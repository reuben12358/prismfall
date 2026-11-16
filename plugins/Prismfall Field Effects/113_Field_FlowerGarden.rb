#===============================================================================
# FLOWER_GARDEN - Gym 9 (Grass), Verdance in Elowen. Juno's terraced garden.
# Five growth stages (1 buds -> 5 overgrown riot). Tending it (Growth, Sunny
# Day, rain, Grassy Terrain, Grass attacks...) makes it grow; fire, blades and
# frost cut it back. At stage 5 fire burns it down to Ashen Waste.
#===============================================================================
# (Helpers live inside the lambda: plugin files share TOPLEVEL_BINDING.)
FieldEffects.register(:FLOWER_GARDEN, (lambda do
  # Local helper: the stage transitions, with the message for this stage's growth.
  fg_transitions = lambda do |grow_message, final|
    rules = []
    if !final
      rules.push(
        { :moves => [:GROWTH, :ROTOTILLER, :FLOWERSHIELD, :INGRAIN, :WATERSPORT, :AROMATHERAPY,
                     :FLORALHEALING, :LIFEDEW, :GRASSPLEDGE, :WATERPLEDGE],
          :even_if_failed => true, :stage_delta => 1, :message => grow_message },
        { :weather => [:Sun, :HarshSun, :Rain, :HeavyRain], :stage_delta => 1, :message => grow_message },
        { :terrain => [:Grassy], :stage_delta => 1, :message => grow_message },
        { :types => [:GRASS], :category => :damaging, :uses => 2, :stage_delta => 1,
          :message => grow_message }
      )
    end
    if final
      rules.push({ :types => [:FIRE], :category => :damaging, :uses => 2, :to => :ASHEN_WASTE,
                   :progress_message => "The overgrowth is catching fire! ({1} more)",
                   :message => "The garden went up in flames! Only ash remains..." })
    else
      rules.push({ :types => [:FIRE], :category => :damaging, :stage_delta => -1,
                   :message => "The flames scorched the garden!" })
    end
    rules.push(
      { :flags => ["Slicing"], :not_types => [:GRASS], :category => :damaging, :stage_delta => -1,
        :message => "The garden was cut back!" },
      { :weather => [:Hail], :stage_delta => -1, :message => "The frost withered the garden!" }
    )
    next rules
  end

  fg_petals = [:PETALDANCE, :PETALBLIZZARD, :FLOWERTRICK, :POLLENPUFF, :FLEURCANNON]

  # Stage 3+ shared rules
  fg_bloom_boosts = [
    { :moves => [:SWEETSCENT], :target_stats => { :DEFENSE => -1, :SPECIAL_DEFENSE => -1 },
      :message => "The blossoms' perfume left the foes defenseless!" },
    { :moves => [:GROWTH], :user_stats => { :ATTACK => 1, :SPECIAL_ATTACK => 1 },
      :message => "The blossoms fed {1}'s growth!" }
  ]
  fg_bloom_damage = [
    { :types => [:GRASS], :user => { :abilities => [:OVERGROW] }, :mult => 1.5 },
    { :category => :physical, :target => { :abilities => [:GRASSPELT] }, :defense_mult => 1.5 }
  ]
  fg_grass_heal = { :battlers => { :types => [:GRASS], :grounded => true }, :heal => 1/16r,
                    :message => "{1} drank from the blooming garden." }
  fg_bug_heal   = { :battlers => { :types => [:BUG] }, :heal => 1/16r,
                    :message => "{1} feasted on the garden's nectar." }
  fg_chlorophyll = { :battlers => { :abilities => [:CHLOROPHYLL],
                                    :condition => proc { |battle, b| ![:Sun, :HarshSun].include?(battle.pbWeather) } },
                     :mult => 1.5 }

  {
    # ---- Stage 1: Buds ---------------------------------------------------------
    :name          => "Flower Garden",
    :backdrop      => "field_flower_garden",
    :intro_message => "Tiny buds dot the garden beds.",
    :description   => "Grows in 5 stages from tending, sun, rain and Grass attacks; Grass, Bug and (later) Fire grow stronger. Fire, blades and frost cut it back.",
    :nature_power  => :MAGICALLEAF,
    :camouflage    => :GRASS,
    :secret_power  => 2,
    :type_mods     => { :GRASS => 1.1 },
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
        :move_mods     => fg_petals.map { |m| [m, 1.2] }.to_h,
        :transitions   => fg_transitions.call("The garden burst into bloom!", false)
      },
      # ---- Stage 3: Blooms -----------------------------------------------------
      3 => {
        :backdrop      => "field_flower_garden_3",
        :intro_message => "Flowers bloom across the garden!",
        :nature_power  => :PETALBLIZZARD,
        :type_mods     => { :GRASS => 1.3, :BUG => 1.2, :FIRE => 1.1 },
        :type_messages => { :GRASS => "The blooming garden empowered the attack!" },
        :move_mods     => fg_petals.map { |m| [m, 1.3] }.to_h,
        :damage_mods   => fg_bloom_damage,
        :move_stat_boosts => fg_bloom_boosts,
        :end_of_round  => [fg_grass_heal],
        :transitions   => fg_transitions.call("The garden is in full flower!", false)
      },
      # ---- Stage 4: Full flower ------------------------------------------------
      4 => {
        :backdrop      => "field_flower_garden_4",
        :intro_message => "The garden is in full flower!",
        :nature_power  => :PETALBLIZZARD,
        :type_mods     => { :GRASS => 1.5, :BUG => 1.3, :FIRE => 1.3 },
        :type_messages => { :GRASS => "The flowering garden empowered the attack!",
                            :FIRE  => "The dry petals fed the flames!" },
        :move_mods     => fg_petals.map { |m| [m, 1.5] }.to_h,
        :damage_mods   => fg_bloom_damage,
        :move_stat_boosts => fg_bloom_boosts,
        :speed_mods    => [fg_chlorophyll],
        :end_of_round  => [fg_grass_heal, fg_bug_heal],
        :transitions   => fg_transitions.call("The garden overflowed into a riot of blossoms!", false)
      },
      # ---- Stage 5: Overgrown riot ---------------------------------------------
      5 => {
        :backdrop      => "field_flower_garden_5",
        :intro_message => "The garden is an overgrown riot of colour!",
        :nature_power  => :PETALDANCE,
        :type_mods     => { :GRASS => 2.0, :BUG => 1.5, :FIRE => 1.5 },
        :type_messages => { :GRASS => "The overgrown garden surged with power!",
                            :FIRE  => "The overgrowth went up like tinder!" },
        :move_mods     => fg_petals.map { |m| [m, 1.5] }.to_h,
        :damage_mods   => fg_bloom_damage,
        :move_stat_boosts => fg_bloom_boosts,
        :speed_mods    => [fg_chlorophyll],
        :end_of_round  => [fg_grass_heal, fg_bug_heal],
        :transitions   => fg_transitions.call(nil, true)
      }
    }
  }
end).call)
