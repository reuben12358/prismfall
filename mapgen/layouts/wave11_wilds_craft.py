#!/usr/bin/env python3
"""Wave 11 Rejuvenation V14 Map Craft — Scenic Forests, Sacred Bride Grove & Rimewood Wilds.

Exclusive Wave 11 builder for 5 iconic outdoor maps:
  - 524 Gossamer Wood      (90x110, ts 53, :SILKWOOD)  — enchanted silkmoth forest
  - 525 Gossamer Deepwood  (44x40,  ts 53, :SILKWOOD)  — sacred Bride/Moth Tree glade + D2 Lantern Hollow
  - 562 The Rimewood       (48x56,  ts 52, snow wood)  — primeval snowy evergreen ridges + Hoar Pond + D7 Frost Loom
  - 563 Rimewood Glade     (34x30,  ts 52, snow glade) — frozen Silk-fall amphitheater + Snowveil Shrine + slide lake
  - 570 Frostwick          (60x48,  ts 52, snow town)  — lantern-lit Elowen/Isenmar alpine mountain village

Guarantees:
  - 100% immutable HEAD event, warp, NPC, item, sign, door, and metadata parity.
  - 100% exact border-connection seam parity across all connected neighbor maps.
  - 100% D2 Lantern Hollow (525), D7 Frost Loom (562), and Hoar/Silk-fall ice slide puzzle proofs.
  - 0 passguard hits, 0 build.py --strict warnings, byte-identical verify.py roundtrip.

Run:
  /usr/bin/python3 -I mapgen/layouts/wave11_wilds_craft.py [524] [525] [562] [563] [570]
"""
import base64
import copy
import json
import math
import os
import random
import sys
import types
import zlib
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
MAPGEN = os.path.dirname(HERE)
for p in (MAPGEN, HERE):
    if p not in sys.path:
        sys.path.insert(0, p)

import numpy as np
import yaml

import rkit as K
from rkit import C, P1, STAMPS
import rcompose as RC
import craftkit as CK
from routekit import Route
from terrain import vnoise, NB2AUTO, nbits


def fix_vauto_l0(L, game, name):
    """Consolidate an opaque virtual autotile onto L0 ONLY and recompute exact 48-shape NB2AUTO (0 mismatches)."""
    lo = RC.vauto(game, name, 0)
    hi = lo + 48
    m0 = (L[0] >= lo) & (L[0] < hi)
    m1 = (L[1] >= lo) & (L[1] < hi)
    L[0, m1] = L[1, m1]
    L[1, m1] = 0
    mask = m0 | m1
    ys, xs = np.where(mask)
    for y, x in zip(ys, xs):
        L[0, y, x] = lo + NB2AUTO[nbits(mask, int(x), int(y))]

# =============================================================================
# 1. IMMUTABLE HEAD EVENT & METADATA SNAPSHOT (100% exact coordinate parity)
# =============================================================================
HEAD_SPECS_B64 = "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"
_HEAD_CACHE = None


def head_spec(mid):
    global _HEAD_CACHE
    if _HEAD_CACHE is None:
        raw = zlib.decompress(base64.b64decode(HEAD_SPECS_B64)).decode('utf-8')
        _HEAD_CACHE = json.loads(raw)
    return copy.deepcopy(_HEAD_CACHE[str(mid)])


# =============================================================================
# 2. REJUVENATION V14 SPRITE & TERRAIN PALETTES (PIXEL-VERIFIED ON PF Rejuv.png)
# =============================================================================
# Register Kristiline 3x4 snow-laden alpine spruces into CK.SPECIES for dense overlapping winter lattices!
CK.SPECIES['kspA'] = ([[9944, 9945, 9946], [9952, 9953, 9954]], [[9960, 9961, 9962], [9968, 9969, 9970]], 1)
CK.SPECIES['kspB'] = ([[9947, 9948, 9949], [9955, 9956, 9957]], [[9963, 9964, 9965], [9971, 9972, 9973]], 1)
CK.SPECIES['kspC'] = ([[9976, 9977, 9978], [9984, 9985, 9986]], [[9992, 9993, 9994], [10000, 10001, 10002]], 1)
CK.SPECIES['kspD'] = ([[9979, 9980, 9981], [9987, 9988, 9989]], [[9995, 9996, 9997], [10003, 10004, 10005]], 1)

# Rich winter alpine evergreen lattice palettes (dominant pointy Kristiline spruces + deep teal/blue frosted oaks)
ALPINE_WOODS = [
    {'kspA': 5, 'kspB': 4, 'snowteal': 3, 'snow0': 2},
    {'kspC': 4, 'kspD': 4, 'snowteal2': 3, 'snowblue': 2},
    {'kspA': 4, 'kspC': 3, 'snowblue': 3, 'snow1': 2},
    {'kspB': 4, 'kspD': 4, 'snow0': 3, 'snowteal': 2},
]

# Forest lattice palettes (rich multi-canopy emerald, teal, silk-draped & deep shade oaks)
GOSSAMER_WOODS = [
    {'sh1': 4, 'teal2': 3, 'silk1': 3},
    {'sh0': 3, 'teal': 3, 'silk0': 3, 'olive': 1},
    {'teal': 3, 'teal2': 3, 'sh1': 3, 'silk1': 2},
    {'silk0': 3, 'silk1': 3, 'sh0': 2, 'olive': 2},
    {'olive': 3, 'sh1': 3, 'teal2': 2, 'lime': 1},
]
DEEP_WOODS = [
    {'silk0': 3, 'silk1': 4, 'sh1': 3},
    {'teal2': 4, 'sh1': 3, 'silk1': 3},
    {'sh0': 2, 'teal': 3, 'silk0': 3, 'olive': 2},
    {'olive': 2, 'sh1': 4, 'teal2': 3},
]
GLASSWOOD_PAL = {'blue': 3, 'purp': 3, 'teal2': 2, 'silk1': 1}

# Pixel-verified multi-tile raw sprites: (top_rows on L2 pri=5, bot_rows on L1 pas=15)
KF_TEAL_PINE_A = ([[9833, 9834], [9841, 9842]], [[9849, 9850], [9857, 9858]])
KF_TEAL_PINE_B = ([[9837, 9838], [9845, 9846]], [[9853, 9854], [9861, 9862]])
KF_SPRUCE_A = ([[9944, 9945, 9946], [9952, 9953, 9954]], [[9960, 9961, 9962], [9968, 9969, 9970]])
KF_SPRUCE_B = ([[9947, 9948, 9949], [9955, 9956, 9957]], [[9963, 9964, 9965], [9971, 9972, 9973]])
KF_SHRUB_A = ([[9864, 9865]], [[9872, 9873]])
KF_SHRUB_B = ([[9880, 9881]], [[9888, 9889]])
KF_SHRUB_LOW = ([], [[9874, 9875]])
KF_CRYS_MONO = ([[9868, 9869]], [[9876, 9877]])
KF_CRYS_STAR = ([[9884, 9887]], [[9892, 9895]])
KF_CRYS_BLADES = ([[9886, 9885]], [[9894, 9893]])
KF_BOULDER = ([[9634, 9635]], [[9642, 9643]])
KF_LANTERN = ([[9640]], [[9648]])

SH_SPRUCE = ([[5612, 5613]], [[5620, 5621], [5628, 5629]])
SH_CYPRESS = ([[5614]], [[5622]])
SH_PINE_TALL = ([[5019, 5020], [5027, 5028]], [[5035, 5036]])

# Bordered Kristiline glacial snow-edged ground sets (100% pas=0, pri=0)
CERULEAN_3X3 = (9512, 9513, 9514, 9520, 9521, 9522, 9528, 9529, 9530)
CERULEAN_IN = (9515, 9516, 9523, 9524)
PERI_3X3 = (9896, 9897, 9898, 9904, 9905, 9906, 9912, 9913, 9914)
PERI_IN = (9899, 9900, 9907, 9908)

# Forest walkable accents (pas=0/64, pri=0) and solid lotus water-surface lilies (pas=15, pri=0)
PETAL_TILE = 5723
GLOW_MUSH = [451, 452, 453, 454, 459, 460, 461, 462]
LOTUS_TILES = [4836, 4837, 4844, 4845]
ROSE_TILE = 5642
ICES = [STAMPS['fw_ice%d' % v]['layers'][1][0][0] for v in range(4)]

# 3-row frosted Sheridan snow cliff kit (lip / face / base — crisp, zero flat overhang bloat)
if 'shs3' not in K.KITS:
    K.KITS['shs3'] = dict(K.KITS['shs'], rows=[K.KITS['shs']['rows'][0], K.KITS['shs']['rows'][1], K.KITS['shs']['rows'][3]])


# =============================================================================
# 3. SHARED REJUVENATION V14 CRAFT HELPERS
# =============================================================================
def colmap(r, fn):
    return [int(round(fn(x))) for x in range(r.W)]


def bump(x, c, w, a):
    return a * math.exp(-((x - c) / float(w)) ** 2)


def ice_at(x, y):
    n = vnoise(x, y, 77, 1.7)
    return ICES[0] if n < 0.45 else ICES[1] if n < 0.62 else ICES[2] if n < 0.82 else ICES[3]


def snowmap(W, H, mid, kit='shs3'):
    m = K.RMap(W, H, 52, mid, water='Still water snow', kit=kit, grass=K.SNOW_GROUND, decor=K.DECOR_SNOW)
    m.tall = K.SNOW_TALL
    m.STAIRS = tuple(STAMPS['fw_stair_' + k]['layers'][1][0][0] for k in 'lmr')
    m.grass2 = None
    m.lattice = K.RMap.TREES_SNOW
    m.SEAL = int(np.array(STAMPS['fw_stone']['layers']).max())
    m.auto = {
        'd': ('Packed Snow', 'pf'),
        'e': ('KristilineDirt', 'rejuvenation'),
        'w': ('Still water snow', 'reborn'),
        'o': ('KristilineWatersFrozen', 'rejuvenation'),
        'p': ('Frozen Pond', 'pf'),
        'W': ('Sea deep', 'rejuvenation'),
    }
    m.JOIN = dict(K.RMap.JOIN, o='oW', W='oW', p='p', e='e')
    m.AUTO_Z = dict(K.RMap.AUTO_Z, o=0, W=0, p=0, e=1)
    return m


def smooth_cls(m, c, into='.', passes=2, only=None):
    for _ in range(passes):
        cur = (m.cls == c)
        pad = np.pad(cur, 1)
        n = sum(np.roll(np.roll(pad, dy, 0), dx, 1)[1:-1, 1:-1] for dy in (-1, 0, 1) for dx in (-1, 0, 1)) - cur
        grow = ~cur & (n >= 5)
        shrink = cur & (n <= 3)
        if only is not None:
            grow &= np.isin(m.cls, list(only))
        m.cls[grow] = c
        m.cls[shrink] = into


def reserve_events(m, events, road_mask=None, radius=1, extra=()):
    """Lock exact event cells & clear immediate surroundings so no prop/tree blocks an event."""
    ev_mask = np.zeros((m.H, m.W), bool)
    pts = [tuple(e['at']) for e in events if e.get('at')] + list(extra)
    for ex, ey in pts:
        if not m.inb(ex, ey):
            continue
        m.taken[ey, ex] = True
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                xx, yy = ex + dx, ey + dy
                if m.inb(xx, yy):
                    ev_mask[yy, xx] = True
                    if road_mask is not None and m.cls[yy, xx] in '.dtge':
                        road_mask[yy, xx] = True
    return ev_mask


def seal_unconnected_edges(m, open_cells=(), filler=None):
    """Seal any stray walkable cell on the 4 map perimeter edges not in `open_cells`."""
    import render as R
    ts = R.tilesets()[m.tid]
    pas, pri, tag = ts['passages'], ts['priorities'], ts['terrain_tags']
    keep = set(open_cells)
    f = filler if filler is not None else getattr(m, 'SEAL', P1('nt_bush0'))

    def is_passable(x, y):
        for z in (2, 1, 0):
            t = int(m.L[z, y, x])
            if t == 0 or t >= len(pas):
                continue
            if t < len(tag) and tag[t] in (13, 15):
                continue
            if (pas[t] & 0x0f) == 0x0f:
                return False
            if pri[t] == 0:
                return True
        return True

    H, W = m.H, m.W
    edge_pts = ([(x, 0) for x in range(W)] + [(x, H - 1) for x in range(W)] +
                [(0, y) for y in range(1, H - 1)] + [(W - 1, y) for y in range(1, H - 1)])
    for x, y in edge_pts:
        if (x, y) in keep:
            continue
        if is_passable(x, y):
            if m.L[1, y, x] == 0:
                m.L[1, y, x] = f
            else:
                m.L[2, y, x] = f


def put_sprite(m, x0, y0, top_rows, bot_rows, on='.t', avoid_mask=None, force=False, post_paint=False):
    """Place a verified multi-tile raw sprite (top on L2 pri=5, bot on L1 pas=15)."""
    h_top, h_bot = len(top_rows), len(bot_rows)
    w = len(bot_rows[0])
    if x0 < 0 or y0 < 0 or x0 + w > m.W or y0 + h_top + h_bot > m.H:
        return False
    if not force:
        for dy in range(h_bot):
            for dx in range(w):
                t = bot_rows[dy][dx]
                if not t:
                    continue
                xx, yy = x0 + dx, y0 + h_top + dy
                if m.taken[yy, xx] or m.cliff[yy, xx] or m.cls[yy, xx] not in on:
                    return False
                if avoid_mask is not None and avoid_mask[yy, xx]:
                    return False
                if post_paint and m.L[1, yy, xx] != 0:
                    return False
    for dy in range(h_top):
        for dx in range(w):
            t = top_rows[dy][dx]
            xx, yy = x0 + dx, y0 + dy
            if t and m.inb(xx, yy):
                if post_paint:
                    if m.L[2, yy, xx] == 0:
                        m.L[2, yy, xx] = t
                else:
                    m.over.append((2, xx, yy, t))
    for dy in range(h_bot):
        for dx in range(w):
            t = bot_rows[dy][dx]
            xx, yy = x0 + dx, y0 + h_top + dy
            if t and m.inb(xx, yy):
                if post_paint:
                    m.L[1, yy, xx] = t
                else:
                    m.over.append((1, xx, yy, t))
                m.taken[yy, xx] = True
    return True


def put_overlay_stamp(m, name, x, y, z=2):
    """Paint a transparent overhead atmospheric stamp (cv_shaft, pf_glow, pf_p_web, gw_drape) cleanly onto L2."""
    st = STAMPS[name]
    L = np.array(st['layers'])
    for dy in range(st['h']):
        for dx in range(st['w']):
            t = int(L[:, dy, dx].max())
            xx, yy = x + dx, y + dy
            if t and m.inb(xx, yy) and m.L[z, yy, xx] == 0:
                m.L[z, yy, xx] = t


def paint_bordered_turf(m, mask, tiles_3x3, inner_4, center_alts=()):
    """Paint seamless 3x3 rounded snow-edged glacial turf on L0 (zero hard snow seams!)."""
    nw, n_, ne, w_, c_, e_, sw, s_, se = tiles_3x3
    in_nw, in_ne, in_sw, in_se = inner_4
    H, W = m.H, m.W
    for y in range(H):
        for x in range(W):
            if not mask[y, x]:
                continue
            up = y > 0 and mask[y - 1, x]
            dn = y + 1 < H and mask[y + 1, x]
            lf = x > 0 and mask[y, x - 1]
            rt = x + 1 < W and mask[y, x + 1]
            if not up and not lf:
                t = nw
            elif not up and not rt:
                t = ne
            elif not dn and not lf:
                t = sw
            elif not dn and not rt:
                t = se
            elif not up:
                t = n_
            elif not dn:
                t = s_
            elif not lf:
                t = w_
            elif not rt:
                t = e_
            else:
                ul = y > 0 and x > 0 and mask[y - 1, x - 1]
                ur = y > 0 and x + 1 < W and mask[y - 1, x + 1]
                dl = y + 1 < H and x > 0 and mask[y + 1, x - 1]
                dr = y + 1 < H and x + 1 < W and mask[y + 1, x + 1]
                if not ul and in_nw:
                    t = in_nw
                elif not ur and in_ne:
                    t = in_ne
                elif not dl and in_sw:
                    t = in_sw
                elif not dr and in_se:
                    t = in_se
                elif center_alts and ((x * 7 + y * 13) % 3 == 0):
                    t = center_alts[(x + y) % len(center_alts)]
                else:
                    t = c_
            m.L[0, y, x] = t


def smooth_bool_mask(mask, ok_mask, passes=2):
    m = mask.copy()
    for _ in range(passes):
        pad = np.pad(m, 1, constant_values=False)
        n4 = pad[:-2, 1:-1].astype(int) + pad[2:, 1:-1] + pad[1:-1, :-2] + pad[1:-1, 2:]
        m = (m & (n4 >= 2)) | (~m & ok_mask & (n4 >= 3))
    return m


def paint_forest_ground_depth(m, seed=1, clearings=(), dark_bias=0.42):
    """Layer organic soft-tufted shaded moss & worn sunlit earth using rkit's baked Grassnone transition shapes
    (zero hard 32x32 square checkerboard seams!)."""
    m.grass_var = True
    m.grass_variation(dark=0.52, worn=True)
    worn = [[P1('gr_worn00'), P1('gr_worn01')], [P1('gr_worn10'), P1('gr_worn11')]]
    # Subtle worn sunlit earth strictly in the heart of campfire/village clearings
    for idx, (cx, cy, rx, ry, mode) in enumerate(clearings):
        if mode != 'worn':
            continue
        for y in range(max(0, int(cy - ry - 1)), min(m.H, int(cy + ry + 2))):
            for x in range(max(0, int(cx - rx - 1)), min(m.W, int(cx + rx + 2))):
                if m.cls[y, x] != '.' or m.cliff[y, x]:
                    continue
                q = ((x - cx) / max(1.0, rx)) ** 2 + ((y - cy) / max(1.0, ry)) ** 2
                q += 0.25 * (vnoise(x, y, seed + 910 + idx, 3.0) - 0.5)
                if q <= 0.52:
                    m.L[0, y, x] = worn[y & 1][x & 1]


