#!/usr/bin/env python3
"""Generic-trainer species coverage (Reuben's rule, 2026-11-24).

"Barring the main cast and NPCs, the game lets you battle all the non-legendaries/mythicals at least once via
trainer battle." This tool checks it against pbs/trainers.txt (+ trainers_trials.txt) and writes design/TRAINER_COVERAGE.md.

  python3 -I tools/trainer_gen/coverage.py            # print the summary, write design/TRAINER_COVERAGE.md
  python3 -I tools/trainer_gen/coverage.py --missing  # also print the missing species, one per line
  python3 -I tools/trainer_gen/coverage.py --no-write # don't touch the report
  python3 -I tools/trainer_gen/coverage.py --json     # machine-readable dump to stdout (species -> data)

Rules (keep them in step with the report header below):
- Species list: every [SPECIES] in the engine PBS (/home/claude/run/PBS/pokemon.txt, Gen 1-9, 1,025 species)
  minus those whose Flags hold Legendary, Mythical, UltraBeast or Paradox (that set already includes the
  sub-legendaries: Type: Null, Silvally, Kubfu, Urshifu, Cosmog, the Tapus, the Loyal Three, Ogerpon ...).
- A base species counts once, in any form. Regional forms (Alolan / Galarian / Hisuian / Paldean in
  pokemon_forms.txt FormName) are listed separately as a bonus ("Form = n" on a generic trainer's Pokemon).
- Generic trainer = a Standard version (version < 100) whose trainer type is a stock class (the base project's
  trainer_types.txt, minus POKEMONTRAINER_*, RIVAL1/2, LEADER_*, ELITEFOUR_*, CHAMPION, ROCKETBOSS, TEAMROCKET_*)
  or a rank-and-file villain/army class (HOLLOW_GRUNT*, MERIDIAN_AGENT*, ISENMAR_SOLDIER*, ISENMAR_OFFICER,
  ASHKAAR_SOLDIER*, ASHKAAR_OFFICER). Excluded as main cast / named story NPCs: RIVAL_*, LEADER_*, CHAMPION_*,
  MERIDIAN_<named> (Voss, Marchetti, Kroll, Quent, Ashe, Directorate, Admin), HOLLOW_<named> (admins, the Mourner,
  Thistle, Wick, Teo, Sable), FESTIVAL_*, ECHO_*, GILDED_*, ARCHSEER_*, OCTAVE_* (the Eevee Octave), REFLECTION,
  PARTNER_*, PLAYER_*, and the test-arena dummy (Map 990). Hard-only Pokemon (version +100) don't count: a
  Standard player never meets them.
- Level plausibility (a check, not a gate): a Pokemon reached by a level evolution should sit at or above that
  level (minus 2); one reached by a stone/trade/friendship evolution at 20+ (third stages 30+). A form that still
  evolves by level should sit no more than max(5, 30% of its evolution level) above it.
"""
import json
import os
import re
import sys
from collections import defaultdict, OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
ENGINE_PBS = "/home/claude/run/PBS"
BASE_TYPES_PBS = "/home/claude/ref/ebdx/PBS/trainer_types.txt"
TRAINERS = [os.path.join(ROOT, "pbs", "trainers.txt"), os.path.join(ROOT, "pbs", "trainers_trials.txt")]
REPORT = os.path.join(ROOT, "design", "TRAINER_COVERAGE.md")

FLAG_EXCLUDE = ("Legendary", "Mythical", "UltraBeast", "Paradox")
STOCK_EXCLUDE = re.compile(r"^(POKEMONTRAINER_|RIVAL\d|LEADER_|ELITEFOUR_|CHAMPION$|ROCKETBOSS$|TEAMROCKET_)")
ARMY = re.compile(r"^(HOLLOW_GRUNT(_[MF])?|MERIDIAN_AGENT(_[MF])?|ISENMAR_SOLDIER(_[MF])?|ISENMAR_OFFICER|"
                  r"ASHKAAR_SOLDIER(_[MF])?|ASHKAAR_OFFICER)$")
REGIONAL = ("Alolan", "Galarian", "Hisuian", "Paldean")
# Gen 9 evolutions the base pokemon.txt doesn't list (validate_trainers.MANUAL_PREVO): child -> (parent, min level)
MANUAL_EVO = {"KINGAMBIT": ("BISHARP", 64), "ANNIHILAPE": ("PRIMEAPE", 35), "FARIGIRAF": ("GIRAFARIG", 32),
              "DUDUNSPARCE": ("DUNSPARCE", 32), "URSALUNA": ("URSARING", 40), "WYRDEER": ("STANTLER", 31),
              "KLEAVOR": ("SCYTHER", 30), "SNEASLER": ("SNEASEL", 30), "OVERQWIL": ("QWILFISH", 30),
              "BASCULEGION": ("BASCULIN", 36)}
