#!/usr/bin/env python3
"""layouts/ironreach_gym.py — Act 3 Batch 3G: Ironreach Gym 8 ("The Pit", Warden Kaito Ren — 5 Maps: 270, 271, 272, 273, 274):
  - Map 270: Ironreach Gym - Entrance         (21x17, TS 57 PF Rejuv Cave, field :COLOSSEUM)
      * Gritty subterranean iron-and-sand colosseum lobby ("the Pit under the Pit"):
        - Full-width 3-wide south exit carpet (9..11, 16) <-> IR_GYM (260 Ironreach)!
        - Kaito's Plaque ("DON'T FIGHT THE ONE IN FRONT OF YOU. MOVE IT."), Gym Guide (explains Colosseum
          crowd roar + pursuer/rope/boulder/plate rules!), Ring Medic (free full heal), Odessa (spawns after
          V130 >= 6 / Badge 8 win to deliver HM02 Fly!), visible HYPERPOTION (hidden=False), canonical PBS
          trainer [BLACKBELT, Goro] (100% open sightline), North Archway Portal (10, 4) -> 271!
  - Map 271: Ironreach Gym - Puzzle Room 1    ("Sparring Floor" — TEACH + TWIST, 29x25, TS 57, :COLOSSEUM)
      * West Half "The Pillar" (TEACH): 1 sparring pursuer (Followers/MACHOP) + 3x3 stone pillar + north bell
        -> rings S344 (G8_TEACH_BELL) unlocking the iron bar gate into the East Half!
      * East Half "Rope Line" (TWIST): 2 sparring pursuers (Followers/MAKUHITA & HITMONLEE) + golden-hemp
        colosseum rope line (pas=0x0 to player, blocks pursuers!) with 1 gap & corner catch-pockets -> rings
        S340 (G8_BELL_1) unlocking the North Gate (21, 4) -> 272!
      * Safe South Foyer: Apprentice Hiro (status, instant reset, 3-tier hints V342, puzzleskip S301), Iron
        Reset Bell, visible FULLHEAL (hidden=False), BOTH canonical PBS trainers [CRUSHGIRL, Mika] &
        [BLACKBELT, Hideo] (100% open sightlines!).
  - Map 272: Ironreach Gym - Puzzle Room 2    ("Boulder & Rope Ring" — COMBINE, 29x25, TS 57, :COLOSSEUM)
      * Combines Strength boulders (pbStrength / pfp_push), iron pressure plates (lm_grate_off -> lm_grate),
        colosseum rope lines, and 2 sparring pursuers (Followers/HITMONCHAN & HARIYAMA):
        - Bait each pursuer behind its pen rope, then push each Strength boulder into the 1-tile rope gap onto
          Plate P1 (6,11) & Plate P2 (22,11) — simultaneously LOCKING both pursuers behind the ropes AND holding
          both plates down to unlock the Central Rope-Ring Bell (14, 11) -> S341 (G8_BELL_2) -> North Gate -> 273!
      * Safe South Foyer: Apprentice Hiro (V343 hints, reset, S301 skip), Iron Reset Bell (zero boulder-push
        softlocks!), BOTH canonical PBS trainers [CRUSHGIRL, Aiko] & [CRUSHKIN, Jin & Rei] (double battle!
        Jin trainer_BLACKBELT + visible partner Rei trainer_CRUSHGIRL beside him, 100% open sightlines!).
  - Map 273: Ironreach Gym - Puzzle Room 3    ("The Gauntlet & Marrowgate Door", 29x25, TS 57, :COLOSSEUM)
      * West Main Arena ("The Gauntlet" -> S342 G8_GAUNTLET): 2 sparring pursuers (Followers/MACHAMP & CONKELDURR),
        3 Strength boulders, rope bars, stone bastion & 2 iron plates (P1=(10,6), P2=(10,14)) -> holding both
        simultaneously unlocks the North Arena Gate (10, 4) -> 274 Warden Arena!
      * East Side Alcove ("Marrowgate Door" — OPTIONAL MASTERY -> S343 G8_MARROWGATE):
        - 2 plates (M1=(22,9), M2=(25,11)), ONLY 1 Strength boulder, rope barrier (24..26, 12), and 1 sparring
          pursuer (Followers/MACHOKE): push the boulder onto M1 AND stand south of the rope at (25, 13) to lure
          the sparring partner onto M2 (because a sparring partner weighs as much as a boulder!) -> unlocks
          Marrowgate Mastery Coffer (TELLURICSEED x2 + BLACKBELT + EXPERTBELT) + Kaito bonus dialogue!
      * Safe South Foyer: Apprentice Hiro (V344 hints, reset, S301 skip), independent Gauntlet & Marrowgate
        Reset Bells (zero softlocks!), canonical PBS trainer [CUEBALL, Tetsu] (100% open sightline!).
  - Map 274: Ironreach Gym - Warden Arena     ("The Pit", 21x17, TS 57, :COLOSSEUM)
      * Dramatic subterranean iron colosseum pit: elevated northern ring dais, roped red earth battle floor,
        4 intact blazing braziers (0 detached pf_glow!), iron spectator galleries, full-width 3-wide south exit
        carpet (9..11, 16) -> 273, framed East Fast-Exit Iron Cage Lift (16, 13) -> 270 with solid readable
        signpost on adjacent non-warp tile (15, 12)!
      * Kaito's Lucario ("Memory") + Warden Kaito Ren (KAITO sprite): win-checked
        Prismfall.gym_battle(pfm_gym(:LEADER_KAITO), double: false), Prismfall.award_badge(pfm_gym(:LEADER_KAITO)),
        TM31 Brick Break, S343 Marrowgate Mastery reaction, advances V130 CH9_STEP >= 6 (spawns Odessa at 270!).

Canonical sources:
  - design/GYM_PUZZLES.md (Gym 8: S340-S343, V340-V341 — verified 0 collisions repo-wide!)
  - story/27_SCRIPT_CH9.md (Maps 270-275 dialogue, Gym Guide, Hiro, Kaito, Odessa HM02 Fly, Marrowgate!)
  - pbs/trainers.txt (Goro, Mika, Hideo, Aiko, Jin & Rei, Tetsu, LEADER_KAITO — verified global_count == 1)

Run:
    /usr/bin/python3 -I mapgen/layouts/ironreach_gym.py
"""
import heapq
import os
import re
import subprocess
import sys
import tempfile
from collections import deque
import numpy as np
import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cavekit import Cave, FLOOR, TER, MASS, P1
import rkit as K
from rkit import STAMPS
import rcompose as RC
import render as R
import passguard as PG

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(HERE, 'data', 'raw')
SPEC_DIR = os.path.join(HERE, 'specs')

TID = 57
FIELD = 'COLOSSEUM'
IRONREACH_POS = [0, 16, 13]

# Canonical Gym 8 Switch & Variable IDs (strictly within 340..344 — ZERO collisions repo-wide!)
S_BELL_1 = 340          # G8_BELL_1: 271 East Bell rung -> opens gate to 272
S_BELL_2 = 341          # G8_BELL_2: 272 Central Bell rung -> opens gate to 273
S_GAUNTLET = 342        # G8_GAUNTLET: 273 Main Gauntlet plates held -> opens gate to 274
S_MARROWGATE = 343      # G8_MARROWGATE: 273 Marrowgate Mastery Alcove solved (boulder + pursuer on plates!)
S_TEACH_BELL = 344      # G8_TEACH_BELL: 271 West Pillar Bell rung -> opens divider gate into East Half
S_PUZZLE_SKIP = 301     # Core PUZZLE_SKIP mirror

V_ROUNDS = 340          # G8_ROUNDS: sparring contacts / resets
V_PUSHES = 341          # G8_PUSHES: boulder pushes counter
V_HINT_271 = 342        # Hiro hint counter in 271
V_HINT_272 = 343        # Hiro hint counter in 272
V_HINT_273 = 344        # Hiro hint counter in 273
V_CH9_STEP = 130        # CH9_STEP (story/27_SCRIPT_CH9.md: 6 = Gym 8 won -> Odessa Fly at 270!)

# Verified TS 57 (PF Rejuv Cave) Tile IDs (ALL visually & programmatically verified!)
T_ROPE_H = 14525                     # pas=0x0, pri=0 (warm golden step-over horizontal colosseum ring rope!)
T_ROPE_V = 14549                     # pas=0x0, pri=0 (warm golden step-over vertical ring rope — west/left edge!)
T_ROPE_VR = 14550                    # pas=0x0, pri=0 (warm golden step-over vertical ring rope — east/right edge!)
T_ROPE_NW = 14533                    # pas=0x0, pri=0 (warm golden ring rope NW corner!)
T_ROPE_NE = 14534                    # pas=0x0, pri=0 (warm golden ring rope NE corner!)
T_ROPE_ALL = {T_ROPE_H, T_ROPE_V, T_ROPE_VR, T_ROPE_NW, T_ROPE_NE}
T_PLATE_OFF = P1('lm_grate_off')     # 24394, pas=0x0 (unpressed cold-iron pressure plate)
T_PLATE_ON = P1('lm_grate')          # 24393, pas=0x0 (pressed amber-lit iron pressure plate!)
T_GATE_SHUT = P1('lm_pdoor')         # 25935, pas=0xf (heavy riveted steel sluice shutter with red lock — ZERO 23998 ladders!)
T_BARS_SHUT = P1('lm_latch')         # 25937, pas=0xf (heavy locked iron/brass barred arena gate — ZERO 23998 ladders!)
T_PDOOR_OPEN = P1('lm_pdoor_open')   # 25936, pas=0x0 (open dark colosseum doorway portal)
T_CHEST_SHUT = P1('mn_trunk')        # 24344, pas=0xf (sealed Marrowgate Mastery coffer)
T_CHEST_OPEN = P1('mn_trunk_open')   # 24345, pas=0xf (opened Marrowgate Mastery coffer)
T_LAMP_OFF = P1('lm_lamp')           # 25931, pas=0xf (unlit iron portal indicator lamp)
T_LAMP_ON = P1('lm_lamp_on')         # 25932, pas=0xf (lit iron portal indicator lamp)
T_POST = P1('cv_post')               # solid dark timber/iron pit post
T_RAIL_W, T_RAIL_M, T_RAIL_E = P1('qy_rail_w'), P1('qy_rail_m'), P1('qy_rail_e')
T_WALL_V = P1('nr_wall_v')           # 22719, pas=0xf (seamless vertical ironstone brick divider wall!)
T_PAL_V = P1('wr_pal_v')             # 23254, pas=0xf (seamless vertical timber spectator-gallery rail!)

BOULDER_SPRITE = 'pf_cave_boulder_L'   # Verified on disk: dark Nadir ironstone Strength boulder!


# =================================================================================================
# Shared Colosseum Architecture, Anti-P0 Verification & Pursuer-Engine Code Generators
# =================================================================================================
def _setup_iron_kits():
    for base_k, new_k in (('cvL', 'cvL2'), ('qy', 'qy2'), ('cvT', 'cvT2'), ('cvE', 'cvE2')):
        K.KITS[new_k] = dict(K.KITS[base_k], rows=[K.KITS[base_k]['rows'][0], K.KITS[base_k]['rows'][2]])


def _new_pit_hall(W, H, seed, wall_kit='qy2', ter_kit='qy2'):
    """Create a subterranean ironstone masonry colosseum chamber (dark qy2 stone — ZERO icy glacier cvL2!)."""
    _setup_iron_kits()
    m = Cave(W, H, 'L', seed=seed, pool='Cave Pool', tid=TID)
    m.STAIRS = (P1('st_stair_l'), P1('st_stair_m'), P1('st_stair_r'))
    m.kit = {TER: ter_kit, FLOOR: wall_kit, MASS: wall_kit, 'default': wall_kit}
    return m


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


def _paint_pit_floors(m, zones):
    palettes = {
        'sand': [P1('E_f%d' % i) for i in range(4)],
        'flag': [P1('T_f%d' % i) for i in range(4)],
        'slate': [P1('L_f%d' % i) for i in range(4)],
        'iron': [P1('Q_f%d' % i) for i in range(4)],
        'timber': [P1('N_f%d' % i) for i in range(4)],
        'soot': [P1('cv_mud%d' % i) for i in range(4)],
    }
    floorpatch_ids = {P1(k) for k in STAMPS if k.startswith(('L_floorpatch_', 'E_floorpatch_'))}
    for x0, y0, x1, y1, kind in zones:
        pal = palettes[kind]
        for y in range(max(0, y0), min(m.H, y1 + 1)):
            for x in range(max(0, x0), min(m.W, x1 + 1)):
                if m.cls[y, x] != '.' or m.cliff[y, x]:
                    continue
                if int(m.L[1, y, x]) in floorpatch_ids:
                    m.L[1, y, x] = 0
                m.L[0, y, x] = pal[(x * 3 + y * 5) % len(pal)]


def _paint_crimson_runner(m, x0, y0, x1, y1, medallion_y=None):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if not m.inb(x, y) or m.cls[y, x] != '.' or m.cliff[y, x] or m.L[1, y, x] != 0:
                continue
            if x == x0:
                t = P1('mn_rugR_w')
            elif x == x1:
                t = P1('mn_rugR_e')
            elif medallion_y is not None and y == medallion_y:
                t = P1('mn_rugR_c2')
            else:
                t = P1('mn_rugR_c')
            m.L[1, y, x] = t


def _paint_ropes(m, ropes_h, ropes_v, ropes_vr=(), ropes_nw=(), ropes_ne=()):
    """Paint warm golden step-over colosseum ring rope lines cleanly onto L[1] (100% live pas=0x0!)."""
    ts = R.tilesets()[TID]
    for tid_r in T_ROPE_ALL:
        assert ts['passages'][tid_r] == 0x0, f'Rope tile {tid_r} is NOT pas=0x0!'
    for rx, ry in ropes_h:
        m.L[1, ry, rx] = T_ROPE_H
    for rx, ry in ropes_v:
        m.L[1, ry, rx] = T_ROPE_V
    for rx, ry in ropes_vr:
        m.L[1, ry, rx] = T_ROPE_VR
    for rx, ry in ropes_nw:
        m.L[1, ry, rx] = T_ROPE_NW
    for rx, ry in ropes_ne:
        m.L[1, ry, rx] = T_ROPE_NE


def _add_shafts(Lr, pts, label='Gym'):
    """Overhead cavern light shafts strictly on 100% unoccupied L[2] cells (ZERO clipping, ZERO pf_glow!)."""
    H, W = Lr.shape[1:]
    ov = RC.resolve(np.array(STAMPS['cv_shaft']['layers'], dtype=np.int32), TID)
    for ox, oy in pts:
        for dy in range(ov.shape[1]):
            for dx in range(ov.shape[2]):
                t = int(ov[2, dy, dx] or ov[1, dy, dx] or ov[0, dy, dx])
                xx, yy = ox + dx, oy + dy
                if t:
                    assert 0 <= xx < W and 0 <= yy < H and int(Lr[2, yy, xx]) == 0, (
                        f'{label}: cv_shaft ({ox},{oy}) clipped at ({xx},{yy}) (L2={Lr[2, yy, xx]})!'
                    )
                    Lr[2, yy, xx] = t


def _assert_braziers_intact(Lr, braziers, label):
    br_ref = RC.resolve(np.array(STAMPS['fw_brazier']['layers'], dtype=np.int32), TID)
    flame_tid = int(br_ref[2, 0, 0])
    base_tid = int(br_ref[1, 1, 0])
    for bx, by in braziers:
        assert int(Lr[2, by, bx]) == flame_tid, f'{label}: fw_brazier flame damaged at ({bx},{by})!'
        assert int(Lr[1, by + 1, bx]) == base_tid, f'{label}: fw_brazier base damaged at ({bx},{by+1})!'


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


