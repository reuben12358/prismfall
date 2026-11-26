#!/usr/bin/env python3
"""Wave 13 Rejuvenation V14 Map Craft — ALL 9 Remaining Outdoor Routes & Passes:
  167 Ebbmouth - Mill Quay  (40x30,  ts 52 PF Rejuv Snow)  — tidal mills & union quay (connects S -> 160)
  552 The Dyers' Ford       (80x72,  ts 53 PF Rejuv Wild)  — S-curve dye river valley (connects N -> 540, S -> 541)
  560 Frostflat Causeway    (64x30,  ts 52 PF Rejuv Snow)  — arctic causeway & brine flats (connects N -> 570, E -> 140)
  561 Gullcry Cliffs        (64x130, ts 52 PF Rejuv Snow)  — coastal crags & landslide (connects N -> 160, S -> 562)
  566 Spinners' Rise        (80x120, ts 53 PF Rejuv Wild)  — terraced highland switchbacks (connects S -> 120, N -> 577)
  568 The Rehearsal         (34x26,  ts 56 PF Rejuv Shore) — twilight Bleed Veil replay stage (D8)
  577 Frostwick Pass        (72x96,  ts 52 PF Rejuv Snow)  — wind-gap alpine pass (connects S -> 566, W -> 570)
  578 Rimewood Path         (80x88,  ts 52 PF Rejuv Snow)  — Long Ice & Unblazed woods (connects S -> 570, N -> 562)
  579 The Wolfsrime         (80x88,  ts 52 PF Rejuv Snow)  — haunted deep-winter drove road (warps N->562, S->577)

Guarantees:
  - 100% immutable HEAD EvID_exact event, warp, NPC, trainer, sign, item, gate & metadata parity.
  - 100% 4-edge border-connection seam parity verified against live Wave 10/11/12 neighbor maps.
  - 0 build.py --strict warnings, 9/9 byte-identical verify.py roundtrip, 0 passguard hits, 0 BFS softlocks.

Run:
  PRISMFALL_GFX=/home/antigravity/pf_engine_run/game/Graphics /usr/bin/python3 -I mapgen/layouts/wave13_routes_craft.py [mids...]
"""
import base64
import copy
import json
import math
import os
import random
import sys
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
import passguard as PG
import rimewood as RW
from routekit import Route
from terrain import vnoise

# =============================================================================
# 1. IMMUTABLE HEAD SPEC SNAPSHOT (100% EXACT EvID/COORDINATE/METADATA PARITY)
# =============================================================================
HEAD_SPECS_B64 = "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"
_HEAD_CACHE = None

SPEC_FILES = {
    167: '167_ebbmouth_mill_quay.yaml',
    552: '552_dyers_ford.yaml',
    560: '560_route5.yaml',
    561: '561_route6.yaml',
    566: '566_spinners_rise.yaml',
    568: '568_the_rehearsal.yaml',
    577: '577_frostwick_pass.yaml',
    578: '578_rimewood_path.yaml',
    579: '579_wolfsrime.yaml',
}


def head_spec(mid):
    global _HEAD_CACHE
    if _HEAD_CACHE is None:
        raw = zlib.decompress(base64.b64decode(HEAD_SPECS_B64)).decode('utf-8')
        _HEAD_CACHE = json.loads(raw)
    return copy.deepcopy(_HEAD_CACHE[str(mid)])


# =============================================================================
# 2. REJUVENATION V14 SPRITE & PALETTE REGISTRY (PIXEL-VERIFIED ON PF Rejuv.png)
# =============================================================================
# Register Kristiline 3x4 snow-laden alpine spruces into CK.SPECIES
CK.SPECIES['kspA'] = ([[9944, 9945, 9946], [9952, 9953, 9954]], [[9960, 9961, 9962], [9968, 9969, 9970]], 1)
CK.SPECIES['kspB'] = ([[9947, 9948, 9949], [9955, 9956, 9957]], [[9963, 9964, 9965], [9971, 9972, 9973]], 1)
CK.SPECIES['kspC'] = ([[9976, 9977, 9978], [9984, 9985, 9986]], [[9992, 9993, 9994], [10000, 10001, 10002]], 1)
CK.SPECIES['kspD'] = ([[9979, 9980, 9981], [9987, 9988, 9989]], [[9995, 9996, 9997], [10003, 10004, 10005]], 1)

# Rich winter alpine evergreen lattice palettes (Kristiline spruces + deep teal/blue frosted oaks)
ALPINE_WOODS = [
    {'kspA': 5, 'kspB': 4, 'snowteal': 3, 'snow0': 2},
    {'kspC': 4, 'kspD': 4, 'snowteal2': 3, 'snowblue': 2},
    {'kspA': 4, 'kspC': 3, 'snowblue': 3, 'snow1': 2},
    {'kspB': 4, 'kspD': 4, 'snow0': 3, 'snowteal': 2},
]

# Deep haunted winter spruce woods (Wolfsrime / Rimewood Path upper ridges)
DARK_WINTER_WOODS = [
    {'kspC': 5, 'kspD': 4, 'snowteal2': 4, 'snowblue': 3},
    {'kspA': 4, 'kspC': 4, 'snowteal': 4, 'snowblue': 2},
    {'kspB': 3, 'kspD': 5, 'snowteal2': 3, 'snow0': 2},
    {'kspA': 4, 'kspB': 3, 'snowblue': 4, 'snow1': 2},
]

# Lush emerald/blossom Elowen river valley woods (552 Dyers' Ford)
VALLEY_WOODS = [
    {'sh1': 4, 'teal2': 3, 'olive': 2, 'blossom': 1},
    {'sh0': 3, 'teal': 3, 'olive': 3, 'lime': 1},
    {'teal': 3, 'teal2': 3, 'sh1': 3, 'blossom': 1},
    {'olive': 3, 'sh1': 3, 'teal2': 2, 'sh0': 2},
]

# Highland switchback woods (566 Spinners' Rise: emerald valley -> alpine pine)
HIGHLAND_LOW_WOODS = [
    {'sh1': 4, 'teal2': 3, 'olive': 3, 'blossom': 1},
    {'sh0': 3, 'teal': 3, 'olive': 2, 'lime': 1},
    {'teal': 3, 'sh1': 3, 'olive': 3, 'blossom': 1},
]
HIGHLAND_MID_WOODS = [
    {'teal2': 4, 'sh1': 4, 'teal': 3},
    {'sh1': 4, 'teal2': 4, 'olive': 2},
]
HIGHLAND_TOP_WOODS = [
    {'teal2': 5, 'sh1': 4, 'snowteal': 2},
    {'sh1': 4, 'teal2': 4, 'snowblue': 1},
]

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

PETAL_TILE = 5723
ROSE_TILE = 5642
GLOW_MUSH = [451, 452, 453, 454, 459, 460, 461, 462]
LOTUS_TILES = [4836, 4837, 4844, 4845]
ICES = [STAMPS['fw_ice%d' % v]['layers'][1][0][0] for v in range(4)]

# 3-row crisp frosted snow cliff kit (lip / face / base — zero bloated 4-row grey slab!)
if 'shs3' not in K.KITS:
    K.KITS['shs3'] = dict(K.KITS['shs'], rows=[K.KITS['shs']['rows'][0], K.KITS['shs']['rows'][1], K.KITS['shs']['rows'][3]])


# =============================================================================
# 3. SHARED REJUVENATION V14 CRAFT HELPERS
# =============================================================================
def colmap(W_or_r, fn):
    W = W_or_r.W if hasattr(W_or_r, 'W') else int(W_or_r)
    return [int(round(fn(x))) for x in range(W)]


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
    m.SEAL = 10371
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


def smooth_bool_mask(mask, ok_mask, passes=2):
    mm = mask.copy()
    for _ in range(passes):
        pad = np.pad(mm, 1, constant_values=False)
        n4 = pad[:-2, 1:-1].astype(int) + pad[2:, 1:-1] + pad[1:-1, :-2] + pad[1:-1, 2:]
        mm = (mm & (n4 >= 2)) | (~mm & ok_mask & (n4 >= 3))
    return mm


def reserve_events(m, events, road_mask=None, radius=1, extra=(), skip_names=()):
    """Lock exact HEAD event cells & clear approach surroundings so zero props/trees block any event."""
    ev_mask = np.zeros((m.H, m.W), bool)
    pts = [tuple(e['at']) for e in events if e.get('at') and e.get('name', '') not in skip_names] + list(extra)
    for ex, ey in pts:
        if not m.inb(ex, ey):
            continue
        m.taken[ey, ex] = True
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                xx, yy = ex + dx, ey + dy
                if m.inb(xx, yy):
                    ev_mask[yy, xx] = True
                    if road_mask is not None and m.cls[yy, xx] in '.dtgeS':
                        road_mask[yy, xx] = True
    return ev_mask


def paint_signposts(m, events, skip_names=('Border Stones',)):
    """Stamp wooden signpost tile 4847 onto L1 for every `type: sign` with `post: false`."""
    for e in events:
        if e.get('type') == 'sign' and not e.get('post', False) and e.get('name') not in skip_names:
            x, y = e['at']
            if m.inb(x, y):
                m.tile(4847, x, y, 1)


def put_safe(m, name, x, y, on='.dt', r=2, prot=None, check_cliff=True, mark='B'):
    """Safe stamp placement near (x, y) respecting cliffs, prot mask, and height uniformity."""
    st = STAMPS[name]
    sw, sh = st['w'], st['h']
    for d in range(r + 1):
        for dy in range(-d, d + 1):
            for dx in range(-d, d + 1):
                if max(abs(dx), abs(dy)) != d:
                    continue
                X, Y = x + dx, y + dy
                if not m.free(X, Y, sw, sh, on=on):
                    continue
                if check_cliff and m.cliff[max(0, Y - 1):min(m.H, Y + sh + 1), X:X + sw].any():
                    continue
                if prot is not None and prot[Y:Y + sh, X:X + sw].any():
                    continue
                h0 = m.ht[Y, X]
                if not (m.ht[Y:Y + sh, X:X + sw] == h0).all():
                    continue
                m.stamp(name, X, Y, mark=mark)
                return (X, Y)
    return None


def put_sprite(m, x0, y0, top_rows, bot_rows, on='.t', avoid_mask=None, force=False, post_paint=False):
    """Place a verified multi-tile raw sprite (top on L2 pri=5, bot on L1 pas=15)."""
    h_top, h_bot = len(top_rows), len(bot_rows)
    w = len(bot_rows[0])
    if x0 < 0 or y0 < 0 or x0 + w > m.W or y0 + h_top + h_bot > m.H:
        return False
    if not force:
        h_ref = m.ht[y0 + h_top, x0]
        for dy in range(h_bot):
            for dx in range(w):
                t = bot_rows[dy][dx]
                if not t:
                    continue
                xx, yy = x0 + dx, y0 + h_top + dy
                if m.taken[yy, xx] or m.cliff[yy, xx] or m.cls[yy, xx] not in on:
                    return False
                if m.ht[yy, xx] != h_ref:
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


def place_snow_grove(m, cx, cy, count=4, radius=2.6, on='.t', seed=0, hero=False, prot=None):
    """Organic multi-species Kristiline conifer cluster (zero lone sticker trees!)."""
    rng = random.Random(m.seed * 41 + seed)
    placed = 0
    if hero:
        st = STAMPS['pf_g_tree2_ice']
        hx, hy = int(round(cx)) - st['w'] // 2, int(round(cy)) - st['h'] + 2
        if put_safe(m, 'pf_g_tree2_ice', hx, hy, on=on, r=1, prot=prot):
            placed += 1
    kf_kinds = [KF_SPRUCE_A, KF_SPRUCE_B, KF_TEAL_PINE_A, KF_TEAL_PINE_B]
    cands = []
    for _ in range(count * 14):
        ang = rng.uniform(0, 2 * math.pi)
        dist = rng.uniform(0.5, radius)
        tx = int(round(cx + math.cos(ang) * dist)) - 1
        ty = int(round(cy + math.sin(ang) * dist * 0.8)) - 3
        cands.append((ty, tx, rng.random()))
    for ty, tx, rv in sorted(cands):
        if placed >= count + (1 if hero else 0):
            break
        if rv < 0.78:
            top_r, bot_r = rng.choice(kf_kinds)
            if put_sprite(m, tx, ty, top_r, bot_r, on=on, avoid_mask=prot):
                placed += 1
        else:
            if put_safe(m, 'kf_tree', tx, ty, on=on, r=0, prot=prot):
                placed += 1
    return placed


def put_overlay_stamp(m, name, x, y, z=2):
    """Paint a transparent overhead atmospheric stamp (cv_shaft, pf_glow, fw_smoke_w) onto L2."""
    st = STAMPS[name]
    L = np.array(st['layers'])
    for dy in range(st['h']):
        for dx in range(st['w']):
            t = int(L[:, dy, dx].max())
            xx, yy = x + dx, y + dy
            if t and m.inb(xx, yy) and m.L[z, yy, xx] == 0:
                m.L[z, yy, xx] = t


def add_warm_glows(m, pts):
    """Add warm overhead `pf_glow` (2x2, pri=5, pas=0) halos centered on (x, y) lamps/beacons/braziers."""
    st = STAMPS['pf_glow']['layers'][2]
    for cx, cy in pts:
        x0, y0 = cx - 1, cy - 1
        for dy in range(2):
            for dx in range(2):
                X, Y = x0 + dx, y0 + dy
                if m.inb(X, Y) and m.L[2, Y, X] == 0:
                    m.L[2, Y, X] = st[dy][dx]


def add_festoon_strings(m, runs, kind='lstring'):
    """Overhead lantern festoon strings (L2, pri=2)."""
    tiles = [P1('pf_lstring0'), P1('pf_lstring1'), P1('pf_lstring2')] if kind == 'lstring' else [
        K.SINGLE['garl_plain'], K.SINGLE['garl_pennant'], K.SINGLE['garl_lantern'], K.SINGLE['garl_tufts']
    ]
    for x0, x1, y, sd in runs:
        for i, x in enumerate(range(x0, x1 + 1)):
            if m.inb(x, y) and m.L[2, y, x] == 0:
                m.L[2, y, x] = tiles[(i + sd) % len(tiles)]


def add_water_glints(m, water_cls='wW', seed=1, density=0.035):
    """Shimmering water glints (`hb_glint0..3`, pri=2, pas=0) strictly over interior water."""
    rng = random.Random(m.seed * 19 + seed)
    glints = [P1('hb_glint%d' % i) for i in range(4)]
    for y in range(1, m.H - 1):
        for x in range(1, m.W - 1):
            if m.cls[y, x] in water_cls and m.L[2, y, x] == 0 and m.L[1, y, x] == 0:
                if all(m.cls[y + dy, x + dx] in water_cls for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    if rng.random() < density:
                        m.L[2, y, x] = rng.choice(glints)


def paint_boardwalk_strip(m, x0, y0, x1, y1, style='ak', on_cls='sd.ge'):
    """Paint walkable timber boardwalk planks on L0 (safe under props, zero passguard hits)."""
    top = [C('ak', 1516 + i) for i in range(3)]
    body = [C('ak', 1524 + i) for i in range(3)]
    end = [C('ak', 1532 + i) for i in range(3)]
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if not m.inb(x, y) or m.cliff[y, x]:
                continue
            if m.cls[y, x] not in on_cls and m.under[y, x] not in on_cls:
                continue
            row = top if y == y0 else end if y == y1 else body
            col = 0 if x == x0 else 2 if x == x1 else 1
            m.L[0, y, x] = row[col]
            if m.L[1, y, x] >= K.RC.VBASE:
                m.L[1, y, x] = 0


def paint_plaza_stone(m, x0, y0, x1, y1, border_tile, fill_tiles, on_cls='gdc.se', skip_coords=()):
    """Framed frosted limestone plaza on L0."""
    skip = set(skip_coords)
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if not m.inb(x, y) or (x, y) in skip or m.cliff[y, x]:
                continue
            if m.cls[y, x] not in on_cls and m.under[y, x] not in on_cls:
                continue
            on_edge = (x == x0 or x == x1 or y == y0 or y == y1)
            m.L[0, y, x] = border_tile if on_edge else fill_tiles[(x * 7 + y * 11) % len(fill_tiles)]
            if m.L[1, y, x] >= K.RC.VBASE:
                m.L[1, y, x] = 0


def paint_rail_run(m, x0, x1, y, kind='qy', gaps=()):
    """Solid forged iron (`qy`) or stone (`rw`) balustrade along row y."""
    w, mid, e = P1(kind + '_rail_w'), P1(kind + '_rail_m'), P1(kind + '_rail_e')
    for x in range(x0, x1 + 1):
        if x in gaps or not m.inb(x, y) or m.taken[y, x]:
            continue
        lft = (x == x0) or ((x - 1) in gaps)
        rgt = (x == x1) or ((x + 1) in gaps)
        t = w if lft and not rgt else e if rgt and not lft else mid
        m.tile(t, x, y, 1)
        if m.cls[y, x] != 'B':
            m.under[y, x] = m.cls[y, x]
        m.cls[y, x] = 'B'


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


def _open_2x2(mask):
    """Keep ONLY cells belonging to at least one complete 2x2 square so 3x3 bordered turf has zero 1-tile spikes."""
    if mask.shape[0] < 2 or mask.shape[1] < 2:
        return np.zeros_like(mask)
    core = mask[:-1, :-1] & mask[:-1, 1:] & mask[1:, :-1] & mask[1:, 1:]
    out = np.zeros_like(mask)
    out[:-1, :-1] |= core
    out[:-1, 1:] |= core
    out[1:, :-1] |= core
    out[1:, 1:] |= core
    return out


def paint_snow_turf_layering(m, seed=1, cer_thr=0.61, peri_thr=0.69, only_cls='.'):
    """Break up flat white snow plains with native seamless wind-swept snow drift variation (sn_g0..sn_g3).
    Replaces CERULEAN_3X3 / PERI_3X3 which carry purple outer borders that created hard square boxes on white snow (S1)."""
    ok = np.isin(m.cls, list(only_cls)) & ~m.cliff & (m.L[1] == 0)
    G = [K.P1('sn_g%d' % i) for i in range(4)]
    for y in range(1, m.H - 1):
        for x in range(1, m.W - 1):
            if not ok[y, x]:
                continue
            v1 = vnoise(x, y, seed * 17 + 3, 7.5)
            v2 = vnoise(x, y, seed * 29 + 11, 4.5)
            if v1 > cer_thr - 0.08:
                m.L[0, y, x] = G[int(v2 * 3.999)]


def paint_forest_ground_depth(m, seed=1, clearings=(), dark=0.48):
    """Soft-tufted shaded moss & worn sunlit earth using rkit's baked Grassnone transition tiles."""
    m.grass_var = True
    m.grass_variation(dark=dark, worn=True)
    worn = [[P1('gr_worn00'), P1('gr_worn01')], [P1('gr_worn10'), P1('gr_worn11')]]
    for idx, (cx, cy, rx, ry, mode) in enumerate(clearings):
        if mode != 'worn':
            continue
        for y in range(max(0, int(cy - ry - 1)), min(m.H, int(cy + ry + 2))):
            for x in range(max(0, int(cx - rx - 1)), min(m.W, int(cx + rx + 2))):
                if m.cls[y, x] != '.' or m.cliff[y, x]:
                    continue
                q = ((x - cx) / max(1.0, rx)) ** 2 + ((y - cy) / max(1.0, ry)) ** 2
                q += 0.25 * (vnoise(x, y, seed + 910 + idx, 3.0) - 0.5)
                if q <= 0.55:
                    m.L[0, y, x] = worn[y & 1][x & 1]


def infill_forest(r, palettes, pick=None, scale=9.0, seed=0):
    """Dense forest rim packer: 3x2 lattice trees -> 2x2 Sheridan spruces/shrubs -> 1x2 slender cypresses."""
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
            for ox in (0, -1):
                if all(m.inb(x + ox + dx, y + dy) and hole[y + dy, x + ox + dx] for dx in range(2) for dy in range(2)):
                    if rng.random() < 0.68:
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
            if y > 0 and m.L[2, y - 1, x] == 0 and rng.random() < 0.78:
                m.L[2, y - 1, x] = SH_CYPRESS[0][0][0]
                m.L[1, y, x] = SH_CYPRESS[1][0][0]
            else:
                b = rng.choice(('nt_bush0', 'nt_bush1'))
                m.L[1, y, x] = int(np.array(STAMPS[b]['layers']).max())
            m.taken[y, x] = True
            hole[y, x] = False
            placed += 1
    return placed


def infill_winter(m_or_r, palettes, scale=9.0, seed=0, avoid_top=None):
    """Dense winter canopy packer: 3x2 Kristiline spruces -> 2x2 teal pines -> 2x1 frosted shrubs/boulders.
    Respects `avoid_top` mask so tree canopies NEVER clip over hut roofs, doorways, or hero landmarks."""
    m = m_or_r.m if hasattr(m_or_r, 'm') else m_or_r
    sd = m_or_r.seed if hasattr(m_or_r, 'seed') else m.seed
    rng = random.Random(sd * 37 + seed + 13)
    s = sd + 1313
    hole = (m.cls == 'T') & ~m.taken & (m.L[1] == 0) & ~m.cliff
    placed = 0

    def top_blocked(xs, ys):
        if avoid_top is None:
            return False
        for yy in ys:
            for xx in xs:
                if m.inb(xx, yy) and avoid_top[yy, xx]:
                    return True
        return False

    for y in range(m.H):
        for x in range(m.W):
            if not hole[y, x]:
                continue
            done = False
            for ox in (0, -1, -2):
                tx = x + ox
                foot = [(tx + dx, y + dy) for dx in range(3) for dy in range(2)]
                if not all(m.inb(fx, fy) and hole[fy, fx] for fx, fy in foot):
                    continue
                if top_blocked(range(tx, tx + 3), range(y - 2, y)):
                    continue
                z = vnoise(tx, y, s, scale)
                pal = palettes[min(len(palettes) - 1, int(z * len(palettes) * 0.999))]
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
            for ox in (0, -1):
                if all(m.inb(x + ox + dx, y + dy) and hole[y + dy, x + ox + dx] for dx in range(2) for dy in range(2)):
                    if top_blocked(range(x + ox, x + ox + 2), range(y - 2, y)):
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
            for ox in (0, -1):
                if all(m.inb(x + ox + dx, y) and hole[y, x + ox + dx] for dx in range(2)):
                    sp = rng.choice((KF_SHRUB_A, KF_SHRUB_B, KF_SHRUB_A, KF_BOULDER))
                    top, bot = sp
                    if top and y > 0 and not top_blocked(range(x + ox, x + ox + 2), (y - 1,)):
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
            m.L[1, y, x] = rng.choice((10551, 10551, 9872, 9888, 10371))
            m.taken[y, x] = True
            hole[y, x] = False
            placed += 1
    return placed


def mark_stamp_avoid(avoid, name, x, y, pad_x=1, pad_n=2, pad_s=1):
    """Mark a stamp's full silhouette + surrounding apron so overhead tree canopies never clip roofs/doorways."""
    st = STAMPS[name]
    H, W = avoid.shape
    y0 = max(0, y - pad_n)
    y1 = min(H, y + st['h'] + pad_s)
    x0 = max(0, x - pad_x)
    x1 = min(W, x + st['w'] + pad_x)
    avoid[y0:y1, x0:x1] = True


def erode_snow_grass_organic(m, seed=1):
    """Erode boxy snow tall-grass ('t') patches into ragged organic wind-swept glades with curved edges,
    interior snow-drift bites, and wispy scattered perimeter tufts (eliminates rigid rectangular grids!)."""
    rng = random.Random(seed * 73 + 19)
    mask = (m.cls == 't')
    H, W = m.H, m.W
    out = mask.copy()
    # 1. Bite out square corners & straight run edges using noise
    for y in range(1, H - 1):
        for x in range(1, W - 1):
            if not mask[y, x]:
                continue
            n4 = int(mask[y - 1, x]) + int(mask[y + 1, x]) + int(mask[y, x - 1]) + int(mask[y, x + 1])
            n8 = int(mask[y - 1:y + 2, x - 1:x + 2].sum()) - 1
            vn = vnoise(x, y, seed * 19 + 5, 2.6)
            # Round off rectangular corners (2 orthogonal neighbors) & bite straight flanks
            if n4 <= 2 and vn < 0.62:
                out[y, x] = False
            elif n4 == 3 and vn < 0.34:
                out[y, x] = False
            # Carve occasional wind-scoured snow drift clearings inside solid >= 3x3 blocks
            elif n8 == 8 and vnoise(x, y, seed * 31 + 7, 3.2) > 0.72:
                out[y, x] = False
    # 2. Feather wispy stray tufts 1-2 tiles off curved borders onto free open snow
    for y in range(2, H - 2):
        for x in range(2, W - 2):
            if out[y, x] or m.cls[y, x] != '.' or m.cliff[y, x] or m.taken[y, x]:
                continue
            n4 = int(out[y - 1, x]) + int(out[y + 1, x]) + int(out[y, x - 1]) + int(out[y, x + 1])
            if n4 == 1 and rng.random() < 0.22:
                out[y, x] = True
    m.cls[mask & ~out] = '.'
    m.cls[out & ~mask] = 't'


def dress_water_lotus(m, prob=0.14, seed=1, avoid_x=None):
    """Scatter pink lotus pads (pas=15) organically on calm water pockets."""
    rng = random.Random(seed)
    water = (m.cls == 'w')
    for y in range(1, m.H - 1):
        for x in range(1, m.W - 1):
            if avoid_x is not None and avoid_x[0] <= x <= avoid_x[1]:
                continue
            if not water[y, x] or m.L[1, y, x] != 0 or m.L[2, y, x] != 0 or m.taken[y, x]:
                continue
            nb_land = sum(1 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if not water[y + dy, x + dx])
            p = prob * (1.35 if nb_land >= 1 else 0.7)
            if rng.random() < p:
                m.L[1, y, x] = rng.choice(LOTUS_TILES)


def scatter_petals_and_mushrooms(m, spots_petals=(), spots_mush=(), seed=1):
    """Place walkable blossom petals (5723) and glowing mushrooms (451..462) strictly on safe open ground."""
    rng = random.Random(seed)
    for cx, cy, rx, ry, density in spots_petals:
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


def seal_unconnected_edges(m, open_cells=(), filler=None):
    """Seal any stray walkable cell on the 4 map perimeter edges NOT listed in `open_cells`."""
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
            ft = f[(x * 7 + y * 13) % len(f)] if isinstance(f, (tuple, list)) else f
            m.L[2, y, x] = 0
            if m.L[1, y, x] == 0 or (int(m.L[1, y, x]) < len(pas) and (pas[int(m.L[1, y, x])] & 0x0f) != 0x0f):
                m.L[1, y, x] = ft
            else:
                m.L[2, y, x] = ft


def water_prop_stamp(m, name, x, y, water_cls='wW', skip_cells=()):
    """Stamp a boat/rock/piling/buoy cleanly onto L2 over open water cells."""
    L = np.array(STAMPS[name]['layers'])
    h, w = L.shape[1:]
    skip = set(skip_cells)
    if x < 0 or y < 0 or x + w > m.W or y + h > m.H:
        return False
    for j in range(h):
        for i in range(w):
            t = int(L[:, j, i].max())
            if t and (m.cls[y + j, x + i] not in water_cls or m.L[2, y + j, x + i] != 0 or (x + i, y + j) in skip):
                return False
    for j in range(h):
        for i in range(w):
            t = int(L[:, j, i].max())
            if t:
                m.L[2, y + j, x + i] = t
    return True


def write_wave13_map(m, mid, header_comment):
    """Resolve virtual autotiles, run passguard, save raw .npy, and write EXACT immutable HEAD YAML spec."""
    Lr = RC.resolve(m.L, m.tid).astype(np.int32)
    hspec = head_spec(mid)
    ev_pts = [tuple(e['at']) for e in (hspec.get('events') or []) if e and e.get('at')]
    PG.guard(Lr, m.tid, ev_pts, 'map %d' % mid)

    os.makedirs(os.path.join(MAPGEN, 'data', 'raw'), exist_ok=True)
    rel = 'data/raw/%d.npy' % mid
    np.save(os.path.join(MAPGEN, rel), Lr)

    key = Lr[0].astype(np.int64) * 10 ** 10 + Lr[1].astype(np.int64) * 10 ** 5 + Lr[2]
    mir = (key == key[:, ::-1]).mean() * 100.0
    print(f'  [wave13] wrote {rel} ({m.W}x{m.H}, ts={m.tid}) | mirror={mir:.1f}%')

    spec = copy.deepcopy(hspec)
    spec['raw'] = rel
    spec['tileset'] = m.tid
    events = spec.pop('events', [])
    body = yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=150, allow_unicode=True)
    body += yaml.safe_dump({'events': events}, sort_keys=False, default_flow_style=None, width=150, allow_unicode=True)
    out_yaml = os.path.join(MAPGEN, 'specs', SPEC_FILES[mid])
    with open(out_yaml, 'w', encoding='utf-8') as f:
        f.write(header_comment + body)
    return Lr


