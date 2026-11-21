#===============================================================================
# Prismfall EBDX Bridge - battler placement (feet on the base).
#-------------------------------------------------------------------------------
# EBDX anchors every battler at a fixed room point (PBS/EBDX/metrics.txt
# BATTLERPOS: foe 234,152 / player 116,252, room px), and every Prismfall room
# paints its bases centred on those points. EBDX then hangs the sprite from that
# point by its bitmap bottom, shifted by the per-species BattlerEnemyY /
# BattlerPlayerY / BattlerAltitude of the base project's PBS/EBDX/pokemon.txt
# (plus EliteBattle::PLAYER_BACKSPRITE_Y_OFFSET). Those numbers do not describe
# the bundled sprites: for 90% of the 1020 front sprites the lowest opaque row
# lands between 2 px above and 26 px below the anchor (median 14 px below), so
# Pokemon stand in front of, or off, their base; back sprites end 20 px above
# to 8 px below; and "floating" species hover at random heights
# (Bronzong's lowest row is 9 px BELOW the base centre, Golbat's 18 px above).
#
# The project's metric source is now this file: the sprite's own pixels. When
# EBDX loads a battler bitmap, the lowest opaque row of each animation frame is
# measured once (cached per file); the median of those rows is put exactly
# FOOT_LINE px from the anchor. Floating species are lifted a constant HOVER px
# above that line; EBDX's ground shadow (squashed silhouette, 1/8 height) stays
# at the base, so they read as hovering over it. Only the vertical origin
# changes: EBDX's X metric and every animation that saves/restores the origin
# (send-out, recall, legacy animations) keep working.
#
#   FOOT_LINE  bitmap px, + = below the anchor (sprite zoom applies: the foe is
#              drawn at 1x and the player at 2x at the battle camera). Foe +16:
#              its feet a little in front of the base centre (the foe base is
#              25 px deep each way at the battle camera), as a creature standing
#              on a disc seen from above shows its front feet. Player +2: just
#              in front of its (1.3x) base's centre.
#   HOVER      bitmap px above the foot line for floating species
#   FLOATING   species => true/false, wins over the automatic rule
#              (EBDX BattlerAltitude > 0, or Levitate for species EBDX has no
#              metrics for, e.g. the Gen 9 pack's statics)
#   FOOT_TWEAK species => [front_dy, back_dy], extra hand tweak in bitmap px
#
# The ally's spot. EBDX stands the single-battle player Pokemon at room
# (116,252), 33 px below the bottom of the screen at the battle camera; with
# its feet on that point a small ally (Joltik, Bidoof, the starters) showed only
# 69-79% of itself. In Prismfall rooms (whose bases art/battlebacks paints
# around bblib.PLAYER) the point is raised PLAYER_RAISE room px: 18 px at the
# battle camera (84-94% shown), and at the send-out pull-back the ally stands a
# little further into the scene. A room whose base is painted higher still adds
# its profile's :player_raise (FROZEN_LAKE). EBDX's stock rooms keep their own point.
#
# Double battles: each Prismfall room's bases are widened (art/battlebacks/
# doubles.py -> elements/dbl_<room>_foe/_ally.png), laid over the room when that
# side has two battlers, and the battlers stand on them (DOUBLE_FOE / DOUBLE_ALLY).
#===============================================================================
module PrismfallEBDX
  GROUND_SPRITES = true
  FOOT_LINE      = { :front => 16, :back => 2 }
  HOVER          = 20
  PLAYER_RAISE   = 8          # room px (EBDX's player point 116,252 -> 116,244 in Prismfall rooms)
  # EBDX gives these an altitude for their animation (a hop, a bounce), but they stand.
  FLOATING = {
    :SKITTY => false, :POLITOED => false, :GROVYLE => false, :KABUTO => false, :FERROTHORN => false,
    :ESCAVALIER => false, :SHELMET => false, :SUNKERN => false, :VICTREEBEL => false, :TIRTOUGA => false,
    :REGICE => false, :PROBOPASS => false
  }
  FOOT_TWEAK = {}
  # Double battles (2 per side; triples keep EBDX's points). Each Prismfall room has widened copies of its own
  # bases, elements/dbl_<room>_foe.png and _ally.png (art/battlebacks/doubles.py), laid over the room when that side
  # has two battlers; the battlers stand on them here (room px; the same numbers as doubles.py). EBDX's own double
  # points (foe 198,152 / 256,164, player 92,240 / 192,262) stood the near foe on the base's front rim and the
  # right-hand ally off its base.
  DOUBLE_FOE  = { 1 => [263, 153], 3 => [205, 151] }
  DOUBLE_ALLY = { 0 => [91, 243], 2 => [175, 246] }
  DOUBLE_Z    = 1          # over the room and its sky-less cut-out (both z 1, drawn earlier), under every other layer

  @ground_cache = {}

  module_function

  # Median over the animation frames of the lowest opaque row, +1 (= the feet line), in bitmap px.
  def sprite_feet(anim)
    return nil if !anim
    file = anim.instance_variable_get(:@bitmapFile)
    frames = anim.instance_variable_get(:@bitmaps) || []
    frames = [anim.bitmap] if frames.empty? && anim.respond_to?(:bitmap) && anim.bitmap
    return nil if frames.empty?
    scale = (anim.respond_to?(:scale) ? anim.scale : 1).to_f
    key = file.is_a?(String) ? [file, scale, frames.length, frames[0].width, frames[0].height] : nil
    return @ground_cache[key] if key && @ground_cache.key?(key)
    step = (scale >= 2 && scale == scale.floor) ? scale.to_i : 1
    picks = frames.length <= 12 ? (0...frames.length).to_a : (0...12).map { |i| (i * (frames.length - 1) / 11.0).round }
    rows = picks.map { |i| lowest_row(frames[i], step) }.compact.sort
    feet = rows.empty? ? nil : rows[rows.length / 2] + 1
    @ground_cache[key] = feet if key
    return feet
  end

  def lowest_row(bmp, step)
    return nil if !bmp || bmp.disposed?
    w, h = bmp.width, bmp.height
    y = h - 1
    while y >= 0
      x = 0
      while x < w
        return y if bmp.get_pixel(x, y).alpha > 40
        x += step
      end
      y -= step
    end
    return nil
  end

  # Widened bases for a double battle: { "img0dbl_foe" => layer, ... } for the sides that have two battlers.
  def double_layers(data, battle)
    return {} if !GROUND_SPRITES || !battle || !data.is_a?(Hash) || !data["prismfall_field"]
    bd = data["backdrop"].to_s
    return {} if !bd.start_with?("field_") || battle.pbMaxSize != 2
    inv = 1.0 / room_scale
    ret = {}
    [[0, "ally"], [1, "foe"]].each do |side, tag|
      next if battle.pbSideSize(side) != 2
      path = EBDX_ELEMENTS + "dbl_#{bd}_#{tag}"
      next if !pbResolveBitmap(path)
      ret["img0dbl_#{tag}"] = { :bitmap => path, :flat => true, :x => 0, :y => 0, :ox => 0, :oy => 0,
                                :zoom_x => inv, :zoom_y => inv, :z => DOUBLE_Z }
    end
    return ret
  end

  # Extra raise of the ally's point for one room (room px): its base was painted higher
  # (art/battlebacks bblib.ROOM_PLAYER -> the field's generated profile :player_raise).
  def room_player_raise(field_id, battle = nil)
    return 0 if field_id.nil? || field_id == :NONE
    stage = battle ? current_stage(battle) : 1
    return (profile_for(field_id, stage)[:player_raise] || 0).to_i
  end

  def floating?(species, form = 0)
    return false if species.nil?
    sp = species.to_s.upcase.to_sym
    return FLOATING[sp] if FLOATING.key?(sp)
    alt = (EliteBattle.get_data(species, :Species, :ALTITUDE, form) rescue nil)
    return alt > 0 if alt.is_a?(Numeric)
    data = (GameData::Species.get_species_form(species, form) rescue nil)
    return false if !data
    return (data.abilities + data.hidden_abilities).include?(:LEVITATE)
  end

  # New vertical origin for a DynamicPokemonSprite (nil = leave EBDX's).
  def grounded_oy(anim, species, form, back)
    feet = sprite_feet(anim)
    return nil if !feet
    t = FOOT_LINE[back ? :back : :front]
    t -= HOVER if floating?(species, form)
    tw = FOOT_TWEAK[species.to_s.upcase.to_sym]
    t += (back ? tw[1] : tw[0]) if tw
    return feet - t
  end
