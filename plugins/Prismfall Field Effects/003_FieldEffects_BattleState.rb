#===============================================================================
# Prismfall Field Effects - per-battle field state, change_field, battle rules
#===============================================================================
module FieldEffects
  #=============================================================================
  # Battle state access
  #=============================================================================
  # Current field ID of a battle (:NONE if none / not a field-aware battle).
  def self.current(battle)
    return NONE if !battle || !battle.respond_to?(:field_effect)
    return battle.field_effect || NONE
  end

  def self.field_is?(battle, *ids)
    return ids.flatten.include?(self.current(battle))
  end

  def self.stage(battle)
    st = self.raw_state(battle)
    return (st) ? st[:stage] : 1
  end

  def self.raw_state(battle)
    return nil if !battle || !battle.respond_to?(:fe_state)
    return battle.fe_state
  end

  # Scratch Hash for bespoke field procs. Cleared whenever the field changes.
  def self.state(battle)
    st = self.raw_state(battle)
    return {} if !st
    return st[:custom]
  end

  def self.reset_state(battle, keep_stage = false)
    st = battle.fe_state
    stage = (keep_stage && st) ? st[:stage] : 1
    battle.instance_variable_set(:@fe_state, {
      :stage         => stage,
      :turns         => 0,
      :counters      => {},
      :borrowed      => [],
      :borrow_timer  => 0,
      :borrow_cursor => 0,
      :custom        => {},
      :active_defs   => nil,
      :shown         => {},
      :use_id        => (st) ? st[:use_id] : 0,
      :changing      => false
    })
  end

  def self.invalidate_cache(battle)
    st = self.raw_state(battle)
    st[:active_defs] = nil if st
  end

  # Definition of the current field with its stage applied (nil if none).
  def self.current_definition(battle)
    id = self.current(battle)
    return nil if id == NONE
    return self.definition_for(id, self.stage(battle))
  end

  def self.backdrop_for(battle)
    return self.current_definition(battle)&.[](:backdrop)
  end

  # Definitions whose effects currently apply: the current field (stage applied)
  # first, then any borrowed overlays (see :borrow).
  def self.active_defs(battle)
    st = self.raw_state(battle)
    return [] if !st
    return st[:active_defs] if st[:active_defs]
    ret = []
    prim = self.current_definition(battle)
    ret.push(prim) if prim
    st[:borrowed].each do |bid|
      next if bid == self.current(battle)
      view = self.borrowable_view(bid)
      ret.push(view) if view
    end
    st[:active_defs] = ret.freeze
    return ret
  end

  def self.active?(battle)
    return !self.active_defs(battle).empty?
  end

  # All rules of the given list key across active definitions.
  def self.rules(battle, key)
    ret = []
    self.active_defs(battle).each { |d| ret.concat(d[key]) if d[key] }
    return ret
  end

  # All procs for the given hook across active definitions.
  def self.hooks(battle, key)
    ret = []
    self.active_defs(battle).each { |d| ret.push(d[:hooks][key]) if d[:hooks] && d[:hooks][key] }
    return ret
  end

  def self.normalize_id(value)
    return NONE if value.nil? || value == false
    value = value.to_s.strip
    return NONE if value.empty? || value.casecmp?("none")
    return value.upcase.to_sym
  end

  #=============================================================================
  # Messages (shown once per move use)
  #=============================================================================
  def self.begin_move_use(battle)
    st = self.raw_state(battle)
    return if !st
    st[:use_id] += 1
    st[:shown].clear if st[:shown].length > 64
  end

  def self.show_once(battle, user, move, text, *args)
    return if nil_or_empty_text?(text)
    st = self.raw_state(battle)
    return if !st
    key = [st[:use_id], battle.turnCount, user&.index, move&.id, text]
    return if st[:shown][key]
    st[:shown][key] = true
    battle.pbDisplay(self.format(text, *args))
  end

  def self.nil_or_empty_text?(text)
    return text.nil? || (text.is_a?(String) && text.empty?)
  end

  #=============================================================================
  # Field lifecycle
  #=============================================================================
  # Runs when a field becomes active (battle start or after a change).
  def self.on_field_start(battle, old_id, initial)
    defn = self.current_definition(battle)
    return if !defn
    # Remove weather/terrain this field doesn't allow
    if defn[:weather] && defn[:weather][:block]&.include?(battle.field.weather) &&
       battle.field.weather != :None
      battle.field.weather = :None
      battle.field.weatherDuration = 0
      battle.pbDisplay(self.format(defn[:weather][:block_message])) if defn[:weather][:block_message]
      battle.allBattlers.each { |b| b.pbCheckFormOnWeatherChange }
    end
    if defn[:terrain] && defn[:terrain][:block]&.include?(battle.field.terrain) &&
       battle.field.terrain != :None
      battle.field.terrain = :None
      battle.field.terrainDuration = 0
      battle.pbDisplay(self.format(defn[:terrain][:block_message])) if defn[:terrain][:block_message]
      battle.allBattlers.each { |b| b.pbAbilityOnTerrainChange }
    end
    self.safe_call(defn[:hooks][:on_start], battle, old_id) if defn[:hooks]
    self.start_borrowing(battle) if defn[:borrow]
    return if initial
    # On a mid-battle change: re-run "also_on_change" entry effects and seeds
    battle.pbPriority(true).each do |b|
      next if b.fainted?
      self.apply_entry_effects(battle, b, true)
      b.pbFaint if b.fainted?
    end
    self.check_all_seeds(battle)
  end

  def self.on_field_end(battle, new_id)
    defn = self.current_definition(battle)
    self.safe_call(defn[:hooks][:on_end], battle, new_id) if defn && defn[:hooks]
  end

  # Battle start: notify listeners, show the intro message, start effects.
  def self.on_battle_start(battle)
    id = self.current(battle)
    return if id == NONE
    self.notify_change(battle, NONE, id)
    defn = self.current_definition(battle)
    if defn
      battle.pbDisplay(self.format(defn[:intro_message])) if !nil_or_empty_text?(defn[:intro_message])
    else
      self.log("Field :#{id} is set but not registered; it has no effects.")
    end
    self.on_field_start(battle, NONE, true)
  end