def _visible_item(at, item_id):
    return {'type': 'item', 'name': 'Item', 'at': list(at), 'item': item_id, 'hidden': False}


def _trainer(at, ttype, name, d, intro, after, sight=3, double=False, sprite_override=None):
    rules = ['setBattleRule("field", :%s)' % FIELD]
    if double:
        rules.append('setBattleRule("double")')
    return {
        'type': 'trainer',
        'name': 'Trainer(%d)' % sight,
        'at': list(at),
        'sight': sight,
        'dir': d,
        'sprite': sprite_override or ('trainer_' + ttype),
        'trainer': [ttype, name],
        'intro': intro,
        'after': after,
        'rules': rules,
    }


def _gate_event(name, at, open_sw, locked_msg, tile_id=None):
    """Heavy steel sluice shutter / iron-bars arena gate (pas=0xf when locked -> blank walkable when open_sw ON!)."""
    gid = tile_id if tile_id is not None else T_GATE_SHUT
    assert gid != 23998, 'FORBIDDEN wooden ladder tile 23998 on gate!'
    return {
        'type': 'event',
        'name': name,
        'at': list(at),
        'pages': [
            {
                'graphic': {'tile': gid},
                'trigger': 'action',
                'commands': [locked_msg],
            },
            {
                'cond': {'switch': open_sw},
                'through': True,
                'trigger': 'action',
                'commands': [],
            },
        ],
    }


def _lamp_event(name, at, lit_sw):
    return {
        'type': 'event',
        'name': name,
        'at': list(at),
        'pages': [
            {'graphic': {'tile': T_LAMP_OFF}, 'trigger': 'action', 'commands': ["An iron signal lamp — unlit until the ring's trial is cleared."]},
            {'cond': {'switch': lit_sw}, 'graphic': {'tile': T_LAMP_ON}, 'trigger': 'action', 'commands': ["The iron signal lamp blazes bright — the gate stands open!"]},
        ],
    }


def _plate_event(name, at):
    """Walkable iron pressure plate indicator (through=True, trigger='touch', commands=[] -> 0 over_trigger traps!).
    Switches visually from cold dark grate (T_PLATE_OFF) to warm ember-lit grate (T_PLATE_ON) on self switch A.
    """
    return {
        'type': 'event',
        'name': name,
        'at': list(at),
        'pages': [
            {'graphic': {'tile': T_PLATE_OFF}, 'through': True, 'trigger': 'touch', 'commands': []},
            {'cond': {'self': 'A'}, 'graphic': {'tile': T_PLATE_ON}, 'through': True, 'trigger': 'touch', 'commands': []},
        ],
    }


def _pursuer_event(name, at, sprite, done_sw, active_msg, done_msg):
    """Sparring partner pursuer event (stops & bows politely once done_sw is ON!)."""
    return {
        'type': 'event',
        'name': name,
        'at': list(at),
        'pages': [
            {
                'graphic': {'sprite': sprite, 'dir': 'down'},
                'trigger': 'action',
                'move': 'fixed',
                'commands': [active_msg],
            },
            {
                'cond': {'switch': done_sw},
                'graphic': {'sprite': sprite, 'dir': 'down'},
                'trigger': 'action',
                'move': 'fixed',
                'commands': [done_msg],
            },
        ],
    }


def _ruby_pts(pts):
    return '[' + ', '.join(f'[{x}, {y}]' for (x, y) in sorted(pts)) + ']'


def _build_plate_eval_ruby(map_id, plates, heavy_names, done_sw, unlock_msg, unlock_flash=False):
    """Generate Ruby snippet that updates all plate visuals (self switch A) & unlocks done_sw when ALL plates held!"""
    plates_rb = '[' + ', '.join(f'[{nm!r}, {x}, {y}]' for (nm, x, y) in plates) + ']'
    heavy_rb = '[' + ', '.join(repr(n) for n in heavy_names) + ']'
    flash_line = '      pfm_flash(100, 170, 255, 10, 140)\n' if unlock_flash else ''
    return (
        f'      _plates = {plates_rb}\n'
        f'      _heavy = {heavy_rb}.map {{ |n| pfp_ev(n) }}.compact\n'
        f'      _all_held = true\n'
        f'      _new_latch = false\n'
        f'      _plates.each do |pnm, px, py|\n'
        f'        _held = _heavy.any? {{ |he| he.x == px && he.y == py }}\n'
        f'        _all_held = false if !_held\n'
        f'        _pev = pfp_ev(pnm)\n'
        f'        if _pev\n'
        f'          _was = $game_self_switches[[{map_id}, _pev.id, "A"]]\n'
        f'          _new_latch = true if _held && !_was\n'
        f'          $game_self_switches[[{map_id}, _pev.id, "A"]] = _held\n'
        f'        end\n'
        f'      end\n'
        f'      pbSEPlay("Mining iron", 85, 105) if _new_latch\n'
        f'      $game_map.need_refresh = true\n'
        f'      if _all_held && !$game_switches[{done_sw}]\n'
        f'        $game_switches[{done_sw}] = true\n'
        f'        pbSEPlay("Mining iron", 95, 90)\n'
        f'        pfm_shake(3, 10, 10)\n'
        f'{flash_line}'
        f'        $game_map.need_refresh = true\n'
        f'        pbMessage(_INTL({unlock_msg!r}))\n'
        f'      end\n'
    )


def _boulder_event(name, at, map_id, ropes, plates, heavy_names, done_sw=None, unlock_msg=None, unlock_flash=False,
                   bell_announce_msg=None, blocked_pts=()):
    """Pushable iron-banded Strength boulder (pf_cave_boulder_L) strictly gated on pbStrength return value!
    Also blocks pushing onto golden rope lines OR protected doorway/warp sills (blocked_pts).
    """
    ropes_rb = _ruby_pts(ropes)
    blocked_rb = _ruby_pts(blocked_pts)
    if done_sw is not None:
        plate_block = _build_plate_eval_ruby(map_id, plates, heavy_names, done_sw, unlock_msg, unlock_flash)
    else:
        plates_rb = '[' + ', '.join(f'[{nm!r}, {x}, {y}]' for (nm, x, y) in plates) + ']'
        heavy_rb = '[' + ', '.join(repr(n) for n in heavy_names) + ']'
        plate_block = (
            f'      _plates = {plates_rb}\n'
            f'      _heavy = {heavy_rb}.map {{ |n| pfp_ev(n) }}.compact\n'
            f'      _all_held = true\n'
            f'      _new_latch = false\n'
            f'      _plates.each do |pnm, px, py|\n'
            f'        _held = _heavy.any? {{ |he| he.x == px && he.y == py }}\n'
            f'        _all_held = false if !_held\n'
            f'        _pev = pfp_ev(pnm)\n'
            f'        if _pev\n'
            f'          _was = $game_self_switches[[{map_id}, _pev.id, "A"]]\n'
            f'          _new_latch = true if _held && !_was\n'
            f'          $game_self_switches[[{map_id}, _pev.id, "A"]] = _held\n'
            f'        end\n'
            f'      end\n'
            f'      pbSEPlay("Mining iron", 85, 105) if _new_latch\n'
            f'      $game_map.need_refresh = true\n'
            f'      if _all_held && _new_latch\n'
            f'        pfm_shake(3, 10, 8)\n'
            f'        pbMessage(_INTL({bell_announce_msg!r}))\n'
            f'      end\n'
        )
    ruby = (
        f'_ev = get_self\n'
        f'_dir = $game_player.direction\n'
        f'_ddx, _ddy = PrismfallPuzzles::DIRS[_dir]\n'
        f'_nx, _ny = _ev.x + _ddx, _ev.y + _ddy\n'
        f'_ropes = {ropes_rb}\n'
        f'_blocked = {blocked_rb}\n'
        f'if _ropes.include?([_nx, _ny])\n'
        f'  pbSEPlay("Player bump", 75, 100)\n'
        f'  pbMessage(_INTL("The iron-banded boulder catches on the taut golden ring rope and refuses to cross it."))\n'
        f'elsif _blocked.include?([_nx, _ny])\n'
        f'  pbSEPlay("Player bump", 75, 100)\n'
        f'  pbMessage(_INTL("The raised steel doorway sill stops the boulder from entering the gate passage."))\n'
        f'else\n'
        f'  _can_push = ($PokemonMap && $PokemonMap.strengthUsed) || (defined?(pbStrength) && pbStrength)\n'
        f'  if _can_push\n'
        f'    if pfp_push(true)\n'
        f'      $game_variables[{V_PUSHES}] = $game_variables[{V_PUSHES}].to_i + 1\n'
        f'{plate_block}'
        f'    else\n'
        f'      pbSEPlay("Player bump", 75, 100)\n'
        f'    end\n'
        f'  end\n'
        f'end'
    )
    return {
        'type': 'event',
        'name': name,
        'at': list(at),
        'pages': [{
            'graphic': {'sprite': BOULDER_SPRITE, 'dir': 'down'},
            'trigger': 'action',
            'dir_fix': True,
            'commands': [{'script': ruby}],
        }],
    }


def _step_hook_installer(map_id, hook_key, zones):
    """Build a Parallel event that syncs plate visuals once per map entry AND installs step_hook(map_id, hook_key)."""
    blocks = []
    sync_blocks = []
    for z in zones:
        x0, y0, x1, y1 = z['box']
        dsw = z['done_sw']
        ropes_rb = _ruby_pts(z['ropes'])
        purs_rb = '[' + ', '.join(f'[{n!r}, {x}, {y}]' for (n, x, y) in z['pursuers']) + ']'
        blds_rb = '[' + ', '.join(f'[{n!r}, {x}, {y}]' for (n, x, y) in z.get('boulders', [])) + ']'
        plates = z.get('plates', [])
        rx, ry = z['reset_pl']
        heavy_names = [n for (n, _, _) in z['pursuers']] + [n for (n, _, _) in z.get('boulders', [])]

        if plates:
            plates_rb = '[' + ', '.join(f'[{nm!r}, {x}, {y}]' for (nm, x, y) in plates) + ']'
            heavy_rb = '[' + ', '.join(repr(n) for n in heavy_names) + ']'
            sync_blocks.append(
                f'  _s_plates = {plates_rb}\n'
                f'  _s_heavy = {heavy_rb}.map {{ |n| pfp_ev(n) }}.compact\n'
                f'  _s_plates.each do |pnm, px, py|\n'
                f'    _pev = pfp_ev(pnm)\n'
                f'    next if !_pev\n'
                f'    _held = _s_heavy.any? {{ |he| he.x == px && he.y == py }}\n'
                f'    if $game_self_switches[[{map_id}, _pev.id, "A"]] != _held\n'
                f'      $game_self_switches[[{map_id}, _pev.id, "A"]] = _held\n'
                f'      _sync_dirty = true\n'
                f'    end\n'
                f'  end'
            )

        plate_eval = ''
        if plates and z.get('auto_unlock'):
            plate_eval = _build_plate_eval_ruby(
                map_id, plates, heavy_names, dsw, z['unlock_msg'], z.get('unlock_flash', False)
            )
        elif plates:
            plates_rb = '[' + ', '.join(f'[{nm!r}, {x}, {y}]' for (nm, x, y) in plates) + ']'
            heavy_rb = '[' + ', '.join(repr(n) for n in heavy_names) + ']'
            plate_eval = (
                f'      _plates = {plates_rb}\n'
                f'      _heavy = {heavy_rb}.map {{ |n| pfp_ev(n) }}.compact\n'
                f'      _plates.each do |pnm, px, py|\n'
                f'        _pev = pfp_ev(pnm)\n'
                f'        $game_self_switches[[{map_id}, _pev.id, "A"]] = _heavy.any? {{ |he| he.x == px && he.y == py }} if _pev\n'
                f'      end\n'
                f'      $game_map.need_refresh = true\n'
            )

        clear_plates_rb = ''
        if plates:
            pnames_rb = '[' + ', '.join(repr(nm) for (nm, _, _) in plates) + ']'
            clear_plates_rb = (
                f'          {pnames_rb}.each {{ |pnm| _pe = pfp_ev(pnm); $game_self_switches[[{map_id}, _pe.id, "A"]] = false if _pe }}\n'
            )

        blk = (
            f'    if !$game_switches[{dsw}] && plx >= {x0} && plx <= {x1} && ply >= {y0} && ply <= {y1}\n'
            f'      _ropes = {ropes_rb}\n'
            f'      _purs = {purs_rb}\n'
            f'      _blds = {blds_rb}\n'
            f'      _purs.each do |pnm, _sx, _sy|\n'
            f'        ev = pfp_ev(pnm)\n'
            f'        next if !ev\n'
            f'        dx = plx - ev.x\n'
            f'        dy = ply - ev.y\n'
            f'        if dx.abs + dy.abs > 1\n'
            f'          horiz = dx > 0 ? 6 : (dx < 0 ? 4 : nil)\n'
            f'          vert  = dy > 0 ? 2 : (dy < 0 ? 8 : nil)\n'
            f'          order = (dx.abs >= dy.abs) ? [horiz, vert] : [vert, horiz]\n'
            f'          order.compact.each do |d|\n'
            f'            ddx, ddy = PrismfallPuzzles::DIRS[d]\n'
            f'            nx, ny = ev.x + ddx, ev.y + ddy\n'
            f'            next if [nx, ny] == [plx, ply] || _ropes.include?([nx, ny])\n'
            f'            next if !PrismfallPuzzles.can_shift?(ev, d)\n'
            f'            ev.direction = d\n'
            f'            PrismfallPuzzles.shift(ev, d)\n'
            f'            break\n'
            f'          end\n'
            f'        end\n'
            f'      end\n'
            f'{plate_eval}'
            f'      if !$game_switches[{dsw}] && !_ropes.include?([plx, ply])\n'
            f'        _hit = _purs.any? {{ |pnm, _sx, _sy| ev = pfp_ev(pnm); ev && (ev.x - plx).abs + (ev.y - ply).abs <= 1 }}\n'
            f'        if _hit\n'
            f'          pbSEPlay("Battle damage normal", 85, 100)\n'
            f'          pfm_shake(3, 10, 8)\n'
            f'          $game_variables[{V_ROUNDS}] = $game_variables[{V_ROUNDS}].to_i + 1\n'
            f'          pbMessage(_INTL("Kaito\'s voice echoes from the iron rafters: \\"Tagged! Stand up. Again.\\""))\n'
            f'          pbFadeOutIn do\n'
            f'            _purs.each {{ |pnm, sx, sy| ev = pfp_ev(pnm); if ev; ev.moveto(sx, sy); ev.direction = 2; end }}\n'
            f'            _blds.each {{ |bnm, sx, sy| ev = pfp_ev(bnm); ev.moveto(sx, sy) if ev }}\n'
            f'{clear_plates_rb}'
            f'            $game_player.moveto({rx}, {ry})\n'
            f'            $game_player.direction = 8\n'
            f'            $game_player.straighten\n'
            f'            $game_map.need_refresh = true\n'
            f'          end\n'
            f'          PrismfallPuzzles.reset_trail\n'
            f'        end\n'
            f'      end\n'
            f'    end'
        )
        blocks.append(blk)

    sync_prefix = ''
    if sync_blocks:
        sync_prefix = (
            f'if !@pf_plate_synced\n'
            f'  @pf_plate_synced = true\n'
            f'  _sync_dirty = false\n'
            + '\n'.join(sync_blocks) + '\n'
            f'  $game_map.need_refresh = true if _sync_dirty\n'
            f'end\n'
        )

    ruby = (
        sync_prefix
        + f'if !PrismfallPuzzles::STEP_HOOKS[{map_id}] || !PrismfallPuzzles::STEP_HOOKS[{map_id}][:{hook_key}]\n'
        + f'  pfp_step_hook({map_id}, :{hook_key}) do |_from, to|\n'
        + f'    plx, ply = to[0], to[1]\n'
        + '\n'.join(blocks) + '\n'
        + f'  end\n'
        + f'end'
    )
    return {
        'type': 'event',
        'name': f'Pit Step Hook {map_id}',
        'at': [0, 0],
        'pages': [{
            'trigger': 'parallel',
            'through': True,
            'commands': [{'script': ruby}],
        }],
    }


