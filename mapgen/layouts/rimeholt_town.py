#!/usr/bin/env python3
"""mapgen/layouts/rimeholt_town.py — Act 3 Batch 3H Builder: Rimeholt Town Wards (300, 301, 302, 303, 304).

Builds the 5 northern capital town maps of Isenmar to First-Pass Critic Gold Standard:
  - 300 Rimeholt - Thane's Harbour   (46x40, TS 52 PF Rejuv Snow, Outdoor, :FROZEN_LAKE, rubric: true)
  - 301 Rimeholt Pokémon Center      (15x11, TS 34 Prismfall Interior, Alpine-Nordic Gold Standard)
  - 302 Rimeholt Mart                (12x10, TS 34 Prismfall Interior, Winter Provisioner Gold Standard)
  - 303 Rimeholt - Icewall Gate      (40x24, TS 52 PF Rejuv Snow, Outdoor, :FROZEN_LAKE, rubric: true)
  - 304 Rimeholt - Sled Market       (46x36, TS 52 PF Rejuv Snow, Outdoor, :FROZEN_LAKE, rubric: true)

Canonical sources: design/maps.json, design/ROUTES.yaml, design/FLAGS.md, design/WALKTHROUGH.md,
story/30_SCRIPT_CH11.md, pbs/encounters.txt ([300]), plugins/Prismfall Trials/.

Run:
  /usr/bin/python3 -I mapgen/layouts/rimeholt_town.py
"""
import math
import os
import random
import subprocess
import sys
import tempfile
import types
from collections import deque

LAYOUT_DIR = os.path.dirname(os.path.abspath(__file__))
HERE = os.path.dirname(LAYOUT_DIR)
for p in (HERE, LAYOUT_DIR):
    if p not in sys.path:
        sys.path.insert(0, p)

import numpy as np
import yaml

import rkit as K
from rkit import C, P1, STAMPS
import rcompose as RC
import render as R
import passguard as PG
import craftkit as CK
from terrain import vnoise

TID_SNOW = 52
TID_INT = 34
RIME_POS = [0, 3, 2]
RIME_HEAL_SPOT = [300, 10, 15]

SPEC_DIR = os.path.join(HERE, 'specs')
RAW_DIR = os.path.join(HERE, 'data', 'raw')

# Register Kristiline 3x4 snow-laden alpine spruces into CK.SPECIES for dense overlapping winter lattices
CK.SPECIES['kspA'] = ([[9944, 9945, 9946], [9952, 9953, 9954]], [[9960, 9961, 9962], [9968, 9969, 9970]], 1)
CK.SPECIES['kspB'] = ([[9947, 9948, 9949], [9955, 9956, 9957]], [[9963, 9964, 9965], [9971, 9972, 9973]], 1)
CK.SPECIES['kspC'] = ([[9976, 9977, 9978], [9984, 9985, 9986]], [[9992, 9993, 9994], [10000, 10001, 10002]], 1)
CK.SPECIES['kspD'] = ([[9979, 9980, 9981], [9987, 9988, 9989]], [[9995, 9996, 9997], [10003, 10004, 10005]], 1)

ALPINE_WOODS = [
    {'kspA': 5, 'kspB': 4, 'snowteal': 3, 'snow0': 2},
    {'kspC': 4, 'kspD': 4, 'snowteal2': 3, 'snowblue': 2},
    {'kspA': 4, 'kspC': 3, 'snowblue': 3, 'snow1': 2},
    {'kspB': 4, 'kspD': 4, 'snow0': 3, 'snowteal': 2},
]

# Pixel-verified multi-tile snow/alpine sprites: (top_rows on L2 pri=5, bot_rows on L1 pas=15)
KF_TEAL_PINE_A = ([[9833, 9834], [9841, 9842]], [[9849, 9850], [9857, 9858]])
KF_TEAL_PINE_B = ([[9837, 9838], [9845, 9846]], [[9853, 9854], [9861, 9862]])
KF_SPRUCE_A = ([[9944, 9945, 9946], [9952, 9953, 9954]], [[9960, 9961, 9962], [9968, 9969, 9970]])
KF_SPRUCE_B = ([[9947, 9948, 9949], [9955, 9956, 9957]], [[9963, 9964, 9965], [9971, 9972, 9973]])
KF_SHRUB_A = ([[9864, 9865]], [[9872, 9873]])
KF_SHRUB_B = ([[9880, 9881]], [[9888, 9889]])
KF_CRYS_MONO = ([[9868, 9869]], [[9876, 9877]])
KF_BOULDER = ([[9634, 9635]], [[9642, 9643]])
# Pixel-verified safe tag==0, pas==0, pri==0 pale glacier-blue 3x3 mosaic (TS 52 & TS 57) & frost overlays
GLACIER_9 = [
    [12476, 12477, 12478],
    [12484, 12485, 12486],
    [12492, 12493, 12494],
]
GLACIER_CENTER = 12485
SNOW_BASE = 10395
SAFE_CRACKS = [19267, 19268, 19269]
SAFE_PUDDLES = [19270, 19271]
SAFE_FROST = [23038, 23039, 23040]   # wr_frost0..2

# 3-row frosted Sheridan snow cliff kit (lip / face / base)
if 'shs3' not in K.KITS:
    K.KITS['shs3'] = dict(K.KITS['shs'], rows=[K.KITS['shs']['rows'][0], K.KITS['shs']['rows'][1], K.KITS['shs']['rows'][3]])

from interiorkit import TF

# TS 34 Interior Constants (Exact 591 Brassfall / 221 Mirefen / 222 Mirefen Mart Gold Standard!)
VOID34 = 5437
CREAM_STONE = [[5920, 5921, 5922], [5928, 5929, 5930], [5936, 5937, 5938]]
ALPINE_SLATE = [[1152, 1153, 1154], [1160, 1161, 1162], [1168, 1169, 1170]]
DARK_WOOD = [[5352, 5353, 5354], [5360, 5361, 5362], [5360, 5361, 5362]]
BROWN_WOVEN_RUG = [[8620, 8621, 8622], [8628, 8629, 8630], [8636, 8637, 8638]]
RED_CARPET = [[7172, 7173, 7174], [7180, 7181, 7182], [7188, 7189, 7190]]
POKEBALL_MEDAL_5X4 = [
    [536, 537, 538, 539, 540],
    [544, 545, 546, 547, 548],
    [552, 553, 554, 555, 556],
    [560, 561, 562, 563, 564],
]
ALPINE_WINDOW = [[2086, 2087], [2094, 2095]]
GEO_MAP = [[4730, 4731], [4738, 4739]]
TF34 = TF

# Verified timber wharf plank tiles (ak sheet, matching 570 Frostwick jetty)
DOCK_TOP = [C('ak', 1516), C('ak', 1517), C('ak', 1518)]
DOCK_MID = [C('ak', 1524), C('ak', 1525), C('ak', 1526)]


# =================================================================================================
# Shared Snow-Map, Event, Verification, Border-Seal & Rubric Helpers
# =================================================================================================
def _snowmap(W, H, mid, kit='shs3'):
    m = K.RMap(W, H, TID_SNOW, mid, water='Still water snow', kit=kit, grass=K.SNOW_GROUND, decor=K.DECOR_SNOW)
    m.tall = K.SNOW_TALL
    m.STAIRS = tuple(STAMPS['fw_stair_' + k]['layers'][1][0][0] for k in 'lmr')
    m.grass2 = None
    m.lattice = K.RMap.TREES_SNOW
    m.SEAL = int(np.array(STAMPS['fw_stone']['layers']).max())
    m.auto = {
        'd': ('Packed Snow', 'pf'),
        'e': ('KristilineDirt', 'rejuvenation'),
        'w': ('Still water snow', 'reborn'),          # tag=6 (Surf + Old/Good/Super Rod fishing!)
        'o': ('KristilineWatersFrozen', 'rejuvenation'),  # tag=0, pas=0xf (impassable frozen harbor sea)
        'p': ('Frozen Pond', 'pf'),                   # tag=12 (slide ice)
        'W': ('Sea deep', 'rejuvenation'),            # tag=5, pas=0xf (impassable deep glacial lead)
    }
    m.JOIN = dict(K.RMap.JOIN, o='oW', W='oW', p='p', e='e', w='w')
    m.AUTO_Z = dict(K.RMap.AUTO_Z, o=0, W=0, p=0, w=0, e=1)
    return m


def _smooth_cls(m, c, into='.', passes=2, only=None):
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


def _doorstep(m, door, depth=5):
    x, y = door
    for dy in range(1, depth):
        if m.inb(x, y + dy) and m.cls[y + dy, x] in '.e':
            m.cls[y + dy, x] = 'd'
    for dx in (-1, 0, 1):
        if m.inb(x + dx, y + 1) and m.cls[y + 1, x + dx] in '.d':
            m.cls[y + 1, x + dx] = 'e'


def _put_sprite(m, x0, y0, top_rows, bot_rows, on='.T', avoid_mask=None, post_paint=False):
    h_top, h_bot = len(top_rows), len(bot_rows)
    w = len(bot_rows[0])
    if x0 < 0 or y0 < 0 or x0 + w > m.W or y0 + h_top + h_bot > m.H:
        return False
    y_bot = y0 + h_top
    for dy in range(h_bot):
        for dx in range(w):
            xx, yy = x0 + dx, y_bot + dy
            if m.cls[yy, xx] not in on or m.cliff[yy, xx] or m.taken[yy, xx]:
                return False
            if avoid_mask is not None and avoid_mask[yy, xx]:
                return False
    if post_paint:
        for dy, row in enumerate(bot_rows):
            for dx, t in enumerate(row):
                if t:
                    m.L[1, y_bot + dy, x0 + dx] = t
        for dy, row in enumerate(top_rows):
            for dx, t in enumerate(row):
                if t and m.L[2, y0 + dy, x0 + dx] == 0:
                    m.L[2, y0 + dy, x0 + dx] = t
    else:
        for dy, row in enumerate(bot_rows):
            for dx, t in enumerate(row):
                if t:
                    m.over.append((1, x0 + dx, y_bot + dy, t))
        for dy, row in enumerate(top_rows):
            for dx, t in enumerate(row):
                if t:
                    m.over.append((2, x0 + dx, y0 + dy, t))
    m.taken[y_bot:y_bot + h_bot, x0:x0 + w] = True
    return True


def _infill_winter(R_, palettes, scale=8.5, seed=0):
    """Fill every remaining bare 'T' cell with crisp overlapping snow evergreens so forest borders never look thin."""
    m = R_.m
    H, W = m.H, m.W
    rng = random.Random(seed + 4401)
    for y in range(H - 1, -1, -1):
        for x in range(W):
            if m.cls[y, x] != 'T' or m.cliff[y, x]:
                continue
            if int(m.L[1, y, x]) != 0:
                continue
            sp = rng.choice((KF_TEAL_PINE_A, KF_TEAL_PINE_B, KF_SPRUCE_A, KF_SPRUCE_B))
            h_top, h_bot = len(sp[0]), len(sp[1])
            w = len(sp[1][0])
            x0, y0 = x - w // 2, y - h_top - h_bot + 1
            if 0 <= x0 and x0 + w <= W and 0 <= y0 and y0 + h_top + h_bot <= H:
                y_bot = y0 + h_top
                if np.all(m.cls[y_bot:y_bot + h_bot, x0:x0 + w] == 'T') and not m.cliff[y_bot:y_bot + h_bot, x0:x0 + w].any():
                    if not m.taken[y_bot:y_bot + h_bot, x0:x0 + w].any():
                        _put_sprite(m, x0, y0, *sp, on='T', post_paint=True)
                        continue
            # Fallback solid snowy shrub/boulder so no 'T' cell is left walkable
            if int(m.L[1, y, x]) == 0:
                m.L[1, y, x] = KF_SHRUB_A[1][0][x % 2]
                if y > 0 and int(m.L[2, y - 1, x]) == 0:
                    m.L[2, y - 1, x] = KF_SHRUB_A[0][0][x % 2]


