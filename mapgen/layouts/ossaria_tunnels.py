#!/usr/bin/env python3
"""layouts/ossaria_tunnels.py — Batch 3F: Ossaria Static Tunnels Subterranean Corridor (2 Maps):
  - Map 604: Static Tunnels                   (44x40, TS 57 PF Rejuv Cave cvE, field :CAVE, DarkMap: true)
      * Old subterranean Meridian tram & high-voltage conduit tunnels boring beneath the Brass Dunes,
        linking 612 The Meridian Mainline (West portal) <-> 600 The Brass Dunes (East portal) and
        descending via twin ladders into 605 Static Tunnels Depths!
      * Features unified cv_rail_h tracks, stranded Tram Car No. 9 (canonical Ch6 inspect:
        "Destination board: DUNEHOLT. Underneath someone has scratched: 'EVENTUALLY.'"),
        glowing blue-gold power strips (lm_strip_h_on / lm_strip_v_on), humming generators (lm_gen),
        intact burning fw_brazier service braziers (L[2]==0 guard!), Conduit Relay Lever (S578),
        South Vault motorized shutter (lm_pdoor) unsealed cross-map by 605 Deep Breaker (S579),
        plus genuine Rock Smash & Strength boulder relic alcoves!
      * Canonical PBS trainers: [HIKER, Garrick] & [BURGLAR, Sly] (0 duplicates, 100% open sightlines!).
  - Map 605: Static Tunnels Depths            (36x34, TS 57 PF Rejuv Cave cvE, field :CAVE, DarkMap: true)
      * Deep subterranean static transformer & sandstone cavern beneath 604 Static Tunnels,
        linked bidirectionally by twin ladders (Main South Shaft & SW Service Shaft).
      * Elevated North Deep-Breaker Sanctum (TER) housing the Deep Conduit Breaker (S579)
        controlling Map 604's Conduit Vault shutter, glowing conduit grid, subterranean cooling pool,
        Rock Smash & Strength boulder relic alcoves, and intact burning braziers!
      * Canonical PBS trainer: [POKEMANIAC, Otho] (0 duplicates, 100% open sightline!).

Canonical sources:
  - design/maps.json (604 44x40, 605 36x34, DarkMap Flash cave, town_map_pos [0, 15, 4])
  - design/DUNGEON_PUZZLES.md (reserved block 576-600 -> S578, S579 — 0 collisions!)
  - story/25_SCRIPT_CH6.md (lines 167-171: dead tram cars, live cables, Tram Car No. 9)
  - pbs/trainers.txt (# Map 604 Garrick, Sly; # Map 605 Otho)

Run:
    /usr/bin/python3 -I mapgen/layouts/ossaria_tunnels.py
"""
import os
import sys
from collections import deque
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cavekit import Cave, FLOOR, TER, MASS, P1
import rkit as K
from rkit import STAMPS
import rcompose as RC
import render as R
import passguard as PG
from ossaria_landmarks import (
    TID_CAVE,
    T_PDOOR,
    T_PDOOR_OPEN,
    T_LEVER_L,
    T_LEVER_R,
    _place_stamp_over,
    _make_npc,
    _sign,
    _trainer_cave,
    _strength_boulder,
    _rock_smash,
    _paint_sandstone_floors,
    _assert_braziers_intact,
    _assert_no_over_trigger,
)
from duneholt_interiors import (
    _add_safe_overlay,
    _verify_all_events_and_trainers,
)

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POS_TUN = [0, 15, 4]

# Reserved dungeon switches (design/DUNGEON_PUZZLES.md block 576-600 — verified 0 collisions!)
S_TUN_RELAY = 578    # 604 North Relay Lever toggled (boosts conduit power & opens north relay locker)
S_TUN_BREAKER = 579  # 605 Deep Conduit Breaker toggled -> opens 604 South Conduit Vault shutter!


def _strength_boulder_touch(name, at):
    """Pushable desert sandstone Strength boulder (pf_cave_boulder_E) with smooth touch trigger."""
    b = _strength_boulder(name, at)
    b['pages'][0]['trigger'] = 'touch'
    return b


def _paint_conduit_floors(m, zones):
    """Paint specialized Zenith subterranean floor tiles (slate road, industrial Z/Q pads, sandstone) on FLOOR/TER."""
    palettes = {
        'sand': [P1('E_f%d' % i) for i in range(4)],
        'plaza': [P1('lm_plaza0'), P1('lm_plaza1')],
        'road': [P1('lm_road0'), P1('lm_road1')],
        'panel': [P1('Z_f%d' % i) for i in range(4)],
        'grate': [P1('Q_f%d' % i) for i in range(4)],
    }
    floorpatch_ids = {P1(k) for k in STAMPS if k.startswith(('E_floorpatch_', 'E_fd'))}
    for x0, y0, x1, y1, kind in zones:
        pal = palettes[kind]
        for y in range(max(0, y0), min(m.H, y1 + 1)):
            for x in range(max(0, x0), min(m.W, x1 + 1)):
                if m.cls[y, x] != '.' or m.cliff[y, x]:
                    continue
                if int(m.L[1, y, x]) in floorpatch_ids:
                    m.L[1, y, x] = 0
                m.L[0, y, x] = pal[(x * 3 + y * 5) % len(pal)]


def _paint_strip_h(m, x0, x1, y, on=True):
    t = P1('lm_strip_h_on' if on else 'lm_strip_h')
    floorpatch_ids = {P1(k) for k in STAMPS if k.startswith(('E_floorpatch_', 'E_fd'))}
    for x in range(x0, x1 + 1):
        if m.inb(x, y) and m.cls[y, x] == '.' and not m.cliff[y, x] and not m.taken[y, x]:
            m.L[0, y, x] = t
            if int(m.L[1, y, x]) in floorpatch_ids:
                m.L[1, y, x] = 0


