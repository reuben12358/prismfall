#!/usr/bin/env python3
"""layouts/verdance_gym.py — Act 3 Batch 3E: Verdance Gym 9 ("The Heartgarden Gym", Warden Juno Hale — 4 Maps: 290, 291, 292, 293):
  - Map 290: Verdance Gym - Entrance         (21x17, TS 60 PF Rejuv Lumen, field :FLOWER_GARDEN)
      * Sunlit botanical conservatory foyer & TEACH chamber ("Gardens are gossips"):
        - Full-width south exit carpet warps (9..11, 16) -> 283 Glasshouse Ward (24, 10) down!
        - Entrance canal (y=9) spanned by Plot P0 (starts at stage 1 = sprouts; 1 watering -> stage 2 walkable
          timber/vine bridge + S348 ON!) beside decorative neighbour Plot P0_nbr (starts at stage 0 = bare soil;
          grows to stage 1 = sprouts when P0 is watered!).
        - Juno's Sign ("Gardens are gossips..."), Gym Guide (explains 1 + hedges arena field stage up to 5!),
          Conservatory Botanist Healer (full heal), canonical PBS trainer [LASS, Poppy] (100% open sightline),
          HYPERPOTION pickup, and North Portal (10, 4) -> 291 (14, 22) up.
  - Map 291: Verdance Gym - Puzzle Room 1    ("Hedge Garden", 29x25, TS 60 PF Rejuv Lumen, field :FLOWER_GARDEN)
      * TWIST — Ring of Six (P1..P6 around central floral fountain, P_i <-> P_{i+-1} mod 6):
        - Start: P1..P6 = [0, 0, 1, 2, 1, 2] (shifted-mod-4 one-hot pfp_state -> zero autorun race, static preview
          immediately shows soil, sprouts, and bridges!).
        - True physical walkable canal-bridge chain: P1 (SW) -> Island I1 -> P3 (NW) -> Central Fountain Island I2
          -> P5 (NE) -> North Portal Dais (14, 4) -> 292! P2, P4, P6 sit visibly in the moat with ZERO bypass.
        - All 6 solid Brass Watering Spigots on Outer Promenade (100% reachable from start, 0 over_trigger? traps!).
        - Cheapest: 2 waterings (P2 x1, P6 x1) -> 1 hedge; Clean: 5 waterings (P4 x1, P5 x2, P6 x2) -> 0 hedges!
        - Updates V346 (291 hedges), V345 (total hedges = V346 + V347), S345 (G9_RING_DONE).
        - Apprentice Bram (live status, zero-softlock reset, 3-tier progressive hints V348, puzzleskip S301) +
          canonical PBS trainers [AROMALADY, Clover] & [PICNICKER, Daisy] (100% open sightlines).
  - Map 292: Verdance Gym - Puzzle Room 2    ("Glasshouse", 29x25, TS 60 PF Rejuv Lumen, field :FLOWER_GARDEN)
      * COMBINE — Figure-Eight (Ring A: J, A1..A4; Ring B: J, B1..B4 sharing Junction J):
        - Start: J=1; A1..A4=[0, 3, 1, 2]; B1..B4=[2, 0, 3, 1].
        - True physical walkable 5-bridge chain: A2 -> SW Island (Lavender) -> A3 -> NW Island -> J (Center Junction)
          -> Center-East Island (Flora) -> B2 -> East Island -> B3 -> North Arena Dais (14, 4) -> 293!
        - Cheapest: 7 waterings -> 2 hedges; Clean: 8 waterings -> 0 hedges!
        - Updates V347 (292 hedges), V345 (total hedges = V346 + V347), S346 (G9_EIGHT_DONE).
        - Optional Mastery Alcove: THE BRIDE BOWER (off North Arena Dais, M1..M5 in a row: Start [0, 2, 1, 3, 1],
          Target [2, 3, 2, 3, 2], min 6 waterings M2x2, M3x3, M5x1 -> S347 G9_BOWER_DONE -> TELLURICSEED x2 +
          MIRACLESEED + GRASSYSEED + pressed Bride Tree petal lore; never adds to V345!).
        - Apprentice Bram (status, reset, 3-tier hints V349, puzzleskip S301) + canonical PBS trainers
          [AROMALADY, Lavender] & [POKEMONBREEDER, Flora] (100% open sightlines).
  - Map 293: Verdance Gym - Warden Arena     (21x17, TS 60 PF Rejuv Lumen, field :FLOWER_GARDEN)
      * Sunlit rose-glass conservatory battle arena over turquoise reflecting moat, elevated north marble floral dais,
        symmetrical sun-lamps, intact overhead chandelier & ceremonial braziers, framed East Fast-Exit Lift -> 290.
      * Warden Juno Hale (JUNO sprite, single battle: setBattleRule("fieldStage", [1 + V345, 5].min) +
        Prismfall.gym_battle(pfm_gym(:LEADER_JUNO), double: false), awards Meadow Badge via
        Prismfall.award_badge(pfm_gym(:LEADER_JUNO)), TM53 Energy Ball, comments on V345 hedges & S347 Bride Bower
        Mastery, advances V131 CH10_STEP >= 9).

Canonical sources:
  - design/GYM_PUZZLES.md (Gym 9: V345, S345, S346, S347 — verified 0 collisions!)
  - story/28_SCRIPT_CH10.md (Maps 290-293 dialogue, Juno's sign, Gym Guide, Bram, Juno J3)
  - pbs/trainers.txt (Poppy, Clover, Daisy, Lavender, Flora, LEADER_JUNO — verified 0 duplicates!)

Run:
    /usr/bin/python3 -I mapgen/layouts/verdance_gym.py
"""
import os
import sys
import subprocess
import tempfile
from collections import deque
from itertools import product
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
TID = 60                  # PF Rejuv Lumen: slot 1 = RJ Still water (clear garden canal!), full PF Rejuv stamps!
FIELD = 'FLOWER_GARDEN'
VERD_POS = [0, 14, 12]

# Canonical Gym 9 Switch / Variable IDs (strictly within 345..349 — ZERO collisions repo-wide!)
V_HEDGES = 345            # G9_HEDGES: total hedges left across 291 + 292 -> arena field stage 1 + min(V345, 4)
V_HEDGES_291 = 346        # Hedges currently left in 291 Hedge Garden (start: 0)
V_HEDGES_292 = 347        # Hedges currently left in 292 Glasshouse (start: 2, recomputed on water/reset/exit)
V_HINT_291 = 348          # Bram progressive hint counter in 291
V_HINT_292 = 349          # Bram progressive hint counter in 292
S_RING_DONE = 345         # G9_RING_DONE: 291 P1=P3=P5=2
S_EIGHT_DONE = 346        # G9_EIGHT_DONE: 292 J=A2=A3=B2=B3=2
S_BOWER_DONE = 347        # G9_BOWER_DONE: 292 Bride Bower Mastery solved ([2, 3, 2, 3, 2])
S_TEACH_DONE = 348        # G9_TEACH_DONE: 290 P0 bridged
S_PUZZLE_SKIP = 301       # PUZZLE_SKIP password mirror (Core)

# Verified TS 60 (PF Rejuv Lumen) Tile IDs (visually audited on sheet_stamps_ts60.png & stage_contrast_compare.png!)
# 4 UNMISTAKABLY DISTINCT GARDEN PLOT STAGES:
#   Stage 0: Dark espresso-brown bare soil bed (stone-rimmed, impassable pas=0xf)
#   Stage 1: Crisp ivory planter bursting with bright lush green sprouts & buds (lm_planter/lm_planter3, impassable pas=0xf!)
#   Stage 2: Warm cedar timber-and-vine footbridge (WALKABLE pas=0x0, pri=0 -> overrides RJ Still water!)
#   Stage 3: Tall dark-emerald hedge studded with crimson roses (pf_planter0, impassable pas=0xf)
T_SOIL_L = 24309          # pas=0xf, pri=0 (mn_grave_r: dark bare soil planter bed, NO cross)
T_SOIL_R = 24309          # pas=0xf, pri=0
T_SPROUT_L = 25662        # pas=0xf, pri=0 (lm_planter left: bright ivory bed overflowing with vibrant green sprouts!)
T_SPROUT_R = 25663        # pas=0xf, pri=0 (lm_planter right: bright ivory bed overflowing with vibrant green sprouts!)
T_SPROUT_C = 25665        # pas=0xf, pri=0 (lm_planter3 center: 1x1 bright green sprout bed for Bride Bower!)
T_BRIDGE_NS_L = 7972      # pas=0x0, pri=0 (ak cedar boardwalk left edge — matches Verdance bridges!)
T_BRIDGE_NS_R = 7974      # pas=0x0, pri=0 (ak cedar boardwalk right edge)
T_BRIDGE_EW = 7973        # pas=0x0, pri=0 (ak seamless plank for E-W / 1x1 crossing)
T_HEDGE_L = 20501         # pas=0xf, pri=0 (pf_planter0 left: lush dark-emerald hedge studded with crimson roses!)
T_HEDGE_R = 20502         # pas=0xf, pri=0 (pf_planter0 right: lush dark-emerald hedge studded with crimson roses!)

# Conservatory architecture & interactive tile IDs (verified on TS 60!)
T_WATER = 48              # RJ Still water autotile (pas=0xf, pri=0 — clear shimmering turquoise canal!)
T_SPIGOT = P1('cv_sluice')         # 24000, pas=0xf (brass garden watering spigot!)
T_SPIGOT_ALT = P1('cv_sluice_hi')  # 24001, pas=0xf (raised brass reset/mastery valve)
T_PDOOR_OPEN = P1('lm_pdoor_open') # 25936, pas=0x0 (open dark recessed doorway portal)
T_LIFT_PAD = P1('lm_grate')        # 24393, pas=0x0 (solid bolted conservatory fast-exit lift grate — NOT an open pit!)
T_CONDUIT_H = P1('lm_strip_h_on')  # 25924, pas=0x0 (glowing aqua horizontal floor water-conduit channel!)
T_CONDUIT_V = P1('lm_strip_v_on')  # 25926, pas=0x0 (glowing aqua vertical floor water-conduit channel!)
T_LAMP_OFF = P1('lm_lamp')         # 25931, pas=0xf (unlit conservatory portal lantern)
T_LAMP_ON = P1('lm_lamp_on')       # 25932, pas=0xf (glowing lit portal lantern)
T_MAT_L = 24335                    # mn_mat left (pas=0x0)
T_MAT_R = 24336                    # mn_mat right (pas=0x0)
T_CHEST_SHUT = P1('mn_trunk')      # 24344, pas=0xf (sealed Bride Bower heirloom coffer)
T_CHEST_OPEN = P1('mn_trunk_open') # 24345, pas=0xf (opened Bride Bower heirloom coffer)
T_SCONCE = P1('mn_sconce')         # 24212, pas=0xf (gilded conservatory wall sconce)
T_PETALS = P1('mn_petals')         # 24334, pas=0x0 (scattered white Bride Tree petals!)


# =================================================================================================
# Shared Botanical Conservatory & Mod-4 Garden Plot Helpers
# =================================================================================================
def _setup_conservatory_kits():
    """Register crisp 2-row conservatory wall kits (sage-evergreen cvF2, rose-ivory cvP2, emerald cvN2)."""
    for base_k, new_k in (('cvF', 'cvF2'), ('cvP', 'cvP2'), ('cvN', 'cvN2'), ('cvB', 'cvB2')):
        K.KITS[new_k] = dict(K.KITS[base_k], rows=[K.KITS[base_k]['rows'][0], K.KITS[base_k]['rows'][2]])


def _new_conservatory(W, H, seed, wall_kit='cvF2', ter_kit='cvP2'):
    _setup_conservatory_kits()
    m = Cave(W, H, 'F', seed=seed, pool='Still water', tid=TID, game='rejuvenation')
    m.STAIRS = tuple(P1('lm_stair_' + k) for k in 'lmr')
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


def _add_safe_overlay(Lr, tid, stamp_name, pts):
    """Stamp overhead sunbeams / glow halos STRICTLY onto unoccupied L[2] cells — NEVER deletes flames/chandeliers!"""
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
    br_ref = RC.resolve(np.array(STAMPS['fw_brazier']['layers'], dtype=np.int32), TID)
    flame_tid = int(br_ref[2, 0, 0])
    for bx, by in braziers:
        assert int(Lr[2, by, bx]) == flame_tid, (
            f'{label}: fw_brazier flame damaged at ({bx},{by})! got {Lr[2, by, bx]} != {flame_tid}'
        )


def _assert_chandeliers_intact(Lr, chandeliers, label):
    ch_ref = RC.resolve(np.array(STAMPS['mn_chandelier']['layers'], dtype=np.int32), TID)
    for cx, cy in chandeliers:
        for dy in range(2):
            for dx in range(3):
                assert int(Lr[2, cy + dy, cx + dx]) == int(ch_ref[2, dy, dx]), (
                    f'{label}: mn_chandelier ({cx},{cy}) damaged at ({cx+dx},{cy+dy})!'
                )


def _assert_columns_intact(Lr, cols, label):
    """Verify BOTH top capital (22720) and solid base (22721) of every nr_col survive 100% un-chopped!"""
    col_ref = RC.resolve(np.array(STAMPS['nr_col']['layers'], dtype=np.int32), TID)
    top_tid = int(col_ref[2, 0, 0] or col_ref[1, 0, 0])
    bot_tid = int(col_ref[1, 1, 0] or col_ref[0, 1, 0])
    for cx, cy in cols:
        assert int(Lr[2, cy, cx]) == top_tid and int(Lr[1, cy + 1, cx]) == bot_tid, (
            f'{label}: nr_col ({cx},{cy}) decapitated/damaged! top={Lr[2, cy, cx]}({top_tid}), base={Lr[1, cy+1, cx]}({bot_tid})'
        )


def _assert_zero_exit_pockets(Lr, events, y_exit, label):
    """Verify 100% of walkable cells on south exit row `y_exit` are covered by warp events (0 unsealed pockets!)."""
    import build as B
    ts = R.tilesets()[TID]
    W = Lr.shape[2]
    warps = {tuple(e['at']) for e in events if e.get('type') in ('warp', 'exit')}
    pockets = [x for x in range(W) if B.cell_passable(Lr, ts, x, y_exit) and (x, y_exit) not in warps]
    assert not pockets, f'{label}: unsealed walkable border pocket(s) on y={y_exit}: {pockets}'


