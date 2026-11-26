#===============================================================================
# Prismfall Base Fixes - 004 Gen 9 Pack AI scoring: an undefined `b` (base-project bug, not a Prismfall one)
#-------------------------------------------------------------------------------
# "[002] Battle_AI/[002] AI New Move Rankings.rb" builds several move scores by calling another move's handler with
# an undefined local `b`:
#     Battle::AI::Handlers.apply_move_effect_against_target_score("PoisonTarget",
#       0, move, user, b, ai, battle)
# Each raises NameError when the AI weighs the move; the engine logs it and the AI never picks the move. Hit:
#   target procs (|score, move, user, target, ai, battle|): Barb Barrage (PoisonTarget), Infernal Parade and
#     Bitter Blade-style HealUserByHalfOfDamageDoneBurnTarget (BurnTarget)  -> pass `target`
#   user-only procs (|score, move, user, ai, battle|): Stone Axe / Ceaseless Edge (AddStealthRocks / AddSpikes),
#     Chilly Reception (SwitchOutUserStatusMove), Shed Tail (SwitchOutUserStatusMove, UserMakeSubstitute)
#     -> those are MoveEffectScore handlers with no target: call apply_move_effect_score(code, 0, move, user, ai, battle)
# The two other `b` uses in the file sit inside loops that define `b` and are left alone. Rewritten in memory as the
# file is evaluated (001's source-patch mechanism, :all => every match). A Gen 9 Pack without the bug doesn't match.
# Found by the engine-hooks agent 2026-11-25 (TODO_QUOTA.md).
#===============================================================================
module PluginManager
  PRISMFALL_SOURCE_PATCHES[:gen9_ai_undefined_b_target] = {
    :file => "AI New Move Rankings.rb", :all => true,
    # exactly six spaces before "0, move": the two calls inside each_foe_battler loops (where `b` IS defined) are deeper
    :line => /(apply_move_effect_against_target_score\("(?:PoisonTarget|BurnTarget)",\n {6}0, move, user, )b(, ai, battle\))/,
    :with => '\1target\2',
    :note => "AI scores for Barb Barrage / Infernal Parade / burn-heal moves pass `target` (Gen 9 Pack fix)"
  }
  PRISMFALL_SOURCE_PATCHES[:gen9_ai_undefined_b_user] = {
    :file => "AI New Move Rankings.rb", :all => true,
    :line => /apply_move_effect_against_target_score\(("(?:AddSpikesToFoeSide|AddStealthRocksToFoeSide|SwitchOutUserStatusMove|UserMakeSubstitute)",\s*0, move, user, )b, (ai, battle\))/,
    :with => 'apply_move_effect_score(\1\2',
    :note => "AI scores for Stone Axe / Ceaseless Edge / Chilly Reception / Shed Tail use the user-only handler (Gen 9 Pack fix)"
  }
end
