#===============================================================================
# DESERT - Gym 5 (Ground), Duneholt. Endless dunes under a merciless sun.
#===============================================================================
FieldEffects.register(:DESERT, {
  :name          => "Desert",
  :backdrop      => "field_desert",
  :intro_message => "Heat shimmers over the endless dunes...",
  :description   => "Sand abilities work without a sandstorm; sand moves and sunlight surge; ice wilts.",
  :nature_power  => :SANDTOMB,
  :camouflage    => :GROUND,
  :secret_power  => 8,
  :type_mods     => { :GROUND => 1.2, :FIRE => 1.2, :ICE => 0.75, :WATER => 0.8 },
  :type_messages => { :GROUND => "The shifting sands surged!",
                      :WATER  => "The desert heat evaporated some of the water..." },
  :move_mods     => { :SANDTOMB => 2.0, :SCORCHINGSANDS => 1.5, :SANDSEARSTORM => 1.3, :SOLARBEAM => 1.5,
                      :SOLARBLADE => 1.5, :NEEDLEARM => 1.5, :DIG => 1.5, :THOUSANDWAVES => 1.3,
                      :BONECLUB => 1.3, :BONEMERANG => 1.3, :BONERUSH => 1.3 },
  :move_messages => { :SANDTOMB  => "The sands swallowed the foe whole!",
                      :SOLARBEAM => "The desert sun blazed through {2}!",
                      :DIG       => "{1} burrowed through the soft sand!" },
  :damage_mods   => [
    { :types => [:GROUND, :ROCK, :STEEL], :user => { :abilities => [:SANDFORCE] }, :mult => 1.3 },
    { :category => :special, :user => { :abilities => [:SOLARPOWER] }, :attack_mult => 1.5 }
  ],
  :accuracy_mods => [
    { :moves => [:SANDATTACK], :always_hit => true },
    { :moves => [:SANDTOMB], :mult => 1.25 },
    { :target => { :abilities => [:SANDVEIL] }, :evasion_mult => 1.25 }
  ],
  :added_effects => [
    { :types => [:GROUND], :category => :physical, :chance => 20, :stats => { :ACCURACY => -1 },
      :message => "{1} got sand in its eyes!" }
  ],
  :move_stat_boosts => [
    { :moves => [:SANDATTACK], :target_stats => { :ACCURACY => -1 },
      :message => "The desert wind whipped up the sand!" },
    { :moves => [:SHOREUP], :user_stats => { :DEFENSE => 1 }, :message => "{1} packed the sand tight!" }
  ],
  :speed_mods    => [{ :battlers => { :abilities => [:SANDRUSH] }, :mult => 2.0 }],
  :end_of_round  => [
    { :battlers => { :abilities => [:DRYSKIN, :SOLARPOWER] }, :damage => 1/8r,
      :message => "The scorching sun beat down on {1}!" },
    { :battlers => { :types => [:ICE] }, :damage => 1/16r, :message => "{1} is wilting in the desert heat!" }
  ],
  :weather       => { :block => [:Hail], :block_message => "The desert heat melted the hail before it fell!",
                      :extend => { :Sandstorm => 3, :Sun => 2 } },
  :terrain       => { :block => [:Grassy], :block_message => "Nothing can grow in the dunes!" },
  :seed => { :item => :TELLURICSEED, :stats => { :DEFENSE => 1, :SPECIAL_DEFENSE => 1, :SPEED => -1 },
             :message => "{1}'s {2} encased it in hardened sand!" }
})
