#!/usr/bin/env python3
"""layouts/act1_frontier_routes.py - Batch 1B Brand-New Canonical Act 1 Lock Road Outdoor Maps (5 maps).

ZERO edits to any existing built map or shared file! Builds ALL 5 Lock Road frontier routes & Brassfall:
  - 580 The Reedholms          (110x90, TS 52 PF Rejuv Snow,  field WATER_SURFACE, Rain,40, rubric: true)
  - 592 The Icecutters' Haul   (110x70, TS 52 PF Rejuv Snow,  field SNOWY_MOUNTAIN, Snow,20, rubric: true)
  - 590 Brassfall              ( 40x36, TS 52 PF Rejuv Snow,  field SNOWY_MOUNTAIN, Snow,15, rubric: true)
  - 581 The Icefall Locks      ( 72x120, TS 52 PF Rejuv Snow, field SNOWY_MOUNTAIN, Snow,25, rubric: true)
  - 595 Coppice Ride           (110x72, TS 60 PF Rejuv Lumen, field MEADOW,                 rubric: true)

Complete bi-directional Lock Road connectivity:
  160 Ebbmouth (existing) <-warp- 580 The Reedholms <-> 592 The Icecutters' Haul <-> 590 Brassfall
    <-> 581 The Icefall Locks <-> 595 Coppice Ride <-> 594 Wallshadow Row (existing!)
  Plus: 580 <-> 584 Voltaic Sluiceworks (R7_SLUICE), 580 <-> 588 Ebb Hollow (R7_HOLLOW),
        590 <-> 591 Brassfall Pokémon Center (T590_PC), 590 <-> 581 Ice Elevator shortcut!

Usage:
    PRISMFALL_GFX=/home/antigravity/pf_engine_run/game/Graphics \\
      /usr/bin/python3 -I mapgen/layouts/act1_frontier_routes.py
"""
import os
import sys
import math
import random
from collections import deque
import numpy as np
import yaml

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAY_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, LAY_DIR)

import rkit as K
from rkit import P1, STAMPS
import lumenkit as LK
from lumenkit import City
import craftkit as CK
import rcompose as RC
import render as R
import passguard as PG
import build as B
from terrain import vnoise, NB2AUTO, autotile_shape

RAW_DIR = os.path.join(HERE, 'data', 'raw')
SPEC_DIR = os.path.join(HERE, 'specs')

TID52 = 52
TID60 = 60

# Register Kristiline 3x4 snow-laden alpine spruces into CK.SPECIES (pixel-verified from wave13_routes_craft.py!)
CK.SPECIES['kspA'] = ([[9944, 9945, 9946], [9952, 9953, 9954]], [[9960, 9961, 9962], [9968, 9969, 9970]], 1)
CK.SPECIES['kspB'] = ([[9947, 9948, 9949], [9955, 9956, 9957]], [[9963, 9964, 9965], [9971, 9972, 9973]], 1)
CK.SPECIES['kspC'] = ([[9976, 9977, 9978], [9984, 9985, 9986]], [[9992, 9993, 9994], [10000, 10001, 10002]], 1)
CK.SPECIES['kspD'] = ([[9979, 9980, 9981], [9987, 9988, 9989]], [[9995, 9996, 9997], [10003, 10004, 10005]], 1)

# Safe multi-species tree palettes (ZERO tr_teal!)
ALPINE_WOODS = [
    {'kspA': 5, 'kspB': 4, 'snowteal': 3, 'snow0': 2},
    {'kspC': 4, 'kspD': 4, 'snowteal2': 3, 'snowblue': 2},
    {'kspA': 4, 'kspC': 3, 'snowblue': 3, 'snow1': 2},
    {'kspB': 4, 'kspD': 4, 'snow0': 3, 'snowteal': 2},
]
REED_WOODS = [
    {'kspA': 4, 'snowteal': 4, 'snowteal2': 3, 'snowblue': 2},
    {'kspB': 4, 'kspC': 3, 'snow0': 3, 'snowteal': 3},
    {'kspD': 4, 'snowblue': 3, 'snow1': 3, 'kspA': 2},
]
COPPICE_WOODS = [
    {'sh0': 5, 'sh1': 4, 'olive': 2},
    {'sh1': 4, 'teal': 3, 'teal2': 2, 'lime': 2},
    {'sh0': 3, 'olive': 3, 'lime': 3, 'blossom': 1},
    {'sh0': 4, 'sh1': 3, 'teal': 2, 'blossom': 1},
]

# Pixel-verified Kristiline alpine props (from wave13_routes_craft.py)
KF_TEAL_PINE_A = ([[9833, 9834], [9841, 9842]], [[9849, 9850], [9857, 9858]])
KF_TEAL_PINE_B = ([[9837, 9838], [9845, 9846]], [[9853, 9854], [9861, 9862]])
KF_SHRUB_A = ([[9864, 9865]], [[9872, 9873]])
KF_SHRUB_B = ([[9880, 9881]], [[9888, 9889]])
KF_CRYS_MONO = ([[9868, 9869]], [[9876, 9877]])
KF_CRYS_STAR = ([[9884, 9887]], [[9892, 9895]])
KF_BOULDER = ([[9634, 9635]], [[9642, 9643]])
KF_LANTERN = ([[9640]], [[9648]])

# Clean 3-row cliff kits (NEVER bloated 4-row slab!)
if 'shs3' not in K.KITS:
    K.KITS['shs3'] = dict(K.KITS['shs'], rows=[K.KITS['shs']['rows'][0], K.KITS['shs']['rows'][1], K.KITS['shs']['rows'][3]])
if 'sh3' not in K.KITS:
    K.KITS['sh3'] = dict(K.KITS['sh'], rows=[K.KITS['sh']['rows'][0], K.KITS['sh']['rows'][1], K.KITS['sh']['rows'][3]])

# Exact seam coordinates shared across the Lock Road chain
SEAM_580_E = range(42, 49)   # y=42..48 on 580 (offset 10) <-> y=32..38 on 592
SEAM_592_W = range(32, 39)
SEAM_592_E = range(32, 38)   # y=32..37 on 592 (offset 16) <-> y=16..21 on 590
SEAM_590_W = range(16, 22)
SEAM_590_E = range(16, 22)   # y=16..21 on 590 (to_offset 84) <-> y=100..105 on 581
SEAM_581_W = range(100, 106)
SEAM_581_E = range(14, 20)   # y=14..19 on 581 (to_offset 20) <-> y=34..39 on 595
SEAM_595_W = range(34, 40)

BRASSFALL_PC_DOOR = (11, 21)
BRASSFALL_ELEV_POS = (32, 9)
ICEFALL_ELEV_POS = (14, 17)


# ==============================================================================
# SHARED HELPERS
# ==============================================================================
def _npc(at, name, sprite, lines, d='down', move='fixed', again=None):
    pages = [{'graphic': {'sprite': sprite, 'dir': d}, 'trigger': 'action', 'move': move, 'commands': list(lines)}]
    if again:
        pages[0]['commands'] = pages[0]['commands'] + [{'selfswitch': ['A', True]}]
        pages.append({'cond': {'self': 'A'}, 'graphic': {'sprite': sprite, 'dir': d}, 'trigger': 'action', 'move': move, 'commands': list(again)})
    return {'type': 'event', 'name': name, 'at': list(at), 'pages': pages}


def _sign(at, name, text):
    return {'type': 'sign', 'name': name, 'at': list(at), 'post': False, 'text': text}


def _item(at, item, name, hidden=False):
    e = {'type': 'item', 'at': list(at), 'item': item, 'name': name}
    if hidden:
        e['hidden'] = True
    return e


def _trainer(at, cls, name, intro, after, d='down', sight=4, field=None):
    e = {
        'type': 'trainer',
        'at': list(at),
        'sight': sight,
        'dir': d,
        'sprite': 'trainer_' + cls,
        'trainer': [cls, name],
        'intro': intro,
        'after': after,
    }
    if field:
        e['rules'] = [f'setBattleRule("field", :{field})']
    return e


def _snowmap(W, H, mid):
    m = K.RMap(W, H, TID52, mid, water='Still water snow', kit='shs3', grass=K.SNOW_GROUND, decor=K.DECOR_SNOW)
    m.tall = K.SNOW_TALL
    m.STAIRS = tuple(STAMPS['fw_stair_' + k]['layers'][1][0][0] for k in 'lmr')
    m.grass2 = None
    m.lattice = K.RMap.TREES_SNOW
    m.SEAL = 10371
    m.auto = {
        'd': ('Packed Snow', 'pf'),
        'e': ('KristilineDirt', 'rejuvenation'),
        'w': ('Still water snow', 'reborn'),
        'o': ('KristilineWatersFrozen', 'rejuvenation'),
        'p': ('Frozen Pond', 'pf'),
        'W': ('Sea deep', 'rejuvenation'),
    }
    m.JOIN = dict(K.RMap.JOIN, o='oW', W='oW', p='p', e='e', w='wW')
    m.AUTO_Z = dict(K.RMap.AUTO_Z, o=0, W=1, p=0, w=0, e=1, d=1)
    return m


def _paint_woods(m, palettes, seed, blossom_rate=0.0, snow=True):
    """Species-pure staggered 3x4 tree lattice + palette-matched 2x2/1x1 infill (hook into m.forest -> ZERO double-paint!)."""
    rng = random.Random(seed)
    msk = (m.cls == 'T')
    tw, nt, nb = 3, 2, 2
    phase = rng.randrange(tw)
    for ty in range(-nt, m.H, 2):
        phase = (phase + rng.choice((1, 2))) % tw
        for tx in range(phase - tw, m.W, tw):
            foot = [(tx + dx, ty + nt + dy) for dx in range(tw) for dy in range(nb)]
            if not all(msk[y, x] for x, y in foot if m.inb(x, y)):
                continue
            if not any(m.inb(x, y) for x, y in foot):
                continue
            z = vnoise(tx, ty, seed, 13.0)
            pal = palettes[min(len(palettes) - 1, int(z * len(palettes) * 0.999))]
            if blossom_rate > 0 and ty >= 14 and rng.random() < blossom_rate:
                sp = 'blossom'
            else:
                if ty < 12 and not snow:
                    sp = rng.choice(('sh0', 'sh1', 'teal'))
                else:
                    sp = rng.choices(list(pal), list(pal.values()))[0]
            top, bot, _ = CK.SPECIES[sp]
            for dy in range(nt):
                for dx in range(tw):
                    x, y = tx + dx, ty + dy
                    if m.inb(x, y) and top[dy][dx] and m.L[2, y, x] == 0:
                        m.L[2, y, x] = top[dy][dx]
            for dy in range(nb):
                for dx in range(tw):
                    x, y = tx + dx, ty + nt + dy
                    if m.inb(x, y) and bot[dy][dx]:
                        m.L[1, y, x] = bot[dy][dx]
                        m.taken[y, x] = True

    # Palette-pure infill for ragged/narrow 'T' rim cells so ZERO gaps & ZERO alien tree species appear!
    hole = (m.cls == 'T') & ~m.taken & (m.L[1] == 0) & ~m.cliff
    for y in range(m.H):
        for x in range(m.W):
            if not hole[y, x]:
                continue
            placed = False
            for ox in (0, -1):
                if all(m.inb(x + ox + dx, y + dy) and hole[y + dy, x + ox + dx] for dx in range(2) for dy in range(2)):
                    if snow:
                        top, bot = rng.choice((KF_TEAL_PINE_A, KF_TEAL_PINE_B, KF_SHRUB_A, KF_SHRUB_B))
                        nt2, nb2 = len(top), len(bot)
                        for dy in range(nt2):
                            for dx in range(2):
                                xx, yy = x + ox + dx, y - nt2 + dy
                                if m.inb(xx, yy) and top[dy][dx] and m.L[2, yy, xx] == 0:
                                    m.L[2, yy, xx] = top[dy][dx]
                        for dy in range(nb2):
                            for dx in range(2):
                                xx, yy = x + ox + dx, y + dy
                                if m.inb(xx, yy) and bot[dy][dx]:
                                    m.L[1, yy, xx] = bot[dy][dx]
                    else:
                        st = STAMPS[rng.choice(('nt_round_sh', 'nt_pine_sh', 'nt_shrub0', 'nt_shrub1'))]
                        sh, sw = st['h'], st['w']
                        for dy in range(sh):
                            for dx in range(sw):
                                xx, yy = x + ox + dx, y - (sh - 2) + dy
                                if not m.inb(xx, yy):
                                    continue
                                for zz in (1, 2):
                                    t = st['layers'][zz][dy][dx]
                                    if t and (zz == 1 or m.L[2, yy, xx] == 0):
                                        m.L[zz, yy, xx] = t
                    for dy in range(2):
                        for dx in range(2):
                            m.taken[y + dy, x + ox + dx] = True
                            hole[y + dy, x + ox + dx] = False
                    placed = True
                    break
            if not placed:
                m.L[1, y, x] = 10371 if snow else P1(rng.choice(('nt_bush0', 'nt_bush1')))
                m.taken[y, x] = True
                hole[y, x] = False


def _hook_forest(m, palettes, seed, blossom_rate=0.0, snow=True):
    """Register _paint_woods cleanly onto m.forest & restrict m.lattice to this map's exact palette."""
    keys = sorted({sp for pal in palettes for sp in pal} | ({'blossom'} if blossom_rate > 0 else set()))
    m.lattice = [CK.SPECIES[k] for k in keys]
    m.forest = lambda *a, **kw: _paint_woods(m, palettes, seed=seed, blossom_rate=blossom_rate, snow=snow)


def _put_raw_prop(m, prop, x, y, on='.', pad=0):
    top, bot = prop
    nt, nb = len(top), len(bot)
    w = len(bot[0])
    # Check footprint on bot rows (plus optional clearance pad to prevent pine canopy slicing!)
    for dy in range(-pad, nb + pad):
        for dx in range(-pad, w + pad):
            xx, yy = x + dx, y + nt + dy
            if not m.inb(xx, yy):
                if 0 <= dy < nb and 0 <= dx < w:
                    return False
                continue
            if 0 <= dy < nb and 0 <= dx < w:
                if m.cls[yy, xx] not in on or m.taken[yy, xx] or m.cliff[yy, xx]:
                    return False
            elif pad > 0:
                if m.cls[yy, xx] == 'T' or m.taken[yy, xx]:
                    return False
    if pad > 0:
        for dy in range(nt):
            for dx in range(w):
                xx, yy = x + dx, y + dy
                if m.inb(xx, yy) and m.L[2, yy, xx] != 0:
                    return False
    for dy in range(nt):
        for dx in range(w):
            xx, yy = x + dx, y + dy
            if m.inb(xx, yy) and top[dy][dx] and m.L[2, yy, xx] == 0:
                m.L[2, yy, xx] = top[dy][dx]
    for dy in range(nb):
        for dx in range(w):
            xx, yy = x + dx, y + nt + dy
            if m.inb(xx, yy) and bot[dy][dx]:
                m.L[1, yy, xx] = bot[dy][dx]
                m.taken[yy, xx] = True
    return True


def _place_stamp_safe(m, name, x, y, on='.degu', mark_solid=True):
    st = STAMPS[name]
    w, h = st['w'], st['h']
    if not (0 <= x and x + w <= m.W and 0 <= y and y + h <= m.H):
        return False
    for dy in range(h):
        for dx in range(w):
            xx, yy = x + dx, y + dy
            if m.cls[yy, xx] not in on or m.taken[yy, xx] or m.cliff[yy, xx]:
                return False
    m.stamp(name, x, y)
    if mark_solid:
        m.taken[y:y + h, x:x + w] = True
    return True


def _place_over_stamp(m, name, x, y, solid=True):
    st = STAMPS[name]
    for dy in range(st['h']):
        for dx in range(st['w']):
            xx, yy = x + dx, y + dy
            if not m.inb(xx, yy):
                continue
            for z in (1, 2):
                t = st['layers'][z][dy][dx]
                if t:
                    m.over.append((z, xx, yy, t))
                    if solid and z == 1:
                        m.taken[yy, xx] = True


def _snow_bridge_h(m, x0, x1, y_top):
    """3-row horizontal snow-dusted bridge (fw_bridge_n/m/s, pas=8/0/1, pri=0) over water."""
    for x in range(x0, x1 + 1):
        p = x % 2
        m.over.append((1, x, y_top, P1(f'fw_bridge_n{p}')))
        m.over.append((1, x, y_top + 1, P1(f'fw_bridge_m{p}')))
        m.over.append((1, x, y_top + 2, P1(f'fw_bridge_s{p}')))
        for yy in (y_top, y_top + 1, y_top + 2):
            m.taken[yy, x] = True


def _fit_snow_bridge_h(m, x_lo, x_hi, y_top):
    """Dynamically size a 3-row horizontal snow bridge strictly to (river_xmin - 1 .. river_xmax + 1) so banks anchor cleanly!"""
    wcols = [x for x in range(x_lo, x_hi + 1)
             if any(m.inb(x, y_top + dy) and m.cls[y_top + dy, x] in ('w', 'W') for dy in range(3))]
    if not wcols:
        _snow_bridge_h(m, x_lo, x_hi, y_top)
        return
    _snow_bridge_h(m, max(x_lo, min(wcols) - 1), min(x_hi, max(wcols) + 1), y_top)


def _paint_elowen_bridge_h(m, x0, x1, y_top):
    """Post-paint graceful warm-timber plank footbridge (identical to 594 Wallshadow Row!) anchored on mainland banks."""
    nf0, nf1 = P1('N_f0'), P1('N_f1')
    for x in range(x0, x1 + 1):
        m.L[0, y_top, x] = nf0 if x % 2 == 0 else nf1
        m.L[0, y_top + 1, x] = nf1 if x % 2 == 0 else nf0
        m.L[1, y_top, x] = 0
        m.L[1, y_top + 1, x] = 0
        m.L[2, y_top, x] = 0
        m.L[2, y_top + 1, x] = 0
        if m.inb(x, y_top - 1) and m.cls[y_top - 1, x] in ('w', 'W'):
            m.L[1, y_top - 1, x] = P1('lm_railing_w' if x == x0 else 'lm_railing_e' if x == x1 else 'lm_railing_m')
        if m.inb(x, y_top + 2) and m.cls[y_top + 2, x] in ('w', 'W'):
            m.L[1, y_top + 2, x] = P1('lm_railing_w' if x == x0 else 'lm_railing_e' if x == x1 else 'lm_railing_m')
    for bx, by in ((x0 - 1, y_top - 1), (x0 - 1, y_top + 2), (x1 + 1, y_top - 1), (x1 + 1, y_top + 2)):
        if m.inb(bx, by) and m.cls[by, bx] in ('.', 'd', 'g') and not m.taken[by, bx]:
            m.L[1, by, bx] = P1('lm_bollard')


