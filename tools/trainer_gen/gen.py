# Prismfall trainers.txt generator (scratch). Run: python3 -I gen.py > trainers.txt
# Each team is written once (Standard); Hard (+100) and Casual (+200) are derived.
import sys

EV = {  # PBS order: HP, Atk, Def, Spe, SpA, SpD
    "A": "4,252,0,252,0,0", "S": "4,0,0,252,252,0", "BA": "252,252,4,0,0,0",
    "BS": "252,0,4,0,252,0", "PD": "252,0,252,0,0,4", "SD": "252,0,4,0,0,252",
    "HA": "252,252,0,0,0,4", "HS": "252,0,0,4,252,0", "MX": "0,128,0,252,128,0",
    "BPD": "252,4,252,0,0,0", "SPD": "252,0,0,4,0,252",
}
TR_IV = "31,31,31,0,31,31"
MEGA_STONES = {"SABLENITE", "GYARADOSITE", "TYRANITARITE", "LUCARIONITE", "METAGROSSITE", "GENGARITE", "SALAMENCITE", "GALLADITE", "GARDEVOIRITE",
               "LATIASITE", "MAWILITE", "BANETTITE"}

def P(sp, lv, ab, item, nat, moves, ev="A", only=None, hard=None, casual=None, **kw):
    d = dict(sp=sp, lv=lv, ab=ab, item=item, nat=nat, moves=moves, ev=ev, only=only,
             hard=hard or {}, casual=casual or {})
    d.update(kw)
    return d

def std_iv(top):
    return 12 if top <= 23 else 18 if top <= 35 else 24 if top <= 51 else 28 if top <= 71 else 31

def casual_iv(top):
    return 4 if top <= 23 else 8 if top <= 35 else 12 if top <= 51 else 16 if top <= 71 else 20

def casual_drop(top):
    return 2 if top < 40 else 3 if top < 70 else 4

def bag(top, diff, boss=False):
    if top <= 19:   t = (["SUPERPOTION"], ["SUPERPOTION"] * 2, [])
    elif top <= 31: t = (["SUPERPOTION"] * 2, ["HYPERPOTION"] * 2, ["SUPERPOTION"])
    elif top <= 47: t = (["HYPERPOTION"] * 2, ["FULLRESTORE"] * 2, ["HYPERPOTION"])
    elif top <= 67: t = (["FULLRESTORE"] * 2, ["FULLRESTORE"] * 3, ["HYPERPOTION"])
    else:           t = (["FULLRESTORE"] * 2, ["FULLRESTORE"] * 3, ["FULLRESTORE"])
    return list(t[diff])

def render(ttype, name, version, mons, lose, diff, cap, size_note="", mega_std=False, route=False):
    """diff 0 std, 1 hard, 2 casual. mons = list of P dicts (already filtered)."""
    top = max(m["lv"] for m in mons)
    out = ["#-------------------------------"]
    hdr = "[%s,%s]" % (ttype, name) if version == 0 else "[%s,%s,%d]" % (ttype, name, version)
    out.append(hdr)
    built = []
    for m in mons:
        o = dict(m)
        if diff == 1:
            o.update(m["hard"])
            if m["lv"] < cap and m.get("only") != "hard":
                o["lv"] = min(cap, m["lv"] + 1)
        elif diff == 2:
            o.update(m["casual"])
            o["lv"] = max(2, m["lv"] - (1 if route else casual_drop(top)))
        built.append(o)
    items = [] if route else bag(top, diff)
    if diff in ((0, 1) if mega_std else (1,)) and any(o["item"] in MEGA_STONES for o in built):
        items = ["MEGARING"] + items
    if diff == 2:
        for o in built:
            if o["item"] in MEGA_STONES:
                o["item"] = o.get("casual_item_fallback", "SITRUSBERRY")
    if items:
        out.append("Items = " + ",".join(items))
    out.append("LoseText = " + lose)
    for o in built:
        out.append("Pokemon = %s,%d" % (o["sp"], o["lv"]))
        if o.get("form"):
            out.append("    Form = %d" % o["form"])
        if o.get("nick"):
            out.append("    Name = %s" % o["nick"])
        if o["moves"]:
            out.append("    Moves = " + o["moves"])
        if o.get("abidx") is not None:
            out.append("    AbilityIndex = %d" % o["abidx"])
        elif o["ab"]:
            out.append("    Ability = " + o["ab"])
        if o["item"]:
            out.append("    Item = " + o["item"])
        if o.get("gender"):
            out.append("    Gender = " + o["gender"])
        out.append("    Nature = " + o["nat"])
        if route:
            out.append("    IV = %d" % (8, 20, 0)[diff])
            if diff == 2:
                out.append("    EV = 0")
        elif diff == 0:
            out.append("    IV = %d" % std_iv(top))
        elif diff == 1:
            out.append("    IV = " + (TR_IV if o.get("tr") else "31"))
            out.append("    EV = " + EV[o["ev"]])
        else:
            out.append("    IV = %d" % casual_iv(top))
            out.append("    EV = 0")
    return "\n".join(out)

def variants(ttype, name, base, mons, lose, cap, mega_std=False, route=False):
    """Yields (version, text) for Standard / Hard / Casual."""
    std = [m for m in mons if m.get("only") not in ("hard",)]
    hard = [m for m in mons if m.get("only") in (None, "hard", "nocasual")]
    cas = [m for m in mons if m.get("only") is None]
    res = []
    res.append(render(ttype, name, base, std, lose, 0, cap, mega_std=mega_std, route=route))
    res.append(render(ttype, name, base + 100, hard, lose, 1, cap, mega_std=mega_std, route=route))
    res.append(render(ttype, name, base + 200, cas, lose, 2, cap, mega_std=mega_std, route=route))
    return res

OUT = []
def section(title):
    OUT.append("#===============================================================================\n# " + title +
               "\n#===============================================================================")

# ------------------------------------------------------------------------------
# WARDENS
# ------------------------------------------------------------------------------
WARDENS = []
def warden(gym, ttype, name, cap, field, lose, mons):
    WARDENS.append((gym, ttype, name, cap, field, lose, mons))

