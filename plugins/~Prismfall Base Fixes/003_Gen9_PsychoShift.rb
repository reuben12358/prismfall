#===============================================================================
# Prismfall Base Fixes - 003 Gen 9 Pack Psycho Shift crash (base-project bug, not a Prismfall one)
#-------------------------------------------------------------------------------
# The Generation 9 Pack 3.2.5 (Manurocker95's Essentials 21 + EBDX project, SETUP option B, and the headless harness's
# base) overrides Psycho Shift in "[003] Moves/[000] Move Functions.rb":
#   class Battle::Move::GiveUserStatusToTarget
#     alias paldea_pbEffectAgainstTarget pbEffectAgainstTarget
#     def pbEffectAgainstTarget(user, target)
#       if [:DROWSY, :FROSTBITE].include?(user.status) ... else
#         paldea_pbEffectAgainstTarget          # <- no (user, target)
# so every Psycho Shift that passes a burn, poison, paralysis or sleep raises ArgumentError and ends the battle. The
# Gen 9 Pack 3.3.8 in the EBDX Renovation fork (SETUP option A) already passes the arguments; there the line is not
# found and this does nothing. Like 001, it rewrites the line in memory as the file is evaluated (this plugin loads
# before every other one). Checked by tools/harness/run_all.rb (section 4, base-project regressions).
#===============================================================================
module PluginManager
  PRISMFALL_SOURCE_PATCHES[:gen9_psycho_shift] = {
    :file => "Move Functions.rb",
    :line => /^([ \t]*)paldea_pbEffectAgainstTarget[ \t]*$/,
    :with => '\1paldea_pbEffectAgainstTarget(user, target)   # arguments restored by Prismfall Base Fixes',
    :note => "Psycho Shift passes (user, target) to the base move (Gen 9 Pack fix)"
  }
end