def _paint_conservatory_floors(m, zones, inlays=()):
    """Apply crisp ivory marble, carved stone paving, walnut timber & mosaic flooring (ZERO B&W checkerboard!)."""
    palettes = {
        'plaza': [P1('lm_plaza0'), P1('lm_plaza1')],
        'pave': [P1('lm_pave%d' % i) for i in range(8)],
        'oak': [P1('A_f%d' % i) for i in range(2)],
        'walnut': [P1('H_f%d' % i) for i in range(2)],
        'mahogany': [P1('N_f%d' % i) for i in range(2)],
    }
    for x0, y0, x1, y1, kind in zones:
        pal = palettes[kind]
        for y in range(max(0, y0), min(m.H, y1 + 1)):
            for x in range(max(0, x0), min(m.W, x1 + 1)):
                if m.cls[y, x] != '.' or m.cliff[y, x]:
                    continue
                if kind == 'plaza':
                    m.L[0, y, x] = pal[(x + y) % 2]
                else:
                    m.L[0, y, x] = pal[(x * 7 + y * 11) % len(pal)]
    # Sweep any default B&W checker F_f* (24035..24038) to warm ivory marble
    plaza = palettes['plaza']
    for y in range(m.H):
        for x in range(m.W):
            if int(m.L[0, y, x]) in (24035, 24036, 24037, 24038):
                m.L[0, y, x] = plaza[(x + y) % 2]
    # Apply gold-cyan marble border inlays cleanly on L[0]
    for x0, y0, x1, y1 in inlays:
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if not m.inb(x, y) or m.cls[y, x] != '.' or m.cliff[y, x]:
                    continue
                on_t, on_b, on_l, on_r = (y == y0), (y == y1), (x == x0), (x == x1)
                if not (on_t or on_b or on_l or on_r):
                    continue
                if on_t and on_l: k = 'nw'
                elif on_t and on_r: k = 'ne'
                elif on_b and on_l: k = 'sw'
                elif on_b and on_r: k = 'se'
                elif on_t or on_b: k = 'h'
                else: k = 'v'
                m.L[0, y, x] = P1('lm_inlay_' + k)


def _paint_emerald_runner(m, x0, y0, x1, y1, medallion=True):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if not m.inb(x, y) or m.cls[y, x] != '.' or m.cliff[y, x] or m.L[1, y, x] != 0:
                continue
            part = ('n' if y == y0 else 's' if y == y1 else '') + ('w' if x == x0 else 'e' if x == x1 else '')
            m.L[1, y, x] = P1('mn_rugG_' + (part or ('c2' if (medallion and (y - y0) % 3 == 1) else 'c')))


def _paint_canal_water(m, cells):
    """Stamp clear turquoise RJ Still water with crisp 48-tile RMXP autotile shorelines onto L[0] and clear L[1..2]."""
    cset = {(x, y) for x, y in cells if m.inb(x, y)}
    for x, y in cset:
        m.cls[y, x] = 'w'
    for x, y in cset:
        b = 0
        for dx, dy, bit in ((0, -1, 1), (1, -1, 2), (1, 0, 4), (1, 1, 8),
                            (0, 1, 16), (-1, 1, 32), (-1, 0, 64), (-1, -1, 128)):
            nx, ny = x + dx, y + dy
            if not m.inb(nx, ny) or (nx, ny) in cset:
                b |= bit
        m.L[0, y, x] = T_WATER + K.NB2AUTO[b]
        m.L[1, y, x] = 0
        m.L[2, y, x] = 0


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


def _stage_tile(stage, side='L', orient='NS'):
    """Return exact verified TS 60 tile ID for garden plot stage (0 soil, 1 sprouts, 2 walkable bridge, 3 hedge)."""
    if stage == 0:
        return T_SOIL_L if side == 'L' else T_SOIL_R
    if stage == 1:
        if side == 'C':
            return T_SPROUT_C
        return T_SPROUT_L if side == 'L' else T_SPROUT_R
    if stage == 2:
        if orient == 'EW' or side == 'C':
            return T_BRIDGE_EW
        return T_BRIDGE_NS_L if side == 'L' else T_BRIDGE_NS_R
    return T_HEDGE_L if side == 'L' else T_HEDGE_R


def _plot_tile_event(ev_name, x, y, s0, side='L', orient='NS', water_ruby=None):
    """Shifted-Mod-4 one-hot 4-stage garden plot tile over turquoise canal water (tile 48, pas=0xf):
      - Page 0 [no cond]:  displays starting stage s0! (Static preview shows true puzzle start!)
      - Page 1 [self A]:   displays (s0 + 1) % 4
      - Page 2 [self B]:   displays (s0 + 2) % 4
      - Page 3 [self C]:   displays (s0 + 3) % 4
    Stage 0/1/3 tiles have pas=0xf -> impassable + safe Action event (0 over_trigger?!).
    Stage 2 tile has pas=0x0 -> overrides canal water (WALKABLE!) with commands=[] so players cross smoothly
    and NEVER accidentally trap themselves inside a hedge!
    """
    pages = []
    self_keys = [None, 'A', 'B', 'C']
    for k in range(4):
        st = (s0 + k) % 4
        pg = {
            'graphic': {'tile': _stage_tile(st, side=side, orient=orient)},
            'trigger': 'action',
            'commands': [] if st == 2 else ([{'script': water_ruby}] if water_ruby else []),
        }
        if self_keys[k] is not None:
            pg['cond'] = {'self': self_keys[k]}
        pages.append(pg)
    return {
        'type': 'event',
        'name': ev_name,
        'at': [x, y],
        'pages': pages,
    }


def _spigot_event(name, x, y, ruby, tile=T_SPIGOT):
    """Solid brass garden watering spigot on dry bank (pas=0xf -> 0 over_trigger?, works at ALL 4 stages 0..3!)."""
    return {
        'type': 'event',
        'name': name,
        'at': [x, y],
        'pages': [{
            'graphic': {'tile': tile},
            'trigger': 'action',
            'commands': [{'script': ruby}],
        }],
    }


def _ruby_plot_inspect(plot_id, label, s0, ev0, nbrs, spigot_hint):
    """Safe read-only plot inspection script (0 state mutation from islands -> mathematically 0 island traps!)."""
    nbr_desc = ', '.join(nbrs) if nbrs else 'none'
    return (
        'st_names = ["Bare Soil", "Sprouts", "Vine Bridge", "Rose Hedge"]\n'
        f'cur_st = ({s0} + pfp_state_of("{ev0}")) % 4\n'
        f'pbMessage(_INTL("{label} — Stage {{1}} ({{2}}). Neighbours: {nbr_desc}. Turn {spigot_hint} to water this bed!", cur_st, st_names[cur_st]))'
    )


def _ruby_water_action(plot_id, label, room_defs, nbrs, room_mode):
    """Generate clean, self-contained Ruby script for watering `plot_id` (+ its neighbours) mod 4,
    with MANDATORY player-on-plot softlock guard, recomputing hedges (V346/V347 -> V345) and completion switch!
    `room_defs` = [(pid, s0, [ev_names...]), ...]
    """
    stages_arr = '["Bare Soil", "Sprouts", "Vine Bridge", "Rose Hedge"]'
    tbl_rows = []
    for pid, s0, evs in room_defs:
        evs_rb = ', '.join(f'"{e}"' for e in evs)
        tbl_rows.append(f'  ["{pid}", {s0}, [{evs_rb}]]')
    tbl_rb = '[\n' + ',\n'.join(tbl_rows) + '\n]'
    targets_rb = ', '.join(f'"{t}"' for t in ([plot_id] + list(nbrs)))
    nbr_desc = ', '.join(nbrs) if nbrs else 'none'

    if room_mode == '290':
        post_rb = f'''  p0_st = cur["P0"]
  $game_switches[{S_TEACH_DONE}] = (p0_st == 2)
  $game_map.need_refresh = true
  if p0_st == 2
    pbSEPlay("Anim/HealBell", 85, 105)
    pbMessage(_INTL("Vines weave across the canal into a sturdy bridge! Beside it, the neighbour bed sprouted too!"))
  elsif p0_st == 3
    pbMessage(_INTL("Plot P0 burst into a dense flowering rose hedge! Water it once more to collapse it back to bare soil."))
  else
    pbMessage(_INTL("Plot P0 is now {{1}}; its neighbour shifted to {{2}}.", st_names[p0_st], st_names[cur["P0N"]]))
  end'''
    elif room_mode == '291':
        post_rb = f'''  h291 = cur.values.count(3)
  $game_variables[{V_HEDGES_291}] = h291
  $game_variables[{V_HEDGES}] = h291 + $game_variables[{V_HEDGES_292}].to_i
  done = (cur["P1"] == 2 && cur["P3"] == 2 && cur["P5"] == 2)
  was_done = $game_switches[{S_RING_DONE}]
  $game_switches[{S_RING_DONE}] = done
  $game_map.need_refresh = true
  if done && !was_done
    pbSEPlay("Anim/HealBell", 90, 100)
    pbMessage(_INTL("P1, P3, and P5 are all woven into vine bridges! The path north is open — hedges left in this room: {{1}}.", h291))
  else
    pbMessage(_INTL("Water ripples along the ring! {{1}} is now {{2}}. (Room hedges: {{3}})", "{label}", st_names[cur["{plot_id}"]], h291))
  end'''
    elif room_mode == '292':
        post_rb = f'''  h292 = cur.values.count(3)
  $game_variables[{V_HEDGES_292}] = h292
  $game_variables[{V_HEDGES}] = $game_variables[{V_HEDGES_291}].to_i + h292
  done = (cur["J"] == 2 && cur["A2"] == 2 && cur["A3"] == 2 && cur["B2"] == 2 && cur["B3"] == 2)
  was_done = $game_switches[{S_EIGHT_DONE}]
  $game_switches[{S_EIGHT_DONE}] = done
  $game_map.need_refresh = true
  if done && !was_done
    pbSEPlay("Anim/HealBell", 90, 100)
    pbMessage(_INTL("All five crossing beds (A2, A3, J, B2, B3) hold as vine bridges! Total Gym hedges: {{1}} (Arena stage {{2}}/5).", $game_variables[{V_HEDGES}], [1 + $game_variables[{V_HEDGES}], 5].min))
  else
    pbMessage(_INTL("Water spreads through the glasshouse! {{1}} is now {{2}}. (Total Gym hedges: {{3}})", "{label}", st_names[cur["{plot_id}"]], $game_variables[{V_HEDGES}]))
  end'''
    else:  # 'bower'
        post_rb = f'''  ok = (cur["M1"] == 2 && cur["M2"] == 3 && cur["M3"] == 2 && cur["M4"] == 3 && cur["M5"] == 2)
  was_ok = $game_switches[{S_BOWER_DONE}]
  $game_switches[{S_BOWER_DONE}] = true if ok
  $game_map.need_refresh = true
  if ok && !was_ok
    pbSEPlay("Anim/HealBell", 95, 105)
    pfm_shake(3, 8, 6) if defined?(pfm_shake)
    pbMessage(_INTL("Bridge — Hedge — Bridge — Hedge — Bridge! The Bride Bower's alternating arch blooms in perfect cadence! The heirloom coffer clicks open!"))
  else
    pbMessage(_INTL("{{1}} grew to {{2}}! (Bower beds: {{3}})", "{label}", st_names[cur["{plot_id}"]], ["M1","M2","M3","M4","M5"].map {{ |k| cur[k] }}.join("-")))
  end'''

    return f'''st_names = {stages_arr}
plots = {tbl_rb}
targets = [{targets_rb}]
on_plot = plots.any? do |pid, _, evs|
  targets.include?(pid) && evs.any? {{ |en| (e = pfp_ev(en)) && e.x == $game_player.x && e.y == $game_player.y }}
end
if on_plot
  pbMessage(_INTL("Step off the vine bridge onto dry stone before watering!"))
else
  cur_st = nil
  plots.each do |pid, s0, evs|
    cur_st = (s0 + pfp_state_of(evs[0])) % 4 if pid == "{plot_id}"
  end
  msg = _INTL("{label} — Stage {{1}} ({{2}}). Neighbours: {nbr_desc}. Water it?", cur_st, st_names[cur_st])
  if pbConfirmMessage(msg)
    pbSEPlay("Anim/Water1", 80, 105)
    cur = {{}}
    plots.each do |pid, s0, evs|
      k = pfp_state_of(evs[0])
      if targets.include?(pid)
        k = (k + 1) % 4
        evs.each {{ |en| pfp_state(en, k) }}
      end
      cur[pid] = (s0 + k) % 4
    end
{post_rb}
  end
end'''


def _check_ruby_syntax(events, label):
    """Compile-check 100% of embedded Ruby scripts in `events` using `ruby -c`."""
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
        assert res.returncode == 0, f'{label}: Ruby syntax error!\n{res.stderr}\n{combined[:1200]}'
    finally:
        os.unlink(tmp_path)


def _ev_active_page(e, vars_, sw, self_sw):
    pages = e.get('pages') or [{}]
    ev_name = e.get('name', '')
    for pg in reversed(pages):
        c = pg.get('cond') or {}
        if 'switch' in c and not sw.get(c['switch'], False):
            continue
        if 'switch2' in c and not sw.get(c['switch2'], False):
            continue
        if 'var' in c and vars_.get(c['var'][0], 0) < c['var'][1]:
            continue
        if 'self' in c and not self_sw.get((ev_name, c['self']), False):
            continue
        return pg
    return None


def _sim_bfs(Lr, events, start, targets, label, vars_=None, sw=None, self_sw=None):
    """Exact Essentials 4-bit directional + tile-event BFS supporting one-hot self-switch plot states!"""
    vars_ = vars_ or {}
    sw = sw or {}
    self_sw = self_sw or {}
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
                pg = _ev_active_page(e, vars_, sw, self_sw)
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


def _verify_over_trigger_and_sightlines(Lr, events, label):
    """Assert ZERO Essentials over_trigger? traps on action signs/events AND 100% unobstructed trainer sightlines!"""
    import build as B
    ts = R.tilesets()[TID]
    H, W = Lr.shape[1:]
    solid_ev = set()
    for e in events:
        if e.get('type') in ('npc', 'trainer', 'mart'):
            solid_ev.add(tuple(e['at']))
        elif e.get('type') == 'event':
            pg0 = (e.get('pages') or [{}])[0]
            g = pg0.get('graphic') or {}
            if g.get('sprite') or (g.get('tile') and (ts['passages'][g['tile']] & 0x0f) == 0x0f):
                solid_ev.add(tuple(e['at']))
    for e in events:
        if e.get('type') == 'sign':
            x, y = e['at']
            assert not B.cell_passable(Lr, ts, x, y), (
                f'{label}: over_trigger? trap! Sign {e.get("name")} at ({x},{y}) sits on a WALKABLE tile!'
            )
        elif e.get('type') == 'event':
            x, y = e['at']
            for idx, pg in enumerate(e.get('pages') or []):
                if pg.get('trigger', 'action') == 'action' and pg.get('commands'):
                    g = pg.get('graphic') or {}
                    if g.get('sprite'):
                        continue
                    tid = g.get('tile')
                    if tid:
                        assert (ts['passages'][tid] & 0x0f) == 0x0f, (
                            f'{label}: over_trigger? trap! Event {e.get("name")} p{idx} at ({x},{y}) has walkable tile {tid} with action commands!'
                        )
                    else:
                        assert not B.cell_passable(Lr, ts, x, y), (
                            f'{label}: over_trigger? trap! Event {e.get("name")} p{idx} at ({x},{y}) has no sprite/tile on walkable cell!'
                        )
        elif e.get('type') == 'trainer':
            tx, ty = e['at']
            d = e['dir']
            sight = e.get('sight', 3)
            dx, dy = {'down': (0, 1), 'up': (0, -1), 'left': (-1, 0), 'right': (1, 0)}[d]
            for step in range(1, sight + 1):
                cx, cy = tx + dx * step, ty + dy * step
                assert 0 <= cx < W and 0 <= cy < H, f'{label}: Trainer {e["trainer"]} sightline OOB at ({cx},{cy})'
                assert B.cell_passable(Lr, ts, cx, cy) and (cx, cy) not in solid_ev, (
                    f'{label}: Trainer {e["trainer"]} sightline BLOCKED at step {step} ({cx},{cy})!'
                )


