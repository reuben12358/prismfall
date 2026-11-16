#===============================================================================
# BEACH - the south coast around Ferrow's Landing. A rising tide -> WATER_SURFACE.
#===============================================================================
FieldEffects.register(:BEACH, {
  :name          => "Beach",
  :backdrop      => "field_beach",
  :intro_message => "Waves lap at the sandy shore...",
  :description   => "Sand and surf: Ground and Water both thrive, sand and swim abilities shine, and the calm sea air rewards focus. Enough surf brings the tide in.",
  :notes         => ["Boosted: Water and Ground x1.2. Mud-Slap x2; Muddy Water, Sand Tomb x1.5.",
                     "Scorching Sands x1.3 (50% burn). Crabhammer, Razor Shell, Shell Side Arm x1.3.",
                     "Shore Up heals 2/3 HP. Calm Mind and Meditate give an extra boost.",
                     "Sand Rush and Swift Swim x1.5 Speed. Sand Veil and Sand Force are active.",
                     "Hail can't form. 3 big surf moves or heavy rain flood it into Water Surface."],
  :nature_power  => :MUDDYWATER,
  :camouflage    => :GROUND,
  :secret_power  => 8,
  :type_mods     => { :WATER => 1.2, :GROUND => 1.2 },
  :move_mods     => { :MUDSLAP => 2.0, :MUDDYWATER => 1.5, :SANDTOMB => 1.5, :SCORCHINGSANDS => 1.3,
                      :CRABHAMMER => 1.3, :RAZORSHELL => 1.3, :SHELLSIDEARM => 1.3 },
  :move_messages => { :MUDDYWATER => "Sand and surf crashed together!",
                      :MUDSLAP    => "{1} flung a fistful of wet sand!",
                      :CRABHAMMER => "{1} struck with the strength of the tide pools!" },
  :damage_mods   => [
    { :types => [:GROUND, :ROCK, :STEEL], :user => { :abilities => [:SANDFORCE] }, :mult => 1.3 }
  ],
  :effect_chance_mods => [{ :moves => [:SCORCHINGSANDS], :set => 50 }],
  :accuracy_mods => [
    { :moves => [:SANDATTACK], :always_hit => true },
    { :target => { :abilities => [:SANDVEIL] }, :evasion_mult => 1.2 }
  ],
  :move_stat_boosts => [
    { :moves => [:CALMMIND], :user_stats => { :SPECIAL_ATTACK => 1 }, :message => "The sound of the waves focused {1}'s mind!" },
    { :moves => [:MEDITATE], :user_stats => { :ATTACK => 1 }, :message => "The sound of the waves focused {1}'s mind!" },
    { :moves => [:KINESIS], :target_stats => { :ACCURACY => -1 }, :message => "The glare off the sea made {2} even more dazzling!" }
  ],
  :speed_mods    => [
    { :battlers => { :abilities => [:SANDRUSH, :SWIFTSWIM] }, :mult => 1.5 }
  ],
  :on_entry      => [
    { :battlers => { :abilities => [:WATERCOMPACTION] }, :stats => { :DEFENSE => 1 },
      :message => "{1} hardened in the wet sand!" }
  ],
  :end_of_round  => [
    { :battlers => { :abilities => [:WATERABSORB, :DRYSKIN] }, :heal => 1/16r, :message => "{1} soaked up the sea spray." },
    { :battlers => { :abilities => [:HYDRATION] }, :cure_status => true }
  ],
  :hooks         => {
    :after_move => proc { |battle, user, targets, move, num_hits|
      next if user.lastMoveFailed || move.id != :SHOREUP || !user.canHeal?
      user.pbRecoverHP([user.totalhp / 6, 1].max)
      battle.pbDisplay(FieldEffects.format("{1} drew extra strength from the shore!", user.pbThis))
    }
  },
  :weather       => { :block => [:Hail], :block_message => "The balmy sea air melted the hail!",
                      :extend => { :Sun => 2, :Sandstorm => 2 } },
  :transitions   => [
    { :weather => [:HeavyRain], :to => :WATER_SURFACE, :message => "The downpour flooded the beach!" },
    { :moves => [:SURF, :MUDDYWATER, :WATERSPOUT, :ORIGINPULSE, :WATERPLEDGE, :WAVECRASH], :to => :WATER_SURFACE,
      :uses => 3, :progress_message => "The tide is rising... ({1} more)",
      :message => "The tide rolled in and swallowed the beach!" }
  ],
  :seed => { :item => :TELLURICSEED, :stats => { :DEFENSE => 1 }, :effects => [:aqua_ring],
             :message => "{1}'s {2} buried it in cool, wet sand!" }
})
