#!/usr/bin/env python3
"""layouts/ironreach_town.py — Act 3 Batch 3G: Ironreach Town, PC, Mart & The Iron Pit (4 Maps: 260, 261, 262, 263):
  - 260 Ironreach                     (44x40, TS 58 PF Rejuv Locks, Outdoor, :NEW_MOON, rubric: true)
      Gritty subterranean/canyon Nadir mining & pit-fighting town built inside old Aurel ironworks shafts:
      * North Escarpment Cavern Wall (y=0..5) with towering slate/timber mine shoring, runoff waterfall chutes,
        iron ventilation vents, and The Long Drop Cage Lift Station (lm_lift + hb_crane + Mandate scanner post
        + guarded PBMoveRoute::BACKWARD exit north -> 672 The Long Drop).
      * Upper Terrace (y=6..15, iron-railed platforms & stone staircases):
          - NW Terrace: Ironreach Pokémon Center (cv_pc -> IR_PC -> 261, HealingSpot [260, 8, 14]) + Pit Announcer's
            megaphone gantry + smelting brazier & chimney smoke.
          - North-Central Cage-Foot Plaza: Conclave Mandate Notice Board + unified ore-cart railhead.
          - NE Terrace: Grand Twin-Towered Colosseum Gatehouse (gt_gate4 -> IR_PIT -> 263 The Iron Pit), framed by
            blazing iron braziers (100% intact flames, 0 pf_glow!), Conclave faction banners & Wardens' envoys.
      * Central Mine-Rail & Chalk-Circle Plaza (y=16..27):
          - Unified Aurel Iron Ore-Cart Track Network (cv_rail_h/v/ne/nw/se/sw/end) connecting the NW mine mouth
            (pf_minemouth) across loaded ore carts (cv_cart) and smelting hearths to the SE hoist yard.
          - Iconic Chalk-Circle Sparring Plaza (packed red earth E_f framed by iron flagstones T_f & ropes) where
            Ironreach settles arguments with fists.
          - West Mid-Terrace: Ironreach Mart (cv_mart -> IR_MART -> 262) + The Last Rung Pawnshop (wh_c) with
            Six-Fingers Ottoline (live pf_trial_ready?(:OTTOLINE_LAST_RUNG) / pf_trial_talk(:OTTOLINE_LAST_RUNG)
            for NA_MEMORY_KATA Lucarionite + Fightinium Z!) & Gutter Book Chalk Board (live pf_trial_board(:NADIR)).
          - East Mid-Terrace: Aurel Smelting Foundry (wh_a) with roaring smelter chimneys (fw_smoke_a/w), forge
            braziers, crates, and Ashmarch/Conclave NPCs.
      * South Lower Ring (y=28..37):
          - South-Central Colosseum Archway to 270 Ironreach Gym — The Pit (wh_e -> IR_GYM -> 270, framed by iron
            railings, twin intact braziers, hanging ring bell pf_bellpost & Kaito's Gym plaque).
          - SW Miners' Row (wh_d, wh_f), Lamplighter Kid, Old Miner, visible PROTEIN Poké Ball (hidden=False).
          - SE Tailings Hoist Yard (wh_b, hb_crane), ore-cart spurs, Nadir Boy, visible ULTRABALL Poké Ball (hidden=False).
      * West Border Exit (x=0, y=20..22): full 3-wide PBMoveRoute::BACKWARD-guarded exit -> 692 The Tailings!
      * Honest Outdoor Rubric PASS (0 glow/shadow cheese, 0 border leaks, 0 clipping structures!).
  - 261 Ironreach Pokémon Center      (15x11, TS 34 Prismfall Interior — Gold Standard 221/591 Layout!)
      Symmetrical 5-wide 0x8f U-counter (7 tiles verified), Nurse + Healing balls + PC + unobstructed Town Map
      size(2,1), Gale Post Ironreach Branch, full 3-wide exit carpet warps (6..8, 10) <-> IR_PC (260).
  - 262 Ironreach Mart                (12x10, TS 34 Prismfall Interior — Gold Standard 222/202 Layout!)
      Flush 5-tile 0x8f counter, canonical Ch9 PBS inventory, complete un-sliced 2x2 crimson doormat with twin
      exit warps (5..6, 9) <-> IR_MART (260), airy east display aisle.
  - 263 The Iron Pit                  (41x33, TS 57 PF Rejuv Cave, field :COLOSSEUM)
      Iconic subterranean mined-out cavern fighting amphitheater & Conclave hall of Ironreach:
      * Sunken octagonal red-earth fighting pit framed by riveted iron railings (qy_rail_*) & 8 intact burning
        iron braziers (fw_brazier, 0 detached pf_glow!), flanked by elevated West/East spectator bleacher galleries
        and the elevated North Conclave High Dais hung with the 18-Plate banners!
      * Ch9 Conclave Lore Plaques & Open Bracket Slate (0 over_trigger? traps), Nell the Chalk-Girl (free between-
        round pit heal), Pit Announcer, Garret cameo ("Stranger" + Followers/LUCARIO), Post-game Kaito Registry hook
        (:PG_KAITO_PIT), hidden Medichamite meditation plinth (pf_mega_stone(:MEDICHAMITE)), 2 visible Poké Balls
        (MUSCLEBAND & MAXPOTION, hidden=False), full-width 3-wide south exit carpet warps (19..21, 32) <-> IR_PIT!
      * ALL 3 Canonical PBS Trainers with 100% OPEN sightlines:
          [BLACKBELT, Dunmore], [CRUSHGIRL, Ysa], [BLACKBELT, Gristle].

Canonical sources:
  - design/maps.json (260..263), design/ROUTES.yaml (672, 692), design/TRIAL_EVENTS.yaml (260, 263)
  - story/27_SCRIPT_CH9.md (Ironreach arrival, Pit Announcer, Conclave, Ironreach Open, Garret cameo)
  - pbs/trainers.txt (Dunmore, Ysa, Gristle — verified global_count == 1)

Run:
    /usr/bin/python3 -I mapgen/layouts/ironreach_town.py
"""
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

import rkit as K
from rkit import STAMPS, P1
from cavekit import Cave, FLOOR, TER, MASS
import rcompose as RC
import render as R
import passguard as PG
import craftkit as CK
from terrain import NB2AUTO
from interiorkit import TF

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(HERE, 'data', 'raw')
SPEC_DIR = os.path.join(HERE, 'specs')

TID_TOWN = 58       # PF Rejuv Locks: dark sump canals, waterfalls, full PF Rejuv industrial/mine stamps
TID_PIT = 57        # PF Rejuv Cave: subterranean cavern masonry, red colosseum earth, iron railings, braziers
TID_INT = 34        # Prismfall Interior
VOID34 = 5437
IRONREACH_POS = [0, 16, 13]
IRONREACH_HEAL_SPOT = [260, 8, 14]   # Walkable stone porch tile directly south of cv_pc door (8, 13)!


# =================================================================================================
# Shared Anti-P0 Event, Syntax & Strict Reachability Helpers
# =================================================================================================
def _guarded_unbuilt_transfer(map_id, tx, ty, direction, blocked_text):
    """Guarded exit to an unbuilt map using uppercase PBMoveRoute::BACKWARD (0 build warnings, 0 leaks)."""
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


def _visible_item(at, item_id):
    """Explicit visible Poké Ball item (hidden=False ALWAYS — never collides with HiddenItem!)."""
    return {'type': 'item', 'name': 'Item', 'at': list(at), 'item': item_id, 'hidden': False}


def _trainer(at, ttype, name, d, intro, after, sight=3, field='COLOSSEUM'):
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
        'rules': ['setBattleRule("field", :%s)' % field],
    }


def _event_footprint(e):
    ax, ay = int(e['at'][0]), int(e['at'][1])
    nm = e.get('name') or ''
    m = re.search(r'size\((\d+),(\d+)\)', nm, re.I)
    if not m:
        return [(ax, ay)]
    w, h = int(m.group(1)), int(m.group(2))
    return [(ax + dx, ay - dy) for dx in range(w) for dy in range(h)]


def _check_ruby_syntax(events, label):
    """Run `ruby -c` on 100% of Ruby script blocks & verify zero bare `return` / `pbShake`."""
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
                for ch in c.get('choices', []) or []:
                    if isinstance(ch, dict):
                        _walk(ch.get('commands'))

    for e in events:
        if e.get('type') == 'event':
            for pg in e.get('pages') or []:
                _walk(pg.get('commands'))
        elif e.get('type') in ('npc', 'sign'):
            _walk(e.get('commands'))

    for idx, sc in enumerate(scripts):
        assert 'pbShake' not in sc, f'{label} script #{idx} uses forbidden pbShake (use pfm_shake)!'
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


def _assert_braziers_intact(Lr, tid, braziers, label):
    br_ref = RC.resolve(np.array(STAMPS['fw_brazier']['layers'], dtype=np.int32), tid)
    flame_tid = int(br_ref[2, 0, 0])
    base_tid = int(br_ref[1, 1, 0])
    for bx, by in braziers:
        assert int(Lr[2, by, bx]) == flame_tid, (
            f'{label}: fw_brazier flame damaged at ({bx},{by})! got {Lr[2, by, bx]} != {flame_tid}'
        )
        assert int(Lr[1, by + 1, bx]) == base_tid, (
            f'{label}: fw_brazier base damaged at ({bx},{by + 1})! got {Lr[1, by + 1, bx]} != {base_tid}'
        )


