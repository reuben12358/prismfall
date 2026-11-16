#!/usr/bin/env python3
"""Render data/templates/<name>.json (with grid) into one montage. usage: python3 -I tpl_preview.py out.png name..."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, rjson, rpg as G, render as R
from PIL import Image, ImageDraw
ims = []
for n in sys.argv[2:]:
    t = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'templates', n + '.json')))
    lay = np.array(t['layers'])
    evs = {i + 1: rjson.from_j(e) for i, e in enumerate(t['events'])}
    m = G.rmap(t['tileset'], t['w'], t['h'], G.table3(lay), evs)
    im = R.render(m, grid=True); ImageDraw.Draw(im).text((2, 2), n, fill=(255, 0, 0, 255))
    ims.append(im.resize((int(im.width * .75), int(im.height * .75))))
W = sum(i.width for i in ims) + 4 * len(ims); H = max(i.height for i in ims)
out = Image.new('RGB', (W, H)); x = 0
for i in ims: out.paste(i, (x, 0)); x += i.width + 4
out.save(sys.argv[1]); print(out.size)
