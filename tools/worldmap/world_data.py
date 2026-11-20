# -*- coding: utf-8 -*-
"""World data for Velmora: the single source the cartography tools read.

Owner: world cartographer.  Consumers: tools/worldmap/gen_docs.py (PLACE_NAMES.md, ROUTES.yaml,
WORLD.md section 11, town map PBS, maps.json), tools/worldmap/gen_world_map.py (the two map images).
Grid: the Essentials town map, 30 x 20 squares of 16 px (x 0-29, y 0-19).
"""

GRID_W, GRID_H = 30, 20

# ----------------------------------------------------------------------------- naming voices
VOICES = {
    'Elowen': dict(
        voice="Fairy-forest English: soft, old and a little courtly. Names come from cloth and thread (the weavers), "
              "from thorn, briar and fruit, and from small country laws. Endings: -wick, -lea, -down, -row, -wold, hollow.",
        examples=["The Ferrymen's Mile", "Windfall Row", "Thistledown Lea", "The Dyers' Ford", "The Briarway"]),
    'Isenmar': dict(
        voice="Nordic sea-ice: short hard words and kennings. Names come from whale, rime, floe, thane and skald, and "
              "from the work that keeps people alive on ice. Endings: -holm, -ness, -garth, -fast, -road.",
        examples=["The Reedholms", "The Icecutters' Haul", "The Whalebone Road", "The Thane's Sled-Road", "Gullcry Cliffs"]),
    'Ashkaar': dict(
        voice="Martial fire and dragon: every road is a march, an oath or a part of the wyrm. Names are blunt and "
              "possessive (the Dominar's, the Legion's). Words: ash, pyre, oath, march, toll, spine, tongue, horn.",
        examples=["The Ashmarch", "The Pyre Road", "The Wyrmspine", "The Wyrmtongue", "Dominar's Toll"]),
    'Ossaria': dict(
        voice="Bone sands: the land is a buried skeleton and is named like one. Roads are bones, flats are bleached, "
              "and the Electors put their title on anything that pays tax. Words: rib, marrow, jaw, spine, vertebrae, sun.",
        examples=["The Rib Road", "The Marrow Road", "The Kneeling Stones", "Spinefall Gorge", "The Vertebrae"]),
    'Zenith': dict(
        voice="Brass and progress: civic, patented and proud. Roads are Mainlines, Parades and Causeways, named for what "
              "they carry or which invention lit them. Words: arc-lamp, conductor, tether, mainline, parade, brink.",
        examples=["The Arc-Lamp Mile", "The Meridian Mainline", "Conductors' Causeway", "The Tetherline", "The Smokestack Parade"]),
    'Nadir': dict(
        voice="Undercity slang: short, rude and accurate. People name a place for what it does to you. "
              "Words: drop, throat, gutter, tailings, sump, leech, knuckle.",
        examples=["The Long Drop", "The Gutterfall", "The Tailings", "Leechman's Walk", "The Throat"]),
    'Antumbra': dict(
        voice="Mirrored and uncanny: names that are true the wrong way round. Time and direction are swapped "
              "(yesterday, hindward, widdershins), and light behaves badly (noonless, downflame).",
        examples=["Widdershins Walk", "Yesterday's Road", "Hindmoor", "Downflame Road", "The Noonless Road"]),
    'Crownhaven': dict(
        voice="Royal and ceremonial: named by decree and counted. Everything is the Sovereign's, the Accord's or one of eighteen.",
        examples=["The Coronation Road", "The Pilgrim Pass", "Sovereign's Ascent", "The Eighteen Gates", "The Crownwall"]),
}

# ----------------------------------------------------------------------------- the early chain (SPINE Revision 14)
# Gym 1 = Saltmere (Dorian, Normal), Gym 2 = Briarwick (Tamsin, Bug). Map IDs are NOT renumbered: Saltmere keeps 140,
# Briarwick 120. `segment` in maps.json is authoritative (validate_encounters.py reads it before the ID scheme).
CITY_ORDER = [100, 140, 120, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 420, 440, 460, 480]

# ----------------------------------------------------------------------------- settlements (town map squares)
# id: (name, x, y, rank, kingdom)   rank: seat / city / town / village / fort
SETTLEMENTS = {
    # Geography v2 (user, 2026-11-19; SPINE Revision 18): Ossaria north, Isenmar west, Ashkaar east, Zenith (Nadir
    # beneath it, same footprint) south, Elowen in the middle touching every kingdom, Crownhaven at its heart. The
    # Act I chain (Ferrow's Landing, Saltmere, Briarwick, Frostwick, the Rimewood, Ebbmouth) and Verdance keep their
    # squares: those maps are built.
    100: ("Ferrow's Landing", 12, 18, 'village', 'Elowen'),
    140: ("Saltmere", 6, 18, 'city', 'Elowen'),
    120: ("Briarwick", 11, 13, 'village', 'Elowen'),
    160: ("Ebbmouth", 3, 7, 'city', 'Isenmar'),
    180: ("Lumen City", 16, 16, 'seat', 'Zenith'),
    200: ("Duneholt", 17, 3, 'seat', 'Ossaria'),
    220: ("Mirefen", 20, 13, 'city', 'Nadir'),
    240: ("Cindervault", 24, 8, 'seat', 'Ashkaar'),
    260: ("Ironreach", 16, 13, 'city', 'Nadir'),
    280: ("Verdance", 9, 10, 'seat', 'Elowen'),
    300: ("Rimeholt", 3, 2, 'seat', 'Isenmar'),
    320: ("Skyreach", 19, 14, 'city', 'Zenith'),
    340: ("Lucent", 28, 16, 'seat', 'Antumbra'),
    360: ("Cragholm", 21, 2, 'city', 'Ossaria'),
    380: ("Gravenmoor", 27, 18, 'city', 'Antumbra'),
    400: ("Cogsworth", 20, 15, 'city', 'Zenith'),
    420: ("Underveil", 16, 18, 'seat', 'Nadir'),
    440: ("Gloaming", 22, 17, 'city', 'Elowen'),
    460: ("Wyrmrest", 25, 13, 'city', 'Ashkaar'),
    480: ("Crownhaven", 14, 9, 'seat', 'Crownhaven'),
    # borderland towns
    570: ("Frostwick", 6, 12, 'town', 'Elowen/Isenmar'),
    590: ("Brassfall", 7, 7, 'town', 'Isenmar/Elowen'),
    610: ("Copperdune", 15, 5, 'town', 'Elowen/Ossaria'),
    630: ("Charwell", 19, 6, 'town', 'Ossaria/Elowen'),
    650: ("Scaldwater", 23, 9, 'town', 'Elowen/Ashkaar'),
    670: ("Glasswake", 23, 4, 'town', 'Ashkaar/Ossaria'),
    690: ("Lanternroot", 12, 12, 'town', 'Nadir/Elowen'),
    710: ("Snowbriar", 5, 8, 'town', 'Elowen/Isenmar'),
    730: ("Anchorhold", 8, 3, 'town', 'Isenmar/Ossaria'),
    750: ("Verdigris", 17, 11, 'town', 'Zenith/Elowen'),
    753: ("Glassmere", 11, 6, 'town', 'Elowen/Antumbra'),
    770: ("Vigil", 20, 3, 'town', 'Antumbra/Ossaria'),
    830: ("Midstair", 19, 17, 'town', 'Zenith/Nadir'),
    850: ("Mothwell", 21, 18, 'village', 'Nadir/Elowen'),
    870: ("Thornwatch", 23, 15, 'town', 'Elowen/Ashkaar'),
    890: ("Pilgrim's Rest", 18, 10, 'town', 'Elowen/Crownhaven'),
    # the war in the sands (Revision 18): Isenmar's border fortress and Ashkaar's staging fortress
    921: ("Skaldfast", 9, 2, 'fort', 'Isenmar'),
    927: ("Cinder Cape Warfort", 26, 3, 'fort', 'Ashkaar'),
}
TOWN_EXTRA_IDS = {140: [146, 147], 180: [181, 194, 195, 196, 608], 200: [203, 204, 205, 208, 214],
                  240: [243, 245, 248, 249, 254], 280: [283, 284, 285, 289, 294, 296], 300: [303, 304, 305, 308, 309, 314],
                  320: [323, 324, 326], 340: [343, 345, 346, 347, 355], 400: [403], 420: [423, 424, 425, 426],
                  440: [443], 480: [482, 483, 485, 486, 489, 495, 496, 497, 498, 499], 160: [167], 260: [263],
                  921: [922, 923]}


def L(id, old, name, origin, kingdom, cells, size, was=None, field=None, landmark='', wild='', fill=(), secret='',
      mode='road', exits='', role='main', side=(), seg=None):
    return dict(id=id, old=old, name=name, origin=origin, kingdom=kingdom, cells=cells, size=size, was=was, field=field,
                landmark=landmark, wild=wild, fill=list(fill), secret=secret, mode=mode, exits=exits, role=role,
                side=list(side), seg=seg)

