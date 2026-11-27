#!/usr/bin/env python3
"""layouts/duneholt_interiors.py — Batch 3A: Duneholt Core Interior & Dungeon Maps (6 Maps):
  - 201 Duneholt Pokémon Center               (15x11, TS 34 Prismfall Interior — 591 9.4/10 Gold Standard!)
  - 202 Duneholt Mart                         (12x10, TS 34 Prismfall Interior — 242 Gold Standard!)
  - 206 Elector's Palace - Hall of Audience   (29x25, TS 59 PF Rejuv Manor — Grand Sandstone/Crimson Palace)
  - 207 Elector's Palace - Mural Gallery      (41x15, TS 59 PF Rejuv Manor — Illuminated Historical Murals)
  - 208 Necropolis of the Electors            (44x40, TS 57 PF Rejuv Cave  — Petra-Style Sandstone Catacombs)
  - 209 Sahar's Dig Lab                       (21x15, TS 34 Prismfall Interior — Paleontology & Fossil Revival)

Canon sources:
  - design/maps.json (exact sizes, features, MapPosition [0,17,3])
  - story/25_SCRIPT_CH6.md (Larch Gale Post #5 KELP TEA BAG, Sahar's first meeting & Warning 1,
    Mural Gallery lore, Tomb-keeper, Kassan's throne)
  - pbs/trainers.txt (# Map 208: CHANNELER Zenobia, RUINMANIAC Lucan — verified 0 duplicates!)
  - plugins/Prismfall Trials (pf_trial_board(:OSSARIA), pf_trial_talk(:SAHAR_DIGLAB))

Run:
    /usr/bin/python3 mapgen/layouts/duneholt_interiors.py
"""
import os
import sys
from collections import deque
import numpy as np
import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cavekit import Cave, FLOOR, TER, MASS, P1
import cavekit as CK
import rkit as K
from rkit import STAMPS
import rcompose as RC
import render as R
import passguard as PG
from interiorkit import TF
from verdance_palace import Palace

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TID_INT = 34
TID_CAVE = 57
TID_MANOR = 59
VOID34 = 5437
DUN_POS = [0, 17, 3]
# PC door in Map 200 is lb_pc at (4,16) + door [5,5] = (9,21) -> HealingSpot steps onto (9,22)
DUNEHOLT_HEAL_SPOT = [200, 9, 22]


# =================================================================================================
# Shared Helpers (TS 34 Terracotta/Sandstone Primitives + 4-bit Directional BFS Verification)
# =================================================================================================
def _guarded_unbuilt_transfer(map_id, tx, ty, direction, blocked_text):
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


def _verify_4bit_bfs(L, tid, events, start, targets, label):
    """Strict Essentials 4-bit directional BFS + passguard check on any interior/dungeon map."""
    import build as B
    ts = R.tilesets()[tid]
    H, W = L.shape[1:]
    solid_ev = set()
    for e in events:
        if e.get('type') in ('npc', 'trainer', 'mart'):
            solid_ev.add(tuple(e['at']))
        elif e.get('type') == 'event':
            pg0 = (e.get('pages') or [{}])[0]
            if (pg0.get('graphic') or {}).get('sprite') and not pg0.get('through'):
                solid_ev.add(tuple(e['at']))
    ok = np.array([[B.cell_passable(L, ts, x, y) and (x, y) not in solid_ev for x in range(W)] for y in range(H)])

    def edge_ok(x, y, d):
        bit = 1 << (d // 2 - 1)
        for z in (2, 1, 0):
            t = int(L[z, y, x])
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
    assert ok[sy, sx], f'{label}: BFS start {start} is NOT passable!'
    seen = {start}
    q = deque([start])
    while q:
        cx, cy = q.popleft()
        for dx, dy, d in ((0, 1, 2), (0, -1, 8), (1, 0, 6), (-1, 0, 4)):
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < W and 0 <= ny < H and (nx, ny) not in seen and ok[ny, nx]:
                if edge_ok(cx, cy, d) and edge_ok(nx, ny, 10 - d):
                    seen.add((nx, ny))
                    q.append((nx, ny))
    missing = []
    for name, (tx, ty), adj in targets:
        if adj:
            reach = (tx, ty) in seen or any((tx + dx, ty + dy) in seen for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)))
        else:
            reach = (tx, ty) in seen
        if not reach:
            missing.append((name, (tx, ty), bool(B.cell_passable(L, ts, tx, ty))))
    print(f'{label} BFS: {len(seen)} walkable cells reached from {start}; missing={missing}')
    assert not missing, f'{label} unreachable targets: {missing}'
    return seen


def _add_safe_overlay(Lr, tid, stamp_name, pts):
    """Stamp overhead light/glow (pf_glow / cv_shaft) strictly onto unoccupied L[2] cells — NEVER overwrites chandeliers or braziers!"""
    H, W = Lr.shape[1:]
    ov = RC.resolve(np.array(STAMPS[stamp_name]['layers'], dtype=np.int32), tid)
    oh, ow = ov.shape[1], ov.shape[2]
    for ox, oy in pts:
        for dy in range(oh):
            for dx in range(ow):
                t = int(ov[2, dy, dx] or ov[1, dy, dx] or ov[0, dy, dx])
                xx, yy = ox + dx, oy + dy
                if t and 0 <= xx < W and 0 <= yy < H and int(Lr[2, yy, xx]) == 0:
                    Lr[2, yy, xx] = t


def _verify_all_events_and_trainers(Lr, tid, events, start, label):
    """Exhaustively verify EVERY event (touch warps W0-reachable, action events adjacent-reachable) AND full trainer sightlines!"""
    import build as B
    ts = R.tilesets()[tid]
    H, W = Lr.shape[1:]
    solid_ev = set()
    for e in events:
        if e.get('type') in ('npc', 'trainer', 'mart'):
            solid_ev.add(tuple(e['at']))
        elif e.get('type') == 'event':
            pg0 = (e.get('pages') or [{}])[0]
            if (pg0.get('graphic') or {}).get('sprite') and not pg0.get('through'):
                solid_ev.add(tuple(e['at']))
    ok = np.array([[B.cell_passable(Lr, ts, x, y) and (x, y) not in solid_ev for x in range(W)] for y in range(H)])

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

    # Full 4-bit BFS (including Essentials 0x80 counter-talk across counter tiles!)
    seen = _verify_4bit_bfs(Lr, tid, events, start, [], label + ' [BASE]')
    missing = []
    for e in events:
        at = tuple(e['at'])
        et = e.get('type')
        is_touch = et in ('exit', 'warp')
        if et == 'event':
            pg0 = (e.get('pages') or [{}])[0]
            if pg0.get('trigger') == 'touch':
                is_touch = True
            if pg0.get('trigger') == 'autorun':
                continue
        if is_touch:
            assert B.cell_passable(Lr, ts, at[0], at[1]), f'{label}: touch/warp event {e.get("name")} at {at} sits on SOLID tile!'
            reach = at in seen
        else:
            reach = at in seen or any((at[0] + dx, at[1] + dy) in seen for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)))
            if not reach:
                # Check Essentials 0x80 counter flag on orthogonal neighbor leading to a reachable player cell!
                for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                    mx, my = at[0] + dx, at[1] + dy
                    px, py = at[0] + 2 * dx, at[1] + 2 * dy
                    if 0 <= mx < W and 0 <= my < H and (px, py) in seen:
                        has_counter = any((int(Lr[z, my, mx]) > 0 and (ts['passages'][int(Lr[z, my, mx])] & 0x80)) for z in (0, 1, 2))
                        if has_counter:
                            reach = True
                            break
        if not reach:
            missing.append((e.get('name') or et, at, bool(B.cell_passable(Lr, ts, at[0], at[1]))))
    print(f'{label} [ALL-EVENTS]: {len(events)} events verified; missing={missing}')
    assert not missing, f'{label} unreachable events: {missing}'

    # Verify trainer sightlines (full cardinal range must be unobstructed W0 tiles!)
    dmap = {'down': (0, 1, 2), 'left': (-1, 0, 4), 'right': (1, 0, 6), 'up': (0, -1, 8)}
    for e in events:
        if e.get('type') != 'trainer':
            continue
        tx, ty = e['at']
        sight = int(e.get('sight', 0))
        dx, dy, d = dmap[e.get('dir', 'down')]
        cx, cy = tx, ty
        for step in range(1, sight + 1):
            nx, ny = cx + dx, cy + dy
            assert 0 <= nx < W and 0 <= ny < H, f'{label}: trainer {e.get("trainer")} sight step {step} OOB!'
            assert ok[ny, nx], f'{label}: trainer {e.get("trainer")} sight step {step} {(nx, ny)} BLOCKED!'
            assert edge_ok(cx, cy, d) and edge_ok(nx, ny, 10 - d), f'{label}: trainer {e.get("trainer")} edge blocked at step {step} {(cx,cy)}->{(nx,ny)}!'
            cx, cy = nx, ny
        print(f'{label}: Trainer {e.get("trainer")} at {(tx, ty)} dir={e.get("dir")} sight={sight} -> 100% OPEN!')
    return seen



# ---- TS 34 Warm Sandstone & Terracotta Floor/Wall/Furniture Kits ----
CREAM_SANDSTONE = [
    [5920, 5921, 5922],
    [5928, 5929, 5930],
    [5936, 5937, 5938],
]
HONEY_PARQUET = [
    [1067, 1068, 1069],
    [1067, 1068, 1069],
    [1067, 1068, 1069],
]
OCHRE_TILE = [
    [1058, 1059, 1060],
    [1066, 1067, 1068],
    [1074, 1075, 1076],
]
CRIMSON_CARPET = [
    [7172, 7173, 7174],
    [7180, 7181, 7182],
    [7188, 7189, 7190],
]
BROWN_WOVEN_RUG = [
    [8620, 8621, 8622],
    [8628, 8629, 8630],
    [8636, 8637, 8638],
]
SHER_WOVEN_RUG = [
    [5411, 5412, 5413],
    [5419, 5420, 5421],
    [5427, 5428, 5429],
]
POKEBALL_MEDAL_5X4 = [
    [536, 537, 538, 539, 540],
    [544, 545, 546, 547, 548],
    [552, 553, 554, 555, 556],
    [560, 561, 562, 563, 564],
]
HERB_RACK = [[5422], [5430], [5438]]
CHALKBOARD = [[3276, 3277, 3278]]
TAPESTRY_GOLD = [[5531, 5532], [5539, 5540]]
SUN_WINDOW = [[2086, 2087], [2094, 2095]]
HOTEL_WINDOW = [[7124, 7125], [7132, 7133]]
GEO_MAP = [[4730, 4731], [4738, 4739]]
HOTEL_VASE = [[7558], [7566]]


