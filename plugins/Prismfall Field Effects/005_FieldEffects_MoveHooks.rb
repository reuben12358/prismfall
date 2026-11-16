#===============================================================================
# Prismfall Field Effects - Battle::Move hooks (all alias-chained)
#===============================================================================
class Battle::Move
  attr_reader :fe_type_message

  #-----------------------------------------------------------------------------
  # Type changes (also used by the AI via rough_type -> pbCalcType)
  #-----------------------------------------------------------------------------
  alias prismfall_fe_pbCalcType pbCalcType
  def pbCalcType(user)
    ret = prismfall_fe_pbCalcType(user)
    @fe_type_message = nil
    return ret if !ret || !FieldEffects.active?(@battle)
    new_type, msg = FieldEffects.changed_move_type(@battle, user, self, ret)
    if new_type && new_type != ret && GameData::Type.exists?(new_type)
      @fe_type_message = msg
      ret = new_type
    end
    return ret
  end

  #-----------------------------------------------------------------------------
  # Type effectiveness: inverse chart, per-matchup overrides, extra types
  #-----------------------------------------------------------------------------
  alias prismfall_fe_pbCalcTypeModSingle pbCalcTypeModSingle
  def pbCalcTypeModSingle(moveType, defType, user, target)
    ret = prismfall_fe_pbCalcTypeModSingle(moveType, defType, user, target)
    return ret if !FieldEffects.active?(@battle)
    return FieldEffects.modify_effectiveness(@battle, self, moveType, defType, user, target, ret)
  end

  alias prismfall_fe_pbCalcTypeMod pbCalcTypeMod
  def pbCalcTypeMod(moveType, user, target)
    ret = prismfall_fe_pbCalcTypeMod(moveType, user, target)
    return ret if !moveType || moveType == :SHADOW || ret == 0
    return ret if !FieldEffects.active?(@battle)
    FieldEffects.extra_types(@battle, user, target, self, moveType).each do |extra, _msg|
      next if !GameData::Type.exists?(extra)
      target.pbTypes(true).each do |def_type|
        eff = pbCalcTypeModSingle(extra, def_type, user, target)
        ret *= eff if eff > 0   # An immune added type is treated as neutral
      end
    end
    return ret
  end

  #-----------------------------------------------------------------------------
  # Damage
  #-----------------------------------------------------------------------------
  alias prismfall_fe_pbCalcDamageMultipliers pbCalcDamageMultipliers
  def pbCalcDamageMultipliers(user, target, numTargets, type, baseDmg, multipliers)
    prismfall_fe_pbCalcDamageMultipliers(user, target, numTargets, type, baseDmg, multipliers)
    return if !FieldEffects.active?(@battle)
    FieldEffects.apply_damage_mods(@battle, user, target, self, type, multipliers)
  end

  #-----------------------------------------------------------------------------
  # Accuracy
  #-----------------------------------------------------------------------------
  alias prismfall_fe_pbCalcAccuracyModifiers pbCalcAccuracyModifiers
  def pbCalcAccuracyModifiers(user, target, modifiers)
    prismfall_fe_pbCalcAccuracyModifiers(user, target, modifiers)
    return if !FieldEffects.active?(@battle)
    FieldEffects.apply_accuracy_mods(@battle, user, target, self, @calcType, modifiers)
  end

  #-----------------------------------------------------------------------------
  # Priority (used by turn order and by the AI's rough_priority)
  #-----------------------------------------------------------------------------
  alias prismfall_fe_pbPriority pbPriority
  def pbPriority(user)
    ret = prismfall_fe_pbPriority(user)
    return ret if !FieldEffects.active?(@battle)
    return ret + FieldEffects.priority_change(@battle, user, self)
  end

  #-----------------------------------------------------------------------------
  # Critical hits
  #-----------------------------------------------------------------------------
  alias prismfall_fe_pbIsCritical? pbIsCritical?
  def pbIsCritical?(user, target)
    return prismfall_fe_pbIsCritical?(user, target) if !FieldEffects.active?(@battle)
    add, always = FieldEffects.crit_change(@battle, user, target, self, @calcType)
    return prismfall_fe_pbIsCritical?(user, target) if add == 0 && !always
    old_focus = user.effects[PBEffects::FocusEnergy]
    old_laser = user.effects[PBEffects::LaserFocus]
    begin
      # Temporarily borrow Focus Energy / Laser Focus so every crit-preventing
      # effect (Battle Armor, Lucky Chant...) is still respected.
      user.effects[PBEffects::FocusEnergy] = old_focus + add if add > 0
      user.effects[PBEffects::LaserFocus]  = [old_laser, 1].max if always
      return prismfall_fe_pbIsCritical?(user, target)
    ensure
      user.effects[PBEffects::FocusEnergy] = old_focus
      user.effects[PBEffects::LaserFocus]  = old_laser
    end
  end

  #-----------------------------------------------------------------------------
  # Additional effect chance of the move's own secondary effect
  #-----------------------------------------------------------------------------
  alias prismfall_fe_pbAdditionalEffectChance pbAdditionalEffectChance
  def pbAdditionalEffectChance(user, target, effectChance = 0)
    ret = prismfall_fe_pbAdditionalEffectChance(user, target, effectChance)
    return ret if ret <= 0 || ret > 100 || !FieldEffects.active?(@battle)
    return FieldEffects.modify_effect_chance(@battle, user, target, self, ret)
  end
end

#===============================================================================
# Nature Power / Camouflage / Secret Power read the field (a built-in terrain,
# if present, still takes precedence).
#===============================================================================
class Battle::Move::UseMoveDependingOnEnvironment < Battle::Move
  alias prismfall_fe_pbOnStartUse pbOnStartUse
  def pbOnStartUse(user, targets)
    prismfall_fe_pbOnStartUse(user, targets)
    return if @battle.field.terrain != :None
    np = FieldEffects.current_definition(@battle)&.[](:nature_power)
    @npMove = np if np && GameData::Move.exists?(np)
  end
end

class Battle::Move::SetUserTypesBasedOnEnvironment < Battle::Move
  alias prismfall_fe_pbMoveFailed? pbMoveFailed?
  def pbMoveFailed?(user, targets)
    camo = nil
    if @battle.field.terrain == :None
      camo = FieldEffects.current_definition(@battle)&.[](:camouflage)
      camo = nil if camo && !GameData::Type.exists?(camo)
    end
    return prismfall_fe_pbMoveFailed?(user, targets) if !camo
    if !user.canChangeType? || !user.pbHasOtherType?(camo)
      @battle.pbDisplay(_INTL("But it failed!"))
      return true
    end
    @newType = camo
    return false
  end
end

class Battle::Move::EffectDependsOnEnvironment < Battle::Move
  alias prismfall_fe_pbOnStartUse pbOnStartUse
  def pbOnStartUse(user, targets)
    prismfall_fe_pbOnStartUse(user, targets)
    return if @battle.field.terrain != :None
    sp = FieldEffects.current_definition(@battle)&.[](:secret_power)
    @secretPower = sp if sp.is_a?(Integer)
  end
end
