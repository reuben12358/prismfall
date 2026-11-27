#!/usr/bin/env python3
"""layouts/verdance_wards.py — Act 3 Batch 3E: Verdance Wards, Briar Hall Interiors, The Heartgarden & Rootward (6 Maps):
  - Map 283: Verdance - Glasshouse Ward      (48x40, Outdoor, TS 55 PF Rejuv City, :FLOWER_GARDEN, rubric: true)
      * Terraced high-town botanical conservatory district with glass-domed conservatories (lb_lab, lb_arcade,
        lb_t9a, lb_t7b, lb_t6c), lush rose-garden beds, Briarwater conservatory canal with twin cedar footbridges,
        pollen-lamp avenues, Quiet Way Lantern Board (pf_trial_board(:ELOWEN)), Ch10 runaway-bloom botanists,
        and Verdance Gym 9 Grand Conservatory Hall (lb_council) framed by the blossoming floral archway (wb_gate)
        -> 290 (10, 15) up! Links cleanly to 280 Market Terraces (96, 66), 294 Heartgarden (3, 20), 296 Rootward (21, 3).
  - Map 284: Verdance - Kingsgate Barbican   (40x24, Outdoor, TS 55 PF Rejuv City, :FLOWER_GARDEN, rubric: true)
      * Monumental fortified briar-and-limestone royal gatehouse flanking Verdance's south approach: twin crenelated
        barbican arches (gt_gate6 N, gt_gate4 S), flanking watchtowers, royal Evergreen banners, blazing beacons,
        cobble parade yard overrun with Ch10 roses, Gate Clerk & Woman with a Trowel (story/28_SCRIPT_CH10.md),
        Thornguard Captain/Sentry (S115/S165 lore), North exit -> 280 (36, 85) up, and PBMoveRoute::BACKWARD-guarded
        South exit -> unbuilt 693 The Briarway (ZERO dev meta-text!).
  - Map 288: Briar Hall - Royal Gallery      (41x15, Mansion Interior, TS 59 PF Rejuv Manor, :NONE)
      * Grand Thorne royal portrait corridor matching 286 Great Hall & 207 Mural Gallery gold craft: 4 deepened
        recessed portrait alcoves (mn_portK/Q/F + mn_company), solid historical plaques (0 over_trigger?), intact
        overhead chandeliers (L[2]==0 guard!), velvet crimson runner, white lilies, Royal Archivist & Thornguard,
        full-width West return -> 286 Great Hall (26, 13) left, SE ornate recessed stair -> 289 Thorn Crypts (17, 5)!
  - Map 289: Briar Hall - Thorn Crypts       (35x31, Gothic Ruins Interior, TS 59 PF Rejuv Manor cvL, :CAVE)
      * Root-entangled subterranean royal tombs beneath Briar Hall where "nothing rots in the grey starving soil":
        ancient Thorne sarcophagi (mn_grave_l/r), glowing root-fungi lanterns (cv_fung0), 100% intact iron braziers,
        crumbling gothic arches, solid sovereign epitaph plaques (0 over_trigger?), canonical PBS trainer
        [CHANNELER, Griselda] (pbs/trainers.txt:19048, 100% open sightline!), treasure alcove (CLEANSETAG, DUSKBALL,
        REVIVE, hidden RAREBONE), Crypt Sexton, and full-width North ascending stair -> 288 Royal Gallery (35, 10) up!
  - Map 294: The Heartgarden                 (40x40, Outdoor, TS 55 PF Rejuv City, :FLOWER_GARDEN, rubric: true)
      * Sacred sunken royal sanctuary around THE BRIDE TREE (Aunt Elin, Fixed in AF 288): monumental white-blossomed
        centerpiece ringed by a shimmering stone-coped reflecting moat, 4 cardinal cedar bridges, 4 terraced floral
        quadrants, Rowan's Potting Shed (NOT SEEDS lore), Chapel Steps, live Juno Hale hooks
        (pf_trial_ready?(:JUNO_BRIDE_TREE) -> pf_trial_talk(:JUNO_BRIDE_TREE) [EL_BRIDE_TREE_HEART / VENUSAURITE] +
        :PG_JUNO_BRIDE_TREE + Ch10 Aunt Elin / S182 Venam's Testimony / EL_EVER_BLOOM), conditional Ogerpon (S223 +
        :PG_BRIDE_TREE_OGRE), reactive Thornguard (S165/S125), Quiet Way board (:ELOWEN), West gate -> 283 (44, 12),
        and PBMoveRoute::BACKWARD-guarded South Veil Stair -> unbuilt 708 The Bride Grove!
  - Map 296: Verdance - Rootward             (44x32, Outdoor, TS 55 PF Rejuv City, :FLOWER_GARDEN, rubric: true)
      * Shaded lower-terrace working quarter beneath Verdance's retaining arches & grey starving soil: stepped north
        limestone retaining wall, drainage runnel & timber footbridges, tenement cottages, laundry lines (hb_washline,
        pf_p_laundry), communal washbasins & dead well, Rootward Laundress (canonical EL_ROOTWARD_WAKE hook + S124/S125
        reactivity), Mourner Sympathiser, North stair -> 283 (15, 36) up, West upper alley -> 280 (9, 75) left, and
        PBMoveRoute::BACKWARD-guarded East Root-Road Arch -> unbuilt 690 Lanternroot!

Run:
    /usr/bin/python3 -I mapgen/layouts/verdance_wards.py
"""
import os
import sys
import math
import random
import subprocess
import tempfile
from collections import deque
import numpy as np
import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cavekit import Cave, FLOOR, TER, MASS, P1
import rkit as K
from rkit import C, STAMPS
import rcompose as RC
import render as R
import passguard as PG
from terrain import vnoise
from verdance_palace import Palace
from wave10_towns_craft import (
    ROYAL_CANOPY,
    reserve_mask,
    seal_unconnected_edges,
    can_put_clean,
    put_safe,
    place_canopy_grove,
    paint_rail_run,
    add_festoon_strings,
    add_warm_glows,
    add_water_glints,
)

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TID_CITY = 55
TID_MANOR = 59
VERD_POS = [0, 14, 12]

# Verified bridge planks (exact same cedar planks used across Verdance 280!)
BRIDGE_P = [C('ak', 1524), C('ak', 1525), C('ak', 1526)]
T_PETALS = P1('mn_petals')
T_MAT_L = 24335
T_MAT_R = 24336


# =================================================================================================
# Shared Event, Verification, Border-Seal & Safe-Overlay Helpers
# =================================================================================================
def _guarded_unbuilt_transfer(map_id, tx, ty, direction, blocked_text):
    """Guarded exit to an unbuilt map with canonical Essentials v21 PBMoveRoute::BACKWARD step-back (0 warnings)."""
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


def _add_safe_overlay(Lr, tid, stamp_name, pts):
    """Stamp overhead sunbeams / glow halos strictly onto unoccupied L[2] cells (NEVER deletes flames/chandeliers!)."""
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
    """Verify ZERO unguarded walkable cells on all 4 outer perimeter borders of an outdoor map!"""
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


def _verify_map(Lr, tid, events, start, label, outdoor=False, targets=None):
    """Full 4-bit Essentials BFS + zero over_trigger? + 100% open trainer sightlines + Ruby syntax + outdoor border seal!"""
    import build as B
    ts = R.tilesets()[tid]
    H, W = Lr.shape[1:]
    _check_ruby_syntax(events, label)
    if outdoor:
        _assert_zero_border_leaks(Lr, tid, events, label)

    solid_ev = set()
    by_cell = {}
    for e in events:
        if e and e.get('at'):
            by_cell.setdefault(tuple(e['at']), []).append(e)
            t = e.get('type')
            if t in ('npc', 'trainer', 'mart'):
                solid_ev.add(tuple(e['at']))
            elif t == 'event':
                pg0 = (e.get('pages') or [{}])[0]
                g = pg0.get('graphic') or {}
                if not pg0.get('through') and (g.get('sprite') or (g.get('tile') and (ts['passages'][g['tile']] & 0x0f) == 0x0f)):
                    solid_ev.add(tuple(e['at']))

    # 1. over_trigger?, NPC/trainer spawn passability & trainer sightline audit
    for e in events:
        if e.get('type') == 'sign':
            x, y = e['at']
            assert not B.cell_passable(Lr, ts, x, y), f'{label}: over_trigger? Sign {e.get("name")} at ({x},{y}) on walkable tile!'
        elif e.get('type') == 'event':
            x, y = e['at']
            for idx, pg in enumerate(e.get('pages') or []):
                g = pg.get('graphic') or {}
                if g.get('sprite') and not pg.get('through'):
                    assert B.cell_passable(Lr, ts, x, y), (
                        f'{label}: Sprite NPC {e.get("name")} p{idx} spawned on SOLID tile ({x},{y})!'
                    )
                if pg.get('trigger', 'action') == 'action' and pg.get('commands'):
                    if g.get('sprite'):
                        continue
                    tid_g = g.get('tile')
                    if tid_g:
                        assert (ts['passages'][tid_g] & 0x0f) == 0x0f, f'{label}: over_trigger? Event {e.get("name")} p{idx} walkable tile {tid_g}'
                    else:
                        assert not B.cell_passable(Lr, ts, x, y), f'{label}: over_trigger? Blank action event {e.get("name")} at ({x},{y}) on walkable tile!'
        elif e.get('type') == 'item' and not e.get('hidden'):
            ix, iy = e['at']
            assert B.cell_passable(Lr, ts, ix, iy), f'{label}: Item {e.get("name")} spawned on SOLID tile ({ix},{iy})!'
        elif e.get('type') == 'trainer':
            tx, ty = e['at']
            assert B.cell_passable(Lr, ts, tx, ty), f'{label}: Trainer {e["trainer"]} spawned on SOLID tile ({tx},{ty})!'
            d = e['dir']
            sight = e.get('sight', 3)
            dx, dy = {'down': (0, 1), 'up': (0, -1), 'left': (-1, 0), 'right': (1, 0)}[d]
            for step in range(1, sight + 1):
                cx, cy = tx + dx * step, ty + dy * step
                assert 0 <= cx < W and 0 <= cy < H, f'{label}: Trainer {e["trainer"]} LoS OOB at ({cx},{cy})'
                assert B.cell_passable(Lr, ts, cx, cy) and (cx, cy) not in solid_ev, (
                    f'{label}: Trainer {e["trainer"]} sightline BLOCKED at step {step} ({cx},{cy})!'
                )

    # 2. 4-bit directional BFS from start
    def dir_ok(x, y, d):
        bit = 1 << (d // 2 - 1)
        for e in by_cell.get((x, y), []):
            t = e.get('type')
            if t in ('npc', 'trainer', 'mart'):
                return False
            if t == 'event':
                pg0 = (e.get('pages') or [{}])[0]
                if pg0.get('through') or pg0.get('cond'):
                    continue
                g = pg0.get('graphic') or {}
                if g.get('tile'):
                    p = ts['passages'][g['tile']]
                    if p & bit or (p & 0x0f) == 0x0f:
                        return False
                    if ts['priorities'][g['tile']] == 0:
                        return True
                elif g.get('sprite'):
                    return False
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

    # Check every event is reachable (either directly or orthogonally adjacent)
    check_list = targets if targets is not None else [
        (e.get('name', e.get('type', 'ev')), tuple(e['at']), e.get('type') not in ('warp', 'exit'))
        for e in events if e.get('at')
    ]
    missing = []
    for nm, (tx, ty), adj in check_list:
        if adj:
            ok = (tx, ty) in seen or any((tx + dx, ty + dy) in seen for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)))
        else:
            ok = (tx, ty) in seen
        if not ok:
            missing.append((nm, (tx, ty)))
    print(f'{label}: reached {len(seen)} cells from {start}; missing={missing}')
    assert not missing, f'{label}: unreachable events/targets: {missing}'
    return seen


def _paint_bridge_ns(m, x0, x1, y0, y1):
    """Paint crisp cedar boardwalk bridge (exact Verdance 280 style) spanning a horizontal canal."""
    w = x1 - x0 + 1
    for y in range(y0, y1 + 1):
        for i, x in enumerate(range(x0, x1 + 1)):
            col = 0 if i == 0 else (2 if i == w - 1 else 1)
            m.L[0, y, x] = BRIDGE_P[col]
            m.L[1, y, x] = 0
            m.L[2, y, x] = 0


def _paint_bridge_ew(m, x0, x1, y_top, y_bot, rail_north=True, under_beam=True):
    """Paint framed horizontal cedar plank footbridge spanning a vertical moat:
    - Walkable bordered cedar planks across y_top..y_bot (top/bottom plank seams!)
    - Optional timber balustrade railing along y_top-1 over water cells
    - Optional wooden under-beam/pilings along y_bot+1 over water cells (solid pas=0xf!)
    """
    top_p = [C('ak', 1516), C('ak', 1517), C('ak', 1518)]
    mid_p = [C('ak', 1524), C('ak', 1525), C('ak', 1526)]
    bot_p = [C('ak', 1532), C('ak', 1533), C('ak', 1534)]
    beam_p = [C('ak', 1540), C('ak', 1541), C('ak', 1542)]
    rw, rm, re = P1('lm_railing_w'), P1('lm_railing_m'), P1('lm_railing_e')
    for y in range(y_top, y_bot + 1):
        row = top_p if y == y_top else (bot_p if y == y_bot else mid_p)
        for x in range(x0, x1 + 1):
            m.L[0, y, x] = row[1]
            m.L[1, y, x] = 0
            m.L[2, y, x] = 0
    if rail_north and y_top - 1 >= 0:
        ry = y_top - 1
        span = [x for x in range(x0, x1 + 1) if m.cls[ry, x] in ('w', 'W')]
        for idx, x in enumerate(span):
            t = rw if idx == 0 else (re if idx == len(span) - 1 else rm)
            m.L[1, ry, x] = t
            m.L[2, ry, x] = 0
    if under_beam and y_bot + 1 < m.H:
        by = y_bot + 1
        span = [x for x in range(x0, x1 + 1) if m.cls[by, x] in ('w', 'W')]
        for idx, x in enumerate(span):
            t = beam_p[0] if idx == 0 else (beam_p[2] if idx == len(span) - 1 else beam_p[1])
            m.L[1, by, x] = t
            m.L[2, by, x] = 0


