import re
# Route / gym trainers (stock trainer types). moves=None -> level-up moveset (always level-legal).
# Field touches (Revision 10): each map's default field is in design/FIELD_DEFAULTS.yaml; trainers get one or two
# field-aware choices (an ability the field switches on, a boosted level-up move, rarely a seed). The per-map notes
# below say which. Explicit movesets only use moves the species knows by level-up at that level.
def ROUTES(P):
    def m(sp, lv, ab, nat, moves=None, item=None, **kw):   # kw: only="nocasual" / "hard", form=, nick= (gen.P)
        return P(sp, lv, ab, item, nat, moves, "A", casual=({"item": None} if item else None), **kw)
    R = []
    # ---------------------------------------------------------------------------------------------------------------
    # Level plan per MAP ID (SPINE Revision 14 swapped Saltmere and Briarwick: Ferrow's Landing -> coast -> Saltmere
    # (Gym 1, cap 15) -> inland -> Gossamer Wood / Briarwick (Gym 2, cap 19) -> north -> Rimewood / Frostwick ->
    # Ebbmouth (Gym 3, cap 23)). The teams below are written at their PRE-SWAP levels; PLAN shifts each map by `delta`,
    # sets the stretch cap (Hard = +1 level, never above it) and swaps species a shifted level would have evolved.
    # Which map sits on which stretch is PROVISIONAL until design/SWAP_GYM1_GYM2.md lands: edit one row here.
    # Map names change (design/PLACE_NAMES.md); the ids don't, so everything is keyed by map id.
    #   map id: (delta, cap, {OLD_SPECIES: (NEW_SPECIES, NEW_ABILITY or None)})
    # Final per design/SWAP_GYM1_GYM2.md section 0 ("segment" = badges held when the map is first reachable).
    PLAN = {
        # Segment 0, cap 15. Ch1: 520 Ferrymen's Mile, 521 Windfall Row (keeps its Ch1 trainers at 6-8).
        # Ch2: 527 Lacecliff Walk / 528 Marram Down (the Strand Road, 8-12), 154 Pell Playhouse auditorium actors (10-13).
        520: (0, 15, {}), 521: (0, 15, {}), 527: (0, 15, {}), 528: (0, 15, {}),
        154: (-5, 15, {}),                                    # Florian, Rosalind, Ambrose (written as map 151 before); lose texts = the Ch1 script's [after] lines
        # Segment 1, cap 19 (Ch2 after Gym 1, and the Ch3 Weavers' Road to Briarwick)
        145: (-1, 19, {}),                                    # Pageant Hall grunts, after Gym 1, 15-16
        541: (0, 19, {}), 544: (0, 19, {}), 545: (0, 19, {}), # the Grey Saltings, Brinecut Mine (14-17)
        552: (0, 19, {}),                                     # the Dyers' Ford (15-17)
        540: (3, 19, {}),                                     # Thistledown Lea, 15-17
        546: (2, 19, {}),                                     # Thistledown Manor (optional), 16-17
        524: (8, 19, {"BLIPBUG": ("DOTTLER", None), "SEEDOT": ("NUZLEAF", None)}),   # Gossamer Wood, 16-18
        131: (4, 19, {"SPEWPA": ("VIVILLON", "SHIELDDUST"), "TAROUNTULA": ("SPIDOPS", None)}),   # Weaving Hall, 15-17
        # Segment 2, cap 23 (after Badge 2)
        132: (8, 23, {"TAROUNTULA": ("SPIDOPS", None)}),       # Loomhouse Upper Lofts (optional), 20-21
        152: (3, 23, {}), 153: (3, 23, {}),                   # Playhouse Backstage D9 (optional), 20-21
        525: (8, 23, {"LEDYBA": ("LEDIAN", None)}),            # Gossamer Deepwood, 19-20
        577: (0, 23, {}), 578: (0, 23, {}),                   # Frostwick Pass 17-20, Rimewood Path 18-21 (map builder 13's cells, round 4)
        # Segment 3, cap 27 (Gym 4, Lumen): the Circuit Gym's six (Ch5 Wave 0 rescue, 2026-11-23)
        190: (0, 27, {}), 191: (0, 27, {}), 192: (0, 27, {}),
        # --- Coverage fill and the Ch5-Ch13 density retrofit (2026-11-25; design/TRAINER_COVERAGE.md). chapter = segment + 2;
        # route trainers sit at previous cap - 2 .. cap - 3, gym and dungeon trainers at cap - 4 .. cap - 1 (BALANCE.md 2).
        # Coverage fill, Ch5 (segment 3, cap 27)
        580: (0, 27, {}), 581: (0, 27, {}), 584: (0, 27, {}), 590: (0, 27, {}), 592: (0, 27, {}), 593: (0, 27, {}), 594: (0, 27, {}), 595: (0, 27, {}),
        # Coverage fill, Ch6 (segment 4, cap 31)
        208: (0, 31, {}), 210: (0, 31, {}), 211: (0, 31, {}), 212: (0, 31, {}), 600: (0, 31, {}), 601: (0, 31, {}), 602: (0, 31, {}), 603: (0, 31, {}),
        604: (0, 31, {}), 605: (0, 31, {}), 612: (0, 31, {}), 613: (0, 31, {}),
        # Coverage fill, Ch7 (segment 5, cap 35)
        230: (0, 35, {}), 231: (0, 35, {}), 232: (0, 35, {}), 620: (0, 35, {}), 621: (0, 35, {}), 624: (0, 35, {}), 628: (0, 35, {}), 632: (0, 35, {}),
        633: (0, 35, {}), 634: (0, 35, {}),
        # Coverage fill, Ch8 (segment 6, cap 39)
        250: (0, 39, {}), 251: (0, 39, {}), 252: (0, 39, {}), 254: (0, 39, {}), 640: (0, 39, {}), 641: (0, 39, {}), 644: (0, 39, {}), 645: (0, 39, {}),
        648: (0, 39, {}), 652: (0, 39, {}), 658: (0, 39, {}),
        # Coverage fill, Ch9 (segment 7, cap 43)
        263: (0, 43, {}), 270: (0, 43, {}), 271: (0, 43, {}), 272: (0, 43, {}), 273: (0, 43, {}), 660: (0, 43, {}), 661: (0, 43, {}), 662: (0, 43, {}),
        663: (0, 43, {}), 664: (0, 43, {}), 665: (0, 43, {}), 666: (0, 43, {}), 668: (0, 43, {}), 672: (0, 43, {}), 673: (0, 43, {}),
        # Coverage fill, Ch10 (segment 8, cap 47)
        289: (0, 47, {}), 290: (0, 47, {}), 291: (0, 47, {}), 292: (0, 47, {}), 680: (0, 47, {}), 681: (0, 47, {}), 682: (0, 47, {}), 684: (0, 47, {}),
        685: (0, 47, {}), 688: (0, 47, {}), 692: (0, 47, {}), 693: (0, 47, {}),
        # Coverage fill, Ch11 (segment 9, cap 51)
        310: (0, 51, {}), 311: (0, 51, {}), 312: (0, 51, {}), 700: (0, 51, {}), 701: (0, 51, {}), 703: (0, 51, {}), 704: (0, 51, {}), 705: (0, 51, {}),
        708: (0, 51, {}), 712: (0, 51, {}),
        # Coverage fill, Ch12 (segment 10, cap 55)
        330: (0, 55, {}), 331: (0, 55, {}), 332: (0, 55, {}), 720: (0, 55, {}), 721: (0, 55, {}), 723: (0, 55, {}), 724: (0, 55, {}), 725: (0, 55, {}),
        726: (0, 55, {}), 728: (0, 55, {}), 732: (0, 55, {}),
        # Coverage fill, Ch13 (segment 11, cap 59)
        345: (0, 59, {}), 350: (0, 59, {}), 351: (0, 59, {}), 352: (0, 59, {}), 353: (0, 59, {}), 355: (0, 59, {}), 740: (0, 59, {}), 741: (0, 59, {}),
        742: (0, 59, {}), 743: (0, 59, {}), 744: (0, 59, {}), 745: (0, 59, {}), 748: (0, 59, {}), 752: (0, 59, {}), 755: (0, 59, {}), 756: (0, 59, {}),
        # Ch14 script roster (story density sections, 2026-11-26)
        360: (0, 63, {}), 370: (0, 63, {}), 371: (0, 63, {}), 372: (0, 63, {}), 760: (0, 63, {}), 761: (0, 63, {}), 764: (0, 63, {}), 765: (0, 63, {}),
        772: (0, 63, {}), 773: (0, 63, {}), 783: (0, 67, {}), 810: (0, 67, {}),
        # Ch15 script roster (story density sections, 2026-11-26)
        392: (0, 67, {}), 780: (0, 67, {}), 781: (0, 67, {}), 790: (0, 67, {}), 800: (0, 71, {}), 804: (0, 71, {}),
        # Coverage fill, Ch19 (segment 17, cap 85)
        861: (0, 85, {}), 864: (0, 85, {}),
    }
    DEFAULT_CAP = 23                                          # 560-564, 170-173: unchanged (Gym 3 stretch)
    def t(note, tt, nm, lose, mons, cap=None, v=0):   # v: a version for a name that returns (Hiker Dunstan, Ch2 -> Ch14)
        mid = int(re.match(r"Map (\d+)", note).group(1))
        delta, pcap, swaps = PLAN.get(mid, (0, DEFAULT_CAP, {}))
        out = []
        for mon in mons:
            mon = dict(mon, lv=max(2, mon["lv"] + delta))
            if mon["sp"] in swaps:
                sp, ab = swaps[mon["sp"]]
                mon = dict(mon, sp=sp, ab=ab or mon["ab"])
            out.append(mon)
        R.append((note, tt, nm, lose, out, cap if cap is not None else pcap) + ((v,) if v else ()))
    # Map 520 The Ferrymen's Mile (lv 4-6) - MEADOW: Run Away Pokemon dart into the grass (+1 Speed on entry)
    t("Map 520 The Ferrymen's Mile", "YOUNGSTER", "Pip", "Aw, my squad lost!", [m("LILLIPUP", 4, "RUNAWAY", "JOLLY"), m("SKWOVET", 5, "CHEEKPOUCH", "IMPISH")])
    t("Map 520 The Ferrymen's Mile", "LASS", "Wren", "My birdies! Oh, well done.", [m("PIKIPEK", 4, "KEENEYE", "ADAMANT"), m("FLETCHLING", 5, "BIGPECKS", "JOLLY")])
    # The Ferrymen's Mile trainers as the script (story/20_SCRIPT_CH0-2.md) and the generated map 520 name them
    t("Map 520 The Ferrymen's Mile", "YOUNGSTER", "Pim", "The dream's fine. The Bidoof needs a minute.", [m("SCATTERBUG", 4, "SHIELDDUST", "MODEST", only="nocasual"), m("BIDOOF", 5, "SIMPLE", "JOLLY")])
    t("Map 520 The Ferrymen's Mile", "LASS", "Dory", "It's judging me now.", [m("FLETCHLING", 5, "BIGPECKS", "ADAMANT")])
    # Map 521 Windfall Row (lv 6-8) - MEADOW: Run Away, Leaf Guard (always on), Growth x2 tends it into a Flower Garden (Mae's Smoliv)
    t("Map 521 Windfall Row", "BUGCATCHER", "Dell", "My Metapod was supposed to evolve this time...", [m("WEEDLE", 6, "SHIELDDUST", "HARDY", only="nocasual"), m("CATERPIE", 6, "RUNAWAY", "HARDY"), m("METAPOD", 7, "SHEDSKIN", "IMPISH")])
    t("Map 521 Windfall Row", "CAMPER", "Joss", "Guess I'll go camp somewhere quieter.", [m("ZIGZAGOON", 6, "PICKUP", "JOLLY"), m("SHINX", 7, "INTIMIDATE", "ADAMANT")])
    t("Map 521 Windfall Row", "PICNICKER", "Mae", "You can have a sandwich anyway!", [m("FIDOUGH", 7, "OWNTEMPO", "IMPISH"), m("SMOLIV", 7, "EARLYBIRD", "MODEST")])
    # Map 524 Gossamer Wood (lv 8-10) - SILKWOOD: Swarm is always on, String Shot never misses (-3 Speed), Struggle Bug x1.5.
    # Camper Bram's Sizzlipede is deliberate: its Embers show the player "Embers are catching in the silk..." before the gym.
    t("Map 524 Gossamer Wood", "AROMALADY", "Petra", "What a lovely, fierce scent you have.", [m("CUTIEFLY", 8, "SHIELDDUST", "TIMID"), m("PETILIL", 9, "OWNTEMPO", "MODEST"), m("BUDEW", 9, "NATURALCURE", "MODEST")])
    t("Map 524 Gossamer Wood", "BUGCATCHER", "Reed", "The wood's full of better bugs than mine, huh.", [m("BLIPBUG", 8, "SWARM", "MODEST"), m("GRUBBIN", 9, "SWARM", "ADAMANT")])
    t("Map 524 Gossamer Wood", "BUGCATCHER", "Tobin", "Careful in the webs past here!", [m("SPEWPA", 8, "SHEDSKIN", "BOLD", "TACKLE,STRINGSHOT,STUNSPORE,PROTECT", only="nocasual"), m("SPINARAK", 9, "SWARM", "ADAMANT"), m("VENONAT", 10, "COMPOUNDEYES", "MODEST")])
    t("Map 524 Gossamer Wood", "CAMPER", "Bram", "Lost to a tourist. Don't tell anyone.", [m("SEEDOT", 8, "EARLYBIRD", "ADAMANT"), m("SHROOMISH", 9, "EFFECTSPORE", "ADAMANT"), m("SIZZLIPEDE", 10, "FLASHFIRE", "ADAMANT")])
    # Maps 131-132 Loomhouse Gym (lv 11-13) - SILKWOOD: Swarm bugs with String Shot / Bug Bite; Ranger Ash's Beautifly
    # holds a Telluric Seed (+1 Def, +1 Sp. Def, -1 Speed) so the player has seen a seed before Tamsin's Swadloon uses one.
    t("Map 131 Loomhouse Gym - Weaving Hall", "BUGCATCHER", "Milo", "Warden Tamsin's going to tie you in knots!", [m("KRICKETOT", 11, "SHEDSKIN", "ADAMANT", only="nocasual"), m("SPEWPA", 11, "SHEDSKIN", "BOLD"), m("KRICKETUNE", 12, "SWARM", "ADAMANT")])
    t("Map 131 Loomhouse Gym - Weaving Hall", "LASS", "Fern", "Ah, you slipped right through my threads.", [m("BLIPBUG", 11, "SWARM", "MODEST", only="nocasual"), m("CUTIEFLY", 11, "SHIELDDUST", "TIMID"), m("SEWADDLE", 12, "SWARM", "ADAMANT")])
    t("Map 132 Loomhouse - Upper Lofts (after Badge 2)", "BUGCATCHER", "Hollis", "My spiders never lose in the lofts... usually.", [m("TAROUNTULA", 12, "INSOMNIA", "ADAMANT"), m("SPINARAK", 12, "SWARM", "ADAMANT")])
    t("Map 132 Loomhouse - Upper Lofts (after Badge 2)", "POKEMONRANGER_M", "Ash", "You read the forest well. The Warden's above.", [m("DOTTLER", 12, "SWARM", "MODEST"), m("BEAUTIFLY", 13, "SWARM", "MODEST", "GUST,BUGBITE,ABSORB,STRINGSHOT", item="TELLURICSEED")])
    # Map 525 Gossamer Deepwood (lv 11-12) - SILKWOOD: Compound Eyes (x1.1 accuracy here), Swarm; Yanma glides (Bug-type Flying x1.2)
    t("Map 525 Gossamer Deepwood", "BUGCATCHER", "Linden", "The deepwood bugs are tougher than mine...", [m("NINCADA", 11, "COMPOUNDEYES", "ADAMANT"), m("LEDYBA", 11, "SWARM", "JOLLY"), m("RELLOR", 12, "COMPOUNDEYES", "IMPISH")])
    t("Map 525 Gossamer Deepwood", "POKEMONRANGER_F", "Sorrel", "Mind the glass trees. They're spreading.", [m("DEERLING", 11, "SAPSIPPER", "JOLLY"), m("SKIDDO", 12, "SAPSIPPER", "ADAMANT")])
    # Map 540 Thistledown Lea (lv 12-14) - MEADOW: Run Away (Sentret, Doduo), Fairy Wind x1.5, Sunkern's Growth / Ingrain tend the meadow
    t("Map 540 Thistledown Lea", "FISHERMAN", "Hale", "Reeled in a loss. Happens.", [m("MAGIKARP", 12, "SWIFTSWIM", "HARDY"), m("GOLDEEN", 13, "SWIFTSWIM", "ADAMANT"), m("TYMPOLE", 13, "SWIFTSWIM", "MODEST")])
    t("Map 540 Thistledown Lea", "PICNICKER", "Bryony", "My flowers wilted! Oh well, picnic time.", [m("FLABEBE", 12, "FLOWERVEIL", "MODEST"), m("COTTONEE", 13, "PRANKSTER", "BOLD"), m("SUNKERN", 13, "CHLOROPHYLL", "MODEST")])
    t("Map 540 Thistledown Lea (double battle)", "TWINS", "Bel & Bea", "Bel: We lost! Bea: Together, though!", [m("MANKEY", 13, "VITALSPIRIT", "JOLLY"), m("PANCHAM", 13, "IRONFIST", "ADAMANT")])
    t("Map 540 Thistledown Lea", "YOUNGSTER", "Corin", "My team's the coolest! ...Was.", [m("SENTRET", 12, "RUNAWAY", "JOLLY"), m("BIDOOF", 13, "SIMPLE", "ADAMANT"), m("DODUO", 14, "EARLYBIRD", "JOLLY")])
    # Map 541 The Grey Saltings (beach, lv 14-16) - BEACH: Mud-Slap / Mud Shot x2 (Bunnelby, Nacli), Water x1.2, Sand Rush works in the sand
    t("Map 541 The Grey Saltings", "CAMPER", "Ned", "Sand in my tent AND I lost. Great day.", [m("BUNNELBY", 14, "CHEEKPOUCH", "ADAMANT"), m("NACLI", 15, "PURIFYINGSALT", "IMPISH")])
    # Hiker Dunstan walks Lacecliff Walk now (script map 527, Gym 1 stretch). Rolycoly and Nacli resist the Normal gym
    # ahead; on the Beach Mud-Slap is x2. A gentle cliff-path fight.
    t("Map 527 Lacecliff Walk", "HIKER", "Dunstan", "Today's a sun day. Lucky you.", [m("ROLYCOLY", 9, "STEAMENGINE", "ADAMANT"), m("NACLI", 10, "PURIFYINGSALT", "IMPISH")])
    t("Map 541 The Grey Saltings", "SAILOR", "Morrow", "Blow me down! The Dovetail crew'll hear of this.", [m("FINNEON", 15, "SWIFTSWIM", "JOLLY"), m("REMORAID", 15, "HUSTLE", "MODEST"), m("CRABRAWLER", 15, "IRONFIST", "ADAMANT")])
    t("Map 541 The Grey Saltings", "TUBER_F", "Pip", "Waaah! My floaty popped!", [m("SURSKIT", 14, "SWIFTSWIM", "TIMID"), m("MINCCINO", 15, "CUTECHARM", "JOLLY")])
    # Map 151-153 Pell Playhouse (Gym 2 actors, lv 15-18) - GRAND_STAGE: sound (Echoed Voice, Disarming Voice), showpieces
    # (Fake Out) and dances (Teeter Dance) raise the applause, so the player sees the stages climb before Dorian
    t("Map 154 Pell Playhouse - Auditorium", "JUGGLER", "Florian", "I'll be in the bar. There is no bar. I'll be in the lobby.", [m("MINCCINO", 15, "TECHNICIAN", "JOLLY", "ECHOEDVOICE,POUND,HELPINGHAND,BABYDOLLEYES"), m("SPINDA", 16, "OWNTEMPO", "ADAMANT")])
    t("Map 154 Pell Playhouse - Auditorium", "BEAUTY", "Rosalind", "...Upstaged. In my own aisle.", [m("SKITTY", 16, "CUTECHARM", "TIMID", "FAKEOUT,ROUND,SING,TAILWHIP"), m("FLABEBE", 16, "FLOWERVEIL", "MODEST")])
    t("Map 154 Pell Playhouse - Auditorium", "JUGGLER", "Ambrose", "Encore? No? No.", [m("AIPOM", 16, "SKILLLINK", "JOLLY"), m("LILLIPUP", 17, "VITALSPIRIT", "ADAMANT")])
    t("Map 152 Pell Playhouse - Backstage (D9, after Badge 2)", "GENTLEMAN", "Reginald", "Splendid form. Dorian will be delighted.", [m("HERDIER", 17, "INTIMIDATE", "ADAMANT"), m("FURFROU", 17, "FURCOAT", "JOLLY")])
    t("Map 153 Pell Playhouse - Backstage (D9, after Badge 2)", "JUGGLER", "Pierrot", "...(Pierrot mimes a dramatic faint.)", [m("AIPOM", 17, "PICKUP", "JOLLY"), m("SPINDA", 17, "TANGLEDFEET", "ADAMANT")])
    t("Map 153 Pell Playhouse - Backstage (D9, after Badge 2)", "LADY", "Odette", "My costume is ruined. Worth it.", [m("BUNEARY", 17, "LIMBER", "JOLLY"), m("FURFROU", 18, "FURCOAT", "JOLLY")])
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
    # Map 560 Frostflat Causeway (lv 16-19) - SNOWY_MOUNTAIN: Powder Snow x2, Ice Body heals without hail (no Snow Cloak on Standard)
    t("Map 560 Frostflat Causeway", "BIKER", "Rook", "Not THAT Rook. Everybody asks.", [m("GLAMEOW", 17, "OWNTEMPO", "JOLLY"), m("TAUROS", 18, "INTIMIDATE", "JOLLY")])
    t("Map 560 Frostflat Causeway", "PICNICKER", "Sela", "Okay, you win the last sandwich.", [m("SKITTY", 16, "CUTECHARM", "TIMID"), m("PHANPY", 17, "PICKUP", "ADAMANT")])
    t("Map 560 Frostflat Causeway", "POKEMANIAC", "Ivo", "My precious monsters!", [m("CUBONE", 17, "ROCKHEAD", "ADAMANT"), m("KANGASKHAN", 19, "EARLYBIRD", "ADAMANT")])
    t("Map 560 Frostflat Causeway", "RUINMANIAC", "Alder", "The old stones told me I'd lose. I never listen.", [m("HELIOPTILE", 17, "DRYSKIN", "TIMID"), m("DUNSPARCE", 18, "SERENEGRACE", "ADAMANT")])
    # Map 561 Gullcry Cliffs (lv 17-20) - MOUNTAIN: Flying x1.2 and wind moves x1.3 for the cliff birds
    t("Map 561 Gullcry Cliffs", "BIRDKEEPER", "Wren", "My flock scattered! Well flown.", [m("TAILLOW", 17, "GUTS", "JOLLY"), m("DUCKLETT", 18, "KEENEYE", "MODEST"), m("CHATOT", 18, "KEENEYE", "MODEST")])
    t("Map 561 Gullcry Cliffs", "COOLTRAINER_F", "Astrid", "Cool. You'll do fine in the Tidelock.", [m("ORICORIO", 19, "DANCER", "TIMID"), m("CRAMORANT", 19, "GULPMISSILE", "MODEST"), m("SNORUNT", 19, "INNERFOCUS", "JOLLY")])
    t("Map 561 Gullcry Cliffs", "FISHERMAN", "Kjell", "The sea gives, the sea takes.", [m("MAGIKARP", 17, "SWIFTSWIM", "HARDY"), m("FINNEON", 18, "SWIFTSWIM", "TIMID"), m("WOOPER", 18, "DAMP", "IMPISH")])
    t("Map 561 Gullcry Cliffs", "SAILOR", "Haldor", "Arr! Isenmar's coast breeds tough kids.", [m("WINGULL", 18, "KEENEYE", "MODEST"), m("SPHEAL", 19, "THICKFAT", "MODEST")])
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
    t("Map 521 Windfall Row", "BUGCATCHER", "Wim", '...Assistant Warden.', [m("WURMPLE", 6, "SHIELDDUST", "HARDY", only="nocasual"), m("SPINARAK", 6, "SWARM", "ADAMANT"), m("COMBEE", 7, "HONEYGATHER", "HASTY")])
    t("Map 521 Windfall Row", "PICNICKER", "Ada", 'Bless you. Bless both of us.', [m("ODDISH", 6, "RUNAWAY", "MODEST"), m("BUDEW", 7, "LEAFGUARD", "MODEST")])
    t("Map 524 Gossamer Wood", "TWINS", "Mo & Jo", 'We lost together!', [m("KARRABLAST", 9, "SWARM", "ADAMANT"), m("SHELMET", 9, "HYDRATION", "BOLD")])
    t("Map 131 Loomhouse Gym - Weaving Hall", "BUGCATCHER", "Nell", "Two of us would've had you.", [m("SILCOON", 11, "SHEDSKIN", "IMPISH", "TACKLE,POISONSTING,STRINGSHOT,HARDEN", only="nocasual"), m("SEWADDLE", 11, "SWARM", "ADAMANT"), m("SPINARAK", 12, "SWARM", "ADAMANT")])
    t("Map 131 Loomhouse Gym - Weaving Hall", "LASS", "Orla", "...I'm going back to the net.", [m("CASCOON", 11, "SHEDSKIN", "IMPISH", "TACKLE,POISONSTING,STRINGSHOT,HARDEN", only="nocasual"), m("LEDYBA", 11, "SWARM", "JOLLY"), m("SPEWPA", 12, "SHEDSKIN", "BOLD")])
    t("Map 131 Loomhouse Gym - Weaving Hall", "GENTLEMAN", "Bram", "I don't need to say it, then.", [m("KAKUNA", 11, "SHEDSKIN", "IMPISH", "POISONSTING,STRINGSHOT,HARDEN", only="nocasual"), m("VENONAT", 12, "COMPOUNDEYES", "MODEST"), m("SEWADDLE", 13, "SWARM", "ADAMANT")])
    t("Map 525 Gossamer Deepwood", "POKEMANIAC", "Ferris", 'That one hummed. Did you hear it hum?', [m("PARAS", 11, "EFFECTSPORE", "ADAMANT"), m("NINCADA", 11, "COMPOUNDEYES", "JOLLY"), m("YANMA", 12, "SPEEDBOOST", "MODEST")])
    t("Map 560 Frostflat Causeway", "LASS", "Tilde", 'My Swinub slid farther than me.', [m("SWINUB", 16, "OBLIVIOUS", "ADAMANT"), m("SNOM", 17, "SHIELDDUST", "MODEST")])
    t("Map 560 Frostflat Causeway", "SAILOR", "Haakon", "Ice'll break by summer. Probably.", [m("SPHEAL", 17, "ICEBODY", "MODEST"), m("CETODDLE", 18, "THICKFAT", "ADAMANT")])
    t("Map 560 Frostflat Causeway", "BIRDKEEPER", "Ailsa", "Frostwick's gulls wear little ice hats. Not really.", [m("WINGULL", 17, "KEENEYE", "MODEST"), m("DELIBIRD", 18, "HUSTLE", "JOLLY")])
    # Map 562 The Rimewood - SILKWOOD under snow: Bug x1.5 (Snom, Tarountula), String Shot never misses
    t("Map 562 The Rimewood", "BUGCATCHER", "Pell", 'They were NOT happy to be woken.', [m("SNOM", 18, "SHIELDDUST", "MODEST"), m("TAROUNTULA", 19, "INSOMNIA", "ADAMANT")])
    t("Map 562 The Rimewood", "POKEMONRANGER_F", "Orla", "You'll do. Mind the silk curtains, they cut.", [m("DEERLING", 18, "SAPSIPPER", "JOLLY"), m("SNOVER", 19, "SNOWWARNING", "MODEST"), m("STANTLER", 20, "INTIMIDATE", "ADAMANT")])
    t("Map 562 The Rimewood", "HIKER", "Ulf", 'Ha! No, no traps for you.', [m("TEDDIURSA", 18, "PICKUP", "ADAMANT"), m("BERGMITE", 19, "OWNTEMPO", "IMPISH")])
    t("Map 562 The Rimewood", "CAMPER", "Rook", "...Is that what the aurora's for?", [m("CUBCHOO", 18, "SNOWCLOAK", "ADAMANT"), m("SNEASEL", 19, "INNERFOCUS", "JOLLY")])
    t("Map 562 The Rimewood", "TWINS", "Ana & Ida", 'Two of us lost! Two kingdoms of losing!', [m("MORELULL", 19, "EFFECTSPORE", "MODEST"), m("SNORUNT", 19, "INNERFOCUS", "JOLLY")])
    # Map 577 Frostwick Pass (Gym 3 stretch, 17-20) - SNOWY_MOUNTAIN: Ice x1.5, Powder Snow x2, Icy Wind x1.5, Slush Rush and
    # Ice Body work without hail, Rock moves come down frozen. No Snow Cloak (evasion: never on Standard). Map builder 13's
    # cells and roles (mapgen/REQUESTS.md, 2026-11-20); ROUTES.yaml: a huscarl, a forester, two sledgers.
    t("Map 577 Frostwick Pass (double battle, cell 36,82)", "TWINS", "Kari & Kaia", "Kari: We crashed! Kaia: We ALWAYS crash.",
      [m("SWINUB", 17, "OBLIVIOUS", "ADAMANT"), m("SNOM", 18, "ICESCALES", "MODEST")])
    t("Map 577 Frostwick Pass (cell 25,66)", "POKEMONRANGER_F", "Liv", "The fences hold the snow. You hold your own, too.",
      [m("DEERLING", 18, "SAPSIPPER", "JOLLY"), m("CUBCHOO", 18, "SLUSHRUSH", "ADAMANT")])
    t("Map 577 Frostwick Pass (cell 33,37)", "CAMPER", "Eirik", "Wait for the gust to drop. That's the whole trick.",
      [m("SNORUNT", 18, "ICEBODY", "JOLLY"), m("SWINUB", 19, "OBLIVIOUS", "ADAMANT")])
    t("Map 577 Frostwick Pass (Handfast Arch, cell 37,16)", "BLACKBELT", "Hrodgar", "The arch stands. So do you. Pass, then.",
      [m("CUBCHOO", 19, "SLUSHRUSH", "ADAMANT"), m("SNORUNT", 19, "INNERFOCUS", "JOLLY"), m("STANTLER", 20, "INTIMIDATE", "ADAMANT")])
    # Map 578 Rimewood Path (Gym 3 stretch, 18-21) - SILKWOOD under snow: Bug x1.5, Grass and Fire x1.2, String Shot never
    # misses, Swarm on. Snover's Snow Warning brings the snow its partners' Ice Body needs; the burner's Carkol and the
    # honey-gatherer's Combee play the silk (Fire, Bug).
    t("Map 578 Rimewood Path (cell 35,79)", "HIKER", "Ottar", "Logs don't fight back. You do. Noted.",
      [m("TEDDIURSA", 18, "PICKUP", "ADAMANT"), m("SWINUB", 18, "OBLIVIOUS", "ADAMANT")])
    t("Map 578 Rimewood Path (cell 36,61)", "POKEMONRANGER_M", "Ketil", "Mind the snares. Mine, and the other kind.",
      [m("BUNEARY", 19, "LIMBER", "JOLLY"), m("CUBCHOO", 19, "RATTLED", "ADAMANT")])
    t("Map 578 Rimewood Path (cell 43,37)", "CAMPER", "Brand", "Kiln's still hot. Warm your hands before you go on.",
      [m("SNOVER", 19, "SNOWWARNING", "MODEST"), m("VANILLITE", 19, "ICEBODY", "MODEST"), m("CARKOL", 19, "STEAMENGINE", "ADAMANT")])
    t("Map 578 Rimewood Path (cell 37,30)", "PICNICKER", "Hild", "Take a comb of honey. The bees won't mind. Much.",
      [m("COMBEE", 19, "HONEYGATHER", "HASTY"), m("TEDDIURSA", 19, "HONEYGATHER", "ADAMANT"), m("DEERLING", 20, "SAPSIPPER", "JOLLY")])
    t("Map 578 Rimewood Path (last blaze, cell 39,9)", "COOLTRAINER_F", "Ragna", "Follow the red blazes. Never the blue one.",
      [m("SNEASEL", 20, "INNERFOCUS", "JOLLY"), m("SNOVER", 20, "SNOWWARNING", "MODEST"), m("MORELULL", 21, "EFFECTSPORE", "MODEST")])
    t("Map 563 Rimewood Glade", "POKEMONRANGER_M", "Sigurd", '...So you cut your way in. Fair.', [m("STANTLER", 19, "INTIMIDATE", "ADAMANT"), m("CRYOGONAL", 20, "LEVITATE", "CALM", "ICESHARD,RAPIDSPIN,ICYWIND,CONFUSERAY")])  # FROZEN_LAKE: Rapid Spin skates (x1.5), Icy Wind -2 Speed
    # --- Trainers named in the SPINE Rev 14 scripts (story/20_SCRIPT_CH0-2.md, story/21_SCRIPT_CH3.md) --------------
    # Map 527 Lacecliff Walk (Strand Road, BEACH, Gym 1 stretch 8-12). Beach: Mud-Slap / Mud Shot x2, Water x1.2.
    t("Map 527 Lacecliff Walk", "FISHERMAN", "Bryn", "The fish win again.", [m("MAGIKARP", 8, "SWIFTSWIM", "HARDY"), m("FINNEON", 9, "SWIFTSWIM", "TIMID"), m("WINGULL", 9, "KEENEYE", "MODEST")])
    t("Map 527 Lacecliff Walk", "PICNICKER", "Moll", "She writes every week. She's never once walked over.", [m("BUNNELBY", 9, "PICKUP", "ADAMANT"), m("SANDYGAST", 10, "WATERCOMPACTION", "MODEST")])
    # Map 528 Marram Down (BEACH). Sea breeze: Gust kicks sand into everyone else's eyes (accuracy -1).
    t("Map 528 Marram Down", "BIRDKEEPER", "Lark", "My kite won. You beat the kite-flier, which is different.", [m("PIKIPEK", 10, "KEENEYE", "JOLLY"), m("ROOKIDEE", 11, "KEENEYE", "JOLLY")])
    t("Map 528 Marram Down", "POKEMONRANGER_F", "Sedge", "I'm going to sit down now. That's allowed in a free port.", [m("DWEBBLE", 11, "STURDY", "ADAMANT"), m("NACLI", 11, "PURIFYINGSALT", "IMPISH"), m("WOOLOO", 12, "FLUFFY", "IMPISH")])
    # Map 528 players' camp: the costume double vs two actors in hound masks (a double battle, one trainer).
    t("Map 528 Marram Down - players' camp (double battle)", "JUGGLER", "Hounds", "Notes: we were bitten. Again.", [m("LILLIPUP", 11, "VITALSPIRIT", "JOLLY"), m("YAMPER", 11, "BALLFETCH", "JOLLY")])
    # Map 544/545 Brinecut Mine (CAVE, Gym 2 stretch). Rock x1.5; Rock Head is safe from a cave-in.
    t("Map 545 Brinecut Mine B1F", "HIKER", "Holt", "It IS a shortcut? To WHERE?", [m("ROGGENROLA", 16, "STURDY", "ADAMANT"), m("NACLI", 16, "PURIFYINGSALT", "IMPISH"), m("WOOBAT", 17, "UNAWARE", "TIMID")])
    t("Map 544 Brinecut Mine 1F", "BLACKBELT", "Saul", "I need a drink. Not salt.", [m("MACHOP", 16, "GUTS", "ADAMANT"), m("CRABRAWLER", 17, "IRONFIST", "ADAMANT")])
    # Map 552 The Dyers' Ford (MEADOW, 15-17). Morwenna works the madder vat: her Litleo's Fire moves set the dry Meadow
    # ablaze (two of them) - a field play for a cap-19 route. Ash's woad-blue Oddish and Marill.
    t("Map 552 The Dyers' Ford", "PAINTER", "Morwenna", "Look at my hands. They'll be red till Fallmorn.", [m("LEDYBA", 15, "SWARM", "JOLLY"), m("LITLEO", 16, "RIVALRY", "MODEST")])
    t("Map 552 The Dyers' Ford", "PAINTER", "Ash", "Bill her. Somebody bill her.", [m("ODDISH", 15, "CHLOROPHYLL", "MODEST"), m("MARILL", 16, "HUGEPOWER", "ADAMANT")])
    # Map 540 Thistledown Lea (MEADOW): Ada's cousin; Budew and Oddish like Ada's, a little grown up.
    t("Map 540 Thistledown Lea", "PICNICKER", "Edie", "...I'll write to Ada. I'll lie.", [m("ODDISH", 13, "RUNAWAY", "MODEST"), m("BUDEW", 13, "LEAFGUARD", "MODEST"), m("SMOLIV", 14, "EARLYBIRD", "MODEST")])
    # --- Ch5 Wave 0 rescue (2026-11-23): Gym 4, the Circuit Gym (mapgen/layouts/circuit_gym.py TRAINERS; GYM_PUZZLES:
    # Engineer x2, Super Nerd, Scientist, Rocker, "Circuit Tester"; Lv 23-26). NEON_GRID: Electric x1.3 on the live board,
    # Static / Volt Absorb / Motor Drive pay, a Blackout (Ground moves) shuts the grid. Ground types are the counter.
    t("Map 190 Circuit Gym - the Switchroom", "ENGINEER", "Volta", "Turn the sideways ones. Chat says so.",
      [m("MAGNEMITE", 23, "STURDY", "MODEST"), m("PAWMI", 23, "STATIC", "JOLLY")])
    t("Map 191 Circuit Gym - Breadboard Hall", "SUPERNERD", "Ohm", "The middle row's a trap. I told him it was too obvious.",
      [m("VOLTORB", 23, "STATIC", "TIMID"), m("TADBULB", 24, "OWNTEMPO", "MODEST")])
    t("Map 191 Circuit Gym - Breadboard Hall", "SCIENTIST", "Faraday", "Hm. You did.",
      [m("ELEKID", 24, "STATIC", "ADAMANT"), m("BLITZLE", 24, "MOTORDRIVE", "JOLLY")])
    t("Map 192 Circuit Gym - Live Wire Hall", "ENGINEER", "Kirch", "Latches hold. Wires don't have to. Rook's motto. Well, mine. He stole it.",
      [m("CHINCHOU", 24, "VOLTABSORB", "MODEST"), m("FLAAFFY", 24, "STATIC", "MODEST"), m("JOLTIK", 25, "COMPOUNDEYES", "TIMID")])
    t("Map 192 Circuit Gym - Live Wire Hall", "ROCKER", "Amp", "Encore? No? Fine.",
      [m("TOXEL", 24, "RATTLED", "MODEST"), m("PICHU", 24, "STATIC", "TIMID"), m("ELECTRIKE", 25, "LIGHTNINGROD", "JOLLY")])
    t("Map 192 Circuit Gym - Live Wire Hall (Circuit Tester)", "ENGINEER", "Tesla", "You conduct well.",
      [m("MAGNEMITE", 25, "ANALYTIC", "MODEST"), m("LUXIO", 25, "INTIMIDATE", "ADAMANT"), m("WATTREL", 26, "VOLTABSORB", "TIMID")])
    # ===============================================================================================================
    # COVERAGE FILL AND THE CH5-CH13 DENSITY RETROFIT (2026-11-25). Reuben's rule: every non-legendary species is fought
    # at least once on a generic trainer, where it fits (class, kingdom, field) and at a level where that form exists.
    # Check with `python3 -I tools/trainer_gen/coverage.py` (report: design/TRAINER_COVERAGE.md). Movesets are level-up
    # (always legal). Most of these maps aren't built yet: the PBS blocks are ready for their events. Also for coverage:
    # the third Pokemon (Standard and Hard only) on Pim, Dell, Wim, Tobin and the five Loomhouse trainers above
    # (Scatterbug, Weedle, Wurmple, Spewpa, Kricketot, Blipbug and the three cocoons can't plausibly appear later).
    # ---------------------------------------------------------------------------------------------------------------
    # Ch5 - the Lock Road and the roads into Lumen (after Gym 3, cap 27; route Lv 20-24, the hatchery teams 19-22)
    # Pokemonbreeder Solveig: the reed-cutters' hatchery: water starters, fresh out of the egg
    t("Map 580 The Reedholms", "POKEMONBREEDER", "Solveig", "Hush, hush. You've set all five of them off.",
      [m("OSHAWOTT", 19, "TORRENT", "MODEST"), m("MUDKIP", 20, "TORRENT", "ADAMANT"), m("PIPLUP", 21, "TORRENT", "MODEST"), m("SQUIRTLE", 21, "TORRENT", "MODEST"), m("TOTODILE", 22, "TORRENT", "ADAMANT")])
    t("Map 580 The Reedholms", "FISHERMAN", "Tarjei", "The eels just sat there and watched. Same as always.",
      [m("WIGLETT", 21, "RATTLED", "JOLLY"), m("LUVDISC", 23, "SWIFTSWIM", "TIMID"), m("LOMBRE", 24, "SWIFTSWIM", "MODEST")])
    t("Map 580 The Reedholms", "SAILOR", "Aksel", "Punt's stuck, pole's stuck, and now this.",
      [m("LOTAD", 19, "RAINDISH", "MODEST"), m("DEWPIDER", 23, "WATERBUBBLE", "ADAMANT"), m("SHELLDER", 24, "SHELLARMOR", "ADAMANT")])
    t("Map 580 The Reedholms", "BIRDKEEPER", "Sunniva", "They've gone back to the heron islet. I don't blame them.",
      [m("ZUBAT", 21, "INNERFOCUS", "ADAMANT"), m("BUTTERFREE", 23, "COMPOUNDEYES", "MODEST"), m("MOTHIM", 24, "SWARM", "ADAMANT")])
    t("Map 580 The Reedholms", "YOUNGSTER", "Jorun", "I cut reeds faster than I battle. Don't tell my da.",
      [m("AZURILL", 21, "HUGEPOWER", "ADAMANT"), m("WHISMUR", 23, "SOUNDPROOF", "ADAMANT"), m("FURRET", 24, "RUNAWAY", "JOLLY")])
    t("Map 592 The Icecutters' Haul", "HIKER", "Bodil", "We're on strike. I wasn't meant to lose on strike.",
      [m("SNOM", 22, "SHIELDDUST", "MODEST"), m("MUDBRAY", 24, "STAMINA", "ADAMANT")])
    t("Map 592 The Icecutters' Haul", "BLACKBELT", "Torsten", "I cut ice all day. You cut me in half the time.",
      [m("TYROGUE", 22, "STEADFAST", "ADAMANT"), m("PAWMO", 24, "NATURALCURE", "JOLLY")])
    t("Map 592 The Icecutters' Haul", "CAMPER", "Nils", "The sled went one way and my team went the other.",
      [m("PATRAT", 21, "RUNAWAY", "ADAMANT"), m("SLAKOTH", 23, "TRUANT", "ADAMANT"), m("GUMSHOOS", 24, "STAKEOUT", "ADAMANT")])
    # Pokemonbreeder Ingvild: the Union Hall boiler keeps her eggs warm: fire starters
    t("Map 590 Brassfall", "POKEMONBREEDER", "Ingvild", "Mind the eggs! ...Oh, you did. Thank you.",
      [m("TEPIG", 19, "BLAZE", "ADAMANT"), m("CHIMCHAR", 19, "BLAZE", "ADAMANT"), m("CYNDAQUIL", 19, "BLAZE", "MODEST"), m("CHARMANDER", 20, "BLAZE", "MODEST"), m("TORCHIC", 21, "BLAZE", "MODEST")])
    t("Map 590 Brassfall", "ENGINEER", "Corwin", "It ran off a Cell. So did my team, apparently.",
      [m("MAREEP", 20, "STATIC", "MODEST"), m("PACHIRISU", 24, "PICKUP", "CALM")])
    # Sailor Brede: a lock-hand's basin of water starters
    t("Map 581 The Icefall Locks", "SAILOR", "Brede", "Every lock on this stair and you still got past me.",
      [m("QUAXLY", 19, "TORRENT", "ADAMANT"), m("SOBBLE", 20, "TORRENT", "MODEST"), m("FROAKIE", 21, "TORRENT", "MODEST"), m("POPPLIO", 22, "TORRENT", "MODEST")])
    t("Map 581 The Icefall Locks", "ENGINEER", "Hartley", "Lattice hums. I hum. You didn't even slow down.",
      [m("TINKATINK", 22, "OWNTEMPO", "ADAMANT"), m("PLUSLE", 24, "PLUS", "TIMID")])
    t("Map 581 The Icefall Locks", "POKEMONRANGER_M", "Alwin", "Elowen soil from here up. You've earned the walk.",
      [m("GOSSIFLEUR", 21, "COTTONDOWN", "ADAMANT"), m("BELLSPROUT", 23, "CHLOROPHYLL", "ADAMANT"), m("WORMADAM", 24, "ANTICIPATION", "MODEST")])
    t("Map 581 The Icefall Locks", "COOLTRAINER_F", "Ylva", "Isenmar ends at the top. So did my streak.",
      [m("POLIWAG", 21, "DAMP", "JOLLY"), m("SMOOCHUM", 23, "OBLIVIOUS", "MODEST"), m("PANPOUR", 24, "GLUTTONY", "ADAMANT")])
    # Pokemonranger F Hazel: the woodward's apprentice: grass starters among the coppice stools
    t("Map 595 Coppice Ride", "POKEMONRANGER_F", "Hazel", "Seven panels, seven ages. These five are the youngest.",
      [m("SNIVY", 19, "OVERGROW", "ADAMANT"), m("TREECKO", 20, "OVERGROW", "MODEST"), m("BULBASAUR", 21, "OVERGROW", "MODEST"), m("CHIKORITA", 21, "OVERGROW", "ADAMANT"), m("TURTWIG", 22, "OVERGROW", "ADAMANT")])
    # Camper Wat: the charcoal clamp: fire starters keep it lit
    t("Map 595 Coppice Ride", "CAMPER", "Wat", "Clamp's meant to smoulder, not blaze. Same goes for me.",
      [m("FENNEKIN", 19, "BLAZE", "MODEST"), m("FUECOCO", 20, "BLAZE", "MODEST"), m("SCORBUNNY", 21, "BLAZE", "ADAMANT"), m("LITTEN", 22, "BLAZE", "ADAMANT")])
    t("Map 595 Coppice Ride", "BUGCATCHER", "Perkin", "The tall panel has the good ones. I got these.",
      [m("NYMBLE", 21, "SWARM", "ADAMANT"), m("BURMY", 23, "SHEDSKIN", "ADAMANT"), m("VENIPEDE", 24, "POISONPOINT", "ADAMANT")])
    t("Map 595 Coppice Ride", "PICNICKER", "Tansy", "I'd offer you hazelnuts but they've eaten them.",
      [m("SEEDOT", 19, "CHLOROPHYLL", "ADAMANT"), m("BOUNSWEET", 21, "OBLIVIOUS", "ADAMANT"), m("HOPPIP", 23, "CHLOROPHYLL", "ADAMANT")])
    t("Map 595 Coppice Ride", "GENTLEMAN", "Osric", "A copper a crossing, and worth every one.",
      [m("SPEAROW", 21, "KEENEYE", "ADAMANT"), m("PIDOVE", 23, "BIGPECKS", "ADAMANT"), m("WATCHOG", 24, "KEENEYE", "ADAMANT")])
    # Aromalady Linnet: hedgerow seedlings: grass starters
    t("Map 594 Wallshadow Row", "AROMALADY", "Linnet", "They do better in the Wall's shade. So do I, usually.",
      [m("GROOKEY", 19, "OVERGROW", "ADAMANT"), m("SPRIGATITO", 20, "OVERGROW", "ADAMANT"), m("CHESPIN", 21, "OVERGROW", "ADAMANT"), m("ROWLET", 22, "OVERGROW", "ADAMANT")])
    t("Map 594 Wallshadow Row", "YOUNGSTER", "Hodge", "I'm telling the tithe-reeve. He won't care either.",
      [m("RATTATA", 21, "GUTS", "ADAMANT"), m("NIDORANmA", 21, "RIVALRY", "ADAMANT"), m("LINOONE", 24, "GLUTTONY", "JOLLY")])
    t("Map 594 Wallshadow Row", "LASS", "Marigold", "Four kingdoms on that signpost and I lost in this one.",
      [m("RALTS", 21, "TRACE", "MODEST"), m("NIDORANfE", 21, "RIVALRY", "ADAMANT"), m("YUNGOOS", 23, "STRONGJAW", "ADAMANT")])
    t("Map 594 Wallshadow Row", "TAMER", "Hob", "Tithe barn's full. My pride isn't.",
      [m("POOCHYENA", 21, "QUICKFEET", "ADAMANT"), m("PURRLOIN", 23, "LIMBER", "ADAMANT"), m("RATICATE", 24, "RUNAWAY", "JOLLY")])
    t("Map 594 Wallshadow Row (double battle)", "TWINS", "Meg & Peg", "Meg: Your fault. Peg: YOUR fault.",
      [m("PIDGEY", 22, "KEENEYE", "ADAMANT"), m("HOOTHOOT", 24, "INSOMNIA", "MODEST")])
    t("Map 593 The Arc-Lamp Mile", "ROCKER", "Jax", "Lamp 47 flickered. That threw me off. That's my story.",
      [m("LECHONK", 21, "GLUTTONY", "ADAMANT"), m("PIKACHU", 23, "STATIC", "JOLLY"), m("CHARJABUG", 24, "BATTERY", "ADAMANT")])
    t("Map 593 The Arc-Lamp Mile", "JUGGLER", "Fitch", "A hundred lamps to light and I drop it at this one.",
      [m("MUNNA", 21, "SYNCHRONIZE", "MODEST"), m("ESPURR", 23, "KEENEYE", "MODEST"), m("KADABRA", 24, "INNERFOCUS", "TIMID")])
    t("Map 593 The Arc-Lamp Mile", "BEAUTY", "Coralie", "The tram's never coming, is it. Neither is my win.",
      [m("STARLY", 19, "KEENEYE", "ADAMANT"), m("SNUBBULL", 23, "INTIMIDATE", "ADAMANT"), m("WIGGLYTUFF", 24, "CUTECHARM", "MODEST")])
    t("Map 593 The Arc-Lamp Mile", "SCIENTIST", "Morley", "Fascinating. Do that again, slower, so I can write it down.",
      [m("WYNAUT", 20, "SHADOWTAG", "ADAMANT"), m("ABRA", 21, "SYNCHRONIZE", "TIMID"), m("BELDUM", 23, "CLEARBODY", "IMPISH")])
    t("Map 584 Voltaic Sluiceworks", "BURGLAR", "Nix", "It's decommissioned! It's not stealing if it's decommissioned!",
      [m("EKANS", 23, "SHEDSKIN", "ADAMANT"), m("DUSTOX", 24, "SHIELDDUST", "CALM"), m("BEEDRILL", 25, "SWARM", "ADAMANT")])
    t("Map 584 Voltaic Sluiceworks", "SUPERNERD", "Elwin", "Episode 112 was filmed RIGHT HERE. Take 41. I counted.",
      [m("TYNAMO", 24, "LEVITATE", "ADAMANT"), m("MINUN", 25, "MINUS", "TIMID")])
    # ---------------------------------------------------------------------------------------------------------------
    # Ch6 - Candle Down, the Mainline and the Dunelands to Duneholt (cap 31; route Lv 25-28, Gym 5 and dungeons 27-30)
    t("Map 602 Candle Down", "GENTLEMAN", "Aldous", "The coach is late and so, it seems, am I.",
      [m("TRUMBEAK", 26, "KEENEYE", "ADAMANT"), m("SQUAWKABILLY", 27, "INTIMIDATE", "JOLLY"), m("FEAROW", 28, "KEENEYE", "JOLLY")])
    t("Map 602 Candle Down", "LASS", "Wynne", "I lit a cairn for luck. Wrong cairn.",
      [m("CLEFFA", 26, "CUTECHARM", "MODEST"), m("TOGEPI", 27, "HUSTLE", "MODEST"), m("MILCERY", 28, "SWEETVEIL", "MODEST")])
    t("Map 602 Candle Down", "CAMPER", "Garth", "You can see into the Wall from here. I was looking at that.",
      [m("IGGLYBUFF", 26, "COMPETITIVE", "MODEST"), m("STUFFUL", 27, "KLUTZ", "ADAMANT"), m("MUNCHLAX", 28, "PICKUP", "ADAMANT")])
    t("Map 603 The Highwold", "TAMER", "Colm", "The flock's scattered to the dew-pond. Again.",
      [m("TANDEMAUS", 26, "PICKUP", "ADAMANT"), m("EEVEE", 27, "ADAPTABILITY", "ADAMANT"), m("FLAAFFY", 28, "STATIC", "MODEST")])
    t("Map 603 The Highwold", "PICNICKER", "Nessa", "Windy up here. Blew my whole plan away.",
      [m("CHERUBI", 26, "CHLOROPHYLL", "MODEST"), m("SKIPLOOM", 27, "CHLOROPHYLL", "ADAMANT"), m("SUNFLORA", 28, "CHLOROPHYLL", "MODEST")])
    t("Map 603 The Highwold", "PSYCHIC_F", "Iseult", "The Wold Stones said you'd come. They didn't say this.",
      [m("HATENNA", 26, "ANTICIPATION", "MODEST"), m("CHINGLING", 27, "LEVITATE", "MODEST"), m("DROWZEE", 28, "FOREWARN", "CAREFUL")])
    t("Map 612 The Meridian Mainline", "ENGINEER", "Pryce", "Signal's at danger. Should've read it myself.",
      [m("LUXIO", 26, "INTIMIDATE", "ADAMANT"), m("MANECTRIC", 27, "LIGHTNINGROD", "TIMID"), m("ELECTABUZZ", 28, "STATIC", "TIMID")])
    t("Map 612 The Meridian Mainline", "BIRDKEEPER", "Corbin", "They roost on the gantries. They'll be up there a while now.",
      [m("NATU", 26, "SYNCHRONIZE", "MODEST"), m("STARAVIA", 27, "INTIMIDATE", "ADAMANT"), m("DRIFLOON", 28, "AFTERMATH", "MODEST")])
    t("Map 612 The Meridian Mainline", "SUPERNERD", "Tobias", "I had the timetable memorised. You weren't on it.",
      [m("CUFANT", 26, "SHEERFORCE", "ADAMANT"), m("PORYGON", 27, "DOWNLOAD", "MODEST"), m("PERRSERKER", 28, "BATTLEARMOR", "ADAMANT")])
    t("Map 604 Static Tunnels", "HIKER", "Garrick", "Can't see my hand down here. Saw that coming, though.",
      [m("MAGNEMITE", 27, "STURDY", "MODEST"), m("ONIX", 28, "ROCKHEAD", "IMPISH"), m("BOLDORE", 29, "WEAKARMOR", "ADAMANT")])
    t("Map 604 Static Tunnels", "BURGLAR", "Sly", "Copper wire's worth good money. You're worth trouble.",
      [m("JOLTIK", 27, "COMPOUNDEYES", "MODEST"), m("LIEPARD", 28, "UNBURDEN", "JOLLY"), m("MAGNETON", 29, "MAGNETPULL", "MODEST")])
    t("Map 605 Static Tunnels Depths", "POKEMANIAC", "Otho", "The rare ones live deeper. So does my disappointment.",
      [m("BAGON", 28, "ROCKHEAD", "ADAMANT"), m("DRATINI", 29, "SHEDSKIN", "ADAMANT"), m("LARVITAR", 30, "GUTS", "ADAMANT")])
    t("Map 600 The Brass Dunes", "RUINMANIAC", "Hadrian", "The rails end where the sand starts. Everything does.",
      [m("SILICOBRA", 26, "SHEDSKIN", "ADAMANT"), m("DRILBUR", 27, "SANDFORCE", "ADAMANT"), m("MAWILE", 28, "HYPERCUTTER", "ADAMANT")])
    t("Map 600 The Brass Dunes", "CAMPER", "Idris", "Sand in the kettle, sand in the tent. Sand in my eyes just now.",
      [m("DIGLETT", 26, "ARENATRAP", "JOLLY"), m("DIGGERSBY", 27, "CHEEKPOUCH", "ADAMANT"), m("SANDSLASH", 28, "SANDVEIL", "ADAMANT")])
    t("Map 600 The Brass Dunes", "POKEMONRANGER_F", "Maren", "Green on one side, gold on the other. I guard the seam.",
      [m("EXEGGCUTE", 26, "CHLOROPHYLL", "BOLD"), m("CACNEA", 27, "SANDVEIL", "ADAMANT"), m("SWADLOON", 28, "LEAFGUARD", "IMPISH")])
    t("Map 601 The Rib Road", "HIKER", "Zahir", "The storm buries the road each night. Today it buried me.",
      [m("ROCKRUFF", 26, "KEENEYE", "ADAMANT"), m("BONSLY", 27, "STURDY", "ADAMANT"), m("SANDILE", 28, "MOXIE", "ADAMANT")])
    t("Map 601 The Rib Road", "BLACKBELT", "Kadir", "I train against the wind. The wind hits softer.",
      [m("TRAPINCH", 26, "HYPERCUTTER", "ADAMANT"), m("GIBLE", 27, "SANDVEIL", "ADAMANT"), m("HIPPOPOTAS", 28, "SANDSTREAM", "ADAMANT")])
    t("Map 601 The Rib Road", "COOLTRAINER_M", "Rashid", "Duneholt's past the red rocks. Go on, you'll manage.",
      [m("SANDILE", 26, "MOXIE", "ADAMANT"), m("GIBLE", 27, "SANDVEIL", "ADAMANT"), m("SANDSHREW", 28, "SANDVEIL", "ADAMANT")])
    t("Map 613 Sunbleach Flats", "BEAUTY", "Samira", "Linen bleaches white in a week out here. I went white in a minute.",
      [m("JIGGLYPUFF", 26, "CUTECHARM", "ADAMANT"), m("MEOWTH", 27, "PICKUP", "JOLLY"), m("MIMEJR", 28, "SOUNDPROOF", "MODEST")])
    t("Map 613 Sunbleach Flats", "YOUNGSTER", "Nabil", "I was guarding the frames! From you, mostly!",
      [m("HAPPINY", 26, "SERENEGRACE", "MODEST"), m("DITTO", 27, "LIMBER", "ADAMANT"), m("DELCATTY", 28, "CUTECHARM", "JOLLY")])
    t("Map 208 Necropolis of the Electors", "CHANNELER", "Zenobia", "The Electors voted. It was unanimous. I lose.",
      [m("GREAVARD", 28, "PICKUP", "ADAMANT"), m("POLTCHAGEIST", 29, "HOSPITALITY", "MODEST"), m("PUMPKABOO", 30, "FRISK", "ADAMANT")])
    t("Map 208 Necropolis of the Electors", "RUINMANIAC", "Lucan", "Eighteen tomb doors and I knocked on yours.",
      [m("SHEDINJA", 28, "WONDERGUARD", "ADAMANT"), m("GIMMIGHOUL", 29, "RATTLED", "MODEST"), m("ONIX", 30, "ROCKHEAD", "IMPISH")])
    t("Map 210 Duneholt Gym - Entrance", "PICNICKER", "Layla", "The sand took my sandwich and you took the rest.",
      [m("PANSAGE", 28, "GLUTTONY", "ADAMANT"), m("TOEDSCOOL", 29, "MYCELIUMMIGHT", "CALM"), m("MUDBRAY", 30, "STAMINA", "ADAMANT")])
    t("Map 211 Duneholt Gym - Puzzle Room 1", "RUINMANIAC", "Darius", "Dig where the Warden says. I dug in the wrong place.",
      [m("LARVITAR", 28, "GUTS", "ADAMANT"), m("TIRTOUGA", 29, "SOLIDROCK", "ADAMANT"), m("GLIGAR", 30, "HYPERCUTTER", "JOLLY")])
    t("Map 211 Duneholt Gym - Puzzle Room 1", "HIKER", "Osman", "Buried to the knees. Carry on over me.",
      [m("ARCHEN", 28, "DEFEATIST", "ADAMANT"), m("CORSOLA", 29, "NATURALCURE", "MODEST"), m("SUDOWOODO", 30, "ROCKHEAD", "ADAMANT")])
    t("Map 212 Duneholt Gym - Puzzle Room 2", "RUINMANIAC", "Farah", "Every layer's older than the last. I feel ancient.",
      [m("CRANIDOS", 28, "MOLDBREAKER", "ADAMANT"), m("GRAVELER", 29, "ROCKHEAD", "ADAMANT"), m("DUGTRIO", 30, "ARENATRAP", "JOLLY")])
    t("Map 212 Duneholt Gym - Puzzle Room 2", "HIKER", "Burak", "Sahar reads sand like a book. You're the next chapter.",
      [m("SHIELDON", 28, "STURDY", "BOLD"), m("GRAVELER", 29, "ROCKHEAD", "ADAMANT"), m("DUGTRIO", 30, "ARENATRAP", "JOLLY")])
    # ---------------------------------------------------------------------------------------------------------------
    # Ch7 - the Marrow Road, the Leach and the Gutterfall to Mirefen (cap 35; route Lv 29-32, Gym 6 and dungeons 31-34)
    t("Map 620 The Marrow Road", "RUINMANIAC", "Cyrus", "There's a city under this road. It can keep me.",
      [m("TRAPINCH", 30, "HYPERCUTTER", "ADAMANT"), m("SILICOBRA", 31, "SHEDSKIN", "ADAMANT"), m("HIPPOPOTAS", 32, "SANDSTREAM", "ADAMANT")])
    t("Map 620 The Marrow Road", "HIKER", "Tariq", "Three days to the next well. I'll walk it off.",
      [m("NACLSTACK", 30, "STURDY", "IMPISH"), m("KLAWF", 31, "SHELLARMOR", "ADAMANT"), m("SANDSLASH", 32, "SANDVEIL", "ADAMANT")])
    t("Map 620 The Marrow Road", "COOLTRAINER_F", "Soraya", "The deep desert doesn't forgive. You don't either.",
      [m("HIPPOPOTAS", 30, "SANDSTREAM", "ADAMANT"), m("KROKOROK", 31, "INTIMIDATE", "ADAMANT"), m("MUDBRAY", 32, "STAMINA", "ADAMANT")])
    t("Map 620 The Marrow Road", "TAMER", "Jamil", "The caravan moves at dusk. So does my pride.",
      [m("PERSIAN", 29, "TECHNICIAN", "JOLLY"), m("GIRAFARIG", 30, "EARLYBIRD", "TIMID"), m("MUDSDALE", 31, "OWNTEMPO", "ADAMANT"), m("URSARING", 32, "GUTS", "ADAMANT")])
    t("Map 632 The Kneeling Stones", "PSYCHIC_M", "Ezra", "The stones kneel to something. Not to me, clearly.",
      [m("GOTHITA", 29, "COMPETITIVE", "MODEST"), m("SOLOSIS", 30, "MAGICGUARD", "MODEST"), m("SPOINK", 31, "THICKFAT", "MODEST"), m("WOBBUFFET", 32, "SHADOWTAG", "ADAMANT")])
    t("Map 632 The Kneeling Stones", "BLACKBELT", "Navid", "Duneholt, Charwell, Vigil. I'll take the long way to all three.",
      [m("PANCHAM", 30, "MOLDBREAKER", "ADAMANT"), m("MACHOKE", 31, "NOGUARD", "ADAMANT"), m("PRIMEAPE", 32, "VITALSPIRIT", "JOLLY")])
    t("Map 632 The Kneeling Stones", "PICNICKER", "Dalia", "A crossroads picnic. Everyone passes, nobody stops. You stopped.",
      [m("TOEDSCOOL", 30, "MYCELIUMMIGHT", "CALM"), m("BAYLEEF", 31, "OVERGROW", "BOLD"), m("DARTRIX", 32, "OVERGROW", "ADAMANT")])
    t("Map 624 Ossuary of Dunes", "RUINMANIAC", "Anwar", "The murals show a trainer winning here. I assumed it was me.",
      [m("FLITTLE", 31, "FRISK", "MODEST"), m("BRONZOR", 32, "HEATPROOF", "BOLD"), m("UNOWN", 33, "LEVITATE", "ADAMANT"), m("HOUNDSTONE", 34, "SANDRUSH", "ADAMANT")])
    t("Map 624 Ossuary of Dunes", "CHANNELER", "Shirin", "They're restless. You woke them, you settle them.",
      [m("GREAVARD", 32, "PICKUP", "ADAMANT"), m("SABLEYE", 33, "STALL", "ADAMANT"), m("COFAGRIGUS", 34, "MUMMY", "MODEST")])
    t("Map 624 Ossuary of Dunes", "POKEMANIAC", "Faisal", "Boulders, bones and me. One of us had to give.",
      [m("BALTOY", 31, "LEVITATE", "ADAMANT"), m("MAROWAK", 32, "LIGHTNINGROD", "ADAMANT"), m("RUNERIGUS", 33, "WANDERINGSPIRIT", "ADAMANT"), m("RAMPARDOS", 34, "MOLDBREAKER", "ADAMANT")])
    t("Map 628 Sinkfield", "POKEMONRANGER_M", "Edmund", "The field swallowed the plough. Keep to the stones.",
      [m("PALPITOAD", 30, "HYDRATION", "ADAMANT"), m("MARSHTOMP", 31, "TORRENT", "ADAMANT"), m("QUAGSIRE", 32, "DAMP", "ADAMANT"), m("WHISCASH", 33, "OBLIVIOUS", "ADAMANT")])
    t("Map 628 Sinkfield", "LASS", "Marjory", "That was our barley. That was our barn. That was my team.",
      [m("PIDGEOTTO", 31, "TANGLEDFEET", "ADAMANT"), m("TRANQUILL", 32, "SUPERLUCK", "ADAMANT"), m("VIGOROTH", 33, "VITALSPIRIT", "JOLLY")])
    t("Map 621 The Leach Canyons", "BURGLAR", "Crake", "Foundry throws away better than Mirefen buys.",
      [m("SHROODLE", 30, "UNBURDEN", "ADAMANT"), m("GLIMMET", 31, "TOXICDEBRIS", "MODEST"), m("IVYSAUR", 32, "OVERGROW", "MODEST")])
    t("Map 621 The Leach Canyons", "SUPERNERD", "Linus", "The runoff's four colours today. I'm the fifth: green.",
      [m("GULPIN", 30, "LIQUIDOOZE", "ADAMANT"), m("ARBOK", 31, "SHEDSKIN", "ADAMANT"), m("GRAFAIAI", 32, "UNBURDEN", "JOLLY")])
    t("Map 621 The Leach Canyons", "FISHERMAN", "Dunn", "Don't eat what I catch here. I don't.",
      [m("CROCONAW", 30, "TORRENT", "ADAMANT"), m("BIBAREL", 31, "UNAWARE", "ADAMANT"), m("BRIONNE", 32, "TORRENT", "MODEST")])
    t("Map 634 Wormwood Lea", "AROMALADY", "Melisande", "Wormwood's bitter. So is this, a little.",
      [m("APPLIN", 29, "RIPEN", "BOLD"), m("KIRLIA", 30, "SYNCHRONIZE", "MODEST"), m("FLOETTE", 31, "FLOWERVEIL", "MODEST"), m("MRMIME", 32, "SOUNDPROOF", "TIMID")])
    t("Map 634 Wormwood Lea", "BUGCATCHER", "Kit", "The water-meadows hum at dusk. That's mostly my team.",
      [m("WIMPOD", 29, "WIMPOUT", "ADAMANT"), m("PINECO", 30, "STURDY", "ADAMANT"), m("RABSCA", 31, "SYNCHRONIZE", "MODEST"), m("SCYTHER", 32, "TECHNICIAN", "JOLLY")])
    t("Map 634 Wormwood Lea", "FISHERMAN", "Aylmer", "The Ironway fords here. So did you, right over me.",
      [m("HORSEA", 29, "SWIFTSWIM", "MODEST"), m("SHELLOS", 30, "STORMDRAIN", "MODEST"), m("STARYU", 31, "ILLUMINATE", "TIMID"), m("WUGTRIO", 32, "RATTLED", "JOLLY")])
    t("Map 634 Wormwood Lea (double battle)", "TWINS", "Tilly & Milly", "Tilly: Bitters! Milly: She means she's bitter.",
      [m("DOLLIV", 31, "EARLYBIRD", "MODEST"), m("GROTLE", 32, "OVERGROW", "ADAMANT")])
    t("Map 633 The Gutterfall", "BIKER", "Rudge", "The falls run blue. Nobody asks why. Don't you start.",
      [m("ZORUA", 30, "ILLUSION", "MODEST"), m("MASCHIFF", 31, "INTIMIDATE", "ADAMANT"), m("MURKROW", 32, "SUPERLUCK", "JOLLY")])
    t("Map 633 The Gutterfall", "CUEBALL", "Knox", "Ladder-town rules: loser climbs down. Long way down.",
      [m("RIOLU", 30, "INNERFOCUS", "ADAMANT"), m("CROAGUNK", 31, "ANTICIPATION", "ADAMANT"), m("GURDURR", 32, "SHEERFORCE", "ADAMANT")])
    t("Map 633 The Gutterfall", "YOUNGSTER", "Tad", "I can hold my breath the whole ladder. Watch. ...Later.",
      [m("TENTACOOL", 30, "LIQUIDOOZE", "CALM"), m("WHIRLIPEDE", 31, "POISONPOINT", "IMPISH"), m("VENOMOTH", 32, "SHIELDDUST", "TIMID")])
    t("Map 230 Mirefen Gym - Entrance", "AROMALADY", "Rue", "The Warden's herbs sting before they heal. Like that did.",
      [m("GLOOM", 31, "CHLOROPHYLL", "MODEST"), m("ROSELIA", 32, "POISONPOINT", "MODEST"), m("FLORAGATO", 33, "OVERGROW", "ADAMANT"), m("THWACKEY", 34, "OVERGROW", "ADAMANT")])
    t("Map 231 Mirefen Gym - Puzzle Room 1", "SCIENTIST", "Hester", "Dose makes the poison. I misjudged the dose.",
      [m("STUNKY", 32, "STENCH", "ADAMANT"), m("KOFFING", 33, "NEUTRALIZINGGAS", "ADAMANT"), m("HAUNTER", 34, "LEVITATE", "TIMID")])
    t("Map 231 Mirefen Gym - Puzzle Room 1", "BURGLAR", "Finch", "I only scavenge what the ward throws out. Like me, now.",
      [m("SALANDIT", 32, "CORROSION", "MODEST"), m("STUNKY", 33, "STENCH", "ADAMANT"), m("ARIADOS", 34, "INSOMNIA", "ADAMANT")])
    t("Map 232 Mirefen Gym - Puzzle Room 2", "SCIENTIST", "Lorcan", "Mind the sludge. It's had a longer day than you.",
      [m("NIDORINA", 32, "POISONPOINT", "ADAMANT"), m("NIDORINO", 33, "POISONPOINT", "ADAMANT"), m("WEEPINBELL", 34, "CHLOROPHYLL", "ADAMANT")])
    t("Map 232 Mirefen Gym - Puzzle Room 2", "BURGLAR", "Mudge", "Corvin patched me up twice. Third time's on you.",
      [m("IMPIDIMP", 32, "PRANKSTER", "MODEST"), m("INKAY", 33, "SUCTIONCUPS", "ADAMANT"), m("MIGHTYENA", 34, "QUICKFEET", "ADAMANT")])
    # ---------------------------------------------------------------------------------------------------------------
    # Ch8 - the fens, Lake Sallow and the Pyre Road to Cindervault (cap 39; route Lv 33-36, Gym 7 and dungeons 35-38)
    t("Map 640 Leechman's Walk", "FISHERMAN", "Gil", "Leeches for the ward, a copper a jar. You're bad for business.",
      [m("CLAUNCHER", 33, "MEGALAUNCHER", "MODEST"), m("CLAMPERL", 34, "SHELLARMOR", "MODEST"), m("QWILFISH", 35, "POISONPOINT", "JOLLY"), m("LANTURN", 36, "ILLUMINATE", "MODEST")])
    t("Map 640 Leechman's Walk", "POKEMONRANGER_F", "Fenella", "Stay on the boards. The fen keeps what it's given.",
      [m("QUILLADIN", 33, "OVERGROW", "ADAMANT"), m("SERVINE", 34, "OVERGROW", "ADAMANT"), m("CARNIVINE", 35, "LEVITATE", "ADAMANT"), m("VICTREEBEL", 36, "CHLOROPHYLL", "ADAMANT")])
    t("Map 640 Leechman's Walk", "CUEBALL", "Brakk", "Plateau folk don't come down here. Now I know why.",
      [m("CROAGUNK", 33, "ANTICIPATION", "ADAMANT"), m("PRIMEAPE", 34, "VITALSPIRIT", "JOLLY"), m("CRAWDAUNT", 35, "SHELLARMOR", "ADAMANT"), m("SKUNTANK", 36, "STENCH", "ADAMANT")])
    t("Map 640 Leechman's Walk", "BUGCATCHER", "Midge", "They bite. Not hard enough, though.",
      [m("LOKIX", 34, "SWARM", "JOLLY"), m("SEVIPER", 35, "SHEDSKIN", "ADAMANT"), m("SWALOT", 36, "LIQUIDOOZE", "ADAMANT")])
    t("Map 644 Miasma Caverns", "HIKER", "Grubb", "Breathe through your sleeve. I should've battled through mine.",
      [m("GRIMER", 35, "STENCH", "ADAMANT"), m("TRUBBISH", 36, "STENCH", "ADAMANT"), m("GLIMMET", 37, "TOXICDEBRIS", "MODEST"), m("NIDOQUEEN", 38, "RIVALRY", "ADAMANT")])
    t("Map 644 Miasma Caverns", "SCIENTIST", "Vane", "Sample forty-one: my own defeat. Noted.",
      [m("MAREANIE", 35, "MERCILESS", "ADAMANT"), m("ELGYEM", 36, "TELEPATHY", "MODEST"), m("GRUMPIG", 37, "OWNTEMPO", "MODEST"), m("GARBODOR", 38, "STENCH", "ADAMANT")])
    t("Map 645 Miasma Caverns B1F", "BURGLAR", "Soot", "Whatever Lumen pours down, somebody down here sells.",
      [m("MORPEKO", 36, "HUNGERSWITCH", "JOLLY"), m("CACTURNE", 37, "SANDVEIL", "ADAMANT"), m("MALAMAR", 38, "SUCTIONCUPS", "ADAMANT")])
    t("Map 645 Miasma Caverns B1F", "POKEMANIAC", "Quill", "It glows down here. So do they. So did you, just then.",
      [m("JANGMOO", 35, "SOUNDPROOF", "ADAMANT"), m("GOLBAT", 36, "INNERFOCUS", "JOLLY"), m("SCOLIPEDE", 37, "SWARM", "JOLLY"), m("MUK", 38, "STICKYHOLD", "ADAMANT")])
    t("Map 648 The Weeping Fen", "CHANNELER", "Lenore", "The fen weeps for them. I only listen.",
      [m("HONEDGE", 36, "NOGUARD", "ADAMANT"), m("FRILLISH", 37, "WATERABSORB", "MODEST"), m("DUSCLOPS", 38, "PRESSURE", "ADAMANT")])
    t("Map 641 Lake Sallow", "SWIMMER_M", "Dale", "Cold lake, warm welcome. Well. Cold lake.",
      [m("DUCKLETT", 34, "KEENEYE", "ADAMANT"), m("SLOWPOKE", 35, "OBLIVIOUS", "ADAMANT"), m("POLIWHIRL", 36, "DAMP", "JOLLY")])
    t("Map 641 Lake Sallow", "SWIMMER_F", "Nerys", "You crossed faster than the ferry. Don't tell Madoc.",
      [m("AZUMARILL", 34, "HUGEPOWER", "BOLD"), m("LUMINEON", 35, "SWIFTSWIM", "JOLLY"), m("KINGLER", 36, "SHELLARMOR", "ADAMANT")])
    t("Map 641 Lake Sallow", "FISHERMAN", "Pike", "Named for the fish. The fish has more wins.",
      [m("SEADRA", 34, "POISONPOINT", "TIMID"), m("SEAKING", 35, "WATERVEIL", "ADAMANT"), m("ARAQUANID", 36, "WATERBUBBLE", "ADAMANT")])
    t("Map 641 Lake Sallow", "SAILOR", "Madoc", "East shore's Ashkaar. You can smell it from mid-lake.",
      [m("FROGADIER", 33, "TORRENT", "TIMID"), m("QUAXWELL", 34, "TORRENT", "ADAMANT"), m("MASQUERAIN", 35, "INTIMIDATE", "MODEST"), m("SWANNA", 36, "KEENEYE", "JOLLY")])
    t("Map 641 Lake Sallow", "TUBER_M", "Finn", "I can swim to the island and back! I can't do this, though.",
      [m("FEEBAS", 34, "SWIFTSWIM", "ADAMANT"), m("ZANGOOSE", 35, "IMMUNITY", "JOLLY"), m("BASCULIN", 36, "RECKLESS", "JOLLY")])
    t("Map 652 The Pyre Road", "TAMER", "Kael", "Every pyre's a house's dead. Mine'll hear about this.",
      [m("VULPIX", 33, "FLASHFIRE", "MODEST"), m("PANSEAR", 34, "GLUTTONY", "ADAMANT"), m("BRAIXEN", 35, "BLAZE", "MODEST"), m("CROCALOR", 36, "BLAZE", "MODEST")])
    t("Map 652 The Pyre Road", "BURGLAR", "Scorch", "Ash hides footprints. Doesn't hide a loss.",
      [m("FLETCHINDER", 34, "FLAMEBODY", "ADAMANT"), m("CHARMELEON", 35, "BLAZE", "MODEST"), m("QUILAVA", 36, "BLAZE", "MODEST")])
    t("Map 652 The Pyre Road", "COOLTRAINER_M", "Varro", "The Caldera Gate's ahead. Brann's no gentler than I was.",
      [m("RABOOT", 34, "BLAZE", "JOLLY"), m("TORRACAT", 35, "BLAZE", "JOLLY"), m("CAMERUPT", 36, "MAGMAARMOR", "MODEST")])
    t("Map 652 The Pyre Road", "LASS", "Asha", "I came to light a pyre for Gran. She'd have laughed at this.",
      [m("DARUMAKA", 34, "HUSTLE", "ADAMANT"), m("MAGBY", 35, "FLAMEBODY", "ADAMANT"), m("LITLEO", 36, "RIVALRY", "MODEST")])
    t("Map 658 Lantern Isle", "TUBER_F", "Kiki", "The lanterns float out at night! I floated out just now.",
      [m("PRINPLUP", 34, "TORRENT", "MODEST"), m("PYUKUMUKU", 35, "INNARDSOUT", "IMPISH"), m("DEWOTT", 36, "TORRENT", "MODEST")])
    t("Map 658 Lantern Isle", "SWIMMER_F", "Leilani", "Warm water makes me slow. That's my excuse.",
      [m("WISHIWASHI", 33, "SCHOOLING", "MODEST"), m("WARTORTLE", 34, "TORRENT", "MODEST"), m("DRIZZILE", 35, "TORRENT", "TIMID"), m("SHARPEDO", 36, "ROUGHSKIN", "JOLLY")])
    t("Map 658 Lantern Isle", "BEAUTY", "Noelani", "Island flowers, island pride. Both wilted.",
      [m("FOMANTIS", 33, "LEAFGUARD", "ADAMANT"), m("STEENEE", 34, "OBLIVIOUS", "ADAMANT"), m("GROVYLE", 35, "OVERGROW", "TIMID"), m("TROPIUS", 36, "SOLARPOWER", "MODEST")])
    t("Map 658 Lantern Isle", "BIRDKEEPER", "Keoni", "They'll sulk in the palms till sundown.",
      [m("SWABLU", 33, "NATURALCURE", "ADAMANT"), m("CORVISQUIRE", 34, "UNNERVE", "ADAMANT"), m("MINIOR", 35, "SHIELDSDOWN", "BOLD"), m("TOUCANNON", 36, "SKILLLINK", "ADAMANT")])
    t("Map 658 Lantern Isle", "FISHERMAN", "Makoa", "Best fishing in Velmora and I still came up empty.",
      [m("MANTYKE", 32, "WATERABSORB", "CALM"), m("CARVANHA", 34, "ROUGHSKIN", "ADAMANT"), m("SEEL", 35, "THICKFAT", "ADAMANT")])
    t("Map 254 Pyre Keep - Ancestor Crypts", "CHANNELER", "Thessaly", "The Ashfall dead are proud. You've embarrassed several.",
      [m("SLUGMA", 36, "MAGMAARMOR", "MODEST"), m("LITWICK", 37, "FLAMEBODY", "MODEST"), m("TALONFLAME", 38, "FLAMEBODY", "JOLLY")])
    t("Map 250 Cindervault Gym - Entrance", "CAMPER", "Flint", "Kindler's job is to start the fire. You put me out.",
      [m("LITWICK", 36, "FLAMEBODY", "MODEST"), m("SALAZZLE", 37, "CORROSION", "TIMID"), m("SCOVILLAIN", 38, "CHLOROPHYLL", "ADAMANT")])
    t("Map 251 Cindervault Gym - Puzzle Room 1", "ENGINEER", "Garran", "Bellows up, bellows down. I'm winded either way.",
      [m("QUILAVA", 36, "BLAZE", "MODEST"), m("CARKOL", 37, "STEAMENGINE", "BOLD"), m("PONYTA", 38, "RUNAWAY", "JOLLY")])
    t("Map 251 Cindervault Gym - Puzzle Room 1", "BLACKBELT", "Ivar", "I hold the tongs. I couldn't hold you.",
      [m("COMBUSKEN", 36, "BLAZE", "ADAMANT"), m("MONFERNO", 37, "BLAZE", "ADAMANT"), m("PIGNITE", 38, "BLAZE", "ADAMANT")])
    t("Map 252 Cindervault Gym - Puzzle Room 2", "ENGINEER", "Oda", "The forge wants an hour to cool. So do I.",
      [m("MONFERNO", 36, "BLAZE", "ADAMANT"), m("CROCALOR", 37, "BLAZE", "MODEST"), m("PIGNITE", 38, "BLAZE", "ADAMANT")])
    t("Map 252 Cindervault Gym - Puzzle Room 2", "COOLTRAINER_M", "Dain", "Brann doesn't talk much. He'll let the forge do it.",
      [m("NUMEL", 36, "SIMPLE", "MODEST"), m("DARMANITAN", 37, "SHEERFORCE", "JOLLY"), m("CINDERACE", 38, "BLAZE", "JOLLY")])
    # ---------------------------------------------------------------------------------------------------------------
    # Ch9 - the ash roads, the Cinderhorn and the Ironway to Ironreach (cap 43; route Lv 37-40, Gym 8 and dungeons 39-42)
    t("Map 660 The Ashmarch", "HIKER", "Tuff", "Ash to the ankles. Now up to the neck.",
      [m("SLUGMA", 38, "MAGMAARMOR", "MODEST"), m("CHARCADET", 39, "FLASHFIRE", "ADAMANT"), m("HOUNDOOM", 40, "EARLYBIRD", "TIMID")])
    t("Map 660 The Ashmarch", "CAMPER", "Embry", "Soot-grass burns if you look at it wrong. I looked wrong.",
      [m("GROWLITHE", 37, "FLASHFIRE", "ADAMANT"), m("SCOVILLAIN", 38, "CHLOROPHYLL", "ADAMANT"), m("MAGMAR", 39, "FLAMEBODY", "TIMID"), m("ARMAROUGE", 40, "FLASHFIRE", "MODEST")])
    t("Map 660 The Ashmarch", "BIRDKEEPER", "Vesna", "They ride the thermals. I ride the consequences.",
      [m("NOCTOWL", 38, "KEENEYE", "MODEST"), m("SKARMORY", 39, "KEENEYE", "ADAMANT"), m("TALONFLAME", 40, "FLAMEBODY", "JOLLY")])
    t("Map 673 The Wyrmtongue", "SAILOR", "Marek", "Beacon's lit for the Warfort, not for me.",
      [m("KABUTO", 38, "SWIFTSWIM", "ADAMANT"), m("OMANYTE", 39, "SHELLARMOR", "MODEST"), m("WAILMER", 40, "OBLIVIOUS", "ADAMANT")])
    t("Map 673 The Wyrmtongue", "FISHERMAN", "Ostap", "The sea's warm off the spit. The fish come pre-cooked.",
      [m("FINIZEN", 38, "WATERVEIL", "ADAMANT"), m("WAILMER", 39, "OBLIVIOUS", "ADAMANT"), m("SWANNA", 40, "KEENEYE", "JOLLY")])
    t("Map 673 The Wyrmtongue", "COOLTRAINER_F", "Ilka", "The legions drill here at dawn. I thought I was ready for them.",
      [m("GOOMY", 38, "HYDRATION", "MODEST"), m("FRAXURE", 39, "MOLDBREAKER", "ADAMANT"), m("GABITE", 40, "SANDVEIL", "ADAMANT")])
    t("Map 662 The Cinderglass Barrens", "RUINMANIAC", "Varrick", "A glass-storm scours you clean. So do you.",
      [m("SOLROCK", 38, "LEVITATE", "ADAMANT"), m("GARGANACL", 39, "STURDY", "ADAMANT"), m("HIPPOWDON", 40, "SANDSTREAM", "ADAMANT")])
    t("Map 662 The Cinderglass Barrens", "BIKER", "Slag", "Obsidian shreds a tyre in a mile. I walked the rest.",
      [m("KROKOROK", 38, "INTIMIDATE", "ADAMANT"), m("CLODSIRE", 39, "POISONPOINT", "ADAMANT"), m("NIDOKING", 40, "POISONPOINT", "JOLLY")])
    t("Map 662 The Cinderglass Barrens", "POKEMANIAC", "Gideon", "Something big sleeps under the black dunes. Not me. I'm wide awake now.",
      [m("AXEW", 37, "RIVALRY", "ADAMANT"), m("VIBRAVA", 38, "LEVITATE", "ADAMANT"), m("TYRUNT", 39, "STRONGJAW", "ADAMANT"), m("DIPPLIN", 40, "GLUTTONY", "MODEST")])
    t("Map 663 The Petrified Ashwood", "POKEMONRANGER_M", "Alaric", "Half these trees are stone. One of them isn't a tree.",
      [m("LUNATONE", 38, "LEVITATE", "MODEST"), m("CRADILY", 40, "SUCTIONCUPS", "ADAMANT"), m("KABUTOPS", 40, "SWIFTSWIM", "ADAMANT")])
    t("Map 663 The Petrified Ashwood", "HIKER", "Petros", "I leaned on a trunk and it walked off.",
      [m("RHYHORN", 37, "ROCKHEAD", "ADAMANT"), m("AMAURA", 38, "REFRIGERATE", "MODEST"), m("CARRACOSTA", 39, "SOLIDROCK", "ADAMANT"), m("OMASTAR", 40, "SHELLARMOR", "MODEST")])
    t("Map 663 The Petrified Ashwood", "PSYCHIC_F", "Sybil", "The forest remembers being green. I remember winning.",
      [m("DUOSION", 37, "MAGICGUARD", "MODEST"), m("HATTREM", 38, "ANTICIPATION", "MODEST"), m("GOTHORITA", 39, "COMPETITIVE", "MODEST"), m("CHIMECHO", 40, "LEVITATE", "MODEST")])
    t("Map 664 The Cinderhorn 1F", "BLACKBELT", "Ragnar", "I punch basalt to toughen up. Basalt's kinder.",
      [m("EMBOAR", 40, "BLAZE", "ADAMANT"), m("BLAZIKEN", 41, "BLAZE", "ADAMANT"), m("INFERNAPE", 42, "BLAZE", "JOLLY")])
    t("Map 664 The Cinderhorn 1F", "HIKER", "Magda", "Mind the lava tubes. They don't mind you.",
      [m("LAIRON", 40, "STURDY", "ADAMANT"), m("MAGCARGO", 41, "MAGMAARMOR", "MODEST"), m("GOLEM", 42, "STURDY", "ADAMANT")])
    t("Map 665 The Cinderhorn 2F", "SUPERNERD", "Wendel", "The tap's reading high. So was my confidence.",
      [m("PONYTA", 40, "RUNAWAY", "JOLLY"), m("HEATMOR", 41, "FLASHFIRE", "MODEST"), m("CERULEDGE", 42, "FLASHFIRE", "JOLLY")])
    t("Map 666 The Cinderhorn Caldera", "COOLTRAINER_M", "Dorn", "Top of the Cinderhorn. Nowhere to go but down.",
      [m("SALAZZLE", 40, "CORROSION", "TIMID"), m("SIMISEAR", 41, "GLUTTONY", "JOLLY"), m("MAGMORTAR", 42, "FLAMEBODY", "MODEST")])
    t("Map 668 Emberfall", "CHANNELER", "Isaura", "The fire's cold here. Touch it. No, don't.",
      [m("DREEPY", 40, "CLEARBODY", "ADAMANT"), m("LAMPENT", 41, "FLAMEBODY", "MODEST"), m("TURTONATOR", 42, "SHELLARMOR", "MODEST")])
    t("Map 661 The Ironway", "HIKER", "Bruna", "Ore goes down, miners go up. I'm going home.",
      [m("ANORITH", 38, "BATTLEARMOR", "ADAMANT"), m("LILEEP", 39, "SUCTIONCUPS", "CALM"), m("BASTIODON", 40, "STURDY", "IMPISH")])
    t("Map 661 The Ironway", "ENGINEER", "Jory", "Winding gear's sound. My nerve, less so.",
      [m("KLINK", 37, "MINUS", "ADAMANT"), m("FERROSEED", 38, "IRONBARBS", "IMPISH"), m("PINCURCHIN", 39, "LIGHTNINGROD", "ADAMANT"), m("TOGEDEMARU", 40, "IRONBARBS", "JOLLY")])
    t("Map 661 The Ironway", "CRUSHGIRL", "Kerra", "The Pit's that way. They hit harder than me. Barely.",
      [m("SCRAGGY", 38, "MOXIE", "ADAMANT"), m("SAWK", 39, "STURDY", "JOLLY"), m("THROH", 40, "INNERFOCUS", "ADAMANT")])
    t("Map 672 The Long Drop", "BURGLAR", "Latch", "The cage only goes down. Like my luck.",
      [m("VAROOM", 38, "OVERCOAT", "ADAMANT"), m("TINKATUFF", 39, "OWNTEMPO", "CAREFUL"), m("DRAPION", 40, "SNIPER", "JOLLY")])
    t("Map 672 The Long Drop", "CUEBALL", "Dregs", "Nobody takes the lift for the view.",
      [m("MEDITITE", 38, "PUREPOWER", "ADAMANT"), m("SCRAGGY", 39, "MOXIE", "ADAMANT"), m("TOXICROAK", 40, "DRYSKIN", "JOLLY")])
    t("Map 672 The Long Drop", "GAMBLER", "Marlow", "I had odds on myself. Long ones, it turns out.",
      [m("LOUDRED", 38, "SOUNDPROOF", "ADAMANT"), m("ABSOL", 39, "SUPERLUCK", "ADAMANT"), m("KROOKODILE", 40, "INTIMIDATE", "JOLLY")])
    # Blackbelt Dunmore: the Open's pit-fighters (story/27_SCRIPT_CH9.md)
    t("Map 263 The Iron Pit", "BLACKBELT", "Dunmore", "Pit rules. You stood, I didn't.",
      [m("MACHOKE", 39, "NOGUARD", "ADAMANT"), m("MEDICHAM", 39, "PUREPOWER", "ADAMANT"), m("HARIYAMA", 40, "THICKFAT", "ADAMANT")])
    # Crushgirl Ysa: the Open's pit-fighters
    t("Map 263 The Iron Pit", "CRUSHGIRL", "Ysa", "Chalk your hands next time. Oh. You did.",
      [m("PANCHAM", 40, "MOLDBREAKER", "ADAMANT"), m("MIENFOO", 40, "REGENERATOR", "ADAMANT"), m("THROH", 40, "INNERFOCUS", "ADAMANT")])
    # Blackbelt Gristle: Old Gristle, the old style
    t("Map 263 The Iron Pit", "BLACKBELT", "Gristle", "The old style still works. On the old.",
      [m("HITMONCHAN", 41, "KEENEYE", "ADAMANT"), m("HITMONLEE", 41, "RECKLESS", "JOLLY"), m("SAWK", 41, "STURDY", "JOLLY")])
    t("Map 270 Ironreach Gym - Entrance", "BLACKBELT", "Goro", "A fist is a promise. Mine broke.",
      [m("SCRAFTY", 40, "MOXIE", "ADAMANT"), m("PAWMOT", 41, "VOLTABSORB", "JOLLY"), m("PANGORO", 42, "MOLDBREAKER", "ADAMANT")])
    t("Map 271 Ironreach Gym - Puzzle Room 1", "CRUSHGIRL", "Mika", "You stepped where I stepped. Then past me.",
      [m("HAKAMOO", 40, "SOUNDPROOF", "ADAMANT"), m("HITMONTOP", 41, "TECHNICIAN", "ADAMANT"), m("GRAPPLOCT", 42, "LIMBER", "ADAMANT")])
    t("Map 271 Ironreach Gym - Puzzle Room 1", "BLACKBELT", "Hideo", "The sand of the Pit keeps every footprint. Yours are over mine.",
      [m("HITMONLEE", 40, "RECKLESS", "JOLLY"), m("PASSIMIAN", 41, "RECEIVER", "ADAMANT"), m("BEWEAR", 42, "FLUFFY", "ADAMANT")])
    t("Map 272 Ironreach Gym - Puzzle Room 2", "CRUSHGIRL", "Aiko", "Kaito says losing is a lesson. I'm very educated.",
      [m("MORGREM", 40, "FRISK", "MODEST"), m("HITMONCHAN", 41, "KEENEYE", "ADAMANT"), m("PANGORO", 42, "MOLDBREAKER", "ADAMANT")])
    t("Map 272 Ironreach Gym - Puzzle Room 2 (double battle)", "CRUSHKIN", "Jin & Rei", "Jin: Together! Rei: We lost together, yes.",
      [m("HARIYAMA", 40, "THICKFAT", "ADAMANT"), m("CRABOMINABLE", 41, "HYPERCUTTER", "ADAMANT"), m("PAWMOT", 42, "VOLTABSORB", "JOLLY")])
    t("Map 273 Ironreach Gym - Puzzle Room 3", "CUEBALL", "Tetsu", "Pit Brawler. Was. Give me a minute.",
      [m("MORGREM", 40, "FRISK", "MODEST"), m("MEDICHAM", 41, "PUREPOWER", "ADAMANT"), m("HITMONTOP", 42, "TECHNICIAN", "ADAMANT")])
    # ---------------------------------------------------------------------------------------------------------------
    # Ch10 - the Rootdeep, Grudgestone, Prism Falls and the Briarway to Verdance (cap 47; route Lv 41-44, Gym 9 and dungeons 43-46)
    t("Map 680 The Rootdeep", "HIKER", "Corm", "Roots above, spores below. I got lost between.",
      [m("AMOONGUSS", 41, "EFFECTSPORE", "ADAMANT"), m("BRAMBLEGHAST", 42, "WINDRIDER", "JOLLY"), m("TOEDSCRUEL", 43, "MYCELIUMMIGHT", "TIMID"), m("VENUSAUR", 44, "OVERGROW", "MODEST")])
    t("Map 680 The Rootdeep", "POKEMONRANGER_F", "Bracken", "The lift goes up to the pastures. You've earned daylight.",
      [m("BRAMBLIN", 41, "WINDRIDER", "ADAMANT"), m("SHIINOTIC", 42, "EFFECTSPORE", "MODEST"), m("BRELOOM", 43, "POISONHEAL", "ADAMANT"), m("SIMISAGE", 44, "GLUTTONY", "JOLLY")])
    t("Map 680 The Rootdeep", "BUGCATCHER", "Emmet", "They glow in the dark. Didn't help.",
      [m("SKORUPI", 41, "SNIPER", "IMPISH"), m("PARASECT", 42, "EFFECTSPORE", "ADAMANT"), m("AMOONGUSS", 43, "EFFECTSPORE", "ADAMANT"), m("ARMALDO", 44, "BATTLEARMOR", "ADAMANT")])
    t("Map 692 The Tailings", "BURGLAR", "Tully", "Grey cones as far as you can see, and all of it somebody's leavings.",
      [m("PAWNIARD", 41, "DEFIANT", "ADAMANT"), m("WEEZING", 42, "NEUTRALIZINGGAS", "ADAMANT"), m("GENGAR", 43, "CURSEDBODY", "TIMID"), m("OVERQWIL", 44, "POISONPOINT", "JOLLY")])
    t("Map 692 The Tailings", "SUPERNERD", "Garrod", "I sift the waste for what the Quarry missed. It missed nothing.",
      [m("METANG", 41, "CLEARBODY", "ADAMANT"), m("DOUBLADE", 42, "NOGUARD", "ADAMANT"), m("KLEFKI", 43, "PRANKSTER", "ADAMANT"), m("REVAVROOM", 44, "OVERCOAT", "JOLLY")])
    t("Map 692 The Tailings", "CUEBALL", "Maul", "The Quarry spat me out. Now you have.",
      [m("FALINKS", 41, "BATTLEARMOR", "ADAMANT"), m("GRAPPLOCT", 42, "LIMBER", "ADAMANT"), m("SCRAFTY", 43, "MOXIE", "ADAMANT"), m("SNEASLER", 44, "PRESSURE", "JOLLY")])
    t("Map 684 Grudgestone Quarry", "BLACKBELT", "Harlan", "Down here a grudge is a kind of training. I've a new one.",
      [m("HAKAMOO", 43, "SOUNDPROOF", "ADAMANT"), m("FALINKS", 44, "BATTLEARMOR", "ADAMANT"), m("STONJOURNER", 45, "POWERSPOT", "ADAMANT"), m("MACHAMP", 46, "NOGUARD", "ADAMANT")])
    t("Map 684 Grudgestone Quarry", "HIKER", "Slate", "Every stone in here's been thrown at somebody.",
      [m("RHYDON", 43, "LIGHTNINGROD", "ADAMANT"), m("GOLEM", 44, "STURDY", "ADAMANT"), m("EXCADRILL", 45, "SANDFORCE", "JOLLY"), m("GIGALITH", 46, "STURDY", "ADAMANT")])
    t("Map 685 Grudgestone Quarry B1F", "CRUSHGIRL", "Rhona", "Nobody books a fight this deep unless they mean it.",
      [m("MIENFOO", 43, "REGENERATOR", "ADAMANT"), m("CONKELDURR", 44, "GUTS", "ADAMANT"), m("MABOSSTIFF", 45, "INTIMIDATE", "JOLLY"), m("SIRFETCHD", 46, "STEADFAST", "ADAMANT")])
    t("Map 685 Grudgestone Quarry B1F", "POKEMANIAC", "Digby", "Scales in the scree. I followed them to you. Mistake.",
      [m("NOIBAT", 43, "FRISK", "MODEST"), m("DEINO", 44, "HUSTLE", "ADAMANT"), m("SLIGGOO", 45, "HYDRATION", "MODEST"), m("KOMMOO", 46, "BULLETPROOF", "JOLLY")])
    t("Map 688 Echo Coliseum", "CHANNELER", "Calliope", "They're still cheering. Listen. Not for me.",
      [m("GOLURK", 43, "IRONFIST", "ADAMANT"), m("SPIRITOMB", 44, "PRESSURE", "ADAMANT"), m("PASSIMIAN", 45, "RECEIVER", "ADAMANT"), m("ANNIHILAPE", 46, "VITALSPIRIT", "JOLLY")])
    t("Map 681 Prism Falls", "SWIMMER_M", "Evander", "I swam up one terrace. One.",
      [m("OCTILLERY", 41, "SNIPER", "ADAMANT"), m("FLOATZEL", 42, "SWIFTSWIM", "JOLLY"), m("TOXAPEX", 43, "LIMBER", "IMPISH"), m("GOLDUCK", 44, "CLOUDNINE", "TIMID")])
    t("Map 681 Prism Falls", "FISHERMAN", "Lachlan", "There's a long blue one under the third fall. That's the rumour.",
      [m("DRAGONAIR", 41, "SHEDSKIN", "ADAMANT"), m("FLOATZEL", 42, "SWIFTSWIM", "JOLLY"), m("POLIWRATH", 43, "DAMP", "ADAMANT"), m("MILOTIC", 44, "COMPETITIVE", "MODEST")])
    t("Map 681 Prism Falls", "PAINTER", "Iris", "Seven colours and I only brought six. That's what went wrong.",
      [m("SMEARGLE", 41, "OWNTEMPO", "ADAMANT"), m("SWIRLIX", 42, "SWEETVEIL", "MODEST"), m("AROMATISSE", 43, "HEALER", "MODEST"), m("CLEFABLE", 44, "CUTECHARM", "MODEST")])
    t("Map 681 Prism Falls", "BEAUTY", "Celandine", "The spray does wonders for the skin. Less for the record.",
      [m("CLEFAIRY", 41, "CUTECHARM", "MODEST"), m("SPRITZEE", 42, "HEALER", "MODEST"), m("SLURPUFF", 43, "SWEETVEIL", "MODEST"), m("ALCREMIE", 44, "SWEETVEIL", "MODEST")])
    t("Map 681 Prism Falls", "BIRDKEEPER", "Merle", "They fly through the rainbow and come out the same colour. Shame.",
      [m("TOGETIC", 41, "SERENEGRACE", "MODEST"), m("JUMPLUFF", 42, "CHLOROPHYLL", "CALM"), m("VESPIQUEN", 43, "PRESSURE", "ADAMANT"), m("ALTARIA", 44, "NATURALCURE", "ADAMANT")])
    t("Map 693 The Briarway", "LADY", "Rosamund", "One does not lose on the royal road. One is merely delayed.",
      [m("RIBOMBEE", 41, "HONEYGATHER", "TIMID"), m("KLEFKI", 42, "PRANKSTER", "ADAMANT"), m("WHIMSICOTT", 43, "PRANKSTER", "TIMID"), m("TINKATON", 44, "MOLDBREAKER", "JOLLY")])
    t("Map 693 The Briarway", "GENTLEMAN", "Godfrey", "I clip the briars for the Queen. You've clipped me.",
      [m("CINCCINO", 41, "CUTECHARM", "JOLLY"), m("AMBIPOM", 42, "PICKUP", "JOLLY"), m("UNFEZANT", 43, "BIGPECKS", "JOLLY"), m("MILTANK", 44, "SCRAPPY", "JOLLY")])
    t("Map 693 The Briarway (double battle)", "TWINS", "Hans & Gretl", "Hans: The crumbs! Gretl: You ATE the crumbs.",
      [m("WHIMSICOTT", 42, "PRANKSTER", "TIMID"), m("COMFEY", 43, "FLOWERVEIL", "TIMID"), m("GRIMMSNARL", 44, "PRANKSTER", "ADAMANT")])
    t("Map 693 The Briarway", "COOLTRAINER_F", "Aveline", "The Kingsgate's ahead. Mind your manners and your flank.",
      [m("DEDENNE", 41, "PICKUP", "TIMID"), m("GRANBULL", 42, "INTIMIDATE", "ADAMANT"), m("DACHSBUN", 43, "WELLBAKEDBODY", "JOLLY"), m("SLURPUFF", 44, "SWEETVEIL", "MODEST")])
    t("Map 682 The Royal Chase", "TAMER", "Gawain", "The Chase was a king's hunting ground. Today I was the quarry.",
      [m("FARFETCHD", 41, "INNERFOCUS", "ADAMANT"), m("PURUGLY", 42, "OWNTEMPO", "JOLLY"), m("LOPUNNY", 43, "KLUTZ", "JOLLY"), m("BOUFFALANT", 43, "RECKLESS", "ADAMANT"), m("EXPLOUD", 44, "SOUNDPROOF", "ADAMANT")])
    t("Map 682 The Royal Chase", "POKEMONRANGER_M", "Roderick", "No snares in the reserve. No mercy either, I see.",
      [m("TANGELA", 41, "LEAFGUARD", "MODEST"), m("KECLEON", 42, "COLORCHANGE", "ADAMANT"), m("DUBWOOL", 43, "STEADFAST", "JOLLY"), m("LICKILICKY", 44, "OWNTEMPO", "ADAMANT")])
    t("Map 682 The Royal Chase", "POKEMONBREEDER", "Odila", "They're all the Queen's, on paper. They've never read the paper.",
      [m("LICKITUNG", 41, "OBLIVIOUS", "MODEST"), m("CASTFORM", 42, "FORECAST", "ADAMANT"), m("AUDINO", 43, "HEALER", "BOLD"), m("CHANSEY", 43, "SERENEGRACE", "CALM"), m("GREEDENT", 44, "CHEEKPOUCH", "ADAMANT")])
    t("Map 289 Briar Hall - Thorn Crypts", "CHANNELER", "Griselda", "Nothing rots down here. Not even a grudge.",
      [m("PALOSSAND", 43, "WATERCOMPACTION", "MODEST"), m("GOURGEIST", 44, "FRISK", "JOLLY"), m("MISMAGIUS", 45, "LEVITATE", "TIMID"), m("SINISTCHA", 46, "HOSPITALITY", "MODEST")])
    t("Map 290 Verdance Gym - Entrance", "LASS", "Poppy", "I only water them. They do the rest. Usually.",
      [m("SHIFTRY", 43, "EARLYBIRD", "ADAMANT"), m("FERROTHORN", 44, "IRONBARBS", "ADAMANT"), m("VILEPLUME", 45, "CHLOROPHYLL", "MODEST"), m("MEOWSCARADA", 46, "OVERGROW", "JOLLY")])
    t("Map 291 Verdance Gym - Puzzle Room 1", "AROMALADY", "Clover", "The whole garden leaned in to watch that.",
      [m("ELDEGOSS", 43, "COTTONDOWN", "MODEST"), m("MARACTUS", 44, "WATERABSORB", "MODEST"), m("VILEPLUME", 45, "CHLOROPHYLL", "MODEST"), m("ROSERADE", 46, "NATURALCURE", "TIMID")])
    t("Map 291 Verdance Gym - Puzzle Room 1", "PICNICKER", "Daisy", "Picnic in the Heartgarden! ...It's allowed. I asked.",
      [m("LILLIGANT", 43, "OWNTEMPO", "TIMID"), m("ESCAVALIER", 44, "SWARM", "ADAMANT"), m("LEAVANNY", 45, "SWARM", "JOLLY"), m("LEAFEON", 46, "LEAFGUARD", "JOLLY")])
    t("Map 292 Verdance Gym - Puzzle Room 2", "AROMALADY", "Lavender", "Breathe in. Now out. Now go and win.",
      [m("CHERRIM", 43, "FLOWERGIFT", "TIMID"), m("APPLETUN", 44, "RIPEN", "MODEST"), m("FERROTHORN", 45, "IRONBARBS", "ADAMANT"), m("TANGROWTH", 46, "LEAFGUARD", "MODEST")])
    t("Map 292 Verdance Gym - Puzzle Room 2", "POKEMONBREEDER", "Flora", "Raised every one from seed. They'll grow back.",
      [m("LURANTIS", 43, "LEAFGUARD", "ADAMANT"), m("FLAPPLE", 44, "GLUTTONY", "ADAMANT"), m("BELLOSSOM", 45, "CHLOROPHYLL", "MODEST"), m("VICTREEBEL", 46, "CHLOROPHYLL", "ADAMANT")])
    # ---------------------------------------------------------------------------------------------------------------
    # Ch11 - the Hart's Run, the Heartwood and the Hoarwood to Rimeholt (cap 51; route Lv 45-48, Gym 10 and dungeons 47-50)
    # Tamer Wystan: the deer-herd (story/30_SCRIPT_CH11.md)
    t("Map 700 The Hart's Run", "TAMER", "Wystan", "Stag says nothing. Most sensible position, I've always thought.",
      [m("SAWSBUCK", 45, "CHLOROPHYLL", "JOLLY"), m("STOUTLAND", 46, "SANDRUSH", "ADAMANT"), m("PYROAR", 47, "RIVALRY", "TIMID"), m("WYRDEER", 48, "FRISK", "ADAMANT")])
    t("Map 700 The Hart's Run", "COOLTRAINER_M", "Gerent", "Crown huntsman. The bloom's taken my trails and you've taken the rest.",
      [m("DODRIO", 45, "RUNAWAY", "JOLLY"), m("PIDGEOT", 46, "TANGLEDFEET", "JOLLY"), m("ARBOLIVA", 47, "SEEDSOWER", "MODEST"), m("DUDUNSPARCE", 48, "RUNAWAY", "ADAMANT")])
    t("Map 700 The Hart's Run", "HIKER", "Oswin", "The wood's growing faster than I can walk it.",
      [m("DONPHAN", 45, "STURDY", "ADAMANT"), m("TSAREENA", 46, "LEAFGUARD", "ADAMANT"), m("TOEDSCRUEL", 47, "MYCELIUMMIGHT", "TIMID"), m("TORTERRA", 48, "OVERGROW", "ADAMANT")])
    t("Map 700 The Hart's Run", "HIKER", "Leofric", "North's the Hoarwood. Bring a coat. Bring two.",
      [m("BRELOOM", 45, "POISONHEAL", "ADAMANT"), m("CRUSTLE", 46, "SHELLARMOR", "ADAMANT"), m("KLEAVOR", 47, "SHEERFORCE", "JOLLY"), m("SHUCKLE", 48, "GLUTTONY", "BOLD")])
    t("Map 703 Gossamer Heartwood", "BUGCATCHER", "Silas", "The big ones live in the heartwood. I am aware of that now.",
      [m("NINJASK", 47, "SPEEDBOOST", "JOLLY"), m("FORRETRESS", 48, "STURDY", "ADAMANT"), m("VIKAVOLT", 49, "LEVITATE", "MODEST"), m("ORBEETLE", 50, "SWARM", "TIMID")])
    t("Map 703 Gossamer Heartwood", "POKEMONRANGER_F", "Thea", "The silk's older than the Loomhouse here. Mind it.",
      [m("GALVANTULA", 47, "COMPOUNDEYES", "TIMID"), m("VIKAVOLT", 48, "LEVITATE", "MODEST"), m("ORBEETLE", 49, "SWARM", "TIMID"), m("CENTISKORCH", 50, "WHITESMOKE", "ADAMANT")])
    t("Map 703 Gossamer Heartwood", "AROMALADY", "Sylvie", "Everything's in bloom at once. It's too much. So were you.",
      [m("LEAVANNY", 47, "SWARM", "JOLLY"), m("SERPERIOR", 48, "OVERGROW", "JOLLY"), m("SCEPTILE", 49, "OVERGROW", "TIMID"), m("GOGOAT", 50, "SAPSIPPER", "ADAMANT")])
    t("Map 703 Gossamer Heartwood", "POKEMANIAC", "Arlo", "I came for one rare bug. I'm leaving with none and a limp.",
      [m("ILLUMISE", 47, "OBLIVIOUS", "TIMID"), m("VOLBEAT", 48, "SWARM", "JOLLY"), m("DURANT", 49, "SWARM", "JOLLY"), m("ACCELGOR", 50, "HYDRATION", "TIMID")])
    t("Map 708 The Bride Grove", "CHANNELER", "Maud", "She's still waiting under the tree. Don't keep her.",
      [m("TREVENANT", 47, "FRISK", "ADAMANT"), m("MIMIKYU", 48, "DISGUISE", "JOLLY"), m("DHELMISE", 49, "STEELWORKER", "ADAMANT"), m("DECIDUEYE", 50, "OVERGROW", "ADAMANT")])
    t("Map 701 The Hoarwood", "CAMPER", "Stig", "Trapper's law: what you can't catch, you salute.",
      [m("VANILLISH", 45, "SNOWCLOAK", "MODEST"), m("BEARTIC", 46, "SLUSHRUSH", "ADAMANT"), m("WEAVILE", 47, "PRESSURE", "JOLLY"), m("URSALUNA", 48, "GUTS", "ADAMANT")])
    t("Map 701 The Hoarwood", "PICNICKER", "Frida", "The tea froze in the cup. Then you happened.",
      [m("ABOMASNOW", 45, "SNOWWARNING", "ADAMANT"), m("BEARTIC", 46, "SLUSHRUSH", "ADAMANT"), m("WEAVILE", 47, "PRESSURE", "JOLLY"), m("AVALUGG", 48, "ICEBODY", "ADAMANT")])
    t("Map 701 The Hoarwood", "POKEMONRANGER_M", "Halvar", "The white stag's nobody's. Same as this win isn't mine.",
      [m("FRIGIBAX", 45, "THERMALEXCHANGE", "ADAMANT"), m("GLALIE", 46, "INNERFOCUS", "ADAMANT"), m("ABOMASNOW", 47, "SNOWWARNING", "ADAMANT"), m("AVALUGG", 48, "ICEBODY", "ADAMANT")])
    t("Map 704 Frostfang Pass", "HIKER", "Bjarne", "Closed by order of the Thane, they said. Should've listened.",
      [m("PILOSWINE", 47, "SNOWCLOAK", "ADAMANT"), m("JYNX", 48, "OBLIVIOUS", "TIMID"), m("EISCUE", 49, "ICEFACE", "ADAMANT"), m("WALREIN", 50, "ICEBODY", "MODEST")])
    t("Map 704 Frostfang Pass", "BLACKBELT", "Styr", "I break ice with my head. It's had a hard day.",
      [m("POLIWRATH", 47, "DAMP", "ADAMANT"), m("SNEASLER", 48, "PRESSURE", "JOLLY"), m("MAMOSWINE", 49, "SNOWCLOAK", "ADAMANT"), m("VANILLUXE", 50, "SNOWWARNING", "MODEST")])
    t("Map 705 Frostfang Pass 2F", "COOLTRAINER_F", "Dagny", "You slid in a straight line. Nobody does that first time.",
      [m("ARCTIBAX", 48, "THERMALEXCHANGE", "ADAMANT"), m("FROSMOTH", 49, "SHIELDDUST", "MODEST"), m("CRYOGONAL", 49, "LEVITATE", "TIMID"), m("VANILLUXE", 50, "SNOWWARNING", "MODEST")])
    t("Map 705 Frostfang Pass 2F", "POKEMANIAC", "Yngve", "Fangs in the ice, older than the pass. Mine are newer and worse.",
      [m("SHELGON", 48, "ROCKHEAD", "ADAMANT"), m("ARCTIBAX", 49, "THERMALEXCHANGE", "ADAMANT"), m("DRAGALGE", 49, "POISONPOINT", "MODEST"), m("GOODRA", 50, "SAPSIPPER", "MODEST")])
    # Rocker Bragi: a skald
    t("Map 712 The Whalebone Road", "ROCKER", "Bragi", "That'll be a verse. Not a kind one.",
      [m("EISCUE", 45, "ICEFACE", "ADAMANT"), m("KOMALA", 46, "COMATOSE", "ADAMANT"), m("DRAMPA", 47, "BERSERK", "MODEST"), m("CLOYSTER", 48, "SHELLARMOR", "ADAMANT")])
    # Isenmar Soldier M Harpooner: the Thane's harpooners (TODO_QUOTA 3: Ch11 harpooners at Lv 48-52)
    t("Map 712 The Whalebone Road", "ISENMAR_SOLDIER_M", "Harpooner", "Line's cut. Let it run.",
      [m("DREDNAW", 48, "SHELLARMOR", "ADAMANT"), m("HUNTAIL", 49, "SWIFTSWIM", "ADAMANT"), m("SIMIPOUR", 50, "GLUTTONY", "JOLLY"), m("LAPRAS", 51, "WATERABSORB", "ADAMANT")])
    # Isenmar Soldier F Harpooner: the Thane's harpooners
    t("Map 712 The Whalebone Road", "ISENMAR_SOLDIER_F", "Harpooner", "The last arch is blank. Don't hurry to fill it.",
      [m("ARCTOVISH", 48, "ICEBODY", "ADAMANT"), m("ARCTOZOLT", 49, "STATIC", "ADAMANT"), m("CETITAN", 50, "SLUSHRUSH", "ADAMANT"), m("EMPOLEON", 51, "TORRENT", "MODEST")])
    t("Map 712 The Whalebone Road", "SAILOR", "Orm", "War-sled's faster than a ship and steers worse.",
      [m("SEALEO", 45, "THICKFAT", "MODEST"), m("ALOMOMOLA", 46, "HYDRATION", "ADAMANT"), m("GOREBYSS", 47, "SWIFTSWIM", "MODEST"), m("SEISMITOAD", 48, "SWIFTSWIM", "ADAMANT")])
    t("Map 310 Rimeholt Gym - Entrance", "HIKER", "Torkel", "The lake's a floor today. Tomorrow, who knows.",
      [m("VANILLISH", 47, "SNOWCLOAK", "MODEST"), m("GLALIE", 48, "INNERFOCUS", "ADAMANT"), m("RELICANTH", 49, "ROCKHEAD", "ADAMANT"), m("AURORUS", 50, "REFRIGERATE", "MODEST")])
    t("Map 311 Rimeholt Gym - Puzzle Room 1", "COOLTRAINER_F", "Annika", "Lean into the turn. I leaned out.",
      [m("SKRELP", 47, "POISONPOINT", "ADAMANT"), m("BRUXISH", 48, "STRONGJAW", "JOLLY"), m("TENTACRUEL", 49, "CLEARBODY", "TIMID"), m("STARMIE", 50, "NATURALCURE", "TIMID")])
    t("Map 311 Rimeholt Gym - Puzzle Room 1", "SWIMMER_M", "Rurik", "I dive under the ice for a living. That was colder.",
      [m("BARRASKEWDA", 47, "SWIFTSWIM", "JOLLY"), m("GOLDUCK", 48, "CLOUDNINE", "TIMID"), m("WAILORD", 49, "OBLIVIOUS", "ADAMANT"), m("STARMIE", 50, "NATURALCURE", "TIMID")])
    t("Map 312 Rimeholt Gym - Puzzle Room 2", "COOLTRAINER_F", "Saga", "Anja skates this hall blindfolded. I can't do it sighted.",
      [m("FROSLASS", 47, "SNOWCLOAK", "JOLLY"), m("MRRIME", 48, "TANGLEDFEET", "MODEST"), m("AURORUS", 49, "REFRIGERATE", "MODEST"), m("GLACEON", 50, "SNOWCLOAK", "MODEST")])
    t("Map 312 Rimeholt Gym - Puzzle Room 2", "COOLTRAINER_M", "Jokull", "Caught an edge. Happens to the best. And to me.",
      [m("JYNX", 47, "OBLIVIOUS", "TIMID"), m("STEELIX", 48, "STURDY", "ADAMANT"), m("MRRIME", 49, "TANGLEDFEET", "MODEST"), m("MAMOSWINE", 50, "SNOWCLOAK", "ADAMANT")])
    # ---------------------------------------------------------------------------------------------------------------
    # Ch12 - Lake Rime, the Sea Grotto, the Tetherline and the Cloudstair to Skyreach (cap 55; route Lv 49-52, Gym 11 and dungeons 51-55)
    t("Map 720 The Thane's Sled-Road", "FISHERMAN", "Hrolf", "Ice is thin by the Lattice. Fish like it. I don't.",
      [m("SAMUROTT", 49, "TORRENT", "MODEST"), m("BLASTOISE", 50, "TORRENT", "MODEST"), m("WALREIN", 51, "ICEBODY", "MODEST"), m("LAPRAS", 52, "WATERABSORB", "ADAMANT")])
    t("Map 720 The Thane's Sled-Road", "SAILOR", "Ulfar", "A sled-master reads ice. I misread you.",
      [m("ARCTIBAX", 49, "THERMALEXCHANGE", "ADAMANT"), m("DEWGONG", 50, "HYDRATION", "ADAMANT"), m("WEAVILE", 51, "PRESSURE", "JOLLY"), m("CLOYSTER", 52, "SHELLARMOR", "ADAMANT")])
    t("Map 720 The Thane's Sled-Road", "COOLTRAINER_M", "Eskil", "Rimeholt breeds them hard. You weren't bred here, were you?",
      [m("DEWGONG", 49, "HYDRATION", "ADAMANT"), m("FROSMOTH", 50, "SHIELDDUST", "MODEST"), m("BEARTIC", 51, "SLUSHRUSH", "ADAMANT"), m("CETITAN", 52, "SLUSHRUSH", "ADAMANT")])
    t("Map 720 The Thane's Sled-Road", "SCIENTIST", "Thora", "The thaw's a tenth of a degree a week. You're faster.",
      [m("STUNFISK", 49, "STATIC", "MODEST"), m("TOXTRICITY", 50, "PUNKROCK", "MODEST"), m("ARCTOZOLT", 51, "STATIC", "ADAMANT"), m("CETITAN", 52, "SLUSHRUSH", "ADAMANT")])
    t("Map 728 Stillwater", "CHANNELER", "Runa", "Not frozen. Stopped. I wish I had.",
      [m("JELLICENT", 51, "CURSEDBODY", "MODEST"), m("ARCTOVISH", 52, "ICEBODY", "ADAMANT"), m("CRYOGONAL", 53, "LEVITATE", "TIMID"), m("BASCULEGION", 54, "ADAPTABILITY", "ADAMANT")])
    t("Map 721 The Mast Glacier", "HIKER", "Hallvard", "There's a ship in this glacier. Mast and all. I'd rather be on it.",
      [m("FROSLASS", 49, "SNOWCLOAK", "JOLLY"), m("AVALUGG", 50, "ICEBODY", "ADAMANT"), m("GLACEON", 51, "SNOWCLOAK", "MODEST"), m("MAMOSWINE", 52, "SNOWCLOAK", "ADAMANT")])
    t("Map 721 The Mast Glacier", "BLACKBELT", "Egil", "Cold makes the knuckles honest.",
      [m("GLALIE", 49, "INNERFOCUS", "ADAMANT"), m("CRYOGONAL", 50, "LEVITATE", "TIMID"), m("CHESNAUGHT", 51, "OVERGROW", "ADAMANT"), m("QUAQUAVAL", 52, "TORRENT", "JOLLY")])
    t("Map 721 The Mast Glacier", "RUINMANIAC", "Njal", "What the ice keeps, it keeps whole. I'm in pieces.",
      [m("PUPITAR", 49, "SHEDSKIN", "ADAMANT"), m("FROSLASS", 50, "SNOWCLOAK", "JOLLY"), m("GLIMMORA", 51, "TOXICDEBRIS", "TIMID"), m("RHYPERIOR", 52, "SOLIDROCK", "ADAMANT")])
    t("Map 723 Ebbmouth Sea Grotto", "SWIMMER_M", "Havard", "Tide's turning. So was the battle, a while back.",
      [m("BARBARACLE", 51, "TOUGHCLAWS", "ADAMANT"), m("CLAWITZER", 52, "MEGALAUNCHER", "MODEST"), m("GOLISOPOD", 53, "EMERGENCYEXIT", "ADAMANT"), m("SWAMPERT", 54, "TORRENT", "ADAMANT")])
    t("Map 723 Ebbmouth Sea Grotto", "SWIMMER_F", "Marit", "Marisol taught me to swim. She didn't teach me that.",
      [m("VELUZA", 51, "MOLDBREAKER", "ADAMANT"), m("SLOWBRO", 52, "OWNTEMPO", "MODEST"), m("BARBARACLE", 53, "TOUGHCLAWS", "ADAMANT"), m("GOLISOPOD", 54, "EMERGENCYEXIT", "ADAMANT")])
    t("Map 723 Ebbmouth Sea Grotto", "FISHERMAN", "Aegir", "Deep-water tackle, deep-water catch, shallow result.",
      [m("VELUZA", 51, "MOLDBREAKER", "ADAMANT"), m("SLOWKING", 52, "OBLIVIOUS", "MODEST"), m("VAPOREON", 53, "WATERABSORB", "MODEST"), m("DONDOZO", 54, "OBLIVIOUS", "ADAMANT")])
    t("Map 723 Ebbmouth Sea Grotto", "SAILOR", "Rolf", "Thirty years on the Ebb and a kid sinks me in a cave.",
      [m("TATSUGIRI", 51, "COMMANDER", "MODEST"), m("TENTACRUEL", 52, "CLEARBODY", "TIMID"), m("FERALIGATR", 53, "TORRENT", "ADAMANT"), m("INTELEON", 54, "TORRENT", "TIMID")])
    t("Map 723 Ebbmouth Sea Grotto", "SWIMMER2_F", "Unn", "There's light down past the second chamber. Don't follow it.",
      [m("PALAFIN", 51, "ZEROTOHERO", "JOLLY"), m("TATSUGIRI", 52, "COMMANDER", "MODEST"), m("CLAWITZER", 53, "MEGALAUNCHER", "MODEST"), m("DRACOVISH", 54, "STRONGJAW", "ADAMANT")])
    # Engineer Halden: a cable-crew rigger
    t("Map 732 The Tetherline", "ENGINEER", "Halden", "Cable's rated for nine tons. I'm rated for less.",
      [m("KLANG", 49, "MINUS", "ADAMANT"), m("BOLTUND", 50, "STRONGJAW", "JOLLY"), m("JOLTEON", 51, "VOLTABSORB", "TIMID"), m("MAGNEZONE", 52, "STURDY", "MODEST")])
    # Engineer Brace: a cable-crew rigger
    t("Map 732 The Tetherline", "ENGINEER", "Brace", "Clip on before you look down. Then don't look down.",
      [m("COPPERAJAH", 49, "SHEERFORCE", "ADAMANT"), m("SCIZOR", 50, "SWARM", "ADAMANT"), m("KLINKLANG", 51, "MINUS", "JOLLY"), m("AGGRON", 52, "STURDY", "ADAMANT")])
    # Birdkeeper Swift: a Gale Post courier
    t("Map 732 The Tetherline", "BIRDKEEPER", "Swift", "Gale Post, on my break. This doesn't count as a delivery.",
      [m("RUFFLET", 49, "SHEERFORCE", "ADAMANT"), m("STARAPTOR", 50, "INTIMIDATE", "JOLLY"), m("GLISCOR", 51, "SANDVEIL", "JOLLY"), m("YANMEGA", 52, "TINTEDLENS", "TIMID")])
    t("Map 724 Cloudstair - Lower", "HIKER", "Anselm", "Rope, piton, prayer. You skipped two of them.",
      [m("LYCANROC", 52, "KEENEYE", "JOLLY"), m("HAWLUCHA", 53, "LIMBER", "JOLLY"), m("AERODACTYL", 53, "ROCKHEAD", "JOLLY"), m("ARCHEOPS", 54, "DEFEATIST", "JOLLY")])
    # Blackbelt Baz: a porter
    t("Map 724 Cloudstair - Lower", "BLACKBELT", "Baz", "I carry sixty pounds up this stair daily. Now a loss as well.",
      [m("RUFFLET", 52, "SHEERFORCE", "ADAMANT"), m("STARAPTOR", 53, "INTIMIDATE", "JOLLY"), m("FLAMIGO", 53, "TANGLEDFEET", "JOLLY"), m("HAWLUCHA", 54, "LIMBER", "JOLLY")])
    t("Map 725 Cloudstair - Inner", "CRUSHGIRL", "Idony", "Three points on the wall at all times. I let go.",
      [m("CARBINK", 52, "CLEARBODY", "BOLD"), m("MIENSHAO", 53, "INNERFOCUS", "JOLLY"), m("AGGRON", 53, "STURDY", "ADAMANT"), m("NOIVERN", 54, "INFILTRATOR", "TIMID")])
    t("Map 725 Cloudstair - Inner", "PSYCHIC_M", "Sorley", "I came up to hear myself think. Thank you for the interruption.",
      [m("SWOOBAT", 52, "KLUTZ", "TIMID"), m("XATU", 53, "SYNCHRONIZE", "TIMID"), m("BRONZONG", 53, "LEVITATE", "ADAMANT"), m("NOIVERN", 54, "INFILTRATOR", "TIMID")])
    t("Map 726 Cloudstair - Summit", "BIRDKEEPER", "Aquila", "Top of the stair. They nest above even this.",
      [m("CORVIKNIGHT", 53, "UNNERVE", "ADAMANT"), m("BRAVIARY", 54, "KEENEYE", "ADAMANT"), m("MANDIBUZZ", 54, "OVERCOAT", "ADAMANT"), m("AERODACTYL", 55, "ROCKHEAD", "JOLLY")])
    t("Map 726 Cloudstair - Summit", "COOLTRAINER_F", "Vela", "Skyreach is one more climb. It's all one more climb.",
      [m("VULLABY", 53, "OVERCOAT", "ADAMANT"), m("HONCHKROW", 54, "SUPERLUCK", "ADAMANT"), m("NOIVERN", 54, "INFILTRATOR", "TIMID"), m("DRAGONITE", 55, "INNERFOCUS", "ADAMANT")])
    t("Map 330 Skyreach Gym - Entrance", "GAMBLER", "Rafe", "I bet on the wind. The wind changed.",
      [m("RUFFLET", 51, "SHEERFORCE", "ADAMANT"), m("VULLABY", 52, "OVERCOAT", "ADAMANT"), m("SWELLOW", 53, "GUTS", "JOLLY"), m("FLAMIGO", 54, "TANGLEDFEET", "JOLLY")])
    t("Map 331 Skyreach Gym - Puzzle Room 1", "BIRDKEEPER", "Piers", "Tailwind's yours now. Use it.",
      [m("MANTINE", 51, "WATERABSORB", "MODEST"), m("GLISCOR", 52, "SANDVEIL", "JOLLY"), m("GYARADOS", 53, "INTIMIDATE", "ADAMANT"), m("ARCHEOPS", 54, "DEFEATIST", "JOLLY")])
    # Cooltrainer M Avery: a pilot
    t("Map 331 Skyreach Gym - Puzzle Room 1", "COOLTRAINER_M", "Avery", "Clear skies, they said. Light chop, they said.",
      [m("PAWNIARD", 51, "DEFIANT", "ADAMANT"), m("KLINKLANG", 52, "MINUS", "JOLLY"), m("PROBOPASS", 53, "MAGNETPULL", "MODEST"), m("GYARADOS", 54, "INTIMIDATE", "ADAMANT")])
    t("Map 332 Skyreach Gym - Puzzle Room 2", "BIRDKEEPER", "Robin", "Odessa flies in worse than this for fun.",
      [m("BOMBIRDIER", 51, "BIGPECKS", "ADAMANT"), m("MANTINE", 52, "WATERABSORB", "MODEST"), m("SIGILYPH", 53, "WONDERSKIN", "TIMID"), m("TOGEKISS", 54, "HUSTLE", "MODEST")])
    # Cooltrainer M Wilbur: a pilot
    t("Map 332 Skyreach Gym - Puzzle Room 2", "COOLTRAINER_M", "Wilbur", "Mayday. Mayday. ...Never mind, I've landed.",
      [m("CRAMORANT", 51, "GULPMISSILE", "JOLLY"), m("BOMBIRDIER", 52, "BIGPECKS", "ADAMANT"), m("DURALUDON", 53, "HEAVYMETAL", "TIMID"), m("ARCHALUDON", 54, "STAMINA", "TIMID")])
    # Cooltrainer F Wrenna: a sky courier
    t("Map 332 Skyreach Gym - Puzzle Room 2", "COOLTRAINER_F", "Wrenna", "Gale Post delivers in any weather. You're the weather.",
      [m("UNFEZANT", 51, "BIGPECKS", "JOLLY"), m("KILOWATTREL", 52, "VOLTABSORB", "TIMID"), m("DRIFBLIM", 53, "AFTERMATH", "MODEST"), m("CROBAT", 54, "INNERFOCUS", "JOLLY")])
    # ---------------------------------------------------------------------------------------------------------------
    # Ch13 - the Causeway, the Spire, Kingsmead and the glass roads to Lucent (cap 59; route Lv 53-56, Gym 12 and dungeons 55-58)
    # Engineer Coyle: a lineman
    t("Map 740 Conductors' Causeway", "ENGINEER", "Coyle", "Line's live. I, briefly, was not.",
      [m("EMOLGA", 53, "STATIC", "JOLLY"), m("RAICHU", 54, "STATIC", "JOLLY"), m("ZEBSTRIKA", 55, "MOTORDRIVE", "JOLLY"), m("AMPHAROS", 56, "STATIC", "MODEST")])
    # Engineer Ferro: a lineman
    t("Map 740 Conductors' Causeway", "ENGINEER", "Ferro", "Forty gantries to inspect and you're on the first.",
      [m("SKARMORY", 53, "KEENEYE", "ADAMANT"), m("ORTHWORM", 54, "EARTHEATER", "ADAMANT"), m("BISHARP", 55, "INNERFOCUS", "ADAMANT"), m("CORVIKNIGHT", 56, "UNNERVE", "ADAMANT")])
    # Crushgirl Zia: a pylon-climber
    t("Map 740 Conductors' Causeway", "CRUSHGIRL", "Zia", "I climb pylons in a storm. That was worse.",
      [m("EMOLGA", 53, "STATIC", "JOLLY"), m("ZEBSTRIKA", 54, "MOTORDRIVE", "JOLLY"), m("DRIFBLIM", 55, "AFTERMATH", "MODEST"), m("LUCARIO", 56, "INNERFOCUS", "TIMID")])
    # Scientist Emeric: a researcher
    t("Map 740 Conductors' Causeway", "SCIENTIST", "Emeric", "The readings spiked when you arrived. I'm writing that down.",
      [m("ROTOM", 53, "LEVITATE", "TIMID"), m("ZEBSTRIKA", 54, "MOTORDRIVE", "JOLLY"), m("AMPHAROS", 55, "STATIC", "MODEST"), m("ELECTIVIRE", 56, "MOTORDRIVE", "JOLLY")])
    t("Map 744 Stormwatch Spire 1F", "SUPERNERD", "Nim", "I chase storms. That one caught me.",
      [m("HELIOLISK", 55, "SANDVEIL", "TIMID"), m("BELLIBOLT", 56, "STATIC", "MODEST"), m("EELEKTROSS", 57, "LEVITATE", "ADAMANT"), m("LUXRAY", 58, "RIVALRY", "ADAMANT")])
    t("Map 745 Stormwatch Spire 2F", "BIRDKEEPER", "Skye", "Up here the birds fly below you. It goes to your head.",
      [m("ELECTRODE", 55, "STATIC", "TIMID"), m("KILOWATTREL", 56, "VOLTABSORB", "TIMID"), m("EELEKTROSS", 57, "LEVITATE", "ADAMANT"), m("MAGNEZONE", 58, "STURDY", "MODEST")])
    t("Map 745 Stormwatch Spire 2F", "COOLTRAINER_M", "Galen", "The roof's the worst of it. I was the easy part.",
      [m("EELEKTRIK", 56, "LEVITATE", "ADAMANT"), m("GALVANTULA", 57, "COMPOUNDEYES", "TIMID"), m("DRACOZOLT", 57, "HUSTLE", "ADAMANT"), m("MAGNEZONE", 58, "STURDY", "MODEST")])
    t("Map 748 The Shattered Sky", "PSYCHIC_F", "Astra", "The islands drift a yard a day. I've drifted further.",
      [m("BEHEEYEM", 55, "TELEPATHY", "MODEST"), m("SIGILYPH", 56, "WONDERSKIN", "TIMID"), m("BRONZONG", 57, "LEVITATE", "ADAMANT"), m("METAGROSS", 58, "CLEARBODY", "ADAMANT")])
    t("Map 741 The Wired Wood", "POKEMONRANGER_F", "Ivy", "The cables came through and the wood grew round them. It adapts. I'm trying.",
      [m("LUXRAY", 53, "RIVALRY", "ADAMANT"), m("MEGANIUM", 54, "OVERGROW", "MODEST"), m("RILLABOOM", 55, "OVERGROW", "JOLLY"), m("HYDRAPPLE", 56, "REGENERATOR", "MODEST")])
    t("Map 741 The Wired Wood", "BUGCATCHER", "Jasper", "They nest in the junction boxes. They're cross about it.",
      [m("BOLTUND", 53, "STRONGJAW", "JOLLY"), m("HERACROSS", 54, "GUTS", "JOLLY"), m("PINSIR", 55, "HYPERCUTTER", "JOLLY"), m("LUXRAY", 56, "RIVALRY", "ADAMANT")])
    t("Map 741 The Wired Wood", "PICNICKER", "Hattie", "Don't sit on that stump. It hums. So do I, now.",
      [m("MAUSHOLD", 53, "FRIENDGUARD", "JOLLY"), m("HELIOLISK", 54, "SANDVEIL", "TIMID"), m("OINKOLOGNE", 55, "LINGERINGAROMA", "ADAMANT"), m("STOUTLAND", 56, "SANDRUSH", "ADAMANT")])
    # Tamer Hugh: an ostler at the old stables
    t("Map 756 Kingsmead", "TAMER", "Hugh", "The royal stud's gone to ruin. The bloodlines haven't.",
      [m("RAPIDASH", 53, "RUNAWAY", "JOLLY"), m("CYCLIZAR", 54, "SHEDSKIN", "JOLLY"), m("FLAREON", 55, "FLASHFIRE", "ADAMANT"), m("TYPHLOSION", 55, "BLAZE", "TIMID"), m("SLAKING", 56, "TRUANT", "JOLLY")])
    # Gambler Jeb: a tout at the horse-fair
    t("Map 756 Kingsmead", "GAMBLER", "Jeb", "Three to one on me. You'd have cleaned up.",
      [m("PORYGON2", 53, "TRACE", "MODEST"), m("OBSTAGOON", 54, "GUTS", "JOLLY"), m("WYRDEER", 55, "FRISK", "ADAMANT"), m("SNORLAX", 56, "THICKFAT", "ADAMANT")])
    t("Map 756 Kingsmead", "LADY", "Arabella", "One comes to the fair to be seen. Not like this.",
      [m("LARVESTA", 53, "FLAMEBODY", "ADAMANT"), m("CARBINK", 54, "CLEARBODY", "BOLD"), m("SYLVEON", 55, "CUTECHARM", "MODEST"), m("TOGEKISS", 56, "HUSTLE", "MODEST")])
    t("Map 756 Kingsmead", "POKEMONBREEDER", "Merrin", "Bred for the Queen's colours, every one. The Queen needn't hear of this.",
      [m("FARIGIRAF", 53, "ARMORTAIL", "MODEST"), m("PORYGONZ", 54, "ADAPTABILITY", "TIMID"), m("BLISSEY", 55, "SERENEGRACE", "MODEST"), m("SNORLAX", 56, "THICKFAT", "ADAMANT")])
    t("Map 742 Mirror Mere", "FISHERMAN", "Lowell", "I cast at the reflection. It bites better.",
      [m("LUDICOLO", 53, "SWIFTSWIM", "MODEST"), m("ESPATHRA", 54, "OPPORTUNIST", "TIMID"), m("GALLADE", 55, "STEADFAST", "ADAMANT"), m("GRENINJA", 56, "TORRENT", "TIMID")])
    t("Map 742 Mirror Mere", "SWIMMER_F", "Ondine", "Dive deep enough and you come up somewhere else.",
      [m("COMFEY", 53, "FLOWERVEIL", "TIMID"), m("GARDEVOIR", 54, "TRACE", "MODEST"), m("PRIMARINA", 55, "TORRENT", "MODEST"), m("FLORGES", 56, "FLOWERVEIL", "MODEST")])
    t("Map 742 Mirror Mere", "PAINTER", "Odilon", "I paint the mere. It never looks back the same.",
      [m("ESPATHRA", 53, "OPPORTUNIST", "TIMID"), m("GOLDUCK", 54, "CLOUDNINE", "TIMID"), m("GARDEVOIR", 55, "TRACE", "MODEST"), m("FLORGES", 56, "FLOWERVEIL", "MODEST")])
    t("Map 743 Antumbra Threshold", "PSYCHIC_M", "Thaddeus", "The roots are overhead. You get used to it. I haven't.",
      [m("MEOWSTIC", 55, "KEENEYE", "TIMID"), m("GOTHITELLE", 56, "FRISK", "MODEST"), m("REUNICLUS", 57, "MAGICGUARD", "MODEST"), m("HATTERENE", 58, "ANTICIPATION", "MODEST")])
    t("Map 743 Antumbra Threshold", "CHANNELER", "Drusilla", "Behind the glass, everyone's expected. Even you.",
      [m("BANETTE", 55, "FRISK", "ADAMANT"), m("MABOSSTIFF", 56, "INTIMIDATE", "JOLLY"), m("DUSKNOIR", 57, "PRESSURE", "ADAMANT"), m("GHOLDENGO", 58, "GOODASGOLD", "MODEST")])
    t("Map 752 The Looking-Glass Wood", "PSYCHIC_F", "Alys", "The stream runs uphill. I thought I would, too.",
      [m("GALLADE", 53, "STEADFAST", "ADAMANT"), m("ESPEON", 54, "SYNCHRONIZE", "TIMID"), m("EXEGGUTOR", 55, "CHLOROPHYLL", "MODEST"), m("DELPHOX", 56, "BLAZE", "TIMID")])
    t("Map 752 The Looking-Glass Wood (double battle)", "TWINS", "Dee & Dum", "Dee: Contrariwise! Dum: We lost. No contrariwise about it.",
      [m("HATTERENE", 55, "ANTICIPATION", "MODEST"), m("DELPHOX", 56, "BLAZE", "TIMID")])
    t("Map 752 The Looking-Glass Wood", "GENTLEMAN", "Hatta", "No room! No room! ...Oh, there's plenty. Sit down.",
      [m("MALAMAR", 53, "SUCTIONCUPS", "ADAMANT"), m("ORANGURU", 54, "INNERFOCUS", "MODEST"), m("ALAKAZAM", 55, "SYNCHRONIZE", "TIMID"), m("ESPEON", 56, "SYNCHRONIZE", "TIMID")])
    t("Map 755 Widdershins Walk", "CHANNELER", "Umbra", "The shadows fall toward the light here. Mine fell on its face.",
      [m("AEGISLASH", 53, "STANCECHANGE", "BOLD"), m("DHELMISE", 54, "STEELWORKER", "ADAMANT"), m("CHANDELURE", 55, "FLASHFIRE", "MODEST"), m("DUSKNOIR", 56, "PRESSURE", "ADAMANT")])
    t("Map 755 Widdershins Walk", "BURGLAR", "Gloam", "Easy to hide where the dark's on the wrong side. Hard to win.",
      [m("HOUNDOOM", 53, "EARLYBIRD", "TIMID"), m("ZOROARK", 54, "ILLUSION", "TIMID"), m("CHANDELURE", 55, "FLASHFIRE", "MODEST"), m("UMBREON", 56, "SYNCHRONIZE", "ADAMANT")])
    t("Map 755 Widdershins Walk", "COOLTRAINER_F", "Lucasta", "Lucent's lamps are ahead. Don't look at your reflection twice.",
      [m("ZWEILOUS", 53, "HUSTLE", "ADAMANT"), m("ZOROARK", 54, "ILLUSION", "TIMID"), m("INCINEROAR", 55, "BLAZE", "ADAMANT"), m("TYRANITAR", 56, "SANDSTREAM", "ADAMANT")])
    # Supernerd Lorimer: an archivist
    t("Map 345 Lucent Athenaeum - Sealed Stacks", "SUPERNERD", "Lorimer", "Shh. ...No, go on, I've already lost.",
      [m("DRAKLOAK", 55, "CLEARBODY", "JOLLY"), m("INDEEDEE", 56, "INNERFOCUS", "TIMID"), m("AEGISLASH", 57, "STANCECHANGE", "BOLD"), m("CLAYDOL", 58, "LEVITATE", "ADAMANT")])
    t("Map 355 Palace of Glass - Undercroft of Echoes", "CHANNELER", "Ione", "The echoes remember every fight. This one will take a while to fade.",
      [m("GENGAR", 55, "CURSEDBODY", "TIMID"), m("POLTEAGEIST", 56, "WEAKARMOR", "MODEST"), m("SINISTCHA", 57, "HOSPITALITY", "MODEST"), m("CURSOLA", 58, "WEAKARMOR", "MODEST")])
    # Supernerd Bede: a scholar
    t("Map 350 Lucent Gym - Entrance", "SUPERNERD", "Bede", "I catalogued every outcome. This was on page one.",
      [m("BRUXISH", 55, "STRONGJAW", "JOLLY"), m("BEHEEYEM", 56, "TELEPATHY", "MODEST"), m("ARMAROUGE", 57, "FLASHFIRE", "MODEST"), m("EXEGGUTOR", 58, "CHLOROPHYLL", "MODEST")])
    t("Map 351 Lucent Gym - Puzzle Room 1", "PSYCHIC_M", "Caspian", "I saw it coming. Seeing isn't stopping.",
      [m("MUSHARNA", 55, "FOREWARN", "MODEST"), m("GOTHITELLE", 56, "FRISK", "MODEST"), m("REUNICLUS", 57, "MAGICGUARD", "MODEST"), m("SLOWKING", 58, "OBLIVIOUS", "MODEST")])
    t("Map 351 Lucent Gym - Puzzle Room 1", "PSYCHIC_F", "Cassia", "Your mind's very loud. It's rather nice.",
      [m("HYPNO", 55, "FOREWARN", "ADAMANT"), m("SLOWBRO", 56, "OWNTEMPO", "MODEST"), m("GRIMMSNARL", 57, "PRANKSTER", "ADAMANT"), m("FARIGIRAF", 58, "ARMORTAIL", "MODEST")])
    t("Map 352 Lucent Gym - Puzzle Room 2", "PSYCHIC_M", "Leander", "The Athenaeum has a shelf for losses. I'm on it.",
      [m("INDEEDEE", 55, "INNERFOCUS", "TIMID"), m("CLAYDOL", 56, "LEVITATE", "ADAMANT"), m("MANDIBUZZ", 57, "OVERCOAT", "ADAMANT"), m("UMBREON", 58, "SYNCHRONIZE", "ADAMANT")])
    t("Map 352 Lucent Gym - Puzzle Room 2", "PSYCHIC_F", "Orla", "Ilsa says a memory's only a battle you lost to time.",
      [m("HYPNO", 55, "FOREWARN", "ADAMANT"), m("MUSHARNA", 56, "FOREWARN", "MODEST"), m("POLTEAGEIST", 57, "WEAKARMOR", "MODEST"), m("CURSOLA", 58, "WEAKARMOR", "MODEST")])
    t("Map 353 Lucent Gym - Puzzle Room 3", "CHANNELER", "Morgane", "Someone you've forgotten says well done.",
      [m("DRAKLOAK", 55, "CLEARBODY", "JOLLY"), m("MIMIKYU", 56, "DISGUISE", "JOLLY"), m("GOLURK", 57, "IRONFIST", "ADAMANT"), m("SKELEDIRGE", 58, "BLAZE", "MODEST")])
    # ---------------------------------------------------------------------------------------------------------------
    # Ch14 - Yesterday's Road, the Barrows, Spinefall, the Vertebrae, Geode Hollow and the Undersands; Gym 13 (cap 63, 67 after the badge; story/33_SCRIPT_CH14.md roster)
    # Hiker Osgood: the hiker on the halfway stone (Inverse flips Ground's immunities; Levitate still holds)
    t("Map 772 Yesterday's Road", "HIKER", "Osgood", "Zero. I like zero. Sit on it and you're nowhere for a minute.",
      [m("DONPHAN", 55, "STURDY", "ADAMANT"), m("CLAYDOL", 56, "LEVITATE", "ADAMANT"), m("GOLURK", 57, "IRONFIST", "ADAMANT")])
    # Psychic F Ilia: Novice Ilia, a Synod novice with a broom; Galarian Slowpoke wanders up from the Dreaming Quarter, the Hisuian Braviary is the road's old bird
    t("Map 772 Yesterday's Road", "PSYCHIC_F", "Ilia", "We sweep yesterday's footprints off the road. Yours too, now.",
      [m("SLOWPOKE", 54, "OWNTEMPO", "ADAMANT", form=1), m("BRONZONG", 55, "LEVITATE", "ADAMANT"), m("BRAVIARY", 56, "SHEERFORCE", "MODEST", form=1), m("GOTHITELLE", 57, "FRISK", "MODEST")])
    # Hiker Mott: the gravedigger (script: Worker)
    t("Map 772 Yesterday's Road", "HIKER", "Mott", "Dig 'em in, dig 'em out. You're the first I've had to dig myself out from.",
      [m("ZOROARK", 55, "ILLUSION", "TIMID", form=1), m("HOUNDSTONE", 56, "SANDRUSH", "ADAMANT"), m("RUNERIGUS", 57, "WANDERINGSPIRIT", "ADAMANT"), m("MUDSDALE", 58, "OWNTEMPO", "ADAMANT")])
    # Channeler Severine: Hex Maniac Severine
    t("Map 760 The Obsidian Barrows", "CHANNELER", "Severine", "The barrows remember you now. Sorry.",
      [m("MAROWAK", 55, "CURSEDBODY", "ADAMANT", form=1), m("BANETTE", 56, "FRISK", "ADAMANT"), m("POLTEAGEIST", 57, "WEAKARMOR", "MODEST"), m("MISMAGIUS", 58, "LEVITATE", "TIMID")])
    # Channeler Agathe: Medium Agathe
    t("Map 760 The Obsidian Barrows", "CHANNELER", "Agathe", "They told me you'd win. The dead are such gossips.",
      [m("SPIRITOMB", 57, "PRESSURE", "ADAMANT"), m("COFAGRIGUS", 58, "MUMMY", "MODEST"), m("DUSKNOIR", 59, "PRESSURE", "ADAMANT")])
    # Hiker Bram: Pallbearer Bram (version 1: the Brinecut Mine's Hiker Bram, twelve badges on)
    t("Map 760 The Obsidian Barrows", "HIKER", "Bram", "Carried a hundred to the barrows. Never been carried off myself till now.",
      [m("DUGTRIO", 56, "SANDVEIL", "JOLLY", form=1), m("SANDACONDA", 57, "SANDSPIT", "ADAMANT"), m("PALOSSAND", 58, "WATERCOMPACTION", "MODEST"), m("GOLURK", 59, "IRONFIST", "ADAMANT")], v=1)
    t("Map 761 Spinefall Gorge", "FISHERMAN", "Teague", "The falls take the line. They take the fight too, apparently.",
      [m("BASCULIN", 56, "RECKLESS", "JOLLY"), m("WHISCASH", 57, "OBLIVIOUS", "ADAMANT"), m("GOLDUCK", 58, "CLOUDNINE", "TIMID"), m("FLOATZEL", 59, "SWIFTSWIM", "JOLLY")])
    # Blackbelt Kenji: Waterfall-trained (Focus Energy)
    t("Map 761 Spinefall Gorge", "BLACKBELT", "Kenji", "I train under the falls. I'll be training under them a while longer.",
      [m("POLIWRATH", 57, "DAMP", "ADAMANT"), m("HITMONLEE", 58, "RECKLESS", "JOLLY"), m("CONKELDURR", 59, "GUTS", "ADAMANT")])
    # Engineer Rhys: Deep Works Fitter Rhys (script: Worker); Alolan Golem is the Works' magnet-rock
    t("Map 773 The Vertebrae", "ENGINEER", "Rhys", "Deep Works says every seam has a weak point. Found mine.",
      [m("GOLEM", 57, "MAGNETPULL", "ADAMANT", form=1), m("PROBOPASS", 58, "MAGNETPULL", "MODEST"), m("EXCADRILL", 59, "SANDFORCE", "JOLLY"), m("MAGNEZONE", 60, "STURDY", "MODEST")])
    t("Map 773 The Vertebrae", "HIKER", "Marga", "The Vertebrae's a spine. I'm feeling mine.",
      [m("AERODACTYL", 58, "ROCKHEAD", "JOLLY"), m("RHYDON", 59, "LIGHTNINGROD", "ADAMANT"), m("GARGANACL", 60, "STURDY", "ADAMANT")])
    # Lady Opaline: Gemcutter Opaline (Crystal Cavern light moves)
    t("Map 360 Cragholm", "LADY", "Opaline", "Cut wrong. One facet off and the whole stone's ruined.",
      [m("SABLEYE", 57, "KEENEYE", "ADAMANT"), m("MAWILE", 58, "HYPERCUTTER", "ADAMANT"), m("KLEFKI", 59, "PRANKSTER", "ADAMANT"), m("CARBINK", 60, "CLEARBODY", "BOLD")])
    t("Map 764 Geode Hollow", "RUINMANIAC", "Fenwick", "The geodes ring when you lose. Listen. That's me.",
      [m("SIGILYPH", 58, "WONDERSKIN", "TIMID"), m("BRONZONG", 59, "LEVITATE", "ADAMANT"), m("CLAYDOL", 60, "LEVITATE", "ADAMANT"), m("GOLURK", 61, "IRONFIST", "ADAMANT")])
    # Lady Beryl: Gemcutter Beryl
    t("Map 765 Geode Hollow B1F", "LADY", "Beryl", "The deepest stones are the clearest. I'm less clear than I was.",
      [m("CRUSTLE", 58, "SHELLARMOR", "ADAMANT"), m("MINIOR", 59, "SHIELDSDOWN", "BOLD"), m("CARBINK", 60, "CLEARBODY", "BOLD"), m("GLIMMORA", 61, "TOXICDEBRIS", "TIMID")])
    # Tamer Hamid: Camel Driver Hamid (script: Backpacker)
    t("Map 810 The Dry Tide", "TAMER", "Hamid", "The tide comes in as sand here. My caravan goes out as losers.",
      [m("STUNFISK", 59, "MIMICRY", "ADAMANT", form=1), m("SANDSLASH", 60, "SANDVEIL", "ADAMANT"), m("MUDSDALE", 61, "OWNTEMPO", "ADAMANT"), m("HIPPOWDON", 62, "SANDSTREAM", "ADAMANT")])
    # Ruinmaniac Tobiah: Unown x2 (!): O and K
    t("Map 783 Duneholt Undersands", "RUINMANIAC", "Tobiah", "O. K. That's what they spell. That's all they've ever spelled.",
      [m("UNOWN", 60, "LEVITATE", "ADAMANT", form=14), m("UNOWN", 61, "LEVITATE", "ADAMANT", form=10), m("SIGILYPH", 62, "WONDERSKIN", "TIMID"), m("COFAGRIGUS", 63, "MUMMY", "MODEST")])
    # Hiker Dunstan: the Lacecliff Walk's Hiker Dunstan (version 1): his Nacli is a Garganacl now
    t("Map 783 Duneholt Undersands", "HIKER", "Dunstan", "Another sun day. Lucky you, again.",
      [m("FLYGON", 61, "LEVITATE", "JOLLY"), m("KROOKODILE", 62, "INTIMIDATE", "JOLLY"), m("GARGANACL", 63, "STURDY", "ADAMANT")], v=1)
    # Engineer Lisle: Deep Works Engineer Lisle (script: Worker; sun + Steel); the Hisuian Arcanine guards the Works' old dig
    t("Map 783 Duneholt Undersands", "ENGINEER", "Lisle", "Sun on steel. You'd think that'd be enough.",
      [m("ARCANINE", 61, "FLASHFIRE", "JOLLY", form=1), m("EXCADRILL", 62, "SANDFORCE", "JOLLY"), m("DURALUDON", 63, "HEAVYMETAL", "TIMID"), m("MAGNEZONE", 64, "STURDY", "MODEST")])
    t("Map 370 Cragholm Gym - Lamp Room", "HIKER", "Clem", "Bastian'll tell you a story about that. Three times.",
      [m("LYCANROC", 57, "KEENEYE", "JOLLY"), m("CRUSTLE", 58, "SHELLARMOR", "ADAMANT"), m("RHYPERIOR", 59, "SOLIDROCK", "ADAMANT")])
    # Lady Jacinth: Gemcutter Jacinth
    t("Map 371 Cragholm Gym - Prism Gallery", "LADY", "Jacinth", "Every colour but the right one. Story of my afternoon.",
      [m("MAWILE", 58, "HYPERCUTTER", "ADAMANT"), m("MINIOR", 59, "SHIELDSDOWN", "BOLD"), m("GIGALITH", 60, "STURDY", "ADAMANT")])
    t("Map 371 Cragholm Gym - Prism Gallery", "HIKER", "Dolph", "Blue gate, green gate. I just walk through walls.",
      [m("GOLEM", 59, "STURDY", "ADAMANT"), m("AGGRON", 60, "STURDY", "ADAMANT"), m("TYRANITAR", 61, "SANDSTREAM", "ADAMANT")])
    # Engineer Ness: a quarry worker
    t("Map 372 Cragholm Gym - Quarry", "ENGINEER", "Ness", "Quarry rules: what breaks, you leave.",
      [m("COALOSSAL", 59, "FLAMEBODY", "ADAMANT"), m("STONJOURNER", 60, "POWERSPOT", "ADAMANT"), m("EXCADRILL", 61, "SANDFORCE", "JOLLY")])
    # Ruinmaniac Petra: the Cragholm museum's fossils
    t("Map 372 Cragholm Gym - Quarry", "RUINMANIAC", "Petra", "The museum wants them back by six. They'll be late.",
      [m("OMASTAR", 59, "SHELLARMOR", "MODEST"), m("CRADILY", 60, "SUCTIONCUPS", "ADAMANT"), m("ARMALDO", 61, "BATTLEARMOR", "ADAMANT"), m("ARCHEOPS", 62, "DEFEATIST", "JOLLY")])
    # ---------------------------------------------------------------------------------------------------------------
    # Ch15 - the Jawbone Ridge, Hindmoor, Downflame Road, the Noonless Road and the Barrow; Gym 14 (cap 67, 71 after the badge; story/34_SCRIPT_CH15.md roster)
    # Hiker Gunnar: Mountain: wind-boosted Flying is bad news for him; the Hisuian Avalugg is the ridge's old ice
    t("Map 780 The Jawbone Ridge", "HIKER", "Gunnar", "Wind off the ridge. My birds hate it. So do my rocks, now.",
      [m("AVALUGG", 60, "STRONGJAW", "ADAMANT", form=1), m("LYCANROC", 61, "KEENEYE", "JOLLY"), m("STEELIX", 62, "STURDY", "ADAMANT"), m("GARGANACL", 63, "STURDY", "ADAMANT")])
    # Cooltrainer F Rosalind: Ace Trainer
    t("Map 780 The Jawbone Ridge", "COOLTRAINER_F", "Rosalind", "Not the Rosalind you're thinking of. Thankfully.",
      [m("SKARMORY", 61, "KEENEYE", "ADAMANT"), m("MAMOSWINE", 62, "SNOWCLOAK", "ADAMANT"), m("KINGDRA", 63, "SNIPER", "JOLLY"), m("LUCARIO", 64, "INNERFOCUS", "TIMID")])
    # Cooltrainer M Brask: Dragon Tamer Brask, a deserter with no uniform
    t("Map 780 The Jawbone Ridge", "COOLTRAINER_M", "Brask", "Going home the long way. Even longer now.",
      [m("TURTONATOR", 62, "SHELLARMOR", "MODEST"), m("FLYGON", 63, "LEVITATE", "JOLLY"), m("SALAMENCE", 64, "INTIMIDATE", "JOLLY")])
    # Channeler Morag: Hex Maniac
    t("Map 781 Hindmoor", "CHANNELER", "Morag", "The moor keeps its own. It'll keep you, if you're not careful.",
      [m("GOURGEIST", 61, "FRISK", "JOLLY"), m("TREVENANT", 62, "FRISK", "ADAMANT"), m("CURSOLA", 63, "WEAKARMOR", "MODEST"), m("MISMAGIUS", 64, "LEVITATE", "TIMID")])
    # Blackbelt Ansel: Pilgrim Ansel
    t("Map 781 Hindmoor", "BLACKBELT", "Ansel", "A pilgrim walks. Today I mostly fell over.",
      [m("SNEASLER", 62, "PRESSURE", "JOLLY"), m("MEDICHAM", 63, "PUREPOWER", "ADAMANT"), m("HITMONTOP", 64, "TECHNICIAN", "ADAMANT"), m("LUCARIO", 65, "INNERFOCUS", "TIMID")])
    # Rocker Cassidy: a punk (script: Guitarist); Inverse: Poison loves it
    t("Map 781 Hindmoor", "ROCKER", "Cassidy", "Inverse road, inverse result. Should've played it backwards.",
      [m("MALAMAR", 62, "SUCTIONCUPS", "ADAMANT"), m("SKUNTANK", 63, "STENCH", "ADAMANT"), m("HOUNDOOM", 64, "EARLYBIRD", "TIMID"), m("TOXTRICITY", 65, "PUNKROCK", "MODEST")])
    # Gentleman Ashby: Mr. Ashby
    t("Map 790 Downflame Road", "GENTLEMAN", "Ashby", "Flames that burn downward. One gets used to it. One does not get used to this.",
      [m("SLOWKING", 62, "OWNTEMPO", "MODEST", form=1), m("MRRIME", 63, "TANGLEDFEET", "MODEST"), m("AEGISLASH", 64, "STANCECHANGE", "BOLD"), m("POLTEAGEIST", 65, "WEAKARMOR", "MODEST")])
    t("Map 790 Downflame Road", "PSYCHIC_F", "Seren", "I read the road. The road didn't mention you.",
      [m("MUSHARNA", 62, "FOREWARN", "MODEST"), m("INDEEDEE", 63, "INNERFOCUS", "TIMID"), m("BRONZONG", 64, "LEVITATE", "ADAMANT"), m("GARDEVOIR", 65, "TRACE", "MODEST")])
    # Channeler Wenna: Medium Wenna; the Hisuian Typhlosion's flame is a ghost-fire
    t("Map 800 The Noonless Road", "CHANNELER", "Wenna", "No noon here. Never was. You brought a little.",
      [m("TYPHLOSION", 64, "BLAZE", "TIMID", form=1), m("FROSLASS", 65, "SNOWCLOAK", "JOLLY"), m("BANETTE", 66, "FRISK", "ADAMANT"), m("DUSKNOIR", 67, "PRESSURE", "ADAMANT")])
    # Channeler Ilse: Hex Maniac
    t("Map 800 The Noonless Road", "CHANNELER", "Ilse", "Something walked with you here. It's gone ahead.",
      [m("DRAKLOAK", 65, "CLEARBODY", "JOLLY"), m("MIMIKYU", 66, "DISGUISE", "JOLLY"), m("HATTERENE", 67, "ANTICIPATION", "MODEST"), m("GENGAR", 68, "CURSEDBODY", "TIMID")])
    # Gentleman Faraday: Revenant Lord Faraday (Barrow, Cave); an old Hisuian blade at his side
    t("Map 804 Barrow of the Wardens", "GENTLEMAN", "Faraday", "I swore an oath to these halls. It didn't mention losing.",
      [m("SAMUROTT", 65, "TORRENT", "JOLLY", form=1), m("GOLURK", 66, "IRONFIST", "ADAMANT"), m("DOUBLADE", 67, "NOGUARD", "ADAMANT"), m("AEGISLASH", 68, "STANCECHANGE", "BOLD")])
    t("Map 392 Gravenmoor Gym - Dead Nave", "CHANNELER", "Edwina", "The bell's for the living. You'll hear it for a while.",
      [m("DRIFBLIM", 61, "AFTERMATH", "MODEST"), m("BANETTE", 62, "FRISK", "ADAMANT"), m("CHANDELURE", 63, "FLASHFIRE", "MODEST")])
    t("Map 392 Gravenmoor Gym - Dead Nave", "CHANNELER", "Beatrix", "They don't move the pews. They just watch you do it.",
      [m("JELLICENT", 62, "CURSEDBODY", "MODEST"), m("COFAGRIGUS", 63, "MUMMY", "MODEST"), m("DUSKNOIR", 64, "PRESSURE", "ADAMANT")])
    t("Map 392 Gravenmoor Gym - Dead Nave", "CHANNELER", "Grizel", "Ysolde sang for them once. You fight like a hymn.",
      [m("SABLEYE", 62, "KEENEYE", "ADAMANT"), m("MISMAGIUS", 63, "LEVITATE", "TIMID"), m("GENGAR", 64, "CURSEDBODY", "TIMID")])
    # Gentleman Mortimer: the revenant
    t("Map 392 Gravenmoor Gym - Dead Nave", "GENTLEMAN", "Mortimer", "One doesn't die in the Dead Nave. One merely sits down.",
      [m("SINISTCHA", 63, "HOSPITALITY", "MODEST"), m("GHOLDENGO", 64, "GOODASGOLD", "MODEST"), m("AEGISLASH", 65, "STANCECHANGE", "BOLD")])
    t("Map 392 Gravenmoor Gym - Dead Nave", "LADY", "Ermengarde", "My veil is three hundred years old. So is that line.",
      [m("FROSLASS", 63, "SNOWCLOAK", "JOLLY"), m("POLTEAGEIST", 64, "WEAKARMOR", "MODEST"), m("CHANDELURE", 65, "FLASHFIRE", "MODEST")])
    # Hollow Grunt F Acolyte: the Mourner-acolyte (HOLLOW)
    t("Map 392 Gravenmoor Gym - Dead Nave", "HOLLOW_GRUNT_F", "Acolyte", "The Mourner taught us grief. You're teaching us something else.",
      [m("TREVENANT", 64, "FRISK", "ADAMANT"), m("DUSKNOIR", 65, "PRESSURE", "ADAMANT"), m("SKELEDIRGE", 66, "BLAZE", "MODEST")])
    # ---------------------------------------------------------------------------------------------------------------
    # Ch19 - two script-roster rows (story/38_SCRIPT_CH19.md) that carry the last four species (cap 85)
    # Cooltrainer F Isolde: script roster (story/38_SCRIPT_CH19.md): Ace Trainer Isolde
    t("Map 861 The Thornwar Marches", "COOLTRAINER_F", "Isolde", "Three kingdoms' worst and you walked through them.",
      [m("KINGAMBIT", 80, "SUPREMEOVERLORD", "ADAMANT"), m("VOLCARONA", 80, "FLAMEBODY", "TIMID"), m("HYDREIGON", 81, "LEVITATE", "TIMID")])
    # Coolcouple Hjal & Ama: script roster: Sigrun's riders Hjal and Ama (double battle)
    t("Map 864 Wyrmscar Rift (double battle)", "COOLCOUPLE", "Hjal & Ama", "Hjal: She'll hear of this. Ama: She'll be pleased.",
      [m("ALTARIA", 82, "NATURALCURE", "ADAMANT"), m("BAXCALIBUR", 82, "THERMALEXCHANGE", "JOLLY"), m("DRAGAPULT", 83, "INFILTRATOR", "JOLLY"), m("SALAMENCE", 83, "INTIMIDATE", "JOLLY")])
    return R
