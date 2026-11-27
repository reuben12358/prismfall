#!/usr/bin/env python3
"""layouts/act1_frontier_dungeons.py - Batch 1B Brand-New Canonical Act 1 Dungeons, Bleed Zone & Interior (5 maps).

ZERO edits to any existing built map or shared file! Builds:
  - 565 Gullcry Caves B1F           (32x30, TS 57 PF Rejuv Cave, field CAVE)
  - 584 Voltaic Sluiceworks         (40x32, TS 60 PF Rejuv Lumen, field SCRAPYARD)
  - 585 Sluiceworks Turbine Hall    (30x24, TS 60 PF Rejuv Lumen, field SCRAPYARD)
  - 588 Ebb Hollow                  (34x30, TS 60 PF Rejuv Lumen, field BLEED, rubric: true)
  - 591 Brassfall Pokémon Center    (15x11, TS 34 Prismfall Interior, template pokecenter)

Usage:
    PRISMFALL_GFX=/home/antigravity/pf_engine_run/game/Graphics \\
      /usr/bin/python3 -I mapgen/layouts/act1_frontier_dungeons.py
"""
import os
import sys
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
from cavekit import Cave, FLOOR, TER, PIT, MASS
import craftkit as CK
import rcompose as RC
import render as R
import passguard as PG
from terrain import vnoise, NB2AUTO, autotile_shape
from interiorkit import TF
import build as B

RAW_DIR = os.path.join(HERE, 'data', 'raw')
SPEC_DIR = os.path.join(HERE, 'specs')

TID34 = 34
TID57 = 57
TID60 = 60
VOID34 = 5437

# Safe Brassfall PC door landing on Map 590 (verified in act1_frontier_routes.py!)
BRASSFALL_PC_DOOR = (11, 21)
BRASSFALL_HEAL_SPOT = [590, 11, 22]


# ==============================================================================
# SHARED HELPERS: NB2AUTO, 4-BIT BFS VERIFIER, RUBRIC & WRITERS
# ==============================================================================
def fix_autotiles_single_layer(Lr):
    """Enforce exact single-layer 8-neighbor NB2AUTO across every layer z in (0, 1, 2)."""
    Z, H, W = Lr.shape
    for z in range(Z):
        layer = Lr[z]
        auto_mask = (layer >= 48) & (layer < 384)
        if not auto_mask.any():
            continue
        slots = np.unique(layer[auto_mask] // 48)
        for slot in slots:
            m = (layer >= slot * 48) & (layer < (slot + 1) * 48)
            pad = np.pad(m, 1, constant_values=True)
            for y, x in np.argwhere(m):
                b = 0
                for dx, dy, bit in ((0, -1, 1), (1, -1, 2), (1, 0, 4), (1, 1, 8),
                                    (0, 1, 16), (-1, 1, 32), (-1, 0, 64), (-1, -1, 128)):
                    if pad[y + 1 + dy, x + 1 + dx]:
                        b |= bit
                Lr[z, y, x] = int(slot * 48 + NB2AUTO[b])


def verify_4bit_bfs(Lr, tid, events, start, targets, label, extra_solid=(), ignore_gate_events=()):
    """Strict 4-bit directional BFS (matching Essentials playerPassable? + directional passage bits)."""
    ts = R.tilesets()[tid]
    H, W = Lr.shape[1:]
    solid_ev = set(extra_solid)
    ign = set(ignore_gate_events)
    for e in events:
        et = e.get('type')
        at = tuple(e['at']) if e.get('at') else None
        if at in ign:
            continue
        if et in ('npc', 'trainer', 'mart'):
            solid_ev.add(at)
        elif et == 'event':
            pg0 = (e.get('pages') or [{}])[0]
            g = pg0.get('graphic') or {}
            if (g.get('sprite') or g.get('tile')) and not pg0.get('through'):
                solid_ev.add(at)
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
    assert ok[sy, sx] and (sx, sy) not in solid_ev, f'{label}: start {start} is blocked!'
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

    missing = []
    for name, (tx, ty), allow_adj in targets:
        if allow_adj:
            reach = ((tx, ty) in seen
                     or any((tx + dx, ty + dy) in seen for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))))
        else:
            reach = (tx, ty) in seen
        if not reach:
            missing.append((name, (tx, ty), bool(ok[ty, tx])))
    assert not missing, f'{label}: UNREACHABLE targets: {missing}'
    # Also verify 0 NB2AUTO mismatches & 0 void L0 & 0 oob!
    assert (Lr[0] > 0).all(), f'{label}: void L0 tiles found!'
    assert (Lr >= 0).all(), f'{label}: negative tile IDs found!'
    for z in range(3):
        for slot in range(1, 8):
            base = slot * 48
            msk = (Lr[z] >= base) & (Lr[z] < base + 48)
            if not msk.any():
                continue
            for yy, xx in np.argwhere(msk):
                assert int(Lr[z, yy, xx]) == base + autotile_shape(msk, xx, yy), \
                    f'{label}: NB2AUTO mismatch at L{z} ({xx},{yy})'
    print(f'  [BFS-OK] {label}: {len(seen)} walkable cells reached from {start}; 0 NB2AUTO; 0 void_L0.')
    return seen


def write_raw_map(m, mid, tid, head, comment, start, extra_targets=(), ignore_gate_events=()):
    """Resolve virtual IDs -> tid, fix NB2AUTO, passguard, verify 4-bit BFS & rubric, write .npy + .yaml."""
    Lr = RC.resolve(m.L, tid).astype(np.int32)
    fix_autotiles_single_layer(Lr)
    ev_pts = [tuple(e['at']) for e in m.events if e and e.get('at')]
    PG.guard(Lr, tid, ev_pts, f'map {mid}')
    hits = PG.hits(Lr, R.tilesets()[tid], ev_pts)
    assert not hits, f'map {mid}: residual passguard hits: {hits[:5]}'

    targets = list(extra_targets)
    for e in m.events:
        et = e.get('type')
        at = tuple(e['at'])
        if et in ('warp', 'door', 'exit'):
            targets.append((e.get('name', et), at, False))
        elif et in ('npc', 'trainer', 'item', 'sign', 'mart', 'pc'):
            targets.append((e.get('name', et), at, True))
        elif et == 'event':
            pgs = e.get('pages') or []
            if any(p.get('trigger', 'action') in ('action', 'touch') and p.get('commands') for p in pgs):
                allow_adj = not all(p.get('trigger') == 'touch' for p in pgs if p.get('commands'))
                targets.append((e.get('name', 'event'), at, allow_adj))

    verify_4bit_bfs(Lr, tid, m.events, start, targets, f'Map {mid} {head["name"]}', ignore_gate_events=ignore_gate_events)

    if head.get('rubric'):
        r = B.rubric(Lr)
        need = [('layer2', 55, 1), ('layer3', 20, 1), ('bare', 35, -1), ('bare3x3', 13, -1), ('stacks', 10, 1), ('mirror', 15, -1)]
        fails = [f'{k}={r[k]:.1f} (need {"≥" if s > 0 else "≤"}{lim})' for k, lim, s in need if (r[k] - lim) * s < 0]
        print(f'  [RUBRIC] Map {mid}: ' + '  '.join(f'{k}={r[k]:.1f}' for k, _, _ in need))
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
    print(f'Wrote {mid} {head["name"]:32s} {m.W}x{m.H} ts={tid} events={len(m.events)}')
    return Lr


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


def _put_if(m, name, x, y, on='.'):
    st = STAMPS[name]
    w, h = st['w'], st['h']
    if m.free(x, y, w, h, on=on) and not any((xx, yy) in m.keep_clear
                                              for xx in range(x, x + w) for yy in range(y, y + h)):
        if isinstance(m, Cave):
            m.put(name, x, y)
        else:
            m.stamp(name, x, y)
        return True
    return False


def _place_over_stamp(m, name, x, y, mark_base=True):
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
                    if mark_base and z == 1:
                        m.taken[yy, xx] = True


def _hang(m, name, x, y):
    L = STAMPS[name]['layers']
    for dy in range(len(L[0])):
        for dx in range(len(L[0][0])):
            t = next((L[z][dy][dx] for z in (2, 1, 0) if L[z][dy][dx]), 0)
            if t and m.inb(x + dx, y + dy) and m.cliff[y + dy, x + dx]:
                m.over.append((2, x + dx, y + dy, t))


def _on_faces(m, name, cells):
    for x, y in cells:
        if m.inb(x, y) and m.cliff[y, x]:
            m.over.append((2, x, y, P1(name)))


def _abyss_piece(m, name, x, y):
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


