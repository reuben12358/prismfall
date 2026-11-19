#===============================================================================
# Prismfall Trials - 130 Event Pokemon, Chapters 1-4 (implemented)
#-------------------------------------------------------------------------------
# Order follows SPINE Revision 14: Ferrow's Landing -> Saltmere (Gym 1) ->
# Briarwick (Gym 2) -> Rimewood / Frostwick -> Ebbmouth (Gym 3).
# Level caps: 15 before Gym 1, 19 before Gym 2, 23 before Gym 3, 27 before Gym 4.
# Full design (40+ incl. later chapters): design/EVENT_POKEMON.md.
#===============================================================================
em = Prismfall::EventMons

#--- Chapter 1: Ferrow's Landing (100), the Ferrymen's Mile (520), Windfall Row (521)
em.register(:EL_NICKIT, {
  :species => :NICKIT, :level => 7, :ability => :STAKEOUT, :nature => :JOLLY, :ivs => 20,
  :moves => [:QUICKATTACK, :BEATUP, :THIEF, :TAILWHIP], :item => :ORANBERRY,
  :kind => :battle, :on_ko => :retry,
  :map => 103, :where => "Tidewatch Station loft, after a chase round Ferrow's Landing", :chapter => 1,
  :quest => :EL_TART_THIEF, :trigger => "Corner it in the loft after four sightings",
  :why => "A Dark type before Gym 1, with Stakeout (double damage on switch-ins) and Thief"
})

em.register(:ZE_CHARCADET, {
  :species => :CHARCADET, :level => 6, :ability => :FLAMEBODY, :nature => :ADAMANT, :ivs => 20,
  :moves => [:EMBER, :ASTONISH, :LEER, :DISABLE], :obtain_text => "Crate 7-B, Ferrow's Landing",
  :kind => :gift,
  :map => 106, :where => "Ferrow Lighthouse lamp room (warmed by Hesper's lamp)", :chapter => 1,
  :quest => :ZE_FORM_7B, :trigger => "File adoption Form 7-C instead of disposal Form 7-B",
  :why => "Early Fire type (Velmora has 4 Fire families before Gym 1) with an Armarouge/Ceruledge future"
})

em.register(:EL_SUDOWOODO, {
  :species => :SUDOWOODO, :level => 10, :ability => :ROCKHEAD, :nature => :IMPISH, :ivs => 20,
  :moves => [:ROCKTHROW, :FLAIL, :FAKETEARS, :COPYCAT],
  :kind => :battle, :on_ko => :retry,
  :map => 521, :where => "Hale orchard, Windfall Row (the 'scarecrow')", :chapter => 1,
  :quest => :EL_SCARECROW, :trigger => "Water the scarecrow with Wenna's Squirt Bottle",
  :why => "A Rock type that resists Normal before Dorian's gym; no wild Bonsly line until Badge 7"
})

em.register(:EL_WATTREL, {
  :species => :WATTREL, :level => 7, :ability => :VOLTABSORB, :nature => :TIMID, :ivs => 20,
  :moves => [:PECK, :THUNDERSHOCK, :QUICKATTACK, :FEATHERDANCE], :nickname => "Mast",
  :obtain_text => "the Dovetail's rigging", :kind => :gift,
  :map => 107, :where => "Dockmaster's House (the bird from the laid-up Dovetail)", :chapter => 1,
  :quest => :EL_MASTER_OF_NOTHING, :trigger => "Help the Dockmaster write the Dovetail's last ledger entry",
  :why => "Electric/Flying in Chapter 1; Electric is otherwise two families until Ebbmouth"
})

#--- Chapter 2: Lacecliff Walk (527), Marram Down (528), Saltmere (140/145/146/147)
em.register(:EL_TIDE_CRABRAWLER, {
  :species => :CRABRAWLER, :level => 12, :ability => :IRONFIST, :nature => :ADAMANT, :ivs => 20,
  :moves => [:ROCKSMASH, :BUBBLE, :LEER, :POWERUPPUNCH],
  :kind => :battle, :on_ko => :retry, :field => :BEACH,
  :map => 527, :where => "The big tide-pool below Lacecliff Walk", :chapter => 2,
  :quest => :EL_TIDE_POOL_FEUD, :trigger => "Side with Clobbopus in the tide-pool feud",
  :why => "Fighting type before the Normal-type Gym 1; Iron Fist Power-Up Punch"
})

em.register(:EL_TIDE_CLOBBOPUS, {
  :species => :CLOBBOPUS, :level => 12, :ability => :TECHNICIAN, :nature => :ADAMANT, :ivs => 20,
  :moves => [:ROCKSMASH, :FEINT, :BIND, :POWERUPPUNCH],
  :kind => :battle, :on_ko => :retry, :field => :BEACH,
  :map => 527, :where => "The big tide-pool below Lacecliff Walk", :chapter => 2,
  :quest => :EL_TIDE_POOL_FEUD, :trigger => "Side with Crabrawler in the tide-pool feud",
  :why => "Fighting type with Technician (Rock Smash and Power-Up Punch at 60 power); no wild Clobbopus until the Gullcry cliffs"
})

