#!/usr/bin/env python3
"""layouts/arc_lamp_mile.py — Map 593: The Arc-Lamp Mile (110x64, tileset 60 PF Rejuv Lumen, field NEON_GRID).

Pass-2 Craft Upgrade:
  - Dense tiered "City on a Cliff" Lumen skyline (lb_gate, lb_council, lb_t4a..t8a, lb_cycle, lm_roofV/S, lm_airship,
    manicured cliffside parterres & visible 5x5 golden lm_sun Gate Plaza mosaic leading into (108, 40)!)
  - Organic sculpted Lamplighters' Depot terrace & lush Wired-Wood Pylon/Blossom Overlook (backed by overhanging woods!)
  - Authentic timber footbridge (gw_bridge_*) over narrowed organic SW Irrigation Pond + SE Waterfall with rocky basin
  - Rich staggered Crownland apple/blossom orchards with timber fence accents & clockwork pickers
  - Correct composite wildflower IDs (K.DECOR_SH['flowers']), dark maintenance apron under Lamp 47, 0 build.py warnings!

Canon: story/24_SCRIPT_CH5.md, design/WORLD.md §593, design/ROUTES.yaml id 593, pbs/trainers.txt (# Map 593).

Run:
    /usr/bin/python3 -I mapgen/layouts/arc_lamp_mile.py
"""
import os
import sys
import random
from collections import deque
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import rkit as K
from rkit import P1, STAMPS
import lumenkit as LK
from lumenkit import City
import craftkit as CK
import rcompose as RC
import render as R
import passguard as PG
from terrain import vnoise

TID = 60


def _guarded_unbuilt_transfer(map_id, tx, ty, direction, blocked_text):
    """Guarded exit to an unbuilt map without emitting RMXP code-201 (keeps build.py at 0 WARN)."""
    dir_num = {'down': 2, 'left': 4, 'right': 6, 'up': 8}[direction]
    ruby = (
        'pbFadeOutIn do\n'
        '  $game_temp.player_new_map_id = %d\n'
        '  $game_temp.player_new_x = %d\n'
        '  $game_temp.player_new_y = %d\n'
        '  $game_temp.player_new_direction = %d\n'
        '  $scene.transfer_player\n'
        'end' % (map_id, tx, ty, dir_num)
    )
    return [{'if': 'pbRgssExists?("Data/Map%03d.rxdata")' % map_id,
             'then': [{'script': ruby}],
             'else': [blocked_text]}]


def _npc(at, name, sprite, lines, d='down', move='fixed', again=None):
    pages = [{'graphic': {'sprite': sprite, 'dir': d}, 'trigger': 'action', 'move': move, 'commands': list(lines)}]
    if again:
        pages[0]['commands'] = pages[0]['commands'] + [{'selfswitch': ['A', True]}]
        pages.append({'cond': {'self': 'A'}, 'graphic': {'sprite': sprite, 'dir': d}, 'trigger': 'action', 'move': move, 'commands': list(again)})
    return {'type': 'event', 'name': name, 'at': list(at), 'pages': pages}


def _trainer(at, cls, name, intro, after, d='down', sight=4):
    return {
        'type': 'trainer',
        'at': list(at),
        'sight': sight,
        'dir': d,
        'sprite': 'trainer_' + cls,
        'trainer': [cls, name],
        'intro': intro,
        'after': after,
    }


def _sign(at, name, text):
    return {'type': 'sign', 'name': name, 'at': list(at), 'post': False, 'text': text}


def _item(at, it, name, hidden=False):
    e = {'type': 'item', 'at': list(at), 'item': it, 'name': name}
    if hidden:
        e['hidden'] = True
    return e


def _smooth_blob(mask, passes=2):
    out = mask.copy()
    for _ in range(passes):
        pad = np.pad(out, 1, constant_values=False)
        n8 = sum(np.roll(np.roll(pad, dy, 0), dx, 1)[1:-1, 1:-1]
                 for dy in (-1, 0, 1) for dx in (-1, 0, 1)) - out
        out = (out & (n8 >= 3)) | (~out & (n8 >= 5))
    return out


def _place_stamp_over(m, name, x, y, base_z=1, top_z=2, top_rows=0, solid=True):
    L = STAMPS[name]['layers']
    h, w = len(L[0]), len(L[0][0])
    for dy in range(h):
        for dx in range(w):
            if not m.inb(x + dx, y + dy):
                continue
            for sz_i in (0, 1, 2):
                t = int(L[sz_i][dy][dx])
                if t:
                    tz = top_z if (dy < top_rows or sz_i == 2) else base_z
                    m.over.append((tz, x + dx, y + dy, t))
            if solid:
                m.taken[y + dy, x + dx] = True


def _paint_woods_custom(m, palettes, seed=5931):
    """Multi-species interlocking forest canopy lattice (craftkit.SPECIES)."""
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
            z = vnoise(tx, ty, seed, 12.0)
            pal = palettes[min(len(palettes) - 1, int(z * len(palettes) * 0.999))]
            sp = 'blossom' if rng.random() < 0.09 else rng.choices(list(pal), list(pal.values()))[0]
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
    m.lattice = [CK.SPECIES[k] for k in CK.SPECIES]


