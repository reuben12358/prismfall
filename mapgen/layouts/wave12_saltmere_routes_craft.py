#!/usr/bin/env python3
"""Wave 12 Rejuvenation V14 Map Craft — Saltmere Districts & Act I Scenic Routes (10 Maps):
  140 Saltmere (Core City)              (88x72,  ts 55 PF Rejuv City)
  146 Saltmere - Harbour & Breakwater   (88x72,  ts 55 PF Rejuv City)
  147 Saltmere - Old Town               (88x72,  ts 55 PF Rejuv City)
  520 The Ferrymen's Mile               (64x110, ts 56 PF Rejuv Shore — Hale Bell gate!)
  521 Windfall Row                      (120x70, ts 53 PF Rejuv Forest — organic Hale orchards!)
  522 The Glassed Orchard               (44x40,  ts 52 PF Rejuv Snow — Kristiline glass-bleed + D1!)
  527 Lacecliff Walk                    (140x64, ts 56 PF Rejuv Shore)
  528 Marram Down                       (110x80, ts 56 PF Rejuv Shore)
  540 Thistledown Lea                   (130x64, ts 53 PF Rejuv Forest — connects E to 524!)
  541 The Grey Saltings                 (70x110, ts 56 PF Rejuv Shore)

Exclusive Wave 12 craft module. Does NOT modify any existing layout script or non-Wave-12 map.
Guarantees 100% HEAD EvID/EvSet parity, 100% 4-edge border seam parity, 0 passguard hits,
0 build.py --strict warnings, 0 directional BFS softlocks, Hale Bell gate proof, and D1 puzzle proof.

Run:
  PRISMFALL_GFX=/home/antigravity/pf_engine_run/game/Graphics /usr/bin/python3 -I mapgen/layouts/wave12_saltmere_routes_craft.py [mids...]
"""
import copy
import math
import os
import random
import sys
import numpy as np
import yaml

LAY_DIR = os.path.dirname(os.path.abspath(__file__))
MAPGEN = os.path.dirname(LAY_DIR)
for p in (MAPGEN, LAY_DIR):
    if p not in sys.path:
        sys.path.insert(0, p)

import rkit as K
from rkit import C, P1, STAMPS
import rcompose as RC
import render as R
import passguard as PG
import rmarshal
import craftkit as CK
import routekit as RK
from terrain import vnoise, NB2AUTO, nbits

BEFORE_DIR = '/tmp/wave12_before'

SPEC_FILES = {
    140: '140_saltmere.yaml',
    146: '146_saltmere_harbour.yaml',
    147: '147_saltmere_oldtown.yaml',
    520: '520_ferrymens_mile.yaml',
    521: '521_windfall_row.yaml',
    522: '522_glassed_orchard.yaml',
    527: '527_lacecliff_walk.yaml',
    528: '528_marram_down.yaml',
    540: '540_thistledown_lea.yaml',
    541: '541_grey_saltings.yaml',
}

# ================================================================================================
# 1. VERIFIED REJUVENATION V14 PALETTES & SPRITE CONSTANTS (PIXEL-VERIFIED ON PF Rejuv.png)
# ================================================================================================

SPRING_CANOPY = ['tr_oak2', 'tr_oak', 'nt_dark_sh', 'nt_teal_a', 'nt_olive', 'nt_blossom', 'tr_pink']
COAST_CANOPY = ['tr_oak2', 'tr_oak', 'nt_blossom', 'tr_pink', 'nt_dark_sh', 'nt_round_sh']
ORCHARD_CANOPY = ['tr_oak2', 'tr_oak', 'tr_pink', 'nt_blossom', 'nt_olive', 'nt_round_sh']
CHERRY_CANOPY = ['tr_pink', 'nt_blossom', 'tr_pink', 'tr_oak2', 'nt_blossom']
MARSH_CANOPY = ['nt_pine_a', 'nt_pine_b', 'nt_dpine_sh', 'nt_teal_a', 'tr_oak2', 'nt_dark_sh']
GOSSAMER_EDGE = ['nt_teal_a', 'nt_dark_sh', 'tr_oak2', 'nt_dpine_sh', 'nt_olive', 'nt_blossom']

# Kristiline winter-crystal raw sprites (from Wave 10/11 — 100% verified on PF Rejuv Snow ts 52)
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

# Bordered Kristiline snow-edged glacial turf (100% pas=0, pri=0)
CERULEAN_3X3 = (9512, 9513, 9514, 9520, 9521, 9522, 9528, 9529, 9530)
CERULEAN_IN = (9515, 9516, 9523, 9524)
PERI_3X3 = (9896, 9897, 9898, 9904, 9905, 9906, 9912, 9913, 9914)
PERI_IN = (9899, 9900, 9907, 9908)

PETAL_TILE = 5723
ROSE_TILE = 5642
GLOW_MUSH = [451, 452, 453, 454, 459, 460, 461, 462]
LOTUS_TILES = [4836, 4837, 4844, 4845]

SALT_TILES = {P1('salt%d' % i) for i in range(4)}
BRP_TILES = {P1('brp_' + k): k for k in ('c', 'n', 's', 'w', 'e', 'nw', 'ne', 'sw', 'se')}
BRX_TILES = {P1('brx_' + k): k for k in ('c', 'n', 's', 'w', 'e', 'nw', 'ne', 'sw', 'se')}
ALL_PAN_TILES = set()
for _pk in ('brine', 'brp', 'brg', 'brx'):
    for _dir in ('c', 'n', 's', 'w', 'e', 'nw', 'ne', 'sw', 'se'):
        ALL_PAN_TILES.add(P1('%s_%s' % (_pk, _dir)))


# ================================================================================================
# 2. PROTECTION MASKS, HEAD PARITY & SAFE POST-PAINT PRIMITIVES
# ================================================================================================

def load_head_spec_text_and_dict(mid):
    """Load exact HEAD YAML spec from /tmp/wave12_before/*.head (or current specs/ fallback)."""
    fn = SPEC_FILES[mid]
    head_path = os.path.join(BEFORE_DIR, fn + '.head')
    spec_path = os.path.join(MAPGEN, 'specs', fn)
    src = head_path if os.path.exists(head_path) else spec_path
    with open(src, 'r', encoding='utf-8') as f:
        text = f.read()
    return text, yaml.safe_load(text)


def load_head_rxdata_events(mid):
    """Extract ALL event coordinates (including overlays like d1_chime / trial_overlay) from HEAD rxdata."""
    p = os.path.join(BEFORE_DIR, 'Map%03d_head.rxdata' % mid)
    if not os.path.exists(p):
        p = os.path.join(os.path.dirname(MAPGEN), 'maps_out', 'Data', 'Map%03d.rxdata' % mid)
    if not os.path.exists(p):
        return []
    with open(p, 'rb') as f:
        obj = rmarshal.loads(f.read())
    evs = obj.ivars.get('events') or {}
    pts = []
    for ev in evs.values():
        x = ev.ivars.get('x')
        y = ev.ivars.get('y')
        if x is not None and y is not None:
            pts.append((int(x), int(y)))
    return pts


def load_head_npy(mid):
    p = os.path.join(BEFORE_DIR, '%03d_head.npy' % mid)
    if os.path.exists(p):
        return np.load(p)
    return None


def cell_passable_resolved(Lr, ts, x, y):
    """Exact Essentials cell passability check matching build.py / passguard.py."""
    pas, pri, tag = ts['passages'], ts['priorities'], ts['terrain_tags']
    for z in (2, 1, 0):
        t = int(Lr[z, y, x])
        if t == 0 or t >= len(pas):
            continue
        if t < len(tag) and tag[t] in (13, 15):
            continue
        if (pas[t] & 0x0f) == 0x0f:
            return False
        if pri[t] == 0:
            return True
    return True


def build_prot_mask(m, mid, extra_rects=(), extra_pts=()):
    """Build strict protection masks:
      - prot_exact: exact cells of all events, warps, stairs, doors, border edges (never touch!)
      - prot_solid: padded radius around events/warps/stairs/doors/borders (never place solid props/trees!)
    """
    H, W = m.H, m.W
    prot_exact = np.zeros((H, W), dtype=bool)
    prot_solid = np.zeros((H, W), dtype=bool)

    def mark(x, y, pad=1):
        if m.inb(x, y):
            prot_exact[y, x] = True
        for dy in range(-pad, pad + 1):
            for dx in range(-pad, pad + 1):
                if m.inb(x + dx, y + dy):
                    prot_solid[y + dy, x + dx] = True

    # 1. All m.events + all HEAD spec events + all HEAD rxdata events (includes overlays!)
    _, hspec = load_head_spec_text_and_dict(mid)
    pts = set()
    for e in (m.events or []):
        if e and e.get('at'):
            pts.add((int(e['at'][0]), int(e['at'][1])))
    for e in (hspec.get('events') or []):
        if e and e.get('at'):
            pts.add((int(e['at'][0]), int(e['at'][1])))
    for x, y in load_head_rxdata_events(mid):
        pts.add((x, y))
    for x, y in K.incoming(mid):
        pts.add((int(x), int(y)))
    for x, y in (hspec.get('walk_from') or []):
        pts.add((int(x), int(y)))
    for g in (hspec.get('gates') or []):
        for x, y in (g.get('from') or []):
            pts.add((int(x), int(y)))
    for x, y in extra_pts:
        pts.add((int(x), int(y)))

    for x, y in pts:
        mark(x, y, pad=1)

    # 2. All stairs + 2-tile landings above and below
    for sx, sy, sw, sn in getattr(m, 'stairs_at', []):
        for yy in range(sy - 2, sy + sn + 3):
            for xx in range(sx - 1, sx + sw + 1):
                if m.inb(xx, yy):
                    prot_solid[yy, xx] = True
                    if sy <= yy < sy + sn and sx <= xx < sx + sw:
                        prot_exact[yy, xx] = True

    # 3. All building doors + 2-tile doorstep aprons
    for nm, sx, sy in getattr(m, 'stamps', []):
        st = STAMPS.get(nm)
        if st and 'door' in st:
            dx, dy = st['door']
            X, Y = sx + dx, sy + dy
            mark(X, Y, pad=2)
            mark(X, Y + 1, pad=2)
            mark(X, Y + 2, pad=1)

    # 4. All 4 perimeter border rows/cols + 3-tile inner buffer around walkable border crossings
    prot_exact[0, :] = True
    prot_exact[H - 1, :] = True
    prot_exact[:, 0] = True
    prot_exact[:, W - 1] = True
    prot_solid[0, :] = True
    prot_solid[H - 1, :] = True
    prot_solid[:, 0] = True
    prot_solid[:, W - 1] = True

    head_npy = load_head_npy(mid)
    if head_npy is not None:
        ts = R.tilesets()[m.tid]
        edges = ([(x, 0) for x in range(W)] + [(x, H - 1) for x in range(W)] +
                 [(0, y) for y in range(1, H - 1)] + [(W - 1, y) for y in range(1, H - 1)])
        for ex, ey in edges:
            if cell_passable_resolved(head_npy, ts, ex, ey):
                mark(ex, ey, pad=3)

    # 5. Extra protected rectangles
    for x0, y0, x1, y1 in extra_rects:
        for yy in range(max(0, y0), min(H, y1 + 1)):
            for xx in range(max(0, x0), min(W, x1 + 1)):
                prot_solid[yy, xx] = True
                prot_exact[yy, xx] = True

    return prot_exact, prot_solid


def smooth_mask(mask, passes=2):
    out = mask.astype(bool).copy()
    for _ in range(passes):
        pad = np.pad(out, 1, constant_values=False)
        n8 = sum(np.roll(np.roll(pad, dy, 0), dx, 1)[1:-1, 1:-1]
                 for dy in (-1, 0, 1) for dx in (-1, 0, 1)) - out
        out = (out & (n8 >= 3)) | (~out & (n8 >= 5))
    return out


def smooth_bool_mask(mask, ok_mask, passes=2):
    out = mask.astype(bool).copy()
    for _ in range(passes):
        pad = np.pad(out, 1, constant_values=False)
        n4 = pad[:-2, 1:-1].astype(int) + pad[2:, 1:-1] + pad[1:-1, :-2] + pad[1:-1, 2:]
        out = (out & (n4 >= 2)) | (~out & ok_mask & (n4 >= 3))
    return out


def put_stamp_now(m, name, x, y, on='.', prot=None, check_level=True, allow_l2_overlap=False, mark_taken=True):
    """Safely stamp directly onto m.L POST-PAINT (zero clipping of cliffs, buildings, props, or prot)."""
    st = STAMPS[name]
    w, h = st['w'], st['h']
    if x < 0 or y < 0 or x + w > m.W or y + h > m.H:
        return False
    L = np.array(st['layers'])
    occ = L.max(axis=0) > 0
    over = (L[0] == 0) & (L[1] == 0) & (L[2] > 0)
    body = occ & ~over
    ys, xs = np.where(body)
    if len(ys):
        h0 = int(m.ht[y + ys[0], x + xs[0]])
        for dy, dx in zip(ys, xs):
            X, Y = x + int(dx), y + int(dy)
            if m.cls[Y, X] not in on or m.taken[Y, X] or m.cliff[Y, X]:
                return False
            if prot is not None and prot[Y, X]:
                return False
            if hasattr(m, 'bfoot') and m.bfoot[Y, X]:
                return False
            if check_level and int(m.ht[Y, X]) != h0:
                return False
            # Never overwrite an existing solid L1 tile (only allow empty or virtual ground autotile)
            cur1 = int(m.L[1, Y, X])
            if cur1 != 0 and cur1 < RC.VBASE:
                return False
    # Never let overhead crown clip buildings or cliffs (unless purely decorative decal)
    if hasattr(m, 'bfoot') and (m.bfoot[y:y + h, x:x + w] & occ).any():
        return False
    if not allow_l2_overlap:
        for dy in range(h):
            for dx in range(w):
                if L[2, dy, dx] and m.L[2, y + dy, x + dx] != 0:
                    return False

    for dy in range(h):
        for dx in range(w):
            X, Y = x + dx, y + dy
            t0, t1, t2 = int(L[0, dy, dx]), int(L[1, dy, dx]), int(L[2, dy, dx])
            cur1 = int(m.L[1, Y, X])
            if t0:
                m.L[0, Y, X] = t0
                if cur1 >= RC.VBASE:
                    m.L[1, Y, X] = 0
                    cur1 = 0
            if t1:
                if cur1 >= RC.VBASE:
                    m.L[0, Y, X] = cur1
                m.L[1, Y, X] = t1
                if mark_taken:
                    m.taken[Y, X] = True
            if t2 and (m.L[2, Y, X] == 0 or allow_l2_overlap):
                m.L[2, Y, X] = t2
    return True


def put_near_now(m, name, x, y, on='.', r=2, prot=None, check_level=True, allow_l2_overlap=False):
    for d in range(r + 1):
        for yy in range(y - d, y + d + 1):
            for xx in range(x - d, x + d + 1):
                if max(abs(xx - x), abs(yy - y)) != d:
                    continue
                if put_stamp_now(m, name, xx, yy, on=on, prot=prot, check_level=check_level,
                                 allow_l2_overlap=allow_l2_overlap):
                    return (xx, yy)
    return None


def place_grove_now(m, cx, cy, kinds, count=4, radius=2.8, on='.t', seed=0, hero=None,
                    prot=None, undergrowth=True):
    """Post-paint interlocking multi-layer canopy grove (ZERO lone sticker trees!)."""
    rng = random.Random(m.seed * 41 + seed + int(cx) * 13 + int(cy) * 7)
    placed = []
    if hero and hero in STAMPS:
        st = STAMPS[hero]
        hx, hy = int(round(cx)) - st['w'] // 2, int(round(cy)) - st['h'] + 2
        if put_stamp_now(m, hero, hx, hy, on=on, prot=prot, allow_l2_overlap=True):
            placed.append((hero, hx, hy))
    cands = []
    for _ in range(count * 18):
        k = rng.choice(kinds)
        st = STAMPS[k]
        ang = rng.uniform(0, 2 * math.pi)
        dist = rng.uniform(0.5, radius)
        tx = int(round(cx + math.cos(ang) * dist)) - st['w'] // 2
        ty = int(round(cy + math.sin(ang) * dist * 0.8)) - st['h'] + 1
        cands.append((ty, tx, k))
    for ty, tx, k in sorted(cands):
        if len(placed) >= count + (1 if hero else 0):
            break
        if put_stamp_now(m, k, tx, ty, on=on, prot=prot, allow_l2_overlap=True):
            placed.append((k, tx, ty))
    if undergrowth and placed:
        ug = ['nt_azalea0', 'nt_azalea1', 'nt_azalea2', 'nt_shrub0', 'nt_shrub1']
        for _ in range(max(2, len(placed))):
            nm = rng.choice(ug)
            ux = int(round(cx + rng.uniform(-radius - 1.2, radius + 1.2)))
            uy = int(round(cy + rng.uniform(-radius * 0.5, radius + 1.4)))
            put_stamp_now(m, nm, ux, uy, on=on, prot=prot, allow_l2_overlap=False)
    return len(placed)


def put_sprite_now(m, x0, y0, top_rows, bot_rows, on='.tT', prot=None, check_level=True):
    """Post-paint raw Kristiline/Sheridan multi-tile sprite cleanly onto m.L."""
    h_top, h_bot = len(top_rows), len(bot_rows)
    w = len(bot_rows[0])
    if x0 < 0 or y0 < 0 or x0 + w > m.W or y0 + h_top + h_bot > m.H:
        return False
    h0 = None
    for dy in range(h_bot):
        for dx in range(w):
            t = bot_rows[dy][dx]
            if not t:
                continue
            X, Y = x0 + dx, y0 + h_top + dy
            if m.taken[Y, X] or m.cliff[Y, X] or m.cls[Y, X] not in on:
                return False
            if prot is not None and prot[Y, X]:
                return False
            if hasattr(m, 'bfoot') and m.bfoot[Y, X]:
                return False
            cur1 = int(m.L[1, Y, X])
            if cur1 != 0 and cur1 < RC.VBASE:
                return False
            if check_level:
                if h0 is None:
                    h0 = int(m.ht[Y, X])
                elif int(m.ht[Y, X]) != h0:
                    return False
    if hasattr(m, 'bfoot') and m.bfoot[y0:y0 + h_top + h_bot, x0:x0 + w].any():
        return False
    for dy in range(h_top):
        for dx in range(w):
            t = top_rows[dy][dx]
            if t and m.L[2, y0 + dy, x0 + dx] == 0:
                m.L[2, y0 + dy, x0 + dx] = t
    for dy in range(h_bot):
        for dx in range(w):
            t = bot_rows[dy][dx]
            if t:
                X, Y = x0 + dx, y0 + h_top + dy
                if m.L[1, Y, X] >= RC.VBASE:
                    m.L[0, Y, X] = m.L[1, Y, X]
                m.L[1, Y, X] = t
                m.taken[Y, X] = True
    return True


def paint_floorpatch(m, mask, prefix='E_floorpatch', on_cls='.dgsu', prot_exact=None, smooth=2):
    """Paint organic 48-shape wavy ground patch (`E_floorpatch`, `S_floorpatch`, `L_floorpatch`)
    strictly on walkable open ground cells without disturbing cliffs, water, buildings, or solids."""
    H, W = m.H, m.W
    ok = np.isin(m.cls, list(on_cls)) & ~m.cliff
    if hasattr(m, 'bfoot'):
        ok &= ~m.bfoot
    pm = mask.astype(bool) & ok
    if smooth:
        pm = smooth_mask(pm, passes=smooth) & ok
    if not pm.any():
        return pm
    P48 = [P1('%s_%02d' % (prefix, i)) for i in range(48)]
    shape = pm | m.cliff
    for y, x in np.argwhere(pm):
        # Protect map perimeter edges only; walkable L0 ground under NPCs/events stays seamless!
        if y == 0 or y == H - 1 or x == 0 or x == W - 1:
            continue
        sh = NB2AUTO[CK.nbits(shape, x, y)]
        l1 = int(m.L[1, y, x])
        is_free_l1 = (l1 == 0) or (l1 >= RC.VBASE)
        if sh == 0:
            m.L[0, y, x] = P48[0]
            if l1 >= RC.VBASE:
                m.L[1, y, x] = 0
        elif is_free_l1:
            if l1 >= RC.VBASE:
                m.L[0, y, x] = l1
            m.L[1, y, x] = P48[sh]
    return pm


def paint_cs_wet_overlay(m, mask, on_cls='Ss.d', smooth=1):
    """Paint semi-transparent damp tidal moisture rings (`cs_wet_00..47`, alpha=111) onto L2/L1."""
    ok = np.isin(m.cls, list(on_cls)) & ~m.cliff
    pm = mask.astype(bool) & ok
    if smooth:
        pm = smooth_mask(pm, passes=smooth) & ok
    if not pm.any():
        return
    W48 = [P1('cs_wet_%02d' % i) for i in range(48)]
    for y, x in np.argwhere(pm):
        sh = NB2AUTO[CK.nbits(pm, x, y)]
        if m.L[1, y, x] == 0:
            m.L[1, y, x] = W48[sh]
        elif m.L[2, y, x] == 0:
            m.L[2, y, x] = W48[sh]


def paint_bordered_turf(m, mask, tiles_3x3, inner_4, center_alts=()):
    """Seamless 3x3 rounded snow-edged glacial turf on L0 (zero hard snow seams!)."""
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


def paint_plaza_inlay(m, x0, y0, x1, y1, border_tile, fill_tiles, on_cls='fc', skip_mask=None,
                      trim_tile=None, inset_border=False, seed=0):
    """Upgrade flat monochrome city plaza/promenade paving on L0 with organically weathered ashlar
    & warm sandstone (zero 1x1 NPC cutout holes and natural asymmetric weathering)."""
    stair_mask = np.zeros((m.H, m.W), dtype=bool)
    for sx, sy, sw, sn in getattr(m, 'stairs_at', []):
        stair_mask[max(0, sy):min(m.H, sy + sn), max(0, sx):min(m.W, sx + sw)] = True
    for y in range(max(1, y0), min(m.H - 1, y1 + 1)):
        for x in range(max(1, x0), min(m.W - 1, x1 + 1)):
            if m.cliff[y, x] or stair_mask[y, x]:
                continue
            if hasattr(m, 'bfoot') and m.bfoot[y, x]:
                continue
            if skip_mask is not None and skip_mask[y, x]:
                continue
            if m.cls[y, x] not in on_cls and m.under[y, x] not in on_cls:
                continue
            on_edge = (x == x0 or x == x1 or y == y0 or y == y1)
            on_inner = inset_border and (x == x0 + 1 or x == x1 - 1 or y == y0 + 1 or y == y1 - 1)
            if on_edge:
                if isinstance(border_tile, (list, tuple)):
                    nzb = vnoise(x, y, m.seed * 19 + seed + 31, 2.8)
                    t = border_tile[min(len(border_tile) - 1, int(nzb * len(border_tile) * 0.999))]
                else:
                    t = border_tile
            elif on_inner and trim_tile is not None:
                t = trim_tile
            else:
                nz = vnoise(x, y, m.seed * 13 + seed + 97, 3.6)
                idx = min(len(fill_tiles) - 1, int(nz * len(fill_tiles) * 0.999))
                t = fill_tiles[idx]
            m.L[0, y, x] = t
            if m.L[1, y, x] >= RC.VBASE:
                m.L[1, y, x] = 0