def _put_tf(L, name, x, y):
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


def _put_grid(L, grid, x, y, z_rows=None):
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


def _put_9slice(L, tiles9, x0, y0, x1, y1, z=0, mask=None):
    H, W = L.shape[1:]
    for y in range(max(0, y0), min(H, y1 + 1)):
        ry = 0 if y == y0 else (2 if y == y1 else 1)
        for x in range(max(0, x0), min(W, x1 + 1)):
            if mask is not None and not mask[y, x]:
                continue
            rx = 0 if x == x0 else (2 if x == x1 else 1)
            L[z, y, x] = tiles9[ry][rx]


def _doormat(L, cx, y):
    H, W = L.shape[1:]
    for i, x in enumerate((cx - 1, cx, cx + 1)):
        if 0 <= y < H and 0 <= x < W:
            L[1, y, x] = 5512 + i


def _seam_terracotta_room(L, floor, wall_style='terracotta'):
    """Auto-seam a warm Ossaria sandstone/terracotta interior on TS 34 with crisp dark void casing."""
    H, W = floor.shape
    L[0, :, :] = VOID34
    wall_face = np.zeros((H, W), dtype=bool)
    for y in range(2, H):
        for x in range(1, W - 1):
            if floor[y, x] and not floor[y - 1, x]:
                wall_face[y - 1, x] = True
                wall_face[y - 2, x] = True
    interior = floor | wall_face
    for y in range(H):
        for x in range(W):
            if floor[y, x]:
                L[0, y, x] = 5929  # Warm cream-sandstone base
            elif wall_face[y, x]:
                is_lower = (y + 1 < H and floor[y + 1, x])
                left_end = (x == 0) or not wall_face[y, x - 1]
                right_end = (x + 1 >= W) or not wall_face[y, x + 1]
                if wall_style == 'terracotta':
                    # Warm ochre-terracotta plaster walls over mahogany dado (6283..6285 / 6291..6293, ALL 0xf!)
                    if is_lower:
                        L[0, y, x] = 6291 if left_end else (6293 if right_end else 6292)
                    else:
                        L[0, y, x] = 6283 if left_end else (6285 if right_end else 6284)
                else:
                    # Warm cedar/mahogany canyon-timber walls (5547/5555)
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
# 1. MAP 201 — DUNEHOLT POKÉMON CENTER (15x11, TS 34 — Exact 591 9.4/10 Gold Standard!)
# =================================================================================================
def build_201():
    W, H = 15, 11
    L = np.zeros((3, H, W), dtype=np.int32)
    floor = np.zeros((H, W), dtype=bool)
    floor[2:9, 1:14] = True
    floor[8, 1] = False
    floor[8, 13] = False
    floor[9, 5:10] = True
    floor[10, 6:9] = True

    _seam_terracotta_room(L, floor, wall_style='terracotta')

    # Warm Ossaria Sandstone & Honey Parquet Flooring + Centered 5x4 Pokéball Medallion!
    _put_9slice(L, HONEY_PARQUET, 1, 2, 3, 8, z=0, mask=floor)
    _put_9slice(L, HONEY_PARQUET, 11, 2, 13, 8, z=0, mask=floor)
    _put_9slice(L, CREAM_SANDSTONE, 4, 2, 10, 8, z=0, mask=floor)
    _put_9slice(L, CREAM_SANDSTONE, 5, 9, 9, 9, z=0, mask=floor)
    _put_9slice(L, CREAM_SANDSTONE, 6, 10, 8, 10, z=0, mask=floor)
    _put_grid(L, POKEBALL_MEDAL_5X4, 5, 4, z_rows=(0, 0, 0, 0))
    # Plush crimson welcome runner flowing cleanly into Exit [7,10] (ZERO white 444 stripe!)
    _put_9slice(L, CRIMSON_CARPET, 6, 9, 8, 10, z=1)

    # North wall architectural accents (symmetrical warm terracotta curtains — ZERO void overhang!)
    _put_grid(L, HOTEL_WINDOW, 2, 0, z_rows=(1, 1))
    _put_grid(L, HOTEL_WINDOW, 9, 0, z_rows=(1, 1))
    # Floor-standing PC at [11,2] (1-tile breather x=10!) & Wall Town Map high at [12,1]
    L[2, 1, 11] = 5847
    L[1, 2, 11] = 5855
    _put_grid(L, GEO_MAP, 12, 0, z_rows=(1, 1))

    # Symmetrical Unbroken 5-Wide Warm Terracotta U-Counter (x=5..9, y=2..3 — 100% 0x8f!)
    L[1, 2, 5] = 5952
    L[1, 2, 9] = 5955
    for dx, t in enumerate((5960, 5961, 5962, 5961, 5963)):
        L[1, 3, 5 + dx] = t
    # Healing pod nestled cleanly inside left bay (6..7, 1..2) -> Healing balls at [7,2], Nurse Joy (NPC 16) at [8,2]!
    L[2, 1, 6] = 6035
    L[2, 1, 7] = 6036
    L[1, 2, 6] = 6043
    L[1, 2, 7] = 6044

    # West Desert Lounge & Gale Post Corner (Larch's Lecture Six + Kelp Tea Bag #5!)
    _put_grid(L, HOTEL_VASE, 1, 2, z_rows=(2, 1))
    _put_grid(L, [[6024, 6026], [6032, 6034]], 2, 3, z_rows=(2, 1))      # Desert lounge sofa (2..3, 3..4)
    _put_grid(L, [[3466, 3467], [3474, 3475]], 1, 6, z_rows=(1, 1))      # Gale Post mail desk (1..2, 6..7)
    L[2, 6, 1] = 3428                                                    # Open Gale Post ledger
    L[2, 6, 2] = 4528                                                    # Tea & bottled water kit

    # East Oasis Lounge Corner (potted ficus, warm mahogany bookcase, terracotta urn & carved wood lamp)
    L[2, 2, 13] = 7126
    L[1, 3, 13] = 7134
    _put_tf(L, 'bookcase', 12, 4)                                        # Warm Ossarian travel bookcase (12..13, 4..5)
    L[1, 6, 13] = 4101                                                   # Warm terracotta water urn
    L[2, 7, 12] = 2271                                                   # Carved desert wood lamp top
    L[1, 8, 12] = 2279                                                   # Carved desert wood lamp base
    L[1, 9, 5] = 4077
    L[1, 9, 9] = 4077
    L[1, 8, 2] = 7177

    # Programmatic assertion: 100% 0x8f counter flags on all 7 U-counter tiles!
    ts34 = R.tilesets()[TID_INT]
    for cx, cy in ((5, 2), (9, 2), (5, 3), (6, 3), (7, 3), (8, 3), (9, 3)):
        t = int(L[1, cy, cx])
        assert ts34['passages'][t] == 0x8f, f'201 counter ({cx},{cy}) tile {t} pas={hex(ts34["passages"][t])} != 0x8f!'

    # Canonical Events (NPC 16 used ONLY on Nurse Joy via take_events — ZERO non-Nurse NPC 16!)
    events = [
        {'type': 'exit', 'at': [7, 10], 'link': 'DH_PC', 'arrive': [7, 10, 'up']},
        # Gale Post Clerk (NPC 14 — story/25_SCRIPT_CH6.md:215 Larch Lecture Six & KELP TEA BAG #5!)
        {'type': 'event', 'name': 'Gale Post Clerk', 'at': [3, 6], 'pages': [
            {'graphic': {'sprite': 'NPC 14', 'dir': 'right'}, 'trigger': 'action', 'commands': [
                'Gale Post Clerk: Gale Post — Duneholt Branch! You have a letter from Tidewatch Station, sealed with grey wax.',
                '"Duneholt: drink water. Not their water. Bottled. Lecture Six is being written in the dark because the Mandate has rationed my lamp-oil. — I.L."',
                {'script': 'pfm_item(:KELPTEABAG, 1, "Kelp Tea Bag") rescue nil'},
                'Five.',
                {'selfswitch': ['A', True]},
            ]},
            {'cond': {'self': 'A'}, 'graphic': {'sprite': 'NPC 14', 'dir': 'right'}, 'trigger': 'action', 'commands': [
                'Gale Post Clerk: No fresh dispatches from Elowen or Lumen yet. Keep hydrated out on the terraces — bottled water only!'
            ]},
        ]},
        _make_npc('Caravan Traveler', (10, 6), 'NPC 20', 'left', [
            "Traveler: If you're bound for the Necropolis of the Electors up on the northeast terrace, pack Dusk Balls and Escape Ropes from the Mart.",
            "Traveler: And stop by Sahar's Dig Lab on the northwest terrace — she knows every bone under Ossaria.",
        ]),
        _make_npc('Desert Scout', (4, 8), 'NPC 18', 'up', [
            "Scout: The Center's water cistern is filtered through three feet of canyon limestone. Best cup in Duneholt, and it doesn't cost a bone.",
        ]),
    ]
    take_events = [
        {'template': 'pokecenter', 'name': 'Nurse', 'at': [8, 2]},
        {'template': 'pokecenter', 'name': 'Healing balls', 'at': [7, 2]},
        {'template': 'pokecenter', 'name': 'PC', 'at': [11, 2]},
        {'template': 'pokecenter', 'name': 'Town Map, size(2,1)', 'at': [12, 1]},
    ]

    ev_pts = [(7, 10), (7, 9), (8, 4), (8, 2), (7, 2), (11, 3), (11, 2), (12, 2), (3, 6), (10, 6), (4, 8)]
    PG.guard(L, TID_INT, ev_pts, 'Map 201')
    assert not PG.hits(L, ts34, ev_pts), 'Map 201 passguard hits!'
    _verify_4bit_bfs(L, TID_INT, events, (7, 9), [
        ('Exit', (7, 10), False),
        ('Nurse Counter (0x8f)', (8, 4), False),
        ('PC Terminal', (11, 3), False),
        ('Town Map', (12, 2), False),
        ('Gale Post Clerk', (3, 6), True),
        ('Caravan Traveler', (10, 6), True),
        ('Desert Scout', (4, 8), True),
    ], 'Map 201 Duneholt PC')

    np.save(os.path.join(HERE, 'data', 'raw', '201.npy'), L.astype(np.int16))
    spec = {
        'id': 201,
        'name': 'Duneholt Pokémon Center',
        'parent': 200,
        'bgm': 'Poke Center',
        'map_audio': {'bgs': ''},
        'tone': [10, 4, -6, 2],
        'metadata': {
            'ShowArea': False,
            'HealingSpot': DUNEHOLT_HEAL_SPOT,
            'MapPosition': DUN_POS,
        },
        'biome': 'interior',
        'palette': 'interior',
        'tileset': TID_INT,
        'map': '\n'.join(['.' * W] * H) + '\n',
        'tiles': _tiles_list_34(L),
        'events': events,
        'take_events': take_events,
    }
    with open(os.path.join(HERE, 'specs', '201_duneholt_pc.yaml'), 'w', encoding='utf-8') as f:
        f.write('# GENERATED by mapgen/layouts/duneholt_interiors.py (Batch 3A): Duneholt Pokémon Center.\n')
        f.write(yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))
    print('Wrote specs/201_duneholt_pc.yaml and data/raw/201.npy')


