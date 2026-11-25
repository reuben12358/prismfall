#!/usr/bin/env python3
"""layouts/verdance_palace.py - Wave 5 Rejuvenation V14 redesign of the 3 Verdance landmark interiors:
  - 286 Briar Hall - Great Hall          (33x25, Tileset 59 PF Rejuv Manor)
  - 287 Briar Hall - Throne Room         (27x27, Tileset 59 PF Rejuv Manor)
  - 295 Cathedral of the Evergreen       (31x29, Tileset 60 PF Rejuv Lumen)

Replaces the bare bleached white-grey outdoor-tileset boxes with distinct, void-sculpted Rejuvenation V14
architectural showpieces featuring elevated TER daises, grand staircases, colonnades, stained-glass sunbeams,
chandeliers, glowing braziers, and living evergreen / white-lily sanctuary chapels — while preserving 100%
of exact HEAD events, NPCs, dialogues, and warp/exit links.
"""
import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)

from cavekit import Cave, FLOOR, TER, MASS, P1
import cavekit as CK
import passguard as PG
from manor import Manor


class Palace(Manor):
    """Extended Manor builder supporting custom tileset IDs (59/60), ivory marble/inlay flooring,
    royal crimson runners, marble/stone/crimson staircases, and strict passguard enforcement."""

    def __init__(self, W, H, seed, tid=59, pool='Cave Pool'):
        Cave.__init__(self, W, H, 'F', seed, pool=pool, tid=tid)
        self.kit = {'default': 'cvF', TER: 'cvB'}
        self.STAIRS = tuple(P1('mn_stair_' + k) for k in 'lmr')
        self.rooms = []
        self.late = []
        self.floor_overrides = []   # (x0, y0, x1, y1, kind) applied cleanly on layer 0 after reskin
        self.inlay_boxes = []       # (x0, y0, x1, y1) gold-cyan inlaid marble border rectangles

    def marble_floor(self, x0, y0, x1, y1, style='plaza'):
        self.floor_overrides.append((x0, y0, x1, y1, style))

    def marble_inlay(self, x0, y0, x1, y1):
        self.inlay_boxes.append((x0, y0, x1, y1))

    def runner(self, x0, y0, x1, y1):
        """Royal crimson-and-gold Lumen runner carpet (lm_carpet_*) on layer 1."""
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                part = ('n' if y == y0 else 's' if y == y1 else '') + ('w' if x == x0 else 'e' if x == x1 else '')
                self.late.append((1, x, y, P1('lm_carpet_' + (part or 'c'))))

    def on_layer(self, name, x, y, z):
        """Force all non-zero tiles of a stamp onto layer z."""
        L = CK.STAMPS[name]['layers']
        for dy in range(len(L[0])):
            for dx in range(len(L[0][0])):
                t = next((int(L[zz][dy][dx]) for zz in (2, 1, 0) if L[zz][dy][dx]), 0)
                if t:
                    self.late.append((z, x + dx, y + dy, t))

    def _apply_custom_floors(self):
        L = self.L
        plaza = [P1('lm_plaza0'), P1('lm_plaza1')]
        pave = [P1('lm_pave%d' % i) for i in range(8)]
        for x0, y0, x1, y1, style in self.floor_overrides:
            for y in range(max(0, y0), min(self.H, y1 + 1)):
                for x in range(max(0, x0), min(self.W, x1 + 1)):
                    if self.cls[y, x] != '.' or self.cliff[y, x]:
                        continue
                    if style == 'plaza':
                        L[0, y, x] = plaza[(x + y) % 2]
                    elif style == 'pave':
                        L[0, y, x] = pave[(x * 7 + y * 11) % len(pave)]
                    elif style == 'walnut':
                        L[0, y, x] = P1('H_f%d' % ((x + y) % 2))
                    elif style == 'oak':
                        L[0, y, x] = P1('A_f%d' % ((x + y) % 2))
                    elif style == 'mahogany':
                        L[0, y, x] = P1('N_f%d' % ((x + y) % 2))
        for x0, y0, x1, y1 in self.inlay_boxes:
            for y in range(y0, y1 + 1):
                for x in range(x0, x1 + 1):
                    if not (0 <= x < self.W and 0 <= y < self.H):
                        continue
                    if self.cls[y, x] != '.' or self.cliff[y, x]:
                        continue
                    on_t, on_b = (y == y0), (y == y1)
                    on_l, on_r = (x == x0), (x == x1)
                    if not (on_t or on_b or on_l or on_r):
                        continue
                    if on_t and on_l: k = 'nw'
                    elif on_t and on_r: k = 'ne'
                    elif on_b and on_l: k = 'sw'
                    elif on_b and on_r: k = 'se'
                    elif on_t or on_b: k = 'h'
                    else: k = 'v'
                    L[0, y, x] = P1('lm_inlay_' + k)

    def paint(self):
        self.floor_ids = {P1('F_f%d' % v) for v in range(4)}
        Cave.paint(self)
        self.reskin()
        self._apply_custom_floors()

        carpets = {P1('mn_rug%s_%s' % (k, p)) for k in 'RBG' for p in ('nw', 'n', 'ne', 'w', 'c', 'e', 'sw', 's', 'se', 'c2')}
        carpets |= {P1('lm_carpet_' + p) for p in ('nw', 'n', 'ne', 'w', 'c', 'e', 'sw', 's', 'se')}
        stair_set = set(self.STAIRS)

        for z, x, y, t in self.late:
            if not (0 <= x < self.W and 0 <= y < self.H):
                continue
            # Never overwrite stair tiles on layer 2 with floor carpets/furniture
            if int(self.L[2, y, x]) in stair_set and z == 2 and t not in stair_set:
                continue
            if z == 1 and int(self.L[1, y, x]) in carpets and t not in carpets and not int(self.L[2, y, x]):
                z = 2
            self.L[z, y, x] = t

        # Re-assert stair tiles cleanly on top of carpets/floors so stairs always read crisp & walkable
        self.paint_stairs()

        # Passguard safety sweep: ensure ZERO solid-under-walkable passability bugs!
        PG.guard(self.L, self.tid)
        return self.L