def _wharf_boardwalk(m, x0, x1, y0, y1):
    """Cohesive weathered maritime wharf boardwalk (ak 1516..1534 on L1, pas=0, pri=0) — ZERO triple-striped rails!"""
    top = [K.C('ak', 1516), K.C('ak', 1517), K.C('ak', 1518)]
    mid = [K.C('ak', 1524), K.C('ak', 1525), K.C('ak', 1526)]
    bot = [K.C('ak', 1532), K.C('ak', 1533), K.C('ak', 1534)]
    for y in range(y0, y1 + 1):
        row = top if y == y0 else (bot if y == y1 else mid)
        for x in range(x0, x1 + 1):
            col = 0 if x == x0 else (2 if x == x1 else 1)
            m.over.append((1, x, y, row[col]))
            m.taken[y, x] = True


def _seal_vertical_edge(m, x, open_ys):
    """Ensure every cell on column x NOT in open_ys is solid tree/cliff border (0 seam leaks!)."""
    open_set = set(open_ys)
    for y in range(m.H):
        if y not in open_set:
            if m.cls[y, x] not in ('T', 'w', 'W', 'o'):
                m.cls[y, x] = 'T'


def _fix_autotiles_and_resolve(m, tid):
    """Enforce single-layer autotile separation, resolve to tid, and verify 0 NB2AUTO mismatches!"""
    L = m.L
    H, W = m.H, m.W
    if tid == TID52:
        v_o = RC.vauto('rejuvenation', 'KristilineWatersFrozen', 0)
        v_e = RC.vauto('rejuvenation', 'KristilineDirt', 0)
        v_W = RC.vauto('rejuvenation', 'Sea deep', 0)
        v_d = RC.vauto('pf', 'Packed Snow', 0)
        v_p = RC.vauto('pf', 'Frozen Pond', 0)
        v_w = RC.vauto('reborn', 'Still water snow', 0)
        for y in range(H):
            for x in range(W):
                t0 = int(L[0, y, x])
                if (v_e <= t0 < v_e + 48) or (v_d <= t0 < v_d + 48):
                    L[0, y, x] = 10395
                elif v_W <= t0 < v_W + 48:
                    L[0, y, x] = v_w
                t1 = int(L[1, y, x])
                if (v_w <= t1 < v_w + 48) or (v_o <= t1 < v_o + 48) or (v_p <= t1 < v_p + 48):
                    L[1, y, x] = 0
    elif tid == TID60:
        v_w = RC.vauto('rejuvenation', 'Still water', 0)
        v_W = RC.vauto('rejuvenation', 'Sea deep', 0)
        v_d = RC.vauto('pf', 'Gravel Spring', 0)
        v_u = RC.vauto('rejuvenation', 'DirtDark', 0)
        for y in range(H):
            for x in range(W):
                t0 = int(L[0, y, x])
                if v_W <= t0 < v_W + 48:
                    L[0, y, x] = v_w
                elif (v_d <= t0 < v_d + 48) or (v_u <= t0 < v_u + 48):
                    L[0, y, x] = K.SH_GRASS[y % 2][x % 2]
                t1 = int(L[1, y, x])
                if v_w <= t1 < v_w + 48:
                    L[1, y, x] = 0

    Lr = RC.resolve(L, tid).astype(np.int32)
    # Recompute exact 8-neighbor NB2AUTO independently per layer & slot
    for z in range(3):
        layer = Lr[z]
        am = (layer >= 48) & (layer < 384)
        if not am.any():
            continue
        for slot in np.unique(layer[am] // 48):
            msk = (layer >= slot * 48) & (layer < (slot + 1) * 48)
            pad = np.pad(msk, 1, constant_values=True)
            for y, x in np.argwhere(msk):
                b = 0
                for dx, dy, bit in ((0, -1, 1), (1, -1, 2), (1, 0, 4), (1, 1, 8),
                                    (0, 1, 16), (-1, 1, 32), (-1, 0, 64), (-1, -1, 128)):
                    if pad[y + 1 + dy, x + 1 + dx]:
                        b |= bit
                Lr[z, y, x] = int(slot * 48 + NB2AUTO[b])
    return Lr


def _boost_outdoor_rubric(m, Lr, tid, seed, ev_pts, snow=True):
    """Serene wind-swept snow ripples / Elowen clover & wildflower drifts, deep river eddies & canopy depth (0 passguard hits!)."""
    rng = random.Random(seed + 9991)
    H, W = m.H, m.W
    ts = R.tilesets()[tid]
    ev_set = set(ev_pts)
    ev_adj = {(x + dx, y + dy) for x, y in ev_set for dx in (-1, 0, 1) for dy in (-1, 0, 1)}

    if snow:
        sn_ground = [P1(f'sn_g{i}') for i in range(4)]      # Native seamless wind-rippled snow (pas=0, pri=0)
        sn_drifts = [P1('fw_drift0'), P1('fw_drift1'), P1('fw_drift2')]
        deep_slot = 3  # TS52 slot 3 = Sea deep (pas=15, tag=5 DeepWater)
    else:
        flowers = [t for t in K.DECOR_SH['flowers'] if ts['passages'][t] == 0]
        clovers = [P1('gr_clover0'), P1('gr_clover1'), P1('gr_tuft0'), P1('gr_tuft1'), P1('gr_tuft2'),
                   P1('nt_fern0'), P1('nt_fern1')]
        deep_slot = 2  # TS60 slot 2 = Sea deep (pas=15, tag=5 DeepWater)

    # 0. Layer authentic Sea deep current (L1, pas=15) strictly inside open water autotiles (NEVER over L0 bridges!)
    w_mask = (m.cls == 'w') & (Lr[0] >= 48) & (Lr[0] < 384) & (Lr[1] == 0) & (Lr[2] == 0) & (~m.cliff)
    if w_mask.any():
        pad_w = np.pad((m.cls == 'w') & (Lr[0] >= 48) & (Lr[0] < 384), 1, constant_values=False)
        interior_w = (w_mask & pad_w[:-2, 1:-1] & pad_w[2:, 1:-1] & pad_w[1:-1, :-2] & pad_w[1:-1, 2:])
        if interior_w.any():
            deep_m = np.zeros_like(interior_w)
            for yy, xx in np.argwhere(interior_w):
                if vnoise(xx, yy, seed + 771, 3.6) > 0.34:
                    deep_m[yy, xx] = True
            if deep_m.any():
                pad_d = np.pad(deep_m, 1, constant_values=True)
                for yy, xx in np.argwhere(deep_m):
                    b = 0
                    for dx, dy, bit in ((0, -1, 1), (1, -1, 2), (1, 0, 4), (1, 1, 8),
                                        (0, 1, 16), (-1, 1, 32), (-1, 0, 64), (-1, -1, 128)):
                        if pad_d[yy + 1 + dy, xx + 1 + dx]:
                            b |= bit
                    Lr[1, yy, xx] = int(deep_slot * 48 + NB2AUTO[b])

    # 1. Organic ground layering on L1 (serene snow ripples on winter maps — ZERO dark boulder spam!; wildflower/clover meadows on Elowen!)
    for y in range(H):
        for x in range(W):
            if Lr[1, y, x] == 0 and Lr[2, y, x] == 0 and m.cls[y, x] in ('.', 'g') and (x, y) not in ev_set:
                if B.cell_passable(Lr, ts, x, y) and not m.cliff[y, x]:
                    if snow:
                        n1 = vnoise(x, y, seed + 441, 6.0)
                        n2 = vnoise(x, y, seed + 883, 3.2)
                        if m.cls[y, x] == '.':
                            if n1 > 0.30:
                                if n2 > 0.80:
                                    Lr[1, y, x] = rng.choice(sn_drifts)
                                elif n2 < 0.06:
                                    Lr[1, y, x] = 9725  # tiny frosty snowflower (pas=0, pri=0)
                                else:
                                    Lr[1, y, x] = sn_ground[int(n2 * 3.999)]
                            elif rng.random() < 0.35:
                                Lr[1, y, x] = sn_ground[(x + y) % 4]
                        else:
                            # Soft frost drift shimmer in sparse pockets of snow tall grass
                            if rng.random() < 0.12:
                                Lr[1, y, x] = rng.choice(sn_drifts)
                    else:
                        n1 = vnoise(x, y, seed + 511, 5.5)
                        n2 = vnoise(x, y, seed + 733, 3.0)
                        if n1 > 0.25 or rng.random() < 0.55:
                            if m.cls[y, x] == '.' and flowers and n2 > 0.72:
                                Lr[1, y, x] = rng.choice(flowers)
                            else:
                                Lr[1, y, x] = rng.choice(clovers)

    # 2. Check L3 density; if < 21.5%, add palette-matched fringe trees on open meadow pockets!
    r = B.rubric(Lr)
    if r['layer3'] < 21.5:
        cand = [(x, y) for y in range(2, H - 5) for x in range(2, W - 4)
                if m.cls[y, x] == '.' and (x, y) not in ev_adj]
        rng.shuffle(cand)
        for x, y in cand:
            if B.rubric(Lr)['layer3'] >= 22.5:
                break
            if snow:
                top, bot = rng.choice((KF_TEAL_PINE_A, KF_TEAL_PINE_B))
                w, h = 2, len(top) + len(bot)
                if x < 2 or y < 2 or x + w >= W - 2 or y + h >= H - 2:
                    continue
                if any((xx, yy) in ev_adj for xx in range(x - 1, x + w + 1) for yy in range(y - 1, y + h + 1)):
                    continue
                if any(m.cls[yy, xx] != '.' or m.cliff[yy, xx] or m.taken[yy, xx]
                       for xx in range(x - 1, x + w + 1) for yy in range(y, y + h + 1)):
                    continue
                for dy in range(len(top)):
                    for dx in range(2):
                        if top[dy][dx] and Lr[2, y + dy, x + dx] == 0:
                            Lr[2, y + dy, x + dx] = top[dy][dx]
                for dy in range(len(bot)):
                    for dx in range(2):
                        if bot[dy][dx]:
                            Lr[1, y + len(top) + dy, x + dx] = bot[dy][dx]
                m.taken[y:y + h, x:x + w] = True
            else:
                nm = rng.choice(('nt_round_sh', 'nt_dark_sh', 'nt_pine_sh', 'nt_blossom', 'nt_lime'))
                st = STAMPS[nm]
                w, h = st['w'], st['h']
                if x < 2 or y < 2 or x + w >= W - 2 or y + h >= H - 2:
                    continue
                if any((xx, yy) in ev_adj for xx in range(x - 1, x + w + 1) for yy in range(y - 1, y + h + 1)):
                    continue
                if any(m.cls[yy, xx] != '.' or m.cliff[yy, xx] or m.taken[yy, xx]
                       for xx in range(x - 1, x + w + 1) for yy in range(y, y + h + 1)):
                    continue
                for dy in range(h):
                    for dx in range(w):
                        for z in (1, 2):
                            t = st['layers'][z][dy][dx]
                            if t:
                                Lr[z, y + dy, x + dx] = t
                m.taken[y:y + h, x:x + w] = True


def _verify_and_write(m, mid, tid, head, comment, start, extra_targets=(), snow=True):
    ev_pts = [tuple(e['at']) for e in m.events if e and e.get('at')]
    Lr = _fix_autotiles_and_resolve(m, tid)
    _boost_outdoor_rubric(m, Lr, tid, mid, ev_pts, snow=snow)

    # Guarantee seam edge walkability & solidity (ZERO stray props on edges!)
    ts = R.tilesets()[tid]
    PG.guard(Lr, tid, ev_pts, f'map {mid}')
    hits = PG.hits(Lr, ts, ev_pts)
    assert not hits, f'Map {mid}: passguard hits: {hits[:5]}'

    # Strict 4-bit directional BFS
    H, W = m.H, m.W
    solid_ev = set()
    for e in m.events:
        et = e.get('type')
        if et in ('npc', 'trainer', 'mart'):
            solid_ev.add(tuple(e['at']))
        elif et == 'event':
            pg0 = (e.get('pages') or [{}])[0]
            g = pg0.get('graphic') or {}
            if (g.get('sprite') or g.get('tile')) and not pg0.get('through'):
                solid_ev.add(tuple(e['at']))
    ok = np.array([[B.cell_passable(Lr, ts, x, y) for x in range(W)] for y in range(H)])

    def edge_ok(x, y, d):
        bit = 1 << (d // 2 - 1)
        for z in (2, 1, 0):
            t = int(Lr[z, y, x])
            if t == 0:
                continue
            tag = ts['terrain_tags'][t] if t < len(ts['terrain_tags']) else 0
            if tag in (13, 15):
                continue
            if ts['passages'][t] & bit:
                return False
            if ts['priorities'][t] == 0:
                return True
        return True

    sx, sy = start
    assert ok[sy, sx] and (sx, sy) not in solid_ev, f'Map {mid}: start {start} not walkable!'
    seen = {start}
    q = deque([start])
    while q:
        cx, cy = q.popleft()
        for dx, dy, d in ((0, 1, 2), (0, -1, 8), (1, 0, 6), (-1, 0, 4)):
            nx, ny = cx + dx, cy + dy
            if (0 <= nx < W and 0 <= ny < H and (nx, ny) not in seen
                    and ok[ny, nx] and (nx, ny) not in solid_ev
                    and edge_ok(cx, cy, d) and edge_ok(nx, ny, 10 - d)):
                seen.add((nx, ny))
                q.append((nx, ny))

    targets = list(extra_targets)
    for e in m.events:
        et = e.get('type')
        at = tuple(e['at'])
        if et in ('warp', 'door', 'exit'):
            targets.append((e.get('name', et), at, False))
        elif et in ('npc', 'trainer', 'item', 'sign', 'mart'):
            targets.append((e.get('name', et), at, True))
        elif et == 'event':
            pgs = e.get('pages') or []
            if any(p.get('trigger', 'action') in ('action', 'touch') and p.get('commands') for p in pgs):
                allow_adj = not all(p.get('trigger') == 'touch' for p in pgs if p.get('commands'))
                targets.append((e.get('name', 'event'), at, allow_adj))

    missing = []
    for name, (tx, ty), allow_adj in targets:
        if allow_adj:
            reach = ((tx, ty) in seen
                     or any((tx + dx, ty + dy) in seen for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))))
        else:
            reach = (tx, ty) in seen
        if not reach:
            missing.append((name, (tx, ty), bool(ok[ty, tx])))
    assert not missing, f'Map {mid} {head["name"]}: UNREACHABLE: {missing[:10]}'

    # Check walk_check cut-off percentage (matching build.py: MUST stay < 5% for 0 warnings!)
    total_walk = int(ok.sum())
    cutoff = total_walk - len(seen)
    cutoff_pct = 100.0 * cutoff / max(1, total_walk)
    assert cutoff_pct < 4.5, f'Map {mid}: walk_check cutoff too high ({cutoff}/{total_walk} = {cutoff_pct:.1f}%)'

    # Verify 0 void_L0, 0 NB2AUTO, and ALL 6 Outdoor Rubric thresholds!
    assert (Lr[0] > 0).all(), f'Map {mid}: void L0 tiles!'
    for z in range(3):
        for slot in range(1, 8):
            base = slot * 48
            msk = (Lr[z] >= base) & (Lr[z] < base + 48)
            if not msk.any():
                continue
            for yy, xx in np.argwhere(msk):
                assert int(Lr[z, yy, xx]) == base + autotile_shape(msk, xx, yy), \
                    f'Map {mid}: NB2AUTO mismatch L{z} ({xx},{yy})'

    r = B.rubric(Lr)
    need = [('layer2', 55, 1), ('layer3', 20, 1), ('bare', 35, -1), ('bare3x3', 13, -1), ('stacks', 10, 1), ('mirror', 15, -1)]
    fails = [f'{k}={r[k]:.1f}' for k, lim, s in need if (r[k] - lim) * s < 0]
    print(f'  [BFS+RUBRIC] Map {mid} {head["name"]:24s}: {len(seen):4d}/{total_walk:4d} ({cutoff_pct:4.1f}% cut) | '
          + ' '.join(f'{k}={r[k]:.1f}' for k, _, _ in need))
    assert not fails, f'Map {mid} RUBRIC FAIL: {fails}'

    os.makedirs(RAW_DIR, exist_ok=True)
    rel = f'data/raw/{mid:03d}.npy'
    np.save(os.path.join(HERE, rel), Lr)
    spec = dict(head)
    fn = spec.pop('_file', f'{mid:03d}.yaml')
    spec['raw'] = rel
    spec['tileset'] = tid
    body = yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=150, allow_unicode=True)
    body += yaml.safe_dump({'events': m.events}, sort_keys=False, default_flow_style=None, width=150, allow_unicode=True)
    with open(os.path.join(SPEC_DIR, fn), 'w', encoding='utf-8') as f:
        f.write(comment + body)
    print(f'Wrote {mid} {head["name"]:26s} {m.W}x{m.H} ts={tid} events={len(m.events)}')
    return Lr, ok


def _enforce_seam_column(m, x, open_ys, road_cls='d'):
    """Carve exact open seam on column x (plus 3-tile approach buffer) and seal all other rows with solid trees."""
    open_set = set(open_ys)
    dx = 1 if x == 0 else -1
    for y in range(m.H):
        if y in open_set:
            for k in range(5):
                xx = x + k * dx
                if m.inb(xx, y):
                    m.cls[y, xx] = road_cls
                    m.ht[y, xx] = 0
        else:
            for k in range(4):
                xx = x + k * dx
                if m.inb(xx, y) and all((y + dy) not in open_set for dy in (-2, -1, 0, 1, 2)):
                    if m.cls[y, xx] not in ('w', 'W', 'o'):
                        m.cls[y, xx] = 'T'


