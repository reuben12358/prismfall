#!/usr/bin/env python3
"""Builds every Prismfall field battle backdrop (EBDX rooms + animated layers).

  python3 -I art/battlebacks/build_backdrops.py            # all fields
  python3 -I art/battlebacks/build_backdrops.py VOLCANIC   # some fields

Writes graphics/EBDX/Battlebacks/{battlebg,elements}/ and the generated Bridge file
plugins/Prismfall EBDX Bridge/006_Bridge_Art.rb, plus art/battlebacks/origins.json (CREDITS source).
Source art is read from the reference games (read-only); see README.md.
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bblib import *
from paint import *
from rubygen import S, rb
import fields_a, fields_b, fields_c

REGISTRY = {}
for mod in (fields_a, fields_b, fields_c):
    REGISTRY.update(mod.BUILDERS)

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RB_OUT = os.path.join(ROOT, "plugins", "Prismfall EBDX Bridge", "006_Bridge_Art.rb")
ORIGINS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "origins.json")


def main(argv):
    want = [a.upper() for a in argv] or sorted(REGISTRY)
    origins = json.load(open(ORIGINS)) if os.path.exists(ORIGINS) else {}
    profiles = {}
    prev = load_previous_profiles()
    for fid in sorted(REGISTRY):
        if fid in want:
            print("building", fid)
            import paint
            paint.PREVIEW.clear()
            res = REGISTRY[fid]()
            write_preview(fid, res)
            profiles[fid] = res["profile"]
            origins[fid] = res["origins"]
        elif fid in prev:
            profiles[fid] = None   # keep the previously generated text
    write_ruby(profiles, prev)
    json.dump(origins, open(ORIGINS, "w"), indent=1, sort_keys=True)


PREV_DIR = "/tmp/bd/prev"


def write_preview(fid, res):
    """Room + recorded layers composited (static frame) for quick offline review."""
    import paint
    os.makedirs(PREV_DIR, exist_ok=True)
    name = res.get("room", "field_" + fid.lower())
    p = os.path.join(OUT, "battlebg", name + "_hd.png")
    if not os.path.exists(p):
        return
    hd = Image.open(p).convert("RGBA")
    for im, (x, y), bl, op, frames in paint.PREVIEW:
        if frames > 1:
            im = im.crop((0, 0, im.width // frames, im.height))
        top = blank(); top.alpha_composite(im, (int(x), int(y)))
        hd = blend(hd, top, "add" if bl == 1 else "normal", (op or 255) / 255.0)
    hd.save(os.path.join(PREV_DIR, name + ".png"))


def load_previous_profiles():
    """Previously generated per-field Ruby blocks (so partial rebuilds keep the others)."""
    out = {}
    if not os.path.exists(RB_OUT):
        return out
    cur = None
    buf = []
    for line in open(RB_OUT, encoding="utf-8"):
        if line.startswith("    # >>> "):
            cur = line.strip()[6:]
            buf = []
        elif line.startswith("    # <<< ") and cur:
            out[cur] = "".join(buf)
            cur = None
        elif cur:
            buf.append(line)
    return out


def write_ruby(profiles, prev):
    lines = [
        "#===============================================================================",
        "# Prismfall EBDX Bridge - GENERATED field art profiles. Do not edit by hand:",
        "# rebuild with `python3 -I art/battlebacks/build_backdrops.py [FIELD ...]`.",
        "# Each entry is merged over the hand-written profile in 001_Bridge_Config.rb:",
        "#   :art_extras  EBDX room keys for the field's own art (scrolling HD strips,",
        "#                EBDX stock elements, lights, bubbles...)",
        "#   :layers      Bridge-animated HD layers (pulse / flicker / sway / rotate / bob)",
        "#   :fx          particle emitters tuned to the art (replace the hand-written ones)",
        "#   :stages      per-stage overrides (FLOWER_GARDEN)",
        "#===============================================================================",
        "module PrismfallEBDX",
        "  ART_PROFILES = {",
    ]
    for fid in sorted(set(list(profiles) + list(prev))):
        p = profiles.get(fid)
        lines.append("    # >>> %s" % fid)
        if p is None:
            lines.append(prev[fid].rstrip("\n"))
        else:
            lines.append("    :%s => %s," % (fid, rb(p, 2)))
        lines.append("    # <<< %s" % fid)
    lines += [
        "  }",
        "",
        "  ART_PROFILES.each do |id, art|",
        "    base = PROFILES[id] || DEFAULT_PROFILE.dup",
        "    merged = base.merge(art.reject { |k, _| k == :stages })",
        "    if art[:stages] || base[:stages]",
        "      st = (base[:stages] || {}).dup",
        "      (art[:stages] || {}).each { |n, o| st[n] = (st[n] || {}).merge(o) }",
        "      merged[:stages] = st",
        "    end",
        "    PROFILES[id] = merged",
        "  end",
        "end",
        "",
    ]
    open(RB_OUT, "w", encoding="utf-8").write("\n".join(lines))
    print("wrote", RB_OUT)


if __name__ == "__main__":
    main(sys.argv[1:])
