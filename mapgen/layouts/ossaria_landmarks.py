#!/usr/bin/env python3
"""layouts/ossaria_landmarks.py — Batch 3D: Ossaria Landmarks & Archaeological Dungeons (5 Maps):
  - Map 606: Temple of the Noon Sun           (20x18, TS 57 PF Rejuv Cave cvE2, field :NONE)
      * Round sandstone sanctuary half-buried under a dune off Sunbleach Flats (613)!
      * Radiant 5x5 golden sundial floor medallion (lm_sun) bathed in overhead midday light-shaft (cv_shaft),
        bronze noon bell (pf_bellpost), 4 intact eternal braziers (fw_brazier), solar lore steles (pas=0xf).
      * Live OS_OCTAVE_NOON_BELL wiring (TRIAL_EVENTS.yaml & 151_Talk_Octave.rb):
          - Sona of the Octave (trainer_OCTAVE_SINGER, pf_trial_talk(:OCTAVE_SONA))
          - Noon (Followers/ESPEON) asleep in the midday beam
          - 3 solid sand-drift mounds (SUN_DRIFT, E_rock0 pas=0xf -> 0 over_trigger?, vanish on selfswitch A!)
      * Guarded pbRgssExists?("Data/Map613.rxdata") return to Sunbleach Flats (613).
  - Map 610: Copperdune                       (40x36, TS 56 PF Rejuv Shore, Outdoor, field :DESERT)
      * Borderland C ("The Brass Dunes") desert rail-junction & oasis caravanserai around a broken viaduct!
      * Passes ALL 6 Outdoor Rubric metrics, 0 green grass autotile borders, 0 forbidden props!
      * NW Zenith Freight Depot (lb_gate) + buried iron rail viaduct + half-buried Car No. 9 (lm_tram,
        OS_TOMB_FREIGHT & Riddle #1!).
      * NE Copperdune Pokémon Center (lb_pc at (24,6) -> door (29,11) CD_PC <-> Map 611; HealingSpot [610,29,12]!)
        + Caravanserai Rolls of Unearthing Board (live pf_trial_board(:OSSARIA)!).
      * Central-South framed turquoise Oasis Cistern (_frame_water_coping + copper smelter kiln w/ intact flames),
        Ossarian bone-traders' caravanserai tents (wr_wartent, wr_tent_bone, wr_tent_r, wr_bonecart, pf_stall0..2),
        canonical Ch6 NPCs (Bone-trader, Freight Clerk, Caravan Child, Riddle Trader w/ playable 3-clue Copperdune riddle!).
      * Guarded pbRgssExists? desert road exits to 600 The Brass Dunes (W), 601 The Rib Road (N), 613 Sunbleach Flats (E).
  - Map 611: Copperdune Pokémon Center        (15x11, TS 34 Prismfall Interior)
      * Exact 201/591 Gold Standard: 7/7 symmetrical warm-timber terracotta 0x8f U-counter centered on 5x4 Pokéball
        medallion, NPC 16 ONLY on Nurse Joy (via take_events), ZERO green scoreboard, ZERO 444 stripe,
        Gale Post corner (NPC 14), bidirectional CD_PC <-> Map 610, HealingSpot [610, 29, 12]!
  - Map 624: Ossuary of Dunes                 (44x40, TS 57 PF Rejuv Cave cvE, field :CAVE)
      * Atmospheric subterranean sandstone bone-catacomb & Aurel-era ruin beneath the Marrow Road skull-mouth!
      * Bidirectional north archway <-> Map 625 Script Vault + guarded pbRgssExists? south exit -> Map 620 Marrow Road.
      * ALL 4 canonical Chapter 6 Murals (Gilded King, Year of Two Weathers, Eighteen-Lit Beast, Falling Lights)
        on solid sandstone frieze walls (pas=0xf -> 0 over_trigger?), Sundial Capstone (V551) + Sanctum Seal (S553),
        Sahar Ostrand at Mural IV (Duneholt Rubbing lore beat, S116 CH6_OSSUARY_DONE = true, V126 >= 7),
        pushable Strength sandstone boulders (pf_cave_boulder_E) & rock_smash rocks (pf_cave_rock_E).
      * ALL 3 canonical PBS # Map 624 trainers ([RUINMANIAC, Anwar], [CHANNELER, Shirin], [POKEMANIAC, Faisal] —
        0 duplicates, 100% unobstructed sightlines, field :CAVE!), 100% intact burning fw_brazier flames!
  - Map 625: Ossuary of Dunes - Script Vault  (34x30, TS 57 PF Rejuv Cave cvE, field :CAVE)
      * Sacred subterranean tablet/scroll archive deep inside the Ossuary (624 <-> 625 bidirectional warps!).
      * Vault Sand-Pulley Wheel (S552), towering scroll/tablet racks (mn_books/mn_books2), solid stone inscription
        plinths (mn_plinth, pas=0xf) revealing the Aurel-era Unown cipher ("HOLLOW") & Nasrin's missing mural glyph.
      * Collectible ODDKEYSTONE in West Relic Alcove + East Hallowed Tower Plinth triggering static Spiritomb Lv 32!
      * North Elevated Script Sanctum (TER, 5x5 lm_sun inlay, glowing cv_shaft sunbeams, intact burning braziers)
        hosting the optional Unown Glyph-Swarm Guardian Altar (WildBattle.start(:UNOWN, 33) -> Telluric Seed x2 + Spell Tag!).

Canonical sources:
  - design/maps.json (exact dimensions, town_map_pos, fields, features)
  - design/TRIAL_EVENTS.yaml & plugins/Prismfall Trials/ (606 OCTAVE_SONA, SUN_DRIFT; 610 Rolls board, Riddle/Tomb Freight)
  - design/DUNGEON_PUZZLES.md (624/625 V551, S552, S553, sundial, pulley, HOLLOW cipher)
  - story/25_SCRIPT_CH6.md (Copperdune NPCs, Ossuary 4 murals, Duneholt Rubbing, S116, V126, Spiritomb/Unown)
  - pbs/trainers.txt (# Map 624 Anwar, Shirin, Faisal — 0 duplicates)

Run:
    /usr/bin/python3 -I mapgen/layouts/ossaria_landmarks.py
"""
import os
import sys
import random
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
import routekit as RK
from routekit import Route, item, hidden
from duneholt_exterior import (
    _guarded_unbuilt_transfer, _fx, _npc, _new_desert, _rect_mask,
    _clean_sand_base, _paint_desert_patch, _paint_tile_rect,
    _paint_water_pool, _frame_water_coping, _place_bldg, _place_prop,
    _place_signpost, _place_stair, _paint_cliff_shadows,
    _dress_desert_surface, _add_canyon_sun_and_glow,
    _finalize_and_verify, _dress_canyon_rims, _seal_oob_overhang,
)
from duneholt_interiors import (
    TID_INT, VOID34, CREAM_SANDSTONE, HONEY_PARQUET, CRIMSON_CARPET,
    POKEBALL_MEDAL_5X4, HOTEL_WINDOW, GEO_MAP, HOTEL_VASE,
    _put_tf, _put_grid, _put_9slice, _seam_terracotta_room,
    _tiles_list_34, _verify_4bit_bfs, _add_safe_overlay,
    _verify_all_events_and_trainers,
)

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TID_OUT = 56
TID_CAVE = 57

# Town map positions from design/maps.json
POS_606 = [0, 15, 4]
POS_610 = [0, 15, 5]
POS_624 = [0, 16, 5]

# Copperdune PC (lb_pc at (24, 6) + door [5, 5] = (29, 11)) -> HealingSpot steps onto (29, 12)!
COPPERDUNE_HEAL_SPOT = [610, 29, 12]

# Canonical Ossuary of Dunes Dungeon Switch / Variable IDs (design/DUNGEON_PUZZLES.md §Ossaria — 0 collisions!)
V_OSS_SUNDIAL = 551   # 0..3 rotating sundial capstone reading the 4 mural glyphs
S_OSS_PULLEY = 552    # 625 Script Vault sand-pulley wheel toggled
S_OSS_SEAL = 553      # 624 North Sanctum Seal opened
S_OSS_SPIRITOMB = 554 # 625 Static Spiritomb awakened & resolved
S_OSS_SWARM = 555     # 625 Optional Unown Glyph-Swarm resolved

# Verified TS 57 Tile IDs
T_DIAL = P1('wr_dial')
T_PLINTH = P1('mn_plinth')
T_ROCK0 = P1('E_rock0')
T_SAND_DRIFT = int(RC.resolve(np.array(STAMPS['sk_pebbles']['layers'], dtype=np.int32), TID_CAVE)[1, 1, 0])       # 23504: pale golden desert sand-drift mound (pas=0xf, pri=0)
T_ROADSTONE_BASE = int(RC.resolve(np.array(STAMPS['pf_roadstone']['layers'], dtype=np.int32), TID_CAVE)[1, 1, 0]) # 22709: carved stone stele base (pas=0xf, pri=0)
T_TRUNK_CLOSED = P1('mn_trunk')      # 24344: ancient relic coffer closed (pas=0xf, pri=0)
T_TRUNK_OPEN = P1('mn_trunk_open')   # 24345: ancient relic coffer open (pas=0xf, pri=0)
T_PDOOR = P1('lm_pdoor')
T_PDOOR_OPEN = P1('lm_pdoor_open')
T_LEVER_L = P1('cv_lever_l')
T_LEVER_R = P1('cv_lever_r')
T_STRENGTH_BOULDER_SPRITE = 'pf_cave_boulder_E'
T_ROCK_SMASH_SPRITE = 'pf_cave_rock_E'


# =================================================================================================
# Shared TS 57 & Guarded-Exit Helpers
# =================================================================================================
def _guarded_unbuilt_transfer_stepback(map_id, tx, ty, direction, blocked_text):
    """Guarded exit to an unbuilt map with clean Essentials v21 PBMoveRoute::BACKWARD step-back (0 warnings)."""
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


def _setup_cve2():
    K.KITS['cvE2'] = dict(K.KITS['cvE'], rows=[K.KITS['cvE']['rows'][0], K.KITS['cvE']['rows'][2]])


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


def _trainer_cave(at, ttype, name, d, intro, after, sight=3):
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
        'rules': ['setBattleRule("field", :CAVE)'],
    }


def _strength_boulder(name, at):
    """Pushable desert sandstone Strength boulder (pf_cave_boulder_E) using native Essentials pbStrength / pfp_push."""
    ruby = (
        'if $PokemonMap && $PokemonMap.strengthUsed\n'
        '  if defined?(pbPushThisEvent)\n'
        '    pbPushThisEvent\n'
        '  elsif defined?(pfp_push)\n'
        '    pfp_push(true)\n'
        '  end\n'
        'elsif defined?(pbStrength) && pbStrength\n'
        '  pbPushThisEvent if defined?(pbPushThisEvent)\n'
        'else\n'
        '  pbMessage(_INTL("A heavy sandstone boulder blocks the side passage. A Pokémon using Strength could shove it aside."))\n'
        'end'
    )
    return {
        'type': 'event',
        'name': name,
        'at': list(at),
        'pages': [{
            'graphic': {'sprite': T_STRENGTH_BOULDER_SPRITE, 'dir': 'down'},
            'trigger': 'action',
            'dir_fix': True,
            'commands': [{'script': ruby}],
        }],
    }


def _rock_smash(at, name='Sandstone Rock'):
    return {'type': 'rock_smash', 'at': list(at), 'name': name, 'sprite': T_ROCK_SMASH_SPRITE}