def _dress_snow_details(m, ev_mask, seed=1, drift_p=0.14, track_p=0.16, crack_p=0.22, reeds_p=0.06, keep_ice_l0=False):
    """Add crisp snow drifts, sled tracks, safe tag==0 ice cracks/puddles/frost, reeds & icy cliff faces (honest layer2 craft!)."""
    rng = random.Random(seed)
    drifts = [P1('fw_drift%d' % i) for i in range(3)]
    tracks = [P1('fw_tracks0'), P1('fw_tracks1')]
    cracks = list(SAFE_CRACKS)
    puddles = list(SAFE_PUDDLES)
    frosts = list(SAFE_FROST)
    icys = [P1('fw_icy%d' % i) for i in range(3)]
    reeds = [STAMPS['fw_reeds0']['layers'], STAMPS['fw_reeds1']['layers']]
    H, W = m.H, m.W
    for y in range(H):
        for x in range(W):
            if m.cliff[y, x]:
                if int(m.L[2, y, x]) == 0 and rng.random() < 0.45:
                    m.L[2, y, x] = rng.choice(icys)
                continue
            if ev_mask[y, x] or m.taken[y, x]:
                continue
            c = m.cls[y, x]
            if c == '.' and int(m.L[1, y, x]) == 0 and rng.random() < drift_p:
                m.L[1, y, x] = rng.choice(drifts)
            elif c == 'd' and int(m.L[1, y, x]) == 0 and rng.random() < track_p:
                m.L[1, y, x] = rng.choice(tracks)
            elif c == 'I':
                # Safe tag==0 frozen surface (ZERO slippery tag==12 fw_ice tiles!):
                # keep pre-painted glacier mosaic if requested, otherwise clean winter snow base 10395
                if not keep_ice_l0:
                    m.L[0, y, x] = SNOW_BASE
                if int(m.L[1, y, x]) == 0:
                    r = rng.random()
                    if r < crack_p:
                        m.L[1, y, x] = rng.choice(cracks)
                    elif not keep_ice_l0 and r < crack_p + 0.16:
                        m.L[1, y, x] = rng.choice(puddles)
                    elif r < crack_p + (0.24 if keep_ice_l0 else 0.30):
                        m.L[1, y, x] = rng.choice(frosts)
                    elif reeds_p > 0 and r < crack_p + 0.30 + reeds_p and y > 1 and int(m.L[2, y - 1, x]) == 0:
                        rd = rng.choice(reeds)
                        m.L[1, y, x] = int(rd[1][1][0] or rd[0][1][0])
                        m.L[2, y - 1, x] = int(rd[2][0][0] or rd[1][0][0])
            elif c == 'o' and int(m.L[1, y, x]) == 0 and rng.random() < 0.22:
                m.L[1, y, x] = rng.choice(puddles)


def _paint_wharf(m, x0, y0, x1, y1):
    """Paint weathered Nordic timber wharf decking spanning [x0..x1, y0..y1] (walkable over harbor water)."""
    w = x1 - x0 + 1
    for y in range(y0, y1 + 1):
        for i, x in enumerate(range(x0, x1 + 1)):
            if not m.inb(x, y):
                continue
            col = 0 if i == 0 else (2 if i == w - 1 else 1)
            m.L[0, y, x] = DOCK_TOP[col] if y == y0 else DOCK_MID[col]
            m.L[1, y, x] = 0
            m.L[2, y, x] = 0
            m.cls[y, x] = 'D'


def _guarded_unbuilt_transfer(map_id, tx, ty, direction, blocked_text):
    """Guarded exit to an unbuilt map with canonical Essentials v21 uppercase PBMoveRoute::BACKWARD."""
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
    return [{
        'if': 'pbRgssExists?("Data/Map%03d.rxdata")' % map_id,
        'then': [{'script': ruby}],
        'else': [
            blocked_text,
            {'script': 'pbMoveRoute($game_player, [PBMoveRoute::BACKWARD], true)'},
        ],
    }]


def _make_npc(name, at, sprite, d, lines, move='fixed'):
    return {
        'type': 'event',
        'name': name,
        'at': list(at),
        'pages': [{
            'graphic': {'sprite': sprite, 'dir': d},
            'trigger': 'action',
            'move': move,
            'commands': list(lines),
        }],
    }


def _sign(name, at, text):
    return {'type': 'sign', 'name': name, 'at': list(at), 'post': False, 'text': text}


def _reserve_mask(m, events, extra=(), pad=1):
    mask = np.zeros((m.H, m.W), dtype=bool)
    pts = [tuple(e['at']) for e in events if e.get('at')] + list(extra)
    for ex, ey in pts:
        for dy in range(-pad, pad + 1):
            for dx in range(-pad, pad + 1):
                xx, yy = ex + dx, ey + dy
                if m.inb(xx, yy):
                    mask[yy, xx] = True
    return mask


def _seal_unconnected_edges(m, open_cells=(), filler=None):
    import build as B
    ts = R.tilesets()[m.tid]
    Lr = RC.resolve(m.L, m.tid)
    keep = set(open_cells)
    f = filler if filler is not None else KF_BOULDER[1][0][0]
    H, W = m.H, m.W
    edge_pts = ([(x, 0) for x in range(W)] + [(x, H - 1) for x in range(W)] +
                [(0, y) for y in range(1, H - 1)] + [(W - 1, y) for y in range(1, H - 1)])
    for x, y in edge_pts:
        if (x, y) in keep:
            continue
        if B.cell_passable(Lr, ts, x, y):
            if m.L[1, y, x] == 0:
                m.L[1, y, x] = f
            else:
                m.L[2, y, x] = f


def _check_ruby_syntax(events, label):
    scripts = []
    def collect(cmds):
        for c in cmds or []:
            if isinstance(c, dict):
                if 'script' in c:
                    scripts.append(c['script'])
                if 'if' in c:
                    scripts.append(f"if ({c['if']})\nend")
                    collect(c.get('then'))
                    collect(c.get('else'))
                if 'choices' in c:
                    for ch in c['choices']:
                        if isinstance(ch, dict):
                            collect(ch.get('commands'))
    for e in events:
        for pg in e.get('pages') or []:
            collect(pg.get('commands'))
        collect(e.get('commands'))
    if not scripts:
        return
    combined = '\n# ---\n'.join(f"proc do\n{s}\nend" for s in scripts)
    with tempfile.NamedTemporaryFile('w', suffix='.rb', delete=False) as tf:
        tf.write(combined)
        tmp_path = tf.name
    try:
        res = subprocess.run(['ruby', '-c', tmp_path], capture_output=True, text=True)
        assert res.returncode == 0, f'{label}: Ruby syntax error!\n{res.stderr}'
    finally:
        os.unlink(tmp_path)


def _assert_zero_border_leaks(Lr, tid, events, label):
    import build as B
    ts = R.tilesets()[tid]
    H, W = Lr.shape[1:]
    touch_cells = set()
    for e in events:
        if e.get('type') in ('warp', 'exit', 'door'):
            touch_cells.add(tuple(e['at']))
        elif e.get('type') == 'event':
            for pg in e.get('pages') or []:
                if pg.get('trigger') == 'touch':
                    touch_cells.add(tuple(e['at']))
    leaks = []
    for x in range(W):
        for y in (0, H - 1):
            if B.cell_passable(Lr, ts, x, y) and (x, y) not in touch_cells:
                leaks.append((x, y))
    for y in range(1, H - 1):
        for x in (0, W - 1):
            if B.cell_passable(Lr, ts, x, y) and (x, y) not in touch_cells:
                leaks.append((x, y))
    assert not leaks, f'{label}: {len(leaks)} unguarded walkable border leak(s), e.g. {leaks[:8]}'


def _verify_map(Lr, tid, events, start, label, outdoor=False, targets=None, require_water=False):
    import build as B
    ts = R.tilesets()[tid]
    H, W = Lr.shape[1:]
    _check_ruby_syntax(events, label)
    if outdoor:
        _assert_zero_border_leaks(Lr, tid, events, label)
        r = B.rubric(Lr)
        need = [('layer2', 55, 1), ('layer3', 20, 1), ('bare', 35, -1), ('bare3x3', 13, -1), ('stacks', 10, 1), ('mirror', 15, -1)]
        fails = [f'{k}={r[k]:.1f}' for k, lim, sgn in need if (r[k] - lim) * sgn < 0]
        print(f'{label} RUBRIC: ' + '  '.join(f'{k}={r[k]:.1f}' for k, _, _ in need))
        assert not fails, f'{label}: Outdoor rubric FAILED: {fails}'

    by_cell = {}
    for e in events:
        if e and e.get('at'):
            by_cell.setdefault(tuple(e['at']), []).append(e)

    for e in events:
        if e.get('type') == 'sign':
            x, y = e['at']
            assert not B.cell_passable(Lr, ts, x, y), f'{label}: over_trigger? Sign {e.get("name")} at ({x},{y}) on walkable tile!'
        elif e.get('type') == 'event':
            x, y = e['at']
            for idx, pg in enumerate(e.get('pages') or []):
                g = pg.get('graphic') or {}
                if g.get('sprite') and not pg.get('through'):
                    assert B.cell_passable(Lr, ts, x, y), f'{label}: NPC {e.get("name")} p{idx} on SOLID tile ({x},{y})!'
                if pg.get('trigger', 'action') == 'action' and pg.get('commands'):
                    if g.get('sprite'):
                        continue
                    tid_g = g.get('tile')
                    if tid_g:
                        assert (ts['passages'][tid_g] & 0x0f) == 0x0f, f'{label}: over_trigger? {e.get("name")} tile {tid_g}'
                    else:
                        assert not B.cell_passable(Lr, ts, x, y), f'{label}: over_trigger? Blank action {e.get("name")} at ({x},{y})!'
        elif e.get('type') == 'item' and not e.get('hidden'):
            ix, iy = e['at']
            assert B.cell_passable(Lr, ts, ix, iy), f'{label}: Item {e.get("name")} on SOLID tile ({ix},{iy})!'
        elif e.get('type') == 'item' and e.get('hidden'):
            ix, iy = e['at']
            assert int(Lr[2, iy, ix]) == 0, f'{label}: HiddenItem {e.get("name")} at ({ix},{iy}) obscured by overhead L2 tile {int(Lr[2, iy, ix])}!'

    # Enforce ZERO walkable tag==12 (:Ice) slippery slide tiles across all Batch 3H maps
    tt = ts['terrain_tags']
    walk_ice = []
    for y in range(H):
        for x in range(W):
            if B.cell_passable(Lr, ts, x, y):
                for z in (2, 1, 0):
                    t = int(Lr[z, y, x])
                    if t > 0 and t < len(tt) and tt[t] != 0:
                        if tt[t] == 12:
                            walk_ice.append((x, y, t))
                        break
    assert not walk_ice, f'{label}: {len(walk_ice)} walkable tag==12 (:Ice) tiles found, e.g. {walk_ice[:6]}'

    def dir_ok(x, y, d):
        bit = 1 << (d // 2 - 1)
        for e in by_cell.get((x, y), []):
            t = e.get('type')
            if t in ('npc', 'trainer', 'mart', 'rock_smash', 'cut', 'strength'):
                return False
            if t == 'event':
                pg0 = (e.get('pages') or [{}])[0]
                if pg0.get('through') or pg0.get('cond'):
                    continue
                g = pg0.get('graphic') or {}
                if g.get('sprite'):
                    return False
                if g.get('tile'):
                    p = ts['passages'][g['tile']]
                    if p & bit or (p & 0x0f) == 0x0f:
                        return False
                    if ts['priorities'][g['tile']] == 0:
                        return True
        for z in (2, 1, 0):
            t = int(Lr[z, y, x])
            if t == 0:
                continue
            tag = ts['terrain_tags'][t] if t < len(ts['terrain_tags']) else 0
            if tag in (13, 15):
                continue
            p = ts['passages'][t]
            if p & bit or (p & 0x0f) == 0x0f:
                return False
            if ts['priorities'][t] == 0:
                return True
        return True

    sx, sy = start
    assert any(dir_ok(sx, sy, d) for d in (2, 4, 6, 8)), f'{label}: start {start} not passable!'
    seen = {start}
    q = deque([start])
    while q:
        cx, cy = q.popleft()
        for dx, dy, d in ((0, 1, 2), (0, -1, 8), (1, 0, 6), (-1, 0, 4)):
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < W and 0 <= ny < H and (nx, ny) not in seen:
                if dir_ok(cx, cy, d) and dir_ok(nx, ny, 10 - d):
                    seen.add((nx, ny))
                    q.append((nx, ny))

    if require_water:
        # Verify reachable Surf/Fish tag==6 water directly orthogonally adjacent to walkable ground
        water_adj = 0
        for cx, cy in seen:
            for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < W and 0 <= ny < H:
                    t0 = int(Lr[0, ny, nx])
                    if t0 < len(ts['terrain_tags']) and ts['terrain_tags'][t0] in (6, 7):
                        water_adj += 1
        print(f'{label}: reachable tag==6/7 water edges = {water_adj}')
        assert water_adj >= 10, f'{label}: insufficient reachable fishing/surfing water ({water_adj})!'

    check_list = targets if targets is not None else [
        (e.get('name', e.get('type', 'ev')), tuple(e['at']), e.get('type') not in ('warp', 'exit'))
        for e in events if e.get('at')
    ]
    missing = []
    for nm, (tx, ty), adj in check_list:
        ok = ((tx, ty) in seen or any((tx + dx, ty + dy) in seen for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)))) if adj else ((tx, ty) in seen)
        if not ok:
            missing.append((nm, (tx, ty)))
    print(f'{label}: reached {len(seen)} cells from {start}; missing={missing}')
    assert not missing, f'{label}: unreachable events/targets: {missing}'
    return seen