def _reset_ruby(map_id, resets, plates, reset_pl):
    """Generate clean fade-reset Ruby for Hiro & Iron Reset Bells (ZERO boulder-push softlocks!)."""
    res_rb = '[' + ', '.join(f'[{n!r}, {x}, {y}]' for (n, x, y) in resets) + ']'
    pnames_rb = '[' + ', '.join(repr(nm) for (nm, _, _) in plates) + ']'
    rx, ry = reset_pl
    return (
        f'pbSEPlay("Mining iron", 90, 95)\n'
        f'pbFadeOutIn do\n'
        f'  {res_rb}.each {{ |nm, sx, sy| ev = pfp_ev(nm); if ev; ev.moveto(sx, sy); ev.direction = 2; end }}\n'
        f'  {pnames_rb}.each {{ |pnm| pe = pfp_ev(pnm); $game_self_switches[[{map_id}, pe.id, "A"]] = false if pe }}\n'
        f'  $game_variables[{V_PUSHES}] = 0\n'
        f'  $game_player.moveto({rx}, {ry})\n'
        f'  $game_player.direction = 8\n'
        f'  $game_player.straighten\n'
        f'  $game_map.need_refresh = true\n'
        f'end\n'
        f'PrismfallPuzzles.reset_trail'
    )


def _hiro_event(at, map_id, room_title, status_ruby, reset_code, hint_var, hints, skip_ruby, reset_choices=None):
    """Apprentice Hiro: Status / Reset (single or multi-zone menu!) / 3-tier Progressive Hint / Skip (S301) / Leave."""
    h1, h2, h3 = hints
    if reset_choices:
        rc_labels = ', '.join(f'_INTL({lbl!r})' for (lbl, _, _) in reset_choices) + ', _INTL("Cancel")'
        rc_cases = []
        for idx, (lbl, rcode, rmsg) in enumerate(reset_choices):
            rc_cases.append(
                f'    when {idx}\n'
                f'      $game_variables[{V_ROUNDS}] = $game_variables[{V_ROUNDS}].to_i + 1\n'
                + '\n'.join('      ' + ln for ln in rcode.splitlines()) + '\n'
                + f'      pbMessage(_INTL({rmsg!r}))\n'
                + f'      _loop = false'
            )
        reset_branch = (
            f'    _rc = pbMessage(_INTL("Which section should I reset?"), [{rc_labels}], {len(reset_choices) + 1})\n'
            f'    case _rc\n'
            + '\n'.join(rc_cases) + '\n'
            f'    end\n'
        )
    else:
        reset_branch = (
            f'    $game_variables[{V_ROUNDS}] = $game_variables[{V_ROUNDS}].to_i + 1\n'
            + '\n'.join('    ' + ln for ln in reset_code.splitlines()) + '\n'
            f'    pbMessage(_INTL("Apprentice Hiro: Boulders and sparring partners are back on their chalk marks. Fresh stance!"))\n'
            f'    _loop = false\n'
        )

    ruby = (
        f'pbMessage(_INTL("Apprentice Hiro: Welcome to {room_title}! Discipline over rage — need a ring reset or a coaching tip?"))\n'
        f'_loop = true\n'
        f'while _loop\n'
        f'  _cmds = [_INTL("Room Status"), _INTL("Reset the Room"), _INTL("Coaching Hint")]\n'
        f'  _cmds.push(_INTL("Skip this Room")) if (pfp_skip? rescue false)\n'
        f'  _cmds.push(_INTL("Leave"))\n'
        f'  _c = pbMessage(_INTL("What\'ll it be, challenger?"), _cmds, _cmds.length)\n'
        f'  case _cmds[_c]\n'
        f'  when _INTL("Room Status")\n'
        f'{status_ruby}\n'
        f'  when _INTL("Reset the Room")\n'
        f'{reset_branch}'
        f'  when _INTL("Coaching Hint")\n'
        f'    $game_variables[{hint_var}] = $game_variables[{hint_var}].to_i + 1\n'
        f'    _tier = [$game_variables[{hint_var}].to_i, 3].min\n'
        f'    if _tier == 1\n'
        f'      pbMessage(_INTL("Apprentice Hiro (Hint 1/3): {h1}"))\n'
        f'    elsif _tier == 2\n'
        f'      pbMessage(_INTL("Apprentice Hiro (Hint 2/3): {h2}"))\n'
        f'    else\n'
        f'      pbMessage(_INTL("Apprentice Hiro (Hint 3/3): {h3}"))\n'
        f'    end\n'
        f'  when _INTL("Skip this Room")\n'
        f'    if pbConfirmMessage(_INTL("Have Apprentice Hiro open this room\'s gate for you?"))\n'
        + '\n'.join('      ' + ln for ln in skip_ruby.splitlines()) + '\n'
        f'      pbMessage(_INTL("Apprentice Hiro: Gate\'s unlatched. Go show Kaito what you\'ve got."))\n'
        f'      _loop = false\n'
        f'    end\n'
        f'  else\n'
        f'    _loop = false\n'
        f'  end\n'
        f'end'
    )
    return {
        'type': 'event',
        'name': 'Apprentice Hiro',
        'at': list(at),
        'pages': [{
            'graphic': {'sprite': 'NPC 08', 'dir': 'down'},
            'trigger': 'action',
            'move': 'fixed',
            'commands': [{'script': ruby}],
        }],
    }


def _check_ruby_syntax(events, label):
    scripts = []

    def _walk(cmds):
        for c in cmds or []:
            if isinstance(c, dict):
                if 'script' in c:
                    scripts.append(c['script'])
                if 'then' in c:
                    _walk(c['then'])
                if 'else' in c:
                    _walk(c['else'])

    for e in events:
        if e.get('type') == 'event':
            for pg in e.get('pages') or []:
                _walk(pg.get('commands'))
        elif e.get('type') in ('npc', 'sign'):
            _walk(e.get('commands'))

    for idx, sc in enumerate(scripts):
        assert 'pbShake' not in sc, f'{label} script #{idx} uses forbidden pbShake!'
        for line in sc.splitlines():
            s = line.strip()
            assert not re.match(r'^return\b', s), f'{label} script #{idx} has bare return: {s!r}'
        with tempfile.NamedTemporaryFile('w', suffix='.rb', delete=False) as tf:
            tf.write(sc + '\n')
            tp = tf.name
        try:
            res = subprocess.run(['ruby', '-c', tp], capture_output=True, text=True)
            assert res.returncode == 0, f'{label} script #{idx} ruby -c FAIL:\n{res.stderr}\n---\n{sc}'
        finally:
            os.unlink(tp)


def _ev_active_page(e, sw):
    pages = e.get('pages') or [{}]
    for pg in reversed(pages):
        c = pg.get('cond') or {}
        if 'switch' in c and not sw.get(c['switch'], False):
            continue
        if 'switch2' in c and not sw.get(c['switch2'], False):
            continue
        if 'self' in c:
            continue
        if 'var' in c:
            continue
        return pg
    return None


def _verify_gym_map(Lr, events, start, targets, label, exit_row, sw=None):
    import build as B
    sw = sw or {}
    ts = R.tilesets()[TID]
    _, H, W = Lr.shape
    max_tid = len(ts['passages'])
    assert (Lr[0] > 0).all(), f'{label}: void L[0]!'
    assert (Lr >= 0).all() and (Lr < max_tid).all(), f'{label}: OOB tile ID!'
    assert not (Lr == 23998).any(), f'{label}: FORBIDDEN wooden-ladder tile 23998 found in map layers!'

    ev_pts = [tuple(e['at']) for e in events if e and e.get('at')]
    PG.guard(Lr, TID, ev_pts, label)
    assert not PG.hits(Lr, ts, ev_pts), f'{label}: passguard hits!'

    # Anti-P0 #1: ZERO over_trigger? traps, ZERO NPCs/Trainers on solid tiles, ZERO 23998 ladder gates!
    for e in events:
        et = e.get('type')
        ax, ay = int(e['at'][0]), int(e['at'][1])
        if et == 'sign':
            assert not B.cell_passable(Lr, ts, ax, ay), f'{label}: sign {e.get("name")} at {(ax,ay)} on passable tile!'
        elif et in ('trainer', 'npc'):
            assert B.cell_passable(Lr, ts, ax, ay), f'{label}: {et} {e.get("name")} at {(ax,ay)} on SOLID tile!'
        elif et == 'event':
            for pg_i in (e.get('pages') or []):
                assert (pg_i.get('graphic') or {}).get('tile') != 23998, f'{label}: FORBIDDEN 23998 ladder graphic on {e.get("name")}!'
            pg0 = (e.get('pages') or [{}])[0]
            trig = pg0.get('trigger', 'action')
            g = pg0.get('graphic') or {}
            if g.get('sprite'):
                assert B.cell_passable(Lr, ts, ax, ay), f'{label}: sprite {e.get("name")} at {(ax,ay)} on SOLID tile!'
            has_solid_gfx = bool(g.get('sprite')) or (bool(g.get('tile')) and (ts['passages'][g['tile']] & 0x0f) == 0x0f)
            if trig == 'action' and not has_solid_gfx and pg0.get('commands'):
                assert not B.cell_passable(Lr, ts, ax, ay), f'{label}: over_trigger? trap {e.get("name")} at {(ax,ay)}!'

    # Compute exact 4-bit walkability for state `sw`
    solid_ev = set()
    for e in events:
        at = tuple(e['at'])
        et = e.get('type')
        if et in ('npc', 'trainer', 'mart', 'item'):
            if not e.get('hidden'):
                solid_ev.add(at)
        elif et == 'event':
            pg = _ev_active_page(e, sw)
            if not pg or pg.get('through'):
                continue
            g = pg.get('graphic') or {}
            if g.get('sprite'):
                solid_ev.add(at)
            elif g.get('tile') and (ts['passages'][g['tile']] & 0x0f) == 0x0f:
                solid_ev.add(at)

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
    assert ok[sy, sx], f'{label}: start {start} not walkable!'
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

    # Anti-P0 #2: 100% open trainer sightlines (on default state sw={})!
    if not sw:
        dir_vec = {'down': (0, 1), 'up': (0, -1), 'right': (1, 0), 'left': (-1, 0)}
        for e in events:
            if e.get('type') == 'trainer':
                tx, ty = int(e['at'][0]), int(e['at'][1])
                dx, dy = dir_vec[e.get('dir', 'down')]
                for step in range(1, int(e.get('sight', 3)) + 1):
                    nx, ny = tx + dx * step, ty + dy * step
                    assert ok[ny, nx] and (nx, ny) in seen, (
                        f'{label}: trainer {e["trainer"]} sightline blocked at step {step} {(nx,ny)}'
                    )

        # Anti-P0 #3: Full-width exit carpet (0 exit pockets on exit_row!)
        warps = {tuple(e['at']) for e in events if e.get('type') in ('warp', 'exit')}
        pockets = [x for x in range(W) if (x, exit_row) in seen and (x, exit_row) not in warps]
        assert not pockets, f'{label}: unsealed exit pocket(s) on y={exit_row}: {pockets}'

        _check_ruby_syntax(events, label)

    for nm, pt, adj in targets:
        if adj:
            r = pt in seen or any((pt[0] + dx, pt[1] + dy) in seen for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)))
        else:
            r = pt in seen
        assert r, f'{label}: target {nm} {pt} NOT reachable in sw={sw}!'
    return seen


# =================================================================================================
# Exhaustive Python Pursuer + Boulder + Plate Solver (Directly Reads Compiled Map Tile Grids!)
# =================================================================================================
_SOL_DIRS = [(0, -1), (0, 1), (-1, 0), (1, 0)]


def _pursuer_step_sim(px, py, plx, ply, walls, ropes, occ):
    dx, dy = plx - px, ply - py
    if abs(dx) + abs(dy) <= 1:
        return (px, py)
    horiz = (1, 0) if dx > 0 else ((-1, 0) if dx < 0 else None)
    vert = (0, 1) if dy > 0 else ((0, -1) if dy < 0 else None)
    order = [horiz, vert] if abs(dx) >= abs(dy) else [vert, horiz]
    for d in order:
        if d is None:
            continue
        nx, ny = px + d[0], py + d[1]
        if (nx, ny) == (plx, ply) or (nx, ny) in walls or (nx, ny) in ropes or (nx, ny) in occ:
            continue
        return (nx, ny)
    return (px, py)


def _step_pursuers_sim(purs, pl, walls, ropes, blds):
    plx, ply = pl
    cur = list(purs)
    bset = set(blds)
    for i in range(len(cur)):
        occ = bset | {cur[j] for j in range(len(cur)) if j != i}
        cur[i] = _pursuer_step_sim(cur[i][0], cur[i][1], plx, ply, walls, ropes, occ)
    caught = (pl not in ropes) and any(abs(px - plx) + abs(py - ply) <= 1 for (px, py) in cur)
    return tuple(cur), caught


def _extract_walls_from_map(Lr, box, extra_solid=()):
    """Extract EXACT solid tiles directly from compiled map Lr inside box (x0, y0, x1, y1)."""
    import build as B
    ts = R.tilesets()[TID]
    x0, y0, x1, y1 = box
    walls = set(extra_solid)
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if not B.cell_passable(Lr, ts, x, y):
                walls.add((x, y))
    return walls


def _solve_bfs_exact(name, box, walls, ropes, start_pl, start_purs, start_blds, goal_fn, allow_push=True, max_states=150000):
    x0, y0, x1, y1 = box
    inb = lambda x, y: x0 <= x <= x1 and y0 <= y <= y1
    init = (start_pl, tuple(start_purs), tuple(start_blds))
    q = deque([(init, 0)])
    seen = {init}
    while q and len(seen) < max_states:
        (pl, purs, blds), dist = q.popleft()
        if goal_fn(pl, purs, blds):
            return dist, len(seen), (pl, purs, blds)
        plx, ply = pl
        pset, bset = set(purs), set(blds)
        for dx, dy in _SOL_DIRS:
            nx, ny = plx + dx, ply + dy
            if not inb(nx, ny) or (nx, ny) in walls or (nx, ny) in pset or (nx, ny) in bset:
                continue
            npurs, caught = _step_pursuers_sim(purs, (nx, ny), walls, ropes, blds)
            if caught:
                continue
            st = ((nx, ny), npurs, blds)
            if st not in seen:
                seen.add(st)
                q.append((st, dist + 1))
        if allow_push and blds:
            for bi, (bx, by) in enumerate(blds):
                if abs(bx - plx) + abs(by - ply) == 1:
                    dx, dy = bx - plx, by - ply
                    nbx, nby = bx + dx, by + dy
                    if (inb(nbx, nby) and (nbx, nby) not in walls and (nbx, nby) not in ropes
                            and (nbx, nby) not in pset and (nbx, nby) not in bset):
                        nblds = list(blds)
                        nblds[bi] = (nbx, nby)
                        st = (pl, purs, tuple(nblds))
                        if st not in seen:
                            seen.add(st)
                            q.append((st, dist + 1))
    return None, len(seen), None