# ==============================================================================
# MAP 1: 565 Gullcry Caves B1F (32x30, TS 57 PF Rejuv Cave, field CAVE)
# ==============================================================================
def build_565():
    m = Cave(32, 30, 'L', seed=565, pool='Sea Cave')
    B_ = m.box

    # ---- 1. North Arrival Terrace (TER) with open north shaft tunnel [15..17, 0..5] -> warp [16,1] ----
    m.room(16.0, 4.0, 5.6, 2.2, h=TER, c='.', rough=0.22, seed=11)
    B_(11, 1, 21, 5, TER, '.')
    B_(15, 0, 17, 5, TER, '.')
    # NW Waterfall spring niche on TER (x=6..7, y=6..7) cascading down cliff (y=8..11) into lagoon!
    B_(6, 6, 7, 7, TER, 'w')
    B_(6, 8, 7, 12, FLOOR, 'w')

    # ---- 2. Organic Subterranean Sea-Cave Lagoon (x=5..26, y=11..22) ----
    for y in range(11, 23):
        for x in range(5, 27):
            q = ((x - 16.0) / 10.6) ** 2 + ((y - 16.8) / 5.8) ** 2
            q += 0.22 * (vnoise(x, y, 5657, 3.2) - 0.5)
            if q <= 1.0:
                m.cls[y, x] = 'w'
                m.ht[y, x] = FLOOR
    B_(6, 12, 25, 21, FLOOR, 'w')

    # ---- 3. Upper Landing, West & East Sea-Galleries, South Causeway & Central Reef Islet ----
    m.room(16.0, 9.5, 5.4, 2.2, h=FLOOR, c='.', rough=0.22, seed=19)
    B_(11, 6, 21, 11, FLOOR, '.')
    # West sea-gallery (x=2..5, y=10..27) -> SW Brine Cove (TM55 at [3,26])
    m.room(3.8, 17.5, 2.4, 7.2, h=FLOOR, c='.', rough=0.24, seed=23)
    B_(2, 11, 5, 27, FLOOR, '.')
    # East sea-gallery (x=26..29, y=9..27) -> SE Shell Grotto (SHELLBELL at [28,26])
    m.room(27.6, 18.0, 2.4, 7.2, h=FLOOR, c='.', rough=0.24, seed=29)
    B_(26, 9, 29, 27, FLOOR, '.')
    B_(21, 8, 28, 11, FLOOR, '.')  # NE gallery link from north landing
    # South tidal causeway & coastal alcoves (y=24..27) connecting West Cove & East Grotto!
    m.room(16.0, 25.5, 11.5, 2.2, h=FLOOR, c='.', rough=0.26, seed=31)
    B_(2, 24, 29, 27, FLOOR, '.')
    B_(14, 22, 18, 23, FLOOR, 'w')

    # Central walkable sea-stack islet (x=14..18, y=15..18) linked by timber jetties to East & West shores!
    B_(14, 15, 18, 18, FLOOR, '.')

    # ---- 4. Sculpted Coastal Headlands & Solid Slate Rock Sea-Stacks (ZERO mid-water stickers!) ----
    m.mass_at(
        [(2, 2), (3, 2), (4, 2), (2, 3), (3, 3), (28, 2), (29, 2), (28, 3), (29, 3)] +
        [(9, 13), (10, 13), (11, 13), (9, 14), (10, 14)] +
        [(21, 13), (22, 13), (23, 13), (22, 14), (23, 14)] +
        [(8, 19), (9, 19), (10, 19), (8, 20), (9, 20)] +
        [(21, 19), (22, 19), (23, 19), (22, 20), (23, 20)] +
        [(1, 14), (1, 15), (30, 15), (30, 16), (11, 27), (12, 27), (20, 27), (21, 27)]
    )

    m.tidy()
    for x in (6, 7):
        for y in (6, 7):
            m.cls[y, x] = 'w'
            m.ht[y, x] = TER
        for y in range(8, 13):
            m.cls[y, x] = 'w'
            m.ht[y, x] = FLOOR
    for x0, y0, x1, y1, h in (
        (11, 1, 21, 5, TER), (15, 0, 17, 5, TER),
        (11, 6, 21, 11, FLOOR), (21, 8, 28, 11, FLOOR),
        (2, 11, 5, 27, FLOOR), (26, 9, 29, 27, FLOOR),
        (3, 24, 28, 27, FLOOR), (14, 15, 18, 18, FLOOR),
    ):
        for yy in range(y0, y1 + 1):
            for xx in range(x0, x1 + 1):
                if m.cls[yy, xx] != 'w':
                    m.cls[yy, xx] = '.'
                    m.ht[yy, xx] = h

    for y in (16, 17):
        for x in range(6, 14):
            m.cls[y, x] = 'w'
            m.ht[y, x] = FLOOR
        for x in range(19, 26):
            m.cls[y, x] = 'w'
            m.ht[y, x] = FLOOR

    # Wide central stairs TER (y<=5) -> FLOOR (y>=6): spans y=5,6,7!
    m.stairs(15, 5, w=3, n=3, c='.')
    m.patch_args = (0.58, 4.4)
    m.plan_cliffs(rows=3)

    # ---- 5. Events ----
    E = m.events
    E += [
        {'type': 'warp', 'name': 'Ladder up to 1F', 'at': [16, 1],
         'to': {'map': 564, 'x': 29, 'y': 6, 'dir': 'down'}, 'se': 'Door exit'},
        _npc((12, 4), 'Cavern Diver', 'NPC 20', [
            "Cavern Diver: The ebb pulls right down into this basin. Half of Gullcry's tide-pools drain through these rocks.",
            "Cavern Diver: Keep to the old jetty boards across the middle if you're hunting for salvage. The shell chimes carry all the way up the shaft."
        ], d='right'),
        _sign((19, 10), 'Smuggler Tide-Post',
              "A salt-bleached timber post lashed with kelp rope. Carved deep into the grain: 'WEST COVE: BRINE CACHE — EAST GROTTO: SHELL BELL — WATCH THE SURGE.'"),
        _item((3, 26), 'TM55', 'TM55 Brine'),
        _item((28, 26), 'SHELLBELL', 'Shell Bell'),
        _item((16, 16), 'DIVEBALL', 'Dive Ball'),
        _item((24, 26), 'PEARL', 'Hidden Pearl', hidden=True),
        _item((4, 15), 'HEARTSCALE', 'Heart Scale'),
    ]

    m.keep_clear |= {
        (16, 0), (16, 1), (16, 2), (16, 3), (15, 2), (17, 2),
        (12, 4), (13, 4), (19, 10), (19, 11), (18, 10),
        (3, 26), (3, 25), (4, 26), (28, 26), (28, 25), (27, 26),
        (16, 16), (15, 16), (17, 16), (16, 17), (24, 26), (4, 15),
    }
    for y in range(4, 11):
        for x in (15, 16, 17):
            m.keep_clear.add((x, y))
    for x in range(5, 27):
        m.keep_clear.add((x, 16))
        m.keep_clear.add((x, 17))

    # ---- 6. Dressing ----
    wf_crest = RC.vauto('rejuvenation', 'Waterfall crest', 0)
    wf_mid = RC.vauto('rejuvenation', 'Waterfall', 0)
    wf_bot = RC.vauto('rejuvenation', 'Waterfall bottom', 0)
    for wx in (6, 7):
        m.over.append((2, wx, 8, wf_crest))
        m.over.append((2, wx, 9, wf_mid))
        m.over.append((2, wx, 10, wf_mid))
        m.over.append((2, wx, 11, wf_bot))

    # Cohesive 2-row weathered maritime wharf timber jetties (ak 1516..1534, pas=0, pri=0) -> ZERO gap & 0 PASS warnings!
    ak_top = [K.C('ak', 1516), K.C('ak', 1517), K.C('ak', 1518)]
    ak_bot = [K.C('ak', 1532), K.C('ak', 1533), K.C('ak', 1534)]
    for x0, x1 in ((6, 13), (19, 25)):
        for x in range(x0, x1 + 1):
            col = 0 if x == x0 else (2 if x == x1 else 1)
            m.over.append((1, x, 16, ak_top[col]))
            m.over.append((1, x, 17, ak_bot[col]))

    # Solid 1x2 Smuggler Tide-Post (L2=23917 at (19,9), SOLID L1=23918 pas=15 at (19,10) right on the sign!)
    _place_over_stamp(m, 'cv_post', 19, 9)

    for x, y in ((15, 15), (6, 11), (27, 24)):
        if m.inb(x + 1, y + 2):
            m.stamps.append(('cv_shaft', x, y))
    for x, y in ((15, 15), (6, 11), (2, 25), (27, 25)):
        m.stamps.append(('pf_glow', x, y))

    for name, x, y in (
        ('cv_xsea2', 9, 12), ('cv_xblue2', 10, 13), ('L_stal', 11, 12),
        ('cv_xblue2', 21, 12), ('cv_xsea2', 22, 13), ('L_stal', 23, 12),
        ('cv_xsea2', 8, 18), ('L_stal', 9, 19), ('cv_xblue2', 10, 18),
        ('cv_xblue2', 21, 18), ('cv_xsea2', 22, 19), ('L_stal', 23, 18),
    ):
        _place_over_stamp(m, name, x, y)
    for x, y, n in (
        (10, 14, 'cv_barn'), (9, 14, 'cv_nest'),
        (22, 14, 'cv_barn'), (23, 14, 'cv_xsea'),
        (8, 20, 'cv_barn'), (9, 20, 'cv_xblue'),
        (22, 20, 'cv_barn'), (23, 20, 'cv_nest'),
    ):
        m.over.append((1, x, y, P1(n)))
        m.taken[y, x] = True

    for name, x, y in (
        ('cv_lamp_on', 14, 3), ('cv_lamp_on', 18, 3),
        ('cv_lamp_on', 12, 9), ('cv_lamp_on', 22, 10),
        ('cv_lamp_on', 4, 22), ('cv_lamp_on', 27, 22),
        ('pf_whalebone', 19, 3), ('pf_whalebone', 2, 19), ('pf_whalebone', 28, 15),
        ('cv_drift', 12, 25), ('cv_drift', 26, 24), ('cv_drift', 15, 18),
        ('hb_barrels', 2, 23), ('hb_barrels', 28, 12),
        ('cv_xsea2', 11, 3), ('cv_xblue2', 20, 3),
        ('L_stal', 2, 14), ('cv_xsea2', 29, 13), ('cv_xblue2', 5, 25), ('L_stal', 25, 25),
    ):
        _put_if(m, name, x, y, on='.')

    for x, y in ((13, 4), (19, 4), (3, 16), (4, 21), (27, 19), (10, 26), (18, 26), (14, 15)):
        if m.free(x, y, 1, 1, on='.') and (x, y) not in m.keep_clear:
            m.over.append((2, x, y, P1('cv_fung0' if (x + y) % 2 == 0 else 'cv_fung1')))
            m.taken[y, x] = True

    for x, y in ((13, 1), (19, 1), (12, 6), (20, 6), (3, 11), (28, 11)):
        if m.inb(x, y) and m.cliff[y, x]:
            m.over.append((2, x, y, P1('cv_walllamp')))

    m.solid_props(['cv_barn', 'L_rock0', 'cv_xsea', 'cv_xblue'], 10, seed=5651)
    m.dress(12, groups=[(['L_fd0', 'L_fd1', 'L_fd2', 'cv_kelp0', 'cv_kelp1', 'cv_wrack'], 6),
                        (['L_rubble0', 'L_rubble1'], 2)], seed=5652)

    m.paint()
    # Mount shaft ladder firmly against solid dark slate cliff face on y=0 (15..17) so ladder rests on rock, NOT bare floor!
    for rx in (15, 16, 17):
        m.L[0, 0, rx] = m.L[0, 0, 14]
        m.L[1, 0, rx] = m.L[1, 0, 14]
    m.L[2, 0, 16] = P1('cv_ladder_q')
    m.L[2, 1, 16] = P1('cv_ladder_q')

    head = {
        'id': 565,
        'name': 'Gullcry Caves B1F',
        'parent': 564,
        'bgm': 'Cave',
        'field': 'CAVE',
        'map_audio': {'bgm': 'Dungeon - Cave', 'bgs': 'Drip - Nadir', 'bgs_volume': 70, 'rain': False},
        'metadata': {'Name': 'Gullcry Caves B1F', 'MapPosition': [0, 2, 8], 'BattleBack': 'cave1', 'SnapEdges': True},
        'tone': [-14, -6, 12, 18],
        'fog': {'name': 'prismfall_seamist', 'opacity': 38, 'blend': 1, 'zoom': 100, 'sx': 1, 'sy': 0},
        '_file': '565_gullcry_caves_b1f.yaml',
    }
    return write_raw_map(m, 565, TID57, head,
                         '# GENERATED by mapgen/layouts/act1_frontier_dungeons.py: Gullcry Caves B1F.\n',
                         start=(16, 2))