# ----------------------------------------------------------------------------- the Eighteen Roads (+ the Pilgrim Road)
ROADS = [
  dict(n=1, name="The Strand Road", frm=100, to=140, chapter="Ch 1-2", detail='full',
       note="Ferrow's Landing west along the chalk coast to the free port. Chapter 1 lives on its first leg and the "
            "orchard branch; Chapter 2 arrives in Saltmere for Gym 1. Wild Lv 3-12 (Gym 1 cap 15).",
       legs=[
    L(520, "Route 1", "The Ferrymen's Mile",
      "The mile the ferrymen walked each dusk to ring the Hale bell once the last boat was in.",
      'Elowen', [(12, 17)], [64, 110], [44, 68], 'MEADOW',
      landmark="The Hale Bell on its post above the sea cliff, and the stile where Larch sees you off.",
      wild="Lillipup, Wooloo, Skwovet, Fletchling, Rookidee, Lechonk, Rolycoly. Night: Hoothoot, Nickit, Tarountula.",
      exits="S: Ferrow's Landing. N: Windfall Row. W (new, at the Hale Bell): Lacecliff Walk, behind the quarantine "
            "roadblock (Accord guards, moved here from Windfall Row; lifts on S105).",
      fill=["sea-cliff walk on the south-west side with Wingull posts and a view down to the moored Dovetail",
            "Hale's Bramble: six berry terraces and a picking shed (Wenna's cousin sells tarts)",
            "the Minding Hedges: a three-turn hedge maze with a hidden Potion (the sign's joke made real)",
            "one-way ledge row (the shortcut home)",
            "Juno's catching clearing (fenced tutorial grass)",
            "sheepfold: herd three stray Wooloo back (the first small Trial-style errand)",
            "the old ferry-toll booth with its fare board (lore)",
            "Road Stone I: the first of the eighteen milestones (one per Road; take a rubbing of each)",
            "4 trainers: Youngster Pim, Lass Dory, a shepherd, a bell-ringer's apprentice",
            "gorse banks, drystone walls, a duck pond, two farm carts, a scarecrow"],
      secret="The Smuggler's Stair: behind the toll booth a bramble (Cut, after Briarwick) hides steps to the "
             "Ferryman's Rest, a sea cave with a rowboat, a Glass Apple and a night-only Nickit den.",
      side=[523]),
    L(521, "Route 2", "Windfall Row",
      "Orchard law: a traveller may keep any fruit that has already fallen, and nothing else.",
      'Elowen', [(12, 16), (13, 16)], [120, 70], [62, 48], 'MEADOW', role='branch',
      landmark="The Cider Press yard, and the Accord's quarantine cordon across the lane to the Glassed Orchard.",
      wild="Smoliv, Fidough, Bounsweet, Nidoran, Shinx, Litleo, Zigzagoon. Night: Oddish, Nymble, Spinarak. "
           "Headbutt: Combee, Cherubi, Heracross.",
      exits="S: the Ferrymen's Mile. NE: the Glassed Orchard (Bleed Veil, Chapter 1). W: the corded forest road to "
            "Gossamer Wood (never opens from this side; opens from the wood once V105 >= 1, after the Matriarch). "
            "Door: Hale Farmhouse.",
      fill=["six named orchards in rows (apple, pear, plum, cherry, quince, medlar); every tree a Headbutt tree",
            "the Cider Press yard: press, barrels, a trade NPC, a cellar door",
            "the Nidoran chase: a wild Nidoran runs between three orchards before it can be battled (Rev 13)",
            "beehive wall and a honey errand (Combee)",
            "scarecrow field: a Twins double battle",
            "Accord cordon camp: two tents, wardens, the barrier events",
            "windmill on a rise, duck pond, a farm stand selling berries",
            "drystone lanes with carts, ladders against the trees, windfall-fruit items on the ground",
            "5 trainers: Bug Catcher Wim, Picnicker Ada, the Twins, a cider-maker, an orchard hand"],
      secret="The Thirteenth Row: the plum orchard has twelve rows on the sign and thirteen on the ground. The gap "
             "behind the thirteenth leads to a walled garden with a sleeping Applin (event Pokemon) and a Miracle Seed.",
      side=[522, 523]),
    L(527, None, "Lacecliff Walk",
      "The sea has worn the chalk into arches as fine as Briarwick lace; the weavers copy the cliffs, not the other way round.",
      'Elowen', [(11, 18), (10, 18), (9, 18)], [140, 64], None, 'BEACH',
      landmark="The Lace Arches: a run of sea-cut chalk arches with the path going through three of them.",
      wild="Wingull, Pikipek, Skwovet, Buneary, Shellos, Krabby. Night: Hoothoot, Noibat. Tide pools: Corphish, Wiglett.",
      exits="E: the Ferrymen's Mile. W: Marram Down.",
      fill=["cliff-top path weaving through three chalk arches (the third collapses into a ledge shortcut after Rock Smash)",
            "cliff stairs down to two coves: shingle, rock pools (Old Rod), a beached rowboat",
            "the Wrecker's Lamp: a false light on a pole that a hermit swears he keeps for the gulls",
            "Wingull rookery on a sea stack and a birder with binoculars (trade)",
            "gorse heath with a hidden field of sea-pinks (Flabebe swarms on clear mornings)",
            "the Lacemakers' Bench: a carved stone seat where Juno makes you rest (comedy beat)",
            "smugglers' signal pole that answers Ferrow lighthouse (lore for Kestrel's sidequest)",
            "Road Stone I-b",
            "5 trainers: a fisher, a hiker, a beachcomber, a Lass, a painter at an easel"],
      secret="The Lost Thread: under the second arch, a cave only reachable at low tide (night) holds a weaver's "
             "drowned sample-book (Briarwick lore) and a Shell Bell."),
    L(528, None, "Marram Down",
      "Dune-down held together by marram grass. Saltmere fines anyone who pulls it up, which is why it is still here.",
      'Elowen', [(8, 18), (7, 18)], [110, 80], None, 'BEACH',
      landmark="The Saltmere Beacon on the highest dune, and the first view of the port and its salt lake.",
      wild="Sandygast, Silicobra, Nacli, Bunnelby, Dwebble, Tandemaus, Wingull. Night: Spinarak, Volbeat.",
      exits="E: Lacecliff Walk. W: Saltmere (East Gate).",
      fill=["rolling dunes with marram tall grass in pockets (dune crests block sight lines, so trainers ambush)",
            "the Beacon dune and its keeper's hut (heal once)",
            "a sand-sledge run from the Beacon down to the shore (one-way, fun shortcut)",
            "Saltmere's outer pageant camp: wagons of travelling players rehearsing (hints at Gym 1's stage)",
            "a shipwrecked theatre barge half buried in the sand (props, costumes, a hidden TM)",
            "bird-hide over a brackish pool (Old Rod)",
            "the toll-free stile into Saltmere and a Free Port charter stone",
            "5 trainers: two actors in costume (double), a kite flier, a sand-sculptor, a dune guard"],
      secret="The Prompter's Box: a sunken box in the theatre barge, dug up with a sand-shovel from the camp, holds "
             "the Prompter's Script (Gym 1 hint) and a Normal Gem."),
  ]),
  dict(n=2, name="The Weavers' Road", frm=140, to=120, chapter="Ch 3", detail='full',
       note="Inland from the port up the River Selvedge to the silk forest: the road Briarwick's cloth comes down. "
            "Salt marsh, then the dyers' river, then the manor meadows, then the Gossamer Wood. Wild Lv 12-17 (Gym 2 cap 19).",
       legs=[
    L(541, "Route 4", "The Grey Saltings",
      "Saltmere's salt comes from this marsh. 'Grey' is the salt before it is washed, and the weather.",
      'Elowen', [(6, 17), (7, 16)], [70, 110], [30, 52], 'BEACH',
      landmark="The salt pans and the smoke of the boiling-house, with the chalk cliff of Brinecut behind.",
      wild="Nacli, Bunnelby, Crabrawler, Dwebble, Sandygast, Tandemaus, Minccino. Water: Shellos, Wingull, Tentacool. "
           "Rock Smash: Binacle.",
      exits="S: Saltmere (North Gate). N: the Dyers' Ford. E cliff: Brinecut Mine. Door: the Brinewife's Rest.",
      fill=["boardwalk maze over tidal pools; planks that are only laid at low water (night)",
            "salt pans with rakers, white salt stacks, the boiling-house",
            "wreck of a salt barge in the mud (item, later Rock Smash)",
            "bird hide (a Squawkabilly watcher who trades)",
            "samphire pickers, and a mudflat of Sandygast 'castles' built by children",
            "the Crabrawler ring: a comic boxing errand",
            "a Nacli herd that crosses the path on a timer",
            "the Brinewife's Rest (rest house)",
            "5 trainers",
            "Road Stone II"],
      secret="The Drowned Lane: at night the tide uncovers an old cart road to a tidal islet with a wreckers' cache "
             "(and a locked chest that needs the Harbour Office key from Saltmere).",
      side=[542, 544, 545]),
    L(552, None, "The Dyers' Ford",
      "Briarwick's dyers wash their cloth here, so the river runs red, blue and yellow in three bands.",
      'Elowen', [(8, 15)], [80, 72], None, 'MEADOW',
      landmark="The Three Waters: the Selvedge in three coloured bands below the dye-works, crossed by stepping stones.",
      wild="Smeargle, Mareep, Flabebe (red, blue or yellow by bank), Cottonee, Marill. Night: Volbeat, Illumise, Oddish. "
           "Fishing: Goldeen, Basculin (red-striped in the red band, blue-striped in the blue).",
      exits="S: the Grey Saltings. N: Thistledown Lea.",
      fill=["dye-works: three vat sheds and drying lines you walk under like corridors",
            "madder, woad and weld fields: three colours of tall grass, each with its own encounter slice",
            "the stepping-stone ford (run and you slip into the shallows)",
            "vat-yard sluice puzzle: step the three colours in the order the foreman hums",
            "fulling mill with hammers (works as a moving obstacle)",
            "cloth barge at a jetty: after the foreman's errand it carries you back to Saltmere",
            "the Smeargle that paints your lead Pokemon's mark on a boundary stone",
            "sheep-wash pool and shearers",
            "5 dyer trainers with colour-themed teams",
            "shrine of the Fourth Colour (a white ribbon nobody will dye)"],
      secret="The white water: one thin band of the river is not dyed at all. Follow it upstream through a culvert to "
             "the Bleachfield, a small Bleed-touched meadow of white flowers with a TM and one Imprinted encounter."),
    L(540, "Route 3", "Thistledown Lea",
      "The river meadows held by House Thistledown until the house died out. Nobody has mown them since.",
      'Elowen', [(9, 15), (10, 15)], [130, 64], [64, 28], 'MEADOW',
      landmark="Thistledown Manor on its hill, and the old stone bridge over the Selvedge.",
      wild="Ponyta, Blitzle, Flabebe, Cottonee, Sentret, Doduo, Pancham, Mankey. Night: Morelull, Snubbull, Stunky. "
           "Water: Marill, Buizel, Psyduck.",
      exits="S: the Dyers' Ford (replaces the old Grey Saltings edge, on the same south side). E: Gossamer Wood (the "
            "wood's west eaves). "
            "N hill: Thistledown Manor. Cave: Brinecut Mine (the shortcut back to the Saltings). No warp to Cocoonfall "
            "Hollow any more: it is entered through the Deepwood.",
      fill=["wildflower meadow in bands of colour, tall grass in four separate fields",
            "the River Selvedge along the south third with two islets (Surf later)",
            "stone bridge with a fisherman and a toll that nobody collects",
            "the manor's ruined wall, gateposts and overgrown topiary garden",
            "Ponyta paddock and a drover who races you along the fence",
            "broken mill and mill-race (Old Rod)",
            "mowers' camp with hay-ricks and a cook-fire (heal once)",
            "bamboo stand with Pancham",
            "6 trainers including a double battle",
            "Road Stone II-b"],
      secret="The Ha-ha: a sunken wall runs round the manor hill. Its ditch is a hidden path to the back garden and "
             "a cellar door into the manor's crypt (a second way in, with a Greavard digging there).",
      side=[546, 547]),
    L(524, None, "Gossamer Wood", "Kept name: the silk forest that gives Briarwick its trade.",
      'Elowen', [(11, 15), (11, 14)], [90, 110], [50, 58], 'SILKWOOD',
      landmark="The Weft Bridge, a rope of spun silk as thick as a road, and Woodward's Hut in the middle clearing.",
      wild="Sewaddle, Scatterbug, Blipbug, Cutiefly, Petilil, Shroomish, Sizzlipede. Night: Morelull, Phantump, Venonat. "
           "Headbutt: Pineco, Heracross, Pinsir.",
      exits="W: Thistledown Lea (new edge). N: Briarwick. S: the corded forest road to Windfall Row (opens from this "
            "side when V105 >= 1, after the Matriarch). E (Cut, after Badge 2): Gossamer Deepwood, and Cocoonfall Hollow "
            "beyond it.",
      fill=["silk-curtain trail west to north with two side loops",
            "canopy walkways on an upper level (rope bridges between giant trunks)",
            "cocoon grove, silk-harvest racks and three weavers at work",
            "Woodward's Hut (heal) in the central clearing",
            "fallen giant trunk used as a tunnel",
            "mushroom ring that glows at night",
            "thread-line shortcuts that open from the far side",
            "6 trainers including Twins Mo & Jo (re-levelled for segment 1)",
            "TM Giga Drain grove"],
      secret="The Unpicked Seam: one silk wall opens only at night. Behind it a Heracross and a Pinsir are fighting over "
             "a sap tree; whichever you help leaves, and the other can be caught.",
      side=[525, 526, 548]),
  ]),
  dict(n=3, name="The Hoar Road", frm=120, to=160, chapter="Ch 4", detail='full',
       note="North out of the Gossamer, over the hoar downs into borderland A (the Rimewood) and down Isenmar's cliffs "
            "to Ebbmouth. Frostflat Causeway becomes the coast road back to Saltmere. Wild Lv 16-21 (Gym 3 cap 23).",
       legs=[
    L(566, None, "Spinners' Rise",
      "The drove road up out of the Gossamer where Briarwick's spinners met the hill shepherds to buy fleece.",
      'Elowen', [(10, 12), (9, 12)], [80, 120], None, 'MEADOW',
      landmark="The Fleece Cross: a market cross on the ridge where the old wool fairs were held, hung with prayer-yarn.",
      wild="Mareep, Wooloo, Skiddo, Deerling, Swablu, Tauros, Nincada. Night: Hoothoot, Noctowl, Spinarak. "
           "Higher up: Swinub, Snom.",
      exits="S: Briarwick (North Gate). N: Frostwick Pass.",
      fill=["switchback drove road from forest edge to open fell (the trees thin out as you climb)",
            "sheepfolds and a shepherd's hamlet of three cottages (one becomes a fast-travel rest)",
            "the Fleece Cross and its yarn-tied prayer ribbons (a Ribbon errand)",
            "a hill fort ring on the summit with a view back over the Gossamer to the sea",
            "the Ram Race: a Skiddo-riding shepherd boy challenges you up the hill (Rev 13 event Pokemon)",
            "stone sheep-wash and a cold spring (Old Rod)",
            "first snow patches near the top, then the hoar line",
            "5 trainers: shepherd, hiker, two spinners (double), a wool merchant",
            "Road Stone III"],
      secret="The Shearing Cave: behind a waterfall in the sheep-wash, a cave where the shepherds hide the best fleece "
             "from the tax-man holds a Soft Sand and a sleeping Dubwool's lost lamb (a Wooloo that joins you)."),
    L(577, None, "Frostwick Pass",
      "The low pass over the hoar downs into Frostwick. Both kingdoms claim it and neither keeps the toll hut.",
      'Elowen/Isenmar', [(8, 12), (7, 12)], [72, 96], None, 'SNOWY_MOUNTAIN',
      landmark="The Handfast Arch: half whale-jaw, half living briar, raised when the border was last agreed, with a "
               "brass Meridian sunburst newly bolted across its keystone (the Chapter 4 border beat).",
      wild="Snom, Swinub, Snorunt, Stantler, Deerling, Cubchoo, Delibird. Night: Sneasel, Smoochum.",
      exits="S: Spinners' Rise (the drove road comes up from the south). W: Frostwick (East Gate, the whale-rib palisade).",
      fill=["the climb through hoar-crusted downs",
            "the wind gap: gust tiles that push you back unless you move between gusts",
            "the empty toll hut with two ledgers, one per kingdom, that disagree",
            "a frozen tarn with an ice-fishing hole (Old Rod)",
            "avalanche fences and a snow-buried signpost in two scripts",
            "shepherd's bothy (rest and a hot drink)",
            "trappers' drying racks",
            "a row of snowmen built by Frostwick children; one is a Snorunt",
            "4 trainers: a huscarl, a forester, two sledgers",
            "Road Stone III-b"],
      secret="Behind the frozen waterfall at the tarn is the Hollow of the Handfast: love-carvings of a forester and a "
             "huscarl and a Soothe Bell. It feeds Frostwick's sidequest 'The Two Hearths'."),
    L(578, None, "Rimewood Path",
      "The trappers' blazed path into the frozen forest: a red axe-mark every twenty paces, and you do not leave them.",
      'Elowen/Isenmar', [(6, 11)], [80, 88], None, 'SILKWOOD',
      landmark="The Blaze-Trees, and the Lantern Birch where trappers leave a light for whoever is late.",
      wild="Snover, Cubchoo, Teddiursa, Deerling, Buneary, Swinub, Vanillite. Night: Sneasel, Snorunt, Morelull.",
      exits="S: Frostwick (North Gate). N: the Rimewood.",
      fill=["hoar-birch outskirts thickening into ice-glazed giants",
            "a frozen brook with a slide shortcut",
            "charcoal burners' clearing with a kiln",
            "trapper's lean-to (heal)",
            "the snare line: free a caught Teddiursa (it remembers you in the Rimewood)",
            "frozen silk curtains, brittle enough to break with Rock Smash",
            "honey-stump hives",
            "Frostwick woodcutters and a sledge of logs",
            "5 trainers",
            "the Lantern Birch (relight it at night for a reward)"],
      secret="The Unblazed: at the one tree with a blue blaze, leave the path. The wood repeats until you follow the "
             "Stantler tracks, which lead to a clearing with the herd and one Stantler that will fight."),
    L(562, None, "The Rimewood", "Kept name: the Elowen oldwood that froze when the sea did.",
      'Elowen/Isenmar', [(5, 10), (4, 10)], [96, 110], [48, 56], 'SILKWOOD',
      landmark="The Frost Loom and the aurora clearing.",
      wild="Snover, Bergmite, Cubchoo, Stantler, Teddiursa, Vanillite, Delibird. Night: Sneasel, Snorunt.",
      exits="S: Rimewood Path. N: Gullcry Cliffs. E (Cut): Rimewood Glade.",
      fill=["ice-glazed giant boles and frozen-silk curtain walls", "fallen giant-tree bridge",
            "frozen-brook slide shortcut", "trapper's lean-to (heal)", "the Frost Loom", "aurora clearing",
            "5 trainers", "the Teddiursa from the snare line, if freed, digs up an item here"],
      secret="Rimewood Glade (563) behind the Cut sapling: the Silk-fall, the pond slide puzzle for Never-Melt Ice, "
             "the Snowveil Shrine.",
      side=[563]),
    L(561, "Route 6 - Gullcry Cliffs", "Gullcry Cliffs",
      "First true Isenmar ground. Named for the noise, which never stops.",
      'Isenmar', [(3, 9), (3, 8)], [64, 130], [30, 60], 'MOUNTAIN',
      landmark="Whalebone waymarkers along the cliff and the cod-skull cairn.",
      wild="Wingull, Ducklett, Cramorant, Taillow, Chatot, Bergmite, Wooper. Water: Swanna, Tentacool.",
      exits="S: the Rimewood. N: Ebbmouth. W cliff mouths: Gullcry Caves.",
      fill=["cliff-top path with whalebone waymarkers", "cod-skull cairn", "stilt fishing huts and drying racks",
            "the landslide that forces the detour through Gullcry Caves", "sea-stack views with nesting birds",
            "rope-and-plank cliff stairs", "a signal-fire platform", "Kestrel's battle ground at the north end (K2)",
            "5 trainers", "Road Stone III-c above Ebbmouth"],
      secret="The Gannet Stair: a rope stair down the cliff face to a rookery ledge, where a Cramorant has swallowed "
             "something that is not a fish.",
      side=[564, 565]),
    L(560, "Route 5 - Frostflat Causeway", "Frostflat Causeway",
      "The raised salt road up the coast from Saltmere. Halfway along, the white underfoot stops being salt.",
      'Elowen/Isenmar', [(5, 17), (5, 16), (5, 15), (5, 14), (5, 13)], [140, 64], [64, 30], 'SNOWY_MOUNTAIN',
      role='side',
      landmark="The Border Stones: Elowen's briar crown and Isenmar's whale and axe, with a Meridian sunburst bolted over both.",
      wild="Spheal, Cetoddle, Snom, Swinub, Wiglett, Skitty, Miltank, Tauros, Dunsparce. Night: Smoochum, Snorunt.",
      exits="E (the south end): Saltmere (West Gate). N: Frostwick (South Gate). Spur: the Rehearsal (Bleed Veil). "
            "Closed at the Border Stones by an Isenmar customs chain until you arrive in Frostwick by the Pass; "
            "then it is the quick road back to Saltmere.",
      fill=["raised causeway with wind-fences and marker poles",
            "salt-to-frost gradient along the whole map (the tiles change, then the weather)",
            "the Border Stones and a Meridian survey camp with pegs and a theodolite",
            "drovers with a Miltank and Tauros herd blocking and unblocking the road",
            "stranded salt wagon (errand: find the wheel pin)",
            "first ice-slide tiles on frozen brine pools",
            "children sledging on the frost-flat",
            "brine pools with Wiglett",
            "5 trainers: Lass Tilde, Sailor Haakon, Bird Keeper Ailsa and two more",
            "Road Stone III-d"],
      secret="The Old Causeway: the first road lies under the ice beside the new one. An ice-slide run along it ends "
             "at a cairn with an Icy Rock and the name of whoever built it scratched out.",
      side=[568]),
  ]),
  dict(n=4, name="The Lock Road", frm=160, to=180, chapter="Ch 5", detail='medium',
       note="West to south across the realm (Geography v2: Isenmar never touches Zenith). Up the River Ebb through "
            "borderland B, the Icefall Locks (Isenmar/Elowen), along Coppice Ride into the Crownlands, round the south "
            "of the Crownwall on Wallshadow Row (the Crown Road), then out through the orchards and lamp-posts of the "
            "Arc-Lamp Mile (borderland G) to Lumen.",
       legs=[
    L(580, "Route 7", "The Reedholms",
      "The islets ('holms') of the Ebb delta, joined by boardwalks that are re-laid every spring.",
      'Isenmar', [(4, 7), (5, 7)], [110, 90], [52, 42], 'SNOWY_MOUNTAIN',
      landmark="The eel-weirs, and the north dam of the Voltaic Sluiceworks.",
      wild="Wooper, Lotad, Tympole, Buizel, Goomy, Croagunk, Stunfisk, Azurill.",
      exits="W: Ebbmouth. E: the Icecutters' Haul. N dam: Voltaic Sluiceworks. S bank: Ebb Hollow.",
      fill=["a mesh of still channels and boardwalks in rain", "eel-weirs and smoke huts",
            "reed-cutters' punts (short ferry hops)", "a current that flips with day and night on two channels",
            "heron islet", "6 trainers"],
      secret="A punt left untied at night drifts to the Sunk Holm, an islet off the boardwalks.", side=[584, 585, 588]),
    L(592, None, "The Icecutters' Haul",
      "The sled road the ice-cutters' union drags its blocks down, from the locks to the Ebbmouth boats.",
      'Isenmar/Elowen', [(6, 7)], [110, 70], None, 'SNOWY_MOUNTAIN',
      landmark="Sawyer's Cross: where the Haul meets the forest track from Snowbriar to the Frostfang Pass (gated until Act III).",
      wild="Bergmite, Snover, Mudbray, Pawmi, Magnemite, Wattrel, Deerling.",
      exits="W: the Reedholms. E: Brassfall. S gate: Snowbriar (Act III). N gate: Frostfang Pass (Act III).",
      fill=["ice-sled ruts and block stacks", "a union picket hut", "haul-teams of Mudsdale", "the crossroads gates",
            "5 trainers"],
      secret="A dropped ice block has something frozen inside it; thaw it in Brassfall."),
    L(581, "Route 8 - Icefall Locks", "The Icefall Locks",
      "Where the Ebb falls off the Crownland downs into Isenmar's ice: frozen falls cut into steps and locks by "
      "Zenith's engineers, to feed the Lattice.",
      'Isenmar/Elowen', [(8, 7), (9, 8)], [72, 120], [32, 52], 'SNOWY_MOUNTAIN',
      landmark="The Ice Elevator and the fenced Meridian Extraction Lattice No. 4.",
      wild="Magnemite, Pawmi, Wattrel, Tadbulb, Bergmite, Snover, Plusle, Minun, Togedemaru.",
      exits="W: Brassfall. E (top of the falls): Coppice Ride.",
      fill=["switchbacks up the frozen falls", "brass sluices and frozen turbine wheels", "the cable lift",
            "Lattice pylons", "6 trainers"],
      secret="Behind the third lock gate, an ice cave with a maintenance ledger."),
    L(595, None, "Coppice Ride",
      "The woodwards' ride through the hazel coppices of the Crownlands, cut back every seventh year since the Accord.",
      'Elowen', [(10, 8)], [110, 72], None, 'MEADOW', seg=3,
      landmark="The coppice stools in their numbered panels, and the Kingsferry where the ride crosses the Ebb.",
      wild="Skwovet, Deerling, Smoliv, Combee, Pikipek, Nymble, Petilil.",
      exits="W: the Icefall Locks (borderland B). E: Wallshadow Row, the Crown Road's west junction.",
      fill=["hazel coppice panels in seven ages (a different encounter slice in the tallest)", "the Kingsferry punt",
            "a woodward's hut and charcoal clamp", "a ride-side shrine where the first view of the Crownwall opens",
            "5 trainers"],
      secret="A coppice panel that has not been cut since AF 0: inside it, a ring of old stools and a Miracle Seed."),
    L(594, None, "Wallshadow Row",
      "The farms in the Crownwall's shadow: sun for half the day, and the Accord's tithe for all of it.",
      'Elowen', [(11, 9), (12, 11), (14, 12)], [150, 80], None, 'MEADOW', seg=3,
      landmark="The Crownwall's white cliffs over the hedgerows, and the Southgate shrine where the Crown Road meets "
               "the road to Lumen.",
      wild="Lillipup, Wooloo, Smoliv, Fidough, Flabebe, Mareep. Night: Hoothoot, Spinarak, Morelull.",
      exits="W junction: Coppice Ride (to Isenmar) and Prism Falls (to Verdance). N: Kingsmead. S junction: the "
            "Arc-Lamp Mile (to Lumen) and the Long Drop (Nadir). E: Candle Down.",
      fill=["the Crown Road: a paved ring road with eighteen milestones round the Crownwall", "tithe barns",
            "hedge-lined fields in the wall's shadow line", "the Southgate shrine at the south junction",
            "the west junction's inn and signpost to four kingdoms", "6 trainers"],
      secret="A shepherd's track up the Crownwall's foot to a cave the Accord bricked up; the bricks are loose."),
    L(593, None, "The Arc-Lamp Mile",
      "The first road in Velmora lit by electric arc lamps. Zenith counts its age from the night they were switched on.",
      'Elowen/Zenith', [(14, 14), (15, 15)], [110, 64], None, 'NEON_GRID',
      landmark="One hundred numbered arc lamps running out of Lumen into the Crownland orchards, and Lumen's West Gate "
               "at the end of them.",
      wild="Yamper, Shinx, Pawmi, Rookidee, Klink, Magnemite, Bounsweet. Night: Joltik, Voltorb.",
      exits="NW: Wallshadow Row (the Crown Road). SE: Lumen West Gate.",
      fill=["paved boulevard with lamp numbers", "orchards with clockwork pickers (borderland G)", "a tram stop without a tram",
            "advertising hoardings", "the lamplighters' depot", "5 trainers"],
      secret="Lamp 47 has been dark for ten years; the reason is under its base plate.", side=[582]),
  ]),
  dict(n=5, name="The Brass Road", frm=180, to=200, chapter="Act II", detail='outline',
       note="South to north through the middle of the realm (Zenith never touches Ossaria): the Meridian railway out of "
            "Lumen (borderland G), the Crown Road round the east of the Crownwall (Candle Down, the Highwold), then "
            "borderland C, the Brass Dunes, where the line ran into the sand, and on to Duneholt.",
       legs=[
    L(612, None, "The Meridian Mainline", "Zenith's first railway. You walk the service road beside the track.",
      'Zenith/Elowen', [(17, 15), (17, 13)], [130, 64], None, 'MOUNTAIN',
      landmark="The signal gantries, and the cutting where the line drops off the plateau into the Crownlands.",
      wild="Electric and Steel with orchard edges: Magnemite, Klink, Varoom, Rufflet, Applin.",
      exits="S: Lumen. N: Candle Down (the Crown Road).",
      secret="A signal box whose levers reroute a handcar to a siding."),
    L(602, None, "Candle Down",
      "The downs east of the Crown, where pilgrims light a candle on each cairn on their way to the Pilgrim's Rest.",
      'Elowen', [(16, 11), (17, 9)], [110, 110], None, 'MEADOW', seg=4,
      landmark="The candle-cairns, and the view into the Crownwall's one gap.",
      wild="Skiddo, Deerling, Swablu, Ponyta, Cottonee, Sentret. Night: Volbeat, Illumise, Litwick.",
      exits="SW: Wallshadow Row (the south junction). SE: the Meridian Mainline and Verdigris. E junction: the Ironway "
            "(to Ashkaar) and the Pilgrim Pass. N: the Highwold.",
      fill=["the Crown Road over open downs", "candle-cairns (a cairn errand)", "the east junction's coaching inn",
            "chalk hill-figure of a crown", "5 trainers"],
      secret="One cairn's candle never goes out; under it, a stair into the Crownwall's foot."),
    L(603, None, "The Highwold",
      "The high wold north of the Crown: sheep, skylarks and the one road in Elowen that runs to the desert.",
      'Elowen', [(16, 7), (14, 6)], [130, 80], None, 'MEADOW', seg=4,
      landmark="The Wold Stones, and the Crownwall's north face white in the sun.",
      wild="Wooloo, Mareep, Skiddo, Rookidee, Hoppip, Bunnelby, Trapinch (on the north slope).",
      exits="SE: Candle Down. N junction: the Brass Dunes (to Ossaria). W: Kingsmead.",
      fill=["the Crown Road along the wold top", "sheepfolds and a dew-pond", "the Wold Stones", "the north junction's "
            "caravan yard (camels and ox-carts side by side)", "5 trainers"],
      secret="A dew-pond that never dries, even in the drought years; something drinks from it at night."),
    L(600, "Route 9 - The Brass Dunes", "The Brass Dunes", "Kept name: dunes the colour of the locomotives buried in them.",
      'Elowen/Ossaria', [(14, 5)], [130, 72], [60, 28], 'DESERT',
      landmark="The broken viaduct where the Mainline ran into the sand, and the half-buried engine 'Progress'.",
      wild="Sandshrew, Silicobra, Hippopotas, Phanpy, Electrike, Orthworm, Cacnea, Skwovet.",
      secret="A carriage door under the sand opens into a buried dining car.", side=[604, 605]),
    L(601, "Route 10", "The Rib Road", "Waymarked by the ribs of a leviathan, one every hundred paces, set there before the Electors.",
      'Ossaria', [(16, 4)], [72, 120], [30, 56], 'DESERT',
      landmark="The Rib Gate: the two largest ribs, meeting overhead.",
      wild="Ground and Rock: Sandile, Trapinch, Cacnea, Rolycoly, Cubone.",
      secret="Count the ribs: one is missing, and its socket is a stair."),
    L(613, None, "Sunbleach Flats", "The flats before Duneholt, where bones and cloth alike go white in a season.",
      'Ossaria', [(16, 3)], [110, 64], None, 'DESERT',
      landmark="The bleaching frames of the linen-makers and Duneholt's Sandgate on the horizon.",
      wild="Maractus, Hippopotas, Silicobra, Vullaby.", secret="A mirage well that is real at noon only."),
  ]),
  dict(n=6, name="The Leach Road", frm=200, to=220, chapter="Act II", detail='outline',
       note="Down the River Leach: south out of the desert through borderland D, the Leach Canyons (Ossaria/Elowen), "
            "along Wormwood Lea east of the Crown, and over the Gutterfall into the Mirefen marsh under Zenith's "
            "escarpment (Nadir, beneath Zenith).",
       legs=[
    L(620, "Route 11", "The Marrow Road", "It runs through the fossil beds where the rock is the colour of marrow.",
      'Ossaria', [(17, 4)], [130, 70], [64, 30], 'DESERT',
      landmark="The dig terraces and the mouth of the Ossuary of Dunes.",
      wild="Fossil country: Cubone, Drilbur, Sandile, Baltoy, Nosepass.",
      secret="An unlabelled dig pit with a complete skeleton nobody has reported.", side=[624, 625]),
    L(632, None, "The Kneeling Stones", "Wind-cut pillars that look like bowed pilgrims. The crossroads of Ossaria.",
      'Ossaria', [(18, 4)], [90, 80], None, 'DESERT',
      landmark="The stones themselves, and the crossroads post: Duneholt, Charwell, Vigil.",
      wild="Sigilyph, Baltoy, Gligar, Sandaconda.", secret="At dusk the stones' shadows point at one buried door.",
      side=[628]),
    L(621, "Route 12 - The Leach Canyons", "The Leach Canyons",
      "Kept name: the red gorges the River Leach cut on its way out of the desert; the forest climbs in along the water.",
      'Ossaria/Elowen', [(19, 5)], [100, 100], [40, 40], 'WASTELAND',
      landmark="Gallery forest in the gorge bottoms and the bone-char filter towers above.",
      wild="Sandile, Trapinch, Maractus, Skwovet, Deerling, Bramblin, Gligar, Ekans.",
      secret="A dry side canyon with a clean spring that neither side knows about."),
    L(634, None, "Wormwood Lea",
      "Bitter meadows along the Leach east of the Crown. The river is still clean here, and the wormwood keeps the "
      "leeches off.",
      'Elowen', [(20, 8), (20, 10)], [90, 130], None, 'MEADOW', seg=5,
      landmark="The Leach's water-meadows, the wormwood stills, and the ford where the Ironway crosses.",
      wild="Marill, Psyduck, Ducklett, Skiddo, Flabebe, Venonat, Wooper. Fishing: Basculin, Barboach.",
      exits="N: Charwell. S: the Gutterfall. Crossings: the Ironway at the ford, the Pilgrim Pass at the south bridge.",
      fill=["the river meadows in strips", "the wormwood stills (a bitters errand)", "the Ironway ford",
            "eel-traps", "the south bridge with its first pilgrim shrine", "5 trainers"],
      secret="Where the Leach first turns blue, a pipe comes out of the bank. It is warm."),
    L(633, None, "The Gutterfall", "Where the Leach drops off the Crownland edge into the marsh under Zenith's escarpment. "
                                  "Nadir named it.",
      'Nadir/Elowen', [(20, 12)], [80, 96], None, 'CORROSIVE_MIRE',
      landmark="The blue waterfall (Zenith's outfall joins the Leach at the lip) and the ladder-town clinging beside it.",
      wild="Grimer, Croagunk, Trubbish, Stunky, Toxel.",
      secret="A ledge behind the fall where the sump-folk leave their dead's lanterns."),
  ]),
  dict(n=7, name="The Sulfur Road", frm=220, to=240, chapter="Act II", detail='outline',
       note="Out of the marsh by the leech-gatherers' causeway, round the sulfur lake of borderland E (the Sulfur "
            "Reach, Elowen/Ashkaar: burnt woods and hot springs), then the Dominion's first road.",
       legs=[
    L(640, "Route 13", "Leechman's Walk", "The plank causeway the leech-gatherers keep up. You pay them or you swim.",
      'Nadir', [(21, 13)], [120, 72], [56, 32], 'CORROSIVE_MIRE',
      landmark="The leech-gatherers' stilts and the mouth of the Miasma Caverns.",
      wild="Croagunk, Grimer, Shroodle, Wooper (Paldean), Scraggy.",
      secret="A sunk plank path that only shows when the marsh gas burns off.", side=[644, 645, 648]),
    L(641, "Route 14 - Sulfur Reach (Lake Sallow)", "Lake Sallow", "Named for its colour. The whole lake is one hot spring.",
      'Elowen/Ashkaar', [(22, 10), (23, 10)], [120, 100], [50, 46], 'ASHEN_WASTE',
      landmark="The yellow lake, its geysers, the scorched woods round its shore, and Lantern Isle steaming in the middle.",
      wild="Salandit, Charcadet, Numel, Houndour, Capsakid, Cyclizar, Bramblin, Fletchinder.",
      secret="A geyser that lifts a surfer onto the cliff shelf above the lake.", side=[658]),
    L(652, None, "The Pyre Road", "Lined with oath-pyres that are never let go out. Every legionary lights one before first posting.",
      'Ashkaar', [(24, 9)], [130, 70], None, 'ASHEN_WASTE',
      landmark="The avenue of pyres and Cindervault's Caldera Gate.",
      wild="Fire and Dragon: Growlithe, Litleo, Torkoal, Axew, Fletchinder.",
      secret="One pyre is cold. Lighting it calls the person it was lit for."),
  ]),
  dict(n=8, name="The Iron Road", frm=240, to=260, chapter="Act II", detail='outline',
       note="West again: the Ashmarch, the Ironway pass out of the Dominion (borderland E), the Crown Road round the "
            "Crownwall's east (Candle Down), then down the Long Drop into Ironreach under Zenith's west rim (Nadir). "
            "The war road (the Cinderglass Barrens, borderland M) leaves Cindervault's north gate for the front in Ossaria.",
       legs=[
    L(660, "Route 15", "The Ashmarch", "The legions' marching road. Ash falls on it every day and is swept every night.",
      'Ashkaar', [(23, 7)], [120, 72], [32, 56], 'ASHEN_WASTE',
      landmark="The mile-forts and the Cinderhorn smoking to the south-east.",
      wild="Numel, Torkoal, Rolycoly, Slugma, Druddigon.",
      secret="A sweepers' tunnel under the road that the legion uses to move unseen.", side=[664, 665, 666, 668]),
    L(661, "Route 16 - The Ironway", "The Ironway",
      "Kept name: the pass the ore came down, on rails laid by Nadir and paid for by Ashkaar.",
      'Elowen/Ashkaar', [(21, 7), (20, 7)], [150, 70], [60, 30], 'MOUNTAIN',
      landmark="The ore-cart incline down to the Leach ford, the burnt woods either side, and the Truce Posts.",
      wild="Scraggy, Houndour, Cyclizar, Machop, Aron, Charcadet, Bramblin.",
      exits="E: the Ashmarch. W: the Leach ford (Wormwood Lea), then Candle Down (the Crown Road's east junction).",
      secret="A runaway ore cart you can ride down a closed spur."),
    L(672, None, "The Long Drop",
      "Ironreach's front door: a shaft road that goes down for an hour. Named by people who carried things up it.",
      'Nadir/Elowen', [(16, 12)], [64, 130], None, 'SCRAPYARD',
      landmark="The winding-tower at the Crown Road's south junction, and the cage lift.",
      wild="Timburr, Machop, Pawniard, Trubbish, Tinkatink.",
      secret="A side adit sealed with a pit-fighter's handprint in iron."),
    L(662, "Route 15b - The Cinderglass Barrens", "The Cinderglass Barrens", "Kept name: obsidian dunes where sand met fire.",
      'Ashkaar/Ossaria', [(24, 6), (23, 5)], [130, 90], [56, 40], 'ASHEN_WASTE', role='side',
      landmark="Black glass dunes and lava tubes: the volcanic ash desert where the Dominion meets the bone sands.",
      wild="Carkol, Magcargo, Torkoal, Vibrava, Gible, Onix.",
      exits="S: Cindervault's north gate. N: Glasswake, then the war road west across Ossaria to the Ashkaar Siege "
            "Camp, or the Wyrmtongue to Cinder Cape.",
      secret="A lava tube that comes out inside the Petrified Ashwood.", side=[663]),
    L(673, None, "The Wyrmtongue",
      "The spit of black lava that runs out to the Cape, forked at the end like a tongue.",
      'Ashkaar', [(24, 3), (25, 3)], [64, 120], None, 'VOLCANIC', role='side',
      landmark="The forked spit and the Warfort's beacon.", wild="Fire and Dragon, high level; sea birds.",
      secret="At the fork's left tip, a sea cave that looks west along the coast to the smoke of the war in the sands."),
  ]),
  dict(n=9, name="The Root Road", frm=260, to=280, chapter="Act III", detail='outline',
       note="Borderland F, the Rootdeep: out of the mines under Zenith's west rim through the Gossamer's roots, past "
            "Lanternroot, across the Crown Road's south-west and over Prism Falls into Elowen's royal country.",
       legs=[
    L(692, None, "The Tailings", "The mine-waste hills outside Ironreach. Kids sled down them on shovels.",
      'Nadir', [(15, 13)], [100, 70], None, 'SCRAPYARD',
      landmark="Grey waste cones and the entrance to Grudgestone Quarry.",
      wild="Trubbish, Roggenrola, Tinkatink, Scraggy, Varoom.",
      secret="A tailings slide that drops into a buried engine house.", side=[684, 685, 688]),
    L(680, "Route 17 - The Rootdeep", "The Rootdeep", "Kept name: where Elowen's roots come through the roof of Nadir's mines.",
      'Nadir/Elowen', [(14, 13), (13, 12)], [72, 130], [30, 56], 'CAVE', mode='under',
      landmark="Root-cathedrals (the Gossamer's roots) and overgrown ore carts.",
      wild="Foongus, Paras, Shiinotic, Breloom, Toedscool, Bramblin, Machoke.",
      secret="A root that bleeds when cut: the start of Lanternroot's sidequest."),
    L(681, "Route 18 - Prism Falls", "Prism Falls", "Kept name: the falls throw a rainbow all day, every day. It is the Imprint.",
      'Elowen', [(11, 11)], [130, 80], [56, 36], 'RAINBOW',
      landmark="The falls and the Rainbow Stair beside them.",
      wild="Fairy and Grass: Togetic, Comfey, Floette, Swablu, Ludicolo.",
      secret="Behind the falls, a cave where the rainbow is the wrong way round."),
    L(693, None, "The Briarway",
      "The royal road to Verdance, hedged with briar on both sides by the first monarch and clipped ever since.",
      'Elowen', [(10, 11)], [72, 120], None, 'FAIRY_TALE',
      landmark="The clipped briar walls, the royal milestones, the Kingsgate ahead.",
      wild="Roselia, Ribombee, Deerling, Fidough, Togedemaru.",
      secret="A gardeners' door in the hedge to the Royal Chase's back fence.", side=[682]),
  ]),
  dict(n=10, name="The Hart Road", frm=280, to=300, chapter="Act III", detail='outline',
       note="Borderland A2, the Hoarwood (Elowen/Isenmar), in the north-west: royal hunting country, the snow-forest, "
            "over the Frostfang Pass to the frozen sea.",
       legs=[
    L(700, "Route 19", "The Hart's Run", "The line the royal hunt rides. No one else may gallop on it, and everyone does.",
      'Elowen', [(8, 9), (7, 9)], [140, 70], [60, 30], 'MEADOW',
      landmark="Hunting towers and the white hart carved into the chalk.",
      wild="Sawsbuck, Stantler, Bouffalant, Girafarig, Tauros.", secret="The carved hart's eye is a trapdoor.",
      side=[708]),
    L(701, "Route 20 - Northern Rimewood", "The Hoarwood",
      "What Isenmar calls the northern Rimewood: older, deeper, and white all year.",
      'Elowen/Isenmar', [(6, 9), (5, 9)], [80, 130], [32, 56], 'SNOWY_MOUNTAIN',
      landmark="Royal hunting lodges and frozen Bride-briar hedges.",
      wild="Abomasnow, Sawsbuck (winter), Ursaring, Beartic, Glalie.", secret="A lodge with one room that is still warm."),
    L(712, None, "The Whalebone Road",
      "Arched with whale ribs from the pass down to Rimeholt's Icewall Gate, one arch per thane.",
      'Isenmar', [(4, 4), (4, 3)], [72, 120], None, 'SNOWY_MOUNTAIN',
      landmark="The rib arches, each carved with a thane's name; the last is blank.",
      wild="Water and Ice: Sealeo, Piloswine, Frosmoth, Arctozolt.", secret="The blank arch has a name on the inside.",
      side=[704, 705]),
  ]),
  dict(n=11, name="The Mast Road", frm=300, to=320, chapter="Act III", detail='outline',
       note="Along the frozen coast on the thane's sled-road, up the Mast Glacier (borderland B2, Isenmar/Ossaria: "
            "tundra and permafrost dunes) to Anchorhold, where the airships moor; then by airship over Ossaria and "
            "Elowen to Skyreach's Cloudstair. The only road with an air leg (Act III, Skyreach's airships): Isenmar and "
            "Zenith share no border.",
       legs=[
    L(720, "Route 21", "The Thane's Sled-Road", "The coast road on the sea ice, kept open by the thane's own teams.",
      'Isenmar', [(4, 1), (5, 1)], [140, 72], [60, 30], 'SNOWY_MOUNTAIN',
      landmark="Sled posts, ice-fishing camps, the frozen sea to the north, and the war-sleds going east.",
      wild="Walrein, Dewgong, Cloyster, Mamoswine, Delibird.",
      secret="A sled team that will run you out to a wreck locked in the ice.", side=[728]),
    L(721, "Route 22 - Mast Glacier", "The Mast Glacier",
      "Kept name: airships are ice-anchored along the glacier tongue, and their masts look like a winter forest.",
      'Isenmar/Ossaria', [(6, 2), (7, 2)], [72, 130], [32, 56], 'SNOWY_MOUNTAIN',
      landmark="The anchored airships, and the glacier's snout running out onto frozen dunes.",
      wild="Ice with Ground or Flying: Swinub, Cetoddle, Sandshrew (Alolan), Swablu, Skarmory, Hippopotas, Cryogonal.",
      secret="A crevasse with an airship that never left."),
    L(732, None, "The Tetherline", "The walkway strung under Skyreach's mooring cables. Zenith calls it safe.",
      'Zenith', [(18, 15)], [130, 64], None, 'STORMFRONT',
      landmark="Cable gantries over a long drop.", wild="Flying and Steel: Skarmory, Corviknight, Drifblim, Magneton.",
      secret="A maintenance cradle that crosses to a mast nobody uses.", side=[724, 725, 726]),
  ]),
  dict(n=12, name="The Glass Road", frm=320, to=340, chapter="Act III", detail='outline',
       note="North off the plateau through borderland G (Conductors' Causeway, the Wired Wood, Verdigris), round the "
            "Crownwall's north on the Crown Road (Candle Down, the Highwold, Kingsmead), into the Looking-Glass Wood "
            "(borderland H) and through Mirror Mere into the kingdom behind the glass.",
       legs=[
    L(740, "Route 23", "Conductors' Causeway",
      "The road between the lightning rods ('conductors') that feed the Lattice. It hums.",
      'Zenith', [(18, 13)], [72, 130], [60, 28], 'STORMFRONT',
      landmark="Rows of conductors and Stormwatch Spire.",
      wild="Electric and Flying: Electabuzz, Kilowattrel, Emolga, Zebstrika.",
      secret="One conductor is grounded, and something lives in the quiet.", side=[744, 745, 746, 748]),
    L(741, "Route 24 - The Wired Wood", "The Wired Wood",
      "Kept name: forest grown up Zenith's pylons, or pylons planted in Elowen's forest, depending who you ask.",
      'Zenith/Elowen', [(18, 12)], [80, 130], [32, 56], 'SILKWOOD',
      landmark="Vine-wrapped pylons and clockwork orchards.", wild="Luxray, Boltund, Klang, Floette, Granbull, Tinkatuff.",
      secret="A greenhouse-factory whose clockwork bees have gone wild."),
    L(756, None, "Kingsmead",
      "The king's meadow under the Crownwall's north-west face, where Elowen's royal horses grazed before there was "
      "an Accord.",
      'Elowen', [(12, 7)], [110, 90], None, 'MEADOW', seg=11,
      landmark="The old paddock walls, and the Glassfall Scar glittering high on the wall above.",
      wild="Ponyta, Blitzle, Deerling, Swablu, Hoppip, Cottonee. Night: Morelull, Hatenna.",
      exits="E: the Highwold. S: Wallshadow Row. W: the Looking-Glass Wood (borderland H).",
      fill=["the Crown Road through paddocks", "the royal stud's ruined stables", "a horse-fair ground (a racing "
            "errand)", "5 trainers"],
      secret="The farrier's forge still has a fire in it; nobody tends it."),
    L(752, None, "The Looking-Glass Wood",
      "Borderland H. The reflections in its pools do not always agree with what is standing over them.",
      'Elowen/Antumbra', [(11, 7)], [100, 90], None, 'MINDSCAPE',
      landmark="Pools that reflect the wrong sky, and a stream that runs uphill.",
      wild="Kirlia, Flittle, Rabsca, Ribombee, Hatenna.", secret="Walk a path backwards and it goes somewhere else.",
      side=[742]),
    L(755, None, "Widdershins Walk",
      "The first road in Antumbra. It can only be walked against the sun, and here the sun agrees.",
      'Antumbra', [(26, 16), (27, 16)], [100, 80], None, 'INVERSE',
      landmark="A colonnade whose shadows fall toward the light.",
      wild="Ghost and Psychic: Duskull, Gothita, Sinistea, Espurr.",
      secret="Turn sunwise three times and the road is not there.", side=[743]),
  ]),
  dict(n=13, name="The Grave Road", frm=340, to=360, chapter="Act IV", detail='outline',
       note="Borderland I, the Obsidian Barrows: out of Antumbra through the Grave Glass at Vigil and up Spinefall "
            "Gorge to Ossaria's high crags.",
       legs=[
    L(772, None, "Yesterday's Road", "Travellers arrive at the far end before they set out. The Synod taxes both ends.",
      'Antumbra', [(28, 17), (27, 17)], [110, 64], None, 'INVERSE',
      landmark="Milestones that count down, then up.", wild="Ghost, Psychic, Dark: Lampent, Duosion, Sableye, Mismagius.",
      secret="A traveller on the road who is you, a little earlier.", side=[768]),
    L(760, "Route 25 - The Obsidian Barrows", "The Obsidian Barrows",
      "Kept name: a necropolis of obsidian tomb-mirrors that became gates.",
      'Antumbra/Ossaria', [(20, 4), (21, 4)], [130, 80], [56, 32], 'INVERSE',
      landmark="The tomb-mirrors and the desert hanging in the sky.",
      wild="Palossand, Golurk, Claydol, Runerigus, Inkay, Absol, Houndstone.", secret="A mirror with no tomb behind it."),
    L(761, "Route 26", "Spinefall Gorge", "The river comes down over the backbone of something that was a mile long.",
      'Ossaria', [(22, 4), (22, 3)], [72, 130], [32, 56], 'DESERT',
      landmark="The waterfall over fossil vertebrae.", wild="Ground and Rock with water: Quagsire, Relicanth, Tyrunt, Archen.",
      secret="A dry cave behind the fall with a nest of something revived.", side=[764, 765]),
    L(773, None, "The Vertebrae", "A stair of round stone drums up to Cragholm, each one a step and a bone.",
      'Ossaria', [(21, 3)], [64, 120], None, 'MOUNTAIN',
      landmark="The drum-stair and Cragholm's lift towers above.", wild="Rhydon, Gliscor, Lairon, Archeops.",
      secret="One drum is hollow."),
  ]),
  dict(n=14, name="The Moor Road", frm=360, to=380, chapter="Act IV", detail='outline',
       note="Along the ridge back to Vigil, through the Grave Glass, and across Antumbra's moors. Side road: the "
            "Dry Tide, Ossaria's dry seabed from Duneholt's west gate out to the war in the sands (the bone-carters' "
            "camp at its end; Ch14-16 convoy and prisoner trips, and Sigrun's landing in Ch19).",
       legs=[
    L(780, "Route 27", "The Jawbone Ridge",
      "A ridge with a toothed skyline. Cragholm says the teeth were cut; Vigil says they grew.",
      'Ossaria', [(20, 2)], [150, 72], [60, 30], 'MOUNTAIN',
      landmark="The teeth, the Darkglass Mine headframe, and the war's smoke to the west.",
      wild="Tyranitar line, Lycanroc, Garganacl, Skarmory.",
      secret="A cave in the largest tooth.", side=[784, 785, 788]),
    L(781, "Route 28", "Hindmoor",
      "The moor that is only seen properly over your shoulder. Look straight at it and it is somewhere else.",
      'Antumbra', [(25, 17), (25, 18)], [80, 130], [32, 56], 'INVERSE',
      landmark="Standing pools that show what is behind you.", wild="Ghost and Dark: Greavard, Dreepy, Absol, Mimikyu.",
      secret="Walk it backwards and you find the cottage."),
    L(810, None, "The Dry Tide", "An old seabed, rippled like a beach the sea left one evening and never came back to.",
      'Ossaria', [(15, 3), (14, 3)], [140, 72], None, 'DESERT', role='side',
      landmark="Shell pavements, a stranded ship's ribs, the bone-carters' white banner over their camp at the west end, "
               "and the Glass Dunes beyond, where the war is fought.",
      wild="Fossil ground types, Sandaconda, Palossand.",
      exits="E: Duneholt's west gate. W end: the bone-carters' camp (930); past it the war maps (the Siege Camp 924 and "
            "the Glass Dunes 926; story-gated). The observers' mesa (929, Ch19) stands south of the battlefield.",
      secret="At night you can hear the tide. Follow it."),
    L(790, None, "Downflame Road", "Lit by candles whose flames hang below the wick. Gravenmoor makes them.",
      'Antumbra', [(26, 18)], [110, 70], None, 'INVERSE',
      landmark="The candle-posts and the lantern hospice on the hill.",
      wild="Litwick line, Drifloon, Shuppet.", secret="Blow one candle out and a door-shaped piece of dark stays lit."),
  ]),
  dict(n=15, name="The Slag Road", frm=380, to=400, chapter="Act IV", detail='outline',
       note="Out of Antumbra by the Slagglass, the black mirror Cogsworth's slag cooled into on the Slag Mesa "
            "(borderland G, Zenith's eastern waste), then down the Smokestack Parade into the foundries.",
       legs=[
    L(800, "Route 29", "The Noonless Road", "Antumbra has no noon. On this road your shadow never shortens.",
      'Antumbra', [(28, 18), (29, 18)], [140, 70], [60, 30], 'INVERSE',
      landmark="Sundials with no shortest mark; the Barrow of the Wardens.", wild="Ghost, Psychic, Dark, high level.",
      secret="A sundial that does work, for one minute.", side=[804, 805, 806, 808]),
    L(801, "Route 30 - Slag Mesa", "The Slag Mesa", "Kept name: a mesa that is half rock and half what Cogsworth poured on it.",
      'Elowen/Zenith', [(21, 14)], [80, 130], [32, 56], 'WASTELAND',
      landmark="Slag falls, still warm, and the Slagglass: a cooled black pour that reflects Antumbra (gate C).",
      wild="Steel and Ground: Excadrill, Orthworm, Bronzong, Garbodor.",
      secret="A cooled slag flow shaped round something large."),
    L(811, None, "The Smokestack Parade", "Cogsworth's ceremonial avenue: one chimney per founding patent.",
      'Zenith', [(20, 14)], [120, 64], None, 'FACTORY',
      landmark="The numbered stacks and three shift-clocks.", wild="Klinklang, Magneton, Revavroom, Corviknight.",
      secret="Stack 9 has no furnace under it."),
  ]),
  dict(n=16, name="The Drowned Road", frm=400, to=420, chapter="Act IV", detail='outline',
       note="Borderland L, the Hanging Stair: off the plateau's south-east rim and down the cliff to the drowned south "
            "coast, then by water over the towers of Aurelia to Underveil.",
       legs=[
    L(832, None, "The Brink", "Where Zenith stops. A promenade with a brass rail and a very long view.",
      'Zenith', [(20, 16)], [130, 60], None, 'STORMFRONT',
      landmark="The rail, the lift-heads, the telescopes over the Hallow Strait.", wild="Flying and Steel.",
      secret="One telescope is fixed on a window in Underveil.", side=[828]),
    L(820, "Route 31 - The Hanging Stair", "The Hanging Stair",
      "Kept name: scaffolds, cable lifts and outflow falls down the cliff beneath Zenith.",
      'Zenith/Nadir', [(19, 16)], [72, 150], [60, 28], 'SCRAPYARD',
      landmark="Cable lifts and shanty scaffolds.", wild="Magneton, Klang, Bisharp, Skuntank, Muk, Scrafty.",
      secret="A lift cage that stops between floors on purpose."),
    L(821, "Route 32", "The Drownings", "Nadir's name for the coast that went under with Aurelia.",
      'Zenith/Nadir', [(18, 19)], [120, 120], [50, 50], 'WATER_SURFACE', mode='sea',
      landmark="Tower-tops standing out of the Hallow Strait.",
      wild="Water with Poison or Dark: Tentacruel, Sharpedo, Toxapex, Dragalge.",
      secret="Dive below: Under the Drownings (822) and Aurelia.", side=[822, 824, 825, 826]),
  ]),
  dict(n=17, name="The Blind Road", frm=420, to=440, chapter="Act V", detail='outline',
       note="Borderland F again, underground: the river that runs east beneath Lumen's cliffs and surfaces in the "
            "Gloamwood, in Elowen's south-east.",
       legs=[
    L(852, None, "The Throat", "The tunnel that swallows the river at Underveil. Boats go in.",
      'Nadir', [(17, 18)], [64, 110], None, 'NEW_MOON', mode='under',
      landmark="The river mouth, in reverse.", wild="Dark and Poison.", secret="An air pocket with a smugglers' chapel."),
    L(840, "Route 33 - Rootdeep River", "The Blindwater",
      "The underground river. Nothing in it has eyes, and the boatmen sing so the walls know where they are.",
      'Nadir/Elowen', [(18, 18), (19, 18)], [150, 80], [56, 32], 'CAVE', mode='under',
      landmark="Root-arches over black water and the lamps of Mothwell.",
      wild="Cave water: Woobat, Toedscruel, Shiinotic, Basculin.",
      secret="A side channel that loops under Lumen's foundations.", side=[844, 845, 848]),
    L(841, "Route 34 - Gloamwood Verge", "The Gloamwood Verge",
      "Kept name: the edge of the twilight wood, where the river comes back into the light.",
      'Elowen', [(21, 17)], [72, 130], [32, 56], 'SILKWOOD',
      landmark="The river's rising and the first lantern-flowers.", wild="Fairy and Grass at dusk: Morgrem, Shiinotic, Trevenant.",
      secret="A clearing that is always one hour later than the rest."),
  ]),
  dict(n=18, name="The Truce Road", frm=440, to=460, chapter="Act V", detail='outline',
       note="Borderland J, the Thornwar Marches: twilight forest, burning forest, then the dragon ridge.",
       legs=[
    L(860, "Route 35 - Gloamwood", "The Gloamwood", "Kept name: Elowen's twilight wood in the south-east, where it has "
                                                   "been dusk for three hundred years.",
      'Elowen', [(23, 17)], [140, 80], [60, 32], 'FAIRY_TALE',
      landmark="The Great Tree on the skyline and paths that move.", wild="Fairy, Grass, Bug, high level.",
      secret="A path that only exists while you are not on it.", side=[868]),
    L(861, "Route 36 - Thornwar Marches", "The Thornwar Marches",
      "Kept name: where Elowen and Ashkaar fought the Thornwar. The trees still burn without dying.",
      'Elowen/Ashkaar', [(23, 16)], [80, 130], [32, 56], 'MOUNTAIN',
      landmark="Ember-leaved giants and Thornwar forts.",
      wild="Scovillain, Centiskorch, Volcarona, Talonflame, Leavanny, Flygon.",
      secret="A fort whose garrison never got the order to stand down."),
    L(872, None, "The Wyrmspine", "The ridge road to Wyrmrest, along a spine of rock that Ashkaar says is exactly that.",
      'Ashkaar', [(24, 14)], [150, 72], None, 'DRAGONS_DEN',
      landmark="The vertebral crags and the dragon roost-poles.", wild="Dragon and Fire, high level.",
      secret="A rib-cave with a clutch of eggs and a very calm mother.", side=[864, 865]),
  ]),
  dict(n=19, name="The Pilgrim Road", frm=460, to=480, chapter="Act V", detail='outline',
       note="Borderland K, now on Elowen ground: from the Dominion's toll-fort west over the Pilgrim Pass (eighteen "
            "shrines across the Sulfur Reach and the Leach) to Pilgrim's Rest, then through Sovereign's Ascent in the "
            "Crownwall's one gap and down the Coronation Road. Every road in Velmora ends on the Crown Road; only this "
            "one goes in.",
       legs=[
    L(892, None, "Dominar's Toll", "The Dominion taxes a holy road here, and has for three hundred years.",
      'Ashkaar', [(24, 12)], [110, 70], None, 'MOUNTAIN',
      landmark="The toll-fort across the whole valley.", wild="Fire, Dragon, Fighting.",
      secret="The toll-keeper's ledger lists one pilgrim who has paid every year since AF 0."),
    L(880, "Route 37 - Pilgrim Pass", "The Pilgrim Pass",
      "Kept name: eighteen shrines, one per Plate, from the Dominion's border to the Crownwall's gap.",
      'Elowen/Crownhaven', [(22, 12), (20, 11)], [140, 80], [32, 56], 'MOUNTAIN',
      landmark="The eighteen shrines, the pilgrim camps, and the south bridge over the Leach.",
      wild="Mixed, every type, high level.", secret="A nineteenth shrine, unfinished."),
    L(893, None, "The Coronation Road", "Walked once by each Sovereign, on foot, from the Ascent to the Eighteen Gates.",
      'Crownhaven', [(15, 10)], [150, 64], None, 'GRAND_STAGE',
      landmark="Statues of every Sovereign; the last plinth is empty.", wild="None on the road; Festival crowds.",
      secret="The empty plinth already has a name cut on the back.", side=[884, 885, 886, 888]),
  ]),
]

