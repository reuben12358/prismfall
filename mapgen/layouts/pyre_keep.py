#!/usr/bin/env python3
"""layouts/pyre_keep.py — Batch 3B: Pyre Keep — The Dominar's Citadel (5 Maps: 245, 246, 247, 248, 254):
  - Map 245: Pyre Keep - Rampart         (33x25, TS 61 PF Rejuv Forge, Outdoor, field DRAGONS_DEN)
      Two-tier obsidian caldera-rim bastion citadel overlooking blazing magma chasms:
      * Exact arrival from 240_cindervault_forge.yaml at (16, 22) facing up, return warps (15..17, 23) -> 240 (6, 3) down
      * Monumental gt_gate6 Keep Gateway (15..17, 5) -> 247 Hall of Oaths (16, 20) up
      * East Iron-Grate Rampart Skybridge (31, 12..14) -> 248 Dragon Roosts (2, 13) right
      * Central Dominar's Oath-Brazier Court, twin gt_tower keep watchtowers, Ashkaar Oath-Guards,
        patrolling Rapidash & Arcanine Followers, DRAGONFANG on West Bastion Lookout
  - Map 246: Pyre Keep - Ember Throne    (27x27, TS 61 PF Rejuv Forge, Interior, field DRAGONS_DEN)
      Symmetrical Obsidian-and-Crimson Imperial Throne Chamber of Ashkaar:
      * Panoramic glowing PF Magma Lava Window directly behind the Elevated Ember Throne Dais (TER)!
      * Empty crimson Ember Throne (Dominar is at the eastern capital), central Royal Oath-Brazier,
        5-wide crimson-carpeted imperial stair, flanking lava moats, colonnade, chandeliers, Lord-Steward Vaelen
        (Ashkaar Festival Delegation court lore), Throne Guard, FIRESTONE pickup
      * South Imperial Doors (12..14, 25) -> 247 Hall of Oaths (16, 6) down
  - Map 247: Pyre Keep - Hall of Oaths   (33x23, TS 61 PF Rejuv Forge, Interior, field DRAGONS_DEN)
      Great Hall of Ashkaar ("lying here is a capital crime"):
      * Sunken PF Magma Channel of True Flame bridged by crimson carpet & iron grates to the Great Oath-Brazier
      * Herald Pyke (canonical AS_TRIAL_OF_TRUTH giver + Ashkaar Trials board hook), Oath-Scribes,
        4 readable Dominion Oath Plinths, FIREGEM in East Reliquary Alcove
      * Bidirectional hub: South (15..17, 21) -> 245 Rampart (16, 6) · North (15..17, 5) -> 246 Ember Throne (13, 24)
        · West Crypt Arch (3, 12..13) -> 254 Ancestor Crypts (16, 26)
  - Map 248: Pyre Keep - Dragon Roosts   (36x24, TS 61 PF Rejuv Forge, Outdoor, field DRAGONS_DEN)
      Dramatic 3-tier cantilevered volcanic basalt aerie jutting out over a sweeping PF Magma lake:
      * Exact arrival from 240_cindervault_forge.yaml at (12, 20) facing up, return warps (11..13, 21) -> 240 (38, 3) down
      * West Rampart Skybridge (1, 12..14) -> 245 Rampart (30, 13) left
      * Canonical NPCs & Live Trials Hooks: Recruit Tamm + TRAPINCH (AS_AFRAID_OF_HEIGHTS), Roost-Mistress + AXEW &
        FLYGON (AS_EGG_RUN), Roost-Keeper Tarn (live pf_trial_talk(:ROOST_KEEPER)!), Old Cinder CHARIZARD on the High
        Roost promontory (live pf_trial_talk(:OLD_CINDER)!), plus perched SALAMENCE, NOIBAT, BAGON Followers
      * DRAGONGEM (NW Spur) & MAXPOTION (East Harness Deck)
  - Map 254: Pyre Keep - Ancestor Crypts (33x29, TS 61 PF Rejuv Forge, Dungeon, field HOLLOW_CATHEDRAL)
      Solemn obsidian cathedral-ossuary beneath Pyre Keep ("Ashfall dead in basalt niches"):
      * Subterranean glowing PF Magma river trenches bridged by riveted iron grates into West Sarcophagus Cloister
        & East Dragon-Rider Ossuary, ascending north stair to Elevated Sanctum of the First Dominar (TER)
      * Canonical PBS Trainer [CHANNELER, Thessaly] (pbs/trainers.txt:15682, 0 duplicates), Crypt Keeper,
        solemn LITWICK flame-tender, readable Ashfall epitaphs, SPELLTAG, DUSKBALL & STARPIECE pickups
      * South Crypt Stair (15..17, 27) -> 247 Hall of Oaths (4, 12) right

Run:
    /usr/bin/python3 -I mapgen/layouts/pyre_keep.py
"""
import os
import sys
from collections import deque
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cavekit import Cave, FLOOR, TER, TER2, MASS, P1
import rkit as K
from rkit import STAMPS
import rcompose as RC
import render as R
import passguard as PG
from verdance_palace import Palace

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TID = 61
CV_POS = [0, 24, 8]


# =================================================================================================
# Shared Helpers & Ashkaar Imperial Palace Subclass (TS 61 PF Rejuv Forge + PF Magma!)
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


def _place_building(m, name, x, y, mark_arch_clear=None):
    """Place a multi-tile fortress stamp (gt_gate6, gt_tower, gl_shed, etc.) cleanly on a Cave map."""
    st = STAMPS[name]
    w, h = st['w'], st['h']
    m.stamps.append((name, x, y))
    L = np.array(st['layers'])
    occ = L.max(axis=0) > 0
    if mark_arch_clear:
        for (ax, ay) in mark_arch_clear:
            lx, ly = ax - x, ay - y
            if 0 <= lx < w and 0 <= ly < h:
                occ[ly, lx] = False
    m.taken[y:y + h, x:x + w] |= occ
    m.bodym[y:y + h, x:x + w] |= occ


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


def _make_follower(name, at, species, d, cry_line):
    return {
        'type': 'event',
        'name': name,
        'at': list(at),
        'pages': [{
            'graphic': {'sprite': f'Followers/{species}', 'dir': d},
            'trigger': 'action',
            'move': 'fixed',
            'commands': [
                {'se': f'Cries/{species}'},
                cry_line,
            ],
        }],
    }


def _sign(name, at, text):
    return {'type': 'sign', 'name': name, 'at': list(at), 'post': False, 'text': text}


def _verify_4bit_bfs(Lr, events, start, targets, label):
    """Strict Essentials 4-bit directional BFS on TS 61 resolved map layers."""
    import build as B
    ts = R.tilesets()[TID]
    H, W = Lr.shape[1:]
    solid_ev = set()
    for e in events:
        if e.get('type') in ('npc', 'trainer', 'mart'):
            solid_ev.add(tuple(e['at']))
        elif e.get('type') == 'event':
            pg0 = (e.get('pages') or [{}])[0]
            if (pg0.get('graphic') or {}).get('sprite') and not pg0.get('through'):
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

    sx, sy = start
    assert ok[sy, sx], f'{label}: BFS start {start} is NOT passable!'
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
    for name, (tx, ty), adj in targets:
        if adj:
            reach = (tx, ty) in seen or any((tx + dx, ty + dy) in seen for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)))
        else:
            reach = (tx, ty) in seen
        if not reach:
            missing.append((name, (tx, ty), bool(B.cell_passable(Lr, ts, tx, ty))))
    print(f'{label} BFS: {len(seen)} walkable cells reached from {start}; missing={missing}')
    assert not missing, f'{label} unreachable targets: {missing}'
    return seen


def _paint_path_rect(m, x0, y0, x1, y1, palette, floorpatch_ids):
    for y in range(max(0, y0), min(m.H, y1 + 1)):
        for x in range(max(0, x0), min(m.W, x1 + 1)):
            if m.cls[y, x] != '.' or m.cliff[y, x] or m.taken[y, x]:
                continue
            m.L[0, y, x] = palette[(x * 3 + y * 5) % len(palette)]
            if int(m.L[1, y, x]) in floorpatch_ids:
                m.L[1, y, x] = 0


class AshkaarPalace(Palace):
    """Obsidian, crimson-lacquer & volcanic magma Imperial Citadel interior on TS 61 (PF Rejuv Forge)."""

    def __init__(self, W, H, seed):
        super().__init__(W, H, seed, tid=TID, pool='Magma')
        self.kit = {'default': 'cvH', TER: 'cvH'}
        self.STAIRS = tuple(P1('mn_stair_' + k) for k in 'lmr')
        self.ash_zones = []  # (x0, y0, x1, y1, kind)

    def ash_floor(self, x0, y0, x1, y1, kind):
        self.ash_zones.append((x0, y0, x1, y1, kind))

    def _apply_custom_floors(self):
        super()._apply_custom_floors()
        pals = {
            'ashlar': [P1('T_f%d' % i) for i in range(4)],
            'basalt': [P1('L_f%d' % i) for i in range(4)],
            'obsidian': [P1('N_f%d' % i) for i in range(4)],
            'iron': [P1('Q_f%d' % i) for i in range(4)],
            'soot': [P1('lm_low%d' % i) for i in range(4)],
        }
        for x0, y0, x1, y1, kind in self.ash_zones:
            pal = pals[kind]
            for y in range(max(0, y0), min(self.H, y1 + 1)):
                for x in range(max(0, x0), min(self.W, x1 + 1)):
                    if self.cls[y, x] == '.' and not self.cliff[y, x]:
                        self.L[0, y, x] = pal[(x * 3 + y * 5) % len(pal)]