def _verify_map_strict(Lr, tid, events, start, label, check_rubric=False, take_events=None,
                       check_border_leaks=False, exit_row=None):
    import build as B
    ts = R.tilesets()[tid]
    Z, H, W = Lr.shape
    max_tid = len(ts['passages'])
    assert (Lr[0] > 0).all(), f'{label}: void L[0] cells found!'
    assert (Lr >= 0).all() and (Lr < max_tid).all(), f'{label}: out-of-bounds tile IDs found (max={max_tid})!'

    ev_pts = [tuple(e['at']) for e in events if e and e.get('at')]
    if take_events:
        ev_pts += [tuple(te['at']) for te in take_events if te.get('at')]
    hits = PG.hits(Lr, ts, ev_pts)
    assert not hits, f'{label}: passguard hits {hits[:5]}'

    solid_ev = set()
    for e in events:
        if e.get('type') in ('npc', 'trainer', 'mart', 'item'):
            if not e.get('hidden'):
                solid_ev.add(tuple(e['at']))
        elif e.get('type') == 'event':
            pg0 = (e.get('pages') or [{}])[0]
            g = pg0.get('graphic') or {}
            if (g.get('sprite') or g.get('tile')) and not pg0.get('through'):
                solid_ev.add(tuple(e['at']))
    if take_events:
        for te in take_events:
            if te.get('name') in ('Nurse', 'Healing balls', 'PC'):
                solid_ev.add(tuple(te['at']))

    # Anti-P0 #1: ZERO over_trigger? traps!
    over_traps = []
    for e in events:
        et = e.get('type')
        fp = _event_footprint(e)
        if et == 'sign':
            for fx, fy in fp:
                if B.cell_passable(Lr, ts, fx, fy):
                    over_traps.append((e.get('name'), (fx, fy), 'sign on passable tile'))
        elif et == 'event':
            pg0 = (e.get('pages') or [{}])[0]
            trig = pg0.get('trigger', 'action')
            g = pg0.get('graphic') or {}
            has_solid_gfx = bool(g.get('sprite')) or (bool(g.get('tile')) and (ts['passages'][g['tile']] & 0x0f) == 0x0f)
            if trig == 'action' and not has_solid_gfx and pg0.get('commands'):
                for fx, fy in fp:
                    if B.cell_passable(Lr, ts, fx, fy):
                        over_traps.append((e.get('name'), (fx, fy), 'action event w/o solid gfx on passable tile'))
    assert not over_traps, f'{label}: over_trigger? traps detected: {over_traps}'

    # Anti-P0 #2: ZERO NPC / Trainer on solid tile!
    for e in events:
        et = e.get('type')
        ax, ay = int(e['at'][0]), int(e['at'][1])
        if et in ('trainer', 'npc'):
            assert B.cell_passable(Lr, ts, ax, ay), f'{label}: {et} {e.get("name")} at {(ax,ay)} on SOLID tile!'
        elif et == 'event':
            pg0 = (e.get('pages') or [{}])[0]
            if (pg0.get('graphic') or {}).get('sprite'):
                assert B.cell_passable(Lr, ts, ax, ay), f'{label}: sprite event {e.get("name")} at {(ax,ay)} on SOLID tile!'

    # Exact 4-bit directional BFS
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
    assert ok[sy, sx], f'{label}: BFS start {start} is NOT walkable!'
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

    # Anti-P0 #3: 100% open trainer sightlines!
    dir_vec = {'down': (0, 1, 2), 'up': (0, -1, 8), 'right': (1, 0, 6), 'left': (-1, 0, 4)}
    for e in events:
        if e.get('type') == 'trainer':
            tx, ty = int(e['at'][0]), int(e['at'][1])
            dx, dy, d = dir_vec[e.get('dir', 'down')]
            sight = int(e.get('sight', 3))
            cx, cy = tx, ty
            for step in range(1, sight + 1):
                nx, ny = cx + dx, cy + dy
                assert 0 <= nx < W and 0 <= ny < H, f'{label}: trainer {e["trainer"]} sightline OOB at {(nx,ny)}'
                assert ok[ny, nx] and (nx, ny) in seen, (
                    f'{label}: trainer {e["trainer"]} sightline blocked at step {step} {(nx,ny)}'
                )
                cx, cy = nx, ny

    # Anti-P0 #4: 100% event reachability!
    missing = []
    for e in events:
        at = tuple(e['at'])
        fp = _event_footprint(e)
        et = e.get('type')
        is_touch = et in ('exit', 'warp', 'door')
        if et == 'event':
            pg0 = (e.get('pages') or [{}])[0]
            if pg0.get('trigger') == 'touch':
                is_touch = True
            elif pg0.get('trigger') in ('autorun', 'parallel'):
                continue
        if is_touch:
            assert B.cell_passable(Lr, ts, at[0], at[1]), f'{label}: touch/warp/door {e.get("name")} at {at} is SOLID!'
            reach = at in seen
        else:
            reach = any(
                (fx, fy) in seen or any((fx + dx, fy + dy) in seen for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)))
                for fx, fy in fp
            )
            if not reach:
                for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                    mx, my = at[0] + dx, at[1] + dy
                    px, py = at[0] + 2 * dx, at[1] + 2 * dy
                    if 0 <= mx < W and 0 <= my < H and (px, py) in seen:
                        if any((int(Lr[z, my, mx]) > 0 and (ts['passages'][int(Lr[z, my, mx])] & 0x80)) for z in (0, 1, 2)):
                            reach = True
                            break
        if not reach:
            missing.append((e.get('name') or et, at))
    assert not missing, f'{label}: unreachable events: {missing}'

    # Anti-P0 #5: Zero unguarded border leaks on outdoor maps / zero exit pockets on interior south rows!
    touch_pts = {tuple(e['at']) for e in events if e.get('type') in ('warp', 'exit', 'door') or (
        e.get('type') == 'event' and (e.get('pages') or [{}])[0].get('trigger') == 'touch'
    )}
    if check_border_leaks:
        leaks = []
        for x in range(W):
            for y in (0, H - 1):
                if (x, y) in seen and (x, y) not in touch_pts:
                    leaks.append((x, y))
        for y in range(H):
            for x in (0, W - 1):
                if (x, y) in seen and (x, y) not in touch_pts:
                    leaks.append((x, y))
        assert not leaks, f'{label}: unguarded border leaks detected: {leaks}'
    if exit_row is not None:
        pockets = [x for x in range(W) if (x, exit_row) in seen and (x, exit_row) not in touch_pts]
        assert not pockets, f'{label}: unsealed exit pocket(s) on y={exit_row}: {pockets}'

    _check_ruby_syntax(events, label)

    if check_rubric:
        rub = B.rubric(Lr)
        print(f'{label} RUBRIC:', {k: round(v, 1) for k, v in rub.items()})
        assert rub['layer2'] >= 55.0, f'{label}: rubric layer2 {rub["layer2"]:.1f} < 55'
        assert rub['layer3'] >= 20.0, f'{label}: rubric layer3 {rub["layer3"]:.1f} < 20'
        assert rub['bare'] <= 35.0, f'{label}: rubric bare {rub["bare"]:.1f} > 35'
        assert rub['bare3x3'] <= 13.0, f'{label}: rubric bare3x3 {rub["bare3x3"]:.1f} > 13'
        assert rub['stacks'] >= 10.0, f'{label}: rubric stacks {rub["stacks"]:.1f} < 10'
        assert rub['mirror'] <= 15.0, f'{label}: rubric mirror {rub["mirror"]:.1f} > 15'

    print(f'{label}: PASS (BFS={len(seen)} cells, {len(events)} events, 0 over_trigger, 0 passguard, ruby -c OK)')
    return seen


def _stamp_raw(L, name, x, y, tid=TID_TOWN, taken=None, protect_top=False):
    st = STAMPS[name]
    sL = RC.resolve(np.array(st['layers'], dtype=np.int32), tid)
    _, h, w = sL.shape
    _, H, W = L.shape
    for dy in range(h):
        for dx in range(w):
            xx, yy = x + dx, y + dy
            if not (0 <= xx < W and 0 <= yy < H):
                continue
            used = False
            for z in (0, 1, 2):
                t = int(sL[z, dy, dx])
                if t:
                    if z == 2 and protect_top and int(L[2, yy, xx]) != 0:
                        continue
                    L[z, yy, xx] = t
                    used = True
            if used and taken is not None:
                taken[yy, xx] = True


def _stamp_bldg(L, name, x, y, taken, tid=TID_TOWN, door_link=None, door_name=None, plaque=None):
    st = STAMPS[name]
    sL = RC.resolve(np.array(st['layers'], dtype=np.int32), tid)
    _, h, w = sL.shape
    _, H, W = L.shape
    for dy in range(h):
        for dx in range(w):
            xx, yy = x + dx, y + dy
            if not (0 <= xx < W and 0 <= yy < H):
                continue
            t0, t1, t2 = int(sL[0, dy, dx]), int(sL[1, dy, dx]), int(sL[2, dy, dx])
            if t0:
                L[0, yy, xx] = t0
                if not t1:
                    L[1, yy, xx] = 0
            if t1:
                L[1, yy, xx] = t1
            if t2:
                L[2, yy, xx] = t2
            if t0 or t1 or t2:
                taken[yy, xx] = True
    dr = st.get('door')
    if dr is not None:
        dx, dy = x + dr[0], y + dr[1]
        if door_link:
            return {
                'type': 'door',
                'name': door_name or (name + ' door'),
                'at': [dx, dy],
                'gfx': ['', 0, 2],
                'link': door_link,
                'fixed': True,
            }, (dx, dy)
        elif plaque:
            if int(L[2, dy, dx]) != 0:
                L[1, dy, dx] = int(L[2, dy, dx])
            blk = PG.blocker(R.tilesets()[tid])
            if blk is not None:
                L[2, dy, dx] = blk
            return _sign(door_name or (name + ' plaque'), (dx, dy), plaque), (dx, dy)
    return None, None


