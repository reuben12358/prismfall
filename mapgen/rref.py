#!/usr/bin/env python3
"""rref.py - read-only access to the downloaded Rejuvenation / Reborn / Desolation games (MAPGEN 2h).
Never executes anything from /home/claude/ref: maps and tilesets are parsed with our safe rmarshal reader.

    python3 -I rref.py render <game> <map id> out.png [scale] [--crop x,y,w,h] [--grid]
    python3 -I rref.py stats  <game> <map id>            # most common tiles per layer
    python3 -I rref.py maps   <game> <tileset id ...>    # maps drawn with these tilesets

Library: tileset(game, id) -> dict like data/tilesets.json entries (gfx root attached),
         load(game, id) -> (layers int32 [3,H,W], map object), tilecache(game, tid)."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import rmarshal as M
import render as R
from PIL import Image, ImageDraw
Image.MAX_IMAGE_PIXELS = None

GAMES = {'rejuvenation': '/home/claude/ref/games/rejuvenation', 'reborn': '/home/claude/ref/games/reborn',
         'desolation': '/home/claude/ref/games/desolation'}
DUMPS = '/home/claude/ref/art/dumps'
_TS = {}; _SUM = {}; _MAPS = {}


def tilesets(game):
    if game not in _TS:
        _TS[game] = {t['id']: t for t in json.load(open(os.path.join(DUMPS, game, 'tilesets.json'))) if t}
    return _TS[game]


def tileset(game, tid):
    t = dict(tilesets(game)[tid]); t['_gfx'] = os.path.join(GAMES[game], 'Graphics'); return t


def summary(game):
    if game not in _SUM:
        _SUM[game] = {int(k): v for k, v in json.load(open(os.path.join(DUMPS, game, 'maps_summary.json'))).items()}
    return _SUM[game]


def load(game, mid):
    key = (game, mid)
    if key not in _MAPS:
        m = M.load_file(os.path.join(GAMES[game], 'Data', 'Map%03d.rxdata' % mid))
        _MAPS[key] = (m.data.data.astype(np.int32), m)
    return _MAPS[key]


class TC(R.TileCache):
    """TileCache reading a game's own Graphics folder (never maps_out)."""
    def __init__(self, ts):
        root = ts['_gfx']
        def g(sub, n):
            p = os.path.join(root, sub, n + '.png'); return p if n and os.path.exists(p) else None
        self.ts = ts
        p = g('Tilesets', ts['tileset_name'])
        self.sheet = Image.open(p).convert('RGBA') if p else None
        self.autos = [Image.open(g('Autotiles', n)).convert('RGBA') if g('Autotiles', n) else None for n in ts['autotile_names']]
        self.cache = {}


_TC = {}


def tilecache(game, tid):
    if (game, tid) not in _TC: _TC[(game, tid)] = TC(tileset(game, tid))
    return _TC[(game, tid)]


def render_layers(L, tc, scale=1.0, crop=None, grid=False):
    _, H, W = L.shape
    x0, y0, w, h = crop or (0, 0, W, H)
    im = Image.new('RGBA', (w * 32, h * 32), (0, 0, 0, 255))
    for z in range(3):
        for y in range(y0, y0 + h):
            for x in range(x0, x0 + w):
                t = int(L[z, y, x])
                if t:
                    ti = tc.tile(t)
                    if ti is not None: im.alpha_composite(ti, ((x - x0) * 32, (y - y0) * 32))
    if grid:
        grid_overlay(im, x0, y0, w, h)
    if scale != 1.0: im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
    return im


def grid_overlay(im, x0, y0, w, h, S=32):
    d = ImageDraw.Draw(im)
    for x in range(x0, x0 + w + 1):
        if x % 5 == 0:
            c = (255, 40, 40, 255) if x % 10 == 0 else (255, 255, 0, 200)
            d.line([((x - x0) * S, 0), ((x - x0) * S, h * S)], fill=c, width=2 if x % 10 == 0 else 1)
    for y in range(y0, y0 + h + 1):
        if y % 5 == 0:
            c = (255, 40, 40, 255) if y % 10 == 0 else (255, 255, 0, 200)
            d.line([(0, (y - y0) * S), (w * S, (y - y0) * S)], fill=c, width=2 if y % 10 == 0 else 1)
    for x in range(x0, x0 + w):
        for y in range(y0, y0 + h):
            if x % 5 == 0 and y % 5 == 0:
                d.rectangle([(x - x0) * S, (y - y0) * S, (x - x0) * S + 34, (y - y0) * S + 11], fill=(0, 0, 0, 255))
                d.text(((x - x0) * S + 1, (y - y0) * S), '%d,%d' % (x, y), fill=(255, 255, 255, 255))


def main():
    a = sys.argv[1:]
    cmd, game = a[0], a[1]
    if cmd == 'render':
        L, m = load(game, int(a[2]))
        crop = tuple(map(int, a[a.index('--crop') + 1].split(','))) if '--crop' in a else None
        sc = float(a[4]) if len(a) > 4 and not a[4].startswith('--') else 0.5
        render_layers(L, tilecache(game, m.tileset_id), sc, crop, '--grid' in a).convert('RGB').save(a[3])
        print(a[3], m.tileset_id, L.shape)
    elif cmd == 'stats':
        from collections import Counter
        L, m = load(game, int(a[2]))
        print('tileset', m.tileset_id, 'size', L.shape)
        for z in range(3):
            c = Counter(L[z].reshape(-1).tolist()); print('L%d' % z, c.most_common(25))
    elif cmd == 'doors':             # events with a Transfer Player command (doors, warps)
        L, m = load(game, int(a[2]))
        for ev in sorted(m.events.values(), key=lambda e: (e.y, e.x)):
            if any(c.code == 201 for p in ev.pages for c in p.list):
                print('door/warp at %d,%d  %s' % (ev.x, ev.y, ev.name))
    elif cmd == 'maps':
        ids = set(int(x) for x in a[2:])
        for k, v in sorted(summary(game).items()):
            if v['tileset_id'] in ids: print(k, v['name'], v['tileset_id'], '%dx%d' % (v['w'], v['h']))


if __name__ == '__main__':
    main()
