#!/usr/bin/env python3
"""Catalogue building-like objects in the Tectonic reference maps (safe parser): connected components of
tiles from the building rows (sheet rows >= 512) on layers 1-2. Writes a labelled contact sheet and a JSON list
{name: {map, rect}} that can be pasted into textract.yaml.   usage: tcatalog.py out.png out.json [minrow maxrow]"""
import sys, os, json, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import rmarshal as M, render as R
from PIL import Image, ImageDraw
# optional: --data DIR --ts 37,40 --off 8616 --rows 118-136,0-22 --prefix s   (appended sheets of tileset 33)
def opt(k, d):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
TD = opt('--data', '/home/claude/ref/art/tectonic/Data')
TS = [int(v) for v in opt('--ts', '24').split(',')]
OFF = int(opt('--off', '384')) - 384
ROWS = [tuple(int(v) for v in r.split('-')) for r in opt('--rows', '512-895').split(',')]
PRE = opt('--prefix', 'c')
def isobj(a):
    r = (a - 384) // 8
    m = np.zeros(a.shape, bool)
    for lo_, hi_ in ROWS: m |= (a >= 384) & (r >= lo_) & (r <= hi_)
    return m
seen_sig = set(); out = {}; ims = []
tc = R.TileCache(R.tilesets()[33])
for f in sorted(glob.glob(TD + '/Map[0-9]*.rxdata')):
    m = M.load_file(f)
    if m.tileset_id not in TS: continue
    mid = int(os.path.basename(f)[3:6]); D = m.data.data; H, W = m.height, m.width
    obj = isobj(D[1]) | isobj(D[2]) | (isobj(D[0]) if '--l0' in sys.argv else False)
    lab = np.zeros((H, W), int); n = 0
    for y0, x0 in np.argwhere(obj):
        if lab[y0, x0]: continue
        n += 1; st = [(x0, y0)]; cells = []
        while st:
            x, y = st.pop()
            if not (0 <= x < W and 0 <= y < H) or lab[y, x] or not obj[y, x]: continue
            lab[y, x] = n; cells.append((x, y)); st += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        xs = [c[0] for c in cells]; ys = [c[1] for c in cells]
        x, y, w, h = min(xs), min(ys), max(xs) - min(xs) + 1, max(ys) - min(ys) + 1
        if w < 3 or h < 3 or w > 30 or h > 30: continue
        sig = (w, h, tuple(D[1:, y:y + h, x:x + w].reshape(-1).tolist()))
        if any(s_[0] == w and s_[1] == h and sum(a != b for a, b in zip(s_[2], sig[2])) < 0.15 * len(sig[2]) for s_ in seen_sig): continue
        if sig in seen_sig: continue
        seen_sig.add(sig)
        name = '%s%d_%d_%d' % (PRE, mid, x, y)
        out[name] = {'map': mid, 'rect': [int(x), int(y), int(w), int(h)]}
        im = Image.new('RGBA', (w * 32, h * 32), (150, 200, 120, 255))
        for z in (0, 1, 2):
            for yy in range(h):
                for xx in range(w):
                    t = int(D[z, y + yy, x + xx])
                    if t >= 384 and (z > 0 or '--l0' in sys.argv) and tc.tile(t + OFF) is not None:
                        im.alpha_composite(tc.tile(t + OFF), (xx * 32, yy * 32))
        ims.append(('%s %dx%d' % (name, w, h), im.resize((w * 16, h * 16))))
json.dump(out, open(sys.argv[2], 'w'), indent=0)
rows = []; row = []; ws = 0
for n_, i in ims:
    if ws + max(i.width, 90) > 1500: rows.append(row); row = []; ws = 0
    row.append((n_, i)); ws += max(i.width, 90) + 6
rows.append(row)
Hh = sum(max(i.height for _, i in r) + 14 for r in rows)
sh = Image.new('RGB', (1510, Hh), (30, 30, 40)); d = ImageDraw.Draw(sh); y = 0
for r in rows:
    x = 0
    for n_, i in r:
        sh.paste(i, (x, y + 12)); d.text((x, y), n_, fill=(255, 255, 0)); x += max(i.width, 90) + 6
    y += max(i.height for _, i in r) + 14
sh.save(sys.argv[1]); print(sh.size, len(ims))
