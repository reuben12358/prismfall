#===============================================================================
# NEON_GRID - Gym 4 (Electric), Lumen City in Zenith. A humming arena of live
# circuitry (Reborn's Electric Terrain + Factory logic). Electric Pokemon draw
# straight from the grid; water and steel conduct; the hum keeps everyone awake.
# Quakes, mud or floods short it into stage 2 "Blackout" (Reborn's Short-
# Circuit): the lights die, current surges in a fixed, learnable pattern and
# shadows rule. Charging moves reboot it. Family: Synthetic.
#===============================================================================
FieldEffects.register(:NEON_GRID, (lambda do
  quakes  = [:EARTHQUAKE, :MAGNITUDE, :BULLDOZE, :FISSURE, :PRECIPICEBLADES, :THOUSANDWAVES, :HEADLONGRUSH]
  floods  = [:SURF, :MUDDYWATER, :HYDROPUMP, :WATERSPOUT, :WAVECRASH]
  chargers = [:CHARGE, :DISCHARGE, :PARABOLICCHARGE, :WILDCHARGE, :CHARGEBEAM, :ELECTRICTERRAIN, :IONDELUGE,
              :OVERDRIVE, :RISINGVOLTAGE, :THUNDER, :SUPERCELLSLAM, :ZAPCANNON]
  lights  = [:DAZZLINGGLEAM, :FLASHCANNON, :LIGHTOFRUIN, :PRISMATICLASER, :PHOTONGEYSER, :LUSTERPURGE,
             :MIRRORSHOT, :SIGNALBEAM, :TECHNOBLAST, :LUMINACRASH, :AURORABEAM]
  conductors = { :moves => [:GEARGRIND, :MAGNETBOMB, :GYROBALL, :FLASHCANNON, :STEELBEAM, :SURF, :MUDDYWATER],
                 :add => :ELECTRIC, :message => "The current ran straight through {2}!" }
  # Blackout surge pattern (Reborn Short-Circuit): same cycle every battle, so it can be read and played.
  surges  = [[0.5, "The dead grid swallowed most of the current..."], [1.5, "Stray current surged into the attack!"],
             [0.8, "The circuits sputtered..."], [2.0, "BZZT! A massive overload!"], [1.2, "The cables crackled with power!"]]
  surge_hook = proc { |battle, user, target, move, type, mults, ai|
    next if type != :ELECTRIC || !move.damagingMove?
    st = FieldEffects.state(battle)
    idx = st[:surge] || 0
    mult, msg = surges[idx % surges.length]
    mults[:power_multiplier] *= mult
    next if ai
    if st[:surge_use] != battle.fe_state[:use_id]   # advance once per move use (not per target)
      st[:surge_use] = battle.fe_state[:use_id]
      st[:surge_next] = idx + 1
      FieldEffects.show_once(battle, user, move, msg)
    end
  }
  surge_advance = proc { |battle, user, targets, move, num_hits|
    st = FieldEffects.state(battle)
    st[:surge] = st.delete(:surge_next) if st[:surge_next]
  }
  {
    # ---- Stage 1: the live grid -------------------------------------------------
    :name          => "Neon Grid",
    :backdrop      => "field_neon_grid",
    :family        => :synthetic,
    :intro_message => "Neon circuitry hums beneath your feet!",
    :description   => "Electric Pokemon draw power from live circuitry; water and steel conduct; nobody can doze off. Quakes, mud or floods black it out.",
    :notes         => ["Electric x1.5, Steel x1.2. Neon light moves (Dazzling Gleam, Flash Cannon, Luster Purge...) x1.3.",
                       "Conductors: Gear Grind, Magnet Bomb, Gyro Ball, Flash Cannon, Steel Beam, Surf and Muddy Water also hit as Electric.",
                       "Rising Voltage, Magnet Bomb x1.5; Discharge, Parabolic Charge, Zing Zap, Plasma Fists, Electro Drift, Overdrive x1.3.",
                       "Damaging Water moves carry the grid's current (30% paralysis). Zap Cannon has 80% accuracy; Thunder x1.2.",
                       "Grounded Pokemon can't fall asleep. Surge Surfer is always active. Magnet Rise lasts 3 turns longer.",
                       "Charge also +1 Sp. Atk; Magnet Rise +1 Speed; Eerie Impulse lowers Sp. Atk one stage more.",
                       "Plus / Minus +1 Sp. Atk on entry; Motor Drive, Lightning Rod, Volt Absorb, Electromorphosis start charged. Each turn Motor Drive gains Speed and Volt Absorb heals.",
                       "Electric Terrain lasts 3 turns longer.",
                       "Blackout: 2 quakes, 2 floods (Surf, Muddy Water, Hydro Pump...) or Mud Sport short the grid -> stage 2.",
                       "Blackout: Electric damage surges in a fixed cycle (x0.5, x1.5, x0.8, x2, x1.2, repeat). Dark x1.3, Ghost x1.2; light moves x1.5 and Flash blinds more. 2 charging moves (or Electric Terrain) reboot the grid.",
                       "Synthetic Seed: +1 Sp. Atk and Magnet Rise (it floats above the live grid)."],
    :nature_power  => :DISCHARGE,
    :camouflage    => :ELECTRIC,
    :secret_power  => 1,
    :activate_abilities => [:SURGESURFER],
    :type_mods     => { :ELECTRIC => 1.5, :STEEL => 1.2 },
    :type_messages => { :ELECTRIC => "{1} drew power straight from the grid!" },
    :move_mods     => { :RISINGVOLTAGE => 1.5, :MAGNETBOMB => 1.5, :DISCHARGE => 1.3, :PARABOLICCHARGE => 1.3,
                        :ZINGZAP => 1.3, :PLASMAFISTS => 1.3, :ELECTRODRIFT => 1.3, :OVERDRIVE => 1.3 },
    :move_messages => { :RISINGVOLTAGE => "The whole grid rose to meet {1}!",
                        :OVERDRIVE     => "The arena speakers boomed with {1}'s riff!",
                        :MAGNETBOMB    => "The grid's magnetism guided the bomb home!" },
    :damage_mods   => [
      { :moves => lights, :mult => 1.3, :message => "The neon light intensified {2}!" }
    ],
    :extra_types   => [conductors],
    :accuracy_mods => [{ :moves => [:ZAPCANNON], :set => 80 }, { :moves => [:THUNDER], :mult => 1.2 }],
    :added_effects => [
      { :types => [:WATER], :category => :damaging, :chance => 30, :status => :PARALYSIS,
        :message => "The water carried the grid's current into {1}!" }
    ],
    :move_stat_boosts => [
      { :moves => [:CHARGE], :user_stats => { :SPECIAL_ATTACK => 1 }, :message => "The grid overcharged {1}!" },
      { :moves => [:MAGNETRISE], :user_stats => { :SPEED => 1 }, :message => "{1} rode the magnetic field!" },
      { :moves => [:EERIEIMPULSE], :target_stats => { :SPECIAL_ATTACK => -1 } }
    ],
    :status_immunity => [
      { :status => [:SLEEP], :battlers => { :grounded => true }, :message => "The humming grid keeps {1} wide awake!" }
    ],
    :effect_durations => { :MAGNETRISE => [3, "The grid's magnetism will hold {1} aloft for longer!"] },
    :on_entry      => [
      { :battlers => { :abilities => [:PLUS, :MINUS] }, :stats => { :SPECIAL_ATTACK => 1 },
        :message => "{1} synced with the grid!" },
      { :battlers => { :abilities => [:MOTORDRIVE, :LIGHTNINGROD, :VOLTABSORB, :ELECTROMORPHOSIS] },
        :effects => [:charge], :message => "{1} soaked up current from the grid!" }
    ],
    :end_of_round  => [
      { :battlers => { :abilities => [:MOTORDRIVE], :grounded => true }, :stats => { :SPEED => 1 },
        :message => "{1} drew current from the grid!" },
      { :battlers => { :abilities => [:VOLTABSORB] }, :heal => 1/16r, :message => "{1} drew power from the grid." }
    ],
    :terrain       => { :extend => { :Electric => 3 } },
    :transitions   => [
      { :moves => quakes, :stage => 2, :uses => 2,
        :progress_message => "The grid flickers and sparks... ({1} more)",
        :message => "The grid shorted out! The neon lights died - only sparks light the dark!" },
      { :moves => floods, :stage => 2, :uses => 2,
        :progress_message => "Water is seeping into the circuits... ({1} more)",
        :message => "The flood shorted out the grid! Sparks crackle in the dark!" },
      { :moves => [:MUDSPORT], :stage => 2, :even_if_failed => true,
        :message => "Mud fouled the circuits! The grid went dark!" }
    ],
    :seed => { :item => :SYNTHETICSEED, :stats => { :SPECIAL_ATTACK => 1 }, :effects => [:magnet_rise],
               :message => "{1}'s {2} magnetized it above the grid!" },
    :stages => {
      # ---- Stage 2: Blackout (short-circuit) --------------------------------------
      2 => {
        :backdrop      => "field_neon_grid_blackout",
        :intro_message => "The grid is dark! Live sparks crackle across the floor...",
        :description   => "Blackout: Electric damage surges in a fixed cycle, shadows grow strong and light dazzles. Charge it back up to reboot.",
        :type_mods     => { :DARK => 1.3, :GHOST => 1.2 },
        :type_messages => { :DARK => "{1} struck from the dark between the sparks!",
                            :GHOST => "{1} flickered through the dead circuitry!" },
        :move_mods     => {},
        :move_messages => {},
        :damage_mods   => [
          { :moves => lights, :mult => 1.5, :message => "Blinding! {2} lit up the whole dead grid!" }
        ],
        :accuracy_mods => [{ :moves => [:ZAPCANNON], :set => 80 }],
        :added_effects => [],
        :move_stat_boosts => [
          { :moves => [:FLASH], :target_stats => { :ACCURACY => -1 }, :message => "The flash was blinding in the dark!" }
        ],
        :status_immunity => [],
        :end_of_round  => [
          { :battlers => { :abilities => [:VOLTABSORB] }, :heal => 1/16r, :message => "{1} drew on the crackling cables." }
        ],
        :hooks         => { :damage => surge_hook, :after_move => surge_advance },
        :transitions   => [
          { :moves => chargers, :stage => 1, :uses => 2, :even_if_failed => true,
            :progress_message => "The grid flickers with returning power... ({1} more)",
            :message => "Power restored! The Neon Grid hums back to life!" },
          { :terrain => [:Electric], :stage => 1, :message => "The electrified terrain rebooted the grid!" }
        ]
      }
    }
  }
end).call)
