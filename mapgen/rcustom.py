#!/usr/bin/env python3
"""rcustom.py - the `pf` part of the PF Rejuv sheet: Prismfall's own pieces (giant trees, Briarwick's elder tree, silk
garlands and lanterns, the quay oil lamps, the moored Dovetail, material variants) ported from tileset 33 so they can
sit in Rejuvenation-family maps (MAPGEN 2h).  Greens of the tree art are re-graded onto Sheridan_2's foliage ramp so
the canopies match the forest around them (ART_DIRECTION 6: remap each source colour once, grid untouched).

    python3 -I rcustom.py && python3 -I rcompose.py
Writes data/rj_custom.png (256 x 32*CUSTOM_ROWS), data/rj_custom.json (passage/priority/tag per index, the 33->pf id
map) and data/stamps_rjc.json (stamps `pf_<name>` in PF Rejuv ids)."""
import os, sys, json, colorsys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image
import render as R, rcompose as RC, rdraw
HERE = os.path.dirname(os.path.abspath(__file__))
OFF33 = json.load(open(os.path.join(HERE, 'data', 'compose_offsets.json')))
C2, C3 = OFF33['custom2']['offset'], OFF33['custom3']['offset']
SV = json.load(open(os.path.join(HERE, 'data', 'stamps_v.json')))
SM = json.load(open(os.path.join(HERE, 'data', 'stamps_m.json')))
TREES = ['g_elder', 'g_tree6', 'g_tree4', 'g_tree4p', 'g_tree2']
PROPS = ['p_lantern', 'p_silk', 'p_silk1', 'p_strand_w', 'p_strand_p', 'p_web', 'p_web1', 'p_loom', 'p_vat_b', 'p_vat_r',
         'p_vat_y', 'p_laundry', 'p_net', 'p_awning']
MATS = ['stairs_log@33', 'stairs_plank@33', 'signpost@33', 'lantern@33', 'logbench@33', 'barricade@33', 'glow@33']
SINGLES = {'lamp_off': C2 + 166, 'lamp_on': C2 + 167, 'garl_plain': C3 + 184, 'garl_pennant': C3 + 185,
           'garl_lantern': C3 + 186, 'garl_tufts': C3 + 187}


EXTRA33 = {'hs_jonquil_26': 'hb_boat1', 'hs_jonquil_29': 'hb_boat2', 'hs_jonquil_31': 'hb_boat3', 'hs_jonquil_33': 'hb_boat4',
           'hs_jonquil_15': 'hb_post1', 'hs_jonquil_16': 'hb_post2', 'hs_jonquil_19': 'hb_posts2', 'hs_jonquil_20': 'hb_posts3',
           'hs_jonquil_05': 'hb_buoy', 'hs_jonquil_07': 'hb_buoy2', 'hs_jonquil_32': 'hb_tubs', 'hs_jonquil_35': 'hb_fish',
           'hs_jonquil_36': 'hb_barrel', 'hs_jonquil_37': 'hb_barrel2', 'hs_jonquil_38': 'hb_barrels', 'hs_jonquil_13': 'hb_plank',
           'tp_stall_02': 'hb_tables', 'tp_stall_05': 'hb_rugline', 'tp_stall_06': 'hb_rugline2', 'tp_stall_08': 'hb_washline',
           'tp_stall_13': 'hb_boxes', 'tp_stall_16': 'hb_boxes2', 'tp_barrel_07': 'hb_shed', 'tp_barrel_03': 'hb_cask',
           'tp_barrel_06': 'hb_keg', 'tp_stall_21': 'hb_dyeline', 'tp_stall_01': 'hb_crates4'}

EXTRA33_B = {'hs_jonquil_12': 'hb_wheelhouse', 'p_banner3': 'hb_banner', 'hs_jonquil_34': 'hb_fishstall', 'hs_jonquil_09': 'hb_lamp2'}


def sheridan_ramp():
    """Sheridan_2's tree greens, dark -> light (from the 3x4 forest tree, rows 26-29)."""
    im = Image.open(os.path.join(RC.RR.GAMES['rejuvenation'], 'Graphics', 'Tilesets', 'Sheridan_2.png')).convert('RGB')
    cols = {}
    for y in range(26 * 32, 30 * 32):
        for x in range(0, 96):
            r, g, b = im.getpixel((x, y))
            h, s, v = colorsys.rgb_to_hsv(r / 255., g / 255., b / 255.)
            if 0.22 < h < 0.48 and s > 0.25: cols[(r, g, b)] = v
    return sorted(cols, key=lambda c: cols[c])