end

if defined?(DynamicPokemonSprite) && defined?(EliteBattle)
  class DynamicPokemonSprite
    alias prismfall_refreshMetrics refreshMetrics unless method_defined?(:prismfall_refreshMetrics)
    def refreshMetrics(metrics = nil, species = nil)
      prismfall_refreshMetrics(metrics, species)
      return if !PrismfallEBDX::GROUND_SPRITES || !@pokemon || !@bitmap
      begin
        sp = species.nil? ? @pokemon.species : species
        oy = PrismfallEBDX.grounded_oy(@bitmap, sp, (@pokemon.form rescue 0), @index % 2 == 0)
        return if oy.nil?
        @sprite.oy = oy
        @oy = oy
      rescue StandardError => e
        PrismfallEBDX.log_error("DynamicPokemonSprite#refreshMetrics", e)
      end
    end

    # EBDX rebuilds the origin from its own metrics when a Substitute ends; keep ours.
    alias prismfall_removeSubstitute removeSubstitute unless method_defined?(:prismfall_removeSubstitute)
    def removeSubstitute
      prismfall_removeSubstitute
      return if !PrismfallEBDX::GROUND_SPRITES || @oy.nil?
      @sprite.ox = @ox
      @sprite.oy = @oy
      formatShadow
    end
  end

  class BattleSceneRoom
    # Prismfall rooms (art named field_*) paint the player's base at the raised point (see PLAYER_RAISE).
    alias prismfall_place_adjustMetrics adjustMetrics unless method_defined?(:prismfall_place_adjustMetrics)
    def adjustMetrics
      prismfall_place_adjustMetrics
      return if !PrismfallEBDX::GROUND_SPRITES
      return if !@data.is_a?(Hash) || !@data["prismfall_field"] || !@data["backdrop"].to_s.start_with?("field_")
      return if !@battle
      if @battle.pbMaxSize == 2
        prismfall_double_points
        return
      end
      return if @battle.pbMaxSize > 1
      lift = PrismfallEBDX::PLAYER_RAISE + PrismfallEBDX.room_player_raise(@data["prismfall_field"], @battle)
      b = @sprites["battler0"]
      b.ey -= lift if b && b.ey && lift != 0
    rescue StandardError => e
      PrismfallEBDX.log_error("BattleSceneRoom#adjustMetrics", e)
    end

    # Doubles: stand each side's two battlers on its widened base (only where the room has one).
    def prismfall_double_points
      lift = PrismfallEBDX.room_player_raise(@data["prismfall_field"], @battle)
      [[PrismfallEBDX::DOUBLE_ALLY, "img0dbl_ally", lift], [PrismfallEBDX::DOUBLE_FOE, "img0dbl_foe", 0]].each do |pts, key, dy|
        next if !@data[key]
        pts.each do |i, (x, y)|
          b = @sprites["battler#{i}"]
          next if !b
          b.ex = x
          b.ey = y - dy
        end
        next if key != "img0dbl_foe" || !@battle.opponent || @battle.opponent.length < 2
        pts.each do |i, (x, y)|
          t = @sprites["trainer_#{i}"]
          next if !t
          t.ex = x
          t.ey = y
        end
      end
    end

    # Doubles: add the widened bases to the room before EBDX draws it (EBDX's refresh draws from @data).
    alias prismfall_place_refresh refresh unless method_defined?(:prismfall_place_refresh)
    def refresh(*args)
      if args[0].is_a?(Hash)
        begin
          @data.delete("img0dbl_ally") if @data.is_a?(Hash)
          @data.delete("img0dbl_foe") if @data.is_a?(Hash)
          extra = PrismfallEBDX.double_layers(@data, @battle)
          extra.each { |k, v| @data[k] = v }
        rescue StandardError => e
          PrismfallEBDX.log_error("BattleSceneRoom#refresh (doubles)", e)
        end
      end
      prismfall_place_refresh(*args)
    end
  end

  # Send-out landing: a floating Pokemon doesn't shake the screen (EBDX asks for its altitude).
  if defined?(getBattlerAltitude)
    alias prismfall_getBattlerAltitude getBattlerAltitude unless defined?(prismfall_getBattlerAltitude)
    def getBattlerAltitude(battler)
      return prismfall_getBattlerAltitude(battler) if !PrismfallEBDX::GROUND_SPRITES || battler.nil?
      sp = (battler.displaySpecies rescue nil)
      return prismfall_getBattlerAltitude(battler) if sp.nil?
      return PrismfallEBDX.floating?(sp, (battler.displayForm rescue 0)) ? PrismfallEBDX::HOVER : 0
    end
  end
end