def _paint_sandstone_floors(m, zones):
    palettes = {
        'sand': [P1('E_f%d' % i) for i in range(4)],
        'plaza': [P1('lm_plaza0'), P1('lm_plaza1')],
        'mosaic': [P1('G_f%d' % i) for i in range(4)],
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
    sun_L = RC.resolve(np.array(STAMPS['lm_sun']['layers'], dtype=np.int32), TID_CAVE)
    for dy in range(sun_L.shape[1]):
        for dx in range(sun_L.shape[2]):
            t = int(sun_L[0, dy, dx] or sun_L[1, dy, dx])
            xx, yy = sx + dx, sy + dy
            if t and m.inb(xx, yy) and not m.cliff[yy, xx]:
                m.L[0, yy, xx] = t
                if not m.taken[yy, xx]:
                    m.L[1, yy, xx] = 0


def _assert_braziers_intact(Lr, tid, braziers, label):
    br_ref = RC.resolve(np.array(STAMPS['fw_brazier']['layers'], dtype=np.int32), tid)
    flame_tid = int(br_ref[2, 0, 0])
    for bx, by in braziers:
        assert int(Lr[2, by, bx]) == flame_tid, (
            f'{label}: fw_brazier flame damaged at ({bx},{by}): got {Lr[2, by, bx]} != {flame_tid}'
        )


def _assert_no_over_trigger(Lr, tid, events, label):
    import build as B
    ts = R.tilesets()[tid]
    solid_ev = set()
    for e in events:
        if e.get('type') in ('npc', 'trainer', 'mart', 'rock_smash'):
            solid_ev.add(tuple(e['at']))
        elif e.get('type') == 'event':
            pg0 = (e.get('pages') or [{}])[0]
            g0 = pg0.get('graphic') or {}
            if not pg0.get('through') and (g0.get('sprite') or (g0.get('tile') and (ts['passages'][g0['tile']] & 0x0f) == 0x0f)):
                solid_ev.add(tuple(e['at']))
    for e in events:
        ex, ey = e['at']
        if e.get('type') == 'sign':
            assert not B.cell_passable(Lr, ts, ex, ey) or (ex, ey) in solid_ev, (
                f'{label}: OVER_TRIGGER TRAP on sign {e.get("name")} at {(ex, ey)}!'
            )
        elif e.get('type') == 'event':
            for pi, pg in enumerate(e.get('pages') or []):
                if pg.get('trigger', 'action') == 'action' and (pg.get('commands') or []):
                    g = pg.get('graphic') or {}
                    if not g.get('sprite') and not g.get('tile'):
                        assert not B.cell_passable(Lr, ts, ex, ey) or (ex, ey) in solid_ev, (
                            f'{label}: OVER_TRIGGER TRAP on action event {e.get("name")} page {pi} at {(ex, ey)}!'
                        )


# =================================================================================================
# 1. MAP 606 — TEMPLE OF THE NOON SUN (20x18, TS 57 PF Rejuv Cave cvE2, field :NONE)
# =================================================================================================
def build_606():
    W, H = 20, 18
    _setup_cve2()
    m = Cave(W, H, 'E', seed=606, pool='Cave Pool', tid=TID_CAVE)
    m.STAIRS = (P1('E_stairl'), P1('E_stairm'), P1('E_stairr'))
    m.kit = {TER: 'cvE2', FLOOR: 'cvE2', MASS: 'cvE2', 'default': 'cvE2'}

    # ---- 1. Sculpt Round / Octagonal Half-Buried Sandstone Solar Rotunda ----
    m.box(5, 2, 14, 14, FLOOR, '.')
    m.box(3, 4, 16, 12, FLOOR, '.')
    m.box(2, 6, 17, 10, FLOOR, '.')
    # Recessed South Sandstone Doorway Vestibule (x=8..11, y=14..16 -> exit warps at (9,16),(10,16))
    m.box(8, 14, 11, 16, FLOOR, '.')
    m.tidy()
    m.plan_cliffs(rows=2)

    # ---- 2. Live OS_OCTAVE_NOON_BELL Events, Bronze Bell, Lore Steles & Guarded Exit ----
    E = m.events

    # Guarded South Return to Sunbleach Flats (613) — 100% immersive desert dialogue + PBMoveRoute::BACKWARD step-back!
    for rx in (9, 10):
        E.append({
            'type': 'event',
            'name': 'Exit to Sunbleach Flats' + (' ' if rx == 10 else ''),
            'at': [rx, 16],
            'pages': [{
                'trigger': 'touch',
                'through': True,
                'commands': _guarded_unbuilt_transfer_stepback(
                    613, 55, 32, 'down',
                    "(Beyond the sunken sandstone archway, blinding salt-glare and windblown sand sweep across Sunbleach Flats. Rest beneath the temple roof until the squall subsides.)"
                ),
            }],
        })

    # Sona of the Octave (TRIAL_EVENTS.yaml:268 — live pf_trial_talk(:OCTAVE_SONA)!)
    # Positioned on the SW sundial rim (7, 9) facing right toward Noon -> ZERO sprite overlap with 64x64 Espeon at (9, 8)!
    sona_ruby = (
        'if defined?(pf_trial_talk)\n'
        '  pf_trial_talk(:OCTAVE_SONA)\n'
        'else\n'
        '  pbMessage(_INTL("Sona: Yes, I\'m the keeper. Yes, the sand filled the roof-shaft. You were going to ask both."))\n'
        '  pbMessage(_INTL("Sona: Clear the three drifts round the midday light-shaft and Noon\'s jewel will wake again."))\n'
        'end'
    )
    E.append({
        'type': 'event',
        'name': 'Sona',
        'at': [7, 9],
        'pages': [{
            'graphic': {'sprite': 'trainer_OCTAVE_SINGER', 'dir': 'right'},
            'trigger': 'action',
            'move': 'fixed',
            'commands': [{'script': sona_ruby}],
        }],
    })

    # Noon — Sona's Espeon centered directly on the sundial center orb (9, 8) inside the midday light-shaft!
    noon_ruby = (
        'if (pf_quest_done?(:OS_OCTAVE_NOON_BELL) rescue false)\n'
        '  pbMessage(_INTL("Noon stretches luxuriously inside the warm circle of midday light, its crimson forehead jewel shining bright as an ember."))\n'
        'else\n'
        '  pbMessage(_INTL("An Espeon lies curled upon the sundial\'s center orb. Its forehead jewel is dim in the gloom — waiting for the blocked light-shaft to clear."))\n'
        'end'
    )
    E.append({
        'type': 'event',
        'name': 'Noon (Espeon)',
        'at': [9, 8],
        'pages': [{
            'graphic': {'sprite': 'Followers/ESPEON', 'dir': 'down'},
            'trigger': 'action',
            'move': 'fixed',
            'commands': [{'script': noon_ruby}],
        }],
    })

    # Three Solid Wind-Packed Desert Sand Drifts around the light-shaft rim (TRIAL_EVENTS.yaml:270-273 — SUN_DRIFT!)
    # Uses pale golden desert sand-drift mound T_SAND_DRIFT (23504, pas=0xf -> 0 over_trigger?, vanishes cleanly on selfswitch A!)
    drift_ruby = (
        'if (pf_trial_ready?(:SUN_DRIFT) rescue false)\n'
        '  pbSEPlay("Mining reveal", 85, 95)\n'
        '  pf_trial_talk(:SUN_DRIFT)\n'
        '  $game_self_switches[[606, @event_id, "A"]] = true\n'
        '  $game_map.need_refresh = true\n'
        'else\n'
        '  pbMessage(_INTL("A dense drift of wind-packed desert sand has spilled down through the roof\'s light-shaft. Talk to Sona before disturbing it."))\n'
        'end'
    )
    for idx, (dx, dy) in enumerate(((6, 8), (9, 5), (12, 8)), 1):
        E.append({
            'type': 'event',
            'name': f'Sand drift {idx}',
            'at': [dx, dy],
            'pages': [
                {
                    'graphic': {'tile': T_SAND_DRIFT},
                    'trigger': 'action',
                    'commands': [{'script': drift_ruby}],
                },
                {
                    'cond': {'self': 'A'},
                    'commands': [],
                },
            ],
        })

    # The Bronze Noon Bell (pf_bellpost 1x3 at (13, 3) -> solid pas=0xf base at (13, 5)!)
    bell_ruby = (
        'pbSEPlay("Anim/HealBell", 95, 85)\n'
        'pfm_shake(1, 6, 8)\n'
        'pbMessage(_INTL("BONG... A single warm bronze note rings around the round sandstone dome and hangs in the shaft of dust."))'
    )
    E.append({
        'type': 'event',
        'name': 'Bronze Noon Bell',
        'at': [13, 5],
        'pages': [{'trigger': 'action', 'commands': [{'script': bell_ruby}]}],
    })

    # Ancient Solar Lore Plaques on solid stone pedestals (pf_roadstone bases, pas=0xf -> 0 over_trigger?!)
    E += [
        _sign('West Solar Stele', (4, 8),
              "TEMPLE OF THE NOON SUN — 'Built before the Electors raised Duneholt's well. When the zenith shaft strikes the brass rim, the sleeper wakes.'"),
        _sign('East Solar Stele', (15, 8),
              "INSCRIPTION OF THE FOURTH NOTE — 'Eight voices once kept the Choir's watch across the realm. Here in Ossaria, the fourth waits where noon stands still.'"),
        {'type': 'item', 'at': [6, 4], 'item': 'SUNSTONE', 'name': 'Temple Sun Stone'},
    ]

    for e in E:
        ex, ey = e['at']
        m.keep_clear.add((ex, ey))
    for pt in ((9, 15), (10, 15), (9, 16), (10, 16), (7, 9), (8, 8), (9, 8), (10, 8), (8, 9), (9, 9), (10, 9)):
        m.keep_clear.add(pt)

    # ---- 3. Round Sandstone Sanctuary Architecture: Obelisks, Bronze Bell, Lore Plinths & 4 Intact Braziers! ----
    _place_stamp_over(m, 'pf_bellpost', 13, 3, base_z=1, top_z=2, top_rows=2, solid=True)   # Base (13, 5) pas=0xf!
    _place_stamp_over(m, 'pf_roadstone', 4, 7, base_z=1, top_z=2, top_rows=1, solid=True)  # Base (4, 8) pas=0xf!
    _place_stamp_over(m, 'pf_roadstone', 15, 7, base_z=1, top_z=2, top_rows=1, solid=True) # Base (15, 8) pas=0xf!

    # Sandstone columns ringing the octagonal solar rotunda
    for cx, cy in ((7, 3), (12, 3), (3, 5), (16, 5), (3, 10), (16, 10), (7, 13), (12, 13)):
        _place_stamp_over(m, 'nr_col', cx, cy, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'lm_banner_w', 9, 2, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'lm_banner_w', 10, 2, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'wr_sacks', 15, 11, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'wr_sacks', 4, 11, base_z=1, top_z=1, top_rows=0, solid=True)

    braziers_606 = [(5, 5), (14, 5), (5, 11), (14, 11)]
    for bx, by in braziers_606:
        _place_stamp_over(m, 'fw_brazier', bx, by, base_z=1, top_z=2, top_rows=1, solid=True)

    m.paint()
    _paint_sandstone_floors(m, [
        (2, 3, 17, 15, 'sand'),
        (6, 5, 13, 12, 'plaza'),
        (8, 12, 11, 16, 'plaza'),
        (4, 6, 15, 11, 'mosaic'),
    ])
    # Radiant 5x5 golden-ivory sundial floor medallion centered at (7, 6) (x=7..11, y=6..10)!
    _paint_sun_medallion(m, 7, 6)

    Lr = RC.resolve(m.L, TID_CAVE).astype(np.int32)
    # Dramatic midday overhead light-shaft falling directly onto the sundial center + safe brazier halos!
    _add_safe_overlay(Lr, TID_CAVE, 'cv_shaft', [(8, 6), (10, 6)])
    _add_safe_overlay(Lr, TID_CAVE, 'pf_glow', braziers_606 + [(9, 7)])
    _assert_braziers_intact(Lr, TID_CAVE, braziers_606, 'Map 606')

    ev_pts = [tuple(e['at']) for e in E]
    PG.guard(Lr, TID_CAVE, ev_pts, 'Map 606')
    assert not PG.hits(Lr, R.tilesets()[TID_CAVE], ev_pts), 'Map 606 passguard hits!'
    _assert_no_over_trigger(Lr, TID_CAVE, E, 'Map 606')
    _verify_all_events_and_trainers(Lr, TID_CAVE, E, (9, 15), 'Map 606 Temple of the Noon Sun')

    m.L = Lr
    head = {
        'id': 606,
        'name': 'Temple of the Noon Sun',
        'parent': 613,
        'bgm': 'Cave',
        'field': 'NONE',
        'map_audio': {'bgm': 'Dungeon - Ruins', 'bgs': ''},
        'metadata': {'Name': 'Temple of the Noon Sun', 'Outdoor': False, 'ShowArea': True, 'SnapEdges': True, 'MapPosition': POS_606},
        'tone': [16, 10, -8, 4],
        '_file': '606_temple_of_the_noon_sun.yaml',
    }
    m.write(606, head, comment='# GENERATED by mapgen/layouts/ossaria_landmarks.py (Batch 3D): Temple of the Noon Sun.\n'
                               '# Edit the layout script, not this file.\n')
    print('Wrote specs/606_temple_of_the_noon_sun.yaml and data/raw/606.npy')


# =================================================================================================
# 2. MAP 610 — COPPERDUNE (40x36, TS 56 PF Rejuv Shore, Outdoor Desert Rail-Junction & Caravanserai)
# =================================================================================================
def build_610():
    W, H = 40, 36
    r, m = _new_desert(610, W, H, kit='sdc', seal='wr_sacks')

    # ---- 1. Sculpt Axis-Aligned Borderland Desert Mesa Basin w/ 3 Clean Caravan/Rail Road Corridors ----
    #   West road (x=0, y=18..20)  -> 600 The Brass Dunes
    #   North road (x=18..21, y=0) -> 601 The Rib Road
    #   East road (x=39, y=18..20) -> 613 Sunbleach Flats
    m.ht[:, :] = 0
    # Outer framing sandstone mesas (strictly clear of buildings & roads; continuous fused ht=2 U-basin on south/west/east!)
    m.ht[0:3, 0:18] = 2     # NW canyon rim above freight depot (cliff lands y=2..4 -> depot roof starts y=5!)
    m.ht[0:3, 22:40] = 2    # NE canyon rim above PC (cliff lands y=2..4 -> PC starts y=6!)
    m.ht[0:16, 0:3] = 2     # West rim north of west rail road (cliff lands y=15..17 -> road clear y=18..20!)
    m.ht[21:36, 0:3] = 2    # West rim south of west road (seals (0, 21) cleanly -> 0 border leaks!)
    m.ht[0:16, 37:40] = 2   # East rim north of east road
    m.ht[21:36, 37:40] = 2  # East rim south of east road (seals (39, 21) cleanly -> 0 border leaks!)
    m.ht[33:36, 0:40] = 2   # Continuous fused ht=2 south canyon rim (0 chopped 3x2 SW/SE cliff slabs!)

    m.plan_cliffs(rows=3)

    # ---- 2. Landmark Buildings: Zenith Freight Depot, Copperdune PC (CD_PC <-> 611), Caravanserai ----
    E = []
    sign_bases = []

    # NW: Zenith Brass Freight Depot (lb_gate 8x5 at (5, 5) -> passable door squarely at (9, 9): touch-trigger + BACKWARD -> 0 over_trigger?!)
    _place_bldg(r, 'lb_gate', 5, 5)
    E.append(_fx({
        'type': 'event', 'name': 'Zenith Freight Depot Door', 'at': [9, 9],
        'pages': [{
            'trigger': 'touch',
            'commands': [
                "ZENITH FREIGHT DEPOT — COPPERDUNE TERMINAL. The heavy brass doors are bolted during the midday shift; manifest boards list brass rails, coal, and drill-heads bound north for Duneholt.",
                {'script': 'pbMoveRoute($game_player, [PBMoveRoute::BACKWARD], true)'},
            ],
        }],
    }))

    # Half-buried Railway Car No. 9 on the broken viaduct stub (lm_tram 5x2 at (8, 12) -> solid base y=13!)
    _place_prop(r, 'lm_tram', 8, 12, solid=True)
    # Interactive Car Nine inspection (OS_TOMB_FREIGHT + Riddle #1 clue!)
    car9_ruby = (
        'pbMessage(_INTL("RAILWAY CAR No. 9 — Half-buried in drifting ochre sand at the end of the broken brass viaduct."))\n'
        'pbMessage(_INTL("Its manifest says \'MACHINE PARTS — LUMEN\', yet dry incense and ancient Ossarian tomb-seal wax smell sharp through the bolted sliding door."))\n'
        'pbMessage(_INTL("(Chalked across the brass bumper: \'RIDDLE ANSWER I: THE IRON HORSE THAT STOPPED AT SAND — CAR NINE.\')"))\n'
        'pfm_set(:cd_riddle_1, true) rescue nil'
    )
    E.append(_fx({
        'type': 'event',
        'name': 'Locked Railway Car No. 9',
        'at': [10, 13],
        'pages': [{'trigger': 'action', 'commands': [{'script': car9_ruby}]}],
    }))

    # NE: Copperdune Pokémon Center (lb_pc 10x6 at (24, 6) -> door (29, 11) linked via CD_PC <-> Map 611!)
    ev, pc_door = _place_bldg(r, 'lb_pc', 24, 6, door_link='CD_PC', door_name='Copperdune Pokémon Center')
    assert pc_door == (29, 11), f'610 PC door moved to {pc_door}!'
    E.append(ev)

    # SE: Copper & Bone Exchange House (wh_b 7x8 at (29, 23) -> double-gate at (32, 30)) + Pottery/Smelter Workshop (sp_pots 4x6 at (23, 25) -> door at (23, 30))
    _place_bldg(r, 'wh_b', 29, 23)
    E.append(_fx({
        'type': 'event', 'name': 'Bone-Exchange House Gate', 'at': [32, 30],
        'pages': [{
            'trigger': 'touch',
            'commands': [
                "OSSARIAN BONE-EXCHANGE & CARAVANSERAI HOUSE. Scales inside weigh fossils against Zenith coal and copper ingots — closed while the noon caravans trade outside.",
                {'script': 'pbMoveRoute($game_player, [PBMoveRoute::BACKWARD], true)'},
            ],
        }],
    }))
    _place_bldg(r, 'sp_pots', 23, 25)
    E.append(_fx({
        'type': 'event', 'name': 'Copper Smelter Workshop Door', 'at': [23, 30],
        'pages': [{
            'trigger': 'touch',
            'commands': [
                "COPPER SMELTER & AMPHORA WORKSHOP. The clay kiln glows orange inside, melting salvaged brass rails into desert cookware — too hot inside to enter without smith's gloves.",
                {'script': 'pbMoveRoute($game_player, [PBMoveRoute::BACKWARD], true)'},
            ],
        }],
    }))

    # SW: Bone-Traders' Caravanserai Pavilion (wr_wartent 5x4 at (5, 22)) + Caravan Tents + Sandstone Mural Stele!
    _place_prop(r, 'wr_wartent', 5, 22, solid=True)
    _place_prop(r, 'wr_tent_bone', 11, 24, solid=True)
    _place_prop(r, 'wr_tent_r', 5, 28, solid=True)
    _place_prop(r, 'wr_tent_bone', 10, 28, solid=True)
    # Caravan Sandstone Mural Stele (pf_roadstone 1x2 at (15, 28) -> solid base (15, 29), Riddle #2 clue!)
    _place_prop(r, 'pf_roadstone', 15, 28, solid=True)
    mural_stele_ruby = (
        'pbMessage(_INTL("An ancient sandstone caravan boundary stele worn smooth by blowing grit. Carved across its face is a coiled serpent drinking from a golden sun-well."))\n'
        'pbMessage(_INTL("(Beneath the carving, a bone-trader has noted: \'RIDDLE ANSWER II: THE SERPENT THAT NEVER SHEDS ITS SKIN — THE MURAL.\')"))\n'
        'pfm_set(:cd_riddle_2, true) rescue nil'
    )
    E.append(_fx({
        'type': 'event',
        'name': 'Caravan Mural Stele',
        'at': [15, 29],
        'pages': [{'trigger': 'action', 'commands': [{'script': mural_stele_ruby}]}],
    }))

    # Copperdune Caravanserai Rolls of Unearthing Board (001_Trials_Config.rb:92 -> live pf_trial_board(:OSSARIA)!)
    _place_prop(r, 'wr_tally', 24, 14, solid=True)  # 3x2 clay tablet rack -> solid base (25, 15)!
    E.append(_fx({
        'type': 'event',
        'name': 'Copperdune Tablet Rack',
        'at': [25, 15],
        'pages': [{
            'trigger': 'action',
            'commands': [{
                'if': 'defined?(pf_trial_board)',
                'then': [{'script': 'pf_trial_board(:OSSARIA)'}],
                'else': ["COPPERDUNE CARAVANSERAI RACK — The Rolls of Unearthing. Clay tablets posted by Ossaria's bone-traders and dig crews."],
            }],
        }],
    }))

    # Guarded Desert Road Exits (pbRgssExists? + PBMoveRoute::BACKWARD step-back on ALL 10 exits, ZERO meta-text!)
    for wy in (18, 19, 20):
        E.append(_fx({
            'type': 'event',
            'name': 'West to The Brass Dunes' + (' ' * (wy - 18)),
            'at': [0, wy],
            'pages': [{
                'trigger': 'touch',
                'through': True,
                'commands': _guarded_unbuilt_transfer_stepback(
                    600, 128, 36, 'left',
                    "(West along the buried rail embankment lies the Brass Dunes. Sand-drifts have buried the viaduct's approach ramp — wait for the rail gangers to clear the line.)"
                ),
            }],
        }))
    for nx in (18, 19, 20, 21):
        E.append(_fx({
            'type': 'event',
            'name': 'North to The Rib Road' + (' ' * (nx - 18)),
            'at': [nx, 0],
            'pages': [{
                'trigger': 'touch',
                'through': True,
                'commands': _guarded_unbuilt_transfer_stepback(
                    601, 36, 118, 'up',
                    "(North between the giant fossil ribs runs the Rib Road toward Duneholt. A wall of red canyon sandstorm is rolling south down the pass.)"
                ),
            }],
        }))
    for ey in (18, 19, 20):
        E.append(_fx({
            'type': 'event',
            'name': 'East to Sunbleach Flats' + (' ' * (ey - 18)),
            'at': [39, ey],
            'pages': [{
                'trigger': 'touch',
                'through': True,
                'commands': _guarded_unbuilt_transfer_stepback(
                    613, 2, 32, 'right',
                    "(East lies the blinding white salt-pan of Sunbleach Flats. Caravan guides advise waiting until the midday glare cools before crossing.)"
                ),
            }],
        }))

    # ---- 3. Bazaar Stalls, Smelter Kiln Braziers, Lanterns, Bone Carts & Desert Props ----
    braziers_610 = [(23, 22), (27, 22), (17, 9), (22, 9)]
    props_610 = [
        # Freight depot yard & broken viaduct props (cv_cart & wr_telegraph strictly CLEAR of y=13 rails!)
        ('wr_supply', 14, 6), ('wr_sacks', 14, 9), ('cv_cart', 4, 11), ('wr_sandbags', 6, 11),
        ('wr_telegraph', 15, 9), ('pf_lantern', 16, 12), ('pf_lantern', 16, 16),
        # PC & Caravanserai Rack forecourt (nt_deadtree in clear 3x3 open sand at (34, 6), 0 building overlap!)
        ('nt_deadtree', 34, 6), ('pf_pcsign', 34, 10), ('pf_stonebench', 30, 14), ('pf_lantern', 23, 12), ('pf_lantern', 35, 14),
        ('wr_ban_bone', 22, 6), ('wr_ban_bone', 17, 6),
        # Oasis, Copper Smelter Yard & Natural Sandstone Talus Framing West/East Mesa Shoulders
        ('wr_well', 17, 26), ('wr_sacks', 22, 26), ('wr_sandbags', 27, 29),
        ('pf_stall0', 11, 21), ('pf_stall1', 14, 16), ('pf_stall2', 29, 15),
        ('wr_bonecart', 8, 16), ('wr_supply', 4, 14),
        ('pf_lantern', 16, 25), ('pf_lantern', 28, 21),
        ('sk_boulder', 3, 16), ('sk_boulder', 35, 16),
        ('sk_boulder', 35, 21), ('sk_boulder', 19, 30),
        # Sculpted mesa-top boulders & desert crags on ht=2 outer canyon rims
        ('sk_pebbles', 0, 6), ('sk_pebbles', 0, 11), ('sk_pebbles', 38, 7), ('sk_pebbles', 38, 12),
        ('sk_pebbles', 0, 24), ('sk_pebbles', 38, 25),
        ('sk_boulder', 8, 34), ('sk_boulder', 27, 34), ('sk_pebbles', 18, 34),
    ] + [('fw_brazier', bx, by) for bx, by in braziers_610]
    for nm, px, py in props_610:
        _place_prop(r, nm, px, py, solid=True)
    _dress_canyon_rims(r, 610, min_ht=2)

    # Signposts (strictly solid pf_signpost base at (sx, sy+1) with walkable south cell!)
    sign_bases.append(_place_signpost(
        r, E, 'Copperdune Town Sign', 17, 17,
        "COPPERDUNE — THE BRASS DUNES JUNCTION. ← Brass Dunes · ↑ Rib Road & Duneholt · → Sunbleach Flats. Trade in bones, copper, and Zenith rail iron."
    ))
    sign_bases.append(_place_signpost(
        r, E, 'Freight Depot Sign', 13, 9,
        "ZENITH FREIGHT DEPOT — Track Terminus. Notice: Viaduct spans past Car No. 9 are buried under shifting dunes."
    ))
    sign_bases.append(_place_signpost(
        r, E, 'Caravanserai Board Sign', 27, 14,
        "THE ROLLS OF UNEARTHING — Copperdune Caravanserai Rack. Inspect the clay tablet rack beside this post for Ossaria Trial notices."
    ))

    # ---- 4. Canonical Ch6 NPCs, Noon Oasis Sandile (Riddle #3!), Playable Riddle Trader & Pickups ----
    # Lounging Oasis Sandile (Riddle #3 clue!) placed at (15, 22) facing down — 100% clear of pool coping at x=17!
    sandile_ruby = (
        'pbMessage(_INTL("Sandile: Krooo... (A dusty desert Sandile sunning itself right beside the oasis cistern rim, half-buried in warm gravel!)"))\n'
        'pbMessage(_INTL("(It snaps its jaws happily at the midday sun — Riddle Answer III: the Sandile that only surfaces at noon!)"))\n'
        'pfm_set(:cd_riddle_3, true) rescue nil'
    )
    E.append(_fx({
        'type': 'event',
        'name': 'Noon Sandile',
        'at': [15, 22],
        'pages': [{
            'graphic': {'sprite': 'Followers/SANDILE', 'dir': 'down'},
            'trigger': 'action',
            'move': 'fixed',
            'commands': [{'script': sandile_ruby}],
        }],
    }))

    # Riddle Caravan Trader (OS_RIDDLE_CARAVAN — playable 3-clue riddle right here in Copperdune!)
    riddle_ruby = (
        'if (pfm_get(:cd_riddle_done) rescue false)\n'
        '  pbMessage(_INTL("Riddle Trader: Still can\'t believe the third answer wasn\'t a goat! Safe trails up the Rib Road, clever traveler."))\n'
        'else\n'
        '  c1 = (pfm_get(:cd_riddle_1) rescue false)\n'
        '  c2 = (pfm_get(:cd_riddle_2) rescue false)\n'
        '  c3 = (pfm_get(:cd_riddle_3) rescue false)\n'
        '  pbMessage(_INTL("Riddle Trader: Three riddles of Copperdune! Find all three answers hidden round town and I\'ll pay you handsomely:"))\n'
        '  pbMessage(_INTL("1) What iron horse ran out of track and stopped at sand?\\n2) What desert serpent never sheds its skin?\\n3) What sharp-toothed bather only surfaces beside the oasis at noon?"))\n'
        '  if c1 && c2 && c3\n'
        '    if pbConfirmMessage(_INTL("You\'ve seen all three right here in Copperdune! Tell her: Car Nine, the Sandstone Mural, and the Oasis Sandile?"))\n'
        '      pbMessage(_INTL("Riddle Trader: Car Nine! The Mural! ...And a SANDILE?! Oh! I always thought the third one was a goat!"))\n'
        '      pbSEPlay("Mining reveal", 90, 100)\n'
        '      pbReceiveItem(:SOFTSAND, 1)\n'
        '      pbReceiveItem(:RAREBONE, 1)\n'
        '      pfm_set(:cd_riddle_done, true) rescue nil\n'
        '    end\n'
        '  else\n'
        '    got = [c1, c2, c3].count(true)\n'
        '    pbMessage(_INTL("Riddle Trader: Looks like you\'ve spotted {1} of the 3 landmarks so far. Check the old rail car, the south caravan stele, and the oasis bank!", got))\n'
        '  end\n'
        'end'
    )
    E += [
        _fx({
            'type': 'event',
            'name': 'Riddle Trader',
            'at': [10, 26],
            'pages': [{
                'graphic': {'sprite': 'NPC 22', 'dir': 'right'},
                'trigger': 'action',
                'move': 'fixed',
                'commands': [{'script': riddle_ruby}],
            }],
        }),
        # Canonical story/25_SCRIPT_CH6.md lines 156-163 NPCs!
        _npc('Bone-trader', (12, 23), 'NPC 20', [
            "Bone-trader: Prices in bones, stranger. A Potion's two bones. A Super's five.",
            "Bone-trader: A bone's a bone, don't ask me which.",
        ], d='down'),
        _npc('Freight Clerk', (11, 10), 'NPC 18', [
            "Freight Clerk: Meridian deep-drill crews come through here every week, north, with drill-heads the size of houses.",
            "Freight Clerk: They go out shiny and come back scraped.",
        ], d='down'),
        _npc('Freight Foreman', (12, 14), 'trainer_FOREMAN', [
            "Freight Foreman: Car Nine on the siding's been sitting twice as heavy as its manifest all morning.",
            "Freight Foreman: Meridian swears it's machine parts bound for Lumen. The Ossarian tomb-guild says grave goods. Nobody's game to break the seal.",
        ], d='left'),
        _npc('Caravan Child', (18, 28), 'NPC 05', [
            "Caravan Child: My mum says the ground under Duneholt's warm.",
            "Caravan Child: She says the sleeping red giant's turning over in his bed. I said, is he going to get up? She said not while I'm talking.",
        ], d='up', move='random'),
        _npc('Copper Smelter', (25, 23), 'trainer_ENGINEER', [
            "Copper Smelter: Zenith brings coal and brass rails; Ossaria brings bone-meal and desert copper. Copperdune lives in the slag between the two!",
        ], d='down'),
        _fx(item((34, 21), 'NUGGET')),
        _fx(item((4, 30), 'ULTRABALL')),
        _fx(hidden((20, 29), 'HEATROCK', 'HiddenItem (smelter cinder pile)')),
    ]

    # ---- 5. Paint Pure Desert Ground (ZERO Green Borders!), Unified Brass Rails, Framed Oasis Cistern! ----
    r.paint()
    _clean_sand_base(r)

    # Central Oasis Cistern (x=18..21, y=22..24) cleanly framed with sandstone coping!
    oasis = _rect_mask(H, W, 18, 22, 21, 24)
    _paint_water_pool(r, oasis)

    dirt_dark0 = K.V('DirtDark', 'rejuvenation')
    plaza = [P1('lm_plaza0'), P1('lm_plaza1')]
    mosaic = [P1('G_f%d' % i) for i in range(4)]

    roads = (
        _rect_mask(H, W, 0, 18, 39, 20) |
        _rect_mask(H, W, 18, 0, 21, 21) |
        _rect_mask(H, W, 7, 10, 16, 15) |
        _rect_mask(H, W, 14, 21, 29, 30)
    ) & ~oasis
    _paint_desert_patch(r, roads, dirt_dark0, z=0)

    # Ceremonial Travertine PC Forecourt & Caravanserai Plaza + Smelter Terracotta Apron!
    _paint_tile_rect(r, 24, 12, 33, 17, plaza, z=0, force_l0=True)
    _paint_tile_rect(r, 18, 17, 21, 21, plaza, z=0, force_l0=True)
    _paint_tile_rect(r, 23, 21, 27, 24, mosaic, z=0, force_l0=True)

    # Crisp 1-tile sandstone coping around all 4 sides of the Oasis Cistern!
    _frame_water_coping(r, oasis)

    # Unified Zenith Brass Railway Stub (cv_rail_h on BOTH west x=3..7 and east x=13..15 of Car No. 9, 0 track clashes!)
    rail_h = P1('cv_rail_h')
    for rx in list(range(3, 8)) + list(range(13, 16)):
        if not m.cliff[13, rx] and not m.taken[13, rx]:
            m.L[1, 13, rx] = rail_h

    _paint_cliff_shadows(r, exclude=roads | oasis)
    _dress_desert_surface(r, 610, exclude=oasis, ripple_p=0.48, bone_p=0.05, rut_mask=roads)
    # Outdoor Copperdune: warm lantern/brazier glows ONLY — ZERO inappropriate cave sunbeams (cv_shaft)!
    _add_canyon_sun_and_glow(
        r,
        sun_pts=(),
        glow_pts=braziers_610 + [(16, 12), (23, 12), (35, 14), (16, 25), (28, 21)],
    )

    # Programmatically check all 4 smelter/gate braziers intact BEFORE finalizing!
    Lr_pre = RC.resolve(m.L, TID_OUT).astype(np.int32)
    _assert_braziers_intact(Lr_pre, TID_OUT, braziers_610, 'Map 610')
    _assert_no_over_trigger(Lr_pre, TID_OUT, E, 'Map 610')

    head = {
        'id': 610,
        'name': 'Copperdune',
        'bgm': 'Lerucean Town',
        'field': 'DESERT',
        'map_audio': {'bgm': 'Town - Ossaria', 'bgs': 'Wind - Isenmar', 'bgs_volume': 35, 'rain': False},
        'tone': [16, 6, -10, 4],
        'metadata': {
            'Name': 'Copperdune',
            'Outdoor': True,
            'ShowArea': True,
            'Bicycle': True,
            'HealingSpot': COPPERDUNE_HEAL_SPOT,
            'MapPosition': POS_610,
            'BattleBack': 'desert',
        },
        'rubric': True,
        'yards_ok': True,
        'biome': 'town',
    }
    _finalize_and_verify(
        r, head, '610_copperdune.yaml',
        '# GENERATED by mapgen/layouts/ossaria_landmarks.py (Batch 3D): Copperdune (Borderland C Desert Rail-Junction).\n',
        start_pt=(19, 19),
        targets=[
            ('West to Brass Dunes (600)', (0, 19), False),
            ('North to Rib Road (601)', (19, 0), False),
            ('East to Sunbleach Flats (613)', (39, 19), False),
            ('PC Door (611)', (29, 12), False),
            ('Car No. 9', (10, 13), True),
            ('Caravan Mural Stele', (15, 29), True),
            ('Noon Sandile', (15, 22), True),
            ('Riddle Trader', (10, 26), True),
            ('Tablet Rack (OSSARIA)', (25, 15), True),
        ],
        signpost_bases=sign_bases,
        events=E,
        exclude_boost=oasis,
    )
    # Strictly prove ZERO unguarded walkable border leaks on all 4 edges of Map 610!
    Lr610 = np.load(os.path.join(HERE, 'data', 'raw', '610.npy')).astype(np.int32)
    seen610 = _verify_4bit_bfs(Lr610, TID_OUT, E, (19, 19), [], 'Map 610 Border Audit')
    guarded_pts = {tuple(e['at']) for e in E if e.get('type') == 'event' and (e.get('pages') or [{}])[0].get('trigger') == 'touch'}
    leaks = [(x, y) for (x, y) in seen610 if (x in (0, W - 1) or y in (0, H - 1)) and (x, y) not in guarded_pts]
    assert not leaks, f'Map 610 unguarded walkable border leaks: {leaks}!'
    print(f'Map 610 Border Audit: 0 unguarded edge leaks ({len(guarded_pts)} guarded exits verified)!')


# =================================================================================================
# 3. MAP 611 — COPPERDUNE POKÉMON CENTER (15x11, TS 34 — Exact 201/591 Gold Standard!)
# =================================================================================================
def build_611():
    W, H = 15, 11
    L = np.zeros((3, H, W), dtype=np.int32)
    floor = np.zeros((H, W), dtype=bool)
    floor[2:9, 1:14] = True
    floor[8, 1] = False
    floor[8, 13] = False
    floor[9, 5:10] = True
    floor[10, 6:9] = True

    _seam_terracotta_room(L, floor, wall_style='terracotta')

    # Warm Ossaria Sandstone & Honey Parquet Flooring + Centered 5x4 Pokéball Medallion!
    _put_9slice(L, HONEY_PARQUET, 1, 2, 3, 8, z=0, mask=floor)
    _put_9slice(L, HONEY_PARQUET, 11, 2, 13, 8, z=0, mask=floor)
    _put_9slice(L, CREAM_SANDSTONE, 4, 2, 10, 8, z=0, mask=floor)
    _put_9slice(L, CREAM_SANDSTONE, 5, 9, 9, 9, z=0, mask=floor)
    _put_9slice(L, CREAM_SANDSTONE, 6, 10, 8, 10, z=0, mask=floor)
    _put_grid(L, POKEBALL_MEDAL_5X4, 5, 4, z_rows=(0, 0, 0, 0))
    # Plush crimson welcome runner flowing cleanly into Exit [7,10] (ZERO white 444 stripe!)
    _put_9slice(L, CRIMSON_CARPET, 6, 9, 8, 10, z=1)

    # North wall architectural accents (symmetrical warm terracotta windows — ZERO green scoreboard!)
    _put_grid(L, HOTEL_WINDOW, 2, 0, z_rows=(1, 1))
    _put_grid(L, HOTEL_WINDOW, 9, 0, z_rows=(1, 1))
    L[2, 1, 11] = 5847
    L[1, 2, 11] = 5855
    _put_grid(L, GEO_MAP, 12, 0, z_rows=(1, 1))

    # Symmetrical Unbroken 5-Wide Warm Terracotta U-Counter (x=5..9, y=2..3 — ALL 7/7 0x8f!)
    L[1, 2, 5] = 5952
    L[1, 2, 9] = 5955
    for dx, t in enumerate((5960, 5961, 5962, 5961, 5963)):
        L[1, 3, 5 + dx] = t
    L[2, 1, 6] = 6035
    L[2, 1, 7] = 6036
    L[1, 2, 6] = 6043
    L[1, 2, 7] = 6044

    # West Caravan Lounge & Gale Post Corner
    _put_grid(L, HOTEL_VASE, 1, 2, z_rows=(2, 1))
    _put_grid(L, [[6024, 6026], [6032, 6034]], 2, 3, z_rows=(2, 1))
    _put_grid(L, [[3466, 3467], [3474, 3475]], 1, 6, z_rows=(1, 1))
    L[2, 6, 1] = 3428
    L[2, 6, 2] = 4528

    # East Oasis Lounge Corner
    L[2, 2, 13] = 7126
    L[1, 3, 13] = 7134
    _put_tf(L, 'bookcase', 12, 4)
    L[1, 6, 13] = 4101
    L[2, 7, 12] = 2271
    L[1, 8, 12] = 2279
    L[1, 9, 5] = 4077
    L[1, 9, 9] = 4077
    L[1, 8, 2] = 7177

    # Programmatic assertion: ALL 7/7 U-counter tiles == 0x8f!
    ts34 = R.tilesets()[TID_INT]
    for cx, cy in ((5, 2), (9, 2), (5, 3), (6, 3), (7, 3), (8, 3), (9, 3)):
        t = int(L[1, cy, cx])
        assert ts34['passages'][t] == 0x8f, f'611 counter ({cx},{cy}) tile {t} pas={hex(ts34["passages"][t])} != 0x8f!'

    # Canonical Events (NPC 16 ONLY on Nurse Joy via take_events!)
    events = [
        {'type': 'exit', 'at': [7, 10], 'link': 'CD_PC', 'arrive': [7, 10, 'up']},
        _make_npc('Gale Post Clerk', (3, 6), 'NPC 14', 'right', [
            "Gale Post Clerk: Gale Post — Copperdune Relay! Our couriers swap from rail-speeders to sand-runners right outside this door.",
            "Gale Post Clerk: Mail bound for Duneholt rides north along the Rib Road; everything south heads back across the Brass Dunes toward Lumen.",
        ]),
        _make_npc('Off-Duty Rail Ganger', (10, 6), 'NPC 18', 'left', [
            "Rail Ganger: Three times Meridian laid brass track across the dunes, and three times the sand swallowed it whole.",
            "Rail Ganger: At least the Pokémon Center's cistern never goes dry — best rest stop between Candle Down and Duneholt!",
        ]),
        _make_npc('Caravan Scout', (4, 8), 'NPC 20', 'up', [
            "Caravan Scout: Heading north to challenge Warden Sahar at Duneholt's Dig? Remember — Ground-types rule the Desert field, so pack Water, Grass, or Ice!",
        ]),
    ]
    take_events = [
        {'template': 'pokecenter', 'name': 'Nurse', 'at': [8, 2]},
        {'template': 'pokecenter', 'name': 'Healing balls', 'at': [7, 2]},
        {'template': 'pokecenter', 'name': 'PC', 'at': [11, 2]},
        {'template': 'pokecenter', 'name': 'Town Map, size(2,1)', 'at': [12, 1]},
    ]

    ev_pts = [(7, 10), (7, 9), (8, 4), (8, 2), (7, 2), (11, 3), (11, 2), (12, 2), (3, 6), (10, 6), (4, 8)]
    PG.guard(L, TID_INT, ev_pts, 'Map 611')
    assert not PG.hits(L, ts34, ev_pts), 'Map 611 passguard hits!'
    _verify_4bit_bfs(L, TID_INT, events, (7, 9), [
        ('Exit CD_PC', (7, 10), False),
        ('Nurse Counter (0x8f)', (8, 4), False),
        ('PC Terminal', (11, 3), False),
        ('Town Map', (12, 2), False),
        ('Gale Post Clerk', (3, 6), True),
        ('Rail Ganger', (10, 6), True),
        ('Caravan Scout', (4, 8), True),
    ], 'Map 611 Copperdune PC')

    np.save(os.path.join(HERE, 'data', 'raw', '611.npy'), L.astype(np.int16))
    spec = {
        'id': 611,
        'name': 'Copperdune Pokémon Center',
        'parent': 610,
        'bgm': 'Poke Center',
        'map_audio': {'bgs': ''},
        'tone': [10, 4, -6, 2],
        'metadata': {
            'ShowArea': False,
            'HealingSpot': COPPERDUNE_HEAL_SPOT,
            'MapPosition': POS_610,
        },
        'biome': 'interior',
        'palette': 'interior',
        'tileset': TID_INT,
        'map': '\n'.join(['.' * W] * H) + '\n',
        'tiles': _tiles_list_34(L),
        'events': events,
        'take_events': take_events,
    }
    with open(os.path.join(HERE, 'specs', '611_copperdune_pc.yaml'), 'w', encoding='utf-8') as f:
        f.write('# GENERATED by mapgen/layouts/ossaria_landmarks.py (Batch 3D): Copperdune Pokémon Center.\n')
        f.write(yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))
    print('Wrote specs/611_copperdune_pc.yaml and data/raw/611.npy')