# =================================================================================================
# MAP 245 — Pyre Keep - Rampart (33x25, TS 61 PF Rejuv Forge, Outdoor, DRAGONS_DEN)
# Exact arrival from 240_cindervault_forge.yaml: (16, 22) facing up!
# =================================================================================================
def build_245():
    W, H = 33, 25
    m = Cave(W, H, 'L', seed=245, pool='Magma', tid=TID)
    m.STAIRS = K.STAIRS_STONE
    m.kit = {MASS: 'cvL', TER2: 'cvL', TER: 'cvL', FLOOR: 'cvL', 'default': 'cvL'}

    # ---- 1. Sculpt Dramatic Two-Tier Obsidian Caldera-Rim Rampart Over Blazing Magma Chasms ----
    # South Approach Gatehouse Forecourt (FLOOR=1, x=7..25, y=18..23 + exit notch x=14..18, y=23..24!)
    m.box(7, 18, 25, 23, FLOOR, '.')
    m.box(14, 23, 18, 24, FLOOR, '.')
    # West & East Caldera Magma Chasms plunging past the Rampart walls (FLOOR=1 filled with PF Magma!)
    m.box(2, 11, 6, 21, FLOOR, 'w')
    m.box(26, 15, 30, 22, FLOOR, 'w')
    m.box(26, 5, 30, 10, FLOOR, 'w')

    # Upper Citadel Rampart & Dominar's Oath-Brazier Courtyard (TER=2, x=3..29, y=5..17)
    m.box(3, 5, 29, 17, TER, '.')
    # Recessed North Keep Gateway terrace (x=10..22, y=1..5) framing gt_gate6 cleanly!
    m.box(10, 1, 22, 5, TER, '.')
    # East Skybridge Causeway exiting cleanly to 248 Dragon Roosts (x=29..32, y=11..15 — carved past x=31!)
    m.box(29, 10, 32, 15, TER, '.')

    # Dramatic volcanic crag corners & basalt spurs
    m.mass_at([
        (3, 5), (4, 5), (3, 6), (29, 5), (28, 5), (29, 6),
        (3, 16), (3, 17), (4, 17), (29, 16), (29, 17), (28, 17),
        (7, 22), (7, 23), (8, 23), (25, 22), (25, 23), (24, 23),
        (10, 1), (22, 1),
    ])

    # Flanking glowing magma moat pockets tucked along the upper rampart flanks
    for mx, my in ((4, 12), (5, 12), (4, 13), (5, 13), (4, 14), (5, 14),
                   (27, 7), (28, 7), (27, 8), (28, 8)):
        m.cls[my, mx] = 'w'

    # Twin Grand Obsidian Bastion Staircases connecting Upper Rampart (TER) <-> South Forecourt (FLOOR)
    m.stairs(10, 17, w=3, n=3, c='.')    # West Rampart Stair (x=10..12, y=17..19 -> lands y=20)
    m.stairs(20, 17, w=3, n=3, c='.')    # East Rampart Stair (x=20..22, y=17..19 -> lands y=20)

    m.tidy()
    m.plan_cliffs(rows=3)

    # ---- 2. Monumental Pyre Keep Gatehouse (gt_gate6 12x8) & Twin Flanking Watchtowers ----
    # gt_gate6 at (10, 0) -> x=10..21, y=0..7; walkable central iron portcullis arch x=13..18, y=5..7!
    keep_arch_clear = [(x, y) for y in (5, 6, 7) for x in (13, 14, 15, 16, 17, 18)]
    _place_building(m, 'gt_gate6', 10, 0, mark_arch_clear=keep_arch_clear)
    _place_building(m, 'gt_tower', 6, 3)       # West Keep Watchtower (3x6 -> x=6..8, y=3..8)
    _place_building(m, 'gt_tower', 23, 3)      # East Keep Watchtower (3x6 -> x=23..25, y=3..8)

    # ---- 3. Bidirectional Warps, Ashkaar Oath-Guards, Follower Pokémon, Plaques & Pickup ----
    E = m.events

    # South Return Warps -> 240 Cindervault - Forge Terraces (6, 3, down) [matches 240 -> 245 (16,22) up!]
    for rx in (15, 16, 17):
        E.append({
            'type': 'warp',
            'name': 'South to Forge Terraces (240)',
            'at': [rx, 23],
            'to': {'map': 240, 'x': 6, 'y': 3, 'dir': 'down'},
            'se': 'Door exit',
        })

    # North Grand Keep Portcullis -> 247 Pyre Keep - Hall of Oaths (16, 20, up)
    for nx in (15, 16, 17):
        E.append({
            'type': 'warp',
            'name': 'Into Hall of Oaths (247)',
            'at': [nx, 5],
            'to': {'map': 247, 'x': 16, 'y': 20, 'dir': 'up'},
            'se': 'Door enter',
        })

    # East Iron-Grate Rampart Skybridge -> 248 Pyre Keep - Dragon Roosts (2, 13, right)
    for ey in (12, 13, 14):
        E.append({
            'type': 'warp',
            'name': 'East Skybridge to Dragon Roosts (248)',
            'at': [31, ey],
            'to': {'map': 248, 'x': 2, 'y': 13, 'dir': 'right'},
            'se': 'Door enter',
        })

    # Canonical Pyre Keep Rampart NPCs & Ashkaar Follower Pokémon
    E += [
        _make_npc('Oath-Guard Captain', (14, 10), 'trainer_ASHKAAR_OFFICER', 'down', [
            "Oath-Guard Captain: Pyre Keep — the Dominar's western seat on Cindervault's caldera rim.",
            "Oath-Guard Captain: Through the north portcullis lies the Hall of Oaths. Say true, or say nothing; lying beneath that roof is a capital crime.",
        ]),
        _make_npc('Rampart Sentinel', (17, 10), 'trainer_ASHKAAR_SOLDIER_F', 'down', [
            "Rampart Sentinel: The Dominar sits at the eastern capital while the passes tighten, so the Ember Throne stands empty today.",
            "Rampart Sentinel: Still, the Oath-Brazier burns day and night. No Ashkaar sentinel lets a keep fire go cold.",
        ]),
        _make_npc('Gate Watchman', (14, 21), 'trainer_ASHKAAR_SOLDIER_M', 'right', [
            "Gate Watchman: Welcome up from the Forge Terraces. Climb either basalt stair to reach the Rampart Court.",
            "Gate Watchman: The east iron skybridge crosses directly over the caldera updraft to the Dragon Roosts.",
        ]),
        _make_npc('Skybridge Rider', (27, 12), 'trainer_ASHKAAR_EMBER_RIDER', 'left', [
            "Skybridge Rider: Mind your hat crossing east — the Salamence dive straight under that span when the caldera bells ring!",
        ]),
        _make_follower('Rampart Rapidash', (20, 12), 'RAPIDASH', 'left',
                       "Rapidash snorts a bright plume of embers, stamping impatiently on the obsidian flagstones."),
        _make_follower('Guard Arcanine', (11, 12), 'ARCANINE', 'right',
                       "Arcanine lets out a warm, low rumble, eyes fixed steadily on the south stair."),
        _sign('Dominar Edict Plaque', (16, 13),
              "THE RAMPART OATH-BRAZIER — 'HERE STANDS PYRE KEEP, SEAT OF ASHKAAR ON THE CALDERA RIM. SAY TRUE, OR SAY NOTHING.'"),
        _sign('Skybridge Sign', (28, 14),
              "EAST SKYBRIDGE — → PYRE KEEP DRAGON ROOSTS (248). Keep your harness clipped and your head low."),
        {'type': 'item', 'at': [4, 11], 'item': 'DRAGONFANG', 'name': 'Rampart Dragon Fang'},
    ]

    # Protect warps, arrivals, stairs, skybridge & NPCs
    m.keep_clear |= {
        (15, 22), (16, 22), (17, 22), (15, 23), (16, 23), (17, 23), (16, 21),
        (15, 5), (16, 5), (17, 5), (15, 6), (16, 6), (17, 6), (16, 7), (16, 8), (16, 9),
        (30, 12), (30, 13), (30, 14), (31, 12), (31, 13), (31, 14), (29, 13),
    }
    for e in E:
        ex, ey = e['at']
        m.keep_clear.add((ex, ey))
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            if m.inb(ex + dx, ey + dy):
                m.keep_clear.add((ex + dx, ey + dy))

    # ---- 4. Imperial Citadel Rampart Props: Central Oath-Brazier, Banners, Siege Racks, Beacons & Lighting ----
    # Central Dominar's Oath-Brazier standing proud at (16, 12..13) — solid base at (16,13) backs Dominar Edict Plaque!
    _place_stamp_over(m, 'fw_brazier', 16, 12, base_z=1, top_z=2, top_rows=1, solid=True)
    # Real solid Skybridge Signpost at (28, 13..14) — solid post base (pas=0xf) at (28,14) eliminates over_trigger? trap!
    _place_stamp_over(m, 'pf_signpost', 28, 13, base_z=1, top_z=2, top_rows=1, solid=True)
    # Processional Ashkaar Dragon Banners & Braziers symmetrically framing the 6-wide gt_gate6 arch (x=13..18)!
    for bx, by in ((12, 8), (19, 8), (12, 14), (19, 14), (9, 20), (23, 20)):
        _place_stamp_over(m, 'fw_brazier', bx, by, base_z=1, top_z=2, top_rows=1, solid=True)
    for bx, by in ((10, 8), (21, 8), (9, 11), (22, 11), (13, 21), (19, 21), (29, 10), (29, 15)):
        _place_stamp_over(m, 'wr_ban_ash', bx, by, base_z=1, top_z=2, top_rows=2, solid=True)
    # West Bastion Lookout & Siege Supply Arsenal (beacon cleanly clear of north cliff lip!)
    _place_stamp_over(m, 'pf_beacon', 4, 8, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'wr_rack', 7, 10, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'wr_supply', 7, 13, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'wr_rack', 25, 10, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'pf_stonebench', 10, 15, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'pf_stonebench', 21, 15, base_z=1, top_z=1, top_rows=0, solid=True)
    # Iron rampart bollards symmetrically along skybridge & south overlook
    for bx, by in ((13, 16), (14, 16), (17, 16), (18, 16), (29, 11), (30, 11), (29, 15), (30, 15)):
        if (bx, by) not in m.keep_clear:
            _place_stamp_over(m, 'lm_bollard', bx, by, base_z=1, top_z=1, top_rows=0, solid=True)

    # Volcanic caldera steam plumes rising strictly off magma + mirror-symmetric fire halos (never clobbering L2 flames!)
    for sx, sy in ((4, 19), (5, 20), (28, 18), (27, 8), (4, 13)):
        _place_stamp_over(m, 'lm_steam0' if (sx + sy) % 2 == 0 else 'lm_steam1', sx, sy, base_z=2, top_z=2, top_rows=2, solid=False)
    for gx, gy in ((12, 8), (18, 8), (12, 14), (18, 14), (4, 8), (9, 20), (22, 20)):
        m.stamps.append(('pf_glow', gx, gy))

    m.paint()

    # ---- 5. Moody Ashkaar Imperial Rampart Paving Hierarchy ----
    low_ids = [P1('lm_low%d' % i) for i in range(4)]
    slate_ids = [P1('T_f%d' % i) for i in range(4)]
    earth_ids = [P1('E_f%d' % i) for i in range(4)]
    qf0, qf1 = P1('Q_f0'), P1('Q_f1')
    grate = P1('lm_grate')
    fp = {P1(k) for k in STAMPS if k.startswith(('L_floorpatch_', 'L_fd'))}

    _paint_path_rect(m, 8, 20, 24, 22, low_ids, fp)
    _paint_path_rect(m, 14, 20, 18, 24, slate_ids, fp)
    _paint_path_rect(m, 8, 9, 24, 16, low_ids, fp)
    # Exact 6-wide slate road (x=13..18) aligned flush with gt_gate6's 6-wide portcullis arch!
    _paint_path_rect(m, 13, 5, 18, 16, slate_ids, fp)
    _paint_path_rect(m, 10, 15, 22, 16, earth_ids, fp)
    _paint_path_rect(m, 18, 12, 29, 14, slate_ids, fp)
    # Iron-Grate East Skybridge Span (x=29..32, y=12..14)
    for y in (12, 13, 14):
        for x in (29, 30, 31, 32):
            if m.inb(x, y) and m.cls[y, x] == '.' and not m.cliff[y, x]:
                m.L[0, y, x] = qf0 if (x + y) % 2 == 0 else qf1
                m.L[1, y, x] = grate

    Lr = RC.resolve(m.L, TID).astype(np.int32)
    ev_pts = [tuple(e['at']) for e in E]
    PG.guard(Lr, TID, ev_pts, 'Map 245')
    assert not PG.hits(Lr, R.tilesets()[TID], ev_pts), 'Map 245 passguard hits!'
    m.L = Lr

    _verify_4bit_bfs(Lr, E, (16, 22), [
        ('South Return -> 240', (16, 23), False),
        ('North Portcullis -> 247', (16, 5), False),
        ('East Skybridge -> 248', (31, 13), False),
        ('Oath-Guard Captain', (14, 10), True),
        ('Rampart Sentinel', (17, 10), True),
        ('Skybridge Rider', (27, 12), True),
        ('Dragon Fang Lookout', (4, 11), True),
        ('Dominar Edict Plaque', (16, 13), True),
        ('Skybridge Sign', (28, 14), True),
    ], 'Map 245 Pyre Keep - Rampart')

    head = {
        'id': 245,
        'name': 'Pyre Keep - Rampart',
        'parent': 240,
        'bgm': 'Lava Town',
        'field': 'DRAGONS_DEN',
        'map_audio': {'bgm': 'Town - Ashkaar', 'bgs': 'Lava - Ashkaar', 'bgs_volume': 55, 'rain': False},
        'metadata': {'Name': 'Pyre Keep', 'Outdoor': True, 'ShowArea': True, 'MapPosition': CV_POS, 'BattleBack': 'cave1'},
        'tone': [22, 2, -16, 10],
        'fog': {'name': 'prismfall_cave', 'opacity': 20, 'blend': 1, 'zoom': 100, 'sx': 1, 'sy': 0},
        '_file': '245_pyre_keep_rampart.yaml',
    }
    m.write(245, head, comment='# GENERATED by mapgen/layouts/pyre_keep.py (Batch 3B): Pyre Keep - Rampart.\n'
                               '# Edit the layout script, not this file.\n')
    return m, Lr


