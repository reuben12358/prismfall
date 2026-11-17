#!/usr/bin/env python3
"""Cross-checks every trainer the generated maps battle against the PBS trainer data.

    python3 -I tools/validate_map_trainers.py [--maps maps_out/Data] [--pbs pbs] [--base-pbs DIR] [--strict]

A trainer missing from PBS crashes the game when its battle starts (Debug mode offers to create it). Scans the event
script text of every Map*.rxdata (bytes only, never deserialized) for:
  TrainerBattle.start(:TYPE, "Name"[, v] ...)    every :TYPE, "Name"[, v] pair, and [:TYPE, "Name"(, v)] arrays
  Prismfall.cameo_battle(:TYPE, "Name"[, v])
  Prismfall.rival_battle(:TYPE, "Name", n)       versions n*10 + slot, slot 0-2 (Core's rival starter scheme)
  Prismfall.gym_battle(n)                        the Warden in Core's GYMS table (001_Config.rb)
  pbTrainerIntro(:TYPE)                          the trainer type must exist
and checks them against pbs/trainers*.txt + maps_out/PBS (ours) and the base project's PBS/trainers*.txt (stock
trainers are fine to use). ERROR: a battled trainer or a trainer type that doesn't exist. WARNING: one of our trainers
lacks its Hard (+100) or Casual (+200) variant (Core then falls back to the Standard team), or a map battles a stock
sample trainer. --strict turns warnings into errors. Exit status 1 on errors.
"""
import argparse
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_BASE = "/home/claude/ref/ebdx_renovation/PBS"

PAT_CALL = re.compile(rb'(?:TrainerBattle\.start|cameo_battle)\(([^)]{0,300})\)')
PAT_PAIR = re.compile(rb':([A-Z][A-Z0-9_]+)\s*,\s*"([^"]+)"(?:\s*,\s*(\d+))?')
PAT_ARR = re.compile(rb'\[:([A-Z][A-Z0-9_]+)\s*,\s*"([^"]+)"(?:\s*,\s*(\d+))?')
PAT_RIVAL = re.compile(rb'rival_battle\(:([A-Z][A-Z0-9_]+)\s*,\s*"([^"]+)"\s*,\s*(\d+)')
PAT_GYM = re.compile(rb'gym_battle\((\d+)')
PAT_INTRO = re.compile(rb'pbTrainerIntro\(:([A-Z][A-Z0-9_]+)')


def pbs_files(d, base):
    if not d or not os.path.isdir(d):
        return []
    return sorted(glob.glob(os.path.join(d, base + ".txt")) + glob.glob(os.path.join(d, base + "_*.txt")))


def read_trainers(files):
    keys = set()
    for f in files:
        for line in open(f, encoding="utf-8-sig"):
            m = re.match(r'\[([A-Z0-9_]+),([^,\]]+)(?:,(\d+))?\]\s*$', line.strip())
            if m:
                keys.add((m.group(1), m.group(2), int(m.group(3) or 0)))
    return keys


def read_types(files):
    types = set()
    for f in files:
        for line in open(f, encoding="utf-8-sig"):
            m = re.match(r'\[([A-Z0-9_]+)\]\s*$', line.strip())
            if m:
                types.add(m.group(1))
    return types


def read_gyms(core_dir):
    """{n: (type, name, version or None, rival battle number or None)} from Core's GYMS table."""
    gyms = {}
    for f in glob.glob(os.path.join(core_dir, "*.rb")):
        for line in open(f, encoding="utf-8"):
            m = re.search(r'index:\s*(\d+).*?trainer_name:\s*"([^"]+)".*?trainer_type:\s*:([A-Z0-9_]+)', line)
            if not m:
                continue
            ver = re.search(r'\bversion:\s*(\d+)', line)
            rival = re.search(r'rival_battle:\s*(\d+)', line)
            gyms[int(m.group(1))] = (m.group(3), m.group(2), int(ver.group(1)) if ver else 0,
                                     int(rival.group(1)) if rival else None)
    return gyms


