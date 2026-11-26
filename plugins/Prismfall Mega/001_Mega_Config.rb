#===============================================================================
# Prismfall Mega - 001 Config (SPINE Revision 20)
#-------------------------------------------------------------------------------
# Mega Evolution is Essentials v21.1's own (Battle#pbMegaEvolve, the Mega Ring
# item flag "MegaRing", MegaStone in pokemon_forms.txt) and Elite Battle DX's own
# (the Fight-menu Mega button, the MEGAEVOLUTION / MEGAEVOLUTION2 animations).
# This plugin adds only what Prismfall needs on top (design/MEGA_EVOLUTION.md):
#   * one Mega per TRAINER per battle (Essentials' own rule, restored 2026-11-25:
#     gemini_recommends/REVIEW.md, acts-3-to-5 audit 1.5; in a tag battle each
#     trainer with a ring and a stone Mega Evolves once, a registered partner
#     included: 002 carries the partner's ring into the battle). Z-moves stay one
#     per SIDE (plugins/Prismfall Z-Power is per trainer on its own);
#     a Mega and a Z-move may both be used in one battle
#   * a Pokemon holding a Z-crystal can't Mega Evolve (Gen 7 rule; matters only
#     for stone-less Megas such as Rayquaza's)
#   * field interactions: the field's ability-keyed entry effects fire for the
#     ability a Pokemon gains by Mega Evolving (Reborn re-runs switch-in
#     abilities on Mega Evolution), plus a few Mega showpieces (FIELD_RULES)
#   * the stone distribution (STONES), the story helpers and the Field Notes lines
# Events: :prismfall_mega_evolved (battle, battler, old_ability_id)
#===============================================================================
module PrismfallMega
  RING = :MEGARING          # the base project's Mega Ring (Flags = KeyItem,MegaRing). Bastian gives it in Chapter 14.
                            # SPINE Rev 23: the same ring wakes Z-crystals (PrismfallZ::RING is this item too).
  # The Ring beat (SPINE Revision 21, "like Reborn and Rejuvenation": Reborn's Mega-Z Ring after Badge 13 at the
  # earliest, Rejuvenation's at about 14): Cragholm, after Gym 13 (cap 63, before Gym 14). Quest OS_RING_DAY.
  RING_BADGES = 13

  # :trainer = one Mega per trainer per battle (Essentials' rule; Prismfall's since 2026-11-25, so both trainers of a
  # tag pair can Mega: every Ch21 tag foe is written with one). :side = one per side (the SPINE Rev 20 rule, kept
  # switchable: tools/harness/run_mega.rb checks both).
  LIMIT = :trainer
  # The same limit for Z-moves, applied to Prismfall Z-Power's owner key (it is per trainer on its own).
  Z_LIMIT = :side
  Z_CRYSTAL_BLOCKS_MEGA = true

  # SPINE Revision 21: from an ace level of about 50 (Gym 10, cap 51) every important story fight has a Mega, any tier,
  # if the story gives that fighter a ring (Wardens, Valen, Meridian, Juno; MEGA_EVOLUTION.md 1.2 and 6.3). Below that a
  # fight may use one only if its design calls for it, and only a WEAK Mega (6.1): Brann's Camerupt, kept as designed.
  # tools/trainer_gen/gen.py applies the same two constants; tools/harness/run_mega.rb checks pbs/trainers.txt for them.
  MEGA_FULL_LEVEL = 50
  WEAK_STONES = [:CAMERUPTITE, :GLALITITE, :ABOMASITE, :BANETTITE, :AUDINITE, :STEELIXITE, :PIDGEOTITE, :BEEDRILLITE,
                 :SABLENITE, :AMPHAROSITE, :MANECTITE, :HOUNDOOMINITE, :ABSOLITE, :SHARPEDONITE].freeze

  # Kestrel (design/MEGA_EVOLUTION.md 1.2): no ring of his own until Morwen's Ring reaches him through the PC. If the PC
  # gives it to him in Ch18 (choice :ch18_kestrel_ring = :give_now), his K8 trainer gets the ring at battle start and his
  # Scizor (his duelist since K3) the Scizorite. (Given at the SF instead, after K8, it first shows in the hijack tag
  # battle on the player's side, where he and the player can both Mega (one per trainer); K9 only happens when he never
  # got it.)
  MORWEN_RING_CHOICE = [:ch18_kestrel_ring, :give_now]
  MORWEN_RING = { :trainer => :RIVAL_KESTREL, :species => :SCIZOR, :item => :SCIZORITE, :min_level => 90 }.freeze

  # Shown once when the player picks up a Z-crystal before the Ring.
  CRYSTAL_TEASER_TEXT = "The crystal is cold, and it rings very faintly against your fingers... then it falls silent, as if listening for something."
  # Shown once when the player picks up a Mega Stone before the Ring (13 badges).
  TEASER_TEXT = "The stone is warm, and it hums faintly in your hand... then goes quiet, as if it were waiting for something."

  #-----------------------------------------------------------------------------
  # Stone distribution (design/MEGA_EVOLUTION.md section 5). One entry per stone:
  #   :badges  fewest badges with which it can be obtained (map event conditions and quest unlocks enforce it)
  #   :how     :hidden, :item (visible), :quest, :rank (Trial rank reward), :boss, :puzzle, :story
  #   :map     map id (design/maps.json), :where (text), :source (quest id, Trial, event key)
  # The headless test (tools/harness/run_mega.rb) checks every entry against the Warden answers (rule R4 with the
  # Ring: a stone obtained at b badges is usable at max(b, RING_BADGES) and must not power up a type that answers
  # the next two Wardens), against the quests that hand it out, and against design/TRIAL_EVENTS.yaml ("Mega Evolution" maps).
  #-----------------------------------------------------------------------------
  STONES = {
    # Before the Ring (13 badges): "they hum and wait", as in Reborn. Only stones whose types answer neither Warden 14
    # (Ghost) nor Warden 15 (Steel) may come this early: they all become usable at 13 (SPINE Revision 21).
    :MANECTITE     => { :badges => 2,  :how => :rank,   :map => 194, :where => "The Prize Exchange, rank 3 (Fellow)", :source => :ZENITH },
    :GLALITITE     => { :badges => 2,  :how => :rank,   :map => 306, :where => "The Tally, rank 3 (Harpooner)", :source => :ISENMAR },
    :AMPHAROSITE   => { :badges => 3,  :how => :quest,  :map => 106, :where => "Ferrow Lighthouse lamp room: Hesper's lamp lens", :source => :EL_LAMP_LENS },
    :SCEPTILITE    => { :badges => 8,  :how => :item,   :map => 682, :where => "The Royal Chase, the old hunting lodge's mantel", :source => :MEGA_STONE_SCEPTILITE },
    :BLASTOISINITE => { :badges => 8,  :how => :hidden, :map => 681, :where => "Prism Falls, behind the falls (Surf)", :source => :MEGA_STONE_BLASTOISINITE },
    :VENUSAURITE   => { :badges => 9,  :how => :story,  :map => 294, :where => "The Heartgarden, Verdance: Juno, after J3", :source => :EL_BRIDE_TREE_HEART },
    :BEEDRILLITE   => { :badges => 9,  :how => :hidden, :map => 703, :where => "Gossamer Heartwood, inside the old hive", :source => :MEGA_STONE_BEEDRILLITE },
    :ALTARIANITE   => { :badges => 10, :how => :item,   :map => 732, :where => "The Tetherline, a cloud-nest on a tether pylon", :source => :MEGA_STONE_ALTARIANITE },
    :SLOWBRONITE   => { :badges => 10, :how => :hidden, :map => 723, :where => "Ebbmouth Sea Grotto, the tide-pool shelf", :source => :MEGA_STONE_SLOWBRONITE },
    :ALAKAZITE     => { :badges => 12, :how => :puzzle, :map => 345, :where => "Lucent Athenaeum, the Sealed Stacks: the Unread Shelf", :source => :MEGA_STONE_ALAKAZITE },
    :AERODACTYLITE => { :badges => 12, :how => :quest,  :map => 209, :where => "Sahar's Dig Lab, Duneholt: bring her a revived Aerodactyl", :source => :OS_AMBER_AGAIN },
    :PINSIRITE     => { :badges => 12, :how => :boss,   :map => 703, :where => "Gossamer Heartwood: the Old Pincer", :source => :EL_OLD_PINCER },
    # The Ring (13 badges): Cragholm, after Gym 13
    :AGGRONITE     => { :badges => 13, :how => :story,  :map => 363, :where => "Cragholm Lift Galleries, Bastian's lamp-room in the deep seams: with the Mega Ring", :source => :OS_RING_DAY },
    :GARDEVOIRITE  => { :badges => 13, :how => :puzzle, :map => 752, :where => "The Looking-Glass Wood, the heart of the mirror maze", :source => :MEGA_STONE_GARDEVOIRITE },
    :MAWILITE      => { :badges => 13, :how => :quest,  :map => 346, :where => "The Speculum, Lucent: the smile behind the glass (Rite of Reflection rank 2)", :source => :AN_SMILE_BEHIND_GLASS },
    :SCIZORITE     => { :badges => 13, :how => :item,   :map => 383, :where => "Vane Hall, Gravenmoor: Morwen Vane's trophy case", :source => :MEGA_STONE_SCIZORITE },
    :ABOMASITE     => { :badges => 13, :how => :hidden, :map => 701, :where => "The Hoarwood, under the frost-giant pine", :source => :MEGA_STONE_ABOMASITE },
    # 14 badges (after Ysolde): Dark, Ghost and Normal Megas no longer answer the next two Wardens
    :ABSOLITE      => { :badges => 14, :how => :hidden, :map => 801, :where => "The Slag Mesa, under the warning-cairn on the mesa's lip", :source => :MEGA_STONE_ABSOLITE },
    :SABLENITE     => { :badges => 14, :how => :hidden, :map => 804, :where => "Barrow of the Wardens, a looted grave-niche the Sableye mine for its gems", :source => :MEGA_STONE_SABLENITE },
    :BANETTITE     => { :badges => 14, :how => :quest,  :map => 547, :where => "Thistledown Manor attic: the doll who waited", :source => :EL_DOLL_WHO_WAITED },
    :PIDGEOTITE    => { :badges => 14, :how => :quest,  :map => 325, :where => "Gale Post Hall, Skyreach: the dead-letter bag", :source => :ZE_RETURN_TO_SENDER },
    :METAGROSSITE  => { :badges => 14, :how => :puzzle, :map => 403, :where => "Strade Works Foundry Floor, the sorting-line puzzle", :source => :MEGA_STONE_METAGROSSITE },
    :GENGARITE     => { :badges => 14, :how => :item,   :map => 805, :where => "Barrow Sanctum, the altar of the nameless Warden", :source => :MEGA_STONE_GENGARITE },
    # 15 badges (after Magnus): Fire and Ground Megas
    :SHARPEDONITE  => { :badges => 15, :how => :hidden, :map => 424, :where => "Underveil Sump Docks, a harpooned Sharpedo jaw in the net-loft", :source => :MEGA_STONE_SHARPEDONITE },
    :SWAMPERTITE   => { :badges => 15, :how => :hidden, :map => 821, :where => "The Drownings, a mud-bank islet (Surf)", :source => :MEGA_STONE_SWAMPERTITE },
    :CHARIZARDITEY => { :badges => 15, :how => :hidden, :map => 832, :where => "The Brink, the wind-scoured ledge above the drop", :source => :MEGA_STONE_CHARIZARDITEY },
    :CAMERUPTITE   => { :badges => 15, :how => :quest,  :map => 244, :where => "Hearthguild Hall, Cindervault: Brann's spare", :source => :AS_FORGE_REMEMBERS },
    :CHARIZARDITEX => { :badges => 15, :how => :boss,   :map => 248, :where => "Pyre Keep Dragon Roosts: Old Cinder, a retired Legion war-Charizard", :source => :AS_OLD_CINDER },
    :GYARADOSITE   => { :badges => 15, :how => :hidden, :map => 824, :where => "Aurelia - Drowned Spires, the flooded bell (Dive)", :source => :MEGA_STONE_GYARADOSITE },
    :HOUNDOOMINITE => { :badges => 15, :how => :quest,  :map => 423, :where => "Underveil Moon Market: the Barons' kennel (Gutter Book)", :source => :NA_MOON_MARKET_DOGS },
    :TYRANITARITE  => { :badges => 15, :how => :quest,  :map => 360, :where => "Cragholm rack: the tyrant's heart (Rolls of Unearthing rank 2)", :source => :OS_TYRANT_HEART },
    :GARCHOMPITE   => { :badges => 15, :how => :hidden, :map => 810, :where => "The Dry Tide, a sand-sunk caravan", :source => :MEGA_STONE_GARCHOMPITE },
    :SALAMENCITE   => { :badges => 15, :how => :quest,  :map => 240, :where => "The Crucible, Cindervault: the brazier writ (Trial by Flames rank 2)", :source => :AS_BRAZIER_WRIT },
    :GALLADITE     => { :badges => 16, :how => :item,   :map => 841, :where => "The Gloamwood Verge, the knight's barrow", :source => :MEGA_STONE_GALLADITE },
    :MEDICHAMITE   => { :badges => 16, :how => :hidden, :map => 263, :where => "The Iron Pit, the meditation shelf above the top tier (Rock Climb)", :source => :MEGA_STONE_MEDICHAMITE },
    :HERACRONITE   => { :badges => 16, :how => :hidden, :map => 524, :where => "Gossamer Wood, the old sap tree", :source => :MEGA_STONE_HERACRONITE },
    :LOPUNNITE     => { :badges => 16, :how => :quest,  :map => 154, :where => "Pell Playhouse, the Grand Stage: Dorian's encore", :source => :EL_ENCORE },
    :KANGASKHANITE => { :badges => 16, :how => :boss,   :map => 560, :where => "Frostflat Causeway: the Causeway Matriarch", :source => :IS_CAUSEWAY_MATRIARCH },
    # 17 badges: Steel/Ground is safe only before the last Warden (Dragon)
    :STEELIXITE    => { :badges => 17, :how => :hidden, :map => 864, :where => "Wyrmscar Rift, an iron-snake's shed skin in the rift wall", :source => :MEGA_STONE_STEELIXITE },
    :BLAZIKENITE   => { :badges => 17, :how => :hidden, :map => 870, :where => "Thornwatch, the war-brazier on the gate tower", :source => :MEGA_STONE_BLAZIKENITE },
    :LUCARIONITE   => { :badges => 17, :how => :quest,  :map => 260, :where => "The Last Rung, Ironreach: the Memory Kata (Gutter Book rank 2)", :source => :NA_MEMORY_KATA },
    # Post-game (Normal/Fairy answers Ysolde, Nyx and Sigrun: Audino waits for the eighteenth badge)
    :AUDINITE      => { :badges => 18, :how => :quest,  :map => 223, :where => "Corvin Mott's Infirmary, Mirefen: Wenlow (post-game)", :source => :NA_BEDSIDE_MANNER },
    :LATIASITE     => { :badges => 18, :how => :item,   :map => 905, :where => "Shardfall Isles, the eon nest (post-game)", :source => :MEGA_STONE_LATIASITE },
    :LATIOSITE     => { :badges => 18, :how => :item,   :map => 905, :where => "Shardfall Isles, the eon nest (post-game)", :source => :MEGA_STONE_LATIOSITE }
  }.freeze
  #-----------------------------------------------------------------------------
  # Z-crystal distribution (SPINE Rev 23, design/Z_MOVES.md section 3): the same keys as STONES, the same rule R4 (the
  # crystal's type must not answer the next two Wardens when it becomes usable, at max(badges, RING_BADGES)), checked by
  # tools/harness/run_mega.rb. The Eevium Z is the Eevee Octave's reward (Ch20) and isn't listed.
  #-----------------------------------------------------------------------------
  Z_CRYSTALS = {
    # Before the Ring: they ring faintly and fall silent (CRYSTAL_TEASER_TEXT)
    :ICIUMZ      => { :badges => 2,  :how => :hidden, :map => 577, :where => "Frostwick Pass, the avalanche gully (Rock Smash)", :source => :Z_CRYSTAL_ICIUMZ },
    :STEELIUMZ   => { :badges => 4,  :how => :hidden, :map => 605, :where => "Static Tunnels Depths, the magnetite seam (Flash)", :source => :Z_CRYSTAL_STEELIUMZ },
    :ROCKIUMZ    => { :badges => 8,  :how => :hidden, :map => 685, :where => "Grudgestone Quarry B1F, the gem seam", :source => :Z_CRYSTAL_ROCKIUMZ },
    :GRASSIUMZ   => { :badges => 8,  :how => :hidden, :map => 680, :where => "The Rootdeep, a root-wrapped ledge on the underground river (Surf)", :source => :Z_CRYSTAL_GRASSIUMZ },
    :FLYINIUMZ   => { :badges => 10, :how => :hidden, :map => 726, :where => "Cloudstair Summit, the wind-scoured ledge", :source => :Z_CRYSTAL_FLYINIUMZ },
    # 13 badges: the Ring
    :PSYCHIUMZ   => { :badges => 13, :how => :hidden, :map => 781, :where => "Hindmoor, the humming standing stone", :source => :Z_CRYSTAL_PSYCHIUMZ },
    :BUGINIUMZ   => { :badges => 13, :how => :hidden, :map => 780, :where => "The Jawbone Ridge, in the resin of a dead tree", :source => :Z_CRYSTAL_BUGINIUMZ },
    :FAIRIUMZ    => { :badges => 13, :how => :hidden, :map => 785, :where => "Darkglass Mine B1F, a pink glint under the shot-out lamps", :source => :Z_CRYSTAL_FAIRIUMZ },
    :MIMIKIUMZ   => { :badges => 13, :how => :item,   :map => 384, :where => "Lantern Hospice, Gravenmoor: a Pikachu-shaped rag doll on an empty cot", :source => :Z_CRYSTAL_MIMIKIUMZ },
    # 14 badges
    :POISONIUMZ  => { :badges => 14, :how => :hidden, :map => 811, :where => "The Smokestack Parade, a soot-black vent", :source => :Z_CRYSTAL_POISONIUMZ },
    :GHOSTIUMZ   => { :badges => 14, :how => :quest,  :map => 547, :where => "Thistledown Manor attic: the doll who waited (with the Banettite)", :source => :EL_DOLL_WHO_WAITED },
    :ELECTRIUMZ  => { :badges => 14, :how => :quest,  :map => 325, :where => "Gale Post Hall, Skyreach: the dead-letter drawer (with the Pidgeotite)", :source => :ZE_RETURN_TO_SENDER },
    # 15 badges
    :FIRIUMZ     => { :badges => 15, :how => :quest,  :map => 240, :where => "The Crucible: the brazier's own sliver (with the Salamencite)", :source => :AS_BRAZIER_WRIT },
    :GROUNDIUMZ  => { :badges => 15, :how => :quest,  :map => 360, :where => "Cragholm rack: the tyrant's heart dig (with the Tyranitarite)", :source => :OS_TYRANT_HEART },
    :DARKINIUMZ  => { :badges => 15, :how => :quest,  :map => 423, :where => "Underveil Moon Market: the Barons' kennel (with the Houndoominite)", :source => :NA_MOON_MARKET_DOGS },
    :DRAGONIUMZ  => { :badges => 15, :how => :boss,   :map => 248, :where => "Pyre Keep Dragon Roosts: Old Cinder's harness (with the Charizardite X)", :source => :AS_OLD_CINDER },
    :WATERIUMZ   => { :badges => 15, :how => :hidden, :map => 822, :where => "Under the Drownings, a drowned shrine (Dive)", :source => :Z_CRYSTAL_WATERIUMZ },
    # 16-17 badges
    :NORMALIUMZ  => { :badges => 16, :how => :quest,  :map => 154, :where => "Pell Playhouse: Dorian's encore (with the Lopunnite)", :source => :EL_ENCORE },
    :SNORLIUMZ   => { :badges => 16, :how => :item,   :map => 850, :where => "Mothwell, the hay barn with a Snorlax-sized dent", :source => :Z_CRYSTAL_SNORLIUMZ },
    :FIGHTINIUMZ => { :badges => 17, :how => :quest,  :map => 260, :where => "The Last Rung, Ironreach: the Memory Kata (with the Lucarionite)", :source => :NA_MEMORY_KATA }
  }.freeze

  # In the base data but not placed: their species are not in Velmora (POKEMON_AVAILABILITY.md section 4).
  UNPLACED = [:MEWTWONITEX, :MEWTWONITEY, :DIANCITE].freeze

  #-----------------------------------------------------------------------------
  # Mega showpieces on Prismfall fields (design/MEGA_EVOLUTION.md section 3).
  # Each rule is a Field Effects battler-effect rule (FIELD_API.md 4.6: :battlers, :stats, :effects, :message,
  # :proc ...) applied to the Pokemon that has just Mega Evolved, on the CURRENT field only (Bleed and Prism
  # Arena borrowings excluded). A :proc returns true if it did something; it shows its own messages.
  #-----------------------------------------------------------------------------
  FIELD_RULES = {
    # A Mega Evolution is the biggest costume change there is: the applause rises one stage.
    :GRAND_STAGE => [
      { :proc => proc { |battle, b| PrismfallMega.raise_stage(battle, {
          2 => "A Mega Evolution! The audience gasps at the costume change!",
          3 => "The Mega Evolution brings the house down! Standing ovation!" }) } }
    ],
    # A Fire-type Mega stirs the magma: the volcano erupts at the end of the round (Volcanic's own eruption).
    :VOLCANIC => [
      { :battlers => { :types => [:FIRE] },
        :proc => proc { |battle, b| PrismfallMega.prime_volcano(battle, b) } }
    ],
    # The crowd counts a Mega Evolution like a knockout toward the Frenzy (two of them whip it up).
    :COLOSSEUM => [
      { :proc => proc { |battle, b| PrismfallMega.colosseum_roar(battle, b) } }
    ],
    # An Ice-type Mega's frost seals every crack in the lake ice.
    :FROZEN_LAKE => [
      { :battlers => { :types => [:ICE] },
        :proc => proc { |battle, b| PrismfallMega.seal_ice(battle, b) } }
    ],
    # The Mega light floods the geode: the crystals take the Mega's colour if it is one of theirs.
    :CRYSTAL_CAVERN => [
      { :proc => proc { |battle, b| PrismfallMega.flood_crystals(battle, b) } }
    ],
    # A Ghost-type Mega calls the dead back into a consecrated nave (stage 2 -> 1, Haunted).
    :HOLLOW_CATHEDRAL => [
      { :battlers => { :types => [:GHOST] },
        :proc => proc { |battle, b| PrismfallMega.rehaunt(battle, b) } }
    ],
    # The foundry hammers a Steel-type Mega's new plating home.
    :FACTORY => [
      { :battlers => { :types => [:STEEL] }, :stats => { :DEFENSE => 1 },
        :message => "The foundry hammered {1}'s new plating home!" }
    ],
    # A Mega Evolution pulls a whole Imprint into one body: the Bleed lurches to new borrowed effects at once.
    :BLEED => [
      { :proc => proc { |battle, b| PrismfallMega.lurch_bleed(battle, b) } }
    ]
  }

  # Field Notes lines (appended to the field's own notes).
  FIELD_NOTES = {
    :GRAND_STAGE      => ["Mega Evolution: the costume change raises the applause one stage."],
    :VOLCANIC         => ["Mega Evolution: a Fire-type Mega stirs the magma - the volcano erupts at the end of the round."],
    :COLOSSEUM        => ["Mega Evolution: the crowd counts it like a knockout toward the Frenzy."],
    :FROZEN_LAKE      => ["Mega Evolution: an Ice-type Mega seals every crack in the ice."],
    :CRYSTAL_CAVERN   => ["Mega Evolution: the crystals take the Mega's colour (Fire, Water, Grass or Psychic)."],
    :HOLLOW_CATHEDRAL => ["Mega Evolution: a Ghost-type Mega calls the dead back into a consecrated nave."],
    :FACTORY          => ["Mega Evolution: a Steel-type Mega's plating is hammered home (+1 Defense)."],
    :BLEED            => ["Mega Evolution: the Bleed lurches and borrows new effects at once."]
  }
  # Shown on every field's notes page: the ability a Mega gains triggers the field's entry effects.
  GENERAL_NOTE = "A Mega Evolution's new ability triggers this field's on-entry ability effects."
end