# =============================================================================
# 4. MAP 167: EBBMOUTH - MILL QUAY (40x30, ts 52 PF Rejuv Snow)
# =============================================================================
def build_167():
    """Ebbmouth - Mill Quay (40x30, ts 52): unified seamlessly with Wave 10's 160 Ebbmouth!
    Weathered maritime timber wharf continuing 160's col 28..30 boardwalk, frosted limestone striker plaza,
    curved River Ebb head-pond with three turning tidal waterwheels + inspection footbridge to east bank
    SUPERPOTION (37, 28), iron quay railings & bollards, dense Kristiline conifer ridges, warm amber beacons."""
    W, H = 40, 30
    hspec = head_spec(167)
    evs = hspec['events']
    m = snowmap(W, H, 167, kit='shs3')

    def river_x(y, base=34.5, amp=1.4, per=7.0):
        return base + amp * math.sin(y / per)

    # ---- 1. Organic Tidal River Ebb & Mill Head-Pond (exact col 31..37 seam match with 160 Ebbmouth!) ----
    for y in range(0, H):
        c = river_x(y - H)
        wob = 0.7 * math.sin(y / 3.8)
        for x in range(int(round(c - 2.6 + wob)), int(round(c + 3.4 + wob))):
            if m.inb(x, y):
                m.cls[y, x] = 'W'
    # Exact south seam alignment with 160 Ebbmouth row 0 (walkable boardwalk x=28..30, river x=31..37)
    for x in range(31, 38):
        m.cls[H - 1, x] = 'W'
    m.cls[H - 1, 28:31] = 'd'
    # Sculpted mill head-pond above the upper waterwheel (NE cove)
    m.blob(29.5, 6.5, 5.2, 3.2, 'W', seed=171, rough=0.38)
    m.blob(33.0, 14.5, 3.4, 2.2, 'W', seed=172, rough=0.35)
    # Keep east bank trail walkable down to SUPERPOTION (37, 28)!
    for y in range(10, 29):
        for x in (37, 38):
            if m.inb(x, y) and y >= 11:
                m.cls[y, x] = '.'
    m.cls[27:29, 36:39] = '.'

    # ---- 2. Stepped Union-Hall Terrace (h=1, crisp 3-row shs3 snow cliff!) ----
    for y in range(H):
        for x in range(W):
            if x <= 19 + int(round(1.1 * vnoise(0, y, 174, 4.0))) and y <= 11:
                m.ht[y, x] = 1
    m.stairs(14, 11, w=3, kit_rows=3)
    m.plan_cliffs()

    # ---- 3. Dense Kristiline Forest Framing (N ridge, W flank, SW/SE pine groves) ----
    for y in range(H):
        for x in range(W):
            if m.cls[y, x] != '.':
                continue
            north = y <= 2 + 1.3 * vnoise(x, 0, 172, 4.0) and x < 28
            west = x <= 1 + 1.2 * vnoise(0, y, 173, 4.0) and not (16 <= y <= 20)
            sw_edge = y >= H - 2 and x < 26
            east_rim = x >= 39 and y < 27
            if north or west or sw_edge or east_rim:
                m.cls[y, x] = 'T'

    # ---- 4. Quay Lanes, Timber Wharf Apron & Cart Yard ----
    m.rect(28, H - 12, 3, 12, 'd', only='.T')  # exact col 28..30 boardwalk link to 160!
    m.lane([(29.0, 22), (26.0, 18.5), (19.0, 18.0), (10.0, 18.0), (4.0, 19.5)], 'd', 3.0, seed=175, wobble=0.35)
    m.lane([(15.5, 16), (15.5, 11)], 'd', 2.6, seed=176, wobble=0.1)
    m.lane([(4, 9.5), (10, 10.0), (18, 9.5)], 'd', 2.4, seed=177, wobble=0.25)
    m.lane([(10, 19), (9, 24.5), (12, 26.5)], 'd', 2.2, seed=178, wobble=0.3)
    m.lane([(26.5, 19), (26.5, 25), (28.5, 27)], 'd', 2.4, seed=179, wobble=0.15)
    m.lane([(37.5, 12), (37.5, 20), (37.5, 28)], 'd', 1.5, seed=180, wobble=0.2, only='.T')  # east mill-race inspection path
    # Keep (2, 17) hidden HEARTSCALE accessible!
    m.lane([(4.5, 18.5), (2.0, 17.0)], 'd', 1.6, seed=181, wobble=0.1, only='.T')
    smooth_cls(m, 'd', into='.', passes=1)
    # Muddy cart tracks under cargo staging yard
    m.blob(17.5, 21.5, 4.2, 2.2, 'e', seed=182, only='d.', rough=0.38)
    m.blob(6.5, 18.5, 2.5, 1.6, 'e', seed=183, only='d.', rough=0.35)

    # Frosted tundra grass pockets breaking up bare white snow
    for cx, cy, rx, ry in ((14, 25, 2.5, 1.6), (22, 14, 2.0, 1.5), (38, 17, 1.5, 2.2)):
        m.blob(cx, cy, rx, ry, 't', seed=cx + cy, only='.', rough=0.55)

    # ---- 5. Buildings (Union Halls on Terrace, Tide Mill on Quay, Carter's Hut SW) ----
    m.stamp('wb_long3', 3, 3, None, 'x')
    m.stamp('wb_long', 14, 2, None, 'x')
    m.stamp('wb_smoke', 22, 10, None, 'x')
    m.stamp('wb_hut', 3, 21, None, 'x')
    m.events = []

    # ---- 6. Lock ALL 10 Exact HEAD Events & Signposts ----
    ev_pts = [tuple(e['at']) for e in evs]
    for ex, ey in ev_pts:
        if m.cls[ey, ex] in 'T':
            m.cls[ey, ex] = 'd'
    prot_wide = reserve_events(m, evs, radius=1, extra=[(28, 29), (29, 29), (30, 29), (15, 11), (15, 12), (15, 13), (15, 14)])
    prot_strict = reserve_events(m, evs, radius=0)
    paint_signposts(m, evs)

    # ---- 7. Harbour Hardware, Cargo Clusters, Railings, Lanterns & Kristiline Conifers ----
    # Iron quay railings along upper union terrace overlook
    paint_rail_run(m, 4, 12, 11, kind='qy', gaps=(8,))
    # Iron mooring bollards along the Mill Quay edge
    for bx, by in ((29, 18), (29, 20), (29, 24), (27, 27)):
        if m.inb(bx, by) and not prot_strict[by, bx] and not m.taken[by, bx] and m.cls[by, bx] in '.de':
            m.over.append((1, bx, by, P1('hb_bollard0' if by % 2 else 'hb_bollard1')))
            m.taken[by, bx] = True

    glow_pts = []
    # Warm braziers, striker cargo piles, crates, barrels, sleds, fish racks, benches
    for nm, x, y in (
        ('fw_brazier', 13, 17), ('fw_brazier', 22, 19), ('fw_brazier', 23, 15),
        ('pf_wlamp', 29, 23), ('pf_wlamp', 12, 16),
        ('pf_lantern', 10, 15), ('pf_lantern', 26, 16), ('pf_lantern', 6, 10), ('pf_lantern', 18, 10),
        ('sh_crates', 18, 20), ('hb_crates4', 20, 22), ('hb_barrels', 6, 16), ('hb_cask', 25, 15),
        ('wr_sacks', 16, 21), ('wr_sacks', 8, 21), ('fw_sled', 8, 20),
        ('fw_wood', 4, 27), ('fw_rack', 15, 23), ('hb_rope', 25, 21),
        ('pf_logbench', 10, 11), ('pf_logbench', 18, 16), ('pf_whalebone', 22, 26),
        ('hb_banner', 7, 9), ('hb_banner', 17, 8),
    ):
        res = put_safe(m, nm, x, y, on='.de', r=2, prot=prot_wide)
        if res and nm in ('fw_brazier', 'pf_wlamp', 'pf_lantern'):
            glow_pts.append((res[0], res[1] + (1 if nm != 'fw_brazier' else 0)))

    # Dense Kristiline conifer groves framing the yard edges (zero bald corners!)
    for idx, (cx, cy, cnt, rad, hero) in enumerate((
        (20, 26, 4, 2.5, True),
        (7, 27, 3, 2.2, False),
        (25, 5, 3, 2.0, False),
        (38, 4, 3, 2.0, False),
        (38, 23, 2, 1.8, False),
    )):
        place_snow_grove(m, cx, cy, count=cnt, radius=rad, on='.tT', seed=167 + idx, hero=hero, prot=prot_wide)

    # Pack forest borders with dense Kristiline spruces via CK.woods + infill_winter!
    r_stub = type('RStub', (), {'m': m, 'W': W, 'H': H, 'seed': 167})()
    CK.woods(r_stub, ALPINE_WOODS, scale=8.0)

    # ---- 8. Paint + Timber Wharf, Stone Plaza, Sluice Bridge, Waterwheels & Atmospheric Polish ----
    m.paint()
    infill_winter(r_stub, ALPINE_WOODS, scale=8.0, seed=167)

    # Weathered maritime timber wharf continuing 160's col 28..30 boardwalk all along the Mill Quay!
    paint_boardwalk_strip(m, 28, 16, 30, H - 1, style='ak', on_cls='de.')
    paint_boardwalk_strip(m, 25, 17, 28, 19, style='ak', on_cls='de.')
    # Frosted limestone quay courtyard for the union strikers
    frost_stone = [P1('lm_pave%d' % i) for i in range(4)]
    paint_plaza_stone(m, 9, 17, 23, 20, P1('lm_pave0'), frost_stone, on_cls='de.')
    paint_plaza_stone(m, 5, 9, 18, 10, P1('lm_pave0'), frost_stone, on_cls='de.')

    # Scenic timber mill-race inspection footbridge at y=11..12 linking west quay to east bank SUPERPOTION (37, 28)!
    RW.bridges(m, ((11, 12),), cls='W')
    # Ensure clean approach onto bridge from both sides
    for bx in range(28, 39):
        if m.inb(bx, 11) and m.cls[11, bx] == 'T':
            m.L[1, 11, bx] = 0
            m.L[2, 11, bx] = 0
        if m.inb(bx, 12) and m.cls[12, bx] == 'T':
            m.L[1, 12, bx] = 0
            m.L[2, 12, bx] = 0

    # Three turning tidal waterwheels along the Mill Quay race + sluice posts!
    for i, wy in enumerate((14, 19, 25)):
        wx = int(round(river_x(wy + 1 - H) - 2.4))
        put_overlay_stamp(m, 'eb_wheel%d' % (i % 2), wx, wy, z=2)
    for sx in (31, 33, 35):
        if m.inb(sx, 10) and m.cls[10, sx] == 'W':
            put_overlay_stamp(m, 'df_sluice', sx, 10, z=2)

    # Rocky river boulders, sea-ice floes & moored work-skiffs in the mill head-pond & race
    for nm, x, y in (('hb_boat1', 27, 5), ('fw_boat', 32, 3), ('ak_rock2', 35, 6), ('nt_boulder', 31, 8), ('nt_boulder', 35, 22)):
        water_prop_stamp(m, nm, x, y, water_cls='W')

    # Glacial snow-edged turf patches, ice sparkles, chimney smoke, festoon strings & warm lantern glows!
    paint_snow_turf_layering(m, seed=167, cer_thr=0.59, peri_thr=0.68)
    RW.icy_faces(m, 0.55, seed=167)
    RW.dress_ice(m, 0.25, seed=167)
    RW.reed_beds(m, 14, seed=167)
    for nm, x, y in (('fw_smoke_w', 6, 1), ('fw_smoke_w', 17, 0), ('fw_smoke_w', 24, 8), ('fw_smoke_w', 5, 19)):
        put_overlay_stamp(m, nm, x, y, z=2)
    add_festoon_strings(m, [(9, 22, 17, 0), (5, 17, 9, 1)], kind='lstring')
    add_warm_glows(m, glow_pts + [(29, 18), (29, 25), (15, 13)])
    add_water_glints(m, water_cls='W', seed=167, density=0.04)
    m.scatter(6, seed=167)
    RW.road_tracks(m, 0.10, seed=167)
    RW.drifts(m, 0.08, seed=167)

    # Seal all perimeter edges strictly except col 28..30 S connection to 160 Ebbmouth!
    seal_unconnected_edges(m, open_cells=[(28, H - 1), (29, H - 1), (30, H - 1)], filler=10371)
    write_wave13_map(m, 167, '# Ebbmouth - Mill Quay (167). WRITTEN BY layouts/wave13_routes_craft.py (Wave 13 Rejuv V14 Craft).\n')
    return m