def snowify(im, mode):
    """recolour a tile: greens -> snow / hoarfrost ramp by brightness; browns -> slate (cliffs) or frosted bark (trees)"""
    px = im.load()
    for yy in range(im.height):
        for xx in range(im.width):
            r, g, b, a = px[xx, yy]
            if not a: continue
            h, s_, v = colorsys.rgb_to_hsv(r / 255., g / 255., b / 255.)
            if 0.17 < h < 0.5 and s_ > 0.15:                      # foliage / grass -> snow
                if mode == 'tree':
                    v2 = min(1.0, 0.45 + v * 0.62); col = colorsys.hsv_to_rgb(0.58, 0.10 + 0.25 * (1 - v), v2)
                else:
                    v2 = min(1.0, 0.62 + v * 0.42); col = colorsys.hsv_to_rgb(0.60, 0.06 + 0.12 * (1 - v), v2)
            elif (h < 0.13 or h > 0.92) and s_ > 0.12:               # earth / bark -> slate blue-grey
                col = colorsys.hsv_to_rgb(0.62, 0.16 + 0.1 * s_, v * (0.92 if mode == 'cliff' else 0.98))
            else:
                continue
            px[xx, yy] = tuple(int(c * 255) for c in col) + (a,)
    return im


# derived snow tiles: (key, game, source sheet, source ids, mode)
SNOW = [('cliff_sh', 'rejuvenation', 'Sheridan_2', list(range(1624, 1664)), 'cliff'),
        ('cliff_ak', 'rejuvenation', 'Route 4', list(range(440, 480)), 'cliff'),
        ('tree_sh', 'rejuvenation', 'Sheridan_2', list(range(592, 624)) + list(range(1504, 1536)), 'tree'),
        ('grass_sh', 'rejuvenation', 'Sheridan_2', [646, 647, 654, 655, 390, 391], 'grass'),
        ('cave_sh', 'rejuvenation', 'Sheridan_2', list(range(616, 648)), 'cliff')]


# map builder 10: chalk copies of the cliff kits (Lacecliff Walk's white cliffs): earth and rock -> chalk by brightness
CHALK = [('cliff_ak', 'rejuvenation', 'Route 4', list(range(440, 480)), 'chalk'),
         ('cliff_sh', 'rejuvenation', 'Sheridan_2', list(range(1624, 1664)), 'chalk'),
         ('rock_ak', 'rejuvenation', 'Route 4', [384 + r_ * 8 + c_ for r_ in (17, 18, 19) for c_ in (0, 1, 2)] +
          [384 + r_ * 8 + c_ for r_ in (39, 40) for c_ in (5, 6)] + [384 + r_ * 8 + 2 for r_ in (20, 21)], 'chalk'),
         ('dune_ak', 'rejuvenation', 'Route 4', list(range(440, 480)), 'dune'),
         ('drock_ak', 'rejuvenation', 'Route 4', [384 + r_ * 8 + c_ for r_ in (17, 18, 19) for c_ in (0, 1, 2)] +
          [384 + r_ * 8 + c_ for r_ in (39, 40) for c_ in (5, 6)] + [384 + r_ * 8 + 2 for r_ in (20, 21)], 'dune'),
         # map builder 12: the war desert's rocks with no moss at all (the dune copies keep their grass tufts for Marram Down)
         ('srock_ak', 'rejuvenation', 'Route 4', [384 + r_ * 8 + c_ for r_ in (17, 18, 19) for c_ in (0, 1, 2)] +
          [384 + r_ * 8 + c_ for r_ in (39, 40) for c_ in (5, 6)] + [384 + r_ * 8 + 2 for r_ in (20, 21)], 'sand')]