def infill_forest(r, palettes, pick=None, scale=9.0, seed=0):
    """Zero-polka-dot forest edge packer: 3x2 lattice trees -> 2x2 Sheridan spruces/shrubs -> 1x2 slender cypresses."""
    m = r.m
    rng = random.Random(r.seed * 31 + seed + 7)
    s = r.seed + 1313
    hole = (m.cls == 'T') & ~m.taken & (m.L[1] == 0) & ~m.cliff
    placed = 0
    for y in range(m.H):
        for x in range(m.W):
            if not hole[y, x]:
                continue
            done = False
            # 1. 3x2 full lattice tree
            for ox in (0, -1, -2):
                tx = x + ox
                foot = [(tx + dx, y + dy) for dx in range(3) for dy in range(2)]
                if not all(m.inb(fx, fy) and hole[fy, fx] for fx, fy in foot):
                    continue
                z = vnoise(tx, y, s, scale)
                pal = (pick(tx + 1, y + 1) if pick else None) or palettes[min(len(palettes) - 1, int(z * len(palettes) * 0.999))]
                top, bot, _ = CK.SPECIES[rng.choices(list(pal), list(pal.values()))[0]]
                for dy in range(2):
                    for dx in range(3):
                        X, Y = tx + dx, y - 2 + dy
                        if m.inb(X, Y) and top[dy][dx] and m.L[2, Y, X] == 0:
                            m.L[2, Y, X] = top[dy][dx]
                for dy in range(2):
                    for dx in range(3):
                        X, Y = tx + dx, y + dy
                        if bot[dy][dx]:
                            m.L[1, Y, X] = bot[dy][dx]
                        m.taken[Y, X] = True
                        hole[Y, X] = False
                done = True
                placed += 1
                break
            if done:
                continue
            # 2. 2x2 Sheridan pointy spruce or lush woodland shrub
            for ox in (0, -1):
                if all(m.inb(x + ox + dx, y + dy) and hole[y + dy, x + ox + dx] for dx in range(2) for dy in range(2)):
                    pal = pick(x + ox, y) if pick else None
                    if pal is None and rng.random() < 0.65:
                        top, bot = SH_SPRUCE
                        for dx in range(2):
                            if m.inb(x + ox + dx, y - 1) and m.L[2, y - 1, x + ox + dx] == 0:
                                m.L[2, y - 1, x + ox + dx] = top[0][dx]
                        for dy in range(2):
                            for dx in range(2):
                                X, Y = x + ox + dx, y + dy
                                m.L[1, Y, X] = bot[dy][dx]
                                m.taken[Y, X] = True
                                hole[Y, X] = False
                    else:
                        sh_nm = rng.choice(('nt_shrub0', 'nt_shrub1'))
                        L = np.array(STAMPS[sh_nm]['layers'])
                        for dy in range(2):
                            for dx in range(2):
                                X, Y = x + ox + dx, y + dy
                                for zz in (1, 2):
                                    if L[zz, dy, dx]:
                                        m.L[zz if zz == 1 or m.L[2, Y, X] == 0 else 1, Y, X] = int(L[zz, dy, dx])
                                m.taken[Y, X] = True
                                hole[Y, X] = False
                    done = True
                    placed += 1
                    break
            if done:
                continue
            # 3. 1x2 slender emerald cypress (looks like real layered tree edge, NOT polka-dot bush!)
            if y > 0 and m.L[2, y - 1, x] == 0 and (pick is None or pick(x, y) is None) and rng.random() < 0.78:
                m.L[2, y - 1, x] = SH_CYPRESS[0][0][0]
                m.L[1, y, x] = SH_CYPRESS[1][0][0]
            else:
                b = rng.choice(('nt_bush0', 'nt_bush1'))
                m.L[1, y, x] = int(np.array(STAMPS[b]['layers']).max())
            m.taken[y, x] = True
            hole[y, x] = False
            placed += 1
    return placed


def infill_winter(r, palettes, scale=9.0, seed=0, safe_canopy=False):
    """Zero-bubble-wrap winter canopy packer: 3x2 alpine spruces -> 2x2 Kristiline teal pines -> 2x1 frosted shrubs/boulders."""
    m = r.m
    rng = random.Random(r.seed * 37 + seed + 13)
    s = r.seed + 1313
    hole = (m.cls == 'T') & ~m.taken & (m.L[1] == 0) & ~m.cliff
    if safe_canopy:
        hole &= (m.L[2] == 0)
    placed = 0
    for y in range(m.H):
        for x in range(m.W):
            if not hole[y, x]:
                continue
            done = False
            # 1. 3x2 alpine spruce / winter oak lattice tree
            for ox in (0, -1, -2):
                tx = x + ox
                foot = [(tx + dx, y + dy) for dx in range(3) for dy in range(2)]
                if not all(m.inb(fx, fy) and hole[fy, fx] for fx, fy in foot):
                    continue
                if safe_canopy and not all(m.L[2, y - 2 + dy, tx + dx] == 0 for dx in range(3) for dy in range(4) if m.inb(tx + dx, y - 2 + dy)):
                    continue
                z = vnoise(tx, y, s, scale)
                pal = palettes[min(len(palettes) - 1, int(z * len(palettes) * 0.999))]
                top, bot, _ = CK.SPECIES[rng.choices(list(pal), list(pal.values()))[0]]
                for dy in range(2):
                    for dx in range(3):
                        X, Y = tx + dx, y - 2 + dy
                        t_top = top[dy][dx]
                        if safe_canopy and dy == 0 and dx == 2 and t_top == 0 and top[1][2] == 18388:
                            t_top = 18380
                        if m.inb(X, Y) and t_top and m.L[2, Y, X] == 0:
                            m.L[2, Y, X] = t_top
                for dy in range(2):
                    for dx in range(3):
                        X, Y = tx + dx, y + dy
                        if bot[dy][dx]:
                            m.L[1, Y, X] = bot[dy][dx]
                        m.taken[Y, X] = True
                        hole[Y, X] = False
                done = True
                placed += 1
                break
            if done:
                continue
            # 2. 2x2 Kristiline teal frosted pine (lush dark evergreen mass!)
            for ox in (0, -1):
                if all(m.inb(x + ox + dx, y + dy) and hole[y + dy, x + ox + dx] for dx in range(2) for dy in range(2)):
                    if safe_canopy and not all(m.L[2, y - 2 + dy, x + ox + dx] == 0 for dx in range(2) for dy in range(4) if m.inb(x + ox + dx, y - 2 + dy)):
                        continue
                    top, bot = KF_TEAL_PINE_A if (x + y) % 2 == 0 else KF_TEAL_PINE_B
                    for dy in range(2):
                        for dx in range(2):
                            X, Y = x + ox + dx, y - 2 + dy
                            if m.inb(X, Y) and m.L[2, Y, X] == 0:
                                m.L[2, Y, X] = top[dy][dx]
                    for dy in range(2):
                        for dx in range(2):
                            X, Y = x + ox + dx, y + dy
                            m.L[1, Y, X] = bot[dy][dx]
                            m.taken[Y, X] = True
                            hole[Y, X] = False
                    done = True
                    placed += 1
                    break
            if done:
                continue
            # 3. 2x1 frosted evergreen shrub or snow-capped boulder
            for ox in (0, -1):
                if all(m.inb(x + ox + dx, y) and hole[y, x + ox + dx] for dx in range(2)):
                    sp = rng.choice((KF_SHRUB_A, KF_SHRUB_B, KF_SHRUB_A, KF_BOULDER))
                    top, bot = sp
                    if safe_canopy:
                        # Require 1-tile L2==0 buffer around boulder/shrub top so boulders NEVER bite into snow_pine shoulders!
                        bx0, bx1 = max(0, x + ox - 1), min(m.W, x + ox + 3)
                        by0, by1 = max(0, y - 1), min(m.H, y + 2)
                        if (m.L[2, by0:by1, bx0:bx1] != 0).any():
                            sp = KF_SHRUB_LOW
                            top, bot = sp
                    if top and y > 0:
                        for dx in range(2):
                            if m.L[2, y - 1, x + ox + dx] == 0:
                                m.L[2, y - 1, x + ox + dx] = top[0][dx]
                    for dx in range(2):
                        X = x + ox + dx
                        m.L[1, y, X] = bot[0][dx]
                        m.taken[y, X] = True
                        hole[y, X] = False
                    done = True
                    placed += 1
                    break
            if done:
                continue
            # 4. Tiny 1x1 crevice: crisp frosted boulder/ice crystal (avoid 10555/10556 grey triangle shards when safe_canopy!)
            if safe_canopy:
                m.L[1, y, x] = rng.choice((10551, 10551, 10371))
            else:
                m.L[1, y, x] = rng.choice((10551, 10551, 10555, 10556, 10371))
            m.taken[y, x] = True
            hole[y, x] = False
            placed += 1
    return placed


def dress_water_lotus(m, prob=0.16, seed=1):
    """Scatter pink lotus water lilies (pas=15, zero passguard risk) organically on calm water pockets."""
    rng = random.Random(seed)
    water = (m.cls == 'w')
    for y in range(1, m.H - 1):
        for x in range(1, m.W - 1):
            if not water[y, x] or m.L[1, y, x] != 0 or m.L[2, y, x] != 0 or m.taken[y, x]:
                continue
            # Favor calm coves / banks slightly over center torrent
            nb_land = sum(1 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if not water[y + dy, x + dx])
            p = prob * (1.35 if nb_land >= 1 else 0.7)
            if rng.random() < p:
                m.L[1, y, x] = rng.choice(LOTUS_TILES)


def scatter_petals_and_mushrooms(m, spots_petals=(), spots_mush=(), seed=1):
    """Place walkable blossom petals (5723) and glowing forest mushrooms (451..462) ONLY on safe walkable ground."""
    rng = random.Random(seed)
    for idx, (cx, cy, rx, ry, density) in enumerate(spots_petals):
        for y in range(max(0, int(cy - ry - 1)), min(m.H, int(cy + ry + 2))):
            for x in range(max(0, int(cx - rx - 1)), min(m.W, int(cx + rx + 2))):
                if m.cls[y, x] not in '.d' or m.taken[y, x] or m.cliff[y, x]:
                    continue
                if m.L[1, y, x] != 0 or m.L[2, y, x] != 0:
                    continue
                q = ((x - cx) / max(1.0, rx)) ** 2 + ((y - cy) / max(1.0, ry)) ** 2
                if q <= 1.0 and rng.random() < density * (1.0 - 0.55 * q):
                    m.L[1, y, x] = PETAL_TILE

    for cx, cy, rad, count in spots_mush:
        for k in range(count):
            ang = k * (2.0 * math.pi / count) + 0.25
            x = int(round(cx + math.cos(ang) * rad))
            y = int(round(cy + math.sin(ang) * rad * 0.72))
            if not m.inb(x, y) or m.cls[y, x] not in '.t' or m.taken[y, x] or m.cliff[y, x]:
                continue
            if m.L[1, y, x] == 0 and m.L[2, y, x] == 0:
                m.L[1, y, x] = GLOW_MUSH[k % len(GLOW_MUSH)]


def solid_at(m, cells, kinds=('nt_bush0', 'nt_bush1')):
    import render as R, build as B
    ts = R.tilesets()[m.tid]
    for i, (x, y) in enumerate(cells):
        Lr = RC.resolve(m.L[:, y:y + 1, x:x + 1], m.tid)
        if B.cell_passable(Lr, ts, 0, 0):
            t = int(np.array(STAMPS[kinds[i % len(kinds)]]['layers']).max())
            z = 2 if m.L[1, y, x] else 1
            m.L[z, y, x] = t


def icy_faces(m, p=0.55, seed=4):
    rng = random.Random(seed)
    ic = [STAMPS['fw_icy%d' % i]['layers'][2][0][0] for i in range(3)]
    for (x, y), (kind, k, h) in getattr(m, 'pieces', {}).items():
        if kind == 'row' and k == 1 and m.L[2, y, x] == 0 and rng.random() < p:
            m.L[2, y, x] = rng.choice(ic)


def road_tracks(m, p=0.08, seed=5):
    rng = random.Random(seed)
    tk = [STAMPS['fw_tracks%d' % i]['layers'][1][0][0] for i in range(2)]
    for y, x in np.argwhere(m.cls == 'd'):
        if m.L[2, y, x] == 0 and not m.taken[y, x] and not m.cliff[y, x] and rng.random() < p and m.L[1, y, x] >= 48:
            m.L[0, y, x] = m.L[1, y, x]
            m.L[1, y, x] = rng.choice(tk)


def drifts(m, p, seed=1):
    rng = random.Random(seed)
    ds = [STAMPS['fw_drift%d' % i]['layers'][1][0][0] for i in range(3)]
    open_ = (m.cls == '.') & ~m.taken & (m.L[1] == 0) & (m.L[2] == 0) & ~m.cliff
    pad = np.pad(open_, 1, constant_values=True)
    for y, x in np.argwhere(open_):
        edge = not pad[y:y + 3, x:x + 3].all()
        if rng.random() < p * (2.4 if edge else 0.8):
            m.L[1, y, x] = rng.choice(ds)


def reed_beds(m, n, seed=3, on='.t', avoid_mask=None):
    rng = random.Random(seed)
    cells = [tuple(c) for c in np.argwhere(np.isin(m.cls, list(on)) & ~m.taken & (m.L[1] == 0) & (m.L[2] == 0) & ~m.cliff)]
    rng.shuffle(cells)
    k = 0
    for y, x in cells:
        if k >= n:
            break
        if avoid_mask is not None and avoid_mask[y, x]:
            continue
        if y > 0 and m.L[2, y - 1, x] == 0 and m.L[1, y - 1, x] == 0 and m.cls[y - 1, x] in on and not m.cliff[y - 1, x]:
            st = STAMPS['fw_reeds%d' % rng.randrange(2)]['layers']
            m.L[1, y, x] = st[1][1][0]
            m.L[2, y - 1, x] = st[2][0][0]
            k += 1


def dress_ice(m, p=0.25, seed=2, reeds=True):
    rng = random.Random(seed)
    one = lambda n: STAMPS[n]['layers'][1][0][0]
    cracks = [one('fw_crack%d' % i) for i in range(3)]
    ds = [one('fw_drift%d' % i) for i in range(3)]
    floes = [one('fw_floe%d' % i) for i in range(2)]
    hole = one('fw_hole')
    land = ~np.isin(m.cls, ['I', 'o', 'p', 'w', 'W'])
    pad = np.pad(land, 1)
    for y, x in np.argwhere(m.cls == 'I'):
        if m.L[1, y, x] or m.L[2, y, x] or m.taken[y, x]:
            continue
        shore = pad[y:y + 3, x:x + 3].any()
        rv = rng.random()
        if reeds and shore and rv < 0.35 and m.inb(x, y - 1) and m.L[2, y - 1, x] == 0 and m.cls[y - 1, x] in 'I.t':
            st = STAMPS['fw_reeds%d' % rng.randrange(2)]['layers']
            m.L[1, y, x] = st[1][1][0]
            m.L[2, y - 1, x] = st[2][0][0]
        elif rv < p * 0.55:
            m.L[1, y, x] = rng.choice(cracks)
        elif rv < p * 0.9:
            m.L[1, y, x] = rng.choice(ds)
        elif rv < p:
            m.L[1, y, x] = hole
    for y, x in np.argwhere(np.isin(m.cls, ['o', 'W'])):
        if m.L[1, y, x] == 0 and rng.random() < p * 0.32 and not pad[y:y + 3, x:x + 3].any():
            m.L[1, y, x] = rng.choice(floes)


def rime_silk(m, spots):
    for x, y in spots:
        if m.inb(x, y) and m.inb(x, y + 1) and m.L[2, y, x] == 0:
            st = STAMPS['pf_p_strand_w']['layers']
            for dy in range(2):
                t = st[1][dy][0] or st[2][dy][0]
                if t and m.L[2, y + dy, x] == 0:
                    m.L[2, y + dy, x] = t


def over_tiles(m, name, x, y, z=2):
    L = np.array(STAMPS[name]['layers'])
    for dy in range(L.shape[1]):
        for dx in range(L.shape[2]):
            t = int(L[:, dy, dx].max())
            if t and m.inb(x + dx, y + dy) and m.L[z, y + dy, x + dx] == 0:
                m.L[z, y + dy, x + dx] = t


def doorstep(m, door, depth=6):
    x, y = door
    for k in range(1, depth + 1):
        yy = y + k
        if not m.inb(x, yy) or m.cls[yy, x] in 'dep' or m.taken[yy, x]:
            break
        if m.cls[yy, x] in '.tT':
            for xx in ((x - 1, x, x + 1) if k == 1 else (x, x + (1 if (x + y) % 2 else -1))):
                if m.inb(xx, yy) and m.cls[yy, xx] in '.tT' and not m.taken[yy, xx]:
                    m.cls[yy, xx] = 'e' if k == 1 else 'd'


def bridges_snow(m, rows, cls='p'):
    T = lambda k, x: STAMPS['fw_bridge_%s%d' % (k, x % 2)]['layers'][1][0][0]
    for y0, y1 in rows:
        for y in range(y0, y1 + 1):
            for x in range(m.W):
                if m.cls[y, x] == cls:
                    m.L[1, y, x] = T('n' if y == y0 else 's' if y == y1 else 'm', x)


# Ice-sliding puzzle solver (100% matching Essentials terrain tag 12 rules)
DIRS4 = ((1, 0), (-1, 0), (0, 1), (0, -1))


def slide_solve(ice_cells, land_cells, start, goal):
    def slide(p, d):
        x, y = p
        while True:
            n = (x + d[0], y + d[1])
            if n in ice_cells:
                x, y = n
                continue
            if n in land_cells:
                return n
            return (x, y) if (x, y) != p else None

    best = {}
    q = deque()
    for st in start:
        best[st] = (0, None)
        q.append(st)
    while q:
        p = q.popleft()
        k = best[p][0]
        for d in DIRS4:
            n = (p[0] + d[0], p[1] + d[1])
            if p in land_cells and n not in ice_cells:
                continue
            res = slide(p, d)
            if res is None or res in best:
                continue
            if res in land_cells and res not in goal and res not in start:
                continue
            best[res] = (k + 1, p)
            q.append(res)
    g = [best[c][0] for c in goal if c in best]
    return (min(g) if g else None), best


def slide_puzzle(m, cells, islet, item_at, n_rocks=(6, 9), tries=4000, seed=7):
    rng = random.Random(seed)
    cells = set(cells)
    isl = set(islet) - {item_at}
    land_out = set()
    for (x, y) in cells:
        for d in DIRS4:
            n = (x + d[0], y + d[1])
            if n not in cells and n not in islet and m.inb(*n) and m.cls[n[1], n[0]] in '.dt' and not m.taken[n[1], n[0]] and not m.cliff[n[1], n[0]]:
                land_out.add(n)
    inner = [c for c in cells if all((c[0] + dx, c[1] + dy) in cells for dx in (-1, 0, 1) for dy in (-1, 0, 1))]
    ring = [c for c in cells if c not in islet and min(abs(c[0] - a) + abs(c[1] - b) for a, b in islet) <= 2]
    best = None
    for _ in range(tries):
        rocks = set(rng.sample(ring, min(len(ring), rng.randint(3, 6)))) | set(rng.sample(inner, min(len(inner), rng.randint(*n_rocks))))
        ice_c = cells - rocks - set(islet)
        k, _ = slide_solve(ice_c, land_out | isl, land_out, isl)
        if k is None or k < 4:
            continue
        back, _ = slide_solve(ice_c, land_out | isl, isl, land_out)
        if back is None:
            continue
        score = k * 10 - len(rocks)
        if best is None or score > best[0]:
            best = (score, rocks, k)
        if k >= 6:
            break
    if best is None:
        isl_xs = {x for x, y in isl}
        isl_ys = {y for x, y in isl}
        rays = [c for c in cells if c not in islet and (c[0] in isl_xs or c[1] in isl_ys)]
        for _ in range(tries):
            rocks = (set(rng.sample(ring, min(len(ring), rng.randint(3, 5)))) |
                     set(rng.sample(rays, min(len(rays), rng.randint(3, 6)))) |
                     set(rng.sample(inner, min(len(inner), rng.randint(5, 10)))))
            ice_c = cells - rocks - set(islet)
            k, _ = slide_solve(ice_c, land_out | isl, land_out, isl)
            if k is None or k < 4:
                continue
            back, _ = slide_solve(ice_c, land_out | isl, isl, land_out)
            if back is None:
                continue
            score = k * 10 - len(rocks)
            if best is None or score > best[0]:
                best = (score, rocks, k)
            if k >= 6 and len(rocks) <= 18:
                break
    if best is None:
        raise SystemExit('slide_puzzle: no solvable layout')
    print('  pond puzzle: %d stoppers, islet in %d slides (shore cells %d)' % (len(best[1]), best[2], len(land_out)))
    return best[1]