# ----------------------------------------------------------------------------- other renames (not route legs)
OTHER_RENAMES = {
    542: ("Marsh Rest House", "The Brinewife's Rest", "A salt-boiler's widow keeps a bed for anyone the marsh has soaked."),
    664: ("Mt. Cinder 1F", "The Cinderhorn 1F", "The volcano above Cindervault, named for its shape: a horn, still smoking."),
    665: ("Mt. Cinder 2F", "The Cinderhorn 2F", "As 664."),
    666: ("Mt. Cinder Caldera", "The Cinderhorn Caldera", "As 664."),
    822: ("Route 32 Seabed", "Under the Drownings", "The seabed below the Drownings: streets, with fish in them."),
}
# Geography v2 / Revision 18: the war moves onto land in Ossaria. These maps keep their IDs but are new places, so
# PLACE_NAMES marks them `replaced`: rename_places.py does NOT rewrite them in prose (the story lines that describe
# them are in design/GEOGRAPHY_V2_STORY_FIXES.md).
REPLACED = {
    582: ("Lumen South Gate", "Lumen West Gate", "Lumen's gate at the end of the Arc-Lamp Mile, facing the Crownlands."),
    920: ("The Rime Narrows", "The Rimed Sands",
          "Isenmar's front in the western dunes: sand its host has frozen into white trench-lines."),
    922: ("Skaldfast - Harbour Keep", "Skaldfast - Rime Keep", "Skaldfast's inner keep, built over a frozen spring."),
    925: ("The Steamline", "The Steamline",
          "No-man's-land in the dunes where the two Imprints meet: ice on one side, fire on the other, steam and glass between."),
    926: ("The Shattered Ice", "The Glass Dunes",
          "The war's battlefield: Kyogre drags a flood-sea into the desert and Reshiram's fire turns the dunes to glass."),
}
PROSE_ALIASES = [("Mt. Cinder", "the Cinderhorn")]

