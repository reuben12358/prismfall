#!/usr/bin/env python3
"""check_art_wiring.py - does every wired art id have its file, and is every pushed art file wired?

Reads the wiring tables straight from the sources (nothing is imported or run):
  pbs/trainer_types.txt                                   -> graphics/Trainers/<TYPE>.png (front), _back, Characters/trainer_<TYPE>
  plugins/Prismfall EBDX Bridge/010_Bridge_VersusIntro.rb -> VS_IDS / THEMES -> graphics/EBDX/VS/<ID>.png (or the portrait fallback)
  plugins/Prismfall Cutscenes/014_Portraits.rb            -> Portrait::CAST + register(..., art:) -> graphics/Portraits/<ID>.png
  plugins/Prismfall Core/025_CharsetAliases.rb            -> CHARSET_ALIASES / NAME_ALIASES / TYPE_CHARSETS -> graphics/Characters
  plugins/Prismfall Core/026_PlayerLooks.rb               -> the player's movement sheets
  plugins/Prismfall Core/028_Interludes.rb                -> Interlude trainer types
and, the other way round, lists art in graphics/ that nothing above reaches.

    python3 -I tools/check_art_wiring.py            # report; exit 1 when a wired id that is in use has no file
    python3 -I tools/check_art_wiring.py --quiet    # only the problems

"ERROR" = a trainer type that pbs/trainers.txt uses has no front sprite, or a table names a file that does not exist
and has no fallback. "GAP" = art still owed (the game falls back: stock stand-in, portrait at 1.5x, plain message box).
"UNWIRED" = a pushed file no table reaches. Pure standard library."""
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
STOCK_TYPES = "/home/claude/ref/ebdx/PBS/trainer_types.txt"   # the base project's classes (their sprites ship with the engine)
G = os.path.join(ROOT, "graphics")
QUIET = "--quiet" in sys.argv

# Stock Essentials classes (their sprites ship with the engine), and ids that are meant to have no art.
NO_FRONT_OK = {
    "HOLLOW_GRUNT": "genderless base class; trainers use _M/_F",
    "MERIDIAN_AGENT": "genderless base class; trainers use _M/_F",
    "ASHKAAR_SOLDIER": "genderless base class; trainers use _M/_F",
    "ISENMAR_SOLDIER": "genderless base class; trainers use _M/_F",
}
EXPRESSIONS = "neutral happy angry sad surprised smug shocked panic blush crying deadpan".split()


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8-sig") as f:
        return f.read()


def have(sub, name):
    return os.path.isfile(os.path.join(G, sub, name + ".png"))


def names(sub):
    d = os.path.join(G, sub)
    return sorted(f[:-4] for f in os.listdir(d) if f.endswith(".png")) if os.path.isdir(d) else []


def block(src, start):
    """text of the { ... } or %i[ ... ] literal that follows `start`"""
    m = re.search(start, src)
    if not m:
        raise ValueError(start)
    i = m.end()
    j = min(k for k in (src.find("{", i), src.find("[", i)) if k >= 0)
    open_c = src[j]
    close_c = "}" if open_c == "{" else "]"
    depth = 0
    for k in range(j, len(src)):
        if src[k] == open_c:
            depth += 1
        elif src[k] == close_c:
            depth -= 1
            if depth == 0:
                return re.sub(r"#[^\n]*", "", src[j + 1:k])
    raise ValueError(start)


