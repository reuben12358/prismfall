#!/usr/bin/env python3
"""pv.py <map id> [x y w h] [--grid] -> /tmp/w/pv_<id>.png : downscaled preview (or a full-res crop in tiles) for review."""
import sys, glob
from PIL import Image
a = [v for v in sys.argv[1:] if not v.startswith('--')]
f = glob.glob('/home/claude/fangame/maps_out/previews/%s_*.png' % a[0])[0]
im = Image.open(f)
if len(a) >= 5:
    x, y, w, h = map(int, a[1:5]); im = im.crop((x * 32, y * 32, (x + w) * 32, (y + h) * 32))
else:
    s = 1500 / max(im.size); im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
im.save('/tmp/w/pv_%s.png' % a[0]); print(im.size)