def _solve_stage_astar(box, walls, ropes, start, goal_fn, h_fn, max_states=150000):
    x0, y0, x1, y1 = box
    inb = lambda x, y: x0 <= x <= x1 and y0 <= y <= y1
    pq = [(h_fn(start), 0, start)]
    parent = {start: None}
    best_g = {start: 0}
    while pq and len(best_g) < max_states:
        _, g, st = heapq.heappop(pq)
        if g > best_g[st]:
            continue
        pl, purs, blds = st
        if goal_fn(pl, purs, blds):
            path = []
            cur = st
            while parent[cur] is not None:
                prev, act = parent[cur]
                path.append(act)
                cur = prev
            path.reverse()
            return path, st, len(best_g)
        plx, ply = pl
        pset, bset = set(purs), set(blds)
        for dx, dy in _SOL_DIRS:
            nx, ny = plx + dx, ply + dy
            if not inb(nx, ny) or (nx, ny) in walls or (nx, ny) in pset or (nx, ny) in bset:
                continue
            npurs, caught = _step_pursuers_sim(purs, (nx, ny), walls, ropes, blds)
            if caught:
                continue
            nst = ((nx, ny), npurs, blds)
            if g + 1 < best_g.get(nst, 10**9):
                best_g[nst] = g + 1
                parent[nst] = (st, ('W', (nx, ny)))
                heapq.heappush(pq, (g + 1 + 2 * h_fn(nst), g + 1, nst))
        for bi, (bx, by) in enumerate(blds):
            if abs(bx - plx) + abs(by - ply) == 1:
                dx, dy = bx - plx, by - ply
                nbx, nby = bx + dx, by + dy
                if (inb(nbx, nby) and (nbx, nby) not in walls and (nbx, nby) not in ropes
                        and (nbx, nby) not in pset and (nbx, nby) not in bset):
                    nblds = list(blds)
                    nblds[bi] = (nbx, nby)
                    nst = (pl, purs, tuple(nblds))
                    if g + 1 < best_g.get(nst, 10**9):
                        best_g[nst] = g + 1
                        parent[nst] = (st, ('P', bi, (nbx, nby)))
                        heapq.heappush(pq, (g + 1 + 2 * h_fn(nst), g + 1, nst))
    return None, None, len(best_g)


# =================================================================================================
# MAP 270 — IRONREACH GYM - ENTRANCE (21x17, TS 57, :COLOSSEUM)
# =================================================================================================
def build_270():
    W, H = 21, 17
    m = _new_pit_hall(W, H, seed=270, wall_kit='qy2', ter_kit='qy2')

    m.box(2, 2, 18, 14, FLOOR, '.')
    m.box(9, 14, 11, 16, FLOOR, '.')          # Exact 3-wide south vestibule (0 exit pockets!)
    m.mass_at([(2, 2), (3, 2), (2, 3), (18, 2), (17, 2), (18, 3), (2, 14), (18, 14)])
    m.tidy()
    m.plan_cliffs(rows=2)

    E = m.events
    # Full-width 3-tile south exit carpet (9..11, 16) <-> IR_GYM (260)
    for rx in (9, 10, 11):
        E.append({
            'type': 'exit',
            'name': f'Exit Gym {rx}',
            'at': [rx, 16],
            'link': 'IR_GYM',
            'arrive': [10, 15, 'up'],
            'se': 'Door exit',
        })

    # North Colosseum Portal (10, 4) -> 271 Sparring Floor (14, 22) up
    E.append({
        'type': 'warp',
        'name': 'To Sparring Floor (271)',
        'at': [10, 4],
        'to': {'map': 271, 'x': 14, 'y': 22, 'dir': 'up'},
        'se': 'Door enter',
    })

    # Kaito's Plaque on solid pf_signpost base (8, 12)
    E.append(_sign(
        "Kaito's Iron Plaque", (8, 12),
        "IRONREACH GYM — THE PIT. Carved in steel by Warden Kaito Ren: 'Don't fight the one in front of you. Move it. Every step you take, they take.'"
    ))

    # Gym Guide (canonical Ch9 rules briefing — explicitly explains the golden rope-break safety rule!)
    E.append(_make_npc('Gym Guide', (7, 13), 'NPC 15', 'right', [
        "Gym Guide: Yo, champ-in-the-making! Welcome to Kaito's Pit — Fighting-types on the Colosseum field!",
        "Gym Guide: Every knockout gets the crowd going, and a roused crowd hits harder. Psychic and Flying go over their heads, and Fairies don't care how loud it gets.",
        "Gym Guide: Listen close to Kaito's ring rules: Every step you take, the sparring partners take one. Step onto a golden rope line — they can't cross ropes, and the ring judges call a rope break so they can't tag you while you're standing on one!",
        "Gym Guide: And remember: Strength boulders hold down iron pressure plates — and so do sparring partners!",
    ]))

    # Ring Medic (free full party heal!)
    medic_ruby = '''pbMessage(_INTL("Ring Medic: Wraps tight, shoulders loose! Let me patch your Pokémon up before you step onto Kaito's sand."))
pbSEPlay("Anim/HealBell", 85, 100)
$player.heal_party
pbMessage(_INTL("Your party was restored to full health!"))'''
    E.append({
        'type': 'event',
        'name': 'Ring Medic',
        'at': [13, 13],
        'pages': [{
            'graphic': {'sprite': 'NPC 18', 'dir': 'left'},
            'trigger': 'action',
            'move': 'fixed',
            'commands': [{'script': medic_ruby}],
        }],
    })

    # Odessa post-Badge 8 HM02 Fly delivery (canonical story/27_SCRIPT_CH9.md:440-450! Appears when V130 >= 6!)
    odessa_ruby = '''if !$game_self_switches[[270, @event_id, "A"]]
  pbMessage(_INTL("Odessa: There you are! Eight badges, says the board."))
  pbMessage(_INTL("Odessa: Fly's allowed at eight, and I don't trust the post to deliver it."))
  pbReceiveItem(:HM02)
  pbMessage(_INTL("Odessa: Courier's privilege. I deliver in person when I like the address. Come to Skyreach sometime — we've got a gym, a storm, and the best dead-letter office in the realm!"))
  $game_self_switches[[270, @event_id, "A"]] = true
  $game_map.need_refresh = true
else
  pbMessage(_INTL("Odessa: Keep your wings dry down in these shafts, kid! See you up in Skyreach when the wind turns!"))
end'''
    E.append({
        'type': 'event',
        'name': 'Odessa (HM02 Fly)',
        'at': [12, 14],
        'pages': [
            {'trigger': 'action', 'through': True, 'commands': []},
            {
                'cond': {'var': [V_CH9_STEP, 6]},
                'graphic': {'sprite': 'ODESSA', 'dir': 'left'},
                'trigger': 'action',
                'move': 'fixed',
                'commands': [{'script': odessa_ruby}],
            },
        ],
    })

    # Canonical PBS Trainer [BLACKBELT, Goro] — 100% open sightline facing down along center aisle!
    E.append(_trainer(
        (10, 7), 'BLACKBELT', 'Goro', 'down',
        "Black Belt Goro: First rule of Kaito's Pit: stand your ground before you try to outrun a sparring partner!",
        "Black Belt Goro: A fist is a promise. Mine broke. Go on north into the Sparring Floor!",
        sight=3,
    ))

    # Visible Poké Ball (hidden=False EXPLICIT!)
    E.append(_visible_item((4, 6), 'HYPERPOTION'))

    # Decorative Pit Training Props, Intact Blazing Braziers, Banners & Golden Rope Preview!
    _place_stamp_over(m, 'pf_signpost', 8, 11, base_z=1, top_z=2, top_rows=1, solid=True)  # Base (8, 12)
    _place_stamp_over(m, 'pf_bellpost', 12, 10, base_z=1, top_z=2, top_rows=2, solid=True) # Base (12, 12)
    for bx, by, bn in ((7, 2, 'wr_ban_ash'), (13, 2, 'wr_ban_bone'), (5, 2, 'hb_banner'), (15, 2, 'hb_banner')):
        _place_stamp_over(m, bn, bx, by, base_z=1, top_z=2, top_rows=1, solid=True)
    braziers_270 = [(8, 4), (12, 4), (7, 10), (13, 10)]
    for bx, by in braziers_270:
        _place_stamp_over(m, 'fw_brazier', bx, by, base_z=1, top_z=2, top_rows=1, solid=True)
    for sx, sy, sn in (
        (3, 12, 'hb_boxes'), (16, 12, 'hb_barrels'), (3, 8, 'wr_rack'), (17, 8, 'wr_rack'),
        (16, 5, 'wr_sandbags'), (17, 5, 'hb_rope'), (4, 10, 'pf_logbench'), (15, 10, 'pf_logbench'),
    ):
        _place_stamp_over(m, sn, sx, sy, base_z=1, top_z=2, top_rows=1 if STAMPS[sn]['h'] >= 2 else 0, solid=True)

    for y in range(4, 17):
        for x in (9, 10, 11):
            m.keep_clear.add((x, y))

    m.paint()
    _paint_pit_floors(m, [
        (2, 4, 18, 14, 'flag'),
        (5, 5, 15, 11, 'sand'),
        (9, 12, 11, 16, 'iron'),
    ])
    _paint_crimson_runner(m, 9, 12, 11, 16, medallion_y=14)
    # Warm golden step-over training rope preview framing the lobby sand ring (teaches visual language for 271..274!)
    _paint_ropes(
        m,
        ropes_h=[(6, 5), (7, 5), (13, 5), (14, 5)],
        ropes_v=[(5, 6), (5, 7), (5, 8)],
        ropes_vr=[(15, 6), (15, 7), (15, 8)],
        ropes_nw=[(5, 5)],
        ropes_ne=[(15, 5)],
    )
    m.L[1, 4, 10] = T_PDOOR_OPEN

    Lr = RC.resolve(m.L, TID).astype(np.int32)
    # Clean, unobstructed overhead light shafts flanking Goro cleanly over open sand (ZERO overlap with Goro's head!)
    _add_shafts(Lr, [(6, 7), (13, 7)], label='Map 270')
    _assert_braziers_intact(Lr, braziers_270, 'Map 270')

    _verify_gym_map(Lr, E, (10, 15), [
        ('North Portal', (10, 4), False),
        ('Gym Guide', (7, 13), True),
        ('Ring Medic', (13, 13), True),
        ('Kaito Plaque', (8, 12), True),
        ('Goro', (10, 7), True),
        ('HYPERPOTION', (4, 6), True),
    ], 'Map 270 Gym 8 Entrance', exit_row=16)

    os.makedirs(RAW_DIR, exist_ok=True)
    np.save(os.path.join(RAW_DIR, '270.npy'), Lr.astype(np.int16))
    spec = {
        'id': 270,
        'name': 'Ironreach Gym - Entrance',
        'parent': 260,
        'bgm': 'Gym',
        'field': FIELD,
        'map_audio': {'bgm': 'Gym - Warden Hall', 'bgs': 'Drip - Nadir', 'bgs_volume': 25, 'rain': False},
        'tone': [-4, -6, -4, 6],
        'metadata': {'Name': 'Ironreach Gym', 'SnapEdges': True, 'MapPosition': IRONREACH_POS, 'BattleBack': 'indoor3'},
        'biome': 'interior',
        'tileset': TID,
        'raw': 'data/raw/270.npy',
        'events': E,
    }
    with open(os.path.join(SPEC_DIR, '270_ironreach_gym_270.yaml'), 'w', encoding='utf-8') as f:
        f.write('# GENERATED by mapgen/layouts/ironreach_gym.py (Batch 3G): Ironreach Gym - Entrance.\n')
        f.write(yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))
    print('Wrote specs/270_ironreach_gym_270.yaml and data/raw/270.npy')
    return Lr