# =================================================================================================
# 1. MAP 283 — VERDANCE - GLASSHOUSE WARD (48x40, Outdoor, TS 55, :FLOWER_GARDEN, rubric: true)
# =================================================================================================
def build_283():
    W, H = 48, 40
    m = K.RMap(W, H, TID_CITY, 283, water='Ocean', kit={1: 'rw', 'default': 'qy'})
    m.keep_under = 'cfdg'
    m.gv_dark = 0.48

    # ---- 1. Two Stepped Botanical Terraces + Shimmering Conservatory Canal ----
    # Upper North Conservatory Terrace (ht=1): y=0..15, flat royal garden terrace housing Gym 9 & Glasshouses!
    for y in range(0, 16):
        for x in range(0, W):
            m.ht[y, x] = 1
    # Clean stair landing across central Gym 9 approach (x=22..26, lip y=15, stairs y=15..17)
    for y in range(13, 16):
        for x in range(20, 29):
            m.ht[y, x] = 1
    for y in range(16, 20):
        for x in range(20, 29):
            m.ht[y, x] = 0

    # Shimmering Briarwater Conservatory Canal across y=24..26 (spanned by West & East cedar footbridges!)
    for x in range(0, W):
        cy = 25 + int(round(0.9 * math.sin(x / 9.0)))
        for y in range(cy - 1, cy + 2):
            if 0 <= y < H:
                m.ht[y, x] = 0
                m.cls[y, x] = 'w'
        if 3 <= x < W - 3 and not (12 <= x <= 17 or 31 <= x <= 36):
            m.cls[cy, x] = 'W'

    # Seal outer forest border (leaving exact clean gate openings on West, NE, and SW!)
    for y in range(H):
        for x in range(W):
            if m.cls[y, x] != '.':
                continue
            outer = (x < 3 or x > W - 4 or y < 2 or y > H - 3)
            if x <= 3 and 18 <= y <= 20:
                outer = False
            if x >= W - 4 and 11 <= y <= 13:
                outer = False
            if 14 <= x <= 16 and y >= H - 4:
                outer = False
            if outer:
                m.cls[y, x] = 'T'

    # Grand 5-wide Royal Stone Staircase ascending to Upper Conservatory Terrace (x=22..26, y=15..17)
    m.stairs(22, 15, w=5, kit_rows=3, kind='stone', c='f')
    m.plan_cliffs(rows=3)

    # ---- 2. Flagstone Conservatory Plazas, Brick Rose-Garden Walks & Sightlines ----
    # Upper Conservatory Terrace Flagstone Promenade (y=9..15) + NE passage to 294 Heartgarden!
    m.rect(17, 9, 15, 6, 'f', only='.tTc')
    m.lane([(6, 12.5), (18, 12.5), (31, 12.5), (46, 12.0)], c='f', w=3.2, seed=1, only='.tT', wobble=0.08)
    # Central Lower Rose Court (y=18..23) linking West Gate (280), Gym Stair, and BOTH Canal Bridges!
    m.rect(20, 18, 9, 5, 'f', only='.tTc')
    m.lane([(1, 19), (14, 19.5), (24, 20), (34, 20), (42, 20)], c='c', w=3.2, seed=2, only='.tT', wobble=0.1)
    # South Conservatory Terrace (south of canal, y=28..37) + SW Stairway to 296 Rootward!
    m.blob(24, 32, 11.5, 4.2, 'f', seed=3, rough=0.2, only='.tTc')
    m.lane([(14.5, 27), (15, 33), (15, 38)], c='c', w=3.2, seed=4, only='.tT', wobble=0.08)
    m.lane([(33.5, 27), (33.5, 32), (24, 32), (15, 32)], c='c', w=3.0, seed=5, only='.tT', wobble=0.08)
    m.lane([(7, 32), (15, 32)], c='c', w=2.4, seed=6, only='.tT', wobble=0.08)
    for c in 'cf':
        m.smooth(c, into='.', passes=1, only='.tT')

    # Re-assert Conservatory Canal so roads never ford outside the two cedar bridges!
    for x in range(0, W):
        cy = 25 + int(round(0.9 * math.sin(x / 9.0)))
        for y in range(cy - 1, cy + 2):
            if 0 <= y < H:
                m.cls[y, x] = 'W' if (y == cy and 3 <= x < W - 3 and not (12 <= x <= 17 or 31 <= x <= 36)) else 'w'

    # ---- 3. Botanical Glasshouses, Guild Halls & Verdance Gym 9 Conservatory Facade ----
    # Centerpiece: Verdance Gym 9 — The Heartgarden Conservatory (`lb_council` 12x6 at (18, 3) -> arched door at (24, 8)!)
    m.stamp('lb_council', 18, 3)
    # West Domed Glasshouse (`lb_lab` 7x6 at (5, 3)) & East Domed Glasshouse (`lb_lab` 7x6 at (33, 3))!
    m.stamp('lb_lab', 5, 3)
    m.stamp('lb_lab', 33, 3)
    # South Botanical Conservatory Galleria (`lb_arcade` 12x5 at (19, 34) — crystal greenhouse facade!)
    m.stamp('lb_arcade', 19, 34)
    # Vine-draped limestone Guild Villa (SW) & Botanical Tea House (SE) framing the South Rose Terrace!
    m.stamp('lb_t7b', 4, 28)
    m.stamp('sp_cafe', 38, 28)

    # Grand Blossoming Floral Archway (`wb_gate` 5x5) framing the stair approach into Gym 9 at (22, 10)!
    # wb_gate feet at (22,14) & (26,14); open 3-wide floral archway x=23..25 directly aligned with Gym Door (24, 8)!
    m.stamp('wb_gate', 22, 10)

    # ---- 4. Events, Warps, Quiet Way Board, Ch10 Runaway-Bloom Botanists & Items ----
    E = []
    # Gym 9 Grand Conservatory Archway Door (24, 8) -> 290 Verdance Gym - Entrance (10, 15) up!
    E.append({
        'type': 'warp',
        'name': 'Verdance Gym - Entrance (290)',
        'at': [24, 8],
        'to': {'map': 290, 'x': 10, 'y': 15, 'dir': 'up'},
        'se': 'Door enter',
    })
    # West Gate (1, 18..20) -> 280 Verdance - Market Terraces (96, 66) left!
    for wy in (18, 19, 20):
        E.append({
            'type': 'warp',
            'name': f'West to Market Terraces {wy}',
            'at': [1, wy],
            'to': {'map': 280, 'x': 96, 'y': 66, 'dir': 'left'},
            'se': 'Door exit',
        })
    # North-East Gate (46, 11..13) -> 294 The Heartgarden (3, 20) right!
    for ey in (11, 12, 13):
        E.append({
            'type': 'warp',
            'name': f'East to Heartgarden {ey}',
            'at': [46, ey],
            'to': {'map': 294, 'x': 3, 'y': 20, 'dir': 'right'},
            'se': 'Door enter',
        })
    # South-West Stairway (14..16, 38) -> 296 Verdance - Rootward (21, 3) down!
    for sx in (14, 15, 16):
        E.append({
            'type': 'warp',
            'name': f'South to Rootward {sx}',
            'at': [sx, 38],
            'to': {'map': 296, 'x': 21, 'y': 3, 'dir': 'down'},
            'se': 'Door exit',
        })

    # Readable Solid Signposts (pf_signpost base tile pas=0xf -> 0 over_trigger?!)
    E.append(_sign('Gym 9 Sign', (21, 11),
                   "HEARTGARDEN GYM — VERDANCE\nWarden: Juno Hale (Grass)\n\"Mind the beds — gardens are gossips.\""))
    E.append(_sign('Glasshouse Ward Sign', (6, 21),
                   "VERDANCE — GLASSHOUSE WARD\n← Market Terraces · ↑ Heartgarden Gym · → The Heartgarden · ↓ Rootward Steps"))
    E.append(_sign('Heartgarden Way Sign', (42, 14),
                   "THE HEARTGARDEN — East through the rose walk.\nHome of the Bride Tree."))

    # Quiet Way Lantern Rope / Trial Board (live pf_trial_board(:ELOWEN) across BOTH solid base tiles (28..29, 21)!)
    board_ruby = '''if defined?(pf_trial_board)
  pf_trial_board(:ELOWEN)
else
  pbMessage(_INTL("The Quiet Way's lantern rope hangs heavy with wax-sealed notes from Verdance's wards."))
end'''
    for bx in (28, 29):
        E.append({
            'type': 'event',
            'name': 'Quiet Way Lantern Board' if bx == 29 else 'Quiet Way Lantern Board L',
            'at': [bx, 21],
            'pages': [{'trigger': 'action', 'commands': [{'script': board_ruby}]}],
        })

    # Ch10 Runaway-Bloom Botanists & Glaziers (reactive to S125 CH10_JUNO_WARDEN!)
    botanist_ruby = '''if $game_switches[125]
  pbMessage(_INTL("Head Botanist: Once young Juno laid her bare hand on the Meadow Plate, every climbing rose in the ward settled right back onto its trellis."))
  pbMessage(_INTL("Head Botanist: Even old Rowan's prize orchids stopped tapping on the glass. She's a true Warden, fifteen or not."))
else
  pbMessage(_INTL("Head Botanist: Three days without a Warden and the glasshouses are bursting at the seams!"))
  pbMessage(_INTL("Head Botanist: Roses pushed clean through two leaded mullions overnight. Keep your pollen mask handy!"))
end'''
    E.append({
        'type': 'event',
        'name': 'Head Botanist',
        'at': [14, 12],
        'pages': [{'graphic': {'sprite': 'NPC 11', 'dir': 'down'}, 'trigger': 'action', 'move': 'fixed',
                   'commands': [{'script': botanist_ruby}]}],
    })

    glazier_ruby = '''if $game_switches[125]
  pbMessage(_INTL("Glasshouse Glazier: Finally catching up on replacing the cracked conservatory panes! Juno even brought us hot cider this morning."))
else
  pbMessage(_INTL("Glasshouse Glazier: I mend a pane at noon and a briar shoot pops it back out by tea! Everything's growing too fast and nothing's composting underneath."))
end'''
    E.append({
        'type': 'event',
        'name': 'Glasshouse Glazier',
        'at': [36, 12],
        'pages': [{'graphic': {'sprite': 'NPC 13', 'dir': 'left'}, 'trigger': 'action', 'move': 'fixed',
                   'commands': [{'script': glazier_ruby}]}],
    })

    E.append(_make_npc('Pollen-Masked Noble', (22, 31), 'NPC 08', 'right', [
        "Noble: You'd think living above the Market Terraces would keep the pollen out. Instead it drifts up here like golden snow.",
        "Noble: If you take the south-west stairs down into Rootward, mind your boots — the soil down under the arches is grey as ash.",
    ], move='random'))
    E.append(_make_npc('Botanical Apprentice', (31, 31), 'NPC 05', 'up', [
        "Apprentice: Warden Juno set up a watering puzzle inside the Heartgarden Gym! Every hedge you leave overgrown makes her Flower Garden start taller.",
    ]))

    # Verified PBS Items
    E.append({'type': 'item', 'name': 'Item (Leaf Stone)', 'at': [9, 34], 'item': 'LEAFSTONE'})
    E.append({'type': 'item', 'name': 'Item (Big Root)', 'at': [40, 22], 'item': 'BIGROOT'})
    E.append({'type': 'item', 'name': 'HiddenItem (Miracle Seed)', 'at': [39, 10], 'item': 'MIRACLESEED', 'hidden': True})

    m.events += E
    key_pts = [tuple(e['at']) for e in E] + [
        (24, 9), (24, 10), (24, 11), (24, 12), (24, 13), (24, 14), (24, 15), (24, 16), (24, 17), (24, 18),
        (2, 19), (3, 19), (44, 12), (45, 12), (15, 36), (15, 37),
        (14, 24), (15, 24), (14, 27), (15, 27), (33, 24), (34, 24), (33, 27), (34, 27),
    ]
    prot = reserve_mask(m, key_pts, pad=1)
    # Protect front-wall aprons & doorsteps of lb_t7b (4..10, 28..33) and sp_cafe (38..42, 28..33) from tree clipping!
    for bx0, by0, bx1, by1 in ((3, 27, 11, 35), (37, 27, 43, 35)):
        for py in range(by0, by1 + 1):
            for px in range(bx0, bx1 + 1):
                if m.inb(px, py):
                    prot[py, px] = True
    for x, y in key_pts:
        if m.inb(x, y):
            m.taken[y, x] = True

    # ---- 5. Rose-Garden Beds, Fountains, Lanterns, Balustrades & Overlapping Blossom Groves ----
    # Solid signposts & Quiet Way shrine board (exact event bases!)
    m.stamp('pf_signpost', 21, 10)          # Gym 9 Sign base (21, 11)
    m.stamp('pf_signpost', 6, 20)           # Ward Sign base (6, 21)
    m.stamp('pf_signpost', 42, 13)          # Heartgarden Way Sign base (42, 14)
    m.stamp('pf_shrine', 28, 19)            # Quiet Way Lantern Board solid base (28..29, 20..21) -> both pas=0xf!

    lamp_pts = []
    for nm, x, y in (
        ('pf_fountain', 22, 28),
        ('lm_topiary', 17, 9), ('lm_topiary', 30, 9), ('lm_topiary', 19, 14), ('lm_topiary', 29, 14),
        ('pf_planter0', 18, 10), ('pf_planter1', 28, 10), ('pf_planter2', 8, 11), ('pf_planter3', 35, 11),
        ('pf_planter0', 19, 22), ('pf_planter2', 28, 22), ('pf_planter1', 19, 32), ('pf_planter3', 28, 32),
        ('pf_stonebench', 12, 14), ('pf_stonebench', 35, 14), ('pf_stonebench', 19, 29), ('pf_stonebench', 28, 29),
        ('nt_azalea2', 11, 21), ('nt_azalea0', 17, 21), ('nt_azalea1', 31, 21), ('nt_azalea2', 36, 21),
        ('nt_azalea2', 7, 35), ('nt_azalea0', 37, 35), ('nt_shrub1', 42, 28), ('nt_shrub0', 9, 14),
    ):
        put_safe(m, nm, x, y, on='.fc', r=1, prot=prot)

    for lx, ly in ((20, 14), (28, 14), (10, 14), (39, 14), (12, 21), (17, 21), (31, 21), (36, 21),
                   (12, 29), (17, 29), (31, 29), (36, 29), (13, 36), (17, 36), (4, 18), (44, 11)):
        if can_put_clean(m, 'pf_lantern', lx, ly - 2, on='.fc', prot=prot):
            m.stamp('pf_lantern', lx, ly - 2)
            lamp_pts.append((lx, ly - 1))

    # Wrought limestone balustrades overlooking Upper Conservatory Terrace & Canal banks!
    paint_rail_run(m, 6, 21, 15, kind='rw')
    paint_rail_run(m, 27, 42, 15, kind='rw')
    paint_rail_run(m, 5, 12, 23, kind='qy')
    paint_rail_run(m, 18, 31, 23, kind='qy')
    paint_rail_run(m, 37, 43, 23, kind='qy')

    # Overlapping lush cherry-blossom & royal emerald canopy groves (well clear of buildings & outer treeline!)
    for idx, (cx, cy) in enumerate(((4, 8), (43, 8), (43, 20), (3, 36), (44, 35), (15, 7), (32, 7))):
        place_canopy_grove(m, cx, cy, ROYAL_CANOPY, count=3, radius=2.1, on='.', seed=idx + 11, prot=prot, undergrowth=True)

    m.greenfill(4)
    m.paint()

    # Royal crimson-gold welcome carpet leading from Floral Archway (24, 14) straight into Gym 9 door (24, 8)!
    for y in range(9, 15):
        for i, x in enumerate((23, 24, 25)):
            part = ('n' if y == 9 else 's' if y == 14 else '') + ('w' if i == 0 else 'e' if i == 2 else '')
            t = P1('lm_carpet_' + (part or 'c'))
            m.L[0, y, x] = t
            if m.L[1, y, x] >= K.RC.VBASE:
                m.L[1, y, x] = 0
    for wy in (8, 9, 10):
        m.L[2, wy, 24] = 0

    # Paint TWO wide cedar footbridges across the Conservatory Canal (x=13..16 & x=32..35)!
    _paint_bridge_ns(m, 13, 16, 23, 27)
    _paint_bridge_ns(m, 32, 35, 23, 27)

    # Overhead festoon lantern strings across bridges & conservatory plaza + lamp-only warm glows & water glints!
    add_festoon_strings(m, [(13, 16, 25, 0), (32, 35, 25, 2), (20, 28, 19, 1), (19, 29, 31, 0)], kind='lstring')
    add_warm_glows(m, lamp_pts)
    add_water_glints(m, water_cls='wW', seed=283, density=0.05)
    m.scatter(12, seed=283, on='.T')

    # Seal open walkable warp flanks directly beside West (1,18..20), East (46,11..13) & South (14..16,38) strips!
    for fx, fy in ((1, 17), (1, 21), (46, 10), (46, 14), (13, 38), (17, 38)):
        if m.L[1, fy, fx] == 0:
            m.L[1, fy, fx] = P1('nt_bush0')

    # Seal ALL 4 perimeter borders (0 border leaks!) — warps sit cleanly inside at x=1, x=46, y=38!
    seal_unconnected_edges(m, open_cells=())

    Lr = RC.resolve(m.L, TID_CITY).astype(np.int32)
    ev_pts = [tuple(e['at']) for e in m.events]
    PG.guard(Lr, TID_CITY, ev_pts, 'Map 283')
    assert not PG.hits(Lr, R.tilesets()[TID_CITY], ev_pts), 'Map 283 passguard hits!'
    _verify_map(Lr, TID_CITY, m.events, (24, 10), 'Map 283 Glasshouse Ward', outdoor=True)

    np.save(os.path.join(HERE, 'data', 'raw', '283.npy'), Lr.astype(np.int16))
    spec = {
        'id': 283,
        'name': 'Verdance - Glasshouse Ward',
        'parent': 280,
        'bgm': 'Natural Park',
        'field': 'FLOWER_GARDEN',
        'rubric': True,
        'yards_ok': True,
        'map_audio': {'bgm': 'Town - Elowen', 'bgs': 'Gossamer Deepwood', 'bgs_volume': 45},
        'tone': [-4, 10, -10, 0],
        'fog': {'name': 'prismfall_spores', 'opacity': 16, 'blend': 1, 'zoom': 100, 'sx': 1, 'sy': 0},
        'metadata': {'Name': 'Verdance - Glasshouse Ward', 'Outdoor': True, 'ShowArea': True, 'Bicycle': True,
                     'MapPosition': VERD_POS, 'BattleBack': 'field'},
        'biome': 'city',
        'tileset': TID_CITY,
        'raw': 'data/raw/283.npy',
        'events': m.events,
    }
    with open(os.path.join(HERE, 'specs', '283_verdance_glasshouse_ward.yaml'), 'w', encoding='utf-8') as f:
        f.write('# GENERATED by mapgen/layouts/verdance_wards.py (Batch 3E): Verdance - Glasshouse Ward.\n')
        f.write(yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))
    print('Wrote specs/283_verdance_glasshouse_ward.yaml and data/raw/283.npy')


