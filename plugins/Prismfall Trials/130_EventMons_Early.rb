#===============================================================================
# Prismfall Trials - 130 Event Pokemon, Chapters 1-4 (implemented)
#-------------------------------------------------------------------------------
# Order follows SPINE Revision 14: Ferrow's Landing -> Saltmere (Gym 1) ->
# Briarwick (Gym 2) -> Rimewood / Frostwick -> Ebbmouth (Gym 3).
# Level caps: 15 before Gym 1, 19 before Gym 2, 23 before Gym 3, 27 before Gym 4.
#
# SPINE Revision 16 (design/DISTRIBUTION_STUDY.md, design/warden_gates.json):
#   :badges = the fewest badges with which the player can obtain the Pokemon
#   (quest unlock plus any badge gate inside the scene; the headless test
#   recomputes it from the quest data and checks the two agree). Nothing
#   obtainable with b badges may be a type answer to Warden b+1 or b+2
#   (Dorian: Fighting/Ghost; Tamsin: Fire/Flying/Rock; Marisol: Electric/Grass;
#   Rook: Ground). Strong or tailored Pokemon come after the gym they would
#   trivialise, the way Reborn hands out Numel and Onyx right after Julia.
# Full design (40+ incl. later chapters): design/EVENT_POKEMON.md (generated).
#===============================================================================
em = Prismfall::EventMons

#--- Chapter 1: Ferrow's Landing (100), the Ferrymen's Mile (520), Windfall Row (521)
em.register(:EL_NICKIT, {
  :species => :NICKIT, :level => 7, :ability => :STAKEOUT, :nature => :JOLLY, :ivs => 20,
  :moves => [:QUICKATTACK, :BEATUP, :THIEF, :TAILWHIP], :item => :ORANBERRY,
  :kind => :battle, :on_ko => :retry, :badges => 0,
  :map => 103, :where => "Tidewatch Station loft, after a chase round Ferrow's Landing", :chapter => 1,
  :quest => :EL_TART_THIEF, :trigger => "Corner it in the loft after four sightings",
  :why => "Rejuvenation's Nidoran chase: four sightings, then a fair fight. Stakeout and Thief, but Dark is no answer to Dorian"
})

em.register(:EL_SCARECROW_SPAR, {
  :species => :SUDOWOODO, :level => 10, :ability => :ROCKHEAD, :nature => :IMPISH, :ivs => 20,
  :moves => [:ROCKTHROW, :FLAIL, :FAKETEARS, :COPYCAT],
  :kind => :battle, :catchable => false, :on_ko => :retry, :badges => 0,
  :map => 521, :where => "Hale orchard, Windfall Row (the 'scarecrow')", :chapter => 1,
  :quest => :EL_SCARECROW, :trigger => "Water the scarecrow with Wenna's Squirt Bottle",
  :why => "A spar, not a catch: far too frightened to stay in a ball. Rock answers Tamsin, so it can be caught only after her badge (EL_SUDOWOODO)"
})

em.register(:EL_KECLEON, {
  :species => :KECLEON, :level => 13, :ability => :PROTEAN, :nature => :JOLLY, :ivs => 20,
  :moves => [:FURYSWIPES, :FEINT, :BIND, :THIEF],
  :kind => :battle, :on_ko => :retry, :field => :GRAND_STAGE, :badges => 0,
  :map => 145, :where => "Lantern Theatre prop room, Saltmere", :chapter => 2,
  :quest => :EL_LANTERNS, :trigger => "Spot the prop lantern that blinks",
  :why => "A search-puzzle find before Gym 1: Protean (every move gets STAB), the Lantern Theatre's quick-change co-star. No Ghost moves, so Protean can't turn it into a Normal-immune ghost"
})

