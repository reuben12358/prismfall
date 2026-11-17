#===============================================================================
# SCRAPYARD - the FACTORY after it is wrecked (also used on Zenith/Nadir junk
# routes). Smouldering scrap heaps, oil slicks, leaking chemicals, live cables,
# rust. Scavengers thrive, junk becomes ammunition, rust leaves Steel weak to
# Water. Recharge the machines and the line restarts (FACTORY); let the
# chemicals leach out and the ground dies (WASTELAND). Family: Synthetic.
#===============================================================================
FieldEffects.register(:SCRAPYARD, (lambda do
  chargers = [:CHARGE, :DISCHARGE, :PARABOLICCHARGE, :WILDCHARGE, :CHARGEBEAM, :ELECTRICTERRAIN, :IONDELUGE,
              :OVERDRIVE, :RISINGVOLTAGE, :MAGNETRISE, :ZAPCANNON]
  leaching = [:ACIDSPRAY, :SLUDGEWAVE, :CORROSIVEGAS, :ACIDARMOR, :ACID]
  {
    :name          => "Scrapyard",
    :backdrop      => "field_scrapyard",
    :family        => :synthetic,
    :intro_message => "Jagged scrap and leaking chemicals litter the ground...",
    :description   => "Scavengers thrive: junk is ammunition, oil burns, cables spark and rust leaves Steel weak to Water. Recharge the machines to restart the line.",
    :notes         => ["Steel x1.2, Poison x1.2 (leaking chemicals). Fling x2; Smog x1.5; Gunk Shot, Clear Smog, Magnet Bomb, Metal Claw, Explosion, Self-Destruct x1.3.",
                       "Rust: Water moves are super effective against Steel types.",
                       "Oil slicks: damaging Fire moves may splash burning oil (20% burn). Live cables: Electric attacks may paralyze Steel targets (20%).",
                       "Stealth Rock is mixed with scrap: an extra 1/16 Steel-scaled hit on entry (Heavy-Duty Boots protect). Smokescreen drops accuracy one stage more.",
                       "Scavengers: Pickup +1 Speed, Scrappy +1 Attack, Magnet Pull +1 Defense (it pulls scrap armor onto itself) on entry.",
                       "Shift Gear and Gear Up fail (the gears have rusted). Gunk Shot x1.25 accuracy.",
                       "3 charging moves (Charge, Discharge, Wild Charge, Magnet Rise, Electric Terrain...; they count even if they fail) restart the machines -> Factory. 2 acid moves (Acid Spray, Sludge Wave, Corrosive Gas, Acid Armor...) leach the chemicals out -> Wasteland.",
                       "Synthetic Seed: +1 Defense, +1 Sp. Def, but the bolted-on scrap is heavy (-1 Speed)."],
    :nature_power  => :GUNKSHOT,
    :camouflage    => :STEEL,
    :secret_power  => 4,
    :type_mods     => { :STEEL => 1.2, :POISON => 1.2 },
    :type_messages => { :POISON => "Chemicals leaking from the scrap fed {2}!" },
    :move_mods     => { :FLING => 2.0, :SMOG => 1.5, :GUNKSHOT => 1.3, :CLEARSMOG => 1.3, :MAGNETBOMB => 1.3,
                        :METALCLAW => 1.3, :EXPLOSION => 1.3, :SELFDESTRUCT => 1.3 },
    :move_messages => { :FLING      => "{1} hurled a hunk of scrap metal!",
                        :SMOG       => "Thick fumes rose from the burning scrap!",
                        :MAGNETBOMB => "The bomb pulled a cloud of scrap along with it!",
                        :EXPLOSION  => "Scrap shrapnel flew everywhere!" },
    # Rust: Water eats into Steel plating
    :effectiveness_mods => [{ :attack => [:WATER], :defend => [:STEEL], :set => 2.0 }],
    :accuracy_mods => [{ :moves => [:GUNKSHOT], :mult => 1.25 }],
    :added_effects => [
      { :types => [:FIRE], :category => :damaging, :chance => 20, :status => :BURN,
        :message => "Burning oil splashed over {1}!" },
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
      { :battlers => { :not_items => [:HEAVYDUTYBOOTS],
                       :condition => proc { |battle, b| b.pbOwnSide.effects[PBEffects::StealthRock] } },
        :damage => 1/16r, :damage_type => :STEEL, :message => "Scrap mixed into the stones cut {1}!" },
      { :battlers => { :abilities => [:PICKUP] }, :stats => { :SPEED => 1 },
        :message => "{1} scavenged something useful from the scrap!" },
      { :battlers => { :abilities => [:SCRAPPY] }, :stats => { :ATTACK => 1 },
        :message => "{1} feels right at home in the scrap heap!" },
      { :battlers => { :abilities => [:MAGNETPULL] }, :stats => { :DEFENSE => 1 },
        :message => "{1} pulled a coat of scrap armor onto itself!" }
    ],
    :transitions   => [
      { :moves => chargers, :to => :FACTORY, :uses => 3, :even_if_failed => true,
        :progress_message => "The machines sputter and twitch... ({1} more)",
        :message => "The machines roared back to life! The foundry line is running again!" },
      { :moves => leaching, :to => :WASTELAND, :uses => 2, :even_if_failed => true,
        :progress_message => "Chemicals are seeping into the ground... ({1} more)",
        :message => "The chemicals leached into the ground! The yard became a blighted wasteland!" }
    ],
    :seed => { :item => :SYNTHETICSEED, :stats => { :DEFENSE => 1, :SPECIAL_DEFENSE => 1, :SPEED => -1 },
               :message => "{1}'s {2} bolted scrap armor onto it!" }
  }
end).call)