# =================================================================================================
# 2. MAP 284 — VERDANCE - KINGSGATE BARBICAN (40x24, Outdoor, TS 55, :FLOWER_GARDEN, rubric: true)
# =================================================================================================
def build_284():
    W, H = 40, 24
    m = K.RMap(W, H, TID_CITY, 284, water='Ocean', kit={1: 'rw', 'default': 'rw'})
    m.keep_under = 'cfdg'
    m.gv_dark = 0.50

    # ---- 1. Real Fortified Royal Limestone Curtain Walls, Cobble Parade Yard & Briar-Lined Flanking Woods ----
    # Elevated North Curtain Ramparts (ht=1, y=0..4) linking outer corner watchtowers (5..7 & 32..34) directly into gt_gate6 (14..25)!
    for y in range(0, 5):
        for x in range(8, 14):
            m.ht[y, x] = 1
        for x in range(26, 32):
            m.ht[y, x] = 1

    # Dense royal briar forest along outer West (x=0..4) & East (x=35..39) flanks
    for y in range(H):
        for x in range(W):
            if x < 5 or x > W - 6 or y < 2 or y > H - 2:
                m.cls[y, x] = 'T'
    # Keep raised north curtain terrace open for stone parapets (y=2..4, x=8..13 & 26..31)
    for y in range(2, 5):
        for x in list(range(8, 14)) + list(range(26, 32)):
            m.cls[y, x] = 'f'

    m.plan_cliffs(rows=3)

    # Carve central fortified Parade Yard & twin gatehouse approaches
    m.rect(7, 7, 26, 11, '.')
    m.rect(16, 4, 8, 20, 'c')
    m.rect(12, 9, 16, 7, 'f', only='.tTc')
    m.lane([(8, 13), (31, 13)], c='c', w=2.8, seed=2, only='.tT', wobble=0.08)
    for c in 'cf':
        m.smooth(c, into='.', passes=1, only='.tT')
    # Full 6-wide cobblestone threshold squarely meeting the 6-wide North Barbican Arch (17..22, 6..8)!
    m.rect(17, 7, 6, 2, 'c')

    # ---- 2. Monumental Twin Barbican Gatehouses, 2 Corner Watchtowers & Continuous Stone Curtain Walls ----
    # North Inner Barbican Curtain Gate: `gt_gate6` (12x8 at (14, 0) -> open 6-wide arch x=17..22 at y=6..7!)
    m.stamp('gt_gate6', 14, 0)
    # ONLY TWO outer corner flanking watchtowers anchoring the West & East ends of the North Stone Curtain Wall!
    m.stamp('gt_tower', 5, 1)
    m.stamp('gt_tower', 32, 1)
    # South Outer Barbican Portcullis Gate: `gt_gate4` (10x8 at (15, 16) -> open 4-wide arch x=18..21 at y=22..23!)
    m.stamp('gt_gate4', 15, 16)
    # West & East Guardhouse Barracks flanking the parade yard (cleanly clear of y=6 curtain wall!)
    m.stamp('gl_shed', 7, 9)
    m.stamp('gl_shed', 29, 9)

    # ---- 3. Events: Full 6-Wide North -> 280, BACKWARD-Guarded South -> 693, Ch10 Gate Clerk, Woman w/ Trowel, Thornguard ----
    E = []
    # Full 6-wide North Barbican Arch (17..22, 6) -> 280 Verdance - Market Terraces (36, 85) up (ZERO dead doorway tiles!)
    for nx in range(17, 23):
        E.append({
            'type': 'warp',
            'name': f'North to Market Terraces {nx}',
            'at': [nx, 6],
            'to': {'map': 280, 'x': 36, 'y': 85, 'dir': 'up'},
            'se': 'Door enter',
        })
    # South Barbican Arch (18..21, 22) -> PBMoveRoute::BACKWARD-guarded exit to unbuilt 693 The Briarway!
    briar_msg = (
        "Thornguard Sentry: Hold there, traveller — runaway briar shoots as thick as a wrist have vaulted clear across "
        "the Briarway south of the Kingsgate. The royal clippers are cutting a lane through; try the north arch into Verdance for now."
    )
    for sx in (18, 19, 20, 21):
        E.append({
            'type': 'event',
            'name': f'South to The Briarway {sx}',
            'at': [sx, 22],
            'pages': [{
                'trigger': 'touch',
                'through': True,
                'commands': _guarded_unbuilt_transfer(693, 36, 4, 'down', briar_msg),
            }],
        })

    # Canonical Ch10 Arrival NPCs (story/28_SCRIPT_CH10.md:231-237)
    clerk_ruby = '''if $game_switches[125]
  pbMessage(_INTL("Gate Clerk: You can tuck the pollen cloth in your pocket now — once Warden Juno steadied the Meadow Plate, the air cleared before evening."))
  pbMessage(_INTL("Gate Clerk: Even the bakers down on the Market Terraces got a loaf out of the oven without it sprouting clover!"))
else
  pbMessage(_INTL("Gate Clerk: Pollen. Take a cloth mask — it's not poison, it just won't stop."))
  pbMessage(_INTL("Gate Clerk: Since the Warden went, the Meadow Plate's had nobody to hold it in. Three days and the whole city's drowning in roses. The bakers can't keep the bread from sprouting!"))
end'''
    E.append({
        'type': 'event',
        'name': 'Gate Clerk',
        'at': [17, 15],
        'pages': [{'graphic': {'sprite': 'NPC 12', 'dir': 'right'}, 'trigger': 'action', 'move': 'fixed',
                   'commands': [{'script': clerk_ruby}]}],
    })

    E.append(_make_npc('Woman with a Trowel', (23, 14), 'NPC 11', 'left', [
        "Woman with a Trowel: Look under the roses I just scraped off these cobbles. Dry, grey soil — and this dead leaf from last autumn hasn't softened an inch.",
        "Woman with a Trowel: Nothing rots in Verdance. My nan used to say it like it was a blessing.",
    ]))

    captain_ruby = '''if $game_switches[165]
  pbMessage(_INTL("Thornguard Captain: By decree of Her Majesty Queen Maelis Thorne, the Kingsgate stands at full guard pending the Heartgarden succession."))
  pbMessage(_INTL("Thornguard Captain: Directorate officers tried to post a Meridian scanner on our barbican this morning. Her Majesty sent them back down the Briarway with a rose each."))
elsif $game_switches[125]
  pbMessage(_INTL("Thornguard Captain: Warden Hale ordered us off the Heartgarden tulips, and the Queen actually laughed. Mind the gate road, challenger."))
else
  pbMessage(_INTL("Thornguard Captain: Keep your papers handy on the Kingsway. Between the Accord Mandate and the runaway bloom, every road into Elowen's under watch."))
end'''
    E.append({
        'type': 'event',
        'name': 'Thornguard Captain',
        'at': [16, 9],
        'pages': [{'graphic': {'sprite': 'trainer_THORNGUARD', 'dir': 'down'}, 'trigger': 'action', 'move': 'fixed',
                   'commands': [{'script': captain_ruby}]}],
    })
    E.append(_make_npc('Thornguard Sentry', (23, 9), 'trainer_THORNGUARD', 'down', [
        "Thornguard Sentry: Twin gatehouses, royal limestone curtain walls, and three centuries of clipped briar. Not even Ironreach's trouble crosses the Kingsgate uninvited.",
    ]))

    # Solid Barbican Signpost (pf_signpost base (14, 15) pas=0xf!) + pickup
    E.append(_sign('Kingsgate Barbican Sign', (14, 15),
                   "KINGSGATE BARBICAN — SOUTHERN APPROACH OF VERDANCE\n↑ Market Terraces & Briar Hall · ↓ The Briarway (Royal Road)"))
    E.append({'type': 'item', 'name': 'Item (Hyper Potion)', 'at': [10, 16], 'item': 'HYPERPOTION'})

    m.events += E
    key_pts = [tuple(e['at']) for e in E] + [
        (17, 7), (18, 7), (19, 7), (20, 7), (21, 7), (22, 7), (19, 8), (20, 8),
        (18, 21), (19, 21), (20, 21), (21, 21), (19, 20), (20, 20),
        (19, 12), (20, 12), (14, 14),
    ]
    prot = reserve_mask(m, key_pts, pad=1)
    for x, y in key_pts:
        if m.inb(x, y):
            m.taken[y, x] = True

    # ---- 4. Stone Parapets, Intact 1x2 Royal Banners, Blazing Gate Beacons, Rose Hedges & Blossom Groves ----
    m.stamp('pf_signpost', 14, 14)     # solid base (14, 15)
    # Stone battlement parapets crowning the North Limestone Curtain Walls!
    paint_rail_run(m, 8, 13, 4, kind='rw')
    paint_rail_run(m, 26, 31, 4, kind='rw')

    lamp_pts = []
    for nm, x, y in (
        ('pf_beacon', 14, 7), ('pf_beacon', 24, 7),
        ('pf_beacon', 13, 17), ('pf_beacon', 25, 17),
        ('nt_azalea2', 12, 10), ('nt_azalea0', 26, 10), ('nt_azalea1', 11, 17), ('nt_azalea2', 27, 17),
        ('pf_planter0', 14, 11), ('pf_planter2', 24, 11),
        ('pf_stonebench', 9, 17), ('pf_stonebench', 29, 17),
        ('sh_crates', 29, 15), ('hb_barrel', 8, 15),
        ('nt_shrub0', 6, 18), ('nt_shrub1', 32, 18),
    ):
        put_safe(m, nm, x, y, on='.fc', r=1, prot=prot)

    for lx, ly in ((16, 13), (23, 13), (12, 13), (27, 13)):
        if can_put_clean(m, 'pf_lantern', lx, ly - 2, on='.fc', prot=prot):
            m.stamp('pf_lantern', lx, ly - 2)
            lamp_pts.append((lx, ly - 1))

    for idx, (cx, cy) in enumerate(((5, 12), (34, 12), (5, 18), (34, 18))):
        place_canopy_grove(m, cx, cy, ROYAL_CANOPY, count=3, radius=1.8, on='.', seed=idx + 30, prot=prot, undergrowth=True)

    m.greenfill(4)
    m.paint()

    # Stamp INTACT full-height 1x2 Royal Evergreen banners cleanly onto the flat North Curtain Wall masonry!
    ban_L = STAMPS['fw_ban_e']['layers']
    for bx, by in ((9, 5), (12, 5), (27, 5), (30, 5)):
        m.L[2, by, bx] = int(ban_L[2][0][0] or ban_L[1][0][0])
        m.L[2, by + 1, bx] = int(ban_L[1][1][0] or ban_L[2][1][0])

    # Build continuous fortified South Limestone Curtain Wall & Battlement Parapets flanking gt_gate4 (x=5..14 & x=25..34)!
    for seg_x0, seg_x1 in ((5, 14), (25, 34)):
        for x in range(seg_x0, seg_x1 + 1):
            is_w, is_e = (x == seg_x0), (x == seg_x1)
            m.L[1, 20, x] = P1('rw_rail_w' if is_w else ('rw_rail_e' if is_e else 'rw_rail_m'))
            m.L[1, 21, x] = P1('rw_f1w0' if is_w else ('rw_f1e0' if is_e else ('rw_f1m1' if x % 2 else 'rw_f1m0')))
            m.L[1, 22, x] = P1('rw_f2w0' if is_w else ('rw_f2e0' if is_e else 'rw_f2m0'))
            m.L[2, 20, x] = 0
            m.L[2, 21, x] = 0
            m.L[2, 22, x] = 0
            if m.L[1, 23, x] == 0:
                m.L[1, 23, x] = P1('nt_bush0')

    # Block rear of North gt_gate6 (y=5, x=17..22) and seal bottom arch shadow (18..21, 23) cleanly with invisible solid tile 505!
    for gx in range(17, 23):
        m.L[1, 5, gx] = P1('rw_f1m0')
    for gx in range(18, 22):
        # Clean cobble road continuing into south arch shadow + invisible pas=0xf blocker 505 on y=23 (ZERO ugly bushes!)
        m.L[2, 23, gx] = 505
    # Ensure full 6-wide north arch (17..22, 6..7) and south guarded strip (18..21, 22) have clean L[2]
    for gx in range(17, 23):
        for gy in (6, 7):
            m.L[2, gy, gx] = 0
    for gx in range(18, 22):
        m.L[2, 22, gx] = 0

    add_festoon_strings(m, [(16, 23, 11, 0), (16, 23, 16, 2)], kind='lstring')
    # Strictly lamp-centered warm glows ONLY (ZERO dark-arch or offset beacon blobs!)
    add_warm_glows(m, lamp_pts)
    m.scatter(12, seed=284, on='.T')
    # Keep gatehouse front aprons crisp and free of stray pond-lilies/flowers (e.g. (24,8))!
    for gx in range(14, 26):
        if m.L[1, 8, gx] not in (0, P1('pf_beacon')) and not m.taken[8, gx]:
            m.L[1, 8, gx] = 0
    seal_unconnected_edges(m, open_cells=())

    Lr = RC.resolve(m.L, TID_CITY).astype(np.int32)
    ev_pts = [tuple(e['at']) for e in m.events]
    PG.guard(Lr, TID_CITY, ev_pts, 'Map 284')
    assert not PG.hits(Lr, R.tilesets()[TID_CITY], ev_pts), 'Map 284 passguard hits!'
    _verify_map(Lr, TID_CITY, m.events, (19, 8), 'Map 284 Kingsgate Barbican', outdoor=True)

    np.save(os.path.join(HERE, 'data', 'raw', '284.npy'), Lr.astype(np.int16))
    spec = {
        'id': 284,
        'name': 'Verdance - Kingsgate Barbican',
        'parent': 280,
        'bgm': 'Natural Park',
        'field': 'FLOWER_GARDEN',
        'rubric': True,
        'yards_ok': True,
        'map_audio': {'bgm': 'Town - Elowen', 'bgs': 'Gossamer Deepwood', 'bgs_volume': 45},
        'tone': [-6, 10, -12, 0],
        'fog': {'name': 'prismfall_spores', 'opacity': 18, 'blend': 1, 'zoom': 100, 'sx': 1, 'sy': 0},
        'metadata': {'Name': 'Verdance - Kingsgate Barbican', 'Outdoor': True, 'ShowArea': True, 'Bicycle': True,
                     'MapPosition': VERD_POS, 'BattleBack': 'field'},
        'biome': 'city',
        'tileset': TID_CITY,
        'raw': 'data/raw/284.npy',
        'events': m.events,
    }
    with open(os.path.join(HERE, 'specs', '284_verdance_kingsgate_barbican.yaml'), 'w', encoding='utf-8') as f:
        f.write('# GENERATED by mapgen/layouts/verdance_wards.py (Batch 3E): Verdance - Kingsgate Barbican.\n')
        f.write(yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))
    print('Wrote specs/284_verdance_kingsgate_barbican.yaml and data/raw/284.npy')