# =================================================================================================
# TS 34 Interior Helpers (Exact 591 Brassfall / 221-222 Mirefen Gold Standard!)
# =================================================================================================
def _put_tf34(L, name, x, y):
    rows, top = TF34[name]
    H, W = L.shape[1:]
    for dy, row in enumerate(rows):
        for dx, t in enumerate(row):
            if not t:
                continue
            xx, yy = x + dx, y + dy
            if not (0 <= xx < W and 0 <= yy < H):
                continue
            z = 2 if dy < top else 1
            if z == 1 and L[1, yy, xx]:
                z = 2
            L[z, yy, xx] = t


def _put_grid34(L, grid, x, y, z_rows=None):
    H, W = L.shape[1:]
    for dy, row in enumerate(grid):
        z_def = z_rows[dy] if z_rows is not None else 1
        for dx, t in enumerate(row):
            if not t:
                continue
            xx, yy = x + dx, y + dy
            if not (0 <= xx < W and 0 <= yy < H):
                continue
            z = z_def
            if z == 1 and L[1, yy, xx]:
                z = 2
            L[z, yy, xx] = t


def _put_9slice34(L, tiles9, x0, y0, x1, y1, z=0, mask=None):
    for y in range(y0, y1 + 1):
        ry = 0 if y == y0 else (2 if y == y1 else 1)
        for x in range(x0, x1 + 1):
            if mask is not None and not mask[y, x]:
                continue
            rx = 0 if x == x0 else (2 if x == x1 else 1)
            L[z, y, x] = tiles9[ry][rx]


def _seam_alpine_ts34(L, floor, wall_rows=2):
    """Warm Isenmar alpine timber & stone walling with dark charcoal void casing (exact 591 Brassfall PC!)."""
    H, W = floor.shape
    L[0, :, :] = VOID34
    wall_face = np.zeros((H, W), dtype=bool)
    for y in range(wall_rows, H):
        for x in range(1, W - 1):
            if floor[y, x] and not floor[y - 1, x]:
                for k in range(1, wall_rows + 1):
                    if y - k >= 0:
                        wall_face[y - k, x] = True
    interior = floor | wall_face
    for y in range(H):
        for x in range(W):
            if floor[y, x]:
                L[0, y, x] = 1161
            elif wall_face[y, x]:
                is_lower = (y + 1 < H and floor[y + 1, x])
                left_end = (x == 0) or not wall_face[y, x - 1]
                right_end = (x + 1 >= W) or not wall_face[y, x + 1]
                if left_end:
                    L[0, y, x] = 5571 if is_lower else 5563
                elif right_end:
                    L[0, y, x] = 5572 if is_lower else 5564
                else:
                    L[0, y, x] = 5555 if is_lower else 5547
            else:
                N = y > 0 and interior[y - 1, x]
                S = y + 1 < H and interior[y + 1, x]
                W_ = x > 0 and interior[y, x - 1]
                E = x + 1 < W and interior[y, x + 1]
                NW = y > 0 and x > 0 and interior[y - 1, x - 1]
                NE = y > 0 and x + 1 < W and interior[y - 1, x + 1]
                SW = y + 1 < H and x > 0 and interior[y + 1, x - 1]
                SE = y + 1 < H and x + 1 < W and interior[y + 1, x + 1]
                if S and E:
                    L[0, y, x] = 5562
                elif S and W_:
                    L[0, y, x] = 5561
                elif N and E:
                    L[0, y, x] = 5554
                elif N and W_:
                    L[0, y, x] = 5553
                elif S:
                    L[0, y, x] = 5534
                elif N:
                    L[0, y, x] = 5550
                elif E:
                    L[0, y, x] = 5541
                elif W_:
                    L[0, y, x] = 5543
                elif SE:
                    L[0, y, x] = 5533
                elif SW:
                    L[0, y, x] = 5535
                elif NE:
                    L[0, y, x] = 5549
                elif NW:
                    L[0, y, x] = 5551


def _tiles_list_34(L):
    _, H, W = L.shape
    out = []
    for z in range(3):
        for y in range(H):
            for x in range(W):
                t = int(L[z, y, x])
                if z == 0 or t != 0:
                    out.append({'tile': t, 'at': [x, y], 'layer': z})
    return out


