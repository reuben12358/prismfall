#!/usr/bin/env python3
"""layouts/cindervault_core.py — Cindervault Core Maps (Batch 2: 240, 241, 242, 243):
  - Map 240: Cindervault - Forge Terraces (46x42, tileset 61 PF Rejuv Forge, field VOLCANIC)
      Three-tier terraced volcanic caldera smithy city above Slag Ward (249) & Caldera Gate (243):
      * Upper Caldera Rim (TER2=3): Grand Foundry (Gym 7 -> 250) flanked by twin basalt gate towers & magma culverts,
        NW Pyre Keep Rampart stair (-> 245), NE Dragon Roosts stair (-> 248), and projecting Hearthguild Bell-Tower
        promontory with walkable overlooking balcony & Bell-Ringer above Caldera Square.
      * Mid Caldera Terrace (TER=2): Cindervault Pokémon Center (cv_pc -> 241), Cindervault Mart (cv_mart -> 242),
        West Pass to The Ashmarch (-> 660), central Caldera Square with Slag Ward arrival at (20,26) facing up &
        descending stairwell at (20,27) -> 249 (4,3) down, market stalls ("BREAD (YESTERDAY'S).", "WATER (BOILING)."),
        glowing vertical quench-channel bridged by iron grates, and East Rim The Crucible Arena (gt_gate4 grand
        archway, sand ring, Legate Varra Kosk, Forte of the Octave).
      * Lower Forge Terraces (FLOOR=1): Varied forged-brick & timber smithy lane (ZERO copy-paste blocks) featuring
        "ADEQUATE SWORDS." across the lane from "EXCELLENT SWORDS.", "SMITH. NOT VERY GOOD. CHEAP.", glowing molten
        quench-channel with iron-grate bridge, anvils, slag carts, and SE stair -> 243 Caldera Gate.
  - Map 241: Cindervault Pokémon Center (15x11, tileset 34 Prismfall Interior, BGM Poke Center, HealingSpot)
      Warm volcanic-slate & timber Ashkaar Pokémon Center with standard Nurse (7,2), Healing Machine (5,2),
      PC (11,2), Town Map (12,1), crackling kettle-hearth lounge, local Ashkaar traveler, and Gale Post desk.
  - Map 242: Cindervault Mart (12x10, tileset 34 Prismfall Interior, BGM Poke Mart)
      Cozy volcanic-timber & slate Ashkaar supply shop with clerk at (2,3), honest war-prices shopper NPC,
      smithing/fire-zone crates, kegs & stocked shelves.
  - Map 243: Cindervault - Caldera Gate (40x24, tileset 61 PF Rejuv Forge, field VOLCANIC)
      Massive basalt crater-rim gatehouse with monumental walkable iron portcullis archway (gt_gate6 -> 652 Pyre Road),
      north arrival promontory from 249 Slag Ward at (20,4) facing down with return warp (19..21,3) -> 249 (21,31) up,
      panoramic caldera rim overlooks peering down onto glowing magma tiers & Tap No. 7 below, NE terrace stair up to
      240 Forge Terraces, West Pass (-> 660 Ashmarch), warning bell-post, Gate Smith, Oath-Guard & caravan carts.

Story canon: story/29_SCRIPT_CH8.md, design/TRIALS_QUESTS.md (AS_OCTAVE_TOO_LOUD, AS_SEVEN_BOUTS, AS_ADEQUATE_SWORDS).
NOTE: Static NPCs/signs only (zero invented plot switches/vars); dynamic Ch8 hooks documented in handoff notes.

Run:
    /usr/bin/python3 -I mapgen/layouts/cindervault_core.py
"""
import os
import sys
from collections import deque
import numpy as np
import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cavekit import Cave, FLOOR, TER, TER2, MASS, P1
import rkit as K
from rkit import STAMPS
import rcompose as RC
import render as R
import passguard as PG
from interiorkit import TF

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TID_FORGE = 61
TID_INT = 34
VOID_34 = 5437


# =================================================================================================
# Shared Helpers (Forge Outdoor Maps 240/243 & Tileset-34 Interiors 241/242)
# =================================================================================================
def _guarded_unbuilt_transfer(map_id, tx, ty, direction, blocked_text):
    """Guarded exit to an unbuilt map without emitting a raw RMXP code-201 command (keeps build.py at 0 WARN)."""
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


def _place_stamp_over(m, name, x, y, base_z=1, top_z=2, top_rows=0, solid=True):
    """Composite a PF Rejuv stamp into m.over with explicit layer split."""
    L = STAMPS[name]['layers']
    h, w = len(L[0]), len(L[0][0])
    for dy in range(h):
        for dx in range(w):
            if not m.inb(x + dx, y + dy):
                continue
            for sz in (0, 1, 2):
                t = int(L[sz][dy][dx])
                if t:
                    tz = top_z if (dy < top_rows or sz == 2) else base_z
                    m.over.append((tz, x + dx, y + dy, t))
            if solid:
                m.taken[y + dy, x + dx] = True


def _place_building(m, name, x, y, door_link=None, door_name=None, plaque=None, mark_arch_clear=None):
    """Place a multi-tile building or gatehouse stamp cleanly on a Cave map."""
    st = STAMPS[name]
    w, h = st['w'], st['h']
    m.stamps.append((name, x, y))
    L = np.array(st['layers'])
    occ = L.max(axis=0) > 0
    if mark_arch_clear:
        for (ax, ay) in mark_arch_clear:
            lx, ly = ax - x, ay - y
            if 0 <= lx < w and 0 <= ly < h:
                occ[ly, lx] = False
    m.taken[y:y + h, x:x + w] |= occ
    m.bodym[y:y + h, x:x + w] |= occ
    d = st.get('door')
    if d is not None:
        dx, dy = x + d[0], y + d[1]
        m.keep_clear.add((dx, dy))
        if m.inb(dx, dy + 1):
            m.keep_clear.add((dx, dy + 1))
        if door_link:
            m.events.append({
                'type': 'door',
                'at': [dx, dy],
                'gfx': ['', 0, 2],
                'name': door_name or (name + ' door'),
                'link': door_link,
            })
        elif plaque:
            m.events.append({
                'type': 'sign',
                'name': door_name or 'Door plate',
                'at': [dx, dy],
                'post': False,
                'text': plaque,
            })
        return (dx, dy)
    return None


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


def _sign(name, at, text, post=False):
    return {'type': 'sign', 'name': name, 'at': list(at), 'post': post, 'text': text}


