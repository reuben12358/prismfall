#===============================================================================
# Prismfall Field Effects - Battle::Battler and Battle hooks (all alias-chained)
#===============================================================================
class Battle::Battler
  #-----------------------------------------------------------------------------
  # New move use (message de-duplication)
  #-----------------------------------------------------------------------------
  alias prismfall_fe_pbUseMove pbUseMove
  # Also: :weather_as for the move's whole use, and :even_if_failed
  # transitions for moves that fail before their hits (pbMoveFailed? etc.).
  def pbUseMove(choice, specialUsage = false)
    FieldEffects.begin_move_use(@battle)
    use = FieldEffects.push_move_use(@battle)
    outer_done = @fe_after_move_done
    @fe_after_move_done = false
    weather = FieldEffects.weather_as_for(@battle, self, choice[2])
    FieldEffects.with_weather_as(self, weather) { prismfall_fe_pbUseMove(choice, specialUsage) }
    mv = choice[2]
    if !@fe_after_move_done && !use[:landed] && @lastMoveFailed && mv && @lastMoveUsed == mv.id
      FieldEffects.failed_move_transitions(@battle, self, mv)
    end
  ensure
    FieldEffects.pop_move_use(@battle, use) if use
    @fe_after_move_done = outer_done
  end

  # Remembers the move, user and targets of the hit being processed, so the move's
  # field change can fire as soon as its damage lands (FieldEffects.hit_recorded).
  alias prismfall_fe_pbProcessMoveHit pbProcessMoveHit
  def pbProcessMoveHit(move, user, targets, hitNum, skipAccuracyCheck)
    use = FieldEffects.move_use(@battle)
    return prismfall_fe_pbProcessMoveHit(move, user, targets, hitNum, skipAccuracyCheck) if !use
    outer = use[:hit]
    use[:hit] = [move, user, targets]
    begin
      return prismfall_fe_pbProcessMoveHit(move, user, targets, hitNum, skipAccuracyCheck)
    ensure
      use[:hit] = outer
    end
  end

  # Weather a :weather_as rule lends to this battler's current move.
  alias prismfall_fe_effectiveWeather effectiveWeather
  def effectiveWeather
    ret = prismfall_fe_effectiveWeather
    return @fe_weather_as if @fe_weather_as && ret == :None
    return ret
  end

  #-----------------------------------------------------------------------------
  # Moves that fail on the field (after sleep/paralysis/confusion checks)
  #-----------------------------------------------------------------------------
  alias prismfall_fe_pbTryUseMove pbTryUseMove
  def pbTryUseMove(choice, move, specialUsage, skipAccuracyCheck)
    ret = prismfall_fe_pbTryUseMove(choice, move, specialUsage, skipAccuracyCheck)
    return ret if !ret
    mv = choice[2] || move
    return ret if !mv || mv == @battle.struggle
    msg = FieldEffects.move_failure_message(@battle, self, mv)
    return ret if !msg
    pbReducePP(mv) if !specialUsage
    @battle.pbDisplay(_INTL("{1} used {2}!", pbThis, mv.name))
    @battle.pbDisplay(FieldEffects.format(msg, pbThis, mv.name))
    @lastMoveFailed = true
    mv.calcType = mv.pbCalcType(self)
    @fe_after_move_done = true
    FieldEffects.failed_move_transitions(@battle, self, mv)
    return false
  end

  #-----------------------------------------------------------------------------
  # Added effects, once per hit per target
  #-----------------------------------------------------------------------------
  alias prismfall_fe_pbEffectsOnMakingHit pbEffectsOnMakingHit
  def pbEffectsOnMakingHit(move, user, target)
    prismfall_fe_pbEffectsOnMakingHit(move, user, target)
    return if target.fainted? && user.fainted?
    FieldEffects.apply_added_effects(@battle, user, target, move)
  end

  #-----------------------------------------------------------------------------
  # Move-triggered transitions (if the move didn't already change the field when
  # it landed), then stat boosts on use and after_move hooks (on the old field if
  # it just changed). Runs before the original so U-turn/Eject Button switching
  # can't change "user"; the original's effects see the new field.
  #-----------------------------------------------------------------------------
  alias prismfall_fe_pbEffectsAfterMove pbEffectsAfterMove
  def pbEffectsAfterMove(user, targets, move, numHits)
    @fe_after_move_done = true
    FieldEffects.after_move(@battle, user, targets, move, numHits)
    prismfall_fe_pbEffectsAfterMove(user, targets, move, numHits)
  end

  #-----------------------------------------------------------------------------
  # Speed
  #-----------------------------------------------------------------------------
  alias prismfall_fe_pbSpeed pbSpeed
  def pbSpeed
    ret = prismfall_fe_pbSpeed
    return ret if fainted? || !FieldEffects.active?(@battle)
    mult = FieldEffects.speed_multiplier(@battle, self)
    return ret if mult == 1.0
    return [(ret * mult).round, 1].max
  end

  #-----------------------------------------------------------------------------
  # Abilities negated by the field
  #-----------------------------------------------------------------------------
  alias prismfall_fe_abilityActive? abilityActive?
  def abilityActive?(ignore_fainted = false, check_ability = nil)
    ret = prismfall_fe_abilityActive?(ignore_fainted, check_ability)
    return ret if !ret
    return ret if !@battle.respond_to?(:fe_state) || !@battle.fe_state
    return false if FieldEffects.ability_negated?(@battle, @ability_id) && !unstoppableAbility?
    return ret
  end
