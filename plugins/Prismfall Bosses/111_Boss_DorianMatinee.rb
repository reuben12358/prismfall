#===============================================================================
# Gym 1 Dorian's Meloetta, the "Act One Matinee" (Gemini proposal 2026-11-23
# gen6-9-sprites-postgame-legendaries-dorian-meloetta, Part C). The Prima Donna
# holds back to a Badge-1 stage: one bar (no boss pips), no status immunity, no
# boss databox, all stats scaled down. Full 600-BST power is saved for the
# post-game "Crownhaven Encore" (PG_MELOETTA) and the Festival Pageant Bout
# (v90/190/290), which this rule never touches.
# Grand Stage pairing: Relic Song gets the Normal boost only (102_Field_GrandStage.rb
# :not_moves), so a Standing Ovation Relic Song can't double-stack.
#===============================================================================
Prismfall::Bosses.register(:DORIAN_MELOETTA_MATINEE, {
  :bars            => 1,
  :status_immunity => false,
  :catch           => false,
  :ebdx            => { :databox => false },
  :stat_mults      => {
    :CASUAL   => { :HP => 0.78, :ATTACK => 0.78, :DEFENSE => 0.78, :SPECIAL_ATTACK => 0.78, :SPECIAL_DEFENSE => 0.78, :SPEED => 0.78 },
    :STANDARD => { :HP => 0.80, :ATTACK => 0.80, :DEFENSE => 0.80, :SPECIAL_ATTACK => 0.80, :SPECIAL_DEFENSE => 0.80, :SPEED => 0.80 },
    :HARD     => { :HP => 0.85, :ATTACK => 0.85, :DEFENSE => 0.85, :SPECIAL_ATTACK => 0.85, :SPECIAL_DEFENSE => 0.85, :SPEED => 0.85 }
  },
  :intro       => ["Dorian: \"Easy now, my dear - this is Act One, not Opening Night!\"",
                   "Meloetta softens her tempo to match a challenger's first stage!"],
  :description => "Gym 1 Dorian's ace Meloetta scaled to Act One (x0.80 / Hard x0.85 / Casual x0.78); never Festival or Pageant"
})

Prismfall::Bosses.register_trainer_boss(:DORIAN_GYM1_MELOETTA, {
  :trainer_type => :LEADER_DORIAN, :name => "Dorian",
  :versions     => [0, 100, 200],   # Gym 1 only: never Festival v50 or the Pageant Bout v90
  :species      => :MELOETTA,
  :boss         => :DORIAN_MELOETTA_MATINEE
})