# =================================================================================================
# 1. MAP 260 — IRONREACH (44x40, TS 58 PF Rejuv Locks, Outdoor, :NEW_MOON, rubric: true)
# =================================================================================================
def build_260():
    W, H = 44, 40
    L = np.zeros((3, H, W), dtype=np.int32)
    taken = np.zeros((H, W), dtype=bool)

    # TS 58 Autotile base:
    #   slot 1 (48): PF Lock Water (deep moody subterranean navy-slate sump water, pas=0xf — ZERO sky-blue!)
    AUTO_SUMP = 48

    # Verified PF Rejuv Industrial / Mining Terraced Tile Palette
    EARTH = [P1('E_f%d' % i) for i in range(4)]           # Packed red-ochre Colosseum / chalk-ring earth
    SLATE = [P1('L_f%d' % i) for i in range(4)]           # Dark subterranean ironstone paving
    FLAG = [P1('T_f%d' % i) for i in range(4)]            # Cut iron-grey quarry flagstones
    IRON_DECK = [P1('Q_f%d' % i) for i in range(4)]       # Riveted iron-plate catwalk decks
    TIMBER = [P1('N_f%d' % i) for i in range(4)]          # Heavy dark mine-timber decking
    SOOT = [P1('cv_mud%d' % i) for i in range(4)]         # Sooty Aurel shaft dirt

    RAIL_W, RAIL_M, RAIL_E = P1('qy_rail_w'), P1('qy_rail_m'), P1('qy_rail_e')
    STAIR_L, STAIR_M, STAIR_R = P1('st_stair_l'), P1('st_stair_m'), P1('st_stair_r')

    def _kit_rows(kname):
        return [
            [int(RC.resolve(np.array([[[t if isinstance(t, int) else P1(t)]]], dtype=np.int32), TID_TOWN)[0, 0, 0]) for t in row]
            for row in K.KITS[kname]['rows']
        ]
    cvE_rows = _kit_rows('cvE')   # Warm rugged subterranean ironstone rock (ZERO icy-blue glacier!)
    cvT_rows = _kit_rows('cvT')   # Heavy dark mine-timber shoring
    qy_rows = _kit_rows('qy')     # Cut dark ironstone quarry masonry

    def _fill_base(x0, y0, x1, y1, pal, accent=None):
        for y in range(max(0, y0), min(H, y1 + 1)):
            for x in range(max(0, x0), min(W, x1 + 1)):
                L[0, y, x] = pal[(x * 7 + y * 11 + (x // 5)) % len(pal)]
                if accent is not None:
                    L[1, y, x] = accent[(x * 5 + y * 13 + (y // 3)) % len(accent)]

    # ---- 1. Subterranean Canyon Base Floor & Moody Dark Sump Basins ----
    _fill_base(0, 0, W - 1, H - 1, SLATE)

    sump = np.zeros((H, W), dtype=bool)
    sump[5:12, 0:4] = True        # NW deep drainage sump under west iron sluice
    sump[5:9, 40:44] = True       # NE narrow drainage culvert under east iron sluice
    sump[35:40, 0:4] = True       # SW sump sink
    sump[38:40, 39:44] = True     # SE compact sump culvert
    sump[38:40, 4:16] = True      # South-west sump runoff
    sump[38:40, 27:39] = True     # South-east sump runoff
    for y in range(H):
        for x in range(W):
            if sump[y, x]:
                L[0, y, x] = AUTO_SUMP + NB2AUTO[CK.nbits(sump, x, y)]
                taken[y, x] = True

    # ---- 2. Towering Seamless North Cavern Escarpment Wall (y=0..4, x=0..43) & Continuous Solid Stone Borders ----
    ROCK_SOLID = cvE_rows[1][1]     # Seamless dark warm subterranean rock face (pas=0xf, ZERO black gaps!)
    ROCK_BASE = cvE_rows[2][1]      # Seamless subterranean rock base face (pas=0xf)
    STONE_SOLID = qy_rows[1][1]     # Seamless cut ironstone masonry (pas=0xf)
    STONE_BASE = qy_rows[2][1]      # Cut ironstone masonry base (pas=0xf)
    ROCK_STRATA = (23781, 23786, 23788)                 # 100% solid, 0% black-notch subterranean rock strata (all pas=0xf)
    STONE_ASHLAR = (20206, 20207, 20208, 20209)         # 100% solid, 0% black-notch cut ironstone quarry blocks (all pas=0xf)
    TIMBER_WALL = (23954, 23959)                        # 100% solid, 0% vertical-slit mine timber shoring (all pas=0xf)

    def _rock(x, y):
        return ROCK_STRATA[(x * 7 + y * 13 + (x // 3)) % len(ROCK_STRATA)]

    def _stone(x, y):
        return STONE_ASHLAR[(x * 5 + y * 11 + (x // 4)) % len(STONE_ASHLAR)]

    for x in range(W):
        L[0, 0, x] = _rock(x, 0)
        L[0, 1, x] = _rock(x + 2, 1)
        if (17 <= x <= 25) or (1 <= x <= 3) or (40 <= x <= 42):
            # Heavy cut ironstone masonry piers for Long Drop Lift & NW/NE drainage sluices (100% solid pas=0xf!)
            L[0, 2, x] = _stone(x, 2)
            L[0, 3, x] = _stone(x + 1, 3)
            L[0, 4, x] = 20211 if (x % 2 == 0) else 20212
            L[1, 2, x] = _stone(x + 2, 2)
        elif (4 <= x <= 14) or (28 <= x <= 38):
            # Heavy mine-timber shoring bays (100% solid seamless planks!)
            L[0, 2, x] = TIMBER_WALL[x % 2]
            L[0, 3, x] = TIMBER_WALL[(x + 1) % 2]
            L[0, 4, x] = cvT_rows[2][1]
            L[1, 2, x] = TIMBER_WALL[x % 2]
        else:
            L[0, 2, x] = _rock(x, 2)
            L[0, 3, x] = _rock(x + 1, 3)
            L[0, 4, x] = ROCK_BASE
        for yy in range(5):
            taken[yy, x] = True

    # Moody subterranean iron drainage sluice culverts on NW (x=1..2) & NE (x=41..42) cavern wall (ZERO sky-blue waterfalls!)
    for sx in (1, 2, 41, 42):
        L[1, 3, sx] = P1('lm_vent')
        L[1, 4, sx] = P1('cv_sluice') if sx in (1, 41) else P1('cv_sluice_hi')
    _stamp_raw(L, 'lm_steam0', 2, 4, protect_top=True)
    _stamp_raw(L, 'lm_steam1', 41, 4, protect_top=True)

    # Continuous cohesive dark ironstone East, West (except 3-wide Tailings exit y=20..22!) & South rock borders (ZERO checkerboard!)
    for y in range(5, H):
        for ex in (42, 43):
            if not sump[y, ex]:
                L[0, y, ex] = _rock(ex + 3, y)
                L[1, y, ex] = _stone(ex, y) if ex == 42 else _rock(ex, y + 4)
                taken[y, ex] = True
        if not (20 <= y <= 22):
            for wx in (0, 1):
                if not sump[y, wx]:
                    L[0, y, wx] = _rock(wx, y + 2)
                    L[1, y, wx] = _stone(wx + 1, y + 3) if wx == 1 else _rock(wx + 2, y)
                    taken[y, wx] = True
    for x in range(W):
        for sy in (38, 39):
            if not sump[sy, x]:
                L[0, sy, x] = _rock(x, sy) if sy == 38 else _rock(x + 3, sy + 1)
                L[1, sy, x] = _stone(x + 1, sy) if sy == 38 else 0
                taken[sy, x] = True

    # ---- 3. Terraced Iron-Shored Town Districts (Built Paving & Decking Layered Cleanly on L[1] Over Bedrock L[0]!) ----
    # Upper Terrace (y=5..15): Cut quarry flagstones layered over ironstone bedrock!
    _fill_base(4, 5, 39, 15, SLATE, accent=FLAG)
    # Upper Terrace retaining lip along y=15 (solid ironstone terrace face EXCEPT wide stone staircases!)
    stair_xs = {8, 9, 10, 20, 21, 22, 33, 34, 35}
    for x in range(2, 42):
        if x in stair_xs:
            L[0, 15, x] = STAIR_L if x in (8, 20, 33) else (STAIR_R if x in (10, 22, 35) else STAIR_M)
            L[1, 15, x] = 0
        else:
            L[0, 15, x] = STONE_BASE
            L[1, 15, x] = RAIL_W if (x - 1) in stair_xs else (RAIL_E if (x + 1) in stair_xs else RAIL_M)
            taken[15, x] = True

    # Central Canyon Floor (y=16..27): Sooty mining dirt base + built iron flagstones, timber pads & iron decks on L[1]!
    _fill_base(2, 16, 41, 27, SOOT)
    # Main West-East Canyon Thoroughfare (y=20..22, x=0..41) — iron flagstones layered over bedrock!
    _fill_base(0, 20, 41, 22, SLATE, accent=FLAG)
    # North-South Central Foundry Spine — riveted iron-plate catwalk layered over bedrock!
    _fill_base(19, 6, 23, 14, SLATE, accent=IRON_DECK)
    _fill_base(20, 16, 22, 17, SLATE, accent=IRON_DECK)
    _fill_base(20, 25, 22, 27, SLATE, accent=IRON_DECK)
    # Upper terrace riveted iron-plate aprons framing PC & Iron Pit plazas!
    _fill_base(4, 12, 14, 14, SLATE, accent=IRON_DECK)
    _fill_base(29, 12, 39, 14, SLATE, accent=IRON_DECK)
    # West Mart & Last Rung weathered mine-timber platform layered over shaft dirt!
    _fill_base(3, 17, 16, 26, SOOT, accent=TIMBER)
    # East Smelting Foundry iron-plate & quarry flagstone work yard!
    _fill_base(28, 17, 40, 26, SLATE, accent=FLAG)
    _fill_base(30, 24, 39, 26, SLATE, accent=IRON_DECK)

    # Iconic Central Chalk-Circle Sparring Plaza (x=17..25, y=18..24): pure packed red earth + crisp WHITE CHALK RING & CENTER CIRCLE!
    _fill_base(17, 18, 25, 24, SLATE, accent=FLAG)
    _fill_base(18, 19, 24, 23, EARTH)
    L[1, 19:24, 18:25] = 0   # Clear flagstone L[1] completely so entire chalk ring sits on pure red-ochre sand!
    L[1, 19, 18] = 9667; L[1, 19, 24] = 9669
    L[1, 23, 18] = 9683; L[1, 23, 24] = 9685
    for rx in range(19, 24):
        L[1, 19, rx] = 9668
        L[1, 23, rx] = 9684
    for ry in range(20, 23):
        L[1, ry, 18] = 9675
        L[1, ry, 24] = 9677
    L[1, 20, 20], L[1, 20, 21], L[1, 20, 22] = 9656, 9657, 9658
    L[1, 21, 20], L[1, 21, 21], L[1, 21, 22] = 9664, 9665, 9666
    L[1, 22, 20], L[1, 22, 21], L[1, 22, 22] = 9672, 9673, 9674

    # Lower Terrace Retaining Lip at y=28 with symmetrical twin staircases (x=13..15 and x=27..29) flanking Kaito's Gym!
    lower_stair_xs = {13, 14, 15, 27, 28, 29}
    for x in range(2, 42):
        if x in lower_stair_xs:
            L[0, 28, x] = STAIR_L if x in (13, 27) else (STAIR_R if x in (15, 29) else STAIR_M)
            L[1, 28, x] = 0
        else:
            L[0, 28, x] = STONE_BASE
            L[1, 28, x] = RAIL_W if (x - 1) in lower_stair_xs else (RAIL_E if (x + 1) in lower_stair_xs else RAIL_M)
            taken[28, x] = True

    # South Lower Ring (y=29..37): Heavy quarry flagstones, timber worker walks & riveted Gym forecourt!
    _fill_base(2, 29, 41, 37, SLATE)
    _fill_base(12, 29, 30, 37, SLATE, accent=FLAG)
    _fill_base(16, 36, 26, 37, SLATE, accent=IRON_DECK)
    _fill_base(4, 35, 12, 37, SOOT, accent=TIMBER)
    _fill_base(30, 35, 40, 37, SOOT, accent=TIMBER)

    # Subtle weathered stepping stones on raw shaft dirt walkways (ZERO shadow/glow cheese!)
    for y in range(16, 35):
        for x in range(2, 42):
            if L[1, y, x] == 0 and not taken[y, x] and not sump[y, x]:
                if (x * 5 + y * 3) % 7 == 0 and y in (16, 17, 27, 30, 31, 32, 33, 34):
                    L[1, y, x] = P1('pf_stepstone0') if (x % 2 == 0) else P1('pf_stepstone1')

    # ---- 4. Unified Aurel Iron Ore-Cart Rail Track System (100% Continuous & Cleanly Capped — ZERO Wall/Roof Crashes!) ----
    R_H, R_V = P1('cv_rail_h'), P1('cv_rail_v')
    R_NE, R_NW, R_SE, R_SW = P1('cv_rail_ne'), P1('cv_rail_nw'), P1('cv_rail_se'), P1('cv_rail_sw')
    R_END = P1('cv_rail_end')

    # (1) Upper Mine-Mouth Line: emerges from pf_minemouth (15,6) -> (15,11) -> east to (27,11) -> south to buffer stop (27,14)!
    for ry in range(7, 11):
        L[1, ry, 15] = R_V
    L[1, 11, 15] = R_NE
    for rx in range(16, 27):
        L[1, 11, rx] = R_H
    L[1, 11, 27] = R_SW
    for ry in range(12, 14):
        L[1, ry, 27] = R_V
    L[1, 14, 27] = R_END
    taken[14, 27] = True

    # (2) Mid-Tier Foundry Line: clean buffer stop (18,16) clear of Last Rung roof -> (18,17) -> (27,17) -> (27,25) -> buffer stop (27,26)!
    L[1, 16, 18] = R_END
    taken[16, 18] = True
    L[1, 17, 18] = R_NE
    for rx in range(19, 27):
        L[1, 17, rx] = R_H
    L[1, 17, 27] = R_SW
    for ry in range(18, 26):
        L[1, ry, 27] = R_V
    L[1, 26, 27] = R_END
    taken[26, 27] = True

    # (3) South Hoist U-Spur: cleanly capped BOTH ends with R_END at (30,36) & (38,35) under SE hoist crane (leaving y=37 walk 100% open!)
    L[1, 36, 30] = R_END
    taken[36, 30] = True
    L[1, 37, 30] = R_NE
    for rx in range(31, 38):
        L[1, 37, rx] = R_H
    L[1, 37, 38] = R_NW
    L[1, 36, 38] = R_V
    L[1, 35, 38] = R_END
    taken[35, 38] = True

    # (4) West Tailings Spur: carries ore off-map west toward 692 along (0..1,21) -> curves south along west alley x=2 -> buffer stop (2,25)!
    L[1, 21, 0] = R_H
    L[1, 21, 1] = R_H
    L[1, 21, 2] = R_SW
    for ry in range(22, 25):
        L[1, ry, 2] = R_V
    L[1, 25, 2] = R_END
    taken[25, 2] = True

    # Loaded Aurel Iron Ore Carts seated crisply ON the tracks (cv_cart, pas=0xf — SE cart on (38,36) keeps SE hoist yard 100% reachable!)
    for cx, cy in ((15, 9), (27, 13), (27, 20), (27, 24), (38, 36)):
        L[1, cy, cx] = P1('cv_cart')
        taken[cy, cx] = True

    # ---- 5. Landmark Buildings (Distinct Gritty Industrial & Colosseum Architecture!) ----
    events = []

    # (a) NW Upper Terrace: Ironreach Pokémon Center (cv_pc 7x7 at (5, 7) -> door at (8, 13), HealingSpot (8, 14)!)
    ev_pc, pc_door = _stamp_bldg(L, 'cv_pc', 5, 7, taken, door_link='IR_PC', door_name='Ironreach PC Door')
    assert pc_door == (8, 13), f'Expected PC door (8,13), got {pc_door}'
    events.append(ev_pc)
    _stamp_raw(L, 'pf_pcsign', 12, 12, taken=taken)

    # (b) North-Central: The Long Drop Cage Lift Station (lm_lift 2x3 at (20, 3) + hb_crane 3x5 at (23, 2)!)
    _stamp_raw(L, 'lm_lift', 20, 3, taken=taken)
    _stamp_raw(L, 'hb_crane', 23, 2, taken=taken)
    _stamp_raw(L, 'pf_minemouth', 14, 4, taken=taken)
    blk58 = PG.blocker(R.tilesets()[TID_TOWN])
    L[2, 5, 15] = blk58
    taken[5, 15] = True

    # (c) NE Upper Terrace: Grand Twin-Towered Gatehouse to 263 The Iron Pit (gt_gate4 10x8 at (29, 5)!)
    _stamp_raw(L, 'gt_gate4', 29, 5, taken=taken)
    for ax in range(32, 36):
        L[0, 10, ax] = STONE_BASE
        L[1, 10, ax] = 0
        taken[10, ax] = True
        taken[11, ax] = False
        taken[12, ax] = False
        L[0, 11, ax] = SLATE[0]
        L[0, 12, ax] = IRON_DECK[0]
        events.append({
            'type': 'warp',
            'name': f'Iron Pit Arch {ax}',
            'at': [ax, 11],
            'to': {'map': 263, 'x': 20, 'y': 31, 'dir': 'up'},
            'se': 'Door enter',
        })

    # (d) West Mid-Terrace: Ironreach Mart (cv_mart 6x6 at (3, 18) -> door (4, 23)) + The Last Rung (wh_c 6x7 at (10, 17))!
    ev_mart, mart_door = _stamp_bldg(L, 'cv_mart', 3, 18, taken, door_link='IR_MART', door_name='Ironreach Mart Door')
    assert mart_door == (4, 23), f'Expected Mart door (4,23), got {mart_door}'
    events.append(ev_mart)
    ev_rung, _ = _stamp_bldg(
        L, 'wh_c', 10, 17, taken,
        door_name='The Last Rung Door',
        plaque="THE LAST RUNG — Pawnshop & Taproom. Chalked across the lintel: 'NO CREDIT. NO ACCORD SCRIPTS. SIX-FINGERS OTTOLINE, PROPRIETOR.'"
    )
    events.append(ev_rung)

    # (e) East Mid-Terrace: Aurel Smelting Foundry (wh_a 6x9 at (31, 16) -> door (34, 24))
    ev_fdy, _ = _stamp_bldg(
        L, 'wh_a', 31, 16, taken,
        door_name='Aurel Smelting Foundry Door',
        plaque="AUREL SMELTING WORKS — SHIFT 3. 'Keep fingers clear of the ore stamp. Kaito's ring chains were forged on Furnace Two.'"
    )
    events.append(ev_fdy)

    # Ensure south walkway y=36..37 across x=4..39 is dry walkable flagging (cleanly framed above sump y=38..39!)
    for x in range(4, 40):
        for sy in (36, 37):
            if sump[sy, x]:
                sump[sy, x] = False
                L[0, sy, x] = FLAG[x % 4]
                taken[sy, x] = False
    for y in range(34, 40):
        for x in range(W):
            if sump[y, x]:
                L[0, y, x] = AUTO_SUMP + NB2AUTO[CK.nbits(sump, x, y)]
                taken[y, x] = True

    # (f) South-Central: BESPOKE RIVETED IRON & ASHLAR STONE COLOSSEUM GYM FACADE — "THE PIT" (x=17..25, y=29..35 -> door (21, 35)!)
    # Grand 2-tile-deep iron forecourt across y=36..37 (replaces domestic brick townhouse wh_e!).
    for gx in range(17, 26):
        # Upper riveted iron parapet roof deck (y=29..32) — 100% solid pas=0xf (0 cut-off walkable roof tiles!)
        L[0, 29, gx] = STONE_SOLID
        L[1, 29, gx] = IRON_DECK[gx % 4]
        L[2, 29, gx] = RAIL_W if gx == 17 else (RAIL_E if gx == 25 else RAIL_M)
        L[0, 30, gx] = STONE_SOLID
        L[1, 30, gx] = STONE_SOLID
        L[0, 31, gx] = STONE_SOLID
        L[1, 31, gx] = STONE_SOLID
        L[0, 32, gx] = STONE_SOLID
        L[1, 32, gx] = STONE_BASE
        # Lower heavy cut-ironstone colosseum bastion wall (y=33..35)
        L[0, 33, gx] = STONE_SOLID
        L[1, 33, gx] = STONE_SOLID
        L[0, 34, gx] = STONE_SOLID
        L[1, 34, gx] = STONE_SOLID
        L[0, 35, gx] = STONE_BASE
        L[1, 35, gx] = STONE_BASE
        for gy in range(29, 36):
            taken[gy, gx] = True
    # Heavy vertical riveted steel corner buttresses on x=17 & x=25
    for gy in range(30, 36):
        L[1, gy, 17] = P1('nr_wall_v')
        L[1, gy, 25] = P1('nr_wall_v')
    # Glowing amber wall sconces & ventilation grates cleanly clear of Warden banners
    L[1, 34, 18] = P1('cv_walllamp'); L[1, 34, 24] = P1('cv_walllamp')
    L[1, 35, 19] = P1('lm_vent');     L[1, 35, 23] = P1('lm_vent')
    # Giant 3x3 riveted iron Pit Wheel emblem (lm_vault) centered on upper facade (20..22, 30..32)!
    _stamp_raw(L, 'lm_vault', 20, 30, taken=taken)
    # Recessed dark timber-and-iron Colosseum Pit Entry Archway (pf_minemouth 3x3 at 20..22, 33..35)!
    L[0, 34, 21] = SLATE[0]; L[1, 34, 21] = 0
    L[0, 35, 21] = IRON_DECK[0]; L[1, 35, 21] = 0
    _stamp_raw(L, 'pf_minemouth', 20, 33, taken=taken)
    # Solid blocker on (21, 34) behind the door, walkable dark portal recess on (21, 35) for IR_GYM door!
    L[2, 34, 21] = blk58
    L[1, 35, 21] = P1('lm_pdoor_open')
    taken[35, 21] = False
    events.append({
        'type': 'door',
        'name': 'Ironreach Gym Door',
        'at': [21, 35],
        'gfx': ['', 0, 2],
        'link': 'IR_GYM',
        'fixed': True,
    })
    # Iron bollards framing the wide 2-tile Colosseum forecourt (y=37 stays 100% open!)
    L[1, 36, 18] = P1('hb_bollard0'); taken[36, 18] = True
    L[1, 36, 24] = P1('hb_bollard0'); taken[36, 24] = True

    # (g) SW Miners' Hall (wh_b 7x8 at (4, 29) -> x=4..10, y=29..36, door (7, 36), completely clear of stairs 13..15!)
    ev_sw1, _ = _stamp_bldg(
        L, 'wh_b', 4, 29, taken,
        door_name='Miners Union Hall Door',
        plaque="NADIR PIT-WORKERS' HALL — 'Two hours up the Long Drop, one hour down. Count the chalk marks on the cage.'"
    )
    events.append(ev_sw1)

    # (h) SE Pit-Fighters' Barracks (wh_d 7x9 at (31, 28) -> x=31..37, y=28..36, door (34, 36), completely clear of stairs 27..29!)
    ev_se1, _ = _stamp_bldg(
        L, 'wh_d', 31, 28, taken,
        door_name='Pit-Fighters Barracks Door',
        plaque="IRONREACH OPEN BARRACKS — 'Chalk your palms, wrap your wrists, leave your coat on the hook. Winners buy the tea.'"
    )
    events.append(ev_se1)
    # SE Tailings Hoist Crane cleanly perched at (39, 29..33)
    _stamp_raw(L, 'hb_crane', 39, 29, taken=taken)

    # ---- 6. Gritty Subterranean Ironworks Street Furniture, Blazing Braziers, Sump Pumps, Shoring Arches & Iron Lamps! ----
    # (ZERO carnival pf_lstring lantern strings! ZERO pf_glow!)
    # NW & NE Sump Drainage Waterwheel Pumps sitting cleanly on the dark sump edges!
    _stamp_raw(L, 'cv_pump', 3, 5, taken=taken)
    _stamp_raw(L, 'cv_pump', 39, 5, taken=taken)

    braziers_260 = [
        (4, 12), (13, 12),       # Framing Ironreach PC terrace
        (30, 12), (37, 12),      # Framing Grand Iron Pit Gatehouse
        (17, 17), (25, 17),      # Framing Central Chalk-Circle Plaza
        (16, 34), (26, 34),      # Framing Ironreach Colosseum Gym — The Pit (bases 16,35 & 26,35)
        (38, 22),                # Aurel Smelting Foundry exterior furnace hearth
        (11, 25), (30, 23),      # Last Rung & Foundry street braziers
    ]
    for bx, by in braziers_260:
        _stamp_raw(L, 'fw_brazier', bx, by, taken=taken)

    _stamp_raw(L, 'pf_bellpost', 27, 34, taken=taken)      # Base (27, 36) solid -> Kaito's Gym Bell!
    _stamp_raw(L, 'pf_signpost', 18, 6, taken=taken)       # Base (18, 7) solid -> Conclave Mandate Notice!
    _stamp_raw(L, 'pf_signpost', 15, 35, taken=taken)      # Base (15, 36) solid -> Ironreach Gym Plaque!
    _stamp_raw(L, 'pf_signpost', 16, 23, taken=taken)      # Base (16, 24) solid -> Gutter Book Chalk Board!
    _stamp_raw(L, 'pf_signpost', 2, 18, taken=taken)       # Base (2, 19) solid -> West Road Sign (The Tailings)!

    # Tall Warden & Conclave banners (natural gritty vertical L[2] framing!)
    for bx, by, bname in (
        (28, 10, 'wr_ban_ash'), (39, 10, 'wr_ban_ise'),
        (27, 6, 'wr_ban_bone'), (19, 3, 'hb_banner'),
        (18, 30, 'wr_ban_ash'), (24, 30, 'wr_ban_bone'),
        (16, 30, 'hb_banner'), (26, 30, 'hb_banner'),
        (2, 16, 'wr_ban_bone'), (40, 16, 'wr_ban_ash'),
    ):
        _stamp_raw(L, bname, bx, by, taken=taken, protect_top=True)

    # Overhead heavy timber mine-shoring portal arches cleanly straddling ore tracks & stairways (center tile stays walkable!)
    for fx, fy in (
        (20, 7),                 # Straddles Long Drop central catwalk (21,8 walkable!)
        (14, 7),                 # Straddles upper ore-cart track out of mine mouth (15,8 walkable!)
        (26, 21),                # Straddles mid-tier foundry ore track (27,22 walkable!)
        (19, 25),                # Straddles central spine south of Chalk Ring (20,26 walkable!)
        (28, 26),                # Straddles SE stair approach (29,27 walkable!)
    ):
        _stamp_raw(L, 'cv_frame', fx, fy, taken=None, protect_top=True)

    # Anchored tall iron mining streetlamps (pf_wlamp 1x3, pf_lantern 1x3) & industrial machinery (zero cut-off pockets!)
    for sx, sy, sname in (
        (4, 7, 'pf_wlamp'), (13, 7, 'pf_wlamp'), (17, 7, 'pf_lantern'), (26, 7, 'pf_lantern'),
        (28, 12, 'pf_wlamp'), (39, 12, 'pf_wlamp'),
        (6, 15, 'pf_lantern'), (12, 15, 'pf_lantern'), (31, 15, 'pf_lantern'), (38, 15, 'pf_lantern'),
        (3, 24, 'pf_wlamp'), (16, 25, 'pf_wlamp'), (29, 24, 'pf_wlamp'), (40, 24, 'pf_wlamp'),
        (11, 33, 'pf_wlamp'), (30, 33, 'pf_wlamp'), (14, 31, 'pf_lantern'), (28, 31, 'pf_lantern'),
        (40, 34, 'pf_wlamp'), (5, 25, 'pf_lantern'), (24, 25, 'pf_lantern'),
        # Industrial dynamos, crates, barrels, foundry supplies & benches (arranged cleanly with 0 sealed pockets!)
        (2, 13, 'lm_gen'), (39, 18, 'lm_gen'), (11, 30, 'lm_gen'), (29, 29, 'lm_gen'),
        (3, 26, 'hb_boxes'), (38, 20, 'hb_boxes'), (38, 24, 'hb_barrels'),
        (2, 26, 'wr_sandbags'), (2, 27, 'wr_sacks'),    # Fill west alley tip cleanly behind rail stop (0 cut-off tiles!)
        (29, 17, 'wr_sacks'), (30, 17, 'wr_sandbags'), (39, 16, 'wr_sandbags'),
        (6, 17, 'pf_stonebench'), (29, 14, 'pf_logbench'), (17, 25, 'pf_logbench'), (23, 25, 'pf_logbench'),
        (14, 13, 'hb_rope'), (37, 24, 'wr_rack'), (17, 13, 'wr_supply'), (24, 13, 'hb_tables'),
        (13, 30, 'wr_sandbags'), (2, 30, 'sh_crates'), (2, 33, 'hb_barrels'), (3, 33, 'hb_barrels'),
        (3, 16, 'lm_gearbox'), (28, 16, 'lm_gearbox'), (15, 29, 'lm_gearbox'),
    ):
        _stamp_raw(L, sname, sx, sy, taken=taken, protect_top=True)

    # Foundry chimney smoke & subterranean boiler steam plumes on L[2] (100% authentic industrial atmosphere!)
    for vx in (6, 10, 18, 25, 31, 36):
        if int(L[1, 3, vx]) == 0:
            L[1, 3, vx] = P1('lm_vent')
    for sx, sy, sname in (
        (6, 0, 'fw_smoke_w'), (11, 0, 'fw_smoke_a'), (24, 0, 'fw_smoke_w'), (36, 0, 'fw_smoke_w'),
        (33, 15, 'fw_smoke_a'), (35, 16, 'fw_smoke_w'), (37, 20, 'lm_steam0'),
        (3, 10, 'lm_steam1'), (39, 16, 'lm_steam0'), (12, 28, 'lm_steam1'), (30, 28, 'lm_steam0'),
    ):
        _stamp_raw(L, sname, sx, sy, protect_top=True)

    # Re-ensure Gym portal tile stays clean on L[1]
    L[1, 35, 21] = P1('lm_pdoor_open')

    # ---- 7. Canonical Events, Live Nadir Trials, Guarded Route Exits & Visible Pickups! ----
    for lx in (20, 21):
        events.append({
            'type': 'event',
            'name': f'Long Drop Lift {lx}',
            'at': [lx, 6],
            'pages': [{
                'trigger': 'touch',
                'commands': _guarded_unbuilt_transfer(
                    672, 32, 126, 'up',
                    "Lift Operator: Cage up to the Long Drop is under Directorate winch inspection right now — one hour down, two hours up. Come back once the cable clears!"
                ),
            }],
        })

    for wy in (20, 21, 22):
        events.append({
            'type': 'event',
            'name': f'Tailings Road Exit {wy}',
            'at': [0, wy],
            'pages': [{
                'trigger': 'touch',
                'commands': _guarded_unbuilt_transfer(
                    692, 98, 35, 'left',
                    "Shaft Guard: The Tailings waste hills west of here are shifting after the last ore dump. Wait till the crew shoves the slag piles clear before heading toward Rootdeep!"
                ),
            }],
        })

    ottoline_ruby = '''if (pf_trial_ready?(:OTTOLINE_LAST_RUNG) rescue false)
  pf_trial_talk(:OTTOLINE_LAST_RUNG)
else
  pbMessage(_INTL("Six-Fingers Ottoline: Six fingers on the left, none of them idle. Welcome to the Last Rung."))
  pbMessage(_INTL("Six-Fingers Ottoline: Chalk jobs for the Gutter Book are pinned right beside me on the post. Don't waste my chalk if you can't hold a stance."))
  pbMessage(_INTL("Six-Fingers Ottoline: Top shelf inside? Old Wardguard ring-stone. Owner comes in once a year to look at it. Not for sale yet — come back when your badge case sings loud enough."))
end'''
    events.append({
        'type': 'event',
        'name': 'Six-Fingers Ottoline',
        'at': [14, 24],
        'pages': [{
            'graphic': {'sprite': 'NPC 23', 'dir': 'down'},
            'trigger': 'action',
            'move': 'fixed',
            'commands': [{'script': ottoline_ruby}],
        }],
    })

    events.append({
        'type': 'event',
        'name': 'Gutter Book Chalk Board',
        'at': [16, 24],
        'pages': [{
            'trigger': 'action',
            'commands': [{
                'if': 'defined?(pf_trial_board)',
                'then': [{'script': 'pf_trial_board(:NADIR)'}],
                'else': ["GUTTER BOOK — IRONREACH CHALK BOARD: 'Pit Ringer: six bouts in the Iron Pit. Lamplighter Kids: old sump lanterns running low.'"],
            }],
        }],
    })

    events.append(_sign(
        'Conclave Mandate Notice', (18, 7),
        "BY MANDATE: A CONCLAVE OF THE ACCORD WILL SIT IN THE IRON PIT. THE IRONREACH OPEN WILL PROCEED AS ENTERTAINMENT. — A. HOLLIS, CHANCELLOR. (Scrawled underneath in thick white chalk: 'ENTERTAINMENT FOR WHO.')"
    ))
    events.append(_sign(
        'Ironreach Gym Sign', (15, 36),
        "IRONREACH GYM — THE PIT. Warden Kaito Ren (Fighting, Colosseum). 'Don't fight the one in front of you. Move it. A fist is a promise.'"
    ))
    events.append(_sign(
        'Tailings Road Sign', (2, 19),
        "IRONREACH — Nadir's Pit-Fighting Quarter. ← The Tailings & Rootdeep · ↑ The Long Drop Cage Lift · → The Iron Pit · ↓ Kaito's Gym."
    ))
    events.append({
        'type': 'event',
        'name': 'Gym Forecourt Bell',
        'at': [27, 36],
        'pages': [{
            'trigger': 'action',
            'commands': [
                {'script': 'pbSEPlay("Mining iron", 90, 95)'},
                "CLANG! A heavy bronze ring-bell outside Kaito's gym sends a deep note echoing up the mine galleries.",
            ],
        }],
    })

    events.append(_make_npc('Pit Announcer', (18, 12), 'NPC 15', 'down', [
        "Pit Announcer (through a brass trumpet): AND HERE COMES A CHALLENGER RIGHT ACROSS IRONREACH, FOLKS! GOOD SHOES! VERY STRAIGHT FACE!",
        "Pit Announcer: THE IRONREACH OPEN IS PACKED TO THE RAFTERS UP IN THE IRON PIT EAST OF HERE — AND ALL EIGHTEEN WARDENS ARE IN TOWN FOR THE CONCLAVE!",
    ]))
    events.append(_make_npc('Old Miner', (16, 13), 'NPC 22', 'right', [
        "Old Miner: He does that. He narrates. He's done it for thirty years.",
        "Old Miner: He narrated my wedding. He narrated my divorce. It was the same speech.",
    ]))
    events.append(_make_npc('Chalk-Circle Woman', (17, 22), 'NPC 17', 'right', [
        "Chalk-Circle Woman: Got an argument? Draw a circle. Settle it. Leave.",
        "Chalk-Circle Woman: That's Ironreach. Topside they have courts and it takes three years and nobody's happy.",
    ]))
    events.append(_make_npc('Pit Sparrer West', (20, 21), 'trainer_BLACKBELT', 'right', [
        "Pit Sparrer: Footwork first! Kaito says if you swing before your heels are planted, you're punching air.",
    ]))
    events.append(_make_npc('Pit Sparrer East', (22, 21), 'trainer_CRUSHGIRL', 'left', [
        "Pit Sparrer: That's three rounds straight I've had him on the chalk line. Winner buys soup at the Last Rung!",
    ]))
    events.append(_make_npc('Nadir Boy', (29, 35), 'NPC 05', 'up', [
        "Nadir Boy: The Conclave's here! All the Wardens!",
        "Nadir Boy: I saw the fire one from Ashkaar. He's as big as a door. He picked me up to see better and then forgot to put me down!",
    ]))
    events.append(_make_npc('Lamplighter Runner', (12, 35), 'NPC 07', 'right', [
        "Lamplighter Kid: Us lamp-runners keep the iron streetlamps lit all down the Aurel shafts. Three of my mates went poking around the old sumps after a rumour of treasure...",
        "Lamplighter Kid: Check Six-Fingers Ottoline's Gutter Book board if you ever want to lend a hand down here!",
    ]))
    events.append(_make_npc('Ashmarch Forge-Hand', (35, 25), 'NPC 25', 'down', [
        "Forge-Hand: Ore comes down from the Sulfur Reach, gets smelted right here in the Aurel furnaces, and heads up the Long Drop to Zenith.",
        "Forge-Hand: Lately the Directorate's been putting scanner plates on every cage lift. Makes the whole pit twitchy.",
    ]))
    events.append(_make_npc('Conclave Envoy', (31, 14), 'NPC 21', 'up', [
        "Conclave Envoy: All eighteen Wardens gathered under one cavern roof for the first time in a hundred and four years.",
        "Conclave Envoy: Step through that twin-towered gatehouse if you want to see the Iron Pit — and keep your wits about you.",
    ]))
    events.append(_make_npc('Ironreach Machop', (23, 36), 'Followers/MACHOP', 'down', [
        "Machop flexes cheerfully beside the gym doorway, hoisting a length of iron rail like a feather!",
    ]))

    # Two Visible Poké Ball Pickups (hidden=False EXPLICIT!)
    events.append(_visible_item((11, 32), 'PROTEIN'))
    events.append(_visible_item((40, 22), 'ULTRABALL'))

    Lr = RC.resolve(L, TID_TOWN).astype(np.int32)
    _assert_braziers_intact(Lr, TID_TOWN, braziers_260, 'Map 260 Ironreach')

    # Verify ZERO pf_lstring & ZERO pf_glow tiles!
    lstr_tids = {int(RC.resolve(np.array([[[P1(k)]]], dtype=np.int32), TID_TOWN)[0, 0, 0]) for k in ('pf_lstring0', 'pf_lstring1', 'pf_lstring2')}
    assert not np.isin(Lr, list(lstr_tids)).any(), 'Map 260 still contains pf_lstring tiles!'

    ev_pts = [tuple(e['at']) for e in events] + [(8, 14), (4, 24), (21, 37), (33, 13), (21, 7), (1, 21)]
    PG.guard(Lr, TID_TOWN, ev_pts, 'Map 260 Ironreach')
    _verify_map_strict(
        Lr, TID_TOWN, events, start=(21, 7), label='Map 260 Ironreach',
        check_rubric=True, check_border_leaks=True
    )

    os.makedirs(RAW_DIR, exist_ok=True)
    np.save(os.path.join(RAW_DIR, '260.npy'), Lr.astype(np.int16))
    spec = {
        'id': 260,
        'name': 'Ironreach',
        'bgm': 'Cedolan City',
        'map_audio': {'bgm': 'Town - Nadir', 'bgs': 'Drip - Nadir', 'bgs_volume': 35, 'rain': False},
        'tone': [-10, -8, -4, 10],
        'metadata': {
            'Outdoor': True,
            'ShowArea': True,
            'HealingSpot': [260, 8, 14],
            'MapPosition': IRONREACH_POS,
            'BattleBack': 'city',
        },
        'biome': 'town',
        'tileset': TID_TOWN,
        'rubric': True,
        'raw': 'data/raw/260.npy',
        'events': events,
    }
    with open(os.path.join(SPEC_DIR, '260_ironreach.yaml'), 'w', encoding='utf-8') as f:
        f.write('# GENERATED by mapgen/layouts/ironreach_town.py (Batch 3G): Ironreach.\n'
                '# Edit the layout script, not this file.\n')
        f.write(yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))
    print('Wrote specs/260_ironreach.yaml and data/raw/260.npy')
    return Lr


# =================================================================================================
# Shared TS 34 Interior Helpers (Exact Certified 221 / 222 / 591 Gold Standard!)
# =================================================================================================
IRON_SLATE = [[1152, 1153, 1154], [1160, 1161, 1162], [1168, 1169, 1170]]
CREAM_STONE = [[5920, 5921, 5922], [5928, 5929, 5930], [5936, 5937, 5938]]
DARK_WOOD = [[5352, 5353, 5354], [5360, 5361, 5362], [5360, 5361, 5362]]
RED_CARPET = [[7172, 7173, 7174], [7180, 7181, 7182], [7188, 7189, 7190]]
BROWN_WOVEN_RUG = [[8620, 8621, 8622], [8628, 8629, 8630], [8636, 8637, 8638]]
POKEBALL_MEDAL_5X4 = [
    [536, 537, 538, 539, 540],
    [544, 545, 546, 547, 548],
    [552, 553, 554, 555, 556],
    [560, 561, 562, 563, 564],
]
CLINIC_WINDOW = [[2086, 2087], [2094, 2095]]
GEO_MAP = [[4730, 4731], [4738, 4739]]


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


def _seam_timber_ts34(L, floor, wall_rows=2):
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
                L[0, y, x] = 1161
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
# 2. MAP 261 — IRONREACH POKÉMON CENTER (15x11, TS 34 — Exact 221/591 Gold Standard!)
# =================================================================================================
def build_261():
    W, H = 15, 11
    L = np.zeros((3, H, W), dtype=np.int32)
    floor = np.zeros((H, W), dtype=bool)
    floor[2:9, 1:14] = True
    floor[8, 1] = False
    floor[8, 13] = False
    floor[9, 5:10] = True
    floor[10, 6:9] = True

    _seam_timber_ts34(L, floor, wall_rows=2)

    _put_9slice34(L, IRON_SLATE, 1, 2, 3, 8, z=0, mask=floor)
    _put_9slice34(L, IRON_SLATE, 11, 2, 13, 8, z=0, mask=floor)
    _put_9slice34(L, CREAM_STONE, 4, 2, 10, 8, z=0, mask=floor)
    _put_9slice34(L, CREAM_STONE, 5, 9, 9, 9, z=0, mask=floor)
    _put_9slice34(L, CREAM_STONE, 6, 10, 8, 10, z=0, mask=floor)
    _put_grid34(L, POKEBALL_MEDAL_5X4, 5, 4, z_rows=(0, 0, 0, 0))
    _put_9slice34(L, RED_CARPET, 6, 9, 8, 10, z=1)

    # North wall: warm subterranean iron wall sconces (2-tall), wooden supply shelf, vent, floor PC [11,2], Town Map [12..13,1] (ZERO blue-sky windows underground!)
    L[1, 0, 2] = 2358   # Subterranean iron air vent
    L[1, 0, 3] = 2358
    _put_tf34(L, 'shelf_low', 2, 1)
    L[1, 0, 4] = 2308; L[1, 1, 4] = 2316   # Full 2-tall amber iron wall sconce (west)
    L[1, 0, 10] = 2309; L[1, 1, 10] = 2317 # Full 2-tall amber iron wall sconce (east)
    L[2, 1, 11] = 5847
    L[1, 2, 11] = 5855
    _put_grid34(L, GEO_MAP, 12, 0, z_rows=(1, 1))

    # Symmetrical 5-wide 0x8f U-counter centered over medallion (x=5..9, y=2..3)
    L[1, 2, 5] = 5952
    L[1, 2, 9] = 5955
    for dx, t in enumerate((5960, 5961, 5962, 5961, 5963)):
        L[1, 3, 5 + dx] = t
    L[2, 1, 6] = 6035; L[2, 1, 7] = 6036
    L[1, 2, 6] = 6043; L[1, 2, 7] = 6044

    # West Wing: Warm stove, fighters' lounge sofa & Gale Post desk
    L[2, 2, 1] = 2470; L[1, 3, 1] = 2478
    _put_grid34(L, [[6024, 6026], [6032, 6034]], 2, 3, z_rows=(2, 1))
    _put_grid34(L, [[3466, 3467], [3474, 3475]], 1, 6, z_rows=(1, 1))
    L[2, 6, 1] = 3428
    L[2, 6, 2] = 4528

    # East Wing: Unobstructed Town Map above (12..13, 2), iron supply crate, medicine shelf & lamp
    _put_tf34(L, 'shelf_bottles', 12, 4)
    _put_tf34(L, 'crate_i', 12, 6)
    L[2, 7, 11] = 2271; L[1, 8, 11] = 2279
    L[1, 9, 5] = 4077
    L[1, 9, 9] = 4077
    L[1, 8, 2] = 7177

    # Programmatic 0x8f counter verification on ALL 7 U-counter tiles!
    ts34 = R.tilesets()[TID_INT]
    for cx, cy in ((5, 2), (9, 2), (5, 3), (6, 3), (7, 3), (8, 3), (9, 3)):
        t = int(L[1, cy, cx])
        assert ts34['passages'][t] == 0x8f, f'261 counter ({cx},{cy}) tile {t} pas={hex(ts34["passages"][t])} != 0x8f!'

    events = [
        {'type': 'exit', 'name': 'Exit West', 'at': [6, 10], 'link': 'IR_PC', 'arrive': [7, 10, 'up']},
        {'type': 'exit', 'name': 'Exit Center', 'at': [7, 10], 'link': 'IR_PC', 'arrive': [7, 10, 'up']},
        {'type': 'exit', 'name': 'Exit East', 'at': [8, 10], 'link': 'IR_PC', 'arrive': [7, 10, 'up']},
        {
            'type': 'event',
            'name': 'Gale Post Clerk',
            'at': [3, 6],
            'pages': [
                {
                    'graphic': {'sprite': 'NPC 14', 'dir': 'right'},
                    'trigger': 'action',
                    'commands': [
                        "Gale Post Clerk: Gale Post — Ironreach Shaft Branch! Mail sacks come down on the same winch as the ore.",
                        "Gale Post Clerk: Professor Larch dropped a sealed dispatch for you on her way off the Ashmarch:",
                        '"Ironreach: Kaito Ren keeps a straight house. If anything in the Conclave starts humming, walk away. Lecture Eleven stands. — I.L."',
                        {'selfswitch': ['A', True]},
                    ],
                },
                {
                    'cond': {'self': 'A'},
                    'graphic': {'sprite': 'NPC 14', 'dir': 'right'},
                    'trigger': 'action',
                    'commands': [
                        "Gale Post Clerk: Odessa herself slid down a courier rope into the Iron Pit earlier — refused to queue forty minutes for the cage lift!",
                    ],
                },
            ],
        },
        _make_npc('Pit Veteran', (10, 6), 'trainer_BLACKBELT', 'left', [
            "Pit Veteran: Every knockout in the Iron Pit or Kaito's Colosseum rouses the crowd — and a loud crowd makes Fighting moves hit even harder!",
            "Pit Veteran: Psychic and Flying moves cut straight over their guard, and Fairy-types don't flinch at the roar.",
        ]),
        _make_npc('Off-Duty Miner', (1, 4), 'NPC 20', 'up', [
            "Off-Duty Miner: Best iron kettle in Nadir sits right on this stove. Keeps the coal dust down after a twelve-hour shift.",
        ]),
    ]
    take_events = [
        {'template': 'pokecenter', 'name': 'Nurse', 'at': [8, 2]},
        {'template': 'pokecenter', 'name': 'Healing balls', 'at': [7, 2]},
        {'template': 'pokecenter', 'name': 'PC', 'at': [11, 2]},
        {'template': 'pokecenter', 'name': 'Town Map, size(2,1)', 'at': [12, 1]},
    ]

    ev_pts = [(6, 10), (7, 10), (8, 10), (7, 9), (8, 4), (8, 2), (7, 2), (11, 3), (11, 2), (12, 2), (13, 2), (3, 6), (10, 6), (1, 4)]
    PG.guard(L, TID_INT, ev_pts, 'Map 261')
    _verify_map_strict(L, TID_INT, events, start=(7, 9), label='Map 261 Ironreach PC', take_events=take_events, exit_row=10)

    os.makedirs(RAW_DIR, exist_ok=True)
    np.save(os.path.join(RAW_DIR, '261.npy'), L.astype(np.int16))
    spec = {
        'id': 261,
        'name': 'Ironreach Pokémon Center',
        'parent': 260,
        'bgm': 'Poke Center',
        'map_audio': {'bgs': ''},
        'tone': [-4, -4, -2, 6],
        'metadata': {
            'ShowArea': False,
            'HealingSpot': IRONREACH_HEAL_SPOT,
            'MapPosition': IRONREACH_POS,
        },
        'biome': 'interior',
        'palette': 'interior',
        'tileset': TID_INT,
        'map': '\n'.join(['.' * W] * H) + '\n',
        'tiles': _tiles_list_34(L),
        'events': events,
        'take_events': take_events,
    }
    with open(os.path.join(SPEC_DIR, '261_ironreach_pc.yaml'), 'w', encoding='utf-8') as f:
        f.write('# GENERATED by mapgen/layouts/ironreach_town.py (Batch 3G): Ironreach Pokémon Center.\n'
                '# Edit the layout script, not this file.\n')
        f.write(yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))
    print('Wrote specs/261_ironreach_pc.yaml and data/raw/261.npy')
    return L


# =================================================================================================
# 3. MAP 262 — IRONREACH MART (12x10, TS 34 — Exact 222/202 Gold Standard!)
# =================================================================================================
def build_262():
    W, H = 12, 10
    L = np.zeros((3, H, W), dtype=np.int32)
    floor = np.zeros((H, W), dtype=bool)
    floor[2:9, 1:11] = True
    floor[8, 1] = False
    floor[8, 10] = False
    floor[9, 5:7] = True

    _seam_timber_ts34(L, floor, wall_rows=2)
    _put_9slice34(L, IRON_SLATE, 1, 2, 10, 8, z=0, mask=floor)
    _put_9slice34(L, IRON_SLATE, 5, 9, 6, 9, z=0, mask=floor)
    _put_9slice34(L, DARK_WOOD, 4, 2, 9, 7, z=0, mask=floor)
    _put_9slice34(L, BROWN_WOVEN_RUG, 4, 4, 6, 7, z=1, mask=floor)
    # Complete, un-sliced 2x2 crimson doormat across (5..6, 8..9)!
    L[1, 8, 5] = 7172; L[1, 8, 6] = 7174
    L[1, 9, 5] = 7188; L[1, 9, 6] = 7190

    # North wall: warm subterranean iron sconces, iron vent & display shelf + regional map (ZERO blue-sky windows!)
    L[1, 0, 1] = 2358; L[1, 1, 1] = 2318
    L[1, 0, 2] = 2308; L[1, 1, 2] = 2316   # Full 2-tall amber iron wall sconce (west)
    L[1, 0, 4] = 2358; L[1, 0, 5] = 2358   # Subterranean ventilation grates
    _put_tf34(L, 'shelf_low', 4, 1)        # Warm supply wall shelf
    L[1, 0, 6] = 2309; L[1, 1, 6] = 2317   # Full 2-tall amber iron wall sconce (east)
    _put_grid34(L, GEO_MAP, 7, 0, z_rows=(1, 1))

    # Flush 5-tile 0x8f Mart Counter wrapping Clerk at (2, 3)!
    L[1, 2, 3] = 5971
    L[1, 3, 3] = 5971
    L[1, 4, 1] = 5962
    L[1, 4, 2] = 5961
    L[1, 4, 3] = 5963
    ts34 = R.tilesets()[TID_INT]
    for cx, cy in ((3, 2), (3, 3), (1, 4), (2, 4), (3, 4)):
        t = int(L[1, cy, cx])
        assert ts34['passages'][t] == 0x8f, f'262 counter ({cx},{cy}) tile {t} pas={hex(ts34["passages"][t])} != 0x8f!'

    # Stocked shelves, iron supply crates & warm lamp
    _put_tf34(L, 'shelf_goods', 9, 2)
    _put_tf34(L, 'shelf_bottles', 1, 5)
    _put_tf34(L, 'crate_i', 8, 5)
    L[1, 7, 1] = 4101
    L[1, 7, 2] = 7177
    L[1, 7, 10] = 7178
    L[2, 7, 9] = 2271
    L[1, 8, 9] = 2279

    events = [
        {'type': 'exit', 'name': 'Exit West', 'at': [5, 9], 'link': 'IR_MART', 'arrive': [5, 9, 'up']},
        {'type': 'exit', 'name': 'Exit East', 'at': [6, 9], 'link': 'IR_MART', 'arrive': [5, 9, 'up']},
        {
            'type': 'mart',
            'name': 'Mart Clerk',
            'at': [2, 3],
            'sprite': 'NPC 19',
            'dir': 'right',
            'greeting': 'Mart Clerk: Welcome to Ironreach Mart! Hyper Potions, Dusk Balls, and Revives — stocked heavy for the Ironreach Open!',
            'items': [
                'POKEBALL', 'GREATBALL', 'ULTRABALL', 'DUSKBALL', 'TIMERBALL',
                'SUPERPOTION', 'HYPERPOTION', 'MAXPOTION', 'FULLHEAL', 'REVIVE',
                'ESCAPEROPE', 'SUPERREPEL',
            ],
        },
        _make_npc('Pit Challenger', (7, 6), 'NPC 18', 'right', [
            "Pit Challenger: Stocking up on Max Potions before I sign Nell's bracket board up at the Iron Pit!",
            "Pit Challenger: The Pit Announcer called me 'sensible and boring' when I walked in here. Man's got eyes everywhere.",
        ]),
    ]

    ev_pts = [(5, 9), (6, 9), (5, 8), (4, 3), (2, 3), (7, 6)]
    PG.guard(L, TID_INT, ev_pts, 'Map 262')
    _verify_map_strict(L, TID_INT, events, start=(5, 8), label='Map 262 Ironreach Mart', exit_row=9)

    os.makedirs(RAW_DIR, exist_ok=True)
    np.save(os.path.join(RAW_DIR, '262.npy'), L.astype(np.int16))
    spec = {
        'id': 262,
        'name': 'Ironreach Mart',
        'parent': 260,
        'bgm': 'Poke Mart',
        'map_audio': {'bgs': ''},
        'tone': [-4, -4, -2, 6],
        'metadata': {
            'MapPosition': IRONREACH_POS,
        },
        'biome': 'interior',
        'tileset': TID_INT,
        'raw': 'data/raw/262.npy',
        'events': events,
    }
    with open(os.path.join(SPEC_DIR, '262_ironreach_mart.yaml'), 'w', encoding='utf-8') as f:
        f.write('# GENERATED by mapgen/layouts/ironreach_town.py (Batch 3G): Ironreach Mart.\n'
                '# Edit the layout script, not this file.\n')
        f.write(yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))
    print('Wrote specs/262_ironreach_mart.yaml and data/raw/262.npy')
    return L


# =================================================================================================
# 4. MAP 263 — THE IRON PIT (41x33, TS 57 PF Rejuv Cave, :COLOSSEUM, Conclave + Ironreach Open!)
# =================================================================================================
def build_263():
    W, H = 41, 33
    for base_k, new_k in (('cvL', 'cvL2'), ('qy', 'qy2'), ('cvT', 'cvT2'), ('cvE', 'cvE2')):
        K.KITS[new_k] = dict(K.KITS[base_k], rows=[K.KITS[base_k]['rows'][0], K.KITS[base_k]['rows'][2]])

    m = Cave(W, H, 'L', seed=263, pool='Cave Pool', tid=TID_PIT)
    m.STAIRS = (P1('st_stair_l'), P1('st_stair_m'), P1('st_stair_r'))
    # Cohesive warm subterranean rock outer walls (cvE2) + dark cut ironstone amphitheater tiers (qy2) — ZERO icy glacier!
    m.kit = {TER: 'qy2', FLOOR: 'qy2', MASS: 'cvE2', 'default': 'qy2'}

    # Carve dramatic octagonal amphitheater bowl + south entrance corridor
    m.box(2, 1, 38, 30, FLOOR, '.')
    m.box(19, 30, 21, 32, FLOOR, '.')
    # Octagonal cavern wall bevels
    bevels = [
        (2, 1), (3, 1), (4, 1), (2, 2), (3, 2), (2, 3),
        (36, 1), (37, 1), (38, 1), (37, 2), (38, 2), (38, 3),
        (2, 29), (2, 30), (3, 30), (38, 29), (38, 30), (37, 30),
    ]
    m.mass_at(bevels)

    # Elevated North Conclave High Dais (10..30, 4..7) with central stone stairs (19..21, 8..9)
    m.box(10, 4, 30, 7, TER, '.')
    # Elevated West & East Spectator Bleacher Galleries (2..6, 10..25 & 34..38, 10..25) with south stone staircases!
    m.box(2, 10, 6, 25, TER, '.')
    m.box(34, 10, 38, 25, TER, '.')
    m.tidy()
    m.plan_cliffs(rows=2)
    m.stairs(19, 8, w=3, n=2, kit_rows=2, kind='stone')
    m.stairs(4, 26, w=3, n=2, kit_rows=2, kind='stone')
    m.stairs(34, 26, w=3, n=2, kit_rows=2, kind='stone')

    m.paint()
    L = m.L

    # Palette tiles (resolved on TS 57)
    EARTH = [P1('E_f%d' % i) for i in range(4)]
    SLATE = [P1('L_f%d' % i) for i in range(4)]
    FLAG = [P1('T_f%d' % i) for i in range(4)]
    IRON_DECK = [P1('Q_f%d' % i) for i in range(4)]
    RAIL_W, RAIL_M, RAIL_E = P1('qy_rail_w'), P1('qy_rail_m'), P1('qy_rail_e')

    def _fill_l0(x0, y0, x1, y1, pal):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                L[0, y, x] = pal[(x * 7 + y * 11) % len(pal)]

    # Distinct architectural floor zones:
    # - North Conclave Dais: polished dark ironstone slate
    _fill_l0(10, 4, 30, 7, SLATE)
    # - West & East Spectator Galleries: cut quarry flagstones
    _fill_l0(2, 10, 6, 25, FLAG)
    _fill_l0(34, 10, 38, 25, FLAG)
    # - Pit Apron Ring (11..29, 11..26): riveted iron colosseum catwalk
    _fill_l0(11, 11, 29, 26, IRON_DECK)
    # - Central Fighting Pit Sand (13..27, 13..24): packed red-ochre earth
    _fill_l0(13, 13, 27, 24, EARTH)
    # - South Entrance Runner (19..21, 27..32): dark ironstone slate
    _fill_l0(19, 27, 21, 32, SLATE)

    # Crimson Conclave Dais Runner (19..21, 5..7) & South Entrance Carpet (19..21, 28..32)
    for ry in (5, 6, 7):
        L[1, ry, 19] = 24146
        L[1, ry, 20] = 24152 if ry == 6 else 24147
        L[1, ry, 21] = 24148
    for ry in range(28, 33):
        L[1, ry, 19] = 24146
        L[1, ry, 20] = 24147
        L[1, ry, 21] = 24148

    # Iconic White Chalk Fighting Ring (16..24, 16..21) + 3x3 Chalk Pokéball Center Circle (19..21, 17..19) (100% pas=0x0!)
    L[1, 16, 16] = 9667; L[1, 16, 24] = 9669
    L[1, 21, 16] = 9683; L[1, 21, 24] = 9685
    for rx in range(17, 24):
        L[1, 16, rx] = 9668
        L[1, 21, rx] = 9684
    for ry in range(17, 21):
        L[1, ry, 16] = 9675
        L[1, ry, 24] = 9677
    L[1, 17, 19], L[1, 17, 20], L[1, 17, 21] = 9656, 9657, 9658
    L[1, 18, 19], L[1, 18, 20], L[1, 18, 21] = 9664, 9665, 9666
    L[1, 19, 19], L[1, 19, 20], L[1, 19, 21] = 9672, 9673, 9674

    # Riveted Iron Pit Railings framing north & south approaches to the fighting pit (open 5-wide central entries x=18..22!)
    for ry in (12, 25):
        for x0, x1 in ((13, 17), (23, 27)):
            for x in range(x0, x1 + 1):
                L[1, ry, x] = RAIL_W if x == x0 else (RAIL_E if x == x1 else RAIL_M)

    # North Conclave High Dais: 11 Warden Plate Banners along y=2..4!
    dais_banners = [
        (10, 2, 'wr_ban_ash'), (12, 2, 'wr_ban_ise'), (14, 2, 'wr_ban_bone'),
        (16, 2, 'hb_banner'), (18, 2, 'lm_banner'), (20, 2, 'wr_ban_ash'),
        (22, 2, 'wr_ban_ise'), (24, 2, 'wr_ban_bone'), (26, 2, 'hb_banner'),
        (28, 2, 'lm_banner'), (30, 2, 'wr_ban_ash'),
    ]
    for bx, by, bname in dais_banners:
        _stamp_raw(L, bname, bx, by, tid=TID_PIT, protect_top=True)

    # Canonical Conclave Long Table on North Dais (split cleanly around central carpet 19..21: west 14..17,5 & east 23..26,5!)
    # Uses lm_bar tiles (25978 left, 25979 mid, 25980 right — pas=0xf!)
    L[1, 5, 14], L[1, 5, 15], L[1, 5, 16], L[1, 5, 17] = 25978, 25979, 25979, 25980
    L[1, 5, 23], L[1, 5, 24], L[1, 5, 25], L[1, 5, 26] = 25978, 25979, 25979, 25980

    # Twin Conclave Dais Plaques separated cleanly on far west (11,5) & far east (29,5) ends of the dais!
    _stamp_raw(L, 'mn_plinth', 11, 5, tid=TID_PIT)
    _stamp_raw(L, 'mn_plinth', 29, 5, tid=TID_PIT)

    # Dedicated NE East Gallery Top-Tier Meditation Perch for MEDICHAMITE (solitary plinth (35,11) + woven mat (34..35,12)!)
    _stamp_raw(L, 'mn_plinth', 35, 11, tid=TID_PIT)
    _stamp_raw(L, 'mn_mat', 34, 12, tid=TID_PIT)

    # 8 Intact Blazing Iron Braziers (dais corners, 4 pit corners, south entrance flanks — ZERO detached pf_glow!)
    braziers_263 = [
        (13, 4), (27, 4),
        (11, 11), (29, 11),
        (11, 25), (29, 25),
        (17, 29), (23, 29),
    ]
    for bx, by in braziers_263:
        _stamp_raw(L, 'fw_brazier', bx, by, tid=TID_PIT)

    # Dark Mining Timber-and-Iron Support Posts (cv_post: top p=0,pr=1 walkable overhead; base p=f,pr=0 solid — ZERO Greek marble!)
    for px, py in ((9, 13), (31, 13), (9, 22), (31, 22)):
        _stamp_raw(L, 'cv_post', px, py, tid=TID_PIT, protect_top=True)

    # Gallery Lanterns, Wooden Bleacher Benches & Foyer Pit Equipment
    for lx, ly in ((10, 7), (30, 7), (3, 24), (37, 24)):
        _stamp_raw(L, 'cv_lamp_on', lx, ly, tid=TID_PIT, protect_top=True)
    for by in (12, 14, 18, 20, 22, 24):
        _stamp_raw(L, 'pf_logbench', 2, by, tid=TID_PIT)
        if by != 12:
            _stamp_raw(L, 'pf_logbench', 37, by, tid=TID_PIT)
    _stamp_raw(L, 'pf_signpost', 15, 26, tid=TID_PIT)   # Base (15, 27) solid -> Open Bracket Slate!
    _stamp_raw(L, 'hb_boxes', 12, 27, tid=TID_PIT)
    _stamp_raw(L, 'hb_barrels', 27, 27, tid=TID_PIT)
    _stamp_raw(L, 'wr_rack', 10, 28, tid=TID_PIT)
    _stamp_raw(L, 'wr_rack', 30, 28, tid=TID_PIT)
    _stamp_raw(L, 'wr_sandbags', 26, 29, tid=TID_PIT)

    # Two Whole, Unclipped Overhead Cavern Light Shafts (cv_shaft 2x3 on L[2] — 100% intact over open center ring & south approach!)
    _stamp_raw(L, 'cv_shaft', 19, 17, tid=TID_PIT)
    _stamp_raw(L, 'cv_shaft', 19, 25, tid=TID_PIT)

    # ---- Events: Full-Width Exit, 3 Canonical Open Trainers, Nell Heal, Garret Cameo, Postgame Kaito, MEDICHAMITE & 2 Items ----
    events = []
    for ex in (19, 20, 21):
        events.append({
            'type': 'warp',
            'name': f'Exit Iron Pit {ex}',
            'at': [ex, 32],
            'to': {'map': 260, 'x': 33, 'y': 13, 'dir': 'down'},
            'se': 'Door exit',
        })

    # ALL 3 Canonical PBS Trainers with 100% OPEN sight: 3 cones across the fighting pit!
    events.append(_trainer(
        (14, 23), 'BLACKBELT', 'Dunmore', 'right',
        "Pit Brawler Dunmore: Round One of the Ironreach Open! My Machoke and I are both wearing shorts — that's psychological!",
        "Pit Brawler Dunmore: ...I'm going to need a shirt. Head east across the pit for Round Two!",
        sight=3, field='COLOSSEUM',
    ))
    events.append(_trainer(
        (26, 23), 'CRUSHGIRL', 'Ysa', 'left',
        "Crush Girl Ysa: Gran's watching from the east gallery! If I lose, I've got to do the washing for a month!",
        "Crush Girl Ysa: GRAN! I did my BEST! ...She's saying 'the washing'. I can't hear her up there, but I know.",
        sight=3, field='COLOSSEUM',
    ))
    events.append(_trainer(
        (20, 15), 'BLACKBELT', 'Gristle', 'down',
        "Old Gristle: I fought Valen Corrigan in this very Pit when he was nineteen. He cried when he won. Don't you cry!",
        "Old Gristle: You didn't cry. That's worse. You've got real grit — go test it against Kaito down in the Gym!",
        sight=3, field='COLOSSEUM',
    ))

    # Nell the Chalk-Girl (free between-round Pit heal!)
    nell_ruby = '\n'.join([
        'pbMessage(_INTL("Nell the Chalk-Girl: I\'m Nell! I do the Open bracket board — neatest S in Ironreach, and I\'ll fight anyone who says I haven\'t!"))',
        'pbMessage(_INTL("Nell the Chalk-Girl: Here, take a breather by my chalk crate — every Ironreach Open entrant gets patched up between bouts!"))',
        'pbSEPlay("Anim/HealBell", 85, 100)',
        '$player.heal_party',
        'pbMessage(_INTL("Your party was restored to full fighting shape!"))',
    ])
    events.append({
        'type': 'event',
        'name': 'Nell the Chalk-Girl',
        'at': [16, 28],
        'pages': [{
            'graphic': {'sprite': 'NPC 06', 'dir': 'right'},
            'trigger': 'action',
            'move': 'fixed',
            'commands': [{'script': nell_ruby}],
        }],
    })

    events.append(_make_npc('Pit Announcer', (25, 28), 'NPC 15', 'left', [
        "Pit Announcer (megaphone echoing off the cavern ceiling): WELCOME TO THE IRON PIT, FOLKS! MINED OUT IN THE AUREL ERA, PACKED RED WITH HONEST SAND!",
        "Pit Announcer: EIGHTEEN BANNERS ON THE NORTH DAIS FOR THE CONCLAVE, AND THREE IRONREACH OPEN STANDOUTS WAITING RIGHT INSIDE THE RAILS!",
    ]))
    events.append(_make_npc('Stranger', (35, 21), 'NPC 24', 'left', [
        "Stranger: ...You. Seen a girl, about this tall? Brown hair. Name's Eden.",
        "Stranger: Never mind. Nobody down here has. Good crowd in the Pit, though — my Lucario hasn't stopped staring at Kaito's.",
    ]))
    events.append(_make_npc("Stranger's Lucario", (35, 22), 'Followers/LUCARIO', 'left', [
        "The foreign trainer's Lucario studies the fighting pit with quiet, unblinking intensity.",
    ]))
    events.append(_make_npc("Ysa's Gran", (35, 16), 'NPC 11', 'left', [
        "Ysa's Gran: Keep your guard up, Ysa! If you drop your left shoulder one more time you're scrubbing shirts till winter!",
    ]))
    events.append(_make_npc('Pit Historian', (5, 16), 'NPC 22', 'right', [
        "Pit Historian: Eighteen banners hang on the north wall tonight — one for every Warden's Plate in Velmora.",
        "Pit Historian: Ironreach hasn't hosted a full Conclave in a hundred and four years. Feels like the cavern roof's holding its breath.",
    ]))
    events.append(_make_npc('Conclave Clerk', (15, 6), 'NPC 21', 'down', [
        "Conclave Clerk: Chancellor Hollis has called the roll of all eighteen Wardens — sixteen at the long table behind me, two watching from the galleries, as tradition permits.",
        "Conclave Clerk: Even Warden Kaito gave his full address to the assembly: 'Here.' Shortest speech in Conclave records.",
    ]))
    events.append(_make_npc('Accord Observer', (25, 6), 'NPC 25', 'down', [
        "Accord Observer: Down in the shafts nobody cares for fancy speeches — only whether you can stand your ground inside the chalk.",
    ]))

    # Post-Game Kaito Registry Hook (:PG_KAITO_PIT)
    kaito_pg_ruby = '''if (pf_trial_ready?(:PG_KAITO_PIT) rescue false)
  pf_trial_talk(:PG_KAITO_PIT)
else
  pbMessage(_INTL("Kaito: The Pit stays open. Five rounds, no breaks, honest sand. Come back when the Registry calls your name."))
end'''
    events.append({
        'type': 'event',
        'name': 'Kaito (the Pit)',
        'at': [20, 6],
        'pages': [
            {'trigger': 'action', 'through': True, 'commands': []},
            {
                'cond': {'switch': 'POSTGAME'},
                'graphic': {'sprite': 'KAITO', 'dir': 'down'},
                'trigger': 'action',
                'move': 'fixed',
                'commands': [{'script': kaito_pg_ruby}],
            },
        ],
    })

    # Solitary NE East Gallery Top-Tier Meditation Shelf Plinth (MEDICHAMITE — self-switch guarded cleanly inside if pf_mega_stone!)
    medichamite_ruby = '''if ($player && $player.badge_count >= 16 && !$bag.has?(:MEDICHAMITE)) && !$game_self_switches[[263, @event_id, "A"]] && defined?(pf_mega_stone)
  if pf_mega_stone(:MEDICHAMITE, "Someone has left a stone on a folded mat, as if mid-breath.")
    $game_self_switches[[263, @event_id, "A"]] = true
  end
else
  pbMessage(_INTL("A quiet stone meditation shelf above the Pit's top tier. A folded training mat lies directly before it — Kaito's pre-bout perch."))
end'''
    events.append({
        'type': 'event',
        'name': 'Meditation Shelf Plinth',
        'at': [35, 11],
        'pages': [{
            'trigger': 'action',
            'commands': [{'script': medichamite_ruby}],
        }],
    })

    events.append(_sign(
        'Open Bracket Slate', (15, 27),
        "IRONREACH OPEN — CHALK BRACKET BOARD (in Nell's neatest hand): Round 1: Dunmore · Round 2: Ysa · Semifinal: Old Gristle · Final: Kestrel Vane (TEAM COMPOST — crossed out twice and rewritten neatly)."
    ))
    events.append(_sign(
        'Conclave Dais Plaque West', (11, 5),
        "THE CONCLAVE OF AF 300 — 'Eighteen Plates, eighteen Wardens, one hole in the ground.' Inscribed in iron beside the Conclave long table's west rail."
    ))
    events.append(_sign(
        'Conclave Dais Plaque East', (29, 5),
        "CHRONICLE OF THE IRON PIT — 'Carved by Aurel iron-miners, kept by Nadir pit-fighters. Sovereign Valen Corrigan fought the Open here at nineteen.'"
    ))

    # Two Visible Poké Ball Pickups (hidden=False EXPLICIT!)
    events.append(_visible_item((4, 11), 'MUSCLEBAND'))
    events.append(_visible_item((36, 14), 'MAXPOTION'))

    Lr = RC.resolve(L, TID_PIT).astype(np.int32)
    _assert_braziers_intact(Lr, TID_PIT, braziers_263, 'Map 263 The Iron Pit')
    ev_pts = [tuple(e['at']) for e in events] + [(20, 31), (35, 12)]
    PG.guard(Lr, TID_PIT, ev_pts, 'Map 263 The Iron Pit')
    _verify_map_strict(Lr, TID_PIT, events, start=(20, 31), label='Map 263 The Iron Pit', exit_row=32)

    os.makedirs(RAW_DIR, exist_ok=True)
    np.save(os.path.join(RAW_DIR, '263.npy'), Lr.astype(np.int16))
    spec = {
        'id': 263,
        'name': 'The Iron Pit',
        'parent': 260,
        'bgm': 'Cave',
        'field': 'COLOSSEUM',
        'map_audio': {'bgm': 'Route - Nadir', 'bgs': 'Drip - Nadir', 'bgs_volume': 30, 'rain': False},
        'tone': [-6, -8, -4, 8],
        'metadata': {
            'Name': 'The Iron Pit',
            'SnapEdges': True,
            'MapPosition': IRONREACH_POS,
            'BattleBack': 'indoor3',
        },
        'biome': 'interior',
        'tileset': TID_PIT,
        'raw': 'data/raw/263.npy',
        'events': events,
    }
    with open(os.path.join(SPEC_DIR, '263_the_iron_pit.yaml'), 'w', encoding='utf-8') as f:
        f.write('# GENERATED by mapgen/layouts/ironreach_town.py (Batch 3G): The Iron Pit.\n'
                '# Edit the layout script, not this file.\n')
        f.write(yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))
    print('Wrote specs/263_the_iron_pit.yaml and data/raw/263.npy')
    return Lr


if __name__ == '__main__':
    build_260()
    build_261()
    build_262()
    build_263()
    print('ALL IRONREACH TOWN MAPS (260, 261, 262, 263) GENERATED & VERIFIED!')