# chalk rock stamps (sheet rectangles of Route 4, as in rstamps.yaml's nt_rock_big / nt_boulder / nt_pebbles)
CHALK_STAMPS = {'ck_rock_big': (0, 17, 3, 3, 1), 'ck_boulder': (5, 39, 2, 2, 0), 'ck_pebbles': (2, 20, 1, 2, 0),
                'dk_rock_big': (0, 17, 3, 3, 1), 'dk_boulder': (5, 39, 2, 2, 0), 'dk_pebbles': (2, 20, 1, 2, 0),
                'sk_rock_big': (0, 17, 3, 3, 1), 'sk_boulder': (5, 39, 2, 2, 0), 'sk_pebbles': (2, 20, 1, 2, 0)}
CHALK_RAMP = [(92, 90, 104), (128, 126, 136), (162, 160, 164), (190, 188, 184), (214, 212, 204), (234, 232, 224)]
DUNE_RAMP = [(112, 84, 58), (146, 116, 80), (176, 148, 102), (200, 176, 126), (220, 200, 148), (234, 218, 170)]


SNOW_MORE = [(0, 13, 3, 4), (3, 14, 3, 4), (0, 30, 3, 4), (0, 0, 2, 3), (2, 0, 2, 3), (6, 17, 2, 3)]   # Route 4: teal oaks, the blue oak, pines
SILK_TREES = [[[592, 593, 0], [600, 601, 602], [608, 609, 610], [616, 617, 618]],
              [[1504, 1505, 1506], [1512, 1513, 1514], [1520, 1521, 1522], [1528, 1529, 1530]]]


def silkwrap(im, seed=1):
    """wrap a tree in silk: sagging white strands from crown to crown, a sheet caught on one side, a few cocoons; only
    over the tree's own pixels (the lattice still reads as one canopy)"""
    import random as _r, math as _m
    rng = _r.Random(seed); px = im.load(); W_, H_ = im.size
    def put(x, y, c, a):
        x, y = int(x), int(y)
        if 0 <= x < W_ and 0 <= y < H_ and px[x, y][3]:
            r0, g0, b0, a0 = px[x, y]; t = a / 255.0
            px[x, y] = (int(r0 * (1 - t) + c[0] * t), int(g0 * (1 - t) + c[1] * t), int(b0 * (1 - t) + c[2] * t), a0)
    for k in range(5):                                     # strands
        x0, y0 = rng.uniform(0, W_ * 0.4), rng.uniform(4, H_ * 0.55)
        x1, y1 = rng.uniform(W_ * 0.6, W_), rng.uniform(4, H_ * 0.55)
        sag = rng.uniform(6, 18)
        for i in range(160):
            t = i / 159.0; x = x0 + (x1 - x0) * t; y = y0 + (y1 - y0) * t + sag * _m.sin(_m.pi * t)
            put(x, y, (248, 250, 255), 210); put(x, y + 1, (190, 196, 214), 120)
    for k in range(2):                                     # a sheet of silk caught in the crown
        cx, cy = rng.uniform(W_ * 0.2, W_ * 0.8), rng.uniform(H_ * 0.15, H_ * 0.45)
        for y in range(int(cy), int(cy + 22)):
            for x in range(int(cx - 8), int(cx + 8)):
                if (x + y) % 3: put(x, y, (240, 244, 252), 110)
    for k in range(3):                                     # cocoons
        cx, cy = rng.uniform(8, W_ - 8), rng.uniform(H_ * 0.3, H_ * 0.62)
        for y in range(int(cy), int(cy + 7)):
            for x in range(int(cx - 2), int(cx + 3)): put(x, y, (236, 236, 244), 230)
        put(cx - 2, cy + 3, (160, 164, 186), 255)
    return im


TALL_DYE = [('tall_r', (214, 64, 80)), ('tall_b', (72, 104, 214)), ('tall_y', (236, 198, 56))]


def dyegrass(im, col):
    """tall grass in flower: the tips of the blades (its two lightest greens) take the field's dye colour"""
    px = im.load(); cols = {}
    for yy in range(im.height):
        for xx in range(im.width):
            r, g, b, a = px[xx, yy]
            if a: cols[(r, g, b)] = cols.get((r, g, b), 0) + 1
    greens = sorted([c for c in cols if c[1] > c[0] and c[1] > c[2]], key=lambda c: sum(c))
    tips = set(greens[-2:])
    hi = tuple(min(255, int(v * 1.15) + 20) for v in col)
    for yy in range(im.height):
        for xx in range(im.width):
            r, g, b, a = px[xx, yy]
            if a and (r, g, b) in tips: px[xx, yy] = (hi if (xx + yy) % 3 == 0 else col) + (a,)
    return im


