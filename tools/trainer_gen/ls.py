import sys
sys.path.insert(0, "/home/claude/fangame/tools")
import validate_trainers as V
ref = V.RefData(V.DEFAULT_REF)
KEY = set("""SWORDSDANCE NASTYPLOT CALMMIND DRAGONDANCE QUIVERDANCE SHELLSMASH BULKUP TRICKROOM STEALTHROCK SPIKES TOXICSPIKES STICKYWEB
THUNDERWAVE WILLOWISP TOXIC SPORE SLEEPPOWDER HYPNOSIS YAWN ROOST RECOVER SYNTHESIS MOONLIGHT MORNINGSUN SOFTBOILED WISH PROTECT
TAILWIND RAINDANCE SUNNYDAY SANDSTORM HAIL AURORAVEIL REFLECT LIGHTSCREEN GROWTH STRINGSHOT LEECHSEED SUBSTITUTE
BELLYDRUM COIL HONECLAWS SHIFTGEAR AGILITY ROCKPOLISH IRONDEFENSE AMNESIA COTTONGUARD COTTONSPORE ENCORE TAUNT KINGSSHIELD
PAINSPLIT RAPIDSPIN DEFOG UTURN VOLTSWITCH FAKEOUT FLOWERSHIELD INGRAIN AQUARING STOCKPILE CHARM SING TEETERDANCE PERISHSONG
DESTINYBOND CLANGOROUSSOUL GEARUP AROMATHERAPY HEALBELL TRICK FOCUSENERGY SCREECH STRUGGLEBUG ELECTROWEB ICYWIND
SNARL PARTINGSHOT KNOCKOFF FLORALHEALING TAILGLOW WORKUP SLACKOFF HEALPULSE LUNARDANCE MEMENTO EXPLOSION""".split())
for arg in sys.argv[1:]:
    sp, _, lv = arg.partition(":")
    lv = int(lv) if lv else 100
    form = 0
    if "/" in sp:
        sp, f = sp.split("/"); form = int(f)
    d = ref.get_form(sp, form)
    if not d: print("??", sp); continue
    mv = ref.all_learnable(sp, form, lv)
    out = []
    for m, how in sorted(mv.items()):
        info = ref.move_info.get(m, {})
        p = info.get("power", "0")
        p = int(p) if p.isdigit() else 0
        if how.startswith("L") or p >= 55 or m in KEY:
            tag = "" if how in ("tutor",) else ("e" if how == "egg" else "L")
            out.append("%s(%s%s%s)" % (m, info.get("type","?")[:3], p if p else "", "*" if tag == "L" else ("^" if tag=="e" else "")))
    print("== %s%s L%d %s | ab=%s / HA=%s" % (d["name"], ("-"+d["formname"]) if d["formname"] else "", lv, "/".join(d["types"]), ",".join(d["abilities"]), ",".join(d["hidden"])))
    print("   " + " ".join(out))
