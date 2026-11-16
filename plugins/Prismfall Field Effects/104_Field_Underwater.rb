#===============================================================================
# UNDERWATER - Beneath the waves. Reached by Dive from WATER_SURFACE.
#===============================================================================
FieldEffects.register(:UNDERWATER, {
  :name          => "Underwater",
  :backdrop      => "field_underwater",
  :intro_message => "Blue silence presses in from every side... The battle is underwater!",
  :description   => "Water rules, fire fails, physical non-Water attacks drag; air-breathers struggle.",
  :nature_power  => :WATERPULSE,
  :camouflage    => :WATER,
  :secret_power  => 5,
  :type_mods     => { :WATER => 1.5, :ELECTRIC => 1.3, :FLYING => 0.5 },
  :type_messages => { :WATER  => "The deep currents empowered the attack!",
                      :FLYING => "There's no air to ride down here..." },
  :move_mods     => { :DIVE => 1.5, :ANCHORSHOT => 1.5, :WATERPULSE => 1.3, :WHIRLPOOL => 1.5,
                      :CRABHAMMER => 1.2 },
  :move_messages => { :ANCHORSHOT => "The anchor plunged through the depths!" },
  :damage_mods   => [
    { :category => :physical, :not_types => [:WATER], :user => { :not_types => [:WATER] },
      :mult => 0.5, :message => "The water's resistance slowed {1}'s attack!" },
    { :flags => ["Sound"], :mult => 1.3, :message => "{2} carried far through the water!" }
  ],
  :accuracy_mods => [{ :moves => [:WHIRLPOOL], :mult => 1.25 }],
  :move_fails    => [
    { :types => [:FIRE], :message => "{2} fizzled out in the deep water!" },
    { :moves => [:FLY, :BOUNCE, :SKYDROP, :SPIKES, :TOXICSPIKES, :STEALTHROCK, :STICKYWEB],
      :message => "{2} is impossible underwater!" }
  ],
  :speed_mods    => [
    { :battlers => { :not_types => [:WATER], :not_abilities => [:SWIFTSWIM] }, :mult => 0.5 },
    { :battlers => { :abilities => [:SWIFTSWIM] }, :mult => 2.0 }
  ],
  :on_entry      => [
    { :battlers => { :status => [:BURN] }, :cure_status => true, :also_on_change => true,
      :message => "The water extinguished {1}'s burn!" }
  ],
  :end_of_round  => [
    { :battlers => { :not_types => [:WATER], :not_abilities => [:WATERABSORB, :DRYSKIN, :STORMDRAIN,
                                                                :SWIFTSWIM, :WATERVEIL] },
      :damage => 1/16r, :damage_type => :WATER, :message => "{1} is struggling for air!" },
    { :battlers => { :abilities => [:WATERABSORB, :DRYSKIN] }, :heal => 1/16r,
      :message => "{1} drank in the sea." }
  ],
  :weather       => { :block => [:Sun, :Rain, :Sandstorm, :Hail, :HarshSun, :HeavyRain, :StrongWinds],
                      :block_message => "The weather can't reach the depths!" },
  :terrain       => { :block => [:Electric, :Grassy, :Misty, :Psychic],
                      :block_message => "Nothing can settle on the shifting sea floor!" },
  :transitions   => [
    { :moves => [:DIVE, :BOUNCE], :even_if_failed => true, :to => :WATER_SURFACE,
      :message => "The battle burst back up to the surface!" }
  ],
  :seed => { :item => :ELEMENTALSEED, :stats => { :DEFENSE => 1 }, :effects => [:aqua_ring],
             :message => "{1}'s {2} released a bubble of air around it!" }
})