warden(1, "LEADER_TAMSIN", "Tamsin", 15, "SILKWOOD", "Oh! You've unpicked every stitch. Well sewn, challenger.", [
    P("JOLTIK", 13, "COMPOUNDEYES", "ORANBERRY", "MODEST", "ELECTROWEB,FURYCUTTER,STRINGSHOT,ABSORB", "S", casual={"moves": "ELECTROWEB,FURYCUTTER,ABSORB"},
      hard={"item": "FOCUSSASH", "moves": "ELECTROWEB,BUGBITE,STRINGSHOT,THUNDERWAVE"}),
    P("SURSKIT", 13, "SWIFTSWIM", "ORANBERRY", "TIMID", "WATERGUN,QUICKATTACK,STRINGSHOT,SWEETSCENT", "S",
      only="nocasual", hard={"moves": "BUBBLEBEAM,QUICKATTACK,STRINGSHOT,STRUGGLEBUG", "item": "BERRYJUICE"}),
    P("VIVILLON", 14, "COMPOUNDEYES", "SILVERPOWDER", "TIMID", "STRUGGLEBUG,GUST,STUNSPORE,POISONPOWDER", "S",
      only="hard"),
    P("SWADLOON", 15, "OVERCOAT", "EVIOLITE", "ADAMANT", "RAZORLEAF,BUGBITE,STRINGSHOT,PROTECT", "BA",
      nick="Bobbin", casual={"ab": "LEAFGUARD"}),
])
warden(2, "LEADER_DORIAN", "Dorian", 19, "GRAND_STAGE", "Bravo! Bravissimo! The audience is yours tonight!", [
    # Gym 2 is a DOUBLE battle: Std 4 / Hard 5 / Casual 3. Spread sound moves (Hyper Voice) get Grand Stage x1.5 twice over.
    P("CHATOT", 17, "BIGPECKS", "ORANBERRY", "MODEST", "CHATTER,ROUND,FURYATTACK,SING", "S",
      hard={"moves": "CHATTER,HYPERVOICE,TAUNT,ROOST", "item": "THROATSPRAY"},
      casual={"moves": "CHATTER,ROUND,PECK,GROWL"}),
    P("AMBIPOM", 18, "TECHNICIAN", "SILKSCARF", "JOLLY", "DUALCHOP,SWIFT,ASTONISH,TICKLE", "A",
      hard={"moves": "FAKEOUT,DUALCHOP,SWIFT,UTURN"}),
    P("LOUDRED", 18, "SCRAPPY", "SITRUSBERRY", "MODEST", "ECHOEDVOICE,BITE,HOWL,UPROAR", "S", only="nocasual",
      hard={"moves": "HYPERVOICE,BITE,UPROAR,PROTECT"}),
    P("FURFROU", 18, "FURCOAT", "SITRUSBERRY", "JOLLY", "HEADBUTT,BABYDOLLEYES,SNARL,UTURN", "BPD", only="hard"),
    P("KECLEON", 19, "COLORCHANGE", "SITRUSBERRY", "ADAMANT", "SHADOWSNEAK,PSYBEAM,THIEF,FEINT", "BA",
      casual={"moves": "SHADOWSNEAK,THIEF,FEINT,LICK"},
      hard={"ab": "PROTEAN", "moves": "FAKEOUT,SHADOWSNEAK,KNOCKOFF,ROCKTOMB"}),
])
warden(3, "LEADER_MARISOL", "Marisol", 23, "WATER_SURFACE", "Ha! Tide's turned. Take the badge before I change my mind.", [
    P("PELIPPER", 21, "DRIZZLE", "DAMPROCK", "MODEST", "WATERPULSE,WINGATTACK,SUPERSONIC,PROTECT", "BS",
      hard={"moves": "WATERPULSE,AIRSLASH,ROOST,TAILWIND"}),
    P("LANTURN", 22, "VOLTABSORB", "ORANBERRY", "MODEST", "BUBBLEBEAM,SPARK,CONFUSERAY,THUNDERWAVE", "BS",
      only="nocasual", hard={"moves": "BUBBLEBEAM,SPARK,ELECTROBALL,THUNDERWAVE", "item": "SITRUSBERRY"}),
    P("ARAQUANID", 22, "WATERBUBBLE", "SITRUSBERRY", "ADAMANT", "BUBBLEBEAM,BUGBITE,BITE,AQUARING", "BA",
      only="hard", hard={"moves": "LIQUIDATION,LEECHLIFE,CRUNCH,AQUARING"}),
    P("FLOATZEL", 22, "SWIFTSWIM", "MYSTICWATER", "JOLLY", "WATERPULSE,BITE,QUICKATTACK,SWIFT", "A",
      hard={"moves": "AQUAJET,WATERPULSE,CRUNCH,ICEFANG", "nat": "NAIVE"}),
    P("GYARADOS", 23, "INTIMIDATE", "SITRUSBERRY", "ADAMANT", "WATERFALL,BITE,ICEFANG,SCARYFACE", "A",
      nick="Lucky", casual={"moves": "BITE,TWISTER,BRINE,LEER"},
      hard={"moves": "WATERFALL,BITE,ICEFANG,DRAGONDANCE"}),
])
warden(4, "LEADER_ROOK", "Rook", 27, "NEON_GRID", "Cut! ...Okay, okay, that's going in the highlight reel. You earned it.", [
    P("LUXIO", 25, "INTIMIDATE", "MAGNET", "ADAMANT", "SPARK,BITE,CHARGE,ROAR", "A",
      hard={"moves": "SPARK,CRUNCH,FIREFANG,ICEFANG", "item": "SITRUSBERRY"}),
    P("ELECTABUZZ", 25, "STATIC", "EVIOLITE", "NAIVE", "SHOCKWAVE,LOWSWEEP,QUICKATTACK,SCREECH", "MX",
      only="nocasual", hard={"moves": "THUNDERPUNCH,BRICKBREAK,ICEPUNCH,QUICKATTACK", "nat": "JOLLY", "ev": "A"}),
    P("HELIOLISK", 26, "DRYSKIN", "SITRUSBERRY", "TIMID", "PARABOLICCHARGE,GRASSKNOT,QUICKATTACK,THUNDERWAVE", "S",
      only="hard"),
    P("TOXTRICITY", 26, "PUNKROCK", "ORANBERRY", "MODEST", "SPARK,VENOSHOCK,NOBLEROAR,ACIDSPRAY", "S",
      hard={"moves": "OVERDRIVE,VENOSHOCK,HYPERVOICE,VOLTSWITCH", "item": "THROATSPRAY"},
      casual={"ab": "PLUS"}),
    P("ROTOM", 27, "LEVITATE", "SITRUSBERRY", "MODEST", "SHOCKWAVE,HEX,HYDROPUMP,THUNDERWAVE", "S", form=2,
      nick="Camera", casual={"moves": "SHOCKWAVE,HEX,THUNDERWAVE,CONFUSERAY"}, hard={"moves": "HYDROPUMP,THUNDERBOLT,HEX,WILLOWISP", "nat": "TIMID"}),
])
warden(5, "LEADER_SAHAR", "Sahar", 31, "DESERT", "The sand remembers everything. It will remember you, too.", [
    P("HIPPOPOTAS", 29, "SANDSTREAM", "SMOOTHROCK", "IMPISH", "BULLDOZE,BITE,YAWN,STEALTHROCK", "PD",
      hard={"moves": "HIGHHORSEPOWER,CRUNCH,YAWN,STEALTHROCK"}),
    P("DUGTRIO", 29, "ARENATRAP", "FOCUSSASH", "JOLLY", "DIG,SUCKERPUNCH,NIGHTSLASH,SANDTOMB", "A", only="hard",
      hard={"moves": "HIGHHORSEPOWER,SUCKERPUNCH,ROCKSLIDE,MEMENTO"}),
    P("SANDACONDA", 30, "SANDSPIT", "SITRUSBERRY", "IMPISH", "BULLDOZE,BRUTALSWING,GLARE,ROCKTOMB", "BPD",
      only="nocasual", hard={"moves": "HIGHHORSEPOWER,STONEEDGE,GLARE,COIL"}),
    P("KROKOROK", 30, "MOXIE", "EVIOLITE", "JOLLY", "CRUNCH,DIG,SANDTOMB,SWAGGER", "A",
      hard={"moves": "CRUNCH,STOMPINGTANTRUM,ROCKSLIDE,FIREFANG"}, casual={"ab": "INTIMIDATE"}),
    P("CLAYDOL", 31, "LEVITATE", "SOFTSAND", "MODEST", "EARTHPOWER,EXTRASENSORY,ROCKTOMB,RAPIDSPIN", "BS",
      nick="Effigy", hard={"moves": "SCORCHINGSANDS,PSYCHIC,ICEBEAM,STEALTHROCK", "item": "SITRUSBERRY"}),
])
warden(6, "LEADER_CORVIN", "Corvin", 35, "CORROSIVE_MIRE", "Hmph. Clean work. The mire doesn't give that compliment often.", [
    P("WEEZING", 33, "LEVITATE", "BLACKSLUDGE", "BOLD", "STRANGESTEAM,SLUDGE,WILLOWISP,TOXICSPIKES", "PD", form=1,
      hard={"ab": "NEUTRALIZINGGAS", "moves": "STRANGESTEAM,SLUDGEBOMB,WILLOWISP,TOXICSPIKES"}),
    P("CROBAT", 33, "INNERFOCUS", "SITRUSBERRY", "JOLLY", "CROSSPOISON,AIRCUTTER,BITE,SUPERSONIC", "A",
      only="nocasual", hard={"moves": "CROSSPOISON,ACROBATICS,UTURN,TAUNT", "item": None}),
    P("SALAZZLE", 34, "CORROSION", "BLACKSLUDGE", "TIMID", "TOXIC,VENOSHOCK,FLAMETHROWER,NASTYPLOT", "S",
      only="hard", gender="female"),
    P("AMOONGUSS", 34, "EFFECTSPORE", "BLACKSLUDGE", "RELAXED", "GIGADRAIN,VENOSHOCK,STUNSPORE,CLEARSMOG", "PD",
      hard={"ab": "REGENERATOR", "moves": "GIGADRAIN,SLUDGEBOMB,SPORE,CLEARSMOG"}),
    P("DRAPION", 34, "SNIPER", "SCOPELENS", "ADAMANT", "POISONFANG,CRUNCH,KNOCKOFF,FELLSTINGER", "A",
      hard={"moves": "POISONJAB,CRUNCH,EARTHQUAKE,SWORDSDANCE", "item": "LIFEORB"}),
    P("TOXAPEX", 35, "MERCILESS", "BLACKSLUDGE", "BOLD", "VENOSHOCK,TOXIC,LIQUIDATION,RECOVER", "BPD",
      nick="Ward", casual={"ab": "LIMBER"},
      hard={"moves": "VENOSHOCK,TOXIC,SCALD,RECOVER", "item": "ROCKYHELMET"}),
])
warden(7, "LEADER_BRANN", "Brann", 39, "VOLCANIC", "Ha! Tempered steel! That's what you are, aye!", [
    P("TORKOAL", 37, "DROUGHT", "HEATROCK", "BOLD", "LAVAPLUME,BODYSLAM,YAWN,STEALTHROCK", "PD",
      hard={"moves": "LAVAPLUME,SOLARBEAM,YAWN,STEALTHROCK", "nat": "MODEST", "ev": "BS"}),
    P("CAMERUPT", 37, "SOLIDROCK", "SITRUSBERRY", "QUIET", "LAVAPLUME,EARTHPOWER,ROCKSLIDE,YAWN", "BS",
      only="nocasual", hard={"moves": "ERUPTION,EARTHPOWER,ANCIENTPOWER,STEALTHROCK", "tr": True}),
    P("CENTISKORCH", 38, "FLASHFIRE", "CHARCOAL", "ADAMANT", "FIRELASH,LUNGE,CRUNCH,COIL", "A", only="hard"),
    P("MAGMORTAR", 38, "FLAMEBODY", "CHARCOAL", "MODEST", "FLAMETHROWER,THUNDERBOLT,CLEARSMOG,CONFUSERAY", "S",
      hard={"moves": "FLAMETHROWER,THUNDERBOLT,FOCUSBLAST,SOLARBEAM", "item": "LIFEORB"}),
    P("ARCANINE", 38, "INTIMIDATE", "SITRUSBERRY", "ADAMANT", "FLAREBLITZ,CRUNCH,EXTREMESPEED,ROAR", "A",
      casual={"moves": "FIREFANG,CRUNCH,EXTREMESPEED,ROAR"},
      hard={"moves": "FLAREBLITZ,WILDCHARGE,EXTREMESPEED,MORNINGSUN"}),
    P("COALOSSAL", 39, "STEAMENGINE", "SITRUSBERRY", "QUIET", "TARSHOT,HEATCRASH,ROCKSLIDE,STEALTHROCK", "HA",
      nick="Anvil", hard={"moves": "TARSHOT,FLAMETHROWER,STONEEDGE,HEATCRASH", "item": "WEAKNESSPOLICY"},
      casual={"ab": "FLAMEBODY"}),
])
warden(8, "LEADER_KAITO", "Kaito", 43, "COLOSSEUM", "...Good. Your Pokémon fight like they remember why.", [
    P("HAWLUCHA", 41, "UNBURDEN", "SITRUSBERRY", "JOLLY", "BRICKBREAK,ACROBATICS,SWORDSDANCE,ROOST", "A",
      hard={"moves": "HIGHJUMPKICK,ACROBATICS,SWORDSDANCE,ROOST"}),
    P("MEDICHAM", 41, "PUREPOWER", "CHOICEBAND", "JOLLY", "HIGHJUMPKICK,ZENHEADBUTT,BULLETPUNCH,ICEPUNCH", "A",
      only="hard"),
    P("MACHAMP", 42, "NOGUARD", "SITRUSBERRY", "ADAMANT", "DYNAMICPUNCH,KNOCKOFF,ROCKSLIDE,BULLETPUNCH", "HA",
      casual={"ab": "GUTS"}, hard={"moves": "DYNAMICPUNCH,KNOCKOFF,STONEEDGE,BULLETPUNCH"}),
    P("HITMONTOP", 42, "INTIMIDATE", "ASSAULTVEST", "ADAMANT", "FAKEOUT,TRIPLEKICK,RAPIDSPIN,SUCKERPUNCH", "BA",
      only="nocasual", hard={"moves": "FAKEOUT,CLOSECOMBAT,RAPIDSPIN,SUCKERPUNCH"}),
    P("CONKELDURR", 42, "GUTS", "FLAMEORB", "ADAMANT", "HAMMERARM,MACHPUNCH,ROCKSLIDE,BULKUP", "HA",
      casual={"item": "SITRUSBERRY"}, hard={"moves": "DRAINPUNCH,MACHPUNCH,KNOCKOFF,ICEPUNCH"}),
    P("LUCARIO", 43, "INNERFOCUS", "LIFEORB", "MODEST", "AURASPHERE,FLASHCANNON,DARKPULSE,NASTYPLOT", "S",
      nick="Memory", casual={"item": "SITRUSBERRY"},
      hard={"item": "LUCARIONITE", "ab": "JUSTIFIED", "nat": "JOLLY", "ev": "A",
            "moves": "SWORDSDANCE,CLOSECOMBAT,METEORMASH,EXTREMESPEED"}),
])
# Gym 9 = J3 is generated with the rivals (rival versioning).
warden(10, "LEADER_ANJA", "Anja", 51, "FROZEN_LAKE", "The ice held for you. It doesn't hold for many.", [
    P("NINETALES", 49, "SNOWWARNING", "LIGHTCLAY", "TIMID", "AURORAVEIL,BLIZZARD,MOONBLAST,FREEZEDRY", "S", form=1,
      casual={"moves": "AURORAVEIL,ICEBEAM,DAZZLINGGLEAM,ICYWIND", "item": "SITRUSBERRY"}),
    P("CLOYSTER", 49, "SKILLLINK", "WHITEHERB", "ADAMANT", "SHELLSMASH,ICICLESPEAR,ROCKBLAST,ICESHARD", "A",
      casual={"moves": "ICICLESPEAR,ROCKBLAST,ICESHARD,PROTECT", "item": "SITRUSBERRY"},
      hard={"item": "FOCUSSASH"}),
    P("BEARTIC", 50, "SLUSHRUSH", "NEVERMELTICE", "ADAMANT", "ICICLECRASH,SUPERPOWER,AQUAJET,SWORDSDANCE", "A",
      only="nocasual"),
    P("WALREIN", 50, "THICKFAT", "SITRUSBERRY", "MODEST", "BLIZZARD,SURF,ENCORE,PROTECT", "BS",
      hard={"ab": "ICEBODY", "item": "LEFTOVERS", "moves": "BLIZZARD,SURF,SUPERFANG,PROTECT"}),
    P("AVALUGG", 50, "STURDY", "ROCKYHELMET", "IMPISH", "AVALANCHE,BODYPRESS,IRONDEFENSE,RECOVER", "BPD",
      hard={"moves": "AVALANCHE,BODYPRESS,RAPIDSPIN,RECOVER"}),
    P("MAMOSWINE", 51, "THICKFAT", "NEVERMELTICE", "ADAMANT", "EARTHQUAKE,ICICLECRASH,ICESHARD,KNOCKOFF", "A",
      nick="Matriarch", hard={"item": "LIFEORB", "moves": "EARTHQUAKE,ICICLECRASH,ICESHARD,STEALTHROCK"}),
])
warden(11, "LEADER_ODESSA", "Odessa", 55, "STORMFRONT", "Clear skies to you, flyer. You've earned the jetstream.", [
    P("PELIPPER", 53, "DRIZZLE", "DAMPROCK", "MODEST", "HURRICANE,SCALD,UTURN,ROOST", "BS",
      hard={"moves": "HURRICANE,SCALD,UTURN,TAILWIND"}),
    P("SWANNA", 53, "HYDRATION", "LEFTOVERS", "TIMID", "HURRICANE,SURF,ROOST,DEFOG", "S", only="nocasual",
      hard={"moves": "HURRICANE,SCALD,ICEBEAM,ROOST"}),
    P("ORICORIO", 54, "DANCER", "SITRUSBERRY", "TIMID", "REVELATIONDANCE,HURRICANE,CALMMIND,ROOST", "S", form=1),
    P("NOIVERN", 54, "INFILTRATOR", "LIFEORB", "TIMID", "HURRICANE,HYPERVOICE,DRAGONPULSE,FLAMETHROWER", "S",
      casual={"item": "SITRUSBERRY"}, hard={"moves": "HURRICANE,BOOMBURST,DRACOMETEOR,FLAMETHROWER"}),
    P("TALONFLAME", 54, "GALEWINGS", "SHARPBEAK", "ADAMANT", "BRAVEBIRD,FLAREBLITZ,SWORDSDANCE,ROOST", "A",
      casual={"ab": "FLAMEBODY"}),
    P("CORVIKNIGHT", 55, "MIRRORARMOR", "LEFTOVERS", "IMPISH", "BRAVEBIRD,IRONHEAD,BULKUP,ROOST", "BPD",
      nick="Taxi", hard={"moves": "BRAVEBIRD,BODYPRESS,BULKUP,ROOST"}),
])
warden(12, "LEADER_ILSA", "Ilsa", 59, "MINDSCAPE", "...Quiet, for once. Your thoughts were very loud. I liked them.", [
    P("BRONZONG", 57, "LEVITATE", "MENTALHERB", "RELAXED", "TRICKROOM,GYROBALL,EXTRASENSORY,STEALTHROCK", "PD", tr=True,
      hard={"moves": "TRICKROOM,GYROBALL,PSYCHIC,EXPLOSION"}),
    P("MUSHARNA", 57, "FOREWARN", "SITRUSBERRY", "QUIET", "PSYCHIC,MOONBLAST,YAWN,CALMMIND", "BS", tr=True,
      only="nocasual", hard={"moves": "PSYCHIC,MOONBLAST,HYPNOSIS,DREAMEATER", "item": "LEFTOVERS"}),
    P("ESPEON", 58, "MAGICBOUNCE", "LIFEORB", "TIMID", "PSYCHIC,SHADOWBALL,DAZZLINGGLEAM,CALMMIND", "S",
      casual={"ab": "SYNCHRONIZE", "item": "SITRUSBERRY"}),
    P("GOTHITELLE", 58, "COMPETITIVE", "LEFTOVERS", "QUIET", "PSYCHIC,THUNDERBOLT,TRICKROOM,CALMMIND", "BS", tr=True,
      hard={"ab": "SHADOWTAG", "moves": "PSYCHIC,THUNDERBOLT,TRICKROOM,TAUNT"}),
    P("REUNICLUS", 58, "MAGICGUARD", "LIFEORB", "QUIET", "PSYCHIC,FOCUSBLAST,SHADOWBALL,RECOVER", "BS", tr=True,
      casual={"item": "SITRUSBERRY"}),
    P("HATTERENE", 59, "MAGICBOUNCE", "SITRUSBERRY", "QUIET", "PSYCHIC,DAZZLINGGLEAM,MYSTICALFIRE,TRICKROOM", "BS",
      tr=True, nick="Hush", hard={"item": "LIFEORB", "moves": "PSYCHIC,DAZZLINGGLEAM,MYSTICALFIRE,CALMMIND"}),
])
warden(13, "LEADER_BASTIAN", "Bastian", 63, "CRYSTAL_CAVERN", "Flawless cut. I'd set you in a crown if I had one left.", [
    P("CARBINK", 61, "STURDY", "LIGHTCLAY", "BOLD", "STEALTHROCK,POWERGEM,MOONBLAST,REFLECT", "PD",
      hard={"moves": "STEALTHROCK,POWERGEM,MOONBLAST,LIGHTSCREEN"}),
    P("GOLEM", 61, "GALVANIZE", "SITRUSBERRY", "ADAMANT", "DOUBLEEDGE,STONEEDGE,EARTHQUAKE,STEALTHROCK", "BA", form=1,
      only="nocasual", hard={"moves": "DOUBLEEDGE,STONEEDGE,EARTHQUAKE,EXPLOSION"}),
    P("AURORUS", 62, "REFRIGERATE", "SITRUSBERRY", "MODEST", "HYPERVOICE,ANCIENTPOWER,EARTHPOWER,THUNDERWAVE", "BS",
      hard={"item": "CHOICESPECS", "moves": "HYPERVOICE,FREEZEDRY,EARTHPOWER,ANCIENTPOWER"}),
    P("LYCANROC", 62, "TOUGHCLAWS", "LIFEORB", "JOLLY", "ACCELEROCK,STONEEDGE,CRUNCH,SWORDSDANCE", "A", form=2,
      casual={"item": "SITRUSBERRY"}, hard={"moves": "ACCELEROCK,STONEEDGE,CLOSECOMBAT,SWORDSDANCE"}),
    P("RHYPERIOR", 62, "SOLIDROCK", "ASSAULTVEST", "ADAMANT", "STONEEDGE,EARTHQUAKE,MEGAHORN,ICEPUNCH", "HA",
      hard={"moves": "STONEEDGE,HIGHHORSEPOWER,MEGAHORN,ICEPUNCH"}),
    P("GIGALITH", 63, "SANDSTREAM", "SITRUSBERRY", "ADAMANT", "STONEEDGE,EARTHQUAKE,HEAVYSLAM,EXPLOSION", "HA",
      nick="Geode", casual={"ab": "STURDY", "moves": "STONEEDGE,EARTHQUAKE,HEAVYSLAM,ROCKPOLISH"},
      hard={"item": "WEAKNESSPOLICY", "moves": "STONEEDGE,EARTHQUAKE,HEAVYSLAM,METEORBEAM"}),
])
warden(14, "LEADER_YSOLDE", "Ysolde", 67, "HOLLOW_CATHEDRAL", "The candles are still lit. ...Morwen would have liked you.", [
    P("SABLEYE", 65, "PRANKSTER", "LEFTOVERS", "CAREFUL", "WILLOWISP,FOULPLAY,RECOVER,SHADOWSNEAK", "SD",
      hard={"moves": "WILLOWISP,FOULPLAY,RECOVER,TAUNT"}),
    P("SPIRITOMB", 65, "INFILTRATOR", "SITRUSBERRY", "ADAMANT", "SUCKERPUNCH,SHADOWSNEAK,WILLOWISP,PAINSPLIT", "HA",
      only="nocasual", hard={"moves": "SUCKERPUNCH,POLTERGEIST,WILLOWISP,PAINSPLIT"}),
    P("DUSKNOIR", 66, "PRESSURE", "LEFTOVERS", "IMPISH", "SHADOWSNEAK,POLTERGEIST,ICEPUNCH,PAINSPLIT", "BPD",
      hard={"moves": "SHADOWSNEAK,POLTERGEIST,EARTHQUAKE,TRICKROOM"}),
    P("COFAGRIGUS", 66, "MUMMY", "SITRUSBERRY", "BOLD", "SHADOWBALL,WILLOWISP,TOXICSPIKES,PAINSPLIT", "PD",
      hard={"moves": "SHADOWBALL,WILLOWISP,NASTYPLOT,PAINSPLIT", "item": "LEFTOVERS"}),
    P("GENGAR", 66, "CURSEDBODY", "LIFEORB", "TIMID", "SHADOWBALL,SLUDGEBOMB,FOCUSBLAST,WILLOWISP", "S",
      casual={"item": "SITRUSBERRY"},
      hard={"item": "GENGARITE", "moves": "SHADOWBALL,SLUDGEBOMB,FOCUSBLAST,PERISHSONG"}),
    P("CHANDELURE", 67, "FLASHFIRE", "SPELLTAG", "MODEST", "SHADOWBALL,FLAMETHROWER,ENERGYBALL,CALMMIND", "S",
      nick="Vigil", hard={"item": "CHOICESPECS", "ab": "INFILTRATOR", "nat": "TIMID",
                          "moves": "SHADOWBALL,FIREBLAST,ENERGYBALL,TRICK"}),
])
warden(15, "LEADER_MAGNUS", "Magnus", 71, "FACTORY", "Efficient. Unexpected. I'll have to redesign around you.", [
    P("FERROTHORN", 69, "IRONBARBS", "ROCKYHELMET", "RELAXED", "STEALTHROCK,LEECHSEED,POWERWHIP,GYROBALL", "PD", tr=True),
    P("EXCADRILL", 69, "SANDRUSH", "LIFEORB", "ADAMANT", "EARTHQUAKE,IRONHEAD,ROCKSLIDE,SWORDSDANCE", "A",
      only="nocasual", hard={"ab": "MOLDBREAKER", "item": "FOCUSSASH", "moves": "EARTHQUAKE,IRONHEAD,ROCKSLIDE,RAPIDSPIN"}),
    P("KINGAMBIT", 70, "DEFIANT", "BLACKGLASSES", "ADAMANT", "KOWTOWCLEAVE,IRONHEAD,SUCKERPUNCH,SWORDSDANCE", "HA",
      hard={"ab": "SUPREMEOVERLORD", "item": "LEFTOVERS"}),
    P("KLINKLANG", 70, "CLEARBODY", "SITRUSBERRY", "ADAMANT", "SHIFTGEAR,GEARGRIND,WILDCHARGE,SUBSTITUTE", "A",
      nick="Mark One"),
    P("SCIZOR", 70, "TECHNICIAN", "METALCOAT", "ADAMANT", "BULLETPUNCH,UTURN,KNOCKOFF,SWORDSDANCE", "HA",
      hard={"item": "LIFEORB", "moves": "BULLETPUNCH,UTURN,DUALWINGBEAT,SWORDSDANCE"}),
    P("METAGROSS", 71, "CLEARBODY", "ASSAULTVEST", "ADAMANT", "METEORMASH,ZENHEADBUTT,EARTHQUAKE,BULLETPUNCH", "HA",
      nick="Engine", hard={"item": "METAGROSSITE", "nat": "JOLLY", "ev": "A",
                           "moves": "METEORMASH,ZENHEADBUTT,EARTHQUAKE,ICEPUNCH"}),
])
warden(16, "LEADER_NYX", "Nyx", 75, "NEW_MOON", "Lights on. ...Huh. You were real the whole time.", [
    P("GRIMMSNARL", 73, "PRANKSTER", "LIGHTCLAY", "CAREFUL", "REFLECT,LIGHTSCREEN,SPIRITBREAK,THUNDERWAVE", "SD",
      hard={"moves": "REFLECT,LIGHTSCREEN,SPIRITBREAK,TAUNT"}),
    P("WEAVILE", 73, "PRESSURE", "LIFEORB", "JOLLY", "KNOCKOFF,ICICLECRASH,ICESHARD,SWORDSDANCE", "A",
      casual={"item": "SITRUSBERRY"}, hard={"ab": "PICKPOCKET", "moves": "KNOCKOFF,TRIPLEAXEL,ICESHARD,SWORDSDANCE"}),
    P("MALAMAR", 74, "CONTRARY", "LEFTOVERS", "ADAMANT", "SUPERPOWER,KNOCKOFF,PSYCHOCUT,SLEEPTALK", "BA",
      only="nocasual", hard={"moves": "SUPERPOWER,KNOCKOFF,PSYCHOCUT,REST"}),
    P("UMBREON", 74, "INNERFOCUS", "LEFTOVERS", "CALM", "FOULPLAY,MOONLIGHT,YAWN,PROTECT", "SD",
      hard={"ab": "SYNCHRONIZE", "moves": "FOULPLAY,WISH,YAWN,PROTECT"}),
    P("ZOROARK", 75, "ILLUSION", "LIFEORB", "TIMID", "NIGHTDAZE,FLAMETHROWER,FOCUSBLAST,NASTYPLOT", "S",
      nick="Nobody", casual={"item": "SITRUSBERRY"},
      hard={"item": "CHOICESPECS", "moves": "NIGHTDAZE,FLAMETHROWER,FOCUSBLAST,SLUDGEBOMB"}),
    P("HONCHKROW", 74, "SUPERLUCK", "SCOPELENS", "ADAMANT", "NIGHTSLASH,BRAVEBIRD,SUCKERPUNCH,HEATWAVE", "A",
      hard={"ab": "MOXIE", "item": "LIFEORB", "moves": "NIGHTSLASH,BRAVEBIRD,SUCKERPUNCH,SUPERPOWER"}),
])
warden(17, "LEADER_CELESTINE", "Celestine", 80, "FAIRY_TALE", "And so the tale turns its final page. Happily, I hope.", [
    P("ALCREMIE", 78, "AROMAVEIL", "LEFTOVERS", "BOLD", "DECORATE,DAZZLINGGLEAM,MYSTICALFIRE,RECOVER", "BS",
      hard={"moves": "CALMMIND,DAZZLINGGLEAM,MYSTICALFIRE,RECOVER"}),
    P("MIMIKYU", 78, "DISGUISE", "LIFEORB", "JOLLY", "PLAYROUGH,SHADOWCLAW,SHADOWSNEAK,SWORDSDANCE", "A",
      only="nocasual", hard={"moves": "PLAYROUGH,SHADOWCLAW,SHADOWSNEAK,SWORDSDANCE"}),
    P("AZUMARILL", 79, "HUGEPOWER", "SITRUSBERRY", "ADAMANT", "AQUAJET,PLAYROUGH,LIQUIDATION,KNOCKOFF", "HA",
      casual={"ab": "THICKFAT"}, hard={"moves": "AQUAJET,PLAYROUGH,KNOCKOFF,BELLYDRUM"}),
    P("TINKATON", 79, "MOLDBREAKER", "SITRUSBERRY", "JOLLY", "GIGATONHAMMER,PLAYROUGH,KNOCKOFF,STEALTHROCK", "A",
      hard={"moves": "GIGATONHAMMER,PLAYROUGH,KNOCKOFF,SWORDSDANCE"}),
    P("SYLVEON", 79, "PIXILATE", "PIXIEPLATE", "MODEST", "HYPERVOICE,SHADOWBALL,CALMMIND,WISH", "BS",
      casual={"ab": "CUTECHARM"}, hard={"item": "CHOICESPECS", "moves": "HYPERVOICE,SHADOWBALL,PSYSHOCK,MYSTICALFIRE"}),
    P("TOGEKISS", 80, "SERENEGRACE", "LEFTOVERS", "TIMID", "AIRSLASH,DAZZLINGGLEAM,NASTYPLOT,ROOST", "S",
      nick="Vigilant", hard={"moves": "AIRSLASH,DAZZLINGGLEAM,FLAMETHROWER,NASTYPLOT"}),
])
warden(18, "LEADER_SIGRUN", "Sigrun", 85, "DRAGONS_DEN", "The den is quiet. That has not happened in thirty years. Go, Sovereign-to-be.", [
    P("FLYGON", 83, "LEVITATE", "CHOICESCARF", "JOLLY", "EARTHQUAKE,OUTRAGE,UTURN,STONEEDGE", "A",
      hard={"moves": "EARTHQUAKE,OUTRAGE,UTURN,FIREPUNCH"}),
    P("KOMMOO", 83, "BULLETPROOF", "THROATSPRAY", "TIMID", "CLANGOROUSSOUL,CLANGINGSCALES,AURASPHERE,FLAMETHROWER", "S",
      casual={"moves": "CLANGINGSCALES,AURASPHERE,FLAMETHROWER,POISONJAB", "item": "SITRUSBERRY"}),
    P("GOODRA", 84, "SAPSIPPER", "ASSAULTVEST", "MODEST", "DRACOMETEOR,FIREBLAST,SLUDGEBOMB,THUNDERBOLT", "BS",
      only="nocasual"),
    P("HAXORUS", 84, "MOLDBREAKER", "LUMBERRY", "JOLLY", "DRAGONDANCE,OUTRAGE,EARTHQUAKE,POISONJAB", "A",
      hard={"moves": "DRAGONDANCE,OUTRAGE,EARTHQUAKE,CLOSECOMBAT"}),
    P("DRAGAPULT", 84, "CLEARBODY", "LIFEORB", "TIMID", "DRAGONDARTS,SHADOWBALL,FLAMETHROWER,UTURN", "MX",
      casual={"item": "SITRUSBERRY"}, hard={"ab": "INFILTRATOR"}),
    P("SALAMENCE", 85, "INTIMIDATE", "LIFEORB", "NAIVE", "DRAGONDANCE,OUTRAGE,EARTHQUAKE,FIREBLAST", "MX",
      nick="Dreamwing", casual={"item": "SITRUSBERRY", "moves": "DRAGONCLAW,FLY,EARTHQUAKE,FIREFANG"},
      hard={"item": "SALAMENCITE", "nat": "ADAMANT", "ev": "A", "moves": "DRAGONDANCE,DOUBLEEDGE,EARTHQUAKE,ROOST"}),
])