# =============================================================================
# 4. MAP 524 — GOSSAMER WOOD (90x110, ts 53, :SILKWOOD)
# =============================================================================
def build_524():
    W, H = 90, 110
    hs = head_spec(524)
    events = hs['events']

    r = Route(524, W, H, 'forest', base='T')
    m = r.m
    rng = random.Random(52411)

    # 1. Sculpted Northern Upper-Wood Terrace (ht=1)
    lipy = colmap(r, lambda x: 26 + 2.5 * (vnoise(x, 0, 5241, 10.0) - 0.5) * 2 + bump(x, 80, 8, 3))
    fall_y = int(lipy[64])
    for x in range(61, 68):
        lipy[x] = fall_y
    for x in range(W):
        m.ht[:lipy[x] + 1, x] = 1
    CK.smooth_ht(m, 1, 2)
    # Re-lock flat waterfall shelf across x=62..66 so waterfall drops crisply off a straight cliff!
    m.ht[:fall_y + 1, 62:67] = 1
    m.ht[fall_y + 1:fall_y + 5, 62:67] = 0

    # 2. Organic Winding Silkwood River + 4 Scenic Lotus Dew-Coves (perpendicular channels at both bridges!)
    stream_pts = [(68, 0), (66, 12), (64, fall_y - 2), (64, fall_y + 4), (60, 36),
                  (58, 42), (58, 46), (58, 50),
                  (54, 58), (48, 70), (45, 78), (42, 80), (39, 80), (36, 80),
                  (31, 85), (26, 92), (16, 102), (8, 109)]
    CK.stream(r, stream_pts, w=3.2, c='w', only='T.t')
    # Organic river widenings & secluded mossy dew ponds (carefully off all events!)
    CK.pond(r, 64.0, fall_y + 6.0, 3.6, 2.4, c='w', rough=0.45, seed=11)   # waterfall plunge cove
    CK.pond(r, 53.5, 57.5, 4.0, 3.0, c='w', rough=0.50, seed=12)   # lotus cove south of Weft Bridge
    CK.pond(r, 15.0, 36.5, 3.2, 2.3, c='w', rough=0.48, seed=13)   # enchanted west mossy dew pond
    CK.pond(r, 32.0, 87.5, 3.0, 2.2, c='w', rough=0.45, seed=14)   # mossy bend south of fallen giant
    smooth_cls(m, 'w', into='T', passes=1)
    # Lock clean straight vertical N-S water channel under Weft Bridge (x=57..59, y=43..49)
    for y in range(43, 50):
        for x in range(55, 62):
            m.cls[y, x] = 'w' if 57 <= x <= 59 else '.'
    # Lock clean straight horizontal E-W water channel under Fallen Giant log bridge (x=36..43, y=79..82)
    for y in range(77, 85):
        for x in range(36, 44):
            m.cls[y, x] = 'w' if 79 <= y <= 82 else '.'
    # Prepare crisp 3-wide waterfall throat: upper water at fall_y-1, dry cliff face at fall_y..fall_y+2, plunge water at fall_y+3!
    m.cls[fall_y - 2:fall_y, 63:66] = 'w'
    m.cls[fall_y:fall_y + 3, 63:66] = '.'
    m.cls[fall_y + 3:fall_y + 5, 63:66] = 'w'

    # 3. Winding Dappled Woodland Trails (demolishing straight bowling alleys!)
    main = [(0, 51.5), (12, 51), (22, 48), (28, 40), (31, lipy[31] + 4)]
    r.road(main, w=3.0, open_=(2, 4))
    CK.stair(r, 30, lipy[31], w=3, h=1)
    r.road([(31, lipy[31] - 2), (34, 20), (40, 13), (45, 6), (45, 0)], w=3.0, open_=(2, 4))
    r.exit('W', 50, 4)
    m.cls[0:3, 44:47] = 'd'

    # Upper fork round the great mossy oak
    r.lane([(31, 20), (26, 15), (30, 9), (40, 13)], w=2.2, open_=(1, 2))
    # East trail: over the Weft Bridge -> Woodward's clearing -> Cut tree & Glasswood Veil
    r.lane([(28, 40), (40, 44), (52, 46), (55, 46)], w=2.6, open_=(1, 3))
    r.lane([(61, 46), (72, 47), (84, 48), (89, 48)], w=2.4, open_=(1, 3))
    r.clearing(70, 52, 8.5, 6.5)

    # South trail over Fallen Giant -> gently S-curving lane to Accord Cordon (40..42, 104) -> Windfall Row
    r.lane([(22, 48), (22, 60), (30, 72), (39, 77)], w=2.6, open_=(1, 3))
    r.lane([(39, 84), (43, 90), (38.5, 96), (41, 101), (41, 109)], w=2.5, open_=(1, 2))
    # Strictly seal flanks of Accord Cordon (y=103..105) so players cannot bypass x=40..42!
    for y in range(103, 106):
        for x in range(36, 47):
            if x not in (40, 41, 42):
                m.cls[y, x] = 'T'
        for x in (40, 41, 42):
            m.cls[y, x] = 'd'
    # Keep Cordon notice (43, 103) reachable from north/west!
    m.cls[102, 43] = '.'; m.cls[103, 43] = '.'

    # SW Cocoon Harvest Grove & twist loop
    r.lane([(22, 60), (12, 68), (10, 80), (16, 88), (26, 84)], w=2.1, open_=(1, 3))
    r.clearing(12, 80, 7.0, 5.5)

    # NW Sacred Mushroom Ring & Monkey Shrine Sanctuary + NE Giga Drain Blossom Grove
    r.lane([(34, 20), (20, 16), (13, 10)], w=2.1, open_=(1, 3))
    r.clearing(15, 10, 6.8, 4.5)
    r.lane([(45, 8), (56, 9), (70, 12), (76, 14)], w=2.0, open_=(1, 2))
    r.clearing(77, 14, 6.5, 4.5)

    # SE Unpicked Seam: S-curving shaded secret path (DEMOLISHING the 24-tile straight vertical alley!)
    r.lane([(73, 56), (76.5, 62), (71.5, 68), (76.0, 74), (74, 79)], w=2.0, open_=(1, 2))
    r.clearing(74, 68, 3.2, 2.5)
    r.pocket(78, 85.5, 6.8, 5.5, gate=None)
    # Seal Silk seam choke strictly at (74, 80)
    for dx in (-2, -1, 1, 2):
        m.cls[80, 74 + dx] = 'T'
        m.cls[79, 74 + dx] = 'T'
    m.cls[79, 74] = 'd'; m.cls[80, 74] = 'd'; m.cls[81, 74] = 'd'
    # Small sacred dew-pool inside SE Sap Tree sanctuary (off events (78,86), (80,85))
    CK.pond(r, 83.2, 82.0, 2.0, 1.5, c='w', rough=0.4, seed=19)

    # Organic dappled tall-grass encounter pockets (multi-lobed, ZERO boxy rectangles!)
    CK.grass_fields(r, [
        (14, 48, 3.0), (24, 66, 3.0), (36, 42, 3.0), (70, 58, 2.8),
        (16, 76, 2.6), (37, 92, 2.6), (14, 13, 2.4), (38, 20, 2.5),
        (78, 16, 2.5), (73, 68, 2.2),
    ])

    # Reserve exact event cells BEFORE finish_plan so none fall on water/trees
    for e in events:
        ex, ey = e['at']
        if m.cls[ey, ex] in 'Tw':
            m.cls[ey, ex] = '.'
        for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
            xx, yy = ex + dx, ey + dy
            if m.inb(xx, yy) and m.cls[yy, xx] == 'T' and e.get('name') not in ('Silk seam', 'Silk wall', 'Fallen log', 'Accord cordon 1', 'Accord cordon 2', 'Accord cordon 3'):
                if abs(dx) + abs(dy) <= 1 and e['type'] in ('npc', 'trainer', 'item', 'door'):
                    m.cls[yy, xx] = '.'

    # Ensure Horn-and-Pincer shortcut choke cells stay clean 1-tile chokes
    for (px, py) in ((31, 25), (20, 87)):
        m.cls[py, px] = 'd'
    # Ensure exact warps & border exits stay clean
    m.cls[106:110, 40:43] = 'd'
    m.cls[0:3, 44:47] = 'd'
    m.cls[47:50, 79:89] = 'd'
    m.cls[48, 89] = 'd'
    for y in (47, 49):
        m.cls[y, 82] = 'T'   # CutTree [82, 48] cleanly gates east Deepwood lane!
        m.cls[y, 89] = 'T'
    for y in range(44, 52):
        if y != 48:
            m.cls[y, 89] = 'T'

    CK.thin_bands(r, passes=2)
    # Re-lock waterfall throat strictly before finish_plan so thin_bands never alters it
    m.cls[fall_y - 2:fall_y, 63:66] = 'w'
    m.cls[fall_y:fall_y + 3, 63:66] = '.'
    m.cls[fall_y + 3:fall_y + 5, 63:66] = 'w'
    r.finish_plan(border=0)

    # Re-assert waterfall, Weft Bridge, Fallen Giant log bridge & stepping stones
    sx = 63
    CK.waterfall(r, sx, sx + 2, fall_y)

    # Straight perpendicular Weft Bridge (timber planks with rails!) spanning x=56..60, y=45..47
    weft_y = 46
    wx0, wx1 = 56, 60
    weft = []
    for y in range(43, 50):
        for x in range(55, 62):
            m.cls[y, x] = 'w' if 57 <= x <= 59 else '.'
    for x in range(wx0, wx1 + 1):
        for k, y in enumerate((weft_y - 1, weft_y, weft_y + 1)):
            weft.append((x, y, 'nms'[k]))
            if 57 <= x <= 59:
                m.cls[y, x] = 'w'
    # Clean open bridgehead aprons (ZERO clipped cypresses at 55..56, 44 or 55, 48!)
    for x in (54, 55, 56, 60, 61):
        for y in (44, 45, 46, 47, 48):
            if m.cls[y, x] == 'T':
                m.cls[y, x] = '.'
    r.lane([(50, 46), (55, weft_y)], w=2.6, open_=(1, 2))
    r.lane([(61, weft_y), (65, 46)], w=2.6, open_=(1, 2))
    # Keep The Weft Bridge sign (54, 47) on clear ground west of bridge
    m.cls[47, 54] = '.'; m.cls[46, 54] = 'd'; m.cls[45, 55] = 'd'; m.cls[46, 55] = 'd'; m.cls[47, 55] = '.'
    m.cls[46, 61] = 'd'

    # Straight perpendicular Fallen Giant log bridge (x=39..40, y=78..83) across horizontal E-W river (y=79..82)
    for y in range(77, 85):
        for x in range(36, 44):
            m.cls[y, x] = 'w' if 79 <= y <= 82 else '.'
    ly0, ly1 = 78, 83
    giant_log = [(x, y) for y in range(ly0, ly1 + 1) for x in (39, 40)]
    # Clear grassy north & south bank landings so Fallen giant sign (41, 76) & south exit (39..40, 84) have ZERO tree collisions!
    for y in (75, 76, 77, 78, 83, 84, 85):
        for x in range(38, 43):
            if m.cls[y, x] == 'T':
                m.cls[y, x] = '.'
    m.cls[76, 39] = 'd'; m.cls[77, 39] = 'd'; m.cls[77, 40] = 'd'
    m.cls[84, 39] = 'd'; m.cls[84, 40] = 'd'

    st = [(x, 11) for x in range(56, 78) if m.cls[11, x] == 'w']
    CK.stones(r, st)

    # Cohesive emerald/teal woodland groves (NO loud alternating purple/blue checkerboard spam!)
    GOSSAMER_WOODS_524 = [
        {'sh1': 5, 'teal2': 3, 'silk1': 2},
        {'sh0': 4, 'teal': 3, 'silk0': 2, 'olive': 2},
        {'teal': 4, 'teal2': 3, 'sh1': 3},
        {'silk0': 3, 'silk1': 3, 'sh1': 3, 'olive': 2},
        {'olive': 3, 'sh1': 4, 'teal2': 2, 'sh0': 2},
    ]
    VEIL_EDGE_524 = {'teal2': 5, 'sh1': 4, 'teal': 3, 'silk1': 2}

    def glass_pick(x, y):
        if x >= 79 and 38 <= y <= 58:
            return VEIL_EDGE_524
        return None

    CK.woods(r, GOSSAMER_WOODS_524, scale=13.0, accents=None, pick=glass_pick)

    # Register immutable HEAD events (zero coordinate drift!)
    r.events = events
    bridge_pad = ([(x, y) for x in range(54, 62) for y in range(44, 49)] +
                  [(x, y) for x in range(38, 43) for y in range(76, 85)])
    ev_mask = reserve_events(m, events, r.road_mask, radius=1,
                             extra=[(45, 1), (44, 1), (40, 108), (41, 108), (42, 108), (88, 48), (1, 51), (1, 52), (70, 52)] + bridge_pad)
    # Signpost graphic for Cordon notice (43, 103)
    m.tile(4847, 43, 103, 1)

    # Stamp Woodward's Hut cleanly onto door [70, 51] (without duplicating door event)
    m.front('gl_shed', 70, 51, None, None)
    m.events = []

    # ---- Monumental Wild Giant Trees (nudged (20,28) west off central cliff stair!)
    for n, x, y in (
        ('pf_g_tree4p', 58, 50), ('pf_g_tree2', 79, 52), ('pf_g_tree4p', 20, 28), ('pf_g_tree2', 46, 22),
        ('pf_g_tree4p', 4, 58), ('pf_g_tree4p', 50, 86), ('pf_g_tree2', 6, 30), ('pf_g_tree4p', 72, 26),
        ('pf_g_tree2', 30, 98), ('pf_g_tree4p', 78, 92), ('pf_g_tree2', 7, 4), ('pf_g_tree2', 82, 8),
    ):
        s = STAMPS[n]
        if m.free(x, y, s['w'], s['h'], on='.tT') and not ev_mask[y:y + s['h'], x:x + s['w']].any():
            m.stamp(n, x, y, mark='B', blend=True)

    # ---- Iconic Story Landmarks & Clustered Vignettes ----
    # 1. NW Sacred Mushroom Ring & Monkey Shrine Sanctuary (dedicated blossom accent glade)
    for n, x, y in (
        ('pf_shrine', 19, 6), ('nr_col', 11, 7), ('nr_col', 17, 7), ('nt_blossom', 21, 6),
        ('pf_lantern', 13, 9), ('pf_lantern', 21, 10), ('nt_azalea2', 10, 11), ('nt_azalea0', 17, 13),
        ('nt_boulder', 12, 12), ('nt_rocks_s1', 18, 12), ('nt_birch_h', 15, 6),
    ):
        s = STAMPS[n]
        if m.free(x, y, s['w'], s['h'], on='.tT') and not ev_mask[y:y + s['h'], x:x + s['w']].any():
            m.stamp(n, x, y, mark='B')

    # 2. Woodward's Clearing (weavers' hub: looms, racks, spools, campfire, lanterns, benches — NO wireframe pf_p_net!)
    for n, x, y in (
        ('pf_p_loom', 66, 53), ('gw_spool', 75, 53), ('gw_rack', 63, 56), ('pf_logbench', 68, 57),
        ('pf_lantern', 67, 51), ('pf_lantern', 73, 51), ('gw_rack', 75, 56), ('sh_campfire', 70, 58),
        ('pf_p_lantern', 64, 49), ('nt_azalea1', 64, 53), ('nt_azalea0', 76, 51), ('nt_boulder', 64, 59),
    ):
        s = STAMPS[n]
        if m.free(x, y, s['w'], s['h'], on='.dt') and not ev_mask[y:y + s['h'], x:x + s['w']].any():
            m.stamp(n, x, y, mark='B')

    # 3. SW Cocoon Harvest Grove (warm weaver lanterns, racks, spools, mossy boulders)
    for n, x, y in (
        ('gw_rack', 6, 76), ('gw_rack', 15, 74), ('gw_spool', 17, 83), ('pf_p_lantern', 11, 79),
        ('pf_lantern', 7, 80), ('pf_lantern', 17, 79), ('pf_logbench', 10, 84), ('nt_boulder', 6, 84),
        ('nt_azalea0', 14, 85), ('nt_birch_h', 12, 74), ('nt_rock_big', 7, 82),
    ):
        s = STAMPS[n]
        if m.free(x, y, s['w'], s['h'], on='.dtT') and not ev_mask[y:y + s['h'], x:x + s['w']].any():
            m.stamp(n, x, y, mark='B')

    # 4. Weft Bridge Grand Stanchions & Lanterns + Fallen Giant Framing + NE Blossom Grove + SE Sap Sanctuary
    for n, x, y in (
        ('nr_col', wx0 - 1, weft_y - 2), ('nr_col', wx1 + 1, weft_y - 2),
        ('pf_lantern', wx0 - 2, weft_y - 1), ('pf_lantern', wx1 + 2, weft_y - 1),
        ('pf_lantern', 38, ly0 - 2), ('pf_lantern', 42, ly1 + 1),
        ('nt_blossom', 79, 10), ('nt_blossom', 73, 10), ('nt_azalea2', 74, 15), ('pf_lantern', 74, 12),   # NE Giga Drain grove
        ('pf_g_tree2', 80, 80), ('nt_azalea1', 75, 87), ('pf_lantern', 75, 83), ('pf_lantern', 81, 87),  # SE Sap Tree
        ('pf_lantern', 29, lipy[31] + 2), ('pf_lantern', 33, lipy[31] + 2),       # Upper wood stairs
        ('pf_lantern', 43, 4), ('pf_lantern', 47, 4),                             # Briarwick north gate
        ('pf_lantern', 6, 49), ('pf_lantern', 6, 53),                             # Thistledown west entry
        ('pf_lantern', 39, 102), ('pf_lantern', 43, 106),                         # Accord cordon road
    ):
        s = STAMPS[n]
        if m.inb(x, y) and m.free(x, y, s['w'], s['h'], on='.dtT') and not ev_mask[y:y + s['h'], x:x + s['w']].any():
            m.stamp(n, x, y, mark='B')

    # 5. Subtle Glasswood Crystal Accents along the East Veil (teal/blue harmony, zero neon checkerboard!)
    for n, x, y in (
        ('cr_teal_t', 80, 45), ('cr_blue_c', 85, 45), ('cr_teal_c', 85, 50),
        ('gd_shard0', 83, 49), ('gd_shard1', 87, 49), ('nt_boulder', 81, 50),
    ):
        s = STAMPS[n]
        if m.inb(x, y) and m.free(x, y, s['w'], s['h'], on='.dtT') and not ev_mask[y:y + s['h'], x:x + s['w']].any():
            m.stamp(n, x, y, mark='B')

    # 6. Clustered Moss-Stone Outcrops & Fallen Logs framing clearings, river bends & coves
    # (ZERO blank white pf_p_web / gw_drape0 / gw_drape1 rectangles!)
    for n, x, y in (
        ('nt_rock_big', 13, 33), ('nt_boulder', 18, 35), ('nt_rocks_s0', 17, 38),       # West mossy dew pond
        ('nt_boulder', 49, 55), ('nt_rocks_s1', 50, 58), ('nt_birch_h', 56, 61),        # Lotus cove south of Weft Bridge
        ('nt_boulder', 60, 31), ('nt_rocks_s2', 66, 33), ('nt_birch_h2', 60, 22),       # Waterfall plunge cove
        ('nt_boulder', 31, 84), ('nt_rocks_s0', 37, 88), ('nt_log', 32, 88),            # South mossy river bend
        ('nt_stump_big', 25, 44), ('nt_birch_h', 33, 37), ('nt_boulder', 36, 40),       # Mid-wood trail clearings
        ('nt_boulder', 48, 8), ('nt_rocks_s1', 51, 9), ('nt_birch_h', 58, 12),          # Upper wood north lane
        ('nt_stump', 72, 65), ('nt_boulder', 76, 70), ('nt_rocks_s2', 75, 86),          # SE Unpicked Seam glades
    ):
        s = STAMPS[n]
        if m.inb(x, y) and m.free(x, y, s['w'], s['h'], on='.t') and not ev_mask[y:y + s['h'], x:x + s['w']].any():
            m.stamp(n, x, y, mark='B')

    CK.props(r, ['nt_log', 'nt_stump', 'nt_birch_h', 'nt_boulder', 'nt_rocks_s0', 'nt_rocks_s1', 'nt_stump_big'], 44, box=(0, 0, W, H), clump=3, seed=7)
    # Cohesive Emerald/Teal Forest Fringe (tight near_forest=2, ZERO random pink blossom polka dots!)
    CK.fringe(r, ['nt_dark_sh', 'nt_dpine_sh', 'nt_teal_a', 'nt_teal_b', 'nt_olive', 'tr_oak2', 'nt_pine_b'], 115, seed=1, near_forest=2)
    CK.undergrowth(r, 290, kinds=('nt_fern0', 'nt_fern1', 'nt_shrub0', 'nt_shrub1', 'ak_fern', 'nt_azalea0', 'nt_azalea1'), seed=3)

    # Reeds around ALL river bends & mossy dew coves
    for rx, ry in ((44, 50), (36, 56), (51, 56), (56, 59), (30, 80), (50, 74), (62, 24), (65, 31),
                   (13, 36), (17, 37), (33, 86), (37, 85), (82, 82)):
        r.near(rng.choice(['nt_reed1', 'nt_reed0']), rx, ry, on='.w', r=2)

    r.dress(trees=('tr_oak',), n_trees=0, copses=0, scatter=0)
    r.paint(glint=0.0)
    infill_forest(r, GOSSAMER_WOODS_524, pick=glass_pick, scale=13.0, seed=524)
    CK.paint_extras(r)

    # Crisp cliff end-caps flanking the 524 waterfall (x=62 east-end of west cliff, x=66 west-end of east cliff)
    sh_rows = K.KITS['sh']['rows']
    for k_row in range(len(sh_rows)):
        wy = fall_y + k_row
        if m.inb(62, wy) and m.L[1, wy, 62] == sh_rows[k_row][1]:
            m.L[1, wy, 62] = sh_rows[k_row][2]
            m.L[0, wy, 62] = K.SH_GRASS[wy % 2][62 % 2]
        if m.inb(66, wy) and m.L[1, wy, 66] == sh_rows[k_row][1]:
            m.L[1, wy, 66] = sh_rows[k_row][0]
            m.L[0, wy, 66] = K.SH_GRASS[wy % 2][66 % 2]

    # Paint Weft Bridge with warm non-snow weathered timber planks (`ak` 1516..1534) + stone/iron rails on y=44/48!
    ak_rows = {
        'n': [C('ak', 1516), C('ak', 1517), C('ak', 1518)],
        'm': [C('ak', 1524), C('ak', 1525), C('ak', 1526)],
        's': [C('ak', 1532), C('ak', 1533), C('ak', 1534)],
    }
    for x, y, k in weft:
        col = 0 if x == wx0 else 2 if x == wx1 else 1
        m.L[1, y, x] = ak_rows[k][col]
        m.L[2, y, x] = 0
    for ry in (weft_y - 2, weft_y + 2):
        for x in range(wx0, wx1 + 1):
            rk = 'w' if x == wx0 else 'e' if x == wx1 else 'm'
            rt = P1('rw_rail_' + rk)
            if 57 <= x <= 59:
                m.L[1, ry, x] = rt
                m.L[2, ry, x] = 0
            elif m.L[1, ry, x] == 0 and not ev_mask[ry, x]:
                m.L[1, ry, x] = rt
                m.L[2, ry, x] = 0
    # Paint perpendicular Fallen Giant log bridge cleanly over straight E-W river channel (y=78..83)
    for x, y in giant_log:
        k = 'n' if y == ly0 else 's' if y == ly1 else 'm'
        L_ = STAMPS['fw_log_' + k]['layers']
        m.L[1, y, x] = int(L_[1][0][x - 39]) or int(L_[2][0][x - 39]) or int(L_[0][0][x - 39])
        m.L[2, y, x] = 0

    # Overhead canopy rope walkways across Woodward's clearing
    for x in range(62, 79):
        if m.L[2, 49, x] == 0:
            m.L[2, 49, x] = P1('fw_walk_h')

    # Rich layered forest moss/earth depth + wildflowers + petals + glowing mushrooms + lotus water lilies!
    paint_forest_ground_depth(m, seed=524, clearings=[
        (15, 10, 6.5, 4.2, 'ring'),   # NW Mushroom Ring & Monkey Shrine
        (70, 53, 7.5, 5.5, 'worn'),   # Woodward's worn-earth clearing
        (12, 80, 6.5, 5.0, 'dark'),   # SW Cocoon Harvest shaded grove
        (77, 14, 5.5, 3.8, 'ring'),   # NE Blossom grove
        (78, 85, 5.5, 4.5, 'ring'),   # SE Sap Tree sanctuary
        (31, 32, 5.0, 4.0, 'dark'),   # Mid-wood trail hollow
        (45, 7, 4.5, 3.5, 'worn'),    # Briarwick north gate
        (24, 52, 5.0, 3.8, 'dark'),   # West trail hollow
    ])
    dress_water_lotus(m, prob=0.14, seed=524)

    FL = K.DECOR_SH['flowers']
    for i, (cx_, cy_, rx, ry) in enumerate(((70, 59, 4.5, 2.5), (15, 11, 4.5, 2.8), (78, 15, 4.5, 2.8),
                                            (26, 70, 3.8, 2.4), (35, 43, 3.8, 2.2), (78, 85, 4.2, 2.6),
                                            (14, 79, 4.2, 2.6), (44, 7, 3.8, 2.2), (16, 48, 3.5, 2.2),
                                            (31, 18, 3.8, 2.4), (56, 10, 3.5, 2.2), (74, 68, 3.2, 2.2))):
        CK.meadow(r, cx_, cy_, rx, ry, tiles=[FL[k] for k in (2, 4, 6)], p=0.64, seed=i)

    scatter_petals_and_mushrooms(
        m,
        spots_petals=[(15, 10, 5.0, 3.2, 0.36), (78, 14, 4.8, 3.2, 0.38), (70, 54, 5.5, 3.5, 0.24),
                      (78, 85, 4.5, 3.2, 0.34), (12, 80, 4.5, 3.0, 0.24), (45, 7, 4.0, 2.5, 0.28),
                      (31, 34, 4.0, 2.8, 0.22), (24, 50, 4.0, 2.8, 0.20)],
        spots_mush=[(14, 11, 2.2, 10), (19, 9, 2.0, 8), (12, 77, 2.0, 8), (74, 68, 1.8, 7),
                    (78, 85, 2.6, 10), (28, 36, 1.8, 7), (15, 38, 1.8, 6), (52, 56, 2.0, 6)],
        seed=524,
    )

    # Warm glow halos ONLY directly centered on real lamps & Woodward's campfire (ZERO cv_shaft smears & ZERO floating bridge glows!)
    for gx_, gy_ in ((13, 9), (69, 57), (11, 79), (75, 83), (74, 12), (43, 4), (47, 4), (67, 51), (73, 51)):
        put_overlay_stamp(m, 'pf_glow', gx_, gy_, z=2)

    CK.scatter_quiet(r, 16, seed=524)

    # Seal West border strictly to [50..53] (matching 540!) and keep N/S/E warps & arrival paths clean!
    r.exits = [('W', 50, 4)]
    r._keep = [tuple(e['at']) for e in events if e.get('type') == 'warp']
    seal_unconnected_edges(
        m,
        open_cells=[(0, y) for y in range(50, 54)] + r._keep,
        filler=P1('nt_bush0'),
    )
    # Consolidate RJ DirtDark onto L0 ONLY & recompute exact NB2AUTO (0 mismatches!)
    fix_vauto_l0(m.L, 'rejuvenation', 'DirtDark')
    h = {k: v for k, v in hs.items() if k != 'events'}
    h['walk_from'] = [[78, 86]]
    r.write(h, '524_gossamer_wood.yaml', '# Gossamer Wood (524). WRITTEN BY layouts/wave11_wilds_craft.py (Wave 11 Rejuv V14 Craft).\n')
    print('  built 524 Gossamer Wood (%dx%d, %d events)' % (W, H, len(events)))


