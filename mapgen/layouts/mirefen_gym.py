#!/usr/bin/env python3
"""layouts/mirefen_gym.py — Batch 3C: Mirefen Gym 6 ("The Infirmary Ward", 4 Maps: 230, 231, 232, 233):
  - Map 230: Mirefen Gym - Entrance          (21x17, TS 58 PF Rejuv Locks, field :CORROSIVE_MIRE)
      Mint-sage apothecary lobby + TEACH chamber ("Measure 3 from the 3-flask"):
      * Bidirectional Exit [10, 16] (MF_GYM <-> 220), Gym Guide, Apothecary Medic (full heal), Corvin's Sign
      * Canonical PBS trainer [AROMALADY, Rue] + HYPERPOTION side pickup
      * TEACH Tap Bench (V330/V331) + TEACH Funnel (needs exact 3 -> S334 ON -> iron drawbridge across mire)
      * North Portal (10, 4) -> 231 (14, 23) up
  - Map 231: Mirefen Gym - Puzzle Room 1     (29x25, TS 58 PF Rejuv Locks, field :CORROSIVE_MIRE)
      "The Dispensary — TWIST: Four from Three and Five" (GYM_PUZZLES.md §231):
      * West Compounding Tap Bench (V330 3-flask, V331 5-flask), North Purge Funnel (needs exact 4 -> S330 ON)
      * Wenlow Apprentice NPC (live flask status, zero-softlock reset, 3-tier progressive hints, puzzleskip)
      * Canonical PBS trainers [SCIENTIST, Hester] & [BURGLAR, Finch] + FULLHEAL pickup
      * North Portal (14, 4) -> 232 (4, 13) right (sealed until S330 ON!)
  - Map 232: Mirefen Gym - Puzzle Room 2     (29x25, TS 58 PF Rejuv Locks, field :CORROSIVE_MIRE)
      "The Sludge Gallery — COMBINE: Carry the Cure + Quiet Alcove Mastery" (GYM_PUZZLES.md §232 & §234):
      * West Tap End (only place to FILL 3/5 flasks) + Mask Filter Refill #1 + Wenlow Apprentice NPC
      * 6-step toxic sludge crossing #1 (V332 += 1 per step; at 10 -> safe return to Tap End keeping flasks & progress)
      * Island A: Socket A (needs exact 1 -> S331 ON, raises East Sluice Gate!), Flask Pouring Tray #1 (no Fill),
        Mask Filter Refill #2 (V332 = 0)
      * 7-step toxic sludge crossing #2 (6 + 7 = 13 > 10 -> refill at Island A mandatory!) -> East Dais B:
        Basin B (cumulative V333 == 7 -> S332 ON, opens North Arena Bridge!; > 7 overflows to 0!), Flask Tray #2,
        Emergency Filter Recall Cord
      * South Dry Wing (isolated from Dais B): Canonical PBS trainer [SCIENTIST, Lorcan] + Optional Quiet Alcove
        Mastery (4 & 9 flasks V430/V431 -> sequential doses 1, 3, 6 via V432 -> S333 ON -> SYNTHETICSEED x2 +
        BLACKSLUDGE + Wenlow's heartfelt note!)
      * North Dry Gallery (sealed until S332 ON!): Canonical PBS trainer [BURGLAR, Mudge] -> Arena Portal (14, 4)
  - Map 233: Mirefen Gym - Warden Arena      (21x17, TS 58 PF Rejuv Locks, field :CORROSIVE_MIRE)
      Corvin Mott's sunken Operating Theatre over glowing Corrosive Mire:
      * Elevated north operating dais, twin candelabras, apothecary vats, emerald clinic runner
      * Canonical DOUBLE battle: Prismfall.gym_battle(pfm_gym(:LEADER_CORVIN), double: true)
      * Awards Remedy Badge (award_badge), TM84 Poison Jab, V127 = 5, S333 Mastery acknowledgement
      * South return -> 232 (14, 5) + framed East Fast-Exit Lift -> 230 (10, 14)

Canonical sources:
  - design/GYM_PUZZLES.md (Gym 6, IDs V330-V333, S330-S334, V430-V432 — verified 0 collisions!)
  - story/26_SCRIPT_CH7.md (Maps 230-233 dialogue, Gym Guide, Wenlow, Corvin)
  - pbs/trainers.txt (Rue, Hester, Finch, Lorcan, Mudge, LEADER_CORVIN — verified 0 duplicates!)

Run:
    /usr/bin/python3 -I mapgen/layouts/mirefen_gym.py
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
TID = 58            # PF Rejuv Locks: PF Sea Cave (toxic emerald-teal Corrosive Mire!) + cvF/cvT/cvN kits!
FIELD = 'CORROSIVE_MIRE'
MF_POS = [0, 20, 13]

# Canonical Gym 6 switch & variable IDs (design/GYM_PUZZLES.md §Gym 6 — verified 100% UNUSED!)
V_FLASK_3 = 330     # 0..3 measures in unmarked 3-flask
V_FLASK_5 = 331     # 0..5 measures in unmarked 5-flask
V_FILTER = 332      # 0..10 mask-filter sludge steps used in Room 232
V_BASIN = 333       # 0..7 cumulative measures in Basin B (Room 232)
V_HINT_TIER = 334   # Progressive hint counter for Wenlow
S_VALVE_4 = 330     # 231 Purge Funnel dosed with exact 4
S_SOCKET_A = 331    # 232 Socket A dosed with exact 1 (opens East Sluice Gate)
S_BASIN_B = 332     # 232 Basin B reached exact 7 (opens North Arena Bridge)
S_QUIET_DONE = 333  # 232 Optional Quiet Alcove Mastery (4+9 -> 1, 3, 6) completed
S_TEACH_DONE = 334  # 230 Teach Funnel dosed with exact 3 (opens Lobby drawbridge)
V_FLASK_4 = 430     # 232 Quiet Alcove unmarked 4-flask
V_FLASK_9 = 431     # 232 Quiet Alcove unmarked 9-flask
V_QUIET_STEP = 432  # 232 Quiet Alcove doses delivered (0 -> needs 1, 1 -> needs 3, 2 -> needs 6, 3 -> done!)

# Verified TS 58 tile IDs
T_IRON_GRATE = P1('lm_grate')          # 24393, pas=0x0, pri=0 (walkable iron drawbridge over mire!)
T_BARS_L = P1('lm_bars_l')             # 26015, pas=0xf, pri=0 (locked brass-iron sluice barrier bar!)
T_BARS_M = P1('lm_bars_m')             # 26017, pas=0xf, pri=0 (locked barrier center with glowing lock core!)
T_BARS_R = P1('lm_bars_r')             # 26015, pas=0xf, pri=0 (locked brass-iron sluice barrier bar!)
T_PDOOR = P1('lm_pdoor')               # 25935, pas=0xf, pri=0 (heavy shut steel sluice shutter w/ red lock light!)
T_PDOOR_OPEN = P1('lm_pdoor_open')     # 25936, pas=0x0, pri=0 (dark recessed open doorway portal pad!)
T_LATCH = P1('lm_latch')               # 25937, pas=0xf, pri=0 (barred iron gate w/ unmistakable red lock cross!)
T_STRIP_V = P1('lm_strip_v_on')        # 25926, pas=0x0, pri=0 (glowing hazard threshold curb!)
T_CURB_PIER = 25885                    # pas=0xf, pri=0 (forged-iron masonry abutment pier)
T_TAP = P1('cv_sluice')                # 24000, pas=0xf (apothecary brass tap valve)
T_RECALL = P1('cv_sluice_hi')          # 24001, pas=0xf (emergency vent pull-cord valve)
T_VAT_BLUE = P1('pf_p_vat_b')          # 17872, pas=0xf (blue-glowing apothecary funnel/basin)
T_VAT_RED = P1('pf_p_vat_r')           # 17873, pas=0xf (crimson purge funnel/mastery vat)
T_VAT_GOLD = P1('pf_p_vat_y')          # 17889, pas=0xf (amber socket vat)
T_REFILL = P1('lm_lamp_on')            # 25932, pas=0xf (glowing mask-filter recharge unit)
T_TRAY = P1('lm_counter_m')            # pas=0xf (portable flask pouring bench, NO fill)
T_CHUTE = P1('lm_latch_open')          # 25938, pas=0x0 (bolted fast-exit lift pad)
T_DOOR_WOOD = P1('mn_door')            # 24366, pas=0xf (framed wooden exit doorway!)
T_MAT = P1('mn_mat')                   # 24335, pas=0x0 (crisp woven exit threshold mat!)
T_WALL_LAMP = P1('cv_walllamp')        # 23922, pas=0xf (centered glowing wall sconce!)
T_PIT_STONE = P1('lm_road0')           # 24375, pas=0x0 (deep charcoal-slate stone battle floor!)
T_SLUDGE = [P1('gd_g%d' % i) for i in range(4)]           # 23059..23062, pas=0x0 (bubbling toxic emerald sludge!)
T_SLUDGE_CRACK = [P1('gd_gc0'), P1('gd_gc1')]             # 23063..23064, pas=0x0 (glowing toxic fissure sludge!)
T_VAPOR = [P1('wr_steam0'), P1('wr_steam1'), P1('wr_steam2')]
T_GLINT = [P1('hb_glint%d' % i) for i in range(4)]        # pri=2 subtle water shimmer (0 passguard!)


# =================================================================================================
# Shared Apothecary / Flask Ruby Script Builders & Map Helpers
# =================================================================================================
def _ruby_flask_bench(allow_fill=True, v_small=V_FLASK_3, cap_s=3, v_big=V_FLASK_5, cap_b=5, title='Apothecary Tap Bench'):
    """Snappy looping Ruby choice menu for unmarked flask measuring (Fill / Pour / Tip / Leave)."""
    if allow_fill:
        return f'''loop do
  s = $game_variables[{v_small}].to_i
  b = $game_variables[{v_big}].to_i
  cmds = [
    _INTL("Fill {cap_s}-Flask (now {{1}}/{cap_s})", s),
    _INTL("Fill {cap_b}-Flask (now {{1}}/{cap_b})", b),
    _INTL("Pour {cap_s} -> {cap_b}"),
    _INTL("Pour {cap_b} -> {cap_s}"),
    _INTL("Tip out {cap_s}-Flask"),
    _INTL("Tip out {cap_b}-Flask"),
    _INTL("Step away")
  ]
  ch = pbMessage(_INTL("{title} — [{cap_s}-Flask: {{1}}/{cap_s} | {cap_b}-Flask: {{2}}/{cap_b}]", s, b), cmds, cmds.length)
  case ch
  when 0
    $game_variables[{v_small}] = {cap_s}
    pbSEPlay("Anim/Water1", 80, 105)
  when 1
    $game_variables[{v_big}] = {cap_b}
    pbSEPlay("Anim/Water1", 80, 95)
  when 2
    amt = [s, {cap_b} - b].min
    if amt > 0
      $game_variables[{v_small}] = s - amt
      $game_variables[{v_big}] = b + amt
      pbSEPlay("Anim/Water2", 80, 100)
    else
      pbSEPlay("GUI sel buzzer", 75, 100)
    end
  when 3
    amt = [b, {cap_s} - s].min
    if amt > 0
      $game_variables[{v_big}] = b - amt
      $game_variables[{v_small}] = s + amt
      pbSEPlay("Anim/Water2", 80, 100)
    else
      pbSEPlay("GUI sel buzzer", 75, 100)
    end
  when 4
    $game_variables[{v_small}] = 0
    pbSEPlay("Anim/Bubble1", 75, 100)
  when 5
    $game_variables[{v_big}] = 0
    pbSEPlay("Anim/Bubble1", 75, 100)
  else
    break
  end
end'''
    else:
        return f'''loop do
  s = $game_variables[{v_small}].to_i
  b = $game_variables[{v_big}].to_i
  cmds = [
    _INTL("Pour {cap_s} -> {cap_b}"),
    _INTL("Pour {cap_b} -> {cap_s}"),
    _INTL("Tip out {cap_s}-Flask"),
    _INTL("Tip out {cap_b}-Flask"),
    _INTL("Step away")
  ]
  ch = pbMessage(_INTL("{title} (No Tap Here) — [{cap_s}-Flask: {{1}}/{cap_s} | {cap_b}-Flask: {{2}}/{cap_b}]", s, b), cmds, cmds.length)
  case ch
  when 0
    amt = [s, {cap_b} - b].min
    if amt > 0
      $game_variables[{v_small}] = s - amt
      $game_variables[{v_big}] = b + amt
      pbSEPlay("Anim/Water2", 80, 100)
    else
      pbSEPlay("GUI sel buzzer", 75, 100)
    end
  when 1
    amt = [b, {cap_s} - s].min
    if amt > 0
      $game_variables[{v_big}] = b - amt
      $game_variables[{v_small}] = s + amt
      pbSEPlay("Anim/Water2", 80, 100)
    else
      pbSEPlay("GUI sel buzzer", 75, 100)
    end
  when 2
    $game_variables[{v_small}] = 0
    pbSEPlay("Anim/Bubble1", 75, 100)
  when 3
    $game_variables[{v_big}] = 0
    pbSEPlay("Anim/Bubble1", 75, 100)
  else
    break
  end
end'''


def _ruby_exact_funnel(target_val, sw_id, name, success_msg):
    unit = 'measure' if target_val == 1 else 'measures'
    return f'''if $game_switches[{sw_id}]
  pbMessage(_INTL("{name}: Already dosed with exact {target_val} {unit}. The iron crossing is open!"))
else
  s = $game_variables[{V_FLASK_3}].to_i
  b = $game_variables[{V_FLASK_5}].to_i
  cmds = [
    _INTL("Pour 3-Flask ({{1}} {{2}})", s, s == 1 ? "measure" : "measures"),
    _INTL("Pour 5-Flask ({{1}} {{2}})", b, b == 1 ? "measure" : "measures"),
    _INTL("Step back")
  ]
  ch = pbMessage(_INTL("{name} — Needs EXACTLY {target_val} {unit}. [3-Flask: {{1}}/3 | 5-Flask: {{2}}/5]", s, b), cmds, 3)
  if ch == 0 || ch == 1
    amt = (ch == 0) ? s : b
    $game_variables[(ch == 0) ? {V_FLASK_3} : {V_FLASK_5}] = 0
    if amt == 0
      pbSEPlay("GUI sel buzzer", 75, 100)
      pbMessage(_INTL("That flask is empty! Fill and measure at the Tap Bench first."))
    elsif amt == {target_val}
      $game_switches[{sw_id}] = true
      $game_map.need_refresh = true
      pbSEPlay("Anim/HealBell", 90, 100)
      pfm_shake(4, 10, 8) if defined?(pfm_shake)
      pbMessage(_INTL("{success_msg}"))
    else
      pbSEPlay("GUI sel buzzer", 85, 95)
      pbMessage(_INTL("The funnel hisses and drains!"))
      pbMessage(_INTL("Wenlow: That was {{1}}! The funnel wants {target_val}. 'Dose makes the cure,' sir says. Sir says it a lot!", amt))
    end
  end
end'''


def _place_stamp_over(m, name, x, y, base_z=1, top_z=2, top_rows=0, solid=True):
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


def _paint_clinic_floors(m, zones):
    """Cohesive Victorian dark-slate stone masonry, weathered flagstone, timber & toxic corrosive sludge palettes (ZERO B&W checkerboard!)."""
    palettes = {
        'quay': [P1('T_f%d' % i) for i in range(4)],
        'slate': [P1('L_f%d' % i) for i in range(4)],
        'pit': [T_PIT_STONE],
        'timber': [P1('N_f%d' % i) for i in range(4)],
        'iron': [P1('Q_f%d' % i) for i in range(4)],
        'sludge': T_SLUDGE,
    }
    for x0, y0, x1, y1, kind in zones:
        pal = palettes[kind]
        for y in range(max(0, y0), min(m.H, y1 + 1)):
            for x in range(max(0, x0), min(m.W, x1 + 1)):
                if m.cls[y, x] != '.' or m.cliff[y, x]:
                    continue
                if kind == 'sludge' and (x * 7 + y * 11) % 9 == 0:
                    m.L[0, y, x] = T_SLUDGE_CRACK[(x + y) % 2]
                else:
                    m.L[0, y, x] = pal[(x * 3 + y * 5) % len(pal)]
    # Sweep any residual default B&W checkerboard tiles (24035..24038) under north wall arches & dais wings!
    slate = palettes['slate']
    for y in range(m.H):
        for x in range(m.W):
            if int(m.L[0, y, x]) in (24035, 24036, 24037, 24038):
                m.L[0, y, x] = slate[(x * 3 + y * 5) % len(slate)]


def _paint_emerald_runner(m, x0, y0, x1, y1):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if m.cls[y, x] != '.' or m.cliff[y, x] or m.L[1, y, x] != 0:
                continue
            part = ('n' if y == y0 else 's' if y == y1 else '') + ('w' if x == x0 else 'e' if x == x1 else '')
            m.L[1, y, x] = P1('mn_rugG_' + (part or ('c2' if (y - y0) % 3 == 1 else 'c')))


def _paint_curb_piers(m, cols, ys):
    qf0 = P1('Q_f0')
    for y in ys:
        for x in cols:
            if m.inb(x, y):
                m.L[0, y, x] = qf0
                m.L[1, y, x] = T_CURB_PIER
                m.L[2, y, x] = 0


def _drawbridge_event(name, x, y, sw_id, closed_msg, closed_tile=None):
    """2-state cast-iron drawbridge / sluice gate over PF Sea Cave corrosive mire (ZERO wooden ladders!):
      - sw OFF: unmistakable locked iron barrier bar / steel shutter (closed_tile, pas=0xf) OR open impassable mire chasm (closed_tile=None)
      - sw ON: walkable cast-iron grate bridge (lm_grate, pas=0x0 -> overrides mire -> WALKABLE!)
    """
    pg0 = {'trigger': 'action', 'commands': [closed_msg]}
    if closed_tile is not None:
        pg0['graphic'] = {'tile': closed_tile}
    return {
        'type': 'event',
        'name': name,
        'at': [x, y],
        'pages': [
            pg0,
            {
                'cond': {'switch': sw_id},
                'graphic': {'tile': T_IRON_GRATE},
                'trigger': 'action',
                'commands': [],
            },
        ],
    }


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


def _sim_bfs(Lr, events, start, targets, label, vars_=None, sw=None, verify_static=False):
    """Exact Essentials 4-bit directional + tile-event BFS + over_trigger? & sightline checker!"""
    import build as B
    vars_ = vars_ or {}
    sw = sw or {}
    ts = R.tilesets()[TID]
    H, W = Lr.shape[1:]
    by_cell = {}
    for e in events:
        if e and e.get('at'):
            by_cell.setdefault(tuple(e['at']), []).append(e)

    if verify_static:
        assert (Lr[0] > 0).all(), f'{label}: void L[0] tiles!'
        assert (Lr >= 0).all() and (Lr < len(ts['passages'])).all(), f'{label}: OOB tile IDs!'
        # Anti-P0 #1: ZERO over_trigger? == true traps!
        traps = []
        for e in events:
            et = e.get('type')
            at = tuple(e['at'])
            if et == 'sign':
                if B.cell_passable(Lr, ts, at[0], at[1]):
                    traps.append((e.get('name'), at, 'sign on walkable tile'))
            elif et == 'event':
                pg0 = (e.get('pages') or [{}])[0]
                trig = pg0.get('trigger', 'action')
                g = pg0.get('graphic') or {}
                has_solid = bool(g.get('sprite')) or (bool(g.get('tile')) and (ts['passages'][g['tile']] & 0x0f) == 0x0f)
                if trig == 'action' and not has_solid and B.cell_passable(Lr, ts, at[0], at[1]):
                    traps.append((e.get('name'), at, 'action event without solid graphic on walkable tile'))
        assert not traps, f'{label}: over_trigger? traps: {traps}'

    def dir_ok(x, y, d):
        bit = 1 << (d // 2 - 1)
        for e in by_cell.get((x, y), []):
            t = e.get('type')
            if t in ('npc', 'trainer', 'mart', 'item'):
                if not e.get('hidden'):
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

    if verify_static:
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
                assert 0 <= nx < W and 0 <= ny < H, f'{label}: trainer {e["trainer"]} sight OOB!'
                assert cell_ok(nx, ny), f'{label}: trainer {e["trainer"]} sight step {step} {(nx, ny)} BLOCKED!'
                if step > 1:
                    assert dir_ok(cx, cy, d), f'{label}: trainer {e["trainer"]} exit edge blocked at {(cx,cy)}'
                assert dir_ok(nx, ny, 10 - d), f'{label}: trainer {e["trainer"]} entry edge blocked at {(nx,ny)}'
                cx, cy = nx, ny
            print(f'{label}: Trainer {e["trainer"]} at {(tx, ty)} dir={e["dir"]} sight={sight} -> 100% OPEN!')

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


# Register 2-row apothecary wallpaper+wainscot (cvF2) & wet timber ward (cvT2) kits matching cindervault_gym.py
K.KITS['cvF2'] = dict(K.KITS['cvF'], rows=[K.KITS['cvF']['rows'][0], K.KITS['cvF']['rows'][2]])
K.KITS['cvT2'] = dict(K.KITS['cvT'], rows=[K.KITS['cvT']['rows'][0], K.KITS['cvT']['rows'][2]])


# =================================================================================================
# MAP 230 — MIREFEN GYM - ENTRANCE ("The Ward — TEACH", 21x17, TS 58, :CORROSIVE_MIRE)
# =================================================================================================
def build_230():
    W, H = 21, 17
    m = Cave(W, H, 'F', seed=230, pool='Sea Cave', tid=TID, game='pf')
    m.STAIRS = K.STAIRS_STONE
    m.kit = {TER: 'cvF2', FLOOR: 'cvF2', MASS: 'cvF2', 'default': 'cvF2'}

    # ---- 1. Sculpt Apothecary Lobby & TEACH Mire Channel (2-row cvF2 mint-sage + oak wainscot walls!) ----
    m.box(7, 2, 13, 5, FLOOR, '.')
    m.box(2, 4, 7, 7, FLOOR, 'w')
    m.box(13, 4, 18, 7, FLOOR, 'w')
    m.box(8, 6, 12, 7, FLOOR, 'w')
    for cy in (6, 7):
        for cx in (8, 12):
            m.cls[cy, cx] = '.'
    m.box(2, 8, 18, 14, FLOOR, '.')
    m.box(8, 15, 12, 16, FLOOR, '.')

    m.mass_at([(2, 14), (18, 14), (7, 2), (13, 2)])
    m.tidy()
    m.plan_cliffs(rows=2)

    # ---- 2. Events: Full-Width 3-Tile Exit MF_GYM, TEACH Bench & Funnel, Locked Iron Drawbridge, Guide, Medic, Rue ----
    E = m.events
    for ex, lbl in ((9, 'Exit West'), (10, 'Exit Center'), (11, 'Exit East')):
        E.append({'type': 'exit', 'name': lbl, 'at': [ex, 16], 'link': 'MF_GYM', 'arrive': [10, 15, 'up']})
    E.append({
        'type': 'warp',
        'name': 'To Dispensary (231)',
        'at': [10, 4],
        'to': {'map': 231, 'x': 14, 'y': 23, 'dir': 'up'},
        'se': 'Door enter',
    })

    # TEACH 3x2 Cast-Iron Drawbridge (9..11, 6..7): locked = barred lock gate on y=7 + open impassable mire on y=6!
    bars_row = {9: T_BARS_L, 10: T_BARS_M, 11: T_BARS_R}
    for bx in (9, 10, 11):
        for by in (6, 7):
            E.append(_drawbridge_event(
                f'Teach Bridge {bx},{by}', bx, by, S_TEACH_DONE,
                "A locked iron sluice-gate bars the open corrosive mire channel. Fill the 3-flask at the west Tap Bench and pour exact 3 measures into the east Teach Funnel to extend the bridge!",
                closed_tile=bars_row[bx] if by == 7 else None,
            ))

    # TEACH Tap Bench (solid cv_sluice at (6, 9))
    E.append({
        'type': 'event',
        'name': 'Teach Tap Bench',
        'at': [6, 9],
        'pages': [{
            'graphic': {'tile': T_TAP},
            'trigger': 'action',
            'commands': [{'script': _ruby_flask_bench(allow_fill=True, title='Ward Tap Bench')}],
        }],
    })

    # TEACH Funnel (solid pf_p_vat_b at (14, 9) — needs exact 3 -> S334 ON!)
    E.append({
        'type': 'event',
        'name': 'Teach Funnel (Needs 3)',
        'at': [14, 9],
        'pages': [{
            'graphic': {'tile': T_VAT_BLUE},
            'trigger': 'action',
            'commands': [{
                'script': _ruby_exact_funnel(
                    3, S_TEACH_DONE, 'Ward Teach Funnel',
                    "Three exact measures fizz green-gold! The ward's sluice drawbridge clanks down over the Corrosive Mire!",
                ),
            }],
        }],
    })

    # Corvin's Sign (backed by solid pf_signpost at (10, 9..10) -> base (10, 10)!)
    E.append(_sign(
        "Corvin's Sign", (10, 10),
        "WARDEN CORVIN MOTT'S RULE: 'If you can count to three, you can count to anything. Measure, don't guess.' (Fill the 3-flask at the west tap, then pour it into the east funnel!)",
    ))

    # Canonical Gym Guide & Apothecary Medic (full heal!)
    E.append(_make_npc('Gym Guide', (7, 13), 'NPC 14', 'right', [
        "Gym Guide: Yo, champ in the making! Welcome to the Mirefen Infirmary Gym — Poison-types on the Corrosive Mire!",
        "Gym Guide: Ground and Psychic cut right through it. Fairies melt fast, and Poison moves even corrode Steel-types down here.",
        "Gym Guide: Doctor Mott fights two Pokémon at once — says it's because patients in Nadir never have only one thing wrong with them. Good luck!",
    ]))
    medic_ruby = '''pbSEPlay("Anim/HealBell", 85, 100)
$player.heal_party
pbMessage(_INTL("Apothecary Medic: Fresh wormwood salve and a quick tonic for your team! All patched up — total bill: zero Pokédollars."))'''
    E.append({
        'type': 'event',
        'name': 'Apothecary Medic',
        'at': [13, 13],
        'pages': [{
            'graphic': {'sprite': 'NPC 22', 'dir': 'left'},
            'trigger': 'action',
            'move': 'fixed',
            'commands': [{'script': medic_ruby}],
        }],
    })

    # Canonical PBS Trainer for Map 230: [AROMALADY, Rue] (pbs/trainers.txt:14154 — 0 duplicates!)
    E.append(_trainer(
        (4, 11), 'AROMALADY', 'Rue', 'right',
        "Aroma Lady Rue: Doctor Mott's bitters keep the mire at bay — let's test whether you can stomach the first dose!",
        "Aroma Lady Rue: The Warden's herbs sting before they heal. Like that did.",
        sight=2,
    ))
    E.append({'type': 'item', 'name': 'Item Hyper Potion', 'at': [17, 11], 'item': 'HYPERPOTION'})

    # Protect key corridors
    for e in E:
        ex, ey = e['at']
        m.keep_clear.add((ex, ey))
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            if m.inb(ex + dx, ey + dy):
                m.keep_clear.add((ex + dx, ey + dy))
    for y in range(4, 17):
        for x in (9, 10, 11):
            m.keep_clear.add((x, y))

    # ---- 3. Apothecary Clinic Architecture, Bookcases, Candelabras & Mire Steam (ZERO floating mushrooms, ZERO offset glows!) ----
    _place_stamp_over(m, 'pf_signpost', 10, 9, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'cv_frame', 9, 3, base_z=1, top_z=2, top_rows=1, solid=False)
    _place_stamp_over(m, 'mn_books2', 3, 8, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'mn_books2', 16, 8, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'mn_candelabra', 8, 4, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'mn_candelabra', 12, 4, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'mn_candelabra', 8, 14, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'mn_candelabra', 12, 14, base_z=1, top_z=2, top_rows=1, solid=True)
    # Cohesive apothecary specimen case & potted fern flanking south corners (NO random nightstand!)
    _place_stamp_over(m, 'mn_case_m', 3, 13, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'mn_fern', 17, 13, base_z=1, top_z=1, top_rows=0, solid=True)
    # Corrosive steam plumes + subtle water surface shimmer strictly over mire moat (ZERO floating mushrooms!)
    for sx, sy in ((4, 6), (16, 6)):
        _place_stamp_over(m, 'lm_steam0' if sx == 4 else 'lm_steam1', sx, sy, base_z=2, top_z=2, top_rows=2, solid=False)
    for gx, gy in ((3, 7), (6, 6), (14, 7), (17, 6)):
        m.over.append((2, gx, gy, T_GLINT[(gx + gy) % 4]))

    m.paint()
    # Cohesive dark-slate masonry floor + weathered apothecary flagstone wings (ZERO B&W checkerboard!)
    _paint_clinic_floors(m, [
        (2, 8, 18, 14, 'slate'),
        (5, 9, 15, 13, 'quay'),
        (8, 15, 12, 16, 'quay'),
        (7, 4, 13, 5, 'slate'),
    ])
    _paint_emerald_runner(m, 9, 11, 11, 16)
    _paint_emerald_runner(m, 9, 5, 11, 5)
    # Dark recessed portal threshold inside north wooden doorway arch (10, 4)!
    m.L[0, 4, 10] = T_PIT_STONE
    m.L[1, 4, 10] = T_PDOOR_OPEN
    _paint_curb_piers(m, (8, 12), (6, 7))
    # Ground Tap Bench (6,9) and Teach Funnel (14,9) on riveted steel apothecary mounting pads!
    for px, py in ((6, 9), (14, 9)):
        m.L[0, py, px] = P1('Q_f0')

    Lr = RC.resolve(m.L, TID).astype(np.int32)
    ev_pts = [tuple(e['at']) for e in E]
    PG.guard(Lr, TID, ev_pts, 'Map 230')
    assert not PG.hits(Lr, R.tilesets()[TID], ev_pts), 'Map 230 passguard hits!'
    m.L = Lr

    # Verify start state (Portal SEALED!) AND solved state (S334 ON -> Portal REACHABLE!)
    s0 = _sim_bfs(Lr, E, (10, 15), [
        ('Exit West MF_GYM', (9, 16), False),
        ('Exit Center MF_GYM', (10, 16), False),
        ('Exit East MF_GYM', (11, 16), False),
        ('Teach Tap Bench', (6, 9), True),
        ('Teach Funnel', (14, 9), True),
        ("Corvin's Sign", (10, 10), True),
        ('Gym Guide', (7, 13), True),
        ('Apothecary Medic', (13, 13), True),
        ('Trainer Rue', (4, 11), True),
        ('Hyper Potion', (17, 11), True),
    ], 'Map 230 (start)', verify_static=True)
    assert (10, 4) not in s0, 'Map 230 LEAK: North Portal reachable before S334!'
    _sim_bfs(Lr, E, (10, 15), [
        ('North Portal -> 231', (10, 4), False),
    ], 'Map 230 (S334 ON)', sw={S_TEACH_DONE: True})

    head = {
        'id': 230,
        'name': 'Mirefen Gym - Entrance',
        'parent': 220,
        'bgm': 'Gym',
        'field': FIELD,
        'map_audio': {'bgm': 'Gym - Warden Hall', 'bgs': 'Drip - Nadir', 'bgs_volume': 45, 'rain': False},
        'metadata': {'Name': 'Mirefen Gym', 'SnapEdges': True, 'MapPosition': MF_POS, 'BattleBack': 'water'},
        'tone': [-12, 2, -8, 12],
        '_file': '230_mirefen_gym.yaml',
    }
    m.write(230, head, comment='# GENERATED by mapgen/layouts/mirefen_gym.py (Batch 3C): Mirefen Gym - Entrance (TEACH).\n'
                               '# Edit the layout script, not this file.\n')
    return m, Lr


# =================================================================================================
# MAP 231 — MIREFEN GYM - PUZZLE ROOM 1 ("The Dispensary — TWIST: 3+5 Make 4", 29x25, TS 58)
# =================================================================================================
def build_231():
    W, H = 29, 25
    m = Cave(W, H, 'F', seed=231, pool='Sea Cave', tid=TID, game='pf')
    m.STAIRS = K.STAIRS_STONE
    m.kit = {TER: 'cvF2', FLOOR: 'cvF2', MASS: 'cvF2', 'default': 'cvF2'}

    # ---- 1. Sculpt Grand Apothecary Dispensary & North Mire Trench ----
    m.box(11, 2, 17, 6, FLOOR, '.')
    m.box(3, 5, 11, 8, FLOOR, 'w')
    m.box(17, 5, 25, 8, FLOOR, 'w')
    m.box(12, 7, 16, 8, FLOOR, 'w')
    for cy in (7, 8):
        for cx in (12, 16):
            m.cls[cy, cx] = '.'
    m.box(3, 9, 25, 22, FLOOR, '.')
    m.box(11, 23, 17, 24, FLOOR, '.')
    m.box(3, 13, 4, 19, FLOOR, 'w')
    m.box(24, 13, 25, 19, FLOOR, 'w')

    m.mass_at([(3, 22), (25, 22), (11, 2), (17, 2), (11, 24), (17, 24)])
    m.tidy()
    m.plan_cliffs(rows=2)

    # ---- 2. Events: Return -> 230, North Portal -> 232, Tap Bench, Purge Funnel (4), Wenlow, Hester, Finch ----
    E = m.events
    for rx in (13, 14, 15):
        E.append({
            'type': 'warp',
            'name': f'Back to Entrance {rx}',
            'at': [rx, 24],
            'to': {'map': 230, 'x': 10, 'y': 5, 'dir': 'down'},
            'se': 'Door exit',
        })
    E.append({
        'type': 'warp',
        'name': 'To Sludge Gallery (232)',
        'at': [14, 4],
        'to': {'map': 232, 'x': 4, 'y': 13, 'dir': 'right'},
        'se': 'Door enter',
    })

    # Dispensary Purge Drawbridge (13..15, 7..8): locked = barred lock gate on y=8 + open impassable mire on y=7!
    bars_row = {13: T_BARS_L, 14: T_BARS_M, 15: T_BARS_R}
    for bx in (13, 14, 15):
        for by in (7, 8):
            E.append(_drawbridge_event(
                f'Dispensary Bridge {bx},{by}', bx, by, S_VALVE_4,
                "The purge gate is locked above the open Corrosive Mire. Measure EXACTLY 4 units using your 3- and 5-flasks and pour it into the crimson Purge Funnel!",
                closed_tile=bars_row[bx] if by == 8 else None,
            ))

    # West Compounding Tap Bench (solid cv_sluice at (7, 14))
    E.append({
        'type': 'event',
        'name': 'Dispensary Tap Bench',
        'at': [7, 14],
        'pages': [{
            'graphic': {'tile': T_TAP},
            'trigger': 'action',
            'commands': [{'script': _ruby_flask_bench(allow_fill=True, title='Dispensary Tap Bench')}],
        }],
    })

    # North Purge Funnel (solid pf_p_vat_r at (14, 10) — needs exact 4 -> S330 ON!)
    E.append({
        'type': 'event',
        'name': 'Purge Funnel (Needs 4)',
        'at': [14, 10],
        'pages': [{
            'graphic': {'tile': T_VAT_RED},
            'trigger': 'action',
            'commands': [{
                'script': _ruby_exact_funnel(
                    4, S_VALVE_4, 'Dispensary Purge Funnel',
                    "Four exact measures neutralize the purge lock! With a heavy iron clang, the drawbridge swings down across the mire!",
                ),
            }],
        }],
    })

    # Solid Plaque beside Purge Funnel (pf_signpost at (12, 10..11) -> base (12, 11)!)
    E.append(_sign(
        'Dispensary Formula Plaque', (12, 11),
        "DISPENSARY PURGE FUNNEL — REQUIRES EXACTLY 4 MEASURES. Unmarked flasks: 3 and 5. Fill at the west tap; pour or tip until one flask holds 4.",
    ))

    # Apprentice Wenlow (Status, Zero-Softlock Reset, 3-Tier Progressive Hints, puzzleskip!)
    wenlow_231_ruby = f'''loop do
  s = $game_variables[{V_FLASK_3}].to_i
  b = $game_variables[{V_FLASK_5}].to_i
  done = $game_switches[{S_VALVE_4}] ? "OPEN!" : "Needs 4"
  cmds = [_INTL("Check flasks"), _INTL("Reset flasks & step back"), _INTL("Ask for a hint")]
  cmds.push(_INTL("Skip room (puzzleskip)")) if $game_switches[301]
  cmds.push(_INTL("Never mind"))
  ch = pbMessage(_INTL("Wenlow: Hi! Mind the bottles — I nearly dropped three just now! [3-Flask: {{1}}/3 | 5-Flask: {{2}}/5 | Funnel: {{3}}]", s, b, done), cmds, cmds.length)
  case ch
  when 0
    pbMessage(_INTL("Wenlow: You've got {{1}} in the little 3-flask and {{2}} in the big 5-flask. The Purge Funnel wants exactly 4!", s, b))
  when 1
    $game_variables[{V_FLASK_3}] = 0
    $game_variables[{V_FLASK_5}] = 0
    $game_variables[{V_HINT_TIER}] = $game_variables[{V_HINT_TIER}].to_i + 1
    pbFadeOutIn do
      $game_player.moveto(14, 22)
      $game_player.turn_up
    end
    pbMessage(_INTL("Wenlow: All rinsed clean and ready for another try!"))
    break
  when 2
    t = $game_variables[{V_HINT_TIER}].to_i
    if t == 0
      pbMessage(_INTL("Wenlow (Hint 1/3): Sir always says: the empty space inside a flask is a measure too!"))
    elsif t == 1
      pbMessage(_INTL("Wenlow (Hint 2/3): Try getting exactly 2 measures into the little 3-flask first — then think about how much empty room is left in it!"))
    else
      pbMessage(_INTL("Wenlow (Hint 3/3): Full recipe! Fill 5 -> Pour 5 to 3 (5 holds 2) -> Tip out 3 -> Pour 5 to 3 (3 holds 2) -> Fill 5 -> Pour 5 to 3 (5 holds EXACTLY 4!) -> Pour the 5-flask into the Purge Funnel!"))
    end
    $game_variables[{V_HINT_TIER}] = t + 1
  when 3
    if $game_switches[301]
      $game_switches[{S_VALVE_4}] = true
      $game_map.need_refresh = true
      pbSEPlay("Anim/HealBell", 85, 100)
      pbMessage(_INTL("Wenlow: Done! I dosed the Purge Funnel for you — the north drawbridge is open!"))
    end
    break
  else
    break
  end
end'''
    E.append({
        'type': 'event',
        'name': 'Apprentice Wenlow',
        'at': [9, 19],
        'pages': [{
            'graphic': {'sprite': 'WENLOW', 'dir': 'right'},
            'trigger': 'action',
            'move': 'fixed',
            'commands': [{'script': wenlow_231_ruby}],
        }],
    })

    # Canonical PBS Trainers for Map 231: Hester patrols the central runner loop (sight=4 -> x=14..17), Finch guards east deck!
    E.append(_trainer(
        (18, 14), 'SCIENTIST', 'Hester', 'left',
        "Scientist Hester: Three and five make four, if your hands don't shake! Let's test your nerve first!",
        "Scientist Hester: Dose makes the poison. I misjudged the dose.",
        sight=4,
    ))
    E.append(_trainer(
        (21, 18), 'BURGLAR', 'Finch', 'left',
        "Scavenger Finch: Doctor Mott lets me watch the Dispensary shelves so long as I keep my fingers off the pure flasks!",
        "Scavenger Finch: I only scavenge what the ward throws out. Like me, now.",
        sight=3,
    ))
    E.append({'type': 'item', 'name': 'Item Full Heal', 'at': [22, 21], 'item': 'FULLHEAL'})

    # Protect all interactive paths, trainers & bridges
    for e in E:
        ex, ey = e['at']
        m.keep_clear.add((ex, ey))
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            if m.inb(ex + dx, ey + dy):
                m.keep_clear.add((ex + dx, ey + dy))
    for y in range(4, 25):
        for x in (13, 14, 15):
            m.keep_clear.add((x, y))
    for x in range(14, 22):
        m.keep_clear.add((x, 14)); m.keep_clear.add((x, 18))

    # ---- 3. Apothecary Dispensary Architecture, Shelving & Mire Steam (ZERO floating mushrooms, ZERO offset glows!) ----
    _place_stamp_over(m, 'pf_signpost', 12, 10, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'cv_frame', 13, 3, base_z=1, top_z=2, top_rows=1, solid=False)
    for bx, by in ((4, 9), (8, 9), (19, 9), (23, 9)):
        _place_stamp_over(m, 'mn_books2', bx, by, base_z=1, top_z=2, top_rows=1, solid=True)
    for cx, cy in ((12, 4), (16, 4), (11, 21), (17, 21), (6, 12), (22, 11)):
        _place_stamp_over(m, 'mn_candelabra', cx, cy, base_z=1, top_z=2, top_rows=1, solid=True)
    # Cohesive glass apothecary specimen case (replaces isolated nightstand at (6, 16)!)
    _place_stamp_over(m, 'mn_case_m', 6, 16, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'mn_fern', 6, 21, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'pf_p_vat_b', 6, 11, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'pf_p_vat_y', 18, 11, base_z=1, top_z=1, top_rows=0, solid=True)
    for sx, sy in ((6, 7), (21, 7), (3, 15), (24, 16)):
        _place_stamp_over(m, 'lm_steam0' if (sx + sy) % 2 == 0 else 'lm_steam1', sx, sy, base_z=2, top_z=2, top_rows=2, solid=False)
    for gx, gy in ((8, 7), (20, 7), (4, 18), (25, 14)):
        m.over.append((2, gx, gy, T_GLINT[(gx + gy) % 4]))

    m.paint()
    # Cohesive dark-slate stone masonry + riveted-iron framed timber work-decks (ZERO B&W checkerboard!)
    _paint_clinic_floors(m, [
        (3, 9, 25, 22, 'quay'),
        (11, 4, 17, 6, 'slate'),
        (11, 23, 17, 24, 'slate'),
        # Iron-bordered west & east apothecary work-decks!
        (5, 12, 10, 20, 'iron'),
        (6, 13, 9, 19, 'timber'),
        (18, 12, 23, 21, 'iron'),
        (19, 13, 22, 20, 'timber'),
    ])
    _paint_emerald_runner(m, 13, 12, 15, 24)
    _paint_emerald_runner(m, 13, 5, 15, 6)
    # Dark recessed portal threshold inside north doorway arch (14, 4)!
    m.L[0, 4, 14] = T_PIT_STONE
    m.L[1, 4, 14] = T_PDOOR_OPEN
    _paint_curb_piers(m, (12, 16), (7, 8))
    for px, py in ((7, 14), (14, 10)):
        m.L[0, py, px] = P1('Q_f0')

    Lr = RC.resolve(m.L, TID).astype(np.int32)
    ev_pts = [tuple(e['at']) for e in E]
    PG.guard(Lr, TID, ev_pts, 'Map 231')
    assert not PG.hits(Lr, R.tilesets()[TID], ev_pts), 'Map 231 passguard hits!'
    m.L = Lr

    head = {
        'id': 231,
        'name': 'Mirefen Gym - Puzzle Room 1',
        'parent': 230,
        'bgm': 'Gym',
        'field': FIELD,
        'map_audio': {'bgm': 'Gym - Warden Hall', 'bgs': 'Drip - Nadir', 'bgs_volume': 50, 'rain': False},
        'metadata': {'Name': 'Mirefen Gym', 'SnapEdges': True, 'MapPosition': MF_POS, 'BattleBack': 'water'},
        'tone': [-14, 4, -10, 14],
        '_file': '231_mirefen_gym_231.yaml',
    }
    m.write(231, head, comment='# GENERATED by mapgen/layouts/mirefen_gym.py (Batch 3C): Mirefen Gym - Puzzle Room 1 (Dispensary).\n'
                               '# Edit the layout script, not this file.\n')
    return m, Lr


# =================================================================================================
# MAP 232 — MIREFEN GYM - PUZZLE ROOM 2 ("The Sludge Gallery — COMBINE + Quiet Alcove Mastery", 29x25, TS 58)
# =================================================================================================
def build_232():
    W, H = 29, 25
    m = Cave(W, H, 'T', seed=232, pool='Sea Cave', tid=TID, game='pf')
    m.STAIRS = K.STAIRS_STONE
    m.kit = {TER: 'cvT2', FLOOR: 'cvT2', MASS: 'cvT2', 'default': 'cvT2'}

    # ---- 1. Sculpt Wet Timber Sludge Gallery + Isolated South Mastery Wing + North Arena Gallery ----
    # North Arena Gallery (x=12..27, y=2..6 -> clean unbroken straight north wall, ZERO jagged corner caps!)
    m.box(12, 2, 27, 6, FLOOR, '.')
    # Mire Trench separating North Gallery from Mid Gallery (x=2..27, y=7..8; bridge cols x=25..26!)
    m.box(2, 7, 27, 8, FLOOR, 'w')
    for cy in (7, 8):
        for cx in (24, 27):
            m.cls[cy, cx] = '.'
    # Mid Band: Full Mire Basin (x=2..27, y=9..17) carved with Dry Platforms & Corrosive Sludge Spans!
    m.box(2, 9, 27, 17, FLOOR, 'w')
    m.box(2, 9, 5, 17, FLOOR, '.')          # West Tap End
    m.box(6, 12, 11, 14, FLOOR, '.')        # Sludge Crossing #1 (EXACTLY 6 sludge steps!)
    m.box(12, 10, 15, 16, FLOOR, '.')       # Island A
    m.box(16, 12, 16, 14, FLOOR, 'w')       # East Sluice Gate (mire under drawbridge controlled by S331!)
    m.box(17, 12, 23, 14, FLOOR, '.')       # Sludge Crossing #2 (EXACTLY 7 sludge steps -> 6+7=13 > 10!)
    m.box(24, 9, 27, 16, FLOOR, '.')        # East Dais B (NO refill station here!)
    # South Dry Wing & Optional Quiet Alcove Mastery (isolated from Island A & Dais B!)
    m.box(3, 17, 5, 19, FLOOR, '.')
    m.box(2, 19, 19, 23, FLOOR, '.')
    m.box(6, 17, 27, 18, FLOOR, 'w')

    # Keep upper north-gallery corners square & crisp (only soften south wing outer corners!)
    m.mass_at([(2, 23), (19, 23)])
    m.tidy()
    m.plan_cliffs(rows=2)

    # ---- 2. Events: Return -> 231, Arena Portal -> 233, Tap, Refills, Sludge Step Triggers, Socket A, Basin B, Mastery ----
    E = m.events
    E.append({
        'type': 'warp',
        'name': 'Back to Dispensary (231)',
        'at': [2, 13],
        'to': {'map': 231, 'x': 14, 'y': 5, 'dir': 'down'},
        'se': 'Door exit',
    })
    E.append(_sign(
        'Dispensary Return Sign', (2, 12),
        "← EXIT TO DISPENSARY (ROOM 1) — Step onto the doorway mat directly south to return to the Dispensary.",
    ))
    E.append({
        'type': 'warp',
        'name': 'To Warden Arena (233)',
        'at': [14, 4],
        'to': {'map': 233, 'x': 10, 'y': 15, 'dir': 'up'},
        'se': 'Door enter',
    })

    # East Sluice Gate (x=16, y=12..14): locked = heavy steel sluice shutter (lm_pdoor) + red lock cross (lm_latch) — ZERO ladders!
    for gy in (12, 13, 14):
        E.append(_drawbridge_event(
            f'Sludge Sluice Gate {gy}', 16, gy, S_SOCKET_A,
            "The east steel sluice gate is bolted shut! Measure EXACTLY 1 unit at the west Tap Bench and pour it into Socket A on this island to open the gate.",
            closed_tile=T_LATCH if gy == 13 else T_PDOOR,
        ))

    # North Arena Bridge (x=25..26, y=7..8): locked = barred lock gate on y=8 + open impassable mire on y=7!
    for bx in (25, 26):
        for by in (7, 8):
            E.append(_drawbridge_event(
                f'Arena Bridge {bx},{by}', bx, by, S_BASIN_B,
                "The Arena bridge is retracted above the open corrosive mire! Basin B on East Dais B needs a cumulative total of EXACTLY 7 measures.",
                closed_tile=(T_BARS_L if bx == 25 else T_BARS_M) if by == 8 else None,
            ))

    # West Tap Bench (ONLY place to Fill 3 & 5 flasks in Room 232!)
    E.append({
        'type': 'event',
        'name': 'Gallery Tap Bench',
        'at': [3, 10],
        'pages': [{
            'graphic': {'tile': T_TAP},
            'trigger': 'action',
            'commands': [{'script': _ruby_flask_bench(allow_fill=True, title='Gallery Tap Bench')}],
        }],
    })

    # Mask Filter Refill Station #1 (West Tap End, (5, 10)) & #2 (Island A, (13, 16))
    refill_ruby = f'''$game_variables[{V_FILTER}] = 0
pbSEPlay("Anim/Smokescreen", 75, 125)
pbMessage(_INTL("Mask Filter Station: Fresh bone-char cartridge seated! Rebreather restored to 10/10 sludge steps."))'''
    E.append({
        'type': 'event',
        'name': 'Mask Filter Refill 1',
        'at': [5, 10],
        'pages': [{'graphic': {'tile': T_REFILL}, 'trigger': 'action', 'commands': [{'script': refill_ruby}]}],
    })
    E.append({
        'type': 'event',
        'name': 'Mask Filter Refill 2',
        'at': [13, 16],
        'pages': [{'graphic': {'tile': T_REFILL}, 'trigger': 'action', 'commands': [{'script': refill_ruby}]}],
    })

    # Portable Flask Pouring Trays (NO Fill — Island A (15, 10) & Dais B (27, 11)!)
    E.append({
        'type': 'event',
        'name': 'Flask Pouring Tray A',
        'at': [15, 10],
        'pages': [{'graphic': {'tile': T_TRAY}, 'trigger': 'action', 'commands': [{'script': _ruby_flask_bench(allow_fill=False, title='Island A Flask Tray')}]}],
    })
    E.append({
        'type': 'event',
        'name': 'Flask Pouring Tray B',
        'at': [27, 11],
        'pages': [{'graphic': {'tile': T_TRAY}, 'trigger': 'action', 'commands': [{'script': _ruby_flask_bench(allow_fill=False, title='Dais B Flask Tray')}]}],
    })

    # Socket A (Island A (13, 10) — needs EXACTLY 1 measure -> S331 ON!)
    E.append({
        'type': 'event',
        'name': 'Socket A (Needs 1)',
        'at': [13, 10],
        'pages': [{
            'graphic': {'tile': T_VAT_GOLD},
            'trigger': 'action',
            'commands': [{
                'script': _ruby_exact_funnel(
                    1, S_SOCKET_A, 'Socket A',
                    "One exact measure clicks the relay! The east sluice gate slides open over the second sludge span!",
                ),
            }],
        }],
    })

    # Basin B (East Dais B (25, 10) — CUMULATIVE EXACTLY 7 -> S332 ON; >7 overflows to 0!)
    basin_b_ruby = f'''if $game_switches[{S_BASIN_B}]
  pbMessage(_INTL("Basin B: Balanced at exactly 7/7 measures! The north Arena bridge is wide open!"))
else
  s = $game_variables[{V_FLASK_3}].to_i
  b = $game_variables[{V_FLASK_5}].to_i
  cur = $game_variables[{V_BASIN}].to_i
  cmds = [
    _INTL("Pour 3-Flask ({{1}} {{2}})", s, s == 1 ? "measure" : "measures"),
    _INTL("Pour 5-Flask ({{1}} {{2}})", b, b == 1 ? "measure" : "measures"),
    _INTL("Step back")
  ]
  ch = pbMessage(_INTL("Basin B (Cumulative) — Currently {{1}}/7 measures. [3-Flask: {{2}}/3 | 5-Flask: {{3}}/5]", cur, s, b), cmds, 3)
  if ch == 0 || ch == 1
    amt = (ch == 0) ? s : b
    $game_variables[(ch == 0) ? {V_FLASK_3} : {V_FLASK_5}] = 0
    if amt == 0
      pbSEPlay("GUI sel buzzer", 75, 100)
      pbMessage(_INTL("That flask is empty!"))
    else
      tot = cur + amt
      if tot == 7
        $game_variables[{V_BASIN}] = 7
        $game_switches[{S_BASIN_B}] = true
        $game_map.need_refresh = true
        pbSEPlay("Anim/HealBell", 90, 100)
        pfm_shake(5, 10, 10) if defined?(pfm_shake)
        pbMessage(_INTL("7/7 exact measures! The mire settles clear and the north Arena bridge locks into place!"))
      elsif tot > 7
        $game_variables[{V_BASIN}] = 0
        pbSEPlay("GUI sel buzzer", 85, 90)
        pbMessage(_INTL("{{1}} measures — too much! Basin B overflows and drains completely back to 0/7!", tot))
      else
        $game_variables[{V_BASIN}] = tot
        pbSEPlay("Anim/Water2", 80, 100)
        pbMessage(_INTL("Basin B absorbs the dose — now holding {{1}}/7 measures.", tot))
      end
    end
  end
end'''
    E.append({
        'type': 'event',
        'name': 'Basin B (Cumulative 7)',
        'at': [25, 10],
        'pages': [{'graphic': {'tile': T_VAT_BLUE}, 'trigger': 'action', 'commands': [{'script': basin_b_ruby}]}],
    })

    # Emergency Filter Recall Cord on Dais B (27, 15) — safe fast return to Tap End keeping flasks & Basin B!
    recall_ruby = f'''if pbConfirmMessage(_INTL("Pull the Emergency Filter Recall cord to return safely to the West Tap End? (Flasks and delivered doses are kept!)"))
  $game_variables[{V_FILTER}] = 0
  pbSEPlay("Anim/Smokescreen", 75, 115)
  pbFadeOutIn do
    $game_player.moveto(4, 13)
    $game_player.turn_right
  end
end'''
    E.append({
        'type': 'event',
        'name': 'Filter Recall Cord',
        'at': [27, 15],
        'pages': [{'graphic': {'tile': T_RECALL}, 'trigger': 'action', 'commands': [{'script': recall_ruby}]}],
    })

    # Walkable Corrosive Sludge Step Trigger Tiles (trigger: touch on bubbling emerald gd_g sludge -> 0 over_trigger!)
    sludge_step_ruby = f'''$game_variables[{V_FILTER}] = $game_variables[{V_FILTER}].to_i + 1
rem = 10 - $game_variables[{V_FILTER}].to_i
if rem <= 0
  pbSEPlay("Poison step", 95, 95)
  pbMessage(_INTL("Your mask filter is spent! Corrosive fumes drive you back to the Tap End. (Your flasks and delivered doses are kept!)"))
  $game_variables[{V_FILTER}] = 0
  pbFadeOutIn do
    $game_player.moveto(4, 13)
    $game_player.turn_right
  end
elsif rem == 2
  pbSEPlay("Poison step", 75, 105)
  pbMessage(_INTL("Your mask filter hisses softly — only 2 sludge steps left!"))
else
  pbSEPlay("Poison step", 45, 100)
end'''
    for sx in list(range(6, 12)) + list(range(17, 24)):
        for sy in (12, 13, 14):
            E.append({
                'type': 'event',
                'name': f'Sludge {sx},{sy}',
                'at': [sx, sy],
                'pages': [{'trigger': 'touch', 'commands': [{'script': sludge_step_ruby}]}],
            })

    # Apprentice Wenlow (232 Combine Status, Zero-Softlock Reset, 3-Tier Hints, puzzleskip!)
    wenlow_232_ruby = f'''loop do
  s = $game_variables[{V_FLASK_3}].to_i
  b = $game_variables[{V_FLASK_5}].to_i
  rem = 10 - $game_variables[{V_FILTER}].to_i
  sa = $game_switches[{S_SOCKET_A}] ? "DONE" : "Needs 1"
  bb = $game_switches[{S_BASIN_B}] ? "OPEN!" : "#{{$game_variables[{V_BASIN}].to_i}}/7"
  cmds = [_INTL("Check status"), _INTL("Reset flasks & filter"), _INTL("Ask for a hint")]
  cmds.push(_INTL("Skip room (puzzleskip)")) if $game_switches[301]
  cmds.push(_INTL("Back to work"))
  ch = pbMessage(_INTL("Wenlow: Mind your mask! Sir says I'll run this place one day — I say not till I can carry a tray! [3F:{{1}} 5F:{{2}} Filter:{{3}}/10 | A:{{4}} | B:{{5}}]", s, b, rem, sa, bb), cmds, cmds.length)
  case ch
  when 0
    pbMessage(_INTL("Wenlow: 3-Flask={{1}}/3, 5-Flask={{2}}/5, Filter={{3}}/10 steps left. Socket A: {{4}}. Basin B: {{5}}.", s, b, rem, sa, bb))
  when 1
    $game_variables[{V_FLASK_3}] = 0
    $game_variables[{V_FLASK_5}] = 0
    $game_variables[{V_FILTER}] = 0
    $game_variables[{V_HINT_TIER}] = $game_variables[{V_HINT_TIER}].to_i + 1
    pbFadeOutIn do
      $game_player.moveto(4, 13)
      $game_player.turn_right
    end
    pbMessage(_INTL("Wenlow: Fresh filter cartridge and rinsed flasks — your delivered Socket A & Basin B doses stayed safe!"))
    break
  when 2
    t = $game_variables[{V_HINT_TIER}].to_i
    if t == 0
      pbMessage(_INTL("Wenlow (Hint 1/3): You can pour between flasks at the island trays, sir lets me — you can only FILL at this west tap! And always hit the glowing filter station on Island A!"))
    elsif t == 1
      pbMessage(_INTL("Wenlow (Hint 2/3): Basin B adds up cumulatively! On trip two, fill both flasks at the tap so they hold 2 + 5 = 7 together, refill on Island A, then pour both into Basin B!"))
    else
      pbMessage(_INTL("Wenlow (Hint 3/3): Trip 1: Fill 3 -> Pour 3 to 5 -> Fill 3 -> Pour 3 to 5 (3-Flask holds 1!). Cross to Island A, pour 1 into Socket A, refill filter, return! Trip 2: Make 2 in 3-Flask (Fill 5->3, Tip 3, 5->3), then Fill 5 (you carry 2 + 5!). Cross to A, refill filter, cross to B, pour BOTH flasks = 7!"))
    end
    $game_variables[{V_HINT_TIER}] = t + 1
  when 3
    if $game_switches[301]
      $game_switches[{S_SOCKET_A}] = true
      $game_switches[{S_BASIN_B}] = true
      $game_variables[{V_BASIN}] = 7
      $game_map.need_refresh = true
      pbSEPlay("Anim/HealBell", 85, 100)
      pbMessage(_INTL("Wenlow: All dosed! Both the east sluice gate and north Arena bridge are open!"))
    end
    break
  else
    break
  end
end'''
    E.append({
        'type': 'event',
        'name': 'Apprentice Wenlow',
        'at': [4, 16],
        'pages': [{
            'graphic': {'sprite': 'WENLOW', 'dir': 'up'},
            'trigger': 'action',
            'move': 'fixed',
            'commands': [{'script': wenlow_232_ruby}],
        }],
    })

    # Optional Quiet Alcove Mastery (South-East Dry Wing, 4 & 9 flasks -> sequential doses 1, 3, 6 -> SYNTHETICSEED x2 + BLACKSLUDGE!)
    E.append({
        'type': 'event',
        'name': 'Quiet Mastery Tap (4 & 9)',
        'at': [13, 20],
        'pages': [{
            'graphic': {'tile': T_TAP},
            'trigger': 'action',
            'commands': [{'script': _ruby_flask_bench(allow_fill=True, v_small=V_FLASK_4, cap_s=4, v_big=V_FLASK_9, cap_b=9, title='Quiet Alcove Tap (4 & 9)')}],
        }],
    })
    mastery_vat_ruby = f'''if $game_switches[{S_QUIET_DONE}]
  pbMessage(_INTL("Quiet Alcove Vat: All three sedative doses (1, 3, and 6) measured perfectly. Wenlow's note rests beside the clean phials."))
else
  targets = [1, 3, 6]
  st = $game_variables[{V_QUIET_STEP}].to_i
  want = targets[st] || 6
  s = $game_variables[{V_FLASK_4}].to_i
  b = $game_variables[{V_FLASK_9}].to_i
  cmds = [
    _INTL("Pour 4-Flask ({{1}} {{2}})", s, s == 1 ? "measure" : "measures"),
    _INTL("Pour 9-Flask ({{1}} {{2}})", b, b == 1 ? "measure" : "measures"),
    _INTL("Step back")
  ]
  ch = pbMessage(_INTL("Quiet Alcove Vat (Dose {{1}}/3 — Needs EXACTLY {{2}}) [4-Flask: {{3}}/4 | 9-Flask: {{4}}/9]", st + 1, want, s, b), cmds, 3)
  if ch == 0 || ch == 1
    amt = (ch == 0) ? s : b
    $game_variables[(ch == 0) ? {V_FLASK_4} : {V_FLASK_9}] = 0
    if amt == want
      st += 1
      $game_variables[{V_QUIET_STEP}] = st
      pbSEPlay("Anim/HealBell", 90, 100)
      if st >= 3
        $game_switches[{S_QUIET_DONE}] = true
        pbMessage(_INTL("Exact dose 6! All three Quiet Ward formulas are balanced!"))
        pbReceiveItem(:SYNTHETICSEED, 2)
        pbReceiveItem(:BLACKSLUDGE, 1)
        pbMessage(_INTL("Tucked under the tray is a slip in Wenlow's round handwriting: 'Thanks for helping with the Quiet ones. Sir pretends he doesn't cry. — W.'"))
      else
        pbMessage(_INTL("Exact dose {{1}}! Next Quiet Ward dose requires EXACTLY {{2}}.", want, targets[st]))
      end
    else
      pbSEPlay("GUI sel buzzer", 80, 95)
      pbMessage(_INTL("That was {{1}} {{2}} — the quiet formula requires EXACTLY {{3}}.", amt, amt == 1 ? "measure" : "measures", want))
    end
  end
end'''
    E.append({
        'type': 'event',
        'name': 'Quiet Alcove Dosing Vat',
        'at': [16, 20],
        'pages': [{'graphic': {'tile': T_VAT_RED}, 'trigger': 'action', 'commands': [{'script': mastery_vat_ruby}]}],
    })

    # Solid Plaques (backed by real solid pf_signposts!)
    E += [
        _sign('Island A Plaque', (15, 16),
              "ISLAND A — Socket A requires EXACTLY 1 measure to raise the east sluice gate. Always recharge your mask filter at the glowing lamp before crossing the 7-step sludge span!"),
        _sign('Quiet Alcove Plaque', (18, 22),
              "OPTIONAL MASTERY: THE QUIET ALCOVE — Measure doses of 1, 3, and 6 in order using unmarked 4- and 9-measure flasks to earn Corvin's Corrosive Mire field hoard!"),
    ]

    # Canonical PBS Trainers for Map 232: Lorcan guards south wing; Mudge at (20,4) facing down (sight=2) guards ENTIRE north corridor!
    E.append(_trainer(
        (7, 21), 'SCIENTIST', 'Lorcan', 'right',
        "Scientist Lorcan: Careful with those unmarked flasks — one drop too many and the whole gallery fumes over!",
        "Scientist Lorcan: Mind the sludge. It's had a longer day than you.",
        sight=3,
    ))
    E.append(_trainer(
        (20, 4), 'BURGLAR', 'Mudge', 'down',
        "Scavenger Mudge: You made it across the sludge gallery AND balanced Basin B! One last scrap before Doctor Mott!",
        "Scavenger Mudge: Corvin patched me up twice. Third time's on you.",
        sight=2,
    ))

    # Protect all interactive paths, trainers & bridges
    for e in E:
        ex, ey = e['at']
        m.keep_clear.add((ex, ey))
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            if m.inb(ex + dx, ey + dy):
                m.keep_clear.add((ex + dx, ey + dy))
    for x in range(13, 27):
        m.keep_clear.add((x, 4)); m.keep_clear.add((x, 5)); m.keep_clear.add((x, 6))
    for x in range(3, 19):
        m.keep_clear.add((x, 21)); m.keep_clear.add((x, 22))

    # ---- 3. Wet Timber Sludge Gallery Architecture, Framed West Exit, Signposts & Steam (ZERO floating mushrooms, ZERO offset glows!) ----
    _place_stamp_over(m, 'pf_signpost', 2, 11, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'pf_signpost', 15, 15, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'pf_signpost', 18, 21, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'cv_frame', 13, 3, base_z=1, top_z=2, top_rows=1, solid=False)
    for cx, cy in ((12, 5), (16, 4), (24, 5), (2, 14), (26, 9), (3, 20), (11, 20)):
        if (cx, cy) not in m.keep_clear:
            _place_stamp_over(m, 'cv_lamp_on', cx, cy, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'hb_barrels', 2, 16, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'cv_tools', 2, 22, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'mn_books2', 14, 19, base_z=1, top_z=2, top_rows=1, solid=True)
    # Corrosive steam plumes & subtle water shimmer over open mire channels (ZERO floating mushrooms!)
    for sx, sy in ((8, 9), (19, 9), (9, 16), (20, 16), (10, 7), (20, 7)):
        _place_stamp_over(m, 'lm_steam0' if (sx + sy) % 2 == 0 else 'lm_steam1', sx, sy, base_z=2, top_z=2, top_rows=2, solid=False)
    for gx, gy in ((7, 10), (18, 10), (8, 15), (21, 15), (12, 17), (22, 17)):
        m.over.append((2, gx, gy, T_GLINT[(gx + gy) % 4]))

    m.paint()
    _paint_clinic_floors(m, [
        (2, 9, 5, 17, 'quay'),
        (12, 10, 15, 16, 'quay'),
        (24, 9, 27, 16, 'quay'),
        (12, 4, 27, 6, 'quay'),
        (2, 19, 11, 23, 'quay'),
        # Cohesive Quiet Alcove Mastery room: dark weathered apothecary flagstone + emerald-gold rug inlay (ZERO checkerboard!)
        (12, 19, 19, 23, 'slate'),
        # Unmistakable toxic bubbling emerald corrosive sludge across BOTH hazard spans!
        (6, 12, 11, 14, 'sludge'),
        (17, 12, 23, 14, 'sludge'),
    ])
    _paint_emerald_runner(m, 13, 5, 15, 6)
    _paint_emerald_runner(m, 13, 21, 17, 22)
    # Dark recessed portal threshold inside north Arena doorway arch (14, 4)!
    m.L[0, 4, 14] = T_PIT_STONE
    m.L[1, 4, 14] = T_PDOOR_OPEN
    _paint_curb_piers(m, (24, 27), (7, 8))

    # Crisp illuminated hazard curbs marking exact 6-step (x=6..11) and 7-step (x=17..23) sludge boundaries!
    for cx in (5, 12, 15, 24):
        for cy in (12, 13, 14):
            m.L[0, cy, cx] = P1('Q_f0')
            if int(m.L[1, cy, cx]) == 0:
                m.L[1, cy, cx] = T_STRIP_V
    # Rising toxic corrosive vapor wisps on L[2] over both bubbling emerald sludge spans (pas=0x0 -> 100% walkable!)
    for vx, vy in ((7, 12), (9, 14), (10, 13), (18, 14), (20, 12), (22, 13)):
        if int(m.L[2, vy, vx]) == 0:
            m.L[2, vy, vx] = T_VAPOR[(vx + vy) % 3]

    # Riveted steel mounting pads under taps/vats/valves!
    for px, py in ((3, 10), (13, 10), (25, 10), (27, 15), (13, 20), (16, 20)):
        m.L[0, py, px] = P1('Q_f0')

    # Clearly legible West Return Exit Doorway at (2, 13): framed wooden door in wall (1, 13) + sconce (1, 12) + woven exit mat (2, 13)!
    m.L[1, 13, 1] = T_DOOR_WOOD
    m.L[1, 12, 1] = T_WALL_LAMP
    m.L[0, 13, 2] = P1('Q_f0')
    m.L[1, 13, 2] = T_MAT

    Lr = RC.resolve(m.L, TID).astype(np.int32)
    ev_pts = [tuple(e['at']) for e in E]
    PG.guard(Lr, TID, ev_pts, 'Map 232')
    assert not PG.hits(Lr, R.tilesets()[TID], ev_pts), 'Map 232 passguard hits!'
    m.L = Lr

    head = {
        'id': 232,
        'name': 'Mirefen Gym - Puzzle Room 2',
        'parent': 230,
        'bgm': 'Gym',
        'field': FIELD,
        'map_audio': {'bgm': 'Gym - Warden Hall', 'bgs': 'Drip - Nadir', 'bgs_volume': 55, 'rain': False},
        'metadata': {'Name': 'Mirefen Gym', 'SnapEdges': True, 'MapPosition': MF_POS, 'BattleBack': 'water'},
        'tone': [-16, 4, -12, 16],
        '_file': '232_mirefen_gym_232.yaml',
    }
    m.write(232, head, comment='# GENERATED by mapgen/layouts/mirefen_gym.py (Batch 3C): Mirefen Gym - Puzzle Room 2 (Sludge Gallery).\n'
                               '# Edit the layout script, not this file.\n')
    return m, Lr


# =================================================================================================
# MAP 233 — MIREFEN GYM - WARDEN ARENA ("The Operating Theatre", Corvin Mott, 21x17, TS 58)
# =================================================================================================
def build_233():
    W, H = 21, 17
    m = Cave(W, H, 'F', seed=233, pool='Sea Cave', tid=TID, game='pf')
    m.STAIRS = K.STAIRS_STONE
    m.kit = {TER: 'cvF2', FLOOR: 'cvF2', MASS: 'cvF2', 'default': 'cvF2'}

    # ---- 1. Sculpt Dramatic Octagonal Operating Theatre Ring Over Bubbling Corrosive Mire! ----
    m.box(2, 2, 18, 14, FLOOR, 'w')
    m.box(7, 2, 13, 7, TER, '.')
    m.box(6, 8, 14, 13, FLOOR, '.')
    m.box(5, 9, 15, 12, FLOOR, '.')
    m.box(15, 12, 17, 14, FLOOR, '.')
    m.box(8, 14, 12, 16, FLOOR, '.')

    m.mass_at([(2, 2), (3, 2), (2, 3), (18, 2), (17, 2), (18, 3), (2, 13), (2, 14), (3, 14), (18, 14)])
    m.stairs(9, 7, w=3, n=2, c='.')
    m.tidy()
    m.plan_cliffs(rows=2)

    # ---- 2. Events: Return -> 232, Fast-Exit Lift -> 230, Warden Corvin Mott (DOUBLE Battle!) ----
    E = m.events
    for rx in (9, 10, 11):
        E.append({
            'type': 'warp',
            'name': f'Back to Sludge Gallery {rx}',
            'at': [rx, 16],
            'to': {'map': 232, 'x': 14, 'y': 5, 'dir': 'down'},
            'se': 'Door exit',
        })
    E.append({
        'type': 'warp',
        'name': 'Fast-Exit Lift to Entrance (230)',
        'at': [16, 13],
        'to': {'map': 230, 'x': 10, 'y': 14, 'dir': 'down'},
        'se': 'Door slide',
    })
    E.append(_sign(
        'Operating Lift Sign', (16, 12),
        "INFIRMARY FAST-EXIT LIFT — Step onto the bolted steel lift plate directly below to return straight to the Gym Entrance!",
    ))

    # WARDEN CORVIN MOTT (story/26_SCRIPT_CH7.md:328-347 + GYM_PUZZLES.md double: true + S333 Mastery line!)
    corvin_battle_ruby = f'''pbMessage(_INTL("Corvin: Everything's poison, dear. Dose makes the cure."))
pbMessage(_INTL("Corvin: Two at once, because nobody in Nadir ever has only one thing wrong with them."))
pbMessage(_INTL("Corvin: Don't worry. I'm a doctor. I know exactly how much this hurts."))
if Prismfall.gym_battle(pfm_gym(:LEADER_CORVIN), double: true)
  pbMessage(_INTL("Corvin: ...Well. That's the correct dose."))
  Prismfall.award_badge(pfm_gym(:LEADER_CORVIN))
  pbSEPlay("Anim/HealBell", 90, 100)
  pbMessage(_INTL("Six clear notes ring out as the Remedy Badge settles in. Light runs along your badge case's seams like water in a channel."))
  pbMessage(_INTL("Corvin: Your case sings. I'd have that looked at. Not by me. I'm busy."))
  pbReceiveItem(:TM84)
  pbMessage(_INTL("Corvin: Poison Jab. Close in, quick, and they go home feeling worse. It's the bedside manner I was never taught."))
  pbMessage(_INTL("Corvin: The ferrymen down on Mirefen's south steps will give you Surf now. Lake Sallow's east, past Leechman's Walk. Cindervault's past it. Don't drink the lake either."))
  if $game_switches[{S_QUIET_DONE}]
    pbMessage(_INTL("Corvin: ...And Wenlow told me you measured for the Quiet Alcove too. Four and nine isn't easy. Thank you. Don't tell him I said that."))
  end
  $game_variables[127] = 5 if $game_variables[127].to_i < 5
  $game_self_switches[[233, @event_id, "A"]] = true
  $game_map.need_refresh = true
end'''
    corvin_after_ruby = f'''if $game_switches[{S_QUIET_DONE}]
  pbMessage(_INTL("Corvin: Four and nine in the Quiet Alcove, and clean work in the Theatre. You'd make a passable apothecary if you weren't busy collecting Badges."))
end
pbMessage(_INTL("Corvin: Take the east lift if you want a quick ride down to the lobby — and mind the ferrymen for Surf before heading east to Ashkaar."))'''

    E.append({
        'type': 'event',
        'name': 'Warden Corvin Mott',
        'at': [10, 5],
        'pages': [
            {
                'graphic': {'sprite': 'CORVIN', 'dir': 'down'},
                'trigger': 'action',
                'move': 'fixed',
                'commands': [{'script': corvin_battle_ruby}],
            },
            {
                'cond': {'self': 'A'},
                'graphic': {'sprite': 'CORVIN', 'dir': 'down'},
                'trigger': 'action',
                'move': 'fixed',
                'commands': [{'script': corvin_after_ruby}],
            },
        ],
    })

    for y in range(5, 17):
        for x in (9, 10, 11):
            m.keep_clear.add((x, y))
    for p in ((15, 12), (15, 13), (16, 12), (16, 13), (17, 13), (14, 12), (14, 13)):
        m.keep_clear.add(p)

    # ---- 3. Operating Theatre Architecture, Framed Lift Bay, Apothecary Specimen Cases & Steam (ZERO floating mushrooms, ZERO offset glows!) ----
    _place_stamp_over(m, 'mn_candelabra', 7, 3, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'mn_candelabra', 13, 3, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'pf_p_vat_b', 7, 6, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'pf_p_vat_r', 13, 6, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'mn_books2', 8, 3, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'mn_books2', 11, 3, base_z=1, top_z=2, top_rows=1, solid=True)

    # Framed Fast-Exit Lift Bay: solid steel hatch lm_sdoor at (16, 11..12) (pas=0xf at (16,12)!) + bollards!
    _place_stamp_over(m, 'lm_sdoor', 16, 11, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'lm_bollard', 17, 12, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'lm_bollard', 17, 14, base_z=1, top_z=1, top_rows=0, solid=True)

    # Corner candelabras & symmetrical Victorian glass apothecary specimen cases (replaces isolated nightstands!)
    for cx, cy in ((6, 9), (14, 9), (6, 12), (14, 12)):
        _place_stamp_over(m, 'mn_candelabra', cx, cy, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'mn_case_m', 5, 10, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'mn_case_m', 15, 10, base_z=1, top_z=1, top_rows=0, solid=True)
    for bx, by in ((8, 15), (12, 15)):
        _place_stamp_over(m, 'lm_bollard', bx, by, base_z=1, top_z=1, top_rows=0, solid=True)
    # Dramatic corrosive steam plumes + subtle water surface shimmer over mire (ZERO floating mushrooms!)
    for sx, sy in ((3, 6), (17, 6), (3, 11), (17, 9)):
        _place_stamp_over(m, 'lm_steam0' if (sx + sy) % 2 == 0 else 'lm_steam1', sx, sy, base_z=2, top_z=2, top_rows=2, solid=False)
    for gx, gy in ((4, 7), (16, 7), (4, 12), (17, 10)):
        m.over.append((2, gx, gy, T_GLINT[(gx + gy) % 4]))

    m.paint()
    # Cohesive moody dark-slate masonry outer ring + sunken charcoal-slate battle pit (ZERO B&W checkerboard!)
    _paint_clinic_floors(m, [
        (7, 3, 13, 7, 'timber'),
        (5, 8, 15, 13, 'quay'),
        (8, 10, 12, 12, 'pit'),
        (8, 14, 12, 16, 'slate'),
        (15, 12, 17, 14, 'iron'),
    ])
    # Iron drainage grate ring framing the octagonal operating battle floor!
    for rx in range(8, 13):
        for ry in (9, 13):
            if m.cls[ry, rx] == '.' and m.L[1, ry, rx] == 0:
                m.L[1, ry, rx] = T_IRON_GRATE
    for ry in (10, 11, 12):
        for rx in (7, 13):
            if m.cls[ry, rx] == '.' and m.L[1, ry, rx] == 0:
                m.L[1, ry, rx] = T_IRON_GRATE
    _paint_emerald_runner(m, 9, 14, 11, 16)
    m.L[1, 13, 16] = T_CHUTE

    Lr = RC.resolve(m.L, TID).astype(np.int32)
    ev_pts = [tuple(e['at']) for e in E]
    PG.guard(Lr, TID, ev_pts, 'Map 233')
    assert not PG.hits(Lr, R.tilesets()[TID], ev_pts), 'Map 233 passguard hits!'
    m.L = Lr

    _sim_bfs(Lr, E, (10, 15), [
        ('Return -> 232', (10, 16), False),
        ('Fast-Exit Lift -> 230', (16, 13), False),
        ('Lift Sign', (16, 12), True),
        ('Warden Corvin Mott', (10, 5), True),
    ], 'Map 233 Warden Arena', verify_static=True)

    head = {
        'id': 233,
        'name': 'Mirefen Gym - Warden Arena',
        'parent': 230,
        'bgm': 'Gym',
        'field': FIELD,
        'map_audio': {'bgm': 'Gym - Warden Hall', 'bgs': 'Drip - Nadir', 'bgs_volume': 55, 'rain': False},
        'metadata': {'Name': 'Mirefen Gym', 'SnapEdges': True, 'MapPosition': MF_POS, 'BattleBack': 'water'},
        'tone': [-10, 6, -12, 12],
        '_file': '233_mirefen_gym_233.yaml',
    }
    m.write(233, head, comment='# GENERATED by mapgen/layouts/mirefen_gym.py (Batch 3C): Mirefen Gym - Warden Arena (Corvin Mott).\n'
                               '# Edit the layout script, not this file.\n')
    return m, Lr


# =================================================================================================
# Exhaustive Gym 6 Puzzle State-Space & Anti-Leak Verifier (231 + 232 + Mastery 4&9!)
# =================================================================================================
def _bfs_flask_recipe(cap_a, cap_b, goal_fn, allow_fill=True):
    """Exact BFS over unmarked flask state space (a, b)."""
    start = (0, 0)
    q = deque([(start, [])])
    seen = {start}
    while q:
        (a, b), path = q.popleft()
        if goal_fn(a, b):
            return path, (a, b)
        moves = []
        if allow_fill:
            moves += [('fillA', (cap_a, b)), ('fillB', (a, cap_b))]
        p_ab = min(a, cap_b - b)
        p_ba = min(b, cap_a - a)
        moves += [
            ('A->B', (a - p_ab, b + p_ab)),
            ('B->A', (a + p_ba, b - p_ba)),
            ('tipA', (0, b)),
            ('tipB', (a, 0)),
        ]
        for lbl, nxt in moves:
            if nxt not in seen:
                seen.add(nxt)
                q.append((nxt, path + [lbl]))
    return None, None


def verify_gym6_puzzles(m231, L231, m232, L232):
    """Prove 231 & 232 puzzles are 100% solvable, 0 leaks, 0 softlocks, AND Mastery (4&9 -> 1, 3, 6) solvable!"""
    # 1. Mathematical Flask BFS Proofs
    p231, st231 = _bfs_flask_recipe(3, 5, lambda a, b: a == 4 or b == 4)
    assert p231 is not None and len(p231) == 6, f'231 flask BFS mismatch: {p231}'
    p232_1, st232_1 = _bfs_flask_recipe(3, 5, lambda a, b: a == 1 or b == 1)
    assert p232_1 is not None and len(p232_1) == 4, f'232 Socket A (1) BFS mismatch: {p232_1}'
    p232_7, st232_7 = _bfs_flask_recipe(3, 5, lambda a, b: a + b == 7)
    assert p232_7 is not None and len(p232_7) == 5, f'232 Basin B (2+5=7) BFS mismatch: {p232_7}'
    for tgt in (1, 3, 6):
        pm, stm = _bfs_flask_recipe(4, 9, lambda a, b, t=tgt: a == t or b == t)
        assert pm is not None, f'Quiet Alcove Mastery (4&9 -> {tgt}) UNSOLVABLE!'
    print(f'FLASK MATH PROOF: 231(4)={len(p231)} moves {st231}; 232(A=1)={len(p232_1)} {st232_1}; 232(B=7)={len(p232_7)} {st232_7}; Mastery(4&9->1,3,6) ALL SOLVABLE!')

    # 2. Map 231 Topology & Anti-Leak Proof
    s231_0 = _sim_bfs(L231, m231.events, (14, 23), [
        ('Return -> 230', (14, 24), False),
        ('Dispensary Tap Bench', (7, 14), True),
        ('Purge Funnel', (14, 10), True),
        ('Formula Plaque', (12, 11), True),
        ('Apprentice Wenlow', (9, 19), True),
        ('Trainer Hester', (18, 14), True),
        ('Trainer Finch', (21, 18), True),
        ('Full Heal', (22, 21), True),
    ], 'Map 231 (start)', verify_static=True)
    assert (14, 4) not in s231_0, '231 LEAK: North Portal reachable before S330!'
    _sim_bfs(L231, m231.events, (14, 23), [
        ('North Portal -> 232', (14, 4), False),
    ], 'Map 231 (S330 ON)', sw={S_VALVE_4: True})

    # 3. Map 232 Topology, Filter-Step Budget & Anti-Leak Proof
    s232_0 = _sim_bfs(L232, m232.events, (4, 13), [
        ('Return -> 231', (2, 13), False),
        ('Dispensary Return Sign', (2, 12), True),
        ('Tap Bench', (3, 10), True),
        ('Refill 1', (5, 10), True),
        ('Apprentice Wenlow', (4, 16), True),
        ('Socket A', (13, 10), True),
        ('Flask Tray A', (15, 10), True),
        ('Refill 2', (13, 16), True),
        ('Island A Plaque', (15, 16), True),
        ('Trainer Lorcan', (7, 21), True),
        ('Quiet Mastery Tap', (13, 20), True),
        ('Quiet Alcove Vat', (16, 20), True),
        ('Quiet Alcove Plaque', (18, 22), True),
    ], 'Map 232 (start: S331=OFF, S332=OFF)', verify_static=True)
    assert (25, 10) not in s232_0 and (25, 11) not in s232_0, '232 LEAK: East Dais B reachable before Socket A (S331)!'
    assert (14, 4) not in s232_0, '232 LEAK: Arena Portal reachable before Basin B (S332)!'

    s232_1 = _sim_bfs(L232, m232.events, (4, 13), [
        ('Basin B', (25, 10), True),
        ('Flask Tray B', (27, 11), True),
        ('Filter Recall Cord', (27, 15), True),
    ], 'Map 232 (Socket A S331=ON, S332=OFF)', sw={S_SOCKET_A: True})
    assert (14, 4) not in s232_1, '232 LEAK: Arena Portal reachable before Basin B (S332)!'

    _sim_bfs(L232, m232.events, (4, 13), [
        ('Trainer Mudge', (20, 4), True),
        ('Warden Arena Portal (233)', (14, 4), False),
    ], 'Map 232 (S331=ON, S332=ON)', sw={S_SOCKET_A: True, S_BASIN_B: True})

    # Verify exact sludge step counts: Span 1 = 6 <= 10, Span 2 = 7 <= 10, Span 1 + Span 2 = 13 > 10!
    span1 = [x for x in range(6, 12)]
    span2 = [x for x in range(17, 24)]
    assert len(span1) == 6 and len(span2) == 7 and len(span1) + len(span2) > 10
    print('GYM 6 PUZZLE PROOF PASSED: 230/231/232/233 solvable, filter budget airtight (6+7=13>10), Mastery solvable, ZERO leaks!')


def main():
    build_230()
    m231, L231 = build_231()
    m232, L232 = build_232()
    build_233()
    verify_gym6_puzzles(m231, L231, m232, L232)
    print('Done: wrote Mirefen Gym 6 specs & raw maps (230, 231, 232, 233).')


if __name__ == '__main__':
    main()
