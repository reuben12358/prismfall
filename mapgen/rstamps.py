#!/usr/bin/env python3
"""rstamps.py - mine object stamps (buildings, props, trees) from the downloaded games' maps into PF Rejuv ids
(MAPGEN 2h).  Definitions in rstamps.yaml:

  name: {game: rejuvenation, map: 82, rect: [x, y, w, h], rows: [[330, 392]], door: [mx, my], ids: [..], drop: [..],
         l0: true, solid: [[dx, dy], ...]}
  - rows: source-sheet row ranges kept (all three layers); ids: extra source ids kept; drop: source ids removed.
  - l0: keep matching layer-1 tiles too (deck floors, paving drawn on the ground layer); default false.
  - door: the door cell in MAP coordinates (stored relative to the stamp's trimmed corner).
  - sheet stamps: {sheet: gl, at: [col, row], size: [w, h], layer: 1, top: n}  copy a block straight from a part of
    the composite sheet (top: the first n rows go on layer 3).
Output data/stamps_rj.json  {name: {w, h, layers (composite / virtual ids), door?, src}}.
    python3 -I rstamps.py [--sheet out.png] [names...]"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import yaml, numpy as np
from PIL import Image, ImageDraw
import rref as RR, rcompose as RC
HERE = os.path.dirname(os.path.abspath(__file__))
OUTF = os.path.join(HERE, 'data', 'stamps_rj.json')


def part_of(game, tileset_id):
    sheet = RR.tileset(game, tileset_id)['tileset_name']
    for key, g, tid, fname in RC.PARTS:
        if g == game and fname == sheet: return key
    raise KeyError('no PF Rejuv part for %s tileset %d (%s)' % (game, tileset_id, sheet))


def composite_map(game, mid):
    L, m = RR.load(game, mid)
    return RC.to_composite(L, game, m.tileset_id, part_of(game, m.tileset_id)), L, m


def ranges(rr):
    out = set()
    for a, b in rr or []:
        out |= set(range(a, b + 1))
    return out


def mine(name, s):
    if 'sheet' in s:
        off = RC.offset(s['sheet']); c0, r0 = s['at']; w, h = s['size']
        lay = np.zeros((3, h, w), int)
        for dy in range(h):
            for dx in range(w):
                z = 2 if dy < s.get('top', 0) else s.get('layer', 1)
                lay[z, dy, dx] = off + (r0 + dy) * 8 + c0 + dx
        st = dict(w=w, h=h, layers=lay.tolist(), src=['sheet', s['sheet'], c0, r0])
        if 'door' in s: st['door'] = list(s['door'])
        return st
    C, L, m = composite_map(s['game'], s['map'])
    x, y, w, h = s['rect']
    src = L[:, y:y + h, x:x + w]; lay = C[:, y:y + h, x:x + w].copy()
    rows = ranges(s.get('rows')) - ranges(s.get('deny')); keep = set(s.get('ids', [])); drop = set(s.get('drop', []))
    srow = np.where(src >= 384, (src - 384) // 8, -1)
    ok = (np.isin(srow, list(rows)) | np.isin(src, list(keep))) & ~np.isin(src, list(drop)) & (src > 0)
    if not s.get('l0'): ok[0] = False
    lay[~ok] = 0
    for cx, cy in s.get('clear', []): lay[:, cy, cx] = 0          # stray neighbour pieces, rect-relative
    occ = np.argwhere(lay.max(axis=0) > 0)
    if len(occ) == 0: raise SystemExit('EMPTY stamp %s' % name)
    (y0, x0), (y1, x1) = occ.min(axis=0), occ.max(axis=0)
    lay = lay[:, y0:y1 + 1, x0:x1 + 1]
    st = dict(w=int(x1 - x0 + 1), h=int(y1 - y0 + 1), layers=lay.tolist(), src=[s['game'], s['map'], x + int(x0), y + int(y0)])
    if 'door' in s: st['door'] = [s['door'][0] - x - int(x0), s['door'][1] - y - int(y0)]
    if 'solid' in s: st['solid'] = s['solid']
    return st


def render_stamp(st, tid=53, bg=(110, 170, 120, 255)):
    import render as R
    tc = _tc(tid)
    L = np.array(st['layers'])
    im = Image.new('RGBA', (st['w'] * 32, st['h'] * 32), bg)
    for z in range(3):
        for yy in range(st['h']):
            for xx in range(st['w']):
                t = int(L[z, yy, xx])
                if t >= RC.VBASE:
                    try: t = int(RC.resolve(np.array([[t]]), tid)[0, 0])
                    except ValueError: t = 0
                if t > 0:
                    ti = tc.tile(t)
                    if ti is not None: im.alpha_composite(ti, (xx * 32, yy * 32))
    if 'door' in st:
        dx, dy = st['door']; ImageDraw.Draw(im).rectangle([dx * 32, dy * 32, dx * 32 + 31, dy * 32 + 31], outline=(255, 0, 0, 255), width=2)
    return im


_TCS = {}


def _tc(tid):
    import render as R
    if tid not in _TCS: _TCS[tid] = R.TileCache(R.tilesets()[tid])
    return _TCS[tid]


def contact(stamps, out, width=1500, scale=0.5):
    ims = [(n, render_stamp(st)) for n, st in stamps.items()]
    ims = [(n, i.resize((max(1, int(i.width * scale)), max(1, int(i.height * scale))))) for n, i in ims]
    rows = []; row = []; ws = 0
    for n, i in ims:
        if ws + i.width > width and row: rows.append(row); row = []; ws = 0
        row.append((n, i)); ws += max(i.width, 60) + 8
    rows.append(row)
    H = sum(max(i.height for _, i in r) + 14 for r in rows if r)
    sh = Image.new('RGB', (width, H), (35, 35, 45)); d = ImageDraw.Draw(sh); y = 0
    for r in rows:
        x = 0
        for n, i in r:
            sh.paste(i.convert('RGB'), (x, y + 12)); d.text((x, y), n[:18], fill=(255, 255, 0)); x += max(i.width, 60) + 8
        y += max(i.height for _, i in r) + 14
    sh.save(out); print('sheet', out, sh.size)


def main():
    a = sys.argv[1:]
    spec = yaml.safe_load(open(os.path.join(HERE, 'rstamps.yaml')))
    out = json.load(open(OUTF)) if os.path.exists(OUTF) else {}
    names = [n for n in a if not n.startswith('--') and not n.endswith('.png')] or list(spec)
    for n in names:
        out[n] = mine(n, spec[n])
    out = {n: v for n, v in out.items() if n in spec}
    json.dump(out, open(OUTF, 'w'))
    print('stamps_rj:', len(out))
    if '--sheet' in a:
        contact({n: out[n] for n in names}, a[a.index('--sheet') + 1])


if __name__ == '__main__':
    main()