# =================================================================================================
# 2. MAP 202 — DUNEHOLT MART (12x10, TS 34 — Exact 242 Gold Standard, 100% 0x8f Counter!)
# =================================================================================================
def build_202():
    W, H = 12, 10
    L = np.zeros((3, H, W), dtype=np.int32)
    floor = np.zeros((H, W), dtype=bool)
    floor[2:9, 1:11] = True
    floor[8, 1] = False
    floor[8, 10] = False
    floor[9, 4:7] = True

    _seam_terracotta_room(L, floor, wall_style='terracotta')
    _put_9slice(L, CREAM_SANDSTONE, 1, 2, 10, 8, z=0, mask=floor)
    _put_9slice(L, HONEY_PARQUET, 4, 2, 9, 7, z=0, mask=floor)
    _put_9slice(L, BROWN_WOVEN_RUG, 4, 4, 6, 7, z=1, mask=floor)
    _doormat(L, 5, 9)

    # North wall: cleanly spaced terracotta windows & framed Ossaria trade map (ZERO void overhang!)
    _put_grid(L, HOTEL_WINDOW, 1, 0, z_rows=(1, 1))
    _put_grid(L, HOTEL_WINDOW, 4, 0, z_rows=(1, 1))
    _put_grid(L, GEO_MAP, 7, 0, z_rows=(1, 1))

    # Clean Unobstructed Warm Terracotta Mart Counter wrapping Clerk at (2,3) — ALL 5 tiles 100% 0x8f!
    # Clean straight vertical counter (5971) at (3,2..3) — zero cyan bush in clerk talk-line!
    # Clean plain terracotta front (5962) flush into west wall at (1,4), single register mat (5961) at (2,4), corner (5963) at (3,4)!
    L[1, 2, 3] = 5971
    L[1, 3, 3] = 5971
    L[1, 4, 1] = 5962
    L[1, 4, 2] = 5961
    L[1, 4, 3] = 5963
    ts34 = R.tilesets()[TID_INT]
    for cx, cy in ((3, 2), (3, 3), (1, 4), (2, 4), (3, 4)):
        t = int(L[1, cy, cx])
        assert ts34['passages'][t] == 0x8f, f'202 counter ({cx},{cy}) tile {t} pas={hex(ts34["passages"][t])} != 0x8f!'

    # Grounded desert spice & expedition shelving, crates, terracotta urn & aisle-clear SE wood lamp!
    _put_tf(L, 'shelf_goods', 9, 2)                                      # Grounded cleanly on floor (9..10, 2..4)!
    _put_tf(L, 'shelf_bottles', 8, 5)                                    # Warm wooden spice/potion shelves (8..9, 5..6)
    _put_tf(L, 'crate_i', 1, 5)
    L[1, 7, 1] = 4101                                                    # Terracotta desert urn
    L[1, 7, 2] = 7177                                                    # Warm stone desert planter
    _put_grid(L, HERB_RACK, 10, 5, z_rows=(2, 1, 1))                     # Flush against east wall (10, 5..7)
    L[2, 7, 9] = 2271                                                    # Wood lamp tucked cleanly in SE corner (9, 7..8), aisle 100% open!
    L[1, 8, 9] = 2279

    events = [
        {'type': 'exit', 'at': [5, 9], 'link': 'DH_MART', 'arrive': [5, 9, 'up']},
        {
            'type': 'mart',
            'name': 'Mart Clerk',
            'at': [2, 3],
            'sprite': 'NPC 19',
            'dir': 'right',
            'greeting': 'Mart Clerk: Welcome to Duneholt Mart! Stock up on Ultra Balls, Dusk Balls, and Escape Ropes before braving the Bone Sands!',
            'items': [
                'POKEBALL', 'GREATBALL', 'ULTRABALL', 'DUSKBALL',
                'SUPERPOTION', 'HYPERPOTION', 'FULLHEAL', 'REVIVE',
                'ESCAPEROPE', 'SUPERREPEL',
            ],
        },
        _make_npc('Caravan Provisioner', (7, 6), 'NPC 18', 'right', [
            "Provisioner: Bone-traders out at Copperdune barter in fossils, so it's a relief to pay in honest League coin here.",
            "Provisioner: Grab a few Dusk Balls if you're heading into the Necropolis of the Electors — the rock-cut tombs stay pitch cool inside.",
        ]),
    ]

    ev_pts = [(5, 9), (5, 8), (4, 3), (2, 3), (7, 6)]
    PG.guard(L, TID_INT, ev_pts, 'Map 202')
    assert not PG.hits(L, ts34, ev_pts), 'Map 202 passguard hits!'
    _verify_all_events_and_trainers(L, TID_INT, events, (5, 8), 'Map 202 Duneholt Mart')
    _verify_4bit_bfs(L, TID_INT, events, (5, 8), [
        ('Exit', (5, 9), False),
        ('Mart Counter Talk', (4, 3), False),
        ('Provisioner', (7, 6), True),
    ], 'Map 202 Duneholt Mart')

    np.save(os.path.join(HERE, 'data', 'raw', '202.npy'), L.astype(np.int16))
    spec = {
        'id': 202,
        'name': 'Duneholt Mart',
        'parent': 200,
        'bgm': 'Poke Mart',
        'map_audio': {'bgs': ''},
        'tone': [10, 4, -6, 2],
        'metadata': {'MapPosition': DUN_POS},
        'biome': 'interior',
        'tileset': TID_INT,
        'raw': 'data/raw/202.npy',
        'events': events,
    }
    with open(os.path.join(HERE, 'specs', '202_duneholt_mart.yaml'), 'w', encoding='utf-8') as f:
        f.write('# GENERATED by mapgen/layouts/duneholt_interiors.py (Batch 3A): Duneholt Mart.\n')
        f.write(yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))
    print('Wrote specs/202_duneholt_mart.yaml and data/raw/202.npy')


# =================================================================================================
# 3. MAP 209 — SAHAR'S DIG LAB (21x15, TS 34 — Bustling Canyon Paleontology & Fossil Workshop!)
# =================================================================================================
FOSSIL_REVIVAL_RUBY = r'''fossils = [
  [:OLDAMBER,    :AERODACTYL, "Old Amber"],
  [:HELIXFOSSIL, :OMANYTE,    "Helix Fossil"],
  [:DOMEFOSSIL,  :KABUTO,     "Dome Fossil"],
  [:ROOTFOSSIL,  :LILEEP,     "Root Fossil"],
  [:CLAWFOSSIL,  :ANORITH,    "Claw Fossil"],
  [:SKULLFOSSIL, :CRANIDOS,   "Skull Fossil"],
  [:ARMORFOSSIL, :SHIELDON,   "Armor Fossil"],
  [:COVERFOSSIL, :TIRTOUGA,   "Cover Fossil"],
  [:PLUMEFOSSIL, :ARCHEN,     "Plume Fossil"],
  [:JAWFOSSIL,   :TYRUNT,     "Jaw Fossil"],
  [:SAILFOSSIL,  :AMAURA,     "Sail Fossil"]
]
found = fossils.select { |it, _sp, _nm| $bag.has?(it) rescue false }
if found.empty?
  pbMessage(_INTL("Fossil Tech: Bring me any fossil or Old Amber from Ossaria's sands or mines, and our revival rig will wake it up!"))
else
  cmds = found.map { |_it, _sp, nm| nm } + [_INTL("Never mind")]
  choice = pbMessage(_INTL("Fossil Tech: Oho! You've got fossils in your pack! Which one should I revive?"), cmds, cmds.length)
  if choice >= 0 && choice < found.length
    it, sp, nm = found[choice]
    pbMessage(_INTL("Fossil Tech: Initializing the sandstone resonance tank for your {1}...", nm))
    pbSEPlay("Mining reveal")
    pbWait(18)
    $bag.remove(it, 1)
    pbAddPokemon(sp, 20)
    pbMessage(_INTL("Fossil Tech: Alive and kicking! The desert keeps everything — and we help give it back."))
  end
end'''