# ==============================================================================
# MAP 2: 584 Voltaic Sluiceworks (40x32, TS 60 PF Rejuv Lumen, field SCRAPYARD)
# ==============================================================================
def build_584():
    m = Cave(40, 32, 'Q', seed=584, pool='Cave Pool', tid=TID60)
    m.STAIRS = LK.STAIRS_LM or K.STAIRS_STONE
    m.kit = {TER: 'cvQ', FLOOR: 'cvQ', 'default': 'cvQ'}
    B_ = m.box

    # ---- 1. Sculpted Abandoned Hydro-Plant Architecture ----
    # Raised North Turbine Gallery (TER, y=2..6 -> cliff y=1..3, walkable y=4..5, x=2..38 -> warp [38,4]!)
    B_(2, 2, 38, 6, TER, '.')
    # Main Hydro-Plant Hall (FLOOR touches TER+1 at y=7 -> cliff y=6..8, walkable y=9..28!)
    B_(2, 7, 37, 28, FLOOR, '.')
    # South Dam Intake Vestibule (x=17..23, y=29..31; warp at [20,31])
    B_(17, 29, 23, 31, FLOOR, '.')
    m.mass_at([(2, 27), (2, 28), (3, 28), (37, 27), (37, 28), (36, 28),
               (15, 30), (16, 30), (24, 30), (25, 30)])

    # Twin Flooded Hydro-Spillway Basins (Cave Pool = tag 6 StillWater -> surfable & fishable!)
    B_(5, 12, 16, 19, FLOOR, 'w')     # West Spillway Basin
    B_(24, 12, 34, 19, FLOOR, 'w')    # East Tailrace Basin
    # Expanded central concrete piers (y=14..16) so lm_pylon_off sits cleanly inside water, ZERO rim clipping!
    m.mass_at([(10, 14), (11, 14), (10, 15), (11, 15), (10, 16), (11, 16),
               (28, 14), (29, 14), (28, 15), (29, 15), (28, 16), (29, 16)])

    # Twin Wide Steel Staircases climbing FLOOR (y>=7) <-> TER (y<=6): spans y=6,7,8!
    m.stairs(6, 6, w=3, n=3, c='.')
    m.stairs(31, 6, w=3, n=3, c='.')
    m.plan_cliffs(rows=3)

    # ---- 2. Events ----
    E = m.events
    E += [
        {'type': 'warp', 'name': 'To The Reedholms', 'at': [20, 31],
         'link': 'R7_SLUICE', 'arrive': [20, 30, 'up'], 'se': 'Door exit'},
        {'type': 'warp', 'name': 'To Turbine Hall', 'at': [38, 4],
         'link': 'SLUICE_TURB', 'arrive': [37, 4, 'left'], 'se': 'Door exit'},
        {'type': 'event', 'name': 'West Breaker Console', 'at': [4, 21], 'pages': [
            {'graphic': {'tile': P1('lm_junction')}, 'trigger': 'action', 'commands': [
                {'se': 'PC open'},
                {'script': 'pfm_set(:sluice_b1)'},
                'You throw Sluice Breaker A. A dead relay clacks loud enough to echo off the spillway.',
                {'if': 'pfm?(:sluice_b2)', 'then': [
                    {'se': 'Door exit'},
                    'Across the hall, power surges to the spillway blast latch and the Turbine Hall shutter!'
                ], 'else': ['One breaker live. The twin relay on the east gallery is still dark.']},
                {'selfswitch': ['A', True]},
            ]},
            {'cond': {'self': 'A'}, 'graphic': {'tile': P1('lm_junction_on')}, 'trigger': 'action', 'commands': [
                'Sluice Breaker A is latched ON. Its indicator bulb buzzes faintly amber.'
            ]}
        ]},
        {'type': 'event', 'name': 'East Breaker Console', 'at': [35, 22], 'pages': [
            {'graphic': {'tile': P1('lm_junction')}, 'trigger': 'action', 'commands': [
                {'se': 'PC open'},
                {'script': 'pfm_set(:sluice_b2)'},
                'You throw Sluice Breaker B. Static snaps across the catwalk rails.',
                {'if': 'pfm?(:sluice_b1)', 'then': [
                    {'se': 'Door exit'},
                    'Across the hall, power surges to the spillway blast latch and the Turbine Hall shutter!'
                ], 'else': ['One breaker live. The twin relay on the west spillway is still dark.']},
                {'selfswitch': ['A', True]},
            ]},
            {'cond': {'self': 'A'}, 'graphic': {'tile': P1('lm_junction_on')}, 'trigger': 'action', 'commands': [
                'Sluice Breaker B is latched ON. A faint smell of ozone hangs around the casing.'
            ]}
        ]},
        # SOLID 1-tile Central Spillway Blast Gate (flanked by solid brass rails at x=18..19 & 21..22 -> UNBYPASSABLE on catwalk!)
        {'type': 'event', 'name': 'Spillway Blast Gate', 'at': [20, 16], 'pages': [
            {'graphic': {'tile': P1('lm_latch')}, 'trigger': 'action', 'through': False, 'commands': [
                {'if': 'pfm?(:sluice_b1) && pfm?(:sluice_b2)', 'then': [
                    {'se': 'Door exit'},
                    'Both breakers are live — the spillway blast gate retracts smoothly into the grate.',
                    {'selfswitch': ['A', True]}
                ], 'else': [
                    'A locked Meridian spillway blast gate spans the middle catwalk. Both the West and East Breaker Consoles are tripped off.'
                ]}
            ]},
            {'cond': {'self': 'A'}, 'graphic': {'tile': P1('lm_latch_open')}, 'trigger': 'action', 'through': True, 'commands': [
                'The spillway blast gate is retracted. Emergency strip lights glow along the catwalk.'
            ]}
        ]},
        # SOLID UNBYPASSABLE Turbine Hall Security Blast Shutter at (36,4) (bollard seals (36,5)!) -> proves puzzle gates [38,4]!
        {'type': 'event', 'name': 'Turbine Blast Shutter', 'at': [36, 4], 'pages': [
            {'graphic': {'tile': P1('cv_gate_shut')}, 'trigger': 'action', 'through': False, 'commands': [
                {'if': 'pfm?(:sluice_b1) && pfm?(:sluice_b2)', 'then': [
                    {'se': 'Door exit'},
                    'Both spillway breakers are live — the heavy iron Turbine Hall shutter grinds open!',
                    {'selfswitch': ['A', True]}
                ], 'else': [
                    'The iron blast shutter sealing the Turbine Hall is dead cold. Flip both the West and East Spillway Breakers downstairs to power the unlock relay.'
                ]}
            ]},
            {'cond': {'self': 'A'}, 'graphic': {'tile': P1('lm_latch_open')}, 'trigger': 'action', 'through': True, 'commands': [
                'The Turbine Hall blast shutter stands unlocked. Ozone hums from the turbine bay beyond.'
            ]}
        ]},
        _sign((20, 12), 'Turbine Builder Plate',
              "BUILDER'S PLATE (riveted to the dead turbine): \"VOLTAIC SLUICE No. 1 — FIRST LIGHT, AF 289 — DESIGN: I. LARCH, CHIEF ENGINEER.\" Scratched underneath, very small, in no particular hand: SORRY."),
        _sign((13, 24), 'Rook Clapperboard',
              "A dropped studio clapperboard resting on a rusted crate: \"ROOK CALDER LIVE — EP. 112 — TAKE 41.\" Forty takes are crossed out."),
        _sign((18, 3), 'Hydro Telemetry Screen',
              "A cracked Meridian telemetry screen still flickering on trickle current: 'SPILLWAY FLOW: STALLED — TURBINE HALL: ISOLATED — CAUTION: STRAY ROTOM ACTIVITY.'"),
        # BOTH Canonical PBS Trainers (# Map 584 Voltaic Sluiceworks): SUPERNERD Elwin & BURGLAR Nix!
        _trainer((10, 22), 'SUPERNERD', 'Elwin',
                 "Elwin: Wait — don't step on that chalk mark! Rook Calder stood right here for Episode 112! Battle me for front-row rights!",
                 "Elwin: Episode 112 was filmed RIGHT HERE. Take 41. I counted.",
                 d='right', sight=4, field='SCRAPYARD'),
        _trainer((30, 10), 'BURGLAR', 'Nix',
                 "Nix: Hey! I saw the copper coils first! Nobody's used this plant in nine years!",
                 "Nix: It's decommissioned! It's not stealing if it's decommissioned!",
                 d='left', sight=4, field='SCRAPYARD'),
        _item((3, 4), 'THUNDERSTONE', 'Thunder Stone'),
        _item((35, 27), 'ELEMENTALSEED', 'Elemental Seed'),
        _item((27, 25), 'SUPERPOTION', 'Super Potion'),
        _item((15, 5), 'QUICKBALL', 'Hidden Quick Ball', hidden=True),
    ]

    m.keep_clear |= {
        (20, 31), (20, 30), (20, 29), (38, 4), (37, 4), (36, 4), (35, 4), (35, 5),
        (4, 21), (5, 21), (4, 22), (35, 22), (34, 22), (35, 21),
        (20, 16), (20, 15), (20, 17), (20, 13), (20, 12),
        (13, 24), (13, 25), (14, 24), (18, 3), (18, 4), (18, 5),
        (10, 22), (11, 22), (12, 22), (13, 22), (14, 22), (30, 10), (29, 10), (3, 4), (4, 4),
        (35, 27), (34, 27), (27, 25), (15, 5),
    }
    for x in (6, 7, 8, 31, 32, 33):
        for y in range(4, 11):
            m.keep_clear.add((x, y))

    # ---- 3. Industrial Hydro-Plant Dressing ----
    _place_over_stamp(m, 'lm_gen', 19, 11)
    # Pylons anchored cleanly inside basins at y=13 (ZERO north basin rim clipping!)
    _place_over_stamp(m, 'lm_pylon_off', 10, 13)
    _place_over_stamp(m, 'lm_pylon_off', 28, 13)
    _place_over_stamp(m, 'lm_table', 13, 24)
    _place_over_stamp(m, 'lm_cam', 12, 23)

    # ALL 3 north telemetry banks hung cleanly flush on cliff wall y=2 (ZERO protrusion onto walkway y=4!)
    _hang(m, 'lm_monitors', 10, 2)
    _hang(m, 'lm_monitors', 17, 2)
    _hang(m, 'lm_monitors', 24, 2)
    _on_faces(m, 'lm_alarm', [(4, 3), (22, 3), (35, 3)])
    _on_faces(m, 'lm_poster0', [(14, 3), (28, 3)])
    _on_faces(m, 'lm_vent', [(8, 3), (32, 3)])
    _on_faces(m, 'lm_pdoor_open', [(38, 3)])

    # Solid brass railings framing both basins + narrow 1-tile Spillway Blast Gate choke at (18..19,16) & (21..22,16)!
    for x in range(5, 17):
        t = 'lm_railing_w' if x == 5 else ('lm_railing_e' if x == 16 else 'lm_railing_m')
        m.over.append((1, x, 20, P1(t)))
        m.taken[20, x] = True
    for x in range(24, 35):
        t = 'lm_railing_w' if x == 24 else ('lm_railing_e' if x == 34 else 'lm_railing_m')
        m.over.append((1, x, 20, P1(t)))
        m.taken[20, x] = True
    for x, t in ((18, 'lm_railing_w'), (19, 'lm_railing_e'), (21, 'lm_railing_w'), (22, 'lm_railing_e')):
        m.over.append((1, x, 16, P1(t)))
        m.taken[16, x] = True
    # Solid steel bulkhead bollard at (36, 5) sealing the Turbine Hall entry cleanly to the 1-tile shutter at (36, 4)!
    m.over.append((1, 36, 5, P1('lm_bollard')))
    m.taken[5, 36] = True

    for name, x, y in (
        ('lm_gen', 14, 25), ('lm_gen', 24, 25),
        ('lm_rack', 3, 24), ('lm_rack', 36, 24),
        ('lm_steam0', 17, 13), ('lm_steam1', 22, 17),
        ('lm_arclamp_off', 17, 26), ('lm_arclamp_off', 23, 26),
        ('lm_arclamp', 18, 13), ('lm_arclamp', 22, 13),
        ('lm_gearbox', 21, 11), ('lm_gearbox', 18, 22), ('lm_gearbox', 25, 23),
        ('lm_bollard', 18, 28), ('lm_bollard', 22, 28),
        ('lm_junk0', 7, 26), ('lm_junk1', 8, 26), ('lm_junk2', 31, 26), ('lm_junk3', 32, 25),
        ('lm_cables', 16, 21), ('lm_cables', 24, 22), ('lm_cables', 12, 5), ('lm_cables', 26, 5),
    ):
        _put_if(m, name, x, y, on='.')

    m.stamps.append(('cv_shaft', 36, 3))

    m.paint()

    # Deep-water cores inside both flooded hydro-spillway basins (Sea deep autotile on L1, auto-shaped cleanly!)
    v_deep = RC.vauto('rejuvenation', 'Sea deep', 0)
    for x0, x1 in ((6, 15), (25, 33)):
        for yy in range(13, 19):
            for xx in range(x0, x1 + 1):
                if m.cls[yy, xx] == 'w' and m.L[1, yy, xx] == 0:
                    m.L[1, yy, xx] = v_deep

    paves = [P1(f'lm_pave{i}') for i in range(4)]
    for yy in range(m.H):
        for xx in range(m.W):
            if m.cls[yy, xx] == '.':
                if yy in range(11, 20) and xx in (18, 19, 20, 21, 22):
                    m.L[0, yy, xx] = P1('lm_grate') if xx in (19, 20, 21) else P1('Z_f0')
                elif yy in range(11, 20) and (xx in (2, 3, 4) or xx in (35, 36, 37)):
                    m.L[0, yy, xx] = P1('lm_grate') if xx in (3, 36) else P1('Z_f0')
                elif yy <= 5:
                    m.L[0, yy, xx] = paves[(xx * 3 + yy * 5) % 4]
                else:
                    m.L[0, yy, xx] = P1('Z_f0') if (xx + yy) % 2 == 0 else P1('Z_f2')
    for yy in range(14, 30):
        if m.cls[yy, 20] == '.':
            m.L[0, yy, 20] = P1('lm_inlay_v')
    for xx in range(8, 38):
        if m.cls[5, xx] == '.':
            m.L[0, 5, xx] = P1('lm_inlay_h')

    head = {
        'id': 584,
        'name': 'Voltaic Sluiceworks',
        'parent': 580,
        'bgm': 'Cave',
        'field': 'SCRAPYARD',
        'gates': [{'name': 'Turbine Blast Shutter', 'from': [[20, 30]], 'sealed': [[38, 4]]}],
        'map_audio': {'bgm': 'Dungeon - Cave', 'bgs': 'Machinery - Zenith', 'bgs_volume': 55, 'rain': False},
        'metadata': {'Name': 'Voltaic Sluiceworks', 'MapPosition': [0, 4, 6], 'BattleBack': 'indoor3', 'SnapEdges': True},
        'tone': [-14, -10, 4, 24],
        'fog': {'name': 'prismfall_cave', 'opacity': 34, 'blend': 1, 'zoom': 100, 'sx': 1, 'sy': 0},
        '_file': '584_voltaic_sluiceworks.yaml',
    }
    return write_raw_map(m, 584, TID60, head,
                         '# GENERATED by mapgen/layouts/act1_frontier_dungeons.py: Voltaic Sluiceworks.\n',
                         start=(20, 30),
                         ignore_gate_events=((20, 16), (36, 4)))