#--- Chapter 2 after Badge 1 ("1 Badge Quests", Reborn-style): back along the Strand Road
em.register(:EL_TIMBURR, {
  :species => :TIMBURR, :level => 13, :ability => :GUTS, :nature => :ADAMANT, :ivs => 20, :nickname => "Plank",
  :moves => [:LOWKICK, :ROCKTHROW, :LEER, :MACHPUNCH], :obtain_text => "the empty berth, Ferrow's Landing",
  :kind => :gift, :badges => 1,
  :map => 100, :where => "The empty ferry berth, Ferrow's Landing (after Badge 1)", :chapter => 2,
  :quest => :EL_LAST_PLANK, :trigger => "Help the ferry carpenters' Timburr finish the berth it keeps mending",
  :why => "Moved after Dorian (Revision 16): Reborn's first Ground types (Numel, Onyx) come right after Julia the same way. Mach Punch (egg move) and Guts; Fighting is resisted by Tamsin's Bugs"
})

em.register(:EL_TIDE_CRABRAWLER, {
  :species => :CRABRAWLER, :level => 14, :ability => :IRONFIST, :nature => :ADAMANT, :ivs => 20,
  :moves => [:ROCKSMASH, :BUBBLE, :LEER, :POWERUPPUNCH],
  :kind => :battle, :on_ko => :retry, :field => :BEACH, :badges => 1,
  :map => 527, :where => "The big tide-pool below Lacecliff Walk (after Badge 1)", :chapter => 2,
  :quest => :EL_TIDE_POOL_FEUD, :trigger => "Side with Clobbopus in the tide-pool feud",
  :why => "A rival duel after Dorian's badge (Revision 16): Iron Fist Power-Up Punch, no use against Tamsin's Bugs"
})

em.register(:EL_TIDE_CLOBBOPUS, {
  :species => :CLOBBOPUS, :level => 14, :ability => :TECHNICIAN, :nature => :ADAMANT, :ivs => 20,
  :moves => [:ROCKSMASH, :FEINT, :BIND, :POWERUPPUNCH],
  :kind => :battle, :on_ko => :retry, :field => :BEACH, :badges => 1,
  :map => 527, :where => "The big tide-pool below Lacecliff Walk (after Badge 1)", :chapter => 2,
  :quest => :EL_TIDE_POOL_FEUD, :trigger => "Side with Crabrawler in the tide-pool feud",
  :why => "Technician (Rock Smash and Power-Up Punch at 60 power); no wild Clobbopus until the Gullcry Caves"
})

em.register(:EL_SMEARGLE, {
  :species => :SMEARGLE, :level => 14, :ability => :TECHNICIAN, :nature => :TIMID, :ivs => 20,
  :moves => [:SKETCH, :AQUAJET, :ICYWIND], :nickname => "Brush", :obtain_text => "the Lantern Theatre paint loft",
  :kind => :gift, :badges => 1,
  :variants => {
    :sea   => { :moves => [:SKETCH, :AQUAJET, :ICYWIND] },
    :night => { :moves => [:SKETCH, :ASTONISH, :CONFUSERAY] },
    :dawn  => { :moves => [:SKETCH, :FAIRYWIND, :CHARM] },
    :earth => { :moves => [:SKETCH, :MUDSLAP, :SANDATTACK] }
  },
  :map => 145, :where => "Lantern Theatre paint loft, Saltmere", :chapter => 2,
  :quest => :EL_PAINT_LOFT, :trigger => "Choose the colours of the new backdrop",
  :why => "Coverage of your choice plus Sketch and Technician; no Fire or Grass palette before Tamsin and Marisol (Revision 16)"
})

em.register(:EL_RALTS, {
  :species => :RALTS, :level => 13, :ability => :TRACE, :nature => :MODEST, :ivs => 25,
  :moves => [:CONFUSION, :DISARMINGVOICE, :DOUBLETEAM, :HYPNOSIS],
  :obtain_text => "the end of the Saltmere breakwater", :kind => :gift, :badges => 1,
  :map => 146, :where => "End of the Saltmere breakwater, at night", :chapter => 2,
  :quest => :EL_SOUND_OF_SALTMERE, :trigger => "Bring three true silences to the breakwater's end",
  :why => "A strong evolver earned by a puzzle (Gardevoir or Gallade); Psychic/Fairy is no answer to Bug or Water"
})

