#===============================================================================
# ASHEN_WASTE - Quenched volcano (or burnt forest): a crust of cooled magma
# under drifting ash. Fertile, choking, and still warm deep below.
#===============================================================================
FieldEffects.register(:ASHEN_WASTE, {
  :name          => "Ashen Waste",
  :backdrop      => "field_ashen_waste",
  :intro_message => "Grey ash drifts over the cooled crust...",
  :description   => "Ash clouds hamper aim and choke the unprotected; Ground, Rock and new growth thrive.",
  :nature_power  => :SCORCHINGSANDS,
  :camouflage    => :GROUND,
  :secret_power  => 8,
  :type_mods     => { :GROUND => 1.2, :ROCK => 1.2, :GRASS => 1.2, :FIRE => 0.8 },
  :type_messages => { :GRASS => "New growth burst from the fertile ash!",
                      :FIRE  => "The ash smothered the flames..." },
  :move_mods     => { :SCORCHINGSANDS => 1.3, :SANDTOMB => 1.5, :MUDSLAP => 1.5 },
  :damage_mods   => [
    { :moves => [:GUST, :TWISTER, :HURRICANE, :AIRCUTTER, :WHIRLWIND, :RAZORWIND, :BLEAKWINDSTORM],
      :category => :damaging, :mult => 1.2, :message => "The wind whipped the ash into a storm!" }
  ],
  :accuracy_mods => [
    { :user => { :not_types => [:GROUND, :ROCK, :FIRE] }, :mult => 0.9 },
    { :target => { :abilities => [:SANDVEIL] }, :evasion_mult => 1.25 }
  ],
  :added_effects => [
    { :moves => [:GUST, :TWISTER, :HURRICANE, :AIRCUTTER, :RAZORWIND, :BLEAKWINDSTORM], :chance => 30,
      :stats => { :ACCURACY => -1 }, :message => "{1} was blinded by flying ash!" }
  ],
  :move_stat_boosts => [
    { :moves => [:SANDATTACK, :SMOKESCREEN], :target_stats => { :ACCURACY => -1 },
      :message => "A cloud of ash billowed up!" },
    { :moves => [:GROWTH], :user_stats => { :SPECIAL_ATTACK => 1 },
      :message => "{1} drew strength from the fertile ash!" }
  ],
  :speed_mods    => [{ :battlers => { :abilities => [:SANDRUSH] }, :mult => 1.5 }],
  :end_of_round  => [
    { :battlers => { :not_types => [:FIRE, :GROUND, :ROCK, :STEEL],
                     :not_abilities => [:OVERCOAT, :SANDVEIL, :SANDRUSH, :SANDFORCE],
                     :not_items => [:SAFETYGOGGLES] },
      :damage => 1/16r, :message => "{1} is choking on the ash!" }
  ],
  :weather       => { :extend => { :Sandstorm => 2 } },
  :terrain       => { :extend => { :Grassy => 2 } },
  :transitions   => [
    { :moves => [:DEFOG], :to => :NONE, :message => "The wind cleared the ash from the battlefield!" },
    { :moves => [:ERUPTION, :LAVAPLUME, :MAGMASTORM, :FIREPLEDGE], :to => :VOLCANIC, :uses => 3,
      :progress_message => "The crust glows red beneath the ash... ({1} more)",
      :message => "The magma reawakened beneath the ash!" }
  ],
  :seed => { :item => :TELLURICSEED, :stats => { :DEFENSE => 1, :EVASION => 1 },
             :message => "{1}'s {2} cloaked it in ash!" }
})
