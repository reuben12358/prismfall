#===============================================================================
# BEACH - the south coast around Ferrow's Landing (and Velmora's other shores).
# Sand and surf, tide pools and the sound of the waves (Reborn's Ashen Beach):
# shore-dwellers dig and splash, the calm rewards focus, the sea breeze kicks
# sand into everyone's eyes. A rising tide floods it (WATER_SURFACE).
# Family: Telluric.
#===============================================================================
FieldEffects.register(:BEACH, (lambda do
  focused = [:INNERFOCUS, :OWNTEMPO, :PUREPOWER, :STEADFAST, :SANDVEIL]
  breezes = [:GUST, :TWISTER, :HURRICANE, :AIRCUTTER, :RAZORWIND, :LEAFTORNADO, :FIRESPIN, :WHIRLPOOL, :AIRSLASH]
  shells  = { :CRABHAMMER => 1.3, :RAZORSHELL => 1.3, :SHELLSIDEARM => 1.3, :SHELLTRAP => 1.3, :BRINE => 1.3 }
  focus   = { :AURASPHERE => 1.3, :FOCUSBLAST => 1.3, :ZENHEADBUTT => 1.3, :STOREDPOWER => 1.3 }
  {
    :name          => "Beach",
    :backdrop      => "field_beach",
    :family        => :telluric,
    :intro_message => "Waves lap at the sandy shore...",
    :description   => "Sand and surf: shore-dwellers dig and splash, the calm sea air rewards focus, and the breeze kicks sand into everyone's eyes. A rising tide floods the beach.",
    :notes         => ["Water x1.2, Ground x1.2. Mud-Slap, Mud Shot, Mud Bomb x2; Muddy Water, Sand Tomb x1.5; Scorching Sands x1.3 (50% burn).",
                       "Tide pools: Crabhammer, Razor Shell, Shell Side Arm, Shell Trap, Brine x1.3. Focus: Aura Sphere, Focus Blast, Zen Headbutt, Stored Power x1.3; Focus Blast x1.1 accuracy.",
                       "Focused minds (Inner Focus, Own Tempo, Pure Power, Steadfast, Sand Veil) ignore every accuracy and evasion stage.",
                       "The sound of the waves: Calm Mind also +1 Sp. Atk, Meditate +1 Attack; Kinesis and Sand Attack drop accuracy one stage more (Sand Attack never misses).",
                       "Sand Rush, Sand Force and Sand Veil work in the beach sand. Water Compaction +1 Def and Sp. Def on entry.",
                       "Sea breeze: wind moves (and Fire Spin, Whirlpool, Leaf Tornado) kick up sand - every other Pokemon loses 1 accuracy.",
                       "Shore Up heals 1/6 HP more. Water Absorb and Dry Skin soak up the spray (1/16); Hydration cures status each turn.",
                       "Hail can't form. Sun and Sandstorm last 2 turns longer.",
                       "Heavy rain, or 3 big surf moves (Surf, Muddy Water, Water Spout, Origin Pulse, Water Pledge, Wave Crash) -> Water Surface (the tide comes in).",
                       "Telluric Seed: +1 Defense and Aqua Ring."],
    :nature_power  => :MUDDYWATER,
    :camouflage    => :GROUND,
    :secret_power  => 8,
    :activate_abilities => [:SANDRUSH, :SANDFORCE, :SANDVEIL],
    :type_mods     => { :WATER => 1.2, :GROUND => 1.2 },
    :type_messages => { :WATER => "{1} rode the surf into the attack!" },
    :move_mods     => { :MUDSLAP => 2.0, :MUDSHOT => 2.0, :MUDBOMB => 2.0, :MUDDYWATER => 1.5, :SANDTOMB => 1.5,
                        :SCORCHINGSANDS => 1.3 }.merge(shells).merge(focus),
    :move_messages => { :MUDDYWATER => "Sand and surf crashed together!",
                        :MUDSLAP    => "{1} flung a fistful of wet sand!",
                        :CRABHAMMER => "{1} struck with the strength of the tide pools!",
                        :FOCUSBLAST => "...And with pure focus!",
                        :AURASPHERE => "...And with pure focus!" },
    :effect_chance_mods => [{ :moves => [:SCORCHINGSANDS], :set => 50 }],
    :accuracy_mods => [
      { :moves => [:SANDATTACK], :always_hit => true },
      { :moves => [:FOCUSBLAST], :mult => 1.1 }
    ],
    :move_stat_boosts => [
      { :moves => [:CALMMIND], :user_stats => { :SPECIAL_ATTACK => 1 }, :message => "The sound of the waves focused {1}'s mind!" },
      { :moves => [:MEDITATE], :user_stats => { :ATTACK => 1 }, :message => "The sound of the waves focused {1}'s mind!" },
      { :moves => [:KINESIS], :target_stats => { :ACCURACY => -1 }, :message => "The glare off the sea made {2} even more dazzling!" },
      { :moves => [:SANDATTACK], :target_stats => { :ACCURACY => -1 }, :message => "{1} flung a whole handful of beach sand!" }
    ],
    :on_entry      => [
      { :battlers => { :abilities => [:WATERCOMPACTION] }, :stats => { :DEFENSE => 1, :SPECIAL_DEFENSE => 1 },
        :message => "{1} hardened in the wet sand!" }
    ],
    :end_of_round  => [
      { :battlers => { :abilities => [:WATERABSORB, :DRYSKIN] }, :heal => 1/16r, :message => "{1} soaked up the sea spray." },
      { :battlers => { :abilities => [:HYDRATION] }, :cure_status => true }
    ],
    :hooks         => {
      # Focused minds ignore accuracy and evasion stages
      :accuracy   => proc { |battle, user, target, move, type, mods|
        next if !user.hasActiveAbility?(focused)
        mods[:accuracy_stage] = 0
        mods[:evasion_stage]  = 0
      },
      :after_move => proc { |battle, user, targets, move, num_hits|
        next if user.lastMoveFailed
        if move.id == :SHOREUP && user.canHeal? && !user.fainted?
          user.pbRecoverHP([user.totalhp / 6, 1].max)
          battle.pbDisplay(FieldEffects.format("{1} drew extra strength from the shore!", user.pbThis))
        end
        if breezes.include?(move.id) && move.damagingMove?
          others = battle.allBattlers.select { |b| b.index != user.index && !b.fainted? && b.pbCanLowerStatStage?(:ACCURACY, user) }
          next if others.empty?
          battle.pbDisplay(FieldEffects.format("The sea breeze kicked sand into everyone's eyes!"))
          others.each { |b| b.pbLowerStatStage(:ACCURACY, 1, user) }
        end
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
  }
end).call)
