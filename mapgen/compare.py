#!/usr/bin/env python3
"""compare.py <our map id> <reference png> out.png [--ours-scale 0.5] : our build preview beside a Rejuvenation render,
both at the reference's tile scale (MAPGEN 2h look rounds)."""
import sys, os, glob
from PIL import Image, ImageDraw
Image.MAX_IMAGE_PIXELS = None
a = sys.argv[1:]
mid, ref, out = int(a[0]), a[1], a[2]
pv = glob.glob(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'maps_out', 'previews', '%03d_*.png' % mid))[0]
o = Image.open(pv).convert('RGB'); r = Image.open(ref).convert('RGB')
ref_scale = float(a[a.index('--ref-tile') + 1]) / 32 if '--ref-tile' in a else 0.4
o = o.resize((int(o.width * ref_scale), int(o.height * ref_scale)), Image.LANCZOS)
H = max(o.height, r.height)
im = Image.new('RGB', (o.width + r.width + 12, H + 16), (20, 20, 24)); d = ImageDraw.Draw(im)
im.paste(o, (0, 16)); im.paste(r, (o.width + 12, 16))
d.text((2, 2), 'Prismfall %d (ours)' % mid, fill=(255, 255, 0)); d.text((o.width + 14, 2), os.path.basename(ref), fill=(255, 255, 0))
im.save(out); print(out, im.size)