# ----------------------------------------------------------------------------- maps with their own town-map square
# (everything else sits on its road leg's or town's square, listed by `side` above / TOWN_EXTRA_IDS)
OWN_SQUARE = {
    522: (14, 16), 525: (12, 14), 546: (9, 14), 548: (10, 14), 544: (8, 16), 563: (6, 10), 564: (2, 8),
    568: (4, 15), 584: (4, 6), 588: (4, 8), 604: (15, 4), 628: (18, 3), 624: (16, 5), 644: (22, 13), 648: (19, 12),
    658: (22, 11), 663: (24, 5), 664: (25, 10), 668: (25, 7), 682: (8, 11), 684: (15, 14), 688: (17, 14),
    698: (10, 13), 699: (13, 14), 703: (12, 13), 704: (5, 5), 708: (8, 10), 723: (2, 6), 724: (19, 15), 728: (2, 3),
    742: (10, 6), 743: (25, 16), 744: (19, 13), 748: (18, 14), 764: (22, 5), 768: (29, 16), 783: (17, 2), 784: (19, 2),
    788: (18, 2), 804: (29, 17), 806: (29, 19), 808: (26, 19), 822: (17, 19), 824: (16, 19), 828: (21, 16),
    838: (14, 10), 844: (20, 17), 848: (18, 17), 864: (25, 14), 868: (22, 18), 884: (16, 10), 888: (13, 8),
    900: (13, 19), 905: (21, 19), 910: (28, 19), 920: (11, 2), 924: (15, 2), 925: (12, 1), 926: (13, 2),
    929: (13, 3), 930: (14, 3),
    959: (19, 14), 960: (13, 15), 961: (14, 16), 962: (16, 19), 963: (14, 9), 109: (12, 19), 110: (12, 19),
}
OWN_SQUARE_INHERIT = {545: 544, 547: 546, 565: 564, 585: 584, 605: 604, 625: 624, 645: 644, 665: 664, 666: 664,
                      685: 684, 705: 704, 725: 724, 726: 724, 745: 744, 746: 744, 765: 764, 785: 784, 805: 804,
                      825: 824, 826: 824, 845: 844, 865: 864, 885: 884, 886: 884, 901: 900, 523: (12, 16), 526: (11, 14),
                      928: 924}
