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

def hard_ev(spread, level):
    """Hard's 252/252 spreads grow with the journey: at most 8 x level per stat (88 at Lv 11, 152 at 19, full from 32).
    Reference: Reborn and Rejuvenation give trainers min(85, 1.5 x level) by default; 252s everywhere is Reborn's
    Pulse-2 password, not its base game. Harness: flat 252s at Lv 11-15 beat even a prepared Gym 1 team 60/60."""
    top = min(252, 8 * level)
    return ",".join(str(min(int(v), top)) for v in spread.split(","))

def bag(top, diff, boss=False):
    if top <= 15:   t = (["POTION"], ["SUPERPOTION"], [])          # Gym 1 stretch: approachable (SPINE Rev 14)
    elif top <= 23: t = (["SUPERPOTION"], ["SUPERPOTION"] * 2, [])   # BALANCE 1: one Super Potion up to cap 23
    elif top <= 31: t = (["SUPERPOTION"] * 2, ["HYPERPOTION"] * 2, ["SUPERPOTION"])
    elif top <= 47: t = (["HYPERPOTION"] * 2, ["FULLRESTORE"] * 2, ["HYPERPOTION"])
    elif top <= 67: t = (["FULLRESTORE"] * 2, ["FULLRESTORE"] * 3, ["HYPERPOTION"])
    else:           t = (["FULLRESTORE"] * 2, ["FULLRESTORE"] * 3, ["FULLRESTORE"])
    return list(t[diff])

def render(ttype, name, version, mons, lose, diff, cap, size_note="", mega_std=False, route=False, nobag=False):
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
    items = [] if (route or nobag) else bag(top, diff)
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
            out.append("    EV = " + hard_ev(EV[o["ev"]], o["lv"]))
        else:
            out.append("    IV = %d" % casual_iv(top))
            out.append("    EV = 0")
    return "\n".join(out)

def variants(ttype, name, base, mons, lose, cap, mega_std=False, route=False, nobag=False):
    """Yields (version, text) for Standard / Hard / Casual."""
    std = [m for m in mons if m.get("only") not in ("hard",)]
    hard = [m for m in mons if m.get("only") in (None, "hard", "nocasual")]
    cas = [m for m in mons if m.get("only") is None]
    res = []
    res.append(render(ttype, name, base, std, lose, 0, cap, mega_std=mega_std, route=route, nobag=nobag))
    res.append(render(ttype, name, base + 100, hard, lose, 1, cap, mega_std=mega_std, route=route, nobag=nobag))
    res.append(render(ttype, name, base + 200, cas, lose, 2, cap, mega_std=mega_std, route=route, nobag=nobag))
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