def _paint_strip_v(m, x, y0, y1, on=True):
    t = P1('lm_strip_v_on' if on else 'lm_strip_v')
    floorpatch_ids = {P1(k) for k in STAMPS if k.startswith(('E_floorpatch_', 'E_fd'))}
    for y in range(y0, y1 + 1):
        if m.inb(x, y) and m.cls[y, x] == '.' and not m.cliff[y, x] and not m.taken[y, x]:
            m.L[0, y, x] = t
            if int(m.L[1, y, x]) in floorpatch_ids:
                m.L[1, y, x] = 0


def _paint_rail_h(m, x0, x1, y):
    t = P1('cv_rail_h')
    for x in range(x0, x1 + 1):
        if m.inb(x, y) and m.cls[y, x] == '.' and not m.cliff[y, x] and not m.taken[y, x]:
            m.L[1, y, x] = t


def _exact_bfs_cave(Lr, tid, events, start):
    import build as B
    ts = R.tilesets()[tid]
    H, W = Lr.shape[1:]
    solid_ev = set()
    for e in events:
        et = e.get('type')
        if et in ('npc', 'trainer', 'mart', 'rock_smash'):
            solid_ev.add(tuple(e['at']))
        elif et == 'event':
            pg0 = (e.get('pages') or [{}])[0]
            g0 = pg0.get('graphic') or {}
            if not pg0.get('through') and (g0.get('sprite') or (g0.get('tile') and (ts['passages'][g0['tile']] & 0x0f) == 0x0f)):
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

    sx, sy = start
    assert ok[sy, sx], f'Cave BFS start {start} is blocked!'
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
    return seen


