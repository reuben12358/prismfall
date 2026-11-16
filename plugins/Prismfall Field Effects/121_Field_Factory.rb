#===============================================================================
# FACTORY - Gym 15 (Steel), Cogsworth, the foundry district of Zenith, the City
# Above. Conveyor lines, crucibles of molten steel, giant gears and catwalks.
# Wreck it (explosions, or quakes that bring the gantries down) -> SCRAPYARD.
#===============================================================================
FieldEffects.register(:FACTORY, {
  :name          => "Factory",
  :backdrop      => "field_factory",
  :intro_message => "Gears grind and molten steel pours... The foundry roars to life!",
  :description   => "Steel and machinery are empowered; the crucibles' heat softens metal. Explosions or quakes wreck it.",
  :notes         => ["Steel x1.5, Electric x1.2, Fire x1.2. Gear Grind, Magnet Bomb, rolling moves x1.5; hammers x1.3.",
                     "Fire attacks may soften a Steel target's Defense. Metal Sound and Screech never miss.",
                     "Indoors: Rain, Sandstorm and Hail can't start. Sun and Electric Terrain last longer.",
                     "Explosions wreck the foundry at once; 3 quakes bring the catwalks down. Either leaves a Scrapyard."],
  :nature_power  => :GEARGRIND,
  :camouflage    => :STEEL,
  :secret_power  => 14,
  :type_mods     => { :STEEL => 1.5, :ELECTRIC => 1.2, :FIRE => 1.2 },
  :type_messages => { :STEEL => "The foundry's machinery roared!",
                      :FIRE  => "The crucibles flared white-hot!" },
  :move_mods     => { :GEARGRIND => 1.5, :MAGNETBOMB => 1.5, :STEELROLLER => 1.5, :STEAMROLLER => 1.5,
                      :DOUBLEIRONBASH => 1.3, :GYROBALL => 1.3, :TECHNOBLAST => 1.3, :STEAMERUPTION => 1.3,
                      :EXPLOSION => 1.3, :SELFDESTRUCT => 1.3, :MISTYEXPLOSION => 1.3 },
  :move_messages => { :GEARGRIND   => "The factory gears ground together!",
                      :STEELROLLER => "{1} came barrelling down the conveyor line!",
                      :STEAMROLLER => "{1} came barrelling down the conveyor line!",
                      :STEAMERUPTION => "The steam vents burst open!" },
  :damage_mods   => [
    { :moves => [:HAMMERARM, :ICEHAMMER, :WOODHAMMER, :CRABHAMMER, :DRAGONHAMMER], :mult => 1.3,
      :message => "{2} rang out like a forge hammer!" },
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
    { :moves => [:MAGNETRISE], :user_stats => { :SPEED => 1 }, :message => "{1} rode the foundry's magnets!" }
  ],
  :on_entry      => [
    { :battlers => { :abilities => [:LIGHTMETAL] }, :stats => { :SPEED => 1 },
      :message => "{1} darted along the catwalks!" },
    { :battlers => { :abilities => [:HEAVYMETAL] }, :stats => { :DEFENSE => 1 },
      :message => "{1} planted itself on the steel floor plates!" }
  ],
  :end_of_round  => [
    { :battlers => { :status => [:FROZEN] }, :cure_status => true,
      :message => "The crucibles' heat thawed {1} out!" }
  ],
  :weather       => { :block => [:Rain, :Sandstorm, :Hail],
                      :block_message => "The foundry roof shuts out the weather!",
                      :extend => { :Sun => 2 } },
  :terrain       => { :extend => { :Electric => 2 } },
  :transitions   => [
    { :moves => [:EXPLOSION, :SELFDESTRUCT, :MISTYEXPLOSION, :MINDBLOWN], :to => :SCRAPYARD,
      :message => "The blast tore the foundry apart! Only scrap remains." },
    { :moves => [:EARTHQUAKE, :MAGNITUDE, :BULLDOZE, :FISSURE, :HEADLONGRUSH, :PRECIPICEBLADES,
                 :THOUSANDWAVES], :to => :SCRAPYARD, :uses => 3,
      :progress_message => "The gantries groan and buckle... ({1} more)",
      :message => "The catwalks came crashing down! The foundry is reduced to scrap." }
  ],
  :seed => { :item => :SYNTHETICSEED, :stats => { :ATTACK => 1, :SPEED => 1 },
             :message => "{1}'s {2} oiled its joints like factory machinery!" }
})