# ==============================================================================
# MAP 3: 585 Sluiceworks Turbine Hall (30x24, TS 60 PF Rejuv Lumen, SCRAPYARD)
# ==============================================================================
def build_585():
    m = Cave(30, 24, 'Q', seed=585, pool='Cave Pool', tid=TID60)
    m.STAIRS = LK.STAIRS_LM or K.STAIRS_STONE
    m.kit = {TER: 'lmw', FLOOR: 'cvQ', 'default': 'cvQ'}
    B_ = m.box

    # ---- 1. Sculpted Vaulted Turbine Hall + Solid Chasm Core Plinths + Walled NE Bay ----
    # Raised North Control Dais (TER, y=2..9) seamlessly joined to walled NE Cell Bay (y=2..6, x=21..28 -> capped at y=0..1!)
    B_(9, 2, 21, 9, TER, '.')
    B_(21, 2, 28, 6, TER, '.')
    # Lower Hall & Spacious West Entrance Corridor (FLOOR touches TER+1 at y=10 -> cliff y=9..11, walkable y=12..21!)
    B_(6, 10, 23, 21, FLOOR, '.')
    B_(1, 17, 6, 21, FLOOR, '.')
    # Twin Abyssal Dynamo Chasms (PIT -> lm_deep0..5) with SOLID structural steel plinths supporting dead cores!
    B_(2, 4, 7, 15, PIT, 'p')
    B_(23, 8, 28, 17, PIT, 'p')
    # Solid MASS plinths inside each chasm (ZERO cliff clipping, ZERO void-floating props, ZERO walk_check cutoff!)
    m.mass_at([(3, 9), (4, 9), (5, 9), (3, 10), (4, 10), (5, 10), (3, 11), (4, 11), (5, 11),
               (24, 12), (25, 12), (26, 12), (24, 13), (25, 13), (26, 13), (24, 14), (25, 14), (26, 14)])
    # Twin South Flooded Coolant Sumps shifted cleanly north (y=17..19 -> leaves wide unobstructed y=20..21 entry corridor!)
    B_(8, 17, 11, 19, FLOOR, 'w')
    B_(19, 17, 22, 19, FLOOR, 'w')
    m.mass_at([(24, 19), (25, 19), (26, 19), (24, 20), (25, 20), (26, 20), (27, 20)])

    # Grand central steel staircase climbing FLOOR (y>=10) <-> TER (y<=9): spans y=9,10,11!
    m.stairs(14, 9, w=3, n=3, c='.')
    m.plan_cliffs(rows=3)

    # ---- 2. Events ----
    E = m.events
    E += [
        {'type': 'warp', 'name': 'To Voltaic Sluiceworks', 'at': [1, 20],
         'link': 'SLUICE_TURB', 'arrive': [2, 20, 'right'], 'se': 'Door exit'},
        {'type': 'event', 'name': 'Wild Rotom', 'at': [15, 6], 'pages': [
            {'graphic': {'sprite': 'Followers/ROTOM', 'dir': 'down'}, 'trigger': 'action',
             'step_anime': True, 'commands': [
                 {'se': 'Cries/ROTOM'},
                 'The old Meridian control desk crackles violet — a grinning Rotom bursts straight out of the dead voltmeter!',
                 {'script': 'setBattleRule("field", :SCRAPYARD)\nWildBattle.start(:ROTOM, 25)'},
                 {'selfswitch': ['A', True]},
             ]},
            {'cond': {'self': 'A'}, 'commands': []},
        ]},
        _item((26, 4), 'CELLBATTERY', 'Cell Battery'),
        _item((8, 16), 'SYNTHETICSEED', 'Synthetic Seed'),
        _item((21, 15), 'ULTRABALL', 'Hidden Ultra Ball', hidden=True),
        _sign((12, 3), 'Turbine Log Console',
              "COMMISSIONING LOG (AF 291): 'Sluiceworks decommissioned ahead of Icefall Lattice No. 4 switch-on. All spare Cell Batteries requisitioned to Brassfall lift-works — except one jammed behind the NE breaker.'"),
        _sign((18, 3), 'Rook Camera Note',
              "A battered camera tripod taped to the console with neon tape: 'EP. 112 — BATTERY DEAD — SOMETHING INSIDE THE VOLTMETER JUST ATE MY SCRIPT CARDS. WE ARE LEAVING. — R.C.'"),
    ]

    m.keep_clear |= {
        (1, 20), (2, 20), (3, 20), (15, 6), (15, 7), (14, 6), (16, 6),
        (26, 4), (25, 4), (26, 5), (12, 3), (12, 4), (18, 3), (18, 4),
        (8, 16), (21, 15),
    }
    for x in (14, 15, 16):
        for y in range(9, 15):
            m.keep_clear.add((x, y))

    # ---- 3. Monumental Turbine Hall Dressing ----
    # Dead turbine cores anchored squarely atop the two solid chasm plinths (ZERO cliff clipping, ZERO void-floating!)
    _abyss_piece(m, 'lm_core', 3, 8)
    _abyss_piece(m, 'lm_core', 24, 11)

    _place_over_stamp(m, 'lm_desk', 14, 4)
    # BOTH dais monitors hung cleanly flush on north cliff wall y=2 (ZERO protrusion onto marble floor y=4!)
    _hang(m, 'lm_monitors', 11, 2)
    _hang(m, 'lm_monitors', 17, 2)
    _hang(m, 'lm_banner', 15, 1)
    _on_faces(m, 'lm_alarm_on', [(10, 2), (20, 2), (26, 2)])

    for name, x, y in (
        ('lm_gen', 9, 7), ('lm_gen', 19, 7),
        ('lm_rack', 23, 4), ('lm_gearbox', 27, 4),
        ('lm_arclamp', 12, 13), ('lm_arclamp', 18, 13),
        ('lm_bollard', 13, 13), ('lm_bollard', 17, 13),
        ('lm_cam', 19, 5),
        ('lm_junk0', 7, 14), ('lm_junk2', 22, 14), ('lm_cables', 13, 16), ('lm_cables', 17, 16),
    ):
        _put_if(m, name, x, y, on='.')

    for x, y in ((14, 4), (25, 3), (14, 14)):
        if m.inb(x + 1, y + 2):
            m.stamps.append(('cv_shaft', x, y))
    m.stamps.append(('pf_glow', 14, 5))

    m.paint()

    v_deep = RC.vauto('rejuvenation', 'Sea deep', 0)
    for x0, x1 in ((9, 10), (20, 21)):
        for yy in (18,):
            for xx in range(x0, x1 + 1):
                if m.cls[yy, xx] == 'w' and m.L[1, yy, xx] == 0:
                    m.L[1, yy, xx] = v_deep

    deeps = [P1(f'lm_deep{i}') for i in range(6)]
    paves = [P1(f'lm_pave{i}') for i in range(4)]
    for yy in range(m.H):
        for xx in range(m.W):
            if m.cls[yy, xx] == 'p':
                m.L[0, yy, xx] = deeps[(xx * 7 + yy * 13) % 6]
            elif m.cls[yy, xx] == '.':
                if m.ht[yy, xx] == TER:
                    m.L[0, yy, xx] = paves[(xx * 3 + yy * 5) % 4] if (xx <= 21) else P1('lm_grate')
                else:
                    m.L[0, yy, xx] = P1('lm_grate') if xx in (14, 15, 16) else (P1('Z_f0') if (xx + yy) % 2 == 0 else P1('Z_f2'))
    for yy in range(13, 21):
        if m.cls[yy, 15] == '.':
            m.L[0, yy, 15] = P1('lm_inlay_v')
    for xx in range(2, 16):
        if m.cls[20, xx] == '.':
            m.L[0, 20, xx] = P1('lm_inlay_h')
    for xx in range(19, 27):
        if m.cls[4, xx] == '.':
            m.L[0, 4, xx] = P1('lm_inlay_h')

    head = {
        'id': 585,
        'name': 'Sluiceworks Turbine Hall',
        'parent': 584,
        'bgm': 'Cave',
        'field': 'SCRAPYARD',
        'map_audio': {'bgm': 'Dungeon - Cave', 'bgs': 'Machinery - Zenith', 'bgs_volume': 65, 'rain': False},
        'metadata': {'Name': 'Sluiceworks Turbine Hall', 'MapPosition': [0, 4, 6], 'BattleBack': 'indoor3', 'SnapEdges': True},
        'tone': [-18, -14, 8, 28],
        'fog': {'name': 'prismfall_cave', 'opacity': 38, 'blend': 1, 'zoom': 100, 'sx': 1, 'sy': 0},
        '_file': '585_sluiceworks_turbine_hall.yaml',
    }
    return write_raw_map(m, 585, TID60, head,
                         '# GENERATED by mapgen/layouts/act1_frontier_dungeons.py: Sluiceworks Turbine Hall.\n',
                         start=(2, 20))