def build_209():
    W, H = 21, 15
    L = np.zeros((3, H, W), dtype=np.int32)
    floor = np.zeros((H, W), dtype=bool)
    floor[2:13, 1:20] = True
    floor[12, 1] = False
    floor[12, 19] = False
    floor[13, 8:13] = True
    floor[14, 9:12] = True

    _seam_terracotta_room(L, floor, wall_style='terracotta')

    # Multi-Zone Paleontology Lab Flooring: Cream Sandstone Central Lab + Ochre Archive Wings + Flush Woven Rug Runner
    _put_9slice(L, CREAM_SANDSTONE, 1, 2, 19, 12, z=0, mask=floor)
    _put_9slice(L, HONEY_PARQUET, 1, 7, 7, 12, z=0, mask=floor)
    _put_9slice(L, HONEY_PARQUET, 13, 7, 19, 12, z=0, mask=floor)
    _put_9slice(L, CREAM_SANDSTONE, 8, 13, 12, 14, z=0, mask=floor)
    # Plush crimson-and-gold Ossaria woven rug flowing cleanly all the way to Exit (10,14) — ZERO cut-off doorframe strip!
    _put_9slice(L, SHER_WOVEN_RUG, 9, 7, 11, 14, z=1, mask=floor)

    # North Canyon Wall: Geological Strata Maps, Sunlit Windows & Rolls of Unearthing Trial Board (crisp spacing!)
    _put_grid(L, GEO_MAP, 2, 0, z_rows=(1, 1))
    _put_grid(L, HOTEL_WINDOW, 6, 0, z_rows=(1, 1))
    _put_grid(L, GEO_MAP, 9, 0, z_rows=(1, 1))
    _put_grid(L, HOTEL_WINDOW, 13, 0, z_rows=(1, 1))
    # Rolls of Unearthing Notice Board cleanly right of bookcase at (17..19, 0..1) -> action event on (18, 1)!
    _put_grid(L, [[5795, 5796, 5797], [5803, 5804, 5805]], 17, 0, z_rows=(1, 1))

    # NW Bay (x=1..7, y=2..6): COMPLETE 3x4 Fossil Revival Tank + Specimen Console + Grounded Spade!
    LABTANK_3X4 = [
        [4784, 4785, 4786],
        [4792, 4793, 4794],
        [4800, 4801, 4802],
        [4808, 4809, 4810],
    ]
    _put_grid(L, LABTANK_3X4, 1, 2, z_rows=(2, 1, 1, 1))                 # Complete 3x4 dome & tank (1..3, 2..5)!
    _put_tf(L, 'console', 4, 2)                                          # Specimen analysis terminal (4..6, 2..3)
    L[1, 3, 7] = 4878                                                    # Dig spade propped beside Sahar's bench

    # North Center (x=8..12, y=2..4): Sahar's Excavation Bench flanked by Ancient Claydol Totems!
    L[2, 2, 8] = 4553; L[1, 3, 8] = 4561                                 # Ancient Claydol clay totem (8, 2..3)
    L[2, 2, 12] = 4553; L[1, 3, 12] = 4561                               # Matching Claydol totem (12, 2..3)
    _put_tf(L, 'workbench', 9, 2)                                        # Wide excavation bench (9..11, 2..3)
    L[2, 2, 10] = 3428                                                   # Sahar's field rubbing ledger on bench

    # NE Bay (x=14..19, y=2..6): COMPLETE 3x3 Closed-Right Mahogany Fossil Display Bookcase & Specimen Crates!
    MAHOG_BOOKCASE_3X3 = [
        [4650, 4651, 4652],
        [4658, 4659, 4660],
        [4666, 4667, 4668],
    ]
    _put_grid(L, MAHOG_BOOKCASE_3X3, 14, 2, z_rows=(2, 1, 1))            # Complete 3x3 mahogany bookcase (14..16, 2..4)!
    _put_tf(L, 'crate_i2', 18, 3)                                        # Fossil-mineral crate (18..19, 3..4)

    # SW Interns' Bay (x=2..7, y=8..11): Study Desks, Specimen Crate + Pickaxe & "KEVIN" on a Pedestal!
    _put_grid(L, [[7384, 7385], [7392, 7393]], 2, 8, z_rows=(1, 1))      # Intern desk with open books (2..3, 8..9)
    _put_tf(L, 'crate_i', 2, 10)                                         # Specimen crate (2..3, 10..11)
    L[1, 11, 4] = 4877                                                   # Excavation pickaxe resting beside specimen crate
    # "KEVIN" — a stubborn grey rock sitting proudly on a specimen pedestal at (6, 9)!
    L[1, 9, 6] = 4749                                                    # Solid fossil boulder ("Kevin")
    L[1, 10, 6] = 4077                                                   # Viewing stool

    # SE Paleontology Archive & Bone Sorting Bay (x=13..19, y=8..11)
    _put_tf(L, 'bookcase', 17, 7)                                        # Reference library shelf (17..18, 7..8)
    _put_grid(L, [[7384, 7385], [7392, 7393]], 14, 9, z_rows=(1, 1))     # Intern desk (14..15, 9..10)
    _put_tf(L, 'crate', 18, 10)                                          # Packed rubbing crate (18..19, 10..11)
    L[2, 10, 13] = 2271; L[1, 11, 13] = 2279                             # Warm carved wood work-lamp
    L[2, 5, 19] = 7126; L[1, 6, 19] = 7134                               # Potted desert ficus

    events = [
        {'type': 'exit', 'at': [10, 14], 'link': 'DH_LAB', 'arrive': [10, 14, 'up']},
        # Warden Sahar Ostrand (SAHAR sprite — calls pf_trial_talk(:SAHAR_DIGLAB) if OS_AMBER_AGAIN ready, else Ch6 canon!)
        {'type': 'event', 'name': 'Sahar', 'at': [10, 5], 'pages': [{
            'graphic': {'sprite': 'SAHAR', 'dir': 'down'},
            'trigger': 'action',
            'move': 'fixed',
            'commands': [{
                'if': '(pf_trial_ready?(:SAHAR_DIGLAB) rescue false)',
                'then': [{'script': 'pf_trial_talk(:SAHAR_DIGLAB)'}],
                'else': [
                    "Sahar: Don't come any closer. You'll breathe on it.",
                    "Sahar: ...You're the challenger. The Lumen one. The one who walks in the glass. Everyone's heard.",
                    "Sahar: Sahar Ostrand. I keep the Dig, and the Earth Plate, and a well that's falling into itself a rung a week while a man in a palace sells the water underneath it.",
                    "Sahar: One thing, before you go anywhere in Ossaria. Walk the bones, never the sand.",
                    "Sahar: Where there's a rib or a road of bone, walk on it. Where there's only sand, don't. The desert keeps everything. It just doesn't keep it where you left it.",
                ],
            }],
        }]},
        # Rolls of Unearthing Trial Board (Live pf_trial_board(:OSSARIA)!)
        {'type': 'event', 'name': 'Rolls of Unearthing Board', 'at': [18, 1], 'pages': [{
            'trigger': 'action',
            'commands': [
                {'if': 'defined?(pf_trial_board)',
                 'then': [{'script': 'pf_trial_board(:OSSARIA)'}],
                 'else': ['THE ROLLS OF UNEARTHING — Ossaria Trial Board. Clay tablets pinned in neat rows.']},
            ],
        }]},
        # Live Fossil Revival Technician!
        {'type': 'event', 'name': 'Fossil Technician', 'at': [5, 5], 'pages': [{
            'graphic': {'sprite': 'trainer_SCIENTIST', 'dir': 'down'},
            'trigger': 'action',
            'move': 'fixed',
            'commands': [{'script': FOSSIL_REVIVAL_RUBY}],
        }]},
        # "Kevin" the Rock/Carbink (OS_KEVIN canon!)
        _sign('Kevin', (6, 9),
              'A round, stubborn grey rock resting on a specimen pad. A taped nametag reads: "KEVIN — STAFF (DO NOT MOVE)." If you hold your breath, it almost sounds like it is snoring.'),
        # Three Exhausted Dig Lab Interns (verified gender/age sprites from sprites.jpg!)
        _make_npc('Dig Intern Tariq', (5, 9), 'NPC 24', 'right', [
            "Intern Tariq: We ran three revival cycles on that specimen and got... Kevin.",
            "Intern Tariq: Kevin is a rock. Kevin is in the staff photo. Sahar says if we throw Kevin out she'll deduct it from our sand-brush stipend.",
        ]),
        _make_npc('Dig Intern Samira', (15, 11), 'NPC 22', 'up', [
            "Intern Samira: Cataloguing rubbings from the Necropolis and the Marrow Road! Everything down there is written in Unown script that refuses to stay still.",
        ]),
        _make_npc('Dig Intern Farid', (17, 5), 'NPC 17', 'left', [
            "Intern Farid: That's the Rolls of Unearthing board on the north wall behind me. Check it whenever you want Ossaria Trial commissions!",
        ]),
    ]

    ts34 = R.tilesets()[TID_INT]
    ev_pts = [(10, 14), (10, 13), (10, 5), (18, 2), (5, 5), (6, 9), (5, 9), (15, 11), (17, 5)]
    PG.guard(L, TID_INT, ev_pts, 'Map 209')
    assert not PG.hits(L, ts34, ev_pts), 'Map 209 passguard hits!'
    _verify_all_events_and_trainers(L, TID_INT, events, (10, 13), "Map 209 Sahar's Dig Lab")
    _verify_4bit_bfs(L, TID_INT, events, (10, 13), [
        ('Exit', (10, 14), False),
        ('Sahar', (10, 5), True),
        ('Rolls of Unearthing Board', (18, 2), False),
        ('Fossil Technician', (5, 5), True),
        ('Kevin', (6, 9), True),
        ('Intern Tariq', (5, 9), True),
        ('Intern Samira', (15, 11), True),
        ('Intern Farid', (17, 5), True),
    ], "Map 209 Sahar's Dig Lab")

    np.save(os.path.join(HERE, 'data', 'raw', '209.npy'), L.astype(np.int16))
    spec = {
        'id': 209,
        'name': "Sahar's Dig Lab",
        'parent': 200,
        'bgm': 'Lab',
        'map_audio': {'bgm': 'Intro - Larch Lab', 'bgs': ''},
        'tone': [8, 4, -4, 0],
        'metadata': {'MapPosition': DUN_POS},
        'biome': 'interior',
        'tileset': TID_INT,
        'raw': 'data/raw/209.npy',
        'events': events,
    }
    with open(os.path.join(HERE, 'specs', '209_sahars_dig_lab.yaml'), 'w', encoding='utf-8') as f:
        f.write("# GENERATED by mapgen/layouts/duneholt_interiors.py (Batch 3A): Sahar's Dig Lab.\n")
        f.write(yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))
    print('Wrote specs/209_sahars_dig_lab.yaml and data/raw/209.npy')


