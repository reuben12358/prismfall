#===============================================================================
# Prismfall Field Effects v1.1 - Rebornverse-depth extensions (all additive)
#-------------------------------------------------------------------------------
#   * :activate_abilities   abilities behave as if their trigger were met
#   * transform strikes     a damaging move that completes a field change x1.3
#   * :status_immunity      the place prevents certain statuses
#   * :effect_durations     Tailwind / rooms / screens... last longer
#   * new named battler effects (side conditions, Wish, Taunt, foe hazards)
#   * natural type          Mimicry and Terrain Pulse read the field's :camouflage
# See design/FIELD_API.md. Old field files keep working unchanged.
#===============================================================================
module FieldEffects
  # Power multiplier for the move that transforms the field (Reborn: x1.3).
  TRANSFORM_BOOST = 1.3

  #=============================================================================
  # Transform strikes
  #=============================================================================
  # True if this damaging move use will complete a transition of the current
  # field that changes it into another field (or a stage rule with :boost => true).
  def self.transform_boost?(battle, user, target, move, type)
    return false if !move || !move.damagingMove? || !user
    st = self.raw_state(battle)
    return false if !st || st[:changing]
    cur = self.current(battle)
    return false if cur == NONE
    self.transitions(battle).each_with_index do |rule, i|
      next if !self.move_trigger?(rule) || rule[:boost] == false
      field_change = rule.key?(:to)
      next if !field_change && !rule[:boost]
      next if !self.move_matches?(rule, battle, user, target, move, type)
      uses = [rule[:uses] || 1, 1].max
      next if (st[:counters][i] || 0) + 1 < uses
      if field_change
        to = rule[:to]
        to = self.safe_call(to, battle) if to.is_a?(Proc)
        next if to.nil? || self.normalize_id(to) == cur
      end
      return true
    end
    return false
  end

  # [count, uses, destination] of the transition this move would advance, for
  # the AI (first matching move rule that changes the field), or nil.
  def self.transition_this_move_advances(battle, user, move, type)
    st = self.raw_state(battle)
    return nil if !st || st[:changing]
    self.transitions(battle).each_with_index do |rule, i|
      next if !self.move_trigger?(rule) || rule[:target]
      next if !rule.key?(:to) && !rule[:stage] && !rule[:stage_delta]
      next if !self.move_matches?(rule, battle, user, nil, move, type)
      dest = if rule.key?(:to)
               to = rule[:to]
               to = self.safe_call(to, battle) if to.is_a?(Proc)
               [self.normalize_id(to), 1]
             else
               [self.current(battle), rule[:stage] || (self.stage(battle) + rule[:stage_delta].to_i)]
             end
      return [st[:counters][i] || 0, [rule[:uses] || 1, 1].max, dest]
    end
    return nil
  end

  #=============================================================================
  # Ability activation (:activate_abilities)
  #=============================================================================
  PINCH_ABILITIES = { :BLAZE => :FIRE, :OVERGROW => :GRASS, :TORRENT => :WATER, :SWARM => :BUG }.freeze

  def self.activated_abilities(battle)
    ret = []
    self.active_defs(battle).each { |d| ret.concat(d[:activate_abilities]) if d[:activate_abilities] }
    return ret
  end

  def self.ability_activated?(battle, battler, ability)
    return false if !battler || battler.fainted?
    return false if !self.activated_abilities(battle).include?(ability)
    return battler.hasActiveAbility?(ability)
  end

  def self.apply_activated_ability_damage(battle, user, target, move, type, mults)
    list = self.activated_abilities(battle)
    return if list.empty?
    if user && user.abilityActive? && list.include?(user.ability_id)
      sunny = [:Sun, :HarshSun].include?(user.effectiveWeather)
      case user.ability_id
      when :BLAZE, :OVERGROW, :TORRENT, :SWARM
        mults[:attack_multiplier] *= 1.5 if type == PINCH_ABILITIES[user.ability_id] && user.hp > user.totalhp / 3
      when :SANDFORCE
        mults[:power_multiplier] *= 1.3 if [:ROCK, :GROUND, :STEEL].include?(type) && battle.pbWeather != :Sandstorm
      when :SOLARPOWER
        mults[:attack_multiplier] *= 1.5 if move.specialMove?(type) && !sunny
      when :TOXICBOOST
        mults[:power_multiplier] *= 1.5 if move.physicalMove?(type) && !user.poisoned?
      when :FLAREBOOST
        mults[:power_multiplier] *= 1.5 if move.specialMove?(type) && !user.burned?
      when :GUTS
        mults[:attack_multiplier] *= 1.5 if move.physicalMove?(type) && !user.pbHasAnyStatus?
      when :FLOWERGIFT
        mults[:attack_multiplier] *= 1.5 if move.physicalMove?(type) && !sunny
      end
    end
    return if !target || battle.moldBreaker || !target.abilityActive? || !list.include?(target.ability_id)
    case target.ability_id
    when :MARVELSCALE
      mults[:defense_multiplier] *= 1.5 if move.physicalMove?(type) && !target.pbHasAnyStatus?
    when :GRASSPELT
      mults[:defense_multiplier] *= 1.5 if move.physicalMove?(type) && battle.field.terrain != :Grassy
    when :FLOWERGIFT
      mults[:defense_multiplier] *= 1.5 if move.specialMove?(type) &&
                                         ![:Sun, :HarshSun].include?(target.effectiveWeather)
    end
  end

  def self.activated_speed_multiplier(battle, battler)
    return 1.0 if !battler.abilityActive?
    list = self.activated_abilities(battle)
    return 1.0 if list.empty? || !list.include?(battler.ability_id)
    w = battler.effectiveWeather
    case battler.ability_id
    when :SWIFTSWIM   then return 2.0 if ![:Rain, :HeavyRain].include?(w)
    when :CHLOROPHYLL then return 2.0 if ![:Sun, :HarshSun].include?(w)
    when :SANDRUSH    then return 2.0 if w != :Sandstorm
    when :SLUSHRUSH   then return 2.0 if w != :Hail
    when :SURGESURFER then return 2.0 if battle.field.terrain != :Electric
    when :QUICKFEET   then return 1.5 if !battler.pbHasAnyStatus?
    end
    return 1.0
  end

  # Rain Dish / Dry Skin / Ice Body heal and Hydration cures as if their weather were up.
  def self.activated_ability_end_of_round(battle, priority)
    list = self.activated_abilities(battle)
    return if list.empty?
    priority.each do |b|
      next if b.fainted? || !b.abilityActive? || !list.include?(b.ability_id)
      rainy = [:Rain, :HeavyRain].include?(b.effectiveWeather)
      heal = case b.ability_id
             when :RAINDISH then (rainy) ? nil : 1 / 16.0
             when :DRYSKIN  then (rainy) ? nil : 1 / 8.0
             when :ICEBODY  then (b.effectiveWeather == :Hail) ? nil : 1 / 16.0
             end
      if heal && b.canHeal?
        battle.pbShowAbilitySplash(b)
        b.pbRecoverHP([(b.totalhp * heal).round, 1].max)
        battle.pbDisplay(_INTL("{1}'s HP was restored.", b.pbThis))
        battle.pbHideAbilitySplash(b)
      elsif b.ability_id == :HYDRATION && !rainy && b.status != :NONE
        battle.pbShowAbilitySplash(b)
        b.pbCureStatus(true)
        battle.pbHideAbilitySplash(b)
      end
    end
  end

  #=============================================================================
  # Status immunity (:status_immunity rules, and an activated Leaf Guard)
  #=============================================================================
  DEFAULT_STATUS_IMMUNITY_TEXT = "{1} is protected by its surroundings!"

  # Message String if the field prevents `status` on battler, else nil.
  def self.status_immunity_message(battle, battler, status)
    self.rules(battle, :status_immunity).each do |rule|
      next if !rule[:status].include?(status) && !(status == :POISON && rule[:status].include?(:TOXIC))
      next if rule[:battlers] && !self.battler_matches?(rule[:battlers], battle, battler)
      return rule[:message] || DEFAULT_STATUS_IMMUNITY_TEXT
    end
    if self.ability_activated?(battle, battler, :LEAFGUARD) &&
       ![:Sun, :HarshSun].include?(battler.effectiveWeather)
      return "{1}'s Leaf Guard shields it!"
    end
    return nil
  end

  #=============================================================================
  # Longer-lasting effects (:effect_durations => { MOVE => n or [n, "message"] })
  #=============================================================================
  DURATION_TARGETS = {
    :TAILWIND => [:own_side, :Tailwind], :REFLECT => [:own_side, :Reflect],
    :LIGHTSCREEN => [:own_side, :LightScreen], :AURORAVEIL => [:own_side, :AuroraVeil],
    :SAFEGUARD => [:own_side, :Safeguard], :MIST => [:own_side, :Mist], :LUCKYCHANT => [:own_side, :LuckyChant],
    :TRICKROOM => [:field, :TrickRoom], :MAGICROOM => [:field, :MagicRoom], :WONDERROOM => [:field, :WonderRoom],
    :GRAVITY => [:field, :Gravity], :MUDSPORT => [:field, :MudSportField], :WATERSPORT => [:field, :WaterSportField],
    :MAGNETRISE => [:user, :MagnetRise], :TELEKINESIS => [:target, :Telekinesis], :TAUNT => [:target, :Taunt],
    :ENCORE => [:target, :Encore], :HEALBLOCK => [:target, :HealBlock], :EMBARGO => [:target, :Embargo],
    :SUNNYDAY => [:weather], :RAINDANCE => [:weather], :SANDSTORM => [:weather], :HAIL => [:weather],
    :SNOWSCAPE => [:weather], :ELECTRICTERRAIN => [:terrain], :GRASSYTERRAIN => [:terrain],
    :MISTYTERRAIN => [:terrain], :PSYCHICTERRAIN => [:terrain]
  }.freeze
  DEFAULT_DURATION_TEXT = "The surroundings will sustain {2} for longer!"

  def self.extend_effect_durations(battle, user, targets, move)
    return if user.lastMoveFailed
    self.active_defs(battle).each do |defn|
      entry = defn[:effect_durations] && defn[:effect_durations][move.id]
      next if !entry
      n, msg = entry
      scope, name = DURATION_TARGETS[move.id]
      next if !scope
      done = false
      case scope
      when :own_side, :field, :user
        holder = { :own_side => user.pbOwnSide, :field => battle.field, :user => user }[scope]
        const = PBEffects.const_get(name)
        if holder.effects[const].is_a?(Integer) && holder.effects[const] > 0
          holder.effects[const] += n
          done = true
        end
      when :target
        const = PBEffects.const_get(name)
        targets.each do |t|
          next if t.fainted? || !t.effects[const].is_a?(Integer) || t.effects[const] <= 0
          t.effects[const] += n
          done = true
        end
      when :weather
        if battle.field.weather != :None && battle.field.weatherDuration > 0
          battle.field.weatherDuration += n
          done = true
        end
      when :terrain
        if battle.field.terrain != :None && battle.field.terrainDuration > 0
          battle.field.terrainDuration += n
          done = true
        end
      end
      battle.pbDisplay(self.format(msg || DEFAULT_DURATION_TEXT, user.pbThis, move.name)) if done
    end
  end

  #=============================================================================
  # New named battler effects (effects: [...])
  #=============================================================================
  side_effect = lambda do |const_name, turns|
    proc { |b|
      side = b.pbOwnSide
      c = PBEffects.const_get(const_name)
      next false if side.effects[c] > 0
      side.effects[c] = turns
    }
  end
  BATTLER_EFFECT_PROCS.merge!(
    :tailwind     => [side_effect.call(:Tailwind, 4), "A tailwind rose behind {1}!"],
    :safeguard    => [side_effect.call(:Safeguard, 5), "{1} is cloaked in a mystical veil!"],
    :mist         => [side_effect.call(:Mist, 5), "{1} is shrouded in mist!"],
    :lucky_chant  => [side_effect.call(:LuckyChant, 5), "A lucky chant shields {1} from critical hits!"],
    :reflect      => [side_effect.call(:Reflect, 5), "A Reflect barrier rose before {1}!"],
    :light_screen => [side_effect.call(:LightScreen, 5), "A Light Screen rose before {1}!"],
    :wish         => [proc { |b|
                        pos = b.battle.positions[b.index]
                        next false if pos.effects[PBEffects::Wish] > 0
                        pos.effects[PBEffects::Wish]       = 2
                        pos.effects[PBEffects::WishAmount] = (b.totalhp / 2.0).round
                        pos.effects[PBEffects::WishMaker]  = b.pokemonIndex
                      }, "{1} made a wish!"],
    :taunt        => [proc { |b|
                        next false if b.effects[PBEffects::Taunt] > 0
                        b.effects[PBEffects::Taunt] = 4
                      }, "{1} is spoiling for a fight! It can only attack for a while."],
    :stealth_rock => [proc { |b|
                        side = b.pbOpposingSide
                        next false if side.effects[PBEffects::StealthRock]
                        side.effects[PBEffects::StealthRock] = true
                      }, "Pointed stones float around {1}'s foes!"],
    :spikes       => [proc { |b|
                        side = b.pbOpposingSide
                        next false if side.effects[PBEffects::Spikes] >= 3
                        side.effects[PBEffects::Spikes] += 1
                      }, "Spikes are scattered around {1}'s foes!"],
    :toxic_spikes => [proc { |b|
                        side = b.pbOpposingSide
                        next false if side.effects[PBEffects::ToxicSpikes] >= 2
                        side.effects[PBEffects::ToxicSpikes] += 1
                      }, "Poison spikes are scattered around {1}'s foes!"],
    :sticky_web   => [proc { |b|
                        side = b.pbOpposingSide
                        next false if side.effects[PBEffects::StickyWeb]
                        side.effects[PBEffects::StickyWeb] = true
                      }, "A sticky web spreads out around {1}'s foes!"]
  )

  # :add_type => TYPE (third type, like Forest's Curse / Trick-or-Treat)
  def self.apply_added_type(battle, battler, type)
    return false if !type || !GameData::Type.exists?(type)
    return false if battler.pbHasType?(type) || !battler.canChangeType?
    battler.effects[PBEffects::ExtraType] = type
    return true
  end

  #=============================================================================
  # Natural type: Mimicry takes the field's :camouflage type when no terrain is up
  #=============================================================================
  def self.natural_type(battle)
    camo = self.current_definition(battle)&.[](:camouflage)
    return (camo && GameData::Type.exists?(camo)) ? camo : nil
  end

  def self.apply_natural_type(battle, battler)
    return false if battle.field.terrain != :None || battler.fainted?
    return false if !battler.hasActiveAbility?(:MIMICRY) || !battler.canChangeType?
    camo = self.natural_type(battle)
    return false if !camo || battler.pbTypes == [camo]
    battle.pbShowAbilitySplash(battler)
    battler.pbChangeTypes(camo)
    battle.pbDisplay(self.format("{1} blended into its surroundings and became the {2} type!",
                                 battler.pbThis, GameData::Type.get(camo).name))
    battle.pbHideAbilitySplash(battler)
    return true
  end