# =================================================================================================
# 3. MAP 288 — BRIAR HALL - ROYAL GALLERY (41x15, Mansion Interior, TS 59 PF Rejuv Manor, :NONE)
# =================================================================================================
def build_288():
    W, H = 41, 15
    m = Palace(W, H, seed=288, tid=TID_MANOR)
    m.STAIRS = tuple(P1('st_stair_' + k) for k in 'lmr')
    Rb = m.room_box

    # ---- 1. Void-Sculpted Royal Portrait Corridor with 4 Deepened North Alcoves + Exact 2-Wide West Portal + SE Crypt Stair ----
    # Main royal gallery nave: x=3..38, y=4..12 + exact 2-wide West entry vestibule (x=1..3, y=6..9 -> floor strictly y=8..9!)
    Rb(3, 4, 38, 12, FLOOR, 'H', 'H')
    m.box(1, 6, 3, 9, FLOOR)
    # Four deepened recessed North Royal Portrait Alcoves (x=7, 16, 25, 34) — ZERO straight sterile box!
    alcove_xs = [7, 16, 25, 34]
    for mx in alcove_xs:
        m.box(mx - 2, 3, mx + 2, 5, FLOOR)
    # Architectural south buttress chamfers (leave SE x=33..37, y=10..12 open for ornate Thorn Crypts stair alcove!)
    m.mass_at([
        (3, 4), (38, 4), (3, 12), (38, 12),
        (11, 12), (20, 12), (29, 12),
    ])
    m.plan_cliffs(rows=3)

    # ---- 2. Ivory Marble + Gold Inlays + Sweeping Royal Crimson-and-Gold Velvet Runner ----
    m.marble_floor(4, 6, 37, 11, 'plaza')
    m.marble_inlay(4, 6, 37, 11)
    for mx in alcove_xs:
        m.marble_floor(mx - 2, 5, mx + 2, 5, 'plaza')
    m.marble_floor(2, 8, 4, 9, 'plaza')
    m.runner(2, 8, 36, 9)

    # ---- 3. Four Framed Royal Monarch Portraits, Banners, Sconces, Fluted Columns & White Lilies (0 sky windows!) ----
    portraits = [('mn_portK', False), ('mn_portQ', False), ('mn_company', True), ('mn_portF', False)]
    for mx, (pt, is_big) in zip(alcove_xs, portraits):
        if is_big:
            m.on('mn_company', mx - 1, 3)         # 2x2 Royal Tapestry spanning (mx-1..mx, 3..4)!
            m.late.append((1, mx - 2, 4, P1('mn_sconce')))
            m.late.append((1, mx + 1, 4, P1('mn_sconce')))
        else:
            m.late.append((1, mx, 4, P1(pt)))     # Royal Monarch Portrait at solid alcove wall (mx, 4)!
            m.late.append((1, mx - 1, 4, P1('mn_sconce')))
            m.late.append((1, mx + 1, 4, P1('mn_sconce')))
        m.on('fw_ban_e', mx - 2, 3)
        m.on('fw_ban_e', mx + 2, 3)
        m.on('mn_plinth', mx - 2, 5)
        m.on('mn_plinth', mx + 2, 5)
        m.on('nr_col', mx - 3, 6)
        m.on('nr_col', mx + 3, 6)

    # South gallery benches, candelabras, royal armour, white lilies & SE Crypt Stair framing!
    for bx in (6, 15, 24):
        m.on('mn_bench', bx, 11)
    for cx in (4, 13, 22, 31):
        m.on('mn_candelabra', cx, 10)
    m.on('mn_armour', 37, 6)
    m.on('mn_armour', 37, 10)
    m.on('nt_lily', 4, 6)
    m.on('nt_lily', 33, 10)
    m.on('pf_signpost', 34, 10)    # Crypt Stair Brass Plaque solid base (34, 11)!

    # FOUR 100% Intact Overhead Chandeliers centered along the crimson runner!
    chandeliers_288 = [(6, 8), (15, 8), (24, 8), (33, 8)]
    for chx, chy in chandeliers_288:
        m.stamps.append(('mn_chandelier', chx, chy))

    # ---- 4. Full-Width West Exit -> 286, SE Ornate Crypt Stair -> 289, Solid Portrait Plaques & NPCs ----
    tap3_text = (
        "TAPESTRY III — THE EIGHTEEN CROWNS OF VELMORA: Eighteen sovereign houses woven round an ivory lamp. "
        "One narrow panel beside the centre has been stitched shut with plain gold thread, leaving nineteen seams and eighteen names."
    )
    m.events = [
        # Full-width West Exit Portal (2, 8..9 — 100% of vestibule floor!) -> 286 Briar Hall - Great Hall (26, 13) left!
        {'type': 'warp', 'name': 'West to Great Hall 8', 'at': [2, 8], 'to': {'map': 286, 'x': 26, 'y': 13, 'dir': 'left'}, 'se': 'Door exit'},
        {'type': 'warp', 'name': 'West to Great Hall 9', 'at': [2, 9], 'to': {'map': 286, 'x': 26, 'y': 13, 'dir': 'left'}, 'se': 'Door exit'},
        # Ornate SE Descending Crypt Stair (35..36, 11) -> 289 Briar Hall - Thorn Crypts (17, 5) down!
        {'type': 'warp', 'name': 'Down to Thorn Crypts 35', 'at': [35, 11], 'to': {'map': 289, 'x': 17, 'y': 5, 'dir': 'down'}, 'se': 'Door enter'},
        {'type': 'warp', 'name': 'Down to Thorn Crypts 36', 'at': [36, 11], 'to': {'map': 289, 'x': 17, 'y': 5, 'dir': 'down'}, 'se': 'Door enter'},
        # 4 Solid Portrait Plaques (full-width coverage including BOTH tiles of Tapestry III (24..25, 4) -> 0 over_trigger?!)
        _sign('Portrait I — King Aldric Thorne', (7, 4),
              "PORTRAIT I — KING ALDRIC THORNE (THE BRIAR-PLANTER): A golden fairy-tale tapestry showing him hedging the Briarway 'to keep the winter wolves at bay.' An archivist's pencil note on the bottom brass rim reads: 'Check AF 14 ledger — the hedges faced inward.'"),
        _sign('Portrait II — Queen Isolde & The Loyal Three', (16, 4),
              "PORTRAIT II — QUEEN ISOLDE & THE LOYAL THREE: Three garlanded beasts — hound, ape, and pheasant — kneeling beneath a peach bough while an ogre flees in shadow. Up close, fresh rose pigment covers a paler paint around all three collars."),
        _sign('Tapestry III — The Eighteen Crowns L', (24, 4), tap3_text),
        _sign('Tapestry III — The Eighteen Crowns', (25, 4), tap3_text),
        _sign('Portrait IV — Queen Maelis Thorne', (34, 4),
              "PORTRAIT IV — QUEEN MAELIS THORNE, SIXTY-FIRST YEAR: Painted leaning on her silver-rose cane beneath an unbroken rose window. Scratched lightly into the gilding: 'Four Sovereigns buried. Every one of them died tired.'"),
        _sign('Thorn Crypts Plaque', (34, 11),
              "THORN CRYPTS — ROYAL UNDERCROFT\nStep down the carved stone stair to the right. Mind the roots — nothing rots below Briar Hall."),
        _make_npc('Royal Archivist', (17, 7), 'NPC 22', 'up', [
            "Royal Archivist: Every portrait in this gallery was woven twice — once when it happened, and once after the Court decided how it ought to be remembered.",
            "Royal Archivist: If you want the unvarnished Thorne lineage, take the south-east stair down into the Thorn Crypts. Epitaphs in grey stone don't flatter nearly so well as silk.",
        ]),
        # Relocated onto open marble tile (33, 7) — cleanly clear of nr_col base (31, 7) and framing the crypt stair!
        _make_npc('Gallery Thornguard', (33, 7), 'trainer_THORNGUARD', 'down', [
            "Thornguard: No touching the tapestries, traveller. And if you go down into the crypts, keep a lantern lit — a Channeler named Griselda's been holding vigils down there all week.",
        ]),
    ]

    m.paint()
    # Stamp crisp carved descending stone stair tiles on (35..36, 11); crimson velvet runner already terminates cleanly at West Portal (2, 8..9)!
    m.L[1, 11, 35] = P1('st_stair_l')
    m.L[1, 11, 36] = P1('st_stair_r')
    m.L[0, 8, 2] = P1('lm_inlay_v')
    m.L[0, 9, 2] = P1('lm_inlay_v')

    Lr = RC.resolve(m.L, TID_MANOR).astype(np.int32)
    # Safe L[2]==0 warm glows strictly inside the gallery nave (ZERO south-wall bleed at (35,11)!) — ALL 4 chandeliers 24/24 intact!
    _add_safe_overlay(Lr, TID_MANOR, 'pf_glow', [(mx, 5) for mx in alcove_xs] + [(4, 10), (13, 10), (22, 10), (31, 10)])

    ch_ref = RC.resolve(np.array(STAMPS['mn_chandelier']['layers'], dtype=np.int32), TID_MANOR)
    for cx, cy in chandeliers_288:
        for dy in range(2):
            for dx in range(3):
                assert int(Lr[2, cy + dy, cx + dx]) == int(ch_ref[2, dy, dx]), f'Map 288 chandelier ({cx},{cy}) damaged!'

    ev_pts = [tuple(e['at']) for e in m.events]
    PG.guard(Lr, TID_MANOR, ev_pts, 'Map 288')
    assert not PG.hits(Lr, R.tilesets()[TID_MANOR], ev_pts), 'Map 288 passguard hits!'
    _verify_map(Lr, TID_MANOR, m.events, (3, 8), 'Map 288 Briar Hall Royal Gallery', outdoor=False)

    np.save(os.path.join(HERE, 'data', 'raw', '288.npy'), Lr.astype(np.int16))
    spec = {
        'id': 288,
        'name': 'Briar Hall - Royal Gallery',
        'parent': 286,
        'bgm': 'Natural Park',
        'map_audio': {'bgm': 'Theme - Accord', 'bgs': ''},
        'tone': [10, 4, -8, 2],
        'metadata': {'Name': 'Briar Hall', 'Outdoor': False, 'MapPosition': VERD_POS},
        'biome': 'interior',
        'tileset': TID_MANOR,
        'raw': 'data/raw/288.npy',
        'events': m.events,
    }
    with open(os.path.join(HERE, 'specs', '288_briar_hall_royal_gallery.yaml'), 'w', encoding='utf-8') as f:
        f.write('# GENERATED by mapgen/layouts/verdance_wards.py (Batch 3E): Briar Hall - Royal Gallery.\n')
        f.write(yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))
    print('Wrote specs/288_briar_hall_royal_gallery.yaml and data/raw/288.npy')


