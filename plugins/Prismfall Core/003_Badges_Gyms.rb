#===============================================================================
# Prismfall Core - 003 Badges, gyms, field-move requirements
#-------------------------------------------------------------------------------
# $player.badges is a plain Array (vanilla starts it at [false] * 8); Ruby grows
# it on demand, so badge indexes 0-17 work without core changes. We still pad it
# to 18 entries so debug/UI code that iterates it sees every badge.
#===============================================================================
module Prismfall
  #-----------------------------------------------------------------------------
  # Field-move badge requirements -> Settings::BADGE_FOR_* (editable in 001_Config)
  #-----------------------------------------------------------------------------
  def self.apply_field_move_settings
    set_setting = lambda do |name, value|
      Settings.send(:remove_const, name) if Settings.const_defined?(name, false)
      Settings.const_set(name, value)
    end
    set_setting.call(:FIELD_MOVES_COUNT_BADGES, FIELD_MOVES_COUNT_BADGES)
    FIELD_MOVE_BADGES.each do |move, number|
      const = "BADGE_FOR_#{move}".to_sym
      next if !Settings.const_defined?(const, false)   # only moves Essentials checks
      value = (FIELD_MOVES_COUNT_BADGES) ? number : [number - 1, 0].max
      set_setting.call(const, value)
    end
  end

  #-----------------------------------------------------------------------------
  # Badge helpers
  #-----------------------------------------------------------------------------
  def self.ensure_badge_array
    return if !$player || !$player.badges.is_a?(Array)
    while $player.badges.length < BADGE_COUNT
      $player.badges.push(false)
    end
    $player.badges.map! { |b| b == true }
  end

  # n = gym number 1-18
  def self.has_badge?(n)
    return false if !$player
    return $player.badges[n - 1] == true
  end

  def self.badge_count
    return 0 if !$player
    return (0...BADGE_COUNT).count { |i| $player.badges[i] == true }
  end

  def self.all_badges?
    return badge_count >= BADGE_COUNT
  end

  # 0-based index of the first gym whose badge the player doesn't own, or nil.
  def self.next_gym_index
    return 0 if !$player
    return (0...BADGE_COUNT).find { |i| $player.badges[i] != true }
  end

  # Gym hash for gym number n (1-18).
  def self.gym(n)
    return nil if !n.is_a?(Integer) || n < 1 || n > GYMS.length
    return GYMS[n - 1]
  end

  def self.next_gym
    idx = next_gym_index
    return (idx) ? GYMS[idx] : nil
  end

  def self.gym_for_trainer_type(trainer_type)
    return GYMS.find { |g| g[:trainer_type] == trainer_type }
  end

  # Gives badge n (1-18). Event usage: Prismfall.award_badge(3)
  def self.award_badge(n, announce = ANNOUNCE_CAP_ON_BADGE)
    raise ArgumentError, "Badge number must be 1-#{BADGE_COUNT} (got #{n.inspect})" if !gym(n)
    ensure_badge_array
    already = $player.badges[n - 1]
    $player.badges[n - 1] = true
    $stats.set_time_to_badge(n - 1) if !already && $stats.respond_to?(:set_time_to_badge)
    EventHandlers.trigger(:prismfall_badge_awarded, n)
    if announce && !already && Prismfall::LevelCap.enabled?
      pbMessage(_INTL("The level cap is now Lv. {1}.", Prismfall::LevelCap.current))
    end
    return true
  end

  # Debug/story: remove badge n.
  def self.remove_badge(n)
    return false if !gym(n)
    ensure_badge_array
    $player.badges[n - 1] = false
    return true
  end

  #-----------------------------------------------------------------------------
  # Field rule helper (Field Effects plugin is optional for Core)
  #-----------------------------------------------------------------------------
  def self.field_effects_available?
    return defined?(FieldEffects) ? true : false
  end

  # Queues setBattleRule("field", id) for the next battle if the Field Effects
  # plugin is installed. Returns true if a rule was set.
  def self.set_field_rule(field_id)
    return false if field_id.nil? || field_id == :NONE
    return false if !field_effects_available?
    setBattleRule("field", field_id)
    return true
  end

  #-----------------------------------------------------------------------------
  # Gym battle helper. Event usage:
  #   Prismfall.gym_battle(3)                       -> Marisol on :WATER_SURFACE
  #   Prismfall.gym_battle(9, lose_text: "...")     -> Juno (rival-versioned)
  #   Prismfall.gym_battle(6)                       -> Corvin, double battle (GYMS :double)
  #   Prismfall.gym_battle(6, double: false)        -> force a single battle
  # Returns true if the player won.
  #-----------------------------------------------------------------------------
  # double: nil (default) = follow GYMS[:double]: true (Gyms 2, 6, 11, 16, 17)
  # sets "double", false (Gym 1) sets "single", no key leaves whatever size rule
  # the event set. The double: argument (true / false) overrides both.
  def self.gym_battle(n, lose_text: nil, can_lose: false, field: true, outcome_var: nil, double: nil)
    g = gym(n)
    raise ArgumentError, "Unknown gym #{n.inspect}" if !g
    setBattleRule("canLose") if can_lose
    setBattleRule("outcomeVar", outcome_var) if outcome_var
    set_field_rule(g[:field]) if field
    want_double = double.nil? ? g[:double] : double
    if want_double == true
      setBattleRule("double")
    elsif want_double == false
      setBattleRule("single")
    end
    if g[:rival_battle]
      return Prismfall::Rival.battle(g[:trainer_type], g[:trainer_name], g[:rival_battle],
                                     lose_text: lose_text)
    end
    return TrainerBattle.start([g[:trainer_type], g[:trainer_name], g[:version] || 0, lose_text])
  end
end

Prismfall.apply_field_move_settings