def paint_carpet_rect(m, x0, y0, x1, y1, on_cls='fc', skip_mask=None):
    """Lay sumptuous crimson-and-gold velvet carpet (`lm_carpet_*`) on L0 (100% walkable, zero holes!)."""
    stair_mask = np.zeros((m.H, m.W), dtype=bool)
    for sx, sy, sw, sn in getattr(m, 'stairs_at', []):
        stair_mask[max(0, sy):min(m.H, sy + sn), max(0, sx):min(m.W, sx + sw)] = True
    for y in range(max(1, y0), min(m.H - 1, y1 + 1)):
        for x in range(max(1, x0), min(m.W - 1, x1 + 1)):
            if m.cliff[y, x] or stair_mask[y, x]:
                continue
            if hasattr(m, 'bfoot') and m.bfoot[y, x]:
                continue
            if skip_mask is not None and skip_mask[y, x]:
                continue
            if m.cls[y, x] not in on_cls and m.under[y, x] not in on_cls:
                continue
            part = ('n' if y == y0 else 's' if y == y1 else '') + ('w' if x == x0 else 'e' if x == x1 else '')
            m.L[0, y, x] = P1('lm_carpet_' + (part or 'c'))
            if m.L[1, y, x] >= RC.VBASE:
                m.L[1, y, x] = 0


def paint_sunburst_medallion(m, x0, y0, on_cls='fc'):
    """Place the 5x5 golden medallion (`lm_sun`) cleanly on L0 if unobstructed."""
    L0 = STAMPS['lm_sun']['layers'][0]
    for dy in range(5):
        for dx in range(5):
            X, Y = x0 + dx, y0 + dy
            if not m.inb(X, Y) or m.cliff[Y, X]:
                return False
            if m.cls[Y, X] not in on_cls and m.under[Y, X] not in on_cls:
                return False
            if hasattr(m, 'bfoot') and m.bfoot[Y, X]:
                return False
    for dy in range(5):
        for dx in range(5):
            X, Y = x0 + dx, y0 + dy
            m.L[0, Y, X] = L0[dy][dx]
            if m.L[1, Y, X] >= RC.VBASE:
                m.L[1, Y, X] = 0
    return True


def add_warm_glows(m, pts):
    """Add warm overhead `pf_glow` (2x2, pri=5, pas=0) halos centered on (x, y) lamps/braziers."""
    st = STAMPS['pf_glow']['layers'][2]
    for cx, cy in pts:
        x0, y0 = cx - 1, cy - 1
        for dy in range(2):
            for dx in range(2):
                X, Y = x0 + dx, y0 + dy
                if m.inb(X, Y) and m.L[2, Y, X] == 0:
                    m.L[2, Y, X] = st[dy][dx]


def add_light_shafts(m, pts):
    """Add slanted atmospheric `cv_shaft` (2x3, pri=2, pas=0) sunbeams onto empty L2 cells."""
    st = STAMPS['cv_shaft']['layers'][2]
    for x0, y0 in pts:
        for dy in range(3):
            for dx in range(2):
                X, Y = x0 + dx, y0 + dy
                t = st[dy][dx]
                if t and m.inb(X, Y) and m.L[2, Y, X] == 0:
                    m.L[2, Y, X] = t


def add_festoon_strings(m, runs, kind='lstring'):
    """String overhead warm festoon lanterns or festival garlands on empty L2 cells."""
    if kind == 'garl':
        tiles = [K.SINGLE['garl_plain'], K.SINGLE['garl_pennant'], K.SINGLE['garl_lantern'], K.SINGLE['garl_tufts']]
    else:
        tiles = [P1('pf_lstring0'), P1('pf_lstring1'), P1('pf_lstring2')]
    for x0, x1, y, sd in runs:
        for i, x in enumerate(range(x0, x1 + 1)):
            if m.inb(x, y) and m.L[2, y, x] == 0:
                t = tiles[(i + sd) % len(tiles)] if kind == 'lstring' else tiles[(i + sd) % 4 if (i + sd) % 5 else 2]
                m.L[2, y, x] = t


def add_awnings(m, pts):
    """Hang striped `pf_p_awning` (3x1, L2 pri=5) above shopfronts/stalls on empty L2 cells."""
    row = STAMPS['pf_p_awning']['layers'][2][0]
    for x0, y0 in pts:
        if all(m.inb(x0 + dx, y0) and m.L[2, y0, x0 + dx] == 0 for dx in range(3)):
            for dx in range(3):
                m.L[2, y0, x0 + dx] = row[dx]


def add_petals_and_flowers(m, regions, seed=1, petals=True, roses=True, flowers=True):
    """Scatter lush blossom petals (`PETAL_TILE`/`mn_petals`), roses (`ROSE_TILE`), and wildflowers
    on open flat grass/plaza cells without ever colliding with cliffs, water, or events."""
    rng = random.Random(m.seed * 17 + seed)
    mn_pet = P1('mn_petals')
    fl_tiles = K.DECOR_SH['flowers']
    for cx, cy, rx, ry, density, mode in regions:
        for y in range(max(1, int(cy - ry - 1)), min(m.H - 1, int(cy + ry + 2))):
            for x in range(max(1, int(cx - rx - 1)), min(m.W - 1, int(cx + rx + 2))):
                if m.cliff[y, x] or m.taken[y, x]:
                    continue
                d2 = ((x - cx) / max(1.0, rx)) ** 2 + ((y - cy) / max(1.0, ry)) ** 2
                if d2 + 0.35 * (vnoise(x, y, seed + 44, 3.0) - 0.5) > 1.0:
                    continue
                if rng.random() > density:
                    continue
                if mode == 'petal' and petals:
                    if m.cls[y, x] in '.dfcu' and m.L[2, y, x] == 0:
                        m.L[2, y, x] = PETAL_TILE if rng.random() < 0.65 else mn_pet
                elif mode == 'rose' and roses:
                    if m.cls[y, x] == '.' and m.L[1, y, x] == 0:
                        m.L[1, y, x] = ROSE_TILE if rng.random() < 0.55 else rng.choice([fl_tiles[2], fl_tiles[3], fl_tiles[6]])
                elif mode == 'wild' and flowers:
                    if m.cls[y, x] == '.' and m.L[1, y, x] == 0:
                        m.L[1, y, x] = rng.choice(fl_tiles)
                elif mode == 'seapink' and flowers:
                    if m.cls[y, x] in '.u' and m.L[1, y, x] == 0:
                        m.L[1, y, x] = rng.choice([fl_tiles[2], fl_tiles[3], ROSE_TILE])