# =================================================================================================
# 4. MAP 289 — BRIAR HALL - THORN CRYPTS (35x31, Gothic Stone Undercroft, TS 59 qy2, :CAVE)
# =================================================================================================
def build_289():
    W, H = 35, 31
    # Moody weathered mossy gothic stone ashlar crypt walls (`qy2`) + dark subterranean rock void (`T`) — ZERO glacial ice!
    K.KITS['qy2'] = dict(K.KITS['qy'], rows=[K.KITS['qy']['rows'][0], K.KITS['qy']['rows'][2]])
    m = Cave(W, H, 'T', seed=289, pool='Cave Pool', tid=TID_MANOR)
    m.STAIRS = tuple(P1('st_stair_' + k) for k in 'lmr')
    m.kit = {MASS: 'qy2', TER: 'qy2', FLOOR: 'qy2', 'default': 'qy2'}

    # ---- 1. Sculpt Multi-Chamber Gothic Root-Entangled Royal Crypts with Recessed Stair Alcove & Tomb Niches ----
    # Exact 3-wide recessed North Ascending Stair Alcove (x=16..18, y=2..5 -> walls y=2..3, stair fills 100% of (16..18, 4)!)
    m.box(16, 2, 18, 5, TER, '.')
    # Elevated North Entry Landing (x=13..21, y=4..8 -> solid wall piers at (13..15, 4..5) & (19..21, 4..5), floor y=6..8!)
    m.box(13, 4, 21, 8, TER, '.')
    # Central Nave of the Unrotting Kings (FLOOR): x=12..22, y=9..23
    m.box(12, 9, 22, 23, FLOOR, '.')
    # West Crypt Cloister (FLOOR): x=3..12, y=10..22 (Canonical PBS Trainer [CHANNELER, Griselda]!)
    m.box(3, 10, 12, 22, FLOOR, '.')
    # East Root-Strangled Reliquary Vault (FLOOR): x=22..31, y=10..22 (Treasure Alcove!)
    m.box(22, 10, 31, 22, FLOOR, '.')
    # South Grey-Soil Undercroft Vault (FLOOR): x=11..23, y=23..28
    m.box(11, 23, 23, 28, FLOOR, '.')
    # Symmetrical gothic tomb-alcove buttresses & chamfered catacomb shoulders (breaks up boxy cloisters cleanly!)
    m.mass_at([
        (3, 15), (3, 16), (3, 17), (31, 15), (31, 16), (31, 17),
        (3, 22), (31, 22),
        (11, 28), (23, 28), (11, 27), (23, 27),
    ])
    # Sunken subterranean spring pool at the heart of the Nave (x=16..18, y=15..17)
    m.box(16, 15, 18, 17, FLOOR, 'w')

    # Grand 3-wide Carved Stone Staircase descending from North Entry Landing (x=16..18, y=8..9)
    m.stairs(16, 8, w=3, n=2, c='.')
    m.tidy()
    m.plan_cliffs(rows=2)

    # ---- 2. Events: North Return Stair -> 288, [CHANNELER, Griselda], Epitaph Plaques, Sexton & Treasure ----
    E = m.events
    # Full-width North Ascending Return Stair (16..18, 4) -> 288 Royal Gallery (35, 10) up (0 open flanks!)
    for rx in (16, 17, 18):
        E.append({
            'type': 'warp',
            'name': f'Up to Royal Gallery {rx}',
            'at': [rx, 4],
            'to': {'map': 288, 'x': 35, 'y': 10, 'dir': 'up'},
            'se': 'Door exit',
        })

    # Canonical PBS Trainer: [CHANNELER, Griselda] (pbs/trainers.txt:19048 — 4-tile left LoS (9..6, 16) 100% OPEN!)
    E.append({
        'type': 'trainer',
        'name': 'Trainer(4)',
        'at': [10, 16],
        'sight': 4,
        'dir': 'left',
        'sprite': 'trainer_CHANNELER',
        'trainer': ['CHANNELER', 'Griselda'],
        'intro': "Channeler Griselda: Three hundred years of Thorne kings lie under grey earth that refuses to let them go — let's hear whether the roots answer you!",
        'after': "Channeler Griselda: Nothing rots down here. Not even a grudge. Walk lightly by the southern soil vault.",
        'rules': ['setBattleRule("field", :CAVE)'],
    })

    # Crypt Sexton & Full-Width Carved Stone Royal Sarcophagus Epitaphs (pas=0xf -> 0 over_trigger?!)
    E.append(_make_npc('Crypt Sexton', (15, 25), 'NPC 21', 'right', [
        "Crypt Sexton: Feel the soil in that southern vault. Grey as cold fireplace ash, and dry as chalk.",
        "Crypt Sexton: Every rose blooming on the Market Terraces pulls its colour straight up through these roots — and leaves the dead below unable to rest.",
    ]))
    aldric_txt = "SARCOPHAGUS OF KING ALDRIC I — 'First of the Briar.' A garland laid on the carved stone lid in AF 14 still holds green thorns, brittle as glass."
    isolde_txt = "SARCOPHAGUS OF QUEEN ISOLDE — 'Keeper of the Meadow.' Carved below the name in a finer hand: 'The roots remember what the tapestries paint over.'"
    for sx in (13, 14):
        E.append(_sign('Sarcophagus of King Aldric' if sx == 14 else 'Sarcophagus of King Aldric L', (sx, 13), aldric_txt))
    for sx in (20, 21):
        E.append(_sign('Sarcophagus of Queen Isolde' if sx == 20 else 'Sarcophagus of Queen Isolde R', (sx, 13), isolde_txt))
    E.append(_sign('Unrotted Bouquet Epitaph', (17, 27),
                   "SOUTHERN SOIL VAULT — A bundle of white Bride Tree blossoms rests on the bare grey earth, dated AF 288. Not a single petal has browned."))

    # Verified Reliquary Vault Pickups (East Alcove + West Cloister!)
    E.append({'type': 'item', 'name': 'Item (Cleanse Tag)', 'at': [29, 13], 'item': 'CLEANSETAG'})
    E.append({'type': 'item', 'name': 'Item (Dusk Ball)', 'at': [29, 20], 'item': 'DUSKBALL'})
    E.append({'type': 'item', 'name': 'Item (Revive)', 'at': [4, 20], 'item': 'REVIVE'})
    E.append({'type': 'item', 'name': 'HiddenItem (Rare Bone)', 'at': [25, 16], 'item': 'RAREBONE', 'hidden': True})

    # Keep central runway, Griselda's sightline (9..6, 16), stairs & items clear
    for x in (16, 17, 18):
        for y in range(4, 15):
            m.keep_clear.add((x, y))
    for x in range(5, 11):
        m.keep_clear.add((x, 16))
    for e in E:
        m.keep_clear.add(tuple(e['at']))

    # ---- 3. Stately Carved Stone Royal Sarcophagi, Gothic Monoliths, Colonnades & 100% Intact Burning Braziers ----
    braziers_289 = [
        (14, 7), (20, 7),
        (14, 15), (20, 15), (14, 18), (20, 18),
        (4, 13), (4, 18), (29, 14), (29, 18),
        (13, 25), (21, 25),
    ]
    def put_over(nm, x, y, top_rows=0, solid=True):
        L = STAMPS[nm]['layers']
        h, w = len(L[0]), len(L[0][0])
        for dy in range(h):
            for dx in range(w):
                if not m.inb(x + dx, y + dy):
                    continue
                for sz in (0, 1, 2):
                    t = int(L[sz][dy][dx])
                    if t:
                        tz = 2 if (dy < top_rows or sz == 2) else 1
                        m.over.append((tz, x + dx, y + dy, t))
                if solid:
                    m.taken[y + dy, x + dx] = True

    # Monumental 2x1 Carved Marble/Stone Royal Sarcophagi (ZERO tiny dirt planter boxes!)
    # Hero Sovereign Tombs in Nave: King Aldric (13..14, 13) & Queen Isolde (20..21, 13) backed by gothic busts!
    put_over('mn_sheet_sofa', 13, 13, top_rows=0, solid=True)
    put_over('mn_sheet_sofa', 20, 13, top_rows=0, solid=True)
    put_over('mn_bust', 14, 11, top_rows=1, solid=True)
    put_over('mn_bust', 20, 11, top_rows=1, solid=True)
    # South Nave & Symmetrical West/East Cloister Carved Stone Sarcophagi + Headstone Monoliths!
    for sx, sy in ((13, 20), (20, 20), (6, 13), (6, 20), (26, 13), (26, 20)):
        put_over('pf_stonebench' if sy == 20 else 'mn_sheet_sofa', sx, sy, top_rows=0, solid=True)
    for rx, ry in ((12, 19), (22, 19), (5, 11), (28, 11)):
        put_over('pf_roadstone', rx, ry, top_rows=1, solid=True)

    # Southern Soil Vault Memorial Plinth (base (17, 27) pas=0xf!) + withered flowers on starving earth
    put_over('mn_plinth', 17, 27, top_rows=0, solid=True)
    put_over('mn_deadplant', 16, 27, top_rows=0, solid=True)
    put_over('mn_deadplant', 18, 27, top_rows=0, solid=True)

    # Symmetrical Gothic Crypt Columns & Sovereign Effigies (cleanly aligned — ZERO floating nr_ruin!)
    for cx, cy in ((12, 10), (22, 10), (13, 22), (21, 22), (10, 12), (10, 19), (24, 12), (24, 19)):
        put_over('nr_col', cx, cy, top_rows=1, solid=True)
    put_over('mn_statue', 13, 6, top_rows=1, solid=True)
    put_over('mn_statue', 21, 6, top_rows=1, solid=True)
    for ix, iy in ((16, 3), (18, 3), (5, 11), (9, 11), (25, 11), (29, 11)):
        if not m.taken[iy, ix]:
            put_over('mn_ivy0' if ix % 2 == 0 else 'mn_ivy1', ix, iy, top_rows=0, solid=True)
    for bx, by in braziers_289:
        put_over('fw_brazier', bx, by, top_rows=1, solid=True)

    m.paint()

    # Cohesive Crypt Floor Zones: weathered slate flagstones (L_f/T_f) + starving grey soil (cv_mud0..3) strictly in South Vault!
    slate = [P1('L_f%d' % i) for i in range(4)]
    ashlar = [P1('T_f%d' % i) for i in range(4)]
    mud = [P1('cv_mud%d' % i) for i in range(4)]
    floorpatch_ids = {P1(k) for k in STAMPS if k.startswith(('L_floorpatch_', 'L_fd', 'T_floorpatch_', 'T_fd'))}
    for y in range(H):
        for x in range(W):
            if m.cls[y, x] != '.' or m.cliff[y, x]:
                continue
            if int(m.L[1, y, x]) in floorpatch_ids:
                m.L[1, y, x] = 0
            if y >= 23 and 12 <= x <= 22:
                m.L[0, y, x] = mud[(x * 5 + y * 3) % 4]
            elif 14 <= x <= 20 and 4 <= y <= 22:
                m.L[0, y, x] = ashlar[(x * 3 + y * 5) % 4]
            else:
                m.L[0, y, x] = slate[(x * 7 + y * 11) % 4]
    # Crisp ascending stone steps filling 100% of recessed North Exit alcove (16..18, 4)
    m.L[1, 4, 16] = P1('st_stair_l')
    m.L[1, 4, 17] = P1('st_stair_m')
    m.L[1, 4, 18] = P1('st_stair_r')
    # Glowing pale cyan root-fungi lanterns tucked along the crypt floor margins (cv_fung0, pas=0x0 -> walkable moss!)
    for fx, fy in ((15, 14), (19, 14), (15, 18), (19, 18), (8, 14), (26, 14), (14, 26), (20, 26)):
        if m.cls[fy, fx] == '.' and m.L[1, fy, fx] == 0:
            m.L[1, fy, fx] = P1('cv_fung0')

    Lr = RC.resolve(m.L, TID_MANOR).astype(np.int32)
    # ZERO detached pf_glow orbs (0 brazier offset orbs, 0 floating water-pool orb!) — crisp burning flames speak for themselves!
    br_ref = RC.resolve(np.array(STAMPS['fw_brazier']['layers'], dtype=np.int32), TID_MANOR)
    flame_tid = int(br_ref[2, 0, 0])
    for bx, by in braziers_289:
        assert int(Lr[2, by, bx]) == flame_tid, f'Map 289 brazier flame damaged at ({bx},{by})!'

    ev_pts = [tuple(e['at']) for e in E]
    PG.guard(Lr, TID_MANOR, ev_pts, 'Map 289')
    assert not PG.hits(Lr, R.tilesets()[TID_MANOR], ev_pts), 'Map 289 passguard hits!'
    _verify_map(Lr, TID_MANOR, E, (17, 5), 'Map 289 Briar Hall Thorn Crypts', outdoor=False)

    np.save(os.path.join(HERE, 'data', 'raw', '289.npy'), Lr.astype(np.int16))
    spec = {
        'id': 289,
        'name': 'Briar Hall - Thorn Crypts',
        'parent': 288,
        'bgm': 'Cave',
        'field': 'CAVE',
        'map_audio': {'bgm': 'Dungeon - Cave', 'bgs': 'Drip - Nadir', 'bgs_volume': 45, 'rain': False},
        'tone': [-18, -14, -18, 18],
        'fog': {'name': 'prismfall_cave', 'opacity': 24, 'blend': 1, 'zoom': 100, 'sx': 1, 'sy': 0},
        'metadata': {'Name': 'Briar Hall - Thorn Crypts', 'Outdoor': False, 'ShowArea': True,
                     'BattleBack': 'cave1', 'MapPosition': VERD_POS},
        'biome': 'interior',
        'tileset': TID_MANOR,
        'raw': 'data/raw/289.npy',
        'events': E,
    }
    with open(os.path.join(HERE, 'specs', '289_briar_hall_thorn_crypts.yaml'), 'w', encoding='utf-8') as f:
        f.write('# GENERATED by mapgen/layouts/verdance_wards.py (Batch 3E): Briar Hall - Thorn Crypts.\n')
        f.write(yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))
    print('Wrote specs/289_briar_hall_thorn_crypts.yaml and data/raw/289.npy')