# ==============================================================================
# MAP 4: 588 Ebb Hollow (34x30, TS 60 PF Rejuv Lumen, field BLEED, rubric: true)
# ==============================================================================
def build_588():
    W, H = 34, 30
    if 'sh3' not in K.KITS:
        K.KITS['sh3'] = dict(K.KITS['sh'], rows=[K.KITS['sh']['rows'][0], K.KITS['sh']['rows'][1], K.KITS['sh']['rows'][3]])
    m = City(W, H, 588, base='.')
    m.auto = {
        'w': ('Still water', 'rejuvenation'),
        'W': ('Sea deep', 'rejuvenation'),
        'd': ('Gravel Spring', 'pf'),
        'u': ('DirtDark', 'rejuvenation'),
    }
    m.JOIN = dict(K.RMap.JOIN, w='wW', W='wW', d='d', u='u')
    m.AUTO_Z = dict(K.RMap.AUTO_Z, w=0, W=1, d=1, u=1)
    m.kit = {1: 'sh3', 2: 'shc', 'default': 'sh3'}
    m.STAIRS = tuple(P1('st_stair_' + k) for k in 'lmr')
    m.grass = K.SH_GRASS
    m.tall = K.SH_TALL

    # ---- 1. Surreal Drowned Village of Holmsby: Sealed Perimeter Woods, Lifted River Pools & Dry Lanes ----
    m.cls[:, :] = '.'
    # Fully sealed irregular Bleed-tinted woodland rim enclosing ALL edges (y<2, x<2, y>=H-2, and E except Veil!)
    for y in range(H):
        for x in range(W):
            w_rim = 3 + int(2.0 * vnoise(x, y, 5881, 4.0))
            if (x < 2 or y < 2 or y >= H - 2
                    or (x < w_rim and y > 6)
                    or (y >= H - 3 and x < 24)
                    or (x >= W - 3 and abs(y - 15) > 3)):
                m.cls[y, x] = 'T'

    # Lifted River Basins (organic NW & SW pools where the Ebb pulled off its bed, staying cleanly inside x>=3!)
    for y in range(4, 12):
        for x in range(3, 9):
            if ((x - 5.5) / 3.2) ** 2 + ((y - 7.8) / 3.2) ** 2 <= 1.0 + 0.25 * (vnoise(x, y, 5882, 2.5) - 0.5):
                m.cls[y, x] = 'w'
    for y in range(18, 27):
        for x in range(3, 10):
            if ((x - 5.8) / 3.6) ** 2 + ((y - 22.5) / 3.4) ** 2 <= 1.0 + 0.25 * (vnoise(x, y, 5883, 2.5) - 0.5):
                m.cls[y, x] = 'w'
    # Keep enclosed NW TM49 glade (x=3..10, y=3..6) cleanly dry & reachable!
    for y in range(3, 6):
        for x in range(3, 11):
            m.cls[y, x] = '.'
    # Keep SE Bleed Shard #4 grotto (x=24..30, y=21..26) dry & reachable inside sealed perimeter!
    for y in range(21, 27):
        for x in range(24, 31):
            if m.cls[y, x] == 'T':
                m.cls[y, x] = '.'

    # Dry village lanes (Gravel Spring 'd' & DirtDark 'u') weaving from East Bleed Veil [33,15] through Holmsby!
    m.lane([(33, 15), (27, 15), (21, 14), (15, 15), (10, 13), (10, 8), (11, 4), (5, 4)], c='d', w=2.2, seed=5884)
    m.lane([(21, 14), (22, 20), (28, 25)], c='u', w=2.0, seed=5885)
    m.lane([(15, 15), (14, 23), (19, 24), (24, 24)], c='u', w=1.9, seed=5886)
    # Guarantee clean east entrance corridor (28..33, 13..17)
    for y in range(13, 18):
        for x in range(28, 34):
            m.cls[y, x] = 'd' if y in (14, 15, 16) else '.'
            m.ht[y, x] = 0

    m.ht[:, :] = 0
    # Scenic raised northern rock bluff (ht=1, y=0..4, x=14..26) purely as dramatic forested backdrop!
    for y in range(0, 4):
        for x in range(14, 27):
            m.ht[y, x] = 1
            m.cls[y, x] = 'T'

    # Re-seal perimeter borders strictly after lanes (ZERO NW corner leaks, ZERO bottom edge leaks!)
    for y in range(H):
        for x in range(W):
            if x < 2 or y < 2 or y >= H - 2:
                m.cls[y, x] = 'T'

    # Lush submerged marsh-weed tall grass patches (matching maps.json [8,12] 18x10 spirit & Land,25 encounters!)
    for y in range(10, 24):
        for x in range(7, 27):
            if m.cls[y, x] == '.' and vnoise(x, y, 5889, 3.6) > 0.36:
                m.cls[y, x] = 'g'

    # Keep footprints clean for Holmsby's 3 weathered cottages, NW TM49 glade & SE Shard #4 clearing
    for x0, y0, x1, y1 in (
        (11, 7, 17, 13),   # Cottage 1: House #9 (wb_short 6x6)
        (21, 7, 27, 13),   # Cottage 2: Kitchen cottage (wb_hut 5x5)
        (12, 18, 19, 24),  # Cottage 3: Cradle cottage (wb_smoke 7x6)
        (3, 3, 7, 5),      # Enclosed NW TM49 clearing (x=3..7, y=3..5 inside x>=2, y>=2 trees!)
        (26, 23, 30, 26),  # SE Bleed Shard #4 clearing
    ):
        for yy in range(y0, y1 + 1):
            for xx in range(x0, x1 + 1):
                if m.inb(xx, yy) and m.cls[yy, xx] in ('T', 'w', 'g'):
                    m.cls[yy, xx] = '.'

    m.plan_cliffs(rows=3)

    # ---- 2. Multi-Species Surreal Bleed-Tinted Woods (hooked cleanly into m.forest -> ZERO double-paint & ZERO tr_teal!) ----
    bleed_pal = [
        {'purp': 5, 'blue': 4, 'teal2': 2},
        {'blue': 5, 'purp': 3, 'pink': 2},
        {'purp': 4, 'teal': 3, 'blue': 3},
    ]

    def _paint_bleed_woods(*_a, **_kw):
        rng = random.Random(5880)
        msk = (m.cls == 'T')
        tw, nt, nb = 3, 2, 2
        phase = 1
        for ty in range(-nt, H, 2):
            phase = (phase + rng.choice((1, 2))) % tw
            for tx in range(phase - tw, W, tw):
                foot = [(tx + dx, ty + nt + dy) for dx in range(tw) for dy in range(nb)]
                if not all(msk[y, x] for x, y in foot if m.inb(x, y)):
                    continue
                if not any(m.inb(x, y) for x, y in foot):
                    continue
                pal = bleed_pal[int(vnoise(tx, ty, 5887, 8.0) * len(bleed_pal) * 0.999)]
                sp = rng.choices(list(pal), list(pal.values()))[0]
                top, bot, _ = CK.SPECIES[sp]
                for dy in range(nt):
                    for dx in range(tw):
                        xx, yy = tx + dx, ty + dy
                        if m.inb(xx, yy) and top[dy][dx] and m.L[2, yy, xx] == 0:
                            m.L[2, yy, xx] = top[dy][dx]
                for dy in range(nb):
                    for dx in range(tw):
                        xx, yy = tx + dx, ty + nt + dy
                        if m.inb(xx, yy) and bot[dy][dx]:
                            m.L[1, yy, xx] = bot[dy][dx]
                            m.taken[yy, xx] = True
        # Clean infill for narrow perimeter 'T' cells (2x2 Bleed pines -> 1x1 bushes, ZERO gaps!)
        hole = (m.cls == 'T') & ~m.taken & (m.L[1] == 0) & ~m.cliff
        for y in range(H):
            for x in range(W):
                if not hole[y, x]:
                    continue
                placed = False
                for ox in (0, -1):
                    if all(m.inb(x + ox + dx, y + dy) and hole[y + dy, x + ox + dx] for dx in range(2) for dy in range(2)):
                        st = STAMPS[rng.choice(('nt_pine_purp', 'nt_pine_blue'))]
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
                    m.L[1, y, x] = P1(rng.choice(('nt_bush0', 'nt_bush1')))
                    m.taken[y, x] = True
                    hole[y, x] = False

    m.lattice = [CK.SPECIES[k] for k in sorted({sp for pal in bleed_pal for sp in pal})]
    m.forest = _paint_bleed_woods

    # ---- 3. Place Holmsby's Weathered Cottages, Stranded Boats, Upside-Down Garden & ALL 3 Boundary Stones ----
    m.stamp('wb_short', 11, 7)      # House #9 (door at 14,12!)
    m.stamp('wb_hut', 22, 8)        # Kitchen Cottage (door at 24,12!)
    m.stamp('wb_smoke', 12, 18)     # Cradle Cottage (door at 15,23!)

    # Boundary Stone monuments (visible carved pf_roadstone pillars for Trials quest IS_EBB_HOLLOW!)
    m.stamp('pf_roadstone', 26, 16)   # Boundary stone 1 at (26,17)
    m.stamp('pf_roadstone', 17, 11)   # Boundary stone 2 by House #9 at (17,12)
    m.stamp('pf_roadstone', 9, 18)    # 3rd Boundary stone directly beside White coral (10,19)! ("wrapped itself round the last stone")
    # Upside-down bean garden planter right beside Kitchen Cottage
    m.stamp('pf_planter2', 20, 12)    # Garden inspect at (20,12)
    # Stranded river punts, Bleed crystals & violet pines (ZERO glitch nt_reed0/1! Clear of Hidden Big Pearl at (8,4)!)
    for nm, x, y in (
        ('hb_boat1', 7, 13), ('hb_boat3', 24, 19),
        ('pf_well', 20, 18), ('hb_barrels', 10, 12), ('hb_post1', 8, 17), ('hb_post2', 8, 20),
        ('nt_pine_purp', 5, 2), ('nt_pine_blue', 27, 4), ('nt_tree_pink', 28, 7),
        ('nt_pine_blue', 29, 19), ('nt_pine_purp', 28, 10),
        ('cv_xblue2', 3, 4), ('cv_xrose2', 30, 24), ('cv_xsea2', 11, 17), ('cv_xblue2', 26, 23),
        ('nt_shrub0', 10, 22), ('nt_shrub1', 10, 24),
    ):
        if m.inb(x, y) and m.free(x, y, STAMPS[nm]['w'], STAMPS[nm]['h'], on='.gdu'):
            m.stamp(nm, x, y)

    # Shimmering Bleed Veil curtain framing the East entry [33,15] & glowing aura around Bleed Shard #4 + landmarks
    for vy in (13, 14, 15, 16, 17):
        m.over.append((2, 32, vy, P1(f'lm_veil{vy % 3}')))
        m.over.append((2, 33, vy, P1(f'lm_veil{(vy + 1) % 3}')))
    for bx, by in ((28, 15), (22, 14), (16, 15), (14, 24), (29, 25), (4, 4), (19, 19)):
        if m.inb(bx - 1, by - 1):
            m.stamps.append(('pf_glow', bx - 1, by - 1))

    # ---- 4. Events (Warp, Field Notes, 4 Holmsby Inspects, 10 Floating Water Orbs, Trials Hooks, TM49 & Shard #4) ----
    E = m.events
    E += [
        {'type': 'warp', 'name': 'Bleed Veil to The Reedholms', 'at': [33, 15],
         'link': 'R7_HOLLOW', 'arrive': [32, 15, 'left'], 'se': 'Door exit'},
        # First-entry Field Notes autorun (once; story/24_SCRIPT_CH5.md:67)
        {'type': 'event', 'name': 'Field Notes Ebb Hollow', 'at': [0, 0], 'pages': [
            {'trigger': 'autorun', 'commands': [
                'FIELD NOTES: "EBB HOLLOW — BLEED. The Splash Plate\'s reach has lifted a river off its bed. Water hangs; fish swim in air; the field leans on water. (Larch, in the margin: \'If you\'re reading this inside it, I\'m not speaking to you.\')"',
                {'selfswitch': ['A', True]},
            ]},
            {'cond': {'self': 'A'}, 'commands': []},
        ]},
        # All 4 Canonical Holmsby Inspect Lines (anchored on actual visible cottages & garden!)
        _sign((14, 12), 'House Number 9',
              'A house number, painted by hand: 9. Under it, in a child\'s chalk: "WE\'LL BE BACK SATERDAY."'),
        _sign((24, 12), 'Drowned Kitchen',
              'Through the open doorway: a kitchen table laid for four, perfectly dry. Above it, filling the rafters, a drop of river with a trout asleep in it.'),
        _sign((15, 23), 'Empty Cradle',
              'Inside the cottage, an empty wooden cradle. A single drop of river water the size of a fist hangs over it, turning slowly, like a mobile.'),
        _sign((20, 12), 'Upside-Down Bean Garden',
              'The garden beans grew straight up toward the hanging river water and into it. They are still growing, upside down, inside the drop.'),
        # Trials Quest IS_EBB_HOLLOW ("The Names in Holmsby") — exact design/TRIAL_EVENTS.yaml contract!
        {'type': 'event', 'name': 'Boundary stone 1', 'at': [26, 17], 'pages': [
            {'trigger': 'action', 'commands': [
                'A weathered Holmsby boundary stone by the lane, carved deep with family names under a hanging drop of river.'
            ]},
            {'trigger': 'action', 'commands': [
                {'comment': 'Condition: quest_step(:IS_EBB_HOLLOW) == :ask'},
                {'script': 'pf_trial_talk(:HOLLOW_STONE)'},
                {'selfswitch': ['A', True]},
            ]},
            {'cond': {'self': 'A'}, 'trigger': 'action', 'commands': [
                'You have copied the names cut into the stone.'
            ]},
        ]},
        {'type': 'event', 'name': 'Boundary stone 2', 'at': [17, 12], 'pages': [
            {'trigger': 'action', 'commands': [
                'A boundary stone beside House 9. Half a dozen Holmsby names are cut clean into the slate.'
            ]},
            {'trigger': 'action', 'commands': [
                {'comment': 'Condition: quest_step(:IS_EBB_HOLLOW) == :ask'},
                {'script': 'pf_trial_talk(:HOLLOW_STONE)'},
                {'selfswitch': ['A', True]},
            ]},
            {'cond': {'self': 'A'}, 'trigger': 'action', 'commands': [
                'You have copied the names cut into the stone beside House 9.'
            ]},
        ]},
        {'type': 'event', 'name': 'White coral', 'at': [10, 19], 'pages': [
            {'commands': []},
            {'graphic': {'sprite': 'Followers/CORSOLA_1', 'dir': 'down'}, 'trigger': 'action', 'commands': [
                {'comment': 'Condition: quest_step(:IS_EBB_HOLLOW) == :coral'},
                {'script': 'pf_trial_talk(:HOLLOW_CORAL)'},
            ]},
        ]},
        # Canonical TM49 (Scald) inside enclosed NW glade & distinct rose-pink Bleed Shard #4 with valid SE 'Mining item get'!
        _item((4, 4), 'TM49', 'TM49 Scald'),
        {'type': 'event', 'name': 'Bleed Shard #4', 'at': [29, 25], 'pages': [
            {'graphic': {'tile': 23887}, 'trigger': 'action', 'commands': [
                'A rose-bright shard of river-cool Bleed glass hovering an inch off the mud, humming a steady water-note.',
                {'if': '!pfm?(:bleed_shard_4)', 'then': [
                    {'se': 'Mining item get'},
                    {'script': 'pfm_set(:bleed_shard_4)'},
                    '(Bleed Shard #4. You pocket it. A faint ring of droplets settles in the grass where it hung.)'
                ], 'else': ['Only the hum of suspended water remains.']},
                {'selfswitch': ['A', True]},
            ]},
            {'cond': {'self': 'A'}, 'trigger': 'action', 'commands': ['Only a faint water-hum remains where the shard hovered.']},
        ]},
        _item((21, 25), 'MAGICALSEED', 'Magical Seed'),
        _item((8, 4), 'BIGPEARL', 'Hidden Big Pearl', hidden=True),
    ]

    # 10 Well-Spaced Shimmering Floating Water-Orb Events (Orb 8 spread cleanly to (6,12), distinct blue/teal vs pink Shard #4!)
    orb_pts = [(8, 10), (18, 9), (27, 11), (12, 15), (21, 16), (23, 22), (16, 25), (6, 12), (6, 16), (29, 22)]
    for idx, (ox, oy) in enumerate(orb_pts, 1):
        E.append({
            'type': 'event', 'name': f'Floating Water Orb {idx}', 'at': [ox, oy],
            'pages': [{'graphic': {'tile': P1('cv_xsea' if idx % 2 else 'cv_xblue')}, 'trigger': 'action',
                       'commands': ['A slow sphere of River Ebb water hangs mid-air here, cold to the touch. Tiny silver fish wheel lazily inside it.']}]
        })

    # Rich undergrowth, Bleed frost-shimmer accents around cottages, ferns & deep lifted river pools!
    rng2 = random.Random(5888)
    ev_set = {tuple(e['at']) for e in E}
    m.paint()

    bleeds = [P1('lm_bleed0'), P1('lm_bleed1'), P1('lm_bleed2')]
    ferns = [P1('nt_fern0'), P1('nt_fern1'), P1('gr_clover0'), P1('gr_clover1'), P1('gr_tuft0'), P1('gr_tuft1'), P1('gr_tuft2')]
    v_w = RC.vauto('rejuvenation', 'Still water', 0)
    v_W = RC.vauto('rejuvenation', 'Sea deep', 0)
    v_d = RC.vauto('pf', 'Gravel Spring', 0)
    v_u = RC.vauto('rejuvenation', 'DirtDark', 0)
    pad_w = np.pad(m.cls == 'w', 1, constant_values=False)
    # Subtle frost-bleed ground accents right around the 3 snow-roofed cottages so the winter roofs read surreal & intentional!
    cottage_aprons = {(x, y) for (x0, y0, x1, y1) in ((10, 6, 18, 14), (21, 7, 28, 14), (11, 17, 20, 25))
                      for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)}
    for y in range(H):
        for x in range(W):
            if m.L[1, y, x] == 0 and m.L[2, y, x] == 0 and m.cls[y, x] in ('.', 'g'):
                if (x, y) not in ev_set:
                    if (x, y) in cottage_aprons and rng2.random() < 0.78:
                        m.L[1, y, x] = bleeds[(x * 3 + y * 5) % 3]
                    elif rng2.random() < 0.72:
                        m.L[1, y, x] = bleeds[(x * 3 + y * 5) % 3] if rng2.random() < 0.28 else rng2.choice(ferns)
            # Layer deep river current & suspended mist shimmer ONLY over the lifted river pools!
            if m.cls[y, x] == 'w':
                if pad_w[y, x + 1] and pad_w[y + 2, x + 1] and pad_w[y + 1, x] and pad_w[y + 1, x + 2]:
                    m.L[1, y, x] = v_W
                if m.L[2, y, x] == 0 and rng2.random() < 0.42:
                    m.L[2, y, x] = P1(f'lm_veil{(x + y) % 3}')

    # Re-enforce clean single-layer autotile separation on L0/L1 (same fix as wallshadow_row.py!)
    for y in range(H):
        for x in range(W):
            t0 = int(m.L[0, y, x])
            if v_W <= t0 < v_W + 48:
                m.L[0, y, x] = v_w
            elif (v_d <= t0 < v_d + 48) or (v_u <= t0 < v_u + 48):
                m.L[0, y, x] = K.SH_GRASS[y % 2][x % 2]
            t1 = int(m.L[1, y, x])
            if v_w <= t1 < v_w + 48:
                m.L[1, y, x] = 0

    head = {
        'id': 588,
        'name': 'Ebb Hollow',
        'parent': 580,
        'bgm': 'Underwater',
        'field': 'BLEED',
        'rubric': True,
        'map_audio': {'bgm': 'Mood - Mystery', 'bgs': 'Glassfall Bleed', 'bgs_volume': 70},
        'metadata': {'Name': 'Ebb Hollow', 'Outdoor': True, 'ShowArea': True,
                     'MapPosition': [0, 4, 8], 'BattleBack': 'water'},
        'tone': [-18, -12, 22, 36],
        'fog': {'name': 'prismfall_seamist', 'opacity': 48, 'blend': 0, 'zoom': 100, 'sx': 1, 'sy': 0},
        '_file': '588_ebb_hollow.yaml',
    }
    return write_raw_map(m, 588, TID60, head,
                         '# GENERATED by mapgen/layouts/act1_frontier_dungeons.py: Ebb Hollow (Holmsby).\n',
                         start=(32, 15))