EXTRA_POINTS = {  # town-map squares that name a place with no map yet (landmarks)
    (12, 19): "Hallow Strait", (26, 17): "The Grave Glass", (29, 17): "The Slagglass", (25, 16): "Mirror Mere",
}

# The Antumbra inset on the town map (squares x 25-29, y 15-19): the mirror realm has no place on the real map.
ANTUMBRA_INSET = (25, 15, 29, 19)


def all_legs():
    for r in ROADS:
        for l in r['legs']:
            yield r, l


def leg_by_id():
    return {l['id']: (r, l) for r, l in all_legs()}


# ----------------------------------------------------------------------------- road drawing order
# Each road: list of segments; a segment is a list of stops: a settlement id, a leg id (all its cells), 'P:<id>'
# (a dungeon's own square), 'pts:<NAME>' (a polyline from world_geo) or 'G:<letter>' (an Antumbra gate). style: road /
# under / sea / side.
GATES = {  # Antumbra gates: letter -> (real-map square, inset square, name)
    'A': ((10, 6), (25, 16), "Mirror Mere"),
    'B': ((20, 3), (26, 17), "the Grave Glass (Vigil)"),
    'C': ((21, 15), (29, 17), "the Slagglass (Slag Mesa)"),
}
# stops: a settlement id, a leg id (its cells in order), 'rev:<id>' (a leg's cells reversed), 'sq:x,y' (one square of a
# leg the road only touches), 'P:<id>' (a dungeon's own square), 'pts:<NAME>' (world_geo polyline), 'G:<letter>'.
# styles: road / side / under / sea / air (airship lane) / inset / ring (the Crown Road, drawn once).
ROAD_PATHS = {
    1: [('road', [100, 520, 527, 528, 140]), ('side', [520, 521])],
    2: [('road', [140, 541, 552, 540, 524, 120])],
    3: [('road', [120, 566, 577, 570, 578, 562, 561, 160]), ('side', [140, 560, 570])],
    4: [('road', [160, 580, 592, 590, 581, 595, 'sq:11,9']), ('road', ['sq:14,12', 593, 180])],
    5: [('road', [180, 612, 'sq:16,11']), ('road', ['sq:14,6', 600, 610, 'P:604', 601, 613, 200])],
    6: [('road', [200, 620, 632, 621, 630, 634, 633, 220])],
    7: [('road', [220, 640, 641, 650, 652, 240])],
    8: [('road', [240, 660, 661, 'sq:17,9']), ('road', ['sq:16,11', 672, 260]),
        ('side', [240, 662, 670, 673, 927])],
    9: [('road', [260, 692, 680, 690, 681, 693, 280]), ('road', ['sq:11,9', 681])],
    10: [('road', [280, 700, 701, 710, 'P:704', 712, 300])],
    11: [('road', [300, 720, 721, 730]), ('air', [730, 'P:724']), ('road', ['P:724', 732, 320])],
    12: [('road', [320, 740, 741, 750, 'sq:17,9']), ('road', ['sq:12,7', 752, 753, 'G:A']), ('inset', ['G:A', 755, 340])],
    13: [('inset', [340, 772, 'G:B']), ('road', ['G:B', 760, 761, 773, 360])],
    14: [('road', [360, 780, 770, 'G:B']), ('inset', ['G:B', 781, 790, 380]), ('side', [200, 810, 'P:926'])],
    15: [('inset', [380, 800, 'G:C']), ('road', ['G:C', 801, 811, 400])],
    16: [('road', [400, 832, 820, 830]), ('sea', [830, 821, 420])],
    17: [('road', [420, 852]), ('under', [852, 'pts:BLINDWATER', 850]), ('road', [850, 841, 440])],
    18: [('road', [440, 860, 861, 870, 872, 460])],
    19: [('road', [460, 892, 880, 890, 'P:884', 893, 480])],
}
# The Crown Road: the ring round the Crownwall that every cross-kingdom journey uses (Geography v2: "all roads lead to
# the Crown"). Four maps: Wallshadow Row (594, SW), Candle Down (602, SE), the Highwold (603, NE), Kingsmead (756, NW).
CROWN_ROAD = ['sq:11,9', 'sq:12,7', 'sq:14,6', 'sq:16,7', 'sq:17,9', 'sq:16,11', 'sq:14,12', 'sq:12,11', 'sq:11,9']
# legs a road walks that another road introduced (shown as "via" in the docs)
VIA = {8: [602], 12: [602, 603]}