# ------------------------------------------------------------------------------
# RIVAL STARTER SETS: battle -> {line: (species, moves, item, nature, ev)}
# The Gen 1 line is written; Prismfall Core swaps it to the player's generation.
# ------------------------------------------------------------------------------
LINES = {"GRASS": ["BULBASAUR", "IVYSAUR", "VENUSAUR"],
         "FIRE": ["CHARMANDER", "CHARMELEON", "CHARIZARD"],
         "WATER": ["SQUIRTLE", "WARTORTLE", "BLASTOISE"]}
SETS = {  # stage -> line -> (moves std, moves hard, nature, ev, item std, item hard)
    0: {"GRASS": ("TACKLE,GROWL,VINEWHIP", "TACKLE,GROWL,VINEWHIP,GROWTH", "MODEST", "S", None, "ORANBERRY"),
        "FIRE": ("SCRATCH,GROWL,EMBER", "SCRATCH,GROWL,EMBER", "MODEST", "S", None, "ORANBERRY"),
        "WATER": ("TACKLE,TAILWHIP,WATERGUN", "TACKLE,TAILWHIP,WATERGUN,WITHDRAW", "MODEST", "S", None, "ORANBERRY")},
    1: {"GRASS": ("RAZORLEAF,LEECHSEED,POISONPOWDER,VINEWHIP", "RAZORLEAF,LEECHSEED,SLEEPPOWDER,SEEDBOMB", "ADAMANT", "A",
                  "ORANBERRY", "SITRUSBERRY"),
        "FIRE": ("FIREFANG,DRAGONBREATH,SCRATCH,SMOKESCREEN", "FIREFANG,DRAGONBREATH,SCRATCH,SMOKESCREEN", "NAIVE", "MX",
                 "ORANBERRY", "SITRUSBERRY"),
        "WATER": ("WATERPULSE,BITE,RAPIDSPIN,PROTECT", "WATERPULSE,BITE,RAPIDSPIN,AQUATAIL", "ADAMANT", "A",
                  "ORANBERRY", "SITRUSBERRY")},
    2: {"GRASS": ("PETALBLIZZARD,SLUDGEBOMB,GROWTH,SYNTHESIS", "GIGADRAIN,SLUDGEBOMB,EARTHQUAKE,SYNTHESIS", "MODEST", "BS",
                  "SITRUSBERRY", "BLACKSLUDGE"),
        "FIRE": ("FLAMETHROWER,AIRSLASH,DRAGONPULSE,FOCUSBLAST", "FLAMETHROWER,AIRSLASH,DRAGONPULSE,FOCUSBLAST", "TIMID", "S",
                 "SITRUSBERRY", "LIFEORB"),
        "WATER": ("HYDROPUMP,ICEBEAM,FLASHCANNON,RAPIDSPIN", "HYDROPUMP,ICEBEAM,DARKPULSE,SHELLSMASH", "MODEST", "S",
                  "SITRUSBERRY", "WHITEHERB")},
}
SLOT_LINE = {"RIVAL_KESTREL": {0: "FIRE", 1: "WATER", 2: "GRASS"},
             "RIVAL_JUNO": {0: "WATER", 1: "GRASS", 2: "FIRE"},
             "LEADER_JUNO": {0: "WATER", 1: "GRASS", 2: "FIRE"}}