# =================================================================================================
# 1. MAP 300 — RIMEHOLT - THANE'S HARBOUR (46x40, TS 52, Outdoor, :FROZEN_LAKE, rubric: true)
# =================================================================================================
def build_300():
    W, H = 46, 40
    m = _snowmap(W, H, 300, kit='shs3')
    rng = random.Random(30011)

    # ---- 1. Sculpt Frozen Nordic Timber-Wharf Capital on Lake Rime ----
    # Raised North Town Terrace (ht=1, y=0..17 -> cliff lip/face/base at y=17..19, leaving y=15..16 WIDE OPEN promenade!)
    for y in range(0, 18):
        for x in range(0, W):
            m.ht[y, x] = 1

    # Perimeter snowy spruce windbreaks along N, W (upper), E (upper), & outer harbor flanks
    for y in range(H):
        for x in range(W):
            if y <= 3 or x <= 3 or x >= W - 4:
                m.cls[y, x] = 'T'

    # Open the central Whalebone Keep North Causeway (x=20..26, y=0..17 -> exit x=21..25, y=0!)
    m.rect(20, 0, 7, 18, 'd', only='.T')
    # Open Upper Town Terrace plateau (x=4..41, y=4..17)
    m.rect(4, 4, 38, 14, '.', only='.T')
    m.rect(21, 0, 5, 18, 'd')
    # Open NW Net Row Spur (x=0..6, y=12..16) looping cleanly around west side of PC!
    m.rect(0, 12, 6, 5, 'd', only='.T')
    # Open 2-row Upper Terrace Promenade (y=15..16) connecting Net Row, PC, Mart, Keep Causeway & Lake Hall!
    m.rect(4, 15, 37, 2, 'd', only='.T')

    # Grand Stone Staircases descending from Upper Town Terrace (y=17..19) onto Harbor Wharf Plaza (y=20)!
    m.stairs(12, 17, w=3, n=3, c='d')
    m.stairs(22, 17, w=3, n=3, c='d')
    m.stairs(34, 17, w=3, n=3, c='d')

    # Lower Harbor Basin (y=20..39):
    for y in range(25, H):
        for x in range(0, W):
            if y >= 36:
                m.cls[y, x] = 'o'
            elif 4 <= x <= W - 5:
                m.cls[y, x] = 'I'
            else:
                m.cls[y, x] = 'o'

    # Carve organic steaming open harbor water leads ('w', tag==6!) right alongside timber piers (for [300] Surf/Fishing!)
    for y in range(29, 35):
        for x in range(7, 16):
            if (x == 7 and y in (29, 34)) or (x == 15 and y in (29, 34)):
                continue
            m.cls[y, x] = 'w'
    for y in range(28, 34):
        for x in range(30, 39):
            if (x == 30 and y in (28, 33)) or (x == 38 and y in (28, 33)):
                continue
            m.cls[y, x] = 'w'
    # Deep sea ice leads ('W') along outer southern perimeter y=37..39 (away from causeway x=20..26)
    for y in range(37, H):
        for x in range(0, W):
            if not (19 <= x <= 27) and m.cls[y, x] == 'o' and vnoise(x, y, 3007, 3.0) > 0.35:
                m.cls[y, x] = 'W'

    # Harbor Packed-Snow Sled Avenues & Plazas (y=20..24 cleanly below cliff!)
    m.rect(5, 20, 37, 5, 'd', only='.TI')
    m.rect(36, 20, 10, 5, 'd', only='.TI')                     # East road -> 304 Sled Market (x=45, y=20..24!)
    m.rect(0, 22, 10, 4, 'd', only='.TIo')                     # West road -> 309 Sinking Quarter (x=0, y=22..25!)
    m.rect(21, 20, 5, 20, 'd')                                 # South Icewall Causeway -> 303 (x=21..25, y=39!)
    m.rect(8, 25, 4, 3, 'd', only='.TI')                       # West fisher's packed-snow apron -> Old Torstein & West Pier
    m.rect(33, 25, 3, 2, 'd', only='.TI')                      # East wharf packed-snow lead-in -> East Pier
    m.lane([(23, 10), (37, 12)], c='d', w=2.0, seed=3002, only='.T')
    _smooth_cls(m, 'd', into='.', passes=1, only='.T')

    # Re-assert crisp exact open edge strips so all 4 directional exits are wide, centered & clean
    m.cls[0:3, 21:26] = 'd'          # North -> 305 Whalebone Keep Bailey
    m.cls[37:40, 21:26] = 'd'        # South -> 303 Icewall Gate
    m.cls[20:25, 42:46] = 'd'        # East  -> 304 Sled Market (y=20..24, cleanly below y=17..19 cliff!)
    m.cls[22:26, 0:4] = 'd'          # West  -> 309 Sinking Quarter
    m.cls[12:15, 0:6] = 'd'          # NW    -> 314 Net Row
    m.cls[15:17, 4:40] = 'd'         # Full upper terrace promenade

    # Clean flat snow yards beneath buildings BEFORE plan_cliffs
    for x0, y0, x1, y1 in (
        (6, 9, 14, 14),    # wb_pc (9x6) -> door (10,14), HealingSpot (10,15)
        (17, 9, 22, 14),   # wb_short Mart (6x6) -> door (20,14)
        (33, 4, 40, 11),   # kf_aframe2 Lake Hall Gym (8x8) -> door (37,10)
        (6, 2, 13, 7),     # wb_long2 Harbourmaster Hall (8x6) -> door (8,7)
        (27, 9, 31, 13),   # wb_hut Harbour Smokehouse (5x5) -> door (29,13)
    ):
        for yy in range(y0, y1 + 1):
            for xx in range(x0, x1 + 1):
                if m.inb(xx, yy):
                    m.cls[yy, xx] = '.'

    m.plan_cliffs(rows=3)

    # ---- 2. Iconic Isenmar Buildings: PC, Mart, Lake Hall Gym, Harbourmaster Hall & Smokehouse ----
    m.stamp('wb_pc', 6, 9)           # Door [10, 14] -> 301 Rimeholt PC!
    m.stamp('wb_short', 17, 9)       # Door [20, 14] -> 302 Rimeholt Mart!
    m.stamp('kf_aframe2', 33, 4)     # Glacial Ice Lake Hall (Gym 10) -> door [37, 10]!
    m.stamp('wb_long2', 6, 2)        # Harbourmaster's Longhouse
    m.stamp('wb_hut', 27, 9)         # Harbour Smokehouse (clean snow alley at x=32!)

    for dx, dy in ((10, 14), (20, 14), (29, 13), (8, 7)):
        _doorstep(m, (dx, dy), depth=2)

    # ---- 3. Events: Warps, Doors, Trials Board, Ch11 Cast (Anja, Juno, Tage, Torstein, Fishers) & Visible Pickups ----
    E = []
    # Bidirectional Doors: PC (RH_PC) & Mart (RH_MART)
    E.append({'type': 'door', 'name': 'Rimeholt PC door', 'at': [10, 14], 'gfx': ['', 0, 2], 'link': 'RH_PC', 'fixed': True})
    E.append({'type': 'door', 'name': 'Rimeholt Mart door', 'at': [20, 14], 'gfx': ['', 0, 2], 'link': 'RH_MART', 'fixed': True})

    # North Causeway -> 305 Whalebone Keep - Bailey (16, 30, up)
    for nx in range(21, 26):
        E.append({'type': 'warp', 'name': f'North to Whalebone Keep {nx}', 'at': [nx, 0],
                  'to': {'map': 305, 'x': 16, 'y': 30, 'dir': 'up'}, 'se': 'Door enter'})
    # South Causeway -> 303 Rimeholt - Icewall Gate (17, 8, down)
    for sx in range(21, 26):
        E.append({'type': 'warp', 'name': f'South to Icewall Gate {sx}', 'at': [sx, 39],
                  'to': {'map': 303, 'x': 17, 'y': 8, 'dir': 'down'}, 'se': 'Door enter'})
    # East Market Road -> 304 Rimeholt - Sled Market (1, 18, right)
    for ey in range(20, 25):
        E.append({'type': 'warp', 'name': f'East to Sled Market {ey}', 'at': [45, ey],
                  'to': {'map': 304, 'x': 1, 'y': 18, 'dir': 'right'}, 'se': 'Door enter'})

    # Guarded unbuilt exits (uppercase PBMoveRoute::BACKWARD, in-world lore!)
    sink_msg = (
        "Harbour Harpooner: Hold up, stranger — the ice shelves down toward the Sinking Quarter have been groaning "
        "since midday. Wait till the sounders finish marking safe floes before heading west!"
    )
    for wy in range(22, 26):
        E.append({'type': 'event', 'name': f'West to Sinking Quarter {wy}', 'at': [0, wy],
                  'pages': [{'trigger': 'touch', 'through': True,
                             'commands': _guarded_unbuilt_transfer(309, 38, 16, 'left', sink_msg)}]})

    net_msg = (
        "Net-Mender: Easy along the upper timber walk — the stilts down to Net Row are iced slick from tower steam. "
        "We're spreading ash across the planks now; stick to Thane's Harbour for the moment."
    )
    for ny in range(12, 15):
        E.append({'type': 'event', 'name': f'NW to Net Row {ny}', 'at': [0, ny],
                  'pages': [{'trigger': 'touch', 'through': True,
                             'commands': _guarded_unbuilt_transfer(314, 38, 14, 'left', net_msg)}]})

    gym_msg = (
        "Lake Hall Attendant: Rimeholt Lake Hall is closed while Warden Anja Sorrel drills the harbour children on "
        "thin-ice safety down on the frozen quay. Speak with her by the harbour piers first!"
    )
    E.append({'type': 'event', 'name': 'Rimeholt Lake Hall Door (310)', 'at': [37, 10],
              'pages': [{'trigger': 'touch', 'through': True,
                         'commands': _guarded_unbuilt_transfer(310, 10, 15, 'up', gym_msg)}]})

    # Rimeholt Harbour Tally Board -> pf_trial_board(:ISENMAR) (solid fw_stone at (26, 21)!)
    board_ruby = (
        'pbMessage(_INTL("RIMEHOLT HARBOUR TALLY BOARD — Notices of the Great Tally of Isenmar."))\n'
        'if defined?(pf_trial_board)\n'
        '  if pbConfirmMessage(_INTL("Check Isenmar\'s Tally notices?"))\n'
        '    pf_trial_board(:ISENMAR)\n'
        '  end\n'
        'end'
    )
    E.append({
        'type': 'event',
        'name': 'Rimeholt Tally Board',
        'at': [26, 21],
        'pages': [{'trigger': 'action', 'commands': [{'script': board_ruby}]}],
    })

    # Canonical Ch11 Cast on Thane's Harbour (story/30_SCRIPT_CH11.md:176-217)
    anja_ruby = (
        'if $game_switches[128]\n'
        '  pbMessage(_INTL("Warden Anja: I read the numbers every month, and I signed anyway because the heaters were warm."))\n'
        '  pbMessage(_INTL("Warden Anja: Now my brother holds court in Whalebone Keep. Walk straight up the north causeway when you\'re ready."))\n'
        'else\n'
        '  pbMessage(_INTL("Warden Anja: What do you do when the ice sings? Lie down flat. What do you do when the lake breathes? RUN — to the towers."))\n'
        '  pbMessage(_INTL("Warden Anja: You\'re the badge-hunter with no colour. The Lake Hall sits up on the north-east terrace — don\'t walk on the grey ice."))\n'
        '  pbMessage(_INTL("Warden Anja: That green-sashed girl from Verdance wanted me to choose between her policy paper and my grandchildren\'s toes. Easy choice. Toes. Every time."))\n'
        'end'
    )
    E.append({'type': 'event', 'name': 'Warden Anja Sorrel', 'at': [19, 24],
              'pages': [{'graphic': {'sprite': 'ANJA', 'dir': 'down'}, 'trigger': 'action', 'move': 'fixed',
                         'commands': [{'script': anja_ruby}]}]})

    juno_ruby = (
        'if $game_switches[128]\n'
        '  pbMessage(_INTL("Juno: Everything\'s warm, and everything\'s growing, and nobody asks what it\'s drinking... That\'s what Uncle Rowan meant."))\n'
        'else\n'
        '  pbMessage(_INTL("Juno: I had a second page on sustainable Imprint stewardship, and Warden Anja asked me how many toes I had!"))\n'
        '  pbMessage(_INTL("Juno: She\'s terrifying. I want her to like me so much."))\n'
        'end'
    )
    E.append({'type': 'event', 'name': 'Juno Hale', 'at': [18, 25],
              'pages': [{'graphic': {'sprite': 'JUNO', 'dir': 'up'}, 'trigger': 'action', 'move': 'fixed',
                         'commands': [{'script': juno_ruby}]}]})

    # Heat-Tower Technician Tage beside Tower Two (29, 26)
    E.append(_make_npc('Technician Tage', (28, 26), 'NPC 18', 'right', [
        "Tage: Tower Two's running at a hundred and twelve percent, and Tower Three's ticking up beside it. It's fine. It's within tolerance.",
        "Tage: ...The tolerance was raised in the spring. Everything's within tolerance if you raise the tolerance.",
    ]))

    # Old Torstein on the West Ice-Fishing Flats (story/30_SCRIPT_CH11.md:216; IS_ELEVEN_YEARS!)
    E.append(_make_npc('Old Torstein', (11, 27), 'NPC 25', 'down', [
        "Old Torstein: Eleven years I've fished this exact hole, friend. Eleven winters! Something's been nibbling my line since Tuesday.",
        "Old Torstein: Eh? Why is my ice-stool breathing? Nonsense, that's just the lake wind under my coat. Quiet now, you'll spook the bite!",
    ]))

    # Harbour Ice-Fisher by the Steaming Open Lead (hints at [300] Water/Rod encounters!)
    E.append(_make_npc('Harbour Ice-Fisher', (31, 27), 'NPC 20', 'down', [
        "Ice-Fisher: Thirty years I've cut holes on Lake Rime. They always freeze shut by morning. This open water by the towers has been steaming since midsummer.",
        "Ice-Fisher: Seel, Spheal, and even Lapras swim right up to the timber wharves here — cast a rod off the planks if you want a cold-water catch!",
    ]))

    # Western Harpooner Watch & Harbour Child
    E.append(_make_npc('Harpooner Watch', (4, 23), 'trainer_HARPOONER', 'right', [
        "Harpooner Watch: Whalebone Keep rises straight north across the frozen narrows. Thane Eirik's lamps never go out up on the rock.",
    ]))
    E.append(_make_npc('Harbour Skater', (24, 27), 'NPC 01', 'left', [
        "Harbour Skater: Gran Anja says when the lake breathes, you run for the heat-tower pilings — they're the only things bolted down to bedrock!",
    ]))

    # Solid Harbor Signposts (ALL backed by pas=0xf pf_signpost / pf_pcsign -> 0 over_trigger?!)
    E.append(_sign('Rimeholt Welcome Sign', (20, 35),
                   "RIMEHOLT — THANE'S HARBOUR\n↑ Whalebone Keep · → Sled Market · ↗ Lake Hall (Gym 10) · ↓ Icewall Gate"))
    E.append(_sign('Rimeholt PC Sign', (15, 14),
                   "RIMEHOLT POKÉMON CENTER — Warm hearths, Gale Post Circular & full recovery for frosty teams."))
    E.append(_sign('Rimeholt Mart Sign', (23, 14),
                   "RIMEHOLT PROVISIONER & MART — Dive Balls, Net Balls, Ice Heals & winter expedition stock."))
    E.append(_sign('Lake Hall Sign', (39, 13),
                   "RIMEHOLT LAKE HALL (GYM 10)\nWarden: ANJA SORREL — 'Ice remembers.'"))

    # Visible & Hidden Pickups (explicit hidden=False on every visible item -> Object ball!)
    E.append({'type': 'item', 'name': 'Item (Dive Ball)', 'at': [9, 32], 'item': 'DIVEBALL', 'hidden': False})
    E.append({'type': 'item', 'name': 'Item (Big Pearl)', 'at': [39, 25], 'item': 'BIGPEARL', 'hidden': False})
    E.append({'type': 'item', 'name': 'HiddenItem (Pearl)', 'at': [16, 35], 'item': 'PEARL', 'hidden': True})

    ev_mask = _reserve_mask(m, E, extra=[
        (10, 15), (20, 15), (37, 11), (37, 12), (23, 1), (23, 38), (44, 22), (1, 23), (1, 13), (5, 13), (5, 15),
        (12, 16), (13, 16), (14, 16), (22, 16), (23, 16), (24, 16), (34, 16), (35, 16), (36, 16),
        (12, 20), (13, 20), (14, 20), (22, 20), (23, 20), (24, 20), (34, 20), (35, 20), (36, 20),
    ], pad=1)

    # ---- 4. Harbour Props, Meridian Heat-Towers, Signposts, Ice Boats, Fish Racks, Braziers & Lanterns ----
    # Exact solid signposts & Tally Rune Stone matching sign/board events (0 over_trigger?!)
    m.stamp('pf_signpost', 20, 34)       # base (20, 35)
    m.stamp('pf_pcsign', 15, 13)         # base (15, 14) right beside wb_pc!
    m.stamp('pf_signpost', 23, 13)       # base (23, 14) right beside wb_short Mart!
    m.stamp('pf_signpost', 39, 12)       # base (39, 13)
    m.stamp('fw_stone', 26, 20)          # Great Tally Harbour Stone -> base (26, 21)!

    # Meridian Heat-Towers (lm_pylon 2x5) standing on the Harbor Ice with steaming vents!
    for tx, ty in ((29, 22), (16, 26), (39, 29)):
        m.stamp('lm_pylon', tx, ty, mark='B')
        if m.inb(tx, ty - 1):
            m.over.append((2, tx, ty - 1, P1('lm_steam0')))
        if m.inb(tx + 1, ty - 1):
            m.over.append((2, tx + 1, ty - 1, P1('lm_steam1')))

    # Crisp Nordic Harbour Props: Ice-fishing holes, boats, fish racks, stalls, sleds, braziers, banners & lanterns!
    for nm, x, y in (
        ('fw_stall_i', 16, 20), ('fw_stall_i', 14, 3),
        ('hb_fishstall', 6, 20),
        ('fw_brazier', 20, 2), ('fw_brazier', 26, 2),
        ('fw_brazier', 20, 21), ('fw_brazier', 26, 24),
        ('fw_brazier', 20, 37), ('fw_brazier', 26, 37),
        ('fw_brazier', 42, 19), ('fw_brazier', 42, 25),
        ('fw_brazier', 34, 12), ('fw_brazier', 38, 12),
        ('wr_ban_ise', 19, 1), ('wr_ban_ise', 27, 1),
        ('wr_ban_ise', 19, 36), ('wr_ban_ise', 27, 36),
        ('fw_ban_i', 5, 13), ('fw_ban_i', 16, 13), ('fw_ban_i', 26, 13),
        ('fw_boat', 12, 34), ('fw_boat', 33, 34), ('fw_boat_over', 17, 34), ('fw_boat_over', 28, 34),
        ('hb_boat1', 4, 30), ('hb_boat2', 36, 25),
        ('fw_rack', 4, 26), ('fw_rack', 39, 21), ('fw_rack', 15, 5), ('fw_rack', 27, 4),
        ('fw_sled', 14, 24), ('pf_sledge', 33, 21), ('fw_sled', 28, 20),
        ('fw_wood', 4, 9), ('fw_wood', 24, 13), ('fw_wood', 40, 14), ('fw_wood', 33, 24),
        ('fw_skull', 18, 4), ('fw_skull', 28, 3),
        ('sh_crates', 40, 20), ('hb_barrels', 13, 21), ('hb_barrels', 32, 20),
        ('hb_crane', 5, 29), ('pf_anchor', 17, 29),
        ('pf_logbench', 12, 23), ('pf_logbench', 35, 22),
        ('pf_lantern', 4, 14), ('pf_lantern', 32, 14), ('pf_lantern', 40, 14),
        ('pf_lantern', 20, 26), ('pf_lantern', 26, 26), ('pf_lantern', 20, 31), ('pf_lantern', 26, 31),
        ('pf_lantern', 4, 20), ('pf_lantern', 41, 20),
    ):
        s = STAMPS[nm]
        if m.inb(x, y) and m.free(x, y, s['w'], s['h'], on='.deI') and not ev_mask[y:y + s['h'], x:x + s['w']].any():
            m.stamp(nm, x, y, mark='B')

    # Decorative snow-pines framing upper terraces & flank edges
    for tx, ty, sp in (
        (4, 3, KF_TEAL_PINE_A), (15, 1, KF_SPRUCE_A), (28, 1, KF_SPRUCE_B), (41, 4, KF_TEAL_PINE_B),
        (41, 8, KF_TEAL_PINE_A), (41, 12, KF_TEAL_PINE_B), (41, 25, KF_SPRUCE_A),
        (4, 24, KF_SHRUB_A), (40, 29, KF_SHRUB_B), (18, 6, KF_BOULDER), (29, 6, KF_BOULDER),
    ):
        _put_sprite(m, tx, ty, *sp, on='.T', avoid_mask=ev_mask)

    # Interlocking Alpine Spruce Forest for all 'T' woodland borders
    R_ = types.SimpleNamespace(m=m, seed=300, road_mask=np.isin(m.cls, ['d']), events=E, rng=rng)
    CK.thin_bands(R_, passes=1)
    CK.woods(R_, ALPINE_WOODS, scale=8.0, accents={'snowblue': 0.08})

    m.events = E
    m.paint()
    _infill_winter(R_, ALPINE_WOODS, scale=8.0, seed=300)

    # Paint weathered timber fishing wharves jutting right into the steaming open harbor water (tag==6)!
    _paint_wharf(m, 8, 28, 10, 33)
    _paint_wharf(m, 33, 26, 35, 31)
    # Paint crisp 3-wide weathered timber plank walk leading cleanly into NW Net Row exit (0..4, 12..14)!
    _paint_wharf(m, 0, 12, 4, 14)
    # Place crisp ice-fishing hole right below Old Torstein (11, 28) & beside Heat-Tower Two (29, 27)!
    m.L[1, 28, 11] = P1('fw_hole')
    m.L[1, 27, 29] = P1('fw_hole_t')
    for bx, by in ((8, 33), (10, 33), (33, 31), (35, 31)):
        m.L[1, by, bx] = P1('hb_bollard0')

    # Ensure kf_aframe2 Lake Hall door (37, 10) & step-in (37, 11) are cleanly walkable
    m.L[2, 10, 37] = 0
    m.L[2, 11, 37] = 0
    m.L[1, 11, 37] = 0

    _dress_snow_details(m, ev_mask, seed=3003, drift_p=0.18, track_p=0.18, crack_p=0.28)

    # Seal any stray walkable outer border cell outside exact warp/touch tiles
    open_300 = ([(x, 0) for x in range(21, 26)] + [(x, H - 1) for x in range(21, 26)] +
                [(W - 1, y) for y in range(20, 25)] + [(0, y) for y in range(22, 26)] +
                [(0, y) for y in range(12, 15)])
    _seal_unconnected_edges(m, open_cells=open_300)

    Lr = RC.resolve(m.L, TID_SNOW).astype(np.int32)
    ev_pts = [tuple(e['at']) for e in E]
    PG.guard(Lr, TID_SNOW, ev_pts, 'Map 300')
    assert not PG.hits(Lr, R.tilesets()[TID_SNOW], ev_pts), 'Map 300 passguard hits!'
    _verify_map(Lr, TID_SNOW, E, (23, 37), 'Map 300 Rimeholt - Thane\'s Harbour', outdoor=True, require_water=True)

    os.makedirs(RAW_DIR, exist_ok=True)
    np.save(os.path.join(RAW_DIR, '300.npy'), Lr.astype(np.int16))
    spec = {
        'id': 300,
        'name': "Rimeholt - Thane's Harbour",
        'parent': 0,
        'bgm': 'Lerucean Town',
        'field': 'FROZEN_LAKE',
        'rubric': True,
        'yards_ok': True,
        'map_audio': {'bgm': 'Town - Isenmar', 'bgs': 'Wind - Isenmar', 'bgs_volume': 55},
        'tone': [-10, -4, 14, 10],
        'fog': {'name': 'prismfall_seamist', 'opacity': 24, 'blend': 0, 'zoom': 100, 'sx': 1, 'sy': 0},
        'metadata': {
            'Name': "Rimeholt - Thane's Harbour",
            'Outdoor': True,
            'ShowArea': True,
            'Bicycle': True,
            'MapPosition': RIME_POS,
            'BattleBack': 'snow',
            'Weather': ['Snow', 20],
        },
        'biome': 'city',
        'tileset': TID_SNOW,
        'raw': 'data/raw/300.npy',
        'events': E,
    }
    with open(os.path.join(SPEC_DIR, '300_rimeholt_thanes_harbour.yaml'), 'w', encoding='utf-8') as f:
        f.write("# GENERATED by mapgen/layouts/rimeholt_town.py (Batch 3H): Rimeholt - Thane's Harbour.\n")
        f.write(yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))
    print('Wrote specs/300_rimeholt_thanes_harbour.yaml and data/raw/300.npy')
    return Lr