end

#===============================================================================
# Battle
#===============================================================================
class Battle
  #-----------------------------------------------------------------------------
  # On-entry effects: right after entry hazards, before switch-in abilities
  #-----------------------------------------------------------------------------
  alias prismfall_fe_pbEntryHazards pbEntryHazards
  def pbEntryHazards(battler)
    prismfall_fe_pbEntryHazards(battler)
    return if battler.fainted?
    FieldEffects.apply_entry_effects(self, battler)
  end

  #-----------------------------------------------------------------------------
  # End of round: after terrain countdown, before EOR abilities/items
  #-----------------------------------------------------------------------------
  alias prismfall_fe_pbEOREndTerrain pbEOREndTerrain
  def pbEOREndTerrain
    prismfall_fe_pbEOREndTerrain
    FieldEffects.end_of_round(self)
    FieldEffects.scripted_changes(self)
  end

  #-----------------------------------------------------------------------------
  # Weather: block / transform / extend / transitions
  #-----------------------------------------------------------------------------
  alias prismfall_fe_pbStartWeather pbStartWeather
  def pbStartWeather(user, newWeather, fixedDuration = false, showAnim = true)
    if newWeather && newWeather != :None && FieldEffects.active?(self)
      transformed = FieldEffects.env_spec_value(self, :weather, :transform, newWeather)
      newWeather = transformed if transformed
      if FieldEffects.env_spec_value(self, :weather, :block, newWeather)
        pbHideAbilitySplash(user) if user
        pbDisplay(FieldEffects.format(FieldEffects.env_block_message(self, :weather)))
        return
      end
    end
    old_weather = @field.weather
    prismfall_fe_pbStartWeather(user, newWeather, fixedDuration, showAnim)
    return if @field.weather == old_weather || @field.weather != newWeather
    return if !FieldEffects.active?(self)
    ext = FieldEffects.env_spec_value(self, :weather, :extend, newWeather).to_i
    @field.weatherDuration += ext if ext > 0 && @field.weatherDuration > 0
    FieldEffects.check_env_transitions(self, :weather, newWeather)
  end

  #-----------------------------------------------------------------------------
  # Terrain: block / transform / extend / transitions
  #-----------------------------------------------------------------------------
  alias prismfall_fe_pbStartTerrain pbStartTerrain
  def pbStartTerrain(user, newTerrain, fixedDuration = true)
    if newTerrain && newTerrain != :None && FieldEffects.active?(self)
      transformed = FieldEffects.env_spec_value(self, :terrain, :transform, newTerrain)
      newTerrain = transformed if transformed
      if FieldEffects.env_spec_value(self, :terrain, :block, newTerrain)
        pbHideAbilitySplash(user) if user
        pbDisplay(FieldEffects.format(FieldEffects.env_block_message(self, :terrain)))
        return
      end
    end
    old_terrain = @field.terrain
    prismfall_fe_pbStartTerrain(user, newTerrain, fixedDuration)
    return if @field.terrain == old_terrain || @field.terrain != newTerrain
    return if !FieldEffects.active?(self)
    ext = FieldEffects.env_spec_value(self, :terrain, :extend, newTerrain).to_i
    @field.terrainDuration += ext if ext > 0 && @field.terrainDuration > 0
    FieldEffects.check_env_transitions(self, :terrain, newTerrain)
  end
end