# ==============================================================================
# MAP 6: 580 The Reedholms (110x90, TS 52 PF Rejuv Snow, WATER_SURFACE, Rain,40)
# ==============================================================================
def build_580():
    W, H = 110, 90
    m = _snowmap(W, H, 580)
    m.cls[:, :] = '.'

    # ---- 1. Organic Delta Woodland Borders (thick varied pine/spruce rims framing the Ebb delta!) ----
    for y in range(H):
        for x in range(W):
            rim_n = 7 + int(4.5 * vnoise(x, y, 5801, 9.0))
            rim_s = 7 + int(5.0 * vnoise(x, y, 5802, 8.5))
            rim_w = 5 + int(4.0 * vnoise(x, y, 5803, 7.5))
            rim_e = 6 + int(4.0 * vnoise(x, y, 5804, 8.0))
            if y < rim_n or y >= H - rim_s or x < rim_w or x >= W - rim_e:
                m.cls[y, x] = 'T'

    # ---- 2. Sculpted Mesh of Ebb Delta Channels & Marsh Holms (Islets) ----
    # Three winding N-S river channels + connecting cross-channels separating 6 organic holms!
    for y in range(10, H - 10):
        c1 = 27 + 4.5 * math.sin(y / 11.0) + 2.0 * math.cos(y / 5.5)
        c2 = 55 + 5.5 * math.cos(y / 12.0) + 2.0 * math.sin(y / 6.0)
        c3 = 82 + 4.0 * math.sin(y / 10.5 + 1.2)
        for cx, half_w in ((c1, 4.8), (c2, 5.2), (c3, 4.6)):
            for x in range(int(cx - half_w - 1), int(cx + half_w + 2)):
                if 10 <= x < W - 10:
                    if abs(x - cx) <= half_w + 1.0 * (vnoise(x, y, 5805, 4.0) - 0.5):
                        m.cls[y, x] = 'w'
    # Winding E-W delta channels splitting North Dam holm, Central holms, Heron Islet, & Sunk Holm!
    for x in range(14, W - 14):
        ry1 = 27 + 3.2 * math.sin(x / 12.0)
        ry2 = 64 + 3.5 * math.cos(x / 13.0)
        for cy, hw in ((ry1, 3.6), (ry2, 3.8)):
            for y in range(int(cy - hw - 1), int(cy + hw + 2)):
                if 12 <= y < H - 12:
                    if abs(y - cy) <= hw + 0.8 * (vnoise(x, y, 5806, 4.0) - 0.5):
                        m.cls[y, x] = 'w'

    # Sculpt key dry holms cleanly over the water mesh:
    holms = [
        (14, 44, 10, 10),   # West Entry Towpath Holm (connects West warp -> 160 Ebbmouth)
        (16, 15, 11, 8),    # NW Dam Holm (Voltaic Sluiceworks door R7_SLUICE!)
        (14, 71, 10, 9),    # SW Bleed Veil Bank (Ebb Hollow warp R7_HOLLOW & Fisher at the Veil!)
        (41, 44, 11, 12),   # Central Smoke-Hut & Eel-Weir Holm (Teo punt / Wanted Poster!)
        (42, 17, 10, 8),    # North-Central Reed Holm (Trainer & reeds)
        (68, 42, 11, 12),   # Heron Islet (Wingull flock & Birdkeeper Sunniva!)
        (69, 73, 10, 8),    # Sunk Holm (South secret islet with hidden Big Pearl & Net Ball!)
        (95, 45, 11, 12),   # East Haul-Road Approach Holm (connects E seam -> 592!)
        (92, 20, 9, 7),     # NE Willow Bluff Holm
        (42, 74, 10, 7),    # South-Central Eel Holm
    ]
    for cx, cy, rx, ry in holms:
        for y in range(max(6, cy - ry - 2), min(H - 6, cy + ry + 3)):
            for x in range(max(4, cx - rx - 2), min(W - 4, cx + rx + 3)):
                q = ((x - cx) / float(rx)) ** 2 + ((y - cy) / float(ry)) ** 2
                if q <= 1.0 + 0.25 * (vnoise(x, y, 5807 + cx, 3.8) - 0.5):
                    m.cls[y, x] = '.'

    # Raised NW Hydro-Dam Bluff (ht=1, y=6..12, x=10..26) — forested top (ZERO cut-off walkable cells!)
    for y in range(6, 13):
        for x in range(10, 26):
            m.ht[y, x] = 1
            m.cls[y, x] = 'T'
    # Raised NE scenic pine ridge (ht=1) + wooded north-central headland (eliminates cut-off islet!)
    for y in range(5, 17):
        for x in range(74, 102):
            if y <= 13 or ((x - 87) / 13.0) ** 2 + ((y - 12) / 5.0) ** 2 <= 1.0:
                if m.cls[y, x] != 'w':
                    m.cls[y, x] = 'T'
                    if y >= 8:
                        m.ht[y, x] = 1
    for y in range(7, 26):
        for x in range(53, 83):
            if m.cls[y, x] != 'w':
                m.cls[y, x] = 'T'

    # ---- 3. Winding Packed-Snow Holm Lanes (clean 'd' approaches -> ZERO dark-purple 'e' stubs past boardwalks!) ----
    m.lane([(0, 44), (14, 44), (22, 44)], c='d', w=2.4, seed=5811)
    m.lane([(33, 44), (41, 44), (49, 44)], c='d', w=2.4, seed=5812)
    m.lane([(61, 44), (68, 44), (77, 44)], c='d', w=2.4, seed=5813)
    m.lane([(87, 45), (96, 45), (109, 45)], c='d', w=2.5, seed=5814)
    # North branch up to NW Voltaic Sluiceworks Dam
    m.lane([(16, 42), (16, 32), (16, 19), (18, 16)], c='d', w=2.1, seed=5815)
    # South branch down to SW Bleed Veil Bank (588 Ebb Hollow) across a genuine SW marsh channel!
    m.lane([(14, 48), (14, 57)], c='d', w=2.1, seed=5816)
    m.lane([(14, 65), (14, 71), (9, 71)], c='d', w=2.1, seed=5821)
    # Ensure a real marsh creek flows under the SW boardwalk (y=58..64, connecting into West Ebb Channel!)
    for yy in range(58, 65):
        for xx in range(11, 25):
            m.cls[yy, xx] = 'w'
            m.ht[yy, xx] = 0
    # Internal loops to North-Central Holm, South-Central Holm & Sunk Holm
    m.lane([(46, 42), (46, 20)], c='d', w=2.0, seed=5817)
    m.lane([(41, 50), (41, 73), (68, 73)], c='d', w=2.0, seed=5818)
    m.lane([(68, 50), (68, 73)], c='d', w=2.0, seed=5819)
    m.lane([(94, 37), (94, 21)], c='d', w=2.0, seed=5820)

    # Clear building footprints & NW Dam courtyard (y>=13 keeps ht=1 cliff cleanly intact at y=12..14!)
    for x0, y0, x1, y1 in (
        (12, 13, 22, 21),   # NW Hydro-Dam portal courtyard
        (36, 36, 45, 43),   # Central Smoke Hut yard
        (64, 36, 73, 43),   # Heron Islet clearing
        (7, 68, 17, 75),    # SW Bleed Veil clearing
        (88, 37, 96, 43),   # East Eel-Weir Hut yard
    ):
        for yy in range(y0, y1 + 1):
            for xx in range(x0, x1 + 1):
                m.cls[yy, xx] = '.'
                m.ht[yy, xx] = 0

    # NW Dam Spillway Waterfall chute pouring off the hydro-dam bluff AND flowing cleanly INTO West Ebb Channel!
    for yy in range(10, 17):
        for xx in (23, 24):
            m.cls[yy, xx] = 'w'
            m.ht[yy, xx] = 1 if yy <= 12 else 0
    for yy in range(15, 18):
        for xx in range(23, 30):
            m.cls[yy, xx] = 'w'
            m.ht[yy, xx] = 0

    # Enforce West entry (y=42..46) & EXACT East Seam (SEAM_580_E = y=42..48)!
    _enforce_seam_column(m, 0, range(42, 47), road_cls='d')
    _enforce_seam_column(m, W - 1, SEAM_580_E, road_cls='d')

    # Organic tall winter reed-grass beds across the holms (for the rich Land encounter table!)
    for y in range(14, H - 14):
        for x in range(8, W - 8):
            if m.cls[y, x] == '.' and m.ht[y, x] == 0:
                if vnoise(x, y, 5825, 5.2) > 0.56:
                    if not (11 <= x <= 24 and 12 <= y <= 22) and not (35 <= x <= 46 and 36 <= y <= 46) and not (7 <= x <= 17 and 68 <= y <= 76):
                        m.cls[y, x] = 'g'

    # Scatter wooded copses inside larger holms so interior foliage reads lush and varied (not bare plains!)
    for cx, cy, rad in ((35, 32, 3.0), (74, 33, 3.6), (92, 56, 4.0), (20, 54, 2.8), (65, 55, 3.0), (47, 62, 3.2), (89, 28, 3.2)):
        for y in range(int(cy - rad - 1), int(cy + rad + 2)):
            for x in range(int(cx - rad - 1), int(cx + rad + 2)):
                if m.inb(x, y) and m.cls[y, x] in ('.', 'g') and m.ht[y, x] == 0:
                    if ((x - cx) / rad) ** 2 + ((y - cy) / rad) ** 2 <= 1.0:
                        m.cls[y, x] = 'T'

    m.plan_cliffs(rows=3)
    _hook_forest(m, REED_WOODS, seed=5800, snow=True)

    # ---- 4. Seamless Wharf Boardwalks, Dam Spillway Waterfall & Bank-Anchored Snow Bridges! ----
    wf_t = RC.vauto('rejuvenation', 'Waterfall (1)', 0)
    for wx in (23, 24):
        for wy in (12, 13, 14):
            m.over.append((2, wx, wy, wf_t))

    # Main E-W Lock Road bridges sized cleanly to actual riverbank widths (bank_w - 1 .. bank_e + 1)!
    _fit_snow_bridge_h(m, 20, 35, 43)      # West Channel Bridge (Ebbmouth -> Smoke Hut Holm)
    _fit_snow_bridge_h(m, 48, 63, 43)      # Central Channel Bridge (Smoke Hut Holm -> Heron Islet; Teo Punt Scene!)
    _fit_snow_bridge_h(m, 75, 89, 44)      # East Channel Bridge (Heron Islet -> Haul Approach Holm)
    # Cohesive 3-wide weathered maritime wharf boardwalks (trimmed cleanly clear of huts & spanning actual water!)
    _wharf_boardwalk(m, 15, 17, 20, 35)    # West -> NW Voltaic Sluiceworks Dam wharf
    _wharf_boardwalk(m, 13, 15, 57, 66)    # West -> SW Bleed Veil wharf (spans the real SW marsh channel!)
    _wharf_boardwalk(m, 45, 47, 21, 36)    # Central -> North-Central Holm wharf (cleanly clear of Smoke Hut!)
    _wharf_boardwalk(m, 40, 42, 52, 68)    # Central -> South-Central Holm wharf
    _wharf_boardwalk(m, 48, 63, 72, 74)    # South-Central -> Sunk Holm wharf!
    _wharf_boardwalk(m, 67, 69, 52, 68)    # Heron Islet -> Sunk Holm wharf!
    _wharf_boardwalk(m, 93, 95, 24, 36)    # East -> NE Bluff wharf (stops cleanly north of East Eel-Weir Hut (90,37)!)

    # ---- 5. Iconic Landmarks: Embedded Industrial Dam Portal, Smoke Huts, Bleed Veil, Eel-Weirs & Heron Islet ----
    # NW Voltaic Sluiceworks Dam Portal: dark industrial tunnel pf_minemouth embedded FLUSH in south cliff y=12..14!
    _place_over_stamp(m, 'pf_minemouth', 17, 12, solid=False)
    for px in (17, 19):
        m.taken[13, px] = True
        m.taken[14, px] = True
    _place_over_stamp(m, 'lm_pylon_off', 13, 13)
    _place_over_stamp(m, 'lm_pylon_off', 21, 13)
    m.stamp('pf_signpost', 15, 18)   # Sluiceworks Dam Sign -> event at (15, 19)!

    # Central Smoke Hut (wb_smoke 7x6 at 37,36 -> door at 40,41) + Wanted Poster board beside it!
    m.stamp('wb_smoke', 37, 36)
    m.stamp('pf_signpost', 44, 41)   # Wanted Poster / Smoke Hut Board -> event at (44, 42)!
    m.stamp('fw_rack', 35, 41)       # Eel-drying rack!
    m.stamp('hb_barrels', 45, 39)
    # East Eel-Weir Hut (wb_hut 5x5 at 90,37) + road sign
    m.stamp('wb_hut', 90, 37)
    m.stamp('pf_signpost', 8, 42)    # Main Reedholms Road Sign -> event at (8, 43)!

    # SW Bleed Veil Shimmer Portal to 588 Ebb Hollow (at [9, 71], shimmering lm_veil curtain!)
    for vy in (70, 71, 72):
        m.over.append((2, 9, vy, P1(f'lm_veil{vy % 3}')))
        m.over.append((2, 10, vy, P1(f'lm_veil{(vy + 1) % 3}')))
    m.stamps.append(('pf_glow', 8, 70))
    m.stamp('cv_xblue2', 8, 69)
    m.stamp('cv_xrose2', 8, 72)

    # Floating river punts placed via _place_over_stamp so they float NATURALLY on water (ZERO rock bathtubs!)
    for nm, x, y in (('hb_boat1', 25, 38), ('hb_boat2', 55, 48), ('hb_boat3', 79, 50), ('hb_boat4', 60, 68)):
        _place_over_stamp(m, nm, x, y)

    # Dry-land riverside props, reeds & warm lamps (Fisher lamp moved to (13,69), Dam approach lamp moved to (20,17)!)
    for nm, x, y in (
        ('hb_fish', 36, 42), ('fw_brazier', 35, 39), ('fw_brazier', 89, 41),
        ('pf_sledge', 96, 41), ('fw_wood', 95, 38),
        ('fw_reeds0', 22, 46), ('fw_reeds1', 23, 47), ('fw_reeds0', 34, 47), ('fw_reeds1', 50, 40),
        ('fw_reeds0', 61, 47), ('fw_reeds1', 74, 42), ('fw_reeds0', 87, 48), ('fw_reeds1', 18, 69),
        ('fw_reeds0', 64, 71), ('fw_reeds1', 72, 71), ('fw_reeds0', 44, 24), ('fw_reeds1', 38, 26),
        ('pf_wlamp', 12, 42), ('pf_wlamp', 38, 42), ('pf_wlamp', 66, 42), ('pf_wlamp', 93, 42),
        ('pf_wlamp', 20, 17), ('pf_wlamp', 13, 69),
    ):
        if m.inb(x, y):
            _place_stamp_safe(m, nm, x, y, on='.degw', mark_solid=(nm not in ('fw_reeds0', 'fw_reeds1')))

    # Scatter scenic snow-spruces, boulders & shrubs on dry holms (strictly EXCLUDING NW Dam courtyard x=10..24, y=11..22!)
    rng = random.Random(5809)
    for _ in range(95):
        rx, ry = rng.randint(6, W - 8), rng.randint(10, H - 10)
        if 10 <= rx <= 25 and 10 <= ry <= 22:
            continue
        if m.cls[ry, rx] == '.' and m.ht[ry, rx] == 0:
            prop = rng.choice((KF_TEAL_PINE_A, KF_TEAL_PINE_B, KF_SHRUB_A, KF_SHRUB_B, KF_BOULDER))
            _put_raw_prop(m, prop, rx, ry, on='.', pad=1)

    # ---- 6. Events (Warps, Canon Ch5 Scenes, Trials Fisher Hook, 5 Canonical PBS Trainers & Pickups) ----
    E = m.events
    # West Edge Warps -> 160 Ebbmouth east quay (58, 36)
    for wy in range(42, 47):
        E.append({'type': 'warp', 'name': 'To Ebbmouth', 'at': [0, wy],
                  'to': {'map': 160, 'x': 58, 'y': 36, 'dir': 'left'}, 'se': 'Door exit'})
    # NW Dam Tunnel Mouth -> 584 Voltaic Sluiceworks (directly on dark pf_minemouth doorway tile [18, 14]!)
    E.append({'type': 'warp', 'name': 'Voltaic Sluiceworks Door', 'at': [18, 14],
              'link': 'R7_SLUICE', 'arrive': [18, 15, 'down'], 'se': 'Door exit'})
    # SW Bleed Veil -> 588 Ebb Hollow
    E.append({'type': 'warp', 'name': 'Bleed Veil to Ebb Hollow', 'at': [9, 71],
              'link': 'R7_HOLLOW', 'arrive': [10, 71, 'right'], 'se': 'Door exit'})

    # Canon Road Sign & Sluiceworks Dam Sign (ALL signposts at (x, y+1) matching solid base 18112!)
    E += [
        _sign((8, 43), 'Reedholms Road Sign',
              "THE REEDHOLMS — The Lock Road. ← Ebbmouth · → the Icecutters' Haul · ↑ the Sluiceworks dam. The boardwalks are re-laid every spring. This spring they weren't."),
        _sign((15, 19), 'Sluiceworks Dam Sign',
              "VOLTAIC SLUICEWORKS — MERIDIAN CONCORD — DECOMMISSIONED AF 291. DANGER: LIVE.\nPainted beside it in bright pink: \"ROOK WAS HERE — EP. 112 'HAUNTED HYDRO' — STAY CHARGED!\""),
        # Eel-weir Keeper (story/24_SCRIPT_CH5.md:23-26)
        _npc((39, 43), 'Eel-weir Keeper', 'NPC 03', [
            "Eel-weir Keeper: Weirs catch eels when the river runs.",
            "Eel-weir Keeper: When it stops, the eels just sit in them and look at you."
        ], d='down', again=[
            "Eel-weir Keeper: Since they blew the intake it's run like a clock.",
            "Eel-weir Keeper: Meridian's still fixing it. I hope they take their time."
        ]),
        # Fisher at the Veil (100% clear of streetlamp!) — WIRED WITH TRIALS QUEST IS_EBB_HOLLOW!
        {'type': 'event', 'name': 'Fisher at the Veil', 'at': [12, 71], 'pages': [
            {'graphic': {'sprite': 'NPC 20', 'dir': 'left'}, 'trigger': 'action', 'commands': [
                {'if': 'defined?(pf_trial_ready?) && pf_trial_ready?(:VEIL_FISHER)', 'then': [
                    {'script': 'pf_trial_talk(:VEIL_FISHER)'}
                ], 'else': [
                    "Fisher at the Veil: Holmsby. The Ebb took it in AF 296.",
                    "Fisher at the Veil: Didn't flood it. Lifted the river clean off its bed and left it hanging.",
                    "Fisher at the Veil: My sister's house is in there. Still dry, I'd bet.",
                    "Fisher at the Veil: You'll go in? Nobody goes in."
                ]}
            ]}
        ]},
    ]
    # Teo on the Channel — UNMISSABLE 3-tile touch strip across ALL 3 central bridge lanes (55, 43..45), shared flag!
    for ty in (43, 44, 45):
        E.append({'type': 'event', 'name': f'Teo on the Channel {ty - 42}', 'at': [55, ty], 'pages': [
            {'trigger': 'touch', 'through': True, 'commands': [
                {'if': '!pfm?(:ch5_teo_reedholms) && (!defined?(pf_choice) || pf_choice(:ch4_teo) != :report)', 'then': [
                    '(A reed-cutter\'s punt slides out of the reeds. The punter has a cutter\'s hat pulled low, and a Carvanha noses along beside the hull.)',
                    '\\pf[TEO,smug]Teo: Don\'t wave. You\'ll make me look like I\'ve got friends.',
                    {'if': 'defined?(pf_choice) && pf_choice(:ch4_teo) == :confront', 'then': [
                        '\\pf[TEO,smug]Teo: Mari says you sat in the kitchen with her. Nobody sits in the kitchen with her when she\'s like that. Not even me. ...Thanks.'
                    ], 'else': [
                        '\\pf[TEO,smug]Teo: You told the Lattice man you didn\'t see my face. You were a foot from my face. I owe you. The Hollow pay their debts. Eventually. In eels.'
                    ]},
                    '\\pf[TEO,sad]Teo: Tell her I\'m eating. Don\'t tell her where.',
                    '(The punt slides quietly back into the reeds.)',
                    {'script': 'pfm_set(:ch5_teo_reedholms)'},
                ], 'else': []},
            ]},
        ]})

    E += [
        # Wanted Poster on Smoke Hut (at (44, 42) matching signpost base!) & Reed-cutter NPC with canon :report branch!
        {'type': 'event', 'name': 'Smoke Hut Board', 'at': [44, 42], 'pages': [
            {'trigger': 'action', 'commands': [
                {'if': 'defined?(pf_choice) && pf_choice(:ch4_teo) == :report', 'then': [
                    'WANTED POSTER: "TEO REYES — WANTED — SABOTAGE OF THE MERIDIAN TIDAL LATTICE." Someone has drawn him a moustache. Under it, smaller: "HE PULLED PELLA OUT."'
                ], 'else': [
                    'A smoke-blackened tally board nailed to the reed hut: "SPRING BOARDWALK REPAIRS — DEFERRED UNTIL THE EBB SETTLES."'
                ]}
            ]}
        ]},
        {'type': 'event', 'name': 'Reed-cutter', 'at': [45, 42], 'pages': [
            {'graphic': {'sprite': 'NPC 24', 'dir': 'left'}, 'trigger': 'action', 'commands': [
                {'if': 'defined?(pf_choice) && pf_choice(:ch4_teo) == :report', 'then': [
                    "Reed-cutter: Those went up on every hut from here to the Haul. They came down again on every hut, too. Wasn't me. Mostly."
                ], 'else': [
                    "Reed-cutter: The Ebb flips twice a day out here when the Lattice isn't choking it. Leave a punt untied at dusk and it drifts clean down to the Sunk Holm."
                ]}
            ]}
        ]},
        # Heron Islet wildlife (Wingull)
        _npc((69, 39), 'Heron Islet Wingull', 'Followers/WINGULL', [
            {'se': 'Cries/WINGULL'},
            'Wingull: Kree! (It guards a nest woven from silver river-reeds.)'
        ], d='down', move='random'),
        # Interactive Reed-Cutter's Punt Ferry (verified existing SE 'Anim/Water1'!)
        _npc((64, 49), 'Punt Poler', 'NPC 10', [
            'Punt Poler: Want a quick pole down the reed channel to the Sunk Holm? Mind your boots!',
            {'choices': ['Pole me south', 'I\'ll walk the boards'], 'cancel': 2, 'branches': [[
                {'se': 'Anim/Water1'},
                {'transfer': {'map': 580, 'x': 68, 'y': 71, 'dir': 'down'}}
            ], []]}
        ], d='down'),
        # ALL 5 Canonical PBS Trainers (# Map 580 The Reedholms: Jorun, Solveig, Tarjei, Aksel, Sunniva!)
        _trainer((19, 39), 'YOUNGSTER', 'Jorun',
                 "Jorun: I cut reeds out here every morning before breakfast — bet my team's just as quick!",
                 "Jorun: I cut reeds faster than I battle. Don't tell my da.", d='down', sight=4, field='WATER_SURFACE'),
        _trainer((42, 22), 'POKEMONBREEDER', 'Solveig',
                 "Solveig: All five of my water starters love the rain on the Reedholms! Come say hello!",
                 "Solveig: Hush, hush. You've set all five of them off.", d='down', sight=2, field='WATER_SURFACE'),
        _trainer((44, 52), 'FISHERMAN', 'Tarjei',
                 "Tarjei: The eels won't bite while the boards are shaking — so you'll have to do!",
                 "Tarjei: The eels just sat there and watched. Same as always.", d='left', sight=4, field='WATER_SURFACE'),
        _trainer((86, 42), 'SAILOR', 'Aksel',
                 "Aksel: Pole's jammed in the silt and my boots are soaked! Let's settle this on the planks!",
                 "Aksel: Punt's stuck, pole's stuck, and now this.", d='down', sight=4, field='WATER_SURFACE'),
        _trainer((70, 45), 'BIRDKEEPER', 'Sunniva',
                 "Sunniva: You startled the birds on Heron Islet! My team's already airborne!",
                 "Sunniva: They've gone back to the heron islet. I don't blame them.", d='up', sight=4, field='WATER_SURFACE'),
        # Pickups (ALL verified valid PBS items!)
        _item((73, 75), 'NETBALL', 'Net Ball'),
        _item((66, 75), 'BIGPEARL', 'Hidden Big Pearl', hidden=True),
        _item((46, 15), 'DAMPROCK', 'Damp Rock'),
        _item((93, 19), 'SUPERPOTION', 'Super Potion'),
        _item((17, 68), 'GREATBALL', 'Great Ball'),
    ]

    m.paint()
    # Industrial riveted steel-grate apron directly in front of the NW Sluiceworks tunnel mouth (16..20, 15..17)!
    gr = P1('lm_grate')
    for yy in (15, 16, 17):
        for xx in range(16, 21):
            if m.cls[yy, xx] in ('.', 'd') and not m.cliff[yy, xx]:
                m.L[0, yy, xx] = gr
                m.L[1, yy, xx] = 0
                m.cls[yy, xx] = 'd'

    head = {
        'id': 580,
        'name': 'The Reedholms',
        'parent': 0,
        'bgm': 'Route 2',
        'field': 'WATER_SURFACE',
        'rubric': True,
        'map_audio': {'bgm': 'Route - Isenmar', 'bgs': 'Wind - Isenmar', 'bgs_volume': 60},
        'connections': [{'dir': 'E', 'offset': 10, 'to': 592, 'to_offset': 0}],
        'metadata': {'Name': 'The Reedholms', 'Outdoor': True, 'ShowArea': True,
                     'MapPosition': [0, 4, 7], 'BattleBack': 'water', 'Weather': ['Rain', 40]},
        'tone': [-10, -6, 8, 22],
        'fog': {'name': 'prismfall_seamist', 'opacity': 44, 'blend': 0, 'zoom': 100, 'sx': 1, 'sy': 0},
        '_file': '580_the_reedholms.yaml',
    }
    return _verify_and_write(
        m, 580, TID52, head,
        '# GENERATED by mapgen/layouts/act1_frontier_routes.py: The Reedholms (110x90, TS 52).\n',
        start=(2, 44),
        extra_targets=[('East seam -> 592', (W - 1, 45), False)],
        snow=True,
    )