def starter_mon(ttype, slot, stage, lv, hidden_on_hard=False, pos_note=""):
    line = SLOT_LINE[ttype][slot]
    ms, mh, nat, ev, it, ith = SETS[stage][line]
    sp = LINES[line][stage]
    hard = {"moves": mh, "item": ith}
    if hidden_on_hard:
        hard["abidx"] = 2
    return P(sp, lv, None, it, nat, ms, ev, abidx=0, hard=hard)

RIVALS = []
def rival(ttype, name, num, cap, lose, build):
    RIVALS.append((ttype, name, num, cap, lose, build))

# --- Kestrel -----------------------------------------------------------------
rival("RIVAL_KESTREL", "Kestrel", 1, 7, "Whatever. Beginner's luck. Don't get used to it.", lambda s: [
    P("STARLY", 5, "KEENEYE", None, "JOLLY", "TACKLE,GROWL,QUICKATTACK", "A", only="hard"),
    dict(starter_mon("RIVAL_KESTREL", s, 0, 6), hard={"moves": SETS[0][SLOT_LINE["RIVAL_KESTREL"][s]][1],
                                                     "item": "ORANBERRY"}),
])
rival("RIVAL_KESTREL", "Kestrel", 2, 23, "...Fine. Stay out of the Hollow's way, then. I mean it.", lambda s: [
    P("STARAVIA", 19, "INTIMIDATE", "SHARPBEAK", "JOLLY", "WINGATTACK,QUICKATTACK,DOUBLETEAM,ENDEAVOR", "A",
      only="nocasual", hard={"moves": "WINGATTACK,QUICKATTACK,DOUBLEEDGE,UTURN", "ab": "RECKLESS"}),
    P("SANDILE", 19, "MOXIE", "ORANBERRY", "JOLLY", "BITE,SANDTOMB,SANDATTACK,HONECLAWS", "A", only="hard"),
    P("HONEDGE", 19, "NOGUARD", "ORANBERRY", "ADAMANT", "FURYCUTTER,SHADOWSNEAK,AERIALACE,METALSOUND", "BA",
      nick="Morwen", hard={"moves": "SHADOWSNEAK,IRONHEAD,AERIALACE,SWORDSDANCE", "item": "EVIOLITE"}),
    starter_mon("RIVAL_KESTREL", s, 1, 21),
])
rival("RIVAL_KESTREL", "Kestrel", 3, 35, "She had a seat, and a Plate... You don't get it. Nobody does.", lambda s: [
    P("STARAVIA", 31, "INTIMIDATE", "SHARPBEAK", "JOLLY", "AERIALACE,QUICKATTACK,TAKEDOWN,DOUBLETEAM", "A",
      hard={"ab": "RECKLESS", "moves": "BRAVEBIRD,QUICKATTACK,DOUBLEEDGE,UTURN"}),
    P("SCYTHER", 32, "TECHNICIAN", "EVIOLITE", "JOLLY", "AERIALACE,BUGBITE,QUICKATTACK,SWORDSDANCE", "A", only="hard"),
    P("KROKOROK", 31, "MOXIE", "ORANBERRY", "JOLLY", "CRUNCH,DIG,SANDTOMB,SWAGGER", "A", only="nocasual",
      hard={"moves": "CRUNCH,STOMPINGTANTRUM,ROCKSLIDE,FIREFANG", "item": "EVIOLITE"}),
    P("DOUBLADE", 32, "NOGUARD", "EVIOLITE", "ADAMANT", "SLASH,SHADOWSNEAK,IRONHEAD,AERIALACE", "BA",
      nick="Morwen", hard={"moves": "NIGHTSLASH,SHADOWSNEAK,IRONHEAD,SWORDSDANCE"}),
    starter_mon("RIVAL_KESTREL", s, 1, 33),
])
rival("RIVAL_KESTREL", "Kestrel", 4, 43, "It wasn't her. It was never her. ...Don't. Just don't.", lambda s: [
    P("STARAPTOR", 41, "INTIMIDATE", "SHARPBEAK", "JOLLY", "CLOSECOMBAT,AERIALACE,QUICKATTACK,DOUBLEEDGE", "A",
      hard={"ab": "RECKLESS", "item": "CHOICEBAND", "moves": "BRAVEBIRD,CLOSECOMBAT,DOUBLEEDGE,UTURN"}),
    P("ZWEILOUS", 41, "HUSTLE", "EVIOLITE", "ADAMANT", "DRAGONRUSH,CRUNCH,HEADBUTT,WORKUP", "A", only="hard"),
    P("KROOKODILE", 41, "MOXIE", "SITRUSBERRY", "JOLLY", "CRUNCH,EARTHQUAKE,ROCKSLIDE,SWAGGER", "A", only="nocasual",
      hard={"moves": "KNOCKOFF,EARTHQUAKE,STONEEDGE,CLOSECOMBAT", "item": "LIFEORB"}),
    P("SCIZOR", 41, "TECHNICIAN", "METALCOAT", "ADAMANT", "BULLETPUNCH,XSCISSOR,AERIALACE,SWORDSDANCE", "HA",
      hard={"moves": "BULLETPUNCH,UTURN,KNOCKOFF,SWORDSDANCE", "item": "LIFEORB"}),
    P("DOUBLADE", 42, "NOGUARD", "EVIOLITE", "ADAMANT", "NIGHTSLASH,SHADOWCLAW,IRONHEAD,SWORDSDANCE", "BA",
      nick="Morwen"),
    starter_mon("RIVAL_KESTREL", s, 2, 42),
])
def kestrel_late(lvs, mis, lose_num):
    a, b, c, d, st, ace = lvs
    def f(s):
        team = [
            P("STARAPTOR", a, "RECKLESS", "CHOICEBAND", "JOLLY", "BRAVEBIRD,CLOSECOMBAT,DOUBLEEDGE,UTURN", "A",
              casual={"ab": "INTIMIDATE", "item": "SITRUSBERRY"}),
            P("KROOKODILE", b, "MOXIE", "LIFEORB", "JOLLY", "KNOCKOFF,EARTHQUAKE,STONEEDGE,CLOSECOMBAT", "A",
              only="nocasual"),
        ]
        if mis:
            team.append(P("MISMAGIUS", c, "LEVITATE", "LIFEORB", "TIMID", "SHADOWBALL,MYSTICALFIRE,THUNDERBOLT,NASTYPLOT", "S",
                          casual={"item": "SITRUSBERRY"}, hard={"moves": "SHADOWBALL,DAZZLINGGLEAM,THUNDERBOLT,NASTYPLOT"}))
        else:
            team.append(P("SCIZOR", c, "TECHNICIAN", "LIFEORB", "ADAMANT", "BULLETPUNCH,UTURN,KNOCKOFF,SWORDSDANCE", "HA",
                          casual={"item": "METALCOAT"}))
        if d < 64:
            team.append(P("ZWEILOUS", d, "HUSTLE", "EVIOLITE", "ADAMANT", "DRAGONRUSH,CRUNCH,BODYSLAM,WORKUP", "A",
                          casual={"moves": "DRAGONBREATH,CRUNCH,BODYSLAM,WORKUP"},
                          hard={"moves": "OUTRAGE,CRUNCH,ZENHEADBUTT,DRAGONTAIL"}))
        else:
            team.append(P("HYDREIGON", d, "LEVITATE", "CHOICESPECS", "TIMID", "DRACOMETEOR,DARKPULSE,FLAMETHROWER,UTURN", "S",
                          casual={"item": "SITRUSBERRY"}, hard={"moves": "DRACOMETEOR,DARKPULSE,FLASHCANNON,UTURN"}))
        st_m = starter_mon("RIVAL_KESTREL", s, 2, st, hidden_on_hard=True)
        team.append(st_m)
        team.append(P("AEGISLASH", ace, "STANCECHANGE", "LEFTOVERS", "QUIET", "KINGSSHIELD,SHADOWBALL,SACREDSWORD,SHADOWSNEAK", "BS",
                      nick="Morwen", hard={"item": "WEAKNESSPOLICY", "moves": "KINGSSHIELD,SHADOWBALL,CLOSECOMBAT,SHADOWSNEAK"}))
        return team
    return f
