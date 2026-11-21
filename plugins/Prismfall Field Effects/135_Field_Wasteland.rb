#===============================================================================
# WASTELAND - Bleed-scarred badlands: slag heaps, dead trees, a jaundiced sky.
# Also what CORROSIVE_MIRE becomes when its gas burns off and what a SCRAPYARD
# becomes when its chemicals leach out. Grime-dwellers thrive: sludge carries
# strange afflictions, hazards splinter into Imprint shards, tough weeds whip.
# Life returns as grass first: Grassy Terrain or Purify x2 -> MEADOW (Rev 24
# audit: it was Grassy Terrain -> FLOWER_GARDEN, a tended garden out of slag).
# Family: Telluric.
# (Helpers inside the lambda so they don't leak into TOPLEVEL_BINDING.)
#===============================================================================
FieldEffects.register(:WASTELAND, (lambda do
  shard_types = [:NORMAL, :FIRE, :WATER, :GRASS, :ELECTRIC, :ICE, :FIGHTING, :POISON, :GROUND,
                 :FLYING, :PSYCHIC, :BUG, :ROCK, :GHOST, :DRAGON, :DARK, :STEEL, :FAIRY]
  sludges = [:SLUDGE, :SLUDGEBOMB, :SLUDGEWAVE, :GUNKSHOT, :OCTAZOOKA]
  {
    :name          => "Wasteland",
    :backdrop      => "field_wasteland",
    :family        => :telluric,
    :intro_message => "Poisoned slag and dead trees stretch to a jaundiced horizon...",
    :description   => "Bleed-scarred badlands where grime-dwellers thrive: sludge carries strange afflictions, hazards splinter into Imprint shards, acid rain stings, and tough weeds whip through the slag.",
    :notes         => ["Poison x1.2 (x1.5 in acid rain). Sludge, Octazooka, Mud Bomb x1.5; Gunk Shot, Belch x1.3; Sludge Bomb, Sludge Wave x1.2; Spit Up x2.",
                       "The slag carries something nasty: Sludge, Sludge Bomb, Sludge Wave, Gunk Shot and Octazooka may inflict a random status (20%).",
                       "Weeds of the waste: Vine Whip and Power Whip x1.5. Explosion-type moves x1.3 (trapped fumes). Quakes x0.5 (the slag soaks them up).",
                       "Toxic Boost is always active. Poison Heal draws 1/16 HP more from the waste each turn while poisoned.",
                       "Synthesis, Morning Sun and Moonlight fail under the jaundiced sky.",
                       "Hazards splinter: Stealth Rock adds an Imprint shard of a random type (1/16, scaled by that type); Toxic Spikes also eat into grounded Pokemon (1/16 Poison-scaled). Heavy-Duty Boots protect.",
                       "Sandstorm lasts 3 turns longer.",
                       "Life returns: Grassy Terrain, or 2 Purify (they count even if they fail) -> Meadow.",
                       "Telluric Seed: +1 Attack and +1 Sp. Atk, but the holder is badly poisoned (great on Poison types and Poison Heal)."],
    :nature_power  => :GUNKSHOT,
    :camouflage    => :POISON,
    :secret_power  => 4,
    :activate_abilities => [:TOXICBOOST],
    :type_mods     => { :POISON => 1.2 },
    :type_messages => { :POISON => "Toxic slag bubbled up with {2}!" },
    :move_mods     => { :SLUDGE => 1.5, :OCTAZOOKA => 1.5, :MUDBOMB => 1.5, :GUNKSHOT => 1.3, :BELCH => 1.3,
                        :SLUDGEBOMB => 1.2, :SLUDGEWAVE => 1.2, :SPITUP => 2.0, :VINEWHIP => 1.5, :POWERWHIP => 1.5,
                        :EXPLOSION => 1.3, :SELFDESTRUCT => 1.3, :MINDBLOWN => 1.3, :MISTYEXPLOSION => 1.3 },
    :move_messages => { :SPITUP       => "{1} spat up a mouthful of slag!",
                        :VINEWHIP     => "Tough weeds of the waste lashed out!",
                        :POWERWHIP    => "Tough weeds of the waste lashed out!",
                        :EXPLOSION    => "The trapped fumes amplified the blast!",
                        :SELFDESTRUCT => "The trapped fumes amplified the blast!",
                        :MINDBLOWN    => "The trapped fumes amplified the blast!" },
    :damage_mods   => [
      { :types => [:POISON], :category => :damaging, :in_weather => [:Rain, :HeavyRain], :mult => 1.25,
        :message => "The acid rain lent its sting to {2}!" },
      { :moves => [:EARTHQUAKE, :MAGNITUDE, :BULLDOZE], :mult => 0.5, :message => "The slag heaps soaked up the shock..." }
    ],
    :added_effects => [
      { :moves => sludges, :chance => 20, :proc => proc { |battle, user, target, move|
          st = [:BURN, :PARALYSIS, :SLEEP, :POISON, :FROZEN][battle.pbRandom(5)]
          next if !FieldEffects.can_inflict_status?(target, st, user, move)
          FieldEffects.inflict_status(target, st, user, nil)
        } }
    ],
    :move_fails    => [
      { :moves => [:SYNTHESIS, :MORNINGSUN, :MOONLIGHT], :message => "The jaundiced sky gives no light to draw on!" }
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
      { :battlers => { :abilities => [:POISONHEAL], :status => [:POISON] }, :heal => 1/16r,
        :message => "{1} thrived on the toxic wastes." }
    ],
    :weather       => { :extend => { :Sandstorm => 3 } },
    :transitions   => [
      { :terrain => [:Grassy], :to => :MEADOW,
        :message => "Grass took root in the blighted soil and spread across the slag! Life returns!" },
      { :moves => [:PURIFY], :even_if_failed => true, :to => :MEADOW, :uses => 2,
        :progress_message => "The blight is lifting... ({1} more)",
        :message => "The blight lifted! Grass ripples across land that can breathe again!" }
    ],
    :seed => { :item => :TELLURICSEED, :stats => { :ATTACK => 1, :SPECIAL_ATTACK => 1 }, :status => :TOXIC,
               :message => "{1}'s {2} drew power from the tainted ground!" }
  }
end).call)
