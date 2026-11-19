#!/usr/bin/env python3
"""Trainer x field cross-check (Revision 10 item 4: "opponents build for their field").

  ruby tools/trainer_gen/dump_fields.rb /tmp/prismfall_fields.json
  python3 -I tools/trainer_gen/field_fit.py [--all] [--json /tmp/prismfall_fields.json] [--trainers FILE]

For every important trainer (Wardens on their gym field, plus every trainer listed in design/FIELD_DEFAULTS.yaml
exceptions.trainers) it reads the Standard team from pbs/trainers.txt and reports, against the field of that battle:
  + boosted moves (type x move multiplier >= 1.2), abilities the field switches on or rewards on entry, the field's
    seed, moves that drive one of the field's transitions or stage changes
  ! PROBLEMS: a move the field makes fail, a weather ability or move the field blocks, an ability that needs a
    weather the field blocks, an ability the field negates
Exit code 1 if any PROBLEM is found. --all also prints the '+' lines.
Borrowing fields (PRISM_ARENA, BLEED) have few rules of their own, so little is reported for them.
"""
import json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import validate_trainers as V   # noqa: E402

GYMS = {"LEADER_TAMSIN": "SILKWOOD", "LEADER_DORIAN": "GRAND_STAGE", "LEADER_MARISOL": "WATER_SURFACE",
        "LEADER_ROOK": "NEON_GRID", "LEADER_SAHAR": "DESERT", "LEADER_CORVIN": "CORROSIVE_MIRE",
        "LEADER_BRANN": "VOLCANIC", "LEADER_KAITO": "COLOSSEUM", "LEADER_JUNO": "FLOWER_GARDEN",
        "LEADER_ANJA": "FROZEN_LAKE", "LEADER_ODESSA": "STORMFRONT", "LEADER_ILSA": "MINDSCAPE",
        "LEADER_BASTIAN": "CRYSTAL_CAVERN", "LEADER_YSOLDE": "HOLLOW_CATHEDRAL", "LEADER_MAGNUS": "FACTORY",
        "LEADER_NYX": "NEW_MOON", "LEADER_CELESTINE": "FAIRY_TALE", "LEADER_SIGRUN": "DRAGONS_DEN",
        "HOLLOW_THISTLE": "SILKWOOD", "MERIDIAN_VOSS": "PRISM_ARENA"}
WEATHER_ABILITY = {"DRIZZLE": "Rain", "DROUGHT": "Sun", "SANDSTREAM": "Sandstorm", "SNOWWARNING": "Hail",
                   "SANDSPIT": "Sandstorm"}
WEATHER_MOVE = {"RAINDANCE": "Rain", "SUNNYDAY": "Sun", "SANDSTORM": "Sandstorm", "HAIL": "Hail", "SNOWSCAPE": "Hail"}
NEEDS_WEATHER = {"SANDRUSH": "Sandstorm", "SANDFORCE": "Sandstorm", "SWIFTSWIM": "Rain", "CHLOROPHYLL": "Sun",
                 "SLUSHRUSH": "Hail", "SOLARPOWER": "Sun", "RAINDISH": "Rain", "ICEBODY": "Hail"}


def listify(v):
    return v if isinstance(v, list) else [v]


def exception_fields():
    out = {}
    for line in open(os.path.join(ROOT, "design", "FIELD_DEFAULTS.yaml"), encoding="utf-8"):
        m = re.match(r"\s*- \{trainer: (\w+), versions: \[([\d, ]+)\], field: (\w+)", line)
        if m:
            for v in m.group(2).split(","):
                out[(m.group(1), int(v))] = m.group(3)
    return out


def matches(rule, move, mtype, flags):
    if "moves" in rule and move not in listify(rule["moves"]):
        return False
    if "types" in rule and mtype not in listify(rule["types"]):
        return False
    if "flags" in rule and not (set(listify(rule["flags"])) & flags):
        return False
    return any(k in rule for k in ("moves", "types", "flags"))


