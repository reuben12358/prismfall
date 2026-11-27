#!/usr/bin/env python3
"""mapgen/layouts/whalebone_keep.py — Act 3 Batch 3H Builder: Whalebone Keep Complex (305, 306, 307, 308).

Builds the 4 royal fortress & ice-vault maps of Isenmar to First-Pass Critic Gold Standard:
  - 305 Whalebone Keep - Bailey       (36x32, TS 52 PF Rejuv Snow, Outdoor, :SNOWY_MOUNTAIN, rubric: true)
  - 306 Whalebone Keep - Mead Hall    (31x21, TS 59 PF Rejuv Manor, Interior, Great Tally & Vault Stair)
  - 307 Whalebone Keep - Thane's Seat (25x23, TS 59 PF Rejuv Manor, Interior, Thane Eirik's Whale-Skull Throne)
  - 308 Whalebone Keep - Ice Vault    (33x33, TS 57 PF Rejuv Cave,  Subterranean Ice Ruins, :FROZEN_LAKE, GATE ok)

Canonical sources: design/maps.json, design/DUNGEON_PUZZLES.md, design/FLAGS.md, design/WALKTHROUGH.md,
story/30_SCRIPT_CH11.md, story/03_CAST.md, plugins/Prismfall Trials/.

Run:
  /usr/bin/python3 -I mapgen/layouts/whalebone_keep.py
"""
import os
import random
import subprocess
import sys
import tempfile
import types
from collections import deque

LAYOUT_DIR = os.path.dirname(os.path.abspath(__file__))
HERE = os.path.dirname(LAYOUT_DIR)
for p in (HERE, LAYOUT_DIR):
    if p not in sys.path:
        sys.path.insert(0, p)

import numpy as np
import yaml

import rkit as K
from rkit import C, P1, STAMPS
import rcompose as RC
import render as R
import passguard as PG
import craftkit as CK
from cavekit import Cave, FLOOR, TER, MASS
from manor import Manor
from terrain import vnoise

from rimeholt_town import (
    TID_SNOW, RIME_POS, SPEC_DIR, RAW_DIR,
    ALPINE_WOODS, KF_TEAL_PINE_A, KF_TEAL_PINE_B, KF_SPRUCE_A, KF_SPRUCE_B,
    KF_SHRUB_A, KF_SHRUB_B, KF_BOULDER,
    GLACIER_9, GLACIER_CENTER, SNOW_BASE, SAFE_CRACKS, SAFE_PUDDLES, SAFE_FROST,
    _snowmap, _smooth_cls, _put_sprite, _infill_winter, _dress_snow_details,
    _guarded_unbuilt_transfer, _make_npc, _sign, _reserve_mask,
    _seal_unconnected_edges, _verify_map, _paint_wharf,
)

TID_MANOR = 59
TID_CAVE = 57


# =================================================================================================
# Nordic Timber-and-Stone Palace Builder (TS 59 — Zero Exterior Sky Windows, Zero Detached pf_glow!)
# =================================================================================================
class NordicKeep(Manor):
    """Grand Viking-Nordic timber & ash-slate hall builder for Whalebone Keep (306 Mead Hall, 307 Thane's Seat)."""

    def __init__(self, W, H, seed, tid=TID_MANOR):
        Cave.__init__(self, W, H, 'F', seed, pool='Cave Pool', tid=tid)
        self.kit = {'default': 'cvF', TER: 'cvB'}
        self.STAIRS = tuple(P1('st_stair_' + k) for k in 'lmr')
        self.rooms = []
        self.late = []
        self.floor_overrides = []

    def hall_floor(self, x0, y0, x1, y1, style='slate'):
        self.floor_overrides.append((x0, y0, x1, y1, style))

    def _apply_custom_floors(self):
        L = self.L
        slate = [P1('T_f%d' % i) for i in range(4)]
        planks = [P1('N_f%d' % i) for i in range(4)]
        walnut = [P1('H_f%d' % i) for i in range(4)]
        for x0, y0, x1, y1, style in self.floor_overrides:
            pal = slate if style == 'slate' else (planks if style == 'planks' else walnut)
            for y in range(max(0, y0), min(self.H, y1 + 1)):
                for x in range(max(0, x0), min(self.W, x1 + 1)):
                    if self.cls[y, x] != '.' or self.cliff[y, x]:
                        continue
                    L[0, y, x] = pal[(x * 3 + y * 5) % len(pal)]

    def paint(self):
        self.floor_ids = {P1('F_f%d' % v) for v in range(4)}
        Cave.paint(self)
        self.reskin()
        self._apply_custom_floors()

        carpets = {P1('mn_rug%s_%s' % (k, p)) for k in 'RBG' for p in ('nw', 'n', 'ne', 'w', 'c', 'e', 'sw', 's', 'se', 'c2')}
        stair_set = set(self.STAIRS)
        for z, x, y, t in self.late:
            if not (0 <= x < self.W and 0 <= y < self.H):
                continue
            if int(self.L[2, y, x]) in stair_set and z == 2 and t not in stair_set:
                continue
            if z == 1 and int(self.L[1, y, x]) in carpets and t not in carpets and not int(self.L[2, y, x]):
                z = 2
            self.L[z, y, x] = t

        self.paint_stairs()
        ts = self.ts()
        VB = RC.VBASE
        for y in range(self.H):
            for x in range(self.W):
                t1, t2 = int(self.L[1, y, x]), int(self.L[2, y, x])
                if t1 and t1 < VB and t2 and t2 < VB and ts['passages'][t1] & 15 == 15 and ts['passages'][t2] & 15 == 0 and ts['priorities'][t2] == 0:
                    self.L[2, y, x] = 0
        return self.L


def _assert_braziers_intact(Lr, tid, braziers, label):
    br_ref = RC.resolve(np.array(STAMPS['fw_brazier']['layers'], dtype=np.int32), tid)
    flame_tid = int(br_ref[2, 0, 0])
    for bx, by in braziers:
        assert int(Lr[2, by, bx]) == flame_tid, f'{label}: brazier flame damaged at ({bx},{by}): {Lr[2, by, bx]} != {flame_tid}'


