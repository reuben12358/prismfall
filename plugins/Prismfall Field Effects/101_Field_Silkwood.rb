#===============================================================================
# SILKWOOD - Gym 1 (Bug), Briarwick. Ancient trees strung with giant silk webs.
#===============================================================================
FieldEffects.register(:SILKWOOD, {
  :name          => "Silkwood",
  :backdrop      => "field_silkwood",
  :intro_message => "Giant webs glisten between the ancient trees...",
  :description   => "Bugs thrive and webs entangle the grounded. Fire spreads through the silk.",
  :nature_power  => :BUGBUZZ,
  :camouflage    => :BUG,
  :secret_power  => 4,
  :type_mods     => { :BUG => 1.5, :GRASS => 1.2, :FIRE => 1.3 },
  :type_messages => { :BUG  => "The Silkwood hums with chittering life!",
                      :FIRE => "The flames raced along the silk!" },
  :move_mods     => { :ELECTROWEB => 1.5, :LUNGE => 1.3, :LEECHLIFE => 1.3, :STRUGGLEBUG => 1.5,
                      :POUNCE => 1.3, :ATTACKORDER => 1.3 },
  :move_messages => { :ELECTROWEB => "The current raced along the web strands!" },
  :damage_mods   => [
    # Swarm is always active here
    { :types => [:BUG], :user => { :abilities => [:SWARM] }, :mult => 1.5 },
    # Blades cut cleanly through the silk
    { :moves => [:CUT, :FURYCUTTER, :XSCISSOR, :SLASH, :NIGHTSLASH, :LEAFBLADE, :SACREDSWORD,
                 :AIRSLASH, :PSYCHOCUT, :CROSSPOISON], :mult => 1.2,
      :message => "{2} sliced through the silk!" },
    # Fliers get tangled in the canopy webs
    { :types => [:FLYING], :user => { :not_types => [:BUG] }, :mult => 0.8,
      :message => "{1} got snagged in the webs!" }
  ],
  :accuracy_mods => [
    { :moves => [:STRINGSHOT, :ELECTROWEB, :STICKYWEB], :always_hit => true },
    { :flags => ["Powder"], :mult => 1.2 },
    { :user => { :abilities => [:COMPOUNDEYES] }, :mult => 1.1 }
  ],
  :effect_chance_mods => [{ :types => [:BUG], :mult => 2.0 }],
  :added_effects => [
    { :types => [:BUG], :flags => ["Contact"], :chance => 20, :stats => { :SPEED => -1 },
      :message => "{1} got tangled in silk!" }
  ],
  :move_stat_boosts => [
    { :moves => [:STRINGSHOT, :SILKTRAP], :target_stats => { :SPEED => -1 },
      :message => "The webs wound tighter!" },
    { :moves => [:DEFENDORDER], :user_stats => { :DEFENSE => 1 },
      :message => "The swarm reinforced {1}!" }
  ],
  :on_entry => [
    # Gym 1 tuning: each Pokémon is caught by the webs only the FIRST time it enters this battle.
    { :battlers => { :grounded => true, :not_types => [:BUG], :not_items => [:HEAVYDUTYBOOTS],
                     :condition => proc { |battle, battler|
                       seen = battle.instance_variable_get(:@pf_silkwood_webbed) ||
                              battle.instance_variable_set(:@pf_silkwood_webbed, {})
                       key = battler.pokemon ? battler.pokemon.personalID : nil
                       next false if key.nil? || seen[[battler.index & 1, key]]
                       seen[[battler.index & 1, key]] = true
                       next true
                     } },
      :stats => { :SPEED => -1 }, :message => "{1} blundered into a sticky web!" }
  ],
  :end_of_round => [
    { :battlers => { :types => [:BUG] }, :heal => 1/16r, :message => "{1} fed on the forest's nectar." }
  ],
  :terrain => { :extend => { :Grassy => 3 } },
  :transitions => [
    { :types => [:FIRE], :category => :damaging, :to => :ASHEN_WASTE, :uses => 3,
      :progress_message => "Embers smoulder in the silk... ({1} more)",
      :message => "The webs went up in flames! The Silkwood burned down to ash!" }
  ],
  :seed => { :item => :TELLURICSEED, :stats => { :DEFENSE => 1 }, :effects => [:ingrain],
             :message => "{1}'s {2} sprouted silk-threaded roots!" }
})
