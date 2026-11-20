#===============================================================================
# DESERT - Gym 5 (Ground), Duneholt in Ossaria, the Bone Sands. Endless dunes,
# buried bones and a white sun. Sand-dwellers own the place: sand abilities
# work without a sandstorm and Ground types hide in the dunes.
# Rain (or 3 floods) wakes the seeds sleeping in the sand: stage 2 "Superbloom".
# A sea-storm (heavy rain) or Origin Pulse drags the sea in over the dunes
# (FLOODED_DUNES); the bloom drowns the same way, or under 3 more floods.
# Searing heat fuses the dunes into glass (GLASS_DUNES, the steam-glass of
# the Ch19 war). Family: Telluric.
#===============================================================================
FieldEffects.register(:DESERT, (lambda do
  floods   = [:SURF, :MUDDYWATER, :WATERSPOUT, :HYDROPUMP, :WATERPLEDGE, :WAVECRASH]
  searing  = [:ERUPTION, :BLASTBURN, :FUSIONFLARE, :BLUEFLARE, :MAGMASTORM, :BURNUP, :OVERHEAT, :ARMORCANNON]
  bones    = { :BONECLUB => 1.3, :BONEMERANG => 1.3, :BONERUSH => 1.3, :SHADOWBONE => 1.3 }
  petals   = [:PETALDANCE, :PETALBLIZZARD, :POLLENPUFF, :FLOWERTRICK, :FLEURCANNON, :SEEDBOMB]
  {
    # ---- Stage 1: the dunes ---------------------------------------------------
    :name          => "Desert",
    :backdrop      => "field_desert",
    :family        => :telluric,
    :intro_message => "Heat shimmers over the endless dunes...",
    :description   => "Sand-dwellers own the dunes: sand abilities always work, Ground types hide in the sand, and the bones of Ossaria make weapons. Rain wakes a superbloom, a sea-storm floods the dunes, and searing heat makes glass.",
    :notes         => ["Ground x1.2, Fire x1.2. Ice x0.75 and Water x0.8 (the dunes drink them).",
                       "Sand Rush, Sand Force, Sand Veil and Solar Power work without weather (Solar Power costs no HP here).",
                       "Ground-type Pokemon burrow into the sand: special attacks against them deal x0.67.",
                       "Sand Tomb x2; Scorching Sands, Solar Beam, Solar Blade, Needle Arm, Dig x1.5; Sandsear Storm, Thousand Waves, Heat Wave, Pin Missile and bone moves x1.3.",
                       "Physical Ground moves may kick sand in the eyes (20%, accuracy -1). Sand Attack never misses and drops accuracy one stage more; Shore Up also gives +1 Def.",
                       "Earth Eater draws on the dunes (1/16 HP a turn). Dry Skin dries out in the heat (1/8).",
                       "Hail can't form; Sandstorm +3 turns, Sun +2. Grassy Terrain can't take root.",
                       "Rain, or 3 floods (Surf, Muddy Water, Hydro Pump...) -> Superbloom (stage 2). Heavy rain or Origin Pulse drags the sea in -> Flooded Dunes. 2 searing moves (Eruption, Blast Burn, Fusion Flare, Blue Flare...) -> Glass Dunes.",
                       "Superbloom: Grass x1.5, Bug x1.2, petal and seed moves x1.5, Chlorophyll and Leaf Guard active, Grass types drink 1/16 HP a turn. Sun, sandstorm or 2 fire attacks bake it back to dunes; heavy rain, Origin Pulse or 3 more floods drown it -> Flooded Dunes.",
                       "Telluric Seed: +1 Defense, +1 Sp. Def, but it's half-buried (-1 Speed)."],
    :nature_power  => :SANDTOMB,
    :camouflage    => :GROUND,
    :secret_power  => 8,
    :activate_abilities => [:SANDRUSH, :SANDFORCE, :SANDVEIL, :SOLARPOWER],
    :type_mods     => { :GROUND => 1.2, :FIRE => 1.2, :ICE => 0.75, :WATER => 0.8 },
    :type_messages => { :GROUND => "The dunes shifted under {1}'s command!",
                        :ICE    => "The desert heat blunted the cold...",
                        :WATER  => "The thirsty dunes drank up some of the water..." },
    :move_mods     => { :SANDTOMB => 2.0, :SCORCHINGSANDS => 1.5, :SOLARBEAM => 1.5, :SOLARBLADE => 1.5,
                        :NEEDLEARM => 1.5, :DIG => 1.5, :SANDSEARSTORM => 1.3, :THOUSANDWAVES => 1.3,
                        :HEATWAVE => 1.3, :PINMISSILE => 1.3 }.merge(bones),
    :move_messages => { :SANDTOMB   => "The dunes swallowed the foe whole!",
                        :SOLARBEAM  => "{1} drank in the desert sun!",
                        :SOLARBLADE => "{1} drank in the desert sun!",
                        :DIG        => "{1} swam through the soft sand!",
                        :BONERUSH   => "{1} wielded the bones of the Bone Sands!",
                        :BONEMERANG => "{1} wielded the bones of the Bone Sands!",
                        :BONECLUB   => "{1} wielded the bones of the Bone Sands!",
                        :SHADOWBONE => "{1} wielded the bones of the Bone Sands!" },
    :damage_mods   => [
      { :category => :special, :target => { :types => [:GROUND] }, :defense_mult => 1.5 }
    ],
    :accuracy_mods => [
      { :moves => [:SANDATTACK], :always_hit => true },
      { :moves => [:SANDTOMB], :mult => 1.25 }
    ],
    :added_effects => [
      { :types => [:GROUND], :category => :physical, :chance => 20, :stats => { :ACCURACY => -1 },
        :message => "{1} got a faceful of sand!" }
    ],
    :move_stat_boosts => [
      { :moves => [:SANDATTACK], :target_stats => { :ACCURACY => -1 }, :message => "The desert wind whipped up the sand!" },
      { :moves => [:SHOREUP], :user_stats => { :DEFENSE => 1 }, :message => "{1} packed the sand tight!" }
    ],
    :end_of_round  => [
      { :battlers => { :abilities => [:EARTHEATER] }, :heal => 1/16r, :message => "{1} ate into the dunes." },
      { :battlers => { :abilities => [:DRYSKIN] }, :damage => 1/8r, :message => "{1}'s skin dried out in the desert heat." }
    ],
    :weather       => { :block => [:Hail], :block_message => "The desert heat melted the hail before it fell!",
                        :extend => { :Sandstorm => 3, :Sun => 2 } },
    :terrain       => { :block => [:Grassy], :block_message => "Nothing can take root in the dry dunes!" },
    :transitions   => [
      { :weather => [:HeavyRain], :to => :FLOODED_DUNES,
        :message => "A sea-storm broke over the desert! The flood-sea is pouring in over the dunes!" },
      { :moves => [:ORIGINPULSE], :to => :FLOODED_DUNES,
        :message => "The sea answered the pulse and poured in over the dunes!" },
      { :weather => [:Rain], :stage => 2,
        :message => "Rain on the dunes! Seeds sleeping in the sand burst into a superbloom!" },
      { :moves => floods, :stage => 2, :uses => 3,
        :progress_message => "The sand darkens with water... ({1} more)",
        :message => "The soaked dunes burst into a superbloom!" },
      { :moves => searing, :to => :GLASS_DUNES, :uses => 2,
        :progress_message => "The sand is starting to glaze over in the heat... ({1} more)",
        :message => "The heat fused the dunes into glass!" }
    ],
    :seed => { :item => :TELLURICSEED, :stats => { :DEFENSE => 1, :SPECIAL_DEFENSE => 1, :SPEED => -1 },
               :message => "{1}'s {2} half-buried it in hardened sand!" },
    :stages => {
      # ---- Stage 2: Superbloom ----------------------------------------------------
      2 => {
        :backdrop      => "field_desert_bloom",
        :intro_message => "The desert is in bloom!",
        :description   => "Superbloom: water woke the seeds in the sand. Grass, Bug and petal moves surge while it lasts.",
        :activate_abilities => [:CHLOROPHYLL, :LEAFGUARD, :SANDFORCE],
        :type_mods     => { :GRASS => 1.5, :BUG => 1.2, :GROUND => 1.2 },
        :type_messages => { :GRASS => "The blooming desert poured life into {2}!" },
        :move_mods     => petals.map { |m| [m, 1.5] }.to_h.merge(bones),
        :move_messages => { :PETALDANCE => "Petals swirled up from the blooming dunes!",
                            :POLLENPUFF => "The superbloom's pollen thickened the puff!" },
        :damage_mods   => [],
        :accuracy_mods => [{ :flags => ["Powder"], :mult => 1.2 }],
        :added_effects => [],
        :end_of_round  => [
          { :battlers => { :types => [:GRASS] }, :heal => 1/16r, :message => "{1} drank from the rain-soaked sand." },
          { :battlers => { :abilities => [:EARTHEATER] }, :heal => 1/16r, :message => "{1} ate into the dunes." }
        ],
        :weather       => { :block => [:Hail], :block_message => "The desert heat melted the hail before it fell!",
                            :extend => { :Rain => 2 } },
        :terrain       => { :extend => { :Grassy => 3 } },
        :transitions   => [
          { :weather => [:HeavyRain], :to => :FLOODED_DUNES,
            :message => "A sea-storm broke over the bloom! The flood-sea is pouring in over the dunes!" },
          { :moves => [:ORIGINPULSE], :to => :FLOODED_DUNES,
            :message => "The sea answered the pulse and poured in over the blooming dunes!" },
          { :moves => floods, :to => :FLOODED_DUNES, :uses => 3,
            :progress_message => "The water is rising through the bloom... ({1} more)",
            :message => "The water kept rising until the sea came in over the dunes!" },
          { :weather => [:Sun, :HarshSun, :Sandstorm], :stage => 1,
            :message => "The bloom withered back into the sand. The dunes return." },
          { :types => [:FIRE], :category => :damaging, :stage => 1, :uses => 2,
            :progress_message => "The blossoms are curling in the heat... ({1} more)",
            :message => "The heat baked the bloom away. The dunes return." }
        ]
      }
    }
  }
end).call)