# =================================================================================================
# 2. MAP 301 — RIMEHOLT POKÉMON CENTER (15x11, TS 34 — Exact 591/221 Alpine-Nordic Gold Standard!)
# =================================================================================================
def build_301():
    W, H = 15, 11
    L = np.zeros((3, H, W), dtype=np.int32)
    floor = np.zeros((H, W), dtype=bool)
    floor[2:9, 1:14] = True
    floor[8, 1] = False
    floor[8, 13] = False
    floor[9, 5:10] = True
    floor[10, 6:9] = True

    _seam_alpine_ts34(L, floor, wall_rows=2)

    # Multi-zone Alpine-Nordic Center flooring: frost-blue slate wings + cream-stone central heart + 5x4 Pokéball medallion!
    _put_9slice34(L, ALPINE_SLATE, 1, 2, 3, 8, z=0, mask=floor)
    _put_9slice34(L, ALPINE_SLATE, 11, 2, 13, 8, z=0, mask=floor)
    _put_9slice34(L, CREAM_STONE, 4, 2, 10, 8, z=0, mask=floor)
    _put_9slice34(L, CREAM_STONE, 5, 9, 9, 9, z=0, mask=floor)
    _put_9slice34(L, CREAM_STONE, 6, 10, 8, 10, z=0, mask=floor)
    _put_grid34(L, POKEBALL_MEDAL_5X4, 5, 4, z_rows=(0, 0, 0, 0))
    # Plush crimson welcome runner flowing cleanly into ALL 3 exit tiles (6..8, 10)
    _put_9slice34(L, RED_CARPET, 6, 9, 8, 10, z=1)

    # North wall (y=0..1): frosted west alpine window, twin brass sconces flanking Nurse (0 window behind Nurse!), PC & unobstructed Town Map!
    _put_grid34(L, ALPINE_WINDOW, 2, 0, z_rows=(1, 1))
    L[1, 0, 4] = 2308
    L[1, 0, 10] = 2309
    L[2, 1, 11] = 5847
    L[1, 2, 11] = 5855
    _put_grid34(L, GEO_MAP, 12, 0, z_rows=(1, 1))

    # Symmetrical 5-wide warm-timber 0x8f U-counter centered over Pokéball medallion (x=5..9, y=2..3)
    L[1, 2, 5] = 5952
    L[1, 2, 9] = 5955
    for dx, t in enumerate((5960, 5961, 5962, 5961, 5963)):
        L[1, 3, 5 + dx] = t
    # Healing pod nestled inside left bay (6..7, 1..2) -> Healing balls at [7, 2]
    L[2, 1, 6] = 6035; L[2, 1, 7] = 6036
    L[1, 2, 6] = 6043; L[1, 2, 7] = 6044

    # West Wing: Crackling Cast-Iron Woodstove with kettle, Warm Lounge Sofa & Gale Post Circular Desk!
    L[2, 2, 1] = 2470; L[1, 3, 1] = 2478
    _put_grid34(L, [[6024, 6026], [6032, 6034]], 2, 3, z_rows=(2, 1))
    _put_grid34(L, [[3466, 3467], [3474, 3475]], 1, 6, z_rows=(1, 1))
    L[2, 6, 1] = 3428
    L[2, 6, 2] = 4528

    # East Wing: Uncrowded Town Map above (12..13, 2) 100% OPEN! Supply Shelf (12..13, 4..6) & Warm Lamp (12, 7..8)
    _put_tf34(L, 'shelf_goods', 12, 4)
    L[2, 7, 12] = 2247; L[1, 8, 12] = 2255
    L[1, 9, 5] = 4077
    L[1, 9, 9] = 4077
    L[1, 8, 2] = 7177

    # Programmatic assertion: ALL 7 U-counter tiles carry exact 0x8f counter flag!
    ts34 = R.tilesets()[TID_INT]
    for cx, cy in ((5, 2), (9, 2), (5, 3), (6, 3), (7, 3), (8, 3), (9, 3)):
        t = int(L[1, cy, cx])
        assert ts34['passages'][t] == 0x8f, f'301 counter ({cx},{cy}) tile {t} pas={hex(ts34["passages"][t])} != 0x8f!'

    # Canonical Events (Full 3-wide exit warps (6..8, 10) <-> RH_PC; NPC 16 ONLY on Nurse!)
    events = [
        {'type': 'exit', 'name': 'Exit West', 'at': [6, 10], 'link': 'RH_PC', 'arrive': [7, 10, 'up']},
        {'type': 'exit', 'name': 'Exit Center', 'at': [7, 10], 'link': 'RH_PC', 'arrive': [7, 10, 'up']},
        {'type': 'exit', 'name': 'Exit East', 'at': [8, 10], 'link': 'RH_PC', 'arrive': [7, 10, 'up']},
        {
            'type': 'event',
            'name': 'Gale Post Clerk',
            'at': [3, 6],
            'pages': [
                {
                    'graphic': {'sprite': 'NPC 14', 'dir': 'right'},
                    'trigger': 'action',
                    'commands': [
                        "Gale Post Clerk: Gale Post — Rimeholt Harbour Relay! Here's the latest Wardens' Circular off the line:",
                        '"EBB GUILD VOTES TO STRIKE IF THE THANE\'S LEVY COMES DOWN THE ROAD. If you\'re a Warden and you\'ve got sleds, don\'t lend them to a war. — Marisol Reyes"',
                        '"Rotom says hi. — Rook"',
                        {'selfswitch': ['A', True]},
                    ],
                },
                {
                    'cond': {'self': 'A'},
                    'graphic': {'sprite': 'NPC 14', 'dir': 'right'},
                    'trigger': 'action',
                    'commands': [
                        "Gale Post Clerk: Airship mail from Skyreach meets our sled-relays out at Anchorhold on the Mast Glacier. Stay warm out there!",
                    ],
                },
            ],
        },
        _make_npc('Harbour Skald', (10, 6), 'NPC 22', 'left', [
            "Harbour Skald: Warden Anja fights on the Frozen Lake field — Ice moves strike half again as hard, and skaters pick up speed.",
            "Harbour Skald: Heavy Fire or Earthquake blows crack the lake into open Water Surface — though watch out for her Mega Glalie sealing those cracks shut!",
        ]),
        _make_npc('Sled-Driver', (1, 4), 'NPC 20', 'up', [
            "Sled-Driver: Nothing beats a cast-iron kettle after crossing the Whalebone Road. Even the towers can't match real birchwood heat.",
        ]),
    ]
    take_events = [
        {'template': 'pokecenter', 'name': 'Nurse', 'at': [8, 2]},
        {'template': 'pokecenter', 'name': 'Healing balls', 'at': [7, 2]},
        {'template': 'pokecenter', 'name': 'PC', 'at': [11, 2]},
        {'template': 'pokecenter', 'name': 'Town Map, size(2,1)', 'at': [12, 1]},
    ]

    ev_pts = [(6, 10), (7, 10), (8, 10), (7, 9), (8, 4), (8, 2), (7, 2), (11, 3), (11, 2), (12, 2), (13, 2), (3, 6), (10, 6), (1, 4)]
    PG.guard(L, TID_INT, ev_pts, 'Map 301')
    assert not PG.hits(L, ts34, ev_pts), 'Map 301 passguard hits!'
    _verify_map(L, TID_INT, events, start=(7, 9), label='Map 301 Rimeholt PC', outdoor=False, targets=[
        ('Exit West', (6, 10), False), ('Exit Center', (7, 10), False), ('Exit East', (8, 10), False),
        ('Nurse counter spot', (8, 4), False), ('PC stand spot', (11, 3), False),
        ('Town Map stand L', (12, 2), False), ('Town Map stand R', (13, 2), False),
        ('Gale Post Clerk', (3, 6), True), ('Harbour Skald', (10, 6), True), ('Sled-Driver', (1, 4), True),
    ])

    np.save(os.path.join(RAW_DIR, '301.npy'), L.astype(np.int16))
    spec = {
        'id': 301,
        'name': 'Rimeholt Pokémon Center',
        'parent': 300,
        'bgm': 'Poke Center',
        'map_audio': {'bgs': ''},
        'tone': [6, 2, -6, 0],
        'metadata': {
            'ShowArea': False,
            'HealingSpot': RIME_HEAL_SPOT,
            'MapPosition': RIME_POS,
        },
        'biome': 'interior',
        'palette': 'interior',
        'tileset': TID_INT,
        'map': '\n'.join(['.' * W] * H) + '\n',
        'tiles': _tiles_list_34(L),
        'events': events,
        'take_events': take_events,
    }
    with open(os.path.join(SPEC_DIR, '301_rimeholt_pc.yaml'), 'w', encoding='utf-8') as f:
        f.write('# GENERATED by mapgen/layouts/rimeholt_town.py (Batch 3H): Rimeholt Pokémon Center.\n')
        f.write(yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))
    print('Wrote specs/301_rimeholt_pc.yaml and data/raw/301.npy')
    return L