# =================================================================================================
# 5. MAP 294 — THE HEARTGARDEN (40x40, Outdoor, TS 55, :FLOWER_GARDEN, rubric: true)
# =================================================================================================
def build_294():
    W, H = 40, 40
    m = K.RMap(W, H, TID_CITY, 294, water='Ocean', kit={1: 'rw', 'default': 'qy'})
    m.keep_under = 'cfdg'
    m.gv_dark = 0.45

    # ---- 1. Sacred Sunken Sanctuary Ringed by Four Elevated Floral Terraces & Reflecting Moat ----
    # Elevated North Terrace (ht=1, y=0..9): Rowan's Potting Shed (NW) & Heartgarden Chapel Steps (NE)!
    for y in range(0, 10):
        for x in range(0, W):
            m.ht[y, x] = 1
    # Clean central stone stair descent from North Chapel Terrace (x=18..21, lip y=9, stairs y=9..11)
    for y in range(7, 10):
        for x in range(16, 24):
            m.ht[y, x] = 1
    for y in range(10, 14):
        for x in range(16, 24):
            m.ht[y, x] = 0

    # Shimmering Stone-Coped Reflecting Moat encircling THE BRIDE TREE Sanctuary Island (center (19.5, 20.5))!
    # Outer ring radius ~ 7.5..8.5, Inner Bride Tree Island radius ~ 4.3 (x=16..23, y=17..24)
    for y in range(12, 29):
        for x in range(11, 29):
            dist = math.hypot((x - 19.5) / 8.2, (y - 20.5) / 7.2)
            inner = math.hypot((x - 19.5) / 4.6, (y - 20.5) / 4.2)
            if dist <= 1.0 and inner >= 1.0:
                m.ht[y, x] = 0
                m.cls[y, x] = 'w'
            if dist <= 0.88 and inner >= 1.15:
                m.cls[y, x] = 'W'

    # Seal outer oldwood sanctuary forest borders (leaving clean West gate x=1..3, y=19..21!)
    for y in range(H):
        for x in range(W):
            if m.cls[y, x] != '.':
                continue
            outer = (x < 3 or x > W - 4 or y < 2 or y > H - 3)
            if x <= 3 and 19 <= y <= 21:
                outer = False
            if outer:
                m.cls[y, x] = 'T'

    m.stairs(18, 9, w=4, kit_rows=3, kind='stone', c='f')
    m.plan_cliffs(rows=3)

    # ---- 2. Symmetrical Cardinal Garden Walks, Bride Tree Sanctuary Plaza & South Veil Stair ----
    # Central Bride Tree Sanctuary Plaza (x=16..23, y=17..24)
    m.rect(16, 17, 8, 8, 'f', only='.tTc')
    # Cardinal Promenades: West Gate -> Island, Island -> East Terrace, North Chapel -> Island, Island -> South Veil!
    m.lane([(1, 20), (12, 20)], c='f', w=3.0, seed=1, only='.tT', wobble=0.06)
    m.lane([(28, 20), (34, 20)], c='f', w=3.0, seed=2, only='.tT', wobble=0.06)
    m.lane([(19.5, 12), (19.5, 14)], c='f', w=3.0, seed=3, only='.tT', wobble=0.04)
    m.lane([(19.5, 28), (19.5, 36)], c='f', w=3.2, seed=4, only='.tT', wobble=0.04)
    # Outer Quadrant Rose-Garden Walk Loop (connecting NW, NE, SW, SE terraces around the moat!)
    m.lane([(6, 13), (12, 13), (28, 13), (34, 13)], c='c', w=2.4, seed=5, only='.tT', wobble=0.08)
    m.lane([(6, 29), (14, 29), (26, 29), (34, 29)], c='c', w=2.4, seed=6, only='.tT', wobble=0.08)
    m.lane([(7, 13), (7, 29)], c='c', w=2.4, seed=7, only='.tT', wobble=0.08)
    m.lane([(33, 13), (33, 29)], c='c', w=2.4, seed=8, only='.tT', wobble=0.08)
    # Upper North Chapel & Potting Shed Terrace Walk (y=6..8)
    m.lane([(7, 8), (20, 8), (32, 8)], c='f', w=2.6, seed=9, only='.tT', wobble=0.05)
    for c in 'cf':
        m.smooth(c, into='.', passes=1, only='.tT')

    # Re-assert Reflecting Moat cleanly (only the 4 cardinal bridges cross it!)
    for y in range(12, 29):
        for x in range(11, 29):
            dist = math.hypot((x - 19.5) / 8.2, (y - 20.5) / 7.2)
            inner = math.hypot((x - 19.5) / 4.6, (y - 20.5) / 4.2)
            if dist <= 1.0 and inner >= 1.0:
                m.cls[y, x] = 'W' if (dist <= 0.88 and inner >= 1.15) else 'w'

    # ---- 3. THE BRIDE TREE Centerpiece, Rowan's Potting Shed, Chapel Steps & Floral Archway ----
    # THE BRIDE TREE (Aunt Elin, Fixed AF 288): luminous white-blossomed hero tree standing alone & un-dwarfed at (18..20, 17..20)!
    # (Oversized flanking nt_tree_pink removed so the sacred white Bride Tree dominates the entire island silhouette!)
    m.stamp('nt_blossom', 18, 17)
    # Rowan's Potting Shed on the NW Upper Terrace (`gl_shed` 4x6 at (7, 2) -> solid facade door at (8, 6)!)
    m.stamp('gl_shed', 7, 2)
    # Heartgarden Chapel Facade on the NE Upper Terrace (`cv_little` 6x7 at (27, 1) -> solid facade door at (30, 6)!)
    m.stamp('cv_little', 27, 1)
    # Blossoming Ceremonial Archway (`wb_gate` 5x5) framing the South Bride Grove Veil Approach at (17, 30)!
    m.stamp('wb_gate', 17, 30)

    # ---- 4. Events: Live Juno Hale Hooks (:JUNO_BRIDE_TREE / :PG_JUNO_BRIDE_TREE / EL_EVER_BLOOM), Ogerpon, Thornguard ----
    E = []
    # West Gate (1, 19..21) -> 283 Verdance - Glasshouse Ward (44, 12) left!
    for wy in (19, 20, 21):
        E.append({
            'type': 'warp',
            'name': f'West to Glasshouse Ward {wy}',
            'at': [1, wy],
            'to': {'map': 283, 'x': 44, 'y': 12, 'dir': 'left'},
            'se': 'Door exit',
        })

    # South Sunken Veil Stair (19..20, 35) -> PBMoveRoute::BACKWARD-guarded exit to unbuilt 708 The Bride Grove!
    grove_msg = (
        "A pale heat-shimmer hangs across the stone steps descending beneath the Bride Tree's roots — the Veil of the Bride Grove. "
        "Warm petals stir along the stairhead, waiting for the Meadow Plate's trial to open."
    )
    for gx in (19, 20):
        E.append({
            'type': 'event',
            'name': f'South to Bride Grove {gx}',
            'at': [gx, 35],
            'pages': [{
                'trigger': 'touch',
                'through': True,
                'commands': _guarded_unbuilt_transfer(708, 14, 3, 'down', grove_msg),
            }],
        })

    # JUNO HALE UNDER THE BRIDE TREE (JUNO sprite — DO NOT EDIT ANY JUNO ART!)
    juno_tree_ruby = '''if (pf_trial_ready?(:JUNO_BRIDE_TREE) rescue false)
  pf_trial_talk(:JUNO_BRIDE_TREE)
elsif (pf_trial_ready?(:PG_JUNO_BRIDE_TREE) rescue false)
  pf_trial_talk(:PG_JUNO_BRIDE_TREE)
elsif $game_switches[125]
  pbMessage(_INTL("Juno: Look at the blossoms now, \\PN — they're finally resting instead of bursting."))
  if $game_switches[182]
    pbMessage(_INTL("Juno: Ever since you played Venam's recording for me, I sit here every dawn and tell Aunt Elin what happened in the city. The petals fall when I finish."))
  else
    pbMessage(_INTL("Juno: The Quiet Way says the roots carry voices all the way down to the Listening Root. Sometimes I leave a bouquet against the bark just to see if she hums back."))
  end
  pbMessage(_INTL("Juno: Uncle Rowan's postscript said: 'Water Elin at dawn. She likes it before the bees are up.' I haven't missed a morning yet."))
else
  pbMessage(_INTL("Juno: You've heard about her. Everyone has. This is Aunt Elin — AF 288."))
  pbMessage(_INTL("Juno: Uncle Rowan walked me up here every dawn for twelve years and watered her roots. Sometimes I think she's listening. Isn't that stupid?"))
  if $game_switches[182]
    pbMessage(_INTL("Juno: ...Wait — that recording from Mirefen? She could hear everything while she was stone? ...Oh. Oh, Aunt Elin."))
  end
end'''
    E.append({
        'type': 'event',
        'name': 'Juno Hale',
        'at': [19, 22],
        'pages': [{
            'graphic': {'sprite': 'JUNO', 'dir': 'up'},
            'trigger': 'action',
            'move': 'fixed',
            'commands': [{'script': juno_tree_ruby}],
        }],
    })

    # OGERPON KEEPING QUIET WATCH BESIDE THE BRIDE TREE (conditional on S223 OGERPON_TRUSTED + :PG_BRIDE_TREE_OGRE!)
    ogre_ruby = '''if (pf_trial_ready?(:PG_BRIDE_TREE_OGRE) rescue false)
  pf_trial_talk(:PG_BRIDE_TREE_OGRE)
else
  pbMessage(_INTL("The masked Ogre sits quietly among the white fallen petals beside the Bride Tree's roots."))
  pbMessage(_INTL("It glances up at you through its carved wooden mask, taps its leafy club softly against the earth, and turns back to watch over Aunt Elin."))
end'''
    E.append({
        'type': 'event',
        'name': 'Bride Tree Ogre',
        'at': [21, 21],
        'pages': [
            {'trigger': 'action', 'through': True, 'commands': []},
            {
                'cond': {'switch': 223},
                'graphic': {'sprite': 'trainer_PARTNER_OGRE', 'dir': 'down'},
                'trigger': 'action',
                'move': 'fixed',
                'commands': [{'script': ogre_ruby}],
            },
        ],
    })

    # REACTIVE THORNGUARD SENTINEL (S165 THORNGUARD_HEARTGARDEN vs S125 CH10_JUNO_WARDEN!)
    tg_ruby = '''if $game_switches[165]
  pbMessage(_INTL("Thornguard Sentinel: By order of Her Majesty Queen Maelis Thorne, the Heartgarden is under royal cordon pending the Meadow Plate succession."))
  pbMessage(_INTL("Thornguard Sentinel: ...You're the one from Ironreach, aren't you? The Sovereign left instructions to let you pass. Mind the tulips."))
elsif $game_switches[125]
  pbMessage(_INTL("Thornguard Sentinel: Warden Hale told Her Majesty to get our boots off her tulips — and we've been posted politely outside the rose beds ever since."))
else
  pbMessage(_INTL("Thornguard Sentinel: The Heartgarden sits on Crown soil, though even the Queen lowers her voice under the Bride Tree."))
end'''
    E.append({
        'type': 'event',
        'name': 'Thornguard Sentinel',
        'at': [6, 19],
        'pages': [{
            'graphic': {'sprite': 'trainer_THORNGUARD', 'dir': 'down'},
            'trigger': 'action',
            'move': 'fixed',
            'commands': [{'script': tg_ruby}],
        }],
    })

    # Heartgarden Gardener & Quiet Way Scribe + Full-Width Quiet Way Board (live pf_trial_board(:ELOWEN) on (32..33, 14)!)
    E.append(_make_npc('Heartgarden Gardener', (11, 28), 'NPC 05', 'up', [
        "Heartgarden Gardener: Twelve years I've swept these terraces. Elin's tree never dropped a single petal — until Juno sat down on the roots and talked to her.",
    ], move='random'))
    E.append(_make_npc('Quiet Way Scribe', (30, 14), 'NPC 22', 'right', [
        "Quiet Way Scribe: We tie paper prayers to the Heartgarden shrine rope for those the Bleed Fixed. The roots hear more than most councils.",
    ]))

    board_294_ruby = '''if defined?(pf_trial_board)
  pf_trial_board(:ELOWEN)
else
  pbMessage(_INTL("A Quiet Way prayer rope tied with green linen ribbons."))
end'''
    for bx in (32, 33):
        E.append({
            'type': 'event',
            'name': 'Heartgarden Quiet Way Board' if bx == 33 else 'Heartgarden Quiet Way Board L',
            'at': [bx, 14],
            'pages': [{'trigger': 'action', 'commands': [{'script': board_294_ruby}]}],
        })

    # Solid Building Facade Doors & Memorial Plaques (0 over_trigger?! — strictly on REAL solid facade doors (8,6) & (30,6)!)
    E.append(_sign('Rowan Potting Shed Door', (8, 6),
                   "ROWAN'S POTTING SHED — A battered tin on the window-ledge is labelled 'NOT SEEDS' in neat green ink. Beside it sits a watering can still cool from dawn."))
    E.append(_sign('Heartgarden Chapel Door', (30, 6),
                   "HEARTGARDEN CHAPEL — The limestone steps where Verdance's Wardens take the Meadow Plate's oath."))
    E.append(_sign('Bride Tree Memorial Plaque', (17, 23),
                   "THE BRIDE TREE — ELIN HALE (AF 288)\n\"She stood up in the garden, raised her arms to the light, and stayed in blossom.\""))
    E.append(_sign('Bride Grove Stair Sign', (16, 34),
                   "THE BRIDE GROVE — Sunken Root Sanctuary below the Heartgarden.\nOnly one the Veil lets through may walk the stair."))

    # Verified PBS Items
    E.append({'type': 'item', 'name': 'Item (Miracle Seed)', 'at': [34, 27], 'item': 'MIRACLESEED'})
    E.append({'type': 'item', 'name': 'Item (Max Ether)', 'at': [6, 13], 'item': 'MAXETHER'})

    m.events += E
    key_pts = [tuple(e['at']) for e in E] + [
        (1, 19), (1, 20), (1, 21), (2, 19), (2, 20), (2, 21), (3, 19), (3, 20), (3, 21), (4, 20),
        (19, 10), (20, 10), (19, 11), (20, 11), (19, 12), (20, 12),
        (19, 13), (20, 13), (19, 14), (20, 14), (19, 15), (20, 15), (19, 16), (20, 16),
        (19, 25), (20, 25), (19, 26), (20, 26), (19, 27), (20, 27), (19, 28), (20, 28),
        (12, 20), (13, 20), (14, 20), (15, 20), (24, 20), (25, 20), (26, 20), (27, 20),
        (19, 21), (20, 21), (19, 23), (20, 23), (19, 34), (20, 34), (19, 33), (20, 33),
        (8, 7), (8, 8), (30, 7), (30, 8), (18, 22), (20, 22), (32, 14), (33, 15),
    ]
    prot = reserve_mask(m, key_pts, pad=1)
    for x, y in key_pts:
        if m.inb(x, y):
            m.taken[y, x] = True

    # ---- 5. Four Floral Terraces, Fountains, White Lilies, Lanterns & Blossom Canopy Groves ----
    m.stamp('pf_signpost', 17, 22)     # Bride Tree Memorial base (17, 23)
    m.stamp('pf_signpost', 16, 33)     # Bride Grove Stair Sign base (16, 34)
    m.stamp('pf_shrine', 32, 12)       # Quiet Way Board solid base (32..33, 13..14) -> BOTH (32,14) & (33,14) pas=0xf!

    lamp_pts = []
    for nm, x, y in (
        ('pf_fountain', 9, 14), ('pf_fountain', 26, 24),
        # Strictly mirror-symmetrical luminous white-lily accents framing THE BRIDE TREE (18..20, 17..20) cleanly!
        ('nt_lily', 17, 17), ('nt_lily', 21, 17),
        ('nt_azalea2', 11, 24), ('nt_azalea0', 27, 15), ('nt_azalea1', 9, 31), ('nt_azalea2', 28, 31),
        ('nt_azalea2', 12, 6), ('nt_azalea0', 24, 6),
        ('pf_planter0', 14, 7), ('pf_planter2', 23, 7),
        ('pf_stonebench', 10, 22), ('pf_stonebench', 29, 22), ('pf_stonebench', 14, 31), ('pf_stonebench', 24, 31),
        ('lm_topiary', 16, 12), ('lm_topiary', 23, 12), ('lm_topiary', 16, 28), ('lm_topiary', 23, 28),
    ):
        put_safe(m, nm, x, y, on='.fc', r=1, prot=prot)

    for lx, ly in ((16, 16), (23, 16), (16, 24), (23, 24), (10, 19), (29, 19),
                   (17, 11), (22, 11), (17, 29), (22, 29), (17, 35), (22, 35), (6, 22), (33, 22)):
        if can_put_clean(m, 'pf_lantern', lx, ly - 2, on='.fc', prot=prot):
            m.stamp('pf_lantern', lx, ly - 2)
            lamp_pts.append((lx, ly - 1))

    paint_rail_run(m, 5, 17, 9, kind='rw')
    paint_rail_run(m, 22, 34, 9, kind='rw')

    # Standalone whole pink cherry accents (ZERO overlap notches!) + lush evergreen royal canopy groves!
    for px, py in ((9, 32), (28, 32), (4, 24), (34, 24)):
        if can_put_clean(m, 'nt_tree_pink', px, py, on='.', prot=prot):
            m.stamp('nt_tree_pink', px, py)
    evergreen_canopy = [k for k in ROYAL_CANOPY if 'pink' not in k and 'blossom' not in k]
    for idx, (cx, cy) in enumerate(((5, 16), (5, 28), (34, 17), (34, 28), (10, 34), (29, 34), (5, 7), (34, 7))):
        place_canopy_grove(m, cx, cy, evergreen_canopy, count=3, radius=2.0, on='.', seed=idx + 60, prot=prot, undergrowth=True)

    # Reserve the exact 3x3 Sunken Veil Root Grotto footprint (18..20, 36..38) BEFORE greenfill so trees NEVER clip pf_minemouth!
    for gy in range(36, 39):
        for gx in range(18, 21):
            m.taken[gy, gx] = True
            m.cls[gy, gx] = '.'

    m.greenfill(4)
    m.paint()

    # Paint FOUR Symmetrical Cardinal Cedar Footbridges across the Reflecting Moat into the Bride Tree Island!
    # CRITICAL P0-1 FIX: North Bridge stops strictly at y=16 — NEVER touches y=17 (THE BRIDE TREE's blossom crown)!
    _paint_bridge_ns(m, 18, 21, 12, 16)                                    # North Bridge (Chapel -> Bride Tree)
    _paint_bridge_ns(m, 18, 21, 24, 29)                                    # South Bridge (Bride Tree -> Veil Stair)
    _paint_bridge_ew(m, 11, 16, 19, 20, rail_north=True, under_beam=True)  # West Framed Bridge (Glasshouse -> Island)
    _paint_bridge_ew(m, 23, 29, 19, 20, rail_north=True, under_beam=True)  # East Framed Bridge (Island -> East Terrace)

    # Symmetrical harbour bollards flanking all 4 E-W bridgeheads cleanly!
    for bx, by in ((11, 18), (11, 21), (29, 18), (29, 21)):
        if m.inb(bx, by) and m.L[1, by, bx] == 0:
            m.L[1, by, bx] = P1('hb_bollard0')

    # Carved descending stone steps (19..20, 35) leading into a 100% WHOLE unclipped Root Veil Grotto (pf_minemouth at (18, 36))!
    mm_L = STAMPS['pf_minemouth']['layers']
    for dy in range(3):
        for dx in range(3):
            xx, yy = 18 + dx, 36 + dy
            if m.inb(xx, yy):
                m.L[1, yy, xx] = 0
                m.L[2, yy, xx] = 0
                for sz in (1, 2):
                    t = int(mm_L[sz][dy][dx])
                    if t:
                        m.L[sz, yy, xx] = t
    # Seal all grotto bottom row & mouth tiles cleanly with transparent blocker 505 so zero south border leaks occur
    for gx in range(18, 21):
        for gy in (36, 37, 38):
            if m.L[2, gy, gx] == 0:
                m.L[2, gy, gx] = 505
    m.L[1, 35, 19] = P1('st_stair_l')
    m.L[1, 35, 20] = P1('st_stair_r')
    m.L[2, 35, 19] = 0
    m.L[2, 35, 20] = 0

    add_festoon_strings(m, [(18, 21, 14, 0), (18, 21, 26, 1)], kind='lstring')
    # Strictly lamp-centered warm glows ONLY (ZERO smudges under Bride Tree or sidewalk!)
    add_warm_glows(m, lamp_pts)
    add_water_glints(m, water_cls='wW', seed=294, density=0.06)
    m.scatter(12, seed=294, on='.T')

    # Keep ALL 4 bridge decks & West Warp (1, 19..21) 100% free of stray scatter flowers/bushes!
    for bx0, bx1, by0, by1 in ((18, 21, 12, 16), (18, 21, 24, 29), (11, 16, 19, 20), (23, 29, 19, 20)):
        for by in range(by0, by1 + 1):
            for bx in range(bx0, bx1 + 1):
                m.L[1, by, bx] = 0
    for wy in (19, 20, 21):
        for wx in (1, 2, 3):
            m.L[1, wy, wx] = 0
            m.L[2, wy, wx] = 0
    # Seal open West warp flanks (1, 18) & (1, 22) with solid hedges!
    for fy in (18, 22):
        if m.L[1, fy, 1] == 0:
            m.L[1, fy, 1] = P1('nt_bush0')

    # Scatter pale white Bride Tree petals across the Sanctuary Island & four bridges AFTER scatter cleanup!
    for px, py in ((18, 21), (20, 21), (19, 23), (21, 23), (17, 20), (22, 20), (19, 15), (20, 26), (19, 32)):
        if m.L[1, py, px] == 0:
            m.L[1, py, px] = T_PETALS

    # Seal gl_shed's real wooden arched door tile (8, 6) with invisible pas=0xf blocker 505 (0 over_trigger?, 0 floating door!)
    m.L[2, 6, 8] = 505

    seal_unconnected_edges(m, open_cells=())

    Lr = RC.resolve(m.L, TID_CITY).astype(np.int32)
    # P0-1 ASSERTION: Verify 100% of THE BRIDE TREE (`nt_blossom` at (18..20, 17..20)) survived UN-SHEARED!
    bt_ref = RC.resolve(np.array(STAMPS['nt_blossom']['layers'], dtype=np.int32), TID_CITY)
    for dy in range(bt_ref.shape[1]):
        for dx in range(bt_ref.shape[2]):
            for sz in (1, 2):
                t_exp = int(bt_ref[sz, dy, dx])
                if t_exp:
                    assert int(Lr[sz, 17 + dy, 18 + dx]) == t_exp, (
                        f'Map 294 BRIDE TREE DAMAGED at ({18+dx},{17+dy}) L{sz}: got {Lr[sz, 17+dy, 18+dx]} != {t_exp}!'
                    )

    ev_pts = [tuple(e['at']) for e in m.events]
    PG.guard(Lr, TID_CITY, ev_pts, 'Map 294')
    assert not PG.hits(Lr, R.tilesets()[TID_CITY], ev_pts), 'Map 294 passguard hits!'
    _verify_map(Lr, TID_CITY, m.events, (3, 20), 'Map 294 The Heartgarden', outdoor=True)

    np.save(os.path.join(HERE, 'data', 'raw', '294.npy'), Lr.astype(np.int16))
    spec = {
        'id': 294,
        'name': 'The Heartgarden',
        'parent': 283,
        'bgm': 'Natural Park',
        'field': 'FLOWER_GARDEN',
        'rubric': True,
        'yards_ok': True,
        'map_audio': {'bgm': 'Town - Elowen', 'bgs': 'Gossamer Deepwood', 'bgs_volume': 45},
        'tone': [4, 12, -6, 0],
        'fog': {'name': 'prismfall_spores', 'opacity': 20, 'blend': 1, 'zoom': 100, 'sx': 1, 'sy': 0},
        'metadata': {'Name': 'The Heartgarden', 'Outdoor': True, 'ShowArea': True, 'Bicycle': True,
                     'MapPosition': VERD_POS, 'BattleBack': 'field'},
        'biome': 'city',
        'tileset': TID_CITY,
        'raw': 'data/raw/294.npy',
        'events': m.events,
    }
    with open(os.path.join(HERE, 'specs', '294_the_heartgarden.yaml'), 'w', encoding='utf-8') as f:
        f.write('# GENERATED by mapgen/layouts/verdance_wards.py (Batch 3E): The Heartgarden (Bride Tree Sanctuary).\n')
        f.write(yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))
    print('Wrote specs/294_the_heartgarden.yaml and data/raw/294.npy')


