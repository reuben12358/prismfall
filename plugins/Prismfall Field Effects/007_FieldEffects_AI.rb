#===============================================================================
# Prismfall Field Effects - AI awareness (v21.1 AI), all alias-chained
#-------------------------------------------------------------------------------
# * Move type changes reach the AI automatically (rough_type -> pbCalcType).
# * Priority changes reach it automatically (rough_priority -> pbPriority).
# * Type immunity checks use Battle::Move#pbCalcTypeMod (hooked in 005).
# Added here: damage multipliers, effectiveness, accuracy, crit, move failure,
# end-of-round damage/healing, and a score bonus for field stat boosts.
#===============================================================================
class Battle::AI::AIMove
  alias prismfall_fe_rough_damage rough_damage
  def rough_damage
    ret = prismfall_fe_rough_damage
    battle = @ai.battle
    return ret if ret <= 0 || !FieldEffects.active?(battle) || !@ai.trainer.medium_skill?
    if @move.is_a?(Battle::Move::FixedDamageMove)
      return FieldEffects.modify_fixed_damage(battle, @ai.user.battler, @ai.target.battler, @move, ret, true)
    end
    mult = FieldEffects.damage_multiplier(battle, @ai.user.battler, @ai.target.battler,
                                          @move, rough_type)
    return ret if mult == 1.0
    ret = [(ret * mult).round, 1].max
    target = @ai.target
    ret = target.hp - 1 if @move.nonLethal?(@ai.user.battler, target.battler) && ret >= target.hp
    return ret
  end

  alias prismfall_fe_apply_rough_accuracy_modifiers apply_rough_accuracy_modifiers
  def apply_rough_accuracy_modifiers(user, target, calc_type, modifiers)
    prismfall_fe_apply_rough_accuracy_modifiers(user, target, calc_type, modifiers)
    return if !FieldEffects.active?(@ai.battle) || !@ai.trainer.medium_skill?
    FieldEffects.apply_accuracy_mods(@ai.battle, user.battler, target.battler, @move,
                                     calc_type, modifiers)
  end

  alias prismfall_fe_rough_critical_hit_stage rough_critical_hit_stage
  def rough_critical_hit_stage
    ret = prismfall_fe_rough_critical_hit_stage
    return ret if ret < 0 || !FieldEffects.active?(@ai.battle)
    add, always = FieldEffects.crit_change(@ai.battle, @ai.user.battler, @ai.target.battler,
                                           @move, rough_type)
    return 99 if always
    return ret if add == 0
    return [ret + add, Battle::Move::CRITICAL_HIT_RATIOS.length - 1].min
  end
end

class Battle::AI::AIBattler
  # Re-computes effectiveness per defending type when the field alters the
  # type chart (inverse, overrides, extra types); otherwise uses the original.
  alias prismfall_fe_effectiveness_of_type_against_battler effectiveness_of_type_against_battler
  def effectiveness_of_type_against_battler(type, user = nil, move = nil)
    ret = prismfall_fe_effectiveness_of_type_against_battler(type, user, move)
    battle = @ai.battle
    return ret if !type || type == :SHADOW || !FieldEffects.active?(battle)
    return ret if !FieldEffects.effectiveness_rules_active?(battle)
    return ret if type == :GROUND && has_type?(:FLYING) && has_active_item?(:IRONBALL)
    user_battler = (user.respond_to?(:battler)) ? user.battler : user
    real_move = (move.respond_to?(:move) && move.move.is_a?(Battle::Move)) ? move.move : move
    real_move = nil if !real_move.is_a?(Battle::Move)
    types = [type]
    if real_move && user_battler
      FieldEffects.extra_types(battle, user_battler, battler, real_move, type).each do |t, _m|
        types.push(t) if GameData::Type.exists?(t)
      end
    end
    ret = Effectiveness::NORMAL_EFFECTIVE_MULTIPLIER
    types.each_with_index do |atk_type, i|
      battler.pbTypes(true).each do |defend_type|
        mult = effectiveness_of_type_against_single_battler_type(atk_type, defend_type, user)
        if real_move && i == 0
          case real_move.function_code
          when "HitsTargetInSkyGroundsTarget"
            mult = Effectiveness::NORMAL_EFFECTIVE_MULTIPLIER if atk_type == :GROUND && defend_type == :FLYING
          when "FreezeTargetSuperEffectiveAgainstWater"
            mult = Effectiveness::SUPER_EFFECTIVE_MULTIPLIER if defend_type == :WATER
          end
        end
        mult = FieldEffects.modify_effectiveness(battle, real_move, atk_type, defend_type,
                                                 user_battler, battler, mult)
        next if i > 0 && mult == 0   # An immune added type is treated as neutral
        ret *= mult
      end
    end
    ret *= 2 if self.effects[PBEffects::TarShot] && type == :FIRE
    return ret
  end

  # Field end-of-round damage (positive) / healing (negative).
  alias prismfall_fe_rough_end_of_round_damage rough_end_of_round_damage
  def rough_end_of_round_damage
    ret = prismfall_fe_rough_end_of_round_damage
    battle = @ai.battle
    return ret if !FieldEffects.active?(battle)
    FieldEffects.rules(battle, :end_of_round).each do |rule|
      next if rule[:battlers] && !FieldEffects.battler_matches?(rule[:battlers], battle, battler)
      chance = (rule[:chance] || 100) / 100.0
      if rule[:damage] && battler.takesIndirectDamage?
        amt = self.totalhp * rule[:damage].to_f
        amt *= Effectiveness.calculate(rule[:damage_type], *battler.pbTypes(true)) if rule[:damage_type]
        ret += (amt * chance).round
      end
      if rule[:heal] && battler.canHeal?
        ret -= (self.totalhp * rule[:heal].to_f * chance).round
      end
    end
    return ret
  end
