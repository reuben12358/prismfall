#!/usr/bin/env python3
"""Contact sheet of real-engine backdrop stills.
   python3 -I make_contact_sheet.py <shots_dir> <out.png> [--clean] [--cols N] [--scale S] [--suffix _wide]
                                    [--title "..."] [names...]
   --suffix: sheet of another framing from a BD_VECTORS=1 run (_wide = SENDOUT pull-back, _enemy = opening
   close-up, _player)."""
import sys, os
from PIL import Image, ImageDraw

args = sys.argv[1:]
src, out = args[0], args[1]
clean = "--clean" in args
cols = int(args[args.index("--cols") + 1]) if "--cols" in args else 5
scale = float(args[args.index("--scale") + 1]) if "--scale" in args else 0.5
suffix = args[args.index("--suffix") + 1] if "--suffix" in args else ("_clean" if clean else "")
title = (args[args.index("--title") + 1] if "--title" in args else
         "Prismfall field backdrops - real engine stills (mkxp-z + EBDX + Prismfall Bridge), %d rooms")
skip = {"--clean", "--cols", "--scale", "--suffix", "--title"}
names = []
i = 2
while i < len(args):
    if args[i] in ("--cols", "--scale", "--suffix", "--title"):
        i += 2; continue
    if args[i] not in skip:
        names.append(args[i])
    i += 1
if not names:
    suffixes = ("_clean", "_player", "_enemy", "_wide")
    names = sorted(f[:-4] for f in os.listdir(src) if f.endswith(".png") and not f[:-4].endswith(suffixes))
tiles = []
for n in names:
    p = os.path.join(src, n + suffix + ".png")
    if not os.path.exists(p):
        continue
    im = Image.open(p).convert("RGB")
    im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
    tiles.append((n, im))
cw = max(t.width for _, t in tiles) + 4
ch = max(t.height for _, t in tiles) + 18
rows = (len(tiles) + cols - 1) // cols
sheet = Image.new("RGB", (cols * cw, rows * ch + 24), (18, 18, 22))
d = ImageDraw.Draw(sheet)
d.text((6, 6), title % len(tiles) if "%d" in title else title, fill=(255, 255, 255))
for k, (n, t) in enumerate(tiles):
    x, y = (k % cols) * cw + 2, (k // cols) * ch + 24
    d.text((x + 2, y + 2), n.upper(), fill=(255, 220, 90))
    sheet.paste(t, (x, y + 16))
sheet.save(out)
print(out, sheet.size, len(tiles))