# =================================================================================================
# MAP 247 — Pyre Keep - Hall of Oaths (33x23, TS 61 PF Rejuv Forge, Interior, DRAGONS_DEN)
# =================================================================================================
def build_247():
    W, H = 33, 23
    m = AshkaarPalace(W, H, seed=247)
    Rb = m.room_box

    # ---- 1. Void-Sculpted Cruciform Great Hall of Ashkaar with Sunken Magma Ribbon of True Flame ----
    # North Elevated Throne Portal Vestibule (TER, x=11..21, y=3..7 — stairs down y=7..9!)
    Rb(11, 3, 21, 7, TER, 'Y', 'H')
    # Central Vaulted Oath Nave (FLOOR, x=10..22, y=8..20)
    Rb(10, 8, 22, 20, FLOOR, 'H', 'H')
    # West Crypt-Cloister Wing (FLOOR, x=3..10, y=9..18 — Crypt Descent Portal at x=3, y=12..13!)
    Rb(3, 9, 10, 18, FLOOR, 'H', 'H')
    # East Oath-Archive Cloister Wing (FLOOR, x=22..29, y=9..18 — FIREGEM Reliquary Alcove!)
    Rb(22, 9, 29, 18, FLOOR, 'H', 'H')
    # Narrowed South Entry Portal framing warps (15..17, 21) -> 245 Rampart
    m.box(13, 20, 19, 21, FLOOR)

    m.mass_at([
        (3, 9), (4, 9), (3, 17), (3, 18), (4, 18),
        (28, 9), (29, 9), (29, 17), (29, 18), (28, 18),
        (11, 3), (21, 3),
    ])

    # Sunken Glowing PF Magma Channels of True Flame flanking the Central Oath-Brazier Dais!
    for my in range(11, 18):
        if my in (13, 14):
            continue  # wide basalt crossing lanes to West Crypt & East Cloister!
        for mx in (11, 12, 20, 21):
            m.cls[my, mx] = 'w'

    # Grand 5-Wide Crimson-Carpeted Staircase descending from North Throne Portal Vestibule (y=7..9)
    m.stairs(14, 7, w=5, n=3, c='.')
    m.plan_cliffs(rows=3)

    # ---- 2. Obsidian-Ashlar Flooring, Crimson Royal Runners & Iron-Grate Crossings ----
    m.ash_floor(11, 5, 21, 7, 'ashlar')
    m.ash_floor(10, 10, 22, 21, 'ashlar')
    m.ash_floor(3, 11, 10, 17, 'obsidian')
    m.ash_floor(22, 11, 29, 17, 'obsidian')
    m.runner(15, 5, 17, 7)
    m.runner(15, 10, 17, 21)
    # East & West cross-aisle crimson rugs bridging to the Crypt Arch & East Reliquary
    m.rug('R', 4, 12, 9, 15, medallion=False)
    m.rug('R', 23, 12, 28, 15, medallion=False)

    # ---- 3. Architectural Walls, Monumental Columns, Oath Banners, Braziers & Lighting ----
    # North Throne Room Double-Door set into north wall (16, 4) — leaves (15..17, 5) walkable for warps!
    m.late.append((1, 16, 4, P1('mn_door')))
    m.late.append((1, 15, 4, P1('mn_sconce')))
    m.late.append((1, 17, 4, P1('mn_sconce')))
    for wx, wy in ((13, 3), (19, 3), (6, 9), (8, 9), (24, 9), (26, 9)):
        m.on('mn_window', wx, wy)
    for bx, by in ((14, 3), (18, 3), (5, 9), (9, 9), (23, 9), (27, 9)):
        m.on('wr_ban_ash', bx, by)

    # Twin Legion Armour Suits & Candelabras framing the Ember Throne Portal
    m.on('mn_armour', 12, 5)
    m.on('mn_armour', 20, 5)
    m.on('mn_candelabra', 12, 6)
    m.on('mn_candelabra', 20, 6)

    # Monumental Obsidian Colonnade & Flaming Oath-Braziers along the Nave
    for x in (13, 19):
        for y in (10, 15, 18):
            m.on('nr_col', x, y)
    # Central Great Oath-Brazier Plinth at (16, 13)
    m.on('fw_brazier', 16, 12)
    m.on('fw_brazier', 14, 19)
    m.on('fw_brazier', 18, 19)

    # Four Carved Memorial Oath Plinths (2 West Cloister, 2 East Cloister — cleanly OFF the gold rug borders!)
    m.on('mn_plinth', 6, 11)
    m.on('mn_plinth', 8, 16)
    m.on('mn_plinth', 26, 11)
    m.on('mn_plinth', 24, 16)
    m.on('mn_armour', 4, 15)
    m.on('mn_armour', 28, 15)
    m.on('mn_candelabra', 5, 16)
    m.on('mn_candelabra', 27, 16)
    m.on('mn_bench', 6, 17)
    m.on('mn_bench', 25, 17)

    # Framed West Crypt Descent Portal (3, 12..13): Ashfall mourning banner, flanking brazier, real signpost & stone steps!
    m.on('wr_ban_ash_t', 3, 9)
    m.on('fw_brazier', 3, 14)
    m.on('pf_signpost', 4, 10)
    m.late.append((1, 3, 12, P1('st_stair_m')))
    m.late.append((1, 3, 13, P1('st_stair_m')))

    # Chandelier (cleanly unobstructed over south nave!), Clerestory Light Shafts & Symmetric Fire Glows
    m.stamps.append(('mn_chandelier', 15, 17))
    for sx, sy in ((15, 5), (6, 11), (26, 11)):
        m.stamps.append(('cv_shaft', sx, sy))
    for gx, gy in ((14, 19), (17, 19), (5, 16), (26, 16)):
        m.stamps.append(('pf_glow', gx, gy))

    # ---- 4. Bidirectional Warps, Herald Pyke (AS_TRIAL_OF_TRUTH), Oath Plinths & Pickup ----
    pyke_ruby = (
        'pbMessage(_INTL("Herald Pyke: You stand in the Hall of Oaths. Under this vault, every word is weighed by flame — lying here is a capital crime."))\n'
        'if $game_switches[120]\n'
        '  pbMessage(_INTL("Herald Pyke: Word reached the Keep of what you did down at Meridian Tap Seven. When the Dominion convenes the Trial of Truth, your testimony will weigh heavy indeed."))\n'
        'else\n'
        '  pbMessage(_INTL("Herald Pyke: Beyond the north steps lies the Ember Throne; through the west arch, the steps drop into the Ancestor Crypts of House Ashfall."))\n'
        'end\n'
        'if defined?(pf_trial_board)\n'
        '  if pbConfirmMessage(_INTL("Herald Pyke: Would you inspect the Ashkaar Trial Rolls while you are here?"))\n'
        '    pf_trial_board(:ASHKAAR)\n'
        '  end\n'
        'end'
    )
    m.events = [
        # South Return Warps -> 245 Rampart (16, 6, down)
        {'type': 'warp', 'name': 'South to Rampart (245) L', 'at': [15, 21], 'to': {'map': 245, 'x': 16, 'y': 6, 'dir': 'down'}, 'se': 'Door exit'},
        {'type': 'warp', 'name': 'South to Rampart (245)', 'at': [16, 21], 'to': {'map': 245, 'x': 16, 'y': 6, 'dir': 'down'}, 'se': 'Door exit'},
        {'type': 'warp', 'name': 'South to Rampart (245) R', 'at': [17, 21], 'to': {'map': 245, 'x': 16, 'y': 6, 'dir': 'down'}, 'se': 'Door exit'},
        # North Throne Portal -> 246 Pyre Keep - Ember Throne (13, 24, up)
        {'type': 'warp', 'name': 'North to Ember Throne (246) L', 'at': [15, 5], 'to': {'map': 246, 'x': 13, 'y': 24, 'dir': 'up'}, 'se': 'Door enter'},
        {'type': 'warp', 'name': 'North to Ember Throne (246)', 'at': [16, 5], 'to': {'map': 246, 'x': 13, 'y': 24, 'dir': 'up'}, 'se': 'Door enter'},
        {'type': 'warp', 'name': 'North to Ember Throne (246) R', 'at': [17, 5], 'to': {'map': 246, 'x': 13, 'y': 24, 'dir': 'up'}, 'se': 'Door enter'},
        # West Crypt Descent Arch -> 254 Pyre Keep - Ancestor Crypts (16, 26, up)
        {'type': 'warp', 'name': 'West to Ancestor Crypts (254)', 'at': [3, 12], 'to': {'map': 254, 'x': 16, 'y': 26, 'dir': 'up'}, 'se': 'Door enter'},
        {'type': 'warp', 'name': 'West to Ancestor Crypts (254) ', 'at': [3, 13], 'to': {'map': 254, 'x': 16, 'y': 26, 'dir': 'up'}, 'se': 'Door enter'},
        # Herald Pyke (canonical AS_TRIAL_OF_TRUTH giver — moved 1 tile south to (16,15) so brazier flame stays cleanly above!)
        {
            'type': 'event',
            'name': 'Herald Pyke',
            'at': [16, 15],
            'pages': [{
                'graphic': {'sprite': 'trainer_ASHKAAR_OFFICER', 'dir': 'down'},
                'trigger': 'action',
                'move': 'fixed',
                'commands': [{'script': pyke_ruby}],
            }],
        },
        _make_npc('Crypt Warden', (5, 13), 'trainer_ASHKAAR_SOLDIER_M', 'right', [
            "Crypt Warden: The western stair descends into the Ancestor Crypts where three centuries of House Ashfall rest in basalt niches.",
            "Crypt Warden: Tread lightly — Channelers keep vigil below, and the Ashfall dead do not suffer discourtesy.",
        ]),
        _make_npc('Oath-Scribe', (24, 13), 'NPC 22', 'left', [
            "Oath-Scribe: Every treaty, duel, and merchant boast ever sworn in Cindervault is recorded on these stone plinths.",
            "Oath-Scribe: You would not believe how many swordsmen have been dragged in here over the word 'Excellent.'",
        ]),
        _make_npc('Throne Usher', (14, 6), 'trainer_ASHKAAR_SOLDIER_F', 'right', [
            "Throne Usher: The Ember Throne lies straight north. The Dominar is at the eastern capital, yet the court remains open to honest visitors.",
        ]),
        _sign('Great Oath-Brazier', (16, 13),
              "THE GREAT OATH-BRAZIER — Set in bronze hand-marks worn glossy by centuries of sworn palms. 'SAY TRUE, OR SAY NOTHING.'"),
        _sign('West Crypt Sign', (4, 11),
              "WEST CRYPT STAIR — ↓ ANCESTOR CRYPTS OF HOUSE ASHFALL (254). Tread softly and keep plain speech beneath the vault."),
        _sign('Oath Plinth I — The Flame', (6, 11),
              "FIRST OATH OF ASHKAAR: 'The Flame Plate belongs to the mountain, and the mountain answers only to truth.'"),
        _sign('Oath Plinth II — Plain Speech', (8, 16),
              "LAW OF PLAIN SPEECH: 'A man who lies under the roof of Pyre Keep forfeits his steel, his banner, and his head.'"),
        _sign('Oath Plinth III — The Riders', (26, 11),
              "OATH OF THE ROOSTS: 'No dragon flies beneath a false banner. First rider to mount, last rider to land.'"),
        _sign('Oath Plinth IV — The Concordance', (24, 16),
              "THE CONCORDANCE STONE: 'What is placed in a Warden's keeping stays in a Warden's keeping — even against a Dominar's seal.'"),
        {'type': 'item', 'at': [28, 14], 'item': 'FIREGEM', 'name': 'Hall of Oaths Fire Gem'},
    ]

    m.paint()
    # Recessed dark obsidian arched stone crypt mouth on x=2 behind West Crypt descent stairs (eliminates raw void edge!)
    for cy in (12, 13):
        m.L[0, cy, 2] = P1('T_f0')
        m.L[1, cy, 2] = P1('cv_gate_open')
        m.L[2, cy, 2] = 0
    # Add riveted iron-grate walkways framing the cross-aisle lanes beside the magma channels
    for y in (13, 14):
        for x in (11, 12, 20, 21):
            if m.cls[y, x] == '.' and m.L[1, y, x] == 0:
                m.L[1, y, x] = P1('lm_grate')

    Lr = RC.resolve(m.L, TID).astype(np.int32)
    ev_pts = [tuple(e['at']) for e in m.events]
    PG.guard(Lr, TID, ev_pts, 'Map 247')
    assert not PG.hits(Lr, R.tilesets()[TID], ev_pts), 'Map 247 passguard hits!'
    m.L = Lr

    _verify_4bit_bfs(Lr, m.events, (16, 20), [
        ('South -> 245 Rampart', (16, 21), False),
        ('North -> 246 Ember Throne', (16, 5), False),
        ('West -> 254 Ancestor Crypts', (3, 12), False),
        ('Crypt Return Landing (4,12)', (4, 12), False),
        ('West Crypt Sign', (4, 11), True),
        ('Herald Pyke', (16, 15), True),
        ('Crypt Warden', (5, 13), True),
        ('Oath-Scribe', (24, 13), True),
        ('Throne Usher', (14, 6), True),
        ('Oath Plinth I', (6, 11), True),
        ('Oath Plinth III', (26, 11), True),
        ('Fire Gem', (28, 14), True),
    ], 'Map 247 Pyre Keep - Hall of Oaths')

    head = {
        'id': 247,
        'name': 'Pyre Keep - Hall of Oaths',
        'parent': 245,
        'bgm': 'Lava Town',
        'field': 'DRAGONS_DEN',
        'map_audio': {'bgm': 'Theme - Accord', 'bgs': '', 'rain': False},
        'metadata': {'Name': 'Pyre Keep', 'SnapEdges': True, 'MapPosition': CV_POS, 'BattleBack': 'cave1'},
        'tone': [16, 0, -16, 10],
        '_file': '247_pyre_keep_hall_of_oaths.yaml',
    }
    m.write(247, head, comment='# GENERATED by mapgen/layouts/pyre_keep.py (Batch 3B): Pyre Keep - Hall of Oaths.\n'
                               '# Edit the layout script, not this file.\n')
    return m, Lr