end

class Battle::AI
  # Moves the field makes fail, and weather/terrain moves the field blocks.
  # :weather_as moves (e.g. Aurora Veil without hail) are judged with that weather.
  alias prismfall_fe_pbGetMoveScore pbGetMoveScore
  def pbGetMoveScore(targets = nil)
    weather = FieldEffects.weather_as_for(@battle, @user.battler, @move.move)
    return FieldEffects.with_weather_as(@user.battler, weather) { prismfall_fe_pbGetMoveScore(targets) }
  end

  alias prismfall_fe_pbPredictMoveFailure pbPredictMoveFailure
  def pbPredictMoveFailure
    weather = FieldEffects.weather_as_for(@battle, @user.battler, @move.move)
    failed = FieldEffects.with_weather_as(@user.battler, weather) { prismfall_fe_pbPredictMoveFailure }
    return true if failed
    return false if !FieldEffects.active?(@battle)
    return true if FieldEffects.move_failure_message(@battle, @user.battler, @move.move)
    weather = FieldEffects::AI_WEATHER_MOVES[@move.function_code]
    return true if weather && FieldEffects.env_spec_value(@battle, :weather, :block,
                     FieldEffects.env_spec_value(@battle, :weather, :transform, weather) || weather)
    terrain = FieldEffects::AI_TERRAIN_MOVES[@move.function_code]
    return true if terrain && FieldEffects.env_spec_value(@battle, :terrain, :block,
                     FieldEffects.env_spec_value(@battle, :terrain, :transform, terrain) || terrain)
    return false
  end
end

module FieldEffects
  AI_WEATHER_MOVES = {
    "StartSunWeather"       => :Sun,
    "StartRainWeather"      => :Rain,
    "StartSandstormWeather" => :Sandstorm,
    "StartHailWeather"      => :Hail
  }.freeze
  AI_TERRAIN_MOVES = {
    "StartElectricTerrain" => :Electric,
    "StartGrassyTerrain"   => :Grassy,
    "StartMistyTerrain"    => :Misty,
    "StartPsychicTerrain"  => :Psychic
  }.freeze
end

#===============================================================================
# Score bonus for moves that gain stat boosts on this field, plus per-field
# :ai_score hooks.
#===============================================================================
Battle::AI::Handlers::GeneralMoveScore.add(:prismfall_field_effects,
  proc { |score, move, user, ai, battle|
    next score if !FieldEffects.active?(battle) || !ai.trainer.medium_skill?
    old_score = score
    FieldEffects.rules(battle, :move_stat_boosts).each do |rule|
      next if !FieldEffects.move_matches?(rule, battle, user.battler, nil, move.move, move.rough_type)
      rule[:user_stats]&.each do |stat, n|
        next if n <= 0 || user.statStageAtMax?(stat)
        score += 4 * n
      end
      score += 3 * rule[:target_stats].values.count { |n| n < 0 } if rule[:target_stats]
    end
    FieldEffects.hooks(battle, :ai_score).each do |h|
      val = FieldEffects.safe_call(h, score, move, user, ai, battle)
      score = val if val.is_a?(Numeric)
    end
    PBDebug.log_score_change(score - old_score, "field effect") if score != old_score
    next score
  }
)
