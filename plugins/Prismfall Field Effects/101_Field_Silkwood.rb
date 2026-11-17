#===============================================================================
# SILKWOOD - Gym 1 (Bug), Briarwick. Ancient trees strung with giant silk webs.
# Bugs ride the silk currents, the threads carry electricity (Electroweb!), and
# fire races along them: 3 fire attacks (2 in sunlight) set it ablaze (WILDFIRE).
# Family: Telluric.
#===============================================================================
FieldEffects.register(:SILKWOOD, (lambda do
  blades = [:CUT, :FURYCUTTER, :SLASH, :NIGHTSLASH, :LEAFBLADE, :XSCISSOR, :AIRSLASH, :PSYCHOCUT,
            :CROSSPOISON, :SACREDSWORD, :RAZORSHELL, :SOLARBLADE, :STONEAXE, :AQUACUTTER, :BITTERBLADE,
            :KOWTOWCLEAVE, :PSYBLADE]
  {
    :name          => "Silkwood",
    :backdrop      => "field_silkwood",
    :family        => :telluric,
    :intro_message => "Giant webs glisten between the ancient trees...",
    :description   => "Bugs ride the silk, the threads carry current, blades cut paths and fire races along the webs.",
    :notes         => ["Bug x1.5, Grass x1.2, Fire x1.2. Swarm and Overgrow are always active.",
                       "Electroweb x1.5 and never misses: the current runs along the threads (30% paralysis). In rain every Electric move rides the wet silk (x1.2).",
                       "Attack Order, Struggle Bug, Silver Wind x1.5; Lunge, Leech Life, Pounce, Fell Stinger, First Impression x1.3.",
                       "Blades (Cut, X-Scissor, Leaf Blade...) x1.2. Bug-type fliers glide on the silk (Flying x1.2); other fliers weave through it (x0.8).",
                       "Bug contact moves may wrap the target in silk (Speed -1). Bug moves' own added effects are twice as likely.",
                       "String Shot, Electroweb, Sticky Web never miss; String Shot and Silk Trap bind tighter; Defend Order +1 Def more.",
                       "Grounded non-Bug Pokemon step into fresh silk the first time they enter (Speed -1; Heavy-Duty Boots avoid it).",
                       "Bug types sip nectar each turn (1/16 HP). Grassy Terrain +3 turns, Electric Terrain +2 (the webs hold the charge).",
                       "Fire races along the silk: 3 damaging Fire moves (2 in sunlight) set it ablaze -> Wildfire.",
                       "Telluric Seed: +1 Defense, +1 Sp. Def, but the cocoon slows it (-1 Speed)."],
    :nature_power  => :BUGBUZZ,
    :camouflage    => :BUG,
    :secret_power  => 4,
    :activate_abilities => [:SWARM, :OVERGROW],
    :type_mods     => { :BUG => 1.5, :GRASS => 1.2, :FIRE => 1.2 },
    :type_messages => { :BUG  => "The whole canopy thrummed with {1}'s swarm!",
                        :FIRE => "The flames raced along the silk!" },
    :move_mods     => { :ELECTROWEB => 1.5, :ATTACKORDER => 1.5, :STRUGGLEBUG => 1.5, :SILVERWIND => 1.5,
                        :LUNGE => 1.3, :LEECHLIFE => 1.3, :POUNCE => 1.3, :FELLSTINGER => 1.3,
                        :FIRSTIMPRESSION => 1.3 },
    :move_messages => { :ELECTROWEB      => "The current raced along the silk threads!",
                        :ATTACKORDER     => "Every bug in the canopy answered {1}'s call!",
                        :SILVERWIND      => "{1} rode a current of silk and scales!",
                        :FIRSTIMPRESSION => "{1} dropped from the canopy on a silk line!",
                        :LUNGE           => "{1} swung in on a strand of silk!" },
    :damage_mods   => [
      { :moves => blades, :mult => 1.2, :message => "{2} sliced a path through the silk!" },
      { :types => [:FLYING], :category => :damaging, :user => { :types => [:BUG] }, :mult => 1.2,
        :message => "{1} glided along the silk lines!" },
      { :types => [:FLYING], :category => :damaging, :user => { :not_types => [:BUG] }, :mult => 0.8,
        :message => "{1} had to weave between the strands..." },
      # Rain beads on the webs and every thread becomes a wire
      { :types => [:ELECTRIC], :category => :damaging, :in_weather => [:Rain, :HeavyRain], :mult => 1.2,
        :message => "The rain-soaked silk carried the current everywhere!" }
    ],
    :accuracy_mods => [
      { :moves => [:STRINGSHOT, :ELECTROWEB, :STICKYWEB], :always_hit => true },
      { :flags => ["Powder"], :mult => 1.2 },
      { :user => { :abilities => [:COMPOUNDEYES] }, :mult => 1.1 }
    ],
    :effect_chance_mods => [{ :types => [:BUG], :mult => 2.0 }],
    :added_effects => [
      { :moves => [:ELECTROWEB], :chance => 30, :status => :PARALYSIS,
        :message => "The charged threads locked {1} in place!" },
      { :types => [:BUG], :flags => ["Contact"], :category => :damaging, :chance => 20, :stats => { :SPEED => -1 },
        :message => "{1} was wrapped in fresh silk!" }
    ],
    :move_stat_boosts => [
      { :moves => [:STRINGSHOT, :SILKTRAP], :target_stats => { :SPEED => -1 }, :message => "The webs wound tighter!" },
      { :moves => [:DEFENDORDER], :user_stats => { :DEFENSE => 1 }, :message => "The swarm reinforced {1}!" },
      { :moves => [:STICKYWEB], :user_stats => { :SPEED => 1 }, :message => "{1} scuttled across its new web!" }
    ],
    :on_entry      => [
      # Gym 1 tuning: each Pokemon steps into fresh silk only the FIRST time it enters this battle.
      { :battlers => { :grounded => true, :not_types => [:BUG], :not_items => [:HEAVYDUTYBOOTS],
                       :condition => proc { |battle, battler|
                         seen = battle.instance_variable_get(:@pf_silkwood_webbed) ||
                                battle.instance_variable_set(:@pf_silkwood_webbed, {})
                         key = battler.pokemon ? battler.pokemon.personalID : nil
                         next false if key.nil? || seen[[battler.index & 1, key]]
                         seen[[battler.index & 1, key]] = true
                         next true
                       } },
        :stats => { :SPEED => -1 }, :message => "{1} stepped into a curtain of sticky silk!" }
    ],
    :end_of_round  => [
      { :battlers => { :types => [:BUG] }, :heal => 1/16r, :message => "{1} sipped nectar from the silk-hung blossoms." }
    ],
    :terrain       => { :extend => { :Grassy => 3, :Electric => 2 } },
    :transitions   => [
      { :types => [:FIRE], :category => :damaging, :to => :WILDFIRE, :uses => 3,
        :condition => proc { |battle, user, target, move, type| ![:Sun, :HarshSun].include?(battle.pbWeather) },
        :progress_message => "Embers are catching in the silk... ({1} more)",
        :message => "The silk caught! Flames leap from web to web - the Silkwood is ablaze!" },
      { :types => [:FIRE], :category => :damaging, :in_weather => [:Sun, :HarshSun], :to => :WILDFIRE, :uses => 2,
        :progress_message => "The sun-dried silk is smouldering... ({1} more)",
        :message => "The sun-dried silk went up in a flash - the Silkwood is ablaze!" }
    ],
    :seed => { :item => :TELLURICSEED, :stats => { :DEFENSE => 1, :SPECIAL_DEFENSE => 1, :SPEED => -1 },
               :message => "{1}'s {2} spun a silk cocoon around it!" }
  }
end).call)
