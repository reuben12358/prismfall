#===============================================================================
# UNDERWATER - Beneath the waves (Dive from WATER_SURFACE, sea-floor ruins).
# Water Pokemon are in their element; sound carries for miles, current spreads
# through everything, silt churns into ground attacks. Fire can't burn here.
# Surfacing moves return to WATER_SURFACE; sludge drives everyone up into a
# CORROSIVE_MIRE. Family: Elemental.
#===============================================================================
FieldEffects.register(:UNDERWATER, {
  :name          => "Underwater",
  :backdrop      => "field_underwater",
  :family        => :elemental,
  :intro_message => "Blue silence presses in from every side... The battle is underwater!",
  :description   => "The deep belongs to swimmers: Water and Electric surge, sound carries, silt joins ground attacks. Fire can't burn and heavy blows drag.",
  :notes         => ["Water x1.5. Electric x1.5 and never misses. Flying x0.5 (no air to catch). Sound moves x1.3.",
                     "Ground attacks churn up the seabed and also hit as Water.",
                     "Physical non-Water attacks from non-Water Pokemon x0.5 (Swift Swim and Steelworker swimmers are exempt).",
                     "Anchor Shot x2; Dive, Water Pulse, Whirlpool, Jet Punch x1.5; Octazooka x1.3 (its ink always clouds); Crabhammer, Liquidation x1.2. Whirlpool may spin the target into confusion.",
                     "Fire moves fizzle. Fly, Bounce, Sky Drop and every entry hazard fail. Nothing can be burned; burns wash away on entry.",
                     "Non-Water Pokemon move at half Speed. Torrent, Swift Swim (x2 Speed) and Hydration act as if it were raining.",
                     "No weather or terrain reaches the depths. Water Absorb and Dry Skin drink in the sea (1/16 HP).",
                     "Dive, Bounce, Fly or Sky Drop -> back to the Water Surface (surfacing is not a transform strike). 2 Sludge Waves -> Corrosive Mire.",
                     "Elemental Seed: +1 Speed and Aqua Ring, and the holder adapts to the deep (becomes pure Water type)."],
  :nature_power  => :WATERPULSE,
  :camouflage    => :WATER,
  :secret_power  => 5,
  :activate_abilities => [:TORRENT, :SWIFTSWIM, :HYDRATION],
  :type_mods     => { :WATER => 1.5, :ELECTRIC => 1.5, :FLYING => 0.5 },
  :type_messages => { :WATER    => "{1} surged through the deep!",
                      :ELECTRIC => "The current crackled through the whole sea!",
                      :FLYING   => "There's no air to catch beneath the waves..." },
  :move_mods     => { :ANCHORSHOT => 2.0, :DIVE => 1.5, :WATERPULSE => 1.5, :WHIRLPOOL => 1.5, :JETPUNCH => 1.5,
                      :OCTAZOOKA => 1.3, :CRABHAMMER => 1.2, :LIQUIDATION => 1.2 },
  :move_messages => { :ANCHORSHOT => "The anchor plunged through the depths!",
                      :JETPUNCH   => "{1} jetted through the water!",
                      :WATERPULSE => "The pulse rippled out through the deep!",
                      :OCTAZOOKA  => "A cloud of ink billowed through the water!" },
  :damage_mods   => [
    { :category => :physical, :not_types => [:WATER],
      :user => { :not_types => [:WATER], :not_abilities => [:SWIFTSWIM, :STEELWORKER] },
      :mult => 0.5, :message => "The water slowed {1}'s strike..." },
    { :flags => ["Sound"], :category => :damaging, :mult => 1.3, :message => "{2} carried for miles through the water!" }
  ],
  :extra_types   => [
    { :types => [:GROUND], :category => :damaging, :add => :WATER, :message => "Silt from the seabed churned into the attack!" }
  ],
  :accuracy_mods => [
    { :types => [:ELECTRIC], :category => :damaging, :always_hit => true },
    { :moves => [:WHIRLPOOL], :mult => 1.25 }
  ],
  :effect_chance_mods => [{ :moves => [:OCTAZOOKA], :set => 100 }],
  :added_effects => [
    { :moves => [:WHIRLPOOL], :chance => 30, :confuse => true, :message => "The maelstrom spun {1} around and around!" }
  ],
  :move_fails    => [
    { :types => [:FIRE], :message => "{2} fizzled out in the deep water!" },
    { :moves => [:SKYDROP, :SPIKES, :TOXICSPIKES, :STEALTHROCK, :STICKYWEB],
      :message => "{2} is impossible underwater!" }
  ],
  :speed_mods    => [
    { :battlers => { :not_types => [:WATER], :not_abilities => [:SWIFTSWIM] }, :mult => 0.5 }
  ],
  :status_immunity => [
    { :status => [:BURN], :message => "The water douses the flames before they can catch on {1}!" }
  ],
  :on_entry      => [
    { :battlers => { :status => [:BURN] }, :cure_status => true, :also_on_change => true,
      :message => "The water washed away {1}'s burn!" }
  ],
  :end_of_round  => [
    { :battlers => { :abilities => [:WATERABSORB, :DRYSKIN] }, :heal => 1/16r, :message => "{1} drank in the sea." }
  ],
  :weather       => { :block => [:Sun, :Rain, :Sandstorm, :Hail, :HarshSun, :HeavyRain, :StrongWinds],
                      :block_message => "The weather can't reach the depths!" },
  :terrain       => { :block => [:Electric, :Grassy, :Misty, :Psychic],
                      :block_message => "Nothing can settle on the shifting sea floor!" },
  :transitions   => [
    # Surfacing is not a transform strike (:boost => false): only diving down is (103_Field_WaterSurface.rb), so Dive
    # can't be looped for x1.3 both ways. Dive surfaces on the turn it strikes (Reborn): one Dive, one change.
    { :moves => [:DIVE], :even_if_failed => true, :strike_turn => true, :boost => false, :to => :WATER_SURFACE,
      :message => "The battle burst back up to the surface!" },
    { :moves => [:BOUNCE, :FLY, :SKYDROP], :even_if_failed => true, :boost => false, :to => :WATER_SURFACE,
      :message => "The battle burst back up to the surface!" },
    { :moves => [:SLUDGEWAVE], :to => :CORROSIVE_MIRE, :uses => 2,
      :progress_message => "A toxic cloud is spreading through the water... ({1} more)",
      :message => "The water turned black with toxins! The battle surfaced into a bubbling mire!" }
  ],
  :seed => { :item => :ELEMENTALSEED, :stats => { :SPEED => 1 }, :effects => [:aqua_ring],
             :message => "{1}'s {2} released a shimmering bubble of air around it!",
             :proc => proc { |battle, battler|
               next false if !battler.canChangeType? || battler.pbTypes == [:WATER]
               battler.pbChangeTypes(:WATER)
               battle.pbDisplay(FieldEffects.format("{1} adapted to the deep and became Water type!", battler.pbThis))
               true
             } }
})