# =================================================================================================
# 1. MAP 604 — STATIC TUNNELS (44x40, TS 57 PF Rejuv Cave cvE, field :CAVE, DarkMap: true)
# =================================================================================================
def build_604():
    W, H = 44, 40
    m = Cave(W, H, 'E', seed=604, pool='Cave Pool', tid=TID_CAVE)
    m.STAIRS = (P1('E_stairl'), P1('E_stairm'), P1('E_stairr'))
    m.kit = {MASS: 'cvE', TER: 'cvE', FLOOR: 'cvE', 'default': 'cvE'}

    # ---- 1. Carve Multi-Tiered Sandstone & Conduit Service Tunnel (44x40, cvE 3-row cliffs!) ----
    # West Entry Tunnel from 612 The Meridian Mainline (FLOOR): x=2..12, y=16..23 -> walkable x=3..12, y=19..23!
    m.box(2, 16, 12, 23, FLOOR, '.')
    # Central Tramway Gallery housing stranded Tram Car No. 9 (FLOOR): x=11..32, y=13..25
    m.box(11, 13, 32, 25, FLOOR, '.')
    # East Exit Tunnel to 600 The Brass Dunes (FLOOR): x=31..41, y=16..23 -> walkable x=31..40, y=19..23!
    m.box(31, 16, 41, 23, FLOOR, '.')

    # North Elevated High-Voltage Relay Terrace (TER): x=10..33, y=3..12 (walkable y=6..11; stairs at y=12..14!)
    m.box(10, 3, 33, 12, TER, '.')
    # Sealed NW Relay Supply Locker (TER) gated by S578 at 1-tile throat (9, 8) -> chamber x=3..8, y=4..10!
    m.box(9, 6, 10, 8, TER, '.')
    m.box(3, 4, 8, 10, TER, '.')

    # South Maintenance Gallery & Cooling Cistern (FLOOR): x=10..33, y=25..31
    m.box(10, 25, 33, 31, FLOOR, '.')
    # SW Ladder Vestibule down to 605 Depths SW return shaft (FLOOR): x=10..15, y=31..35
    m.box(10, 31, 15, 35, FLOOR, '.')
    # SE Maintenance Alcove approach (FLOOR): x=28..33, y=31..34
    m.box(28, 31, 33, 34, FLOOR, '.')

    # Sealed South-Central Conduit Vault (FLOOR): 2-wide throat x=21..22, y=31..33 -> chamber x=19..24, y=34..37
    m.box(21, 31, 22, 34, FLOOR, '.')
    m.box(19, 34, 24, 37, FLOOR, '.')

    # SW Rock Smash Relic Alcove: 1-tile walkable throat (9, 29) -> rear pocket x=4..8, y=27..31 (guards THUNDERSTONE!)
    m.box(9, 27, 10, 29, FLOOR, '.')
    m.box(4, 27, 8, 31, FLOOR, '.')

    # SE Strength Boulder Relic Alcove: 1-tile walkable throat (34, 29) -> rear pocket x=35..39, y=27..31 (guards MAGNET!)
    m.box(33, 27, 34, 29, FLOOR, '.')
    m.box(35, 27, 39, 31, FLOOR, '.')

    # Sculpted cavern chamfers (strictly clear of all corridors, portals, stairs, and alcoves!)
    m.mass_at([
        (2, 16), (2, 23), (41, 16), (41, 23),
        (10, 3), (33, 3), (19, 37), (24, 37), (3, 4),
    ])

    # Central-South Subterranean Cooling Cistern (x=19..24, y=27..29 -> navigable ring around it!)
    m.box(19, 27, 24, 29, FLOOR, 'w')

    # Twin 3-wide Sandstone Staircases ascending North onto the High-Voltage Relay Terrace
    m.stairs(14, 12, w=3, n=3, c='.')
    m.stairs(27, 12, w=3, n=3, c='.')
    m.plan_cliffs(rows=3)

    # ---- 2. Events: Bidirectional Warps (612, 600, 605x2), Tram Car 9, Relay S578 + Shutter, Vault S579, 2 Trainers! ----
    E = m.events

    # West Portal -> 612 The Meridian Mainline (118, 20, down)
    for wy in (19, 20, 21):
        E.append({
            'type': 'warp',
            'name': 'West to The Meridian Mainline' + (' ' * (wy - 19)),
            'at': [3, wy],
            'to': {'map': 612, 'x': 118, 'y': 20, 'dir': 'down'},
            'se': 'Door exit',
        })

    # East Portal -> 600 The Brass Dunes (24, 22, down)
    for ey in (19, 20, 21):
        E.append({
            'type': 'warp',
            'name': 'East to The Brass Dunes' + (' ' * (ey - 19)),
            'at': [40, ey],
            'to': {'map': 600, 'x': 24, 'y': 22, 'dir': 'down'},
            'se': 'Door exit',
        })

    # North-East Ladder Down -> 605 Static Tunnels Depths (18, 28, up)
    E.append({
        'type': 'warp',
        'name': 'Ladder Down to Static Tunnels Depths',
        'at': [30, 7],
        'to': {'map': 605, 'x': 18, 'y': 28, 'dir': 'up'},
        'se': 'Door enter',
    })

    # South-West Ladder Down -> 605 Static Tunnels Depths (7, 27, down)
    E.append({
        'type': 'warp',
        'name': 'West Service Ladder to Depths',
        'at': [12, 33],
        'to': {'map': 605, 'x': 7, 'y': 27, 'dir': 'down'},
        'se': 'Door enter',
    })

    # Stranded Tram Car No. 9 (lm_tram 5x2 at (18, 17..18) -> solid base (20, 18), pas=0xf!)
    # Canonical story/25_SCRIPT_CH6.md line 170!
    E.append(_sign(
        'Tram Car No. 9', (20, 18),
        "TRAM CAR No. 9 — An abandoned Meridian subterranean tram car half-choked with drifted sand. Destination board: DUNEHOLT. Underneath, someone has scratched: 'EVENTUALLY.'"
    ))

    # Tunnel Service Plaque on solid pf_roadstone base (7, 22) — cleanly SOUTH of y=18 rail so rail runs unbroken!
    E.append(_sign(
        'Static Tunnels Conduit Plaque', (7, 22),
        "MERIDIAN SUB-DUNE CONDUIT 04 — High-voltage tram feeder. WARNING: Static build-up attracts Joltik & Magnemite in the dark. Auxiliary Relay 04 controls the NW Supply Locker; Deep Vault breaker sits one level down."
    ))

    # North Terrace Conduit Relay Lever (S578) — genuinely unseals NW Relay Supply Shutter at (9, 8)!
    relay_ruby = (
        f's = !$game_switches[{S_TUN_RELAY}]\n'
        f'$game_switches[{S_TUN_RELAY}] = s\n'
        'pbSEPlay("Strength push", 85, 105)\n'
        'pfm_shake(1, 6, 8)\n'
        '$game_map.need_refresh = true\n'
        'if s\n'
        '  pbMessage(_INTL("CLACK-BZZT! Auxiliary Conduit Relay 04 engages! A cyan surge races west along the bus-bar — unsealing the Northwest Relay Supply Locker!"))\n'
        '  if !$game_switches[579]\n'
        '    pbMessage(_INTL("(A red indicator still blinks on the monitor bank: SOUTH CONDUIT VAULT LOCKED — RESET DEEP BREAKER ON B1F DEPTHS.)"))\n'
        '  end\n'
        'else\n'
        '  pbMessage(_INTL("CLACK! You disengage Auxiliary Conduit Relay 04; the Northwest Relay Supply Locker shutter drops shut again."))\n'
        'end'
    )
    E.append({
        'type': 'event',
        'name': 'Conduit Relay Lever (S578)',
        'at': [21, 7],
        'pages': [
            {'graphic': {'tile': T_LEVER_L}, 'trigger': 'action', 'commands': [{'script': relay_ruby}]},
            {'cond': {'switch': S_TUN_RELAY}, 'graphic': {'tile': T_LEVER_R}, 'trigger': 'action', 'commands': [{'script': relay_ruby}]},
        ],
    })

    # REAL Mechanical S578 Motorized Shutter gating NW Relay Supply Locker at (9, 8)!
    E.append({
        'type': 'event',
        'name': 'Relay Supply Locker Shutter',
        'at': [9, 8],
        'pages': [
            {
                'graphic': {'tile': T_PDOOR},
                'trigger': 'action',
                'commands': [
                    "NORTHWEST RELAY SUPPLY LOCKER — Sealed by an electromagnetic latch. Follow the cyan floor conduit east to Auxiliary Conduit Relay 04.",
                ],
            },
            {
                'cond': {'switch': S_TUN_RELAY},
                'graphic': {'tile': T_PDOOR_OPEN},
                'through': True,
                'commands': [],
            },
        ],
    })

    # REAL Cross-Map S579 Motorized Bulkhead Shutter gating South Conduit Vault ((21..22, 33))!
    for vx in (21, 22):
        E.append({
            'type': 'event',
            'name': 'Conduit Vault Shutter' + (' ' if vx == 22 else ''),
            'at': [vx, 33],
            'pages': [
                {
                    'graphic': {'tile': T_PDOOR},
                    'trigger': 'action',
                    'commands': [
                        "CONDUIT VAULT BULKHEAD — Locked tight by an electromagnetic latch. The red copper bus-bar runs north toward the ladder descending into Static Tunnels Depths.",
                    ],
                },
                {
                    'cond': {'switch': S_TUN_BREAKER},
                    'graphic': {'tile': T_PDOOR_OPEN},
                    'through': True,
                    'commands': [],
                },
            ],
        })

    # Stranded Meridian Linesman NPC near West Entry (gives helpful Flash / Depths hint!)
    E.append(_make_npc(
        'Meridian Linesman', (9, 22), 'trainer_ENGINEER', 'up',
        [
            "Linesman: Watch your step in the dark — Flash helps a lot down here, and the live floor cables hum loud enough to make your hair stand up!",
            "Linesman: Meridian dug these tram tunnels straight under the Brass Dunes, then abandoned Car No. 9 when the sand broke through the roof vents.",
            "Linesman: Throw the Relay Lever up on the north deck for the supply locker, or climb down the northeast ladder to the Depths for the South Vault breaker!",
        ],
    ))

    # Canonical PBS Trainers (# Map 604: [HIKER, Garrick] & [BURGLAR, Sly] — 100% open sightlines!)
    E.append(_trainer_cave(
        (15, 23), 'HIKER', 'Garrick', 'up',
        "Hiker Garrick: Pitch-black tunnel, sparks flying off the rails — best training ground between Lumen and Duneholt!",
        "Hiker Garrick: Can't see my hand down here. Saw that coming, though.",
        sight=3,
    ))
    E.append(_trainer_cave(
        (28, 17), 'BURGLAR', 'Sly', 'down',
        "Burglar Sly: Hey, keep your flashlight off my salvage! Meridian left miles of copper conduit down here and I saw it first!",
        "Burglar Sly: Copper wire's worth good money. You're worth trouble.",
        sight=3,
    ))

    # Rock Smash & Touch-Trigger Strength Alcove Barriers
    E.append(_rock_smash((9, 29), 'Cracked Conduit Rock'))
    E.append(_strength_boulder_touch('Tunnel Boulder', (34, 29)))

    # Verified Pickups (including S578 NW Relay Locker rewards at (5, 7) & (7, 7)!)
    E += [
        {'type': 'item', 'at': [5, 7], 'item': 'METALCOAT', 'name': 'Relay Locker Metal Coat'},
        {'type': 'item', 'at': [7, 7], 'item': 'SUPERREPEL', 'name': 'Relay Locker Super Repel'},
        {'type': 'item', 'at': [6, 30], 'item': 'THUNDERSTONE', 'name': 'Tunnel Thunder Stone'},
        {'type': 'item', 'at': [38, 30], 'item': 'MAGNET', 'name': 'Tunnel Magnet'},
        {'type': 'item', 'at': [20, 35], 'item': 'CELLBATTERY', 'name': 'Vault Cell Battery'},
        {'type': 'item', 'at': [23, 35], 'item': 'ULTRABALL', 'name': 'Vault Ultra Ball'},
        {'type': 'item', 'at': [33, 27], 'item': 'ESCAPEROPE', 'name': 'Tunnel Escape Rope'},
        {'type': 'item', 'at': [25, 29], 'item': 'STARPIECE', 'hidden': True, 'name': 'HiddenItem (cistern rubble)'},
    ]

    for e in E:
        m.keep_clear.add(tuple(e['at']))
    for pt in [(4, 20), (5, 20), (6, 20), (38, 20), (39, 20), (30, 8), (12, 34),
               (15, 20), (15, 21), (15, 22), (28, 18), (28, 19), (28, 20),
               (9, 8), (10, 8), (8, 8), (6, 7), (6, 8), (7, 8),
               (21, 32), (22, 32), (21, 34), (22, 34), (35, 29), (36, 29), (8, 29)]:
        m.keep_clear.add(pt)

    # ---- 3. Subterranean Tramway Architecture: Car No. 9, Generators, Monitors, Ladders & Intact Braziers! ----
    _place_stamp_over(m, 'lm_tram', 18, 17, base_z=1, top_z=2, top_rows=1, solid=True)
    # Plaque cleanly south of y=18 rail at (7, 21..22) (base (7, 22)!)
    _place_stamp_over(m, 'pf_roadstone', 7, 21, base_z=1, top_z=2, top_rows=1, solid=True)

    # Twin bidirectional ladders (passable cv_ladder base -> solid=False!)
    _place_stamp_over(m, 'cv_ladder', 30, 6, base_z=1, top_z=2, top_rows=1, solid=False)
    _place_stamp_over(m, 'cv_ladder', 12, 32, base_z=1, top_z=2, top_rows=1, solid=False)

    # North High-Voltage Relay Substation & NW Relay Locker props
    _place_stamp_over(m, 'lm_gen', 17, 6, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'lm_gen', 24, 6, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'lm_monitors', 20, 5, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'wr_sacks', 4, 9, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'cv_cart', 13, 18, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'cv_cart', 32, 18, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'wr_supply', 24, 21, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'wr_sacks', 12, 24, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'wr_sandbags', 31, 24, base_z=1, top_z=1, top_rows=0, solid=True)
    for cx, cy in ((13, 6), (28, 6), (17, 26), (26, 26), (19, 35), (24, 35)):
        _place_stamp_over(m, 'nr_col', cx, cy, base_z=1, top_z=2, top_rows=1, solid=True)
    for ex, ey in ((5, 22), (35, 22), (11, 29), (32, 29)):
        _place_stamp_over(m, 'E_stal', ex, ey, base_z=1, top_z=2, top_rows=1, solid=True)

    braziers_604 = [
        (5, 18), (11, 16), (32, 16), (38, 18),
        (16, 10), (27, 10),
        (16, 29), (27, 29),
        (14, 33), (21, 35),
    ]
    for bx, by in braziers_604:
        _place_stamp_over(m, 'fw_brazier', bx, by, base_z=1, top_z=2, top_rows=1, solid=True)

    m.paint()
    _paint_conduit_floors(m, [
        (3, 19, 40, 21, 'road'),
        (12, 16, 31, 24, 'sand'),
        (11, 6, 32, 11, 'panel'),
        (17, 6, 26, 10, 'grate'),
        (4, 6, 8, 10, 'panel'),
        (5, 7, 7, 9, 'grate'),
        (19, 34, 24, 37, 'plaza'),
        (10, 31, 15, 35, 'road'),
    ])

    # Unbroken Unified Iron Tram Rails (y=18 leading cleanly into/out of Tram Car No. 9!) & Glowing Cyan Conduit Strips!
    _paint_rail_h(m, 4, 17, 18)
    _paint_rail_h(m, 23, 39, 18)
    _paint_strip_h(m, 4, 39, 20, on=True)
    _paint_strip_h(m, 14, 29, 9, on=True)
    # Visual cyan feeder connecting Relay Lever (21, 7) bus-bar seamlessly west into NW Relay Locker Shutter (9, 8)!
    _paint_strip_h(m, 5, 15, 8, on=True)
    _paint_strip_v(m, 15, 8, 20, on=True)
    _paint_strip_v(m, 28, 10, 20, on=True)
    _paint_strip_v(m, 16, 21, 30, on=True)
    _paint_strip_v(m, 27, 21, 30, on=True)
    _paint_strip_h(m, 16, 27, 30, on=True)

    Lr = RC.resolve(m.L, TID_CAVE).astype(np.int32)
    # Clean, unbroken subterranean vent shafts strictly on open floor/cistern — ZERO offset/chopped pf_glow orbs!
    _add_safe_overlay(Lr, TID_CAVE, 'cv_shaft', [(24, 15), (21, 25)])
    _assert_braziers_intact(Lr, TID_CAVE, braziers_604, 'Map 604')

    ev_pts = [tuple(e['at']) for e in E]
    PG.guard(Lr, TID_CAVE, ev_pts, 'Map 604')
    assert not PG.hits(Lr, R.tilesets()[TID_CAVE], ev_pts), 'Map 604 passguard hits!'
    _assert_no_over_trigger(Lr, TID_CAVE, E, 'Map 604')

    # Dual-state BFS verification: sealed vs S578-only vs full unlock (S578 + S579 + Rock Smash + Strength)!
    relay_items = {(5, 7), (7, 7)}
    other_gated = {(6, 30), (38, 30), (20, 35), (23, 35)}
    gated_items = relay_items | other_gated
    main_events = [e for e in E if tuple(e['at']) not in gated_items and (e.get('name') or '') != 'Tunnel Boulder']
    _verify_all_events_and_trainers(Lr, TID_CAVE, main_events, (5, 20), 'Map 604 [TRAINERS + MAIN]')

    seen_sealed = _exact_bfs_cave(Lr, TID_CAVE, E, (5, 20))
    assert any((34 + dx, 29 + dy) in seen_sealed for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))), 'Map 604: Tunnel Boulder unreachable!'
    for gp in gated_items:
        assert gp not in seen_sealed and not any((gp[0] + dx, gp[1] + dy) in seen_sealed for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))), (
            f'Map 604 LEAK: gated item {gp} reachable while sealed!'
        )
    assert (38, 20) in seen_sealed and (30, 7) in seen_sealed and (12, 33) in seen_sealed, 'Map 604 main warps unreachable!'

    # Prove S578 specifically unlocks NW Relay Supply Locker ((5, 7) & (7, 7)) while other 4 remain sealed!
    s578_events = [
        ({**e, 'pages': [e['pages'][1]]} if (e.get('name') or '') == 'Relay Supply Locker Shutter' else e)
        for e in E
    ]
    seen_s578 = _exact_bfs_cave(Lr, TID_CAVE, s578_events, (5, 20))
    for gp in relay_items:
        assert any((gp[0] + dx, gp[1] + dy) in seen_s578 for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))), (
            f'Map 604: S578 locker item {gp} NOT reachable after S578!'
        )
    for gp in other_gated:
        assert gp not in seen_s578 and not any((gp[0] + dx, gp[1] + dy) in seen_s578 for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))), (
            f'Map 604 LEAK: non-S578 item {gp} unlocked prematurely by S578!'
        )

    unlocked_events = []
    for e in E:
        nm = e.get('name') or ''
        if e.get('type') == 'rock_smash':
            continue
        if nm == 'Tunnel Boulder':
            unlocked_events.append({**e, 'at': [36, 29]})
        elif nm.startswith('Conduit Vault Shutter') or nm == 'Relay Supply Locker Shutter':
            unlocked_events.append({**e, 'pages': [e['pages'][1]]})
        else:
            unlocked_events.append(e)
    seen_open = _exact_bfs_cave(Lr, TID_CAVE, unlocked_events, (5, 20))
    for gp in gated_items:
        assert any((gp[0] + dx, gp[1] + dy) in seen_open for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))), (
            f'Map 604: gated item {gp} NOT reachable after unlock!'
        )
    print(f'Map 604 Dual-State Proof PASSED: sealed={len(seen_sealed)}, S578={len(seen_s578)}, open={len(seen_open)} cells!')

    m.L = Lr
    head = {
        'id': 604,
        'name': 'Static Tunnels',
        'parent': 600,
        'bgm': 'Cave',
        'field': 'CAVE',
        'map_audio': {'bgm': 'Route - Nadir', 'bgs': 'Machinery - Zenith', 'bgs_volume': 50, 'rain': False},
        'fog': {'name': 'prismfall_cave', 'opacity': 26, 'blend': 1, 'zoom': 100, 'sx': 1, 'sy': 0},
        'metadata': {
            'Name': 'Static Tunnels',
            'Outdoor': False,
            'ShowArea': True,
            'BattleBack': 'cave1',
            'DarkMap': True,
            'MapPosition': POS_TUN,
        },
        'gates': [
            {
                'name': 'Static Tunnels Relay Locker (S578), Vault (S579) & Field Move Alcoves',
                'from': [[5, 20]],
                'sealed': [[5, 7], [7, 7], [6, 30], [38, 30], [20, 35], [23, 35]],
            },
        ],
        'tone': [-18, -16, -6, 18],
        '_file': '604_static_tunnels.yaml',
    }
    m.write(604, head, comment='# GENERATED by mapgen/layouts/ossaria_tunnels.py: Static Tunnels (604).\n')
    print('Wrote specs/604_static_tunnels.yaml and data/raw/604.npy')


