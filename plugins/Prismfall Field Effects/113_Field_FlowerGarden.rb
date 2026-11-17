#===============================================================================
# FLOWER_GARDEN - Gym 9 (Grass), Verdance in Elowen. Juno's terraced garden.
# Five growth stages (1 buds -> 5 overgrown riot). Tending it (Growth, Sunny
# Day, rain, Grassy Terrain, Grass attacks...) makes it grow; fire, blades,
# frost and acid cut it back. At stage 5 fire sets the overgrowth ablaze
# (WILDFIRE). Family: Telluric.
#===============================================================================
# (Helpers live inside the lambda: plugin files share TOPLEVEL_BINDING.)
FieldEffects.register(:FLOWER_GARDEN, (lambda do
  tending = [:GROWTH, :ROTOTILLER, :FLOWERSHIELD, :INGRAIN, :WATERSPORT, :AROMATHERAPY, :FLORALHEALING,
             :LIFEDEW, :GRASSPLEDGE, :WATERPLEDGE, :LEECHSEED]
  blades  = [:CUT, :FURYCUTTER, :SLASH, :NIGHTSLASH, :XSCISSOR, :AIRSLASH, :AIRCUTTER, :PSYCHOCUT,
             :CROSSPOISON, :SACREDSWORD, :RAZORSHELL, :STONEAXE, :AQUACUTTER, :BITTERBLADE, :KOWTOWCLEAVE,
             :PSYBLADE, :BEHEMOTHBLADE, :BREAKINGSWIPE]
  acid    = [:ACIDSPRAY, :SLUDGEWAVE, :CORROSIVEGAS, :ACID]
  petals  = [:PETALDANCE, :PETALBLIZZARD, :FLOWERTRICK, :POLLENPUFF, :FLEURCANNON]

  fg_transitions = lambda do |grow_message, final|
    rules = []
    if !final
      rules.push(
        { :moves => tending, :even_if_failed => true, :stage_delta => 1, :message => grow_message },
        { :weather => [:Sun, :HarshSun, :Rain, :HeavyRain], :stage_delta => 1, :message => grow_message },
        { :terrain => [:Grassy], :stage_delta => 1, :message => grow_message },
        { :types => [:GRASS], :category => :damaging, :uses => 2, :stage_delta => 1, :message => grow_message }
      )
      rules.push({ :types => [:FIRE], :category => :damaging, :stage_delta => -1,
                   :message => "The flames scorched the garden back!" })
    else
      rules.push({ :types => [:FIRE], :category => :damaging, :uses => 2, :to => :WILDFIRE,
                   :progress_message => "The overgrowth is catching fire! ({1} more)",
                   :message => "The overgrowth went up like tinder! The garden is ablaze!" })
    end
    rules.push(
      { :moves => blades, :not_types => [:GRASS], :stage_delta => -1, :message => "The garden was cut back!" },
      { :weather => [:Hail], :stage_delta => -1, :message => "The frost nipped the garden back!" },
      { :moves => acid, :stage => 1, :message => "The acid burned the garden back to its roots!" }
    )
    next rules
  end

  # Stage 3+ shared rules
  fg_bloom_boosts = [
    { :moves => [:SWEETSCENT], :target_stats => { :DEFENSE => -1, :SPECIAL_DEFENSE => -1 },
      :message => "The blossoms' perfume left the foes defenseless!" },
    { :moves => [:GROWTH], :user_stats => { :ATTACK => 1, :SPECIAL_ATTACK => 1 },
      :message => "The blossoms fed {1}'s growth!" },
    { :moves => [:ROTOTILLER], :user_stats => { :ATTACK => 1, :SPECIAL_ATTACK => 1 },
      :message => "{1} turned the rich soil!" }
  ]
  fg_grass_heal = { :battlers => { :types => [:GRASS], :grounded => true }, :heal => 1/16r,
                    :message => "{1} drank from the blooming garden." }
  fg_bug_heal   = { :battlers => { :types => [:BUG] }, :heal => 1/16r,
                    :message => "{1} feasted on the garden's nectar." }
  cut_rule = { :moves => [:CUT], :mult => 1.5, :message => "{1} pruned with a gardener's precision!" }
  # Entry: Flower Veil / Flower Gift Pokemon tend the garden as they arrive
  tend_entry = { :battlers => { :abilities => [:FLOWERVEIL, :FLOWERGIFT] },
                 :proc => proc { |battle, b|
                   st = FieldEffects.stage(battle)
                   next false if st >= 5
                   battle.set_field_stage(st + 1, FieldEffects.format("{1} tended the flowerbeds! The garden grew!", b.pbThis))
                 } }

  {
    # ---- Stage 1: Buds ---------------------------------------------------------
    :name          => "Flower Garden",
    :backdrop      => "field_flower_garden",
    :family        => :telluric,
    :intro_message => "Tiny buds dot the garden beds.",
    :description   => "Grows in 5 stages from tending, sun, rain and Grass attacks; Grass, Bug and (later) Fire grow stronger. Fire, blades, frost and acid cut it back.",
    :notes         => ["5 growth stages; the gym's starting stage depends on the puzzle.",
                       "Grows +1: Growth, Rototiller, Flower Shield, Ingrain, Water Sport, Aromatherapy, Floral Healing, Life Dew, Leech Seed, the Pledges (they count even if they fail); sun or rain starting; Grassy Terrain starting; every 2 Grass attacks; a Flower Veil or Flower Gift Pokemon entering.",
                       "Cut back -1: Fire attacks (stages 1-4), non-Grass blades (Slash, X-Scissor, Air Slash...), hail. Acid (Acid Spray, Sludge Wave, Corrosive Gas) burns it back to stage 1.",
                       "Grass x1.1 / 1.2 / 1.3 / 1.5 / 2.0. Bug - / 1.1 / 1.2 / 1.3 / 1.5. Fire - / - / 1.1 / 1.3 / 1.5. Petal moves - / 1.2 / 1.3 / 1.5 / 1.5. Cut x1.5 at every stage.",
                       "Stage 3+: Overgrow, Swarm and Grass Pelt always active; Sweet Scent also lowers Def and Sp. Def; Growth and Rototiller give +1 Atk and Sp. Atk more; powder moves x1.2 accuracy; grounded Grass types drink 1/16 HP a turn.",
                       "Stage 4+: Chlorophyll and Flower Gift active; Bug types feast on nectar (1/16 HP).",
                       "Stage 5: the overgrowth shields Grass types (their weaknesses become neutral) - but 2 Fire attacks set it ablaze -> Wildfire.",
                       "Grassy Terrain lasts 3 turns longer at every stage.",
                       "Telluric Seed: +1 Sp. Def and Ingrain, and the garden grows one stage."],
    :nature_power  => :MAGICALLEAF,
    :camouflage    => :GRASS,
    :secret_power  => 2,
    :type_mods     => { :GRASS => 1.1 },
    :damage_mods   => [cut_rule],
    :on_entry      => [tend_entry],
    :terrain       => { :extend => { :Grassy => 3 } },
    :transitions   => fg_transitions.call("Sprouts pushed up through the soil!", false),
    :seed => { :item => :TELLURICSEED, :stats => { :SPECIAL_DEFENSE => 1 }, :effects => [:ingrain],
               :message => "{1}'s {2} took root in the garden!",
               :proc => proc { |battle, battler|
                 battle.set_field_stage(FieldEffects.stage(battle) + 1, "The seed made the garden grow!")
               } },
    :stages => {
      # ---- Stage 2: Sprouts ----------------------------------------------------
      2 => {
        :backdrop      => "field_flower_garden_2",
        :intro_message => "Green sprouts carpet the garden beds.",
        :type_mods     => { :GRASS => 1.2, :BUG => 1.1 },
        :move_mods     => petals.map { |m| [m, 1.2] }.to_h,
        :transitions   => fg_transitions.call("The garden burst into bloom!", false)
      },
      # ---- Stage 3: Blooms -----------------------------------------------------
      3 => {
        :backdrop      => "field_flower_garden_3",
        :intro_message => "Flowers bloom across the garden!",
        :nature_power  => :PETALBLIZZARD,
        :activate_abilities => [:OVERGROW, :SWARM, :GRASSPELT],
        :type_mods     => { :GRASS => 1.3, :BUG => 1.2, :FIRE => 1.1 },
        :type_messages => { :GRASS => "The blooming garden poured its strength into {2}!" },
        :move_mods     => petals.map { |m| [m, 1.3] }.to_h,
        :move_stat_boosts => fg_bloom_boosts,
        :accuracy_mods => [{ :flags => ["Powder"], :mult => 1.2 }],
        :end_of_round  => [fg_grass_heal],
        :transitions   => fg_transitions.call("The garden is in full flower!", false)
      },
      # ---- Stage 4: Full flower ------------------------------------------------
      4 => {
        :backdrop      => "field_flower_garden_4",
        :intro_message => "The garden is in full flower!",
        :nature_power  => :PETALBLIZZARD,
        :activate_abilities => [:OVERGROW, :SWARM, :GRASSPELT, :CHLOROPHYLL, :FLOWERGIFT],
        :type_mods     => { :GRASS => 1.5, :BUG => 1.3, :FIRE => 1.3 },
        :type_messages => { :GRASS => "The flowering garden poured its strength into {2}!",
                            :FIRE  => "The dry petals fed the flames!" },
        :move_mods     => petals.map { |m| [m, 1.5] }.to_h,
        :move_stat_boosts => fg_bloom_boosts,
        :accuracy_mods => [{ :flags => ["Powder"], :mult => 1.2 }],
        :end_of_round  => [fg_grass_heal, fg_bug_heal],
        :transitions   => fg_transitions.call("The garden overflowed into a riot of blossoms!", false)
      },
      # ---- Stage 5: Overgrown riot ---------------------------------------------
      5 => {
        :backdrop      => "field_flower_garden_5",
        :intro_message => "The garden is an overgrown riot of colour!",
        :nature_power  => :PETALDANCE,
        :activate_abilities => [:OVERGROW, :SWARM, :GRASSPELT, :CHLOROPHYLL, :FLOWERGIFT],
        :type_mods     => { :GRASS => 2.0, :BUG => 1.5, :FIRE => 1.5 },
        :type_messages => { :GRASS => "The overgrown garden surged with power!",
                            :FIRE  => "The overgrowth went up like tinder!" },
        :move_mods     => petals.map { |m| [m, 1.5] }.to_h,
        :move_stat_boosts => fg_bloom_boosts,
        :accuracy_mods => [{ :flags => ["Powder"], :mult => 1.2 }],
        :end_of_round  => [fg_grass_heal, fg_bug_heal],
        :hooks         => {
          # The overgrowth shields Grass types: their weaknesses become neutral
          :effectiveness => proc { |battle, move, move_type, def_type, user, target, eff|
            (def_type == :GRASS && eff > Effectiveness::NORMAL_EFFECTIVE_MULTIPLIER) ? Effectiveness::NORMAL_EFFECTIVE_MULTIPLIER : nil
          }
        },
        :transitions   => fg_transitions.call(nil, true)
      }
    }
  }
end).call)