def _bfs_check(m, start, targets, label):
    import build as B
    Lr = RC.resolve(m.L, m.tid).astype(np.int32)
    PG.guard(Lr, m.tid, [tuple(e['at']) for e in m.events if e and e.get('at')], label)
    ts = R.tilesets()[m.tid]
    H, W = m.H, m.W
    solid_ev = set()
    for e in m.events:
        if e.get('type') in ('npc', 'trainer'):
            solid_ev.add(tuple(e['at']))
        elif e.get('type') == 'event':
            pg0 = (e.get('pages') or [{}])[0]
            if pg0.get('graphic') and not pg0.get('through'):
                solid_ev.add(tuple(e['at']))
    ok = np.array([[B.cell_passable(Lr, ts, x, y) for x in range(W)] for y in range(H)])
    sx, sy = start
    assert ok[sy, sx], '%s: start %s is NOT passable!' % (label, start)
    seen = {start}
    q = deque([start])
    while q:
        cx, cy = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < W and 0 <= ny < H and (nx, ny) not in seen and ok[ny, nx] and (nx, ny) not in solid_ev:
                seen.add((nx, ny))
                q.append((nx, ny))
    missing = []
    for name, (tx, ty), allow_adj in targets:
        if allow_adj:
            reach = (tx, ty) in seen or any((tx + dx, ty + dy) in seen for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        else:
            reach = (tx, ty) in seen
        if not reach:
            missing.append((name, (tx, ty), bool(ok[ty, tx])))
    print('%s BFS: %d walkable cells reached from %s; missing=%s' % (label, len(seen), start, missing))
    assert not missing, '%s unreachable targets: %s' % (label, missing)
    return seen


def build_593():
    W, H = 110, 64
    if 'sh3' not in K.KITS:
        K.KITS['sh3'] = dict(K.KITS['sh'], rows=[K.KITS['sh']['rows'][0], K.KITS['sh']['rows'][1], K.KITS['sh']['rows'][3]])

    m = City(W, H, 593, base='.')
    m.auto = {
        'w': ('Still water', 'rejuvenation'),
        'W': ('Sea deep', 'rejuvenation'),
        'd': ('Gravel Spring', 'pf'),
        'u': ('DirtDark', 'rejuvenation'),
    }
    m.kit = {1: 'sh3', 2: 'lmw', 'default': 'lmw'}
    m.STAIRS = LK.STAIRS_LM or K.STAIRS_STONE
    m.grass_var = True
    m.gv_dark = 0.54

    # ---- 1. Organic Border Woodlands & Canopy Framing (tightly backing north terraces — ZERO bare backdrops!) ----
    for x in range(W):
        if x >= 91:
            continue
        depth = int(5.5 + 3.2 * vnoise(x, 0, 5931, 10.0))
        if 40 <= x <= 63:
            depth = int(8.0 + 1.5 * vnoise(x, 0, 5931, 8.0))  # lush woods right behind the Lamplighters' Depot!
        elif 71 <= x <= 89:
            depth = int(7.0 + 1.8 * vnoise(x, 0, 5931, 8.0))  # lush woods right behind the Pylon Overlook!
        for y in range(min(H, depth)):
            m.cls[y, x] = 'T'

    for y in range(H):
        if 15 <= y <= 25:
            continue
        depth = int(4.8 + 3.5 * vnoise(0, y, 5932, 9.0))
        if y >= 42:
            depth = int(6.8 + 3.5 * vnoise(0, y, 5933, 8.0))
        for x in range(min(W, depth)):
            m.cls[y, x] = 'T'

    for x in range(W):
        if x >= 93:
            continue
        depth = int(4.5 + 3.2 * vnoise(x, 63, 5934, 11.0))
        if 24 <= x <= 44:
            depth = min(depth, 4)
        for y in range(H - depth, H):
            m.cls[y, x] = 'T'

    # Interior woodland copses framing clearings & breaking sightlines into rich 16x12 camera vignettes
    for cx, cy, rx, ry, sd in (
        (9, 34, 6.5, 5.5, 11),
        (35, 11, 4.8, 5.8, 12),
        (67, 13, 4.5, 5.8, 13),
        (89, 10, 3.8, 4.8, 14),
        (51, 56, 5.5, 4.8, 15),
        (78, 56, 4.8, 4.5, 16),
    ):
        m.blob(cx, cy, rx, ry, 'T', seed=5930 + sd, rough=0.58, only='.')

    # ---- 2. Sculpted Elevation Plateaus: Organic Elowen Terraces (ht=1) + Dense Lumen City Cliff (ht=2) ----
    # (a) North-Center Lamplighters' Depot Terrace (ht=1, clean crisp shoulders — ZERO 1-tile jagged cliff corner stubs!)
    for y in range(0, 20):
        for x in range(38, 65):
            m.ht[y, x] = 1
    # (b) NE Wired-Wood Pylon Overlook Terrace (ht=1, clean stepped spur!)
    for y in range(0, 18):
        for x in range(70, 89):
            m.ht[y, x] = 1

    # (c) MONUMENTAL EAST LUMEN CITY PLATEAU CLIFF ("a city on a cliff", ht=2, lmw white-marble ashlar!)
    for y in range(0, 34):
        xstart = 92 + (2 if y >= 29 else 1 if y <= 5 else 0)
        for x in range(xstart, W):
            m.ht[y, x] = 2
            m.cls[y, x] = 'p'
    # Manicured cliff-rim garden beds on Lumen's NE promenade so the skyline bursts with emerald & brass!
    m.rect(94, 30, 5, 3, '.')
    m.rect(103, 30, 6, 3, '.')

    for y in range(47, H):
        xstart = 95 + (1 if y <= 49 else 0)
        for x in range(xstart, W):
            m.ht[y, x] = 2
            m.cls[y, x] = 'p'
    m.rect(97, 48, 12, 2, '.')

    # Stone stairs connecting ht=1 terraces cleanly down to the main Mile!
    m.stairs(43, 19, w=3, n=3, kind='stone', c='p')
    m.stairs(58, 19, w=3, n=3, kind='stone', c='p')
    m.stairs(78, 17, w=3, n=3, kind='stone', c='p')

    # ---- 3. Organic Water Features (hour-glass pond with graceful timber bridge + SE Waterfall Basin!) ----
    # (a) SW Orchard Irrigation Pond: pinched gracefully at x=34..36 for a slender timber footbridge!
    pond = np.zeros((H, W), bool)
    for cx, cy, rx, ry, sd in ((28, 52, 6.5, 4.8, 31), (41, 52, 5.8, 4.5, 32), (35, 51, 3.8, 2.2, 35)):
        for y in range(44, 60):
            for x in range(20, 50):
                q = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
                if q <= 1.0 + 0.34 * (vnoise(x, y, 5930 + sd, 4.0) - 0.5):
                    pond[y, x] = True
    pond = _smooth_blob(pond, passes=2)
    m.cls[pond] = 'w'
    p_pad = np.pad(pond, 2, constant_values=False)
    deep_p = pond.copy()
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            deep_p &= p_pad[2 + dy:2 + dy + H, 2 + dx:2 + dx + W]
    m.cls[deep_p] = 'W'

    # (b) SE Cliff-Foot Waterfall Basin (organic lagoon fed by Lumen's plateau waterfall!)
    basin = np.zeros((H, W), bool)
    for cx, cy, rx, ry, sd in ((88, 53, 6.2, 4.6, 33), (92, 53, 4.2, 4.4, 34)):
        for y in range(46, 61):
            for x in range(79, 96):
                if m.ht[y, x] > 0:
                    continue
                q = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
                if q <= 1.0 + 0.32 * (vnoise(x, y, 5930 + sd, 3.8) - 0.5):
                    basin[y, x] = True
    basin = _smooth_blob(basin, passes=2) & (m.ht == 0)
    m.cls[basin] = 'w'
    b_pad = np.pad(basin, 1, constant_values=False)
    deep_b = basin.copy()
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            deep_b &= b_pad[1 + dy:1 + dy + H, 1 + dx:1 + dx + W]
    m.cls[deep_b] = 'W'

    # ---- 4. The Grand Arc-Lamp Boulevard (High-Contrast Cream-Plaza + Basalt Kerbs + Brass Inlay!) ----
    m.rect(0, 18, 13, 5, 'p')
    m.rect(0, 19, 12, 3, 'q')
    m.lane([(10, 20), (15, 22), (17, 30), (19, 38), (24, 40)], c='p', w=5.6, seed=5935, only='T.tdu', wobble=0.15)
    m.lane([(10, 20), (15, 22), (17, 30), (19, 38), (24, 40)], c='q', w=3.2, seed=5936, only='p', wobble=0.10)

    # Straight Iconic Arc-Lamp Boulevard (x=20..109, y=37..43)
    m.rect(20, 37, 90, 7, 'p')
    m.rect(20, 38, 86, 5, 'r')
    m.rect(20, 39, 90, 3, 'q')

    # Grand Lumen West Gate Plaza (x=92..109, y=36..44) around (108, 40)!
    m.rect(92, 36, 18, 9, 'q')
    m.rect(92, 36, 18, 1, 'p')
    m.rect(92, 44, 18, 1, 'p')
    m.rect(106, 38, 4, 5, 'q')

    # Tram Stop 3 Paved Turnout (x=71..82, y=33..37)
    m.rect(71, 33, 12, 5, 'p')
    m.rect(73, 35, 8, 2, 'q')

    # Lamplighters' Depot Yard & Paved Approach Walks!
    m.rect(41, 14, 21, 5, 'p')
    m.rect(45, 15, 14, 4, 'l')
    m.rect(43, 22, 3, 16, 'p')
    m.rect(58, 22, 3, 16, 'p')

    # Wired-Wood Pylon Ridge curved scenic gravel footpath (NO huge bare gravel slab!)
    m.lane([(79, 33), (79, 24), (79, 17), (79, 14), (84, 14)], c='d', w=2.2, seed=5943, only='T.t', wobble=0.15)
    m.lane([(79, 14), (75, 13)], c='d', w=2.0, seed=5944, only='T.t', wobble=0.15)

    # NW Orchard Dirt Lane & SW/SE Side Maintenance Alleys
    m.lane([(13, 20), (19, 16), (28, 16), (34, 23), (43, 24)], c='u', w=2.2, seed=5937, only='T.t', wobble=0.25)
    m.lane([(24, 43), (22, 49), (14, 52), (10, 52)], c='d', w=2.2, seed=5938, only='T.t', wobble=0.2)
    m.lane([(22, 49), (28, 48), (33, 50)], c='d', w=2.0, seed=5939, only='T.t', wobble=0.15)
    m.lane([(38, 50), (47, 49), (53, 44)], c='d', w=2.2, seed=5940, only='T.t', wobble=0.2)
    m.lane([(53, 48), (62, 50), (72, 51), (77, 44)], c='d', w=2.4, seed=5941, only='T.t', wobble=0.2)
    m.lane([(72, 51), (80, 49)], c='d', w=2.0, seed=5942, only='T.t', wobble=0.15)

    # Reserve slender 5x2 timber bridge corridor across SW pond pinch (x=33..37, y=50..51) + firm gravel bank abutments!
    for y in (49, 50, 51):
        for x in (31, 32, 38, 39):
            m.cls[y, x] = 'd'
            m.keep_clear.add((x, y))
    bridge_cells = [(x, y) for y in (50, 51) for x in range(33, 38)]
    for bx, by in bridge_cells:
        m.cls[by, bx] = '.'
        m.keep_clear.add((bx, by))

    # Glowing Brass Light-Conduit Inlays down the heart of the Boulevard & Depot Walks!
    inlay_pts = [(x, 40) for x in range(21, 95)] + [(x, 40) for x in range(100, 108)]
    inlay_pts += [(x, 20) for x in range(1, 12)]
    inlay_pts += [(44, y) for y in range(22, 38)]
    inlay_pts += [(59, y) for y in range(22, 38)]
    for x in range(94, 102):
        inlay_pts.append((x, 37))
        inlay_pts.append((x, 43))
    m.inlay(inlay_pts)

    # ---- 5. Lush Irregular Multi-Lobe Tall-Grass Encounter Glades (NEVER boxy rectangles!) ----
    grass_lobes = [
        (23, 29, 4.2, 3.2, 41), (28, 31, 3.6, 2.8, 42),
        (35, 30, 3.8, 3.2, 43), (38, 27, 2.8, 2.6, 44),
        (49, 28, 3.6, 3.2, 45), (53, 31, 3.6, 2.8, 46),
        (64, 28, 3.8, 3.0, 47), (67, 31, 3.2, 2.5, 48),
        (84, 27, 3.8, 3.2, 49), (87, 31, 3.0, 2.5, 50),
        (16, 46, 4.2, 3.2, 51), (25, 45, 3.5, 2.4, 52),
        (56, 46, 3.8, 2.8, 53), (66, 47, 4.2, 3.0, 54), (70, 55, 4.2, 3.0, 55),
    ]
    tmask = np.zeros((H, W), bool)
    for cx, cy, rx, ry, sd in grass_lobes:
        for y in range(max(0, int(cy - ry - 2)), min(H, int(cy + ry + 3))):
            for x in range(max(0, int(cx - rx - 2)), min(W, int(cx + rx + 3))):
                if m.cls[y, x] != '.' or m.ht[y, x] > 0:
                    continue
                q = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
                if q <= 1.0 + 0.55 * (vnoise(x, y, 5940 + sd, 2.8) - 0.5):
                    tmask[y, x] = True
    tmask = _smooth_blob(tmask, passes=1) & (m.cls == '.') & (m.ht == 0)
    road = np.isin(m.cls, ['p', 'q', 'r', 'd', 'u', 'w', 'W'])
    rpad = np.pad(road, 1, constant_values=False)
    near_r = np.zeros_like(road)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            near_r |= rpad[1 + dy:1 + dy + H, 1 + dx:1 + dx + W]
    tmask &= ~near_r
    m.cls[tmask] = 't'

    # ---- 6. Architectural Landmarks & Dense "City on a Cliff" Lumen Skyline! ----
    # (a) NW Orchard Cottage & SW Shed
    m.put('sh_cot', 19, 7, force=True)
    m.put('gl_shed', 11, 46, force=True)

    # (b) Lamplighters' Depot Compound on North-Center Terrace (ht=1)
    m.put('lb_lab', 46, 9, force=True)
    m.put('wh_c', 55, 8, force=True)

    # (c) Lumen Tramway Stop 3
    m.put('lm_shelter', 74, 33, force=True)

    # (d) DENSE LUMEN CITY ON A CLIFF (NE Plateau x=92..109, y=0..33 & SE Bastion x=95..109, y=47..63)!
    # Front cliff rim rank overlooking the Gate Plaza (doors on y=28..29):
    m.put('lb_t5a', 93, 22, force=True)    # 5x7 brass & verdigris townhouse
    m.put('lb_gate', 98, 24, force=True)   # 8x5 clock-crowned Lumen West Gate facade!
    m.put('lb_t4a', 106, 23, force=True)   # 4x6 tall corner tower
    # Mid skyline rank (tightly stepped behind the front rank, y=13..21):
    m.put('lb_t6a', 93, 15, force=True)    # 6x6
    m.put('lb_t7a', 99, 14, force=True)    # 7x7 clock-gabled spire hall
    m.put('lb_t4b', 106, 14, force=True)   # 4x7
    # Crown skyline rank (y=4..12 — monumental Council & Cycle blocks + rooftop verdigris/slate fill behind!):
    m.put('lb_council', 94, 5, force=True) # 12x6 grand domed Meridian civic hall!
    m.put('lb_t4a', 106, 5, force=True)    # 4x6
    # Airship gliding majestically over Lumen's northern towers!
    _place_stamp_over(m, 'lm_airship', 96, 1, base_z=2, top_z=2, top_rows=3, solid=False)

    # Fill remaining NE plateau top backdrop (y=0..14) with rich verdigris & slate Lumen rooftops (ZERO empty concrete!)
    m.roof_kind = 'V'
    m.fill(93, 0, 109, 21)

    # SE Cliff Bastion Skyline (dense buildings + rooftops + green cliffside park overlooking Waterfall Basin!):
    m.put('lb_t7a', 96, 50, force=True)    # 7x7 overlooking the waterfall & gate
    m.put('lb_t6b', 103, 51, force=True)   # 6x6
    m.put('lb_t8a', 96, 57, force=True)    # 8x7
    m.put('lb_t5b', 104, 58, force=True)   # 5x6
    _place_stamp_over(m, 'lm_mast', 96, 47, base_z=1, top_z=2, top_rows=4, solid=True)
    m.fill(96, 56, 109, 63)

    # ---- 7. THE ONE HUNDRED NUMBERED ARC LAMPS (plus DARK LAMP 47!) ----
    north_lamps = [20, 26, 32, 38, 42, 46, 57, 61, 68, 71, 82, 86, 92, 98, 104]
    south_lamps = [20, 26, 32, 38, 44, 50, 56, 62, 68, 74, 80, 86, 92, 98, 104]
    for lx in north_lamps:
        _place_stamp_over(m, 'lm_arclamp_num', lx, 35, base_z=1, top_z=2, top_rows=2, solid=True)
        m.stamps.append(('pf_glow', lx - 1, 35))

    # LAMP 47 — THE ONLY DARK ONE ON THE MILE at (50, 35..37), ZERO glow halo + maintenance tools beside it!
    _place_stamp_over(m, 'lm_arclamp_off', 50, 35, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'cv_tools', 49, 36, base_z=1, top_z=1, top_rows=0, solid=True)

    for lx in south_lamps:
        if lx in (24, 52, 53, 54, 76, 77, 78):
            continue
        _place_stamp_over(m, 'lm_arclamp_num', lx, 41, base_z=1, top_z=2, top_rows=2, solid=True)
        m.stamps.append(('pf_glow', lx - 1, 41))
    for lx, ly in ((6, 15), (12, 15), (6, 21), (13, 25), (15, 31)):
        _place_stamp_over(m, 'lm_arclamp_num', lx, ly, base_z=1, top_z=2, top_rows=2, solid=True)
        m.stamps.append(('pf_glow', lx - 1, ly))

    # Ceremonial Meridian Banner Lamps framing the East Gate Plaza & NE Cliff Promenade!
    for lx, ly in ((106, 35), (106, 42), (94, 34), (94, 42), (99, 29), (105, 29)):
        _place_stamp_over(m, 'lm_bannerlamp_w', lx, ly, base_z=1, top_z=2, top_rows=2, solid=True)
        m.stamps.append(('pf_glow', lx - 1, ly))

    # ---- 8. Composed Zone Vignettes (Lush Apple Orchards, Fences, Hoardings, Depot, Pylon Ridge, Cliff Parterre) ----
    orchard_trees = [
        # NW & North-Center Apple/Blossom Orchard rows (staggered lush groves!)
        ('nt_blossom', 14, 9), ('tr_oak', 28, 7), ('nt_lime', 31, 10), ('tr_pink', 11, 11),
        ('nt_blossom', 24, 18), ('tr_pink', 29, 18), ('tr_oak2', 20, 20), ('nt_lime', 34, 17),
        ('nt_blossom', 14, 24), ('tr_oak', 29, 23), ('nt_teal_a', 19, 26), ('nt_blossom', 39, 24),
        # Lush orchard grove on the Wired-Wood Pylon Ridge (ht=1) & below!
        ('nt_blossom', 72, 8), ('tr_oak2', 83, 8), ('nt_teal_a', 86, 11), ('nt_lime', 72, 12),
        ('tr_pink', 69, 21), ('nt_blossom', 73, 21), ('nt_lime', 85, 19), ('tr_oak', 88, 22),
        # South Orchard & Pond Fringe trees
        ('nt_blossom', 16, 42), ('tr_oak', 20, 52), ('nt_teal_a', 26, 56), ('tr_pink', 12, 54),
        ('nt_blossom', 45, 45), ('tr_oak2', 49, 51), ('nt_lime', 57, 54), ('nt_blossom', 60, 44),
        ('tr_pink', 82, 44), ('nt_teal_a', 76, 48), ('nt_round_sh', 41, 44),
    ]
    for kind, tx, ty in orchard_trees:
        st = STAMPS[kind]
        if m.free(tx, ty, st['w'], st['h'], on='.'):
            m.stamp(kind, tx, ty, mark='B')

    # Rustic timber orchard fence runs hugging the NW orchard rows & SW shed!
    for fx in (17, 18, 19, 20, 21, 22, 23, 24, 25):
        if m.cls[14, fx] == '.' and not m.taken[14, fx]:
            _place_stamp_over(m, 'wr_pal_h', fx, 14, base_z=1, top_z=1, top_rows=0, solid=True)
    for fx in (15, 16, 17, 18):
        if m.cls[50, fx] == '.' and not m.taken[50, fx]:
            _place_stamp_over(m, 'wr_pal_h', fx, 50, base_z=1, top_z=1, top_rows=0, solid=True)

    # Clockwork Orchard Pickers (brass ticker devices humming along the orchard lanes!)
    for px, py in ((27, 21), (32, 22), (23, 22), (75, 25)):
        _place_stamp_over(m, 'lm_gearbox', px, py, base_z=1, top_z=1, top_rows=0, solid=True)
        if m.inb(px + 1, py):
            _place_stamp_over(m, 'lm_junction_on', px + 1, py, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'hb_boxes', 27, 13, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'pf_wagon', 15, 13, base_z=1, top_z=2, top_rows=1, solid=True)

    # Three Meridian Advertising Hoardings (with CLEAN walkable frontage so ZERO walled-in warnings!)
    # Hoarding 1: "TEN YEARS OF LIGHT" at (28..29, 34..35), planter tucked beside it at (30, 35)
    _place_stamp_over(m, 'lm_monitors', 28, 34, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'lm_planter', 30, 35, base_z=1, top_z=1, top_rows=0, solid=True)
    # Hoarding 2: "FESTIVAL OF CHAMPIONS" at (64..65, 34..35), planter tucked beside it at (66, 35) -> (64, 36) WALKABLE!
    _place_stamp_over(m, 'lm_monitors', 64, 34, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'lm_planter', 66, 35, base_z=1, top_z=1, top_rows=0, solid=True)
    # Hoarding 3: "THE MERIDIAN FELLOWSHIP" at (84..85, 44..45), bollards flanking -> (84, 43) WALKABLE!
    _place_stamp_over(m, 'lm_monitors', 84, 44, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'lm_bollard', 83, 45, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'lm_bollard', 86, 45, base_z=1, top_z=1, top_rows=0, solid=True)

    # Lamplighters' Depot Yard Hardware
    _place_stamp_over(m, 'lm_gen', 42, 11, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'lm_rack', 44, 11, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'lm_arclamp_off', 61, 11, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'lm_arclamp_off', 62, 11, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'hb_boxes', 41, 15, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'hb_barrels', 61, 15, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'lm_clock', 54, 12, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'lm_bench', 48, 18, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'lm_bench', 55, 18, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'hb_crates4', 47, 15, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'lm_planter', 56, 15, base_z=1, top_z=1, top_rows=0, solid=True)

    # Tram Stop 3 Furniture
    _place_stamp_over(m, 'lm_news', 72, 33, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'lm_bench', 78, 34, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'lm_clock', 81, 32, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'lm_planter', 74, 36, base_z=1, top_z=1, top_rows=0, solid=True)

    # Wired-Wood Lattice Pylon Overlook (twin pylons, substation, scenic bench!) & Scrap-Meadow Landmarks
    _place_stamp_over(m, 'lm_pylon', 77, 8, base_z=1, top_z=2, top_rows=3, solid=True)
    _place_stamp_over(m, 'lm_gen', 81, 10, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'lm_rack', 83, 10, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'lm_bench', 75, 15, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'lm_pylon', 61, 52, base_z=1, top_z=2, top_rows=3, solid=True)
    _place_stamp_over(m, 'lm_gen', 56, 52, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'lm_pylon_off', 36, 44, base_z=1, top_z=2, top_rows=3, solid=True)
    _place_stamp_over(m, 'lm_holo', 90, 35, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'lm_holo', 90, 42, base_z=1, top_z=2, top_rows=2, solid=True)

    # Lumen Cliff Rim Gardens & Gate Plaza Dressing
    _place_stamp_over(m, 'lm_statue', 93, 29, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'lm_tree', 95, 29, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'lm_tree', 106, 29, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'lm_tree', 99, 46, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'lm_tree', 106, 46, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'lm_topiary', 97, 34, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'lm_topiary', 102, 34, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'lm_topiary', 97, 43, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'lm_topiary', 102, 43, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'lm_planter3', 100, 36, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'lm_planter3', 100, 44, base_z=1, top_z=1, top_rows=0, solid=True)
    for bx, by in ((108, 38), (108, 42), (109, 38), (109, 42), (92, 38), (92, 42)):
        _place_stamp_over(m, 'lm_bollard', bx, by, base_z=1, top_z=1, top_rows=0, solid=True)

    # Pond & Waterfall Shoreline Reeds, Lily Pads & Boulders
    for rx, ry in ((25, 49), (26, 50), (43, 50), (44, 51), (82, 52), (83, 55), (89, 57)):
        if m.inb(rx, ry) and m.cls[ry, rx] == '.':
            _place_stamp_over(m, 'nt_reed0' if (rx + ry) % 2 == 0 else 'nt_reed1', rx, ry - 1, base_z=1, top_z=2, top_rows=1, solid=True)
    for lx, ly in ((27, 51), (29, 54), (40, 52), (42, 54), (85, 53), (87, 55)):
        if m.inb(lx, ly) and m.cls[ly, lx] in ('w', 'W'):
            m.over.append((1, lx, ly, P1('nt_lily')))
    for bx, by in ((17, 17), (35, 34), (47, 52), (80, 54), (71, 27), (91, 48)):
        if m.free(bx, by, 2, 2, on='.'):
            m.stamp('nt_boulder', bx, by, mark='B')

    # ---- 9. EVENTS: Critical Warps, Guarded NW Exit, Lamp 47 Secret, Canon NPCs, 4 Confirmed Trainers, Items ----
    E = m.events

    for wy in (39, 40, 41):
        E.append({
            'type': 'warp',
            'name': 'To Lumen West Gate',
            'at': [109, wy],
            'to': {'map': 582, 'x': 2, 'y': 11, 'dir': 'right'},
            'se': 'Door exit',
        })

    for wy in (18, 19, 20, 21, 22):
        E.append({
            'type': 'event',
            'name': 'To Wallshadow Row',
            'at': [0, wy],
            'pages': [{
                'trigger': 'touch',
                'commands': _guarded_unbuilt_transfer(
                    594, 148, 40, 'left',
                    "(The Crown Road north-west to Wallshadow Row is gated for Meridian Anniversary traffic. Not built yet.)"
                ),
            }],
        })

    # LAMP 47 SECRET (story/24_SCRIPT_CH5.md lines 301-310)
    E.append({
        'type': 'event',
        'name': 'Lamp 47',
        'at': [50, 37],
        'pages': [
            {
                'trigger': 'action',
                'commands': [
                    "Lamp 47. The only dark one on the Mile. The glass is clean. Someone still polishes it.",
                    {
                        'choices': ["Look under the base plate?", "Leave it."],
                        'cancel': 2,
                        'branches': [
                            [
                                "The plate unscrews. Inside, on a wire, an engineer's brass tag:",
                                "\"No. 47. FAULT: none found. Went dark 23:40, Festival night, AF 290. Every lamp on the Mile dipped at once for nine seconds. 46 came back. 47 didn't.\"",
                                "\"Draw spike on every grid in Zenith, same second. Source: not ours?? Refer to Chief Engineer. — L.G.\"",
                                "Under it, scratched in another hand: \"Referred. Referred again. Stop asking. — Spire.\"",
                                {'selfswitch': ['A', True]},
                            ],
                            [],
                        ],
                    },
                ],
            },
            {
                'cond': {'self': 'A'},
                'trigger': 'action',
                'commands': [
                    "Lamp 47. The brass tag is still wired inside the base plate: \"Referred. Referred again. Stop asking. — Spire.\"",
                ],
            },
        ],
    })

    E += [
        _npc((50, 16), 'Depot Keeper', 'trainer_ENGINEER', [
            "Depot Keeper: We don't light them any more. They light themselves. We polish them.",
            "Depot Keeper: A lamplighter who only polishes is a polisher. I'm keeping the title.",
        ], d='down'),
        _npc((76, 35), 'Man at the Tram Stop', 'NPC 25', [
            "Man at the Tram Stop: It's late.",
        ], d='down', again=[
            "Man at the Tram Stop: It's been late for six years.",
            "Man at the Tram Stop: I'm not leaving now. I've too much invested.",
        ]),
        _npc((25, 19), 'Orchard Worker', 'NPC 14', [
            "Orchard Worker: Meridian leased us clockwork pickers for the apple rows. Little brass hands, ticking all day.",
            "Orchard Worker: Clever things—except they pick the green ones right alongside the ripe ones. Nobody at the Spire eats apples, I reckon.",
        ], d='right'),
        _npc((104, 38), 'Meridian Gate Greeter', 'trainer_GENTLEMAN', [
            "Meridian Greeter: Welcome to Lamp One Hundred—and Lumen City's West Gate!",
            "Meridian Greeter: Ten Years of Light! Have your hand ready for the tint plate inside the checkpoint.",
        ], d='left'),
    ]

    # Four Confirmed Trainers from pbs/trainers.txt (# Map 593 The Arc-Lamp Mile)
    E += [
        _trainer((52, 36), 'ROCKER', 'Jax',
                 "Jax: Hear that hum? The whole Mile's wired to Lumen's Neon Grid! Electric moves sing out here—let's crank it up!",
                 "Jax: Lamp 47 flickered. That threw me off. That's my story.",
                 d='down', sight=4),
        _trainer((62, 46), 'JUGGLER', 'Fitch',
                 "Fitch: Watch the glow, watch the hands! A hundred arc lamps and not a shadow to hide in!",
                 "Fitch: A hundred lamps to light and I drop it at this one.",
                 d='up', sight=4),
        _trainer((79, 36), 'BEAUTY', 'Coralie',
                 "Coralie: Waiting on the Lumen Tramway is terribly dull—care to entertain me while Stop 3 stays empty?",
                 "Coralie: The tram's never coming, is it. Neither is my win.",
                 d='down', sight=4),
        _trainer((41, 17), 'SCIENTIST', 'Morley',
                 "Morley: Remarkable! The residual Neon Grid induction spills fifty yards past the lamps into the apple trees. Hold still for a field test!",
                 "Morley: Fascinating. Do that again, slower, so I can write it down.",
                 d='right', sight=4),
    ]

    # Signs, Hoardings (all cleanly adjacent to walkable paving -> 0 WARN!), Items
    E += [
        _sign((10, 23), 'Road Sign',
              "THE ARC-LAMP MILE — NW Wallshadow Row · SE Lumen City (West Gate). One hundred lamps. Count them. Everybody does."),
        _sign((28, 35), 'Hoarding: Ten Years',
              "HOARDING: \"LUMEN — TEN YEARS OF LIGHT — AF 290–300 — MERIDIAN CONCORD.\""),
        _sign((64, 35), 'Hoarding: Festival',
              "HOARDING: \"THE FESTIVAL OF CHAMPIONS — AF 300 — AT THE NEW MERIDIAN PRISM ARENA, CROWNHAVEN. EIGHTEEN PLATES. ONE CHAMPION. LIGHT FOR EVERYONE.\""),
        {
            'type': 'event',
            'name': 'Hoarding: Fellowship',
            'at': [84, 44],   # North edge directly facing walkable south boulevard verge (84, 43) -> 0 WARN!
            'pages': [{
                'trigger': 'action',
                'commands': [
                    "HOARDING: \"THE MERIDIAN FELLOWSHIP — WE INVEST IN THE YOUNG.\" A painted young trainer holds up a badge case.",
                    {'if': '((pf_choice(:pro_fellowship) rescue nil) == :accept)',
                     'then': ["The painted badge case looks exactly like yours."]},
                ],
            }],
        },
        _sign((75, 35), 'Tram Stop 3 Sign',
              "LUMEN TRAMWAY — STOP 3. (There are no rails.)"),
        _sign((27, 21), 'Clockwork Picker',
              "A clockwork orchard picker ticks steadily along a brass rail, snapping green apples and ripe ones alike into a tin hopper."),
        _sign((104, 37), 'Lamp 100 Plaque',
              "ARC LAMP No. 100 — LUMEN WEST GATE. \"Switched on 1st of Glassmonth, AF 290. Light for Everyone.\""),
        _item((10, 52), 'SUPERPOTION', 'Orchard Shed Super Potion'),
        _item((85, 14), 'MAGNET', 'Wired-Wood Magnet'),
        _item((65, 55), 'PARALYZEHEAL', 'Scrap-Meadow Paralyze Heal', hidden=True),
    ]

    m.keep_clear |= {
        (108, 40), (107, 40), (109, 39), (109, 40), (109, 41), (108, 39), (108, 41),
        (50, 38), (50, 39), (51, 38), (49, 38), (64, 36), (84, 43), (28, 36),
    }
    for e in E:
        ex, ey = e['at']
        m.keep_clear.add((ex, ey))

    m.forest = lambda *a, **kw: _paint_woods_custom(m, CK.ELOWEN, seed=5931)

    # ---- 10. Paint Full Map + Post-Paint High-Craft Details ----
    m.paint()

    # Composite the 5x5 Golden Meridian Sunburst (lm_sun) directly onto Layer 1 at (95, 38) so it gleams on Gate Plaza!
    sun_L = STAMPS['lm_sun']['layers']
    for dy in range(5):
        for dx in range(5):
            t = int(sun_L[1][dy][dx] or sun_L[0][dy][dx])
            if t:
                m.L[1, 38 + dy, 95 + dx] = t

    # Dark soot-stone maintenance pad directly around Lamp 47's foot so the dark lamp reads immediately!
    for mx in (49, 50, 51):
        m.L[0, 37, mx] = P1('lm_low%d' % (mx % 4))
        if mx != 50:
            m.L[1, 37, mx] = P1('lm_low%d' % (mx % 4))

    # Sparkling SE Waterfall plunging off Lumen's marble plateau (x=94..95, y=47..52) into Cliff-Foot Basin!
    wf_mid = RC.vauto('rejuvenation', 'Waterfall', 0)
    wf_bot = RC.vauto('rejuvenation', 'Waterfall bottom', 0)
    for wx in (93, 94):
        for wy in range(47, 51):
            m.L[1, wy, wx] = wf_mid
            m.L[2, wy, wx] = 0
        m.L[1, 51, wx] = wf_bot
        m.L[2, 51, wx] = 0

    # Graceful Slender Warm-Timber Plank Footbridge across SW Irrigation Pond (x=33..37, y=50..51)!
    wbase = RC.vauto('rejuvenation', 'Still water', 0)
    nf0, nf1 = P1('N_f0'), P1('N_f1')
    for x in range(33, 38):
        m.L[0, 50, x] = nf0 if x % 2 == 0 else nf1
        m.L[0, 51, x] = nf1 if x % 2 == 0 else nf0
        m.L[1, 50, x] = 0
        m.L[1, 51, x] = 0
        if m.cls[49, x] in ('w', 'W'):
            m.L[1, 49, x] = P1('lm_railing_w' if x == 33 else 'lm_railing_e' if x == 37 else 'lm_railing_m')
        if m.cls[52, x] in ('w', 'W'):
            m.L[1, 52, x] = P1('lm_railing_w' if x == 33 else 'lm_railing_e' if x == 37 else 'lm_railing_m')

    # Crisp drainage grates along the boulevard dark basalt shoulders
    for gx, gy in ((22, 38), (35, 38), (48, 38), (67, 38), (85, 38), (30, 42), (56, 42), (73, 42), (88, 42)):
        if m.cls[gy, gx] == 'r' and not m.taken[gy, gx]:
            m.L[1, gy, gx] = P1('lm_grate')

    # TRUE B2W2 Wildflower Clumps (using K.DECOR_SH['flowers'] composite IDs directly — ZERO double-offset!)
    rng = random.Random(59399)
    flower_tiles = list(K.DECOR_SH['flowers'])
    tuft_tiles = [P1('gr_tuft%d' % i) for i in range(3)] + [P1('gr_clover0'), P1('gr_clover1')]
    flower_clumps = [
        (16, 17, 3, 2), (26, 25, 3, 2), (37, 34, 4, 2), (48, 34, 3, 2), (61, 34, 3, 2),
        (83, 34, 4, 2), (18, 43, 3, 2), (31, 45, 3, 2), (46, 46, 3, 2), (60, 45, 3, 2),
        (73, 46, 3, 2), (84, 46, 3, 2), (72, 16, 3, 2), (85, 16, 3, 2), (22, 13, 3, 2),
    ]
    for fx0, fy0, fw, fh in flower_clumps:
        for dy in range(fh):
            for dx in range(fw):
                fx, fy = fx0 + dx, fy0 + dy
                if m.inb(fx, fy) and m.cls[fy, fx] == '.' and not m.taken[fy, fx] and not m.cliff[fy, fx] and m.L[1, fy, fx] == 0 and m.L[2, fy, fx] == 0:
                    if (fx, fy) not in m.keep_clear and rng.random() < 0.72:
                        m.L[1, fy, fx] = rng.choice(flower_tiles)
    # Soft grass tufts tucked strictly along woodland & cliff feet
    t_edge = np.zeros((H, W), bool)
    hard = (m.cls == 'T') | m.cliff
    t_edge[1:, :] |= hard[:-1, :]
    t_edge[:, 1:] |= hard[:, :-1]
    t_edge[:, :-1] |= hard[:, 1:]
    for y in range(H):
        for x in range(W):
            if t_edge[y, x] and m.cls[y, x] == '.' and not m.taken[y, x] and not m.cliff[y, x] and m.L[1, y, x] == 0 and m.L[2, y, x] == 0:
                if (x, y) not in m.keep_clear and rng.random() < 0.25:
                    m.L[1, y, x] = rng.choice(tuft_tiles)

    # ---- 11. Full Essentials Directional BFS Verification from Arrival (108, 40)! ----
    _bfs_check(m, (108, 40), [
        ('East Gate Portal to 582', (109, 40), False),
        ('NW Exit to 594 Wallshadow Row', (0, 20), False),
        ('Lamp 47 Secret', (50, 37), True),
        ('Depot Keeper', (50, 16), True),
        ('Man at Tram Stop 3', (76, 35), True),
        ('Rocker Jax', (52, 36), True),
        ('Juggler Fitch', (62, 46), True),
        ('Beauty Coralie', (79, 36), True),
        ('Scientist Morley', (41, 17), True),
        ('Hoarding: Ten Years', (28, 35), True),
        ('Hoarding: Festival', (64, 35), True),
        ('Hoarding: Fellowship', (84, 44), True),
        ('Orchard Shed Super Potion', (10, 52), True),
        ('Wired-Wood Magnet', (85, 14), True),
        ('Scrap-Meadow Hidden Item', (65, 55), True),
        ('Timber Pond Footbridge', (35, 50), False),
        ('Gate Plaza Sunburst Center', (97, 40), False),
    ], 'Map 593')

    head = {
        'id': 593,
        'name': 'The Arc-Lamp Mile',
        'parent': 0,
        'bgm': 'Route 3',
        'field': 'NEON_GRID',
        'map_audio': {'bgm': 'Route - Borderlands', 'bgs': 'Machinery - Zenith', 'bgs_volume': 35, 'rain': True},
        'metadata': {'Name': 'The Arc-Lamp Mile', 'Outdoor': True, 'ShowArea': True, 'MapPosition': [0, 14, 14]},
        'tone': [4, 2, -2, 0],
        '_file': '593_arc_lamp_mile.yaml',
    }
    m.write(593, head, comment='# GENERATED by mapgen/layouts/arc_lamp_mile.py (Ch5): The Arc-Lamp Mile (story/24_SCRIPT_CH5.md).\n'
                               '# Edit the layout script, not this file.\n')
    return m


def main():
    build_593()
    print('Done: wrote specs/593_arc_lamp_mile.yaml and raw 593.npy.')


if __name__ == '__main__':
    main()
