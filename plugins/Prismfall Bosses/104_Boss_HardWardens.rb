#===============================================================================
# Hard mode: Warden aces as 2-bar bosses (GYM_PUZZLES.md: Ilsa, Gym 12 and
# Celestine, Gym 17). No event changes needed: the rules below fire on trainer
# load, so Prismfall.gym_battle(12) / (17) on Hard gets a boss ace (the last
# Pokémon of the loaded Hard team). Add more Wardens with register_trainer_boss.
#===============================================================================
Prismfall::Bosses.register(:WARDEN_ACE_2BAR, {
  :bars          => 2,
  :break_message => "{1}'s Warden sigil flared!",
  :on_break      => { :messages => ["{1} refuses to fall! Its Warden's resolve restores it!"],
                      :cure_status => true, :reset_stats => :negative,
                      :stats => { :DEFENSE => 1, :SPECIAL_DEFENSE => 1 } }
})

[[:HARD_ILSA, :LEADER_ILSA, "Ilsa"], [:HARD_CELESTINE, :LEADER_CELESTINE, "Celestine"]].each do |key, type, name|
  Prismfall::Bosses.register_trainer_boss(key, {
    :trainer_type => type, :name => name,
    :versions     => [0, 100],          # gym battle (Standard base / Hard variant); never Festival v50
    :condition    => proc { |_trainer| Prismfall::Difficulty.hard? },
    :slot         => :ace,
    :boss         => :WARDEN_ACE_2BAR
  })
end
