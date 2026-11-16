#===============================================================================
# SCRAPYARD - the FACTORY after it is wrecked (also used on Zenith/Nadir junk
# routes). Smouldering scrap heaps, leaking chemicals, severed live cables, rust.
#===============================================================================
FieldEffects.register(:SCRAPYARD, {
  :name          => "Scrapyard",
  :backdrop      => "field_scrapyard",
  :intro_message => "Jagged scrap and leaking chemicals litter the ground...",
  :description   => "Jagged scrap cuts the grounded on entry; rust leaves Steel weak to Water; junk and fumes are weapons.",
  :notes         => ["Steel x1.2, Poison x1.2. Fling x2; Smog, Gunk Shot and Magnet Bomb are stronger.",
                     "Rust: Water moves are super effective against Steel types. Steel rusts in the rain.",
                     "Grounded Pokemon are cut by scrap when they enter (Heavy-Duty Boots protect).",
                     "Electric attacks may paralyze Steel targets. Shift Gear and Gear Up fail."],
  :nature_power  => :GUNKSHOT,
  :camouflage    => :STEEL,
  :secret_power  => 4,
  :type_mods     => { :STEEL => 1.2, :POISON => 1.2 },
  :type_messages => { :POISON => "Chemicals leaking from the scrap fed the attack!" },
  :move_mods     => { :FLING => 2.0, :GUNKSHOT => 1.3, :SMOG => 1.5, :CLEARSMOG => 1.3, :MAGNETBOMB => 1.3 },
  :move_messages => { :FLING => "{1} hurled a hunk of scrap metal!",
                      :SMOG  => "Choking fumes rose from the burning scrap!" },
  # Rust: Water eats into Steel plating
  :effectiveness_mods => [{ :attack => [:WATER], :defend => [:STEEL], :set => 2.0 }],
  :accuracy_mods => [{ :moves => [:GUNKSHOT], :mult => 1.25 }],
  :added_effects => [
    { :types => [:ELECTRIC], :category => :damaging, :target => { :types => [:STEEL] }, :chance => 20,
      :status => :PARALYSIS, :message => "Current from a severed cable arced through {1}!" }
  ],
  :move_stat_boosts => [
    { :moves => [:SMOKESCREEN], :target_stats => { :ACCURACY => -1 },
      :message => "Thick smoke billowed from the smouldering scrap!" }
  ],
  :move_fails    => [
    { :moves => [:SHIFTGEAR, :GEARUP], :message => "The rusted gears wouldn't turn!" }
  ],
  :on_entry      => [
    { :battlers => { :grounded => true, :not_items => [:HEAVYDUTYBOOTS] }, :damage => 1/16r,
      :damage_type => :STEEL, :message => "{1} was cut by jagged scrap!" },
    { :battlers => { :abilities => [:SCRAPPY] }, :stats => { :ATTACK => 1 },
      :message => "{1} feels right at home in the scrap heap!" },
    { :battlers => { :abilities => [:PICKUP] }, :stats => { :SPEED => 1 },
      :message => "{1} scavenged something useful from the scrap!" }
  ],
  :end_of_round  => [
    { :battlers => { :types => [:STEEL],
                     :condition => proc { |battle, battler| [:Rain, :HeavyRain].include?(battle.pbWeather) } },
      :damage => 1/16r, :message => "{1} is rusting in the rain!" }
  ],
  :seed => { :item => :SYNTHETICSEED, :stats => { :DEFENSE => 1, :SPECIAL_DEFENSE => 1, :SPEED => -1 },
             :message => "{1}'s {2} bolted scrap armor onto it!" }
})
