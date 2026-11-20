#!/usr/bin/env python3
"""
Prismfall encounters validator  (run with:  python3 -I tools/validate_encounters.py)

Checks pbs/encounters.txt the way the Essentials v21.1 compiler would
(compile_encounters in 021_Compiler/002_Compiler_CompilePBS.rb) and against the
World design rules:
  * syntax: map headers, encounter-type lines, "weight,SPECIES,min[,max]" slots
  * encounter types  <- GameData::EncounterType.register in the core scripts
  * species / forms  <- base project PBS (Gen 1-9): pokemon.txt, pokemon_forms.txt
  * levels 1..MAXIMUM_LEVEL, min <= max, duplicate [map,version]
  * design: level caps per badge count (map segment from design/maps.json, plus
    HM/rod unlocks per encounter type), evolution-level sanity, weight sums,
    time-of-day variants without a base type, legendaries in wild tables,
    kingdom type share (~70%) for kingdom maps.
Usage:
  python3 -I tools/validate_encounters.py [--summary] [--strict]
      [--file pbs/encounters.txt] [--pbs /home/claude/ref/ebdx/PBS]
      [--scripts /home/claude/ref/essentials/Data/Scripts] [--maps design/maps.json]
Exit 1 on errors (or on warnings with --strict). Pure standard library.
"""
import argparse, json, os, re, sys
from collections import defaultdict, OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# ---- design config (mirror of design/WORLD.md) ------------------------------
GYM_CAPS = [15, 19, 23, 27, 31, 35, 39, 43, 47, 51, 55, 59, 63, 67, 71, 75, 80, 85]
FESTIVAL_CAP, POSTGAME_CAP, POSTGAME_SEG = 90, 100, 19
UNLOCK = {"OldRod": 0, "GoodRod": 3, "SuperRod": 10, "RockSmash": 2, "Water": 6}  # badges
VERSION_MIN_BADGES = {1: 12, 3: POSTGAME_SEG}   # 1 = Bleed-spread (Act IV+), 2 = Ruin Route, 3 = postgame
KINGDOM_TYPES = {"Elowen": {"FAIRY", "GRASS", "BUG", "NORMAL"}, "Antumbra": {"GHOST", "PSYCHIC", "DARK"},
                 "Isenmar": {"WATER", "ICE"}, "Ashkaar": {"FIRE", "DRAGON"}, "Ossaria": {"GROUND", "ROCK"},
                 "Zenith": {"ELECTRIC", "STEEL", "FLYING"}, "Nadir": {"POISON", "DARK", "FIGHTING"}}
KINGDOM_SHARE_MIN = 65
EVO_TOLERANCE = 5           # wild evolved form may appear this many levels before its evo level
NONLEVEL_EVO_MIN = 20       # stone/trade/happiness evolutions shouldn't appear wild below this
LEVEL_METHODS = {"AttackGreater", "DefenseGreater", "AtkDefEqual", "Silcoon", "Cascoon", "Ninjask", "Shedinja"}
SPECIAL_FLAGS = ("Legendary", "Mythical", "UltraBeast")


def cap_for(badges):
    if badges is None: return POSTGAME_CAP
    if badges >= POSTGAME_SEG: return POSTGAME_CAP
    if badges >= 18: return FESTIVAL_CAP
    return GYM_CAPS[badges]


# SPINE Rev 14 (design/SWAP_GYM1_GYM2.md §0): Act I maps whose segment no longer follows from their ID block.
# Optional gym wings and the Gossamer side maps open after Badge 2; Gossamer Wood itself is on the Ch3 road.
ACT1_SEGMENTS = {132: 2, 133: 1, 134: 2,            # Loomhouse Upper Lofts (optional, after Badge 2); 133 the Spindle
                 151: 2, 152: 2, 153: 2,            # Pell Playhouse Backstage, D9 (after Badge 2)
                 524: 1, 526: 1,                    # Gossamer Wood, Woodward's Hut (Weavers' Road, Ch3)
                 525: 2, 548: 2}                    # Gossamer Deepwood (Cut), Cocoonfall Hollow


