#===============================================================================
# NEON_GRID - Gym 4 (Electric), Lumen City. A humming arena of live circuitry.
#===============================================================================
FieldEffects.register(:NEON_GRID, {
  :name          => "Neon Grid",
  :backdrop      => "field_neon_grid",
  :intro_message => "Neon circuitry hums beneath your feet!",
  :description   => "Electricity surges and stray currents jolt the grounded. Earthquakes can short it out.",
  :nature_power  => :DISCHARGE,
  :camouflage    => :ELECTRIC,
  :secret_power  => 1,
  :type_mods     => { :ELECTRIC => 1.5, :STEEL => 1.2 },
  :type_messages => { :ELECTRIC => "The neon grid surged!" },
  :move_mods     => { :DISCHARGE => 1.3, :PARABOLICCHARGE => 1.3, :RISINGVOLTAGE => 1.5 },
  :damage_mods   => [
    { :flags => ["Pulse"], :mult => 1.5, :message => "The circuitry amplified {2}!" },
    { :moves => [:DAZZLINGGLEAM, :FLASHCANNON, :LIGHTOFRUIN, :PRISMATICLASER, :PHOTONGEYSER,
                 :LUSTERPURGE, :MIRRORSHOT, :SIGNALBEAM, :TECHNOBLAST], :mult => 1.3,
      :message => "The neon light intensified {2}!" }
  ],
  :extra_types   => [
    { :moves => [:GEARGRIND, :MAGNETBOMB, :GYROBALL, :FLASHCANNON, :STEELBEAM], :add => :ELECTRIC,
      :message => "The charged metal crackled with electricity!" }
  ],
  :accuracy_mods => [
    { :moves => [:ZAPCANNON], :set => 80 },
    { :moves => [:THUNDER], :mult => 1.2 }
  ],
  :added_effects => [
    { :types => [:WATER], :category => :damaging, :chance => 30, :status => :PARALYSIS,
      :message => "The water conducted the grid's current into {1}!" }
  ],
  :move_stat_boosts => [
    { :moves => [:CHARGE], :user_stats => { :SPECIAL_ATTACK => 1 }, :message => "The grid overcharged {1}!" },
    { :moves => [:MAGNETRISE], :user_stats => { :SPEED => 1 }, :message => "{1} rode the magnetic field!" },
    { :moves => [:EERIEIMPULSE], :target_stats => { :SPECIAL_ATTACK => -1 } }
  ],
  :speed_mods    => [{ :battlers => { :abilities => [:SURGESURFER] }, :mult => 2.0 }],
  :on_entry      => [
    { :battlers => { :abilities => [:PLUS, :MINUS] }, :stats => { :SPECIAL_ATTACK => 1 },
      :message => "{1} synced with the grid!" },
    { :battlers => { :abilities => [:MOTORDRIVE, :LIGHTNINGROD, :VOLTABSORB, :ELECTROMORPHOSIS] },
      :effects => [:charge], :message => "{1} soaked up current from the grid!" }
  ],
  :end_of_round  => [
    { :battlers => { :grounded => true, :not_types => [:ELECTRIC, :GROUND] }, :chance => 10,
      :status => :PARALYSIS, :message => "{1} was jolted by a stray current!" },
    { :battlers => { :abilities => [:VOLTABSORB] }, :heal => 1/16r,
      :message => "{1} drew power from the grid." }
  ],
  :terrain       => { :extend => { :Electric => 3 } },
  :transitions   => [
    { :moves => [:EARTHQUAKE, :MAGNITUDE, :BULLDOZE, :FISSURE, :PRECIPICEBLADES, :THOUSANDWAVES],
      :to => :NONE, :uses => 2,
      :progress_message => "The grid flickers and sparks... ({1} more)",
      :message => "The grid shorted out! The neon lights went dark." }
  ],
  :seed => { :item => :SYNTHETICSEED, :stats => { :SPECIAL_ATTACK => 1 }, :effects => [:magnet_rise],
             :message => "{1}'s {2} magnetized it above the grid!" }
})