# =================================================================================================
# 1. MAP 305 — WHALEBONE KEEP - BAILEY (36x32, TS 52, Outdoor, :SNOWY_MOUNTAIN, rubric: true)
# =================================================================================================
def build_305():
    W, H = 36, 32
    m = _snowmap(W, H, 305, kit='shs3')
    rng = random.Random(30511)

    # ---- 1. Fortified Rock-Island Citadel Courtyard in Frozen Lake Rime (Asymmetric Natural Island!) ----
    m.cls[:, :] = 'o'
    for y in range(H):
        for x in range(W):
            if (x <= 1 or x >= W - 2 or y >= H - 2) and vnoise(x, y, 3059, 3.0) > 0.45:
                m.cls[y, x] = 'W'

    # Elevated Keep Citadel Plateau (ht=1, x=2..33, y=0..18 — natural asymmetric rock crag!)
    for y in range(0, 19):
        for x in range(2, 34):
            m.ht[y, x] = 1
            m.cls[y, x] = '.'

    # Dense windswept alpine snow-spruce & crag ridges framing NW/W/NE castle flanks
    for y in range(0, 19):
        for x in range(0, W):
            if y < 2 or x <= 2 or x >= 33:
                if 0 <= x <= 35 and y <= 17:
                    m.cls[y, x] = 'T' if (y < 6 or x <= 3 or x >= 32) else 'o'
    # Organic crag spruce pockets on West plateau edge (x=2..4, y=14..18) & SE shoreline (x=27..32, y=24..29)
    for y in range(14, 19):
        for x in (2, 3):
            m.cls[y, x] = 'T'

    # Dense alpine snow-spruce ridge behind North Curtain Parapets (y=2..3 -> ZERO raw ice rectangles behind walls!)
    for y in range(2, 4):
        for x in list(range(5, 10)) + list(range(22, 31)):
            m.cls[y, x] = 'T'
    for x in list(range(5, 10)) + list(range(22, 31)):
        m.cls[4, x] = '.'

    # Lower South Rock-Island Forecourt (ht=0, x=5..30, y=19..29 — slightly wider East bastion!)
    for y in range(19, 30):
        for x in range(5, 31):
            m.cls[y, x] = '.'
    for y in range(25, 30):
        for x in range(5, 9):
            m.cls[y, x] = 'T'
    for y in range(26, 30):
        for x in range(27, 31):
            m.cls[y, x] = 'T'
    for cx, cy in ((5, 19), (5, 29), (30, 19), (30, 29), (29, 29)):
        m.cls[cy, cx] = 'o'

    # Packed-snow citadel avenues & asymmetric Bailey Ice Court
    m.rect(12, 6, 8, 13, 'd')                        # Upper Keep Portal Approach (x=12..19, y=6..18)
    m.rect(18, 10, 12, 7, 'I', only='.T')            # Shimmering East Bailey Ice Training Court
    m.rect(13, 7, 6, 12, 'd')
    m.rect(10, 22, 16, 6, 'd', only='.T')            # Lower South Forecourt Plaza
    m.rect(14, 22, 4, 10, 'd')                       # South Causeway -> 300 Thane's Harbour (x=14..17, y=31!)
    m.rect(22, 21, 14, 4, 'd')                       # East Causeway -> 304 Sled Market (x=35, y=21..24, clear of cliff!)
    m.rect(9, 21, 18, 3, 'd', only='.T')
    # Twin Grand Stone Staircases climbing Lower Forecourt -> Elevated Bailey Courtyard (y=18..20)!
    m.stairs(10, 18, w=3, n=3, c='d')
    m.stairs(21, 18, w=3, n=3, c='d')

    # Re-assert crisp exact open edge strips (South x=14..17 y=31, East x=35 y=21..24)
    m.cls[29:32, 14:18] = 'd'
    m.cls[21:25, 29:36] = 'd'

    # Clean flat snow yards under flanking citadel halls before plan_cliffs
    for x0, y0, x1, y1 in ((4, 8, 8, 14), (23, 8, 30, 13)):
        for yy in range(y0, y1 + 1):
            for xx in range(x0, x1 + 1):
                m.cls[yy, xx] = '.'

    m.plan_cliffs(rows=3)

    # ---- 2. Towering Whalebone Keep Portal Facade, ONLY 2 Corner Watchtowers & Flanking Halls ----
    m.stamp('gt_gate6', 10, 0)       # Grand Whalebone Keep Great Hall Portal (12x8 -> open 6-wide x=13..18, y=6..7!)
    m.stamp('gt_tower', 2, 1)        # NW Bastion Watchtower (ONLY 2 outer towers!)
    m.stamp('gt_tower', 31, 1)       # NE Bastion Watchtower
    m.stamp('kf_aframe', 4, 8)       # West Glacial Watch-Chapel (5x7 -> x=4..8, y=8..14)
    m.stamp('wb_long2', 23, 8)       # East Hirdmen Longhouse Barracks (8x6 -> x=23..30, y=8..13)

    # ---- 3. Events: Warps to 300/304/306, Canonical Keep Guards, Skalds, Plaques & Pickups ----
    E = []
    # Full 6-wide North Grand Keep Portal (13..18, 6) -> 306 Whalebone Keep - Mead Hall (15, 18, up)
    for nx in range(13, 19):
        E.append({'type': 'warp', 'name': f'Into Mead Hall {nx}', 'at': [nx, 6],
                  'to': {'map': 306, 'x': 15, 'y': 18, 'dir': 'up'}, 'se': 'Door enter'})
    # Full 4-wide South Causeway Gate (14..17, 31) -> 300 Thane's Harbour (23, 1, down)
    for sx in range(14, 18):
        E.append({'type': 'warp', 'name': f'South to Thanes Harbour {sx}', 'at': [sx, 31],
                  'to': {'map': 300, 'x': 23, 'y': 1, 'dir': 'down'}, 'se': 'Door exit'})
    # Full 4-wide East Causeway Bridge (35, 21..24) -> 304 Sled Market (12, 1, down)
    for ey in range(21, 25):
        E.append({'type': 'warp', 'name': f'East to Sled Market {ey}', 'at': [35, ey],
                  'to': {'map': 304, 'x': 12, 'y': 1, 'dir': 'down'}, 'se': 'Door exit'})

    # Canonical Whalebone Keep Bailey NPCs
    E.append(_make_npc('Hirdman Captain', (12, 9), 'trainer_ISENMAR_OFFICER', 'down', [
        "Hirdman Captain: Whalebone Keep — royal seat of Thane Eirik Sorrel on the rock island of Lake Rime.",
        "Hirdman Captain: Step straight through the north portal into the Mead Hall. The hearth fire never goes out for travellers.",
    ]))
    E.append(_make_npc('Portal Hirdman', (19, 9), 'trainer_ISENMAR_HIRDMAN', 'down', [
        "Portal Hirdman: Beyond the Mead Hall sits the Thane's Seat — and beneath its flagstones, the ancient Ice Vault carved straight into lake bedrock.",
    ]))
    E.append(_make_npc('Citadel Skald', (10, 15), 'NPC 25', 'right', [
        "Citadel Skald: Three centuries ago the first Thane hauled a sea-leviathan's ribs up this rock and built his roof beneath them.",
        "Citadel Skald: Every winter since, the lake froze three fathoms thick around this island... until this year.",
    ]))
    E.append(_make_npc('East Causeway Watch', (27, 22), 'trainer_ISENMAR_SOLDIER_M', 'left', [
        "Causeway Watch: The east timber bridge drops straight onto the Sled Market. War-sleds have been rolling out since sunrise.",
    ]))
    E.append(_make_npc('South Gate Sentinel', (13, 25), 'trainer_ISENMAR_SOLDIER_F', 'right', [
        "Gate Sentinel: Mind the wind off the narrows crossing back south to Thane's Harbour!",
    ]))

    # Solid Citadel Signposts (0 over_trigger?!)
    E.append(_sign('Whalebone Keep Plaque', (11, 14),
                   "WHALEBONE KEEP — SEAT OF THE THANES OF ISENMAR\n↑ Great Mead Hall & Thane's Seat · ↓ Thane's Harbour · → Sled Market"))
    E.append(_sign('East Causeway Sign', (25, 26),
                   "EAST CAUSEWAY BRIDGE — → RIMEHOLT SLED MARKET."))

    # Pickups (explicit hidden=False on visible item!)
    E.append({'type': 'item', 'name': 'Item (Ice Stone)', 'at': [6, 16], 'item': 'ICESTONE', 'hidden': False})
    E.append({'type': 'item', 'name': 'HiddenItem (Big Pearl)', 'at': [10, 27], 'item': 'BIGPEARL', 'hidden': True})

    ev_mask = _reserve_mask(m, E, extra=[
        (13, 7), (14, 7), (15, 7), (16, 7), (17, 7), (18, 7), (16, 8),
        (16, 30), (34, 22), (11, 13), (25, 25),
        (10, 18), (11, 18), (12, 18), (21, 18), (22, 18), (23, 18),
        (10, 21), (11, 21), (12, 21), (21, 21), (22, 21), (23, 21),
    ], pad=1)

    # ---- 4. Fortified Bailey Props: Watch-Beacons, Braziers, Banners, Whale Skulls, Racks & Snow Pines ----
    m.stamp('pf_signpost', 11, 13)   # solid base (11, 14)
    m.stamp('pf_signpost', 25, 25)   # solid base (25, 26)

    for nm, x, y in (
        ('pf_beacon', 9, 7), ('pf_beacon', 21, 7),
        ('pf_beacon', 8, 22), ('pf_beacon', 23, 26),
        ('fw_brazier', 12, 11), ('fw_brazier', 19, 11),
        ('fw_brazier', 13, 27), ('fw_brazier', 18, 27),
        ('fw_brazier', 28, 25), ('fw_brazier', 26, 15),
        ('wr_ban_ise', 9, 10), ('wr_ban_ise', 22, 10),
        ('wr_ban_ise', 12, 23), ('wr_ban_ise', 19, 23),
        ('fw_skull', 9, 13), ('fw_skull', 22, 14),
        ('fw_skull', 11, 25), ('fw_skull', 21, 25),
        ('wr_rack', 9, 8), ('wr_rack', 21, 9), ('wr_rack', 29, 14),
        ('wr_sledfort', 24, 14), ('wr_sledfort2', 20, 26),
        ('fw_sled', 18, 15), ('pf_sledge', 20, 24),
        ('sh_crates', 27, 15), ('fw_wood', 6, 15), ('hb_barrels', 9, 24), ('fw_rack', 24, 25),
        ('pf_stonebench', 9, 16), ('pf_stonebench', 21, 16),
        ('pf_lantern', 12, 15), ('pf_lantern', 19, 15),
        ('pf_lantern', 13, 22), ('pf_lantern', 18, 22),
    ):
        s = STAMPS[nm]
        if m.inb(x, y) and m.free(x, y, s['w'], s['h'], on='.dI') and not ev_mask[y:y + s['h'], x:x + s['w']].any():
            m.stamp(nm, x, y, mark='B')

    # Beached longboat cleanly on snowy south shore (ZERO snow-boxed fw_boat_over stickers in open blue water!)
    for nm, x, y in (
        ('fw_boat', 20, 29),
    ):
        s = STAMPS[nm]
        if m.inb(x, y) and m.free(x, y, s['w'], s['h'], on='oWI.') and not ev_mask[y:y + s['h'], x:x + s['w']].any():
            m.stamp(nm, x, y, mark='B')

    for tx, ty, sp in (
        (4, 14, KF_TEAL_PINE_A), (31, 13, KF_TEAL_PINE_B), (6, 21, KF_SPRUCE_A), (27, 26, KF_SPRUCE_B),
        (7, 17, KF_SHRUB_A),
    ):
        _put_sprite(m, tx, ty, *sp, on='.T', avoid_mask=ev_mask)

    R_ = types.SimpleNamespace(m=m, seed=305, road_mask=np.isin(m.cls, ['d']), events=E, rng=rng)
    CK.thin_bands(R_, passes=1)
    CK.woods(R_, ALPINE_WOODS, scale=7.0, accents={'snowblue': 0.08})

    m.events = E
    m.paint()
    _infill_winter(R_, ALPINE_WOODS, scale=7.0, seed=305)

    # Snow-capped glacial boulders protruding from frozen Lake Rime surround (authentic winter crags!)
    for bx, by in ((1, 19), (2, 26), (32, 26), (32, 16)):
        _put_sprite(m, bx, by, *KF_BOULDER, on='oW.', avoid_mask=ev_mask, post_paint=True)

    # Paint weathered timber causeway spans over the lake narrows (South x=14..17 y=29..31 & East x=29..35 y=21..24)!
    _paint_wharf(m, 14, 29, 17, 31)
    _paint_wharf(m, 29, 21, 35, 24)

    # Monumental Continuous Stone Curtain Wall + Battlement Parapets + Intact Royal Banners linking Towers & Keep Portal!
    for seg_x0, seg_x1 in ((5, 9), (22, 30)):
        for x in range(seg_x0, seg_x1 + 1):
            is_w, is_e = (x == seg_x0), (x == seg_x1)
            for yy in (4, 5, 6):
                m.L[0, yy, x] = SNOW_BASE
                m.L[2, yy, x] = 0
            m.L[1, 4, x] = P1('rw_rail_w' if is_w else ('rw_rail_e' if is_e else 'rw_rail_m'))
            m.L[1, 5, x] = P1('rw_f1w0' if is_w else ('rw_f1e0' if is_e else ('rw_f1m1' if (x + seg_x0) % 3 == 0 else 'rw_f1m0')))
            m.L[1, 6, x] = P1('rw_f2w0' if is_w else ('rw_f2e0' if is_e else 'rw_f2m0'))
    ban_L = STAMPS['fw_ban_i']['layers']
    for bx, by in ((6, 5), (8, 5), (24, 5), (27, 5), (29, 5)):
        m.L[2, by, bx] = int(ban_L[2][0][0] or ban_L[1][0][0])
        m.L[2, by + 1, bx] = int(ban_L[1][1][0] or ban_L[2][1][0])

    # Seal rear of North Keep Portal (y=5, x=13..18) & clear walkable arch L2 (13..18, 6..7)
    for gx in range(13, 19):
        m.L[1, 5, gx] = P1('rw_f1m0')
        m.L[2, 6, gx] = 0
        m.L[2, 7, gx] = 0

    # Scatter extra floating glacial ice-floes across frozen lake surround ('o') for authentic wind-broken lake texture
    floes = [P1('fw_floe0'), P1('fw_floe1')]
    for y in range(H):
        for x in range(W):
            if m.cls[y, x] == 'o' and int(m.L[1, y, x]) == 0 and not ev_mask[y, x] and rng.random() < 0.48:
                m.L[1, y, x] = rng.choice(floes)

    _dress_snow_details(m, ev_mask, seed=3055, drift_p=0.24, track_p=0.25, crack_p=0.30, reeds_p=0.0)

    open_305 = [(x, H - 1) for x in range(14, 18)] + [(W - 1, y) for y in range(21, 25)]
    _seal_unconnected_edges(m, open_cells=open_305)

    Lr = RC.resolve(m.L, TID_SNOW).astype(np.int32)
    ev_pts = [tuple(e['at']) for e in E]
    PG.guard(Lr, TID_SNOW, ev_pts, 'Map 305')
    assert not PG.hits(Lr, R.tilesets()[TID_SNOW], ev_pts), 'Map 305 passguard hits!'
    _verify_map(Lr, TID_SNOW, E, (16, 29), 'Map 305 Whalebone Keep - Bailey', outdoor=True)

    np.save(os.path.join(RAW_DIR, '305.npy'), Lr.astype(np.int16))
    spec = {
        'id': 305,
        'name': 'Whalebone Keep - Bailey',
        'parent': 300,
        'bgm': 'Lerucean Town',
        'field': 'FROZEN_LAKE',
        'rubric': True,
        'yards_ok': True,
        'map_audio': {'bgm': 'Town - Isenmar', 'bgs': 'Wind - Isenmar', 'bgs_volume': 65},
        'tone': [-12, -4, 16, 12],
        'fog': {'name': 'prismfall_seamist', 'opacity': 24, 'blend': 0, 'zoom': 100, 'sx': 1, 'sy': 0},
        'metadata': {
            'Name': 'Whalebone Keep - Bailey',
            'Outdoor': True,
            'ShowArea': True,
            'Bicycle': True,
            'MapPosition': RIME_POS,
            'BattleBack': 'snow',
            'Weather': ['Snow', 25],
        },
        'biome': 'city',
        'tileset': TID_SNOW,
        'raw': 'data/raw/305.npy',
        'events': E,
    }
    with open(os.path.join(SPEC_DIR, '305_whalebone_keep_bailey.yaml'), 'w', encoding='utf-8') as f:
        f.write('# GENERATED by mapgen/layouts/whalebone_keep.py (Batch 3H): Whalebone Keep - Bailey.\n')
        f.write(yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))
    print('Wrote specs/305_whalebone_keep_bailey.yaml and data/raw/305.npy')
    return Lr