# =================================================================================================
# MAP 246 — Pyre Keep - Ember Throne (27x27, TS 61 PF Rejuv Forge, Interior, DRAGONS_DEN)
# Iconic design/maps.json features: "throne before a lava window; oath-brazier; Festival delegation court"
# =================================================================================================
def build_246():
    W, H = 27, 27
    m = AshkaarPalace(W, H, seed=246)
    Rb = m.room_box

    # ---- 1. Symmetrical Imperial Obsidian Throne Chamber with Panoramic Volcanic Caldera Lava Window! ----
    # Panoramic Glowing Caldera Lava Window behind the Ember Throne (TER, x=9..17, y=2..4 -> 3 full rows PF Magma!)
    m.box(9, 2, 17, 4, TER, 'w')
    # Elevated Imperial Ember Throne Dais (TER, x=8..18, y=5..10 — Parapet y=5, Promenade y=6, Throne (13, 7)!)
    Rb(8, 5, 18, 10, TER, 'Y', 'H')
    # Re-assert the full 9x3 Caldera Lava Window directly behind the Throne Dais (x=9..17, y=2..4) after room_box
    for wy in (2, 3, 4):
        for wx in range(9, 18):
            m.ht[wy, wx] = TER
            m.cls[wy, wx] = 'w'
    # Central Imperial Audience Court (FLOOR, x=7..19, y=11..24)
    Rb(7, 11, 19, 24, FLOOR, 'H', 'H')
    # Symmetrical Flanking Magma Moats & Viewing Galleries (FLOOR, West x=3..7 & East x=19..23, y=12..21)
    Rb(3, 12, 7, 21, FLOOR, 'H', 'H')
    Rb(19, 12, 23, 21, FLOOR, 'H', 'H')
    # Narrowed Monumental South Portal framing warps (12..14, 25) -> 247 Hall of Oaths
    m.box(10, 24, 16, 25, FLOOR)

    m.mass_at([
        (3, 12), (4, 12), (3, 20), (3, 21), (4, 21),
        (22, 12), (23, 12), (23, 20), (23, 21), (22, 21),
        (8, 5), (18, 5), (10, 25), (16, 25),
    ])

    # Symmetrical Flanking Magma Moats framing the West & East Side Galleries (leaves x=6..7 & x=19..20 walkable!)
    for my in range(14, 20):
        for mx in (4, 5, 21, 22):
            m.cls[my, mx] = 'w'

    # Grand 5-Wide Crimson Imperial Staircase descending from Ember Throne Dais (x=11..15, y=10..12)
    m.stairs(11, 10, w=5, n=3, c='.')
    m.plan_cliffs(rows=3)

    # ---- 2. Multi-Zone Imperial Flooring: Obsidian-Ashlar Court + Continuous Crimson Royal Carpet Runner ----
    m.ash_floor(8, 5, 18, 10, 'iron')
    m.ash_floor(9, 6, 17, 9, 'ashlar')
    m.ash_floor(8, 13, 18, 24, 'ashlar')
    m.ash_floor(6, 13, 7, 21, 'obsidian')
    m.ash_floor(19, 13, 20, 21, 'obsidian')
    m.ash_floor(10, 24, 16, 25, 'soot')
    # Continuous Sweeping Crimson-and-Gold Royal Runner (NO broken y=13..14 stub!) up to the Elevated Ember Throne!
    m.runner(12, 13, 14, 25)
    m.runner(12, 7, 14, 9)

    # ---- 3. Solid Lava-Window Parapet (y=5), Grand Ember Throne Ensemble (13,7), Colonnade & Symmetric Glow ----
    # Solid Imperial Balustrade/Parapet across y=5 (pas=0xf) separating dais promenade (y=6) from caldera magma (y=2..4)!
    # Facing north from (13, 6) cleanly reads Lava Window Aperture at (13, 5) with over_trigger? == false!
    m.on('nr_col', 9, 4)
    m.on('nr_col', 17, 4)
    m.late.append((2, 10, 5, P1('lm_railing_w')))
    for rx in range(11, 16):
        m.late.append((2, rx, 5, P1('lm_railing_m')))
    m.late.append((2, 16, 5, P1('lm_railing_e')))

    # Elevated Imperial Ember Throne centerpiece at (13, 7) tightly framed by candelabras, guardian statues, banners & braziers!
    m.on('mn_chairR_down', 13, 7)
    m.on('mn_candelabra', 11, 6)
    m.on('mn_candelabra', 15, 6)
    m.on('mn_statue', 10, 6)
    m.on('mn_statue', 16, 6)
    m.on('wr_ban_ash', 8, 5)
    m.on('wr_ban_ash', 18, 5)
    m.on('fw_brazier', 9, 8)
    m.on('fw_brazier', 17, 8)

    # Central Royal Oath-Brazier standing grandly on the continuous royal runner at (13, 14..15)
    m.on('fw_brazier', 13, 14)

    # Symmetrical Imperial Colonnade flanking the Royal Audience Court!
    for x in (9, 17):
        for y in (13, 17, 21):
            m.on('nr_col', x, y)
    for bx, by in ((10, 22), (16, 22), (7, 15), (19, 15)):
        m.on('fw_brazier', bx, by)
    for ax, ay in ((8, 13), (18, 13), (8, 22), (18, 22)):
        m.on('mn_armour', ax, ay)
    for bx, by in ((7, 11), (19, 11), (11, 23), (15, 23)):
        m.on('wr_ban_ash', bx, by)

    # Single unobstructed Chandelier over the south audience court (dais completely clear!), Sunbeams & Symmetric Fire Glows!
    m.stamps.append(('mn_chandelier', 12, 19))
    for sx, sy in ((11, 5), (14, 5), (12, 17)):
        m.stamps.append(('cv_shaft', sx, sy))
    for gx, gy in ((9, 8), (16, 8), (10, 22), (15, 22), (7, 15), (18, 15)):
        m.stamps.append(('pf_glow', gx, gy))

    # ---- 4. Events: South Return Warps, Empty Throne Lore, Lava Window Aperture, Festival Court Steward & Guards ----
    m.events = [
        {'type': 'warp', 'name': 'South to Hall of Oaths (247) L', 'at': [12, 25], 'to': {'map': 247, 'x': 16, 'y': 6, 'dir': 'down'}, 'se': 'Door exit'},
        {'type': 'warp', 'name': 'South to Hall of Oaths (247)', 'at': [13, 25], 'to': {'map': 247, 'x': 16, 'y': 6, 'dir': 'down'}, 'se': 'Door exit'},
        {'type': 'warp', 'name': 'South to Hall of Oaths (247) R', 'at': [14, 25], 'to': {'map': 247, 'x': 16, 'y': 6, 'dir': 'down'}, 'se': 'Door exit'},
        _sign('The Ember Throne', (13, 7),
              "THE EMBER THRONE OF ASHKAAR — Carved of caldera basalt and inlaid with iron. The seat is empty: the Dominar holds court at the eastern capital, while the lava window burns unabated behind it."),
        _sign('Royal Oath-Brazier', (13, 15),
              "THE ROYAL OATH-BRAZIER — Before this fire Ashkaar names its Festival champions and seals its Dominion embassies. Its flame never drops below white-orange."),
        _sign('Lava Window Aperture', (13, 5),
              "Through the great obsidian aperture behind the dais, living magma rolls down the inner wall of Cindervault's caldera, bathing the entire throne room in warm amber light."),
        _make_npc('Lord-Steward Vaelen', (15, 9), 'NPC 25', 'down', [
            "Lord-Steward Vaelen: You stand before the Ember Throne, child of Elowen. The Dominar is presently at the capital, leaving Cindervault's seat kept in honour.",
            "Lord-Steward Vaelen: In calmer seasons, it is from this very floor that Ashkaar names its Festival delegation and sends its champions west beneath the gold dragon standard.",
        ]),
        _make_npc('Captain of the Throne Guard', (10, 15), 'trainer_ASHKAAR_OFFICER', 'right', [
            "Captain of the Throne Guard: Stand clear of the lava moats and speak plainly before the brazier.",
            "Captain of the Throne Guard: Lady Sigrun stood on these very tiles as a girl of eleven, arguing policy with her father while a Bagon chewed his cloak.",
        ]),
        _make_npc('Royal Oath-Guard', (16, 15), 'trainer_ASHKAAR_SOLDIER_F', 'left', [
            "Royal Oath-Guard: Even empty, the Ember Throne carries the weight of the Dragonfire Dominion.",
        ]),
        _make_npc('Dragon-Banner Herald', (10, 20), 'trainer_ASHKAAR_EMBER_RIDER', 'right', [
            "Dragon-Banner Herald: When the war drums sound on the Pyre Road, it is this standard that rides at the head of the column.",
        ]),
        _make_npc('Flame-Keeper', (16, 20), 'NPC 22', 'left', [
            "Flame-Keeper: The caldera window has been running hotter all month. Even the basalt behind the throne is humming.",
        ]),
        {'type': 'item', 'at': [6, 17], 'item': 'FIRESTONE', 'name': 'Ember Throne Fire Stone'},
    ]

    m.paint()
    # ---- 5. Sculpt True Volcanic Obsidian Caldera Lava Window Overlook (ZERO floating crimson wallpaper!) ----
    # Clear the 3-row cvH interior parlor wallpaper that plan_cliffs placed over y=1..3 so live PF Magma shines across y=2..4,
    # and cap y=0..1 with dark cut-basalt volcanic arch masonry (qy kit: pas=0xf)!
    for wx in range(9, 18):
        m.L[1, 0, wx] = 20202 if wx == 9 else (20205 if wx == 17 else (20204 if wx % 2 == 0 else 20203))
        m.L[2, 0, wx] = 0
        m.L[1, 1, wx] = 20206 if wx == 9 else (20209 if wx == 17 else (20208 if wx % 3 == 0 else 20207))
        m.L[2, 1, wx] = 0
        for wy in (2, 3, 4):
            m.L[1, wy, wx] = 0
            if not (wy == 4 and wx in (9, 17)):  # preserve flanking nr_col obsidian pillar capitals at (9,4) & (17,4)!
                m.L[2, wy, wx] = 0
    # Subtle volcanic steam plumes rising off the living caldera magma window
    for sx, sy, nm in ((10, 2, 'lm_steam0'), (16, 2, 'lm_steam1')):
        stL = STAMPS[nm]['layers']
        for dy in range(len(stL[2])):
            if stL[2][dy][0]:
                m.L[2, sy + dy, sx] = int(stL[2][dy][0])

    Lr = RC.resolve(m.L, TID).astype(np.int32)
    ev_pts = [tuple(e['at']) for e in m.events]
    PG.guard(Lr, TID, ev_pts, 'Map 246')
    assert not PG.hits(Lr, R.tilesets()[TID], ev_pts), 'Map 246 passguard hits!'
    m.L = Lr

    _verify_4bit_bfs(Lr, m.events, (13, 24), [
        ('South -> 247 Hall of Oaths', (13, 25), False),
        ('Empty Ember Throne', (13, 7), True),
        ('Lava Window Promenade (13,6)', (13, 6), False),
        ('Lava Window Aperture (13,5)', (13, 5), True),
        ('Royal Oath-Brazier', (13, 15), True),
        ('Lord-Steward Vaelen', (15, 9), True),
        ('Captain of Throne Guard', (10, 15), True),
        ('Fire Stone', (6, 17), True),
    ], 'Map 246 Pyre Keep - Ember Throne')

    head = {
        'id': 246,
        'name': 'Pyre Keep - Ember Throne',
        'parent': 245,
        'bgm': 'Lava Town',
        'field': 'DRAGONS_DEN',
        'map_audio': {'bgm': 'Theme - Accord', 'bgs': 'Lava - Ashkaar', 'bgs_volume': 35, 'rain': False},
        'metadata': {'Name': 'Pyre Keep', 'SnapEdges': True, 'MapPosition': CV_POS, 'BattleBack': 'cave1'},
        'tone': [24, 4, -18, 10],
        '_file': '246_pyre_keep_ember_throne.yaml',
    }
    m.write(246, head, comment='# GENERATED by mapgen/layouts/pyre_keep.py (Batch 3B): Pyre Keep - Ember Throne.\n'
                               '# Edit the layout script, not this file.\n')
    return m, Lr