def _self_sw_for_stages(room_defs, target_stages):
    """Build self_sw dict for _sim_bfs given desired logical stage per plot ID."""
    ss = {}
    ch_map = {1: 'A', 2: 'B', 3: 'C'}
    for pid, s0, evs in room_defs:
        st = target_stages[pid]
        k = (st - s0) % 4
        if k in ch_map:
            for en in evs:
                ss[(en, ch_map[k])] = True
    return ss


# =================================================================================================
# MAP 290 — VERDANCE GYM - ENTRANCE (TEACH: "Gardens are gossips", 21x17, TS 60)
# =================================================================================================
def build_290():
    W, H = 21, 17
    m = _new_conservatory(W, H, seed=290, wall_kit='cvF2', ter_kit='cvP2')

    # ---- 1. Void-Sculpted Conservatory Foyer Bisected by Clear Turquoise Entrance Canal (y=9) ----
    # North landing (y=2..8 -> wall y=2..3, open marble landing y=4..8)
    m.box(3, 2, 17, 8, FLOOR, '.')
    # Canal strip (y=9, x=3..17)
    m.box(3, 9, 17, 9, FLOOR, '.')
    # South entrance foyer (y=10..14) + EXACT 3-wide south exit bay (x=9..11, y=14..16 -> 0 border pockets!)
    m.box(3, 10, 17, 14, FLOOR, '.')
    m.box(9, 14, 11, 16, FLOOR, '.')
    m.mass_at([(3, 2), (17, 2), (3, 14), (17, 14)])
    m.tidy()
    m.plan_cliffs(rows=2)

    # ---- 2. Events: Exit -> 283, TEACH Canal Plots (P0 & P0N), Juno's Sign, Guide, Healer, Poppy ----
    E = m.events

    # Full-width south exit carpet warps (9..11, 16) -> 283 Glasshouse Ward right outside Gym 9 conservatory door!
    for ex in (9, 10, 11):
        E.append({
            'type': 'warp',
            'name': f'Exit to Glasshouse Ward {ex}',
            'at': [ex, 16],
            'to': {'map': 283, 'x': 24, 'y': 10, 'dir': 'down'},
            'se': 'Door exit',
        })

    # North Portal (10, 4) -> 291 Hedge Garden (14, 22) up
    E.append({
        'type': 'warp',
        'name': 'To Hedge Garden (291)',
        'at': [10, 4],
        'to': {'map': 291, 'x': 14, 'y': 22, 'dir': 'up'},
        'se': 'Door enter',
    })

    # TEACH Plot Definitions: P0 starts at Stage 1 (bright green sprouts), P0N starts at Stage 0 (dark bare soil)!
    defs_290 = [
        ('P0', 1, ['P0_L', 'P0_R']),
        ('P0N', 0, ['P0N_L', 'P0N_R']),
    ]
    water_p0 = _ruby_water_action('P0', 'Entrance Plot P0', defs_290, ['P0N'], '290')
    inspect_p0n = _ruby_plot_inspect('P0N', 'Neighbour Display Bed P0N', 0, 'P0N_L', ['P0'], 'Brass Spigot P0 to the left')

    # P0 spans the entrance canal at (9..10, 9) — 1 watering turns sprouts -> walkable bridge!
    E.append(_plot_tile_event('P0_L', 9, 9, 1, side='L', orient='NS', water_ruby=water_p0))
    E.append(_plot_tile_event('P0_R', 10, 9, 1, side='R', orient='NS', water_ruby=water_p0))
    # Framed Demonstration Neighbour Bed P0N at (13..14, 9) — linked to P0 by glowing aqua floor conduit along y=10!
    # Stone balustrade curb at (13..14, 8) seals its north edge cleanly so it reads intentionally as a display bed (0 bypass)!
    E.append(_plot_tile_event('P0N_L', 13, 9, 0, side='L', orient='NS', water_ruby=inspect_p0n))
    E.append(_plot_tile_event('P0N_R', 14, 9, 0, side='R', orient='NS', water_ruby=inspect_p0n))

    # Solid Brass Watering Spigot for P0 on South Bank (8, 10) -> works at ALL stages 0..3 with 0 over_trigger?!
    E.append(_spigot_event('Spigot P0', 8, 10, water_p0))

    # Juno's Sign mounted on solid pf_signpost at (12, 11..12) -> base (12, 12) pas=0xf (leaves y=10 aqua conduit clear!)
    E.append(_sign(
        "Juno's Sign", (12, 12),
        "JUNO'S SIGN — \"Gardens are gossips. Water one and the neighbours hear about it.\n— J.H., Warden (it still feels weird to write that).\""
    ))

    # Canonical Ch10 Gym Guide (story/28_SCRIPT_CH10.md:533-538)
    E.append(_make_npc('Gym Guide', (6, 13), 'NPC 12', 'right', [
        "Gym Guide: Yo, champ in the making! Welcome to the Heartgarden Gym — Grass-types on a Flower Garden that grows while you fight!",
        "Gym Guide: Fire, Ice, Flying, Poison, and Bug go straight through them. Be honest with yourself about Fire: you'll burn the garden down at full bloom, and that's a strategy.",
        "Gym Guide: Here's the catch — every flowering hedge (Stage 3) you leave behind in the puzzle beds starts Juno's arena garden one stage taller (Stage 1 + hedges, up to Stage 5)!",
        "Gym Guide: Fewer waterings, harder fight. Clean pruning, calmer arena. Your call — she told me to say 'your call'. She feels very strongly about it being your call.",
    ]))

    # Conservatory Botanist Healer (full heal!)
    heal_ruby = '''pbMessage(_INTL("Conservatory Botanist: Pollen thick in the air today? Let me mist your team with Heartgarden springwater!"))
pbFadeOutIn do
  $player.heal_party
  pbMEPlay("Pkmn healing")
  pbWait(0.8)
end
pbMessage(_INTL("Conservatory Botanist: Fresh as dawn petals! Remember: Stage 0 is bare soil, Stage 1 sprouts, Stage 2 a walkable vine bridge, and Stage 3 a flowering rose hedge — watering a hedge collapses it back to soil."))'''
    E.append({
        'type': 'event',
        'name': 'Conservatory Botanist',
        'at': [14, 13],
        'pages': [{
            'graphic': {'sprite': 'NPC 11', 'dir': 'left'},
            'trigger': 'action',
            'move': 'fixed',
            'commands': [{'script': heal_ruby}],
        }],
    })

    # Canonical PBS Trainer #1: [LASS, Poppy] (pbs/trainers.txt:19110 — 4-tile left sightline 100% OPEN!)
    E.append(_trainer(
        (14, 6), 'LASS', 'Poppy', 'left',
        "Lass Poppy: You crossed the teach canal already? Let's see if your team keeps pace with a blooming garden!",
        "Lass Poppy: I only water them. They do the rest. Usually. Go on north into the Hedge Garden!",
        sight=4,
    ))

    # Side pickup on NW garden landing
    E.append({'type': 'item', 'name': 'Item (Hyper Potion)', 'at': [5, 5], 'item': 'HYPERPOTION'})

    # Protect key corridors & arrival cells
    for x in (9, 10, 11):
        for y in range(4, 17):
            m.keep_clear.add((x, y))
    for p in ((8, 10), (7, 10), (12, 11), (12, 12), (11, 12), (10, 6), (11, 6), (12, 6), (13, 6), (14, 6), (5, 5)):
        m.keep_clear.add(p)

    # ---- 3. Sunlit Conservatory Architecture: Windows, Evergreen Banners, Rose Planters, Candelabras ----
    for wx in (6, 8, 12, 14):
        _place_stamp_over(m, 'mn_window_bare', wx, 2, base_z=1, top_z=1, top_rows=0, solid=True)
    for bx in (5, 9, 11, 15):
        _place_stamp_over(m, 'fw_ban_e', bx, 2, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'mn_candelabra', 4, 4, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'mn_candelabra', 16, 4, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'mn_palm', 4, 7, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'mn_palm', 16, 7, base_z=1, top_z=2, top_rows=1, solid=True)
    # Carved stone ornamental balustrade framing demonstration bed P0N on north curb (13..14, 8) — distinct from Stage 1 sprouts!
    m.over.append((1, 13, 8, P1('rw_rail_w')))
    m.over.append((1, 14, 8, P1('rw_rail_e')))
    m.taken[8, 13] = True
    m.taken[8, 14] = True
    _place_stamp_over(m, 'pf_planter0', 5, 10, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'pf_planter2', 15, 10, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'nt_lily', 4, 12, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'nt_lily', 16, 12, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'pf_signpost', 12, 11, base_z=1, top_z=2, top_rows=1, solid=True)  # Juno's Sign solid base (12, 12)!
    # Foyer candelabras cleanly inside south foyer flanking the 3-wide exit bay (0 void bleed!)
    _place_stamp_over(m, 'mn_candelabra', 8, 13, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'mn_candelabra', 12, 13, base_z=1, top_z=2, top_rows=1, solid=True)

    chandeliers_290 = [(9, 11), (9, 5)]
    for cx, cy in chandeliers_290:
        _place_stamp_over(m, 'mn_chandelier', cx, cy, base_z=2, top_z=2, top_rows=2, solid=False)

    m.paint()
    _paint_conservatory_floors(m, [
        (3, 4, 17, 8, 'plaza'),
        (3, 10, 17, 14, 'plaza'),
        (9, 14, 11, 16, 'plaza'),
    ], inlays=[(4, 4, 16, 8), (4, 10, 16, 14)])
    # Glowing aqua irrigation conduit channel visibly linking Spigot P0 (8,10) -> P0 (9..10,9) -> P0N (13..14,9)!
    for cx in (8, 12, 13, 14):
        m.L[0, 10, cx] = T_CONDUIT_H
    _paint_emerald_runner(m, 9, 4, 11, 8, medallion=True)
    _paint_emerald_runner(m, 9, 10, 11, 16, medallion=True)

    # Carve turquoise Entrance Canal across y=9 (x=3..17)
    _paint_canal_water(m, [(x, 9) for x in range(3, 18)])
    # Crisp dark portal pad at North Portal (10, 4); golden-framed 3-wide emerald runner cleanly fills south exit (9..11, 16)!
    m.L[1, 4, 10] = T_PDOOR_OPEN

    # Scatter gentle Bride Tree white petals on open conservatory marble
    for px, py in ((7, 11), (13, 12), (7, 5), (12, 5)):
        if m.L[1, py, px] == 0:
            m.L[1, py, px] = T_PETALS

    Lr = RC.resolve(m.L, TID).astype(np.int32)
    # Crisp diagonal conservatory sunbeams ONLY — ZERO void-bleeding / rug-smearing pf_glow circles!
    _add_safe_overlay(Lr, TID, 'cv_shaft', [(6, 4), (14, 4), (6, 11), (14, 11)])
    _assert_chandeliers_intact(Lr, chandeliers_290, 'Map 290')
    _assert_zero_exit_pockets(Lr, E, 16, 'Map 290')

    ev_pts = [tuple(e['at']) for e in E]
    PG.guard(Lr, TID, ev_pts, 'Map 290')
    assert not PG.hits(Lr, R.tilesets()[TID], ev_pts), 'Map 290 passguard hits!'
    _verify_over_trigger_and_sightlines(Lr, E, 'Map 290')
    _check_ruby_syntax(E, 'Map 290')

    # Multi-state 4-bit Essentials BFS verification:
    seen0 = _sim_bfs(Lr, E, (10, 15), [
        ('Spigot P0', (8, 10), True), ('Juno Sign', (12, 12), True),
        ('Guide', (6, 13), True), ('Healer', (14, 13), True),
    ], 'Map 290 Start (P0=1)')
    assert (10, 4) not in seen0, 'Map 290 BUG: North Portal reachable before watering P0!'

    # Even if P0N reaches Stage 2 while P0 != 2, stone curb (13..14,8) prevents bypass!
    ss_p0n_only = _self_sw_for_stages(defs_290, {'P0': 3, 'P0N': 2})
    seen_nb = _sim_bfs(Lr, E, (10, 15), [], 'Map 290 P0N-only bypass check', self_sw=ss_p0n_only)
    assert (10, 4) not in seen_nb, 'Map 290 BYPASS BUG: North Portal reached via P0N!'

    ss_bridged = _self_sw_for_stages(defs_290, {'P0': 2, 'P0N': 1})
    _sim_bfs(Lr, E, (10, 15), [
        ('North Portal', (10, 4), False), ('Poppy', (14, 6), True), ('Hyper Potion', (5, 5), True),
    ], 'Map 290 Bridged (P0=2, P0N=1)', self_sw=ss_bridged)

    np.save(os.path.join(HERE, 'data', 'raw', '290.npy'), Lr.astype(np.int16))
    spec = {
        'id': 290,
        'name': 'Verdance Gym - Entrance',
        'parent': 283,
        'bgm': 'Gym',
        'field': FIELD,
        'map_audio': {'bgm': 'Gym - Warden Hall', 'bgs': 'Gossamer Deepwood', 'bgs_volume': 25, 'rain': False},
        'metadata': {'Name': 'Verdance Gym', 'SnapEdges': True, 'MapPosition': VERD_POS, 'BattleBack': 'field'},
        'tone': [6, 10, -4, 0],
        'fog': {'name': 'prismfall_spores', 'opacity': 16, 'blend': 1, 'zoom': 100, 'sx': 1, 'sy': 0},
        'biome': 'interior',
        'tileset': TID,
        'raw': 'data/raw/290.npy',
        'events': E,
    }
    with open(os.path.join(HERE, 'specs', '290_verdance_gym.yaml'), 'w', encoding='utf-8') as f:
        f.write('# GENERATED by mapgen/layouts/verdance_gym.py (Batch 3E): Verdance Gym - Entrance (TEACH).\n')
        f.write(yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))
    print('Wrote specs/290_verdance_gym.yaml and data/raw/290.npy')
    return m, Lr


