#===============================================================================
# FACTORY - Gym 15 (Steel), Cogsworth, the foundry district of Zenith, the City
# Above. Conveyor lines, crucibles of molten steel, giant gears and catwalks.
# Steel Pokemon mesh with the machinery, gears and hammers ring, the crucibles'
# heat softens rival plating. Wreck it (explosions, or quakes that bring the
# gantries down) -> SCRAPYARD. Family: Synthetic.
#===============================================================================
FieldEffects.register(:FACTORY, (lambda do
  hammers = [:HAMMERARM, :ICEHAMMER, :WOODHAMMER, :CRABHAMMER, :DRAGONHAMMER, :GIGATONHAMMER]
  quakes  = [:EARTHQUAKE, :MAGNITUDE, :BULLDOZE, :FISSURE, :HEADLONGRUSH, :PRECIPICEBLADES, :THOUSANDWAVES]
  {
    :name          => "Factory",
    :backdrop      => "field_factory",
    :family        => :synthetic,
    :intro_message => "Gears grind and molten steel pours... The foundry roars to life!",
    :description   => "Steel Pokemon mesh with the machinery: gears, hammers and rollers ring out, metal-tuning moves work better, the crucibles' heat softens rival plating. Explosions or quakes wreck it.",
    :notes         => ["Steel x1.5, Electric x1.2, Fire x1.2 (the crucibles). Steelworker and Steely Spirit users' Steel moves x1.2 more.",
                       "Gear Grind x2; Magnet Bomb, Steel Roller, Steamroller, Gyro Ball, Techno Blast x1.5; Double Iron Bash, Flash Cannon, Steam Eruption, Spin Out, Explosion, Self-Destruct, Misty Explosion x1.3; hammers (Hammer Arm, Ice/Wood/Crab/Dragon/Gigaton Hammer) x1.3.",
                       "Damaging Fire moves may soften a Steel target's plating (30%, Defense -1). Metal Sound and Screech never miss.",
                       "Shift Gear also +1 Defense; Autotomize, Iron Defense and Metal Sound work one stage better; Magnet Rise +1 Speed and lasts 3 turns longer.",
                       "On entry: Light Metal +1 Speed, Heavy Metal +1 Defense, Download +1 Speed (it syncs with the line).",
                       "Nothing can be frozen near the crucibles. Indoors: Rain, Sandstorm and Hail can't start. Sun +2 turns, Electric Terrain +2.",
                       "An explosion (Explosion, Self-Destruct, Misty Explosion, Mind Blown) wrecks it at once; 3 quakes bring the catwalks down. Either leaves a Scrapyard.",
                       "Synthetic Seed: +1 Attack and +1 Speed."],
    :nature_power  => :GEARGRIND,
    :camouflage    => :STEEL,
    :secret_power  => 14,
    :type_mods     => { :STEEL => 1.5, :ELECTRIC => 1.2, :FIRE => 1.2 },
    :type_messages => { :STEEL => "{1} meshed with the foundry's machinery!",
                        :FIRE  => "The crucibles flared white-hot!" },
    :move_mods     => { :GEARGRIND => 2.0, :MAGNETBOMB => 1.5, :STEELROLLER => 1.5, :STEAMROLLER => 1.5, :GYROBALL => 1.5,
                        :TECHNOBLAST => 1.5, :DOUBLEIRONBASH => 1.3, :FLASHCANNON => 1.3, :STEAMERUPTION => 1.3,
                        :SPINOUT => 1.3, :EXPLOSION => 1.3, :SELFDESTRUCT => 1.3, :MISTYEXPLOSION => 1.3 },
    :move_messages => { :GEARGRIND     => "The factory gears ground together!",
                        :STEELROLLER   => "{1} came barrelling down the conveyor line!",
                        :STEAMROLLER   => "{1} came barrelling down the conveyor line!",
                        :GYROBALL      => "{1} spun up like a turbine!",
                        :STEAMERUPTION => "The steam vents burst open!" },
    :damage_mods   => [
      { :moves => hammers, :mult => 1.3, :message => "{2} rang out like a forge hammer!" },
      { :types => [:STEEL], :user => { :abilities => [:STEELWORKER, :STEELYSPIRIT] }, :mult => 1.2 }
    ],
    :accuracy_mods => [{ :moves => [:METALSOUND, :SCREECH], :set => 100 }],
    # The crucibles' heat softens metal plating: counterplay against Steel walls
    :added_effects => [
      { :types => [:FIRE], :category => :damaging, :target => { :types => [:STEEL] }, :chance => 30,
        :stats => { :DEFENSE => -1 }, :message => "The heat softened {1}'s metal plating!" }
    ],
    :move_stat_boosts => [
      { :moves => [:SHIFTGEAR], :user_stats => { :DEFENSE => 1 }, :message => "The factory's gears meshed with {1}'s!" },
      { :moves => [:AUTOTOMIZE], :user_stats => { :SPEED => 1 }, :message => "{1} shed its spare parts on the line!" },
      { :moves => [:IRONDEFENSE], :user_stats => { :DEFENSE => 1 }, :message => "{1} bolted on extra plating!" },
      { :moves => [:METALSOUND], :target_stats => { :SPECIAL_DEFENSE => -1 }, :message => "The screech rang off every girder!" },
      { :moves => [:MAGNETRISE], :user_stats => { :SPEED => 1 }, :message => "{1} rode the foundry's magnets!" }
    ],
    :status_immunity => [{ :status => [:FROZEN], :message => "Nothing can freeze this close to the crucibles!" }],
    :effect_durations => { :MAGNETRISE => [3, "The foundry's magnets will hold {1} aloft for longer!"] },
    :on_entry      => [
      { :battlers => { :abilities => [:LIGHTMETAL] }, :stats => { :SPEED => 1 }, :message => "{1} darted along the catwalks!" },
      { :battlers => { :abilities => [:HEAVYMETAL] }, :stats => { :DEFENSE => 1 },
        :message => "{1} planted itself on the steel floor plates!" },
      { :battlers => { :abilities => [:DOWNLOAD] }, :stats => { :SPEED => 1 }, :message => "{1} synced with the assembly line!" }
    ],
    :end_of_round  => [
      { :battlers => { :status => [:FROZEN] }, :cure_status => true, :message => "The crucibles' heat thawed {1} out!" }
    ],
    :weather       => { :block => [:Rain, :Sandstorm, :Hail],
                        :block_message => "The foundry roof shuts out the weather!",
                        :extend => { :Sun => 2 } },
    :terrain       => { :extend => { :Electric => 2 } },
    :transitions   => [
      { :moves => [:EXPLOSION, :SELFDESTRUCT, :MISTYEXPLOSION, :MINDBLOWN], :to => :SCRAPYARD,
        :message => "The blast tore the foundry apart! Only scrap remains." },
      { :moves => quakes, :to => :SCRAPYARD, :uses => 3,
        :progress_message => "The gantries groan and buckle... ({1} more)",
        :message => "The catwalks came crashing down! The foundry is reduced to scrap." }
    ],
    :seed => { :item => :SYNTHETICSEED, :stats => { :ATTACK => 1, :SPEED => 1 },
               :message => "{1}'s {2} oiled its joints like factory machinery!" }
  }
end).call)