# =================================================================================================
# 4. MAP 624 — OSSUARY OF DUNES (44x40, TS 57 PF Rejuv Cave cvE, field :CAVE)
# =================================================================================================
def build_624():
    W, H = 44, 40
    m = Cave(W, H, 'E', seed=624, pool='Cave Pool', tid=TID_CAVE)
    m.STAIRS = (P1('E_stairl'), P1('E_stairm'), P1('E_stairr'))
    m.kit = {MASS: 'cvE', TER: 'cvE', FLOOR: 'cvE', 'default': 'cvE'}

    # ---- 1. Carve Multi-Chamber Aurel-Era Sandstone Bone-Catacomb (44x40, cvE 3-row cliffs!) ----
    # South Skull-Mouth Antechamber (FLOOR): x=16..27, y=31..38 (exit to 620 at (21..22, 38)!)
    m.box(16, 31, 27, 38, FLOOR, '.')
    # Central Sunlit Ossuary Nave (FLOOR): x=15..28, y=14..30 (directly meets TER y=13 for 3-row stair!)
    m.box(15, 14, 28, 30, FLOOR, '.')
    # West Gilded-King Mural Cloister (FLOOR): x=6..15, y=16..31 (Mural I & Trainer Anwar!)
    m.box(6, 16, 15, 31, FLOOR, '.')
    # West-South Connecting Crypt: x=8..16, y=29..34
    m.box(8, 29, 16, 34, FLOOR, '.')
    # East Eighteen-Locks Relic Gallery (FLOOR): x=28..37, y=16..31 (Mural III & Trainer Faisal!)
    m.box(28, 16, 37, 31, FLOOR, '.')
    # East-South Connecting Crypt: x=27..35, y=29..34
    m.box(27, 29, 35, 34, FLOOR, '.')
    # North Elevated Inner Sanctum (TER): x=13..30, y=4..13 + Symmetrical Recessed Script-Vault Archway x=20..23, y=2..6!
    m.box(13, 4, 30, 13, TER, '.')
    m.box(20, 2, 23, 6, TER, '.')

    # Four Genuine 1-Tile-Throat Strength & Rock Smash Relic Alcoves Carved Into Outer Sandstone Walls!
    #   NW Rock Smash Alcove: walkable 1-tile tunnel x=2..5, y=20 -> Cracked Sandstone W (5, 20) guards ULTRABALL (3, 20)!
    m.box(2, 18, 5, 20, FLOOR, '.')
    #   SW Strength Boulder Chamber: throat (5, 28) -> rear chamber x=2..4, y=28..30 -> Boulder (5, 28) guards SUNSTONE (3, 30)!
    m.box(5, 26, 6, 28, FLOOR, '.')
    m.box(2, 26, 4, 30, FLOOR, '.')
    #   NE Rock Smash Alcove: walkable 1-tile tunnel x=38..41, y=20 -> Cracked Sandstone E (38, 20) guards DUSKBALL (40, 20)!
    m.box(38, 18, 41, 20, FLOOR, '.')
    #   SE Strength Boulder Chamber: throat (38, 28) -> rear chamber x=39..41, y=28..30 -> Boulder (38, 28) guards RAREBONE (40, 30)!
    m.box(37, 26, 38, 28, FLOOR, '.')
    m.box(39, 26, 41, 30, FLOOR, '.')

    # Sculpted catacomb rock chamfers & buttress corners (strictly clear of alcove mouths y=20, 28!)
    m.mass_at([
        (6, 16), (6, 31), (16, 38), (27, 38),
        (37, 16), (37, 31), (13, 4), (30, 4),
        (14, 29), (15, 29), (28, 29), (29, 29),
    ])

    # Central sunken dark subterranean spring pool flanking the Sundial Nave (x=20..23, y=22..24)
    m.box(20, 22, 23, 24, FLOOR, 'w')

    # Grand 4-wide Sandstone Staircase ascending into the Elevated Inner Sanctum (x=20..23, y=13..15)
    m.stairs(20, 13, w=4, n=3, c='.')
    m.plan_cliffs(rows=3)

    # ---- 2. Events: Sealed S553 625 Archway, S552 Drained Sluice Trough, Guarded 620 Exit, 4 Murals, Sahar, 3 Trainers! ----
    E = m.events

    # Guarded South Skull-Mouth Exit -> 620 The Marrow Road (with Essentials v21 PBMoveRoute::BACKWARD step-back!)
    for rx in (21, 22):
        E.append({
            'type': 'event',
            'name': 'South to Marrow Road' + (' ' if rx == 22 else ''),
            'at': [rx, 38],
            'pages': [{
                'trigger': 'touch',
                'through': True,
                'commands': _guarded_unbuilt_transfer_stepback(
                    620, 65, 35, 'down',
                    "(Through the colossal fossil skull-mouth lies the Marrow Road. Sand pours steadily down the brow of the skull — wait for Sahar's diggers to shore the lintel.)"
                ),
            }],
        })

    # REAL Sanctum Seal (S553) Gating Bidirectional North Archway -> 625 Script Vault (16, 27, up)!
    # Page 0 (default): SOLID sealed Elector stone slab (T_PDOOR, pas=0xf, trigger: action) until Sundial Capstone sets S553!
    # Page 1 (switch: 553): OPEN dark portal (T_PDOOR_OPEN, pas=0x0, trigger: touch) warping cleanly into Map 625!
    vault_warp_ruby = (
        'pbSEPlay("Door enter", 80, 100)\n'
        'pbFadeOutIn do\n'
        '  $game_temp.player_new_map_id = 625\n'
        '  $game_temp.player_new_x = 16\n'
        '  $game_temp.player_new_y = 27\n'
        '  $game_temp.player_new_direction = 8\n'
        '  $scene.transfer_player\n'
        'end'
    )
    for vx in (21, 22):
        E.append({
            'type': 'event',
            'name': 'North to Script Vault (625)' + (' ' if vx == 22 else ''),
            'at': [vx, 4],
            'pages': [
                {
                    'graphic': {'tile': T_PDOOR},
                    'trigger': 'action',
                    'commands': [
                        "An ancient Elector seal-stone holds the Script Vault archway fast. Four carved notches on its face match the central Sundial Capstone in the nave below.",
                    ],
                },
                {
                    'cond': {'switch': S_OSS_SEAL},
                    'graphic': {'tile': T_PDOOR_OPEN},
                    'trigger': 'touch',
                    'commands': [{'script': vault_warp_ruby}],
                },
            ],
        })

    # REAL Cross-Map S552 Payoff (Central Nave Lower Sluice Trough at (20..23, 27), controlled by 625 Sand-Pulley Wheel!)
    buried_sluice_msg = (
        "Wind-packed desert sand chokes this sunken Ossuary sluice trough. Bronze drainage grates glint beneath the grit — "
        "a counterweight pulley deeper inside the Script Vault must control these sluices."
    )
    for sx, lbl in ((20, 'W'), (23, 'E')):
        E.append({
            'type': 'event',
            'name': f'Sluice Sandbank {lbl}',
            'at': [sx, 27],
            'pages': [
                {
                    'graphic': {'tile': T_SAND_DRIFT},
                    'trigger': 'action',
                    'commands': [buried_sluice_msg],
                },
                {
                    'cond': {'switch': S_OSS_PULLEY},
                    'through': True,
                    'commands': [],
                },
            ],
        })
    E.append({
        'type': 'event',
        'name': 'Sunken Elector Sluice Plinth',
        'at': [21, 27],
        'pages': [
            {
                'graphic': {'tile': T_SAND_DRIFT},
                'trigger': 'action',
                'commands': [buried_sluice_msg],
            },
            {
                'cond': {'switch': S_OSS_PULLEY},
                'graphic': {'tile': T_ROADSTONE_BASE},
                'trigger': 'action',
                'commands': [
                    "EXPOSED AUREL SLUICE PLINTH — 'When the western Dry Tide retreated, the first Electors buried the Vault's treasury beneath four cubits of dune-sand. Only the Script Vault counterweight drains the nave trough.'",
                ],
            },
        ],
    })
    sluice_coffer_ruby = (
        'pbSEPlay("Mining reveal", 90, 100)\n'
        'pbMessage(_INTL("With the dune-sand drained away, the bronze clasp yields easily! Inside the buried Elector coffer lie preserved vault relics!"))\n'
        'pbReceiveItem(:TELLURICSEED, 1)\n'
        'pbReceiveItem(:STARPIECE, 1)\n'
        '$game_self_switches[[624, @event_id, "A"]] = true\n'
        '$game_map.need_refresh = true'
    )
    E.append({
        'type': 'event',
        'name': 'Buried Sluice Relic Coffer',
        'at': [22, 27],
        'pages': [
            {
                'graphic': {'tile': T_SAND_DRIFT},
                'trigger': 'action',
                'commands': [buried_sluice_msg],
            },
            {
                'cond': {'switch': S_OSS_PULLEY},
                'graphic': {'tile': T_TRUNK_CLOSED},
                'trigger': 'action',
                'commands': [{'script': sluice_coffer_ruby}],
            },
            {
                'cond': {'switch': S_OSS_PULLEY, 'self': 'A'},
                'graphic': {'tile': T_TRUNK_OPEN},
                'trigger': 'action',
                'commands': [
                    "The ancient bronze-bound sluice coffer stands open and empty, dry dune-sand still clinging to its hinges.",
                ],
            },
        ],
    })

    # Field Notes Entry Plaque on solid pf_roadstone base (18, 35) (story/25_SCRIPT_CH6.md:395!)
    E.append(_sign(
        'Ossuary Field Notes Stele', (18, 35),
        "FIELD NOTES — THE OSSUARY OF DUNES (CAVE). Unown drift in and out of the sandstone walls. They aren't hiding — they're the words. (Larch's margin note: 'Copy everything. Twice.')"
    ))

    # Sundial Capstone (V551, cycles 0..3 -> reveals the 4 Aurel-era words & ACTUALLY unlocks Sanctum Seal S553!)
    sundial_ruby = (
        f'v = ($game_variables[{V_OSS_SUNDIAL}].to_i + 1) % 4\n'
        f'$game_variables[{V_OSS_SUNDIAL}] = v\n'
        'pbSEPlay("Strength push", 85, 95)\n'
        'lines = [\n'
        '  "The sundial capstone turns EAST — the sun-shaft illuminates an Unown glyph: K (KING).",\n'
        '  "The sundial capstone turns SOUTH — the sun-shaft illuminates an Unown glyph: C (CHAIN).",\n'
        '  "The sundial capstone turns WEST — the sun-shaft illuminates an Unown glyph: E (EIGHTEEN).",\n'
        '  "The sundial capstone clicks NORTH — all four ancient glyphs chime in unison!"\n'
        ']\n'
        'pbMessage(_INTL("{1}", lines[v]))\n'
        f'if v == 3 && !$game_switches[{S_OSS_SEAL}]\n'
        f'  $game_switches[{S_OSS_SEAL}] = true\n'
        '  $game_map.need_refresh = true\n'
        '  pbSEPlay("Mining reveal", 95, 95)\n'
        '  pfm_shake(2, 8, 12)\n'
        '  pbMessage(_INTL("Deep in the north sanctum, the ancient Elector seal-stone grinds open, unsealing the Script Vault archway!"))\n'
        'end'
    )
    E.append({
        'type': 'event',
        'name': 'Ossuary Sundial Capstone',
        'at': [21, 20],
        'pages': [{'graphic': {'tile': T_DIAL}, 'trigger': 'action', 'commands': [{'script': sundial_ruby}]}],
    })

    # Four Canonical Chapter 6 Murals (story/25_SCRIPT_CH6.md:402-423) mounted on SOLID carved glyph mural steles (hb_banner, pas=0xf)!
    # Mural II cleanly anchored against TER cliff wall at (17, 16) (0 floating portraits, 0 blue vases!)
    E += [
        _sign('Mural I — The Gilded King', (9, 18),
              "MURAL I: A king in gold on a throne under a sun, one hand raised as if weighing the sky itself. Below him, white domes and a harbour. His face has been scratched out with a chisel — all but the corner of a smile they missed. (Sahar's note: 'He isn't praying. He's giving the sun an order.')"),
        _sign('Mural II — Year of Two Weathers', (17, 16),
              "MURAL II: Two titans tearing at the land — one red rising out of the earth with fire in its back, one blue rising out of the sea with the tide in its arms. Between them, tiny armies hold golden chains along what is now Ossaria's western Dry Tide."),
        _sign('Mural III — The Eighteen-Lit Beast', (34, 18),
              "MURAL III: A great beast ringed by eighteen coloured lights, bound in a chain of eighteen golden locks held by the tiny figure of the golden king. Unown letters shift across the frame — spelling a warning someone tried to bury."),
        _sign('Mural IV — The Falling Lights', (18, 6),
              "MURAL IV: The great beast breaking apart — eighteen lights falling out of it like coloured rain while the golden city tips towers-first into the sea. Three hundred years later, Zenith was built on its roof."),
    ]

    # Warden Sahar Ostrand beside Mural IV in the North Sanctum (story/25_SCRIPT_CH6.md:425-430 -> S116 + V126=7, aware of S553!)
    sahar_ossuary_ruby = (
        'if $game_switches[116]\n'
        f'  if $game_switches[{S_OSS_SEAL}]\n'
        '    pbMessage(_INTL("Sahar: Keep your copy of the Duneholt Rubbing safe. The north seal-stone stands open — watch your step among the Unown inside the Script Vault."))\n'
        '  else\n'
        '    pbMessage(_INTL("Sahar: Keep your copy of the Duneholt Rubbing safe. If you want inside the Script Vault behind me, turn the central Sundial Capstone in the nave below until all four glyphs align."))\n'
        '  end\n'
        'else\n'
        '  pbMessage(_INTL("Sahar: I sealed this hall in AF 281 on Sovereign Valen\'s order. I burned my first rubbing and told my crew we\'d found a collapsed granary."))\n'
        '  pbMessage(_INTL("Sahar: Look at all four murals: the golden king, the two titans, the chain of eighteen locks, and the lights falling like rain while his city sank into the sea."))\n'
        '  pbSEPlay("Mining reveal", 90, 100)\n'
        '  pbMessage(_INTL("Sahar presses a sheet of heavy paper against the third mural and rubs it quickly with red wax — \'S.O., AF 300. AF 281.\'"))\n'
        '  pbMessage(_INTL("Sahar: I made two. Keep yours — I burned the first rubbing I ever made; I\'m not burning a second."))\n'
        '  pfm_set(:duneholt_rubbing, true) rescue nil\n'
        '  $game_switches[116] = true\n'
        '  $game_variables[126] = 7 if $game_variables[126].to_i < 7\n'
        '  $game_map.need_refresh = true\n'
        f'  if $game_switches[{S_OSS_SEAL}]\n'
        '    pbMessage(_INTL("Sahar: You already ground open the north seal-stone from the nave sundial — the Script Vault lies open ahead. Watch your step among the Unown."))\n'
        '  else\n'
        '    pbMessage(_INTL("Sahar: The north archway behind me still holds an Elector seal-stone. Align all four glyphs on the Sundial Capstone in the nave below to open the Script Vault."))\n'
        '  end\n'
        'end'
    )
    E.append({
        'type': 'event',
        'name': 'Sahar (Ossuary Sanctum)',
        'at': [23, 8],
        'pages': [{
            'graphic': {'sprite': 'SAHAR', 'dir': 'down'},
            'trigger': 'action',
            'move': 'fixed',
            'commands': [{'script': sahar_ossuary_ruby}],
        }],
    })

    # ALL 3 Canonical PBS # Map 624 Trainers (pbs/trainers.txt:13352-13524 — 0 duplicates, 100% OPEN sightlines!)
    E.append(_trainer_cave(
        (11, 24), 'RUINMANIAC', 'Anwar', 'left',
        "Ruin Maniac Anwar: The Unown along the west frieze are shifting into a battle stance — let's see who the murals favour!",
        "Ruin Maniac Anwar: The murals show a trainer winning here. I assumed it was me.",
        sight=3,
    ))
    E.append(_trainer_cave(
        (26, 20), 'CHANNELER', 'Shirin', 'down',
        "Channeler Shirin: Listen to the stone humming! The ancient voices inside the Ossuary woke when you crossed the skull-mouth!",
        "Channeler Shirin: They're restless. You woke them, you settle them.",
        sight=3,
    ))
    E.append(_trainer_cave(
        (32, 24), 'POKEMANIAC', 'Faisal', 'right',
        "Poké Maniac Faisal: Boulders, fossil ribs, and Unown — this catacomb is a collector's dream! Show me what you brought down here!",
        "Poké Maniac Faisal: Boulders, bones and me. One of us had to give.",
        sight=3,
    ))

    # Genuine Pushable Strength Boulders & Rock Smash Rocks Sealing 4 Carved Relic Alcoves!
    E += [
        _strength_boulder('Ossuary Boulder W', (5, 28)),
        _strength_boulder('Ossuary Boulder E', (38, 28)),
        _rock_smash((5, 20), 'Cracked Sandstone W'),
        _rock_smash((38, 20), 'Cracked Sandstone E'),
        {'type': 'item', 'at': [3, 20], 'item': 'ULTRABALL', 'name': 'Ossuary Ultra Ball'},
        {'type': 'item', 'at': [3, 30], 'item': 'SUNSTONE', 'name': 'Ossuary Sun Stone'},
        {'type': 'item', 'at': [40, 30], 'item': 'RAREBONE', 'name': 'Ossuary Rare Bone'},
        {'type': 'item', 'at': [40, 20], 'item': 'DUSKBALL', 'name': 'Ossuary Dusk Ball'},
        {'type': 'item', 'at': [15, 8], 'item': 'HYPERPOTION', 'name': 'Sanctum Hyper Potion'},
        {'type': 'item', 'name': 'HiddenItem (pool stone)', 'at': [19, 25], 'item': 'STARPIECE', 'hidden': True},
    ]

    # Protect warps, stairs, trainers, sightlines, sundial, sluice trough, alcove throats & murals
    for pt in [(21, 38), (22, 38), (21, 37), (22, 37), (21, 4), (22, 4), (21, 5), (22, 5),
               (10, 24), (9, 24), (8, 24), (26, 21), (26, 22), (26, 23), (33, 24), (34, 24), (35, 24),
               (6, 20), (4, 20), (6, 28), (4, 28), (3, 28), (4, 29), (4, 30),
               (37, 20), (39, 20), (37, 28), (39, 28), (40, 28), (39, 29), (39, 30),
               (20, 26), (21, 26), (22, 26), (23, 26), (20, 28), (21, 28), (22, 28), (23, 28)]:
        m.keep_clear.add(pt)
    for e in E:
        ex, ey = e['at']
        m.keep_clear.add((ex, ey))

    # ---- 3. Catacomb Architecture: Carved Ancient Glyph Mural Steles, Symmetrical Archway Columns & 14 Intact Braziers! ----
    # All 4 Canonical Murals mounted flush against sandstone cliff walls on solemn carved glyph steles (hb_banner, pas=0xf base -> 0 over_trigger?!)
    for mx, my in ((9, 18), (17, 16), (34, 18), (18, 6)):
        _place_stamp_over(m, 'hb_banner', mx, my - 2, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'pf_roadstone', 18, 34, base_z=1, top_z=2, top_rows=1, solid=True)  # Base (18,35) Field Notes!

    # Symmetrical North Script Vault Archway Framing (2-wide sealed doors at (21..22, 4) flanked symmetrically by lm_pillar at x=20 & x=23!)
    _place_stamp_over(m, 'lm_pillar', 20, 2, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'lm_pillar', 23, 2, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'wr_ban_bone', 19, 5, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'wr_ban_bone', 24, 5, base_z=1, top_z=2, top_rows=2, solid=True)

    # Sandstone colonnades & fallen columns (strictly clear of alcove mouths y=20, 28 and Mural II at (17, 16)!)
    for cx, cy in ((19, 34), (24, 34), (17, 27), (26, 27), (17, 19), (26, 17),
                   (7, 19), (12, 19), (31, 19), (36, 19), (15, 10), (28, 10)):
        _place_stamp_over(m, 'nr_col', cx, cy, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'nr_colfall', 29, 31, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'lm_statue', 26, 6, base_z=1, top_z=2, top_rows=2, solid=True)

    braziers_624 = [
        (19, 36), (24, 36),
        (18, 22), (25, 22), (18, 25), (25, 25),
        (7, 25), (12, 21),
        (31, 21), (36, 25),
        (16, 11), (27, 11),
        (19, 9), (24, 9),
    ]
    for bx, by in braziers_624:
        _place_stamp_over(m, 'fw_brazier', bx, by, base_z=1, top_z=2, top_rows=1, solid=True)

    m.paint()
    _paint_sandstone_floors(m, [
        (19, 31, 24, 38, 'plaza'),
        (18, 17, 25, 28, 'plaza'),
        (16, 6, 27, 12, 'mosaic'),
        (20, 4, 23, 12, 'plaza'),
        (7, 19, 13, 27, 'mosaic'),
        (30, 19, 36, 27, 'mosaic'),
    ])
    # Sunken dark drainage sluice channel directly beneath the S552 sandbank trough (20..23, 27)!
    t_mud = P1('cv_mud0')
    for sx in range(20, 24):
        m.L[0, 27, sx] = t_mud
        m.L[1, 27, sx] = 0
    # Scattered ancient bones along catacomb side corridors
    for bx, by, nm in ((10, 31, 'wr_bones0'), (33, 31, 'wr_bones1'), (8, 21, 'wr_bones1'), (35, 21, 'wr_bones0')):
        if int(m.L[1, by, bx]) == 0 and m.cls[by, bx] == '.' and not m.cliff[by, bx]:
            m.L[1, by, bx] = P1(nm)

    Lr = RC.resolve(m.L, TID_CAVE).astype(np.int32)
    _add_safe_overlay(Lr, TID_CAVE, 'cv_shaft', [(20, 19), (21, 6), (9, 19), (34, 19), (21, 33)])
    _add_safe_overlay(Lr, TID_CAVE, 'pf_glow', braziers_624)
    _assert_braziers_intact(Lr, TID_CAVE, braziers_624, 'Map 624')

    ev_pts = [tuple(e['at']) for e in E]
    PG.guard(Lr, TID_CAVE, ev_pts, 'Map 624')
    assert not PG.hits(Lr, R.tilesets()[TID_CAVE], ev_pts), 'Map 624 passguard hits!'
    _assert_no_over_trigger(Lr, TID_CAVE, E, 'Map 624')

    # Dual-State Exact Essentials 4-bit BFS Proof on Map 624 (respecting tile-graphic & rock_smash solidity!):
    def _exact_bfs_624(ev_list):
        import build as B
        ts = R.tilesets()[TID_CAVE]
        solid_ev = set()
        for e in ev_list:
            et = e.get('type')
            if et in ('npc', 'trainer', 'mart', 'rock_smash'):
                solid_ev.add(tuple(e['at']))
            elif et == 'event':
                pg0 = (e.get('pages') or [{}])[0]
                if pg0.get('through'):
                    continue
                g0 = pg0.get('graphic') or {}
                tid0 = g0.get('tile')
                if g0.get('sprite') or (tid0 and (ts['passages'][tid0] & 0x0f) == 0x0f):
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
        seen = {(21, 37)}
        q = deque([(21, 37)])
        while q:
            cx, cy = q.popleft()
            for dx, dy, d in ((0, 1, 2), (0, -1, 8), (1, 0, 6), (-1, 0, 4)):
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < W and 0 <= ny < H and (nx, ny) not in seen and ok[ny, nx]:
                    if edge_ok(cx, cy, d) and edge_ok(nx, ny, 10 - d):
                        seen.add((nx, ny))
                        q.append((nx, ny))
        return seen

    alcove_items = {(3, 20), (3, 30), (40, 20), (40, 30)}
    main_events = [e for e in E if tuple(e['at']) not in alcove_items]
    _verify_all_events_and_trainers(Lr, TID_CAVE, main_events, (21, 37), 'Map 624 [TRAINERS + MAIN]')
    seen_sealed = _exact_bfs_624(E)
    assert (21, 4) not in seen_sealed and (22, 4) not in seen_sealed, 'Map 624 LEAK: S553 archway reachable while sealed!'
    assert (21, 5) in seen_sealed and (22, 5) in seen_sealed, 'Map 624: sealed archway not inspectable from (21..22, 5)!'
    assert (20, 27) not in seen_sealed and (23, 27) not in seen_sealed, 'Map 624: S552 sandbank not solid before pulley!'
    for ap in alcove_items:
        assert ap not in seen_sealed and not any((ap[0]+dx, ap[1]+dy) in seen_sealed for dx, dy in ((0,1),(0,-1),(1,0),(-1,0))), (
            f'Map 624 LEAK: alcove item {ap} reachable without Strength/Rock Smash!'
        )
    #   2) Unlocked state (S553=True, S552=True, Rock Smash cleared, Strength boulders pushed 2 tiles deep to (3,28) & (40,28)!):
    unlocked_events = []
    for e in E:
        nm = e.get('name') or ''
        if e.get('type') == 'rock_smash' or nm.startswith('Sluice Sandbank'):
            continue
        if nm == 'Ossuary Boulder W':
            unlocked_events.append({**e, 'at': [3, 28]})
        elif nm == 'Ossuary Boulder E':
            unlocked_events.append({**e, 'at': [40, 28]})
        elif nm.startswith('North to Script Vault'):
            unlocked_events.append({**e, 'pages': [e['pages'][1]]})
        elif nm in ('Sunken Elector Sluice Plinth', 'Buried Sluice Relic Coffer'):
            unlocked_events.append({**e, 'pages': [e['pages'][1]]})
        else:
            unlocked_events.append(e)
    seen_open = _exact_bfs_624(unlocked_events)
    assert (21, 4) in seen_open and (22, 4) in seen_open, 'Map 624: S553 archway still blocked after unlocking!'
    assert (20, 27) in seen_open and (23, 27) in seen_open, 'Map 624: S552 sluice sandbank did not drain!'
    assert (21, 26) in seen_open and (22, 26) in seen_open, 'Map 624: S552 plinth/coffer not reachable after draining!'
    for ap in alcove_items:
        assert any((ap[0]+dx, ap[1]+dy) in seen_open for dx, dy in ((0,1),(0,-1),(1,0),(-1,0))), (
            f'Map 624: alcove item {ap} NOT reachable after Strength/Rock Smash!'
        )
    print(f'Map 624 Dual-State Proof PASSED: sealed={len(seen_sealed)} cells, open={len(seen_open)} cells (S553 seal, S552 drain, 4 Strength/Smash alcoves 100% verified!)')

    m.L = Lr
    head = {
        'id': 624,
        'name': 'Ossuary of Dunes',
        'parent': 620,
        'bgm': 'Cave',
        'field': 'CAVE',
        'map_audio': {'bgm': 'Dungeon - Ruins', 'bgs': 'Drip - Nadir', 'bgs_volume': 40, 'rain': False},
        'fog': {'name': 'prismfall_cave', 'opacity': 24, 'blend': 1, 'zoom': 100, 'sx': 1, 'sy': 0},
        'metadata': {'Name': 'Ossuary of Dunes', 'Outdoor': False, 'ShowArea': True, 'BattleBack': 'cave1', 'MapPosition': POS_624},
        'gates': [
            {'name': 'Ossuary Sanctum Seal (S553)', 'from': [[21, 37]], 'sealed': [[21, 4], [22, 4]]},
            {'name': 'Ossuary Strength & Smash Alcoves', 'from': [[21, 37]], 'sealed': [[3, 20], [3, 30], [40, 20], [40, 30]]},
        ],
        'tone': [-12, -16, -24, 16],
        '_file': '624_ossuary_of_dunes.yaml',
    }
    m.write(624, head, comment='# GENERATED by mapgen/layouts/ossaria_landmarks.py (Batch 3D): Ossuary of Dunes.\n'
                               '# Edit the layout script, not this file.\n')
    print('Wrote specs/624_ossuary_of_dunes.yaml and data/raw/624.npy')