def main():
    errors, gaps, unwired, notes = [], [], [], []

    # ---- trainer types ------------------------------------------------------------------------------------------
    tt_src = read("pbs/trainer_types.txt")
    types = re.findall(r"^\[([A-Za-z0-9_]+)\]", tt_src, re.M)
    dup = sorted({t for t in types if types.count(t) > 1})
    for t in dup:
        errors.append("trainer_types.txt defines [%s] %d times" % (t, types.count(t)))
    used = {}
    for rel in ("pbs/trainers.txt", "pbs/trainers_trials.txt"):
        if os.path.isfile(os.path.join(ROOT, rel)):
            for t in re.findall(r"^\[([A-Za-z0-9_]+),", read(rel), re.M):
                used[t] = used.get(t, 0) + 1
    fronts = set(names("Trainers"))
    si_rel = "plugins/Prismfall Core/032_TrainerArtStandIns.rb"
    stand_ins = {}
    if os.path.isfile(os.path.join(ROOT, si_rel)):
        stand_ins = dict(re.findall(r":([A-Z0-9_]+)\s*=>\s*:([A-Z0-9_]+)", block(read(si_rel), r"TRAINER_ART_STAND_INS =")))

    stock = set()
    if os.path.isfile(STOCK_TYPES):
        with open(STOCK_TYPES, encoding="utf-8-sig") as f:
            stock = set(re.findall(r"^\[([A-Za-z0-9_]+)\]", f.read(), re.M))

    def borrowed(t):
        for _ in range(2):
            t = stand_ins.get(t)
            if t is None or t in fronts or t in stock:
                return t
        return None

    for t, alt in sorted(stand_ins.items()):
        if t not in types:
            errors.append("TRAINER_ART_STAND_INS: %s is not a trainer type in pbs/trainer_types.txt" % t)
        if alt not in types and stock and alt not in stock:
            errors.append("TRAINER_ART_STAND_INS %s => %s: %s is neither a Prismfall nor a stock trainer type" % (t, alt, alt))
        if t in fronts:
            notes.append("TRAINER_ART_STAND_INS: %s has its own front sprite now; its row can go" % t)
    for t in types:
        if t in fronts:
            continue
        if borrowed(t):
            (gaps if used.get(t) else notes).append("type %s: no front sprite, battles in %s's (%d trainer blocks)"
                                                    % (t, borrowed(t), used.get(t, 0)))
        elif t in NO_FRONT_OK:
            if used.get(t):
                errors.append("type %s has no front sprite but %d trainer(s) use it" % (t, used[t]))
            else:
                notes.append("type %s: no front sprite (%s)" % (t, NO_FRONT_OK[t]))
        elif used.get(t):
            errors.append("type %s: graphics/Trainers/%s.png missing (%d trainer blocks use it)" % (t, t, used[t]))
        else:
            gaps.append("type %s: no front sprite graphics/Trainers/%s.png (no trainers yet)" % (t, t))
    ow_missing = []
    for t in types:
        if t.startswith("PLAYER_") and not have("Trainers", t + "_back"):
            errors.append("player type %s has no back sprite" % t)
        if not have("Characters", "trainer_" + t) and t not in NO_FRONT_OK:
            ow_missing.append(t)
    if ow_missing:
        gaps.append("no overworld sheet graphics/Characters/trainer_<TYPE>.png (maps use a stand-in) for %d type(s): %s"
                    % (len(ow_missing), " ".join(ow_missing)))
    for f in sorted(fronts):
        base = f[:-5] if f.endswith("_back") else f
        if base not in types:
            unwired.append("graphics/Trainers/%s.png: no [%s] in pbs/trainer_types.txt" % (f, base))
    for c in names("Characters"):
        if c.startswith("trainer_") and c[8:] not in types:
            unwired.append("graphics/Characters/%s.png: no [%s] in pbs/trainer_types.txt" % (c, c[8:]))

    # ---- VS busts -----------------------------------------------------------------------------------------------
    vs_src = read("plugins/Prismfall EBDX Bridge/010_Bridge_VersusIntro.rb")
    vs_ids = dict(re.findall(r":([A-Za-z0-9_]+)\s*=>\s*\"([A-Z0-9_]+)\"", block(vs_src, r"VS_IDS\s*=")))
    themes = dict(re.findall(r"\"([A-Z0-9_]+)\"\s*=>\s*:([a-z]+)", block(vs_src, r"THEMES\s*=")))
    for t, cid in sorted(vs_ids.items()):
        if t not in types:
            errors.append("VS_IDS: :%s is not a trainer type in pbs/trainer_types.txt" % t)
        if have("EBDX/VS", cid):
            continue
        if have("Portraits", cid):
            gaps.append("VS bust %s (for :%s): no graphics/EBDX/VS/%s.png, the portrait is shown at 1.5x" % (cid, t, cid))
        else:
            errors.append("VS_IDS :%s => %s: neither graphics/EBDX/VS/%s.png nor a portrait" % (t, cid, cid))
    for cid, th in sorted(themes.items()):
        for kind in ("tunnel", "bandfoe", "bandplayer"):
            if not have("EBDX/VS", "%s_%s" % (kind, th)):
                errors.append("THEMES %s => :%s: graphics/EBDX/VS/%s_%s.png missing" % (cid, th, kind, th))
        if not have("EBDX/VS", cid) and not have("Portraits", cid):
            errors.append("THEMES names %s, which has no bust and no portrait" % cid)
    ui = re.compile(r"^(tunnel|bandfoe|bandplayer)_|^(bolt|spark|emblem|flash|vs)")
    name_ids = set()
    for rel in ("pbs/trainers.txt", "pbs/trainers_trials.txt"):
        if os.path.isfile(os.path.join(ROOT, rel)):
            for nm in re.findall(r"^\[[A-Za-z0-9_]+,([^,\]]+)", read(rel), re.M):
                name_ids.add(re.sub(r"[^A-Z0-9_]", "", nm.upper()))
    for b in names("EBDX/VS"):
        if ui.match(b):
            continue
        if b not in vs_ids.values() and b not in name_ids and not b.startswith("PLAYER_"):
            unwired.append("graphics/EBDX/VS/%s.png: no VS_IDS entry and no trainer of that name" % b)
        elif b not in themes:
            gaps.append("VS bust %s has no THEMES colour (it gets the default violet)" % b)

    # ---- portraits ----------------------------------------------------------------------------------------------
    po_src = re.sub(r"(?m)^\s*#.*$", "", read("plugins/Prismfall Cutscenes/014_Portraits.rb"))
    cast = set(block(po_src, r"CAST = %i").split())
    art = {}
    for rid, rest in re.findall(r"Portrait\.register\(:([A-Z0-9_]+)([^\n]*)\)", po_src):
        if "cast: true" in rest:
            cast.add(rid)
        m = re.search(r"art:\s*:([A-Z0-9_]+)", rest)
        if m:
            art[rid] = m.group(1)
    for m in re.finditer(r"\{([^{}]*)\}\.each do \|id, type\|\s*\n\s*Prismfall::Portrait\.register\(id,[^\n]*cast: true", po_src):
        cast.update(re.findall(r":([A-Z0-9_]+)\s*=>", m.group(1)))
    portraits = set(names("Portraits"))
    reached = set()
    for cid in sorted(cast):
        ids = ["PLAYER_A", "PLAYER_B"] if cid == "PLAYER" else [art.get(cid, cid)]
        for a in ids:
            reached.add(a)
            if a not in portraits:
                gaps.append("portrait cast %s: no graphics/Portraits/%s.png (plain message box)" % (cid, a))
                continue
            miss = [e for e in EXPRESSIONS if "%s_%s" % (a, e) not in portraits]
            if miss and len(miss) < len(EXPRESSIONS):
                notes.append("portrait %s: no file for %s (falls back to %s.png)" % (a, ", ".join(miss), a))
            elif miss:
                notes.append("portrait %s: one face only, no expressions" % a)
    for pfile in sorted(portraits):
        base = pfile
        for e in EXPRESSIONS:
            if pfile.endswith("_" + e):
                base = pfile[:-len(e) - 1]
        if base not in reached:                      # an extra expression (JUNO_wink): the longest wired prefix
            pre = [r for r in reached if pfile.startswith(r + "_")]
            base = max(pre, key=len) if pre else base
        if base not in reached:
            unwired.append("graphics/Portraits/%s.png: %s is not in Portrait::CAST" % (pfile, base))
            reached.add(base)   # one line per character

    # ---- overworld charsets -------------------------------------------------------------------------------------
    ca_src = read("plugins/Prismfall Core/025_CharsetAliases.rb")
    targets = set(re.findall(r"=>\s*\"([A-Z0-9_]+)\"", block(ca_src, r"CHARSET_ALIASES =") + block(ca_src, r"NAME_ALIASES =")))
    chars = set(names("Characters"))
    for t in sorted(targets):
        if t not in chars:
            gaps.append("charset alias target %s: no graphics/Characters/%s.png (the stand-in stays)" % (t, t))
    for t in block(ca_src, r"TYPE_CHARSETS = %i").split():
        if t not in types:
            errors.append("TYPE_CHARSETS: %s is not a trainer type" % t)
        elif "trainer_" + t not in chars:
            alt = stand_ins.get(t)
            if alt and "trainer_" + alt in chars:
                notes.append("TYPE_CHARSETS %s: wears trainer_%s.png (Core 032 stand-in)" % (t, alt))
            else:
                gaps.append("TYPE_CHARSETS %s: no graphics/Characters/trainer_%s.png yet (the stand-in stays)" % (t, t))
    pl_src = read("plugins/Prismfall Core/026_PlayerLooks.rb")
    player_sheets = set(re.findall(r":(?:walk|run|cycle|surf|dive|fish|surf_fish)\s*=>\s*\"([A-Za-z0-9_]+)\"", pl_src))
    for sheet in sorted(player_sheets):
        if sheet not in chars:
            (errors if sheet.startswith("trainer_PLAYER") else gaps).append("player sheet graphics/Characters/%s.png missing" % sheet)
    il_src = read("plugins/Prismfall Core/028_Interludes.rb")
    for t in sorted(set(re.findall(r":trainer_type\s*=>\s*:([A-Z0-9_]+)", il_src))):
        if t not in types:
            errors.append("Interlude trainer type :%s is not in pbs/trainer_types.txt" % t)
        elif not have("Trainers", t + "_back"):
            gaps.append("Interlude type %s: no back sprite graphics/Trainers/%s_back.png (the front strip is not shown either: "
                        "the player's side needs a back)" % (t, t))
    interlude_sheets = set(re.findall(r"\"([A-Z][A-Z0-9_]+)\"", "".join(re.findall(r":charset\s*=>\s*\[([^\]]*)\]", il_src))))
    for c in sorted(chars):
        if c.startswith(("trainer_", "pose_", "act_", "pf_")) or c in targets or c in player_sheets or c in interlude_sheets:
            continue
        if c in ("PLAYER_A", "PLAYER_B"):
            continue   # byte-identical twins of trainer_PLAYER_A/B
        unwired.append("graphics/Characters/%s.png: no alias reaches it (a map event must name the sheet itself)" % c)
    poses = [c[5:] for c in chars if c.startswith("pose_")]
    for p in sorted(poses):
        if p not in chars and "trainer_" + p not in chars:
            unwired.append("graphics/Characters/pose_%s.png: no walking sheet %s.png beside it" % (p, p))

    # ---- report -------------------------------------------------------------------------------------------------
    print("trainer types %d (fronts %d) | VS ids %d, themes %d | portrait cast %d | charset alias targets %d"
          % (len(types), len(fronts), len(vs_ids), len(themes), len(cast), len(targets)))
    for title, rows in (("ERROR", errors), ("GAP", gaps), ("UNWIRED", unwired)):
        for r in rows:
            print("%-7s %s" % (title, r))
    if not QUIET:
        for r in notes:
            print("note    %s" % r)
    print("%d error(s), %d gap(s), %d unwired file(s)" % (len(errors), len(gaps), len(unwired)))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
