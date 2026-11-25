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
from terrain import vnoise, NB2AUTO

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


def save_wave12_map(m, mid, header_comment, tone_override=None):
    """Resolve virtual autotiles, run passguard + exact border seam guard, write .npy & exact HEAD YAML."""
    Lr = RC.resolve(m.L, m.tid).astype(np.int32)
    Lr = restore_exact_border_seams(Lr, mid, m.tid)

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
    """140 Saltmere — Core City: dressed stone Market Square & Promenade mosaic inlays, Pageant Hall
    crimson carpet runner, striped awnings, clustered coastal plane-tree groves, textured mineral
    salt-works with raker carts & bollards, bobbing lake buoys, warm lantern glows & coastal sunbeams."""
    prot_exact, prot = build_prot_mask(m, 140)
    paves = [P1('lm_pave%d' % i) for i in range(4)]
    plazas = [P1('lm_plaza0'), P1('lm_plaza1'), P1('lm_pave1'), P1('lm_pave2')]
    warm_cream = [P1('lm_plaza0'), P1('lm_plaza1')]
    pave0 = P1('lm_pave0')
    pave3 = P1('lm_pave3')

    # 1. Grand Market Square (22..63, 25..41): crisp dressed limestone border + warm cream plaza + Fountain medallion!
    paint_plaza_inlay(m, 22, 25, 63, 41, pave0, paves, on_cls='fc', trim_tile=pave3, inset_border=True, seed=1)
    # Inner warm cream Market Plaza ring around the Fountain (33..52, 27..39)
    paint_plaza_inlay(m, 33, 27, 52, 39, pave0, warm_cream, on_cls='fc', seed=2)
    # Central inlaid ashlar frame directly under Fountain dais (38..47, 29..36)
    paint_plaza_inlay(m, 38, 29, 47, 36, pave3, paves, on_cls='fc', seed=3)

    # 2. Pageant Hall Crimson Carpet Welcome & Fountain Walk Ceremonial Runner (43..46, 42..49) — ZERO cutout holes!
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

    # 5. Striped Awnings over Market Stalls & Shopfronts (Layer 2 overhead)
    add_awnings(m, [
        (25, 28), (29, 36), (55, 35), (59, 28), (51, 37), (33, 37),
        (51, 24), (59, 24), (24, 24), (4, 50), (30, 50), (44, 50), (68, 50), (76, 49),
    ])

    # 6. Sculpted Topiaries, Planters, Wrought-Iron Lanterns & Market Life
    lamp_pts = collect_lamp_positions(m)
    for nm, x, y in (
        ('lm_topiary', 38, 28), ('lm_topiary', 47, 28), ('lm_topiary', 38, 35), ('lm_topiary', 47, 35),
        ('lm_topiary', 41, 43), ('lm_topiary', 48, 43), ('lm_topiary', 41, 47), ('lm_topiary', 48, 47),
        ('pf_planter0', 31, 26), ('pf_planter1', 36, 26), ('pf_planter2', 52, 26), ('pf_planter3', 57, 26),
        ('pf_stonebench', 35, 30), ('pf_stonebench', 49, 30), ('pf_stonebench', 18, 55), ('pf_stonebench', 57, 55),
        ('mn_statue', 42, 41), ('mn_statue', 47, 41),
        ('cv_cart_salt', 21, 66), ('cv_cart_salt', 34, 65), ('cv_cart_salt', 47, 66), ('cv_cart_salt', 77, 66),
        ('hb_salt0', 30, 65), ('hb_salt1', 42, 65), ('hb_salt2', 71, 66),
    ):
        on_c = 'S' if nm in ('cv_cart_salt', 'hb_salt0', 'hb_salt1', 'hb_salt2') else 'fc'
        put_near_now(m, nm, x, y, on=on_c, r=2, prot=prot)

    for lx, ly in ((39, 31), (46, 31), (42, 45), (47, 45), (10, 62), (14, 66), (57, 62), (61, 66),
                   (32, 66), (75, 66), (17, 53), (33, 53), (53, 53), (75, 53), (43, 19), (48, 19)):
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
    ], seed=140)

    # 8. Transform Salt Lake & Brine Pans (textured mineral crust + damp tidal edges + lake buoys!)
    craft_salt_flats(m, seed=140, pink_keep=0.35, grey_salt=False, prot=prot)
    enrich_water_zone(m, water_cls='wW', seed=140, lotus=False, shoals=True, glints=True,
                      buoys=[('hb_buoy', 6, 63), ('hb_buoy2', 15, 64), ('hb_buoy', 54, 65), ('hb_buoy2', 63, 66)],
                      rocks=[('cs_wrock0', 4, 67), ('cs_wrock1', 64, 63), ('cs_wrock2', 82, 61)],
                      reeds_cls='', prot=prot, glint_density=0.10)

    # 9. Festive Garlands, Warm Golden Lantern Glows & Coastal Sunbeams
    add_festoon_strings(m, [
        (40, 49, 44, 0), (40, 49, 48, 2), (9, 14, 62, 1), (56, 61, 62, 0),
        (43, 48, 17, 1), (31, 40, 29, 2), (46, 55, 29, 0),
    ], kind='garl')
    add_warm_glows(m, lamp_pts + [
        (42, 31), (33, 24), (54, 24), (45, 7), (85, 44), (3, 32), (12, 58), (58, 58),
    ])
    add_light_shafts(m, [
        (36, 28), (48, 30), (44, 44), (24, 52), (62, 52), (11, 63), (58, 63), (78, 45),
    ])


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
    """147 Saltmere — Old Town: Pell Playhouse crimson theatrical red carpet down the Grand Stair,
    5x5 golden sunburst medallion in Theatre Square, sculpted statues & topiaries, rose petal drifts,
    terrace awnings, festival pennant garlands, glowing theatre lamps & golden sunset sunbeams."""
    prot_exact, prot = build_prot_mask(m, 147)
    paves = [P1('lm_pave%d' % i) for i in range(4)]
    plazas = [P1('lm_plaza0'), P1('lm_plaza1'), P1('lm_pave1'), P1('lm_pave2')]
    warm_cream = [P1('lm_plaza0'), P1('lm_plaza1')]
    pave0 = P1('lm_pave0')
    pave3 = P1('lm_pave3')

    # 1. Players' Causeway (40..45, 1..6) & Mask Row (y=15..17): organically weathered dressed stone
    paint_plaza_inlay(m, 40, 1, 45, 6, paves, plazas, on_cls='fc', seed=21)
    paint_plaza_inlay(m, 2, 15, 85, 17, paves, paves, on_cls='cf', seed=22)

    # 2. Pell Playhouse Forecourt (18..35, 34..37) + Curtain Lane (y=36..37) + GRAND CRIMSON CARPET!
    paint_plaza_inlay(m, 18, 34, 35, 37, pave3, warm_cream, on_cls='fc', seed=23)
    paint_plaza_inlay(m, 2, 36, 85, 37, paves, paves, on_cls='cf', seed=24)
    # Seamless Royal Crimson Velvet Carpet from Pell Playhouse Gym door (zero NPC cutout holes!)
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

    # 4. Seafront Promenade (y=57..59): weathered cream & ashlar seawall walk (asymmetric vnoise!)
    paint_plaza_inlay(m, 1, 57, 86, 59, paves, plazas, on_cls='f', seed=27)
    for x in range(2, 86):
        if m.cls[59, x] == 'f' and not m.cliff[59, x] and vnoise(x, 59, 1473, 4.2) > 0.46:
            m.L[0, 59, x] = paves[(x * 5 + 2) % 4]

    # 5. Theatre Awnings, Sculpted Statues, Topiaries, Planters & Wrought-Iron Lanterns
    add_awnings(m, [
        (18, 46), (27, 48), (33, 48), (43, 45), (52, 48), (18, 56), (78, 56),
        (36, 35), (62, 35), (20, 33), (31, 33),
    ])
    lamp_pts = collect_lamp_positions(m)
    for nm, x, y in (
        ('mn_statue', 22, 34), ('mn_statue', 31, 34), ('mn_statue', 23, 41), ('mn_statue', 30, 41),
        ('lm_topiary', 20, 35), ('lm_topiary', 33, 35), ('lm_topiary', 55, 35), ('lm_topiary', 61, 35),
        ('lm_topiary', 16, 42), ('lm_topiary', 40, 42), ('lm_topiary', 20, 49), ('lm_topiary', 39, 49),
        ('pf_planter0', 38, 16), ('pf_planter1', 47, 16), ('pf_planter2', 12, 58), ('pf_planter3', 50, 58),
        ('pf_stonebench', 26, 44), ('pf_stonebench', 37, 45), ('pf_stonebench', 20, 58), ('pf_stonebench', 48, 58),
        ('fw_brazier', 23, 36), ('fw_brazier', 30, 36),
    ):
        res = put_near_now(m, nm, x, y, on='fc', r=2, prot=prot)
        if res and nm == 'fw_brazier':
            lamp_pts.append((res[0], res[1]))

    for lx, ly in ((24, 35), (29, 35), (21, 44), (39, 44), (31, 48), (48, 45), (41, 12), (45, 12),
                   (18, 17), (64, 17), (24, 59), (40, 59), (60, 59), (74, 59)):
        res = put_near_now(m, 'pf_lantern', lx, ly - 2, on='fc', r=1, prot=prot, allow_l2_overlap=False)
        if res:
            lamp_pts.append((res[0], res[1] + 1))

    # 6. Theatrical Blossom Groves & Rose Petal Drifts across Theatre Square & Seafront
    add_petals_and_flowers(m, [
        (27, 36, 7.0, 2.2, 0.28, 'petal'),
        (32, 45, 14.0, 4.5, 0.16, 'petal'),
        (42, 16, 10.0, 2.0, 0.12, 'petal'),
        (36, 58, 22.0, 1.8, 0.10, 'petal'),
    ], seed=147)

    # 7. Northern Channel & Southern Sea detailing (asymmetric buoys/rocks/glints keep mirror < 11%!)
    enrich_water_zone(m, water_cls='wW', seed=147, lotus=False, shoals=True, glints=True,
                      buoys=[('hb_buoy', 15, 65), ('hb_buoy2', 39, 64), ('hb_buoy', 68, 66),
                             ('hb_buoy2', 23, 3), ('hb_buoy', 61, 3)],
                      rocks=[('cs_wrock0', 12, 67), ('cs_wrock1', 49, 68), ('cs_wrock2', 76, 67),
                             ('cs_wrock0', 17, 2), ('cs_wrock1', 66, 2)],
                      reeds_cls='', prot=prot, glint_density=0.22)
    rng_w = random.Random(14799)
    GL = [P1('hb_glint%d' % i) for i in range(4)]
    for y in list(range(0, 7)) + list(range(61, m.H)):
        for x in range(1, m.W - 1):
            if m.cls[y, x] in 'wW' and m.L[1, y, x] == 0 and m.L[2, y, x] == 0:
                bias = 0.42 if x > 44 else 0.12
                if rng_w.random() < bias:
                    m.L[2, y, x] = rng_w.choice(GL)

    # 8. Festival Pennant Garlands, Theatrical Warm Glows & Golden Sunset Sunbeams
    add_festoon_strings(m, [
        (20, 34, 35, 0), (19, 36, 42, 2), (22, 40, 47, 1), (40, 45, 3, 0),
        (54, 65, 36, 1), (10, 24, 58, 2), (48, 64, 58, 0),
    ], kind='garl')
    add_warm_glows(m, lamp_pts + [
        (26, 33), (27, 36), (58, 34), (42, 11), (32, 45), (22, 45), (42, 45), (30, 58), (64, 58),
    ])
    add_light_shafts(m, [
        (26, 33), (33, 43), (21, 44), (58, 34), (42, 13), (18, 57), (54, 57),
    ])


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
        return (x <= 3 and y >= 29) or (x == 4 and y >= 31)

    # 1. Silky Rounded Cerulean & Periwinkle Glacial Turf on frosted glass ground (zero hard seams!)
    base_ok = np.isin(m.cls, ['.', 't', 'T']) & ~m.cliff & ~r.road_mask
    for y in range(H):
        for x in range(W):
            if in_living(x, y) or (27 <= x <= 34 and y <= 10) or (35 <= x <= 41 and y <= 5):
                base_ok[y, x] = False

    cer_raw = np.zeros((H, W), dtype=bool)
    peri_raw = np.zeros((H, W), dtype=bool)
    for y in range(H):
        for x in range(W):
            if not base_ok[y, x]:
                continue
            d_pond = ((x - 9) / 8.5) ** 2 + ((y - 23) / 7.5) ** 2
            d_nw = ((x - 10) / 7.5) ** 2 + ((y - 9) / 6.5) ** 2
            d_se = ((x - 32) / 8.0) ** 2 + ((y - 28) / 6.0) ** 2
            nz = vnoise(x, y, 52211, 4.0)
            if d_pond < 1.15 + 0.30 * (nz - 0.5) or d_nw < 1.05 + 0.25 * (nz - 0.5) or d_se < 0.95 + 0.25 * (nz - 0.5):
                cer_raw[y, x] = True
            else:
                d_mid = ((x - 22) / 9.5) ** 2 + ((y - 16) / 7.5) ** 2
                d_up = ((x - 33) / 8.5) ** 2 + ((y - 10) / 5.5) ** 2
                if d_mid < 1.05 + 0.30 * (nz - 0.5) or d_up < 1.0 + 0.25 * (nz - 0.5):
                    peri_raw[y, x] = True

    cer_mask = smooth_bool_mask(cer_raw, base_ok, passes=3)
    peri_mask = smooth_bool_mask(peri_raw & ~cer_mask, base_ok & ~cer_mask, passes=3)
    paint_bordered_turf(m, cer_mask, CERULEAN_3X3, CERULEAN_IN, center_alts=(9521, 9521, 10395))
    paint_bordered_turf(m, peri_mask, PERI_3X3, PERI_IN, center_alts=(9905, 9905, 10395))

    # 2. Dense Overlapping Kristiline Winter Spruces & Teal Pines packing ALL perimeter borders!
    for hx, hy in ((1, 3), (12, 1), (39, 10), (39, 29), (14, 34), (24, 34), (34, 34)):
        put_stamp_now(m, 'pf_g_tree2_ice', hx, hy, on='T.', prot=prot, check_level=False, allow_l2_overlap=True)
    infill_forest_now(m, seed=522, prot=prot, snow=True)

    # Extra perimeter Kristiline teal pine & spruce infill along south & east rims (kills polka-dot snow gaps!)
    kf_kinds = [KF_TEAL_PINE_A, KF_TEAL_PINE_B, KF_SPRUCE_A, KF_SPRUCE_B]
    for tx in range(6, 41, 2):
        for ty in (34, 35, 36):
            top_r, bot_r = kf_kinds[(tx + ty) % len(kf_kinds)]
            put_sprite_now(m, tx, ty - len(top_r), top_r, bot_r, on='T.', prot=prot, check_level=False)
    for ty in range(7, 36, 2):
        for tx in (39, 40, 41):
            top_r, bot_r = kf_kinds[(tx + ty) % len(kf_kinds)]
            put_sprite_now(m, tx, ty - len(top_r), top_r, bot_r, on='T.', prot=prot, check_level=False)

    # 3. Companion Kristiline frosted spruces & shrubs enriching open frosted orchard pockets
    for cx, cy in ((7, 4), (16, 4), (24, 4), (26, 28), (37, 17), (15, 22), (8, 30)):
        if prot[cy, cx]:
            continue
        top_r, bot_r = rng.choice(kf_kinds)
        put_sprite_now(m, cx, cy, top_r, bot_r, on='.T', prot=prot, check_level=True)

    # 4. Luminous Crystal Mineral Formations (`KF_CRYS_*`), Frosted Shrubs & Boulders
    for sx, sy, sp in (
        (6, 20, KF_CRYS_STAR), (13, 24, KF_CRYS_BLADES), (16, 26, KF_CRYS_MONO),
        (25, 19, KF_CRYS_STAR), (32, 22, KF_CRYS_BLADES), (27, 10, KF_SHRUB_A),
        (36, 11, KF_CRYS_MONO), (12, 15, KF_SHRUB_B), (7, 13, KF_BOULDER),
        (22, 29, KF_CRYS_STAR), (39, 21, KF_CRYS_BLADES), (16, 12, KF_SHRUB_A),
    ):
        put_sprite_now(m, sx, sy, sp[0], sp[1], on='.t', prot=prot, check_level=True)

    # 5. Kristiline Frosted Lantern Posts (`KF_LANTERN`) along path junctions & Pruett Terrace
    lamp_pts = []
    for lx, ly in ((7, 34), (16, 33), (22, 28), (29, 17), (32, 12), (28, 10), (36, 8)):
        if put_sprite_now(m, lx, ly - 1, KF_LANTERN[0], KF_LANTERN[1], on='.d', prot=prot, check_level=True):
            lamp_pts.append((lx, ly - 1))

    # 6. Lush Living SW Meadow Contrast west of Bleed Veil (x<=3, y>=31): vibrant roses & petals!
    for y in range(31, H - 1):
        for x in range(1, 4):
            if m.cls[y, x] == '.' and not m.taken[y, x] and not r.road_mask[y, x]:
                if m.L[1, y, x] == 0:
                    m.L[1, y, x] = ROSE_TILE if (x + y) % 2 == 0 else K.DECOR_SH['flowers'][(x * 3 + y) % 4]
                if m.L[2, y, x] == 0 and (x + y) % 3 == 0:
                    m.L[2, y, x] = PETAL_TILE

    # 7. Still Mirror Pond crystalline shimmer & shoals
    enrich_water_zone(m, water_cls='w', seed=522, lotus=False, shoals=True, glints=True,
                      reeds_cls='', prot=prot, glint_density=0.14)

    # 8. Ethereal Glow Halos & Slanted Crystal Sunbeams (`cv_shaft`)
    add_warm_glows(m, lamp_pts + [(4, 36), (19, 31), (30, 8), (34, 15)])
    add_light_shafts(m, [
        (9, 21), (19, 25), (29, 7), (36, 22), (10, 10), (22, 14),
    ])

    # 9. Re-verify sacred Pruett frost base + Bleed Veil + D1 NE alcove clarity!
    m.L[1, 8, 28] = 9232
    for yy in range(1, 4):
        m.L[1, yy, 38] = 0
        m.L[2, yy, 38] = 0
    veil_tiles = [26048, 26049, 26050]
    for y in range(30, H):
        if y not in (33, 34, 38, 39):
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
    """527 Lacecliff Walk: chalk cliff arches over sparkling sea, sea-pink thrift carpets,
    chalk flagstone headlands (`S_floorpatch`), glowing Wrecker's Lamp & Smugglers' Signal Pole,
    Dew Pond lotus/reeds, cove campfires/shells, coastal buoys & dramatic coastal sunbeams!"""
    extra_rects = [
        (0, 16, 4, 23),      # W->528 seam
        (135, 20, 139, 27),  # E->520 seam
        (74, 42, 82, 50),    # Lost Thread tide-rock neck
        (40, 10, 47, 17),    # Fallen 3rd arch + Rock Smash rubble
        (95, 7, 114, 10),    # High Down corridor between stairs, Birder, Signal Pole & Dew Pond!
    ]
    prot_exact, prot = build_prot_mask(m, 527, extra_rects=extra_rects)
    H, W = m.H, m.W

    # Fix pre-existing HEAD High Down stair pinch: clear stray bushes blocking (98..99, 8..9) & (112, 9)!
    for cx, cy in ((98, 8), (98, 9), (99, 8), (99, 9), (112, 9)):
        if m.inb(cx, cy) and m.ht[cy, cx] == 2 and not m.cliff[cy, cx]:
            m.L[1, cy, cx] = 0
            m.L[2, cy, cx] = 0
            m.taken[cy, cx] = False

    # 1. Mottled coastal heath turf depth
    m.grass_var = True
    m.grass_variation(dark=0.47, worn=True)

    # 2. Chalk Flagstone Headlands (`S_floorpatch`) at Lace Arches, Lacemakers' Bench & Wrecker's Lamp!
    chalk_mask = np.zeros((H, W), dtype=bool)
    for cx, cy, rx, ry in (
        (118, 45, 5.2, 4.0),  # Wrecker's Lamp headland
        (57, 40, 4.8, 3.5),   # Lacemakers' Bench headland
        (104, 28, 4.5, 4.0),  # Lace Arch A approach
        (78, 29, 4.5, 4.0),   # Lace Arch B approach
        (105, 5, 4.2, 2.6),   # Smugglers' Signal Pole pad
    ):
        for y in range(max(2, int(cy - ry - 1)), min(H - 2, int(cy + ry + 2))):
            for x in range(max(2, int(cx - rx - 1)), min(W - 2, int(cx + rx + 2))):
                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 + 0.25 * (vnoise(x, y, 5271, 3.0) - 0.5) <= 1.0:
                    chalk_mask[y, x] = True
    paint_floorpatch(m, chalk_mask, prefix='S_floorpatch', on_cls='.ud', prot_exact=prot_exact, smooth=2)

    # 3. Pack northern coastal woods & add windswept coastal pine/blossom clusters
    infill_forest_now(m, seed=527, prot=prot, snow=False)
    for idx, (cx, cy, pal, cnt, rad, hero) in enumerate([
        (20, 5, COAST_CANOPY, 4, 2.8, None),
        (60, 4, COAST_CANOPY, 4, 2.8, None),
        (132, 6, COAST_CANOPY, 4, 2.8, None),
        (135, 31, COAST_CANOPY, 4, 2.6, None),
        (6, 32, COAST_CANOPY, 4, 2.6, None),
        (74, 12, COAST_CANOPY, 4, 2.6, None),
    ]):
        place_grove_now(m, cx, cy, pal, count=cnt, radius=rad, on='.t', seed=idx + 30, hero=hero, prot=prot)

    # 4. Headland Benches, Coastal Lanterns & Cove Camp Details
    lamp_pts = collect_lamp_positions(m)
    for nm, x, y in (
        ('pf_stonebench', 115, 46), ('hb_barrels', 113, 39), ('hb_crates4', 109, 39),
        ('cs_shell0', 27, 47), ('cs_shell1', 39, 47), ('cs_shell0', 86, 48), ('cs_shell1', 94, 48),
        ('nt_azalea0', 53, 41), ('nt_azalea1', 61, 41), ('nt_azalea2', 114, 43),
    ):
        on_c = 's' if nm.startswith('cs_') else '.du'
        put_near_now(m, nm, x, y, on=on_c, r=2, prot=prot)

    for lx, ly in ((132, 23), (118, 22), (105, 34), (91, 35), (76, 22), (57, 24),
                   (58, 41), (32, 22), (12, 22), (118, 46), (105, 5)):
        res = put_near_now(m, 'pf_lantern', lx, ly - 2, on='.du', r=2, prot=prot)
        if res:
            lamp_pts.append((res[0], res[1] + 1))

    # 5. Dew Pond (113, 6) lotus & reeds + Rich Coastal Sea (shoals, buoys, rocks, glints!)
    enrich_water_zone(m, water_cls='p', seed=5271, lotus=True, shoals=True, glints=True,
                      reeds_cls='.d', prot=prot)
    enrich_water_zone(m, water_cls='wW', seed=5272, lotus=False, shoals=True, glints=True,
                      buoys=[('hb_buoy', 18, 52), ('hb_buoy2', 44, 54), ('hb_buoy', 88, 56),
                             ('hb_buoy2', 124, 57)],
                      rocks=[('cs_wrock0', 6, 54), ('cs_wrock1', 30, 56), ('cs_wrock2', 58, 56),
                             ('cs_wrock0', 84, 59), ('cs_wrock1', 112, 57), ('cs_wrock2', 135, 58)],
                      reeds_cls='', prot=prot)

    # 6. Iconic Sea-Pink Thrift Hollow (22, 5) & Cliff-Top Wildflower Drifts
    add_petals_and_flowers(m, [
        (22, 5, 7.0, 3.2, 0.72, 'seapink'),   # Hidden field of sea-pinks!
        (57, 39, 6.0, 3.5, 0.42, 'seapink'),  # Lacemakers' Bench headland
        (119, 43, 6.0, 4.5, 0.42, 'seapink'), # Wrecker's Lamp headland
        (113, 7, 8.0, 3.5, 0.35, 'wild'),     # High Down Dew Pond
        (46, 9, 7.0, 3.0, 0.32, 'wild'),      # West Down
        (88, 25, 8.0, 4.0, 0.25, 'seapink'),  # Mid cliff heath
        (16, 26, 7.0, 4.0, 0.28, 'wild'),     # West cliff road
    ], seed=527)

    # 7. Warm Glows (Wrecker's Lamp, Signal Pole, Cove Campfire, Lamps) & Coastal Sunbeams!
    add_warm_glows(m, lamp_pts + [(120, 47), (104, 4), (34, 43), (57, 41), (104, 28), (78, 29)])
    add_light_shafts(m, [
        (119, 45), (57, 39), (104, 26), (78, 27), (33, 44), (112, 6), (22, 5), (90, 46),
    ])


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
    """540 Thistledown Lea: grand overgrown estate meadows & Selvedge river!
      - 100% preserves S->552 [20..23], E->524 [30..33] (Wave 11 Gossamer Wood!), Ha-ha ditch,
        Ponyta paddock ledges (30..46, 30), and Stone Bridge (19..24)!
      - Dressed estate flagstones (`S_floorpatch`), sculpted topiaries/statues & rose beds on Manor Hill
      - Lush Selvedge River lotus pads, tall reeds, shoals, mossy rocks & islet groves
      - Mowers' Camp packed earth & glow, lush Bamboo Stand, Gossamer Wood deep-emerald east transition!"""
    extra_rects = [
        (18, 59, 25, 63),    # S->552 seam
        (125, 28, 129, 35),  # E->524 Gossamer Wood seam
        (18, 46, 25, 59),    # Old Stone Bridge
        (28, 28, 48, 32),    # Ponyta paddock ledges
        (80, 1, 93, 25),     # Ha-ha ditch & secret back garden
        (6, 18, 12, 26),     # Brinecut mine mouth
    ]
    prot_exact, prot = build_prot_mask(m, 540, extra_rects=extra_rects)
    H, W = m.H, m.W

    # 1. Deep unmown meadow shaded turf variation
    m.grass_var = True
    m.grass_variation(dark=0.46, worn=True)

    # 2. Manor Hill Weathered Limestone Estate Terraces (`S_floorpatch`) & Mowers' Camp (`E_floorpatch`)!
    manor_mask = np.zeros((H, W), dtype=bool)
    for y in range(4, 23):
        for x in range(52, 81):
            if m.ht[y, x] >= 1 and not m.cliff[y, x]:
                d2 = ((x - 66) / 13.5) ** 2 + ((y - 13) / 8.5) ** 2
                if d2 + 0.25 * (vnoise(x, y, 5401, 3.5) - 0.5) <= 0.92:
                    manor_mask[y, x] = True
    paint_floorpatch(m, manor_mask, prefix='S_floorpatch', on_cls='.d', prot_exact=prot_exact, smooth=2)

    earth_mask = np.zeros((H, W), dtype=bool)
    for cx, cy, rx, ry in (
        (80, 41, 6.2, 4.0),   # Mowers' camp yard
        (95, 45, 4.5, 3.2),   # Broken mill yard
        (112, 20, 5.5, 4.2),  # Bamboo stand floor
        (38, 22, 7.0, 3.5),   # Ponyta paddock run
    ):
        for y in range(max(2, int(cy - ry - 1)), min(H - 2, int(cy + ry + 2))):
            for x in range(max(2, int(cx - rx - 1)), min(W - 2, int(cx + rx + 2))):
                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 + 0.25 * (vnoise(x, y, 5402, 3.0) - 0.5) <= 1.0:
                    earth_mask[y, x] = True
    paint_floorpatch(m, earth_mask, prefix='E_floorpatch', on_cls='.d', prot_exact=prot_exact, smooth=2)

    # 3. Pack forest rim & place rich estate/meadow/Gossamer-edge canopy groves!
    infill_forest_now(m, seed=540, prot=prot, snow=False)
    for idx, (cx, cy, pal, cnt, rad, hero) in enumerate([
        (119, 12, GOSSAMER_EDGE, 6, 3.5, 'pf_g_tree2'),
        (124, 46, GOSSAMER_EDGE, 5, 3.0, 'pf_g_tree2'),
        (6, 40, SPRING_CANOPY, 4, 2.8, None),
        (36, 6, CHERRY_CANOPY, 5, 3.0, None),
        (14, 8, SPRING_CANOPY, 4, 2.8, None),
        (50, 46, SPRING_CANOPY, 4, 2.6, None),
        (100, 46, SPRING_CANOPY, 4, 2.6, None),
        (70, 53, CHERRY_CANOPY, 2, 1.8, None),   # River islet 1 shade!
        (104, 54, SPRING_CANOPY, 2, 1.6, None),  # River islet 2 shade!
    ]):
        place_grove_now(m, cx, cy, pal, count=cnt, radius=rad, on='.t', seed=idx + 50, hero=hero, prot=prot)

    # 4. Manor Topiary Garden Statues, Rose Hedges, Bamboo Reinforcement & Antique Estate Lanterns!
    lamp_pts = collect_lamp_positions(m)
    for nm, x, y in (
        ('mn_statue', 61, 16), ('mn_statue', 70, 16), ('lm_topiary', 55, 13), ('lm_topiary', 77, 13),
        ('lm_topiary', 60, 12), ('lm_topiary', 72, 12), ('pf_stonebench', 61, 18), ('pf_stonebench', 70, 18),
        ('pf_planter0', 62, 23), ('pf_planter1', 68, 23), ('pf_hayrick', 74, 40), ('pf_hayrick', 85, 42),
        ('hb_barrels', 92, 46), ('hb_crates4', 98, 46), ('pf_logbench', 35, 38),
        ('pf_bamboo', 109, 20), ('pf_bamboo', 115, 19), ('pf_bamboo', 117, 21), ('pf_bamboo', 111, 14),
    ):
        put_near_now(m, nm, x, y, on='.dt', r=2, prot=prot)

    for lx, ly in ((24, 46), (24, 59), (38, 35), (56, 33), (63, 25), (67, 25), (64, 15),
                   (70, 15), (78, 34), (96, 35), (114, 31), (124, 31), (14, 30)):
        res = put_near_now(m, 'pf_lantern', lx, ly - 2, on='.d', r=2, prot=prot)
        if res:
            lamp_pts.append((res[0], res[1] + 1))

    # 5. River Selvedge: lush lotus pads, tall reeds, shoals, mossy river boulders & sparkling glints!
    enrich_water_zone(m, water_cls='w', seed=540, lotus=True, shoals=True, glints=True,
                      rocks=[('cs_wrock0', 10, 52), ('cs_wrock1', 35, 54), ('cs_wrock2', 52, 52),
                             ('cs_wrock0', 84, 53), ('cs_wrock1', 116, 54)],
                      reeds_cls='.d', prot=prot)

    # 6. Sweeping Unmown Wildflower Ribbons, Manor Roses & Bamboo/Orchard Petals!
    add_petals_and_flowers(m, [
        (66, 15, 13.0, 6.0, 0.35, 'rose'),    # Overgrown Thistledown Manor rose garden!
        (38, 22, 8.0, 5.0, 0.32, 'wild'),     # Ponyta wildflower paddock
        (46, 44, 11.0, 4.0, 0.38, 'wild'),    # Unmown south meadows
        (88, 42, 10.0, 5.0, 0.30, 'petal'),   # Mowers' meadow petals
        (112, 20, 7.0, 5.0, 0.28, 'petal'),   # Bamboo stand drifting leaves/petals
        (118, 34, 8.0, 6.0, 0.30, 'rose'),    # Gossamer Wood border glade
        (18, 38, 7.0, 5.0, 0.35, 'wild'),     # West river lea
    ], seed=540)

    # 7. Warm Antique Lantern Glows & Golden Estate Sunbeams!
    add_warm_glows(m, lamp_pts + [(66, 10), (78, 41), (21, 52), (94, 44), (9, 22)])
    add_light_shafts(m, [
        (66, 11), (21, 51), (80, 40), (38, 21), (112, 20), (124, 31), (52, 36), (95, 45),
    ])


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

    def intercept_write(self, m_id, head, comment=''):
        captured['m'] = self
        captured['head'] = head
        return self.L

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
    orig_orchard = RE.orchard_rows

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
    try:
        if mid == 521:
            RE.build_521()
        else:
            RCRAFT.BUILD[mid]()
    finally:
        RK.Route.write = orig_rwrite
        RE.orchard_rows = orig_orchard

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