# ==============================================================================
# MAP 7: 592 The Icecutters' Haul (110x70, TS 52 PF Rejuv Snow, SNOWY_MOUNTAIN)
# ==============================================================================
def build_592():
    W, H = 110, 70
    m = _snowmap(W, H, 592)
    m.cls[:, :] = '.'

    # ---- 1. Dense Organic Alpine Timber Borders (with Sawyer's Cross N & S Forest Track Corridors!) ----
    for y in range(H):
        for x in range(W):
            rn = 8 + int(4.5 * vnoise(x, y, 5921, 9.0))
            rs = 8 + int(4.5 * vnoise(x, y, 5922, 9.0))
            rw = 5 + int(3.5 * vnoise(x, y, 5923, 7.5))
            re_ = 5 + int(3.5 * vnoise(x, y, 5924, 7.5))
            if y < rn or y >= H - rs or x < rw or x >= W - re_:
                m.cls[y, x] = 'T'

    # Sawyer's Cross N-S forest track corridor ONLY between North Gate (y=15) and South Gate (y=57)!
    for y in range(15, 58):
        for x in range(67, 75):
            m.cls[y, x] = '.'

    # ---- 2. Crisp Axis-Aligned Stepped Limestone Bluffs (shs3, ht=1 -> ZERO shattered elliptical rims!) & Frozen Ponds ----
    # NW Ice-Shelf Bluff (ht=1): crisp axis-aligned stepped plateau (every edge >= 4 tiles wide!)
    for y in range(12, 22):
        for x in range(16, 43):
            m.ht[y, x] = 1
            m.cls[y, x] = '.'
    for y in range(10, 12):
        for x in range(20, 39):
            m.ht[y, x] = 1
            m.cls[y, x] = '.'
    # SW Pine Ridge (ht=1, forested crisp rectangle -> ZERO shattered rim!)
    for y in range(51, 61):
        for x in range(12, 39):
            m.ht[y, x] = 1
            m.cls[y, x] = 'T'
    # NE Glacial Cutting-Quarry Bluff (ht=1, crisp axis-aligned rectangle x=82..100, y=12..20!)
    for y in range(12, 21):
        for x in range(82, 101):
            m.ht[y, x] = 1
            m.cls[y, x] = '.'
    # Frozen Ice-Cutting Ponds (decorative Still water snow basins south & north of haul road)
    for cx, cy, rx, ry, c in ((24, 44, 6.2, 4.0, 'w'), (54, 19, 6.2, 4.0, 'w'), (91, 51, 7.2, 4.5, 'w')):
        for y in range(int(cy - ry - 1), int(cy + ry + 2)):
            for x in range(int(cx - rx - 1), int(cx + rx + 2)):
                if m.inb(x, y) and ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1.0 + 0.22 * (vnoise(x, y, 5926 + cx, 3.0) - 0.5):
                    m.cls[y, x] = c
                    m.ht[y, x] = 0

    # ---- 3. Clean Continuous Packed-Snow Haul Road (ZERO L1 rut punch-holes!) ----
    m.lane([(0, 35), (16, 35), (30, 33), (46, 36), (60, 35), (71, 35), (86, 33), (98, 35), (109, 35)],
           c='d', w=3.1, seed=5927)
    # Dirt sled track up Sawyer's Cross strictly terminating at North Gate (y=16) & South Gate (y=56)!
    m.lane([(71, 16), (71, 35), (71, 56)], c='e', w=2.5, seed=5928)
    # Side spurs to NW Dropped Ice Block ledge, Mudsdale Haul Yard & NE Quarry Overlook
    m.lane([(30, 33), (30, 18), (22, 17)], c='e', w=2.1, seed=5929)
    m.lane([(46, 36), (48, 49), (58, 50)], c='d', w=2.2, seed=5930)
    m.lane([(86, 33), (90, 18)], c='e', w=2.0, seed=5931)

    # Wide snow-stone stairs climbing NW Bluff & NE Bluff cleanly!
    for xx in range(28, 33):
        for yy in range(18, 22):
            m.ht[yy, xx] = 1; m.cls[yy, xx] = 'e'
        for yy in range(22, 26):
            m.ht[yy, xx] = 0; m.cls[yy, xx] = 'e'
    m.stairs(29, 21, w=3, n=3, c='e')

    for xx in range(88, 93):
        for yy in range(17, 21):
            m.ht[yy, xx] = 1; m.cls[yy, xx] = 'e'
        for yy in range(21, 25):
            m.ht[yy, xx] = 0; m.cls[yy, xx] = 'e'
    m.stairs(89, 20, w=3, n=3, c='e')

    # Enforce EXACT West Seam (SEAM_592_W = 32..38) & East Seam (SEAM_592_E = 32..37)!
    _enforce_seam_column(m, 0, SEAM_592_W, road_cls='d')
    _enforce_seam_column(m, W - 1, SEAM_592_E, road_cls='d')

    # Clear pads for Picket Hut, Mudsdale Haul Yard & Dropped Ice Block (NEVER unseal Sawyer's Cross behind gates!)
    for x0, y0, x1, y1 in (
        (36, 26, 48, 33),   # Union Picket Hut yard
        (67, 15, 74, 19),   # North Gate front apron ONLY (y>=15; y<=14 stays sealed!)
        (67, 52, 74, 57),   # South Gate front apron ONLY (y<=57; y>=58 stays sealed!)
        (46, 44, 62, 53),   # Mudsdale Haul Team yard
        (19, 14, 27, 20),   # NW Dropped Ice Block ledge
    ):
        for yy in range(y0, y1 + 1):
            for xx in range(x0, x1 + 1):
                if m.cls[yy, xx] in ('T', 'w'):
                    m.cls[yy, xx] = '.'

    # Strictly seal dense perimeter forest FLUSH against BOTH sides and backs of North Gate (66..75, 8..15) & South Gate (66..75, 55..62)!
    for y in range(0, 15):
        for x in range(62, 80):
            m.cls[y, x] = 'T'
    for y in range(8, 19):
        for x in list(range(62, 67)) + list(range(75, 80)):
            if m.cls[y, x] != 'w':
                m.cls[y, x] = 'T'
    for y in range(58, H):
        for x in range(62, 80):
            m.cls[y, x] = 'T'
    for y in range(54, H):
        for x in list(range(62, 67)) + list(range(75, 80)):
            if m.cls[y, x] != 'w':
                m.cls[y, x] = 'T'

    # Organic snowy tall-grass patches & interior spruce groves
    for y in range(12, H - 12):
        for x in range(8, W - 8):
            if m.cls[y, x] == '.' and vnoise(x, y, 5933, 4.8) > 0.52:
                if not (35 <= x <= 49 and 25 <= y <= 34) and not (65 <= x <= 77):
                    m.cls[y, x] = 'g'
    for cx, cy, rad in ((14, 25, 3.4), (55, 29, 3.2), (82, 45, 3.8), (38, 49, 3.5), (98, 25, 3.4), (58, 57, 3.2)):
        for y in range(int(cy - rad - 1), int(cy + rad + 2)):
            for x in range(int(cx - rad - 1), int(cx + rad + 2)):
                if m.inb(x, y) and m.cls[y, x] in ('.', 'g') and m.ht[y, x] == 0:
                    if ((x - cx) / rad) ** 2 + ((y - cy) / rad) ** 2 <= 1.0:
                        m.cls[y, x] = 'T'

    m.plan_cliffs(rows=3)
    _hook_forest(m, ALPINE_WOODS, seed=5920, snow=True)

    # ---- 4. Landmarks: Union Picket Hut, Truly Sealed N & S Border Gates, Ice Stacks & Mudsdale Yard ----
    # Union Picket Hut (wb_hut 5x5 at 39,26) + barricades, union banner, braziers & timber stacks!
    m.stamp('wb_hut', 39, 26)
    m.stamp('wr_ban_ise', 37, 28)
    m.stamp('fw_brazier', 45, 30)
    m.stamp('pf_barricade', 45, 32)
    m.stamp('pf_barricade', 37, 32)

    # Sawyer's Cross TRULY SEALED Closed Border Gates (matching monumental stone gt_gate4 + solid pf_barricade rows!)
    _place_over_stamp(m, 'gt_gate4', 66, 8)
    _place_over_stamp(m, 'pf_barricade', 69, 15)    # Seals North Gate arch solid (x=69..70, y=15)
    _place_over_stamp(m, 'pf_barricade', 71, 15)    # Seals North Gate arch solid (x=71..72, y=15)
    _place_over_stamp(m, 'gt_gate4', 66, 55)        # Replaces pink wb_gate with matching solid stone border gate!
    _place_over_stamp(m, 'pf_barricade', 69, 57)    # Seals South Gate arch solid (x=69..70, y=57)
    _place_over_stamp(m, 'pf_barricade', 71, 57)    # Seals South Gate arch solid (x=71..72, y=57)
    m.stamp('pf_signpost', 68, 16)   # North Gate sign -> event at (68, 17)!
    m.stamp('pf_signpost', 68, 53)   # South Gate sign -> event at (68, 54)!
    m.stamp('pf_signpost', 74, 33)   # Chalked crossroads post -> event at (74, 34)!
    m.stamp('pf_signpost', 8, 33)    # Haul Road Sign -> event at (8, 34)!
    m.stamp('pf_signpost', 83, 31)   # Contract Seven Poster -> event at (83, 32)!

    # Dropped Ice Block & Tipped Sled on NW Bluff (21,16) + authentic crystal ice & firewood stacks (NO pink cv_saltblocks!)
    m.stamp('pf_sledge', 23, 16)
    _put_raw_prop(m, KF_CRYS_MONO, 25, 15, on='.')
    _put_raw_prop(m, KF_CRYS_MONO, 48, 38, on='.')
    _put_raw_prop(m, KF_CRYS_MONO, 80, 37, on='.')
    _put_raw_prop(m, KF_CRYS_MONO, 95, 30, on='.')
    # Authentic sleds (pf_sledge replacing spiky wr_glasssled!), firewood, braziers & barrels off the lane!
    for nm, x, y in (
        ('pf_sledge', 48, 45), ('pf_sledge', 55, 48), ('fw_sled', 15, 38), ('fw_sled', 94, 38),
        ('fw_wood', 44, 28), ('fw_wood', 59, 47), ('fw_wood', 49, 39), ('fw_brazier', 74, 37), ('fw_brazier', 11, 37),
        ('pf_wlamp', 18, 32), ('pf_wlamp', 52, 32), ('pf_wlamp', 75, 32), ('pf_wlamp', 97, 32),
        ('hb_barrels', 44, 46), ('wr_sacks', 57, 46),
    ):
        _place_stamp_safe(m, nm, x, y, on='.deg')

    # NOTE: ZERO L1 sled-rut overwrite over Packed Snow ('d') -> continuous pristine 110-tile winter haul road!

    # Scatter crystalline ice-stacks, snow-spruces & boulders with pad=1 spacing (ZERO canopy slicing!)
    rng = random.Random(5929)
    for _ in range(95):
        rx, ry = rng.randint(6, W - 8), rng.randint(10, H - 10)
        if 64 <= rx <= 77 and (ry <= 18 or ry >= 52):
            continue
        if m.cls[ry, rx] == '.' and not m.cliff[ry, rx]:
            prop = rng.choice((KF_TEAL_PINE_A, KF_TEAL_PINE_B, KF_SHRUB_A, KF_SHRUB_B, KF_CRYS_MONO, KF_BOULDER))
            _put_raw_prop(m, prop, rx, ry, on='.', pad=1)

    # ---- 5. Events (Canon Picket, Mudsdale Team, Sawyer's Cross, Recruiter, Dropped Ice Block, 3 Canonical PBS Trainers & Pickups) ----
    E = m.events
    E += [
        _sign((8, 34), 'Icecutters Haul Sign',
              "THE ICECUTTERS' HAUL — The Lock Road. ← the Reedholms · → Brassfall & the Icefall Locks. Sled road: give way to ice."),
        # Union Picket Captain Hulda + 2 Strikers (story/24_SCRIPT_CH5.md:77-82)
        _npc((41, 32), 'Picket Captain Hulda', 'NPC 21', [
            "Picket Captain Hulda: Ice-cutters' union.",
            "Picket Captain Hulda: No ice goes up the Locks to Lumen till Ebbmouth's wheel turns on its own.",
            "Picket Captain Hulda: Lumen puts Isenmar ice in its fancy drinks. Lumen can drink them warm for a week."
        ], d='down'),
        _npc((39, 33), 'Union Striker 1', 'NPC 24', [
            "Striker: We're on strike for Ebbmouth. Ebbmouth's not even on strike.",
            "Striker: That's solidarity. Look it up."
        ], d='down'),
        _npc((43, 33), 'Union Striker 2', 'NPC 04', [
            "Striker: Meridian offered us bonus scrip to haul ahead of the Gala. Nobody touched a single sled."
        ], d='left'),
        # Mudsdale Haul-Team & Driver (story/24_SCRIPT_CH5.md:83)
        _npc((53, 49), 'Mudsdale Driver', 'NPC 20', [
            "Mudsdale Driver: The Mudsdale don't strike. They just refuse. It's different."
        ], d='up'),
        _npc((52, 47), 'Haul Mudsdale', 'Followers/MUDSDALE', [
            {'se': 'Cries/MUDSDALE'},
            'Mudsdale stamps a heavy, frost-caked hoof and refuses to budge an inch.'
        ], d='right'),
        _npc((56, 47), 'Haul Mudbray', 'Followers/MUDBRAY', [
            {'se': 'Cries/MUDBRAY'},
            'Mudbray chews a tuft of hay, thoroughly unbothered by Meridian schedules.'
        ], d='left'),
        # Sawyer's Cross Closed Gates & Chalked Crossroads Sign (ALL signposts at (x, y+1)!)
        _sign((68, 17), 'Sawyers Cross North Gate',
              "SAWYER'S CROSS (NORTH GATE): FROSTFANG PASS — CLOSED BY ORDER OF THE THANE."),
        _sign((68, 54), 'Sawyers Cross South Gate',
              "SAWYER'S CROSS (SOUTH GATE): SNOWBRIAR — CLOSED BY ORDER OF THE QUEEN."),
        _sign((74, 34), 'Sawyers Cross Chalk Post',
              "SAWYER'S CROSS — ↑ Frostfang Pass (Closed) · ↓ Snowbriar (Closed).\nChalked boldly between the two arrows: \"THEY AGREE ON ONE THING.\""),
        # Meridian Heat-Contract Recruiter & Poster (story/24_SCRIPT_CH5.md:87)
        _sign((83, 32), 'Contract Seven Poster',
              "MERIDIAN CONCORD — CONTRACT SEVEN: HEAT FOR LIFE! Guaranteed winter warmth for every Isenmar hearth. Sign today — ask your local representative!"),
        _npc((84, 32), 'Meridian Recruiter', 'NPC 14', [
            "Meridian Recruiter: Contract Seven! Heat for life! Ask me about Contract Seven!",
            "Meridian Recruiter: ...Wait, are you with the union? Please don't throw snow at my clipboard again."
        ], d='down'),
        # Dropped Ice Block -> ICE-BOUND SATCHEL (story/24_SCRIPT_CH5.md:88-89; thaw in Brassfall!)
        {'type': 'event', 'name': 'Dropped Ice Block', 'at': [21, 16], 'pages': [
            {'graphic': {'tile': P1('cv_xblue')}, 'trigger': 'action', 'commands': [
                'A block of cut ice that slid off a haul-sled. Something is frozen dead-center inside it: a leather satchel stamped with a Meridian sunburst.',
                {'script': 'pfm_item(:ICEBOUNDSATCHEL, 1, "ICE-BOUND SATCHEL")'},
                'ICE-BOUND SATCHEL: "Frozen solid. You\'d need a boiler to thaw it open."',
                {'selfswitch': ['A', True]},
            ]},
            {'cond': {'self': 'A'}, 'trigger': 'action', 'commands': [
                'Only chipped shavings of blue river-ice remain beside the tipped sled.'
            ]},
        ]},
        # ALL 3 Canonical PBS Trainers (# Map 592 The Icecutters' Haul: Nils, Bodil, Torsten!)
        _trainer((16, 33), 'CAMPER', 'Nils',
                 "Nils: My haul-sled went sideways off the ice-track — care for a battle while I right it?",
                 "Nils: The sled went one way and my team went the other.", d='down', sight=4, field='SNOWY_MOUNTAIN'),
        _trainer((59, 37), 'HIKER', 'Bodil',
                 "Bodil: Picket line's cold work! A proper battle will keep the frost off our mittens!",
                 "Bodil: We're on strike. I wasn't meant to lose on strike.", d='up', sight=4, field='SNOWY_MOUNTAIN'),
        _trainer((92, 33), 'BLACKBELT', 'Torsten',
                 "Torsten: Twelve hours a day sawing river-ice builds iron fists! Show me your stance!",
                 "Torsten: I cut ice all day. You cut me in half the time.", d='down', sight=4, field='SNOWY_MOUNTAIN'),
        # Pickups (ALL verified valid PBS items!)
        _item((91, 16), 'NEVERMELTICE', 'Never-Melt Ice'),
        _item((59, 52), 'ICEHEAL', 'Ice Heal'),
        _item((27, 15), 'GREATBALL', 'Great Ball'),
        _item((74, 53), 'SUPERREPEL', 'Super Repel'),
        _item((83, 49), 'REVIVE', 'Hidden Revive', hidden=True),
    ]

    m.paint()
    head = {
        'id': 592,
        'name': "The Icecutters' Haul",
        'parent': 0,
        'bgm': 'Route 3',
        'field': 'SNOWY_MOUNTAIN',
        'rubric': True,
        'walk_from': [[2, 35]],
        'map_audio': {'bgm': 'Route - Borderlands', 'bgs': 'Wind - Isenmar', 'bgs_volume': 60},
        'connections': [
            {'dir': 'W', 'offset': 0, 'to': 580, 'to_offset': 10},
            {'dir': 'E', 'offset': 16, 'to': 590, 'to_offset': 0},
        ],
        'metadata': {'Name': "The Icecutters' Haul", 'Outdoor': True, 'ShowArea': True,
                     'MapPosition': [0, 6, 7], 'BattleBack': 'snow', 'Weather': ['Snow', 20]},
        'tone': [-6, -2, 10, 12],
        '_file': '592_the_icecutters_haul.yaml',
    }
    return _verify_and_write(
        m, 592, TID52, head,
        "# GENERATED by mapgen/layouts/act1_frontier_routes.py: The Icecutters' Haul (110x70, TS 52).\n",
        start=(2, 35),
        extra_targets=[('West seam <- 580', (0, 35), False), ('East seam -> 590', (W - 1, 35), False)],
        snow=True,
    )