# =================================================================================================
# 2. MAP 605 — STATIC TUNNELS DEPTHS (36x34, TS 57 PF Rejuv Cave cvE, field :CAVE, DarkMap: true)
# =================================================================================================
def build_605():
    W, H = 36, 34
    m = Cave(W, H, 'E', seed=605, pool='Cave Pool', tid=TID_CAVE)
    m.STAIRS = (P1('E_stairl'), P1('E_stairm'), P1('E_stairr'))
    m.kit = {MASS: 'cvE', TER: 'cvE', FLOOR: 'cvE', 'default': 'cvE'}

    # ---- 1. Carve Subterranean Static Transformer Vault (36x34, cvE 3-row cliffs!) ----
    # South Main Entry Vestibule (FLOOR): x=14..21, y=24..31 (Main Ladder up -> 604 at (18, 30)!)
    m.box(14, 24, 21, 31, FLOOR, '.')
    # Central Static Transformer Cavern (FLOOR): x=10..26, y=13..24 (meets TER y=12 for 4-wide stair!)
    m.box(10, 13, 26, 24, FLOOR, '.')
    # West Service Wing & SW Return Ladder (FLOOR): x=6..11, y=16..28 (SW Ladder up -> 604 at (7, 26)!)
    m.box(6, 16, 11, 28, FLOOR, '.')
    # East Collector Gallery (FLOOR): x=25..31, y=14..23 (Trainer Otho!)
    m.box(25, 14, 31, 23, FLOOR, '.')
    # North Elevated Deep-Breaker Sanctum (TER): x=10..25, y=4..12
    m.box(10, 4, 25, 12, TER, '.')

    # NW Rock Smash Alcove: 1-tile walkable throat (5, 18) -> pocket x=2..4, y=16..18 (guards STARPIECE at (3,18)!)
    m.box(5, 16, 6, 18, FLOOR, '.')
    m.box(2, 16, 4, 18, FLOOR, '.')

    # SW Strength Boulder Magnetite Inner Sanctum: 1-tile throat (5, 24) -> chamber x=2..4, y=22..28 (guards :STEELIUMZ & MAXETHER!)
    m.box(5, 22, 6, 24, FLOOR, '.')
    m.box(2, 22, 4, 28, FLOOR, '.')

    # Clean chamfers (removed broken east cliff tooth (24,13)/(25,13)!)
    m.mass_at([
        (10, 4), (25, 4), (14, 31), (21, 31),
        (31, 14), (31, 23), (6, 28), (11, 28),
    ])

    # Central Static Cooling Pool (x=16..19, y=18..20)
    m.box(16, 18, 19, 20, FLOOR, 'w')

    # Grand 4-wide Sandstone Staircase ascending North to the Deep-Breaker Sanctum
    m.stairs(16, 12, w=4, n=3, c='.')
    m.plan_cliffs(rows=3)

    # ---- 2. Events: Twin Bidirectional Ladders -> 604, Deep Breaker S579, :STEELIUMZ Altar, Trainer Otho & Pickups! ----
    E = m.events

    # Main South Ladder Up -> 604 Static Tunnels (30, 8, down)
    E.append({
        'type': 'warp',
        'name': 'Main Ladder Up to Static Tunnels',
        'at': [18, 30],
        'to': {'map': 604, 'x': 30, 'y': 8, 'dir': 'down'},
        'se': 'Door exit',
    })

    # SW Service Ladder Up -> 604 Static Tunnels (12, 34, down)
    E.append({
        'type': 'warp',
        'name': 'West Service Ladder Up to Static Tunnels',
        'at': [7, 26],
        'to': {'map': 604, 'x': 12, 'y': 34, 'dir': 'down'},
        'se': 'Door exit',
    })

    # Deep Conduit Breaker (S579 — Pyrous cross-map unlock of Map 604's South Conduit Vault!)
    breaker_ruby = (
        f's = !$game_switches[{S_TUN_BREAKER}]\n'
        f'$game_switches[{S_TUN_BREAKER}] = s\n'
        'pbSEPlay("Mining reveal", 90, 95)\n'
        'pfm_shake(2, 8, 12)\n'
        '$game_map.need_refresh = true\n'
        'if s\n'
        '  pbMessage(_INTL("KRA-THOOM! The Deep Conduit Breaker slams closed! A blue surge races up the ceiling bus-bars — unsealing the South Conduit Vault on the upper level of Static Tunnels!"))\n'
        'else\n'
        '  pbMessage(_INTL("CLANK! You trip the Deep Conduit Breaker back to standby; the upper Conduit Vault bulkhead drops shut again."))\n'
        'end'
    )
    E.append({
        'type': 'event',
        'name': 'Deep Conduit Breaker (S579)',
        'at': [18, 7],
        'pages': [
            {'graphic': {'tile': T_LEVER_L}, 'trigger': 'action', 'commands': [{'script': breaker_ruby}]},
            {'cond': {'switch': S_TUN_BREAKER}, 'graphic': {'tile': T_LEVER_R}, 'trigger': 'action', 'commands': [{'script': breaker_ruby}]},
        ],
    })

    # Canonical :STEELIUMZ Magnetite Seam Z-Crystal Altar (plugins/Prismfall Mega/001_Mega_Config.rb:128!)
    # Seated on solid mn_plinth at (3, 27) inside the SW Strength Boulder inner sanctum!
    steelium_ruby = (
        'if $bag && $bag.has?(:STEELIUMZ)\n'
        '  pbMessage(_INTL("The humming magnetite seam rests dark and still where the cold silver-grey Z-Crystal once lay."))\n'
        'elsif defined?(pf_z_crystal)\n'
        '  pbSEPlay("Mining reveal", 95, 110)\n'
        '  if pf_z_crystal(:STEELIUMZ, "Wedged deep in the humming magnetite seam sits a faceted shard of cold silver-grey crystal — it answers your Flash with a low metallic ring!")\n'
        '    $game_self_switches[[605, @event_id, "A"]] = true\n'
        '    $game_map.need_refresh = true\n'
        '  end\n'
        'else\n'
        '  pbSEPlay("Mining reveal", 95, 110)\n'
        '  pbMessage(_INTL("Wedged deep in the humming magnetite seam sits a faceted shard of cold silver-grey crystal — it answers your Flash with a low metallic ring!"))\n'
        '  if pbReceiveItem(:STEELIUMZ, 1)\n'
        '    $game_self_switches[[605, @event_id, "A"]] = true\n'
        '    $game_map.need_refresh = true\n'
        '  end\n'
        'end'
    )
    E.append({
        'type': 'event',
        'name': 'Z-Crystal: STEELIUMZ',
        'at': [3, 27],
        'pages': [
            {'trigger': 'action', 'commands': [{'script': steelium_ruby}]},
            {'cond': {'self': 'A'}, 'trigger': 'action', 'commands': [
                "The humming magnetite seam rests dark and still where the cold silver-grey Z-Crystal once lay.",
            ]},
        ],
    })

    # Lore Stele on North Sanctum (pf_roadstone base (14, 7))
    E.append(_sign(
        'Deep Grid Survey Stele', (14, 7),
        "MERIDIAN SUB-GRID LOG (AF 296): 'Earth conductivity spikes sharply beneath the southwest boulder pocket — raw magnetite seams ring like struck iron under lamp-light. Deep Breaker controls upper Vault bulkhead.'"
    ))

    # Canonical PBS Trainer (# Map 605: [POKEMANIAC, Otho] — 100% open sightline!)
    E.append(_trainer_cave(
        (26, 20), 'POKEMANIAC', 'Otho', 'left',
        "Poké Maniac Otho: Everyone stops at the tram tracks upstairs! Down here where the static hums, the real rare Pokémon nest — let's test yours!",
        "Poké Maniac Otho: The rare ones live deeper. So does my disappointment.",
        sight=3,
    ))

    # Rock Smash & Touch-Trigger Strength Alcoves (1-tile throats at x=5!)
    E.append(_rock_smash((5, 18), 'Cracked Bedrock'))
    E.append(_strength_boulder_touch('Depths Boulder', (5, 24)))

    # Verified Pickups
    E += [
        {'type': 'item', 'at': [3, 18], 'item': 'STARPIECE', 'name': 'Depths Star Piece'},
        {'type': 'item', 'at': [2, 25], 'item': 'MAXETHER', 'name': 'Depths Max Ether'},
        {'type': 'item', 'at': [22, 7], 'item': 'HYPERPOTION', 'name': 'Sanctum Hyper Potion'},
        {'type': 'item', 'at': [30, 16], 'item': 'DUSKBALL', 'name': 'Depths Dusk Ball'},
        {'type': 'item', 'at': [9, 22], 'item': 'RAREBONE', 'name': 'Depths Rare Bone'},
        {'type': 'item', 'at': [18, 22], 'item': 'SYNTHETICSEED', 'hidden': True, 'name': 'HiddenItem (transformer rim)'},
    ]

    for e in E:
        m.keep_clear.add(tuple(e['at']))
    for pt in [(18, 28), (18, 29), (18, 30), (7, 26), (7, 27), (25, 20), (24, 20), (23, 20),
               (16, 12), (17, 12), (18, 12), (19, 12), (4, 18), (6, 18),
               (4, 24), (3, 24), (2, 24), (6, 24), (3, 25), (3, 26), (4, 25)]:
        m.keep_clear.add(pt)

    # ---- 3. Deep Transformer Architecture, Magnetite Altar, Twin Ladders & Intact Burning Braziers! ----
    _place_stamp_over(m, 'cv_ladder', 18, 29, base_z=1, top_z=2, top_rows=1, solid=False)
    _place_stamp_over(m, 'cv_ladder', 7, 25, base_z=1, top_z=2, top_rows=1, solid=False)
    _place_stamp_over(m, 'pf_roadstone', 14, 6, base_z=1, top_z=2, top_rows=1, solid=True)

    # Dramatic SW Magnetite Z-Crystal Altar pedestal ((3, 27)) flanked by shimmering crystals!
    _place_stamp_over(m, 'mn_plinth', 3, 27, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'cr_clear_c', 2, 27, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'cr_clear_c', 4, 27, base_z=1, top_z=1, top_rows=0, solid=True)

    _place_stamp_over(m, 'lm_gen', 11, 6, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'lm_gen', 23, 6, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'lm_monitors', 17, 5, base_z=1, top_z=2, top_rows=1, solid=True)
    for cx, cy in ((13, 17), (22, 17), (13, 22), (22, 22), (15, 26), (20, 26)):
        _place_stamp_over(m, 'nr_col', cx, cy, base_z=1, top_z=2, top_rows=1, solid=True)
    for ex, ey in ((8, 18), (29, 21), (11, 10), (24, 10)):
        _place_stamp_over(m, 'E_stal', ex, ey, base_z=1, top_z=2, top_rows=1, solid=True)

    braziers_605 = [
        (15, 29), (20, 29),
        (14, 15), (21, 15),
        (12, 9), (23, 9),
        (9, 25), (28, 17),
    ]
    for bx, by in braziers_605:
        _place_stamp_over(m, 'fw_brazier', bx, by, base_z=1, top_z=2, top_rows=1, solid=True)

    m.paint()
    _paint_conduit_floors(m, [
        (11, 6, 24, 11, 'panel'),
        (15, 6, 20, 10, 'grate'),
        (14, 15, 21, 23, 'road'),
        (15, 24, 20, 30, 'road'),
        (6, 20, 10, 27, 'sand'),
        (2, 24, 4, 28, 'plaza'),
    ])
    _paint_strip_h(m, 12, 23, 9, on=True)
    _paint_strip_v(m, 14, 15, 23, on=True)
    _paint_strip_v(m, 21, 15, 23, on=True)
    _paint_strip_h(m, 10, 26, 16, on=True)
    _paint_strip_h(m, 10, 26, 22, on=True)
    # Glowing magnetite vein leading straight to the :STEELIUMZ pedestal!
    _paint_strip_h(m, 2, 4, 26, on=True)

    Lr = RC.resolve(m.L, TID_CAVE).astype(np.int32)
    # Clean unbroken vent shafts over cooling pool & south slate floor — ZERO chopped/offset pf_glow blobs!
    _add_safe_overlay(Lr, TID_CAVE, 'cv_shaft', [(17, 17), (17, 25)])
    _assert_braziers_intact(Lr, TID_CAVE, braziers_605, 'Map 605')

    ev_pts = [tuple(e['at']) for e in E]
    PG.guard(Lr, TID_CAVE, ev_pts, 'Map 605')
    assert not PG.hits(Lr, R.tilesets()[TID_CAVE], ev_pts), 'Map 605 passguard hits!'
    _assert_no_over_trigger(Lr, TID_CAVE, E, 'Map 605')

    gated_items = {(3, 18), (2, 25), (3, 27)}
    main_events = [e for e in E if tuple(e['at']) not in gated_items and (e.get('name') or '') != 'Depths Boulder']
    _verify_all_events_and_trainers(Lr, TID_CAVE, main_events, (18, 28), 'Map 605 [TRAINERS + MAIN]')

    seen_sealed = _exact_bfs_cave(Lr, TID_CAVE, E, (18, 28))
    assert any((5 + dx, 24 + dy) in seen_sealed for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))), 'Map 605: Depths Boulder unreachable!'
    for gp in gated_items:
        assert gp not in seen_sealed and not any((gp[0] + dx, gp[1] + dy) in seen_sealed for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))), (
            f'Map 605 LEAK: gated item {gp} reachable while sealed!'
        )
    assert (7, 26) in seen_sealed and (18, 30) in seen_sealed, 'Map 605 ladders unreachable!'

    # Verify BOTH boulder push depths (pushed to (3, 24) AND pushed all the way to (2, 24)) reach :STEELIUMZ & MAXETHER!
    for push_x in (3, 2):
        unlocked_events = []
        for e in E:
            if e.get('type') == 'rock_smash':
                continue
            if (e.get('name') or '') == 'Depths Boulder':
                unlocked_events.append({**e, 'at': [push_x, 24]})
            else:
                unlocked_events.append(e)
        seen_open = _exact_bfs_cave(Lr, TID_CAVE, unlocked_events, (18, 28))
        for gp in gated_items:
            assert any((gp[0] + dx, gp[1] + dy) in seen_open for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))), (
                f'Map 605: gated item {gp} NOT reachable when boulder at ({push_x},24)!'
            )
    print(f'Map 605 Dual-State Proof PASSED (incl. :STEELIUMZ altar!): sealed={len(seen_sealed)} cells, open={len(seen_open)} cells!')

    m.L = Lr
    head = {
        'id': 605,
        'name': 'Static Tunnels Depths',
        'parent': 604,
        'bgm': 'Cave',
        'field': 'CAVE',
        'map_audio': {'bgm': 'Dungeon - Cave', 'bgs': 'Drip - Nadir', 'bgs_volume': 55, 'rain': False},
        'fog': {'name': 'prismfall_cave', 'opacity': 28, 'blend': 1, 'zoom': 100, 'sx': 1, 'sy': 0},
        'metadata': {
            'Name': 'Static Tunnels Depths',
            'Outdoor': False,
            'ShowArea': True,
            'BattleBack': 'cave1',
            'DarkMap': True,
            'MapPosition': POS_TUN,
        },
        'gates': [
            {'name': 'Depths Rock Smash & Strength Magnetite Sanctum (:STEELIUMZ)', 'from': [[18, 28]], 'sealed': [[3, 18], [2, 25], [3, 27]]},
        ],
        'tone': [-22, -20, -4, 20],
        '_file': '605_static_tunnels_depths.yaml',
    }
    m.write(605, head, comment='# GENERATED by mapgen/layouts/ossaria_tunnels.py: Static Tunnels Depths (605).\n')
    print('Wrote specs/605_static_tunnels_depths.yaml and data/raw/605.npy')


def main():
    build_604()
    build_605()
    print('Done: wrote 2 Ossaria Static Tunnels maps (604, 605).')


if __name__ == '__main__':
    main()
