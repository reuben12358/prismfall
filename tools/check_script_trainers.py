#!/usr/bin/env python3
"""List every trainer a story script or a map layout calls for and check it against pbs/trainers.txt.

  python3 -I tools/check_script_trainers.py                       # Ch16-21 + post-game scripts + mapgen/layouts/*.py
  python3 -I tools/check_script_trainers.py story/36_SCRIPT_CH17.md mapgen/layouts/war.py
  python3 -I tools/check_script_trainers.py --all                 # every story/2*-4*_SCRIPT_*.md + the layouts
  python3 -I tools/check_script_trainers.py --quiet               # only the missing ones

It reads these forms (anywhere in the text, so "BATTLE:" and "Script:" lines and tables are all covered):
  TrainerBattle.start(:TYPE, "Name"[, ver][, :TYPE2, "Name2"[, ver2]])
  pbRegisterPartner(:TYPE, "Name"[, ver])
  Prismfall.rival_battle(:TYPE, "Name", n ...)        -> versions n*10 + 0/1/2
  ... Prismfall::Rival.version_for(n) / partner_version(n) as a version   -> every starter slot
  Prismfall.gym_battle(n)                               -> the Warden (Gym 9 = LEADER_JUNO 30/31/32)
  [TYPE,Name] / [TYPE,Name,ver] in backticks            (PBS keys quoted in prose)
For each base version it reports Standard / Hard (+100) / Casual (+200). A partner that exists in one version is fine
(Core falls back to Standard), so only a missing Standard block is an error. Exit code 1 when anything is missing.
A placeholder such as TrainerBattle.start(<pair A>, <pair B>) is listed as "unresolved" (not an error).
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT = ["story/35_SCRIPT_CH16.md", "story/36_SCRIPT_CH17.md", "story/37_SCRIPT_CH18.md", "story/38_SCRIPT_CH19.md",
           "story/39_SCRIPT_CH20.md", "story/40_SCRIPT_CH21.md", "story/41_SCRIPT_POSTGAME.md"]
WARDENS = {1: ("LEADER_DORIAN", "Dorian"), 2: ("LEADER_TAMSIN", "Tamsin"), 3: ("LEADER_MARISOL", "Marisol"),
           4: ("LEADER_ROOK", "Rook"), 5: ("LEADER_SAHAR", "Sahar"), 6: ("LEADER_CORVIN", "Corvin"),
           7: ("LEADER_BRANN", "Brann"), 8: ("LEADER_KAITO", "Kaito"), 9: ("LEADER_JUNO", "Juno"),
           10: ("LEADER_ANJA", "Anja"), 11: ("LEADER_ODESSA", "Odessa"), 12: ("LEADER_ILSA", "Ilsa"),
           13: ("LEADER_BASTIAN", "Bastian"), 14: ("LEADER_YSOLDE", "Ysolde"), 15: ("LEADER_MAGNUS", "Magnus"),
           16: ("LEADER_NYX", "Nyx"), 17: ("LEADER_CELESTINE", "Celestine"), 18: ("LEADER_SIGRUN", "Sigrun")}
PARTNER_OFFSET = 3   # Prismfall::Rival.partner_version(n) = n*10 + 3 + starter_slot (Core 006)


def pbs_keys(path):
    keys = set()
    with open(path, encoding="utf-8") as f:
        for line in f:
            m = re.match(r"\[([A-Za-z0-9_]+),([^\],]+)(?:,(\d+))?\]", line)
            if m:
                keys.add((m.group(1), m.group(2).strip(), int(m.group(3) or 0)))
    return keys


def versions(expr):
    """A version argument -> list of base versions (or None if it can't be read)."""
    expr = (expr or "0").strip()
    if re.fullmatch(r"\d+", expr):
        return [int(expr)]
    m = re.fullmatch(r"Prismfall::Rival\.version_for\((\d+)\)", expr)
    if m:
        return [int(m.group(1)) * 10 + s for s in (0, 1, 2)]
    m = re.fullmatch(r"Prismfall::Rival\.partner_version\((\d+)\)", expr)
    if m:
        return [int(m.group(1)) * 10 + PARTNER_OFFSET + s for s in (0, 1, 2)]
    return None


def split_args(s):
    out, depth, cur = [], 0, ""
    for ch in s:
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth -= 1
        if ch == "," and depth == 0:
            out.append(cur.strip()); cur = ""
        else:
            cur += ch
    if cur.strip():
        out.append(cur.strip())
    return out


def call_args(text, start):
    """Text of a balanced (...) argument list starting at text[start] == '('."""
    depth = 0
    for i in range(start, min(len(text), start + 400)):
        if text[i] == "(":
            depth += 1
        elif text[i] == ")":
            depth -= 1
            if depth == 0:
                return text[start + 1:i]
    return None


def refs_in(text):
    """Yields (line number, kind, type, name, [versions] or None, raw)."""
    for m in re.finditer(r"(TrainerBattle\.start|pbRegisterPartner|Prismfall\.rival_battle|Prismfall\.gym_battle)\(", text):
        line = text.count("\n", 0, m.start()) + 1
        raw = call_args(text, m.end() - 1)
        if raw is None:
            continue
        kind = m.group(1)
        args = split_args(raw.replace("%s", "?").replace("%d", "?"))
        if kind == "Prismfall.gym_battle":
            if args and args[0].isdigit() and int(args[0]) in WARDENS:
                tt, nm = WARDENS[int(args[0])]
                yield line, "gym", tt, nm, ([30, 31, 32] if int(args[0]) == 9 else [0]), raw
            continue
        i, found = 0, False
        while i < len(args):
            a = args[i]
            if re.fullmatch(r":[A-Z][A-Za-z0-9_]*", a) and i + 1 < len(args) and re.fullmatch(r'"[^"]*"', args[i + 1]):
                tt, nm = a[1:], args[i + 1][1:-1]
                ver = None
                if i + 2 < len(args) and (args[i + 2].isdigit() or args[i + 2].startswith("Prismfall::Rival.")):
                    ver = args[i + 2]; i += 1
                if kind == "Prismfall.rival_battle":
                    vs = [int(ver) * 10 + s for s in (0, 1, 2)] if ver and ver.isdigit() else None
                else:
                    vs = versions(ver)
                yield line, kind.split(".")[-1].replace("pbRegisterPartner", "partner"), tt, nm, vs, raw
                found = True
                i += 2
            else:
                i += 1
        if not found:
            yield line, "unresolved", None, None, None, raw
    for m in re.finditer(r"`\[([A-Z][A-Z0-9_]+),\s*([^\],`]+?)(?:,\s*(\d+))?\]`", text):
        line = text.count("\n", 0, m.start()) + 1
        yield line, "key", m.group(1), m.group(2).strip(), [int(m.group(3) or 0)], m.group(0)


def main(argv):
    quiet = "--quiet" in argv
    files = [a for a in argv if not a.startswith("--")]
    if "--all" in argv:
        files = sorted(glob.glob(os.path.join(ROOT, "story", "[2-4]*_SCRIPT_*.md")))
    elif not files:
        files = [os.path.join(ROOT, f) for f in DEFAULT]
    if "--all" in argv or len([a for a in argv if not a.startswith("--")]) == 0:
        files += sorted(glob.glob(os.path.join(ROOT, "mapgen", "layouts", "*.py")))
    keys = pbs_keys(os.path.join(ROOT, "pbs", "trainers.txt"))
    missing = unresolved = total = 0
    for fn in files:
        with open(fn, encoding="utf-8", errors="replace") as f:
            text = f.read()
        seen, rows = set(), []
        for line, kind, tt, nm, vs, raw in refs_in(text):
            if kind == "unresolved" or vs is None:
                unresolved += 1
                rows.append((line, "??", "unresolved %s: (%s)" % (kind if tt is None else "version of %s %s" % (tt, nm), raw[:110])))
                continue
            for v in vs:
                if (tt, nm, v) in seen:
                    continue
                seen.add((tt, nm, v))
                total += 1
                have = [d for d in (0, 100, 200) if (tt, nm, v + d) in keys] if v < 100 else ([0] if (tt, nm, v) in keys else [])
                tag = "".join(c if d in have else "-" for c, d in zip("SHC", (0, 100, 200)))
                if 0 not in have:
                    missing += 1
                    rows.append((line, "MISSING", "[%s,%s,%d] (%s)" % (tt, nm, v, kind)))
                elif not quiet:
                    rows.append((line, tag, "[%s,%s,%d] (%s)" % (tt, nm, v, kind)))
        if rows:
            print("== " + os.path.relpath(fn, ROOT))
            for line, tag, msg in rows:
                print("  %5d  %-7s %s" % (line, tag, msg))
    print("%d trainer reference(s), %d missing from pbs/trainers.txt, %d unresolved placeholder(s)" % (total, missing, unresolved))
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