# =================================================================================================
# 2. MAP 306 — WHALEBONE KEEP - MEAD HALL (31x21, TS 59 PF Rejuv Manor — Viking Timber Great Hall!)
# =================================================================================================
def build_306():
    W, H = 31, 21
    m = NordicKeep(W, H, seed=306, tid=TID_MANOR)
    Rb = m.room_box

    # ---- 1. Void-Sculpted Nordic Timber Banquet Hall with Elevated Royal Vestibule & Vault Stair ----
    # Elevated North Thane's Vestibule (TER, x=10..20, y=3..7 -> walls y=2..4, floor y=5..6, stairs y=7..9!)
    Rb(10, 3, 20, 7, TER, 'T', 'T')
    # Central Roaring Hearth-Fire Nave (FLOOR, x=10..20, y=8..18 -> open floor y=10..18!)
    Rb(10, 8, 20, 18, FLOOR, 'T', 'T')
    # West Banquet & Ice-Vault Stair Wing (FLOOR, x=3..10, y=8..17 -> walls y=7..9, floor y=10..17!)
    Rb(3, 8, 10, 17, FLOOR, 'T', 'N')
    # East Banquet & Great Tally Wing (FLOOR, x=20..27, y=8..17 -> walls y=7..9, floor y=10..17!)
    Rb(20, 8, 27, 17, FLOOR, 'T', 'N')
    # Narrowed Monumental Southern Entry Portal framing full 3-wide exit carpet warps (14..16, 19)
    m.box(12, 18, 18, 19, FLOOR)

    # Architectural corner chamfers into pure black void (ZERO boxy rectangle!)
    m.mass_at([
        (3, 8), (4, 8), (3, 16), (3, 17), (4, 17),
        (26, 8), (27, 8), (27, 16), (27, 17), (26, 17),
        (10, 3), (20, 3),
    ])

    # Grand 5-Wide Stone Staircase descending from North Thane's Vestibule (x=13..17, y=7..9 -> lands y=10!)
    m.stairs(13, 7, w=5, n=3, c='.')
    m.plan_cliffs(rows=3)

    # ---- 2. Rich Nordic Timber & Ash-Slate Flooring + Royal Blue Isenmar Carpets (ZERO sky windows!) ----
    m.hall_floor(10, 5, 20, 7, 'slate')
    m.hall_floor(11, 10, 19, 19, 'slate')
    m.hall_floor(3, 10, 10, 17, 'planks')
    m.hall_floor(20, 10, 27, 17, 'planks')

    # Sweeping Royal-Blue & Gold Isenmar Medallion Carpets along Central Aisle & Vestibule (full 3-wide at exit!)
    m.rug('B', 14, 5, 16, 6, medallion=False)
    m.rug('B', 14, 10, 16, 19, medallion=True)

    # ---- 3. Grand Timber Walls: Throne Double-Door, Hearths, Banners, Whale Skulls, Tables & Braziers ----
    # Carved Double-Door set into North Vestibule wall (15, 4) -> leaves (14..16, 5) walkable for warps to 307!
    m.late.append((1, 15, 4, P1('mn_door')))
    m.late.append((1, 14, 4, P1('mn_sconce')))
    m.late.append((1, 16, 4, P1('mn_sconce')))

    # ZERO exterior sky windows! Warm wall sconces, royal blue Isenmar banners & whale-skull trophies instead!
    for sx, sy in ((11, 4), (19, 4), (5, 9), (10, 9), (20, 9), (25, 9)):
        m.late.append((2, sx, sy, P1('mn_sconce')))
    for bx, by in ((13, 3), (17, 3), (9, 8), (21, 8)):
        m.on('fw_ban_i', bx, by)
    # Twin Hirdman Armour Suits & Candelabras framing the North Thane's Seat Portal
    m.on('mn_armour', 12, 4)
    m.on('mn_armour', 18, 4)
    m.on('mn_candelabra', 11, 5)
    m.on('mn_candelabra', 19, 5)

    # Twin Roaring Grand Viking Hearths warming the West & East Banquet Wings!
    m.on('mn_fire_lit', 6, 9)
    m.on('mn_fire_lit', 22, 9)

    # Flaming Central Hearth-Aisle Braziers (ZERO detached pf_glow — 100% crisp burning flames!)
    braziers_306 = [(12, 11), (18, 11), (12, 15), (18, 15), (13, 18), (17, 18)]
    for bx, by in braziers_306:
        m.on('fw_brazier', bx, by)

    # Monumental Carved Stone Columns framing the Hearth Nave (unobstructed above whale-skull trophies!)
    for cx, cy in ((11, 12), (19, 12), (11, 15), (19, 15)):
        m.on('nr_col', cx, cy)

    # Long Viking Timber Feasting Banquet Tables (West x=6..8, y=13..15 & East x=22..24, y=13..15)
    m.table(6, 13, 8, 15)
    for px, py in ((6, 13), (8, 13), (6, 15), (8, 15)):
        m.late.append((2, px, py, P1('mn_dt_plate')))
    m.late.append((2, 7, 14, P1('mn_dt_cand')))
    for cy in (13, 15):
        m.on('mn_chair_right', 5, cy)
        m.on('mn_chair_left', 9, cy)

    m.table(22, 13, 24, 15)
    for px, py in ((22, 13), (24, 13), (22, 15), (24, 15)):
        m.late.append((2, px, py, P1('mn_dt_plate')))
    m.late.append((2, 23, 14, P1('mn_dt_cand')))
    for cy in (13, 15):
        m.on('mn_chair_right', 21, cy)
        m.on('mn_chair_left', 25, cy)

    # Carved Debt-Tally Plinths, Snowless Great Tally Obelisk & Indoor Nordic Royal Standards + Hoard Chests (0 snow indoors!)
    m.on('mn_plinth', 10, 10)        # Debt-Tally Plaque West
    m.on('mn_plinth', 20, 10)        # Debt-Tally Plaque East
    m.on('pf_roadstone', 26, 10)     # Snowless Carved Great Tally Obelisk -> solid base at (26, 11)!
    m.on('wr_ban_ise', 10, 15)       # Standing Royal Isenmar Whale-and-Axe Standard West -> base (10, 17)
    m.on('mn_trunk', 11, 17)         # Iron-Banded Nordic Hoard Chest West
    m.on('mn_trunk', 19, 17)         # Iron-Banded Nordic Hoard Chest East
    m.on('wr_ban_ise', 20, 15)       # Standing Royal Isenmar Whale-and-Axe Standard East -> base (20, 17)
    m.on('mn_sideboard2', 23, 17)    # Mead Cask Sideboard

    # Cohesive Framed West Stone Vault Stair Descent (x=3, y=11..12 -> 308 Whalebone Keep - Ice Vault!)
    m.on('pf_signpost', 4, 9)        # Vault Stair Signpost -> solid base (4, 10)!
    m.late.append((2, 3, 9, P1('mn_sconce')))
    m.late.append((1, 3, 13, P1('mn_newel')))

    # Intact Hanging Chandeliers centered cleanly over the open Hearth Nave (zero collisions!)
    m.stamps.append(('mn_chandelier', 14, 12))
    m.stamps.append(('mn_chandelier', 14, 16))

    # ---- 4. Events: Full-Width Warps, Great Tally Keeper Halla (pf_trial_keeper/board), Lore & Pickup ----
    halla_ruby = (
        'pbMessage(_INTL("Old Halla Brinesdottir: Welcome beneath the whale-ribs, young Warden-hunter. I keep the Great Tally of Isenmar."))\n'
        'pbMessage(_INTL("Old Halla Brinesdottir: Every deed on the ice is notched into these timbers — and every Harpooner\'s rank earns its due from our hoard."))\n'
        'if defined?(pf_trial_keeper)\n'
        '  pf_trial_keeper(:ISENMAR)\n'
        'elsif defined?(pf_trial_board)\n'
        '  pf_trial_board(:ISENMAR)\n'
        'end'
    )
    tally_board_ruby = (
        'pbMessage(_INTL("THE GREAT TALLY OF ISENMAR — Notched rows of harpoon-marks, winter oaths, and harbour deeds."))\n'
        'if defined?(pf_trial_board)\n'
        '  if pbConfirmMessage(_INTL("Inspect the Great Tally board?"))\n'
        '    pf_trial_board(:ISENMAR)\n'
        '  end\n'
        'end'
    )

    E = [
        # Full 3-wide South Exit Carpet Warps (14..16, 19) -> 305 Whalebone Keep - Bailey (16, 8, down)
        {'type': 'warp', 'name': 'South to Bailey L', 'at': [14, 19], 'to': {'map': 305, 'x': 16, 'y': 8, 'dir': 'down'}, 'se': 'Door exit'},
        {'type': 'warp', 'name': 'South to Bailey C', 'at': [15, 19], 'to': {'map': 305, 'x': 16, 'y': 8, 'dir': 'down'}, 'se': 'Door exit'},
        {'type': 'warp', 'name': 'South to Bailey R', 'at': [16, 19], 'to': {'map': 305, 'x': 16, 'y': 8, 'dir': 'down'}, 'se': 'Door exit'},
        # Full 3-wide North Grand Arch Warps (14..16, 5) -> 307 Whalebone Keep - Thane's Seat (12, 20, up)
        {'type': 'warp', 'name': 'North to Thanes Seat L', 'at': [14, 5], 'to': {'map': 307, 'x': 12, 'y': 20, 'dir': 'up'}, 'se': 'Door enter'},
        {'type': 'warp', 'name': 'North to Thanes Seat C', 'at': [15, 5], 'to': {'map': 307, 'x': 12, 'y': 20, 'dir': 'up'}, 'se': 'Door enter'},
        {'type': 'warp', 'name': 'North to Thanes Seat R', 'at': [16, 5], 'to': {'map': 307, 'x': 12, 'y': 20, 'dir': 'up'}, 'se': 'Door enter'},
        # Full 2-wide West Stone Vault Stair Descent (3, 11..12) -> 308 Whalebone Keep - Ice Vault (16, 5, down)
        {'type': 'warp', 'name': 'West to Ice Vault N', 'at': [3, 11], 'to': {'map': 308, 'x': 16, 'y': 5, 'dir': 'down'}, 'se': 'Door enter'},
        {'type': 'warp', 'name': 'West to Ice Vault S', 'at': [3, 12], 'to': {'map': 308, 'x': 16, 'y': 5, 'dir': 'down'}, 'se': 'Door enter'},

        # Canonical Old Halla Brinesdottir — Keeper of the Great Tally (:ISENMAR rewards: Glalitite & Lapras!)
        {'type': 'event', 'name': 'Old Halla Brinesdottir', 'at': [25, 11],
         'pages': [{'graphic': {'sprite': 'NPC 11', 'dir': 'left'}, 'trigger': 'action', 'move': 'fixed',
                    'commands': [{'script': halla_ruby}]}]},
        # Great Tally Wall Stone (solid base (26, 11) -> 0 over_trigger?!)
        {'type': 'event', 'name': 'Great Tally Board', 'at': [26, 11],
         'pages': [{'trigger': 'action', 'commands': [{'script': tally_board_ruby}]}]},

        # Canonical Mead Hall NPCs
        _make_npc('Mead-Hall Steward', (17, 6), 'NPC 12', 'down', [
            "Steward: Thane Eirik holds court straight beyond the north doors. Eat something warm before you go in — everyone wants a thing from him and nobody eats.",
            "Steward: These walls carry three centuries of Isenmar's debt-tallies. Half the new notches are Meridian heat ledgers.",
        ]),
        _make_npc('Vault Stair Hirdman', (5, 11), 'trainer_ISENMAR_HIRDMAN', 'right', [
            "Vault Hirdman: Those western steps drop straight down into the Ice Vault beneath the lake ice.",
            "Vault Hirdman: Keep your footing down there — old skalds swear the ice carries the sound of something huge breathing below the cistern.",
        ]),
        _make_npc('Feasting Skald', (9, 14), 'NPC 22', 'left', [
            "Feasting Skald: Whale-rib rafters overhead, roaring hearth fires at each end, and spiced cider in the barrel — that's an Isenmar winter done right.",
        ]),
        _make_npc('Harbour Captain', (21, 14), 'NPC 20', 'right', [
            "Harbour Captain: Ashkaar shut the southern passes and cut the forge-heat pipes from Cindervault. Now the city's towers draw straight from the lake.",
        ]),

        # Solid Wall Plaques & Vault Sign (0 over_trigger?!)
        _sign('Vault Descent Sign', (4, 10),
              "WEST VAULT STAIR — ↓ WHALEBONE KEEP ICE VAULT. Ancient glacial crypts beneath Lake Rime."),
        _sign('Debt-Tally Wall West', (10, 10),
              "DEBT-TALLY LEDGER I — Carved notches mark winter grain loans, sled-wright shares, and ten winters of Meridian Heat Services invoices."),
        _sign('Debt-Tally Wall East', (20, 10),
              "DEBT-TALLY LEDGER II — 'AF 290: Four hundred lost to the Long Freeze. AF 292–300: Zero lost to cold. Signed, Eirik Sorrel, Thane of Isenmar.'"),

        # Visible East Trophy Alcove Pickup (explicit hidden=False!)
        {'type': 'item', 'name': 'Item (Exp. Candy L)', 'at': [26, 15], 'item': 'EXPCANDYL', 'hidden': False},
    ]
    m.events = E
    m.paint()

    # Cohesive West Vault Stair Descent (3, 11..12): left-curbed st_stair_l over vault slate with ZERO split T_shadow seam!
    for sy, sf in ((11, 'T_f0'), (12, 'T_f1')):
        m.L[0, sy, 3] = P1(sf)
        m.L[1, sy, 3] = P1('st_stair_l')
        m.L[2, sy, 3] = 0

    Lr = RC.resolve(m.L, TID_MANOR).astype(np.int32)
    _assert_braziers_intact(Lr, TID_MANOR, braziers_306, 'Map 306')
    ev_pts = [tuple(e['at']) for e in E]
    PG.guard(Lr, TID_MANOR, ev_pts, 'Map 306')
    assert not PG.hits(Lr, R.tilesets()[TID_MANOR], ev_pts), 'Map 306 passguard hits!'
    _verify_map(Lr, TID_MANOR, E, (15, 18), 'Map 306 Whalebone Keep - Mead Hall', outdoor=False)

    np.save(os.path.join(RAW_DIR, '306.npy'), Lr.astype(np.int16))
    spec = {
        'id': 306,
        'name': 'Whalebone Keep - Mead Hall',
        'parent': 305,
        'bgm': 'Lerucean Town',
        'map_audio': {'bgm': 'Theme - Accord', 'bgs': ''},
        'tone': [10, 2, -10, 6],
        'metadata': {'Name': 'Whalebone Keep - Mead Hall', 'Outdoor': False, 'ShowArea': True, 'MapPosition': RIME_POS},
        'biome': 'interior',
        'tileset': TID_MANOR,
        'raw': 'data/raw/306.npy',
        'events': E,
    }
    with open(os.path.join(SPEC_DIR, '306_whalebone_keep_mead_hall.yaml'), 'w', encoding='utf-8') as f:
        f.write('# GENERATED by mapgen/layouts/whalebone_keep.py (Batch 3H): Whalebone Keep - Mead Hall.\n')
        f.write(yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))
    print('Wrote specs/306_whalebone_keep_mead_hall.yaml and data/raw/306.npy')
    return Lr