# =================================================================================================
# 3. MAP 302 — RIMEHOLT MART (12x10, TS 34 — Exact 222/202 Gold Standard!)
# =================================================================================================
def build_302():
    W, H = 12, 10
    L = np.zeros((3, H, W), dtype=np.int32)
    floor = np.zeros((H, W), dtype=bool)
    floor[2:9, 1:11] = True
    floor[8, 1] = False
    floor[8, 10] = False
    floor[9, 5:7] = True

    _seam_alpine_ts34(L, floor, wall_rows=2)
    _put_9slice34(L, ALPINE_SLATE, 1, 2, 10, 8, z=0, mask=floor)
    _put_9slice34(L, ALPINE_SLATE, 5, 9, 6, 9, z=0, mask=floor)
    _put_9slice34(L, DARK_WOOD, 4, 2, 9, 7, z=0, mask=floor)
    _put_9slice34(L, BROWN_WOVEN_RUG, 4, 4, 6, 7, z=1, mask=floor)
    # Complete un-sliced 2x2 crimson welcome mat spanning (5..6, 8..9)
    L[1, 8, 5] = 7172; L[1, 8, 6] = 7174
    L[1, 9, 5] = 7188; L[1, 9, 6] = 7190

    # North wall: cleanly spaced frosted alpine windows & Isenmar Trade Map
    _put_grid34(L, ALPINE_WINDOW, 1, 0, z_rows=(1, 1))
    _put_grid34(L, ALPINE_WINDOW, 4, 0, z_rows=(1, 1))
    _put_grid34(L, GEO_MAP, 7, 0, z_rows=(1, 1))

    # Flush 5-tile warm-timber 0x8f Mart Counter wrapping Clerk at (2, 3)
    L[1, 2, 3] = 5971
    L[1, 3, 3] = 5971
    L[1, 4, 1] = 5962
    L[1, 4, 2] = 5961
    L[1, 4, 3] = 5963
    ts34 = R.tilesets()[TID_INT]
    for cx, cy in ((3, 2), (3, 3), (1, 4), (2, 4), (3, 4)):
        t = int(L[1, cy, cx])
        assert ts34['passages'][t] == 0x8f, f'302 counter ({cx},{cy}) tile {t} pas={hex(ts34["passages"][t])} != 0x8f!'

    # Stocked shelves, frost-tonic bottles, iron supply crate & airy east aisle
    _put_tf34(L, 'shelf_goods', 9, 2)
    _put_tf34(L, 'shelf_bottles', 8, 5)
    _put_tf34(L, 'crate_i', 1, 5)
    L[1, 7, 1] = 4101
    L[1, 7, 2] = 7177
    L[1, 7, 10] = 7178
    L[2, 7, 9] = 2271
    L[1, 8, 9] = 2279

    # Twin exit warps (5..6, 9) <-> RH_MART + canonical Ch11 PBS winter/healing stock!
    events = [
        {'type': 'exit', 'name': 'Exit West', 'at': [5, 9], 'link': 'RH_MART', 'arrive': [5, 9, 'up']},
        {'type': 'exit', 'name': 'Exit East', 'at': [6, 9], 'link': 'RH_MART', 'arrive': [5, 9, 'up']},
        {
            'type': 'mart',
            'name': 'Mart Clerk',
            'at': [2, 3],
            'sprite': 'NPC 19',
            'dir': 'right',
            'greeting': "Mart Clerk: Welcome to Rimeholt Mart! Stock up on Dive Balls, Ice Heals, and Max Potions before stepping onto Lake Rime!",
            'items': [
                'POKEBALL', 'GREATBALL', 'ULTRABALL', 'DIVEBALL', 'NETBALL', 'DUSKBALL',
                'HYPERPOTION', 'MAXPOTION', 'FULLHEAL', 'ICEHEAL', 'REVIVE',
                'ESCAPEROPE', 'SUPERREPEL',
            ],
        },
        _make_npc('Hoarwood Fur-Trader', (7, 6), 'NPC 17', 'right', [
            "Fur-Trader: Firewood's dear this year, and half the city stopped buying it once Meridian lit the heat-towers.",
            "Fur-Trader: Still, I keep my pack stuffed with Ice Heals and Revives. A winter storm doesn't read a Meridian contract.",
        ]),
    ]

    ev_pts = [(5, 9), (6, 9), (5, 8), (6, 8), (4, 3), (2, 3), (7, 6)]
    PG.guard(L, TID_INT, ev_pts, 'Map 302')
    assert not PG.hits(L, ts34, ev_pts), 'Map 302 passguard hits!'
    _verify_map(L, TID_INT, events, start=(5, 8), label='Map 302 Rimeholt Mart', outdoor=False, targets=[
        ('Exit West', (5, 9), False), ('Exit East', (6, 9), False),
        ('Mart Clerk counter spot', (4, 3), False), ('Hoarwood Fur-Trader', (7, 6), True),
    ])

    np.save(os.path.join(RAW_DIR, '302.npy'), L.astype(np.int16))
    spec = {
        'id': 302,
        'name': 'Rimeholt Mart',
        'parent': 300,
        'bgm': 'Poke Mart',
        'map_audio': {'bgs': ''},
        'tone': [6, 2, -6, 0],
        'metadata': {'MapPosition': RIME_POS},
        'biome': 'interior',
        'tileset': TID_INT,
        'raw': 'data/raw/302.npy',
        'events': events,
    }
    with open(os.path.join(SPEC_DIR, '302_rimeholt_mart.yaml'), 'w', encoding='utf-8') as f:
        f.write('# GENERATED by mapgen/layouts/rimeholt_town.py (Batch 3H): Rimeholt Mart.\n')
        f.write(yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))
    print('Wrote specs/302_rimeholt_mart.yaml and data/raw/302.npy')
    return L


