#!/usr/bin/env python3
"""sheetzoom.py <tileset id> out.png scale r0-r1 [r0-r1 ...] [--base N] : zoomed crops of registered-tileset rows with the
tile id of each row's first tile printed (ids are composite ids; --base = id of the sheet part's first tile, default 384)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render as R
from PIL import Image, ImageDraw
a = [v for v in sys.argv[1:] if not v.startswith('--')]
base = int(sys.argv[sys.argv.index('--base') + 1]) if '--base' in sys.argv else 384
if '--base' in sys.argv: a.remove(str(base))
tc = R.TileCache(R.tilesets()[int(a[0])]); sc = float(a[2]); S = int(32 * sc); ims = []
for rg in a[3:]:
    r0, r1 = map(int, rg.split('-'))
    im = Image.new('RGBA', (8 * S, (r1 - r0) * S), (120, 170, 110, 255)); d = ImageDraw.Draw(im)
    for r in range(r0, r1):
        for c in range(8):
            t = tc.tile(base + r * 8 + c)
            if t is not None: im.alpha_composite(t.resize((S, S), Image.NEAREST), (c * S, (r - r0) * S))
            d.rectangle([c * S, (r - r0) * S, (c + 1) * S, (r - r0 + 1) * S], outline=(255, 255, 0, 50))
        d.text((1, (r - r0) * S + 1), str(base + r * 8), fill=(255, 255, 255), stroke_width=1, stroke_fill=(0, 0, 0))
    ims.append(im)
o = Image.new('RGB', (sum(i.width + 6 for i in ims), max(i.height for i in ims)), (0, 0, 0)); x = 0
for i in ims:
    o.paste(i.convert('RGB'), (x, 0)); x += i.width + 6
o.save(a[1]); print(o.size)