end

#===============================================================================
# Battle
#===============================================================================
class Battle
  attr_reader :field_effect
  attr_reader :fe_state

  alias prismfall_fe_initialize initialize
  def initialize(*args)
    prismfall_fe_initialize(*args)
    @field_effect = FieldEffects::NONE
    FieldEffects.reset_state(self)
  end

  # Sets the field before the battle starts (no messages, no events).
  # Used by the battle rule; story code should use setBattleRule("field", :ID).
  def fe_set_initial_field(new_id)
    @field_effect = FieldEffects.normalize_id(new_id)
    FieldEffects.reset_state(self)
  end

  def field_stage
    return @fe_state[:stage]
  end

  # LOCKED API. Changes the field mid-battle. Returns true if it changed.
  #   message:    shown after the change; if nil, the new field's :intro_message
  #               is shown instead (pass "" to show nothing).
  def change_field(new_id, message = nil)
    new_id = FieldEffects.normalize_id(new_id)
    return false if new_id == @field_effect
    return false if @fe_state[:changing]   # No chain reactions within a change
    if new_id != FieldEffects::NONE && !FieldEffects.exists?(new_id)
      FieldEffects.log("change_field: :#{new_id} is not registered; it will have no effects.")
    end
    old_id = @field_effect
    @fe_state[:changing] = true
    begin
      FieldEffects.on_field_end(self, new_id)
      @field_effect = new_id
      FieldEffects.reset_state(self)
      @fe_state[:changing] = true
      PBDebug.log("[Field Effects] Field changed: #{old_id} -> #{new_id}")
      FieldEffects.notify_change(self, old_id, new_id)
      if message.nil?
        intro = FieldEffects.current_definition(self)&.[](:intro_message)
        pbDisplay(FieldEffects.format(intro)) if !FieldEffects.nil_or_empty_text?(intro)
      elsif !message.empty?
        pbDisplay(FieldEffects.format(message))
      end
      FieldEffects.on_field_start(self, old_id, false)
    ensure
      @fe_state[:changing] = false
    end
    return true
  end

  # Changes the current field's stage (see :stages). Returns true if it changed.
  def set_field_stage(new_stage, message = nil)
    return false if @field_effect == FieldEffects::NONE
    new_stage = new_stage.to_i.clamp(1, FieldEffects.max_stage(@field_effect))
    return false if new_stage == @fe_state[:stage]
    old_stage = @fe_state[:stage]
    @fe_state[:stage] = new_stage
    @fe_state[:counters] = {}
    FieldEffects.invalidate_cache(self)
    PBDebug.log("[Field Effects] Field #{@field_effect} stage: #{old_stage} -> #{new_stage}")
    FieldEffects.notify_change(self, @field_effect, @field_effect)
    pbDisplay(FieldEffects.format(message)) if !FieldEffects.nil_or_empty_text?(message)
    return true
  end

  #-----------------------------------------------------------------------------
  # Battle start: intro message and start-of-field effects happen right before
  # the battlers' on-entry effects (entry hazards, abilities, items).
  #-----------------------------------------------------------------------------
  alias prismfall_fe_pbOnAllBattlersEnteringBattle pbOnAllBattlersEnteringBattle
  def pbOnAllBattlersEnteringBattle
    FieldEffects.on_battle_start(self)
    prismfall_fe_pbOnAllBattlersEnteringBattle
  end