# ================================================================================================ 286 Briar Hall - Great Hall
def build_286():
    W, H = 33, 25
    m = Palace(W, H, seed=286, tid=59)
    m.STAIRS = tuple(P1('mn_stair_' + k) for k in 'lmr')
    R = m.room_box

    # ---- 1. Void-sculpted buttressed cathedral-palace silhouette
    # Elevated Northern Royal Vestibule (TER): y=4..10 (wall lip y=3, face y=4, base y=5, open marble landing y=6..9!)
    R(11, 4, 21, 10, TER, 'Y', 'H')
    # Central Grand Banquet Nave (FLOOR): y=11..22
    R(11, 11, 21, 22, FLOOR, 'H', 'H')
    # West & East Buttressed Banquet Wings (FLOOR): y=9..21 (north wall lip y=8, face y=9, base y=10, open floor y=11..21!)
    R(3, 9, 11, 21, FLOOR, 'H', 'H')
    R(21, 9, 29, 21, FLOOR, 'H', 'H')
    # Narrowed monumental Southern Entry Portal framing warps (15..17, 23)
    m.box(13, 22, 19, 23, FLOOR)

    # Carve architectural gothic buttress recesses & corner chamfers into black void (ZERO boxy rectangle!)
    m.mass_at([
        # Outer banquet wing corner chamfers (NW, SW, NE, SE)
        (3, 9), (4, 9), (3, 10), (3, 20), (3, 21), (4, 21),
        (28, 9), (29, 9), (29, 10), (29, 20), (29, 21), (28, 21),
        # Mid-wing stone buttress notches along West (x=3) and East (x=29) walls
        (3, 15), (29, 15),
        # Royal Vestibule upper shoulders
        (11, 4), (21, 4),
    ])

    # Grand 5-wide Crimson-Carpeted Palace Staircase descending from Royal Vestibule (y=10..12)
    m.stairs(14, 10, w=5, n=3, c='.')
    m.plan_cliffs(rows=3)

    # ---- 2. Rich Multi-Zone Floor Craft (Warm Walnut Parquet + Ivory Marble + Gold Inlays + Crimson Runner)
    # Elevated Royal Vestibule: warm ivory marble framed by a gold-cyan geometric inlay border!
    m.marble_floor(11, 6, 21, 9, 'plaza')
    m.marble_inlay(12, 6, 20, 9)
    # Central Processional Nave: ivory marble aisle with inlaid gold borders
    m.marble_floor(12, 13, 20, 22, 'plaza')
    m.marble_inlay(12, 13, 20, 21)
    # Southern Entry Vestibule marble threshold
    m.marble_floor(13, 22, 19, 23, 'plaza')

    # Sweeping Royal Crimson-and-Gold Grand Carpet Runner from South Entry (y=23) up to the Throne Portal (y=6)!
    m.runner(15, 13, 17, 23)
    m.runner(15, 6, 17, 9)
    # Ornate Medallion Crimson Rugs framing the West & East Banquet Dining Bays
    # (Skip cells directly under the opaque white banquet tables so plates/candelabras layer cleanly on z=2!)
    m.rug('R', 5, 13, 10, 19, medallion=True)
    m.rug('R', 22, 13, 27, 19, medallion=True)
    table_cells = {(x, y) for x in (6, 7, 8, 24, 25, 26) for y in range(14, 19)}
    m.late = [(z, x, y, t) for (z, x, y, t) in m.late if not (z == 1 and (x, y) in table_cells)]

    # ---- 3. Architectural Walls: Throne Portal, Tall Gothic Windows, Evergreen Banners & Hearths
    # Rich carved Gothic Mahogany Palace Double-Door (mn_door) set into north wall base (16, 5),
    # leaving (16, 6) open crimson carpet for the warp to 287 Throne Room!
    m.late.append((1, 16, 5, P1('mn_door')))
    m.late.append((1, 15, 5, P1('mn_sconce')))
    m.late.append((1, 17, 5, P1('mn_sconce')))
    # Crimson-draped Gothic palace windows on North Vestibule wall & Banquet Wing walls
    for wx, wy in ((13, 4), (19, 4), (6, 9), (9, 9), (23, 9), (26, 9)):
        m.on('mn_window', wx, wy)
    # Royal Evergreen & Crimson-Gold Banners along the palace walls
    for bx, by in ((14, 4), (18, 4), (5, 9), (10, 9), (22, 9), (27, 9)):
        m.on('fw_ban_e', bx, by)
    # Twin Suits of Thorn Guard Armour flanking the Throne Room Portal on the Vestibule dais!
    m.on('mn_armour', 13, 6)
    m.on('mn_armour', 19, 6)
    # Warm standing golden candelabras framing the Vestibule stairhead & corners
    for cx, cy in ((12, 7), (20, 7), (14, 21), (18, 21)):
        m.on('mn_candelabra', cx, cy)
    # Potted palace palms accenting the Royal Vestibule
    m.on('mn_palm', 11, 7)
    m.on('mn_palm', 21, 7)

    # ---- 4. Monumental Marble Colonnade Pillars framing the Central Nave (replacing old tiny shrubs!)
    # Using nr_col (1x2: p0/r2 overhead top, p15/r0 solid base) so players walk freely behind column capitals!
    for x in (12, 20):
        for y in (13, 16, 19):
            m.on('nr_col', x, y)
    # Flaming ceremonial braziers flanking the southern entry foyer & mid-nave
    for bx, by in ((13, 21), (19, 21)):
        m.on('fw_brazier', bx, by)

    # ---- 5. Sumptuous Royal Banquet Tables, Velvet Chairs, Sideboards & Hearths
    # NOTE: Courtier stands at (9, 12) facing right — keep (9, 12) and full promenade (y=11..12) wide open!
    # West Banquet Long Table (x=6..8, y=14..18) on z=1 with gold candelabras & porcelain plates composited on z=2!
    m.table(6, 14, 8, 18)
    m.late.append((2, 7, 15, P1('mn_dt_cand')))
    m.late.append((2, 7, 17, P1('mn_dt_cand')))
    m.late.append((2, 6, 14, P1('mn_dt_plate')))
    m.late.append((2, 8, 14, P1('mn_dt_plate')))
    m.late.append((2, 6, 16, P1('mn_dt_plate')))
    m.late.append((2, 8, 16, P1('mn_dt_plate')))
    m.late.append((2, 6, 18, P1('mn_dt_plate')))
    m.late.append((2, 8, 18, P1('mn_dt_plate')))
    for cy in (14, 16, 18):
        m.on('mn_chairR_right', 5, cy)
        m.on('mn_chairR_left', 9, cy)
    # West Wing side decor: glowing hearth, sideboard, harp, candelabra & greenery tucked cleanly into alcoves
    m.on('mn_fire_lit', 6, 10)
    m.on('mn_sideboard2', 4, 11)
    m.on('mn_harp', 4, 18)
    m.on('mn_candelabra', 4, 13)
    m.on('mn_palm', 5, 20)
    m.on('lm_planter', 7, 20)

    # East Banquet Long Table (x=24..26, y=14..18) mirroring the West Banquet Hall
    m.table(24, 14, 26, 18)
    m.late.append((2, 25, 15, P1('mn_dt_cand')))
    m.late.append((2, 25, 17, P1('mn_dt_cand')))
    m.late.append((2, 24, 14, P1('mn_dt_plate')))
    m.late.append((2, 26, 14, P1('mn_dt_plate')))
    m.late.append((2, 24, 16, P1('mn_dt_plate')))
    m.late.append((2, 26, 16, P1('mn_dt_plate')))
    m.late.append((2, 24, 18, P1('mn_dt_plate')))
    m.late.append((2, 26, 18, P1('mn_dt_plate')))
    for cy in (14, 16, 18):
        m.on('mn_chairR_right', 23, cy)
        m.on('mn_chairR_left', 27, cy)
    # East Wing side decor: glowing hearth, china display cabinet, noble bust & greenery
    m.on('mn_fire_lit', 24, 10)
    m.on('mn_china', 27, 11)
    m.on('mn_bust', 28, 18)
    m.on('mn_candelabra', 28, 13)
    m.on('mn_palm', 27, 20)
    m.on('lm_planter', 24, 20)

    # ---- 6. Overhead Chandeliers, Stained-Glass Sunbeams (cv_shaft) & Candlelight Glows (pf_glow)
    for cx, cy in ((15, 7), (15, 14), (15, 19)):
        m.stamps.append(('mn_chandelier', cx, cy))
    for sx, sy in ((13, 6), (19, 6), (6, 11), (9, 11), (23, 11), (26, 11)):
        m.stamps.append(('cv_shaft', sx, sy))
    for gx, gy in ((16, 7), (16, 15), (16, 20), (7, 15), (25, 15), (7, 11), (25, 11), (13, 21), (19, 21)):
        m.stamps.append(('pf_glow', gx, gy))

    # ---- 7. Exact HEAD Events & Warps (6/6 preserved!)
    m.events = [
        {'type': 'npc', 'name': 'Steward', 'at': [18, 9], 'sprite': 'NPC 12', 'dir': 'down',
         'text': 'Steward: The throne room lies beyond the arch. Speak when spoken to. [TODO story]'},
        {'type': 'npc', 'name': 'Courtier', 'at': [9, 12], 'sprite': 'NPC 08', 'dir': 'right',
         'text': 'Courtier: Living-wood rafters. They say the hall grows a hand taller every reign. [TODO story]'},
        {'type': 'warp', 'at': [16, 6], 'to': {'map': 287, 'x': 13, 'y': 23, 'dir': 'up'}},
        {'type': 'warp', 'at': [15, 23], 'to': {'map': 285, 'x': 48, 'y': 23, 'dir': 'down'}},
        {'type': 'warp', 'at': [16, 23], 'to': {'map': 285, 'x': 48, 'y': 23, 'dir': 'down'}},
        {'type': 'warp', 'at': [17, 23], 'to': {'map': 285, 'x': 48, 'y': 23, 'dir': 'down'}},
    ]

    m.paint()
    head = {
        'id': 286, 'name': 'Briar Hall - Great Hall', 'bgm': 'Natural Park', 'parent': 285,
        'tone': [10, 4, -10, 0],
        'metadata': {'Name': 'Briar Hall', 'Outdoor': False, 'MapPosition': [0, 14, 12]},
        '_file': '286_briar_hall_great_hall.yaml',
    }
    m.write(286, head, comment='# Briar Hall - Great Hall (286). GENERATED by layouts/verdance_palace.py (Wave 5 Map Craft).\n')
    return m