def main():
    args = sys.argv[1:]
    show_all = "--all" in args
    jpath = args[args.index("--json") + 1] if "--json" in args else "/tmp/prismfall_fields.json"
    if not os.path.exists(jpath):
        sys.exit("run first: ruby tools/trainer_gen/dump_fields.rb %s" % jpath)
    fields = json.load(open(jpath, encoding="utf-8"))
    ref = V.RefData(V.DEFAULT_REF)
    flags_of = {}
    for mid, sec in V.parse_sections(os.path.join(V.DEFAULT_REF, "moves.txt")).items():
        flags_of[mid] = set(f for v in sec.get("Flags", []) for f in v.split(","))
    tpath = args[args.index("--trainers") + 1] if "--trainers" in args else os.path.join(ROOT, "pbs", "trainers.txt")
    trainers = V.parse_trainers(tpath, V.Report())
    exc = exception_fields()
    problems = checked = 0
    for t in trainers:
        if t.version >= 100:
            continue
        field = exc.get((t.ttype, t.version))
        if field is None and t.ttype in GYMS and (t.version == 0 or t.ttype == "LEADER_JUNO"):
            field = GYMS[t.ttype]
        if field in (None, "NONE"):
            continue
        checked += 1
        fd = fields[field]
        active = set(fd.get("activate_abilities") or [])
        entry_ab = set()
        for r in fd.get("on_entry") or []:
            entry_ab |= set(listify((r.get("battlers") or {}).get("abilities", [])))
        seeds = {s["item"] for s in listify(fd.get("seed") or [])}
        trans = list(fd.get("transitions") or [])
        for st in (fd.get("stages") or {}).values():
            trans += st.get("transitions") or []
        fails = fd.get("move_fails") or []
        blocked = set(listify((fd.get("weather") or {}).get("block", [])))
        plus, bad = [], []
        for mon in t.mons:
            prop = lambda k: mon.props[k][0] if k in mon.props else None
            ab, item = prop("Ability"), prop("Item")
            moves = V.csv(prop("Moves")) if prop("Moves") else []
            if ab in active:
                plus.append("%s: %s is always on" % (mon.species, ab))
            elif ab in entry_ab:
                plus.append("%s: %s is rewarded on entry" % (mon.species, ab))
            if ab in (fd.get("negated_abilities") or []):
                bad.append("%s: %s is negated on %s" % (mon.species, ab, field))
            if WEATHER_ABILITY.get(ab) in blocked:
                bad.append("%s: %s can't start %s on %s" % (mon.species, ab, WEATHER_ABILITY[ab], field))
            for r in trans:   # a weather ability that changes the field the moment it enters (e.g. Sand Stream in a crystal cave)
                if WEATHER_ABILITY.get(ab) in listify(r.get("weather", [])):
                    dest = r.get("to") or ("stage %s" % r.get("stage", "%+d" % r.get("stage_delta", 0)))
                    plus.append("%s: %s (%s) drives %s -> %s on entry - make sure that is wanted" %
                                (mon.species, ab, WEATHER_ABILITY[ab], field, dest))
                    break
            if ab in NEEDS_WEATHER and ab not in active and NEEDS_WEATHER[ab] in blocked:
                bad.append("%s: %s never works on %s (%s is blocked)" % (mon.species, ab, field, NEEDS_WEATHER[ab]))
            if item in seeds:
                plus.append("%s: holds the field's %s" % (mon.species, item))
            for mv in moves:
                info = ref.move_info.get(mv, {})
                mtype, fl = info.get("type"), flags_of.get(mv, set())
                status = info.get("cat") == "Status"
                mult = 1.0 if status else (fd.get("type_mods") or {}).get(mtype, 1.0)
                mult *= (fd.get("move_mods") or {}).get(mv, 1.0)
                if mult >= 1.2:
                    plus.append("%s: %s x%.2f" % (mon.species, mv, mult))
                elif mult <= 0.8:
                    plus.append("%s: %s x%.2f (weakened)" % (mon.species, mv, mult))
                driven = False
                for r in trans:
                    if matches(r, mv, mtype, fl) and not (r.get("category") == "damaging" and status):
                        dest = r.get("to") or ("stage %s" % r.get("stage", "%+d" % r.get("stage_delta", 0)))
                        if "rewind" in r:
                            dest = "(rewinds '%s')" % r["rewind"]
                        plus.append("%s: %s drives %s -> %s" % (mon.species, mv, field, dest))
                        driven = True
                        break
                if any(matches(r, mv, mtype, fl) for r in fails):
                    bad.append("%s: %s fails on %s" % (mon.species, mv, field))
                if WEATHER_MOVE.get(mv) in blocked and not driven:
                    bad.append("%s: %s is blocked on %s" % (mon.species, mv, field))
        problems += len(bad)
        if bad or show_all:
            print("%s on %s: %d field hooks, %d problem(s)" % (t.label(), field, len(plus), len(bad)))
            for b in bad:
                print("   ! " + b)
            if show_all:
                for q in plus:
                    print("   + " + q)
    print("%d important Standard team(s) checked, %d problem(s)" % (checked, problems))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