# =================================================================================================
# MAP 248 — Pyre Keep - Dragon Roosts (36x24, TS 61 PF Rejuv Forge, Outdoor, DRAGONS_DEN)
# Exact arrival from 240_cindervault_forge.yaml: (12, 20) facing up!
# Live Trials hooks: ROOST_KEEPER (Tarn), OLD_CINDER (Charizard), plus Tamm (Trapinch) & Roost-Mistress!
# =================================================================================================
def build_248():
    W, H = 36, 24
    m = Cave(W, H, 'L', seed=248, pool='Magma', tid=TID)
    m.STAIRS = K.STAIRS_STONE
    m.kit = {MASS: 'cvL', TER2: 'cvL', TER: 'cvL', FLOOR: 'cvL', 'default': 'cvL'}

    # ---- 1. Sculpt Dramatic 3-Tier Volcanic Dragon Aerie Cantilevered Over a Sweeping Magma Lake! ----
    # Sweeping Eastern & South-Eastern Caldera Magma Lake (FLOOR=1 filled with PF Magma!)
    m.box(19, 14, 34, 22, FLOOR, 'w')
    m.box(29, 8, 34, 15, FLOOR, 'w')
    # Lower Aerie Landing (FLOOR=1, x=3..20, y=13..21) + West Skybridge to 245 (x=1..4, y=11..15)
    m.box(3, 13, 20, 21, FLOOR, '.')
    m.box(1, 10, 4, 15, FLOOR, '.')
    # South Stair Notch to 240 Forge Terraces (x=10..14, y=20..22 -> exact 240 arrival (12,20) up!)
    m.box(10, 20, 14, 22, FLOOR, '.')

    # Mid Hatchery & Harness Aerie Terrace (TER=2, x=4..29, y=8..13)
    m.box(4, 8, 29, 13, TER, '.')
    # NW Overlook Roost Spur (TER=2, x=4..12, y=3..8 — DRAGONGEM spur overlooking glowing NW lava pocket!)
    m.box(4, 3, 12, 8, TER, '.')
    m.box(13, 3, 19, 7, FLOOR, 'w')     # Dramatic volcanic caldera gorge between NW Spur & High Roost!

    # HIGH ROOST PROMONTORY (TER2=3, x=21..33, y=2..7 — Old Cinder's aerie crag jutting over the magma lake!)
    m.box(21, 2, 33, 7, TER2, '.')

    # Organic volcanic crag edges (ZERO boxy grid!)
    m.mass_at([
        (4, 3), (12, 3), (21, 2), (33, 2), (33, 7),
        (3, 20), (3, 21), (4, 21), (20, 20), (20, 21),
        (19, 22), (34, 22),
    ])

    # Grand Carved Basalt Aerie Staircases (TER2 -> TER -> FLOOR)
    m.stairs(12, 13, w=3, n=3, c='.')   # Lower Landing -> Mid Hatchery Terrace (x=12..14, y=13..15 -> lands y=16)
    m.stairs(24, 7, w=3, n=3, c='.')    # Mid Hatchery -> High Roost Crag (x=24..26, y=7..9 -> lands y=10)

    m.tidy()
    m.plan_cliffs(rows=3)

    # ---- 2. Ashkaar Wing-Harness Pavilion & Aerie Architecture (100% clear below y=13..15 TER cliff face!) ----
    _place_stamp_over(m, 'wr_tent_r', 5, 16, base_z=1, top_z=2, top_rows=1, solid=True)   # 3x3 -> x=5..7, y=16..18!
    _place_stamp_over(m, 'wr_rack', 8, 16, base_z=1, top_z=2, top_rows=1, solid=True)     # harness rack beside pavilion

    # ---- 3. Bidirectional Warps, Live Trials Hooks (Tarn & Old Cinder), Tamm, Roost-Mistress & Dragon Followers! ----
    E = m.events

    # South Return Warps -> 240 Cindervault - Forge Terraces (38, 3, down) [matches 240 -> 248 (12,20) up!]
    for rx in (11, 12, 13):
        E.append({
            'type': 'warp',
            'name': 'South to Forge Terraces (240)',
            'at': [rx, 21],
            'to': {'map': 240, 'x': 38, 'y': 3, 'dir': 'down'},
            'se': 'Door exit',
        })

    # West Rampart Skybridge -> 245 Pyre Keep - Rampart (30, 13, left)
    for wy in (12, 13, 14):
        E.append({
            'type': 'warp',
            'name': 'West Skybridge to Pyre Keep Rampart (245)',
            'at': [1, wy],
            'to': {'map': 245, 'x': 30, 'y': 13, 'dir': 'left'},
            'se': 'Door exit',
        })

    # LIVE TRIALS HOOK #1: Roost-Keeper Tarn (plugins/Prismfall Trials/152_Talk_Megas.rb:40 -> :ROOST_KEEPER!)
    tarn_ruby = (
        'if defined?(pf_trial_talk)\n'
        '  pf_trial_talk(:ROOST_KEEPER)\n'
        'else\n'
        '  pbMessage(_INTL("Roost-Keeper Tarn: Mind your step climbing up to the High Roost. Old Cinder\'s been coiled round his late rider\'s saddle since the last border march."))\n'
        'end'
    )
    E.append({
        'type': 'event',
        'name': 'Roost-Keeper Tarn',
        'at': [23, 11],
        'pages': [{
            'graphic': {'sprite': 'NPC 25', 'dir': 'down'},
            'trigger': 'action',
            'move': 'fixed',
            'commands': [{'script': tarn_ruby}],
        }],
    })

    # LIVE TRIALS HOOK #2: Old Cinder — Grieving War-Charizard on the High Roost! (:OLD_CINDER -> Charizardite X!)
    old_cinder_ruby = (
        'pbSEPlay("Cries/CHARIZARD", 95, 95)\n'
        'if (pf_trial_ready?(:OLD_CINDER) rescue false)\n'
        '  pf_trial_talk(:OLD_CINDER)\n'
        'else\n'
        '  pbMessage(_INTL("Old Cinder raises its scarred snout from an empty Ashkaar war-saddle and gazes out over the magma lake. Its tail-flame burns quiet and fierce."))\n'
        'end'
    )
    E.append({
        'type': 'event',
        'name': 'Old Cinder',
        'at': [29, 5],
        'pages': [{
            'graphic': {'sprite': 'Followers/CHARIZARD', 'dir': 'down'},
            'trigger': 'action',
            'move': 'fixed',
            'commands': [{'script': old_cinder_ruby}],
        }],
    })

    # Canonical Chapter 8 & Trials NPCs + Ashkaar Dragon/Fire Follower Pokémon!
    E += [
        # Recruit Tamm (AS_AFRAID_OF_HEIGHTS, story/29_SCRIPT_CH8.md:98-101!)
        _make_npc('Recruit Tamm', (16, 18), 'trainer_ASHKAAR_SOLDIER_M', 'left', [
            "Recruit Tamm: I'm a dragon-rider. They gave me a Trapinch until I'm ready.",
            "Recruit Tamm: I'm afraid of heights. They don't know. Don't tell them. ...I just told you. I can't lie. It's the law. It's awful.",
        ]),
        _make_follower("Tamm's Trapinch", (17, 18), 'TRAPINCH', 'left',
                       "Trapinch clicks its jaws cheerfully and tries to climb onto Tamm's boot, completely unfazed by the caldera drop."),
        # Roost-Mistress (AS_EGG_RUN, 120_Quests_Catalogue.rb:261!)
        _make_npc('Roost-Mistress', (16, 11), 'trainer_ASHKAAR_EMBER_RIDER', 'down', [
            "Roost-Mistress: Keep the draft off the warm nests! A dragon egg needs caldera heat every step of the way — if it chills over the Cinderhorn, it won't hatch.",
            "Roost-Mistress: Lady Sigrun flew out of these roosts at dawn on her Salamence. You could hear the wingbeats all the way down in the Slag Ward.",
        ]),
        _make_follower('Hatchery Axew', (18, 11), 'AXEW', 'down',
                       "Axew tests its small tusks gently against a warm basalt vent stone, chirping brightly!"),
        _make_follower('Perched Flygon', (20, 10), 'FLYGON', 'left',
                       "Flygon hums a soft, sand-song chord with its emerald wings, riding the warm updraft off the magma lake."),
        _make_follower('Roost Salamence', (9, 10), 'SALAMENCE', 'right',
                       "Salamence folds its crimson wings like twin sails and regards you with calm, amber eyes."),
        _make_follower('Roost Noibat', (14, 18), 'NOIBAT', 'up',
                       "Noibat flutters excitedly on a perch rail, ears twitching toward Recruit Tamm as if it knows his secret."),
        _make_follower('Young Bagon', (18, 16), 'BAGON', 'down',
                       "Bagon stares resolutely out over the magma chasm, dreaming of the day its wings finally sprout."),
        _sign('High Roost Cairn', (27, 5),
              "THE HIGH ROOST — Resting perch of Old Cinder, war-mount of the Ashkaar Legion. Leave the empty saddle untouched."),
        _sign('Roosts Signpost', (10, 19),
              "PYRE KEEP DRAGON ROOSTS — ← West Skybridge to Rampart (245) · ↑ Hatchery & High Roost · ↓ Forge Terraces (240)."),
        _sign('Harness Pavilion', (6, 18),
              "ASHKAAR WING-HARNESS PAVILION — Spare flight-goggles, flameproof riding gloves, and oiled leather dragon-saddles hang cleanly in rows."),
        {'type': 'item', 'at': [6, 5], 'item': 'DRAGONGEM', 'name': 'Roosts Dragon Gem'},
        {'type': 'item', 'at': [27, 11], 'item': 'MAXPOTION', 'name': 'Roosts Max Potion'},
    ]

    # Protect arrivals, warps, stairs, skybridge & NPCs
    m.keep_clear |= {
        (11, 20), (12, 20), (13, 20), (11, 21), (12, 21), (13, 21), (12, 19),
        (1, 12), (1, 13), (1, 14), (2, 12), (2, 13), (2, 14), (3, 13), (4, 13),
        (12, 12), (13, 12), (14, 12), (12, 16), (13, 16), (14, 16),
        (24, 6), (25, 6), (26, 6), (24, 10), (25, 10), (26, 10),
    }
    for e in E:
        ex, ey = e['at']
        m.keep_clear.add((ex, ey))
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            if m.inb(ex + dx, ey + dy):
                m.keep_clear.add((ex + dx, ey + dy))

    # ---- 4. Dramatic Aerie Beacons, Banners, Roost Nests, Volcanic Rocks & Glow ----
    # High Roost Promontory landmarks framing Old Cinder cleanly on flat TER2 stone (beacon pulled 1 tile off cliff!)
    _place_stamp_over(m, 'pf_beacon', 31, 4, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'wr_ban_ash', 22, 3, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'wr_ban_ash', 25, 3, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'fw_brazier', 27, 3, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'fw_brazier', 30, 3, base_z=1, top_z=2, top_rows=1, solid=True)
    # Real solid basalt High Roost Cairn at (27, 5) (pas=0xf!) + empty war-saddle harness pack beside Old Cinder!
    _place_stamp_over(m, 'E_rock0', 27, 5, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'wr_sacks', 30, 6, base_z=1, top_z=1, top_rows=0, solid=True)

    # Mid Hatchery Aerie & NW Dragon-Gem Spur props (beacon pulled 1 tile clear of north cliff!)
    _place_stamp_over(m, 'fw_brazier', 11, 10, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'fw_brazier', 22, 10, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'wr_ban_ash', 5, 9, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'wr_ban_ash', 28, 9, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'wr_sacks', 15, 9, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'wr_rack', 7, 10, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'pf_beacon', 9, 5, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'E_rock0', 5, 7, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'E_rock1', 11, 6, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'pf_whalebone', 7, 7, base_z=1, top_z=2, top_rows=1, solid=True)

    # Lower Landing props: REAL solid pf_signpost at (10, 18..19) + symmetric flanking south braziers (9,19) & (15,19)!
    _place_stamp_over(m, 'pf_signpost', 10, 18, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'fw_brazier', 9, 19, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'fw_brazier', 15, 19, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'wr_ban_ash', 4, 11, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'hb_barrels', 9, 16, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'pf_stonebench', 5, 20, base_z=1, top_z=1, top_rows=0, solid=True)

    # Volcanic updraft steam plumes over magma + mirror-symmetric amber fire halos!
    for sx, sy in ((22, 17), (27, 19), (31, 14), (32, 10), (16, 5), (24, 15)):
        _place_stamp_over(m, 'lm_steam0' if (sx + sy) % 2 == 0 else 'lm_steam1', sx, sy, base_z=2, top_z=2, top_rows=2, solid=False)
    for gx, gy in ((31, 4), (27, 3), (29, 3), (9, 5), (11, 10), (21, 10), (9, 19), (14, 19)):
        m.stamps.append(('pf_glow', gx, gy))

    m.paint()

    # ---- 5. Aerie Basalt, Ochre Landing Pads & West Skybridge Iron Grate ----
    low_ids = [P1('lm_low%d' % i) for i in range(4)]
    slate_ids = [P1('T_f%d' % i) for i in range(4)]
    earth_ids = [P1('E_f%d' % i) for i in range(4)]
    qf0, qf1 = P1('Q_f0'), P1('Q_f1')
    grate = P1('lm_grate')
    fp = {P1(k) for k in STAMPS if k.startswith(('L_floorpatch_', 'L_fd'))}

    _paint_path_rect(m, 4, 16, 19, 20, low_ids, fp)
    _paint_path_rect(m, 10, 16, 14, 22, earth_ids, fp)
    for bx, by in ((9, 19), (9, 20), (15, 19), (15, 20)):
        if m.cls[by, bx] == '.' and not m.cliff[by, bx]:
            m.L[0, by, bx] = low_ids[(bx * 3 + by * 5) % len(low_ids)]
    _paint_path_rect(m, 6, 9, 28, 12, slate_ids, fp)
    _paint_path_rect(m, 5, 4, 11, 9, earth_ids, fp)
    _paint_path_rect(m, 23, 3, 32, 7, slate_ids, fp)
    _paint_path_rect(m, 27, 4, 31, 6, earth_ids, fp)
    # West Iron-Grate Skybridge connecting smoothly to 245 Rampart!
    for y in (12, 13, 14):
        for x in (1, 2, 3):
            if m.cls[y, x] == '.' and not m.cliff[y, x]:
                m.L[0, y, x] = qf0 if (x + y) % 2 == 0 else qf1
                m.L[1, y, x] = grate

    Lr = RC.resolve(m.L, TID).astype(np.int32)
    ev_pts = [tuple(e['at']) for e in E]
    PG.guard(Lr, TID, ev_pts, 'Map 248')
    assert not PG.hits(Lr, R.tilesets()[TID], ev_pts), 'Map 248 passguard hits!'
    m.L = Lr

    _verify_4bit_bfs(Lr, E, (12, 20), [
        ('South -> 240 Forge Terraces', (12, 21), False),
        ('West Skybridge -> 245 Rampart', (1, 13), False),
        ('Recruit Tamm', (16, 18), True),
        ('Roost-Mistress', (16, 11), True),
        ('Roost-Keeper Tarn', (23, 11), True),
        ('Old Cinder (High Roost)', (29, 5), True),
        ('High Roost Cairn', (27, 5), True),
        ('Roosts Signpost', (10, 19), True),
        ('Harness Pavilion', (6, 18), True),
        ('Dragon Gem (NW Spur)', (6, 5), True),
        ('Max Potion', (27, 11), True),
    ], 'Map 248 Pyre Keep - Dragon Roosts')

    head = {
        'id': 248,
        'name': 'Pyre Keep - Dragon Roosts',
        'parent': 245,
        'bgm': 'Lava Town',
        'field': 'DRAGONS_DEN',
        'map_audio': {'bgm': 'Town - Ashkaar', 'bgs': 'Lava - Ashkaar', 'bgs_volume': 60, 'rain': False},
        'metadata': {'Name': 'Pyre Keep - Dragon Roosts', 'Outdoor': True, 'ShowArea': True, 'MapPosition': CV_POS, 'BattleBack': 'cave1'},
        'tone': [24, 4, -14, 8],
        'fog': {'name': 'prismfall_cave', 'opacity': 18, 'blend': 1, 'zoom': 100, 'sx': 1, 'sy': 0},
        '_file': '248_pyre_keep_dragon_roosts.yaml',
    }
    m.write(248, head, comment='# GENERATED by mapgen/layouts/pyre_keep.py (Batch 3B): Pyre Keep - Dragon Roosts.\n'
                               '# Edit the layout script, not this file.\n')
    return m, Lr


