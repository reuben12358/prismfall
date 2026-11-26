#!/usr/bin/env python3
"""layouts/cindervault_town.py — Cindervault Ch8 maps connected to Map 255 (Tap Chamber):
  - Map 249: Cindervault - Slag Ward (44x34, tileset 61 PF Rejuv Forge, field SCRAPYARD)
      Volcanic terraced caldera under-ward directly above Meridian Standard Tap No. 7:
      NW elevated Hearthguild Terrace (wh_e Hearthguild Hall, warning bell-post, guarded stair up to 240 Forge Terraces),
      Central Slag Plaza & Tap No. 7 Service Stair landing at (20,12) with return stairwell at (20,13) -> 255 (13,18),
      Warm soot-brick & earth-stone terraced thoroughfares, communal evacuation hearth & lantern strings,
      East tiered soot-brick tenement lanes (10 distinct silhouettes, zero copy-paste),
      South sunken volcanic magma run-off channels crossed by iron-grate footbridges & salvage yard.
  - Map 244: Hearthguild Hall (21x18, tileset 61 PF Rejuv Forge, field NONE)
      Void-sculpted Ashkaar smiths' guildhall:
      Elevated North Forge Sanctum (roaring hearth, sunken magma firebox, bellows, anvil, quench trough) with the
      grilled Light Stone Alcove centered at (10,3..4) straight ahead of arrival (10,8) facing up;
      Grand Council Nave with single-slab carved basalt council table, candelabras, chairs, Brann's Warden Chair;
      Recessed West Armory Bay & East Archive/Cider-Hearth Bay; narrowed South Yard Entry Vestibule exiting to 249.

Story canon: story/29_SCRIPT_CH8.md (Map 244 & Map 249).
NOTE: Keeps story scripting minimal (static NPC/examine flavour text; no invented plot switches/variables).
      V129 Ch8 scenes ("My Father", "Whose Is It" :ch8_lightstone, "Chestnuts") and Ch17 AS_FORGE_REMEMBERS
      are left unstaged with clear actor positions for Claude hand-off.

Run:
    /usr/bin/python3 -I mapgen/layouts/cindervault_town.py
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

TID = 61
HERE = K.HERE


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


def _place_building(m, name, x, y, door_link=None, door_name=None, plaque=None):
    """Place a multi-tile building stamp cleanly on a Cave map."""
    st = STAMPS[name]
    w, h = st['w'], st['h']
    m.stamps.append((name, x, y))
    L = np.array(st['layers'])
    occ = L.max(axis=0) > 0
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


def _bfs_check(m, start, targets, label):
    """Verify 4-neighbor Essentials walkability from start to every target cell."""
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


# =================================================================================================
# MAP 249 — Cindervault - Slag Ward (44x34, tileset 61 PF Rejuv Forge, field SCRAPYARD)
# =================================================================================================
def build_249():
    W, H = 44, 34
    m = Cave(W, H, 'L', seed=249, pool='Magma', tid=TID)
    m.STAIRS = K.STAIRS_STONE
    m.kit = {MASS: 'cvL', TER: 'cvL', FLOOR: 'cvL', 'default': 'cvL'}

    # ---- 1. Sculpt organic volcanic caldera terraces (MASS=6 outer crater walls, TER=2 upper rim, FLOOR=1 main ward) ----
    m.box(3, 11, 40, 29, FLOOR, '.')
    m.box(5, 29, 38, 30, FLOOR, '.')
    # Dramatic jagged volcanic basalt promontories framing the crater bowl
    m.mass_at([
        (3, 11), (3, 12), (3, 13), (3, 27), (3, 28), (3, 29), (4, 29),
        (40, 11), (40, 12), (40, 26), (40, 27), (40, 28), (40, 29), (39, 29),
        (5, 30), (6, 30), (7, 30), (35, 30), (36, 30), (37, 30), (38, 30),
        (16, 30), (17, 30), (26, 30), (27, 30),
    ])

    # NW Upper Hearthguild Terrace (TER=2, y=2..10, x=2..17)
    m.box(2, 2, 17, 10, TER, '.')
    # Ascending stone stair notch up toward 240 Forge Terraces at x=4..5, y=0..2!
    m.box(4, 0, 5, 2, TER, '.')
    m.mass_at([(2, 2), (3, 2), (2, 3), (17, 2), (17, 3)])

    # Central-North Caldera Culvert Shelf (FLOOR=1, x=18..25, y=4..11) — steaming magma feed!
    m.box(18, 4, 25, 11, FLOOR, '.')
    m.mass_at([(18, 4), (25, 4), (18, 5)])

    # NE Upper Tenement Terrace (TER=2, x=26..40, y=2..11)
    m.box(26, 2, 40, 11, TER, '.')
    m.mass_at([(26, 2), (39, 2), (40, 2), (40, 3), (40, 11)])

    # Guarded South Caldera Gate spur (x=19..23, y=30..32, FLOOR=1)
    m.box(19, 30, 23, 32, FLOOR, '.')

    # ---- 2. Organic Glowing Molten Slag Quench-Channels (PF Magma — NEVER straight boxes!) ----
    magma_cells = [
        # North caldera feed culvert (visible from (20,12) arrival!)
        (20, 6), (21, 6), (22, 6), (23, 6),
        (19, 7), (20, 7), (21, 7), (22, 7), (23, 7), (24, 7),
        (19, 8), (20, 8), (21, 8), (22, 8), (23, 8),
        (20, 9), (21, 9), (22, 9),
        # West caldera run-off trough (south of Hearthguild cliff)
        (4, 15), (5, 15), (6, 15), (7, 15),
        (4, 16), (5, 16), (6, 16), (7, 16), (8, 16), (9, 16),
        (5, 17), (6, 17), (7, 17), (8, 17), (9, 17),
        (6, 18), (7, 18), (8, 18),
        # Grand South-Central Meandering Slag Channel (organic stepped volcanic gully!)
        (14, 21), (15, 21), (16, 21), (17, 21),
        (13, 22), (14, 22), (15, 22), (16, 22), (17, 22), (18, 22), (19, 22),
        (14, 23), (15, 23), (16, 23), (17, 23), (18, 23), (19, 23), (20, 23), (21, 23), (22, 23),
        (17, 24), (18, 24), (19, 24), (20, 24), (21, 24), (22, 24), (23, 24), (24, 24), (25, 24), (26, 24),
        (21, 25), (22, 25), (23, 25), (24, 25), (25, 25), (26, 25), (27, 25), (28, 25),
        (24, 26), (25, 26), (26, 26), (27, 26), (28, 26), (29, 26),
        (26, 27), (27, 27), (28, 27),
        # East volcanic fissure gorge along east rim
        (37, 15), (38, 15), (39, 15),
        (37, 16), (38, 16), (39, 16),
        (37, 17), (38, 17), (39, 17),
        (37, 18), (38, 18),
    ]
    for mx, my in magma_cells:
        m.cls[my, mx] = 'w'

    # ---- 3. Terraced Stone Stairs connecting TER=2 <-> FLOOR=1 ----
    m.stairs(12, 10, w=4, n=3, c='.')
    m.stairs(28, 11, w=3, n=3, c='.')

    m.tidy()
    m.plan_cliffs(rows=3)

    # ---- 4. Sturdy Iron-Grate Footbridges across the South-Central Magma Channel! ----
    bridges = [
        (16, 21), (17, 21), (16, 22), (17, 22), (16, 23), (17, 23), (16, 24), (17, 24),
        (23, 23), (24, 23), (23, 24), (24, 24), (23, 25), (24, 25), (23, 26), (24, 26),
    ]
    for bx, by in bridges:
        m.cls[by, bx] = '.'
        m.keep_clear.add((bx, by))

    # ---- 5. Architectural Buildings (10 UNIQUE silhouettes — ZERO copy-paste!) ----
    # NW Upper Terrace (TER=2): Hearthguild Hall (wh_e 8x8 -> door (10,7), forecourt y=8..9!)
    _place_building(m, 'wh_e', 7, 0, door_link='CV_HEARTHGUILD', door_name='Hearthguild Hall')

    # NE Upper Terrace (TER=2): Varied slag-brick upper shacks!
    _place_building(m, 'lb_l6b', 27, 2, plaque='SLAG-BRICK TENEMENT 4. Chalked on the frame: "THREE BELLS — SHUTTERS DOWN."')
    _place_building(m, 'lb_l3a', 33, 3, plaque='A narrow slag-brick cottage. Warm air whistles through the keyhole.')
    _place_building(m, 'gl_shed', 36, 3, plaque='SLAG-COAL (MOSTLY ROCK, BURNS ANYWAY).')

    # East Mid-Tier (FLOOR=1, y=15..21): Leaves y=14 wide open for East Stair landing!
    _place_building(m, 'lb_l5b', 26, 15, plaque='An iron fire-escape clings to the brick. Bundles are stacked inside the doorway.')
    _place_building(m, 'th_m', 31, 15, plaque='SMITH. NOT VERY GOOD. CHEAP. (Honest Ashkaar sign.)')

    # SW Lower Slag Basin (FLOOR=1, x=4..14, y=19..29): Clustered worker shacks & lean-to!
    _place_building(m, 'lb_l5a', 4, 19, plaque='A slag-brick shack with soot-darkened shutters. The chimney is still warm.')
    _place_building(m, 'lb_l4a', 9, 20, plaque='Locked. A chalk note: "GONE UP TO THE TERRACES. LEFT WATER FOR THE HOUNDOUR."')
    _place_building(m, 'hb_shed', 4, 26)

    # SE Salvage & Forge Yard (FLOOR=1, y=23..28): Furnace-front salvage workshop!
    _place_building(m, 'lb_l6a', 31, 23, plaque='HEARTHGUILD SALVAGE YARD. "QUENCH-IRON & GRATES. PRICES HIGH BECAUSE OF THE FEVER."')

    # ---- 6. CRITICAL WARPS, GUARDED UNBUILT EXITS, STORY NPCs & SIGNS ----
    E = m.events
    # CRITICAL: Return stair down to Map 255 Tap Chamber right south of (20,12) arrival!
    E.append({
        'type': 'warp',
        'name': 'Down to Tap No. 7',
        'at': [20, 13],
        'to': {'map': 255, 'x': 13, 'y': 18, 'dir': 'up'},
        'se': 'Door exit',
    })
    # Guarded NW Upper Stair -> Map 240 Cindervault - Forge Terraces (unbuilt -> 0 WARN!)
    for ux in (4, 5):
        E.append({
            'type': 'event',
            'name': 'Up to Forge Terraces',
            'at': [ux, 2],
            'pages': [{
                'trigger': 'touch',
                'commands': _guarded_unbuilt_transfer(
                    240, 20, 26, 'up',
                    "(Hearthguild wardens have roped off the stair up to the Forge Terraces while the caldera bells clear.)"
                ),
            }],
        })
    # Guarded South Rim Path -> Map 243 Cindervault - Caldera Gate (unbuilt -> 0 WARN!)
    for sx in (20, 21, 22):
        E.append({
            'type': 'event',
            'name': 'To Caldera Gate',
            'at': [sx, 32],
            'pages': [{
                'trigger': 'touch',
                'commands': _guarded_unbuilt_transfer(
                    243, 20, 4, 'down',
                    "(The slag-cart track out toward the Caldera Gate is barricaded against falling ash.)"
                ),
            }],
        })

    # Story-canon NPCs (static, zero invented plot switches/vars; directly from story/29_SCRIPT_CH8.md!)
    E += [
        _make_npc('Evacuating Mother', (12, 13), 'NPC 15', 'up', [
            "Mother: Keep your boots off the grate edges, love. The channels are running hot today.",
            "Mother: Three bells means off the forges. Four means get up the stairs before the steam rises.",
        ]),
        _make_npc('Child with Litwick Jar', (15, 13), 'NPC 05', 'up', [
            "(The child holds a glass jam jar up like a lantern. Inside, a tiny purple flame bobs cheerfully.)",
            "Child: Mama says the bells mean go up, not down. My Litwick isn't scared—he likes the warm steps!",
        ]),
        _make_npc('Hearthguild Watchman', (16, 8), 'trainer_BLACKBELT', 'down', [
            "Hearthguild Watchman: Cindervault's bells used to ring the hours. Now they ring the heat.",
            "Hearthguild Watchman: Three bells, you take your Pokémon off the forges. Four, you take yourself. We've never rung five.",
        ]),
        _make_npc('Slag Ward Smith', (23, 14), 'trainer_HIKER', 'left', [
            "Slag Ward Smith: Meridian bolted Tap Seven straight into the caldera floor under our boots.",
            "Slag Ward Smith: They put a brass gauge on it. The gauge says fine. The gauge is also melting.",
        ]),
        _make_npc('Broth Seller', (23, 19), 'NPC 18', 'down', [
            "Broth Seller: Boiled broth! Very boiled! Didn't even need a fire—just set the kettle on the grate.",
            "Broth Seller: Lying's a crime in Ashkaar, so I won't tell you it's delicate. It's hot and it's cheap.",
        ]),
        _make_npc('Old Coal-Hauler', (12, 26), 'NPC 25', 'right', [
            "Old Coal-Hauler: Whole Slag Ward sits on two hundred years of cooled foundry run-off.",
            "Old Coal-Hauler: Hearthguild keeps the stairs patched and the drains clear. Up on the rim they forget we're down here until the bells start.",
        ]),
        _make_npc('Salvage Tinker', (29, 28), 'trainer_ENGINEER', 'left', [
            "Salvage Tinker: Quench-channels down here are running at a boil. You can't quench steel in boiling water—a blade wants a shock, not a bath.",
        ]),
        _sign('Tap Seven Notice', (18, 13),
              "MERIDIAN STANDARD TAP No. 7 — SERVICE STAIR. AUTHORISED ENGINEERS ONLY. (Someone has scratched below it: OUR FIRE.)"),
        _sign('Hearthguild Plaque', (11, 8),
              "HEARTHGUILD HALL — WARDEN BRANN HOLLOWAY. Say true, or keep your breath for the bellows."),
        _sign('Broth Sign', (25, 19),
              "WATER (BOILING). BROTH (ALSO BOILING). BREAD (YESTERDAY'S)."),
        _sign('Slag Channel Marker', (18, 20),
              "LOWER QUENCH RUN-OFF — MIND THE GRATES. HEAT RISES FASTER THAN THE BELLS."),
        {'type': 'item', 'at': [38, 28], 'item': 'CHARCOAL', 'name': 'Slag Ward Charcoal'},
    ]

    m.keep_clear |= {
        (20, 12), (20, 13), (19, 12), (21, 12), (20, 11), (19, 13), (21, 13),
        (10, 7), (10, 8), (10, 9), (11, 9), (12, 9), (13, 9), (14, 9), (15, 9),
        (4, 2), (5, 2), (4, 3), (5, 3), (4, 4), (5, 4), (4, 5), (5, 5), (6, 9), (7, 9), (8, 9), (9, 9),
        (20, 31), (21, 31), (22, 31), (20, 32), (21, 32), (22, 32),
        (38, 28), (37, 28), (36, 28), (35, 28), (34, 28),
    }
    for e in E:
        ex, ey = e['at']
        m.keep_clear.add((ex, ey))
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            if m.inb(ex + dx, ey + dy):
                m.keep_clear.add((ex + dx, ey + dy))

    # ---- 7. Composed Props, Landmarks, Focal Gathering Hearth & Atmospheric Volcanic Lighting ----
    # (a) Tap No. 7 Service Stair Gantry at (18..22, 11..14)
    _place_stamp_over(m, 'lm_bollard', 18, 12, base_z=1, top_z=2, top_rows=0, solid=True)
    _place_stamp_over(m, 'lm_bollard', 22, 12, base_z=1, top_z=2, top_rows=0, solid=True)
    _place_stamp_over(m, 'lm_bollard', 18, 14, base_z=1, top_z=2, top_rows=0, solid=True)
    _place_stamp_over(m, 'lm_bollard', 22, 14, base_z=1, top_z=2, top_rows=0, solid=True)
    _place_stamp_over(m, 'lm_railing_w', 19, 14, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'lm_railing_e', 21, 14, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'lm_alarm_on', 22, 11, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'cv_sluice', 23, 11, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'lm_gearbox', 24, 11, base_z=1, top_z=1, top_rows=0, solid=True)

    # (b) Hearthguild Upper Terrace Landmarks (Bell-Post, Ashkaar Banners, Forge Braziers, Bench)
    _place_stamp_over(m, 'pf_bellpost', 16, 4, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'wr_ban_ash', 6, 4, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'wr_ban_ash', 15, 4, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'fw_brazier', 8, 7, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'fw_brazier', 12, 7, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'pf_stonebench', 3, 7, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'pf_barricade', 4, 1, base_z=1, top_z=1, top_rows=0, solid=True)

    # (c) Central-North Caldera Watch-Beacon (stands proud on basalt shelf overlooking magma culvert!)
    _place_stamp_over(m, 'pf_beacon', 24, 5, base_z=1, top_z=2, top_rows=2, solid=True)

    # (d) NE Upper Tenement Terrace Vignette (coal sacks, barrels, brazier, tools — clean of cliff lip!)
    _place_stamp_over(m, 'wr_sacks', 26, 9, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'hb_barrels', 32, 9, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'wr_sacks', 37, 9, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'fw_brazier', 27, 9, base_z=1, top_z=2, top_rows=1, solid=True)

    # (e) Central Slag Ward Gathering Square (breaks up center plaza with cozy evacuation hearth + broth stall + lantern string!)
    _place_stamp_over(m, 'wr_firering', 17, 17, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'fw_brazier', 17, 16, base_z=1, top_z=2, top_rows=1, solid=True)  # lit brazier inside stone hearth ring!
    _place_stamp_over(m, 'pf_stonebench', 15, 18, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'wr_sacks', 19, 17, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'hb_boxes', 15, 16, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'lm_noodles', 23, 17, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'lm_washline', 26, 22, base_z=2, top_z=2, top_rows=1, solid=False)
    # Warm overhead festival/ward lantern string spanning the central square (y=16, x=19..22, pri overhead!)
    for i, lx in enumerate((19, 20, 21, 22)):
        m.over.append((2, lx, 16, P1('pf_lstring%d' % (i % 3))))
    _place_stamp_over(m, 'fw_brazier', 11, 14, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'fw_brazier', 25, 12, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'cv_cart', 10, 14, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'hb_boxes', 34, 13, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'cv_tools', 35, 20, base_z=1, top_z=1, top_rows=0, solid=True)

    # (f) SW Slag-Brick Shack Cluster (Coal Wagon, Steaming Well, Cobbler Bench, Sacks, Barrels)
    _place_stamp_over(m, 'pf_wagon', 13, 26, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'pf_well', 7, 26, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'wr_sacks', 9, 26, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'hb_barrel', 4, 25, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'lm_cobbler', 9, 28, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'fw_brazier', 14, 19, base_z=1, top_z=2, top_rows=1, solid=True)

    # (g) SE Salvage & Forge Yard (Sluice Pump, Supply Cart, Forged Weapon Rack, Banners, Barrels)
    _place_stamp_over(m, 'cv_pump', 37, 22, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'cv_sluice', 37, 24, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'wr_rack', 39, 22, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'wr_supply', 29, 22, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'fw_brazier', 26, 28, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'wr_ban_ash', 18, 29, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'wr_ban_ash', 24, 29, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'hb_barrels', 38, 25, base_z=1, top_z=2, top_rows=1, solid=True)

    # (h) Volcanic Basalt Rock Outcrops framing outer caldera crags & hot channel banks
    for rx, ry, k in ((4, 14, 0), (10, 17, 1), (12, 20, 0), (35, 19, 1), (36, 28, 0), (6, 29, 1)):
        if m.cls[ry, rx] == '.' and not m.taken[ry, rx] and (rx, ry) not in m.keep_clear:
            _place_stamp_over(m, 'E_rock%d' % k, rx, ry, base_z=1, top_z=1, top_rows=0, solid=True)

    # (i) Volcanic Steam Plumes & Warm Magma/Brazier Glow Halos (strictly anchored to fire & magma!)
    for sx, sy in ((21, 7), (23, 8), (6, 16), (15, 22), (20, 23), (26, 25), (38, 16), (7, 27)):
        _place_stamp_over(m, 'lm_steam0' if (sx + sy) % 2 == 0 else 'lm_steam1', sx, sy, base_z=2, top_z=2, top_rows=2, solid=False)
    for gx, gy in ((20, 7), (22, 8), (5, 15), (14, 21), (19, 23), (25, 24), (27, 26), (37, 15),
                   (8, 7), (12, 7), (24, 5), (17, 16), (11, 14), (25, 12), (26, 28), (19, 12)):
        m.stamps.append(('pf_glow', gx, gy))

    # Paint Cave geometry & basalt cliffs first
    m.paint()

    # ---- 8. Moody Volcanic Ashkaar Paving Hierarchy (Warm Soot-Cobbles + Dressed Earth-Stone + Steel Deck!) ----
    # Replaces harsh bright white marble with authentic warm charcoal-brick setts (lm_low) & worn basalt-earth (E_f)
    # so the walkways have crisp figure-ground readability while glowing magma & warm windows steal the show!
    low_ids = [P1('lm_low%d' % i) for i in range(4)]      # warm dark soot-brick setts (main thoroughfares!)
    earth_ids = [P1('E_f%d' % i) for i in range(4)]       # warm volcanic ochre-earth stone (plaza & terrace accents!)
    slate_ids = [P1('T_f%d' % i) for i in range(4)]       # dressed dark ashlar flagstones (Hearthguild forecourt!)
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

    # Upper Hearthguild Terrace: warm volcanic earth-stone promenade leading from stair to Hall & 240 steps!
    paint_path_rect(4, 2, 6, 9, earth_ids)
    paint_path_rect(6, 8, 16, 9, earth_ids)
    paint_path_rect(8, 8, 12, 9, slate_ids)  # dressed ashlar doorstep pad directly before Hearthguild Hall!
    # NE Upper Tenement Terrace soot-brick lane
    paint_path_rect(27, 9, 37, 10, low_ids)
    # Central Slag Ward Main Thoroughfare: warm earth-stone core bordered by dark soot-brick cobbles!
    paint_path_rect(11, 13, 25, 20, low_ids)
    paint_path_rect(12, 14, 24, 15, earth_ids)
    paint_path_rect(24, 14, 34, 14, earth_ids)
    paint_path_rect(20, 15, 22, 20, earth_ids)
    paint_path_rect(15, 19, 25, 20, earth_ids)
    # SW Shack Courtyard Lane & South Basin Road
    paint_path_rect(6, 25, 18, 28, low_ids)
    paint_path_rect(15, 24, 18, 28, earth_ids)
    # SE Salvage Yard & South Rim Road
    paint_path_rect(19, 27, 36, 29, earth_ids)
    paint_path_rect(20, 29, 22, 32, earth_ids)
    paint_path_rect(26, 22, 35, 22, low_ids)

    # Riveted-steel Meridian Tap No. 7 Service Stair Deck around (19..21, 11..13)
    for y in (11, 12, 13):
        for x in (19, 20, 21):
            if m.cls[y, x] == '.' and not m.cliff[y, x]:
                m.L[0, y, x] = qf0 if (x + y) % 2 == 0 else qf1
                if int(m.L[1, y, x]) in floorpatch_ids:
                    m.L[1, y, x] = 0
    m.L[1, 13, 20] = stair_m
    m.L[1, 12, 19] = grate
    m.L[1, 12, 21] = grate

    # Iron-Grate Footbridges over the South-Central Magma Channel!
    for bx, by in bridges:
        m.L[0, by, bx] = qf0 if (bx + by) % 2 == 0 else qf1
        m.L[1, by, bx] = grate
    for rx, ry, piece in (
        (15, 22, 'lm_bollard'), (18, 22, 'lm_bollard'),
        (22, 24, 'lm_bollard'), (25, 24, 'lm_bollard'),
    ):
        if m.cls[ry, rx] == 'w':
            m.L[1, ry, rx] = P1(piece)

    # Subtle glowing volcanic floor embers in quiet caldera corners
    for i, (x, y) in enumerate(((5, 13), (9, 13), (10, 18), (22, 16), (35, 16), (36, 21), (11, 29), (28, 29))):
        if m.cls[y, x] == '.' and not m.cliff[y, x] and not m.taken[y, x] and (x, y) not in m.keep_clear:
            m.L[1, y, x] = P1('wr_ember%d' % (i % 3))

    _bfs_check(m, (20, 12), [
        ('Tap No. 7 stair down', (20, 13), False),
        ('Hearthguild Hall door', (10, 7), False),
        ('Hearthguild Hall step-out', (10, 8), False),
        ('Up to Forge Terraces (240)', (4, 2), False),
        ('NE Tenement Terrace', (30, 9), False),
        ('SW Shack Basin', (10, 26), False),
        ('SE Salvage Yard Charcoal', (38, 28), False),
        ('South Caldera Gate (243)', (21, 32), False),
        ('Evacuating Mother', (12, 13), True),
        ('Child with Litwick Jar', (15, 13), True),
    ], 'Map 249')

    head = {
        'id': 249,
        'name': 'Cindervault - Slag Ward',
        'parent': 0,
        'bgm': 'Lava Town',
        'field': 'SCRAPYARD',
        'map_audio': {'bgm': 'Town - Ashkaar', 'bgs': 'Lava - Ashkaar', 'bgs_volume': 55, 'rain': False},
        'metadata': {'Name': 'Cindervault', 'Outdoor': True, 'ShowArea': True, 'MapPosition': [0, 24, 8], 'BattleBack': 'cave1'},
        'tone': [20, 0, -18, 10],
        'fog': {'name': 'prismfall_cave', 'opacity': 24, 'blend': 1, 'zoom': 100, 'sx': 1, 'sy': 0},
        '_file': '249_slag_ward.yaml',
    }
    m.write(249, head, comment='# GENERATED by mapgen/layouts/cindervault_town.py (Ch8): Cindervault - Slag Ward (story/29_SCRIPT_CH8.md).\n'
                               '# Edit the layout script, not this file.\n')
    return m


# =================================================================================================
# MAP 244 — Hearthguild Hall (21x18, tileset 61 PF Rejuv Forge, field NONE)
# =================================================================================================
def build_244():
    W, H = 21, 18
    m = Cave(W, H, 'L', seed=244, pool='Magma', tid=TID)
    m.auto = {'w': ('Magma', 'pf'), 'q': ('Cave Pool', 'pf'), 'W': ('Sea deep', 'rejuvenation')}
    m.STAIRS = K.STAIRS_STONE

    # ---- 1. Sculpt the Black Void into a Cruciform Guildhall (ZERO flat box!) ----
    m.box(3, 3, 17, 6, TER, '.')
    m.box(8, 2, 12, 3, TER, '.')      # recessed Light Stone Sanctuary Alcove!
    m.box(5, 7, 15, 14, FLOOR, '.')   # Grand Council Nave
    m.box(2, 9, 4, 13, FLOOR, '.')    # Recessed West Armory & Anvil Wing
    m.box(16, 9, 18, 13, FLOOR, '.')  # Recessed East Archive & Cider-Hearth Wing
    m.box(8, 15, 12, 16, FLOOR, '.')  # Narrowed South Yard Entrance Vestibule
    m.mass_at([(3, 3), (17, 3), (5, 14), (15, 14)])

    # ---- 2. Sunken Magma Forge Firebox (W) & Steaming Quench Basin (E) ----
    m.cls[5, 4] = 'w'
    m.cls[5, 5] = 'w'
    m.cls[5, 15] = 'q'
    m.cls[5, 16] = 'q'

    # 2-row carved basalt dais drop (lip y=6, base y=7 -> row y=8 including (10,8) is 100% open Nave floor!)
    K.KITS['cvL2'] = dict(K.KITS['cvL'], rows=[K.KITS['cvL']['rows'][0], K.KITS['cvL']['rows'][2]])
    m.kit = {TER: 'cvL2', FLOOR: 'cvH', MASS: 'cvH', 'default': 'cvH'}
    m.stairs(9, 6, w=3, n=2, c='.')

    m.tidy()
    m.plan_cliffs(rows=3)

    # ---- 3. Events (Exit to 249, Static Lore NPCs, Interactive Landmarks — 0 warnings!) ----
    E = m.events
    E.append({
        'type': 'exit',
        'at': [10, 16],
        'link': 'CV_HEARTHGUILD',
        'arrive': [10, 15, 'up'],
    })

    E += [
        _make_npc('Hearthguild Apprentice', (14, 6), 'trainer_HIKER', 'right', [
            "Hearthguild Apprentice: Warden Brann says a blade decides what it's going to be in the quench. Too slow, it's soft; too fast, it cracks.",
            "Hearthguild Apprentice: Lately the quench trough steams before we even dip a bar. That's the mountain's fever.",
        ]),
        _make_npc('Elder Smith', (17, 11), 'NPC 25', 'left', [
            "Elder Smith: That white stone over the forge has been in the Hearthguild's keeping for thirty years—since before the Dominar's great-grandmother learned to ride.",
            "Elder Smith: Warden Brann roasts chestnuts on the coals at two in the morning when he's thinking hard. Cuts a cross in every shell so they don't go off like a Voltorb.",
        ]),
        _sign('Light Stone Grille', (10, 4),
              "Behind the iron grille, resting in a forged cradle: a white stone the size of a fist, giving off a light like a cold morning. The Light Stone of the Hearthguild."),
        _sign('Hearthguild Forge', (6, 5),
              "The great Hearthguild forge. White-hot coals pulse in the basalt hearth; heavy tongs, hammers, and quenching bars hang within arm's reach."),
        _sign('Warden Chair', (7, 10),
              "Warden Brann's chair at the head of the basalt table, iron-ringed and worn smooth by big hands. Ashkaar envoys have been known to sit in it without asking."),
        _sign('Basalt Council Table', (10, 10),
              "A long council table hewn from a single slab of black caldera basalt. Candle wax and ring-marks from cider mugs speckle the dark stone."),
        _sign('Chestnut Pan', (13, 4),
              "A blackened iron pan resting by the hearth coals, dusted with ash and split chestnut shells. Every shell has a neat cross scored into its top."),
        _sign('Cider Cask', (17, 10),
              "A stout oak cask smelling sharply of spiced apples and cloves. A tin ladle hangs on its spigot."),
        # Positioned at (16, 9) so (16, 10) right below it is walkable -> 0 walled-in warnings!
        _sign('Hearthguild Ledger', (16, 9),
              "THE HEARTHGUILD LEDGER — CINDERVAULT. Entries run back three centuries in iron-gall ink: bellows mended, bells cast, and Warden rings cut."),
    ]

    m.keep_clear |= {
        (10, 8), (9, 8), (11, 8), (10, 7), (10, 6), (10, 5), (9, 5), (11, 5),
        (10, 16), (10, 15), (10, 14), (10, 13), (9, 15), (11, 15),
        (6, 8), (6, 9), (6, 10), (6, 11), (6, 12), (6, 13),
        (14, 8), (14, 9), (14, 10), (14, 11), (14, 12), (14, 13),
        (16, 10),
    }

    # ---- 4. Architectural Furnishings, Forge Hardware & Interior Lighting (ZERO outdoor street lamps!) ----
    # (a) The Light Stone Alcove (dead-center at x=9..11, y=2..4 — directly ahead of (10,8)!)
    _place_stamp_over(m, 'lm_cradle_cold', 10, 2, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'cr_clear_c', 10, 3, base_z=2, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'lm_bars_l', 9, 4, base_z=1, top_z=2, top_rows=0, solid=True)
    _place_stamp_over(m, 'lm_bars_m', 10, 4, base_z=1, top_z=2, top_rows=0, solid=True)
    _place_stamp_over(m, 'lm_bars_r', 11, 4, base_z=1, top_z=2, top_rows=0, solid=True)
    _place_stamp_over(m, 'cv_chain', 8, 3, base_z=2, top_z=2, top_rows=1, solid=False)
    _place_stamp_over(m, 'cv_chain', 12, 3, base_z=2, top_z=2, top_rows=1, solid=False)

    # (b) The Great Hearthguild Forge (West Dais + East Quench Wing)
    _place_stamp_over(m, 'cv_pump', 3, 3, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'mn_fire_lit', 5, 3, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'cv_tools', 3, 5, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'lm_gearbox', 6, 5, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'wr_rack', 14, 3, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'cv_sluice', 16, 3, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'hb_barrel', 17, 4, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'wr_sacks', 17, 5, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'fw_brazier', 13, 3, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'fw_brazier', 8, 3, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'fw_brazier', 12, 3, base_z=1, top_z=2, top_rows=1, solid=True)
    # Dark forged iron corner bollards flanking the dais steps (replaces loud yellow Lumen railings!)
    for bx, by in ((8, 6), (12, 6)):
        _place_stamp_over(m, 'lm_bollard', bx, by, base_z=1, top_z=1, top_rows=0, solid=True)

    # (c) Seating around the Single-Slab Basalt Council Table
    _place_stamp_over(m, 'mn_chair_right', 7, 10, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'mn_chair_left', 13, 10, base_z=1, top_z=1, top_rows=0, solid=True)
    for cx in (8, 10, 12):
        _place_stamp_over(m, 'mn_dch_up', cx, 12, base_z=1, top_z=1, top_rows=0, solid=True)
    for cx in (8, 12):
        _place_stamp_over(m, 'mn_dch_down', cx, 9, base_z=1, top_z=1, top_rows=0, solid=True)

    # (d) Recessed West Armory & Tool Bay
    _place_stamp_over(m, 'mn_armour', 2, 9, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'wr_rack', 4, 9, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'hb_boxes', 2, 12, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'cv_tools', 4, 13, base_z=1, top_z=1, top_rows=0, solid=True)

    # (e) Recessed East Guild Archive & Cider-Hearth Bay
    _place_stamp_over(m, 'mn_books2', 16, 8, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'hb_cask', 18, 9, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'hb_barrels', 18, 11, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'mn_candelabra', 16, 12, base_z=1, top_z=2, top_rows=1, solid=True)

    # (f) South Yard Entrance Vestibule
    _place_stamp_over(m, 'wr_ban_ash', 8, 13, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'wr_ban_ash', 12, 13, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'mn_candelabra', 5, 12, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'mn_armour', 7, 14, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'mn_armour', 13, 14, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'mn_mat', 9, 16, base_z=1, top_z=1, top_rows=0, solid=False)

    # (g) Strictly Wall-Mounted Interior Sconces (removed floating cliff-lip candles!), Chandelier & Anchored Glows!
    for sx, sy in ((3, 8), (17, 8)):
        m.over.append((2, sx, sy, P1('mn_sconce')))
    for sx, sy in ((8, 2), (12, 2), (3, 3), (17, 3)):
        m.over.append((2, sx, sy, P1('cv_walllamp')))
    m.stamps.append(('mn_chandelier', 9, 9))
    m.stamps.append(('cv_shaft', 9, 3))
    # Every pf_glow anchored strictly onto an actual light/fire source!
    for gx, gy in ((9, 2), (5, 3), (4, 5), (8, 3), (12, 3), (13, 3), (9, 10)):
        m.stamps.append(('pf_glow', gx, gy))
    _place_stamp_over(m, 'lm_steam0', 15, 4, base_z=2, top_z=2, top_rows=2, solid=False)
    _place_stamp_over(m, 'lm_steam1', 16, 4, base_z=2, top_z=2, top_rows=2, solid=False)

    m.paint()

    # ---- 5. Cohesive Ashkaar Floors (NO bright white Lumen marble at south door!) & Basalt Council Table ----
    nf = [P1('N_f%d' % i) for i in range(4)]
    tf = [P1('T_f%d' % i) for i in range(4)]
    lf = [P1('L_f%d' % i) for i in range(4)]
    low = [P1('lm_low%d' % i) for i in range(4)]   # rich dark soot-brick vestibule!
    floorpatch_ids = {P1(k) for k in STAMPS if k.startswith(('L_floorpatch_', 'L_fd'))}

    for y in range(H):
        for x in range(W):
            if m.cls[y, x] != '.' or m.cliff[y, x]:
                continue
            if int(m.L[1, y, x]) in floorpatch_ids:
                m.L[1, y, x] = 0
            if m.ht[y, x] == TER:
                m.L[0, y, x] = lf[(x * 3 + y * 5) % 4]
            elif x <= 4 or x >= 16:
                m.L[0, y, x] = nf[(x * 5 + y * 3) % 4]
            elif y >= 15:
                m.L[0, y, x] = low[(x + y) % 4]
            else:
                m.L[0, y, x] = tf[(x * 7 + y * 3) % 4]

    # Iron forge grates cleanly along the firebox & quench edges
    for gx, gy in ((4, 6), (5, 6), (6, 6), (15, 6), (16, 6)):
        if m.cls[gy, gx] == '.' and not m.taken[gy, gx] and not m.cliff[gy, gx]:
            m.L[1, gy, gx] = P1('lm_grate')

    # Crimson Hearthguild woven carpet runner leading from South Yard Door (y=15) up to the Forge Steps (y=8)!
    for y in range(8, 16):
        for x in (9, 10, 11):
            if 10 <= y <= 11:
                continue
            if m.L[1, y, x] == 0:
                part = ('n' if y == 8 else 's' if y == 15 else '') + ('w' if x == 9 else 'e' if x == 11 else '')
                m.L[1, y, x] = P1('mn_rugR_' + (part or ('c2' if y in (9, 13) else 'c')))

    # THE SINGLE-SLAB BASALT COUNCIL TABLE (x=8..12, y=10..11)
    for x in range(8, 13):
        side = 'w' if x == 8 else 'e' if x == 12 else 'm'
        m.L[1, 10, x] = P1('L_lip' + side)
        m.L[1, 11, x] = P1('L_base' + side)
    m.L[2, 10, 9] = P1('mn_dt_cand')
    m.L[2, 10, 11] = P1('mn_dt_cand')
    m.L[2, 10, 8] = P1('mn_dt_plate')
    m.L[2, 10, 12] = P1('mn_dt_plate')

    for ex, ey, k in ((3, 6, 0), (7, 5, 1), (7, 6, 2)):
        if m.cls[ey, ex] == '.' and not m.L[1, ey, ex] and not m.L[2, ey, ex]:
            m.L[1, ey, ex] = P1('wr_ember%d' % k)

    _bfs_check(m, (10, 8), [
        ('Yard Door Exit (249)', (10, 16), False),
        ('Yard Arrival from 249', (10, 15), False),
        ('Light Stone Grille', (10, 4), True),
        ('Hearthguild Forge', (6, 5), True),
        ('Warden Chair', (7, 10), True),
        ('Basalt Council Table', (10, 10), True),
        ('West Armory Bay', (3, 11), False),
        ('East Cider/Archive Bay', (17, 11), True),
        ('Hearthguild Ledger', (16, 9), True),
        ('Forge Dais Steps', (10, 6), False),
    ], 'Map 244')

    head = {
        'id': 244,
        'name': 'Hearthguild Hall',
        'parent': 249,
        'bgm': 'Lava Town',
        'field': 'NONE',
        'map_audio': {'bgm': 'Town - Ashkaar', 'bgs': '', 'rain': False},
        'metadata': {'Name': 'Hearthguild Hall', 'SnapEdges': True, 'MapPosition': [0, 24, 8]},
        'tone': [16, 2, -16, 8],
        '_file': '244_hearthguild_hall.yaml',
    }
    m.write(244, head, comment='# GENERATED by mapgen/layouts/cindervault_town.py (Ch8): Hearthguild Hall (story/29_SCRIPT_CH8.md).\n'
                               '# Edit the layout script, not this file.\n')
    return m


def main():
    build_249()
    build_244()
    print('Done: wrote specs/249_slag_ward.yaml, specs/244_hearthguild_hall.yaml, and raw 249.npy / 244.npy.')


if __name__ == '__main__':
    main()
