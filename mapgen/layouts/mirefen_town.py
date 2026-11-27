#!/usr/bin/env python3
"""layouts/mirefen_town.py — Batch 3C: Mirefen Core & Corvin Mott's Infirmary (4 Maps: 220, 221, 222, 223):
  - 220 Mirefen                     (44x40, TS 58 PF Rejuv Locks, Outdoor, :CORROSIVE_MIRE, rubric: true)
      Atmospheric mist-drenched Nadir boardwalk-and-apothecary swamp town tucked under Zenith's Gutterfall cliff:
      * North Escarpment Cliff + roaring Gutterfall waterfall cascade + Gutterfall Lift Cage (guarded -> 633)
      * Elevated Goldenleaf weathered-timber stilt buildings linked by lantern-lit wooden boardwalks over dark
        Surfable/Fishable Corrosive Mire runoff (PF Sea Cave tag=7 + PF Lock Water deep sumps):
          - NW Stilt Deck: Mirefen Pokémon Center (gl_pc -> MF_PC -> 221, HealingSpot [220, 8, 16]) + Sweetrot
            Offer 3 Vendor (Prismfall.checkpoint / GO_SWEET_TOOTH) + Mother Gutter's barge moored beside the deck
          - W-Central Island: Mirefen Mart (gl_mart -> MF_MART -> 222) + Noodle Cart (lm_noodles) & Cook + Child w/
            Alolan Grimer "Gloop"
          - Central Boardwalk Hub: Apothecary Cottage + Hollow Ring & Folk-Saint Ogre graffiti + Gutter Book
            chalk board (live pf_trial_board(:NADIR)) + optional street rival Riot Punk Zara (PUNK_ZARA, badges >= 6)
          - NE High-Stilt Terrace: Corvin Mott's Infirmary (gl_hall -> MF_INFIRMARY -> 223) + grey harbour crane
          - Central-East Tower: Mirefen Gym (gl_gym -> MF_GYM -> 230)
          - South Lower Walkway: The Sweet Market (3 stalls, Sweetrot Vendor Offer 1/2, Singing Child, Mirefen Woman)
          - SW Ferry Steps & Crossing: Marsh Ferryman (live pf_trial_talk(:FERRYMAN_MIREFEN) + post-Gym-6 HM03 Surf),
            3 Ferry Lamps (live pf_trial_talk(:FERRY_LAMP)), Lamplighter's Hut & Noct + Umbreon (pf_trial_talk(:OCTAVE_NOCT))
          - Guarded in-world exits to unbuilt adjacent maps: North Lift -> 633 The Gutterfall, East Causeway -> 640
            Leechman's Walk, South Pier -> 648 The Weeping Fen (ZERO meta-text!)
  - 221 Mirefen Pokémon Center      (15x11, TS 34 Prismfall Interior — Exact 591 Brassfall PC Gold Standard!)
      Symmetrical 5-wide warm-timber 0x8f U-counter centered over Pokéball medallion, NPC 16 ONLY on Nurse Joy,
      ZERO green scoreboard, ZERO 444 stripe, Gale Post desk, Nadir/swamp slate wings & apothecary decor.
  - 222 Mirefen Mart                (12x10, TS 34 Prismfall Interior — Exact 202 Duneholt Mart Gold Standard!)
      Flush 5-tile 0x8f counter, ZERO green chalkboard, ZERO sliced props or aisle-blocking lamps, canonical Ch7
      PBS items + green apothecary medicine shelves & herb drying rack.
  - 223 Corvin Mott's Infirmary     (25x19, TS 34 Prismfall Interior — Front Ward, Dispensary & Quiet Ward!)
      Three distinct clinical zones on dark weathered timber walls:
      * South Front Ward: patient cots, woodstove, Matron the Audino (free ward heal), Wenlow (pf_trial_talk(:WENLOW_INFIRMARY)),
        Gutter Book board (pf_trial_board(:NADIR)), Cragholm short-wave radio
      * East Dispensary: complete green-bottle shelves, 3x3 closed mahogany bookcase, compounding bench, Corvin's
        medicine ledger, Juno alphabetising the AF 296 ledgers
      * North Quiet Ward (partitioned sterile cream-and-sage sanctuary): 6 complete beds incl. Ama by the window,
        Mister Garrod, Old Fen, Tull twins (3 post-game WARD_BED hooks for NA_BEDSIDE_MANNER), Warden Corvin Mott
        (pf_trial_talk(:CORVIN_INFIRMARY) + Ch7 Quiet Ward canon).

Run:
    /usr/bin/python3 -I mapgen/layouts/mirefen_town.py
"""
import os
import sys
import random
from collections import deque
import numpy as np
import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import rkit as K
from rkit import STAMPS, P1
import rcompose as RC
import render as R
import passguard as PG
import craftkit as CK
from terrain import vnoise, NB2AUTO
from interiorkit import TF

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(HERE, 'data', 'raw')
SPEC_DIR = os.path.join(HERE, 'specs')

TID_MIRE = 58       # PF Rejuv Locks: PF Sea Cave (slot 2, tag=7 toxic mire!), PF Lock Water (slot 0), RJ Waterfall!
TID_INT = 34        # Prismfall Interior
VOID34 = 5437
MIREFEN_POS = [0, 20, 13]
MIREFEN_HEAL_SPOT = [220, 8, 16]    # Walkable stilt porch tile directly south of gl_pc door (8,15)