# ================================================================================================ 287 Briar Hall - Throne Room
def build_287():
    W, H = 27, 27
    m = Palace(W, H, seed=287, tid=59)
    m.STAIRS = tuple(P1('lm_stair_' + k) for k in 'lmr')   # Grand White-Marble Sovereign Staircase!
    R = m.room_box

    # ---- 1. Dramatic Void-Sculpted Octagonal / Stepped Sovereign Sanctuary
    # Elevated Marble Sovereign Dais (TER) in a regal T-stepped apse:
    #   - Crown Throne Apse: x=8..18, y=5..9 (wall lip y=4, face y=5, base y=6 -> OPEN DAIS FLOOR y=7..9!)
    #   - Projecting Central Dais Tongue: x=11..15, y=9..11 (so Queen Maelis @ (14,10) stands heroically on the dais!)
    #   - Side Dais Cliffs drop at y=9..11 (lip y=9, face y=10, base y=11) -> y=12..13 OPEN FLOOR for Thorn Guards @ (10,13)/(16,13)!
    R(8, 5, 18, 9, TER, 'Y', 'H')
    R(11, 9, 15, 11, TER, 'Y', 'H')
    # Stepped Octagonal Royal Court Nave (FLOOR): y=10..23
    R(4, 11, 22, 22, FLOOR, 'H', 'H')
    # Recessed West & East Royal Guard / Banner Gallery Alcoves (x=3..4 & x=22..23, y=14..19)
    R(2, 13, 5, 20, FLOOR, 'H', 'H')
    R(21, 13, 24, 20, FLOOR, 'H', 'H')
    # Narrowed Monumental Southern Entry Portal framing warps (12..14, 25) and arrival (13, 23)
    R(10, 22, 16, 25, FLOOR, 'Y', 'H')

    # Carve bold octagonal corner chamfers into pure black void (ZERO flat rectangle!)
    m.mass_at([
        # Dais crown corners
        (8, 5), (18, 5),
        # Upper court shoulders & outer octagonal bevels
        (4, 11), (5, 11), (21, 11), (22, 11),
        (2, 13), (2, 14), (24, 13), (24, 14),
        (2, 19), (2, 20), (24, 19), (24, 20),
        # Lower court octagonal bevels narrowing cleanly to the southern entry portal
        (4, 21), (4, 22), (5, 22), (6, 22),
        (22, 21), (22, 22), (21, 22), (20, 22),
    ])

    # Grand 5-wide Marble Sovereign Staircase descending from Queen Maelis's Dais (x=11..15, y=11..13)!
    m.stairs(11, 11, w=5, n=3, c='.')
    m.plan_cliffs(rows=3)

    # ---- 2. Regal Material Contrast: Ivory-and-Gold Marble Nave + Walnut Side Galleries + Crimson Runner
    # Elevated Marble Sovereign Dais (y=7..10) with golden inlay frame!
    m.marble_floor(8, 7, 18, 10, 'plaza')
    m.marble_inlay(9, 7, 17, 9)
    # Central Processional Court Nave (x=9..17, y=14..25) — pale ivory marble with gold-cyan border
    m.marble_floor(9, 13, 17, 25, 'plaza')
    m.marble_inlay(9, 14, 17, 22)
    # Sweeping Royal Crimson-and-Gold Sovereign Carpet Runner from entry (y=25) up to the marble stairs (y=14)
    m.runner(12, 14, 14, 25)
    # Royal Crimson Medallion Throne Carpet on the elevated Dais framing the Thorn Throne!
    m.rug('R', 11, 7, 15, 10, medallion=True)
    # Matching Crimson Court Gallery Rugs under West & East Spectator Alcoves
    m.rug('R', 4, 15, 7, 20, medallion=False)
    m.rug('R', 19, 15, 22, 20, medallion=False)

    # ---- 3. The Sovereign Thorn Throne Focal Masterpiece (perfect bilateral symmetry around x=13!)
    # Towering Crimson-Draped Sovereign Window directly behind the Throne (13, 5..6), flanked by golden sconces,
    # Evergreen Elowen Banners (11,5 & 15,5) and twin gothic palace windows (10,5 & 16,5)!
    for wx, wy in ((13, 5), (10, 5), (16, 5), (6, 11), (20, 11)):
        m.on('mn_window', wx, wy)
    for bx, by in ((9, 5), (11, 5), (15, 5), (17, 5), (5, 11), (21, 11)):
        m.on('fw_ban_e', bx, by)
    m.late.append((1, 12, 6, P1('mn_sconce')))
    m.late.append((1, 14, 6, P1('mn_sconce')))
    # The Thorn Throne Seat (x=13, y=8) framed tightly by twin gilded candelabras (12,7 & 14,7 -> bases 12,8 & 14,8!)
    # and ceremonial white briar lilies & royal marble statues on the Dais wings!
    m.on('mn_chairR_down', 13, 8)
    m.on('mn_candelabra', 12, 7)
    m.on('mn_candelabra', 14, 7)
    m.on('nt_lily', 10, 7)
    m.on('nt_lily', 16, 7)
    m.on('mn_statue', 9, 7)
    m.on('mn_statue', 17, 7)
    m.on('fw_brazier', 8, 8)
    m.on('fw_brazier', 18, 8)

    # ---- 4. Imposing Marble Colonnade Pillars, Ceremonial Braziers & Royal Guard Gallery Alcoves
    # Monumental fluted marble colonnade along x=9 and x=17 (rows y=15, 18, 21) framing the Sovereign Aisle!
    for x in (9, 17):
        for y in (15, 18, 21):
            m.on('nr_col', x, y)
    # Flaming braziers flanking the southern grand entrance & lower nave
    for bx, by in ((11, 23), (15, 23), (8, 14), (18, 14)):
        m.on('fw_brazier', bx, by)
    # Suits of Thorn Guard ceremonial armour standing sentry inside the recessed West & East Banner Alcoves!
    for ax, ay in ((3, 15), (3, 18), (23, 15), (23, 18)):
        m.on('mn_armour', ax, ay)
    # Velvet court seating benches in the West & East walnut spectator bays (leaving wide aisles all around!)
    for by in (16, 19):
        m.on('mn_sofa', 5, by)
        m.on('mn_sofa', 20, by)
    # Noble floral urns & candelabras finishing the alcoves
    for cx, cy in ((5, 13), (21, 13), (6, 21), (20, 21)):
        m.on('mn_candelabra', cx, cy)
    m.on('mn_palm', 7, 13)
    m.on('mn_palm', 19, 13)

    # ---- 5. Grand Chandeliers, Stained-Glass Sunbeam Shafts & Warm Brazier/Throne Halos
    for cx, cy in ((12, 8), (12, 15), (12, 20)):
        m.stamps.append(('mn_chandelier', cx, cy))
    for sx, sy in ((10, 7), (16, 7), (12, 7), (6, 13), (20, 13)):
        m.stamps.append(('cv_shaft', sx, sy))
    for gx, gy in ((13, 8), (8, 8), (18, 8), (8, 14), (18, 14), (13, 16), (13, 21), (11, 23), (15, 23)):
        m.stamps.append(('pf_glow', gx, gy))

    # ---- 6. Exact HEAD Events & Warps (6/6 preserved!)
    m.events = [
        {'type': 'npc', 'name': 'Queen Maelis', 'at': [14, 10], 'sprite': 'NPC 25', 'dir': 'down',
         'text': 'Queen Maelis: You stand before the Thorn Throne of Elowen. [TODO story: court audience, Festival delegation]'},
        {'type': 'npc', 'name': 'Thorn Guard', 'at': [10, 13], 'sprite': 'NPC 07', 'dir': 'right', 'text': 'Thorn Guard: ...'},
        {'type': 'npc', 'name': 'Thorn Guard', 'at': [16, 13], 'sprite': 'NPC 07', 'dir': 'left', 'text': 'Thorn Guard: ...'},
        {'type': 'warp', 'at': [12, 25], 'to': {'map': 286, 'x': 16, 'y': 8, 'dir': 'down'}},
        {'type': 'warp', 'at': [13, 25], 'to': {'map': 286, 'x': 16, 'y': 8, 'dir': 'down'}},
        {'type': 'warp', 'at': [14, 25], 'to': {'map': 286, 'x': 16, 'y': 8, 'dir': 'down'}},
    ]

    m.paint()
    head = {
        'id': 287, 'name': 'Briar Hall - Throne Room', 'bgm': 'Natural Park', 'parent': 285,
        'tone': [12, 6, -8, 0],
        'metadata': {'Name': 'Briar Hall', 'Outdoor': False, 'MapPosition': [0, 14, 12]},
        '_file': '287_briar_hall_throne.yaml',
    }
    m.write(287, head, comment='# Briar Hall - Throne Room (287). GENERATED by layouts/verdance_palace.py (Wave 5 Map Craft).\n')
    return m