# ==============================================================================
# MAP 8: 590 Brassfall (40x36, TS 52 PF Rejuv Snow, SNOWY_MOUNTAIN, Town)
# ==============================================================================
def build_590():
    W, H = 40, 36
    m = _snowmap(W, H, 590)
    m.cls[:, :] = '.'

    # ---- 1. Alpine Lock-and-Lift Town Climbing the Frozen Falls ----
    # Perimeter snow-spruce woodland borders (leaving W seam y=16..21 & E seam y=16..21 open!)
    for y in range(H):
        for x in range(W):
            if y < 4 or y >= H - 4 or x < 3 or x >= W - 3:
                m.cls[y, x] = 'T'

    # Upper Town Terrace (ht=1, y=4..12, x=4..35) overlooking Lower Lock Square (ht=0, y=13..31)!
    for y in range(4, 13):
        for x in range(4, 36):
            m.ht[y, x] = 1
            m.cls[y, x] = '.' if (5 <= x <= 34 and y >= 6) else 'T'

    # Frozen River Ebb Lock Channel cutting N-S through Brassfall (x=21..25) with waterfall off upper terrace!
    for y in range(4, H - 3):
        for x in range(21, 26):
            m.cls[y, x] = 'w'
    # Upper terrace waterfall cascade at x=22..24, y=12..14
    for y in range(11, 15):
        for x in range(21, 26):
            m.cls[y, x] = 'w'

    # Clear building footprints FIRST (before painting roads -> ZERO fragmented blue-bordered blobs in front of PC!)
    for x0, y0, x1, y1, h in (
        (6, 15, 16, 23, 0),    # Brassfall Pokémon Center yard
        (6, 5, 16, 11, 1),     # Upper Brassfall Union Hall terrace
        (28, 22, 35, 29, 0),   # Meridian Company Store yard
        (27, 6, 35, 12, 1),    # Upper Ice Elevator Base Station terrace
    ):
        for yy in range(y0, y1 + 1):
            for xx in range(x0, x1 + 1):
                if m.inb(xx, yy) and m.cls[yy, xx] != 'w':
                    m.cls[yy, xx] = '.'
                    m.ht[yy, xx] = h

    # Smooth Connected Packed-Snow Town Avenues (W seam -> front of PC -> Lower Lock Square -> Lock Bridge -> E seam!)
    m.lane([(0, 19), (5, 19), (6, 23), (12, 23), (17, 22), (19, 19), (27, 19), (39, 19)], c='d', w=2.5, seed=5901)
    # West Plaza, PC Door Apron & South Sled Yard connecting smoothly into South Footbridge (y=28)!
    m.lane([(11, 22), (11, 28), (20, 28)], c='d', w=2.2, seed=5902)
    m.lane([(27, 28), (32, 28)], c='d', w=2.1, seed=5904)
    # Connections up to West Stairs (14,15) & East Stairs (31,15) and Upper Terraces!
    m.lane([(14, 19), (14, 15)], c='d', w=2.1, seed=5905)
    m.lane([(31, 19), (31, 10)], c='d', w=2.2, seed=5903)
    m.lane([(10, 11), (16, 11)], c='d', w=1.8, seed=5906)
    # West Stone Stairs climbing Lower Lock Square -> Upper Union Hall Terrace (x=13..15, y=12..14)
    for xx in range(12, 17):
        for yy in range(8, 13):
            m.ht[yy, xx] = 1; m.cls[yy, xx] = 'd'
        for yy in range(13, 18):
            m.ht[yy, xx] = 0; m.cls[yy, xx] = 'd'
    m.stairs(13, 12, w=3, n=3, c='d')
    # East Stone Stairs climbing Lower Lock Square -> Upper Ice Elevator Platform (x=30..32, y=12..14)
    for xx in range(29, 34):
        for yy in range(8, 13):
            m.ht[yy, xx] = 1; m.cls[yy, xx] = 'd'
        for yy in range(13, 18):
            m.ht[yy, xx] = 0; m.cls[yy, xx] = 'd'
    m.stairs(30, 12, w=3, n=3, c='d')

    # Re-assert crisp frozen river channel (x=21..25) & exact building base footprints ONLY (leaving street y=22..23 intact!)
    for y in range(4, H - 3):
        for x in range(21, 26):
            m.cls[y, x] = 'w'
    for x0, y0, x1, y1 in ((7, 16, 15, 21), (6, 5, 14, 10), (29, 22, 34, 27)):
        for yy in range(y0, y1 + 1):
            for xx in range(x0, x1 + 1):
                if m.cls[yy, xx] != 'w':
                    m.cls[yy, xx] = '.'

    # Enforce EXACT West Seam (SEAM_590_W = 16..21) & East Seam (SEAM_590_E = 16..21)!
    _enforce_seam_column(m, 0, SEAM_590_W, road_cls='d')
    _enforce_seam_column(m, W - 1, SEAM_590_E, road_cls='d')

    m.plan_cliffs(rows=3)
    _hook_forest(m, ALPINE_WOODS, seed=5900, snow=True)

    # ---- 2. Bridges, Waterfall, Buildings & Zenith-Meets-Isenmar Town Dressing ----
    # Frozen waterfall cascade tumbling off upper terrace (x=22..24, y=12..14)!
    wf_t = RC.vauto('rejuvenation', 'Waterfall (1)', 0)
    for wx in (22, 23, 24):
        for wy in (12, 13, 14):
            m.over.append((2, wx, wy, wf_t))
    # Main Lower Lock Timber Bridge (x=20..26, y=18..20) & South Footbridge (x=20..26, y=27..29)!
    _snow_bridge_h(m, 20, 26, 18)
    _snow_bridge_h(m, 20, 26, 27)

    # Buildings:
    # 1. Brassfall Pokémon Center (wb_pc 9x6 at (7,16) -> door at [11,21] = BRASSFALL_PC_DOOR!)
    m.stamp('wb_pc', 7, 16)
    # 2. Brassfall Union Hall (wb_long 9x6 at (6,5) -> door [10,10]) + steaming Union Boiler & Notice Board!
    m.stamp('wb_long', 6, 5)
    m.stamp('pf_signpost', 16, 9)    # Union Notice Board -> base & event at (16, 10), walkable (16, 11) directly south!
    _place_over_stamp(m, 'lm_gen', 17, 9)  # Brassfall Union Steam Boiler (thaws ICE-BOUND SATCHEL!)
    # 3. Meridian Company Store (wb_short 6x6 at (29,22) -> door [32,27]) + Scrip-Only sign!
    m.stamp('wb_short', 29, 22)
    m.stamp('pf_signpost', 28, 27)   # "MERIDIAN COMPANY STORE — SCRIP ONLY." -> event at (28, 28)!
    # 4. The Ice Elevator Brass Cage (lm_lift 2x3 at (31,7) -> solid action tile at (32,9)!) & Meridian Lattice Pylon!
    _place_over_stamp(m, 'lm_lift', 31, 7)
    _place_over_stamp(m, 'lm_pylon', 27, 6)
    m.stamp('pf_signpost', 30, 9)    # Ice Elevator board -> base & event at (30, 10), walkable (30, 11) directly south!

    # Town welcome sign, Meridian arc-lamps, Isenmar braziers, sleds & timber crates (NO pink saltblocks!)
    m.stamp('pf_signpost', 4, 21)    # Brassfall Town Sign -> event at (4, 22)!
    for nm, x, y in (
        ('lm_arclamp', 20, 15), ('lm_arclamp', 27, 15), ('lm_arclamp', 29, 17), ('lm_arclamp', 17, 25),
        ('fw_brazier', 6, 22), ('fw_brazier', 15, 22), ('fw_brazier', 27, 25),
        ('pf_sledge', 6, 27), ('hb_barrels', 8, 29), ('fw_wood', 14, 29),
        ('hb_barrels', 27, 23), ('wr_sacks', 15, 25), ('fw_ban_i', 6, 10), ('fw_ban_e', 34, 15),
        ('fw_reeds0', 20, 23), ('fw_reeds1', 26, 23),
    ):
        _place_stamp_safe(m, nm, x, y, on='.de')

    # Add alpine spruces/shrubs in outer yards (staying clear of x=16 arrival lane & Ingvild's sightline!)
    rng = random.Random(5908)
    for _ in range(30):
        rx, ry = rng.randint(4, W - 6), rng.randint(5, H - 6)
        if (15 <= rx <= 18 and 14 <= ry <= 26) or (26 <= rx <= 32 and 27 <= ry <= 31):
            continue
        if m.cls[ry, rx] == '.' and not m.cliff[ry, rx]:
            _put_raw_prop(m, rng.choice((KF_TEAL_PINE_A, KF_SHRUB_A, KF_SHRUB_B, KF_CRYS_MONO)), rx, ry, on='.', pad=1)

    # ---- 3. Events (PC Door, On-Screen Arrival Touch Strip, Lockmaster & Gunnhild, Boiler Thaw, Ice Elevator, 2 Canonical PBS Trainers!) ----
    E = m.events
    E += [
        # Bi-directional Pokémon Center Door -> 591 Brassfall Pokémon Center!
        {'type': 'door', 'name': 'Brassfall Pokémon Center Door', 'at': list(BRASSFALL_PC_DOOR),
         'gfx': ['', 0, 2], 'link': 'T590_PC'},
        _sign((4, 22), 'Brassfall Town Sign',
              "BRASSFALL — The Lock-and-Lift Town. Cut ice & smoked eel below; Crownland air above."),
        _sign((10, 10), 'Brassfall Union Hall Door',
              "BRASSFALL UNION HALL — 'Steam boiler running out east on the terrace. Members and travelers welcome.'"),
    ]
    # On-Screen Brassfall Arrival Touch Strip (x=16, y=15..24 — entering Lower Lock Square right beside Garrow & Gunnhild!)
    for ay in range(15, 25):
        E.append({'type': 'event', 'name': f'Brassfall Arrival {ay - 14}', 'at': [16, ay], 'pages': [
            {'trigger': 'touch', 'through': True, 'commands': [
                {'if': '!pfm?(:brassfall_arrival)', 'then': [
                    '(A town built up the face of a frozen waterfall: lock after lock of brass and timber, lift-cages hanging on chains, and everyone\'s breath smoking in the cold.)',
                    'Lockmaster Garrow: The Locks lift the Ebb\'s boats onto the Crownland. Or they would, if the boats were moving.',
                    'Union Steward Gunnhild: The Locks lift what we cut. Ice goes up, scrip comes down. Meridian pays us in scrip, and scrip\'s only good at Meridian\'s store.',
                    'Lockmaster Garrow: It\'s perfectly good money!',
                    'Union Steward Gunnhild: Try buying a pint with it in Ebbmouth.',
                    'Lockmaster Garrow: ...I\'ve never been to Ebbmouth.',
                    'Union Steward Gunnhild: No. You haven\'t.',
                    {'script': 'pfm_set(:brassfall_arrival)'},
                ], 'else': []},
            ]},
        ]})

    E += [
        # Lockmaster Garrow & Union Steward Gunnhild by the lower lock!
        _npc((19, 17), 'Lockmaster Garrow', 'NPC 25', [
            "Lockmaster Garrow: Zenith engineers cut every lock on these falls to the millimeter. If the river stutters, take it up with the Spire — not me."
        ], d='left'),
        _npc((17, 17), 'Union Steward Gunnhild', 'NPC 21', [
            "Union Steward Gunnhild: Scrip's only good at Meridian's store, and the company store doesn't sell boots that last an Isenmar winter.",
            "Union Steward Gunnhild: If you haul anything strange off the sled road, bring it up to our Union Boiler on the upper terrace."
        ], d='right'),
        # Company Store Sign (at (28, 28) matching signpost base!) & Clerk
        _sign((28, 28), 'Company Store Sign', "MERIDIAN COMPANY STORE — SCRIP ONLY."),
        _npc((32, 28), 'Company Store Clerk', 'NPC 14', [
            "Store Clerk: Scrip only. ...You haven't got scrip.",
            "Store Clerk: Nobody who isn't from here has scrip.",
            "Store Clerk: I've sold one Potion this year, to myself."
        ], d='down'),
        # Ice-cutter flavour NPC (story/24_SCRIPT_CH5.md:111-112)
        _npc((14, 24), 'Brassfall Ice-cutter', 'NPC 04', [
            "Ice-cutter: Lumen's getting a gala and we're getting frostbite.",
            "Ice-cutter: That's the Lock Road for you. Everything goes uphill."
        ], d='down'),
        # Brassfall Union Hall Notice Board (at (16, 10) matching signpost base!) & Steam Boiler
        _sign((16, 10), 'Union Notice Board',
              'UNION NOTICE BOARD: "SOLIDARITY WITH THE EBB GUILD." · "SCRIP IS NOT MONEY." · "LOST: one (1) Mudsdale. Answers to Mudsdale."'),
        {'type': 'event', 'name': 'Union Steam Boiler', 'at': [18, 10], 'pages': [
            {'trigger': 'action', 'commands': [
                {'if': 'pfm_has?(:ICEBOUNDSATCHEL) && !pfm_has?(:HEATCONTRACT)', 'then': [
                    'You prop the Ice-Bound Satchel against the roaring brass boiler. Meltwater hisses and drips for a long time until the clasp pops free.',
                    {'script': 'pfm_take(:ICEBOUNDSATCHEL)\npfm_item(:HEATCONTRACT, 1, "HEAT CONTRACT (DRAFT)")'},
                    'HEAT CONTRACT (DRAFT): "MERIDIAN CONCORD — HEAT SUPPLY CONTRACT 7-B (DRAFT). Party B: the Dominion of Ashkaar. Terms identical to Contract 7 (Isenmar)." Penciled in the margin: "Don\'t let the Thane see B."',
                    'Union Steward Gunnhild: (reading over your shoulder) Contract Seven. That\'s ours. That\'s what keeps Rimeholt\'s children warm.',
                    'Union Steward Gunnhild: And this is the same contract. Word for word. For Ashkaar. They\'re selling the same fire to both of them.',
                    'Union Steward Gunnhild: Keep that. Don\'t show it to an Isenmar man with a drink in him. Or an Ashkaar man with a sword. Or anybody, really.',
                ], 'else': [
                    'A massive cast-iron union boiler heating the whole upper terrace. Snow melts three feet back from its firebox.'
                ]}
            ]}
        ]},
        # Optional Sidequest: THE ICE ELEVATOR (solid base at [32, 9] = BRASSFALL_ELEV_POS, board at (30, 10)!)
        _sign((30, 10), 'Ice Elevator Board',
              "BRASSFALL ICE ELEVATOR — OUT OF ORDER SINCE THE STRIKE. Motor requires live spark or Cell Battery."),
        {'type': 'event', 'name': 'The Ice Elevator', 'at': list(BRASSFALL_ELEV_POS), 'pages': [
            {'trigger': 'action', 'commands': [
                {'if': 'pfm?(:brassfall_elevator)', 'then': [
                    'The brass Ice Elevator hums on its rail, cables thawed clean. Ride up to the top of the Icefall Locks?',
                    {'choices': ['Ride to the top', 'Not now'], 'cancel': 2, 'branches': [[
                        {'se': 'Door exit'},
                        {'transfer': {'map': 581, 'x': ICEFALL_ELEV_POS[0], 'y': ICEFALL_ELEV_POS[1] + 1, 'dir': 'down'}}
                    ], []]}
                ], 'else': [
                    'A brass lift-cage frozen solid to its rail.',
                    {'if': '$player.party.any? { |p| p && !p.egg? && p.hasType?(:ELECTRIC) }', 'then': [
                        'Your Electric-type Pokémon could jolt the frozen motor awake!',
                        {'choices': ['Let your Pokémon jolt it', 'Leave it'], 'cancel': 2, 'branches': [[
                            {'se': 'Anim/Thunder1'},
                            {'script': 'pfm_set(:brassfall_elevator)'},
                            'Sparks dance down the brass rail! The cage shakes off its sheath of ice and grinds smoothly to life — the shortcut to the top of the Icefall Locks is open!'
                        ], []]}
                    ], 'else': [
                        {'if': 'pfm_has?(:CELLBATTERY)', 'then': [
                            'You have a Cell Battery in your bag. Slot it into the lift motor?',
                            {'choices': ['Use Cell Battery', 'Keep it'], 'cancel': 2, 'branches': [[
                                {'se': 'Anim/Thunder1'},
                                {'script': 'pfm_take(:CELLBATTERY)\npfm_set(:brassfall_elevator)'},
                                'The Cell Battery clicks home! The cage shudders free of the ice — the shortcut to the top of the Icefall Locks is open!'
                            ], []]}
                        ], 'else': [
                            'The motor is dead cold. An Electric-type Pokémon — or a spare Cell Battery — could jump-start it.'
                        ]}
                    ]}
                ]}
            ]}
        ]},
        {'type': 'event', 'name': 'Lift-boy', 'at': [33, 10], 'pages': [
            {'graphic': {'sprite': 'NPC 09', 'dir': 'left'}, 'trigger': 'action', 'commands': [
                {'if': 'pfm?(:brassfall_elevator)', 'then': [
                    "Lift-boy: It goes all the way to the top of the Locks!",
                    "Lift-boy: Don't tell the union I fixed a Meridian lift. Don't tell Meridian the union let me."
                ], 'else': [
                    "Lift-boy: It runs off a Cell, and Meridian took the Cells back when the union walked out.",
                    "Lift-boy: Give the motor a jolt and it'll go. Anything with a spark in it — or a Cell Battery from the old Sluiceworks."
                ]}
            ]}
        ]},
        # Both Canonical PBS Trainers (# Map 590 Brassfall: ENGINEER Corwin & POKEMONBREEDER Ingvild!)
        _trainer((9, 27), 'ENGINEER', 'Corwin',
                 "Corwin: Brassfall's lift might be frozen, but my portable Cell pack is fully charged! Let's test it!",
                 "Corwin: It ran off a Cell. So did my team, apparently.", d='right', sight=3, field='SNOWY_MOUNTAIN'),
        _trainer((30, 29), 'POKEMONBREEDER', 'Ingvild',
                 "Ingvild: Keep your feet off the frost-slick! My five fire starters keep me warm enough to battle anyone!",
                 "Ingvild: Mind the eggs! ...Oh, you did. Thank you.", d='left', sight=3, field='SNOWY_MOUNTAIN'),
        # Town Pickups (ALL verified valid PBS items!)
        _item((17, 29), 'HYPERPOTION', 'Hyper Potion'),
        _item((35, 29), 'STARPIECE', 'Hidden Star Piece', hidden=True),
    ]

    m.paint()
    head = {
        'id': 590,
        'name': 'Brassfall',
        'parent': 0,
        'bgm': 'Lerucean Town',
        'field': 'SNOWY_MOUNTAIN',
        'rubric': True,
        'map_audio': {'bgm': 'Town - Isenmar', 'bgs': 'Wind - Isenmar', 'bgs_volume': 55},
        'connections': [
            {'dir': 'W', 'offset': 0, 'to': 592, 'to_offset': 16},
            {'dir': 'E', 'offset': 0, 'to': 581, 'to_offset': 84},
        ],
        'metadata': {'Name': 'Brassfall', 'Outdoor': True, 'ShowArea': True,
                     'MapPosition': [0, 7, 7], 'BattleBack': 'snow', 'Weather': ['Snow', 15]},
        'tone': [-4, -2, 8, 8],
        '_file': '590_brassfall.yaml',
    }
    return _verify_and_write(
        m, 590, TID52, head,
        '# GENERATED by mapgen/layouts/act1_frontier_routes.py: Brassfall (40x36, TS 52).\n',
        start=(11, 22),
        extra_targets=[
            ('West seam <- 592', (0, 19), False),
            ('East seam -> 581', (W - 1, 19), False),
            ('PC Door', BRASSFALL_PC_DOOR, False),
            ('Heal Spot', (11, 22), False),
        ],
        snow=True,
    )