# =================================================================================================
# MAP 271 — IRONREACH GYM - PUZZLE ROOM 1 ("Sparring Floor" — TEACH + TWIST, 29x25, TS 57)
# =================================================================================================
def build_271():
    W, H = 29, 25
    # Dark cut ironstone masonry (qy2) for both perimeter walls AND the 3x3 West Pillar (ZERO icy glacier!)
    m = _new_pit_hall(W, H, seed=271, wall_kit='qy2', ter_kit='qy2')
    m.box(3, 3, 26, 22, FLOOR, '.')
    m.box(13, 22, 15, 24, FLOOR, '.')
    m.box(23, 2, 25, 4, FLOOR, '.')          # North Exit Portal Alcove: wall y=2..3, floor (24, 4), Gate (24, 5)!
    m.mass_at(
        [(x, y) for x in (13, 14, 15) for y in range(3, 19)]      # 3-wide solid ironstone divider between West & East
        + [(x, y) for x in range(6, 9) for y in range(10, 13)]    # 3x3 solid ironstone West Pillar ("The Pillar")
    )
    m.tidy()
    m.plan_cliffs(rows=2)

    E = m.events
    for rx in (13, 14, 15):
        E.append({
            'type': 'warp',
            'name': f'Back to Entrance {rx}',
            'at': [rx, 24],
            'to': {'map': 270, 'x': 10, 'y': 5, 'dir': 'down'},
            'se': 'Door exit',
        })
    E.append({
        'type': 'warp',
        'name': 'To Puzzle Room 2 (272)',
        'at': [24, 4],
        'to': {'map': 272, 'x': 14, 'y': 22, 'dir': 'up'},
        'se': 'Door enter',
    })
    E.append(_gate_event(
        'East Entry Iron Gate', (21, 19), S_TEACH_BELL,
        "Heavy iron bars seal the East Rope-Line ring. Ring the West Pillar Bell first!",
        tile_id=T_BARS_SHUT,
    ))
    E.append(_gate_event(
        'North Exit Iron Gate', (24, 5), S_BELL_1,
        "The steel sluice gate to Puzzle Room 2 is sealed! Ring the East Rope-Line Bell to unlatch it!",
        tile_id=T_GATE_SHUT,
    ))
    E.append(_lamp_event('Lamp West Done', (20, 19), S_TEACH_BELL))
    E.append(_lamp_event('Lamp Room 1 Done', (23, 5), S_BELL_1))

    # West Half Bell (7, 5) -> unlocks S344 (East Entry Gate!)
    bell_w_ruby = f'''pbSEPlay("Mining iron", 95, 95)
if !$game_switches[{S_TEACH_BELL}]
  $game_switches[{S_TEACH_BELL}] = true
  pfm_shake(3, 10, 8)
  $game_map.need_refresh = true
  pbMessage(_INTL("CLANG! The West Pillar Bell rings out! The iron gate to the East Rope-Line ring slides open!"))
else
  pbMessage(_INTL("CLANG! The West Pillar trial is already cleared. Head through the east gate!"))
end'''
    E.append({
        'type': 'event',
        'name': 'West Pillar Bell',
        'at': [7, 5],
        'pages': [{'trigger': 'action', 'commands': [{'script': bell_w_ruby}]}],
    })

    # East Half Bell (21, 5) -> unlocks S340 (North Exit Gate -> 272!)
    bell_e_ruby = f'''pbSEPlay("Mining iron", 95, 90)
if !$game_switches[{S_BELL_1}]
  $game_switches[{S_BELL_1}] = true
  pfm_shake(4, 12, 10)
  $game_map.need_refresh = true
  pbMessage(_INTL("DONG!! The East Rope-Line Bell echoes across the pit! The steel gate to Puzzle Room 2 unlocks!"))
else
  pbMessage(_INTL("DONG! Room 1 is cleared — step through the north-east gate to Puzzle Room 2!"))
end'''
    E.append({
        'type': 'event',
        'name': 'East Rope-Line Bell',
        'at': [21, 5],
        'pages': [{'trigger': 'action', 'commands': [{'script': bell_e_ruby}]}],
    })

    # Sparring Pursuers!
    E.append(_pursuer_event(
        'Spar_271_W', (7, 7), 'Followers/MACHOP', S_TEACH_BELL,
        "Machop bounces on its heels, matching your stance step for step!",
        "Machop bows respectfully — you outmaneuvered it around the pillar!"
    ))
    E.append(_pursuer_event(
        'Spar_271_E1', (20, 7), 'Followers/MAKUHITA', S_BELL_1,
        "Makuhita slaps its palms together, watching the golden rope line!",
        "Makuhita nods proudly — it couldn't cross the ropes to stop you!"
    ))
    E.append(_pursuer_event(
        'Spar_271_E2', (22, 7), 'Followers/HITMONLEE', S_BELL_1,
        "Hitmonlee stretches its legs, ready to intercept your rush!",
        "Hitmonlee lowers its guard — clean footwork!"
    ))

    ropes_271e_h = [(x, 12) for x in range(16, 27) if x != 21]
    ropes_271e_v = [(19, 11)]
    ropes_271e_vr = [(23, 11)]
    ropes_271e = set(ropes_271e_h) | set(ropes_271e_v) | set(ropes_271e_vr)

    E.append(_step_hook_installer(271, 'g8_271', [
        {
            'box': (3, 5, 12, 18),
            'done_sw': S_TEACH_BELL,
            'ropes': set(),
            'pursuers': [('Spar_271_W', 7, 7)],
            'boulders': [],
            'plates': [],
            'reset_pl': (7, 18),
        },
        {
            'box': (16, 5, 26, 18),
            'done_sw': S_BELL_1,
            'ropes': ropes_271e,
            'pursuers': [('Spar_271_E1', 20, 7), ('Spar_271_E2', 22, 7)],
            'boulders': [],
            'plates': [],
            'reset_pl': (21, 18),
        },
    ]))

    reset_271 = _reset_ruby(
        271,
        [('Spar_271_W', 7, 7), ('Spar_271_E1', 20, 7), ('Spar_271_E2', 22, 7)],
        [], (14, 21)
    )
    status_271 = (
        f'    w_st = $game_switches[{S_TEACH_BELL}] ? "CLEARED" : "ACTIVE"\n'
        f'    e_st = $game_switches[{S_BELL_1}] ? "CLEARED" : "LOCKED/ACTIVE"\n'
        f'    pbMessage(_INTL("Apprentice Hiro: West Pillar: {{1}} | East Rope Line: {{2}} | Rounds tagged: {{3}}.", w_st, e_st, $game_variables[{V_ROUNDS}].to_i))'
    )
    skip_271 = (
        f'$game_switches[{S_TEACH_BELL}] = true\n'
        f'$game_switches[{S_BELL_1}] = true\n'
        f'$game_map.need_refresh = true'
    )
    E.append(_hiro_event(
        (12, 21), 271, 'the Sparring Floor', status_271, reset_271, V_HINT_271,
        (
            "Sparring partners always close the larger gap first. Use the 3x3 stone pillar in the West ring to pull Machop to one side, then circle past it!",
            "In the East ring, YOU can step right onto the golden rope lines — the ring judges call a rope break while you're standing on a rope, so sparring partners can't cross ropes OR tag you there! Hold them on the ropes to split them apart!",
            "West: walk up the right side of the pillar until Machop commits east, circle clockwise around the pillar and dash to the West Bell. East: step onto the west golden rope at (19,12) — remember you're safe from tags while standing on a rope! — lure Makuhita and Hitmonlee into the rope pockets, then cut north around the center post to the East Bell!"
        ),
        skip_271,
    ))
    E.append({
        'type': 'event',
        'name': 'Room 1 Reset Bell',
        'at': [16, 21],
        'pages': [{
            'trigger': 'action',
            'commands': [{'script': reset_271 + '\npbMessage(_INTL("CLANG! All sparring partners returned to their starting marks."))'}],
        }],
    })
    E.append(_sign(
        "Kaito's Sparring Sign", (5, 20),
        "KAITO'S RULE #1: 'Don't fight the one in front of you. Move it. Step onto a golden rope line — the ring judges call a rope break, so sparring partners can neither cross ropes nor tag you while you stand on one.'"
    ))

    # BOTH Canonical PBS Trainers in 271 (100% open sightlines in Safe South Foyer!)
    E.append(_trainer(
        (8, 22), 'CRUSHGIRL', 'Mika', 'right',
        "Crush Girl Mika: Footwork check before you hit Kaito's sand! Let's see if you can keep your balance!",
        "Crush Girl Mika: You stepped where I stepped — then right past me! Go ring that West Bell!",
        sight=3,
    ))
    E.append(_trainer(
        (18, 21), 'BLACKBELT', 'Hideo', 'right',
        "Black Belt Hideo: Heading into the Rope-Line ring? Prove your footing against my Hitmonlee first!",
        "Black Belt Hideo: The sand of the Pit keeps every footprint. Yours are right over mine.",
        sight=3,
    ))

    E.append(_visible_item((3, 5), 'FULLHEAL'))

    # Architecture: Hanging Bells, Signpost, Braziers, Banners & Dark Timber/Iron Center Post (21, 8) (ZERO marble columns!)
    _place_stamp_over(m, 'pf_bellpost', 7, 3, base_z=1, top_z=2, top_rows=2, solid=True)   # Base (7, 5)
    _place_stamp_over(m, 'pf_bellpost', 21, 3, base_z=1, top_z=2, top_rows=2, solid=True)  # Base (21, 5)
    _place_stamp_over(m, 'pf_bellpost', 16, 19, base_z=1, top_z=2, top_rows=2, solid=True) # Base (16, 21) Reset Bell!
    _place_stamp_over(m, 'pf_signpost', 5, 19, base_z=1, top_z=2, top_rows=1, solid=True)  # Base (5, 20)
    _place_stamp_over(m, 'cv_post', 21, 7, base_z=1, top_z=2, top_rows=1, solid=True)      # Dark mining post base (21, 8)!
    braziers_271 = [(3, 20), (26, 20), (12, 5), (16, 5)]
    for bx, by in braziers_271:
        _place_stamp_over(m, 'fw_brazier', bx, by, base_z=1, top_z=2, top_rows=1, solid=True)
    for bx, by, bn in ((5, 3, 'wr_ban_ash'), (9, 3, 'wr_ban_bone'), (18, 3, 'wr_ban_ash'), (22, 3, 'wr_ban_ise')):
        _place_stamp_over(m, bn, bx, by, base_z=1, top_z=2, top_rows=1, solid=True)

    m.paint()
    _paint_pit_floors(m, [
        (3, 5, 12, 18, 'sand'),
        (16, 5, 26, 18, 'sand'),
        (3, 20, 26, 22, 'flag'),
        (13, 22, 15, 24, 'iron'),
        (23, 4, 25, 5, 'iron'),
    ])
    _paint_crimson_runner(m, 13, 22, 15, 24, medallion_y=23)
    _paint_ropes(m, ropes_271e_h, ropes_271e_v, ropes_vr=ropes_271e_vr)

    # Riveted Iron Pit Railings along y=19 separating Foyer from West & East rings (100% solid pas=0xf, 0 bypass!)
    # Open West Entry at x=7..8, Gated East Entry at x=21 (Lamp at (20, 19)!)
    for rx in range(3, 27):
        if rx in (7, 8, 20, 21):
            continue
        if rx in (13, 14, 15):
            m.L[1, 19, rx] = T_RAIL_M
        elif rx == 6 or rx == 19:
            m.L[1, 19, rx] = T_RAIL_E
        elif rx == 9 or rx == 22:
            m.L[1, 19, rx] = T_RAIL_W
        else:
            m.L[1, 19, rx] = T_RAIL_M
    # Seal North Portal flanking tiles (23, 4) and (25, 4..5) with seamless vertical ironstone walls!
    m.L[1, 4, 23] = T_WALL_V
    m.L[1, 4, 25] = T_WALL_V
    m.L[1, 5, 25] = T_WALL_V
    m.L[1, 4, 24] = T_PDOOR_OPEN

    Lr = RC.resolve(m.L, TID).astype(np.int32)
    # Clean, 100% unobstructed overhead light shafts strictly on open sand (ZERO overlap with Machop, Hitmonlee, post, ropes!)
    _add_shafts(Lr, [(4, 14), (24, 14)], label='Map 271')
    _assert_braziers_intact(Lr, braziers_271, 'Map 271')

    seen0 = _verify_gym_map(Lr, E, (14, 22), [
        ('Hiro', (12, 21), True), ('Reset Bell', (16, 21), True), ('West Bell', (7, 5), True),
        ('Mika', (8, 22), True), ('Hideo', (18, 21), True), ('FULLHEAL', (3, 5), True),
    ], 'Map 271 Start', exit_row=24)
    assert (24, 4) not in seen0, 'Map 271 BYPASS BUG: North Portal reachable at Start!'
    assert (21, 18) not in seen0, 'Map 271 BYPASS BUG: East Half reachable before West Bell!'
    seen_w = _verify_gym_map(Lr, E, (14, 22), [
        ('East Bell', (21, 5), True),
    ], 'Map 271 West Cleared', exit_row=24, sw={S_TEACH_BELL: True})
    assert (24, 4) not in seen_w, 'Map 271 BYPASS BUG: North Portal reachable before East Bell!'
    seen_solved = _verify_gym_map(Lr, E, (14, 22), [
        ('East Bell', (21, 5), True), ('North Portal', (24, 4), False),
    ], 'Map 271 Solved', exit_row=24, sw={S_TEACH_BELL: True, S_BELL_1: True})
    assert (24, 4) in seen_solved

    # Exhaustive Pursuer Solver Proofs reading walls straight from compiled Lr!
    w271w = _extract_walls_from_map(Lr, (3, 5, 12, 18))
    d1, st1, _ = _solve_bfs_exact(
        '271W', (3, 5, 12, 18), w271w, set(), (7, 18), [(7, 7)], [],
        lambda pl, pu, bl: abs(pl[0] - 7) + abs(pl[1] - 5) == 1, allow_push=False
    )
    assert d1 is not None, 'Map 271W Pursuer Solver FAILED!'

    w271e = _extract_walls_from_map(Lr, (16, 5, 26, 18), extra_solid={(24, 5), (23, 5), (25, 5)})
    d2, st2, _ = _solve_bfs_exact(
        '271E', (16, 5, 26, 18), w271e, ropes_271e, (21, 18), [(20, 7), (22, 7)], [],
        lambda pl, pu, bl: abs(pl[0] - 21) + abs(pl[1] - 5) == 1, allow_push=False
    )
    assert d2 is not None, 'Map 271E Pursuer Solver FAILED!'
    d2_norope, _, _ = _solve_bfs_exact(
        '271E-NoRope', (16, 5, 26, 18), w271e, set(), (21, 18), [(20, 7), (22, 7)], [],
        lambda pl, pu, bl: abs(pl[0] - 21) + abs(pl[1] - 5) == 1, allow_push=False, max_states=15000
    )
    assert d2_norope is None, 'Map 271E ANTI-BYPASS FAILED: solvable without ropes!'
    print(f'Map 271 Pursuer Solver PASS: 271W={d1} steps ({st1} states), 271E={d2} steps ({st2} states, No-Rope=UNSOLVABLE!)')

    os.makedirs(RAW_DIR, exist_ok=True)
    np.save(os.path.join(RAW_DIR, '271.npy'), Lr.astype(np.int16))
    spec = {
        'id': 271,
        'name': 'Ironreach Gym - Puzzle Room 1',
        'parent': 270,
        'bgm': 'Gym',
        'field': FIELD,
        'map_audio': {'bgm': 'Gym - Warden Hall', 'bgs': 'Drip - Nadir', 'bgs_volume': 25, 'rain': False},
        'tone': [-4, -6, -4, 6],
        'metadata': {'Name': 'Ironreach Gym', 'SnapEdges': True, 'MapPosition': IRONREACH_POS, 'BattleBack': 'indoor3'},
        'biome': 'interior',
        'tileset': TID,
        'raw': 'data/raw/271.npy',
        'events': E,
    }
    with open(os.path.join(SPEC_DIR, '271_ironreach_gym_271.yaml'), 'w', encoding='utf-8') as f:
        f.write('# GENERATED by mapgen/layouts/ironreach_gym.py (Batch 3G): Ironreach Gym - Puzzle Room 1.\n')
        f.write(yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))
    print('Wrote specs/271_ironreach_gym_271.yaml and data/raw/271.npy')
    return Lr