# =================================================================================================
# Ossaria Grand Palace Subclass (Maps 206 & 207 on TS 59 PF Rejuv Manor)
# =================================================================================================
class OssariaPalace(Palace):
    """Crimson-and-gold brocade (cvH) + warm terracotta-ochre mosaic (G_f*) + travertine (lm_plaza) Palace."""

    def __init__(self, W, H, seed):
        super().__init__(W, H, seed, tid=TID_MANOR)
        self.kit = {'default': 'cvH', TER: 'cvB'}
        self.STAIRS = tuple(P1('mn_stair_' + k) for k in 'lmr')
        self.mosaic_boxes = []
        self.sun_medallions = []

    def mosaic_floor(self, x0, y0, x1, y1):
        self.mosaic_boxes.append((x0, y0, x1, y1))

    def sun_medallion(self, x, y):
        self.sun_medallions.append((x, y))

    def _apply_custom_floors(self):
        super()._apply_custom_floors()
        mosaic = [P1('G_f%d' % i) for i in range(4)]
        for x0, y0, x1, y1 in self.mosaic_boxes:
            for y in range(max(0, y0), min(self.H, y1 + 1)):
                for x in range(max(0, x0), min(self.W, x1 + 1)):
                    if self.cls[y, x] == '.' and not self.cliff[y, x]:
                        self.L[0, y, x] = mosaic[(x * 3 + y * 5) % 4]
        sun_L = RC.resolve(np.array(STAMPS['lm_sun']['layers'], dtype=np.int32), TID_MANOR)
        for sx, sy in self.sun_medallions:
            for dy in range(sun_L.shape[1]):
                for dx in range(sun_L.shape[2]):
                    t = int(sun_L[0, dy, dx] or sun_L[1, dy, dx])
                    if t and self.inb(sx + dx, sy + dy):
                        self.L[0, sy + dy, sx + dx] = t


# =================================================================================================
# 4. MAP 206 — ELECTOR'S PALACE - HALL OF AUDIENCE (29x25, TS 59 PF Rejuv Manor)
# =================================================================================================
def build_206():
    W, H = 29, 25
    m = OssariaPalace(W, H, seed=206)
    Rb = m.room_box

    # ---- 1. Void-Sculpted Cruciform Audience Hall with Elevated Throne Dais (TER) & Recessed Portals ----
    # Elevated North Throne Dais (TER): x=9..19, y=3..9 (open dais floor y=5..8!)
    Rb(9, 3, 19, 9, TER, 'Y', 'H')
    # Central Vaulted Audience Nave (FLOOR): x=9..19, y=10..22
    Rb(9, 10, 19, 22, FLOOR, 'H', 'H')
    # West Mural-Gallery Wing (FLOOR): x=3..9, y=10..20 + recessed West Portal Alcove x=2..3, y=12..16!
    Rb(3, 10, 9, 20, FLOOR, 'H', 'H')
    m.box(2, 12, 3, 16, FLOOR)
    # East Royal-Crypt Wing (FLOOR): x=19..25, y=10..20 + recessed East Portal Alcove x=25..26, y=12..16!
    Rb(19, 10, 25, 20, FLOOR, 'H', 'H')
    m.box(25, 12, 26, 16, FLOOR)
    # Recessed Monumental South Entry Portal framing exits (13..15, 23)
    m.box(12, 22, 16, 23, FLOOR)

    # Architectural corner chamfers & stone buttress recesses (ZERO boring box!)
    m.mass_at([
        (3, 10), (4, 10), (3, 11), (3, 19), (3, 20), (4, 20),
        (24, 10), (25, 10), (25, 11), (25, 19), (25, 20), (24, 20),
        (9, 3), (19, 3),
    ])

    # Grand 5-Wide Crimson-Carpeted Palace Staircase descending from Kassan's Dais (x=12..16, y=10..12)
    m.stairs(12, 10, w=5, n=3, c='.')
    m.plan_cliffs(rows=3)

    # ---- 2. Sandstone Travertine, Terracotta Mosaic, Gold Inlays, Crimson Runner & Sun Medallion ----
    m.marble_floor(9, 5, 19, 9, 'plaza')
    m.marble_inlay(10, 5, 18, 8)
    m.marble_floor(10, 13, 18, 22, 'plaza')
    m.marble_inlay(10, 13, 18, 21)
    m.marble_floor(12, 22, 16, 23, 'plaza')
    m.marble_floor(2, 14, 3, 15, 'plaza')
    m.marble_floor(25, 14, 26, 15, 'plaza')
    m.mosaic_floor(4, 12, 9, 19)
    m.mosaic_floor(19, 12, 24, 19)
    m.sun_medallion(12, 15)                                              # 5x5 gilded sun medallion in court center!
    m.runner(13, 19, 15, 23)
    m.runner(13, 13, 15, 14)
    m.runner(13, 5, 15, 9)
    m.runner(2, 14, 6, 15)                                               # Unobstructed crimson runner into West Mural Gallery!
    m.runner(22, 14, 26, 15)                                             # Unobstructed crimson runner into East Royal Crypt!

    # ---- 3. Prince-Elector Kassan's Throne, Classical Pillars, Royal Sun Banners & Braziers ----
    # Regally Framed Throne Dais Backdrop (north wall y=3..4, throne seat at (14, 5))
    m.on('mn_window', 10, 3)
    m.on('mn_window', 18, 3)
    m.stamps.append(('lm_banner_w', 13, 3))                              # Crimson-gold royal sun banners framing throne!
    m.stamps.append(('lm_banner_w', 14, 3))
    m.stamps.append(('lm_banner_w', 15, 3))
    m.on('lm_pillar', 12, 3)                                             # Ivory-gold classical columns framing throne dais (base y=5)!
    m.on('lm_pillar', 16, 3)
    m.on('mn_chairR_down', 14, 5)                                        # Prince-Elector Kassan's Throne!
    m.on('mn_statue', 10, 5)
    m.on('mn_statue', 18, 5)
    m.on('mn_candelabra', 12, 6)                                         # Golden candelabras flanking throne carpet cleanly!
    m.on('mn_candelabra', 16, 6)
    m.on('mn_palm', 10, 7)                                               # Grounded cleanly on dais marble (y=7..8, OFF y=9 balustrade!)
    m.on('mn_palm', 18, 7)

    # Fossil Pillars & Armored Court Statues flanking the Central Audience Nave (ZERO grey pipe whalebones!)
    for x in (10, 18):
        for y in (13, 17, 20):
            m.on('nr_col', x, y)
    m.on('mn_armour', 9, 15)                                             # Ceremonial royal armour flanking sun medallion
    m.on('mn_armour', 19, 15)
    m.on('fw_brazier', 11, 21)
    m.on('fw_brazier', 17, 21)

    # West Wing (Mural Gallery approach) & East Wing (Royal Crypt approach) — runners 100% UNOBSTRUCTED!
    for wx, wy in ((6, 10), (8, 10), (20, 10), (22, 10)):
        m.on('mn_window', wx, wy)
    m.stamps.append(('lm_banner_w', 4, 11))                              # Royal sun banners marking West & East portal alcoves!
    m.stamps.append(('lm_banner_w', 24, 11))
    m.late.append((1, 5, 11, P1('mn_sconce')))
    m.late.append((1, 23, 11, P1('mn_sconce')))
    m.on('mn_bust', 5, 12)                                               # Moved north to (5, 12..13) — 1 full tile clear of y=14..15 runner!
    m.on('mn_bust', 23, 12)                                              # Moved north to (23, 12..13) — 1 full tile clear of y=14..15 runner!
    m.on('mn_candelabra', 5, 17)
    m.on('mn_candelabra', 23, 17)
    m.on('mn_palm', 7, 17)
    m.on('mn_palm', 21, 17)
    m.on('mn_bench', 7, 12)
    m.on('mn_bench', 20, 12)

    # ALL THREE Chandeliers (3x2 on L[2]) — pf_glow & cv_shaft applied SAFELY post-paint where L[2]==0!
    chandeliers_206 = [(13, 6), (13, 15), (13, 20)]
    for cx, cy in chandeliers_206:
        m.stamps.append(('mn_chandelier', cx, cy))

    # ---- 4. Bidirectional Warps & Canonical Court NPCs ----
    m.events = [
        {'type': 'exit', 'at': [14, 23], 'link': 'DH_PALACE', 'arrive': [14, 22, 'up']},
        {'type': 'warp', 'name': 'South to Courtyard L', 'at': [13, 23], 'to': {'map': 205, 'x': 20, 'y': 9, 'dir': 'down'}, 'se': 'Door exit'},
        {'type': 'warp', 'name': 'South to Courtyard R', 'at': [15, 23], 'to': {'map': 205, 'x': 20, 'y': 9, 'dir': 'down'}, 'se': 'Door exit'},
        # West Recessed Portal -> 207 Elector's Palace - Mural Gallery
        {'type': 'warp', 'name': 'West to Mural Gallery', 'at': [2, 14], 'to': {'map': 207, 'x': 38, 'y': 8, 'dir': 'left'}, 'se': 'Door enter'},
        {'type': 'warp', 'name': 'West to Mural Gallery ', 'at': [2, 15], 'to': {'map': 207, 'x': 38, 'y': 8, 'dir': 'left'}, 'se': 'Door enter'},
        # East Recessed Portal -> 208 Necropolis of the Electors (NW Royal Crypt Stair!)
        {'type': 'warp', 'name': 'East to Royal Crypt (Necropolis)', 'at': [26, 14], 'to': {'map': 208, 'x': 7, 'y': 7, 'dir': 'down'}, 'se': 'Door enter'},
        {'type': 'warp', 'name': 'East to Royal Crypt (Necropolis) ', 'at': [26, 15], 'to': {'map': 208, 'x': 7, 'y': 7, 'dir': 'down'}, 'se': 'Door enter'},
        # Elector's Throne inspectable
        _sign("Elector's Throne", (14, 5),
              "The sandstone-and-ivory throne of Prince-Elector Idris Kassan of Ossaria. Carved into its plinth: 'ELECTED FOR LIFE — BY SEAL OF THE EIGHTEEN.'"),
        # Canonical Court NPCs
        _make_npc('Grand Chamberlain', (17, 7), 'NPC 12', 'down', [
            "Grand Chamberlain: You stand in the Hall of Audience of Ossaria. Every pillar along the nave incorporates fossil bone quarried from the Rib Road.",
            "Grand Chamberlain: His Excellency Prince-Elector Kassan is presently in Lumen conferring with the Accord. When the Festival delegation is named, it departs from this very court.",
        ]),
        _make_npc('Palace Guard', (11, 14), 'trainer_WARDGUARD', 'right', [
            "Palace Guard: The west arch leads into the Mural Gallery. Curator-Elect Nasrin is overseeing restoration work inside.",
        ]),
        _make_npc('Crypt Warden', (22, 15), 'trainer_WARDGUARD', 'left', [
            "Crypt Warden: The eastern steps descend directly into the Royal Crypt corner of the Necropolis of the Electors.",
            "Crypt Warden: Mind your lanterns down there — Channelers and Ruin Maniacs haunt the lower chambers.",
        ]),
    ]

    m.paint()
    Lr = RC.resolve(m.L, TID_MANOR).astype(np.int32)
    # Safe overhead sunbeams & floor glows (NEVER overwrite L[2] chandeliers or brazier flames!)
    _add_safe_overlay(Lr, TID_MANOR, 'cv_shaft', [(11, 5), (17, 5), (6, 12), (22, 12)])
    _add_safe_overlay(Lr, TID_MANOR, 'pf_glow', [(14, 8), (14, 17), (11, 21), (17, 21), (5, 17), (23, 17), (3, 14), (24, 14)])

    # Assert 100% intact 3x2 chandeliers (all 18 tiles untouched!) and intact braziers!
    ch_ref = RC.resolve(np.array(STAMPS['mn_chandelier']['layers'], dtype=np.int32), TID_MANOR)
    for cx, cy in chandeliers_206:
        for dy in range(2):
            for dx in range(3):
                assert int(Lr[2, cy + dy, cx + dx]) == int(ch_ref[2, dy, dx]), f'206 chandelier ({cx},{cy}) damaged at ({cx+dx},{cy+dy})!'
    br_ref = RC.resolve(np.array(STAMPS['fw_brazier']['layers'], dtype=np.int32), TID_MANOR)
    for bx, by in ((11, 21), (17, 21)):
        assert int(Lr[2, by, bx]) == int(br_ref[2, 0, 0]), f'206 brazier flame damaged at ({bx},{by})!'

    ev_pts = [tuple(e['at']) for e in m.events]
    PG.guard(Lr, TID_MANOR, ev_pts, 'Map 206')
    assert not PG.hits(Lr, R.tilesets()[TID_MANOR], ev_pts), 'Map 206 passguard hits!'
    _verify_all_events_and_trainers(Lr, TID_MANOR, m.events, (14, 22), 'Map 206 Hall of Audience')

    np.save(os.path.join(HERE, 'data', 'raw', '206.npy'), Lr.astype(np.int16))
    spec = {
        'id': 206,
        'name': "Elector's Palace - Hall of Audience",
        'parent': 205,
        'bgm': 'Tiall',
        'map_audio': {'bgm': 'Theme - Accord', 'bgs': ''},
        'tone': [12, 4, -6, 2],
        'metadata': {'Name': "Elector's Palace", 'Outdoor': False, 'MapPosition': DUN_POS},
        'biome': 'interior',
        'tileset': TID_MANOR,
        'raw': 'data/raw/206.npy',
        'events': m.events,
    }
    with open(os.path.join(HERE, 'specs', '206_electors_palace_hall.yaml'), 'w', encoding='utf-8') as f:
        f.write("# GENERATED by mapgen/layouts/duneholt_interiors.py (Batch 3A): Elector's Palace - Hall of Audience.\n")
        f.write(yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))
    print('Wrote specs/206_electors_palace_hall.yaml and data/raw/206.npy')