em.register(:EL_GLASS_PONYTA, {
  :species => :PONYTA, :form => 1, :level => 15, :ability => :PASTELVEIL, :nature => :TIMID, :ivs => 25,
  :moves => [:CONFUSION, :FAIRYWIND, :TAILWHIP, :HYPNOSIS],
  :kind => :battle, :on_ko => :retry, :field => :BLEED, :badges => 1,
  :map => 522, :where => "The Glassed Orchard, after Badge 1", :chapter => 2,
  :quest => :EL_GLASS_FOAL, :trigger => "Follow the chiming hoofprints through the glass trees",
  :why => "Galarian Ponyta (Psychic, Fairy at Rapidash): an Imprinted variant found only in the Orchard"
})

#--- Chapter 3 after Badge 2: the Gossamer (524/525), Briarwick (120)
em.register(:EL_HERACROSS, {
  :species => :HERACROSS, :level => 19, :ability => :MOXIE, :nature => :ADAMANT, :ivs => 25,
  :moves => [:FURYATTACK, :HORNATTACK, :REVENGE, :ENDURE],
  :kind => :battle, :on_ko => :retry, :field => :SILKWOOD, :badges => 2,
  :map => 524, :where => "The sap tree on the old trail, Gossamer Wood (after Badge 2)", :chapter => 3,
  :quest => :EL_HORN_AND_PINCER, :trigger => "Side with Pinsir; Heracross fights you",
  :why => "Reborn's Pinsir/Heracross duel, after Tamsin (Revision 16): a strong Bug earned by exploration. Moxie; wild ones are 3% Headbutt finds without it"
})

em.register(:EL_PINSIR, {
  :species => :PINSIR, :level => 19, :ability => :MOXIE, :nature => :ADAMANT, :ivs => 25,
  :moves => [:VISEGRIP, :BIND, :SEISMICTOSS, :BUGBITE],
  :kind => :battle, :on_ko => :retry, :field => :SILKWOOD, :badges => 2,
  :map => 524, :where => "The sap tree on the old trail, Gossamer Wood (after Badge 2)", :chapter => 3,
  :quest => :EL_HORN_AND_PINCER, :trigger => "Side with Heracross; Pinsir fights you",
  :why => "Moxie Pinsir with Seismic Toss (fixed damage through any field)"
})

em.register(:EL_SPIDOPS, {
  :species => :SPIDOPS, :level => 20, :ability => :STAKEOUT, :nature => :IMPISH, :ivs => 25, :nickname => "Silkthief",
  :moves => [:SILKTRAP, :BUGBITE, :FEINT, :ASSURANCE],
  :kind => :boss, :field => :SILKWOOD, :badges => 2,
  :boss => { :bars => { :CASUAL => 1, :STANDARD => 2, :HARD => 2, :default => 2 },
             :stat_mults => { :HP => 1.15, :DEFENSE => 1.1 },
             :intro => "The Silkthief drops from the canopy on a rope of stolen silk!",
             :breaks => { 1 => { :message => "{1} spins a fresh trap from the stolen thread!", :stats => { :DEFENSE => 1 } } } },
  :joins => { :level => 18 }, :join_choice => true,
  :map => 525, :where => "Gossamer Deepwood, the moth nests (Cut, after Tamsin's badge)", :chapter => 3,
  :quest => :EL_SILKTHIEF, :trigger => "Beat the boss, then choose to take it or leave it guarding the nests",
  :why => "Rejuvenation-style boss reward: Spidops with Stakeout and its signature Silk Trap"
})