# =============================================================================
# 5. MAP 525 — GOSSAMER DEEPWOOD / SACRED BRIDE TREE GLADE (44x40, ts 53)
# =============================================================================
def build_525():
    import puzzles.dungeons as DG
    W, H = 44, 40
    hs = head_spec(525)
    events = hs['events']

    r = Route(525, W, H, 'forest', base='T')
    m = r.m
    rng = random.Random(52511)

    # 1. Northern Upper-Wood Terrace (ht=1)
    def lip(x):
        if x <= 21:
            return 11 + (1 if 9 <= x <= 12 else 0)
        if x <= 36:
            return 13
        if x <= 40:
            return 10
        return -1

    for x in range(W):
        if lip(x) >= 0:
            m.ht[:lip(x) + 1, x] = 1

    # 2. D2 Lantern Hollow (100% FIXED geometry for silk_model proof!)
    THICKET = [(x, y) for x in range(30, 37) for y in range(7, 10)]
    ISLAND = [(x, y) for x in range(31, 40) for y in range(1, 6)]
    WALLS = set(DG.D2_WALLS) | {c for c, _ in DG.D2_CURTAINS.values()} | {DG.D2_EXIT[0]} | set(DG.D2_COCOONS.values())
    POSTS = [p for p, _ in DG.D2_POSTS.values()]
    MUST_SOLID = ([(30, 1), (30, 2), (30, 3)] + [(x, 0) for x in range(29, 42)] +
                  [(x, 10) for x in range(33, 37)] + [(x, y) for x in range(38, 41) for y in range(7, 10)])
    for x, y in THICKET + ISLAND:
        m.cls[y, x] = '.'
    POOL = [(x, y) for x in range(37, 40) for y in range(1, 4)]
    for x, y in POOL:
        m.cls[y, x] = 'w'
    for x, y in WALLS | set(MUST_SOLID):
        m.cls[y, x] = 'T'

    # 3. Main Woodland Trail + Curved Weft Brook & Organic Shelly's Dew Pond (ZERO boxy corners!)
    r.road([(0, 18), (5, 18), (11, 18.5), (17, 19), (24, 19.5), (31, 20), (38, 20), (41, 20)], w=3.0, open_=(1, 2))
    r.exit('W', 17, 3)

    BROOK_TOP = [(6, 0), (5.5, 4), (6.5, 7), (7, 9.5)]
    BROOK = [(7, 14), (8.2, 16.5), (9.0, 18.5), (9.5, 22.5), (11.0, 26.5), (11.5, 30.0)]
    CK.stream(r, BROOK_TOP, w=2.5, only='T.t')
    CK.stream(r, BROOK, w=2.6, only='T.td')
    # Organic curved multi-lobe Dew Pond (replaces blocky staircase rectangle!)
    CK.pond(r, 11.2, 32.5, 4.8, 3.0, c='w', rough=0.45, seed=21)
    CK.pond(r, 8.2, 33.8, 2.8, 2.2, c='w', rough=0.40, seed=22)
    CK.pond(r, 14.2, 33.2, 2.4, 2.0, c='w', rough=0.40, seed=23)
    smooth_cls(m, 'w', into='.', passes=1, only='.')

    # 4. SACRED CENTRAL BRIDE / MOTH TREE GLADE (Circular mossy sanctuary + generous cutscene staging room!)
    # Wide open circular clearing spanning x=16..34, y=16..28 framed by ancient Bride Tree (pf_g_tree4p at (24,22))
    r.clearing(25.5, 22.0, 9.2, 5.6)
    # Curved mossy sanctuary path around the ancient Bride Tree to Ferris (26,20), Moth Tree (31,24), Shelly (15,26), Rangers
    r.lane([(17, 20), (16.5, 24), (15.5, 27)], w=2.2, open_=(1, 1))
    r.clearing(15.5, 27.0, 3.8, 2.5)
    # Organic shimmering crystal-mist cove for Glassed Masquerain (23, 34) (NO flat square gravel box!)
    r.lane([(16.5, 27.5), (17.5, 31.0), (19.5, 33.0), (21.5, 34.0)], w=2.6, open_=None)
    r.clearing(23.0, 34.2, 3.5, 2.5)
    for y in range(31, 38):
        for x in range(19, 28):
            q = ((x - 23.0) / 3.4) ** 2 + ((y - 34.2) / 2.4) ** 2 + 0.25 * (vnoise(x, y, 5259, 2.6) - 0.5)
            if m.cls[y, x] == '.' and q <= 1.0:
                m.cls[y, x] = 'g'
    # SE Rangers' Camp clearing
    r.lane([(31, 21), (32.5, 25), (34.5, 28.5), (36.5, 31.5)], w=2.0, open_=(0, 1))
    r.clearing(36.5, 32.5, 5.5, 3.4)
    # West fern bank along dew brook
    r.lane([(5, 19), (4.2, 24), (5.0, 28)], w=1.7, c='.', open_=(0, 1))
    r.clearing(4.5, 29.0, 2.6, 2.0)

    # 5. Upper Wood (ht=1): Weavers' Camp, Ring of Caps & D2 Outer Glade
    r.lane([(15, 9.5), (12, 8), (9, 6)], w=2.1, c='.', open_=(0, 1), only='T.t')
    r.lane([(15, 14), (15, 18)], w=3.0, c='d', open_=None, only='T.t')
    r.clearing(13.0, 6.2, 4.2, 2.5)
    for x in range(2, 5):
        for y in range(3, 9):
            if ((x - 3) / 1.8) ** 2 + ((y - 5.5) / 3.0) ** 2 <= 1.0:
                m.cls[y, x] = '.'
    OUT = ({(x, y) for x in range(22, 29) for y in range(6, 11)} |
           {(x, y) for x in range(23, 26) for y in range(10, 13)} |
           {(x, y) for x in range(24, 33) for y in (11, 12)} |
           {(x, y) for x in range(27, 30) for y in range(3, 7)}) - {(22, 6), (22, 10), (28, 10)}
    for x, y in OUT:
        if (x, y) not in WALLS and (x, y) not in MUST_SOLID:
            m.cls[y, x] = '.'
    for x, y in WALLS | set(MUST_SOLID):
        m.cls[y, x] = 'T'

    # East Crystal-Silk Mouth (strictly 1-tile choke at (41, 20) -> (43, 20)!)
    for x in range(40, 44):
        for y in range(16, 25):
            if y != 20 and x >= 41:
                m.cls[y, x] = 'T'
        m.cls[20, x] = 'd'

    # Organic encounter tall-grass pockets (tucked cleanly off the central Bride Grove staging plaza!)
    CK.grass_fields(r, [(12, 23, 2.0), (20, 28, 1.9), (30, 30, 1.8), (36, 24, 1.8), (14, 5, 1.4)])

    # Ensure ALL 24 events sit on walkable ground (never water/forest)
    for e in events:
        ex, ey = e['at']
        if m.cls[ey, ex] in 'Tw':
            m.cls[ey, ex] = '.'

    # Clean thin 1-cell T bands outside D2 so we NEVER get polka-dot bush rows!
    d2_protect = set(WALLS) | set(MUST_SOLID) | {(x, y) for x in range(41, 44) for y in range(16, 25)}
    T_mask = (m.cls == 'T')
    padT = np.pad(T_mask, 1, constant_values=True)
    thin = T_mask & ((~padT[:-2, 1:-1] & ~padT[2:, 1:-1]) | (~padT[1:-1, :-2] & ~padT[1:-1, 2:]))
    for y, x in np.argwhere(thin):
        if (x, y) not in d2_protect and m.ht[y, x] == 0:
            m.cls[y, x] = '.'

    r.finish_plan(border=0)
    r.flatten(6, 8, 11, 1)
    for x in range(6, 9):
        for y in range(11, 14):
            m.cls[y, x] = '.'
    CK.waterfall(r, 6, 8, 11)
    CK.stair(r, 14, 11, w=3, h=1)
    CK.stair(r, 23, 13, w=3, h=1)
    for x in range(14, 17):
        m.cls[9:11, x] = '.'
    for x in range(23, 26):
        m.cls[11:13, x] = '.'

    # Plank bridge across Weft Brook + stepping stones to Great Ball
    BRIDGE = [(x, y) for y in range(17, 21) for x in range(6, 13) if m.cls[y, x] in 'wW']
    for x, y in BRIDGE:
        r.plank_bridge(x, y, x, y)
    CK.stones(r, [(x, 6) for x in range(4, 9) if m.cls[6, x] == 'w'])

    # Lock D2 cells & reserve all 24 HEAD events
    for x, y in THICKET + ISLAND + list(OUT) + POSTS + list(WALLS):
        m.taken[y, x] = True
    for x, y in POOL:
        m.taken[y, x] = False

    def zone(x, y):
        edge = 33.5 + 2.8 * math.sin(y / 4.5) + 3.5 * (vnoise(x, y, 5253, 5.0) - 0.5)
        return GLASSWOOD_PAL if x > edge else None

    CK.woods(r, DEEP_WOODS, scale=8.0, pick=zone, accents={'blossom': 0.015})

    r.events = events
    masq_path = [(x, y) for x in range(16, 21) for y in range(28, 34)]
    ev_mask = reserve_events(m, events, r.road_mask, radius=1, extra=POSTS + [DG.D2_START, DG.D2_GOAL, (1, 18), (42, 20)] + masq_path)
    for mx, my in masq_path:
        if m.inb(mx, my) and m.cls[my, mx] == 'T':
            m.cls[my, mx] = '.'
    # Signpost at Deepwood marker [2, 16]
    m.tile(4847, 2, 16, 1)

    # ---- SACRED BRIDE / MOTH TREE SANCTUARY HERO SETPIECES ----
    # Centerpiece: towering wild ancient tree (pf_g_tree4p, 6x7, ZERO door!) at (24, 22) right beside The Moth Tree [31, 24]!
    # Leaves wide sunlit mossy staging plaza across (16..34, 17..21) and (30..33, 22..26)!
    m.stamp('pf_g_tree4p', 24, 22, mark='B', blend=True)
    # Framing ancient giant trees on NW weavers' ridge & SW deepwood corner
    for nm, x, y in (('pf_g_tree2', 11, 0), ('pf_g_tree2', 0, 33)):
        s = STAMPS[nm]
        if m.free(x, y, s['w'], s['h'], on='.tT') and not ev_mask[y:y + s['h'], x:x + s['w']].any():
            m.stamp(nm, x, y, mark='B', blend=True)

    # Sacred Bride Grove framing props: blossom canopy sentinels, mossy ruin columns, lanterns, shrine, benches!
    for n, x, y in (
        ('nt_blossom', 19, 14), ('nt_blossom', 29, 14),            # twin pink blossom crowns framing the upper sanctuary
        ('nr_col', 21, 17), ('nr_col', 30, 17),                    # weathered mossy sanctuary pillars
        ('pf_lantern', 18, 17), ('pf_lantern', 32, 18),            # warm sanctuary lanterns
        ('pf_lantern', 12, 17), ('pf_lantern', 12, 20),            # Weft Brook bridgehead lanterns
        ('pf_lantern', 17, 26), ('pf_lantern', 29, 27),            # lower sanctuary & pond lanterns
        ('pf_shrine', 20, 23),                                     # small ancient mossy forest shrine beside Bride Tree!
        ('nt_azalea2', 22, 27), ('nt_azalea0', 30, 26),            # blooming sanctuary shrubs
        ('nt_boulder', 19, 25), ('nt_boulder', 31, 22),            # mossy sanctuary boulders
        # NW Weavers' camp
        ('gw_rack', 17, 7), ('gw_spool', 9, 4), ('gw_spool', 17, 5), ('nt_log', 9, 9), ('pf_lantern', 12, 7),
        # SE Rangers' camp
        ('nt_stump_big', 39, 27), ('sh_campfire', 34, 31), ('pf_logbench', 35, 34),
        ('pf_lantern', 41, 33), ('gw_rack', 37, 35), ('nt_stump', 32, 30), ('nt_boulder', 38, 36),
        # West fern bank & pond overlook
        ('nt_boulder', 2, 25), ('pf_p_lantern', 22, 8),
    ):
        s = STAMPS[n]
        if m.inb(x, y) and m.free(x, y, s['w'], s['h'], on='.dtT') and not ev_mask[y:y + s['h'], x:x + s['w']].any():
            m.stamp(n, x, y, mark='B')

    # Reeds around Dew Pond & D2 glowing island pool
    for n, x, y in (('nt_reed0', 6, 30), ('nt_reed1', 7, 34), ('nt_reed0', 15, 30), ('nt_reed1', 16, 33),
                    ('nt_reed0', 9, 35), ('nt_reed1', 12, 35), ('nt_reed0', 38, 3), ('nt_reed1', 37, 1)):
        r.near(n, x, y, on='w', r=2)

    # Creeping Glasswood crystal spires east of x=33 & around Masquerain's crystal-mist cove
    CRY = ['cr_teal_t', 'cr_blue_e', 'cr_clear_t', 'cr_purple_t', 'cr_clear_e', 'cr_teal_c', 'cr_blue_c', 'gd_shard0', 'gd_shard1', 'gd_shard2']
    for n, x, y in (('cr_teal_t', 35, 17), ('cr_clear_e', 37, 17), ('cr_blue_e', 40, 18), ('cr_purple_t', 39, 22),
                    ('cr_teal_c', 36, 22), ('cr_clear_t', 41, 22), ('gd_shard1', 34, 22), ('cr_blue_c', 38, 17),
                    ('gd_spire', 41, 15), ('cr_teal_t', 33, 23),
                    ('cr_teal_t', 21, 31), ('cr_purple_t', 25, 31), ('cr_blue_c', 26, 35), ('cr_teal_c', 20, 36)):
        s = STAMPS[n]
        if m.inb(x, y) and m.free(x, y, s['w'], s['h'], on='.gtT') and not ev_mask[y:y + s['h'], x:x + s['w']].any():
            m.stamp(n, x, y, mark='B')
    for _ in range(70):
        x, y = rng.randrange(31, W), rng.randrange(13, H)
        if zone(x, y) is None:
            continue
        n = rng.choice(CRY)
        s = STAMPS[n]
        if m.free(x, y, s['w'], s['h'], on='.g') and not ev_mask[y:y + s['h'], x:x + s['w']].any():
            if not r.road_mask[max(0, y - 1):y + s['h'] + 1, max(0, x - 1):x + s['w'] + 1].any():
                m.stamp(n, x, y, mark='B')

    # Silk drapes, layered canopy fringe (ZERO broken nt_conifer!), blooming undergrowth
    CK.drapes_along(r, every=3, seed=2)
    for _ in range(W * H // 24):
        nm = rng.choice(['pf_p_web', 'pf_p_web1', 'gw_cocoons', 'gw_cocoons', 'pf_p_strand_w', 'pf_p_strand_p', 'gw_drape0', 'gw_drape1'])
        x, y = rng.randrange(W), rng.randrange(H)
        st_ = STAMPS[nm]
        if nm.startswith('gw_drape') or nm == 'gw_cocoons':
            if y + st_['h'] < H and (m.cls[y, x:x + st_['w']] == 'T').all() and m.free(x, y + 1, st_['w'], st_['h'] - 1, on='.dt'):
                m.stamp(nm, x, y, mark=None)
        elif m.free(x, y, st_['w'], st_['h'], on='.'):
            m.stamp(nm, x, y, mark=None)

    CK.fringe(r, ['nt_dark_sh', 'nt_teal_b', 'nt_dpine_sh', 'nt_olive', 'nt_blossom'], 48, box=(0, 0, 31, H), seed=1, near_forest=3)
    CK.fringe(r, ['nt_tree_blue', 'nt_pine_blue', 'nt_tree_purp', 'nt_pine_purp'], 16, box=(31, 13, W, H), seed=2, near_forest=3)
    CK.undergrowth(r, 85, kinds=('nt_fern0', 'nt_fern1', 'nt_shrub0', 'nt_shrub1', 'ak_fern', 'nt_azalea0', 'nt_azalea2'), seed=3)
    CK.props(r, ['nt_log', 'nt_stump', 'nt_rocks_s0', 'nt_boulder', 'nt_birch_h'], 14, box=(0, 12, 31, H), clump=3, seed=7)
    CK.earth(r, [(38.5, 21, 3.0, 2.0), (36, 24, 1.8, 1.4)], c='g', on='.t')

    r.dress(trees=('tr_oak',), n_trees=0, copses=0, scatter=0)
    r.paint(glint=0.0)
    infill_forest(r, DEEP_WOODS, pick=zone, scale=8.0, seed=525)
    CK.paint_extras(r)

    # Rich layered mossy forest ground depth + Bride Grove circular sanctuary ring!
    paint_forest_ground_depth(m, seed=525, clearings=[
        (26.0, 22.0, 8.8, 5.5, 'ring'),   # Sacred circular Bride/Moth Tree glade!
        (15.5, 27.0, 4.0, 2.8, 'dark'),   # Shelly's dew pond bank
        (36.5, 32.5, 5.2, 3.2, 'worn'),   # Rangers' camp clearing
        (13.0, 6.2, 4.2, 2.5, 'ring'),    # Upper Weavers' camp
    ])
    dress_water_lotus(m, prob=0.26, seed=525)

    # Lush wildflower drifts, Bride Grove pink blossom petals (5723) & glowing mushroom fairy rings!
    FL = K.DECOR_SH['flowers']
    for i, (cx_, cy_, rx, ry, ks) in enumerate((
        (25, 20, 6.0, 3.0, (2, 4, 6)), (33, 3, 3, 1.6, (2, 6)), (13, 5, 2.8, 1.6, (4, 6)),
        (16, 27, 3.2, 1.8, (2, 4)), (26, 9, 2.2, 1.3, (6,)), (4, 29, 2.2, 1.6, (2,)), (33, 8, 2.5, 1.2, (4,)),
    )):
        CK.meadow(r, cx_, cy_, rx, ry, tiles=[FL[k] for k in ks], p=0.58, seed=i)

    scatter_petals_and_mushrooms(
        m,
        spots_petals=[
            (25.5, 21.0, 7.5, 4.5, 0.42),  # Sacred Bride Grove pink blossom petal carpet!
            (15.5, 26.5, 3.2, 2.2, 0.28),  # Shelly's dew pond bank
            (13.5, 6.0, 3.0, 2.0, 0.25),   # Upper Weavers' camp
        ],
        spots_mush=[
            (15, 5, 2.1, 10),   # Ring of caps [15, 5]
            (26, 22, 4.6, 12),  # Sacred mushroom ring circling the Bride Tree!
            (6, 29, 1.6, 7),
            (27, 5, 1.5, 6),
        ],
        seed=525,
    )

    # Shimmering Veil curtain around Masquerain's crystal-mist pocket
    VEIL = [int(np.array(STAMPS['bl_veil%d' % i]['layers']).max()) for i in (0, 1)]
    for y in range(31, 38):
        for x in range(18, 22):
            if m.cls[y, x] in '.gd' and m.L[2, y, x] == 0 and (x == 19 or (x == 20 and y % 2) or (x in (18, 21) and (x + y) % 3 == 0)):
                m.L[2, y, x] = VEIL[(x + y) % 2]

    # Dramatic volumetric sunbeam shafts & glowing sacred sanctuary halos!
    for sx_, sy_ in ((23, 17), (28, 17), (25, 21), (14, 25), (35, 30), (13, 4), (33, 2), (7, 13)):
        put_overlay_stamp(m, 'cv_shaft', sx_, sy_, z=2)
    for gx_, gy_ in ((25, 19), (29, 23), (22, 33), (14, 26), (34, 31), (14, 4)):
        put_overlay_stamp(m, 'pf_glow', gx_, gy_, z=2)

    # Guarantee D2 MUST_SOLID walls are 100% solid (critical for silk_model proof!)
    solid_at(m, MUST_SOLID)

    # Dress D2 Lantern Hollow floors (walkable tufts, clover, glowing caps, overhead webs)
    evc = {tuple(e['at']) for e in events} | set(POSTS) | set(WALLS) | {DG.D2_GOAL}
    for x, y in THICKET + ISLAND + sorted(OUT):
        if (x, y) in evc or m.cls[y, x] not in '.t' or m.L[1, y, x] or m.L[2, y, x]:
            continue
        k = rng.random()
        if k < 0.22:
            m.L[1, y, x] = rng.choice(K.TUFTS + K.CLOVER)
        elif k < 0.34:
            m.L[1, y, x] = rng.choice([FL[2], FL[6], FL[4], PETAL_TILE])
        elif k < 0.40:
            m.L[1, y, x] = rng.choice(GLOW_MUSH)
    for wx, wy in ((31, 1), (36, 4), (32, 7), (22, 6), (26, 3)):
        put_overlay_stamp(m, 'pf_p_web', wx, wy, z=2)

    CK.scatter_quiet(r, 14, seed=525)

    r.exits = [('W', 17, 3)]
    r._keep = [tuple(e['at']) for e in events if e.get('type') == 'warp']
    seal_unconnected_edges(
        m,
        open_cells=[(0, y) for y in range(17, 20)] + r._keep,
        filler=P1('nt_bush0'),
    )
    h = {k: v for k, v in hs.items() if k != 'events'}
    h['walk_from'] = [[1, 18], [33, 8], [34, 4], [42, 20]]
    r.write(h, '525_gossamer_deepwood.yaml',
            '# Gossamer Deepwood (525). WRITTEN BY layouts/wave11_wilds_craft.py (Wave 11 Rejuv V14 Craft).\n'
            '# The D2 lantern hollow events are laid over it by puzzles/dungeons.py (EVENTS[525]).\n')
    print('  built 525 Gossamer Deepwood (%dx%d, %d events)' % (W, H, len(events)))


# =============================================================================
# 6. MAP 562 — THE RIMEWOOD (48x56, ts 52, primeval snow pine woodland)
# =============================================================================
def build_562():
    import puzzles.dungeons as DG
    W, H = 48, 56
    hs = head_spec(562)
    events = hs['events']

    m = snowmap(W, H, 562, kit='shs3')
    rng = random.Random(56211)
    m.cls[:, :] = 'T'

    # 1. Flat Primeval Snow-Forest Floor (ZERO tiny clipped ht=1 cliff-pillar shards or floating icicles!)
    # Dense interlocking alpine spruces in NW/ES/SW naturally frame the forest without orphan cliff stubs.

    # 2. Winding Primeval Forest Trails & Clearings
    path = [(29, 56), (29, 50), (22, 46), (14, 44), (10, 38), (12, 30), (20, 27), (30, 26),
            (38, 22), (30, 22), (25, 20), (24.5, 13), (24, 10), (18, 8), (15, 4), (15, -1)]
    m.lane(path, '.', 4.4, seed=3, only='T', wobble=1.3)
    for cx, cy, rx, ry in ((26, 3.5, 4.5, 2.5), (35, 9.5, 5.0, 3.4), (10, 41, 4.4, 3.5), (40, 44, 4.4, 3.4),
                           (20, 32, 8.2, 4.6), (44, 24, 4.2, 3.2), (35, 36, 4.6, 3.2), (12, 26, 3.6, 2.6), (8, 48, 3.5, 2.6)):
        m.blob(cx, cy, rx, ry, '.', seed=int(cx + cy), only='T', rough=0.55)
    m.lane([(29, 56), (29, 50), (22, 46), (14, 44), (10, 38), (12, 30), (20, 27), (30, 26),
            (38, 22), (30, 22), (25.5, 21), (24.5, 14), (24, 11), (18, 8), (15, 4), (15, -1)],
           'd', 2.5, seed=4, only='.T', wobble=0.45)
    m.lane([(24, 11), (30, 10), (35, 9)], 'd', 2.2, seed=6, only='.T', wobble=0.3)
    m.lane([(33, 36), (37, 40), (40, 43)], '.', 2.2, seed=8, only='T', wobble=0.3)
    m.lane([(38, 22), (44, 24), (47, 24)], 'd', 2.0, seed=5, only='.T')
    # Clean path spur to Wolfsrime warp [47, 26]
    m.lane([(42, 24), (45, 26), (47, 26)], 'd', 1.8, seed=15, only='.T')

    # Keep exact N (12..15) and S (26..29) border connection spans open!
    for x in range(12, 16):
        for y in range(0, 4):
            m.cls[y, x] = 'd' if m.cls[y, x] == 'd' else '.'
    for x in range(26, 30):
        for y in range(52, 56):
            m.cls[y, x] = 'd' if m.cls[y, x] == 'd' else '.'

    # 3. Sculpted Glacial Ravine (frost-rippled water with crisp snowy shorelines!)
    for x in range(1, 47):
        c = 16.5 + 1.7 * math.sin(x / 6.2) + 1.5 * (vnoise(x, 0, 9, 3.0) - 0.5)
        hw = 1.4 + 1.3 * vnoise(x, 0, 10, 4.0) + (0.9 if 20 <= x <= 29 else 0)
        for y in range(int(c - hw), int(round(c + hw)) + 1):
            if 0 <= y < m.H and m.cls[y, x] in '.dT':
                m.cls[y, x] = 'W'
    smooth_cls(m, 'W', into='T', passes=2)

    # Keep D7 Frost Loom east corridor (x=47, y=14..20), cache pocket (43..47, 11..15), & threads (40..42, 19) 100% intact!
    for y in range(14, 21):
        m.cls[y, 47] = '.'
    for y in range(11, 15):
        for x in range(43, 48):
            if (x, y) != (47, 11) and (x, y) != (47, 12) and (x, y) != (47, 13):
                m.cls[y, x] = '.'
    for y in range(18, 22):
        for x in range(38, 47):
            if m.cls[y, x] not in 'oW':
                m.cls[y, x] = '.'
    # Seal D7 pocket strictly from north/west so player MUST pass through D7_CURTAINS (47, 16..18)!
    for y in range(10, 15):
        m.cls[y, 42] = 'T'
    for x in range(42, 48):
        m.cls[10, x] = 'T'
        m.cls[11, x] = 'T' if x <= 43 else '.'
    for y in range(15, 19):
        m.cls[y, 46] = 'W'
    # Keep cache (44, 12) and approach from (47, 15) -> (47, 14) -> (45..46, 13..14) -> (44, 12) wide open!
    for cx, cy in ((47, 15), (47, 14), (46, 14), (46, 13), (45, 13), (45, 12), (44, 12), (44, 13), (47, 19), (47, 20), (46, 20), (45, 20)):
        m.cls[cy, cx] = '.'

    # Open ragged snowy bank along ravine so evergreens don't butt awkwardly into water edges
    bank = np.zeros((H, W), bool)
    for y, x in np.argwhere(np.isin(m.cls, ['o', 'W'])):
        bank[max(0, y - 2):y + 3, max(0, x - 1):x + 2] = True
    for y, x in np.argwhere(bank & (m.cls == 'T')):
        if x < 41 and vnoise(x, y, 12, 2.5) > 0.45:
            m.cls[y, x] = '.'

    # 4. Sculpted Organic Hoar Pond Slide Puzzle (kidney lobes + rounded organic snow islet for ICESTONE [26, 33])
    for cx, cy, rx, ry, sd in ((22.5, 33.4, 6.2, 3.4, 19), (28.8, 34.8, 4.0, 2.6, 21),
                               (17.6, 31.4, 2.8, 2.0, 23), (25.5, 30.7, 3.2, 1.5, 25), (31.5, 32.2, 1.8, 1.4, 27)):
        m.blob(cx, cy, rx, ry, 'p', seed=sd, rough=0.35, only='.dT')
    smooth_cls(m, 'p', into='.', passes=2)
    # Rounded organic snow island keeping ICESTONE [26,33] & solvable >=4-slide puzzle!
    ISLET = [(25, 33), (26, 33), (24, 34), (25, 34), (26, 34), (25, 35)]
    for x, y in ISLET:
        m.cls[y, x] = '.'
        m.taken[y, x] = True
    # Crisp 1-tile open snowy south shore around Hoar Pond (pulls south-rim pines down +1 tile so ZERO sheared canopies!)
    for y in range(32, 41):
        for x in range(14, 34):
            if m.cls[y, x] == 'T' and any(m.inb(x + dx, y - 1) and m.cls[y - 1, x + dx] == 'p' for dx in (-1, 0, 1)):
                m.cls[y, x] = '.'
            if m.cls[y, x] == 'T' and any(m.inb(x + dx, y - 2) and m.cls[y - 2, x + dx] == 'p' for dx in (0,)) and y <= 38:
                m.cls[y, x] = '.'

    # 5. Fallen Giant Ice-Log Bridge spanning the ravine at x=24..25
    oy = [y for y in range(H) if m.cls[y, 24] in 'oW' or m.cls[y, 25] in 'oW']
    LOG = (min(oy) - 1, max(oy) + 1)
    log_water_rows = [y for y in range(LOG[0] + 1, LOG[1]) if (m.cls[y, 23] in 'oW' or m.cls[y, 26] in 'oW')]
    for y in range(LOG[0], LOG[1] + 1):
        m.cls[y, 24] = m.cls[y, 25] = 'D'
    # Clear wide snow landing south of Fallen Giant bridge (x=22..27, y=20..24) so signpost [24,21] has ZERO pine/log collision!
    for y in range(LOG[1] + 1, min(H, LOG[1] + 6)):
        for x in range(22, 28):
            if m.cls[y, x] == 'T':
                m.cls[y, x] = '.'
    m.cls[20, 24] = '.'; m.cls[20, 25] = 'd'; m.cls[20, 26] = 'd'
    m.cls[21, 24] = '.'; m.cls[21, 25] = 'd'; m.cls[21, 26] = 'd'

    # 6. Organic Frosted Fern Encounter Pockets (ZERO square rectangles!)
    for cx, cy, rx, ry, sd in ((12, 48, 3.6, 2.6, 51), (34, 39, 3.8, 2.6, 52), (16, 11, 3.6, 2.2, 53), (38, 46, 3.0, 2.2, 54)):
        m.blob(cx, cy, rx, ry, 't', seed=sd, rough=0.65, only='.')

    # Clear Trapper's Chalet yard (1..9, 32..42)
    for yy in range(32, 42):
        for xx in range(0, 10):
            if m.cls[yy, xx] == 'T':
                m.cls[yy, xx] = '.'

    # Ensure ALL 18 HEAD events + D7 threads/cache/trapper sit on clean ground!
    d7_pts = list(DG.D7_CURTAINS) + [p for p, _ in DG.D7_THREADS.values()] + [DG.D7_CACHE, DG.D7_START, (39, 21)]
    for e in events:
        ex, ey = e['at']
        if m.cls[ey, ex] in 'ToW':
            m.cls[ey, ex] = '.'
    for ex, ey in d7_pts:
        if m.cls[ey, ex] in 'ToW':
            m.cls[ey, ex] = '.'

    # Keep [46, 24] & [47, 24] & [47, 26] open on packed snow
    for ex, ey in ((45, 24), (46, 24), (47, 24), (45, 26), (46, 26), (47, 26)):
        m.cls[ey, ex] = 'd'
    m.cls[25, 46] = 'T'; m.cls[25, 47] = 'T'   # Clean evergreen divider between Glade cut-tree & Wolfsrime lane!
    m.cls[23, 46] = 'T'; m.cls[23, 47] = 'T'

    m.plan_cliffs(rows=3)

    # Clean thin 1-cell T bands (protecting D7 walls!)
    R_ = types.SimpleNamespace(m=m, seed=562, road_mask=np.isin(m.cls, ['d']), events=events, rng=rng)
    d7_wall_cells = ((42, 10), (42, 11), (42, 12), (42, 13), (42, 14), (43, 10), (44, 10), (45, 10), (46, 10), (47, 10), (46, 23), (47, 23), (46, 25), (47, 25))
    d7_wall_set = set(d7_wall_cells)
    bridge_clear = [(x, y) for x in range(23, 27) for y in range(LOG[0], LOG[1] + 4)]
    se_lane_clear = [(x, y) for x in range(34, 42) for y in range(37, 45) if abs((x - 34) - (y - 37)) <= 2]
    ev_mask = reserve_events(m, events, R_.road_mask, radius=1, extra=d7_pts + [(45, 24), (46, 26)] + bridge_clear + se_lane_clear)
    for x, y in d7_wall_cells:
        m.taken[y, x] = True
    CK.thin_bands(R_, passes=2)
    for x, y in d7_wall_cells:
        m.taken[y, x] = False

    # Signboards for Frost Loom [33, 10] & Fallen giant [24, 21] (cleanly clear of bridge & pines!)
    m.tile(4847, 33, 10, 1)
    m.tile(4847, 24, 21, 1)

    # 7. Landmarks & Warm Lantern Trail Markers (ZERO floating wood signposts, ZERO treehouse windows in the wild!)
    # Trapper's Cozy Chalet (door at (4, 40) matching Lodge door sign [4, 40]!)
    m.stamp('ch_chalet_b', 1, 34, None, None)
    doorstep(m, (4, 40))
    m.cls[40, 4] = 'B'

    # Pre-paint hero kf_tree reservation (clears full 4x6 box + 2-row south canopy buffer from 'T' so CK.woods/infill NEVER shoot L2 up into kf_tree!)
    hero_kf_trees = []
    kf_reserved = np.zeros((H, W), dtype=bool)
    for x, y in (
        (31, 3), (3, 2), (1, 19), (1, 26),
        (41, 30), (18, 49), (41, 47),
        (41, 21), (28, 19), (36, 31),
    ):
        w, h = STAMPS['kf_tree']['w'], STAMPS['kf_tree']['h']
        if x < 1 or y < 1 or x + w >= W - 1 or y + h >= H - 1:
            continue
        if not m.free(x, y, w, h, on='.T'):
            continue
        if m.cliff[y:y + h, x:x + w].any() or ev_mask[y:y + h, x:x + w].any():
            continue
        # Require 1-tile crown buffer & 2-row south clearance from other hero trees/walls/chalet
        bx0, bx1 = max(0, x - 1), min(W, x + w + 1)
        by0, by1 = max(0, y - 1), min(H, y + h + 2)
        if kf_reserved[by0:by1, bx0:bx1].any():
            continue
        if any((xx, yy) in d7_wall_set for yy in range(by0, by1) for xx in range(bx0, bx1)):
            continue
        # Clear 'T' in full box + 2 rows south & 1 col E/W so CK.woods/infill stay strictly outside crown buffer!
        for yy in range(by0, by1):
            for xx in range(bx0, bx1):
                if m.cls[yy, xx] == 'T':
                    m.cls[yy, xx] = '.'
        m.taken[y:y + h, x:x + w] = True
        m.overm[y:y + h, x:x + w] = True
        m.bodym[y:y + h, x:x + w] = True
        kf_reserved[y:y + h, x:x + w] = True
        hero_kf_trees.append((x, y))

    # Frost Loom frozen loom prop
    if m.free(34, 11, STAMPS['pf_p_loom']['w'], STAMPS['pf_p_loom']['h'], on='.dtT') and not ev_mask[11:13, 34:36].any():
        m.stamp('pf_p_loom', 34, 11, mark='B')

    # Trapper's warm yard, Aurora Clearing, Child's big tree, Fallen Birch Logs & Warm Lantern Trail Markers
    # Track ONLY actually placed braziers/lanterns so pf_glow NEVER lands on bare snow!
    placed_lights_562 = []
    for n, x, y in (
        # Trapper's yard
        ('fw_wood', 4, 43), ('fw_wood', 6, 44), ('pf_sledge', 9, 44), ('fw_rack', 1, 43),
        ('fw_brazier', 10, 40), ('pf_lantern', 7, 39), ('nt_birch_h', 12, 37), ('nt_stump', 15, 41),
        # Aurora Clearing (sacred frost monoliths + warm braziers)
        ('fw_brazier', 22, 2), ('fw_brazier', 28, 2), ('fw_stone', 20, 4), ('fw_stone', 30, 4),
        # Warm lantern trail markers & Frost Loom / Fallen Giant / Glade framing
        ('pf_lantern', 22, 20), ('pf_lantern', 27, 20), ('pf_lantern', 23, 12), ('pf_lantern', 26, 12),
        ('pf_lantern', 32, 11), ('pf_lantern', 37, 10),
        ('pf_lantern', 12, 2), ('pf_lantern', 16, 2),
        ('pf_lantern', 26, 52), ('pf_lantern', 30, 52),
        ('pf_lantern', 44, 22), ('pf_lantern', 44, 27),
        ('fw_brazier', 35, 22), ('fw_brazier', 15, 28),
        # Trail survey pegs
        ('fw_peg', 26, 27), ('fw_peg', 29, 25), ('fw_peg', 32, 24), ('fw_peg', 35, 23),
        # Child's big tree camp (SE) & natural fallen birch logs + alpine rock outcrops (NO pale-pink fw_skull!)
        ('fw_wood', 38, 42), ('fw_wood', 42, 46), ('nt_stump_big', 43, 40), ('fw_peg', 36, 45),
        ('pf_lantern', 39, 43),
        ('nt_birch_h', 16, 22), ('nt_birch_h2', 29, 28), ('nt_birch_h', 22, 44), ('nt_birch_h2', 32, 46),
        ('nt_birch_v', 13, 30), ('nt_birch_h', 18, 9), ('fw_stone', 17, 23), ('fw_stone', 33, 35),
        ('nt_rocks_s0', 21, 11), ('nt_rocks_s1', 28, 11), ('nt_rocks_s2', 14, 26), ('nt_rocks_s0', 36, 37),
        ('nt_rocks_s1', 23, 47), ('nt_rocks_s2', 31, 48), ('nt_stump', 27, 48), ('nt_stump', 37, 26),
    ):
        s = STAMPS[n]
        sw, sh = s['w'], s['h']
        if (m.inb(x, y) and m.free(x, y, sw, sh, on='.d')
                and not ev_mask[y:y + sh, x:x + sw].any()
                and not m.overm[y:y + sh, x:x + sw].any()
                and not kf_reserved[y:y + sh, x:x + sw].any()):
            m.stamp(n, x, y, mark='B')
            if n in ('fw_brazier', 'pf_lantern'):
                placed_lights_562.append((n, x, y))

    # 8. Interlocking Alpine Spruce Forest (CK.woods + safe_canopy infill_winter -> ZERO L2-on-L2 overlaps!)
    CK.woods(R_, ALPINE_WOODS, scale=8.5, accents={'snowblue': 0.08})

    m.events = events
    m.paint()
    infill_winter(R_, ALPINE_WOODS, scale=8.5, seed=562, safe_canopy=True)

    # P0 #1 FIX: Guarantee EVERY frosted_oak (snow0, L2=18388) has L2=18380 directly above it (0 missing crowns!)
    for y_o, x_o in np.argwhere(m.L[2] == 18388):
        if y_o > 0 and m.L[2, y_o - 1, x_o] == 0:
            m.L[2, y_o - 1, x_o] = 18380

    # Strict post-paint stamp & sprite placers for 562:
    # Require FULL bounding box L1==0 & L2==0 PLUS 1-tile L2==0 crown buffer so ZERO tree/boulder ever clips another crown!
    def stamp_post_562(nm, x, y, on='.T', crown_pad=1, check_taken=True):
        s = STAMPS[nm]
        w, h = s['w'], s['h']
        if x < 1 or y < 1 or x + w >= W - 1 or y + h >= H - 1:
            return False
        if m.cliff[y:y + h, x:x + w].any() or ev_mask[y:y + h, x:x + w].any():
            return False
        if check_taken and m.taken[y:y + h, x:x + w].any():
            return False
        if any((xx, yy) in d7_wall_set for yy in range(y, y + h) for xx in range(x, x + w)):
            return False
        if (m.L[1, y:y + h, x:x + w] != 0).any() or (m.L[2, y:y + h, x:x + w] != 0).any():
            return False
        if crown_pad > 0:
            px0, px1 = max(0, x - crown_pad), min(W, x + w + crown_pad)
            py0, py1 = max(0, y - crown_pad), min(H, y + h + crown_pad)
            if (m.L[2, py0:py1, px0:px1] != 0).any():
                return False
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                if m.cls[yy, xx] not in on:
                    return False
        for z_ in (1, 2):
            grid = s['layers'][z_]
            for dy in range(h):
                for dx in range(w):
                    t = grid[dy][dx]
                    if t:
                        m.L[z_, y + dy, x + dx] = t
        m.taken[y:y + h, x:x + w] = True
        m.overm[y:y + h, x:x + w] = True
        m.bodym[y:y + h, x:x + w] = True
        return True

    def put_sprite_562(tx, ty, top_r, bot_r, on='.T', post_paint=True, crown_pad=1):
        ht_, hb_ = len(top_r), len(bot_r)
        w_ = len(bot_r[0]) if hb_ else len(top_r[0])
        h_ = ht_ + hb_
        if tx < 1 or ty < 1 or tx + w_ >= W - 1 or ty + h_ >= H - 1:
            return False
        if m.cliff[ty:ty + h_, tx:tx + w_].any() or ev_mask[ty:ty + h_, tx:tx + w_].any() or m.taken[ty:ty + h_, tx:tx + w_].any():
            return False
        if any((xx, yy) in d7_wall_set for yy in range(ty, ty + h_) for xx in range(tx, tx + w_)):
            return False
        if (m.L[1, ty:ty + h_, tx:tx + w_] != 0).any() or (m.L[2, ty:ty + h_, tx:tx + w_] != 0).any():
            return False
        if crown_pad > 0 and ht_ > 0:
            px0, px1 = max(0, tx - crown_pad), min(W, tx + w_ + crown_pad)
            py0, py1 = max(0, ty - crown_pad), min(H, ty + h_ + crown_pad)
            if (m.L[2, py0:py1, px0:px1] != 0).any():
                return False
        for yy in range(ty, ty + h_):
            for xx in range(tx, tx + w_):
                if m.cls[yy, xx] not in on:
                    return False
        if put_sprite(m, tx, ty, top_r, bot_r, on=on, avoid_mask=ev_mask, force=True, post_paint=True):
            m.overm[ty:ty + h_, tx:tx + w_] = True
            m.bodym[ty:ty + h_, tx:tx + w_] = True
            m.taken[ty:ty + h_, tx:tx + w_] = True
            return True
        return False

    # Stamp reserved hero kf_tree ancient frosted oaks cleanly into their pre-cleared pockets (ZERO overlap!)
    for hx, hy in hero_kf_trees:
        stamp_post_562('kf_tree', hx, hy, on='.T', crown_pad=1, check_taken=False)

    # Post-paint focal nt_pine_blue conifers (strict L1==0 & L2==0 + 1-tile crown buffer, gentle r<=2 nudge if needed!)
    for bx, by in (
        (36, 3), (28, 4), (8, 2), (1, 6), (6, 20), (45, 30), (40, 36),
        (23, 50), (15, 51), (45, 48), (42, 52), (15, 24), (33, 27),
        (12, 34), (34, 43), (20, 41), (7, 46),
    ):
        placed_bp = False
        for rad in range(0, 3):
            for dy in range(-rad, rad + 1):
                for dx in range(-rad, rad + 1):
                    if abs(dx) != rad and abs(dy) != rad:
                        continue
                    if stamp_post_562('nt_pine_blue', bx + dx, by + dy, on='.', crown_pad=1):
                        placed_bp = True
                        break
                if placed_bp:
                    break
            if placed_bp:
                break

    # Post-paint Aurora Clearing frost monoliths + Ravine sentinel teal pines + alpine boulders & frosted shrubs
    # (ALL gated by full-box L1==0 & L2==0 + 1-tile L2 crown buffer -> ZERO sheared canopies or boulder-in-crown bites!)
    for tx, ty, sp in (
        (24, 1, KF_CRYS_MONO), (26, 1, KF_CRYS_STAR), (29, 1, KF_CRYS_BLADES),
        (19, 12, KF_TEAL_PINE_A), (28, 12, KF_TEAL_PINE_B), (39, 12, KF_TEAL_PINE_A),
        (7, 21, KF_TEAL_PINE_B), (35, 28, KF_TEAL_PINE_B),
        (17, 39, KF_TEAL_PINE_A), (30, 44, KF_TEAL_PINE_B), (21, 50, KF_TEAL_PINE_A),
        (11, 6, KF_TEAL_PINE_B), (32, 3, KF_TEAL_PINE_A),
        # Clustered alpine boulder outcrops & frosted evergreen shrubs
        (21, 3, KF_BOULDER), (29, 5, KF_BOULDER), (16, 24, KF_BOULDER), (34, 33, KF_BOULDER),
        (37, 24, KF_BOULDER), (15, 45, KF_BOULDER), (31, 41, KF_BOULDER),
        (19, 25, KF_SHRUB_A), (29, 23, KF_SHRUB_B), (13, 35, KF_SHRUB_A), (34, 37, KF_SHRUB_B),
        (18, 43, KF_SHRUB_A), (27, 45, KF_SHRUB_B), (20, 7, KF_SHRUB_A), (30, 8, KF_SHRUB_B),
    ):
        put_sprite_562(tx, ty, sp[0], sp[1], on='.', post_paint=True, crown_pad=1)

    # Post-paint pine2 fringe near woods (replaces pre-paint CK.fringe so 10610/10611 NEVER overwrites any crown below!)
    fr_rng = random.Random(56291)
    t_mask = (m.cls == 'T')
    cand_fr = []
    for fy in range(2, H - 4):
        for fx in range(2, W - 3):
            if m.cls[fy + 2, fx] == '.' and not m.taken[fy:fy + 3, fx:fx + 2].any():
                if t_mask[max(0, fy - 2):min(H, fy + 5), max(0, fx - 2):min(W, fx + 4)].any():
                    cand_fr.append((fx, fy))
    fr_rng.shuffle(cand_fr)
    fr_placed = 0
    for fx, fy in cand_fr:
        if fr_placed >= 26:
            break
        if stamp_post_562('pine2', fx, fy, on='.', crown_pad=1):
            fr_placed += 1

    # Post-paint small ground props (logs, stumps, stones) strictly on clear snow (ZERO crown overlaps!)
    pr_rng = random.Random(5627)
    pr_cands = [(x, y) for y in range(2, H - 3) for x in range(2, W - 3) if m.cls[y, x] == '.' and not m.taken[y, x]]
    pr_rng.shuffle(pr_cands)
    pr_placed = 0
    for px, py in pr_cands:
        if pr_placed >= 18:
            break
        pnm = pr_rng.choice(('fw_wood', 'nt_birch_h', 'nt_stump', 'fw_stone', 'nt_rocks_s0'))
        if stamp_post_562(pnm, px, py, on='.', crown_pad=1):
            pr_placed += 1

    # Fallen Giant Ice-Glazed Log Bridge across Ravine — paint blue Still water snow on L0 underneath water rows!
    w_vauto = RC.vauto('reborn', 'Still water snow', 0)
    for y in log_water_rows:
        m.L[0, y, 24] = w_vauto
        m.L[0, y, 25] = w_vauto
    fix_vauto_l0(m.L, 'reborn', 'Still water snow')
    for y in range(LOG[0], LOG[1] + 1):
        nm = 'fw_log_n' if y == LOG[0] else 'fw_log_s' if y == LOG[1] else 'fw_log_m'
        L_ = STAMPS[nm]['layers'][1][0]
        m.L[1, y, 24], m.L[1, y, 25] = L_[0], L_[1]
        m.L[2, y, 24] = m.L[2, y, 25] = 0
    # Guarantee Fallen giant signpost [24, 21] has ZERO overhead canopy clipping
    m.L[1, 21, 24] = 4847
    m.L[2, 21, 24] = 0

    # Hoar Pond Slide Puzzle stoppers (mathematically proven >= 4 slides to ICESTONE [26,33] & proven exit,
    # AND every stopper boulder sits strictly >= 1 tile inside the ice — ZERO shore-clipping boulders!)
    pond_cells = set(tuple(c[::-1]) for c in np.argwhere(m.cls == 'p'))
    isl_set = set(ISLET) - {(26, 33)}
    land_out_562 = {
        (x + dx, y + dy)
        for (x, y) in pond_cells for dx, dy in DIRS4
        if (x + dx, y + dy) not in pond_cells and (x + dx, y + dy) not in set(ISLET)
        and m.inb(x + dx, y + dy) and m.cls[y + dy, x + dx] in '.dt'
        and not m.taken[y + dy, x + dx] and not m.cliff[y + dy, x + dx]
    }
    pond_all = pond_cells | set(ISLET)
    interior_ice = [c for c in sorted(pond_cells)
                    if all((c[0] + dx, c[1] + dy) in pond_all for dx in (-1, 0, 1) for dy in (-1, 0, 1))]
    isl_xs, isl_ys = {x for x, _ in isl_set}, {y for _, y in isl_set}
    ray_ice = [c for c in interior_ice if c[0] in isl_xs or c[1] in isl_ys]
    # Identify direct 1-slide lanes from shore to islet:
    # - If a lane has interior_ice cells, sample an interior stopper along it.
    # - If a lane is too short to contain any interior_ice cell (1-tile shore-to-islet gap), place a crisp L1-only snow-rim stone on the shore cell (strictly L1==0 & L2==0!).
    direct_lanes = []
    blocked_shore = set()
    for sx, sy in sorted(land_out_562):
        for dx, dy in DIRS4:
            cx, cy = sx + dx, sy + dy
            lane = []
            while (cx, cy) in pond_cells:
                lane.append((cx, cy))
                cx += dx; cy += dy
            if (cx, cy) in isl_set:
                int_lane = [c for c in lane if c in interior_ice]
                if int_lane:
                    direct_lanes.append(int_lane)
                elif m.cls[sy, sx] == '.' and not ev_mask[sy, sx] and m.L[1, sy, sx] == 0 and m.L[2, sy, sx] == 0:
                    m.L[1, sy, sx] = 10551
                    m.taken[sy, sx] = True
                    blocked_shore.add((sx, sy))
    land_out_562 -= blocked_shore
    sp_rng = random.Random(56211)
    best_sp = None
    for it_ in range(20000):
        rocks = set()
        for ln in direct_lanes:
            if sp_rng.random() < 0.92:
                rocks.add(sp_rng.choice(ln))
        rocks |= set(sp_rng.sample(ray_ice, min(len(ray_ice), sp_rng.randint(2, 7))))
        rocks |= set(sp_rng.sample(interior_ice, min(len(interior_ice), sp_rng.randint(2, 7))))
        ice_c = pond_cells - rocks - set(ISLET)
        k_sl, _ = slide_solve(ice_c, land_out_562 | isl_set, land_out_562, isl_set)
        if k_sl is None or k_sl < 4:
            continue
        back_sl, _ = slide_solve(ice_c, land_out_562 | isl_set, isl_set, land_out_562)
        if back_sl is None:
            continue
        sc = k_sl * 100 - len(rocks)
        if best_sp is None or sc > best_sp[0]:
            best_sp = (sc, rocks, k_sl)
        if k_sl >= 5 and len(rocks) <= 13:
            break
    if best_sp is None:
        raise SystemExit('562 Hoar Pond: no solvable interior layout')
    print('  pond puzzle: %d strictly-interior stoppers, islet in %d slides (shore cells %d)' %
          (len(best_sp[1]), best_sp[2], len(land_out_562)))
    for x, y in sorted(best_sp[1]):
        m.L[1, y, x] = 10371 if (x + y) % 3 else 10551

    # P1 FIX: Warm glow halos ONLY on actually placed braziers/lanterns (ZERO orphaned pf_glow on bare snow!)
    for lnm, lx, ly in placed_lights_562:
        # Center 2x2 pf_glow halo cleanly on verified lamp/brazier tiles (never overwrite tree L2!)
        gy_ = ly if lnm == 'fw_brazier' else ly + 1
        if m.inb(lx, gy_) and m.L[1, gy_ + (1 if lnm == 'fw_brazier' else 0), lx] != 0:
            put_overlay_stamp(m, 'pf_glow', lx, gy_, z=2)

    rime_silk(m, ((33, 6), (36, 8), (22, 4), (27, 4), (35, 30)))
    dress_ice(m, 0.22, seed=562, reeds=False)
    # Frosted boulders & snow-shrubs framing ravine shoreline (strict full-box + 1-tile L2 crown buffer!)
    for tx, ty, sp in (
        (18, 13, KF_SHRUB_A), (29, 13, KF_SHRUB_B), (12, 19, KF_BOULDER),
        (33, 19, KF_SHRUB_A), (36, 13, KF_BOULDER), (39, 34, KF_SHRUB_B), (39, 36, KF_SHRUB_A),
    ):
        put_sprite_562(tx, ty, sp[0], sp[1], on='.', post_paint=True, crown_pad=1)
    # Wind-swept clustered snowdrift bands hugging tree edges & frosted glades
    ds_tiles = [STAMPS['fw_drift%d' % i]['layers'][1][0][0] for i in range(3)]
    open_snow = (m.cls == '.') & ~m.taken & (m.L[1] == 0) & (m.L[2] == 0) & ~m.cliff
    pad_s = np.pad(open_snow, 1, constant_values=True)
    for y, x in np.argwhere(open_snow):
        if ev_mask[y, x]:
            continue
        edge = not pad_s[y:y + 3, x:x + 3].all()
        nz_d = vnoise(x, y, 5629, 4.5)
        if (edge and nz_d > 0.44 and rng.random() < 0.42) or (not edge and nz_d > 0.66 and rng.random() < 0.28):
            m.L[1, y, x] = ds_tiles[int(vnoise(x, y, 5631, 2.5) * 2.999)]
    CK.snow_ground_var(R_, thr=0.34)
    # Purge any stray 10555/10556 grey triangle shard tiles (DECOR_SNOW['green'] in Gen 5 reskin!)
    for z_ in (1, 2):
        shard_m = (m.L[z_] == 10555) | (m.L[z_] == 10556)
        if shard_m.any():
            m.L[z_, shard_m] = 0
    # Consolidate PF Packed Snow onto L0 ONLY & recompute exact NB2AUTO (0 mismatches!), THEN lay tracks on L1!
    fix_vauto_l0(m.L, 'pf', 'Packed Snow')
    tk_tiles = [STAMPS['fw_tracks%d' % i]['layers'][1][0][0] for i in range(2)]
    tr_rng = random.Random(5625)
    for y, x in np.argwhere(m.cls == 'd'):
        if m.L[1, y, x] == 0 and m.L[2, y, x] == 0 and not m.taken[y, x] and not m.cliff[y, x] and tr_rng.random() < 0.11:
            m.L[1, y, x] = tr_rng.choice(tk_tiles)

    # Ensure D7 corridor (47, 14..20), Glade warp (47, 24) & Wolfsrime warp (47, 26) stay 100% passable!
    for ex, ey in ((47, 14), (47, 15), (47, 16), (47, 17), (47, 18), (47, 19), (47, 20), (47, 24), (47, 26)):
        m.L[1, ey, ex] = 0
        m.L[2, ey, ex] = 0

    # Seal N strictly to [12..15] (561) and S strictly to [26..29] (578)!
    m.seal_against(
        [{'dir': 'N', 'offset': 12, 'to': 561, 'to_offset': 10}, {'dir': 'S', 'offset': 26, 'to': 578, 'to_offset': 36}],
        spans=[('N', 12, 4), ('S', 26, 4)],
        keep=[tuple(e['at']) for e in events if e.get('type') == 'warp'],
    )
    seal_unconnected_edges(
        m,
        open_cells=[(x, 0) for x in range(12, 16)] +
                   [(x, H - 1) for x in range(26, 30)] +
                   [(47, y) for y in (14, 15, 16, 17, 18, 19, 20, 24, 26)],
        filler=10371,
    )
    fix_vauto_l0(m.L, 'pf', 'Packed Snow')
    fix_vauto_l0(m.L, 'reborn', 'Still water snow')
    h = {k: v for k, v in hs.items() if k != 'events'}
    h['walk_from'] = [[13, 1]]
    h['_file'] = '562_rimewood.yaml'
    m.write(562, h, '# The Rimewood (562). WRITTEN BY layouts/wave11_wilds_craft.py (Wave 11 Rejuv V14 Craft).\n')
    print('  built 562 The Rimewood (%dx%d, %d events)' % (W, H, len(events)))


# =============================================================================
# 7. MAP 563 — RIMEWOOD GLADE (34x30, ts 52, sacred frozen lakefront & shrine)
# =============================================================================
def build_563():
    W, H = 34, 30
    hs = head_spec(563)
    events = hs['events']

    m = snowmap(W, H, 563, kit='shs3')
    rng = random.Random(56311)
    m.cls[:, :] = 'T'

    # 1. Sculpted Organic Curved North Amphitheater Cliff Ridge (ht=1, shs3 + icicles!)
    for x in range(W):
        if x < 11:
            lip = 5 + (1 if x < 6 else 0)
        elif x <= 22:
            lip = 4
        elif x <= 26:
            lip = 5
        else:
            lip = 4
        m.ht[:lip + 1, x] = 1
    # Ensure Stantler ridge meadow (x=24..32, y=0..4) & stairhead (x=28..30, y=4) stay clean!
    m.ht[0:5, 24:34] = 1

    # 2. Organic Sacred Glade Clearing + Sleeping Stantler Ridge Meadow
    m.blob(16.8, 16.8, 13.4, 9.6, '.', seed=2, only='T', rough=0.72)
    m.blob(28.0, 2.0, 4.8, 2.0, '.', seed=21, only='T', rough=0.35)
    # Extra open sanctuary amphitheater around Snowveil Shrine (25..31, 17..23)
    m.blob(28.0, 20.5, 4.0, 3.2, '.', seed=63, only='T', rough=0.4)

    # Winding snow footpath from West warp [0, 15] -> Ice note [9, 17] -> Sigurd [20, 24] -> Snowveil Shrine [28, 21] -> Stairs [29, 8]
    m.lane([(0, 15), (5, 15.2), (8.5, 19.5), (13.5, 23.0), (20.5, 24.2), (26.5, 22.8), (29.2, 19.5), (29.2, 10.0)],
           'd', 2.0, seed=3, only='.T', wobble=0.35)
    m.rect(0, 14, 3, 3, 'd', only='.T')

    # 3. Sculpted Organic Frozen Silk-Fall Lake ('p' slide puzzle) + Snowy Central Islet (NEVERMELTICE [19, 13])
    for cx, cy, rx, ry, sd in ((18.5, 12.6, 6.6, 3.5, 31), (12.4, 14.4, 3.2, 2.3, 33),
                               (24.2, 14.5, 3.1, 2.1, 35), (18.5, 16.0, 3.6, 1.7, 37)):
        m.blob(cx, cy, rx, ry, 'p', seed=sd, rough=0.35, only='.T')
    smooth_cls(m, 'p', into='.', passes=2)
    for y in range(8, 11):
        for x in range(16, 20):
            m.cls[y, x] = 'p'
    ISLET = [(18, 12), (19, 12), (18, 13), (19, 13), (20, 13), (19, 14)]
    for x, y in ISLET:
        m.cls[y, x] = '.'
        m.taken[y, x] = True

    # 4. Frosted Fern Encounter Hollows (night Emolga!)
    for i, (cx, cy, sz) in enumerate(((6.5, 21.5, 3.0), (26.5, 10.0, 2.3), (7.5, 10.5, 2.4), (12.5, 26.2, 2.1), (26.5, 26.0, 1.8))):
        m.blob(cx, cy, sz, sz * 0.72, 't', seed=50 + i, only='.', rough=0.65)

    # Clear cliff face zone & build snowy timber stairs at (28..30, 4)
    for y in range(H):
        for x in range(W):
            if m.cls[y, x] in '.t' and m.ht[y, x] == 0 and y <= 7:
                m.cls[y, x] = 'T'
    m.stairs(28, 4, w=3, kit_rows=3, c='d')
    m.plan_cliffs(rows=3)
    for x in range(28, 31):
        for y in (2, 3, 7, 8, 9):
            if m.cls[y, x] in 'T.t':
                m.cls[y, x] = '.'

    # Ensure ALL 10 HEAD events sit on clean walkable snow
    for e in events:
        ex, ey = e['at']
        if m.cls[ey, ex] in 'T':
            m.cls[ey, ex] = '.'
    m.cls[15, 0] = 'd'

    R_ = types.SimpleNamespace(m=m, seed=563, road_mask=np.isin(m.cls, ['d']), events=events, rng=rng)
    ev_mask = reserve_events(m, events, R_.road_mask, radius=1, extra=[(1, 15), (29, 3), (29, 8)])
    CK.thin_bands(R_, passes=2)

    # Signboards for Snowveil Shrine [28, 21] & Silk-fall [14, 9]
    m.tile(4847, 28, 21, 1)
    m.tile(4847, 14, 9, 1)

    # 5. SACRED FROZEN SILK-FALL & SNOWVEIL SHRINE OVERLOOK (ACTUALLY BUILT!)
    # Frozen Silk-fall waterfall down the north cliff face
    m.stamp('fw_fall', 16, 4, mark='B')

    # Snowveil Shrine Overlook: pf_shrine (2x3) directly north of sign [28, 21] at (28, 18), flanked by glowing braziers!
    m.cls[17:22, 26:32] = '.'
    m.cls[21, 28] = 'd'; m.cls[22, 27:30] = 'd'
    m.stamp('pf_shrine', 28, 17, mark='B')
    for n, x, y in (
        ('fw_brazier', 26, 18), ('fw_brazier', 30, 18),      # twin warm fire-bowls flanking the shrine altar!
        ('pf_logbench', 24, 21), ('fw_stone', 31, 21),
        ('pf_lantern', 26, 22), ('pf_lantern', 30, 22),
        # Warm trail lanterns & Silk-fall framing
        ('pf_lantern', 3, 14), ('pf_lantern', 7, 17), ('pf_lantern', 17, 24),
        ('pf_lantern', 27, 8), ('pf_lantern', 31, 8),
        ('fw_brazier', 15, 9), ('fw_brazier', 20, 9),
        ('fw_wood', 4, 18), ('fw_stone', 9, 12), ('fw_stone', 24, 10), ('fw_skull', 21, 20),
    ):
        s = STAMPS[n]
        if m.inb(x, y) and m.free(x, y, s['w'], s['h'], on='.dt') and not ev_mask[y:y + s['h'], x:x + s['w']].any():
            m.stamp(n, x, y, mark='B')

    # Crystal frost spires flanking the frozen Silk-fall & wild frosted corner giant trees + teal pine sentinels!
    for tx, ty, sp in (
        (13, 6, KF_CRYS_STAR), (21, 6, KF_CRYS_BLADES), (14, 7, KF_CRYS_MONO), (20, 7, KF_CRYS_MONO),
        (10, 8, KF_TEAL_PINE_A), (22, 7, KF_TEAL_PINE_B), (5, 10, KF_TEAL_PINE_B), (26, 11, KF_TEAL_PINE_A),
        (4, 20, KF_TEAL_PINE_A), (23, 24, KF_TEAL_PINE_B), (10, 24, KF_TEAL_PINE_A), (30, 14, KF_TEAL_PINE_B),
        (11, 18, KF_BOULDER), (25, 17, KF_BOULDER), (7, 13, KF_BOULDER),
    ):
        put_sprite(m, tx, ty, *sp, on='.tT', avoid_mask=ev_mask)

    for nm, x, y in (('pf_g_tree2_ice', 0, 0), ('pf_g_tree2_ice', 30, 23), ('pf_g_tree2_ice', 0, 23)):
        s = STAMPS[nm]
        if m.inb(x, y) and m.free(x, y, s['w'], s['h'], on='T.t') and not ev_mask[y:y + s['h'], x:x + s['w']].any():
            m.stamp(nm, x, y, mark='B', blend=True)

    # 6. Dense Interlocking Alpine Spruce Amphitheater (ZERO bubble-wrap rock spam!)
    CK.woods(R_, ALPINE_WOODS, scale=7.5, accents={'snowblue': 0.08})
    CK.fringe(R_, ['pine2', 'kf_tree', 'pine2'], 22, seed=1, near_forest=3)

    m.events = events
    m.paint()
    infill_winter(R_, ALPINE_WOODS, scale=7.5, seed=563)

    # 8. Proven Solvable Silk-Fall Slide Puzzle (reaching NEVERMELTICE [19, 13] in >= 4 slides & sliding back!)
    pond_cells = [tuple(c[::-1]) for c in np.argwhere(m.cls == 'p')]
    for x, y in slide_puzzle(m, pond_cells, ISLET, (19, 13), n_rocks=(10, 16), tries=3500, seed=17):
        m.L[1, y, x] = 10371 if (x + y) % 3 else 10551

    # Frozen silk strands over the Silk-fall + Dramatic Winter Light Shafts & Sacred Shrine Glow!
    for y in range(4, 9):
        for x in range(16, 20):
            if (x + y) % 2 == 0 and m.L[2, y, x] == 0:
                m.L[2, y, x] = STAMPS['pf_p_strand_w']['layers'][1][0][0] or m.L[2, y, x]
    rime_silk(m, ((6, 6), (12, 5), (24, 6), (5, 13), (30, 12)))

    for sx_, sy_ in ((17, 6), (18, 11), (28, 17), (27, 1), (9, 16)):
        put_overlay_stamp(m, 'cv_shaft', sx_, sy_, z=2)
    for gx_, gy_ in ((17, 8), (18, 12), (28, 19), (26, 18), (30, 18), (28, 1)):
        put_overlay_stamp(m, 'pf_glow', gx_, gy_, z=2)

    # Micro-detailing: frosted reeds along the lakefront, drifts, snow wind ripples, icicles!
    reed_beds(m, 20, seed=563, avoid_mask=ev_mask)
    drifts(m, 0.14, seed=564)
    CK.snow_ground_var(R_, thr=0.38)
    road_tracks(m, 0.11, seed=563)
    icy_faces(m, p=0.28, seed=563)

    seal_unconnected_edges(
        m,
        open_cells=[tuple(e['at']) for e in events if e.get('type') == 'warp'],
        filler=10371,
    )
    h = {k: v for k, v in hs.items() if k != 'events'}
    h['_file'] = '563_rimewood_glade.yaml'
    m.write(563, h, '# Rimewood Glade (563). WRITTEN BY layouts/wave11_wilds_craft.py (Wave 11 Rejuv V14 Craft).\n')
    print('  built 563 Rimewood Glade (%dx%d, %d events)' % (W, H, len(events)))


# =============================================================================
# 8. MAP 570 — FROSTWICK (60x48, ts 52, warm lantern-lit alpine village)
# =============================================================================
def build_570():
    W, H = 60, 48
    hs = head_spec(570)
    events = hs['events']

    TL, NL, EL = 12, 8, 5
    SQ0 = 22
    ROAD = (23, 25)
    LANE = (36, 38)

    # Graceful S-curving Hoar Brook (keeps Ice-fisher [32,17] on brook ice & Old woman [30,33] on cozy snow bank!)
    def fw_bx(y):
        if y <= 21:
            return 29 + int(round(1.4 * math.sin(y / 5.5)))
        if 27 <= y <= 35:
            return 31 + int(round(0.6 * math.sin((y - 27) / 3.0)))  # bends gently east so (30,33) is snow bank!
        return 29 + int(round(1.3 * math.sin(y / 5.8)))

    m = snowmap(W, H, 570, kit='shs')
    rng = random.Random(57011)

    # 1. Terraces (NW Elowen treehouse terrace, North band, NE mountain bench)
    def lip(x):
        if x <= 24:
            return TL
        if x <= 35:
            return NL
        return EL + (1 if vnoise(x, 0, 3, 5.0) > 0.6 else 0)

    for x in range(W):
        for y in range(H):
            if y <= lip(x):
                m.ht[y, x] = 1

    # 2. Meandering Hoar Brook ('p') + Plunge Pool + Natural Frozen Southern Lagoon (ZERO robotic stone-teeth fence!)
    for y in range(H):
        bx = fw_bx(y)
        w_brook = 3 if 27 <= y <= 35 else 4
        for x in range(bx, bx + w_brook):
            if 0 <= x < W:
                m.cls[y, x] = 'p'
    m.blob(31.8, 13.5, 3.2, 2.0, 'p', seed=31, rough=0.4, only='.')   # plunge pool below waterfall

    # Southern frozen salt lagoon: shore ice ('I') organically transitioning to DEEP OPEN SEA ('o'/'W') along y=45..47!
    for y in range(40, H):
        for x in range(W):
            shore_y = 40.0 + 1.8 * math.sin(x / 7.5) + 1.6 * (vnoise(x, 0, 4, 6.0) - 0.5)
            if y >= shore_y:
                m.cls[y, x] = 'o'
    # Walkable shore ice on upper lagoon (y=40..44), impassable open sea-ice water on y=45..47 (ZERO stone teeth!)
    for y, x in np.argwhere(m.cls == 'o'):
        if y <= 44 and vnoise(x, y, 12, 3.5) < 0.68:
            m.cls[y, x] = 'I'
        elif y == 45 and vnoise(x, y, 12, 3.5) < 0.30:
            m.cls[y, x] = 'I'
    # Deep abyssal sea-ice leads ('W') inside outer sea water ('o')
    o_mask = (m.cls == 'o')
    pad_o = np.pad(o_mask, 1, constant_values=True)
    o_inner = o_mask & pad_o[:-2, 1:-1] & pad_o[2:, 1:-1] & pad_o[1:-1, :-2] & pad_o[1:-1, 2:]
    for y, x in np.argwhere(o_inner):
        if y >= 45 and vnoise(x, y, 5709, 3.5) > 0.35:
            m.cls[y, x] = 'W'

    # Ensure hidden SNOWBALL [40, 41] and Swinub herder [50, 39] sit on solid walkable shore/ice!
    for gx, gy in ((40, 41), (40, 40), (41, 41), (39, 41), (50, 39), (50, 40)):
        if m.cls[gy, gx] in 'oW':
            m.cls[gy, gx] = 'I'

    # 3. Dense Overlapping Snowy Evergreen Canopy (North, NE ridge, West flank, & East pine windbreak!)
    for y in range(H):
        for x in range(W):
            if m.cls[y, x] != '.':
                continue
            north = m.ht[y, x] == 1 and (y <= lip(x) - 5 + 2 * vnoise(x, 0, 7, 4.0) or x >= 36)
            west = x <= 2 + 1.5 * vnoise(0, y, 6, 4.0) and y > TL and y < 40
            if north or west:
                m.cls[y, x] = 'T'
    for y in range(0, 3):
        for x in range(0, 25):
            if m.cls[y, x] == '.':
                m.cls[y, x] = 'T'

    # 4. Warm Curved Packed-Snow Village Lanes & Hearth Plazas (NO sterile grid!)
    m.rect(27, 0, 4, NL, 'd', only='.T')                               # Exact North path to 578 (x=27..30!)
    m.stairs(26, NL, w=3, kit_rows=4)
    m.lane([(27.5, NL + 4), (26.5, 15.5), (25.5, 18.5), (24.5, 22)], 'd', 2.6, seed=71, wobble=0.45)
    m.blob(19.5, 25.5, 11.5, 4.2, 'd', seed=72, rough=0.35, only='.T')  # West market plaza
    m.blob(41.5, 25.8, 7.8, 4.0, 'd', seed=73, rough=0.35, only='.T')   # East Hearth Elder plaza
    m.lane([(46, 25.0), (51, 24.2), (55, 24.4), (60, 24.5)], 'd', 3.0, seed=74, wobble=0.35)
    m.rect(56, 23, 4, 4, 'd', only='.T')                                # Exact East Gate to 577 (y=23..26!)
    m.lane([(3, TL - 1.2), (9, TL - 1.6), (15, TL - 1.0), (23, TL - 1.5)], 'd', 1.9, seed=75, wobble=0.3)
    m.rect(9, TL - 1, 3, 1, 'd', only='.T')
    m.stairs(9, TL, w=3, kit_rows=4)
    m.lane([(10.5, TL + 4), (9.2, 18.5), (10.5, 22)], 'd', 2.3, seed=76, wobble=0.5)
    m.lane([(2, 37.2), (11, 37.5), (21, 36.8), (30, 37.2), (40, 37.5), (50, 36.8), (57, 37.2)], 'd', 2.5, seed=77, wobble=0.6)
    m.lane([(26.5, 29), (28.5, 32.5), (27.5, 36.5)], 'd', 2.2, seed=78, wobble=0.45)
    m.lane([(45, 38), (45.5, 41)], 'd', 2.6, seed=79, wobble=0.2)
    smooth_cls(m, 'd', into='.', passes=1)

    # South Gate packed-snow causeway over the lagoon ice: strictly x=4..6 at y=47 (matching 560!)
    for y in range(LANE[1] - 1, H):
        for x in range(4, 7):
            m.cls[y, x] = 'd'
    # Make sure South Gate sign [8, 44] is reachable beside the South Gate lane!
    for x in (7, 8, 9):
        for y in (43, 44, 45):
            if y < 46:
                m.cls[y, x] = 'I'
    m.cls[46:48, 7:10] = 'o'
    m.cls[46:48, 0:4] = 'o'

    # 5. Frozen Waterfall + ALL 6 Iconic Frostwick Buildings (100% EXACT door coords!)
    m.stamp('fw_fall', fw_bx(NL), NL - 1)

    m.stamp('pf_g_tree6_ice', 1, 2, None, None, blend=True)          # Loft door [5, 9]
    m.stamp('pf_g_tree4_ice', 11, 3, blend=True)                     # Elowen treehouse 2
    m.stamp('pf_g_tree4p_ice', 18, 2, blend=True)                    # Elowen treehouse 3
    m.stamp('wb_inn', 13, TL + 4, None, None)                        # Two Hearths door [19, 21]
    m.stamp('pf_g_elder_ice', 34, SQ0 - 12, None, None)              # Exchange door [40, 21]
    m.stamp('wb_long2', 46, SQ0 - 6, None, None)                     # Border House door [48, 21]
    m.stamp('wb_gate', 54, ROAD[1] - 4)                              # Briar-wrapped whalebone East Gate
    m.stamp('wb_pc', 2, LANE[0] - 7, None, None)                     # Poke Center door [6, 34]
    m.stamp('wb_hut', 14, LANE[0] - 6, None, None)
    m.stamp('wb_long3', 33, LANE[0] - 7, None, None)
    m.stamp('wb_short', 45, LANE[0] - 6, None, None)
    m.stamp('wb_smoke', 52, LANE[0] - 7, None, None)                 # Smokehouse door [55, 34]
    m.events = []

    # Warm worn-earth door aprons (KristilineDirt 'e') at doorways only (no muddy puddles in snowy yards!)
    for dx, dy in ((5, 9), (19, 21), (40, 21), (48, 21), (6, 34), (55, 34), (16, 34), (39, 34), (48, 34)):
        doorstep(m, (dx, dy))

    # East palisade along x=58 (leaving East Gate y=21..26 cleanly open!)
    for y in range(7, 40):
        if not (21 <= y <= 26) and m.cls[y, 58] in '.T' and m.ht[y, 58] == 0 and not m.taken[y, 58]:
            m.stamp('fw_pal_v', 58, y, mark='B')

    # Reserve ALL 26 HEAD events BEFORE placing market/yard props & cozy evergreen clusters!
    R_ = types.SimpleNamespace(m=m, seed=570, road_mask=np.isin(m.cls, ['d']), events=events, rng=rng)
    ev_mask = reserve_events(m, events, R_.road_mask, radius=1,
                             extra=[(27, 0), (28, 0), (29, 0), (30, 0), (59, 23), (59, 24), (59, 25), (59, 26),
                                    (4, 47), (5, 47), (6, 47), (5, 10), (19, 22), (40, 22), (48, 22), (6, 35), (55, 35)])

    # Signboards for Town/PC/Exchange/Inn signs (Hearth Stone & South Gate sign keep clean custom graphics)
    for sx, sy in ((53, 26), (10, 36), (43, 22), (22, 22), (8, 44)):
        m.tile(4847, sx, sy, 1)

    # 6. Cozy Warm Market Square, Hearth Stone, Braziers, Banners & Village Life Props!
    for n, x, y in (
        ('fw_stall_e', 6, 23), ('fw_stall_e', 11, 24), ('fw_stall_e', 16, 24),
        ('fw_stall_i', 37, 25), ('fw_stall_i', 41, 25),
        ('fw_stone', 24, 24),                                # The Hearth Stone right beside sign [23, 25]
        ('pf_logbench', 22, 27), ('pf_logbench', 25, 27), ('pf_logbench', 36, 28),
        ('sh_campfire', 25, 21), ('fw_sled', 44, 28), ('sh_crates', 45, 26), ('fw_wood', 34, 28),
        # Warm flickering braziers illuminating plaza, bridges, East Gate & Old Woman's brookside!
        ('fw_brazier', 21, 23), ('fw_brazier', 13, 28), ('fw_brazier', 35, 23), ('fw_brazier', 45, 24),
        ('fw_brazier', 29, 32),                              # Cozy brazier right beside Old woman [30, 33]!
        ('fw_brazier', 53, 22), ('fw_brazier', 53, 25),      # East Gate warm braziers!
        ('fw_brazier', 28, 22), ('fw_brazier', 33, 22),      # Brook bridgehead braziers!
        ('fw_ban_e', 12, 21), ('fw_ban_i', 23, 21), ('fw_ban_e', 52, 21), ('fw_ban_i', 47, 26),
        # Cozy lived-in village yards (woodpiles, drying racks, sleds, crates, glowing lanterns!)
        ('fw_rack', 23, 31), ('fw_wood', 21, 34), ('fw_sled', 25, 33), ('fw_rack', 33, 39),
        ('fw_sled', 47, 39), ('fw_rack', 54, 39), ('fw_skull', 33, 27), ('fw_wood', 5, 18),
        ('fw_wood', 47, 13), ('fw_rack', 51, 13), ('fw_sled', 20, 39), ('fw_skull', 6, 39),
        ('sh_crates', 43, 27), ('sh_crates', 20, 27), ('fw_wood', 28, 34), ('fw_wood', 11, 29),
        ('fw_wood', 49, 28), ('sh_crates', 10, 32), ('fw_sled', 15, 19),
        ('pf_lantern', 8, 20), ('pf_lantern', 25, 19), ('pf_lantern', 46, 22), ('pf_lantern', 12, 37),
        ('pf_lantern', 34, 35), ('pf_lantern', 51, 35), ('pf_lantern', 4, 9), ('pf_lantern', 20, 9),
        ('pf_lantern', 25, 11), ('pf_lantern', 29, 11), ('pf_lantern', 27, 35), ('pf_lantern', 33, 35),
        ('pf_lantern', 5, 42), ('pf_lantern', 7, 39), ('pf_lantern', 43, 39),
    ):
        s = STAMPS[n]
        if m.inb(x, y) and m.free(x, y, s['w'], s['h'], on='.de') and not ev_mask[y:y + s['h'], x:x + s['w']].any():
            m.stamp(n, x, y, mark='B')

    # Frozen fishing boats & weathered timber jetty out onto the southern ice
    for nm, x, y in (('fw_boat', 38, 42), ('fw_boat', 49, 42), ('fw_boat_over', 15, 39), ('fw_boat_over', 52, 39)):
        s = STAMPS[nm]
        if m.inb(x, y) and m.free(x, y, s['w'], s['h'], on='.I') and not ev_mask[y:y + s['h'], x:x + s['w']].any():
            m.stamp(nm, x, y, mark='B')

    for y in range(LANE[1] + 1, 45):
        for i, x in enumerate((44, 45, 46)):
            m.tile(C('ak', (1516 if y == LANE[1] + 1 else 1524) + i), x, y, 1)
            m.cls[y, x] = 'D'

    # 7. Cozy Overlapping Snowy Evergreen Clusters Framing EVERY House Yard & Village Edge (NO sterile white voids!)
    for tx, ty, sp in (
        # Framing the NE mountain slope & Exchange Elder
        (45, 9, KF_TEAL_PINE_A), (48, 10, KF_TEAL_PINE_B), (52, 9, KF_SPRUCE_A), (55, 11, KF_TEAL_PINE_A),
        (54, 15, KF_TEAL_PINE_B), (55, 18, KF_TEAL_PINE_A),
        # Framing the West forest slope & Inn / PC yards
        (3, 15, KF_TEAL_PINE_A), (6, 15, KF_TEAL_PINE_B), (2, 20, KF_SPRUCE_B), (4, 24, KF_TEAL_PINE_A),
        (1, 26, KF_TEAL_PINE_B), (11, 29, KF_TEAL_PINE_A), (25, 29, KF_TEAL_PINE_B),
        # Cozy village pocket evergreens breaking up open yards
        (26, 13, KF_TEAL_PINE_A), (35, 18, KF_TEAL_PINE_B), (50, 27, KF_TEAL_PINE_A),
        (20, 31, KF_TEAL_PINE_A), (22, 33, KF_SHRUB_A), (43, 31, KF_TEAL_PINE_B),
        # Backing up the East palisade south of East Gate
        (56, 28, KF_TEAL_PINE_B), (56, 36, KF_TEAL_PINE_A), (54, 36, KF_SHRUB_B),
        # Terrace edge pines & snow boulders
        (23, 8, KF_TEAL_PINE_A), (1, 12, KF_BOULDER), (26, 18, KF_BOULDER), (42, 13, KF_BOULDER),
    ):
        put_sprite(m, tx, ty, *sp, on='.T', avoid_mask=ev_mask)

    for nm, tx, ty in (('kf_tree', 53, 12), ('kf_tree', 2, 14), ('pine2', 11, 33), ('pine2', 24, 34), ('pine2', 3, 22), ('pine2', 56, 15)):
        s = STAMPS[nm]
        if m.inb(tx, ty) and m.free(tx, ty, s['w'], s['h'], on='.T') and not ev_mask[ty:ty + s['h'], tx:tx + s['w']].any():
            m.stamp(nm, tx, ty, mark='B')

    # Interlocking Alpine Spruce Forest for all 'T' woodland margins
    CK.thin_bands(R_, passes=1)
    CK.woods(R_, ALPINE_WOODS, scale=8.5, accents={'snowblue': 0.06})
    m.events = events
    m.paint()
    infill_winter(R_, ALPINE_WOODS, scale=8.5, seed=570)

    # 9. Bridges, Lagoon Ice, Fishing Holes, Rope Walkways, Hearth Smoke & Warm Lighting!
    bridges_snow(m, (ROAD, LANE), cls='p')
    for y, x in np.argwhere(m.cls == 'I'):
        m.L[0, y, x] = ice_at(x, y)

    hole = STAMPS['fw_hole']['layers'][1][0][0]
    holet = STAMPS['fw_hole_t']['layers'][1][0][0]
    for i, (x, y) in enumerate(((31, 16), (30, 19), (32, 29), (32, 33), (31, 40))):
        if m.cls[y, x] == 'p' and m.L[1, y, x] == 0 and m.L[2, y, x] == 0 and not ev_mask[y, x]:
            m.L[1, y, x] = holet if i % 2 == 0 else hole
    for y, x in np.argwhere(m.cls == 'I'):
        if vnoise(x, y, 43, 2.0) > 0.87 and m.L[1, y, x] in ICES and not ev_mask[y, x]:
            m.L[1, y, x] = holet if (x + y) % 3 == 0 else hole

    # Overhead rope walkways between Elowen treehouses
    for x0, x1, y in ((8, 11, 7), (16, 18, 7)):
        for x in range(x0, x1 + 1):
            over_tiles(m, 'fw_walk_e' if x == x0 else 'fw_walk_w' if x == x1 else 'fw_walk_h', x, y)

    # Cozy hearth smoke plumes (applewood from Elowen crowns/inn, whale oil from Isenmar longhouses)
    for nm, x, y in (('fw_smoke_a', 6, 0), ('fw_smoke_a', 14, 1), ('fw_smoke_w', 16, TL + 2), ('fw_smoke_a', 22, TL + 2),
                     ('fw_smoke_w', 18, LANE[0] - 8), ('fw_smoke_w', 40, LANE[0] - 8), ('fw_smoke_w', 48, LANE[0] - 8),
                     ('fw_smoke_w', 54, LANE[0] - 8), ('fw_smoke_w', 57, LANE[0] - 8), ('fw_smoke_w', 51, SQ0 - 8)):
        over_tiles(m, nm, x, y)
    rime_silk(m, ((3, 2), (9, 3), (17, 2), (23, 3), (35, 11), (45, 11)))

    # Warm hearth glow halos & atmospheric waterfall/plaza winter light shafts!
    for gx_, gy_ in ((21, 23), (24, 24), (35, 23), (45, 24), (29, 32), (54, 23), (19, 21), (40, 21), (6, 34), (55, 34), (30, 12)):
        put_overlay_stamp(m, 'pf_glow', gx_, gy_, z=2)
    for sx_, sy_ in ((30, 8), (23, 22), (40, 20), (54, 21), (10, 7)):
        put_overlay_stamp(m, 'cv_shaft', sx_, sy_, z=2)

    # Brook ice cracks/drifts, lagoon reeds & floes, snow ripples, icicles down NW terrace cliff!
    dress_ice(m, 0.30, seed=570)
    for y, x in np.argwhere(m.cls == 'p'):
        if m.L[1, y, x] == 0 and m.L[2, y, x] == 0 and not ev_mask[y, x] and vnoise(x, y, 91, 1.5) > 0.62:
            m.L[1, y, x] = STAMPS['fw_crack%d' % ((x + y) % 3)]['layers'][1][0][0] if (x * 3 + y) % 2 else STAMPS['fw_drift%d' % ((x + y) % 3)]['layers'][1][0][0]
    CK.snow_ground_var(R_, thr=0.38)
    road_tracks(m, 0.08, seed=570)
    drifts(m, 0.10, seed=570)
    icy_faces(m, p=0.28, seed=570)

    # Seal N=[27..30] (578), E=[23..26] (577), S=[4..6] (560) — y=47 is already dark sea water so ZERO grey stone teeth!
    m.seal_against(hs['connections'], spans=[('N', 27, 4), ('E', 23, 4), ('S', 4, 3)])
    seal_unconnected_edges(
        m,
        open_cells=[(x, 0) for x in range(27, 31)] +
                   [(W - 1, y) for y in range(23, 27)] +
                   [(x, H - 1) for x in range(4, 7)] +
                   [tuple(e['at']) for e in events if e.get('type') == 'warp'],
        filler=10371,
    )
    h = {k: v for k, v in hs.items() if k != 'events'}
    h['_file'] = '570_frostwick.yaml'
    m.write(570, h, '# Frostwick (570). WRITTEN BY layouts/wave11_wilds_craft.py (Wave 11 Rejuv V14 Craft).\n')
    print('  built 570 Frostwick (%dx%d, %d events)' % (W, H, len(events)))


BUILDERS = {524: build_524, 525: build_525, 562: build_562, 563: build_563, 570: build_570}


def main():
    args = [int(a) for a in sys.argv[1:] if a.isdigit()]
    targets = args or [524, 525, 562, 563, 570]
    for mid in targets:
        if mid not in BUILDERS:
            raise SystemExit('wave11_wilds_craft: unknown map %d' % mid)
        BUILDERS[mid]()


if __name__ == '__main__':
    main()
