#===============================================================================
# BLEED - Imprints spilling beyond their cities. Unstable: every few rounds it
# borrows the effects of another registered field (fields added later join the
# pool automatically). Raw Imprint energy rewards adaptable Pokemon.
# Story battles only change INTO the Bleed; it never transforms itself.
# A map can narrow what it borrows (FIELD_DEFAULTS.yaml `borrow:` ->
# MAP_BORROW_POOLS): the Steamline (925) and the Glass Dunes (926) only echo the
# war's fire, ice, sand and steam-glass fields.
# Family: Magical.
#===============================================================================
FieldEffects.register(:BLEED, {
  :name          => "The Bleed",
  :backdrop      => "field_bleed",
  :family        => :magical,
  :intro_message => "Reality frays at the edges... The Bleed is spreading!",
  :description   => "Every 3 rounds it borrows another field's effects. Raw Imprint energy rewards coverage, shapeshifters and type-shifting moves.",
  :notes         => ["Every 3 rounds (and at once) it borrows the full effects of another field at random. Borrowed fields never transform the Bleed and their seeds don't react.",
                     "Where the Fire and Ice Imprints meet (the Steamline, the Glass Dunes) it only echoes the war's own fields: Volcanic, Cinderglass, Frozen Lake, Snowy Mountain, Desert, Flooded Dunes, Glass Dunes.",
                     "Attacks that don't match the user's type x1.2 (raw Imprint energy rewards coverage).",
                     "Type-shifting moves drink the raw Imprints: Judgment, Multi-Attack, Techno Blast, Revelation Dance, Weather Ball, Terrain Pulse, Hidden Power x1.3.",
                     "Protean, Libero and Color Change Pokemon adapt fast (+1 Speed on entry). Mimicry takes the Bleed's natural type (Psychic).",
                     "End of turn: each Pokemon has a 20% chance to have its power warped - one stat +1, another -1.",
                     "Magical Seed: a random stat +2. Synthetic Seed: +1 Defense and +1 Sp. Def (insulated against the warp)."],
  :nature_power  => :TRIATTACK,
  :camouflage    => :PSYCHIC,
  :secret_power  => 4,
  :borrow        => { :pool => :all, :interval => 3, :count => 1, :order => :random,
                      :start_immediately => true,
                      :message => "The Bleed convulses... echoes of the {1} tear through the battlefield!" },
  :move_mods     => { :JUDGMENT => 1.3, :MULTIATTACK => 1.3, :TECHNOBLAST => 1.3, :REVELATIONDANCE => 1.3,
                      :WEATHERBALL => 1.3, :TERRAINPULSE => 1.3, :HIDDENPOWER => 1.3 },
  :move_messages => { :JUDGMENT    => "The raw Imprints poured into {2}!",
                      :MULTIATTACK => "The raw Imprints poured into {2}!",
                      :WEATHERBALL => "The raw Imprints poured into {2}!" },
  :damage_mods   => [
    { :category => :damaging, :mult => 1.2,
      :condition => proc { |battle, user, target, move, type| type && !user.pbHasType?(type) },
      :message => "The Bleed warped {2} into something stronger!" }
  ],
  :on_entry      => [
    { :battlers => { :abilities => [:PROTEAN, :LIBERO, :COLORCHANGE] }, :stats => { :SPEED => 1 },
      :message => "{1} adapted to the shifting Imprints!" }
  ],
  :end_of_round  => [
    { :chance => 20, :proc => proc { |battle, battler|
        stats = [:ATTACK, :DEFENSE, :SPECIAL_ATTACK, :SPECIAL_DEFENSE, :SPEED]
        up = stats.delete_at(battle.pbRandom(stats.length))
        down = stats[battle.pbRandom(stats.length)]
        battle.pbDisplay(FieldEffects.format("The Bleed warped {1}'s power!", battler.pbThis))
        FieldEffects.apply_stat_changes(battler, { up => 1, down => -1 }, nil)
        true
      } }
  ],
  :seed => [
    { :item => :MAGICALSEED, :message => "{1}'s {2} drank from the Bleed!",
      :proc => proc { |battle, battler|
        stats = [:ATTACK, :DEFENSE, :SPECIAL_ATTACK, :SPECIAL_DEFENSE, :SPEED]
        FieldEffects.apply_stat_changes(battler, { stats[battle.pbRandom(stats.length)] => 2 }, battler)
      } },
    { :item => :SYNTHETICSEED, :stats => { :DEFENSE => 1, :SPECIAL_DEFENSE => 1 },
      :message => "{1}'s {2} insulated it against the Bleed!" }
  ]
})