# =================================================================================================
# 3. MAP 307 — WHALEBONE KEEP - THANE'S SEAT (25x23, TS 59 PF Rejuv Manor — Thane Eirik's Court!)
# =================================================================================================
def build_307():
    W, H = 25, 23
    m = NordicKeep(W, H, seed=307, tid=TID_MANOR)
    Rb = m.room_box

    # ---- 1. Void-Sculpted Octagonal Royal Audience Chamber of Thane Eirik Sorrel ----
    # Elevated Northern Whale-Skull Throne Dais (TER, x=7..17, y=3..9 -> walls y=2..4, dais floor y=5..8!)
    Rb(7, 3, 17, 9, TER, 'T', 'T')
    # Central Processional Audience Court (FLOOR, x=6..18, y=10..20 -> stairs y=9..11, court floor y=12..20!)
    Rb(6, 10, 18, 20, FLOOR, 'T', 'T')
    # Recessed West & East Royal Tapestry / Banner Galleries (FLOOR, x=3..6 & x=18..21, y=11..18)
    Rb(3, 11, 6, 18, FLOOR, 'T', 'N')
    Rb(18, 11, 21, 18, FLOOR, 'T', 'N')
    # Narrowed Monumental Southern Portal framing full 3-wide exit carpet warps (11..13, 21)
    m.box(9, 20, 15, 21, FLOOR)

    # Octagonal architectural chamfers into pure black void (ZERO flat box!)
    m.mass_at([
        (7, 3), (17, 3),
        (3, 11), (3, 17), (3, 18), (4, 18),
        (21, 11), (21, 17), (21, 18), (20, 18),
        (6, 19), (6, 20), (18, 19), (18, 20),
    ])

    # Grand 5-Wide Stone Staircase descending from Thane Eirik's Dais (x=10..14, y=9..11 -> lands y=12!)
    m.stairs(10, 9, w=5, n=3, c='.')
    m.plan_cliffs(rows=3)

    # ---- 2. Material Contrast: Ash-Slate Throne Dais & Nave + Dark Timber Galleries + Royal-Blue Carpet ----
    m.hall_floor(7, 5, 17, 8, 'slate')
    m.hall_floor(8, 12, 16, 21, 'slate')
    m.hall_floor(3, 13, 7, 17, 'planks')
    m.hall_floor(17, 13, 21, 17, 'planks')

    # Sweeping Royal-Blue & Gold Isenmar Medallion Carpets (full 3-wide at South Exit (11..13, 21)!)
    m.rug('B', 10, 5, 14, 8, medallion=True)
    m.rug('B', 11, 12, 13, 21, medallion=True)

    # ---- 3. Monumental Nordic Thane's High Seat Masterpiece (ZERO snow indoors, ZERO carpet clipping!) ----
    # Royal Blue & Gold Sovereign Tapestry centered behind the throne + flanking Isenmar wall banners & sconces
    m.on('lm_banner', 12, 3)         # Sovereign blue-and-gold crest tapestry directly behind the High Seat (12, 3..4)
    for bx, by in ((10, 3), (14, 3), (5, 11), (19, 11)):
        m.on('fw_ban_i', bx, by)
    for sx, sy in ((8, 4), (16, 4), (4, 12), (20, 12)):
        m.late.append((2, sx, sy, P1('mn_sconce')))

    # Dais Slate Wings (completely OFF the royal-blue carpet x=10..14 so all 4 gold corners stay 100% pristine!)
    m.on('lm_pillar', 9, 3)          # Towering 3-tall ivory-and-gold fluted royal column West -> base (9, 5)
    m.on('lm_pillar', 15, 3)         # Towering 3-tall ivory-and-gold fluted royal column East -> base (15, 5)
    m.on('mn_candelabra', 8, 5)      # Golden 3-Branch Candelabra West -> base (8, 6), clear of pillar & brazier!
    m.on('mn_candelabra', 16, 5)     # Golden 3-Branch Candelabra East -> base (16, 6), clear of pillar & brazier!
    m.on('mn_statue', 7, 5)          # Marble Ancestral Thane Statue West -> base (7, 6)
    m.on('mn_statue', 17, 5)         # Marble Ancestral Thane Statue East -> base (17, 6)

    # Monumental 3-Wide Thane's High Seat Ensemble on the Royal Dais Carpet (11..13, 4..6):
    # Twin standing Whale-and-Axe Royal Standards flanking the crimson High Seat beneath the Sovereign Tapestry!
    m.on('wr_ban_ise', 11, 4)        # Royal Whale-and-Axe Standard Left -> base (11, 6)
    m.on('wr_ban_ise', 13, 4)        # Royal Whale-and-Axe Standard Right -> base (13, 6)
    m.on('mn_chairR_down', 12, 6)    # Crimson Velvet High Seat centered on the gold medallion (12, 6)!

    braziers_307 = [(8, 7), (16, 7), (8, 13), (16, 13), (10, 19), (14, 19)]
    for bx, by in braziers_307:
        m.on('fw_brazier', bx, by)

    # Symmetrical Carved Stone Colonnade & Gallery Armour / Historical Tapestry Plinths (0 over_trigger?!)
    for cx, cy in ((9, 14), (15, 14), (9, 17), (15, 17)):
        m.on('nr_col', cx, cy)
    for ax, ay in ((4, 13), (20, 13), (6, 17), (18, 17)):
        m.on('mn_armour', ax, ay)
    m.on('mn_plinth', 6, 14)         # Historical Plaque: Founding of Rimeholt
    m.on('mn_plinth', 18, 14)        # Historical Plaque: Isenmar Festival Delegation
    m.on('mn_bench', 4, 16)
    m.on('mn_bench', 19, 16)

    # Single Unobstructed Hanging Chandelier over the Central Audience Court (dais 100% clear!)
    m.stamps.append(('mn_chandelier', 11, 15))

    # ---- 4. Events: Full 3-Wide Exit, Thane Eirik Sorrel (EIRIK), Housecarls, Meridian Envoy & Plaques ----
    eirik_ruby = (
        'if $game_variables[122] >= 2\n'
        '  pbMessage(_INTL("Thane Eirik: Ashkaar starved Rimeholt, and the lake ate what was left. My host marches east along the Sled-Road."))\n'
        '  pbMessage(_INTL("Thane Eirik: Walk safe, young challenger. When the Prism Festival convenes, Isenmar\'s delegation will speak from this very floor."))\n'
        'elsif $game_switches[128]\n'
        '  pbMessage(_INTL("Thane Eirik: Two hundred and six of my people are not in their beds this morning. Martial law stands across Rimeholt until every family is south over Frostfang."))\n'
        'else\n'
        '  pbMessage(_INTL("Thane Eirik: Warden Hale\'s friend. Stand by the fire a moment — everyone who comes in here wants a thing and nobody warms their hands."))\n'
        '  pbMessage(_INTL("Thane Eirik: Ten years ago a winter killed four hundred people in this city. Old people. Babies. I buried them on the ice because the ground was too hard to dig."))\n'
        '  pbMessage(_INTL("Thane Eirik: Then Meridian came with the towers, and nobody has died of cold in Rimeholt in eight years. Now Ashkaar has closed the passes, so my towers run on the lake."))\n'
        '  pbMessage(_INTL("Thane Eirik: My sister says the lake can take it. So the lake can take it."))\n'
        'end'
    )

    E = [
        # Full 3-wide South Exit Carpet Warps (11..13, 21) -> 306 Whalebone Keep - Mead Hall (15, 6, down)
        {'type': 'warp', 'name': 'South to Mead Hall L', 'at': [11, 21], 'to': {'map': 306, 'x': 15, 'y': 6, 'dir': 'down'}, 'se': 'Door exit'},
        {'type': 'warp', 'name': 'South to Mead Hall C', 'at': [12, 21], 'to': {'map': 306, 'x': 15, 'y': 6, 'dir': 'down'}, 'se': 'Door exit'},
        {'type': 'warp', 'name': 'South to Mead Hall R', 'at': [13, 21], 'to': {'map': 306, 'x': 15, 'y': 6, 'dir': 'down'}, 'se': 'Door exit'},

        # Canonical Ruler of Isenmar: Thane Eirik Sorrel (graphics/Characters/EIRIK.png!)
        {'type': 'event', 'name': 'Thane Eirik Sorrel', 'at': [12, 8],
         'pages': [{'graphic': {'sprite': 'EIRIK', 'dir': 'down'}, 'trigger': 'action', 'move': 'fixed',
                    'commands': [{'script': eirik_ruby}]}]},

        _make_npc('Housecarl Commander', (9, 12), 'trainer_ISENMAR_OFFICER', 'right', [
            "Housecarl Commander: Stand respectfully before the Whale-Skull Throne. Thane Eirik has been signing heat manifests since midnight.",
        ]),
        _make_npc('Royal Hirdman', (15, 12), 'trainer_ISENMAR_HIRDMAN', 'left', [
            "Royal Hirdman: Lady Anja is the Thane's own sister, yet even she refuses to step onto the dais with wet boots.",
        ]),
        _make_npc('Court Lawspeaker', (7, 16), 'NPC 25', 'right', [
            "Lawspeaker: From this stone aisle Isenmar names its champions for the Prism Festival of AF 300.",
            "Lawspeaker: Pray the sea stays frozen long enough for our delegation to sail south.",
        ]),
        _make_npc('Meridian Envoy', (17, 16), 'trainer_MERIDIAN_DIRECTORATE', 'left', [
            "Meridian Envoy: Meridian Heat Services operates strictly within the tolerances co-signed by Isenmar's Warden.",
            "Meridian Envoy: Any rumour of excess lake-draw is pure dockside superstition.",
        ]),

        # Solid Throne & Historical Plaques (ALL on pas=0xf tiles -> 0 over_trigger?!)
        _sign('The Whale-Skull Throne', (12, 6),
              "THE WHALE-SKULL THRONE OF ISENMAR — Carved from a single ancient leviathan skull hauled from Lake Rime three centuries ago."),
        _sign('Tapestry of the First Thane', (6, 14),
              "CHRONICLE OF THE FIRST THANE — 'Here we bound the harbour to the rock, and swore the Icicle Plate would keep the north alive.'"),
        _sign('Festival Delegation Charter', (18, 14),
              "ROYAL COURT OF ISENMAR — 'From the Thane's Seat the northern champions depart beneath the Whale and Axe for the Prism Festival.'"),

        # Visible West Court Reliquary Pickup (explicit hidden=False!)
        {'type': 'item', 'name': 'Item (Full Restore)', 'at': [5, 14], 'item': 'FULLRESTORE', 'hidden': False},
    ]
    m.events = E
    m.paint()

    Lr = RC.resolve(m.L, TID_MANOR).astype(np.int32)
    _assert_braziers_intact(Lr, TID_MANOR, braziers_307, 'Map 307')
    ev_pts = [tuple(e['at']) for e in E]
    PG.guard(Lr, TID_MANOR, ev_pts, 'Map 307')
    assert not PG.hits(Lr, R.tilesets()[TID_MANOR], ev_pts), 'Map 307 passguard hits!'
    _verify_map(Lr, TID_MANOR, E, (12, 20), "Map 307 Whalebone Keep - Thane's Seat", outdoor=False)

    np.save(os.path.join(RAW_DIR, '307.npy'), Lr.astype(np.int16))
    spec = {
        'id': 307,
        'name': "Whalebone Keep - Thane's Seat",
        'parent': 306,
        'bgm': 'Lerucean Town',
        'map_audio': {'bgm': 'Theme - Accord', 'bgs': ''},
        'tone': [8, 2, -6, 8],
        'metadata': {'Name': "Whalebone Keep - Thane's Seat", 'Outdoor': False, 'ShowArea': True, 'MapPosition': RIME_POS},
        'biome': 'interior',
        'tileset': TID_MANOR,
        'raw': 'data/raw/307.npy',
        'events': E,
    }
    with open(os.path.join(SPEC_DIR, '307_whalebone_keep_thanes_seat.yaml'), 'w', encoding='utf-8') as f:
        f.write("# GENERATED by mapgen/layouts/whalebone_keep.py (Batch 3H): Whalebone Keep - Thane's Seat.\n")
        f.write(yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))
    print("Wrote specs/307_whalebone_keep_thanes_seat.yaml and data/raw/307.npy")
    return Lr