LEVEL_METHODS = ("Level", "Silcoon", "Cascoon", "Ninjask", "Shedinja", "AttackGreater", "DefenseGreater",
                 "AtkDefEqual")
# Placeholder or odd methods with a level-like param that isn't one (Gen 9 Pack "Level,100" walk/step evolutions)
FAKE_LEVEL = {("PAWMO", "PAWMOT"), ("BRAMBLIN", "BRAMBLEGHAST"), ("RELLOR", "RABSCA")}
PSEUDO_LEVEL = {"PAWMOT": 32, "BRAMBLEGHAST": 30, "RABSCA": 29}


def parse_pbs(path):
    """[ID] sections -> OrderedDict of key -> value (last wins)."""
    out = OrderedDict()
    cur = None
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            line = line.rstrip("\n")
            if line.startswith("["):
                cur = OrderedDict()
                out[line.strip()[1:-1]] = cur
            elif cur is not None and "=" in line and not line.lstrip().startswith("#"):
                k, _, v = line.partition("=")
                cur[k.strip()] = v.strip()
    return out


def load_species():
    raw = parse_pbs(os.path.join(ENGINE_PBS, "pokemon.txt"))
    sp = OrderedDict()
    for sid, d in raw.items():
        flags = d.get("Flags", "")
        sp[sid] = dict(name=d.get("Name", sid), gen=int(d.get("Generation", "0") or 0),
                       types=d.get("Types", "").split(","), flags=flags,
                       excluded=any(f in flags.split(",") for f in FLAG_EXCLUDE),
                       eggs=d.get("EggGroups", ""), evos=[], prevo=None, method=None, param=None,
                       bst=sum(int(x) for x in d.get("BaseStats", "0").split(",") if x.isdigit()))
        ev = d.get("Evolutions", "")
        parts = [p for p in ev.split(",") if p != ""] if ev else []
        for i in range(0, len(parts) - 1, 3):
            sp[sid]["evos"].append((parts[i], parts[i + 1], parts[i + 2] if i + 2 < len(parts) else ""))
    for sid, d in sp.items():
        for tgt, meth, prm in d["evos"]:
            if tgt in sp and sp[tgt]["prevo"] is None:
                sp[tgt].update(prevo=sid, method=meth, param=prm)
    for child, (par, lv) in MANUAL_EVO.items():
        if child in sp and sp[child]["prevo"] is None:
            sp[child].update(prevo=par, method="Level", param=str(lv))
            sp[par]["evos"].append((child, "Level", str(lv)))
    return sp


def is_baby(sp, sid):
    return "Undiscovered" in sp[sid]["eggs"] and sp[sid]["evos"] and \
        any("Undiscovered" not in sp.get(t, {}).get("eggs", "Undiscovered") for t, _, _ in sp[sid]["evos"])


def stage(sp, sid):
    n, cur = 1, sid
    while sp[cur]["prevo"] and not is_baby(sp, sp[cur]["prevo"]):
        n += 1
        cur = sp[cur]["prevo"]
    return n


def min_level(sp, sid):
    d = sp[sid]
    if sid in PSEUDO_LEVEL:
        return PSEUDO_LEVEL[sid]
    if not d["prevo"] or is_baby(sp, d["prevo"]):
        return 1 if sid != "LUCARIO" else 20
    if d["method"].startswith(LEVEL_METHODS) and d["param"].isdigit():
        return int(d["param"])
    base = min_level(sp, d["prevo"])
    return max(20, base + 8) if stage(sp, sid) <= 2 else max(30, base + 8)


def max_level(sp, sid):
    """Highest plausible level for a form that still evolves by level (None = no ceiling: final forms, and forms
    whose only way on is a stone, a trade or friendship)."""
    lv = []
    for tgt, meth, prm in sp[sid]["evos"]:
        if (sid, tgt) in FAKE_LEVEL:
            continue
        if meth.startswith(LEVEL_METHODS) and prm.isdigit():
            lv.append(int(prm))
    if not lv:
        return None
    e = min(lv)
    return e + max(5, int(round(e * 0.3)))


def regional_forms(sp):
    raw = parse_pbs(os.path.join(ENGINE_PBS, "pokemon_forms.txt"))
    out = []
    for key, d in raw.items():
        base, _, form = key.partition(",")
        fn = d.get("FormName", "")
        if base in sp and not sp[base]["excluded"] and any(fn.startswith(r) for r in REGIONAL) and form.isdigit():
            out.append((base, int(form), fn))
    return out


def generic_types():
    raw = parse_pbs(BASE_TYPES_PBS)
    return {t for t in raw if not STOCK_EXCLUDE.match(t)}


