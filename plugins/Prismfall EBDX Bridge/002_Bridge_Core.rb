#===============================================================================
# Prismfall EBDX Bridge - resolver, helpers and event dispatch
#===============================================================================
module PrismfallEBDX
  EBDX_BATTLEBG = "Graphics/EBDX/Battlebacks/battlebg/"
  EBDX_BASE     = "Graphics/EBDX/Battlebacks/base/"
  EBDX_ELEMENTS = "Graphics/EBDX/Battlebacks/elements/"
  VANILLA_DIR   = "Graphics/Battlebacks/"

  @bitmap_cache = {}

  module_function

  #-----------------------------------------------------------------------------
  # Logging (never raise from a visual-only plugin)
  #-----------------------------------------------------------------------------
  def log(msg)
    PBDebug.log("[Prismfall EBDX Bridge] #{msg}") if defined?(PBDebug)
  end

  def log_error(where, err)
    msg = "#{where}: #{err.class}: #{err.message}"
    log(msg)
    err.backtrace&.first(4)&.each { |line| log("  #{line}") }
    if $DEBUG && defined?(Console) && Console.respond_to?(:echo_warn)
      Console.echo_warn("[Prismfall EBDX Bridge] #{msg}")
    end
  end

  #-----------------------------------------------------------------------------
  # Environment detection
  #-----------------------------------------------------------------------------
  def ebdx?
    return defined?(EliteBattle) && defined?(BattleSceneRoom) ? true : false
  end

  def ebdx_room(scene)
    return nil if !ebdx? || !scene.respond_to?(:sprites)
    sprites = scene.sprites
    return nil if !sprites.is_a?(Hash)
    room = sprites["battlebg"]
    return nil if !room.is_a?(BattleSceneRoom) || room.disposed?
    return room
  end

  def vanilla_scene?(scene)
    return false if !scene.respond_to?(:sprites) || !scene.sprites.is_a?(Hash)
    return false if ebdx_room(scene)
    return !scene.sprites["battle_bg"].nil?
  end

  #-----------------------------------------------------------------------------
  # Field data (reads the Field Effects public API, see design/FIELD_API.md)
  #-----------------------------------------------------------------------------
  def current_field(battle)
    return :NONE if !battle
    return FieldEffects.current(battle) if defined?(FieldEffects) && FieldEffects.respond_to?(:current)
    return (battle.respond_to?(:field_effect) && battle.field_effect) || :NONE
  end

  def current_stage(battle)
    return 1 if !defined?(FieldEffects) || !FieldEffects.respond_to?(:stage)
    return FieldEffects.stage(battle) || 1
  end

  # Stage-aware :backdrop base name of a field ("field_volcanic").
  def backdrop_name(field_id, stage = 1)
    return nil if field_id.nil? || field_id == :NONE
    defn = nil
    if defined?(FieldEffects)
      if FieldEffects.respond_to?(:definition_for)
        defn = FieldEffects.definition_for(field_id, stage)
      elsif FieldEffects.respond_to?(:get)
        defn = FieldEffects.get(field_id)
      end
    end
    name = defn[:backdrop] if defn.is_a?(Hash)
    name = "field_#{field_id.to_s.downcase}" if name.nil? || name.to_s.empty?
    return name.to_s
  end

  def profile_for(field_id, stage = 1)
    base = PROFILES[field_id] || DEFAULT_PROFILE
    return base if !base[:stages] || stage.nil? || stage <= 1
    over = base[:stages][stage]
    over ||= base[:stages][base[:stages].keys.select { |k| k <= stage }.max] if !base[:stages].empty?
    return over ? base.merge(over) : base
  end

  # Identifies what the room currently shows, to skip redundant swaps.
  def signature(battle)
    id = current_field(battle)
    return [:NONE] if id == :NONE
    stage = current_stage(battle)
    return [id, stage, backdrop_name(id, stage)]
  end

  #-----------------------------------------------------------------------------
  # Transitions
  #-----------------------------------------------------------------------------
  def transition_for(old_id, new_id)
    t = TRANSITION_OVERRIDES[[old_id, new_id]] ||
        TRANSITION_OVERRIDES[[:ANY, new_id]] ||
        TRANSITION_OVERRIDES[[old_id, :ANY]]
    t ||= profile_for(new_id)[:transition] if new_id && new_id != :NONE
    t ||= DEFAULT_TRANSITION
    t = TRANSITIONS[t] if TRANSITIONS.key?(t)
    return t   # [r, g, b] or EBDX common animation Symbol
  end

  def to_color(rgb, alpha = 255)
    return Color.new(rgb[0] || 0, rgb[1] || 0, rgb[2] || 0, alpha)
  end

  #-----------------------------------------------------------------------------
  # Plain-data deep copy (EBDX environment Hashes hold strings/numbers/arrays)
  #-----------------------------------------------------------------------------
  def deep_dup(obj)
    case obj
    when Hash   then obj.each_with_object({}) { |(k, v), h| h[k] = deep_dup(v) }
    when Array  then obj.map { |v| deep_dup(v) }
    when String then obj.dup
    else obj
    end
  end

  #-----------------------------------------------------------------------------
  # EBDX room data for a field (nil for :NONE)
  #-----------------------------------------------------------------------------
  def room_data(field_id, stage = 1)
    return nil if field_id.nil? || field_id == :NONE
    profile = profile_for(field_id, stage)
    bd = backdrop_name(field_id, stage)
    # A stage without its own art reuses the stage-1 art (not the stock fallback).
    if stage && stage > 1 && !pbResolveBitmap(EBDX_BATTLEBG + bd)
      base_bd = backdrop_name(field_id, 1)
      bd = base_bd if pbResolveBitmap(EBDX_BATTLEBG + base_bd)
    end
    outdoor = profile[:outdoor] && ebdx_outdoor_now?
    art = nil
    if outdoor && PBDayNight.isNight? && pbResolveBitmap(EBDX_BATTLEBG + bd + "_night")
      art = bd + "_night"
    elsif pbResolveBitmap(EBDX_BATTLEBG + bd)
      art = bd
    end
    if art
      data = { "backdrop" => art }
      # HD art: <art>_hd.png is the same room painted at ROOM_SCALE resolution (864x693). It is
      # drawn as a flat EBDX layer at 1/ROOM_SCALE zoom, so the default camera shows it 1:1.
      if HD_ART && pbResolveBitmap(EBDX_BATTLEBG + art + "_hd")
        inv = 1.0 / room_scale
        data["img000"] = { :bitmap => EBDX_BATTLEBG + art + "_hd", :flat => true, :x => 0, :y => 0,
                           :ox => 0, :oy => 0, :zoom_x => inv, :zoom_y => inv, :z => 0 }
      end
      data["base"] = bd if pbResolveBitmap(EBDX_BASE + bd)
      if pbResolveBitmap(EBDX_ELEMENTS + bd + "_fog")
        data["img090"] = { :bitmap => bd + "_fog", :scrolling => true, :speed => 0.5,
                           :oy => 0, :z => 30, :flat => true }
      end
      (profile[:art_extras] || {}).each do |k, v|
        # Skip (and log) EBDX image layers whose graphic is missing, so a partial art drop never crashes.
        if v.is_a?(Hash) && v[:bitmap] && !pbResolveBitmap(v[:bitmap].to_s) &&
           !pbResolveBitmap(EBDX_ELEMENTS + v[:bitmap].to_s)
          log("Missing element '#{v[:bitmap]}' for :#{field_id} (#{k}); layer skipped.")
          next
        end
        data[k] = deep_dup(v)
      end
      data["prismfall_tone"] = profile[:art_tone] if profile[:art_tone]
    else
      data = fallback_room(profile[:fallback])
      (profile[:fallback_extras] || {}).each { |k, v| data[k] = deep_dup(v) }
      data["prismfall_tone"] = profile[:tone] if profile[:tone]
      log("No EBDX art '#{EBDX_BATTLEBG}#{bd}' for :#{field_id}; using fallback room.")
    end
    data["outdoor"] = true if outdoor
    data["prismfall_fx"] = deep_dup(profile[:fx] || []) if AMBIENT_FX
    # Animated art layers only belong to the field's own art (the fallback room has none of it).
    if art && AMBIENT_LAYERS
      layers = (profile[:layers] || []).select { |l| l[:bitmap].nil? || pbResolveBitmap(EBDX_ELEMENTS + l[:bitmap].to_s) }
      data["prismfall_layers"] = deep_dup(layers)
    end
    data["prismfall_field"] = field_id
    return data
  end

  def room_scale
    return (defined?(EliteBattle::ROOM_SCALE) ? EliteBattle::ROOM_SCALE : 2.25).to_f
  end

  def fallback_room(fallback)
    data = nil
    if fallback.is_a?(Hash)
      data = deep_dup(fallback)
    elsif fallback.is_a?(Symbol) && defined?(EnvironmentEBDX) && EnvironmentEBDX.const_defined?(fallback)
      data = deep_dup(EnvironmentEBDX.const_get(fallback))
    end
    if data.nil? && defined?(EnvironmentEBDX)
      const = ebdx_outdoor_now? ? :OUTDOOR : :INDOOR
      data = deep_dup(EnvironmentEBDX.const_get(const)) if EnvironmentEBDX.const_defined?(const)
    end
    return data || { "backdrop" => "IndoorA" }
  end

  def ebdx_outdoor_now?
    return false if !defined?(EliteBattle) || !EliteBattle.respond_to?(:outdoor_map?)
    return false if !Settings::TIME_SHADING
    return (EliteBattle.outdoor_map? rescue false) ? true : false
  end

  #-----------------------------------------------------------------------------
  # Generated particle bitmaps: white shapes, tinted per sprite via Sprite#color.
  # Cached for the whole session (a few tiny bitmaps).
  #-----------------------------------------------------------------------------
  def particle_bitmap(spec)
    if spec[:bitmap]
      return pbBitmap(EBDX_ELEMENTS + spec[:bitmap].to_s) if defined?(pbBitmap)
      return RPG::Cache.load_bitmap(EBDX_ELEMENTS, spec[:bitmap].to_s)
    end
    shape = spec[:shape] || :dot
    size = [(spec[:size] || 3).to_i, 1].max
    w = (spec[:w] || size).to_i
    h = (spec[:h] || size).to_i
    key = [shape, size, w, h]
    bmp = @bitmap_cache[key]
    return bmp if bmp && !bmp.disposed?
    bmp = make_shape(shape, size, w, h)
    @bitmap_cache[key] = bmp
    return bmp
  end

  def make_shape(shape, size, w, h)
    white = proc { |a| Color.new(255, 255, 255, a) }
    case shape
    when :rect
      bmp = Bitmap.new([w, 1].max, [h, 1].max)
      bmp.fill_rect(0, 0, bmp.width, bmp.height, white.call(255))
    when :glow   # soft radial-ish blob built from nested squares
      bmp = Bitmap.new(size, size)
      layers = (size + 1) / 2
      layers.times do |i|
        a = (255 * (i + 1) / layers.to_f).round
        bmp.fill_rect(i, i, size - (2 * i), size - (2 * i), white.call(a))
      end
      if size >= 3
        [[0, 0], [size - 1, 0], [0, size - 1], [size - 1, size - 1]].each do |p|
          bmp.set_pixel(p[0], p[1], white.call(0))
        end
      end
    when :puff   # soft round cloud (steam, smoke, spores): radial alpha falloff
      bmp = Bitmap.new(size, size)
      r = size / 2.0
      size.times do |yy|
        size.times do |xx|
          d = Math.sqrt(((xx + 0.5 - r)**2) + ((yy + 0.5 - r)**2)) / r
          next if d >= 1
          bmp.set_pixel(xx, yy, white.call((255 * ((1 - d)**1.5)).round))
        end
      end
    when :spark  # four-point star
      s = size.odd? ? size : size + 1
      bmp = Bitmap.new(s, s)
      c = s / 2
      bmp.fill_rect(c, 0, 1, s, white.call(170))
      bmp.fill_rect(0, c, s, 1, white.call(170))
      bmp.fill_rect(c - 1, c - 1, 3, 3, white.call(210)) if s >= 5
      bmp.set_pixel(c, c, white.call(255))
    else         # :dot
      bmp = Bitmap.new(size, size)
      bmp.fill_rect(0, 0, size, size, white.call(255))
      if size >= 3
        [[0, 0], [size - 1, 0], [0, size - 1], [size - 1, size - 1]].each do |p|
          bmp.set_pixel(p[0], p[1], white.call(110))
        end
      end
    end
    return bmp
  end

  #-----------------------------------------------------------------------------
  # Event entry points
  #-----------------------------------------------------------------------------
  def on_field_changed(battle, old_id, new_id)
    return if !ENABLED || !battle
    scene = battle.scene
    return if !scene
    if ebdx_room(scene)
      EBDX.swap(scene, battle, old_id, new_id)
    elsif vanilla_scene?(scene)
      Vanilla.swap(scene, battle, old_id, new_id)
    end
  rescue StandardError => e
    log_error("on_field_changed(#{old_id.inspect} -> #{new_id.inspect})", e)
  end

  def on_overlay_changed(battle, field_id, old_ids, new_ids)
    return if !ENABLED || !AMBIENT_FX || !battle
    room = ebdx_room(battle.scene)
    return if !room
    specs = []
    (new_ids || []).first(OVERLAY_MAX_FIELDS).each do |bid|
      next if bid.nil? || bid == :NONE || bid == field_id
      (profile_for(bid)[:fx] || []).each do |spec|
        next if spec[:type] == :flash
        s = deep_dup(spec)
        s[:count] = [((s[:count] || 10) * OVERLAY_FX_SCALE).round, 1].max
        specs.push(s)
      end
    end
    room.prismfall_set_overlay_fx(specs)
    flash = profile_for(field_id)[:flash]
    room.prismfall_flash(flash, 150, 16) if flash
  rescue StandardError => e
    log_error("on_overlay_changed(#{field_id.inspect})", e)
  end

  #-----------------------------------------------------------------------------
  # Public helpers for story scripts
  #-----------------------------------------------------------------------------
  # Re-sync the battle backdrop with the battle's current field (no-op if equal).
  def refresh(battle)
    on_field_changed(battle, current_field(battle), current_field(battle))
  end

  # EBDX room Hash for a field, e.g. for EliteBattle.set(:nextBattleBack, ...)
  # in a cutscene battle that has no field effect.
  def environment_for(field_id, stage = 1)
    return room_data(field_id, stage)
  end
end
