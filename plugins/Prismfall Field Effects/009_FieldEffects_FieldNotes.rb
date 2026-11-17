#===============================================================================
# Prismfall Field Effects - Field Notes (in-game field encyclopedia)
#-------------------------------------------------------------------------------
# Records every field the player battles on (save data :prismfall_field_notes)
# and shows them from the pause menu. Unseen fields are listed as "???".
# Text comes from the field's :description plus :notes (if given) or lines
# generated from its definition.
#===============================================================================
module FieldEffects
  module FieldNotes
    def self.data
      @data = {} if !@data.is_a?(Hash)
      return @data
    end

    def self.data=(value)
      @data = (value.is_a?(Hash)) ? value : {}
    end

    def self.seen?(id); return self.data.key?(id); end
    def self.count(id); return (self.data[id]) ? self.data[id][:count].to_i : 0; end
    def self.seen_count; return self.ids.count { |i| self.seen?(i) }; end

    # Called whenever a field becomes active in a player battle.
    def self.record(battle, id)
      return if id.nil? || id == NONE || !FieldEffects.exists?(id)
      return if !$player || (battle.respond_to?(:internalBattle) && !battle.internalBattle)
      entry = (self.data[id] ||= { :count => 0 })
      entry[:count] += 1
    end

    # Display order: SPINE roster, then the Revision 10 fields, then any others.
    def self.ids
      known = KNOWN_FIELDS.select { |i| FieldEffects.exists?(i) }
      return known + (FieldEffects.ids - known)
    end

    FAMILY_NAMES = { :elemental => "Elemental", :telluric => "Telluric",
                     :synthetic => "Synthetic", :magical => "Magical" }.freeze

    # "Elemental field - reacts to the Elemental Seed." (nil if no :family)
    def self.family_line(id)
      fam = FieldEffects.get(id)&.[](:family)
      return nil if !fam || !FAMILY_NAMES[fam]
      seed = FAMILY_SEEDS[fam]
      seed_name = (seed && GameData::Item.exists?(seed)) ? GameData::Item.get(seed).name : seed.to_s
      return _INTL("{1} field - reacts to the {2}.", _INTL(FAMILY_NAMES[fam]), seed_name)
    end

    def self.name(klass, id)
      data = klass.try_get(id)
      return (data) ? data.name : id.to_s
    end

    def self.mult_text(m)
      return (m == m.to_i) ? m.to_i.to_s : sprintf("%.2f", m).sub(/0+\z/, "")
    end

    def self.field_label(id)
      return _INTL("no field") if id == NONE
      return (self.seen?(id)) ? FieldEffects.name_of(id) : "???"
    end

    # Short player-facing summary lines for a field.
    def self.effect_lines(id)
      defn = FieldEffects.get(id)
      return [] if !defn
      return Array(defn[:notes]).map { |n| _INTL(n) } if defn[:notes]
      ret = []
      ret.push(_INTL("Type matchups are reversed.")) if defn[:inverse]
      if defn[:type_mods]
        up = defn[:type_mods].select { |_t, m| m > 1 }
        down = defn[:type_mods].select { |_t, m| m < 1 }
        if !up.empty?
          ret.push(_INTL("Boosted: {1}", up.map { |t, m| "#{self.name(GameData::Type, t)} x#{self.mult_text(m)}" }.join(", ")))
        end
        if !down.empty?
          ret.push(_INTL("Weakened: {1}", down.map { |t, m| "#{self.name(GameData::Type, t)} x#{self.mult_text(m)}" }.join(", ")))
        end
      end
      if defn[:move_mods] && !defn[:move_mods].empty?
        strong = defn[:move_mods].select { |_m, x| x > 1 }.sort_by { |_m, x| -x }.first(4)
        ret.push(_INTL("Moves boosted: {1}", strong.map { |m, _x| self.name(GameData::Move, m) }.join(", "))) if !strong.empty?
      end
      ret.push(_INTL("Some type matchups are altered.")) if defn[:effectiveness_mods]
      ret.push(_INTL("Some moves change or gain types.")) if defn[:type_changes] || defn[:extra_types]
      ret.push(_INTL("Some moves fail here.")) if defn[:move_fails]
      ret.push(_INTL("Some moves gain extra effects.")) if defn[:added_effects] || defn[:move_stat_boosts]
      ret.push(_INTL("Speed is affected.")) if defn[:speed_mods]
      ret.push(_INTL("Affects Pokémon as they enter.")) if defn[:on_entry]
      ret.push(_INTL("Has end-of-turn effects.")) if defn[:end_of_round]
      if defn[:weather] && defn[:weather][:block]
        ret.push(_INTL("Blocks weather: {1}", defn[:weather][:block].map { |w| self.name(GameData::BattleWeather, w) }.join(", ")))
      end
      if defn[:terrain] && defn[:terrain][:block]
        ret.push(_INTL("Blocks terrain: {1}", defn[:terrain][:block].map { |t| self.name(GameData::BattleTerrain, t) }.join(", ")))
      end
      ret.push(_INTL("Borrows the effects of other fields.")) if defn[:borrow]
      ret.push(_INTL("Grows through {1} stages.", FieldEffects.max_stage(id))) if defn[:stages]
      if defn[:transitions]
        targets = defn[:transitions].map { |t| t[:to] }.select { |t| t.is_a?(Symbol) }.uniq
        ret.push(_INTL("Can become: {1}", targets.map { |t| self.field_label(t) }.join(", "))) if !targets.empty?
      end
      if defn[:seed]
        seeds = defn[:seed].map { |s| s[:item] }.uniq
        ret.push(_INTL("Reacts to: {1}", seeds.map { |s| self.name(GameData::Item, s) }.join(", ")))
      end
      return ret
    end
  end

  # Hook into field activation (battle start and mid-battle changes).
  class << self
    alias prismfall_fn_on_field_start on_field_start
    def on_field_start(battle, old_id, initial)
      FieldNotes.record(battle, self.current(battle))
      prismfall_fn_on_field_start(battle, old_id, initial)
    end
  end