# =================================================================================================
# MAP 291 — VERDANCE GYM - PUZZLE ROOM 1 ("Hedge Garden — Ring of Six", 29x25, TS 60)
# =================================================================================================
def build_291():
    W, H = 29, 25
    m = _new_conservatory(W, H, seed=291, wall_kit='cvF2', ter_kit='cvP2')

    # ---- 1. Sculpt Grand Sunlit Botanical Water-Court Around Central Grand Fountain Island ----
    m.box(2, 2, 26, 22, FLOOR, '.')
    # Exact 3-wide south exit bay (x=13..15, y=22..23 -> 0 border pockets!)
    m.box(13, 22, 15, 23, FLOOR, '.')
    m.mass_at([(2, 2), (26, 2), (2, 22), (26, 22)])
    m.tidy()
    m.plan_cliffs(rows=2)

    # Canonical Ring of Six: Start P1..P6 = [0, 0, 1, 2, 1, 2], Required bridges: P1, P3, P5 = 2!
    # ALL 6 PLOTS GENUINELY BRIDGE TWO REAL DRY STONE BANKS (ZERO floating dead-end rafts in open water!)
    # Clockwise around the grand pf_fountain centerpiece:
    #   P1 (7 o'clock, SW, NS): (10..11, 18) bridges South Promenade <-> SW Island I1 (10..13, 14..17)
    #   P2 (9 o'clock, W,  EW): (5..6, 15)   bridges West Promenade  <-> West Lily Plinth Island G_P2 (7..8, 14..16)
    #   P3 (10 o'clock, NW,NS): (10..11, 13) bridges SW Island I1    <-> Central Fountain Island I2 (10..19, 8..12)
    #   P4 (11 o'clock, NW,EW): (5..6, 9)    bridges West Promenade  <-> NW Rose Gazebo Island G_P4 (7..8, 8..10)
    #   P5 (2 o'clock, NE, NS): (17..18, 7)  bridges Fountain I2     <-> North Exit Dais (12..19, 4..6)
    #   P6 (4 o'clock, E,  EW): (22..23, 14) bridges East Promenade  <-> East Rose Pavilion Island G_P6 (19..21, 14..17)
    defs_291 = [
        ('P1', 0, ['P1_L', 'P1_R']),
        ('P2', 0, ['P2_L', 'P2_R']),
        ('P3', 1, ['P3_L', 'P3_R']),
        ('P4', 2, ['P4_L', 'P4_R']),
        ('P5', 1, ['P5_L', 'P5_R']),
        ('P6', 2, ['P6_L', 'P6_R']),
    ]
    nbrs_291 = {
        'P1': ['P6', 'P2'], 'P2': ['P1', 'P3'], 'P3': ['P2', 'P4'],
        'P4': ['P3', 'P5'], 'P5': ['P4', 'P6'], 'P6': ['P5', 'P1'],
    }
    plot_specs_291 = {
        'P1': (10, 18, 'NS'), 'P2': (5, 15, 'EW'), 'P3': (10, 13, 'NS'),
        'P4': (5, 9, 'EW'),   'P5': (17, 7, 'NS'), 'P6': (22, 14, 'EW'),
    }
    # Every Brass Spigot sits DIRECTLY BESIDE its own plot (or on a dedicated dry stone Valve Pier 1 water tile away!)
    spigot_coords_291 = {
        'P1': (9, 19), 'P2': (4, 14), 'P3': (8, 12),
        'P4': (4, 8),  'P5': (20, 7), 'P6': (24, 13),
    }
    spigot_hints_291 = {
        'P1': 'Brass Spigot P1 beside the SW bridgehead',
        'P2': 'Brass Spigot P2 beside the West bridgehead',
        'P3': 'Brass Spigot P3 on the West Valve Pier',
        'P4': 'Brass Spigot P4 beside the NW bridgehead',
        'P5': 'Brass Spigot P5 on the East Valve Pier',
        'P6': 'Brass Spigot P6 beside the East bridgehead',
    }

    # Define exact turquoise water basin cells (sealing North Dais, I1, I2, and all 3 side gazebos with ZERO bypass!)
    water_291 = set()
    # Main sunken moat x=5..23, y=7..18
    for y in range(7, 19):
        for x in range(5, 24):
            water_291.add((x, y))
    # Seal West & East channels flanking North Dais (12..19, 4..6) so Outer Promenades cannot bypass P5!
    for y in range(4, 7):
        for x in range(5, 12):
            water_291.add((x, y))
        for x in range(20, 24):
            water_291.add((x, y))

    # Carve Dry Interior Islands & Decorative Side-Bank Gazebos + 2 Valve Piers:
    dry_rects_291 = [
        (10, 14, 13, 17),  # SW Island I1 (connects P1 <-> P3)
        (10, 8, 19, 12),   # Central Grand Fountain Island I2 (connects P3 <-> P5, houses pf_fountain 5x4!)
        (7, 14, 8, 16),    # West Lily Plinth Island G_P2 (east bank of P2; water x=9 separates from I1!)
        (7, 8, 8, 10),     # NW Rose Gazebo Island G_P4 (east bank of P4; water x=9 & y=11 separate from I2/Pier!)
        (19, 14, 21, 17),  # East Rose Pavilion Island G_P6 (west bank of P6; water y=13 & x=14..18 separate!)
        (5, 12, 8, 12),    # West Valve Pier for Spigot P3 (water x=9 separates from I2; y=11 & y=13 separate!)
        (20, 7, 23, 7),    # East Valve Pier for Spigot P5 (water x=19 separates from P5; y=6 & y=8 separate!)
    ]
    for x0, y0, x1, y1 in dry_rects_291:
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                water_291.discard((x, y))

    # ---- 2. Events: Warps, 6 Ring Plots + 6 Solid Spigots, Bram, Blueprint Plaque, Clover & Daisy ----
    E = m.events

    # Full-width south return warps (13..15, 23) -> 290 Entrance (10, 5) down
    for ex in (13, 14, 15):
        E.append({
            'type': 'warp',
            'name': f'Back to Entrance {ex}',
            'at': [ex, 23],
            'to': {'map': 290, 'x': 10, 'y': 5, 'dir': 'down'},
            'se': 'Door exit',
        })

    # North Portal (14, 4) -> 292 Glasshouse (14, 22) up (only reachable across P1, P3, P5!)
    E.append({
        'type': 'warp',
        'name': 'To Glasshouse (292)',
        'at': [14, 4],
        'to': {'map': 292, 'x': 14, 'y': 22, 'dir': 'up'},
        'se': 'Door enter',
    })

    # Portal status lamps flanking (14, 4) (light up when S345 G9_RING_DONE is ON!)
    for lx in (13, 15):
        E.append({
            'type': 'event',
            'name': f'Portal Lamp {lx}',
            'at': [lx, 4],
            'pages': [
                {'graphic': {'tile': T_LAMP_OFF}, 'trigger': 'action', 'commands': ['A conservatory ring lamp — it blooms bright when P1, P3, and P5 all hold as vine bridges.']},
                {'cond': {'switch': S_RING_DONE}, 'graphic': {'tile': T_LAMP_ON}, 'trigger': 'action', 'commands': ['The ring lamp shines bright emerald! All three crossing bridges (P1, P3, P5) are woven!']},
            ],
        })

    # Add all 6 Ring Plots (2x1 each = 12 tile events) + 6 Solid Brass Watering Spigots!
    # Watering happens cleanly at the Outer Promenade / Valve Pier Brass Spigots -> 0 island softlocks!
    # Inspecting any impassable plot tile directly reads out its exact stage, neighbours, and Brass Spigot!
    for pid, s0, evs in defs_291:
        px, py, orient = plot_specs_291[pid]
        sx, sy = spigot_coords_291[pid]
        role = 'REQUIRED BRIDGE' if pid in ('P1', 'P3', 'P5') else 'Ring Bed'
        w_ruby = _ruby_water_action(pid, f'Plot {pid} ({role})', defs_291, nbrs_291[pid], '291')
        i_ruby = _ruby_plot_inspect(pid, f'Plot {pid} ({role})', s0, evs[0], nbrs_291[pid], spigot_hints_291[pid])
        E.append(_plot_tile_event(evs[0], px, py, s0, side='L', orient=orient, water_ruby=i_ruby))
        E.append(_plot_tile_event(evs[1], px + 1, py, s0, side='R', orient=orient, water_ruby=i_ruby))
        E.append(_spigot_event(f'Spigot {pid}', sx, sy, w_ruby))

    # Ring Blueprint Plaque (solid pf_signpost at (12, 19..20) -> base (12, 20) pas=0xf!)
    E.append(_sign(
        'Ring of Six Blueprint', (12, 20),
        "HEDGE GARDEN — THE RING OF SIX\nClockwise Ring: P1 (SW) — P2 (W) — P3 (NW Pier) — P4 (NW) — P5 (NE Pier) — P6 (E) — P1.\nFollow the glowing aqua floor conduits to each Brass Spigot! Watering any bed advances it + both ring neighbours (+1 mod 4: 0 Soil -> 1 Sprouts -> 2 Bridge -> 3 Hedge -> 0).\nCrossings needed: P1, P3, P5 = Stage 2. Every Stage 3 Hedge left raises Juno's arena!"
    ))

    # Apprentice Bram (Juno's cousin): Status readout, Reset (w/ on-plot guard!), 3-Tier Hints (V348), puzzleskip (S301)!
    bram_291_ruby = f'''st_n = ["0:Soil", "1:Sprouts", "2:Bridge", "3:Hedge"]
defs = [["P1",0,["P1_L","P1_R"]],["P2",0,["P2_L","P2_R"]],["P3",1,["P3_L","P3_R"]],["P4",2,["P4_L","P4_R"]],["P5",1,["P5_L","P5_R"]],["P6",2,["P6_L","P6_R"]]]
vals = {{}}
defs.each {{ |pid, s0, evs| vals[pid] = (s0 + pfp_state_of(evs[0])) % 4 }}
h291 = vals.values.count(3)
$game_variables[{V_HEDGES_291}] = h291
$game_variables[{V_HEDGES}] = h291 + $game_variables[{V_HEDGES_292}].to_i
summary = defs.map {{ |pid, _, _| "#{{pid}}=#{{vals[pid]}}" }}.join("  ")
cmds = [_INTL("Check beds & hedge count"), _INTL("Ask for a hint"), _INTL("Reset all six beds")]
cmds.push(_INTL("Skip room (Puzzle Skip)")) if $game_switches[{S_PUZZLE_SKIP}]
cmds.push(_INTL("Never mind"))
ch = pbMessage(_INTL("Bram: Juno's cousin, at your service! [#{{summary}}] | Hedges here: {{1}} (Total: {{2}})", h291, $game_variables[{V_HEDGES}]), cmds, cmds.length)
case ch
when 0
  pbMessage(_INTL("Bram: Current stages — P1={{1}}, P2={{2}}, P3={{3}}, P4={{4}}, P5={{5}}, P6={{6}}.", st_n[vals["P1"]], st_n[vals["P2"]], st_n[vals["P3"]], st_n[vals["P4"]], st_n[vals["P5"]], st_n[vals["P6"]]))
  pbMessage(_INTL("Bram: You need P1, P3, and P5 at Stage 2 (Bridge) to cross north. Every Stage 3 Hedge raises Juno's arena Flower Garden stage by +1!"))
when 1
  tier = $game_variables[{V_HINT_291}].to_i
  if tier == 0
    pbMessage(_INTL("Bram (Hint 1/3): Water the plot NEXT to the one you want. Neighbours hear everything along the ring!"))
    $game_variables[{V_HINT_291}] = 1
  elsif tier == 1
    pbMessage(_INTL("Bram (Hint 2/3): P6 is already a bridge — one watering turns it into a hedge (fast, +1 arena stage), while two waterings collapse it cleanly while feeding P1 and P5!"))
    $game_variables[{V_HINT_291}] = 2
  else
    pbMessage(_INTL("Bram (Hint 3/3): From a fresh reset — FAST (2 waterings, 1 hedge): water P2 once, P6 once. CLEAN (5 waterings, 0 hedges): water P4 once, P5 twice, P6 twice!"))
  end
when 2
  on_plot = defs.any? {{ |_, _, evs| evs.any? {{ |en| (e = pfp_ev(en)) && e.x == $game_player.x && e.y == $game_player.y }} }}
  if on_plot
    pbMessage(_INTL("Bram: Step onto dry stone before I prune the beds!"))
  elsif pbConfirmMessage(_INTL("Bram: Want me to prune all six beds back to their starting growth?"))
    defs.each {{ |_, _, evs| evs.each {{ |en| pfp_state(en, 0) }} }}
    $game_variables[{V_HEDGES_291}] = 0
    $game_variables[{V_HEDGES}] = $game_variables[{V_HEDGES_292}].to_i
    $game_switches[{S_RING_DONE}] = false
    $game_map.need_refresh = true
    pbSEPlay("Anim/Water2", 80, 100)
    pbMessage(_INTL("Bram: Done! Fresh start: P1..P6 = 0, 0, 1, 2, 1, 2."))
  end
when 3
  if $game_switches[{S_PUZZLE_SKIP}]
    clean = {{"P1"=>2,"P2"=>0,"P3"=>2,"P4"=>1,"P5"=>2,"P6"=>2}}
    defs.each do |pid, s0, evs|
      k = (clean[pid] - s0) % 4
      evs.each {{ |en| pfp_state(en, k) }}
    end
    $game_variables[{V_HEDGES_291}] = 0
    $game_variables[{V_HEDGES}] = $game_variables[{V_HEDGES_292}].to_i
    $game_switches[{S_RING_DONE}] = true
    $game_map.need_refresh = true
    pbSEPlay("Anim/HealBell", 90, 100)
    pbMessage(_INTL("Bram: Puzzle Skip active! I've pruned the clean zero-hedge bridges (P1, P3, P5) for you."))
  end
end'''
    E.append({
        'type': 'event',
        'name': 'Apprentice Bram',
        'at': [11, 21],
        'pages': [{
            'graphic': {'sprite': 'NPC 05', 'dir': 'up'},
            'trigger': 'action',
            'move': 'fixed',
            'commands': [{'script': bram_291_ruby}],
        }],
    })

    # Canonical PBS Trainers (pbs/trainers.txt:19172 & 19234 — 100% OPEN 4-tile sightlines!)
    E.append(_trainer(
        (21, 21), 'AROMALADY', 'Clover', 'left',
        "Aroma Lady Clover: Smell that? Six beds breathing together — and my team's been waiting for a challenger!",
        "Aroma Lady Clover: The whole garden leaned in to watch that. Mind the hedges if you want an easier fight with Juno!",
        sight=4,
    ))
    E.append(_trainer(
        (18, 12), 'PICNICKER', 'Daisy', 'left',
        "Picnicker Daisy: You made it onto the Fountain Island! Care for a quick match before crossing P5?",
        "Picnicker Daisy: Picnic in the Heartgarden! ...It's allowed. I asked.",
        sight=4,
    ))

    # Bonus pickup tucked on West Promenade NW garden terrace
    E.append({'type': 'item', 'name': 'Item (Full Heal)', 'at': [3, 5], 'item': 'FULLHEAL'})

    # Protect every aisle, spigot, pier, bridgehead, trainer LoS & warp
    for y in range(4, 24):
        for x in (2, 3, 14, 25, 26):
            m.keep_clear.add((x, y))
    for x in range(2, 27):
        for y in (19, 20, 21, 22):
            m.keep_clear.add((x, y))
    for p in ((4, 9), (4, 15), (24, 14), (7, 9), (7, 15), (21, 14), (17, 8), (18, 8), (10, 12), (11, 12)):
        m.keep_clear.add(p)

    # ---- 3. Botanical Conservatory Decor (Windows, Banners, Grand pf_fountain Centerpiece, Lilies, Gazebos) ----
    for wx in (3, 12, 16, 20, 25):
        _place_stamp_over(m, 'mn_window_bare', wx, 2, base_z=1, top_z=1, top_rows=0, solid=True)
    for bx in (4, 13, 15, 19, 24):
        _place_stamp_over(m, 'fw_ban_e', bx, 2, base_z=1, top_z=2, top_rows=1, solid=True)
    # GRAND 5x4 FLORAL FOUNTAIN (`pf_fountain`) crowning Central Island I2 at (12..16, 8..11) — open marble promenade all around!
    _place_stamp_over(m, 'pf_fountain', 12, 8, base_z=1, top_z=2, top_rows=1, solid=True)
    # Symmetrical botanical accents on corners, Dais, I1 & all 3 Decorative Gazebo Islands (ZERO aisle/LoS obstruction!)
    _place_stamp_over(m, 'pf_signpost', 12, 19, base_z=1, top_z=2, top_rows=1, solid=True)  # Blueprint base (12, 20)
    for lx, ly in ((12, 4), (19, 4), (10, 8), (19, 8), (13, 14), (8, 14), (20, 14), (2, 17), (26, 17)):
        _place_stamp_over(m, 'nt_lily', lx, ly, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'mn_bust', 8, 8, base_z=1, top_z=2, top_rows=1, solid=True)        # NW Rose Gazebo sculpture!
    _place_stamp_over(m, 'pf_stonebench', 19, 17, base_z=1, top_z=1, top_rows=0, solid=True) # East Rose Pavilion bench!
    for cx, cy in ((2, 20), (26, 20), (2, 4), (26, 4)):
        _place_stamp_over(m, 'mn_candelabra', cx, cy, base_z=1, top_z=2, top_rows=1, solid=True)

    chandeliers_291 = [(13, 20), (13, 5)]
    for cx, cy in chandeliers_291:
        _place_stamp_over(m, 'mn_chandelier', cx, cy, base_z=2, top_z=2, top_rows=2, solid=False)

    m.paint()
    _paint_conservatory_floors(m, [
        (2, 4, 26, 22, 'plaza'),
        (13, 22, 15, 23, 'plaza'),
        (10, 8, 19, 12, 'pave'),
        (10, 14, 13, 17, 'pave'),
        (7, 14, 8, 16, 'pave'),
        (7, 8, 8, 10, 'pave'),
        (19, 14, 21, 17, 'pave'),
        (5, 12, 8, 12, 'pave'),
        (20, 7, 23, 7, 'pave'),
    ], inlays=[(12, 4, 19, 6), (10, 8, 19, 12), (10, 14, 13, 17)])
    _paint_emerald_runner(m, 13, 20, 15, 23, medallion=True)
    _paint_emerald_runner(m, 13, 4, 15, 6, medallion=False)
    _paint_canal_water(m, water_291)

    # Glowing aqua irrigation conduit channels visibly connecting EVERY Brass Spigot straight to its plot!
    for cx, cy, t_c in (
        # Spigot P1 (9,19) -> P1 (10..11, 18)
        (9, 19, T_CONDUIT_H), (10, 19, T_CONDUIT_H),
        # Spigot P2 (4,14) -> P2 (5..6, 15)
        (4, 14, T_CONDUIT_V), (4, 15, T_CONDUIT_V),
        # West Valve Pier conduit leading into Spigot P3 (8,12) pointing straight at P3 (10..11, 13)!
        (4, 12, T_CONDUIT_H), (5, 12, T_CONDUIT_H), (6, 12, T_CONDUIT_H), (7, 12, T_CONDUIT_H),
        # Spigot P4 (4,8) -> P4 (5..6, 9)
        (4, 8, T_CONDUIT_V), (4, 9, T_CONDUIT_V),
        # East Valve Pier conduit leading into Spigot P5 (20,7) pointing straight at P5 (17..18, 7)!
        (21, 7, T_CONDUIT_H), (22, 7, T_CONDUIT_H), (23, 7, T_CONDUIT_H), (24, 7, T_CONDUIT_H),
        # Spigot P6 (24,13) -> P6 (22..23, 14)
        (24, 13, T_CONDUIT_V), (24, 14, T_CONDUIT_V),
    ):
        m.L[0, cy, cx] = t_c

    # Portal pad at North Portal (14, 4); clean symmetrical 3-wide emerald runner terminates at south exit (13..15, 23)!
    m.L[1, 4, 14] = T_PDOOR_OPEN

    # Scatter gentle petals on islands & gazebos
    for px, py in ((11, 16), (11, 11), (17, 11), (7, 16), (7, 10), (20, 16), (7, 21), (22, 20), (16, 5)):
        if m.cls[py, px] == '.' and m.L[1, py, px] == 0:
            m.L[1, py, px] = T_PETALS

    Lr = RC.resolve(m.L, TID).astype(np.int32)
    # Crisp conservatory sunlight shafts ONLY — ZERO detached / void-bleeding pf_glow blobs!
    _add_safe_overlay(Lr, TID, 'cv_shaft', [(12, 4), (16, 4), (10, 9), (17, 9), (11, 15), (14, 20)])
    _assert_chandeliers_intact(Lr, chandeliers_291, 'Map 291')
    _assert_zero_exit_pockets(Lr, E, 23, 'Map 291')

    ev_pts = [tuple(e['at']) for e in E]
    PG.guard(Lr, TID, ev_pts, 'Map 291')
    assert not PG.hits(Lr, R.tilesets()[TID], ev_pts), 'Map 291 passguard hits!'
    _verify_over_trigger_and_sightlines(Lr, E, 'Map 291')
    _check_ruby_syntax(E, 'Map 291')

    # Multi-state 4-bit Essentials BFS proof:
    # 1. Start state: ALL 6 Spigots + Bram + Clover + Blueprint + Full Heal + G_P4 (via P4=2) + G_P6 (via P6=2) reachable; Portal BLOCKED!
    seen_start = _sim_bfs(Lr, E, (14, 22), [
        ('Spigot P1', spigot_coords_291['P1'], True),
        ('Spigot P2', spigot_coords_291['P2'], True),
        ('Spigot P3', spigot_coords_291['P3'], True),
        ('Spigot P4', spigot_coords_291['P4'], True),
        ('Spigot P5', spigot_coords_291['P5'], True),
        ('Spigot P6', spigot_coords_291['P6'], True),
        ('G_P4 Bank', (7, 9), False), ('G_P6 Bank', (21, 14), False),
        ('Bram', (11, 21), True), ('Clover', (21, 21), True), ('Full Heal', (3, 5), True),
    ], 'Map 291 Start')
    assert (14, 4) not in seen_start, 'Map 291 BUG: North Portal reachable at Start!'

    # 2. Negative bypass proofs: if ANY of P1, P3, P5 != 2 (even with P2=P4=P6=2!), Portal MUST be unreachable!
    for missing_p in ('P1', 'P3', 'P5'):
        st_bad = {p: 2 for p in ('P1', 'P2', 'P3', 'P4', 'P5', 'P6')}
        st_bad[missing_p] = 3
        s_bad = _sim_bfs(Lr, E, (14, 22), [], f'Map 291 No-{missing_p}', self_sw=_self_sw_for_stages(defs_291, st_bad))
        assert (14, 4) not in s_bad, f'Map 291 BYPASS BUG: North Portal reached without {missing_p}!'

    # 3. Cheapest 2-watering solution (P2x1, P6x1 -> 2,1,2,2,2,3 = 1 hedge): Portal & Daisy REACHABLE!
    ss_cheap = _self_sw_for_stages(defs_291, {'P1': 2, 'P2': 1, 'P3': 2, 'P4': 2, 'P5': 2, 'P6': 3})
    _sim_bfs(Lr, E, (14, 22), [('North Portal', (14, 4), False), ('Daisy', (18, 12), True)],
             'Map 291 Cheapest (2w, 1 hedge)', self_sw=ss_cheap)

    # 4. Clean 5-watering solution (P4x1, P5x2, P6x2 -> 2,0,2,1,2,2 = 0 hedges): Portal & Daisy REACHABLE!
    ss_clean = _self_sw_for_stages(defs_291, {'P1': 2, 'P2': 0, 'P3': 2, 'P4': 1, 'P5': 2, 'P6': 2})
    _sim_bfs(Lr, E, (14, 22), [('North Portal', (14, 4), False), ('Daisy', (18, 12), True)],
             'Map 291 Clean (5w, 0 hedges)', self_sw=ss_clean)

    # 5. All-bridges-2 test: verify ALL 3 decorative gazebos (G_P2, G_P4, G_P6) are physically reached across P2, P4, P6!
    ss_all2 = _self_sw_for_stages(defs_291, {p: 2 for p in ('P1', 'P2', 'P3', 'P4', 'P5', 'P6')})
    _sim_bfs(Lr, E, (14, 22), [
        ('G_P2 Bank', (7, 15), False), ('G_P4 Bank', (7, 9), False), ('G_P6 Bank', (21, 14), False),
        ('North Portal', (14, 4), False),
    ], 'Map 291 All-6-Bridged Bank Proof', self_sw=ss_all2)

    np.save(os.path.join(HERE, 'data', 'raw', '291.npy'), Lr.astype(np.int16))
    spec = {
        'id': 291,
        'name': 'Verdance Gym - Puzzle Room 1',
        'parent': 290,
        'bgm': 'Gym',
        'field': FIELD,
        'map_audio': {'bgm': 'Gym - Warden Hall', 'bgs': 'Gossamer Deepwood', 'bgs_volume': 25, 'rain': False},
        'metadata': {'Name': 'Verdance Gym', 'SnapEdges': True, 'MapPosition': VERD_POS, 'BattleBack': 'field'},
        'tone': [6, 10, -4, 0],
        'fog': {'name': 'prismfall_spores', 'opacity': 16, 'blend': 1, 'zoom': 100, 'sx': 1, 'sy': 0},
        'biome': 'interior',
        'tileset': TID,
        'raw': 'data/raw/291.npy',
        'events': E,
    }
    with open(os.path.join(HERE, 'specs', '291_verdance_gym_291.yaml'), 'w', encoding='utf-8') as f:
        f.write('# GENERATED by mapgen/layouts/verdance_gym.py (Batch 3E): Verdance Gym - Puzzle Room 1 (Hedge Garden).\n')
        f.write(yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))
    print('Wrote specs/291_verdance_gym_291.yaml and data/raw/291.npy')
    return m, Lr


