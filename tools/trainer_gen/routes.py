import re
# Route / gym trainers (stock trainer types). moves=None -> level-up moveset (always level-legal).
# Field touches (Revision 10): each map's default field is in design/FIELD_DEFAULTS.yaml; trainers get one or two
# field-aware choices (an ability the field switches on, a boosted level-up move, rarely a seed). The per-map notes
# below say which. Explicit movesets only use moves the species knows by level-up at that level.
def ROUTES(P):
    def m(sp, lv, ab, nat, moves=None, item=None):
        return P(sp, lv, ab, item, nat, moves, "A", casual=({"item": None} if item else None))
    R = []
    # ---------------------------------------------------------------------------------------------------------------
    # Level plan per MAP ID (SPINE Revision 14 swapped Saltmere and Briarwick: Ferrow's Landing -> coast -> Saltmere
    # (Gym 1, cap 15) -> inland -> Gossamer Wood / Briarwick (Gym 2, cap 19) -> north -> Rimewood / Frostwick ->
    # Ebbmouth (Gym 3, cap 23)). The teams below are written at their PRE-SWAP levels; PLAN shifts each map by `delta`,
    # sets the stretch cap (Hard = +1 level, never above it) and swaps species a shifted level would have evolved.
    # Which map sits on which stretch is PROVISIONAL until design/SWAP_GYM1_GYM2.md lands: edit one row here.
    # Map names change (design/PLACE_NAMES.md); the ids don't, so everything is keyed by map id.
    #   map id: (delta, cap, {OLD_SPECIES: (NEW_SPECIES, NEW_ABILITY or None)})
    PLAN = {
        # Gym 1 stretch, cap 15: route trainers lv 4-12, gym trainers 11-13 (BALANCE 2)
        520: (0, 15, {}),                                     # coastal heath out of Ferrow's Landing, 4-6
        541: (-6, 15, {}),                                    # the coast road to Saltmere (beach), 8-10
        544: (-5, 15, {}), 545: (-5, 15, {}),                 # Brinecut Mine (optional, Rock Smash later), 9-12
        151: (-5, 15, {"HERDIER": ("LILLIPUP", "VITALSPIRIT")}), 152: (-5, 15, {"HERDIER": ("LILLIPUP", "VITALSPIRIT")}),
        153: (-5, 15, {}),                                    # Pell Playhouse = Gym 1 actors, 11-13
        145: (-1, 19, {}),                                    # Pageant Hall grunts, after Gym 1, 15-16
        # Gym 2 stretch, cap 19: route trainers 15-17, gym trainers 15-17
        540: (3, 19, {}),                                     # river meadows inland from Saltmere, 15-17
        546: (2, 19, {}),                                     # Thistledown Manor (optional), 16-17
        521: (9, 19, {"SHINX": ("LUXIO", None)}),             # orchard country into the forest, 15-16
        524: (8, 19, {"BLIPBUG": ("DOTTLER", None), "SEEDOT": ("NUZLEAF", None)}),   # Gossamer Wood, 16-18
        131: (4, 19, {"SPEWPA": ("VIVILLON", "SHIELDDUST"), "TAROUNTULA": ("SPIDOPS", None)}),
        132: (4, 19, {"TAROUNTULA": ("SPIDOPS", None)}),       # Loomhouse = Gym 2 trainers, 15-17
        # Gym 3 stretch, cap 23
        525: (8, 23, {"LEDYBA": ("LEDIAN", None)}),            # Gossamer Deepwood, after Gym 2, 19-20
    }
    DEFAULT_CAP = 23                                          # 560-564, 170-173: unchanged (Gym 3 stretch)
    def t(note, tt, nm, lose, mons, cap=None):
        mid = int(re.match(r"Map (\d+)", note).group(1))
        delta, pcap, swaps = PLAN.get(mid, (0, DEFAULT_CAP, {}))
        out = []
        for mon in mons:
            mon = dict(mon, lv=max(2, mon["lv"] + delta))
            if mon["sp"] in swaps:
                sp, ab = swaps[mon["sp"]]
                mon = dict(mon, sp=sp, ab=ab or mon["ab"])
            out.append(mon)
        R.append((note, tt, nm, lose, out, cap if cap is not None else pcap))
    # Map 520 Route 1 (lv 4-6) - MEADOW: Run Away Pokemon dart into the grass (+1 Speed on entry)
    t("Map 520 Route 1", "YOUNGSTER", "Pip", "Aw, my squad lost!", [m("LILLIPUP", 4, "RUNAWAY", "JOLLY"), m("SKWOVET", 5, "CHEEKPOUCH", "IMPISH")])
    t("Map 520 Route 1", "LASS", "Wren", "My birdies! Oh, well done.", [m("PIKIPEK", 4, "KEENEYE", "ADAMANT"), m("FLETCHLING", 5, "BIGPECKS", "JOLLY")])
    # Route 1 trainers as the script (story/20_SCRIPT_CH0-2.md) and the generated map 520 name them
    t("Map 520 Route 1", "YOUNGSTER", "Pim", "The dream's fine. The Bidoof needs a minute.", [m("BIDOOF", 5, "SIMPLE", "JOLLY")])
    t("Map 520 Route 1", "LASS", "Dory", "It's judging me now.", [m("FLETCHLING", 5, "BIGPECKS", "ADAMANT")])
    # Map 521 Route 2 (lv 6-8) - MEADOW: Run Away, Leaf Guard (always on), Growth x2 tends it into a Flower Garden (Mae's Smoliv)
    t("Map 521 Route 2", "BUGCATCHER", "Dell", "My Metapod was supposed to evolve this time...", [m("CATERPIE", 6, "RUNAWAY", "HARDY"), m("METAPOD", 7, "SHEDSKIN", "IMPISH")])
    t("Map 521 Route 2", "CAMPER", "Joss", "Guess I'll go camp somewhere quieter.", [m("ZIGZAGOON", 6, "PICKUP", "JOLLY"), m("SHINX", 7, "INTIMIDATE", "ADAMANT")])
    t("Map 521 Route 2", "PICNICKER", "Mae", "You can have a sandwich anyway!", [m("FIDOUGH", 7, "OWNTEMPO", "IMPISH"), m("SMOLIV", 7, "EARLYBIRD", "MODEST")])
    # Map 524 Gossamer Wood (lv 8-10) - SILKWOOD: Swarm is always on, String Shot never misses (-3 Speed), Struggle Bug x1.5.
    # Camper Bram's Sizzlipede is deliberate: its Embers show the player "Embers are catching in the silk..." before the gym.
    t("Map 524 Gossamer Wood", "AROMALADY", "Petra", "What a lovely, fierce scent you have.", [m("CUTIEFLY", 8, "SHIELDDUST", "TIMID"), m("PETILIL", 9, "OWNTEMPO", "MODEST"), m("BUDEW", 9, "NATURALCURE", "MODEST")])
    t("Map 524 Gossamer Wood", "BUGCATCHER", "Reed", "The wood's full of better bugs than mine, huh.", [m("BLIPBUG", 8, "SWARM", "MODEST"), m("GRUBBIN", 9, "SWARM", "ADAMANT")])
    t("Map 524 Gossamer Wood", "BUGCATCHER", "Tobin", "Careful in the webs past here!", [m("SPINARAK", 9, "SWARM", "ADAMANT"), m("VENONAT", 10, "COMPOUNDEYES", "MODEST")])
    t("Map 524 Gossamer Wood", "CAMPER", "Bram", "Lost to a tourist. Don't tell anyone.", [m("SEEDOT", 8, "EARLYBIRD", "ADAMANT"), m("SHROOMISH", 9, "EFFECTSPORE", "ADAMANT"), m("SIZZLIPEDE", 10, "FLASHFIRE", "ADAMANT")])
    # Maps 131-132 Loomhouse Gym (lv 11-13) - SILKWOOD: Swarm bugs with String Shot / Bug Bite; Ranger Ash's Beautifly
    # holds a Telluric Seed (+1 Def, +1 Sp. Def, -1 Speed) so the player has seen a seed before Tamsin's Swadloon uses one.
    t("Map 131 Loomhouse Gym - Weaving Hall", "BUGCATCHER", "Milo", "Warden Tamsin's going to tie you in knots!", [m("SPEWPA", 11, "SHEDSKIN", "BOLD"), m("KRICKETUNE", 12, "SWARM", "ADAMANT")])
    t("Map 131 Loomhouse Gym - Weaving Hall", "LASS", "Fern", "Ah, you slipped right through my threads.", [m("CUTIEFLY", 11, "SHIELDDUST", "TIMID"), m("SEWADDLE", 12, "SWARM", "ADAMANT")])
    t("Map 132 Loomhouse Gym - Canopy Lofts", "BUGCATCHER", "Hollis", "My spiders never lose in the lofts... usually.", [m("TAROUNTULA", 12, "INSOMNIA", "ADAMANT"), m("SPINARAK", 12, "SWARM", "ADAMANT")])
    t("Map 132 Loomhouse Gym - Canopy Lofts", "POKEMONRANGER_M", "Ash", "You read the forest well. The Warden's above.", [m("DOTTLER", 12, "SWARM", "MODEST"), m("BEAUTIFLY", 13, "SWARM", "MODEST", "GUST,BUGBITE,ABSORB,STRINGSHOT", item="TELLURICSEED")])
    # Map 525 Gossamer Deepwood (lv 11-12) - SILKWOOD: Compound Eyes (x1.1 accuracy here), Swarm; Yanma glides (Bug-type Flying x1.2)
    t("Map 525 Gossamer Deepwood", "BUGCATCHER", "Linden", "The deepwood bugs are tougher than mine...", [m("NINCADA", 11, "COMPOUNDEYES", "ADAMANT"), m("LEDYBA", 11, "SWARM", "JOLLY"), m("RELLOR", 12, "COMPOUNDEYES", "IMPISH")])
    t("Map 525 Gossamer Deepwood", "POKEMONRANGER_F", "Sorrel", "Mind the glass trees. They're spreading.", [m("DEERLING", 11, "SAPSIPPER", "JOLLY"), m("SKIDDO", 12, "SAPSIPPER", "ADAMANT")])
    # Map 540 Route 3 (lv 12-14) - MEADOW: Run Away (Sentret, Doduo), Fairy Wind x1.5, Sunkern's Growth / Ingrain tend the meadow
    t("Map 540 Route 3", "FISHERMAN", "Hale", "Reeled in a loss. Happens.", [m("MAGIKARP", 12, "SWIFTSWIM", "HARDY"), m("GOLDEEN", 13, "SWIFTSWIM", "ADAMANT"), m("TYMPOLE", 13, "SWIFTSWIM", "MODEST")])
    t("Map 540 Route 3", "PICNICKER", "Bryony", "My flowers wilted! Oh well, picnic time.", [m("FLABEBE", 12, "FLOWERVEIL", "MODEST"), m("COTTONEE", 13, "PRANKSTER", "BOLD"), m("SUNKERN", 13, "CHLOROPHYLL", "MODEST")])
    t("Map 540 Route 3 (double battle)", "TWINS", "Bel & Bea", "Bel: We lost! Bea: Together, though!", [m("MANKEY", 13, "VITALSPIRIT", "JOLLY"), m("PANCHAM", 13, "IRONFIST", "ADAMANT")])
    t("Map 540 Route 3", "YOUNGSTER", "Corin", "My team's the coolest! ...Was.", [m("SENTRET", 12, "RUNAWAY", "JOLLY"), m("BIDOOF", 13, "SIMPLE", "ADAMANT"), m("DODUO", 14, "EARLYBIRD", "JOLLY")])
    # Map 541 Route 4 (beach, lv 14-16) - BEACH: Mud-Slap / Mud Shot x2 (Bunnelby, Nacli), Water x1.2, Sand Rush works in the sand
    t("Map 541 Route 4", "CAMPER", "Ned", "Sand in my tent AND I lost. Great day.", [m("BUNNELBY", 14, "CHEEKPOUCH", "ADAMANT"), m("NACLI", 15, "PURIFYINGSALT", "IMPISH")])
    t("Map 541 Route 4", "HIKER", "Dunstan", "Ho! Solid as Brinecut stone, you are.", [m("DWEBBLE", 15, "STURDY", "ADAMANT"), m("NACLI", 15, "PURIFYINGSALT", "IMPISH", "ROCKTHROW,MUDSHOT,SMACKDOWN,HARDEN"), m("CRABRAWLER", 16, "HYPERCUTTER", "ADAMANT")])
    t("Map 541 Route 4", "SAILOR", "Morrow", "Blow me down! The Dovetail crew'll hear of this.", [m("FINNEON", 15, "SWIFTSWIM", "JOLLY"), m("REMORAID", 15, "HUSTLE", "MODEST"), m("CRABRAWLER", 15, "IRONFIST", "ADAMANT")])
    t("Map 541 Route 4", "TUBER_F", "Pip", "Waaah! My floaty popped!", [m("SURSKIT", 14, "SWIFTSWIM", "TIMID"), m("MINCCINO", 15, "CUTECHARM", "JOLLY")])
    # Map 151-153 Pell Playhouse (Gym 2 actors, lv 15-18) - GRAND_STAGE: sound (Echoed Voice, Disarming Voice), showpieces
    # (Fake Out) and dances (Teeter Dance) raise the applause, so the player sees the stages climb before Dorian
    t("Map 151 Pell Playhouse - Revolving Stage", "JUGGLER", "Florian", "Dropped every pin! Bravo, though.", [m("MINCCINO", 15, "TECHNICIAN", "JOLLY", "ECHOEDVOICE,POUND,HELPINGHAND,BABYDOLLEYES"), m("SPINDA", 16, "OWNTEMPO", "ADAMANT")])
    t("Map 151 Pell Playhouse - Revolving Stage", "BEAUTY", "Rosalind", "The spotlight suits you better, darling.", [m("SKITTY", 16, "CUTECHARM", "TIMID", "FAKEOUT,ROUND,SING,TAILWHIP"), m("FLABEBE", 16, "FLOWERVEIL", "MODEST")])
    t("Map 151 Pell Playhouse - Revolving Stage", "JUGGLER", "Ambrose", "An encore? No? Fair.", [m("AIPOM", 16, "SKILLLINK", "JOLLY"), m("HERDIER", 17, "INTIMIDATE", "ADAMANT")])
    t("Map 152 Pell Playhouse - Fly Loft", "GENTLEMAN", "Reginald", "Splendid form. Dorian will be delighted.", [m("HERDIER", 17, "INTIMIDATE", "ADAMANT"), m("FURFROU", 17, "FURCOAT", "JOLLY")])
    t("Map 153 Pell Playhouse - Dressing Rooms", "JUGGLER", "Pierrot", "...(Pierrot mimes a dramatic faint.)", [m("AIPOM", 17, "PICKUP", "JOLLY"), m("SPINDA", 17, "TANGLEDFEET", "ADAMANT")])
    t("Map 153 Pell Playhouse - Dressing Rooms", "LADY", "Odette", "My costume is ruined. Worth it.", [m("BUNEARY", 17, "LIMBER", "JOLLY"), m("FURFROU", 18, "FURCOAT", "JOLLY")])
    # Map 145 Pageant Hall: tag battle vs both grunts (version 0 = this encounter; later grunt battles use 1, 2, ...)
    t("Map 145 Pageant Hall (tag battle with HOLLOW_GRUNT_F)", "HOLLOW_GRUNT_M", "Grunt", "Let the land grieve... ugh, not today.", [m("NICKIT", 16, "UNBURDEN", "JOLLY"), m("FOONGUS", 17, "EFFECTSPORE", "RELAXED")], cap=19)
    t("Map 145 Pageant Hall (tag battle with HOLLOW_GRUNT_M)", "HOLLOW_GRUNT_F", "Grunt", "The Plates are poison. You'll see.", [m("PHANTUMP", 16, "NATURALCURE", "ADAMANT"), m("MORELULL", 17, "EFFECTSPORE", "MODEST")], cap=19)
    # Map 544-545 Brinecut Mine (lv 14-17) - CAVE: Rock x1.5, Rock Tomb x1.5; Rock Head is safe from a cave-in
    t("Map 544 Brinecut Mine 1F", "BLACKBELT", "Taro", "Hah! My fists need more salt-mine training.", [m("MACHOP", 15, "GUTS", "ADAMANT"), m("TIMBURR", 16, "GUTS", "ADAMANT")])
    t("Map 544 Brinecut Mine 1F", "HIKER", "Bram", "Tunnels go on forever. So does losing, apparently.", [m("GEODUDE", 14, "ROCKHEAD", "ADAMANT"), m("ROGGENROLA", 15, "STURDY", "ADAMANT"), m("NACLI", 15, "PURIFYINGSALT", "IMPISH")])
    t("Map 545 Brinecut Mine B1F", "HIKER", "Gorse", "Deep enough down here to hear the sea. Well fought.", [m("ARON", 16, "ROCKHEAD", "ADAMANT"), m("NOSEPASS", 17, "STURDY", "IMPISH")])
    # Map 546 Thistledown Manor (haunted house, lv 14-15) - HOLLOW_CATHEDRAL: Lick always paralyzes, Night Shade x1.5,
    # Astonish x2, Cursed Body +1 Sp. Def on entry
    t("Map 546 Thistledown Manor", "CHANNELER", "Mireille", "The Players say... you were adequate. High praise.", [m("GASTLY", 14, "LEVITATE", "TIMID", "LICK,CONFUSERAY,HYPNOSIS,PAYBACK"), m("SHUPPET", 14, "CURSEDBODY", "ADAMANT"), m("SINISTEA", 15, "CURSEDBODY", "MODEST")])
    # Map 560 Route 5 (lv 16-19) - SNOWY_MOUNTAIN: Powder Snow x2, Ice Body heals without hail (no Snow Cloak on Standard)
    t("Map 560 Route 5", "BIKER", "Rook", "Not THAT Rook. Everybody asks.", [m("GLAMEOW", 17, "OWNTEMPO", "JOLLY"), m("TAUROS", 18, "INTIMIDATE", "JOLLY")])
    t("Map 560 Route 5", "PICNICKER", "Sela", "Okay, you win the last sandwich.", [m("SKITTY", 16, "CUTECHARM", "TIMID"), m("PHANPY", 17, "PICKUP", "ADAMANT")])
    t("Map 560 Route 5", "POKEMANIAC", "Ivo", "My precious monsters!", [m("CUBONE", 17, "ROCKHEAD", "ADAMANT"), m("KANGASKHAN", 19, "EARLYBIRD", "ADAMANT")])
    t("Map 560 Route 5", "RUINMANIAC", "Alder", "The old stones told me I'd lose. I never listen.", [m("HELIOPTILE", 17, "DRYSKIN", "TIMID"), m("DUNSPARCE", 18, "SERENEGRACE", "ADAMANT")])
    # Map 561 Route 6 (lv 17-20) - MOUNTAIN: Flying x1.2 and wind moves x1.3 for the cliff birds
    t("Map 561 Route 6", "BIRDKEEPER", "Wren", "My flock scattered! Well flown.", [m("TAILLOW", 17, "GUTS", "JOLLY"), m("DUCKLETT", 18, "KEENEYE", "MODEST"), m("CHATOT", 18, "KEENEYE", "MODEST")])
    t("Map 561 Route 6", "COOLTRAINER_F", "Astrid", "Cool. You'll do fine in the Tidelock.", [m("ORICORIO", 19, "DANCER", "TIMID"), m("CRAMORANT", 19, "GULPMISSILE", "MODEST"), m("SNORUNT", 19, "INNERFOCUS", "JOLLY")])
    t("Map 561 Route 6", "FISHERMAN", "Kjell", "The sea gives, the sea takes.", [m("MAGIKARP", 17, "SWIFTSWIM", "HARDY"), m("FINNEON", 18, "SWIFTSWIM", "TIMID"), m("WOOPER", 18, "DAMP", "IMPISH")])
    t("Map 561 Route 6", "SAILOR", "Haldor", "Arr! Isenmar's coast breeds tough kids.", [m("WINGULL", 18, "KEENEYE", "MODEST"), m("SPHEAL", 19, "THICKFAT", "MODEST")])
    # Map 564 Gullcry Caves (lv 19-20)
    t("Map 564 Gullcry Caves", "HIKER", "Torvald", "The gulls laugh at me every time.", [m("BINACLE", 19, "TOUGHCLAWS", "ADAMANT"), m("CLOBBOPUS", 20, "LIMBER", "ADAMANT")])
    # Maps 170-173 Tidelock Gym (Gym 3, lv 18-21) - WATER_SURFACE: Swift Swim and Hydration work without rain, Electric is
    # x1.5 against grounded targets (Chinchou). Sailor Bjorn's Chinchou holds an Elemental Seed (+1 Speed, Aqua Ring).
    t("Map 170 Tidelock Gym - Lock Hall", "FISHERMAN", "Gunnar", "Lock's open. Mind the current.", [m("GOLDEEN", 18, "SWIFTSWIM", "ADAMANT"), m("BARBOACH", 19, "HYDRATION", "ADAMANT")])
    t("Map 171 Tidelock Gym - Basins (Low Water)", "SWIMMER_F", "Ingrid", "You swim like you were born here.", [m("BUIZEL", 19, "SWIFTSWIM", "JOLLY"), m("CHEWTLE", 19, "STRONGJAW", "ADAMANT")])
    t("Map 172 Tidelock Gym - Basins (Mid Water)", "FISHERMAN", "Oskar", "Hooked a loss. Marisol'll laugh.", [m("BARBOACH", 20, "OBLIVIOUS", "ADAMANT"), m("CORPHISH", 20, "HYPERCUTTER", "ADAMANT")])
    t("Map 172 Tidelock Gym - Basins (Mid Water)", "SWIMMER_M", "Leif", "Ugh, the water's rising. So's my shame.", [m("ARROKUDA", 20, "SWIFTSWIM", "ADAMANT"), m("PSYDUCK", 20, "SWIFTSWIM", "MODEST")])
    t("Map 173 Tidelock Gym - Basins (High Water)", "SAILOR", "Bjorn", "The Warden's pool is next. Good luck, sprat.", [m("WINGULL", 20, "KEENEYE", "MODEST"), m("CHINCHOU", 21, "VOLTABSORB", "MODEST", "SPARK,BUBBLEBEAM,CONFUSERAY,THUNDERWAVE", item="ELEMENTALSEED")])
    # Map 990 test arena dummy
    t("Map 990 Prismfall Test Arena (dummy)", "YOUNGSTER", "Prismtest", "Testing, testing... you win!",
      [m("SNORLAX", 50, "THICKFAT", "HARDY", "TACKLE,DEFENSECURL,REST,SNORE")], cap=50)
    # Trainers the generated maps use that were missing (playtest, 2026-11-17)
    t("Map 521 Route 2", "BUGCATCHER", "Wim", '...Assistant Warden.', [m("SPINARAK", 6, "SWARM", "ADAMANT"), m("COMBEE", 7, "HONEYGATHER", "HASTY")])
    t("Map 521 Route 2", "PICNICKER", "Ada", 'Bless you. Bless both of us.', [m("ODDISH", 6, "RUNAWAY", "MODEST"), m("BUDEW", 7, "LEAFGUARD", "MODEST")])
    t("Map 524 Gossamer Wood", "TWINS", "Mo & Jo", 'We lost together!', [m("KARRABLAST", 9, "SWARM", "ADAMANT"), m("SHELMET", 9, "HYDRATION", "BOLD")])
    t("Map 131 Loomhouse Gym - Weaving Hall", "BUGCATCHER", "Nell", "Knotted up. Tamsin'll untangle you.", [m("SEWADDLE", 11, "SWARM", "ADAMANT"), m("SPINARAK", 12, "SWARM", "ADAMANT")])
    t("Map 131 Loomhouse Gym - Weaving Hall", "LASS", "Orla", 'See? Never the red shuttle first.', [m("LEDYBA", 11, "SWARM", "JOLLY"), m("SPEWPA", 12, "SHEDSKIN", "BOLD")])
    t("Map 131 Loomhouse Gym - Weaving Hall", "GENTLEMAN", "Bram", 'Sorry. No, wait, you won. Well done.', [m("VENONAT", 12, "COMPOUNDEYES", "MODEST"), m("SEWADDLE", 13, "SWARM", "ADAMANT")])
    t("Map 525 Gossamer Deepwood", "POKEMANIAC", "Ferris", 'That one hummed. Did you hear it hum?', [m("PARAS", 11, "EFFECTSPORE", "ADAMANT"), m("NINCADA", 11, "COMPOUNDEYES", "JOLLY"), m("YANMA", 12, "SPEEDBOOST", "MODEST")])
    t("Map 560 Route 5", "LASS", "Tilde", 'My Swinub slid farther than me.', [m("SWINUB", 16, "OBLIVIOUS", "ADAMANT"), m("SNOM", 17, "SHIELDDUST", "MODEST")])
    t("Map 560 Route 5", "SAILOR", "Haakon", "Ice'll break by summer. Probably.", [m("SPHEAL", 17, "ICEBODY", "MODEST"), m("CETODDLE", 18, "THICKFAT", "ADAMANT")])
    t("Map 560 Route 5", "BIRDKEEPER", "Ailsa", "Frostwick's gulls wear little ice hats. Not really.", [m("WINGULL", 17, "KEENEYE", "MODEST"), m("DELIBIRD", 18, "HUSTLE", "JOLLY")])
    # Map 562 The Rimewood - SILKWOOD under snow: Bug x1.5 (Snom, Tarountula), String Shot never misses
    t("Map 562 The Rimewood", "BUGCATCHER", "Pell", 'They were NOT happy to be woken.', [m("SNOM", 18, "SHIELDDUST", "MODEST"), m("TAROUNTULA", 19, "INSOMNIA", "ADAMANT")])
    t("Map 562 The Rimewood", "POKEMONRANGER_F", "Orla", "You'll do. Mind the silk curtains, they cut.", [m("DEERLING", 18, "SAPSIPPER", "JOLLY"), m("SNOVER", 19, "SNOWWARNING", "MODEST"), m("STANTLER", 20, "INTIMIDATE", "ADAMANT")])
    t("Map 562 The Rimewood", "HIKER", "Ulf", 'Ha! No, no traps for you.', [m("TEDDIURSA", 18, "PICKUP", "ADAMANT"), m("BERGMITE", 19, "OWNTEMPO", "IMPISH")])
    t("Map 562 The Rimewood", "CAMPER", "Rook", "...Is that what the aurora's for?", [m("CUBCHOO", 18, "SNOWCLOAK", "ADAMANT"), m("SNEASEL", 19, "INNERFOCUS", "JOLLY")])
    t("Map 562 The Rimewood", "TWINS", "Ana & Ida", 'Two of us lost! Two kingdoms of losing!', [m("MORELULL", 19, "EFFECTSPORE", "MODEST"), m("SNORUNT", 19, "INNERFOCUS", "JOLLY")])
    t("Map 563 Rimewood Glade", "POKEMONRANGER_M", "Sigurd", '...So you cut your way in. Fair.', [m("STANTLER", 19, "INTIMIDATE", "ADAMANT"), m("CRYOGONAL", 20, "LEVITATE", "CALM", "ICESHARD,RAPIDSPIN,ICYWIND,CONFUSERAY")])  # FROZEN_LAKE: Rapid Spin skates (x1.5), Icy Wind -2 Speed
    return R
