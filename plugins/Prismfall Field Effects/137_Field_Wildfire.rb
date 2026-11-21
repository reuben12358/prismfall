#===============================================================================
# WILDFIRE - (new, Revision 10) What woods, meadows and gardens become when
# they catch fire (SILKWOOD, MEADOW, FLOWER_GARDEN stage 5). Reborn's Burning
# Field, told from the fire-users' side: fire Pokemon draw the blaze into their
# attacks, winds fan it, every fire attack can spread it around the foes.
#   Stage 1 Wildfire: it burns down to embers after 4 rounds unless fire
#                     attacks keep feeding it; water, rain or sand put it
#                     out sooner (wind only fans it).
#   Stage 2 Embers:   smouldering coals and fertile ash - fire still flares,
#                     ghosts thicken in the smoke, pioneer plants take root.
#                     Big fire or sun re-ignite it; rain, Grassy Terrain or
#                     growth bring the land back (MEADOW).
# Family: Elemental.
#===============================================================================
FieldEffects.register(:WILDFIRE, (lambda do
  winds   = [:GUST, :TWISTER, :AIRCUTTER, :HURRICANE, :RAZORWIND, :HEATWAVE, :BLEAKWINDSTORM, :AIRSLASH]
  douse   = [:SURF, :MUDDYWATER, :HYDROPUMP, :WATERSPOUT, :WATERPLEDGE, :SPARKLINGARIA, :WAVECRASH, :SANDTOMB,
             :WATERSPORT, :MUDSPORT]
  big_fire = [:ERUPTION, :LAVAPLUME, :HEATWAVE, :FIREBLAST, :INFERNO, :OVERHEAT, :BLASTBURN, :FIREPLEDGE,
              :FLAREBLITZ, :BURNUP, :MAGMASTORM, :FUSIONFLARE, :BLUEFLARE]
  regrow  = [:GROWTH, :INGRAIN, :GRASSPLEDGE, :FLORALHEALING, :ROTOTILLER, :LEECHSEED]
  spread = proc { |battle, user, targets, move, num_hits|
    next if user.lastMoveFailed || !move.damagingMove? || move.calcType != :FIRE
    st = FieldEffects.state(battle)
    if (st[:fuel] || 4) < 5
      st[:fuel] = [(st[:fuel] || 4) + 1, 5].min
      battle.pbDisplay(FieldEffects.format("The flames roared higher!")) if st[:fuel] >= 4
    end
    side = user.pbOpposingSide
    next if side.effects[PBEffects::SeaOfFire] > 0 || battle.pbRandom(100) >= 30
    side.effects[PBEffects::SeaOfFire] = 3
    battle.pbDisplay(FieldEffects.format("{1} spread the wildfire all around its foes!", user.pbThis))
  }
  burn_down = proc { |battle|
    st = FieldEffects.state(battle)
    st[:fuel] = (st[:fuel] || 4) - 1
    battle.pbDisplay(FieldEffects.format("The wildfire is starting to burn itself out...")) if st[:fuel] == 1
  }
  {
    # ---- Stage 1: Wildfire -------------------------------------------------------
    :name          => "Wildfire",
    :backdrop      => "field_wildfire",
    :family        => :elemental,
    :intro_message => "The battlefield is ablaze! Flames leap from tree to tree!",
    :description   => "Fire Pokemon draw the blaze into their attacks, winds fan it and every fire attack can spread it around the foes. It burns down to embers unless it's fed.",
    :notes         => ["Wildfire (stage 1): Fire x1.5; Blaze and Flare Boost always active; Flash Fire starts lit. Ice x0.5; Grass moves x0.5 against grounded targets.",
                       "Damaging wind moves fan the flames (also Fire, x1.2). Smog, Clear Smog x1.5 (also Fire); Smack Down, Thousand Arrows x2 (into the burning undergrowth, also Fire); Flame Charge, Fire Spin x1.5.",
                       "Spreading: a damaging Fire attack may spread the fire around the user's foes (30%: a 3-turn sea of fire on their side).",
                       "Will-O-Wisp never misses; Smokescreen drops accuracy one stage more. Nothing can be frozen.",
                       "Fuel: it burns down to Embers after 4 rounds; each damaging Fire attack feeds it a round (max 5).",
                       "Put out sooner: 2 douses (Surf, Muddy Water, Hydro Pump, Water Spout, Sand Tomb, Water/Mud Sport...), rain or a sandstorm -> Embers. Wind fans it, it never blows it out.",
                       "Embers (stage 2): Fire, Ground, Grass and Ghost x1.2 (coals, ash, pioneer shoots, smoke wraiths); Flare Boost active; wind moves whirl ash (30% accuracy -1); Grass types take root in the fertile ash (1/16 HP a turn); Growth also +1 Sp. Atk.",
                       "Embers: 2 big fire moves or sunlight -> Wildfire again. Rain, Grassy Terrain, or 2 growing moves (Growth, Ingrain, Grass Pledge, Rototiller...) -> Meadow (life returns).",
                       "Elemental Seed: +1 Attack, +1 Sp. Atk and Flash Fire, but the holder is burned."],
    :nature_power  => :FLAMETHROWER,
    :camouflage    => :FIRE,
    :secret_power  => 10,
    :activate_abilities => [:BLAZE, :FLAREBOOST],
    :type_mods     => { :FIRE => 1.5, :ICE => 0.5 },
    :type_messages => { :FIRE => "{1} drew the wildfire into its attack!",
                        :ICE  => "The ice melted in the blaze..." },
    :move_mods     => { :SMOG => 1.5, :CLEARSMOG => 1.5, :SMACKDOWN => 2.0, :THOUSANDARROWS => 2.0,
                        :FLAMECHARGE => 1.5, :FIRESPIN => 1.5 },
    :move_messages => { :FLAMECHARGE => "{1} charged straight through the flames!",
                        :SMACKDOWN   => "The foe was slammed into the burning undergrowth!",
                        :FIRESPIN    => "The whole blaze spun up around the foe!" },
    :extra_types   => [
      { :moves => winds + [:SMOG, :CLEARSMOG, :SMACKDOWN, :THOUSANDARROWS], :category => :damaging, :add => :FIRE,
        :message => "The attack carried a wall of flame with it!" }
    ],
    :damage_mods   => [
      { :moves => winds, :category => :damaging, :mult => 1.2, :message => "The wind fanned the wildfire!" },
      { :types => [:GRASS], :category => :damaging, :target => { :grounded => true }, :mult => 0.5,
        :message => "The flames consumed {2} before it could land..." }
    ],
    :accuracy_mods => [{ :moves => [:WILLOWISP], :always_hit => true }],
    :move_stat_boosts => [
      { :moves => [:SMOKESCREEN], :target_stats => { :ACCURACY => -1 }, :message => "The smoke of the wildfire thickened!" }
    ],
    :status_immunity => [{ :status => [:FROZEN], :message => "Nothing can freeze in the middle of a wildfire!" }],
    :on_entry      => [
      { :battlers => { :abilities => [:FLASHFIRE] }, :effects => [:flash_fire], :also_on_change => true }
    ],
    :hooks         => {
      :on_start     => proc { |battle, old_id| FieldEffects.state(battle)[:fuel] = 4 },
      :after_move   => spread,
      :end_of_round => burn_down
    },
    :transitions   => [
      { :check => proc { |battle|
          st = FieldEffects.state(battle)
          next false if (st[:fuel] || 4) > 0
          st[:fuel] = 4   # fresh fuel for the next time the embers re-ignite
          true
        }, :stage => 2,
        :message => "The wildfire has burned itself down to glowing embers." },
      { :moves => douse, :stage => 2, :uses => 2, :even_if_failed => true,
        :progress_message => "Steam hisses as the flames die back... ({1} more)",
        :message => "The wildfire was beaten down to smouldering embers!" },
      { :weather => [:Rain, :HeavyRain, :Sandstorm], :stage => 2, :message => "The flames died down to glowing embers!" }
    ],
    :seed => { :item => :ELEMENTALSEED, :status => :BURN, :stats => { :ATTACK => 1, :SPECIAL_ATTACK => 1 },
               :effects => [:flash_fire], :message => "{1}'s {2} caught the blaze inside it!" },
    :stages => {
      # ---- Stage 2: Embers ---------------------------------------------------------
      2 => {
        :backdrop      => "field_wildfire_embers",
        :intro_message => "Embers glow beneath drifting ash...",
        :description   => "Embers: smouldering coals and fertile ash. Fire still flares, ghosts thicken in the smoke and pioneer plants take root. Fire can re-ignite it; rain and growth bring the land back.",
        :activate_abilities => [:FLAREBOOST],
        :type_mods     => { :FIRE => 1.2, :GROUND => 1.2, :GRASS => 1.2, :GHOST => 1.2 },
        :type_messages => { :FIRE  => "The embers flared up with {2}!",
                            :GRASS => "Pioneer shoots burst through the ash with {2}!",
                            :GHOST => "The ghosts thickened in the smoke around {1}!" },
        :move_mods     => { :SMOG => 1.5, :CLEARSMOG => 1.3, :OMINOUSWIND => 1.3 },
        :move_messages => { :SMOG => "The smouldering coals thickened the smog!" },
        :extra_types   => [],
        :damage_mods   => [],
        :added_effects => [
          { :moves => winds, :category => :damaging, :chance => 30, :stats => { :ACCURACY => -1 },
            :message => "Whirling ash got in {1}'s eyes!" }
        ],
        :move_stat_boosts => [
          { :moves => [:SMOKESCREEN], :target_stats => { :ACCURACY => -1 }, :message => "The smoke of the embers thickened!" },
          { :moves => [:GROWTH], :user_stats => { :SPECIAL_ATTACK => 1 }, :message => "{1} drew strength from the fertile ash!" }
        ],
        :status_immunity => [],
        :end_of_round  => [
          { :battlers => { :types => [:GRASS], :grounded => true }, :heal => 1/16r,
            :message => "{1} took root in the fertile ash." }
        ],
        :hooks         => {},
        :transitions   => [
          { :moves => big_fire, :stage => 1, :uses => 2,
            :progress_message => "The embers are glowing brighter... ({1} more)",
            :message => "The embers roared back into a blaze!" },
          { :weather => [:Sun, :HarshSun], :stage => 1, :message => "The sun dried the ash - and the embers roared back into a blaze!" },
          { :weather => [:Rain, :HeavyRain], :to => :MEADOW, :message => "Rain soaked the ash, and green shoots burst through! Life returns!" },
          { :terrain => [:Grassy], :to => :MEADOW, :message => "Grass rushed over the ash! Life returns!" },
          { :moves => regrow, :to => :MEADOW, :uses => 2, :even_if_failed => true,
            :progress_message => "Green shoots are pushing up through the ash... ({1} more)",
            :message => "The ash bloomed into a sea of new grass! Life returns!" }
        ]
      }
    }
  }
end).call)