def _bfs_check_cave(m, start, targets, label):
    """Verify 4-neighbor Essentials walkability from start to every target cell on a Cave map."""
    import build as B
    Lr = RC.resolve(m.L, m.tid).astype(np.int32)
    PG.guard(Lr, m.tid, [tuple(e['at']) for e in m.events if e and e.get('at')], label)
    ts = R.tilesets()[m.tid]
    H, W = m.H, m.W
    solid_ev = set()
    for e in m.events:
        if e.get('type') in ('npc', 'trainer', 'mart'):
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
            reach = (tx, ty) in seen or any((tx + dx, ty + dy) in seen for dx, dy in ((1, 0), (-1, 0), (0, 1), (-1, 0)))
            reach = (tx, ty) in seen or any((tx + dx, ty + dy) in seen for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        else:
            reach = (tx, ty) in seen
        if not reach:
            missing.append((name, (tx, ty), bool(ok[ty, tx])))
    print('%s BFS: %d walkable cells reached from %s; missing=%s' % (label, len(seen), start, missing))
    assert not missing, '%s unreachable targets: %s' % (label, missing)
    return seen


def _bfs_check_interior(L, start, targets, label):
    """Verify 4-neighbor Essentials walkability for a tileset 34 interior map."""
    import build as B
    ts = R.tilesets()[TID_INT]
    H, W = L.shape[1:]
    ok = np.array([[B.cell_passable(L, ts, x, y) for x in range(W)] for y in range(H)])
    sx, sy = start
    assert ok[sy, sx], '%s: start %s is NOT passable!' % (label, start)
    seen = {start}
    q = deque([start])
    while q:
        cx, cy = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < W and 0 <= ny < H and (nx, ny) not in seen and ok[ny, nx]:
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


# =================================================================================================
# MAP 240 — Cindervault - Forge Terraces (46x42, tileset 61 PF Rejuv Forge, field VOLCANIC)
# =================================================================================================
def build_240():
    W, H = 46, 42
    m = Cave(W, H, 'L', seed=240, pool='Magma', tid=TID_FORGE)
    m.STAIRS = K.STAIRS_STONE
    m.kit = {MASS: 'cvL', TER2: 'cvL', TER: 'cvL', FLOOR: 'cvL', 'default': 'cvL'}

    # ---- 1. Sculpt Three-Tier Volcanic Caldera Terraces (TER2=3 upper rim, TER=2 square/civic/Crucible, FLOOR=1 lower lane) ----
    # Lower Forge Terraces (FLOOR=1, y=29..39, x=3..42) + SE exit notch down to 243 Caldera Gate + lower quench culvert (10..11, 39..40)
    m.box(3, 29, 42, 39, FLOOR, '.')
    m.box(27, 39, 31, 41, FLOOR, '.')
    m.box(10, 39, 11, 40, FLOOR, 'w')
    # Jagged outer basalt spurs framing the lower basin
    m.mass_at([
        (3, 38), (3, 39), (4, 39), (42, 38), (42, 39), (41, 39),
        (13, 39), (14, 39), (35, 39), (36, 39),
    ])

    # Mid Caldera Terrace (TER=2, y=11..28, x=3..42) — PC, Mart, Caldera Square, The Crucible!
    m.box(3, 11, 42, 28, TER, '.')
    # West Rim Pass notch out toward 660 The Ashmarch (x=1..3, y=20..26 so y=20..22 cliff leaves y=23..26 walkable!)
    m.box(1, 20, 3, 26, TER, '.')
    m.mass_at([
        (3, 11), (3, 12), (3, 27), (3, 28), (4, 28),
        (42, 11), (42, 12), (42, 27), (42, 28),
    ])

    # Upper Caldera Rim (TER2=3, y=3..10, x=4..41) + projecting Hearthguild Bell-Tower Spur over Caldera Square!
    m.box(4, 3, 41, 10, TER2, '.')
    # Three upper exit notches carved to y=0 (ZERO cliff hang over y=2, exact pattern of Map 249!):
    m.box(5, 0, 7, 3, TER2, '.')
    m.box(19, 0, 23, 3, TER2, '.')
    m.box(37, 0, 39, 3, TER2, '.')
    # Projecting Hearthguild Bell-Tower rocky spur (TER2=3, x=18..24, y=10..17) overlooking Caldera Square!
    m.box(18, 10, 24, 17, TER2, '.')
    m.mass_at([
        (4, 3), (4, 4), (41, 3), (41, 4), (15, 3), (27, 3), (34, 3),
    ])

    # ---- 2. Organic Glowing Molten Quench-Channels (PF Magma — stepped volcanic channels!) ----
    magma_cells = [
        # Upper Rim Foundry flanking cooling culverts (visible beside the twin Foundry towers!)
        (14, 6), (15, 6), (14, 7), (15, 7), (14, 8), (15, 8),
        (27, 6), (28, 6), (27, 7), (28, 7), (27, 8), (28, 8),
        # Mid-Tier Vertical Quench-Channel dividing Caldera Square from The Crucible (x=30..31, y=14..27)!
        (30, 14), (31, 14), (30, 15), (31, 15), (30, 16), (31, 16),
        (30, 17), (31, 17), (29, 17), (30, 18), (31, 18), (29, 18),
        (30, 19), (31, 19), (30, 20), (31, 20), (30, 21), (31, 21),
        (30, 22), (31, 22), (30, 23), (31, 23), (30, 24), (31, 24),
        (30, 25), (31, 25), (30, 26), (31, 26), (31, 27),
        # Lower Forge Terrace Meandering Molten Quench-Channel (x=22..25, y=32..38)!
        (22, 32), (23, 32), (24, 32),
        (22, 33), (23, 33), (24, 33), (25, 33),
        (22, 34), (23, 34), (24, 34), (25, 34),
        (23, 35), (24, 35), (25, 35),
        (23, 36), (24, 36), (25, 36),
        (23, 37), (24, 37), (25, 37),
        (24, 38), (25, 38),
        # West Lower Quench Sluice flowing continuously from cliff base (y=31) under Honest Swords Lane grate (y=37..38) to south culvert (y=39..40)!
        (10, 31), (11, 31), (10, 32), (11, 32), (10, 33), (11, 33),
        (10, 34), (11, 34), (10, 35), (11, 35), (10, 36), (11, 36),
        (10, 37), (11, 37), (10, 38), (11, 38), (10, 39), (11, 39),
        (10, 40), (11, 40),
    ]
    for mx, my in magma_cells:
        m.cls[my, mx] = 'w'

    # ---- 3. Grand Stone Staircases connecting TER2 <-> TER <-> FLOOR ----
    # Upper Rim (TER2=3) -> Mid Terrace (TER=2):
    m.stairs(10, 10, w=3, n=3, c='.')   # West Foundry Grand Stair (x=10..12, y=10..12 -> lands y=13)
    m.stairs(27, 10, w=3, n=3, c='.')   # East Foundry Grand Stair (x=27..29, y=10..12 -> lands y=13)
    # Mid Terrace (TER=2) -> Lower Forge Terraces (FLOOR=1):
    m.stairs(12, 28, w=3, n=3, c='.')   # West Forge Stair (x=12..14, y=28..30 -> lands y=31)
    m.stairs(26, 28, w=3, n=3, c='.')   # East Caldera Stair (x=26..28, y=28..30 -> lands y=31)

    m.tidy()
    m.plan_cliffs(rows=3)

    # ---- 4. Iron-Grate Footbridges crossing Glowing Molten Quench-Channels ----
    bridges = (
        # Grand Crucible Bridge across Mid-Tier Quench-Channel (x=30..31, y=22..24)
        [(x, y) for y in (22, 23, 24) for x in (30, 31)] +
        # Lower Honest Swords Lane Bridge across Lower Quench-Channel (x=23..25, y=36..37)
        [(x, y) for y in (36, 37) for x in (23, 24, 25)] +
        # West Honest Swords Lane Iron-Grate Bridge cleanly spanning flowing quench sluice (x=10..11, y=37..38)!
        [(x, y) for y in (37, 38) for x in (10, 11)]
    )
    for bx, by in bridges:
        m.cls[by, bx] = '.'
        m.keep_clear.add((bx, by))

    # ---- 5. Varied Volcanic Forged-Brick & Timber Buildings (ZERO copy-paste blocks!) ----
    # (a) Upper Caldera Rim (TER2=3): Twin Foundry Gate Towers + Upper Quarters + Roost Shed
    _place_building(m, 'gt_tower', 16, 2)      # West Foundry Gate Bastion (3x6 -> x=16..18, y=2..7)
    _place_building(m, 'gt_tower', 24, 2)      # East Foundry Gate Bastion (3x6 -> x=24..26, y=2..7)
    _place_building(m, 'lb_l4a', 9, 3, plaque='FOUNDRY SHIFT HOUSE. Chalked on the lintel: "FOUR BELLS — LEAVE YOUR TONGS."')
    _place_building(m, 'gl_shed', 30, 3, plaque='ROOST HARNESS & ORE SHED. Smells of scorched saddle-leather and brimstone.')

    # (b) Projecting Hearthguild Bell-Tower Spur (TER2=3): Bell-Tower overlooking Caldera Square!
    _place_building(m, 'gt_tower', 20, 9)      # Hearthguild Bell-Tower (3x6 -> x=20..22, y=9..14; balcony y=15..16!)

    # (c) Mid Caldera Terrace (TER=2): Cindervault Pokémon Center & Cindervault Mart + The Crucible Grand Archway!
    _place_building(m, 'cv_pc', 4, 14, door_link='CV_PC', door_name='Cindervault Pokémon Center')   # door (7,20), step-out (7,21)
    _place_building(m, 'cv_mart', 12, 15, door_link='CV_MART', door_name='Cindervault Mart')        # door (13,20), step-out (13,21)

    # THE CRUCIBLE GRAND ARCHWAY (gt_gate4 10x8 at (32,13) -> x=32..41, y=13..20, walkable central arch x=35..38, y=18..20!)
    crucible_arch_clear = [(x, y) for y in (18, 19, 20) for x in (35, 36, 37, 38)]
    _place_building(m, 'gt_gate4', 32, 13, mark_arch_clear=crucible_arch_clear)

    # (d) Lower Forge Terraces (FLOOR=1): Iconic Honest Ashkaar Smithy Row (4 distinct silhouettes!)
    _place_building(m, 'th_c', 4, 31, plaque='ADEQUATE SWORDS. (The door handle is sturdy. Not ornate. Adequate.)')
    _place_building(m, 'th_j', 15, 31, plaque='EXCELLENT SWORDS. (Inside, blades ring like tuning forks on a dark basalt rack.)')
    _place_building(m, 'th_w', 31, 31, plaque='SMITH. NOT VERY GOOD. CHEAP. (A pile of slightly lopsided horseshoes sits by the threshold.)')
    _place_building(m, 'lb_l5b', 37, 31, plaque='CALDERA TENEMENT. Iron shutters bolted against rising ash.')

    # ---- 6. CRITICAL WARPS, GUARDED EXITS, CANON STATIC NPCs & ICONIC HONEST ASHKAAR SIGNS ----
    E = m.events

    # ACTIVE WARP: Descending Slag Ward Stairwell right below (20,26) arrival -> 249 (4,3) down!
    E.append({
        'type': 'warp',
        'name': 'Down to Slag Ward',
        'at': [20, 27],
        'to': {'map': 249, 'x': 4, 'y': 3, 'dir': 'down'},
        'se': 'Door exit',
    })

    # ACTIVE WARP: SE Caldera Stair down to 243 Caldera Gate -> 243 (34,6) down!
    for sx in (28, 29, 30):
        E.append({
            'type': 'warp',
            'name': 'To Caldera Gate',
            'at': [sx, 40],
            'to': {'map': 243, 'x': 34, 'y': 6, 'dir': 'down'},
            'se': 'Door exit',
        })

    # GUARDED FUTURE EXITS (pbRgssExists? -> 0 warnings!)
    # (1) North-Center Upper Rim -> 250 The Foundry (Gym 7)
    for gx in (20, 21, 22):
        E.append({
            'type': 'event',
            'name': 'To The Foundry (Gym 7)',
            'at': [gx, 2],
            'pages': [{
                'trigger': 'touch',
                'commands': _guarded_unbuilt_transfer(
                    250, 12, 22, 'up',
                    "(The heavy bronze doors of The Foundry are sealed while Brann resets the casting channels. Gym 7 not built yet.)"
                ),
            }],
        })
    # (2) NW Upper Rim -> 245 Pyre Keep Rampart
    for px in (5, 6, 7):
        E.append({
            'type': 'event',
            'name': 'To Pyre Keep Rampart',
            'at': [px, 2],
            'pages': [{
                'trigger': 'touch',
                'commands': _guarded_unbuilt_transfer(
                    245, 16, 22, 'up',
                    "(Red-lacquered Oath-Guards bar the stair to Pyre Keep Rampart until the Dominar's envoys conclude their audience.)"
                ),
            }],
        })
    # (3) NE Upper Rim -> 248 The Dragon Roosts
    for rx in (37, 38, 39):
        E.append({
            'type': 'event',
            'name': 'To The Dragon Roosts',
            'at': [rx, 2],
            'pages': [{
                'trigger': 'touch',
                'commands': _guarded_unbuilt_transfer(
                    248, 12, 20, 'up',
                    "(A Roost-keeper waves you back—updrafts off the caldera rim are too fierce for climbers without a wing-pass.)"
                ),
            }],
        })
    # (4) West Rim Gate -> 660 The Ashmarch
    for wy in (23, 24, 25):
        E.append({
            'type': 'event',
            'name': 'To The Ashmarch',
            'at': [1, wy],
            'pages': [{
                'trigger': 'touch',
                'commands': _guarded_unbuilt_transfer(
                    660, 118, 36, 'left',
                    "(The West Pass out onto the Ashmarch is chained while the Hearthguild bells ring out the caldera heat.)"
                ),
            }],
        })

    # CANON STATIC NPCs (story/29_SCRIPT_CH8.md & design/TRIALS_QUESTS.md; clear hooks for Ch8 dynamic scenes!)
    E += [
        _make_npc('Hearthguild Bell-Ringer', (21, 15), 'NPC 25', 'down', [
            "Hearthguild Bell-Ringer: Three bells this morning. Four yesterday.",
            "Hearthguild Bell-Ringer: We've never rung five. Five means leave the mountain.",
            "Hearthguild Bell-Ringer: I've got the rope for it. I've never had to touch it.",
        ]),
        _make_npc('Legate Varra Kosk', (37, 21), 'trainer_COOLTRAINER_F', 'down', [
            "Legate Varra Kosk: The Crucible judges two things: truth and steel.",
            "Legate Varra Kosk: Lying is a crime in Ashkaar; losing honestly is not. Come back when you're ready for a Writ of Flame.",
        ]),
        _make_npc('Forte', (34, 24), 'trainer_LASS', 'right', [
            "Forte: I'm Forte—of the Octave! And that's Bellows, if he'd stop trying to chew the brazier!",
            "Forte: The Crucible won't hear a Choir orphan without a second to stand for her. I'm louder than every bell on this mountain, and I'm NOT sorry!",
        ]),
        _make_npc('Terrace Smith', (26, 33), 'trainer_HIKER', 'left', [
            "Terrace Smith: I can't work. The quench-channels are running at a boil.",
            "Terrace Smith: You can't quench in boiling. A blade wants a shock, not a bath.",
        ]),
        _make_npc("Smith's Apprentice", (17, 25), 'NPC 14', 'up', [
            "Smith's Apprentice: The Meridian men say the tap's fine.",
            "Smith's Apprentice: They put a gauge on it. The gauge says fine. The gauge is also melting.",
        ]),
        _make_npc('Old Smith', (35, 37), 'NPC 25', 'down', [
            "(An old smith sits beside a cold anvil, turning a piece of slag over in calloused fingers.)",
            "Old Smith: My grandmother used to say the Flame Plate's not a fire, it's a heart. You don't put a pipe in a heart.",
        ]),
        _make_npc('Adequate Swords Owner', (7, 38), 'trainer_BLACKBELT', 'right', [
            "Adequate Swords Owner: Look across the lane. 'EXCELLENT SWORDS.' Claiming excellence is a bold gamble where lying is a crime!",
            "Adequate Swords Owner: Mine are adequate. Honestly adequate. Good steel, fair edge, no boasts.",
        ]),
    ]

    # ALL ICONIC HONEST ASHKAAR SIGNS + LANDMARK PLAQUES!
    E += [
        _sign('Honest Sign: Mart', (15, 21),
              "MART: PRICES HIGH BECAUSE OF THE WAR THAT ISN'T HAPPENING."),
        _sign('Honest Sign: Bread', (16, 24),
              "BREAD (YESTERDAY'S). (The crust could stop a hammer; the baker looks proud of his candour.)"),
        _sign('Honest Sign: Water', (25, 22),
              "WATER (BOILING). (Steam curls briskly out of the iron cauldron set over a floor grate.)"),
        _sign('Honest Sign: Adequate Swords', (9, 37),
              "ADEQUATE SWORDS. (Carved neatly into dark basalt. Not a word more than the truth.)"),
        _sign('Honest Sign: Excellent Swords', (14, 37),
              "EXCELLENT SWORDS. (Freshly painted across the lane from Adequate Swords. Neighbours are squinting at it.)"),
        _sign('Honest Sign: Cheap Smith', (30, 36),
              "SMITH. NOT VERY GOOD. CHEAP."),
        _sign('Foundry Gym Sign', (19, 8),
              "THE FOUNDRY — CINDERVAULT GYM. Warden Brann Holloway. \"Pour, then quench. Bring Water.\""),
        _sign('Pyre Keep Sign', (8, 4),
              "PYRE KEEP RAMPART — THE DOMINAR'S SEAT. Say true, or say nothing."),
        _sign('Dragon Roosts Sign', (36, 4),
              "THE DRAGON ROOSTS — LEGION WING. Keep your chin down when the Salamence bank."),
        _sign('Crucible Plaque', (34, 21),
              "THE CRUCIBLE — CALDERA RIM PROVING RING. Legate Varra Kosk presiding. Seven bouts, no healing, no lies."),
        _sign('Caldera Square Marker', (22, 26),
              "CALDERA SQUARE — ↑ Bell-Tower & Foundry · ← Pokémon Center, Mart & Ashmarch · → The Crucible · ↓ Slag Ward & Caldera Gate."),
        {'type': 'item', 'at': [39, 9], 'item': 'HEATROCK', 'name': 'Upper Rim Heat Rock'},
    ]

    # Reserve arrival, warps, doors, stairs, bridges & NPC/sign frontages (including SE courtyard lane to (39,37)!)
    m.keep_clear |= {
        (20, 26), (20, 27), (19, 26), (21, 26), (20, 25), (19, 25), (21, 25),
        (7, 20), (7, 21), (7, 22), (13, 20), (13, 21), (13, 22),
        (28, 39), (29, 39), (30, 39), (28, 40), (29, 40), (30, 40),
        (20, 2), (21, 2), (22, 2), (20, 3), (21, 3), (22, 3),
        (5, 2), (6, 2), (7, 2), (37, 2), (38, 2), (39, 2),
        (1, 23), (1, 24), (1, 25), (2, 23), (2, 24), (2, 25), (3, 23), (3, 24), (3, 25),
        (21, 15), (21, 16), (22, 15), (22, 16), (20, 15), (20, 16),
        (36, 20), (37, 20), (36, 21), (37, 21), (37, 22), (38, 22),
        (32, 22), (32, 23), (32, 24), (33, 22), (33, 23),
        (35, 38), (36, 38), (37, 38), (38, 38), (39, 38), (39, 37), (40, 38),
    }
    for e in E:
        ex, ey = e['at']
        m.keep_clear.add((ex, ey))
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            if m.inb(ex + dx, ey + dy):
                m.keep_clear.add((ex + dx, ey + dy))

    # ---- 7. Multi-Tier Ashkaar Props, Bell-Tower Balcony, Crucible Ring & Volcanic Lighting ----
    # (a) Upper Rim (TER2=3): Foundry Braziers, Banners, Beacon (clean stone lips around magma culverts!)
    _place_stamp_over(m, 'fw_brazier', 19, 6, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'fw_brazier', 23, 6, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'wr_ban_ash', 15, 4, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'wr_ban_ash', 27, 4, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'wr_ban_ash', 4, 5, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'pf_beacon', 34, 5, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'wr_ban_ash_t', 40, 5, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'wr_sacks', 36, 6, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'hb_barrels', 6, 8, base_z=1, top_z=2, top_rows=1, solid=True)

    # (b) Projecting Hearthguild Bell-Tower Balcony (TER2=3, x=18..24, y=15..16)
    _place_stamp_over(m, 'pf_bellpost', 19, 12, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'wr_ban_ash', 18, 13, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'wr_ban_ash', 24, 13, base_z=1, top_z=2, top_rows=2, solid=True)
    # Balcony iron guard-rail along south edge of Bell-Tower spur (y=16, x=19..23) overlooking Caldera Square!
    for rx, piece in ((19, 'lm_bollard'), (20, 'lm_railing_w'), (21, 'lm_railing_m'),
                      (22, 'lm_railing_e'), (23, 'lm_bollard')):
        _place_stamp_over(m, piece, rx, 16, base_z=1, top_z=1, top_rows=0, solid=True)

    # (c) Mid-Tier Civic Promenade & Caldera Square (TER=2)
    _place_stamp_over(m, 'pf_pcsign', 11, 19, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'pf_stall0', 15, 22, base_z=1, top_z=2, top_rows=1, solid=True)     # BREAD (YESTERDAY'S)
    _place_stamp_over(m, 'pf_stall1', 24, 20, base_z=1, top_z=2, top_rows=1, solid=True)     # WATER (BOILING)
    _place_stamp_over(m, 'pf_stonebench', 5, 24, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'pf_stonebench', 10, 24, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'fw_brazier', 4, 21, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'fw_brazier', 18, 21, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'fw_brazier', 28, 21, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'fw_brazier', 28, 25, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'wr_ban_ash', 3, 20, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'lm_bollard', 4, 26, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'pf_well', 8, 26, base_z=1, top_z=2, top_rows=2, solid=True)
    # Slag Ward Descending Stairwell Gantry around (20,27) (leaves (20,26) arrival & (20,27) stair 100% open!)
    _place_stamp_over(m, 'lm_bollard', 19, 27, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'lm_bollard', 21, 27, base_z=1, top_z=1, top_rows=0, solid=True)
    # Warm overhead festival/square lantern string spanning Caldera Square (y=21, x=20..23, pri overhead!)
    for i, lx in enumerate((20, 21, 22, 23)):
        m.over.append((2, lx, 21, P1('pf_lstring%d' % (i % 3))))

    # (d) East Rim — THE CRUCIBLE SAND RING & ARENA PROPS (x=32..42, y=21..27; clean dark archway!)
    _place_stamp_over(m, 'fw_brazier', 33, 20, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'fw_brazier', 41, 20, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'fw_brazier', 33, 26, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'fw_brazier', 41, 26, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'wr_rack', 41, 22, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'wr_rack', 41, 24, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'pf_stonebench', 35, 26, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'pf_stonebench', 38, 26, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'wr_ban_ash', 32, 18, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'wr_ban_ash', 42, 18, base_z=1, top_z=2, top_rows=2, solid=True)

    # (e) Lower Forge Terraces & Honest Swords Lane (FLOOR=1, y=31..39): Anvils, Slag Carts, Braziers, Weapon Racks!
    _place_stamp_over(m, 'wr_rack', 14, 32, base_z=1, top_z=2, top_rows=1, solid=True)     # Cleanly beside Excellent Swords wall!
    _place_stamp_over(m, 'cv_tools', 15, 37, base_z=1, top_z=1, top_rows=0, solid=True)    # Cleanly clear of magma channel!
    _place_stamp_over(m, 'lm_gearbox', 34, 37, base_z=1, top_z=1, top_rows=0, solid=True)  # Old Smith's cold anvil (SE lane (35..36,38) OPEN!)
    _place_stamp_over(m, 'cv_tools', 41, 38, base_z=1, top_z=1, top_rows=0, solid=True)    # Relocated cleanly into SE courtyard corner!
    _place_stamp_over(m, 'cv_cart', 21, 35, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'pf_wagon', 18, 38, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'hb_barrels', 4, 37, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'wr_sacks', 29, 34, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'cv_pump', 29, 31, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'fw_brazier', 14, 34, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'fw_brazier', 27, 38, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'fw_brazier', 31, 38, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'wr_ban_ash', 27, 39, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'wr_ban_ash', 31, 39, base_z=1, top_z=2, top_rows=2, solid=True)

    # (f) Volcanic Steam Plumes & Warm Magma/Brazier Glow Halos (strictly anchored to fire & magma!)
    for sx, sy in ((14, 7), (28, 7), (30, 16), (31, 20), (30, 26), (23, 33), (24, 35), (10, 34)):
        _place_stamp_over(m, 'lm_steam0' if (sx + sy) % 2 == 0 else 'lm_steam1', sx, sy, base_z=2, top_z=2, top_rows=2, solid=False)
    for gx, gy in ((14, 6), (27, 6), (19, 6), (23, 6), (34, 6), (4, 21), (18, 21), (28, 21), (28, 25),
                   (30, 16), (30, 20), (30, 25), (33, 20), (41, 20), (33, 26), (41, 26),
                   (23, 33), (24, 35), (10, 33), (14, 34), (27, 38), (31, 38)):
        m.stamps.append(('pf_glow', gx, gy))

    # Paint Cave geometry & basalt cliffs first
    m.paint()

    # Fix latent passguard(no_ev)=1 on gl_shed door cell (31,7): keep exact visual tile (3094) under an invisible solid blocker!
    if int(m.L[2, 7, 31]) == 3094:
        m.L[1, 7, 31] = 3094
        m.L[2, 7, 31] = PG.blocker(R.tilesets()[m.tid])

    # ---- 8. Moody Volcanic Ashkaar Paving Hierarchy (Warm Soot-Cobbles + Dressed Earth-Stone + Ashlar + Iron Grates!) ----
    low_ids = [P1('lm_low%d' % i) for i in range(4)]
    earth_ids = [P1('E_f%d' % i) for i in range(4)]
    slate_ids = [P1('T_f%d' % i) for i in range(4)]
    qf0, qf1 = P1('Q_f0'), P1('Q_f1')
    grate = P1('lm_grate')
    stair_m = P1('st_stair_m')
    floorpatch_ids = {P1(k) for k in STAMPS if k.startswith(('L_floorpatch_', 'L_fd'))}

    def paint_path_rect(x0, y0, x1, y1, palette):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if not m.inb(x, y):
                    continue
                if m.cls[y, x] != '.' or m.cliff[y, x] or m.taken[y, x]:
                    continue
                m.L[0, y, x] = palette[(x * 3 + y * 5) % len(palette)]
                if int(m.L[1, y, x]) in floorpatch_ids:
                    m.L[1, y, x] = 0

    # Upper Rim promenade (TER2=3): dark soot-brick walk + dressed ashlar Foundry Plaza running cleanly to y=0!
    paint_path_rect(5, 8, 40, 9, low_ids)
    paint_path_rect(19, 0, 23, 9, slate_ids)
    paint_path_rect(5, 0, 7, 8, earth_ids)
    paint_path_rect(37, 0, 39, 8, earth_ids)
    paint_path_rect(19, 10, 24, 15, slate_ids)   # Bell-Tower Balcony terrace flags!

    # Mid-Tier Civic Promenade & Caldera Square (TER=2)
    paint_path_rect(1, 21, 29, 26, low_ids)
    paint_path_rect(4, 21, 15, 23, earth_ids)    # PC & Mart forecourt
    paint_path_rect(18, 21, 28, 26, slate_ids)   # Dressed ashlar Caldera Square!
    paint_path_rect(19, 22, 27, 25, earth_ids)   # Warm central square paving inlay!
    paint_path_rect(0, 23, 5, 25, earth_ids)     # West Pass road to Ashmarch!
    paint_path_rect(12, 25, 15, 28, earth_ids)
    paint_path_rect(26, 25, 28, 28, earth_ids)

    # THE CRUCIBLE SAND RING (x=33..41, y=21..26): warm volcanic ochre sand!
    paint_path_rect(33, 21, 41, 26, earth_ids)
    paint_path_rect(35, 18, 38, 20, slate_ids)   # Walkable stone archway floor inside gt_gate4!

    # Lower Forge Terraces & Honest Swords Lane (FLOOR=1)
    paint_path_rect(4, 37, 41, 39, low_ids)
    paint_path_rect(6, 37, 39, 38, earth_ids)
    paint_path_rect(27, 31, 30, 41, earth_ids)
    paint_path_rect(12, 31, 14, 37, earth_ids)

    # Slag Ward Descending Stairwell Deck at (20,27)
    m.L[0, 27, 20] = qf0
    m.L[1, 27, 20] = stair_m
    m.L[1, 26, 19] = grate
    m.L[1, 26, 21] = grate

    # Iron-Grate Footbridges over Molten Quench-Channels!
    for bx, by in bridges:
        m.L[0, by, bx] = qf0 if (bx + by) % 2 == 0 else qf1
        m.L[1, by, bx] = grate
    for rx, ry in ((29, 21), (32, 21), (29, 25), (32, 25), (22, 36), (26, 36), (12, 36), (12, 39)):
        if m.cls[ry, rx] == '.' and not m.taken[ry, rx] and (rx, ry) not in m.keep_clear:
            m.L[1, ry, rx] = P1('lm_bollard')

    # Subtle volcanic embers in quiet basalt corners
    for i, (x, y) in enumerate(((12, 7), (32, 8), (5, 26), (17, 27), (34, 25), (39, 25), (5, 39), (33, 39))):
        if m.cls[y, x] == '.' and not m.cliff[y, x] and not m.taken[y, x] and (x, y) not in m.keep_clear:
            m.L[1, y, x] = P1('wr_ember%d' % (i % 3))

    _bfs_check_cave(m, (20, 26), [
        ('Slag Ward Return Stair (249)', (20, 27), False),
        ('PC Door (241)', (7, 20), False),
        ('PC Step-out', (7, 21), False),
        ('Mart Door (242)', (13, 20), False),
        ('Mart Step-out', (13, 21), False),
        ('Bell-Tower Balcony & Bell-Ringer', (21, 15), True),
        ('Foundry Gym 7 Exit (250)', (21, 2), False),
        ('Pyre Keep Exit (245)', (6, 2), False),
        ('Dragon Roosts Exit (248)', (38, 2), False),
        ('Ashmarch West Exit (660)', (1, 23), False),
        ('The Crucible Steps (Varra Kosk)', (37, 21), True),
        ('Forte outside Crucible', (34, 24), True),
        ('Adequate Swords Owner', (7, 38), True),
        ('Honest Sign: Excellent Swords', (14, 37), True),
        ('Honest Sign: Cheap Smith', (30, 36), True),
        ('SE Smithy Door Plate', (39, 37), True),
        ('Caldera Gate Exit (243)', (29, 40), False),
        ('Upper Rim Heat Rock', (39, 9), True),
    ] + [(e.get('name', 'ev'), tuple(e['at']), True) for e in E if e and e.get('at')], 'Map 240')

    head = {
        'id': 240,
        'name': 'Cindervault - Forge Terraces',
        'parent': 0,
        'bgm': 'Lava Town',
        'field': 'VOLCANIC',
        'map_audio': {'bgm': 'Town - Ashkaar', 'bgs': 'Lava - Ashkaar', 'bgs_volume': 55, 'rain': False},
        'metadata': {'Name': 'Cindervault', 'Outdoor': True, 'ShowArea': True, 'MapPosition': [0, 24, 8], 'BattleBack': 'cave1'},
        'tone': [22, 2, -16, 10],
        'fog': {'name': 'prismfall_cave', 'opacity': 22, 'blend': 1, 'zoom': 100, 'sx': 1, 'sy': 0},
        '_file': '240_cindervault_forge.yaml',
    }
    m.write(240, head, comment='# GENERATED by mapgen/layouts/cindervault_core.py (Ch8): Cindervault - Forge Terraces.\n'
                               '# Edit the layout script, not this file.\n')
    return m


# =================================================================================================
# MAP 243 — Cindervault - Caldera Gate (40x24, tileset 61 PF Rejuv Forge, field VOLCANIC)
# =================================================================================================
def build_243():
    W, H = 40, 24
    m = Cave(W, H, 'L', seed=243, pool='Magma', tid=TID_FORGE)
    m.STAIRS = K.STAIRS_STONE
    m.kit = {MASS: 'cvL', TER: 'cvL', FLOOR: 'cvL', 'default': 'cvL'}

    # ---- 1. Sculpt Panoramic Basalt Crater-Rim Gatehouse & Magma Overlook Bowl ----
    # Main Gate Courtyard (FLOOR=1, x=3..36, y=9..19) + South Portcullis Archway (x=16..23, y=19..22)
    m.box(3, 9, 36, 19, FLOOR, '.')
    m.box(16, 19, 23, 22, FLOOR, '.')
    # West Pass road to 660 The Ashmarch (x=1..3, y=10..16 so y=10..12 cliff leaves y=13..16 walkable!)
    m.box(1, 10, 3, 16, FLOOR, '.')
    # Sunken North-West & North-East Caldera Magma Overlook Basins (FLOOR=1 filled with glowing magma!)
    m.box(5, 3, 15, 6, FLOOR, 'w')
    m.box(25, 3, 30, 6, FLOOR, 'w')
    m.mass_at([
        (5, 3), (6, 3),
        (3, 18), (3, 19), (4, 19), (36, 18), (36, 19), (35, 19),
    ])

    # North Central Arrival Promontory from 249 Slag Ward (TER=2, carved to y=0 -> ZERO cliff hang over (20,4)!)
    m.box(17, 0, 23, 8, TER, '.')
    # Flanking Panoramic Rim Balconies peering out over the sunken glowing magma tiers (TER=2, y=7..8)!
    m.box(6, 7, 16, 8, TER, '.')
    m.box(24, 7, 30, 8, TER, '.')
    # NE Ascending Terrace Shelf up to 240 Forge Terraces (TER=2, carved to y=0 -> ZERO cliff hang over (34,5..6)!)
    m.box(32, 0, 37, 8, TER, '.')
    m.mass_at([(6, 7), (30, 7)])

    # Additional organic molten vents flanking the south gatehouse crags (natural 4x2 rocky fissures!)
    for mx, my in ((6, 18), (7, 18), (8, 18), (9, 18), (7, 17), (8, 17),
                   (30, 18), (31, 18), (32, 18), (33, 18), (31, 17), (32, 17)):
        m.cls[my, mx] = 'w'

    # ---- 2. Sweeping Panoramic Stone Stairs (TER=2 <-> FLOOR=1) ----
    m.stairs(18, 8, w=4, n=3, c='.')    # Grand Central Caldera Stair (x=18..21, y=8..10 -> lands y=11)
    m.stairs(33, 8, w=3, n=3, c='.')    # NE Forge Terrace Stair (x=33..35, y=8..10 -> lands y=11)

    m.tidy()
    m.plan_cliffs(rows=3)

    # ---- 3. Monumental Basalt Crater-Rim Gatehouse (gt_gate6 12x8 at (14,15)!) ----
    # Walkable 6-wide central iron portcullis archway: x=17..22, y=20..22!
    gate_arch_clear = [(x, y) for y in (20, 21, 22) for x in (17, 18, 19, 20, 21, 22)]
    _place_building(m, 'gt_gate6', 14, 15, mark_arch_clear=gate_arch_clear)

    # ---- 4. CRITICAL WARPS, GUARDED EXITS, CANON STATIC NPCs & PLAQUES ----
    E = m.events

    # ACTIVE WARP: North Return Path back to 249 Slag Ward -> 249 (21,31) up! (Directly north of (20,4) arrival!)
    for nx in (19, 20, 21):
        E.append({
            'type': 'warp',
            'name': 'North to Slag Ward',
            'at': [nx, 3],
            'to': {'map': 249, 'x': 21, 'y': 31, 'dir': 'up'},
            'se': 'Door exit',
        })

    # ACTIVE WARP: NE Ascending Terrace Stair up to 240 Forge Terraces -> 240 (29,37) up!
    for tx in (33, 34, 35):
        E.append({
            'type': 'warp',
            'name': 'Up to Forge Terraces',
            'at': [tx, 5],
            'to': {'map': 240, 'x': 29, 'y': 37, 'dir': 'up'},
            'se': 'Door exit',
        })

    # GUARDED FUTURE EXITS (pbRgssExists? -> 0 warnings!)
    # (1) South Crater Portcullis Archway -> 652 The Pyre Road
    for px in (18, 19, 20, 21):
        E.append({
            'type': 'event',
            'name': 'To The Pyre Road',
            'at': [px, 22],
            'pages': [{
                'trigger': 'touch',
                'commands': _guarded_unbuilt_transfer(
                    652, 65, 6, 'down',
                    "(The Caldera Gate's great iron portcullis groans on its chains—The Pyre Road south is sealed for ash-fall clearance.)"
                ),
            }],
        })
    # (2) West Rim Pass -> 660 The Ashmarch
    for wy in (13, 14, 15):
        E.append({
            'type': 'event',
            'name': 'To The Ashmarch',
            'at': [1, wy],
            'pages': [{
                'trigger': 'touch',
                'commands': _guarded_unbuilt_transfer(
                    660, 118, 36, 'left',
                    "(Ashkaar Oath-Guards have barred the West Pass out onto the Ashmarch while the caldera bells ring.)"
                ),
            }],
        })

    # Canon Static NPCs (story/29_SCRIPT_CH8.md)
    E += [
        _make_npc('Gate Smith', (15, 12), 'trainer_HIKER', 'right', [
            "Gate Smith: Three bells! Off the forges! It's not even noon!",
            "Gate Smith: Look out from the north rim balcony—you can see the steam rising straight off Meridian's tap down in the Slag Ward.",
        ]),
        _make_npc('Oath-Guard', (24, 14), 'trainer_BLACKBELT', 'left', [
            "Oath-Guard: Cindervault's Caldera Gate. Say true, or say nothing.",
            "Oath-Guard: South portcullis leads down the Pyre Road; north stairs drop to Slag Ward; the east terrace climbs to the Forge Terraces.",
        ]),
        _make_npc('Caravan Drover', (9, 14), 'NPC 25', 'right', [
            "Caravan Drover: Hauling quenched iron bars out toward the Ashmarch before the Dominar shuts the eastern passes.",
            "Caravan Drover: Lying's a crime in Ashkaar, so I'll tell you plain: my wheels are smoking and the mountain's in a foul mood.",
        ]),
        _sign('Caldera Overlook Plaque', (17, 7),
              "CALDERA RIM OVERLOOK — Below: Slag Ward & Meridian Standard Tap No. 7. Above: Forge Terraces & Hearthguild Bell-Tower."),
        _sign('Caldera Gate Oath Stone', (16, 14),
              "CINDERVAULT — CALDERA GATE. \"Say true, or keep your breath for the bellows.\" ↑ Slag Ward · ↗ Forge Terraces · ← The Ashmarch · ↓ The Pyre Road."),
    ]

    m.keep_clear |= {
        (20, 4), (19, 4), (21, 4), (20, 5), (19, 3), (20, 3), (21, 3),
        (34, 6), (33, 6), (35, 6), (33, 5), (34, 5), (35, 5),
        (18, 20), (19, 20), (20, 20), (21, 20), (18, 21), (19, 21), (20, 21), (21, 21),
        (18, 22), (19, 22), (20, 22), (21, 22),
        (1, 12), (1, 13), (1, 14), (1, 15), (2, 13), (2, 14),
    }
    for e in E:
        ex, ey = e['at']
        m.keep_clear.add((ex, ey))
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            if m.inb(ex + dx, ey + dy):
                m.keep_clear.add((ex + dx, ey + dy))

    # ---- 5. Panoramic Overlook Railings, Warning Bell-Post, Braziers, Caravan Carts & Volcanic Lighting ----
    # Panoramic overlook railings along north rim balconies peering down into glowing magma tiers!
    for rx in range(8, 16):
        piece = 'lm_bollard' if rx in (8, 15) else 'lm_railing_m'
        _place_stamp_over(m, piece, rx, 7, base_z=1, top_z=1, top_rows=0, solid=True)
    for rx in range(25, 30):
        piece = 'lm_bollard' if rx in (25, 29) else 'lm_railing_m'
        _place_stamp_over(m, piece, rx, 7, base_z=1, top_z=1, top_rows=0, solid=True)
    # Solid-body volcanic forge braziers framing north arrival promontory (zero floating flame gap!)
    _place_stamp_over(m, 'fw_brazier', 17, 4, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'fw_brazier', 23, 4, base_z=1, top_z=2, top_rows=1, solid=True)

    # Gate Courtyard: Warning Bell-Post, Ashkaar Banners, Forge Braziers, Caravan Carts & Crates!
    _place_stamp_over(m, 'pf_bellpost', 13, 11, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'wr_ban_ash', 13, 15, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'wr_ban_ash', 26, 15, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'wr_ban_ash', 4, 10, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'wr_ban_ash', 4, 15, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'fw_brazier', 17, 11, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'fw_brazier', 22, 11, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'fw_brazier', 12, 18, base_z=1, top_z=2, top_rows=1, solid=True)   # Clear of gt_gate6 left spire (x=14)!
    _place_stamp_over(m, 'fw_brazier', 26, 18, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'fw_brazier', 31, 11, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'pf_wagon', 6, 15, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'cv_cart', 11, 16, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'wr_supply', 28, 15, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'hb_barrels', 34, 14, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'wr_sacks', 28, 12, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'wr_rack', 35, 11, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'pf_stonebench', 9, 11, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'pf_barricade', 2, 16, base_z=1, top_z=1, top_rows=0, solid=True)

    # Steam plumes & strictly anchored volcanic glows (12,18 keeps gt_gate6 left tower spire 100% intact!)
    for sx, sy in ((8, 5), (12, 4), (27, 5), (29, 4), (7, 18), (32, 18)):
        _place_stamp_over(m, 'lm_steam0' if (sx + sy) % 2 == 0 else 'lm_steam1', sx, sy, base_z=2, top_z=2, top_rows=2, solid=False)
    for gx, gy in ((8, 5), (12, 4), (27, 5), (17, 4), (22, 4), (17, 11), (22, 11), (12, 18), (26, 18), (31, 11), (7, 17), (32, 17)):
        m.stamps.append(('pf_glow', gx, gy))

    m.paint()

    # ---- 6. Ashkaar Paving Hierarchy ----
    low_ids = [P1('lm_low%d' % i) for i in range(4)]
    earth_ids = [P1('E_f%d' % i) for i in range(4)]
    slate_ids = [P1('T_f%d' % i) for i in range(4)]
    floorpatch_ids = {P1(k) for k in STAMPS if k.startswith(('L_floorpatch_', 'L_fd'))}

    def paint_path_rect(x0, y0, x1, y1, palette):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if not m.inb(x, y):
                    continue
                if m.cls[y, x] != '.' or m.cliff[y, x] or m.taken[y, x]:
                    continue
                m.L[0, y, x] = palette[(x * 3 + y * 5) % len(palette)]
                if int(m.L[1, y, x]) in floorpatch_ids:
                    m.L[1, y, x] = 0

    paint_path_rect(18, 0, 22, 8, slate_ids)        # North Slag Ward arrival promontory running cleanly to y=0!
    paint_path_rect(32, 0, 36, 8, earth_ids)        # NE Forge Terrace landing running cleanly to y=0!
    paint_path_rect(3, 11, 36, 18, low_ids)         # Gate Courtyard cobbles
    paint_path_rect(0, 13, 35, 15, earth_ids)       # Main Caravan Road West <-> East
    paint_path_rect(17, 11, 22, 22, earth_ids)      # Grand North-South Portcullis Approach & Arch Floor!
    paint_path_rect(18, 12, 21, 19, slate_ids)      # Dressed ashlar center axis!

    _bfs_check_cave(m, (20, 4), [
        ('North Return to Slag Ward (249)', (20, 3), False),
        ('NE Stair to Forge Terraces (240)', (34, 5), False),
        ('NE Arrival from Forge Terraces', (34, 6), False),
        ('South Portcullis to Pyre Road (652)', (19, 22), False),
        ('West Pass to Ashmarch (660)', (1, 13), False),
        ('Gate Smith', (15, 12), True),
        ('Oath-Guard', (24, 14), True),
        ('Caravan Drover', (9, 14), True),
        ('Caldera Overlook Plaque', (17, 7), True),
    ], 'Map 243')

    head = {
        'id': 243,
        'name': 'Cindervault - Caldera Gate',
        'parent': 0,
        'bgm': 'Lava Town',
        'field': 'VOLCANIC',
        'map_audio': {'bgm': 'Town - Ashkaar', 'bgs': 'Lava - Ashkaar', 'bgs_volume': 55, 'rain': False},
        'metadata': {'Name': 'Cindervault', 'Outdoor': True, 'ShowArea': True, 'MapPosition': [0, 24, 8], 'BattleBack': 'cave1'},
        'tone': [20, 0, -18, 10],
        'fog': {'name': 'prismfall_cave', 'opacity': 22, 'blend': 1, 'zoom': 100, 'sx': 1, 'sy': 0},
        '_file': '243_caldera_gate.yaml',
    }
    m.write(243, head, comment='# GENERATED by mapgen/layouts/cindervault_core.py (Ch8): Cindervault - Caldera Gate.\n'
                               '# Edit the layout script, not this file.\n')
    return m


# =================================================================================================
# Tileset 34 Ashkaar Interior Primitives (Maps 241 & 242 — ZERO outdoor lamps, max 1 indoor lamp!)
# =================================================================================================
SLATE_STONE = [
    [1152, 1153, 1154],
    [1152, 1153, 1154],
    [1160, 1161, 1162],
]
# Clean seamless timber parquet inlay (row 1067..1069 has ZERO dark dotted horizontal stripes!)
HONEY_PARQUET = [
    [1067, 1068, 1069],
    [1067, 1068, 1069],
    [1067, 1068, 1069],
]
HOTEL_CRIMSON_RUG = [
    [7172, 7173, 7174],
    [7180, 7181, 7182],
    [7188, 7189, 7190],
]
# True TS34 9-slice woven rug (cols 4..6: 8620..8622 / 8628..8630 / 8636..8638 -> crisp 4-sided border!)
BROWN_WOVEN_RUG = [
    [8620, 8621, 8622],
    [8628, 8629, 8630],
    [8636, 8637, 8638],
]
HELP_HEAL = [[6035, 6036], [6043, 6044]]
HOTEL_RED_WINDOW = [[7124, 7125], [7132, 7133]]
TAPESTRY_GOLD = [[5531, 5532], [5539, 5540]]
SEA_CHART = [[4730, 4731], [4738, 4739]]
SHER_DESK = [[5694, 5695], [5702, 5703]]
WOOD_BENCH = [[7875, 7876, 7877], [7883, 7884, 7885]]
HERB_RACK = [[5422], [5430], [5438]]
CHALKBOARD = [[3276, 3277, 3278]]
HOTEL_VASE = [[7558], [7566]]


def _put_tf(L, name, x, y):
    rows, top = TF[name]
    H, W = L.shape[1:]
    for dy, row in enumerate(rows):
        for dx, t in enumerate(row):
            if not t:
                continue
            yy, xx = y + dy, x + dx
            if not (0 <= yy < H and 0 <= xx < W):
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
            yy, xx = y + dy, x + dx
            if not (0 <= yy < H and 0 <= xx < W):
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


def _put_lamp(L, x, y):
    """Warm turned walnut & brass rustic Ashkaar hearth stand/lantern (replaces sterile silver sci-fi pole!)."""
    H, W = L.shape[1:]
    if 0 <= y - 1 < H and 0 <= x < W:
        L[2, y - 1, x] = 2271
    if 0 <= y < H and 0 <= x < W:
        L[1, y, x] = 2279


def _put_stove(L, x, y, kettle=True):
    """Crackling cast-iron hearth stove with steaming kettle."""
    H, W = L.shape[1:]
    if 0 <= y - 1 < H and 0 <= x < W:
        L[2, y - 1, x] = 2470 if kettle else 2464
    if 0 <= y < H and 0 <= x < W:
        L[1, y, x] = 2478 if kettle else 2472


def _put_dressed_table(L, x, y, item_l=0, item_r=0):
    L[1, y, x] = 3466
    L[1, y, x + 1] = 3467
    L[1, y + 1, x] = 3474
    L[1, y + 1, x + 1] = 3475
    if item_l:
        L[2, y, x] = item_l
    if item_r:
        L[2, y, x + 1] = item_r


def _put_tree(L, x, y, style='parlor'):
    pairs = {'parlor': (5415, 5423), 'fern': (5431, 5439), 'ficus': (7126, 7134)}
    top_t, bot_t = pairs[style]
    H, W = L.shape[1:]
    if 0 <= y < H and 0 <= x < W:
        L[2, y, x] = top_t
    if 0 <= y + 1 < H and 0 <= x < W:
        L[1, y + 1, x] = bot_t


def _doormat(L, cx, y):
    H, W = L.shape[1:]
    for i, x in enumerate((cx - 1, cx, cx + 1)):
        if 0 <= y < H and 0 <= x < W:
            L[1, y, x] = 5512 + i


def _seam_stone_room(L, floor):
    """Auto-seam a volcanic-slate & stone room on Tileset 34 with ZERO void gaps."""
    H, W = floor.shape
    L[0, :, :] = VOID_34
    wall_face = np.zeros((H, W), dtype=bool)
    for y in range(1, H):
        for x in range(W):
            if floor[y, x] and not floor[y - 1, x]:
                for k in (1, 2):
                    if y - k >= 0 and not floor[y - k, x]:
                        wall_face[y - k, x] = True
    interior = floor | wall_face
    for y in range(H):
        for x in range(W):
            if floor[y, x]:
                top_row = (y == 0) or (not floor[y - 1, x])
                left_edge = (x == 0) or (not floor[y, x - 1])
                right_edge = (x + 1 >= W) or (not floor[y, x + 1])
                bot_edge = (y + 1 >= H) or (not floor[y + 1, x])
                ry = 0 if top_row else (2 if bot_edge else 1)
                rx = 0 if left_edge else (2 if right_edge else 1)
                L[0, y, x] = SLATE_STONE[ry][rx]
            elif wall_face[y, x]:
                is_lower = (y + 1 < H and floor[y + 1, x])
                left_end = (x == 0) or (not wall_face[y, x - 1])
                right_end = (x + 1 >= W) or (not wall_face[y, x + 1])
                if is_lower:
                    L[0, y, x] = 1219 if left_end else (1221 if right_end else 1220)
                else:
                    L[0, y, x] = 1211 if left_end else (1213 if right_end else 1212)
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


def _layers_to_palette_tiles(L):
    """Export a Tileset-34 (3,H,W) array into `palette: interior` ASCII grid + explicit tile list (for take_events!)."""
    H, W = L.shape[1:]
    grid_str = '\n'.join('.' * W for _ in range(H)) + '\n'
    tiles = []
    for z in range(3):
        for y in range(H):
            for x in range(W):
                t = int(L[z, y, x])
                if t > 0:
                    tiles.append({'tile': t, 'at': [x, y], 'layer': z})
    return grid_str, tiles


# =================================================================================================
# MAP 241 — Cindervault Pokémon Center (15x11, tileset 34, BGM Poke Center, HealingSpot)
# =================================================================================================
def build_241():
    W, H = 15, 11
    L = np.zeros((3, H, W), dtype=np.int32)
    floor = np.zeros((H, W), dtype=bool)
    floor[2:10, 1:14] = True
    floor[9, 1] = False
    floor[9, 13] = False
    floor[10, 6:9] = True
    _seam_stone_room(L, floor)

    # Warm Ashkaar timber hearth-lounge & Gale Post alcoves + crimson reception runner (ZERO blank slabs!)
    _put_9slice(L, HONEY_PARQUET, 1, 4, 4, 8, z=0, mask=floor)
    _put_9slice(L, HONEY_PARQUET, 10, 5, 13, 8, z=0, mask=floor)
    _put_9slice(L, HOTEL_CRIMSON_RUG, 6, 4, 8, 9, z=1, mask=floor)
    _doormat(L, 7, 10)

    # Volcanic stone north wall: crimson-draped window, Ashkaar tapestry, Town Map (12..13, 0..1)
    _put_grid(L, HOTEL_RED_WINDOW, 2, 0, z_rows=(1, 1))
    _put_grid(L, TAPESTRY_GOLD, 9, 0, z_rows=(1, 1))
    _put_grid(L, SEA_CHART, 12, 0, z_rows=(1, 1))

    # Healing Machine (4..5, 1..2 -> event at 5,2) & Ashkaar Crimson-Rose Reception Counter wrapping Nurse (7,2)
    _put_grid(L, HELP_HEAL, 4, 1, z_rows=(2, 1))
    L[1, 2, 8] = 7235
    for x, t in ((5, 7240), (6, 7241), (7, 7242), (8, 7243)):
        L[1, 3, x] = t

    # PC Console cleanly anchored at (11,2) (screen z=2 at (11,1), base z=1 at (11,2) -> player activates from (11,3)!)
    L[2, 1, 11] = 5847
    L[1, 2, 11] = 5855

    # SW Dressed Hearth Lounge Corner (kettle stove, dressed tea table, timber bench, kindling bucket, fern)
    _put_stove(L, 1, 4, kettle=True)
    L[1, 5, 1] = 4101                                       # Kindling oak bucket
    _put_dressed_table(L, 2, 5, 4528, 4537)                 # Steaming tea & spiced biscuits
    _put_grid(L, WOOD_BENCH, 1, 7, z_rows=(2, 1))
    _put_tree(L, 4, 8, 'fern')

    # SE Gale Post Desk & Reading Corner (keeps (12,2) Town Map approach & (11,3) PC approach 100% OPEN!)
    _put_grid(L, SHER_DESK, 11, 5, z_rows=(2, 1))           # Gale Post sorting desk (11..12, 5..6)
    L[2, 5, 11] = 3428                                      # Open Ashkaar dispatch ledger
    _put_grid(L, HOTEL_VASE, 13, 3, z_rows=(2, 1))
    _put_tf(L, 'crate_i', 11, 7)                            # Iron-strapped mail pouch crate cleanly on parquet!
    _put_lamp(L, 9, 8)                                      # Single warm indoor brass floor lamp (MAX 1!)

    # Save raw .npy and run passguard + BFS verification
    PG.guard(L, TID_INT, [(7, 10), (7, 9), (7, 2), (5, 2), (11, 2), (12, 1), (4, 6), (10, 6)], 'Map 241')
    _bfs_check_interior(L, (7, 10), [
        ('Doormat Arrival', (7, 9), False),
        ('Nurse Counter Talk', (7, 4), False),
        ('PC (11,2)', (11, 2), True),
        ('Town Map (12,1)', (12, 1), True),
        ('Ashkaar Traveler', (4, 6), True),
        ('Gale Post Desk', (10, 6), True),
    ], 'Map 241')

    raw_p = os.path.join(HERE, 'data', 'raw', '241.npy')
    os.makedirs(os.path.dirname(raw_p), exist_ok=True)
    np.save(raw_p, L.astype(np.int16))

    grid_str, tiles = _layers_to_palette_tiles(L)
    spec = {
        'id': 241,
        'name': 'Cindervault Pokémon Center',
        'parent': 240,
        'bgm': 'Poke Center',
        'metadata': {
            'HealingSpot': [240, 7, 21],
            'MapPosition': [0, 24, 8],
        },
        'tone': [12, 2, -10, 4],
        'biome': 'interior',
        'palette': 'interior',
        'map': grid_str,
        'tiles': tiles,
        'events': [
            {'type': 'exit', 'at': [7, 10], 'link': 'CV_PC', 'arrive': [7, 10, 'up']},
            _make_npc('Ashkaar Traveler', (4, 6), 'NPC 14', 'left', [
                "Ashkaar Traveler: Best kettle in Cindervault—you don't even have to light the grate under it when the caldera runs hot.",
                "Ashkaar Traveler: If you're heading into The Foundry, heal up first. Brann's Volcanic field makes Fire moves hit like a falling anvil.",
            ]),
            _make_npc('Gale Post Clerk', (10, 6), 'NPC 16', 'down', [
                "Gale Post Clerk: Gale Post — Cindervault Branch. Mail from the eastern passes has been thin since the Dominar's envoys rode in.",
                "Gale Post Clerk: Still sorting dispatches for the Hearthguild, though. Iron-sealed envelopes don't melt in the updrafts.",
            ]),
        ],
        'take_events': [
            {'template': 'pokecenter', 'name': 'Nurse', 'at': [7, 2]},
            {'template': 'pokecenter', 'name': 'Healing balls', 'at': [5, 2]},
            {'template': 'pokecenter', 'name': 'PC', 'at': [11, 2]},
            {'template': 'pokecenter', 'name': 'Town Map, size(2,1)', 'at': [12, 1]},
        ],
    }
    spec_p = os.path.join(HERE, 'specs', '241_cindervault_pc.yaml')
    with open(spec_p, 'w', encoding='utf-8') as f:
        f.write('# GENERATED by mapgen/layouts/cindervault_core.py (Ch8): Cindervault Pokémon Center.\n'
                '# Edit the layout script, not this file.\n')
        f.write(yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))
    print('Wrote specs/241_cindervault_pc.yaml and data/raw/241.npy')