rival("RIVAL_KESTREL", "Kestrel", 5, 55, "Meridian's paying for my next Ball. Funny how that works.",
      kestrel_late((52, 52, 53, 52, 54, 54), False, 5))
rival("RIVAL_KESTREL", "Kestrel", 6, 67, "She burned her own name. For YOU. ...Get out of my sight.",
      kestrel_late((64, 64, 65, 65, 66, 66), False, 6))
rival("RIVAL_KESTREL", "Kestrel", 7, 80, "They all want to use you. Fine. Walk into Crownhaven. I'll be waiting.",
      kestrel_late((77, 77, 78, 78, 79, 79), True, 7))
rival("RIVAL_KESTREL", "Kestrel", 8, 94, "If I lost, I lost to you. Not to them. ...That's enough.",
      kestrel_late((90, 91, 92, 92, 93, 94), True, 8))

def kestrel_fallen(s_):
    team = promote(kestrel_late((90, 91, 92, 92, 93, 94), True, 9)(s_))
    for i, m in enumerate(team):
        if m["sp"] == "KROOKODILE":
            team[i] = P("GENESECT", 91, "DOWNLOAD", "CHOICESCARF", "HASTY", "UTURN,IRONHEAD,THUNDERBOLT,FLAMETHROWER", "MX",
                        nick="Gauntlet", casual={"item": "SITRUSBERRY"})
    return team
rival("RIVAL_KESTREL", "Kestrel", 9, 94, "...It won't let go. Why won't it let go?", kestrel_fallen)

# --- Juno --------------------------------------------------------------------
rival("RIVAL_JUNO", "Juno", 1, 19, "Aww, you're so good at this! Okay, again soon, okay?", lambda s: [
    P("COTTONEE", 15, "PRANKSTER", "ORANBERRY", "BOLD", "FAIRYWIND,MEGADRAIN,STUNSPORE", "SD",
      only="nocasual", hard={"moves": "FAIRYWIND,MEGADRAIN,LEECHSEED,STUNSPORE"}),
    P("PETILIL", 16, "OWNTEMPO", "ORANBERRY", "MODEST", "MEGADRAIN,SLEEPPOWDER,GROWTH,LEECHSEED", "S", only="hard"),
    P("BOUNSWEET", 15, "LEAFGUARD", "ORANBERRY", "ADAMANT", "RAZORLEAF,RAPIDSPIN,PLAYNICE", "BA",
      nick="Sweetpea", hard={"moves": "RAZORLEAF,RAPIDSPIN,MAGICALLEAF,PLAYNICE", "item": "EVIOLITE"}),
    starter_mon("RIVAL_JUNO", s, 1, 17),
])
rival("RIVAL_JUNO", "Juno", 2, 35, "That's not his name in the ledger. It can't be. ...Good battle, though.", lambda s: [
    P("WHIMSICOTT", 31, "PRANKSTER", "SITRUSBERRY", "TIMID", "LEECHSEED,ENERGYBALL,COTTONSPORE,FAIRYWIND", "S",
      hard={"moves": "LEECHSEED,ENERGYBALL,MOONBLAST,TAILWIND"}),
    P("SHIINOTIC", 32, "EFFECTSPORE", "SITRUSBERRY", "CALM", "GIGADRAIN,MOONBLAST,SPORE,STRENGTHSAP", "SD", only="hard"),
    P("LILLIGANT", 31, "OWNTEMPO", "MIRACLESEED", "MODEST", "MAGICALLEAF,TEETERDANCE,SLEEPPOWDER,QUIVERDANCE", "S",
      only="nocasual", hard={"moves": "GIGADRAIN,PETALDANCE,SLEEPPOWDER,QUIVERDANCE"}),
    P("STEENEE", 32, "LEAFGUARD", "EVIOLITE", "ADAMANT", "RAZORLEAF,STOMP,RAPIDSPIN,PLAYNICE", "BA",
      nick="Sweetpea", hard={"moves": "SEEDBOMB,STOMP,RAPIDSPIN,PLAYROUGH"}),
    starter_mon("RIVAL_JUNO", s, 1, 33),
])
rival("LEADER_JUNO", "Juno", 3, 47, "I'm crying. I said I would. ...Take it. The Meadow badge is yours.", lambda s: [
    P("WHIMSICOTT", 45, "PRANKSTER", "LEFTOVERS", "TIMID", "LEECHSEED,ENERGYBALL,MOONBLAST,GROWTH", "S",
      hard={"moves": "LEECHSEED,ENERGYBALL,MOONBLAST,TAILWIND"}),
    P("SHIINOTIC", 45, "EFFECTSPORE", "SITRUSBERRY", "CALM", "GIGADRAIN,MOONBLAST,STRENGTHSAP,SLEEPPOWDER", "SD",
      only="nocasual", hard={"moves": "GIGADRAIN,MOONBLAST,STRENGTHSAP,SPORE"}),
    P("ROSERADE", 46, "NATURALCURE", "MIRACLESEED", "TIMID", "GIGADRAIN,SLUDGEBOMB,SHADOWBALL,TOXICSPIKES", "S",
      only="hard", nick="Rowan"),
    P("LILLIGANT", 46, "OWNTEMPO", "MIRACLESEED", "MODEST", "PETALDANCE,GIGADRAIN,STUNSPORE,QUIVERDANCE", "S",
      hard={"moves": "PETALDANCE,GIGADRAIN,SLEEPPOWDER,QUIVERDANCE"}),
    starter_mon("LEADER_JUNO", s, 2, 46),
    P("TSAREENA", 47, "QUEENLYMAJESTY", "SITRUSBERRY", "ADAMANT", "TROPKICK,LOWSWEEP,PLAYROUGH,UTURN", "A",
      nick="Sweetpea", casual={"ab": "LEAFGUARD"}, hard={"item": "LIFEORB", "moves": "POWERWHIP,HIGHJUMPKICK,KNOCKOFF,UTURN"}),
])
rival("RIVAL_JUNO", "Juno", 4, 90, "We started on the same dock. ...You grew more. I'm so glad it was you.", lambda s: [
    P("SHIINOTIC", 86, "EFFECTSPORE", "LEFTOVERS", "CALM", "GIGADRAIN,MOONBLAST,STRENGTHSAP,SPORE", "SD",
      casual={"moves": "GIGADRAIN,MOONBLAST,STRENGTHSAP,CONFUSERAY"}),
    P("WHIMSICOTT", 87, "PRANKSTER", "LEFTOVERS", "TIMID", "LEECHSEED,ENERGYBALL,MOONBLAST,TAILWIND", "S",
      hard={"moves": "LEECHSEED,MOONBLAST,ENCORE,TAILWIND"}),
    P("LILLIGANT", 87, "OWNTEMPO", "LIFEORB", "TIMID", "PETALDANCE,GIGADRAIN,SLEEPPOWDER,QUIVERDANCE", "S",
      casual={"item": "MIRACLESEED", "moves": "PETALDANCE,GIGADRAIN,STUNSPORE,QUIVERDANCE"}),
    P("COMFEY", 88, "TRIAGE", "LEFTOVERS", "CALM", "DRAININGKISS,GIGADRAIN,CALMMIND,SYNTHESIS", "SD"),
    starter_mon("RIVAL_JUNO", s, 2, 89, hidden_on_hard=True),
    P("TSAREENA", 90, "QUEENLYMAJESTY", "LIFEORB", "JOLLY", "POWERWHIP,HIGHJUMPKICK,KNOCKOFF,UTURN", "A",
      nick="Sweetpea", casual={"item": "SITRUSBERRY"}, hard={"item": "CHOICEBAND"}),
])

