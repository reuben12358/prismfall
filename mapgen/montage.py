#!/usr/bin/env python3
"""Montage of generated previews. usage: python3 -I montage.py out.png <id> [<id> ...] [--scale 0.5] [--cols 4]"""
import sys, os, glob
from PIL import Image, ImageDraw
a = sys.argv[1:]
scale = float(a[a.index('--scale') + 1]) if '--scale' in a else 0.5
cols = int(a[a.index('--cols') + 1]) if '--cols' in a else 4
ids = [x for x in a[1:] if x.isdigit() and not (a[a.index(x) - 1] in ('--scale', '--cols'))]
pv = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'maps_out', 'previews')
ims = []
for i in ids:
    f = glob.glob(os.path.join(pv, '%03d_*.png' % int(i)))
    if not f: continue
    im = Image.open(f[0]); im = im.resize((int(im.width * scale), int(im.height * scale)))
    ImageDraw.Draw(im).text((3, 3), os.path.basename(f[0])[:-4], fill=(255, 40, 40))
    ims.append(im)
rows = [ims[k:k + cols] for k in range(0, len(ims), cols)]
W = max(sum(i.width + 4 for i in r) for r in rows); H = sum(max(i.height for i in r) + 4 for r in rows)
out = Image.new('RGB', (W, H), (20, 20, 28)); y = 0
for r in rows:
    x = 0
    for i in r: out.paste(i, (x, y)); x += i.width + 4
    y += max(i.height for i in r) + 4
out.save(a[0]); print(out.size)