end

#===============================================================================
# Battle rule: setBattleRule("field", :VOLCANIC)
#===============================================================================
class Game_Temp
  alias prismfall_fe_add_battle_rule add_battle_rule
  def add_battle_rule(rule, var = nil)
    if rule.to_s.downcase == "field"
      self.battle_rules["field"] = FieldEffects.normalize_id(var)
      return
    end
    prismfall_fe_add_battle_rule(rule, var)
  end
end

module FieldEffects
  # Battle rules that consume the following argument (mirrors setBattleRule).
  BATTLE_RULES_WITH_VALUE = ["terrain", "weather", "environment", "environ", "backdrop",
                             "battleback", "base", "outcome", "outcomevar"].freeze
end

alias prismfall_fe_setBattleRule setBattleRule
def setBattleRule(*args)
  passthrough = []
  i = 0
  while i < args.length
    arg = args[i]
    key = (arg.is_a?(String) || arg.is_a?(Symbol)) ? arg.to_s.downcase : nil
    if key == "field"
      raise _INTL("Argument {1} expected a variable after it but didn't have one.", arg) if i + 1 >= args.length
      $game_temp.add_battle_rule("field", args[i + 1])
      i += 2
      next
    end
    if key && FieldEffects::BATTLE_RULES_WITH_VALUE.include?(key) && i + 1 < args.length
      passthrough.push(arg, args[i + 1])
      i += 2
      next
    end
    passthrough.push(arg)
    i += 1
  end
  prismfall_fe_setBattleRule(*passthrough) if !passthrough.empty?
end

module BattleCreationHelperMethods
  class << self
    alias prismfall_fe_prepare_battle prepare_battle
    def prepare_battle(battle)
      prismfall_fe_prepare_battle(battle)
      FieldEffects.apply_battle_rule(battle)
    end
  end
end

module FieldEffects
  # Decides the field for a battle being prepared: explicit rule > map default.
  def self.apply_battle_rule(battle)
    return if !battle.respond_to?(:fe_set_initial_field)
    rules = $game_temp.battle_rules
    id = nil
    if rules.key?("field")
      id = rules["field"]
    elsif $game_map && MAP_FIELDS[$game_map.map_id]
      id = self.normalize_id(MAP_FIELDS[$game_map.map_id])
    end
    return if id.nil? || id == NONE
    battle.fe_set_initial_field(id)
    # Silently drop overworld weather/terrain the field doesn't allow
    defn = self.definition_for(id)
    if defn && defn[:weather] && defn[:weather][:block]&.include?(battle.field.weather)
      battle.field.defaultWeather  = :None
      battle.field.weather         = :None
      battle.field.weatherDuration = 0
    end
    if defn && defn[:terrain] && defn[:terrain][:block]&.include?(battle.field.terrain)
      battle.field.defaultTerrain  = :None
      battle.field.terrain         = :None
      battle.field.terrainDuration = 0
    end
    # Non-EBDX fallback: use the field's battle background if its graphic
    # exists and no explicit backdrop rule was given.
    backdrop = self.definition_for(id)&.[](:backdrop)
    if backdrop && rules["backdrop"].nil? && battle.respond_to?(:backdrop=) &&
       pbResolveBitmap(sprintf("Graphics/Battlebacks/%s_bg", backdrop))
      battle.backdrop = backdrop
    end
    self.log("Battle field set to :#{id}")
  end
end