rival("RIVAL_JUNO", "Juno", 7, 97, "We did it. We actually did it.", lambda s: [
    P("WHIMSICOTT", 95, "PRANKSTER", "LEFTOVERS", "TIMID", "TAILWIND,MOONBLAST,ENCORE,LEECHSEED", "S"),
    starter_mon("RIVAL_JUNO", s, 2, 96, hidden_on_hard=True),
    P("TSAREENA", 97, "QUEENLYMAJESTY", "LIFEORB", "JOLLY", "POWERWHIP,HIGHJUMPKICK,KNOCKOFF,UTURN", "A", nick="Sweetpea"),
])

# ------------------------------------------------------------------------------
# BOSSES
# ------------------------------------------------------------------------------
ADMINS = []  # villain admins: full sets, Std/Hard/Casual (versions 0/100/200; later rematches 1, 2, ...)
ADMINS.append(("Map 120 Briarwick - first admin battle (Act I)", "HOLLOW_THISTLE", "Thistle", 15,
    "Lowmarsh is glass now. Remember that when you sleep.", [
    P("MORELULL", 13, "EFFECTSPORE", "ORANBERRY", "MODEST", "MEGADRAIN,CONFUSERAY,INGRAIN,ASTONISH", "BS", casual={"moves": "ABSORB,CONFUSERAY,ASTONISH"},
      hard={"moves": "MEGADRAIN,CONFUSERAY,LEECHSEED,DAZZLINGGLEAM"}),
    P("FOONGUS", 14, "EFFECTSPORE", "ORANBERRY", "RELAXED", "MEGADRAIN,STUNSPORE,GROWTH,ASTONISH", "PD",
      only="nocasual", hard={"ab": "REGENERATOR", "moves": "MEGADRAIN,STUNSPORE,VENOSHOCK,GROWTH"}),
    P("PHANTUMP", 15, "NATURALCURE", "SITRUSBERRY", "ADAMANT", "BRANCHPOKE,ASTONISH,LEECHSEED,CONFUSERAY", "HA",
      nick="Lowmarsh", hard={"ab": "HARVEST", "moves": "BRANCHPOKE,SHADOWCLAW,LEECHSEED,WILLOWISP"}),
]))
ADMINS.append(("Map 160 Ebbmouth - Teo Reyes, Ebbmouth Hollow cell (recurring: later battles use versions 1, 2, ...)", "HOLLOW_TEO", "Teo", 23,
    "Tell my sister— no. Don't tell her anything.", [
    P("CARVANHA", 19, "ROUGHSKIN", "ORANBERRY", "JOLLY", "AQUAJET,BITE,POISONFANG,SCARYFACE", "A",
      only="nocasual", hard={"ab": "SPEEDBOOST", "moves": "AQUAJET,CRUNCH,POISONFANG,ICEFANG", "item": "FOCUSSASH"}),
    P("BASCULIN", 20, "RECKLESS", "SITRUSBERRY", "ADAMANT", "AQUAJET,BITE,FLAIL,TAILWHIP", "A", only="hard",
      hard={"moves": "WATERFALL,CRUNCH,AQUAJET,PSYCHICFANGS"}),
    P("ARROKUDA", 20, "SWIFTSWIM", "ORANBERRY", "ADAMANT", "AQUAJET,BITE,FURYATTACK,AGILITY", "A",
      hard={"moves": "LIQUIDATION,BITE,AQUAJET,CLOSECOMBAT", "item": "MYSTICWATER"}),
    P("CHEWTLE", 21, "STRONGJAW", "SITRUSBERRY", "ADAMANT", "BITE,HEADBUTT,WATERGUN,PROTECT", "BA", nick="Snapper", casual={"moves": "BITE,WATERGUN,PROTECT,TACKLE"},
      hard={"moves": "BITE,LIQUIDATION,ICEFANG,PROTECT", "item": "EVIOLITE"}),
]))
BOSSES = []
BOSSES.append(("CHAMPION_VALEN", "Valen", 96, "Order, not justice. I chose order... Perhaps the land will forgive us both.", [
    P("BRONZONG", 92, "LEVITATE", "LEFTOVERS", "RELAXED", "STEALTHROCK,GYROBALL,PSYCHIC,TRICKROOM", "PD",
      hard={"moves": "STEALTHROCK,GYROBALL,EARTHQUAKE,EXPLOSION"}),
    P("LAPRAS", 93, "WATERABSORB", "ASSAULTVEST", "MODEST", "FREEZEDRY,HYDROPUMP,THUNDERBOLT,SPARKLINGARIA", "BS",
      nick="Ferry"),
    P("KINGDRA", 94, "SNIPER", "SCOPELENS", "MODEST", "DRACOMETEOR,HYDROPUMP,ICEBEAM,FOCUSENERGY", "S",
      hard={"ab": "SWIFTSWIM", "item": "LIFEORB", "moves": "DRACOMETEOR,HYDROPUMP,ICEBEAM,RAINDANCE"}),
    P("GALLADE", 94, "JUSTIFIED", "LIFEORB", "JOLLY", "CLOSECOMBAT,PSYCHOCUT,LEAFBLADE,SWORDSDANCE", "A",
      casual={"item": "SITRUSBERRY"},
      hard={"item": "GALLADITE", "moves": "CLOSECOMBAT,ZENHEADBUTT,KNOCKOFF,SWORDSDANCE"}),
    P("VOLCARONA", 95, "FLAMEBODY", "HEAVYDUTYBOOTS", "TIMID", "QUIVERDANCE,FIERYDANCE,BUGBUZZ,GIGADRAIN", "S",
      casual={"moves": "FIERYDANCE,BUGBUZZ,GIGADRAIN,PSYCHIC"}),
    P("ZYGARDE", 96, "POWERCONSTRUCT", "LEFTOVERS", "ADAMANT", "THOUSANDARROWS,OUTRAGE,DRAGONDANCE,STONEEDGE", "BA",
      casual={"ab": "AURABREAK", "moves": "THOUSANDARROWS,DRAGONTAIL,CRUNCH,GLARE"},
      hard={"moves": "THOUSANDARROWS,OUTRAGE,COIL,STONEEDGE"}),
]))
BOSSES.append(("MERIDIAN_VOSS", "Aurelian", 100, "The god owes us. It owes ME. ...This isn't over. Machines don't grieve.", [
    P("KLINKLANG", 96, "CLEARBODY", "SITRUSBERRY", "JOLLY", "SHIFTGEAR,GEARGRIND,WILDCHARGE,SUBSTITUTE", "A",
      ),
    P("MAGNEZONE", 96, "MAGNETPULL", "CHOICESPECS", "MODEST", "THUNDERBOLT,FLASHCANNON,VOLTSWITCH,BODYPRESS", "BS",
      casual={"item": "SITRUSBERRY", "moves": "THUNDERBOLT,FLASHCANNON,VOLTSWITCH,THUNDERWAVE"},
      hard={"moves": "THUNDERBOLT,FLASHCANNON,VOLTSWITCH,TRIATTACK"}),
    P("GOLURK", 97, "NOGUARD", "LIFEORB", "ADAMANT", "DYNAMICPUNCH,EARTHQUAKE,POLTERGEIST,STONEEDGE", "HA",
      nick="Gilder", casual={"item": "SITRUSBERRY", "ab": "IRONFIST"}),
    P("ARCHALUDON", 97, "STAMINA", "POWERHERB", "MODEST", "ELECTROSHOT,FLASHCANNON,DRACOMETEOR,BODYPRESS", "BS",
      casual={"item": "SITRUSBERRY", "moves": "THUNDERBOLT,FLASHCANNON,DRAGONPULSE,BODYPRESS"}),
    P("PORYGONZ", 99, "ADAPTABILITY", "CHOICESCARF", "TIMID", "TRIATTACK,DARKPULSE,ICEBEAM,THUNDERBOLT", "S",
      casual={"item": "SITRUSBERRY"}, hard={"moves": "HYPERBEAM,TRIATTACK,SHADOWBALL,ICEBEAM", "item": "CHOICESPECS"}),
    P("SILVALLY", 100, "RKSSYSTEM", "STEELMEMORY", "JOLLY", "MULTIATTACK,CRUSHCLAW,FLAMECHARGE,SWORDSDANCE", "A",
      form=8, nick="NULL", hard={"moves": "MULTIATTACK,PARTINGSHOT,FLAMECHARGE,SWORDSDANCE"},
      casual={"moves": "MULTIATTACK,CRUSHCLAW,FLAMECHARGE,SCARYFACE"}),
]))

# ------------------------------------------------------------------------------
# FESTIVAL CHOICE-DRAW TEAMS + STORY EXTRAS (design/NARRATIVE_KEYS.md §7)
# ------------------------------------------------------------------------------
def promote(mons, lead=None):
    """Hard sets become the Standard sets (Hard keeps them); optional new lead."""
    out = []
    for m in mons:
        n = dict(m); n["hard"] = dict(m["hard"]); n["casual"] = dict(m["casual"])
        for k, v in m["hard"].items():
            if k != "item" or v not in MEGA_STONES:
                n[k] = v
        out.append(n)
    if lead is not None:
        out.insert(0, out.pop(lead))
    return out

def relevel(mons, levels):
    return [dict(m, lv=l) for m, l in zip(mons, levels)]

def warden_mons(name):
    for gym, tt, nm, cap, field, lose, mons in WARDENS:
        if nm == name:
            return [m for m in mons if m.get("only") != "hard"] + [m for m in mons if m.get("only") == "hard"]

def drop_only(mons):
    return [dict(m, only=None) for m in mons]

EXTRA = []  # (note, ttype, name, base_version, cap, lose, mons, mega_std)
def X(note, tt, nm, v, cap, lose, mons, mega_std=False):
    EXTRA.append((note, tt, nm, v, cap, lose, mons, mega_std))