#--- Chapter 4 (Badge 2+): the Hoar Road, Frostwick (570/573), Gullcry Cliffs (561), Ebbmouth (160),
#--- and the Frostflat Causeway back to Saltmere and the Strand Road ("2 Badge Quests")
em.register(:AS_LITLEO, {
  :species => :LITLEO, :level => 21, :ability => :MOXIE, :nature => :HASTY, :ivs => 25, :nickname => "Cinderpaw",
  :moves => [:EMBER, :HEADBUTT, :WORKUP, :NOBLEROAR],
  :kind => :boss, :field => :COLOSSEUM, :badges => 2,
  :boss => { :bars => { :CASUAL => 1, :STANDARD => 2, :HARD => 2, :default => 2 },
             :stat_mults => { :HP => 1.1 },
             :intro => "Cinderpaw shakes its ember mane. The barge deck shudders under its paws!",
             :breaks => { 1 => { :message => "{1} roars, and the crowd roars back!", :stats => { :SPECIAL_ATTACK => 1 } } } },
  :joins => { :level => 19 },
  :map => 146, :where => "Legion recruiting barge, Saltmere harbour (after Badge 2, by the Frostflat Causeway)", :chapter => 4,
  :quest => :AS_LITTLE_CRUCIBLE, :trigger => "Win three bouts in a row, then beat the barge's mascot",
  :why => "Reborn's Litleo is a hard fight after Julia; ours waits until after Tamsin, because Fire burns her Silkwood (Revision 16)"
})

em.register(:ZE_CHARCADET, {
  :species => :CHARCADET, :level => 18, :ability => :FLAMEBODY, :nature => :ADAMANT, :ivs => 20,
  :moves => [:EMBER, :CLEARSMOG, :FIRESPIN, :WILLOWISP], :obtain_text => "Crate 7-B, Ferrow's Landing",
  :kind => :gift, :badges => 2,
  :map => 106, :where => "Ferrow Lighthouse lamp room (Hesper keeps it by the lamp until you hold two badges)", :chapter => 4,
  :quest => :ZE_FORM_7B, :trigger => "File adoption Form 7-C in Chapter 1; collect it from Hesper after Badge 2",
  :why => "Fire before Gym 2 would hand over Tamsin's answer, so the crate stays by the lamp until her badge; an Armarouge/Ceruledge future"
})

em.register(:EL_SUDOWOODO, {
  :species => :SUDOWOODO, :level => 20, :ability => :ROCKHEAD, :nature => :IMPISH, :ivs => 20,
  :moves => [:ROCKTHROW, :FLAIL, :FAKETEARS, :COPYCAT],
  :kind => :battle, :on_ko => :retry, :badges => 2,
  :map => 521, :where => "Hale orchard, Windfall Row (the scarecrow's rematch, after Badge 2)", :chapter => 4,
  :quest => :EL_SCARECROW, :trigger => "Come back to the plum rows with two badges",
  :why => "A Rock type that resists Normal and burns no bridges after Tamsin; no wild Bonsly line until Badge 7"
})

em.register(:IS_SNOM, {
  :species => :SNOM, :level => 15, :ability => :ICESCALES, :nature => :MODEST, :ivs => 25, :happiness => 170,
  :moves => [:POWDERSNOW, :STRUGGLEBUG, :MIRRORCOAT, :FAIRYWIND], :obtain_text => "an oath-parcel from Frostwick",
  :kind => :gift, :badges => 2,
  :map => 160, :where => "The Ebbmouth Net Loft (the parcel was a Snom all along)", :chapter => 4,
  :quest => :IS_OATH_PARCEL, :trigger => "Carry the oath-parcel; open it or don't",
  :why => "Ice Scales Snom that already loves you: Frosmoth (friendship at night) by Lumen"
})

em.register(:EL_DITTO, {
  :species => :DITTO, :level => 20, :ability => :IMPOSTER, :nature => :JOLLY, :ivs => 31,
  :moves => [:TRANSFORM],
  :kind => :battle, :on_ko => :retry, :field => :BLEED, :badges => 2,
  :map => 568, :where => "The Rehearsal (Bleed zone off the Frostflat Causeway)", :chapter => 4,
  :quest => :EL_REHEARSAL, :trigger => "Break the five-second loop; the 'other you' stays behind",
  :why => "Imposter Ditto with perfect IVs: copies the foe's lead (and breeds anything)"
})