# ==============================================================================
# MAP 5: 591 Brassfall Pokémon Center (15x11, TS 34, template pokecenter)
# ==============================================================================
CREAM_STONE = [[5920, 5921, 5922], [5928, 5929, 5930], [5936, 5937, 5938]]
ALPINE_SLATE = [[1152, 1153, 1154], [1160, 1161, 1162], [1168, 1169, 1170]]
RED_CARPET = [[7172, 7173, 7174], [7180, 7181, 7182], [7188, 7189, 7190]]
POKEBALL_MEDAL_5X4 = [
    [536, 537, 538, 539, 540],
    [544, 545, 546, 547, 548],
    [552, 553, 554, 555, 556],
    [560, 561, 562, 563, 564],
]


def _put_tf34(L, name, x, y):
    rows, top = TF[name]
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


def _seam_brassfall_ts34(L, floor, wall_rows=2):
    """Warm Brassfall alpine timber & stone walling with dark charcoal void casing (5533..5562)."""
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
                L[0, y, x] = 1161  # Alpine slate base
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
    """Emit explicit tiles: entries (100% exact L0 + all non-zero L1/L2) matching 241_cindervault_pc.yaml."""
    _, H, W = L.shape
    out = []
    for z in range(3):
        for y in range(H):
            for x in range(W):
                t = int(L[z, y, x])
                if z == 0 or t != 0:
                    out.append({'tile': t, 'at': [x, y], 'layer': z})
    return out