# =================================================================================================
# MAP 272 — IRONREACH GYM - PUZZLE ROOM 2 ("Boulder & Rope Ring" — COMBINE, 29x25, TS 57)
# =================================================================================================
def build_272():
    W, H = 29, 25
    m = _new_pit_hall(W, H, seed=272, wall_kit='qy2', ter_kit='qy2')

    # Main Arena: x=4..24, y=6..18 | Divider Iron Rail: y=19 (3-wide central archway x=13..15 ONLY — 0 freeze exploit!)
    # Safe South Foyer: x=4..24, y=20..22 | South Exit: x=13..15, y=22..24
    # North Portal Alcove: x=13..15, y=2..5 (wall y=2..3, Portal (14, 4), Steel Sluice Gate (14, 5)!)
    m.box(4, 4, 24, 22, FLOOR, '.')
    m.box(13, 22, 15, 24, FLOOR, '.')
    m.box(13, 2, 15, 5, FLOOR, '.')
    m.mass_at(
        [(x, y) for x in range(4, 13) for y in (4, 5)]
        + [(x, y) for x in range(16, 25) for y in (4, 5)]
    )
    m.tidy()
    m.plan_cliffs(rows=2)

    E = m.events
    for rx in (13, 14, 15):
        E.append({
            'type': 'warp',
            'name': f'Back to Room 1 {rx}',
            'at': [rx, 24],
            'to': {'map': 271, 'x': 24, 'y': 6, 'dir': 'down'},
            'se': 'Door exit',
        })
    E.append({
        'type': 'warp',
        'name': 'To Puzzle Room 3 (273)',
        'at': [14, 4],
        'to': {'map': 273, 'x': 10, 'y': 22, 'dir': 'up'},
        'se': 'Door enter',
    })
    E.append(_gate_event(
        'Room 2 North Gate', (14, 5), S_BELL_2,
        "A heavy steel sluice shutter seals the path to the Gauntlet! Hold BOTH iron plates down and ring the Central Bell!",
        tile_id=T_GATE_SHUT,
    ))
    E.append(_lamp_event('Lamp Room 2 West', (12, 6), S_BELL_2))
    E.append(_lamp_event('Lamp Room 2 East', (16, 6), S_BELL_2))

    # Warm golden step-over colosseum ropes (100% live pas=0x0, exact 1-to-1 parity with Ruby _ropes!)
    ropes_272_h = (
        [(x, 11) for x in range(4, 10) if x != 6]
        + [(x, 11) for x in range(19, 25) if x != 22]
        + [(13, 9), (15, 9), (12, 13), (13, 13), (15, 13), (16, 13)]
    )
    ropes_272_v = [(5, 10), (12, 10), (12, 11), (12, 12)]
    ropes_272_vr = [(23, 10), (16, 10), (16, 11), (16, 12)]
    ropes_272_nw = [(12, 9)]
    ropes_272_ne = [(16, 9)]
    ropes_272 = set(ropes_272_h) | set(ropes_272_v) | set(ropes_272_vr) | set(ropes_272_nw) | set(ropes_272_ne)

    plates_272 = [('Plate_272_W', 6, 11), ('Plate_272_E', 22, 11)]
    heavy_272 = ['Boulder_272_W', 'Boulder_272_E', 'Spar_272_W', 'Spar_272_E']
    for pnm, px, py in plates_272:
        E.append(_plate_event(pnm, (px, py)))

    bell_ready_msg = "CLICK-CLANG!! Both iron pressure plates locked — the Central Ring Bell's iron clasp drops! Step into the center ring and ring the bell!"
    E.append(_boulder_event(
        'Boulder_272_W', (6, 15), 272, ropes_272, plates_272, heavy_272,
        bell_announce_msg=bell_ready_msg, blocked_pts=[(14, 5), (14, 4)],
    ))
    E.append(_boulder_event(
        'Boulder_272_E', (22, 15), 272, ropes_272, plates_272, heavy_272,
        bell_announce_msg=bell_ready_msg, blocked_pts=[(14, 5), (14, 4)],
    ))

    E.append(_pursuer_event(
        'Spar_272_W', (6, 7), 'Followers/HITMONCHAN', S_BELL_2,
        "Hitmonchan bob-and-weaves behind the west golden rope line, waiting for an opening!",
        "Hitmonchan taps its gloves together in respect — solid boulder work!"
    ))
    E.append(_pursuer_event(
        'Spar_272_E', (22, 7), 'Followers/HARIYAMA', S_BELL_2,
        "Hariyama stomps the sand behind the east golden rope line!",
        "Hariyama gives a deep nod — cleanly boxed out!"
    ))

    bell_272_ruby = f'''if $game_switches[{S_BELL_2}]
  pbSEPlay("Mining iron", 95, 90)
  pbMessage(_INTL("DONG! The steel gate to the Gauntlet stands open!"))
else
  _heavy = ["Boulder_272_W", "Boulder_272_E", "Spar_272_W", "Spar_272_E"].map {{ |n| pfp_ev(n) }}.compact
  _p1 = _heavy.any? {{ |e| e.x == 6 && e.y == 11 }}
  _p2 = _heavy.any? {{ |e| e.x == 22 && e.y == 11 }}
  if _p1 && _p2
    $game_switches[{S_BELL_2}] = true
    pbSEPlay("Mining iron", 95, 90)
    pfm_shake(4, 12, 10)
    $game_map.need_refresh = true
    pbMessage(_INTL("DONG!! Both iron plates hold steady as the Central Ring Bell thunders! The steel gate to Puzzle Room 3 opens!"))
  else
    pbSEPlay("Player bump", 80, 100)
    pbMessage(_INTL("An iron clasp holds the bell clapper silent! Hold down BOTH the West (6,11) and East (22,11) iron plates with Strength boulders first!"))
  end
end'''
    E.append({
        'type': 'event',
        'name': 'Central Ring Bell',
        'at': [14, 11],
        'pages': [{'trigger': 'action', 'commands': [{'script': bell_272_ruby}]}],
    })

    E.append(_step_hook_installer(272, 'g8_272', [
        {
            'box': (4, 6, 24, 18),
            'done_sw': S_BELL_2,
            'ropes': ropes_272,
            'pursuers': [('Spar_272_W', 6, 7), ('Spar_272_E', 22, 7)],
            'boulders': [('Boulder_272_W', 6, 15), ('Boulder_272_E', 22, 15)],
            'plates': plates_272,
            'auto_unlock': False,
            'reset_pl': (14, 18),
        },
    ]))

    reset_272 = _reset_ruby(
        272,
        [('Spar_272_W', 6, 7), ('Spar_272_E', 22, 7), ('Boulder_272_W', 6, 15), ('Boulder_272_E', 22, 15)],
        plates_272, (14, 21)
    )
    status_272 = (
        f'    _heavy = ["Boulder_272_W", "Boulder_272_E", "Spar_272_W", "Spar_272_E"].map {{ |n| pfp_ev(n) }}.compact\n'
        f'    _p1 = _heavy.any? {{ |e| e.x == 6 && e.y == 11 }} ? "HELD" : "OPEN"\n'
        f'    _p2 = _heavy.any? {{ |e| e.x == 22 && e.y == 11 }} ? "HELD" : "OPEN"\n'
        f'    pbMessage(_INTL("Apprentice Hiro: West Plate: {{1}} | East Plate: {{2}} | Bell Gate: {{3}}.", _p1, _p2, $game_switches[{S_BELL_2}] ? "OPEN" : "LOCKED"))'
    )
    skip_272 = f'$game_switches[{S_BELL_2}] = true\n$game_map.need_refresh = true'
    E.append(_hiro_event(
        (11, 21), 272, 'the Boulder & Rope Ring', status_272, reset_272, V_HINT_272,
        (
            "Strength boulders do two jobs at once in this ring: they hold down iron pressure plates AND plug the 1-tile gaps in the golden rope lines so sparring partners can't get out!",
            "If you walk straight up behind a boulder, the sparring partner rushes down through the rope gap. Bait each partner sideways into its corner rope pocket first, then shove the boulder straight north onto the gap plate!",
            "Walk to the far-left golden rope (x=4) to pull Hitmonchan into the west corner pocket, then rush under the west boulder and push it 4 tiles north onto the West Plate (6,11) — trapping it! Repeat on the east side for Hariyama and the East Plate (22,11), then step into the central rope ring and ring the bell!"
        ),
        skip_272,
    ))
    E.append({
        'type': 'event',
        'name': 'Room 2 Reset Bell',
        'at': [17, 22],
        'pages': [{
            'trigger': 'action',
            'commands': [{'script': reset_272 + '\npbMessage(_INTL("CLANG! All boulders, plates, and sparring partners reset to their starting marks!"))'}],
        }],
    })

    E.append(_trainer(
        (5, 21), 'CRUSHGIRL', 'Aiko', 'right',
        "Crush Girl Aiko: Strength and timing go hand-in-hand in Kaito's Pit! Let's see your form!",
        "Crush Girl Aiko: Kaito says losing is a lesson. I'm very educated. Try plugging those rope gaps with the boulders!",
        sight=3,
    ))
    E.append(_trainer(
        (22, 21), 'CRUSHKIN', 'Jin & Rei', 'left',
        "Jin: Two fighters, one ring! Rei: Show us if your team can keep up with a Crush Kin double bout!",
        "Jin: Together! Rei: We lost together, yes. Go show Kaito you've got discipline!",
        sight=3, double=True, sprite_override='trainer_BLACKBELT',
    ))
    E.append(_make_npc('Crush Kin Rei', (23, 21), 'trainer_CRUSHGIRL', 'left', [
        "Rei: Jin and I train side-by-side every morning in the Iron Pit. Talk to Jin right beside me if you haven't fought us yet!",
    ]))

    _place_stamp_over(m, 'pf_bellpost', 14, 9, base_z=1, top_z=2, top_rows=2, solid=True)   # Base (14, 11)
    _place_stamp_over(m, 'pf_bellpost', 17, 20, base_z=1, top_z=2, top_rows=2, solid=True) # Base (17, 22) Reset Bell (clear of y=19 rail!)
    braziers_272 = [(4, 21), (24, 21), (11, 6), (17, 6)]
    for bx, by in braziers_272:
        _place_stamp_over(m, 'fw_brazier', bx, by, base_z=1, top_z=2, top_rows=1, solid=True)
    for bx, by, bn in ((12, 4, 'wr_ban_ash'), (16, 4, 'wr_ban_bone')):
        _place_stamp_over(m, bn, bx, by, base_z=1, top_z=2, top_rows=1, solid=True)

    m.paint()
    _paint_pit_floors(m, [
        (4, 6, 24, 18, 'sand'),
        (12, 9, 16, 13, 'iron'),
        (4, 19, 24, 22, 'flag'),
        (13, 22, 15, 24, 'iron'),
        (13, 4, 15, 5, 'iron'),
    ])
    _paint_crimson_runner(m, 13, 22, 15, 24, medallion_y=23)
    _paint_ropes(m, ropes_272_h, ropes_272_v, ropes_vr=ropes_272_vr, ropes_nw=ropes_272_nw, ropes_ne=ropes_272_ne)

    # Riveted Iron Pit Divider Fence along y=19 leaving ONLY 3-wide central archway (x=13..15) open (fixes P1-272-1 freeze exploit!)
    for rx in range(4, 25):
        if rx in (13, 14, 15):
            continue
        if rx == 12:
            m.L[1, 19, rx] = T_RAIL_E
        elif rx == 16:
            m.L[1, 19, rx] = T_RAIL_W
        else:
            m.L[1, 19, rx] = T_RAIL_M

    # Seamless Vertical Ironstone Pen Dividers (x=10 & x=18, y=6..11) + North Portal Throat Walls (13,4..5) & (15,4..5)
    for ry in range(6, 12):
        m.L[1, ry, 10] = T_WALL_V
        m.L[1, ry, 18] = T_WALL_V
    for ry in (4, 5):
        m.L[1, ry, 13] = T_WALL_V
        m.L[1, ry, 15] = T_WALL_V
    m.L[1, 4, 14] = T_PDOOR_OPEN

    Lr = RC.resolve(m.L, TID).astype(np.int32)
    # Clean, 100% unobstructed overhead light shafts strictly on open sand (ZERO overlap with pursuers, ropes, or bell!)
    _add_shafts(Lr, [(8, 15), (19, 15)], label='Map 272')
    _assert_braziers_intact(Lr, braziers_272, 'Map 272')

    seen0 = _verify_gym_map(Lr, E, (14, 22), [
        ('Hiro', (11, 21), True), ('Reset Bell', (17, 22), True),
        ('Aiko', (5, 21), True), ('Jin & Rei', (22, 21), True),
        ('Boulder W', (6, 15), True), ('Boulder E', (22, 15), True),
        ('Central Bell', (14, 11), True),
    ], 'Map 272 Start', exit_row=24)
    assert (14, 4) not in seen0, 'Map 272 BYPASS BUG: North Portal reachable at Start!'
    seen_s = _verify_gym_map(Lr, E, (14, 22), [('North Portal', (14, 4), False)], 'Map 272 Solved', exit_row=24, sw={S_BELL_2: True})
    assert (14, 4) in seen_s

    w272 = _extract_walls_from_map(Lr, (4, 6, 24, 18))
    st0 = ((14, 18), ((6, 7), (22, 7)), ((6, 15), (22, 15)))
    pa, st1, e1 = _solve_stage_astar(
        (4, 6, 24, 18), w272, ropes_272, st0,
        lambda pl, pu, bl: (6, 11) in bl,
        lambda s: abs(s[2][0][0] - 6) + abs(s[2][0][1] - 11) + abs(s[0][0] - s[2][0][0]) + abs(s[0][1] - (s[2][0][1] + 1))
    )
    assert pa is not None, 'Map 272 Stage 1 FAILED!'
    pb, st2, e2 = _solve_stage_astar(
        (4, 6, 24, 18), w272, ropes_272, st1,
        lambda pl, pu, bl: (6, 11) in bl and (22, 11) in bl,
        lambda s: abs(s[2][1][0] - 22) + abs(s[2][1][1] - 11) + abs(s[0][0] - s[2][1][0]) + abs(s[0][1] - (s[2][1][1] + 1))
    )
    assert pb is not None, 'Map 272 Stage 2 FAILED!'
    pc, st3, e3 = _solve_stage_astar(
        (4, 6, 24, 18), w272, ropes_272, st2,
        lambda pl, pu, bl: (6, 11) in bl and (22, 11) in bl and abs(pl[0] - 14) + abs(pl[1] - 11) == 1,
        lambda s: abs(s[0][0] - 14) + abs(s[0][1] - 11)
    )
    assert pc is not None, 'Map 272 Stage 3 FAILED!'
    print(f'Map 272 Combined Solver PASS: {len(pa)+len(pb)+len(pc)} steps ({e1+e2+e3} states; end={st3})')

    os.makedirs(RAW_DIR, exist_ok=True)
    np.save(os.path.join(RAW_DIR, '272.npy'), Lr.astype(np.int16))
    spec = {
        'id': 272,
        'name': 'Ironreach Gym - Puzzle Room 2',
        'parent': 270,
        'bgm': 'Gym',
        'field': FIELD,
        'map_audio': {'bgm': 'Gym - Warden Hall', 'bgs': 'Drip - Nadir', 'bgs_volume': 25, 'rain': False},
        'tone': [-4, -6, -4, 6],
        'metadata': {'Name': 'Ironreach Gym', 'SnapEdges': True, 'MapPosition': IRONREACH_POS, 'BattleBack': 'indoor3'},
        'biome': 'interior',
        'tileset': TID,
        'raw': 'data/raw/272.npy',
        'events': E,
    }
    with open(os.path.join(SPEC_DIR, '272_ironreach_gym_272.yaml'), 'w', encoding='utf-8') as f:
        f.write('# GENERATED by mapgen/layouts/ironreach_gym.py (Batch 3G): Ironreach Gym - Puzzle Room 2.\n')
        f.write(yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))
    print('Wrote specs/272_ironreach_gym_272.yaml and data/raw/272.npy')
    return Lr