def chalkify(im, ramp=None, greens=False):
    """recolour a cliff tile: browns / mauves -> the chalk ramp (dark crevices stay a cool grey); grass caps untouched
    (greens=True, map builder 12: moss and grass go to the ramp too, for the war desert)"""
    px = im.load()
    for yy in range(im.height):
        for xx in range(im.width):
            r, g, b, a = px[xx, yy]
            if not a: continue
            h, s_, v = colorsys.rgb_to_hsv(r / 255., g / 255., b / 255.)
            if (h < 0.14 or h > 0.85) and s_ > 0.08 or (greens and 0.14 <= h <= 0.6 and s_ > 0.12):
                t = max(0.0, min(0.999, (v - 0.20) / 0.50))
                ramp_ = ramp or CHALK_RAMP
                px[xx, yy] = ramp_[int(t * len(ramp_))] + (a,)
    return im


def main():
    ts33 = R.tilesets()[33]; tc = R.TileCache(ts33)
    want = {}
    for n in TREES + PROPS:
        want[n] = SV[n]
    for n in MATS:
        want[n.replace('@33', '')] = SM[n]
    ship = json.load(open(os.path.join(HERE, 'data', 'ship_moored.json')))
    ids = set()
    for st in want.values():
        ids |= {t for t in np.array(st['layers']).reshape(-1).tolist() if t >= 384}
    ids |= set(SINGLES.values())
    off_ship = OFF33['ship_moored']['offset']
    ids |= {off_ship + i for _, _, _, i in ship}
    ids = sorted(ids)
    if len(ids) > RC.CUSTOM_ROWS * 8: raise SystemExit('custom part too small: %d tiles' % len(ids))
    tree_ids = {t for n in TREES for t in np.array(want[n]['layers']).reshape(-1).tolist() if t >= 384}
    ramp = sheridan_ramp()
    sheet = Image.new('RGBA', (256, RC.CUSTOM_ROWS * 32), (0, 0, 0, 0))
    idmap = {}; props = {}
    cache = {}
    for i, t in enumerate(ids):
        im = tc.tile(t)
        if im is None: continue
        im = im.copy()
        if t in tree_ids:                     # foliage greens -> Sheridan ramp by brightness; bark and windows untouched
            px = im.load()
            for yy in range(32):
                for xx in range(32):
                    r, g, b, a = px[xx, yy]
                    if not a: continue
                    k = (r, g, b)
                    if k not in cache:
                        h, s, v = colorsys.rgb_to_hsv(r / 255., g / 255., b / 255.)
                        cache[k] = ramp[min(len(ramp) - 1, int(v * len(ramp)))] if (0.18 < h < 0.45 and s > 0.2) else k
                    px[xx, yy] = cache[k] + (a,)
        sheet.paste(im, ((i % 8) * 32, (i // 8) * 32))
        idmap[t] = i
        props[i] = (ts33['passages'][t], ts33['priorities'][t], ts33['terrain_tags'][t])
    snow = {}
    n0 = len(ids)
    k = n0
    for key, game, sheetname, srcs, mode in SNOW:
        src = Image.open(os.path.join(RC.RR.GAMES[game], 'Graphics', 'Tilesets', sheetname + '.png')).convert('RGBA')
        t = RC.RR.tileset(game, {'Sheridan_2': 126, 'Route 4': 211}[sheetname])
        for sid in srcs:
            i = sid - 384; tile = src.crop(((i % 8) * 32, (i // 8) * 32, (i % 8) * 32 + 32, (i // 8) * 32 + 32))
            tile = snowify(tile.copy(), mode)
            sheet.paste(tile, ((k % 8) * 32, (k // 8) * 32))
            props[k] = (t['passages'][sid], t['priorities'][sid], t['terrain_tags'][sid] if t['terrain_tags'][sid] <= 16 else 0)
            snow['%s:%d' % (key, sid)] = k; k += 1
    if k > RC.CUSTOM_ROWS * 8: raise SystemExit('custom part too small: %d tiles' % k)
    # snowy giant trees: every tree tile again, snowified (ice-glazed boles for the Rimewood)
    tree_snow = {}
    for t in sorted(tree_ids):
        im = tc.tile(t)
        if im is None: continue
        sheet.paste(snowify(im.copy(), 'tree'), ((k % 8) * 32, (k // 8) * 32))
        props[k] = props[idmap[t]]; tree_snow[t] = k; k += 1
    if k > RC.CUSTOM_ROWS * 8: raise SystemExit('custom part too small: %d tiles' % k)
    # hand-drawn pieces (rdraw.py): Frostwick's whalebone longhouses, rib gate, walkways, smoke, stalls, props, the
    # frozen fall.  Appended after everything above, so earlier ids never move.
    drawn = {}
    seen = {}
    def draw_in(table, k, dedup=False):
        for n, (im, code, door) in table.items():
            big = im.resize((im.width * 2, im.height * 2), Image.NEAREST)
            h, w = len(code), len(code[0])
            lay = [[[0] * w for _ in range(h)] for _ in range(3)]
            for ty in range(h):
                for tx in range(w):
                    c = code[ty][tx]
                    if c == '.': continue
                    tile = big.crop((tx * 32, ty * 32, tx * 32 + 32, ty * 32 + 32))
                    if tile.getbbox() is None: continue
                    z, p_, q_ = rdraw.CODE[c][:3]
                    pr = (p_, q_, rdraw.CODE[c][3] if len(rdraw.CODE[c]) > 3 else 0)
                    if dedup:
                        h_ = (tile.tobytes(), pr)
                        if h_ in seen: lay[z][ty][tx] = seen[h_]; continue
                        seen[h_] = k
                    sheet.paste(tile, ((k % 8) * 32, (k // 8) * 32))
                    props[k] = pr; lay[z][ty][tx] = k; k += 1
            drawn[n] = (w, h, lay, door)
        return k
    k = draw_in(rdraw.pieces(), k)
    # harbour and market props from tileset 33 (Ekat's Jonquil pieces, Magiscarf stalls): appended AFTER the drawn
    # pieces so no earlier id moves (map builder 7).  Add new names at the END of EXTRA33 only.
    extra = {}
    def add33(t, k):
        """one tileset-33 tile appended at k (once); returns (index, k)"""
        if ('x', t) not in idmap:
            im = tc.tile(t)
            if im is None: return 0, k
            sheet.paste(im, ((k % 8) * 32, (k // 8) * 32))
            props[k] = (ts33['passages'][t], ts33['priorities'][t], 0); idmap[('x', t)] = k; k += 1
        return idmap[('x', t)], k
    def add_stamps(table, k):
        for n in table:
            st = SV[n]; L = np.array(st['layers']); out_l = np.zeros_like(L)
            for (z, yy, xx), t in np.ndenumerate(L):
                if t < 384: continue
                out_l[z, yy, xx], k = add33(int(t), k)
            extra[table[n]] = (st['w'], st['h'], out_l.tolist())
        return k
    k = add_stamps(EXTRA33, k)
    k = draw_in(rdraw.pieces_late(), k)
    # third block (after the late pieces): the Dovetail's own deck art (ship_art config `dovetail`, map 109) and deck props
    k = add_stamps(EXTRA33_B, k)
    ship_d = json.load(open(os.path.join(HERE, 'data', 'ship_dovetail.json'))); off_d = OFF33['dovetail']['offset']; dove = []
    for x, y, z, i in ship_d:
        t, k = add33(off_d + i, k); dove.append([x, y, z, t])
    idmap = {t: i for t, i in idmap.items() if not isinstance(t, tuple)}
    k = draw_in(rdraw.pieces_late2(), k)
    k0 = k
    k = draw_in(rdraw.pieces_late3(), k, dedup=True)       # map builder 8: the city kit (tdraw.py), deduplicated
    print('city kit tiles', k - k0)
    k0 = k
    k = draw_in(rdraw.pieces_late4(), k, dedup=True)       # map builder 10: the nature kit (ndraw.py), deduplicated
    print('nature kit tiles', k - k0)
    chalk = {}                                             # map builder 10: chalk copies of the cliff kits (Lacecliff)
    for key, game, sheetname, srcs, mode in CHALK:
        src = Image.open(os.path.join(RC.RR.GAMES[game], 'Graphics', 'Tilesets', sheetname + '.png')).convert('RGBA')
        t = RC.RR.tileset(game, {'Sheridan_2': 126, 'Route 4': 211}[sheetname])
        for sid in srcs:
            i = sid - 384; tile = src.crop(((i % 8) * 32, (i // 8) * 32, (i % 8) * 32 + 32, (i // 8) * 32 + 32))
            sheet.paste(chalkify(tile.copy(), DUNE_RAMP if mode in ('dune', 'sand') else None, greens=(mode == 'sand')), ((k % 8) * 32, (k // 8) * 32))
            props[k] = (t['passages'][sid], t['priorities'][sid], t['terrain_tags'][sid] if t['terrain_tags'][sid] <= 16 else 0)
            chalk['%s:%d' % (key, sid)] = k; k += 1
    silked = {}                                            # map builder 10: Gossamer Wood's silk-wrapped lattice trees
    sh2s = Image.open(os.path.join(RC.RR.GAMES['rejuvenation'], 'Graphics', 'Tilesets', 'Sheridan_2.png')).convert('RGBA')
    t126s = RC.RR.tileset('rejuvenation', 126)
    for grid in SILK_TREES:
        h_, w_ = len(grid), len(grid[0])
        big = Image.new('RGBA', (w_ * 32, h_ * 32), (0, 0, 0, 0))
        for ty, row in enumerate(grid):
            for tx, sid in enumerate(row):
                if not sid: continue
                i = sid - 384; big.paste(sh2s.crop(((i % 8) * 32, (i // 8) * 32, (i % 8) * 32 + 32, (i // 8) * 32 + 32)), (tx * 32, ty * 32))
        big = silkwrap(big, seed=grid[0][0] or grid[0][1])
        for ty, row in enumerate(grid):
            for tx, sid in enumerate(row):
                if not sid: continue
                sheet.paste(big.crop((tx * 32, ty * 32, tx * 32 + 32, ty * 32 + 32)), ((k % 8) * 32, (k // 8) * 32))
                props[k] = (t126s['passages'][sid], t126s['priorities'][sid], 0)
                silked['silk_sh:%d' % sid] = k; k += 1
    snow2 = {}                                             # map builder 10: more snowy lattice species for the Hoar Road
    r4s = Image.open(os.path.join(RC.RR.GAMES['rejuvenation'], 'Graphics', 'Tilesets', 'Route 4.png')).convert('RGBA')
    t211 = RC.RR.tileset('rejuvenation', 211)
    for (c0, r0, w_, h_) in SNOW_MORE:
        for dy in range(h_):
            for dx in range(w_):
                sid = 384 + (r0 + dy) * 8 + c0 + dx; i = sid - 384
                tile = r4s.crop(((i % 8) * 32, (i // 8) * 32, (i % 8) * 32 + 32, (i // 8) * 32 + 32))
                if tile.getbbox() is None or ('snow_ak:%d' % sid) in snow2: continue
                sheet.paste(snowify(tile.copy(), 'tree'), ((k % 8) * 32, (k // 8) * 32))
                props[k] = (t211['passages'][sid], t211['priorities'][sid], 0)
                snow2['snow_ak:%d' % sid] = k; k += 1
    dyed = {}                                              # map builder 10: the Dyers' Ford's madder / woad / weld fields
    sh2 = Image.open(os.path.join(RC.RR.GAMES['rejuvenation'], 'Graphics', 'Tilesets', 'Sheridan_2.png')).convert('RGBA')
    t126 = RC.RR.tileset('rejuvenation', 126)
    for name, col in TALL_DYE:
        i = 390 - 384; tile = sh2.crop(((i % 8) * 32, (i // 8) * 32, (i % 8) * 32 + 32, (i // 8) * 32 + 32)).copy()
        sheet.paste(dyegrass(tile, col), ((k % 8) * 32, (k // 8) * 32))
        props[k] = (t126['passages'][390], t126['priorities'][390], t126['terrain_tags'][390] if t126['terrain_tags'][390] <= 16 else 0)
        dyed[name] = k; k += 1
    k0 = k
    import cdraw                                           # map builder 13: the cave kit (tileset 57), after everything
    k = draw_in(cdraw.pieces(), k, dedup=True)
    print('cave kit tiles', k - k0)
    if k > RC.CUSTOM_ROWS * 8: raise SystemExit('custom part too small: %d tiles' % k)
    sheet.save(os.path.join(HERE, 'data', 'rj_custom.png'))
    json.dump({'props': {str(k): v for k, v in props.items()}, 'map33': {str(k): v for k, v in idmap.items()},
               'singles': {k: idmap[v] for k, v in SINGLES.items()}, 'snow': snow}, open(os.path.join(HERE, 'data', 'rj_custom.json'), 'w'))
    # stamps in PF Rejuv ids (the pf part's offset is fixed: it is the last part)
    base = json.load(open(os.path.join(HERE, 'data', 'rj_compose.json')))['parts']['pf']['offset']
    out = {}
    for n, st in want.items():
        L = np.array(st['layers'])
        L2 = np.where(L >= 384, np.vectorize(lambda t: base + idmap.get(int(t), 0) if t >= 384 else 0)(L), 0)
        d = dict(w=st['w'], h=st['h'], layers=L2.tolist(), src=['pf33', n])
        if n in ('g_elder',): d['door'] = [6, 11]
        if n == 'g_tree6': d['door'] = [4, 7]
        if n == 'g_tree4': d['door'] = [2, 6]
        out['pf_' + n] = d
    for n in TREES:
        st = want[n]; L = np.array(st['layers'])
        L2 = np.where(L >= 384, np.vectorize(lambda t: base + tree_snow.get(int(t), idmap.get(int(t), 0)) if t >= 384 else 0)(L), 0)
        d = dict(out['pf_' + n]); d['layers'] = L2.tolist(); d['src'] = ['pf33-snow', n]
        out['pf_' + n + '_ice'] = d
    for n, (w, h, lay, door) in drawn.items():
        d = dict(w=w, h=h, layers=[[[base + t if t else 0 for t in row] for row in L] for L in lay], src=['rdraw', n])
        if door: d['door'] = list(door)
        out[n] = d
    for n, (w, h, lay) in extra.items():
        out[n] = dict(w=w, h=h, layers=[[[base + t if t else 0 for t in row] for row in L] for L in lay], src=['pf33x', n])
    out['_snow'] = {k2: base + v for k2, v in snow.items()}
    out['_chalk'] = {k2: base + v for k2, v in chalk.items()}
    out['_dyegrass'] = {k2: base + v for k2, v in dyed.items()}
    out['_silk'] = {k2: base + v for k2, v in silked.items()}
    out['_snow2'] = {k2: base + v for k2, v in snow2.items()}
    r4 = Image.open(os.path.join(RC.RR.GAMES['rejuvenation'], 'Graphics', 'Tilesets', 'Route 4.png')).convert('RGBA')
    for n, (c0, r0, w, h, top) in CHALK_STAMPS.items():
        lay = [[[0] * w for _ in range(h)] for _ in range(3)]
        for dy in range(h):
            for dx in range(w):
                sid = 384 + (r0 + dy) * 8 + c0 + dx; i = sid - 384
                if r4.crop(((i % 8) * 32, (i // 8) * 32, (i % 8) * 32 + 32, (i // 8) * 32 + 32)).getbbox() is None: continue
                lay[2 if dy < top else 1][dy][dx] = base + chalk[('drock_ak:%d' if n.startswith('dk') else 'srock_ak:%d' if n.startswith('sk') else 'rock_ak:%d') % sid]
        out[n] = dict(w=w, h=h, layers=lay, src=['chalk', n])
    out['_ship_dovetail'] = {'tiles': [[x, y, z, base + t] for x, y, z, t in dove if t]}
    out['_ship_moored'] = {'tiles': [[x, y, z, base + idmap[off_ship + i]] for x, y, z, i in ship]}
    out['_singles'] = {k: base + idmap[v] for k, v in SINGLES.items()}
    json.dump(out, open(os.path.join(HERE, 'data', 'stamps_rjc.json'), 'w'))
    print('custom tiles', len(ids), 'stamps', len(out))


if __name__ == '__main__':
    main()