# =================================================================================================
# 6. MAP 296 — VERDANCE - ROOTWARD (44x32, Outdoor, TS 55, :FLOWER_GARDEN, rubric: true)
# =================================================================================================
def build_296():
    W, H = 44, 32
    m = K.RMap(W, H, TID_CITY, 296, water='Ocean', kit={1: 'rw', 'default': 'qy'})
    m.keep_under = 'cfdg'
    m.gv_dark = 0.62

    # ---- 1. Shaded Lower-Terrace Working Quarter Beneath Retaining Arches & Irrigation Runoff ----
    # High Northern Retaining Terrace Wall (ht=1, y=0..4) overlooking the sunken Rootward tenements!
    for y in range(0, 5):
        for x in range(0, W):
            m.ht[y, x] = 1
    # Clean central stone stair landing descending from 283 Glasshouse Ward (x=19..23, lip y=4, stairs y=4..6)
    for y in range(0, 5):
        for x in range(18, 25):
            m.ht[y, x] = 1
    for y in range(5, 9):
        for x in range(18, 25):
            m.ht[y, x] = 0

    # Narrow Root-Fed Irrigation Drainage Runnel cutting East-West along y=19..20 (spanned by 2 rustic bridges!)
    for x in range(0, W):
        ry = 19 + int(round(0.6 * math.sin(x / 7.5)))
        for y in (ry, ry + 1):
            if 0 <= y < H:
                m.ht[y, x] = 0
                m.cls[y, x] = 'w'

    # Seal outer steep earthen/root-wall woods (leaving exact 3-wide North Stair, West Alley, East Root-Road Arch!)
    for y in range(H):
        for x in range(W):
            if m.cls[y, x] != '.':
                continue
            outer = (x < 3 or x > W - 4 or y < 2 or y > H - 3)
            if 20 <= x <= 22 and y <= 4:
                outer = False
            if x <= 3 and 14 <= y <= 16:
                outer = False
            if x >= W - 4 and 22 <= y <= 24:
                outer = False
            if outer:
                m.cls[y, x] = 'T'

    m.stairs(19, 4, w=5, kit_rows=3, kind='stone', c='f')
    m.plan_cliffs(rows=3)

    # ---- 2. Grey Starving Earth Alleys, Damp Cobble Lanes & Washbasin Courtyard ----
    # Upper Retaining Terrace Walkway & North Stair Arrival (y=1..4)
    m.rect(19, 1, 5, 4, 'c', only='.tT')
    m.lane([(6, 2.5), (19, 2.5), (24, 2.5), (37, 2.5)], c='c', w=2.0, seed=10, only='.t', wobble=0.05)
    m.lane([(21, 7), (21, 15), (14, 15), (1, 15)], c='c', w=2.8, seed=1, only='.tT', wobble=0.1)
    m.lane([(21, 15), (34, 15), (34, 18)], c='c', w=2.6, seed=2, only='.tT', wobble=0.1)
    # Communal Laundress Washbasin & Dead Well Yard (grey dirt 'd' + damp cobble 'c', x=11..28, y=22..28!)
    m.blob(20, 25, 10.5, 3.6, 'd', seed=3, rough=0.35, only='.tTc')
    m.lane([(12, 22), (12, 26), (26, 26), (34, 23), (42, 23)], c='c', w=2.6, seed=4, only='.tTd', wobble=0.1)
    m.lane([(12, 16), (12, 18)], c='c', w=2.6, seed=5, only='.tT', wobble=0.05)
    m.lane([(33, 21), (33, 24)], c='c', w=2.6, seed=6, only='.tT', wobble=0.05)
    for c in 'cd':
        m.smooth(c, into='.', passes=1, only='.tT')

    # Re-assert Drainage Runnel so alleys cross strictly at the two rustic footbridges!
    for x in range(0, W):
        ry = 19 + int(round(0.6 * math.sin(x / 7.5)))
        for y in (ry, ry + 1):
            if 0 <= y < H:
                m.cls[y, x] = 'w'

    # ---- 3. Distinct Working-Class Tenement Cottages & Root-Cellars (ZERO copy-pasted adjacent shack roofs!) ----
    for nm, x, y in (
        ('gl_flat1', 5, 8), ('th_d', 12, 8), ('th_h', 16, 8),
        ('th_s', 25, 8), ('th_m', 29, 8), ('th_q', 35, 8),
        ('th_v', 4, 22), ('gl_shed', 27, 23), ('th_f', 35, 22),
    ):
        if can_put_clean(m, nm, x, y, on='.cdTf', check_level=True):
            m.stamp(nm, x, y)

    # ---- 4. Events: Warps, BACKWARD Exit -> 690, Rootward Laundress (EL_ROOTWARD_WAKE), NPCs & Items ----
    E = []
    # North Stairway (20..22, 1) -> 283 Verdance - Glasshouse Ward (15, 36) up!
    for nx in (20, 21, 22):
        E.append({
            'type': 'warp',
            'name': f'Up to Glasshouse Ward {nx}',
            'at': [nx, 1],
            'to': {'map': 283, 'x': 15, 'y': 36, 'dir': 'up'},
            'se': 'Door enter',
        })
    # West Upper Alley (1, 14..16) -> 280 Verdance - Market Terraces (9, 75) left!
    for wy in (14, 15, 16):
        E.append({
            'type': 'warp',
            'name': f'West to Market Terraces {wy}',
            'at': [1, wy],
            'to': {'map': 280, 'x': 9, 'y': 75, 'dir': 'left'},
            'se': 'Door exit',
        })
    # East Root-Road Arch (42, 22..24) -> PBMoveRoute::BACKWARD-guarded exit to unbuilt 690 Lanternroot!
    rootroad_msg = (
        "Rootward Freight-Hand: Careful by the eastern root-arch — the freight-lift down toward Lanternroot and the Rootdeep "
        "is hauled up for inspection after the last landslide. Stay on the Verdance terraces until the cables clear."
    )
    for ey in (22, 23, 24):
        E.append({
            'type': 'event',
            'name': f'East to Lanternroot {ey}',
            'at': [42, ey],
            'pages': [{
                'trigger': 'touch',
                'through': True,
                'commands': _guarded_unbuilt_transfer(690, 4, 18, 'right', rootroad_msg),
            }],
        })

    # ROOTWARD LAUNDRESS — Canonical EL_ROOTWARD_WAKE hook ("The Rootward Wake", design/TRIALS_QUESTS.md:49)
    # P0-1 FIX: Check Ch10 S125 (Juno confirmed Warden) BEFORE Ch9 S124 so Juno's Ch10 dialogue is 100% reachable!
    laundress_ruby = '''pbMessage(_INTL("Rootward Laundress: Scrub, wring, hang — and half an hour later the sheets are dusted yellow with upper-town pollen all over again."))
pbMessage(_INTL("Rootward Laundress: Folks up on the Market Terraces call it a blessing that nothing ever rots in Verdance. Try burying someone you loved in soil that won't take a leaf."))
pbMessage(_INTL("Rootward Laundress: We're planning one proper old-Elowen wake by the dead well — a candle allowed to burn out, a flower from beyond the walls that can actually wilt, and a song nobody's sung since the Bleed."))
if $game_switches[125]
  pbMessage(_INTL("Rootward Laundress: Young Juno came down yesterday with her gloves still muddy and asked if she could sit by the well with us. That girl's got her uncle's heart without his secrets."))
elsif $game_switches[124]
  pbMessage(_INTL("Rootward Laundress: ...After what came out at Ironreach, even the Hollow folk down here say old Rowan understood that much: everything that grows has to be allowed to die."))
end'''
    E.append({
        'type': 'event',
        'name': 'Rootward Laundress',
        'at': [19, 25],
        'pages': [{
            'graphic': {'sprite': 'NPC 11', 'dir': 'right'},
            'trigger': 'action',
            'move': 'fixed',
            'commands': [{'script': laundress_ruby}],
        }],
    })

    # Mourner / Rowan Sympathiser (reacts to S124 CH9_MOURNER_UNMASKED!)
    symp_ruby = '''if $game_switches[124]
  pbMessage(_INTL("Rootward Resident: Print whatever you like in the Gazette — Rowan Ashby watered the apple trees in this alley every autumn for twenty years without charging a copper."))
  pbMessage(_INTL("Rootward Resident: If that makes a man Hollow, half the Rootward's Hollow too."))
else
  pbMessage(_INTL("Rootward Resident: All the runoff from the Glasshouse Ward trickles right down into our channel. They get the roses up top; we get the grey dirt and the damp."))
end'''
    E.append({
        'type': 'event',
        'name': 'Rootward Resident',
        'at': [26, 15],
        'pages': [{
            'graphic': {'sprite': 'NPC 08', 'dir': 'down'},
            'trigger': 'action',
            'move': 'fixed',
            'commands': [{'script': symp_ruby}],
        }],
    })

    E.append(_make_npc('Washerwoman', (15, 25), 'NPC 05', 'up', [
        "Washerwoman: Best place to dry linen in Verdance is right under the retaining arch — the pollen doesn't drift quite so thick in the shade.",
    ], move='random'))
    E.append(_make_npc('Grey-Soil Digger', (31, 24), 'NPC 13', 'left', [
        "Grey-Soil Digger: Spade down two feet anywhere in Rootward and you hit roots thick as harbour pilings, dry as bone. Whatever's feeding the upper gardens is starving the floor.",
    ]))

    # Solid Plaques (0 over_trigger?!) — Sign shifted cleanly to roadside corner (23, 14), Dead Well covers ALL 4 solid coping tiles!
    E.append(_sign('Rootward Sign', (23, 14),
                   "VERDANCE — ROOTWARD\n↑ Glasshouse Ward Steps · ← Market Terraces · → Root-Road Arch (Lanternroot)"))
    well_txt = "THE ROOTWARD DEAD WELL — Dry since AF 288. Someone has tied three white linen ribbons and a burnt-down candle stub to the stone coping."
    for idx_w, (wx, wy) in enumerate(((21, 24), (22, 24), (21, 25), (22, 25))):
        E.append(_sign('Dead Well Plaque' if idx_w == 3 else f'Dead Well Plaque {idx_w}', (wx, wy), well_txt))

    # Verified PBS Items
    E.append({'type': 'item', 'name': 'Item (Cleanse Tag)', 'at': [9, 27], 'item': 'CLEANSETAG'})
    E.append({'type': 'item', 'name': 'Item (Full Heal)', 'at': [38, 15], 'item': 'FULLHEAL'})
    E.append({'type': 'item', 'name': 'HiddenItem (Big Root)', 'at': [24, 27], 'item': 'BIGROOT', 'hidden': True})

    m.events += E
    key_pts = [tuple(e['at']) for e in E] + [
        (21, 2), (21, 3), (21, 4), (21, 5), (21, 6), (21, 7),
        (2, 15), (3, 15), (40, 23), (41, 23),
        (11, 18), (12, 18), (13, 18), (11, 21), (12, 21), (13, 21),
        (32, 18), (33, 18), (34, 18), (32, 21), (33, 21), (34, 21),
        (19, 24), (20, 25), (21, 25), (22, 26), (23, 13), (17, 14),
    ]
    prot = reserve_mask(m, key_pts, pad=1)
    for x, y in key_pts:
        if m.inb(x, y):
            m.taken[y, x] = True

    # ---- 5. Upper Retaining Terrace Dressing, Laundry Lines, Washbasins, Dead Well, Crates & Lanterns ----
    m.stamp('pf_signpost', 23, 13)      # Rootward Sign cleanly at roadside corner (23, 14), clear of tenement door!
    m.stamp('pf_well', 21, 23)          # Rootward Dead Well solid base (21..22, 24..25) -> ALL 4 tiles pas=0xf!

    lamp_pts = []
    for nm, x, y in (
        # Upper retaining terrace y=2..3 dressing (planters, stone benches, hedges, topiaries framing Glasshouse Steps!)
        ('pf_planter0', 15, 2), ('pf_planter2', 26, 2), ('pf_stonebench', 10, 2), ('pf_stonebench', 31, 2),
        ('nt_azalea0', 6, 2), ('nt_azalea2', 35, 2), ('lm_topiary', 18, 2), ('lm_topiary', 24, 2),
        # Lower Rootward wash courtyard & alleys (somber authentic working-class props — ZERO carnival party lights!)
        ('hb_washline', 14, 23), ('hb_washline', 24, 23), ('pf_p_laundry', 15, 27), ('pf_p_laundry', 24, 22),
        ('hb_tubs', 17, 25), ('hb_tubs', 23, 26), ('hb_barrel', 10, 14), ('hb_barrel2', 29, 14),
        ('sh_crates', 7, 16), ('hb_boxes', 35, 16), ('pf_logbench', 19, 27),
        ('nt_azalea0', 8, 21), ('nt_shrub1', 37, 21), ('hb_barrel', 17, 22), ('hb_boxes', 25, 22),
    ):
        put_safe(m, nm, x, y, on='.cd', r=1, prot=prot)

    for lx, ly in ((13, 3), (29, 3), (18, 8), (24, 8), (9, 15), (28, 15), (14, 22), (26, 22), (38, 22), (18, 27)):
        if can_put_clean(m, 'pf_lantern', lx, ly - 2, on='.cd', prot=prot):
            m.stamp('pf_lantern', lx, ly - 2)
            lamp_pts.append((lx, ly - 1))

    paint_rail_run(m, 8, 18, 4, kind='rw')
    paint_rail_run(m, 24, 35, 4, kind='rw')

    for idx, (cx, cy) in enumerate(((4, 8), (39, 8), (4, 27), (39, 18), (8, 3), (35, 3))):
        place_canopy_grove(m, cx, cy, ROYAL_CANOPY, count=3, radius=2.0, on='.', seed=idx + 80, prot=prot, undergrowth=True)

    m.greenfill(3)
    m.paint()

    # Paint TWO Rustic Cedar Footbridges across the Irrigation Drainage Runnel (x=11..13 & x=32..34)!
    _paint_bridge_ns(m, 11, 13, 18, 21)
    _paint_bridge_ns(m, 32, 34, 18, 21)

    # Stamp crisp ascending stone steps at North "Glasshouse Ward Steps" exit (20..22, 1)!
    m.L[1, 1, 20] = P1('st_stair_l')
    m.L[1, 1, 21] = P1('st_stair_m')
    m.L[1, 1, 22] = P1('st_stair_r')
    m.L[2, 1, 20] = 0
    m.L[2, 1, 21] = 0
    m.L[2, 1, 22] = 0

    # Somber lamp-only warm glows (ZERO carnival lstring lights & ZERO bridge/well/stair yellow blobs!)
    add_warm_glows(m, lamp_pts)
    add_water_glints(m, water_cls='w', seed=296, density=0.04)
    m.scatter(10, seed=296, on='.T')

    # Keep bridges clean of stray scatter and seal ALL North/West/East warp flanking tiles cleanly!
    for bx0, bx1 in ((11, 13), (32, 34)):
        for by in range(18, 22):
            for bx in range(bx0, bx1 + 1):
                m.L[1, by, bx] = 0
    for fx, fy in ((19, 1), (23, 1), (19, 2), (23, 2), (1, 13), (1, 17), (42, 21), (42, 25)):
        if m.L[1, fy, fx] == 0:
            m.L[1, fy, fx] = P1('nt_bush0')

    seal_unconnected_edges(m, open_cells=())

    Lr = RC.resolve(m.L, TID_CITY).astype(np.int32)
    ev_pts = [tuple(e['at']) for e in m.events]
    PG.guard(Lr, TID_CITY, ev_pts, 'Map 296')
    assert not PG.hits(Lr, R.tilesets()[TID_CITY], ev_pts), 'Map 296 passguard hits!'
    _verify_map(Lr, TID_CITY, m.events, (21, 3), 'Map 296 Verdance - Rootward', outdoor=True)

    np.save(os.path.join(HERE, 'data', 'raw', '296.npy'), Lr.astype(np.int16))
    spec = {
        'id': 296,
        'name': 'Verdance - Rootward',
        'parent': 280,
        'bgm': 'Natural Park',
        'field': 'FLOWER_GARDEN',
        'rubric': True,
        'yards_ok': True,
        'map_audio': {'bgm': 'Town - Elowen', 'bgs': 'Gossamer Deepwood', 'bgs_volume': 35},
        'tone': [-14, -4, -10, 12],
        'metadata': {'Name': 'Verdance - Rootward', 'Outdoor': True, 'ShowArea': True, 'Bicycle': True,
                     'MapPosition': VERD_POS, 'BattleBack': 'field'},
        'biome': 'city',
        'tileset': TID_CITY,
        'raw': 'data/raw/296.npy',
        'events': m.events,
    }
    with open(os.path.join(HERE, 'specs', '296_verdance_rootward.yaml'), 'w', encoding='utf-8') as f:
        f.write('# GENERATED by mapgen/layouts/verdance_wards.py (Batch 3E): Verdance - Rootward.\n')
        f.write(yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))
    print('Wrote specs/296_verdance_rootward.yaml and data/raw/296.npy')


def main():
    build_283()
    build_284()
    build_288()
    build_289()
    build_294()
    build_296()
    print('Done: built all 6 Verdance wards, Briar Hall interiors & Heartgarden maps (283, 284, 288, 289, 294, 296).')


if __name__ == '__main__':
    main()