# ================================================================================================ 295 Cathedral of the Evergreen
def build_295():
    W, H = 31, 29
    m = Palace(W, H, seed=295, tid=59, pool='Cave Pool')
    m.STAIRS = tuple(P1('st_stair_' + k) for k in 'lmr')   # Carved Stone Sanctuary Staircase!
    R = m.room_box

    # ---- 1. True Cruciform Cathedral Silhouette carved into Black Void
    # Unified Sacred Evergreen & Sage-Stone Cathedral Paneling ('N' deep emerald fluted apse + 'F' sage-evergreen transepts/nave!)
    # (Replaces jarring dark night-glasshouse wall strip 'G' with true reverent cathedral architecture!)
    R(9, 4, 21, 12, TER, 'N', 'A')
    R(2, 13, 28, 20, FLOOR, 'F', 'A')
    R(5, 19, 25, 25, FLOOR, 'F', 'A')
    R(11, 25, 19, 27, FLOOR, 'N', 'A')

    # Carve sculpted Cruciform apse bevels & corner chamfers into void (ZERO boxy rectangle!)
    m.mass_at([
        # Semi-octagonal High Apse crown chamfers
        (9, 4), (10, 4), (9, 5), (20, 4), (21, 4), (21, 5),
        # Transept chapel outer bevels
        (2, 13), (2, 14), (28, 13), (28, 14),
        (2, 19), (2, 20), (3, 20), (28, 19), (28, 20), (27, 20),
        # Nave lower shoulders tapering to the Narthex Porch
        (5, 24), (5, 25), (6, 25), (25, 24), (25, 25), (24, 25),
        (11, 27), (19, 27),
    ])

    # Grand 5-wide Carved Stone Sanctuary Staircase descending from the High Apse (x=13..17, y=12..14)!
    m.stairs(13, 12, w=5, n=3, c='.')
    m.plan_cliffs(rows=3)

    # ---- 2. Distinct Sacred Emerald, Pale Carved Stone & Aged Oak Palette (Completely distinct from Briar Hall!)
    # High Sanctuary Apse: pale carved cathedral paving with inlaid stone Sanctuary border
    m.marble_floor(9, 6, 21, 11, 'pave')
    m.marble_inlay(11, 6, 19, 10)
    # Central Nave Processional Aisle & Transept Crossing: pale carved stone paving (oak planks remain under pew bays!)
    m.marble_floor(12, 15, 18, 27, 'pave')
    m.marble_floor(3, 16, 27, 18, 'pave')
    # Sweeping Sacred Emerald-and-Gold Sanctuary Medallion Runner from Narthex (y=27) straight to the High Altar!
    m.rug('G', 14, 15, 16, 27, medallion=True)
    m.rug('G', 13, 8, 17, 11, medallion=True)
    # Sacred Emerald Sanctuary Crossing Medallion
    m.rug('G', 12, 16, 18, 18, medallion=True)

    # ---- 3. High Sanctuary Apse: Clear 19th Rose Oculus, Sacred Altar Shrine & Living White Lilies!
    # The iconic "nineteenth pane left clear": Rose Oculus directly over the High Altar at (14..15, 4..5)!
    m.on('mn_oculus', 14, 4)
    # Tall sky-blue leaded cathedral windows (mn_window_bare) along the apse & transept north walls
    for wx, wy in ((11, 4), (13, 4), (17, 4), (19, 4), (5, 13), (7, 13), (23, 13), (25, 13)):
        m.on('mn_window_bare', wx, wy)
    # Sacred Evergreen Banners hanging between the cathedral windows
    for bx, by in ((12, 4), (18, 4), (4, 13), (8, 13), (22, 13), (26, 13)):
        m.on('fw_ban_e', bx, by)

    # Sacred Stone High Altar Shrine (pf_shrine 2x3) centered cleanly at (14..15, 6..8) directly behind Prior (15, 11)!
    m.on('pf_shrine', 14, 6)
    # Living White Lily Shrines (nt_lily, foreshadowing Ch9's white lilies!) & marble white-blossom planters flanking Altar!
    # Placed at x=11/19 & x=10/20 so the ENTIRE emerald Sanctuary carpet (x=13..17, y=9..11) is wide open & walkable!
    for lx, ly in ((11, 7), (19, 7), (10, 9), (20, 9)):
        m.on('nt_lily', lx, ly)
    m.on('lm_planter', 12, 6)
    m.on('lm_planter', 17, 6)
    # Tall Golden Cathedral Candelabras flanking the Sanctuary Carpet & Stairhead cleanly outside (13..17, 9..11)!
    for cx, cy in ((12, 8), (18, 8), (11, 10), (19, 10), (12, 15), (18, 15)):
        m.on('mn_candelabra', cx, cy)
    # Sacred Indoor Saplings framing the outer apse shoulders
    m.on('nt_sapling', 10, 6)
    m.on('nt_sapling', 20, 6)

    # ---- 4. Cruciform Living Evergreen Transept Chapels (West x=2..8 & East x=22..28, y=15..19)
    # Living indoor sacred evergreens (nt_pine_a 2x3), marble garden fountain shrines (mn_fountain 2x2),
    # living White Lilies, ferns, stone contemplative benches & cathedral harp!
    # West Evergreen Chapel:
    m.on('nt_pine_a', 3, 15)
    m.on('mn_fountain', 6, 16)
    m.on('nt_lily', 5, 15)
    m.on('nt_lily', 8, 15)
    m.on('nt_fern0', 3, 18)
    m.on('nt_fern1', 5, 18)
    m.on('mn_harp', 8, 18)
    m.on('mn_candelabra', 4, 18)
    # East Evergreen Chapel:
    m.on('nt_pine_a', 26, 15)
    m.on('mn_fountain', 23, 16)
    m.on('nt_lily', 22, 15)
    m.on('nt_lily', 25, 15)
    m.on('nt_fern1', 27, 18)
    m.on('nt_fern0', 25, 18)
    m.on('pf_stonebench', 22, 18)
    m.on('mn_candelabra', 26, 18)

    # ---- 5. Monumental Cathedral Colonnade & Perfectly Symmetrical Oak Pew Bays!
    # Fluted marble columns framing the Nave & Transept Crossing (x=11 and x=19)
    for x in (11, 19):
        for y in (19, 22, 24):
            m.on('nr_col', x, y)
    # SYMMETRICAL 2-column Oak Pew Bays on BOTH Left (x=6..9) and Right (x=21..24), 3 neat rows!
    for py in (20, 22):
        m.on('mn_bench', 6, py)
        m.on('mn_bench', 9, py)
        m.on('mn_bench', 20, py)
        m.on('mn_bench', 23, py)
    m.on('mn_bench', 8, 24)
    m.on('mn_bench', 21, 24)

    # Reverent Southern Narthex Porch framing Exit @ (15, 27):
    m.on('lm_planter', 12, 25)
    m.on('lm_planter', 17, 25)
    m.on('nt_lily', 12, 26)
    m.on('nt_lily', 18, 26)
    m.on('mn_candelabra', 13, 26)
    m.on('mn_candelabra', 17, 26)

    # ---- 6. Soaring Cathedral Light Shafts (cv_shaft), Chandeliers & Sacred Candlelight Halos
    for cx, cy in ((14, 9), (14, 16), (14, 21)):
        m.stamps.append(('mn_chandelier', cx, cy))
    for sx, sy in ((11, 6), (14, 6), (18, 6),            # High Altar sunbeams from the 19th clear oculus & apse windows!
                   (5, 15), (7, 15), (23, 15), (25, 15), # East/West Evergreen Transept sunbeams
                   (8, 20), (21, 20), (14, 22)):         # Nave stained-glass light shafts across pews & emerald runner
        m.stamps.append(('cv_shaft', sx, sy))
    for gx, gy in ((15, 8), (15, 11), (15, 17), (15, 22), (6, 16), (23, 16), (13, 26), (17, 26)):
        m.stamps.append(('pf_glow', gx, gy))

    # ---- 7. Exact HEAD Events (2/2 preserved!)
    m.events = [
        {'type': 'exit', 'at': [15, 27], 'link': 'C280_CATH'},
        {'type': 'npc', 'name': 'Evergreen prior', 'at': [15, 11], 'sprite': 'NPC 12', 'dir': 'down',
         'text': 'Prior: Eighteen windows for eighteen Plates. The nineteenth pane is clear, and we do not say why. [TODO story]'},
    ]

    m.paint()
    head = {
        'id': 295, 'name': 'Cathedral of the Evergreen', 'bgm': 'Natural Park', 'parent': 280,
        'tone': [2, 8, -4, 0],
        'metadata': {'Name': 'Cathedral of the Evergreen', 'Outdoor': False, 'MapPosition': [0, 14, 12]},
        '_file': '295_cathedral.yaml',
    }
    m.write(295, head, comment='# Cathedral of the Evergreen (295). GENERATED by layouts/verdance_palace.py (Wave 5 Map Craft).\n')
    return m


def main(which=None):
    sel = set(which or [])
    if not sel or '286' in sel:
        build_286()
    if not sel or '287' in sel:
        build_287()
    if not sel or '295' in sel:
        build_295()


if __name__ == '__main__':
    main(sys.argv[1:])
