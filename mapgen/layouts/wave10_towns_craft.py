#!/usr/bin/env python3
"""Wave 10 Rejuvenation V14 Map Craft — The 5 Core Hub Towns & Cities:
  100 Ferrow's Landing          (68x60, ts 51 PF Rejuv Coast)
  120 Briarwick                 (72x64, ts 50 PF Rejuv Village)
  160 Ebbmouth                  (60x54, ts 52 PF Rejuv Snow — unified with Wave 6 Tidelock)
  180 Lumen City - Concourse    (96x72, ts 60 PF Rejuv Lumen)
  280 Verdance - Market Terraces(104x88, ts 55 PF Rejuv City — upgraded from stock ts 33!)

All new/refactored layout craft helpers live cleanly in this exclusive module.
Every building door warp, edge connection road seam, NPC, item, sign, HealingSpot,
and trial_overlay coordinate is preserved 100% matching HEAD.
"""
import os
import sys
import math
import random
import numpy as np
import yaml

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
LAY_DIR = os.path.dirname(os.path.abspath(__file__))
if LAY_DIR not in sys.path:
    sys.path.insert(0, LAY_DIR)

import rkit as K
from rkit import C, P1, STAMPS
from terrain import vnoise

# ================================================================================================
# SHARED REJUVENATION V14 TOWN-CRAFT PRIMITIVES
# ================================================================================================

# Clean-alpha outdoor spring/forest tree families (verified visually against PF Rejuv.png!)
SPRING_CANOPY = ['tr_oak2', 'tr_oak', 'nt_dark_sh', 'nt_teal_a', 'nt_olive', 'nt_blossom', 'tr_pink']
COAST_CANOPY = ['tr_oak2', 'tr_oak', 'nt_blossom', 'tr_pink', 'nt_dark_sh', 'nt_round_sh']
FOREST_CANOPY = ['tr_oak2', 'nt_dark_sh', 'nt_teal_a', 'nt_dpine_sh', 'nt_pine_sh', 'nt_olive', 'tr_oak']
ROYAL_CANOPY = ['tr_oak2', 'nt_dark_sh', 'nt_teal_a', 'nt_blossom', 'tr_pink', 'nt_conifer', 'nt_olive']

# Kristiline frosted teal pines & silver spruces (proven clean in 548 Cocoonfall Hollow!)
KF_TEAL_PINE_A = ([[0, 9833, 9834, 0], [0, 9841, 9842, 0]], [[0, 9849, 9850, 0], [0, 9857, 9858, 0]])
KF_TEAL_PINE_B = ([[0, 9837, 9838, 0], [0, 9845, 9846, 0]], [[0, 9853, 9854, 0], [0, 9861, 9862, 0]])
KF_SPRUCE_A = ([[9944, 9945, 9946], [9952, 9953, 9954]], [[9960, 9961, 9962], [9968, 9969, 9970]])
KF_SPRUCE_B = ([[9947, 9948, 9949], [9955, 9956, 9957]], [[9963, 9964, 9965], [9971, 9972, 9973]])


def reserve_mask(m, coords, pad=0):
    """Build a boolean protection mask around critical event / warp / overlay coordinates."""
    prot = np.zeros((m.H, m.W), dtype=bool)
    for x, y in coords:
        for dy in range(-pad, pad + 1):
            for dx in range(-pad, pad + 1):
                if m.inb(x + dx, y + dy):
                    prot[y + dy, x + dx] = True
    return prot


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


def can_put_clean(m, name, x, y, on='.', prot=None, check_level=True):
    """Strict non-clipping stamp placement check respecting cliffs, events, buildings & level."""
    st = STAMPS[name]
    w, h = st['w'], st['h']
    if x < 0 or y < 0 or x + w > m.W or y + h > m.H:
        return False
    if not m.free(x, y, w, h, on=on):
        return False
    if m.cliff[y:y + h, x:x + w].any():
        return False
    if hasattr(m, 'bfoot') and m.bfoot[y:y + h, x:x + w].any():
        return False
    if prot is not None and prot[y:y + h, x:x + w].any():
        return False
    if check_level:
        sub = m.ht[y:y + h, x:x + w]
        if sub.min() != sub.max():
            return False
    return True


def put_safe(m, name, x, y, on='.', r=1, prot=None, check_level=True):
    """Place prop at (x, y) or nearest clean spot within r; returns (xx, yy) or None."""
    for d in range(r + 1):
        for yy in range(y - d, y + d + 1):
            for xx in range(x - d, x + d + 1):
                if max(abs(xx - x), abs(yy - y)) != d:
                    continue
                if can_put_clean(m, name, xx, yy, on=on, prot=prot, check_level=check_level):
                    m.stamp(name, xx, yy)
                    return (xx, yy)
    return None


def _can_tree_cluster(m, name, x, y, on='.', prot=None):
    """Allows overhanging canopies to interlock naturally while keeping trunks on flat free turf
    and NEVER clipping buildings, cliffs, roads, or protected event zones."""
    st = STAMPS[name]
    w, h = st['w'], st['h']
    if x < 0 or y < 0 or x + w > m.W or y + h > m.H:
        return False
    L = np.array(st['layers'])
    occ = L.max(axis=0) > 0
    over = (L[0] == 0) & (L[1] == 0) & (L[2] > 0)
    body = occ & ~over
    # Body (trunk + lower canopy) must sit cleanly on free flat ground off cliffs/events/buildings
    ys, xs = np.where(body)
    if not len(ys):
        return False
    h0 = m.ht[y + ys[0], x + xs[0]]
    for dy, dx in zip(ys, xs):
        X, Y = x + int(dx), y + int(dy)
        if m.cls[Y, X] not in on or m.taken[Y, X] or m.cliff[Y, X]:
            return False
        if m.ht[Y, X] != h0:
            return False
        if prot is not None and prot[Y, X]:
            return False
        if hasattr(m, 'bfoot') and m.bfoot[Y, X]:
            return False
    # Overhead crown must NEVER clip a building footprint!
    if hasattr(m, 'bfoot') and (m.bfoot[y:y + h, x:x + w] & occ).any():
        return False
    return True


def place_canopy_grove(m, cx, cy, kinds, count=4, radius=2.8, on='.t', seed=0, hero=None,
                       prot=None, undergrowth=True):
    """Place a lush multi-layer overlapping tree cluster (ZERO lone sticker trees!).
    Optionally anchors with a hero giant tree (`pf_g_tree2`) then wraps interlocking mid/low
    canopies & flowering undergrowth (`nt_azalea`, `nt_shrub`, `nt_fern`) around its foot."""
    rng = random.Random(m.seed * 41 + seed + int(cx) * 13 + int(cy) * 7)
    placed = []
    if hero and hero in STAMPS:
        st = STAMPS[hero]
        hx, hy = int(round(cx)) - st['w'] // 2, int(round(cy)) - st['h'] + 2
        if _can_tree_cluster(m, hero, hx, hy, on=on, prot=prot):
            m.stamp(hero, hx, hy, mark='B')
            placed.append((hero, hx, hy))
    # Place overlapping ring of companion trees sorted north-to-south so southern crowns overhang properly
    cand_pts = []
    for _ in range(count * 18):
        k = rng.choice(kinds)
        st = STAMPS[k]
        ang = rng.uniform(0, 2 * math.pi)
        dist = rng.uniform(0.6, radius)
        tx = int(round(cx + math.cos(ang) * dist)) - st['w'] // 2
        ty = int(round(cy + math.sin(ang) * dist * 0.8)) - st['h'] + 1
        cand_pts.append((ty, tx, k))
    # Sort north to south for clean painterly canopy overlap
    for ty, tx, k in sorted(cand_pts):
        if len(placed) >= count + (1 if hero else 0):
            break
        if _can_tree_cluster(m, k, tx, ty, on=on, prot=prot):
            m.stamp(k, tx, ty, mark='B')
            placed.append((k, tx, ty))
    # Cluster lush flowering shrubs & ferns at the grove's sunny edge
    if undergrowth and placed:
        ug_pool = ['nt_azalea0', 'nt_azalea1', 'nt_azalea2', 'nt_shrub0', 'nt_shrub1']
        for _ in range(max(2, len(placed))):
            nm = rng.choice(ug_pool)
            ux = int(round(cx + rng.uniform(-radius - 1.2, radius + 1.2)))
            uy = int(round(cy + rng.uniform(-radius * 0.5, radius + 1.4)))
            if can_put_clean(m, nm, ux, uy, on=on, prot=prot):
                m.stamp(nm, ux, uy)
    return len(placed)


def put_kf_tree(m, x0, y0, top_rows, bot_rows, on='.t', prot=None):
    """Place a Kristiline frosted teal pine or silver spruce cleanly with crown overhang."""
    h_top, w = len(top_rows), len(top_rows[0])
    h_bot = len(bot_rows)
    if x0 < 0 or y0 < 0 or x0 + w > m.W or y0 + h_top + h_bot > m.H:
        return False
    # Check trunk/body cells
    h0 = None
    for dy in range(h_bot):
        for dx in range(w):
            if not bot_rows[dy][dx]:
                continue
            X, Y = x0 + dx, y0 + h_top + dy
            if m.cls[Y, X] not in on or m.taken[Y, X] or m.cliff[Y, X]:
                return False
            if prot is not None and prot[Y, X]:
                return False
            if hasattr(m, 'bfoot') and m.bfoot[Y, X]:
                return False
            if h0 is None:
                h0 = m.ht[Y, X]
            elif m.ht[Y, X] != h0:
                return False
    # Crown must not clip buildings
    if hasattr(m, 'bfoot') and m.bfoot[y0:y0 + h_top + h_bot, x0:x0 + w].any():
        return False
    for dy in range(h_top):
        for dx in range(w):
            t = top_rows[dy][dx]
            if t:
                m.over.append((2, x0 + dx, y0 + dy, t))
    for dy in range(h_bot):
        for dx in range(w):
            t = bot_rows[dy][dx]
            if t:
                X, Y = x0 + dx, y0 + h_top + dy
                m.over.append((1, X, Y, t))
                m.taken[Y, X] = True
                m.cls[Y, X] = 'B'
    return True


def place_snow_grove(m, cx, cy, count=4, radius=2.8, on='.t', seed=0, hero=False, prot=None):
    """Rich multi-species Nordic winter conifer cluster: `pf_g_tree2_ice` + Kristiline teal
    frosted pines + silver spruces + `kf_tree` + `pine2` (ZERO lonely snow stickers!)."""
    rng = random.Random(m.seed * 53 + seed + int(cx) * 11 + int(cy) * 7)
    placed = 0
    if hero:
        st = STAMPS['pf_g_tree2_ice']
        hx, hy = int(round(cx)) - st['w'] // 2, int(round(cy)) - st['h'] + 2
        if _can_tree_cluster(m, 'pf_g_tree2_ice', hx, hy, on=on, prot=prot):
            m.stamp('pf_g_tree2_ice', hx, hy, mark='B')
            placed += 1
    kf_kinds = [KF_TEAL_PINE_A, KF_TEAL_PINE_B, KF_SPRUCE_A, KF_SPRUCE_B]
    cands = []
    for _ in range(count * 16):
        ang = rng.uniform(0, 2 * math.pi)
        dist = rng.uniform(0.5, radius)
        tx = int(round(cx + math.cos(ang) * dist)) - 1
        ty = int(round(cy + math.sin(ang) * dist * 0.8)) - 3
        cands.append((ty, tx, rng.random()))
    for ty, tx, r in sorted(cands):
        if placed >= count + (1 if hero else 0):
            break
        if r < 0.65:
            top_r, bot_r = rng.choice(kf_kinds)
            if put_kf_tree(m, tx, ty, top_r, bot_r, on=on, prot=prot):
                placed += 1
        else:
            k = 'kf_tree' if r < 0.85 else 'pine2'
            if _can_tree_cluster(m, k, tx, ty, on=on, prot=prot):
                m.stamp(k, tx, ty, mark='B')
                placed += 1
    return placed


def add_warm_glows(m, pts):
    """Add warm overhead `pf_glow` (2x2, pri=5, pas=0) halos centered cleanly on (x, y) lamps/beacons."""
    st = STAMPS['pf_glow']['layers'][2]
    for cx, cy in pts:
        x0, y0 = cx - 1, cy - 1
        for dy in range(2):
            for dx in range(2):
                X, Y = x0 + dx, y0 + dy
                if m.inb(X, Y) and m.L[2, Y, X] == 0:
                    m.L[2, Y, X] = st[dy][dx]


def add_festoon_strings(m, runs, kind='lstring'):
    """String overhead warm festoon lanterns across walkable streets & bridges (Layer 3, pri=2)."""
    if kind == 'garl':
        tiles = [K.SINGLE['garl_plain'], K.SINGLE['garl_pennant'], K.SINGLE['garl_lantern'], K.SINGLE['garl_tufts']]
    else:
        tiles = [P1('pf_lstring0'), P1('pf_lstring1'), P1('pf_lstring2')]
    for x0, x1, y, sd in runs:
        for i, x in enumerate(range(x0, x1 + 1)):
            if m.inb(x, y) and m.L[2, y, x] == 0:
                t = tiles[(i + sd) % len(tiles)] if kind == 'lstring' else tiles[(i + sd) % 4 if (i + sd) % 5 else 2]
                m.L[2, y, x] = t