em.register(:IS_BOMBIRDIER, {
  :species => :BOMBIRDIER, :level => 24, :ability => :ROCKYPAYLOAD, :nature => :ADAMANT, :ivs => 25, :nickname => "Postmaster",
  :moves => [:ROCKTHROW, :PLUCK, :THIEF, :TORMENT],
  :kind => :boss, :badges => 3,
  :boss => { :bars => { :CASUAL => 1, :STANDARD => 2, :HARD => 3, :default => 2 },
             :stat_mults => { :HP => 1.1, :ATTACK => 1.1 },
             :intro => "A Bombirdier swoops off the cliff with an egg under each wing!",
             :breaks => { 1 => { :message => "{1} drops its eggs into a safe ledge and fights in earnest!", :stats => { :ATTACK => 1 } } } },
  :joins => { :level => 21 },
  :map => 561, :where => "The egg ledges of the Gullcry Cliffs", :chapter => 4,
  :quest => :IS_EGG_THIEF, :trigger => "After Gym 3, beat the 'egg thief' and decide where it belongs",
  :why => "Flying/Dark with Rocky Payload; weak to Rook's Electric, so it is no Gym 4 answer"
})

em.register(:EL_WATTREL, {
  :species => :WATTREL, :level => 20, :ability => :VOLTABSORB, :nature => :TIMID, :ivs => 20,
  :moves => [:SPARK, :PLUCK, :QUICKATTACK, :FEATHERDANCE], :nickname => "Mast",
  :obtain_text => "the Dovetail's rigging", :kind => :gift, :badges => 3,
  :map => 160, :where => "Ebbmouth harbour mast (the Dovetail's bird followed the first boat north)", :chapter => 4,
  :quest => :EL_MASTER_OF_NOTHING, :trigger => "Close the Dovetail's ledger in Chapter 1; find its Wattrel in Ebbmouth after Badge 3",
  :why => "Electric answers Marisol and Flying answers Tamsin, so the bird waits until both are behind you (Revision 16)"
})

#--- Trial rank rewards (later chapters) -----------------------------------------
em.register(:EL_RANK_COMFEY, {
  :species => :COMFEY, :level => 35, :ability => :TRIAGE, :nature => :CALM, :ivs => 31,
  :moves => [:DRAININGKISS, :FLORALHEALING, :GIGADRAIN, :CALMMIND], :kind => :gift,
  :obtain_text => "the Quiet Way (rank Heartwood)",
  :where => "Hall of the Listening Root, Verdance", :chapter => 10, :trigger => "Reach Heartwood in the Quiet Way",
  :why => "Triage healer for doubles; Fairy with priority Draining Kiss"
})

em.register(:IS_RANK_LAPRAS, {
  :species => :LAPRAS, :level => 45, :ability => :WATERABSORB, :nature => :MODEST, :ivs => 31,
  :moves => [:FREEZEDRY, :SPARKLINGARIA, :THUNDERBOLT, :ICESHARD], :kind => :gift, :nickname => "Saga",
  :obtain_text => "the Great Tally, Rimeholt",
  :where => "Mead Hall of Rimeholt", :chapter => 11, :trigger => "Reach Sagaborn in the Tally",
  :why => "Freeze-Dry Lapras: hits Water types super-effectively in an Isenmar full of them"
})

em.register(:AS_RANK_DEINO, {
  :species => :DEINO, :level => 1, :kind => :egg, :obtain_text => "the Crucible's dragon roosts",
  :where => "The Crucible, Cindervault", :chapter => 8, :trigger => "Reach Pyre in the Trial by Flames",
  :why => "The earliest Deino (wild only from Badge 13); Act III's one earned pseudo-legend (rule R7)"
})
