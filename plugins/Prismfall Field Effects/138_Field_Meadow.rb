#===============================================================================
# MEADOW - (new, Revision 10) Elowen's open countryside: coastal heath, orchard
# rows, river meadows, hedgerows. Tall grass ripples in the breeze; grazers
# stampede, bugs and birds work the wildflowers, the wind carries seed and
# petal, blades send clippings flying. Fire spreads fast through dry grass
# (WILDFIRE); tending it makes it bloom into a FLOWER_GARDEN.
# Family: Telluric.
#===============================================================================
FieldEffects.register(:MEADOW, (lambda do
  breezes  = [:GUST, :TWISTER, :AIRCUTTER, :HURRICANE, :RAZORWIND, :ICYWIND, :BLEAKWINDSTORM, :SPRINGTIDESTORM,
              :PETALBLIZZARD, :LEAFTORNADO]
  carried  = { :FAIRYWIND => 1.5, :SILVERWIND => 1.5, :MAGICALLEAF => 1.5, :RAZORLEAF => 1.5, :POLLENPUFF => 1.5,
               :LEAFAGE => 1.5, :CUT => 2.0 }
  stampede = [:STOMP, :TAKEDOWN, :DOUBLEEDGE, :BODYSLAM, :HEADBUTT, :HORNATTACK, :WILDCHARGE, :HEADCHARGE,
              :RAGINGBULL, :HIGHHORSEPOWER, :STOMPINGTANTRUM]
  foragers = [:BUGBITE, :POUNCE, :LUNGE, :STRUGGLEBUG, :PLUCK]
  clippers = [:CUT, :SLASH, :AIRSLASH, :AIRCUTTER, :FURYCUTTER, :PSYCHOCUT, :XSCISSOR]
  tending  = [:GROWTH, :ROTOTILLER, :FLOWERSHIELD, :FLORALHEALING, :AROMATHERAPY, :GRASSPLEDGE, :INGRAIN]
  {
    :name          => "Meadow",
    :backdrop      => "field_meadow",
    :family        => :telluric,
    :intro_message => "Tall grass ripples in the breeze across the meadow.",
    :description   => "Elowen's open countryside: grazers stampede, bugs and birds work the wildflowers, the breeze carries seed and petal, and the tall grass hides whoever lives in it. Fire races through it; tending makes it bloom.",
    :notes         => ["Grass x1.2 and Bug x1.2. Grass Pelt and Leaf Guard are always active (the tall grass).",
                       "Grounded Grass and Bug Pokemon melt into the tall grass (x1.1 evasion).",
                       "The breeze carries them: Fairy Wind, Silver Wind, Magical Leaf, Razor Leaf, Leafage, Pollen Puff x1.5; wind moves x1.2. Cut x2 (and blades send grass clippings flying: Cut, Slash, Air Slash, Air Cutter, Fury Cutter, Psycho Cut, X-Scissor also hit as Grass).",
                       "Stampede: Stomp, Take Down, Double-Edge, Body Slam, Headbutt, Horn Attack, Wild Charge, Head Charge, Raging Bull, High Horsepower, Stomping Tantrum x1.2. Foragers: Bug Bite, Pounce, Lunge, Struggle Bug, Pluck x1.3.",
                       "Powder moves x1.25 accuracy; Grass Whistle x1.3. Sweet Scent lowers evasion one stage more.",
                       "On entry: Run Away +1 Speed (it darts into the grass), Sap Sipper +1 Attack. Sap Sipper grazes each turn (1/16 HP).",
                       "Sun lasts 2 turns longer; Grassy Terrain 3 turns longer.",
                       "2 damaging Fire moves (1 in sunlight) set the dry grass alight -> Wildfire. Grassy Terrain, or 2 tending moves (Growth, Rototiller, Flower Shield, Floral Healing, Aromatherapy, Grass Pledge, Ingrain) -> Flower Garden.",
                       "Telluric Seed: +1 evasion (it vanishes into the tall grass) and Ingrain."],
    :nature_power  => :ENERGYBALL,
    :camouflage    => :GRASS,
    :secret_power  => 2,
    :activate_abilities => [:GRASSPELT, :LEAFGUARD],
    :type_mods     => { :GRASS => 1.2, :BUG => 1.2 },
    :type_messages => { :GRASS => "The whole meadow swayed with {2}!",
                        :BUG   => "{1} hummed out of the tall grass!" },
    :move_mods     => carried.merge(foragers.map { |m| [m, 1.3] }.to_h),
    :move_messages => { :FAIRYWIND  => "The breeze swept seeds and petals into the attack!",
                        :SILVERWIND => "The breeze swept seeds and petals into the attack!",
                        :RAZORLEAF  => "The breeze sent the leaves spinning!",
                        :CUT        => "{1} mowed a path through the tall grass!",
                        :POUNCE     => "{1} sprang out of the tall grass!" },
    :extra_types   => [
      { :moves => clippers, :category => :damaging, :add => :GRASS, :message => "{2} sent grass clippings flying!" }
    ],
    :damage_mods   => [
      { :moves => breezes, :category => :damaging, :mult => 1.2, :message => "The breeze swept across the meadow behind {2}!" },
      { :moves => stampede, :mult => 1.2, :message => "{1} stampeded through the tall grass!" }
    ],
    :accuracy_mods => [
      { :flags => ["Powder"], :mult => 1.25 },
      { :moves => [:GRASSWHISTLE], :mult => 1.3 },
      { :target => { :types => [:GRASS, :BUG], :grounded => true }, :evasion_mult => 1.1 }
    ],
    :move_stat_boosts => [
      { :moves => [:SWEETSCENT], :target_stats => { :EVASION => -1 }, :message => "The meadow's flowers sweetened the scent!" }
    ],
    :on_entry      => [
      { :battlers => { :abilities => [:RUNAWAY] }, :stats => { :SPEED => 1 }, :message => "{1} darted into the tall grass!" },
      { :battlers => { :abilities => [:SAPSIPPER] }, :stats => { :ATTACK => 1 }, :message => "{1} munched on the meadow grass!" }
    ],
    :end_of_round  => [
      { :battlers => { :abilities => [:SAPSIPPER] }, :heal => 1/16r, :message => "{1} grazed on the meadow." }
    ],
    :weather       => { :extend => { :Sun => 2 } },
    :terrain       => { :extend => { :Grassy => 3 } },
    :transitions   => [
      { :types => [:FIRE], :category => :damaging, :to => :WILDFIRE, :uses => 2,
        :condition => proc { |battle, user, target, move, type| ![:Sun, :HarshSun].include?(battle.pbWeather) },
        :progress_message => "Sparks are catching in the dry grass... ({1} more)",
        :message => "The dry grass went up in flames! The meadow is ablaze!" },
      { :types => [:FIRE], :category => :damaging, :in_weather => [:Sun, :HarshSun], :to => :WILDFIRE,
        :message => "The sun-baked grass went up in a flash! The meadow is ablaze!" },
      { :terrain => [:Grassy], :to => :FLOWER_GARDEN, :message => "Wildflowers burst open everywhere! The meadow became a garden!" },
      { :moves => tending, :to => :FLOWER_GARDEN, :uses => 2, :even_if_failed => true,
        :progress_message => "Buds are opening all across the meadow... ({1} more)",
        :message => "Wildflowers burst open everywhere! The meadow became a garden!" }
    ],
    :seed => { :item => :TELLURICSEED, :stats => { :EVASION => 1 }, :effects => [:ingrain],
               :message => "{1}'s {2} let it vanish into the tall grass!" }
  }
end).call)