# =================================================================================================
# MAP 292 — VERDANCE GYM - PUZZLE ROOM 2 ("Glasshouse — Figure-Eight + Bride Bower", 29x25, TS 60)
# =================================================================================================
def build_292():
    W, H = 29, 25
    m = _new_conservatory(W, H, seed=292, wall_kit='cvP2', ter_kit='cvF2')

    # ---- 1. Sculpt Rose-and-Emerald Glasshouse Water-Court + NW Bride Bower Mastery Alcove ----
    m.box(2, 2, 26, 22, FLOOR, '.')
    # Exact 3-wide south exit bay (x=13..15, y=22..23 -> 0 border pockets!)
    m.box(13, 22, 15, 23, FLOOR, '.')
    m.mass_at([(2, 2), (26, 2), (2, 22), (26, 22)])
    m.tidy()
    m.plan_cliffs(rows=2)

    # Canonical Figure-Eight: J=1; A1..A4=[0,3,1,2]; B1..B4=[2,0,3,1]; Required bridges: J, A2, A3, B2, B3 = 2!
    defs_292 = [
        ('J',  1, ['J_L',  'J_R']),
        ('A1', 0, ['A1_L', 'A1_R']),
        ('A2', 3, ['A2_L', 'A2_R']),
        ('A3', 1, ['A3_L', 'A3_R']),
        ('A4', 2, ['A4_L', 'A4_R']),
        ('B1', 2, ['B1_L', 'B1_R']),
        ('B2', 0, ['B2_L', 'B2_R']),
        ('B3', 3, ['B3_L', 'B3_R']),
        ('B4', 1, ['B4_L', 'B4_R']),
    ]
    nbrs_292 = {
        'J':  ['A1', 'A4', 'B1', 'B4'],
        'A1': ['J', 'A2'], 'A2': ['A1', 'A3'], 'A3': ['A2', 'A4'], 'A4': ['A3', 'J'],
        'B1': ['J', 'B2'], 'B2': ['B1', 'B3'], 'B3': ['B2', 'B4'], 'B4': ['B3', 'J'],
    }
    # ALL 9 PLOTS GENUINELY BRIDGE TWO REAL DRY STONE BANKS (ZERO floating disconnected rafts in open lake!)
    # Required 5-bridge sequential path:
    #   A2 (9..10, 19, NS) -> SW Ring-A Island I_A1 (9..11, 14..18) -> A3 (9..10, 13, NS)
    #   -> NW Ring-A Island I_A2 (9..12, 10..12) -> J (13..14, 11, EW)
    #   -> Center-East Ring-B Island I_B1 (15..17, 10..13) -> B2 (18..19, 11, EW)
    #   -> East Ring-B Island I_B2 (20..21, 9..14) -> B3 (20..21, 8, NS) -> North Arena Dais (13..21, 4..7)!
    # 4 Free Ring Beds — each bridging Outer Promenade <-> dedicated Decorative Side-Bank Island (ZERO bypasses!):
    #   A1 (5..6, 16, EW):   West Prom <-> SW Lily Plinth G_A1 (7, 15..17) [water x=8 separates from I_A1!]
    #   A4 (5..6, 11, EW):   West Prom <-> NW Lily Plinth G_A4 (7, 10..11) [water x=8 & y=12 separate!]
    #   B1 (15..16, 19, NS): South Prom <-> SE Central Rose Terrace G_B1 (15..17, 16..18) [water y=14..15 & x=14 separate!]
    #   B4 (22..23, 17, EW): East Prom <-> SE East Lily Gazebo G_B4 (19..21, 16..18) [water y=15 & x=18 separate!]
    plot_specs_292 = {
        'J':  (13, 11, 'EW'),
        'A1': (5, 16, 'EW'),  'A2': (9, 19, 'NS'),  'A3': (9, 13, 'NS'),  'A4': (5, 11, 'EW'),
        'B1': (15, 19, 'NS'), 'B2': (18, 11, 'EW'), 'B3': (20, 8, 'NS'),  'B4': (22, 17, 'EW'),
    }
    # Every Brass Spigot sits DIRECTLY BESIDE its plot or at the tip of a dedicated conduit-lined Valve Pier!
    # Central Aqueduct Pier (x=13, y=13..19) brings Spigot J (13,13) right into the heart of the Figure-Eight!
    spigot_coords_292 = {
        'J':  (13, 13),
        'A1': (4, 15),  'A2': (8, 20),  'A3': (7, 13),  'A4': (4, 10),
        'B1': (17, 20), 'B2': (23, 11), 'B3': (23, 8),  'B4': (24, 16),
    }
    spigot_hints_292 = {
        'J':  'Central Brass Spigot J on the Aqueduct Pier',
        'A1': 'Brass Spigot A1 beside the SW bridgehead',
        'A2': 'Brass Spigot A2 beside the South-West bridgehead',
        'A3': 'Brass Spigot A3 on the West Valve Pier',
        'A4': 'Brass Spigot A4 beside the NW bridgehead',
        'B1': 'Brass Spigot B1 beside the South-East bridgehead',
        'B2': 'Brass Spigot B2 on the East Valve Pier',
        'B3': 'Brass Spigot B3 on the North-East Valve Pier',
        'B4': 'Brass Spigot B4 beside the SE bridgehead',
    }

    # Bride Bower Mastery Alcove (NW off North Arena Dais, x=2..12, y=4..7):
    # P0-1 ZERO-SOFTLOCK ARCHITECTURE:
    #   Pure observational floral arch bed M1..M5 at (5..9, 4), separated from dry marble walkway (3..12, 6)
    #   by a crystal turquoise reflecting rill (5..9, 5)! Watered strictly via directly opposite Bower Spigots (5..9, 7)!
    #   Player can NEVER stand on M1..M5 -> MATHEMATICALLY 0 SOFTLOCKS!
    defs_bw = [
        ('M1', 0, ['M1_C']), ('M2', 2, ['M2_C']), ('M3', 1, ['M3_C']), ('M4', 3, ['M4_C']), ('M5', 1, ['M5_C']),
    ]
    nbrs_bw = {'M1': ['M2'], 'M2': ['M1', 'M3'], 'M3': ['M2', 'M4'], 'M4': ['M3', 'M5'], 'M5': ['M4']}

    # Carve turquoise water basin (sealing North Dais, Bride Bower, 4 chain islands, 4 decorative islands & 4 valve piers!)
    water_292 = set()
    # Main Figure-Eight water court: x=5..23, y=8..19
    for y in range(8, 20):
        for x in range(5, 24):
            water_292.add((x, y))
    # Seal Bride Bower South edge (x=2..4, y=8..9) so West Promenade (y=10..20) CANNOT bypass into Bride Bower!
    for y in (8, 9):
        for x in range(2, 5):
            water_292.add((x, y))
    # Seal East Moat flanking North Arena Dais (x=22..23, y=4..7) so East Promenade CANNOT bypass B3!
    for y in range(4, 8):
        for x in (22, 23):
            water_292.add((x, y))
    # Bride Bower observational floral trough (5..9, 4) + crystal reflecting rill (5..9, 5) — 100% impassable barrier!
    for x in range(5, 10):
        water_292.add((x, 4))
        water_292.add((x, 5))

    # Carve Dry Interior Islands, Decorative Side-Bank Islands & Conduit Valve Piers (0 bypasses!):
    dry_rects_292 = [
        # 4 Required-Chain Islands:
        (9, 14, 11, 18),    # SW Ring-A Island I_A1 (connects A2 <-> A3; Lavender at (11,16) left sight=2!)
        (9, 10, 12, 12),    # NW Ring-A Island I_A2 (connects A3 <-> J)
        (15, 10, 17, 13),   # Center-East Ring-B Island I_B1 (connects J <-> B2; Flora at (16,13) up sight=3!)
        (20, 9, 21, 14),    # East Ring-B Island I_B2 (connects B2 <-> B3)
        # 4 Decorative Side-Bank Islands anchoring A1, A4, B1, B4 (water-separated -> 0 bypasses!):
        (7, 15, 7, 17),     # SW Lily Plinth G_A1 (east bank of A1; water x=8 separates from I_A1!)
        (7, 10, 7, 11),     # NW Lily Plinth G_A4 (east bank of A4; water x=8 & y=12 separate!)
        (15, 16, 17, 18),   # SE Central Rose Terrace G_B1 (north bank of B1; water y=14..15, x=14, x=18 separate!)
        (19, 16, 21, 18),   # SE East Lily Gazebo G_B4 (west bank of B4; water y=15, x=18, y=19 separate!)
        # 4 Dedicated Dry Stone Conduit Valve Piers (water-separated -> 0 bypasses!):
        (5, 13, 7, 13),     # West Valve Pier for Spigot A3 (7, 13) [water x=8, y=12, y=14 separate!]
        (13, 13, 13, 19),   # Central Stone Aqueduct Pier for Spigot J (13, 13) [water x=12, x=14, y=12 separate!]
        (23, 11, 23, 11),   # East Valve Pier for Spigot B2 (23, 11) [water x=22 separates from I_B2!]
        (23, 8, 23, 8),     # NE Valve Pier for Spigot B3 (23, 8) [water x=22 separates from B3 & Dais!]
    ]
    for x0, y0, x1, y1 in dry_rects_292:
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                water_292.discard((x, y))

    # ---- 2. Events: Warps, 9 Figure-Eight Plots/Spigots, 5 Observational Bride Bower Plots/Spigots, Bram, Trainers ----
    E = m.events

    # Full-width south return warps (13..15, 23) -> 291 Hedge Garden (14, 5) down
    for ex in (13, 14, 15):
        E.append({
            'type': 'warp',
            'name': f'Back to Hedge Garden {ex}',
            'at': [ex, 23],
            'to': {'map': 291, 'x': 14, 'y': 5, 'dir': 'down'},
            'se': 'Door exit',
        })

    # North Arena Portal (14, 4) -> 293 Warden Arena (10, 15) up (also syncs V347 & V345 as belt-and-suspenders!)
    arena_portal_ruby = f'''defs = [["J",1,["J_L","J_R"]],["A1",0,["A1_L","A1_R"]],["A2",3,["A2_L","A2_R"]],["A3",1,["A3_L","A3_R"]],["A4",2,["A4_L","A4_R"]],["B1",2,["B1_L","B1_R"]],["B2",0,["B2_L","B2_R"]],["B3",3,["B3_L","B3_R"]],["B4",1,["B4_L","B4_R"]]]
h292 = defs.count {{ |_, s0, evs| ((s0 + pfp_state_of(evs[0])) % 4) == 3 }}
$game_variables[{V_HEDGES_292}] = h292
$game_variables[{V_HEDGES}] = $game_variables[{V_HEDGES_291}].to_i + h292
pbSEPlay("Door enter", 80, 100)
pbFadeOutIn do
  $game_temp.player_new_map_id = 293
  $game_temp.player_new_x = 10
  $game_temp.player_new_y = 15
  $game_temp.player_new_direction = 8
  $scene.transfer_player
end'''
    E.append({
        'type': 'event',
        'name': 'To Warden Arena (293)',
        'at': [14, 4],
        'pages': [{
            'trigger': 'touch',
            'through': True,
            'commands': [{'script': arena_portal_ruby}],
        }],
    })

    # Portal status lamps flanking (14, 4)
    for lx in (13, 15):
        E.append({
            'type': 'event',
            'name': f'Arena Portal Lamp {lx}',
            'at': [lx, 4],
            'pages': [
                {'graphic': {'tile': T_LAMP_OFF}, 'trigger': 'action', 'commands': ['An arena lantern — it lights up once all five Figure-Eight bridges (A2, A3, J, B2, B3) are woven.']},
                {'cond': {'switch': S_EIGHT_DONE}, 'graphic': {'tile': T_LAMP_ON}, 'trigger': 'action', 'commands': ['The arena lantern gleams gold! Warden Juno awaits beyond the rose-glass archway!']},
            ],
        })

    # Add all 9 Figure-Eight Plots (18 tile events) + 9 Solid Brass Watering Spigots!
    # Watering happens strictly from permanently connected Outer Promenade / Valve Pier Spigots -> 0 island softlocks!
    for pid, s0, evs in defs_292:
        px, py, orient = plot_specs_292[pid]
        sx, sy = spigot_coords_292[pid]
        role = 'REQUIRED BRIDGE' if pid in ('J', 'A2', 'A3', 'B2', 'B3') else 'Ring Bed'
        w_ruby = _ruby_water_action(pid, f'Plot {pid} ({role})', defs_292, nbrs_292[pid], '292')
        i_ruby = _ruby_plot_inspect(pid, f'Plot {pid} ({role})', s0, evs[0], nbrs_292[pid], spigot_hints_292[pid])
        E.append(_plot_tile_event(evs[0], px, py, s0, side='L', orient=orient, water_ruby=i_ruby))
        E.append(_plot_tile_event(evs[1], px + 1, py, s0, side='R', orient=orient, water_ruby=i_ruby))
        E.append(_spigot_event(f'Spigot {pid}', sx, sy, w_ruby))

    # Optional Mastery: THE BRIDE BOWER (pure observational bed M1..M5 at (5..9, 4) across reflecting rill (5..9, 5)!)
    # Watered strictly from directly opposite Brass Bower Spigots (5..9, 7) -> 0 softlocks across ALL 4^5 states!
    for idx, (pid, s0, evs) in enumerate(defs_bw):
        bx = 5 + idx
        w_bw = _ruby_water_action(pid, f'Bride Bower {pid}', defs_bw, nbrs_bw[pid], 'bower')
        E.append(_plot_tile_event(evs[0], bx, 4, s0, side='C', orient='EW', water_ruby=None))
        E.append(_spigot_event(f'Bower Spigot {pid}', bx, 7, w_bw))

    bower_reset_ruby = '''bw_evs = ["M1_C","M2_C","M3_C","M4_C","M5_C"]
on_plot = bw_evs.any? { |en| (e = pfp_ev(en)) && e.x == $game_player.x && e.y == $game_player.y }
if on_plot
  pbMessage(_INTL("Step onto dry stone before resetting the Bride Bower beds!"))
elsif pbConfirmMessage(_INTL("Bower Pruning Valve — Reset the five Bride Bower beds (M1..M5) back to 0-2-1-3-1?"))
  bw_evs.each { |en| pfp_state(en, 0) }
  $game_map.need_refresh = true
  pbSEPlay("Anim/Water2", 80, 100)
  pbMessage(_INTL("The five Bride Bower beds return to their starting pattern (0-2-1-3-1)."))
end'''
    E.append(_spigot_event('Bride Bower Reset Valve', 10, 7, bower_reset_ruby, tile=T_SPIGOT_ALT))

    E.append(_sign(
        'Bride Bower Plaque', (11, 5),
        "THE BRIDE BOWER (OPTIONAL MASTERY) — Five observational beds across the reflecting pool (M1–M5), each linked only to left and right.\nTurn the five matching brass valves along the south curb to braid 2-3-2-3-2 (Bridge — Hedge — Bridge — Hedge — Bridge), Aunt Elin's bridal arch.\nHedges grown here are for remembrance — they NEVER raise Juno's arena stage!"
    ))

    # P0-3 FIX: Verified existing SE "Anim/HealBell" (pbReceiveItem already plays official Audio/ME/Item get fanfare!)
    bower_chest_ruby = f'''if $game_switches[{S_BOWER_DONE}]
  pbSEPlay("Anim/HealBell", 85, 110)
  pbMessage(_INTL("Inside the heirloom coffer lies a single pressed white petal from the Bride Tree, still cool with morning dew."))
  pbReceiveItem(:TELLURICSEED, 2)
  pbReceiveItem(:MIRACLESEED)
  pbReceiveItem(:GRASSYSEED)
  pbMessage(_INTL("A note in Rowan's neat gardener's hand reads: 'For whoever braided the arch properly — Elin planted hers in twos and threes so the bees had both path and shelter.'"))
  $game_self_switches[[292, @event_id, "A"]] = true
  $game_map.need_refresh = true
else
  pbMessage(_INTL("A rose-carved heirloom coffer, sealed tight. Braid the five Bride Bower beds into 2-3-2-3-2 (Bridge-Hedge-Bridge-Hedge-Bridge) to unlatch it."))
end'''
    E.append({
        'type': 'event',
        'name': 'Bride Bower Coffer',
        'at': [3, 5],
        'pages': [
            {'graphic': {'tile': T_CHEST_SHUT}, 'trigger': 'action', 'commands': [{'script': bower_chest_ruby}]},
            {'cond': {'self': 'A'}, 'graphic': {'tile': T_CHEST_OPEN}, 'trigger': 'action',
             'commands': ["The heirloom coffer stands open, scented faintly with Bride Tree blossom."]},
        ],
    })

    # Figure-Eight Blueprint Plaque (solid pf_signpost at (11, 20..21) -> base (11, 21) pas=0xf, leaves Aqueduct Pier (13,20) wide open!)
    E.append(_sign(
        'Figure-Eight Blueprint', (11, 21),
        "GLASSHOUSE — TWO RINGS, ONE HEART\nRing A (West): J — A1 — A2 — A3 — A4 — J.\nRing B (East): J — B1 — B2 — B3 — B4 — J.\nWalk north along the central aqua conduit pier to reach Junction Spigot J (linked to A1, A4, B1, B4)! Crossings needed: A2, A3, J, B2, B3 = Stage 2."
    ))

    # Apprentice Bram in 292 (story/28_SCRIPT_CH10.md:540-541 + status/reset/3-tier hints/puzzleskip!)
    bram_292_ruby = f'''defs = [["J",1,["J_L","J_R"]],["A1",0,["A1_L","A1_R"]],["A2",3,["A2_L","A2_R"]],["A3",1,["A3_L","A3_R"]],["A4",2,["A4_L","A4_R"]],["B1",2,["B1_L","B1_R"]],["B2",0,["B2_L","B2_R"]],["B3",3,["B3_L","B3_R"]],["B4",1,["B4_L","B4_R"]]]
vals = {{}}
defs.each {{ |pid, s0, evs| vals[pid] = (s0 + pfp_state_of(evs[0])) % 4 }}
h292 = vals.values.count(3)
$game_variables[{V_HEDGES_292}] = h292
$game_variables[{V_HEDGES}] = $game_variables[{V_HEDGES_291}].to_i + h292
stage = [1 + $game_variables[{V_HEDGES}], 5].min
cmds = [_INTL("Check beds & Arena stage"), _INTL("Ask for a hint"), _INTL("Reset Figure-Eight beds")]
cmds.push(_INTL("Skip room (Puzzle Skip)")) if $game_switches[{S_PUZZLE_SKIP}]
cmds.push(_INTL("Never mind"))
ch = pbMessage(_INTL("Bram: She's my cousin. She used to make me be the bee in games. I'm still the bee. | Hedges here: {{1}}, Total: {{2}} (Arena Stage {{3}}/5)", h292, $game_variables[{V_HEDGES}], stage), cmds, cmds.length)
case ch
when 0
  pbMessage(_INTL("Bram: J={{1}} | Ring A: A1={{2}}, A2={{3}}, A3={{4}}, A4={{5}} | Ring B: B1={{6}}, B2={{7}}, B3={{8}}, B4={{9}}.", vals["J"], vals["A1"], vals["A2"], vals["A3"], vals["A4"], vals["B1"], vals["B2"], vals["B3"], vals["B4"]))
  pbMessage(_INTL("Bram: Crossings needed: A2, A3, J, B2, B3 = Stage 2. Leave hedges if you want fewer waterings, or prune clean to keep Juno's arena calm!"))
when 1
  tier = $game_variables[{V_HINT_292}].to_i
  if tier == 0
    pbMessage(_INTL("Bram (Hint 1/3): Junction J feeds FOUR neighbours (A1, A4, B1, B4). Decide J's waterings first, then balance Ring A and Ring B!"))
    $game_variables[{V_HINT_292}] = 1
  elsif tier == 1
    pbMessage(_INTL("Bram (Hint 2/3): You can solve this in 7 waterings (leaving 2 hedges on A4 & B1) — OR spend just ONE extra watering (8 total) for ZERO hedges!"))
    $game_variables[{V_HINT_292}] = 2
  else
    pbMessage(_INTL("Bram (Hint 3/3): From a fresh reset — FAST (7w, 2 hedges): A1 x2, A3 x1, B1 x1, B3 x1, B4 x2. CLEAN (8w, 0 hedges): J x2, A1 x2, A3 x1, B3 x2, B4 x1!"))
  end
when 2
  on_plot = defs.any? {{ |_, _, evs| evs.any? {{ |en| (e = pfp_ev(en)) && e.x == $game_player.x && e.y == $game_player.y }} }}
  if on_plot
    pbMessage(_INTL("Bram: Step onto dry stone before I prune the beds!"))
  elsif pbConfirmMessage(_INTL("Bram: Reset all nine Figure-Eight beds back to their starting growth?"))
    defs.each {{ |_, _, evs| evs.each {{ |en| pfp_state(en, 0) }} }}
    $game_variables[{V_HEDGES_292}] = 2
    $game_variables[{V_HEDGES}] = $game_variables[{V_HEDGES_291}].to_i + 2
    $game_switches[{S_EIGHT_DONE}] = false
    $game_map.need_refresh = true
    pbSEPlay("Anim/Water2", 80, 100)
    pbMessage(_INTL("Bram: Pruned back to start! J=1; A=[0,3,1,2]; B=[2,0,3,1]."))
  end
when 3
  if $game_switches[{S_PUZZLE_SKIP}]
    clean = {{"J"=>2,"A1"=>0,"A2"=>2,"A3"=>2,"A4"=>1,"B1"=>0,"B2"=>2,"B3"=>2,"B4"=>2}}
    defs.each do |pid, s0, evs|
      k = (clean[pid] - s0) % 4
      evs.each {{ |en| pfp_state(en, k) }}
    end
    $game_variables[{V_HEDGES_292}] = 0
    $game_variables[{V_HEDGES}] = $game_variables[{V_HEDGES_291}].to_i
    $game_switches[{S_EIGHT_DONE}] = true
    $game_map.need_refresh = true
    pbSEPlay("Anim/HealBell", 90, 100)
    pbMessage(_INTL("Bram: Puzzle Skip active! All five Figure-Eight bridges are woven cleanly with zero hedges."))
  end
end'''
    E.append({
        'type': 'event',
        'name': 'Apprentice Bram',
        'at': [9, 21],
        'pages': [{
            'graphic': {'sprite': 'NPC 05', 'dir': 'up'},
            'trigger': 'action',
            'move': 'fixed',
            'commands': [{'script': bram_292_ruby}],
        }],
    })

    # Canonical PBS Trainers (pbs/trainers.txt:19296 & 19358 — 100% OPEN sightlines!)
    E.append(_trainer(
        (11, 16), 'AROMALADY', 'Lavender', 'left',
        "Aroma Lady Lavender: Two rings linked at one heart — steady your breath before you face my Grass-types!",
        "Aroma Lady Lavender: Breathe in. Now out. Now go and win.",
        sight=2,
    ))
    E.append(_trainer(
        (16, 13), 'POKEMONBREEDER', 'Flora', 'up',
        "Pokémon Breeder Flora: Right past the central junction! Let's test your squad against seedlings raised in this glasshouse!",
        "Pokémon Breeder Flora: Raised every one from seed. They'll grow back. Juno's waiting just north!",
        sight=3,
    ))

    # Protect promenades, piers, bridges, Bower aisle & trainer sightlines
    for x in range(2, 27):
        for y in (20, 21, 22):
            m.keep_clear.add((x, y))
    for y in range(10, 21):
        m.keep_clear.add((2, y))
        m.keep_clear.add((3, y))
    for y in range(6, 21):
        m.keep_clear.add((25, y))
        m.keep_clear.add((26, y))
    for x in range(3, 21):
        m.keep_clear.add((x, 6))
    for y in range(13, 21):
        m.keep_clear.add((13, y))

    # ---- 3. Rose-Glass Conservatory Architecture, Lily Plinths & Sun-Lamps ----
    for wx in (4, 8, 12, 16, 20, 25):
        _place_stamp_over(m, 'mn_window_bare', wx, 2, base_z=1, top_z=1, top_rows=0, solid=True)
    for bx in (6, 10, 18, 24):
        _place_stamp_over(m, 'fw_ban_e', bx, 2, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'pf_signpost', 11, 20, base_z=1, top_z=2, top_rows=1, solid=True)   # Blueprint base (11, 21)
    _place_stamp_over(m, 'pf_signpost', 11, 4, base_z=1, top_z=2, top_rows=1, solid=True)    # Bower Plaque base (11, 5)
    for cx, cy in ((2, 20), (26, 20), (2, 4), (17, 4), (26, 4)):
        _place_stamp_over(m, 'mn_candelabra', cx, cy, base_z=1, top_z=2, top_rows=1, solid=True)
    # White lilies framing Bride Bower reflecting rill (4,4) & (10,4), Dais, & decorative side-bank islands!
    for lx, ly in ((4, 4), (10, 4), (2, 6), (12, 4), (19, 4), (19, 16), (11, 14), (26, 18), (2, 18)):
        _place_stamp_over(m, 'nt_lily', lx, ly, base_z=1, top_z=2, top_rows=1, solid=True)
    # 1x1 blooming conservatory orchids on G_A1 (7,15) & G_A4 (7,10) leaving bridge landings (7,16) & (7,11) 100% open!
    _place_stamp_over(m, 'mn_orchid', 7, 15, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'mn_orchid', 7, 10, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'pf_stonebench', 15, 16, base_z=1, top_z=1, top_rows=0, solid=True) # SE Central Rose Terrace bench!

    chandeliers_292 = [(13, 20), (13, 5)]
    for cx, cy in chandeliers_292:
        _place_stamp_over(m, 'mn_chandelier', cx, cy, base_z=2, top_z=2, top_rows=2, solid=False)

    m.paint()
    _paint_conservatory_floors(m, [
        (2, 4, 26, 22, 'plaza'),
        (13, 22, 15, 23, 'plaza'),
        (2, 4, 12, 7, 'pave'),
        (9, 14, 11, 18, 'pave'),
        (9, 10, 12, 12, 'pave'),
        (15, 10, 17, 13, 'pave'),
        (20, 9, 21, 14, 'pave'),
        (7, 15, 7, 17, 'pave'),
        (7, 10, 7, 11, 'pave'),
        (15, 16, 17, 18, 'pave'),
        (19, 16, 21, 18, 'pave'),
        (5, 13, 7, 13, 'pave'),
        (13, 13, 13, 19, 'pave'),
        (23, 11, 23, 11, 'pave'),
        (23, 8, 23, 8, 'pave'),
    ], inlays=[(13, 4, 21, 7), (3, 4, 12, 7)])
    _paint_emerald_runner(m, 13, 20, 15, 23, medallion=True)
    _paint_emerald_runner(m, 13, 4, 15, 6, medallion=False)
    _paint_canal_water(m, water_292)

    # Glowing aqua irrigation conduit channels visibly connecting EVERY Brass Spigot to its matching bed!
    for cx, cy, t_c in (
        # Central Aqueduct Pier leading straight north to Spigot J (13, 13) -> Junction J (13..14, 11)!
        (13, 14, T_CONDUIT_V), (13, 15, T_CONDUIT_V), (13, 16, T_CONDUIT_V),
        (13, 17, T_CONDUIT_V), (13, 18, T_CONDUIT_V), (13, 19, T_CONDUIT_V),
        # West Ring-A conduits: A1, A2, A3 Pier, A4
        (4, 15, T_CONDUIT_V), (4, 16, T_CONDUIT_V),
        (8, 20, T_CONDUIT_H), (9, 20, T_CONDUIT_H),
        (4, 13, T_CONDUIT_H), (5, 13, T_CONDUIT_H), (6, 13, T_CONDUIT_H),
        (4, 10, T_CONDUIT_V), (4, 11, T_CONDUIT_V),
        # East Ring-B conduits: B1, B2 Pier, B3 Pier, B4
        (16, 20, T_CONDUIT_H), (17, 20, T_CONDUIT_H),
        (24, 11, T_CONDUIT_H),
        (24, 8, T_CONDUIT_H),
        (24, 16, T_CONDUIT_V), (24, 17, T_CONDUIT_V),
        # Bride Bower vertical aqua alignment lines linking Bower Spigots (5..9, 7) straight to M1..M5 (5..9, 4)!
        (5, 6, T_CONDUIT_V), (6, 6, T_CONDUIT_V), (7, 6, T_CONDUIT_V), (8, 6, T_CONDUIT_V), (9, 6, T_CONDUIT_V),
    ):
        m.L[0, cy, cx] = t_c

    m.L[1, 4, 14] = T_PDOOR_OPEN
    for px, py in ((4, 6), (10, 6), (10, 11), (16, 11), (10, 17), (16, 17), (20, 17), (16, 21)):
        if m.cls[py, px] == '.' and m.L[1, py, px] == 0:
            m.L[1, py, px] = T_PETALS

    Lr = RC.resolve(m.L, TID).astype(np.int32)
    # Crisp conservatory sunlight shafts ONLY — ZERO void-bleeding / walkway-smearing pf_glow circles!
    _add_safe_overlay(Lr, TID, 'cv_shaft', [(6, 5), (14, 5), (10, 11), (16, 11), (10, 16), (20, 11)])
    _assert_chandeliers_intact(Lr, chandeliers_292, 'Map 292')
    _assert_zero_exit_pockets(Lr, E, 23, 'Map 292')

    ev_pts = [tuple(e['at']) for e in E]
    PG.guard(Lr, TID, ev_pts, 'Map 292')
    assert not PG.hits(Lr, R.tilesets()[TID], ev_pts), 'Map 292 passguard hits!'
    _verify_over_trigger_and_sightlines(Lr, E, 'Map 292')
    _check_ruby_syntax(E, 'Map 292')

    # Multi-state 4-bit Essentials BFS proof:
    # 1. Start state: ALL 9 Spigots + Bram + Blueprint + G_A4 (via A4=2) + G_B1 (via B1=2) reachable; Portal & Bower BLOCKED!
    seen0 = _sim_bfs(Lr, E, (14, 22), [
        (f'Spigot {k}', v, True) for k, v in spigot_coords_292.items()
    ] + [
        ('G_A4 Bank', (7, 11), False), ('G_B1 Bank', (16, 18), False),
        ('Bram', (9, 21), True), ('Blueprint', (11, 21), True),
    ], 'Map 292 Start')
    assert (14, 4) not in seen0, 'Map 292 BUG: Arena Portal reachable at Start!'
    assert (3, 6) not in seen0, 'Map 292 BUG: Bride Bower reachable at Start!'

    # 2. Negative bypass proofs: removing ANY ONE of (A2, A3, J, B2, B3) blocks Arena Portal!
    for req_p in ('A2', 'A3', 'J', 'B2', 'B3'):
        st_bad = {p: 2 for p in ('J', 'A1', 'A2', 'A3', 'A4', 'B1', 'B2', 'B3', 'B4')}
        st_bad[req_p] = 3
        s_bad = _sim_bfs(Lr, E, (14, 22), [], f'Map 292 No-{req_p}', self_sw=_self_sw_for_stages(defs_292, st_bad))
        assert (14, 4) not in s_bad, f'Map 292 BYPASS BUG: Arena Portal reached without {req_p}!'

    # 3. Cheapest 7-watering solution (2 hedges): Portal + Lavender + Flora + ALL Bride Bower spigots, Reset, Plaque & Coffer!
    ss_cheap = _self_sw_for_stages(defs_292, {
        'J': 2, 'A1': 2, 'A2': 2, 'A3': 2, 'A4': 3, 'B1': 3, 'B2': 2, 'B3': 2, 'B4': 0
    })
    seen_cheap = _sim_bfs(Lr, E, (14, 22), [
        ('Arena Portal', (14, 4), False),
        ('Lavender', (11, 16), True),
        ('Flora', (16, 13), True),
        ('Bride Bower Coffer', (3, 5), True),
        ('Bower Spigot M1', (5, 7), True),
        ('Bower Spigot M5', (9, 7), True),
        ('Bower Reset', (10, 7), True),
        ('Bower Plaque', (11, 5), True),
    ], 'Map 292 Cheapest (7w, 2 hedges)', self_sw=ss_cheap)
    # P0-1 PROOF: Player can NEVER step onto ANY Bride Bower bed tile (5..9, 4) even when Stage 2!
    for bx in range(5, 10):
        assert (bx, 4) not in seen_cheap, f'Map 292 SOFTLOCK RISK: Bride Bower bed ({bx},4) is walkable!'

    # 4. Clean 8-watering solution (0 hedges): Portal + Bower REACHABLE!
    ss_clean = _self_sw_for_stages(defs_292, {
        'J': 2, 'A1': 0, 'A2': 2, 'A3': 2, 'A4': 1, 'B1': 0, 'B2': 2, 'B3': 2, 'B4': 2
    })
    _sim_bfs(Lr, E, (14, 22), [('Arena Portal', (14, 4), False), ('Bower Coffer', (3, 5), True)],
             'Map 292 Clean (8w, 0 hedges)', self_sw=ss_clean)

    # 5. All-9-bridged bank connectivity proof: ALL 4 decorative side-bank islands physically reachable across A1, A4, B1, B4!
    ss_all9 = _self_sw_for_stages(defs_292, {p: 2 for p in ('J', 'A1', 'A2', 'A3', 'A4', 'B1', 'B2', 'B3', 'B4')})
    _sim_bfs(Lr, E, (14, 22), [
        ('G_A1 Bank', (7, 16), False), ('G_A4 Bank', (7, 11), False),
        ('G_B1 Bank', (16, 18), False), ('G_B4 Bank', (21, 17), False),
        ('Arena Portal', (14, 4), False),
    ], 'Map 292 All-9-Bridged Bank Proof', self_sw=ss_all9)

    np.save(os.path.join(HERE, 'data', 'raw', '292.npy'), Lr.astype(np.int16))
    spec = {
        'id': 292,
        'name': 'Verdance Gym - Puzzle Room 2',
        'parent': 290,
        'bgm': 'Gym',
        'field': FIELD,
        'map_audio': {'bgm': 'Gym - Warden Hall', 'bgs': 'Gossamer Deepwood', 'bgs_volume': 25, 'rain': False},
        'metadata': {'Name': 'Verdance Gym', 'SnapEdges': True, 'MapPosition': VERD_POS, 'BattleBack': 'field'},
        'tone': [8, 10, -2, 0],
        'fog': {'name': 'prismfall_spores', 'opacity': 18, 'blend': 1, 'zoom': 100, 'sx': 1, 'sy': 0},
        'biome': 'interior',
        'tileset': TID,
        'raw': 'data/raw/292.npy',
        'events': E,
    }
    with open(os.path.join(HERE, 'specs', '292_verdance_gym_292.yaml'), 'w', encoding='utf-8') as f:
        f.write('# GENERATED by mapgen/layouts/verdance_gym.py (Batch 3E): Verdance Gym - Puzzle Room 2 (Glasshouse).\n')
        f.write(yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))
    print('Wrote specs/292_verdance_gym_292.yaml and data/raw/292.npy')
    return m, Lr


