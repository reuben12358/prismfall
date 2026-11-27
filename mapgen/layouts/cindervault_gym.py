#!/usr/bin/env python3
"""layouts/cindervault_gym.py — Batch 3B: Cindervault Gym 7 ("The Foundry", 4 Maps: 250, 251, 252, 253):
  - Map 250: Cindervault Gym - Entrance         (25x24, TS 61 PF Rejuv Forge, field VOLCANIC)
      Grand volcanic basalt & iron Foundry Lobby + TEACH room ("Pour, then quench"):
      * Exact arrival from 240_cindervault_forge.yaml at (12, 22) facing up, return warps (11..13, 23) -> 240 (21, 3) down
      * Gym Guide (canonical Ch8 field/puzzle briefing), Foundry Medic (full party heal), Foreman at drain grate,
        canonical PBS trainer [CAMPER, Flint]
      * Teach Crucible Lever (W) + Teach Quench Wheel (E) spanning a 5-wide castable lava trench (V339: 0 empty ->
        1 animated PF Magma molten -> 2 walkable lm_grate cast-iron bridge!)
      * North Foundry Portal (12, 4) -> 251 (14, 24) up + HYPERPOTION side alcove
  - Map 251: Cindervault Gym - Puzzle Room 1    (29x27, TS 61 PF Rejuv Forge, field VOLCANIC)
      "Pour Floor — TWIST" (GYM_PUZZLES.md Gym 7):
      * 3 aimable crucibles K1 (X1/X2), K2 (X2/X3), K3 (X1/X3) [V335-V337, S335-S337]
      * 3 quench valves Q1, Q2, Q3 sharing ONE cistern charge [V338: 0 ready, 1 dry]
      * 3 castable lava channels X1, X2, X3 [V435-V437: 0 empty, 1 molten, 2 iron]
      * Chutes C1 (S band) & C2 (Mid2) drain any molten channels (V43k==1 -> V43k=0, S43k=true) into 252 moulds below
      * Apprentice Hessa (status readout, full reset, 3-tier progressive hints, puzzleskip support)
      * Canonical PBS trainers [ENGINEER, Garran] & [BLACKBELT, Ivar] + FULLHEAL pickup
  - Map 252: Cindervault Gym - Puzzle Room 2    (29x27, TS 61 PF Rejuv Forge, field VOLCANIC)
      "Mould Floor — COMBINE + Cracked-Mould Mastery Vault" (GYM_PUZZLES.md Gym 7):
      * Mirrored sub-foundry floor directly below 251 with castable mould pits M1, M2, M3 [S435-S437]
      * Walled-off West Cracked-Mould Mastery Vault (reached by draining X2 unquenched -> M2 cast) holding Brann's
        apprentice-piece hoard (ELEMENTALSEED x2 + CHARCOAL + AF 280 Festival Hammer lore, S339)
      * East Chute-2 Landing Bay -> castable M3 -> North Band -> North Ladder up to 251 Arena Portal
      * Canonical PBS trainers [ENGINEER, Oda] & [COOLTRAINER_M, Dain] + Mould-Runner safety reset NPC
  - Map 253: Cindervault Gym - Warden Arena     (21x19, TS 61 PF Rejuv Forge, field VOLCANIC)
      Warden Brann Holloway's Volcanic Casting Floor Ring suspended over glowing magma chasm:
      * Elevated north basalt dais, blazing volcano beacons, Ashkaar Forge standards, iron-grate battle ring
      * Canonical LEADER_BRANN battle (Prismfall.gym_battle / award_badge / TM35 Flamethrower / CH8_STEP >= 5 / S339 lore)
      * South return warp -> 251 (14, 3) + Fast-Exit Foundry Lift -> 250 (12, 21)

Canonical sources:
  - design/GYM_PUZZLES.md (Gym 7, IDs V335-V339, S335-S339, V435-V437, S435-S437)
  - story/29_SCRIPT_CH8.md (Maps 250-253 dialogue, Gym Guide, Foreman, Hessa, Brann)
  - pbs/trainers.txt (Flint, Garran, Ivar, Oda, Dain, LEADER_BRANN — verified 0 duplicates)

Run:
    /usr/bin/python3 -I mapgen/layouts/cindervault_gym.py
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
TID = 61
FIELD = 'VOLCANIC'
CV_POS = [0, 24, 8]

# Canonical Gym 7 switch / variable IDs (design/GYM_PUZZLES.md §Gym 7, unused in mapgen/flags.yaml)
V_AIM_K1, V_AIM_K2, V_AIM_K3 = 335, 336, 337   # K1: 0=X1/1=X2, K2: 0=X2/1=X3, K3: 0=X1/1=X3
V_QUENCH_DRY = 338                               # 0 = cistern full (1 charge), 1 = dry (0 charges)
V_TEACH = 339                                    # 250 teach channel: 0 empty, 1 molten, 2 iron
S_POUR_K1, S_POUR_K2, S_POUR_K3 = 335, 336, 337  # crucible spent
S_TEACH_DONE = 338                               # 250 teach bridge cast
S_VAULT_DONE = 339                               # 252 Mastery cracked-mould hoard opened
V_X1, V_X2, V_X3 = 435, 436, 437                 # 251 channels: 0 empty, 1 molten, 2 iron
S_M1, S_M2, S_M3 = 435, 436, 437                 # 252 moulds: false empty pit, true cast iron bridge

# Tile IDs verified on TS 61 (PF Rejuv Forge)
T_TROUGH_NW = 25882             # pas=0xf, pri=0 (recessed riveted forged-iron casting wall, left)
T_TROUGH_N = 25883              # pas=0xf, pri=0 (recessed riveted forged-iron casting wall, mid)
T_TROUGH_NE = 25884             # pas=0xf, pri=0 (recessed riveted forged-iron casting wall, right)
T_TROUGH_BED = 23977            # pas=0xf, pri=0 (dark cracked volcanic slag/basalt trough bed)
T_CURB_PIER = 25885             # pas=0xf, pri=0 (solid forged-iron masonry channel divider pier)
T_IRON_GRATE = P1('lm_grate')   # 24393, pas=0x0, pri=0 (walkable iron grate bridge w/ ember glow)
T_IRON_PLATE = P1('Q_f0')       # 25901, pas=0x0, pri=0 (walkable riveted cast-iron mould deck)
T_LEVER_L = P1('cv_lever_l')    # 23910, pas=0xf
T_LEVER_R = P1('cv_lever_r')    # 23911, pas=0xf
T_SPENT = P1('lm_gearbox')      # 25973, pas=0xf
T_VALVE = P1('cv_sluice')       # 24000, pas=0xf
T_VALVE_DRY = P1('cv_sluice_hi')  # 24001, pas=0xf
T_HOLE = P1('cv_hole')          # 23876, pas=0x0 (circular wooden-rung ladder shaft)
T_CHUTE = P1('lm_latch_open')   # 25938, pas=0x0 (heavy dark-iron double chute hatch / lift deck!)
T_DRAIN_VENT = P1('lm_vent')    # 25783, pas=0xf (solid cast-iron floor drain vent grille)
T_PDOOR_OPEN = P1('lm_pdoor_open')  # 25936, pas=0x0


# =================================================================================================
# Shared Helpers
# =================================================================================================
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


def _trough_tile_for(x, x0, x1, is_top_row):
    """Return 3D recessed forged-iron / dark volcanic slag trough tile (pas=0xf, pri=0) for an empty casting span."""
    if not is_top_row:
        return T_TROUGH_BED
    if x == x0:
        return T_TROUGH_NW
    if x == x1:
        return T_TROUGH_NE
    return T_TROUGH_N


def _paint_trough_curbs(m, cols, ys):
    """Paint solid 1-tile forged-iron channel abutment piers (pas=0xf, pri=0) separating magma moats from troughs."""
    qf0 = P1('Q_f0')
    for y in ys:
        for x in cols:
            if m.inb(x, y):
                m.L[0, y, x] = qf0
                m.L[1, y, x] = T_CURB_PIER
                m.L[2, y, x] = 0


def _channel_tile_event(name, x, y, var_id, empty_tile, bridge_tile=T_IRON_GRATE, molten_msg=None):
    """3-state castable channel over PF Magma layer 0:
      - var == 0: recessed forged-iron & dark volcanic slag casting trench (pas=0xf, pri=0)
      - var == 1: blank graphic -> animated PF Magma on L[0] shines through (pas=0xf)!
      - var >= 2: solid iron bridge (lm_grate, pas=0x0, pri=0 -> overrides magma -> WALKABLE!)
    """
    msg = molten_msg or "White-hot molten iron surges through the channel — far too hot to step across! Turn a quench valve to cast it into iron."
    return {
        'type': 'event',
        'name': name,
        'at': [x, y],
        'pages': [
            {
                'graphic': {'tile': empty_tile},
                'trigger': 'action',
                'commands': ["An empty forged-iron casting trench drops down toward the lower moulds. Pour molten iron into it first."],
            },
            {
                'cond': {'var': [var_id, 1]},
                'trigger': 'action',
                'commands': [msg],
            },
            {
                'cond': {'var': [var_id, 2]},
                'graphic': {'tile': bridge_tile},
                'trigger': 'action',
                'commands': [],
            },
        ],
    }


def _mould_tile_event(name, x, y, sw_id, bridge_tile=T_IRON_PLATE):
    """2-state sub-foundry mould pit over recessed forged-iron/slag trough layer 0 (pas=0xf):
      - sw OFF: blank -> recessed forged-iron/slag trough underneath (pas=0xf, impassable pit)
      - sw ON: solid cast-iron deck (Q_f0, pas=0x0, pri=0 -> WALKABLE!)
    """
    return {
        'type': 'event',
        'name': name,
        'at': [x, y],
        'pages': [
            {
                'trigger': 'action',
                'commands': ["An empty cast-iron mould pit beneath the Pour Floor. Whatever drains molten from upstairs will harden into a bridge here."],
            },
            {
                'cond': {'switch': sw_id},
                'graphic': {'tile': bridge_tile},
                'trigger': 'action',
                'commands': [],
            },
        ],
    }


def _paint_foundry_floors(m, zones):
    """Apply cohesive dark Ashkaar Foundry flooring (ashlar T_f, volcanic basalt L_f, riveted iron Q_f, soot lm_low)."""
    palettes = {
        'ashlar': [P1('T_f%d' % i) for i in range(4)],
        'basalt': [P1('L_f%d' % i) for i in range(4)],
        'iron': [P1('Q_f%d' % i) for i in range(4)],
        'soot': [P1('lm_low%d' % i) for i in range(4)],
        'earth': [P1('E_f%d' % i) for i in range(4)],
    }
    floorpatch_ids = {P1(k) for k in STAMPS if k.startswith(('L_floorpatch_', 'L_fd'))}
    for x0, y0, x1, y1, kind in zones:
        pal = palettes[kind]
        for y in range(max(0, y0), min(m.H, y1 + 1)):
            for x in range(max(0, x0), min(m.W, x1 + 1)):
                if m.cls[y, x] != '.' or m.cliff[y, x]:
                    continue
                if int(m.L[1, y, x]) in floorpatch_ids:
                    m.L[1, y, x] = 0
                m.L[0, y, x] = pal[(x * 3 + y * 5) % len(pal)]


def _paint_crimson_runner(m, x0, y0, x1, y1):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if m.cls[y, x] != '.' or m.cliff[y, x] or m.L[1, y, x] != 0:
                continue
            part = ('n' if y == y0 else 's' if y == y1 else '') + ('w' if x == x0 else 'e' if x == x1 else '')
            m.L[1, y, x] = P1('mn_rugR_' + (part or ('c2' if (y - y0) % 3 == 1 else 'c')))


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


def _sim_bfs(Lr, events, start, targets, label, vars_=None, sw=None):
    """Exact Essentials 4-bit directional + tile-event BFS for a given (vars_, sw) puzzle state."""
    import build as B
    vars_ = vars_ or {}
    sw = sw or {}
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


def _finalize_cave(m, mid, head, comment, check_start=None, check_targets=None):
    """Paint, run passguard with 0 hits, verify BFS, and write spec + raw npy."""
    m.paint()
    Lr = RC.resolve(m.L, TID).astype(np.int32)
    ev_pts = [tuple(e['at']) for e in m.events if e and e.get('at')]
    PG.guard(Lr, TID, ev_pts, f'Map {mid}')
    ts = R.tilesets()[TID]
    hits = PG.hits(Lr, ts, ev_pts)
    assert not hits, f'Map {mid} passguard hits: {hits[:5]}'
    # Copy guarded layers back into m.L before m.write() so raw .npy matches resolved/guarded tiles
    m.L = Lr
    if check_start is not None and check_targets is not None:
        _sim_bfs(Lr, m.events, check_start, check_targets, f'Map {mid} (initial)')
    m.write(mid, head, comment=comment)
    return m, Lr


# =================================================================================================
# MAP 250 — Cindervault Gym - Entrance ("Gate Hall — TEACH", 25x24, TS 61, VOLCANIC)
# Exact arrival from 240_cindervault_forge.yaml: (12, 22) facing up!
# =================================================================================================
def build_250():
    W, H = 25, 24
    m = Cave(W, H, 'L', seed=250, pool='Magma', tid=TID)
    m.STAIRS = K.STAIRS_STONE
    K.KITS['cvH2'] = dict(K.KITS['cvH'], rows=[K.KITS['cvH']['rows'][0], K.KITS['cvH']['rows'][2]])
    m.kit = {TER: 'cvH2', FLOOR: 'cvH2', MASS: 'cvH2', 'default': 'cvH2'}

    # ---- 1. Sculpt Cruciform Volcanic Foundry Gate Hall from Black Void (ZERO flat box!) ----
    # North Foundry Portal Vestibule (y=4..9, x=4..20) + recessed portal niche (x=10..14, y=3..4)
    m.box(4, 4, 20, 9, FLOOR, '.')
    m.box(10, 3, 14, 4, FLOOR, '.')
    # TEACH Molten Casting Moat (y=10..11, x=4..20) flanked by solid 1-tile basalt/iron channel curbs (x=9 & x=15)!
    # Central 5-wide crossing (x=10..14, y=10..11) is controlled by 3-state castable Teach Channel events!
    m.box(4, 10, 20, 11, FLOOR, 'w')
    for cy in (10, 11):
        for cx in (9, 15):
            m.cls[cy, cx] = '.'
    # Main Foundry Lobby & Crucible Control Deck (y=12..21, x=3..21)
    m.box(3, 12, 21, 21, FLOOR, '.')
    # Recessed South Entry Vestibule (x=9..15, y=22..23 -> exact 240 arrival (12,22) & return warps (11..13,23)!)
    m.box(9, 22, 15, 23, FLOOR, '.')

    # Sculpted obsidian corner chamfers & hearth piers
    m.mass_at([
        (4, 4), (20, 4), (3, 20), (3, 21), (4, 21), (21, 20), (21, 21), (20, 21),
        (3, 12), (21, 12), (9, 23), (15, 23),
    ])

    m.tidy()
    m.plan_cliffs(rows=2)

    # ---- 2. Events: Warps, TEACH Crucible & Quench, Gym Guide, Healer, Foreman, Flint ----
    E = m.events

    # South Return Warps -> 240 Forge Terraces (21, 3, down)
    for rx in (11, 12, 13):
        E.append({
            'type': 'warp',
            'name': 'Exit to Cindervault',
            'at': [rx, 23],
            'to': {'map': 240, 'x': 21, 'y': 3, 'dir': 'down'},
            'se': 'Door exit',
        })

    # North Foundry Portal -> 251 Pour Floor (14, 24, up)
    E.append({
        'type': 'warp',
        'name': 'To Pour Floor (251)',
        'at': [12, 4],
        'to': {'map': 251, 'x': 14, 'y': 24, 'dir': 'up'},
        'se': 'Door enter',
    })

    # TEACH 5x2 Castable Channel Events (x=10..14, y=10..11) over animated PF Magma (3D forged-iron/slag empty trough)!
    for y in (10, 11):
        for x in range(10, 15):
            E.append(_channel_tile_event(
                f'Teach X {x},{y}', x, y, V_TEACH,
                _trough_tile_for(x, 10, 14, y == 10), T_IRON_GRATE,
                "White-hot molten iron glows in the casting trench! Turn the Quench Wheel on the east deck to harden it into a walkable bridge."
            ))

    # TEACH Crucible Lever (West Deck, (7, 13))
    pour_ruby = (
        f'v = $game_variables[{V_TEACH}].to_i\n'
        'if v == 0\n'
        '  pbSEPlay("Anim/Fire4", 90, 85)\n'
        '  pfm_shake(3, 8, 12)\n'
        f'  $game_variables[{V_TEACH}] = 1\n'
        '  $game_map.need_refresh = true\n'
        '  pbMessage(_INTL("CLANK! The crucible tips — glowing molten iron surges across the casting trench!"))\n'
        '  pbMessage(_INTL("Too hot to walk across yet. Turn the Quench Wheel on the east deck to cool it into solid iron."))\n'
        'elsif v == 1\n'
        '  pbMessage(_INTL("The trench is already brimming with molten iron! Turn the Quench Wheel on the east side to harden it."))\n'
        'else\n'
        '  pbMessage(_INTL("The crucible lever is locked — the bridge ahead is already quenched solid."))\n'
        'end'
    )
    E.append({
        'type': 'event',
        'name': 'Teach Crucible Lever',
        'at': [7, 13],
        'pages': [
            {'graphic': {'tile': T_LEVER_L}, 'trigger': 'action', 'commands': [{'script': pour_ruby}]},
            {'cond': {'var': [V_TEACH, 1]}, 'graphic': {'tile': T_LEVER_R}, 'trigger': 'action', 'commands': [{'script': pour_ruby}]},
        ],
    })

    # TEACH Quench Wheel (East Deck, (17, 13))
    quench_ruby = (
        f'v = $game_variables[{V_TEACH}].to_i\n'
        'if v == 0\n'
        '  pbSEPlay("GUI sel buzzer", 80, 100)\n'
        '  pbMessage(_INTL("Nothing in the trench to quench! Pull the Crucible Lever on the west deck to pour molten iron first."))\n'
        'elsif v == 1\n'
        '  pbSEPlay("Anim/Water3", 95, 90)\n'
        '  pbSEPlay("Anim/metal", 85, 85)\n'
        f'  $game_variables[{V_TEACH}] = 2\n'
        f'  $game_switches[{S_TEACH_DONE}] = true\n'
        '  $game_map.need_refresh = true\n'
        '  pbMessage(_INTL("HISS! Cold quench water floods the iron — steam roars up, and the molten stream hardens into a solid iron bridge!"))\n'
        'else\n'
        '  pbMessage(_INTL("The iron bridge is quenched and cool enough to cross."))\n'
        'end'
    )
    E.append({
        'type': 'event',
        'name': 'Teach Quench Wheel',
        'at': [17, 13],
        'pages': [
            {'graphic': {'tile': T_VALVE}, 'trigger': 'action', 'commands': [{'script': quench_ruby}]},
            {'cond': {'switch': S_TEACH_DONE}, 'graphic': {'tile': T_VALVE_DRY}, 'trigger': 'action', 'commands': [{'script': quench_ruby}]},
        ],
    })

    # Gym Guide (canonical story/29_SCRIPT_CH8.md lines 200-206!)
    E.append(_make_npc('Gym Guide', (9, 19), 'NPC 21', 'right', [
        "Gym Guide: Yo, challenger! Welcome to The Foundry — Fire-types on the Volcanic field!",
        "Gym Guide: Rock moves hit like Fire here, and everybody leans on Lava Plume. Bring Water. Bring a lot of Water.",
        "Gym Guide: The puzzle's simple: Pour, then quench. Molten's a wall, iron's a bridge, and what you don't quench runs down to the moulds below.",
        "Gym Guide: Warden Brann says the bridge you don't finish is the one that carries you. He says it a lot.",
    ]))

    # Lobby Healer / Foundry Medic (Prismfall Gym Lobby Standard!)
    heal_ruby = (
        'pbMessage(_INTL("Foundry Medic: The caldera heat takes it out of a team fast. Let me patch your Pokémon up before you step onto the casting floor!"))\n'
        'pbMEPlay("Pkmn healing")\n'
        'pbFadeOutIn do\n'
        '  $player.heal_party\n'
        'end\n'
        'pbMessage(_INTL("Foundry Medic: Good as tempered steel! Come right back here whenever you need a cool compress and a breather."))'
    )
    E.append({
        'type': 'event',
        'name': 'Foundry Medic',
        'at': [15, 19],
        'pages': [{
            'graphic': {'sprite': 'NPC 18', 'dir': 'left'},
            'trigger': 'action',
            'move': 'fixed',
            'commands': [{'script': heal_ruby}],
        }],
    })

    # Canonical Foreman beside floor drain grate (story/29_SCRIPT_CH8.md line 207!)
    E.append(_make_npc('Foundry Foreman', (15, 14), 'trainer_HIKER', 'down', [
        "Foreman: Pull the west lever to pour molten iron into the trench, then turn the east wheel to quench it solid.",
        "Foreman: And remember on the Pour Floor upstairs: what you don't quench runs down to the moulds below. Waste not.",
    ]))

    # Canonical PBS Trainer #1: [CAMPER, Flint] (pbs/trainers.txt:15731, # Map 250 Cindervault Gym - Entrance)
    E.append(_trainer(
        (7, 16), 'CAMPER', 'Flint', 'right',
        "Kindler Flint: Warden Brann says every challenger needs a spark before they touch a crucible. Let's strike one!",
        "Kindler Flint: Kindler's job is to start the fire. You put me out.",
        sight=3,
    ))

    # Gym Statues / Plaques & North Alcove Pickup
    E += [
        _sign('Foundry Statue West', (10, 21),
              "CINDERVAULT GYM — THE FOUNDRY · WARDEN: BRANN HOLLOWAY · TYPE: FIRE · FIELD: VOLCANIC · BADGE: QUENCH BADGE."),
        _sign('Foundry Statue East', (14, 21),
              "FOUNDRY RULE OF CASTING: EMPTY TRENCH -> POUR (MOLTEN) -> QUENCH (IRON BRIDGE). UNQUENCHED MOLTEN DRAINS DOWN TO THE MOULDS BELOW."),
        _sign('Floor Drain Grate', (14, 14),
              "A heavy cast-iron floor drain vent humming with heat from the Mould Floor underneath. Molten runoff trickles down through channels like this."),
        {'type': 'item', 'at': [7, 6], 'item': 'HYPERPOTION', 'name': 'Foundry Hyper Potion'},
    ]

    # Reserve walkways, events, bridge approaches & doors
    m.keep_clear |= {
        (12, 22), (11, 22), (13, 22), (11, 23), (12, 23), (13, 23),
        (12, 4), (12, 5), (12, 6), (11, 5), (13, 5),
        (10, 9), (11, 9), (12, 9), (13, 9), (14, 9),
        (10, 12), (11, 12), (12, 12), (13, 12), (14, 12),
    }
    for e in E:
        ex, ey = e['at']
        m.keep_clear.add((ex, ey))
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            if m.inb(ex + dx, ey + dy):
                m.keep_clear.add((ex + dx, ey + dy))

    # ---- 3. Foundry Architecture, Braziers, Banners, Chains, Bellows & Glow Halos ----
    # North Foundry Portal frame & twin banners
    _place_stamp_over(m, 'cv_frame', 11, 3, base_z=1, top_z=2, top_rows=1, solid=False)
    m.over.append((1, 12, 4, T_PDOOR_OPEN))
    _place_stamp_over(m, 'wr_ban_ash', 9, 4, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'wr_ban_ash', 15, 4, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'fw_brazier', 9, 7, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'fw_brazier', 15, 7, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'wr_rack', 17, 5, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'cv_tools', 17, 7, base_z=1, top_z=1, top_rows=0, solid=True)

    # Casting Deck Machinery (Bellows pump on West behind Crucible, Quench cistern barrels on East)
    _place_stamp_over(m, 'cv_pump', 4, 13, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'cv_cart', 4, 16, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'hb_barrels', 19, 13, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'hb_cask', 19, 16, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'wr_rack', 20, 18, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'wr_sacks', 4, 19, base_z=1, top_z=1, top_rows=0, solid=True)

    # Bridge abutment bollards & South Gym Entry statues / braziers
    for bx, by in ((9, 9), (15, 9), (9, 12), (15, 12)):
        _place_stamp_over(m, 'lm_bollard', bx, by, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'mn_statue', 10, 20, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'mn_statue', 14, 20, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'fw_brazier', 7, 19, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'fw_brazier', 17, 19, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'wr_ban_ash', 5, 17, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'wr_ban_ash', 19, 17, base_z=1, top_z=2, top_rows=2, solid=True)

    # Wall lamps, overhead iron chains, steam plumes & mirror-symmetric fire glow halos!
    for sx, sy in ((6, 3), (18, 3), (10, 3), (14, 3)):
        m.over.append((2, sx, sy, P1('cv_walllamp')))
    for cx, cy in ((8, 4), (16, 4)):
        m.over.append((2, cx, cy, P1('cv_chain')))
    for sx, sy in ((5, 10), (7, 10), (17, 10), (19, 10)):
        _place_stamp_over(m, 'lm_steam0' if sx % 2 else 'lm_steam1', sx, sy, base_z=2, top_z=2, top_rows=2, solid=False)
    for gx, gy in ((9, 7), (14, 7), (7, 19), (16, 19), (11, 4)):
        m.stamps.append(('pf_glow', gx, gy))
    m.stamps.append(('cv_shaft', 11, 5))

    m.paint()
    _paint_foundry_floors(m, [
        (3, 12, 21, 21, 'basalt'),
        (6, 13, 18, 20, 'ashlar'),
        (9, 21, 15, 23, 'soot'),
        (4, 4, 20, 9, 'ashlar'),
        (10, 3, 14, 9, 'iron'),
        (10, 12, 14, 15, 'iron'),
    ])
    # Solid forged-iron channel abutment piers at x=9 and x=15 (pas=0xf) framing Teach Channel!
    _paint_trough_curbs(m, (9, 15), (10, 11))
    _paint_crimson_runner(m, 11, 15, 13, 22)
    # Solid cast-iron floor drain vent at (14, 14) (pas=0xf -> over_trigger? == false!) & entrance mat
    m.L[1, 14, 14] = T_DRAIN_VENT
    m.L[1, 23, 11] = P1('lm_grate_off')
    m.L[1, 23, 12] = P1('lm_grate_off')
    m.L[1, 23, 13] = P1('lm_grate_off')

    Lr = RC.resolve(m.L, TID).astype(np.int32)
    ev_pts = [tuple(e['at']) for e in E]
    PG.guard(Lr, TID, ev_pts, 'Map 250')
    assert not PG.hits(Lr, R.tilesets()[TID], ev_pts), 'Map 250 passguard hits!'
    m.L = Lr

    # Verify initial state (south lobby reachable, north sealed!) AND quenched state (100% reachable!)
    seen0 = _sim_bfs(Lr, E, (12, 22), [
        ('Exit to 240', (12, 23), False),
        ('Gym Guide', (9, 19), True),
        ('Foundry Medic', (15, 19), True),
        ('Foreman', (15, 14), True),
        ('Floor Drain Grate', (14, 14), True),
        ('Trainer Flint', (7, 16), True),
        ('Teach Crucible Lever', (7, 13), True),
        ('Teach Quench Wheel', (17, 13), True),
    ], 'Map 250 (unquenched)')
    assert (12, 4) not in seen0, 'Map 250 LEAK: North portal reachable before quenching Teach bridge!'
    _sim_bfs(Lr, E, (12, 22), [
        ('North Portal -> 251', (12, 4), False),
        ('Hyper Potion', (7, 6), True),
    ], 'Map 250 (quenched V339=2)', vars_={V_TEACH: 2}, sw={S_TEACH_DONE: True})

    head = {
        'id': 250,
        'name': 'Cindervault Gym - Entrance',
        'parent': 240,
        'bgm': 'Gym',
        'field': FIELD,
        'map_audio': {'bgm': 'Gym - Warden Hall', 'bgs': 'Lava - Ashkaar', 'bgs_volume': 40, 'rain': False},
        'metadata': {'Name': 'Cindervault Gym', 'SnapEdges': True, 'MapPosition': CV_POS, 'BattleBack': 'cave1'},
        'tone': [20, 2, -16, 10],
        '_file': '250_cindervault_gym.yaml',
    }
    m.write(250, head, comment='# GENERATED by mapgen/layouts/cindervault_gym.py (Batch 3B): Cindervault Gym - Entrance (TEACH).\n'
                               '# Edit the layout script, not this file.\n')
    return m, Lr


# =================================================================================================
# MAP 251 — Cindervault Gym - Puzzle Room 1 ("Pour Floor — TWIST", 29x27, TS 61, VOLCANIC)
# =================================================================================================
def _crucible_ruby(name, aim_var, pour_sw, ch_a, ch_b, lbl_a, lbl_b):
    """Self-contained RMXP Ruby for an aimable single-pour crucible."""
    return f'''if $game_switches[{pour_sw}]
  pbMessage(_INTL("{name} is empty — its iron has already been poured. Ask Apprentice Hessa to reset the foundry if you want a fresh cast."))
else
  aim = $game_variables[{aim_var}].to_i
  tgt_lbl = (aim == 0) ? "{lbl_a}" : "{lbl_b}"
  alt_lbl = (aim == 0) ? "{lbl_b}" : "{lbl_a}"
  c = pbMessage(_INTL("{name} is brimming with molten iron, aimed at Channel {{1}}.", tgt_lbl),
                [_INTL("Aim spout at {{1}}", alt_lbl), _INTL("Pour into {{1}}", tgt_lbl), _INTL("Leave it")], 3)
  if c == 0
    pbSEPlay("Strength push", 85, 100)
    $game_variables[{aim_var}] = (aim == 0) ? 1 : 0
    $game_map.need_refresh = true
    pbMessage(_INTL("The bronze spout grinds round — {name} now aims at Channel {{1}}.", alt_lbl))
  elsif c == 1
    tgt_var = (aim == 0) ? {ch_a} : {ch_b}
    cur = $game_variables[tgt_var].to_i
    pbSEPlay("Anim/Fire4", 95, 85)
    pfm_shake(3, 8, 12)
    $game_switches[{pour_sw}] = true
    if cur == 0
      $game_variables[tgt_var] = 1
      $game_map.need_refresh = true
      pbMessage(_INTL("ROAR! {name} pours white-hot molten iron into Channel {{1}}!", tgt_lbl))
    elsif cur == 2
      $game_variables[tgt_var] = 1
      $game_map.need_refresh = true
      pbMessage(_INTL("HISS! Fresh molten iron re-melts the iron bridge in Channel {{1}}!", tgt_lbl))
    else
      $game_map.need_refresh = true
      pbMessage(_INTL("{name} pours into Channel {{1}}, which is already brimming molten.", tgt_lbl))
    end
  end
end'''


def _quench_ruby(q_label, ch_var, ch_label):
    """Self-contained RMXP Ruby for Quench Valve Q1/Q2/Q3 sharing ONE cistern charge (V338: 0 ready, 1 dry)."""
    return f'''if $game_variables[{V_QUENCH_DRY}].to_i >= 1
  pbSEPlay("GUI sel buzzer", 80, 100)
  pbMessage(_INTL("{q_label} ({ch_label}): The quench cistern is dry — the foundry only holds ONE quench charge per cast! Ask Hessa to reset."))
elsif $game_variables[{ch_var}].to_i == 1
  pbSEPlay("Anim/Water3", 95, 90)
  pbSEPlay("Anim/metal", 85, 85)
  $game_variables[{ch_var}] = 2
  $game_variables[{V_QUENCH_DRY}] = 1
  $game_map.need_refresh = true
  pbMessage(_INTL("HISS! Quench water surges into {ch_label} — steam billows as it hardens into a walkable iron bridge! (Cistern is now dry.)"))
elsif $game_variables[{ch_var}].to_i == 2
  pbMessage(_INTL("{ch_label} is already cast in solid iron."))
else
  pbSEPlay("GUI sel buzzer", 80, 100)
  pbMessage(_INTL("{q_label}: Nothing molten in {ch_label} to quench yet!"))
end'''


def _chute_drain_ruby(chute_label, dest_x, dest_y, dest_dir=2):
    """Player-Touch chute confirm: drains molten channels (V43k==1 -> 0, S43k=true) & drops to 252, or steps cleanly back."""
    return f'''if pbConfirmMessage(_INTL("Drop down {chute_label} to the Mould Floor? (Any molten iron upstairs will drain into the moulds below!)"))
  drained = []
  [[{V_X1}, {S_M1}, "M1"], [{V_X2}, {S_M2}, "M2"], [{V_X3}, {S_M3}, "M3"]].each do |v, s, nm|
    if $game_variables[v].to_i == 1
      $game_variables[v] = 0
      $game_switches[s] = true
      drained.push(nm)
    end
  end
  if !drained.empty?
    pbSEPlay("Anim/Earth4", 90, 80)
    pbSEPlay("Anim/metal", 85, 85)
    pfm_shake(3, 8, 12)
    pbMessage(_INTL("A deep roar shakes the floor below! Unquenched molten iron drains straight into mould(s): {{1}}!", drained.join(", ")))
  end
  pbSEPlay("Door exit", 85, 100)
  pbFadeOutIn do
    $game_temp.player_new_map_id = 252
    $game_temp.player_new_x = {dest_x}
    $game_temp.player_new_y = {dest_y}
    $game_temp.player_new_direction = {dest_dir}
    $scene.transfer_player
  end
else
  pbMoveRoute($game_player, [PBMoveRoute::BACKWARD], true)
end'''


def _reset_foundry_ruby(warp_to_251=False):
    warp = (
        '  $game_temp.player_new_map_id = 251\n'
        '  $game_temp.player_new_x = 14\n'
        '  $game_temp.player_new_y = 23\n'
        '  $game_temp.player_new_direction = 8\n'
        '  $scene.transfer_player\n'
    ) if warp_to_251 else (
        '  $game_player.moveto(14, 23)\n'
        '  $game_player.turn_up\n'
    )
    return f'''pbSEPlay("Anim/Water2", 85, 95)
pbFadeOutIn do
  [{V_AIM_K1}, {V_AIM_K2}, {V_AIM_K3}, {V_QUENCH_DRY}, {V_X1}, {V_X2}, {V_X3}].each {{ |v| $game_variables[v] = 0 }}
  [{S_POUR_K1}, {S_POUR_K2}, {S_POUR_K3}, {S_M1}, {S_M2}, {S_M3}].each {{ |s| $game_switches[s] = false }}
{warp}  $game_map.need_refresh = true
end
pbMessage(_INTL("Crucibles refilled, moulds cleared, and the quench cistern topped up to 1 charge!"))'''


def _hessa_ruby():
    return f'''st_fn = proc do |v|
  x = $game_variables[v].to_i
  x == 0 ? "Empty" : (x == 1 ? "MOLTEN" : "IRON BRIDGE")
end
m_fn = proc {{ |s| $game_switches[s] ? "CAST IRON" : "Empty pit" }}
cmds = [_INTL("Check foundry status"), _INTL("Reset the foundry"), _INTL("Ask for a hint")]
can_skip = ($game_switches[301] == true)
cmds.push(_INTL("Skip puzzle (puzzleskip)")) if can_skip
cmds.push(_INTL("Never mind"))
c = pbMessage(_INTL("Apprentice Hessa: Brann says pour where it hurts, not where it's easy. Need a hand on the Pour Floor?"), cmds, cmds.length)
if c == 0
  q = ($game_variables[{V_QUENCH_DRY}].to_i == 0) ? "1 charge ready" : "DRY (0 left)"
  k1 = $game_switches[{S_POUR_K1}] ? "Spent" : ($game_variables[{V_AIM_K1}].to_i == 0 ? "aimed X1" : "aimed X2")
  k2 = $game_switches[{S_POUR_K2}] ? "Spent" : ($game_variables[{V_AIM_K2}].to_i == 0 ? "aimed X2" : "aimed X3")
  k3 = $game_switches[{S_POUR_K3}] ? "Spent" : ($game_variables[{V_AIM_K3}].to_i == 0 ? "aimed X1" : "aimed X3")
  pbMessage(_INTL("Crucibles: K1={{1}}, K2={{2}}, K3={{3}}. Quench cistern: {{4}}.", k1, k2, k3, q))
  pbMessage(_INTL("Upstairs channels: X1={{1}}, X2={{2}}, X3={{3}}.\\nMoulds below: M1={{4}}, M2={{5}}, M3={{6}}.",
                  st_fn.call({V_X1}), st_fn.call({V_X2}), st_fn.call({V_X3}),
                  m_fn.call({S_M1}), m_fn.call({S_M2}), m_fn.call({S_M3})))
elsif c == 1
  if pbConfirmMessage(_INTL("Reset all crucibles, channels, moulds, and refill the quench cistern?"))
    {_reset_foundry_ruby(False).replace(chr(10), chr(10) + "    ")}
  end
elsif c == 2
  h = (pfm_get(:g7_hint).to_i rescue 0)
  if h == 0
    pbMessage(_INTL("Hessa (Hint 1): Brann never wastes a pour. Whatever channel is still MOLTEN when you drop down a chute drains down and casts the matching mould below!"))
  elsif h == 1
    pbMessage(_INTL("Hessa (Hint 2): You only get ONE quench upstairs. Look at the floor below: M1 and M3 can carry you across, but M2 only leads to Brann's side vault — NOT to the second chute! So which single channel MUST be quenched upstairs?"))
  else
    pbMessage(_INTL("Hessa (Full Solution): 1) Aim K1->X2, K2->X3, K3->X1 and pour all three. 2) Pull Quench Valve Q2 ONLY (X2 becomes iron). 3) Drop down Chute C1 (X1 and X3 drain to cast M1 and M3 below!). 4) Cross M1 -> climb Ladder H -> cross X2 -> drop Chute C2 -> cross M3 -> climb North Ladder to Brann!"))
  end
  (pfm_set(:g7_hint, [h + 1, 2].min) rescue nil)
elsif can_skip && c == 3
  pbSEPlay("Anim/metal", 90, 90)
  $game_variables[{V_X1}] = 0
  $game_variables[{V_X2}] = 2
  $game_variables[{V_X3}] = 0
  $game_variables[{V_QUENCH_DRY}] = 1
  $game_switches[{S_POUR_K1}] = true
  $game_switches[{S_POUR_K2}] = true
  $game_switches[{S_POUR_K3}] = true
  $game_switches[{S_M1}] = true
  $game_switches[{S_M3}] = true
  $game_map.need_refresh = true
  pbMessage(_INTL("Hessa throws the master bypass! M1 and M3 are cast below, and X2 is quenched upstairs — head down Chute C1!"))
end'''


def build_251():
    W, H = 29, 27
    m = Cave(W, H, 'L', seed=251, pool='Magma', tid=TID)
    m.STAIRS = K.STAIRS_STONE
    K.KITS['cvH2'] = dict(K.KITS['cvH'], rows=[K.KITS['cvH']['rows'][0], K.KITS['cvH']['rows'][2]])
    m.kit = {TER: 'cvH2', FLOOR: 'cvH2', MASS: 'cvH2', 'default': 'cvH2'}

    # ---- 1. Sculpt 4-Band Foundry Pour Floor separated by 3 Glowing Lava Moats ----
    # North Arena Band (y=2..4, x=3..25)
    m.box(3, 2, 25, 4, FLOOR, '.')
    # Channel X3 Lava Moat (y=5..6, x=3..25 -> castable iron span x=12..16 flanked by curbs x=11/17!)
    m.box(3, 5, 25, 6, FLOOR, 'w')
    # Mid2 Upper Pour Deck (y=7..10, x=3..25)
    m.box(3, 7, 25, 10, FLOOR, '.')
    # Channel X2 Lava Moat (y=11..12, x=3..25 -> castable iron span x=12..16 flanked by curbs x=11/17!)
    m.box(3, 11, 25, 12, FLOOR, 'w')
    # Mid1 Central Casting Deck (y=13..16, x=3..25)
    m.box(3, 13, 25, 16, FLOOR, '.')
    # Channel X1 Lava Moat (y=17..18, x=3..25 -> castable iron span x=12..16 flanked by curbs x=11/17!)
    m.box(3, 17, 25, 18, FLOOR, 'w')
    # South Crucible & Quench Control Deck (y=19..24, x=3..25)
    m.box(3, 19, 25, 24, FLOOR, '.')
    # Narrowed South Vestibule to 250 (x=12..16, y=25)
    m.box(12, 25, 16, 25, FLOOR, '.')
    # Reserve 1-tile solid forged-iron channel curb piers separating magma moats from castable channels X1-X3!
    for cy in (5, 6, 11, 12, 17, 18):
        for cx in (11, 17):
            m.cls[cy, cx] = '.'

    # Sculpted foundry piers & SE steaming cooling cistern pool (Cave Pool!)
    m.auto = {'w': ('Magma', 'pf'), 'q': ('Cave Pool', 'pf'), 'W': ('Sea deep', 'rejuvenation')}
    m.mass_at([
        (3, 2), (25, 2), (3, 23), (3, 24), (4, 24), (25, 23), (25, 24), (24, 24),
        (11, 25), (17, 25),
    ])
    # Quench Cistern water basin beside Q1-Q3 (x=24..25, y=20..21) — visual storytelling for the 1 quench charge!
    for qx, qy in ((24, 20), (25, 20), (24, 21), (25, 21)):
        m.cls[qy, qx] = 'q'

    m.tidy()
    m.plan_cliffs(rows=2)

    # ---- 2. Events: Warps, 3 Castable Channels, 3 Crucibles, 3 Quench Valves, 2 Chutes, 2 Ladders, Hessa, Trainers ----
    E = m.events

    # South Return Warps -> 250 Gate Hall (12, 5, down)
    for rx in (13, 14, 15):
        E.append({
            'type': 'warp',
            'name': 'Back to Entrance (250)',
            'at': [rx, 25],
            'to': {'map': 250, 'x': 12, 'y': 5, 'dir': 'down'},
            'se': 'Door exit',
        })

    # North Arena Portal -> 253 Warden Arena (10, 16, up)
    E.append({
        'type': 'warp',
        'name': 'To Warden Arena (253)',
        'at': [14, 2],
        'to': {'map': 253, 'x': 10, 'y': 16, 'dir': 'up'},
        'se': 'Door enter',
    })

    # Castable Channels X1 (y=17..18), X2 (y=11..12), X3 (y=5..6) — 5-wide crossing x=12..16 (3D forged-iron/slag trough)!
    for ch_lbl, var_id, rows in (('X1', V_X1, (17, 18)), ('X2', V_X2, (11, 12)), ('X3', V_X3, (5, 6))):
        for y in rows:
            for x in range(12, 17):
                E.append(_channel_tile_event(
                    f'{ch_lbl} {x},{y}', x, y, var_id,
                    _trough_tile_for(x, 12, 16, y == rows[0]), T_IRON_GRATE,
                    f"Channel {ch_lbl} is roaring with molten iron! Quench it with Q{ch_lbl[1]} — or drop down a chute to drain it into Mould M{ch_lbl[1]} below."
                ))

    # Three Aimable Single-Pour Crucibles (West Control Deck: K1=(5,19), K2=(8,19), K3=(11,19))
    for nm, x, aim_v, pour_s, ca, cb, la, lb in (
        ('Crucible K1', 5, V_AIM_K1, S_POUR_K1, V_X1, V_X2, 'X1', 'X2'),
        ('Crucible K2', 8, V_AIM_K2, S_POUR_K2, V_X2, V_X3, 'X2', 'X3'),
        ('Crucible K3', 11, V_AIM_K3, S_POUR_K3, V_X1, V_X3, 'X1', 'X3'),
    ):
        rb = _crucible_ruby(nm, aim_v, pour_s, ca, cb, la, lb)
        E.append({
            'type': 'event',
            'name': nm,
            'at': [x, 19],
            'pages': [
                {'graphic': {'tile': T_LEVER_L}, 'trigger': 'action', 'commands': [{'script': rb}]},
                {'cond': {'var': [aim_v, 1]}, 'graphic': {'tile': T_LEVER_R}, 'trigger': 'action', 'commands': [{'script': rb}]},
                {'cond': {'switch': pour_s}, 'graphic': {'tile': T_SPENT}, 'trigger': 'action', 'commands': [{'script': rb}]},
            ],
        })

    # Three Quench Valves sharing ONE Cistern Charge (East Control Deck: Q1=(21,19), Q2=(22,20), Q3=(21,21))
    for nm, (qx, qy), ch_v, ch_l in (
        ('Quench Valve Q1', (21, 19), V_X1, 'X1'),
        ('Quench Valve Q2', (22, 20), V_X2, 'X2'),
        ('Quench Valve Q3', (21, 21), V_X3, 'X3'),
    ):
        rb = _quench_ruby(nm, ch_v, ch_l)
        E.append({
            'type': 'event',
            'name': nm,
            'at': [qx, qy],
            'pages': [
                {'graphic': {'tile': T_VALVE}, 'trigger': 'action', 'commands': [{'script': rb}]},
                {'cond': {'var': [V_QUENCH_DRY, 1]}, 'graphic': {'tile': T_VALVE_DRY}, 'trigger': 'action', 'commands': [{'script': rb}]},
            ],
        })

    # Slag Chutes C1 (14,22 -> 252 (14,23) down) & C2 (23,8 -> 252 (23,9) down) — Player Touch + Confirm + Iron Chute Hatch!
    E.append({
        'type': 'event',
        'name': 'Slag Chute C1',
        'at': [14, 22],
        'pages': [{'graphic': {'tile': T_CHUTE}, 'trigger': 'touch', 'commands': [{'script': _chute_drain_ruby('Slag Chute C1', 14, 23, 2)}]}],
    })
    E.append({
        'type': 'event',
        'name': 'Slag Chute C2',
        'at': [23, 8],
        'pages': [{'graphic': {'tile': T_CHUTE}, 'trigger': 'touch', 'commands': [{'script': _chute_drain_ruby('Slag Chute C2', 23, 9, 2)}]}],
    })

    # Up/Down Ladders connecting to 252 Mould Floor (no drain on ladders; circular wooden-rung cv_hole visual):
    # Ladder H (5, 14) <-> 252 (5, 14) [lands (6,14) right]
    E.append({
        'type': 'warp',
        'name': 'Ladder H down to 252',
        'at': [5, 14],
        'to': {'map': 252, 'x': 6, 'y': 14, 'dir': 'right'},
        'se': 'Door exit',
    })
    # North Ladder (23, 3) <-> 252 (23, 3) [lands (22,3) left]
    E.append({
        'type': 'warp',
        'name': 'North Ladder down to 252',
        'at': [23, 3],
        'to': {'map': 252, 'x': 22, 'y': 3, 'dir': 'left'},
        'se': 'Door exit',
    })

    # Apprentice Hessa ("Sooty") at (18, 22)
    E.append({
        'type': 'event',
        'name': 'Apprentice Hessa',
        'at': [18, 22],
        'pages': [{
            'graphic': {'sprite': 'NPC 13', 'dir': 'left'},
            'trigger': 'action',
            'move': 'fixed',
            'commands': [{'script': _hessa_ruby()}],
        }],
    })

    # Canonical PBS Trainers for Map 251 (pbs/trainers.txt:15780 & 15829 — 0 duplicates!)
    E.append(_trainer(
        (17, 20), 'ENGINEER', 'Garran', 'left',
        "Foundry Engineer Garran: Bellows up, crucibles hot! Let's test if you can handle the heat before touching Brann's valves!",
        "Foundry Engineer Garran: Bellows up, bellows down. I'm winded either way.",
        sight=2,
    ))
    E.append(_trainer(
        (19, 14), 'BLACKBELT', 'Ivar', 'left',
        "Black Belt Ivar: Made it up Ladder H? Good footwork — now test your grip against my team!",
        "Black Belt Ivar: I hold the tongs. I couldn't hold you.",
        sight=3,
    ))

    # Plaques (backed by real solid pf_signposts!) & Mid1 Pickup
    E += [
        _sign('Crucible Schematic', (7, 22),
              "POUR FLOOR SCHEMATIC: K1 aims X1/X2 · K2 aims X2/X3 · K3 aims X1/X3. ONE quench charge per cast (Q1/Q2/Q3). Step onto Slag Chute C1 or C2 to drain molten channels into the Mould Floor below!"),
        _sign('Upper Chute Plaque', (8, 8),
              "UPPER POUR DECK (MID 2): Slag Chute C2 on the east iron bay drops directly above Mould M3 below. Any iron left molten in X3 casts M3 solid!"),
        {'type': 'item', 'at': [23, 14], 'item': 'FULLHEAL', 'name': 'Pour Floor Full Heal'},
    ]

    # Protect all interactive lanes, bridge crossings, ladders & chutes
    for x in range(12, 17):
        for y in (4, 5, 6, 7, 10, 11, 12, 13, 16, 17, 18, 19, 24, 25):
            m.keep_clear.add((x, y))
    for e in E:
        ex, ey = e['at']
        m.keep_clear.add((ex, ey))
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            if m.inb(ex + dx, ey + dy):
                m.keep_clear.add((ex + dx, ey + dy))

    # ---- 3. Volcanic Foundry Machinery, Solid Signposts, Banners, Braziers, Bollards & Lighting ----
    # Real solid pf_signposts for BOTH puzzle plaques (solid pas=0xf base -> over_trigger? == false!)
    _place_stamp_over(m, 'pf_signpost', 7, 21, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'pf_signpost', 8, 7, base_z=1, top_z=2, top_rows=1, solid=True)

    _place_stamp_over(m, 'cv_frame', 13, 1, base_z=1, top_z=2, top_rows=1, solid=False)
    m.over.append((1, 14, 2, T_PDOOR_OPEN))
    _place_stamp_over(m, 'wr_ban_ash', 11, 2, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'wr_ban_ash', 17, 2, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'fw_brazier', 9, 3, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'fw_brazier', 19, 3, base_z=1, top_z=2, top_rows=1, solid=True)

    # Bridge abutment iron bollards framing all 3 castable spans (x=11 & x=17!)
    for by in (4, 7, 10, 13, 16, 19):
        for bx in (11, 17):
            if (bx, by) not in m.keep_clear:
                _place_stamp_over(m, 'lm_bollard', bx, by, base_z=1, top_z=1, top_rows=0, solid=True)

    # Industrial bellows, carts, weapon racks, braziers, wall sconces & banners!
    _place_stamp_over(m, 'cv_pump', 3, 7, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'wr_rack', 4, 15, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'cv_cart', 3, 21, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'fw_brazier', 6, 8, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'fw_brazier', 20, 8, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'fw_brazier', 8, 14, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'fw_brazier', 24, 15, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'fw_brazier', 10, 23, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'fw_brazier', 18, 23, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'wr_ban_ash', 10, 7, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'wr_ban_ash', 18, 7, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'wr_sacks', 24, 22, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'cv_tools', 10, 20, base_z=1, top_z=1, top_rows=0, solid=True)
    for sx, sy in ((6, 1), (10, 1), (18, 1), (22, 1)):
        m.over.append((2, sx, sy, P1('cv_walllamp')))

    # Steam plumes over flanking magma & cistern + mirror-symmetric amber fire glow halos!
    for sx, sy in ((6, 5), (21, 5), (6, 11), (21, 11), (6, 17), (21, 17), (24, 20)):
        _place_stamp_over(m, 'lm_steam0' if (sx + sy) % 2 == 0 else 'lm_steam1', sx, sy, base_z=2, top_z=2, top_rows=2, solid=False)
    for gx, gy in ((9, 3), (18, 3), (6, 8), (19, 8), (8, 14), (23, 15), (10, 23), (17, 23), (13, 2)):
        m.stamps.append(('pf_glow', gx, gy))
    m.stamps.append(('cv_shaft', 13, 2))

    m.paint()
    _paint_foundry_floors(m, [
        (3, 2, 25, 24, 'basalt'),
        (12, 2, 16, 4, 'iron'),
        (12, 7, 16, 10, 'iron'),
        (12, 13, 16, 16, 'iron'),
        (12, 19, 16, 25, 'iron'),
        (4, 19, 11, 23, 'ashlar'),
        (17, 19, 23, 23, 'ashlar'),
        # Crisp riveted-iron control station pads under K1-K3, Q1-Q3, and Chute C2 bay!
        (5, 19, 11, 19, 'iron'),
        (21, 19, 22, 21, 'iron'),
        (22, 7, 24, 9, 'iron'),
    ])
    # Solid 1-tile forged-iron channel abutment piers at x=11 and x=17 (pas=0xf) flanking X1, X2, X3!
    _paint_trough_curbs(m, (11, 17), (5, 6, 11, 12, 17, 18))
    # Visual circular wooden-rung ladder shafts at Ladder H (5,14) & North Ladder (23,3) (distinct from iron chute hatches!)
    m.L[1, 14, 5] = T_HOLE
    m.L[1, 3, 23] = T_HOLE

    Lr = RC.resolve(m.L, TID).astype(np.int32)
    ev_pts = [tuple(e['at']) for e in E]
    PG.guard(Lr, TID, ev_pts, 'Map 251')
    assert not PG.hits(Lr, R.tilesets()[TID], ev_pts), 'Map 251 passguard hits!'
    m.L = Lr

    head = {
        'id': 251,
        'name': 'Cindervault Gym - Puzzle Room 1',
        'parent': 250,
        'bgm': 'Gym',
        'field': FIELD,
        'map_audio': {'bgm': 'Gym - Warden Hall', 'bgs': 'Lava - Ashkaar', 'bgs_volume': 50, 'rain': False},
        'metadata': {'Name': 'Cindervault Gym', 'SnapEdges': True, 'MapPosition': CV_POS, 'BattleBack': 'cave1'},
        'tone': [24, 4, -18, 10],
        '_file': '251_cindervault_gym_251.yaml',
    }
    m.write(251, head, comment='# GENERATED by mapgen/layouts/cindervault_gym.py (Batch 3B): Cindervault Gym - Puzzle Room 1 (Pour Floor).\n'
                               '# Edit the layout script, not this file.\n')
    return m, Lr


# =================================================================================================
# MAP 252 — Cindervault Gym - Puzzle Room 2 ("Mould Floor — COMBINE + Mastery Vault", 29x27, TS 61)
# =================================================================================================
def build_252():
    W, H = 29, 27
    m = Cave(W, H, 'L', seed=252, pool='Magma', tid=TID)
    m.STAIRS = K.STAIRS_STONE
    K.KITS['cvH2'] = dict(K.KITS['cvH'], rows=[K.KITS['cvH']['rows'][0], K.KITS['cvH']['rows'][2]])
    m.kit = {TER: 'cvH2', FLOOR: 'cvH2', MASS: 'cvH2', 'default': 'cvH2'}

    # ---- 1. Sculpt Mirrored Sub-Foundry Mould Floor (WITH flush airtight bulkhead between West Vault & East C2 Bay!) ----
    # North Band (y=2..4, x=15..25 — receives M3 crossing and North Ladder (23,3) up to 251!)
    m.box(15, 2, 25, 4, FLOOR, '.')
    # Mould Pit M3 Chasm (y=5..6, x=19..25 -> solid curbs x=19 & x=25 frame M3 span x=20..24; ZERO 1-tile lava sliver!)
    m.box(19, 5, 25, 6, FLOOR, 'w')
    # Mid2 WEST: Cracked-Mould Mastery Vault (y=7..10, x=4..16)
    m.box(4, 7, 16, 10, FLOOR, '.')
    # Mid2 BULKHEAD SOUTH FACE (y=10, x=17..19): MASS ends at y=9 so 2-row cvH2 cliff lands FLUSH on y=9..10 (100% airtight, ZERO y=11 overhang!)
    m.box(17, 10, 19, 10, FLOOR, '.')
    # Mid2 EAST: Chute C2 Landing Bay (y=7..10, x=20..25 — directly below 251 C2 (23,8) and south of M3!)
    m.box(20, 7, 25, 10, FLOOR, '.')
    # Mould Pit M2 Chasm (y=11..12, x=3..25 — castable iron mould M2 spans x=12..16 into the West Mastery Vault!)
    m.box(3, 11, 25, 12, FLOOR, 'w')
    # Mid1 Gallery (y=13..16, x=3..25 — connects M1 to Ladder H (5,14) up to 251 Mid1 AND to M2 Vault!)
    m.box(3, 13, 25, 16, FLOOR, '.')
    # Mould Pit M1 Chasm (y=17..18, x=3..25 — castable iron mould M1 spans x=12..16!)
    m.box(3, 17, 25, 18, FLOOR, 'w')
    # South Mould Floor (y=19..24, x=3..25 — receives Chute C1 (14,23) & Ladder C1 up!)
    m.box(3, 19, 25, 24, FLOOR, '.')
    # Reserve 1-tile solid forged-iron channel abutment curbs flanking M1, M2 (x=11/17) and M3 (x=19/25)!
    for cy in (11, 12, 17, 18):
        for cx in (11, 17):
            m.cls[cy, cx] = '.'
    for cy in (5, 6):
        for cx in (19, 25):
            m.cls[cy, cx] = '.'

    m.mass_at([
        (15, 2), (25, 2), (4, 7), (16, 7), (25, 7),
        (3, 23), (3, 24), (4, 24), (25, 23), (25, 24), (24, 24),
    ])

    m.tidy()
    m.plan_cliffs(rows=2)

    # ---- 2. Events: Ladders up to 251, Castable Mould Pits M1/M2/M3, Mastery Chest, Reset Apprentice, Trainers ----
    E = m.events

    # Ladder C1 up to 251 South Band (14, 22) -> lands 251 (14, 23) down
    E.append({
        'type': 'warp',
        'name': 'Ladder C1 up to Pour Floor',
        'at': [14, 22],
        'to': {'map': 251, 'x': 14, 'y': 23, 'dir': 'down'},
        'se': 'Door enter',
    })
    # Ladder H up to 251 Mid1 (5, 14) -> lands 251 (6, 14) right
    E.append({
        'type': 'warp',
        'name': 'Ladder H up to Pour Floor',
        'at': [5, 14],
        'to': {'map': 251, 'x': 6, 'y': 14, 'dir': 'right'},
        'se': 'Door enter',
    })
    # Ladder C2 up to 251 Mid2 (23, 8) -> lands 251 (22, 8) left
    E.append({
        'type': 'warp',
        'name': 'Ladder C2 up to Pour Floor',
        'at': [23, 8],
        'to': {'map': 251, 'x': 22, 'y': 8, 'dir': 'left'},
        'se': 'Door enter',
    })
    # North Ladder up to 251 North Band (23, 3) -> lands 251 (22, 3) left (straight to Warden Arena Portal!)
    E.append({
        'type': 'warp',
        'name': 'North Ladder up to Arena Band',
        'at': [23, 3],
        'to': {'map': 251, 'x': 22, 'y': 3, 'dir': 'left'},
        'se': 'Door enter',
    })

    # Castable Mould Pit Events: M1 (x=12..16, y=17..18), M2 (x=12..16, y=11..12), M3 (x=20..24, y=5..6)
    for m_lbl, sw_id, xs, ys in (
        ('M1', S_M1, range(12, 17), (17, 18)),
        ('M2', S_M2, range(12, 17), (11, 12)),
        ('M3', S_M3, range(20, 25), (5, 6)),
    ):
        for y in ys:
            for x in xs:
                E.append(_mould_tile_event(f'{m_lbl} {x},{y}', x, y, sw_id, T_IRON_PLATE))

    # MASTERY VAULT CHEST ("forge to break right", GYM_PUZZLES.md lines 1049-1055!)
    vault_ruby = (
        'pbSEPlay("Mining reveal", 95, 100)\n'
        'pbMessage(_INTL("The cracked iron mould split cleanly under the pour, revealing a recessed stone coffer!"))\n'
        'pbMessage(_INTL("Engraved on a blackened iron smithing hammer inside: \'BRANN HOLLOWAY — AF 280 FESTIVAL MATCH vs. VALEN. SOME THINGS YOU FORGE TO BREAK RIGHT.\'"))\n'
        'pbReceiveItem(:ELEMENTALSEED, 2)\n'
        'pbReceiveItem(:CHARCOAL, 1)\n'
        f'$game_switches[{S_VAULT_DONE}] = true\n'
        '$game_map.need_refresh = true'
    )
    E.append({
        'type': 'event',
        'name': 'Cracked-Mould Mastery Hoard',
        'at': [10, 8],
        'pages': [
            {
                'graphic': {'sprite': 'Object ball', 'dir': 'down'},
                'trigger': 'action',
                'commands': [{'script': vault_ruby}, {'selfswitch': ['A', True]}],
            },
            {
                'cond': {'self': 'A'},
                'commands': [],
            },
        ],
    })

    # Safety Mould-Runner Apprentice on 252 South Band (lets player reset straight back to 251 anytime!)
    runner_ruby = (
        'c = pbMessage(_INTL("Mould-Runner: Down here we catch whatever Brann\'s crucibles didn\'t quench upstairs. Want me to clear the moulds and send you back to the Pour Floor?"),\n'
        '              [_INTL("Reset foundry & return upstairs"), _INTL("Leave it")], 2)\n'
        'if c == 0\n'
        f'  {_reset_foundry_ruby(True).replace(chr(10), chr(10) + "  ")}\n'
        'end'
    )
    E.append({
        'type': 'event',
        'name': 'Mould-Runner Apprentice',
        'at': [18, 22],
        'pages': [{
            'graphic': {'sprite': 'NPC 14', 'dir': 'left'},
            'trigger': 'action',
            'move': 'fixed',
            'commands': [{'script': runner_ruby}],
        }],
    })

    # Canonical PBS Trainers for Map 252 (pbs/trainers.txt:15878 & 15927 — 0 duplicates!)
    E.append(_trainer(
        (8, 21), 'ENGINEER', 'Oda', 'right',
        "Foundry Engineer Oda: Molten iron drops down here like rain! Let's see if you stay cool under the moulds!",
        "Foundry Engineer Oda: The forge wants an hour to cool. So do I.",
        sight=3,
    ))
    E.append(_trainer(
        (18, 3), 'COOLTRAINER_M', 'Dain', 'right',
        "Ace Trainer Dain: You cast M3 and made it all the way to the north climb! One last temper before Warden Brann!",
        "Ace Trainer Dain: Brann doesn't talk much. He'll let the forge do it.",
        sight=3,
    ))

    # Plaques (backed by real solid pf_signposts!)
    E += [
        _sign('Cracked-Mould Plaque', (7, 8),
              "BRANN'S APPRENTICE VAULT — 'A mould that breaks on the seam frees the blade inside. Drain X2 unquenched to split the stone.'"),
        _sign('Mould Floor Notice', (11, 22),
              "MOULD FLOOR (SUB-LEVEL): Mould M1 links to Ladder H (west) · Mould M2 opens Brann's Cracked-Mould Vault · Mould M3 crosses from Chute C2 to the North Ladder."),
    ]

    for x in range(12, 17):
        for y in (10, 11, 12, 13, 16, 17, 18, 19):
            m.keep_clear.add((x, y))
    for x in range(20, 25):
        for y in (4, 5, 6, 7):
            m.keep_clear.add((x, y))
    for e in E:
        ex, ey = e['at']
        m.keep_clear.add((ex, ey))
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            if m.inb(ex + dx, ey + dy):
                m.keep_clear.add((ex + dx, ey + dy))

    # ---- 3. Sub-Foundry Mould Architecture, Solid Signposts, Cracked Cradle, Vault Candelabras & Lighting ----
    # Real solid pf_signposts for BOTH 252 puzzle plaques (solid pas=0xf base -> over_trigger? == false!)
    _place_stamp_over(m, 'pf_signpost', 7, 7, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'pf_signpost', 11, 21, base_z=1, top_z=2, top_rows=1, solid=True)

    _place_stamp_over(m, 'lm_cradle_cracked', 10, 7, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'fw_brazier', 6, 8, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'fw_brazier', 14, 8, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'mn_candelabra', 8, 7, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'mn_candelabra', 12, 7, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'wr_ban_ash', 5, 7, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'wr_ban_ash', 15, 7, base_z=1, top_z=2, top_rows=2, solid=True)

    # Symmetric iron mould bollards framing M1, M2 south lip & M3 north lip (orphan (11,10) removed!)
    for bx, by in ((11, 13), (17, 13), (11, 16), (17, 16), (11, 19), (17, 19), (19, 4), (25, 4)):
        if m.inb(bx, by) and m.cls[by, bx] == '.' and (bx, by) not in m.keep_clear:
            _place_stamp_over(m, 'lm_bollard', bx, by, base_z=1, top_z=1, top_rows=0, solid=True)

    # Sub-foundry slag carts, chains, tool racks, braziers, magma steam & mirror-symmetric fire glows!
    _place_stamp_over(m, 'fw_brazier', 16, 3, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'fw_brazier', 21, 9, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'fw_brazier', 8, 14, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'fw_brazier', 21, 14, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'fw_brazier', 6, 22, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'fw_brazier', 22, 22, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'cv_cart', 23, 14, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'cv_tools', 23, 21, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'wr_sacks', 4, 21, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'hb_barrels', 4, 15, base_z=1, top_z=2, top_rows=1, solid=True)
    for sx, sy in ((6, 17), (22, 17), (6, 11), (21, 11)):
        _place_stamp_over(m, 'lm_steam0' if (sx + sy) % 2 == 0 else 'lm_steam1', sx, sy, base_z=2, top_z=2, top_rows=2, solid=False)

    for gx, gy in ((6, 8), (13, 8), (8, 14), (20, 14), (6, 22), (21, 22)):
        m.stamps.append(('pf_glow', gx, gy))
    m.stamps.append(('cv_shaft', 9, 7))

    m.paint()
    _paint_foundry_floors(m, [
        (3, 2, 25, 24, 'soot'),
        (12, 13, 16, 16, 'ashlar'),
        (12, 19, 16, 24, 'ashlar'),
        (5, 8, 15, 10, 'ashlar'),
        (20, 7, 25, 10, 'ashlar'),
        (16, 2, 24, 4, 'ashlar'),
    ])
    # Solidify bulkhead interior mass pixels so (17..19, 5..8) reads as monolithic dark obsidian with zero light-cobble sliver!
    for mx, my in ((18, 7), (18, 8), (17, 6)):
        m.L[0, my, mx] = P1('L_m3a')
    # Solid forged-iron channel abutment piers separating magma moats from M1, M2 (x=11/17) & M3 (x=19/25)!
    _paint_trough_curbs(m, (11, 17), (11, 12, 17, 18))
    _paint_trough_curbs(m, (19, 25), (5, 6))
    # Paint M1, M2, M3 castable spans on L[0] with 3D recessed forged-iron & dark volcanic slag mould beds (pas=0xf, pri=0)!
    for xs, ys in ((range(12, 17), (17, 18)), (range(12, 17), (11, 12)), (range(20, 25), (5, 6))):
        x0, x1 = xs.start, xs.stop - 1
        for y in ys:
            for x in xs:
                m.L[0, y, x] = _trough_tile_for(x, x0, x1, y == ys[0])
                m.L[1, y, x] = 0
                m.L[2, y, x] = 0
    # Visual circular wooden-rung ladder shafts at C1 (14,22), H (5,14), C2 (23,8), North Ladder (23,3)
    for lx, ly in ((14, 22), (5, 14), (23, 8), (23, 3)):
        m.L[1, ly, lx] = T_HOLE

    Lr = RC.resolve(m.L, TID).astype(np.int32)
    ev_pts = [tuple(e['at']) for e in E]
    PG.guard(Lr, TID, ev_pts, 'Map 252')
    assert not PG.hits(Lr, R.tilesets()[TID], ev_pts), 'Map 252 passguard hits!'
    m.L = Lr

    head = {
        'id': 252,
        'name': 'Cindervault Gym - Puzzle Room 2',
        'parent': 250,
        'bgm': 'Gym',
        'field': FIELD,
        'map_audio': {'bgm': 'Gym - Warden Hall', 'bgs': 'Lava - Ashkaar', 'bgs_volume': 55, 'rain': False},
        'metadata': {'Name': 'Cindervault Gym', 'SnapEdges': True, 'MapPosition': CV_POS, 'BattleBack': 'cave1'},
        'tone': [10, -6, -24, 16],
        '_file': '252_cindervault_gym_252.yaml',
    }
    m.write(252, head, comment='# GENERATED by mapgen/layouts/cindervault_gym.py (Batch 3B): Cindervault Gym - Puzzle Room 2 (Mould Floor).\n'
                               '# Edit the layout script, not this file.\n')
    return m, Lr


# =================================================================================================
# MAP 253 — Cindervault Gym - Warden Arena (Brann Holloway, 21x19, TS 61, VOLCANIC)
# =================================================================================================
def build_253():
    W, H = 21, 19
    m = Cave(W, H, 'L', seed=253, pool='Magma', tid=TID)
    m.STAIRS = K.STAIRS_STONE
    K.KITS['cvH2'] = dict(K.KITS['cvH'], rows=[K.KITS['cvH']['rows'][0], K.KITS['cvH']['rows'][2]])
    m.kit = {TER: 'cvH2', FLOOR: 'cvH2', MASS: 'cvH2', 'default': 'cvH2'}

    # ---- 1. Sculpt Dramatic Octagonal Volcanic Casting Floor Ring Over Blazing Magma Chasm ----
    # Outer magma chasm rim (x=2..18, y=3..16)
    m.box(2, 3, 18, 16, FLOOR, 'w')
    # Elevated North Warden Dais (TER, x=7..13, y=3..8 — flush with north wall y=2..3 -> ZERO black void bar!)
    m.box(7, 3, 13, 8, TER, '.')
    # Central Octagonal Iron Casting Ring (FLOOR, x=6..14, y=9..15)
    m.box(6, 9, 14, 15, FLOOR, '.')
    m.box(5, 10, 15, 14, FLOOR, '.')
    # East Fast-Exit Foundry Lift Pier (x=15..17, y=14..16)
    m.box(15, 14, 17, 16, FLOOR, '.')
    # South Approach Causeway (x=8..12, y=15..17)
    m.box(8, 15, 12, 17, FLOOR, '.')

    # Sculpted basalt corners into black void
    m.mass_at([
        (2, 3), (3, 3), (2, 4), (18, 3), (17, 3), (18, 4),
        (2, 15), (2, 16), (3, 16), (18, 16),
    ])

    # 3-wide stone stair descending from Brann's Elevated Dais (TER lip y=8, base y=9 -> lands y=10)
    m.stairs(9, 8, w=3, n=2, c='.')

    m.tidy()
    m.plan_cliffs(rows=2)

    # ---- 2. Events: Return Warp to 251, Fast-Exit Lift to 250, Warden Brann Battle! ----
    E = m.events

    # South Return Warps -> 251 North Band (14, 3, down)
    for rx in (9, 10, 11):
        E.append({
            'type': 'warp',
            'name': 'Back to Pour Floor (251)',
            'at': [rx, 17],
            'to': {'map': 251, 'x': 14, 'y': 3, 'dir': 'down'},
            'se': 'Door exit',
        })

    # Fast-Exit Foundry Lift -> straight back to 250 Gate Hall (12, 21, down)!
    E.append({
        'type': 'warp',
        'name': 'Fast-Exit Lift to Entrance (250)',
        'at': [16, 15],
        'to': {'map': 250, 'x': 12, 'y': 21, 'dir': 'down'},
        'se': 'Door slide',
    })
    E.append(_sign('Foundry Lift Sign', (16, 14),
                   "FOUNDRY FAST-EXIT LIFT — Step onto the bolted steel lift plate directly below to ride straight back to the Gym Entrance!"))

    # WARDEN BRANN HOLLOWAY (story/29_SCRIPT_CH8.md lines 214-233 + GYM_PUZZLES.md S339 Mastery reaction!)
    brann_battle_ruby = f'''pbMessage(_INTL("Brann: Some things you forge to last."))
pbMessage(_INTL("Brann: Some things you forge to BREAK right. That's the harder craft. Took me thirty years to learn the second one."))
pbMessage(_INTL("Brann: Let's see which one you are!"))
if Prismfall.gym_battle(pfm_gym(:LEADER_BRANN), double: false)
  pbMessage(_INTL("Brann: HA! Broke me right! That's the harder craft!"))
  Prismfall.award_badge(pfm_gym(:LEADER_BRANN))
  pbSEPlay("Anim/HealBell", 90, 100)
  pbMessage(_INTL("Seven clear notes ring out as the Quench Badge settles in. A thin, bright light runs along every seam of your badge case."))
  pbMessage(_INTL("Brann: ...Your case sings. Huh. Don't let Imelda take it apart."))
  pbReceiveItem(:TM35)
  pbMessage(_INTL("Brann: Flamethrower — honest heat, no tricks. And the Quench Badge: quench is the moment a blade decides what it's going to be. Too slow, it's soft. Too fast, it cracks."))
  if $game_switches[{S_VAULT_DONE}]
    pbMessage(_INTL("Brann: Ha! And I hear you found my cracked mould down in the vault too! Aye — some things you break ON PURPOSE."))
  end
  $game_variables[129] = 5 if $game_variables[129].to_i < 5
  $game_self_switches[[253, @event_id, "A"]] = true
  $game_map.need_refresh = true
end'''
    brann_after_ruby = f'''if $game_switches[{S_VAULT_DONE}]
  pbMessage(_INTL("Brann: Ha! Found the cracked one down in the Mould Floor, did you? Aye — some things you break on purpose."))
end
pbMessage(_INTL("Brann: You earned the Quench Badge clean and honest! Take the east Foundry Lift if you want a quick ride back to the lobby."))'''

    E.append({
        'type': 'event',
        'name': 'Warden Brann',
        'at': [10, 6],
        'pages': [
            {
                'graphic': {'sprite': 'BRANN', 'dir': 'down'},
                'trigger': 'action',
                'move': 'fixed',
                'commands': [{'script': brann_battle_ruby}],
            },
            {
                'cond': {'self': 'A'},
                'graphic': {'sprite': 'BRANN', 'dir': 'down'},
                'trigger': 'action',
                'move': 'fixed',
                'commands': [{'script': brann_after_ruby}],
            },
        ],
    })

    # Protect center runway, Brann, stairs, return warp & lift
    for y in range(6, 18):
        for x in (9, 10, 11):
            m.keep_clear.add((x, y))
    for p in ((15, 14), (15, 15), (16, 15), (16, 14), (17, 15), (14, 14), (14, 15)):
        m.keep_clear.add(p)

    # ---- 3. Monumental Volcanic Casting-Floor Architecture, Framed Lift Bay, Banners & Lighting ----
    _place_stamp_over(m, 'fw_brazier', 7, 4, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'fw_brazier', 13, 4, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'wr_ban_ash', 8, 4, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'wr_ban_ash', 12, 4, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'lm_gearbox', 7, 7, base_z=1, top_z=1, top_rows=0, solid=True)    # Brann's anvil
    _place_stamp_over(m, 'cv_tools', 13, 7, base_z=1, top_z=1, top_rows=0, solid=True)
    for sx, sy in ((8, 2), (10, 2), (12, 2)):
        m.over.append((2, sx, sy, P1('cv_walllamp')))

    # Fast-Exit Foundry Lift Bay: solid steel elevator hatch door lm_sdoor at (16, 13..14) (pas=0xf at (16,14)!) + bollards!
    _place_stamp_over(m, 'lm_sdoor', 16, 13, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'lm_bollard', 17, 14, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'lm_bollard', 17, 16, base_z=1, top_z=1, top_rows=0, solid=True)

    # Mirror-symmetric corner braziers, bollards & weapon racks framing the Octagonal Casting Floor Ring!
    for bx, by in ((6, 10), (14, 10), (6, 13), (14, 13)):
        _place_stamp_over(m, 'fw_brazier', bx, by, base_z=1, top_z=2, top_rows=1, solid=True)
    for bx, by in ((8, 16), (12, 16)):
        _place_stamp_over(m, 'lm_bollard', bx, by, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'wr_rack', 5, 11, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'wr_rack', 15, 11, base_z=1, top_z=2, top_rows=1, solid=True)

    # Magma steam plumes rising strictly over magma + mirror-symmetric fire glow halos!
    for sx, sy in ((3, 7), (17, 7), (3, 12), (17, 11)):
        _place_stamp_over(m, 'lm_steam0' if (sx + sy) % 2 == 0 else 'lm_steam1', sx, sy, base_z=2, top_z=2, top_rows=2, solid=False)
    for gx, gy in ((7, 4), (12, 4), (6, 10), (13, 10), (6, 13), (13, 13)):
        m.stamps.append(('pf_glow', gx, gy))
    m.stamps.append(('cv_shaft', 9, 5))

    m.paint()
    _paint_foundry_floors(m, [
        (7, 4, 13, 8, 'iron'),
        (5, 10, 15, 15, 'basalt'),
        (7, 10, 13, 14, 'ashlar'),
        (8, 15, 12, 17, 'iron'),
        (15, 14, 17, 16, 'iron'),
    ])
    # Battle ring iron-grate inlay & bolted steel Fast-Exit Lift deck pad (distinct from decorative ring grates!)
    for rx in range(8, 13):
        for ry in (10, 14):
            if m.cls[ry, rx] == '.' and m.L[1, ry, rx] == 0:
                m.L[1, ry, rx] = T_IRON_GRATE
    for ry in (11, 12, 13):
        for rx in (7, 13):
            if m.cls[ry, rx] == '.' and m.L[1, ry, rx] == 0:
                m.L[1, ry, rx] = T_IRON_GRATE
    _paint_crimson_runner(m, 9, 15, 11, 17)
    m.L[1, 15, 16] = T_CHUTE

    Lr = RC.resolve(m.L, TID).astype(np.int32)
    ev_pts = [tuple(e['at']) for e in E]
    PG.guard(Lr, TID, ev_pts, 'Map 253')
    assert not PG.hits(Lr, R.tilesets()[TID], ev_pts), 'Map 253 passguard hits!'
    m.L = Lr

    _sim_bfs(Lr, E, (10, 16), [
        ('Return -> 251', (10, 17), False),
        ('Fast-Exit Lift -> 250', (16, 15), False),
        ('Lift Sign', (16, 14), True),
        ('Warden Brann', (10, 6), True),
    ], 'Map 253 Warden Arena')

    head = {
        'id': 253,
        'name': 'Cindervault Gym - Warden Arena',
        'parent': 250,
        'bgm': 'Gym',
        'field': FIELD,
        'map_audio': {'bgm': 'Gym - Warden Hall', 'bgs': 'Lava - Ashkaar', 'bgs_volume': 55, 'rain': False},
        'metadata': {'Name': 'Cindervault Gym', 'SnapEdges': True, 'MapPosition': CV_POS, 'BattleBack': 'cave1'},
        'tone': [26, 4, -20, 12],
        '_file': '253_cindervault_gym_253.yaml',
    }
    m.write(253, head, comment='# GENERATED by mapgen/layouts/cindervault_gym.py (Batch 3B): Cindervault Gym - Warden Arena (Brann).\n'
                               '# Edit the layout script, not this file.\n')
    return m, Lr


# =================================================================================================
# Cross-Floor Puzzle Verification (251 <-> 252 Exact Mechanics & Anti-Leak Proof!)
# =================================================================================================
def verify_gym7_puzzle(m251, L251, m252, L252):
    """Prove 251 + 252 puzzle is airtight, solvable by canonical route, AND Mastery Vault reachable!"""
    # 1. Start state: S band reachable, Arena Portal (14,2) SEALED!
    s0 = _sim_bfs(L251, m251.events, (14, 24), [
        ('Exit -> 250', (14, 25), False),
        ('Crucible K1', (5, 19), True),
        ('Crucible K2', (8, 19), True),
        ('Crucible K3', (11, 19), True),
        ('Quench Q1', (21, 19), True),
        ('Quench Q2', (22, 20), True),
        ('Quench Q3', (21, 21), True),
        ('Chute C1', (14, 22), True),
        ('Apprentice Hessa', (18, 22), True),
        ('Trainer Garran', (17, 20), True),
        ('Schematic Sign', (7, 22), True),
    ], 'Map 251 (start)')
    assert (14, 2) not in s0, '251 LEAK: Arena Portal reachable in start state!'
    assert (23, 8) not in s0, '251 LEAK: Chute C2 reachable in start state!'

    # 2. Canonical Main Solution State: K3->X1, K1->X2, K2->X3 -> Quench X2 (V436=2) -> Drain C1 (M1=ON, M3=ON)!
    v_main = {V_X1: 0, V_X2: 2, V_X3: 0, V_QUENCH_DRY: 1}
    sw_main = {S_POUR_K1: True, S_POUR_K2: True, S_POUR_K3: True, S_M1: True, S_M2: False, S_M3: True}
    # Step A: On 252 S Band -> cross M1 -> reach Ladder H (5,14) & Trainer Oda!
    s252_a = _sim_bfs(L252, m252.events, (14, 23), [
        ('Ladder C1 up', (14, 22), False),
        ('Trainer Oda', (8, 21), True),
        ('Mould-Runner', (18, 22), True),
        ('Ladder H up', (5, 14), False),
    ], 'Map 252 (main step A: M1->H)', vars_=v_main, sw=sw_main)
    assert (10, 8) not in s252_a, '252 LEAK: Mastery Vault reachable without M2!'
    assert (23, 8) not in s252_a, '252 LEAK: East C2 bay reachable from Mid1!'

    # Step B: Climb Ladder H -> 251 Mid1 (6,14) -> battle Ivar, grab Full Heal -> cross X2 -> reach Chute C2 (23,8)!
    s251_b = _sim_bfs(L251, m251.events, (6, 14), [
        ('Ladder H down', (5, 14), False),
        ('Trainer Ivar', (19, 14), True),
        ('Full Heal', (23, 14), True),
        ('Upper Chute Plaque', (8, 8), True),
        ('Chute C2', (23, 8), True),
    ], 'Map 251 (main step B: H->X2->C2)', vars_=v_main, sw=sw_main)
    assert (14, 2) not in s251_b, '251 LEAK: Arena Portal reachable from Mid2 without X3/M3!'

    # Step C: Drop Chute C2 -> 252 East Bay (23,9) -> cross M3 -> battle Dain -> reach North Ladder (23,3)!
    _sim_bfs(L252, m252.events, (23, 9), [
        ('Ladder C2 up', (23, 8), False),
        ('Trainer Dain', (18, 3), True),
        ('North Ladder up', (23, 3), False),
    ], 'Map 252 (main step C: C2->M3->North)', vars_=v_main, sw=sw_main)

    # Step D: Climb North Ladder -> 251 North Band (22,3) -> reach Warden Arena Portal (14,2)!
    _sim_bfs(L251, m251.events, (22, 3), [
        ('North Ladder down', (23, 3), False),
        ('Warden Arena Portal (253)', (14, 2), False),
    ], 'Map 251 (main step D: North->253)', vars_=v_main, sw=sw_main)

    # 3. Mastery Vault Proof: Drain X1 & X2 unquenched -> M1=ON, M2=ON -> reach Cracked-Mould Hoard (10,8), STILL isolated from East C2 Bay!
    sw_mast = {S_M1: True, S_M2: True, S_M3: False}
    s252_m = _sim_bfs(L252, m252.events, (14, 23), [
        ('Cracked-Mould Mastery Hoard', (10, 8), True),
        ('Cracked-Mould Plaque', (7, 8), True),
    ], 'Map 252 (Mastery M1+M2 -> Vault)', vars_={}, sw=sw_mast)
    assert (23, 9) not in s252_m and (23, 3) not in s252_m, '252 BULKHEAD LEAK: Mastery Vault leaked into East C2 bay!'
    print('GYM 7 PUZZLE PROOF PASSED: Main route solvable, Mastery Vault isolated & solvable, ZERO leaks!')


def main():
    build_250()
    m251, L251 = build_251()
    m252, L252 = build_252()
    build_253()
    verify_gym7_puzzle(m251, L251, m252, L252)
    print('Done: wrote Cindervault Gym 7 specs & raw maps (250, 251, 252, 253).')


if __name__ == '__main__':
    main()