# Field logic per team: design/TRAINER_FIELD_PLAYBOOK.md. Field data: plugins/Prismfall Field Effects/1xx_Field_*.rb.
# SPINE Revision 14: Gym 1 is Dorian (Saltmere, Normal, single), Gym 2 is Tamsin (Briarwick, Bug, double).
warden(1, "LEADER_DORIAN", "Dorian", 15, "GRAND_STAGE", "Bravo! Bravissimo! The audience is yours tonight!", [
    # Gym 1, a SINGLE battle and the player's first field. Reference calibration (BALANCE.md 1b): Reborn's Julia and
    # Rejuvenation's Venam bring SIX Pokemon to the first gym, two to five levels under the cap, with real natures, Oran
    # Berries, a Gem and field plays (Charge Beam on Electric Terrain, Fake Out / Rollout on the Concert Venue). Dorian's
    # troupe is built the same way: Std 5 / Hard 6 / Casual 3, cap-3 .. cap.
    # THE SHOW BUILDS. Grand Stage: Normal x1.3 (x1.5 from Encore up), damaging sound and dances x1.3 / x1.4 / x1.5,
    # Fake Out x1.5. Two showpieces, two dances or two damaging sound moves raise the applause a stage; any crit does too.
    # At Standing Ovation (stage 3) every attack gets +1 crit stage and SING NEVER MISSES - the play that punishes a
    # careless player who lets the crowd climb. Counterplay: KO the singers first, stall (Protect, Endure, Splash...)
    # to calm the crowd, Rock and Ghost types (Rolycoly, Sudowoodo, Sandygast) shrug off the Normal moves.
    # 1. The stagehand opens the show: Fake Out is a showpiece (x1.5 here) - one more and the crowd rises.
    P("AIPOM", 10, "PICKUP", "ORANBERRY", "JOLLY", "FAKEOUT,ASTONISH,SCRATCH,BATONPASS", "A",
      casual={"moves": "SCRATCH,ASTONISH,TAILWHIP,BATONPASS"},
      hard={"moves": "FAKEOUT,SWIFT,ASTONISH,TICKLE"}),
    # 2. The chorus: Echoed Voice and Round are damaging sound moves (x1.3 x1.3 STAB here); Echoed Voice doubles each
    #    turn it is repeated, so the echo and the applause climb together where the player can see it - switch, or KO
    #    the singer. Encore lasts two turns longer on this stage (it locks a player who set up); Baby-Doll Eyes also
    #    lowers Sp. Atk here.
    P("MINCCINO", 10, "CUTECHARM", "ORANBERRY", "MODEST", "ECHOEDVOICE,ROUND,ENCORE,BABYDOLLEYES", "S",
      casual={"moves": "ECHOEDVOICE,POUND,BABYDOLLEYES"},
      hard={"ab": "TECHNICIAN", "nat": "JOLLY", "moves": "TAILSLAP,ECHOEDVOICE,SING,ENCORE"}),
    # 3. The dancer: Teeter Dance is a dance (+1 Speed and a step toward the next stage) that confuses the target;
    #    Own Tempo keeps Spinda steady. Headbutt is a Normal move at x1.3 with a 30% flinch.
    P("SPINDA", 11, "OWNTEMPO", "ORANBERRY", "ADAMANT", "TEETERDANCE,TACKLE,COPYCAT", "A",
      only="nocasual", hard={"moves": "TEETERDANCE,HEADBUTT,PSYBEAM,COPYCAT", "item": "SITRUSBERRY"}),
    # Hard only: the understudy who shouts. Soundproof ignores the player's sound moves (and Dorian's own songs), and
    #    its Echoed Voice is the loudest thing in the house. Glass-jawed (Def 23 base): hit it hard and early.
    #    (Furfrou's Fur Coat + Headbutt and a Chatter Chatot both swept prepared teams at Lv 13-14 in the harness.)
    P("WHISMUR", 13, "SOUNDPROOF", "ORANBERRY", "MODEST", "ECHOEDVOICE,ASTONISH,POUND,HOWL", "S", only="hard"),
    # 4. The soprano: Sing is x1.3 accurate here and never misses at Standing Ovation; Round and Disarming Voice keep
    #    the applause rising. A bulky HP pool to stand in the spotlight. Casual leaves her at home.
    P("JIGGLYPUFF", 11, "CUTECHARM", "ORANBERRY", "MODEST", "SING,DISARMINGVOICE,POUND,DEFENSECURL", "BS",
      only="nocasual", hard={"ab": "COMPETITIVE", "item": "SITRUSBERRY", "moves": "SING,ROUND,DISARMINGVOICE,ECHOEDVOICE"}),
    # 5. The quick-change artist: Color Change is a costume change (it becomes the type of the move that hit it - hit
    #    it once with Fighting, then switch). It opens with its own Fake Out ("Costume change!"); Fury Swipes hits 2-5
    #    times and every critical hit is applause. Hard: Protean and the Synthetic Seed (Laser Focus: a sure crit).
    P("KECLEON", 15, "COLORCHANGE", "SITRUSBERRY", "HARDY", "FURYSWIPES,SHADOWSNEAK,FEINT,LICK", "BA",
      casual={"item": "ORANBERRY", "moves": "SCRATCH,LICK,TAILWHIP,BIND"},
      hard={"ab": "PROTEAN", "item": "SYNTHETICSEED", "nat": "ADAMANT", "moves": "FAKEOUT,FURYSWIPES,SHADOWSNEAK,KNOCKOFF"}),
])
warden(2, "LEADER_TAMSIN", "Tamsin", 19, "SILKWOOD", "Oh! You've unpicked every stitch. Well sewn, challenger.", [
    # Gym 2, a DOUBLE battle: "a thread holds because it's twisted with others". Std 4 / Hard 5 / Casual 3.
    # Silkwood: Electroweb x1.5, never misses, 30% paralysis; String Shot never misses (-3 Speed); Bug x1.5; Bug types
    # heal 1/16 a turn. In a double, Electroweb and String Shot hit BOTH foes, so the lead pair locks the player's
    # whole side down, and Struggle Bug (spread, x1.5) cuts both foes' Sp. Atk.
    # Lead pair - the twist: Surskit's Rain Dance wets the silk (every Electric move x1.2) for Joltik's Electroweb,
    # doubles Surskit's own Speed, halves Fire, and douses a Wildfire to Embers.
    # Standard is tuned down for an approachable Gym 2 (harness: realistic teams lost 25/30 to the sharper set):
    # neutral natures, Joltik at cap-5 without Protect (it outlasted every spread answer), the others at cap-4 / cap-3,
    # Absorb instead of Bug Bite, Water Gun instead of Bubble Beam,
    # Feint instead of Assurance (Assurance doubles after a partner's hit: Hard only).
    P("JOLTIK", 14, "COMPOUNDEYES", "ORANBERRY", "HARDY", "ELECTROWEB,ABSORB,STRINGSHOT,FURYCUTTER", "S",
      casual={"moves": "ELECTROWEB,FURYCUTTER,ABSORB,PROTECT"},
      hard={"item": "FOCUSSASH", "nat": "MODEST", "moves": "ELECTROWEB,STRUGGLEBUG,THUNDERWAVE,PROTECT"}),
    P("SURSKIT", 15, "SWIFTSWIM", "ORANBERRY", "HARDY", "RAINDANCE,WATERGUN,STRUGGLEBUG,QUICKATTACK", "S",
      hard={"item": "DAMPROCK", "nat": "TIMID", "moves": "RAINDANCE,BUBBLEBEAM,STRUGGLEBUG,QUICKATTACK"},
      casual={"moves": "WATERGUN,STRUGGLEBUG,QUICKATTACK,SWEETSCENT"}),
    # Hard: Rage Powder (powders x1.2 accurate here) pulls single-target hits off Bobbin.
    P("VIVILLON", 18, "COMPOUNDEYES", "SILVERPOWDER", "TIMID", "RAGEPOWDER,STRUGGLEBUG,GUST,STUNSPORE", "S",
      only="hard"),
    # The trap spider: Silk Trap guards it while its partner attacks, and binds tighter here (an extra Speed drop on
    # a contact move). Hard: Lunge, x1.3 here, which lowers Attack.
    P("SPIDOPS", 16, "INSOMNIA", "ORANBERRY", "HARDY", "SILKTRAP,STRUGGLEBUG,FEINT,STRINGSHOT", "BA",
      only="nocasual", hard={"ab": "STAKEOUT", "item": "SITRUSBERRY", "nat": "ADAMANT", "moves": "SILKTRAP,LUNGE,STRUGGLEBUG,ASSURANCE"}),
    # Telluric Seed: +1 Def, +1 Sp. Def, -1 Speed - a silk cocoon. Razor Leaf hits both foes (Grass x1.2, Overgrow on).
    P("SWADLOON", 19, "OVERCOAT", "TELLURICSEED", "HARDY", "RAZORLEAF,BUGBITE,STRUGGLEBUG,PROTECT", "BA",
      nick="Bobbin", casual={"ab": "LEAFGUARD", "item": "ORANBERRY", "moves": "RAZORLEAF,BUGBITE,STRINGSHOT,PROTECT"},
      hard={"item": "EVIOLITE"}),
])
warden(3, "LEADER_MARISOL", "Marisol", 23, "WATER_SURFACE", "Ha! Tide's turned. Take the badge before I change my mind.", [
    # Water Surface already switches Swift Swim on and gives Water x1.5, so Standard and Casual drop Drizzle (rain on top
    # of the field made Water Pulse a one-hit KO at Gym 3). Hard keeps Drizzle + Damp Rock: rain lasts 8+3 turns here.
    # Standard is tuned down for an approachable Gym 3 (harness: realistic teams lost 29/30): neutral natures, the
    # openers two levels under the cap, Water Gun on Pelipper. Water x1.5 on the field still makes every hit count.
    P("PELIPPER", 20, "KEENEYE", "ORANBERRY", "HARDY", "WATERGUN,WINGATTACK,SUPERSONIC,PROTECT", "BS",
      hard={"ab": "DRIZZLE", "item": "DAMPROCK", "nat": "MODEST", "moves": "WATERPULSE,AIRSLASH,ROOST,TAILWIND"}),
    # Volt Absorb punishes the Electric answer; its own Spark is x1.5 against grounded targets. Elemental Seed: +1 Speed, Aqua Ring.
    # Standard: the lantern-fish is still a Chinchou (Lanturn walled realistic teams: 64 knockouts in 30 runs).
    # Volt Absorb still punishes the Electric answer, and its Spark is x1.5 against grounded targets. Hard: Lanturn
    # with the Elemental Seed (+1 Speed, Aqua Ring).
    P("CHINCHOU", 21, "VOLTABSORB", "ORANBERRY", "HARDY", "WATERGUN,SPARK,CONFUSERAY,SUPERSONIC", "BS",
      only="nocasual", hard={"sp": "LANTURN", "item": "ELEMENTALSEED", "nat": "MODEST",
                             "moves": "BUBBLEBEAM,SPARK,ELECTROBALL,THUNDERWAVE"}),
    P("ARAQUANID", 22, "WATERBUBBLE", "SITRUSBERRY", "ADAMANT", "BUBBLEBEAM,BUGBITE,BITE,AQUARING", "BA",
      only="hard", hard={"moves": "LIQUIDATION,LEECHLIFE,CRUNCH,AQUARING"}),
    P("FLOATZEL", 21, "SWIFTSWIM", "ORANBERRY", "HARDY", "WATERPULSE,BITE,QUICKATTACK,SWIFT", "A",
      hard={"moves": "AQUAJET,WATERPULSE,CRUNCH,ICEFANG", "nat": "NAIVE"}),
    # Transition play: Dive drags the fight Underwater (x1.3 strike), "a current that changes direction mid-fight".
    # Standard Lucky (harness: the ace swept 25 of 30 realistic teams after they beat the other three): Hardy, Brine
    # (special, Gyarados's weak side) instead of Waterfall, and the Dive play kept. Hard: Adamant Waterfall + Dragon Dance.
    P("GYARADOS", 23, "INTIMIDATE", "SITRUSBERRY", "HARDY", "BRINE,BITE,ICEFANG,DIVE", "A",
      nick="Lucky", casual={"moves": "BITE,TWISTER,BRINE,LEER"},
      hard={"nat": "ADAMANT", "moves": "WATERFALL,DIVE,ICEFANG,DRAGONDANCE"}),
])
warden(4, "LEADER_ROOK", "Rook", 27, "NEON_GRID", "Cut! ...Okay, okay, that's going in the highlight reel. You earned it.", [
    # Charge reboots a blacked-out grid (2 charging moves); Bite is his hedge for the Blackout (Dark x1.3).
    P("LUXIO", 25, "INTIMIDATE", "MAGNET", "ADAMANT", "SPARK,BITE,CHARGE,ROAR", "A",
      hard={"moves": "WILDCHARGE,CRUNCH,ICEFANG,VOLTSWITCH", "item": "SITRUSBERRY"}),
    # Synthetic Seed on Neon Grid: +1 Sp. Atk and Magnet Rise - the answer to the Ground types the Gym Guide recommends.
    P("ELECTABUZZ", 25, "STATIC", "SYNTHETICSEED", "NAIVE", "SHOCKWAVE,LOWSWEEP,QUICKATTACK,CHARGE", "MX",
      only="nocasual", hard={"moves": "THUNDERPUNCH,BRICKBREAK,ICEPUNCH,QUICKATTACK", "nat": "JOLLY", "ev": "A"}),
    P("HELIOLISK", 26, "DRYSKIN", "SITRUSBERRY", "TIMID", "PARABOLICCHARGE,GRASSKNOT,QUICKATTACK,THUNDERWAVE", "S",
      only="hard"),
    # Eerie Impulse drops Sp. Atk 3 stages on this field.
    P("TOXTRICITY", 26, "PUNKROCK", "ORANBERRY", "MODEST", "SHOCKWAVE,VENOSHOCK,EERIEIMPULSE,CHARGE", "S",
      hard={"moves": "OVERDRIVE,VENOSHOCK,HYPERVOICE,VOLTSWITCH", "item": "THROATSPRAY"},
      casual={"moves": "SPARK,VENOSHOCK,NOBLEROAR,ACIDSPRAY"}),
    # Levitate dodges the quakes; Hydro Pump answers Ground types and carries the grid's 30% paralysis for Hex.
    P("ROTOM", 27, "LEVITATE", "SITRUSBERRY", "MODEST", "SHOCKWAVE,HEX,HYDROPUMP,THUNDERWAVE", "S", form=2,
      nick="Camera", casual={"moves": "SHOCKWAVE,HEX,THUNDERWAVE,CONFUSERAY"}, hard={"moves": "HYDROPUMP,THUNDERBOLT,HEX,WILLOWISP", "nat": "TIMID"}),
])
warden(5, "LEADER_SAHAR", "Sahar", 31, "DESERT", "The sand remembers everything. It will remember you, too.", [
    # Sandstorm lasts 8+3 turns here and bakes a Superbloom back to dunes. Sand Tomb x2.
    P("HIPPOPOTAS", 29, "SANDSTREAM", "SMOOTHROCK", "IMPISH", "SANDTOMB,BITE,YAWN,STEALTHROCK", "PD",
      hard={"moves": "HIGHHORSEPOWER,CRUNCH,YAWN,STEALTHROCK"}),
    P("DUGTRIO", 29, "ARENATRAP", "FOCUSSASH", "JOLLY", "DIG,SUCKERPUNCH,NIGHTSLASH,SANDTOMB", "A", only="hard",
      hard={"moves": "HIGHHORSEPOWER,SUCKERPUNCH,ROCKSLIDE,MEMENTO"}),
    # Sand Spit: hit it with the Water move that was meant to start the Superbloom and the sandstorm comes straight back.
    P("SANDACONDA", 30, "SANDSPIT", "TELLURICSEED", "IMPISH", "BULLDOZE,BRUTALSWING,GLARE,ROCKTOMB", "BPD",
      only="nocasual", hard={"moves": "HIGHHORSEPOWER,STONEEDGE,GLARE,COIL"}),
    # Fire Fang answers Grass and two Fire attacks bake the Superbloom back (stage play). Dig x1.5, Sand Tomb x2.
    P("KROKOROK", 30, "MOXIE", "EVIOLITE", "JOLLY", "CRUNCH,DIG,SANDTOMB,FIREFANG", "A",
      hard={"moves": "CRUNCH,STOMPINGTANTRUM,ROCKSLIDE,FIREFANG"},
      casual={"ab": "INTIMIDATE", "moves": "CRUNCH,DIG,SANDTOMB,SWAGGER"}),
    P("CLAYDOL", 31, "LEVITATE", "SOFTSAND", "MODEST", "EARTHPOWER,EXTRASENSORY,ANCIENTPOWER,RAPIDSPIN", "BS",
      nick="Effigy", hard={"moves": "SCORCHINGSANDS,PSYCHIC,ICEBEAM,STEALTHROCK", "item": "SITRUSBERRY"}),
])
warden(6, "LEADER_CORVIN", "Corvin", 35, "CORROSIVE_MIRE", "Hmph. Clean work. The mire doesn't give that compliment often.", [
    # DOUBLE battle (story; Prismfall.gym_battle sets it). Lead pair: Weezing spreads, Amoonguss draws the fire.
    # Never Misty Surge (it would purify the field). Transition play: Heat Wave hits both foes, ignites the marsh gas
    # (1/8 to each grounded non-Fire foe per use) and the second one burns it off to Wasteland, where quakes are halved.
    P("WEEZING", 33, "LEVITATE", "BLACKSLUDGE", "BOLD", "STRANGESTEAM,SLUDGE,HEATWAVE,PROTECT", "PD", form=1,
      casual={"moves": "STRANGESTEAM,SLUDGE,WILLOWISP,PROTECT"},
      hard={"ab": "NEUTRALIZINGGAS", "moves": "STRANGESTEAM,SLUDGEBOMB,HEATWAVE,PROTECT"}),
    # Powders are x1.25 accurate here. On Hard the doctor redirects: Rage Powder pulls single-target moves off Weezing and Ward
    # (Amoonguss only learns it at 40, so Standard gets Protect instead).
    P("AMOONGUSS", 34, "EFFECTSPORE", "BLACKSLUDGE", "RELAXED", "GIGADRAIN,VENOSHOCK,STUNSPORE,PROTECT", "PD",
      casual={"moves": "GIGADRAIN,VENOSHOCK,STUNSPORE,CLEARSMOG"},
      hard={"ab": "REGENERATOR", "moves": "GIGADRAIN,SLUDGEBOMB,RAGEPOWDER,SPORE"}),
    # Synthetic Seed on the Mire: +1 Atk, +1 Sp. Atk, holder poisoned - and a Poison type can't be poisoned. Tailwind for the pair.
    P("CROBAT", 33, "INNERFOCUS", "SYNTHETICSEED", "JOLLY", "CROSSPOISON,WINGATTACK,BITE,TAILWIND", "A",
      only="nocasual", hard={"moves": "CROSSPOISON,ACROBATICS,TAILWIND,TAUNT"}),
    P("SALAZZLE", 34, "CORROSION", "BLACKSLUDGE", "TIMID", "FAKEOUT,VENOSHOCK,HEATWAVE,PROTECT", "S",
      only="hard", gender="female"),
    P("DRAPION", 34, "SNIPER", "SCOPELENS", "ADAMANT", "POISONFANG,KNOCKOFF,FELLSTINGER,PROTECT", "A",
      hard={"moves": "POISONJAB,KNOCKOFF,EARTHQUAKE,PROTECT", "item": "LIFEORB"}),
    # Merciless: +1 Attack on entry here, and the mire keeps poisoning grounded foes. Baneful Bunker is his Protect;
    # Scald answers the Fire flip.
    P("TOXAPEX", 35, "MERCILESS", "BLACKSLUDGE", "BOLD", "VENOSHOCK,SCALD,BANEFULBUNKER,RECOVER", "BPD",
      nick="Ward", casual={"ab": "LIMBER", "moves": "VENOSHOCK,TOXIC,SCALD,RECOVER"},
      hard={"item": "ROCKYHELMET", "moves": "VENOSHOCK,SCALD,BANEFULBUNKER,WIDEGUARD"}),
])
warden(7, "LEADER_BRANN", "Brann", 39, "VOLCANIC", "Ha! Tempered steel! That's what you are, aye!", [
    # No Stealth Rock on this team any more: his own eruptions blow hazards away. Lava Plume and Earth Power prime eruptions
    # (+1 to his Fire types, lava on grounded foes) and three Lava Plumes re-melt Cinderglass back to Volcanic.
    P("TORKOAL", 37, "DROUGHT", "SITRUSBERRY", "BOLD", "LAVAPLUME,EARTHPOWER,WILLOWISP,CLEARSMOG", "PD",
      casual={"moves": "LAVAPLUME,BODYSLAM,WILLOWISP,PROTECT"},
      hard={"item": "HEATROCK", "moves": "LAVAPLUME,SOLARBEAM,EARTHPOWER,WILLOWISP", "nat": "MODEST", "ev": "BS"}),
    # Magma Armor: +1 Def on entry, 1/16 a turn, +1 Def/Sp. Def per eruption. Elemental Seed: +1 Atk/Sp. Atk/Speed, and Fire types can't be burned.
    P("CAMERUPT", 37, "MAGMAARMOR", "ELEMENTALSEED", "QUIET", "LAVAPLUME,EARTHPOWER,ROCKSLIDE,AMNESIA", "BS",
      only="nocasual", hard={"moves": "ERUPTION,EARTHPOWER,ANCIENTPOWER,LAVAPLUME"}),
    P("CENTISKORCH", 38, "FLASHFIRE", "CHARCOAL", "ADAMANT", "FIRELASH,LUNGE,CRUNCH,COIL", "A", only="hard"),
    P("MAGMORTAR", 38, "FLAMEBODY", "CHARCOAL", "MODEST", "FLAMETHROWER,THUNDERBOLT,CLEARSMOG,CONFUSERAY", "S",
      hard={"moves": "FLAMETHROWER,THUNDERBOLT,FOCUSBLAST,SOLARBEAM", "item": "ELEMENTALSEED"}),
    P("ARCANINE", 38, "INTIMIDATE", "SITRUSBERRY", "ADAMANT", "FLAREBLITZ,CRUNCH,EXTREMESPEED,ROAR", "A",
      casual={"moves": "FIREFANG,CRUNCH,EXTREMESPEED,ROAR"},
      hard={"ab": "FLASHFIRE", "moves": "FLAREBLITZ,WILDCHARGE,EXTREMESPEED,MORNINGSUN"}),
    # Answer to the quench: on Cinderglass Steam Engine gains Speed every turn and obsidian sharpens Rock Slide (x1.3).
    P("COALOSSAL", 39, "STEAMENGINE", "SITRUSBERRY", "BRAVE", "TARSHOT,HEATCRASH,SMACKDOWN,ROCKSLIDE", "HA",
      nick="Anvil", hard={"moves": "TARSHOT,FLAMETHROWER,STONEEDGE,HEATCRASH", "item": "WEAKNESSPOLICY", "nat": "QUIET"},
      casual={"ab": "FLAMEBODY"}),
])
warden(8, "LEADER_KAITO", "Kaito", 43, "COLOSSEUM", "...Good. Your Pokémon fight like they remember why.", [
    # Synthetic Seed on the Colosseum: +1 Attack and Focus Energy, Taunted. The seed is eaten, so Unburden doubles Speed
    # and Acrobatics is at full power; the Taunt costs an all-out attacker nothing.
    P("HAWLUCHA", 41, "UNBURDEN", "SYNTHETICSEED", "JOLLY", "BRICKBREAK,ACROBATICS,THUNDERPUNCH,UTURN", "A",
      casual={"item": "SITRUSBERRY", "moves": "BRICKBREAK,ACROBATICS,SWORDSDANCE,ROOST"},
      hard={"moves": "HIGHJUMPKICK,ACROBATICS,THUNDERPUNCH,UTURN"}),
    P("MEDICHAM", 41, "PUREPOWER", "CHOICEBAND", "JOLLY", "HIGHJUMPKICK,ZENHEADBUTT,BULLETPUNCH,ICEPUNCH", "A",
      only="hard"),
    # No Guard: +1 Attack on entry here.
    P("MACHAMP", 42, "NOGUARD", "SITRUSBERRY", "ADAMANT", "DYNAMICPUNCH,KNOCKOFF,ROCKSLIDE,BULLETPUNCH", "HA",
      casual={"ab": "GUTS"}, hard={"moves": "DYNAMICPUNCH,KNOCKOFF,STONEEDGE,BULLETPUNCH"}),
    P("HITMONTOP", 42, "INTIMIDATE", "ASSAULTVEST", "ADAMANT", "FAKEOUT,TRIPLEKICK,RAPIDSPIN,SUCKERPUNCH", "BA",
      only="nocasual", hard={"moves": "FAKEOUT,CLOSECOMBAT,RAPIDSPIN,SUCKERPUNCH"}),
    P("CONKELDURR", 42, "GUTS", "FLAMEORB", "ADAMANT", "HAMMERARM,MACHPUNCH,ROCKSLIDE,BULKUP", "HA",
      casual={"item": "SITRUSBERRY"}, hard={"moves": "DRAINPUNCH,MACHPUNCH,KNOCKOFF,ICEPUNCH"}),
    # Inner Focus: +1 crit stage here; Scope Lens makes it 50%, a Frenzy makes it certain.
    P("LUCARIO", 43, "INNERFOCUS", "SCOPELENS", "MODEST", "AURASPHERE,FLASHCANNON,DARKPULSE,NASTYPLOT", "S",
      nick="Memory", casual={"item": "SITRUSBERRY"},
      hard={"item": "LUCARIONITE", "ab": "JUSTIFIED", "nat": "JOLLY", "ev": "A",
            "moves": "SWORDSDANCE,CLOSECOMBAT,METEORMASH,EXTREMESPEED"}),
])
# Gym 9 = J3 is generated with the rivals (rival versioning).
warden(10, "LEADER_ANJA", "Anja", 51, "FROZEN_LAKE", "The ice held for you. It doesn't hold for many.", [
    # Freeze-Dry answers Water types; Blizzard / Freeze-Dry also refreeze a melted lake (3 big Ice moves on Water Surface).
    P("NINETALES", 49, "SNOWWARNING", "LIGHTCLAY", "TIMID", "AURORAVEIL,BLIZZARD,MOONBLAST,FREEZEDRY", "S", form=1,
      casual={"moves": "AURORAVEIL,ICEBEAM,DAZZLINGGLEAM,ICYWIND", "item": "SITRUSBERRY"}),
    # Rock Blast would freeze into an Ice move here, so Razor Shell is the Fire answer; it is x1.5 once the lake is open water.
    P("CLOYSTER", 49, "SKILLLINK", "WHITEHERB", "ADAMANT", "SHELLSMASH,ICICLESPEAR,RAZORSHELL,ICESHARD", "A",
      casual={"moves": "ICICLESPEAR,RAZORSHELL,ICESHARD,PROTECT", "item": "SITRUSBERRY"},
      hard={"item": "FOCUSSASH"}),
    P("BEARTIC", 50, "SLUSHRUSH", "NEVERMELTICE", "ADAMANT", "ICICLECRASH,SUPERPOWER,AQUAJET,SWORDSDANCE", "A",
      only="nocasual"),
    P("WALREIN", 50, "THICKFAT", "SITRUSBERRY", "MODEST", "BLIZZARD,SURF,ENCORE,PROTECT", "BS",
      hard={"ab": "ICEBODY", "item": "LEFTOVERS", "moves": "BLIZZARD,SURF,SUPERFANG,PROTECT"}),
    # Transition play: Body Press is a "heavy blow" - three crack the lake to Water Surface (x1.3 strike), which halves
    # the challenger's Fire moves and feeds Walrein and Cloyster. Rapid Spin skates (x1.5).
    P("AVALUGG", 50, "STURDY", "ROCKYHELMET", "IMPISH", "AVALANCHE,BODYPRESS,RAPIDSPIN,RECOVER", "BPD",
      casual={"moves": "AVALANCHE,BODYPRESS,IRONDEFENSE,RECOVER"}),
    # High Horsepower instead of Earthquake: it cracks the ice without laying Spikes on her own side, and it still works on
    # open water where quakes fail. Elemental Seed: +2 Speed for 1/8 HP. Ice Shard refreezes one crack and slides (+1 Speed).
    P("MAMOSWINE", 51, "THICKFAT", "ELEMENTALSEED", "ADAMANT", "HIGHHORSEPOWER,ICICLECRASH,ICESHARD,KNOCKOFF", "A",
      nick="Matriarch", casual={"item": "NEVERMELTICE"},
      hard={"item": "LIFEORB", "moves": "HIGHHORSEPOWER,ICICLECRASH,ICESHARD,STEALTHROCK"}),
])
warden(11, "LEADER_ODESSA", "Odessa", 55, "STORMFRONT", "Clear skies to you, flyer. You've earned the jetstream.", [
    # DOUBLE battle (story). No Drizzle: in rain the Stormfront's lightning strikes every airborne non-Electric Pokemon,
    # which is her team. Hurricane and Thunder never miss here anyway.
    # Lead pair: Pelipper's Tailwind lasts 6 turns here and its Wide Guard stops the Rock Slides and Discharges that a
    # team of fliers fears; Noivern's Hyper Voice hits both foes.
    P("PELIPPER", 53, "KEENEYE", "SITRUSBERRY", "MODEST", "TAILWIND,WIDEGUARD,HURRICANE,SCALD", "BS",
      casual={"moves": "TAILWIND,HURRICANE,SCALD,UTURN"}),
    # Transition play: two Sunny Days tear the storm open -> Rainbow (added effects doubled: Air Slash flinches 60%,
    # Hurricane confuses 60%; Normal x1.5 for Hyper Voice / Boomburst).
    P("NOIVERN", 54, "INFILTRATOR", "LIFEORB", "TIMID", "HURRICANE,HYPERVOICE,AIRSLASH,SUNNYDAY", "S",
      casual={"item": "SITRUSBERRY", "moves": "HURRICANE,HYPERVOICE,DRAGONPULSE,FLAMETHROWER"},
      hard={"moves": "HURRICANE,BOOMBURST,DRACOMETEOR,SUNNYDAY"}),
    # Big Pecks: +1 Defense on entry here. Icy Wind is a wind move (x1.2) that slows both foes.
    P("SWANNA", 53, "BIGPECKS", "LEFTOVERS", "TIMID", "HURRICANE,SCALD,ICYWIND,ROOST", "S", only="nocasual",
      hard={"moves": "HURRICANE,SCALD,ICYWIND,PROTECT"}),
    # Elemental Seed on the Stormfront: +1 Speed and Charge - the first Electric Revelation Dance is doubled.
    P("ORICORIO", 54, "DANCER", "ELEMENTALSEED", "TIMID", "REVELATIONDANCE,HURRICANE,HELPINGHAND,ROOST", "S", form=1,
      casual={"item": "SITRUSBERRY"}),
    # The answer to Electric: Wind Power arrives charged on this field, and Electric is x1.3. Replaces Talonflame.
    P("KILOWATTREL", 54, "WINDPOWER", "SHARPBEAK", "TIMID", "THUNDERBOLT,HURRICANE,VOLTSWITCH,PROTECT", "S",
      casual={"ab": "VOLTABSORB", "moves": "THUNDERBOLT,HURRICANE,VOLTSWITCH,ROOST"},
      hard={"moves": "THUNDER,HURRICANE,VOLTSWITCH,PROTECT", "item": "MAGNET"}),
    P("CORVIKNIGHT", 55, "MIRRORARMOR", "LEFTOVERS", "IMPISH", "BRAVEBIRD,IRONHEAD,BULKUP,ROOST", "BPD",
      nick="Taxi", hard={"moves": "BRAVEBIRD,BODYPRESS,BULKUP,ROOST"}),
])
warden(12, "LEADER_ILSA", "Ilsa", 59, "MINDSCAPE", "...Quiet, for once. Your thoughts were very loud. I liked them.", [
    # Trick Room lasts 2 turns longer in the Mindscape (3 on the Inverse Field). Extrasensory x1.3.
    P("BRONZONG", 57, "LEVITATE", "MENTALHERB", "RELAXED", "TRICKROOM,GYROBALL,EXTRASENSORY,STEALTHROCK", "PD", tr=True,
      hard={"moves": "TRICKROOM,GYROBALL,PSYCHIC,EXPLOSION"}),
    # Forewarn: +1 Sp. Def on entry. Calm Mind is also a soothing move: two of them calm a Nightmare back into a Dream.
    P("MUSHARNA", 57, "FOREWARN", "SITRUSBERRY", "QUIET", "PSYCHIC,MOONBLAST,YAWN,CALMMIND", "BS", tr=True,
      only="nocasual", hard={"moves": "PSYCHIC,MOONBLAST,HYPNOSIS,DREAMEATER", "item": "LEFTOVERS"}),
    P("ESPEON", 58, "MAGICBOUNCE", "LIFEORB", "TIMID", "PSYCHIC,SHADOWBALL,DAZZLINGGLEAM,CALMMIND", "S",
      casual={"ab": "SYNCHRONIZE", "item": "SITRUSBERRY"}),
    P("GOTHITELLE", 58, "COMPETITIVE", "LEFTOVERS", "QUIET", "PSYCHIC,THUNDERBOLT,TRICKROOM,CALMMIND", "BS", tr=True,
      hard={"ab": "SHADOWTAG", "moves": "PSYCHIC,THUNDERBOLT,TRICKROOM,TAUNT"}),
    P("REUNICLUS", 58, "MAGICGUARD", "LIFEORB", "QUIET", "PSYCHIC,FOCUSBLAST,SHADOWBALL,RECOVER", "BS", tr=True,
      casual={"item": "SITRUSBERRY"}),
    # Transition play: Psychic Noise is a damaging sound move - the third one cracks the dream into the Inverse Field
    # (x1.3 strike), where the Dark, Ghost and Bug answers are resisted and Psychic hits Dark types for double.
    P("HATTERENE", 59, "MAGICBOUNCE", "SITRUSBERRY", "QUIET", "PSYCHICNOISE,DAZZLINGGLEAM,MYSTICALFIRE,TRICKROOM", "BS",
      tr=True, nick="Hush", casual={"moves": "PSYCHIC,DAZZLINGGLEAM,MYSTICALFIRE,TRICKROOM"},
      hard={"item": "LIFEORB", "moves": "PSYCHICNOISE,DAZZLINGGLEAM,MYSTICALFIRE,CALMMIND"}),
])
warden(13, "LEADER_BASTIAN", "Bastian", 63, "CRYSTAL_CAVERN", "Flawless cut. I'd set you in a crown if I had one left.", [
    # Light moves x1.5 here (Power Gem, Dazzling Gleam); two of them also relight a darkened cavern. Screens last 2 turns longer.
    P("CARBINK", 61, "STURDY", "LIGHTCLAY", "BOLD", "STEALTHROCK,POWERGEM,DAZZLINGGLEAM,REFLECT", "PD",
      hard={"moves": "STEALTHROCK,POWERGEM,DAZZLINGGLEAM,LIGHTSCREEN"}),
    # Transition play: a miner's blast. Explosion (Galvanized, x1.3 strike) shatters the crystals -> Cave, where Rock is x1.5,
    # Stealth Rock cuts twice as deep and Aurorus's Hyper Voice echoes (x1.5).
    P("GOLEM", 61, "GALVANIZE", "SITRUSBERRY", "ADAMANT", "DOUBLEEDGE,STONEEDGE,EARTHQUAKE,EXPLOSION", "BA", form=1,
      only="nocasual"),
    P("AURORUS", 62, "REFRIGERATE", "SITRUSBERRY", "MODEST", "HYPERVOICE,ANCIENTPOWER,EARTHPOWER,FLASHCANNON", "BS",
      casual={"moves": "HYPERVOICE,ANCIENTPOWER,EARTHPOWER,THUNDERWAVE"},
      hard={"item": "CHOICESPECS"}),
    P("LYCANROC", 62, "TOUGHCLAWS", "LIFEORB", "JOLLY", "ACCELEROCK,STONEEDGE,CRUNCH,SWORDSDANCE", "A", form=2,
      casual={"item": "SITRUSBERRY"}, hard={"moves": "ACCELEROCK,STONEEDGE,CLOSECOMBAT,SWORDSDANCE"}),
    P("RHYPERIOR", 62, "SOLIDROCK", "ASSAULTVEST", "ADAMANT", "STONEEDGE,EARTHQUAKE,MEGAHORN,ICEPUNCH", "HA"),
    # Sand Stream is gone: a sandstorm blots out his own crystals (-> Dark Crystal). Magical Seed: +1 Sp. Atk and a Light
    # Screen (7 turns here) against the Water and Grass specials; Power Gem is a light move.
    P("GIGALITH", 63, "STURDY", "MAGICALSEED", "BRAVE", "STONEEDGE,EARTHQUAKE,BODYPRESS,POWERGEM", "HA",
      nick="Geode", casual={"item": "SITRUSBERRY", "moves": "STONEEDGE,EARTHQUAKE,HEAVYSLAM,ROCKPOLISH"},
      hard={"item": "WEAKNESSPOLICY", "moves": "STONEEDGE,EARTHQUAKE,BODYPRESS,METEORBEAM"}),
])
warden(14, "LEADER_YSOLDE", "Ysolde", 67, "HOLLOW_CATHEDRAL", "The candles are still lit. ...Morwen would have liked you.", [
    # Will-O-Wisp never misses here.
    P("SABLEYE", 65, "PRANKSTER", "LEFTOVERS", "CAREFUL", "WILLOWISP,FOULPLAY,RECOVER,SHADOWSNEAK", "SD",
      hard={"moves": "WILLOWISP,FOULPLAY,RECOVER,TAUNT"}),
    # Answer to a consecration (3 holy moves, e.g. Dazzling Gleam): two Ghost rites by a Ghost type bring the spirits back.
    # Curse here, Destiny Bond on Gengar.
    P("SPIRITOMB", 65, "INFILTRATOR", "SITRUSBERRY", "ADAMANT", "SUCKERPUNCH,SHADOWSNEAK,WILLOWISP,CURSE", "HA",
      only="nocasual", hard={"moves": "SUCKERPUNCH,POLTERGEIST,WILLOWISP,CURSE"}),
    P("DUSKNOIR", 66, "PRESSURE", "LEFTOVERS", "IMPISH", "SHADOWSNEAK,POLTERGEIST,BRICKBREAK,PAINSPLIT", "BPD",
      hard={"moves": "SHADOWSNEAK,POLTERGEIST,BRICKBREAK,WILLOWISP"}),
    # Mummy: +1 Sp. Def on entry; Magical Seed: +1 Sp. Def more. Body Press answers the Dark types.
    P("COFAGRIGUS", 66, "MUMMY", "MAGICALSEED", "BOLD", "SHADOWBALL,WILLOWISP,BODYPRESS,PAINSPLIT", "PD",
      casual={"item": "SITRUSBERRY", "moves": "SHADOWBALL,WILLOWISP,TOXICSPIKES,PAINSPLIT"},
      hard={"moves": "SHADOWBALL,BODYPRESS,IRONDEFENSE,PAINSPLIT"}),
    P("GENGAR", 66, "CURSEDBODY", "LIFEORB", "TIMID", "SHADOWBALL,SLUDGEBOMB,FOCUSBLAST,DESTINYBOND", "S",
      casual={"item": "SITRUSBERRY", "moves": "SHADOWBALL,SLUDGEBOMB,FOCUSBLAST,WILLOWISP"},
      hard={"item": "GENGARITE", "moves": "SHADOWBALL,SLUDGEBOMB,FOCUSBLAST,PERISHSONG"}),
    # Ghostfire: Fire moves also hit as Ghost; Mystical Fire x1.3.
    P("CHANDELURE", 67, "FLASHFIRE", "SPELLTAG", "MODEST", "SHADOWBALL,MYSTICALFIRE,ENERGYBALL,CALMMIND", "S",
      nick="Vigil", hard={"item": "CHOICESPECS", "ab": "INFILTRATOR", "nat": "TIMID",
                          "moves": "SHADOWBALL,FIREBLAST,ENERGYBALL,TRICK"}),
])
warden(15, "LEADER_MAGNUS", "Magnus", 71, "FACTORY", "Efficient. Unexpected. I'll have to redesign around you.", [
    # Nobody on this team uses a quake or an explosion any more: three quakes wreck his own Factory. Gyro Ball x1.5.
    P("FERROTHORN", 69, "IRONBARBS", "ROCKYHELMET", "RELAXED", "STEALTHROCK,LEECHSEED,POWERWHIP,GYROBALL", "PD", tr=True),
    # Sand Rush can't work indoors (no sandstorm in the Factory): Mold Breaker and Drill Run instead.
    P("EXCADRILL", 69, "MOLDBREAKER", "LIFEORB", "ADAMANT", "DRILLRUN,IRONHEAD,ROCKSLIDE,SWORDSDANCE", "A",
      only="nocasual", hard={"item": "FOCUSSASH", "moves": "DRILLRUN,IRONHEAD,ROCKSLIDE,RAPIDSPIN"}),
    P("KINGAMBIT", 70, "DEFIANT", "BLACKGLASSES", "ADAMANT", "KOWTOWCLEAVE,IRONHEAD,SUCKERPUNCH,SWORDSDANCE", "HA",
      hard={"ab": "SUPREMEOVERLORD", "item": "LEFTOVERS"}),
    # Field engine. Synthetic Seed: +1 Attack, +1 Speed. Shift Gear also gives +1 Defense and Gear Grind is x2 here.
    # Answer to the wrecking flip: Magnet Rise dodges the quakes (+1 Speed here) and, with Wild Charge, restarts a
    # Scrapyard (3 charging moves -> Factory).
    P("KLINKLANG", 70, "CLEARBODY", "SYNTHETICSEED", "ADAMANT", "SHIFTGEAR,GEARGRIND,WILDCHARGE,MAGNETRISE", "A",
      nick="Mark One", casual={"item": "SITRUSBERRY", "moves": "SHIFTGEAR,GEARGRIND,WILDCHARGE,SUBSTITUTE"}),
    P("SCIZOR", 70, "TECHNICIAN", "METALCOAT", "ADAMANT", "BULLETPUNCH,UTURN,KNOCKOFF,SWORDSDANCE", "HA",
      hard={"item": "LIFEORB", "moves": "BULLETPUNCH,UTURN,DUALWINGBEAT,SWORDSDANCE"}),
    # Hammer Arm is a hammer (x1.3) and replaces Earthquake.
    P("METAGROSS", 71, "CLEARBODY", "ASSAULTVEST", "ADAMANT", "METEORMASH,ZENHEADBUTT,HAMMERARM,BULLETPUNCH", "HA",
      nick="Engine", hard={"item": "METAGROSSITE", "nat": "JOLLY", "ev": "A",
                           "moves": "METEORMASH,ZENHEADBUTT,HAMMERARM,ICEPUNCH"}),
])
warden(16, "LEADER_NYX", "Nyx", 75, "NEW_MOON", "Lights on. ...Huh. You were real the whole time.", [
    # DOUBLE battle (story: the illusion double). Lead pair: Prankster screens beside Weavile's Fake Out.
    P("GRIMMSNARL", 73, "PRANKSTER", "LIGHTCLAY", "CAREFUL", "REFLECT,LIGHTSCREEN,SPIRITBREAK,FAKEOUT", "SD",
      hard={"moves": "REFLECT,LIGHTSCREEN,SPIRITBREAK,TAUNT"}),
    # Stage play: Magical Seed on the New Moon gives +1 accuracy and Focus Energy and pulls the field down into the Abyss
    # (shadow moves x1.4, the challenger's accuracy x0.8). Night Slash then always crits.
    P("WEAVILE", 73, "PRESSURE", "MAGICALSEED", "JOLLY", "FAKEOUT,NIGHTSLASH,ICICLECRASH,ICESHARD", "A",
      casual={"item": "SITRUSBERRY", "moves": "KNOCKOFF,ICICLECRASH,ICESHARD,SWORDSDANCE"},
      hard={"ab": "PICKPOCKET", "moves": "FAKEOUT,NIGHTSLASH,TRIPLEAXEL,ICESHARD"}),
    P("MALAMAR", 74, "CONTRARY", "LEFTOVERS", "ADAMANT", "SUPERPOWER,KNOCKOFF,PSYCHOCUT,PROTECT", "BA",
      only="nocasual"),
    # Moonlight fails under the New Moon: Wish instead.
    # Snarl is a Dark spread move (x1.5 here) that cuts both foes' Sp. Atk; Helping Hand for the sweeper beside it.
    P("UMBREON", 74, "INNERFOCUS", "LEFTOVERS", "CALM", "FOULPLAY,SNARL,HELPINGHAND,WISH", "SD",
      hard={"ab": "SYNCHRONIZE", "moves": "FOULPLAY,SNARL,HELPINGHAND,PROTECT"}),
    # Night Daze never misses and three of them deepen the New Moon to an Abyss. Flamethrower is for the Lamplight
    # (Fire x1.2) and Sludge Bomb for the Fairy types who lit it.
    P("ZOROARK", 75, "ILLUSION", "LIFEORB", "TIMID", "NIGHTDAZE,FLAMETHROWER,SLUDGEBOMB,NASTYPLOT", "S",
      nick="Nobody", casual={"item": "SITRUSBERRY", "moves": "NIGHTDAZE,FLAMETHROWER,FOCUSBLAST,NASTYPLOT"},
      hard={"item": "CHOICESPECS", "moves": "NIGHTDAZE,FLAMETHROWER,FOCUSBLAST,SLUDGEBOMB"}),
    P("HONCHKROW", 74, "SUPERLUCK", "SCOPELENS", "ADAMANT", "NIGHTSLASH,BRAVEBIRD,SUCKERPUNCH,HEATWAVE", "A",
      hard={"ab": "MOXIE", "item": "LIFEORB", "moves": "NIGHTSLASH,BRAVEBIRD,SUCKERPUNCH,SUPERPOWER"}),
])
warden(17, "LEADER_CELESTINE", "Celestine", 80, "FAIRY_TALE", "And so the tale turns its final page. Happily, I hope.", [
    # Lead pair: Tinkaton (Fake Out) + Alcremie (Helping Hand on Tinkaton's hammer).
    # The knight: Steel x1.3, hammers swing true. Fake Out buys Alcremie a turn.
    P("TINKATON", 79, "MOLDBREAKER", "SITRUSBERRY", "JOLLY", "FAKEOUT,GIGATONHAMMER,PLAYROUGH,KNOCKOFF", "A",
      casual={"moves": "GIGATONHAMMER,PLAYROUGH,KNOCKOFF,STEALTHROCK"}),
    # DOUBLE battle (story: "the knight and the dragon").
    # Magical Seed on Fairy Tale: +1 Sp. Atk, +1 Sp. Def, no cost. Helping Hand for the partner (Decorate was the first
    # pick, but the v21 AI only aims a NearOther move at foes, so it never decorated its partner in the harness).
    P("ALCREMIE", 78, "AROMAVEIL", "MAGICALSEED", "BOLD", "HELPINGHAND,DAZZLINGGLEAM,MYSTICALFIRE,RECOVER", "BS",
      casual={"item": "LEFTOVERS"}, hard={"moves": "CALMMIND,DRAININGKISS,MYSTICALFIRE,RECOVER"}),
    P("MIMIKYU", 78, "DISGUISE", "LIFEORB", "JOLLY", "PLAYROUGH,SHADOWCLAW,SHADOWSNEAK,SWORDSDANCE", "A",
      only="nocasual"),
    # Fire is no Steel answer here (dragonfire: Fire also hits as Dragon, which Steel resists). Superpower is.
    P("AZUMARILL", 79, "HUGEPOWER", "SITRUSBERRY", "ADAMANT", "AQUAJET,PLAYROUGH,LIQUIDATION,SUPERPOWER", "HA",
      casual={"ab": "THICKFAT"}, hard={"moves": "AQUAJET,PLAYROUGH,SUPERPOWER,BELLYDRUM"}),
    # "Vigilant" guards: Follow Me draws the Steel and Poison hits meant for the ace; Dazzling Gleam hits both foes.
    P("TOGEKISS", 79, "SERENEGRACE", "LEFTOVERS", "BOLD", "FOLLOWME,AIRSLASH,DAZZLINGGLEAM,AURASPHERE", "BS",
      nick="Vigilant", casual={"moves": "AIRSLASH,DAZZLINGGLEAM,AURASPHERE,ROOST"}),
    # Ace per the story bible. Pixilate Hyper Voice hits both foes; Draining Kiss x2 here (and it wakes sleepers); three
    # Fairy attacks tame a roused Dragon's Den back into Fairy Tale with a x1.3 strike.
    P("SYLVEON", 80, "PIXILATE", "PIXIEPLATE", "MODEST", "HYPERVOICE,DRAININGKISS,PSYSHOCK,CALMMIND", "BS",
      nick="Vow", casual={"ab": "CUTECHARM", "moves": "MOONBLAST,DRAININGKISS,PSYSHOCK,CALMMIND"},
      hard={"item": "LEFTOVERS"}),
])
warden(18, "LEADER_SIGRUN", "Sigrun", 85, "DRAGONS_DEN", "The den is quiet. That has not happened in thirty years. Go, Sovereign-to-be.", [
    P("FLYGON", 83, "LEVITATE", "CHOICESCARF", "JOLLY", "EARTHQUAKE,OUTRAGE,UTURN,STONEEDGE", "A",
      hard={"moves": "EARTHQUAKE,OUTRAGE,UTURN,FIREPUNCH"}),
    # Clanging Scales x2 re-opens a cooled Cave into the Den; Flash Cannon is the Fairy answer.
    P("KOMMOO", 83, "BULLETPROOF", "THROATSPRAY", "TIMID", "CLANGOROUSSOUL,CLANGINGSCALES,AURASPHERE,FLASHCANNON", "S",
      casual={"moves": "CLANGINGSCALES,AURASPHERE,FLAMETHROWER,POISONJAB", "item": "SITRUSBERRY"}),
    # Multiscale in the Den: Dragon's weaknesses become neutral. Dragon Dance gives +2 Speed here. Replaces Goodra.
    P("DRAGONITE", 84, "MULTISCALE", "LUMBERRY", "ADAMANT", "DRAGONDANCE,DRAGONCLAW,EXTREMESPEED,FIREPUNCH", "A",
      only="nocasual", hard={"item": "ELEMENTALSEED", "moves": "DRAGONDANCE,OUTRAGE,EXTREMESPEED,EARTHQUAKE"}),
    P("HAXORUS", 84, "MOLDBREAKER", "LUMBERRY", "JOLLY", "DRAGONDANCE,OUTRAGE,EARTHQUAKE,POISONJAB", "A",
      hard={"moves": "DRAGONDANCE,OUTRAGE,EARTHQUAKE,CLOSECOMBAT"}),
    # Transition play: one Draco Meteor turns a Cave straight back into the Den (x1.3 strike).
    P("DRAGAPULT", 84, "CLEARBODY", "LIFEORB", "NAIVE", "DRAGONDARTS,DRACOMETEOR,FLAMETHROWER,UTURN", "MX",
      casual={"item": "SITRUSBERRY"}, hard={"ab": "INFILTRATOR"}),
    # "The hoard protects its own": an Amulet Coin holder can't be statused in the Den.
    P("SALAMENCE", 85, "INTIMIDATE", "AMULETCOIN", "NAIVE", "DRAGONDANCE,OUTRAGE,EARTHQUAKE,FIREBLAST", "MX",
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

def starter_mon(ttype, slot, stage, lv, hidden_on_hard=False, pos_note="", moves=None, item=None, casual=None):
    """moves / item: {line: value} Standard overrides for this battle. They only show when the player picked a Gen 1
    starter: for any other generation Core swaps the species and regenerates its level-up moves (item kept)."""
    line = SLOT_LINE[ttype][slot]
    ms, mh, nat, ev, it, ith = SETS[stage][line]
    if moves and line in moves:
        ms = moves[line]
    if item and line in item:
        it = item[line]
    sp = LINES[line][stage]
    hard = {"moves": mh, "item": ith}
    if hidden_on_hard:
        hard["abidx"] = 2
    return P(sp, lv, None, it, nat, ms, ev, abidx=0, hard=hard, casual=(casual or {}).get(line))

RIVALS = []
def rival(ttype, name, num, cap, lose, build):
    RIVALS.append((ttype, name, num, cap, lose, build))

# --- Kestrel -----------------------------------------------------------------
rival("RIVAL_KESTREL", "Kestrel", 1, 7, "Whatever. Beginner's luck. Don't get used to it.", lambda s: [
    # K1, the tutorial on Ferrow's Landing (can be lost). Reborn's Cain / Victoria and Rejuvenation's Ren open with a
    # Lv 5 starter and basic moves; Kestrel picks the starter with the type edge, so Standard matches the player's level
    # (Lv 5) instead of out-levelling it. Hard: Lv 6 with Starly; Casual: Lv 3 (no type move yet on a Gen 1 pick).
    P("STARLY", 5, "KEENEYE", None, "JOLLY", "TACKLE,GROWL,QUICKATTACK", "A", only="hard"),
    dict(starter_mon("RIVAL_KESTREL", s, 0, 5), hard={"moves": SETS[0][SLOT_LINE["RIVAL_KESTREL"][s]][1],
                                                     "item": "ORANBERRY"},
         casual={"moves": {"FIRE": "SCRATCH,GROWL", "WATER": "TACKLE,TAILWHIP", "GRASS": "TACKLE,GROWL"}[SLOT_LINE["RIVAL_KESTREL"][s]]}),
])
rival("RIVAL_KESTREL", "Kestrel", 2, 23, "...Fine. Stay out of the Hollow's way, then. I mean it.", lambda s: [
    # K2 is on the Gullcry Cliffs (MOUNTAIN): Rock x1.5, Flying x1.2, wind moves x1.3, Tailwind 2 turns longer. Reference
    # rivals at this point (Reborn's Fern 2, Rejuvenation's Ren 4) bring four Pokemon at cap-3 .. cap-1 with items.
    # Staravia's Telluric Seed gives +1 Speed and a Tailwind (6 turns here) for his side; Sandile's Rock Tomb is x1.5
    # on the cliffs and slows; Moxie snowballs. Counterplay: Protect / switch out the Tailwind turns, Water and Grass for
    # Sandile, Ghost and Dark for Morwen.
    P("STARAVIA", 20, "INTIMIDATE", "TELLURICSEED", "JOLLY", "WINGATTACK,QUICKATTACK,AERIALACE,ENDEAVOR", "A",
      only="nocasual", hard={"moves": "WINGATTACK,QUICKATTACK,DOUBLEEDGE,UTURN", "ab": "RECKLESS"}),
    P("SANDILE", 20, "MOXIE", "ORANBERRY", "JOLLY", "BITE,ROCKTOMB,SANDTOMB,HONECLAWS", "A", only="nocasual",
      hard={"moves": "BITE,ROCKTOMB,DIG,HONECLAWS"}),
    # Hard only: the Deino that becomes Hydreigon (K5+), already mean.
    P("DEINO", 21, "HUSTLE", "ORANBERRY", "ADAMANT", "DRAGONBREATH,BITE,HEADBUTT,ROAR", "A", only="hard"),
    P("HONEDGE", 20, "NOGUARD", "ORANBERRY", "ADAMANT", "SLASH,SHADOWSNEAK,AERIALACE,FURYCUTTER", "BA",
      nick="Morwen", hard={"moves": "SHADOWSNEAK,IRONHEAD,AERIALACE,SWORDSDANCE", "item": "EVIOLITE"}),
    starter_mon("RIVAL_KESTREL", s, 1, 22),
])
rival("RIVAL_KESTREL", "Kestrel", 3, 35, "She had a seat, and a Plate... You don't get it. Nobody does.", lambda s: [
    P("STARAVIA", 31, "INTIMIDATE", "SHARPBEAK", "JOLLY", "AERIALACE,QUICKATTACK,TAKEDOWN,DOUBLETEAM", "A",
      hard={"ab": "RECKLESS", "moves": "BRAVEBIRD,QUICKATTACK,DOUBLEEDGE,UTURN"}),
    P("SCYTHER", 32, "TECHNICIAN", "EVIOLITE", "JOLLY", "AERIALACE,BUGBITE,QUICKATTACK,SWORDSDANCE", "A", only="hard"),
    # K3 is in the Bone Sands (DESERT): Sand Tomb x2, Dig x1.5, and special attacks do x0.67 to the burrowed Ground type.
    P("KROKOROK", 31, "MOXIE", "SOFTSAND", "JOLLY", "CRUNCH,DIG,SANDTOMB,SWAGGER", "A", only="nocasual",
      hard={"moves": "CRUNCH,STOMPINGTANTRUM,ROCKSLIDE,FIREFANG", "item": "EVIOLITE"}),
    P("DOUBLADE", 32, "NOGUARD", "EVIOLITE", "ADAMANT", "SLASH,SHADOWSNEAK,IRONHEAD,AERIALACE", "BA",
      nick="Morwen", hard={"moves": "NIGHTSLASH,SHADOWSNEAK,IRONHEAD,SWORDSDANCE"}),
    starter_mon("RIVAL_KESTREL", s, 1, 33),
])
rival("RIVAL_KESTREL", "Kestrel", 4, 43, "It wasn't her. It was never her. ...Don't. Just don't.", lambda s: [
    # K4 is the Ironreach Open final (COLOSSEUM): Close Combat x1.2, Retaliate x1.3, every knockout feeds the crowd (+1 Attack,
    # on top of Krookodile's Moxie), Technician Bullet Punch is a punch (x1.2).
    P("STARAPTOR", 41, "INTIMIDATE", "SHARPBEAK", "JOLLY", "CLOSECOMBAT,AERIALACE,RETALIATE,DOUBLEEDGE", "A",
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
def kestrel_late(lvs, mis, lose_num, ov=None):
    """ov: {SPECIES: {field: value}} per-battle field tweaks (Standard set; 'hard'/'casual' keys replace those dicts)."""
    a, b, c, d, st, ace = lvs
    ov = ov or {}
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
        for i, m in enumerate(team):
            if m["sp"] in ov:
                team[i] = dict(m, **ov[m["sp"]])
        return team
    return f
# K5, Skyreach (STORMFRONT): Brave Bird x1.2; Smack Down is x2 on the airship deck and grounds fliers for Earthquake.
rival("RIVAL_KESTREL", "Kestrel", 5, 55, "Meridian's paying for my next Ball. Funny how that works.",
      kestrel_late((52, 52, 53, 52, 54, 54), False, 5, ov={
          "KROOKODILE": {"moves": "KNOCKOFF,EARTHQUAKE,SMACKDOWN,CLOSECOMBAT"},
          "SCIZOR": {"moves": "BULLETPUNCH,UTURN,DUALWINGBEAT,SWORDSDANCE"}}))
# K6, Gravenmoor (HOLLOW_CATHEDRAL): Ghost x1.5 for Morwen's blade; the veil is thin, so Staraptor's Double-Edge hits Ghosts;
# Hydreigon's Flamethrower is ghostfire (also Ghost). Spell Tag on the blade.
rival("RIVAL_KESTREL", "Kestrel", 6, 67, "She burned her own name. For YOU. ...Get out of my sight.",
      kestrel_late((64, 64, 65, 65, 66, 66), False, 6, ov={
          "AEGISLASH": {"item": "SPELLTAG"}}))
# K7, Gloaming (FAIRY_TALE): "he insists he's the knight". Sacred Sword is a blade (x1.3) and King's Shield gives +1 Defense.
# Transition play: Hydreigon's Dragon Pulse is x1.5 here and the third Dragon attack rouses the Dragon's Den (x1.3 strike),
# where it takes x0.83 and Fairy loses its boost. Flash Cannon (Steel x1.3) is for the Fairy types.
rival("RIVAL_KESTREL", "Kestrel", 7, 80, "They all want to use you. Fine. Walk into Crownhaven. I'll be waiting.",
      kestrel_late((77, 77, 78, 78, 79, 79), True, 7, ov={
          "HYDREIGON": {"item": "LIFEORB", "moves": "DRAGONPULSE,DARKPULSE,FLASHCANNON,FLAMETHROWER",
                        "hard": {"moves": "DRAGONPULSE,DARKPULSE,FLASHCANNON,EARTHPOWER"},
                        "casual": {"item": "SITRUSBERRY"}}}))
# K8 / K9, Festival semifinal (PRISM_ARENA): the arena opens with Fire, Water, Grass, so the starter (advantage over the
# player's) and Hydreigon's coverage carry the opening. Magical Seed on the arena: +1 Sp. Atk, +1 Sp. Def, no cost.
PRISM_KESTREL = {"AEGISLASH": {"item": "MAGICALSEED", "hard": {"item": "WEAKNESSPOLICY", "moves": "KINGSSHIELD,SHADOWBALL,CLOSECOMBAT,SHADOWSNEAK"}},
                 "HYDREIGON": {"moves": "DRACOMETEOR,DARKPULSE,FLAMETHROWER,EARTHPOWER", "item": "LIFEORB",
                               "hard": {"moves": "DRACOMETEOR,DARKPULSE,FLASHCANNON,EARTHPOWER"}, "casual": {"item": "SITRUSBERRY"}}}
rival("RIVAL_KESTREL", "Kestrel", 8, 94, "If I lost, I lost to you. Not to them. ...That's enough.",
      kestrel_late((90, 91, 92, 92, 93, 94), True, 8, ov=PRISM_KESTREL))

def kestrel_fallen(s_):
    team = promote(kestrel_late((90, 91, 92, 92, 93, 94), True, 9, ov=PRISM_KESTREL)(s_))
    for i, m in enumerate(team):
        if m["sp"] == "KROOKODILE":
            # The Gauntlet: Techno Blast's type follows its Drive; with the Burn Drive it opens on the arena's Fire turn.
            team[i] = P("GENESECT", 91, "DOWNLOAD", "BURNDRIVE", "HASTY", "TECHNOBLAST,IRONHEAD,THUNDERBOLT,UTURN", "MX",
                        nick="Gauntlet", form=2, casual={"item": "SITRUSBERRY", "form": 0, "moves": "UTURN,IRONHEAD,THUNDERBOLT,FLAMETHROWER"})
    return team
rival("RIVAL_KESTREL", "Kestrel", 9, 94, "...It won't let go. Why won't it let go?", kestrel_fallen)

# --- Juno --------------------------------------------------------------------
rival("RIVAL_JUNO", "Juno", 1, 15, "Aww, you're so good at this! Okay, again soon, okay?", lambda s: [
    # J1 is on Saltmere's promenade green (MEADOW, set by TRAINER_FIELDS), just before Gym 1: Grass and Bug x1.2, Fairy Wind
    # and Razor Leaf x1.5 in the breeze, Leaf Guard always on, powders x1.25 accurate.
    # Transition play: Cottonee's Prankster Grassy Terrain - or Petilil's two tending moves (Growth, Aromatherapy) - turn
    # the Meadow into a Flower Garden, the field she will defend at Gym 9 (Grass x1.5 from stage 2).
    # Reference: Reborn's Fern 0 (three at 13-14, Oran Berry, Potion) and Rejuvenation's Ren (four at 13-16): Std 4 here.
    # Counterplay: two Fire attacks burn the Meadow away (one in sun); Flying and Poison for the Grass types.
    P("COTTONEE", 12, "PRANKSTER", "ORANBERRY", "BOLD", "FAIRYWIND,MEGADRAIN,GRASSYTERRAIN,STUNSPORE", "SD",
      only="nocasual"),
    P("PETILIL", 13, "OWNTEMPO", "ORANBERRY", "MODEST", "MEGADRAIN,GROWTH,AROMATHERAPY,STUNSPORE", "S", only="nocasual"),
    P("BOUNSWEET", 13, "LEAFGUARD", "ORANBERRY", "ADAMANT", "RAZORLEAF,RAPIDSPIN,PLAYNICE,SPLASH", "BA",
      nick="Sweetpea", hard={"item": "EVIOLITE", "moves": "RAZORLEAF,RAPIDSPIN,PLAYNICE,MAGICALLEAF"},
      casual={"moves": "RAPIDSPIN,PLAYNICE,SPLASH"}),
    # Hard only: the farm's Fidough (Fairy; Own Tempo), Covet and Bite.
    P("FIDOUGH", 13, "OWNTEMPO", "ORANBERRY", "IMPISH", "COVET,BITE,LICK,TAILWHIP", "BA", only="hard"),
    starter_mon("RIVAL_JUNO", s, 0, 14, moves={"GRASS": "VINEWHIP,RAZORLEAF,LEECHSEED,TACKLE",
                                              "FIRE": "EMBER,DRAGONBREATH,SCRATCH,SMOKESCREEN",
                                              "WATER": "WATERGUN,RAPIDSPIN,TACKLE,WITHDRAW"},
                item={"GRASS": "ORANBERRY", "FIRE": "ORANBERRY", "WATER": "ORANBERRY"}),
])
rival("RIVAL_JUNO", "Juno", 2, 35, "That's not his name in the ledger. It can't be. ...Good battle, though.", lambda s: [
    # J2 is on Mirefen's stilt-walk (CORROSIVE_MIRE), where her Grass moves also hit as Poison. Transition play: a Prankster
    # Misty Terrain cleanses the mire to open water (-> Water Surface), which her Grass types resist and which lasts 7 turns.
    P("WHIMSICOTT", 31, "PRANKSTER", "SITRUSBERRY", "TIMID", "LEECHSEED,ENERGYBALL,MISTYTERRAIN,FAIRYWIND", "S",
      casual={"moves": "LEECHSEED,ENERGYBALL,COTTONSPORE,FAIRYWIND"},
      hard={"moves": "LEECHSEED,ENERGYBALL,MOONBLAST,MISTYTERRAIN"}),
    # Ever-Bloom (SPINE Rev 12): the white Floette that becomes J3's Florges "Everbloom". Hard only here.
    P("FLOETTE", 32, "FLOWERVEIL", "SITRUSBERRY", "CALM", "MAGICALLEAF,RAZORLEAF,WISH,FAIRYWIND", "SD", form=4,
      nick="Everbloom", only="hard"),
    P("LILLIGANT", 31, "OWNTEMPO", "MIRACLESEED", "MODEST", "MAGICALLEAF,TEETERDANCE,SLEEPPOWDER,QUIVERDANCE", "S",
      only="nocasual", hard={"moves": "GIGADRAIN,PETALDANCE,SLEEPPOWDER,QUIVERDANCE"}),
    P("STEENEE", 32, "LEAFGUARD", "EVIOLITE", "ADAMANT", "RAZORLEAF,STOMP,RAPIDSPIN,PLAYNICE", "BA",
      nick="Sweetpea", hard={"moves": "SEEDBOMB,STOMP,RAPIDSPIN,PLAYROUGH"}),
    starter_mon("RIVAL_JUNO", s, 1, 33),
])
rival("LEADER_JUNO", "Juno", 3, 47, "I'm crying. I said I would. ...Take it. The Meadow badge is yours.", lambda s: [
    # Gardener. Telluric Seed: +1 Sp. Def, Ingrain, garden +1 stage on entry; Prankster Growth and Leech Seed each add a stage
    # (and regrow what Fire prunes; from Embers two of them bring the Meadow back).
    P("WHIMSICOTT", 45, "PRANKSTER", "TELLURICSEED", "TIMID", "LEECHSEED,GROWTH,ENERGYBALL,MOONBLAST", "S",
      casual={"item": "LEFTOVERS"}, hard={"moves": "LEECHSEED,GROWTH,MOONBLAST,TAILWIND"}),
    # Ever-Bloom (SPINE Rev 12): the white Florges is the bridal blossom, and replaces Shiinotic. Flower Veil: the
    # garden grows a stage when it enters and her Grass types can't be statused or have stats lowered beside it.
    # Grassy Terrain grows it again and lasts 8 turns here.
    P("FLORGES", 45, "FLOWERVEIL", "SITRUSBERRY", "CALM", "MOONBLAST,PETALBLIZZARD,GRASSYTERRAIN,WISH", "SD", form=4,
      nick="Everbloom", only="nocasual", hard={"moves": "MOONBLAST,PETALDANCE,GRASSYTERRAIN,WISH"}),
    P("ROSERADE", 46, "NATURALCURE", "MIRACLESEED", "TIMID", "GIGADRAIN,SLUDGEBOMB,SHADOWBALL,TOXICSPIKES", "S",
      only="hard", nick="Rowan"),
    # Petal Dance is a petal move (up to x1.5 on top of Grass) and Own Tempo never tires of it. Aromatherapy grows the garden.
    P("LILLIGANT", 46, "OWNTEMPO", "MIRACLESEED", "MODEST", "PETALDANCE,GIGADRAIN,AROMATHERAPY,QUIVERDANCE", "S",
      casual={"moves": "PETALDANCE,GIGADRAIN,STUNSPORE,QUIVERDANCE"},
      hard={"moves": "PETALDANCE,GIGADRAIN,SLEEPPOWDER,QUIVERDANCE"}),
    starter_mon("LEADER_JUNO", s, 2, 46),
    # Acrobatics (full power once the Sitrus is eaten) is for the Bug and Grass types that feast in her garden.
    P("TSAREENA", 47, "QUEENLYMAJESTY", "SITRUSBERRY", "ADAMANT", "TROPKICK,PLAYROUGH,ACROBATICS,UTURN", "A",
      nick="Sweetpea", casual={"ab": "LEAFGUARD", "moves": "TROPKICK,LOWSWEEP,PLAYROUGH,UTURN"},
      hard={"item": "LIFEORB", "moves": "POWERWHIP,HIGHJUMPKICK,KNOCKOFF,UTURN"}),
])
rival("RIVAL_JUNO", "Juno", 4, 90, "We started on the same dock. ...You grew more. I'm so glad it was you.", lambda s: [
    P("FLORGES", 86, "FLOWERVEIL", "LEFTOVERS", "CALM", "MOONBLAST,GIGADRAIN,CALMMIND,SYNTHESIS", "SD", form=4,
      nick="Everbloom"),
    P("WHIMSICOTT", 87, "PRANKSTER", "LEFTOVERS", "TIMID", "LEECHSEED,ENERGYBALL,MOONBLAST,TAILWIND", "S",
      hard={"moves": "LEECHSEED,MOONBLAST,ENCORE,TAILWIND"}),
    # J4 is on the PRISM_ARENA. Magical Seed there: +1 Sp. Atk, +1 Sp. Def - set up with Quiver Dance in the three quiet
    # opening turns; the Meadow Plate's turn (Flower Garden, rounds 10-12) is hers.
    P("LILLIGANT", 87, "OWNTEMPO", "MAGICALSEED", "TIMID", "PETALDANCE,GIGADRAIN,SLEEPPOWDER,QUIVERDANCE", "S",
      casual={"item": "MIRACLESEED", "moves": "PETALDANCE,GIGADRAIN,STUNSPORE,QUIVERDANCE"}, hard={"item": "LIFEORB"}),
    P("COMFEY", 88, "TRIAGE", "MEADOWPLATE", "CALM", "DRAININGKISS,GIGADRAIN,CALMMIND,SYNTHESIS", "SD"),
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
ADMINS.append(("Map 120 Briarwick - first admin battle (Act I; before Gym 2 since SPINE Rev 14)", "HOLLOW_THISTLE", "Thistle", 19,
    "Lowmarsh is glass now. Remember that when you sleep.", [
    # Thistle fights at the pylon in Briarwick (SILKWOOD). A weaver's team (02_FACTIONS: Bug/Poison) plus the glassed
    # Phantump she named for her village. Bug x1.5, Grass x1.2, powders x1.2 accurate (Poison Powder, Stun Spore).
    # She lets the wood burn: if the player sets it ablaze, Embers favour Grass and Ghost and heal her Grass types,
    # and Leech Seed + Ingrain-style regrowth (two growing moves) turn the ash into a Meadow.
    # Dustox is a Bug-type flier: it glides on the silk (Flying x1.2) and Shield Dust ignores the player's add-ons.
    P("DUSTOX", 16, "SHIELDDUST", "ORANBERRY", "BOLD", "GUST,STRUGGLEBUG,POISONPOWDER,CONFUSION", "BS",
      casual={"moves": "GUST,BUGBITE,CONFUSION,HARDEN"}),
    P("WHIRLIPEDE", 17, "POISONPOINT", "ORANBERRY", "IMPISH", "POISONTAIL,BUGBITE,PROTECT,IRONDEFENSE", "BPD", only="hard"),
    P("FOONGUS", 17, "EFFECTSPORE", "ORANBERRY", "RELAXED", "MEGADRAIN,STUNSPORE,GROWTH,ASTONISH", "PD",
      only="nocasual", hard={"ab": "REGENERATOR"}),
    P("PHANTUMP", 18, "NATURALCURE", "SITRUSBERRY", "ADAMANT", "BRANCHPOKE,ASTONISH,LEECHSEED,WILLOWISP", "HA",
      nick="Lowmarsh", casual={"moves": "BRANCHPOKE,ASTONISH,LEECHSEED,CONFUSERAY"},
      hard={"ab": "HARVEST", "moves": "BRANCHPOKE,SHADOWCLAW,LEECHSEED,WILLOWISP"}),
]))
ADMINS.append(("Map 160 Ebbmouth - Teo Reyes, Ebbmouth Hollow cell (recurring: later battles use versions 1, 2, ...)", "HOLLOW_TEO", "Teo", 23,
    "Tell my sister— no. Don't tell her anything.", [
    # Teo fights on the stalled mill-race (WATER_SURFACE, set by TRAINER_FIELDS): Water x1.5 and Swift Swim doubles Speed
    # with no rain. No transition play on purpose - this is the fight before Gym 3 teaches the field.
    P("CARVANHA", 19, "ROUGHSKIN", "ORANBERRY", "JOLLY", "AQUAJET,BITE,POISONFANG,SCARYFACE", "A",
      only="nocasual", hard={"ab": "SPEEDBOOST", "moves": "AQUAJET,CRUNCH,POISONFANG,ICEFANG", "item": "FOCUSSASH"}),
    P("BASCULIN", 20, "RECKLESS", "SITRUSBERRY", "ADAMANT", "AQUAJET,BITE,FLAIL,TAILWHIP", "A", only="hard",
      hard={"moves": "WATERFALL,CRUNCH,AQUAJET,PSYCHICFANGS"}),
    P("ARROKUDA", 20, "SWIFTSWIM", "ORANBERRY", "ADAMANT", "AQUAJET,BITE,FURYATTACK,AGILITY", "A",
      hard={"moves": "LIQUIDATION,BITE,AQUAJET,CLOSECOMBAT", "item": "MYSTICWATER"}),
    P("CHEWTLE", 21, "SWIFTSWIM", "SITRUSBERRY", "ADAMANT", "BITE,HEADBUTT,WATERGUN,PROTECT", "BA", nick="Snapper", casual={"ab": "STRONGJAW", "moves": "BITE,WATERGUN,PROTECT,TACKLE"},
      hard={"moves": "BITE,LIQUIDATION,ICEFANG,PROTECT", "item": "EVIOLITE"}),
]))
BOSSES = []
BOSSES.append(("CHAMPION_VALEN", "Valen", 96, "Order, not justice. I chose order... Perhaps the land will forgive us both.", [
    # PRISM_ARENA: three quiet rounds, then the Plates turn every three rounds in a fixed order (Fire, Water, Grass,
    # Electric, Ice, Fighting, Ground, ...). "Order" is his theme, so the team is ordered to meet each Plate as it rises.
    # Quiet rounds: the Crownhaven bells set Stealth Rock and Trick Room.
    P("BRONZONG", 92, "LEVITATE", "LEFTOVERS", "RELAXED", "STEALTHROCK,GYROBALL,PSYCHIC,TRICKROOM", "PD",
      hard={"moves": "STEALTHROCK,GYROBALL,EARTHQUAKE,EXPLOSION"}),
    # Flame Plate (rounds 4-6, Volcanic): Fiery Dance x1.5. Magical Seed on the arena: +1 Sp. Atk, +1 Sp. Def.
    P("VOLCARONA", 95, "FLAMEBODY", "MAGICALSEED", "TIMID", "QUIVERDANCE,FIERYDANCE,BUGBUZZ,GIGADRAIN", "S",
      casual={"item": "SITRUSBERRY", "moves": "FIERYDANCE,BUGBUZZ,GIGADRAIN,PSYCHIC"}, hard={"item": "HEAVYDUTYBOOTS"}),
    # Splash Plate (7-9, Water Surface): Swift Swim is on without rain; his own Rain Dance keeps it on afterwards.
    P("KINGDRA", 94, "SWIFTSWIM", "MYSTICWATER", "MODEST", "DRACOMETEOR,HYDROPUMP,ICEBEAM,RAINDANCE", "S",
      casual={"ab": "SNIPER", "item": "SCOPELENS", "moves": "DRAGONPULSE,HYDROPUMP,ICEBEAM,FOCUSENERGY"},
      hard={"item": "LIFEORB"}),
    # Meadow Plate (10-12) for Leaf Blade, Fist Plate (19-21, Colosseum) for Close Combat; Justified gets +1 Attack there.
    P("GALLADE", 94, "JUSTIFIED", "LIFEORB", "JOLLY", "CLOSECOMBAT,PSYCHOCUT,LEAFBLADE,SWORDSDANCE", "A",
      casual={"item": "SITRUSBERRY"},
      hard={"item": "GALLADITE", "moves": "CLOSECOMBAT,ZENHEADBUTT,KNOCKOFF,SWORDSDANCE"}),
    # Zap Plate (13-15, Neon Grid) for Thunderbolt, Icicle Plate (16-18, Frozen Lake) for Freeze-Dry.
    P("LAPRAS", 93, "WATERABSORB", "ASSAULTVEST", "MODEST", "FREEZEDRY,HYDROPUMP,THUNDERBOLT,SPARKLINGARIA", "BS",
      nick="Ferry"),
    # Earth Plate (22-24, Desert): Ground x1.2 and Thousand Arrows grounds whatever is left in the air.
    P("ZYGARDE", 96, "POWERCONSTRUCT", "LEFTOVERS", "ADAMANT", "THOUSANDARROWS,OUTRAGE,DRAGONDANCE,STONEEDGE", "BA",
      casual={"ab": "AURABREAK", "moves": "THOUSANDARROWS,DRAGONTAIL,CRUNCH,GLARE"},
      hard={"moves": "THOUSANDARROWS,OUTRAGE,COIL,STONEEDGE"}),
]))
BOSSES.append(("MERIDIAN_VOSS", "Aurelian", 100, "The god owes us. It owes ME. ...This isn't over. Machines don't grieve.", [
    # PRISM_ARENA, "things men made". Ordered for the arena's opening: gears spin up in the quiet rounds; Archaludon
    # (Steel/Dragon, neutral to Fire) takes the Flame Plate's turn that the rest of a Steel team dreads; Magnezone gets the
    # Splash Plate's turn (Electric x1.5 against grounded targets) and later the Zap Plate's.
    P("KLINKLANG", 96, "CLEARBODY", "SITRUSBERRY", "JOLLY", "SHIFTGEAR,GEARGRIND,WILDCHARGE,SUBSTITUTE", "A",
      ),
    P("ARCHALUDON", 97, "STAMINA", "POWERHERB", "MODEST", "ELECTROSHOT,FLASHCANNON,DRACOMETEOR,BODYPRESS", "BS",
      casual={"item": "SITRUSBERRY", "moves": "THUNDERBOLT,FLASHCANNON,DRAGONPULSE,BODYPRESS"}),
    # Magical Seed on the arena: +1 Sp. Atk, +1 Sp. Def.
    P("MAGNEZONE", 96, "MAGNETPULL", "MAGICALSEED", "MODEST", "THUNDERBOLT,FLASHCANNON,VOLTSWITCH,BODYPRESS", "BS",
      casual={"item": "SITRUSBERRY", "moves": "THUNDERBOLT,FLASHCANNON,VOLTSWITCH,THUNDERWAVE"},
      hard={"item": "CHOICESPECS", "moves": "THUNDERBOLT,FLASHCANNON,VOLTSWITCH,TRIATTACK"}),
    P("GOLURK", 97, "NOGUARD", "LIFEORB", "ADAMANT", "DYNAMICPUNCH,EARTHQUAKE,POLTERGEIST,STONEEDGE", "HA",
      nick="Gilder", casual={"item": "SITRUSBERRY", "ab": "IRONFIST"}),
    # Tri Attack x1.3 on the arena, with Adaptability.
    P("PORYGONZ", 99, "ADAPTABILITY", "CHOICESCARF", "TIMID", "TRIATTACK,DARKPULSE,ICEBEAM,THUNDERBOLT", "S",
      casual={"item": "SITRUSBERRY"}, hard={"moves": "HYPERBEAM,TRIATTACK,SHADOWBALL,ICEBEAM", "item": "CHOICESPECS"}),
    # Project NULL: Core / Bosses swap its Memory to the ascendant Plate's type (BALANCE.md 6).
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

def patch(mons, sp, **kw):
    """Copy of mons with one species' Standard fields replaced (hard=/casual= replace those dicts)."""
    assert any(m["sp"] == sp for m in mons), sp
    return [dict(m, **kw) if m["sp"] == sp else m for m in mons]

EXTRA = []  # (note, ttype, name, base_version, cap, lose, mons, mega_std)
def X(note, tt, nm, v, cap, lose, mons, mega_std=False):
    EXTRA.append((note, tt, nm, v, cap, lose, mons, mega_std))

X("R16 - Marisol (Grievance) / Ebb Guild exhibition, field :WATER_SURFACE", "LEADER_MARISOL", "Marisol", 90, 90,
  "The tide always comes back. So will I.", [
    # PRISM_ARENA: Drizzle halves the Flame Plate's opening turn; the Splash Plate follows (rounds 7-9) and Swift Swim
    # works with or without the rain.
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
  "Tailwinds, flyer. All the way up.",
  relevel(patch(drop_only(promote(warden_mons("Odessa"))), "NOIVERN", moves="HURRICANE,BOOMBURST,DRACOMETEOR,FLAMETHROWER",
                hard={"moves": "HURRICANE,BOOMBURST,DRACOMETEOR,FLAMETHROWER"}), [88, 89, 90, 90, 91, 92]))
X("Final - Brann, stand-in (Valen collapsed)", "LEADER_BRANN", "Brann", 96, 96,
  "He asked me to. Last thing he asked. ...Forge on, then.", relevel(drop_only(promote(warden_mons("Brann"))), [92, 93, 94, 94, 95, 96]))
valen0 = [b for b in BOSSES if b[0] == "CHAMPION_VALEN"][0][4]
vlast = relevel(promote(valen0), [92, 95, 94, 94, 93, 96])
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
    # INVERSE (set by TRAINER_FIELDS): Trick Room lasts 8 turns, Foul Play x1.3, Psyshock x1.2, Magic Bounce +1 Sp. Def.
    # Magical Seed there: +1 Atk, +1 Sp. Atk, -2 Speed - made for Trick Room.
    P("GOTHITELLE", 91, "COMPETITIVE", "MAGICALSEED", "QUIET", "PSYSHOCK,THUNDERBOLT,TRICKROOM,CALMMIND", "BS", tr=True,
      casual={"item": "LEFTOVERS"}),
    # Transition play: Contrary gets +1 Speed on entry here, and Topsy-Turvy (+1 Speed more) rights the world into the
    # Mindscape whenever the inverted chart favours the challenger - and can turn it back again.
    P("MALAMAR", 92, "CONTRARY", "LEFTOVERS", "ADAMANT", "SUPERPOWER,KNOCKOFF,PSYCHOCUT,TOPSYTURVY", "BA", nick="Behind"),
])
X("Exhibition - Pageant Bout (2-vs-1 double with Rook v90): Dorian's half", "LEADER_DORIAN", "Dorian", 90, 90,
  "Encore! ENCORE!", [
    P("AMBIPOM", 88, "TECHNICIAN", "LIFEORB", "JOLLY", "FAKEOUT,DOUBLEHIT,KNOCKOFF,UTURN", "A", casual={"item": "SILKSCARF"}),
    P("EXPLOUD", 89, "SCRAPPY", "THROATSPRAY", "MODEST", "BOOMBURST,FIREBLAST,FOCUSBLAST,ICEBEAM", "S"),
    # Grand Stage: Synthetic Seed = +1 Speed and Laser Focus; the Taunt costs an all-attack set nothing.
    P("KECLEON", 90, "PROTEAN", "SYNTHETICSEED", "ADAMANT", "FAKEOUT,SHADOWSNEAK,KNOCKOFF,DRAINPUNCH", "BA", nick="Encore",
      casual={"ab": "COLORCHANGE", "item": "SITRUSBERRY"}),
])
X("Exhibition - Pageant Bout (2-vs-1 double with Dorian v90): Rook's half", "LEADER_ROOK", "Rook", 90, 90,
  "Aaand that's a wrap! Clip it, Camera!", [
    P("TOXTRICITY", 88, "PUNKROCK", "THROATSPRAY", "MODEST", "OVERDRIVE,SLUDGEBOMB,BOOMBURST,VOLTSWITCH", "S"),
    P("ELECTIVIRE", 89, "MOTORDRIVE", "LIFEORB", "JOLLY", "WILDCHARGE,ICEPUNCH,CROSSCHOP,EARTHQUAKE", "A", casual={"item": "SITRUSBERRY"}),
    P("ROTOM", 90, "LEVITATE", "LEFTOVERS", "TIMID", "HYDROPUMP,THUNDERBOLT,WILLOWISP,VOLTSWITCH", "S", form=2, nick="Camera"),
])
X("Hijack - Dr. Percival Quent (Voss removed)", "MERIDIAN_QUENT", "Percival", 99, 100,
  "Hee... the numbers were so pretty. So pretty.", [
    # PRISM_ARENA: Heatproof Bronzong sets Trick Room in the quiet rounds and is the one Steel type safe on the Flame
    # Plate's turn (rounds 4-6). Tri Attack is x1.3 on the arena; Magnezone holds the Magical Seed (+1 Sp. Atk, +1 Sp. Def).
    P("BRONZONG", 96, "HEATPROOF", "LEFTOVERS", "RELAXED", "TRICKROOM,GYROBALL,EARTHQUAKE,EXPLOSION", "PD", tr=True),
    P("METAGROSS", 97, "CLEARBODY", "ASSAULTVEST", "ADAMANT", "METEORMASH,ZENHEADBUTT,EARTHQUAKE,BULLETPUNCH", "HA"),
    P("JIRACHI", 97, "SERENEGRACE", "LEFTOVERS", "JOLLY", "IRONHEAD,ZENHEADBUTT,UTURN,FIREPUNCH", "A"),
    P("PORYGONZ", 98, "ADAPTABILITY", "CHOICESPECS", "TIMID", "TRIATTACK,DARKPULSE,ICEBEAM,THUNDERBOLT", "S", casual={"item": "SITRUSBERRY"}),
    P("MAGNEZONE", 99, "MAGNETPULL", "MAGICALSEED", "MODEST", "THUNDERBOLT,FLASHCANNON,VOLTSWITCH,BODYPRESS", "BS",
      casual={"item": "SITRUSBERRY"}),
    P("SILVALLY", 100, "RKSSYSTEM", "STEELMEMORY", "JOLLY", "MULTIATTACK,PARTINGSHOT,FLAMECHARGE,SWORDSDANCE", "A",
      form=8, nick="NULL", casual={"moves": "MULTIATTACK,CRUSHCLAW,FLAMECHARGE,SCARYFACE"}),
])
X("Hijack (Ruin) - Theodric, the Gilded Reflection", "GILDED_THEODRIC", "Theodric", 0, 100,
  "Three hundred years and still the god will not kneel...", [
    # PRISM_ARENA "running Inverse" (story/12_RUIN_ROUTE; the event layers the inverted chart). Reviewed for it: under the
    # inverted chart Fighting and Ghost hit what they could not touch before (No Guard Dynamic Punch into Ghosts,
    # Close Combat into Psychic / Fairy / Flying, Poltergeist into Normal and Dark), and Kyogre + Groudon share one team
    # on purpose: the "Year of Two Weathers". Regigigas keeps Slow Start and Protect.
    P("GOLURK", 97, "NOGUARD", "LIFEORB", "ADAMANT", "DYNAMICPUNCH,EARTHQUAKE,POLTERGEIST,STONEEDGE", "HA", casual={"item": "SITRUSBERRY"}),
    P("AEGISLASH", 97, "STANCECHANGE", "WEAKNESSPOLICY", "QUIET", "KINGSSHIELD,SHADOWBALL,CLOSECOMBAT,SHADOWSNEAK", "BS"),
    P("KYOGRE", 98, "DRIZZLE", "CHOICESPECS", "MODEST", "WATERSPOUT,ORIGINPULSE,ICEBEAM,THUNDER", "S", casual={"item": "LEFTOVERS"}),
    P("GROUDON", 98, "DROUGHT", "LIFEORB", "ADAMANT", "PRECIPICEBLADES,STONEEDGE,FIREPUNCH,SWORDSDANCE", "A", casual={"item": "LEFTOVERS"}),
    P("REGIGIGAS", 99, "SLOWSTART", "LEFTOVERS", "ADAMANT", "CRUSHGRIP,KNOCKOFF,DRAINPUNCH,PROTECT", "HA"),
    # Magical Seed on the arena (+1 Sp. Atk, +1 Sp. Def) with Nasty Plot instead of being locked by Specs: the chart
    # flips under him, so he needs to change moves.
    P("GHOLDENGO", 100, "GOODASGOLD", "MAGICALSEED", "TIMID", "MAKEITRAIN,SHADOWBALL,FOCUSBLAST,NASTYPLOT", "S", nick="Gilt",
      casual={"item": "LEFTOVERS"}, hard={"item": "CHOICESPECS", "moves": "MAKEITRAIN,SHADOWBALL,FOCUSBLAST,TRICK"}),
])
X("Exhibition - Morwen's Echo (Night of Masques, Crownhaven Cathedral lantern)", "ECHO_MORWEN", "Morwen", 90, 90,
  "...Tell him I'm proud. Tell him I'm sorry. In that order.", [
    P("SPIRITOMB", 86, "INFILTRATOR", "LEFTOVERS", "CAREFUL", "FOULPLAY,SHADOWSNEAK,WILLOWISP,PAINSPLIT", "SD"),
    P("DUSKNOIR", 87, "FRISK", "LEFTOVERS", "IMPISH", "POLTERGEIST,SHADOWSNEAK,EARTHQUAKE,TRICKROOM", "BPD"),
    P("JELLICENT", 88, "CURSEDBODY", "LEFTOVERS", "BOLD", "SCALD,SHADOWBALL,WILLOWISP,RECOVER", "BPD"),
    # HOLLOW_CATHEDRAL (set by TRAINER_FIELDS). Last Respects is a Ghost rite: it re-haunts a consecrated nave.
    P("HOUNDSTONE", 88, "FLUFFY", "LIFEORB", "ADAMANT", "LASTRESPECTS,PLAYROUGH,BODYPRESS,WILLOWISP", "HA", casual={"item": "SITRUSBERRY"}),
    P("GENGAR", 89, "CURSEDBODY", "LIFEORB", "TIMID", "SHADOWBALL,SLUDGEBOMB,FOCUSBLAST,PERISHSONG", "S",
      casual={"item": "SITRUSBERRY", "moves": "SHADOWBALL,SLUDGEBOMB,FOCUSBLAST,WILLOWISP"}),
    P("CHANDELURE", 90, "FLASHFIRE", "CHOICESPECS", "TIMID", "SHADOWBALL,FIREBLAST,ENERGYBALL,TRICK", "S", nick="Lantern",
      casual={"item": "SPELLTAG", "moves": "SHADOWBALL,FLAMETHROWER,ENERGYBALL,CALMMIND"}),
])
# Ch21 tag foes (versions 21), aces 97
X("Ch21 tag foe - Sabine Kroll", "MERIDIAN_KROLL", "Sabine", 21, 97, "Nothing personal. It never is.", [
    P("OBSTAGOON", 95, "GUTS", "FLAMEORB", "ADAMANT", "OBSTRUCT,KNOCKOFF,FACADE,CLOSECOMBAT", "A", casual={"item": "SITRUSBERRY"}),
    # Tag double on the PRISM_ARENA: Protect on the frail hitters, Obstruct on the lead.
    P("CRAWDAUNT", 96, "ADAPTABILITY", "LIFEORB", "ADAMANT", "CRABHAMMER,KNOCKOFF,AQUAJET,PROTECT", "A", casual={"item": "SITRUSBERRY"}),
    P("KINGAMBIT", 97, "SUPREMEOVERLORD", "BLACKGLASSES", "ADAMANT", "KOWTOWCLEAVE,IRONHEAD,SUCKERPUNCH,SWORDSDANCE", "HA"),
])
X("Ch21 tag foe - Director Helene Marchetti", "MERIDIAN_MARCHETTI", "Helene", 21, 97, "Directorate, stand down. ...That's an order.", [
    P("MABOSSTIFF", 95, "INTIMIDATE", "SITRUSBERRY", "ADAMANT", "CRUNCH,PLAYROUGH,PSYCHICFANGS,WILDCHARGE", "BA"),
    # Double Intimidate lead; Corviknight's Tailwind for the pair.
    P("ARCANINE", 96, "INTIMIDATE", "SITRUSBERRY", "ADAMANT", "FLAREBLITZ,EXTREMESPEED,WILDCHARGE,PROTECT", "A"),
    P("CORVIKNIGHT", 97, "MIRRORARMOR", "LEFTOVERS", "IMPISH", "BRAVEBIRD,BODYPRESS,TAILWIND,ROOST", "BPD"),
])
X("Ch21 tag foe - Dr. Percival Quent", "MERIDIAN_QUENT", "Percival", 21, 97, "Data! Glorious data! Do it again!", [
    # Heatproof for the Flame Plate's turn; Trick Room for the pair; Tri Attack x1.3 on the arena.
    P("BRONZONG", 95, "HEATPROOF", "LEFTOVERS", "RELAXED", "TRICKROOM,GYROBALL,PSYCHIC,PROTECT", "PD", tr=True),
    P("METAGROSS", 96, "CLEARBODY", "LIFEORB", "ADAMANT", "METEORMASH,ZENHEADBUTT,ROCKSLIDE,BULLETPUNCH", "HA", casual={"item": "SITRUSBERRY"}),
    P("PORYGONZ", 97, "ADAPTABILITY", "LIFEORB", "TIMID", "TRIATTACK,DARKPULSE,ICEBEAM,PROTECT", "S", casual={"item": "SITRUSBERRY"}),
])
X("Ch21 tag foe - Directorate Captain (when Marchetti is turned)", "MERIDIAN_DIRECTORATE", "Captain", 21, 97, "For the Concord.", [
    P("ALAKAZAM", 95, "MAGICGUARD", "LIFEORB", "TIMID", "PSYCHIC,FOCUSBLAST,DAZZLINGGLEAM,PROTECT", "S", casual={"item": "SITRUSBERRY"}),
    P("SCIZOR", 96, "TECHNICIAN", "LIFEORB", "ADAMANT", "BULLETPUNCH,UTURN,KNOCKOFF,SWORDSDANCE", "HA", casual={"item": "METALCOAT"}),
    P("MAGNEZONE", 97, "MAGNETPULL", "CHOICESPECS", "MODEST", "THUNDERBOLT,FLASHCANNON,VOLTSWITCH,BODYPRESS", "BS", casual={"item": "SITRUSBERRY"}),
])
# Ruin Route Gyms 15-18 (version 1): harder (Hard sets on Standard) with different leads
X("Ruin Gym 15 - Magnus on :FACTORY -> :SCRAPYARD turn one", "LEADER_MAGNUS", "Magnus", 1, 71,
  "You came here to break it. So did I, once.",
  # He breaks it himself: the lead's Explosion (x1.3 on the Factory, x1.3 transform strike) leaves a Scrapyard, and
  # Klinklang's Wild Charge / Magnet Rise can restart the line later (Shift Gear fails among the rust until then).
  patch(drop_only(promote(warden_mons("Magnus"))), "FERROTHORN", moves="EXPLOSION,GYROBALL,POWERWHIP,LEECHSEED", item="OCCABERRY"))
X("Ruin Gym 16 - Nyx, illusion DOUBLE battle on :NEW_MOON with Inverse matchups", "LEADER_NYX", "Nyx", 1, 75,
  "Three hundred years of keeping secrets. Let's spend them.", drop_only(promote(warden_mons("Nyx"), lead=1)))
X("Ruin Gym 17 - Celestine on :FAIRY_TALE (refuses the badge)", "LEADER_CELESTINE", "Celestine", 1, 80,
  "Every tale has a verse of none. You found it.", drop_only(promote(warden_mons("Celestine"), lead=3)))
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
# STORY ADMINS, THE MOURNER, THE EEVEE OCTAVE, WAR SOLDIERS (round 2; design/TRAINER_FIELD_PLAYBOOK.md 6-8)
# Named admins count rematches from 0. Fields: design/FIELD_DEFAULTS.yaml exceptions.trainers unless the map default fits.
# ------------------------------------------------------------------------------
STORY = []  # (note, ttype, name, base_version, cap, lose, mons, nobag)
def S(note, tt, nm, v, cap, lose, mons, nobag=False):
    STORY.append((note, tt, nm, v, cap, lose, mons, nobag))

# --- Ch7: Brother Wick, drowned chapel at the Weeping Fen (HOLLOW_CATHEDRAL) --------------------------------------
S("Ch7 - Brother Wick, drowned chapel (field :HOLLOW_CATHEDRAL). He consecrates it: three holy acts (Heal Bell, Dazzling Gleam) "
  "make hymns x1.3 and holy moves x1.5, and weaken the Ghosts the player brought for a Ghost fight.",
  "HOLLOW_WICK", "Wick", 0, 35, "Nobody bleeds three hundred years from a gift, child. ...Sit. I'll tell you the rest.", [
    # The chapel bell: Heal Bell is a holy act (it counts even with nothing to cure); Echoed Voice is a hymn.
    P("CHIMECHO", 33, "LEVITATE", "SITRUSBERRY", "CALM", "HEALBELL,ECHOEDVOICE,EXTRASENSORY,YAWN", "SD",
      casual={"moves": "HEALBELL,ECHOEDVOICE,CONFUSION,YAWN"}, hard={"moves": "HEALBELL,HYPERVOICE,EXTRASENSORY,YAWN"}),
    P("BRONZONG", 33, "LEVITATE", "SITRUSBERRY", "RELAXED", "GYROBALL,EXTRASENSORY,CONFUSERAY,SAFEGUARD", "PD",
      only="nocasual", hard={"moves": "GYROBALL,EXTRASENSORY,CONFUSERAY,TRICKROOM"}, tr=True),
    # Dazzling Gleam is the third holy act and is x1.5 x1.2 once the nave is consecrated.
    P("MUSHARNA", 34, "FOREWARN", "SITRUSBERRY", "BOLD", "DAZZLINGGLEAM,PSYBEAM,MOONLIGHT,YAWN", "BPD"),
    P("GARDEVOIR", 34, "SYNCHRONIZE", "SITRUSBERRY", "MODEST", "DAZZLINGGLEAM,PSYCHIC,HEALPULSE,CALMMIND", "S", only="hard"),
    # "Sexton": Night Shade is x1.5 in the haunted nave, Will-O-Wisp never misses. He fights to hold, not to win.
    P("DUSCLOPS", 35, "PRESSURE", "EVIOLITE", "IMPISH", "NIGHTSHADE,SHADOWSNEAK,WILLOWISP,PAINSPLIT", "BPD",
      nick="Sexton", casual={"item": "SITRUSBERRY"}),
])
# --- Ch8: Dr. Quent, Cindervault caldera (VOLCANIC -> he damps it) ------------------------------------------------
S("Ch8 - Dr. Percival Quent at the caldera taps (field :VOLCANIC). Transition play: his Rain Dances are the 'dampers' - rain "
  "quenches the field to Cinderglass at once, where rain-form Castform rides the geysers and Thunder never misses.",
  "MERIDIAN_QUENT", "Percival", 0, 39, "Fascinating! You broke it. Do you know what that costs per hour?", [
    # Heatproof is safe from the lava rain and the geysers.
    P("BRONZONG", 37, "HEATPROOF", "DAMPROCK", "RELAXED", "RAINDANCE,GYROBALL,EXTRASENSORY,CONFUSERAY", "PD", tr=True,
      casual={"item": "SITRUSBERRY"}),
    P("MAGNETON", 37, "STURDY", "EVIOLITE", "MODEST", "THUNDER,FLASHCANNON,THUNDERWAVE,RAINDANCE", "BS",
      casual={"moves": "SPARK,FLASHCANNON,THUNDERWAVE,SCREECH", "item": "SITRUSBERRY"}),
    # The weather probe: Forecast makes it a Water type in rain (it rides the Cinderglass geysers: +1 Speed).
    P("CASTFORM", 38, "FORECAST", "SITRUSBERRY", "MODEST", "RAINDANCE,WEATHERBALL,THUNDER,ICEBEAM", "S", only="nocasual"),
    P("ROTOM", 38, "LEVITATE", "SITRUSBERRY", "MODEST", "HYDROPUMP,THUNDER,RAINDANCE,HEX", "S", form=2, only="hard"),
    P("PORYGON2", 39, "DOWNLOAD", "EVIOLITE", "MODEST", "TRIATTACK,ICEBEAM,THUNDERBOLT,RECOVER", "BS",
      nick="Probe", casual={"item": "SITRUSBERRY", "moves": "TRIATTACK,ICEBEAM,THUNDERBOLT,CONVERSION"}),
])
# --- Ch9: Ironreach. Tag battle Sable + Hammer Captain Brisk, then the Mourner -----------------------------------
S("Ch9 - Sable, tag DOUBLE with Hammer Captain Brisk vs player + Kestrel (field :COLOSSEUM). Transition play: the Hammer "
  "brings the roof down - three quakes drop the pit into a Cave (x1.3 strike), where Ground moves reach Kestrel's Staraptor.",
  "HOLLOW_SABLE", "Sable", 0, 43, "Light for everyone, right? ...Oops. Wrong mask.", [
    P("SKUNTANK", 41, "AFTERMATH", "SITRUSBERRY", "ADAMANT", "NIGHTSLASH,POISONJAB,SUCKERPUNCH,PROTECT", "BA"),
    # Dry Skin; Drain Punch is a punch (x1.2) and Fake Out opens the double.
    P("TOXICROAK", 42, "DRYSKIN", "BLACKSLUDGE", "JOLLY", "FAKEOUT,DRAINPUNCH,SUCKERPUNCH,BULLDOZE", "A",
      hard={"moves": "FAKEOUT,DRAINPUNCH,SUCKERPUNCH,EARTHQUAKE", "item": "LIFEORB"}),
    # Battle Armor: +1 Defense on entry here. Fell Stinger is x2 in the pit and a knockout feeds the crowd too.
    P("DRAPION", 43, "BATTLEARMOR", "SCOPELENS", "ADAMANT", "KNOCKOFF,CROSSPOISON,EARTHQUAKE,FELLSTINGER", "A",
      casual={"moves": "KNOCKOFF,CROSSPOISON,BULLDOZE,PROTECT"}),
])
S("Ch9 - Hammer Captain Brisk, Sable's tag partner (field :COLOSSEUM). Bulldoze counts toward the cave-in and slows both foes.",
  "HOLLOW_ADMIN", "Brisk", 0, 43, "Until they listen! ...They're not listening.", [
    P("MIGHTYENA", 40, "MOXIE", "SITRUSBERRY", "JOLLY", "CRUNCH,FIREFANG,SUCKERPUNCH,SNARL", "A"),
    P("BANETTE", 41, "CURSEDBODY", "SPELLTAG", "ADAMANT", "SHADOWCLAW,KNOCKOFF,WILLOWISP,SHADOWSNEAK", "A", only="nocasual"),
    P("SCOLIPEDE", 42, "POISONPOINT", "SITRUSBERRY", "JOLLY", "POISONTAIL,BULLDOZE,ROCKSLIDE,PROTECT", "A",
      hard={"ab": "SPEEDBOOST", "moves": "POISONJAB,BULLDOZE,MEGAHORN,PROTECT"}),
])
S("Ch9 - the Mourner in the reliquary (field :COLOSSEUM). He fights defensively ('get BACK'): Protect and Spiky Shield also "
  "calm a Frenzy. Trevenant is the multi-bar boss (Prismfall Bosses config still to be written: :MOURNER_TREVENANT).",
  "HOLLOW_MOURNER", "Mourner", 0, 43, "Not now - you don't understand - ...Juno. Don't look at me like that.", [
    P("SHIFTRY", 41, "CHLOROPHYLL", "SITRUSBERRY", "JOLLY", "FAKEOUT,LEAFBLADE,SUCKERPUNCH,PROTECT", "A",
      hard={"item": "FOCUSSASH", "moves": "FAKEOUT,LEAFBLADE,SUCKERPUNCH,TAILWIND"}),
    # Payback x1.3 in the pit (he hits back, never first); Spiky Shield is his wall.
    P("CACTURNE", 41, "WATERABSORB", "SITRUSBERRY", "ADAMANT", "SPIKYSHIELD,PAYBACK,SEEDBOMB,LEECHSEED", "BA", only="nocasual"),
    P("GOURGEIST", 42, "FRISK", "LEFTOVERS", "IMPISH", "SEEDBOMB,SHADOWSNEAK,WILLOWISP,LEECHSEED", "BPD", only="hard"),
    # The Phantump he showed Juno in Ch1. Harvest regrows the Sitrus; the same Pokemon is Rowan's Festival ace.
    P("TREVENANT", 43, "HARVEST", "SITRUSBERRY", "IMPISH", "HORNLEECH,SHADOWCLAW,WILLOWISP,PROTECT", "BPD",
      nick="Glasswood", casual={"ab": "NATURALCURE"}, hard={"moves": "HORNLEECH,PHANTOMFORCE,WILLOWISP,PROTECT"}),
])
# --- Ch12-17: the Directorate, Kroll unmasked, Quent again -------------------------------------------------------
S("Ch12 - Director Marchetti on Skyreach's sorting-hall catwalks (field :STORMFRONT). Electric x1.3 for the guard dogs; "
  "Thunder never misses; Tailwind lasts 6 turns. No transition play: she holds a position, she doesn't remake it.",
  "MERIDIAN_MARCHETTI", "Helene", 0, 55, "You're not under arrest. You're under protection. Learn the difference.", [
    P("MABOSSTIFF", 53, "INTIMIDATE", "SITRUSBERRY", "ADAMANT", "CRUNCH,WILDCHARGE,PLAYROUGH,ROAR", "BA"),
    # Lightning Rod takes the Electric answer aimed at Corviknight.
    P("MANECTRIC", 54, "LIGHTNINGROD", "MAGNET", "TIMID", "THUNDER,FLAMETHROWER,SNARL,VOLTSWITCH", "S", only="nocasual"),
    P("ARCANINE", 54, "INTIMIDATE", "SITRUSBERRY", "ADAMANT", "FLAREBLITZ,WILDCHARGE,EXTREMESPEED,CRUNCH", "A",
      casual={"moves": "FIREFANG,WILDCHARGE,EXTREMESPEED,CRUNCH"}),
    P("MAGNEZONE", 54, "STURDY", "AIRBALLOON", "MODEST", "THUNDER,FLASHCANNON,VOLTSWITCH,THUNDERWAVE", "BS", only="hard"),
    P("CORVIKNIGHT", 55, "MIRRORARMOR", "LEFTOVERS", "IMPISH", "BRAVEBIRD,IRONHEAD,TAILWIND,ROOST", "BPD"),
])
S("Ch13 - Sabine Kroll, unmasked at the Lucent tribunal (field :MINDSCAPE). Stage play: three Dark attacks curdle Ilsa's "
  "dream into a Nightmare (Dark x1.5, her Dark types heal 1/16 a turn, Fairy x0.8).",
  "MERIDIAN_KROLL", "Sabine", 0, 59, "Special Accounts thanks you for your testimony.", [
    P("SKUNTANK", 57, "AFTERMATH", "BLACKSLUDGE", "ADAMANT", "NIGHTSLASH,POISONJAB,SUCKERPUNCH,TAUNT", "BA", only="nocasual"),
    P("TOXICROAK", 57, "DRYSKIN", "LIFEORB", "JOLLY", "DRAINPUNCH,GUNKSHOT,SUCKERPUNCH,SWORDSDANCE", "A",
      casual={"item": "BLACKSLUDGE"}),
    P("CRAWDAUNT", 58, "ADAPTABILITY", "SITRUSBERRY", "ADAMANT", "CRABHAMMER,KNOCKOFF,AQUAJET,SWORDSDANCE", "A", only="hard"),
    P("HONCHKROW", 58, "SUPERLUCK", "SCOPELENS", "ADAMANT", "NIGHTSLASH,BRAVEBIRD,SUCKERPUNCH,ROOST", "A"),
    P("DRAPION", 59, "SNIPER", "BLACKGLASSES", "JOLLY", "KNOCKOFF,CROSSPOISON,EARTHQUAKE,SWORDSDANCE", "A",
      casual={"moves": "KNOCKOFF,CROSSPOISON,EARTHQUAKE,TOXICSPIKES"}),
])
S("Ch14 - Marchetti in the Darkglass gallery (field :DARK_CRYSTAL; she shot the lamps out). Dark x1.5, Dark contact moves +1 "
  "crit, the player aims at x0.9. Transition play: if the cavern is relit, one Dark Pulse darkens it again (x1.3 strike).",
  "MERIDIAN_MARCHETTI", "Helene", 1, 63, "Lights. ...Someone get the lights.", [
    # Magical Seed in the dark: +1 Atk, +1 Sp. Atk.
    P("HOUNDOOM", 61, "FLASHFIRE", "MAGICALSEED", "TIMID", "DARKPULSE,FLAMETHROWER,SLUDGEBOMB,NASTYPLOT", "S",
      only="nocasual"),
    P("ARCANINE", 62, "INTIMIDATE", "SITRUSBERRY", "ADAMANT", "FLAREBLITZ,CRUNCH,EXTREMESPEED,WILDCHARGE", "A"),
    P("KINGAMBIT", 62, "DEFIANT", "BLACKGLASSES", "ADAMANT", "KOWTOWCLEAVE,IRONHEAD,SUCKERPUNCH,SWORDSDANCE", "HA", only="hard"),
    P("CORVIKNIGHT", 62, "MIRRORARMOR", "LEFTOVERS", "IMPISH", "BRAVEBIRD,BODYPRESS,BULKUP,ROOST", "BPD"),
    P("MABOSSTIFF", 63, "INTIMIDATE", "BLACKGLASSES", "ADAMANT", "CRUNCH,JAWLOCK,PLAYROUGH,PSYCHICFANGS", "BA",
      casual={"item": "SITRUSBERRY"}),
])
S("Ch16 - Marchetti, tag DOUBLE with Quent v1 vs player + Rook on the casting floor (field :FACTORY). Fire x1.2 softens "
  "Steel plating; Iron Head x1.5.",
  "MERIDIAN_MARCHETTI", "Helene", 2, 71, "Doctor, if you break one more thing in here -", [
    P("ARCANINE", 69, "INTIMIDATE", "SITRUSBERRY", "ADAMANT", "FLAREBLITZ,WILDCHARGE,EXTREMESPEED,PROTECT", "A"),
    P("CORVIKNIGHT", 70, "MIRRORARMOR", "LEFTOVERS", "IMPISH", "BRAVEBIRD,IRONHEAD,TAILWIND,ROOST", "BPD"),
    P("MABOSSTIFF", 71, "INTIMIDATE", "SITRUSBERRY", "ADAMANT", "CRUNCH,PLAYROUGH,WILDCHARGE,PROTECT", "BA"),
])
S("Ch16 - Dr. Quent, Marchetti's tag partner (field :FACTORY). Transition play both ways, for the data: Bronzong's Explosion "
  "wrecks the floor (-> Scrapyard, x1.3 on the Factory and x1.3 strike); three of Porygon-Z's Discharges restart the line.",
  "MERIDIAN_QUENT", "Percival", 1, 71, "Data! Glorious data! ...Why is Helene looking at me like that?", [
    P("BRONZONG", 69, "HEATPROOF", "SITRUSBERRY", "RELAXED", "GYROBALL,TRICKROOM,PROTECT,EXPLOSION", "PD", tr=True,
      casual={"moves": "GYROBALL,TRICKROOM,PROTECT,EXTRASENSORY"}),
    # Magnet Pull: +1 Defense on entry in the Scrapyard. Discharge spares a Levitating / Ground-immune partner only.
    P("MAGNEZONE", 70, "MAGNETPULL", "SITRUSBERRY", "MODEST", "THUNDERBOLT,FLASHCANNON,PROTECT,VOLTSWITCH", "BS"),
    # Download: +1 Speed on entry in the Factory. Discharge is a charging move.
    P("PORYGONZ", 71, "DOWNLOAD", "LIFEORB", "TIMID", "TRIATTACK,DISCHARGE,ICEBEAM,PROTECT", "S",
      casual={"item": "SITRUSBERRY"}),
])
S("Ch17 - Kroll holds the Sun Court in drowned Aurelia (field :CAVE). The Hammer's play again: one quake cracks the "
  "ceiling, the next brings it down on everyone (1/8, Rock-scaled); Rock Slide is x1.5 here.",
  "MERIDIAN_KROLL", "Sabine", 1, 75, "Nothing personal. The cradle's already on the lift.", [
    P("SKUNTANK", 73, "AFTERMATH", "BLACKSLUDGE", "ADAMANT", "NIGHTSLASH,POISONJAB,SUCKERPUNCH,EXPLOSION", "BA",
      casual={"moves": "NIGHTSLASH,POISONJAB,SUCKERPUNCH,TAUNT"}),
    P("TOXICROAK", 73, "DRYSKIN", "LIFEORB", "JOLLY", "DRAINPUNCH,GUNKSHOT,SUCKERPUNCH,EARTHQUAKE", "A", only="nocasual"),
    P("HONCHKROW", 74, "SUPERLUCK", "SCOPELENS", "ADAMANT", "NIGHTSLASH,BRAVEBIRD,SUCKERPUNCH,ROOST", "A"),
    P("OBSTAGOON", 74, "GUTS", "FLAMEORB", "ADAMANT", "OBSTRUCT,KNOCKOFF,FACADE,CLOSECOMBAT", "A", casual={"item": "SITRUSBERRY"}),
    P("KINGAMBIT", 74, "SUPREMEOVERLORD", "BLACKGLASSES", "ADAMANT", "KOWTOWCLEAVE,IRONHEAD,SUCKERPUNCH,SWORDSDANCE", "HA", only="hard"),
    P("DRAPION", 75, "BATTLEARMOR", "SCOPELENS", "JOLLY", "KNOCKOFF,CROSSPOISON,EARTHQUAKE,ROCKSLIDE", "A"),
])
S("Ch17 (if Kroll was beaten publicly in Ch13) - Quent holds the Sun Court instead (field :CAVE). Rock x1.5 for Rock Slide; "
  "Metal Sound is x1.3 accurate in the echo. No transition play.",
  "MERIDIAN_QUENT", "Percival", 2, 75, "Oh, bother. Well. It was a very good reading.", [
    P("BRONZONG", 73, "LEVITATE", "LEFTOVERS", "RELAXED", "TRICKROOM,GYROBALL,ROCKSLIDE,METALSOUND", "PD", tr=True),
    P("MAGNEZONE", 73, "STURDY", "AIRBALLOON", "MODEST", "THUNDERBOLT,FLASHCANNON,VOLTSWITCH,METALSOUND", "BS", only="nocasual"),
    P("METAGROSS", 74, "CLEARBODY", "ASSAULTVEST", "ADAMANT", "METEORMASH,ZENHEADBUTT,ROCKSLIDE,BULLETPUNCH", "HA"),
    P("ROTOM", 74, "LEVITATE", "LEFTOVERS", "MODEST", "HYDROPUMP,THUNDERBOLT,WILLOWISP,VOLTSWITCH", "S", form=2, only="hard"),
    P("PORYGONZ", 75, "ADAPTABILITY", "LIFEORB", "TIMID", "TRIATTACK,DARKPULSE,ICEBEAM,THUNDERBOLT", "S",
      casual={"item": "SITRUSBERRY"}),
])

# --- THE EEVEE OCTAVE --------------------------------------------------------------------------------------------
# Eight Glassfall orphans of the Prism Choir, each raised beside a different Imprint; in-world an Eevee evolves by the
# Imprint it grows up in, so every singer's partner is at home on exactly one field. Leader: Vesper Lindqvist.
#   Ch2  (Saltmere, backstage, after Gym 1): optional DOUBLE, Vesper's Eevee + Carol's Sylveon on the Grand Stage.
#   Ch13 (Lucent cloister): optional DOUBLE vs Vesper alone, on the Mindscape.
#   Ch20 (Crownhaven Choir gardens): the gauntlet. Singers 1-8, one Eeveelution each, each on its own field
#        (TRAINER_FIELDS by version), then Vesper (version 2): the field follows whichever Eeveelution is out
#        (plugins/Prismfall Field Effects/013_FieldEffects_TrainerPlays.rb, ENTRY_FIELDS).
S("Ch2 - Vesper, backstage at the Lantern Theatre after Gym 1, DOUBLE with Chorister Carol (field :GRAND_STAGE). Two singers: "
  "sound moves raise the applause. Her Eevee 'hasn't decided which Imprint it belongs to yet'.",
  "OCTAVE_VESPER", "Vesper", 0, 19, "It hasn't decided yet. ...Neither have you, I think.", [
    P("EEVEE", 18, "ADAPTABILITY", "ORANBERRY", "JOLLY", "SWIFT,QUICKATTACK,BABYDOLLEYES,HELPINGHAND", "A", nick="Amen",
      hard={"item": "EVIOLITE"}),
])
S("Ch2 - Chorister Carol, Vesper's partner in the Saltmere double (field :GRAND_STAGE). Disarming Voice is a spread sound move.",
  "OCTAVE_SINGER", "Carol", 0, 19, "Oh! You sing back. Most people don't.", [
    P("SYLVEON", 18, "CUTECHARM", "ORANBERRY", "MODEST", "DISARMINGVOICE,SWIFT,BABYDOLLEYES,QUICKATTACK", "BS"),
])
S("Ch13 - Vesper in the Lucent Athenaeum cloister, optional DOUBLE (field :MINDSCAPE). Espeon is at home; Amen's Hyper Voice "
  "and Sylveon's Pixilate Hyper Voice are spread sound moves (x1.2 here), and the third one cracks the dream to Inverse.",
  "OCTAVE_VESPER", "Vesper", 1, 59, "The Choir says we were born lucky. I don't feel lucky.", [
    P("ESPEON", 56, "MAGICBOUNCE", "TWISTEDSPOON", "TIMID", "PSYCHIC,DAZZLINGGLEAM,SHADOWBALL,PROTECT", "S",
      casual={"ab": "SYNCHRONIZE"}),
    P("UMBREON", 56, "INNERFOCUS", "LEFTOVERS", "CALM", "FOULPLAY,SNARL,HELPINGHAND,WISH", "SD", only="nocasual"),
    P("SYLVEON", 57, "PIXILATE", "SITRUSBERRY", "MODEST", "HYPERVOICE,MYSTICALFIRE,CALMMIND,PROTECT", "BS",
      casual={"ab": "CUTECHARM", "moves": "MOONBLAST,MYSTICALFIRE,CALMMIND,PROTECT"}),
    P("EEVEE", 58, "ADAPTABILITY", "EVIOLITE", "JOLLY", "HYPERVOICE,DOUBLEEDGE,QUICKATTACK,HELPINGHAND", "A", nick="Amen"),
])
def octave_singer(v, name, field, lose, mon):
    S("Ch20 gauntlet %d/8 - Chorister %s (field :%s)" % (v, name, field), "OCTAVE_SINGER", name, v, 90, lose, [mon])
# 1 Water: Water Absorb sips 1/16 a turn here; Elemental Seed = +1 Speed and Aqua Ring; Dive -> Underwater (x1.3 strike),
#   where everything that isn't a Water type moves at half Speed.
octave_singer(1, "Aria", "WATER_SURFACE", "The tide took the note. That's all right.",
    P("VAPOREON", 90, "WATERABSORB", "ELEMENTALSEED", "BOLD", "SCALD,ICEBEAM,DIVE,WISH", "BPD", casual={"item": "LEFTOVERS"}))
# 2 Electric: Volt Absorb starts charged and heals every turn on the grid; Synthetic Seed = +1 Sp. Atk and Magnet Rise
#   (no Ground answer); Shadow Ball is the hedge for a Blackout (Ghost x1.2) and Discharge reboots it.
octave_singer(2, "Cadence", "NEON_GRID", "Off the beat. Mine, not yours.",
    P("JOLTEON", 90, "VOLTABSORB", "SYNTHETICSEED", "TIMID", "THUNDERBOLT,SHADOWBALL,DISCHARGE,HYPERVOICE", "S",
      casual={"item": "MAGNET"}))
# 3 Fire: Flash Fire starts lit; Lava Plume primes an eruption (+1 for Flareon, lava for the foe); Elemental Seed =
#   +1 Atk / Sp. Atk / Speed and a burn that can't touch a Fire type.
octave_singer(3, "Forte", "VOLCANIC", "Too loud? ...No. Just right, and you were louder.",
    P("FLAREON", 90, "FLASHFIRE", "ELEMENTALSEED", "ADAMANT", "FLAREBLITZ,LAVAPLUME,SUPERPOWER,QUICKATTACK", "A",
      casual={"item": "CHARCOAL"}))
# 4 Ice: Ice Body heals without hail; Elemental Seed = +2 Speed (for 1/8 HP); Ice Shard slides (+1 Speed) and reseals a crack.
octave_singer(4, "Lento", "FROZEN_LAKE", "Slowly, slowly. You got there first anyway.",
    P("GLACEON", 90, "ICEBODY", "ELEMENTALSEED", "MODEST", "ICEBEAM,FREEZEDRY,ICESHARD,SHADOWBALL", "S",
      casual={"item": "NEVERMELTICE"}))
# 5 Grass: the garden starts at stage 3 and the Telluric Seed makes it 4 on entry, which switches Chlorophyll on.
#   No non-Grass blades (they would cut her own garden back).
octave_singer(5, "Lyra", "FLOWER_GARDEN", "It bloomed for you. It doesn't do that for everyone.",
    P("LEAFEON", 90, "CHLOROPHYLL", "TELLURICSEED", "JOLLY", "LEAFBLADE,KNOCKOFF,SWORDSDANCE,SYNTHESIS", "A",
      casual={"ab": "LEAFGUARD", "item": "MIRACLESEED"}))
# 6 Psychic: Magic Bounce gets +1 Sp. Def on the Inverse side of the dream; Hyper Voice x3 cracks the Mindscape into it.
octave_singer(6, "Sona", "MINDSCAPE", "I heard that coming. I still couldn't stop it.",
    P("ESPEON", 90, "MAGICBOUNCE", "TWISTEDSPOON", "TIMID", "PSYCHIC,SHADOWBALL,HYPERVOICE,CALMMIND", "S",
      casual={"ab": "SYNCHRONIZE"}))
# 7 Dark: Magical Seed under the New Moon = +1 accuracy, Focus Energy and an instant Abyss; Dark Pulse x1.5 x1.4 there.
#   Wish, not Moonlight (Moonlight fails).
octave_singer(7, "Noct", "NEW_MOON", "...Good night.",
    P("UMBREON", 90, "INNERFOCUS", "MAGICALSEED", "CALM", "DARKPULSE,FOULPLAY,SNARL,WISH", "SD",
      casual={"item": "LEFTOVERS"}))
# 8 Fairy: Draining Kiss x2, Mystical Fire x1.5, Magical Seed = +1 Sp. Atk, +1 Sp. Def.
octave_singer(8, "Carol", "FAIRY_TALE", "And they all lived. That's the whole ending. They all lived.",
    P("SYLVEON", 90, "PIXILATE", "MAGICALSEED", "MODEST", "HYPERVOICE,DRAININGKISS,MYSTICALFIRE,CALMMIND", "BS",
      casual={"ab": "CUTECHARM", "item": "PIXIEPLATE", "moves": "MOONBLAST,DRAININGKISS,MYSTICALFIRE,CALMMIND"}))
S("Ch20 gauntlet finale - Vesper (starts on :GRAND_STAGE; the field becomes each Eeveelution's home as it enters: Water Surface, "
  "Neon Grid, Volcanic, Mindscape, New Moon, Fairy Tale). Six fields in one fight, so no held seeds: abilities carry it.",
  "OCTAVE_VESPER", "Vesper", 2, 92, "We were all born the year the Crown broke. I think we're just... what was left.", [
    P("VAPOREON", 90, "WATERABSORB", "LEFTOVERS", "BOLD", "SCALD,ICEBEAM,WISH,PROTECT", "BPD"),
    P("JOLTEON", 90, "VOLTABSORB", "LIFEORB", "TIMID", "THUNDERBOLT,SHADOWBALL,VOLTSWITCH,HYPERVOICE", "S",
      casual={"item": "MAGNET"}),
    P("FLAREON", 91, "FLASHFIRE", "CHOICEBAND", "ADAMANT", "FLAREBLITZ,SUPERPOWER,QUICKATTACK,LAVAPLUME", "A",
      casual={"item": "CHARCOAL"}),
    P("UMBREON", 91, "INNERFOCUS", "LEFTOVERS", "CALM", "FOULPLAY,DARKPULSE,WISH,YAWN", "SD"),
    P("ESPEON", 91, "MAGICBOUNCE", "LIFEORB", "TIMID", "PSYCHIC,SHADOWBALL,DAZZLINGGLEAM,CALMMIND", "S",
      casual={"ab": "SYNCHRONIZE", "item": "TWISTEDSPOON"}),
    P("SYLVEON", 92, "PIXILATE", "LEFTOVERS", "MODEST", "HYPERVOICE,DRAININGKISS,MYSTICALFIRE,CALMMIND", "BS",
      nick="Vespers", casual={"ab": "CUTECHARM", "moves": "MOONBLAST,DRAININGKISS,MYSTICALFIRE,CALMMIND"}),
])

# --- THE ASHKAAR-ISENMAR WAR (Ch19 gauntlets; map defaults: 924/925 Cinderglass, 927 Volcanic, 922/926 Frozen Lake) ---
# Generic "Soldier" / "Captain", version = encounter number like the grunts. No bag items.
def soldier(tt, nm, v, lose, mons, note):
    S("Ch19 war - " + note, tt, nm, v, 85, lose, mons, nobag=True)
# Ashkaar (Fire / Dragon / Rock). On Cinderglass: Rock x1.3 and obsidian edges, Magma Armor +1 Def, Steam Engine and
# Sand Rush work, Fire and Water types ride the geysers. Three Lava Plumes re-melt it to Volcanic.
soldier("ASHKAAR_SOLDIER_M", "Soldier", 0, "The Dominar will hear of this!", [
    P("MAGCARGO", 79, "MAGMAARMOR", "SITRUSBERRY", "BOLD", "LAVAPLUME,ANCIENTPOWER,EARTHPOWER,RECOVER", "BPD"),
    P("DRUDDIGON", 80, "ROUGHSKIN", "ROCKYHELMET", "ADAMANT", "DRAGONCLAW,ROCKSLIDE,SUPERPOWER,GLARE", "HA", only="nocasual"),
], "Ashkaar siege line (map 924, Cinderglass)")
soldier("ASHKAAR_SOLDIER_F", "Soldier", 0, "Hold the line - hold - oh, forget it.", [
    P("NINETALES", 79, "DROUGHT", "HEATROCK", "TIMID", "FLAMETHROWER,SOLARBEAM,WILLOWISP,NASTYPLOT", "S"),
    P("FLYGON", 80, "LEVITATE", "SITRUSBERRY", "JOLLY", "DRAGONCLAW,STONEEDGE,EARTHQUAKE,UTURN", "A", only="nocasual"),
], "Ashkaar siege line (map 924, Cinderglass)")
soldier("ASHKAAR_SOLDIER_M", "Soldier", 1, "Tell them we burned bright.", [
    P("CAMERUPT", 80, "MAGMAARMOR", "SITRUSBERRY", "QUIET", "LAVAPLUME,EARTHPOWER,ROCKSLIDE,YAWN", "BS"),
    P("TYRANTRUM", 81, "ROCKHEAD", "SITRUSBERRY", "ADAMANT", "HEADSMASH,DRAGONCLAW,EARTHQUAKE,DRAGONDANCE", "A", only="nocasual"),
], "Cinder Cape Warfort (map 927, Volcanic)")
soldier("ASHKAAR_SOLDIER_F", "Soldier", 1, "My wing's still in the air. You're not done.", [
    P("TALONFLAME", 80, "FLAMEBODY", "SHARPBEAK", "JOLLY", "BRAVEBIRD,FLAREBLITZ,UTURN,ROOST", "A"),
    P("TURTONATOR", 81, "SHELLARMOR", "SITRUSBERRY", "QUIET", "SHELLTRAP,DRAGONPULSE,FLAMETHROWER,SHELLSMASH", "BS", only="nocasual"),
], "Cinder Cape Warfort (map 927, Volcanic)")
soldier("ASHKAAR_OFFICER", "Captain", 0, "Dragons bow to no Accord. ...I'm not a dragon. Go.", [
    # Drought lasts 8 turns on Volcanic; Lava Plume primes eruptions there and re-melts Cinderglass.
    P("TORKOAL", 82, "DROUGHT", "SITRUSBERRY", "BOLD", "LAVAPLUME,EARTHPOWER,SOLARBEAM,WILLOWISP", "PD"),
    P("COALOSSAL", 82, "STEAMENGINE", "SITRUSBERRY", "BRAVE", "HEATCRASH,STONEEDGE,TARSHOT,ROCKPOLISH", "HA"),
    P("ARCANINE", 83, "FLASHFIRE", "SITRUSBERRY", "ADAMANT", "FLAREBLITZ,WILDCHARGE,EXTREMESPEED,CLOSECOMBAT", "A", only="nocasual"),
    # Stone Edge is x1.3 x1.3 on obsidian; Ground x1.2.
    P("GARCHOMP", 84, "ROUGHSKIN", "LUMBERRY", "JOLLY", "DRAGONCLAW,STONEEDGE,EARTHQUAKE,SWORDSDANCE", "A",
      casual={"moves": "DRAGONCLAW,STONEEDGE,EARTHQUAKE,SANDSTORM"}),
], "Ashkaar siege camp officer (map 924, Cinderglass)")
# Isenmar (Water / Ice). On the Frozen Lake: Ice x1.5, Slush Rush and Ice Body without hail, Thick Fat +1 Def on entry;
# heavy blows crack the ice to open water, which suits their Water types.
soldier("ISENMAR_SOLDIER_M", "Soldier", 0, "Skaldfast stands. I don't, apparently.", [
    P("WALREIN", 79, "ICEBODY", "LEFTOVERS", "MODEST", "BLIZZARD,SURF,ENCORE,PROTECT", "BS"),
    P("CRABOMINABLE", 80, "IRONFIST", "SITRUSBERRY", "ADAMANT", "ICEHAMMER,CLOSECOMBAT,ICEPUNCH,THUNDERPUNCH", "HA", only="nocasual"),
], "Skaldfast harbour (map 922, Frozen Lake)")
soldier("ISENMAR_SOLDIER_F", "Soldier", 0, "The whale's awake and I lose to you. Some war.", [
    P("FROSLASS", 79, "CURSEDBODY", "SITRUSBERRY", "TIMID", "ICEBEAM,SHADOWBALL,ICYWIND,DESTINYBOND", "S"),
    P("DEWGONG", 80, "THICKFAT", "SITRUSBERRY", "CALM", "SURF,ICEBEAM,ICESHARD,ENCORE", "SD", only="nocasual"),
], "Skaldfast harbour (map 922, Frozen Lake)")
soldier("ISENMAR_SOLDIER_M", "Soldier", 1, "Ice remembers. So will I.", [
    P("BEARTIC", 80, "SLUSHRUSH", "SITRUSBERRY", "ADAMANT", "ICICLECRASH,SUPERPOWER,AQUAJET,SWORDSDANCE", "A"),
    P("AVALUGG", 81, "STURDY", "ROCKYHELMET", "IMPISH", "AVALANCHE,BODYPRESS,RAPIDSPIN,RECOVER", "BPD", only="nocasual"),
], "The Shattered Ice (map 926, Frozen Lake)")
soldier("ISENMAR_SOLDIER_F", "Soldier", 1, "Fine. Walk. Everyone walks through us lately.", [
    P("GLALIE", 80, "ICEBODY", "SITRUSBERRY", "JOLLY", "ICICLECRASH,CRUNCH,ICESHARD,SPIKES", "A"),
    P("LAPRAS", 81, "WATERABSORB", "SITRUSBERRY", "MODEST", "SURF,FREEZEDRY,THUNDERBOLT,ICESHARD", "BS", only="nocasual"),
], "The Shattered Ice (map 926, Frozen Lake)")
soldier("ISENMAR_OFFICER", "Captain", 0, "Tell the Thane the line held as long as it could.", [
    # Snow Warning: hail lasts 8 turns here; Aurora Veil needs no hail on this field.
    P("ABOMASNOW", 82, "SNOWWARNING", "SITRUSBERRY", "QUIET", "BLIZZARD,GIGADRAIN,ICESHARD,AURORAVEIL", "BS"),
    P("LAPRAS", 83, "WATERABSORB", "LEFTOVERS", "MODEST", "SURF,FREEZEDRY,THUNDERBOLT,ICESHARD", "BS"),
    P("WEAVILE", 83, "PRESSURE", "LIFEORB", "JOLLY", "TRIPLEAXEL,KNOCKOFF,ICESHARD,SWORDSDANCE", "A", only="nocasual"),
    # Slush Rush without hail; Ice Spinner skates (x1.3); Heavy Slam is the heavy blow that cracks the lake.
    P("CETITAN", 84, "SLUSHRUSH", "SITRUSBERRY", "ADAMANT", "ICESPINNER,EARTHQUAKE,HEAVYSLAM,ICESHARD", "A",
      casual={"ab": "THICKFAT"}),
], "Isenmar ice-fleet officer (map 926, Frozen Lake)")

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
    section("STORY ADMINS, THE MOURNER, THE EEVEE OCTAVE, WAR SOLDIERS")
    for note, tt, nm, v, cap, lose, mons, nobag in STORY:
        OUT.append("# " + note)
        OUT.extend(variants(tt, nm, v, mons, lose, cap, nobag=nobag))
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