# =================================================================================================
# MAP 242 — Cindervault Mart (12x10, tileset 34, BGM Poke Mart)
# =================================================================================================
def build_242():
    W, H = 12, 10
    L = np.zeros((3, H, W), dtype=np.int32)
    floor = np.zeros((H, W), dtype=bool)
    floor[2:9, 1:11] = True
    floor[8, 1] = False
    floor[8, 10] = False
    floor[9, 4:7] = True
    _seam_stone_room(L, floor)

    # Cozy volcanic-slate & warm timber Ashkaar supply floor + woven coir runner (ZERO raw red rug!)
    _put_9slice(L, HONEY_PARQUET, 4, 2, 9, 7, z=0, mask=floor)
    _put_9slice(L, BROWN_WOVEN_RUG, 4, 4, 6, 7, z=1, mask=floor)
    _doormat(L, 5, 9)

    # North wall: Ashkaar tapestry, crimson-draped window & unobstructed honest chalkboard price list (6..8,0)!
    _put_grid(L, TAPESTRY_GOLD, 1, 0, z_rows=(1, 1))
    _put_grid(L, HOTEL_RED_WINDOW, 4, 0, z_rows=(1, 1))
    _put_grid(L, CHALKBOARD, 6, 0, z_rows=(1,))

    # Warm crimson-rose marble checkout counter wrapping Clerk at (2,3) (counter flag 0x80 on (3,3) & (1..3,4)!)
    L[1, 2, 3] = 5835
    L[1, 3, 3] = 7235
    L[1, 4, 1] = 7240
    L[1, 4, 2] = 7241
    L[1, 4, 3] = 7243

    # Stocked smithing & fire-zone shelves, iron crates, quench-kegs & herb rack!
    _put_tf(L, 'shelf_goods', 9, 1)                         # 2x3 supply shelves (9..10, 1..3 -> cleanly clear of chalkboard!)
    _put_tf(L, 'shelf_bottles', 8, 5)                       # 2x2 Burn Heal & potion bottles (8..9, 5..6)
    _put_tf(L, 'crate_i', 1, 5)                             # 2x2 iron-bound smithing crate (1..2, 5..6)
    _put_tf(L, 'barrel_y', 1, 7)                            # Quench-oil keg (1, 7)
    _put_tf(L, 'barrel_b', 2, 7)                            # Fire-salt cask tucked beside quench keg (2, 7..8)
    _put_grid(L, HERB_RACK, 10, 4, z_rows=(2, 1, 1))        # Cooling herb rack (10, 4..6)
    L[1, 7, 10] = 4101                                      # Soot-oak bucket (10, 7)
    _put_lamp(L, 7, 8)                                      # Warm rustic dark-wood hearth stand (2271/2279)

    PG.guard(L, TID_INT, [(5, 9), (5, 8), (2, 3), (7, 6)], 'Map 242')
    _bfs_check_interior(L, (5, 9), [
        ('Doormat Arrival', (5, 8), False),
        ('Mart Counter Talk', (4, 3), False),
        ('Honest Shopper', (7, 6), True),
    ], 'Map 242')

    raw_p = os.path.join(HERE, 'data', 'raw', '242.npy')
    os.makedirs(os.path.dirname(raw_p), exist_ok=True)
    np.save(raw_p, L.astype(np.int16))

    spec = {
        'id': 242,
        'name': 'Cindervault Mart',
        'parent': 240,
        'bgm': 'Poke Mart',
        'metadata': {'MapPosition': [0, 24, 8]},
        'tone': [12, 2, -10, 4],
        'biome': 'interior',
        'tileset': TID_INT,
        'raw': 'data/raw/242.npy',
        'events': [
            {'type': 'exit', 'at': [5, 9], 'link': 'CV_MART', 'arrive': [5, 9, 'up']},
            {
                'type': 'mart',
                'name': 'Mart Clerk',
                'at': [2, 3],
                'sprite': 'NPC 19',
                'dir': 'right',
                'greeting': "Mart Clerk: Welcome to Cindervault Mart! Prices are high because of the war that isn't happening. What can I get you?",
                'items': [
                    'POKEBALL', 'GREATBALL', 'ULTRABALL',
                    'SUPERPOTION', 'HYPERPOTION',
                    'BURNHEAL', 'FULLHEAL', 'REVIVE',
                    'ESCAPEROPE', 'SUPERREPEL',
                ],
            },
            _make_npc('Honest Ashkaar Shopper', (7, 6), 'NPC 18', 'right', [
                "Shopper: 'PRICES HIGH BECAUSE OF THE WAR THAT ISN'T HAPPENING.'",
                "Shopper: Lying's a crime in Ashkaar, so you have to respect the sign. Still buying Burn Heals by the crate before four bells ring.",
            ]),
        ],
    }
    spec_p = os.path.join(HERE, 'specs', '242_cindervault_mart.yaml')
    with open(spec_p, 'w', encoding='utf-8') as f:
        f.write('# GENERATED by mapgen/layouts/cindervault_core.py (Ch8): Cindervault Mart.\n'
                '# Edit the layout script, not this file.\n')
        f.write(yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))
    print('Wrote specs/242_cindervault_mart.yaml and data/raw/242.npy')


def main():
    build_240()
    build_243()
    build_241()
    build_242()
    print('Done: wrote 240, 241, 242, 243 specs and raw .npy files.')


if __name__ == '__main__':
    main()