# =================================================================================================
# 4. MAP 303 — RIMEHOLT - ICEWALL GATE (40x24, TS 52, Outdoor, :FROZEN_LAKE, rubric: true)
# =================================================================================================
def build_303():
    W, H = 40, 24
    m = _snowmap(W, H, 303, kit='shs3')
    rng = random.Random(30311)

    # ---- 1. Monumental Flush Cut-Stone Curtain Walls, Twin-Towered Gatehouses & 2 Corner Watchtowers ----
    # Dense overlapping alpine snow-spruce & glacial flank walls along West (x=0..3), East (x=36..39), & North ridge (y=0..3)!
    for y in range(H):
        for x in range(W):
            if x < 4 or x > W - 5 or y <= 3 or y > H - 2:
                m.cls[y, x] = 'T'

    m.plan_cliffs(rows=3)

    # Carve central snow-drifted Barbican Parade Yard & twin gatehouse approaches
    m.rect(5, 7, 30, 12, '.')
    m.rect(14, 4, 8, 20, 'd')
    # Frozen lake-ice court hugging the East Heat-Tower yard (x=21..33, y=9..18) vs packed snow West Guard Yard!
    m.rect(21, 9, 13, 9, 'I', only='.Td')
    m.rect(15, 7, 6, 16, 'd')
    m.lane([(7, 14), (15, 13), (25, 14), (32, 13)], c='d', w=2.4, seed=3031, only='.TI', wobble=0.18)
    _smooth_cls(m, 'd', into='.', passes=1, only='.TI')
    m.rect(15, 7, 6, 3, 'd')

    # ---- 2. Monumental Gatehouses, 2 Corner Watchtowers & West Guard Lodge (ZERO cloned turret spam!) ----
    m.stamp('gt_gate6', 12, 0)       # North Inner Icewall Gate (12x8 -> open 6-wide arch x=15..20, y=6..7!)
    m.stamp('gt_tower', 4, 1)        # NW Corner Watchtower (ONLY 2 outer towers!)
    m.stamp('gt_tower', 33, 1)       # NE Corner Watchtower
    m.stamp('gt_gate4', 13, 16)      # South Outer Whalebone Road Gate (10x8 -> open 4-wide arch x=16..19, y=22..23!)
    m.stamp('wb_short', 5, 8)        # West Guard Lodge (6x6 -> x=5..10, y=8..13)

    # ---- 3. Events: Full 6-Wide North -> 300, BACKWARD-Guarded South -> 712, Ch11 Gate Skald, Climbers & Scanner ----
    E = []
    # Full 6-wide North Icewall Arch (15..20, 6) -> 300 Thane's Harbour (23, 38) up
    for nx in range(15, 21):
        E.append({'type': 'warp', 'name': f'North to Thanes Harbour {nx}', 'at': [nx, 6],
                  'to': {'map': 300, 'x': 23, 'y': 38, 'dir': 'up'}, 'se': 'Door enter'})

    # Full 4-wide South Gate Arch (16..19, 22) -> PBMoveRoute::BACKWARD-guarded exit to unbuilt 712 The Whalebone Road!
    whale_msg = (
        "Icewall Watchman: Hold there, traveller — blizzard squalls have buried the whale-rib arches south along "
        "the Whalebone Road toward Frostfang Pass. Sled-crews are digging a track through; step north into Thane's Harbour for now."
    )
    for sx in (16, 17, 18, 19):
        E.append({'type': 'event', 'name': f'South to Whalebone Road {sx}', 'at': [sx, 22],
                  'pages': [{'trigger': 'touch', 'through': True,
                             'commands': _guarded_unbuilt_transfer(712, 36, 4, 'down', whale_msg)}]})

    # Canonical Ch11 Gate Skald (story/30_SCRIPT_CH11.md:168-170)
    skald_ruby = (
        'if $game_switches[128]\n'
        '  pbMessage(_INTL("Gate Skald: I told them the ice past the towers was thin. They had a machine that said it was fine. The lake didn\'t read the machine."))\n'
        'else\n'
        '  pbMessage(_INTL("Gate Skald: Mind the ice past the towers inside the city. It\'s thin."))\n'
        '  pbMessage(_INTL("Gate Skald: It\'s been thin since the summer. They say it\'s fine. They\'ve got a machine that says it\'s fine."))\n'
        'end'
    )
    E.append({'type': 'event', 'name': 'Gate Skald', 'at': [14, 15],
              'pages': [{'graphic': {'sprite': 'NPC 21', 'dir': 'right'}, 'trigger': 'action', 'move': 'fixed',
                         'commands': [{'script': skald_ruby}]}]})

    # Icewall Warden Captain (reactive to V132 / S128 & Ch11 "Toes" / evacuation lore)
    cap_ruby = (
        'if $game_variables[132] >= 7 || $game_switches[128]\n'
        '  pbMessage(_INTL("Icewall Captain: By order of Thane Eirik, south-bound family sleds have right of way through the Icewall Gate."))\n'
        '  pbMessage(_INTL("Icewall Captain: Keep your lantern lit — the road south over Frostfang is crowded tonight."))\n'
        'else\n'
        '  pbMessage(_INTL("Icewall Captain: Welcome to Rimeholt. Warden Anja\'s down on Thane\'s Harbour drilling the schoolkids — and arguing with a very determined girl from Verdance."))\n'
        '  pbMessage(_INTL("Icewall Captain: Follow the north arch straight out onto the harbour flats."))\n'
        'end'
    )
    E.append({'type': 'event', 'name': 'Icewall Captain', 'at': [14, 9],
              'pages': [{'graphic': {'sprite': 'trainer_ISENMAR_OFFICER', 'dir': 'down'}, 'trigger': 'action', 'move': 'fixed',
                         'commands': [{'script': cap_ruby}]}]})

    E.append(_make_npc('Icewall Sentry', (21, 9), 'trainer_ISENMAR_SOLDIER_M', 'down', [
        "Icewall Sentry: Packed glacial stone, cut whale-ribs, and Meridian's shiny brass scanner arch bolted straight on top of it.",
        "Icewall Sentry: Funny how the old ice never needed a power bill to stay standing.",
    ]))

    # Canonical Ch11 Ice-Climber Pair by the East Icewall Face (story/30_SCRIPT_CH11.md:526)
    E.append(_make_npc('Ice-Climber Halvor', (28, 12), 'NPC 18', 'up', [
        "Ice-Climber Halvor: We test pitons along the east curtain of the Icewall every morning before the sun hits it.",
        "Ice-Climber Halvor: Once you've got Warden Anja's Sounding Badge, ask around the wall — a good Rock Climb harness gets you down sheer faces as cleanly as up.",
    ]))

    # Solid Signpost (Meridian Scanner Arch notice) & Gate Notice (0 over_trigger?!)
    E.append(_sign('Icewall Gate Sign', (12, 15),
                   "RIMEHOLT — ICEWALL GATE\n↑ Thane's Harbour & Whalebone Keep · ↓ The Whalebone Road & Frostfang Pass"))
    E.append(_sign('Meridian Scanner Plaque', (22, 15),
                   "◆ PRIORITY GUEST ◆ Welcome to Rimeholt. Warmth is a right. — Meridian Heat Services."))

    # Pickups (explicit hidden=False on visible item!)
    E.append({'type': 'item', 'name': 'Item (Hyper Potion)', 'at': [8, 17], 'item': 'HYPERPOTION', 'hidden': False})
    E.append({'type': 'item', 'name': 'HiddenItem (Snowball)', 'at': [30, 17], 'item': 'SNOWBALL', 'hidden': True})

    ev_mask = _reserve_mask(m, E, extra=[
        (15, 7), (16, 7), (17, 7), (18, 7), (19, 7), (20, 7), (17, 8), (18, 8),
        (16, 21), (17, 21), (18, 21), (19, 21), (17, 20), (18, 20), (12, 14), (22, 14),
    ], pad=1)

    # ---- 4. Stone/Ice Parapets, Blazing Watch-Beacons, Steaming Tower Hole, Braziers & Snow Spruce Flanks ----
    m.stamp('pf_signpost', 12, 14)   # rustic wood Icewall Gate Sign -> solid base (12, 15)
    m.stamp('lm_news', 22, 14)       # distinct teal metallic Meridian Scanner Terminal -> solid base (22, 15)

    # First Meridian Heat-Tower & Steaming Hole tucked inside East Forecourt (canonical Ch11:172!)
    m.stamp('lm_pylon', 31, 12, mark='B')
    m.over.append((2, 31, 11, P1('lm_steam0')))
    m.over.append((2, 32, 11, P1('lm_steam1')))
    # East Ice-Climbers' Supply Camp & Sled Park
    for nm, x, y in (
        ('pf_beacon', 12, 7), ('pf_beacon', 22, 7),
        ('pf_beacon', 11, 17), ('pf_beacon', 23, 17),
        ('fw_stall_i', 25, 8),
        ('fw_brazier', 11, 11), ('fw_brazier', 24, 11),
        ('fw_sled', 6, 15), ('pf_sledge', 27, 15),
        ('fw_wood', 10, 17), ('fw_rack', 29, 14),
        ('sh_crates', 26, 16), ('hb_barrels', 5, 17),
        ('fw_skull', 11, 15), ('fw_skull', 29, 9),
        ('pf_logbench', 9, 14), ('pf_stonebench', 27, 13),
        ('pf_lantern', 13, 11), ('pf_lantern', 21, 11),
        ('pf_lantern', 10, 14), ('pf_lantern', 25, 13),
    ):
        s = STAMPS[nm]
        if m.inb(x, y) and m.free(x, y, s['w'], s['h'], on='.dI') and not ev_mask[y:y + s['h'], x:x + s['w']].any():
            m.stamp(nm, x, y, mark='B')

    for tx, ty, sp in (
        (4, 13, KF_TEAL_PINE_A), (34, 11, KF_SPRUCE_B), (4, 16, KF_SPRUCE_A), (33, 16, KF_TEAL_PINE_B),
        (10, 18, KF_SHRUB_A), (34, 15, KF_SHRUB_B),
    ):
        _put_sprite(m, tx, ty, *sp, on='.T', avoid_mask=ev_mask)

    R_ = types.SimpleNamespace(m=m, seed=303, road_mask=np.isin(m.cls, ['d']), events=E, rng=rng)
    CK.thin_bands(R_, passes=1)
    CK.woods(R_, ALPINE_WOODS, scale=7.5, accents={'snowblue': 0.08})

    m.events = E
    m.paint()
    _infill_winter(R_, ALPINE_WOODS, scale=7.5, seed=303)

    # Flush Continuous Fortified Cut-Stone Masonry North Curtain Wall & Parapets (matching 303 south & 305 north!)
    for seg_x0, seg_x1 in ((7, 11), (24, 32)):
        for x in range(seg_x0, seg_x1 + 1):
            is_w, is_e = (x == seg_x0), (x == seg_x1)
            for yy in (4, 5, 6):
                m.L[0, yy, x] = SNOW_BASE
                m.L[2, yy, x] = 0
            m.L[1, 4, x] = P1('rw_rail_w' if is_w else ('rw_rail_e' if is_e else 'rw_rail_m'))
            m.L[1, 5, x] = P1('rw_f1w0' if is_w else ('rw_f1e0' if is_e else ('rw_f1m1' if (x + seg_x0) % 3 == 0 else 'rw_f1m0')))
            m.L[1, 6, x] = P1('rw_f2w0' if is_w else ('rw_f2e0' if is_e else 'rw_f2m0'))

    # Stamp INTACT full-height 1x2 Isenmar Royal Banners onto the North Curtain Wall face (y=5..6)!
    ban_L = STAMPS['fw_ban_i']['layers']
    for bx, by in ((8, 5), (10, 5), (26, 5), (29, 5), (31, 5)):
        m.L[2, by, bx] = int(ban_L[2][0][0] or ban_L[1][0][0])
        m.L[2, by + 1, bx] = int(ban_L[1][1][0] or ban_L[2][1][0])

    # Build Continuous Fortified South Stone/Ice Curtain Wall & Parapets flanking gt_gate4 (x=4..12 & x=23..35)!
    for seg_x0, seg_x1 in ((4, 12), (23, 35)):
        for x in range(seg_x0, seg_x1 + 1):
            is_w, is_e = (x == seg_x0), (x == seg_x1)
            m.L[1, 20, x] = P1('rw_rail_w' if is_w else ('rw_rail_e' if is_e else 'rw_rail_m'))
            m.L[1, 21, x] = P1('rw_f1w0' if is_w else ('rw_f1e0' if is_e else ('rw_f1m1' if (x + seg_x0) % 3 == 0 else 'rw_f1m0')))
            m.L[1, 22, x] = P1('rw_f2w0' if is_w else ('rw_f2e0' if is_e else 'rw_f2m0'))
            m.L[2, 20, x] = 0
            m.L[2, 21, x] = 0
            m.L[2, 22, x] = 0
            if m.L[1, 23, x] == 0:
                m.L[1, 23, x] = KF_BOULDER[1][0][x % 2]

    # Steaming fishing hole beside Tower One (31, 17)
    m.L[1, 17, 31] = P1('fw_hole_t')

    # Seal rear of North gt_gate6 (y=5, x=15..20) & bottom shadow of South gt_gate4 (y=23, x=16..19) cleanly!
    for gx in range(15, 21):
        m.L[1, 5, gx] = P1('rw_f1m0')
        m.L[2, 6, gx] = 0
        m.L[2, 7, gx] = 0
    for gx in range(16, 20):
        m.L[2, 23, gx] = 505   # Clean invisible pas=0xf blocker on bottom shadow row (exact 284 Barbican!)
        m.L[2, 22, gx] = 0

    _dress_snow_details(m, ev_mask, seed=3033, drift_p=0.20, track_p=0.22, crack_p=0.26, reeds_p=0.0)
    _seal_unconnected_edges(m, open_cells=())

    Lr = RC.resolve(m.L, TID_SNOW).astype(np.int32)
    ev_pts = [tuple(e['at']) for e in E]
    PG.guard(Lr, TID_SNOW, ev_pts, 'Map 303')
    assert not PG.hits(Lr, R.tilesets()[TID_SNOW], ev_pts), 'Map 303 passguard hits!'
    _verify_map(Lr, TID_SNOW, E, (17, 8), 'Map 303 Rimeholt - Icewall Gate', outdoor=True)

    np.save(os.path.join(RAW_DIR, '303.npy'), Lr.astype(np.int16))
    spec = {
        'id': 303,
        'name': 'Rimeholt - Icewall Gate',
        'parent': 300,
        'bgm': 'Lerucean Town',
        'field': 'SNOWY_MOUNTAIN',
        'rubric': True,
        'yards_ok': True,
        'map_audio': {'bgm': 'Town - Isenmar', 'bgs': 'Wind - Isenmar', 'bgs_volume': 60},
        'tone': [-10, -4, 14, 12],
        'fog': {'name': 'prismfall_seamist', 'opacity': 24, 'blend': 0, 'zoom': 100, 'sx': 1, 'sy': 0},
        'metadata': {
            'Name': 'Rimeholt - Icewall Gate',
            'Outdoor': True,
            'ShowArea': True,
            'Bicycle': True,
            'MapPosition': RIME_POS,
            'BattleBack': 'snow',
            'Weather': ['Snow', 25],
        },
        'biome': 'city',
        'tileset': TID_SNOW,
        'raw': 'data/raw/303.npy',
        'events': E,
    }
    with open(os.path.join(SPEC_DIR, '303_rimeholt_icewall_gate.yaml'), 'w', encoding='utf-8') as f:
        f.write('# GENERATED by mapgen/layouts/rimeholt_town.py (Batch 3H): Rimeholt - Icewall Gate.\n')
        f.write(yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))
    print('Wrote specs/303_rimeholt_icewall_gate.yaml and data/raw/303.npy')
    return Lr


