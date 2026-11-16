#===============================================================================
# SNOWY_MOUNTAIN - Isenmar's frozen summits. Big fire or sunlight -> MOUNTAIN.
# (Helpers inside the lambda so they don't leak into TOPLEVEL_BINDING.)
#===============================================================================
FieldEffects.register(:SNOWY_MOUNTAIN, (lambda do
  winds = [:GUST, :TWISTER, :RAZORWIND, :AIRCUTTER, :HURRICANE, :ICYWIND, :OMINOUSWIND, :SILVERWIND,
           :FAIRYWIND, :HEATWAVE, :PETALBLIZZARD, :BLIZZARD, :BLEAKWINDSTORM, :WILDBOLTSTORM,
           :SANDSEARSTORM, :SPRINGTIDESTORM, :MOUNTAINGALE]
  {
    :name          => "Snowy Mountain",
    :backdrop      => "field_snowy_mountain",
    :intro_message => "A blizzard rages over the snowbound peak!",
    :description   => "Ice and wind rule the summit; fire is dulled. Snow abilities work without hail. Big fire attacks melt it back to bare rock.",
    :notes         => ["Boosted: Ice x1.5, Rock and Flying x1.2, wind moves x1.3. Weakened: Fire x0.75.",
                       "Powder Snow x2; Avalanche, Ice Ball, Rollout x1.5. Blizzard never misses.",
                       "Ice types take less from physical attacks (x1.5 Defense).",
                       "Slush Rush, Snow Cloak and Ice Body work without hail. Hail lasts 3 turns longer.",
                       "2 big fire moves, or sunlight, melt it into a Mountain."],
    :nature_power  => :AVALANCHE,
    :camouflage    => :ICE,
    :secret_power  => 9,
    :type_mods     => { :ICE => 1.5, :ROCK => 1.2, :FLYING => 1.2, :FIRE => 0.75 },
    :type_messages => { :ICE  => "The frigid peak sharpened the cold!",
                        :FIRE => "The bitter cold dulled the flames..." },
    :move_mods     => { :POWDERSNOW => 2.0, :AVALANCHE => 1.5, :ICEBALL => 1.5, :ROLLOUT => 1.5 },
    :move_messages => { :AVALANCHE  => "An avalanche thundered down the slope!",
                        :ICEBALL    => "The snowball grew as it rolled!",
                        :ROLLOUT    => "{1} gathered snow as it rolled!",
                        :POWDERSNOW => "{1} kicked up a snowdrift!" },
    :damage_mods   => [
      { :moves => winds, :mult => 1.3, :message => "The freezing gale howled behind {2}!" },
      { :category => :physical, :target => { :types => [:ICE] }, :defense_mult => 1.5 }
    ],
    :accuracy_mods => [
      { :moves => [:BLIZZARD], :always_hit => true },
      { :target => { :abilities => [:SNOWCLOAK] }, :evasion_mult => 1.25 }
    ],
    :speed_mods    => [{ :battlers => { :abilities => [:SLUSHRUSH] }, :mult => 2.0 }],
    :on_entry      => [
      { :battlers => { :abilities => [:WINDRIDER] }, :stats => { :ATTACK => 1 }, :also_on_change => true,
        :message => "{1} rode the freezing winds!" },
      { :battlers => { :abilities => [:WINDPOWER] }, :effects => [:charge], :also_on_change => true }
    ],
    :end_of_round  => [
      { :battlers => { :abilities => [:ICEBODY] }, :heal => 1/16r, :message => "{1} absorbed the falling snow." },
      { :battlers => { :grounded => true, :status => [:BURN] }, :cure_status => true,
        :message => "The deep snow soothed {1}'s burn!" }
    ],
    :weather       => { :extend => { :Hail => 3 } },
    :transitions   => [
      { :weather => [:Sun, :HarshSun], :to => :MOUNTAIN, :message => "The sun melted the snow from the slopes!" },
      { :moves => [:HEATWAVE, :ERUPTION, :LAVAPLUME, :FIREPLEDGE, :BLASTBURN, :MAGMASTORM, :INFERNO,
                   :OVERHEAT, :SEARINGSHOT, :BLUEFLARE, :FUSIONFLARE, :MINDBLOWN],
        :to => :MOUNTAIN, :uses => 2,
        :progress_message => "The snow is melting... ({1} more)",
        :message => "The snow melted away, baring the rocky slopes!" }
    ],
    :seed => { :item => :TELLURICSEED, :stats => { :DEFENSE => 1 }, :effects => [:defense_curl],
               :message => "{1}'s {2} packed it in a shell of snow!" }
  }
end).call)