em.register(:EL_KECLEON, {
  :species => :KECLEON, :level => 13, :ability => :PROTEAN, :nature => :JOLLY, :ivs => 20,
  :moves => [:SHADOWSNEAK, :FEINT, :LICK, :THIEF],
  :kind => :battle, :on_ko => :retry, :field => :GRAND_STAGE,
  :map => 145, :where => "Lantern Theatre prop room, Saltmere", :chapter => 2,
  :quest => :EL_LANTERNS, :trigger => "Spot the prop lantern that blinks",
  :why => "Protean in Chapter 2 (every move gets STAB); Dorian's own ace species"
})

em.register(:AS_LITLEO, {
  :species => :LITLEO, :level => 17, :ability => :MOXIE, :nature => :HASTY, :ivs => 25, :nickname => "Cinderpaw",
  :moves => [:EMBER, :HEADBUTT, :WORKUP, :NOBLEROAR],
  :kind => :boss, :field => :COLOSSEUM,
  :boss => { :bars => { :CASUAL => 1, :STANDARD => 2, :HARD => 2, :default => 2 },
             :stat_mults => { :HP => 1.1 },
             :intro => "Cinderpaw shakes its ember mane. The barge deck shudders under its paws!",
             :breaks => { 1 => { :message => "{1} roars, and the crowd roars back!", :stats => { :SPECIAL_ATTACK => 1 } } } },
  :joins => { :level => 15 },
  :map => 146, :where => "Legion recruiting barge, Saltmere harbour", :chapter => 2,
  :quest => :AS_LITTLE_CRUCIBLE, :trigger => "Win three bouts in a row, then beat the barge's mascot",
  :why => "Rejuvenation-style boss reward: a Moxie Litleo (Fire/Normal) before Gym 2"
})

em.register(:EL_SMEARGLE, {
  :species => :SMEARGLE, :level => 12, :ability => :TECHNICIAN, :nature => :TIMID, :ivs => 20,
  :moves => [:SKETCH, :AQUAJET, :ICYWIND], :nickname => "Brush", :obtain_text => "the Lantern Theatre paint loft",
  :kind => :gift,
  :variants => {
    :sea   => { :moves => [:SKETCH, :AQUAJET, :ICYWIND] },
    :ember => { :moves => [:SKETCH, :EMBER, :WILLOWISP] },
    :grove => { :moves => [:SKETCH, :MAGICALLEAF, :STUNSPORE] },
    :night => { :moves => [:SKETCH, :ASTONISH, :CONFUSERAY] }
  },
  :map => 145, :where => "Lantern Theatre paint loft, Saltmere", :chapter => 2,
  :quest => :EL_PAINT_LOFT, :trigger => "Choose the colours of the new backdrop",
  :why => "Coverage of your choice (Water, Fire, Grass or Ghost) plus Sketch; Technician"
})

em.register(:EL_RALTS, {
  :species => :RALTS, :level => 12, :ability => :TRACE, :nature => :MODEST, :ivs => 25,
  :moves => [:CONFUSION, :DISARMINGVOICE, :DOUBLETEAM, :HYPNOSIS],
  :obtain_text => "the end of the Saltmere breakwater", :kind => :gift,
  :map => 146, :where => "End of the Saltmere breakwater, at night", :chapter => 2,
  :quest => :EL_SOUND_OF_SALTMERE, :trigger => "Bring three true silences to the breakwater's end",
  :why => "Psychic/Fairy (Psychic has 1 wild family before Gym 4); Gardevoir or Gallade line"
})

em.register(:EL_GLASS_PONYTA, {
  :species => :PONYTA, :form => 1, :level => 15, :ability => :PASTELVEIL, :nature => :TIMID, :ivs => 25,
  :moves => [:CONFUSION, :FAIRYWIND, :TAILWHIP, :HYPNOSIS],
  :kind => :battle, :on_ko => :retry, :field => :BLEED,
  :map => 522, :where => "The Glassed Orchard, after Badge 1", :chapter => 2,
  :quest => :EL_GLASS_FOAL, :trigger => "Follow the chiming hoofprints through the glass trees",
  :why => "Galarian Ponyta (Psychic, Fairy at Rapidash): an Imprinted variant found only in the Orchard"
})

#--- Chapter 3: the Weavers' Road (541/552/540), Gossamer Wood (524/525), Briarwick (120)
em.register(:EL_HERACROSS, {
  :species => :HERACROSS, :level => 15, :ability => :MOXIE, :nature => :ADAMANT, :ivs => 25,
  :moves => [:FURYATTACK, :AERIALACE, :HORNATTACK, :ENDURE],
  :kind => :battle, :on_ko => :retry, :field => :SILKWOOD,
  :map => 524, :where => "The sap tree on the old trail, Gossamer Wood", :chapter => 3,
  :quest => :EL_HORN_AND_PINCER, :trigger => "Side with Pinsir; Heracross fights you",
  :why => "Moxie Heracross (Bug/Fighting) before Tamsin's Bug gym; wild ones are Headbutt-only and lack Moxie"
})