# =================================================================================================
# 5. MAP 207 — ELECTOR'S PALACE - MURAL GALLERY (41x15, TS 59 PF Rejuv Manor)
# =================================================================================================
def build_207():
    W, H = 41, 15
    m = OssariaPalace(W, H, seed=207)
    Rb = m.room_box

    # ---- 1. Sculpted Gallery Hall with FOUR Deepened North Mural Alcoves + 2-Row East Vestibule ----
    # Main gallery hall: x=2..38, y=4..12 + East entry vestibule x=38..39, y=6..10 (walkable floor y=8..9!)
    Rb(2, 4, 38, 12, FLOOR, 'H', 'H')
    m.box(38, 6, 39, 10, FLOOR)
    # Four deepened recessed north mural alcoves (breaks straight corridor monotony -> genuine gallery bays!)
    mural_xs = [7, 16, 25, 34]
    for mx in mural_xs:
        m.box(mx - 2, 3, mx + 2, 5, FLOOR)
    # Architectural south wall buttress chamfers
    m.mass_at([
        (2, 4), (38, 4), (2, 12), (38, 12),
        (11, 12), (20, 12), (29, 12),
    ])
    m.plan_cliffs(rows=3)

    # ---- 2. Travertine & Mosaic Gallery Floor + Continuous Crimson-and-Gold Runner ----
    m.marble_floor(3, 6, 37, 11, 'plaza')
    m.marble_inlay(3, 6, 37, 11)
    for mx in mural_xs:
        m.marble_floor(mx - 2, 5, mx + 2, 5, 'plaza')
    m.mosaic_floor(4, 6, 36, 7)
    m.runner(4, 8, 39, 9)

    # ---- 3. Four Illuminated Recessed Historical Mural Alcoves (x=7, 16, 25, 34) ----
    # Each bay has classical columns on flanking piers, crimson-gold sun banners, sconces, artifact plinths & mural relief!
    ports = ['mn_portK', 'mn_portX', 'mn_portX', 'mn_portL']
    for mx, pt in zip(mural_xs, ports):
        m.late.append((1, mx, 4, P1(pt)))                                # Illuminated mural panel recessed on alcove wall (y=4)!
        m.late.append((1, mx - 1, 4, P1('mn_sconce')))
        m.late.append((1, mx + 1, 4, P1('mn_sconce')))
        m.stamps.append(('lm_banner_w', mx - 2, 3))                      # Royal crimson-gold sun banner framing alcove
        m.stamps.append(('lm_banner_w', mx + 2, 3))
        m.on('mn_plinth', mx - 2, 5)                                     # Artifact display plinths framing recessed floor niche
        m.on('mn_plinth', mx + 2, 5)
        m.on('nr_col', mx - 3, 6)
        m.on('nr_col', mx + 3, 6)

    # South wall velvet gallery benches, grounded potted palm & candelabras (y=10 -> bases firmly on y=11 floor!)
    for bx in (6, 15, 24, 33):
        m.on('mn_bench', bx, 11)
    for cx in (4, 13, 22, 31, 37):
        m.on('mn_candelabra', cx, 10)                                    # y=10..11 -> bases stand cleanly on marble floor y=11!
    m.on('mn_palm', 3, 6)
    m.on('mn_palm', 3, 10)                                               # y=10..11 -> pot stands cleanly on marble floor y=11!
    m.on('mn_statue', 3, 8)

    # FOUR Intact Chandeliers centered over the crimson runner, cleanly BETWEEN every column & aligned with the 4 alcoves!
    chandeliers_207 = [(6, 8), (15, 8), (24, 8), (33, 8)]
    for chx, chy in chandeliers_207:
        m.stamps.append(('mn_chandelier', chx, chy))

    # ---- 4. Four Canonical Readable Murals, Curator-Elect Nasrin Vael & W0-Walkable East Return Portal ----
    m.events = [
        # Strictly on walkable W0 runner tiles (39, 8) and (39, 9) — ZERO solid-wall touch warp!
        {'type': 'warp', 'name': 'East to Hall of Audience', 'at': [39, 8], 'to': {'map': 206, 'x': 4, 'y': 14, 'dir': 'right'}, 'se': 'Door exit'},
        {'type': 'warp', 'name': 'East to Hall of Audience ', 'at': [39, 9], 'to': {'map': 206, 'x': 4, 'y': 14, 'dir': 'right'}, 'se': 'Door exit'},
        _sign('Mural I — The Gilded King', (7, 4),
              "MURAL I: A golden king under a burning sun, one hand raised as if weighing the sky itself. Below him, white domes and a harbour. Someone has painted fresh ochre over old chisel-scratches across his face."),
        _sign('Mural II — Year of Two Weathers', (16, 4),
              "MURAL II: Two colossi tearing at the land — one red from the earth, one blue from the sea — along a western coastline that is now Ossaria's Dry Tide. Tiny armies hold golden chains between them."),
        _sign('Mural III — The Eighteen-Lit Beast', (25, 4),
              "MURAL III: A towering beast ringed in eighteen coloured lights, bound by a chain of eighteen golden locks held by the golden king. Along the stone frame runs a line of Unown script — one single glyph chiseled blank."),
        _sign('Mural IV — The First Electors', (34, 4),
              "MURAL IV: Eighteen sandstone slabs raised around Duneholt's well after the golden city tipped into the sea. A brass plaque screwed underneath reads: 'CLOSED FOR RESTORATION BY ORDER OF HIS EXCELLENCY IDRIS KASSAN.'"),
        _make_npc('Curator-Elect Nasrin Vael', (26, 7), 'NPC 22', 'up', [
            "Curator-Elect Nasrin: Mind the varnish. His Excellency ordered the gallery 'restored' — which mostly meant adding a heavier lock to the door.",
            "Curator-Elect Nasrin: Look at the third mural's inscription. One Unown letter is missing, and without it the sentence reads wrong. Once you've seen the Ossuary's own walls, come back and help me check what it truly says.",
        ]),
        _make_npc('Gallery Restorer', (9, 7), 'NPC 13', 'up', [
            "Restorer: Three layers of gilt and red canyon ochre! Whoever painted the original frieze three hundred years ago wasn't celebrating that golden king — they were warning us.",
        ]),
    ]

    m.paint()
    Lr = RC.resolve(m.L, TID_MANOR).astype(np.int32)
    # Safe overhead sunbeams & floor glows (NEVER overwrite L[2] chandeliers or banners!)
    _add_safe_overlay(Lr, TID_MANOR, 'cv_shaft', [(mx - 1, 5) for mx in mural_xs])
    _add_safe_overlay(Lr, TID_MANOR, 'pf_glow', [(mx, 5) for mx in mural_xs] + [(chx + 1, 10) for chx, _ in chandeliers_207])

    # Assert ALL 4 chandeliers 100% intact (24/24 tiles!)
    ch_ref = RC.resolve(np.array(STAMPS['mn_chandelier']['layers'], dtype=np.int32), TID_MANOR)
    for cx, cy in chandeliers_207:
        for dy in range(2):
            for dx in range(3):
                assert int(Lr[2, cy + dy, cx + dx]) == int(ch_ref[2, dy, dx]), f'207 chandelier ({cx},{cy}) damaged at ({cx+dx},{cy+dy})!'

    ev_pts = [tuple(e['at']) for e in m.events]
    PG.guard(Lr, TID_MANOR, ev_pts, 'Map 207')
    assert not PG.hits(Lr, R.tilesets()[TID_MANOR], ev_pts), 'Map 207 passguard hits!'
    _verify_all_events_and_trainers(Lr, TID_MANOR, m.events, (38, 8), 'Map 207 Mural Gallery')

    np.save(os.path.join(HERE, 'data', 'raw', '207.npy'), Lr.astype(np.int16))
    spec = {
        'id': 207,
        'name': "Elector's Palace - Mural Gallery",
        'parent': 206,
        'bgm': 'Tiall',
        'map_audio': {'bgm': 'Theme - Accord', 'bgs': ''},
        'tone': [10, 4, -8, 4],
        'metadata': {'Name': "Elector's Palace", 'Outdoor': False, 'MapPosition': DUN_POS},
        'biome': 'interior',
        'tileset': TID_MANOR,
        'raw': 'data/raw/207.npy',
        'events': m.events,
    }
    with open(os.path.join(HERE, 'specs', '207_electors_palace_mural_gallery.yaml'), 'w', encoding='utf-8') as f:
        f.write("# GENERATED by mapgen/layouts/duneholt_interiors.py (Batch 3A): Elector's Palace - Mural Gallery.\n")
        f.write(yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))
    print('Wrote specs/207_electors_palace_mural_gallery.yaml and data/raw/207.npy')


