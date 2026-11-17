#!/usr/bin/env python3
"""tilestrip.py <tileset id> out.png id [id ...] : labelled strip of single tiles (research helper, MAPGEN 2h)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render as R
from PIL import Image, ImageDraw
tid = int(sys.argv[1]); out = sys.argv[2]
ids = []
for a in sys.argv[3:]:
    if '-' in a: x, y = map(int, a.split('-')); ids += list(range(x, y + 1))
    else: ids.append(int(a))
tc = R.TileCache(R.tilesets()[tid]); per = 16
o = Image.new('RGB', (per * 50, ((len(ids) + per - 1) // per) * 50), (90, 150, 110)); d = ImageDraw.Draw(o)
for k, t in enumerate(ids):
    x, y = (k % per) * 50, (k // per) * 50
    im = tc.tile(t)
    if im is not None: o.paste(im, (x + 9, y + 14), im)
    d.text((x + 1, y + 1), str(t), fill=(255, 255, 0))
o.save(out); print(o.size)