# =================================================================================================
# 5. MAP 625 — OSSUARY OF DUNES - SCRIPT VAULT (34x30, TS 57 PF Rejuv Cave cvE, field :CAVE)
# =================================================================================================
def build_625():
    W, H = 34, 30
    m = Cave(W, H, 'E', seed=625, pool='Cave Pool', tid=TID_CAVE)
    m.STAIRS = (P1('E_stairl'), P1('E_stairm'), P1('E_stairr'))
    m.kit = {MASS: 'cvE', TER: 'cvE', FLOOR: 'cvE', 'default': 'cvE'}

    # ---- 1. Carve Sacred Subterranean Tablet & Scroll Archive (34x30, cvE 3-row cliffs!) ----
    # South Archive Entry Vestibule (FLOOR): x=12..21, y=21..28 (return warps to 624 at (16..17, 28)!)
    m.box(12, 21, 21, 28, FLOOR, '.')
    # Central Inscribed Archive Nave (FLOOR): x=10..23, y=12..23 (directly meets TER y=11 for 3-row stair!)
    m.box(10, 12, 23, 23, FLOOR, '.')
    # West Tablet & Odd-Keystone Alcove (FLOOR): x=3..11, y=13..22
    m.box(3, 13, 11, 22, FLOOR, '.')
    # East Scroll Archive & Spiritomb Hallowed Plinth (FLOOR): x=22..30, y=13..22
    m.box(22, 13, 30, 22, FLOOR, '.')
    # North Elevated Script Sanctum (TER): x=9..24, y=3..11 (Unown Glyph-Swarm Altar & 5x5 lm_sun inlay!)
    m.box(9, 3, 24, 11, TER, '.')

    m.mass_at([
        (3, 13), (3, 22), (30, 13), (30, 22),
        (12, 28), (21, 28), (9, 3), (24, 3),
    ])

    # Grand 4-wide Sandstone Stairs ascending to the Elevated Script Sanctum (x=15..18, y=11..13)
    m.stairs(15, 11, w=4, n=3, c='.')
    m.plan_cliffs(rows=3)

    # ---- 2. Events: Return Warp -> 624, Sand Pulley (S552), 4 Unown Plinths, Spiritomb, Unown Guardian! ----
    E = m.events

    # Bidirectional South Return Warps -> 624 Ossuary of Dunes (21, 5, down)!
    for rx in (16, 17):
        E.append({
            'type': 'warp',
            'name': 'South to Ossuary of Dunes (624)' + (' ' if rx == 17 else ''),
            'at': [rx, 28],
            'to': {'map': 624, 'x': 21, 'y': 5, 'dir': 'down'},
            'se': 'Door exit',
        })

    # Vault Sand-Pulley Wheel (DUNGEON_PUZZLES.md S552 — wired live to Map 624 Central Nave Sluice Trough (20..23, 27)!)
    pulley_ruby = (
        f's = !$game_switches[{S_OSS_PULLEY}]\n'
        f'$game_switches[{S_OSS_PULLEY}] = s\n'
        'pbSEPlay("Strength push", 90, 90)\n'
        'pfm_shake(2, 8, 10)\n'
        '$game_map.need_refresh = true\n'
        'if s\n'
        '  pbMessage(_INTL("CLANK! The bronze counterweight drops — fine sand drains out of the Ossuary\'s central nave sluice trough below the spring pool, exposing a buried Elector plinth and relic coffer!"))\n'
        'else\n'
        '  pbMessage(_INTL("CLANK! You wind the counterweight back up — dry dune-sand pours back across the Ossuary\'s central sluice trough."))\n'
        'end'
    )
    E.append({
        'type': 'event',
        'name': 'Vault Sand-Pulley Wheel',
        'at': [14, 24],
        'pages': [
            {'graphic': {'tile': T_LEVER_L}, 'trigger': 'action', 'commands': [{'script': pulley_ruby}]},
            {'cond': {'switch': S_OSS_PULLEY}, 'graphic': {'tile': T_LEVER_R}, 'trigger': 'action', 'commands': [{'script': pulley_ruby}]},
        ],
    })

    # Solid Carved Ancient Stone Steles (pf_roadstone bases, pas=0xf -> ZERO over_trigger?, ZERO blue vases!)
    E += [
        _sign('West Tablet — Aurel Cipher I', (5, 18),
              "AUREL-ERA STONE TABLET I: 'H - O - L ...' Rows of carved Unown script describe a golden monarch who mistook eighteen blessings for eighteen locks."),
        _sign('West Tablet — Aurel Cipher II', (9, 18),
              "AUREL-ERA STONE TABLET II: '... L - O - W.' Scratched in fresh chalk along the base in Sahar's neat script: 'Read the six tall letters together. Someone else found this word before us.'"),
        _sign('East Scroll — Missing Mural Letter', (24, 18),
              "SEALED ARCHIVE TABLET (CURATOR NASRIN'S CLUE): A complete rubbing of the Mural Gallery's third inscription! The chiseled-out letter at the end of the Elector's sentence is Unown 'S' — turning 'SEALED' into 'STOLEN.'"),
        _sign('Archive Index Plinth', (19, 24),
              "THE SCRIPT VAULT — 'All things written on bone endure longer than crowns. Do not disturb the Hallowed Stone on the east dais unless you carry an Odd Keystone.'"),
    ]

    # Static Spiritomb Encounter on East Hallowed Stone Shrine (lm_cradle_cracked at (28, 16..17), solid pas=0xf base!)
    # CRITICAL P0 FIX: Verify real Essentials v21 WildBattle outcome ([1=win, 4=catch]) BEFORE consuming ODDKEYSTONE or setting S554!
    spiritomb_ruby = (
        f'if $game_switches[{S_OSS_SPIRITOMB}]\n'
        '  pbMessage(_INTL("The ancient sandstone well-plinth stands silent now, its hundred-and-eight carved fissures cool to the touch."))\n'
        'elsif ($bag.has?(:ODDKEYSTONE) rescue false)\n'
        '  if pbConfirmMessage(_INTL("A weathered hollow stone tower hums with eerie cold! Fit your Odd Keystone into its carved socket?"))\n'
        '    pbSEPlay("Anim/HealBell", 85, 70)\n'
        '    pfm_shake(3, 10, 14)\n'
        '    pbMessage(_INTL("A swirl of violet mist erupts from the cracked keystone — SPIRITOMB materializes from the vault\'s shadow!"))\n'
        '    setBattleRule("field", :CAVE)\n'
        '    setBattleRule("outcomeVar", 1)\n'
        '    $game_variables[1] = 0\n'
        '    if WildBattle.start(:SPIRITOMB, 32) && [1, 4].include?($game_variables[1])\n'
        '      $bag.remove(:ODDKEYSTONE, 1) rescue nil\n'
        f'      $game_switches[{S_OSS_SPIRITOMB}] = true\n'
        '      $game_map.need_refresh = true\n'
        '      pbMessage(_INTL("The violet mist settles back into the cracked stone. Your Odd Keystone locks into the Hallowed Stone as the shrine grows still."))\n'
        '    else\n'
        '      pbMessage(_INTL("The violet mist recedes back into the socket. Your Odd Keystone remains cold in your bag — you can challenge the Hallowed Stone again when ready."))\n'
        '    end\n'
        '  end\n'
        'else\n'
        '  pbMessage(_INTL("An ancient hollow stone shrine covered in Unown wards. A notched round socket waits for an Odd Keystone."))\n'
        'end'
    )
    E.append({
        'type': 'event',
        'name': 'Hallowed Stone (Spiritomb)',
        'at': [28, 17],
        'pages': [{'trigger': 'action', 'commands': [{'script': spiritomb_ruby}]}],
    })

    # Optional North Sanctum Unown Glyph-Swarm Guardian Altar — centered squarely at (16, 7) on lm_sun medallion!
    # CRITICAL P0 FIX: setBattleRule("cannotRun") + explicit [1, 4].include?($game_variables[1]) prevents flee-for-loot!
    swarm_ruby = (
        f'if $game_switches[{S_OSS_SWARM}]\n'
        '  pbMessage(_INTL("The golden sundial altar rests peacefully. Faint Unown glyphs drift up the light-shaft, forming a quiet circle."))\n'
        'else\n'
        '  pbMessage(_INTL("Scores of Unown orbit the sunlit sandstone altar, humming in tight harmonic rings!"))\n'
        '  if pbConfirmMessage(_INTL("Step forward and read the living sentence aloud? (Optional Vault Guardian battle!)"))\n'
        '    pbSEPlay("Mining reveal", 95, 90)\n'
        '    pfm_shake(2, 10, 12)\n'
        '    pbMessage(_INTL("The hovering glyphs lock into a blinding formation — the Vault\'s ancient Unown guardian descends!"))\n'
        '    setBattleRule("field", :CAVE)\n'
        '    setBattleRule("cannotRun")\n'
        '    setBattleRule("outcomeVar", 1)\n'
        '    $game_variables[1] = 0\n'
        '    if WildBattle.start(:UNOWN, 33) && [1, 4].include?($game_variables[1])\n'
        f'      $game_switches[{S_OSS_SWARM}] = true\n'
        '      pfm_set(:unown_report, true) rescue nil\n'
        '      $game_map.need_refresh = true\n'
        '      pbMessage(_INTL("The swarm parts reverently! You transcribe their complete Unown Report and claim the relics beneath the altar."))\n'
        '      pbReceiveItem(:TELLURICSEED, 2)\n'
        '      pbReceiveItem(:SPELLTAG, 1)\n'
        '    else\n'
        '      pbMessage(_INTL("The hovering Unown scatter back into the shaft of light, leaving the altar sealed until a challenger overcomes them."))\n'
        '    end\n'
        '  end\n'
        'end'
    )
    E.append({
        'type': 'event',
        'name': 'Unown Glyph-Swarm Altar',
        'at': [16, 7],
        'pages': [{'trigger': 'action', 'commands': [{'script': swarm_ruby}]}],
    })

    # Verified Pickups (including ODDKEYSTONE in West Relic Alcove so Spiritomb is 100% playable!)
    E += [
        {'type': 'item', 'at': [5, 20], 'item': 'ODDKEYSTONE', 'name': 'Vault Odd Keystone'},
        {'type': 'item', 'at': [11, 7], 'item': 'LIGHTCLAY', 'name': 'Vault Light Clay'},
        {'type': 'item', 'at': [22, 7], 'item': 'RAREBONE', 'name': 'Vault Rare Bone'},
        {'type': 'item', 'at': [27, 20], 'item': 'DUSKBALL', 'name': 'Vault Dusk Ball'},
        {'type': 'item', 'name': 'HiddenItem (scroll rack)', 'at': [21, 18], 'item': 'STARPIECE', 'hidden': True},
    ]

    for pt in [(16, 28), (17, 28), (16, 27), (17, 27), (16, 11), (17, 11), (16, 12), (17, 12), (16, 13), (17, 13),
               (16, 8), (15, 7), (17, 7), (27, 17), (29, 17), (28, 18), (28, 16)]:
        m.keep_clear.add(pt)
    for e in E:
        ex, ey = e['at']
        m.keep_clear.add((ex, ey))

    # ---- 3. Sacred Tablet/Scroll Archive Architecture: Carved Stone Steles, Uncrowded Spiritomb Shrine & 12 Intact Braziers! ----
    # Solid carved stone steles (pf_roadstone, y-1..y -> pas=0xf base at y, ZERO blue vases, 1 tile clear of mn_books2!)
    for px, py in ((5, 18), (9, 18), (24, 18), (19, 24)):
        _place_stamp_over(m, 'pf_roadstone', px, py - 1, base_z=1, top_z=2, top_rows=1, solid=True)

    # Centered Unown Glyph-Swarm Altar on gold-trimmed stone relic pedestal (lm_cradle_cold at (16, 6..7) -> solid base (16, 7)!)
    _place_stamp_over(m, 'lm_cradle_cold', 16, 6, base_z=1, top_z=2, top_rows=1, solid=True)
    # Uncrowded East Spiritomb Hallowed Stone Shrine (lm_cradle_cracked at (28, 16..17) -> solid violet-wisp shrine base (28, 17)!)
    _place_stamp_over(m, 'lm_cradle_cracked', 28, 16, base_z=1, top_z=2, top_rows=1, solid=True)

    # Towering stone tablet & scroll racks lining West & East Archive walls (clear of Spiritomb's east shrine dais!)
    _place_stamp_over(m, 'mn_books2', 4, 15, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'mn_books2', 8, 15, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'mn_books2', 23, 15, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'mn_books', 11, 16, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'mn_books', 22, 16, base_z=1, top_z=2, top_rows=1, solid=True)

    # Classical sandstone columns, royal sun banners (strictly on cliff wall y=3..4 clear of y=5 sundial!) & candelabrums
    for cx, cy in ((13, 25), (20, 25), (13, 18), (20, 18), (12, 8), (21, 8), (12, 5), (21, 5)):
        _place_stamp_over(m, 'nr_col', cx, cy, base_z=1, top_z=2, top_rows=1, solid=True)
    # Symmetrical sun banners around x=16 axis on cliff face y=3..4 (L[2] keeps sandstone cliff intact behind banners, 0 overlap with sundial!)
    _place_stamp_over(m, 'lm_banner_w', 14, 3, base_z=2, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'lm_banner_w', 18, 3, base_z=2, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'wr_ban_bone', 13, 5, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'wr_ban_bone', 20, 5, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'mn_candelabra', 14, 15, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'mn_candelabra', 19, 15, base_z=1, top_z=2, top_rows=1, solid=True)

    braziers_625 = [
        (14, 27), (19, 27),
        (14, 21), (19, 21),
        (4, 19), (9, 20),
        (24, 20), (26, 16),
        (13, 9), (20, 9),
        (11, 5), (22, 5),
    ]
    for bx, by in braziers_625:
        _place_stamp_over(m, 'fw_brazier', bx, by, base_z=1, top_z=2, top_rows=1, solid=True)

    m.paint()
    _paint_sandstone_floors(m, [
        (14, 21, 19, 28, 'plaza'),
        (12, 16, 21, 21, 'plaza'),
        (4, 17, 10, 21, 'mosaic'),
        (23, 17, 29, 21, 'mosaic'),
        (11, 5, 22, 10, 'mosaic'),
        (14, 6, 19, 10, 'plaza'),
    ])
    # Center 5x5 golden sundial floor inlay directly centered beneath the Unown Altar (16, 7) at (14, 5) (x=14..18, y=5..9)!
    _paint_sun_medallion(m, 14, 5)

    Lr = RC.resolve(m.L, TID_CAVE).astype(np.int32)
    _add_safe_overlay(Lr, TID_CAVE, 'cv_shaft', [(15, 5), (17, 5), (7, 17), (26, 17), (16, 18)])
    _add_safe_overlay(Lr, TID_CAVE, 'pf_glow', braziers_625 + [(16, 7), (28, 17)])
    _assert_braziers_intact(Lr, TID_CAVE, braziers_625, 'Map 625')

    ev_pts = [tuple(e['at']) for e in E]
    PG.guard(Lr, TID_CAVE, ev_pts, 'Map 625')
    assert not PG.hits(Lr, R.tilesets()[TID_CAVE], ev_pts), 'Map 625 passguard hits!'
    _assert_no_over_trigger(Lr, TID_CAVE, E, 'Map 625')
    _verify_all_events_and_trainers(Lr, TID_CAVE, E, (16, 27), 'Map 625 Script Vault')

    m.L = Lr
    head = {
        'id': 625,
        'name': 'Ossuary of Dunes - Script Vault',
        'parent': 624,
        'bgm': 'Cave',
        'field': 'CAVE',
        'map_audio': {'bgm': 'Dungeon - Ruins', 'bgs': 'Drip - Nadir', 'bgs_volume': 35, 'rain': False},
        'fog': {'name': 'prismfall_cave', 'opacity': 20, 'blend': 1, 'zoom': 100, 'sx': 1, 'sy': 0},
        'metadata': {'Name': 'Ossuary Script Vault', 'Outdoor': False, 'ShowArea': True, 'BattleBack': 'cave1', 'MapPosition': POS_624},
        'tone': [-8, -14, -20, 14],
        '_file': '625_ossuary_of_dunes_script_vault.yaml',
    }
    m.write(625, head, comment='# GENERATED by mapgen/layouts/ossaria_landmarks.py (Batch 3D): Ossuary of Dunes - Script Vault.\n'
                               '# Edit the layout script, not this file.\n')
    print('Wrote specs/625_ossuary_of_dunes_script_vault.yaml and data/raw/625.npy')


def main():
    build_606()
    build_610()
    build_611()
    build_624()
    build_625()
    print('Done: wrote 5 Ossaria landmark & archaeological dungeon maps (606, 610, 611, 624, 625).')


if __name__ == '__main__':
    main()