# =================================================================================================
# MAP 293 — VERDANCE GYM - WARDEN ARENA (Warden Juno Hale — J3, 21x17, TS 60)
# =================================================================================================
def build_293():
    W, H = 21, 17
    m = _new_conservatory(W, H, seed=293, wall_kit='cvP2', ter_kit='cvF2')

    # ---- 1. Sculpt Sunlit Octagonal Rose-Glass Conservatory Arena Over Turquoise Reflecting Moat ----
    m.box(2, 2, 18, 14, FLOOR, '.')
    # Elevated North Floral Dais (TER): x=6..14, y=2..6 (wall y=2..3, open marble dais y=4..6)
    m.box(6, 2, 14, 6, TER, '.')
    # EXACT 3-wide South Approach Vestibule: x=9..11, y=14..16 (arrival (10,15) up -> 0 border pockets on y=16!)
    m.box(9, 14, 11, 16, FLOOR, '.')
    m.mass_at([(2, 2), (3, 2), (2, 3), (18, 2), (17, 2), (18, 3), (2, 14), (18, 14)])
    # 3-wide White-Marble Staircase descending from Juno's Floral Dais (x=9..11, y=6..7)
    m.stairs(9, 6, w=3, n=2, c='.')
    m.tidy()
    m.plan_cliffs(rows=2)

    # Turquoise reflecting moat framing the outer east/west flanks of the conservatory arena (x=2..4 & x=16..18)
    moat_293 = set()
    for y in range(4, 13):
        for x in (2, 3, 4):
            if m.cls[y, x] == '.' and not m.cliff[y, x]:
                moat_293.add((x, y))
        for x in (16, 17, 18):
            if m.cls[y, x] == '.' and not m.cliff[y, x] and not (y >= 10 and x in (15, 16, 17, 18)):
                moat_293.add((x, y))
    # Also water between dais shoulders and lower ring corners (5,4..7) & (15,4..7)
    for y in range(4, 8):
        for x in (5, 15):
            if m.cls[y, x] == '.' and not m.cliff[y, x]:
                moat_293.add((x, y))

    # ---- 2. Events: Return -> 292, Framed East Fast-Exit Lift -> 290, Warden Juno Hale (J3)! ----
    E = m.events

    # Full-width south return carpet (9..11, 16) -> 292 Glasshouse (14, 5) down
    for rx in (9, 10, 11):
        E.append({
            'type': 'warp',
            'name': f'Back to Glasshouse {rx}',
            'at': [rx, 16],
            'to': {'map': 292, 'x': 14, 'y': 5, 'dir': 'down'},
            'se': 'Door exit',
        })

    # Framed East Fast-Exit Conservatory Lift (16, 13) -> 290 Entrance (10, 14) down!
    E.append({
        'type': 'warp',
        'name': 'Fast-Exit Lift to Entrance (290)',
        'at': [16, 13],
        'to': {'map': 290, 'x': 10, 'y': 14, 'dir': 'down'},
        'se': 'Door slide',
    })
    # Lift Sign on solid pf_signpost (15, 11..12 -> base (15, 12) pas=0xf, readable from non-warp (15, 13)!)
    E.append(_sign(
        'Conservatory Lift Sign', (15, 12),
        "HEARTGARDEN FAST-EXIT LIFT — Step onto the bolted conservatory lift grate directly to the right to ride straight back to the Gym Entrance!"
    ))

    # WARDEN JUNO HALE (story/28_SCRIPT_CH10.md:545-575 + GYM_PUZZLES.md:1206-1210, V345 fieldStage + S347 Mastery!)
    juno_battle_ruby = f'''hedges = $game_variables[{V_HEDGES}].to_i
stage = [1 + hedges, 5].min
if hedges >= 3
  pbMessage(_INTL("Juno: You let it grow? For me? ({{1}} hedges — Flower Garden Stage {{2}}!)", hedges, stage))
  pbMessage(_INTL("Juno: ...That's either kind or tactical and I'm too nervous to ask which."))
elsif hedges == 0
  pbMessage(_INTL("Juno: Not a single hedge left overgrown out there! You really did listen to the guide — Stage 1 it is."))
else
  pbMessage(_INTL("Juno: {{1}} hedge(s) still blooming in the glasshouse — my garden's already at Stage {{2}}!", hedges, stage))
end
pbMessage(_INTL("Juno: I didn't want this seat. I wanted him in it."))
pbMessage(_INTL("Juno: But the city's drowning in flowers and nobody else is coming, so."))
pbMessage(_INTL("Juno: Hi. I'm the Warden of Verdance. Please don't go easy on me — I'll cry either way."))
setBattleRule("fieldStage", stage)
if Prismfall.gym_battle(pfm_gym(:LEADER_JUNO), double: false)
  pbMessage(_INTL("Juno: I'm crying. I said I would."))
  pbMessage(_INTL("Juno: ...Take it. The Meadow Badge is yours."))
  Prismfall.award_badge(pfm_gym(:LEADER_JUNO))
  pbSEPlay("Anim/HealBell", 95, 100)
  pbMessage(_INTL("Nine clear notes ring out from your badge case. Light runs along its seams and doesn't fade — it stays, softly, like a pilot light."))
  pbMessage(_INTL("Juno: It's singing. Mine never sang. I wrote to Uncle Rowan after Briarwick about your case doing a chord — he wrote back: 'That one'll sing in every gym in the realm, Juno, mark me.'"))
  pbReceiveItem(:TM53)
  pbMessage(_INTL("Juno: Energy Ball. It's the first move I ever taught anything. And that badge means Pokémon up to level fifty-one will listen to you — I checked twice!"))
  if $game_switches[{S_BOWER_DONE}]
    pbMessage(_INTL("Juno: ...And Bram told me you braided the Bride Bower's alternating arch too! Aunt Elin planted those five beds in twos and threes every spring. Thank you — really."))
  end
  $game_variables[131] = 9 if $game_variables[131].to_i < 9
  $game_self_switches[[293, @event_id, "A"]] = true
  $game_map.need_refresh = true
end'''
    juno_after_ruby = f'''if $game_switches[{S_BOWER_DONE}]
  pbMessage(_INTL("Juno: You braided the Bride Bower and earned the Meadow Badge fairly. Come visit me under the Bride Tree in the Heartgarden whenever you have a minute!"))
else
  pbMessage(_INTL("Juno: The Meadow Badge is yours — and take the east lift if you want a quick ride straight down to the entrance. Meet me by the Bride Tree in the Heartgarden soon!"))
end'''

    E.append({
        'type': 'event',
        'name': 'Warden Juno Hale',
        'at': [10, 5],
        'pages': [
            {
                'graphic': {'sprite': 'JUNO', 'dir': 'down'},
                'trigger': 'action',
                'move': 'fixed',
                'commands': [{'script': juno_battle_ruby}],
            },
            {
                'cond': {'self': 'A'},
                'graphic': {'sprite': 'JUNO', 'dir': 'down'},
                'trigger': 'action',
                'move': 'fixed',
                'commands': [{'script': juno_after_ruby}],
            },
        ],
    })

    for y in range(4, 17):
        for x in (9, 10, 11):
            m.keep_clear.add((x, y))
    for p in ((14, 13), (15, 13), (16, 13), (15, 12), (16, 12)):
        m.keep_clear.add(p)

    # ---- 3. Sunlit Rose-Glass Conservatory Architecture, Symmetrical Columns, Braziers & Framed Lift ----
    # Center Rose Oculus directly above Juno's Floral Dais (9..10, 2..3), flanked by sunlit windows & Evergreen banners!
    _place_stamp_over(m, 'mn_oculus', 9, 2, base_z=1, top_z=1, top_rows=0, solid=True)
    for wx in (7, 13):
        _place_stamp_over(m, 'mn_window_bare', wx, 2, base_z=1, top_z=1, top_rows=0, solid=True)
    for bx in (8, 12):
        _place_stamp_over(m, 'fw_ban_e', bx, 2, base_z=1, top_z=2, top_rows=1, solid=True)
    # Dais framing: white Bride-Tree lilies & golden candelabras
    _place_stamp_over(m, 'nt_lily', 7, 4, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'nt_lily', 13, 4, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'mn_candelabra', 6, 4, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'mn_candelabra', 14, 4, base_z=1, top_z=2, top_rows=1, solid=True)

    # Framed East Fast-Exit Lift Bay: solid lm_sdoor (16, 11..12) + pf_signpost (15, 11..12) + matching candelabra & white lily!
    # (Replaces jarring yellow street bollards with harmonious conservatory decor!)
    _place_stamp_over(m, 'lm_sdoor', 16, 11, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'pf_signpost', 15, 11, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'mn_candelabra', 17, 11, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'nt_lily', 17, 13, base_z=1, top_z=2, top_rows=1, solid=True)

    # P0-1 FIX: ALL 3 Marble Columns (6,8..9), (14,8..9), (6,11..12) stand 100% WHOLE & UN-CHOPPED — ZERO planter overlap!
    cols_293 = [(6, 8), (14, 8), (6, 11)]
    for cx, cy in cols_293:
        _place_stamp_over(m, 'nr_col', cx, cy, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'pf_planter0', 5, 10, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'pf_planter2', 14, 10, base_z=1, top_z=1, top_rows=0, solid=True)
    # 4 Intact Ceremonial Braziers (south pair cleanly on (8,13)/(12,13) flanking the exact 3-wide exit bay!)
    braziers_293 = [(7, 8), (13, 8), (8, 13), (12, 13)]
    for bx, by in braziers_293:
        _place_stamp_over(m, 'fw_brazier', bx, by, base_z=1, top_z=2, top_rows=1, solid=True)
    chandeliers_293 = [(9, 9)]
    for cx, cy in chandeliers_293:
        _place_stamp_over(m, 'mn_chandelier', cx, cy, base_z=2, top_z=2, top_rows=2, solid=False)

    m.paint()
    _paint_conservatory_floors(m, [
        (6, 4, 14, 6, 'plaza'),
        (5, 8, 15, 13, 'plaza'),
        (9, 14, 11, 16, 'plaza'),
        (15, 11, 17, 14, 'pave'),
    ], inlays=[(7, 4, 13, 6), (7, 8, 13, 13)])
    _paint_emerald_runner(m, 9, 8, 11, 16, medallion=True)
    _paint_emerald_runner(m, 9, 4, 11, 6, medallion=False)
    _paint_canal_water(m, moat_293)

    # P1-2 FIX (a): Fill the two pitch-black wall holes at (6, 2..3) & (14, 2..3) AND clear dark wainscoting behind dais candelabras (6,4)&(14,4)!
    cvp_rows = K.KITS['cvP2']['rows']
    for wx in (6, 14):
        m.L[0, 2, wx] = cvp_rows[0][1]
        m.L[0, 3, wx] = cvp_rows[1][1]
        m.L[1, 2, wx] = 0
        m.L[1, 3, wx] = 0
        m.L[1, 4, wx] = 0

    # P1-2 FIX (b): Crisp carved limestone balustrades framing BOTH east moat cutoff (16..18, 10) AND west moat south curb (2..4, 13)!
    m.L[1, 10, 16] = P1('rw_rail_w')
    m.L[1, 10, 17] = P1('rw_rail_m')
    m.L[1, 10, 18] = P1('rw_rail_e')
    m.L[1, 13, 2] = P1('rw_rail_w')
    m.L[1, 13, 3] = P1('rw_rail_m')
    m.L[1, 13, 4] = P1('rw_rail_e')

    # P1-3 FIX: Sleek glowing cyan-trimmed metal lift platform pad `lm_pdoor_open` (pas=0x0) at (16, 13) matching conservatory portals!
    m.L[1, 13, 16] = T_PDOOR_OPEN
    for px, py in ((8, 5), (12, 5), (8, 10), (12, 10), (8, 12), (12, 12)):
        if m.L[1, py, px] == 0:
            m.L[1, py, px] = T_PETALS

    Lr = RC.resolve(m.L, TID).astype(np.int32)
    # Crisp conservatory sunbeams ONLY — ZERO void-bleeding / lift-smearing pf_glow halos!
    _add_safe_overlay(Lr, TID, 'cv_shaft', [(7, 4), (10, 4), (13, 4), (8, 9), (12, 9)])
    _assert_columns_intact(Lr, cols_293, 'Map 293')
    _assert_braziers_intact(Lr, braziers_293, 'Map 293')
    _assert_chandeliers_intact(Lr, chandeliers_293, 'Map 293')
    _assert_zero_exit_pockets(Lr, E, 16, 'Map 293')

    ev_pts = [tuple(e['at']) for e in E]
    PG.guard(Lr, TID, ev_pts, 'Map 293')
    assert not PG.hits(Lr, R.tilesets()[TID], ev_pts), 'Map 293 passguard hits!'
    _verify_over_trigger_and_sightlines(Lr, E, 'Map 293')
    _check_ruby_syntax(E, 'Map 293')

    _sim_bfs(Lr, E, (10, 15), [
        ('Warden Juno', (10, 5), True),
        ('Fast-Exit Lift', (16, 13), False),
        ('Lift Sign', (15, 12), True),
        ('South Return', (10, 16), False),
    ], 'Map 293 Warden Arena')

    np.save(os.path.join(HERE, 'data', 'raw', '293.npy'), Lr.astype(np.int16))
    spec = {
        'id': 293,
        'name': 'Verdance Gym - Warden Arena',
        'parent': 290,
        'bgm': 'Gym',
        'field': FIELD,
        'map_audio': {'bgm': 'Gym - Warden Hall', 'bgs': 'Gossamer Deepwood', 'bgs_volume': 25, 'rain': False},
        'metadata': {'Name': 'Verdance Gym', 'SnapEdges': True, 'MapPosition': VERD_POS, 'BattleBack': 'field'},
        'tone': [10, 12, -2, 0],
        'fog': {'name': 'prismfall_spores', 'opacity': 20, 'blend': 1, 'zoom': 100, 'sx': 1, 'sy': 0},
        'biome': 'interior',
        'tileset': TID,
        'raw': 'data/raw/293.npy',
        'events': E,
    }
    with open(os.path.join(HERE, 'specs', '293_verdance_gym_293.yaml'), 'w', encoding='utf-8') as f:
        f.write('# GENERATED by mapgen/layouts/verdance_gym.py (Batch 3E): Verdance Gym - Warden Arena (Juno Hale).\n')
        f.write(yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))
    print('Wrote specs/293_verdance_gym_293.yaml and data/raw/293.npy')
    return m, Lr