def build_591():
    """Brassfall Pokémon Center (15x11, TS 34) — Gold-Standard Symmetrical Alpine Timber U-Counter:
    - Uses `biome: interior` + `palette: interior` + `take_events` (exact 241/121 pattern!) so:
        * Unbroken symmetrical 5-wide warm alpine timber U-counter at x=5..9, y=2..3 (ALL 0x8f counter flags!),
          aligned dead-center above the 5x4 Pokéball medallion (x=5..9, y=4..7)!
        * Sleek healing pod (6035..6044) nestled cleanly inside left bay (6..7, 1..2) -> Healing balls (id=4) at [7, 2]!
        * Nurse Joy (NPC 16, id=2) at [8, 2] behind 0x8f counter pad (8, 3) -> turns LEFT directly into [7, 2] pod!
        * Giant green scoreboard REMOVED completely; north timber wall framed by twin frosted alpine windows!
        * Clean 1-tile breather at x=10, floor-standing PC at [11, 2] (L2 5847 / L1 5855), wall Town Map at [12, 1]!
        * Plush burgundy exit carpet runs cleanly into [7, 10] doorway (jarring white 444 stripe REMOVED!).
        * ZERO non-Nurse NPCs use NPC 16!
    """
    W, H = 15, 11
    L = np.zeros((3, H, W), dtype=np.int32)
    floor = np.zeros((H, W), dtype=bool)
    floor[2:9, 1:14] = True     # Main cozy alpine hall (x=1..13, y=2..8)
    floor[8, 1] = False         # SW chamfer
    floor[8, 13] = False        # SE chamfer
    floor[9, 5:10] = True       # Stepped foyer vestibule (x=5..9, y=9)
    floor[10, 6:9] = True       # Recessed entry notch (x=6..8, y=10; Exit @ [7,10]!)

    _seam_brassfall_ts34(L, floor, wall_rows=2)

    # Multi-zone Brassfall Center flooring: warm alpine slate wings + cream-stone central heart + 5x4 Pokeball medallion!
    _put_9slice34(L, ALPINE_SLATE, 1, 2, 3, 8, z=0, mask=floor)
    _put_9slice34(L, ALPINE_SLATE, 11, 2, 13, 8, z=0, mask=floor)
    _put_9slice34(L, CREAM_STONE, 4, 2, 10, 8, z=0, mask=floor)
    _put_9slice34(L, CREAM_STONE, 5, 9, 9, 9, z=0, mask=floor)
    _put_9slice34(L, CREAM_STONE, 6, 10, 8, 10, z=0, mask=floor)
    _put_grid34(L, POKEBALL_MEDAL_5X4, 5, 4, z_rows=(0, 0, 0, 0))
    # Plush crimson welcome runner flowing cleanly into Exit [7,10] (NO jarring white 444 stripe!)
    _put_9slice34(L, RED_CARPET, 6, 9, 8, 10, z=1)

    # North wall architectural details (y=0..1): clean warm alpine timber framed by twin frosted alpine windows!
    _put_grid34(L, [[2086, 2087], [2094, 2095]], 2, 0, z_rows=(1, 1))   # West frosted alpine window
    _put_grid34(L, [[2086, 2087], [2094, 2095]], 8, 0, z_rows=(1, 1))   # Center-east frosted alpine window
    # Floor-standing PC terminal at (11, 1..2) (matching 241!) & wall-mounted Town Map high at (12..13, 0..1) -> ZERO crowding!
    L[2, 1, 11] = 5847
    L[1, 2, 11] = 5855                                                   # PC @(11,2); (10,2) & (11,3) open!
    _put_grid34(L, [[4730, 4731], [4738, 4739]], 12, 0, z_rows=(1, 1))   # Town Map @(12,1); (12,2) open!

    # Unbroken, symmetrical 5-wide warm alpine timber U-counter (exact 121 Briarwick tiles, ALL 0x8f!) at x=5..9, y=2..3!
    L[1, 2, 5] = 5952   # Curved timber left return + potted plant (0x8f)
    L[1, 2, 9] = 5955   # Curved timber right return + potted plant (0x8f)
    for dx, t in enumerate((5960, 5961, 5962, 5961, 5963)):
        L[1, 3, 5 + dx] = t  # Unbroken rounded front counter (ALL 0x8f; service pads at (6,3) and (8,3)!)
    # Sleek silver-purple healing pod nestled cleanly inside left bay (6..7, 1..2) -> Healing balls (id=4) at (7,2)!
    L[2, 1, 6] = 6035; L[2, 1, 7] = 6036
    L[1, 2, 6] = 6043; L[1, 2, 7] = 6044

    # West Wing: Warm Cast-Iron Woodstove + Cozy Lounge Sofa + Gale Post Desk (Juno's Letter!)
    L[2, 2, 1] = 2470; L[1, 3, 1] = 2478                                 # Crackling cast-iron woodstove with kettle
    _put_grid34(L, [[6024, 6026], [6032, 6034]], 2, 3, z_rows=(2, 1))    # Cozy lounge sofa (2..3, 3..4) with 1-tile headroom above Clerk!
    _put_grid34(L, [[3466, 3467], [3474, 3475]], 1, 6, z_rows=(1, 1))    # Gale Post timber mail desk (1..2, 6..7)
    L[2, 6, 1] = 3428                                                    # Open Gale Post mail ledger
    L[2, 6, 2] = 4528                                                    # Parcel dispatch kit

    # East Wing: Parlor Ficus, Supply Mart Shelf & Warm Brass Lamp
    L[2, 2, 13] = 7126; L[1, 3, 13] = 7134                               # Tall potted ficus (cleanly clear of Town Map (12,2)!)
    _put_grid34(L, [[2750, 2751], [2758, 2759], [2766, 2767]], 12, 4, z_rows=(2, 2, 1))  # Supply shelf (12..13, 4..6)
    L[2, 7, 12] = 2247; L[1, 8, 12] = 2255                               # Warm brass floor lamp cleanly clear of shelf!
    # Vestibule stools & low planter
    L[1, 9, 5] = 4077
    L[1, 9, 9] = 4077
    L[1, 8, 2] = 7177

    # Verify every front & wing counter tile carries exact 0x8f counter flag!
    ts34 = R.tilesets()[TID34]
    for cx, cy in ((5, 2), (9, 2), (5, 3), (6, 3), (7, 3), (8, 3), (9, 3)):
        t = int(L[1, cy, cx])
        assert ts34['passages'][t] == 0x8f, f'591 counter ({cx},{cy}) tile {t} pas={hex(ts34["passages"][t])} != 0x8f!'

    # Canonical Events (ZERO non-Nurse NPCs use NPC 16!)
    events = [
        {'type': 'exit', 'at': [7, 10], 'link': 'T590_PC'},
        # Gale Post Desk Clerk (NPC 14 — NEVER NPC 16!): Juno's green-ink letter (V125 0 -> 1, story/24_SCRIPT_CH5.md:125-136)
        {'type': 'event', 'name': 'Gale Post Clerk', 'at': [3, 6], 'pages': [
            {'graphic': {'sprite': 'NPC 14', 'dir': 'right'}, 'trigger': 'action', 'commands': [
                'Gale Post Clerk: Gale Post Express! A letter arrived from Elowen with your name on it — green ink, and three exclamation marks on the envelope.',
                '"\\PN!!! Uncle Rowan was invited to Meridian\'s gala in Lumen (the TENTH YEAR OF LIGHT, with AIRSHIPS) and he\'s got Warden business, again, so he gave me his invitation and said, \'Go and eat their little cakes for me, Juno. All of them.\'"',
                '"He\'s never once missed a chance to tell Meridian what he thinks of them. I think he\'s being nice to me. He\'s been very nice to me lately. It\'s a bit worrying."',
                '"I\'m coming down the Prism Falls road. Meet me at the Four Ways on the Crown Road? It\'s the inn with the signpost that points at four kingdoms. You can\'t miss it. FOUR KINGDOMS. — Juno"',
                '"P.S. The Spewpa evolved. It\'s a Vivillon now, and it\'s still rude."',
                {'if': '$game_variables[125] < 1', 'then': [
                    {'var': ['CH5_STEP', 1]},
                    {'script': 'pfm_quest(:ch5_eighteen_roads, "Eighteen Roads", "Meet Juno at the Four Ways on Wallshadow Row, then go on to Lumen.")'},
                ], 'else': []},
                {'selfswitch': ['A', True]},
            ]},
            {'cond': {'self': 'A'}, 'graphic': {'sprite': 'NPC 14', 'dir': 'right'}, 'trigger': 'action', 'commands': [
                'Gale Post Clerk: No fresh mail from Elowen yet. The Four Ways inn is east over the Icefall Locks and along Coppice Ride!'
            ]},
        ]},
        # Brassfall Pokémon Center Supply Clerk (NPC 19 — NEVER NPC 16!)
        {'type': 'mart', 'name': 'Center Supply Clerk', 'at': [11, 6], 'sprite': 'NPC 19', 'dir': 'left',
         'greeting': 'Supply Clerk: Meridian\'s company store outside only takes scrip, so the League Center keeps real coin supplies right here. What do you need?',
         'items': ['POKEBALL', 'GREATBALL', 'NETBALL', 'SUPERPOTION', 'HYPERPOTION',
                   'ANTIDOTE', 'PARALYZEHEAL', 'ICEHEAL', 'SUPERREPEL', 'ESCAPEROPE']},
        # Local Brassfall Traveler (NPC 20 — NEVER NPC 16!)
        _npc((4, 8), 'Lock Road Traveler', 'NPC 20', [
            'Traveler: Climbing the Icefall Locks on foot is a haul, friend. If you\'ve got an Electric-type — or a spare Cell Battery from the old Sluiceworks — the lift-boy outside can wake the frozen Ice Elevator!',
            'Traveler: And keep warm by the stove. Isenmar frost doesn\'t let go till you crest the top lock into Elowen.'
        ], d='up'),
    ]

    take_events = [
        {'template': 'pokecenter', 'name': 'Nurse', 'at': [8, 2]},
        {'template': 'pokecenter', 'name': 'Healing balls', 'at': [7, 2]},
        {'template': 'pokecenter', 'name': 'PC', 'at': [11, 2]},
        {'template': 'pokecenter', 'name': 'Town Map, size(2,1)', 'at': [12, 1]},
    ]

    ev_pts = [(7, 10), (7, 9), (8, 4), (8, 2), (7, 2), (11, 3), (11, 2), (12, 2), (3, 6), (11, 6), (4, 8)]
    PG.guard(L, TID34, ev_pts, 'map 591')
    hits = PG.hits(L, ts34, ev_pts)
    assert not hits, f'map 591: passguard hits {hits}'

    # Strict 4-bit BFS verification on 591's exact tile array!
    verify_4bit_bfs(
        L, TID34, events,
        start=(7, 9),
        targets=[
            ('Exit', (7, 10), False),
            ('Nurse heal spot (across 0x8f counter)', (8, 4), False),
            ('PC stand spot', (11, 3), False),
            ('Town Map stand spot', (12, 2), False),
            ('Gale Post Clerk', (3, 6), True),
            ('Supply Clerk', (11, 6), True),
            ('Traveler', (4, 8), True),
        ],
        label='Map 591 Brassfall Pokémon Center',
    )

    os.makedirs(RAW_DIR, exist_ok=True)
    np.save(os.path.join(RAW_DIR, '591.npy'), L)

    spec = {
        'id': 591,
        'name': 'Brassfall Pokémon Center',
        'parent': 590,
        'bgm': 'Poke Center',
        'map_audio': {'bgs': ''},
        'tone': [6, 2, -6, 0],
        'metadata': {
            'ShowArea': False,
            'HealingSpot': BRASSFALL_HEAL_SPOT,
            'MapPosition': [0, 7, 7],
        },
        'biome': 'interior',
        'palette': 'interior',
        'tileset': TID34,
        'map': '\n'.join(['.' * W] * H) + '\n',
        'tiles': _tiles_list_34(L),
        'events': events,
        'take_events': take_events,
    }
    comment = '# GENERATED by mapgen/layouts/act1_frontier_dungeons.py: Brassfall Pokémon Center (15x11, TS 34).\n'
    body = yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True)
    with open(os.path.join(SPEC_DIR, '591_brassfall_pc.yaml'), 'w', encoding='utf-8') as f:
        f.write(comment + body)
    print(f'Wrote 591 Brassfall Pokémon Center        15x11 ts=34 events={len(events)} (+4 take_events: Nurse/Balls/PC/Map)')
    return L


def main():
    build_565()
    build_584()
    build_585()
    build_588()
    build_591()


if __name__ == '__main__':
    main()