def segment_from_id(mid):
    """Fallback for maps missing from maps.json (it reads `segment` first)."""
    if mid in ACT1_SEGMENTS: return ACT1_SEGMENTS[mid]
    # Saltmere (140-159) holds Gym 1 and Briarwick (120-139) Gym 2, so the two Act I blocks swap relative to the
    # ID scheme below.
    if 120 <= mid < 140: return 1
    if 140 <= mid < 160: return 0
    if 100 <= mid < 480: return max(0, (mid - 100) // 20 - 1)
    if 480 <= mid < 520: return 18
    if 520 <= mid < 900: return (mid - 520) // 20
    return POSTGAME_SEG


# ---- reference parsing -------------------------------------------------------
def parse_species(pbs):
    sp, cur = {}, None
    def evo_add(cur, parts):
        for i in range(0, len(parts) - 1, 3):
            tgt, meth = parts[i], parts[i + 1]
            par = parts[i + 2] if i + 2 < len(parts) else ""
            sp[cur]["evos"].append((tgt, meth, par))
    for path, is_form in ((os.path.join(pbs, "pokemon.txt"), False), (os.path.join(pbs, "pokemon_forms.txt"), True)):
        with open(path, encoding="utf-8-sig") as f:
            for line in f:
                line = line.split("#")[0].strip() if not line.lstrip().startswith("Pokedex") else line.strip()
                m = re.match(r"^\[\s*([A-Za-z0-9_]+)\s*(?:,\s*(\d+))?\s*\]$", line)
                if m:
                    cur = m.group(1) + ("_" + m.group(2) if m.group(2) and m.group(2) != "0" else "")
                    base = sp.get(m.group(1), {})
                    sp[cur] = {"types": list(base.get("types", [])), "flags": base.get("flags", ""), "evos": [],
                               "base": m.group(1), "bst": base.get("bst", 0)}
                    continue
                if not cur or "=" not in line: continue
                k, v = [x.strip() for x in line.split("=", 1)]
                if k == "Types": sp[cur]["types"] = [t.strip() for t in v.split(",")]
                elif k == "Flags": sp[cur]["flags"] = v
                elif k == "BaseStats": sp[cur]["bst"] = sum(int(x) for x in v.split(","))
                elif k in ("Evolution", "Evolutions"): evo_add(cur, [x.strip() for x in v.split(",")])
    prevo = {}
    for s, d in sp.items():
        for (tgt, meth, par) in d["evos"]:
            prevo.setdefault(tgt, (d["base"], meth, par))
    return sp, prevo


def parse_enc_types(scripts):
    types = {}
    for dp, _, fs in os.walk(scripts):
        for fn in fs:
            if not fn.endswith(".rb"): continue
            txt = open(os.path.join(dp, fn), encoding="utf-8", errors="replace").read()
            for blk in re.findall(r"GameData::EncounterType\.register\(\{(.*?)\}\)", txt, re.S):
                i = re.search(r":id\s*=>\s*:(\w+)", blk)
                t = re.search(r":type\s*=>\s*:(\w+)", blk)
                c = re.search(r":trigger_chance\s*=>\s*(\d+)", blk)
                if i: types[i.group(1)] = (t.group(1) if t else "none", int(c.group(1)) if c else 0)
    return types


def max_level(scripts):
    p = os.path.join(scripts, "001_Settings.rb")
    try:
        m = re.search(r"MAXIMUM_LEVEL\s*=\s*(\d+)", open(p, encoding="utf-8").read())
        return int(m.group(1)) if m else 100
    except OSError:
        return 100


# ---- encounters parsing (mirrors compile_encounters) ------------------------
def parse_encounters(path, enc_types, errors):
    maps, cur, ctype = OrderedDict(), None, None
    with open(path, "rb") as f:
        raw = f.read()
    if raw.startswith(b"\xef\xbb\xbf"): raw = raw[3:]
    for no, line in enumerate(raw.decode("utf-8").splitlines(), 1):
        comment = line.split("#", 1)[1].strip() if "#" in line else ""
        line = re.sub(r"\s*#.*$", "", line).strip()
        if not line: continue
        if ctype and re.match(r"^\d+,", line):
            v = [x.strip() for x in line.split(",")]
            if len(v) < 3 or len(v) > 4:
                errors.append(f"L{no}: slot needs 3-4 fields: {line}"); continue
            if not all(re.match(r"^\d+$", x) for x in [v[0], v[2]] + v[3:]):
                errors.append(f"L{no}: weight/levels must be positive integers: {line}"); continue
            w, s, lo = int(v[0]), v[1], int(v[2]); hi = int(v[3]) if len(v) > 3 else lo
            cur["types"][ctype].append((w, s, lo, hi, no))
        elif re.match(r"^\[\s*(.+)\s*\]$", line):
            vals = [x.strip() for x in re.match(r"^\[\s*(.+)\s*\]$", line).group(1).split(",")]
            if not all(re.match(r"^\d+$", x) for x in vals) or len(vals) > 2:
                errors.append(f"L{no}: bad map header {line}"); cur = None; ctype = None; continue
            key = (int(vals[0]), int(vals[1]) if len(vals) > 1 else 0)
            if key in maps: errors.append(f"L{no}: encounters for map {key} defined twice")
            cur = {"name": comment, "types": OrderedDict(), "steps": {}, "line": no}
            maps[key] = cur; ctype = None
        elif cur is None:
            errors.append(f"L{no}: expected a map header, got {line!r}")
        else:
            v = [x.strip() for x in line.split(",")]
            if v[0] not in enc_types:
                errors.append(f"L{no}: undefined encounter type {v[0]!r} (map {list(maps)[-1]})"); ctype = None; continue
            ctype = v[0]
            if len(v) > 1 and v[1]:
                if not re.match(r"^\d+$", v[1]) or int(v[1]) == 0:
                    errors.append(f"L{no}: step chance must be a positive integer: {line}")
                cur["steps"][ctype] = v[1]
            cur["types"][ctype] = []
    return maps


def base_unlock(etype):
    for k, b in UNLOCK.items():
        if etype.startswith(k): return b
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default=os.path.join(ROOT, "pbs", "encounters.txt"))
    ap.add_argument("--pbs", default="/home/claude/ref/ebdx/PBS")
    ap.add_argument("--scripts", default="/home/claude/ref/essentials/Data/Scripts")
    ap.add_argument("--maps", default=os.path.join(ROOT, "design", "maps.json"))
    ap.add_argument("--summary", action="store_true")
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()
    errors, warns = [], []
    sp, prevo = parse_species(a.pbs)
    enc_types = parse_enc_types(a.scripts)
    if not enc_types: print("FATAL: no encounter types found in", a.scripts); return 2
    maxlv = max_level(a.scripts)
    mapinfo = {}
    if os.path.exists(a.maps):
        for m in json.load(open(a.maps, encoding="utf-8"))["maps"]: mapinfo[m["id"]] = m
    else:
        warns.append(f"maps.json not found ({a.maps}); using ID-scheme segments only")
    maps = parse_encounters(a.file, enc_types, errors)

    first_seen = {}   # base family -> (segment, map)
    def family_root(s):
        b = sp[s]["base"] if s in sp else s
        seen = set()
        while b in prevo and b not in seen:
            seen.add(b); b = prevo[b][0]
        return b

    for (mid, ver), m in maps.items():
        tag = f"[{mid}{','+str(ver) if ver else ''}] {m['name']}"
        info = mapinfo.get(mid)
        if mid < 100 or mid > 999: errors.append(f"{tag}: map ID outside 100-999 (sample maps end at 075)")
        if not m["name"]: warns.append(f"{tag}: header has no '# Map name' comment")
        if info is None and mapinfo: warns.append(f"{tag}: map ID not in maps.json")
        elif info and info.get("name") and m["name"] and not m["name"].startswith(info["name"].split(" - ")[0][:10]):
            warns.append(f"{tag}: comment name differs from maps.json name {info['name']!r}")
        seg = info.get("segment") if info else segment_from_id(mid)
        if info and info.get("postgame"): seg = POSTGAME_SEG
        if ver in VERSION_MIN_BADGES and seg is not None: seg = max(seg, VERSION_MIN_BADGES[ver])
        names = set(m["types"])
        for t in names:
            for suf in ("Day", "Night", "Morning", "Afternoon", "Evening"):
                if t.endswith(suf) and t[:-len(suf)] not in names and t[:-len(suf)] in enc_types:
                    warns.append(f"{tag}: {t} without base {t[:-len(suf)]} (no encounters at other times)")
        for t, slots in m["types"].items():
            if not slots: warns.append(f"{tag} {t}: empty table"); continue
            tot = sum(s[0] for s in slots)
            if tot != 100: warns.append(f"{tag} {t}: weights sum to {tot}, not 100")
            eff = None if seg is None else max(seg, base_unlock(t))
            cap = cap_for(eff)
            kshare, kdenom = 0, 0
            ktypes = KINGDOM_TYPES.get(info.get("kingdom")) if info else None
            for (w, s, lo, hi, no) in slots:
                if s not in sp:
                    errors.append(f"L{no} {tag} {t}: undefined species {s}"); continue
                if lo < 1 or hi > maxlv: errors.append(f"L{no} {tag}: level {lo}-{hi} outside 1-{maxlv}")
                if lo > hi: errors.append(f"L{no} {tag}: min level {lo} > max {hi}")
                if hi > cap and not (info and info.get("allow_over_cap")):
                    errors.append(f"L{no} {tag} {t}: {s} Lv{hi} exceeds cap {cap} (badges {eff})")
                fl = sp[s]["flags"]
                if any(x in fl for x in SPECIAL_FLAGS):
                    warns.append(f"L{no} {tag}: {s} is {fl}; use a static event, not a wild table")
                if "Paradox" in fl and (seg is None or seg < POSTGAME_SEG):
                    warns.append(f"L{no} {tag}: Paradox {s} before postgame")
                pv = prevo.get(sp[s]["base"]) or prevo.get(s)
                if pv:
                    meth, par = pv[1], pv[2]
                    if par == "100" and meth == "Level":
                        pass   # Gen 9 Pack placeholder (Pawmot/Brambleghast/Rabsca): real method is scripted
                    elif (meth.startswith("Level") or meth in LEVEL_METHODS) and par.isdigit():
                        if lo < int(par) - EVO_TOLERANCE:
                            warns.append(f"L{no} {tag}: {s} at Lv{lo} but evolves from {pv[0]} at {par}")
                    elif lo < NONLEVEL_EVO_MIN:
                        warns.append(f"L{no} {tag}: {s} ({meth} evolution) wild at Lv{lo}")
                if ktypes and (t.startswith("Land") or t.startswith("Cave")):
                    kdenom += w
                    if set(sp[s]["types"]) & ktypes: kshare += w
                fam = family_root(s)
                key = eff if eff is not None else 99
                if fam not in first_seen or key < first_seen[fam][0]: first_seen[fam] = (key, mid, s)
            if kdenom and not info.get("wild_theme_exempt") and 100 * kshare // kdenom < KINGDOM_SHARE_MIN:
                warns.append(f"{tag} {t}: only {100*kshare//kdenom}% {info['kingdom']}-type (target ~70)")

    for e in errors: print("ERROR  ", e)
    for w in warns: print("WARN   ", w)
    if a.summary:
        print("\n## Families first available, by badges held\n")
        byseg = defaultdict(list)
        for fam, (seg, mid, s) in first_seen.items(): byseg[seg].append(fam)
        for seg in sorted(byseg):
            print(f"- **{seg if seg != POSTGAME_SEG else 'PG'}** ({len(byseg[seg])}): " + ", ".join(sorted(byseg[seg])))
        print("\n## Families with a member of each type, cumulative (s0 / s4 / s8 / s12 / s18)\n")
        alltypes = sorted({t for d in sp.values() for t in d["types"]} - {"QMARKS"})
        def fam_types(fam):
            out, stack = set(), [fam]
            while stack:
                x = stack.pop(); out |= set(sp.get(x, {}).get("types", []))
                stack += [e[0] for e in sp.get(x, {}).get("evos", [])]
            return out
        for t in alltypes:
            row = [sum(1 for f, (sg, _, _) in first_seen.items() if sg <= c and t in fam_types(f)) for c in (0, 4, 8, 12, 18)]
            print(f"- {t}: " + " / ".join(map(str, row)))
        roots = {family_root(s) for s, d in sp.items() if "_" not in s and not any(x in d["flags"] for x in SPECIAL_FLAGS + ("Paradox",))}
        miss = sorted(roots - set(first_seen))
        print(f"\n## Non-legendary families with no wild slot ({len(miss)}): gifts/statics must cover these\n")
        print(", ".join(miss))
    print(f"\n{len(maps)} encounter tables, {len(errors)} errors, {len(warns)} warnings")
    return 1 if errors or (a.strict and warns) else 0


if __name__ == "__main__":
    sys.exit(main())