# ==============================================================================
# MAP 9: 581 The Icefall Locks (72x120, TS 52 PF Rejuv Snow, SNOWY_MOUNTAIN)
# ==============================================================================
def build_581():
    W, H = 72, 120
    m = _snowmap(W, H, 581)
    m.cls[:, :] = '.'

    # ---- 1. Epic 5-Terrace Frozen Escarpment Climbing 120 Tiles (S -> N, W Brassfall -> E Coppice Ride!) ----
    # Perimeter snow-alpine woods
    for y in range(H):
        for x in range(W):
            if y < 6 or y >= H - 7 or x < 4 or x >= W - 4:
                m.cls[y, x] = 'T'

    # 4 Crisp Flat Stepped Escarpment Terraces (constant y across river x=20..52 -> razor-straight waterfall lips!)
    for y in range(H):
        for x in range(W):
            b1 = 88 if (18 <= x <= 56) else (86 if x < 18 else 89)
            b2 = 59 if (12 <= x <= 54) else (60 if x < 12 else 58)
            b3 = 31 if (16 <= x <= 62) else (30 if x < 16 else 32)
            if y < b3:
                m.ht[y, x] = 3
            elif y < b2:
                m.ht[y, x] = 2
            elif y < b1:
                m.ht[y, x] = 1
            else:
                m.ht[y, x] = 0

    # Great Frozen Waterfall River Ebb cascading straight down all 4 tiers (curving cleanly down center x~31..39)!
    for y in range(8, H - 8):
        cx = 35 + 4.5 * math.sin(y / 17.0)
        for x in range(int(cx - 4), int(cx + 5)):
            if 10 <= x < W - 10:
                m.cls[y, x] = 'w'

    # ---- 2. Switchback Lock Road Climbing W Seam (0, 100..105) -> 4 Tiers -> E Seam (71, 14..19) ----
    # Tier 0 (bottom, y~102): West entry from Brassfall -> cross Lock Bridge 1 -> East Stairs 1 (x=52..54)
    m.lane([(0, 102), (18, 102), (35, 102), (53, 102), (53, 91)], c='d', w=2.5, seed=5811)
    # Tier 1 (y~74): Climb East Stairs 1 -> head West across Lock Bridge 2 -> West Stairs 2 (x=15..17)
    m.lane([(53, 85), (53, 74), (35, 74), (16, 74), (16, 62)], c='d', w=2.5, seed=5812)
    # Tier 2 (y~49): Climb West Stairs 2 -> across Lock Bridge 3 SOUTH of Lattice #4 fence (y=46!) -> sweep east around Lattice -> East Stairs 3 (x=58..60)!
    m.lane([(16, 56), (16, 49), (35, 49), (54, 49), (62, 49), (62, 36), (59, 34)], c='d', w=2.5, seed=5813)
    # Tier 3 (top, y~17): Climb East Stairs 3 -> Ice Elevator Top Station (14,17) & Top Border Post -> E Seam (71, 14..19)!
    m.lane([(59, 28), (59, 17), (35, 17), (15, 17)], c='d', w=2.5, seed=5814)
    m.lane([(59, 17), (71, 17)], c='d', w=2.6, seed=5815)
    # Side snow spur on Tier 2 up to the recessed Third-Lock Ice Cave embedded in Tier 3 cliff face (21..23, 30..32)!
    m.lane([(22, 49), (22, 35)], c='d', w=2.0, seed=5817)

    # Guarantee flat straight cliff faces & exact 3-row stone staircases at ALL 3 switchback climbs!
    stair_specs = [
        (52, 87, 1, 0),   # Tier 0 -> Tier 1 (East climb, y=87..89)
        (15, 58, 2, 1),   # Tier 1 -> Tier 2 (West climb, y=58..60)
        (58, 30, 3, 2),   # Tier 2 -> Tier 3 (East climb, y=30..32 — cleanly east of Lattice #4!)
    ]
    for sx, sy, hi, lo in stair_specs:
        for xx in range(sx - 2, sx + 5):
            for yy in range(sy - 3, sy + 1):
                m.ht[yy, xx] = hi
                m.cls[yy, xx] = 'd'
            for yy in range(sy + 1, sy + 5):
                m.ht[yy, xx] = lo
                m.cls[yy, xx] = 'd'
        m.stairs(sx, sy, w=3, n=3, c='d')

    # Enforce EXACT West Seam (SEAM_581_W = 100..105 at ht=0) & East Seam (SEAM_581_E = 14..19 at ht=3)!
    _enforce_seam_column(m, 0, SEAM_581_W, road_cls='d')
    for y in range(H):
        if y in SEAM_581_E:
            for xx in range(W - 5, W):
                m.cls[y, xx] = 'd'
                m.ht[y, xx] = 3
        else:
            for xx in range(W - 4, W):
                if all((y + dy) not in SEAM_581_E for dy in (-2, -1, 0, 1, 2)) and m.cls[y, xx] != 'w':
                    m.cls[y, xx] = 'T'

    # Clear pads for Lattice #4 Terrace, Recessed Ice Cave Apron, Top Ice Elevator & Top Border Post
    for x0, y0, x1, y1, h in (
        (45, 40, 64, 53, 2),   # Extraction Lattice No. 4 fenced terrace (Lattice y=42..45, fence y=46, road y=49..50!)
        (19, 33, 27, 38, 2),   # Recessed Third-Lock Ice Cave apron cleanly south of Tier 3 cliff y=30..32!
        (10, 13, 20, 22, 3),   # Ice Elevator Top Station
        (58, 12, 68, 22, 3),   # Top-of-the-Falls Border Post
    ):
        for yy in range(y0, y1 + 1):
            for xx in range(x0, x1 + 1):
                if m.cls[yy, xx] in ('T', 'w'):
                    m.cls[yy, xx] = '.'
                m.ht[yy, xx] = h

    # Lush tall winter grass beds & alpine tree copses on every terrace!
    for y in range(12, H - 12):
        for x in range(8, W - 8):
            if m.cls[y, x] == '.' and vnoise(x, y, 5819, 4.6) > 0.50:
                if not (45 <= x <= 64 and 40 <= y <= 53) and not (58 <= x <= 68 and 12 <= y <= 22) and not (18 <= x <= 28 and 32 <= y <= 38):
                    m.cls[y, x] = 'g'
    for cx, cy, rad in ((14, 96, 3.6), (60, 96, 3.4), (24, 80, 3.2), (61, 70, 3.6), (11, 39, 3.0), (45, 24, 2.8), (16, 108, 3.5), (56, 107, 3.5)):
        for y in range(int(cy - rad - 1), int(cy + rad + 2)):
            for x in range(int(cx - rad - 1), int(cx + rad + 2)):
                if m.inb(x, y) and m.cls[y, x] in ('.', 'g'):
                    if ((x - cx) / rad) ** 2 + ((y - cy) / rad) ** 2 <= 1.0:
                        m.cls[y, x] = 'T'

    m.plan_cliffs(rows=3)
    _hook_forest(m, ALPINE_WOODS, seed=5810, snow=True)

    # ---- 3. Clean Horizontal Waterfall Cascades, Bank-Anchored Bridges, Lattice #4, Recessed Ice Cave, Elevator & Border Post ----
    wf_t = RC.vauto('rejuvenation', 'Waterfall (1)', 0)
    for y in range(10, H - 10):
        for x in range(25, 45):
            if m.cls[y, x] == 'w' and m.cliff[y, x]:
                m.over.append((2, x, y, wf_t))

    # 4 Bank-Anchored Snow-Dusted Lock Bridges sized strictly to (river_xmin - 1 .. river_xmax + 1)!
    _fit_snow_bridge_h(m, 26, 45, 101)  # Tier 0 Lock Bridge 1
    _fit_snow_bridge_h(m, 26, 45, 73)   # Tier 1 Lock Bridge 2
    _fit_snow_bridge_h(m, 26, 45, 48)   # Tier 2 Lock Bridge 3 (aligns cleanly with y=49 road south of Lattice #4!)
    _fit_snow_bridge_h(m, 26, 45, 16)   # Tier 3 Top Lock Bridge 4

    # EXTRACTION LATTICE NO. 4 (fenced north of the road: Lattice y=42..45, brass railing y=46, steel apron y=47..48, road y=49..50!)
    _place_over_stamp(m, 'lm_core', 53, 42)
    _place_over_stamp(m, 'lm_pylon', 50, 42)
    _place_over_stamp(m, 'lm_pylon', 57, 42)
    # Clean horizontal brass safety railing along y=46 ENCLOSING Lattice #4 north of the walkway!
    for fx in range(50, 60):
        if fx == 54:
            continue
        t = 'lm_railing_w' if fx == 50 else ('lm_railing_e' if fx == 59 else 'lm_railing_m')
        m.over.append((1, fx, 46, P1(t)))
        m.taken[46, fx] = True
    m.stamp('pf_signpost', 54, 45)  # Lattice No. 4 Builder's Plate -> solid base & event at (54, 46) in fence gap!
    # The Thaw Ring right at the river edge beneath Lattice #4 (x=45, y=46, glowing melting ice!)
    m.stamps.append(('pf_glow', 44, 45))
    m.over.append((1, 45, 46, P1('cv_xsea')))
    m.taken[46, 45] = True

    # THE ICE ELEVATOR TOP STATION (NW crest, lm_lift at (13,15) -> solid action tile at (14,17)!)
    _place_over_stamp(m, 'lm_lift', 13, 15)
    _place_over_stamp(m, 'lm_pylon', 10, 14)
    m.stamp('pf_signpost', 16, 17)  # Top Station indicator board -> event at (16, 18)!

    # SECRET RECESSED ICE CAVE behind the Third Lock Gate: embedded FLUSH into the Tier 2->3 cliff face at (21..23, 30..32)!
    _place_over_stamp(m, 'pf_minemouth', 21, 30, solid=False)
    for px in (21, 23):
        m.taken[31, px] = True
        m.taken[32, px] = True
    m.stamp('pf_signpost', 24, 32)  # Maintenance Ledger on a nail -> event at (24, 33)!

    # TOP-OF-THE-FALLS BORDER POST (banners moved up to y=13 so Elowen Forester at (60,15) stands 100% clear!)
    _place_over_stamp(m, 'gt_tower', 61, 9)
    _place_over_stamp(m, 'gt_tower', 61, 19)
    m.stamp('fw_ban_i', 60, 13)
    m.stamp('fw_ban_e', 64, 13)
    m.stamp('pf_signpost', 8, 100)  # Icefall Locks Road Sign -> event at (8, 101)!

    # Meridian pylons, arc-lamps & alpine props lining every switchback (NO pink saltblocks!)
    for nm, x, y in (
        ('lm_pylon', 22, 98), ('lm_pylon', 46, 98), ('lm_pylon', 22, 69), ('lm_pylon', 46, 69),
        ('lm_pylon', 22, 41), ('lm_pylon', 46, 12),
        ('lm_arclamp', 12, 99), ('lm_arclamp', 49, 99), ('lm_arclamp', 49, 71), ('lm_arclamp', 19, 71),
        ('lm_arclamp', 20, 46), ('lm_arclamp', 50, 14), ('lm_arclamp', 25, 14),
        ('fw_brazier', 58, 15), ('fw_brazier', 12, 104), ('pf_sledge', 18, 105), ('fw_wood', 58, 78),
    ):
        _place_stamp_safe(m, nm, x, y, on='.de')

    rng = random.Random(5818)
    for _ in range(110):
        rx, ry = rng.randint(6, W - 8), rng.randint(10, H - 10)
        if (45 <= rx <= 65 and 37 <= ry <= 54) or (18 <= rx <= 28 and 31 <= ry <= 38) or (46 <= rx <= 58 and 14 <= ry <= 22):
            continue
        if m.cls[ry, rx] == '.' and not m.cliff[ry, rx]:
            prop = rng.choice((KF_TEAL_PINE_A, KF_TEAL_PINE_B, KF_SHRUB_A, KF_SHRUB_B, KF_CRYS_MONO, KF_CRYS_STAR, KF_BOULDER))
            _put_raw_prop(m, prop, rx, ry, on='.', pad=1)

    # ---- 4. Events (Road Sign, Lattice #4, Tolly, Thaw Ring, Elevator Top, Ice Cave Ledger, Border Post, 4 Canonical PBS Trainers & Items!) ----
    E = m.events
    E += [
        _sign((8, 101), 'Icefall Locks Sign',
              "THE ICEFALL LOCKS — The Lock Road. ↓ Brassfall · ↑ Coppice Ride & the Crownland. Isenmar ends at the top. So does the ice."),
        # Extraction Lattice No. 4 (plate at (54, 46) on fence gap; Tolly at (52, 48) facing UP toward the Lattice!)
        _sign((54, 46), 'Lattice No. 4 Plate',
              "MERIDIAN CONCORD — EXTRACTION LATTICE No. 4 (ICEFALL). COMMISSIONED AF 289. DESIGN: I. LARCH, CHIEF ENGINEER. LIGHT FOR EVERYONE."),
        _npc((52, 48), 'Linesman Tolly', 'NPC 25', [
            "Linesman Tolly: Number Four. Eleven like her in the realm, and she was the second one built.",
            "Linesman Tolly: The Professor's own drawing. Larch. Before she went soft.",
            "Linesman Tolly: Know her? ...Course you do. Everybody who comes up this road with that look on them knows her."
        ], d='up', again=[
            "Linesman Tolly: They say she cried at the switch-on.",
            "Linesman Tolly: Happy tears, I always thought. I'm less sure now."
        ]),
        _sign((45, 46), 'The Thaw Ring',
              "Everywhere else on the Locks the falls are frozen solid. Here, in a ring round the Lattice, the ice is clear as glass, and behind it the water is running. It's melting from the inside."),
        # Secret Recessed Third-Lock Ice Cave Maintenance Ledger (signpost base at (24, 33)!)
        _sign((24, 33), 'Maintenance Ledger',
              "A maintenance ledger hanging on an iron nail by the ice-cave mouth:\n\"Lumen grid. Zap feed diverted to Spire vault for 'anniversary load test'. Draw x3 nominal, sustained. Cradle temperature: HIGH. Recommend inspection. — Inspection deferred. P.Q., R&D.\"\nNext line, a different pen: \"Deferred again. P.Q.\"\nNext: \"Deferred. P.Q. (Don't ask.)\""),
        # Ice Elevator Top Station (board at (16, 18); action event directly on solid cage base (14, 17)!)
        _sign((16, 18), 'Top Station Board',
              "ICE ELEVATOR — UPPER LOCK TERMINAL. Direct descent to Brassfall lower square."),
        {'type': 'event', 'name': 'Ice Elevator Top Station', 'at': list(ICEFALL_ELEV_POS), 'pages': [
            {'trigger': 'action', 'commands': [
                {'if': 'pfm?(:brassfall_elevator)', 'then': [
                    'The brass Ice Elevator is waiting on its upper stop. Ride down to Brassfall?',
                    {'choices': ['Ride down to Brassfall', 'Stay up here'], 'cancel': 2, 'branches': [[
                        {'se': 'Door exit'},
                        {'transfer': {'map': 590, 'x': BRASSFALL_ELEV_POS[0], 'y': BRASSFALL_ELEV_POS[1] + 1, 'dir': 'down'}}
                    ], []]}
                ], 'else': [
                    'The upper cage housing stands empty. Its drive cable leads down to Brassfall — the lift motor at the foot of the falls is still frozen.'
                ]}
            ]}
        ]},
        # Top-of-the-Falls Border Post (Forester 100% clear of banner at (60, 15)!)
        _npc((60, 15), 'Elowen Forester', 'NPC 21', [
            "Elowen Forester: Crown Road country from here. Elowen soil, the Accord's road."
        ], d='down'),
        _npc((64, 19), 'Meridian Guard', 'trainer_SCIENTIST', [
            "Meridian Guard: And Meridian's pylons. Welcome to all three."
        ], d='up'),
        # ALL 4 Canonical PBS Trainers (# Map 581 The Icefall Locks: Brede, Hartley, Alwin, COOLTRAINER_F Ylva!)
        _trainer((20, 100), 'SAILOR', 'Brede',
                 "Brede: Four lock stairs and icy spray the whole way up — prove you've got your sea legs!",
                 "Brede: Every lock on this stair and you still got past me.", d='down', sight=4, field='SNOWY_MOUNTAIN'),
        _trainer((22, 51), 'ENGINEER', 'Hartley',
                 "Hartley: Hear Lattice Number Four humming through your soles? Electric moves love this terrace!",
                 "Hartley: Lattice hums. I hum. You didn't even slow down.", d='up', sight=4, field='SNOWY_MOUNTAIN'),
        _trainer((50, 19), 'COOLTRAINER_F', 'Ylva',
                 "Ylva: Four frozen tiers and a howling wind — show me if your team can still fight at the top of Isenmar!",
                 "Ylva: Isenmar ends at the top. So did my streak.", d='up', sight=3, field='SNOWY_MOUNTAIN'),
        _trainer((55, 19), 'POKEMONRANGER_M', 'Alwin',
                 "Alwin: One last test before you step off Isenmar ice onto Crownland grass!",
                 "Alwin: Elowen soil from here up. You've earned the walk.", d='up', sight=3, field='SNOWY_MOUNTAIN'),
        # Pickups (ALL verified valid PBS items; Magnet & Icy Rock cleanly in recessed Ice Cave alcove!)
        _item((11, 108), 'SUPERREPEL', 'Super Repel'),
        _item((20, 34), 'MAGNET', 'Hidden Magnet', hidden=True),
        _item((25, 34), 'ICYROCK', 'Icy Rock'),
        _item((59, 80), 'ULTRABALL', 'Ultra Ball'),
        _item((13, 64), 'REVIVE', 'Revive'),
    ]

    m.paint()
    # Industrial riveted steel-grate inspection apron directly south of Lattice #4's y=46 fence (y=47..48)!
    gr = P1('lm_grate')
    for yy in (47, 48):
        for xx in range(50, 60):
            if m.cls[yy, xx] in ('.', 'd') and not m.cliff[yy, xx]:
                m.L[0, yy, xx] = gr
                m.L[1, yy, xx] = 0
                m.cls[yy, xx] = 'd'

    head = {
        'id': 581,
        'name': 'The Icefall Locks',
        'parent': 0,
        'bgm': 'Route 3',
        'field': 'SNOWY_MOUNTAIN',
        'rubric': True,
        'walk_from': [[2, 102]],
        'map_audio': {'bgm': 'Route - Borderlands', 'bgs': 'Wind - Isenmar', 'bgs_volume': 65},
        'connections': [
            {'dir': 'W', 'offset': 84, 'to': 590, 'to_offset': 0},
            {'dir': 'E', 'offset': 0, 'to': 595, 'to_offset': 20},
        ],
        'metadata': {'Name': 'The Icefall Locks', 'Outdoor': True, 'ShowArea': True,
                     'MapPosition': [0, 8, 7], 'BattleBack': 'snow', 'Weather': ['Snow', 25]},
        'tone': [-8, -2, 12, 14],
        '_file': '581_the_icefall_locks.yaml',
    }
    return _verify_and_write(
        m, 581, TID52, head,
        '# GENERATED by mapgen/layouts/act1_frontier_routes.py: The Icefall Locks (72x120, TS 52).\n',
        start=(2, 102),
        extra_targets=[
            ('West seam <- 590', (0, 102), False),
            ('East seam -> 595', (W - 1, 17), False),
            ('Ice Elevator Top', ICEFALL_ELEV_POS, True),
        ],
        snow=True,
    )


