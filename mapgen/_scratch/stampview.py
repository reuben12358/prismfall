"""render named stamps on a checkerboard (transparency visible) with per-layer view, for inspection"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
from PIL import Image, ImageDraw
import render as R, rcompose as RC
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'layouts'))
import rkit as K
names = sys.argv[2:]; out = sys.argv[1]
tid = 52
ts = R.tilesets()[tid]; tc = R.TileCache(ts)
ims = []
for n in names:
    st = K.STAMPS[n]; L = np.array(st['layers']); h, w = L.shape[1:]
    Lr = RC.resolve(L, tid)
    panels = []
    for zs in ((0, 1, 2), (0,), (1,), (2,)):
        im = Image.new('RGBA', (w * 32, h * 32))
        d = ImageDraw.Draw(im)
        for y in range(h * 4):
            for x in range(w * 4):
                d.rectangle([x * 8, y * 8, x * 8 + 7, y * 8 + 7], fill=(255, 0, 255, 255) if (x + y) % 2 else (200, 0, 200, 255))
        for z in zs:
            for y in range(h):
                for x in range(w):
                    t = int(Lr[z, y, x])
                    if t:
                        ti = tc.tile(t)
                        if ti is not None: im.alpha_composite(ti, (x * 32, y * 32))
        panels.append(im)
    W = sum(p.width for p in panels) + 8 * len(panels)
    row = Image.new('RGBA', (W, h * 32 + 14), (30, 30, 30, 255))
    ImageDraw.Draw(row).text((2, 0), n, fill=(255, 255, 0, 255))
    x = 0
    for p in panels: row.paste(p, (x, 14)); x += p.width + 8
    ims.append(row)
H = sum(i.height for i in ims); W = max(i.width for i in ims)
sheet = Image.new('RGBA', (W, H), (30, 30, 30, 255)); y = 0
for i in ims: sheet.paste(i, (0, y)); y += i.height
sc = float(os.environ.get('SC', '0.5'))
sheet = sheet.resize((int(W * sc), int(H * sc)), Image.NEAREST)
sheet.save(out)
print(sheet.size)
