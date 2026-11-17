#===============================================================================
# SNOWY_MOUNTAIN - Isenmar's frozen summits. Ice Pokemon ride the blizzard,
# boulders come down frozen, snowballs grow as they roll. Big fire or sunlight
# melts it to bare rock (MOUNTAIN); an eruption blows the snowcap off
# (VOLCANIC). Family: Telluric.
# (Helpers inside the lambda so they don't leak into TOPLEVEL_BINDING.)
#===============================================================================
FieldEffects.register(:SNOWY_MOUNTAIN, (lambda do
  winds = [:GUST, :TWISTER, :RAZORWIND, :AIRCUTTER, :HURRICANE, :ICYWIND, :OMINOUSWIND, :SILVERWIND,
           :FAIRYWIND, :HEATWAVE, :PETALBLIZZARD, :BLIZZARD, :BLEAKWINDSTORM, :WILDBOLTSTORM,
           :SANDSEARSTORM, :SPRINGTIDESTORM, :MOUNTAINGALE]
  melt  = [:HEATWAVE, :LAVAPLUME, :FIREPLEDGE, :BLASTBURN, :INFERNO, :OVERHEAT, :SEARINGSHOT, :BLUEFLARE,
           :FUSIONFLARE, :MINDBLOWN, :BURNUP, :RAGINGFURY]
  {
    :name          => "Snowy Mountain",
    :backdrop      => "field_snowy_mountain",
    :family        => :telluric,
    :intro_message => "A blizzard rages over the snowbound peak!",
    :description   => "Ice Pokemon ride the blizzard: snow abilities always work, boulders freeze, snowballs grow as they roll, Ice types shrug off blows. Big fire or sunlight melts it back to bare rock.",
    :notes         => ["Ice x1.5, Rock and Flying x1.2, wind moves x1.3. Fire x0.75 (the cold dulls it).",
                       "Rock moves come down frozen (also Ice).",
                       "Powder Snow x2; Icy Wind, Avalanche, Ice Ball, Rollout and throws (Vital/Circle/Storm Throw) x1.5; Glaciate, Mountain Gale, Bitter Malice x1.3.",
                       "Ice types take less from physical attacks (x0.67). Blizzard and Thunder never miss.",
                       "Slush Rush, Snow Cloak and Ice Body work without hail. Hail lasts 3 turns longer; Aurora Veil works without hail. Tailwind lasts 2 turns longer.",
                       "On entry: Wind Rider +1 Attack, Wind Power charged. The deep snow soothes grounded Pokemon's burns each turn.",
                       "Sun, or 2 big fire moves (Heat Wave, Lava Plume, Blast Burn, Inferno, Overheat, Blue Flare, Fusion Flare...) -> Mountain. 2 of Eruption or Magma Storm -> Volcanic Field.",
                       "Telluric Seed: +1 Defense and Defense Curl (pair it with Ice Ball or Rollout)."],
    :nature_power  => :AVALANCHE,
    :camouflage    => :ICE,
    :secret_power  => 9,
    :activate_abilities => [:SLUSHRUSH, :SNOWCLOAK, :ICEBODY],
    :type_mods     => { :ICE => 1.5, :ROCK => 1.2, :FLYING => 1.2, :FIRE => 0.75 },
    :type_messages => { :ICE  => "{1} rode the blizzard into the attack!",
                        :FIRE => "The bitter cold dulled the flames..." },
    :move_mods     => { :POWDERSNOW => 2.0, :ICYWIND => 1.5, :AVALANCHE => 1.5, :ICEBALL => 1.5, :ROLLOUT => 1.5,
                        :VITALTHROW => 1.5, :CIRCLETHROW => 1.5, :STORMTHROW => 1.5, :GLACIATE => 1.3,
                        :MOUNTAINGALE => 1.3, :BITTERMALICE => 1.3 },
    :move_messages => { :AVALANCHE  => "An avalanche thundered down the slope!",
                        :ICEBALL    => "The snowball grew as it rolled!",
                        :ROLLOUT    => "{1} gathered snow as it rolled!",
                        :POWDERSNOW => "{1} kicked up a whole snowdrift!",
                        :CIRCLETHROW => "{1} sent its foe tumbling into a snowdrift!" },
    :extra_types   => [
      { :types => [:ROCK], :category => :damaging, :add => :ICE, :message => "The boulders came down frozen solid!" }
    ],
    :damage_mods   => [
      { :moves => winds, :category => :damaging, :mult => 1.3, :message => "The freezing gale howled behind {2}!" },
      { :category => :physical, :target => { :types => [:ICE] }, :defense_mult => 1.5 }
    ],
    :accuracy_mods => [{ :moves => [:BLIZZARD, :THUNDER], :always_hit => true }],
    :effect_durations => { :TAILWIND => [2, "The freezing gale strengthened the Tailwind!"] },
    :on_entry      => [
      { :battlers => { :abilities => [:WINDRIDER] }, :stats => { :ATTACK => 1 }, :also_on_change => true,
        :message => "{1} rode the freezing winds!" },
      { :battlers => { :abilities => [:WINDPOWER] }, :effects => [:charge], :also_on_change => true }
    ],
    :end_of_round  => [
      { :battlers => { :grounded => true, :status => [:BURN] }, :cure_status => true,
        :message => "The deep snow soothed {1}'s burn!" }
    ],
    :weather       => { :extend => { :Hail => 3 } },
    :weather_as    => [{ :moves => [:AURORAVEIL], :as => :Hail }],
    :transitions   => [
      { :moves => [:ERUPTION, :MAGMASTORM], :to => :VOLCANIC, :uses => 2,
        :progress_message => "The snowcap trembles... ({1} more)",
        :message => "The peak erupted, blasting the snow away! Magma pours down the slopes!" },
      { :weather => [:Sun, :HarshSun], :to => :MOUNTAIN, :message => "The sun melted the snow from the slopes!" },
      { :moves => melt, :to => :MOUNTAIN, :uses => 2,
        :progress_message => "The snow is melting... ({1} more)",
        :message => "The snow melted away, baring the rocky slopes!" }
    ],
    :seed => { :item => :TELLURICSEED, :stats => { :DEFENSE => 1 }, :effects => [:defense_curl],
               :message => "{1}'s {2} packed it in a shell of snow!" }
  }
end).call)