# =================================================================================================
# 6. MAP 208 — NECROPOLIS OF THE ELECTORS (44x40, TS 57 PF Rejuv Cave — Petra Sandstone Tombs!)
# =================================================================================================
def build_208():
    W, H = 44, 40
    m = Cave(W, H, 'E', seed=208, pool='Cave Pool', tid=TID_CAVE)
    m.STAIRS = (P1('E_stairl'), P1('E_stairm'), P1('E_stairr'))
    m.kit = {MASS: 'cvE', TER: 'cvE', FLOOR: 'cvE', 'default': 'cvE'}

    # ---- 1. Carve Interconnected Petra-Style Sandstone Catacomb Chambers (Axis-Aligned & Chamfered!) ----
    # South Petra Entrance Vestibule (FLOOR): x=16..27, y=30..38 (South Return Warp at x=21..22, y=38!)
    m.box(16, 30, 27, 38, FLOOR, '.')
    # Central Hall of the Eighteen Electors (FLOOR): x=15..28, y=11..29 (with central spring pool!)
    m.box(15, 11, 28, 29, FLOOR, '.')
    # West Sarcophagus Cloister (FLOOR): x=4..15, y=13..29 (Trainer CHANNELER Zenobia!)
    m.box(4, 13, 15, 29, FLOOR, '.')
    # Connecting West-South Crypt Passage: x=8..16, y=28..33
    m.box(8, 28, 16, 33, FLOOR, '.')
    # NW Royal Crypt Elevated Landing (TER): x=4..12, y=4..12 + Recessed North Ascending Stair Alcove x=7..8, y=2..5!
    m.box(4, 4, 12, 12, TER, '.')
    m.box(7, 2, 8, 5, TER, '.')
    # North Inner Sanctum of the First Elector (TER): x=15..28, y=4..10 (Smooth Rock treasure!)
    m.box(15, 4, 28, 10, TER, '.')
    # East Catacomb Gallery (FLOOR): x=28..41, y=14..24 + Carved East Marrow Tunnel Opening x=40..43, y=16..21!
    m.box(28, 14, 41, 24, FLOOR, '.')
    m.box(40, 16, 43, 21, FLOOR, '.')                                    # Recessed 3-row walkable tunnel y=18..20 exiting east!
    # SE Bone Reliquary Alcove (FLOOR): x=30..38, y=25..33 (Rare Bone treasure!)
    m.box(30, 25, 38, 33, FLOOR, '.')

    # Sculpted rock piers & chamfers for catacomb depth (ZERO featureless giant square!)
    m.mass_at([
        (4, 29), (14, 27), (15, 27),
        (16, 30), (27, 30), (16, 38), (27, 38),
        (30, 32), (30, 33), (38, 25), (38, 33),
        (29, 14), (29, 24), (41, 14), (41, 24),
        (4, 4), (12, 4), (15, 4), (28, 4),
    ])

    # Central Subterranean Aquifer Pool inside the Hall of the Eighteen Electors (x=20..23, y=19..23)
    m.box(20, 19, 23, 23, FLOOR, 'w')

    # Carved Sandstone Staircases ascending to elevated TER Sanctums (starting directly on TER cliff lip!)
    m.stairs(6, 12, w=3, n=3, c='.')
    m.stairs(20, 10, w=4, n=3, c='.')
    m.plan_cliffs(rows=3)

    # ---- 2. Petra Sarcophagi, Ancient Elector Monument, Pillars & 13/13 Burning Braziers! ----
    # ZERO snowdrift fw_skull, ZERO Elowen pf_shrine, ZERO grey pipe pf_whalebone!
    braziers_208 = [
        (19, 36), (24, 36),
        (19, 18), (24, 18), (19, 24), (24, 24),
        (11, 20),                                                        # Moved clear of Zenobia (10,22) 4-tile left sightline!
        (6, 9), (9, 9),
        (19, 8), (24, 8),
        (36, 17), (36, 21), (39, 17), (39, 21),
    ]
    props_208 = [
        # South Petra Entry Vestibule
        ('nr_col', 18, 34), ('nr_col', 25, 34),
        ('nr_col', 18, 31), ('nr_col', 25, 31),
        ('pf_roadstone', 17, 35), ('pf_roadstone', 26, 35),
        # Central Hall of Eighteen Electors (framing subterranean pool)
        ('nr_col', 17, 17), ('nr_col', 26, 17),
        ('nr_col', 17, 25), ('nr_col', 26, 25),
        ('pf_roadstone', 18, 21), ('pf_roadstone', 25, 21),
        # West Sarcophagus Cloister (rock-cut tombs — Zenobia's 4-tile left LoS (9..6, 22) 100% OPEN!)
        ('nr_ruin', 6, 18), ('nr_ruin', 6, 24),
        ('mn_plinth', 11, 18), ('mn_plinth', 11, 24),
        ('pf_roadstone', 5, 21), ('pf_roadstone', 10, 29),
        # NW Royal Crypt (beneath Elector's Palace!)
        ('nr_col', 5, 7), ('nr_col', 10, 7),
        ('mn_statue', 5, 10), ('mn_statue', 10, 10),
        # North Inner Sanctum — Authentic Ancient Bronze & Stone First Elector Monument (replaces Elowen ribbon shrine!)
        ('lm_statue', 21, 5),
        ('nr_col', 18, 6), ('nr_col', 25, 6),
        ('mn_bust', 17, 8), ('mn_bust', 26, 8),
        # East Catacomb Gallery & Carved Marrow Tunnel + SE Bone Reliquary
        ('nr_col', 32, 16), ('nr_col', 32, 22),
        ('nr_col', 38, 16), ('nr_col', 38, 22),
        ('nr_colfall', 34, 16),                                          # Pulled south off y=15 north rock wall!
        ('mn_plinth', 31, 27), ('nr_ruin', 32, 29),
        ('pf_roadstone', 12, 28), ('pf_roadstone', 33, 25), ('pf_roadstone', 36, 28),
    ] + [('fw_brazier', bx, by) for bx, by in braziers_208]

    for nm, px, py in props_208:
        L_st = STAMPS[nm]['layers']
        h_s, w_s = len(L_st[0]), len(L_st[0][0])
        m.stamps.append((nm, px, py))
        occ = np.array(L_st).max(axis=0) > 0
        m.taken[py:py + h_s, px:px + w_s] |= occ
        m.bodym[py:py + h_s, px:px + w_s] |= occ

    # ---- 3. Canonical Events, Bidirectional Warps & Exact PBS Trainers (Zenobia & Lucan!) ----
    E = [
        # South Return Warp -> 200 Terrace Bazaar NE Petra Tomb Mouth (36, 9, down)
        {'type': 'warp', 'name': 'South to Terrace Bazaar', 'at': [21, 38], 'to': {'map': 200, 'x': 36, 'y': 9, 'dir': 'down'}, 'se': 'Door exit'},
        {'type': 'warp', 'name': 'South to Terrace Bazaar ', 'at': [22, 38], 'to': {'map': 200, 'x': 36, 'y': 9, 'dir': 'down'}, 'se': 'Door exit'},
        # NW Royal Crypt Recessed Ascending Stair -> 206 Hall of Audience East Crypt Portal (24, 14, left)
        {'type': 'warp', 'name': 'Up to Hall of Audience', 'at': [7, 5], 'to': {'map': 206, 'x': 24, 'y': 14, 'dir': 'left'}, 'se': 'Door exit'},
        {'type': 'warp', 'name': 'Up to Hall of Audience ', 'at': [8, 5], 'to': {'map': 206, 'x': 24, 'y': 14, 'dir': 'left'}, 'se': 'Door exit'},
        # Guarded East Marrow Road Carved Tunnel Exit -> 620 The Marrow Road (in-world, 0 warnings!)
        {'type': 'event', 'name': 'East to Marrow Road', 'at': [42, 18], 'pages': [{'trigger': 'touch', 'through': True,
            'commands': _guarded_unbuilt_transfer(620, 2, 35, 'right', "(Beyond the eastern tomb-tunnel lies the Marrow Road and the Ossuary of Dunes. Tomb-wardens are still clearing a fresh dune-collapse across the outer canyon mouth.)")}]},
        {'type': 'event', 'name': 'East to Marrow Road ', 'at': [42, 19], 'pages': [{'trigger': 'touch', 'through': True,
            'commands': _guarded_unbuilt_transfer(620, 2, 35, 'right', "(Beyond the eastern tomb-tunnel lies the Marrow Road and the Ossuary of Dunes. Tomb-wardens are still clearing a fresh dune-collapse across the outer canyon mouth.)")}]},
        {'type': 'event', 'name': 'East to Marrow Road  ', 'at': [42, 20], 'pages': [{'trigger': 'touch', 'through': True,
            'commands': _guarded_unbuilt_transfer(620, 2, 35, 'right', "(Beyond the eastern tomb-tunnel lies the Marrow Road and the Ossuary of Dunes. Tomb-wardens are still clearing a fresh dune-collapse across the outer canyon mouth.)")}]},
        # Canonical Tomb-keeper (older robed desert keeper sprite NPC 21 — story/25_SCRIPT_CH6.md:315)
        _make_npc('Tomb-keeper', (20, 35), 'NPC 21', 'right', [
            "Tomb-keeper: The Electors are buried facing the dunes. So they can see who's coming.",
            "Tomb-keeper: Lately they've seen a lot of drill-heads.",
        ]),
        # Exact PBS Trainer #1 for Map 208 (pbs/trainers.txt: [CHANNELER, Zenobia]) — 4-tile left LoS 100% OPEN!
        {
            'type': 'trainer',
            'name': 'Trainer(4)',
            'at': [10, 22],
            'sight': 4,
            'dir': 'left',
            'sprite': 'trainer_CHANNELER',
            'trainer': ['CHANNELER', 'Zenobia'],
            'intro': "Channeler Zenobia: Eighteen Electors sit in stone silence — and they've called a quorum on you!",
            'after': "Channeler Zenobia: The Electors voted. It was unanimous. Walk softly past their niches.",
        },
        # Exact PBS Trainer #2 for Map 208 (pbs/trainers.txt: [RUINMANIAC, Lucan]) — 4-tile down LoS 100% OPEN!
        {
            'type': 'trainer',
            'name': 'Trainer(4) ',
            'at': [26, 20],
            'sight': 4,
            'dir': 'down',
            'sprite': 'trainer_RUINMANIAC',
            'trainer': ['RUINMANIAC', 'Lucan'],
            'intro': "Ruin Maniac Lucan: Eighteen rock-cut doors and every one older than Meridian! Test your mettle before the inner sanctum!",
            'after': "Ruin Maniac Lucan: Eighteen tomb doors and I knocked on yours. Fair play — the First Elector's shrine lies north up the stairs.",
        },
        # Readable Tomb Monument Plaque & Verified PBS Pickups
        _sign('First Elector Plaque', (22, 7),
              "MONUMENT OF THE FIRST ELECTOR — 'Walk the bones, keep the well, answer to the sand.'"),
        {'type': 'item', 'at': [26, 7], 'item': 'SMOOTHROCK'},
        {'type': 'item', 'at': [6, 27], 'item': 'HYPERPOTION'},
        {'type': 'item', 'at': [36, 31], 'item': 'RAREBONE'},
        {'type': 'item', 'name': 'HiddenItem (spring rim)', 'at': [18, 23], 'item': 'STARPIECE', 'hidden': True},
    ]
    m.events = E
    for e in E:
        ex, ey = e['at']
        m.keep_clear.add((ex, ey))
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            if m.inb(ex + dx, ey + dy):
                m.keep_clear.add((ex + dx, ey + dy))

    m.paint()

    # Inlay warm travertine & terracotta-ochre mosaic paving in the Ceremonial Hall, Sanctum, Royal Crypt & Carved Marrow Tunnel!
    plaza = [P1('lm_plaza0'), P1('lm_plaza1')]
    mosaic = [P1('G_f%d' % i) for i in range(4)]
    floorpatch_ids = {P1(k) for k in STAMPS if k.startswith(('E_floorpatch_', 'E_fd'))}
    for x0, y0, x1, y1, pal in [
        (19, 31, 24, 38, plaza),
        (17, 15, 26, 27, plaza),
        (19, 6, 24, 10, mosaic),
        (6, 5, 9, 11, plaza),
        (33, 18, 43, 20, plaza),                                         # Flows cleanly right into the carved east Marrow tunnel!
    ]:
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if m.cls[y, x] == '.' and not m.cliff[y, x] and not m.taken[y, x]:
                    m.L[0, y, x] = pal[(x * 3 + y * 5) % len(pal)]
                    if int(m.L[1, y, x]) in floorpatch_ids:
                        m.L[1, y, x] = 0
    # Crisp ascending stone steps inside the recessed NW Royal Crypt alcove (7..8, 4..5) leading up to Elector's Palace (206)!
    for sy in (4, 5):
        m.L[1, sy, 7] = P1('E_stairl')
        m.L[1, sy, 8] = P1('E_stairr')

    Lr = RC.resolve(m.L, TID_CAVE).astype(np.int32)
    # Safe sunbeams & brazier glows strictly on unoccupied L[2] cells — ALL 15/15 brazier flames burn 100% intact!
    _add_safe_overlay(Lr, TID_CAVE, 'cv_shaft', [(21, 7), (7, 8), (21, 16), (21, 33), (35, 18), (40, 18)])
    _add_safe_overlay(Lr, TID_CAVE, 'pf_glow', braziers_208)

    # Programmatic assertion: ALL 15/15 fw_brazier flames intact on L[2]!
    br_ref = RC.resolve(np.array(STAMPS['fw_brazier']['layers'], dtype=np.int32), TID_CAVE)
    flame_tid = int(br_ref[2, 0, 0])
    for bx, by in braziers_208:
        assert int(Lr[2, by, bx]) == flame_tid, f'208 brazier flame LOST at ({bx},{by}): got {Lr[2, by, bx]} != {flame_tid}!'
    print(f'Map 208: Verified {len(braziers_208)}/{len(braziers_208)} fw_brazier flames 100% INTACT (tile {flame_tid})!')

    ev_pts = [tuple(e['at']) for e in E]
    PG.guard(Lr, TID_CAVE, ev_pts, 'Map 208')
    assert not PG.hits(Lr, R.tilesets()[TID_CAVE], ev_pts), 'Map 208 passguard hits!'
    _verify_all_events_and_trainers(Lr, TID_CAVE, E, (21, 37), 'Map 208 Necropolis of the Electors')

    np.save(os.path.join(HERE, 'data', 'raw', '208.npy'), Lr.astype(np.int16))
    spec = {
        'id': 208,
        'name': 'Necropolis of the Electors',
        'parent': 200,
        'bgm': 'Cave',
        'field': 'CAVE',
        'map_audio': {'bgm': 'Dungeon - Cave', 'bgs': 'Drip - Nadir', 'bgs_volume': 45, 'rain': False},
        'tone': [-14, -18, -22, 16],
        'fog': {'name': 'prismfall_cave', 'opacity': 24, 'blend': 1, 'zoom': 100, 'sx': 1, 'sy': 0},
        'metadata': {'Name': 'Necropolis of the Electors', 'Outdoor': False, 'ShowArea': True, 'BattleBack': 'cave1', 'MapPosition': DUN_POS},
        'biome': 'interior',
        'tileset': TID_CAVE,
        'raw': 'data/raw/208.npy',
        'events': E,
    }
    with open(os.path.join(HERE, 'specs', '208_necropolis_of_the_electors.yaml'), 'w', encoding='utf-8') as f:
        f.write('# GENERATED by mapgen/layouts/duneholt_interiors.py (Batch 3A): Necropolis of the Electors.\n')
        f.write(yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))
    print('Wrote specs/208_necropolis_of_the_electors.yaml and data/raw/208.npy')


def main():
    build_201()
    build_202()
    build_209()
    build_206()
    build_207()
    build_208()
    print('Done: built 6 Duneholt interior & dungeon maps (201, 202, 206, 207, 208, 209).')


if __name__ == '__main__':
    main()