end

#===============================================================================
# Battler hook: field status immunity
#===============================================================================
class Battle::Battler
  alias prismfall_fe_pbCanInflictStatus? pbCanInflictStatus?
  def pbCanInflictStatus?(newStatus, user, showMessages, move = nil, ignoreStatus = false)
    ret = prismfall_fe_pbCanInflictStatus?(newStatus, user, showMessages, move, ignoreStatus)
    return ret if !ret || !@battle.respond_to?(:fe_state) || !@battle.fe_state
    return ret if !FieldEffects.active?(@battle)
    return ret if user && user.index == @index && move   # Rest still works
    msg = FieldEffects.status_immunity_message(@battle, self, newStatus)
    return ret if msg.nil?
    @battle.pbDisplay(FieldEffects.format(msg, pbThis)) if showMessages && !msg.empty?
    return false
  end
end

#===============================================================================
# Terrain Pulse takes the field's natural type (and doubles) when no terrain is up
#===============================================================================
class Battle::Move::TypeAndPowerDependOnTerrain < Battle::Move
  alias prismfall_fe_pbBaseType pbBaseType
  def pbBaseType(user)
    ret = prismfall_fe_pbBaseType(user)
    return ret if @battle.field.terrain != :None || !FieldEffects.active?(@battle)
    return FieldEffects.natural_type(@battle) || ret
  end

  alias prismfall_fe_pbBaseDamage pbBaseDamage
  def pbBaseDamage(baseDmg, user, target)
    ret = prismfall_fe_pbBaseDamage(baseDmg, user, target)
    if @battle.field.terrain == :None && FieldEffects.natural_type(@battle) && !user.airborne?
      ret *= 2
    end
    return ret
  end
end