# ==============================================================================
# MAP 10: 595 Coppice Ride (110x72, TS 60 PF Rejuv Lumen, field MEADOW)
# ==============================================================================
def build_595():
    W, H = 110, 72
    m = City(W, H, 595, base='.')
    m.auto = {
        'w': ('Still water', 'rejuvenation'),
        'W': ('Sea deep', 'rejuvenation'),
        'd': ('Gravel Spring', 'pf'),
        'u': ('DirtDark', 'rejuvenation'),
    }
    m.JOIN = dict(K.RMap.JOIN, w='wW', W='wW', d='d', u='u')
    m.AUTO_Z = dict(K.RMap.AUTO_Z, w=0, W=1, d=1, u=1)
    # Exact 594 Wallshadow Row Crownwall kit: ht=1 warm earthen terrace (sh3), ht=2 & ht=3 sheer gleaming white chalk (shc)!
    m.kit = {1: 'sh3', 2: 'shc', 3: 'shc', 'default': 'shc'}
    m.STAIRS = tuple(P1('st_stair_' + k) for k in 'lmr')
    m.grass = K.SH_GRASS
    m.tall = K.SH_TALL
    m.cls[:, :] = '.'

    # ---- 1. MONUMENTAL DOUBLE-TIERED WHITE CROWNWALL (Exact 594 Wallshadow Row shc Architecture!) ----
    # Bold 14-24 tile wide architectural stepped facets — ZERO choppy 1-tile sine-wave scraps!
    wall_h2 = [
        (0, 18, 10), (18, 36, 11), (36, 54, 10),
        (54, 78, 9),   # Framed lower vista directly behind the Ride-Side Shrine Terrace!
        (78, 94, 11), (94, 110, 10),
    ]
    for x0, x1, ybot in wall_h2:
        for y in range(0, ybot):
            for x in range(x0, x1):
                m.ht[y, x] = 2

    wall_h3 = [
        (0, 22, 5), (22, 46, 6), (46, 74, 5), (74, 96, 6), (96, 110, 5),
    ]
    for x0, x1, ybot in wall_h3:
        for y in range(0, ybot):
            for x in range(x0, x1):
                m.ht[y, x] = 3

    # High-rim evergreen alpine crown on ht=3 (staying cleanly clear of the sheer ht=3 white cliff lip -> ZERO clutter & <3% cutoff!)
    for x in range(W):
        for y in range(0, 5):
            if m.ht[y, x] == 3 and y + 1 < H and m.ht[y + 1, x] == 3:
                m.cls[y, x] = 'T'

    # Outer West, East & South Elowen woodland borders
    for y in range(11, H):
        for x in range(W):
            if y >= H - 7 or x < 5 or x >= W - 5:
                m.cls[y, x] = 'T'

    # Crisp Axis-Aligned Rectangular Ride-Side Shrine Terrace (ht=1, sh3, x=58..76, y=15..22 — ZERO shattered elliptical edges!)
    for y in range(15, 23):
        for x in range(58, 77):
            m.ht[y, x] = 1
            m.cls[y, x] = '.'

    # ---- 2. The River Ebb Emerging Cleanly From Base of White Crownwall (y=13, waterfall chute y=10..12!) ----
    for y in range(13, H - 6):
        cx = 29 + 4.0 * math.sin(y / 11.0) + 1.5 * math.cos(y / 5.5)
        for x in range(int(cx - 4), int(cx + 5)):
            if 12 <= x < W - 12:
                m.cls[y, x] = 'w'
                m.ht[y, x] = 0
    # Crisp spring pool right at the base of the white Crownwall (x=27..31, y=11..15) so waterfall splashes cleanly into River Ebb!
    for y in range(11, 16):
        for x in range(27, 32):
            m.cls[y, x] = 'w'
            if y >= 13:
                m.ht[y, x] = 0

    # ---- 3. Seven Numbered Hazel Coppice Panels in Seven Ages + Winding Main Ride ----
    m.lane([(0, 36), (14, 36), (22, 36)], c='d', w=2.7, seed=5952)
    m.lane([(20, 36), (21, 26), (24, 26)], c='d', w=2.5, seed=5953)   # West approach to Woodwards' Footbridge!
    m.lane([(35, 26), (38, 26), (40, 36)], c='d', w=2.5, seed=5951)   # East return from Woodwards' Footbridge!
    m.lane([(35, 36), (52, 36), (67, 37), (84, 35), (98, 36), (109, 36)], c='d', w=2.7, seed=5954)
    # Branch North up to Ride-Side Shrine Terrace (67, 18) for "The First View of the Crownwall"!
    m.lane([(67, 36), (67, 25), (67, 19)], c='u', w=2.2, seed=5955)
    # Branch South to Woodward's Hut & Charcoal Clamp (47, 52) and Secret Uncut Panel (87, 56)!
    m.lane([(50, 36), (48, 52), (62, 54), (78, 55), (87, 56)], c='u', w=2.2, seed=5956)
    # Organic curved woodland tracks into all 7 numbered hazel coppice panels
    m.lane([(16, 36), (14, 44), (17, 52)], c='u', w=2.2, seed=5957)
    m.lane([(47, 35), (44, 26), (47, 18)], c='u', w=2.2, seed=5958)
    m.lane([(85, 35), (83, 27), (87, 19)], c='u', w=2.2, seed=5959)

    # Re-assert crisp river channel under Woodwards' Footbridge (x=26..34, y=24..27) with solid dry mainland banks!
    for y in range(24, 28):
        for x in range(26, 35):
            m.cls[y, x] = 'w'
            m.ht[y, x] = 0
        for x in (23, 24, 25, 35, 36, 37, 38):
            m.cls[y, x] = 'd' if y in (25, 26) else '.'
            m.ht[y, x] = 0

    # Clean 3-wide stone stairs climbing up to the Rectangular Shrine Terrace (x=66..68, y=22..24 -> top landing y=21!)
    for xx in range(65, 70):
        for yy in range(19, 23):
            m.ht[yy, xx] = 1; m.cls[yy, xx] = 'u'
        for yy in range(23, 27):
            m.ht[yy, xx] = 0; m.cls[yy, xx] = 'u'
    m.stairs(66, 22, w=3, n=3, c='u')

    # Enforce EXACT West Seam (SEAM_595_W = 34..39) & East Exit to 594 Wallshadow Row (y=34..38; (108,36) wide open!)
    _enforce_seam_column(m, 0, SEAM_595_W, road_cls='d')
    _enforce_seam_column(m, W - 1, range(34, 39), road_cls='d')

    # Sculpt the 7 Coppice Panels in 7 Ages (progressing from freshly cut stumps W -> tall dense woods E!)
    panel_woods = [
        (42, 16, 5.2, 3.4),   # Panel III mid-coppice grove (cleanly south of Crownwall!)
        (81, 17, 5.6, 3.6),   # Panel VI dense hazel wood
        (96, 22, 6.0, 4.4),   # Panel VII tallest coppice stand
        (64, 46, 5.4, 4.0),   # Panel V hazel stand
        (96, 50, 5.6, 4.8),   # East boundary of Uncut Panel
        (74, 61, 5.4, 3.8),   # South-east coppice bank
        (14, 18, 5.4, 3.8),   # West riverbank alder wood
        (11, 58, 5.4, 4.2),   # SW coppice rim
        (37, 57, 4.8, 3.6),   # South riverbank coppice stand
        (56, 61, 4.8, 3.6),   # South-central hazel wood
        (95, 43, 4.4, 3.2),   # East Panel VII border stand
    ]
    for cx, cy, rx, ry in panel_woods:
        for y in range(int(cy - ry - 1), int(cy + ry + 2)):
            for x in range(int(cx - rx - 1), int(cx + rx + 2)):
                if m.inb(x, y) and m.cls[y, x] == '.' and m.ht[y, x] == 0:
                    if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1.0:
                        m.cls[y, x] = 'T'

    # Clear key pads: Woodward's Hut, Shrine Terrace, Kingsferry landings, Uncut Panel glade
    for x0, y0, x1, y1 in (
        (41, 45, 55, 56),   # Woodward's Hut & Charcoal Clamp
        (59, 16, 75, 21),   # Ride-Side Shrine Terrace walkable deck
        (19, 33, 25, 40),   # Kingsferry West Landing
        (33, 33, 40, 40),   # Kingsferry East Landing
        (80, 51, 93, 61),   # Uncut Panel secret glade!
    ):
        for yy in range(y0, y1 + 1):
            for xx in range(x0, x1 + 1):
                if m.cls[yy, xx] in ('T', 'w'):
                    m.cls[yy, xx] = '.'

    # Rich tall-grass meadows across all 7 coppice panels (strictly below Crownwall y>=14!)
    for y in range(14, H - 10):
        for x in range(8, W - 8):
            if m.cls[y, x] == '.' and m.ht[y, x] == 0 and vnoise(x, y, 5960, 4.5) > 0.48:
                if not (41 <= x <= 55 and 45 <= y <= 56) and not (80 <= x <= 93 and 51 <= y <= 61):
                    m.cls[y, x] = 'g'

    m.plan_cliffs(rows=3)
    _hook_forest(m, COPPICE_WOODS, seed=5950, blossom_rate=0.06, snow=False)

    # ---- 4. Crownwall Watch-Buttresses, Chalk Boulders & River Ebb Spring Waterfall! ----
    # Dramatic stone Crownwall watch-buttresses & sparse white chalk boulders matching 594 Wallshadow Row (NO busy rock stripes!)
    for bx, by in ((11, 1), (41, 2), (83, 2), (101, 1)):
        _place_over_stamp(m, 'gt_tower', bx, by)
    # Cascading River Ebb spring emerging from the foot of the sheer white Crownwall (x=28..30, y=10..12)!
    wf_mid = RC.vauto('rejuvenation', 'Waterfall', 0)
    wf_bot = RC.vauto('rejuvenation', 'Waterfall bottom', 0)
    for wx in (28, 29, 30):
        m.over.append((2, wx, 10, wf_mid))
        m.over.append((2, wx, 11, wf_mid))
        m.over.append((2, wx, 12, wf_bot))
    # Graceful white chalk boulders hugging the River Ebb spring & clean sunlit Crownwall shelves (matching 594!)
    for bx, by in (
        (26, 12), (31, 12), (5, 7), (18, 7), (35, 7), (49, 7), (61, 6), (72, 6), (89, 8), (97, 7), (105, 7),
    ):
        _place_over_stamp(m, 'ck_boulder', bx, by)
    # Sparse stately evergreen alpine pines tucked cleanly on wide Crownwall shelves (staying clear of white cliff lips!)
    for px, py in ((3, 6), (15, 6), (32, 6), (46, 6), (56, 5), (76, 6), (92, 6), (103, 5)):
        _place_over_stamp(m, 'nt_pine_sh', px, py)

    # ---- 5. Landmarks: Kingsferry Punt, Woodward's Hut & Smouldering Clamp, Crownwall Shrine & Uncut Panel ----
    m.over.append((1, 24, 36, P1('bw_h')))
    m.over.append((1, 34, 36, P1('bw_h')))
    _place_over_stamp(m, 'hb_boat2', 27, 36)

    # Woodward's Hut (sh_cot 8x7 at 42,45) + Smouldering Charcoal Clamp (sh_campfire + glowing brazier/embers!)
    m.stamp('sh_cot', 42, 45)
    m.stamp('sh_campfire', 50, 50)
    _place_over_stamp(m, 'fw_brazier', 52, 50)   # Glowing smouldering core inside Charcoal Clamp!
    m.over.append((2, 51, 51, P1('wr_ember0')))
    m.over.append((2, 53, 51, P1('wr_ember1')))
    m.stamp('pf_wagon', 43, 54)
    m.stamp('pf_hayrick', 52, 46)

    # Ride-Side Shrine (pf_shrine 2x3 at 66,15 -> sign at (67,17)) on Rectangular Terrace overlooking Crownwall!
    m.stamp('pf_shrine', 66, 15)
    m.stamp('pf_stonebench', 61, 18)
    m.stamp('pf_stonebench', 71, 18)

    # The Uncut Panel (AF 0): 4 ancient giant stools encircling glowing OPEN Miracle Seed at (87,56) (NO covering stonering!)
    m.stamps.append(('pf_glow', 86, 55))
    for nm, x, y in (
        ('nt_stump_big', 82, 51), ('nt_stump_big', 89, 51), ('nt_stump_big', 81, 56), ('nt_stump_big', 90, 56),
    ):
        _place_stamp_safe(m, nm, x, y, on='.g')

    # Numbered Hazel Coppice Panel Posts (events at y+1!) + Real Wood Stumps, Logs, Stacks & Saplings (NO nt_stump gravestones, NO nt_reed0/1!)
    m.stamp('pf_signpost', 7, 34)    # Coppice Ride Road Sign -> event at (7, 35)
    m.stamp('pf_signpost', 14, 42)   # Panel I Post -> event at (14, 43)
    m.stamp('pf_signpost', 54, 34)   # Panel IV Post -> event at (54, 35)
    m.stamp('pf_signpost', 83, 33)   # Panel VII Post -> event at (83, 34)
    for nm, x, y in (
        # Authentic cut timber piles, logs, benches & young hazel saplings in Panel I (ZERO gravestones!)
        ('fw_wood', 12, 45), ('pf_logbench', 17, 47), ('nt_log', 13, 50), ('nt_log', 18, 43), ('nt_log', 11, 49),
        ('nt_sapling', 15, 44), ('nt_sapling', 20, 48), ('nt_sapling', 44, 24), ('nt_sapling', 49, 26),
        ('nt_azalea0', 55, 29), ('nt_azalea1', 59, 31), ('nt_azalea2', 74, 39),
        ('nt_shrub0', 60, 41), ('nt_shrub1', 79, 43),
        # Wat's log moved cleanly off the lane from (53,53) -> (52,55) so Wat has a clear 4-tile sightline!
        ('nt_log', 52, 55),
        # East lantern moved cleanly north of road (102,34) -> (102,32) (post on 102,33)!
        ('pf_lantern', 22, 34), ('pf_lantern', 36, 34), ('pf_lantern', 65, 34), ('pf_lantern', 102, 32),
        # Natural riverbank shrubs replacing glitchy cyan-box nt_reed0/1!
        ('nt_shrub0', 25, 31), ('nt_shrub1', 25, 39), ('nt_shrub0', 34, 31), ('nt_shrub1', 34, 41),
    ):
        _place_stamp_safe(m, nm, x, y, on='.dug')

    # Scatter varied Elowen fringe trees & bushes strictly below the Crownwall (y >= 15, ZERO tr_teal!)
    rng = random.Random(5959)
    fringe_trees = ['nt_round_sh', 'nt_pine_sh', 'tr_oak', 'tr_oak2', 'nt_dark_sh', 'nt_olive', 'nt_lime', 'nt_blossom']
    for _ in range(135):
        rx, ry = rng.randint(7, W - 9), rng.randint(15, H - 10)
        if (21 <= rx <= 39 and 22 <= ry <= 29) or (56 <= rx <= 78 and 13 <= ry <= 26) or (79 <= rx <= 94 and 50 <= ry <= 62):
            continue
        if m.cls[ry, rx] == '.' and m.ht[ry, rx] == 0:
            _place_stamp_safe(m, rng.choice(fringe_trees), rx, ry, on='.')

    # ---- 6. Events (East Warps -> 594, 3-Tile Crownwall Trigger, Kingsferry Anim/Water1, Woodward, 5 Canonical PBS Trainers & Miracle Seed!) ----
    E = m.events
    for wy in range(34, 39):
        E.append({'type': 'warp', 'name': 'To Wallshadow Row', 'at': [W - 1, wy],
                  'to': {'map': 594, 'x': 1, 'y': 41, 'dir': 'right'}, 'se': 'Door exit'})

    E += [
        # ALL 4 signposts shifted cleanly to (x, y+1) matching solid base tile 18112!
        _sign((7, 35), 'Coppice Ride Sign',
              "COPPICE RIDE — The Crownlands (Elowen). ← the Icefall Locks · → Wallshadow Row & the Crown Road. Cut every seventh year since the Accord."),
        _sign((14, 43), 'Coppice Panel I Post',
              "PANEL I (YEAR 1): Fresh hazel stools and cut faggots. Next cut: AF 307."),
        _sign((54, 35), 'Coppice Panel IV Post',
              "PANEL IV (YEAR 4): Shoulder-high hazel. Mind the Combee hives."),
        _sign((83, 34), 'Coppice Panel VII Post',
              "PANEL VII (YEAR 7): Tallest hazel canopy — ready for the woodward's billhook next winter."),
        _sign((67, 17), 'Crownwall Offering Shrine',
              "A ride-side stone shrine with an offering bowl holding eighteen coloured pebbles — and one clear pebble in the middle."),
    ]
    # UNMISSABLE 3-tile Touch Strip at the top of the Shrine Stairs ((66..68, 21), shared flag pfm?(:ch5_crownwall_view))!
    for cx in (66, 67, 68):
        E.append({'type': 'event', 'name': f'First View of the Crownwall {cx - 65}', 'at': [cx, 21], 'pages': [
            {'trigger': 'touch', 'through': True, 'commands': [
                {'if': '!pfm?(:ch5_crownwall_view)', 'then': [
                    '(The ride climbs out of the hazel coppice onto a bare shoulder of down. A stone shrine stands at the edge with eighteen coloured pebbles and one clear one.)',
                    {'raw': [203, [8, 9, 2]]}, {'wait': 42},  # slow dramatic scroll north onto the towering double-tiered white Crownwall!
                    '(On the north horizon a ring of white peaks stands up out of the green Crownland, sheer as a wall, enormous, snow on its rim. Inside the ring, very small and very far away, the glint of towers.)',
                    'Pilgrim: The Crownwall. Crownhaven\'s inside it.',
                    'Pilgrim: Every road in Velmora goes round it and none of them go in. Not without eighteen badges, or a Sovereign\'s seal.',
                    '(Something under your ribs aches. Not a pain. Like a bell somebody struck a long way off, and you\'re only hearing it now.)',
                    {'wait': 40},
                    {'choices': ['(Read Mum\'s letter.)', '(Look at the wall.)'], 'cancel': 2, 'branches': [
                        ['"...Don\'t let anyone scan you. Don\'t go to Crownhaven. I\'m sorry I never told you why..."\n(You read the line twice. You fold the letter away.)'],
                        ['(You look at it for a long time. It doesn\'t look back. You\'re nearly sure.)'],
                    ]},
                    'Pilgrim: Ten years ago there was a light in there you could see from here. Festival night. Then it went out and the stories started. You look like you\'ve heard them.',
                    {'raw': [203, [2, 9, 3]]}, {'wait': 20},
                    {'script': 'pfm_set(:ch5_crownwall_view)'},
                ], 'else': []},
            ]},
        ]})

    E += [
        _npc((64, 18), 'Crownwall Pilgrim', 'NPC 23', [
            "Pilgrim: Eighteen coloured pebbles for the eighteen types, and one clear stone for the centre. Nobody remembers who started leaving the clear one."
        ], d='up'),
        # Kingsferry Ferryman & Punt Hand (verified existing SE 'Anim/Water1'!)
        _npc((23, 35), 'Kingsferry Ferryman', 'NPC 10', [
            "Kingsferry Ferryman: Kingsferry. A copper a crossing. Nobody's paid me in a copper since the Accord, but I still say it.",
            {'choices': ['Cross east by punt', 'I\'ll take the footbridge'], 'cancel': 2, 'branches': [[
                {'se': 'Anim/Water1'},
                {'transfer': {'map': 595, 'x': 35, 'y': 36, 'dir': 'right'}}
            ], []]}
        ], d='right'),
        _npc((35, 35), 'Kingsferry Punt Hand', 'NPC 04', [
            "Punt Hand: Heading back west toward the Icefall Locks? Hop aboard and we'll pole you over the Ebb!",
            {'choices': ['Cross west by punt', 'Stay east'], 'cancel': 2, 'branches': [[
                {'se': 'Anim/Water1'},
                {'transfer': {'map': 595, 'x': 23, 'y': 36, 'dir': 'left'}}
            ], []]}
        ], d='left'),
        # Woodward by the Charcoal Clamp (story/24_SCRIPT_CH5.md:185-187)
        _npc((48, 52), 'Coppice Woodward', 'NPC 20', [
            "Woodward: Seven panels, seven ages. You cut one a year, and by the time you're back round to the first it's grown again.",
            "Woodward: That's coppice. It's the only kind of forever I trust."
        ], d='down'),
        # ALL 5 Canonical PBS Trainers (# Map 595 Coppice Ride: GENTLEMAN Osric, Hazel, Wat, Perkin, Tansy!)
        _trainer((18, 34), 'GENTLEMAN', 'Osric',
                 "Osric: Kingsferry takes a copper a crossing — and a gentleman's wager takes a proper battle!",
                 "Osric: A copper a crossing, and worth every one.", d='down', sight=4, field='MEADOW'),
        _trainer((48, 34), 'POKEMONRANGER_F', 'Hazel',
                 "Hazel: Seven coppice panels, seven ages — and my five grass partners grew up right alongside them!",
                 "Hazel: Seven panels, seven ages. These five are the youngest.", d='down', sight=4, field='MEADOW'),
        _trainer((55, 53), 'CAMPER', 'Wat',
                 "Wat: Tending a charcoal clamp teaches patience — and fiery focus! Battle me!",
                 "Wat: Clamp's meant to smoulder, not blaze. Same goes for me.", d='left', sight=4, field='MEADOW'),
        _trainer((84, 23), 'BUGCATCHER', 'Perkin',
                 "Perkin: Wait till you see what's hiding in the seven-year tall hazel! Let's battle!",
                 "Perkin: The tall panel has the good ones. I got these.", d='down', sight=4, field='MEADOW'),
        _trainer((98, 34), 'PICNICKER', 'Tansy',
                 "Tansy: Just past this bend is Wallshadow Row and the Four Ways inn — battle me for the last mile!",
                 "Tansy: I'd offer you hazelnuts but they've eaten them.", d='down', sight=4, field='MEADOW'),
        # Secret Uncut Panel Miracle Seed (100% uncovered & visible!) + Route Pickups (ALL verified valid PBS items!)
        _item((87, 56), 'MIRACLESEED', 'Miracle Seed'),
        _item((17, 52), 'GREATBALL', 'Great Ball'),
        _item((47, 18), 'ENERGYROOT', 'Energy Root'),
        _item((88, 19), 'SUPERPOTION', 'Super Potion'),
        _item((72, 57), 'TINYMUSHROOM', 'Hidden Tiny Mushroom', hidden=True),
    ]

    m.paint()
    # Cleanly remove stray left-column fence tiles (42, 45..47) left by sh_cot!
    for cy in (45, 46, 47):
        m.L[1, cy, 42] = 0

    # Gorgeous 594-style warm-timber plank footbridge (N_f0/N_f1 + lm_railing + lm_bollard abutments!)
    _paint_elowen_bridge_h(m, 26, 34, 25)
    head = {
        'id': 595,
        'name': 'Coppice Ride',
        'parent': 0,
        'bgm': 'Route 2',
        'field': 'MEADOW',
        'rubric': True,
        'map_audio': {'bgm': 'Route - Elowen', 'bgs': 'Gossamer Deepwood', 'bgs_volume': 45},
        'connections': [{'dir': 'W', 'offset': 20, 'to': 581, 'to_offset': 0}],
        'metadata': {'Name': 'Coppice Ride', 'Outdoor': True, 'ShowArea': True,
                     'MapPosition': [0, 10, 8], 'BattleBack': 'field'},
        'tone': [2, 4, -2, 0],
        '_file': '595_coppice_ride.yaml',
    }
    return _verify_and_write(
        m, 595, TID60, head,
        '# GENERATED by mapgen/layouts/act1_frontier_routes.py: Coppice Ride (110x72, TS 60).\n',
        start=(108, 36),
        extra_targets=[
            ('West seam <- 581', (0, 36), False),
            ('Arrival from 594', (108, 36), False),
            ('Uncut Panel Miracle Seed', (87, 56), True),
        ],
        snow=False,
    )