# =================================================================================================
# MAP 254 — Pyre Keep - Ancestor Crypts (33x29, TS 61 PF Rejuv Forge, Dungeon, HOLLOW_CATHEDRAL)
# Canonical PBS Trainer: [CHANNELER, Thessaly] (pbs/trainers.txt:15682 — 0 duplicates!)
# =================================================================================================
def build_254():
    W, H = 33, 29
    m = Cave(W, H, 'L', seed=254, pool='Magma', tid=TID)
    m.STAIRS = K.STAIRS_STONE
    K.KITS['cvL2'] = dict(K.KITS['cvL'], rows=[K.KITS['cvL']['rows'][0], K.KITS['cvL']['rows'][2]])
    m.kit = {TER: 'cvL2', FLOOR: 'cvL2', MASS: 'cvL2', 'default': 'cvL2'}

    # ---- 1. Sculpt Solemn Obsidian Cathedral-Ossuary Beneath Pyre Keep ----
    # North Elevated Sanctum of the First Dominar (TER=2, x=11..21, y=3..9 — stair down y=9..10!)
    m.box(11, 3, 21, 9, TER, '.')
    # Central Nave of the Eternal Flame (FLOOR=1, x=10..22, y=10..22)
    m.box(10, 10, 22, 22, FLOOR, '.')
    # West Sarcophagus Cloister (FLOOR=1, x=3..10, y=9..21 — [CHANNELER, Thessaly] & SPELLTAG!)
    m.box(3, 9, 10, 21, FLOOR, '.')
    # East Dragon-Rider Ossuary (FLOOR=1, x=22..29, y=9..21 — LITWICK flame-tender & DUSKBALL!)
    m.box(22, 9, 29, 21, FLOOR, '.')
    # South Crypt Entry Narthex (FLOOR=1, x=12..20, y=22..27 — arrival (16,26) & warps (15..17,27)!)
    m.box(12, 22, 20, 27, FLOOR, '.')

    # Sculpted catacomb rock piers & chamfers (ZERO boxy rectangle!)
    m.mass_at([
        (11, 3), (21, 3), (3, 9), (4, 9), (3, 20), (3, 21), (4, 21),
        (28, 9), (29, 9), (29, 20), (29, 21), (28, 21),
        (12, 26), (12, 27), (20, 26), (20, 27),
        (3, 15), (29, 15),
    ])

    # Twin Subterranean Glowing Magma River Trenches flanking the Central Nave (x=10..11 & x=21..22, y=12..20)
    # Bridged across y=15..16 by riveted iron-grate bridges into the West & East Crypt Cloisters!
    for my in range(12, 21):
        for mx in (10, 11, 21, 22):
            m.cls[my, mx] = 'w'

    # Central 3-Wide Carved Basalt Staircase ascending to the First Dominar's Sanctum (y=9..10 -> lands y=11!)
    m.stairs(15, 9, w=3, n=2, c='.')

    m.tidy()
    m.plan_cliffs(rows=2)

    # Iron-grate crypt bridges cleanly spanning both subterranean magma trenches (y=15..16)!
    crypt_bridges = [(x, y) for y in (15, 16) for x in (10, 11, 21, 22)]
    for bx, by in crypt_bridges:
        m.cls[by, bx] = '.'
        m.keep_clear.add((bx, by))

    # ---- 2. Events: Return Warp -> 247, PBS Trainer Thessaly, Crypt Keeper, Litwick, Epitaphs & Pickups ----
    E = m.events

    # South Return Warps -> 247 Pyre Keep - Hall of Oaths West Crypt Arch (4, 12, right)
    for rx in (15, 16, 17):
        E.append({
            'type': 'warp',
            'name': 'Up to Hall of Oaths (247)',
            'at': [rx, 27],
            'to': {'map': 247, 'x': 4, 'y': 12, 'dir': 'right'},
            'se': 'Door exit',
        })

    # Canonical PBS Trainer for Map 254: [CHANNELER, Thessaly] (pbs/trainers.txt:15682 — 0 duplicates!)
    E.append({
        'type': 'trainer',
        'name': 'Trainer(3)',
        'at': [7, 15],
        'sight': 3,
        'dir': 'right',
        'sprite': 'trainer_CHANNELER',
        'trainer': ['CHANNELER', 'Thessaly'],
        'intro': "Channeler Thessaly: Three centuries of House Ashfall watch from these basalt niches! Prove you belong in their quiet!",
        'after': "Channeler Thessaly: The Ashfall dead are proud. You've embarrassed several.",
        'rules': ['setBattleRule("field", :HOLLOW_CATHEDRAL)'],
    })

    E += [
        _make_npc('Crypt Keeper', (14, 24), 'NPC 28', 'right', [
            "Crypt Keeper: Ashfall dead lie in basalt niches along both cloisters — rulers to the west, their dragon-riders to the east.",
            "Crypt Keeper: The subterranean magma keeps the stone dry and warm. We never bury our dead in cold earth.",
        ]),
        _make_follower('Crypt Litwick', (26, 16), 'LITWICK', 'left',
                       "A quiet Litwick hovers beside an ash-urn plinth, its violet flame bowing politely like a candle in no wind."),
        _sign('First Dominar Sarcophagus', (16, 6),
              "FIRST DOMINAR OF ASHKAAR — 'I took no crown the fire would not weigh. Stand straight before the mountain, or do not stand at all.'"),
        _sign('West Cloister Epitaph', (6, 12),
              "BASALT NICHE OF DOMINAR VEYRA ASHFALL (AF 112–179) — 'She built the Rampart and swore the first Law of Plain Speech.'"),
        _sign('East Ossuary Epitaph', (26, 12),
              "RIDER NICHE OF CAPTAIN TOREN — 'His Salamence circled Cindervault seven nights after the pass closed, then folded its wings beside this door.'"),
        {'type': 'item', 'at': [5, 11], 'item': 'SPELLTAG', 'name': 'Ancestor Crypts Spell Tag'},
        {'type': 'item', 'at': [27, 11], 'item': 'DUSKBALL', 'name': 'Ancestor Crypts Dusk Ball'},
        {'type': 'item', 'at': [19, 7], 'item': 'STARPIECE', 'name': 'Sanctum Star Piece'},
    ]

    m.keep_clear |= {
        (15, 26), (16, 26), (17, 26), (15, 27), (16, 27), (17, 27), (16, 25),
        (15, 9), (16, 9), (17, 9), (15, 10), (16, 10), (17, 10), (15, 11), (16, 11), (17, 11),
        (16, 7), (16, 8), (15, 7), (17, 7),
        (9, 15), (9, 16), (12, 15), (12, 16), (20, 15), (20, 16), (23, 15), (23, 16),
    }
    for e in E:
        ex, ey = e['at']
        m.keep_clear.add((ex, ey))
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            if m.inb(ex + dx, ey + dy):
                m.keep_clear.add((ex + dx, ey + dy))

    # ---- 3. Solemn Basalt Sarcophagi, Ash-Urn Plinths, Obsidian Columns, Mourning Banners & Eternal Flames ----
    # North Sanctum of the First Dominar (TER): solemn Ashkaar obsidian monolith stele + twin sarcophagi + candelabras!
    _place_stamp_over(m, 'pf_roadstone', 16, 5, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'mn_grave_l', 15, 6, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'mn_grave_r', 17, 6, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'mn_candelabra', 14, 5, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'mn_candelabra', 18, 5, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'mn_statue', 13, 5, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'mn_statue', 19, 5, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'fw_brazier', 12, 7, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'fw_brazier', 20, 7, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'wr_ban_ash_t', 12, 4, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'wr_ban_ash_t', 20, 4, base_z=1, top_z=2, top_rows=2, solid=True)

    # Central Nave Obsidian Colonnade & Eternal Flames
    for cx in (13, 19):
        for cy in (12, 18, 22):
            _place_stamp_over(m, 'nr_col', cx, cy, base_z=1, top_z=2, top_rows=1, solid=True)
    for bx, by in ((14, 14), (18, 14), (14, 20), (18, 20), (14, 26), (18, 26)):
        _place_stamp_over(m, 'fw_brazier', bx, by, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'wr_ban_ash_t', 13, 24, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'wr_ban_ash_t', 19, 24, base_z=1, top_z=2, top_rows=2, solid=True)

    # West Sarcophagus Cloister (Basalt Graves, Ash-Urn Plinths & Candelabras!)
    for gy in (12, 18):
        _place_stamp_over(m, 'mn_grave_l', 5, gy, base_z=1, top_z=1, top_rows=0, solid=True)
        _place_stamp_over(m, 'mn_grave_r', 6, gy, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'mn_plinth', 8, 11, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'mn_plinth', 8, 19, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'mn_candelabra', 4, 13, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'mn_candelabra', 4, 18, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'mn_statue', 8, 13, base_z=1, top_z=2, top_rows=1, solid=True)

    # East Dragon-Rider Ossuary (Armour Vigils, Urn Plinths, Dragon Bones & Braziers!)
    for gy in (12, 18):
        _place_stamp_over(m, 'mn_grave_l', 26, gy, base_z=1, top_z=1, top_rows=0, solid=True)
        _place_stamp_over(m, 'mn_grave_r', 27, gy, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'mn_armour', 24, 11, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'mn_armour', 24, 19, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'mn_plinth', 25, 16, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'pf_whalebone', 28, 13, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'pf_whalebone', 28, 17, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'fw_brazier', 24, 13, base_z=1, top_z=2, top_rows=1, solid=True)

    # Dramatic Crypt Light Shafts, Subtle Magma Steam & Mirror-Symmetric Eternal Flame Glow Halos!
    for sx, sy in ((15, 5), (15, 15), (6, 14), (25, 14)):
        m.stamps.append(('cv_shaft', sx, sy))
    for sx, sy in ((10, 13), (21, 13), (10, 19), (21, 19)):
        _place_stamp_over(m, 'lm_steam0' if (sx + sy) % 2 == 0 else 'lm_steam1', sx, sy, base_z=2, top_z=2, top_rows=2, solid=False)
    for gx, gy in ((12, 7), (19, 7), (14, 14), (17, 14), (14, 20), (17, 20), (14, 26), (17, 26)):
        m.stamps.append(('pf_glow', gx, gy))

    m.paint()

    # ---- 4. Solemn Volcanic Basalt/Ashlar Crypt Paving, Mourning Runner, South Ascent Stairs & Trench Bridges ----
    slate_ids = [P1('T_f%d' % i) for i in range(4)]
    low_ids = [P1('lm_low%d' % i) for i in range(4)]
    basalt_ids = [P1('L_f%d' % i) for i in range(4)]
    qf0, qf1 = P1('Q_f0'), P1('Q_f1')
    grate = P1('lm_grate')
    fp = {P1(k) for k in STAMPS if k.startswith(('L_floorpatch_', 'L_fd'))}

    # Clear stray asymmetric cave gravel speckles across the dressed stone crypt interior
    for cy in range(3, H - 1):
        for cx in range(3, W - 1):
            if int(m.L[1, cy, cx]) in fp:
                m.L[1, cy, cx] = 0

    _paint_path_rect(m, 12, 4, 20, 9, slate_ids, fp)
    _paint_path_rect(m, 12, 11, 20, 27, slate_ids, fp)
    _paint_path_rect(m, 4, 10, 9, 20, low_ids, fp)
    _paint_path_rect(m, 23, 10, 28, 20, low_ids, fp)
    _paint_path_rect(m, 5, 13, 8, 17, basalt_ids, fp)
    _paint_path_rect(m, 24, 13, 27, 17, basalt_ids, fp)
    _paint_path_rect(m, 13, 22, 19, 27, low_ids, fp)

    # Crimson-charcoal ceremonial nave carpet runner (x=15..17, y=11..26)
    for y in range(11, 27):
        for x in (15, 16, 17):
            if m.cls[y, x] == '.' and not m.cliff[y, x] and m.L[1, y, x] == 0:
                part = ('n' if y == 11 else 's' if y == 26 else '') + ('w' if x == 15 else 'e' if x == 17 else '')
                m.L[1, y, x] = P1('mn_rugR_' + (part or ('c2' if y % 4 == 0 else 'c')))

    # 3-wide Stone Ascent Stairs at South Exit (15..17, 27) ascending back up to 247 Hall of Oaths!
    for i, sx in enumerate((15, 16, 17)):
        m.L[1, 27, sx] = K.STAIRS_STONE[i]

    # Riveted Iron-Grate Bridges across both subterranean magma trenches (y=15..16)
    for bx, by in crypt_bridges:
        m.L[0, by, bx] = qf0 if (bx + by) % 2 == 0 else qf1
        m.L[1, by, bx] = grate

    Lr = RC.resolve(m.L, TID).astype(np.int32)
    ev_pts = [tuple(e['at']) for e in E]
    PG.guard(Lr, TID, ev_pts, 'Map 254')
    assert not PG.hits(Lr, R.tilesets()[TID], ev_pts), 'Map 254 passguard hits!'
    m.L = Lr

    _verify_4bit_bfs(Lr, E, (16, 26), [
        ('South Return -> 247 Hall of Oaths', (16, 27), False),
        ('Crypt Keeper', (14, 24), True),
        ('Trainer Thessaly (West Cloister)', (7, 15), True),
        ('Spell Tag (West)', (5, 11), True),
        ('Crypt Litwick (East)', (26, 16), True),
        ('Dusk Ball (East)', (27, 11), True),
        ('First Dominar Sarcophagus (North TER)', (16, 6), True),
        ('Sanctum Star Piece', (19, 7), True),
    ], 'Map 254 Pyre Keep - Ancestor Crypts')

    head = {
        'id': 254,
        'name': 'Pyre Keep - Ancestor Crypts',
        'parent': 245,
        'bgm': 'Cave',
        'field': 'HOLLOW_CATHEDRAL',
        'map_audio': {'bgm': 'Dungeon - Cave', 'bgs': 'Lava - Ashkaar', 'bgs_volume': 40, 'rain': False},
        'metadata': {'Name': 'Pyre Keep - Ancestor Crypts', 'SnapEdges': True, 'ShowArea': True, 'MapPosition': CV_POS, 'BattleBack': 'cave1'},
        'tone': [-14, -18, -22, 18],
        'fog': {'name': 'prismfall_cave', 'opacity': 26, 'blend': 1, 'zoom': 100, 'sx': 1, 'sy': 0},
        '_file': '254_pyre_keep_ancestor_crypts.yaml',
    }
    m.write(254, head, comment='# GENERATED by mapgen/layouts/pyre_keep.py (Batch 3B): Pyre Keep - Ancestor Crypts.\n'
                               '# Edit the layout script, not this file.\n')
    return m, Lr


def main():
    build_245()
    build_247()
    build_246()
    build_248()
    build_254()
    print('Done: wrote Pyre Keep specs & raw maps (245, 246, 247, 248, 254).')


if __name__ == '__main__':
    main()
