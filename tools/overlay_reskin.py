#!/usr/bin/env python3
"""overlay_reskin.py - lay Gemini's Gen 5 tileset/autotile reskin over an installed Graphics folder.

graphics/Tilesets and graphics/Autotiles hold recoloured copies of the sheets mapgen writes to maps_out/Graphics
(mapgen/gen5_reskin.py: same file names, same size, same alpha mask, only the colours change). Both trees are copied
into a game, so whichever is copied last wins. This script makes that explicit and safe:

  * a reskinned sheet is installed only while it still matches its mapgen source (same size, same alpha mask);
  * a stale one (mapgen added or moved tiles since the reskin was made) is skipped, the mapgen sheet is installed
    instead and the file is listed, so a new tile can never come out blank. Re-run the reskin to refresh it:
        python3 mapgen/gen5_reskin.py --src-roots maps_out/Graphics <engine>/Graphics --out-dirs graphics art/out/Graphics --verify
  * sheets with no mapgen source (the four stock interiors, Lava, water2...) replace the engine's stock files of the
    same name: that is the point of the reskin, and they are listed so nobody is surprised.

    python3 -I tools/overlay_reskin.py <game>/Graphics            # install
    python3 -I tools/overlay_reskin.py <game>/Graphics --off      # install the plain mapgen sheets instead (PF_NO_GEN5=1)
    python3 -I tools/overlay_reskin.py --check                    # only report stale sheets; exit 1 if any

Needs Pillow + numpy for the alpha check; without them only the sizes are compared."""
import os
import shutil
import struct
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
RESKIN = os.path.join(ROOT, "graphics")
MAPGEN = os.path.join(ROOT, "maps_out", "Graphics")
SUBS = ("Tilesets", "Autotiles")


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(24)
    return struct.unpack(">II", head[16:24])


def same_alpha(a, b):
    try:
        import numpy as np
        from PIL import Image
        Image.MAX_IMAGE_PIXELS = None
    except Exception:
        return True
    x = np.asarray(Image.open(a).convert("RGBA"))[..., 3]
    y = np.asarray(Image.open(b).convert("RGBA"))[..., 3]
    return x.shape == y.shape and bool((x == y).all())


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    check = "--check" in sys.argv
    off = "--off" in sys.argv or bool(os.environ.get("PF_NO_GEN5"))
    if not check and not args:
        print(__doc__)
        return 2
    dest = args[0] if args else None
    used, stale, stock = 0, [], []
    for sub in SUBS:
        rdir = os.path.join(RESKIN, sub)
        if not os.path.isdir(rdir):
            continue
        for f in sorted(os.listdir(rdir)):
            if not f.endswith(".png"):
                continue
            new, src = os.path.join(rdir, f), os.path.join(MAPGEN, sub, f)
            pick = new
            if os.path.isfile(src):
                if off:
                    pick = src
                elif png_size(new) != png_size(src) or not same_alpha(new, src):
                    stale.append("%s/%s" % (sub, f))
                    pick = src
            else:
                if off:
                    continue          # the engine's own stock sheet stays (it is not ours to restore)
                stock.append("%s/%s" % (sub, f))
            used += pick == new
            if dest:
                os.makedirs(os.path.join(dest, sub), exist_ok=True)
                shutil.copyfile(pick, os.path.join(dest, sub, f))
    for s in stale:
        print("STALE reskin (mapgen sheet installed instead): graphics/%s" % s)
    print("Gen 5 reskin: %s%d sheet(s)%s, %d stale, %d over stock engine sheets%s"
          % ("OFF, " if off else "", used, "" if dest else " current", len(stale), len(stock),
             (" (" + ", ".join(os.path.basename(s)[:-4] for s in stock) + ")") if stock and not off else ""))
    return 1 if (check and stale) else 0


if __name__ == "__main__":
    sys.exit(main())