# =================================================================================================
# 4. MAP 308 — WHALEBONE KEEP - ICE VAULT (33x33, TS 57 PF Rejuv Cave — Subterranean Glacial Vault!)
# =================================================================================================
def build_308():
    W, H = 33, 33
    # Glacial wet blue-grey slate bedrock walls (cvL) + PF Cave Pool subterranean breathing lake cistern!
    K.KITS['cvL2'] = dict(K.KITS['cvL'], rows=[K.KITS['cvL']['rows'][0], K.KITS['cvL']['rows'][2]])
    m = Cave(W, H, 'L', seed=308, pool='Cave Pool', tid=TID_CAVE)
    m.STAIRS = tuple(P1('st_stair_' + k) for k in 'lmr')
    m.kit = {MASS: 'cvL2', TER: 'cvL2', FLOOR: 'cvL2', 'default': 'cvL2'}

    # ---- 1. Sculpt Multi-Chamber Glacial Crypt & Whalesong Resonance Vault ----
    # Exact 3-wide Recessed North Ascending Stair Alcove (x=15..17, y=2..5 -> walls y=2..3, stair fills (15..17, 4)!)
    m.box(15, 2, 17, 5, TER, '.')
    # Elevated North Vault Landing (TER, x=12..20, y=4..8 -> floor y=5..7, stairs y=8..9!)
    m.box(12, 4, 20, 8, TER, '.')
    # Central Whalesong Cistern Hall (FLOOR, x=9..23, y=9..23)
    m.box(9, 9, 23, 23, FLOOR, '.')
    # West Rock-Smash Choke (7, 16) -> Sealed West Glacial Reliquary (x=3..6, y=12..19 -> floor y=14..19, NEVERMELTICE!)
    m.box(6, 15, 9, 17, FLOOR, '.')
    m.box(3, 12, 6, 19, FLOOR, '.')
    # East Strength-Boulder Choke (25, 16) -> Sealed East Glacial Reliquary (x=26..29, y=12..19 -> floor y=14..19, ICYROCK!)
    m.box(23, 15, 26, 17, FLOOR, '.')
    m.box(26, 12, 29, 19, FLOOR, '.')
    # South Sleeping-Whale Seal Sanctum (FLOOR, x=11..21, y=23..29) + Recessed Depths Arch (x=15..17, y=29..30)!
    m.box(11, 23, 21, 29, FLOOR, '.')
    m.box(15, 29, 17, 30, FLOOR, '.')

    # Sculpt exact 1-tile gated chokes at (7, 16) [Rock Smash] & (25, 16) [Strength] + architectural chamfers!
    # cvL2 paints a 2-row south-facing wall onto y=14..15 below y=14 MASS, so placing MASS at y=17 leaves ONLY y=16 open!
    m.mass_at([
        (7, 17), (8, 17),         # Exact 1-tile West Rock-Smash choke at (7, 16)!
        (24, 17), (25, 17),       # Exact 1-tile East Strength-Boulder choke at (25, 16)!
        (3, 12), (3, 19), (29, 12), (29, 19),
        (9, 9), (23, 9), (9, 23), (23, 23),
        (11, 29), (21, 29),
    ])

    # Central Sunken Subterranean Lake Rime Cistern ("the dark that breathes" — x=14..18, y=15..18!)
    m.box(14, 15, 18, 18, FLOOR, 'w')

    # Grand 3-Wide Carved Stone Staircase descending from North Vault Landing (x=15..17, y=8..9)
    m.stairs(15, 8, w=3, n=2, c='.')
    m.tidy()
    m.plan_cliffs(rows=2)

    # ---- 2. Events: North Stair -> 306, Guarded South Depths -> 318, Rock Smash & Strength Gates, Monoliths, Relics ----
    E = m.events
    # Full 3-wide North Ascending Return Stair (15..17, 4) -> 306 Mead Hall (4, 11, right)
    for rx in (15, 16, 17):
        E.append({'type': 'warp', 'name': f'Up to Mead Hall {rx}', 'at': [rx, 4],
                  'to': {'map': 306, 'x': 4, 'y': 11, 'dir': 'right'}, 'se': 'Door exit'})

    # Full 3-wide South Sleeping-Whale Depths Arch (15..17, 30) -> PBMoveRoute::BACKWARD-guarded 318 Ice Vault Depths!
    depths_msg = (
        "(An ancient door of blue glacier-ice blocks the descent into the Vault Depths. Four carved whale-song channels "
        "run dry across its threshold — only when the lake thaws will the song carry down into the dark below.)"
    )
    for dx in (15, 16, 17):
        E.append({'type': 'event', 'name': f'South to Ice Vault Depths {dx}', 'at': [dx, 30],
                  'pages': [{'trigger': 'touch', 'through': True,
                             'commands': _guarded_unbuilt_transfer(318, 16, 4, 'down', depths_msg)}]})

    # Vault Lorekeeper near North Landing explaining the Whalesong Channels & Breathing Cistern
    E.append(_make_npc('Vault Lorekeeper', (14, 7), 'NPC 21', 'right', [
        "Vault Lorekeeper: Listen beside the dark cistern in the middle of the vault. Not wind — breath. Slow as a tide.",
        "Vault Lorekeeper: The four monoliths around the water carry the Sleeping Whale's verses. Ice carries sound along cut channels, and meltwater carries it farther still.",
    ]))

    # West Rock-Smash Gate at exact 1-tile choke (7, 16) -> seals West Reliquary NEVERMELTICE!
    E.append({'type': 'rock_smash', 'name': 'Cracked Glacial Slate', 'at': [7, 16], 'sprite': 'pf_cave_rock_L'})

    # East Native Essentials v21.1 StrengthBoulder Gate at exact 1-tile choke (25, 16) -> seals East Reliquary ICYROCK!
    # Naming 'StrengthBoulder' hooks Essentials :on_player_interact :strength_event cleanly (0 duplicate messages),
    # and trigger: 'touch' + pbPushThisBoulder calls pbPushThisEvent(true) with authentic "Strength push" SE!
    E.append({
        'type': 'event',
        'name': 'StrengthBoulder',
        'at': [25, 16],
        'pages': [{
            'graphic': {'sprite': 'pf_cave_boulder_L', 'dir': 'down'},
            'trigger': 'touch',
            'dir_fix': True,
            'commands': [{'script': 'pbPushThisBoulder'}],
        }],
    })

    # Four Carved Nordic Whalesong Monoliths framing the Cistern + Twin Sealed Depths Obelisks (ALL on solid bases -> 0 over_trigger?!)
    E.append(_sign('Whalesong Monolith I (Low)', (12, 13),
                   "SONG PILLAR I — WAVY CARVING (LOW NOTE): 'Sleep, old whale, under the white.'"))
    E.append(_sign('Whalesong Monolith II (Mid)', (20, 13),
                   "SONG PILLAR II — DOUBLE CARVING (MID NOTE): 'Sleep while the Thane keeps the lamps alight.'"))
    E.append(_sign('Whalesong Monolith III (High)', (12, 20),
                   "SONG PILLAR III — DOTTED CARVING (HIGH NOTE): 'Wake when the ice remembers your name.'"))
    E.append(_sign('Whalesong Monolith IV (Whale)', (20, 20),
                   "SONG PILLAR IV — PLAIN WHALE SEAL: 'Wake, and the sea will be yours again.'"))
    E.append(_sign('Sealed Depths Inscription', (14, 28),
                   "VAULT DEPTHS SEAL — 'Beneath Lake Rime sleeps the Sea that answered no Thane. Strike the four pitches only in dire need.'"))
    E.append(_sign('Sealed Depths Inscription II', (18, 28),
                   "CHISELLED WARNING — 'Hear the four channels: Low, Mid, High, and the Whale's Own Name. When Lake Rime opens, the Vault Depths answer.'"))

    # Authentic Relic Pickups (explicit hidden=False on every visible item -> Object ball!)
    E.append({'type': 'item', 'name': 'Item (Never-Melt Ice)', 'at': [4, 16], 'item': 'NEVERMELTICE', 'hidden': False})
    E.append({'type': 'item', 'name': 'Item (Icy Rock)', 'at': [28, 16], 'item': 'ICYROCK', 'hidden': False})
    E.append({'type': 'item', 'name': 'Item (Ice Gem)', 'at': [21, 11], 'item': 'ICEGEM', 'hidden': False})
    E.append({'type': 'item', 'name': 'HiddenItem (Star Piece)', 'at': [16, 20], 'item': 'STARPIECE', 'hidden': True})

    # Protect key corridors, cistern perimeter, stairs, chokes & push runway
    for x in (15, 16, 17):
        for y in range(4, 15):
            m.keep_clear.add((x, y))
        for y in range(19, 31):
            m.keep_clear.add((x, y))
    for x in range(4, 14):
        m.keep_clear.add((x, 16))
    for x in range(19, 29):
        m.keep_clear.add((x, 16))
    for e in E:
        m.keep_clear.add(tuple(e['at']))

    # ---- 3. Crystalline Ice Pillars, Carved Monoliths, Columns & 100% Intact Burning Braziers ----
    def put_over(nm, x, y, top_rows=0, solid=True):
        Ls = STAMPS[nm]['layers']
        h, w = len(Ls[0]), len(Ls[0][0])
        for dy in range(h):
            for dx in range(w):
                if not m.inb(x + dx, y + dy):
                    continue
                for sz in (0, 1, 2):
                    t = int(Ls[sz][dy][dx])
                    if t:
                        tz = 2 if (dy < top_rows or sz == 2) else 1
                        m.over.append((tz, x + dx, y + dy, t))
                if solid:
                    m.taken[y + dy, x + dx] = True

    # Four Whalesong Monoliths (pf_roadstone 1x2 -> solid bases at (12,13), (20,13), (12,20), (20,20)!)
    for mx, my in ((12, 12), (20, 12), (12, 19), (20, 19)):
        put_over('pf_roadstone', mx, my, top_rows=1, solid=True)
    # Twin Sealed Depths Rune Monoliths (fw_stone 1x2 -> solid bases at (14, 28) & (18, 28)!)
    put_over('fw_stone', 14, 27, top_rows=1, solid=True)
    put_over('fw_stone', 18, 27, top_rows=1, solid=True)

    # Towering Faceted Ice Crystal Pillars (cv_xblue2 & cv_xsea2) framing the Cistern, Reliquaries & Sanctum!
    for cx, cy, nm in (
        (10, 11, 'cv_xblue2'), (22, 11, 'cv_xblue2'),
        (10, 19, 'cv_xsea2'), (22, 19, 'cv_xsea2'),
        (12, 24, 'cv_xblue2'), (20, 24, 'cv_xblue2'),
        (4, 14, 'cv_xblue2'), (4, 18, 'cv_xsea2'),
        (28, 14, 'cv_xblue2'), (28, 18, 'cv_xsea2'),
        (12, 6, 'cv_xblue'), (20, 6, 'cv_xblue'),
        (11, 14, 'cv_xblue'), (21, 14, 'cv_xblue'),
        (11, 18, 'cv_xsea'), (21, 18, 'cv_xsea'),
    ):
        put_over(nm, cx, cy, top_rows=1 if nm.endswith('2') else 0, solid=True)

    # Ancient Nordic Carved Stone Columns framing the Cistern Nave & Sanctum
    for cx, cy in ((13, 11), (19, 11), (13, 21), (19, 21), (13, 25), (19, 25)):
        put_over('nr_col', cx, cy, top_rows=1, solid=True)

    # 100% Intact Burning Iron Braziers (ZERO detached pf_glow, all iron bases cleanly on floor!)
    braziers_308 = [
        (13, 6), (19, 6),
        (13, 14), (19, 14), (13, 18), (19, 18),
        (5, 14), (5, 18), (27, 14), (27, 18),
        (13, 27), (19, 27),
    ]
    for bx, by in braziers_308:
        put_over('fw_brazier', bx, by, top_rows=1, solid=True)

    m.paint()

    # Cohesive Subterranean Ice-Vault Floor Hierarchy (ZERO slippery tag==12 :Ice tiles!):
    # - Wet blue-grey glacial slate (L_f0..3) in side cloisters
    # - Inlaid pale glacier-blue 3x3 mosaic resonance channels (GLACIER_9: 12476..12494, tag==0, pas==0!)
    # - Blue-grey ashlar flagstones (T_f0..3) on North Landing & South Seal Sanctum
    slate = [P1('L_f%d' % i) for i in range(4)]
    ashlar = [P1('T_f%d' % i) for i in range(4)]
    floorpatch_ids = {P1(k) for k in STAMPS if k.startswith(('L_floorpatch_', 'L_fd', 'T_floorpatch_', 'T_fd'))}
    ev_cells = {tuple(e['at']) for e in E}

    def _in_ice_chan(xx, yy):
        return (
            (15 <= xx <= 17 and (10 <= yy <= 14 or 19 <= yy <= 25))
            or (yy == 16 and (8 <= xx <= 13 or 19 <= xx <= 24))
            or (13 <= xx <= 19 and 14 <= yy <= 19)
        )

    rng_308 = random.Random(3087)
    for y in range(H):
        for x in range(W):
            if m.cls[y, x] != '.' or m.cliff[y, x]:
                continue
            if int(m.L[1, y, x]) in floorpatch_ids:
                m.L[1, y, x] = 0
            if _in_ice_chan(x, y):
                if y == 16 and (8 <= x <= 12 or 20 <= x <= 24):
                    m.L[0, y, x] = GLACIER_CENTER
                else:
                    ry = 0 if not _in_ice_chan(x, y - 1) else (2 if not _in_ice_chan(x, y + 1) else 1)
                    rx = 0 if not _in_ice_chan(x - 1, y) else (2 if not _in_ice_chan(x + 1, y) else 1)
                    m.L[0, y, x] = GLACIER_9[ry][rx]
                # Subtle safe tag==0 frost-crack & crystal sheen decals along dry channel margins (keep events spotless!)
                if int(m.L[1, y, x]) == 0 and not m.taken[y, x] and (x, y) not in ev_cells:
                    r = rng_308.random()
                    if r < 0.14:
                        m.L[1, y, x] = rng_308.choice(SAFE_CRACKS)
                    elif r < 0.24:
                        m.L[1, y, x] = rng_308.choice(SAFE_FROST)
            elif y <= 8 or y >= 26:
                m.L[0, y, x] = ashlar[(x * 3 + y * 5) % 4]
            else:
                m.L[0, y, x] = slate[(x * 7 + y * 11) % 4]

    # Crisp 3-wide stone steps filling 100% of North Return Alcove (15..17, 4)
    m.L[1, 4, 15] = P1('st_stair_l')
    m.L[1, 4, 16] = P1('st_stair_m')
    m.L[1, 4, 17] = P1('st_stair_r')

    # Sealed Glacier-Ice South Depths Arch (15..17, 30): pale glacier mosaic threshold + flanking blue crystal pillars!
    m.L[0, 30, 15] = GLACIER_9[2][0]
    m.L[0, 30, 16] = GLACIER_9[2][1]
    m.L[0, 30, 17] = GLACIER_9[2][2]
    m.L[1, 30, 15] = SAFE_CRACKS[0]
    m.L[1, 30, 16] = SAFE_FROST[1]
    m.L[1, 30, 17] = SAFE_CRACKS[1]
    # Towering blue glacier crystal pillars flanking the South Depths Arch on wall shoulders (14, 30) & (18, 30)
    xb2 = STAMPS['cv_xblue2']['layers']
    for sx in (14, 18):
        m.L[2, 29, sx] = int(xb2[2][0][0] or xb2[1][0][0])
        m.L[1, 30, sx] = int(xb2[1][1][0] or xb2[2][1][0])
    # Glacier-ice crystal seal rim capping the solid wall directly beneath the threshold (15..17, 31)
    for sx in (15, 16, 17):
        m.L[1, 31, sx] = P1('cv_xblue')

    # Bioluminescent cyan frost-fungi decals tucked along vault floor margins (pas=0x0 walkable)
    for fx, fy in ((14, 12), (18, 12), (14, 21), (18, 21), (10, 15), (22, 15), (12, 26), (20, 26)):
        if m.cls[fy, fx] == '.' and int(m.L[1, fy, fx]) == 0 and not m.taken[fy, fx]:
            m.L[1, fy, fx] = P1('cv_fung0')

    Lr = RC.resolve(m.L, TID_CAVE).astype(np.int32)
    _assert_braziers_intact(Lr, TID_CAVE, braziers_308, 'Map 308')

    ev_pts = [tuple(e['at']) for e in E]
    PG.guard(Lr, TID_CAVE, ev_pts, 'Map 308')
    assert not PG.hits(Lr, R.tilesets()[TID_CAVE], ev_pts), 'Map 308 passguard hits!'

    # Verify ALL main-hall events reachable BEFORE breaking gates, and verify gates seal (4,16) & (28,16)!
    main_targets = [
        ('North Stair L', (15, 4), False), ('North Stair C', (16, 4), False), ('North Stair R', (17, 4), False),
        ('South Depths Arch', (16, 30), False), ('Vault Lorekeeper', (14, 7), True),
        ('West Rock-Smash Choke', (7, 16), True), ('East Strength Choke', (25, 16), True),
        ('Monolith I', (12, 13), True), ('Monolith II', (20, 13), True),
        ('Monolith III', (12, 20), True), ('Monolith IV', (20, 20), True),
        ('Sealed Depths Inscription', (14, 28), True), ('Sealed Depths Inscription II', (18, 28), True),
        ('Ice Gem', (21, 11), True), ('Hidden Star Piece', (16, 20), True),
    ]
    seen_gated = _verify_map(Lr, TID_CAVE, E, (16, 5), 'Map 308 Whalebone Keep - Ice Vault (gated)',
                             outdoor=False, targets=main_targets)
    assert (4, 16) not in seen_gated, 'Map 308: West Rock-Smash chamber LEAKED around gate!'
    assert (28, 16) not in seen_gated, 'Map 308: East Strength chamber LEAKED around gate!'

    # Also verify BOTH side chambers & relics are 100% reachable ONCE the 2 gates are cleared!
    E_open = [e for e in E if e.get('name') not in ('Cracked Glacial Slate', 'StrengthBoulder')]
    _verify_map(Lr, TID_CAVE, E_open, (16, 5), 'Map 308 Whalebone Keep - Ice Vault (unlocked)',
                outdoor=False, targets=[('Never-Melt Ice', (4, 16), True), ('Icy Rock', (28, 16), True)])

    np.save(os.path.join(RAW_DIR, '308.npy'), Lr.astype(np.int16))
    spec = {
        'id': 308,
        'name': 'Whalebone Keep - Ice Vault',
        'parent': 306,
        'bgm': 'Cave',
        'field': 'FROZEN_LAKE',
        'map_audio': {'bgm': 'Dungeon - Ruins', 'bgs': 'Drip - Nadir', 'bgs_volume': 45, 'rain': False},
        'tone': [-22, -10, 16, 16],
        'fog': {'name': 'prismfall_cave', 'opacity': 22, 'blend': 1, 'zoom': 100, 'sx': 1, 'sy': 0},
        'gates': [
            {
                'name': 'Ice Vault Rock Smash & Strength Reliquaries',
                'from': [[16, 5]],
                'sealed': [[4, 16], [28, 16]],
            },
        ],
        'metadata': {
            'Name': 'Whalebone Keep - Ice Vault',
            'Outdoor': False,
            'ShowArea': True,
            'BattleBack': 'cave1',
            'MapPosition': RIME_POS,
        },
        'biome': 'interior',
        'tileset': TID_CAVE,
        'raw': 'data/raw/308.npy',
        'events': E,
    }
    with open(os.path.join(SPEC_DIR, '308_whalebone_keep_ice_vault.yaml'), 'w', encoding='utf-8') as f:
        f.write('# GENERATED by mapgen/layouts/whalebone_keep.py (Batch 3H): Whalebone Keep - Ice Vault.\n')
        f.write(yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))
    print('Wrote specs/308_whalebone_keep_ice_vault.yaml and data/raw/308.npy')
    return Lr


def main():
    build_305()
    build_306()
    build_307()
    build_308()


if __name__ == '__main__':
    main()