def add_water_glints(m, water_cls='wW', seed=1, density=0.04):
    """Shimmering water surface glints (`hb_glint0..3`, pri=2, pas=0) on open water."""
    rng = random.Random(m.seed * 19 + seed)
    glints = [P1('hb_glint%d' % i) for i in range(4)]
    for y in range(1, m.H - 1):
        for x in range(1, m.W - 1):
            if m.cls[y, x] in water_cls and m.L[2, y, x] == 0 and m.L[1, y, x] == 0:
                if all(m.cls[y + dy, x + dx] in water_cls for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    if rng.random() < density:
                        m.L[2, y, x] = rng.choice(glints)


def add_stepping_stones(m, pts, on_cls='dg'):
    """Walkable stepping stone accents (`pf_stepstone0/1`) strictly over open flat ground."""
    s0, s1 = P1('pf_stepstone0'), P1('pf_stepstone1')
    for x, y in pts:
        if m.inb(x, y) and m.cls[y, x] in on_cls and not m.cliff[y, x] and m.L[1, y, x] == 0 and m.L[2, y, x] == 0:
            m.L[1, y, x] = s0 if (x + y) % 2 == 0 else s1


def paint_boardwalk_strip(m, x0, y0, x1, y1, style='ak', on_cls='sd.g'):
    """Paint walkable timber boardwalk planks on Layer 0 (safe under props, zero passguard hits!)."""
    if style == 'ak':
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
    else:
        t_top, t_mid, t_bot = P1('cv_raft_t'), P1('cv_raft_m'), P1('cv_raft_b')
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if not m.inb(x, y) or m.cliff[y, x]:
                    continue
                if m.cls[y, x] not in on_cls and m.under[y, x] not in on_cls:
                    continue
                t = t_top if y == y0 else t_bot if y == y1 else t_mid
                m.L[0, y, x] = t
                if m.L[1, y, x] >= K.RC.VBASE:
                    m.L[1, y, x] = 0


def paint_plaza_stone(m, x0, y0, x1, y1, border_tile, fill_tiles, on_cls='gdc.s', skip_coords=()):
    """Paint a framed stone plaza on Layer 0 (clearing autotile overlays on L1 when bare),
    never touching cliffs, water, buildings, or `skip_coords`."""
    skip = set(skip_coords)
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if not m.inb(x, y) or (x, y) in skip or m.cliff[y, x]:
                continue
            if m.cls[y, x] not in on_cls and m.under[y, x] not in on_cls:
                continue
            on_edge = (x == x0 or x == x1 or y == y0 or y == y1)
            t = border_tile if on_edge else fill_tiles[(x * 7 + y * 11) % len(fill_tiles)]
            m.L[0, y, x] = t
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


# ================================================================================================
# TOWN 1: 100 FERROW'S LANDING (68x60, ts 51 PF Rejuv Coast)
# ================================================================================================

FERROW_HEAD_EVENTS = {
    'Larch (sendoff)': (35, 5), 'Juno (sendoff)': (31, 3),
    'Quay lamp 1': (22, 46), 'Quay lamp 2': (29, 41), 'Quay lamp 3': (37, 40),
    'Quay lamp 4': (46, 46), 'Quay lamp 5': (51, 41), 'Quay lamp 6': (30, 46),
    'Girl with Wingull': (27, 45), 'Wingull (with girl)': (28, 45), 'Lamplighter': (30, 43),
    'Harbor Crier': (30, 28), 'Town sign': (38, 7), 'Lane sign': (28, 34),
    'Notice board': (27, 27), 'Festival poster': (38, 27), 'Fish barrels': (47, 44),
    'Rope-skipping Girl 1': (34, 27), 'Rope-skipping Girl 2': (35, 27), 'Kelp-drier': (27, 42),
    'Old Sailor': (36, 45), 'Meridian Linesman': (29, 47), 'Fishwife': (48, 45),
    'Woman hanging washing': (14, 43), 'Boy with toy boat': (31, 45), 'Accord Clerk': (25, 45),
    'Drunk on the steps': (27, 35), 'Old Woman on bench': (38, 32), 'Net-mender': (51, 44),
    'Twin 1': (55, 30), 'Twin 2': (56, 30), 'Meridian Recruiter': (35, 22),
    'Boy (town)': (37, 12), "Boy's Mother (town)": (35, 9), 'Woman with crate (town)': (42, 31),
}

# Exact trial_overlay.py event coords on 100 (must remain clear & passable!)
FERROW_OVERLAY_COORDS = [
    (38, 46), (39, 47), (38, 42), (25, 42), (35, 44), (4, 41), (15, 42),
    (32, 46), (34, 55), (33, 45), (45, 45), (50, 46), (52, 43),
    (31, 45), (34, 52), (33, 50), (47, 45), (52, 44), (24, 15), (24, 28),
]


def build_ferrow_100(preview=None):
    """Ferrow's Landing (100) — Rejuvenation V14 coastal harbour town craft revamp."""
    import story_early as SE
    W, H = 68, 60
    SHORE = 48
    PIER = (33, 35)
    WHARF = (21, 49, 46, 47)

    def lip(x):
        if 24 <= x <= 46:
            return 35
        if 47 <= x <= 52:
            return 36
        if 18 <= x <= 23:
            return 37
        if x < 18:
            return 45 + int(round(1.0 * math.sin(x / 3.0)))
        return 43 + int(round(1.5 * math.sin(x / 4.0) + 1.5 * (vnoise(x, 0, 4, 5.0) - 0.5)))

    def shore(x):
        if 18 <= x <= 52:
            return SHORE + (0 if 21 <= x <= 49 else -1)
        return lip(x) + 2

    def hill(x, y):
        # Tidewatch hill (h=2) with organic curved west shoulder instead of dead-straight x=44 ruler line
        if x < 44:
            return False
        if x == 44 and y > 13:
            return False
        if x == 44 and y < 5:
            return False
        return y <= (16 if x < 61 else 18)

    def terrace(x, y):
        # Center terrace (h=2) with softened east promontory instead of dead-straight x=30 ruler line
        if x <= 9 and y <= 18:
            return 2
        if 10 <= x <= 29 and y <= 20:
            return 2
        if x == 30 and 4 <= y <= 18:
            return 2
        return 1

    m = K.RMap(W, H, 51, 100, water='Ocean', kit={1: 'ak', 2: 'sh', 3: 'sh'})
    m.keep_under = 'sgd'
    m.gv_dark = 0.54  # richer mottled coastal meadow shading

    # ---- 1. Terrain: Bluff, Stepped Terraces, Harbour Beach & Layered Ocean ----
    for x in range(W):
        for y in range(H):
            if y <= lip(x):
                m.ht[y, x] = 1
            if hill(x, y):
                m.ht[y, x] = 2
            if terrace(x, y) >= 2:
                m.ht[y, x] = terrace(x, y)
            if y >= shore(x):
                m.cls[y, x] = 'w'
            elif y > lip(x):
                m.cls[y, x] = 's'

    # Deep ocean bathymetry curve offshore (curving around the rocky headland reefs)
    for x in range(W):
        for y in range(H):
            if m.cls[y, x] == 'w' and not (PIER[0] - 2 <= x <= PIER[1] + 2):
                deep_y = 54 + 2.5 * math.sin(x / 8.0) + 2.5 * vnoise(x, 0, 5, 8.0)
                if y >= deep_y:
                    m.cls[y, x] = 'W'

    # Lush interlocking forest rim framing the entire upper town, terraces & flanks
    for y in range(H):
        for x in range(W):
            if m.ht[y, x] < 1:
                continue
            nw = m.ht[y, x] == 2 and x < 30 and (y < 4 + 2 * vnoise(x, 0, 9, 4.0) or x < 5)
            ne = m.ht[y, x] == 2 and x >= 44 and (x > 60 + 2 * vnoise(0, y, 8, 4.0) or (y < 2 and x > 58))
            east = x > 63 + 2 * vnoise(0, y, 11, 4.0) and y < 42
            west = x < 3 + 2 * vnoise(0, y, 12, 4.0) and y < 25
            if nw or ne or east or west:
                m.cls[y, x] = 'T'

    # ---- 2. Stairs (cut cliffs cleanly) ----
    m.stairs(45, 16, w=3, kit_rows=4)
    m.stairs(23, 20, w=3, kit_rows=4)
    m.stairs(25, 35, w=3, kit_rows=3, kind="stone")
    m.stairs(47, 36, w=3, kit_rows=3, kind="stone")
    m.plan_cliffs()

    # ---- 3. Curved Streets & Harbour Overlook Plaza ----
    G = dict(c='g', only='.tT')
    m.rect(32, 0, 3, 7, 'd')
    m.lane([(33.5, 6.5), (37.4, 8.8), (38.6, 13.5), (37, 19.5), (33.8, 24.5)], w=3.3, seed=31, wobble=0.2, **G)
    m.blob(32.5, 29.2, 8.6, 4.3, 'g', seed=32, rough=0.3, only='.tT')
    m.rect(29, 31, 9, 3, 'g', only='.tT')
    m.lane([(24.5, 24.5), (25.2, 27), (27, 28.5)], w=3.0, seed=33, wobble=0.3, **G)
    m.rect(23, 24, 3, 2, 'g', only='.tT')
    m.lane([(25.5, 30.5), (20, 31.6), (13, 31.2), (9.4, 32.5), (8.6, 36), (8.4, 40), (6, 41.6), (4.5, 41.5)],
           w=2.7, seed=34, wobble=0.2, **G)
    m.lane([(8.6, 40.5), (11, 43), (15, 43.2), (17.4, 43)], c='d', w=2.1, seed=35, wobble=0.3, only='.tT')
    m.lane([(39.5, 30.4), (45, 31.3), (51, 30.4), (57, 29.6), (63, 30.4)], w=2.9, seed=36, wobble=0.2, **G)
    m.lane([(46.4, 20.5), (46.2, 22.2), (42.6, 22.6), (41.4, 24), (40.6, 26.6)], c='d', w=2.2, seed=37, wobble=0.2, only='.tT')
    m.rect(45, 20, 3, 1, 'd', only='.tT')
    m.rect(25, 32, 3, 3, 'g', only='.tT')
    m.lane([(48.4, 31.5), (48.4, 35)], w=3.0, seed=39, wobble=0.1, **G)
    m.rect(47, 32, 3, 4, 'g', only='.tT')
    m.lane([(59.5, 31), (60.5, 35), (59.6, 39), (55, 39.6), (53.6, 39.4)], c='d', w=2.1, seed=40, wobble=0.3, only='.tT')
    m.lane([(12, 18.6), (18, 18.4), (24, 18.8), (29, 18.5)], c='d', w=2.0, seed=41, wobble=0.25, only='.tT')
    m.rect(23, 18, 3, 2, 'd', only='.tTg')
    m.street([(46, 15), (46, 13), (51, 13)], 2, 'd', only='.')
    for c in "gd":
        m.smooth(c, into=".", passes=2, only=".tT")
    for y in range(SHORE, H):
        for x in range(PIER[0], PIER[1] + 1):
            m.cls[y, x] = 'w'

    m.stamp('pf_anchor', 32, 29)

    # ---- 4. Buildings (100% Exact HEAD Coordinates & Doors!) ----
    E = []
    P = lambda n, at, **kw: E.append(SE.place(100, n, at, **kw))
    d = {}
    d['pc'] = m.stamp('gl_pc', 18, 4, 'FL_PC', 'Poke Center door')
    d['inn'] = m.stamp('gl_ell', 9, 24, 'FL_INN', 'Inn door')
    d['mart'] = m.stamp('gl_mart', 44, 24, 'FL_MART', 'Mart door')
    d['lab'] = m.stamp('gl_hall', 48, 0, 'FL_LAB', 'Lab door')
    d['customs'] = m.stamp('gl_flat1', 19, 40, 'FL_CUSTOMS', 'Customs door')
    d['dock'] = m.stamp('gl_shed', 43, 39, 'FL_DOCK', 'Dockmaster door')
    m.stamp('lighthouse', 3, 25)
    light_door = (5, 40)
    m.cls[light_door[1], light_door[0]] = 'B'
    houses = (('gl_shed', 11, 10), ('gl_shed', 31, 12), ('gl_shed', 19, 25), ('gl_cot', 52, 20),
              ('gl_shed', 60, 23), ('gl_emblem', 52, 33), ('gl_cot', 11, 34), ('gl_flat2', 36, 1))
    hd = []
    for nm, x, y in houses:
        m.stamp(nm, x, y)
        dd = STAMPS[nm]['door']
        hd.append((x + dd[0], y + dd[1]))
    for dx, dy in list(d.values()) + hd:
        m.doorpath((dx, dy), depth=3 if (dx, dy) == (32, 16) else 6)

    # ---- 5. Exact HEAD Story Events (ALL 68 spec events + 13 trial_overlay anchors protected!) ----
    for i, x in enumerate(range(PIER[0], PIER[1] + 1)):
        P('Customs gate %d' % (i + 1), (x, SHORE - 1))
    for i, x in enumerate(range(PIER[0], PIER[1] + 1)):
        P("Edda's last call %d" % (i + 1), (x, SHORE + 3))
    P('Docking', (33, 58)); P('Calla', (31, SHORE - 1)); P('Captain Edda', (35, SHORE + 5)); P('Aurelian Voss (dock)', (33, SHORE + 6))
    P('Boy (pier)', (34, SHORE)); P("Boy's Mother (pier)", (33, SHORE + 1)); P('Woman with crate (pier)', (35, SHORE + 1))
    P('Accord plaque', (37, SHORE - 1)); P('Odo', (34, 58))
    P('Lighthouse door', light_door)
    gx, gy = d['lab']
    P('Kestrel K1', (gx - 2, gy + 2)); P('Juno (lab yard)', (gx, gy + 1))
    for i, x in enumerate((32, 33, 34, 35)):
        P('Sendoff %d' % (i + 1), (x, 4))
    P('Larch (sendoff)', FERROW_HEAD_EVENTS['Larch (sendoff)'])
    P('Juno (sendoff)', FERROW_HEAD_EVENTS['Juno (sendoff)'])
    P('Wenna Hale', (39, 44)); P('Coll Hale', (41, 45)); P('HiddenItem tart stall', (37, 43))
    P('HiddenItem breakwater', (52, 46)); P('Wingull (rocks)', (19, 47))
    for i in range(1, 7):
        nm = 'Quay lamp %d' % i
        x, y = FERROW_HEAD_EVENTS[nm]
        e = SE.place(100, nm, (x, y))
        e['pages'][0]['graphic'] = {'tile': K.SINGLE['lamp_off'], 'dir': 'down'}
        e['pages'][1]['graphic'] = {'tile': K.SINGLE['lamp_on'], 'dir': 'down'}
        E.append(e)
    for nm in ('Girl with Wingull', 'Wingull (with girl)', 'Lamplighter', 'Harbor Crier', 'Town sign',
               'Lane sign', 'Notice board', 'Festival poster', 'Fish barrels',
               'Rope-skipping Girl 1', 'Rope-skipping Girl 2', 'Kelp-drier', 'Old Sailor',
               'Meridian Linesman', 'Fishwife', 'Woman hanging washing', 'Boy with toy boat',
               'Accord Clerk', 'Drunk on the steps', 'Old Woman on bench', 'Net-mender',
               'Twin 1', 'Twin 2', 'Meridian Recruiter', 'Boy (town)', "Boy's Mother (town)",
               'Woman with crate (town)'):
        P(nm, FERROW_HEAD_EVENTS[nm])
    for e in E:
        m.taken[e['at'][1], e['at'][0]] = True
    for e in E:
        if e.get('type') == 'sign':
            e['post'] = False
            x, y = e['at']
            if e['name'] == 'Town sign':
                m.tile(C('sh', 4833 - 4448), x, y - 1, 2)
                m.tile(C('sh', 4841 - 4448), x, y, 1)
            else:
                m.tile(C('sh', 4847 - 4448), x, y, 1)
    missing = SE.unplaced(100)
    if missing:
        raise SystemExit('ferrow: script events not placed: %s' % missing)
    m.events += E

    # Protect EVERY event & trial_overlay coordinate + doorsteps + N seam + West Street passage!
    door_steps = [(dx, dy + 1) for dx, dy in list(d.values()) + hd + [light_door]]
    seam_n = [(x, y) for x in range(32, 36) for y in range(0, 4)]
    west_street = [(x, y) for x in range(16, 25) for y in range(33, 37)]
    all_ev_pts = [tuple(e['at']) for e in m.events] + FERROW_OVERLAY_COORDS + door_steps + seam_n + west_street
    # Also protect the exact anchor-neighbor cells used by trial_overlay.py (@Accord plaque etc.)
    prot_strict = reserve_mask(m, all_ev_pts, pad=0)
    prot_wide = reserve_mask(m, all_ev_pts, pad=1)
    for x, y in FERROW_OVERLAY_COORDS + door_steps + seam_n + west_street:
        if m.inb(x, y):
            m.taken[y, x] = True

    # ---- 6. High-Craft Coastal Overlook Plaza, Harbour Beach & Lived-in Yards ----
    # Forged iron maritime overlook rail above the harbour (upgrading rustic wood fence!)
    paint_rail_run(m, 29, 46, 34, kind='qy')
    for nm, x, y in (
        # Colorful harbor plaza awning stalls, flower planters, stone benches, barrels & crates
        ('pf_stall0', 26, 25), ('pf_stall2', 36, 25),
        ('gl_tables', 39, 27), ('gl_tables', 25, 28),
        ('pf_planter0', 29, 25), ('pf_planter2', 33, 25), ('pf_planter1', 31, 33), ('pf_planter3', 35, 33),
        ('pf_stonebench', 29, 30), ('pf_stonebench', 36, 32),
        ('sh_crates', 31, 25), ('hb_boxes', 40, 31), ('hb_barrel', 29, 32), ('hb_cask', 38, 33), ('hb_keg', 35, 25),
        ('pf_well', 41, 28),
    ):
        put_safe(m, nm, x, y, on='g.', r=2, prot=prot_wide)

    # Lived-in coastal yards, gardens, washing lines, lighthouse beacon & flower planters
    for nm, x, y in (
        ('pf_beacon', 8, 39), ('pf_stonebench', 10, 41), ('pf_planter0', 4, 42), ('pf_planter1', 6, 42),
        ('hb_washline', 14, 39), ('hb_rugline', 55, 28), ('hb_washline', 57, 40), ('hb_cask', 23, 29),
        ('hb_barrel', 15, 14), ('hb_shed', 35, 14), ('hb_boxes2', 51, 28), ('hb_barrel2', 42, 28),
        ('hb_keg', 64, 28), ('hb_dyeline', 13, 22), ('pf_logbench', 15, 44), ('pf_logbench', 61, 37),
        ('hb_barrel', 19, 31), ('hb_cask', 35, 8), ('pf_logbench', 13, 17), ('hb_shed', 59, 26),
        ('sh_crates', 49, 24), ('hb_rugline2', 41, 6), ('pf_planter2', 21, 15), ('pf_planter3', 26, 15),
        ('pf_planter0', 50, 12), ('pf_planter1', 55, 12), ('pf_planter2', 48, 28), ('pf_planter3', 55, 27),
        ('pf_wagon', 40, 14),
    ):
        put_safe(m, nm, x, y, on='.d', r=2, prot=prot_wide)
    m.fence(51, 58, 29, gaps=((54, 56),))

    # Harbour quay & beach: lively market stalls, fish tubs, nets, bollards, rope coils, ferns & crates!
    for nm, x, y in (
        ('pf_stall1', 35, 41), ('pf_stall3', 29, 39), ('sh_crates', 27, 39), ('sh_crates', 50, 39),
        ('pf_p_net', 31, 40), ('pf_p_net', 51, 39), ('ak_boulder', 18, 39), ('ak_fern', 39, 39),
        ('ak_fern', 33, 39), ('ak_fern', 24, 41), ('pf_p_laundry', 41, 40), ('hb_tubs', 32, 41),
        ('hb_fish', 40, 42), ('hb_boat2', 26, 43), ('hb_boat4', 48, 42), ('hb_barrels', 40, 39),
        ('hb_barrel', 26, 40), ('hb_boxes', 35, 39), ('hb_crates4', 37, 39), ('hb_boxes2', 23, 44),
        ('hb_keg', 32, 44), ('hb_rope', 24, 46), ('hb_rope', 41, 46), ('hb_rope', 48, 46),
        ('hb_banner', 24, 39), ('hb_banner', 45, 39), ('pf_beacon', 20, 45),
    ):
        put_safe(m, nm, x, y, on='s', r=2, prot=prot_wide)

    # Iron bollards & timber mooring posts rhythmically lining the harbour wharf
    for x in (21, 25, 28, 36, 40, 43, 48):
        if not prot_strict[46, x] and not prot_strict[47, x] and not m.taken[46, x] and not m.taken[47, x]:
            m.stamp('hb_post1' if x % 2 else 'hb_post2', x, 46)
    for bx, by in ((23, 47), (32, 47), (36, 47), (44, 47), (49, 47)):
        if not prot_strict[by, bx] and not m.taken[by, bx]:
            m.over.append((1, bx, by, P1('hb_bollard0' if bx % 2 else 'hb_bollard1')))
            m.taken[by, bx] = True

    # ---- 7. Multi-Layer Overhanging Canopy Groves (ZERO lone sticker trees!) ----
    # Replace ALL old polka-dot `autotrees(46)` & single trees with lush interlocking groves + hero trees!
    grove_specs = [
        # NW Poke Center Terrace woodland frame
        (8, 13, COAST_CANOPY, 4, 2.8, 'pf_g_tree2'),
        (16, 14, COAST_CANOPY, 3, 2.4, None),
        (5, 20, COAST_CANOPY, 4, 2.6, 'pf_g_tree2'),
        (28, 8, COAST_CANOPY, 3, 2.2, None),
        # Central valley & cliff shoulders
        (41, 10, COAST_CANOPY, 4, 2.5, 'pf_g_tree2'),
        (42, 17, COAST_CANOPY, 4, 2.6, None),
        (30, 21, COAST_CANOPY, 3, 2.2, None),
        (17, 22, COAST_CANOPY, 4, 2.6, 'pf_g_tree2'),
        # NE Tidewatch Hill lush blossom & oak park
        (61, 9, COAST_CANOPY, 4, 2.8, 'pf_g_tree2'),
        (59, 15, COAST_CANOPY, 4, 2.6, None),
        (46, 5, COAST_CANOPY, 3, 2.3, None),
        # East village & sea-view garden headland
        (63, 20, COAST_CANOPY, 4, 2.6, None),
        (64, 34, COAST_CANOPY, 5, 3.0, 'pf_g_tree2'),
        (61, 41, COAST_CANOPY, 4, 2.6, None),
        (54, 42, COAST_CANOPY, 3, 2.4, None),
        (49, 34, COAST_CANOPY, 3, 2.2, None),
        # West lighthouse bluff & cliff overlook grove
        (2, 31, COAST_CANOPY, 4, 2.5, None),
        (3, 44, COAST_CANOPY, 3, 2.2, None),
    ]
    for idx, (cx, cy, kinds, cnt, rad, hero) in enumerate(grove_specs):
        place_canopy_grove(m, cx, cy, kinds, count=cnt, radius=rad, on='.', seed=idx + 10,
                           hero=hero, prot=prot_wide, undergrowth=True)

    # Tall warm harbour lamps along roads, plaza & wharf
    lamp_pts = []
    for x, y in ((31, 7), (36, 13), (38, 18), (32, 23), (26, 25), (40, 25), (22, 30), (15, 30),
                 (10, 34), (7, 39), (44, 30), (52, 29), (61, 29), (27, 33), (46, 33), (58, 38),
                 (14, 18), (28, 18), (44, 21), (50, 14), (15, 42), (32, 29), (34, 29)):
        if can_put_clean(m, 'gl_lamp', x, y - 1, on='.', prot=prot_wide):
            m.stamp('gl_lamp', x, y - 1)
            lamp_pts.append((x, y - 1))
    for x, y in ((24, 38), (46, 38), (23, 45), (47, 45)):
        if can_put_clean(m, 'pf_wlamp', x, y - 2, on='s', prot=prot_wide):
            m.stamp('pf_wlamp', x, y - 2)
            lamp_pts.append((x, y - 1))

    m.beds()
    # Organic wooded edges (zero scattered single trees!)
    m.greenfill(2)

    # ---- 8. Paint Layers + Post-Paint Stone Plaza, Boardwalks, Reefs & Glows ----
    m.paint_ground()
    m.autotiles()
    m.cliffs()
    m.paint_stairs()
    m.forest()

    # Subtle inset Coastal Cobblestone Medallion right around the Anchor Monument (29..37, 27..32)
    paint_plaza_stone(m, 29, 27, 37, 32, P1('lm_pave0'), [P1('lm_pave1'), P1('lm_pave2'), P1('lm_pave3')],
                      on_cls='g', skip_coords={(32, 29), (33, 29), (34, 29), (32, 30), (33, 30), (34, 30)})

    # Timber Wharf along waterline + Ferry Pier + Harbour Boardwalk Connectors (breaking up the stark white sand!)
    top, body, end = ([C('ak', 1516 + i) for i in range(3)],
                      [C('ak', 1524 + i) for i in range(3)],
                      [C('ak', 1532 + i) for i in range(3)])
    x0, x1, y0, y1 = WHARF
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if m.eff[y, x] not in 'sw':
                continue
            row = top if y == y0 else end if (y == y1 and not PIER[0] <= x <= PIER[1]) else body
            m.L[0, y, x] = row[0 if x == x0 else 2 if x == x1 else 1]
            m.L[1, y, x] = 0
    for y in range(SHORE, H):
        for i, x in enumerate(range(PIER[0], PIER[1] + 1)):
            m.L[0, y, x] = body[i]
            m.L[1, y, x] = 0

    # Weathered timber boardwalk lanes across the beach linking Stairs -> Customs/Dockmaster -> Ferry Pier!
    paint_boardwalk_strip(m, 25, 38, 27, 45, style='ak', on_cls='s')
    paint_boardwalk_strip(m, 47, 39, 49, 45, style='ak', on_cls='s')
    paint_boardwalk_strip(m, 23, 45, 48, 45, style='ak', on_cls='s')
    paint_boardwalk_strip(m, 33, 42, 35, 45, style='ak', on_cls='s')

    # Organic coastal tide-pool pebbles & shells on remaining sand
    rng = random.Random(8)
    for y in range(39, SHORE - 2):
        for x in range(18, 54):
            if m.cls[y, x] == 's' and not m.taken[y, x] and m.L[0, y, x] not in set(top + body + end) and rng.random() < 0.06:
                m.tile(rng.choice([C('ak', 414), C('ak', 427), C('ak', 435)]), x, y, 2)
                m.taken[y, x] = False

    m.put_stamps()
    m.grass_variation(dark=0.54)

    # Stepping stone touches along village lanes & Lighthouse approach
    add_stepping_stones(m, [(33, 6), (34, 7), (36, 10), (37, 15), (36, 20), (33, 24),
                            (24, 19), (25, 25), (46, 21), (47, 14), (8, 35), (8, 39), (6, 41), (11, 31)], on_cls='dg')

    # Moored ship (The Dovetail), layered coastal rock reefs, rowing skiffs & mooring buoys!
    for x, y, z, t in K.SHIP:
        if m.inb(x, y):
            m.L[1 if z == 0 else 2, y, x] = t

    # Sea rocks & rocky coastal reef clusters
    small = [[[C('ak', 1644), C('ak', 1645)], [C('ak', 1652), C('ak', 1653)]],
             [[C('ak', 1646), C('ak', 1647)], [C('ak', 1654), C('ak', 1655)]]]
    rng_r = random.Random(5)
    for nm, x, y in (('ak_rock2', 10, 50), ('ak_boulder', 58, 50), ('ak_rock2', 25, 54), ('ak_rock2', 61, 45),
                     ('ak_rock2', 3, 52), ('ak_rock2', 14, 54), ('ak_boulder', 62, 53)):
        L = np.array(STAMPS[nm]['layers'])
        h, w = L.shape[1:]
        if x + w <= W and y + h <= H and all(m.cls[y + j, x + i] in 'wW' and m.L[2, y + j, x + i] == 0 for i in range(w) for j in range(h)):
            for j in range(h):
                for i in range(w):
                    for z in (1, 2):
                        if L[z, j, i]:
                            m.L[2, y + j, x + i] = L[z, j, i]
    for x, y in ((15, 52), (5, 56), (44, 57), (64, 57), (20, 51), (53, 49), (1, 49), (8, 56), (22, 57)):
        r = rng_r.choice(small)
        if x + 2 <= W and y + 2 <= H and all(m.cls[y + j, x + i] in 'wW' and m.L[2, y + j, x + i] == 0 for i in range(2) for j in range(2)):
            for j in range(2):
                for i in range(2):
                    m.L[2, y + j, x + i] = r[j][i]

    # Moored skiffs & harbour buoys
    for nm, x, y in (('hb_boat1', 23, 48), ('hb_boat3', 28, 49), ('hb_boat2', 37, 49), ('hb_boat1', 43, 48),
                     ('hb_boat4', 29, 52), ('hb_boat3', 18, 49), ('hb_buoy', 32, 50), ('hb_buoy', 36, 51), ('hb_buoy', 22, 52)):
        L = np.array(STAMPS[nm]['layers'])
        h, w = L.shape[1:]
        if x + w <= W and y + h <= H and all(m.cls[y + j, x + i] in 'wW' and m.L[2, y + j, x + i] == 0 and m.L[1, y + j, x + i] == 0 for i in range(w) for j in range(h)):
            for j in range(h):
                for i in range(w):
                    t = int(L[:, j, i].max())
                    if t:
                        m.L[2, y + j, x + i] = t

    # Overhead harbour festoon strings, warm glowing lantern halos & shimmering ocean wave glints!
    add_festoon_strings(m, [(27, 39, 26, 0), (26, 42, 33, 2), (24, 33, 45, 1), (36, 46, 45, 0)], kind='lstring')
    add_warm_glows(m, lamp_pts + [(33, 30), (22, 46), (29, 41), (37, 40), (46, 46), (51, 41), (30, 46), (8, 40), (20, 46), (5, 27)])
    add_water_glints(m, water_cls='wW', seed=100, density=0.032)

    m.scatter(12, seed=12, on=".T")
    for sx_ in range(32, 36):
        for sy_ in (0, 1):
            m.L[1, sy_, sx_] = 0
            m.L[2, sy_, sx_] = 0
    m.seal_against([{'dir': 'N', 'offset': 28, 'to': 520, 'to_offset': 11}],
                   spans=[('N', 32, 4)],
                   keep=[tuple(e['at']) for e in m.events if e.get('type') == 'warp'] +
                        [(x, y) for x in range(m.W) for y in range(m.H - 12, m.H)])
    seal_unconnected_edges(
        m,
        open_cells=[(x, 0) for x in range(32, 36)] +
                   [tuple(e['at']) for e in m.events if e.get('type') == 'warp'] +
                   [(x, y) for x in range(m.W) for y in range(m.H - 12, m.H)],
    )

    if preview:
        m.preview(preview, 0.5)
    head = {'id': 100, 'biome': 'village', 'name': "Ferrow's Landing", 'parent': 0, 'bgm': 'Lappet Town',
            'rubric': True, 'yards_ok': True,
            'metadata': {'Outdoor': True, 'ShowArea': True, 'MapPosition': [0, 14, 26], 'BattleBack': 'field'},
            'tone': [6, 2, -10, 0],
            'fog': {'name': 'prismfall_seamist', 'opacity': 34, 'blend': 0, 'zoom': 100, 'sx': 2, 'sy': 0},
            'connections': [{'dir': 'N', 'offset': 28, 'to': 520, 'to_offset': 11}],
            '_file': '100_ferrows_landing.yaml'}
    m.write(100, head, "# Ferrow's Landing (100). WRITTEN BY layouts/ferrow_rj.py (Wave 10 Rejuv V14 Craft) - edit wave10_towns_craft.py.\n")
    print('100 Ferrow doors', d)
    return m


# ================================================================================================
# TOWN 2: 120 BRIARWICK (72x64, ts 50 PF Rejuv Village)
# ================================================================================================

BRIARWICK_HEAD_EVENTS = {
    'North Gate sign': (51, 4), 'Town sign': (38, 58), 'Finch': (57, 33),
    'Rope-bridge Boy': (28, 32), 'Grandmother knitting': (45, 36), 'Dyer': (16, 37),
    'Apprentice': (21, 32), 'Silk Merchant': (35, 35), 'Meridian Linesman': (53, 31),
    'Tired Mother': (32, 46), 'Old Man on bridge': (9, 32), 'Girl in ogre mask': (44, 31),
    'Boy in dog mask': (45, 32), 'Egg-seller': (47, 34), 'Tax-barge Deserter': (33, 55),
    'Accord Chaplain': (60, 47), 'Youngster': (50, 29), 'Woman with basket': (48, 41),
    "Cutter's Wife": (44, 52), 'Bun-seller': (40, 40),
}
BRIARWICK_OVERLAY_COORDS = [(25, 9), (26, 9), (47, 26), (36, 62)]


def build_briarwick_120(preview=None):
    """Briarwick (120) — Rejuvenation V14 lush weaver's silkwood village craft revamp."""
    import story_early as SE
    W, H = 72, 64
    DECK = {k: C('sh', v) for k, v in dict(
        TL=488, T=489, TR=490, L=496, C=497, R=498, BL=504, B=505, BR=506,
        legL=523, leg=524, legR=525).items()}

    def sx(y):
        dye_bend = 2.6 * math.exp(-((y - 39.5) / 6.5) ** 2)
        return 8 + int(round(dye_bend + 2.0 * math.sin(y / 6.8) + 1.5 * (vnoise(0, y, 6, 6.0) - 0.5)))

    def ridge(x):
        if 28 <= x <= 50:
            return 14
        if 18 <= x <= 27:
            return 12 + (1 if x > 22 else 0)
        return 10 + int(round(1.5 * math.sin(x / 5.0) + 1.5 * (vnoise(x, 0, 3, 6.0) - 0.5)))

    def deck(m, x0, y0, w, h, stairs=None, open_e=(), open_w=()):
        if not hasattr(m, '_deck_tiles'):
            m._deck_tiles = []
        for y in range(y0, y0 + h):
            for x in range(x0, x0 + w):
                top = (y == y0)
                bot = (y == y0 + h - 1) and not (stairs is not None and x in (stairs, stairs + 1))
                lft = (x == x0) and (y not in open_w)
                rgt = (x == x0 + w - 1) and (y not in open_e)
                k = ('T' if top else 'B' if bot else '') + ('L' if lft else 'R' if rgt else '')
                k = k or 'C'
                tid = DECK[k]
                m.tile(tid, x, y, 1)
                m.cls[y, x] = 'D'
                m._deck_tiles.append((x, y, tid))
        if all(m.inb(x, y0 - 1) and m.cls[y0 - 1, x] in '.t' and not m.taken[y0 - 1, x] for x in range(x0, x0 + w)):
            m.fence(x0, x0 + w - 1, y0 - 1)
        for x in range(x0, x0 + w):
            if stairs is not None and x in (stairs, stairs + 1):
                continue
            m.tile(DECK['legL' if x == x0 else 'legR' if x == x0 + w - 1 else 'leg'], x, y0 + h, 1)
            m.cls[y0 + h, x] = 'B'
        if stairs is not None:
            for i, x in enumerate((stairs, stairs + 1)):
                m.tile(m.STAIRS[0 if i == 0 else 2], x, y0 + h, 2)
                m.cls[y0 + h, x] = 'd'

    def walkway(m, x0, x1, y):
        if not hasattr(m, '_deck_tiles'):
            m._deck_tiles = []
        for x in range(x0, x1 + 1):
            m.tile(DECK['T'], x, y, 1); m.tile(DECK['B'], x, y + 1, 1)
            m.cls[y, x] = m.cls[y + 1, x] = 'D'
            m._deck_tiles.append((x, y, DECK['T'])); m._deck_tiles.append((x, y + 1, DECK['B']))
            m.taken[y, x] = m.taken[y + 1, x] = True

    m = K.RMap(W, H, 50, 120, water='Sea(Grass)', kit='sh')
    m.keep_under = 'd'
    m.gv_dark = 0.50  # deeper dappled woodland shade!

    # ---- 1. Terrain: North Ridge, Organic Woodland Brook & Deep Silkwood Rim ----
    for x in range(W):
        for y in range(H):
            if y <= ridge(x):
                m.ht[y, x] = 1
    for y in range(H):
        s = sx(y)
        for x in range(s, s + 3):
            m.cls[y, x] = 'w'
    m.blob(16, 49, 5.8, 3.4, 'w', seed=7, rough=0.5)
    m.blob(13, 45, 2.8, 2.2, 'w', seed=8, rough=0.4)
    for y in range(H):
        for x in range(W):
            if m.cls[y, x] == 'w':
                m.ht[y, x] = 0

    for y in range(H):
        for x in range(W):
            if m.cls[y, x] != '.':
                continue
            edge = min(x, W - 1 - x, y, H - 1 - y)
            s_skirt = (H - 1 - y) < 5 + int(round(2.4 * vnoise(x, 9, 13, 5.5))) and not (32 <= x <= 39)
            deep = edge < 4 + 4 * vnoise(x, y, 11, 6.0) or s_skirt
            knoll = ((x - 36) / 9.0) ** 2 + ((y - 11) / 5.5) ** 2 < 1.0 + 0.5 * (vnoise(x, y, 4, 3.0) - 0.5)
            shrine = ((x - 22) / 5.5) ** 2 + ((y - 9) / 4.5) ** 2 < 1.0 + 0.5 * (vnoise(x, y, 5, 3.0) - 0.5)
            ridge_forest = m.ht[y, x] == 1 and not knoll and not shrine
            if deep or ridge_forest:
                m.cls[y, x] = 'T'

    # ---- 2. Stairs & Curved Woodland Lanes ----
    m.stairs(35, 14, w=3, kit_rows=4)
    m.stairs(21, 12, w=2, kit_rows=4)
    m.plan_cliffs()
    LN = dict(c='d', only='.tT')
    m.blob(40.5, 33.0, 8.4, 5.0, 'd', seed=51, rough=0.3, only='.tT')
    m.rect(0, 30, 16, 2, 'd', only='.T')
    m.lane([(15, 31), (21, 31.4), (27, 32.4), (32.5, 33)], w=2.6, seed=52, wobble=0.2, **LN)
    m.rect(35, 18, 3, 1, 'd', only='.tT')
    m.lane([(36.5, 18.5), (37.2, 21.5), (39.2, 24.6), (40, 28.4)], w=2.8, seed=53, wobble=0.2, **LN)
    m.rect(21, 16, 2, 1, 'd', only='.tT')
    m.lane([(22, 16.5), (23.4, 19.2), (29, 20.4), (35.6, 19.6)], w=2.1, seed=54, wobble=0.2, **LN)
    m.lane([(48.4, 32.6), (54, 31.3), (60, 31)], w=2.9, seed=55, wobble=0.2, **LN)
    m.rect(59, 30, 13, 3, 'd', only='.tT')
    m.rect(34, 57, 4, 7, 'd', only='.tT')
    m.lane([(35.6, 57.5), (34.4, 52), (34.8, 46.5), (36.6, 41.5), (38.4, 38)], w=2.9, seed=56, wobble=0.25, **LN)
    m.lane([(46, 36.6), (48.4, 41), (52, 46), (58, 47.4), (64.4, 47.2)], w=2.4, seed=57, wobble=0.25, **LN)
    m.lane([(36.5, 56.6), (44, 57), (53, 56.6), (62.5, 56.8)], w=2.2, seed=58, wobble=0.2, **LN)
    m.lane([(34.6, 46.2), (30, 45.2), (25, 45.4), (19.6, 44.6), (17.8, 40), (17.6, 35), (18.4, 32)], w=2.3, seed=59, wobble=0.25, **LN)
    m.lane([(34.5, 57.4), (30, 57.2), (26.5, 56.6)], w=2.0, seed=60, wobble=0.15, **LN)
    m.rect(22, 10, 2, 3, 'd', only='.')
    m.smooth('d', into='.', passes=2, only='.tT')
    m.lane([(42.5, 12.5), (46, 9.5), (51, 6), (53.5, 2), (53.5, 0)], w=3.2, seed=63, wobble=0.15, **LN)
    m.rect(52, 0, 4, 3, 'd', only='.tT')
    m.rect(0, 29, 4, 4, 'T', only='.d')
    m.blob(40.8, 32.0, 3.6, 2.0, '.', seed=61, rough=0.2, only='d')

    # ---- 3. Buildings (100% Exact HEAD Coordinates & Doors!) ----
    E = []
    P = lambda n, at, **kw: E.append(SE.place(120, n, at, **kw))
    d = {}
    d['gym'] = m.stamp('pf_g_elder', 30, 1, 'BW_GYM', 'Gym door')
    d['guild'] = m.stamp('pf_g_tree6', 13, 19, 'BW_GUILD', 'Guildhall door')
    d['pc'] = m.stamp('gl_ell', 45, 19, 'BW_PC', 'Poke Center door')
    d['house1'] = m.stamp('pf_g_tree4', 58, 17, 'BW_HOUSE1', 'Treetop House door')
    d['mart'] = m.stamp('gl_flat2', 25, 39, 'BW_MART', 'Mart door')
    d['chapel'] = m.stamp('sh_big', 55, 34, 'BW_CHAPEL', 'Chapel door')
    d['house2'] = m.stamp('pf_g_tree4', 40, 44, 'BW_HOUSE2', "Cutter's House door")
    m.stamp('pf_g_tree2', 39, 27)
    hd = []
    for y in range(49, 59):
        for x in range(23, 32):
            if m.cls[y, x] == 'T':
                m.cls[y, x] = '.'
    for nm, x, y in (('pf_g_tree4p', 20, 36), ('pf_g_tree2', 57, 7), ('pf_g_tree2', 66, 14),
                     ('pf_g_tree2', 46, 50), ('gl_shed', 65, 22), ('gl_shed', 50, 36), ('gl_cot', 24, 49),
                     ('pf_g_tree2', 8, 54), ('pf_g_tree2', 67, 40)):
        if m.free(x, y, STAMPS[nm]['w'], STAMPS[nm]['h'], on='.dT') and not (nm.startswith('pf_g') and (m.cls[y:y + STAMPS[nm]['h'], x:x + STAMPS[nm]['w']] == 'd').any()):
            m.stamp(nm, x, y)
            if 'door' in STAMPS[nm]:
                dd = STAMPS[nm]['door']
                hd.append((x + dd[0], y + dd[1]))
    # Lantern House hollow tree at exact HEAD (24, 2) -> door (26, 8)
    d['lantern'] = m.stamp('pf_g_tree4', 24, 2, 'BW_LANTERN', 'Lantern House door', blend=True)
    for dx, dy in list(d.values()) + hd:
        m.doorpath((dx, dy), depth=8)
    for x, y in ((38, 31), (39, 33), (43, 31), (42, 33), (44, 32), (37, 32), (45, 27), (44, 27)):
        if m.cls[y, x] == '.' and not m.taken[y, x]:
            m.tile(m.decor['flowers'][(x * 3 + y) % 6], x, y, 1)

    if can_put_clean(m, 'pf_pcsign', 44, 25, on='.d'):
        m.stamp('pf_pcsign', 44, 25)
    deck(m, 22, 23, 7, 4, stairs=24)
    deck(m, 51, 52, 5, 3, stairs=52, open_e=(52, 53))
    deck(m, 59, 52, 5, 3, stairs=61, open_w=(52, 53))
    walkway(m, 56, 58, 52)
    walkway(m, sx(30) - 2, sx(31) + 4, 30)

    # ---- 4. Exact HEAD Events (ALL 53 spec events + Lyra overlay protected!) ----
    P('To Gossamer Wood', (35, 63)); P('To Gossamer Wood b', (36, 63))
    E.append({'type': 'sign', 'name': 'North Gate sign', 'at': list(BRIARWICK_HEAD_EVENTS['North Gate sign']),
              'post': False, 'text': "NORTH GATE - Spinners' Rise, Frostwick Pass and the Hoar Road north."})
    P('Arrival', (34, 62)); P('Juno (arrival)', (36, 61)); P('Stage manager', (37, 62))
    gx, gy = d['gym']
    P('Loomhouse sign', (gx + 4, gy))
    P('Loyal Three shrine', (21, 8)); P('Old woman at the shrine', (22, 9)); P('Dusk petal', (23, 8))
    P('Lattice pylon', (69, 30)); P('Survey flags', (67, 33))
    for i, y in enumerate((30, 31, 32)):
        P('Pylon watch %d' % (i + 1), (63, y))
    P('Pallbearer Thistle', (66, 31)); P('Bereaved 1', (65, 30)); P('Bereaved 2', (66, 32))
    P('Tamsin (square)', (41, 34)); P('Festival poster', (38, 30)); P('Charcoal child', (38, 35))
    P('Weaver at loom', (26, 25)); P('Silk racks', (23, 24)); P('HiddenItem rope bridge', (28, 21))
    P('HiddenItem dye vats', (14, 38))
    for nm in ('Town sign', 'Finch', 'Rope-bridge Boy', 'Grandmother knitting', 'Dyer', 'Apprentice',
               'Silk Merchant', 'Meridian Linesman', 'Tired Mother', 'Old Man on bridge',
               'Girl in ogre mask', 'Boy in dog mask', 'Egg-seller', 'Tax-barge Deserter',
               'Accord Chaplain', 'Youngster', 'Woman with basket', "Cutter's Wife", 'Bun-seller'):
        P(nm, BRIARWICK_HEAD_EVENTS[nm])
    for e in E:
        m.taken[e['at'][1], e['at'][0]] = True
    for e in E:
        if e.get('type') == 'sign':
            e['post'] = False
            x, y = e['at']
            if e['name'] in ('Town sign', 'Loomhouse sign'):
                m.tile(4833, x, y - 1, 2); m.tile(4841, x, y, 1)
            elif e['name'] != 'Silk racks':
                m.tile(4847, x, y, 1)
    missing = SE.unplaced(120)
    if missing:
        raise SystemExit('briarwick: script events not placed: %s' % missing)
    m.events += E

    door_steps = [(dx, dy + 1) for dx, dy in list(d.values()) + hd]
    pc_yard_exit = [(x, y) for x in range(46, 49) for y in range(26, 32)]
    all_ev_pts = [tuple(e['at']) for e in m.events] + BRIARWICK_OVERLAY_COORDS + door_steps + pc_yard_exit
    prot_wide = reserve_mask(m, all_ev_pts, pad=1)
    for x, y in BRIARWICK_OVERLAY_COORDS + door_steps + pc_yard_exit:
        if m.inb(x, y):
            m.taken[y, x] = True

    # ---- 5. High-Craft Weaver's Village Dressing: Silk Racks, Stalls, Flower Boxes & Shrine ----
    for nm, x, y in (
        ('pf_p_loom', 23, 24), ('pf_p_loom', 27, 24), ('pf_p_laundry', 23, 23),
        ('pf_p_vat_b', 14, 36), ('pf_p_vat_r', 15, 37), ('pf_p_vat_y', 14, 39),
        ('sh_crates', 51, 52), ('sh_crates', 62, 52), ('pf_logbench', 59, 53),
        ('sh_campfire', 38, 36), ('sh_crates', 52, 29), ('pf_p_silk', 54, 52), ('pf_p_silk', 60, 52),
        ('pf_logbench', 38, 33), ('pf_logbench', 42, 33),
        # Upgraded colorful artisan weaver stalls & silk racks around the Gathering Green!
        ('pf_stall0', 33, 29), ('pf_stall4', 44, 36), ('gw_rack', 15, 34), ('gw_spool', 16, 40),
        ('gw_rack', 31, 35), ('gw_spool', 43, 29),
        ('hb_boxes', 34, 37), ('hb_cask', 44, 29), ('hb_washline', 62, 26), ('hb_barrel', 53, 26),
        ('pf_logbench', 20, 47), ('hb_keg', 31, 43), ('hb_barrel2', 57, 46), ('hb_rugline2', 20, 28),
        ('pf_logbench', 47, 44), ('hb_boxes2', 37, 51), ('hb_cask', 31, 54), ('hb_barrel', 47, 36),
        # Flower planters, stone benches, village well, shrine incense & weavers' flower boxes
        ('pf_planter0', 42, 26), ('pf_planter1', 26, 44), ('pf_planter2', 60, 43), ('pf_planter3', 31, 44),
        ('pf_planter0', 34, 13), ('pf_planter1', 38, 13), ('pf_planter2', 19, 10), ('pf_planter3', 24, 10),
        ('pf_planter0', 33, 57), ('pf_planter2', 38, 57),
        ('pf_stonebench', 32, 21), ('pf_stonebench', 40, 21), ('pf_stonebench', 33, 13),
        ('pf_well', 44, 42), ('pf_shrine', 20, 6),
    ):
        st = STAMPS[nm]
        on_deck = all(m.inb(x + i, y + j) and m.cls[y + j, x + i] == 'D' for i in range(st['w']) for j in range(st['h']))
        if on_deck or can_put_clean(m, nm, x, y, on='.dD', prot=prot_wide):
            m.over += [(z, x + i, y + j, t) for z in (1, 2) for j in range(st['h']) for i in range(st['w'])
                       for t in [st['layers'][z][j][i]] if t]
            m.taken[y:y + st['h'], x:x + st['w']] = True
        else:
            put_safe(m, nm, x, y, on='.d', r=2, prot=prot_wide)

    # Stream-bank reeds, water lilies, mossy boulders & vibrant azaleas along the dye-mill brook!
    for nm, x, y in (
        ('nt_reed0', 11, 33), ('nt_reed1', 12, 35), ('nt_reed0', 13, 41), ('nt_reed1', 18, 47),
        ('nt_reed0', 12, 52), ('nt_reed1', 11, 25), ('nt_reed0', 12, 18), ('nt_reed1', 19, 51),
        ('nt_lily', 13, 38), ('nt_lily', 17, 45), ('nt_lily', 19, 49), ('nt_lily', 12, 28),
        ('nt_boulder', 12, 22), ('nt_boulder', 20, 49), ('nt_boulder', 13, 54),
        ('nt_azalea0', 33, 19), ('nt_azalea1', 42, 19), ('nt_azalea2', 32, 59),
        ('nt_azalea0', 39, 59), ('nt_azalea1', 55, 29), ('nt_azalea2', 20, 49),
        ('nt_azalea0', 18, 9), ('nt_azalea1', 27, 11), ('nt_azalea2', 42, 13),
        ('nt_shrub0', 30, 13), ('nt_shrub1', 44, 13), ('nt_shrub0', 52, 26), ('nt_shrub1', 24, 34),
    ):
        put_safe(m, nm, x, y, on='.t', r=1, prot=prot_wide)

    # Wild grass edges along forest & brook
    for y in range(0, 3):
        for x in range(26, 47):
            if m.cls[y, x] == '.' and not m.taken[y, x]:
                m.cls[y, x] = 't'
    for y in range(H):
        for x in range(W):
            if m.cls[y, x] == '.' and not m.taken[y, x] and m.ht[y, x] == 0:
                near_edge = any(m.inb(x + dx, y + dy) and m.cls[y + dy, x + dx] in 'Tw'
                                for dx in (-2, -1, 0, 1, 2) for dy in (-2, -1, 0, 1, 2))
                if near_edge and vnoise(x, y, 17, 4.0) > 0.56:
                    m.cls[y, x] = 't'

    # ---- 6. Lush Overlapping Silkwood Canopy Clusters (ZERO lone sticker trees!) ----
    grove_specs = [
        (30, 27, FOREST_CANOPY, 4, 2.5, None),
        (24, 37, FOREST_CANOPY, 4, 2.5, None),
        (23, 47, FOREST_CANOPY, 3, 2.2, None),
        (33, 22, FOREST_CANOPY, 3, 2.2, None),
        (42, 21, FOREST_CANOPY + ['nt_blossom'], 4, 2.4, None),
        (56, 26, FOREST_CANOPY, 3, 2.3, None),
        (53, 41, FOREST_CANOPY, 4, 2.6, 'pf_g_tree2'),
        (46, 59, FOREST_CANOPY, 4, 2.6, None),
        (56, 59, FOREST_CANOPY, 4, 2.6, None),
        (20, 58, FOREST_CANOPY, 4, 2.6, None),
        (17, 17, FOREST_CANOPY + ['nt_blossom'], 3, 2.2, None),
        (55, 13, FOREST_CANOPY + ['nt_blossom'], 4, 2.6, None),
        (66, 35, FOREST_CANOPY, 3, 2.2, None),
        (39, 54, FOREST_CANOPY, 3, 2.2, None),
    ]
    for idx, (cx, cy, kinds, cnt, rad, hero) in enumerate(grove_specs):
        place_canopy_grove(m, cx, cy, kinds, count=cnt, radius=rad, on='.', seed=idx + 20,
                           hero=hero, prot=prot_wide, undergrowth=True)

    # Warm village street lanterns lining every curved silkwood lane
    lamp_pts = []
    for x, y in ((34, 22), (42, 27), (32, 38), (49, 35), (37, 48), (58, 29), (26, 31), (19, 30),
                 (33, 29), (50, 45), (22, 46), (16, 40), (45, 55), (57, 55), (61, 46), (32, 55),
                 (25, 19), (33, 60), (38, 60), (34, 13), (39, 13), (19, 9), (47, 10)):
        if can_put_clean(m, 'pf_lantern', x, y - 1, on='.', prot=prot_wide):
            m.stamp('pf_lantern', x, y - 1)
            lamp_pts.append((x, y - 1))

    m.beds(prefixes=('sh_', 'gl_'))
    m.greenfill(2)

    # ---- 7. Paint + Cedar Decks + Stepping Stones + Garlands + Warm Glows ----
    m.paint()
    for dx_, dy_, tid_ in getattr(m, '_deck_tiles', ()):
        m.L[0, dy_, dx_] = tid_
        if m.L[1, dy_, dx_] == tid_:
            m.L[1, dy_, dx_] = 0
    if m.L[2, 49, 30] == 3255:
        m.L[2, 49, 30] = 0

    # Curved stepping stones around the Gathering Tree Green, Loomhouse Plaza, Shrine & Brook!
    add_stepping_stones(m, [
        (36, 19), (37, 22), (39, 25), (35, 31), (36, 33), (38, 34), (42, 34), (44, 33), (45, 31),
        (36, 59), (35, 61), (47, 26), (29, 44), (22, 11), (22, 16), (36, 13), (46, 9), (50, 6),
        (17, 32), (18, 36), (18, 41), (24, 45), (51, 31), (57, 31),
    ], on_cls='d')

    # Overhead weaver's silk garlands strung across ALL major lanes & commons
    add_festoon_strings(m, [
        (33, 48, 28, 0), (33, 48, 38, 1), (44, 50, 27, 2), (17, 28, 30, 3),
        (50, 58, 33, 1), (33, 38, 56, 2), (32, 37, 45, 3), (34, 38, 60, 0),
        (35, 40, 20, 2), (48, 56, 47, 1),
    ], kind='garl')

    # Warm golden firefly/lantern glows across every lantern, campfire, shrine & cedar deck!
    add_warm_glows(m, lamp_pts + [(40, 36), (21, 7), (36, 12), (25, 24), (53, 53), (61, 53), (12, 30), (47, 25)])
    add_water_glints(m, water_cls='w', seed=120, density=0.04)

    m.scatter(11, seed=21, on='.T')
    m.seal_against([{'dir': 'N', 'offset': 52, 'to': 566, 'to_offset': 38}],
                   spans=[('N', 52, 4)],
                   keep=[tuple(e['at']) for e in m.events if e.get('type') == 'warp'])
    seal_unconnected_edges(
        m,
        open_cells=[(x, 0) for x in range(52, 56)] +
                   [tuple(e['at']) for e in m.events if e.get('type') == 'warp'],
    )
    if preview:
        m.preview(preview, 0.5)
    head = {'id': 120, 'biome': 'forest', 'name': 'Briarwick', 'parent': 0, 'bgm': 'Lappet Town',
            'rubric': True, 'yards_ok': True,
            'metadata': {'Outdoor': True, 'ShowArea': True, 'MapPosition': [0, 12, 22], 'BattleBack': 'forest'},
            'tone': [-10, -22, 2, 4],
            'fog': {'name': 'prismfall_spores', 'opacity': 46, 'blend': 1, 'zoom': 100, 'sx': 1, 'sy': -1},
            'connections': [{'dir': 'N', 'offset': 52, 'to': 566, 'to_offset': 38}],
            '_file': '120_briarwick.yaml'}
    src = yaml.safe_load(open(os.path.join(HERE, 'layouts', 'briarwick_events.yaml')))[120]['head']
    for k in ('bgm', 'metadata', 'field', 'display_name'):
        if k in src:
            head[k] = src[k]
    m.write(120, head, '# Briarwick (120). WRITTEN BY layouts/briarwick_rj.py (Wave 10 Rejuv V14 Craft) - edit wave10_towns_craft.py.\n')
    print('120 Briarwick doors', d)
    return m


# ================================================================================================
# TOWN 3: 160 EBBMOUTH (60x54, ts 52 PF Rejuv Snow — Unified with Wave 6 Tidelock!)
# ================================================================================================

EBBMOUTH_HEAD_EVENTS = {
    'Gym sign': (22, 17), 'Town sign': (24, 46), 'Lattice sign': (27, 40),
    'Towpath sign': (30, 2), 'PC sign': (9, 22), 'Upper mill': (31, 3),
    'Guild mill': (29, 37), 'Harbour mast': (52, 37), 'Ice-fisher': (13, 33),
    'Guild striker': (8, 26), 'Dockworker': (49, 36), 'Guild organiser': (22, 30),
    'Eel-smoker': (13, 29), 'Lock-keeper': (43, 20), 'Meridian surveyor': (36, 36),
    'Child with a toy boat': (17, 41), 'Old whaler': (55, 34), 'Gull': (46, 36),
    'HiddenItem': (57, 43), 'Item': (6, 48), 'Teo': (29, 31),
}
EBBMOUTH_OVERLAY_COORDS = [
    (21, 29), (26, 39), (30, 4), (27, 37), (51, 36), (28, 39), (29, 41), (46, 34),
    (29, 42), (45, 37), (7, 21),
]


def build_ebbmouth_160(prev=False):
    """Ebbmouth (160) — Unified with Wave 6 Tidelock weathered harbour stone, iron railings,
    timber boardwalks, curved rocky cove shoreline, Kristiline conifers & warm beacons!"""
    import rimewood as RW
    from rimewood import snowmap, apron, doorstep, smooth, npc, sign, item, signboard, head, over_tiles, bridges, \
        dress_ice, road_tracks, drifts, reed_beds, lagoon
    import ebbmouth as EB

    W, H = 60, 54
    TOW = (28, 31)
    CONN160 = [{'dir': 'S', 'offset': 22, 'to': 561, 'to_offset': 12}, {'dir': 'N', 'offset': 0, 'to': 167, 'to_offset': 0}]

    def river_x(y, base=34.5, amp=1.4, per=7.0):
        return base + amp * math.sin(y / per)

    m = snowmap(W, H, 160)

    # ---- 1. Sculpted Organic Tidal River, Rocky Cove Harbour Basin & Shallow/Deep Banding ----
    for y in range(0, 40):
        c = river_x(y)
        for x in range(int(c - 2.6), int(c + 3.4)):
            m.cls[y, x] = 'W'
    # Keep (31, 0) water so N seam [28, 29, 30] matches Map 167 100%!
    m.cls[0, 31] = 'W'

    # Organic curved harbour cove (ZERO ruler-straight horizontal seawall!)
    m.blob(44, 42.5, 14.2, 4.8, 'W', seed=161, rough=0.45)
    m.blob(38, 40.5, 5.5, 2.8, 'W', seed=169, rough=0.40)
    m.blob(51, 41.0, 5.2, 2.4, 'W', seed=173, rough=0.40)
    for y in range(44, H):
        for x in range(W):
            coast = 27.5 + 2.8 * math.sin(y / 3.5) + 2.5 * vnoise(0, y, 162, 5.0) - (y - 44) * 0.15
            if x >= coast:
                m.cls[y, x] = 'W'
    # Carve organic rocky coastal cove & sea-ice pack floes in SE
    for y in range(45, H):
        for x in range(45, W):
            if m.cls[y, x] == 'W' and x >= 49 + 2.8 * vnoise(0, y, 163, 4.0) - (y - 45) * 0.45:
                m.cls[y, x] = 'o'
    lagoon(m, 0.58, seed=164)
    # Add natural frozen sea-ice melt pond tucked cleanly in SE cove (x=52..57, y=47..51)
    m.blob(54.5, 49.5, 3.2, 2.0, 'p', seed=188, only='o.', rough=0.35)

    # ---- 2. Upper Town Terrace & Dense Interlocking Nordic Forest Rim ----
    for y in range(H):
        for x in range(W):
            if x <= 25 + 1.5 * vnoise(0, y, 165, 4.0) and y <= 12 + 1.2 * vnoise(x, 0, 166, 5.0):
                m.ht[y, x] = 1
    for y in range(H):
        for x in range(W):
            if m.cls[y, x] != '.':
                continue
            west = x <= 1 + 1.5 * vnoise(0, y, 167, 4.0) and 13 < y < 44
            north = y <= 1 + 1.2 * vnoise(x, 0, 168, 4.0) and not (TOW[0] <= x <= TOW[1])
            ne = x >= 50 + 3 * vnoise(0, y, 169, 5.0) and y <= 14 - 3 * vnoise(x, 0, 170, 5.0)
            east = x >= W - 2 - 1.5 * vnoise(0, y, 171, 4.0) and y < 36
            sw = x <= 4 + 6 * vnoise(0, y, 172, 6.0) and y >= 44
            if west or north or ne or east or sw:
                m.cls[y, x] = 'T'

    # Frosted fern tundra pockets breaking up bare white snow expanses!
    for cx, cy, rx, ry in ((2, 13, 2.5, 1.5), (19, 44, 2.8, 1.6), (11, 50, 3.5, 2.2),
                           (41, 24, 2.8, 1.8), (54, 17, 2.8, 1.8), (38, 6, 2.0, 2.0)):
        m.blob(cx, cy, rx, ry, 't', seed=cx + cy, only='.', rough=0.6)

    # ---- 3. Stairs & Curved Packed-Snow / Slush Lanes ----
    m.stairs(19, 12, w=3, kit_rows=4)
    m.plan_cliffs()
    m.rect(TOW[0], 0, 3, 18, 'd', only='.T')  # cols 28..30 match Map 167!
    m.rect(31, 1, 1, 17, 'd', only='.T')
    m.lane([(29.5, 17), (27, 22), (22, 26)], 'd', 2.6, seed=71, wobble=0.4)
    m.lane([(4, 9), (12, 10.2), (20, 10.6), (24, 9.6)], 'd', 2.2, seed=72, wobble=0.4)
    m.lane([(20.5, 16), (20, 21), (19, 26)], 'd', 2.4, seed=73, wobble=0.4)
    m.blob(15, 27.5, 9.5, 4.0, 'd', seed=74, rough=0.35, only='.T')
    m.lane([(6, 24), (12, 26.5)], 'd', 2.2, seed=75, wobble=0.3)
    m.lane([(23, 29), (29, 29.5), (33, 29.5)], 'd', 3.0, seed=76, wobble=0.0, only='.T')
    m.lane([(38, 29.5), (44, 30), (50, 32), (55, 35)], 'd', 2.8, seed=77, wobble=0.4)
    m.lane([(42, 18.5), (45, 22), (44, 29)], 'd', 2.4, seed=78, wobble=0.4)
    m.lane([(40, 15.5), (46, 15.5), (52, 16.5)], 'd', 2.4, seed=82, wobble=0.2)
    m.lane([(15, 31), (16, 36), (21, 40), (21.5, 46), (21.5, 54)], 'd', 3.4, seed=79, wobble=0.3)
    m.lane([(6, 36), (12, 37.5), (17, 37)], 'd', 2.2, seed=80, wobble=0.3)
    m.lane([(24, 37.5), (29, 38.5)], 'd', 2.4, seed=81, wobble=0.2)
    m.rect(20, 50, 4, 4, 'd', only='.T')
    smooth(m, 'd', into='.', passes=1)
    # Quays round the basin & curved stone breakwater out to the headland light
    for y in range(32, 40):
        for x in range(36, W):
            if m.cls[y, x] in '.T' and any(m.inb(x + dx, y + dy) and m.cls[y + dy, x + dx] == 'W'
                                           for dx in (-1, 0, 1) for dy in (-1, 0, 1, 2)):
                m.cls[y, x] = 'd'
    for x, y in [(57, 38), (56, 40), (55, 42), (53, 44), (51, 45), (49, 46)]:
        for dx in (0, 1, 2):
            for dy in (0, 1):
                if m.inb(x + dx, y + dy):
                    m.cls[y + dy, x + dx] = 'd'
    for x in range(55, W):
        for y in range(36, 39):
            m.cls[y, x] = 'd'

    # ---- 4. Buildings (100% Exact HEAD Coordinates & Doors!) ----
    d = {}
    d['reyes'] = m.stamp('wb_short', 3, 3, 'EB_REYES', 'Reyes House door')
    d['house'] = m.stamp('wb_hut', 12, 4, 'EB_HOUSE', "Net-mender's House door")
    d['pc'] = m.stamp('wb_pc', 3, 15, 'EB_PC', 'Poke Center door')
    d['mart'] = m.stamp('wb_long2', 12, 16, 'EB_MART', 'Mart door')
    d['angler'] = m.stamp('wb_long3', 2, 30, 'EB_ANGLER', "Anglers' Guild door")
    m.stamp('wb_inn', 22, 20, None, 'x')
    d['gym'] = m.stamp('wb_inn', 40, 8, 'EB_GYM', 'Tidelock Gym door')
    d['loft'] = m.stamp('wb_long3', 45, 21, 'EB_NETLOFT', 'Net Loft door')
    m.stamp('wb_smoke', 4, 38, None, 'x')
    m.stamp('wb_short', 39, 1, None, 'x')
    m.stamp('wb_hut', 25, 32, None, 'x')
    m.events = [e for e in m.events if e.get('name') != 'x']
    for k, (dx, dy) in d.items():
        doorstep(m, (dx, dy))
        apron(m, (dx, dy))
    # Rich coastal mud/gravel aprons under the west market stalls & cranes (taming blank white snow!)
    m.blob(14, 28, 5.5, 2.6, 'e', seed=165, only='d.', rough=0.35)
    m.blob(48, 35, 6.0, 1.8, 'e', seed=166, only='d.', rough=0.35)

    # ---- 5. Exact HEAD Events (ALL 28 spec events + 8 trial_overlay coords locked!) ----
    obj = EB.obj
    E = [
        sign(EBBMOUTH_HEAD_EVENTS['Gym sign'], 'Gym sign', "TIDELOCK GYM\nWarden: Marisol Reyes - The Ebb runs both ways."),
        sign(EBBMOUTH_HEAD_EVENTS['Town sign'], 'Town sign', "EBBMOUTH\nWhere the Ebb meets the sea. Southern port of Isenmar."),
        sign(EBBMOUTH_HEAD_EVENTS['Lattice sign'], 'Lattice sign', "MERIDIAN TIDAL LATTICE - UNIT 2\nPowering Isenmar's future. Keep off the intake."),
        sign(EBBMOUTH_HEAD_EVENTS['Towpath sign'], 'Towpath sign', "THE TOWPATH - up the Ebb to the Mill Quay. Mind the ropes: the river pulls both ways."),
        sign(EBBMOUTH_HEAD_EVENTS['PC sign'], 'PC sign', "POKEMON CENTER"),
        obj(EBBMOUTH_HEAD_EVENTS['Upper mill'], 'Upper mill', ["The Upper Mill's wheel turns, stops dead, and turns again. The miller's boy counts under his breath: 'nine... ten... go on, go on...'"]),
        obj(EBBMOUTH_HEAD_EVENTS['Guild mill'], 'Guild mill', ["The Guild Mill. Its race runs past Meridian's brass intake. When the river stutters the wheel freezes mid-turn and the whole quay holds its breath."]),
        obj(EBBMOUTH_HEAD_EVENTS['Harbour mast'], 'Harbour mast', ["A whaler's mast at the quay, its yard hung with nets. Gulls have opinions about it."]),
        npc(EBBMOUTH_HEAD_EVENTS['Ice-fisher'], 'Ice-fisher', 'trainer_FISHERMAN', ["♪ Sleep, old whale, under the ice... When the whale wakes, the sea remembers it's a sea. ♪"], d='up'),
        npc(EBBMOUTH_HEAD_EVENTS['Guild striker'], 'Guild striker', 'NPC 03', ["Ebb Guild: Thane Eirik taxes our catch, Meridian lays us off. And the river stops dead for minutes now!"], move='random'),
        npc(EBBMOUTH_HEAD_EVENTS['Dockworker'], 'Dockworker', 'trainer_SAILOR', ["Watch the mill-wheels. When the Ebb stutters they freeze mid-turn and we all hold our breath."], d='left'),
        npc(EBBMOUTH_HEAD_EVENTS['Guild organiser'], 'Guild organiser', 'NPC 27', ["Guild organiser: Strike vote's at the bell. Marisol says she's 'neutral'. Marisol has never been neutral about anything in her life."]),
        npc(EBBMOUTH_HEAD_EVENTS['Eel-smoker'], 'Eel-smoker', 'NPC 20', ["Smoked eel! Smoked char! Smoked anything you hold still long enough!", "The Warden buys two every night after a gym fight. Win or lose. Mostly win."]),
        npc(EBBMOUTH_HEAD_EVENTS['Lock-keeper'], 'Lock-keeper', 'NPC 25', ["Lock-keeper: The Tidelock lifts boats up the Ebb when the tide's in and lets them down when it's out.",
                                                                          "Lately the river doesn't know which it is. Neither do the gates."], d='down'),
        npc(EBBMOUTH_HEAD_EVENTS['Meridian surveyor'], 'Meridian surveyor', 'NPC 12', ["Meridian surveyor: The stutters are within tolerance. Everything is within tolerance. Please stop asking."], d='left'),
        npc(EBBMOUTH_HEAD_EVENTS['Child with a toy boat'], 'Child with a toy boat', 'NPC 07', ["I race my boat down the race! When the river stops, it stops too. Then it's a draw."], move='random'),
        npc(EBBMOUTH_HEAD_EVENTS['Old whaler'], 'Old whaler', 'NPC 28', ["Forty winters on the ice. You don't hear the sea under it. You FEEL it. Lately it's been turning over in its sleep."], d='down'),
        {'type': 'npc', 'name': 'Gull', 'at': list(EBBMOUTH_HEAD_EVENTS['Gull']), 'sprite': 'Followers/WINGULL', 'dir': 'left', 'move': 'random', 'text': '(Kyaa! It eyes your bag.)'},
        item(EBBMOUTH_HEAD_EVENTS['HiddenItem'], 'NETBALL', True),
        item(EBBMOUTH_HEAD_EVENTS['Item'], 'FRESHWATER'),
        dict(EB.OLD160_TEO, at=list(EBBMOUTH_HEAD_EVENTS['Teo'])),
    ]
    for e in E:
        x, y = e['at']
        m.taken[y, x] = True
        if m.cls[y, x] in 'wWoT':
            m.cls[y, x] = 'd'
        if e['type'] == 'sign':
            signboard(m, e)
    m.events = [e for e in m.events if e['type'] == 'door'] + E

    door_steps = [(dx, dy + 1) for dx, dy in d.values()]
    all_ev_pts = [tuple(e['at']) for e in m.events] + EBBMOUTH_OVERLAY_COORDS + door_steps
    prot_strict = reserve_mask(m, all_ev_pts, pad=0)
    prot_wide = reserve_mask(m, all_ev_pts, pad=1)
    for x, y in EBBMOUTH_OVERLAY_COORDS + door_steps:
        if m.inb(x, y):
            m.taken[y, x] = True
            if m.cls[y, x] in 'wWoT':
                m.cls[y, x] = 'd'

    # ---- 6. Wave 6 Unified Harbour Hardware: Beacons, Iron Quay Railings, Net Racks, Cranes, Stalls ----
    # Forged iron quay railings (matching Tidelock Gym 170-174!) along the fish quay & river banks!
    paint_rail_run(m, 39, 44, 37, kind='qy', gaps=(42,))
    paint_rail_run(m, 41, 44, 15, kind='qy')
    paint_rail_run(m, 49, 53, 15, kind='qy')
    # Iron mooring bollards along riverfront & fish harbour quay
    for bx, by in ((38, 37), (45, 37), (48, 37), (54, 37), (56, 38), (30, 15), (30, 18), (38, 15), (38, 18), (31, 27), (38, 27)):
        if m.inb(bx, by) and not prot_strict[by, bx] and not m.taken[by, bx] and m.cls[by, bx] in '.de':
            m.over.append((1, bx, by, P1('hb_bollard0' if bx % 2 else 'hb_bollard1')))
            m.taken[by, bx] = True

    beacon_pts = []
    lamp_pts = []
    # Blazing Wave 6 coastal harbour beacons flanking Tidelock Gym, Market Bridge & Breakwater!
    for bx, by in ((42, 13), (50, 13), (38, 31), (52, 43), (18, 25)):
        res = put_safe(m, 'pf_beacon', bx, by, on='.de', r=1, prot=prot_wide)
        if res:
            beacon_pts.append((res[0] + 1, res[1] + 1))

    # Smoked-eel market, net-drying racks, harbour cranes, fish tubs, whalebones & dock freight
    for nm, x, y in (
        ('fw_stall_i', 10, 25), ('fw_stall_e', 14, 25), ('fw_stall_i', 18, 26), ('fw_stall_e', 9, 29),
        ('fw_rack', 12, 31), ('fw_rack', 15, 31), ('pf_p_net', 40, 27), ('pf_p_net', 55, 29),
        ('pf_logbench', 17, 30), ('fw_brazier', 21, 27), ('fw_brazier', 8, 27), ('fw_brazier', 31, 26),
        ('fw_brazier', 42, 27), ('fw_brazier', 48, 17), ('fw_wood', 22, 31), ('sh_crates', 31, 20),
        ('fw_sled', 24, 27), ('hb_crane', 47, 31), ('hb_crane', 54, 33), ('hb_crates4', 50, 34),
        ('hb_barrels', 41, 33), ('hb_tubs', 44, 34), ('hb_rope', 57, 35), ('hb_rope', 43, 36),
        ('hb_rope', 30, 14), ('pf_whalebone', 39, 15), ('pf_whalebone', 52, 15), ('pf_whalebone', 15, 45),
        ('hb_banner', 44, 14), ('hb_banner', 48, 14), ('wr_sacks', 40, 35), ('wr_sacks', 46, 33),
        ('fw_rack', 6, 44), ('fw_rack', 9, 44), ('fw_wood', 13, 43), ('fw_skull', 16, 44),
        ('fw_boat_over', 10, 47), ('sh_crates', 26, 11), ('fw_wood', 8, 10), ('fw_sled', 16, 9),
        ('hb_barrel', 43, 18), ('hb_cask', 50, 18), ('fw_boat_over', 25, 47), ('fw_rack', 17, 48),
        ('fw_rack', 25, 50), ('fw_skull', 13, 51), ('hb_rope', 24, 44), ('fw_wood', 18, 45),
        ('ak_rock2', 11, 47), ('ak_boulder', 27, 52), ('fw_sled', 15, 46), ('hb_barrel', 26, 45),
        ('fw_wood', 14, 15), ('sh_crates', 17, 4),
    ):
        res = put_safe(m, nm, x, y, on='.de', r=2, prot=prot_wide)
        if res and nm == 'fw_brazier':
            beacon_pts.append((res[0], res[1]))

    # Harbour tall lamps & breakwater light
    for nm, x, y in (('pf_wlamp', 49, 45), ('pf_wlamp', 25, 41), ('pf_wlamp', 39, 34), ('pf_wlamp', 54, 35),
                     ('pf_lantern', 23, 15), ('pf_lantern', 12, 23), ('pf_lantern', 27, 29),
                     ('pf_lantern', 40, 28), ('pf_lantern', 52, 29), ('pf_lantern', 18, 36),
                     ('pf_lantern', 23, 45), ('pf_lantern', 10, 12), ('pf_lantern', 31, 8), ('pf_lantern', 46, 19)):
        res = put_safe(m, nm, x, y, on='.de', r=2, prot=prot_wide)
        if res:
            lamp_pts.append((res[0], res[1] + 1))

    # ---- 7. Multi-Species Overlapping Nordic Conifer Clusters (ZERO lone grey snow stickers!) ----
    snow_groves = [
        (22, 5, 4, 2.5, True),    # NE of Net-mender overlooking the river
        (2, 24, 3, 2.2, False),   # West flank above Anglers' Guild
        (13, 41, 4, 2.4, True),   # Mid-SW snow woods
        (8, 50, 5, 2.8, True),    # SW coastal cliff pines
        (55, 19, 4, 2.6, True),   # East bluff behind Net Loft & Gym
        (41, 24, 3, 2.2, False),  # East bank pines above Market Bridge
        (56, 30, 3, 2.2, False),  # Far-east quay pines
        (18, 4, 3, 2.0, False),   # North terrace crest
    ]
    for idx, (cx, cy, cnt, rad, hero) in enumerate(snow_groves):
        place_snow_grove(m, cx, cy, count=cnt, radius=rad, on='.t', seed=idx + 30, hero=hero, prot=prot_wide)

    m.greenfill(3)

    # ---- 8. Paint + Wave 6 Weathered Harbour Stonework, Timber Boardwalks, Rocky Islets & Glows ----
    m.paint()

    # Frosted harbour limestone forecourt & weathered maritime timber boardwalks harmonizing with snowy Ebbmouth!
    frost_stone = [P1('lm_pave%d' % i) for i in range(4)]
    paint_plaza_stone(m, 41, 14, 51, 16, P1('lm_pave0'), frost_stone, on_cls='de.', skip_coords=[(46, 13)])
    # Weathered maritime timber boardwalks along Fish Quay, Mill Quay & Market Walk (zero harsh black slabs!)
    paint_boardwalk_strip(m, 40, 35, 55, 36, style='ak', on_cls='de.')
    paint_boardwalk_strip(m, 28, 1, 31, 17, style='ak', on_cls='d.')
    paint_boardwalk_strip(m, 26, 36, 29, 40, style='ak', on_cls='de')
    paint_boardwalk_strip(m, 9, 28, 20, 29, style='ak', on_cls='de')

    # Market Bridge & Tidelock Gate Footway + sluices + mill-wheels + Meridian intake
    bridges(m, ((28, 30),), cls='W')
    bridges(m, ((16, 17),), cls='W')
    for x in range(m.W):
        for y in (15, 18):
            if m.cls[y, x] == 'W' and m.cls[y - 1 if y == 15 else y + 1, x] == 'W' and (x % 2 == 0):
                over_tiles(m, 'df_sluice', x, y - 1 if y == 15 else y, z=2)
    over_tiles(m, 'eb_wheel0', int(river_x(4)) - 1, 2, z=2)
    over_tiles(m, 'eb_wheel1', int(river_x(33)) - 2, 32, z=2)
    over_tiles(m, 'eb_intake', 26, 37)

    # Rocky cove islets & boulders anchored along the harbour shoreline & breakwater (ZERO sterile empty pool!)
    for nm, x, y in (('ak_rock2', 31, 47), ('ak_rock2', 42, 49), ('nt_boulder', 35, 38), ('nt_boulder', 48, 44),
                     ('nt_boulder', 54, 41), ('nt_boulder', 30, 44), ('nt_boulder', 45, 48)):
        L = np.array(STAMPS[nm]['layers'])
        h, w = L.shape[1:]
        if x + w <= W and y + h <= H and all(m.cls[y + j, x + i] in 'wW' and m.L[2, y + j, x + i] == 0 for i in range(w) for j in range(h)):
            for j in range(h):
                for i in range(w):
                    t = int(L[:, j, i].max())
                    if t:
                        m.L[2, y + j, x + i] = t

    # Moored fishing boats & buoys in the harbour basin
    for nm, x, y in (('hb_boat1', 40, 39), ('hb_boat3', 46, 41), ('fw_boat', 33, 41), ('hb_boat2', 51, 39),
                     ('fw_boat', 37, 45), ('hb_boat4', 42, 44), ('hb_buoy', 39, 42), ('hb_buoy', 49, 43)):
        L = np.array(STAMPS[nm]['layers'])
        if all(m.inb(x + i, y + j) and m.cls[y + j, x + i] in 'wW' and m.L[2, y + j, x + i] == 0
               for i in range(L.shape[2]) for j in range(L.shape[1])):
            for j in range(L.shape[1]):
                for i in range(L.shape[2]):
                    t = int(L[:, j, i].max())
                    if t:
                        m.L[2, y + j, x + i] = t

    for y, x in np.argwhere(np.isin(m.cls, ['i', 'I'])):
        m.L[0, y, x] = RW.ice_at(x, y)
    dress_ice(m, 0.28, seed=160)
    reed_beds(m, 14, seed=160)
    for nm, x, y in (('fw_smoke_w', 6, 36), ('fw_smoke_w', 24, 18), ('fw_smoke_w', 6, 1), ('fw_smoke_w', 43, 4), ('fw_smoke_w', 50, 19)):
        over_tiles(m, nm, x, y)

    # Overhead harbour lantern strings, warm amber beacon/lantern glows & dark-fjord water glints!
    add_festoon_strings(m, [(41, 51, 15, 0), (39, 53, 35, 1), (10, 20, 27, 2)], kind='lstring')
    add_warm_glows(m, lamp_pts + beacon_pts + [(46, 14), (35, 29), (35, 16), (50, 45)])
    add_water_glints(m, water_cls='wW', seed=160, density=0.03)

    m.scatter(6, seed=160)
    road_tracks(m, 0.10, seed=160)
    drifts(m, 0.08, seed=160)
    m.seal_against(CONN160, spans=[('S', 20, 4), ('N', TOW[0], 3)],
                   keep=[tuple(e['at']) for e in m.events if e.get('type') == 'warp'])
    seal_unconnected_edges(
        m,
        open_cells=[(x, H - 1) for x in range(20, 24)] +
                   [(x, 0) for x in range(TOW[0], TOW[0] + 3)] +
                   [tuple(e['at']) for e in m.events if e.get('type') == 'warp'],
        filler=10371,
    )
    if prev:
        m.preview('/tmp/craft/e160.png', 0.5)
    m.write(160, head(160, 'Ebbmouth', biome='village', bgm='Lerucean Town',
                      metadata={'Outdoor': True, 'ShowArea': True, 'MapPosition': [0, 8, 20], 'BattleBack': 'field', 'Weather': ['Rain', 30]},
                      tone=[-6, -4, 6, 18],
                      fog={'name': 'prismfall_seamist', 'opacity': 40, 'blend': 0, 'zoom': 100, 'sx': 1, 'sy': 0},
                      connections=CONN160, _file='160_ebbmouth.yaml'),
            '# Ebbmouth (160). WRITTEN BY layouts/ebbmouth.py (Wave 10 Rejuv V14 Craft) - edit wave10_towns_craft.py.\n'
            '# The old stock-palette version is layouts/old_160_ebbmouth.yaml.\n')
    print('160 Ebbmouth doors', d)
    return m


# ================================================================================================
# TOWN 4: 180 LUMEN CITY — THE CONCOURSE (96x72, ts 60 PF Rejuv Lumen)
# ================================================================================================

LUMEN_180_OVERLAY_COORDS = [(30, 29), (73, 37), (73, 39), (25, 46)]


def enhance_lumen_180_pre(m):
    """Pre-paint Rejuv V14 urban grandeur enhancements for 180 Lumen City - The Concourse.
    Called inside `lumen.build_180()` right after events are seated and before `m.paint()`."""
    # Protect ALL events + trial_overlay coords so ZERO events ever shift or get blocked!
    ev_pts = [tuple(e['at']) for e in m.events] + LUMEN_180_OVERLAY_COORDS
    for ex, ey in ev_pts:
        m.keep_clear.add((ex, ey))
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            m.keep_clear.add((ex + dx, ey + dy))

    # 1. Twin Shimmering Marble-Rimmed Reflecting Pools nested inside the 2 Northern Prism Plaza Parterres!
    for rx, ry in ((32, 14), (53, 14)):
        for dx in range(4):
            m.cls[ry, rx + dx] = 'w'
    # Ornamental reflecting water channels nested inside Meridian Spire Forecourt parterres!
    for bx in (76, 90):
        for py in (19, 20, 23, 24):
            if not m.taken[py, bx]:
                m.cls[py, bx] = 'w'

    # 2. Lush Botanical Flowering Azalea & Shrub Clusters in the Plaza & South Esplanade Gardens!
    for nm, x, y in (
        ('nt_azalea0', 32, 25), ('nt_azalea1', 35, 26), ('nt_azalea2', 55, 25), ('nt_azalea0', 57, 26),
        ('nt_shrub0', 31, 26), ('nt_shrub1', 54, 26),
        ('nt_azalea1', 75, 16), ('nt_azalea2', 89, 16), ('nt_azalea0', 75, 26), ('nt_azalea1', 89, 26),
    ):
        if m.free(x, y, STAMPS[nm]['w'], STAMPS[nm]['h'], on='.'):
            m.stamp(nm, x, y)
    # Cluster lush flowering shrubs beside every South Esplanade tree (destroying polka-dot uniformity!)
    for i, x in enumerate(range(4, 80, 9)):
        nm = ['nt_azalea0', 'nt_azalea1', 'nt_azalea2', 'nt_shrub0', 'nt_shrub1'][i % 5]
        if m.free(x, 60, 2, 2, on='.'):
            m.stamp(nm, x, 60)

    # 3. Storefront Awnings, Café Terraces, Planters & Urban Street Furniture on Market St, North Ave & East Terrace!
    # Colorful storefront awnings overhanging open shopfront paving (pri=2 or clean Layer 2)
    awning = STAMPS['pf_p_awning']
    for ax, ay in ((20, 46), (34, 46), (39, 46), (50, 46), (67, 46), (22, 57), (45, 57),
                   (29, 18), (59, 18), (10, 23)):
        if all(m.inb(ax + i, ay) and not m.taken[ay, ax + i] and (ax + i, ay) not in m.keep_clear for i in range(3)):
            for i in range(3):
                t = max(awning['layers'][z][0][i] for z in range(3))
                if t:
                    m.over.append((2, ax + i, ay, t))

    # Richer East Lowlight Transit Overlook furniture (x=84..95, y=38..62 — zero dead empty slab!)
    for nm, x, y in (
        ('lm_bench', 85, 43), ('lm_bench', 91, 43), ('lm_kiosk', 84, 50), ('lm_planter', 84, 46),
        ('lm_planter', 91, 46), ('lm_holo', 93, 52), ('lm_bench', 90, 58), ('lm_planter', 89, 60),
        ('pf_planter0', 85, 38), ('pf_planter1', 89, 38),
        # Extra Prism Plaza & Spire Forecourt planters, statues & café seating
        ('pf_planter0', 42, 12), ('pf_planter1', 48, 12), ('pf_planter2', 42, 25), ('pf_planter3', 48, 25),
        ('lm_planter3', 31, 10), ('lm_planter3', 55, 10), ('lm_planter3', 44, 31),
        ('lm_bench', 41, 23), ('lm_bench', 50, 23), ('lm_bench', 79, 20), ('lm_bench', 89, 14),
        ('lm_topiary', 82, 13), ('lm_topiary', 88, 13), ('lm_topiary', 82, 31), ('lm_topiary', 88, 31),
        ('lm_statue', 90, 29), ('lm_bannerlamp', 42, 10), ('lm_bannerlamp', 50, 10),
        # Gym Square circuit flair
        ('lm_planter', 11, 26), ('lm_planter', 17, 26), ('lm_bannerlamp', 12, 23), ('lm_bannerlamp', 17, 23),
    ):
        m.try_put(nm, x, y, on='pq')

    # 4. Dramatic Abyssal Nadir Skyline Landmarks (Towering Spire Pylons, Induction Rings & Steam in Void!)
    def abyss_piece(name, x, y):
        st = STAMPS[name]
        for dy in range(st['h']):
            for dx in range(st['w']):
                for z in (1, 2):
                    t = st['layers'][z][dy][dx]
                    if t and m.inb(x + dx, y + dy):
                        m.over.append((z, x + dx, y + dy, t))

    for py in (4, 15, 27, 39):
        abyss_piece('lm_pylon', 94, py)
    for ry in (10, 22, 34):
        abyss_piece('lm_ring', 94, ry)
    for px in (6, 20, 35, 50, 65, 80, 92):
        abyss_piece('lm_pylon', px, 67)
    for rx in (13, 28, 43, 58, 73, 87):
        abyss_piece('lm_ring', rx, 65)
    for sx in (16, 46, 76):
        abyss_piece('lm_steam0', sx, 64)


def enhance_lumen_180_post(m):
    """Post-paint Rejuv V14 floor patterning, marble/obsidian contrast, tram crosswalks, rooftop details
    & warm glowing streetlamp halos for 180 Lumen City - The Concourse."""
    pave_ids = {P1('lm_pave%d' % i) for i in range(8)}
    plaza_ids = {P1('lm_plaza0'), P1('lm_plaza1')}
    road_ids = {P1('lm_road0'), P1('lm_road1')}
    base_walk = {0} | pave_ids | plaza_ids | road_ids
    inlay_ids = {P1('lm_inlay_' + k) for k in ('h', 'v', 'x', 'ne', 'nw', 'se', 'sw')}
    carpet_ids = {P1('lm_carpet_' + k) for k in ('c', 'n', 's', 'w', 'e', 'nw', 'ne', 'sw', 'se')}
    keep_surf = inlay_ids | carpet_ids | {P1('lm_grate'), P1('lm_grate_off')}
    trim0, trim1 = P1('lm_pave0'), P1('lm_pave2')
    low0, low1 = P1('lm_low0'), P1('lm_low1')
    p0, p1 = P1('lm_plaza0'), P1('lm_plaza1')
    gr = P1('lm_grate')

    def set_floor(x, y, t):
        if not m.inb(x, y) or m.cliff[y, x] or m.cls[y, x] not in 'pqr':
            return
        if m.L[0, y, x] in keep_surf or m.L[1, y, x] in keep_surf:
            return
        m.L[0, y, x] = t
        if m.L[1, y, x] in base_walk:
            m.L[1, y, x] = t

    # 1. Refined Limestone Promenade Frame & Checker Medallions across Prism Plaza (28..64, 10..31)!
    for x in range(28, 65):
        set_floor(x, 10, trim0); set_floor(x, 31, trim0)
    for y in range(10, 32):
        set_floor(28, y, trim0); set_floor(64, y, trim0)
    # Subtle warm limestone frame bordering the Central Fountain + Sunburst + Founders Monument Spine
    for y in range(12, 30):
        set_floor(41, y, trim0 if y % 2 == 0 else trim1)
        set_floor(50, y, trim0 if y % 2 == 0 else trim1)
    for x in range(41, 51):
        set_floor(x, 12, trim0); set_floor(x, 29, trim0)
    # Subtle checkered marble inlays in the wide E/W plaza quadrants (31..39 & 52..61, y=18..24)
    for y in range(18, 25):
        for x in list(range(31, 40)) + list(range(52, 62)):
            if (x + y) % 2 == 0 and m.cls[y, x] == 'q':
                set_floor(x, y, P1('lm_pave%d' % ((x + y) % 4)))

    # 2. Meridian Spire Imperial Forecourt (73..92, 13..31): Refined Limestone Border + Checker Esplanade!
    for y in range(13, 32):
        set_floor(83, y, trim0); set_floor(87, y, trim0)
        set_floor(73, y, trim0); set_floor(92, y, trim0)
    for x in range(73, 93):
        set_floor(x, 13, trim0); set_floor(x, 31, trim0)
    for y in range(14, 31):
        for x in range(78, 83):
            if (x + y) % 2 == 0:
                set_floor(x, y, P1('lm_pave0'))

    # 3. Boulevard Curb Runners & Crisp Marble Zebra Crosswalks across the Tram Boulevard (y=33..36)!
    for x in range(0, 84):
        if x not in (16, 17, 18, 63, 64, 65):
            set_floor(x, 8, low0 if x % 2 == 0 else low1)       # North Ave dark slate center strip
            set_floor(x, 47, low0 if x % 2 == 0 else low1)      # Market Street dark slate median
            set_floor(x, 58, low0 if x % 2 == 0 else low1)      # South Walk promenade trim
    for cx0 in (14, 45, 63, 78):
        for dx in range(3):
            for y in (33, 35, 36):
                if (cx0 + dx, y) not in m.tracks:
                    set_floor(cx0 + dx, y, p0 if (dx % 2 == 0) else p1)
    # Gym Square limestone-bordered Circuit Court (9..19, 23..31)
    for x in range(9, 20):
        set_floor(x, 23, trim0); set_floor(x, 31, trim0)
    for y in range(23, 32):
        set_floor(9, y, trim0); set_floor(19, y, trim0)

    # 4. East Lowlight Transit Terrace (84..95, 38..62): Slate Border + Steam Drainage Grates!
    for y in range(38, 47):
        set_floor(84, y, low0); set_floor(92, y, low0)
    for y in range(51, 63):
        set_floor(84, y, low0); set_floor(95, y, low0)
    for x in range(84, 96):
        set_floor(x, 51, low0); set_floor(x, 62, low0)
    for gx, gy in ((86, 53), (87, 53), (88, 53), (90, 53), (88, 56), (91, 56), (88, 59)):
        if (gx, gy) not in m.keep_clear:
            set_floor(gx, gy, gr)

    # 5. Rooftop Skylight & Vent Details breaking up flat uniform roof blocks!
    rng_r = random.Random(1809)
    for y in range(0, 56):
        for x in range(0, 84):
            if m.cls[y, x] == 'f' and m.L[1, y, x] == 0 and rng_r.random() < 0.05:
                m.L[1, y, x] = P1('lm_grate_off')

    # 6. Warm Golden Streetlamp, Fountain, Spire & Nadir Overlook Glow Halos (pf_glow)!
    glow_pts = [
        # Prism Plaza Fountain, Sunburst & Monument lamps
        (46, 15), (46, 22), (46, 27), (41, 13), (50, 13), (41, 19), (50, 19),
        (38, 24), (53, 24), (30, 11), (63, 11), (30, 30), (63, 30),
        # Meridian Spire Gala Carpet & Entrance
        (85, 13), (82, 16), (88, 16), (82, 24), (88, 24), (85, 29),
        # Gym Square & Market Street Landmarks (PC, Arcade, Cycles, Lab, West Gate)
        (14, 23), (13, 26), (25, 46), (40, 46), (53, 46), (5, 57), (25, 57),
        # East Lowlight Stairs & Terrace + Nadir Abyss warm under-glow!
        (89, 47), (86, 55), (93, 55), (14, 65), (36, 65), (58, 65), (80, 65), (94, 22),
    ]
    add_warm_glows(m, glow_pts)
    add_water_glints(m, water_cls='w', seed=180, density=0.06)


# ================================================================================================
# TOWN 5: 280 VERDANCE — MARKET TERRACES (104x88, UPGRADED TO ts 55 PF Rejuv City!)
# ================================================================================================

def build_verdance_280():
    """Verdance - Market Terraces (280) — Complete Rejuvenation V14 royal terraced botanical capital
    on Tileset 55 (`PF Rejuv City`), seamlessly leading into Wave 5's `286`/`287` Briar Hall & `295` Cathedral!
    Preserves ALL 11 HEAD events, warps, links, and HealingSpot (50, 66) AND fixes the HEAD Briar Hall softlock!"""
    W, H = 104, 88
    m = K.RMap(W, H, 55, 280, water='Ocean', kit={1: 'rw', 2: 'rw', 'default': 'qy'})
    m.keep_under = 'cfdg'
    m.gv_dark = 0.52

    # ---- 1. Three Stepped Botanical Elevation Tiers + Sinuous Briarwater River ----
    # Tier 2 (ht=2): Upper Royal Thornhill Conservatory & Briar Hall Forecourt (NE, x=48..98, y=0..24)
    # Tier 1 (ht=1): Mid Noble Promenade & Botanical Switchback Terrace (NE/Mid, x=44..100, y=14..39)
    # Tier 0 (ht=0): Cathedral Close (NW), Briarwater Valley, Grand Market Terraces (SE), Rootward (SW)
    def river_y(x):
        return 51 + int(round(3.2 * math.sin(x / 15.0) + 1.8 * (vnoise(x, 0, 7, 9.0) - 0.5)))

    for y in range(H):
        for x in range(W):
            # Stepped botanical terraces with organic curving contours
            d1 = ((x - 73.0) / 30.0) ** 2 + ((y - 23.0) / 18.0) ** 2
            d2 = ((x - 73.0) / 22.0) ** 2 + ((y - 14.0) / 11.5) ** 2
            n1 = 0.25 * (vnoise(x, y, 5, 5.0) - 0.5)
            n2 = 0.22 * (vnoise(x, y, 6, 4.5) - 0.5)
            if (x >= 47 and y <= 39 and d1 <= 1.0 + n1) or (50 <= x <= 97 and y <= 24):
                m.ht[y, x] = 1
            if (50 <= x <= 97 and y <= 14) or (52 <= x <= 96 and y <= 24 and d2 <= 1.0 + n2):
                m.ht[y, x] = 2

    # Carve clean flat south-facing landings for the TWO Grand Royal Stone Staircases!
    # Stair 1 (Tier 0 -> Tier 1): x=57..61, lip at y=39 (5 wide, 3 rows: y=39..41)
    for x in range(55, 64):
        for y in range(36, 40):
            m.ht[y, x] = max(m.ht[y, x], 1)
        for y in range(40, 45):
            m.ht[y, x] = 0
    # Stair 2 (Tier 1 -> Tier 2): x=74..78, lip at y=24 (5 wide, 3 rows: y=24..26)
    for x in range(72, 81):
        for y in range(21, 25):
            m.ht[y, x] = 2
        for y in range(25, 31):
            m.ht[y, x] = 1
    # Ensure Briar Hall Forecourt (x=54..92, y=0..15) is cleanly level Tier 2
    for y in range(0, 16):
        for x in range(52, 95):
            m.ht[y, x] = 2

    # Carve the winding Briarwater River across the valley (y ~ 48..55, Tier 0)
    for x in range(W):
        ry = river_y(x)
        for y in range(ry - 2, ry + 3):
            if 0 <= y < H:
                m.ht[y, x] = 0
                m.cls[y, x] = 'w'
    # Deep water ribbon along the river center (avoiding bridge columns)
    for x in range(2, W - 2):
        if 42 <= x <= 47 or 60 <= x <= 65:
            continue
        ry = river_y(x)
        if 0 <= ry < H and m.cls[ry, x] == 'w':
            m.cls[ry, x] = 'W'

    # Dense interlocking emerald forest encircling Verdance's outer slopes & noble park ridges
    for y in range(H):
        for x in range(W):
            if m.cls[y, x] != '.':
                continue
            outer = (x < 4 or x > W - 5 or y < 3 or y > H - 5)
            # Keep Kingsgate approach (x=33..40, y=79..87) and Briar Hall crown (x=52..94, y=0..12) clear of border forest
            if 32 <= x <= 41 and y >= 78:
                outer = False
            if 51 <= x <= 95 and y <= 14:
                outer = False
            if outer:
                m.cls[y, x] = 'T'

    # ---- 2. Grand Royal Stone Staircases & Cliffs ----
    m.stairs(57, 39, w=5, kit_rows=3, kind='stone', c='f')
    m.stairs(74, 24, w=5, kit_rows=3, kind='stone', c='f')
    m.plan_cliffs(rows=3)

    # ---- 3. Royal Streets, Flagstone Plazas & Ceremonial Sightlines ----
    # Kingsway Entry (South Kingsgate -> Market Fork -> West Kingsway Bridge -> Cathedral & Thornhill!)
    m.rect(34, 77, 6, 11, 'c')
    m.lane([(36.5, 86), (36.5, 74), (39, 66), (44, 59), (44.5, 55)], c='c', w=4.0, seed=1, only='.tT', wobble=0.15)
    m.lane([(44.5, 48), (47, 45), (54, 44.5), (59, 43.5)], c='c', w=3.8, seed=2, only='.tT', wobble=0.15)
    m.rect(57, 42, 5, 3, 'f', only='.tTc')
    # Mid Botanical Terrace Switchback Promenade (Tier 1: Stair 1 top -> Noble Walk -> Stair 2 base!)
    m.rect(57, 36, 5, 3, 'f', only='.tTc')
    m.lane([(59.5, 36.5), (65, 33.5), (72, 31), (76.5, 29), (76.5, 27)], c='f', w=3.4, seed=3, only='.tT', wobble=0.12)
    m.lane([(50, 35.5), (58, 35.5), (70, 35.5), (84, 35), (94, 34)], c='c', w=2.8, seed=16, only='.tT', wobble=0.12)
    # Upper Royal Thornhill Conservatory Court (Tier 2: Stair 2 top -> Grand Palace Forecourt!)
    m.rect(74, 21, 5, 3, 'f', only='.tTc')
    m.lane([(76.5, 21.5), (74, 17), (71, 14)], c='f', w=3.4, seed=4, only='.tT', wobble=0.12)
    m.rect(62, 10, 19, 6, 'f', only='.tTc')  # Grand Briar Hall Palace Forecourt!
    m.lane([(55, 13.5), (62, 13.5), (81, 13.5), (90, 14)], c='c', w=2.6, seed=17, only='.tT', wobble=0.1)

    # Cathedral of the Evergreen Close & Sweeping Ceremonial Avenue (NW)
    m.rect(9, 25, 16, 6, 'f', only='.tTc')
    m.blob(18, 29, 10.5, 3.6, 'f', seed=5, rough=0.25, only='.tTc')
    m.lane([(21, 30), (30, 36), (39, 43), (44.5, 47)], c='f', w=3.6, seed=6, only='.tT', wobble=0.15)
    # West Burgher Lanes
    m.lane([(6, 39), (18, 39), (30, 39)], c='c', w=2.6, seed=7, only='.tT', wobble=0.1)
    m.lane([(6, 46), (20, 46), (34, 46), (43, 46)], c='c', w=2.8, seed=8, only='.tT', wobble=0.1)
    m.lane([(17, 39), (17, 46)], c='c', w=2.4, seed=21, only='.tT', wobble=0.1)

    # Grand Market Terraces Plaza (SE: Poke Center (50,65), Mart (70,60), Flower seller (58,70)!)
    m.blob(60, 69, 13.5, 6.5, 'f', seed=9, rough=0.3, only='.tTc')
    m.blob(72, 65, 8.5, 4.5, 'f', seed=10, rough=0.3, only='.tTc')
    m.rect(48, 65, 26, 8, 'f', only='.tTc')
    m.lane([(38, 69), (49, 69)], c='c', w=3.4, seed=12, only='.tT', wobble=0.1)
    m.lane([(74, 66), (86, 65), (97, 67)], c='c', w=3.2, seed=13, only='.tT', wobble=0.12)
    m.lane([(62.5, 63), (62.5, 56)], c='c', w=3.6, seed=14, only='.tT', wobble=0.1)
    m.lane([(62.5, 47), (60, 44)], c='c', w=3.4, seed=15, only='.tT', wobble=0.1)
    m.lane([(72, 75), (85, 75), (96, 74)], c='c', w=2.6, seed=18, only='.tT', wobble=0.1)
    m.lane([(85, 66), (85, 75)], c='c', w=2.4, seed=19, only='.tT', wobble=0.1)
    m.lane([(40, 76), (54, 76), (68, 76)], c='c', w=2.6, seed=20, only='.tT', wobble=0.1)

    # Rootward Old Quarter Alleys (SW: Rootward child (15, 66)!)
    m.lane([(6, 66), (18, 66), (34, 66)], c='c', w=2.8, seed=30, only='.tT', wobble=0.12)
    m.lane([(6, 75), (18, 75), (34, 75)], c='c', w=2.6, seed=31, only='.tT', wobble=0.12)
    m.lane([(12, 66), (12, 75)], c='c', w=2.4, seed=32, only='.tT', wobble=0.1)
    m.lane([(24, 66), (24, 75)], c='c', w=2.4, seed=33, only='.tT', wobble=0.1)

    for c in 'cf':
        m.smooth(c, into='.', passes=1, only='.tT')

    # Re-assert Briarwater river so streets NEVER ford the river outside the two grand bridges!
    for x in range(W):
        ry = river_y(x)
        for y in range(ry - 2, ry + 3):
            if 0 <= y < H:
                m.cls[y, x] = 'W' if (y == ry and not (42 <= x <= 47 or 60 <= x <= 65) and 2 <= x < W - 2) else 'w'

    # ---- 4. Monumental Royal Architecture & Landmarks (100% Exact HEAD Door/Warp Coords!) ----
    # A. Briar Hall Royal Citadel Front along the North Crest (y=0..9)
    # `gt_gate6` (12x8) at (65, 2) -> bottom y=9, 6-wide open arch spans x=68..73 right over Warp (71, 9)!
    m.stamp('gt_gate6', 65, 2)
    for tx in (53, 59, 78, 84, 90):
        m.stamp('gt_tower', tx, 3)
    # Curtain wall connecting towers via masonry parapet & banners
    for tx in (4, 16, 28, 40):
        m.stamp('gt_tower', tx, 3)

    # B. Southern Kingsgate (x=32..41, y=79..86): `gt_gate4` (10x8) opens cleanly across x=35..38!
    m.stamp('gt_gate4', 32, 79)
    for tx in (6, 18, 46, 60, 74, 88, 97):
        if can_put_clean(m, 'gt_tower', tx, 80, on='.Tcf', check_level=False):
            m.stamp('gt_tower', tx, 80)

    # C. Cathedral of the Evergreen (`cv_lantern` 12x9 at (10, 17) -> exact door (16, 25)!) flanked by twin Gothic towers!
    d = {}
    d['cath'] = m.stamp('cv_lantern', 10, 17, 'C280_CATH', 'Cathedral door')
    m.stamp('gt_tower', 7, 19)
    m.stamp('gt_tower', 22, 19)

    # D. Pokémon Center (`cv_pc` 7x7 at (47, 59) -> exact door (50, 65), HealingSpot (50, 66)!)
    d['pc'] = m.stamp('cv_pc', 47, 59, 'C280_PC', 'Poke Center door')

    # E. Mart (`cv_mart` 6x6 at (69, 55) -> exact door (70, 60)!)
    d['mart'] = m.stamp('cv_mart', 69, 55, 'C280_MART', 'Mart door')

    # ---- 5. Exact HEAD Events (ALL 11 events locked 100% verbatim!) ----
    E = [
        {'type': 'sign', 'at': [37, 78], 'post': False,
         'text': 'VERDANCE\nSeat of the Evergreen Crown. The Kingsgate closes at dusk.'},
        {'type': 'sign', 'at': [19, 27], 'post': False,
         'text': 'CATHEDRAL OF THE EVERGREEN\nEighteen windows, and one left clear.'},
        {'type': 'sign', 'at': [68, 11], 'post': False,
         'text': 'BRIAR HALL\nBy leave of Queen Maelis.'},
        {'type': 'npc', 'name': 'Gate serjeant', 'at': [73, 11], 'sprite': 'NPC 07', 'dir': 'down',
         'text': 'Gate serjeant: The Queen holds court in the Thorn Throne room. Mind the roses. [TODO story]'},
        {'type': 'npc', 'name': 'Flower seller', 'at': [58, 70], 'sprite': 'NPC 11', 'dir': 'right', 'move': 'random',
         'text': 'Flower seller: Everything blooms in Verdance. Nobody asks what it costs the soil. [TODO story]'},
        {'type': 'npc', 'name': 'Rootward child', 'at': [15, 66], 'sprite': 'NPC 05', 'dir': 'down', 'move': 'random',
         'text': 'Rootward child: Dig under any step here and the soil comes up grey. [TODO story]'},
        {'type': 'npc', 'name': 'Bridge warden', 'at': [45, 48], 'sprite': 'NPC 12', 'dir': 'down',
         'text': 'Bridge warden: Low town south of the Briarwater, high town north. Know which you belong to. [TODO story]'},
        {'type': 'warp', 'at': [71, 9], 'to': {'map': 285, 'x': 24, 'y': 60, 'dir': 'up'}},
    ]
    for e in E:
        x, y = e['at']
        m.taken[y, x] = True
        if e['type'] == 'sign':
            m.tile(4847, x, y, 1)
    m.events += E

    # Protect ALL 11 event coords, return warp (71, 11), HealingSpot (50, 66), doors & main avenues!
    key_pts = [tuple(e['at']) for e in m.events] + [
        (71, 10), (71, 11), (50, 66), (16, 26), (70, 61), (36, 79), (37, 79),
        (59, 39), (59, 40), (59, 41), (59, 42), (76, 24), (76, 25), (76, 26), (76, 27),
        (44, 48), (44, 49), (44, 55), (62, 48), (62, 56),
    ]
    prot_wide = reserve_mask(m, key_pts, pad=1)
    for x, y in key_pts:
        if m.inb(x, y):
            m.taken[y, x] = True

    # ---- 6. Four Distinct Urban Districts: Royal Mansions, Burgher Quarter, Artisan Shops & Rootward ----
    def place_district_row(x0, x1, y_bot, pool, seed, gap_choices=(0, 0, 1)):
        rng = random.Random(2800 + seed)
        x = x0
        last = None
        while x <= x1:
            room = x1 - x + 1
            cands = [n for n in pool if n != last and STAMPS[n]['w'] <= room]
            rng.shuffle(cands)
            ok = False
            for nm in cands:
                w, h = STAMPS[nm]['w'], STAMPS[nm]['h']
                y = y_bot - h + 1
                if can_put_clean(m, nm, x, y, on='.cfT', prot=prot_wide, check_level=True):
                    # Keep street below bottom row open
                    m.stamp(nm, x, y)
                    last = nm
                    x += w + rng.choice(gap_choices)
                    ok = True
                    break
            if not ok:
                x += 1

    NOBLE_POOL = ['th_p', 'th_x', 'th_ac', 'th_j', 'th_y', 'sp_inn', 'th_c', 'th_ab', 'gl_cot']
    SHOP_POOL = ['sp_bake', 'sp_cafe', 'sp_cloth', 'sp_pots', 'sp_books', 'sp_chand', 'sp_masks', 'sp_tav', 'th_a', 'th_d', 'th_m', 'th_q']
    BURGHER_POOL = ['th_c', 'th_f', 'th_k', 'th_r', 'th_ae', 'th_y', 'th_j', 'sp_books', 'sp_cafe', 'gl_cot', 'gl_ell']
    ROOTWARD_POOL = ['th_d', 'th_h', 'th_m', 'th_q', 'th_s', 'th_t', 'th_u', 'th_v', 'gl_flat1', 'gl_flat2', 'gl_shed']

    # Noble Hill Villas flanking the Mid Botanical Terrace (Tier 1: y_bot=33)
    place_district_row(50, 68, 33, NOBLE_POOL, seed=10, gap_choices=(2, 3))
    place_district_row(81, 96, 33, NOBLE_POOL, seed=11, gap_choices=(1, 2))
    # Burgher Quarter south of Cathedral Close (Tier 0: y_bot=37 & y_bot=44)
    place_district_row(6, 28, 37, BURGHER_POOL, seed=12, gap_choices=(0, 1))
    place_district_row(6, 38, 44, BURGHER_POOL, seed=13, gap_choices=(0, 1))
    # Artisan Market Shops flanking Market Terraces (Tier 0: y_bot=63 & y_bot=73)
    place_district_row(76, 97, 63, SHOP_POOL, seed=14, gap_choices=(0, 1))
    place_district_row(74, 96, 73, SHOP_POOL, seed=15, gap_choices=(0, 1))
    place_district_row(40, 46, 63, SHOP_POOL, seed=16, gap_choices=(0, 1))
    # Rootward Old Quarter cozy townhouses (SW: y_bot=64 & y_bot=73)
    place_district_row(6, 34, 64, ROOTWARD_POOL, seed=17, gap_choices=(0, 0, 1))
    place_district_row(6, 32, 73, ROOTWARD_POOL, seed=18, gap_choices=(0, 1))

    # ---- 7. Royal Botanical Gardens, Fountains, Market Awning Stalls, Banners & Lanterns ----
    # Royal Banners crowning Briar Hall Citadel, Cathedral & Kingsgate!
    for bx, by in ((66, 7), (75, 7), (60, 7), (81, 7), (12, 23), (20, 23), (33, 83), (40, 83)):
        m.over.append((2, bx, by, P1('lm_banner_w') if bx % 2 == 0 else P1('lm_banner')))

    # Grand Royal Fountains, Well, Classical Statues, Topiaries, Market Stalls & Flower Planters!
    lamp_pts = []
    beacon_pts = []
    for nm, x, y in (
        # Upper Royal Conservatory Court (Tier 2): Twin Fountains, Statues, Topiaries, Planters & Beacons!
        ('lm_fountain', 55, 16), ('lm_fountain', 83, 16),
        ('lm_statue', 64, 10), ('lm_statue', 77, 10),
        ('pf_beacon', 66, 10), ('pf_beacon', 74, 10),
        ('pf_planter0', 62, 13), ('pf_planter1', 65, 13), ('pf_planter2', 76, 13), ('pf_planter3', 79, 13),
        ('lm_topiary', 63, 15), ('lm_topiary', 78, 15), ('lm_topiary', 73, 21), ('lm_topiary', 79, 21),
        ('pf_stonebench', 65, 15), ('pf_stonebench', 74, 15),
        # Cathedral of the Evergreen Close: Royal Fountain, Stone Benches, Planters & Topiaries!
        ('pf_fountain', 26, 26), ('pf_stonebench', 12, 27), ('pf_stonebench', 22, 27),
        ('pf_planter0', 11, 25), ('pf_planter1', 13, 25), ('pf_planter2', 18, 25), ('pf_planter3', 20, 25),
        ('lm_topiary', 9, 26), ('lm_topiary', 23, 26),
        # Grand Market Terraces: Central Plaza Fountain, Well, Vibrant Awning Stalls, Flower Carts!
        ('pf_fountain', 61, 66), ('pf_well', 54, 71),
        ('pf_stall0', 53, 66), ('pf_stall1', 56, 66), ('pf_stall2', 67, 66), ('pf_stall3', 70, 66),
        ('pf_stall4', 53, 72), ('pf_stall0', 60, 72), ('pf_stall2', 66, 72), ('pf_stall1', 73, 68),
        ('pf_wagon', 47, 70), ('pf_stonebench', 59, 65), ('pf_stonebench', 65, 65), ('pf_stonebench', 62, 71),
        ('pf_planter0', 48, 66), ('pf_planter1', 52, 66), ('pf_planter2', 68, 62), ('pf_planter3', 72, 62),
        ('pf_planter0', 58, 67), ('pf_planter1', 66, 67),
        # Mid Botanical Terrace overlooks & Kingsgate entry beacons!
        ('pf_beacon', 33, 78), ('pf_beacon', 40, 78),
        ('pf_stonebench', 64, 34), ('pf_stonebench', 71, 32), ('pf_planter0', 55, 38), ('pf_planter2', 62, 38),
        # Rootward cozy village clutter (crates, barrels, washing lines, well)
        ('pf_well', 18, 70), ('hb_washline', 14, 73), ('hb_barrel', 10, 66), ('sh_crates', 28, 66),
        ('hb_boxes', 32, 74), ('pf_logbench', 20, 67),
    ):
        res = put_safe(m, nm, x, y, on='.fc', r=1, prot=prot_wide)
        if res and nm == 'pf_beacon':
            beacon_pts.append((res[0] + 1, res[1] + 1))

    # Royal Streetlamps lining Kingsway, Cathedral Close, Market Terraces, Thornhill & Bridges!
    for x, y in ((34, 77), (39, 77), (36, 71), (41, 63), (42, 57), (47, 57), (42, 47), (47, 47),
                 (60, 57), (65, 57), (60, 47), (65, 47), (56, 42), (62, 42), (56, 36), (62, 36),
                 (73, 27), (79, 27), (73, 21), (79, 21), (63, 12), (79, 12), (56, 14), (86, 14),
                 (14, 29), (24, 29), (33, 39), (51, 68), (64, 63), (75, 65), (84, 66), (14, 67), (26, 67)):
        if can_put_clean(m, 'pf_lantern', x, y - 2, on='.fc', prot=prot_wide):
            m.stamp('pf_lantern', x, y - 2)
            lamp_pts.append((x, y - 1))

    # Forged balustrades overlooking Thornhill terraces & Briarwater riverfront!
    paint_rail_run(m, 50, 56, 39, kind='rw')
    paint_rail_run(m, 62, 74, 39, kind='rw')
    paint_rail_run(m, 64, 73, 24, kind='rw')
    paint_rail_run(m, 79, 89, 24, kind='rw')
    paint_rail_run(m, 26, 41, 47, kind='qy')
    paint_rail_run(m, 48, 59, 47, kind='qy')
    paint_rail_run(m, 66, 82, 47, kind='qy')

    # ---- 8. Lush Botanical Hedges, Overlapping Groves & Cherry Blossoms (ZERO lone sticker trees!) ----
    # Manicured ornamental flowerbed/azalea hedges lining the Upper & Mid Botanical Terraces!
    for hx, hy in ((54, 21), (57, 21), (60, 21), (63, 21), (66, 21), (81, 21), (84, 21), (87, 21),
                   (66, 16), (76, 16), (52, 28), (55, 28), (82, 28), (85, 28), (88, 28),
                   (32, 24), (35, 24), (38, 24), (28, 32), (31, 32), (48, 74), (51, 74), (72, 73)):
        nm = ['nt_azalea0', 'nt_azalea1', 'nt_azalea2', 'nt_shrub0', 'nt_shrub1'][(hx + hy) % 5]
        put_safe(m, nm, hx, hy, on='.', r=0, prot=prot_wide)

    # Overlapping lush botanical canopy groves across every hillside park, river bank & Cathedral green!
    verdance_groves = [
        (33, 14, ROYAL_CANOPY, 5, 3.0, 'pf_g_tree2'),
        (42, 16, ROYAL_CANOPY, 5, 3.0, 'pf_g_tree2'),
        (35, 29, ROYAL_CANOPY, 4, 2.5, None),
        (8, 12, ROYAL_CANOPY, 4, 2.5, None),
        (52, 19, ROYAL_CANOPY, 4, 2.6, None),
        (93, 18, ROYAL_CANOPY, 5, 2.8, 'pf_g_tree2'),
        (94, 28, ROYAL_CANOPY, 4, 2.6, None),
        (49, 28, ROYAL_CANOPY, 4, 2.6, None),
        (86, 41, ROYAL_CANOPY, 5, 3.0, 'pf_g_tree2'),
        (95, 42, ROYAL_CANOPY, 5, 2.8, None),
        (16, 56, ROYAL_CANOPY, 4, 2.6, None),
        (30, 56, ROYAL_CANOPY, 4, 2.6, None),
        (76, 56, ROYAL_CANOPY, 4, 2.5, None),
        (92, 57, ROYAL_CANOPY, 5, 2.8, 'pf_g_tree2'),
        (12, 81, ROYAL_CANOPY, 4, 2.6, None),
        (25, 81, ROYAL_CANOPY, 4, 2.6, None),
        (54, 82, ROYAL_CANOPY, 4, 2.6, None),
        (72, 82, ROYAL_CANOPY, 4, 2.6, None),
        (86, 82, ROYAL_CANOPY, 4, 2.6, None),
    ]
    for idx, (cx, cy, kinds, cnt, rad, hero) in enumerate(verdance_groves):
        place_canopy_grove(m, cx, cy, kinds, count=cnt, radius=rad, on='.', seed=idx + 50,
                           hero=hero, prot=prot_wide, undergrowth=True)

    # Reeds & water lilies along the Briarwater banks
    for x in range(8, 96, 6):
        if 41 <= x <= 48 or 59 <= x <= 66:
            continue
        ry = river_y(x)
        for dy in (-3, 3):
            nm = 'nt_reed0' if (x + dy) % 2 == 0 else 'nt_reed1'
            put_safe(m, nm, x, ry + dy, on='.', r=1, prot=prot_wide)
        if x % 12 == 2:
            put_safe(m, 'nt_lily', x + 2, ry + 3, on='.', r=1, prot=prot_wide)

    m.greenfill(4)

    # ---- 9. Paint Layers + Bridges + Crimson Palace Runner + River Rocks + Glows ----
    m.paint()

    # Royal Crimson-and-Gold Carpet descending from Briar Hall Palace Gate (70..72, 9..15)!
    for y in range(9, 16):
        for i, x in enumerate((70, 71, 72)):
            part = ('n' if y == 9 else 's' if y == 15 else '') + ('w' if i == 0 else 'e' if i == 2 else '')
            t = P1('lm_carpet_' + (part or 'c'))
            m.L[0, y, x] = t
            if m.L[1, y, x] >= K.RC.VBASE:
                m.L[1, y, x] = 0
    # Ensure Warp (71, 9) cell & its approach (71, 10..11) have zero blocking tiles
    for wy in (9, 10, 11):
        m.L[2, wy, 71] = 0
    # Block the north back of the gate archway at y=8 so player cannot walk behind Briar Hall wall
    for gx in range(68, 74):
        m.L[1, 8, gx] = P1('rw_f1m0')

    # Paint TWO Wide Dressed-Timber & Stone Bridges across the Briarwater (x=43..46 & x=61..64)!
    top_p = [C('ak', 1516 + i) for i in range(3)]
    body_p = [C('ak', 1524 + i) for i in range(3)]
    for bx0 in (43, 61):
        ry0 = river_y(bx0 + 1) - 3
        ry1 = river_y(bx0 + 1) + 3
        for y in range(ry0, ry1 + 1):
            for i, x in enumerate(range(bx0, bx0 + 4)):
                col = 0 if i == 0 else 2 if i == 3 else 1
                m.L[0, y, x] = body_p[col]
                m.L[1, y, x] = 0
                m.L[2, y, x] = 0
            # Side bridge posts at bridge heads
            if y in (ry0, ry1):
                for px in (bx0 - 1, bx0 + 4):
                    if m.inb(px, y) and not prot_wide[y, px]:
                        m.L[1, y, px] = P1('hb_bollard0')

    # Rocky mossy islets & boulders in the Briarwater River
    for nm, x, y in (('nt_boulder', 22, river_y(22) - 1), ('nt_boulder', 35, river_y(35)),
                     ('nt_boulder', 53, river_y(53) - 1), ('nt_boulder', 74, river_y(74)),
                     ('nt_boulder', 88, river_y(88) - 1)):
        L = np.array(STAMPS[nm]['layers'])
        h, w = L.shape[1:]
        if x + w <= W and y + h <= H and all(m.cls[y + j, x + i] in 'wW' and m.L[2, y + j, x + i] == 0 for i in range(w) for j in range(h)):
            for j in range(h):
                for i in range(w):
                    t = int(L[:, j, i].max())
                    if t:
                        m.L[2, y + j, x + i] = t

    # Overhead festoon lantern strings across Market Terraces, Kingsway & Twin Bridges!
    add_festoon_strings(m, [
        (52, 72, 66, 0), (52, 72, 71, 2), (43, 46, river_y(44), 1), (61, 64, river_y(62), 0),
        (12, 24, 28, 1), (34, 39, 77, 2),
    ], kind='lstring')

    # Warm regal glows around Briar Hall Gate, Cathedral, Fountains, Market Stalls, Kingsgate & Lamps!
    add_warm_glows(m, lamp_pts + beacon_pts + [
        (71, 10), (58, 18), (86, 18), (16, 26), (28, 28), (63, 68), (50, 66), (70, 61), (36, 80),
        (59, 40), (76, 25),
    ])
    add_water_glints(m, water_cls='wW', seed=280, density=0.04)

    m.scatter(12, seed=280, on='.T')
    head = {'id': 280, 'name': 'Verdance - Market Terraces', 'bgm': 'Natural Park', 'parent': 0,
            'rubric': True, 'yards_ok': True, 'tone': [-6, 10, -12, 0],
            'metadata': {'Outdoor': True, 'ShowArea': True, 'MapPosition': [0, 14, 12],
                         'BattleBack': 'field', 'Name': 'Verdance'},
            '_file': '280_verdance.yaml'}
    m.write(280, head, '# Verdance - Market Terraces (280). WRITTEN BY layouts/wave10_towns_craft.py (Wave 10 Rejuv V14 Craft).\n')
    print('280 Verdance doors', d)
    return d


def build_lumen_180():
    """Lumen City - The Concourse (180) — invokes lumen.build_180() with Wave 10 pre/post hooks."""
    import lumen
    orig_city = lumen.City
    lumen.USED_LINKS.clear()

    class Wave10City(orig_city):
        def paint(self):
            enhance_lumen_180_pre(self)
            return super().paint()

        def seal_edges(self, *args, **kwargs):
            enhance_lumen_180_post(self)
            return super().seal_edges(*args, **kwargs)

    lumen.City = Wave10City
    try:
        m = lumen.build_180()
    finally:
        lumen.City = orig_city

    m.write(180, dict(lumen.HEAD180, _file='180_lumen_concourse.yaml'),
            comment='# GENERATED by mapgen/layouts/wave10_towns_craft.py (Wave 10 Rejuv V14 Craft).\n')
    print('180 Lumen unplaced:', lumen.ST.unplaced(180))
    return m


BUILDERS = {
    100: build_ferrow_100,
    120: build_briarwick_120,
    160: build_ebbmouth_160,
    180: build_lumen_180,
    280: build_verdance_280,
}


def main():
    args = [int(a) for a in sys.argv[1:] if a.isdigit()]
    targets = args or [100, 120, 160, 180, 280]
    for mid in targets:
        if mid not in BUILDERS:
            raise SystemExit('wave10_towns_craft: unknown map %d' % mid)
        BUILDERS[mid]()


if __name__ == '__main__':
    main()