# =================================================================================================
# MAP 273 — IRONREACH GYM - PUZZLE ROOM 3 ("The Gauntlet & Marrowgate Mastery", 29x25, TS 57)
# =================================================================================================
def build_273():
    W, H = 29, 25
    m = _new_pit_hall(W, H, seed=273, wall_kit='qy2', ter_kit='qy2')

    # Main Gauntlet Arena: x=3..18, y=5..19 | Iron Divider Fence: y=20 (3-wide central archway x=9..11 ONLY — 0 freeze exploit!)
    # North Arena Portal Alcove: x=9..11, y=2..4 (Portal (10,4), Steel Sluice Gate (10,5)!)
    # East Marrowgate Mastery Alcove: x=21..26, y=7..18 (separated by solid 2-wide rock wall x=19..20, y=3..19!)
    # Safe South Foyer spanning BOTH entrances: x=3..26, y=21..22 | 3-wide South Exit: x=9..11, y=22..24
    m.box(3, 3, 18, 22, FLOOR, '.')
    m.box(21, 5, 26, 22, FLOOR, '.')
    m.box(18, 20, 21, 22, FLOOR, '.')
    m.box(9, 2, 11, 4, FLOOR, '.')
    m.box(9, 22, 11, 24, FLOOR, '.')
    m.tidy()
    m.plan_cliffs(rows=2)

    E = m.events
    for rx in (9, 10, 11):
        E.append({
            'type': 'warp',
            'name': f'Back to Room 2 {rx}',
            'at': [rx, 24],
            'to': {'map': 272, 'x': 14, 'y': 6, 'dir': 'down'},
            'se': 'Door exit',
        })
    E.append({
        'type': 'warp',
        'name': 'To Warden Arena (274)',
        'at': [10, 4],
        'to': {'map': 274, 'x': 10, 'y': 15, 'dir': 'up'},
        'se': 'Door enter',
    })
    E.append(_gate_event(
        'Arena Gate', (10, 5), S_GAUNTLET,
        "The steel sluice gate to Warden Kaito's Arena is sealed! Hold down BOTH Gauntlet pressure plates (P1 and P2) simultaneously!",
        tile_id=T_GATE_SHUT,
    ))
    E.append(_lamp_event('Lamp Arena W', (8, 5), S_GAUNTLET))
    E.append(_lamp_event('Lamp Arena E', (12, 5), S_GAUNTLET))

    ropes_g_h = [(x, 11) for x in range(3, 8)] + [(x, 11) for x in range(13, 18)]
    ropes_g_v = [(13, 10)]
    ropes_g_vr = [(7, 10)]
    ropes_g = set(ropes_g_h) | set(ropes_g_v) | set(ropes_g_vr)
    # Plate_273_P1 moved cleanly OFF the 1-tile Arena Gate axis (10,6) -> (8,6) so solving leaves (10,6)->(10,5)->(10,4) 100% UNPLUGGED!
    plates_g = [('Plate_273_P1', 8, 6), ('Plate_273_P2', 10, 14)]
    heavy_g = ['Boulder_273_1', 'Boulder_273_2', 'Boulder_273_3', 'Spar_273_W', 'Spar_273_E']
    unlock_g_msg = "CLANG-THOOM!! Both Gauntlet iron plates hold firm — the steel Arena Gate to Warden Kaito's Pit slides open clear ahead!"

    for pnm, px, py in plates_g:
        E.append(_plate_event(pnm, (px, py)))
    # All 3 Gauntlet boulders strictly Strength-checked AND blocked from ever entering doorway/warp (10,5)/(10,4)!
    for bnm, bx, by in (('Boulder_273_1', 7, 14), ('Boulder_273_2', 5, 7), ('Boulder_273_3', 14, 14)):
        E.append(_boulder_event(
            bnm, (bx, by), 273, ropes_g, plates_g, heavy_g, S_GAUNTLET, unlock_g_msg,
            blocked_pts=[(10, 5), (10, 4)],
        ))
    E.append(_pursuer_event(
        'Spar_273_W', (4, 10), 'Followers/MACHAMP', S_GAUNTLET,
        "Machamp flexes all four arms across the west golden rope bar!",
        "Machamp crosses its arms with an approving grunt — the Arena Gate is open!"
    ))
    E.append(_pursuer_event(
        'Spar_273_E', (16, 10), 'Followers/CONKELDURR', S_GAUNTLET,
        "Conkeldurr hefts its concrete pillars behind the east golden rope bar!",
        "Conkeldurr rests its pillars — worthy of Warden Kaito!"
    ))

    ropes_m_h = [(24, 12), (25, 12), (26, 12)]
    ropes_m = set(ropes_m_h)
    plates_m = [('Plate_273_M1', 22, 9), ('Plate_273_M2', 25, 11)]
    heavy_m = ['Boulder_273_M', 'Spar_273_M']
    unlock_m_msg = "Three hollow knocks sound behind the iron seal... then silence. Blue aura flickers across the stone wall as Kaito's Marrowgate Mastery Coffer unlocks!"

    for pnm, px, py in plates_m:
        E.append(_plate_event(pnm, (px, py)))
    E.append(_boulder_event(
        'Boulder_273_M', (22, 14), 273, ropes_m, plates_m, heavy_m, S_MARROWGATE, unlock_m_msg, unlock_flash=True
    ))
    E.append(_pursuer_event(
        'Spar_273_M', (25, 8), 'Followers/MACHOKE', S_MARROWGATE,
        "Machoke stands heavy and silent beside the sealed Marrowgate plaque, ready to mirror your steps.",
        "Machoke bows its head softly beside the unlatched Marrowgate coffer."
    ))

    coffer_ruby = '''pbSEPlay("Door enter", 85, 100)
pbMessage(_INTL("You lift the heavy iron lid of Kaito's Marrowgate Mastery coffer."))
pbMessage(_INTL("Behind the sealed iron door lies only cold stone and dust. Empty."))
pbReceiveItem(:TELLURICSEED, 2)
pbReceiveItem(:BLACKBELT, 1)
pbReceiveItem(:EXPERTBELT, 1)
pbMessage(_INTL("A folded order slip rests at the bottom: 'MARROWGATE — SEALED AF 285 — BY ORDER. Forgive me.'"))
$game_self_switches[[273, @event_id, "A"]] = true
$game_map.need_refresh = true'''
    E.append({
        'type': 'event',
        'name': 'Marrowgate Mastery Coffer',
        'at': [24, 7],
        'pages': [
            {
                'graphic': {'tile': T_CHEST_SHUT},
                'trigger': 'action',
                'commands': [
                    {'script': 'pbSEPlay("Mining iron", 70, 80)'},
                    "MARROWGATE COFFER (SEALED) — Faint knocking sounds from behind the iron gate: three knocks... a pause... three knocks. Hold down BOTH alcove plates simultaneously to unseal it!",
                ],
            },
            {
                'cond': {'switch': S_MARROWGATE},
                'graphic': {'tile': T_CHEST_SHUT},
                'trigger': 'action',
                'commands': [{'script': coffer_ruby}],
            },
            {
                'cond': {'switch': S_MARROWGATE, 'self': 'A'},
                'graphic': {'tile': T_CHEST_OPEN},
                'trigger': 'action',
                'commands': ["The Marrowgate Mastery coffer stands open and empty — only cool air and old dust remain."],
            },
        ],
    })

    E.append(_step_hook_installer(273, 'g8_273', [
        {
            'box': (3, 5, 18, 19),
            'done_sw': S_GAUNTLET,
            'ropes': ropes_g,
            'pursuers': [('Spar_273_W', 4, 10), ('Spar_273_E', 16, 10)],
            'boulders': [('Boulder_273_1', 7, 14), ('Boulder_273_2', 5, 7), ('Boulder_273_3', 14, 14)],
            'plates': plates_g,
            'auto_unlock': True,
            'unlock_msg': unlock_g_msg,
            'unlock_flash': False,
            'reset_pl': (10, 19),
        },
        {
            'box': (21, 7, 26, 18),
            'done_sw': S_MARROWGATE,
            'ropes': ropes_m,
            'pursuers': [('Spar_273_M', 25, 8)],
            'boulders': [('Boulder_273_M', 22, 14)],
            'plates': plates_m,
            'auto_unlock': True,
            'unlock_msg': unlock_m_msg,
            'unlock_flash': True,
            'reset_pl': (22, 18),
        },
    ]))

    reset_g = _reset_ruby(
        273,
        [('Spar_273_W', 4, 10), ('Spar_273_E', 16, 10),
         ('Boulder_273_1', 7, 14), ('Boulder_273_2', 5, 7), ('Boulder_273_3', 14, 14)],
        plates_g, (10, 21)
    )
    reset_m = _reset_ruby(
        273,
        [('Spar_273_M', 25, 8), ('Boulder_273_M', 22, 14)],
        plates_m, (22, 20)
    )
    reset_both = _reset_ruby(
        273,
        [('Spar_273_W', 4, 10), ('Spar_273_E', 16, 10),
         ('Boulder_273_1', 7, 14), ('Boulder_273_2', 5, 7), ('Boulder_273_3', 14, 14),
         ('Spar_273_M', 25, 8), ('Boulder_273_M', 22, 14)],
        plates_g + plates_m, (10, 21)
    )
    status_273 = (
        f'    g_st = $game_switches[{S_GAUNTLET}] ? "OPEN" : "LOCKED"\n'
        f'    m_st = $game_switches[{S_MARROWGATE}] ? "UNSEALED" : "SEALED (optional)"\n'
        f'    pbMessage(_INTL("Apprentice Hiro: Arena Gate: {{1}} | Marrowgate Mastery: {{2}} | Boulders pushed: {{3}}.", g_st, m_st, $game_variables[{V_PUSHES}].to_i))'
    )
    skip_273 = f'$game_switches[{S_GAUNTLET}] = true\n$game_map.need_refresh = true'
    # Exact solver-verified, zero-deadlock Hiro hints for P1=(8,6) & P2=(10,14) + Marrowgate!
    E.append(_hiro_event(
        (6, 21), 273, 'the Pit Gauntlet', status_273, reset_g, V_HINT_273,
        (
            "Discipline over rage. Push the lower-west boulder onto the south plate P2 (10,14) first — both sparring partners are greedy, so let them snag on the golden rope bars!",
            "After pushing (7,14) east onto P2 (10,14), use the west golden rope line to lure both partners south of the ropes, then circle up x=4 to push the upper-west boulder (5,7) onto P1 (8,6) — leaving the Arena Gate at (10,5) wide open! In the east Marrowgate alcove, remember a sparring partner weighs as much as a boulder!",
            "Main Gauntlet: push (7,14) east 3 tiles onto P2 (10,14). Walk up the center aisle to (8,9), step onto the west rope at (4,11) and weave south-north twice to draw both partners below the ropes, then climb x=4 to (5,8), push (5,7) north 1 tile to (5,6), step to (4,6), and push east 3 tiles onto P1 (8,6) — the Arena Gate (10,5) opens unobstructed! Marrowgate: push (22,14) north 5 tiles onto M1 (22,9), then stand south of the rope at (25,13) to pull Machoke onto M2 (25,11)!"
        ),
        skip_273,
        reset_choices=[
            ('Reset Main Gauntlet', reset_g, 'Apprentice Hiro: Main Gauntlet boulders and sparring partners are back on their chalk marks!'),
            ('Reset Marrowgate Alcove', reset_m, 'Apprentice Hiro: Marrowgate Mastery alcove is reset to its starting marks!'),
            ('Reset Both Sections', reset_both, 'Apprentice Hiro: Both the Main Gauntlet and Marrowgate alcove are reset. Fresh stance!'),
        ],
    ))
    E.append({
        'type': 'event',
        'name': 'Gauntlet Reset Bell',
        'at': [13, 22],
        'pages': [{
            'trigger': 'action',
            'commands': [{'script': reset_g + '\npbMessage(_INTL("CLANG! Main Gauntlet boulders and sparring partners reset cleanly!"))'}],
        }],
    })
    E.append({
        'type': 'event',
        'name': 'Marrowgate Reset Bell',
        'at': [24, 21],
        'pages': [{
            'trigger': 'action',
            'commands': [{'script': reset_m + '\npbMessage(_INTL("CLANG! Marrowgate Mastery alcove reset cleanly!"))'}],
        }],
    })
    E.append(_sign(
        'Marrowgate Plaque', (20, 21),
        "MARROWGATE — SEALED AF 285 — BY ORDER. (Optional Mastery Alcove: Two iron plates, one boulder, one sparring partner. A partner weighs as much as a boulder.)"
    ))

    E.append(_trainer(
        (15, 22), 'CUEBALL', 'Tetsu', 'right',
        "Cue Ball Tetsu: Pit Brawler born and bred! You don't step into Kaito's final Gauntlet without getting past me!",
        "Cue Ball Tetsu: Pit Brawler. Was. Give me a minute. Don't miss that east alcove if you want to know what Kaito's carrying.",
        sight=3,
    ))

    _place_stamp_over(m, 'pf_bellpost', 13, 20, base_z=1, top_z=2, top_rows=2, solid=True) # Base (13, 22) (clear of y=20 rail!)
    _place_stamp_over(m, 'pf_bellpost', 24, 19, base_z=1, top_z=2, top_rows=2, solid=True) # Base (24, 21)
    _place_stamp_over(m, 'pf_signpost', 20, 20, base_z=1, top_z=2, top_rows=1, solid=True) # Base (20, 21)
    # North braziers shifted cleanly onto y=4 (bases (6,5) & (14,5)) leaving ALL of y=6 & y=7 100% open for boulder pushes!
    braziers_273 = [(3, 21), (26, 21), (6, 4), (14, 4), (21, 7), (26, 7)]
    for bx, by in braziers_273:
        _place_stamp_over(m, 'fw_brazier', bx, by, base_z=1, top_z=2, top_rows=1, solid=True)
    for bx, by, bn in ((5, 3, 'wr_ban_ash'), (15, 3, 'wr_ban_bone'), (22, 5, 'wr_ban_bone'), (25, 5, 'wr_ban_bone')):
        _place_stamp_over(m, bn, bx, by, base_z=1, top_z=2, top_rows=1, solid=True)

    m.paint()
    _paint_pit_floors(m, [
        (3, 5, 18, 19, 'sand'),
        (21, 7, 26, 18, 'slate'),
        (24, 7, 26, 11, 'soot'),
        (3, 20, 26, 22, 'flag'),
        (9, 22, 11, 24, 'iron'),
        (9, 4, 11, 5, 'iron'),
    ])
    _paint_crimson_runner(m, 9, 22, 11, 24, medallion_y=23)
    _paint_ropes(m, ropes_g_h + ropes_m_h, ropes_g_v, ropes_vr=ropes_g_vr)

    # Riveted Iron Barriers (100% solid pas=0xf, immune to Cave.tidy!):
    # 1) Main Gauntlet central bastion (9..11, 9)
    m.L[1, 9, 9] = T_RAIL_W
    m.L[1, 9, 10] = T_RAIL_M
    m.L[1, 9, 11] = T_RAIL_E
    # 2) Main Gauntlet south divider fence along y=20 leaving ONLY 3-wide central archway (x=9..11) open (fixes P1-273-1!)
    for rx in range(3, 19):
        if rx in (9, 10, 11):
            continue
        if rx == 8:
            m.L[1, 20, rx] = T_RAIL_E
        elif rx == 12:
            m.L[1, 20, rx] = T_RAIL_W
        else:
            m.L[1, 20, rx] = T_RAIL_M
    # 3) North Arena Gate throat framing (9, 4..5) & (11, 4..5) with seamless vertical ironstone walls!
    for ry in (4, 5):
        m.L[1, ry, 9] = T_WALL_V
        m.L[1, ry, 11] = T_WALL_V
    m.L[1, 4, 10] = T_PDOOR_OPEN
    # 4) Marrowgate Alcove vertical stone partition (23, 9..12) + horizontal south doorway rail (21, 19) & (24..26, 19)!
    for ry in range(9, 13):
        m.L[1, ry, 23] = T_WALL_V
    m.L[1, 19, 21] = T_RAIL_E
    m.L[1, 19, 24] = T_RAIL_W
    m.L[1, 19, 25] = T_RAIL_M
    m.L[1, 19, 26] = T_RAIL_E

    Lr = RC.resolve(m.L, TID).astype(np.int32)
    # Clean, 100% unobstructed overhead light shafts strictly on open floor (ZERO overlap with plates, boulders, ropes, or pursuers!)
    _add_shafts(Lr, [(9, 10), (15, 16)], label='Map 273')
    _assert_braziers_intact(Lr, braziers_273, 'Map 273')

    seen0 = _verify_gym_map(Lr, E, (10, 22), [
        ('Hiro', (6, 21), True), ('Gauntlet Reset', (13, 22), True), ('Marrowgate Reset', (24, 21), True),
        ('Tetsu', (15, 22), True), ('Marrowgate Plaque', (20, 21), True),
        ('Boulder 1', (7, 14), True), ('Boulder M', (22, 14), True), ('Marrowgate Coffer', (24, 7), True),
    ], 'Map 273 Start', exit_row=24)
    assert (10, 4) not in seen0, 'Map 273 BYPASS BUG: Arena Portal reachable at Start!'
    seen_s = _verify_gym_map(Lr, E, (10, 22), [('Arena Portal', (10, 4), False)], 'Map 273 Solved', exit_row=24, sw={S_GAUNTLET: True})
    assert (10, 4) in seen_s

    # Exhaustive Gauntlet Solver + Anti-Bypass + Post-Solve UNPLUGGED Arena Gate BFS Proof!
    w273g = _extract_walls_from_map(Lr, (3, 5, 18, 19), extra_solid={(10, 5), (8, 5), (12, 5)})
    st0 = ((10, 19), ((4, 10), (16, 10)), ((7, 14), (5, 7), (14, 14)))
    d_bypass, _, _ = _solve_bfs_exact(
        '273G-NoPush', (3, 5, 18, 19), w273g, ropes_g,
        (10, 19), [(4, 10), (16, 10)], [(7, 14), (5, 7), (14, 14)],
        lambda pl, pu, bl: (8, 6) in (set(bl) | set(pu)) and (10, 14) in (set(bl) | set(pu)),
        allow_push=False, max_states=100000
    )
    assert d_bypass is None, 'Map 273 Gauntlet ANTI-BYPASS FAILED: solvable without boulders!'
    pa, st1, e1 = _solve_stage_astar(
        (3, 5, 18, 19), w273g, ropes_g, st0,
        lambda pl, pu, bl: (10, 14) in bl,
        lambda s: abs(s[2][0][0] - 10) + abs(s[2][0][1] - 14) + abs(s[0][0] - (s[2][0][0] - 1)) + abs(s[0][1] - s[2][0][1])
    )
    assert pa is not None, 'Map 273 Main Gauntlet Stage 1 FAILED!'
    pb, st2, e2 = _solve_stage_astar(
        (3, 5, 18, 19), w273g, ropes_g, st1,
        lambda pl, pu, bl: (10, 14) in bl and (8, 6) in bl,
        lambda s: abs(s[2][1][0] - 8) + abs(s[2][1][1] - 6) + abs(s[0][0] - s[2][1][0]) + abs(s[0][1] - s[2][1][1])
    )
    assert pb is not None, 'Map 273 Main Gauntlet Stage 2 FAILED!'
    # PROVE Arena Gate (10,5) -> Warp (10,4) is 100% UNPLUGGED after solving with boulders remaining SOLID in place!
    pl_end, pu_end, bl_end = st2
    post_walls = (w273g - {(10, 5)}) | set(bl_end) | set(pu_end)
    q_post = deque([(pl_end, 0)])
    v_post = {pl_end}
    gate_steps = None
    while q_post:
        (cx, cy), cd = q_post.popleft()
        if (cx, cy) == (10, 4):
            gate_steps = cd
            break
        for dx, dy in _SOL_DIRS:
            nx, ny = cx + dx, cy + dy
            if ((3 <= nx <= 18 and 5 <= ny <= 19) or (nx, ny) == (10, 4)) and (nx, ny) not in post_walls and (nx, ny) not in v_post:
                v_post.add((nx, ny))
                q_post.append(((nx, ny), cd + 1))
    assert gate_steps is not None, f'Map 273 P0 PLUGGED GATE BUG: Arena Warp (10,4) unreachable from {pl_end} with boulders {bl_end}!'

    w273m = _extract_walls_from_map(Lr, (21, 7, 26, 18), extra_solid={(24, 7)})
    dm, stm, end_m = _solve_bfs_exact(
        '273 Marrowgate', (21, 7, 26, 18), w273m, ropes_m,
        (22, 18), [(25, 8)], [(22, 14)],
        lambda pl, pu, bl: (22, 9) in (set(bl) | set(pu)) and (25, 11) in (set(bl) | set(pu)),
        allow_push=True
    )
    assert dm is not None, 'Map 273 Marrowgate Mastery Solver FAILED!'
    assert (25, 11) in end_m[1] and (22, 9) in end_m[2], f'Marrowgate unexpected end state: {end_m}'
    print(f'Map 273 Dual Solver PASS: Gauntlet={len(pa)+len(pb)} steps ({e1+e2} states, Gate UNPLUGGED={gate_steps} steps to (10,4), 0 bypass!), Marrowgate={dm} steps ({stm} states)')

    os.makedirs(RAW_DIR, exist_ok=True)
    np.save(os.path.join(RAW_DIR, '273.npy'), Lr.astype(np.int16))
    spec = {
        'id': 273,
        'name': 'Ironreach Gym - Puzzle Room 3',
        'parent': 270,
        'bgm': 'Gym',
        'field': FIELD,
        'map_audio': {'bgm': 'Gym - Warden Hall', 'bgs': 'Drip - Nadir', 'bgs_volume': 25, 'rain': False},
        'tone': [-6, -8, -4, 8],
        'metadata': {'Name': 'Ironreach Gym', 'SnapEdges': True, 'MapPosition': IRONREACH_POS, 'BattleBack': 'indoor3'},
        'biome': 'interior',
        'tileset': TID,
        'raw': 'data/raw/273.npy',
        'events': E,
    }
    with open(os.path.join(SPEC_DIR, '273_ironreach_gym_273.yaml'), 'w', encoding='utf-8') as f:
        f.write('# GENERATED by mapgen/layouts/ironreach_gym.py (Batch 3G): Ironreach Gym - Puzzle Room 3.\n')
        f.write(yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))
    print('Wrote specs/273_ironreach_gym_273.yaml and data/raw/273.npy')
    return Lr