# =================================================================================================
# 5. MAP 304 — RIMEHOLT - SLED MARKET (46x36, TS 52, Outdoor, :FROZEN_LAKE, rubric: true)
# =================================================================================================
def build_304():
    W, H = 46, 36
    m = _snowmap(W, H, 304, kit='shs3')
    rng = random.Random(30411)

    # ---- 1. Bustling Nordic Winter Dog-Sled & Timber Trade Bazaar ----
    # Raised North Guildhall Terrace (ht=1, y=0..12) overlooking the Ice-Bazaar Floor (y=13..35)!
    for y in range(0, 13):
        for x in range(0, W):
            m.ht[y, x] = 1

    # Perimeter snow-spruce woodland borders on all 4 flanks
    for y in range(H):
        for x in range(W):
            if y <= 2 or y >= H - 4 or x <= 3 or x >= W - 4:
                m.cls[y, x] = 'T'

    # Open North Guildhall Terrace plateau & NW Keep Ramp (x=10..14, y=0..12!)
    m.rect(5, 3, 36, 10, '.', only='.T')
    m.rect(10, 0, 5, 13, 'd')
    # Twin grand stairs connecting Guildhall Terrace -> Bazaar Square
    m.stairs(11, 12, w=3, n=3, c='d')
    m.stairs(29, 12, w=3, n=3, c='d')

    # Central Sled-Market Ice Plaza & Organic Trade Lanes (naturally asymmetric, ZERO mirror grid!)
    m.rect(5, 15, 36, 17, '.', only='.T')
    # Frozen market ice floor skewed slightly east around the Bazaar Hearth & Stalls
    m.rect(11, 17, 26, 13, 'I', only='.T')
    # Gently winding E-W Grand Sled Avenue (West -> 300 y=16..20; gently curves to East -> 720 y=18..22!)
    m.lane([(0, 18), (10, 18), (22, 19), (34, 20), (45, 20)], c='d', w=2.6, seed=3041, wobble=0.35)
    # Asymmetric Bazaar Loops & South Wharf Spur -> guarded 309 Sinking Quarter (x=18..21, y=28..35!)
    m.rect(11, 15, 4, 15, 'd')
    m.rect(31, 15, 4, 15, 'd')
    m.rect(11, 27, 24, 3, 'd')
    m.rect(18, 28, 4, 8, 'd')
    # Upper terrace promenade linking Guildhall, Timber Exchange & Keep Ramp
    m.rect(10, 10, 29, 2, 'd', only='.T')

    # Asymmetric Southern Margin: Frozen Lake Rime Bay on SW (x=4..16, y=31..35) vs Spruce-Sheltered War-Sled Paddock on SE!
    for y in range(31, H):
        for x in range(4, 17):
            m.cls[y, x] = 'o'
    for y in range(33, H):
        for x in range(24, 39):
            m.cls[y, x] = 'T'

    # Clear exact building footprints before plan_cliffs
    for x0, y0, x1, y1 in (
        (16, 4, 27, 9),    # wb_inn Sledwright's Guildhall (12x6)
        (30, 4, 40, 9),    # wb_long3 Timber Exchange (11x6)
        (5, 23, 11, 28),   # wb_smoke Fish Smokehouse (7x6)
        (36, 24, 40, 28),  # wb_hut Furrier's Lean-to (5x5)
    ):
        for yy in range(y0, y1 + 1):
            for xx in range(x0, x1 + 1):
                if m.inb(xx, yy):
                    m.cls[yy, xx] = '.'

    # Re-assert crisp exact edge seams
    m.cls[16:21, 0:4] = 'd'          # West  -> 300 Thane's Harbour
    m.cls[18:23, 42:46] = 'd'        # East  -> guarded 720 The Thane's Sled-Road
    m.cls[0:4, 10:15] = 'd'          # NW    -> 305 Whalebone Keep Bailey
    m.cls[32:36, 18:22] = 'd'        # South -> guarded 309 Sinking Quarter

    m.plan_cliffs(rows=3)

    # ---- 2. Nordic Trade Halls & Guildhouses ----
    m.stamp('wb_inn', 16, 4)         # Sledwright's Guildhall
    m.stamp('wb_long3', 30, 4)       # Timber & Whalebone Exchange
    m.stamp('wb_smoke', 5, 23)       # Smoked-Fish Hall
    m.stamp('wb_hut', 36, 24)        # Hoarwood Furrier's Lean-to

    for dx, dy in ((22, 9), (37, 9), (8, 28), (38, 28)):
        _doorstep(m, (dx, dy), depth=2)

    # ---- 3. Events: Warps to 300/305, Guarded 720/309, Canonical Sled Market NPCs & Pickups ----
    E = []
    # West Approach -> 300 Thane's Harbour (44, 22, left)
    for wy in range(16, 21):
        E.append({'type': 'warp', 'name': f'West to Thanes Harbour {wy}', 'at': [0, wy],
                  'to': {'map': 300, 'x': 44, 'y': 22, 'dir': 'left'}, 'se': 'Door enter'})
    # NW Keep Causeway -> 305 Whalebone Keep - Bailey (34, 22, left)
    for nx in range(10, 15):
        E.append({'type': 'warp', 'name': f'NW to Whalebone Keep {nx}', 'at': [nx, 0],
                  'to': {'map': 305, 'x': 34, 'y': 22, 'dir': 'left'}, 'se': 'Door enter'})

    # East Gate -> PBMoveRoute::BACKWARD-guarded 720 The Thane's Sled-Road!
    sled_msg = (
        "Sled-Road Outrider: Hold the line, friend — the Thane's war-sleds have priority east along the Thane's Sled-Road "
        "toward the Mast Glacier right now. Wait for the convoy horn before heading out on the sea ice."
    )
    for ey in range(18, 23):
        E.append({'type': 'event', 'name': f'East to Thanes Sled-Road {ey}', 'at': [45, ey],
                  'pages': [{'trigger': 'touch', 'through': True,
                             'commands': _guarded_unbuilt_transfer(720, 2, 36, 'right', sled_msg)}]})

    # South Wharf -> PBMoveRoute::BACKWARD-guarded 309 Rimeholt - Sinking Quarter!
    sq_msg = (
        "Bazaar Warden: Careful down the south steps — the lower slips toward the Sinking Quarter are slick with meltwater "
        "from the harbour towers. Stay up on the Sled Market ice for now."
    )
    for sx in range(18, 22):
        E.append({'type': 'event', 'name': f'South to Sinking Quarter {sx}', 'at': [sx, 35],
                  'pages': [{'trigger': 'touch', 'through': True,
                             'commands': _guarded_unbuilt_transfer(309, 20, 2, 'down', sq_msg)}]})

    # Canonical Ch11 Sled Market NPCs (story/30_SCRIPT_CH11.md:214 & war state!)
    wright_ruby = (
        'if $game_variables[122] >= 2\n'
        '  pbMessage(_INTL("Sled-Wright: Half my stalls are shuttered under wartime rationing — every ash-wood runner we cut goes straight east to Skaldfast."))\n'
        'else\n'
        '  pbMessage(_INTL("Sled-Wright: The Thane\'s buying every war-sled in the city. \'Just in case.\'"))\n'
        '  pbMessage(_INTL("Sled-Wright: Just in case what, I said. He looked east toward the glacier and said \'just in case.\'"))\n'
        'end'
    )
    E.append({'type': 'event', 'name': 'Sled-Wright', 'at': [20, 11],
              'pages': [{'graphic': {'sprite': 'NPC 20', 'dir': 'down'}, 'trigger': 'action', 'move': 'fixed',
                         'commands': [{'script': wright_ruby}]}]})

    E.append(_make_npc('Hoarwood Furrier', (36, 29), 'NPC 18', 'left', [
        "Hoarwood Furrier: Birchwood's dear this winter, and nobody in Rimeholt's buying it because everyone's got Meridian's towers.",
        "Hoarwood Furrier: Mark my words, southerner — a fur coat never fails when a wire snaps.",
    ]))

    E.append(_make_npc('Ice-Fishmonger', (16, 25), 'NPC 11', 'down', [
        "Fishmonger: Smoked lake char and salted cod! Fresh off the morning sleds — though nobody's cutting holes near Tower Three any more.",
    ]))

    E.append(_make_npc('Isenmar Quartermaster', (40, 20), 'trainer_ISENMAR_OFFICER', 'left', [
        "Quartermaster: East lies the Thane's Sled-Road — a highway of packed sea-ice kept open all the way to the Mast Glacier and Anchorhold.",
        "Quartermaster: Keep clear of the supply sleds when the war-horns blow.",
    ]))

    E.append(_make_npc('Bazaar Skald', (24, 25), 'NPC 22', 'up', [
        'Bazaar Skald: "Sleep, old whale, under the white / Sleep while the Thane keeps the lamps alight..."',
        "Bazaar Skald: Folk used to sing that once a winter at the Long Night. Now you hear it every evening round the market fire.",
    ]))

    E.append(_make_npc('Sled-Team Handler', (27, 21), 'NPC 17', 'left', [
        "Sled-Team Handler: Good harness dogs and Mamoswine teams keep Rimeholt fed when the southern passes drift shut.",
    ]))

    # Solid Market Signposts (0 over_trigger?!)
    E.append(_sign('Sled Market Sign', (6, 15),
                   "RIMEHOLT — SLED MARKET\n← Thane's Harbour · ↖ Whalebone Keep · → The Thane's Sled-Road"))
    E.append(_sign('Sled-Road Sign', (42, 17),
                   "EAST GATE — THE THANE'S SLED-ROAD\nEast to the Mast Glacier & Anchorhold. Sled convoys have priority."))

    # Pickups (explicit hidden=False on every visible item!)
    E.append({'type': 'item', 'name': 'Item (Ultra Ball)', 'at': [39, 11], 'item': 'ULTRABALL', 'hidden': False})
    E.append({'type': 'item', 'name': 'Item (Snowball)', 'at': [7, 30], 'item': 'SNOWBALL', 'hidden': False})
    E.append({'type': 'item', 'name': 'HiddenItem (Star Piece)', 'at': [28, 29], 'item': 'STARPIECE', 'hidden': True})

    ev_mask = _reserve_mask(m, E, extra=[
        (1, 18), (44, 20), (12, 1), (20, 34), (6, 14), (42, 16),
        (11, 12), (12, 12), (13, 12), (29, 12), (30, 12), (31, 12),
        (11, 15), (12, 15), (13, 15), (29, 15), (30, 15), (31, 15),
    ], pad=1)

    # ---- 4. Bustling Winter Bazaar Props: Stalls, Campfire, Dog-Sleds, Crates, Braziers & Banners ----
    m.stamp('pf_signpost', 6, 14)    # solid base (6, 15)
    m.stamp('pf_signpost', 42, 16)   # solid base (42, 17)

    for nm, x, y in (
        # Central roaring bazaar hearth campfire!
        ('sh_campfire', 21, 22),
        # Snow-dusted market stalls lining the bazaar square!
        ('fw_stall_i', 15, 16), ('fw_stall_i', 19, 16), ('fw_stall_e', 24, 16), ('fw_stall_i', 28, 16),
        ('hb_fishstall', 15, 21),
        ('fw_stall_i', 35, 20), ('fw_stall_e', 6, 19),
        # Sleds, war-sled barricades, supply wagons, crates & fish racks!
        ('wr_sledfort', 36, 15), ('wr_sledfort2', 36, 22),
        ('wr_supply', 31, 29), ('fw_sled', 16, 28), ('pf_sledge', 25, 29), ('fw_sled', 7, 11),
        ('sh_crates', 13, 24), ('sh_crates', 30, 25), ('hb_barrels', 33, 22), ('hb_barrels', 12, 21),
        ('fw_rack', 10, 29), ('fw_rack', 33, 29), ('fw_wood', 13, 8), ('fw_wood', 28, 8), ('fw_wood', 14, 29),
        # Warm glowing hearth braziers & royal blue Isenmar banners!
        ('fw_brazier', 9, 2), ('fw_brazier', 15, 2),
        ('fw_brazier', 14, 20), ('fw_brazier', 29, 20),
        ('fw_brazier', 17, 30), ('fw_brazier', 22, 27),
        ('fw_brazier', 42, 23), ('fw_brazier', 4, 21),
        ('wr_ban_ise', 8, 1), ('wr_ban_ise', 15, 1),
        ('wr_ban_ise', 43, 15), ('wr_ban_ise', 43, 23),
        ('fw_ban_i', 15, 8), ('fw_ban_i', 29, 8),
        ('pf_logbench', 20, 25), ('pf_logbench', 25, 25),
        ('pf_lantern', 9, 15), ('pf_lantern', 15, 15), ('pf_lantern', 28, 15), ('pf_lantern', 34, 15),
        ('pf_lantern', 17, 32), ('pf_lantern', 34, 27), ('pf_lantern', 12, 27),
    ):
        s = STAMPS[nm]
        if m.inb(x, y) and m.free(x, y, s['w'], s['h'], on='.dI') and not ev_mask[y:y + s['h'], x:x + s['w']].any():
            m.stamp(nm, x, y, mark='B')

    # Decorative snowy evergreen clusters framing guildhall & bazaar corners
    for tx, ty, sp in (
        (5, 4, KF_SPRUCE_A), (7, 7, KF_TEAL_PINE_A), (41, 4, KF_TEAL_PINE_B), (41, 8, KF_SPRUCE_B),
        (4, 12, KF_TEAL_PINE_A), (41, 25, KF_TEAL_PINE_B), (40, 29, KF_SHRUB_B),
    ):
        _put_sprite(m, tx, ty, *sp, on='.T', avoid_mask=ev_mask)

    R_ = types.SimpleNamespace(m=m, seed=304, road_mask=np.isin(m.cls, ['d']), events=E, rng=rng)
    CK.thin_bands(R_, passes=1)
    CK.woods(R_, ALPINE_WOODS, scale=8.0, accents={'snowblue': 0.08})

    m.events = E
    m.paint()
    _infill_winter(R_, ALPINE_WOODS, scale=8.0, seed=304)

    # Safe tag==0 3x3 bordered pale glacier-blue mosaic paving across central Sled Market Bazaar Square (x=15..30, y=17..26)!
    for y in range(H):
        for x in range(W):
            if m.cls[y, x] != 'I':
                continue
            if 15 <= x <= 30 and 17 <= y <= 26:
                ry = 0 if y == 17 else (2 if y == 26 else 1)
                rx = 0 if x == 15 else (2 if x == 30 else 1)
                m.L[0, y, x] = GLACIER_9[ry][rx]
            else:
                m.L[0, y, x] = SNOW_BASE

    # Matching weathered Nordic timber causeway deck cue at NW Keep Bridge exit (10..14, 0..2 -> 305 East Causeway)!
    _paint_wharf(m, 10, 0, 14, 2)

    _dress_snow_details(m, ev_mask, seed=3044, drift_p=0.18, track_p=0.22, crack_p=0.26, reeds_p=0.0, keep_ice_l0=True)

    open_304 = ([(0, y) for y in range(16, 21)] + [(W - 1, y) for y in range(18, 23)] +
                [(x, 0) for x in range(10, 15)] + [(x, H - 1) for x in range(18, 22)])
    _seal_unconnected_edges(m, open_cells=open_304)

    Lr = RC.resolve(m.L, TID_SNOW).astype(np.int32)
    ev_pts = [tuple(e['at']) for e in E]
    PG.guard(Lr, TID_SNOW, ev_pts, 'Map 304')
    assert not PG.hits(Lr, R.tilesets()[TID_SNOW], ev_pts), 'Map 304 passguard hits!'
    _verify_map(Lr, TID_SNOW, E, (2, 18), 'Map 304 Rimeholt - Sled Market', outdoor=True)

    np.save(os.path.join(RAW_DIR, '304.npy'), Lr.astype(np.int16))
    spec = {
        'id': 304,
        'name': 'Rimeholt - Sled Market',
        'parent': 300,
        'bgm': 'Lerucean Town',
        'field': 'SNOWY_MOUNTAIN',
        'rubric': True,
        'yards_ok': True,
        'map_audio': {'bgm': 'Town - Isenmar', 'bgs': 'Wind - Isenmar', 'bgs_volume': 50},
        'tone': [-8, -2, 10, 10],
        'fog': {'name': 'prismfall_seamist', 'opacity': 20, 'blend': 0, 'zoom': 100, 'sx': 1, 'sy': 0},
        'metadata': {
            'Name': 'Rimeholt - Sled Market',
            'Outdoor': True,
            'ShowArea': True,
            'Bicycle': True,
            'MapPosition': RIME_POS,
            'BattleBack': 'snow',
            'Weather': ['Snow', 20],
        },
        'biome': 'city',
        'tileset': TID_SNOW,
        'raw': 'data/raw/304.npy',
        'events': E,
    }
    with open(os.path.join(SPEC_DIR, '304_rimeholt_sled_market.yaml'), 'w', encoding='utf-8') as f:
        f.write('# GENERATED by mapgen/layouts/rimeholt_town.py (Batch 3H): Rimeholt - Sled Market.\n')
        f.write(yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))
    print('Wrote specs/304_rimeholt_sled_market.yaml and data/raw/304.npy')
    return Lr


def main():
    build_300()
    build_301()
    build_302()
    build_303()
    build_304()


if __name__ == '__main__':
    main()