# =================================================================================================
# Shared Verification & Event Helpers (Anti-P0 Enforced Programmatically!)
# =================================================================================================
def _guarded_unbuilt_transfer(map_id, tx, ty, direction, blocked_text, step_back=None):
    """Guarded exit to an unbuilt map without emitting a raw RMXP code-201 command (0 build warnings)."""
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
    else_cmds = [blocked_text]
    if step_back:
        mv_const = {
            'down': 'PBMoveRoute::DOWN',
            'up': 'PBMoveRoute::UP',
            'left': 'PBMoveRoute::LEFT',
            'right': 'PBMoveRoute::RIGHT',
        }[step_back]
        else_cmds.append({'script': f'pbMoveRoute($game_player, [{mv_const}], true)'})
    return [{
        'if': 'pbRgssExists?("Data/Map%03d.rxdata")' % map_id,
        'then': [{'script': ruby}],
        'else': else_cmds,
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
    """Stamp overhead light/glow (pf_glow / cv_shaft) strictly onto unoccupied L[2] cells — NEVER deletes lanterns/flames!"""
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


def _event_footprint(e):
    """Return all occupied tiles for an event (supporting Essentials size(w,h) anchored bottom-left)."""
    import re
    ax, ay = int(e['at'][0]), int(e['at'][1])
    nm = e.get('name') or ''
    m = re.search(r'size\((\d+),(\d+)\)', nm, re.I)
    if not m:
        return [(ax, ay)]
    w, h = int(m.group(1)), int(m.group(2))
    return [(ax + dx, ay - dy) for dx in range(w) for dy in range(h)]


def _verify_map_strict(Lr, tid, events, start, label, check_rubric=False, take_events=None):
    """Strict verification suite enforcing:
      - 0 void L[0] tiles, 0 OOB tile IDs, 0 passguard hits
      - 0 over_trigger? == true traps (every tile of every trigger:action without a blocking sprite MUST be solid!)
      - 100% 4-bit directional BFS reachability of EVERY event (incl. 0x80 counter-talk and size(w,h)!)
      - Optional Outdoor Rubric PASS (all 6 build.py strict metrics!)
    """
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

    # Anti-P0 #1: ZERO over_trigger? == true traps (including ALL tiles of size(w,h) events)!
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
            if trig == 'action' and not has_solid_gfx:
                for fx, fy in fp:
                    if B.cell_passable(Lr, ts, fx, fy):
                        over_traps.append((e.get('name'), (fx, fy), 'action event with no solid graphic on passable tile'))
    assert not over_traps, f'{label}: over_trigger? traps detected: {over_traps}'

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
                # Essentials 0x80 counter-talk across 1 tile!
                for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                    mx, my = at[0] + dx, at[1] + dy
                    px, py = at[0] + 2 * dx, at[1] + 2 * dy
                    if 0 <= mx < W and 0 <= my < H and (px, py) in seen:
                        if any((int(Lr[z, my, mx]) > 0 and (ts['passages'][int(Lr[z, my, mx])] & 0x80)) for z in (0, 1, 2)):
                            reach = True
                            break
        if not reach:
            missing.append((e.get('name') or et, at, bool(B.cell_passable(Lr, ts, at[0], at[1]))))
    assert not missing, f'{label}: unreachable events: {missing}'

    if check_rubric:
        rub = B.rubric(Lr)
        print(f'{label} RUBRIC:', {k: round(v, 1) for k, v in rub.items()})
        assert rub['layer2'] >= 55.0, f'{label}: rubric layer2 {rub["layer2"]:.1f} < 55'
        assert rub['layer3'] >= 20.0, f'{label}: rubric layer3 {rub["layer3"]:.1f} < 20'
        assert rub['bare'] <= 35.0, f'{label}: rubric bare {rub["bare"]:.1f} > 35'
        assert rub['bare3x3'] <= 13.0, f'{label}: rubric bare3x3 {rub["bare3x3"]:.1f} > 13'
        assert rub['stacks'] >= 10.0, f'{label}: rubric stacks {rub["stacks"]:.1f} < 10'
        assert rub['mirror'] <= 15.0, f'{label}: rubric mirror {rub["mirror"]:.1f} > 15'

    print(f'{label}: PASS (BFS={len(seen)} cells, {len(events)} events, 0 over_trigger, 0 passguard)')
    return seen


# =================================================================================================
# 1. MAP 220 — MIREFEN (44x40, TS 58 PF Rejuv Locks, Outdoor, :CORROSIVE_MIRE, rubric: true)
# =================================================================================================
def _stamp_raw(L, name, x, y, tid=TID_MIRE, taken=None, protect_top=False):
    """Stamp a resolved rkit stamp into raw layer array L without clobbering existing lower layers on 0 tiles."""
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


def _stamp_bldg_220(L, name, x, y, taken, door_link=None, door_name=None, plaque=None, max_w=None, patch_fn=None):
    """Stamp a Goldenleaf / Sheridan timber building cleanly over Mirefen marshland/islands.
    Preserves existing mud/water under transparent cells, supports trimming/patching (e.g., cow-skull removal,
    mart plank-strip trim), and preserves visible L[2] door tiles when placing a solid plaque blocker.
    """
    st = STAMPS[name]
    sL = RC.resolve(np.array(st['layers'], dtype=np.int32), TID_MIRE).copy()
    if max_w is not None:
        sL = sL[:, :, :max_w]
    if patch_fn is not None:
        patch_fn(sL)
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
            # Preserve any visible L[2] door graphic (e.g. gl_shed tile 3094) by moving it to L[1] before placing blocker!
            if int(L[2, dy, dx]) != 0:
                L[1, dy, dx] = int(L[2, dy, dx])
            blk = PG.blocker(R.tilesets()[TID_MIRE])
            if blk is not None:
                L[2, dy, dx] = blk
            return _sign(door_name or (name + ' plaque'), (dx, dy), plaque), (dx, dy)
    return None, None


def build_220():
    W, H = 44, 40
    L = np.zeros((3, H, W), dtype=np.int32)
    taken = np.zeros((H, W), dtype=bool)
    keep_clear = set()

    # TS 58 Autotile bases:
    #   slot 2 (144): PF Sea Cave (unified dark emerald-teal Corrosive Mire water, pas=0xf, tag=7 Surfable & Fishable!)
    #   slot 3 (192): RJ Waterfall (pas=0xf, tag=8)
    #   slot 4 (240): RJ Waterfall crest (pas=0xf, tag=9)
    #   slot 5 (288): RJ Waterfall bottom foam (pas=0xf, tag=7)
    AUTO_MIRE = 144
    AUTO_WF = 192
    AUTO_WF_CREST = 240
    AUTO_WF_BOT = 288

    MUD = [P1('cv_mud%d' % i) for i in range(4)]
    STONE_DARK = [P1('L_f%d' % i) for i in range(4)]
    QUAY_STONE = [P1('T_f%d' % i) for i in range(4)]
    DECK_WOOD = [P1('N_f%d' % i) for i in range(4)]
    BW_H = P1('bw_h')
    BW_V = P1('bw_v')
    RAIL_W, RAIL_M, RAIL_E = P1('qy_rail_w'), P1('qy_rail_m'), P1('qy_rail_e')

    # ---- 1. Sculpt Wet Marsh Islands (Mud Hummocks Framed cleanly inside the Mire) ----
    island = np.zeros((H, W), dtype=bool)
    island_rects = [
        (2, 5, 13, 18),       # NW Island: Mirefen Pokémon Center (gl_pc)
        (18, 9, 24, 15),      # N-Central Hummock: Apothecary Cottage & Ogre Graffiti Wall
        (27, 5, 42, 16),      # NE High-Stilt Terrace: Corvin Mott's Infirmary (gl_ell + crane)
        (4, 22, 14, 28),      # W-Central Island: Mirefen Mart + Noodle Cart
        (29, 20, 43, 39),     # East & SE Marsh Peninsula: Mirefen Gym (sh_big) + dry eastern woods (ZERO canal clipping!)
        (2, 30, 7, 36),       # SW Lamplighter's Hummock: gl_shed + Noct
        (0, 5, 2, 19),        # West Marsh Fringe (trees & reeds)
        (0, 27, 1, 39),       # SW Marsh Fringe (trees)
        (2, 36, 6, 39),       # SW corner dry tree islet
        (25, 5, 27, 8),       # Small northern stepping islet
    ]
    for x0, y0, x1, y1 in island_rects:
        island[max(5, y0):min(H, y1 + 1), max(0, x0):min(W, x1 + 1)] = True
    # Carve natural south-east mire bay south of the Gym forecourt (y=36..39, x=26..36) for lush marsh water framing!
    island[36:40, 26:37] = False
    # Carve organic mire cove east of the east boardwalk spur (x=29..30, y=20..21)
    island[20:22, 29:30] = False

    # ---- 2. Seamless Weathered Timber Stilt Decks & Narrow Plank Boardwalks ----
    boardwalk = np.zeros((H, W), dtype=bool)

    def _paint_deck(x0, y0, x1, y1):
        """Seamless multi-tile weathered dark timber stilt deck (N_f0..3 layered on L[0] & L[1], zero seams!)."""
        for yy in range(max(5, y0), min(H, y1 + 1)):
            for xx in range(max(0, x0), min(W, x1 + 1)):
                boardwalk[yy, xx] = True
                L[0, yy, xx] = DECK_WOOD[(xx * 3 + yy * 5) % 4]
                L[1, yy, xx] = DECK_WOOD[(xx * 3 + yy * 5 + 1) % 4]

    def _paint_bw(x0, y0, x1, y1, horiz=True):
        """Narrow 1-2 tile stilt plank bridge over mire water (bw_h / bw_v, 100% passguard clean!)."""
        t = BW_H if horiz else BW_V
        for yy in range(max(5, y0), min(H, y1 + 1)):
            for xx in range(max(0, x0), min(W, x1 + 1)):
                boardwalk[yy, xx] = True
                if not island[yy, xx]:
                    L[1, yy, xx] = t
                else:
                    L[0, yy, xx] = t

    # ---- 3. Unified Single-Layer Dark Mire Water on L[0] with Crisp Autotiled Shore Banks (ZERO dual-layer cutouts!) ----
    water_mask = np.zeros((H, W), dtype=bool)
    for y in range(5, H):
        for x in range(W):
            if not island[y, x]:
                water_mask[y, x] = True
    for y in range(5, H):
        for x in range(W):
            if water_mask[y, x]:
                sh = NB2AUTO[CK.nbits(water_mask, x, y)]
                L[0, y, x] = AUTO_MIRE + sh
            else:
                L[0, y, x] = MUD[(x * 5 + y * 3) % 4]
                if 27 <= x <= 41 and 14 <= y <= 16:
                    L[0, y, x] = QUAY_STONE[(x + y) % 4]
                elif 18 <= x <= 24 and 13 <= y <= 15:
                    L[0, y, x] = STONE_DARK[(x * 3 + y) % 4]
                elif 30 <= x <= 39 and 31 <= y <= 33:
                    L[0, y, x] = STONE_DARK[(x * 3 + y) % 4]

    # Seamless multi-tile stilt plazas & wide decks (rich dark-timber planks!)
    _paint_deck(14, 5, 17, 19)      # North Gutterfall Lift Pier
    _paint_deck(4, 18, 17, 20)      # PC Forecourt Deck
    _paint_deck(4, 20, 6, 21)       # Mother Gutter Jetty & Overlook Spur (flush beside barge at x=1..3, y=20..21!)
    _paint_deck(20, 16, 21, 16)     # Direct 2-Wide Apothecary Cottage Bridge across y=16!
    _paint_deck(15, 17, 29, 22)     # Central Boardwalk Hub & Graffiti Square
    _paint_deck(28, 16, 43, 18)     # Infirmary Approach & East Avenue to Leechman's Walk
    _paint_deck(14, 20, 16, 30)     # West Market Vertical Walk
    _paint_deck(5, 27, 16, 29)      # Mart & Noodle Plaza
    _paint_deck(15, 28, 28, 35)     # South-Central Sweet Market Deck
    _paint_deck(28, 33, 39, 35)     # East Gym Forecourt & Southern Link (directly below sh_big stairs!)
    _paint_deck(6, 33, 15, 36)      # SW Ferry Steps & Night-Ferry Plaza
    # Crisp 2-wide narrow plank stilt bridges over open marsh channels!
    _paint_bw(20, 35, 22, 39, horiz=False)     # South Weeping Fen Pier
    _paint_bw(8, 29, 9, 33, horiz=False)       # West Mart -> Ferry Steps bridge
    _paint_bw(27, 22, 28, 26, horiz=False)     # Marsh Stump Poison Barb bridge

    # ---- 4. North Escarpment Cliff (Zenith's Overhang, y=0..4) with Staggered Buttresses, Pipes & Moss! ----
    kitL = K.KITS['cvL']
    l_mass = [P1('L_m0a'), P1('L_m0b'), P1('L_m1a'), P1('L_m1b')]
    for y in range(0, 3):
        for x in range(W):
            L[0, y, x] = l_mass[(x * 3 + y * 5) % len(l_mass)]
            taken[y, x] = True
    lip_m = kitL['rows'][0][1]
    face_m = kitL['rows'][1][1]
    base_m = kitL['rows'][2][1]
    for x in range(W):
        L[1, 2, x] = lip_m
        L[0, 3, x] = face_m
        L[0, 4, x] = base_m
        taken[3, x] = True
        taken[4, x] = True
    # Break up straight horizontal dam silhouette with staggered stone buttresses, drainage vents, hanging moss & piers!
    for bx in (2, 7, 11, 25, 31, 37, 42):
        _stamp_raw(L, 'nr_col', bx, 2, taken=taken)
    for vx in (4, 9, 27, 34, 39):
        L[1, 4, vx] = P1('lm_vent')
    for mx in range(W):
        if (mx * 3) % 5 != 0 and int(L[1, 0, mx]) == 0:
            L[1, 0, mx] = P1('rw_ivy0' if mx % 2 == 0 else 'rw_ivy1')
        if (mx * 7 + 1) % 4 != 0 and int(L[1, 1, mx]) == 0:
            L[1, 1, mx] = P1('rw_ivy1' if mx % 2 == 0 else 'rw_ivy0')
    for mx in (1, 5, 8, 12, 13, 23, 24, 28, 30, 35, 38, 40, 41):
        if int(L[2, 3, mx]) == 0:
            L[2, 3, mx] = P1('rw_ivy0' if mx % 2 == 0 else 'rw_ivy1')
        if int(L[2, 4, mx]) == 0 and mx % 3 != 0:
            L[2, 4, mx] = P1('cs_kelp0' if mx % 2 == 0 else 'cs_kelp1')

    # Roaring Gutterfall Cascade pouring cleanly out of a recessed dark stone culvert at y=2..6 + Splash Foam at y=7!
    for wx in (19, 20, 21):
        L[0, 2, wx] = AUTO_WF_CREST
        L[1, 2, wx] = 0
        L[0, 3, wx] = AUTO_WF
        L[0, 4, wx] = AUTO_WF
        L[0, 5, wx] = AUTO_WF
        L[0, 6, wx] = AUTO_WF_BOT
        # Animated white waterfall splash / churning foam seamlessly blending into dark mire at y=7!
        L[1, 7, wx] = P1('cv_race0' if wx == 20 else 'cv_race1')
        L[2, 7, wx] = P1('hb_glint0' if wx == 20 else 'hb_glint2')
        for wy in range(2, 8):
            taken[wy, wx] = True
    # Stone culvert abutments & mist flanking the waterfall
    L[1, 2, 18] = kitL['rows'][0][2]
    L[1, 2, 22] = kitL['rows'][0][0]
    _stamp_raw(L, 'lm_steam0', 18, 6, taken=None, protect_top=True)
    _stamp_raw(L, 'lm_steam1', 22, 6, taken=None, protect_top=True)

    # ---- 5. Stamp All Distinct Iconic Mirefen Buildings (ZERO Cow Skulls, ZERO Clipped Roofs!) ----
    E = []
    _stamp_raw(L, 'lm_lift', 15, 2, taken=taken)

    # 5a. Mirefen Pokémon Center (gl_pc 12x14 at (2,5) -> door (8,15) MF_PC; cow skull patched cleanly to timber!)
    def _patch_gl_pc(sL):
        sL[1, 8, 5] = 3369
        sL[1, 8, 6] = 3369
        sL[1, 8, 7] = 3369
        sL[1, 9, 6] = 3227

    ev_pc, _ = _stamp_bldg_220(
        L, 'gl_pc', 2, 5, taken,
        door_link='MF_PC', door_name='Mirefen Pokémon Center', patch_fn=_patch_gl_pc,
    )
    E.append(ev_pc)
    # Keep taken=True across the entire PC porch so ZERO weeds ever stamp onto floorboards!

    # 5b. Apothecary Cottage (gl_flat1 6x6 at (18,9) -> door (21,13); direct 2-wide bridge across (20..21,16)!)
    ev_cot, _ = _stamp_bldg_220(
        L, 'gl_flat1', 18, 9, taken,
        door_name='Apothecary Cottage',
        plaque="A timber stilt-cottage smelling of boiled wormwood and carbolic soap. A tin sign on the latch reads: 'OUT GATHERING LEECHES — BACK AT BELLS.'",
    )
    E.append(ev_cot)

    # 5c. Corvin Mott's Infirmary (gl_ell 10x10 at (29,5) -> door (31,11) MF_INFIRMARY! Distinct L-clinic, ZERO roof clip, ZERO skull!)
    ev_inf, _ = _stamp_bldg_220(
        L, 'gl_ell', 29, 5, taken,
        door_link='MF_INFIRMARY', door_name="Corvin Mott's Infirmary",
    )
    E.append(ev_inf)

    # 5d. Mirefen Mart (gl_mart trimmed to 6x6 at (4,22) -> door (6,26) MF_MART; ZERO orphaned right plank strip!)
    ev_mart, _ = _stamp_bldg_220(
        L, 'gl_mart', 4, 22, taken,
        door_link='MF_MART', door_name='Mirefen Mart', max_w=6,
    )
    E.append(ev_mart)

    # 5e. Mirefen Gym (sh_big 11x12 at (29,21) -> door (37,29) MF_GYM! Distinct dark-timber stilt tower, ZERO roof clip, ZERO skull!)
    def _patch_sh_big(sL):
        # Strip un-keyed bright flower/bush tiles at bottom-left & along row 11 stilts for moody swamp harmony
        sL[0, 10, 1] = 0
        sL[0, 11, 1] = 0
        for cx in range(sL.shape[2]):
            if int(sL[1, 11, cx]) in (4941, 4939, 4933):
                sL[1, 11, cx] = 0

    ev_gym, _ = _stamp_bldg_220(
        L, 'sh_big', 29, 21, taken,
        door_link='MF_GYM', door_name='Mirefen Gym', patch_fn=_patch_sh_big,
    )
    E.append(ev_gym)
    # Give sh_big's left twin doorway (32, 29) a solid apothecary service-door plaque (0 over_trigger!)
    blk_mire = PG.blocker(R.tilesets()[TID_MIRE])
    if blk_mire is not None:
        if int(L[2, 29, 32]) != 0:
            L[1, 29, 32] = int(L[2, 29, 32])
        L[2, 29, 32] = blk_mire
    E.append(_sign(
        'Mirefen Gym Service Door', (32, 29),
        "MIREFEN GYM — APOTHECARY SERVICE DOOR. 'Reagent deliveries only. Gym challengers please use the main east stairs!'",
    ))

    # 5f. Old Lamplighter's Hut (gl_shed 4x6 at (2,30) -> real wooden door 3094 preserved at (3,34)!)
    ev_hut, _ = _stamp_bldg_220(
        L, 'gl_shed', 2, 30, taken,
        door_name="Lamplighter's Hut",
        plaque="The old lamplighter's hut at the end of the ferry steps. Through the parted timber door, four small children are fast asleep under a patched boat-sail.",
    )
    E.append(ev_hut)

    # ---- 6. Iconic Landmarks, Weathered Ogre Graffiti Wall, Market Stalls, Noodle Cart, Boats, Cranes & Signs ----
    _stamp_raw(L, 'hb_crane', 40, 6, taken=taken)
    _stamp_raw(L, 'lm_noodles', 12, 24, taken=taken)
    # Weathered timber Ogre Graffiti Wall at (24, 13..14) — solid palisade + chalked mark (ZERO lm_ring lamp!)
    L[1, 13, 24] = P1('wr_pal_h')
    L[1, 14, 24] = P1('wr_pal_h')
    L[2, 14, 24] = P1('cv_chalkx')
    taken[13, 24] = taken[14, 24] = True
    _stamp_raw(L, 'lm_stall_a', 16, 29, taken=taken)
    _stamp_raw(L, 'lm_stall_b', 20, 29, taken=taken)
    _stamp_raw(L, 'lm_stall_c', 24, 29, taken=taken)
    _stamp_raw(L, 'hb_boat2', 1, 20, taken=taken)
    _stamp_raw(L, 'hb_boat1', 8, 37, taken=taken)
    # Two solid apothecary vats/barrels holding HiddenItems cleanly OFF walkway pinch points (pas=0xf -> 0 over_trigger!)
    _stamp_raw(L, 'pf_p_vat_r', 28, 14, taken=taken)   # Tucked neatly beside Infirmary west garden fence!
    _stamp_raw(L, 'hb_barrels', 26, 17, taken=taken)

    # Solid wooden signposts (pf_signpost 1x2 -> solid pas=0xf base at y+1 -> ZERO over_trigger? traps!)
    signposts = [
        (15, 18),   # Town Sign base at (15, 19)
        (18, 17),   # Gutter Book Chalk Board base at (18, 18)
        (29, 14),   # Infirmary Sign base at (29, 15) — right beside Infirmary courtyard entrance!
    ]
    for sx, sy in signposts:
        _stamp_raw(L, 'pf_signpost', sx, sy, taken=taken)

    # Three Night-Ferry Lamps (pf_lantern 1x3 -> solid pas=0xf base at y+2 -> live pf_trial_talk(:FERRY_LAMP)!)
    ferry_lamps = [
        ('Ferry lamp 1', (7, 31)),    # base (7, 33)
        ('Ferry lamp 2', (11, 31)),   # base (11, 33)
        ('Ferry lamp 3', (14, 34)),   # base (14, 36)
    ]
    for _, (lx, ly) in ferry_lamps:
        _stamp_raw(L, 'pf_lantern', lx, ly, taken=taken)

    # ---- 7. All Canonical Events, Trials, NPCs, Zara Street Rival, Guarded Exits & Pickups ----
    # 7a. Guarded Exits to Unbuilt Adjacent Maps (UPPERCASE PBMoveRoute::DOWN/LEFT/UP + waitComplete=true!)
    for gx in (15, 16):
        E.append({
            'type': 'event',
            'name': f'Gutterfall Lift {gx}',
            'at': [gx, 5],
            'pages': [{
                'trigger': 'touch',
                'commands': _guarded_unbuilt_transfer(
                    633, 40, 90, 'up',
                    "Lift-keeper: Counterweight's jammed by Zenith's outfall surge! Wait till the sump-crews clear the Gutterfall cables before riding back up the cliff.",
                    step_back='down',
                ),
            }],
        })
    for gy in (16, 17, 18):
        E.append({
            'type': 'event',
            'name': f'East Causeway {gy}',
            'at': [43, gy],
            'pages': [{
                'trigger': 'touch',
                'commands': _guarded_unbuilt_transfer(
                    640, 2, 36, 'right',
                    "Causeway Watch: Leechman's Walk east toward Lake Sallow is thick with sulfur marsh gas right now. Check in at Corvin's Infirmary and earn your Remedy Badge before heading out across the causeway.",
                    step_back='left',
                ),
            }],
        })
    for gx in (20, 21, 22):
        E.append({
            'type': 'event',
            'name': f'South Weeping Fen Pier {gx}',
            'at': [gx, 39],
            'pages': [{
                'trigger': 'touch',
                'commands': _guarded_unbuilt_transfer(
                    648, 20, 2, 'down',
                    "Marsh Watch: Past these reeds lies the Weeping Fen, where rain falls upward out of the Bleed pools. Even the ferrymen won't pole into the Fen without Doctor Mott's word.",
                    step_back='up',
                ),
            }],
        })

    # 7b. Interactive Signs & Gutter Book Chalk Board (ALL on verified solid pas=0xf bases!)
    E += [
        _sign('Mirefen Town Sign', (15, 19),
              "MIREFEN — Nadir's Apothecary Marsh. ↑ The Gutterfall Lift · ↗ Corvin Mott's Infirmary · → Leechman's Walk & Mirefen Gym · ↓ Sweet Market & Ferry Steps."),
        _sign('Infirmary Sign', (29, 15),
              "CORVIN MOTT'S INFIRMARY — Front Ward · Dispensary · The Quiet Ward. 'Please wipe your boots. The mire stays outside.'"),
        # Mounted directly on sh_big's built-in ornate black signboard at (39, 32) (solid pas=0xf!)
        _sign('Mirefen Gym Sign', (39, 32),
              "MIREFEN GYM — Warden Corvin Mott (Poison · Corrosive Mire). 'Everything's poison, dear. Dose makes the cure.'"),
        _sign('Ogre Graffiti Wall', (24, 14),
              "Painted fresh on the weathered timber palisade: a grey ring broken at the top beside an Ogre's sad, masked face. Chalked underneath: 'HE TALKED. HE DIDN'T STEAL.'"),
        {
            'type': 'event',
            'name': 'Gutter Book Chalk Board',
            'at': [18, 18],
            'pages': [{
                'trigger': 'action',
                'commands': [{
                    'if': 'defined?(pf_trial_board)',
                    'then': [{'script': 'pf_trial_board(:NADIR)'}],
                    'else': ["THE GUTTER BOOK — Six-Fingers Ottoline's Nadir Trial Board. Jobs chalked cleanly in white slate."],
                }],
            }],
        },
    ]

    # 7c. Night-Ferry Lamps (3 solid pf_lantern bases -> live pf_trial_talk(:FERRY_LAMP)!)
    for lname, (lx, ly) in ferry_lamps:
        E.append({
            'type': 'event',
            'name': lname,
            'at': [lx, ly + 2],
            'pages': [{
                'trigger': 'action',
                'commands': [{
                    'if': '(pf_trial_ready?(:FERRY_LAMP) rescue false)',
                    'then': [{'script': 'pf_trial_talk(:FERRY_LAMP)'}],
                    'else': ["An oil-burning ferry lamp hanging over the dark runoff marsh. Its amber flame throws faint blue halos across the water."],
                }],
            }],
        })

    # 7d. Marsh Ferryman — HM03 Surf checked FIRST (never blocked by optional trial!), proper post-Surf dialogue!
    ferryman_ruby = '''if (pfm_gym_won?(:LEADER_CORVIN) rescue false) && !$game_self_switches[[220, @event_id, "B"]]
  pbMessage(_INTL("Ferryman: Remedy Badge! Well I'll be — the Doctor signed off on you."))
  pbMessage(_INTL("Ferryman: Surf's yours, then. Take this old ferrymen's manual — Lake Sallow's east, past Leechman's Walk."))
  if pbReceiveItem(:HM03)
    $game_self_switches[[220, @event_id, "B"]] = true
    pbMessage(_INTL("Ferryman: Mind the sulfur. Mind the dragons up in Ashkaar. Mind everything."))
  end
elsif (pf_trial_ready?(:FERRYMAN_MIREFEN) rescue false)
  pf_trial_talk(:FERRYMAN_MIREFEN)
elsif $game_self_switches[[220, @event_id, "B"]]
  pbMessage(_INTL("Ferryman: Your team's got the knack for Surf now — Lake Sallow's east past Leechman's Walk. Mind the sulfur, friend."))
  if defined?(pf_trial_board) && pbConfirmMessage(_INTL("Want a look at the Gutter Book chalk board while you're by the steps?"))
    pf_trial_board(:NADIR)
  end
else
  pbMessage(_INTL("Ferryman: Poles and flat-bottom skiffs only out here, friend. Once you earn Doctor Mott's Remedy Badge, come back and I'll teach your team how to Surf the runoff."))
  if defined?(pf_trial_board) && pbConfirmMessage(_INTL("Want a look at the Gutter Book chalk board while you're by the steps?"))
    pf_trial_board(:NADIR)
  end
end'''
    E.append({
        'type': 'event',
        'name': 'Marsh Ferryman',
        'at': [10, 35],
        'pages': [{
            'graphic': {'sprite': 'trainer_SAILOR', 'dir': 'down'},
            'trigger': 'action',
            'move': 'fixed',
            'commands': [{'script': ferryman_ruby}],
        }],
    })

    # 7e. Noct of the Octave & Wick the Umbreon (live pf_trial_talk(:OCTAVE_NOCT)!)
    noct_ruby = '''if (pf_trial_ready?(:OCTAVE_NOCT) rescue false)
  pf_trial_talk(:OCTAVE_NOCT)
else
  pbMessage(_INTL("Noct: ...Shh. Keep your voice low by the hut. Four kids are sleeping under that sail."))
  pbMessage(_INTL("Noct: Dark's the only thing down here in Nadir that nobody charges a tax on."))
end'''
    E.append({
        'type': 'event',
        'name': 'Noct',
        'at': [6, 35],
        'pages': [{
            'graphic': {'sprite': 'NPC 24', 'dir': 'right'},
            'trigger': 'action',
            'move': 'fixed',
            'commands': [{'script': noct_ruby}],
        }],
    })
    E.append(_make_npc('Wick the Umbreon', (7, 35), 'Followers/UMBREON', 'down', [
        "Umbreon's golden rings pulse softly in the marsh mist, keeping watch over the lamplighter's hut.",
    ]))

    # 7f. Riot Punk Zara (Optional Ch7 Nadir Street Rival — canonical [PUNK_ZARA, Zara], badges >= 6, :CORROSIVE_MIRE!)
    zara_ruby = '''if $game_self_switches[[220, @event_id, "A"]]
  pbMessage(_INTL("Zara: Still got paint under my nails and sparks in my boots. Next time we throw down, it's gonna shake the whole Undercity!"))
elsif (Prismfall.badge_count >= 6 rescue false)
  pbMessage(_INTL("Zara: Yo! You're the trainer who took down Doctor Mott on his own turf, yeah? Riot Punk Zara — best muralist below the plateau!"))
  if pbConfirmMessage(_INTL("Zara: Wanna test that Remedy Badge against my crew right here on the stilt-walks?"))
    pbMessage(_INTL("Zara: That's what I'm talking about! Stencil, Voltage — crank it up!"))
    setBattleRule("field", :CORROSIVE_MIRE) if defined?(FieldEffects)
    if TrainerBattle.start(:PUNK_ZARA, "Zara")
      pbMessage(_INTL("Zara: Whoa — alright, null-kid, you've got serious bite! Here, take this spare Black Sludge for the road."))
      pbReceiveItem(:BLACKSLUDGE)
      $game_self_switches[[220, @event_id, "A"]] = true
    end
  else
    pbMessage(_INTL("Zara: No sweat. I'll be right here touching up the Ogre mural when you want a real scrap!"))
  end
else
  pbMessage(_INTL("Zara: Riot Punk Zara, tagging Zenith's dirty laundry one boardwalk at a time!"))
  pbMessage(_INTL("Zara: Go grab Corvin's Remedy Badge first — then come back here and I'll give you a real Nadir street battle!"))
end'''
    E.append({
        'type': 'event',
        'name': 'Riot Punk Zara',
        'at': [22, 19],
        'pages': [{
            'graphic': {'sprite': 'ZARA', 'dir': 'down'},
            'trigger': 'action',
            'move': 'fixed',
            'commands': [{'script': zara_ruby}],
        }],
    })

    # 7g. Sweetrot Market Vendor (Offer 1 & Offer 2 ONLY; at V128 >= 2 redirects cleanly to Center Steps vendor!)
    sweet_market_ruby = '''if $game_variables[128].to_i == 0
  pbMessage(_INTL("Sweet Vendor: Sweetrot! Try one. Soft as mochi, sweet as summer peaches. First one's free, sweetling."))
  if pbConfirmMessage(_INTL("Take a pastel Sweetrot?"))
    $game_variables[128] = 1
    pbSEPlay("Sweet Scent", 85, 100)
    pbMessage(_INTL("It's soft and cool and tastes of peaches, and for a second everything is fine. Everything is so fine. You'd agree with anyone about anything."))
    pbMessage(_INTL("The feeling goes. You want another one. You don't know why."))
  else
    pbMessage(_INTL("Sweet Vendor: Next time. There's always a next time, down here."))
  end
elsif $game_variables[128].to_i == 1
  pbMessage(_INTL("Sweet Vendor: You look like you've had a day, sweetling. Another Sweetrot? Half price, just for you."))
  if pbConfirmMessage(_INTL("Take a second Sweetrot?"))
    $game_variables[128] = 2
    pbSEPlay("Sweet Scent", 85, 100)
    pbMessage(_INTL("Peaches. Everything is fine. The marsh is fine. You'd agree with anyone."))
    pbMessage(_INTL("It fades. You want another one even more than the last."))
    pbMessage(_INTL("Wenlow (calling from the Infirmary walk above): NO! No no no — please, that's two! Don't take a third one!"))
  else
    pbMessage(_INTL("Sweet Vendor: (smiling the exact same smile) Next time's the charm, sweetling."))
  end
else
  pbMessage(_INTL("Sweet Vendor: (smiling the exact same smile) My sister by the Pokémon Center steps saved the pink one just for you, sweetling."))
end'''
    E.append({
        'type': 'event',
        'name': 'Sweetrot Vendor',
        'at': [21, 31],
        'pages': [{
            'graphic': {'sprite': 'NPC 21', 'dir': 'down'},
            'trigger': 'action',
            'move': 'fixed',
            'commands': [{'script': sweet_market_ruby}],
        }],
    })

    # 7h. Sweetrot Offer 3 Vendor outside Pokémon Center (Prismfall.checkpoint ONLY when V128 >= 2 before fatal 3rd!)
    sweet_pc_ruby = '''pbMessage(_INTL("Sweet Vendor: I saved you the best one, sweetling. The pink. Nobody else gets the pink."))
if $game_variables[128].to_i >= 2
  Prismfall.checkpoint if defined?(Prismfall) && Prismfall.respond_to?(:checkpoint)
  if pbConfirmMessage(_INTL("Take the pink Sweetrot?"))
    if pbConfirmMessage(_INTL("...Really? Wenlow begged you not to take a third one."))
      $game_variables[128] = $game_variables[128].to_i + 1
      pbSEPlay("Sweet Scent", 90, 90)
      pbMessage(_INTL("Peaches. And then nothing is ever wrong again, and you never wonder why again, and you are so very happy, for the rest of your life."))
      if defined?(Prismfall) && Prismfall.respond_to?(:game_over)
        Prismfall.game_over(:GO_SWEET_TOOTH)
      end
    else
      pbMessage(_INTL("Sweet Vendor: Mother Gutter will be so disappointed."))
    end
  else
    pbMessage(_INTL("Sweet Vendor: Mother Gutter will be so disappointed."))
  end
else
  if pbConfirmMessage(_INTL("Take the pink Sweetrot?"))
    $game_variables[128] = $game_variables[128].to_i + 1
    pbSEPlay("Sweet Scent", 85, 100)
    pbMessage(_INTL("Peaches. For a heartbeat, everything in Velmora feels soft and fine. Then it vanishes, leaving a strange ache for more."))
    if $game_variables[128].to_i >= 2
      pbMessage(_INTL("Wenlow (calling from the Infirmary walk above): NO! No no no — please, that's two! Don't take a third one!"))
    end
  else
    pbMessage(_INTL("Sweet Vendor: Mother Gutter is patient. Peaches are patient."))
  end
end'''
    E.append({
        'type': 'event',
        'name': 'Sweet Vendor (Center Steps)',
        'at': [10, 17],
        'pages': [{
            'graphic': {'sprite': 'NPC 23', 'dir': 'left'},
            'trigger': 'action',
            'move': 'fixed',
            'commands': [{'script': sweet_pc_ruby}],
        }],
    })

    # 7i. Mother Gutter standing solidly on the wooden barge-jetty at (4, 20) flush beside her moored barge (1..3, 20..21)!
    E.append(_make_npc('Mother Gutter', (4, 20), 'GUTTER', 'right', [
        "Mother Gutter: Oh, don't mind an old woman by her barge, dear. Just listening to the drips and watching the peaches ripen.",
        "Mother Gutter: My Muk's asleep in the hull — step light on the planks. Peaches are patient, and so am I.",
    ]))

    # 7j. Canonical Ch7 Mirefen Townsfolk
    E += [
        _make_npc('Lift-keeper', (14, 7), 'NPC 19', 'right', [
            "Lift-keeper: Down's a copper. Up's a silver. Don't ask why. Everybody asks why.",
            "Lift-keeper: Welcome to Nadir. Mind the drips off Zenith's pipes — and don't buy cheap rebreathers. The cheap ones are just masks.",
        ]),
        _make_npc('Noodle-cart Cook', (13, 26), 'NPC 18', 'down', [
            "Noodle-cart Cook: Slag-fried noodles! You're new. You look it. Sit.",
            "Noodle-cart Cook: I rate everyone out of ten. Nobody's scored over four. Doctor Mott's a solid two.",
            "Noodle-cart Cook: Boy in a black coat came through two days back — three out of ten. Ate like he was angry at the bowl. Asked about masks.",
        ]),
        _make_npc('Child with Grimer', (11, 28), 'NPC 03', 'right', [
            "Child: Don't be scared of Gloop! Gloop eats the bad bits out of the runoff.",
            "Child: That's his job. He's very good at his job!",
        ]),
        _make_npc('Gloop the Grimer', (12, 28), 'Followers/GRIMER_1', 'left', [
            "Gloop burbles happily, its colorful crystalline teeth clinking as it gobbles a clump of glowing mire-sludge!",
        ]),
        _make_npc('Singing Child', (17, 32), 'NPC 02', 'right', [
            "Child: ♪ One for the sweet and two for the tongue, the peach that keeps you, keeps you young... ♪",
            "Child: Doctor Mott gets mad when we sing that one near the Infirmary!",
        ]),
        _make_npc('Mirefen Woman', (25, 32), 'NPC 12', 'left', [
            "Mirefen Woman: People up top in Lumen think we're dirty.",
            "Mirefen Woman: We're the cleanest people in Velmora. We have to be. Everything else isn't.",
        ]),
        _make_npc('Infirmary Runner', (27, 17), 'NPC 17', 'down', [
            "Runner: Corvin's Infirmary is up in the timber courtyard right ahead — and the Gym's the dark-timber stilt tower south of the walkway.",
            "Runner: If you hear someone dropping a tray inside, don't panic. That's just Wenlow.",
        ]),
        # Visible & Hidden Mirefen Pickups (verified PBS items; HiddenItems anchored on solid props OFF pinch walkways!)
        {'type': 'item', 'name': 'Item Poison Barb', 'at': [28, 26], 'item': 'POISONBARB'},
        {'type': 'item', 'name': 'HiddenItem', 'at': [28, 14], 'item': 'BIGMUSHROOM', 'hidden': True},
        {'type': 'item', 'name': 'HiddenItem', 'at': [26, 18], 'item': 'ANTIDOTE', 'hidden': True},
    ]

    # Protect all event coordinates and their cardinal neighbors
    for e in E:
        ex, ey = e['at']
        keep_clear.add((ex, ey))
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            if 0 <= ex + dx < W and 0 <= ey + dy < H:
                keep_clear.add((ex + dx, ey + dy))
    # Keep boardwalk main thoroughfares, Apothecary bridge, Infirmary courtyard & Gym stairs 100% open!
    for y in range(5, 20):
        keep_clear.add((15, y)); keep_clear.add((16, y))
    for x in range(5, 30):
        for y in (18, 19, 20):
            keep_clear.add((x, y))
    for x in (20, 21):
        for y in range(13, 18):
            keep_clear.add((x, y))
    for x in (30, 31, 32):
        for y in range(11, 18):
            keep_clear.add((x, y))
    for x in range(28, 44):
        for y in (16, 17, 18):
            keep_clear.add((x, y))
    for y in range(20, 36):
        keep_clear.add((15, y))
    for x in range(6, 40):
        keep_clear.add((x, 34))
        keep_clear.add((x, 35))
    for x in range(6, 16):
        keep_clear.add((x, 28))
    for y in range(28, 36):
        keep_clear.add((8, y)); keep_clear.add((9, y))
    for y in range(34, 40):
        keep_clear.add((21, y))
    for x in (32, 36, 37, 38):
        for y in range(29, 36):
            keep_clear.add((x, y))
    for x in (7, 8, 9):
        for y in (15, 16, 17, 18, 19):
            keep_clear.add((x, y))
    keep_clear.add((27, 23)); keep_clear.add((27, 24)); keep_clear.add((27, 25)); keep_clear.add((28, 25))
    keep_clear.add((4, 21)); keep_clear.add((5, 21)); keep_clear.add((5, 20))

    # ---- 8. Boardwalk Pilings, Quay Rails, Apothecary Vats, Dry-Land Washlines & Swamp Atmosphere! ----
    rail_spans = [
        ((18, 22), (26, 22), 'h'),
        ((17, 35), (19, 35), 'h'),
        ((23, 35), (27, 35), 'h'),
    ]
    for (x0, y0), (x1, y1), orient in rail_spans:
        if orient == 'h':
            for xx in range(x0, x1 + 1):
                if (xx, y0) not in keep_clear and not taken[y0, xx]:
                    rt = RAIL_W if xx == x0 else (RAIL_E if xx == x1 else RAIL_M)
                    L[1, y0, xx] = rt
                    taken[y0, xx] = True

    # Stilt pilings framing boardwalk corners & pier edges (strictly over water, clear of waterfall mouth!)
    for px, py in ((13, 6), (13, 11), (27, 19), (14, 37), (19, 36), (23, 36), (36, 37)):
        if 0 <= px < W - 1 and 0 <= py < H - 1 and not taken[py, px] and not boardwalk[py, px] and not island[py, px]:
            _stamp_raw(L, 'hb_posts2' if (px + py) % 2 == 0 else 'hb_posts3', px, py, taken=taken)

    # Tall glowing marsh lanterns along main boardwalks (strictly off keep_clear & doorways!)
    lamp_pts = [
        (17, 6), (13, 17), (25, 16), (34, 15), (38, 15), (41, 15),
        (16, 23), (28, 28), (15, 31), (28, 31), (35, 33), (5, 25), (1, 34),
    ]
    for lx, ly in lamp_pts:
        base = (lx, ly + 2)
        if 0 <= lx < W and 0 <= ly and ly + 2 < H and base not in keep_clear and not taken[ly + 2, lx]:
            _stamp_raw(L, 'pf_lantern' if (lx + ly) % 2 == 0 else 'pf_wlamp', lx, ly, taken=taken, protect_top=True)

    # Overhead festoon lantern strings over Sweet Market, Central Hub, Mart Plaza & East Avenue (L[2] overhead, walkable below!)
    for sx, sy in (
        (17, 28), (19, 28), (21, 28), (23, 28), (25, 28), (27, 28),
        (17, 18), (19, 18), (22, 18), (25, 18), (29, 17), (32, 17), (35, 17), (38, 17), (41, 17),
        (7, 28), (10, 28), (13, 28), (29, 34), (31, 34), (34, 34), (37, 34),
        (6, 19), (9, 19), (12, 19), (15, 10), (16, 14),
    ):
        if int(L[2, sy, sx]) == 0:
            L[2, sy, sx] = P1('pf_lstring0' if (sx + sy) % 2 == 0 else 'pf_lstring1')

    # Apothecary dye/herb vats, barrels, crates & DRY-LAND washlines (ZERO washlines spanning water or clipping banks!)
    prop_placements = [
        ('pf_p_vat_b', 28, 15), ('pf_p_vat_y', 39, 14), ('pf_p_vat_b', 33, 15),
        ('hb_barrels', 10, 25), ('hb_barrels', 27, 12), ('hb_barrels', 29, 31),
        ('hb_crates4', 39, 12), ('hb_washline', 10, 22),
        ('lm_bench', 23, 17), ('lm_bench', 24, 20), ('lm_bench', 23, 33),
        ('lm_vent', 16, 14), ('lm_vent', 26, 14),
        ('lm_junk0', 10, 23), ('lm_junk1', 1, 32),
    ]
    for nm, px, py in prop_placements:
        st = STAMPS[nm]
        pw, ph = st['w'], st['h']
        if px + pw <= W and py + ph <= H:
            cells = [(px + dx, py + dy) for dy in range(ph) for dx in range(pw)]
            if not any(c in keep_clear or taken[c[1], c[0]] for c in cells):
                _stamp_raw(L, nm, px, py, taken=taken, protect_top=True)

    # ---- 9. Lush Swamp Canopies (Strictly on DRY Land!), Transparent Lilies, Moss & Steam! ----
    # Every tree trunk base sits strictly on dry mud (island == True, ZERO trees clipping water!)
    tree_spots = [
        # West & SW swamp canopy
        ('nt_teal_a', 0, 5), ('nt_deadtree', 0, 10), ('nt_tree_purp', 0, 14),
        ('nt_teal_a', 0, 26), ('nt_deadtree', 0, 34), ('nt_teal_a', 2, 36), ('nt_tree_purp', 4, 36),
        # North escarpment overhang & canyon moss trees
        ('nt_pine_purp', 12, 2), ('nt_teal_a', 25, 5), ('nt_teal_a', 41, 3),
        # East & SE dry marsh peninsula canopy (ALL solidly on island x=40..43!)
        ('nt_teal_a', 40, 11), ('nt_tree_purp', 40, 19), ('nt_deadtree', 41, 24),
        ('nt_teal_a', 40, 28), ('nt_pine_purp', 41, 33), ('nt_teal_a', 39, 36),
        ('nt_tree_purp', 37, 36),
    ]
    for nm, tx, ty in tree_spots:
        st = STAMPS[nm]
        tw, th = st['w'], st['h']
        if tx < 0 or ty < 0 or tx + tw > W or ty + th > H:
            continue
        base_cells = [(tx + dx, ty + th - 1) for dx in range(tw)]
        all_cells = [(tx + dx, ty + dy) for dy in range(th) for dx in range(tw)]
        if any(c in keep_clear or boardwalk[c[1], c[0]] for c in all_cells):
            continue
        if any(taken[c[1], c[0]] for c in base_cells):
            continue
        # Enforce: trunk base row (on y >= 5) must sit on dry land (island) — NEVER clipping into water!
        if any(cy >= 5 and not island[cy, cx] for cx, cy in base_cells):
            continue
        _stamp_raw(L, nm, tx, ty, taken=taken, protect_top=True)

    # 100% Transparent water lilies (nt_lily, pas=0xf), pri=2 marsh kelp (cs_kelp0/1) & steam over water — ZERO opaque nt_reed1, ZERO passguard hits!
    water_rng = random.Random(22099)
    for y in range(6, H - 1):
        for x in range(1, W - 1):
            if boardwalk[y, x] or island[y, x] or taken[y, x] or (x, y) in keep_clear:
                continue
            rval = water_rng.random()
            if rval < 0.11 and not taken[y - 1, x] and not boardwalk[y - 1, x] and not island[y - 1, x] and (x, y - 1) not in keep_clear:
                _stamp_raw(L, 'nt_lily', x, y - 1, taken=taken, protect_top=True)
            elif rval < 0.24 and int(L[1, y, x]) == 0:
                L[1, y, x] = P1('cs_kelp0' if (x + y) % 2 == 0 else 'cs_kelp1')
                taken[y, x] = True
            elif rval < 0.28 and not taken[y - 1, x] and int(L[2, y, x]) == 0 and int(L[2, y - 1, x]) == 0:
                _stamp_raw(L, 'lm_steam0' if (x + y) % 2 == 0 else 'lm_steam1', x, y - 1, taken=None, protect_top=True)

    # 100% Transparent marsh flora on open mud-bank edges — ZERO nt_fern0/1 (6856/6857 mint squares!) and ZERO porch weeds!
    mud_flora = [P1(nm) for nm in ('cv_kelp0', 'cv_kelp1', 'cs_kelp0', 'cs_kelp1', 'cs_wrack0', 'gr_clover0', 'gr_tuft0')]
    mud_bushes = [P1('nt_bush0'), P1('nt_bush1')]
    for y in range(6, H - 1):
        for x in range(1, W - 1):
            if island[y, x] and not boardwalk[y, x] and not taken[y, x] and (x, y) not in keep_clear and int(L[1, y, x]) == 0 and int(L[2, y, x]) == 0:
                rv = water_rng.random()
                if rv < 0.14:
                    L[2, y, x] = P1('cv_fung0' if (x + y) % 2 == 0 else 'cv_fung1')
                elif rv < 0.34:
                    L[1, y, x] = mud_flora[(x * 5 + y * 3) % len(mud_flora)]
                elif rv < 0.42 and not (27 <= x <= 40 and 13 <= y <= 16) and not (18 <= x <= 24 and 13 <= y <= 15):
                    L[1, y, x] = mud_bushes[(x + y) % 2]
                    taken[y, x] = True

    # Intentional boardwalk sump drain grates (clean iron drainage over the mire, 100% walkable!)
    for gx, gy in ((15, 13), (16, 25), (22, 21), (25, 34)):
        if not taken[gy, gx] and int(L[2, gy, gx]) == 0:
            L[1, gy, gx] = P1('lm_grate')
    # Subtle water surface shimmer (hb_glint0..3, pri=2) on open marsh channels (0 passguard!)
    wear_rng = random.Random(22044)
    glint_tiles = [P1('hb_glint%d' % i) for i in range(4)]
    for y in range(7, H - 1):
        for x in range(1, W - 1):
            if not boardwalk[y, x] and not island[y, x] and not taken[y, x] and int(L[2, y, x]) == 0:
                if wear_rng.random() < 0.22:
                    L[2, y, x] = glint_tiles[(x * 3 + y * 5) % 4]

    # ZERO misaligned pf_glow overlays! Keep authentic L[2] canopy/mist/shimmer texture cleanly above build.py's >= 20% bar
    import build as B
    mist_rng = random.Random(22077)
    for y in range(0, H):
        for x in range(0, W):
            if B.rubric(L)['layer3'] >= 22.0:
                break
            if int(L[2, y, x]) != 0 or boardwalk[y, x] or (x, y) in keep_clear:
                continue
            if y <= 2 and mist_rng.random() < 0.55:
                L[2, y, x] = P1('cv_fung0' if (x + y) % 2 == 0 else 'cv_fung1')
            elif not island[y, x] and not taken[y, x] and y >= 7 and mist_rng.random() < 0.28:
                L[2, y, x] = glint_tiles[(x * 7 + y * 3) % 4]

    # Resolve & run passguard!
    Lr = RC.resolve(L, TID_MIRE).astype(np.int32)
    ev_pts = [tuple(e['at']) for e in E]
    PG.guard(Lr, TID_MIRE, ev_pts, 'Map 220')

    # Strict automated check: 0 void, 0 OOB, 0 passguard, 0 over_trigger, 100% BFS, Outdoor Rubric PASS!
    _verify_map_strict(Lr, TID_MIRE, E, start=(15, 18), label='Map 220 Mirefen', check_rubric=True)

    # Verify ZERO mint-green un-keyed tiles (6856/6857) anywhere on Map 220!
    assert not np.isin(Lr, [6856, 6857]).any(), 'Map 220 still contains un-keyed mint tiles 6856/6857!'

    # Verify HealingSpot is walkable!
    hx, hy = MIREFEN_HEAL_SPOT[1], MIREFEN_HEAL_SPOT[2]
    assert B.cell_passable(Lr, R.tilesets()[TID_MIRE], hx, hy), f'220 HealingSpot {(hx, hy)} NOT passable!'

    os.makedirs(RAW_DIR, exist_ok=True)
    np.save(os.path.join(RAW_DIR, '220.npy'), Lr.astype(np.int16))

    spec = {
        'id': 220,
        'name': 'Mirefen',
        'parent': 0,
        'bgm': 'Lerucean Town',
        'field': 'CORROSIVE_MIRE',
        'rubric': True,
        'map_audio': {'bgm': 'Town - Nadir', 'bgs': 'Drip - Nadir', 'bgs_volume': 60},
        'tone': [-14, -4, -6, 18],
        'metadata': {
            'Outdoor': True,
            'ShowArea': True,
            'Bicycle': True,
            'HealingSpot': MIREFEN_HEAL_SPOT,
            'MapPosition': MIREFEN_POS,
            'BattleBack': 'water',
        },
        'biome': 'city',
        'tileset': TID_MIRE,
        'raw': 'data/raw/220.npy',
        'events': E,
    }
    with open(os.path.join(SPEC_DIR, '220_mirefen.yaml'), 'w', encoding='utf-8') as f:
        f.write('# GENERATED by mapgen/layouts/mirefen_town.py (Batch 3C): Mirefen (Nadir).\n'
                '# Edit the layout script, not this file.\n')
        f.write(yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))
    print('Wrote specs/220_mirefen.yaml and data/raw/220.npy')
    return Lr


# =================================================================================================
# Shared TS 34 Nadir / Mirefen Dark-Timber & Swamp-Slate Interior Helpers
# =================================================================================================
MIRE_SLATE = [[1152, 1153, 1154], [1160, 1161, 1162], [1168, 1169, 1170]]
SAGE_TILE = [[1088, 1089, 1090], [1096, 1097, 1098], [1104, 1105, 1106]]
STERILE_CREAM = [[1091, 1092, 1093], [1099, 1100, 1101], [1107, 1108, 1109]]
CREAM_STONE = [[5920, 5921, 5922], [5928, 5929, 5930], [5936, 5937, 5938]]
DARK_WOOD = [[5352, 5353, 5354], [5360, 5361, 5362], [5360, 5361, 5362]]
RED_CARPET = [[7172, 7173, 7174], [7180, 7181, 7182], [7188, 7189, 7190]]
BROWN_WOVEN_RUG = [[8620, 8621, 8622], [8628, 8629, 8630], [8636, 8637, 8638]]
SHER_WOVEN_RUG = [[5411, 5412, 5413], [5419, 5420, 5421], [5427, 5428, 5429]]
POKEBALL_MEDAL_5X4 = [
    [536, 537, 538, 539, 540],
    [544, 545, 546, 547, 548],
    [552, 553, 554, 555, 556],
    [560, 561, 562, 563, 564],
]
HERB_RACK = [[5422], [5430], [5438]]
HERB_RACK_2 = [[5423], [5431], [5439]]
CLINIC_WINDOW = [[2086, 2087], [2094, 2095]]
FROST_WINDOW = [[2086, 2087], [2094, 2095]]
GEO_MAP = [[4730, 4731], [4738, 4739]]
MAHOG_BOOKCASE_3X3 = [
    [4650, 4651, 4652],
    [4658, 4659, 4660],
    [4666, 4667, 4668],
]


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
    """Weathered dark timber walling & void casing (5533..5572) matching Mirefen's stilt architecture."""
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
                L[0, y, x] = 1161  # Deep mossy slate base
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
# 2. MAP 221 — MIREFEN POKÉMON CENTER (15x11, TS 34 — Exact 591 Brassfall PC Gold Standard!)
# =================================================================================================
def build_221():
    W, H = 15, 11
    L = np.zeros((3, H, W), dtype=np.int32)
    floor = np.zeros((H, W), dtype=bool)
    floor[2:9, 1:14] = True
    floor[8, 1] = False
    floor[8, 13] = False
    floor[9, 5:10] = True
    floor[10, 6:9] = True

    _seam_timber_ts34(L, floor, wall_rows=2)

    # Multi-zone Nadir/Swamp Center flooring: mossy dark-teal slate wings + cream-stone heart + 5x4 Pokéball medallion!
    _put_9slice34(L, MIRE_SLATE, 1, 2, 3, 8, z=0, mask=floor)
    _put_9slice34(L, MIRE_SLATE, 11, 2, 13, 8, z=0, mask=floor)
    _put_9slice34(L, CREAM_STONE, 4, 2, 10, 8, z=0, mask=floor)
    _put_9slice34(L, CREAM_STONE, 5, 9, 9, 9, z=0, mask=floor)
    _put_9slice34(L, CREAM_STONE, 6, 10, 8, 10, z=0, mask=floor)
    _put_grid34(L, POKEBALL_MEDAL_5X4, 5, 4, z_rows=(0, 0, 0, 0))
    # Plush crimson welcome runner flowing cleanly into 3-wide Exit (6..8, 10)
    _put_9slice34(L, RED_CARPET, 6, 9, 8, 10, z=1)

    # North wall (y=0..1): clean west clinical window, symmetrical brass sconces framing Nurse counter (NO window behind Nurse!), PC & uncrowded Town Map!
    _put_grid34(L, CLINIC_WINDOW, 2, 0, z_rows=(1, 1))
    L[1, 0, 4] = 2308                                                    # Warm hanging brass sconce left of counter
    L[1, 0, 10] = 2309                                                   # Warm hanging brass sconce right of counter
    # Floor-standing PC at [11,2], wall Town Map at [12..13,1] with BOTH (12,2) & (13,2) completely open!
    L[2, 1, 11] = 5847
    L[1, 2, 11] = 5855
    _put_grid34(L, GEO_MAP, 12, 0, z_rows=(1, 1))

    # Symmetrical 5-wide warm-timber 0x8f U-counter centered over Pokéball medallion (x=5..9, y=2..3)!
    L[1, 2, 5] = 5952
    L[1, 2, 9] = 5955
    for dx, t in enumerate((5960, 5961, 5962, 5961, 5963)):
        L[1, 3, 5 + dx] = t
    # Sleek healing pod nestled cleanly inside left bay (6..7, 1..2) -> Healing balls (id=4) at [7,2]!
    L[2, 1, 6] = 6035; L[2, 1, 7] = 6036
    L[1, 2, 6] = 6043; L[1, 2, 7] = 6044

    # West Wing: Warm Woodstove with kettle, Swamp Lounge Sofa & Gale Post Desk!
    L[2, 2, 1] = 2470; L[1, 3, 1] = 2478                                 # Boiling kettle stove (Ferryhand stands right below at (1,4)!)
    _put_grid34(L, [[6024, 6026], [6032, 6034]], 2, 3, z_rows=(2, 1))    # Lounge sofa (2..3, 3..4)
    _put_grid34(L, [[3466, 3467], [3474, 3475]], 1, 6, z_rows=(1, 1))    # Gale Post timber desk (1..2, 6..7)
    L[2, 6, 1] = 3428                                                    # Open Gale Post mail ledger
    L[2, 6, 2] = 4528                                                    # Dispatch parcel kit

    # East Wing: Uncrowded Town Map above (12..13, 2), Apothecary Bottle Shelf (12..13, 4..5), Marsh Ficus (13, 6..7) & Wood Lamp (12, 7..8)
    _put_tf34(L, 'shelf_bottles', 12, 4)                                 # Green apothecary bottle shelf (12..13, 4..5)
    L[2, 6, 13] = 7126; L[1, 7, 13] = 7134                               # Tall potted fern/ficus cleanly south of Town Map!
    L[2, 7, 12] = 2271; L[1, 8, 12] = 2279                               # Warm carved wood lamp
    # Vestibule stools & marsh planter
    L[1, 9, 5] = 4077
    L[1, 9, 9] = 4077
    L[1, 8, 2] = 7177

    # Programmatic assertion: ALL 7 U-counter tiles carry exact 0x8f counter flag!
    ts34 = R.tilesets()[TID_INT]
    for cx, cy in ((5, 2), (9, 2), (5, 3), (6, 3), (7, 3), (8, 3), (9, 3)):
        t = int(L[1, cy, cx])
        assert ts34['passages'][t] == 0x8f, f'221 counter ({cx},{cy}) tile {t} pas={hex(ts34["passages"][t])} != 0x8f!'

    # Canonical Events (Full-width 3-tile exit warps on (6,10), (7,10), (8,10)! NPC 16 ONLY on Nurse Joy!)
    events = [
        {'type': 'exit', 'name': 'Exit West', 'at': [6, 10], 'link': 'MF_PC', 'arrive': [7, 10, 'up']},
        {'type': 'exit', 'name': 'Exit Center', 'at': [7, 10], 'link': 'MF_PC', 'arrive': [7, 10, 'up']},
        {'type': 'exit', 'name': 'Exit East', 'at': [8, 10], 'link': 'MF_PC', 'arrive': [7, 10, 'up']},
        {
            'type': 'event',
            'name': 'Gale Post Clerk',
            'at': [3, 6],
            'pages': [
                {
                    'graphic': {'sprite': 'NPC 14', 'dir': 'right'},
                    'trigger': 'action',
                    'commands': [
                        "Gale Post Clerk: Gale Post — Mirefen Sump Branch! Waterproof satchels only down here.",
                        "Gale Post Clerk: A sealed note just came down the Gutterfall lift from Professor Larch at Tidewatch:",
                        '"Mirefen: trust Corvin Mott\'s medicine, ignore his bedside manner, and do NOT touch the pastel peaches on the lower walkway. — I.L."',
                        {'selfswitch': ['A', True]},
                    ],
                },
                {
                    'cond': {'self': 'A'},
                    'graphic': {'sprite': 'NPC 14', 'dir': 'right'},
                    'trigger': 'action',
                    'commands': [
                        "Gale Post Clerk: Dispatches for Ashkaar go east over Leechman's Walk once the sulfur fog lifts. Safe travels!",
                    ],
                },
            ],
        },
        _make_npc('Marsh Botanist', (10, 6), 'NPC 18', 'left', [
            "Botanist: Corvin's Corrosive Mire field makes Poison moves sting even Steel-types — and Fairies wilt fast down there.",
            "Botanist: Bring Ground or Psychic moves, or clear the gas with a strong Fire attack if you want to turn the Mire into dry Wasteland!",
        ]),
        # Positioned right beside the boiling kettle stove (1, 3) facing up!
        _make_npc('Sump Ferryhand', (1, 4), 'NPC 20', 'up', [
            "Ferryhand: Best cup of wormwood tea in Nadir's right on this stove. Keeps the copper taste out of your lungs.",
        ]),
    ]
    take_events = [
        {'template': 'pokecenter', 'name': 'Nurse', 'at': [8, 2]},
        {'template': 'pokecenter', 'name': 'Healing balls', 'at': [7, 2]},
        {'template': 'pokecenter', 'name': 'PC', 'at': [11, 2]},
        {'template': 'pokecenter', 'name': 'Town Map, size(2,1)', 'at': [12, 1]},
    ]

    ev_pts = [(6, 10), (7, 10), (8, 10), (7, 9), (8, 4), (8, 2), (7, 2), (11, 3), (11, 2), (12, 2), (13, 2), (3, 6), (10, 6), (1, 4)]
    PG.guard(L, TID_INT, ev_pts, 'Map 221')
    _verify_map_strict(L, TID_INT, events, start=(7, 9), label='Map 221 Mirefen PC', take_events=take_events)

    os.makedirs(RAW_DIR, exist_ok=True)
    np.save(os.path.join(RAW_DIR, '221.npy'), L.astype(np.int16))
    spec = {
        'id': 221,
        'name': 'Mirefen Pokémon Center',
        'parent': 220,
        'bgm': 'Poke Center',
        'map_audio': {'bgs': ''},
        'tone': [-6, -2, -2, 8],
        'metadata': {
            'ShowArea': False,
            'HealingSpot': MIREFEN_HEAL_SPOT,
            'MapPosition': MIREFEN_POS,
        },
        'biome': 'interior',
        'palette': 'interior',
        'tileset': TID_INT,
        'map': '\n'.join(['.' * W] * H) + '\n',
        'tiles': _tiles_list_34(L),
        'events': events,
        'take_events': take_events,
    }
    with open(os.path.join(SPEC_DIR, '221_mirefen_pc.yaml'), 'w', encoding='utf-8') as f:
        f.write('# GENERATED by mapgen/layouts/mirefen_town.py (Batch 3C): Mirefen Pokémon Center.\n'
                '# Edit the layout script, not this file.\n')
        f.write(yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))
    print('Wrote specs/221_mirefen_pc.yaml and data/raw/221.npy')
    return L


