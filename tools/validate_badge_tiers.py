#!/usr/bin/env python3
"""
Prismfall badge-tier overlay validator  (python3 -I tools/validate_badge_tiers.py)

Checks pbs/encounters_badgetiers.txt (overlays read by plugins/Prismfall Trials/007_Trials_BadgeTiers.rb):
  * the v21.1 compiler's syntax rules (same parser as tools/validate_encounters.py)
  * species/forms exist (base project PBS), encounter types exist
  * version = 100 * (encounter_version + 1) + badges, badges 1-18
  * levels: max <= level cap while holding that many badges; min >= 1
  * rods / Surf / Rock Smash unlocks (an overlay can't use a method the player can't have yet)
  * the map exists in design/maps.json; the map is reached BEFORE the badge (else the tier is pointless)
  * the base table (pbs/encounters.txt) has the encounter type, or a step chance is given (warning)
  * evolved species no earlier than their evolution level - tolerance (warning)
  * every overlay section has a rumour in 140_BadgeTier_Rumours.rb (warning)
Exit 1 on errors (or warnings with --strict).
"""
import argparse, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import validate_encounters as VE   # noqa: E402  (shared parsers and design constants)

# maps.json `segment` (badges held when a map is first reachable) is authoritative since
# SPINE Revision 14 (WORLD.md section 2). Overrides for maps whose gate is a field move:
FIRST_REACH = {
    525: 2, 548: 2,   # Gossamer Deepwood / Cocoonfall Hollow: Cut needs 2 badges (BADGE_FOR_CUT = 2, Rev 14)
}
RUMOUR_FILE = os.path.join(ROOT, "plugins", "Prismfall Trials", "140_BadgeTier_Rumours.rb")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default=os.path.join(ROOT, "pbs", "encounters_badgetiers.txt"))
    ap.add_argument("--base", default=os.path.join(ROOT, "pbs", "encounters.txt"))
    ap.add_argument("--pbs", default="/home/claude/ref/ebdx/PBS")
    ap.add_argument("--scripts", default="/home/claude/ref/essentials/Data/Scripts")
    ap.add_argument("--maps", default=os.path.join(ROOT, "design", "maps.json"))
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--summary", action="store_true")
    a = ap.parse_args()

    errors, warnings = [], []
    species, prevo = VE.parse_species(a.pbs)
    enc_types = VE.parse_enc_types(a.scripts)
    maxlv = VE.max_level(a.scripts)
    tiers = VE.parse_encounters(a.file, enc_types, errors)
    base_errs = []
    base = VE.parse_encounters(a.base, enc_types, base_errs)
    maps = {m["id"]: m for m in json.load(open(a.maps, encoding="utf-8"))["maps"]}
    rumours = set()
    if os.path.isfile(RUMOUR_FILE):
        for m in re.finditer(r"\[(\d+),\s*(\d+)\]\s*=>", open(RUMOUR_FILE, encoding="utf-8").read()):
            rumours.add((int(m.group(1)), int(m.group(2))))

    def evo_level(sp):
        p = prevo.get(sp)
        if not p: return None
        meth, par = p[1], p[2]
        if meth == "Level" or meth in VE.LEVEL_METHODS:
            try: return int(par)
            except ValueError: return None
        return VE.NONLEVEL_EVO_MIN

    slots = 0
    for (mid, ver), sec in tiers.items():
        where = f"[{mid},{ver}]"
        enc_version, badges = divmod(ver, 100)
        enc_version -= 1
        if ver < 100 or not (1 <= badges <= 18) or enc_version < 0:
            errors.append(f"{where}: version must be 100*(encounter_version+1)+badges (badges 1-18), got {ver}")
            continue
        if mid not in maps:
            errors.append(f"{where}: map {mid} is not in maps.json")
        seg = maps.get(mid, {}).get("segment")
        reach = FIRST_REACH.get(mid, seg if isinstance(seg, int) else VE.segment_from_id(mid))
        if reach >= badges:
            warnings.append(f"{where}: map is first reached with {reach} badges, so a tier at {badges} is never a revisit")
        if (mid, badges) not in rumours:
            warnings.append(f"{where}: no rumour in 140_BadgeTier_Rumours.rb")
        cap = VE.cap_for(badges)
        base_sec = base.get((mid, enc_version)) or base.get((mid, 0))
        if not base_sec:
            warnings.append(f"{where}: map {mid} has no base table in pbs/encounters.txt yet (overlay waits for it)")
        for etype, lst in sec["types"].items():
            need = VE.base_unlock(etype)
            if badges < need:
                errors.append(f"{where} {etype}: needs {need} badges (rod/HM unlock) but the tier opens at {badges}")
            if base_sec and etype not in base_sec["types"] and etype not in sec["steps"]:
                warnings.append(f"{where} {etype}: the base table has no {etype}; give a step chance ('{etype},N') or check it")
            for (w, sp, lo, hi, no) in lst:
                slots += 1
                if sp not in species:
                    errors.append(f"L{no} {where}: unknown species {sp}"); continue
                if not (1 <= lo <= hi <= maxlv):
                    errors.append(f"L{no} {where}: bad levels {lo}-{hi}")
                if hi > cap:
                    errors.append(f"L{no} {where}: {sp} Lv{hi} is over the {badges}-badge cap {cap}")
                if w > 10:
                    warnings.append(f"L{no} {where}: weight {w} is not rare (overlays should be 2-6)")
                if any(f in species[sp]["flags"] for f in VE.SPECIAL_FLAGS):
                    errors.append(f"L{no} {where}: {sp} is legendary/mythical")
                el = evo_level(sp)
                if el and lo < el - VE.EVO_TOLERANCE:
                    warnings.append(f"L{no} {where}: {sp} at Lv{lo} but evolves in at Lv{el}")
    if a.summary:
        for (mid, ver), sec in tiers.items():
            print(f"[{mid},{ver}] {sec['name']}: " + "; ".join(
                f"{t}: " + ", ".join(f"{s}{lo}-{hi}({w})" for (w, s, lo, hi, _n) in l) for t, l in sec["types"].items()))
    for e in errors: print("ERROR  ", e)
    for w in warnings: print("WARNING", w)
    print(f"{len(tiers)} overlay sections, {slots} slots, {len(errors)} errors, {len(warnings)} warnings")
    sys.exit(1 if errors or (a.strict and warnings) else 0)


if __name__ == "__main__":
    main()