em.register(:EL_PINSIR, {
  :species => :PINSIR, :level => 15, :ability => :MOXIE, :nature => :ADAMANT, :ivs => 25,
  :moves => [:VISEGRIP, :BIND, :SEISMICTOSS, :BUGBITE],
  :kind => :battle, :on_ko => :retry, :field => :SILKWOOD,
  :map => 524, :where => "The sap tree on the old trail, Gossamer Wood", :chapter => 3,
  :quest => :EL_HORN_AND_PINCER, :trigger => "Side with Heracross; Pinsir fights you",
  :why => "Moxie Pinsir with Seismic Toss (fixed damage that ignores the Silkwood's resistances)"
})

em.register(:EL_SPIDOPS, {
  :species => :SPIDOPS, :level => 20, :ability => :STAKEOUT, :nature => :IMPISH, :ivs => 25, :nickname => "Silkthief",
  :moves => [:SILKTRAP, :BUGBITE, :FEINT, :ASSURANCE],
  :kind => :boss, :field => :SILKWOOD,
  :boss => { :bars => { :CASUAL => 1, :STANDARD => 2, :HARD => 2, :default => 2 },
             :stat_mults => { :HP => 1.15, :DEFENSE => 1.1 },
             :intro => "The Silkthief drops from the canopy on a rope of stolen silk!",
             :breaks => { 1 => { :message => "{1} spins a fresh trap from the stolen thread!", :stats => { :DEFENSE => 1 } } } },
  :joins => { :level => 18 }, :join_choice => true,
  :map => 525, :where => "Gossamer Deepwood, the moth nests (Cut, after Tamsin's badge)", :chapter => 3,
  :quest => :EL_SILKTHIEF, :trigger => "Beat the boss, then choose to take it or leave it guarding the nests",
  :why => "Rejuvenation-style boss reward: Spidops with Stakeout and its signature Silk Trap"
})

#--- Chapter 4: Frostwick (570/573), the Rimewood, Gullcry Cliffs (561), Ebbmouth (160)
em.register(:IS_SNOM, {
  :species => :SNOM, :level => 15, :ability => :ICESCALES, :nature => :MODEST, :ivs => 25, :happiness => 170,
  :moves => [:POWDERSNOW, :STRUGGLEBUG, :MIRRORCOAT, :FAIRYWIND], :obtain_text => "an oath-parcel from Frostwick",
  :kind => :gift,
  :map => 160, :where => "The Ebbmouth Net Loft (the parcel was a Snom all along)", :chapter => 4,
  :quest => :IS_OATH_PARCEL, :trigger => "Carry the oath-parcel; open it or don't",
  :why => "Ice Scales Snom that already loves you: Frosmoth (friendship at night) by Lumen"
})

em.register(:EL_DITTO, {
  :species => :DITTO, :level => 20, :ability => :IMPOSTER, :nature => :JOLLY, :ivs => 31,
  :moves => [:TRANSFORM],
  :kind => :battle, :on_ko => :retry, :field => :BLEED,
  :map => 568, :where => "The Rehearsal (Bleed zone off the Frostflat Causeway)", :chapter => 4,
  :quest => :EL_REHEARSAL, :trigger => "Break the five-second loop; the 'other you' stays behind",
  :why => "Imposter Ditto with perfect IVs: copies the foe's lead (and breeds anything)"
})

em.register(:IS_BOMBIRDIER, {
  :species => :BOMBIRDIER, :level => 24, :ability => :ROCKYPAYLOAD, :nature => :ADAMANT, :ivs => 25, :nickname => "Postmaster",
  :moves => [:ROCKTHROW, :PLUCK, :THIEF, :TORMENT],
  :kind => :boss,
  :boss => { :bars => { :CASUAL => 1, :STANDARD => 2, :HARD => 3, :default => 2 },
             :stat_mults => { :HP => 1.1, :ATTACK => 1.1 },
             :intro => "A Bombirdier swoops off the cliff with an egg under each wing!",
             :breaks => { 1 => { :message => "{1} drops its eggs into a safe ledge and fights in earnest!", :stats => { :ATTACK => 1 } } } },
  :joins => { :level => 21 },
  :map => 561, :where => "The egg ledges of the Gullcry Cliffs", :chapter => 4,
  :quest => :IS_EGG_THIEF, :trigger => "After Gym 3, beat the 'egg thief' and decide where it belongs",
  :why => "Flying/Dark with Rocky Payload before Lumen's Electric gym... it learns Knock Off later"
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
  :why => "The earliest Deino (wild only from Badge 13)"
})
