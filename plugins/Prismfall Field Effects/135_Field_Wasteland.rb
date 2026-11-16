#===============================================================================
# WASTELAND - Bleed-scarred badlands: slag heaps, dead trees, a jaundiced sky.
# Also what CORROSIVE_MIRE becomes when it burns. Life (Grassy Terrain) ->
# FLOWER_GARDEN; Purify x2 -> no field.
# (Helpers inside the lambda so they don't leak into TOPLEVEL_BINDING.)
#===============================================================================
FieldEffects.register(:WASTELAND, (lambda do
  shard_types = [:NORMAL, :FIRE, :WATER, :GRASS, :ELECTRIC, :ICE, :FIGHTING, :POISON, :GROUND,
                 :FLYING, :PSYCHIC, :BUG, :ROCK, :GHOST, :DRAGON, :DARK, :STEEL, :FAIRY]
  {
    :name          => "Wasteland",
    :backdrop      => "field_wasteland",
    :intro_message => "Poisoned slag and dead trees stretch to a jaundiced horizon...",
    :description   => "Bleed-scarred badlands. Grime and fumes thrive, hazards turn vicious, rain burns, and the sickly sky gives no light to heal by.",
    :notes         => ["Boosted: Poison x1.2, Sludge, Octazooka, Mud Bomb x1.5, Gunk Shot x1.3, Spit Up x2.",
                       "Explosion-type moves x1.3 (trapped fumes). Weakened: Grass x0.75.",
                       "Synthesis, Morning Sun and Moonlight fail.",
                       "Stealth Rock adds a shard of a random type; Toxic Spikes also corrode on entry.",
                       "Rain is acidic: non-Poison/Steel Pokémon lose 1/16 HP each turn.",
                       "Grassy Terrain revives it into a Flower Garden. 2 uses of Purify cleanse it."],
    :nature_power  => :GUNKSHOT,
    :camouflage    => :POISON,
    :secret_power  => 4,
    :type_mods     => { :POISON => 1.2, :GRASS => 0.75 },
    :type_messages => { :POISON => "Toxic slag bubbled up from the ground!",
                        :GRASS  => "The blighted soil sapped the plant life..." },
    :move_mods     => { :SLUDGE => 1.5, :OCTAZOOKA => 1.5, :MUDBOMB => 1.5, :GUNKSHOT => 1.3, :SPITUP => 2.0,
                        :BELCH => 1.3, :EXPLOSION => 1.3, :SELFDESTRUCT => 1.3, :MINDBLOWN => 1.3,
                        :MISTYEXPLOSION => 1.3 },
    :move_messages => { :SPITUP       => "{1} spat up a mouthful of slag!",
                        :EXPLOSION    => "The trapped fumes amplified the blast!",
                        :SELFDESTRUCT => "The trapped fumes amplified the blast!",
                        :MINDBLOWN    => "The trapped fumes amplified the blast!" },
    :move_fails    => [
      { :moves => [:SYNTHESIS, :MORNINGSUN, :MOONLIGHT],
        :message => "The jaundiced sky gives no light to draw on!" }
    ],
    :on_entry      => [
      # Imprint shards: Stealth Rock carries a splinter of a random type
      { :battlers => { :not_items => [:HEAVYDUTYBOOTS],
                       :condition => proc { |battle, b| b.pbOwnSide.effects[PBEffects::StealthRock] } },
        :proc => proc { |battle, b|
          t = shard_types[battle.pbRandom(shard_types.length)]
          FieldEffects.apply_battler_effect(battle, b, { :damage => 1/16r, :damage_type => t,
                                                         :message => "An Imprint shard flared with {2} energy as it struck {1}!" },
                                            GameData::Type.get(t).name)
        } },
      { :battlers => { :grounded => true, :not_items => [:HEAVYDUTYBOOTS],
                       :condition => proc { |battle, b| b.pbOwnSide.effects[PBEffects::ToxicSpikes] > 0 } },
        :damage => 1/16r, :damage_type => :POISON, :message => "The corroded spikes ate into {1}!" }
    ],
    :end_of_round  => [
      { :battlers => { :not_types => [:POISON, :STEEL], :not_abilities => [:OVERCOAT],
                       :condition => proc { |battle, b| [:Rain, :HeavyRain].include?(battle.pbWeather) } },
        :damage => 1/16r, :message => "The acid rain burned {1}!" },
      { :battlers => { :abilities => [:POISONHEAL], :status => [:POISON] }, :heal => 1/16r,
        :message => "{1} thrived on the toxic wastes." }
    ],
    :weather       => { :extend => { :Sandstorm => 3 } },
    :transitions   => [
      { :terrain => [:Grassy], :to => :FLOWER_GARDEN,
        :message => "Life took root in the blighted soil! Buds push up through the slag!" },
      { :moves => [:PURIFY], :even_if_failed => true, :to => :NONE, :uses => 2,
        :progress_message => "The blight is lifting... ({1} more)",
        :message => "The blight lifted, and the land could breathe again." }
    ],
    :seed => { :item => :TELLURICSEED, :stats => { :ATTACK => 1, :SPECIAL_ATTACK => 1 }, :status => :TOXIC,
               :message => "{1}'s {2} drew power from the tainted ground!" }
  }
end).call)