X("R16 - Marisol (Grievance) / Ebb Guild exhibition, field :WATER_SURFACE", "LEADER_MARISOL", "Marisol", 90, 90,
  "The tide always comes back. So will I.", [
    P("PELIPPER", 87, "DRIZZLE", "DAMPROCK", "MODEST", "HURRICANE,SCALD,UTURN,ROOST", "BS"),
    P("FLOATZEL", 87, "SWIFTSWIM", "LIFEORB", "ADAMANT", "LIQUIDATION,AQUAJET,ICEPUNCH,BULKUP", "A", casual={"item": "MYSTICWATER"}),
    P("LANTURN", 88, "VOLTABSORB", "LEFTOVERS", "MODEST", "SCALD,THUNDERBOLT,VOLTSWITCH,ICEBEAM", "BS"),
    P("ARAQUANID", 88, "WATERBUBBLE", "SITRUSBERRY", "ADAMANT", "LIQUIDATION,LEECHLIFE,STICKYWEB,MIRRORCOAT", "HA",
      casual={"ab": "WATERABSORB"}),
    P("BARRASKEWDA", 89, "SWIFTSWIM", "CHOICEBAND", "ADAMANT", "LIQUIDATION,CLOSECOMBAT,PSYCHICFANGS,AQUAJET", "A",
      casual={"item": "SITRUSBERRY"}),
    P("GYARADOS", 90, "INTIMIDATE", "SITRUSBERRY", "ADAMANT", "WATERFALL,DRAGONDANCE,CRUNCH,ICEFANG", "A", nick="Lucky",
      hard={"item": "GYARADOSITE"}),
])
X("R16 - Anja (exposed)", "LEADER_ANJA", "Anja", 90, 90, "Ice remembers.",
  relevel(drop_only(promote(warden_mons("Anja"))), [86, 87, 88, 88, 89, 90]))
X("R16 - Rowan, the Gardener (requires ROWAN_ALIVE); sun team", "LEADER_ROWAN", "Rowan", 90, 90,
  "Tend your garden, they told me. ...I think I finally did.", [
    P("SUNFLORA", 86, "SOLARPOWER", "HEATROCK", "MODEST", "SUNNYDAY,SOLARBEAM,EARTHPOWER,SLUDGEBOMB", "S"),
    P("LEAVANNY", 87, "CHLOROPHYLL", "LIFEORB", "JOLLY", "LEAFBLADE,XSCISSOR,KNOCKOFF,SWORDSDANCE", "A", casual={"item": "SITRUSBERRY"}),
    P("ROSERADE", 88, "NATURALCURE", "FOCUSSASH", "TIMID", "LEAFSTORM,SLUDGEBOMB,SHADOWBALL,SPIKES", "S"),
    P("BRELOOM", 88, "TECHNICIAN", "LIFEORB", "JOLLY", "MACHPUNCH,BULLETSEED,ROCKTOMB,SPORE", "A",
      casual={"moves": "MACHPUNCH,BULLETSEED,ROCKTOMB,STUNSPORE", "item": "SITRUSBERRY"}),
    P("SHIFTRY", 89, "CHLOROPHYLL", "LIFEORB", "JOLLY", "LEAFBLADE,KNOCKOFF,SUCKERPUNCH,SWORDSDANCE", "A", casual={"item": "SITRUSBERRY"}),
    P("TREVENANT", 90, "HARVEST", "SITRUSBERRY", "IMPISH", "HORNLEECH,POLTERGEIST,WILLOWISP,LEECHSEED", "BPD", nick="Glasswood"),
])
X("QF - Sigrun (Resonance <= -3, or Isenmar won the war)", "LEADER_SIGRUN", "Sigrun", 92, 92,
  "You'll carry it better than I would have. Go.", relevel(drop_only(promote(warden_mons("Sigrun"))), [88, 89, 90, 90, 91, 92]))
X("QF - Odessa (warm draw)", "LEADER_ODESSA", "Odessa", 92, 92,
  "Tailwinds, flyer. All the way up.", relevel(drop_only(promote(warden_mons("Odessa"))), [88, 89, 90, 90, 91, 92]))
X("Final - Brann, stand-in (Valen collapsed)", "LEADER_BRANN", "Brann", 96, 96,
  "He asked me to. Last thing he asked. ...Forge on, then.", relevel(drop_only(promote(warden_mons("Brann"))), [92, 93, 94, 94, 95, 96]))
valen0 = [b for b in BOSSES if b[0] == "CHAMPION_VALEN"][0][4]
vlast = relevel(promote(valen0), [92, 93, 94, 94, 95, 96])
vlast[-1] = dict(vlast[-1], form=2, nick="Order", casual=dict(vlast[-1]["casual"], ab="POWERCONSTRUCT"))
X("Final (Ruin) - Valen, the Last Tuning: Zygarde Complete from bar 1", "CHAMPION_VALEN", "Valen", 1, 96,
  "Then unmake it, and be the last thing it remembers.", vlast)
X("QF - Celestine (\"the wrong key\")", "LEADER_CELESTINE", "Celestine", 92, 92,
  "Wrong key, right door. ...Go on.", relevel(drop_only(promote(warden_mons("Celestine"))), [88, 89, 90, 90, 91, 92]))
X("QF - Kaito (\"Marrowgate's still knocking\")", "LEADER_KAITO", "Kaito", 92, 92,
  "...It still remembers. So do I.", relevel(drop_only(promote(warden_mons("Kaito"))), [88, 89, 90, 90, 91, 92]))
X("QF - Ysolde (Kestrel fallen)", "LEADER_YSOLDE", "Ysolde", 92, 92,
  "Bring him back. Whatever it costs. Promise me.", relevel(drop_only(promote(warden_mons("Ysolde"))), [88, 89, 90, 90, 91, 92]))
X("QF (Ruin) - Archseer Imre Dask of the Veiled Synod; suggested field :INVERSE", "ARCHSEER_DASK", "Imre", 92, 92,
  "Behind, welcome. ...Welcome, behind.", [
    P("BRONZONG", 88, "LEVITATE", "LIGHTCLAY", "RELAXED", "TRICKROOM,REFLECT,LIGHTSCREEN,GYROBALL", "PD", tr=True),
    P("SABLEYE", 89, "PRANKSTER", "LEFTOVERS", "CAREFUL", "WILLOWISP,FOULPLAY,RECOVER,QUASH", "SD",
      hard={"item": "SABLENITE", "moves": "WILLOWISP,FOULPLAY,RECOVER,KNOCKOFF"}),
    P("ESPEON", 90, "MAGICBOUNCE", "LIFEORB", "TIMID", "PSYCHIC,SHADOWBALL,DAZZLINGGLEAM,CALMMIND", "S", casual={"item": "SITRUSBERRY"}),
    P("UMBREON", 90, "SYNCHRONIZE", "LEFTOVERS", "CALM", "FOULPLAY,WISH,YAWN,PROTECT", "SD"),
    P("GOTHITELLE", 91, "COMPETITIVE", "LEFTOVERS", "BOLD", "PSYCHIC,THUNDERBOLT,TRICKROOM,CALMMIND", "BPD"),
    P("MALAMAR", 92, "CONTRARY", "LEFTOVERS", "ADAMANT", "SUPERPOWER,KNOCKOFF,PSYCHOCUT,TOPSYTURVY", "BA", nick="Behind"),
])
X("Exhibition - Pageant Bout (2-vs-1 double with Rook v90): Dorian's half", "LEADER_DORIAN", "Dorian", 90, 90,
  "Encore! ENCORE!", [
    P("AMBIPOM", 88, "TECHNICIAN", "LIFEORB", "JOLLY", "FAKEOUT,DOUBLEHIT,KNOCKOFF,UTURN", "A", casual={"item": "SILKSCARF"}),
    P("EXPLOUD", 89, "SCRAPPY", "THROATSPRAY", "MODEST", "BOOMBURST,FIREBLAST,FOCUSBLAST,ICEBEAM", "S"),
    P("KECLEON", 90, "PROTEAN", "SITRUSBERRY", "ADAMANT", "FAKEOUT,SHADOWSNEAK,KNOCKOFF,DRAINPUNCH", "BA", nick="Encore",
      casual={"ab": "COLORCHANGE"}),
])
X("Exhibition - Pageant Bout (2-vs-1 double with Dorian v90): Rook's half", "LEADER_ROOK", "Rook", 90, 90,
  "Aaand that's a wrap! Clip it, Camera!", [
    P("TOXTRICITY", 88, "PUNKROCK", "THROATSPRAY", "MODEST", "OVERDRIVE,SLUDGEBOMB,BOOMBURST,VOLTSWITCH", "S"),
    P("ELECTIVIRE", 89, "MOTORDRIVE", "LIFEORB", "JOLLY", "WILDCHARGE,ICEPUNCH,CROSSCHOP,EARTHQUAKE", "A", casual={"item": "SITRUSBERRY"}),
    P("ROTOM", 90, "LEVITATE", "LEFTOVERS", "TIMID", "HYDROPUMP,THUNDERBOLT,WILLOWISP,VOLTSWITCH", "S", form=2, nick="Camera"),
])
X("Hijack - Dr. Percival Quent (Voss removed)", "MERIDIAN_QUENT", "Percival", 99, 100,
  "Hee... the numbers were so pretty. So pretty.", [
    P("BRONZONG", 96, "LEVITATE", "LEFTOVERS", "RELAXED", "TRICKROOM,GYROBALL,EARTHQUAKE,EXPLOSION", "PD", tr=True),
    P("METAGROSS", 97, "CLEARBODY", "ASSAULTVEST", "ADAMANT", "METEORMASH,ZENHEADBUTT,EARTHQUAKE,BULLETPUNCH", "HA"),
    P("JIRACHI", 97, "SERENEGRACE", "LEFTOVERS", "JOLLY", "IRONHEAD,ZENHEADBUTT,UTURN,FIREPUNCH", "A"),
    P("PORYGONZ", 98, "ADAPTABILITY", "CHOICESPECS", "TIMID", "TRIATTACK,DARKPULSE,ICEBEAM,THUNDERBOLT", "S", casual={"item": "SITRUSBERRY"}),
    P("MAGNEZONE", 99, "MAGNETPULL", "ASSAULTVEST", "MODEST", "THUNDERBOLT,FLASHCANNON,VOLTSWITCH,BODYPRESS", "BS"),
    P("SILVALLY", 100, "RKSSYSTEM", "STEELMEMORY", "JOLLY", "MULTIATTACK,PARTINGSHOT,FLAMECHARGE,SWORDSDANCE", "A",
      form=8, nick="NULL", casual={"moves": "MULTIATTACK,CRUSHCLAW,FLAMECHARGE,SCARYFACE"}),
])
X("Hijack (Ruin) - Theodric, the Gilded Reflection", "GILDED_THEODRIC", "Theodric", 0, 100,
  "Three hundred years and still the god will not kneel...", [
    P("GOLURK", 97, "NOGUARD", "LIFEORB", "ADAMANT", "DYNAMICPUNCH,EARTHQUAKE,POLTERGEIST,STONEEDGE", "HA", casual={"item": "SITRUSBERRY"}),
    P("AEGISLASH", 97, "STANCECHANGE", "WEAKNESSPOLICY", "QUIET", "KINGSSHIELD,SHADOWBALL,CLOSECOMBAT,SHADOWSNEAK", "BS"),
    P("KYOGRE", 98, "DRIZZLE", "CHOICESPECS", "MODEST", "WATERSPOUT,ORIGINPULSE,ICEBEAM,THUNDER", "S", casual={"item": "LEFTOVERS"}),
    P("GROUDON", 98, "DROUGHT", "LIFEORB", "ADAMANT", "PRECIPICEBLADES,STONEEDGE,FIREPUNCH,SWORDSDANCE", "A", casual={"item": "LEFTOVERS"}),
    P("REGIGIGAS", 99, "SLOWSTART", "LEFTOVERS", "ADAMANT", "CRUSHGRIP,KNOCKOFF,DRAINPUNCH,PROTECT", "HA"),
    P("GHOLDENGO", 100, "GOODASGOLD", "CHOICESPECS", "TIMID", "MAKEITRAIN,SHADOWBALL,FOCUSBLAST,TRICK", "S", nick="Gilt",
      casual={"item": "LEFTOVERS", "moves": "MAKEITRAIN,SHADOWBALL,FOCUSBLAST,NASTYPLOT"}),
])
X("Exhibition - Morwen's Echo (Night of Masques, Crownhaven Cathedral lantern)", "ECHO_MORWEN", "Morwen", 90, 90,
  "...Tell him I'm proud. Tell him I'm sorry. In that order.", [
    P("SPIRITOMB", 86, "INFILTRATOR", "LEFTOVERS", "CAREFUL", "FOULPLAY,SHADOWSNEAK,WILLOWISP,PAINSPLIT", "SD"),
    P("DUSKNOIR", 87, "FRISK", "LEFTOVERS", "IMPISH", "POLTERGEIST,SHADOWSNEAK,EARTHQUAKE,TRICKROOM", "BPD"),
    P("JELLICENT", 88, "CURSEDBODY", "LEFTOVERS", "BOLD", "SCALD,SHADOWBALL,WILLOWISP,RECOVER", "BPD"),
    P("HOUNDSTONE", 88, "SANDRUSH", "LIFEORB", "ADAMANT", "LASTRESPECTS,PLAYROUGH,BODYPRESS,WILLOWISP", "HA", casual={"item": "SITRUSBERRY"}),
    P("GENGAR", 89, "CURSEDBODY", "LIFEORB", "TIMID", "SHADOWBALL,SLUDGEBOMB,FOCUSBLAST,PERISHSONG", "S",
      casual={"item": "SITRUSBERRY", "moves": "SHADOWBALL,SLUDGEBOMB,FOCUSBLAST,WILLOWISP"}),
    P("CHANDELURE", 90, "FLASHFIRE", "CHOICESPECS", "TIMID", "SHADOWBALL,FIREBLAST,ENERGYBALL,TRICK", "S", nick="Lantern",
      casual={"item": "SPELLTAG", "moves": "SHADOWBALL,FLAMETHROWER,ENERGYBALL,CALMMIND"}),
])
# Ch21 tag foes (versions 21), aces 97
X("Ch21 tag foe - Sabine Kroll", "MERIDIAN_KROLL", "Sabine", 21, 97, "Nothing personal. It never is.", [
    P("OBSTAGOON", 95, "GUTS", "FLAMEORB", "ADAMANT", "OBSTRUCT,KNOCKOFF,FACADE,CLOSECOMBAT", "A", casual={"item": "SITRUSBERRY"}),
    P("CRAWDAUNT", 96, "ADAPTABILITY", "LIFEORB", "ADAMANT", "CRABHAMMER,KNOCKOFF,AQUAJET,SWORDSDANCE", "A", casual={"item": "SITRUSBERRY"}),
    P("KINGAMBIT", 97, "SUPREMEOVERLORD", "BLACKGLASSES", "ADAMANT", "KOWTOWCLEAVE,IRONHEAD,SUCKERPUNCH,SWORDSDANCE", "HA"),
])
X("Ch21 tag foe - Director Helene Marchetti", "MERIDIAN_MARCHETTI", "Helene", 21, 97, "Directorate, stand down. ...That's an order.", [
    P("MABOSSTIFF", 95, "INTIMIDATE", "SITRUSBERRY", "ADAMANT", "CRUNCH,PLAYROUGH,PSYCHICFANGS,WILDCHARGE", "BA"),
    P("ARCANINE", 96, "INTIMIDATE", "SITRUSBERRY", "ADAMANT", "FLAREBLITZ,EXTREMESPEED,WILDCHARGE,MORNINGSUN", "A"),
    P("CORVIKNIGHT", 97, "MIRRORARMOR", "LEFTOVERS", "IMPISH", "BRAVEBIRD,BODYPRESS,BULKUP,ROOST", "BPD"),
])
X("Ch21 tag foe - Dr. Percival Quent", "MERIDIAN_QUENT", "Percival", 21, 97, "Data! Glorious data! Do it again!", [
    P("BRONZONG", 95, "LEVITATE", "LEFTOVERS", "RELAXED", "TRICKROOM,GYROBALL,PSYCHIC,STEALTHROCK", "PD", tr=True),
    P("METAGROSS", 96, "CLEARBODY", "LIFEORB", "ADAMANT", "METEORMASH,ZENHEADBUTT,EARTHQUAKE,BULLETPUNCH", "HA", casual={"item": "SITRUSBERRY"}),
    P("PORYGONZ", 97, "ADAPTABILITY", "LIFEORB", "TIMID", "TRIATTACK,DARKPULSE,ICEBEAM,THUNDERBOLT", "S", casual={"item": "SITRUSBERRY"}),
])
X("Ch21 tag foe - Directorate Captain (when Marchetti is turned)", "MERIDIAN_DIRECTORATE", "Captain", 21, 97, "For the Concord.", [
    P("ALAKAZAM", 95, "MAGICGUARD", "LIFEORB", "TIMID", "PSYCHIC,FOCUSBLAST,SHADOWBALL,DAZZLINGGLEAM", "S", casual={"item": "SITRUSBERRY"}),
    P("SCIZOR", 96, "TECHNICIAN", "LIFEORB", "ADAMANT", "BULLETPUNCH,UTURN,KNOCKOFF,SWORDSDANCE", "HA", casual={"item": "METALCOAT"}),
    P("MAGNEZONE", 97, "MAGNETPULL", "CHOICESPECS", "MODEST", "THUNDERBOLT,FLASHCANNON,VOLTSWITCH,BODYPRESS", "BS", casual={"item": "SITRUSBERRY"}),
])
# Ruin Route Gyms 15-18 (version 1): harder (Hard sets on Standard) with different leads
X("Ruin Gym 15 - Magnus on :FACTORY -> :SCRAPYARD turn one", "LEADER_MAGNUS", "Magnus", 1, 71,
  "You came here to break it. So did I, once.", drop_only(promote(warden_mons("Magnus"), lead=3)))