# =================================================================================================
# MAP 274 — IRONREACH GYM - WARDEN ARENA (Warden Kaito Ren, 21x17, TS 57, :COLOSSEUM)
# =================================================================================================
def build_274():
    W, H = 21, 17
    m = _new_pit_hall(W, H, seed=274, wall_kit='qy2', ter_kit='qy2')

    # Dramatic subterranean iron colosseum pit with elevated northern fighting dais!
    m.box(2, 2, 18, 14, FLOOR, '.')
    m.box(6, 2, 14, 6, TER, '.')              # Elevated Northern Ring Dais: wall y=2..3, open ring floor y=4..6!
    m.box(9, 14, 11, 16, FLOOR, '.')          # Exact 3-wide South Approach Vestibule (0 exit pockets!)
    m.mass_at([(2, 2), (3, 2), (2, 3), (18, 2), (17, 2), (18, 3), (2, 14), (18, 14)])
    m.stairs(9, 6, w=3, n=2, c='.')           # 3-wide stone steps ascending to Kaito's Dais!
    m.tidy()
    m.plan_cliffs(rows=2)

    E = m.events

    # Full-width 3-tile south exit carpet (9..11, 16) -> 273 (10, 6) down (100% open sand directly south of Arena Gate!)
    for rx in (9, 10, 11):
        E.append({
            'type': 'warp',
            'name': f'Back to Gauntlet {rx}',
            'at': [rx, 16],
            'to': {'map': 273, 'x': 10, 'y': 6, 'dir': 'down'},
            'se': 'Door exit',
        })

    # Framed East Fast-Exit Iron Cage Lift Deck (16..17, 13 directly in front of lm_lift cage!) -> 270 Entrance (10, 14) down!
    for lx in (16, 17):
        E.append({
            'type': 'warp',
            'name': f'Fast-Exit Lift {lx} to Entrance (270)',
            'at': [lx, 13],
            'to': {'map': 270, 'x': 10, 'y': 14, 'dir': 'down'},
            'se': 'Door slide',
        })
    # Solid readable Lift Signpost at (15, 13) — literally DIRECTLY LEFT of the bolted lift deck (16..17, 13) (fixes P1-274-1!)
    E.append(_sign(
        'Pit Fast-Exit Lift Sign', (15, 13),
        "PIT FAST-EXIT CAGE LIFT — Step onto the bolted iron lift deck directly to the right to ride straight back to Ironreach Gym's Entrance!"
    ))

    # Kaito's Lucario ("Memory") sitting quietly on the dais at (12, 5)!
    E.append({
        'type': 'event',
        'name': "Kaito's Lucario (Memory)",
        'at': [12, 5],
        'pages': [
            {
                'graphic': {'sprite': 'Followers/LUCARIO', 'dir': 'down'},
                'trigger': 'action',
                'move': 'fixed',
                'commands': ["Kaito's Lucario sits cross-legged against the far rope with its eyes shut, listening to the stillness of the Pit."],
            },
            {
                'cond': {'var': [V_CH9_STEP, 6]},
                'graphic': {'sprite': 'Followers/LUCARIO', 'dir': 'down'},
                'trigger': 'action',
                'move': 'fixed',
                'commands': ["Memory's eyes are open now. It watches you calmly — not your badge case, but the quiet warmth in your chest."],
            },
        ],
    })

    # WARDEN KAITO REN (canonical story/27_SCRIPT_CH9.md:410-439 & GYM_PUZZLES.md:1129-1142!)
    kaito_battle_ruby = f'''pbMessage(_INTL("Kaito: You made it through the Pit."))
pbMessage(_INTL("Kaito: The Open upstairs is for the crowd. This isn't. There's nobody watching this one."))
pbMessage(_INTL("Kaito: Ironreach's Warden is whoever wins the Iron Trial. I won it nine years ago. Every year somebody tries to take it off me. Every year I'm still here."))
pbMessage(_INTL("Kaito: Stand up. Again. That's all I teach. Ready?"))
if Prismfall.gym_battle(pfm_gym(:LEADER_KAITO), double: false)
  pbMessage(_INTL("Kaito: ...Good. Your Pokémon fight like they remember why."))
  Prismfall.award_badge(pfm_gym(:LEADER_KAITO))
  pbSEPlay("Anim/HealBell", 95, 100)
  pbMessage(_INTL("Eight deep notes ring out from your badge case. Light runs along its seams and pools in the corners, like water finding the low places."))
  pbMessage(_INTL("Kaito: It sings. Memory heard it too. Look — Lucario feel what's alive in a room. Sometimes what's alive in a room is more than the people in it."))
  pbReceiveItem(:TM31)
  pbMessage(_INTL("Kaito: Brick Break. It goes through walls. And that badge says Pokémon up to level forty-seven will heed you."))
  if $game_switches[{S_MARROWGATE}]
    pbMessage(_INTL("Kaito: ...And Hiro told me you opened the Marrowgate door back in the Gauntlet. It was empty, wasn't it."))
    pbMessage(_INTL("Kaito: ...I always hoped it would be."))
  end
  pbMessage(_INTL("Kaito: A fist is a promise. Don't make one you won't keep."))
  $game_variables[{V_CH9_STEP}] = 6 if $game_variables[{V_CH9_STEP}].to_i < 6
  $game_self_switches[[274, @event_id, "A"]] = true
  $game_map.need_refresh = true
end'''
    kaito_after_ruby = f'''if $game_switches[{S_MARROWGATE}]
  pbMessage(_INTL("Kaito: You opened the Marrowgate door. It was empty, wasn't it. ...I always hoped it would be."))
  pbMessage(_INTL("Kaito: Stand up. Again. Take the east cage lift back to the entrance — Odessa's waiting on the doorstep with something for your eighth badge."))
else
  pbMessage(_INTL("Kaito: The Promise Badge is yours. A fist is a promise — don't make one you won't keep."))
  pbMessage(_INTL("Kaito: Take the east cage lift back to the entrance. Odessa's waiting on the doorstep with HM02 Fly for your eighth badge."))
end'''
    E.append({
        'type': 'event',
        'name': 'Warden Kaito Ren',
        'at': [10, 5],
        'pages': [
            {
                'graphic': {'sprite': 'KAITO', 'dir': 'down'},
                'trigger': 'action',
                'move': 'fixed',
                'commands': [{'script': kaito_battle_ruby}],
            },
            {
                'cond': {'self': 'A'},
                'graphic': {'sprite': 'KAITO', 'dir': 'down'},
                'trigger': 'action',
                'move': 'fixed',
                'commands': [{'script': kaito_after_ruby}],
            },
        ],
    })

    # Architecture: Iron Colosseum Ring, Intact Blazing Braziers, Spectator Galleries, Framed East Cage Lift!
    for bx, by, bn in ((7, 2, 'wr_ban_ash'), (13, 2, 'wr_ban_ash'), (9, 2, 'wr_ban_bone'), (11, 2, 'wr_ban_bone')):
        _place_stamp_over(m, bn, bx, by, base_z=1, top_z=2, top_rows=1, solid=True)
    # 4 Intact Blazing Iron Braziers (ZERO detached pf_glow!; aligned cleanly on x=7 & x=13!)
    braziers_274 = [(7, 4), (13, 4), (7, 13), (13, 13)]
    for bx, by in braziers_274:
        _place_stamp_over(m, 'fw_brazier', bx, by, base_z=1, top_z=2, top_rows=1, solid=True)
    # Dark mining timber/iron posts (replaces white marble nr_col!) & spectator bleacher benches!
    for cx, cy in ((5, 8), (15, 8)):
        _place_stamp_over(m, 'cv_post', cx, cy, base_z=1, top_z=2, top_rows=1, solid=True)
    for by in (6, 8, 10, 12):
        _place_stamp_over(m, 'pf_logbench', 2, by, base_z=1, top_z=1, top_rows=0, solid=True)
    for by in (6, 8):
        _place_stamp_over(m, 'pf_logbench', 17, by, base_z=1, top_z=1, top_rows=0, solid=True)
    # Framed East Fast-Exit Iron Cage Lift Bay: lm_lift (16..17, 10..12) + pf_signpost (15, 12..13 -> base (15,13) solid!)
    _place_stamp_over(m, 'lm_lift', 16, 10, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'pf_signpost', 15, 12, base_z=1, top_z=2, top_rows=1, solid=True)

    for y in range(4, 17):
        for x in (9, 10, 11):
            m.keep_clear.add((x, y))
    for pt in ((14, 13), (15, 14), (16, 13), (17, 13), (16, 14), (12, 5)):
        m.keep_clear.add(pt)

    m.paint()
    _paint_pit_floors(m, [
        (2, 4, 18, 14, 'slate'),
        (6, 4, 14, 6, 'sand'),
        (6, 8, 14, 12, 'sand'),
        (2, 5, 4, 13, 'timber'),
        (16, 5, 18, 9, 'timber'),
        (15, 12, 17, 14, 'iron'),
        (9, 14, 11, 16, 'iron'),
    ])
    _paint_crimson_runner(m, 9, 14, 11, 16, medallion_y=15)
    # Warm golden step-over colosseum boxing ropes framing Kaito's battle floor + 3x3 white chalk Pokéball center circle!
    _paint_ropes(
        m,
        ropes_h=[(7, 8), (8, 8), (12, 8), (13, 8), (6, 12), (7, 12), (8, 12), (12, 12), (13, 12), (14, 12)],
        ropes_v=[(6, 9), (6, 10), (6, 11)],
        ropes_vr=[(14, 9), (14, 10), (14, 11)],
        ropes_nw=[(6, 8)],
        ropes_ne=[(14, 8)],
    )
    m.L[1, 9, 9], m.L[1, 9, 10], m.L[1, 9, 11] = 9656, 9657, 9658
    m.L[1, 10, 9], m.L[1, 10, 10], m.L[1, 10, 11] = 9664, 9665, 9666
    m.L[1, 11, 9], m.L[1, 11, 10], m.L[1, 11, 11] = 9672, 9673, 9674

    # Seamless vertical timber palisade railings framing West & East spectator galleries!
    for ry in (6, 7, 8, 9, 10, 11, 12):
        if m.L[1, ry, 4] == 0:
            m.L[1, ry, 4] = T_PAL_V
    for ry in (6, 7, 8, 9):
        if m.L[1, ry, 16] == 0:
            m.L[1, ry, 16] = T_PAL_V
    # Full 2-wide bolted iron fast-exit lift platform deck directly in front of lm_lift (16..17, 13)!
    m.L[1, 13, 16] = T_PDOOR_OPEN
    m.L[1, 13, 17] = T_PDOOR_OPEN

    Lr = RC.resolve(m.L, TID).astype(np.int32)
    # Single stark overhead colosseum spotlight squarely over Kaito's open fighting ring (off Kaito's sprite, ZERO pf_glow!)
    _add_shafts(Lr, [(9, 9)], label='Map 274')
    _assert_braziers_intact(Lr, braziers_274, 'Map 274')

    _verify_gym_map(Lr, E, (10, 15), [
        ('Warden Kaito', (10, 5), True),
        ('Lucario Memory', (12, 5), True),
        ('Fast-Exit Lift 16', (16, 13), False),
        ('Fast-Exit Lift 17', (17, 13), False),
        ('Lift Sign', (15, 13), True),
        ('South Exit', (10, 16), False),
    ], 'Map 274 Warden Arena', exit_row=16)

    os.makedirs(RAW_DIR, exist_ok=True)
    np.save(os.path.join(RAW_DIR, '274.npy'), Lr.astype(np.int16))
    spec = {
        'id': 274,
        'name': 'Ironreach Gym - Warden Arena',
        'parent': 270,
        'bgm': 'Gym',
        'field': FIELD,
        'map_audio': {'bgm': 'Gym - Warden Hall', 'bgs': 'Drip - Nadir', 'bgs_volume': 25, 'rain': False},
        'tone': [-6, -8, -4, 8],
        'metadata': {'Name': 'Ironreach Gym', 'SnapEdges': True, 'MapPosition': IRONREACH_POS, 'BattleBack': 'indoor3'},
        'biome': 'interior',
        'tileset': TID,
        'raw': 'data/raw/274.npy',
        'events': E,
    }
    with open(os.path.join(SPEC_DIR, '274_ironreach_gym_274.yaml'), 'w', encoding='utf-8') as f:
        f.write('# GENERATED by mapgen/layouts/ironreach_gym.py (Batch 3G): Ironreach Gym - Warden Arena.\n')
        f.write(yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))
    print('Wrote specs/274_ironreach_gym_274.yaml and data/raw/274.npy')
    return Lr


def main():
    build_270()
    build_271()
    build_272()
    build_273()
    build_274()
    print('Done: built & mathematically verified all 5 Ironreach Gym 8 maps (270, 271, 272, 273, 274)!')


if __name__ == '__main__':
    main()