# ----------------------------------------------------------------------------- kingdoms and borderlands (Geography v2)
KINGDOM_WHERE = {
    'Ossaria': 'the north: the bone sands along the north coast, the crags, and the war front in its western dunes',
    'Isenmar': 'the west and north-west: fjords, snowfields, the frozen sea and Rimeholt on Lake Rime',
    'Ashkaar': 'the east: basalt, ash plains, the Cinderhorn and the Wyrmspine; Cinder Cape at its north-east tip',
    'Elowen': 'the middle, from the south-west coast to the Gloamwood in the south-east; borders every kingdom',
    'Zenith': 'the south: the plateau of the City Above, Lumen on its south brink',
    'Nadir': 'beneath Zenith (the same footprint): the undercity, the marsh and mines at the plateau foot, the drowned '
             'south coast',
    'Crownhaven': "Elowen's heart, inside the Crownwall",
    'Antumbra': 'behind the glass: reached by gates A (Mirror Mere), B (the Grave Glass) and C (the Slagglass)',
}
# code: (name, kingdoms, town, member maps, biome, wild)
BORDERLANDS = {
    'A': ("The Rimewood", ('Elowen', 'Isenmar'), 570, [560, 562, 563, 577, 578],
          "The Gossamer's oldwood frozen in hoar: ice-glazed giant trees, frozen silk curtains, fells turning to frost "
          "north of Briarwick, salt flats turning to frost-flats along the coast road to Saltmere.",
          "Snover, Snom, Cubchoo, Swinub, Bergmite, Vanillite, Deerling, Stantler, Teddiursa, Smoochum, Delibird"),
    'A2': ("The Hoarwood", ('Elowen', 'Isenmar'), 710, [701],
           "The northern Rimewood: deep snow-forest of royal hunting lodges.", "as A + Abomasnow, Sawsbuck, Ursaring"),
    'B': ("The Icefall Locks", ('Isenmar', 'Elowen'), 590, [581, 584, 585, 592],
          "Where the Ebb falls off the Crownland downs onto Isenmar's frozen lowland: ice-falls cut into brass locks "
          "and sluices, frozen water-meadows, ice-cutters' sleds, Lattice pylons frozen into the ice.",
          "Magnemite, Pawmi, Wattrel, Tadbulb, Snover, Bergmite, Deerling, Wooloo"),
    'B2': ("The Mast Glacier", ('Isenmar', 'Ossaria'), 730, [721],
           "Tundra and permafrost dunes: a glacier tongue running out onto frozen sand, wind-carved ice-dunes, and "
           "airship masts anchored in the ice.",
           "Swinub, Piloswine, Cetoddle, Alolan Sandshrew, Snom, Hippopotas, Bergmite, Skarmory"),
    'C': ("The Brass Dunes", ('Elowen', 'Ossaria'), 610, [600, 604, 605],
          "Heath and dune scrub where the forest gives out: gorse and broom on the dune-feet, the buried Mainline, "
          "sand-scoured brass and a broken viaduct.",
          "Sandshrew, Silicobra, Hippopotas, Phanpy, Cacnea, Skwovet, Rufflet, Orthworm"),
    'D': ("The Leach Canyons", ('Ossaria', 'Elowen'), 630, [621],
          "Red sandstone gorges with gallery forest along the River Leach; bone-char filter towers.",
          "Sandile, Trapinch, Maractus, Gligar, Ekans, Skwovet, Deerling, Bramblin"),
    'E': ("The Sulfur Reach", ('Elowen', 'Ashkaar'), 650, [641, 661],
          "Ash woods and hot springs: scorched oaks around the sulfur lake, boiling yellow pools, the Ironway pass.",
          "Salandit, Charcadet, Numel, Houndour, Capsakid, Cyclizar, Bramblin, Fletchinder"),
    'F': ("The Rootdeep", ('Nadir', 'Elowen'), 690, [680, 840, 633, 672],
          "Under the plateau's foot: the Gossamer's roots through Nadir's mine shafts, glowing fungus, root-cathedrals; "
          "the roads that go down off the Crownland edge into Nadir (the Gutterfall under the north cliff, the Long "
          "Drop under the west rim); the Blindwater under the south coast. South hamlet: Mothwell (850).",
          "Foongus, Parasect, Shiinotic, Breloom, Toedscruel, Bramblin, Machoke, Scraggy"),
    'G': ("The Wired Wood", ('Zenith', 'Elowen'), 750, [593, 612, 741, 801],
          "Industrial fringe and orchards round the plateau: vine-wrapped pylons, clockwork orchards, greenhouse "
          "factories, the Mainline cutting, Cogsworth's slag on the Slag Mesa.",
          "Luxray, Boltund, Klang, Floette, Granbull, Tinkatuff, Applin, Bounsweet"),
    'H': ("The Looking-Glass Wood", ('Elowen', 'Antumbra'), 753, [742, 743, 752],
          "Reflections that disagree, rivers running uphill near Mirror Mere (gate A).", "Kirlia, Flittle, Rabsca, Ribombee"),
    'I': ("The Obsidian Barrows", ('Antumbra', 'Ossaria'), 770, [760],
          "A necropolis of obsidian tomb-mirrors that became gates (the Grave Glass, gate B); shadows fall upward.",
          "Palossand, Golurk, Claydol, Runerigus, Inkay, Absol, Houndstone"),
    'J': ("The Thornwar Marches", ('Elowen', 'Ashkaar'), 870, [861],
          "Ash woods and burnt forest: ash-grey giants with ember leaves that burn without dying, charcoal clearings, "
          "Thornwar forts.", "Scovillain, Centiskorch, Volcarona, Talonflame, Leavanny, Flygon"),
    'K': ("The Pilgrim Pass", ('Elowen', 'Crownhaven'), 890, [880],
          "Eighteen roadside shrines from the Dominion's border to the Crownwall's gap; pilgrim camps of every kingdom.",
          "mixed, high level"),
    'L': ("The Hanging Stair", ('Zenith', 'Nadir'), 830, [820, 821],
          "The cliff under the plateau's south rim: cable lifts, outflow falls, shanty scaffolds, the drowned coast.",
          "Magneton, Klang, Bisharp, Skuntank, Muk, Scrafty"),
    'M': ("The Cinderglass Barrens", ('Ashkaar', 'Ossaria'), 670, [662, 663],
          "Volcanic ash desert: obsidian dunes, a petrified ash forest, lava tubes, glass-storms.",
          "Carkol, Magcargo, Torkoal, Vibrava, Gible, Sudowoodo, Onix, Rhyhorn, Golett"),
}
# the war in the sands (Revision 18): fire and ice meet only on neutral Ossarian ground
WAR = {
    'theatre': [920, 921, 922, 923, 924, 925, 926, 927],
    'isenmar': "from Rimeholt along the Thane's Sled-Road and over the Mast Glacier to Skaldfast, then east into the "
               "dunes (the Rimed Sands)",
    'ashkaar': "from Cindervault's north gate through the Cinderglass Barrens and Glasswake, then west across the bone "
               "sands to the Ashkaar Siege Camp; Cinder Cape Warfort is the staging fortress on the north-east coast",
    'front': "the Steamline, where the two Imprints meet; the battlefield is the Glass Dunes",
}