def verify_internal_seams(built_ok):
    """Tile-by-tile seam parity check across all 4 internal Lock Road connections!"""
    seams = [
        (580, 'E', 10, 592, 0),
        (592, 'E', 16, 590, 0),
        (590, 'E', 0, 581, 84),
        (581, 'E', 0, 595, 20),
    ]
    for a, d, oa, b_, ob in seams:
        oka = built_ok[a]
        okb = built_ok[b_]
        ha, wa = oka.shape
        hb, wb = okb.shape
        opened = 0
        mismatches = []
        for y1 in range(ha):
            y2 = y1 - oa + ob
            inb = 0 <= y2 < hb
            pa = bool(oka[y1, wa - 1])
            pb = bool(okb[y2, 0]) if inb else False
            if pa and pb:
                opened += 1
            elif pa != pb and (pa or inb):
                mismatches.append((y1, pa, y2, pb))
        assert opened > 0 and not mismatches, f'SEAM {a} E <-> {b_} W FAILED: opened={opened} mismatches={mismatches[:5]}'
        print(f'  [SEAM-OK] {a} E <-> {b_} W: {opened} matched walkable crossing tiles, 0 mismatches!')


def main():
    built_ok = {}
    for mid, fn in ((580, build_580), (592, build_592), (590, build_590), (581, build_581), (595, build_595)):
        _, ok = fn()
        built_ok[mid] = ok
    verify_internal_seams(built_ok)


if __name__ == '__main__':
    main()