def parse_trainers(paths=TRAINERS):
    """-> list of dict(type, name, ver, note, mons=[(species, level, form)]) from every trainers file."""
    out = []
    for path in paths:
        if os.path.exists(path):
            out += parse_trainer_file(path)
    return out


def parse_trainer_file(path):
    out, cur, note = [], None, ""
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            s = line.rstrip("\n")
            if s.startswith("#") and not s.startswith("#---"):
                note = s[1:].strip()
                continue
            m = re.match(r"^\[([^,\]]+),([^\]]*?)(?:,(\d+))?\]\s*$", s)
            if m:
                cur = dict(type=m.group(1), name=m.group(2), ver=int(m.group(3) or 0), note=note, mons=[])
                out.append(cur)
                continue
            if cur is None:
                continue
            pm = re.match(r"^Pokemon\s*=\s*([A-Za-z0-9_]+)\s*,\s*(\d+)", s)
            if pm:
                cur["mons"].append([pm.group(1), int(pm.group(2)), 0])
                continue
            fm = re.match(r"^\s+Form\s*=\s*(\d+)", s)
            if fm and cur["mons"]:
                cur["mons"][-1][2] = int(fm.group(1))
    return out


def is_generic(t, gtypes):
    if t["ver"] >= 100:
        return False
    if "Map 990" in t["note"] or t["name"] == "Prismtest":
        return False
    return t["type"] in gtypes or bool(ARMY.match(t["type"]))


def analyse():
    sp = load_species()
    gtypes = generic_types()
    trainers = parse_trainers()
    gen = [t for t in trainers if is_generic(t, gtypes)]
    used = defaultdict(list)          # species -> [(type,name,ver,level)]
    used_forms = defaultdict(list)
    level_issues = []
    for t in gen:
        for s, lv, form in t["mons"]:
            used[s].append((t["type"], t["name"], t["ver"], lv))
            if form:
                used_forms[(s, form)].append((t["type"], t["name"], t["ver"], lv))
            if s not in sp:
                continue
            lo, hi = min_level(sp, s), max_level(sp, s)
            if lv < lo - 2 or (hi is not None and lv > hi):
                level_issues.append((t["type"], t["name"], t["ver"], s, lv, lo, hi))
    eligible = [s for s, d in sp.items() if not d["excluded"]]
    legend_used = sorted({s for s in used if s in sp and sp[s]["excluded"]})
    missing = [s for s in eligible if s not in used]
    regs = regional_forms(sp)
    segs = {}
    try:
        with open(os.path.join(ROOT, "design", "maps.json"), encoding="utf-8") as f:
            segs = {m["id"]: m.get("segment") for m in json.load(f)["maps"]}
    except (OSError, ValueError):
        pass
    by = defaultdict(lambda: [0, set()])
    for t in gen:
        m = re.match(r"Map (\d+)", t["note"])
        seg = segs.get(int(m.group(1))) if m else None
        by[seg][0] += 1
        if m and seg is not None:
            by[seg][1].add(int(m.group(1)))
    by_seg = [(k, (by[k][0], sorted(by[k][1]))) for k in sorted(by, key=lambda x: (x is None, x))]
    return dict(by_seg=by_seg, sp=sp, gen=gen, used=used, used_forms=used_forms, eligible=eligible, missing=missing,
                regs=regs, level_issues=level_issues, legend_used=legend_used)