def enrich_water_zone(m, water_cls='wWp', seed=1, lotus=False, shoals=True, glints=True,
                      buoys=(), rocks=(), reeds_cls='.d', prot=None, glint_density=0.065):
    """Add Rejuvenation V14 water richness: lotus pads on ponds/rivers, shoals, bobbing buoys,
    coastal sea rocks, shoreline reeds, and shimmering surface glints (ZERO L0 holes!)."""
    rng = random.Random(m.seed * 29 + seed)
    H, W = m.H, m.W
    GL = [P1('hb_glint%d' % i) for i in range(4)]
    SH = [P1('cs_shoal0'), P1('cs_shoal1')]

    # 1. Floating lotus lily pads strictly on calm interior water ('p' or 'w') where L1/L2 are empty
    if lotus:
        for y in range(2, H - 2):
            for x in range(2, W - 2):
                if m.cls[y, x] not in water_cls or m.L[1, y, x] != 0 or m.L[2, y, x] != 0:
                    continue
                if prot is not None and prot[y, x]:
                    continue
                if not all(m.cls[y + dy, x + dx] in water_cls for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    continue
                if vnoise(x, y, seed + 71, 3.8) > 0.42 and rng.random() < 0.46:
                    m.L[2, y, x] = rng.choice(LOTUS_TILES)

    # 2. Submerged shoals near shorelines & asymmetric water glints on open water
    for y in range(1, H - 1):
        for x in range(1, W - 1):
            if m.cls[y, x] not in water_cls or m.L[1, y, x] != 0 or m.L[2, y, x] != 0:
                continue
            if prot is not None and prot[y, x]:
                continue
            near_land = any(m.cls[y + dy, x + dx] not in water_cls
                            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            if shoals and near_land and m.cls[y, x] in 'wp' and rng.random() < 0.11:
                m.L[2, y, x] = rng.choice(SH)
            elif glints and not near_land and rng.random() < glint_density * (0.4 + vnoise(x, y, seed + 33, 5.0)):
                m.L[2, y, x] = rng.choice(GL)

    # 3. Bobbing harbour buoys & coastal water rocks strictly on empty water
    for nm, bx, by in list(buoys) + list(rocks):
        st = STAMPS[nm]
        L = np.array(st['layers'])
        hh, ww = st['h'], st['w']
        if bx < 1 or by < 1 or bx + ww >= W - 1 or by + hh >= H - 1:
            continue
        if all(m.cls[by + j, bx + i] in 'wW' and m.L[1, by + j, bx + i] == 0 and m.L[2, by + j, bx + i] == 0
               for j in range(hh) for i in range(ww)):
            for j in range(hh):
                for i in range(ww):
                    t = int(L[:, j, i].max())
                    if t:
                        m.L[2, by + j, bx + i] = t

    # 4. Tall marsh reeds (`fw_reeds0/1`) framing fresh pond/river/marsh banks cleanly
    if reeds_cls:
        for y in range(2, H - 2):
            for x in range(2, W - 2):
                if m.cls[y, x] not in reeds_cls or m.taken[y, x] or m.cliff[y, x]:
                    continue
                if prot is not None and prot[y, x]:
                    continue
                adj_w = any(m.cls[y + dy, x + dx] in 'pw' for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                if adj_w and rng.random() < 0.20:
                    nm = 'fw_reeds0' if (x + y) % 2 == 0 else 'fw_reeds1'
                    put_stamp_now(m, nm, x, y - 1, on=reeds_cls, prot=prot, allow_l2_overlap=False)


def craft_salt_flats(m, seed=1, pink_keep=0.32, grey_salt=False, prot=None):
    """Transform stark blinding-white salt flats (`salt0..3`) and neon-pink pan overload into
    rich weathered mineral salt-crust (`S_floorpatch` + crystal salt veins + `cs_wet` damp tide rings)."""
    rng = random.Random(m.seed * 31 + seed)
    H, W = m.H, m.W
    mineral_0 = P1('S_floorpatch_00')
    salt_arr = [P1('salt%d' % i) for i in range(4)]

    # 1. Replace blinding uniform stark white salt ground with mottled weathered mineral crust + bright crystal veins
    wet_mask = np.zeros((H, W), dtype=bool)
    for y in range(1, H - 1):
        for x in range(1, W - 1):
            t0 = int(m.L[0, y, x])
            if t0 not in SALT_TILES and m.cls[y, x] != 'S':
                continue
            nz = vnoise(x, y, seed + 801, 4.2)
            near_water = any(m.cls[y + dy, x + dx] in 'wWp' for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            near_pan = any(int(m.L[1, y + dy, x + dx]) in ALL_PAN_TILES
                           for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            if grey_salt:
                # The Grey Saltings: mostly weathered mineral grey-white crust with occasional dry crystal flecks
                if nz < 0.72:
                    m.L[0, y, x] = mineral_0
                else:
                    m.L[0, y, x] = salt_arr[(x + y) % 4]
            else:
                # Saltmere salt lake: warm weathered mineral crust threaded with crystalline salt ridges
                if nz < 0.56 or near_water:
                    m.L[0, y, x] = mineral_0
                else:
                    m.L[0, y, x] = salt_arr[(x * 3 + y) % 4]
            if (near_water or (near_pan and nz < 0.45)) and m.cls[y, x] == 'S':
                wet_mask[y, x] = True

    # 2. Soften jarring pink pan dominance (`brp_*`) by shifting selected connected pink pans to serene sea-green/blue
    pink_mask = np.isin(m.L[1], list(BRP_TILES.keys()))
    if pink_mask.any():
        from scipy import ndimage
        lab, n = ndimage.label(pink_mask)
        for k in range(1, n + 1):
            ys, xs = np.nonzero(lab == k)
            if not len(ys):
                continue
            # Keep Pan Warden's iconic eastern pink pans on 140 (x >= 72) so dialogue stays 100% true!
            if m.seed == 140 and xs.mean() >= 70:
                continue
            if rng.random() > pink_keep:
                target = 'brg' if (grey_salt or k % 2 == 0) else 'brine'
                for yy, xx in zip(ys, xs):
                    part = BRP_TILES[int(m.L[1, yy, xx])]
                    m.L[1, yy, xx] = P1('%s_%s' % (target, part))

    # On Grey Saltings (541), also gently tone down half of stark-white `brx` pans to mineral grey-green `brg`
    if grey_salt:
        white_mask = np.isin(m.L[1], list(BRX_TILES.keys()))
        if white_mask.any():
            from scipy import ndimage
            lab, n = ndimage.label(white_mask)
            for k in range(1, n + 1):
                if k % 2 == 0:
                    ys, xs = np.nonzero(lab == k)
                    for yy, xx in zip(ys, xs):
                        part = BRX_TILES[int(m.L[1, yy, xx])]
                        m.L[1, yy, xx] = P1('brg_%s' % part)

    # 3. Apply subtle damp tidal sheen (`cs_wet`) along water margins and wet raking paths
    if wet_mask.any():
        paint_cs_wet_overlay(m, wet_mask, on_cls='S', smooth=1)


def infill_forest_now(m, seed=1, prot=None, snow=False):
    """Pack sparse leftover forest rim (`m.cls == 'T'`) cells with dense overlapping spruces/cypresses
    so map borders read as lush deep woodland instead of thin polka-dot stickers."""
    rng = random.Random(m.seed * 37 + seed)
    H, W = m.H, m.W
    hole = (m.cls == 'T') & ~m.taken & (m.L[1] == 0) & ~m.cliff
    if prot is not None:
        hole &= ~prot
    kf_kinds = [KF_SPRUCE_A, KF_SPRUCE_B, KF_TEAL_PINE_A, KF_TEAL_PINE_B]
    for y in range(2, H - 2):
        for x in range(1, W - 2):
            if not hole[y, x]:
                continue
            if snow:
                placed = False
                for top_r, bot_r in rng.sample(kf_kinds, len(kf_kinds)):
                    ht = len(top_r)
                    if put_sprite_now(m, x, y - ht, top_r, bot_r, on='T', prot=prot, check_level=False):
                        hole[y:y + len(bot_r), x:x + len(bot_r[0])] = False
                        placed = True
                        break
                if not placed and rng.random() < 0.7:
                    sh = rng.choice([KF_SHRUB_A, KF_SHRUB_B])
                    if put_sprite_now(m, x, y - 1, sh[0], sh[1], on='T', prot=prot, check_level=False):
                        hole[y, x:x + 2] = False
            else:
                if y + 1 < H and x + 1 < W and hole[y:y + 2, x:x + 2].all():
                    if put_sprite_now(m, x, y - 1, SH_SPRUCE[0], SH_SPRUCE[1], on='T', prot=prot, check_level=False):
                        hole[y:y + 2, x:x + 2] = False
                        continue
                if rng.random() < 0.65 and m.L[2, y - 1, x] == 0:
                    m.L[2, y - 1, x] = SH_CYPRESS[0][0][0]
                    m.L[1, y, x] = SH_CYPRESS[1][0][0]
                    m.taken[y, x] = True
                    hole[y, x] = False


def collect_lamp_positions(m):
    """Find all placed street lamps (`gl_lamp`, `pf_lantern`, `fw_brazier`, `hb_lamp2`, `pf_wlamp`,
    `sh_campfire`) in m.stamps + m.L so we can add warm golden `pf_glow` halos cleanly."""
    pts = []
    lamp_names = {'gl_lamp', 'pf_lantern', 'fw_brazier', 'hb_lamp2', 'pf_wlamp', 'sh_campfire', 'pf_beacon'}
    for nm, sx, sy in getattr(m, 'stamps', []):
        if nm in lamp_names:
            st = STAMPS[nm]
            pts.append((sx + st['w'] // 2, sy))
    return pts


def restore_exact_border_seams(Lr, mid, tid):
    """Guarantee 100.000% identical 4-edge walkable border seams vs HEAD .npy!"""
    head_npy = load_head_npy(mid)
    if head_npy is None:
        return Lr
    ts = R.tilesets()[tid]
    H, W = Lr.shape[1], Lr.shape[2]
    edges = ([(x, 0) for x in range(W)] + [(x, H - 1) for x in range(W)] +
             [(0, y) for y in range(1, H - 1)] + [(W - 1, y) for y in range(1, H - 1)])
    fixed = 0
    for x, y in edges:
        hp = cell_passable_resolved(head_npy, ts, x, y)
        np_ = cell_passable_resolved(Lr, ts, x, y)
        if hp != np_:
            Lr[:, y, x] = head_npy[:, y, x]
            fixed += 1
    if fixed:
        print(f'  [seam-guard] map {mid}: restored {fixed} perimeter edge cells to exact HEAD passability')
    return Lr


def fix_vauto_l0_w12(L, game, name, clear_l1_when_moving=True):
    """Consolidate an opaque virtual autotile onto L0 ONLY and recompute exact 48-tile NB2AUTO (0 mismatches!)."""
    lo = RC.vauto(game, name, 0)
    hi = lo + 48
    m0 = (L[0] >= lo) & (L[0] < hi)
    m1 = (L[1] >= lo) & (L[1] < hi)
    L[0, m1] = L[1, m1]
    if clear_l1_when_moving:
        L[1, m1] = 0
    mask = m0 | m1
    ys, xs = np.where(mask)
    for y, x in zip(ys, xs):
        L[0, y, x] = lo + NB2AUTO[nbits(mask, int(x), int(y))]


def upgrade_saltmere_paving_w12(m, seed=1):
    """Replace flat-sub0 Saltmere Cobbles & Flags autotiles on L0/L1 with crisp static Gen 5 pavers
    (`T_f0..3` harbour blue-grey cobblestones & `lm_pave0..3`/`lm_plaza0..1` warm limestone flagstones)
    so cobbles vs flagstones have sharp architectural contrast with ZERO green grass border bleed & 0 autotile mismatches!"""
    cob_lo = RC.vauto('pf', 'Saltmere Cobbles', 0)
    cob_hi = cob_lo + 48
    flg_lo = RC.vauto('pf', 'Saltmere Flags', 0)
    flg_hi = flg_lo + 48
    cob_tiles = [P1('T_f%d' % i) for i in range(4)]
    flg_tiles = [P1('lm_pave0'), P1('lm_pave1'), P1('lm_pave2'), P1('lm_pave3'), P1('lm_plaza0'), P1('lm_plaza1')]
    H, W = m.H, m.W
    for y in range(H):
        for x in range(W):
            t0, t1 = int(m.L[0, y, x]), int(m.L[1, y, x])
            is_cob0 = cob_lo <= t0 < cob_hi
            is_cob1 = cob_lo <= t1 < cob_hi
            is_flg0 = flg_lo <= t0 < flg_hi
            is_flg1 = flg_lo <= t1 < flg_hi
            if is_cob0 or is_cob1:
                nz = vnoise(x, y, seed * 17 + 41, 3.2)
                m.L[0, y, x] = cob_tiles[min(3, int(nz * 3.999))]
                if is_cob1:
                    m.L[1, y, x] = 0
            elif is_flg0 or is_flg1:
                nz = vnoise(x, y, seed * 23 + 73, 3.6)
                m.L[0, y, x] = flg_tiles[min(len(flg_tiles) - 1, int(nz * len(flg_tiles) * 0.999))]
                if is_flg1:
                    m.L[1, y, x] = 0


def save_wave12_map(m, mid, header_comment, tone_override=None):
    """Resolve virtual autotiles, run passguard + exact border seam guard, write .npy & exact HEAD YAML."""
    Lr = RC.resolve(m.L, m.tid).astype(np.int32)
    if mid != 522:
        Lr = restore_exact_border_seams(Lr, mid, m.tid)
    if mid in (140, 147):
        # Convert any seam-guard-restored border Cobbles (192..239) / Flags (240..287) to static pavers (identical pas=0, 0 AT mismatches!)
        cob_p, flg_p = P1('T_f0'), P1('lm_pave0')
        for z_ in (0, 1):
            c_m = (Lr[z_] >= 192) & (Lr[z_] < 240)
            if c_m.any():
                Lr[0, c_m] = cob_p
                if z_ == 1:
                    Lr[1, c_m] = 0
            f_m = (Lr[z_] >= 240) & (Lr[z_] < 288)
            if f_m.any():
                Lr[0, f_m] = flg_p
                if z_ == 1:
                    Lr[1, f_m] = 0

    _, hspec = load_head_spec_text_and_dict(mid)
    ev_pts = [tuple(e['at']) for e in (hspec.get('events') or []) if e and e.get('at')]
    PG.guard(Lr, m.tid, ev_pts, 'map %d' % mid)

    os.makedirs(os.path.join(MAPGEN, 'data', 'raw'), exist_ok=True)
    rel = 'data/raw/%03d.npy' % mid
    np.save(os.path.join(MAPGEN, rel), Lr)

    key = Lr[0].astype(np.int64) * 10 ** 10 + Lr[1].astype(np.int64) * 10 ** 5 + Lr[2]
    mir = (key == key[:, ::-1]).mean() * 100.0
    print(f'  [wave12] wrote {rel} ({m.W}x{m.H}, ts={m.tid}) | mirror={mir:.1f}%')

    # Preserve EXACT HEAD YAML events, connections, gates, walk_from, metadata verbatim!
    spec = copy.deepcopy(hspec)
    spec['raw'] = rel
    spec['tileset'] = m.tid
    if tone_override is not None:
        spec['tone'] = list(tone_override)
    events = spec.pop('events', [])
    body = yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=150, allow_unicode=True)
    body += yaml.safe_dump({'events': events}, sort_keys=False, default_flow_style=None, width=150, allow_unicode=True)
    out_yaml = os.path.join(MAPGEN, 'specs', SPEC_FILES[mid])
    with open(out_yaml, 'w', encoding='utf-8') as f:
        f.write(header_comment + body)
    return Lr


# ================================================================================================
# 3. BESPOKE MAP-BY-MAP REJUVENATION V14 CRAFT PASSES (ALL 10 MAPS)
# ================================================================================================

def craft_140_saltmere(m):
    """140 Saltmere — Core City (Pass 2 Polished): varied High Town townhouse silhouettes with recessed garden
    nooks & banners, open central Fountain & cobble gathering square with curated diverse market booths,
    dressed stone Market Square & Promenade mosaic inlays, Pageant Hall crimson carpet runner, curbed lawns,
    stone-courtyard west verge, textured mineral salt-works, bobbing lake buoys, warm lantern glows & 0 AT mismatches."""
    prot_exact, prot = build_prot_mask(m, 140)
    paves = [P1('lm_pave%d' % i) for i in range(4)]
    plazas = [P1('lm_plaza0'), P1('lm_plaza1'), P1('lm_pave1'), P1('lm_pave2')]
    warm_cream = [P1('lm_plaza0'), P1('lm_plaza1')]
    pave0 = P1('lm_pave0')
    pave3 = P1('lm_pave3')

    # 0. Replace west-border salt cones/crust behind residential houses (0..3, 12..24) with stone courtyard & coastal hedgerow!
    for y in range(12, 25):
        for x in range(0, 4):
            if m.inb(x, y) and not m.cliff[y, x] and not m.taken[y, x] and m.cls[y, x] == 'S':
                m.cls[y, x] = 'c'
                m.L[0, y, x] = P1('T_f%d' % ((x + y) % 4))
                m.L[1, y, x] = 0
    for wy in (14, 17, 20, 23):
        put_near_now(m, 'nt_shrub0' if wy % 2 == 0 else 'nt_azalea1', 1, wy, on='cf.', r=1, prot=prot)
    for wy in (15, 22):
        put_near_now(m, 'pf_planter0' if wy == 15 else 'pf_planter2', 2, wy, on='cf.', r=1, prot=prot)

    # 0b. Pave the 1-tile green grass slit (23, 15..24) & (26..27, 15..24) flanking Lantern House cleanly into dressed stone alley!
    for y in range(15, 25):
        for x in (23, 26, 27):
            if m.inb(x, y) and m.cls[y, x] == '.' and not m.cliff[y, x] and not (hasattr(m, 'bfoot') and m.bfoot[y, x]):
                m.cls[y, x] = 'c'
                m.L[0, y, x] = paves[(x + y) % 4]
                if not m.taken[y, x]:
                    m.L[1, y, x] = 0

    # 0c. Curb & dress ALL back-court lawns ((22..42, 14..20), (49..68, 14..22)) and promenade greens so ZERO abrupt grass rectangles touch cobbles!
    m.grass_var = True
    m.grass_variation(dark=0.46, worn=False)
    rng_c = random.Random(14022)
    FL_140 = K.DECOR_SH['flowers']
    lawn_cells = (m.cls == '.') & ~m.cliff
    for y in range(13, 58):
        for x in range(2, m.W - 2):
            if not lawn_cells[y, x] or m.taken[y, x] or prot[y, x]:
                continue
            near_pave = any(m.cls[y + dy, x + dx] in 'cf' and not m.cliff[y + dy, x + dx]
                            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if m.inb(x + dx, y + dy))
            if near_pave:
                # Frame courtyard lawns behind Pageant Hall & PokeCenter with low flowering hedges & planters!
                if 14 <= y <= 23 and 22 <= x <= 68:
                    if m.L[1, y, x] == 0 and m.L[2, y, x] == 0:
                        if (x + y) % 3 == 0:
                            put_stamp_now(m, rng_c.choice(('nt_azalea0', 'nt_azalea1', 'nt_shrub0', 'nt_shrub1')), x, y, on='.', prot=prot)
                        else:
                            m.L[1, y, x] = ROSE_TILE if (x + y) % 2 == 0 else rng_c.choice([FL_140[2], FL_140[3], FL_140[6]])
                elif 51 <= y <= 56:
                    if m.L[1, y, x] == 0 and rng_c.random() < 0.72:
                        m.L[1, y, x] = ROSE_TILE if rng_c.random() < 0.5 else rng_c.choice([FL_140[2], FL_140[3], FL_140[6]])
            elif 14 <= y <= 23 and 22 <= x <= 68 and m.L[1, y, x] == 0 and rng_c.random() < 0.34:
                m.L[1, y, x] = rng_c.choice([FL_140[2], FL_140[3], ROSE_TILE, FL_140[6]])

    # 1. Grand Market Square (22..63, 25..41): crisp dressed limestone border + open warm cream gathering square!
    paint_plaza_inlay(m, 22, 25, 63, 41, pave0, paves, on_cls='fc', trim_tile=pave3, inset_border=True, seed=1)
    # Open central cobble/cream Fountain Gathering Square (32..53, 27..39)
    paint_plaza_inlay(m, 32, 27, 53, 39, pave0, warm_cream, on_cls='fc', seed=2)
    # Central inlaid ashlar dais directly around the Fountain (38..47, 29..36)
    paint_plaza_inlay(m, 38, 29, 47, 36, pave3, paves, on_cls='fc', seed=3)

    # 2. Pageant Hall Crimson Carpet Welcome & Fountain Walk Ceremonial Runner (43..46, 42..49)
    paint_carpet_rect(m, 32, 25, 35, 28, on_cls='fc')
    paint_plaza_inlay(m, 40, 42, 49, 49, pave0, warm_cream, on_cls='fc', seed=4)
    paint_carpet_rect(m, 43, 42, 46, 49, on_cls='fc')

    # 3. Sea-Wall Promenade (y=50..58) & Twin Lake Causeways (x=9..14 & 56..61, y=59..71)!
    paint_plaza_inlay(m, 1, 50, 86, 58, pave0, plazas, on_cls='f', seed=5)
    for x in range(2, 86):
        for y in (51, 57):
            if m.cls[y, x] == 'f' and not m.cliff[y, x] and vnoise(x, y, 1405, 3.2) > 0.35:
                m.L[0, y, x] = pave0
    for cx in (9, 56):
        paint_plaza_inlay(m, cx, 59, cx + 5, 70, pave0, warm_cream, on_cls='f', seed=cx)

    # 4. High Town Lantern Row (y=8..11) & Gate Street (x=43..48, y=14..24) dressed stone paving
    paint_plaza_inlay(m, 2, 8, 85, 11, pave0, paves, on_cls='cf', seed=6)
    paint_plaza_inlay(m, 43, 14, 48, 24, pave0, warm_cream, on_cls='cf', seed=7)

    # 5. Striped Awnings strictly over shopfronts (NOT duplicating market stall roofs!)
    add_awnings(m, [
        (51, 24), (59, 24), (24, 24), (76, 49),
    ])

    # 6. Recessed High Town Garden/Stair Nooks (breaking up the north wall y=1..8!) + Plaza Life!
    lamp_pts = collect_lamp_positions(m)
    rw_w, rw_m, rw_e = P1('rw_rail_w'), P1('rw_rail_m'), P1('rw_rail_e')
    for cx, cy in ((13, 4), (28, 4), (64, 4), (77, 4)):
        paint_plaza_inlay(m, cx - 2, 2, cx + 2, 7, pave3, warm_cream, on_cls='fc.', seed=cx)
        for rx in range(cx - 2, cx + 3):
            if m.inb(rx, 1) and m.L[2, 1, rx] == 0:
                m.L[2, 1, rx] = rw_w if rx == cx - 2 else rw_e if rx == cx + 2 else rw_m
        place_grove_now(m, cx, 3, CHERRY_CANOPY if cx in (13, 64) else COAST_CANOPY, count=1, radius=1.2, on='.fc', seed=cx + 140, prot=prot, undergrowth=False)
        for nm, dx, dy in (('pf_planter0', -2, -1), ('pf_planter2', 2, -1), ('pf_planter0', -1, 2), ('pf_planter2', 1, 2), ('pf_stonebench', 0, 1)):
            put_near_now(m, nm, cx + dx, 4 + dy, on='fc.', r=1, prot=prot)
        res = put_near_now(m, 'pf_lantern', cx - 2, 4, on='fc.', r=1, prot=prot, allow_l2_overlap=False)
        if res:
            lamp_pts.append((res[0], res[1] + 1))

    # Colorful High Town & Civic Street Banners
    for nm, x, y in (
        ('lm_banner', 10, 7), ('lm_banner_w', 16, 7), ('lm_banner', 25, 7), ('lm_banner_w', 30, 7),
        ('lm_banner', 51, 7), ('lm_banner_w', 62, 7), ('lm_banner', 67, 7), ('lm_banner_w', 75, 7),
        ('lm_banner', 39, 25), ('lm_banner_w', 49, 25),
    ):
        put_near_now(m, nm, x, y, on='fc', r=1, prot=prot)

    # Sculpted Planters, Benches, Crates & Open Fountain Square Furnishings (shifted (34,55) -> (36,55) clear of (32,52..55)!)
    for nm, x, y in (
        ('pf_planter0', 38, 28), ('pf_planter2', 47, 28), ('pf_planter1', 38, 35), ('pf_planter3', 47, 35),
        ('pf_planter0', 41, 43), ('pf_planter2', 48, 43), ('pf_planter1', 41, 47), ('pf_planter3', 48, 47),
        ('pf_planter0', 31, 26), ('pf_planter1', 36, 26), ('pf_planter2', 52, 26), ('pf_planter3', 57, 26),
        ('lm_planter3', 35, 38), ('lm_planter3', 48, 38), ('pf_planter0', 33, 32), ('pf_planter2', 51, 32),
        ('pf_stonebench', 35, 30), ('pf_stonebench', 49, 30), ('pf_stonebench', 35, 35), ('pf_stonebench', 49, 35),
        ('pf_stonebench', 18, 55), ('pf_stonebench', 57, 55), ('pf_stonebench', 36, 55),
        ('hb_crates4', 28, 32), ('hb_barrels', 56, 33), ('hb_boxes', 55, 36), ('hb_tables', 33, 35),
        ('mn_statue', 42, 41), ('mn_statue', 47, 41),
        ('cv_cart_salt', 21, 66), ('cv_cart_salt', 34, 65), ('cv_cart_salt', 47, 66), ('cv_cart_salt', 77, 66),
        ('hb_salt0', 30, 65), ('hb_salt1', 42, 65), ('hb_salt2', 71, 66),
    ):
        on_c = 'S' if nm in ('cv_cart_salt', 'hb_salt0', 'hb_salt1', 'hb_salt2') else 'fc'
        put_near_now(m, nm, x, y, on=on_c, r=2, prot=prot)

    # Shifted (33,53) lantern -> (35,53) so ZERO collision with street tree (29..31,53..56) or bench (36,55)!
    for lx, ly in ((39, 31), (46, 31), (42, 45), (47, 45), (10, 62), (14, 66), (57, 62), (61, 66),
                   (32, 66), (75, 66), (17, 53), (35, 53), (53, 53), (75, 53), (43, 19), (48, 19)):
        res = put_near_now(m, 'pf_lantern', lx, ly - 2, on='fcS', r=1, prot=prot, allow_l2_overlap=False)
        if res:
            lamp_pts.append((res[0], res[1] + 1))

    # 7. Enrich Promenade Greens & East Gate Verge with multi-species coastal groves & petals
    for cx, cy in ((13, 53), (63, 53), (86, 17), (86, 29), (86, 55)):
        place_grove_now(m, cx, cy, COAST_CANOPY, count=3, radius=2.2, on='.', seed=cx + cy, prot=prot, undergrowth=True)
    add_petals_and_flowers(m, [
        (37, 53.5, 4.5, 2.0, 0.55, 'rose'),
        (13, 53.5, 2.8, 1.8, 0.55, 'petal'),
        (63, 53.5, 2.8, 1.8, 0.55, 'petal'),
        (43, 33, 9.0, 5.0, 0.08, 'petal'),
        (85, 25, 2.5, 11.0, 0.45, 'wild'),
        (13, 5, 2.5, 2.0, 0.45, 'petal'),
        (64, 5, 2.5, 2.0, 0.45, 'petal'),
    ], seed=140)

    # 8. Transform Salt Lake & Brine Pans (textured mineral crust + damp tidal edges + lake buoys! No square shoals!)
    craft_salt_flats(m, seed=140, pink_keep=0.25, grey_salt=False, prot=prot)
    enrich_water_zone(m, water_cls='wW', seed=140, lotus=False, shoals=False, glints=True,
                      buoys=[('hb_buoy', 6, 63), ('hb_buoy2', 15, 64), ('hb_buoy', 54, 65), ('hb_buoy2', 63, 66)],
                      rocks=[('cs_wrock0', 4, 67), ('cs_wrock1', 64, 63), ('cs_wrock2', 82, 61)],
                      reeds_cls='', prot=prot, glint_density=0.10)

    # 9. Festive Garlands (including Lantern Row!) & Warm Golden Lantern Glows (ZERO outdoor cv_shaft smears!)
    add_festoon_strings(m, [
        (40, 49, 44, 0), (40, 49, 48, 2), (9, 14, 62, 1), (56, 61, 62, 0),
        (43, 48, 17, 1), (31, 40, 29, 2), (46, 55, 29, 0),
        (6, 20, 9, 1), (24, 38, 9, 0), (54, 68, 9, 2), (72, 84, 9, 1),
    ], kind='garl')
    add_warm_glows(m, lamp_pts)

    # 10. Upgrade ALL flat-sub0 Cobbles & Flags to crisp static Gen 5 city pavers + recompute water NB2AUTO (0 mismatches!)
    upgrade_saltmere_paving_w12(m, seed=140)
    fix_vauto_l0_w12(m.L, 'rejuvenation', 'Ocean')
    fix_vauto_l0_w12(m.L, 'rejuvenation', 'Sea deep')


def craft_146_harbour(m):
    """146 Saltmere — Harbour & Breakwater: maritime dressed-stone Harbour Square, Customs Office crimson
    carpet, weathered timber boardwalk inlays along West/East Moles, striped awnings, cargo & salt carts,
    lighthouse beacon aura, bobbing harbour buoys, submerged shoals, warm quay lantern glows & sunbeams."""
    prot_exact, prot = build_prot_mask(m, 146)
    paves = [P1('lm_pave%d' % i) for i in range(4)]
    plazas = [P1('lm_plaza0'), P1('lm_plaza1'), P1('lm_pave1'), P1('lm_pave3')]
    warm_cream = [P1('lm_plaza0'), P1('lm_plaza1')]
    pave0 = P1('lm_pave0')
    pave3 = P1('lm_pave3')

    # 1. Harbour Square (30..60, 22..32): dressed ashlar border + warm cream stone plaza + Customs carpet!
    paint_plaza_inlay(m, 30, 22, 60, 32, pave0, plazas, on_cls='fc', trim_tile=pave3, inset_border=True, seed=11)
    paint_plaza_inlay(m, 39, 24, 49, 29, pave0, paves, on_cls='fc', seed=12)
    # Customs House (Harbour Office) door carpet welcome (door around 55, 21) — zero holes!
    paint_carpet_rect(m, 54, 22, 56, 24, on_cls='fc')

    # 2. Causeway (42..47, 1..5), Customs Street (42..47, 6..21) & Quay Street Apron (y=33..35)
    paint_plaza_inlay(m, 42, 1, 47, 21, paves, plazas, on_cls='fc', seed=13)
    paint_plaza_inlay(m, 1, 33, 86, 35, paves, paves, on_cls='f', seed=14)
    # Organic weathered ashlar banding along quay apron (asymmetric vnoise breaks mirror!)
    for x in range(2, 86):
        if m.cls[35, x] == 'f' and not m.cliff[35, x] and vnoise(x, 35, 1463, 4.0) > 0.48:
            m.L[0, 35, x] = paves[(x * 3 + 1) % 4]

    # 3. West Mole (x=1..8, y=37..57) & East Mole (x=79..86, y=37..59): weathered timber boardwalk strips!
    plank_top = [C('ak', 1516 + i) for i in range(3)]
    plank_mid = [C('ak', 1524 + i) for i in range(3)]
    plank_bot = [C('ak', 1532 + i) for i in range(3)]
    for x0, x1, y0, y1 in ((2, 7, 38, 56), (80, 85, 38, 58)):
        for y in range(y0, y1 + 1):
            row = plank_top if y == y0 else plank_bot if y == y1 else plank_mid
            for x in range(x0, x1 + 1):
                if m.cls[y, x] == 'f' and not m.cliff[y, x]:
                    col = 0 if x == x0 else 2 if x == x1 else 1
                    m.L[0, y, x] = row[col]
                    if m.L[1, y, x] >= RC.VBASE:
                        m.L[1, y, x] = 0

    # 4. Breakwater (24..86, 60..62) & Striped Lighthouse Footing (20..26, 56..62): warm sandstone terrace!
    paint_plaza_inlay(m, 25, 60, 86, 62, paves, plazas, on_cls='f', seed=15)
    paint_plaza_inlay(m, 20, 56, 26, 62, pave3, warm_cream, on_cls='f', seed=16)

    # 5. Striped Awnings, Harbour Cargo, Salt Carts, Planters & Wrought-Iron Lanterns
    add_awnings(m, [
        (32, 24), (32, 28), (52, 22), (56, 27), (2, 43), (52, 20), (42, 32), (62, 32),
    ])
    lamp_pts = collect_lamp_positions(m)
    for nm, x, y in (
        ('cv_cart_salt', 12, 34), ('cv_cart_salt', 63, 34), ('cv_cart_salt', 26, 2), ('cv_cart_salt', 18, 2),
        ('hb_salt0', 6, 2), ('hb_salt2', 22, 1), ('hb_barrels', 4, 38), ('hb_crates4', 82, 38),
        ('pf_planter0', 41, 22), ('pf_planter1', 48, 22), ('pf_planter2', 39, 28), ('pf_planter3', 49, 28),
        ('pf_stonebench', 45, 61), ('pf_stonebench', 72, 61), ('hb_rope', 75, 61), ('hb_plank', 35, 61),
        ('fw_brazier', 26, 58), ('fw_brazier', 80, 58),
    ):
        on_c = 'S' if nm in ('hb_salt0', 'hb_salt2') or y <= 4 else 'fc'
        res = put_near_now(m, nm, x, y, on=on_c, r=2, prot=prot)
        if res and nm == 'fw_brazier':
            lamp_pts.append((res[0], res[1]))

    for lx, ly in ((42, 4), (47, 4), (42, 18), (47, 18), (37, 25), (51, 25), (18, 35), (55, 35),
                   (72, 35), (8, 46), (8, 54), (79, 46), (79, 53), (36, 61), (54, 61), (70, 61)):
        res = put_near_now(m, 'pf_lantern', lx, ly - 2, on='fc', r=1, prot=prot, allow_l2_overlap=False)
        if res:
            lamp_pts.append((res[0], res[1] + 1))

    # 6. Northern Salt Flats upgrade (x=0..37, y=0..5) — eliminate flat stark white strip!
    craft_salt_flats(m, seed=146, pink_keep=0.25, grey_salt=False, prot=prot)

    # 7. Harbour Basin & Open Sea: asymmetric buoys, submerged shoals, coastal rocks, lively glints!
    enrich_water_zone(m, water_cls='wW', seed=146, lotus=False, shoals=True, glints=True,
                      buoys=[('hb_buoy', 15, 44), ('hb_buoy2', 14, 54), ('hb_buoy', 32, 49),
                             ('hb_buoy2', 56, 48), ('hb_buoy', 68, 44), ('hb_buoy2', 73, 52),
                             ('hb_buoy', 19, 66), ('hb_buoy2', 43, 67), ('hb_buoy', 71, 65)],
                      rocks=[('cs_wrock0', 11, 64), ('cs_wrock1', 36, 68), ('cs_wrock2', 57, 68),
                             ('cs_wrock0', 81, 68), ('cs_wrock1', 53, 2), ('cs_wrock2', 74, 2)],
                      reeds_cls='', prot=prot, glint_density=0.22)
    # Asymmetric sunlit ocean & harbour-basin glint ribbons (y=38..71) — breaks water mirror naturally!
    rng_w = random.Random(14699)
    GL = [P1('hb_glint%d' % i) for i in range(4)]
    for y in range(38, m.H):
        for x in range(1, m.W - 1):
            if m.cls[y, x] in 'wW' and m.L[1, y, x] == 0 and m.L[2, y, x] == 0:
                bias = 0.42 if x < 44 else 0.10
                if rng_w.random() < bias:
                    m.L[2, y, x] = rng_w.choice(GL)

    # 8. Harbour Festoons, Lighthouse Beacon Halo & Maritime Light Shafts
    add_festoon_strings(m, [
        (42, 47, 3, 0), (42, 47, 14, 2), (35, 55, 24, 1), (10, 26, 33, 0), (58, 74, 33, 2),
        (32, 48, 60, 1), (56, 76, 60, 0),
    ], kind='lstring')
    add_warm_glows(m, lamp_pts + [
        (23, 48), (22, 49), (24, 49), (23, 58), (44, 26), (55, 21), (81, 49), (44, 34),
    ])
    add_light_shafts(m, [
        (44, 25), (21, 57), (52, 33), (82, 42), (5, 44), (62, 60), (44, 9),
    ])


def craft_147_oldtown(m):
    """147 Saltmere — Old Town (Pass 2 Polished): Pell Playhouse crimson theatrical red carpet down the Grand
    Stair, 5x5 golden sunburst medallion in Theatre Square, softened organic courtyard gardens with flower
    borders & blossom trees, varied historic Mask Row facades, clean promenade planters (ZERO wireframe nets!),
    organic harbor deep-water bays (ZERO wood shoal debris & 0 AT mismatches!), & eastern pocket terrace."""
    prot_exact, prot = build_prot_mask(m, 147)
    paves = [P1('lm_pave%d' % i) for i in range(4)]
    plazas = [P1('lm_plaza0'), P1('lm_plaza1'), P1('lm_pave1'), P1('lm_pave2')]
    warm_cream = [P1('lm_plaza0'), P1('lm_plaza1')]
    pave0 = P1('lm_pave0')
    pave3 = P1('lm_pave3')

    # 0. Pave raw 2x3 grass box wedged between buildings at (10..13, 9..13) into dressed stone alley + courtyard planter!
    for y in range(9, 14):
        for x in range(10, 14):
            if m.inb(x, y) and m.cls[y, x] == '.' and not m.cliff[y, x]:
                m.cls[y, x] = 'c'
                m.L[0, y, x] = paves[(x + y) % 4]
                if not m.taken[y, x]:
                    m.L[1, y, x] = 0
                    m.L[2, y, x] = 0
    put_near_now(m, 'pf_planter0', 11, 10, on='cf', r=1, prot=prot)

    # 0b. Replace floating 3-tile standalone decorative house (72..74, 30..35, 0 events!) with an anchored stone pocket terrace courtyard!
    ev_in_house = any(72 <= int(e['at'][0]) <= 74 and 30 <= int(e['at'][1]) <= 35 for e in (m.events or []) if e and e.get('at'))
    if not ev_in_house:
        prot_exact[30:38, 71:76] = False
        prot[30:38, 71:76] = False
        for y in range(30, 36):
            for x in range(72, 75):
                m.L[1, y, x] = 0
                m.L[2, y, x] = 0
                m.cls[y, x] = 'f'
                m.taken[y, x] = False
                if hasattr(m, 'bfoot'):
                    m.bfoot[y, x] = False
        paint_plaza_inlay(m, 71, 30, 75, 35, pave3, warm_cream, on_cls='fc', seed=1470)
        place_grove_now(m, 73, 32, CHERRY_CANOPY, count=1, radius=1.0, on='fc.', seed=1471, prot=prot_exact, undergrowth=False)
        for nm, gx, gy in (('pf_planter0', 71, 30), ('pf_planter2', 75, 30), ('pf_stonebench', 72, 34)):
            put_near_now(m, nm, gx, gy, on='fc', r=1, prot=prot_exact)

    # 1. Players' Causeway (40..45, 1..6) & Mask Row (y=15..17): organically weathered dressed stone
    paint_plaza_inlay(m, 40, 1, 45, 6, paves, plazas, on_cls='fc', seed=21)
    paint_plaza_inlay(m, 2, 15, 85, 17, paves, paves, on_cls='cf', seed=22)

    # Recessed Mask Row Historic Balcony/Garden Nooks (x=15..18 and x=64..67, y=8..14)
    lamp_pts = collect_lamp_positions(m)
    rw_w, rw_m, rw_e = P1('rw_rail_w'), P1('rw_rail_m'), P1('rw_rail_e')
    for cx in (16, 65):
        paint_plaza_inlay(m, cx - 2, 8, cx + 2, 14, pave3, warm_cream, on_cls='fc.', seed=cx + 147)
        for rx in range(cx - 2, cx + 3):
            if m.inb(rx, 7) and m.L[2, 7, rx] == 0:
                m.L[2, 7, rx] = rw_w if rx == cx - 2 else rw_e if rx == cx + 2 else rw_m
        place_grove_now(m, cx, 10, CHERRY_CANOPY, count=1, radius=1.2, on='.fc', seed=cx + 47, prot=prot, undergrowth=False)
        for nm, dx, dy in (('pf_planter0', -2, -1), ('pf_planter2', 2, -1), ('pf_planter0', -1, 3), ('pf_planter2', 1, 3), ('pf_stonebench', 0, 2)):
            put_near_now(m, nm, cx + dx, 10 + dy, on='fc.', r=1, prot=prot)
        res = put_near_now(m, 'pf_lantern', cx - 2, 11, on='fc.', r=1, prot=prot, allow_l2_overlap=False)
        if res:
            lamp_pts.append((res[0], res[1] + 1))

    # 2. Pell Playhouse Forecourt (18..35, 34..37) + Curtain Lane (y=36..37) + GRAND CRIMSON CARPET!
    paint_plaza_inlay(m, 18, 34, 35, 37, pave3, warm_cream, on_cls='fc', seed=23)
    paint_plaza_inlay(m, 2, 36, 85, 37, paves, paves, on_cls='cf', seed=24)
    paint_carpet_rect(m, 24, 34, 29, 37, on_cls='fc')
    paint_carpet_rect(m, 57, 36, 60, 37, on_cls='fc')

    # 3. Theatre Square (15..56, 41..50): Golden 5x5 Sunburst Medallion + Cream & Ashlar Promenade!
    paint_plaza_inlay(m, 15, 41, 56, 50, paves, plazas, on_cls='f', trim_tile=pave3, inset_border=True, seed=25)
    paint_carpet_rect(m, 25, 41, 28, 43, on_cls='fc')
    placed_sun = False
    for sx, sy in ((32, 43), (28, 43), (34, 43), (24, 43)):
        if paint_sunburst_medallion(m, sx, sy, on_cls='fc'):
            placed_sun = True
            break
    if not placed_sun:
        paint_plaza_inlay(m, 27, 43, 35, 47, pave3, warm_cream, on_cls='fc', seed=26)

    # 4. Seafront Promenade (y=57..59): weathered cream & ashlar seawall walk
    paint_plaza_inlay(m, 1, 57, 86, 59, paves, plazas, on_cls='f', seed=27)
    for x in range(2, 86):
        if m.cls[59, x] == 'f' and not m.cliff[59, x] and vnoise(x, 59, 1473, 4.2) > 0.46:
            m.L[0, 59, x] = paves[(x * 5 + 2) % 4]

    # 5. Soften ALL Old Town Garden Courts (x0-7 y20-24, x12-17 y21-26, x36..86 y20-26, x20..36 y51-56)!
    # Layer organic weathered limestone garden paths (`S_floorpatch`) + dappled turf + flower/azalea borders!
    m.grass_var = True
    m.grass_variation(dark=0.46, worn=True)
    garden_stone = np.zeros((m.H, m.W), dtype=bool)
    for gcx, gcy, grx, gry in ((4, 22, 2.5, 2.0), (15, 23, 2.2, 2.0), (40, 23, 2.8, 2.0),
                               (57, 23, 3.6, 2.2), (79, 23, 4.2, 2.2), (28, 53, 4.2, 1.8)):
        for y in range(max(2, int(gcy - gry - 1)), min(m.H - 2, int(gcy + gry + 2))):
            for x in range(max(1, int(gcx - grx - 1)), min(m.W - 1, int(gcx + grx + 2))):
                if m.cls[y, x] == '.' and not m.cliff[y, x]:
                    if ((x - gcx) / grx) ** 2 + ((y - gcy) / gry) ** 2 + 0.35 * (vnoise(x, y, 1478, 2.6) - 0.5) <= 0.72:
                        garden_stone[y, x] = True
    paint_floorpatch(m, garden_stone, prefix='S_floorpatch', on_cls='.', prot_exact=prot_exact, smooth=1)

    rng_g = random.Random(14747)
    FL_147 = K.DECOR_SH['flowers']
    garden_cells = (m.cls == '.') & ~m.cliff
    # Rim flower & shrub borders hugging every courtyard garden edge so zero hard bare-lawn rectangles remain!
    for y in range(2, m.H - 2):
        for x in range(1, m.W - 1):
            if not garden_cells[y, x] or m.taken[y, x] or prot[y, x]:
                continue
            near_pave = any(m.cls[y + dy, x + dx] in 'cfB' or m.cliff[y + dy, x + dx]
                            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if m.inb(x + dx, y + dy))
            if near_pave:
                rv = rng_g.random()
                if rv < 0.24 and m.L[1, y, x] == 0 and m.L[2, y, x] == 0:
                    put_stamp_now(m, rng_g.choice(('nt_azalea0', 'nt_azalea1', 'nt_azalea2', 'nt_shrub0')), x, y, on='.', prot=prot)
                elif rv < 0.75 and m.L[1, y, x] == 0:
                    m.L[1, y, x] = ROSE_TILE if rng_g.random() < 0.55 else rng_g.choice([FL_147[2], FL_147[3], FL_147[6], FL_147[0]])
            elif m.L[1, y, x] == 0 and rng_g.random() < 0.32:
                m.L[1, y, x] = rng_g.choice([FL_147[2], FL_147[3], ROSE_TILE, FL_147[6]])
    # Lush blossom & garden shade clusters + charming courtyard benches/planters inside terraced gardens
    for gcx, gcy in ((4, 22), (15, 23), (40, 23), (57, 23), (78, 23), (28, 53)):
        place_grove_now(m, gcx, gcy, CHERRY_CANOPY if gcx in (4, 40, 78) else COAST_CANOPY, count=2, radius=2.2, on='.', seed=gcx + gcy, prot=prot, undergrowth=True)
        put_near_now(m, 'pf_planter0' if (gcx % 2 == 0) else 'pf_planter2', gcx - 1, gcy + 1, on='.cf', r=2, prot=prot)
        put_near_now(m, 'pf_stonebench', gcx + 1, gcy + 1, on='.cf', r=2, prot=prot)

    # 6. Theatre Awnings (shopfronts only), Statues, Planters, Theatrical Banners & Clean Promenade Props (ZERO wireframe pf_p_net!)
    add_awnings(m, [
        (36, 35), (62, 35), (20, 33), (31, 33), (78, 56),
    ])
    for nm, x, y in (
        ('mn_statue', 22, 34), ('mn_statue', 31, 34), ('mn_statue', 23, 41), ('mn_statue', 30, 41),
        ('pf_planter0', 20, 35), ('pf_planter2', 33, 35), ('pf_planter1', 55, 35), ('pf_planter3', 61, 35),
        ('pf_planter0', 16, 42), ('pf_planter2', 40, 42), ('pf_planter1', 20, 49), ('pf_planter3', 39, 49),
        ('pf_planter0', 38, 16), ('pf_planter1', 47, 16), ('pf_planter2', 12, 58), ('pf_planter3', 50, 58),
        ('pf_stonebench', 26, 44), ('pf_stonebench', 37, 45), ('pf_stonebench', 20, 58), ('pf_stonebench', 48, 58),
        ('fw_brazier', 23, 36), ('fw_brazier', 30, 36),
        # Theatrical banners along Mask Row & Playhouse Forecourt
        ('lm_banner', 13, 14), ('lm_banner_w', 20, 14), ('lm_banner', 62, 14), ('lm_banner_w', 69, 14),
        ('lm_banner', 19, 34), ('lm_banner_w', 35, 34),
        # Dockside barrels, crates, planters, tubs, ropes & anchor along Seafront Quay (replaced floating wireframe pf_p_net!)
        ('hb_barrels', 9, 58), ('hb_crates4', 14, 58), ('pf_planter0', 26, 57), ('hb_tubs', 34, 57),
        ('hb_rope', 42, 59), ('hb_barrels', 53, 58), ('pf_planter2', 61, 57), ('hb_fish', 66, 58),
        ('hb_crates4', 72, 58), ('hb_rope', 82, 59), ('pf_anchor', 59, 56), ('hb_boxes', 4, 58),
    ):
        res = put_near_now(m, nm, x, y, on='fc', r=2, prot=prot)
        if res and nm == 'fw_brazier':
            lamp_pts.append((res[0], res[1]))

    # Mooring bollards along seafront quay lip (y=60, clear of boat steps 56..58!)
    for bx in (5, 11, 22, 37, 45, 52, 62, 71, 83):
        if m.inb(bx, 60) and not prot[60, bx] and m.L[2, 60, bx] == 0:
            m.L[2, 60, bx] = P1('hb_bollard%d' % (bx % 2))

    for lx, ly in ((24, 35), (29, 35), (21, 44), (39, 44), (31, 48), (48, 45), (41, 12), (45, 12),
                   (18, 17), (64, 17), (24, 59), (40, 59), (60, 59), (74, 59), (73, 33)):
        res = put_near_now(m, 'pf_lantern', lx, ly - 2, on='fc', r=1, prot=prot, allow_l2_overlap=False)
        if res:
            lamp_pts.append((res[0], res[1] + 1))

    # 7. Theatrical Blossom Groves & Rose Petal Drifts across Gardens, Theatre Square & Seafront
    add_petals_and_flowers(m, [
        (27, 36, 7.0, 2.2, 0.28, 'petal'),
        (32, 45, 14.0, 4.5, 0.16, 'petal'),
        (42, 16, 10.0, 2.0, 0.12, 'petal'),
        (36, 58, 22.0, 1.8, 0.10, 'petal'),
        (5, 22, 4.5, 3.0, 0.48, 'rose'),
        (15, 23, 4.0, 3.0, 0.48, 'petal'),
        (40, 23, 4.5, 3.0, 0.48, 'rose'),
        (57, 23, 5.5, 3.0, 0.45, 'petal'),
        (78, 23, 6.5, 3.0, 0.45, 'rose'),
        (28, 53, 8.0, 2.8, 0.45, 'rose'),
    ], seed=147)

    # Keep courtyard red carpet (25..28, 41..43) spotless (zero stray petals/artifacts on L1/L2, clean crimson center/border!)
    paint_carpet_rect(m, 25, 41, 28, 43, on_cls='fc')
    for cy_c in range(42, 44):
        for cx_c in range(25, 29):
            m.L[1, cy_c, cx_c] = 0
            m.L[2, cy_c, cx_c] = 0

    # 8. Smooth Southern Harbor Deep-Water Bays + Mixed Shoal-Stone Reefs, Buoys, Kelp & Glints (ZERO cs_shoal wood squares!)
    oc_lo = RC.vauto('rejuvenation', 'Ocean', 0)
    dp_lo = RC.vauto('rejuvenation', 'Sea deep', 0)
    for x in range(m.W):
        deep_y = int(round(66.8 + 1.8 * math.sin(x / 10.5) + 0.9 * math.cos(x / 6.0)))
        deep_y = max(65, min(70, deep_y))
        for y in range(62, m.H):
            if m.cls[y, x] in 'wW':
                if y >= deep_y:
                    m.cls[y, x] = 'W'
                    m.L[0, y, x] = dp_lo
                    if dp_lo <= int(m.L[1, y, x]) < dp_lo + 48:
                        m.L[1, y, x] = 0
                else:
                    m.cls[y, x] = 'w'
                    m.L[0, y, x] = oc_lo
                    if dp_lo <= int(m.L[1, y, x]) < dp_lo + 48:
                        m.L[1, y, x] = 0

    enrich_water_zone(m, water_cls='wW', seed=147, lotus=False, shoals=False, glints=True,
                      buoys=[('hb_buoy', 17, 65), ('hb_buoy2', 38, 64), ('hb_buoy', 56, 65), ('hb_buoy2', 69, 66),
                             ('hb_buoy2', 24, 3), ('hb_buoy', 58, 3)],
                      rocks=[('cs_wrock0', 7, 68), ('cs_wrockb0', 9, 69), ('cs_wrock1', 28, 67), ('cs_wrock2', 30, 68),
                             ('cs_wrockb1', 32, 67), ('cs_wrock0', 48, 68), ('cs_wrockb0', 50, 69),
                             ('cs_wrock1', 79, 68), ('cs_wrock2', 82, 67), ('cs_wrockb1', 84, 69),
                             ('cs_wrock0', 11, 2), ('cs_wrockb0', 77, 2), ('cs_wrock1', 79, 3), ('cs_wrock2', 81, 2)],
                      reeds_cls='', prot=prot, glint_density=0.18)
    # Natural kelp rings around reef clusters ONLY (NO cs_shoal0/cs_shoal1 detached wood squares!)
    rng_w = random.Random(14799)
    GL = [P1('hb_glint%d' % i) for i in range(4)]
    KELP = [P1('cs_kelp0'), P1('cs_kelp1')]
    for rx, ry in ((6, 67), (29, 67), (49, 68), (81, 68), (79, 2), (10, 3)):
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                X, Y = rx + dx, ry + dy
                if m.inb(X, Y) and m.cls[Y, X] in 'wW' and m.L[1, Y, X] == 0 and m.L[2, Y, X] == 0:
                    if abs(dx) + abs(dy) in (1, 2) and rng_w.random() < 0.35:
                        m.L[2, Y, X] = rng_w.choice(KELP)
    for y in list(range(0, 7)) + list(range(61, m.H)):
        for x in range(1, m.W - 1):
            if m.cls[y, x] in 'wW' and m.L[1, y, x] == 0 and m.L[2, y, x] == 0:
                bias = 0.34 if x > 44 else 0.12
                if rng_w.random() < bias:
                    m.L[2, y, x] = rng_w.choice(GL)

    # 9. Festival Pennant Garlands & Theatrical Warm Glows (clear of red carpet y=42 & ZERO outdoor cv_shaft smears!)
    add_festoon_strings(m, [
        (20, 34, 35, 0), (19, 24, 42, 2), (29, 36, 42, 0), (22, 40, 47, 1), (40, 45, 3, 0),
        (54, 65, 36, 1), (10, 24, 58, 2), (48, 64, 58, 0), (8, 26, 16, 1), (56, 76, 16, 0),
    ], kind='garl')
    add_warm_glows(m, lamp_pts)

    # 10. Upgrade ALL flat-sub0 Cobbles & Flags to crisp static Gen 5 city pavers + single-layer Sea deep/Ocean NB2AUTO (0 mismatches!)
    upgrade_saltmere_paving_w12(m, seed=147)
    fix_vauto_l0_w12(m.L, 'rejuvenation', 'Sea deep')
    fix_vauto_l0_w12(m.L, 'rejuvenation', 'Ocean')


def craft_522_glassed_orchard(m, r):
    """522 The Glassed Orchard: Wave 11 Kristiline winter-crystal mastercraft!
      - Seamless snow-edged Cerulean & Periwinkle glacial turf (`CERULEAN_3X3`, `PERI_3X3`)
      - Dense overlapping Kristiline frosted teal pines & silver spruces packing the forest border
      - Crystal spire/blade mineral accents, Still Mirror Pond frost detail, `KF_LANTERN` posts
      - Lush living Sheridan wildflower/rose contrast pocket west of Bleed Veil (x<=4, y>=31)
      - 100% D1 Chime Rows (19,33 / 4,16 / 23,16 / 35,25 / 38,1..4) & Glass Foal parity!"""
    extra_rects = [
        (35, 0, 41, 5),     # Sealed D1 NE Alcove + Glass hedge (38, 1..4)
        (0, 30, 5, 39),     # Living SW meadow pocket + Bleed Veil (x=4)
        (27, 1, 34, 10),    # Pruett Farmhouse (kf_aframe) + doorstep
        (17, 28, 21, 34),   # South stone stair + Chime post (19, 33)
        (32, 13, 36, 18),   # Upper homestead stair
    ]
    extra_pts = [
        (4, 16), (23, 16), (35, 25), (19, 33),
        (8, 34), (18, 20), (30, 12), (34, 10),
        (27, 13), (38, 24), (24, 18), (38, 6), (11, 13),
    ]
    prot_exact, prot = build_prot_mask(m, 522, extra_rects=extra_rects, extra_pts=extra_pts)
    H, W = m.H, m.W
    rng = random.Random(52299)

    def in_living(x, y):
        return (x <= 7 and y >= 28)

    # 1. Native seamless frosted snow variation (preserves organic patchy snow-transition across x=0..7, y=28..39!)
    base_ok = np.isin(m.cls, ['.', 't', 'T']) & ~m.cliff & ~r.road_mask
    for y in range(H):
        for x in range(W):
            if in_living(x, y) or (27 <= x <= 34 and y <= 10) or (35 <= x <= 41 and y <= 5):
                base_ok[y, x] = False

    sn_g = [K.P1('sn_g%d' % i) for i in range(4)]
    for y in range(H):
        for x in range(W):
            if base_ok[y, x] and vnoise(x, y, 52211, 5.0) > 0.44:
                m.L[0, y, x] = sn_g[int(vnoise(x, y, 52219, 2.8) * 3.999)]

    # 1b. Wipe any purple-tree stubs (6998..7130) & half-off-frame orphan tree slivers from rkit border fill!
    PURP_TILES = {6998, 6999, 7006, 7007, 7014, 7015, 7105, 7112, 7113, 7114, 7120, 7121, 7122, 7128, 7129, 7130}
    BLUE_TREE_TILES = {6992, 6993, 7000, 7001, 7008, 7009, 7073, 7080, 7081, 7082, 7088, 7089, 7090, 7096, 7097, 7098}
    for y in range(H):
        for x in range(W):
            for z in (1, 2):
                if int(m.L[z, y, x]) in PURP_TILES:
                    m.L[z, y, x] = 0
                    if z == 1:
                        m.taken[y, x] = False
    # Clear orphaned single-column/single-row half-off-edge blue tree slivers on x=0, x=W-1, y=H-1
    for y in range(0, 28):
        if (int(m.L[1, y, 0]) in BLUE_TREE_TILES or int(m.L[2, y, 0]) in BLUE_TREE_TILES) and (
                int(m.L[1, y, 1]) not in BLUE_TREE_TILES and int(m.L[2, y, 1]) not in BLUE_TREE_TILES):
            m.L[1, y, 0] = 0; m.L[2, y, 0] = 0; m.taken[y, 0] = False
    for y in range(H):
        if (int(m.L[1, y, W - 1]) in BLUE_TREE_TILES or int(m.L[2, y, W - 1]) in BLUE_TREE_TILES) and (
                int(m.L[1, y, W - 2]) not in BLUE_TREE_TILES and int(m.L[2, y, W - 2]) not in BLUE_TREE_TILES):
            m.L[1, y, W - 1] = 0; m.L[2, y, W - 1] = 0; m.taken[y, W - 1] = False
    for x in range(6, W):
        if int(m.L[1, H - 1, x]) in BLUE_TREE_TILES and int(m.L[1, H - 2, x]) not in BLUE_TREE_TILES and int(m.L[2, H - 2, x]) not in BLUE_TREE_TILES:
            m.L[1, H - 1, x] = 0; m.taken[H - 1, x] = False

    # 2. Strict ZERO-OVERLAP Kristiline Winter Spruce/Pine infill ONLY in completely empty L1+L2 border pockets!
    kf_kinds = [KF_TEAL_PINE_A, KF_TEAL_PINE_B, KF_SPRUCE_A, KF_SPRUCE_B]
    def try_put_clean_sprite(tx, ty, top_r, bot_r, on='T'):
        ht, hb = len(top_r), len(bot_r)
        w = len(bot_r[0]) if hb else len(top_r[0])
        h = ht + hb
        if tx < 0 or ty < 0 or tx + w > W or ty + h > H:
            return False
        if tx < 5 and ty + h > 29:
            return False
        # Never touch any existing L1/L2 tile, cliff, taken cell, or protected anchor across FULL box!
        if (m.L[1, ty:ty + h, tx:tx + w] != 0).any() or (m.L[2, ty:ty + h, tx:tx + w] != 0).any():
            return False
        if m.cliff[ty:ty + h, tx:tx + w].any() or m.taken[ty:ty + h, tx:tx + w].any() or prot[ty:ty + h, tx:tx + w].any():
            return False
        for dy in range(ht, h):
            for dx in range(w):
                if m.cls[ty + dy, tx + dx] not in on:
                    return False
        for dy, row in enumerate(top_r):
            for dx, tid in enumerate(row):
                if tid:
                    m.L[2, ty + dy, tx + dx] = tid
        for dy, row in enumerate(bot_r):
            for dx, tid in enumerate(row):
                if tid:
                    m.L[1, ty + ht + dy, tx + dx] = tid
                    m.taken[ty + ht + dy, tx + dx] = True
        return True

    for ty in range(0, H - 3):
        for tx in range(0, W - 2):
            if m.cls[ty + 2, tx] != 'T':
                continue
            top_r, bot_r = kf_kinds[(tx * 5 + ty * 7) % len(kf_kinds)]
            try_put_clean_sprite(tx, ty, top_r, bot_r, on='T')

    # 3. Companion Kristiline frosted spruces & shrubs enriching open frosted orchard pockets (zero-overlap!)
    for cx, cy in ((7, 4), (16, 4), (24, 4), (26, 28), (37, 17), (15, 22), (8, 30)):
        if prot[cy, cx]:
            continue
        top_r, bot_r = rng.choice(kf_kinds)
        try_put_clean_sprite(cx, cy, top_r, bot_r, on='.T')

    # 4. Luminous Glass Cloches (`KF_CRYS_*`), Frosted Shrubs & Boulders framing structured orchard rows!
    for sx, sy, sp in (
        (6, 20, KF_CRYS_STAR), (13, 24, KF_CRYS_BLADES), (16, 26, KF_CRYS_MONO),
        (25, 19, KF_CRYS_STAR), (32, 22, KF_CRYS_BLADES), (27, 10, KF_SHRUB_A),
        (36, 11, KF_CRYS_MONO), (12, 15, KF_SHRUB_B), (7, 13, KF_BOULDER),
        (22, 29, KF_CRYS_STAR), (39, 21, KF_CRYS_BLADES), (16, 12, KF_SHRUB_A),
        (8, 8, KF_CRYS_MONO), (19, 8, KF_CRYS_STAR), (29, 24, KF_CRYS_MONO), (35, 22, KF_CRYS_STAR),
    ):
        try_put_clean_sprite(sx, sy, sp[0], sp[1], on='.t')

    # 5. Kristiline Frosted Lantern Posts (`KF_LANTERN`) along path junctions & Pruett Terrace
    lamp_pts = []
    for lx, ly in ((7, 34), (16, 33), (22, 28), (29, 17), (32, 12), (28, 10), (36, 8)):
        if put_sprite_now(m, lx, ly - 1, KF_LANTERN[0], KF_LANTERN[1], on='.d', prot=prot, check_level=True):
            lamp_pts.append((lx, ly - 1))

    # 6. Lush Living SW Meadow Flowers & Petals tapering naturally through the patchy snow-transition border (x=1..4)!
    for y in range(30, H - 1):
        for x in range(1, 5):
            if m.cls[y, x] == '.' and not m.taken[y, x] and not r.road_mask[y, x]:
                if m.L[1, y, x] == 0 and (x <= 3 or (x + y) % 3 == 0):
                    m.L[1, y, x] = ROSE_TILE if (x + y) % 2 == 0 else K.DECOR_SH['flowers'][(x * 3 + y) % 4]
                if m.L[2, y, x] == 0 and (x + y) % 3 == 0:
                    m.L[2, y, x] = PETAL_TILE

    # 6b. Subtle frost-flower & snow-drift ground accents across open frosted clearings (keeps rubric layer2 >= 58%!)
    for y in range(2, H - 1):
        for x in range(1, W - 1):
            if in_living(x, y) or m.cliff[y, x] or m.taken[y, x] or r.road_mask[y, x] or prot[y, x]:
                continue
            if m.cls[y, x] == '.' and m.L[1, y, x] == 0 and m.L[2, y, x] == 0:
                if (x * 7 + y * 13) % 7 == 0:
                    m.L[1, y, x] = K.P1('fw_drift%d' % ((x + y) % 3))
                elif (x * 5 + y * 11) % 9 == 0:
                    m.L[1, y, x] = 9725 if (x + y) % 2 == 0 else 10620

    # 7. Still Mirror Pond crystalline shimmer & shoals
    enrich_water_zone(m, water_cls='w', seed=522, lotus=False, shoals=True, glints=True,
                      reeds_cls='', prot=prot, glint_density=0.14)

    # 8. Ethereal Glow Halos & Slanted Crystal Sunbeams (`cv_shaft`)
    add_warm_glows(m, lamp_pts + [(4, 36), (19, 31), (30, 8), (34, 15)])
    add_light_shafts(m, [
        (9, 21), (19, 25), (29, 7), (36, 22), (10, 10), (22, 14),
    ])

    # 9. Re-verify sacred Pruett frost base + Bleed Veil (y=35..37 between gateposts) + D1 NE alcove clarity!
    m.L[1, 8, 28] = 9232
    for yy in range(1, 4):
        m.L[1, yy, 38] = 0
        m.L[2, yy, 38] = 0
    veil_tiles = [26048, 26049, 26050]
    for y in (35, 36, 37):
        m.L[2, y, 4] = veil_tiles[y % 3]


def organic_orchard_rows(r, x0, y0, x1, y1, kind, gap=5, name=None, sign_at=None, skip_row=None):
    """Replacement for routes_early.orchard_rows on 521 Windfall Row!
    Replaces rigid mechanical 3x3 military tree grids with lush, staggered, multi-species
    blooming Hale orchard groves while keeping every orchard sign & event 100% intact."""
    m = r.m
    m.rect(x0, y0, x1 - x0 + 1, y1 - y0 + 1, '.', only='T.t')
    rng = random.Random(52100 + x0 * 31 + y0 * 17)

    # Species-authentic palette per orchard block
    if kind == 'tr_pink':
        pool = ['tr_pink', 'nt_blossom', 'tr_pink', 'tr_oak2']
    elif name and 'PLUM' in name:
        pool = ['nt_dark_sh', 'tr_oak2', 'nt_blossom', 'tr_oak']
    elif name and 'PEAR' in name:
        pool = ['tr_oak2', 'nt_round_sh', 'nt_teal_a', 'tr_oak']
    elif name and 'QUINCE' in name:
        pool = ['nt_olive', 'tr_oak', 'tr_oak2', 'nt_round_sh']
    elif name and 'MEDLAR' in name:
        pool = ['tr_oak2', 'tr_pink', 'nt_olive', 'tr_oak']
    else:
        pool = ['tr_oak', 'tr_oak2', 'nt_olive', 'tr_pink']

    # Plant organic wind-staggered orchard rows (wavy y-offset + irregular spacing + cozy glade gaps)
    rows = 0
    y = y0
    while y + 4 <= y1:
        rows += 1
        if skip_row != rows:
            x = x0 + rng.randint(0, 2)
            while x + 3 <= x1:
                # Leave occasional sunlit windfall glades so the orchard breathes organically!
                if rng.random() < 0.78:
                    k = rng.choice(pool)
                    st = STAMPS[k]
                    jx = rng.randint(-1, 1)
                    jy = rng.randint(-1, 1)
                    tx = max(x0, min(x1 - st['w'] + 1, x + jx))
                    ty = max(y0, min(y1 - st['h'] + 1, y + jy))
                    if m.can_tree(k, tx, ty, on='.t'):
                        m.stamp(k, tx, ty, mark='B')
                        # Tuck a flowering shrub or basket beside occasional orchard trees
                        if rng.random() < 0.25:
                            sh = rng.choice(['nt_azalea0', 'nt_azalea1', 'nt_shrub0', 'nt_fern0'])
                            sx_, sy_ = tx + st['w'], ty + st['h'] - 1
                            if m.free(sx_, sy_, 1, 1, on='.t') and not m.cliff[sy_, sx_]:
                                m.stamp(sh, sx_, sy_, mark='B')
                x += rng.randint(4, 6)
        y += max(4, gap + rng.randint(-1, 1))

    if sign_at:
        r.add(RK.sign(sign_at, name + ' sign', name))
    return rows


def craft_521_windfall_row(m, r):
    """521 Windfall Row: lush Rejuvenation V14 meadow/orchard elevation!
      - Kills flat neon-green lawn with shaded grass variation + packed-earth farmyards (`E_floorpatch`)
      - Overhauls the bare SE Mill Rise (92..110, 34..48) into a scenic cobblestone hilltop courtyard (`S_floorpatch`)
      - Turns Duck Pond (30, 50) into a lush lotus-and-reed oasis
      - Packs dense woodland borders + subtle frosted trees right beside the Glassed Orchard gate (61, 22..23)
      - Abundant blossom petal drifts, wildflowers, farm lanterns, warm glows & afternoon sunbeams!"""
    extra_rects = [
        (0, 8, 7, 13),       # Forest-road cordon + Gossamer Wood warps
        (59, 20, 63, 25),    # Glassed Orchard gate warps
        (56, 65, 63, 69),    # South exit to 520
        (96, 39, 105, 51),   # Mill Rise stairs + wide-open courtyard around Mill Tower & Mae!
        (48, 43, 53, 47),    # Hale Farmhouse doorway
    ]
    prot_exact, prot = build_prot_mask(m, 521, extra_rects=extra_rects)
    H, W = m.H, m.W

    # 1. Lush shaded grass depth (breaks up flat neon-green meadow!)
    m.grass_var = True
    m.grass_variation(dark=0.47, worn=True)

    # 2. Organic Packed-Earth Farmyards (`E_floorpatch`) around Farmhouse, Cider Press & Farm Stand!
    earth_mask = np.zeros((H, W), dtype=bool)
    for cx, cy, rx, ry in (
        (50, 46, 6.5, 4.2),   # Hale Farmhouse yard (Coll & Parsnip!)
        (100, 55, 7.5, 4.2),  # Cider Press yard
        (66, 48, 4.2, 2.5),   # Farm stand clearing
        (10, 11, 5.0, 2.8),   # Forest-road cordon checkpoint
        (58, 23, 3.8, 2.8),   # Glassed Orchard gate apron
    ):
        for y in range(max(2, int(cy - ry - 1)), min(H - 2, int(cy + ry + 2))):
            for x in range(max(2, int(cx - rx - 1)), min(W - 2, int(cx + rx + 2))):
                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 + 0.25 * (vnoise(x, y, 5211, 3.0) - 0.5) <= 1.0:
                    earth_mask[y, x] = True
    paint_floorpatch(m, earth_mask, prefix='E_floorpatch', on_cls='.d', prot_exact=prot_exact, smooth=2)

    # 3. Scenic Old Mill Rise Courtyard (`S_floorpatch` weathered stone terrace on 92..110, 34..48!)
    mill_mask = np.zeros((H, W), dtype=bool)
    for y in range(36, 46):
        for x in range(94, 108):
            if m.ht[y, x] == 1 and not m.cliff[y, x]:
                d2 = ((x - 101) / 6.8) ** 2 + ((y - 41) / 4.4) ** 2
                if d2 + 0.22 * (vnoise(x, y, 5212, 3.0) - 0.5) <= 1.0:
                    mill_mask[y, x] = True
    paint_floorpatch(m, mill_mask, prefix='S_floorpatch', on_cls='.d', prot_exact=prot_exact, smooth=2)

    # Guarantee Mill Rise stairhead -> Mill Tower & Mae walkway has zero random r.dress() trees/bushes!
    for yy in range(40, 47):
        for xx in range(98, 104):
            if m.ht[yy, xx] == 1 and not m.cliff[yy, xx] and not (xx == 104 and yy == 40):
                cur1 = int(m.L[1, yy, xx])
                if cur1 != 0 and cur1 < RC.VBASE:
                    m.L[1, yy, xx] = 0
                    m.taken[yy, xx] = False
                    if yy > 0 and m.L[2, yy - 1, xx] != 0:
                        m.L[2, yy - 1, xx] = 0

    # Dress Mill Rise rim + Farmhouse + Cider Yard with curated storybook props
    lamp_pts = collect_lamp_positions(m)
    for nm, x, y in (
        ('pf_stonebench', 94, 42), ('pf_hayrick', 94, 37), ('hb_barrels', 106, 37), ('hb_crates4', 94, 39),
        ('nt_azalea0', 93, 44), ('nt_azalea1', 107, 44), ('nt_azalea2', 107, 36), ('pf_well', 44, 42),
        ('pf_planter0', 48, 45), ('pf_planter1', 53, 45), ('pf_hayrick', 91, 52), ('pf_hayrick', 109, 53),
        ('hb_tables', 68, 47), ('pf_logbench', 27, 48), ('pf_logbench', 33, 53),
        ('pf_planter2', 56, 21), ('pf_planter3', 56, 25),
    ):
        put_near_now(m, nm, x, y, on='.d', r=1, prot=prot)

    # 4. Dense Forest Border Packing + Overlapping Canopy Groves + Frosted Bleed Foreshadowing!
    infill_forest_now(m, seed=521, prot=prot, snow=False)
    for idx, (cx, cy, pal, cnt, rad, hero) in enumerate([
        (16, 52, SPRING_CANOPY, 5, 3.0, 'pf_g_tree2'),
        (38, 63, SPRING_CANOPY, 5, 3.0, 'pf_g_tree2'),
        (24, 54, CHERRY_CANOPY, 4, 2.6, None),
        (42, 13, CHERRY_CANOPY, 5, 3.2, None),
        (108, 12, ORCHARD_CANOPY, 5, 3.0, 'pf_g_tree2'),
        (109, 41, ORCHARD_CANOPY, 4, 2.6, None),
        (12, 26, SPRING_CANOPY, 4, 2.8, None),
        (80, 38, ORCHARD_CANOPY, 4, 2.6, None),
        (114, 32, SPRING_CANOPY, 4, 2.6, None),
    ]):
        place_grove_now(m, cx, cy, pal, count=cnt, radius=rad, on='.t', seed=idx + 10, hero=hero, prot=prot)

    # Subtle frosted crystal trees RIGHT inside the Glassed Orchard hedge (x=63..68, y=16..27) foreshadowing 522!
    for fx, fy in ((64, 18), (66, 21), (64, 25), (67, 16)):
        put_sprite_now(m, fx, fy, KF_TEAL_PINE_A[0], KF_TEAL_PINE_A[1], on='T.', prot=prot, check_level=False)

    # 5. Duck Pond Oasis (30, 50): floating lotus pads, tall reeds, shoals & water glints!
    enrich_water_zone(m, water_cls='wp', seed=521, lotus=True, shoals=True, glints=True,
                      reeds_cls='.d', prot=prot)

    # 6. Warm Road Lanterns (`pf_lantern`) along Windfall Row lanes, Farmhouse, Cider Yard & Mill Rise rim!
    for lx, ly in ((57, 62), (55, 50), (54, 42), (47, 45), (55, 31), (59, 24), (44, 34),
                   (24, 22), (10, 12), (72, 46), (88, 49), (95, 45), (106, 42), (99, 54)):
        res = put_near_now(m, 'pf_lantern', lx, ly - 2, on='.d', r=1, prot=prot)
        if res:
            lamp_pts.append((res[0], res[1] + 1))

    # 7. Abundant Cherry Blossom Petals, Orchard Roses & Meadow Wildflowers!
    add_petals_and_flowers(m, [
        (44, 13, 10.0, 8.0, 0.38, 'petal'),    # Cherry Orchard pink petal carpet!
        (81, 17, 10.0, 8.0, 0.16, 'petal'),    # Apple Orchard windfall blossoms
        (104, 24, 11.0, 6.0, 0.14, 'petal'),   # Pear Orchard blossoms
        (26, 36, 8.0, 6.0, 0.22, 'petal'),     # Medlar Orchard blossoms
        (75, 59, 10.0, 6.0, 0.18, 'rose'),     # Plum Rows & Thirteenth Row garden!
        (101, 41, 7.0, 5.0, 0.28, 'wild'),     # Old Mill Rise hilltop blooms
        (30, 50, 9.0, 6.0, 0.30, 'wild'),      # Duck Pond meadow
        (50, 45, 7.0, 4.0, 0.22, 'rose'),      # Hale Farmhouse cottage garden
        (46, 58, 9.0, 5.0, 0.35, 'wild'),      # Southern meadow
    ], seed=521)

    # 8. Warm Golden Lantern Glows & Sunlit Afternoon Orchard Sunbeams!
    add_warm_glows(m, lamp_pts + [(50, 44), (100, 39), (60, 22), (100, 54)])
    add_light_shafts(m, [
        (45, 14), (50, 43), (30, 49), (101, 38), (78, 18), (75, 58), (58, 56), (22, 26),
    ])


def craft_520_ferrymens_mile(m, r):
    """520 The Ferrymen's Mile: scenic cliff-top lane from Ferrow's Landing to Windfall Row!
      - 100% preserves Hale Bell quarantine roadblock gate (x<=5, 64..80) + S->100, N->521, W->527 seams!
      - Rich shaded meadow turf, chalk flagstones (`S_floorpatch`) at Hale Bell & cliff lookouts,
        packed earth (`E_floorpatch`) around toll booth, picking shed & stile
      - Lotus & reed Duck Pond (48, 72), lush coastal/bramble groves, sea-pinks, lanterns & sea-mist beams!"""
    extra_rects = [
        (0, 63, 7, 81),      # CRITICAL: Hale Bell quarantine roadblock & sealed W woods flank!
        (13, 105, 20, 109),  # S->100 Ferrow's Landing seam
        (28, 0, 35, 4),      # N->521 Windfall Row seam
        (11, 88, 15, 95),    # Smuggler's Stair & CutTree
    ]
    prot_exact, prot = build_prot_mask(m, 520, extra_rects=extra_rects)
    H, W = m.H, m.W

    # 1. Enriched shaded turf depth
    m.grass_var = True
    m.grass_variation(dark=0.47, worn=True)

    # 2. Weathered chalk aprons (`S_floorpatch`) at Hale Bell lookout & Ferryman's Rest cliff top
    chalk_mask = np.zeros((H, W), dtype=bool)
    for cx, cy, rx, ry in ((16, 70, 4.5, 3.5), (14, 86, 4.0, 2.8), (18, 105, 4.2, 2.8)):
        for y in range(max(2, int(cy - ry - 1)), min(H - 2, int(cy + ry + 2))):
            for x in range(max(7, int(cx - rx - 1)), min(W - 2, int(cx + rx + 2))):
                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 + 0.25 * (vnoise(x, y, 5201, 3.0) - 0.5) <= 1.0:
                    chalk_mask[y, x] = True
    paint_floorpatch(m, chalk_mask, prefix='S_floorpatch', on_cls='.du', prot_exact=prot_exact, smooth=2)

    # Packed-earth picking yards (`E_floorpatch`) on Hale's Bramble & Sheepfold gate
    earth_mask = np.zeros((H, W), dtype=bool)
    for cx, cy, rx, ry in ((52, 37, 5.5, 3.2), (46, 20, 5.5, 3.5), (29, 85, 4.5, 3.0)):
        for y in range(max(2, int(cy - ry - 1)), min(H - 2, int(cy + ry + 2))):
            for x in range(max(7, int(cx - rx - 1)), min(W - 2, int(cx + rx + 2))):
                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 + 0.25 * (vnoise(x, y, 5202, 3.0) - 0.5) <= 1.0:
                    earth_mask[y, x] = True
    paint_floorpatch(m, earth_mask, prefix='E_floorpatch', on_cls='.d', prot_exact=prot_exact, smooth=2)

    # 3. Pack forest rim & place rich multi-layer coastal/meadow groves
    infill_forest_now(m, seed=520, prot=prot, snow=False)
    for idx, (cx, cy, pal, cnt, rad, hero) in enumerate([
        (47, 93, SPRING_CANOPY, 5, 3.2, 'pf_g_tree2'),
        (56, 79, SPRING_CANOPY, 4, 2.8, None),
        (9, 15, SPRING_CANOPY, 5, 3.0, 'pf_g_tree2'),
        (10, 44, COAST_CANOPY, 4, 2.8, None),
        (52, 26, SPRING_CANOPY, 4, 2.6, None),
        (43, 7, CHERRY_CANOPY, 4, 2.8, None),
        (21, 6, SPRING_CANOPY, 4, 2.6, None),
    ]):
        place_grove_now(m, cx, cy, pal, count=cnt, radius=rad, on='.t', seed=idx + 20, hero=hero, prot=prot)

    # 4. Curated Roadside & Bramble Props + Lantern Posts
    lamp_pts = collect_lamp_positions(m)
    for nm, x, y in (
        ('nt_azalea0', 42, 55), ('nt_azalea1', 48, 49), ('nt_azalea2', 54, 42), ('nt_azalea0', 55, 38),
        ('pf_hayrick', 42, 17), ('pf_hayrick', 51, 24), ('pf_logbench', 19, 71), ('pf_stonebench', 45, 76),
        ('hb_crates4', 49, 36), ('hb_barrels', 55, 36), ('pf_planter0', 14, 104), ('pf_planter1', 20, 104),
    ):
        put_near_now(m, nm, x, y, on='.d', r=2, prot=prot)

    for lx, ly in ((18, 102), (16, 86), (17, 71), (25, 72), (30, 56), (31, 40), (33, 24),
                   (32, 10), (49, 37), (45, 74)):
        res = put_near_now(m, 'pf_lantern', lx, ly - 2, on='.d', r=2, prot=prot)
        if res:
            lamp_pts.append((res[0], res[1] + 1))

    # 5. Duck Pond (48, 72) & SW Sea detailing
    enrich_water_zone(m, water_cls='p', seed=5201, lotus=True, shoals=True, glints=True,
                      reeds_cls='.d', prot=prot)
    enrich_water_zone(m, water_cls='wW', seed=5202, lotus=False, shoals=True, glints=True,
                      buoys=[('hb_buoy', 4, 86), ('hb_buoy2', 3, 103)],
                      rocks=[('cs_wrock0', 6, 91), ('cs_wrock1', 5, 106)],
                      reeds_cls='', prot=prot)

    # 6. Wildflowers, Sea-Pinks & Blossom Petals
    add_petals_and_flowers(m, [
        (16, 75, 5.0, 5.0, 0.35, 'seapink'),
        (15, 92, 4.0, 6.0, 0.30, 'seapink'),
        (48, 48, 9.0, 9.0, 0.25, 'rose'),
        (46, 20, 8.0, 7.0, 0.28, 'wild'),
        (29, 85, 6.0, 4.0, 0.30, 'wild'),
        (48, 72, 7.0, 5.0, 0.26, 'petal'),
        (33, 12, 7.0, 5.0, 0.24, 'petal'),
    ], seed=520)

    # 7. Warm Glows & Sea-Mist Sunbeams
    add_warm_glows(m, lamp_pts + [(15, 69), (11, 84), (52, 35)])
    add_light_shafts(m, [
        (17, 69), (16, 97), (48, 71), (46, 20), (31, 45), (50, 36), (31, 14),
    ])


def craft_527_lacecliff_walk(m, r):
    """527 Lacecliff Walk (Pass 2 Polished): sculpted coastal groves across the western meadow, cliffside overlooks
    with weathered drystone walls & benches, authentic Gen 5 chalk-rock gateways (ZERO MS-Paint arches or lavender
    S_floorpatch spills!), smooth rounded coastal coves & deep-water contours, varied staggered sea-rock reefs &
    Wingull chalk stack, sea-pink thrift carpets, Dew Pond lotus/reeds, warm lamp glows & 0 AT mismatches!"""
    extra_rects = [
        (0, 16, 4, 23),      # W->528 seam
        (135, 20, 139, 27),  # E->520 seam
        (74, 42, 82, 50),    # Lost Thread tide-rock neck
        (42, 9, 46, 16),     # Collapsed 3rd arch + Rock Smash rubble (43..45, 14) + PEARL (44, 10)
        (95, 7, 114, 10),    # High Down corridor between stairs, Birder, Signal Pole & Dew Pond!
        (6, 13, 63, 17),     # West Down staggered chalk ledges (y=14..15) + immediate landing rows!
    ]
    prot_exact, prot = build_prot_mask(m, 527, extra_rects=extra_rects)
    road_prot = prot | np.isin(m.cls, ['u', 'd'])
    if hasattr(r, 'road_mask'):
        road_prot |= r.road_mask
    H, W = m.H, m.W

    # Fix pre-existing HEAD High Down stair pinch: clear stray bushes blocking (98..99, 8..9) & (112, 9)!
    for cx, cy in ((98, 8), (98, 9), (99, 8), (99, 9), (112, 9)):
        if m.inb(cx, cy) and m.ht[cy, cx] == 2 and not m.cliff[cy, cx]:
            m.L[1, cy, cx] = 0
            m.L[2, cy, cx] = 0
            m.taken[cy, cx] = False

    # 1. Mottled coastal heath turf depth (ZERO lavender S_floorpatch spills on green grass!)
    m.grass_var = True
    m.grass_variation(dark=0.47, worn=True)

    # 2. Pack northern coastal woods & transform western meadow (x6..60, y16..39) with scenic coastal groves!
    infill_forest_now(m, seed=527, prot=prot, snow=False)
    WIND_PINE_GROVE = ['nt_pine_a', 'nt_pine_b', 'nt_dpine_sh', 'nt_teal_a', 'tr_oak2', 'nt_dark_sh', 'nt_round_sh']
    for idx, (cx, cy, pal, cnt, rad, hero) in enumerate([
        (12, 19, WIND_PINE_GROVE, 7, 3.4, None),
        (28, 18, WIND_PINE_GROVE, 8, 3.6, None),
        (48, 18, WIND_PINE_GROVE, 7, 3.4, None),
        (16, 32, WIND_PINE_GROVE, 8, 3.6, None),
        (36, 28, WIND_PINE_GROVE, 7, 3.4, None),
        (48, 32, WIND_PINE_GROVE, 8, 3.6, None),
        (63, 18, WIND_PINE_GROVE, 6, 3.2, None),
        (20, 5, COAST_CANOPY, 5, 2.8, None),
        (60, 4, COAST_CANOPY, 5, 2.8, None),
        (132, 6, COAST_CANOPY, 5, 2.8, None),
        (135, 31, COAST_CANOPY, 5, 2.8, None),
        (6, 32, WIND_PINE_GROVE, 5, 2.8, None),
        (74, 12, COAST_CANOPY, 5, 2.8, None),
        (92, 22, WIND_PINE_GROVE, 6, 3.2, None),
    ]):
        place_grove_now(m, cx, cy, pal, count=cnt, radius=rad, on='.t', seed=idx + 30, hero=hero, prot=road_prot, undergrowth=True)

    # 3. Weathered Coastal Drystone Walls along road shoulders & cliffside overlooks
    for y_w, x0_w, x1_w in (
        (17, 17, 23), (17, 35, 41), (26, 10, 17), (27, 22, 30), (26, 42, 49),
        (36, 10, 16), (34, 28, 34), (24, 62, 68),
    ):
        for xw in range(x0_w, x1_w + 1):
            nm_w = 'nr_wall_w' if xw == x0_w else 'nr_wall_e' if xw == x1_w else 'nr_wall_m'
            put_stamp_now(m, nm_w, xw, y_w, on='.t', prot=road_prot)

    # 4. Ground BOTH Arch Gateways (Arch A @ 104,27 & Arch B @ 78,28), Collapsed 3rd Arch, Standing Stones & Cove Props!
    lamp_pts = collect_lamp_positions(m)
    for nm, x, y in (
        # Ground Arch A (wb_gate @ 102..106, 25..29) into chalk rock crags & coastal gorse hedgerows!
        ('ck_rock_big', 99, 27), ('ck_rock_big', 107, 27), ('ck_boulder', 100, 29), ('ck_boulder', 107, 29),
        ('nt_shrub1', 98, 28), ('nt_shrub1', 109, 28), ('nt_azalea0', 100, 25), ('nt_azalea1', 107, 25),
        # Ground Arch B (sculpted Chalk Cairn & Column Gateway @ 75..81, 26..30) into flanking rock crags & hedges!
        ('ck_rock_big', 72, 27), ('ck_rock_big', 82, 27), ('ck_boulder', 74, 29), ('ck_boulder', 81, 29),
        ('nt_shrub1', 71, 28), ('nt_shrub1', 84, 28), ('nt_azalea2', 74, 26), ('nt_azalea0', 81, 26),
        # Authentic collapsed 3rd arch ruin flanking Rock Smash (44, 14) & PEARL (44, 10)
        ('nr_ruin', 39, 12), ('nr_col', 41, 13), ('nr_col', 47, 13), ('nr_colfall', 46, 10),
        ('ck_boulder', 39, 10), ('ck_boulder', 47, 11),
        # Standing stones & coastal rock outcrops across western heath
        ('nr_col', 19, 28), ('nr_col', 21, 29), ('nr_colfall', 20, 31),
        ('nr_col', 52, 28), ('ck_rock_big', 25, 31), ('ck_rock_big', 53, 19),
        ('ck_boulder', 11, 27), ('ck_boulder', 39, 25), ('ck_boulder', 58, 30),
        # Cliffside overlook benches, lanterns & cove details
        ('pf_stonebench', 12, 35), ('pf_stonebench', 30, 34), ('pf_stonebench', 25, 20), ('pf_stonebench', 44, 22),
        ('pf_stonebench', 115, 46), ('hb_barrels', 113, 39), ('hb_crates4', 109, 39),
        ('cs_shell0', 27, 47), ('cs_shell1', 39, 47), ('cs_shell0', 86, 48), ('cs_shell1', 94, 48),
        ('nt_azalea0', 53, 41), ('nt_azalea1', 61, 41), ('nt_azalea2', 114, 43),
        ('nt_azalea0', 15, 35), ('nt_azalea1', 34, 34), ('nt_azalea2', 22, 26), ('nt_azalea0', 46, 26),
    ):
        on_c = 's' if nm.startswith('cs_') else '.du'
        put_near_now(m, nm, x, y, on=on_c, r=2, prot=road_prot if nm not in ('nr_col', 'nr_ruin', 'nr_colfall', 'ck_boulder', 'ck_rock_big') else prot)

    for lx, ly in ((132, 23), (118, 22), (102, 31), (106, 31), (76, 31), (80, 31), (91, 35), (76, 22), (57, 24),
                   (58, 41), (32, 22), (12, 22), (118, 46), (105, 5), (14, 36), (33, 35), (44, 21)):
        res = put_near_now(m, 'pf_lantern', lx, ly - 2, on='.du', r=2, prot=road_prot)
        if res:
            lamp_pts.append((res[0], res[1] + 1))

    # 5. Dew Pond (113, 6) lotus & reeds + Rich Coastal Sea (varied rock reefs, buoys, glints — ZERO cs_shoal squares!)
    enrich_water_zone(m, water_cls='p', seed=5271, lotus=True, shoals=False, glints=True,
                      reeds_cls='.d', prot=prot)
    enrich_water_zone(m, water_cls='wW', seed=5272, lotus=False, shoals=False, glints=True,
                      buoys=[('hb_buoy', 18, 52), ('hb_buoy2', 44, 54), ('hb_buoy', 88, 56),
                             ('hb_buoy2', 124, 57)],
                      rocks=[('cs_wrock0', 7, 55), ('cs_wrockb0', 14, 57), ('cs_wrock1', 28, 57), ('cs_wrock2', 31, 59),
                             ('cs_wrock2', 58, 56), ('cs_wrockb1', 62, 58), ('cs_wrock0', 84, 59),
                             ('cs_wrock1', 102, 56), ('cs_wrock0', 108, 56), ('cs_wrock2', 113, 55), ('cs_wrockb1', 112, 58),
                             ('cs_wrock2', 134, 57)],
                      reeds_cls='', prot=prot)

    # Clear any stray cs_shoal0/cs_shoal1 near Cove A boat & pier (28..42, 48..55)
    sh_ids = {P1('cs_shoal0'), P1('cs_shoal1')}
    for y in range(48, 56):
        for x in range(28, 43):
            if m.inb(x, y) and int(m.L[2, y, x]) in sh_ids:
                m.L[2, y, x] = 0

    # 6. Iconic Sea-Pink Thrift Hollow (22, 5) & Sweeping Cliff-Top + Overlook Wildflower Drifts
    add_petals_and_flowers(m, [
        (22, 5, 7.0, 3.2, 0.72, 'seapink'),   # Hidden field of sea-pinks!
        (57, 39, 6.0, 3.5, 0.45, 'seapink'),  # Lacemakers' Bench headland
        (119, 43, 6.0, 4.5, 0.45, 'seapink'), # Wrecker's Lamp headland
        (13, 36, 5.5, 3.0, 0.48, 'seapink'),  # West cliffside overlook
        (32, 34, 5.5, 2.8, 0.44, 'seapink'),  # Cove A overlook
        (21, 22, 6.0, 3.0, 0.38, 'wild'),     # West meadow roadside flowers
        (43, 24, 6.5, 3.2, 0.40, 'wild'),     # Mid meadow roadside flowers
        (53, 21, 5.0, 2.8, 0.38, 'seapink'),  # East meadow roadside thrift
        (113, 7, 8.0, 3.5, 0.35, 'wild'),     # High Down Dew Pond
        (46, 9, 7.0, 3.0, 0.32, 'wild'),      # West Down
        (88, 25, 8.0, 4.0, 0.28, 'seapink'),  # Mid cliff heath
        (16, 26, 7.0, 4.0, 0.32, 'wild'),     # West cliff road
    ], seed=527)

    # 7. Warm Glows ONLY on real lamps/beacons/campfire (ZERO outdoor cv_shaft smears!)
    add_warm_glows(m, lamp_pts + [(120, 47), (104, 4), (34, 43)])

    # 8. Rebuild ALL coastal & dirt autotiles on a SINGLE layer (L0) with exact 48-tile NB2AUTO (0 mismatches — was 280!)
    # Smooth away any 1-tile jagged Dirt ('u') spurs around y=28..35 before recomputing NB2AUTO
    dirt_lo = RC.vauto('rejuvenation', 'Dirt', 0)
    dirt_hi = dirt_lo + 48
    dmask = ((m.L[0] >= dirt_lo) & (m.L[0] < dirt_hi)) | ((m.L[1] >= dirt_lo) & (m.L[1] < dirt_hi))
    # Fill 1-tile holes inside dirt & trim 1-tile isolated dirt speckles (skip protected cells)
    pad_d = np.pad(dmask, 1, constant_values=False)
    n4_d = pad_d[:-2, 1:-1].astype(int) + pad_d[2:, 1:-1] + pad_d[1:-1, :-2] + pad_d[1:-1, 2:]
    for yy, xx in zip(*np.where(dmask & (n4_d == 0) & ~prot)):
        if dirt_lo <= int(m.L[1, yy, xx]) < dirt_hi:
            m.L[1, yy, xx] = 0
        if dirt_lo <= int(m.L[0, yy, xx]) < dirt_hi:
            m.L[0, yy, xx] = K.SH_GRASS[yy % 2][xx % 2]
    # Ensure EVERY beach sand cell ('s') has Sand shore on L0 (never hidden Ocean L0 under cove props or cliff bases!)
    sand_lo = RC.vauto('rejuvenation', 'Sand shore', 0)
    sand_hi = sand_lo + 48
    for yy, xx in np.argwhere(m.cls == 's'):
        m.L[0, yy, xx] = sand_lo
        if sand_lo <= int(m.L[1, yy, xx]) < sand_hi:
            m.L[1, yy, xx] = 0
        if sand_lo <= int(m.L[2, yy, xx]) < sand_hi:
            m.L[2, yy, xx] = 0
    fix_vauto_l0_w12(m.L, 'rejuvenation', 'Dirt')
    fix_vauto_l0_w12(m.L, 'rejuvenation', 'DirtDark')
    fix_vauto_l0_w12(m.L, 'rejuvenation', 'Sea deep')
    fix_vauto_l0_w12(m.L, 'rejuvenation', 'Sand shore')
    fix_vauto_l0_w12(m.L, 'rejuvenation', 'Ocean')
    fix_vauto_l0_w12(m.L, 'rejuvenation', 'Sea(Grass)')


def craft_528_marram_down(m, r):
    """528 Marram Down: tiered dunes overlooking Saltmere, glowing Beacon summit terrace,
    Players' Rehearsal Camp with crimson stage mat & festoons, half-buried theatre barge,
    Brackish Pool lotus/reeds, Saltmere Free Port stone gate approach, buoys & golden sunbeams!"""
    bx = r.chute[0] if hasattr(r, 'chute') else 52
    extra_rects = [
        (0, 36, 4, 43),          # W->140 Saltmere East Gate seam
        (105, 28, 109, 35),      # E->527 Lacecliff Walk seam
        (bx - 1, 8, bx + 1, 66), # Sledge Run chute column!
        (12, 54, 34, 65),        # Half-buried theatre barge (Wandering Chorus) + west beach approach!
    ]
    prot_exact, prot = build_prot_mask(m, 528, extra_rects=extra_rects)
    H, W = m.H, m.W

    # Fix pre-existing HEAD Prompter's Box beach pinch around west bow of the buried theatre barge!
    for cx, cy in ((12, 57), (13, 57), (13, 61), (14, 61), (13, 60), (13, 59), (15, 58), (16, 58), (19, 58)):
        if m.inb(cx, cy) and not m.cliff[cy, cx]:
            m.L[1, cy, cx] = 0
            m.L[2, cy, cx] = 0
            m.taken[cy, cx] = False

    # 1. Rich dune-slack grass depth
    m.grass_var = True
    m.grass_variation(dark=0.47, worn=True)

    # 2. Beacon Summit Stone Terrace (`S_floorpatch`), Saltmere Gate Approach (`S_floorpatch`) & Players' Camp (`E_floorpatch`)!
    stone_mask = np.zeros((H, W), dtype=bool)
    for cx, cy, rx, ry in (
        (56, 9, 5.2, 3.2),    # Saltmere Beacon summit lookout!
        (4, 39, 4.5, 4.0),    # Free Port Gate cobbled approach!
    ):
        for y in range(max(2, int(cy - ry - 1)), min(H - 2, int(cy + ry + 2))):
            for x in range(max(1, int(cx - rx - 1)), min(W - 2, int(cx + rx + 2))):
                if abs(x - bx) <= 1:
                    continue
                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 + 0.22 * (vnoise(x, y, 5281, 3.0) - 0.5) <= 1.0:
                    stone_mask[y, x] = True
    paint_floorpatch(m, stone_mask, prefix='S_floorpatch', on_cls='.du', prot_exact=prot_exact, smooth=2)

    camp_mask = np.zeros((H, W), dtype=bool)
    for y in range(40, 50):
        for x in range(62, 83):
            if ((x - 72) / 9.5) ** 2 + ((y - 45) / 4.5) ** 2 + 0.25 * (vnoise(x, y, 5282, 3.0) - 0.5) <= 1.0:
                camp_mask[y, x] = True
    paint_floorpatch(m, camp_mask, prefix='E_floorpatch', on_cls='.du', prot_exact=prot_exact, smooth=2)

    # Seamless Crimson Theatre Rehearsal Rug in the heart of the Players' Camp (zero NPC cutout holes!)
    paint_carpet_rect(m, 69, 43, 74, 45, on_cls='.du')

    # 3. Pack northern dune pines & place lush coastal pine/blossom windbreak clusters
    infill_forest_now(m, seed=528, prot=prot, snow=False)
    for idx, (cx, cy, pal, cnt, rad, hero) in enumerate([
        (9, 7, COAST_CANOPY, 4, 2.8, None),
        (103, 7, COAST_CANOPY, 4, 2.8, None),
        (30, 9, COAST_CANOPY, 4, 2.6, None),
        (84, 9, COAST_CANOPY, 4, 2.6, None),
        (5, 29, COAST_CANOPY, 4, 2.6, None),
        (105, 47, COAST_CANOPY, 4, 2.6, None),
    ]):
        place_grove_now(m, cx, cy, pal, count=cnt, radius=rad, on='.t', seed=idx + 40, hero=hero, prot=prot)

    # 4. Beacon Braziers, Camp Props, Gate Lanterns & Beach Shells
    lamp_pts = collect_lamp_positions(m)
    for nm, x, y in (
        ('fw_brazier', 57, 7), ('pf_stonebench', 59, 10), ('pf_planter0', 4, 35), ('pf_planter1', 4, 43),
        ('pf_logbench', 69, 47), ('hb_crates4', 82, 46), ('hb_boxes', 63, 46),
        ('cs_shell0', 38, 64), ('cs_shell1', 59, 64), ('cs_shell0', 74, 65), ('cs_shell1', 90, 64),
    ):
        on_c = 's' if nm.startswith('cs_') else '.du'
        res = put_near_now(m, nm, x, y, on=on_c, r=2, prot=prot)
        if res and nm == 'fw_brazier':
            lamp_pts.append((res[0], res[1]))

    for lx, ly in ((6, 37), (6, 42), (24, 39), (46, 36), (62, 37), (80, 34), (98, 33),
                   (66, 42), (76, 42), (71, 47), (59, 11), (96, 20)):
        res = put_near_now(m, 'pf_lantern', lx, ly - 2, on='.du', r=2, prot=prot)
        if res:
            lamp_pts.append((res[0], res[1] + 1))

    # 5. Brackish Pool (96, 15) lotus & reeds + Southern Sea buoys/shoals/glints!
    enrich_water_zone(m, water_cls='p', seed=5281, lotus=True, shoals=True, glints=True,
                      reeds_cls='.du', prot=prot)
    enrich_water_zone(m, water_cls='wW', seed=5282, lotus=False, shoals=True, glints=True,
                      buoys=[('hb_buoy', 22, 72), ('hb_buoy2', 48, 72), ('hb_buoy', 72, 71), ('hb_buoy2', 102, 72)],
                      rocks=[('cs_wrock0', 6, 73), ('cs_wrock1', 41, 74), ('cs_wrock2', 66, 75), ('cs_wrock0', 87, 74)],
                      reeds_cls='', prot=prot)

    # 6. Dune Sea-Pinks, Rehearsal Camp Petals & Wildflower Slacks
    add_petals_and_flowers(m, [
        (72, 44, 8.0, 4.0, 0.22, 'petal'),    # Players' rehearsal camp festive petals!
        (55, 9, 7.0, 4.0, 0.32, 'seapink'),   # Saltmere Beacon summit
        (36, 57, 10.0, 3.0, 0.40, 'seapink'), # Foredune sea-pinks
        (14, 38, 7.0, 4.0, 0.32, 'seapink'),  # Saltmere Gate dunes
        (88, 30, 8.0, 4.0, 0.28, 'wild'),     # East slack
        (26, 28, 7.0, 4.0, 0.28, 'wild'),     # West slack
        (96, 17, 7.0, 4.0, 0.28, 'wild'),     # Brackish pool
    ], seed=528)

    # 7. Camp Festoon Strings, Warm Glows & Golden Beacon Sunbeams!
    add_festoon_strings(m, [
        (65, 78, 41, 0), (66, 77, 46, 2), (2, 8, 39, 1),
    ], kind='garl')
    add_warm_glows(m, lamp_pts + [(54, 6), (55, 9), (70, 45), (3, 39), (24, 60)])
    add_light_shafts(m, [
        (55, 8), (71, 43), (4, 38), (24, 59), (96, 15), (32, 37), (86, 35),
    ])


def craft_540_thistledown_lea(m, r):
    """540 Thistledown Lea (Pass 2 Polished): grand overgrown estate meadows & Selvedge river!
      - Fixes ALL 3 softlocks: (a) unseals Greavard @ (80,6) & purges orphaned cliff stubs (81..86,4..8);
        (b) clears porch rail blocker (63,10) & left stair cliff wall (60..62,12..13) for Locked door @ (61,9);
        (c) clears solid L2 cliff 6105 off Mine mouth warp @ (9,25)!
      - Replaces E_floorpatch dark mud blobs with clean single-layer RJ DirtDark NB2AUTO (0 mismatches!)
      - Replaces yellow-box lm_topiary with Gen 5 shrubs/flowerbeds & pulls S_floorpatch clear of cliff edges
      - Strips outdoor cv_shaft smears, bridge pf_glow (21,51), detached cs_shoal1 (32,49) & stark fw_reeds1!"""
    extra_rects = [
        (18, 59, 25, 63),    # S->552 seam
        (125, 28, 129, 35),  # E->524 Gossamer Wood seam
        (18, 46, 25, 59),    # Old Stone Bridge
        (28, 28, 48, 32),    # Ponyta paddock ledges
        (78, 1, 93, 25),     # Ha-ha ditch & Greavard back garden
        (6, 18, 12, 26),     # Brinecut mine mouth
        (34, 20, 41, 27),    # Ponyta (36,22) grazing ring & Drover (40,26) approach
        (59, 9, 68, 15),     # Manor porch + BOTH stairs (61,11..14) & (66..67,11..14)!
    ]
    prot_exact, prot = build_prot_mask(m, 540, extra_rects=extra_rects)
    road_prot = prot | np.isin(m.cls, ['d', 'u'])
    if hasattr(r, 'road_mask'):
        road_prot |= r.road_mask
    H, W = m.H, m.W

    # ---- 0. HARD FIX ALL 3 P0 GAMEPLAY SOFTLOCKS! ----
    # (a) Mine mouth warp @ (9, 25): clear solid L2 cliff bottom 6105 stamped over pf_minemouth portal!
    if m.inb(9, 25):
        m.L[2, 25, 9] = 0
        m.cliff[25, 9] = False
    # (b) Locked door @ (61, 9): replace blocking porch rail 5014 (pas=5) at (63, 10) with walk-through rail 4982 (pas=1, Down-only)!
    if m.inb(63, 10) and int(m.L[2, 10, 63]) == 5014:
        m.L[2, 10, 63] = 4982
    # Ensure left terrace stair (61..62, 12..14) & foot landing (61..62, 15) stay completely clear of rock/cliffs!
    for sy in (12, 13, 14):
        for sx in (61, 62):
            if m.inb(sx, sy):
                m.cliff[sy, sx] = False
                m.taken[sy, sx] = True
    for sx in (60, 61, 62):
        if m.inb(sx, 15):
            m.L[1, 15, sx] = 0
            m.L[2, 15, sx] = 0
            m.cliff[15, sx] = False
    for sx in (60, 61):
        if m.inb(sx, 16):
            m.L[1, 16, sx] = 0
            m.L[2, 16, sx] = 0
    # (c) Greavard & Ha-ha back garden (79..87, 3..7): purge any residual cliff stubs & keep walkable dirt garden path clear!
    cliff_stubs = {6072, 6073, 6075, 6080, 6082, 6083, 6084, 6088, 6089, 6090, 6096, 6097, 6098, 6104, 6105, 6106}
    for gy in range(3, 8):
        for gx in range(79, 88):
            if m.inb(gx, gy):
                if int(m.L[1, gy, gx]) in cliff_stubs:
                    m.L[1, gy, gx] = 0
                if int(m.L[2, gy, gx]) in cliff_stubs:
                    m.L[2, gy, gx] = 0
                m.cliff[gy, gx] = False
    dd_lo = RC.vauto('rejuvenation', 'DirtDark', 0)
    for gy in (4, 5):
        for gx in range(80, 87):
            if m.inb(gx, gy):
                m.L[0, gy, gx] = dd_lo
                m.L[1, gy, gx] = 0
                m.L[2, gy, gx] = 0
                m.cls[gy, gx] = 'd'
                m.cliff[gy, gx] = False

    # 1. Deep unmown meadow shaded turf variation
    m.grass_var = True
    m.grass_variation(dark=0.46, worn=True)

    # 2. Manor Hill Weathered Limestone Estate Terraces (`S_floorpatch`) kept strictly >= 1 tile clear of ALL cliff walls!
    cliff_pad = np.pad(m.cliff, 1, constant_values=False)
    near_cliff = (cliff_pad[:-2, 1:-1] | cliff_pad[2:, 1:-1] | cliff_pad[1:-1, :-2] | cliff_pad[1:-1, 2:] |
                  cliff_pad[:-2, :-2] | cliff_pad[:-2, 2:] | cliff_pad[2:, :-2] | cliff_pad[2:, 2:] | m.cliff)
    manor_mask = np.zeros((H, W), dtype=bool)
    for y in range(14, 21):
        for x in range(54, 76):
            if m.ht[y, x] >= 1 and not near_cliff[y, x] and m.cls[y, x] in '.d':
                d2 = ((x - 65) / 10.5) ** 2 + ((y - 17) / 3.4) ** 2
                if d2 + 0.25 * (vnoise(x, y, 5401, 3.5) - 0.5) <= 0.90:
                    manor_mask[y, x] = True
    paint_floorpatch(m, manor_mask, prefix='S_floorpatch', on_cls='.d', prot_exact=prot_exact, smooth=2)

    # Organic worn earth strictly via properly bordered RJ DirtDark (REPLACING ugly square E_floorpatch blobs!)
    earth_mask = np.zeros((H, W), dtype=bool)
    for cx, cy, rx, ry in (
        (80, 41, 5.4, 3.4),   # Mowers' camp yard
        (95, 45, 3.8, 2.6),   # Broken mill yard
    ):
        for y in range(max(2, int(cy - ry - 1)), min(H - 2, int(cy + ry + 2))):
            for x in range(max(2, int(cx - rx - 1)), min(W - 2, int(cx + rx + 2))):
                if m.cls[y, x] in '.d' and not near_cliff[y, x]:
                    if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 + 0.25 * (vnoise(x, y, 5402, 3.0) - 0.5) <= 1.0:
                        earth_mask[y, x] = True
    # Smooth curved dirt trail junction from main road (112,31) -> (110,27) -> (111,24)
    curve_pts = [(113.0, 31.5), (111.5, 29.5), (110.2, 27.5), (110.0, 25.5), (111.0, 24.0)]
    for x in range(107, 116):
        for y in range(23, 33):
            if m.cls[y, x] in '.d' and not near_cliff[y, x]:
                md = min(math.hypot(x - px, y - py) for px, py in curve_pts)
                if md <= 1.55 + 0.25 * (vnoise(x, y, 5406, 2.5) - 0.5):
                    earth_mask[y, x] = True
    # Natural curved paddock grazing track from west drove-way (29, 22) -> (35, 22) -> (39, 25)
    pad_pts = [(29.5, 22.0), (32.5, 21.5), (35.5, 22.2), (38.0, 23.5), (39.5, 25.0)]
    for x in range(29, 43):
        for y in range(20, 27):
            if m.cls[y, x] in '.d' and not near_cliff[y, x]:
                md = min(math.hypot(x - px, y - py) for px, py in pad_pts)
                if md <= 1.65 + 0.3 * (vnoise(x, y, 5407, 2.8) - 0.5):
                    earth_mask[y, x] = True
    earth_mask = smooth_bool_mask(earth_mask, np.isin(m.cls, ['.', 'd']) & ~near_cliff, passes=2)
    for y, x in np.argwhere(earth_mask):
        if m.L[1, y, x] == 0 or (dd_lo <= int(m.L[1, y, x]) < dd_lo + 48):
            m.L[0, y, x] = dd_lo
            if dd_lo <= int(m.L[1, y, x]) < dd_lo + 48:
                m.L[1, y, x] = 0

    # 3. Pack forest rim & place cohesive multi-tree estate groves framing clear sunlit meadows!
    infill_forest_now(m, seed=540, prot=prot, snow=False)
    ESTATE_GROVE = ['tr_oak2', 'tr_oak', 'nt_dark_sh', 'nt_teal_a', 'nt_olive', 'nt_round_sh']
    for idx, (cx, cy, pal, cnt, rad, hero) in enumerate([
        (119, 12, GOSSAMER_EDGE, 8, 3.8, 'pf_g_tree2'),
        (124, 46, GOSSAMER_EDGE, 7, 3.4, 'pf_g_tree2'),
        (7, 40, ESTATE_GROVE, 7, 3.4, None),
        (36, 7, CHERRY_CANOPY, 7, 3.4, None),
        (15, 9, ESTATE_GROVE, 6, 3.2, None),
        (49, 46, ESTATE_GROVE, 7, 3.4, None),
        (100, 46, ESTATE_GROVE, 6, 3.2, None),
        (24, 13, ESTATE_GROVE, 6, 3.2, None),
        (102, 13, GOSSAMER_EDGE, 6, 3.2, None),
        (116, 44, GOSSAMER_EDGE, 6, 3.2, None),
        (68, 45, ESTATE_GROVE, 5, 2.8, None),
        (70, 53, CHERRY_CANOPY, 2, 1.8, None),   # River islet 1 shade!
        (104, 54, SPRING_CANOPY, 2, 1.6, None),  # River islet 2 shade!
    ]):
        place_grove_now(m, cx, cy, pal, count=cnt, radius=rad, on='.t', seed=idx + 50, hero=hero, prot=road_prot, undergrowth=True)

    # 4. Lived-In Pastoral Ponyta Paddock (x29-46, y17-27): hay bales, trough, fruit trees, crates, wagon & aligned east rail!
    # (Removed disconnected west stub at (29, 25..26) and anchored ledge ends cleanly with shrubs!)
    pal_v = P1('fw_pal_v')
    for py_ in range(18, 27):
        if m.inb(47, py_) and m.cls[py_, 47] == '.' and not m.taken[py_, 47] and not prot[py_, 47] and m.L[1, py_, 47] == 0:
            m.L[1, py_, 47] = pal_v
            m.taken[py_, 47] = True
    # Ground paddock ledge corners at (29, 30) & (47, 30) with natural mossy boulders/shrubs
    for gx, gy, nm in ((29, 30, 'nt_boulder'), (47, 30, 'nt_boulder'), (29, 28, 'nt_shrub0')):
        if m.inb(gx, gy) and not prot[gy, gx]:
            put_near_now(m, nm, gx, gy, on='.t', r=1, prot=prot)
    # Paddock shade fruit trees in NW & NE corners (off grazing ring & events!)
    place_grove_now(m, 44, 19, ['tr_pink', 'nt_blossom', 'tr_oak2'], count=2, radius=1.8, on='.', seed=5401, prot=road_prot, undergrowth=False)
    place_grove_now(m, 31, 25, ['nt_blossom', 'tr_oak2'], count=1, radius=1.2, on='.', seed=5402, prot=road_prot, undergrowth=False)
    if put_stamp_now(m, 'mn_trough_l', 33, 18, on='.', prot=road_prot):
        put_stamp_now(m, 'mn_trough_r', 34, 18, on='.', prot=road_prot)
    for nm, x, y in (
        ('pf_hayrick', 30, 18), ('pf_hayrick', 44, 18), ('pf_hayrick', 42, 24),
        ('pf_wagon', 43, 21), ('hb_crates4', 30, 20), ('hb_barrels', 45, 23),
        ('hb_post1', 36, 18), ('hb_post1', 40, 18), ('pf_logbench', 31, 25),
        ('nt_azalea0', 29, 24), ('nt_azalea1', 45, 26),
    ):
        put_near_now(m, nm, x, y, on='.d', r=1, prot=road_prot)

    # 5. Manor Garden Statues, Lush Gen 5 Azalea/Shrub Hedges (REPLACED yellow-box lm_topiary!), Bamboo & Estate Lanterns!
    lamp_pts = collect_lamp_positions(m)
    for nm, x, y in (
        ('mn_statue', 63, 16), ('mn_statue', 70, 16),
        ('nt_azalea0', 55, 14), ('nt_azalea1', 76, 14), ('nt_shrub0', 69, 14), ('nt_shrub1', 55, 16),
        ('pf_stonebench', 61, 18), ('pf_stonebench', 70, 18),
        ('pf_planter0', 62, 23), ('pf_planter1', 68, 23), ('pf_hayrick', 74, 40), ('pf_hayrick', 85, 42),
        ('hb_barrels', 92, 46), ('hb_crates4', 98, 46), ('pf_logbench', 35, 38),
        ('pf_bamboo', 109, 19), ('pf_bamboo', 115, 19), ('pf_bamboo', 117, 21), ('pf_bamboo', 111, 14),
        ('pf_bamboo', 107, 20), ('pf_bamboo', 114, 21),
    ):
        put_near_now(m, nm, x, y, on='.dt', r=2, prot=road_prot)

    for lx, ly in ((24, 46), (24, 59), (38, 35), (56, 33), (63, 25), (67, 25), (64, 15),
                   (70, 15), (78, 34), (96, 35), (114, 31), (124, 31), (14, 30), (31, 23)):
        res = put_near_now(m, 'pf_lantern', lx, ly - 2, on='.d', r=2, prot=road_prot)
        if res:
            lamp_pts.append((res[0], res[1] + 1))

    # 6. River Selvedge: bank- & islet-hugging organic lily-pad clusters (NO cs_shoal1 wood squares, NO stark white fw_reeds1!)
    enrich_water_zone(m, water_cls='w', seed=540, lotus=False, shoals=False, glints=True,
                      rocks=[('cs_wrock0', 10, 52), ('cs_wrock1', 35, 54), ('cs_wrock2', 52, 52),
                             ('cs_wrock0', 84, 53), ('cs_wrock1', 116, 54)],
                      reeds_cls='', prot=prot, glint_density=0.05)
    # Clear any stray cs_shoal0/1, stark fw_reeds tiles, or water rocks overlapping the Old Stone Bridge (x=19..23)!
    bad_river = {P1('cs_shoal0'), P1('cs_shoal1'), 19265, 19266, 19267, 19268}
    for y in range(44, H):
        for x in range(W):
            if int(m.L[1, y, x]) in bad_river:
                m.L[1, y, x] = 0
            if int(m.L[2, y, x]) in bad_river:
                m.L[2, y, x] = 0
    m.L[2, 47:58, 19:24] = 0
    # Cluster lily pads organically near calm river banks & islet coves ONLY (clear central channel!)
    rng_lot = random.Random(54099)
    lotus_coves = [
        (13, 50, 3.2, 1.8), (39, 50, 3.5, 1.8), (67, 52, 4.0, 2.2),
        (74, 54, 3.8, 2.0), (101, 53, 3.5, 2.0), (108, 55, 3.2, 1.8),
        (56, 56, 3.4, 1.6), (89, 51, 3.2, 1.8), (121, 52, 3.5, 1.8),
    ]
    for lcx, lcy, lrx, lry in lotus_coves:
        for y in range(max(2, int(lcy - lry - 1)), min(H - 2, int(lcy + lry + 2))):
            for x in range(max(2, int(lcx - lrx - 1)), min(W - 2, int(lcx + lrx + 2))):
                if m.cls[y, x] != 'w' or m.L[1, y, x] != 0 or m.L[2, y, x] != 0 or prot[y, x]:
                    continue
                near_bank = any(m.cls[y + dy, x + dx] != 'w'
                                for dy in range(-2, 3) for dx in range(-2, 3)
                                if m.inb(x + dx, y + dy))
                if not near_bank:
                    continue
                d2 = ((x - lcx) / lrx) ** 2 + ((y - lcy) / lry) ** 2
                if d2 <= 1.0 and rng_lot.random() < 0.62 * (1.0 - 0.45 * d2):
                    m.L[2, y, x] = rng_lot.choice(LOTUS_TILES)

    # 7. Sweeping Unmown Wildflower Ribbons, Paddock Clumps, Manor Roses & Bamboo/Orchard Petals!
    add_petals_and_flowers(m, [
        (66, 15, 13.0, 6.0, 0.35, 'rose'),    # Overgrown Thistledown Manor rose garden!
        (33, 19, 4.5, 2.0, 0.48, 'wild'),     # Ponyta paddock north fence flowers
        (42, 26, 4.8, 1.8, 0.46, 'wild'),     # Ponyta paddock south fence flowers
        (46, 44, 11.0, 4.0, 0.38, 'wild'),    # Unmown south meadows
        (88, 42, 10.0, 5.0, 0.30, 'petal'),   # Mowers' meadow petals
        (111, 21, 5.5, 4.0, 0.32, 'petal'),   # Bamboo stand drifting leaves/petals
        (110, 27, 4.0, 2.5, 0.36, 'wild'),    # Curved Bamboo trail junction border
        (118, 34, 8.0, 6.0, 0.30, 'rose'),    # Gossamer Wood border glade
        (18, 38, 7.0, 5.0, 0.35, 'wild'),     # West river lea
    ], seed=540)

    # 8. Warm Antique Lantern Glows ONLY on real lamps & Mowers' campfire (ZERO outdoor cv_shaft & ZERO orphaned bridge glow (21,51)!)
    add_warm_glows(m, lamp_pts + [(78, 41)])

    # 9. Consolidate ALL RJ DirtDark onto L0 ONLY & recompute exact 48-tile NB2AUTO (0 mismatches — was 47!)
    fix_vauto_l0_w12(m.L, 'rejuvenation', 'DirtDark')
    fix_vauto_l0_w12(m.L, 'rejuvenation', 'Sea(Grass)')


def craft_541_grey_saltings(m, r):
    """541 The Grey Saltings: atmospheric tidal salt marsh & salterns north of Saltmere!
      - 100% preserves S->140 [30..35], N->552 [34..37], Drowned Lane (y=84), night boardwalk planks
        (25,38 / 27,45 / 44,77), Wreckers' Islet (4,84), and Brinecut Mine back door (52, my)!
      - Transforms blinding white/pink SW salt pans into authentic weathered grey-mineral salt-flats
        (`S_floorpatch` + `cs_wet` damp tidal rings + salt carts & lanterns)
      - Enriches marsh pools & estuary with tall reeds (`fw_reeds`), shoals, buoys & misty lanterns
      - Weathered chalk mine apron on Brinecut + warm hearth yard at The Brinewife's Rest!"""
    extra_rects = [
        (28, 105, 37, 109),  # S->140 Saltmere North Gate seam
        (32, 0, 39, 4),      # N->552 seam
        (1, 80, 22, 88),     # Wreckers' Islet + Drowned Lane (y=84)!
        (49, 32, 55, 41),    # Brinecut Mine back door!
        (10, 56, 16, 62),    # Brinewife's Rest cottage doorstep
    ]
    extra_pts = [(25, 38), (27, 45), (44, 77), (25, 34), (45, 101), (28, 88)]
    prot_exact, prot = build_prot_mask(m, 541, extra_rects=extra_rects, extra_pts=extra_pts)
    H, W = m.H, m.W

    # 1. Moody wet-marsh shaded turf variation
    m.grass_var = True
    m.grass_variation(dark=0.40, worn=True)

    # 2. Transform SW Salt Pans (x=10..30, y=90..107) — kill stark white/pink blob!
    craft_salt_flats(m, seed=541, pink_keep=0.18, grey_salt=True, prot=prot)

    # 3. Chalk Mine Apron (`S_floorpatch`) on Brinecut Shelf & Packed-Earth Yards (`E_floorpatch`)
    chalk_mask = np.zeros((H, W), dtype=bool)
    for cx, cy, rx, ry in ((52, 35, 5.5, 4.0), (58, 22, 5.0, 3.5), (56, 10, 5.0, 3.2)):
        for y in range(max(2, int(cy - ry - 1)), min(H - 2, int(cy + ry + 2))):
            for x in range(max(39, int(cx - rx - 1)), min(W - 2, int(cx + rx + 2))):
                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 + 0.25 * (vnoise(x, y, 5411, 3.0) - 0.5) <= 1.0:
                    chalk_mask[y, x] = True
    paint_floorpatch(m, chalk_mask, prefix='S_floorpatch', on_cls='.dg', prot_exact=prot_exact, smooth=2)

    earth_mask = np.zeros((H, W), dtype=bool)
    for cx, cy, rx, ry in (
        (13, 60, 4.8, 3.2),   # Brinewife's Rest cottage garden yard
        (45, 101, 5.2, 3.8),  # Crabrawler mudflat ring
        (28, 86, 4.5, 3.2),   # Boiling-house yard
        (46, 62, 4.0, 2.8),   # Bird hide clearing
    ):
        for y in range(max(2, int(cy - ry - 1)), min(H - 2, int(cy + ry + 2))):
            for x in range(max(2, int(cx - rx - 1)), min(W - 2, int(cx + rx + 2))):
                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 + 0.25 * (vnoise(x, y, 5412, 3.0) - 0.5) <= 1.0:
                    earth_mask[y, x] = True
    paint_floorpatch(m, earth_mask, prefix='E_floorpatch', on_cls='.dg', prot_exact=prot_exact, smooth=2)

    # Damp estuary mudflat sheen (`cs_wet`) along the west shoreline & marsh pool margins
    wet_shore = np.zeros((H, W), dtype=bool)
    for y in range(2, H - 2):
        for x in range(2, W - 2):
            if m.cls[y, x] == 'd' and not m.cliff[y, x]:
                if any(m.cls[y + dy, x + dx] in 'wWp' for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    if vnoise(x, y, 5415, 4.0) > 0.35:
                        wet_shore[y, x] = True
    paint_cs_wet_overlay(m, wet_shore, on_cls='d', smooth=1)

    # 4. Pack East Forest Band & Marsh Pine Copses
    infill_forest_now(m, seed=541, prot=prot, snow=False)
    for idx, (cx, cy, pal, cnt, rad, hero) in enumerate([
        (60, 76, MARSH_CANOPY, 4, 2.8, None),
        (58, 96, MARSH_CANOPY, 5, 3.0, 'pf_g_tree2'),
        (62, 8, MARSH_CANOPY, 4, 2.8, None),
        (16, 10, MARSH_CANOPY, 4, 2.8, None),
        (62, 48, MARSH_CANOPY, 4, 2.6, None),
    ]):
        place_grove_now(m, cx, cy, pal, count=cnt, radius=rad, on='.t', seed=idx + 60, hero=hero, prot=prot)

    # 5. Saltern Carts, Mine Barrels, Brinewife's Garden & Misty Causeway Lanterns!
    lamp_pts = collect_lamp_positions(m)
    for nm, x, y in (
        ('cv_cart_salt', 25, 92), ('cv_cart_salt', 17, 98), ('cv_cart_salt', 24, 103),
        ('cv_cart_salt', 50, 39), ('hb_barrels', 55, 39), ('hb_crates4', 49, 41),
        ('pf_planter0', 10, 59), ('pf_planter1', 15, 59), ('pf_logbench', 15, 61),
        ('fw_brazier', 27, 86), ('fw_brazier', 42, 99), ('fw_brazier', 48, 99),
    ):
        on_c = 'S' if nm == 'cv_cart_salt' and y >= 90 else '.dg'
        res = put_near_now(m, nm, x, y, on=on_c, r=2, prot=prot)
        if res and nm == 'fw_brazier':
            lamp_pts.append((res[0], res[1]))

    for lx, ly in ((34, 104), (35, 92), (33, 78), (33, 64), (31, 48), (32, 34), (35, 20),
                   (36, 8), (15, 60), (50, 40), (22, 90), (45, 63)):
        res = put_near_now(m, 'pf_lantern', lx, ly - 2, on='.dgS', r=2, prot=prot)
        if res:
            lamp_pts.append((res[0], res[1] + 1))

    # 6. Tidal Marsh Pools & Estuary: tall marsh reeds, shoals, buoys, coastal rocks & glints!
    enrich_water_zone(m, water_cls='p', seed=5411, lotus=False, shoals=True, glints=True,
                      reeds_cls='.d', prot=prot)
    enrich_water_zone(m, water_cls='wW', seed=5412, lotus=False, shoals=True, glints=True,
                      buoys=[('hb_buoy', 6, 32), ('hb_buoy2', 7, 56), ('hb_buoy', 6, 74), ('hb_buoy2', 5, 98)],
                      rocks=[('cs_wrock0', 4, 14), ('cs_wrock1', 8, 44), ('cs_wrock2', 5, 66), ('cs_wrock0', 8, 103)],
                      reeds_cls='', prot=prot)

    # 7. Coastal Sea-Lavender & Marsh Wildflower Drifts
    add_petals_and_flowers(m, [
        (38, 96, 6.0, 5.0, 0.25, 'seapink'),
        (26, 20, 6.0, 5.0, 0.25, 'seapink'),
        (54, 24, 6.0, 5.0, 0.22, 'wild'),
        (14, 60, 4.0, 3.0, 0.35, 'rose'),     # Brinewife's Rest cottage flowers
        (50, 72, 6.0, 5.0, 0.22, 'seapink'),
    ], seed=541)

    # 8. Misty Lantern Glows & Dramatic Coastal Marsh Sunbeams!
    add_warm_glows(m, lamp_pts + [(12, 58), (28, 84), (52, 36), (45, 101), (4, 83)])
    add_light_shafts(m, [
        (33, 96), (33, 62), (32, 36), (52, 34), (13, 58), (20, 96), (4, 82), (36, 14),
    ])


# ================================================================================================
# 4. CLEAN INTERCEPTION RUNNERS (INVOKES ORIGINAL BUILDERS IN-MEMORY WITHOUT TOUCHING THEIR FILES!)
# ================================================================================================

def run_saltmere_map(mid):
    import saltmere_rj as SM
    captured = {}
    orig_write = K.RMap.write
    orig_stamp = K.RMap.stamp
    orig_can_tree = K.RMap.can_tree
    orig_put = SM.put
    orig_block = SM.block
    orig_props = SM.props
    orig_boats = SM.boats
    orig_gardens = SM.gardens
    orig_street_trees = SM.street_trees

    def intercept_write(self, m_id, head, comment=''):
        captured['m'] = self
        captured['head'] = head
        return self.L

    # Scoped architectural, tree & plaza upgrades ONLY for 140 & 147 (146 stays 100% untouched!)
    if mid in (140, 147):
        # Replace broken off-by-1 `tr_teal` stamp transparently with symmetric `nt_teal_a` (ZERO rstamps.yaml edits!)
        def stamp_clean_teal(self, name, *args, **kw):
            if name == 'tr_teal':
                name = 'nt_teal_a'
            return orig_stamp(self, name, *args, **kw)

        def can_tree_clean_teal(self, name, *args, **kw):
            if name == 'tr_teal':
                name = 'nt_teal_a'
            return orig_can_tree(self, name, *args, **kw)

        def street_trees_clean(m, pts, kinds=('tr_oak2', 'tr_oak', 'nt_teal_a')):
            clean_k = tuple('nt_teal_a' if k == 'tr_teal' else k for k in kinds)
            return orig_street_trees(m, pts, kinds=clean_k)

        K.RMap.stamp = stamp_clean_teal
        K.RMap.can_tree = can_tree_clean_teal
        SM.street_trees = street_trees_clean

    if mid == 140:
        WARM_TERR = ['th_a', 'th_c', 'th_d', 'th_w', 'th_j', 'sp_bake']
        SLATE_TEAL = ['th_f', 'th_g', 'th_h', 'th_ad', 'th_k', 'sp_books', 'th_o']
        TIMBER_PLUM = ['th_m', 'th_r', 'th_s', 'th_t', 'th_u', 'th_v', 'th_ae', 'th_n', 'sp_cafe', 'sp_cost']

        def put_140(m, n, x, y, link=None, dname=None):
            # Pull vertically sheared edge watchtowers inward >= 1 tile off x=0 / x=87 (keeping West Gate sign [3,30] clear!)
            if n == 'gt_tower' and x == 0 and y == 25:
                return orig_put(m, n, 1, 24, link, dname)
            if n == 'gt_tower' and x == 0 and y == 35:
                return orig_put(m, n, 1, 35, link, dname)
            if n == 'gt_tower' and x == 85 and y in (38, 48):
                return orig_put(m, n, 84, y, link, dname)
            # Replace glitched upper-roof `th_af` at (24,17) with clean 3x8 `th_l` (exact same door [25,24]!)
            if n == 'th_af' and x == 24 and y == 17:
                return orig_put(m, 'th_l', 24, 17, link, dname)
            return orig_put(m, n, x, y, link, dname)

        def block_140(m, x0, x1, ytop, yb, pool, seed, alley_every=14, setback=0.15):
            # Break the monotonous edge-to-edge north townhouse wall (y=0..7) into varied height/color segments + recessed garden nooks!
            if ytop == 0 and yb == 7 and x0 == 0 and x1 == 39:
                orig_block(m, 0, 10, 0, 7, WARM_TERR + SLATE_TEAL, 111, alley_every=0, setback=0.45)
                m.rect(11, 1, 5, 7, 'f', only='T.c')
                orig_block(m, 16, 25, 0, 7, TIMBER_PLUM + SLATE_TEAL, 112, alley_every=0, setback=0.40)
                m.rect(26, 1, 4, 7, 'f', only='T.c')
                orig_block(m, 30, 39, 0, 7, WARM_TERR + TIMBER_PLUM, 113, alley_every=0, setback=0.40)
                return
            if ytop == 0 and yb == 7 and x0 == 52 and x1 == 87:
                orig_block(m, 52, 61, 0, 7, SLATE_TEAL + TIMBER_PLUM, 121, alley_every=0, setback=0.45)
                m.rect(62, 1, 5, 7, 'f', only='T.c')
                orig_block(m, 67, 74, 0, 7, WARM_TERR + SLATE_TEAL, 122, alley_every=0, setback=0.40)
                m.rect(75, 1, 5, 7, 'f', only='T.c')
                orig_block(m, 80, 87, 0, 7, TIMBER_PLUM + WARM_TERR, 123, alley_every=0, setback=0.45)
                return
            return orig_block(m, x0, x1, ytop, yb, pool, seed, alley_every=alley_every, setback=setback)

        def props_140(m, items, on='cf', r=2):
            # Break cloned market stalls, pull gl_tables off Pageant crimson carpet, give pf_well clearance, drop west salt cones!
            stall_map = {
                ('pf_stall4', 25, 29): ('fw_stall_e', 24, 28),
                ('pf_stall3', 25, 32): ('lm_stall_b', 25, 33),
                ('pf_stall1', 29, 37): ('lm_kiosk', 28, 37),
                ('pf_stall0', 25, 36): None,   # open SW plaza corner!
                ('pf_stall2', 33, 38): None,   # open south central gathering square!
                ('pf_stall1', 59, 29): ('fw_stall_i', 58, 28),
                ('pf_stall0', 59, 33): ('lm_stall_a', 59, 33),
                ('pf_stall4', 51, 38): ('lm_stall_c', 52, 38),
                ('pf_stall2', 55, 36): None,   # open SE plaza corner!
                ('pf_stall3', 59, 37): None,   # open east market walkway!
                # Pull stall/table off Pageant Hall red carpet (32..35, 25..28) & give well 1-tile clearance!
                ('gl_tables', 33, 28): ('gl_tables', 33, 31),
                ('pf_well', 30, 26): ('pf_well', 28, 27),
                # Remove bizarre west-border salt cones behind residential houses (0..3, 15..25)
                ('hb_salt0', 1, 15): None,
                ('hb_salt1', 0, 20): None,
                # Promenade stalls: genuine mix of awnings/kiosks/craft booth
                ('pf_stall1', 4, 51): ('lm_kiosk', 4, 51),
                ('pf_stall0', 30, 51): ('lm_stall_a', 30, 51),
                ('pf_stall2', 44, 51): ('lm_stall_c', 45, 51),
                ('pf_stall3', 68, 51): ('fw_stall_e', 68, 50),
            }
            new_items = []
            for it in items:
                if it in stall_map:
                    rep = stall_map[it]
                    if rep is not None:
                        new_items.append(rep)
                else:
                    new_items.append(it)
            return orig_props(m, tuple(new_items), on=on, r=r)

        def gardens_140(m, seed, trees=('tr_oak', 'tr_oak2', 'nt_teal_a', 'tr_pink', 'tr_oak')):
            clean_t = tuple('nt_teal_a' if t == 'tr_teal' else t for t in trees)
            return orig_gardens(m, seed, trees=clean_t)

        SM.put = put_140
        SM.block = block_140
        SM.props = props_140
        SM.gardens = gardens_140

    elif mid == 147:
        OLD_HIST_A = ['th_m', 'th_r', 'th_f', 'th_d', 'th_v', 'sp_cafe', 'th_a', 'th_h']
        OLD_HIST_B = ['th_ad', 'th_g', 'th_s', 'th_w', 'th_ae', 'sp_books', 'th_q', 'th_c']

        def block_147(m, x0, x1, ytop, yb, pool, seed, alley_every=14, setback=0.15):
            # Vary historic Mask Row facades (y=7..14) with height/color rhythm + 2 recessed garden/balcony nooks!
            if ytop == 7 and yb == 14 and x0 == 0 and x1 == 36:
                orig_block(m, 0, 13, 7, 14, OLD_HIST_A, 141, alley_every=0, setback=0.40)
                m.rect(14, 8, 5, 7, 'f', only='T.c')
                orig_block(m, 19, 36, 7, 14, OLD_HIST_B, 142, alley_every=10, setback=0.35)
                return
            if ytop == 7 and yb == 14 and x0 == 49 and x1 == 87:
                orig_block(m, 49, 62, 7, 14, OLD_HIST_B, 143, alley_every=0, setback=0.40)
                m.rect(63, 8, 5, 7, 'f', only='T.c')
                orig_block(m, 68, 87, 7, 14, OLD_HIST_A, 144, alley_every=11, setback=0.35)
                return
            return orig_block(m, x0, x1, ytop, yb, pool, seed, alley_every=alley_every, setback=setback)

        def gardens_147(m, seed, trees=('tr_oak', 'tr_oak2', 'nt_teal_a', 'tr_pink', 'tr_oak')):
            # Soften all hard rectangular garden lawn boxes into organic chamfered courtyard gardens! (Zero tr_teal!)
            clean_t = tuple('nt_teal_a' if t == 'tr_teal' else t for t in trees)
            res = orig_gardens(m, seed, trees=clean_t)
            for _ in range(2):
                dot = (m.cls == '.')
                to_cobble = []
                for y in range(1, m.H - 1):
                    for x in range(1, m.W - 1):
                        if not dot[y, x] or m.taken[y, x] or m.cliff[y, x]:
                            continue
                        n4 = int(dot[y - 1, x]) + int(dot[y + 1, x]) + int(dot[y, x - 1]) + int(dot[y, x + 1])
                        if n4 <= 2 or (n4 == 3 and vnoise(x, y, 1477, 2.8) > 0.68):
                            to_cobble.append((x, y))
                for x, y in to_cobble:
                    m.cls[y, x] = 'c'
            return res

        def boats_147(m, items):
            # Replace cloned rowboats & cloned ak_boulder sea-rock with varied moored vessels + crisp chalk headland rock!
            varied = (
                ('ck_rock_big', 3, 66),
                ('fw_boat', 11, 63),
                ('hb_boat2', 59, 63),
                ('hb_wheelhouse', 76, 63),
                ('fw_boat', 71, 65),
                ('fw_boat', 15, 2),
                ('hb_boat4', 66, 2),
            )
            return orig_boats(m, varied)

        SM.block = block_147
        SM.gardens = gardens_147
        SM.boats = boats_147

    K.RMap.write = intercept_write
    try:
        if mid == 140:
            SM.build_140(None)
        elif mid == 146:
            SM.build_146(None)
        elif mid == 147:
            SM.build_147(None)
    finally:
        K.RMap.write = orig_write
        K.RMap.stamp = orig_stamp
        K.RMap.can_tree = orig_can_tree
        SM.put = orig_put
        SM.block = orig_block
        SM.props = orig_props
        SM.boats = orig_boats
        SM.gardens = orig_gardens
        SM.street_trees = orig_street_trees

    m = captured['m']
    if mid == 140:
        craft_140_saltmere(m)
        save_wave12_map(m, 140, '# Saltmere - The Upper Town (140). WRITTEN BY layouts/wave12_saltmere_routes_craft.py (Wave 12 Rejuv V14 Craft).\n')
    elif mid == 146:
        craft_146_harbour(m)
        save_wave12_map(m, 146, '# Saltmere - The Harbour (146). WRITTEN BY layouts/wave12_saltmere_routes_craft.py (Wave 12 Rejuv V14 Craft).\n')
    elif mid == 147:
        craft_147_oldtown(m)
        save_wave12_map(m, 147, '# Saltmere - The Old Town (147). WRITTEN BY layouts/wave12_saltmere_routes_craft.py (Wave 12 Rejuv V14 Craft).\n')


def run_orchard_522():
    import orchard as OR
    captured = {}
    orig_write = K.RMap.write
    orig_route_init = RK.Route.__init__

    def intercept_init(self, *args, **kw):
        orig_route_init(self, *args, **kw)
        captured['r'] = self

    def intercept_write(self, m_id, head, comment=''):
        captured['m'] = self
        captured['head'] = head
        return self.L

    RK.Route.__init__ = intercept_init
    K.RMap.write = intercept_write
    try:
        OR.build()
    finally:
        RK.Route.__init__ = orig_route_init
        K.RMap.write = orig_write

    m = captured['m']
    r = captured['r']
    craft_522_glassed_orchard(m, r)
    save_wave12_map(m, 522, '# The Glassed Orchard (522). WRITTEN BY layouts/wave12_saltmere_routes_craft.py (Wave 12 Rejuv V14 Craft).\n')


def run_route_map(mid):
    import routes_early as RE
    import routes_craft as RCRAFT
    captured = {}
    orig_rwrite = RK.Route.write
    orig_finish_plan = RK.Route.finish_plan
    orig_near = RK.Route.near
    orig_orchard = RE.orchard_rows
    orig_stamp = K.RMap.stamp
    orig_water_stamp = CK.water_stamp
    orig_smooth_sea = CK.smooth_sea
    orig_fringe = CK.fringe
    orig_woods = CK.woods
    orig_ledge = CK.ledge

    def intercept_rwrite(self, head, fname, comment, preview=None):
        m = self.m
        connections = head.pop('connections', [])
        head['connections'] = connections
        head['_file'] = fname
        self.sealed = m.seal_against(connections, keep=getattr(self, '_keep', []), spans=self.exits)
        captured['r'] = self
        captured['m'] = m
        captured['head'] = head
        return m.L

    RK.Route.write = intercept_rwrite
    if mid == 521:
        RE.orchard_rows = organic_orchard_rows
    elif mid == 527:
        # 527 Lacecliff Walk Pass-2 hooks:
        # - Ground cliffs at (76..81, 41..45) cleanly onto sand meeting Tide-rock neck (y=46) (zero cliffs floating over cyan water!)
        # - Smooth jagged Cove A/B shoreline teeth
        # - Break 60-tile ruler-straight West Down wall into organic staggered chalk ledges sealed with boulders
        # - Replace flat concrete pf_lacearch/pf_chalkarch with Gen 5 wb_gate & Chalk Cairn/Column Gateway
        # - Keep cove props off cliff tops/faces (eliminates (40,42) cliff-top rope & (26..29,43) floating plank puddle!)
        # - Replace 4 cloned sea rocks + flat pf_seastack cone with varied rock species/depths & pull boat off jetty!
        def finish_plan_527(self, border=3):
            m_ = self.m
            # 1. Bring cliff lip at x=76..80 cleanly down to y=43 (matching x=81) so cliff base (y=45) meets Tide-rock sand neck (y=46)!
            m_.ht[42:44, 76:81] = 1
            m_.cls[43, 76:81] = '.'
            m_.cls[44:47, 76:82] = 's'
            m_.cls[47, 75:77] = 's'
            m_.cls[47:, 77:81] = 'w'
            # 2. Smooth 1-tile jagged sand/water shoreline teeth in Cove A (20..44) & Cove B (81..102)
            for _ in range(2):
                prev = m_.cls.copy()
                for x0_, x1_ in ((20, 44), (81, 102)):
                    for y_ in range(45, m_.H - 2):
                        for x_ in range(x0_, x1_ + 1):
                            if m_.ht[y_, x_] > 0 or prev[y_, x_] not in ('s', 'w'):
                                continue
                            if y_ == 46 and 74 <= x_ <= 83:
                                continue
                            ns = sum(1 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if prev[y_ + dy, x_ + dx] == 's')
                            nw = sum(1 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if prev[y_ + dy, x_ + dx] in ('w', 'W'))
                            if prev[y_, x_] == 's' and nw >= 3:
                                m_.cls[y_, x_] = 'w'
                            elif prev[y_, x_] == 'w' and ns >= 3:
                                m_.cls[y_, x_] = 's'
            return orig_finish_plan(self, border=border)

        def ledge_527(r, x0, x1, y, chalk=False, face=None):
            m_ = r.m
            if chalk and x0 == 6 and x1 == 40 and y == 15:
                orig_ledge(r, 6, 15, 14, chalk=True, face=face)
                orig_ledge(r, 18, 28, 15, chalk=True, face=face)
                orig_ledge(r, 31, 40, 14, chalk=True, face=face)
                for bx in (16, 29):
                    m_.cls[14:16, bx:bx + 2] = '.'
                    m_.taken[14:16, bx:bx + 2] = False
                    orig_stamp(m_, 'ck_boulder', bx, 14, mark='B')
                return None
            if chalk and x0 == 48 and x1 == 62 and y == 14:
                orig_ledge(r, 48, 54, 14, chalk=True, face=face)
                orig_ledge(r, 57, 62, 15, chalk=True, face=face)
                m_.cls[14:16, 55:57] = '.'
                m_.taken[14:16, 55:57] = False
                orig_stamp(m_, 'ck_boulder', 55, 14, mark='B')
                return None
            return orig_ledge(r, x0, x1, y, chalk=chalk, face=face)

        def woods_527(r, palettes, *args, **kw):
            m_ = r.m
            # Plant dense interlocking coastal pine/oak groves into the giant bare western meadow (x6..60, y16..39)!
            for cx, cy, rx, ry in (
                (14, 18, 3.6, 1.8), (30, 18, 3.8, 1.8), (50, 18, 4.0, 2.0),
                (16, 31, 4.2, 2.8), (44, 31, 4.2, 2.8), (64, 18, 3.6, 2.0), (88, 22, 4.0, 2.4),
            ):
                for y in range(max(17, int(cy - ry - 1)), min(39, int(cy + ry + 2))):
                    for x in range(max(6, int(cx - rx - 1)), min(95, int(cx + rx + 2))):
                        if m_.cls[y, x] in '.t' and not m_.taken[y, x] and not m_.cliff[y, x] and not r.road_mask[max(0, y - 1):y + 2, max(0, x - 1):x + 2].any():
                            if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 + 0.3 * (vnoise(x, y, 5278, 3.0) - 0.5) <= 1.0:
                                m_.cls[y, x] = 'T'
            return orig_woods(r, palettes, *args, **kw)

        def stamp_527(self, name, x, y, *args, **kw):
            if name == 'pf_lacearch' and x == 101 and y == 25:
                # Replace floating concrete dome Arch A with authentic Gen 5 floral archway wb_gate (5x5, 3-tile road opening x103..105!)
                return orig_stamp(self, 'wb_gate', 102, 25, mark='B')
            if name == 'pf_lacearch' and x == 75 and y == 26:
                # Replace MS-Paint concrete Arch B with sculpted Gen 5 Chalk Cairn & Column Gateway flanking road x77..79!
                for rx, ry, rnm in (
                    (76, 27, 'nr_col'), (80, 27, 'nr_col'),
                    (76, 29, 'nr_col'), (80, 29, 'nr_col'),
                    (75, 29, 'nr_wall_w'), (81, 29, 'nr_wall_e'),
                    (73, 27, 'ck_rock_big'), (82, 27, 'ck_rock_big'),
                ):
                    st_ = STAMPS[rnm]
                    if self.inb(rx, ry) and self.free(rx, ry, st_['w'], st_['h'], on='.tuT'):
                        orig_stamp(self, rnm, rx, ry, mark='B')
                return None
            if name == 'pf_lacearch' and x == 41 and y == 11:
                # Replace intact cloned 3rd dolmen with solid collapsed masonry side walls preserving Rock Smash gate (43..45, 14)!
                for rx, ry, rnm in (
                    (41, 13, 'ck_boulder'), (41, 14, 'nr_col'), (42, 14, 'ck_boulder'),
                    (46, 13, 'ck_boulder'), (46, 14, 'nr_col'), (47, 13, 'ck_boulder'),
                ):
                    if self.inb(rx, ry) and self.free(rx, ry, STAMPS[rnm]['w'], STAMPS[rnm]['h'], on='.tuT'):
                        orig_stamp(self, rnm, rx, ry, mark='B')
                for bx in (41, 42, 46, 47):
                    for by in (14, 15):
                        if self.cls[by, bx] in '.tu' and not self.taken[by, bx]:
                            orig_stamp(self, 'nr_wall_m', bx, by, mark='B')
                return None
            return orig_stamp(self, name, x, y, *args, **kw)

        def near_527(self, name, x, y, on='.', r=4):
            # Remap cliff-colliding cove props cleanly onto flat open Cove A beach sand & forbid cliff tiles on on='s'!
            if name == 'hb_rope' and x == 40 and y == 42:
                x, y = 39, 46
            elif name == 'hb_plank' and x == 26 and y == 43:
                x, y = 26, 46
            if on == 's':
                m_ = self.m
                st_ = STAMPS[name]
                ww, hh = st_['w'], st_['h']
                for rad in range(0, r + 4):
                    for dy in range(-rad, rad + 1):
                        for dx in range(-rad, rad + 1):
                            if abs(dx) != rad and abs(dy) != rad:
                                continue
                            xx, yy = x + dx, y + dy
                            if not (m_.inb(xx, yy) and m_.inb(xx + ww - 1, yy + hh - 1)):
                                continue
                            if m_.cliff[yy:yy + hh, xx:xx + ww].any():
                                continue
                            if m_.free(xx, yy, ww, hh, on=on):
                                orig_stamp(m_, name, xx, yy, mark='B')
                                return (xx, yy)
                return None
            return orig_near(self, name, x, y, on=on, r=r)

        def water_stamp_527(r, n, x, y):
            # Replace 4 cloned sea rocks + flat concrete pf_seastack cone with varied rock species/sizes at irregular depths & clear boat from jetty!
            remap = {
                ('pf_seaarch', 11, 52): ('dk_rock_big', 10, 54),
                ('pf_seastack', 50, 53): ('ak_rock2', 49, 57),
                ('pf_seastack2', 76, 53): ('ck_rock_big', 74, 53),
                ('pf_seaarch', 100, 55): ('dk_boulder', 97, 59),
                ('pf_seastack2', 131, 54): ('ck_rock_big', 109, 54),  # Natural chalk Wingull sea stack below Birder (108, 7)!
                ('pf_seastack', 22, 57): ('ck_boulder', 22, 58),
                ('pf_seastack2', 64, 58): None,
                ('hb_boat3', 34, 50): ('fw_boat', 37, 52),            # Cleanly separated >= 4 tiles from Cove A shore/jetty!
            }
            key = (n, x, y)
            if key in remap:
                rep = remap[key]
                if rep is None:
                    return True
                rn, rx, ry = rep
            else:
                rn, rx, ry = n, x, y
            # Clear purely decorative water glints on L2 inside the water footprint so rocks & boat always place cleanly!
            m_ = r.m
            st_ = STAMPS[rn]
            ww, hh = st_['w'], st_['h']
            if all(m_.inb(rx + i, ry + j) and m_.cls[ry + j, rx + i] in 'wW' for i in range(ww) for j in range(hh)):
                m_.L[2, ry:ry + hh, rx:rx + ww] = 0
            return orig_water_stamp(r, rn, rx, ry)

        def smooth_sea_527(m, passes=3):
            # Smooth out stair-stepping deep-water band ('W') into long, natural coastal depth curves!
            H_, W_ = m.H, m.W
            sea = np.isin(m.cls, ['w', 'W'])
            for x in range(W_):
                ys = np.where(sea[:, x])[0]
                if not len(ys):
                    continue
                sea0 = int(ys[0])
                deep_y = int(round(max(sea0 + 5.5, 54.5 + 2.4 * math.sin(x / 18.0) + 1.4 * math.cos(x / 11.0))))
                deep_y = min(H_ - 2, max(sea0 + 4, deep_y))
                for y in ys:
                    m.cls[y, x] = 'W' if y >= deep_y else 'w'
            return orig_smooth_sea(m, passes=5)

        RK.Route.finish_plan = finish_plan_527
        RK.Route.near = near_527
        CK.ledge = ledge_527
        CK.woods = woods_527
        K.RMap.stamp = stamp_527
        CK.water_stamp = water_stamp_527
        CK.smooth_sea = smooth_sea_527

    elif mid == 540:
        # 540 Thistledown Lea Pass-2 hooks:
        # - Square off Manor h2 plinth & add matching left terrace stair (61..62, 12..14) so Locked door @ (61,9) is 100% reachable!
        # - Level Ha-ha back garden (79..88, 0..7) to ht=0 & square east manor lawn (79..84, 8..14) so ZERO diagonal cliff stubs form and Greavard is 100% reachable!
        # - Build interlocking estate woodland groves & eliminate scattered confetti trees!
        def finish_plan_540(self, border=3):
            m_ = self.m
            # 1. Clean rectangular Manor h2 front lip at y=12 across x=60..69 + matching 2-wide left terrace stair (61..62, 12..14)!
            m_.ht[10:12, 59] = 2
            m_.ht[10:13, 60:63] = 2
            CK.stair(self, 61, 12, w=2, h=2)
            # 2. Level Ha-ha back garden (78..88, 0..7) to ht=0 & square east manor rose lawn (78..84, 8..14) -> ZERO orphaned cliff stubs!
            m_.ht[4:8, 77] = np.minimum(m_.ht[4:8, 77], 1)
            m_.ht[0:8, 78:89] = 0
            m_.ht[8:15, 78:85] = 1
            m_.ht[8:17, 85:89] = 0
            # Open Ha-ha back garden clearing & dirt spur connecting Ha-ha ditch (86..87, 3..14) directly to Greavard (80,4)!
            for yy in range(3, 8):
                for xx in range(79, 87):
                    if m_.cls[yy, xx] == 'T':
                        m_.cls[yy, xx] = '.'
            for yy in (4, 5):
                for xx in range(80, 87):
                    m_.cls[yy, xx] = 'd'
                    self.road_mask[yy, xx] = True
            return orig_finish_plan(self, border=border)

        def woods_540(r, palettes, *args, **kw):
            m_ = r.m
            for cx, cy, rx, ry in (
                (15, 29, 4.0, 2.6), (55, 27, 4.0, 2.6), (98, 22, 4.2, 2.8),
                (50, 45, 4.5, 2.6), (68, 45, 4.2, 2.6), (115, 43, 4.4, 2.8),
            ):
                for y in range(max(4, int(cy - ry - 1)), min(49, int(cy + ry + 2))):
                    for x in range(max(4, int(cx - rx - 1)), min(124, int(cx + rx + 2))):
                        if y < 9 and x >= 78:
                            continue
                        if m_.ht[y, x] == 0 and m_.cls[y, x] in '.t' and not m_.taken[y, x] and not m_.cliff[y, x]:
                            if not r.road_mask[max(0, y - 1):y + 2, max(0, x - 1):x + 2].any():
                                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 + 0.3 * (vnoise(x, y, 5408, 3.0) - 0.5) <= 1.0:
                                    m_.cls[y, x] = 'T'
            return orig_woods(r, palettes, *args, **kw)

        def fringe_540(r, kinds, n, box=None, on='.', seed=0, near_forest=2, zone_scale=9.0):
            if near_forest == 0:
                return 0
            return orig_fringe(r, kinds, min(n, 70), box=box, on=on, seed=seed, near_forest=2, zone_scale=zone_scale)

        RK.Route.finish_plan = finish_plan_540
        CK.woods = woods_540
        CK.fringe = fringe_540

    try:
        if mid == 521:
            RE.build_521()
        else:
            RCRAFT.BUILD[mid]()
    finally:
        RK.Route.write = orig_rwrite
        RK.Route.finish_plan = orig_finish_plan
        RK.Route.near = orig_near
        RE.orchard_rows = orig_orchard
        K.RMap.stamp = orig_stamp
        CK.water_stamp = orig_water_stamp
        CK.smooth_sea = orig_smooth_sea
        CK.fringe = orig_fringe
        CK.woods = orig_woods
        CK.ledge = orig_ledge

    m = captured['m']
    r = captured['r']
    if mid == 521:
        craft_521_windfall_row(m, r)
        save_wave12_map(m, 521, '# Windfall Row (521). WRITTEN BY layouts/wave12_saltmere_routes_craft.py (Wave 12 Rejuv V14 Craft).\n')
    elif mid == 520:
        craft_520_ferrymens_mile(m, r)
        save_wave12_map(m, 520, "# The Ferrymen's Mile (520). WRITTEN BY layouts/wave12_saltmere_routes_craft.py (Wave 12 Rejuv V14 Craft).\n")
    elif mid == 527:
        craft_527_lacecliff_walk(m, r)
        save_wave12_map(m, 527, '# Lacecliff Walk (527). WRITTEN BY layouts/wave12_saltmere_routes_craft.py (Wave 12 Rejuv V14 Craft).\n')
    elif mid == 528:
        craft_528_marram_down(m, r)
        save_wave12_map(m, 528, '# Marram Down (528). WRITTEN BY layouts/wave12_saltmere_routes_craft.py (Wave 12 Rejuv V14 Craft).\n')
    elif mid == 540:
        craft_540_thistledown_lea(m, r)
        save_wave12_map(m, 540, '# Thistledown Lea (540). WRITTEN BY layouts/wave12_saltmere_routes_craft.py (Wave 12 Rejuv V14 Craft).\n')
    elif mid == 541:
        craft_541_grey_saltings(m, r)
        save_wave12_map(m, 541, '# The Grey Saltings (541). WRITTEN BY layouts/wave12_saltmere_routes_craft.py (Wave 12 Rejuv V14 Craft).\n')


ALL_WAVE12 = [140, 146, 147, 520, 521, 522, 527, 528, 540, 541]


def main():
    args = [int(a) for a in sys.argv[1:] if a.isdigit()]
    targets = args or ALL_WAVE12
    for mid in targets:
        print(f'=== Wave 12 Crafting Map {mid} ===')
        if mid in (140, 146, 147):
            run_saltmere_map(mid)
        elif mid == 522:
            run_orchard_522()
        else:
            run_route_map(mid)
    print(f'Done crafting {len(targets)} Wave 12 maps!')


if __name__ == '__main__':
    main()