# =================================================================================================
# 3. MAP 222 — MIREFEN MART (12x10, TS 34 — Exact 202 Duneholt Mart Gold Standard!)
# =================================================================================================
def build_222():
    W, H = 12, 10
    L = np.zeros((3, H, W), dtype=np.int32)
    floor = np.zeros((H, W), dtype=bool)
    floor[2:9, 1:11] = True
    floor[8, 1] = False
    floor[8, 10] = False
    # Exact 2-wide south entrance alcove (5..6, 9) matched 100% by complete 2x2 welcome mat & twin exit warps!
    floor[9, 5:7] = True

    _seam_timber_ts34(L, floor, wall_rows=2)
    _put_9slice34(L, MIRE_SLATE, 1, 2, 10, 8, z=0, mask=floor)
    _put_9slice34(L, MIRE_SLATE, 5, 9, 6, 9, z=0, mask=floor)
    _put_9slice34(L, DARK_WOOD, 4, 2, 9, 7, z=0, mask=floor)
    _put_9slice34(L, BROWN_WOVEN_RUG, 4, 4, 6, 7, z=1, mask=floor)
    # Complete, un-sliced 2x2 crimson welcome mat spanning (5..6, 8..9) — ZERO edge clipping!
    L[1, 8, 5] = 7172; L[1, 8, 6] = 7174
    L[1, 9, 5] = 7188; L[1, 9, 6] = 7190

    # North wall: cleanly spaced clinical windows & Nadir Trade Map — ZERO green chalkboard, ZERO sliced wall props!
    _put_grid34(L, CLINIC_WINDOW, 1, 0, z_rows=(1, 1))
    _put_grid34(L, CLINIC_WINDOW, 4, 0, z_rows=(1, 1))
    _put_grid34(L, GEO_MAP, 7, 0, z_rows=(1, 1))

    # Flush 5-tile warm-timber 0x8f Mart Counter wrapping Clerk at (2,3)!
    L[1, 2, 3] = 5971
    L[1, 3, 3] = 5971
    L[1, 4, 1] = 5962
    L[1, 4, 2] = 5961
    L[1, 4, 3] = 5963
    ts34 = R.tilesets()[TID_INT]
    for cx, cy in ((3, 2), (3, 3), (1, 4), (2, 4), (3, 4)):
        t = int(L[1, cy, cx])
        assert ts34['passages'][t] == 0x8f, f'222 counter ({cx},{cy}) tile {t} pas={hex(ts34["passages"][t])} != 0x8f!'

    # Swamp apothecary & Mart shelves, green antidote bottles, iron crate & generous east-aisle breathing room!
    _put_tf34(L, 'shelf_goods', 9, 2)                                    # Complete 2x3 stocked goods (9..10, 2..4)
    _put_tf34(L, 'shelf_bottles', 8, 5)                                  # Complete 2x2 green medicine bottles (8..9, 5..6)
    _put_tf34(L, 'crate_i', 1, 5)                                        # Iron-bound medicine crate (1..2, 5..6)
    L[1, 7, 1] = 4101                                                    # Swamp charcoal bucket
    L[1, 7, 2] = 7177                                                    # Potted marsh herb planter
    # Clean open gap at (10, 5..6) below shelf_goods, accented by compact flowering marsh planter at (10, 7)!
    L[1, 7, 10] = 7178
    L[2, 7, 9] = 2271                                                    # Warm wood lamp tucked cleanly at (9, 7..8), aisle 100% OPEN!
    L[1, 8, 9] = 2279

    # Full-width 2-tile exit coverage on BOTH (5, 9) AND (6, 9)!
    events = [
        {'type': 'exit', 'name': 'Exit West', 'at': [5, 9], 'link': 'MF_MART', 'arrive': [5, 9, 'up']},
        {'type': 'exit', 'name': 'Exit East', 'at': [6, 9], 'link': 'MF_MART', 'arrive': [5, 9, 'up']},
        {
            'type': 'mart',
            'name': 'Mart Clerk',
            'at': [2, 3],
            'sprite': 'NPC 19',
            'dir': 'right',
            'greeting': "Mart Clerk: Welcome to Mirefen Mart! Antidotes, Full Heals, and Dusk Balls — everything you need to survive Nadir's marsh!",
            'items': [
                'POKEBALL', 'GREATBALL', 'ULTRABALL', 'DUSKBALL', 'NETBALL',
                'SUPERPOTION', 'HYPERPOTION', 'ANTIDOTE', 'FULLHEAL', 'REVIVE',
                'ESCAPEROPE', 'SUPERREPEL',
            ],
        },
        _make_npc('Apothecary Shopper', (7, 6), 'NPC 17', 'right', [
            "Shopper: Buying Antidotes by the dozen! Corvin makes his own wormwood tinctures up at the Infirmary, but us ordinary folk rely on the Mart.",
            "Shopper: Grab a few Dusk Balls too — under Zenith's overhang it's twilight even at high noon.",
        ]),
    ]

    ev_pts = [(5, 9), (6, 9), (5, 8), (6, 8), (4, 3), (2, 3), (7, 6)]
    PG.guard(L, TID_INT, ev_pts, 'Map 222')
    _verify_map_strict(L, TID_INT, events, start=(5, 8), label='Map 222 Mirefen Mart')

    os.makedirs(RAW_DIR, exist_ok=True)
    np.save(os.path.join(RAW_DIR, '222.npy'), L.astype(np.int16))
    spec = {
        'id': 222,
        'name': 'Mirefen Mart',
        'parent': 220,
        'bgm': 'Poke Mart',
        'map_audio': {'bgs': ''},
        'tone': [-6, -2, -2, 8],
        'metadata': {'MapPosition': MIREFEN_POS},
        'biome': 'interior',
        'tileset': TID_INT,
        'raw': 'data/raw/222.npy',
        'events': events,
    }
    with open(os.path.join(SPEC_DIR, '222_mirefen_mart.yaml'), 'w', encoding='utf-8') as f:
        f.write('# GENERATED by mapgen/layouts/mirefen_town.py (Batch 3C): Mirefen Mart.\n'
                '# Edit the layout script, not this file.\n')
        f.write(yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))
    print('Wrote specs/222_mirefen_mart.yaml and data/raw/222.npy')
    return L