end

SaveData.register(:prismfall_field_notes) do
  save_value { FieldEffects::FieldNotes.data }
  load_value { |value| FieldEffects::FieldNotes.data = value }
  new_game_value { {} }
end

#===============================================================================
# Scene (code-drawn: no graphics needed)
#===============================================================================
class PrismfallFieldNotes_Scene
  LIST_WIDTH  = 200
  BASE_COLOR   = Color.new(248, 248, 248)
  SHADOW_COLOR = Color.new(72, 72, 88)
  DIM_COLOR    = Color.new(176, 176, 200)

  def pbStartScene
    @viewport = Viewport.new(0, 0, Graphics.width, Graphics.height)
    @viewport.z = 99999
    @sprites = {}
    @ids = FieldEffects::FieldNotes.ids
    @sprites["bg"] = BitmapSprite.new(Graphics.width, Graphics.height, @viewport)
    @sprites["bg"].bitmap.fill_rect(0, 0, Graphics.width, Graphics.height, Color.new(24, 20, 40))
    @sprites["bg"].bitmap.fill_rect(LIST_WIDTH, 0, 2, Graphics.height, Color.new(120, 96, 200))
    commands = @ids.map { |id| FieldEffects::FieldNotes.seen?(id) ? FieldEffects.name_of(id) : "???" }
    commands = [_INTL("(no fields)")] if commands.empty?
    @sprites["list"] = Window_CommandPokemon.newWithSize(commands, 0, 0, LIST_WIDTH, Graphics.height, @viewport)
    @sprites["panel"] = BitmapSprite.new(Graphics.width - LIST_WIDTH - 2, Graphics.height, @viewport)
    @sprites["panel"].x = LIST_WIDTH + 2
    pbSetSystemFont(@sprites["panel"].bitmap)
    @index = -1
    @page = 0
    refresh_panel
    pbFadeInAndShow(@sprites) { pbUpdate }
  end

  def wrap(bitmap, text, width)
    lines = []
    text.to_s.split("\n").each do |para|
      line = ""
      para.split(" ").each do |word|
        trial = (line.empty?) ? word : "#{line} #{word}"
        if bitmap.text_size(trial).width > width && !line.empty?
          lines.push(line)
          line = word
        else
          line = trial
        end
      end
      lines.push(line)
    end
    return lines
  end

  def refresh_panel
    bitmap = @sprites["panel"].bitmap
    bitmap.clear
    w = bitmap.width - 24
    id = @ids[@sprites["list"].index]
    textpos = []
    seen_total = FieldEffects::FieldNotes.seen_count
    textpos.push([_INTL("Field Notes  {1}/{2}", seen_total, @ids.length), 12, 10, :left, DIM_COLOR, SHADOW_COLOR])
    lines = []
    if !id
      lines = [_INTL("No fields are known.")]
    elsif !FieldEffects::FieldNotes.seen?(id)
      textpos.push(["???", 12, 40, :left, BASE_COLOR, SHADOW_COLOR])
      lines = [_INTL("You haven't battled on this field yet.")]
    else
      defn = FieldEffects.get(id)
      textpos.push([defn[:name], 12, 40, :left, BASE_COLOR, SHADOW_COLOR])
      textpos.push([_INTL("Battled here: {1}", FieldEffects::FieldNotes.count(id)), w + 12, 40, :right,
                    DIM_COLOR, SHADOW_COLOR])
      lines.concat(wrap(bitmap, _INTL(defn[:description]), w)) if defn[:description]
      fam = FieldEffects::FieldNotes.family_line(id)
      lines.concat(wrap(bitmap, fam, w)) if fam
      lines.push("")
      FieldEffects::FieldNotes.effect_lines(id).each { |l| lines.concat(wrap(bitmap, "- " + l, w)) }
    end
    per_page = (bitmap.height - 80 - 24) / 28
    @pages = [(lines.length + per_page - 1) / per_page, 1].max
    @page = @page.clamp(0, @pages - 1)
    lines[@page * per_page, per_page]&.each_with_index do |l, i|
      textpos.push([l, 12, 76 + (i * 28), :left, BASE_COLOR, SHADOW_COLOR])
    end
    if @pages > 1
      textpos.push([_INTL("{1}/{2}  USE: next page", @page + 1, @pages), w + 12, bitmap.height - 30,
                    :right, DIM_COLOR, SHADOW_COLOR])
    end
    pbDrawTextPositions(bitmap, textpos)
  end

  def pbUpdate
    pbUpdateSpriteHash(@sprites)
  end

  def pbMain
    loop do
      Graphics.update
      Input.update
      pbUpdate
      if @sprites["list"].index != @index
        @index = @sprites["list"].index
        @page = 0
        refresh_panel
      end
      if Input.trigger?(Input::BACK)
        pbPlayCloseMenuSE
        break
      elsif Input.trigger?(Input::USE) && @pages > 1
        pbPlayCursorSE
        @page = (@page + 1) % @pages
        refresh_panel
      end
    end
  end

  def pbEndScene
    pbFadeOutAndHide(@sprites) { pbUpdate }
    pbDisposeSpriteHash(@sprites)
    @viewport.dispose
  end
end

def pbPrismfallFieldNotes
  pbFadeOutIn do
    scene = PrismfallFieldNotes_Scene.new
    scene.pbStartScene
    scene.pbMain
    scene.pbEndScene
  end
end

MenuHandlers.add(:pause_menu, :prismfall_field_notes, {
  "name"      => _INTL("Field Notes"),
  "order"     => 45,
  "condition" => proc { next FieldEffects::FieldNotes.seen_count > 0 },
  "effect"    => proc { |menu|
    pbPlayDecisionSE
    pbPrismfallFieldNotes
    menu.pbRefresh
    next false
  }
})