GYMS = [140, 120, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 420, 440, 460]   # gym n = GYMS[n-1]

# one-line origins for the kept settlement names (PLACE_NAMES.md)
SETTLEMENT_ORIGINS = {
    100: "The ferry lands here and nowhere else; Old Ferrow ran the first boat across the Hallow Strait.",
    140: "A salt lake behind a sandbar: the town's wealth and its name. Elowen's chartered free port.",
    120: "Briar-wick, the dairy-farm in the briars, before the weavers came and the farm became a loom-town.",
    160: "Where the River Ebb meets the sea, and where the Ebb runs both ways.",
    180: "The first city lit all night; Zenith named it for the light and has not let anyone forget.",
    200: "Dune-holt: the hold among the dunes, carved into canyon walls by the first Electors.",
    220: "The mire-fen at the foot of Zenith's outfall; the name is a description, not a boast.",
    240: "The vault of cinders: the Dominion's seat in the caldera rim, built on the ash of the old one.",
    260: "Iron-reach: as far down as the iron goes, and then the pit-fighters went further.",
    280: "Green-ance: the Evergreen Crown's seat, where nothing has wilted in three hundred years.",
    300: "Rime-holt: the hold on the rime, a fortress-port standing on Lake Rime's ice.",
    320: "The spire that reaches the sky-roads; Zenith's airship port.",
    340: "The light that comes from nowhere in the kingdom behind the glass.",
    360: "Crag-holm: the island of rock in the crags, where Ossaria cut its lift-galleries.",
    380: "The grave-moor: Antumbra buries above ground and walks below it.",
    400: "Named for the cog-works of its founding patent and the worth of what it makes.",
    420: "Under the veil of the sea, in the upper towers of drowned Aurelia.",
    440: "The town in the Gloamwood, Elowen's twilight south-east, where it has been dusk for three hundred years.",
    460: "Where the wyrms rest: the roost-citadel on the Wyrmspine.",
    480: "The haven of the Crown: the Accord's capital, the only city all seven kingdoms agreed to.",
    570: "Frost-wick, the frost farm: Elowen named it for the cold and Isenmar for the farm.",
    590: "Where the brass meets the falls: the Icefall Locks' company town.",
    610: "Copper in the dunes: the railway's caravanserai where the line went under the sand.",
    630: "Char-well: the well that bone-char keeps clean.",
    650: "Scald-water: the hot springs of the Sulfur Reach, and their temper.",
    670: "The glass-wake: the black glass a lava flow leaves behind it, and the furnace town that sells it.",
    690: "Lantern-root: the glowing roots the miners read their way by.",
    710: "Snow-briar: the royal lodge in the frozen bride-briar hedges.",
    730: "Anchor-hold: where the airships are anchored to the glacier.",
    750: "Verdigris: the green that copper turns in the rain, and the town that is both.",
    753: "Glass-mere: the lake that shows you the wrong sky.",
    770: "The watch kept over the dead, and the town that keeps it.",
    830: "Midway up the Hanging Stair.",
    850: "The moths that come to the lamps of the underground river.",
    870: "Thorn-watch: the watchtower of the Thornwar, still manned.",
    890: "The last rest before the Crownwall, where every kingdom's pilgrims sleep in the same hall.",
    921: "Skald-fast: the skalds' fastness, Isenmar's oldest fort, on the edge of the bone sands where the thanes "
         "first stood against the desert. The besieged Isenmar fortress of the war.",
    927: "The Dominion's warfort on the Cape of Cinders: the staging fortress for the war in the sands.",
    928: "The Dominar's war-tent: red lacquer, an oath-brazier and a map table, pitched at the heart of the Siege Camp.",
    929: "A flat-topped sandstone mesa behind the lines, where Meridian's observers set up their instruments.",
    930: "Where Ossaria's burial guild camps at the edge of the war, under the white bone-banner both armies let pass.",
}