def verify_mod4_solver():
    """Exhaustive mod-4 proof verifying 290, 291, 292, and 292 Bride Bower Mastery."""
    # 291 Ring of Six
    sols_291 = []
    for w in product(range(4), repeat=6):
        st = [0, 0, 1, 2, 1, 2]
        for i, c in enumerate(w):
            if c:
                for j in ((i - 1) % 6, i, (i + 1) % 6):
                    st[j] = (st[j] + c) % 4
        if st[0] == 2 and st[2] == 2 and st[4] == 2:
            sols_291.append((sum(w), st.count(3), w))
    sols_291.sort()
    clean_291 = sorted(s for s in sols_291 if s[1] == 0)
    assert sols_291[0][:2] == (2, 1) and clean_291[0][:2] == (5, 0)

    # 292 Figure-Eight
    adj = {0: (1, 4, 5, 8), 1: (0, 2), 2: (1, 3), 3: (2, 4), 4: (3, 0), 5: (0, 6), 6: (5, 7), 7: (6, 8), 8: (7, 0)}
    sols_292 = []
    for w in product(range(4), repeat=9):
        st = [1, 0, 3, 1, 2, 2, 0, 3, 1]
        for i, c in enumerate(w):
            if c:
                st[i] = (st[i] + c) % 4
                for nb in adj[i]:
                    st[nb] = (st[nb] + c) % 4
        if st[0] == 2 and st[2] == 2 and st[3] == 2 and st[6] == 2 and st[7] == 2:
            sols_292.append((sum(w), st.count(3), w))
    sols_292.sort()
    clean_292 = sorted(s for s in sols_292 if s[1] == 0)
    assert len(sols_292) == 256 and sols_292[0][:2] == (7, 2) and clean_292[0][:2] == (8, 0)

    # 292 Bride Bower Mastery
    sols_bw = []
    for w in product(range(4), repeat=5):
        st = [0, 2, 1, 3, 1]
        for i, c in enumerate(w):
            if c:
                for j in (i - 1, i, i + 1):
                    if 0 <= j < 5:
                        st[j] = (st[j] + c) % 4
        if st == [2, 3, 2, 3, 2]:
            sols_bw.append((sum(w), w))
    sols_bw.sort()
    assert sols_bw[0] == (6, (0, 2, 3, 0, 1))
    print('Gym 9 Mod-4 Solver Proof PASS: 291 (2w/1h vs 5w/0h), 292 (256 sols; 7w/2h vs 8w/0h), Bower (6w: M2x2,M3x3,M5x1)')


def main():
    verify_mod4_solver()
    build_290()
    build_291()
    build_292()
    build_293()
    print('Done: built all 4 Verdance Gym 9 maps (290, 291, 292, 293).')


if __name__ == '__main__':
    main()
