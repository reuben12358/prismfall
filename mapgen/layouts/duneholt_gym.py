#!/usr/bin/env python3
"""layouts/duneholt_gym.py — Batch 3D: Duneholt Gym 5 ("The Dig", Warden Sahar Ostrand — 4 Maps: 210, 211, 212, 213):
  - Map 210: Duneholt Gym - Entrance         (21x17, TS 57 PF Rejuv Cave cvE2, field :DESERT)
      * Exact warp parity with 200_duneholt_terrace_bazaar.yaml (8, 38) -> arrives (10, 15) facing up!
      * Return warps (9..11, 16) -> 200 (8, 39) down.
      * Fake painted north door mural ("Everyone tries the door. The way in is down.")
      * TEACH Cracked Soft-Sand Drop Zone (x=8..12, y=7..9) -> drops smoothly into 212 Cellar (14, 23) up!
      * Gym Guide (Ch6 canon), Excavation Medic (full heal), Sahar's Aide, Excavator Foreman (HM04 Strength after badge!),
        canonical PBS trainer [PICNICKER, Layla].
  - Map 211: Duneholt Gym - Puzzle Room 1    ("The Dunes", 29x25, TS 57 PF Rejuv Cave cvE2, field :DESERT)
      * Twin footprint directly above 212 The Under-Dig!
      * Four sun-hardened / shade-sinking sand lanes:
          a (T0 <-> T1, lit iff V325 == 0 [start])
          b (T0 <-> T2, lit iff V325 == 1)
          c (T1 <-> T3, lit iff V326 == 2)
          d (T2 <-> Cistern X [Max Ether], lit iff V326 == 0 [start])
      * Two rotatable Sun-Mirrors: M1 on T1 (3, 12) cycles V325; M2 on T2 (25, 12) cycles V326.
      * Apprentice Nadim on T0 (17, 22): status readout, instant reset, 3-tier hints, puzzleskip support.
      * Canonical PBS trainers [HIKER, Osman] (T1) & [RUINMANIAC, Darius] (T3).
  - Map 212: Duneholt Gym - Puzzle Room 2    ("The Under-Dig", 29x25, TS 57 PF Rejuv Cave cvE2, field :DESERT)
      * Five airtight sealed subterranean galleries directly under 211's lanes & cellar:
          Cellar (from 210 drop) -> Ladder (14, 22) up to 211 T0 + Rope (12, 22) back to 210
          Ua (under lane a)      -> Ladder Ha (4, 14) up to 211 T1  [Glyph A: WAVE]
          Ub (under lane b)      -> Ladder Hb (18, 20) up to 211 T0 [Glyph B: SUN]
          Uc (under lane c)      -> Long dig tunnel -> Ladder Hc (22, 12) up to 211 T2 [Glyph C: BONE]
          Ud (under lane d)      -> Optional Mastery 4-Tablet Mural Shrine (V425..V428 -> S325: Telluric Seed x2 + Soft Sand!)
                                    -> Ladder Hd (26, 14) up to 211 T2 [Glyph D: EYE]
      * Zero-softlock Under-Dig Reset Apprentice Samim in Uc (17, 12) + canonical PBS trainers [RUINMANIAC, Farah] & [HIKER, Burak].
  - Map 213: Duneholt Gym - Warden Arena     (21x17, TS 57 PF Rejuv Cave cvE2, field :DESERT)
      * Sunlit sandstone excavation pit under overhead light shafts, 5x5 golden sundial center ring (lm_sun),
        labelled bone alcoves, burning braziers (100% intact flames!), framed Fast-Exit Lift -> 210 (10, 14) down.
      * Warden Sahar Ostrand (Prismfall.gym_battle(pfm_gym(:LEADER_SAHAR), double: false), Sandglass Badge, TM83 Bulldoze,
        :ch6_drillsite reactivity, S325 Mastery mural reaction, V126 CH6_STEP = 5).

Canonical sources:
  - design/GYM_PUZZLES.md (Gym 5: V325-V326, S325-S326, V425-V428)
  - story/25_SCRIPT_CH6.md (Maps 210-213 dialogue, Gym Guide, Aide, Nadim, Sahar, HM04 excavators)
  - pbs/trainers.txt (Layla, Darius, Osman, Farah, Burak, LEADER_SAHAR — 0 duplicates)

Run:
    /usr/bin/python3 -I mapgen/layouts/duneholt_gym.py
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

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TID = 57
FIELD = 'DESERT'
DUN_POS = [0, 17, 3]

# Canonical Gym 5 Switch / Variable IDs (design/GYM_PUZZLES.md §Gym 5 — 0 collisions across repo!)
V_MIRROR_1 = 325          # 0 = Lane a lit (start), 1 = Lane b lit, 2 = Wall
V_MIRROR_2 = 326          # 0 = Lane d lit (start), 1 = Wall, 2 = Lane c lit
S_MURAL_DONE = 325        # Optional 4-tablet Elector Mural Mastery solved in 212 Ud
S_FIRST_FALL = 326        # First-fall teaching message shown in 210
S_STRENGTH_TAUGHT = 327   # HM04 Strength received from Sahar's excavators after Badge 5
V_TAB_A, V_TAB_B, V_TAB_C, V_TAB_D = 425, 426, 427, 428  # 0=Sun, 1=Eye, 2=Wave, 3=Bone

# Verified TS 57 (PF Rejuv Cave) Tile IDs
T_CRUST_0 = P1('lm_plaza0')      # 24376, pas=0x0, pri=0 (sun-baked golden travertine crust!)
T_CRUST_1 = P1('lm_plaza1')      # 24378, pas=0x0, pri=0
T_SOFT_0 = P1('cv_mud0')         # 23985, pas=0x0, pri=0 (dark shaded loose sand — sinks to 212!)
T_SOFT_1 = P1('cv_mud0')         # uniform dark desert shade (zero blue pebble!)
T_HOLE = P1('cv_hole')           # 23876, pas=0x0, pri=0 (circular excavation ladder shaft)
T_LADDER_Q = P1('cv_ladder_q')   # 24006, pas=0x0, pri=0 (return rope/ladder rungs)
T_DIAL = P1('wr_dial')           # 23029, pas=0xf, pri=0 (brass sun-mirror azimuth dial)
T_PLINTH = P1('mn_plinth')       # 24250, pas=0xf, pri=0 (solid stone relic plinth)
T_PDOOR = P1('mn_door')          # 24366, pas=0xf, pri=0 (solid warm wooden/ochre fake painted door!)
T_PDOOR_OPEN = P1('lm_pdoor_open')  # 25936, pas=0x0, pri=0 (open doorway portal)
T_LATCH_OPEN = P1('lm_latch_open')  # 25938, pas=0x0, pri=0 (fast-exit excavation lift pad)
T_LAMP_OFF = P1('lm_lamp')       # 25931, pas=0xf, pri=0
T_LAMP_ON = P1('lm_lamp_on')     # 25932, pas=0xf, pri=0
T_STRIP_H_ON = P1('lm_strip_h_on')  # 25924, pas=0x0, pri=0
T_STRIP_V_ON = P1('lm_strip_v_on')  # 25926, pas=0x0, pri=0

# Twin-footprint sand lane rectangles on 211 (each tile drops to exact same (x,y) on 212!)
LANE_A = [(x, y) for y in range(19, 22) for x in range(6, 10)]    # 4x3 = 12 tiles (T0 <-> T1)
LANE_B = [(x, y) for y in range(19, 22) for x in range(19, 23)]   # 4x3 = 12 tiles (T0 <-> T2)
LANE_C = [(x, y) for y in range(5, 9) for x in range(4, 8)]       # 4x4 = 16 tiles (T1 <-> T3)
LANE_D = [(x, y) for y in range(5, 9) for x in range(21, 25)]     # 4x4 = 16 tiles (T2 <-> Cistern X)
ALL_LANES = set(LANE_A) | set(LANE_B) | set(LANE_C) | set(LANE_D)


# =================================================================================================
# Shared Desert Sandstone Gym Helpers (Zero P0s: Safe L[2] Overlays, 100% Intact Flames, 4-bit BFS)
# =================================================================================================
def _setup_cve2():
    K.KITS['cvE2'] = dict(K.KITS['cvE'], rows=[K.KITS['cvE']['rows'][0], K.KITS['cvE']['rows'][2]])


def _new_dig_cave(W, H, seed):
    _setup_cve2()
    m = Cave(W, H, 'E', seed=seed, pool='Cave Pool', tid=TID)
    m.STAIRS = (P1('E_stairl'), P1('E_stairm'), P1('E_stairr'))
    m.kit = {TER: 'cvE2', FLOOR: 'cvE2', MASS: 'cvE2', 'default': 'cvE2'}
    return m


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


def _add_safe_overlay(Lr, tid, stamp_name, pts):
    """Stamp overhead sunbeams / glow halos STRICTLY onto unoccupied L[2] cells — NEVER deletes brazier flames!"""
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


def _assert_braziers_intact(Lr, braziers, label):
    """Programmatically verify 100% of fw_brazier L[2] flame tiles survived untouched."""
    br_ref = RC.resolve(np.array(STAMPS['fw_brazier']['layers'], dtype=np.int32), TID)
    flame_tid = int(br_ref[2, 0, 0])
    for bx, by in braziers:
        assert int(Lr[2, by, bx]) == flame_tid, (
            f'{label}: fw_brazier flame damaged at ({bx},{by})! got {Lr[2, by, bx]} != {flame_tid}'
        )


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


def _trainer(at, ttype, name, d, intro, after, sight=3):
    return {
        'type': 'trainer',
        'name': 'Trainer(%d)' % sight,
        'at': list(at),
        'sight': sight,
        'dir': d,
        'sprite': 'trainer_' + ttype,
        'trainer': [ttype, name],
        'intro': intro,
        'after': after,
        'rules': ['setBattleRule("field", :%s)' % FIELD],
    }


def _paint_desert_floors(m, zones):
    """Apply cohesive warm Ossaria excavation flooring (sand E_f, travertine plaza, terracotta mosaic G_f, shaded mud)."""
    palettes = {
        'sand': [P1('E_f%d' % i) for i in range(4)],
        'plaza': [P1('lm_plaza0'), P1('lm_plaza1')],
        'mosaic': [P1('G_f%d' % i) for i in range(4)],
        'shaded': [P1('cv_mud0'), P1('cv_mud1')],
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


def _paint_sun_medallion(m, sx, sy):
    """Inlay the 5x5 golden-ivory lm_sun sundial medallion cleanly onto L[0] (all pas=0x0)."""
    sun_L = RC.resolve(np.array(STAMPS['lm_sun']['layers'], dtype=np.int32), TID)
    for dy in range(sun_L.shape[1]):
        for dx in range(sun_L.shape[2]):
            t = int(sun_L[0, dy, dx] or sun_L[1, dy, dx])
            xx, yy = sx + dx, sy + dy
            if t and m.inb(xx, yy) and not m.cliff[yy, xx]:
                m.L[0, yy, xx] = t
                m.L[1, yy, xx] = 0


def _ev_active_page(e, vars_, sw):
    pages = e.get('pages') or [{}]
    for pg in reversed(pages):
        c = pg.get('cond') or {}
        if 'switch' in c and not sw.get(c['switch'], False):
            continue
        if 'switch2' in c and not sw.get(c['switch2'], False):
            continue
        if 'var' in c and vars_.get(c['var'][0], 0) < c['var'][1]:
            continue
        if 'self' in c:
            continue
        return pg
    return None


def _sim_bfs(Lr, events, start, targets, label, vars_=None, sw=None, block_touch_names=None):
    """Exact Essentials 4-bit directional + tile-event BFS for a given (vars_, sw) puzzle state."""
    vars_ = vars_ or {}
    sw = sw or {}
    block_touch_names = block_touch_names or ()
    ts = R.tilesets()[TID]
    H, W = Lr.shape[1:]
    by_cell = {}
    for e in events:
        if e and e.get('at'):
            by_cell.setdefault(tuple(e['at']), []).append(e)

    def dir_ok(x, y, d):
        bit = 1 << (d // 2 - 1)
        for e in by_cell.get((x, y), []):
            t = e.get('type')
            if t in ('npc', 'trainer', 'mart'):
                return False
            if t == 'event':
                pg = _ev_active_page(e, vars_, sw)
                if pg is None or pg.get('through'):
                    continue
                if pg.get('trigger') == 'touch' and any((e.get('name') or '').startswith(pfx) for pfx in block_touch_names):
                    return False
                g = pg.get('graphic') or {}
                tid = g.get('tile')
                if tid:
                    p = ts['passages'][tid]
                    if p & bit or (p & 0x0f) == 0x0f:
                        return False
                    if ts['priorities'][tid] == 0:
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

    def cell_ok(x, y):
        return dir_ok(x, y, 2) or dir_ok(x, y, 4) or dir_ok(x, y, 6) or dir_ok(x, y, 8)

    sx, sy = start
    assert cell_ok(sx, sy), f'{label}: start {start} is NOT passable!'
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
    missing = []
    for name, (tx, ty), adj in targets:
        if adj:
            reach = (tx, ty) in seen or any((tx + dx, ty + dy) in seen for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)))
        else:
            reach = (tx, ty) in seen
        if not reach:
            missing.append((name, (tx, ty)))
    if targets:
        print(f'{label}: reached {len(seen)} cells from {start}; missing={missing}')
        assert not missing, f'{label} unreachable targets: {missing}'
    return seen


def _verify_no_over_trigger_and_sightlines(Lr, events, label):
    """Enforce ZERO over_trigger? traps on action signs/plaques AND 100% unobstructed trainer sightlines!"""
    import build as B
    ts = R.tilesets()[TID]
    H, W = Lr.shape[1:]
    solid_ev = set()
    for e in events:
        if e.get('type') in ('npc', 'trainer', 'mart'):
            solid_ev.add(tuple(e['at']))
        elif e.get('type') == 'event':
            pg0 = (e.get('pages') or [{}])[0]
            g0 = pg0.get('graphic') or {}
            if not pg0.get('through') and (g0.get('sprite') or (g0.get('tile') and (ts['passages'][g0['tile']] & 0x0f) == 0x0f)):
                solid_ev.add(tuple(e['at']))
    for e in events:
        et = e.get('type')
        ex, ey = e['at']
        if et == 'sign':
            assert not B.cell_passable(Lr, ts, ex, ey) or (ex, ey) in solid_ev, (
                f'{label}: OVER_TRIGGER TRAP! sign {e.get("name")} at {(ex, ey)} sits on walkable floor!'
            )
        if et == 'trainer':
            dmap = {'down': (0, 1), 'left': (-1, 0), 'right': (1, 0), 'up': (0, -1)}
            dx, dy = dmap[e.get('dir', 'down')]
            sight = int(e.get('sight', 0))
            for step in range(1, sight + 1):
                nx, ny = ex + dx * step, ey + dy * step
                assert 0 <= nx < W and 0 <= ny < H, f'{label}: trainer {e.get("trainer")} sight OOB at step {step}!'
                assert B.cell_passable(Lr, ts, nx, ny) and (nx, ny) not in solid_ev, (
                    f'{label}: trainer {e.get("trainer")} sight BLOCKED at {(nx, ny)} step {step}!'
                )


def _soft_sand_drop_ruby(lane_label):
    """Player-Touch drop script for soft/shaded sand lanes on 211 -> transfers cleanly to exact same (x,y) on 212!"""
    return (
        'pbSEPlay("Anim/Earth4", 90, 90)\n'
        'pfm_shake(2, 10, 10)\n'
        f'pbMessage(_INTL("The shaded sand of Lane {lane_label} gives way! You drop cleanly into the Under-Dig below!"))\n'
        'if defined?(pfp_swap_map)\n'
        '  pfp_swap_map(212)\n'
        'else\n'
        '  pbFadeOutIn do\n'
        '    $game_temp.player_new_map_id = 212\n'
        '    $game_temp.player_new_x = $game_player.x\n'
        '    $game_temp.player_new_y = $game_player.y\n'
        '    $game_temp.player_new_direction = $game_player.direction\n'
        '    $scene.transfer_player\n'
        '  end\n'
        'end'
    )


def _lane_tile_event(lane, x, y):
    """Dynamic multi-page sand lane event on 211:
      - LIT  -> T_CRUST_0/1 (bright golden sun-hardened travertine, pas=0x0, action, firm & walkable!)
      - SOFT -> T_SOFT_0/1  (dark shaded loose sand, pas=0x0, trigger=touch -> drops to 212 at same (x,y)!)
    RMXP var conditions test `>= k`:
      - Lane a lit iff V325 == 0  -> P0 [>=0] LIT,  P1 [V325>=1] SOFT
      - Lane b lit iff V325 == 1  -> P0 [>=0] SOFT, P1 [V325>=1] LIT, P2 [V325>=2] SOFT
      - Lane c lit iff V326 == 2  -> P0 [>=0] SOFT, P1 [V326>=2] LIT
      - Lane d lit iff V326 == 0  -> P0 [>=0] LIT,  P1 [V326>=1] SOFT
    """
    crust = T_CRUST_0 if (x + y) % 2 == 0 else T_CRUST_1
    soft = T_SOFT_0 if (x + y) % 2 == 0 else T_SOFT_1
    drop_cmd = [{'script': _soft_sand_drop_ruby(lane.upper())}]

    def pg_lit(cond=None):
        p = {'graphic': {'tile': crust}, 'trigger': 'action', 'commands': []}
        if cond:
            p['cond'] = cond
        return p

    def pg_soft(cond=None):
        p = {'graphic': {'tile': soft}, 'trigger': 'touch', 'commands': drop_cmd}
        if cond:
            p['cond'] = cond
        return p

    if lane == 'a':
        pages = [pg_lit(), pg_soft({'var': [V_MIRROR_1, 1]})]
    elif lane == 'b':
        pages = [pg_soft(), pg_lit({'var': [V_MIRROR_1, 1]}), pg_soft({'var': [V_MIRROR_1, 2]})]
    elif lane == 'c':
        pages = [pg_soft(), pg_lit({'var': [V_MIRROR_2, 2]})]
    elif lane == 'd':
        pages = [pg_lit(), pg_soft({'var': [V_MIRROR_2, 1]})]
    else:
        raise ValueError(lane)
    return {'type': 'event', 'name': f'Sand {lane} {x},{y}', 'at': [x, y], 'pages': pages}


# =================================================================================================
# 1. MAP 210 — DUNEHOLT GYM - ENTRANCE ("The Dig — TEACH", 21x17, TS 57, :DESERT)
# Exact arrival from 200_duneholt_terrace_bazaar.yaml (8, 38): (10, 15) facing up!
# =================================================================================================
def build_210():
    W, H = 21, 17
    m = _new_dig_cave(W, H, seed=210)

    # Sculpted Sandstone Excavation Lobby (x=2..18, y=3..14 -> walkable y=4..14) + South Entry Vestibule (x=8..12, y=15..16)
    m.box(2, 3, 18, 14, FLOOR, '.')
    m.box(8, 14, 12, 16, FLOOR, '.')
    m.mass_at([
        (2, 3), (18, 3), (2, 13), (2, 14), (3, 14),
        (18, 13), (18, 14), (17, 14),
    ])
    m.tidy()
    m.plan_cliffs(rows=2)

    E = m.events

    # South Return Warps (9..11, 16) -> 200 Duneholt Terrace Bazaar (8, 39) facing down!
    for rx in (9, 10, 11):
        E.append({
            'type': 'warp',
            'name': 'Exit to Duneholt',
            'at': [rx, 16],
            'to': {'map': 200, 'x': 8, 'y': 39, 'dir': 'down'},
            'se': 'Door exit',
        })

    # TEACH Cracked Soft-Sand Pit (x=8..12, y=7..9): touch drops smoothly into 212 Under-Dig Cellar (14, 23) facing up!
    teach_drop_ruby = (
        'pbSEPlay("Anim/Earth4", 90, 90)\n'
        'pfm_shake(2, 10, 10)\n'
        f'if !$game_switches[{S_FIRST_FALL}]\n'
        f'  $game_switches[{S_FIRST_FALL}] = true\n'
        '  pbMessage(_INTL("The shaded sand gives way beneath your boots! You slide down a carved excavation chute into the Under-Dig cellar below..."))\n'
        'else\n'
        '  pbMessage(_INTL("You drop down the soft-sand chute into the Under-Dig cellar."))\n'
        'end\n'
        'pbFadeOutIn do\n'
        '  $game_temp.player_new_map_id = 212\n'
        '  $game_temp.player_new_x = 14\n'
        '  $game_temp.player_new_y = 23\n'
        '  $game_temp.player_new_direction = 8\n'
        '  $scene.transfer_player\n'
        'end'
    )
    for y in range(7, 10):
        for x in range(8, 13):
            E.append({
                'type': 'event',
                'name': f'Teach Sand {x},{y}',
                'at': [x, y],
                'pages': [{'trigger': 'touch', 'commands': [{'script': teach_drop_ruby}]}],
            })

    # Fake Painted North Door Mural on solid cliff wall (10, 3) -> reachable from (10, 4)!
    E.append(_sign(
        'Painted North Door', (10, 3),
        "You press against the grand iron-banded door — it doesn't budge a hair. Looking closer, the hinges, rivets, and keyhole are painted straight onto solid canyon sandstone in red ochre!"
    ))

    # Gym Guide (story/25_SCRIPT_CH6.md lines 322-326!)
    E.append(_make_npc('Gym Guide', (7, 13), 'NPC 21', 'right', [
        "Gym Guide: Yo, challenger! Welcome to The Dig — Ground-types on the Desert field!",
        "Gym Guide: Water, Grass, and Ice dig in here. Electric doesn't, ever, at all.",
        "Gym Guide: Sun hardens and shade sinks. The sun-mirrors downstairs pick which sand lanes bake into crust and which stay soft.",
        "Gym Guide: Falling isn't failing in here. Warden Sahar says falling's how you find the second floor!",
    ]))

    # Excavation Medic (full party heal right inside the entrance lobby!)
    heal_ruby = (
        'pbMessage(_INTL("Excavation Medic: Desert grit gets into every joint. Let me brush off your Pokémon and patch them up!"))\n'
        'pbMEPlay("Pkmn healing")\n'
        'pbFadeOutIn do\n'
        '  $player.heal_party\n'
        'end\n'
        'pbMessage(_INTL("Excavation Medic: Right as rain — or as close as we get in Ossaria! Stop back anytime."))'
    )
    E.append({
        'type': 'event',
        'name': 'Excavation Medic',
        'at': [13, 13],
        'pages': [{
            'graphic': {'sprite': 'NPC 18', 'dir': 'left'},
            'trigger': 'action',
            'move': 'fixed',
            'commands': [{'script': heal_ruby}],
        }],
    })

    # Sahar's Aide right beside the fake painted north door (story/25_SCRIPT_CH6.md:320-321!)
    E.append(_make_npc("Sahar's Aide", (12, 4), 'NPC 14', 'down', [
        "Sahar's Aide: Everyone tries the door. The door's painted on.",
        "Sahar's Aide: The way in is down — step right onto the shaded cracked sand in the center of the hall!",
    ]))

    # Excavator Foreman — teaches / awards HM04 Strength once Warden Sahar is beaten (story/25_SCRIPT_CH6.md:360-364!)
    excavator_ruby = (
        'if (pfm_gym_won?(:LEADER_SAHAR) rescue false)\n'
        f'  if !$game_switches[{S_STRENGTH_TAUGHT}]\n'
        '    pbMessage(_INTL("Excavator Foreman: Word came up the lift — you beat Warden Sahar! She told us to hand this over the moment you surfaced."))\n'
        '    pbReceiveItem(:HM04)\n'
        f'    $game_switches[{S_STRENGTH_TAUGHT}] = true\n'
        '    pbMessage(_INTL("Excavator Foreman: HM04 Strength! With the Sandglass Badge, your Pokémon can shove heavy tomb boulders clear — handy out on the Marrow Road and inside the Ossuary of Dunes!"))\n'
        '  else\n'
        '    pbMessage(_INTL("Excavator Foreman: Put Strength to good use out in the Ossuary of Dunes — those Elector-era boulders haven\'t budged in three hundred years!"))\n'
        '  end\n'
        'else\n'
        '  pbMessage(_INTL("Excavator Foreman: We\'re shoring the upper excavation walls. Once you earn Sahar\'s Sandglass Badge, come talk to me — my crew has HM04 Strength waiting for you!"))\n'
        'end'
    )
    E.append({
        'type': 'event',
        'name': 'Excavator Foreman',
        'at': [15, 11],
        'pages': [{
            'graphic': {'sprite': 'trainer_FOREMAN', 'dir': 'left'},
            'trigger': 'action',
            'move': 'fixed',
            'commands': [{'script': excavator_ruby}],
        }],
    })

    # Canonical PBS Trainer for Map 210: [PICNICKER, Layla] (pbs/trainers.txt:12738 — sight 2 open to (5,9),(6,9)!)
    E.append(_trainer(
        (4, 9), 'PICNICKER', 'Layla', 'right',
        "Picnicker Layla: I came down here to look for shade and a quiet lunch — and now the sand's trying to eat my basket! Battle me while I still have footing!",
        "Picnicker Layla: The sand took my sandwich and you took the rest.",
        sight=2,
    ))

    # Solid Gym Statues flanking entrance arrival (10, 15) — pas=0xf bases at (8,14) and (12,14)!
    E += [
        _sign('Dig Statue West', (8, 14),
              "DUNEHOLT GYM — THE DIG · WARDEN: SAHAR OSTRAND · TYPE: GROUND · FIELD: DESERT · BADGE: SANDGLASS BADGE."),
        _sign('Dig Statue East', (12, 14),
              "SAHAR'S FIRST RULE OF EXCAVATION: SUN HARDENS SAND INTO CRUST; SHADE KEEPS IT SOFT. FALLING IS HOW YOU REACH THE SECOND FLOOR."),
    ]

    # Protect arrival (10, 15), return warps, teach pit, walkways & events
    for pt in [(10, 15), (9, 15), (11, 15), (9, 16), (10, 16), (11, 16), (10, 4), (10, 5), (10, 6), (5, 9), (6, 9)]:
        m.keep_clear.add(pt)
    for y in range(7, 10):
        for x in range(8, 13):
            m.keep_clear.add((x, y))
    for e in E:
        ex, ey = e['at']
        m.keep_clear.add((ex, ey))

    # Architecture: Fake Painted North Door Frame, Ossarian Bone Banners, Braziers, Statues, Excavation Props!
    _place_stamp_over(m, 'cv_frame', 9, 2, base_z=1, top_z=2, top_rows=1, solid=False)
    m.over.append((1, 10, 3, T_PDOOR))                                     # Solid faux-door painted on cliff face (10,3)!
    _place_stamp_over(m, 'wr_ban_bone', 7, 3, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'wr_ban_bone', 13, 3, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'lm_banner_w', 8, 2, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'lm_banner_w', 12, 2, base_z=1, top_z=2, top_rows=1, solid=True)

    # Excavation Pit Perimeter Bollards & Sandbags (x=7 and x=13 flanking y=7..9 soft sand!)
    for bx, by in ((7, 7), (13, 7), (7, 9), (13, 9)):
        _place_stamp_over(m, 'lm_bollard', bx, by, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'wr_sandbags', 7, 8, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'wr_sandbags', 13, 8, base_z=1, top_z=1, top_rows=0, solid=True)

    # Entrance Statues (bases at (8,14) and (12,14) -> solid pas=0xf!)
    _place_stamp_over(m, 'mn_statue', 8, 13, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'mn_statue', 12, 13, base_z=1, top_z=2, top_rows=1, solid=True)

    # Sandstone Columns, Excavation Crates, Bone Cart & 6 Burning Braziers!
    _place_stamp_over(m, 'nr_col', 4, 4, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'nr_col', 16, 4, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'wr_bonecart', 3, 11, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'wr_supply', 16, 6, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'wr_sacks', 17, 11, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'wr_tripod', 15, 4, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'wr_sacks', 3, 6, base_z=1, top_z=1, top_rows=0, solid=True)

    braziers_210 = [(6, 5), (14, 5), (6, 11), (14, 11), (7, 15), (13, 15)]
    # Note: (7,15)/(13,15) are rock wall; place south braziers inside hall at (5,13) and (15,13)!
    braziers_210 = [(6, 5), (14, 5), (6, 11), (14, 11), (5, 13), (15, 13)]
    for bx, by in braziers_210:
        _place_stamp_over(m, 'fw_brazier', bx, by, base_z=1, top_z=2, top_rows=1, solid=True)

    for sx, sy in ((5, 2), (15, 2)):
        m.over.append((2, sx, sy, P1('cv_walllamp')))

    m.paint()
    _paint_desert_floors(m, [
        (2, 4, 18, 14, 'sand'),
        (8, 4, 12, 6, 'plaza'),
        (8, 10, 12, 16, 'plaza'),
    ])
    # Warm shaded desert sand ripples over uniform dark cv_mud0 for the TEACH drop pit (8..12, 7..9) — ZERO blue ice cracks!
    ripples = [P1('wr_ripple0'), P1('wr_ripple1'), P1('wr_ripple2')]
    for y in range(7, 10):
        for x in range(8, 13):
            m.L[0, y, x] = T_SOFT_0
            m.L[1, y, x] = ripples[(x * 2 + y) % 3]
    # Scattered excavation bone fragments on the side aisles
    for rx, ry, t in ((4, 7, 'wr_bones0'), (16, 9, 'wr_bones1'), (5, 11, 'wr_ripple0'), (15, 9, 'wr_ripple1')):
        if int(m.L[1, ry, rx]) == 0:
            m.L[1, ry, rx] = P1(t)

    Lr = RC.resolve(m.L, TID).astype(np.int32)
    _add_safe_overlay(Lr, TID, 'cv_shaft', [(9, 4), (4, 6), (15, 6)])
    _add_safe_overlay(Lr, TID, 'pf_glow', braziers_210)
    _assert_braziers_intact(Lr, braziers_210, 'Map 210')

    ev_pts = [tuple(e['at']) for e in E]
    PG.guard(Lr, TID, ev_pts, 'Map 210')
    assert not PG.hits(Lr, R.tilesets()[TID], ev_pts), 'Map 210 passguard hits!'
    _verify_no_over_trigger_and_sightlines(Lr, E, 'Map 210')
    _sim_bfs(Lr, E, (10, 15), [
        ('Exit to 200', (10, 16), False),
        ('Gym Guide', (7, 13), True),
        ('Excavation Medic', (13, 13), True),
        ('Excavator Foreman', (15, 11), True),
        ('Trainer Layla', (4, 9), True),
        ('Painted North Door', (10, 3), True),
        ("Sahar's Aide", (12, 4), True),
        ('Statue West', (8, 14), True),
        ('Statue East', (12, 14), True),
    ], 'Map 210 Entrance (around pit)', block_touch_names=('Teach Sand',))
    _sim_bfs(Lr, E, (10, 15), [
        ('Teach Drop Pit center', (10, 8), False),
        ('Teach Drop Pit NW', (8, 7), False),
        ('Teach Drop Pit SE', (12, 9), False),
    ], 'Map 210 Entrance (onto pit)')

    m.L = Lr
    head = {
        'id': 210,
        'name': 'Duneholt Gym - Entrance',
        'parent': 200,
        'bgm': 'Gym',
        'field': FIELD,
        'map_audio': {'bgm': 'Gym - Warden Hall', 'bgs': 'Wind - Isenmar', 'bgs_volume': 25, 'rain': False},
        'metadata': {'Name': 'Duneholt Gym', 'SnapEdges': True, 'MapPosition': DUN_POS, 'BattleBack': 'desert'},
        'tone': [14, 6, -10, 4],
        '_file': '210_duneholt_gym.yaml',
    }
    m.write(210, head, comment='# GENERATED by mapgen/layouts/duneholt_gym.py (Batch 3D): Duneholt Gym - Entrance (TEACH).\n'
                               '# Edit the layout script, not this file.\n')
    return m, Lr


# =================================================================================================
# 2. MAP 211 — DUNEHOLT GYM - PUZZLE ROOM 1 ("The Dunes — TWIST", 29x25, TS 57, :DESERT)
# =================================================================================================
def _mirror_ruby(mirror_name, var_id, states_meta):
    """Self-contained RMXP Ruby for rotatable Sun-Mirror M1/M2 (cycles 0 -> 1 -> 2 -> 0)."""
    # states_meta: [(0, label0, desc0), (1, label1, desc1), (2, label2, desc2)]
    lbl_cases = '\n'.join(f'when {k} then "{lbl}"' for k, lbl, _ in states_meta)
    desc_cases = '\n'.join(f'when {k} then "{desc}"' for k, _, desc in states_meta)
    return f'''cur = $game_variables[{var_id}].to_i % 3
cur_lbl = case cur
{lbl_cases}
else "Wall"
end
c = pbMessage(_INTL("{mirror_name} is aimed at {{1}}.", cur_lbl),
              [_INTL("Rotate sun-mirror"), _INTL("Leave it")], 2)
if c == 0
  nxt = (cur + 1) % 3
  pbSEPlay("Strength push", 85, 105)
  pbSEPlay("Mining reveal", 70, 120)
  $game_variables[{var_id}] = nxt
  $game_map.need_refresh = true
  msg = case nxt
{desc_cases}
  else "The beam sweeps harmlessly onto bare canyon sandstone."
  end
  pbMessage(_INTL("{{1}}", msg))
end'''


def _reset_dig_ruby(warp_to_211=False):
    warp = (
        '  $game_temp.player_new_map_id = 211\n'
        '  $game_temp.player_new_x = 14\n'
        '  $game_temp.player_new_y = 21\n'
        '  $game_temp.player_new_direction = 8\n'
        '  $scene.transfer_player\n'
    ) if warp_to_211 else (
        '  $game_player.moveto(14, 21)\n'
        '  $game_player.turn_up\n'
    )
    return f'''pbSEPlay("Strength push", 85, 100)
pbFadeOutIn do
  $game_variables[{V_MIRROR_1}] = 0
  $game_variables[{V_MIRROR_2}] = 0
{warp}  $game_map.need_refresh = true
end
pbMessage(_INTL("Both sun-mirrors swung back to start: Lane A (west) and Lane D (northeast) are sun-hardened crust!"))'''


def _nadim_ruby():
    return f'''m1 = $game_variables[{V_MIRROR_1}].to_i % 3
m2 = $game_variables[{V_MIRROR_2}].to_i % 3
s1 = (m1 == 0 ? "Lane A (hard crust)" : (m1 == 1 ? "Lane B (hard crust)" : "Canyon wall (A & B soft)"))
s2 = (m2 == 0 ? "Lane D (hard crust)" : (m2 == 1 ? "Canyon wall (C & D soft)" : "Lane C (hard crust)"))
cmds = [_INTL("Check sun-mirrors"), _INTL("Reset sun-mirrors"), _INTL("Ask for a hint")]
can_skip = ($game_switches[301] == true)
cmds.push(_INTL("Skip puzzle (puzzleskip)")) if can_skip
cmds.push(_INTL("Leave it"))
c = pbMessage(_INTL("Aide Nadim: Sun hardens, shade sinks! Need a hand reading the lanes?"), cmds, cmds.length)
if c == 0
  pbMessage(_INTL("Mirror 1 (West Terrace): {{1}}.\\nMirror 2 (East Terrace): {{2}}.", s1, s2))
elsif c == 1
  if pbConfirmMessage(_INTL("Swing both sun-mirrors back to start (Lane A and Lane D lit)?"))
    {_reset_dig_ruby(False).replace(chr(10), chr(10) + "    ")}
  end
elsif c == 2
  h = (pfm_get(:g5_hint).to_i rescue 0)
  if h == 0
    pbMessage(_INTL("Nadim (Hint 1): Sahar says the dig taught her more than the dunes ever did. Every soft sand lane drops you into a sealed gallery below — with its own ladder back up!"))
  elsif h == 1
    pbMessage(_INTL("Nadim (Hint 2): Lane C's mirror is over on the east terrace. Walk west across Lane A, then step into soft Lane C on purpose and see where the tunnel beneath it leads!"))
  else
    pbMessage(_INTL("Nadim (Full Solution): 1) Walk west across lit Lane A to the West Terrace. 2) Step into soft Lane C to drop into the Under-Dig tunnel, follow it east, and climb Ladder Hc up to the East Terrace. 3) Rotate Mirror 2 TWICE (D -> Wall -> C) so Lane C hardens! 4) Step into soft Lane B to drop and climb back to this plaza. 5) Walk Lane A -> Lane C -> Warden Sahar's stairs!"))
  end
  (pfm_set(:g5_hint, [h + 1, 2].min) rescue nil)
elsif can_skip && c == 3
  pbSEPlay("Mining reveal", 90, 100)
  $game_variables[{V_MIRROR_1}] = 0
  $game_variables[{V_MIRROR_2}] = 2
  $game_map.need_refresh = true
  pbMessage(_INTL("Nadim signals the mirror crew! Both Lane A and Lane C are now baked solid — walk straight west and north to Warden Sahar!"))
end'''


def build_211():
    W, H = 29, 25
    m = _new_dig_cave(W, H, seed=211)

    # ---- 1. Carve Twin-Footprint Upper Terraces & 4 Sand Lanes (cvE2, 0 Cliff Overlaps!) ----
    # North Terrace T3 (Arena Portal (14,2) & Darius): x=4..17, y=2..4
    m.box(4, 1, 17, 4, FLOOR, '.')
    # East Cistern X (Dead-end Max Ether platform across Lane d): x=21..26, y=2..4
    m.box(21, 1, 26, 4, FLOOR, '.')
    # West Terrace T1 (Mirror M1 (3,12), Ladder Ha (4,14)) + South Apron (Osman): x=2..7, y=10..15 + x=2..5, y=15..22
    m.box(2, 9, 7, 15, FLOOR, '.')
    m.box(2, 15, 5, 22, FLOOR, '.')
    # East Terrace T2 (Mirror M2 (25,12), Ladders Hc (22,12) & Hd (26,14)) + South Apron: x=21..26, y=10..15 + x=23..26, y=15..22
    m.box(21, 9, 26, 15, FLOOR, '.')
    m.box(23, 15, 26, 22, FLOOR, '.')
    # South Terrace T0 (Cellar Arrival (14,21), Ladder (14,22), Nadim (17,22)): x=10..18, y=19..23
    m.box(10, 18, 18, 23, FLOOR, '.')
    # Four Sun-Mirror Sand Lane Corridors:
    m.box(4, 4, 7, 10, FLOOR, '.')      # Lane c corridor (x=4..7, y=5..8)
    m.box(21, 4, 24, 10, FLOOR, '.')    # Lane d corridor (x=21..24, y=5..8)
    m.box(5, 18, 10, 21, FLOOR, '.')    # Lane a corridor (x=6..9, y=19..21)
    m.box(18, 18, 23, 21, FLOOR, '.')   # Lane b corridor (x=19..22, y=19..21)

    m.tidy()
    m.plan_cliffs(rows=2)

    # Assert EVERY tile of all 4 sand lanes is clean walkable floor (not cliff!)
    for lx, ly in ALL_LANES:
        assert m.cls[ly, lx] == '.' and not m.cliff[ly, lx], f'211 sand lane tile {(lx, ly)} blocked by cliff!'

    # ---- 2. Events: Warps, 4 Dynamic Sand Lanes, Mirrors M1/M2, Nadim, Trainers, Pickups ----
    E = m.events

    # Cellar Ladder (14, 22) -> down to 212 Cellar (14, 23) down
    E.append({
        'type': 'warp',
        'name': 'Cellar Ladder down to 212',
        'at': [14, 22],
        'to': {'map': 212, 'x': 14, 'y': 23, 'dir': 'down'},
        'se': 'Door exit',
    })

    # North Arena Portal (14, 2) -> 213 Warden Arena (10, 15) up
    E.append({
        'type': 'warp',
        'name': 'To Warden Arena (213)',
        'at': [14, 2],
        'to': {'map': 213, 'x': 10, 'y': 15, 'dir': 'up'},
        'se': 'Door enter',
    })

    # Dynamic Sand Lane Tile Events (56 tiles across a, b, c, d!)
    for x, y in LANE_A:
        E.append(_lane_tile_event('a', x, y))
    for x, y in LANE_B:
        E.append(_lane_tile_event('b', x, y))
    for x, y in LANE_C:
        E.append(_lane_tile_event('c', x, y))
    for x, y in LANE_D:
        E.append(_lane_tile_event('d', x, y))

    # Sun-Mirror M1 on West Terrace T1 (3, 12) -> cycles V325: 0=Lane A, 1=Lane B, 2=Wall
    m1_ruby = _mirror_ruby('Sun-Mirror M1', V_MIRROR_1, [
        (0, 'Lane A (southwest)', 'Sunlight floods Lane A! Its sand bakes into firm golden crust — Lane B goes soft in the shade.'),
        (1, 'Lane B (southeast)', 'Sunlight pivots east across Lane B! Lane B hardens into crust while Lane A sinks back into shade.'),
        (2, 'the bare canyon wall', 'The mirror tilts into the sandstone wall — both Lane A and Lane B fall into shade and turn soft!'),
    ])
    E.append({
        'type': 'event',
        'name': 'Sun-Mirror M1',
        'at': [3, 12],
        'pages': [
            {'graphic': {'tile': T_DIAL}, 'trigger': 'action', 'commands': [{'script': m1_ruby}]},
        ],
    })

    # Sun-Mirror M2 on East Terrace T2 (25, 12) -> cycles V326: 0=Lane D (start), 1=Wall, 2=Lane C
    m2_ruby = _mirror_ruby('Sun-Mirror M2', V_MIRROR_2, [
        (0, 'Lane D (northeast cistern)', 'Sunlight pours down Lane D! The path to the northeast cistern bakes solid — Lane C turns soft in the shade.'),
        (1, 'the bare canyon wall', 'The mirror swings against the sandstone cliff — both Lane C and Lane D fall into shade and turn soft!'),
        (2, 'Lane C (northwest arena approach)', 'A blinding sunbeam locks onto Lane C! Its sand hardens into bright golden crust all the way to the north terrace!'),
    ])
    E.append({
        'type': 'event',
        'name': 'Sun-Mirror M2',
        'at': [25, 12],
        'pages': [
            {'graphic': {'tile': T_DIAL}, 'trigger': 'action', 'commands': [{'script': m2_ruby}]},
        ],
    })

    # Mirror Aim Status Beacon Lamps beside M1 & M2 (solid pas=0xf indicators showing lit state!)
    E.append({
        'type': 'event', 'name': 'Beam M1 Indicator', 'at': [2, 12],
        'pages': [
            {'graphic': {'tile': T_LAMP_ON}, 'trigger': 'action', 'commands': ["Mirror 1's bronze beacon burns gold — Lane A is sun-hardened."]},
            {'cond': {'var': [V_MIRROR_1, 1]}, 'graphic': {'tile': T_LAMP_ON}, 'trigger': 'action', 'commands': ["Mirror 1's bronze beacon burns gold — Lane B is sun-hardened."]},
            {'cond': {'var': [V_MIRROR_1, 2]}, 'graphic': {'tile': T_LAMP_OFF}, 'trigger': 'action', 'commands': ["Mirror 1 is angled at bare canyon rock — both lower lanes are shaded and soft."]},
        ],
    })
    E.append({
        'type': 'event', 'name': 'Beam M2 Indicator', 'at': [26, 12],
        'pages': [
            {'graphic': {'tile': T_LAMP_ON}, 'trigger': 'action', 'commands': ["Mirror 2's bronze beacon burns gold — Lane D (northeast cistern) is sun-hardened."]},
            {'cond': {'var': [V_MIRROR_2, 1]}, 'graphic': {'tile': T_LAMP_OFF}, 'trigger': 'action', 'commands': ["Mirror 2 is angled at bare canyon rock — both upper lanes (C and D) are shaded and soft!"]},
            {'cond': {'var': [V_MIRROR_2, 2]}, 'graphic': {'tile': T_LAMP_ON}, 'trigger': 'action', 'commands': ["Mirror 2's bronze beacon burns gold — Lane C (arena terrace) is sun-hardened!"]},
        ],
    })

    # Apprentice Nadim on T0 (17, 22)
    E.append({
        'type': 'event',
        'name': 'Apprentice Nadim',
        'at': [17, 22],
        'pages': [{
            'graphic': {'sprite': 'NPC 13', 'dir': 'left'},
            'trigger': 'action',
            'move': 'fixed',
            'commands': [{'script': _nadim_ruby()}],
        }],
    })

    # Canonical PBS Trainers for Map 211 (pbs/trainers.txt:12787 & 12836 — 0 duplicates!)
    # [HIKER, Osman] on T1 south apron (3, 19) facing right, sight 2 -> (4,19), (5,19) 100% open!
    E.append(_trainer(
        (3, 19), 'HIKER', 'Osman', 'right',
        "Hiker Osman: Made it over Lane A without losing a boot? Let's see how you stand when the earth shakes!",
        "Hiker Osman: Buried to the knees. Carry on over me.",
        sight=2,
    ))
    # [RUINMANIAC, Darius] on North Terrace T3 (11, 3) facing left, sight 3 -> (10,3), (9,3), (8,3) 100% open!
    E.append(_trainer(
        (11, 3), 'RUINMANIAC', 'Darius', 'left',
        "Ruin Maniac Darius: You hardened Lane C from across the entire canyon! Only one digger stands between you and Warden Sahar!",
        "Ruin Maniac Darius: Dig where the Warden says. I dug in the wrong place.",
        sight=3,
    ))

    # Plaques (on solid pf_signpost bases!) & Cistern X Max Ether Pickup
    E += [
        _sign('Dunes Schematic Sign', (11, 22),
              "THE DUNES — SUN-MIRROR MAP: Mirror 1 (West Terrace) aims Lane A or Lane B. Mirror 2 (East Terrace) aims Lane D or Lane C. Bright golden crust holds firm; dark shaded sand drops you into the sealed Under-Dig gallery directly beneath it!"),
        {'type': 'item', 'at': [25, 3], 'item': 'MAXETHER', 'name': 'Cistern Max Ether'},
    ]

    # Protect ladders, landing squares, mirror approaches, lanes, sightlines & warps
    for pt in [(14, 22), (14, 21), (14, 2), (14, 3), (4, 14), (5, 14), (22, 12), (23, 12), (26, 14), (25, 14),
               (17, 20), (18, 20), (4, 19), (5, 19), (10, 3), (9, 3), (8, 3)]:
        m.keep_clear.add(pt)
    for lx, ly in ALL_LANES:
        m.keep_clear.add((lx, ly))
    for e in E:
        ex, ey = e['at']
        m.keep_clear.add((ex, ey))

    # ---- 3. Desert Dig Architecture: Mirror Frames, Arena Portal, Solid Signpost, Bollards, Braziers ----
    _place_stamp_over(m, 'pf_signpost', 11, 21, base_z=1, top_z=2, top_rows=1, solid=True)
    # Tall bronze mirror frames directly behind M1 (3, 10..11) and M2 (25, 10..11)!
    _place_stamp_over(m, 'mn_mirror', 3, 10, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'mn_mirror', 25, 10, base_z=1, top_z=2, top_rows=1, solid=True)
    # North Arena Portal Frame + Symmetrical Ossarian Sun Banners & Columns (0 overlap with cv_frame posts!)
    _place_stamp_over(m, 'cv_frame', 13, 1, base_z=1, top_z=2, top_rows=1, solid=False)
    m.over.append((1, 14, 2, T_PDOOR_OPEN))
    _place_stamp_over(m, 'lm_banner_w', 12, 1, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'lm_banner_w', 16, 1, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'nr_col', 11, 1, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'nr_col', 17, 1, base_z=1, top_z=2, top_rows=1, solid=True)

    # Lane Entrance Bollards & Excavation Props (100% off all lanes and ladder landings!)
    for bx, by in ((2, 15), (26, 22), (2, 22)):
        _place_stamp_over(m, 'lm_bollard', bx, by, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'wr_sacks', 16, 23, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'wr_sandbags', 12, 19, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'wr_sandbags', 16, 19, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'nr_col', 22, 2, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'wr_tripod', 2, 16, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'wr_sacks', 26, 17, base_z=1, top_z=1, top_rows=0, solid=True)

    braziers_211 = [(10, 22), (18, 22), (6, 10), (22, 10), (6, 2), (26, 2)]
    for bx, by in braziers_211:
        if (bx, by) not in m.keep_clear and m.cls[by, bx] == '.' and not m.cliff[by, bx]:
            _place_stamp_over(m, 'fw_brazier', bx, by, base_z=1, top_z=2, top_rows=1, solid=True)
    braziers_placed_211 = [(bx, by) for bx, by in braziers_211 if (bx, by) not in m.keep_clear and m.cls[by, bx] == '.' and not m.cliff[by, bx]]

    m.paint()
    _paint_desert_floors(m, [
        (0, 0, W - 1, H - 1, 'sand'),
        (11, 19, 17, 23, 'plaza'),
        (2, 11, 6, 14, 'mosaic'),
        (22, 11, 26, 14, 'mosaic'),
        (12, 2, 16, 4, 'plaza'),
        (23, 2, 26, 4, 'mosaic'),
    ])
    # Visual ladder shaft openings matching 212's ladders below!
    for lx, ly in ((14, 22), (4, 14), (18, 20), (22, 12), (26, 14)):
        m.L[1, ly, lx] = T_HOLE

    Lr = RC.resolve(m.L, TID).astype(np.int32)
    _add_safe_overlay(Lr, TID, 'cv_shaft', [(13, 19), (3, 10), (24, 10), (13, 2), (24, 2)])
    _add_safe_overlay(Lr, TID, 'pf_glow', braziers_placed_211 + [(3, 12), (24, 12)])
    _assert_braziers_intact(Lr, braziers_placed_211, 'Map 211')

    ev_pts = [tuple(e['at']) for e in E]
    PG.guard(Lr, TID, ev_pts, 'Map 211')
    assert not PG.hits(Lr, R.tilesets()[TID], ev_pts), 'Map 211 passguard hits!'
    _verify_no_over_trigger_and_sightlines(Lr, E, 'Map 211')

    m.L = Lr
    head = {
        'id': 211,
        'name': 'Duneholt Gym - Puzzle Room 1',
        'parent': 210,
        'bgm': 'Gym',
        'field': FIELD,
        'map_audio': {'bgm': 'Gym - Warden Hall', 'bgs': 'Wind - Isenmar', 'bgs_volume': 35, 'rain': False},
        'metadata': {'Name': 'Duneholt Gym', 'SnapEdges': True, 'MapPosition': DUN_POS, 'BattleBack': 'desert'},
        'tone': [22, 10, -14, 4],
        '_file': '211_duneholt_gym_211.yaml',
    }
    m.write(211, head, comment='# GENERATED by mapgen/layouts/duneholt_gym.py (Batch 3D): Duneholt Gym - Puzzle Room 1 (The Dunes).\n'
                               '# Edit the layout script, not this file.\n')
    return m, Lr


# =================================================================================================
# 3. MAP 212 — DUNEHOLT GYM - PUZZLE ROOM 2 ("The Under-Dig — COMBINE + Mastery", 29x25, TS 57, :DESERT)
# =================================================================================================
def _tablet_ruby(slot_lbl, var_id):
    return f'''v = ($game_variables[{var_id}].to_i + 1) % 4
$game_variables[{var_id}] = v
pbSEPlay("Strength push", 85, 100)
nm = ["SUN", "EYE", "WAVE", "BONE"][v]
pbMessage(_INTL("Tablet {slot_lbl} pivots with a sandstone grind — showing the carved glyph: {{1}}.", nm))'''


def _mural_check_ruby():
    # Canonical targets from GYM_PUZZLES.md:873 -> Ua: Wave (2), Ub: Sun (0), Uc: Bone (3), Ud: Eye (1)
    return f'''if $game_switches[{S_MURAL_DONE}]
  pbMessage(_INTL("Sahar's sealed Elector Mural stands open. Scratched along the frame: 'SEALED AF 281 — BY ORDER OF SOVEREIGN VALEN.'"))
else
  a = $game_variables[{V_TAB_A}].to_i % 4
  b = $game_variables[{V_TAB_B}].to_i % 4
  c = $game_variables[{V_TAB_C}].to_i % 4
  d = $game_variables[{V_TAB_D}].to_i % 4
  nms = ["SUN", "EYE", "WAVE", "BONE"]
  if a == 2 && b == 0 && c == 3 && d == 1
    pbSEPlay("Mining reveal", 95, 100)
    pfm_shake(2, 8, 12)
    $game_switches[{S_MURAL_DONE}] = true
    pbMessage(_INTL("CLICK! All four Elector tablets lock flush — a hidden sandstone niche slides open behind the mural!"))
    pbMessage(_INTL("Inside lies a sealed wax rubbing note: 'THE CHAIN OF EIGHTEEN — SEALED AF 281 ON VALEN'S ORDER. — S.O.'"))
    pbReceiveItem(:TELLURICSEED, 2)
    pbReceiveItem(:SOFTSAND, 1)
  else
    pbSEPlay("GUI sel buzzer", 80, 100)
    pbMessage(_INTL("'Each road remembers what lies beneath it.'\\nCurrent glyphs — A: {{1}} · B: {{2}} · C: {{3}} · D: {{4}}.", nms[a], nms[b], nms[c], nms[d]))
    if a != 2
      pbMessage(_INTL("The A-tablet grinds and stops. {{1}} doesn't sit beneath Lane A.", nms[a]))
    elsif b != 0
      pbMessage(_INTL("The B-tablet grinds and stops. {{1}} doesn't sit beneath Lane B.", nms[b]))
    elsif c != 3
      pbMessage(_INTL("The C-tablet grinds and stops. {{1}} doesn't sit beneath Lane C.", nms[c]))
    else
      pbMessage(_INTL("The D-tablet grinds and stops. {{1}} doesn't sit beneath Lane D.", nms[d]))
    end
  end
end'''


def build_212():
    W, H = 29, 25
    m = _new_dig_cave(W, H, seed=212)

    # ---- 1. Carve FIVE Airtight Sealed Subterranean Galleries Matching 211's Twin Footprint ----
    # Gallery 1: Cellar (receives 210 drop at (14,23), ladder (14,22) -> 211 T0, rope (12,22) -> 210): x=12..15, y=21..23
    m.box(12, 20, 15, 23, FLOOR, '.')
    # Gallery 2: Ua (under Lane a x=6..9, y=19..21 -> Ladder Ha (4,14) -> 211 T1): x=4..9, y=19..22 + x=3..6, y=14..20
    m.box(4, 18, 9, 22, FLOOR, '.')
    m.box(3, 13, 6, 20, FLOOR, '.')
    # Gallery 3: Ub (under Lane b x=19..22, y=19..21 -> Ladder Hb (18,20) -> 211 T0): x=18..23, y=18..22
    m.box(18, 17, 23, 22, FLOOR, '.')
    # Gallery 4: Uc (under Lane c x=4..7, y=5..8 -> Long Dig Tunnel -> Ladder Hc (22,12) -> 211 T2):
    m.box(4, 3, 7, 8, FLOOR, '.')
    m.box(7, 6, 17, 10, FLOOR, '.')
    m.box(16, 10, 23, 13, FLOOR, '.')
    # Gallery 5: Ud (under Lane d x=21..24, y=5..8 + NE Mastery Mural Alcove -> East Shaft -> Ladder Hd (26,14) -> 211 T2):
    m.box(21, 1, 27, 8, FLOOR, '.')
    m.box(26, 7, 27, 15, FLOOR, '.')

    m.tidy()
    m.plan_cliffs(rows=2)

    # Assert EVERY single tile of Lanes a, b, c, d lands on 100% open walkable floor in 212!
    for lx, ly in ALL_LANES:
        assert m.cls[ly, lx] == '.' and not m.cliff[ly, lx], f'212 drop landing {(lx, ly)} blocked by cliff!'

    # ---- 2. Events: 5 Up-Ladders + 210 Return Rope, 4 Elector Glyphs, Mastery Mural Shrine, Trainers, Reset NPC ----
    E = m.events

    # Cellar Ladder up -> 211 T0 (14, 21) facing up (1 tile north of 211's down-ladder (14, 22)!)
    E.append({
        'type': 'warp',
        'name': 'Cellar Ladder up to Dunes (211)',
        'at': [14, 22],
        'to': {'map': 211, 'x': 14, 'y': 21, 'dir': 'up'},
        'se': 'Door enter',
    })
    # Cellar Exit Rope back -> 210 Entrance (10, 13) facing down!
    E.append({
        'type': 'warp',
        'name': 'Return Rope to Entrance (210)',
        'at': [12, 22],
        'to': {'map': 210, 'x': 10, 'y': 13, 'dir': 'down'},
        'se': 'Door exit',
    })
    # Ladder Ha (Ua) -> 211 T1 (5, 14) facing right
    E.append({
        'type': 'warp',
        'name': 'Ladder Ha up to West Terrace',
        'at': [4, 14],
        'to': {'map': 211, 'x': 5, 'y': 14, 'dir': 'right'},
        'se': 'Door enter',
    })
    # Ladder Hb (Ub) -> 211 T0 (17, 20) facing left
    E.append({
        'type': 'warp',
        'name': 'Ladder Hb up to South Plaza',
        'at': [18, 20],
        'to': {'map': 211, 'x': 17, 'y': 20, 'dir': 'left'},
        'se': 'Door enter',
    })
    # Ladder Hc (Uc) -> 211 T2 (23, 12) facing right
    E.append({
        'type': 'warp',
        'name': 'Ladder Hc up to East Terrace',
        'at': [22, 12],
        'to': {'map': 211, 'x': 23, 'y': 12, 'dir': 'right'},
        'se': 'Door enter',
    })
    # Ladder Hd (Ud) -> 211 T2 (25, 14) facing up
    E.append({
        'type': 'warp',
        'name': 'Ladder Hd up to East Terrace',
        'at': [26, 14],
        'to': {'map': 211, 'x': 25, 'y': 14, 'dir': 'up'},
        'se': 'Door enter',
    })

    # Four Carved Elector Glyph Clues over each gallery's ladder (on solid cliff walls, pas=0xf -> 0 over_trigger?!)
    E += [
        _sign('Elector Glyph A (Wave)', (3, 13),
              "CARVED ELECTOR GLYPH ABOVE LADDER A: WAVE — 'Worn smooth by water that has not run beneath Duneholt in three hundred years.'"),
        _sign('Elector Glyph B (Sun)', (18, 17),
              "CARVED ELECTOR GLYPH ABOVE LADDER B: SUN — 'A sharp noon disk cut deep into the sandstone lintel.'"),
        _sign('Elector Glyph C (Bone)', (22, 10),
              "CARVED ELECTOR GLYPH ABOVE LADDER C: BONE — 'Ribs crossed over an ancient Elector's seal.'"),
        _sign('Elector Glyph D (Eye)', (26, 1),
              "CARVED ELECTOR GLYPH ABOVE LADDER D: EYE — 'An unblinking stone eye watching the buried cistern.'"),
    ]

    # Optional Gym 5 Mastery Puzzle in Ud (x=21..25, y=2): 4 Pivoting Sandstone Tablet Cradles + Carved Rune Mural Stele (ALL solid pas=0xf!)
    for lbl, tx, vid in (('A', 21, V_TAB_A), ('B', 22, V_TAB_B), ('C', 23, V_TAB_C), ('D', 24, V_TAB_D)):
        E.append({
            'type': 'event',
            'name': f'Elector Tablet {lbl}',
            'at': [tx, 2],
            'pages': [{'trigger': 'action', 'commands': [{'script': _tablet_ruby(lbl, vid)}]}],
        })
    E.append({
        'type': 'event',
        'name': 'Sealed Elector Mural',
        'at': [25, 2],
        'pages': [{'trigger': 'action', 'commands': [{'script': _mural_check_ruby()}]}],
    })

    # Zero-Softlock Under-Dig Reset Apprentice Samim in Uc (17, 12) (100% off drop tiles!)
    samim_ruby = (
        'c = pbMessage(_INTL("Digger Samim: Dropped straight through Lane C, huh? Climb Ladder Hc just ahead to pop up on the East Terrace! Or want me to reset both sun-mirrors and hoist you back to the South Plaza?"),\n'
        '              [_INTL("Reset mirrors & return to South Plaza"), _INTL("Keep digging")], 2)\n'
        'if c == 0\n'
        f'  {_reset_dig_ruby(True).replace(chr(10), chr(10) + "  ")}\n'
        'end'
    )
    E.append({
        'type': 'event',
        'name': 'Digger Samim',
        'at': [17, 12],
        'pages': [{
            'graphic': {'sprite': 'NPC 17', 'dir': 'right'},
            'trigger': 'action',
            'move': 'fixed',
            'commands': [{'script': samim_ruby}],
        }],
    })

    # Canonical PBS Trainers for Map 212 (pbs/trainers.txt:12885 & 12934 — 0 duplicates, ZERO overlap with drop tiles!)
    # [RUINMANIAC, Farah] in Uc long dig tunnel at (13, 8) facing left, sight 3 -> (12,8),(11,8),(10,8) open!
    E.append(_trainer(
        (13, 8), 'RUINMANIAC', 'Farah', 'left',
        "Ruin Maniac Farah: Welcome to the Elector-era necropolis under the Gym! Every layer down here is older than the last — let's dig in!",
        "Ruin Maniac Farah: Every layer's older than the last. I feel ancient.",
        sight=3,
    ))
    # [HIKER, Burak] in Ub along south wall at (23, 22) facing left, sight 3 -> (22,22),(21,22),(20,22) open & clear of Lane b y=19..21!
    E.append(_trainer(
        (23, 22), 'HIKER', 'Burak', 'left',
        "Hiker Burak: Fell straight through Lane B? Good landing — now hold your footing against my team before climbing up to the plaza!",
        "Hiker Burak: Sahar reads sand like a book. You're the next chapter.",
        sight=3,
    ))

    # Optional Ua Pickup (clear of Lane a x=6..9, y=19..21!)
    E.append({'type': 'item', 'at': [5, 22], 'item': 'HYPERPOTION', 'name': 'Under-Dig Hyper Potion'})

    # Protect ALL 56 drop landing tiles + ladders + trainers + sightlines
    for lx, ly in ALL_LANES:
        m.keep_clear.add((lx, ly))
    for pt in [(14, 23), (14, 22), (12, 22), (4, 14), (18, 20), (22, 12), (26, 14),
               (12, 8), (11, 8), (10, 8), (22, 22), (21, 22), (20, 22)]:
        m.keep_clear.add(pt)
    for e in E:
        ex, ey = e['at']
        m.keep_clear.add((ex, ey))

    # ---- 3. Subterranean Elector-Era Necropolis Props, Carved Glyph Wall Steles & Ud Mastery Shrine! ----
    # Clear carved stone stele markers mounted onto the cliff walls at ALL 4 Elector Glyph clues (L[2], pas=0xf -> intact cliff behind, 0 over_trigger?!)
    for gx, gy in ((3, 13), (18, 17), (22, 10), (26, 1)):
        _place_stamp_over(m, 'pf_roadstone', gx, gy - 1, base_z=2, top_z=2, top_rows=2, solid=True)

    # Ud Mastery Shrine: 4 sleek gold-trimmed stone tablet cradles (lm_cradle_cold, y=1..2 -> pas=0xf base at y=2!) + carved glyph mural stele (hb_banner at (25, 0..2) -> pas=0xf base at (25,2)!)
    for tx in (21, 22, 23, 24):
        _place_stamp_over(m, 'lm_cradle_cold', tx, 1, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'hb_banner', 25, 0, base_z=1, top_z=2, top_rows=2, solid=True)

    braziers_212 = [(15, 21), (3, 17), (23, 18), (9, 7), (19, 11), (27, 4)]
    for bx, by in braziers_212:
        _place_stamp_over(m, 'fw_brazier', bx, by, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'wr_sacks', 15, 23, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'nr_col', 16, 7, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'nr_col', 27, 2, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'wr_ban_bone', 20, 11, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'wr_sacks', 4, 22, base_z=1, top_z=1, top_rows=0, solid=True)

    m.paint()
    _paint_desert_floors(m, [
        (0, 0, W - 1, H - 1, 'sand'),
        (12, 21, 15, 23, 'plaza'),
        (21, 2, 27, 4, 'mosaic'),
        (17, 11, 23, 13, 'plaza'),
    ])
    # Mark drop-cushion sand zones directly beneath Lanes a, b, c, d with crisp golden-dust ripples (all pas=0x0!)
    rip = [P1('wr_ripple0'), P1('wr_ripple1'), P1('wr_ripple2')]
    for lx, ly in ALL_LANES:
        if int(m.L[1, ly, lx]) == 0:
            m.L[1, ly, lx] = rip[(lx + ly) % 3]
    # Ladders & return rope graphics!
    for lx, ly in ((14, 22), (4, 14), (18, 20), (22, 12), (26, 14)):
        m.L[1, ly, lx] = T_HOLE
    m.L[1, 22, 12] = T_LADDER_Q

    Lr = RC.resolve(m.L, TID).astype(np.int32)
    _add_safe_overlay(Lr, TID, 'cv_shaft', [(5, 5), (22, 5), (7, 19), (20, 19), (13, 21)])
    _add_safe_overlay(Lr, TID, 'pf_glow', braziers_212)
    _assert_braziers_intact(Lr, braziers_212, 'Map 212')

    ev_pts = [tuple(e['at']) for e in E]
    PG.guard(Lr, TID, ev_pts, 'Map 212')
    assert not PG.hits(Lr, R.tilesets()[TID], ev_pts), 'Map 212 passguard hits!'
    _verify_no_over_trigger_and_sightlines(Lr, E, 'Map 212')

    m.L = Lr
    head = {
        'id': 212,
        'name': 'Duneholt Gym - Puzzle Room 2',
        'parent': 210,
        'bgm': 'Gym',
        'field': FIELD,
        'map_audio': {'bgm': 'Gym - Warden Hall', 'bgs': 'Drip - Nadir', 'bgs_volume': 35, 'rain': False},
        'fog': {'name': 'prismfall_cave', 'opacity': 20, 'blend': 1, 'zoom': 100, 'sx': 1, 'sy': 0},
        'metadata': {'Name': 'Duneholt Gym', 'SnapEdges': True, 'MapPosition': DUN_POS, 'BattleBack': 'desert'},
        'tone': [-10, -14, -22, 14],
        # Provide seeds for all 5 sealed Under-Dig galleries so build.py walk_check validates 100% of events cleanly!
        'walk_from': [[14, 23], [6, 20], [20, 20], [6, 6], [23, 6]],
        '_file': '212_duneholt_gym_212.yaml',
    }
    m.write(212, head, comment='# GENERATED by mapgen/layouts/duneholt_gym.py (Batch 3D): Duneholt Gym - Puzzle Room 2 (The Under-Dig).\n'
                               '# Edit the layout script, not this file.\n')
    return m, Lr


# =================================================================================================
# 4. MAP 213 — DUNEHOLT GYM - WARDEN ARENA (Sahar Ostrand, 21x17, TS 57, :DESERT)
# =================================================================================================
def build_213():
    W, H = 21, 17
    m = _new_dig_cave(W, H, seed=213)

    # ---- 1. Sculpt Dramatic Sunlit Subterranean Sandstone Pit & Elevated North Warden Dais ----
    # Elevated North Warden Dais (TER): x=6..14, y=2..6 (walkable y=3..6, stair descends y=6..7 -> lands y=8!)
    m.box(6, 2, 14, 6, TER, '.')
    # Main Sunlit Arena Pit (FLOOR): x=3..17, y=7..14
    m.box(3, 7, 17, 14, FLOOR, '.')
    # Recessed South Approach Vestibule: x=8..12, y=14..16 (arrival (10,15) up, return warps (9..11,16)!)
    m.box(8, 14, 12, 16, FLOOR, '.')
    # Chamfered pit corners
    m.mass_at([(3, 7), (17, 7), (3, 14), (17, 14), (6, 2), (14, 2)])
    # 3-wide Sandstone Staircase descending from Sahar's Dais (x=9..11, y=6..7)
    m.stairs(9, 6, w=3, n=2, c='.')

    m.tidy()
    m.plan_cliffs(rows=2)

    # ---- 2. Events: Return Warp -> 211, Framed Fast-Exit Lift -> 210, Warden Sahar Ostrand! ----
    E = m.events

    for rx in (9, 10, 11):
        E.append({
            'type': 'warp',
            'name': 'Back to The Dunes (211)',
            'at': [rx, 16],
            'to': {'map': 211, 'x': 14, 'y': 3, 'dir': 'down'},
            'se': 'Door exit',
        })

    # Framed Fast-Exit Excavation Lift (16, 13) -> straight back to 210 Entrance (10, 14) down!
    E.append({
        'type': 'warp',
        'name': 'Fast-Exit Lift to Entrance (210)',
        'at': [16, 13],
        'to': {'map': 210, 'x': 10, 'y': 14, 'dir': 'down'},
        'se': 'Door slide',
    })
    # Lift Sign mounted on solid pf_signpost at (15, 11..12) -> 100% readable from walkable NON-WARP tile (15, 13)!
    E.append(_sign(
        'Excavation Lift Sign', (15, 12),
        "EXCAVATION FAST-EXIT LIFT — Step onto the bolted lift deck to the right to ride straight back to the Gym Entrance!"
    ))

    # WARDEN SAHAR OSTRAND (story/25_SCRIPT_CH6.md lines 332-363 + GYM_PUZZLES.md:869, 879!)
    sahar_battle_ruby = f'''ds = (pf_choice(:ch6_drillsite) rescue nil)
if ds == :sanctuary
  pbMessage(_INTL("Sahar: You shouted my name across the well. Nobody's shouted my name since I was a girl."))
  pbMessage(_INTL("Sahar: It was very loud. Thank you."))
elsif ds == :hollow
  pbMessage(_INTL("Sahar: You let the Hollow take Meridian's diggers into my dunes. I've been told to be angry about it. I'm working on it."))
elsif ds == :directorate
  pbMessage(_INTL("Sahar: You helped them put the collars back on. I saw. I'm not going to say anything about it. The sand will."))
end
pbMessage(_INTL("Sahar: The desert keeps everything. It just doesn't keep it where you left it."))
pbMessage(_INTL("Sahar: Patience is a Ground-type's whole art. I'm fifty-eight and I have a cough. Let's see who runs out first."))
if Prismfall.gym_battle(pfm_gym(:LEADER_SAHAR), double: false)
  pbMessage(_INTL("Sahar: ...Well. You found the bottom. Most people stop one layer short."))
  Prismfall.award_badge(pfm_gym(:LEADER_SAHAR))
  pbSEPlay("Anim/HealBell", 90, 100)
  pbMessage(_INTL("Five clear notes ring out from your badge case, one after another and then together. The light along its seams is steadier now."))
  pbMessage(_INTL("Sahar: It sings. ...Of course it does. Everything you carry is strange, isn't it."))
  pbReceiveItem(:TM83)
  pbMessage(_INTL("Sahar: TM83 Bulldoze. Shake the ground, slow whatever's standing on it. And my excavators upstairs will hand you HM04 Strength — they've been waiting for an excuse."))
  if $game_switches[{S_MURAL_DONE}]
    pbMessage(_INTL("Sahar: ...And I heard the lock grind in the east gallery. I buried that mural once. The sand dug it up. I'd rather not argue with sand twice."))
  end
  $game_variables[126] = 5 if $game_variables[126].to_i < 5
  $game_self_switches[[213, @event_id, "A"]] = true
  $game_map.need_refresh = true
end'''
    sahar_after_ruby = f'''if $game_switches[{S_MURAL_DONE}]
  pbMessage(_INTL("Sahar: I buried that mural in the Under-Dig. The sand dug it up. I'd rather not argue with sand twice."))
end
pbMessage(_INTL("Sahar: You earned the Sandglass Badge honestly. Stop by my excavators in the entrance lobby for HM04 Strength, then meet me out on the Marrow Road — the dunes shifted last night."))'''

    E.append({
        'type': 'event',
        'name': 'Warden Sahar',
        'at': [10, 4],
        'pages': [
            {
                'graphic': {'sprite': 'SAHAR', 'dir': 'down'},
                'trigger': 'action',
                'move': 'fixed',
                'commands': [{'script': sahar_battle_ruby}],
            },
            {
                'cond': {'self': 'A'},
                'graphic': {'sprite': 'SAHAR', 'dir': 'down'},
                'trigger': 'action',
                'move': 'fixed',
                'commands': [{'script': sahar_after_ruby}],
            },
        ],
    })

    # Protect center runway, stairs, lift bay, arrival & return warps
    for y in range(4, 17):
        for x in (9, 10, 11):
            m.keep_clear.add((x, y))
    for pt in ((15, 13), (16, 13), (15, 12), (16, 12), (14, 13)):
        m.keep_clear.add(pt)

    # ---- 3. Sunlit Excavation Pit Architecture, Labelled Fossil Alcoves, Framed Lift & Burning Braziers! ----
    # North Dais framing: Ossarian bone standards (y=2..4), royal sunburst banners & sandstone bollards!
    _place_stamp_over(m, 'wr_ban_bone', 7, 2, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'wr_ban_bone', 13, 2, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'lm_banner_w', 8, 2, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'lm_banner_w', 12, 2, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'lm_bollard', 7, 5, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'lm_bollard', 13, 5, base_z=1, top_z=1, top_rows=0, solid=True)

    # Framed Fast-Exit Lift Bay: solid lm_sdoor (16, 11..12) + pf_signpost (15, 11..12 -> solid base 18112 at (15,12)!) + east bollard!
    _place_stamp_over(m, 'lm_sdoor', 16, 11, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'lm_bollard', 17, 12, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'pf_signpost', 15, 11, base_z=1, top_z=2, top_rows=1, solid=True)

    # Arena Pit Columns, Excavation Relics & 6 Intact Burning Braziers (all bases grounded 100% on floor, lift aisle 100% open!)
    for cx, cy in ((5, 9), (15, 9), (5, 11), (14, 11)):
        _place_stamp_over(m, 'nr_col', cx, cy, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'wr_sacks', 4, 11, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'wr_sandbags', 4, 13, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'wr_tripod', 16, 8, base_z=1, top_z=2, top_rows=1, solid=True)

    braziers_213 = [(6, 4), (14, 4), (6, 8), (14, 8), (7, 13), (13, 13)]
    for bx, by in braziers_213:
        _place_stamp_over(m, 'fw_brazier', bx, by, base_z=1, top_z=2, top_rows=1, solid=True)

    m.paint()
    _paint_desert_floors(m, [
        (3, 8, 17, 14, 'sand'),
        (6, 3, 14, 6, 'plaza'),
        (7, 8, 13, 14, 'mosaic'),
        (8, 14, 12, 16, 'plaza'),
        (15, 13, 17, 13, 'plaza'),
    ])
    # Center 5x5 golden sundial medallion lm_sun at (8, 9) (x=8..12, y=9..13)!
    _paint_sun_medallion(m, 8, 9)
    # Bolted lift pad at (16, 13) + fossil bones along pit walls
    m.L[1, 13, 16] = T_LATCH_OPEN
    for bx, by, nm in ((4, 9, 'wr_bones0'), (16, 10, 'wr_bones1'), (4, 12, 'wr_bones1'), (7, 11, 'wr_ripple0'), (13, 11, 'wr_ripple1')):
        if int(m.L[1, by, bx]) == 0 and m.cls[by, bx] == '.' and not m.cliff[by, bx]:
            m.L[1, by, bx] = P1(nm)

    Lr = RC.resolve(m.L, TID).astype(np.int32)
    _add_safe_overlay(Lr, TID, 'cv_shaft', [(9, 3), (9, 9), (11, 9)])
    _add_safe_overlay(Lr, TID, 'pf_glow', braziers_213 + [(9, 10)])
    _assert_braziers_intact(Lr, braziers_213, 'Map 213')

    ev_pts = [tuple(e['at']) for e in E]
    PG.guard(Lr, TID, ev_pts, 'Map 213')
    assert not PG.hits(Lr, R.tilesets()[TID], ev_pts), 'Map 213 passguard hits!'
    _verify_no_over_trigger_and_sightlines(Lr, E, 'Map 213')
    seen213 = _sim_bfs(Lr, E, (10, 15), [
        ('Return -> 211', (10, 16), False),
        ('Fast-Exit Lift -> 210', (16, 13), False),
        ('Lift Sign (non-warp adj)', (15, 13), False),
        ('Warden Sahar', (10, 4), True),
    ], 'Map 213 Warden Arena')
    # Strictly prove Excavation Lift Sign (15, 12) has an adjacent passable NON-WARP tile ((15, 13))!
    warp_pts = {tuple(e['at']) for e in E if e.get('type') == 'warp'}
    assert (15, 13) in seen213 and (15, 13) not in warp_pts, 'Map 213: Lift Sign (15,12) not readable from non-warp tile (15,13)!'

    m.L = Lr
    head = {
        'id': 213,
        'name': 'Duneholt Gym - Warden Arena',
        'parent': 210,
        'bgm': 'Gym',
        'field': FIELD,
        'map_audio': {'bgm': 'Gym - Warden Hall', 'bgs': 'Wind - Isenmar', 'bgs_volume': 30, 'rain': False},
        'metadata': {'Name': 'Duneholt Gym', 'SnapEdges': True, 'MapPosition': DUN_POS, 'BattleBack': 'desert'},
        'tone': [24, 12, -12, 4],
        '_file': '213_duneholt_gym_213.yaml',
    }
    m.write(213, head, comment='# GENERATED by mapgen/layouts/duneholt_gym.py (Batch 3D): Duneholt Gym - Warden Arena (Sahar).\n'
                               '# Edit the layout script, not this file.\n')
    return m, Lr


# =================================================================================================
# Exhaustive Cross-Floor Gym 5 State-Space & Anti-Leak / Zero-Softlock Verification!
# =================================================================================================
def verify_gym5_puzzle(m211, L211, m212, L212):
    """Exhaustively prove ALL 211 <-> 212 mechanics, 0 leaks, 0 softlocks, canonical solution & Mastery reachability!"""
    # 1. Verify ALL 56 sand lane landing tiles in 212 are strictly walkable & event-free!
    import build as B
    ts = R.tilesets()[TID]
    ev212_pts = {tuple(e['at']) for e in m212.events}
    for lx, ly in ALL_LANES:
        assert B.cell_passable(L212, ts, lx, ly), f'212 drop tile {(lx, ly)} NOT passable!'
        assert (lx, ly) not in ev212_pts, f'212 drop tile {(lx, ly)} occupied by event!'

    # 2. Verify all 5 Under-Dig galleries on 212 are 100% SEALED from each other!
    g_seeds = {
        'Cellar': ((14, 23), [('Cellar Ladder', (14, 22), False), ('Return Rope 210', (12, 22), False)]),
        'Ua': ((7, 20), [('Ladder Ha', (4, 14), False), ('Glyph A', (3, 13), True), ('Hyper Potion', (5, 22), True)]),
        'Ub': ((20, 20), [('Ladder Hb', (18, 20), False), ('Glyph B', (18, 17), True), ('Trainer Burak', (23, 22), True)]),
        'Uc': ((6, 6), [('Ladder Hc', (22, 12), False), ('Glyph C', (22, 10), True), ('Trainer Farah', (13, 8), True), ('Samim', (17, 12), True)]),
        'Ud': ((23, 6), [('Ladder Hd', (26, 14), False), ('Glyph D', (26, 1), True), ('Tablet A', (21, 2), True), ('Tablet D', (24, 2), True), ('Mural Lock', (25, 2), True)]),
    }
    g_sets = {}
    for gname, (st, tgts) in g_seeds.items():
        g_sets[gname] = _sim_bfs(L212, m212.events, st, tgts, f'Map 212 gallery {gname}')
    names = list(g_sets.keys())
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            ov = g_sets[names[i]] & g_sets[names[j]]
            assert not ov, f'212 SEAL LEAK: {names[i]} overlaps {names[j]} at {list(ov)[:3]}!'
    print('Map 212: All 5 Under-Dig galleries (Cellar, Ua, Ub, Uc, Ud) 100% AIRTIGHT SEALED!')

    # 3. Verify 211 start state (V325=0 [a lit], V326=0 [d lit]):
    #    From T0 (14, 21), can reach T1 (Mirror M1, Osman) via lit Lane a, CANNOT reach T2, T3, or X on foot!
    s_start = _sim_bfs(L211, m211.events, (14, 21), [
        ('Cellar Ladder', (14, 22), False),
        ('Nadim', (17, 22), True),
        ('Dunes Schematic', (11, 22), True),
        ('Mirror M1', (3, 12), True),
        ('Trainer Osman', (3, 19), True),
    ], 'Map 211 (start: a,d lit)', vars_={V_MIRROR_1: 0, V_MIRROR_2: 0}, block_touch_names=('Sand ',))
    assert (14, 2) not in s_start, '211 LEAK: Arena Portal reachable in start state without dropping!'
    assert (25, 12) not in s_start and (24, 12) not in s_start, '211 LEAK: T2/Mirror M2 reachable in start state without dropping!'

    # 4. Verify solved state (V325=0 [a lit], V326=2 [c lit]): T0 -> Lane a -> T1 -> Lane c -> T3 -> Arena Portal (14,2)!
    _sim_bfs(L211, m211.events, (14, 21), [
        ('Trainer Darius', (11, 3), True),
        ('Arena Portal (213)', (14, 2), False),
    ], 'Map 211 (solved: a,c lit)', vars_={V_MIRROR_1: 0, V_MIRROR_2: 2}, block_touch_names=('Sand ',))

    # 5. Verify East Terrace T2 in start state (V326=0 [d lit]): can walk d to Cistern X (Max Ether) & touch Mirror M2!
    _sim_bfs(L211, m211.events, (23, 12), [
        ('Mirror M2', (25, 12), True),
        ('Cistern Max Ether', (25, 3), True),
    ], 'Map 211 (T2: d lit -> X)', vars_={V_MIRROR_1: 0, V_MIRROR_2: 0}, block_touch_names=('Sand ',))

    # 6. Exhaustive State-Graph Solver over ALL (terrace, m1, m2) states!
    #    Terraces: T0, T1, T2, T3, X.
    #    Transitions:
    #      - Walk lit lane: a (m1==0: T0<->T1), b (m1==1: T0<->T2), c (m2==2: T1<->T3), d (m2==0: T2<->X)
    #      - Drop soft lane -> 212 gallery -> climb ladder:
    #          soft a (m1!=0, from T0 or T1) -> Ua -> T1
    #          soft b (m1!=1, from T0 or T2) -> Ub -> T0
    #          soft c (m2!=2, from T1 or T3) -> Uc -> T2
    #          soft d (m2!=0, from T2 or X)  -> Ud -> T2  (also visits Ud Mastery Shrine!)
    #      - Rotate mirror: on T1 -> (T1, (m1+1)%3, m2); on T2 -> (T2, m1, (m2+1)%3)
    def neighbors(state):
        t, m1, m2 = state
        out = []
        # Lit walks
        if m1 == 0 and t in ('T0', 'T1'):
            out.append(('walk_a', ('T1' if t == 'T0' else 'T0', m1, m2)))
        if m1 == 1 and t in ('T0', 'T2'):
            out.append(('walk_b', ('T2' if t == 'T0' else 'T0', m1, m2)))
        if m2 == 2 and t in ('T1', 'T3'):
            out.append(('walk_c', ('T3' if t == 'T1' else 'T1', m1, m2)))
        if m2 == 0 and t in ('T2', 'X'):
            out.append(('walk_d', ('X' if t == 'T2' else 'T2', m1, m2)))
        # Soft drops (via 212 ladders!)
        if m1 != 0 and t in ('T0', 'T1'):
            out.append(('drop_a->T1', ('T1', m1, m2)))
        if m1 != 1 and t in ('T0', 'T2'):
            out.append(('drop_b->T0', ('T0', m1, m2)))
        if m2 != 2 and t in ('T1', 'T3'):
            out.append(('drop_c->T2', ('T2', m1, m2)))
        if m2 != 0 and t in ('T2', 'X'):
            out.append(('drop_d->Ud->T2', ('T2', m1, m2)))
        # Rotations
        if t == 'T1':
            out.append(('rot_M1', ('T1', (m1 + 1) % 3, m2)))
        if t == 'T2':
            out.append(('rot_M2', ('T2', m1, (m2 + 1) % 3)))
        return out

    start_st = ('T0', 0, 0)
    # Prove impossible WITHOUT drops
    q_nodrop = deque([start_st])
    seen_nd = {start_st}
    while q_nodrop:
        s = q_nodrop.popleft()
        for act, ns in neighbors(s):
            if act.startswith('drop_'):
                continue
            if ns not in seen_nd:
                seen_nd.add(ns)
                q_nodrop.append(ns)
    assert not any(t == 'T3' for t, _, _ in seen_nd), 'GYM 5 LEAK: T3 reachable WITHOUT dropping!'

    # Find shortest full solution & collect ALL reachable states
    prev = {start_st: None}
    q = deque([start_st])
    goal_st = None
    ud_visited = False
    while q:
        s = q.popleft()
        if s[0] == 'T3' and goal_st is None:
            goal_st = s
        for act, ns in neighbors(s):
            if act == 'drop_d->Ud->T2':
                ud_visited = True
            if ns not in prev:
                prev[ns] = (s, act)
                q.append(ns)
    assert goal_st is not None, 'GYM 5 UNSOLVABLE: T3 never reached!'
    assert ud_visited, 'GYM 5 MASTERY UNREACHABLE: Ud never visited!'

    # Reconstruct shortest path
    path = []
    cur = goal_st
    while prev[cur] is not None:
        p_st, act = prev[cur]
        path.append(act)
        cur = p_st
    path.reverse()

    # ZERO-SOFTLOCK PROOF: from EVERY reachable state, BOTH T3 (goal) AND T0 (exit to 210) are reachable!
    for st in prev:
        sub_seen = {st}
        sq = deque([st])
        while sq:
            u = sq.popleft()
            for _, v in neighbors(u):
                if v not in sub_seen:
                    sub_seen.add(v)
                    sq.append(v)
        assert any(t == 'T3' for t, _, _ in sub_seen), f'GYM 5 SOFTLOCK: cannot reach T3 from {st}!'
        assert any(t == 'T0' for t, _, _ in sub_seen), f'GYM 5 SOFTLOCK: cannot return to T0 from {st}!'

    print(f'GYM 5 PUZZLE PROOF PASSED: {len(prev)} reachable states, 0 softlocks, 0 leaks, Ud Mastery reachable!')
    print(f'  Shortest canonical solution ({len(path)} steps): {" -> ".join(path)}')


def main():
    build_210()
    m211, L211 = build_211()
    m212, L212 = build_212()
    build_213()
    verify_gym5_puzzle(m211, L211, m212, L212)
    print('Done: wrote Duneholt Gym 5 specs & raw maps (210, 211, 212, 213).')


if __name__ == '__main__':
    main()