X("Ruin Gym 16 - Nyx, illusion DOUBLE battle on :NEW_MOON with Inverse matchups", "LEADER_NYX", "Nyx", 1, 75,
  "Three hundred years of keeping secrets. Let's spend them.", drop_only(promote(warden_mons("Nyx"), lead=1)))
X("Ruin Gym 17 - Celestine on :FAIRY_TALE (refuses the badge)", "LEADER_CELESTINE", "Celestine", 1, 80,
  "Every tale has a verse of none. You found it.", drop_only(promote(warden_mons("Celestine"), lead=4)))
_sig = drop_only(promote(warden_mons("Sigrun"), lead=3))
_sig = [dict(m, nat=("JOLLY" if m["nat"] in ("ADAMANT", "IMPISH", "NAIVE") else "TIMID" if m["nat"] in ("MODEST", "QUIET") else m["nat"])) for m in _sig]
X("Ruin Gym 18 - Sigrun on :DRAGONS_DEN, every Pokemon a step faster", "LEADER_SIGRUN", "Sigrun", 1, 85,
  "Dragons don't let anything end quietly.", _sig)
X("Ruin R1 - the Reflection (fallback only; Core mirrors $player.party at battle start)", "REFLECTION", "???", 0, 85,
  "...", [
    P("DITTO", 85, "IMPOSTER", "CHOICESCARF", "JOLLY", "TRANSFORM", "HS"),
    P("DITTO", 85, "IMPOSTER", "FOCUSSASH", "JOLLY", "TRANSFORM", "HS"),
    P("DITTO", 85, "IMPOSTER", "LEFTOVERS", "JOLLY", "TRANSFORM", "HS"),
])

# ------------------------------------------------------------------------------
CAMEO_VERSIONS = (0, 9)   # Rev 4: Festival versions 1-3 retired; sidequest versions come from the new CAMEOS.md

def main():
    OUT.append("# Pokémon Prismfall - trainers (Essentials v21.1 format).\n"
               "# Generated from the Prismfall balance data. See design/BALANCE.md for the scheme:\n"
               "#   [TYPE,Name] = Standard (v), [TYPE,Name,v+100] = Hard, [TYPE,Name,v+200] = Casual.\n"
               "#   Rivals: v = battle*10 + starter_slot (0 Grass, 1 Fire, 2 Water); the Gen 1 starter line is\n"
               "#   swapped at battle start by Prismfall Core. IV/EV order: HP,Atk,Def,Spe,SpA,SpD.\n"
               "# Validate with: python3 -I tools/validate_trainers.py")
    section("WARDENS (Gyms 1-8, 10-18; Gym 9 = Juno J3 below)")
    for gym, tt, nm, cap, field, lose, mons in WARDENS:
        OUT.append("# Gym %d - %s - field :%s - cap %d" % (gym, nm, field, cap))
        OUT.extend(variants(tt, nm, 0, mons, lose, cap))
    section("RIVALS (version = battle*10 + slot; +100 Hard, +200 Casual)")
    for tt, nm, num, cap, lose, build in RIVALS:
        OUT.append("# %s%d" % (nm[0], num) + ("  (Gym 9 Warden battle, field :FLOWER_GARDEN)" if tt == "LEADER_JUNO" else ""))
        for slot in (0, 1, 2):
            mons = build(slot)
            for txt in variants(tt, nm, num * 10 + slot, mons, lose, cap):
                OUT.append(txt)
    section("ROUTE & GYM TRAINERS (stock trainer types; map ids from maps_out/trainers_needed.txt)")
    import importlib.util, os
    _sp = importlib.util.spec_from_file_location("routes", os.path.join(os.path.dirname(os.path.abspath(__file__)), "routes.py"))
    routes = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(routes)
    for note, tt, nm, lose, mons, cap in routes.ROUTES(P):
        OUT.append("# " + note)
        OUT.extend(variants(tt, nm, 0, mons, lose, cap, route=True))
    section("VILLAIN ADMINS")
    for note, tt, nm, cap, lose, mons in ADMINS:
        OUT.append("# " + note)
        OUT.extend(variants(tt, nm, 0, mons, lose, cap))
    section("FESTIVAL OF CHAMPIONS - final and hijack")
    for tt, nm, cap, lose, mons in BOSSES:
        OUT.extend(variants(tt, nm, 0, mons, lose, cap))
    section("FESTIVAL CHOICE-DRAW TEAMS AND FINALE/RUIN STORY EXTRAS (design/NARRATIVE_KEYS.md 7)")
    for note, tt, nm, v, cap, lose, mons, mega_std in EXTRA:
        OUT.append("# " + note)
        OUT.extend(variants(tt, nm, v, mons, lose, cap, mega_std=mega_std))
    if len(sys.argv) > 1:
        import importlib.util
        spec = importlib.util.spec_from_file_location("cameos", sys.argv[1])
        mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        section("FESTIVAL OF CHAMPIONS - invited cameo champions (see design/CAMEOS.md)")
        OUT.append("# Optional sidequest cameos (SPINE Rev 4). Version 1 = sidequest fight at its placement level, 2 = post-game\n"
                   "# rematch at 100; each +100 Hard / +200 Casual. Started with Prismfall.cameo_battle(:FESTIVAL_X, \"Name\", v).")
        for cm in mod.CAMEOS(P):
            for v, (ace, mode) in sorted(cm["versions"].items()):
                OUT.append("# %s (%s) v%d - ace %d%s" % (cm["nm"], cm["tt"], v, ace, (" (" + mode + ")") if mode else ""))
                src = cm["v1_mons"] if (v == 1 and cm.get("v1_mons")) else cm["mons"]
                if mode == "last4":
                    src = src[-4:]
                mons = [dict(m, lv=ace + (0 if mode == "flat" else m["lv"])) for m in src]
                OUT.extend(variants(cm["tt"], cm["nm"], v, mons, cm["lose"], ace, mega_std=cm["mega_std"]))
    print("\n".join(OUT))

main()