def scan_map(data, gyms):
    """-> (set of (type, name, version, how), set of intro types)"""
    found, intros = set(), set()
    dec = lambda b: b.decode("utf-8", "replace")
    for m in PAT_CALL.finditer(data):
        for p in PAT_PAIR.finditer(m.group(1)):
            found.add((dec(p.group(1)), dec(p.group(2)), int(p.group(3) or 0), "battle"))
    for p in PAT_ARR.finditer(data):
        found.add((dec(p.group(1)), dec(p.group(2)), int(p.group(3) or 0), "battle"))
    for p in PAT_RIVAL.finditer(data):
        for slot in (0, 1, 2):
            found.add((dec(p.group(1)), dec(p.group(2)), int(p.group(3)) * 10 + slot, "rival battle %s" % dec(p.group(3))))
    for p in PAT_GYM.finditer(data):
        n = int(p.group(1))
        g = gyms.get(n)
        if g is None:
            found.add(("?", "gym %d" % n, 0, "gym battle with no GYMS entry"))
        elif g[3] is not None:
            for slot in (0, 1, 2):
                found.add((g[0], g[1], g[3] * 10 + slot, "gym %d (rival-versioned)" % n))
        else:
            found.add((g[0], g[1], g[2], "gym %d" % n))
    for p in PAT_INTRO.finditer(data):
        intros.add(dec(p.group(1)))
    return found, intros


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--maps", default=os.path.join(ROOT, "maps_out", "Data"))
    ap.add_argument("--pbs", default=os.path.join(ROOT, "pbs"))
    ap.add_argument("--base-pbs", default=DEFAULT_BASE if os.path.isdir(DEFAULT_BASE) else None,
                    help="the base project's PBS folder (stock trainers and trainer types)")
    ap.add_argument("--core", default=os.path.join(ROOT, "plugins", "Prismfall Core"))
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()

    ours = read_trainers(pbs_files(a.pbs, "trainers") + pbs_files(os.path.join(ROOT, "maps_out", "PBS"), "trainers"))
    stock = read_trainers(pbs_files(a.base_pbs, "trainers"))
    types = read_types(pbs_files(a.pbs, "trainer_types") + pbs_files(a.base_pbs, "trainer_types"))
    gyms = read_gyms(a.core)
    if not a.base_pbs:
        print("note: no base project PBS given (--base-pbs): stock trainers/types count as missing")
    errors, warnings, checked = [], [], 0
    for path in sorted(glob.glob(os.path.join(a.maps, "Map*.rxdata"))):
        fn = os.path.basename(path)
        found, intros = scan_map(open(path, "rb").read(), gyms)
        for tt in sorted(intros):
            if tt not in types:
                errors.append("%s: pbTrainerIntro(:%s) - no such trainer type" % (fn, tt))
        for tt, name, ver, how in sorted(found):
            checked += 1
            label = "[%s,%s%s] (%s)" % (tt, name, "" if ver == 0 else ",%d" % ver, how)
            if tt not in types:
                errors.append("%s: %s - no such trainer type" % (fn, label))
            if (tt, name, ver) in ours:
                for extra, mode in ((100, "Hard"), (200, "Casual")):
                    if ver < 100 and (tt, name, ver + extra) not in ours:
                        warnings.append("%s: %s has no %s variant (version %d)" % (fn, label, mode, ver + extra))
            elif (tt, name, ver) in stock:
                warnings.append("%s: %s is a base-project sample trainer" % (fn, label))
            else:
                errors.append("%s: %s is not in the PBS trainer data" % (fn, label))
    for w in warnings:
        print("WARNING", w)
    for e in errors:
        print("ERROR  ", e)
    if a.strict:
        errors += warnings
    print("%d battle reference(s) in %d map(s): %d error(s), %d warning(s)"
          % (checked, len(glob.glob(os.path.join(a.maps, "Map*.rxdata"))), len(errors), len(warnings)))
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