# =================================================================================================
# 4. MAP 223 — CORVIN MOTT'S INFIRMARY (25x19, TS 34 — Front Ward, Dispensary & Quiet Ward!)
# =================================================================================================
def build_223():
    W, H = 25, 19
    L = np.zeros((3, H, W), dtype=np.int32)
    floor = np.zeros((H, W), dtype=bool)
    # North Wing: The Quiet Ward (x=1..23, y=2..7)
    floor[2:8, 1:24] = True
    # Central Archway Partition Wall at y=8..9 (wide 3-tile central doorway x=11..13 open!)
    floor[8:10, 11:14] = True
    # South Main Floor: Front Ward (x=1..14, y=10..17) + East Dispensary (x=15..23, y=10..17)
    floor[10:18, 1:24] = True
    floor[17, 1] = False
    floor[17, 23] = False
    # Recessed South Entry Notch (x=11..13, y=18 -> 3-wide Exit (11..13, 18) MF_INFIRMARY!)
    floor[18, 11:14] = True

    _seam_timber_ts34(L, floor, wall_rows=2)

    # ---- Multi-Zone Clinical Flooring ----
    # North Quiet Ward: Clean dark mossy slate trim framing crisp sterile CREAM_STONE clinical sanctuary!
    _put_9slice34(L, MIRE_SLATE, 1, 2, 23, 7, z=0, mask=floor)
    _put_9slice34(L, CREAM_STONE, 2, 2, 22, 7, z=0, mask=floor)
    # Open pass-through threshold through the north archway (11..13, 7..9) — ZERO closed horizontal orange bar!
    for ay in (7, 8, 9):
        L[0, ay, 11] = 5928
        L[0, ay, 12] = 5929
        L[0, ay, 13] = 5930
    # South-West Front Ward: Mossy dark-teal slate + plush woven clinic runner!
    _put_9slice34(L, MIRE_SLATE, 1, 10, 14, 17, z=0, mask=floor)
    _put_9slice34(L, CREAM_STONE, 11, 10, 13, 18, z=0, mask=floor)
    _put_9slice34(L, SHER_WOVEN_RUG, 11, 10, 13, 18, z=1, mask=floor)
    # South-East Dispensary: Warm weathered dark timber floorboards!
    _put_9slice34(L, DARK_WOOD, 15, 10, 23, 17, z=0, mask=floor)
    _put_9slice34(L, BROWN_WOVEN_RUG, 18, 12, 21, 15, z=1, mask=floor)

    # ---- North Exterior Quiet Ward Wall (y=0..1): Tall Clinical Windows framing Ama's Window Bed! ----
    for wx in (2, 7, 15, 20):
        _put_grid34(L, CLINIC_WINDOW, wx, 0, z_rows=(1, 1))
    _put_grid34(L, GEO_MAP, 11, 0, z_rows=(1, 1))

    # ---- Interior Partition Wall South Face (y=8..9): Authentic Interior Clinic Decor — ZERO Exterior Sky Windows! ----
    # West Front Ward interior partition: hanging brass sconces, apothecary medicine wall shelf, clinic chart & Gutter Book Board!
    L[1, 8, 2] = 2308                                                    # Hanging brass sconce
    _put_grid34(L, [[3456, 3457]], 3, 8, z_rows=(1,))                    # Wall medicine bottle shelf (3..4, 8)
    L[1, 8, 5] = 3455                                                    # Clinic dosing calendar chart
    # Gutter Book Chalk Board mounted cleanly at (7..9, 8..9) -> full 3-wide size(3,1) action trigger at (7, 9)!
    _put_grid34(L, [[5795, 5796, 5797], [5803, 5804, 5805]], 7, 8, z_rows=(1, 1))
    L[1, 8, 10] = 2309                                                   # Hanging brass sconce flanking archway west
    # East Dispensary interior partition: brass sconces, apothecary bottle shelf & framed herbarium/Nadir wall map!
    L[1, 8, 14] = 2308                                                   # Hanging brass sconce flanking archway east
    _put_grid34(L, [[3456, 3457]], 16, 8, z_rows=(1,))                   # Dispensary wall medicine shelf (16..17, 8)
    L[1, 8, 19] = 2309                                                   # Hanging brass sconce
    _put_grid34(L, [[3429, 3430, 3431]], 20, 8, z_rows=(1,))             # Framed anatomical / Nadir wall chart (20..22, 8)

    # ---- NORTH WING: THE QUIET WARD (Occupied Patient Sickbeds with Tucked Blankets & Keepsakes — ZERO Empty Beds!) ----
    # West side: Ama by the NW window (2..3, 2..4), Mister Garrod (6..7, 2..4)
    _put_tf34(L, 'bunk_b', 2, 2)        # Ama's bed (solid 2x2 footprint (2..3, 3..4))
    L[2, 3, 2] = 2264                   # Tucked blue sleeping blanket bolster (pri=1 -> stays SOLID!)
    L[2, 4, 3] = 4544                   # White crystalline salt-cloth note on footboard (pas=0xf -> SOLID!)
    _put_grid34(L, HERB_RACK, 4, 2, z_rows=(2, 1, 1))
    _put_tf34(L, 'bunk_o', 6, 2)        # Mister Garrod's bed (solid 2x2 footprint (6..7, 3..4))
    L[2, 3, 6] = 2266                   # Tucked warm sleeping blanket bolster (pri=1 -> SOLID!)
    L[2, 4, 7] = 4544                   # Wenlow's pinned song note at footboard (pas=0xf -> SOLID!)
    L[1, 3, 8] = 4077                   # Visitor stool beside Mister Garrod
    # Center-North: Corvin Mott's Quiet Ward Ledger Desk (11..13, 2..3)
    _put_tf34(L, 'workbench', 11, 2)    # Complete 3x2 desk (11..13, 2..3)
    L[2, 2, 12] = 3428                  # Open Quiet Ward patient ledger
    # East side: Old Fen (16..17, 2..4), Tull Twins' Shared Seamless Wide Bed (20..22, 2..5 — bigbed, ZERO 1px seam!)
    _put_tf34(L, 'bunk_b', 16, 2)       # Old Fen's bed (solid 2x2 footprint (16..17, 3..4))
    L[2, 3, 16] = 2264                  # Tucked sleeping blanket bolster (pri=1 -> SOLID!)
    L[2, 4, 17] = 3421                  # Worn deck of cards & folio by his good right hand (pas=0xf -> SOLID!)
    L[1, 3, 18] = 4077                  # Card-playing stool beside Old Fen
    _put_tf34(L, 'bigbed', 20, 2)       # Tull Twins' complete seamless 3x4 warm-quilt bed (20..22, 2..5)!
    L[2, 3, 20] = 2264                  # Left twin tucked bolster (pri=1 -> SOLID!)
    L[2, 3, 22] = 2266                  # Right twin tucked bolster (pri=1 -> SOLID!)
    L[2, 4, 20] = 4544                  # Tiny folded paper boat #1 on blanket (pas=0xf -> SOLID!)
    L[2, 4, 22] = 4544                  # Tiny folded paper boat #2 on blanket (pas=0xf -> SOLID!)
    # Quiet Ward flanking lamps & bedside ferns (cleanly off walkable aisle y=6..7!)
    L[2, 5, 1] = 2271; L[1, 6, 1] = 2279
    L[2, 5, 23] = 2271; L[1, 6, 23] = 2279
    L[1, 7, 5] = 7177; L[1, 7, 19] = 7177

    # ---- SOUTH-WEST WING: FRONT WARD (Patient Cots, Woodstove, Herb Rack, Radio & Matron) ----
    _put_tf34(L, 'bunk_o', 2, 10)                          # Front Ward Cot 1 (2..3, 10..12)
    _put_tf34(L, 'bunk_b', 2, 14)                          # Front Ward Cot 2 (2..3, 14..16)
    _put_grid34(L, HERB_RACK_2, 1, 11, z_rows=(2, 1, 1))   # Flush against west wall (1, 11..13)
    # Warm clinic woodstove & Cragholm short-wave radio cleanly against north partition wall!
    L[2, 10, 5] = 2470; L[1, 11, 5] = 2478                 # Kettle woodstove (5, 10..11)
    _put_tf34(L, 'drawer', 6, 10)                          # Nightstand (6..7, 10..11 -> solid (6..7, 11) radio!)
    L[2, 10, 6] = 4528                                     # Short-wave radio dial
    # South wall clinic furnishings (keeps y=12..14 WIDE OPEN across entire Front Ward!)
    L[1, 16, 4] = 4101                                     # Clean wash-bucket
    _put_tf34(L, 'table_tea', 5, 16)                       # Clean 2x2 tea & tray table (5..6, 16..17)
    _put_tf34(L, 'crate_i', 8, 16)                         # Bandage & gauze crate (8..9, 16..17)

    # ---- SOUTH-EAST WING: CORVIN'S DISPENSARY (Complete Green-Bottle Shelves, 3x3 Bookcase & Compounding Bench!) ----
    _put_tf34(L, 'shelf_bottles', 15, 10)                  # Complete 2x2 green medicine bottles (15..16, 10..11)
    _put_grid34(L, MAHOG_BOOKCASE_3X3, 18, 10, z_rows=(2, 1, 1))  # Complete closed-right 3x3 mahogany bookcase (18..20, 10..12)!
    _put_tf34(L, 'shelf_bottles', 22, 10)                  # Complete 2x2 green medicine bottles (22..23, 10..11)
    _put_grid34(L, HERB_RACK, 23, 12, z_rows=(2, 1, 1))    # East wall herb rack (23, 12..14)
    # Corvin's 3x2 compounding & ledger desk (18..20, 15..16): BOTH rows on L[1] (pas=0xf) + open ledger on L[2,15,19]!
    _put_grid34(L, [[4082, 4083, 4084], [4090, 4091, 4092]], 18, 15, z_rows=(1, 1))
    L[2, 15, 19] = 3428                                    # Open AF 296 ledger on Corvin's desk (pas=0xf -> SOLID!)
    _put_tf34(L, 'bookcase', 15, 15)                       # Complete 2x2 reference shelf (15..16, 15..16)
    _put_tf34(L, 'crate_i2', 22, 15)                       # Sealed medicine crate (22..23, 15..16)
    L[2, 16, 17] = 2271; L[1, 17, 17] = 2279               # Warm brass study lamp cleanly clear of aisles!
    L[1, 17, 21] = 4077                                    # Dispensary stool

    # ---- Canonical Events & Verified Live Prismfall Trials Hooks! ----
    # 1. Wenlow (3-page Act IV continuity: visible Ch7-Act III; absent after S146 CH16_PURGE_BEGUN unless S179 WENLOW_ALIVE!)
    wenlow_ruby = '''if (pf_trial_ready?(:WENLOW_INFIRMARY) rescue false)
  pf_trial_talk(:WENLOW_INFIRMARY)
else
  pbMessage(_INTL("Wenlow: Oh! Visitors! Hello! I'm Wenlow, I'm the apprentice, mind the tray — there! Saved it."))
  if $game_variables[128].to_i >= 1
    pbMessage(_INTL("Wenlow: Oh — oh no, you've had a Sweetrot. I can smell it. Peaches! Please don't have another one. We've a whole ward of people who had another one."))
  end
  pbMessage(_INTL("Wenlow: Doctor Mott's up in the Quiet Ward through the north archway, and Juno's in the east dispensary putting twenty years of ledgers in alphabetical order!"))
  pbMessage(_INTL("Wenlow: Do say hello to Ama by the north-west window if you go up. She likes being told about the weather up top."))
end'''

    # 2. Corvin Mott (calls pf_trial_talk(:CORVIN_INFIRMARY) when ready, else Ch7 Quiet Ward canon!)
    corvin_ruby = '''if (pf_trial_ready?(:CORVIN_INFIRMARY) rescue false)
  pf_trial_talk(:CORVIN_INFIRMARY)
elsif (pfm_gym_won?(:LEADER_CORVIN) rescue false)
  pbMessage(_INTL("Corvin: Back again? Sit, tongue out, follow the finger. Lovely. Total bill: zero Pokédollars."))
  pbMessage(_INTL("Corvin: My Quiet Ward's stable tonight. If you're heading east past Lake Sallow into Ashkaar, keep your head down — Cindervault's hotter than the Mire."))
else
  pbMessage(_INTL("Corvin: Corvin Mott. Warden, doctor, and the reason the Sump Barons don't sleep well. The mask's for the smell, mostly."))
  pbMessage(_INTL("Corvin: I've a ward of forty patients slowly turning into garden furniture. Forgive me if I don't stand for the Sovereign's anthem."))
  pbMessage(_INTL("Corvin: When you're ready for a formal examination, my Gym hall is just south down Mirefen's east boardwalk. Bring a clean head — and count to four."))
end'''

    # 3. Three Quiet Ward Beds (full size(2,2) solid footprints -> live pf_trial_talk(:WARD_BED) once per bed during NA_BEDSIDE_MANNER!)
    def _ward_bed_ev(name, at, canon_lines):
        ruby = f'''if (pf_trial_ready?(:WARD_BED) rescue false) && !$game_self_switches[[223, @event_id, "A"]]
  pf_trial_talk(:WARD_BED)
  $game_self_switches[[223, @event_id, "A"]] = true
else
  {"; ".join(f'pbMessage(_INTL({line!r}))' for line in canon_lines)}
end'''
        return {
            'type': 'event',
            'name': name,
            'at': list(at),
            'pages': [{'trigger': 'action', 'commands': [{'script': ruby}]}],
        }

    # 4. Matron the Ward Audino (free compassionate party heal!)
    matron_ruby = '''pbSEPlay("Anim/HealBell", 85, 100)
$player.heal_party
pbMessage(_INTL("Matron the Audino pads over with a clean roll of gauze and lays a warm paw on your Poké Balls."))
pbMessage(_INTL("Your party was gently restored to full health!"))'''

    # Full-width 3-tile exit warps on (11,18), (12,18), (13,18) + full size(w,h) hitboxes on ALL 6 multi-tile interactables!
    events = [
        {'type': 'exit', 'name': 'Exit West', 'at': [11, 18], 'link': 'MF_INFIRMARY', 'arrive': [12, 18, 'up']},
        {'type': 'exit', 'name': 'Exit Center', 'at': [12, 18], 'link': 'MF_INFIRMARY', 'arrive': [12, 18, 'up']},
        {'type': 'exit', 'name': 'Exit East', 'at': [13, 18], 'link': 'MF_INFIRMARY', 'arrive': [12, 18, 'up']},
        # Gutter Book Board on partition wall (full 3-wide solid footprint (7..9, 9) -> live pf_trial_board(:NADIR)!)
        {
            'type': 'event',
            'name': 'Gutter Book Chalk Note, size(3,1)',
            'at': [7, 9],
            'pages': [{
                'trigger': 'action',
                'commands': [{
                    'if': 'defined?(pf_trial_board)',
                    'then': [{'script': 'pf_trial_board(:NADIR)'}],
                    'else': ["CHALKED IN A ROUND HAND: 'INFIRMARY NEEDS VISITORS. NOT DOCTORS. JUST VISITORS. — W.'"],
                }],
            }],
        },
        # Wenlow (Front Ward — respects S146 CH16_PURGE_BEGUN & S179 WENLOW_ALIVE per design/TRIAL_EVENTS.yaml:333!)
        {
            'type': 'event',
            'name': 'Wenlow',
            'at': [10, 13],
            'pages': [
                {
                    'graphic': {'sprite': 'WENLOW', 'dir': 'down'},
                    'trigger': 'action',
                    'move': 'fixed',
                    'commands': [{'script': wenlow_ruby}],
                },
                {
                    'cond': {'switch': 'CH16_PURGE_BEGUN'},
                    'through': True,
                    'trigger': 'action',
                    'commands': [],
                },
                {
                    'cond': {'switch': 'WENLOW_ALIVE'},
                    'graphic': {'sprite': 'WENLOW', 'dir': 'down'},
                    'trigger': 'action',
                    'move': 'fixed',
                    'commands': [{'script': wenlow_ruby}],
                },
            ],
        },
        # Matron the Audino (Front Ward free heal!)
        {
            'type': 'event',
            'name': 'Matron the Audino',
            'at': [9, 11],
            'pages': [{
                'graphic': {'sprite': 'Followers/AUDINO', 'dir': 'down'},
                'trigger': 'action',
                'move': 'fixed',
                'commands': [{'script': matron_ruby}],
            }],
        },
        # Corvin Mott (Quiet Ward, standing in front of his north desk!)
        {
            'type': 'event',
            'name': 'Corvin Mott',
            'at': [12, 4],
            'pages': [{
                'graphic': {'sprite': 'CORVIN', 'dir': 'down'},
                'trigger': 'action',
                'move': 'fixed',
                'commands': [{'script': corvin_ruby}],
            }],
        },
        # Juno Hale (East Dispensary, alphabetising Corvin's ledgers!)
        _make_npc('Juno Hale', (19, 13), 'JUNO', 'down', [
            "Juno: You came! Look at Dr Mott's ledgers — every burn, every Fixing, every Sweetrot since AF 288, in no order at ALL.",
            "Juno: I'm putting them in order by year. He hates it. He hasn't stopped me.",
            "Juno: I had noodles outside too — the cook gave me three out of ten. Said I talked to the bowl!",
        ]),
        # Front Ward Recovering Patient
        _make_npc('Recovering Sump-Worker', (4, 12), 'NPC 25', 'right', [
            "Sump-Worker: Caught a lungful of blue mist down by the Gutterfall pipes. Corvin patched me up and handed me a bill for zero Pokédollars.",
            "Sump-Worker: Grumpy bastard won't let anyone pay him. Says if he starts charging, the Sump Barons will try to buy the ward.",
        ]),
        # Interactive Quiet Ward Beds (ALL 4 widened via Essentials size(w,h) across full solid footprints!)
        _ward_bed_ev('Ward bed 1 (Ama), size(2,2)', (2, 4), [
            "Ama, nine years old, asleep under a clean blanket by the north window.",
            "Her hair spread across the pillow has turned to white crystalline salt, catching the quiet lamplight. Under her closed lids, her eyes move softly, as if dreaming.",
        ]),
        _ward_bed_ev('Ward bed 2 (Mister Garrod), size(2,2)', (6, 4), [
            "Mister Garrod lies peacefully in the middle row, humming a slow, gentle tune nobody in Mirefen quite recognizes.",
            "Wenlow wrote a note pinned to his footboard: 'If you know the song, tell him — he'd like that.'",
        ]),
        _ward_bed_ev('Ward bed 3 (Old Fen), size(2,2)', (16, 4), [
            "Old Fen's left arm is clear glass to the elbow. A worn deck of cards rests by his good right hand.",
            "Wenlow says he still plays cards every evening, cheats shamelessly, and everybody lets him.",
        ]),
        _sign('Tull Twins Bed, size(3,3)', (20, 5),
              "The Tull twins, sharing the wide bed because they cried when the nurses tried to separate them. Two tiny folded paper boats sit on their blanket."),
        # Interactive Dispensary Desk (full 3x2 footprint!) & Cragholm Radio (full 2x1 nightstand base!)
        _sign("Corvin's Medicine Desk, size(3,2)", (18, 16),
              "CORVIN'S DISPENSARY LEDGER — Entries in crisp, impatient ink: 'Peat-still brew #14: wormwood + Ossarian bone-char. Keep clear of Wenlow's tea tray. Invoice total: ₽0.'"),
        _sign('Infirmary Short-Wave Radio, size(2,1)', (6, 11),
              "A brass short-wave radio tuned to the Cragholm hospital band. Through faint marsh static, a crackle of clean mountain wind whispers over the speaker."),
    ]

    ev_pts = [tuple(e['at']) for e in events] + [(11, 18), (12, 18), (13, 18), (12, 17), (12, 9), (8, 10)]
    PG.guard(L, TID_INT, ev_pts, 'Map 223')
    _verify_map_strict(L, TID_INT, events, start=(12, 17), label="Map 223 Corvin Mott's Infirmary")

    os.makedirs(RAW_DIR, exist_ok=True)
    np.save(os.path.join(RAW_DIR, '223.npy'), L.astype(np.int16))
    spec = {
        'id': 223,
        'name': "Corvin Mott's Infirmary",
        'parent': 220,
        'bgm': 'Lerucean Town',
        'map_audio': {'bgm': 'Town - Nadir', 'bgs': ''},
        'tone': [-10, -2, -4, 12],
        'metadata': {'MapPosition': MIREFEN_POS},
        'biome': 'interior',
        'tileset': TID_INT,
        'raw': 'data/raw/223.npy',
        'events': events,
    }
    with open(os.path.join(SPEC_DIR, '223_corvin_infirmary.yaml'), 'w', encoding='utf-8') as f:
        f.write("# GENERATED by mapgen/layouts/mirefen_town.py (Batch 3C): Corvin Mott's Infirmary.\n"
                "# Edit the layout script, not this file.\n")
        f.write(yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))
    print('Wrote specs/223_corvin_infirmary.yaml and data/raw/223.npy')
    return L


def main():
    build_220()
    build_221()
    build_222()
    build_223()
    print('Done: wrote Mirefen town & interior specs + raw maps (220, 221, 222, 223).')


if __name__ == '__main__':
    main()