# =============================================================================
# 5. MAP 552: THE DYERS' FORD (80x72, ts 53 PF Rejuv Wild)
# =============================================================================
def build_552():
    """The Dyers' Ford (80x72, ts 53): lush Rejuv V14 river valley — curved north dye-works bluff,
    sinuous S-curve River Selvedge with twin mossy islets, crimson/indigo/ochre braided dye plumes
    dissolving into an organic curving Fourth Colour white-water waterfall & plunge basin, organic curved
    SE sheep-wash lotus pool (zero boxy rectangles!), dense multi-canopy emerald & cherry woods with
    dark-moss ground depth, weathered dye-crop meadows, and exact HEAD event/sluice/culvert parity."""
    W, H = 80, 72
    hspec = head_spec(552)
    evs = hspec['events']
    r = Route(552, W, H, 'meadow', base='.')
    m = r.m

    # ---- 1. Organic Curved North Dye-Works Bluff (h=1, keeping sluice plaza y<=20 & culvert flat!) ----
    lipy = colmap(r, lambda x: 20 + 2.2 * math.sin((x - 12) / 10.5)
                  + 1.3 * (vnoise(x, 0, 5521, 8.0) - 0.5) * 2
                  + bump(x, 12, 8, 2.0) + bump(x, 52, 9, 2.8))
    fall_y = lipy[68]
    for x in range(66, 72):
        lipy[x] = fall_y
    for x in range(W):
        m.ht[:lipy[x] + 1, x] = 1
    CK.smooth_ht(m, 1, 2)

    # ---- 2. Organic S-Curve River Selvedge + Twin Mossy Islets + Sinuous Fourth Colour Stream ----
    cy = colmap(r, lambda x: 35.5 + 4.4 * math.sin((x - 18) / 13.5)
                + 1.3 * (vnoise(x, 1, 552, 11.0) - 0.5) * 2)
    for x in range(W):
        hw = 5 + int(round(3.0 * bump(x, 15, 7.5, 1.0) + 2.8 * bump(x, 58, 7.5, 1.0)))
        for y in range(max(lipy[x] + 5, cy[x] - hw), min(H - 12, cy[x] + hw + 1)):
            m.cls[y, x] = 'w'
    CK.smooth_sea(m, 2)

    # Twin lush mossy river islets splitting the braided current
    m.blob(15, cy[15], 4.8, 2.8, '.', seed=5528, rough=0.32, only='w')
    m.blob(58, cy[58], 4.5, 2.6, '.', seed=5529, rough=0.32, only='w')

    # Gently curving Fourth Colour clear mountain brook (NO ruler-straight vertical canal!)
    CK.stream(r, [(69.5, 0), (69.0, 5), (67.5, 10), (68.0, 15), (68.0, fall_y - 1)], w=2.5, c='w', only='.tT')
    CK.stream(r, [(68.0, fall_y + 4), (68.5, fall_y + 7), (67.5, cy[68] - 3)], w=2.6, c='w', only='.tT')
    # Organic waterfall plunge pool below the bluff
    m.blob(68.2, fall_y + 5.5, 3.2, 2.0, 'w', seed=5535, rough=0.35, only='.t')
    m.cls[fall_y:fall_y + 4, 67:70] = '.'
    sx = 67

    # ---- 3. Curved Weavers' Road, Diagonal Gravel-Shoal Stepping Ford & Side Lanes ----
    r.road([(40.5, 0), (39, 6), (34, 12), (32, lipy[32] - 1)], w=3.0, open_=None, only='.tT')
    stair_y = max(y for y in range(30) if m.ht[y, 32] == 1)
    CK.stair(r, 31, stair_y, w=3, h=1)
    ford_n = (44, cy[44] - 6)
    ford_s = (40, cy[40] + 6)
    r.road([(32, stair_y + 3), (35, 28), (41, 30), ford_n], w=3.0, open_=None, only='.tT')
    r.road([ford_s, (37, 51), (35, 58), (38, 65), (39.5, 71)], w=3.0, open_=None, only='.tT')
    r.exit('N', 39, 4)
    r.exit('S', 38, 4)

    # Pale gravel shoal aprons framing both banks of the diagonal ford
    m.blob(ford_n[0], ford_n[1], 3.4, 1.9, 'g', seed=5531, rough=0.38, only='.d')
    m.blob(ford_s[0], ford_s[1], 3.4, 1.9, 'g', seed=5532, rough=0.38, only='.d')

    # Diagonal staggered stepping stones across the wide shoal
    y_top = min(y for y in range(25, 55) if m.cls[y, 44] == 'w')
    y_bot = max(y for y in range(25, 55) if m.cls[y, 40] == 'w')
    stones_ = []
    for y in range(y_top, y_bot + 1):
        t = (y - y_top) / float(max(1, y_bot - y_top))
        xc = int(round(44 * (1 - t) + 40 * t))
        for dx in (-1, 0, 1):
            xx = xc + dx
            if m.inb(xx, y) and m.cls[y, xx] == 'w' and (dx == 0 or (xx + y) % 2 == 0):
                stones_.append((xx, y))
        if y > y_top:
            xc_prev = int(round(44 * (1 - (y - 1 - y_top) / float(max(1, y_bot - y_top))) + 40 * ((y - 1 - y_top) / float(max(1, y_bot - y_top)))))
            if xc_prev != xc and m.cls[y, xc_prev] == 'w':
                stones_.append((xc_prev, y))
    stones_ = sorted(set(stones_))

    # Side lanes to dye-works, sluice plaza, culvert, jetty, fulling mill, sheep-wash
    r.lane([(37, 11), (46, 13), (56, 14), (61, 13)], w=2.2, open_=None)
    r.lane([(50, 14), (51, 18)], w=2.4, open_=None)
    r.lane([(61, 13), (64, 11), (64, 5)], w=1.6, open_=None)
    r.lane([(42, 30), (54, 28), (64, 26), (72, cy[72] - 6)], w=2.2, open_=None)
    r.lane([(37, 51), (28, 48), (22, 46)], w=2.0, open_=None)
    r.lane([(36, 58), (52, 57), (65, 56)], w=2.0, open_=None)
    # Stone-gravel sluice basin terrace around the 3 colour stones (49/51/53, 18)
    m.rect(47, 16, 9, 4, 'g', only='.dt')

    # Bleachfield white-flower meadow (NE behind culvert) & ORGANIC multi-lobe SE sheep-wash lotus pond!
    r.clearing(60, 3, 5.5, 2.8, c='.')
    m.blob(70.5, 57.5, 4.6, 2.4, 'w', seed=5541, rough=0.45, only='.t')
    m.blob(73.0, 59.5, 3.2, 2.1, 'w', seed=5542, rough=0.45, only='.t')
    m.blob(68.0, 56.0, 2.5, 1.7, 'w', seed=5543, rough=0.42, only='.t')
    CK.smooth_sea(m, 1)

    # ---- 4. Dense Organic Valley Woods & Copses (leaving clear sightlines & landmarks!) ----
    r.forest_band('W', 5, wobble=2.5)
    r.forest_band('E', 4, wobble=2.2)
    r.forest_band('N', 3, wobble=1.5)
    r.forest_band('S', 2, wobble=1.5)
    for cx, cy_, rx, ry in (
        (9, 7, 7.5, 5.5), (22, 6, 5.8, 4.2), (6, 62, 5.5, 6.2), (74, 67, 5.5, 4.2),
        (23, 25, 3.6, 2.4), (52, 46, 3.8, 2.6), (65, 45, 3.4, 2.4), (28, 7, 3.8, 3.0),
        (4, 50, 3.2, 4.0), (48, 70, 4.2, 2.2), (76, 54, 2.8, 3.8), (15, 23, 3.5, 2.2),
    ):
        r.copse(cx, cy_, rx, ry)
    # Culvert choke wall: ensure (64, 8) Culvert grate is the ONLY access to the Bleachfield!
    for y in range(6, 11):
        for x in (62, 63, 65, 66):
            if m.cls[y, x] in '.td' and m.cls[y, x] != 'w':
                m.cls[y, x] = 'T'
    m.cls[8, 64] = 'd'
    m.cls[7, 64] = 'd'
    m.cls[9, 64] = 'd'
    # Keep Bargee (72, 26) & north/south river approaches open!
    for ex, ey in [tuple(e['at']) for e in evs]:
        if m.cls[ey, ex] == 'T':
            m.cls[ey, ex] = '.'
    r.finish_plan(border=0)
    CK.waterfall(r, sx, sx + 2, lipy[sx + 1])

    # ---- 5. Organic Madder (red), Woad (blue) & Weld (yellow) Crop Meadows + Tall Grass ----
    fields = {'r': [(13, 55, 4.5), (20, 60, 3.8)],
              'b': [(52, 52, 4.2), (58, 62, 3.8)],
              'y': [(27, 64, 3.8), (16, 66, 3.2)]}
    for k, spots in fields.items():
        CK.grass_fields(r, spots)
    dyemask = {k: np.zeros((H, W), bool) for k in fields}
    for k, spots in fields.items():
        for (fx, fy, s_) in spots:
            for y in range(max(0, int(fy - 2.4 * s_)), min(H, int(fy + 2.4 * s_))):
                for x in range(max(0, int(fx - 2.4 * s_)), min(W, int(fx + 2.4 * s_))):
                    wob = 0.28 * (vnoise(x, y, 5590 + ord(k), 4.0) - 0.5)
                    if m.cls[y, x] == 't' and ((x - fx) / (2.0 * s_)) ** 2 + ((y - fy) / (1.7 * s_)) ** 2 <= 0.95 + wob:
                        dyemask[k][y, x] = True
    CK.grass_fields(r, [(16, 26, 2.8), (56, 24, 2.8), (7, 25, 2.4), (24, 14, 2.8), (14, 15, 2.6), (74, 24, 2.4), (46, 66, 2.8)])
    CK.ledge(r, 25, 33, 50)
    for y in (49, 50, 51):
        for x in (24, 34):
            if m.cls[y, x] in '.t':
                m.cls[y, x] = 'T'

    # Lock exact HEAD events & stepping stones before tree/prop dressing!
    stones_ = [c for c in stones_ if m.cls[c[1], c[0]] == 'w']
    CK.stones(r, stones_)
    prot_wide = reserve_events(m, evs, road_mask=r.road_mask, radius=1,
                               extra=[(39, 0), (40, 0), (41, 0), (42, 0), (38, H - 1), (39, H - 1), (40, H - 1), (41, H - 1),
                                      (64, 7), (64, 8), (64, 9), (60, 4), (57, 4), (58, 4), (59, 4)])
    paint_signposts(m, evs)

    # Dense multi-canopy Elowen valley woods
    CK.woods(r, VALLEY_WOODS, scale=10.0)

    # ---- 6. Dye Sheds, Vats, Fulling Mill, Drying-Cloth Corridors, Lanterns & River Jetty ----
    glow_pts = []
    for nm, x, y in (('gl_shed', 45, 4), ('gl_shed', 51, 6), ('gl_shed', 58, 5)):
        put_safe(m, nm, x, y, on='.d', r=3, prot=prot_wide)
    for n, x, y in (
        # Upper dye-works terrace (vats, hanging fabric racks, barrels & sluice works)
        ('pf_p_vat_r', 49, 16), ('pf_p_vat_b', 51, 16), ('pf_p_vat_y', 53, 16),
        ('pf_p_vat_r', 45, 11), ('pf_p_vat_b', 52, 12), ('pf_p_vat_y', 57, 13),
        ('hb_dyeline', 43, 8), ('hb_rugline', 49, 11), ('hb_rugline2', 55, 11),
        ('hb_barrels', 60, 16), ('hb_crates4', 58, 17), ('df_sluice', 62, 16),
        # North & south bankside drying racks, dye vats & barrels framing The Dyers' Ford!
        ('hb_rugline', 19, 25), ('hb_dyeline', 27, 26), ('hb_rugline2', 35, 25),
        ('hb_barrels', 21, 28), ('hb_crates4', 29, 28), ('hb_barrels', 36, 28),
        ('hb_dyeline', 46, 26), ('hb_rugline', 53, 25),
        ('pf_p_vat_r', 18, 45), ('pf_p_vat_b', 20, 45), ('pf_p_vat_y', 23, 45),
        ('hb_rugline2', 25, 46), ('hb_dyeline', 45, 47), ('hb_rugline', 48, 45),
        ('pf_p_vat_b', 46, 49), ('pf_p_vat_y', 48, 49), ('hb_crates4', 32, 49),
        ('pf_logbench', 31, 47), ('hb_tubs', 63, 58), ('hb_barrels', 21, 48),
        ('pf_shrine', 63, 25), ('pf_lantern', 46, 17), ('pf_lantern', 56, 17),
        ('pf_lantern', 35, 29), ('pf_lantern', 43, 47), ('pf_lantern', 64, 25),
        ('pf_lantern', 23, 47), ('pf_lantern', 38, 66), ('pf_lantern', 42, 6),
        ('pf_lantern', 25, 29), ('pf_lantern', 47, 46),
    ):
        res = put_safe(m, n, x, y, on='.dg', r=3, prot=prot_wide)
        if res and n == 'pf_lantern':
            glow_pts.append((res[0], res[1] + 1))

    # Low mossy stone curb framing sluice basin plaza
    for x in (47, 48, 54, 55):
        if m.free(x, 19, 1, 1, on='.g') and not m.taken[19, x] and not prot_wide[19, x]:
            m.stamp('nr_wall_' + ('w' if x == 47 else 'e' if x == 55 else 'm'), x, 19, mark='B')

    # Grounded Fulling Mill on SW river bend + timber mill-race deck & south dye-washing pier
    put_safe(m, 'gl_flat2', 11, 43, on='.t', r=5, prot=prot_wide)
    mill_y0 = max(y for y in range(25, 52) if m.cls[y, 16] == 'w')
    r.deck += [(x, y) for x in (15, 16) for y in range(mill_y0 - 1, mill_y0 + 1) if m.inb(x, y) and m.cls[y, x] == 'w']
    for sx_p in (22, 47):
        s_bank = max(y for y in range(25, 52) if m.cls[y, sx_p] == 'w')
        r.deck += [(sx_p, s_bank), (sx_p + 1, s_bank)]

    # Sheep-wash fences & organically staggered, themed drying-cloth bunting banners (NO identical parallel lines!)
    m.fence(58, 68, 51, gaps=((62, 64),))
    m.fence(58, 68, 64, gaps=((60, 62),))
    bunting_specs = [
        # (y_base, x_lo, x_hi, palette_seq, sag_center)
        (6,  35, 44, 'rrybrr', True),    # Upper Weavers' Road — crimson & weld welcome banner
        (12, 30, 38, 'bbybby', False),   # Dye-works lane — indigo woad banner (shorter, shifted W)
        (25, 32, 40, 'ryyryb', True),    # Bluff foot — ochre & crimson drying flags
        (30, 39, 47, 'rbrbyy', False),   # Ford north approach — festive tri-colour guild flags (shifted E)
        (49, 34, 42, 'ybyrbb', True),    # South ford bank — fulling-mill pennant line
    ]
    for i, (yy, x_lo, x_hi, pal, sag) in enumerate(bunting_specs):
        xs = [x for x in range(x_lo, x_hi + 1)
              if (m.cls[yy, x] in 'd.tg' and not m.taken[yy, x]) or r.road_mask[yy, x]]
        if len(xs) < 4:
            continue
        x0, x1 = min(xs), max(xs)
        xm = (x0 + x1) // 2
        for x in range(x0, x1 + 1):
            y_row = yy + (1 if (sag and abs(x - xm) <= 1 and m.inb(x, yy + 1) and m.cls[yy + 1, x] in 'd.tg' and not m.taken[yy + 1, x]) else 0)
            if x in (x0, x1):
                if m.free(x, yy, 1, 1, on='.t') and not prot_wide[yy, x]:
                    m.stamp('dl_post', x, yy, mark='B')
            else:
                col_c = pal[(x - x0 + i) % len(pal)]
                m.over.append((2, x, y_row, K.P1('dl_cloth_%s%d' % (col_c, (x * 5 + y_row + i) % 2))))

    # Cloth-barge jetty in NE bend + timber footbridge across the Fourth Colour stream so Bargee (72, 26) is reachable!
    jetty = [(x, y) for x in (70, 71, 72) for y in range(cy[71] - 5, cy[71] - 1) if m.cls[y, x] == 'w']
    barge_bridge = [(x, y) for x in range(65, 72) for y in (25, 26) if m.cls[y, x] == 'w']
    r.deck += jetty + barge_bridge

    # Three riverside dye-works spillway stations on north bank: paired vats, wooden sluice chutes & timber bank aprons!
    chute_banks = []
    for ch_x, vat_nm, barrel_dx in ((23, 'pf_p_vat_r', -2), (31, 'pf_p_vat_b', 2), (38, 'pf_p_vat_y', -2)):
        bank_y = min(y for y in range(20, 48) if m.cls[y, ch_x] == 'w') - 1
        chute_banks.append((ch_x, bank_y))
        put_safe(m, vat_nm, ch_x, bank_y - 2, on='.tdg', r=2, prot=prot_wide)
        put_safe(m, vat_nm, ch_x + (1 if barrel_dx < 0 else -1), bank_y - 1, on='.tdg', r=2, prot=prot_wide)
        put_safe(m, 'df_sluice', ch_x, bank_y - 1, on='.tdg', r=1, prot=prot_wide)
        put_safe(m, 'hb_barrels', ch_x + barrel_dx, bank_y - 1, on='.tdg', r=2, prot=prot_wide)
        # Small weathered wooden wash-pier stepping 1 tile into the river edge right below each chute
        if m.inb(ch_x, bank_y + 1) and m.cls[bank_y + 1, ch_x] == 'w':
            r.deck.append((ch_x, bank_y + 1))
        if m.inb(ch_x + 1, bank_y + 1) and m.cls[bank_y + 1, ch_x + 1] == 'w':
            r.deck.append((ch_x + 1, bank_y + 1))
        if m.free(ch_x - 1, bank_y, 1, 1, on='.t') and not prot_wide[bank_y, ch_x - 1]:
            m.stamp('nr_wall_v', ch_x - 1, bank_y, mark='B')
        if m.free(ch_x + 2, bank_y, 1, 1, on='.t') and not prot_wide[bank_y, ch_x + 2]:
            m.stamp('nr_wall_v', ch_x + 2, bank_y, mark='B')

    # Lush trees on twin mossy river islets
    for ix, iy, trk in ((15, cy[15], 'tr_oak2'), (58, cy[58], 'nt_teal_a')):
        if m.can_tree(trk, ix - 1, iy - 2, on='.w'):
            m.stamp(trk, ix - 1, iy - 2, mark='B')
        else:
            put_safe(m, 'nt_pine_sh', ix - 1, iy - 1, on='.', r=2, prot=prot_wide)

    # Mossy drystone walls between dye-crop fields
    for (x0, x1, y) in ((4, 22, 51), (44, 62, 46), (12, 32, 70)):
        for x in range(x0, x1 + 1):
            if abs(x - (x0 + x1) // 2) <= 1:
                continue
            if m.free(x, y, 1, 1, on='.t') and not prot_wide[y, x] and vnoise(x, y, 5522, 3.0) > 0.25:
                m.stamp('nr_wall_' + ('w' if x == x0 else 'e' if x == x1 else 'm'), x, y, mark='B')

    CK.props(r, ['nt_boulder', 'nt_rocks_s0', 'nt_rocks_s1', 'nt_log', 'nt_stump'], 28, box=(0, 0, W, H), clump=3, seed=7)
    CK.fringe(r, CK.FRINGE['meadow'], 175, seed=1, near_forest=5)
    CK.fringe(r, ['tr_pink', 'nt_blossom', 'nt_teal_a'], 24, box=(2, 22, 78, 70), seed=2, near_forest=0)
    CK.undergrowth(r, 240, seed=3)

    # ---- 7. Paint + Dense Forest Infill, Ground Depth, Clean Animated River, Lotus & Warm Lantern Glows ----
    r.paint(glint=0.25)
    CK.paint_extras(r)
    infill_forest(r, VALLEY_WOODS, scale=10.0, seed=552)
    paint_forest_ground_depth(m, seed=552, clearings=[(51, 16, 6, 4, 'worn'), (39, 51, 4, 3, 'worn'), (28, 28, 8, 2.5, 'worn')], dark=0.46)
    CK.boardwalks(r, r.deck)

    # Dye the madder/woad/weld tall grass patches (authentic crop meadows on land!)
    T_dye = {k: K._ST['_dyegrass']['tall_' + k] for k in 'rby'}
    for k, msk in dyemask.items():
        for y, x in np.argwhere(msk & (m.cls == 't')):
            m.L[1, y, x] = T_dye[k]

    # Clean animated river water flows uninterrupted (ZERO opaque flat dye squares on top of water!).
    # Add natural river shoreline stones & subtle current ripples near the 3 bankside dye chutes.
    rng_sh = random.Random(5529)
    for ch_x, bank_y in chute_banks:
        for dx, dy in ((-2, 2), (2, 2), (0, 3), (3, 2)):
            rx, ry = ch_x + dx, bank_y + dy
            if m.inb(rx, ry) and m.cls[ry, rx] == 'w' and m.L[1, ry, rx] == 0 and m.L[2, ry, rx] == 0:
                if rng_sh.random() < 0.7:
                    m.L[2, ry, rx] = K.P1('cs_wrock%d' % ((rx + ry) % 3))

    # Lotus lilies on SE sheep-wash pond & calm river backwaters across the full clean channel!
    dress_water_lotus(m, prob=0.14, seed=552)
    # Moored boats & river boulders
    m.L[2, 29:35, 73:79] = 0
    water_prop_stamp(m, 'hb_boat2', 74, 30, water_cls='w')
    m.L[2, 29:35, 4:10] = 0
    water_prop_stamp(m, 'hb_boat1', 5, 31, water_cls='w')
    for bx, by in ((10, 34), (27, 36), (48, 37), (63, 35), (71, 58)):
        water_prop_stamp(m, 'nt_boulder', bx, by, water_cls='w')

    # Bleachfield white flowers, valley flower meadows, petals & glowing mushrooms
    CK.meadow(r, 60, 3, 4.5, 2.2, tiles=[K.DECOR_SH['flowers'][2], K.DECOR_SH['flowers'][11]], p=0.92, seed=1)
    for i, (cx_, cy_, rx, ry) in enumerate(((20, 24, 5, 2), (55, 25, 5, 2), (8, 22, 3, 2), (28, 48, 4, 1.5), (68, 46, 3, 2), (46, 68, 4, 2))):
        CK.meadow(r, cx_, cy_, rx, ry, p=0.68, seed=i + 3)
    scatter_petals_and_mushrooms(
        m,
        spots_petals=[(40, 6, 5, 3, 0.25), (34, 28, 5, 3, 0.22), (62, 27, 4, 2.5, 0.24), (24, 52, 4, 3, 0.20)],
        spots_mush=[(14, 15, 3.0, 5), (22, 26, 2.8, 5), (65, 47, 3.0, 5)],
        seed=552,
    )
    add_warm_glows(m, glow_pts + [(51, 18), (68, 26)])
    add_water_glints(m, water_cls='w', seed=552, density=0.035)
    CK.scatter_quiet(r, 14)

    # Seal all perimeter edges strictly except N (39..42 -> 540) and S (38..41 -> 541)!
    seal_unconnected_edges(
        m,
        open_cells=[(x, 0) for x in range(39, 43)] + [(x, H - 1) for x in range(38, 42)],
        filler=P1('nt_bush0'),
    )
    write_wave13_map(m, 552, "# The Dyers' Ford (552). WRITTEN BY layouts/wave13_routes_craft.py (Wave 13 Rejuv V14 Craft).\n")
    return m


# =============================================================================
# 6. MAP 560: FROSTFLAT CAUSEWAY (64x30, ts 52 PF Rejuv Snow)
# =============================================================================
def build_560():
    """Frostflat Causeway (64x30, ts 52): sweeping arctic coastal causeway linking Frostwick (N col 2..4)
    to Saltmere (E row 12..14) and The Rehearsal (S warp 30, 29). Staggered multi-headland shs3 coastal
    escarpment, smooth curved NE brine lagoon & NW frost-pan (zero comb teeth or rectangular trenches),
    deep-sea & pine-headland north border (zero uniform top-row boulder fence), Customs Chain at x=34."""
    W, H = 64, 30
    hspec = head_spec(560)
    evs = hspec['events']
    m = snowmap(W, H, 560, kit='shs3')

    def emb_at(x):
        if x <= 7:
            return 16
        if x <= 16:
            return 14
        if x <= 26:
            return 16
        if x <= 38:
            return 15
        if x <= 45:
            return 13
        if x <= 54:
            return 15
        return 16

    # ---- 1. Organic Coastlines, Deep-Sea North Rim & Staggered Headland Escarpment ----
    for x in range(W):
        # Taper north coast cleanly east of the N pine headland (x>=10) to avoid any vertical trench at x=7..8
        if x < 10 or x >= 59:
            top = -1
        else:
            taper = min(1.0, (x - 9) / 4.5, (59 - x) / 4.5)
            top = int(round((1.5 + 1.0 * math.sin(x / 6.5) + 0.9 * vnoise(x, 0, 5601, 5.0)) * taper))
        bot = 26 - int(round(1.3 * math.sin(x / 8.0 + 1.8) + 1.3 * vnoise(x, 0, 5602, 5.5)))
        emb = emb_at(x)
        for y in range(H):
            if y <= emb:
                m.ht[y, x] = 1
            if top >= 0 and y <= top:
                m.cls[y, x] = 'W' if (y == 0 or (y == 1 and top >= 2 and x % 5 != 0)) else 'o'
            if y >= bot and not (28 <= x <= 32):
                m.cls[y, x] = 'W' if y == H - 1 and bot <= H - 2 else 'o'
    RW.lagoon(m, 0.42, seed=560)
    # Keep y=0 north sea strictly deep impassable water 'W' (zero uniform boulder fence!)
    for x in range(10, 59):
        m.cls[0, x] = 'W'
        if m.cls[1, x] == 'o' and vnoise(x, 1, 5608, 4.0) > 0.48:
            m.cls[1, x] = 'W'
    for x in range(W):
        if m.cls[H - 1, x] == 'o' and not (28 <= x <= 32):
            m.cls[H - 1, x] = 'W'

    # Keep N exit (x=2..4) and E exit (y=12..14) clean & open
    for y in range(0, 14):
        for x in range(2, 5):
            m.cls[y, x] = 'd'
            m.ht[y, x] = 1

    # Three crisp flights of timber steps aligned cleanly with the staggered headland escarpment
    for sx in (11, 29, 49):
        m.stairs(sx, emb_at(sx), w=3, kit_rows=3)
    m.plan_cliffs()

    # ---- 2. Gently Curving Causeway Road, South Spur to Rehearsal & Organic Flats ----
    for x in range(W):
        emb = emb_at(x)
        # Keep causeway road cleanly north of cliff lip while meeting E exit (12..14) & Customs chain (34, 11..14)
        y1 = min(14, emb - 1)
        y0 = max(10, y1 - 2)
        if 31 <= x <= 36:
            y0, y1 = 11, 14
        elif x >= 58:
            y0, y1 = 12, 14
        for y in range(y0, y1 + 1):
            if m.cls[y, x] in '.o' and not m.cliff[y, x]:
                m.cls[y, x] = 'd'
    # Smooth diagonal road transitions at headland bends
    for bx in (7, 8, 16, 17, 26, 27, 38, 39, 45, 46, 54, 55):
        for y in range(11, 15):
            if m.cls[y, bx] == '.' and not m.cliff[y, bx]:
                m.cls[y, bx] = 'd'
    # Spur south to the drowned pier warp (30, 29)
    m.rect(29, 18, 3, 8, 'd', only='.o')
    for y in range(19, H):
        if m.cls[y, 30] in 'oIW.' and y >= 24:
            for x in (29, 30, 31):
                m.cls[y, x] = 'D'
    m.lane([(12, 17), (13, 21), (18, 22)], 'd', 2.0, seed=4, only='.')
    m.lane([(50, 18), (50, 21), (44, 22)], 'd', 2.0, seed=5, only='.')
    m.lane([(30, 21), (26, 21)], 'd', 1.8, seed=6, only='.')
    m.lane([(30, 21), (36, 21), (42, 21)], 'd', 1.8, seed=7, only='.')

    # Organic curved NW frost-pan (ZERO vertical rectangular trench!) & smooth crescent NE brine lagoon (ZERO comb teeth!)
    for cx, cy, rx, ry, sd in (
        (11.5, 6.2, 3.8, 2.0, 51), (16.0, 5.8, 3.0, 1.7, 52), (14.2, 7.6, 2.8, 1.4, 53),
    ):
        m.blob(cx, cy, rx, ry, 'p', seed=sd, only='.', rough=0.32)
    for cx, cy, rx, ry, sd in (
        (44.8, 5.8, 4.4, 2.1, 561), (49.8, 6.0, 4.4, 2.0, 562), (47.5, 7.5, 3.8, 1.6, 563),
    ):
        m.blob(cx, cy, rx, ry, 'w', seed=sd, only='.', rough=0.28)
    # First slide frost-pan on SW flat (with stoppers at 14,23 & 18,22!)
    m.blob(15.0, 23.0, 6.2, 2.3, 'p', seed=21, only='.', rough=0.35)
    smooth_cls(m, 'p', into='.', passes=2)
    smooth_cls(m, 'w', into='.', passes=2)
    # Keep item (56, 6), item (3, 8), surveyor (20, 6), trainer (48, 10) cleanly on walkable dry shore!
    for gx, gy in ((56, 6), (55, 6), (56, 7), (55, 7), (57, 6), (3, 8), (20, 6), (48, 10)):
        if m.cls[gy, gx] in 'wp':
            m.cls[gy, gx] = '.'

    # Frosted sedge tall-grass encounter pockets (eroded organically!)
    for cx, cy, rx, ry in (
        (26, 5.5, 3.2, 1.6), (34, 6.0, 3.4, 1.5), (10, 9.5, 2.6, 1.2), (59, 6.5, 2.2, 1.4),
        (40, 21.5, 3.0, 1.5), (56.5, 20.5, 2.8, 1.6), (6.5, 20.5, 2.2, 1.3), (23.0, 20.0, 2.2, 1.1),
    ):
        m.blob(cx, cy, rx, ry, 't', seed=int(cx + cy * 3), only='.', rough=0.65)
    erode_snow_grass_organic(m, seed=560)

    # Natural forest windbreak borders & north-coast pine capes (x=0..1, 5..9, 59..63 — replaces top boulder fence!)
    for y in range(H):
        for x in range(W):
            if m.cls[y, x] != '.' or m.cliff[y, x]:
                continue
            if x <= 1 and y >= 15:
                m.cls[y, x] = 'T'
            if x <= 1 and y < 11:
                m.cls[y, x] = 'T'
            if 5 <= x <= 9 and y <= 2:
                m.cls[y, x] = 'T'
            if x >= 59 and y <= 3:
                m.cls[y, x] = 'T'
            if x >= W - 2 and (y < 10 or y > 17):
                m.cls[y, x] = 'T'

    # ---- 3. Lock ALL 20 Exact HEAD Events & Signposts ----
    for e in evs:
        ex, ey = e['at']
        if m.cls[ey, ex] in 'oWT':
            m.cls[ey, ex] = 'd' if e['name'].startswith('Customs chain') else '.'
    # Ensure walk corridor on S warp (30, 29) & E/N seams
    m.cls[28:30, 29:32] = 'D'
    prot_wide = reserve_events(m, evs, radius=1, extra=[(2, 0), (3, 0), (4, 0), (W - 1, 12), (W - 1, 13), (W - 1, 14),
                                                        (30, 28), (30, 29), (14, 23), (18, 22), (56, 6), (55, 6), (56, 7)])
    prot_strict = reserve_events(m, evs, radius=0)
    paint_signposts(m, evs, skip_names=('Border Stones',))

    # ---- 4. Border Stones, Salt-Wagon Wreck, Survey Pegs, Railings & Kristiline Conifers ----
    m.stamp('fw_stone', 30, 9)
    m.stamp('fw_stone', 36, 9)
    glow_pts = []
    # Overturned salt wagon (HEALPOWDER 45, 23) + coastal causeway props
    for nm, x, y in (
        ('sh_crates', 44, 19), ('pf_barricade', 46, 21), ('fw_sled', 47, 19),
        ('fw_rack', 38, 9), ('fw_wood', 57, 10), ('fw_skull', 14, 9),
        ('pf_lantern', 27, 9), ('pf_lantern', 39, 8), ('pf_lantern', 32, 24), ('pf_lantern', 5, 10),
        ('fw_sled', 7, 10), ('sh_crates', 60, 8), ('fw_brazier', 41, 9), ('fw_brazier', 32, 10),
        ('wr_sacks', 43, 21), ('hb_barrels', 52, 19), ('pf_whalebone', 25, 23),
    ):
        res = put_safe(m, nm, x, y, on='.td', r=2, prot=prot_wide)
        if res and nm in ('pf_lantern', 'fw_brazier'):
            glow_pts.append((res[0], res[1] + (1 if nm == 'pf_lantern' else 0)))

    # Causeway north verge rope-and-post railing with clean lay-by gaps following staggered road
    for x0, x1 in ((6, 9), (14, 17), (23, 26), (51, 57)):
        for x in range(x0, x1 + 1):
            vy = max(9, min(11, emb_at(x) - 4))
            if m.free(x, vy, 1, 1, on='.') and not prot_wide[vy, x] and not m.cliff[vy, x]:
                m.stamp('fw_pal_h', x, vy, mark='B')

    # Meridian survey pegs across the flats
    for x, y in ((5, 5), (9, 5), (17, 7), (22, 4), (25, 9), (37, 4), (54, 4), (55, 19), (36, 20), (20, 19), (8, 19)):
        if m.free(x, y, 1, 1, on='.t') and not prot_wide[y, x] and not m.cliff[y, x]:
            m.stamp('fw_peg', x, y)

    # Dense Kristiline conifer windbreak groves (STRICTLY off cliff faces!)
    for idx, (cx, cy, cnt, rad, hero) in enumerate((
        (3, 22, 4, 2.4, False), (27, 4, 3, 2.2, True), (37, 5, 3, 2.2, False),
        (60, 8, 3, 2.0, False), (59, 23, 3, 2.2, True), (37, 23, 3, 2.0, False),
        (23, 24, 2, 1.8, False), (15, 19, 2, 1.6, False), (52, 23, 2, 1.8, False),
        (7, 3, 3, 1.8, False),
    )):
        place_snow_grove(m, cx, cy, count=cnt, radius=rad, on='.t', seed=560 + idx, hero=hero, prot=prot_wide)

    r_stub = type('RStub', (), {'m': m, 'W': W, 'H': H, 'seed': 560})()
    CK.woods(r_stub, ALPINE_WOODS, scale=8.0)

    # ---- 5. Paint + Ice, Timber Boardwalk, Crystalline Glacial Turf & Warm Glows ----
    m.paint()
    RW.ice(m)
    infill_winter(r_stub, ALPINE_WOODS, scale=8.0, seed=560)

    # Boardwalk planks over the south lagoon spur down to The Rehearsal warp (30, 29)
    for y in range(19, H):
        for i, x in enumerate((29, 30, 31)):
            if m.cls[y, x] == 'D':
                m.L[1, y, x] = C('ak', 1524 + i)
    # Ice slide stoppers on SW frost-pan
    for x, y in ((14, 23), (18, 22)):
        if m.cls[y, x] == 'p':
            m.L[1, y, x] = 10371
    # Crystalline salt crust & shimmer strictly on INTERIOR NE evaporation lagoon cells (crisp icy rims!)
    for y, x in np.argwhere(m.cls == 'w'):
        if all(m.inb(x + dx, y + dy) and m.cls[y + dy, x + dx] == 'w' for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            if vnoise(x, y, 61, 2.0) > 0.52:
                m.L[1, y, x] = ice_at(x, y)
    # Clustered sea-ice boulders & rocky skerries framing the north & south lagoons (natural clusters, NOT a straight line!)
    for nm, x, y in (
        ('nt_boulder', 16, 1), ('nt_boulder', 18, 2), ('nt_boulder', 33, 1),
        ('nt_boulder', 47, 1), ('nt_boulder', 49, 2), ('nt_boulder', 10, 27),
        ('nt_boulder', 45, 27), ('nt_boulder', 58, 26),
    ):
        water_prop_stamp(m, nm, x, y, water_cls='oIW')

    # Wind-swept snow drift variation across the flats!
    paint_snow_turf_layering(m, seed=560, cer_thr=0.59, peri_thr=0.67)
    # Subtle crystal outcrops near the salt-works & frost-pans
    for cx, cy, sp in ((39, 7, KF_CRYS_MONO), (58, 7, KF_CRYS_STAR), (8, 8, KF_CRYS_BLADES), (34, 22, KF_CRYS_MONO)):
        put_sprite(m, cx, cy, sp[0], sp[1], on='.', avoid_mask=prot_wide, post_paint=True)

    m.scatter(14, seed=560)
    RW.icy_faces(m, 0.65, seed=560)
    RW.dress_ice(m, 0.70, seed=560)
    RW.reed_beds(m, 14, seed=561)
    RW.road_tracks(m, 0.12, seed=560)
    RW.drifts(m, 0.06, seed=560)
    add_warm_glows(m, glow_pts + [(33, 12), (30, 26)])
    add_water_glints(m, water_cls='w', seed=560, density=0.05)

    # Seal any remaining stray perimeter edges with varied frosted shrubs/boulders (deep water 'W' already seals N sea!)
    seal_unconnected_edges(
        m,
        open_cells=[(2, 0), (3, 0), (4, 0), (W - 1, 12), (W - 1, 13), (W - 1, 14), (30, H - 1)],
        filler=(10551, 10371, 9872, 9888),
    )
    write_wave13_map(m, 560, '# Frostflat Causeway (560). WRITTEN BY layouts/wave13_routes_craft.py (Wave 13 Rejuv V14 Craft).\n')
    return m


# =============================================================================
# 7. MAP 568: THE REHEARSAL (34x26, ts 56 PF Rejuv Shore, :BLEED)
# =============================================================================
def build_568():
    """The Rehearsal (34x26, ts 56): intimate twilight Bleed Veil stage where 5 seconds of a salt-wagon
    crash replay forever. Dense overhanging purple/dead/alpine Bleed canopy (ZERO thin green oak row!),
    organic curved shoreline & drowned pier village (ZERO water-backed reed glitches on grass, ZERO green
    square floating in the sea!), sculptural crystalline salt flat with prism spires & Bleed Veil shafts,
    and 100% locked D8_FRAME gust-wall gate sealing TM10 (31, 9) on frame 0."""
    W, H = 34, 26
    hspec = head_spec(568)
    evs = hspec['events']
    r = Route(568, W, H, 'shore', kit={1: 'akc', 'default': 'akc'}, base='.')
    m = r.m

    # ---- 1. Organic Sinuous Shoreline & Drowned Pier Inlet ----
    for x in range(W):
        for y in range(H):
            coast = (20.8 + 1.4 * math.sin(x / 3.8) + 1.1 * (vnoise(x, 0, 5681, 4.5) - 0.5) * 2
                     - (2.0 if x > 18 else 0.0) - (2.6 if x > 25 else 0.0))
            # Guarantee y>=16 at x=23 & x=26 is sea so Frame-0 gust wall at x=23, y=2..15 NEVER leaks!
            if 22 <= x <= 27:
                coast = min(coast, 16.0)
            if y >= coast:
                m.cls[y, x] = 'W' if y >= coast + 3.0 else 'w'
            elif y >= coast - 1.2:
                m.cls[y, x] = 's'
    for y in range(17, H):
        for x in range(0, 10):
            if m.cls[y, x] == '.' and y >= 19.2 + 1.3 * vnoise(x, y, 5682, 3.0):
                m.cls[y, x] = 'w'
    CK.smooth_sea(m, 1)
    # Hard lock sea cells at x=23, y=16..25 and x=26, y=16..25 so gust walls seal cleanly to the sea
    for x in (22, 23, 26):
        for y in range(16, H):
            if m.cls[y, x] not in 'wW':
                m.cls[y, x] = 'w'

    # ---- 2. Organic Sculpted Salt Flat (E, frozen mid-gust) ----
    for y in range(2, 16):
        for x in range(17, W):
            edge_x = 18.2 + 1.6 * math.sin(y / 2.6) + 1.2 * (vnoise(0, y, 5683, 3.5) - 0.5) * 2
            if m.cls[y, x] in '.s' and x >= edge_x:
                m.cls[y, x] = 'S'
    # Guarantee gust wall columns x=23 and x=26 (y=2..15) and TM10 (31,9) & Stardust (29,4) are clean salt flat 'S'
    for y in range(2, 16):
        m.cls[y, 23] = 'S'
        m.cls[y, 26] = 'S'
    for x in range(27, 33):
        for y in range(3, 14):
            if m.cls[y, x] == '.':
                m.cls[y, x] = 'S'

    # ---- 3. Old Salt Road (Veil -> Tipped Wagon -> Drowned Pier) ----
    road = [(16, 0), (16, 4), (14.5, 8), (12.5, 11), (10, 15), (7, 18), (5, 20)]
    r.road(road, w=3.0, open_=None, only='.tTSs')
    r.lane([(17, 6), (20, 8), (22, 9)], w=2.0, c='d', open_=None, only='.tS')
    r.exit('N', 15, 3)
    # Weathered drowned pier planks (x=3..5, y=20..25) — pier gust walls sit at y=22 & y=24, Bleed Shard at (4, 25)!
    for x in range(3, 6):
        for y in range(20, 26):
            m.cls[y, x] = 'w'
            r.deck.append((x, y))

    # Dense twilight Bleed forest rim on N (y=0..1, sealing x=23 north!) and W (x=0..2)
    for y in range(0, 2):
        for x in range(W):
            if not (15 <= x <= 17):
                m.cls[y, x] = 'T'
    for y in range(0, 18):
        for x in range(0, 3):
            if m.cls[y, x] == '.':
                if x <= 1 or vnoise(x, y, 5689, 3.0) > 0.42:
                    m.cls[y, x] = 'T'
    # Extra haunted grove pocket in NW corner framing the onlookers
    m.blob(3.5, 4.5, 2.8, 2.2, 'T', seed=5688, rough=0.35, only='.')
    r.finish_plan(border=0)

    # Organic bleached tall-grass pockets (keeping road, onlookers & wagon completely clean!)
    CK.grass_fields(r, [(8, 13.5, 3.2), (12.5, 16.5, 2.8), (4.5, 12, 2.4), (15.5, 14, 2.2)])

    # ---- 4. Lock ALL 58 Exact HEAD Events (Zero Collisions!) ----
    for e in evs:
        ex, ey = e['at']
        if m.cls[ey, ex] == 'T' and (ex, ey) != (0, 0):
            m.cls[ey, ex] = 'd' if ex < 18 else 'S'
    prot_exact = reserve_events(m, evs, road_mask=r.road_mask, radius=0, extra=[(16, 0), (16, 1), (4, 25)])
    # Keep gust columns (x=23, x=26, y=2..15) and walkway corridors around them strictly clear of solid props
    gust_pad = [(x, y) for x in (22, 23, 24, 25, 26, 27) for y in range(2, 16)] + [(x, y) for x in range(3, 6) for y in range(19, 26)]
    prot_props = reserve_events(m, evs, radius=1, extra=gust_pad)
    paint_signposts(m, evs)

    # ---- 5. Haunted Bleed Woodland Canopy (Purple/Dead/Dark-Pine — ZERO uniform green oak row!) ----
    bleed_woods = [
        {'purp': 5, 'blue': 3, 'teal2': 2},
        {'blue': 4, 'purp': 4, 'silk1': 2},
        {'purp': 4, 'teal2': 3, 'sh1': 2, 'blue': 2},
    ]
    CK.woods(r, bleed_woods, scale=6.0)

    # ---- 6. Landmarks: Drowned House, Tipped Wagon, Prism Crystal Formations & Salt Spires ----
    put_safe(m, 'sh_small', 0, 12, on='.tsT', r=2, prot=prot_exact)
    if m.free(9, 10, 3, 2, on='.dtg') and not prot_exact[10:12, 9:12].any():
        m.stamp('pf_wagon', 9, 10, mark='B')
    else:
        put_safe(m, 'pf_wagon', 9, 10, on='.dtg', r=2, prot=prot_exact)

    # Luminous Bleed crystal formations framing the Veil, wheel-rut, onlookers & salt-flat edge!
    for nm, x, y in (
        ('cr_pink_t', 13, 2), ('cr_pink_c', 19, 2), ('cr_purple_e', 11, 3), ('cr_pink_e', 18, 2),
        ('cr_teal_c', 10, 12), ('cr_pink_c', 15, 13), ('cr_purple_c', 6, 15), ('cr_clear_t', 20, 12),
        ('cr_pink_t', 30, 13), ('cr_teal_e', 32, 3), ('cr_pink_c', 28, 7), ('cr_clear_c', 20, 5),
        ('cr_purple_t', 4, 8), ('cr_pink_c', 5, 6), ('cr_purple_e', 31, 11), ('cr_teal_c', 29, 2),
        ('cr_pink_e', 18, 15), ('cr_clear_c', 14, 18),
    ):
        put_safe(m, nm, x, y, on='.tgSs', r=2, prot=prot_props)

    # Subtle salt-mound piles & weathered driftwood (ZERO ugly rectangular brp/brx wall boxes!)
    CK.props(r, ['hb_salt0', 'hb_salt1', 'hb_salt2'], 7, box=(19, 3, 33, 15), on='S', clump=1, seed=568)
    CK.props(r, ['nt_rocks_s0', 'ck_pebbles', 'nt_stump', 'nt_log'], 8, box=(2, 3, 18, 19), clump=1, seed=6)
    # Atmospheric twisted/purple fringe trees in NW & S meadow (strictly off dry grass reeds!)
    for nm, x, y in (('nt_tree_purp', 6, 2), ('nt_deadtree', 4, 3), ('nt_pine_purp', 2, 7), ('nt_birch_v', 10, 4)):
        put_safe(m, nm, x, y, on='.t', r=2, prot=prot_props)
    # Dry-land undergrowth ONLY (ferns, dark bushes — NEVER nt_reed0/1 on grass!)
    CK.undergrowth(r, 85, kinds=('nt_fern1', 'nt_bush1', 'nt_shrub1'), seed=568)
    for i, (cx, cy, rx, ry) in enumerate(((5, 8, 3, 2), (14, 16, 3, 2), (3, 15, 2, 2), (11, 5, 2, 1.5))):
        CK.meadow(r, cx, cy, rx, ry, tiles=[K.DECOR_SH['flowers'][k] for k in (8, 9, 10)], p=0.58, seed=i)

    # ---- 7. Paint + Canopy Infill, Ground Depth, Salt Crust, Wet Shore, Pier Pilings & Ethereal Shafts ----
    r.paint(glint=0.22)
    CK.paint_extras(r)
    infill_forest(r, bleed_woods, scale=6.0, seed=568)
    paint_forest_ground_depth(m, seed=568, clearings=[(11, 10, 4, 3, 'worn')], dark=0.52)

    # Sculpted crystalline salt crust across the eastern salt flat
    CK.crust_ground(r, [(x, y) for y, x in np.argwhere((m.cls == 'S') | ((m.cls == 'B') & (m.under == 'S')))])
    # Damp wet-sand sheen along shoreline & drowned pier edge
    wet_t = P1('cs_wet_c') if 'cs_wet_c' in STAMPS else None
    if wet_t:
        for y in range(1, H - 1):
            for x in range(1, W - 1):
                if m.cls[y, x] in 's.' and m.L[1, y, x] == 0:
                    if any(m.cls[y + dy, x + dx] in 'wW' for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                        m.L[1, y, x] = wet_t
    CK.boardwalks(r, r.deck)

    # Bleed Veil ethereal shimmer & frozen salt spray drifts
    rng = random.Random(568)
    for y in range(1, 5):
        for x in range(13, 20):
            if m.L[2, y, x] == 0 and not prot_exact[y, x] and m.cls[y, x] != 'B':
                m.L[2, y, x] = K.P1('bl_veil%d' % ((x + y) % 2))
    for y, x in np.argwhere(m.cls == 'S'):
        if m.L[2, y, x] == 0 and not prot_exact[y, x] and rng.random() < 0.28:
            m.L[2, y, x] = K.P1('bl_gust%d' % rng.randrange(3))
    for y, x in np.argwhere(np.isin(m.cls, ['.', 'g'])):
        if m.L[2, y, x] == 0 and not prot_exact[y, x] and vnoise(x, y, 5684, 3.0) > 0.72:
            m.L[2, y, x] = K.P1('bl_veil%d' % ((x * 3 + y) % 2))

    # Drowned village pilings, half-sunk skiff, sea-rocks & kelp cleanly over open water (ZERO grass box in sea!)
    for nm, x, y in (
        ('hb_posts3', 6, 22), ('hb_posts2', 1, 21), ('hb_post1', 7, 20), ('hb_post1', 10, 22),
        ('hb_boat3', 0, 23), ('nt_boulder', 13, 23), ('nt_boulder', 22, 20), ('ak_rock2', 28, 19),
    ):
        water_prop_stamp(m, nm, x, y, water_cls='wW', skip_cells=r.deck)

    # Ethereal light shafts piercing the Bleed Veil + glowing twilight mushrooms + eerie soft lantern glows!
    for sx_, sy_ in ((15, 0), (17, 1), (29, 7)):
        put_overlay_stamp(m, 'cv_shaft', sx_, sy_, z=2)
    scatter_petals_and_mushrooms(
        m,
        spots_petals=[(16, 4, 4, 2.5, 0.25), (12, 12, 4, 2.5, 0.20)],
        spots_mush=[(6, 5, 2.5, 5), (5, 14, 2.2, 4)],
        seed=568,
    )
    add_warm_glows(m, [(16, 1), (11, 10), (5, 20), (4, 25), (31, 9)])
    add_water_glints(m, water_cls='wW', seed=568, density=0.04)
    CK.scatter_quiet(r, 18)

    # Seal east salt-flat edge (x=33, y=2..15) with pale frost stones (19232, pas=15) instead of green bushes on salt!
    for y in range(2, 16):
        if m.cls[y, W - 1] in 'Ss.':
            m.L[2, y, W - 1] = 0
            m.L[1, y, W - 1] = 19232
    # Seal ALL stray perimeter edges strictly except Bleed Veil warp (16, 0) and Bleed Shard pier end (4, 25)!
    seal_unconnected_edges(m, open_cells=[(16, 0), (4, 25)], filler=P1('nt_bush0'))
    write_wave13_map(m, 568, '# The Rehearsal (568, :BLEED). WRITTEN BY layouts/wave13_routes_craft.py (Wave 13 Rejuv V14 Craft).\n')
    return m


# =============================================================================
# 8. MAP 561: GULLCRY CLIFFS (64x130, ts 52 PF Rejuv Snow)
# =============================================================================
def build_561():
    """Gullcry Cliffs (64x130, ts 52): dramatic Isenmar coastal crags from Rimewood (S col 10..13) to
    Ebbmouth (N col 10..13). Four snow-capped headlands jut over sinuous sea coves & sea stacks;
    geological fan-shaped landslide (rows 55..70) seals S from N forcing passage via Gullcry Caves
    (exact cave mouths MN=(6, 49) & MS=(6, 75)); Kestrel's tors narrow the north pass at (11, 8);
    stilt fishing hamlet with timber pier & boats in south cove; secret Gannet Stair (50, 18) to
    Cramorant rookery; blazing signal-fire headland beacon; dense Kristiline alpine conifer ridges."""
    W, H = 64, 130
    hspec = head_spec(561)
    evs = hspec['events']
    r = Route(561, W, H, 'snow', base='.', kit='shs3')
    m = r.m

    # ---- 1. Sculpted Coastal Headlands (h=1) & Inland Crags (h=2, shs3 -> cliff base at y_lip+2!) ----
    # Headlands keep exact stair faces at y=18 (Gannet), y=44 (N cove), y=100 (Hamlet) & shingle beach x=48..50 around Headland 3!
    CK.shelf(r, [(0, 0), (30, 0), (39, 3), (64, 6), (64, 18), (30, 18), (27, 24), (29, 31), (36, 33),
                 (64, 35), (64, 44), (31, 45), (29, 50), (33, 56), (42, 62), (40, 70), (30, 72),
                 (27, 78), (28, 86), (34, 90), (45, 93), (47, 100), (29, 100), (26, 106), (27, 114),
                 (31, 121), (44, 123), (46, 129), (0, 129)], 1)
    # Inland crags: bottom lip at y=47 (base y=49 -> MN=(6,49)!) and y=73 (base y=75 -> MS=(6,75)!)
    CK.shelf(r, [(0, 25), (11, 24), (14, 30), (13, 39), (12, 47), (0, 47)], 2)
    CK.shelf(r, [(0, 52), (15, 51), (19, 58), (18, 65), (14, 73), (0, 73)], 2)
    CK.shelf(r, [(0, 92), (6, 90), (9, 98), (7, 112), (0, 113)], 2)
    for hh in (1, 2):
        CK.smooth_ht(m, hh, 2)
    # Lock exact crag lips around x=5..7 so cave mouths land strictly on MN=(6,49) and MS=(6,75)!
    for cx_ in (5, 6, 7):
        m.ht[45:48, cx_] = 2
        m.ht[48:52, cx_] = 1
        m.ht[71:74, cx_] = 2
        m.ht[74:78, cx_] = 1

    # ---- 2. Organic Sinuous Ocean Shoreline & Headland Coves (ZERO straight vertical sea line!) ----
    xc = [int(round(53.0 + 2.8 * math.sin(y / 8.5) + 1.8 * math.cos(y / 4.3)
                    + 1.6 * (vnoise(0, y, 5611, 6.0) - 0.5) * 2)) for y in range(H)]
    for y in range(H):
        if 86 <= y <= 106:
            xc[y] = max(xc[y], 51)  # guarantee dry shingle beach x=48..50 around Headland 3 connecting hamlet <-> (38,80)/(34,84)!
        for x in range(W):
            if m.ht[y, x] == 0 and x >= xc[y]:
                m.cls[y, x] = 'W' if x >= xc[y] + 3 + int(2 * vnoise(x, y, 5612, 4.0)) else 'w'
    # Carve dramatic sea coves biting naturally between headlands (while keeping shingle beach x=48..50 dry!)
    for cy_c, cx_c, rx_c, ry_c in ((26, 56, 5.5, 4.0), (50, 56, 5.0, 3.5), (82, 57, 5.0, 4.0), (115, 55, 5.0, 4.5)):
        m.blob(cx_c, cy_c, rx_c, ry_c, 'w', seed=5610 + cy_c, rough=0.45, only='.')
    CK.smooth_sea(m, 1)
    # Lock shingle beach passage around Headland 3 tip (x=48..50, y=82..106)
    for y in range(82, 107):
        for x in (48, 49, 50):
            if m.ht[y, x] == 0:
                m.cls[y, x] = '.'

    # ---- 3. Hoar Road, Headland Trails, Kestrel's Tors & Fan-Shaped Landslide ----
    r.road([(11.5, 129), (13, 120), (18, 110), (17, 100), (13, 88), (16, 80), (12, 76), (6, 76)], w=3.0, open_=None)
    r.road([(6, 50), (14, 50), (19, 46), (20, 36), (18, 26), (15, 16), (12, 9), (11.5, 0)], w=3.0, open_=None)
    r.exit('S', 10, 4)
    r.exit('N', 10, 4)
    r.lane([(17, 100), (28, 96), (38, 97)], w=2.0, open_=None)
    r.lane([(38, 103), (38, 109), (44, 109), (49, 104), (49, 92), (43, 84), (35, 84)], w=2.0, open_=None)
    r.lane([(20, 36), (34, 38), (46, 40), (50, 39)], w=2.0, open_=None)
    r.lane([(15, 16), (30, 10), (44, 12), (50, 16)], w=2.0, open_=None)

    # Kestrel's tors: organic staggered pine groves + twin crag tors narrowing road cleanly at (11, 8) (NO 1-tile horizontal fence!)
    KG = (11, 8)
    r.copse(4.5, 7.5, 3.6, 3.0)
    r.copse(20.5, 9.5, 3.2, 2.4)
    for bx, by in ((8, 8), (9, 8), (10, 8), (12, 8), (13, 8)):
        if m.cls[by, bx] in '.d':
            m.cls[by, bx] = 'B'
    m.cls[KG[1], KG[0]] = 'd'
    m.cls[KG[1] - 1, KG[0]] = 'd'

    # Readable snow switchback approach trails framing the north & south sides of the diagonal rockslide!
    r.lane([(18, 49), (26, 52), (38, 54), (48, 53), (52, 52)], w=2.0, open_=None)
    r.lane([(13, 74), (22, 72), (32, 70), (39, 73)], w=2.0, open_=None)

    # ONE sculpted organic diagonal rockslide ridge (only ~3 tiles thick, clearing ~85% of the old boulder spam block!)
    # Sweeps from the west inland crag (x=13, y=58) diagonally SE into the eastern sea (x=54, y=68) -> 100% airtight GATE!
    def slide_cy(x):
        return 58.2 + 0.24 * max(0.0, x - 13.0) + 1.35 * math.sin((x - 13.0) / 7.2)

    SLIDE = (55, 72)
    slide_spine = np.zeros((H, W), bool)
    for x in range(12, W):
        yc = int(round(slide_cy(x)))
        # Airtight 3-row diagonal core (yc-1..yc+1) guarantees zero orthogonal or diagonal bypasses!
        for y in range(max(0, yc - 1), min(H, yc + 2)):
            if m.ht[y, x] <= 1 and m.cls[y, x] in '.dtw':
                m.cls[y, x] = 'B'
                slide_spine[y, x] = True
        # Organic subtle scree shoulders (sporadic ±1 tile toe rocks, NEVER a solid wall)
        if m.ht[yc, x] <= 1 and vnoise(x, yc, 5617, 3.5) > 0.62:
            for y_s in (yc - 2, yc + 2):
                if m.inb(x, y_s) and m.ht[y_s, x] <= 1 and m.cls[y_s, x] == '.' and (x, y_s) not in ((52, 52), (52, 53)):
                    if vnoise(x, y_s, 5618, 2.5) > 0.58:
                        m.cls[y_s, x] = 'B'

    # Forest windbreaks on inland crags & sheltered cliff hollows (framing switchbacks north & south of the rockslide)
    r.forest_band('W', 4, wobble=2.2)
    for cx, cy_, rx, ry in (
        (4, 10, 4.5, 6.0), (22, 122, 4.5, 3.2), (3, 82, 3.5, 5.0), (26, 92, 4.2, 2.8),
        (25, 55, 3.2, 2.2), (26, 4, 3.5, 2.8), (28, 40, 3.5, 3.0), (24, 22, 2.8, 3.0),
        (22, 80, 3.5, 2.6), (24, 110, 3.5, 3.2), (34, 71, 3.0, 2.0), (6, 20, 3.5, 3.0),
        (36, 77, 3.5, 2.5), (14, 102, 3.0, 2.5),
    ):
        r.copse(cx, cy_, rx, ry)
    # Organic frozen cove rock-pools (ice slides!)
    for cx, cy_, rx, ry, sd in (
        (40, 26, 3.6, 1.9, 1), (44, 30, 2.6, 1.5, 2), (40, 50, 3.2, 1.6, 3),
        (36, 82, 3.6, 1.7, 4), (46, 114, 2.6, 1.5, 5), (34, 116, 2.2, 1.3, 6),
    ):
        m.blob(cx, cy_, rx, ry, 'p', seed=5620 + sd, rough=0.42, only='.')

    # Clear exact HEAD event spots before finish_plan (except landslide rubble!)
    MN, MS = (6, 49), (6, 75)
    for e in evs:
        ex, ey = e['at']
        if m.cls[ey, ex] in 'T':
            m.cls[ey, ex] = 'd'
    m.cls[MN[1] + 1, MN[0]] = 'd'
    m.cls[MS[1] + 1, MS[0]] = 'd'
    r.finish_plan(border=0)

    # Three rope-and-plank headland stairs (matching crisp 3-row shs3 faces!)
    CK.stair(r, 38, 100, w=2, h=1)   # Hamlet stair
    CK.stair(r, 46, 44, w=2, h=1)    # North cove stair
    CK.stair(r, 50, 18, w=2, h=1)    # Secret Gannet Stair -> Cramorant rookery cove!

    CK.grass_fields(r, [
        (20, 116, 3.6), (22, 92, 3.2), (6, 104, 2.6), (26, 30, 3.6), (8, 16, 3.0),
        (28, 8, 3.2), (22, 50, 2.6), (38, 30, 2.6), (6, 120, 2.6), (28, 67, 2.8), (44, 57, 2.6),
    ])

    # ---- 4. Lock ALL 25 Exact HEAD Events + 3 trial_overlay anchors (15,9 Parcel rattle, 36,107 Old Asta, 44,13 Egg ledge)! ----
    prot_wide = reserve_events(
        m, evs, road_mask=r.road_mask, radius=1,
        extra=[(x, 0) for x in range(10, 14)] + [(x, H - 1) for x in range(10, 14)] +
              [(MN[0], MN[1] + 1), (MS[0], MS[1] + 1), KG, (15, 9), (36, 107), (44, 13),
               (38, 100), (39, 100), (38, 103), (39, 103), (49, 98), (49, 100), (49, 102),
               (46, 44), (47, 44), (46, 47), (47, 47), (50, 18), (51, 18), (50, 21), (51, 21),
               (52, 52), (52, 53)],
    )
    paint_signposts(m, evs)

    # Dense Kristiline alpine woods on all inland crags & hollows!
    CK.woods(r, ALPINE_WOODS, scale=9.0)

    # ---- 5. Stilt Fishing Hamlet, Signal Beacon, Whalebones, Cave Lanterns & Sculpted Landslide Ridge ----
    glow_pts = []
    for nm, x, y in (
        ('kf_flat', 32, 104), ('kf_flat', 44, 103), ('wb_hut', 38, 114),
        ('fw_rack', 36, 110), ('fw_rack', 41, 111), ('fw_boat', 48, 118),
        ('fw_boat', 50, 110), ('fw_rack', 47, 106), ('fw_wood', 42, 118),
        ('fw_brazier', 40, 108), ('fw_rack', 40, 84), ('fw_wood', 44, 78),
        ('pf_beacon', 50, 36), ('pf_whalebone', 14, 116), ('pf_whalebone', 19, 92),
        ('pf_whalebone', 22, 42), ('pf_whalebone', 20, 22), ('pf_whalebone', 16, 6),
        ('fw_skull', 24, 51), ('pf_lantern', 8, 50), ('pf_lantern', 8, 76),
        ('pf_lantern', 15, 123), ('pf_lantern', 16, 73), ('pf_lantern', 48, 39),
        ('pf_lantern', 39, 107), ('pf_lantern', 49, 17), ('fw_brazier', 13, 10),
    ):
        res = put_safe(m, nm, x, y, on='.td', r=3, prot=prot_wide)
        if res and nm in ('pf_beacon', 'fw_brazier', 'pf_lantern'):
            glow_pts.append((res[0] + (1 if nm == 'pf_beacon' else 0), res[1] + (1 if nm != 'fw_brazier' else 0)))

    # Kestrel's twin crag tors + staggered pine clusters framing (11, 8) organically
    for (x, y) in ((8, 6), (12, 6)):
        put_safe(m, 'ck_rock_big', x, y, on='.B', r=1, prot=prot_wide)
    for (x, y) in ((16, 11), (19, 8), (7, 11)):
        put_safe(m, 'ck_boulder', x, y, on='.B', r=1, prot=prot_wide)
    place_snow_grove(m, 19, 9, count=3, radius=2.2, on='.t', seed=5619, prot=prot_wide)

    # Sculpted diagonal rockslide ridge: bold 3x3 crags + 2x2 boulders + 4 Strength-style round boulders + fallen logs!
    # Step systematically along the diagonal spine so multi-tile rock masses dominate (ZERO small-snowball grid!)
    for idx, x in enumerate(range(14, 52, 3)):
        yc = int(round(slide_cy(x)))
        k = 'ck_rock_big' if idx % 2 == 0 else 'ck_boulder'
        st = STAMPS[k]
        ty = yc - st['h'] // 2
        if m.inb(x, ty) and m.inb(x + st['w'] - 1, ty + st['h'] - 1):
            if not m.cliff[ty:ty + st['h'], x:x + st['w']].any() and not prot_wide[ty:ty + st['h'], x:x + st['w']].any():
                if not m.taken[ty:ty + st['h'], x:x + st['w']].any():
                    m.stamp(k, x, ty, mark='B')
    # Secondary pass filling 2x2 boulders & 4 iconic Strength-style accent boulders along the ridge toe
    for sx_b, nm_b in ((18, 'nt_boulder'), (27, 'nt_boulder'), (36, 'nt_boulder'), (45, 'nt_boulder')):
        yb = int(round(slide_cy(sx_b))) + 1
        put_safe(m, nm_b, sx_b, yb, on='.B', r=1, prot=prot_wide)
    rr = random.Random(5615)
    for x in range(13, 53):
        yc = int(round(slide_cy(x)))
        for dy in (-1, 0, 1):
            y = yc + dy
            if not m.inb(x, y) or m.cls[y, x] != 'B' or m.taken[y, x]:
                continue
            for k in ('ck_boulder', 'fw_log_m', 'ck_pebbles', 'fw_stone'):
                st = STAMPS[k]
                if m.inb(x + st['w'] - 1, y + st['h'] - 1) and not m.taken[y:y + st['h'], x:x + st['w']].any() \
                        and not m.cliff[y:y + st['h'], x:x + st['w']].any() and not prot_wide[y:y + st['h'], x:x + st['w']].any() \
                        and all(m.cls[y + yy, x + xx] in 'B.' for yy in range(st['h']) for xx in range(st['w'])):
                    m.stamp(k, x, y, mark='B')
                    break

    # Coastal Kristiline conifer clusters along cliff-top heaths & flanking the diagonal rockslide!
    for idx, (cx, cy, cnt, rad) in enumerate((
        (16, 118, 3, 2.2), (8, 96, 3, 2.2), (17, 40, 3, 2.2), (24, 14, 3, 2.2),
        (32, 36, 3, 2.0), (18, 86, 3, 2.0), (29, 53, 3, 2.2), (42, 56, 3, 2.0), (22, 69, 3, 2.2),
    )):
        place_snow_grove(m, cx, cy, count=cnt, radius=rad, on='.t', seed=561 + idx, prot=prot_wide)

    CK.undergrowth(r, 28, kinds=('fw_stone', 'fw_drift2', 'fw_drift0'), seed=3)
    CK.props(r, ['fw_stone', 'fw_drift2', 'fw_drift0', 'fw_wood'], 18, box=(0, 0, W, H), clump=3, seed=7)

    # ---- 6. Paint + Dense Winter Canopy, Cave Mouths, Glacial Turf, Sea Stacks & Warm Glows ----
    r.paint(glint=0.0)
    CK.paint_extras(r)
    infill_winter(r, ALPINE_WOODS, scale=9.0, seed=561)

    # Match HEAD trial_overlay Parcel rattle (15, 9) exact placement by anchoring frost stone at (15, 10) with (14, 9) & (16, 9) open!
    m.L[1, 10, 15] = 10371
    m.L[1, 9, 14] = 0; m.L[2, 9, 14] = 0
    m.L[1, 9, 15] = 0; m.L[2, 9, 15] = 0
    m.L[1, 9, 16] = 0; m.L[2, 9, 16] = 0
    # Paint real cave mouths on the crag cliff faces at exact HEAD coordinates MN=(6,49) & MS=(6,75)!
    for x, y in (MN, MS):
        RW.cave_mouth(m, x, y)
    # Seal only remaining tiny uncovered seam cells strictly inside the thin diagonal spine (ZERO giant snowball grid!)
    for y, x in np.argwhere(slide_spine):
        if (x, y) in ((52, 52), (52, 53)):
            continue
        if m.L[1, y, x] == 0 and m.L[2, y, x] == 0:
            m.L[1, y, x] = 10551 if (x + y) % 2 else int(np.array(STAMPS['fw_stone']['layers']).max())
    # Ensure Kestrel's tor flank cells stay solid
    for bx, by in ((8, 8), (9, 8), (10, 8), (12, 8), (13, 8)):
        if m.L[1, by, bx] == 0 and m.L[2, by, bx] == 0:
            m.L[1, by, bx] = 10551
    m.L[1, 53, 52] = 0; m.L[2, 53, 52] = 0   # ensure south approach to Item @(52,52) is walkable

    # Stilt fishing hamlet timber boardwalk quay & smoky stove chimneys
    paint_boardwalk_strip(m, 34, 111, 46, 112, style='ak', on_cls='.d')
    for nm, x, y in (('fw_smoke_w', 40, 112), ('fw_smoke_w', 34, 102)):
        put_overlay_stamp(m, nm, x, y, z=2)

    # Sea stacks, moored fishing boats, drift ice & coastal rocks in eastern sea coves
    for nm, x, y in (
        ('ak_rock2', 56, 10), ('ak_rock2', 58, 25), ('ak_rock2', 57, 49), ('ak_rock2', 55, 84),
        ('hb_boat1', 53, 112), ('hb_boat3', 55, 118), ('fw_boat', 52, 86),
        ('nt_boulder', 54, 15), ('nt_boulder', 56, 38), ('nt_boulder', 54, 72), ('nt_boulder', 57, 104),
    ):
        water_prop_stamp(m, nm, x, y, water_cls='wW')

    rng = random.Random(561)
    for y, x in np.argwhere(m.cls == 'w'):
        if m.L[2, y, x] == 0 and not m.taken[y, x]:
            q = rng.random()
            if q < 0.06:
                m.L[2, y, x] = K.P1('cs_wrock%d' % rng.randrange(3)) if q < 0.03 else K.P1('cs_wrockb%d' % rng.randrange(2))
            elif q < 0.10:
                m.L[2, y, x] = STAMPS['fw_floe%d' % rng.randrange(2)]['layers'][1][0][0] or m.L[2, y, x]

    # Cerulean/periwinkle snow-edged coastal heath turf + icy cliff faces + glows + water glints!
    paint_snow_turf_layering(m, seed=561, cer_thr=0.62, peri_thr=0.70)
    CK.snow_ground_var(r, thr=0.48)
    RW.icy_faces(m, 0.60, seed=561)
    RW.drifts(m, 0.05, seed=561)
    RW.road_tracks(m, 0.12, seed=561)
    RW.dress_ice(m, 0.24, seed=561)
    RW.reed_beds(m, 8, seed=561)
    add_warm_glows(m, glow_pts + [(51, 38), (6, 50), (6, 76), (40, 109)])
    add_water_glints(m, water_cls='wW', seed=561, density=0.04)

    # Seal ALL stray perimeter edges strictly except N (10..13 -> 160) and S (10..13 -> 562)!
    seal_unconnected_edges(
        m,
        open_cells=[(x, 0) for x in range(10, 14)] + [(x, H - 1) for x in range(10, 14)],
        filler=10371,
    )
    write_wave13_map(m, 561, '# Gullcry Cliffs (561). WRITTEN BY layouts/wave13_routes_craft.py (Wave 13 Rejuv V14 Craft).\n')
    return m


# =============================================================================
# 9. MAP 566: SPINNERS' RISE (80x120, ts 53 PF Rejuv Wild)
# =============================================================================
def build_566():
    """Spinners' Rise (80x120, ts 53): sweeping highland switchback ascent from Briarwick (S col 38..41)
    to Frostwick Pass (N col 42..45). Four organically sculpted fell terraces with elevation gradient:
    dense emerald-blossom lower forest -> lush heather & drystone sheepfolds -> alpine pine & frost-kissed
    hill-fort summit! Plunging Sheep-Wash brook with wider lotus plunge pool & Shearing Waterfall (14, 58),
    cozy 3-cottage Shepherds' Hamlet, Fleece Cross (50, 34), Ram Race finish [47..53, 33] well within
    the HEAD 73-step limit, drove-slide jump ledges, dark-moss ground depth, wildflower bands & warm glows."""
    W, H = 80, 120
    hspec = head_spec(566)
    evs = hspec['events']
    r = Route(566, W, H, 'meadow', base='.')
    m = r.m

    # ---- 1. Sweeping Organic Fell Terraces & Rocky Tors ----
    lips = [(97, 1), (73, 2), (47, 3), (23, 4)]
    r.terraces(lips, wobble=4.5, scale=8.0)
    CK.plateau(r, 14, 40, 9, 5, 4, rough=0.45, seed=1)   # Summit crag over cold spring (W)
    CK.plateau(r, 68, 52, 7, 4, 3, rough=0.45, seed=2)   # Eastern fell tor
    for h_ in (1, 2, 3, 4):
        CK.smooth_ht(m, h_, 3)

    # ---- 2. Lush Briarwick Lower Woods -> Highland Edge Groves ----
    r.forest_band('S', 22, wobble=6.0)
    r.forest_band('W', 6, wobble=4.0)
    r.forest_band('E', 6, wobble=4.0)
    r.forest_band('N', 3, wobble=2.5)
    for cx, cy, rx, ry in (
        (22, 80, 5.2, 3.2), (62, 64, 4.5, 3.2), (12, 92, 5.5, 4.2), (70, 104, 5.5, 4.2),
        (30, 30, 3.5, 2.4), (44, 66, 3.6, 2.4), (60, 56, 3.2, 2.2), (34, 84, 3.2, 2.2),
        (70, 78, 3.2, 2.2), (58, 12, 3.5, 2.4), (24, 6, 3.5, 2.4), (66, 26, 3.4, 2.6),
        (8, 30, 3.5, 3.2), (50, 104, 3.4, 2.4), (18, 108, 4.5, 3.5), (66, 110, 4.5, 3.5),
    ):
        r.copse(cx, cy, rx, ry)

    # ---- 3. Switchback Drove Road (Preserving Exact Ram Race [47..53, 33] <= 73 Steps from [56, 78]!) ----
    road = [(39.5, 119), (40, 108), (26, 100), (24, 88), (46, 82), (58, 74), (52, 62),
            (30, 56), (26, 44), (44, 36), (50, 33), (56, 28), (48, 14), (43.5, 0)]
    r.road(road, w=3.2, open_=(2, 5))
    # Direct shepherd drove-path shortcut climbing from hamlet shelf up through (47, 47) to Fleece Cross (50, 33) (Ram Race <= 60 steps!)
    r.lane([(57, 78), (57, 70), (50, 56), (48, 47), (49, 38), (50, 33)], w=2.2, open_=None)
    # Scenic summit spur out to REPEL (70, 20)
    r.lane([(52, 16), (62, 18), (70, 20)], w=2.2, open_=None)
    r.exit('S', 38, 4)
    r.exit('N', 42, 4)
    # Keep Ram Race finish line [47..53, 33] cleanly on road/gravel!
    m.cls[32:35, 47:54] = 'd'
    stairs = []
    for yl, h_ in lips:
        xs = [x for x in range(W) if r.road_mask[yl, x]]
        if xs:
            stairs.append((min(xs) + max(0, (len(xs) - 3) // 2), yl, h_))
    # Add direct highland drove stair on lip 3 (y~47) at x=47 for the Ram Race climb!
    lip47_y = max(y for y in range(38, 56) if m.ht[y, 48] == 3)
    stairs.append((47, lip47_y, 3))
    # Shepherds' Hamlet shelf & Summit Hill-Fort Ring
    r.clearing(64, 89, 13, 6)
    r.lane([(46, 84), (58, 92)], w=2.2)
    r.clearing(40, 9, 9.5, 6.2)

    # ---- 4. Cold Spring, Organic Sheep-Wash Pool & Shearing Waterfall ----
    CK.stream(r, [(20, 46), (19, 52), (18, 58), (16, 64), (14, 70), (12, 76), (9, 84), (6, 92)], w=2.0, seed=1, only='T.t')
    # Sculpted organic sheep-wash pool (multi-lobe, zero oval stampiness!)
    m.blob(18.0, 59.0, 3.6, 2.0, 'w', seed=5662, rough=0.45, only='.tT')
    r.lane([(30, 58), (22, 60)], w=2.0)
    # Keep Shearing fall events ([13,60] Wooloo, [14,58] Waterfall, [15,61] SOFTSAND, [20,57] Sheep-wash) cleanly connected!
    for y_ in range(57, 62):
        for x_ in range(12, 17):
            if m.cls[y_, x_] in 'wT':
                m.cls[y_, x_] = '.'
    for ex, ey in ((13, 60), (14, 58), (15, 61), (20, 57)):
        m.cls[ey, ex] = '.'
    FALL = None
    for x in range(6, 22):
        for y in range(62, 90):
            if m.cls[y, x] == 'w' and m.ht[y, x] == 2 and m.ht[y + 1, x] < 2:
                FALL = (x, y)
                break
        if FALL:
            break
    if FALL:
        fx, fy = FALL
        for y in range(fy - 3, fy + 8):
            for x in range(fx - 2, fx + 4):
                if m.cls[y, x] == 'w':
                    m.cls[y, x] = '.'
            m.cls[y, fx] = m.cls[y, fx + 1] = 'w'
        for y in range(fy, fy + 4):
            m.cls[y, fx] = m.cls[y, fx + 1] = '.'
        # Organic plunge pool at waterfall base
        m.blob(fx + 0.5, fy + 6.0, 2.8, 1.8, 'w', seed=5665, rough=0.38, only='.t')

    for e in evs:
        ex, ey = e['at']
        if m.cls[ey, ex] == 'T':
            m.cls[ey, ex] = '.'
    r.finish_plan(border=0)
    for sx, yl, h_ in stairs:
        CK.stair(r, sx, yl, w=3, h=h_)
    # Stepping stones across the sheep-wash brook at y=58..59 connecting Wooloo (13,60), Waterfall (14,58) & SOFTSAND (15,61)!
    wash_stones = [(x, 58) for x in range(15, 22) if m.cls[58, x] == 'w'] + [(x, 59) for x in range(15, 22) if m.cls[59, x] == 'w']
    if FALL:
        CK.waterfall(r, fx, fx + 1, fy)
        wash_stones += [(fx, fy + 5), (fx + 1, fy + 6)] if m.cls[fy + 6, fx + 1] == 'w' else [(fx, fy + 5)]
    if wash_stones:
        CK.stones(r, sorted(set(wash_stones)))

    # One-way drove-slide jump ledges where the switchback doubles back
    for x0, x1, y in ((30, 40, 66), (46, 56, 42), (60, 70, 82), (28, 36, 92)):
        if all(m.ht[y, x] == m.ht[y, x0] and m.cls[y, x] in '.t' and not r.road_mask[y - 1:y + 2, x].any() for x in range(x0, x1 + 1)):
            CK.ledge(r, x0, x1, y)

    CK.grass_fields(r, [
        (32, 104, 4.0), (54, 98, 3.6), (16, 84, 3.2), (40, 74, 4.0), (64, 72, 3.2),
        (40, 60, 3.6), (60, 46, 3.2), (30, 40, 3.2), (58, 20, 3.6), (26, 16, 3.2), (70, 34, 3.2),
    ])

    # ---- 5. Lock ALL 26 Exact HEAD Events & Signposts ----
    prot_wide = reserve_events(
        m, evs, road_mask=r.road_mask, radius=1,
        extra=[(x, 0) for x in range(42, 46)] + [(x, H - 1) for x in range(38, 42)] +
              [(x, 33) for x in range(47, 54)],
    )
    paint_signposts(m, evs)

    # Elevation-graded highland woods! (Lush blossom lower -> deep emerald/pine mid -> alpine spruce summit!)
    def pick_566_pal(x, y):
        if y > 82:
            return HIGHLAND_LOW_WOODS[int(vnoise(x, y, 5661, 10.0) * len(HIGHLAND_LOW_WOODS) * 0.999)]
        if y > 38:
            return HIGHLAND_MID_WOODS[int(vnoise(x, y, 5662, 10.0) * len(HIGHLAND_MID_WOODS) * 0.999)]
        return HIGHLAND_TOP_WOODS[int(vnoise(x, y, 5663, 10.0) * len(HIGHLAND_TOP_WOODS) * 0.999)]

    CK.woods(r, HIGHLAND_LOW_WOODS, scale=11.0, pick=pick_566_pal, accents={'blossom': 0.015})

    # ---- 6. Shepherds' Hamlet Cottages, Fleece Cross, Hill-Fort Ring, Sheepfolds & Warm Lanterns ----
    glow_pts = []
    for n, x, y in (('gl_cot', 52, 82), ('sh_small', 62, 83), ('sh_cot', 68, 83)):
        put_safe(m, n, x, y, on='.t', r=5, prot=prot_wide)
    put_safe(m, 'pf_fleececross', 49, 30, on='.t', r=3, prot=prot_wide)
    m.fence(52, 78, 96, gaps=((60, 62),))
    # Standing-stone Hill-Fort Ring crowning the summit
    for i, (cx, cy) in enumerate(((40, 3), (34, 5), (46, 5), (32, 10), (48, 10), (35, 14), (45, 14), (40, 16))):
        put_safe(m, 'fw_stone' if i % 2 else 'pf_roadstone', cx, cy, on='.t', r=1, prot=prot_wide)
    # Drystone sheepfolds on every terrace
    for (x0, y0, w_, h_) in ((54, 104, 9, 5), (14, 62, 7, 4), (60, 36, 8, 5), (22, 22, 7, 4)):
        for x in range(x0, x0 + w_):
            for y in (y0, y0 + h_):
                if x != x0 + w_ // 2 or y == y0:
                    if m.free(x, y, 1, 1, on='.t') and not m.cliff[y, x] and not r.road_mask[y, x] and not prot_wide[y, x]:
                        m.stamp('nr_wall_' + ('w' if x == x0 else 'e' if x == x0 + w_ - 1 else 'm'), x, y, mark='B')
        for y in range(y0 + 1, y0 + h_):
            for x in (x0, x0 + w_ - 1):
                if m.free(x, y, 1, 1, on='.t') and not m.cliff[y, x] and not r.road_mask[y, x] and not prot_wide[y, x]:
                    m.stamp('nr_wall_v', x, y, mark='B')

    for nm, x, y in (
        ('pf_hayrick', 58, 100), ('pf_logbench', 56, 92), ('pf_well', 60, 86),
        ('pf_wagon', 47, 90), ('pf_shrine', 50, 30), ('pf_hayrick', 66, 40), ('nt_stonering', 24, 26),
        ('pf_lantern', 43, 112), ('pf_lantern', 59, 90), ('pf_lantern', 69, 90),
        ('pf_lantern', 49, 35), ('pf_lantern', 22, 58), ('pf_lantern', 43, 10),
        ('pf_lantern', 29, 86), ('pf_lantern', 56, 73), ('pf_lantern', 30, 54),
    ):
        res = put_safe(m, nm, x, y, on='.td', r=3, prot=prot_wide)
        if res and nm == 'pf_lantern':
            glow_pts.append((res[0], res[1] + 1))

    CK.fringe(r, CK.FRINGE['meadow'], 230, seed=1, near_forest=6)
    CK.fringe(r, ['nt_pine_sh', 'nt_dpine_sh', 'tr_pine', 'nt_round_sh'], 75, box=(0, 0, W, 96), seed=2, near_forest=0)
    CK.undergrowth(r, 260, seed=3)
    CK.props(r, ['nt_boulder', 'nt_rocks_s0', 'nt_rocks_s1', 'nt_rock_big', 'nt_stump'], 42, box=(0, 0, W, 72), clump=3, seed=7)
    CK.props(r, ['nt_log', 'nt_stump', 'nt_rocks_s1'], 18, box=(0, 70, W, H), clump=2, seed=8)

    # ---- 7. Paint + Forest Infill, Mossy Ground Depth, Wildflowers, Summit Hoar & Warm Glows ----
    r.paint(glint=0.0)
    CK.paint_extras(r)
    infill_forest(r, HIGHLAND_MID_WOODS, pick=pick_566_pal, scale=11.0, seed=566)
    paint_forest_ground_depth(m, seed=566, clearings=[(63, 89, 8, 5, 'worn'), (40, 9, 6, 4, 'worn')], dark=0.45)

    # Lotus lilies on Sheep-wash pool & wildflower ribbons across the fell terraces
    dress_water_lotus(m, prob=0.14, seed=566)
    FL = K.DECOR_SH['flowers']
    for i, (cx_, cy_, rx, ry, ks) in enumerate((
        (50, 70, 6, 2.2, (2, 6)), (24, 50, 5, 2.2, (8, 9)), (62, 30, 5, 2.2, (0, 4)),
        (36, 96, 6, 3.0, (1, 5)), (68, 58, 4.5, 2.2, (6, 7)), (30, 22, 5, 2.2, (10, 11)),
        (44, 110, 5, 2.5, (1, 2)),
    )):
        CK.meadow(r, cx_, cy_, rx, ry, tiles=[FL[k] for k in ks], p=0.72, seed=i)
    scatter_petals_and_mushrooms(
        m,
        spots_petals=[(40, 108, 6, 4, 0.25), (60, 90, 6, 4, 0.22), (50, 35, 5, 3, 0.20)],
        spots_mush=[(16, 86, 3.0, 5), (22, 62, 3.0, 5), (36, 12, 3.0, 4)],
        seed=566,
    )
    # First mountain hoar frost on summit grass (transitioning naturally into snowy Frostwick Pass!)
    for y in range(0, 26):
        for x in range(W):
            if m.cls[y, x] == '.' and m.L[1, y, x] == 0 and m.L[2, y, x] == 0 and r.rng.random() < 0.22 * (1 - y / 26.0):
                m.L[1, y, x] = r.rng.choice([K.STAMPS['fw_drift0']['layers'][1][0][0], K.STAMPS['fw_drift1']['layers'][1][0][0]])
    CK.shore(r, wet=0, wrack=0, shallows=0.05, kelp=0.0, chalk_rocks=False)
    add_warm_glows(m, glow_pts + [(50, 33), (62, 88), (40, 8)])
    CK.scatter_quiet(r, 20)

    # Seal ALL stray perimeter edges strictly except S (38..41 -> 120) and N (42..45 -> 577)!
    seal_unconnected_edges(
        m,
        open_cells=[(x, H - 1) for x in range(38, 42)] + [(x, 0) for x in range(42, 46)],
        filler=P1('nt_bush0'),
    )
    write_wave13_map(m, 566, "# Spinners' Rise (566). WRITTEN BY layouts/wave13_routes_craft.py (Wave 13 Rejuv V14 Craft).\n")
    return m


# =============================================================================
# 10. MAP 577: FROSTWICK PASS (72x96, ts 52 PF Rejuv Snow)
# =============================================================================
def build_577():
    """Frostwick Pass (72x96, ts 52): sweeping alpine pass climbing from Spinners' Rise (S col 30..33)
    to Frostwick East Gate (W row 37..40). Boldly staggered multi-promontory shs3 snow cliffs (zero
    ruler-straight horizontal walls!), organic eroded snow-grass glades, dense Kristiline alpine spruce
    canopy with clean hut aprons, strictly sealed Wind Gap (x=40..42, y=54..66), Rock-Smash-sealed
    Icium Z gully ([66, 57]), Frozen Tarn (54, 32), Handfast Arch (8, 36), lantern-lit Bothy & Toll Hut."""
    W, H = 72, 96
    hspec = head_spec(577)
    evs = hspec['events']
    r = Route(577, W, H, 'snow', base='.', kit='shs3')
    m = r.m

    # ---- 1. Boldly Staggered Alpine Ridge Terraces (shs3 — ZERO ruler-straight horizontal walls!) ----
    def lip1_at(x):
        if x <= 18:
            return 71
        if x <= 27:
            return 77
        if x <= 36:
            return 73
        if x <= 46:
            return 75
        if x <= 58:
            return 79
        return 72

    def lip2_at(x):
        if x <= 15:
            return 52
        if x <= 31:
            return 45
        if x <= 44:
            return 50
        if x <= 57:
            return 47
        return 48

    for x in range(W):
        y1 = lip1_at(x)
        y2 = lip2_at(x)
        m.ht[:y1 + 1, x] = 1
        m.ht[:y2 + 1, x] = 2
    for hh in (1, 2):
        CK.smooth_ht(m, hh, 1)

    # ---- 2. Dense Alpine Forest Framing & Rich Upper-Basin Groves (ZERO barren snow slab!) ----
    r.forest_band('E', 9, wobble=4.0)
    r.forest_band('S', 5, wobble=3.0)
    r.forest_band('N', 6, wobble=3.0)
    r.forest_band('W', 4, wobble=2.2)

    # ---- 3. Winding Hoar Road & Strictly Framed Wind Gap (x=40..42, y=54..66) ----
    GX, GY0, GY1 = 40, 54, 66
    road = [(31.5, 95), (33, 86), (40, 80), (41, 75), (41, GY1 + 2), (41, GY0 - 2),
            (37, 46), (26, 41), (14, 38.5), (0, 38.5)]
    r.road(road, w=3.0, c='d', open_=(2, 5))
    r.exit('S', 30, 4)
    r.exit('W', 37, 4)
    # Wind gap choke: solid flanking woods on both sides of x=40..42, y=54..66!
    for y in range(GY0, GY1 + 1):
        for x in range(GX - 12, GX + 13):
            if abs(x - (GX + 1)) >= 2 and m.cls[y, x] in '.td':
                m.cls[y, x] = 'T'
        for x in (GX, GX + 1, GX + 2):
            m.cls[y, x] = 'd'

    # Align road stairs cleanly onto the exact staggered lip row where the road crosses
    stairs = []
    for yl, hh in ((75, 1), (50, 2)):
        xs = [x for x in range(34, 46) if r.road_mask[yl, x]]
        if xs:
            sx = min(xs) + max(0, (len(xs) - 3) // 2)
            # Ensure flat 3-wide lip directly at the stair crossing
            m.ht[:yl + 1, sx - 1:sx + 4] = np.maximum(m.ht[:yl + 1, sx - 1:sx + 4], hh)
            m.ht[yl + 1:yl + 4, sx - 1:sx + 4] = np.minimum(m.ht[yl + 1:yl + 4, sx - 1:sx + 4], hh - 1)
            stairs.append((sx, yl, hh))

    # ---- 4. Organic Multi-Lobe Frozen Tarn, Frozen Fall Hollow, Wolfsrime Landing & Side Lanes ----
    m.blob(54.0, 32.0, 7.6, 4.2, 'p', seed=5771, rough=0.45, only='.tT')
    m.blob(58.5, 34.5, 4.0, 2.5, 'p', seed=5772, rough=0.42, only='.tT')
    m.blob(49.5, 30.0, 3.5, 2.2, 'p', seed=5773, rough=0.40, only='.tT')
    smooth_cls(m, 'p', into='.', passes=2)
    r.lane([(38, 46), (46, 36), (52, 28)], w=2.0, c='d', open_=(1, 3))
    r.pocket(58, 20, 4.5, 2.8, gate=None)
    r.lane([(52, 28), (57, 22)], w=2.0, c='d', open_=(1, 2))
    r.lane([(31, 82), (20, 84), (14, 80)], w=2.0, c='d', open_=(1, 3))
    r.lane([(42, 70), (54, 70), (60, 66)], w=2.0, c='d', open_=(1, 2))
    # Clear snow aprons around Toll Hut (31, 77) & Bothy (12, 78) so zero pine woods encroach on roofs!
    r.clearing(33, 79, 5.0, 3.5, c='.')
    r.clearing(15, 80, 5.5, 3.8, c='.')
    # Wolfsrime snow-bank arrival clearing (16..19, 4) connected cleanly down onto the upper pass!
    r.clearing(17.5, 5.5, 4.5, 3.2, c='.')
    r.lane([(17.5, 6), (22, 16), (34, 17), (37, 25), (35, 38)], w=2.2, c='d', open_=(1, 3))

    # Rich copses sculpting intimate alpine glades across the upper down (zero bare flat plateau!)
    for cx, cy_, rx, ry in (
        (11, 88, 5.2, 3.2), (10, 20, 7.5, 5.5), (61, 46, 4.5, 4.2), (22, 60, 5.2, 3.2),
        (51, 87, 4.5, 3.2), (27, 24, 4.8, 3.5), (46, 15, 5.5, 3.8), (28, 8, 5.0, 3.5),
        (12, 30, 4.2, 3.0), (48, 44, 3.5, 2.5), (62, 79, 4.5, 3.5), (24, 34, 3.8, 2.6),
    ):
        r.copse(cx, cy_, rx, ry)

    # Icium Z avalanche gully (E wood behind Rock Smash boulder at [66, 57]): MUST stay strictly sealed behind (66, 57)!
    for y in range(52, 63):
        for x in range(63, 72):
            m.cls[y, x] = '.' if (68 <= x <= 70 and 56 <= y <= 58) or (y == 57 and 63 <= x <= 67) else 'T'
    # Connect east pass trail cleanly up to Rock Smash entrance (63, 57), SUPERPOTION (64, 45) & Snow-buried signpost (46, 44)!
    r.lane([(56, 66), (56, 57), (64, 57)], w=2.0, c='d', open_=(0, 1))
    r.lane([(54, 45), (64, 45)], w=2.0, c='d', open_=(0, 1))
    r.lane([(40, 44), (46, 44), (50, 40)], w=2.0, c='d', open_=(0, 1))
    # Ensure Snowmen [24, 49] & Snorunt [27, 49] connect cleanly south onto the central plateau!
    r.lane([(24, 50), (31, 51), (37, 51)], w=2.0, c='.', open_=(1, 1))

    # Keep all HEAD event coordinates & Wolfsrime landing (16..19, 4) free of 'T'
    for e in evs:
        ex, ey = e['at']
        if (ex, ey) != (1, 1) and m.cls[ey, ex] == 'T':
            m.cls[ey, ex] = '.'
    for wx in range(16, 20):
        m.cls[4, wx] = '.'
        m.cls[5, wx] = '.'
    m.cls[20:23, 57:60] = '.'
    r.finish_plan(border=0)
    for sx, yl, hh in stairs:
        CK.stair(r, sx, yl, w=3, h=hh)

    # Organic eroded tall-grass glades (smaller varied multi-lobe clusters + organic erosion -> ZERO 6x6 blocks!)
    CK.grass_fields(r, [
        (16, 43, 2.8), (22, 42, 2.3), (30, 53, 2.6), (54, 58, 2.6), (22, 69, 2.8),
        (51, 76, 2.6), (56, 74, 2.2), (14, 28, 2.6), (40, 28, 2.8), (34, 88, 2.3), (26, 16, 2.6),
    ])
    erode_snow_grass_organic(m, seed=577)

    # ---- 5. Lock ALL 64 Exact HEAD Events & Signposts ----
    prot_wide = reserve_events(
        m, evs, road_mask=r.road_mask, radius=1,
        extra=[(x, H - 1) for x in range(30, 34)] + [(0, y) for y in range(37, 41)] +
              [(x, 4) for x in range(16, 20)] + [(x, 57) for x in range(56, 71)] +
              [(68, 56), (69, 57), (70, 58), (69, 56), (69, 58), (64, 45), (56, 60), (57, 60)],
        skip_names=('Wind',),
    )
    paint_signposts(m, evs)

    # Dense Kristiline alpine woods!
    CK.woods(r, ALPINE_WOODS, scale=9.5)

    # ---- 6. Handfast Arch, Bothy, Toll Hut, Avalanche Fences, Frozen Fall, Lanterns & Groves ----
    glow_pts = []
    avoid_top = np.zeros((H, W), bool)
    if m.free(7, 33, STAMPS['wb_gate']['w'], STAMPS['wb_gate']['h'], on='.dt'):
        m.stamp('wb_gate', 7, 33)
        mark_stamp_avoid(avoid_top, 'wb_gate', 7, 33)
    smoke_pts = []
    for n, x, y in (
        ('wb_hut', 30, 77), ('wb_short', 12, 77), ('fw_rack', 58, 66), ('fw_rack', 54, 64),
        ('fw_sled', 36, 80), ('fw_fall', 56, 14), ('fw_brazier', 20, 80), ('fw_brazier', 36, 76),
        ('pf_lantern', 9, 37), ('pf_lantern', 12, 40), ('pf_lantern', 38, 68), ('pf_lantern', 38, 52),
        ('pf_lantern', 33, 89), ('pf_lantern', 49, 34), ('pf_lantern', 19, 7), ('pf_lantern', 56, 21),
        ('fw_wood', 18, 83), ('sh_crates', 37, 75), ('pf_logbench', 16, 84), ('fw_skull', 44, 52),
    ):
        res = put_safe(m, n, x, y, on='.td', r=4, prot=prot_wide)
        if res and n in ('wb_hut', 'wb_short'):
            mark_stamp_avoid(avoid_top, n, res[0], res[1], pad_x=1, pad_n=2, pad_s=1)
            smoke_pts.append((res[0] + 3, max(0, res[1] - 2)))
        if res and n in ('fw_brazier', 'pf_lantern'):
            glow_pts.append((res[0], res[1] + (1 if n == 'pf_lantern' else 0)))

    # Avalanche fences of split larch (with 2-tile mountain pass gap at x=56..57 leading north to Rock Smash gully!)
    for x in range(50, 62):
        if x in (56, 57):
            continue
        if m.free(x, 60, 1, 1, on='.t') and not prot_wide[60, x] and not m.cliff[60, x]:
            m.stamp('fw_pal_h', x, 60, mark='B')
    # Wind gap flanking crag stones
    for (x, y) in ((GX - 2, GY0 - 1), (GX + 3, GY0 - 1), (GX - 2, GY1 + 1), (GX + 4, GY1 + 1)):
        put_safe(m, 'fw_stone', x, y, on='.t', r=1, prot=prot_wide)
    # Ancient ice-glazed giant trees framing the Wolfsrime snow-bank descent & upper down!
    for nm, x, y in (('pf_g_tree4p_ice', 10, 1), ('pf_g_tree2_ice', 22, 2), ('pf_g_tree2_ice', 42, 20)):
        res = put_safe(m, nm, x, y, on='.tT', r=2, prot=prot_wide)
        if res:
            mark_stamp_avoid(avoid_top, nm, res[0], res[1], pad_x=1, pad_n=1, pad_s=1)
    # Kristiline conifer clusters breaking up open alpine glades
    prot_groves = prot_wide | avoid_top
    for idx, (cx, cy, cnt, rad) in enumerate(((22, 40, 3, 2.2), (43, 30, 3, 2.2), (29, 43, 3, 2.0), (50, 72, 3, 2.2), (16, 67, 3, 2.2))):
        place_snow_grove(m, cx, cy, count=cnt, radius=rad, on='.t', seed=577 + idx, prot=prot_groves)

    CK.props(r, ['fw_stone', 'fw_wood', 'fw_log_m', 'fw_drift2'], 28, box=(0, 0, W, H), clump=3, seed=7)

    # ---- 7. Paint + Dense Winter Canopy, Sealed Icium Z Gully, Glacial Turf & Warm Glows ----
    r.paint(glint=0.0)
    CK.paint_extras(r)
    infill_winter(r, ALPINE_WOODS, scale=9.5, seed=577, avoid_top=avoid_top)

    # Guarantee 100% airtight Rock-Smash wall around Icium Z gully (x=63..71)!
    for y in range(52, 63):
        for x in range(63, 72):
            if m.cls[y, x] == 'T' and m.L[1, y, x] == 0:
                m.L[1, y, x] = (10371, 10551)[(x + y) % 2]
    # Guarantee Wind Gap flanking 'T' cells are 100% solid (zero bypass!)
    for y in range(GY0, GY1 + 1):
        for x in range(GX - 12, GX + 13):
            if m.cls[y, x] == 'T' and m.L[1, y, x] == 0:
                m.L[1, y, x] = (10551, 10371)[(x + y) % 2]

    # Native seamless wind-swept snow drift variation + crystal spires near Frozen Fall!
    paint_snow_turf_layering(m, seed=577, cer_thr=0.61, peri_thr=0.69)
    for cx, cy, sp in ((55, 21, KF_CRYS_MONO), (61, 19, KF_CRYS_STAR), (48, 34, KF_CRYS_BLADES), (14, 7, KF_CRYS_MONO)):
        put_sprite(m, cx, cy, sp[0], sp[1], on='.', avoid_mask=prot_wide, post_paint=True)
    for sx_, sy_ in smoke_pts:
        put_overlay_stamp(m, 'fw_smoke_w', sx_, sy_, z=2)
    CK.snow_ground_var(r, thr=0.48)
    RW.icy_faces(m, 0.65, seed=577)
    RW.drifts(m, 0.06, seed=577)
    RW.road_tracks(m, 0.14, seed=577)
    RW.dress_ice(m, 0.25, seed=577)
    RW.reed_beds(m, 12, seed=577)
    add_warm_glows(m, glow_pts + [(8, 36), (17, 81), (36, 77), (58, 19)])

    # Seal ALL stray perimeter edges strictly except S (30..33 -> 566) and W (37..40 -> 570)!
    seal_unconnected_edges(
        m,
        open_cells=[(x, H - 1) for x in range(30, 34)] + [(0, y) for y in range(37, 41)],
        filler=(10551, 10371, 9872, 9888),
    )
    write_wave13_map(m, 577, '# Frostwick Pass (577). WRITTEN BY layouts/wave13_routes_craft.py (Wave 13 Rejuv V14 Craft).\n')
    return m


# =============================================================================
# 11. MAP 578: RIMEWOOD PATH (80x88, ts 52 PF Rejuv Snow)
# =============================================================================
def build_578():
    """Rimewood Path (80x88, ts 52): sweeping hoar-wood ascent from Frostwick (S col 40..43) to
    The Rimewood (N col 36..39) over three boldly staggered overlapping shs3 alpine ridges (zero
    ruler-straight cliffs!). Meandering +/-3-tile Long Ice frozen creek curving through its freed-up
    glacial valley (connecting Frozen fall [4,48], Snare Nook [19,50] stopper, and Long Ice [37,48]),
    organic eroded snow-grass glades, airtight Rock-Smash Silk-fall Glade ([60, 34]) & Unblazed maze."""
    W, H = 80, 88
    hspec = head_spec(578)
    evs = hspec['events']
    r = Route(578, W, H, 'snow', base='.', kit='shs3')
    m = r.m

    # ---- 1. Three Boldly Staggered Overlapping Alpine Ridges (ZERO ruler-straight horizontal walls!) ----
    def lip1_at(x):
        if x <= 18:
            return 66
        if x <= 31:
            return 70
        if x <= 44:
            return 68
        if x <= 55:
            return 73
        return 67

    def lip2_at(x):
        if x <= 9:
            return 44
        if x <= 22:
            return 39
        if x <= 33:
            return 41
        if x <= 48:
            return 45
        if x <= 60:
            return 42
        return 46

    def lip3_at(x):
        if x <= 15:
            return 18
        if x <= 31:
            return 23
        if x <= 46:
            return 20
        if x <= 65:
            return 22
        return 24

    for x in range(W):
        m.ht[:lip1_at(x) + 1, x] = 1
        m.ht[:lip2_at(x) + 1, x] = 2
        m.ht[:lip3_at(x) + 1, x] = 3
    for hh in (1, 2, 3):
        CK.smooth_ht(m, hh, 1)
    # Lock Frozen Fall crag lip (x=1..9, y=44) so waterfall pours cleanly into [4, 48]
    YL = 44
    for x in range(1, 10):
        m.ht[:YL + 1, x] = np.maximum(m.ht[:YL + 1, x], 2)
        m.ht[YL + 1:YL + 5, x] = np.minimum(m.ht[YL + 1:YL + 5, x], 1)

    # ---- 2. Forest Borders, Winding Hoar Road & Copses ----
    r.forest_band('W', 5, wobble=3.0)
    r.forest_band('E', 6, wobble=3.0)
    r.forest_band('N', 3, wobble=2.0)
    r.forest_band('S', 3, wobble=2.0)
    road = [(41.5, 87), (44, 81), (41, 75), (37, 68), (37, 63), (43, 57), (45, 50),
            (44, 45), (40, 38), (35, 31), (38, 25), (43, 20), (43, 13), (39, 6), (37.5, 0)]
    r.road(road, w=3.0, open_=None)
    r.exit('S', 40, 4)
    r.exit('N', 36, 4)
    stairs = []
    for yl, hh, xlo, xhi in ((68, 1, 33, 43), (45, 2, 38, 48), (20, 3, 38, 47)):
        xs = [x for x in range(xlo, xhi + 1) if r.road_mask[yl, x]]
        if xs:
            sx = min(xs) + max(0, (len(xs) - 3) // 2)
            m.ht[:yl + 1, sx - 1:sx + 4] = np.maximum(m.ht[:yl + 1, sx - 1:sx + 4], hh)
            m.ht[yl + 1:yl + 4, sx - 1:sx + 4] = np.minimum(m.ht[yl + 1:yl + 4, sx - 1:sx + 4], hh - 1)
            stairs.append((sx, yl, hh))
    # Ensure flat lip at west Woodcutter stair (x=25, y=70, h=1)
    m.ht[:71, 24:29] = np.maximum(m.ht[:71, 24:29], 1)
    m.ht[71:74, 24:29] = np.minimum(m.ht[71:74, 24:29], 0)

    BY = 47   # exact anchor rows y=47, 48 matching Frozen fall [4,48], Long Ice [37,48], Snare [19,50]
    BX0, BX1 = 6, 35

    def creek_rows(x):
        """Organic +/-3-tile meandering frozen creek across x=6..35 inside the broadened middle valley!"""
        if x <= 8:
            return (47, 48)
        if x <= 17:
            c = int(round(47.0 - 2.8 * math.sin((x - 8.0) * math.pi / 9.5)))
            return (c, c + 1)
        if x <= 21:
            return (47, 48)
        if x <= 32:
            c = int(round(47.0 - 2.3 * math.sin((x - 21.0) * math.pi / 11.5)))
            return (c, c + 1)
        return (47, 48)

    for cx, cy_, rx, ry in (
        (26, 54, 6.5, 2.8), (14, 83, 5.0, 2.5), (66, 84, 7, 3), (58, 60, 6, 4), (70, 48, 6, 4.5),
        (24, 30, 6, 4), (56, 30, 5, 4), (62, 10, 5, 3), (14, 12, 6, 4), (30, 63, 4.5, 2.8),
        (52, 74, 4, 2.5), (10, 62, 4, 2.8), (20, 17, 4.5, 3.0), (14, 34, 4.5, 2.8),
    ):
        r.copse(cx, cy_, rx, ry)

    # Woodcutters' yard (SW — generous apron around wb_hut 12,77!), Honey-stump hives (SE), Long Ice & Burners' Clearing (W)
    r.clearing(20, 78, 11.0, 5.5, only='T.t')
    r.lane([(40, 79), (30, 78)], w=2.0, open_=None)
    r.clearing(58, 81, 7, 3.5, only='T.t')
    # Carve snow valley around the meandering creek first so banks breathe organically
    for x in range(BX0 - 2, BX1 + 3):
        y0c, y1c = creek_rows(min(BX1, max(BX0, x)))
        for y in range(max(43, y0c - 1), min(53, y1c + 2)):
            if m.cls[y, x] in 'T.t':
                m.cls[y, x] = '.'
    for x in range(BX0, BX1 + 1):
        y0c, y1c = creek_rows(x)
        for y in range(y0c, y1c + 1):
            m.cls[y, x] = 'p'
        # Smooth organic inner bend fills so curves are never 1-tile stair-steps
        if x in (10, 11, 15, 16, 23, 24, 30, 31):
            m.cls[y1c + 1, x] = 'p'
    # Organic conifer clumps framing the creek's south bends (instead of a rigid horizontal tree bar!)
    for cx, cy_, rx, ry in ((14, 52, 3.2, 2.0), (26, 52, 4.0, 2.2), (32, 53, 2.8, 1.8)):
        r.copse(cx, cy_, rx, ry)
    for x in range(BX0 - 4, BX0):
        for y in range(BY - 1, BY + 4):
            m.cls[y, x] = '.'
    for x in range(BX1 + 1, BX1 + 6):
        for y in range(BY, BY + 3):
            m.cls[y, x] = '.'
    r.lane([(BX1 + 4, BY + 1), (43, 50)], w=2.0, open_=None)
    SNARE = 20
    for x in range(SNARE - 3, SNARE + 2):
        for y in (BY + 2, BY + 3):
            m.cls[y, x] = '.'
    r.clearing(9, 54, 5.5, 3.6, only='T.t')
    r.lane([(4, BY + 3), (8, 52)], w=2.0, open_=None)
    r.lane([(12, 57), (24, 60), (36, 62)], w=2.0, open_=None)

    # ---- 3. Airtight Silk-fall Glade (E) behind Frozen Silk Curtain [60, 34] ----
    GX, GY, GRX, GRY = 67, 34, 5.5, 3.5
    GAP1 = (60, 34)
    RING = set()
    for y in range(GY - 9, GY + 10):
        for x in range(GX - 12, min(W, GX + 13)):
            qi = ((x - GX) / GRX) ** 2 + ((y - GY) / GRY) ** 2
            qo = ((x - GX) / (GRX + 3.2)) ** 2 + ((y - GY) / (GRY + 3.2)) ** 2
            if not m.inb(x, y):
                continue
            if qi <= 1.0:
                m.cls[y, x] = '.'
            elif qo <= 1.0 or (x >= W - 2 and abs(y - GY) <= GRY + 3):
                m.cls[y, x] = 'T'
                RING.add((x, y))
    for x in range(GAP1[0] - 3, GAP1[0] + 2):
        m.cls[GAP1[1], x] = '.'
        RING.discard((x, GAP1[1]))
    r.lane([(46, 40), (52, 36), (GAP1[0] - 3, GAP1[1])], w=2.0, open_=None)
    r.lane([(46, 27), (56, 25), (66, 25)], w=2.0, c='.', open_=(1, 2))
    for x, y in RING:
        m.cls[y, x] = 'T'
    for x in range(GAP1[0] - 3, GAP1[0] + 2):
        m.cls[GAP1[1], x] = '.'
        RING.discard((x, GAP1[1]))

    # ---- 4. Airtight Unblazed Stantler Maze (NE h=3, preserving all 15 wrong-turn warps & GAP2 [51, 5]) ----
    BLAZE = (45, 16)
    for x in range(48, W):
        for y in range(0, 21):
            if m.cls[y, x] in '.t':
                m.cls[y, x] = 'T'
    r.lane([(46, 16), (57, 15)], w=3.0, c='.', open_=None)
    r.clearing(58, 15, 4.2, 3.0)
    r.clearing(70, 14, 4.2, 3.0)
    r.clearing(66, 4, 6.5, 2.8)
    r.lane([(57, 15), (67, 14), (70, 15)], w=3.0, c='.', open_=None)
    r.lane([(70, 16), (70, 10), (67, 4)], w=3.0, c='.', open_=None)
    r.lane([(58, 16), (58, 8)], w=3.0, c='.', open_=None)
    r.lane([(58, 16), (62, 20)], w=3.0, c='.', open_=None)
    r.lane([(70, 15), (73, 20)], w=3.0, c='.', open_=None)
    r.lane([(60, 4), (52, 5), (44, 6)], w=2.0, open_=None)
    GAP2 = (51, 5)
    UNB = r.road_mask.copy()
    UNB[:, :45] = False
    UNB[23:, :] = False
    for x in range(48, 60):
        for y in (3, 4, 6, 7):
            if m.cls[y, x] in '.d' and x in range(50, 53):
                m.cls[y, x] = 'T'
    for x in range(50, 53):
        m.cls[5, x] = 'd' if x != GAP2[0] else '.'

    for e in evs:
        ex, ey = e['at']
        if m.cls[ey, ex] == 'T' and (ex, ey) not in RING:
            m.cls[ey, ex] = '.'
    r.finish_plan(border=0)
    for sx, yl, hh in stairs:
        CK.stair(r, sx, yl, w=3, h=hh)
    CK.stair(r, 25, 70, w=3, h=1)
    # Re-apply meandering frozen creek strictly off cliff faces!
    for x in range(BX0, BX1 + 1):
        y0c, y1c = creek_rows(x)
        for y in range(y0c, y1c + 1):
            if not m.cliff[y, x]:
                m.cls[y, x] = 'p'
        if x in (10, 11, 15, 16, 23, 24, 30, 31) and not m.cliff[y1c + 1, x]:
            m.cls[y1c + 1, x] = 'p'
    # One-way snow-bank drop from Trapper's lean-to shelf down to Honey-stump hives
    CK.ledge(r, 54, 62, 74, face='snow')

    # Eroded organic snow-grass glades (ZERO stamped rectangular boxes!)
    CK.grass_fields(r, [
        (19, 75, 2.5), (30, 84, 2.3), (60, 63, 2.8), (28, 62, 2.6), (52, 52, 2.8),
        (30, 35, 2.8), (20, 27, 2.5), (30, 12, 2.6), (14, 32, 2.6), (64, 26, 2.3),
    ])
    erode_snow_grass_organic(m, seed=578)

    # ---- 5. Lock ALL 47 Exact HEAD Events & Signposts ----
    prot_wide = reserve_events(
        m, evs, road_mask=r.road_mask, radius=1,
        extra=[(x, 0) for x in range(36, 40)] + [(x, H - 1) for x in range(40, 44)] +
              [(45, 17), GAP1, GAP2, (18, 50), (67, 34), (42, 86), (38, 1)],
    )
    m.taken |= UNB
    paint_signposts(m, evs)

    # Dense Kristiline evergreen canopy (rich alpine/rimewood mix!)
    CK.woods(r, ALPINE_WOODS, scale=8.5)

    # ---- 6. Woodcutters' Yard, Honey-Stumps, Trapper's Lean-To, Charcoal Kiln, Lantern Birch & Giants ----
    glow_pts = []
    avoid_top = np.zeros((H, W), bool)
    smoke_pts = [(7, 50)]
    for n, x, y in (
        ('wb_hut', 12, 76), ('fw_wood', 20, 75), ('fw_wood', 22, 75), ('fw_log_m', 22, 81),
        ('pf_sledge', 28, 80), ('fw_rack', 17, 80), ('fw_wood', 14, 81), ('fw_log_n', 26, 74), ('fw_log_s', 18, 83),
        ('nt_stump_big', 55, 78), ('nt_stump', 60, 82), ('nt_stump_big', 61, 78), ('nt_stump', 64, 82),
        ('fw_rack', 58, 70), ('fw_brazier', 61, 72), ('fw_rack', 67, 71), ('fw_wood', 65, 73), ('fw_skull', 69, 72),
        ('nt_stonering', 5, 54), ('fw_smoke_a', 7, 50), ('fw_wood', 11, 51), ('fw_wood', 13, 53), ('fw_sled', 13, 56),
        ('pf_lantern', 42, 38), ('fw_stone', 39, 42),
        ('pf_lantern', 43, 83), ('pf_lantern', 38, 60), ('pf_lantern', 46, 17), ('pf_lantern', 65, 33),
        ('pf_lantern', 39, 5), ('fw_brazier', 18, 79),
    ):
        res = put_safe(m, n, x, y, on='.d', r=3, prot=prot_wide)
        if res and n == 'wb_hut':
            mark_stamp_avoid(avoid_top, 'wb_hut', res[0], res[1], pad_x=1, pad_n=2, pad_s=1)
            smoke_pts.append((res[0] + 3, max(0, res[1] - 2)))
        if res and n in ('pf_lantern', 'fw_brazier'):
            glow_pts.append((res[0], res[1] + (1 if n == 'pf_lantern' else 0)))

    for x in range(SNARE - 3, SNARE + 1, 2):
        if m.free(x, BY + 2, 1, 1, on='.') and not prot_wide[BY + 2, x]:
            m.stamp('fw_peg', x, BY + 2)
    m.stamp('fw_fall', BX0 - 4, YL - 1, mark='B')
    # Towering ancient ice-glazed giants on the upper ridges!
    for nm, x, y in (('pf_g_tree6_ice', 2, 1), ('pf_g_tree4p_ice', 25, 2), ('pf_g_tree2_ice', 74, 25), ('pf_g_tree2_ice', 27, 33)):
        res = put_safe(m, nm, x, y, on='.tT', r=3, prot=prot_wide)
        if res:
            mark_stamp_avoid(avoid_top, nm, res[0], res[1], pad_x=1, pad_n=1, pad_s=1)

    # Extra Kristiline conifer groves framing the woodcutters' yard & birch hollows
    prot_groves = prot_wide | avoid_top
    for idx, (cx, cy, cnt, rad) in enumerate(((50, 82, 3, 2.2), (24, 36, 3, 2.0), (18, 28, 3, 2.2), (48, 56, 3, 2.2), (28, 15, 3, 2.2))):
        place_snow_grove(m, cx, cy, count=cnt, radius=rad, on='.t', seed=578 + idx, prot=prot_groves)

    CK.undergrowth(r, 30, kinds=('fw_stone', 'fw_drift2', 'fw_drift0'), seed=3)
    CK.props(r, ['fw_stone', 'fw_wood', 'fw_log_m', 'fw_drift2', 'fw_drift0'], 16, box=(0, 0, W, H), clump=3, seed=7)

    # ---- 7. Paint + Dense Winter Canopy, Airtight Walls, Stantler Tracks, Crystals & Glows ----
    r.paint(glint=0.0)
    CK.paint_extras(r)
    infill_winter(r, ALPINE_WOODS, scale=8.5, seed=578, avoid_top=avoid_top)

    SHRUB = (10371, 10551, 9872)
    # Long Ice stopper dropping players cleanly at the Snare Nook (17..20, 49..50)!
    m.L[1, BY + 1, SNARE - 1] = 10371
    # Airtight Silk-fall glade wall (ZERO gate leaks around [60, 34]!)
    for x, y in RING:
        if m.cls[y, x] == 'T' and m.L[1, y, x] == 0 and m.L[2, y, x] == 0 and (x, y) != GAP1:
            m.L[1, y, x] = SHRUB[(x * 7 + y * 3) % 3]
    # Airtight Unblazed wood (no slipping between trees!)
    for y in range(0, 23):
        for x in range(47, W):
            if m.cls[y, x] == 'T' and m.L[1, y, x] == 0 and not m.taken[y, x]:
                m.L[1, y, x] = SHRUB[(x * 7 + y * 3) % 3]

    # Visible Stantler hoofprints leading cleanly through The Unblazed (A -> B -> C)!
    TK = [STAMPS['fw_tracks%d' % i]['layers'][1][0][0] for i in range(2)]
    for x, y in ([(55 + k, 16 - (k % 2)) for k in range(6)]
                 + [(62 + k, 14) for k in range(5)]
                 + [(70 - (k // 3), 10 - k) for k in range(5)]):
        if m.inb(x, y) and m.cls[y, x] in '.d' and m.L[2, y, x] == 0 and (UNB[y, x] or not m.taken[y, x]):
            m.L[2, y, x] = TK[(x + y) % 2]

    # Native seamless wind-swept snow drift variation + glistening frost crystals around Frozen Fall & Silk-fall glade!
    paint_snow_turf_layering(m, seed=578, cer_thr=0.62, peri_thr=0.70)
    for cx, cy, sp in ((64, 33, KF_CRYS_STAR), (69, 32, KF_CRYS_MONO), (66, 36, KF_CRYS_BLADES), (5, 50, KF_CRYS_MONO)):
        put_sprite(m, cx, cy, sp[0], sp[1], on='.', avoid_mask=prot_wide, post_paint=True)
    for sx_, sy_ in smoke_pts:
        put_overlay_stamp(m, 'fw_smoke_w', sx_, sy_, z=2)
    CK.snow_ground_var(r, thr=0.46)
    RW.icy_faces(m, 0.65, seed=578)
    RW.rime_silk(m, ((30, 12), (48, 22), (63, 31), (65, 31), (70, 31), (72, 35), (26, 76), (20, 44), (8, 58)))
    RW.drifts(m, 0.06, seed=578)
    RW.road_tracks(m, 0.14, seed=578)
    RW.dress_ice(m, 0.24, seed=578)
    RW.reed_beds(m, 14, seed=578)
    add_warm_glows(m, glow_pts + [(41, 40), (7, 52), (62, 72), (67, 34)])

    # Seal ALL stray perimeter edges strictly except S (40..43 -> 570) and N (36..39 -> 562)!
    seal_unconnected_edges(
        m,
        open_cells=[(x, H - 1) for x in range(40, 44)] + [(x, 0) for x in range(36, 40)],
        filler=(10551, 10371, 9872, 9888),
    )
    write_wave13_map(m, 578, '# Rimewood Path (578). WRITTEN BY layouts/wave13_routes_craft.py (Wave 13 Rejuv V14 Craft).\n')
    return m


# =============================================================================
# 12. MAP 579: THE WOLFSRIME (80x88, ts 52 PF Rejuv Snow)
# =============================================================================
def build_579():
    """The Wolfsrime (80x88, ts 52): haunting ancient drove road winding down from The Rimewood
    (N warps [36..39, 0]) to the steep one-way snow bank above Frostwick Pass (S events [40..43, 87]).
    Sculpted breathing northern timberland with 6 spacious connected woodland glades (breaking wall-to-wall
    pine grid spam!), mixed-scale conifers/snowdrifts/fallen logs, sinuous brook valley with weathered
    timber bridge, cozy Drovers' Bothy cabin (59, 65) with clean snow apron & zero tree clipping, Cold
    Kiln amphitheater (20, 44), Hanging Bell crossroads (42, 34), and hidden Old Wolf Den (62, 18)."""
    W, H = 80, 88
    hspec = head_spec(579)
    evs = hspec['events']
    r = Route(579, W, H, 'snow', base='T', kit='shs3')
    m = r.m

    # ---- 1. Winding Ancient Drove Road & Spacious Connected Woodland Clearings (ZERO 80% pine wallpaper!) ----
    road = [(42, 87), (44, 76), (36, 64), (40, 52), (50, 42), (44, 30), (38, 18), (38, 8), (38, 0)]
    r.road(road, w=3.2, open_=(5, 10))
    r.exit('S', 40, 4)
    r.exit('N', 36, 4)

    # Six generous, connected storybook snow glades framing every landmark & hut (bringing forest to ~48%!)
    r.clearing(20, 45, 11.5, 7.5)                                               # 1. Cold Kiln amphitheater (20, 44)
    r.lane([(40, 50), (26, 46)], w=2.6, open_=(2, 4))
    r.clearing(60, 70, 12.5, 8.5)                                               # 2. Drovers' Bothy meadow (59, 65 / 60, 74)
    r.lane([(44, 74), (54, 73), (62, 73), (66, 72)], w=2.8, open_=(2, 4))
    r.clearing(62, 19, 9.5, 6.5)                                                # 3. Old Wolf Den crystalline basin (62, 18)
    r.lane([(44, 28), (52, 24), (58, 22)], w=2.2, open_=(1, 3))
    r.clearing(19, 21, 10.5, 7.2)                                               # 4. NW Ancient-Tree & Birch glade
    r.clearing(29, 25, 7.0, 4.5)                                                #    merged into Birch Hollow (28, 24)
    r.lane([(38, 24), (31, 25), (21, 22)], w=2.2, open_=(2, 3))
    r.clearing(45, 34, 9.5, 6.0)                                                # 5. Hanging Bell crossroads glade (42, 34)
    r.clearing(24, 70, 10.5, 6.8)                                               # 6. SW Birch Fork & Brookside meadow (31, 67)
    r.clearing(33, 67, 5.2, 3.8)
    r.lane([(36, 65), (30, 67), (24, 69)], w=2.4, open_=(1, 3))
    # North gate glade & South bank glade so entries breathe gracefully
    r.clearing(38, 9, 8.5, 5.0)
    r.clearing(42, 80, 9.0, 5.2)

    # Organic sinuous frozen brook meandering east-west across y~56..61 inside a snowy brook valley!
    for x in range(W):
        c = 58.0 + 2.4 * math.sin(x / 10.5) + 1.6 * (vnoise(x, 0, 5791, 9.0) - 0.5) * 2
        hw = 1.6 + 0.8 * bump(x, 22, 7.0, 1.0) + 0.9 * bump(x, 54, 7.0, 1.0)
        # Open snowy riverbanks flanking the brook across the valley interior (x=10..68)
        if 10 <= x <= 68:
            for y in range(int(round(c - hw - 2.6)), int(round(c + hw + 2.6)) + 1):
                if m.inb(x, y) and m.cls[y, x] == 'T':
                    m.cls[y, x] = '.'
        for y in range(int(round(c - hw)), int(round(c + hw)) + 1):
            if m.inb(x, y) and m.cls[y, x] in 'T.t':
                m.cls[y, x] = 'p'
    smooth_cls(m, 'p', into='.', passes=2)

    # Scenic brookside alcoves around Drover's grandson (46, 59) & Old Wolf Trap (56, 58)
    r.clearing(46, 59, 4.5, 3.2)
    r.clearing(56, 58, 4.8, 3.2)
    r.lane([(40, 56), (46, 59), (56, 58)], w=2.4, open_=(1, 2))
    # Connect Cold Kiln & SW meadow smoothly across brook west bank so zero clearing tiles are cut off
    r.lane([(20, 51), (20, 56), (22, 64)], w=2.4, c='.', open_=(1, 1))
    r.lane([(56, 61), (57, 65)], w=2.4, c='.', open_=(1, 1))

    # Strict 3-tile north / 2-tile W/E/S clear snow apron around Drovers' Bothy hut (59, 65 -> 59..63, 65..69)
    # Guarantees ZERO pine crowns poke behind its roof or clip its NW porch!
    for y in range(62, 72):
        for x in range(56, 67):
            if m.cls[y, x] == 'T':
                m.cls[y, x] = '.'

    # Ensure ALL 23 HEAD events sit on clear walkable snow (NEVER trapped inside 'T'!)
    for e in evs:
        ex, ey = e['at']
        if m.cls[ey, ex] == 'T':
            m.cls[ey, ex] = '.'
    r.grass(thr=0.58, scale=5.0)
    erode_snow_grass_organic(m, seed=579)
    # Keep Drovers' Bothy yard & doorstep neat snow/packed path (no grass right over roof/porch)
    for y in range(63, 72):
        for x in range(57, 66):
            if m.cls[y, x] == 't':
                m.cls[y, x] = '.'
    r.finish_plan(border=0)

    # ---- 2. Lock ALL 23 Exact HEAD Events & Signposts ----
    prot_wide = reserve_events(
        m, evs, road_mask=r.road_mask, radius=1,
        extra=[(x, 0) for x in range(36, 40)] + [(x, 1) for x in range(36, 40)] +
              [(x, H - 1) for x in range(40, 44)] + [(x, H - 2) for x in range(40, 44)] +
              [(x, 73) for x in range(46, 67)] + [(x, 74) for x in range(54, 65)] +
              [(x, 59) for x in range(41, 56)],
    )
    paint_signposts(m, evs)

    # ---- 3. Deep Haunted Dark-Winter Kristiline Spruce Canopy! ----
    CK.woods(r, DARK_WINTER_WOODS, scale=8.5)

    # ---- 4. Landmarks: Drovers' Bothy Cabin, Cold Kiln Ring, Hanging Bell Lantern, Giants & Mixed Glade Islands ----
    glow_pts = []
    avoid_top = np.zeros((H, W), bool)
    # Cozy timber Drovers' Bothy cabin perched cleanly NORTH of the yard (59, 65) with wide cleared snow apron!
    hut_pos = put_safe(m, 'wb_hut', 59, 65, on='.td', r=2, prot=prot_wide)
    if hut_pos:
        mark_stamp_avoid(avoid_top, 'wb_hut', hut_pos[0], hut_pos[1], pad_x=2, pad_n=3, pad_s=2)
    put_safe(m, 'nt_stonering', 18, 43, on='.td', r=2, prot=prot_wide)   # Cold kiln stonework!
    for nm, x, y in (
        ('fw_wood', 18, 48), ('fw_rack', 24, 42), ('fw_sled', 48, 63), ('fw_wood', 50, 64),
        ('pf_lantern', 43, 33), ('pf_lantern', 40, 8), ('pf_lantern', 57, 71), ('pf_lantern', 21, 46),
        ('pf_lantern', 45, 29), ('pf_lantern', 42, 84), ('fw_brazier', 64, 71), ('fw_brazier', 22, 44),
        ('fw_skull', 32, 66), ('fw_skull', 61, 19), ('fw_skull', 57, 57),
        ('pf_logbench', 57, 75), ('fw_log_m', 26, 25), ('fw_wood', 65, 75), ('sh_crates', 55, 70),
        # Fallen winter timber logs, snowdrifts & mossy boulders seasoning the open woodland clearings!
        ('fw_log_m', 14, 48), ('fw_log_n', 25, 49), ('fw_log_s', 22, 67), ('fw_log_m', 18, 72),
        ('fw_log_n', 49, 36), ('fw_log_m', 15, 24), ('fw_log_s', 65, 23), ('fw_sled', 26, 71),
        ('ck_boulder', 13, 43), ('ck_boulder', 29, 73), ('ck_boulder', 51, 32), ('ck_boulder', 34, 11),
        ('fw_wood', 24, 21), ('fw_stone', 19, 17), ('fw_stone', 65, 67),
    ):
        res = put_safe(m, nm, x, y, on='.td', r=3, prot=prot_wide)
        if res and nm in ('pf_lantern', 'fw_brazier'):
            glow_pts.append((res[0], res[1] + (1 if nm == 'pf_lantern' else 0)))

    # Towering ice-glazed ancient trees showcased in open glades (zero pine overlap!)
    for nm, x, y in (
        ('pf_g_tree6_ice', 12, 16), ('pf_g_tree4p_ice', 64, 38), ('pf_g_tree4p_ice', 15, 67),
        ('pf_g_tree2_ice', 66, 6), ('pf_g_tree2_ice', 56, 15), ('pf_g_tree2_ice', 31, 34),
        ('pf_g_tree2_ice', 12, 40), ('pf_g_tree2_ice', 48, 76),
    ):
        res = put_safe(m, nm, x, y, on='.tT', r=3, prot=prot_wide | avoid_top)
        if res:
            mark_stamp_avoid(avoid_top, nm, res[0], res[1], pad_x=1, pad_n=1, pad_s=1)

    # Mixed-size Kristiline spruce islands framing clearings (strictly OUTSIDE hut & giant-tree aprons!)
    prot_groves = prot_wide | avoid_top
    for idx, (cx, cy, cnt, rad) in enumerate((
        (48, 79, 3, 2.2), (35, 50, 3, 2.2), (49, 38, 2, 2.0), (33, 13, 3, 2.2),
        (24, 17, 2, 2.0), (14, 51, 2, 2.0), (29, 74, 2, 2.0), (68, 66, 2, 2.0),
    )):
        place_snow_grove(m, cx, cy, count=cnt, radius=rad, on='.t', seed=579 + idx, prot=prot_groves)

    CK.props(r, ['fw_stone', 'fw_wood', 'fw_log_m', 'fw_drift2', 'fw_drift0', 'ck_boulder'], 28, box=(0, 0, W, H), clump=3, seed=7)

    # ---- 5. Paint + Deep Winter Canopy Infill (with avoid_top!), Rustic Timber Crossing & Glows ----
    r.paint(glint=0.0)
    CK.paint_extras(r)
    infill_winter(r, DARK_WINTER_WOODS, scale=8.5, seed=579, avoid_top=avoid_top)

    # Rustic weathered timber bridge across the frozen brook where the drove road crosses!
    brook_rows = sorted(set(y for y in range(53, 64) if m.cls[y, 38] == 'p'))
    if brook_rows:
        y0b, y1b = min(brook_rows), max(brook_rows)
        for y in range(y0b, y1b + 1):
            for i, x in enumerate((37, 38, 39)):
                if m.inb(x, y) and m.cls[y, x] == 'p':
                    m.L[1, y, x] = C('ak', 1524 + i)

    # Native seamless wind-swept snow drift variation across forest clearings!
    paint_snow_turf_layering(m, seed=579, cer_thr=0.58, peri_thr=0.67)
    # Eerie frost crystals & ethereal forest light shafts near Hanging Bell, Ancient Tree & Old Den!
    for cx, cy, sp in ((60, 21, KF_CRYS_MONO), (64, 17, KF_CRYS_STAR), (26, 23, KF_CRYS_BLADES), (40, 35, KF_CRYS_MONO), (16, 23, KF_CRYS_STAR)):
        put_sprite(m, cx, cy, sp[0], sp[1], on='.', avoid_mask=prot_groves, post_paint=True)
    for sx_, sy_ in ((41, 32), (61, 16), (37, 2), (18, 20)):
        put_overlay_stamp(m, 'cv_shaft', sx_, sy_, z=2)
    if hut_pos:
        put_overlay_stamp(m, 'fw_smoke_w', hut_pos[0] + 3, max(0, hut_pos[1] - 2), z=2)   # Warm Bothy chimney smoke!
    CK.snow_ground_var(r, thr=0.45)
    RW.rime_silk(m, ((30, 12), (48, 22), (34, 40), (52, 50), (26, 78), (58, 24), (44, 34)))
    RW.drifts(m, 0.08, seed=579)
    RW.road_tracks(m, 0.14, seed=579)
    RW.dress_ice(m, 0.25, seed=579)
    RW.reed_beds(m, 14, seed=579)
    add_warm_glows(m, glow_pts + [(42, 34), (60, 73), (20, 45), (38, 1)])

    # Seal ALL stray perimeter edges strictly except N warps (36..39, 0) and S snow banks (40..43, 87)!
    seal_unconnected_edges(
        m,
        open_cells=[(x, 0) for x in range(36, 40)] + [(x, H - 1) for x in range(40, 44)],
        filler=(10551, 10371, 9872, 9888),
    )
    write_wave13_map(m, 579, '# The Wolfsrime (579). WRITTEN BY layouts/wave13_routes_craft.py (Wave 13 Rejuv V14 Craft).\n')
    return m


# =============================================================================
# 13. CLI ENTRYPOINT
# =============================================================================
BUILD = {
    167: build_167,
    552: build_552,
    560: build_560,
    561: build_561,
    566: build_566,
    568: build_568,
    577: build_577,
    578: build_578,
    579: build_579,
}


def main():
    ids = [int(a) for a in sys.argv[1:] if a.isdigit()] or sorted(BUILD)
    for mid in ids:
        print(f'=== Building Wave 13 Map {mid} ===')
        BUILD[mid]()


if __name__ == '__main__':
    main()
