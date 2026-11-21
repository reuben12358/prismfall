#===============================================================================
# Prismfall Field Effects - rule evaluation engine
#-------------------------------------------------------------------------------
# Pure logic used by the Battle/Battler/Move/AI hooks in later files.
#===============================================================================
module FieldEffects
  DEFAULT_FAIL_MESSAGE        = "But it failed!"
  DEFAULT_SEED_MESSAGE        = "{1}'s {2} reacted to the field!"
  DEFAULT_WEATHER_BLOCK_TEXT  = "The field prevented the weather from changing!"
  DEFAULT_TERRAIN_BLOCK_TEXT  = "The field prevented the terrain from changing!"

  #=============================================================================
  # Matchers
  #=============================================================================
  # rule: Hash containing any MOVE_MATCH_KEYS. target may be nil (then a rule
  # with a target: matcher never matches). type is the move's type this use.
  def self.move_matches?(rule, battle, user, target, move, type)
    return false if !move
    return false if rule[:moves] && !rule[:moves].include?(move.id)
    return false if rule[:not_moves]&.include?(move.id)
    return false if rule[:types] && !rule[:types].include?(type)
    return false if rule[:not_types]&.include?(type)
    return false if rule[:flags] && rule[:flags].none? { |f| self.move_has_flag?(move, f, user) }
    return false if rule[:category] && rule[:category].none? { |c| self.category_matches?(move, c, type) }
    return false if rule[:function_codes] && !rule[:function_codes].include?(move.function_code)
    return false if rule[:user] && !self.battler_matches?(rule[:user], battle, user)
    return false if rule[:target] && !self.battler_matches?(rule[:target], battle, target)
    return false if rule[:in_weather] && !rule[:in_weather].include?(battle.pbWeather)
    return false if rule[:on_terrain] && !rule[:on_terrain].include?(battle.field.terrain)
    return false if rule[:condition] && !self.safe_call(rule[:condition], battle, user, target, move, type)
    return true
  end

  def self.move_has_flag?(move, flag, user = nil)
    flag = flag.to_s
    if flag.casecmp?("Contact")
      return (user) ? move.pbContactMove?(user) : move.contactMove?
    end
    return move.flags.any? { |f| f.casecmp?(flag) }
  end

  def self.category_matches?(move, category, type)
    case category
    when :physical then return move.damagingMove? && move.physicalMove?(type)
    when :special  then return move.damagingMove? && move.specialMove?(type)
    when :status   then return move.statusMove?
    when :damaging then return move.damagingMove?
    end
    return false
  end

  # spec: Hash containing any BATTLER_MATCH_KEYS.
  def self.battler_matches?(spec, battle, battler)
    return false if !battler
    return true if !spec
    return false if spec[:types] && spec[:types].none? { |t| battler.pbHasType?(t) }
    return false if spec[:not_types]&.any? { |t| battler.pbHasType?(t) }
    return false if spec[:abilities] && !battler.hasActiveAbility?(spec[:abilities])
    return false if spec[:not_abilities] && battler.hasActiveAbility?(spec[:not_abilities])
    return false if spec[:items] && !battler.hasActiveItem?(spec[:items])
    return false if spec[:not_items] && battler.hasActiveItem?(spec[:not_items])
    if spec.key?(:grounded)
      return false if spec[:grounded] == battler.airborne?
    end
    if spec[:status]
      st = battler.status
      ok = spec[:status].include?(st) || (st == :POISON && spec[:status].include?(:TOXIC))
      return false if !ok
    end
    return false if spec[:hp_below] && battler.hp > battler.totalhp * spec[:hp_below].to_f
    return false if spec[:hp_above] && battler.hp <= battler.totalhp * spec[:hp_above].to_f
    return false if spec[:in_weather] && !spec[:in_weather].include?(battler.effectiveWeather)
    return false if spec[:on_terrain] && !spec[:on_terrain].include?(battle.field.terrain)
    return false if spec[:condition] && !self.safe_call(spec[:condition], battle, battler)
    return true
  end

  #=============================================================================
  # Move type
  #=============================================================================
  # Returns [new_type, message] (new_type == type if unchanged).
  def self.changed_move_type(battle, user, move, type)
    msg = nil
    self.active_defs(battle).each do |defn|
      defn[:type_changes]&.each do |rule|
        next if rule[:to] == type
        next if !self.move_matches?(rule, battle, user, nil, move, type)
        type = rule[:to]
        msg = rule[:message] if rule[:message]
        break
      end
      next if !defn[:hooks] || !defn[:hooks][:base_type]
      new_type = self.safe_call(defn[:hooks][:base_type], battle, user, move, type)
      type = new_type if new_type.is_a?(Symbol)
    end
    return type, msg
  end

  # Extra types added to a move this use (Flying Press-style). Returns
  # [[type, message], ...].
  def self.extra_types(battle, user, target, move, type)
    ret = []
    return ret if !type
    self.rules(battle, :extra_types).each do |rule|
      next if rule[:add] == type || ret.any? { |e| e[0] == rule[:add] }
      next if !self.move_matches?(rule, battle, user, target, move, type)
      ret.push([rule[:add], rule[:message]])
    end
    return ret
  end

  #=============================================================================
  # Type effectiveness
  #=============================================================================
  def self.effectiveness_rules_active?(battle)
    return self.active_defs(battle).any? do |d|
      d[:effectiveness_mods] || d[:inverse] || d[:extra_types] ||
        (d[:hooks] && d[:hooks][:effectiveness])
    end
  end

  # Modifies the effectiveness of move_type against ONE defending type.
  def self.modify_effectiveness(battle, move, move_type, def_type, user, target, eff)
    self.active_defs(battle).each do |defn|
      defn[:effectiveness_mods]&.each do |rule|
        next if rule[:attack] && !rule[:attack].include?(move_type)
        next if rule[:defend] && !rule[:defend].include?(def_type)
        next if rule[:moves] && (!move || !rule[:moves].include?(move.id))
        next if rule[:user] && !self.battler_matches?(rule[:user], battle, user)
        next if rule[:target] && !self.battler_matches?(rule[:target], battle, target)
        eff = rule[:set].to_f if rule.key?(:set)
        eff *= rule[:mult] if rule[:mult]
      end
      eff = self.invert_effectiveness(eff) if defn[:inverse]
      next if !defn[:hooks] || !defn[:hooks][:effectiveness]
      val = self.safe_call(defn[:hooks][:effectiveness], battle, move, move_type, def_type, user, target, eff)
      eff = val.to_f if val.is_a?(Numeric)
    end
    return eff
  end

  # Inverse Battle chart: immune/resisted -> super effective, super -> resisted.
  def self.invert_effectiveness(eff)
    return Effectiveness::SUPER_EFFECTIVE_MULTIPLIER if eff < Effectiveness::NORMAL_EFFECTIVE_MULTIPLIER
    return Effectiveness::NOT_VERY_EFFECTIVE_MULTIPLIER if eff > Effectiveness::NORMAL_EFFECTIVE_MULTIPLIER
    return eff
  end

  #=============================================================================
  # Damage
  #=============================================================================
  # Applies every damage modifier of the active field(s) to the multipliers
  # Hash used by Battle::Move#pbCalcDamage. ai = true: prediction only (no
  # messages).
  def self.apply_damage_mods(battle, user, target, move, type, mults, ai = false)
    uname = (ai) ? "" : user.pbThis
    mname = move.name
    if !ai
      # Messages for this use's type change / added types
      tmsg = move.instance_variable_get(:@fe_type_message)
      self.show_once(battle, user, move, tmsg, uname, mname) if tmsg
      self.extra_types(battle, user, target, move, type).each do |_t, emsg|
        self.show_once(battle, user, move, emsg, uname, mname) if emsg
      end
    end
    self.active_defs(battle).each do |defn|
      if type && defn[:type_mods] && defn[:type_mods][type]
        mults[:power_multiplier] *= defn[:type_mods][type]
        if !ai && defn[:type_messages] && defn[:type_messages][type]
          self.show_once(battle, user, move, defn[:type_messages][type], uname, mname)
        end
      end
      if defn[:move_mods] && defn[:move_mods][move.id]
        mults[:power_multiplier] *= defn[:move_mods][move.id]
        if !ai && defn[:move_messages] && defn[:move_messages][move.id]
          self.show_once(battle, user, move, defn[:move_messages][move.id], uname, mname)
        end
      end
      defn[:damage_mods]&.each do |rule|
        next if !self.move_matches?(rule, battle, user, target, move, type)
        mults[:power_multiplier]        *= rule[:mult]         if rule[:mult]
        mults[:attack_multiplier]       *= rule[:attack_mult]  if rule[:attack_mult]
        mults[:defense_multiplier]      *= rule[:defense_mult] if rule[:defense_mult]
        mults[:final_damage_multiplier] *= rule[:final_mult]   if rule[:final_mult]
        self.show_once(battle, user, move, rule[:message], uname, mname) if !ai && rule[:message]
      end
      if defn[:hooks] && defn[:hooks][:damage]
        self.safe_call(defn[:hooks][:damage], battle, user, target, move, type, mults, ai)
      end
    end
    self.apply_activated_ability_damage(battle, user, target, move, type, mults)
    if self.transform_boost?(battle, user, target, move, type)
      mults[:power_multiplier] *= TRANSFORM_BOOST
    end
  end

  # Single number summarising the field's damage effect (used by the AI).
  def self.damage_multiplier(battle, user, target, move, type)
    mults = { :power_multiplier => 1.0, :attack_multiplier => 1.0,
              :defense_multiplier => 1.0, :final_damage_multiplier => 1.0 }
    self.apply_damage_mods(battle, user, target, move, type, mults, true)
    defense = [mults[:defense_multiplier], 0.01].max
    return mults[:power_multiplier] * mults[:attack_multiplier] / defense *
           mults[:final_damage_multiplier]
  end

  #=============================================================================
  # Accuracy, priority, critical hits, effect chances
  #=============================================================================
  def self.apply_accuracy_mods(battle, user, target, move, type, mods)
    self.active_defs(battle).each do |defn|
      defn[:accuracy_mods]&.each do |rule|
        next if !self.move_matches?(rule, battle, user, target, move, type)
        mods[:accuracy_multiplier] *= rule[:mult]         if rule[:mult]
        mods[:evasion_multiplier]  *= rule[:evasion_mult] if rule[:evasion_mult]
        mods[:base_accuracy] = rule[:set]                 if rule[:set]
        mods[:base_accuracy] = 0                          if rule[:always_hit]
      end
      if defn[:hooks] && defn[:hooks][:accuracy]
        self.safe_call(defn[:hooks][:accuracy], battle, user, target, move, type, mods)
      end
    end
    if target && !battle.moldBreaker
      [[:SANDVEIL, [:Sandstorm]], [:SNOWCLOAK, [:Hail]]].each do |ab, weathers|
        next if !self.ability_activated?(battle, target, ab)
        next if weathers.include?(target.effectiveWeather)
        mods[:evasion_multiplier] *= 1.25
      end
    end
  end

  def self.priority_change(battle, user, move)
    rules = self.rules(battle, :priority_mods)
    return 0 if rules.empty?
    type = move.pbBaseType(user)
    type, _msg = self.changed_move_type(battle, user, move, type)
    ret = 0
    rules.each do |rule|
      ret += rule[:add].to_i if self.move_matches?(rule, battle, user, nil, move, type)
    end
    return ret
  end

  # Returns [extra critical hit stages, always_crit?]
  def self.crit_change(battle, user, target, move, type)
    add = 0
    always = false
    self.rules(battle, :crit_mods).each do |rule|
      next if !self.move_matches?(rule, battle, user, target, move, type)
      add += rule[:add].to_i if rule[:add]
      always = true if rule[:always]
    end
    return add, always
  end

  def self.modify_effect_chance(battle, user, target, move, chance)
    return chance if chance <= 0
    self.rules(battle, :effect_chance_mods).each do |rule|
      next if !self.move_matches?(rule, battle, user, target, move, move.calcType)
      chance = rule[:set] if rule[:set]
      chance = (chance * rule[:mult]).round if rule[:mult]
    end
    return chance.clamp(0, 100)
  end

  #=============================================================================
  # Move failure
  #=============================================================================
  # Returns a failure message if the field makes this move fail, else nil.
  def self.move_failure_message(battle, user, move)
    return nil if !self.active?(battle)
    type = move.pbBaseType(user)
    type, _msg = self.changed_move_type(battle, user, move, type)
    self.rules(battle, :move_fails).each do |rule|
      next if !self.move_matches?(rule, battle, user, nil, move, type)
      return rule[:message] || DEFAULT_FAIL_MESSAGE
    end
    self.hooks(battle, :block_move).each do |h|
      val = self.safe_call(h, battle, user, move)
      return val if val.is_a?(String)
      return DEFAULT_FAIL_MESSAGE if val
    end
    return nil
  end

  #=============================================================================
  # Stat / status helpers
  #=============================================================================
  def self.can_inflict_status?(battler, status, user = nil, move = nil)
    case status
    when :SLEEP           then return battler.pbCanSleep?(user, false, move)
    when :POISON, :TOXIC  then return battler.pbCanPoison?(user, false, move)
    when :BURN            then return battler.pbCanBurn?(user, false, move)
    when :PARALYSIS       then return battler.pbCanParalyze?(user, false, move)
    when :FROZEN          then return battler.pbCanFreeze?(user, false, move)
    end
    return false
  end

  # msg: custom message replacing the default "X was burned!" (may be nil).
  def self.inflict_status(battler, status, user = nil, msg = nil)
    case status
    when :SLEEP     then battler.pbSleep(msg)
    when :POISON    then battler.pbPoison(user, msg)
    when :TOXIC     then battler.pbPoison(user, msg, true)
    when :BURN      then battler.pbBurn(user, msg)
    when :PARALYSIS then battler.pbParalyze(user, msg)
    when :FROZEN    then battler.pbFreeze(msg)
    end
  end

  def self.stat_changes_possible?(battler, stats, user = nil)
    return stats.any? do |stat, n|
      next false if n == 0
      next battler.pbCanRaiseStatStage?(stat, user || battler) if n > 0
      next battler.pbCanLowerStatStage?(stat, user)
    end
  end

  # user nil = caused by the field (respects Mist/Clear Body etc. for drops).
  def self.apply_stat_changes(battler, stats, user = nil)
    anim = true
    ret = false
    stats.each do |stat, n|
      next if n == 0 || battler.fainted?
      if n > 0
        next if !battler.pbCanRaiseStatStage?(stat, user || battler)
        ret = true if battler.pbRaiseStatStage(stat, n, user || battler, anim)
      else
        next if !battler.pbCanLowerStatStage?(stat, user)
        ret = true if battler.pbLowerStatStage(stat, -n, user, anim)
      end
      anim = false
    end
    return ret
  end

  #=============================================================================
  # Named battler effects (effects: [...])
  #=============================================================================
  BATTLER_EFFECT_PROCS = {
    :ingrain      => [proc { |b| next false if b.effects[PBEffects::Ingrain]
                                 b.effects[PBEffects::Ingrain] = true },
                      "{1} planted its roots!"],
    :aqua_ring    => [proc { |b| next false if b.effects[PBEffects::AquaRing]
                                 b.effects[PBEffects::AquaRing] = true },
                      "{1} surrounded itself with a veil of water!"],
    :magnet_rise  => [proc { |b| next false if b.effects[PBEffects::MagnetRise] > 0 ||
                                               b.effects[PBEffects::Ingrain] ||
                                               b.effects[PBEffects::SmackDown]
                                 b.effects[PBEffects::MagnetRise] = 5 },
                      "{1} levitated with electromagnetism!"],
    :focus_energy => [proc { |b| next false if b.effects[PBEffects::FocusEnergy] >= 2
                                 b.effects[PBEffects::FocusEnergy] = 2 },
                      "{1} is getting pumped!"],
    :laser_focus  => [proc { |b| next false if b.effects[PBEffects::LaserFocus] > 0
                                 b.effects[PBEffects::LaserFocus] = 2 },
                      "{1} concentrated intensely!"],
    :charge       => [proc { |b| next false if b.effects[PBEffects::Charge] > 0
                                 b.effects[PBEffects::Charge] = 2 },
                      "{1} began charging power!"],
    :defense_curl => [proc { |b| next false if b.effects[PBEffects::DefenseCurl]
                                 b.effects[PBEffects::DefenseCurl] = true },
                      "{1} curled up!"],
    :minimize     => [proc { |b| next false if b.effects[PBEffects::Minimize]
                                 b.effects[PBEffects::Minimize] = true },
                      "{1} shrank!"],
    :smack_down   => [proc { |b| next false if b.effects[PBEffects::SmackDown] || !b.airborne?
                                 b.effects[PBEffects::SmackDown]   = true
                                 b.effects[PBEffects::MagnetRise]  = 0
                                 b.effects[PBEffects::Telekinesis] = 0 },
                      "{1} fell straight down!"],
    :telekinesis  => [proc { |b| next false if b.effects[PBEffects::Telekinesis] > 0 ||
                                               b.effects[PBEffects::Ingrain] ||
                                               b.effects[PBEffects::SmackDown]
                                 b.effects[PBEffects::Telekinesis] = 3 },
                      "{1} was hurled into the air!"],
    :flash_fire   => [proc { |b| next false if b.effects[PBEffects::FlashFire]
                                 b.effects[PBEffects::FlashFire] = true },
                      "The power of {1}'s Fire-type moves rose!"],
    :stockpile    => [proc { |b| next false if b.effects[PBEffects::Stockpile] >= 3
                                 b.effects[PBEffects::Stockpile] += 1 },
                      "{1} stockpiled energy!"]
  }

  def self.apply_named_effect(battler, effect)
    entry = BATTLER_EFFECT_PROCS[effect]
    return nil if !entry
    return (entry[0].call(battler) == false) ? nil : entry[1]
  end

  #=============================================================================
  # Battler effects (end_of_round / on_entry / seed rules)
  #=============================================================================
  # Applies one rule to one battler. extra_args are extra message arguments
  # ({2}, {3}...). Returns true if anything happened.
  def self.apply_battler_effect(battle, battler, rule, *extra_args)
    return false if !battler || battler.fainted?
    return false if rule[:chance] && battle.pbRandom(100) >= rule[:chance]
    shown = false
    did = false
    msg = rule[:message]
    announce = lambda do
      next if shown
      shown = true
      battle.pbCommonAnimation(rule[:animation], battler) if rule[:animation]
      battle.pbDisplay(self.format(msg, battler.pbThis, *extra_args)) if msg
    end
    # Damage
    if rule[:damage] && battler.takesIndirectDamage?
      amt = battler.totalhp * rule[:damage].to_f
      if rule[:damage_type]
        amt *= Effectiveness.calculate(rule[:damage_type], *battler.pbTypes(true))
      end
      if amt > 0
        battle.pbCommonAnimation(rule[:animation], battler) if rule[:animation]
        shown = true
        battler.pbTakeEffectDamage([amt.round, 1].max) do |_hp_lost|
          battle.pbDisplay(self.format(msg, battler.pbThis, *extra_args)) if msg
        end
        did = true
        return true if battler.fainted?
      end
    end
    # Healing
    if rule[:heal] && battler.canHeal?
      announce.call
      battler.pbRecoverHP([(battler.totalhp * rule[:heal].to_f).round, 1].max)
      did = true
    end
    # Status cure
    if rule[:cure_status] && battler.status != :NONE
      announce.call
      battler.pbCureStatus(true)
      did = true
    end
    # Status
    if rule[:status] && self.can_inflict_status?(battler, rule[:status])
      custom = (!shown && msg) ? self.format(msg, battler.pbThis, *extra_args) : nil
      battle.pbCommonAnimation(rule[:animation], battler) if rule[:animation] && !shown
      shown = true
      self.inflict_status(battler, rule[:status], nil, custom)
      did = true
    end
    # Confusion
    if rule[:confuse] && battler.pbCanConfuse?(nil, false)
      announce.call
      battler.pbConfuse
      did = true
    end
    # Stat changes
    if rule[:stats] && self.stat_changes_possible?(battler, rule[:stats])
      announce.call
      did = true if self.apply_stat_changes(battler, rule[:stats], nil)
    end
    # Named effects
    rule[:effects]&.each do |eff|
      default_msg = self.apply_named_effect(battler, eff)
      next if !default_msg
      if msg
        announce.call
      else
        battle.pbDisplay(self.format(default_msg, battler.pbThis))
      end
      did = true
    end
    # Added type (third type)
    if rule[:add_type] && self.apply_added_type(battle, battler, rule[:add_type])
      if msg
        announce.call
      else
        battle.pbDisplay(self.format("{1} became part {2} type!", battler.pbThis,
                                     GameData::Type.get(rule[:add_type]).name))
      end
      did = true
    end
    # Bespoke
    if rule[:proc]
      res = self.safe_call(rule[:proc], battle, battler)
      if res
        announce.call   # a proc-only rule still shows its :message (e.g. BLEED's Magical Seed)
        did = true
      end
    end
    return did
  end

  def self.apply_entry_effects(battle, battler, on_change_only = false)
    return if !self.active?(battle) || battler.fainted?
    self.apply_natural_type(battle, battler)
    self.rules(battle, :on_entry).each do |rule|
      next if on_change_only && !rule[:also_on_change]
      next if rule[:battlers] && !self.battler_matches?(rule[:battlers], battle, battler)
      self.apply_battler_effect(battle, battler, rule)
      return if battler.fainted?
    end
    return if on_change_only
    self.hooks(battle, :on_entry).each { |h| self.safe_call(h, battle, battler) }
  end

  #=============================================================================
  # Seeds
  #=============================================================================
  def self.seed_rule(battle, battler, item)
    defn = self.current_definition(battle)
    return nil if !defn || !defn[:seed]
    defn[:seed].each do |rule|
      next if rule[:item] != item
      next if rule[:battlers] && !self.battler_matches?(rule[:battlers], battle, battler)
      return rule
    end
    return nil
  end

  # Triggers a held seed if the current field defines an effect for it.
  def self.trigger_seed(battle, battler, item)
    return false if battler.fainted? || !battler.itemActive?
    rule = self.seed_rule(battle, battler, item)
    return false if !rule
    item_name = GameData::Item.get(item).name
    battle.pbCommonAnimation("UseItem", battler)
    rule = rule.merge(:message => DEFAULT_SEED_MESSAGE) if !rule[:message]
    rule = rule.reject { |k, _v| k == :chance }
    self.apply_battler_effect(battle, battler, rule, item_name)
    battler.pbConsumeItem if battler.item_id == item
    return true
  end

  def self.check_all_seeds(battle)
    battle.pbPriority(true).each do |b|
      next if b.fainted? || !b.item_id || !SEED_ITEMS.include?(b.item_id)
      self.trigger_seed(battle, b, b.item_id)
    end
  end

  #=============================================================================
  # Speed and abilities
  #=============================================================================
  def self.speed_multiplier(battle, battler)
    mult = 1.0
    self.rules(battle, :speed_mods).each do |rule|
      next if rule[:battlers] && !self.battler_matches?(rule[:battlers], battle, battler)
      mult *= rule[:mult]
    end
    mult *= self.activated_speed_multiplier(battle, battler)
    self.hooks(battle, :speed).each do |h|
      val = self.safe_call(h, battle, battler, mult)
      mult = val if val.is_a?(Numeric)
    end
    return mult
  end

  def self.ability_negated?(battle, ability_id)
    return false if !ability_id
    defs = self.active_defs(battle)
    return false if defs.empty?
    return defs.any? { |d| d[:negated_abilities]&.include?(ability_id) }
  end

  #=============================================================================
  # Weather and terrain
  #=============================================================================
  def self.env_spec_value(battle, kind, key, id)
    self.active_defs(battle).each do |defn|
      spec = defn[kind]
      next if !spec || !spec[key]
      val = (key == :block) ? spec[key].include?(id) : spec[key][id]
      return val if val
    end
    return nil
  end

  def self.env_block_message(battle, kind)
    self.active_defs(battle).each do |defn|
      spec = defn[kind]
      return spec[:block_message] if spec && spec[:block_message]
    end
    return (kind == :weather) ? DEFAULT_WEATHER_BLOCK_TEXT : DEFAULT_TERRAIN_BLOCK_TEXT
  end

  #=============================================================================
  # Transitions
  #=============================================================================
  def self.move_trigger?(rule)
    return !(rule[:weather] || rule[:terrain] || rule[:turns] || rule[:check])
  end

  # Counts one trigger of transition idx; performs it once :uses is reached.
  # Returns true if the field (or stage) changed.
  def self.count_transition(battle, rule, idx)
    st = self.raw_state(battle)
    if rule[:rewind]
      rewound = self.rewind_transitions(battle, rule[:rewind])
      if !rule.key?(:to) && !rule[:stage] && !rule[:stage_delta]   # Rewind-only rule
        battle.pbDisplay(self.format(rule[:message])) if rewound && rule[:message]
        return false
      end
    end
    uses = [rule[:uses] || 1, 1].max
    st[:counters][idx] = (st[:counters][idx] || 0) + 1
    if st[:counters][idx] >= uses
      st[:counters][idx] = 0
      return self.perform_transition(battle, rule)
    end
    if rule[:progress_message]
      battle.pbDisplay(self.format(rule[:progress_message], (uses - st[:counters][idx]).to_s))
    end
    return false
  end

  # Lowers the progress of other transitions (by :id). Returns true if any moved.
  def self.rewind_transitions(battle, spec)
    st = self.raw_state(battle)
    list = self.transitions(battle)
    ret = false
    spec.each do |tid, n|
      idx = list.index { |r| r[:id] == tid }
      next if !idx || !st[:counters][idx] || st[:counters][idx] <= 0
      st[:counters][idx] = [st[:counters][idx] - n.to_i, 0].max
      ret = true
    end
    return ret
  end

  # Read-only progress of a transition (by :id): [count, uses] or nil.
  def self.transition_progress(battle, tid)
    list = self.transitions(battle)
    idx = list.index { |r| r[:id] == tid }
    return nil if !idx
    return [self.raw_state(battle)[:counters][idx] || 0, [list[idx][:uses] || 1, 1].max]
  end

  def self.perform_transition(battle, rule)
    if rule.key?(:to)
      to = (rule[:to].is_a?(Proc)) ? self.safe_call(rule[:to], battle) : rule[:to]
      return false if to.nil?
      return battle.change_field(to, rule[:message])
    end
    if rule[:stage] || rule[:stage_delta]
      new_stage = rule[:stage] || (self.stage(battle) + rule[:stage_delta].to_i)
      return battle.set_field_stage(new_stage, rule[:message])
    end
    return false
  end

  def self.transitions(battle)
    defn = self.current_definition(battle)
    return [] if !defn || !defn[:transitions]
    return defn[:transitions]
  end

  def self.check_move_transitions(battle, user, targets, move)
    st = self.raw_state(battle)
    return if !st || st[:changing] || self.lingering?(battle)
    self.transitions(battle).each_with_index do |rule, i|
      next if !self.move_trigger?(rule)
      next if user.lastMoveFailed && !rule[:even_if_failed]
      # :strike_turn - a two-turn move counts on the turn it strikes, not the turn it charges (Reborn).
      next if rule[:strike_turn] && user.effects[PBEffects::TwoTurnAttack]
      next if !self.move_matches?(rule, battle, user, targets.first, move, move.calcType)
      return if self.count_transition(battle, rule, i)
    end
  end

  def self.check_env_transitions(battle, kind, id)
    st = self.raw_state(battle)
    return if !st || st[:changing] || self.lingering?(battle)
    self.transitions(battle).each_with_index do |rule, i|
      next if !rule[kind] || !rule[kind].include?(id)
      return if self.count_transition(battle, rule, i)
    end
  end

  def self.check_round_transitions(battle)
    self.transitions(battle).each_with_index do |rule, i|
      if rule[:turns]
        next if self.raw_state(battle)[:turns] < rule[:turns]
        return if self.perform_transition(battle, rule)
      elsif rule[:check]
        next if !self.safe_call(rule[:check], battle)
        return if self.count_transition(battle, rule, i)
      end
    end
  end

  # A move that failed before its hits (pbMoveFailed?, :move_fails, "no
  # target"...): only :even_if_failed transitions can count it.
  def self.failed_move_transitions(battle, user, move)
    return if !self.active?(battle) || !move
    self.check_move_transitions(battle, user, [], move)
  end

  #=============================================================================
  # When a move changes the field: the moment it lands (FIELD_API §5)
  #-----------------------------------------------------------------------------
  # A move's transitions are checked once per use, as soon as it has landed:
  #   * a single-hit damaging move: right after its damage and the hit messages
  #     ("It's super effective!"), before its secondary effects (pbRecordDamageLost
  #     of the last target hit; 005);
  #   * anything else (multi-hit moves after their last hit, status moves, moves
  #     whose hits all missed): at the start of the after-move effects.
  # If that changes the field (or its stage), the old field LINGERS for the rest
  # of that move: its secondary effects, the old field's :added_effects,
  # :move_stat_boosts and :after_move hooks resolve exactly as they did when the
  # change came last; the battle reads as the new field once the after-move
  # effects are done (Life Orb, Eject Button, switching... see the new field).
  # No other transition fires while the old field lingers; a real change_field
  # (a boss phase...) ends it.
  #=============================================================================
  # Per move use (a stack: a move can call another, e.g. Metronome).
  def self.move_use(battle)
    list = battle.instance_variable_get(:@fe_move_uses)
    return (list) ? list.last : nil
  end

  def self.push_move_use(battle)
    list = battle.instance_variable_get(:@fe_move_uses)
    list = battle.instance_variable_set(:@fe_move_uses, []) if !list
    ctx = { :landed => false, :hit => nil }
    list.push(ctx)
    return ctx
  end

  def self.pop_move_use(battle, ctx)
    list = battle.instance_variable_get(:@fe_move_uses)
    i = (list) ? list.rindex { |c| c.equal?(ctx) } : nil
    list.delete_at(i) if i
    self.end_linger(battle, ctx)
  end

  def self.lingering?(battle)
    return !battle.instance_variable_get(:@fe_linger).nil?
  end

  # Ends the old field's linger (only one started by this move use, if given).
  def self.end_linger(battle, ctx = nil)
    lg = battle.instance_variable_get(:@fe_linger)
    return if !lg
    return if ctx && lg[:use] && !lg[:use].equal?(ctx)
    battle.instance_variable_set(:@fe_linger, nil)
  end

  # Called after each target's hit is recorded (Battle::Move#pbRecordDamageLost).
  def self.hit_recorded(battle, user, target, move)
    ctx = self.move_use(battle)
    return if !ctx || ctx[:landed] || !ctx[:hit]
    hmove, huser, htargets = ctx[:hit]
    return if !hmove.equal?(move) || !huser.equal?(user)
    return if move.multiHitMove? || move.pbRepeatHit? || user.effects[PBEffects::ParentalBond] > 0
    last = htargets.reverse.find { |b| b && !b.damageState.unaffected }
    return if !last.equal?(target)
    self.move_landed(battle, user, htargets, move)
  end

  # Checks the move's transitions (once per move use); on a change the old field lingers.
  def self.move_landed(battle, user, targets, move)
    ctx = self.move_use(battle)
    return if ctx && ctx[:landed]
    ctx[:landed] = true if ctx
    return if !self.active?(battle) || self.lingering?(battle)
    old_id = battle.instance_variable_get(:@field_effect)
    real = battle.instance_variable_get(:@fe_state)
    return if !real
    snap = real.dup
    snap[:counters] = real[:counters].dup
    self.check_move_transitions(battle, user, targets, move)
    now = battle.instance_variable_get(:@fe_state)
    changed = battle.instance_variable_get(:@field_effect) != old_id || !now.equal?(real) ||
              now[:stage] != snap[:stage]
    battle.instance_variable_set(:@fe_linger, { :id => old_id, :state => snap, :use => ctx }) if changed
  end

  #=============================================================================
  # Fixed-damage moves (Dragon Rage, Seismic Toss, Super Fang...)
  #=============================================================================
  def self.modify_fixed_damage(battle, user, target, move, damage, ai = false)
    return damage if damage <= 0
    self.rules(battle, :fixed_damage_mods).each do |rule|
      next if !self.move_matches?(rule, battle, user, target, move, move.calcType || move.type)
      damage = rule[:set] if rule[:set]
      damage = [(damage * rule[:mult]).round, 1].max if rule[:mult]
      self.show_once(battle, user, move, rule[:message], user.pbThis, move.name) if !ai && rule[:message]
    end
    return damage
  end

  #=============================================================================
  # Weather-gated moves (:weather_as): the user's move sees this weather
  #=============================================================================
  def self.weather_as_for(battle, user, move)
    return nil if !self.active?(battle) || !move
    rules = self.rules(battle, :weather_as)
    return nil if rules.empty?
    type = move.type
    rules.each do |rule|
      return rule[:as] if self.move_matches?(rule, battle, user, nil, move, type)
    end
    return nil
  end

  # Runs the block with battler seeing `weather` (when no weather is active).
  def self.with_weather_as(battler, weather)
    return yield if !weather || !battler
    old = battler.instance_variable_get(:@fe_weather_as)
    battler.instance_variable_set(:@fe_weather_as, weather)
    begin
      return yield
    ensure
      battler.instance_variable_set(:@fe_weather_as, old)
    end
  end

  #=============================================================================
  # Public read API for borrowing fields (:BLEED, :PRISM_ARENA)
  #=============================================================================
  def self.borrowed_fields(battle)
    st = self.raw_state(battle)
    return (st) ? st[:borrowed].dup : []
  end

  def self.borrowed_field(battle)
    return self.borrowed_fields(battle).first
  end

  # PRISM_ARENA's public state (the field keeps it in FieldEffects.state(battle)[:prism]).
  # Returns a frozen summary Hash, or nil when PRISM_ARENA isn't the current field.
  def self.prism_state(battle)
    pr = self.state(battle)[:prism]
    return nil if !pr.is_a?(Hash)
    return {
      :field       => pr[:field],      :type       => pr[:type],      :plate       => pr[:plate],
      :next_field  => pr[:next_field], :next_type  => pr[:next_type], :next_plate  => pr[:next_plate],
      :rounds_left => pr[:rounds_left], :rotation  => pr[:rotation],  :interval    => pr[:interval]
    }.freeze
  end

  #=============================================================================
  # After a move is used
  #=============================================================================
  def self.after_move(battle, user, targets, move, num_hits)
    # Transitions first (no-op if the move already changed the field when it landed); a changed field lingers
    # until the end of this method, so the effects below are the old field's, exactly as before the change.
    self.move_landed(battle, user, targets, move)
    self.after_move_effects(battle, user, targets, move, num_hits)
  ensure
    self.end_linger(battle, self.move_use(battle))
  end

  def self.after_move_effects(battle, user, targets, move, num_hits)
    return if !self.active?(battle)
    type = move.calcType
    charging = user.effects[PBEffects::TwoTurnAttack]
    if !user.lastMoveFailed && !user.fainted? && !charging
      self.rules(battle, :move_stat_boosts).each do |rule|
        next if !self.move_matches?(rule, battle, user, targets.first, move, type)
        affected = []
        if rule[:user_stats] && self.stat_changes_possible?(user, rule[:user_stats], user)
          affected.push([user, rule[:user_stats], user])
        end
        if rule[:target_stats]
          targets.each do |t|
            next if t.fainted? || t.damageState.unaffected || t.index == user.index
            next if !self.stat_changes_possible?(t, rule[:target_stats], user)
            affected.push([t, rule[:target_stats], user])
          end
        end
        next if affected.empty?
        battle.pbDisplay(self.format(rule[:message], user.pbThis, move.name)) if rule[:message]
        affected.each { |b, stats, src| self.apply_stat_changes(b, stats, src) }
      end
    end
    self.extend_effect_durations(battle, user, targets, move) if !user.fainted?
    self.hooks(battle, :after_move).each do |h|
      self.safe_call(h, battle, user, targets, move, num_hits)
    end
  end

  #=============================================================================
  # Added effects (per hit)
  #=============================================================================
  def self.apply_added_effects(battle, user, target, move)
    return if !self.active?(battle)
    return if target.damageState.unaffected || target.damageState.calcDamage == 0
    type = move.calcType
    self.rules(battle, :added_effects).each do |rule|
      next if !self.move_matches?(rule, battle, user, target, move, type)
      recipient = (rule[:apply_to] == :user) ? user : target
      next if recipient.fainted?
      if recipient.index != user.index
        next if target.damageState.substitute
        next if user.hasActiveAbility?(:SHEERFORCE)
        next if target.hasActiveAbility?(:SHIELDDUST) && !battle.moldBreaker
      end
      chance = rule[:chance] || 100
      chance *= 2 if chance < 100 && (user.hasActiveAbility?(:SERENEGRACE) ||
                                      user.pbOwnSide.effects[PBEffects::Rainbow] > 0)
      next if battle.pbRandom(100) >= chance
      msg = (rule[:message]) ? self.format(rule[:message], recipient.pbThis, move.name) : nil
      if rule[:status] && self.can_inflict_status?(recipient, rule[:status], user, move)
        self.inflict_status(recipient, rule[:status], user, msg)
        msg = nil
      end
      if rule[:confuse] && recipient.pbCanConfuse?(user, false, move)
        battle.pbDisplay(msg) if msg
        msg = nil
        recipient.pbConfuse
      end
      if rule[:flinch] && recipient.index != user.index
        recipient.pbFlinch(user)
      end
      if rule[:stats] && self.stat_changes_possible?(recipient, rule[:stats], user)
        battle.pbDisplay(msg) if msg
        msg = nil
        self.apply_stat_changes(recipient, rule[:stats], user)
      end
      self.safe_call(rule[:proc], battle, user, target, move) if rule[:proc]
    end
  end

  #=============================================================================
  # Borrowing (overlay effects from other fields, e.g. :BLEED)
  #=============================================================================
  def self.borrow_pool(battle, spec)
    cur = self.current(battle)
    pool = (spec[:pool] == :all) ? (self.map_borrow_pool || self.ids) : Array(spec[:pool])
    return pool.select do |id|
      next false if id == cur || spec[:exclude].include?(id)
      defn = self.get(id)
      next defn && !defn[:borrow]
    end
  end

  # The current map's MAP_BORROW_POOLS entry (registered fields only), or nil.
  # Narrows only open pools (:all); fixed pools such as PRISM_ARENA's are kept.
  def self.map_borrow_pool
    return nil if MAP_BORROW_POOLS.empty? || !defined?($game_map) || !$game_map
    list = Array(MAP_BORROW_POOLS[$game_map.map_id]).map { |id| self.normalize_id(id) }
    list = list.select { |id| id != NONE && self.exists?(id) }
    return (list.empty?) ? nil : list
  end

  def self.start_borrowing(battle)
    spec = self.current_definition(battle)&.[](:borrow)
    return if !spec
    self.raw_state(battle)[:borrow_timer] = spec[:interval]
    self.rotate_borrowed(battle) if spec[:start_immediately]
  end

  def self.rotate_borrowed(battle)
    spec = self.current_definition(battle)&.[](:borrow)
    return if !spec
    st = self.raw_state(battle)
    pool = self.borrow_pool(battle, spec)
    return if pool.empty?
    old = st[:borrowed].dup
    count = [spec[:count].to_i, pool.length].min
    chosen = []
    if spec[:order] == :sequential
      count.times do
        chosen.push(pool[st[:borrow_cursor] % pool.length])
        st[:borrow_cursor] += 1
      end
    else
      candidates = pool - old
      candidates = pool.dup if candidates.length < count
      count.times do
        break if candidates.empty?
        chosen.push(candidates.delete_at(battle.pbRandom(candidates.length)))
      end
    end
    st[:borrowed] = chosen
    self.invalidate_cache(battle)
    names = chosen.map { |id| self.name_of(id) }.join(", ")
    battle.pbDisplay(self.format(spec[:message], names)) if spec[:message]
    self.log("Borrowed effects now: #{chosen.inspect}")
    self.notify_overlay_change(battle, self.current(battle), old, chosen)
    # Borrowed fields' "also_on_change" entry effects hit the active battlers
    battle.pbPriority(true).each do |b|
      next if b.fainted?
      chosen.each do |bid|
        view = self.borrowable_view(bid)
        view[:on_entry]&.each do |rule|
          next if !rule[:also_on_change]
          next if rule[:battlers] && !self.battler_matches?(rule[:battlers], battle, b)
          self.apply_battler_effect(battle, b, rule)
        end
      end
      b.pbFaint if b.fainted?
    end
  end

  def self.tick_borrowing(battle)
    spec = self.current_definition(battle)&.[](:borrow)
    return if !spec
    st = self.raw_state(battle)
    st[:borrow_timer] -= 1
    return if st[:borrow_timer] > 0
    st[:borrow_timer] = spec[:interval]
    self.rotate_borrowed(battle)
  end

  #=============================================================================
  # End of round
  #=============================================================================
  def self.end_of_round(battle)
    return if battle.decision > 0
    return if !self.active?(battle)
    st = self.raw_state(battle)
    field_at_start = self.current(battle)
    priority = battle.pbPriority(true)
    self.rules(battle, :end_of_round).each do |rule|
      priority.each do |b|
        next if b.fainted?
        next if rule[:battlers] && !self.battler_matches?(rule[:battlers], battle, b)
        self.apply_battler_effect(battle, b, rule)
        b.pbFaint if b.fainted?
      end
    end
    self.activated_ability_end_of_round(battle, priority)
    self.hooks(battle, :end_of_round).each { |h| self.safe_call(h, battle) }
    return if battle.decision > 0
    return if self.current(battle) != field_at_start   # A hook changed the field
    st[:turns] += 1
    self.check_round_transitions(battle)
    return if self.current(battle) != field_at_start
    self.tick_borrowing(battle)
  end
end