def report(a):
    sp, used = a["sp"], a["used"]
    by_gen = defaultdict(lambda: [0, 0])
    for s in a["eligible"]:
        by_gen[sp[s]["gen"]][0] += 1
        if s in used:
            by_gen[sp[s]["gen"]][1] += 1
    tot = len(a["eligible"])
    cov = tot - len(a["missing"])
    L = ["# Generic-trainer species coverage",
         "",
         "Generated by `python3 -I tools/trainer_gen/coverage.py` from `pbs/trainers.txt` and `pbs/trainers_trials.txt`;",
         "don't edit by hand.",
         "",
         "**Reuben's rule (2026-11-24):** barring the main cast and NPCs, the game lets you battle every non-legendary,",
         "non-mythical species at least once in a trainer battle, placed where it makes sense (a class, region or field",
         "that fits it) and at a level where it plausibly exists in that form.",
         "",
         "**How it counts.** Species: the engine's `pokemon.txt` (Gen 1–9) minus every species flagged Legendary, Mythical,",
         "UltraBeast or Paradox (that already covers Type: Null/Silvally, Kubfu/Urshifu, Cosmog, the Tapus, the Loyal Three",
         "and Ogerpon). A species counts once in any form; regional forms are a bonus list. Generic trainers: Standard",
         "versions (< 100) of stock classes (Hiker, Fisherman, Ace Trainer ...) and the rank-and-file villain/army classes",
         "(Hollow grunts, Meridian agents, Isenmar/Ashkaar soldiers and captains). Not counted: rivals, Wardens, the",
         "Champion, named admins (Hollow/Meridian), the Festival, Echo, Gilded, Archseer, the Eevee Octave, partners,",
         "Hard-only Pokémon and the Map 990 test dummy.",
         "",
         "## Totals",
         "",
         "| | Count |",
         "|---|---|",
         "| Eligible species | %d |" % tot,
         "| Covered by a generic trainer | **%d** (%.1f%%) |" % (cov, 100.0 * cov / tot),
         "| Missing | %d |" % len(a["missing"]),
         "| Generic trainers (Standard versions) | %d |" % len(a["gen"]),
         "| Legendary/Mythical/UB/Paradox on a generic trainer (must be 0) | %d%s |" % (
             len(a["legend_used"]), (" — " + ", ".join(a["legend_used"])) if a["legend_used"] else ""),
         "| Level-plausibility flags | %d |" % len(a["level_issues"]),
         "",
         "## By generation",
         "",
         "| Gen | Eligible | Covered | Missing |",
         "|---|---|---|---|"]
    for g in sorted(by_gen):
        e, c = by_gen[g]
        L.append("| %d | %d | %d | %d |" % (g, e, c, e - c))
    L += ["", "## Generic trainers by stretch (density floor: 12–20 route, gym and dungeon trainers per chapter)", "",
          "Counted from the `# Map NNN` note above each block and that map's `segment` (badges held) in",
          "`design/maps.json`; chapter = segment + 2 from Ch3 on (segment 0 is Ch1–2).", "",
          "| Badges held | Chapter | Generic trainers | Maps |", "|---|---|---|---|"]
    for seg, (n, mids) in a["by_seg"]:
        ch = "—" if seg is None else "1–2" if seg == 0 else str(seg + 2)
        L.append("| %s | %s | %d | %s |" % ("—" if seg is None else seg, ch, n,
                                           ", ".join(str(m) for m in mids) if mids else "no map note (story-placed grunts, soldiers, Trials)"))
    L += ["", "## Missing species", ""]
    if not a["missing"]:
        L.append("None: every eligible species is on a generic trainer.")
    else:
        bg = defaultdict(list)
        for s in a["missing"]:
            bg[sp[s]["gen"]].append(s)
        for g in sorted(bg):
            L.append("- **Gen %d** (%d): %s" % (g, len(bg[g]), ", ".join(bg[g])))
    L += ["", "## Regional forms (bonus)", ""]
    have = [(b, f, n) for b, f, n in a["regs"] if (b, f) in a["used_forms"]]
    L.append("%d of %d regional forms are on a generic trainer." % (len(have), len(a["regs"])))
    L.append("")
    if have:
        L.append("- Covered: " + ", ".join("%s %s" % (n, sp[b]["name"]) for b, f, n in have))
    miss = [(b, f, n) for b, f, n in a["regs"] if (b, f) not in a["used_forms"]]
    if miss:
        L.append("- Not yet: " + ", ".join("%s %s" % (n, sp[b]["name"]) for b, f, n in miss))
    L += ["", "## Level-plausibility flags", ""]
    if not a["level_issues"]:
        L.append("None.")
    else:
        L.append("| Trainer | Pokémon | Lv | Plausible from | Plausible to |")
        L.append("|---|---|---|---|---|")
        for tt, nm, v, s, lv, lo, hi in a["level_issues"]:
            L.append("| %s,%s,%d | %s | %d | %d | %s |" % (tt, nm, v, s, lv, lo, hi if hi else "—"))
    return "\n".join(L) + "\n", cov, tot


def main():
    a = analyse()
    text, cov, tot = report(a)
    if "--json" in sys.argv:
        sp = a["sp"]
        print(json.dumps({s: dict(name=sp[s]["name"], gen=sp[s]["gen"], types=sp[s]["types"], bst=sp[s]["bst"],
                                  stage=stage(sp, s), min=min_level(sp, s), max=max_level(sp, s),
                                  prevo=sp[s]["prevo"], covered=s in a["used"], excluded=sp[s]["excluded"])
                              for s in sp}, indent=0))
        return
    if "--no-write" not in sys.argv:
        with open(REPORT, "w", encoding="utf-8") as f:
            f.write(text)
    print("coverage: %d / %d eligible species (%.1f%%), %d missing; %d generic trainers; %d legendary on generic; "
          "%d level flags" % (cov, tot, 100.0 * cov / tot, tot - cov, len(a["gen"]), len(a["legend_used"]),
                              len(a["level_issues"])))
    if "--missing" in sys.argv:
        for s in a["missing"]:
            print(s)
    if "--levels" in sys.argv:
        for row in a["level_issues"]:
            print(row)


if __name__ == "__main__":
    main()
