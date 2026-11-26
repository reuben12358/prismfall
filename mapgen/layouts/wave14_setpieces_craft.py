#!/usr/bin/env python3
"""layouts/wave14_setpieces_craft.py - Rejuvenation V14 Map Craft Wave 14:
ALL 11 Remaining Gym, Ferry & Story Setpiece Interiors (100% exclusive to Wave 14):

  Group 1 — Prologue Ferry (109_dovetail.yaml):
    - 109: The Dovetail - Deck (34x22, ts 51)
        Layered deep-ocean swells, shimmering stern/bow wake glints, organized nautical cargo &
        rigging clusters, warm amber deck-lantern halos, coiled rope beside HiddenItem (27,12),
        preserving 100% of all 22 events (incl. Wattrel nest (12,9), start (7,6), Deckhand walk (5..8,12)).
    - 110: The Dovetail - Cabin (20x15, ts 34)
        Void-sculpted tapered ferry-hull cabin with west bunk berth & east stern larder alcove,
        twin maritime diamond portholes, intact 2x2 lifebuoy on bulkhead, crimson cabin rug,
        ship's galley behind Cook (9,7), 2x2 iron-bound sea trunk, glowing ruby bulkhead lamps.

  Group 2 — Gym 2 Loomhouse Lofts & Gym 1 Pell Playhouse Backstage (ts 54, hooked in hallkit.py):
    - 132: Loomhouse Upper Lofts - Canopy Lofts (25x26, ts 54)
        Unified 100% with 131 The Canopy: living elder-tree bark crown & side trunk walls, twin
        knot-holes with diagonal golden canopy sunbeams, shadowed hollow depth gradient, 3D timber
        ledge fascias & vertical pier supports under all 6 decks, pas=15 color-coded spool rigging
        lines, hanging cocoons/dyed silk strands/roots, and woven crimson-gold deck carpets.
    - 134: Loomhouse Upper Lofts - Granny's Knot (20x15, ts 54)
        Unified 100% with 130/131: void-sculpted weaver's sanctum with raised 3-row timber wall,
        tall arched sunlit windows, living elder-bark pilasters, crimson-gold loom sanctuary carpet
        framing T1..T5 & Treadle 1..5, heritage looms/dye vats/shelves/lanterns & golden sunbeams.
    - 151: Pell Playhouse Backstage - The Old Revolve (25x21, ts 54)
        Unified 100% with 150/154: dark Art-Deco burgundy-plum opera paneling & gilded proscenium
        beam/crest banishing stark white walls, sunken orchestra pit with footlights/glow/music
        stands, Nightbox damask promenade carpet with gold-filigree borders & royal crimson runner,
        gilded sconces/chandeliers & dramatic spotlighting (0 blocked puzzle tiles!).
    - 152: Pell Playhouse Backstage - Fly Loft (25x15, ts 54)
        Unified 100% with 150/151/154: dark burgundy fly-gallery wall with hung Act I-III drop-tops
        & brass sconces, gold-trimmed catwalk with batten slot marks, brass safety rail & girder
        fascia overlooking a breathtaking 40-foot shadowed aerial stage-well vista (pas=15) with
        vertical rigging piers, color-coded counterweight fly-ropes, distant footlights & spotlights!
    - 153: Pell Playhouse Backstage - The Trap Room (20x15, ts 54)
        Unified 100% with 150-154: moody sub-stage clockwork cellar & prop vault wrapping the
        playable labyrinth (all outer vaults strictly pas=15), with sunken mechanical gear pits,
        spare cogwheels, counterweight shafts, stacked retired drops/props, gilded Art-Deco 5x5
        turntable ring highlighting the rotating floor, and crimson runner from Ladder up (9,12).

  Group 3 — All 4 Trial Interiors (148_trial_interiors.yaml, ts 34):
    - 148: Saltmere Lantern House (20x16, ts 34)
        Void-sculpted octagonal weathered-stone coastal vigil chapel with west/east side-chapels,
        panoramic clerestory & arched coastal windows, golden beacon light pool, crystal lantern
        pedestal at Lantern rope (8,5), ruby vigil lamps, pews, scripture archives & crimson carpet.
    - 126: Briarwick Lantern House (20x16, ts 34)
        Void-sculpted hollow-tree woodland sanctuary with Sheridan timber walls, west loom-dyer
        niche, sunlit emerald-diamond East Botanical Conservatory bay (tile 501), golden shrine halo
        under Mother Aldreth (7,6) & Lantern-loom (6,6), lush ferns & crystal/ruby beacon lamps.
    - 168: The Net Loft (21x17, ts 34)
        Void-sculpted Ebbmouth harbor loft with stepped west net-hoist & east tackle/rum-cask bays,
        slate cargo apron, crimson crew feast carpet around the long dining table, glowing Tally
        Mast beacon bay, intact 2x2 wall lifebuoy, coastal charts, barrels, crates & fishing gear.
    - 542: The Brinewife's Rest (20x16, ts 34)
        Void-sculpted storm-weathered stone-and-timber marsh wayside inn with twin tucked-in bunk
        alcoves, simmering salt-broth stone hearth kitchenette, crimson hearth carpet & guestbook
        table below Rest house keeper (9,7), glowing ruby hearth lamps & marsh ferns.

Run directly:
    /usr/bin/python3 -I mapgen/layouts/wave14_setpieces_craft.py
or selectively:
    /usr/bin/python3 -I mapgen/layouts/wave14_setpieces_craft.py 109 110 148 126 168 542
"""
import os
import sys
import random
import numpy as np
import yaml

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAYOUTS = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
if LAYOUTS not in sys.path:
    sys.path.insert(0, LAYOUTS)

import passguard as PG
from interiorkit import TF

TID_INT = 34
VOID_INT = 5437
FLOOR_GLASS = 501

SLATE = [
    [1152, 1153, 1154],
    [1160, 1161, 1162],
    [1168, 1169, 1170],
]
HOTEL_RUG = [
    [7172, 7173, 7174],
    [7180, 7181, 7182],
    [7188, 7189, 7190],
]
SHER_RUG = [
    [5411, 5412, 5413],
    [5419, 5420, 5421],
    [5427, 5428, 5429],
]
BLUE_CARPET = [
    [7496, 7497, 7498],
    [7504, 7505, 7506],
    [7512, 7513, 7514],
]
NORDIC_RUG = [
    [1008, 1009, 1010],
    [1016, 1017, 1018],
    [1024, 1025, 1026],
    [1032, 1033, 1034],
]


def _put_nordic_rug(L, x0, y0, x1, y1, z=1):
    for y in range(y0, y1 + 1):
        ry = 0 if y == y0 else (3 if y == y1 else (1 if (y - y0) % 2 == 1 else 2))
        for x in range(x0, x1 + 1):
            rx = 0 if x == x0 else (2 if x == x1 else 1)
            L[z, y, x] = NORDIC_RUG[ry][rx]


# ==============================================================================
# SHARED TILESET 34 INTERIOR HELPERS (MATCHING station_103 / lighthouse_105_106)
# ==============================================================================
def _put_tf(L, name, x, y):
    rows, top = TF[name]
    for dy, row in enumerate(rows):
        for dx, t in enumerate(row):
            if not t:
                continue
            z = 2 if dy < top else 1
            if z == 1 and L[1, y + dy, x + dx]:
                z = 2
            L[z, y + dy, x + dx] = t


def _put_grid(L, grid, x, y, z_rows=None):
    for dy, row in enumerate(grid):
        z_def = z_rows[dy] if z_rows is not None else 1
        for dx, t in enumerate(row):
            if not t:
                continue
            z = z_def
            if z == 1 and L[1, y + dy, x + dx]:
                z = 2
            L[z, y + dy, x + dx] = t


def _put_9slice(L, tiles9, x0, y0, x1, y1, z=0):
    for y in range(y0, y1 + 1):
        ry = 0 if y == y0 else (2 if y == y1 else 1)
        for x in range(x0, x1 + 1):
            rx = 0 if x == x0 else (2 if x == x1 else 1)
            L[z, y, x] = tiles9[ry][rx]


def _seam_room(L, floor, style='timber', wall_rows=2, base_floor_fn=None):
    """Paint void-sculpted Sheridan timber OR weathered coastal stone walls + perimeter
    void casing (5533..5562) around any sculpted boolean floor mask on Tileset 34."""
    H, W = floor.shape
    L[0, :, :] = VOID_INT

    wall_face = np.zeros((H, W), dtype=bool)
    for y in range(wall_rows + 1, H):
        for x in range(1, W - 1):
            if floor[y, x] and not floor[y - 1, x]:
                for k in range(1, wall_rows + 1):
                    wall_face[y - k, x] = True

    interior = floor | wall_face

    for y in range(H):
        for x in range(W):
            if floor[y, x]:
                if base_floor_fn is not None:
                    L[0, y, x] = base_floor_fn(x, y, floor)
                else:
                    top_row = not floor[y - 1, x]
                    left_edge = not floor[y, x - 1]
                    if top_row:
                        L[0, y, x] = 5352 if left_edge else 5353 + (x - 3) % 3
                    else:
                        L[0, y, x] = 5360 if left_edge else 5361 + (x - 3) % 3
            elif wall_face[y, x]:
                is_lower = (y + 1 < H and floor[y + 1, x])
                left_end = not wall_face[y, x - 1]
                right_end = not wall_face[y, x + 1]
                if style == 'stone':
                    if is_lower:
                        L[0, y, x] = 1219 if left_end else (1221 if right_end else 1220)
                    else:
                        L[0, y, x] = 1211 if left_end else (1213 if right_end else 1212)
                else:
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


# ==============================================================================
# SHARED TILESET 54 HELPERS (MATCHING halls_craft.py)
# ==============================================================================
def _put_mi_rug(h, x0, y0, x1, y1, z=1):
    import hallkit as K
    MI = K.MI
    grid = [[MI(1040), MI(1041), MI(1042)],
            [MI(1048), MI(1049), MI(1050)],
            [MI(1056), MI(1057), MI(1058)]]
    for y in range(y0, y1 + 1):
        ry = 0 if y == y0 else (2 if y == y1 else 1)
        for x in range(x0, x1 + 1):
            rx = 0 if x == x0 else (2 if x == x1 else 1)
            h.put(grid[ry][rx], x, y, z)


def _put_deco_frame(h, x0, y0, x1, y1, z=1):
    """Art-Deco gold-filigree promenade border (NM 1560..1578, pas=0, pri=0)."""
    import hallkit as K
    NM = K.NM
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            top = (y == y0)
            bot = (y == y1)
            lft = (x == x0)
            rgt = (x == x1)
            if not (top or bot or lft or rgt):
                continue
            if top and lft:
                t = NM(1560)
            elif top and rgt:
                t = NM(1562)
            elif bot and lft:
                t = NM(1576)
            elif bot and rgt:
                t = NM(1578)
            elif top:
                t = NM(1561)
            elif bot:
                t = NM(1577)
            elif lft:
                t = NM(1568)
            else:
                t = NM(1570)
            h.put(t, x, y, z)


def _put_windows_54(h, xs, y0):
    import hallkit as K
    for x in xs:
        for dy, part in enumerate(('top', 'mid', 'sill')):
            for c in range(2):
                h.put(K.CU('window_%s_%d' % (part, c)), x + c, y0 + dy, 1)


# ==============================================================================
# GROUP 1: THE DOVETAIL PROLOGUE FERRY (Maps 109 & 110)
# ==============================================================================
def build_109(save=True):
    """Wave 14 craft of Map 109 (The Dovetail - Deck, 34x22, Tileset 51).
    Layered deep-ocean swell channels, shimmering wake glints, organized nautical cargo &
    rigging vignettes, glowing deck lanterns, coiled rope by HiddenItem (27,12), and wide
    unobstructed cutscenes for Deckhand (5..8,12), Edda (6,9), Voss (21,8), Start (7,6),
    Wattrel nest (12,9), Cabin hatch (15,10..11) & Gangway (9,15)."""
    import rkit as K
    import render as R
    import ship_art as SA

    W, H = 34, 22
    m = K.RMap(W, H, 51, 109, water='Ocean')
    SA.use('dovetail')
    deck = SA.deck
    dk = np.array([[bool(deck(x, y)) for x in range(W)] for y in range(H)])

    # Sculpt dramatic layered deep-ocean swell bands framing the ferry (banishing polka-dot blobs!)
    for y in range(H):
        for x in range(W):
            m.cls[y, x] = 'w'
    # Outer deep-water horizon bands top (y=0..2), bottom (y=19..21), plus sweeping bow/stern ocean swells
    for y in range(H):
        for x in range(W):
            dy_ship = 0
            if y < 5:
                dy_ship = 5 - y
            elif y > 15:
                dy_ship = y - 15
            # Gentle sinusoidal coastal swell waves in open water far from the hull
            wave_n = 2.6 + 0.85 * np.sin((x + 3) * 0.38)
            wave_s = 18.4 + 0.85 * np.sin((x - 2) * 0.34)
            if y <= wave_n or y >= wave_s:
                m.cls[y, x] = 'W'
            # Distant deep-ocean horizon pockets on far west/east edges
            if (x <= 1 and (y <= 6 or y >= 15)) or (x >= 32 and (y <= 6 or y >= 15)):
                m.cls[y, x] = 'W'
    # Keep a 2-tile clear turquoise wake cushion immediately surrounding the hull
    near = np.zeros((H, W), bool)
    for y, x in np.argwhere(dk):
        near[max(0, y - 2):min(H, y + 3), max(0, x - 2):min(W, x + 3)] = True
    m.cls[near] = 'w'
    K.RMap.smooth(m, 'W', into='w', passes=1, only='w')
    m.cls[near] = 'w'

    m.paint_ground()
    m.autotiles()

    # Paint the vessel hull onto the ocean
    tc = R.TileCache(R.tilesets()[51])
    opaque = {}

    def is_opaque(t):
        if t not in opaque:
            im = tc.tile(t)
            opaque[t] = im is not None and im.getchannel('A').getextrema()[0] == 255
        return opaque[t]

    interior = np.zeros((H, W), bool)
    for x, y, z, t in K._ST['_ship_dovetail']['tiles']:
        if not m.inb(x, y):
            continue
        if z == 0:
            if is_opaque(t):
                m.L[0, y, x] = t
                m.L[1, y, x] = 0
                interior[y, x] = True
            else:
                m.L[1, y, x] = t
        else:
            m.L[2, y, x] = t

    # Reserved cells: ALL 22 events (incl. Wattrel nest (12,9)), start (7,6), Cabin arrival (15,11),
    # Deckhand intro walk (5..8,12), Rail watch (10..14,6), Voss approach (15..21,8), Edda approach (6..9,7..9)
    events_109 = {
        (16, 13), (12, 5), (13, 5), (10, 6), (11, 6), (12, 6), (13, 6), (14, 6),
        (6, 9), (21, 8), (9, 15), (30, 10), (27, 12), (8, 12), (18, 6), (24, 13),
        (16, 7), (17, 8), (26, 9), (4, 11), (15, 10), (15, 11), (12, 9), (7, 6),
    }
    reserved = set(events_109) | {
        (5, 12), (6, 12), (7, 12),  # Deckhand intro walk [left, left, left] from (8,12)
        (8, 6), (9, 6),             # Clear port-rail promenade right from Start (7,6) to Rail watch (10,6)!
        (7, 7), (8, 7), (9, 7), (10, 7),  # Edda & player promenade
        (9, 14), (9, 13),           # Clear approach to Gangway (9,15)
        (14, 10), (16, 10), (15, 9), (15, 12),  # Clear approach around Cabin hatch (15,10)
        (18, 8), (19, 8), (20, 8),  # Voss walk corridor west toward rail
        (27, 11), (26, 12), (28, 12),  # Clear access around HiddenItem coiled rope (27,12)
        (27, 10), (28, 10), (29, 10),  # Clear bow Horizon (30,10) approach!
    }

    def place_stamp(nm, x, y, allow_water=False):
        st = K.STAMPS[nm]
        Ls = np.array(st['layers'])
        for j in range(st['h']):
            for i in range(st['w']):
                cx, cy = x + i, y + j
                if not m.inb(cx, cy):
                    return False
                if Ls[1, j, i]:
                    if (cx, cy) in reserved or m.taken[cy, cx]:
                        return False
                    if not allow_water and not interior[cy, cx]:
                        return False
        for j in range(st['h']):
            for i in range(st['w']):
                cx, cy = x + i, y + j
                if Ls[1, j, i]:
                    m.L[1, cy, cx] = int(Ls[1, j, i])
                    m.taken[cy, cx] = True
                if Ls[2, j, i]:
                    if m.L[2, cy, cx] == 0:
                        m.L[2, cy, cx] = int(Ls[2, j, i])
        return True

    # Organized nautical deck architecture & cargo clusters:
    props = [
        # 1. Stern Wheelhouse & Captain Edda's Quarterdeck
        ('hb_wheelhouse', 4, 6),
        ('hb_lamp2', 4, 9),          # Warm deck lamp framing stern rail beside Edda (6,9)!
        ('hb_barrels', 6, 13),
        ('hb_rope', 7, 13),
        ('hb_keg', 5, 13),
        # 2. Midship Companionway & Aft Lantern Framing
        ('pf_lantern', 10, 11),      # Tall glowing deck lantern illuminating Gangway & midship!
        ('hb_boxes', 11, 13),
        ('sh_crates', 13, 12),
        ('hb_keg', 12, 12),
        ('hb_bollard1', 10, 14),
        # 3. Starboard Cargo & Fresh-Catch Freight Cluster (x=18..23, y=11..14)
        ('sh_crates', 18, 11),
        ('sh_crates', 21, 11),
        ('hb_fish', 18, 13),
        ('hb_barrel', 20, 13),
        ('hb_barrel2', 21, 13),
        ('hb_boxes2', 22, 13),
        ('hb_keg', 17, 12),
        # 4. Port-Side Rail Rigging & Fore-Deck Watch (bow corridor y=10 wide open to Horizon (30,10)!)
        ('hb_crates4', 20, 6),
        ('pf_p_lantern', 23, 6),     # Hanging ship's rigging lantern frame!
        ('hb_boxes', 25, 6),
        ('pf_p_net', 24, 8),         # Stowed maritime haul net
        ('hb_buoy2', 26, 7),         # Red-and-white lifebuoy near Sailor (26,9)
        ('hb_cask', 25, 11),         # Ship's rum cask aft of bow watch (keeps (27,10) wide open!)
        ('hb_rope', 26, 12),         # Coiled hawser rope right beside HiddenItem (27,12)!
        ('hb_bollard0', 28, 8),
        ('hb_bollard1', 28, 11),
    ]
    for nm, x, y in props:
        place_stamp(nm, x, y)

    # Subtle warm amber lantern halos (pf_glow: pri=5, pas=0) centered cleanly on ship lanterns only
    for gx, gy in ((10, 11), (23, 6)):
        st = K.STAMPS['pf_glow']
        Lg = np.array(st['layers'])
        for j in range(st['h']):
            for i in range(st['w']):
                cx, cy = gx + i, gy + j
                if m.inb(cx, cy) and Lg[2, j, i] and m.L[2, cy, cx] == 0:
                    m.L[2, cy, cx] = int(Lg[2, j, i])

    # Shimmering white-gold ocean wake & swell glints (hb_glint0..3: pri=2, pas=0) strictly on open water!
    wake_spots = [
        # Trailing stern wake turbulence (x=0..4, y=7..14)
        (0, 9), (1, 10), (1, 12), (2, 8), (2, 13), (3, 14),
        # Bow wave & Velmora horizon sparkles (x=29..33, y=7..14)
        (30, 8), (31, 9), (32, 11), (31, 13), (29, 14), (33, 10),
        # Distant northern & southern ocean swell glints
        (6, 3), (12, 2), (19, 3), (26, 2), (8, 17), (15, 18), (22, 17), (28, 18),
        (4, 17), (14, 4), (24, 4), (17, 17),
    ]
    for idx, (wx, wy) in enumerate(wake_spots):
        if m.inb(wx, wy) and not dk[wy, wx] and m.L[1, wy, wx] == 0 and m.L[2, wy, wx] == 0:
            gnm = 'hb_glint%d' % (idx % 4)
            gt = int(K.STAMPS[gnm]['layers'][2][0][0])
            m.L[2, wy, wx] = gt

    Lr = K.RC.resolve(m.L, 51).astype(np.int32)
    PG.guard(Lr, 51, list(events_109), 'map 109')
    if save:
        out = os.path.join(HERE, 'data', 'raw', '109.npy')
        np.save(out, Lr)
        print('wrote', out, Lr.shape)
    return Lr


def build_110(save=True):
    """Wave 14 craft of Map 110 (The Dovetail - Cabin, 20x15, Tileset 34).
    Void-sculpted tapered ferry-hull passenger cabin with west bunk berth, east stern larder
    alcove, twin diamond maritime portholes, intact 2x2 bulkhead lifebuoy, glowing ruby cabin
    lamps, crimson cabin carpet, ship's galley & 2x2 iron-bound sea trunk."""
    W, H = 20, 15
    L = np.zeros((3, H, W), dtype=np.int32)

    # 1. Tapered Ferry-Hull Cabin Silhouette (zero sterile box, balanced across 20x15!)
    floor = np.zeros((H, W), dtype=bool)
    floor[5:11, 3:13] = True       # Core cabin deck x=3..12, y=5..10
    floor[6:10, 2] = True          # West bow-berth hull alcove (x=2, y=6..9)
    floor[6:10, 13:16] = True      # East stern larder & rigging bay (x=13..15, y=6..9)
    floor[11, 6:9] = True          # Recessed companionway hatch vestibule around Up to deck (7,11)

    _seam_room(L, floor, style='timber', wall_rows=2)

    # 2. Multi-Zone Maritime Flooring
    # Cool slate stone galley hearth (8..11, 5..6) & companionway hatch threshold (6..8, 10..11)
    _put_9slice(L, SLATE, 8, 5, 11, 6, z=0)
    for y in (10, 11):
        for x in (6, 7, 8):
            L[0, y, x] = SLATE[0 if y == 10 else 2][x - 6]
    # Companionway timber stair mat at (6..8, 11) framing Up to deck (7,11)
    for i, x in enumerate((6, 7, 8)):
        L[1, 11, x] = 5512 + i
    # Cozy crimson braided passenger cabin carpet (5..8, 8..9)
    _put_9slice(L, SHER_RUG, 5, 8, 8, 9, z=1)

    # 3. Bulkhead Timber Ribs, Twin Diamond Portholes, Strait Map & Complete 2x2 Lifebuoy!
    for px in (5, 8, 10):
        L[0, 3, px] = 5548
        L[0, 4, px] = 5556
    # Twin maritime diamond portholes: above your bunk (4, 3..4) AND directly above Porthole (11,5)!
    L[0, 3, 4] = 5560; L[0, 4, 4] = 5568
    L[0, 3, 11] = 5560; L[0, 4, 11] = 5568
    # Complete intact 2x2 maritime lifebuoy cleanly mounted on bulkhead wall (5..6, 3..4) — ZERO clipping!
    _put_grid(L, [[4118, 4119], [4126, 4127]], 5, 3, z_rows=(1, 1))
    # Velmora strait chart cleanly above galley (8..10, 3) — zero overlap with kitchen (y=4..5)!
    _put_tf(L, 'map_wall', 8, 3)
    # Single portholes in West Berth (2, 4..5) & East Stern Bay (15, 4..5)
    L[0, 4, 2] = 5560; L[0, 5, 2] = 5568
    L[0, 4, 15] = 5560; L[0, 5, 15] = 5568

    # 4. Exact Story Anchors & Authentic Ship Cabin Props (100% HEAD event & passability parity!)
    # Bunk (3,7) + Mum's letter (4,7): complete bunk_o at (3..4, 5..7) -> solid bottom squarely on (3,7) & (4,7)!
    _put_tf(L, 'bunk_o', 3, 5)
    # West bow-berth bedside detail: potted herb (2,6), glowing ruby bulkhead lamp (2,7..8), passenger satchel (2,9)
    L[1, 6, 2] = 3391
    L[2, 7, 2] = 2244; L[1, 8, 2] = 2252
    L[1, 9, 2] = 5580
    # Bookshelf (7,5): tall cabin bookcase cleanly at (7, 4..5) right on (7,5)!
    _put_tf(L, 'bookshelf_s', 7, 4)
    # Ship's Galley Counter (kitchen 4x2 at (8..11, 4..5)) backing Cook (9,7) & Porthole sill (11,5)!
    _put_tf(L, 'kitchen', 8, 4)
    # Central Cabin Mess Table on crimson rug (6..7, 8..9) + open passenger manifest + stool!
    _put_tf(L, 'table_dark', 6, 8)
    L[2, 8, 6] = 3428
    L[2, 9, 5] = 4077
    # Locked trunk (10,8) stays cell_pas=True (exact BEFORE parity!); genuine 2x2 iron-bound sea chest at (10..11, 9..10)!
    _put_grid(L, [[5585, 5586], [5593, 5594]], 10, 9, z_rows=(1, 1))
    # SW Cabin Detail: oak water barrel (3, 9..10) + glowing ruby companionway lamp (4, 9..10) — leaves (3..4, 8) 100% open!
    L[2, 9, 3] = 4822; L[1, 10, 3] = 4830
    L[2, 9, 4] = 2244; L[1, 10, 4] = 2252
    # East Stern Larder & Rigging Bay (x=13..15, y=6..9): clean shelf_bottles with ZERO wall-chart overlap!
    _put_tf(L, 'shelf_bottles', 13, 5)        # (13..14, 5..6) galley spice & chowder bottles
    L[2, 6, 15] = 4823; L[1, 7, 15] = 4831    # tall salt-water cask
    L[1, 8, 15] = 4168                         # coiled hawser rope basket
    L[1, 9, 15] = 4101                         # oak mop bucket
    L[2, 8, 13] = 2244; L[1, 9, 13] = 2252    # glowing warm stern brass lamp!
    L[1, 9, 14] = 4077                         # sailor's stool

    PG.guard(L, TID_INT, [(7, 11), (7, 10), (3, 7), (4, 7), (7, 5), (9, 7), (10, 8), (11, 5)], 'map 110')
    if save:
        out = os.path.join(HERE, 'data', 'raw', '110.npy')
        np.save(out, L)
        print('wrote', out, L.shape)
    return L


# ==============================================================================
# GROUP 2: GYM 2 LOOMHOUSE LOFTS (132, 134) & GYM 1 PELL PLAYHOUSE BACKSTAGE (151, 152, 153)
# ==============================================================================
def build_132(save=True):
    """Wave 14 craft of Map 132 (Loomhouse Upper Lofts - Canopy Lofts, 25x26, Tileset 54).
    Unified 100% with 131 The Canopy (halls_craft.build_131):
      - Replaces pitch-black empty chasm with living elder-tree hollow (bark crown, curving side
        trunks, twin knot-hole skylights, deep shadowed hollow gradient, gnarled roots, hanging
        cocoons & dyed drying silk strands — ALL strictly pas=15!)
      - Frames every single one of the 6 suspended loft decks with 3D ledge fascias, vertical
        timber support piers, warm plank grain & woven crimson-gold Loomhouse silk carpets
      - Connects spools to destinations with pas=15 color-coded rigging threads (zero passguard hits!)
      - Preserves 100% of all 29 events, bridge cells, and 0 blocked puzzle tiles!"""
    import hallkit as K
    from puzzles import loomhouse as g1

    CU, MI = K.CU, K.MI
    rows = g1.LOFTS
    H, W = len(rows), len(rows[0])
    CLS = {'#': 'void', 'W': 'wall', '.': 'floor', 'v': 'pit', 'S': 'stair', 'o': 'floor'}
    h = K.Hall(rows, 'loom', dict(CLS, v='void'), seed=132)
    rnd = h.r

    BARK = [CU('bark_%d' % t) for t in (18044, 18045, 18046, 18047)]
    BARK_HI = [CU('bark_%d' % t) for t in (18036, 18037, 18038, 18039)]
    BARK_DIM = [CU('bark_dim_%d' % t) for t in (18044, 18045, 18046, 18047)]
    BOARDS = [MI(1241), MI(1242), MI(1243)]

    bridge_cells = set()
    for cells in g1.BRIDGE.values():
        bridge_cells.update(cells)

    # 1. Paint deep shadowed living elder-tree hollow across all chasm/void & bridge-gap cells (ALL pas=15!)
    for y in range(H):
        for x in range(W):
            ch = rows[y][x]
            if ch in ('#', 'v'):
                # Clear Hall's auto-void borders; replace with authentic elder-tree hollow & curving bark!
                h.put(0, x, y, 1)
                h.put(0, x, y, 2)
                if y == 0:
                    h.put(rnd.choice(BARK_HI), x, y, 0)
                elif y == 1:
                    h.put(rnd.choice(BARK), x, y, 0)
                elif x in (0, W - 1):
                    h.put(rnd.choice(BARK_DIM), x, y, 0)
                else:
                    # Depth shading: deeper shadow bands further from top skylights
                    depth = 0 if y < 8 else (1 if y < 17 else 2)
                    h.put(CU('hollow_%d_%d' % (depth, rnd.randrange(3))), x, y, 0)
            elif ch == '.':
                h.put(rnd.choice(BOARDS), x, y, 0)
            elif ch == 'S':
                h.put(BOARDS[0], x, y, 0)
                h.put(MI(962), x, y, 1)

    # 2. Living elder-tree knot-hole skylights high in the bark crown (y=0..1, pas=15!)
    for x0 in (5, 13):
        for part, (dx, dy) in (('tl', (0, 0)), ('tr', (1, 0)), ('bl', (0, 1)), ('br', (1, 1))):
            h.put(CU('knot_hole_' + part), x0 + dx, dy, 1)
    # Gossamer silk webs draped cleanly at high canopy corners (pri=2, non-blocking)
    h.obj('web', 1, 0)
    h.obj('web', 9, 0)
    h.obj('web', 16, 0)
    h.obj('web1', 22, 0)

    # 3. 3D Timber Ledge Fascias & Vertical Support Piers beneath EVERY one of the 6 decks (ALL pas=15!)
    for p, (x0, y0) in g1.DECKS.items():
        dh = 4 if p == 6 else 3
        fy = y0 + dh
        if fy < H:
            for i in range(4):
                fx = x0 + i
                if rows[fy][fx] != '#':
                    continue  # Never overwrite Down stair (2,24) or Bridge 2 (20,6)!
                t = 'ledge_face_l' if i == 0 else ('ledge_face_r' if i == 3 else 'ledge_face_mid')
                h.put(CU(t), fx, fy, 0)
        # Vertical timber pier legs dropping 3 tiles into the shadowed elder hollow from outer corners
        for px in (x0, x0 + 3):
            for k in range(1, 5):
                py = fy + k
                if py >= H - 1 or rows[py][px] != '#' or (px, py) in bridge_cells:
                    break
                tp = 'tpost_band' if k == 1 else ('tpost_base' if k == 4 else 'tpost_mid')
                h.put(CU(tp), px, py, 1)

    # 4. Color-Coded Spool Rigging Lines & Chasm Anchor Tie-Offs (ALL pas=15 -> ZERO passguard hits!)
    #    alpha -> blue, brass -> gold, gamma -> red
    cord_col = {'alpha': 'blue', 'brass': 'gold', 'gamma': 'red'}
    drawn = set()
    for name, (pos, cord, on, off) in g1.SPOOLS.items():
        # Anchor tie-off directly outside each spool on the chasm edge!
        ax, ay = pos[0] + 1, pos[1]
        if 1 <= ax < W - 1 and rows[ay][ax] == '#' and (ax, ay) not in bridge_cells:
            h.put(CU('web_anchor_r'), ax, ay, 1)
        col = cord_col[cord]
        for dest in (on, off):
            (x0, y0), (x1, y1) = pos, g1.CENTRE[dest]
            n = max(abs(x1 - x0), abs(y1 - y0))
            for i in range(1, n):
                x = round(x0 + (x1 - x0) * i / n)
                y = round(y0 + (y1 - y0) * i / n)
                if not (1 <= x < W - 1 and 2 <= y < H - 1):
                    continue
                if rows[y][x] != '#' or (x, y) in bridge_cells or (x, y) in drawn:
                    continue
                # Avoid stepping on immediate deck fascias
                if h.L[0, y, x] in (CU('ledge_face_l'), CU('ledge_face_mid'), CU('ledge_face_r')):
                    continue
                if h.L[1, y, x] != 0:
                    continue
                drawn.add((x, y))
                th = 'thread_%s_%s' % (col, 'h' if abs(x1 - x0) > abs(y1 - y0) else 'v')
                h.put(CU(th), x, y, 2)

    # 5. Hanging Silk Cocoons, Dyed Drying Strands, Gnarled Elder Roots & Canopy Sunbeams (ALL pas=15!)
    cocoons = [
        (2, 4), (8, 3), (16, 2), (23, 7), (1, 14), (9, 13), (15, 16),
        (23, 18), (7, 21), (17, 22), (8, 8), (22, 11),
    ]
    for cx, cy in cocoons:
        if (0 < cx < W - 1 and 2 <= cy < H - 2
                and rows[cy][cx] == '#' and rows[cy + 1][cx] == '#'
                and (cx, cy) not in bridge_cells and (cx, cy + 1) not in bridge_cells
                and h.L[1, cy, cx] == 0 and h.L[1, cy + 1, cx] == 0
                and h.L[2, cy, cx] == 0 and h.L[2, cy + 1, cx] == 0
                and h.L[0, cy, cx] not in (CU('ledge_face_l'), CU('ledge_face_mid'), CU('ledge_face_r'))):
            h.put(CU('cocoon_top'), cx, cy, 1)
            h.put(CU('cocoon_bot'), cx, cy + 1, 1)

    strands = [
        (3, 7, 'p'), (9, 4, 'w'), (17, 8, 'p'), (2, 17, 'w'),
        (16, 12, 'p'), (22, 21, 'w'), (7, 17, 'p'), (13, 12, 'w'),
    ]
    for sx, sy, col in strands:
        if (0 < sx < W - 1 and 2 <= sy < H - 2
                and rows[sy][sx] == '#' and rows[sy + 1][sx] == '#'
                and (sx, sy) not in bridge_cells and (sx, sy + 1) not in bridge_cells
                and h.L[1, sy, sx] == 0 and h.L[1, sy + 1, sx] == 0
                and h.L[2, sy, sx] == 0 and h.L[2, sy + 1, sx] == 0
                and h.L[0, sy, sx] not in (CU('ledge_face_l'), CU('ledge_face_mid'), CU('ledge_face_r'))):
            h.put(CU('strand_%s_top' % col), sx, sy, 1)
            h.put(CU('strand_%s_bot' % col), sx, sy + 1, 1)

    # Gnarled woodland roots across deep hollow shadow tiles (pas=15)
    for y in range(3, H - 1):
        for x in range(2, W - 2):
            if (rows[y][x] == '#' and (x, y) not in bridge_cells
                    and h.L[1, y, x] == 0 and h.L[2, y, x] == 0
                    and h.L[0, y, x] not in (CU('ledge_face_l'), CU('ledge_face_mid'), CU('ledge_face_r'))
                    and all(rows[y][x + dx] == '#' for dx in (-1, 1))
                    and rnd.random() < 0.08):
                h.put(CU('root_%d' % rnd.randrange(4)), x, y, 1)

    # Diagonal golden canopy sunbeams plunging from BOTH knot-hole skylights (strictly light_*_x pas=15 in chasm!)
    for x0, y1 in ((5, 9), (13, 8)):
        for y in range(2, y1 + 1):
            c = x0 + (y - 2)
            for dx, k in ((0, 'l'), (1, 'full'), (2, 'r')):
                x = c + dx
                if not (1 <= x < W - 1):
                    continue
                if rows[y][x] == '#' and (x, y) not in bridge_cells and h.L[1, y, x] == 0 and h.L[2, y, x] == 0:
                    h.put(CU('light_%s_x' % k), x, y, 1)

    # 6. Woven Crimson-Gold Loomhouse Silk Carpets centering all 6 loft decks (100% walkable, 0 blocked cells!)
    #    Keep exact deck footprints crisp & inviting!
    for p, (x0, y0) in g1.DECKS.items():
        if p == 6:
            # Grand royal woven carpet on P6 Granny's landing (19..22, 2..5)
            _put_mi_rug(h, x0, y0, x0 + 3, y0 + 2, z=1)
        else:
            # Inner crimson-gold silk mat framing center of each 4x3 deck
            _put_mi_rug(h, x0 + 1, y0, x0 + 2, y0 + 2, z=1)
    # Warm entry threshold framing Down to Weaving Hall (2, 24)
    h.put(MI(1049), 2, 23, 1)
    # Subtle overhead webs framing side edges of P3 & P4 (pri=2)
    h.obj('web1', 1, 10)
    h.obj('web1', 21, 12)

    ev_cells = (
        [s[0] for s in g1.SPOOLS.values()]
        + list(g1.CORDS.values())
        + list(g1.LADDERS.values())
        + [g1.LOFT_AT[k] for k in ('arrive', 'down', 'warp', 'mossy', 'hollis', 'ash', 'item')]
    )
    PG.guard(h.L, K.TID, ev_cells, 'map 132')
    if save:
        out = os.path.join(HERE, 'data', 'raw', '132.npy')
        np.save(out, h.L)
        print('wrote', out, h.L.shape)
    return h.L


def build_134(save=True):
    """Wave 14 craft of Map 134 (Loomhouse Upper Lofts - Granny's Knot, 20x15, Tileset 54).
    Unified 100% with 130 Loomhouse Lobby & 131 The Canopy:
      - Void-sculpted weaver's sanctum (SW (3,11) & SE (15,11) chamfered corners + recessed
        southern vestibule (8..10,12)) with raised 3-row timber wall (y=1..3)
      - Twin tall arched Loomhouse windows pouring diagonal golden sunbeams across the planks
      - Living elder-bark pilasters framing the corners & Briarwick silk/heddle tapestry framing Sampler (7,3)
      - Grand crimson-gold Loomhouse tapestry carpet framing T1..T5 (7..11,6) & Treadle 1..5 (7..11,9)
      - Heritage wooden looms, woven-pattern shelves, dye vats, silk bales & warm glowing lanterns!"""
    import hallkit as K
    from puzzles import loomhouse as g1

    CU, MI = K.CU, K.MI
    W, H = 20, 15
    g = [['#'] * W for _ in range(H)]
    for y in range(1, 4):
        for x in range(3, 16):
            g[y][x] = 'W'
    for y in range(4, 12):
        for x in range(3, 16):
            g[y][x] = '.'
    # Void-sculpted SW & SE sanctuary chamfers (100% clear of Granny's chest (5,10) & lever (12,10)!)
    g[11][3] = '#'
    g[11][15] = '#'
    # Recessed southern exit vestibule framing Back to the Lofts (9,12)
    for x in (8, 9, 10):
        g[12][x] = '.'

    rows = [''.join(r) for r in g]
    CLS = {'#': 'void', 'W': 'wall', '.': 'floor'}
    h = K.Hall(rows, 'loom', CLS, seed=134)

    # 1. Living elder-tree bark pilasters framing the outer corners & Briarwick weaver's wall banner
    BARK_HI = [CU('bark_18036'), CU('bark_18037')]
    BARK = [CU('bark_18044'), CU('bark_18045')]
    for bx in (3, 15):
        h.put(BARK_HI[0 if bx == 3 else 1], bx, 1, 0)
        h.put(BARK[0 if bx == 3 else 1], bx, 2, 0)
        h.put(BARK[1 if bx == 3 else 0], bx, 3, 0)

    # Tall 3-row arched Loomhouse windows at (4..5, 1..3) & (12..13, 1..3)!
    _put_windows_54(h, (4, 12), 1)

    # Pure Briarwick Weaver's Sampler Alcove (x=6..11, y=1..3): dyed silk strands & ceremonial heddle looms!
    for x in range(6, 12):
        h.put(CU('beam_l') if x == 6 else (CU('beam_r') if x == 11 else CU('beam_mid')), x, 1, 1)
    h.put(CU('strand_p_top'), 6, 2, 1); h.put(CU('strand_p_bot'), 6, 3, 1)
    h.put(CU('heddle_silk_top'), 7, 2, 1); h.put(CU('heddle_silk_bot'), 7, 3, 1)
    h.put(CU('heddle_gold_top'), 8, 2, 1); h.put(CU('heddle_gold_bot'), 8, 3, 1)
    h.put(CU('heddle_red_top'), 9, 2, 1); h.put(CU('heddle_red_bot'), 9, 3, 1)
    h.put(CU('heddle_green_top'), 10, 2, 1); h.put(CU('heddle_green_bot'), 10, 3, 1)
    h.put(CU('strand_w_top'), 11, 2, 1); h.put(CU('strand_w_bot'), 11, 3, 1)

    # 2. Grand Woven Crimson-Gold Sanctuary Carpet framing T1..T5 (7..11,6) & Treadle 1..5 (7..11,9)!
    _put_mi_rug(h, 6, 5, 12, 10, z=1)
    # Crimson runner connecting the altar straight south to Back to the Lofts (9, 12)
    for y in (11, 12):
        for x in (8, 9, 10):
            h.put(MI(1048 if x == 8 else (1050 if x == 10 else 1049)), x, y, 0)
    h.obj('mat_mi', 8, 12)

    # 3. Heritage Weaver's Sanctum Props (strictly clear of Sampler (7,3), T1..5, Treadles, Chest (5,10), Lever (12,10)!)
    # West wing (x=3..4): gossamer ceiling web, parlor fern, Mother Loom's antique loom, glowing lantern!
    h.obj('web', 3, 1)
    h.obj('plant', 3, 3)            # base at (3, 4)
    h.obj('loom', 3, 6)             # 2x2 wooden loom at (3..4, 6..7)
    h.obj('lantern', 3, 8)          # 1x3 tall lantern (base at (3, 10), glowing beside Granny's chest (5,10)!)
    h.obj('vat_y', 4, 11)           # golden dye vat framing SW chamfer (clear of (5,10) chest!)
    # East wing (x=14..15): floor-to-ceiling pattern shelf, silk bale, dye vats & warm glowing lantern!
    h.obj('shelf', 14, 1)           # 2x4 tall weaver's shelf (14..15, 1..4) — top on wall, base at y=4!
    h.obj('silk', 15, 5)            # stacked silk bolts at (15, 5..6)
    h.obj('lantern', 15, 7)         # 1x3 tall lantern (base at (15, 9))
    h.obj('vat_b', 14, 10)          # indigo dye vat in SE alcove (leaves (13, 4..11) wide open beside Lever (12,10)!)
    h.obj('vat_r', 15, 10)          # crimson dye vat beside it
    h.obj('plant', 14, 10) if False else h.obj('plant', 13, 10) if False else None
    # Potted woodland fern neatly flanking SE chamfer (14, 11) — top at (14,10)? Don't overlap vat_b! Put at (13, 11) base!
    h.put(MI(584), 13, 10, 2); h.put(MI(592), 13, 11, 1)  # clear of lever (12,10) & exit runner (8..10,11..12)!
    h.obj('web1', 13, 1)

    # 4. Warm Diagonal Canopy Sunbeams falling from both arched windows (strictly on open walkable cells!)
    for x0 in (4, 12):
        for y in range(4, 9):
            c = x0 + (y - 4)
            for dx, k in ((0, 'l'), (1, 'full'), (2, 'r')):
                xx = c + dx
                if (4 <= xx <= 14 and rows[y][xx] == '.'
                        and h.L[1, y, xx] in (0, MI(1040), MI(1041), MI(1042), MI(1048), MI(1049), MI(1050), MI(1056), MI(1057), MI(1058))
                        and h.L[2, y, xx] == 0):
                    h.put(CU('light_' + k), xx, y, 2)

    ev_cells = (
        list(g1.KNOT_THREADS) + list(g1.KNOT_TREADLES)
        + [g1.KNOT_AT[k] for k in ('sampler', 'chest', 'lever', 'exit', 'start')]
    )
    PG.guard(h.L, K.TID, ev_cells, 'map 134')
    if save:
        out = os.path.join(HERE, 'data', 'raw', '134.npy')
        np.save(out, h.L)
        print('wrote', out, h.L.shape)
    return h.L


def build_151(save=True):
    """Wave 14 craft of Map 151 (Pell Playhouse Backstage - The Old Revolve, 25x21, Tileset 54).
    Unified 100% with 150 Lobby & 154 Auditorium:
      - Replaces blinding pale white walls with dark Nightbox Art-Deco burgundy-plum opera paneling,
        gilded proscenium beam, Comedy/Tragedy crest over Upstage door (12,2), velvet curtains & sconces
      - Upgrades pitch-black orchestra pit (y=14..15) & central trap pit (y=7) to real sunken stage pits
        with glowing footlights, golden apron glow & retired music stands (all pas=15!)
      - Upgrades flat mauve rear house promenade (y=16..19) to dark crimson-plum Opera Damask carpet,
        Art-Deco gold-filigree promenade frames, royal crimson runner & suspended golden chandeliers
      - Keeps 100% of every puzzle cell, dynamic drop/bridge/flat, rope, ladder & trainer unobstructed!"""
    import hallkit as K
    from puzzles import playhouse as P

    CU, MG, MI, NM = K.CU, K.MG, K.MI, K.NM
    S = P.STAGE
    H, W = len(S), len(S[0])
    cls = {'#': 'void', 'W': 'wall', 'D': 'stair', 'v': 'pit', 'S': 'pit', 'F': 'pit', 'T': 'pit', 'C': 'pit'}
    h = K.Hall(S, 'stage', cls, seed=151)
    rnd = h.r
    BOARDS = [MI(1241), MI(1242), MI(1243)]
    BOARDS_SH = [MI(1233), MI(1234), MI(1235)]

    # 1. Repaint North Wall (y=1..2) to Nightbox Dark Art-Deco Burgundy Paneling & Gilded Proscenium!
    for y in (1, 2):
        for x in range(1, W - 1):
            if S[y][x] == 'W':
                h.put(NM(402) if y == 1 else NM(865), x, y, 0)
            elif S[y][x] == 'D':
                h.put(NM(393) if y == 1 else BOARDS[0], x, y, 0)
                if y == 2:
                    h.put(MG(3151), x, y, 1)
    # Continuous gilded proscenium cornice across y=1 + Comedy/Tragedy crest over Upstage door (12,2)!
    for x in range(1, W - 1):
        h.put(CU('beam_l') if x == 1 else (CU('beam_r') if x == W - 2 else CU('beam_mid')), x, 1, 1)
    h.block([[CU('crest_0'), CU('crest_1'), CU('crest_2')]], 11, 1, 2)
    # Gilded Opera Wall Sconces along north backstage wall (pri=5, non-blocking)
    for sx in (3, 6, 9, 15, 19, 22):
        h.block([[NM(779)], [NM(787)]], sx, 1, 2)
    # Gathered crimson velvet proscenium swags at outer north wings
    for vx in (1, 2, 22, 23):
        if vx in (1, 23):
            h.put(NM(904) if vx == 1 else NM(906), vx, 2, 2)

    # 2. Polish Backstage Floors (y=3..13) + Sunken Trap Pit (y=7) + Sunken Orchestra Pit (y=14..15)
    for y in range(3, 14):
        for x in range(1, W - 1):
            ch = S[y][x]
            if ch in 'vC':
                h.put(CU('pit_%d' % rnd.randrange(3)), x, y, 0)
                h.put(0, x, y, 1)
            elif ch != '#':
                sh = S[y - 1][x] in '#WD'
                h.put(rnd.choice(BOARDS_SH if sh else BOARDS), x, y, 0)
                if ch == 'x':
                    h.put(CU('mark'), x, y, 1)
                elif ch in 'LK':
                    h.put(MG(3151), x, y, 1)

    # Orchestra Pit (y=14..15): sunken darkened pit depth + footlights along y=14 (non-bridge) + retired music stands!
    for y in (14, 15):
        for x in range(1, W - 1):
            ch = S[y][x]
            if ch in 'vSFT':
                h.put(CU('pit_%d' % rnd.randrange(3)), x, y, 0)
                h.put(0, x, y, 1)
                if y == 14 and ch == 'v':
                    h.put(CU('footlight'), x, y, 0)
    # Warm golden footlight halo along the stage apron (y=13) ONLY on open walkable floor cells!
    for x in range(1, W - 1):
        if S[13][x] == '.' and h.L[2, 13, x] == 0:
            h.put(CU('glow'), x, 13, 2)
    # Retired backstage orchestra music stands in darkened pit (y=15, v cells only, pas=15!)
    for mx in (2, 7, 15, 22):
        if S[15][mx] == 'v':
            h.put(CU('music_stand'), mx, 15, 1)

    # 3. Dress Internal Structural Masonry Dividers (#) with Gilded Stage Pilasters & Work-Lantern Sconces (pri=5)!
    for sx, sy in ((9, 5), (9, 10), (15, 5), (15, 10), (10, 3), (14, 3)):
        if S[sy][sx] == '#':
            h.put(NM(787), sx, sy, 2)
            if sy - 1 >= 2 and S[sy - 1][sx] == '#':
                h.put(NM(779), sx, sy - 1, 2)

    # 4. Sumptuous Velvet-and-Gold Central Revolve Stage Dais (x=10..14, y=8..13)!
    #    Base NM(685) dark damask carpet blends 100% seamlessly under NM(1560..1578) gold-filigree border!
    for y in range(8, 14):
        for x in range(10, 15):
            if S[y][x] != '#':
                h.put(NM(685), x, y, 0)
    _put_deco_frame(h, 10, 8, 14, 13, z=1)
    # Keep Rope/Mark/Drop/Flat/Bridge cells 100% clear on layer 1 (only floor '.' gets deco frame)
    for y in range(3, 14):
        for x in range(1, W - 1):
            if S[y][x] in 'sftABCSFT123LKx':
                if S[y][x] == 'x':
                    h.put(CU('mark'), x, y, 1)
                elif S[y][x] in 'LK':
                    h.put(MG(3151), x, y, 1)
                else:
                    h.put(0, x, y, 1)

    # 5. Sumptuous Opera House Rear Promenade (y=16..19): Dark Crimson-Plum Damask + Gold Borders + Royal Runner!
    for y in range(16, 20):
        for x in range(1, W - 1):
            if S[y][x] != '#':
                h.put(NM(685), x, y, 0)
    # Gold-filigree promenade frames zoning West Cue Station & East Stage-Manager Gallery (100% walkable!)
    _put_deco_frame(h, 4, 16, 10, 18, z=1)
    _put_deco_frame(h, 14, 16, 23, 18, z=1)
    # Grand Royal Crimson Ceremonial Runner sweeping up from To the auditorium (12,19) to Forest bridge (12,15)!
    for y in (16, 17, 18):
        r = 0 if y == 16 else (2 if y == 18 else 1)
        for i in range(3):
            h.put(NM([[773, 774, 775], [781, 782, 783], [789, 790, 791]][r][i]), 11 + i, y, 1)
    h.put(NM(782), 12, 19, 1)
    h.obj('mat_mg', 11, 18)
    # Preserve mark at (2, 17) crisply over dark damask carpet
    h.put(CU('mark'), 2, 17, 1)
    # Suspended golden Opera Chandeliers over the West, Center & East House Promenade (pri=5, non-blocking!)
    for cx in (6, 12, 18):
        h.block([[NM(779)], [NM(787)]], cx, 16, 2)

    # 6. Warm Theatrical Spotlight Cones illuminating Center Stage & Upstage Approach (walkable '.' cells only!)
    for sy in (9, 10, 11):
        for sx, k in ((11, 'l'), (12, 'full'), (13, 'r')):
            if S[sy][sx] == '.' and h.L[2, sy, sx] == 0:
                h.put(CU('light_' + k), sx, sy, 2)

    ev_cells = [P.STAGE_AT[k] for k in ('start', 'pip', 'goal', 'ferdie', 'rosalind', 'crewe', 'exit')]
    PG.guard(h.L, K.TID, ev_cells, 'map 151')
    if save:
        out = os.path.join(HERE, 'data', 'raw', '151.npy')
        np.save(out, h.L)
        print('wrote', out, h.L.shape)
    return h.L


def build_152(save=True):
    """Wave 14 craft of Map 152 (Pell Playhouse Backstage - Fly Loft, 25x15, Tileset 54).
    Unified 100% with 150, 151 & 154:
      - Replaces blinding white wall strip with dark Art-Deco burgundy fly-gallery paneling,
        gilded cornice beam, brass sconces & hung painted Act I/II/III drop-tops above battens a/b/c
      - Clean weathered mahogany rigging catwalk with woven crimson fly-runner & crisp batten marks
      - Transforms the giant pitch-black bottom half (y=7..14) into a breathtaking 40-foot aerial
        stage-well vista (100% pas=15!): brass catwalk rail & girder fascia, vertical timber
        rigging columns, color-coded counterweight fly-ropes plunging from both pin-rails, distant
        shadowed stage wings/props/footlights far below, and diagonal amber spotlight shafts!"""
    import hallkit as K
    from puzzles import playhouse as P

    CU, MG, MI, NM = K.CU, K.MG, K.MI, K.NM
    Lf = P.LOFT
    H, W = len(Lf), len(Lf[0])
    h = K.Hall(Lf, 'stage', {'#': 'void', 'W': 'wall'}, seed=152)
    rnd = h.r
    BOARDS = [MI(1241), MI(1242), MI(1243)]
    BOARDS_SH = [MI(1233), MI(1234), MI(1235)]

    # 1. Rich Burgundy-Plum North Fly-Gallery Wall (y=1..2) + Gilded Cornice + Act I-III Hung Drop Tops!
    for x in range(1, W - 1):
        h.put(NM(402), x, 1, 0)
        h.put(NM(865), x, 2, 0)
        h.put(CU('beam_l') if x == 1 else (CU('beam_r') if x == W - 2 else CU('beam_mid')), x, 1, 1)
    # Hung painted drop banners centered right above Flats a (x=6), b (x=11), c (x=16)!
    for bx, dn in ((6, 'ship'), (11, 'forest'), (16, 'throne')):
        h.put(CU('drop_%s_top' % dn), bx, 1, 2)
        h.put(CU('drop_%s_bot' % dn), bx, 2, 2)
    # Brass fly-gallery wall sconces flanking ladders, pin-rails & trapdoor (pri=5)
    for sx in (2, 4, 8, 14, 19, 22):
        h.block([[NM(779)], [NM(787)]], sx, 1, 2)

    # 2. Catwalk Rigging Deck (y=3..6): Warm Weathered Mahogany Boards + Crimson Walk Runner + Batten Marks!
    for y in range(3, 7):
        for x in range(1, W - 1):
            h.put(rnd.choice(BOARDS_SH if y == 3 else BOARDS), x, y, 0)
            h.put(0, x, y, 1)
            h.put(0, x, y, 2)
    # Sleek woven crimson rigging mat along the central catwalk promenade (y=4..5 between batten slots, pas=0!)
    for x0, x1 in ((2, 5), (7, 10), (12, 15), (17, 22)):
        for x in range(x0, x1 + 1):
            c = 0 if x == x0 else (2 if x == x1 else 1)
            h.put(MI([1040, 1041, 1042][c]), x, 4, 1)
            h.put(MI([1056, 1057, 1058][c]), x, 5, 1)
    # Painted batten slot guide marks under moving flats a (x=6), b (x=11), c (x=16)
    for bx in (6, 11, 16):
        for y in range(3, 7):
            h.put(CU('mark'), bx, y, 1)
    # Restore crisp Ladder L/K & Trapdoor hatch tiles on layer 1 (matching gen_playhouse.py)
    for ch in 'LK':
        lx, ly = P.find(Lf, ch)[0]
        h.put(MG(3151), lx, ly, 1)
    tx, ty = P.LOFT_AT['trap']
    h.put(MI(962), tx, ty, 1)

    # 3. Catwalk South Safety Balustrade & Structural Girder Fascia (y=7, ALL pas=15!)
    for x in range(1, W - 1):
        h.put(CU('ledge_face_l') if x == 1 else (CU('ledge_face_r') if x == W - 2 else CU('ledge_face_mid')), x, 7, 0)
        h.put(CU('pit_rail_l') if x == 1 else (CU('pit_rail_r') if x == W - 2 else CU('pit_rail_mid')), x, 7, 1)

    # 4. Breathtaking 40-Foot Deep Aerial Stage-Well Vista Below the Catwalk (y=8..13, x=1..23, ALL pas=15!)
    #    Keep outer perimeter frame (x=0, x=24, y=14) as crisp purple-trimmed Opera void!
    for y in range(8, 14):
        for x in range(1, W - 1):
            if y == 8:
                h.put(CU('lower_1_%d' % rnd.randrange(3)), x, y, 0)
            elif y == 9:
                h.put(CU('lower_2_%d' % rnd.randrange(3)), x, y, 0)
            elif y in (10, 11):
                h.put(CU('lower_3_%d' % rnd.randrange(3)), x, y, 0)
            else:
                h.put(CU('pit_%d' % rnd.randrange(3)), x, y, 0)
            h.put(0, x, y, 1)
            h.put(0, x, y, 2)
    # Crisp purple Opera House outer border casing wrapping the entire aerial well (x=0, x=24, y=14)
    st = K.STYLES['stage']
    for y in range(7, 14):
        h.put(st['edge']['E'], 0, y, 0)
        h.put(st['edge']['W'], W - 1, y, 0)
    for x in range(1, W - 1):
        h.put(st['edge']['N'], x, 14, 0)
    h.put(st['edge']['NE'], 0, 14, 0)
    h.put(st['edge']['NW'], W - 1, 14, 0)

    # Heavy vertical timber rigging piers descending from the catwalk girders (x=1, 6, 11, 16, 23, ALL pas=15!)
    for px in (1, 6, 11, 16, 23):
        for y in range(8, 14):
            tp = 'tpost_band' if y == 8 else ('tpost_base' if y == 13 else 'tpost_mid')
            h.put(CU(tp), px, y, 1)

    # Color-coded counterweight fly-ropes plunging straight down from BOTH counterweight pin-rails (ALL pas=15!)
    for x, col in ((2, 'red'), (3, 'green'), (4, 'gold'), (20, 'red'), (21, 'green'), (22, 'gold')):
        for y in range(8, 14):
            h.put(CU('thread_%s_v' % col), x, y, 2)

    # Distant crimson theatre wing curtains flanking the shadowy stage below (x=5 & x=19, y=8..11, pas=15!)
    for y in range(8, 12):
        h.put(NM(904) if y == 8 else (NM(920) if y == 11 else NM(912)), 5, y, 1)
        h.put(NM(906) if y == 8 else (NM(922) if y == 11 else NM(914)), 19, y, 1)

    # Distant darkened backstage props & scenery crates far down on the shadowed stage floor (y=11..12, pas=15!)
    dim_props = [
        (8, 11, 'dim_19434'), (9, 11, 'dim_19435'), (10, 11, 'dim_19436'),
        (13, 11, 'dim_17872'), (14, 11, 'dim_17873'), (15, 11, 'dim_17889'),
        (17, 11, 'dim_19381'), (17, 12, 'dim_19382'),
        (7, 12, 'music_stand'), (12, 12, 'music_stand'), (18, 12, 'music_stand'),
    ]
    for dx, dy, dn in dim_props:
        h.put(CU(dn), dx, dy, 1)

    # Distant glowing stage footlights along the far auditorium rim (y=13, x=7..18, pas=15!)
    for x in range(7, 19):
        if x not in (11, 16):
            h.put(CU('footlight'), x, 13, 0)

    # Dramatic diagonal amber theatrical spotlights slicing from the catwalk down into the shadowed well (light_*_x pas=15!)
    for x0 in (7, 13):
        for y in range(8, 13):
            c = x0 + (y - 8)
            for dx, k in ((0, 'l'), (1, 'full'), (2, 'r')):
                xx = c + dx
                if 7 <= xx <= 18 and h.L[1, y, xx] == 0 and h.L[2, y, xx] == 0:
                    h.put(CU('light_%s_x' % k), xx, y, 2)

    ev_cells = (
        [P.LOFT_AT[k] for k in ('dot', 'item', 'trap')]
        + P.find(Lf, 'L') + P.find(Lf, 'K')
        + P.find(Lf, '1') + P.find(Lf, '2') + P.find(Lf, '3')
    )
    PG.guard(h.L, K.TID, ev_cells, 'map 152')
    if save:
        out = os.path.join(HERE, 'data', 'raw', '152.npy')
        np.save(out, h.L)
        print('wrote', out, h.L.shape)
    return h.L


def build_153(save=True):
    """Wave 14 craft of Map 153 (Pell Playhouse Backstage - The Trap Room, 20x15, Tileset 54).
    Unified 100% with 150-154:
      - Wraps the playable sub-stage labyrinth in a moody under-stage clockwork cellar & prop
        vault (x=2..17, y=1..13) where EVERY non-playable vault cell stays strictly pas=15!
      - North burgundy-plum cellar masonry wall with gilded rafters & opera sconces
      - West & East sunken mechanical clockwork vaults with spare cogwheels, timber load-bearing
        stage piers, vertical counterweight lines, retired scenery drops & dramatic cellar spotlights
      - Inside the playable labyrinth: gilded Art-Deco velvet-and-brass 5x5 rotating turntable
        (x=7..11, y=5..9), warm mahogany stage corridors, crimson damask entry landing for
        Old Joss (8,11) & Ladder up (9,12), and spotlight over Prop chest (12,3)!"""
    import hallkit as K
    from puzzles import playhouse as P

    CU, MG, MI, NM = K.CU, K.MG, K.MI, K.NM
    T = P.TRAP_AT
    ox, oy = P.TRAP_OFF
    W, H = 20, 15

    # Compute the EXACT playable cell mask (identical to gen_playhouse.py!)
    playable = np.zeros((H, W), dtype=bool)
    for y, r in enumerate(P.TRAP):
        for x, ch in enumerate(r):
            if ch in '.@o*':
                playable[y + oy, x + ox] = True
    tx0, ty0, tn = P.TABLE
    for y in range(ty0, ty0 + tn):
        for x in range(tx0, tx0 + tn):
            playable[y + oy, x + ox] = True
    playable[T['chest'][1] + oy, T['chest'][0] + ox] = True

    rows = [['.' if playable[y, x] else '#' for x in range(W)] for y in range(H)]
    rows = [''.join(r) for r in rows]
    h = K.Hall(rows, 'stage', {'#': 'void'}, seed=153)
    rnd = h.r
    BOARDS = [MI(1241), MI(1242), MI(1243)]
    BOARDS_SH = [MI(1233), MI(1234), MI(1235)]
    st = K.STYLES['stage']

    # 1. Outer Sub-Stage Cellar Architecture & Sunken Clockwork Vaults (x=2..17, y=1..13, STRICTLY pas=15!)
    # North cellar burgundy-plum masonry wall (y=1..2, x=2..17 — NEVER overwriting playable cells!)
    for y in (1, 2):
        for x in range(2, 18):
            if not playable[y, x]:
                h.put(NM(402) if y == 1 else NM(865), x, y, 0)
                if y == 1:
                    h.put(CU('beam_l') if x == 2 else (CU('beam_r') if x == 17 else CU('beam_mid')), x, y, 1)
    # Opera wall sconces & crest along the sub-stage ceiling beam (y=1..2, pri=5)
    for sx in (3, 6, 9, 12, 16):
        h.block([[NM(779)], [NM(787)]], sx, 1, 2)
    h.block([[CU('crest_0'), CU('crest_1'), CU('crest_2')]], 8, 1, 2)

    # West Clockwork Vault (x=2..4, y=3..12) & East Scenery Prop Vault (x=14..17, y=3..12) — ALL pas=15!
    vault_cells = set()
    for y in range(3, 13):
        for x in (2, 3, 4, 14, 15, 16, 17):
            if not playable[y, x]:
                vault_cells.add((x, y))
    for y in (11, 12):
        for x in (5, 6, 12, 13):
            if not playable[y, x]:
                vault_cells.add((x, y))

    for (vx, vy) in vault_cells:
        if vy == 3:
            h.put(CU('lower_1_%d' % rnd.randrange(3)), vx, vy, 0)
            rail = 'pit_rail_l' if vx in (2, 14) else ('pit_rail_r' if vx in (4, 17) else 'pit_rail_mid')
            h.put(CU(rail), vx, vy, 1)
        elif vy in (4, 5):
            h.put(CU('lower_2_%d' % rnd.randrange(3)), vx, vy, 0)
        elif vy in (6, 7, 8):
            h.put(CU('lower_3_%d' % rnd.randrange(3)), vx, vy, 0)
        else:
            h.put(CU('pit_%d' % rnd.randrange(3)), vx, vy, 0)

    # Outer vault boundary casing (x=1, x=18, y=0, y=13) so the entire cellar sits crisply in the void
    for x in range(2, 18):
        h.put(st['edge']['S'], x, 0, 0)
        if not playable[13, x]:
            h.put(st['edge']['N'], x, 13, 0)
    for y in range(1, 13):
        h.put(st['edge']['E'], 1, y, 0)
        h.put(st['edge']['W'], 18, y, 0)
    h.put(st['edge']['SE'], 1, 0, 0)
    h.put(st['edge']['SW'], 18, 0, 0)
    h.put(st['edge']['NE'], 1, 13, 0)
    h.put(st['edge']['NW'], 18, 13, 0)

    # Load-bearing timber stage piers descending through West & East vaults (ALL pas=15!)
    for px in (2, 17):
        for y in range(4, 13):
            tp = 'tpost_band' if y == 4 else ('tpost_base' if y == 12 else 'tpost_mid')
            h.put(CU(tp), px, y, 1)

    # West Vault Mechanical Clockwork: spare turntable gears, counterweight cables & stage crates (ALL pas=15!)
    for gx, gy in ((3, 5), (4, 6), (3, 7), (4, 8), (3, 9)):
        h.put(CU('gear'), gx, gy, 1)
    for y in range(4, 12):
        h.put(CU('thread_gold_v'), 4, y, 2)
    h.put(CU('dim_19381'), 3, 11, 1); h.put(CU('dim_19382'), 3, 12, 1)
    h.put(CU('dim_17872'), 5, 11, 1); h.put(CU('dim_17873'), 6, 11, 1)

    # East Vault Retired Backstage Scenery & Spare Clockwork (ALL pas=15!)
    h.put(CU('drop_ship_top'), 15, 4, 1); h.put(CU('drop_ship_bot'), 15, 5, 1)
    h.put(CU('drop_throne_top'), 16, 4, 1); h.put(CU('drop_throne_bot'), 16, 5, 1)
    for gx, gy in ((14, 7), (15, 8), (14, 9)):
        h.put(CU('gear'), gx, gy, 1)
    for y in range(4, 12):
        h.put(CU('thread_red_v'), 16, y, 2)
    h.put(CU('dim_19434'), 12, 11, 1); h.put(CU('dim_19435'), 13, 11, 1)
    h.put(CU('dim_17889'), 14, 12, 1); h.put(CU('dim_17872'), 15, 11, 1)

    # Diagonal dramatic work-light shafts slicing into both sunken mechanical vaults (light_*_x pas=15!)
    for y in range(4, 9):
        for bx in (3, 14):
            xx = bx + (y - 4) // 2
            if (xx, y) in vault_cells and h.L[2, y, xx] == 0:
                h.put(CU('light_full_x'), xx, y, 2)

    # 2. Enrich Playable Sub-Stage Labyrinth Floors (100% pas=0!)
    for y in range(H):
        for x in range(W):
            if not playable[y, x]:
                continue
            sh = (y > 0 and not playable[y - 1, x])
            h.put(rnd.choice(BOARDS_SH if sh else BOARDS), x, y, 0)

    # Entry Landing (x=8..10, y=10..12): Nightbox dark crimson-plum Opera Carpet + royal crimson runner!
    for y in (10, 11, 12):
        for x in (8, 9, 10):
            if playable[y, x]:
                h.put(NM(685), x, y, 0)
    for y, row_t in ((10, (773, 774, 775)), (11, (781, 782, 783))):
        for i, x in enumerate((8, 9, 10)):
            if playable[y, x]:
                h.put(NM(row_t[i]), x, y, 1)
    # Ladder up (9, 12) crisply preserved!
    lx, ly = T['ladder'][0] + ox, T['ladder'][1] + oy
    h.put(MG(3151), lx, ly, 1)

    # Sumptuous Velvet-and-Gold 5x5 Rotating Turntable Ring (x=7..11, y=5..9)!
    mx0, my0 = tx0 + ox, ty0 + oy
    for y in range(my0, my0 + tn):
        for x in range(mx0, mx0 + tn):
            h.put(NM(685), x, y, 0)
    _put_deco_frame(h, mx0, my0, mx0 + tn - 1, my0 + tn - 1, z=1)
    # Warm crimson hub directly under Brass Crank (9, 7)
    cx, cy = T['crank'][0] + ox, T['crank'][1] + oy
    h.put(MI(1049), cx, cy, 1)
    # Soft spotlight illuminating the secret Prop Chest alcove (11..12, 3..4)
    for sx, sy in ((12, 3), (11, 4), (12, 4)):
        if playable[sy, sx] and h.L[2, sy, sx] == 0:
            h.put(CU('light_full'), sx, sy, 2)

    ev_cells = [
        (cx, cy), (T['chest'][0] + ox, T['chest'][1] + oy),
        (T['joss'][0] + ox, T['joss'][1] + oy), (lx, ly),
        (T['start'][0] + ox, T['start'][1] + oy),
    ]
    PG.guard(h.L, K.TID, ev_cells, 'map 153')
    if save:
        out = os.path.join(HERE, 'data', 'raw', '153.npy')
        np.save(out, h.L)
        print('wrote', out, h.L.shape)
    return h.L


# ==============================================================================
# GROUP 3: ALL 4 TRIAL INTERIORS (Maps 148, 126, 168, 542 — Tileset 34)
# ==============================================================================
def _put_dressed_table(L, x, y, item_l=0, item_r=0):
    """Place intact 2x2 timber craft/tea table on L1 with crisp L2 tabletop items."""
    L[1, y, x] = 3466; L[1, y, x + 1] = 3467
    L[1, y + 1, x] = 3474; L[1, y + 1, x + 1] = 3475
    if item_l:
        L[2, y, x] = item_l
    if item_r:
        L[2, y, x + 1] = item_r


def _put_dressed_workbench(L, x, y, i0=0, i1=0, i2=0):
    """Place intact 3x2 raw-timber workbench on L1 with crisp L2 tools/twine/ledgers."""
    L[1, y, x] = 4082; L[1, y, x + 1] = 4083; L[1, y, x + 2] = 4084
    L[1, y + 1, x] = 4090; L[1, y + 1, x + 1] = 4091; L[1, y + 1, x + 2] = 4092
    for dx, t in enumerate((i0, i1, i2)):
        if t:
            L[2, y, x + dx] = t


def build_148(save=True):
    """Wave 14 craft of Map 148 (Saltmere Lantern House, 20x16, Tileset 34).
    Void-sculpted octagonal weathered-stone coastal vigil & wick-craft sanctuary: maritime
    cobalt carpet anchored by a central lantern-mending & oil-wick worktable with glowing jars,
    coastal charts, oil cask, wick sacks, crystal Lantern rope (8,5) & max 1 standing lamp."""
    W, H = 20, 16
    L = np.zeros((3, H, W), dtype=np.int32)

    # 1. Sculpted Octagonal Stone Vigil Chapel Silhouette
    floor = np.zeros((H, W), dtype=bool)
    floor[5:12, 4:13] = True       # Central sanctuary nave (x=4..12, y=5..11)
    floor[11, 4] = False           # SW octagonal chamfer
    floor[11, 12] = False          # SE octagonal chamfer
    floor[12, 7:10] = True         # Recessed storm-entry vestibule around Exit (8,12)
    floor[6:11, 2:4] = True        # West Vigil Pew Side-Chapel (x=2..3, y=6..10)
    floor[6:11, 13:16] = True      # East Coastal Chart & Oil-Archive Alcove (x=13..15, y=6..10)

    _seam_room(L, floor, style='stone', wall_rows=2)

    # 2. Multi-Zone Weathered Coastal Slate, Timber Nave & Maritime Blue Sanctuary Carpet (distinct from 126!):
    _put_9slice(L, SLATE, 2, 6, 3, 10, z=0)
    _put_9slice(L, SLATE, 13, 6, 15, 10, z=0)
    _put_9slice(L, SLATE, 6, 5, 10, 6, z=0)
    for y in (11, 12):
        for x in (7, 8, 9):
            L[0, y, x] = SLATE[0 if y == 11 else 2][x - 7]
    for i, x in enumerate((7, 8, 9)):
        L[1, 12, x] = 5512 + i
    # Saltmere maritime cobalt-blue woven sanctuary carpet (replaces generic empty red S7 rug!)
    _put_9slice(L, BLUE_CARPET, 6, 7, 10, 10, z=1)

    # 3. Panoramic Coastal Clerestory, Arched Windows & Framed Sea Chart (y=3..4 on nave; y=4..5 on side-chapels)
    _put_grid(L, [[2105, 2108, 2109], [2113, 2116, 2117]], 7, 3, z_rows=(1, 1))
    _put_grid(L, [[2086, 2087], [2094, 2095]], 4, 3, z_rows=(1, 1))
    _put_grid(L, [[2086, 2087], [2094, 2095]], 11, 3, z_rows=(1, 1))
    L[1, 4, 2] = 2105; L[1, 5, 2] = 2113
    # Framed coastal tide & lighthouse chart on East archive wall (13..14, 4..5)
    _put_grid(L, [[4730, 4731], [4738, 4739]], 13, 4, z_rows=(1, 1))
    L[1, 4, 15] = 2105; L[1, 5, 15] = 2113

    # 4. Exact Story Anchors & Lantern-Crafting Craft (100% intact transparent sprites, MAX 1 brass floor lamp!):
    # Lantern rope (8,5): Radiant tall crystal lantern pedestal (2245/2253 -> solid at (8,5))
    L[2, 4, 8] = 2245; L[1, 5, 8] = 2253
    # Single warm indoor brass candle stand on West apse (5, 5) — ZERO mirrored lamp pair!
    L[2, 4, 5] = 2247; L[1, 5, 5] = 2255
    L[1, 5, 6] = 3391                       # Coastal herb offering beside beacon
    # East apse oil-bottle & wick-trimming shelf (10..11, 4..5 -> replaces 2nd mirrored standing lamp!)
    _put_tf(L, 'shelf_bottles', 10, 4)

    # Central Lantern-Display & Wick-Crafting Table breaking up the central carpet (clear of Slate (7,7) & Hollin (9,7)!):
    _put_dressed_table(L, 7, 9, 4528, 4529) # (7..8, 9..10) Glowing amber lantern-oil jar & ruby wick phials!
    L[2, 9, 6] = 4077                       # West wick-crafter's stool on blue carpet
    L[2, 9, 9] = 4077                       # East wick-crafter's stool on blue carpet (leaves y=8 & x=10 wide open!)
    L[1, 8, 4] = 4077                       # Quiet side vigil stool
    L[1, 8, 12] = 4077

    # West Vigil Pew & Wick-Notice Side-Chapel (x=2..4, y=5..10):
    _put_tf(L, 'easel1', 4, 5)              # (4, 5..6) Tide & lantern-watch notice easel
    _put_tf(L, 'bench_v', 2, 6)             # (2, 6..8) Timber vigil pew
    _put_tf(L, 'bookshelf_s', 3, 5)         # (3, 5..6) Vigil ledger shelf flush on stone wall
    L[2, 9, 2] = 5431; L[1, 10, 2] = 5439   # Coastal parlor fern

    # East Coastal Chart, Lamp-Oil & Archive Alcove (x=13..15, y=6..10):
    _put_tf(L, 'barrel_y', 15, 6)           # (15, 6..7) Golden lamp-oil cask
    _put_tf(L, 'bench_v', 15, 8)            # (15, 8..10) East chart-reading bench
    _put_dressed_table(L, 13, 7, 3428, 4546)  # (13..14, 7..8) Open coastal lantern-logbook & folded linen wicks!
    L[1, 10, 13] = 4077                     # Archive reading stool
    L[1, 10, 14] = 4101                     # Oak lamp-trimming bucket

    # Storm-entry braided wick sack & oil pitcher flanking vestibule (replaces half-crate 4168!):
    L[2, 10, 5] = 5475; L[1, 11, 5] = 5483  # Intact tied wick & tallow burlap sack
    L[1, 11, 11] = 5580                     # Keeper's weathered lantern-tool satchel

    PG.guard(L, TID_INT, [(8, 12), (9, 7), (8, 5), (7, 7)], 'map 148')
    if save:
        out = os.path.join(HERE, 'data', 'raw', '148.npy')
        np.save(out, L)
        print('wrote', out, L.shape)
    return L


def build_126(save=True):
    """Wave 14 craft of Map 126 (Briarwick Lantern House, 20x16, Tileset 34).
    Distinct woodland-village botanical glass-chimney lantern workshop (NOT a clone of 148!):
    fringed Nordic woodland rug anchored by a central glass-chimney & botanical sketch worktable,
    dried-herb rack, wood-shaving & herb bales, sunlit emerald conservatory bay, max 1 standing lamp."""
    W, H = 20, 16
    L = np.zeros((3, H, W), dtype=np.int32)

    # 1. Sculpted Hollow-Tree Woodland Conservatory Silhouette
    floor = np.zeros((H, W), dtype=bool)
    floor[5:12, 3:12] = True       # Core hollow-tree workshop sanctuary (x=3..11, y=5..11)
    floor[11, 3] = False           # SW organic tree chamfer
    floor[11, 11] = False          # SE organic tree chamfer
    floor[12, 6:9] = True          # Recessed entry vestibule around Exit (7,12)
    floor[6:11, 2] = True          # West loom-dyer & dried-herb niche (x=2, y=6..10)
    floor[6:11, 12:16] = True      # East Sunlit Loyal-Three Botanical Conservatory Bay (x=12..15, y=6..10)

    _seam_room(L, floor, style='timber', wall_rows=2)

    # 2. Multi-Zone Woodland Timber, Fringed Nordic Woven Rug (distinct from 148!) & Emerald Conservatory Bay:
    for y in range(6, 11):
        for x in range(12, 16):
            L[0, y, x] = FLOOR_GLASS
    # Warm Fringed Nordic Woven Workshop Rug (replaces empty plain red S7 rug!)
    _put_nordic_rug(L, 5, 7, 9, 10, z=1)
    for i, x in enumerate((6, 7, 8)):
        L[1, 12, x] = 5512 + i

    # 3. Sheridan Hollow-Tree Walls, Timber Pilasters & Sunlit Conservatory Windows
    for px in (5, 9):
        L[0, 3, px] = 5548; L[0, 4, px] = 5556
    for wx, wy in ((7, 3), (12, 4), (14, 4)):
        L[0, wy, wx] = 5544; L[0, wy + 1, wx] = 5552
    _put_tf(L, 'painting1', 3, 3)
    L[1, 3, 10] = 5453; L[1, 4, 10] = 5461

    # 4. Exact Story Anchors & Distinct Woodland Botanical Lantern-Workshop Craft (MAX 1 standing lamp!):
    # Mother Aldreth (7,6), Lantern-loom (6,6), Lantern board (10,6) all remain cell_pas=True & reachable via y=7!
    _put_tf(L, 'easel1', 5, 4)              # (5, 4..5) Woven paper-cord lantern loom frame NW of (6,6)
    L[2, 4, 4] = 2245; L[1, 5, 4] = 2253    # Single radiant crystal sanctuary beacon (max 1 standing lamp!)
    L[1, 5, 3] = 3391                       # Potted woodland herb
    _put_tf(L, 'shelf_wood', 9, 4)          # (9..10, 4..5) Lantern-cord & pressed-leaf archive shelf
    L[1, 5, 11] = 7178                      # Blooming briar-rose planter (replaces 2nd standing lamp at 11,5!)

    # Central Glass-Chimney & Botanical Sketch Worktable breaking up the central rug (x=6..7, y=8..9):
    _put_dressed_table(L, 6, 8, 4544, 4548) # (6..7, 8..9) Botanical sketch ledger & glass lantern-chimney vase!
    L[2, 8, 5] = 2604                       # Backed timber workshop chair west of worktable
    L[2, 8, 8] = 2605                       # Backed timber workshop chair east of worktable
    L[2, 10, 7] = 4077                      # Low craftsman's stool south of worktable (leaves y=7 & x=4,9 wide open!)

    # West Loom-Dyer, Dried-Herb & Wood-Shaving Niche (x=2..3, y=6..10):
    _put_grid(L, [[5422], [5430], [5438]], 2, 6, z_rows=(2, 1, 1))  # Hanging dried-herb & flower drying rack!
    L[2, 8, 3] = 5476; L[1, 9, 3] = 5484    # Bundled botanical herb & cedar-shaving bale
    L[1, 10, 2] = 4101                      # Oak dye-water bucket

    # East Sunlit Botanical Conservatory Bay (x=12..15, y=6..10):
    _put_dressed_table(L, 13, 7, 3428, 4528)  # (13..14, 7..8) Open lantern-name ledger & glowing amber oil lamp!
    L[2, 5, 15] = 5431; L[1, 6, 15] = 5439  # Lush emerald fern in NE conservatory corner
    L[2, 9, 15] = 5431; L[1, 10, 15] = 5439 # Matching emerald fern in SE conservatory corner
    L[1, 10, 12] = 4077                     # Conservatory reading stool
    L[1, 6, 12] = 3391                      # Potted woodland sprout

    # Woven cordage & wood-shaving sacks flanking Exit vestibule (replaces half-crate 4168!):
    L[2, 10, 4] = 5475; L[1, 11, 4] = 5483  # Tied cedar-shaving & paper-pulp burlap sack
    L[2, 10, 10] = 5476; L[1, 11, 10] = 5484  # Bundled dried-briar lantern herbs

    PG.guard(L, TID_INT, [(7, 12), (7, 6), (6, 6), (10, 6)], 'map 126')
    if save:
        out = os.path.join(HERE, 'data', 'raw', '126.npy')
        np.save(out, L)
        print('wrote', out, L.shape)
    return L


def build_168(save=True):
    """Wave 14 craft of Map 168 (The Net Loft, 21x17, Tileset 34).
    Authentic Ebbmouth coastal Net-Mender's Loft (ZERO generic red banquet dining room!):
    slate net-hauling wharf bays, weathered oak floor & maritime blue runner, central 3-wide
    raw-timber net-mending workbench w/ twine & tally ledger, coiled hawser rope sacks, fishing
    rods & hanging line poles, cork-float crates, brine/tar barrels, lifebuoy & coastal charts."""
    W, H = 21, 17
    L = np.zeros((3, H, W), dtype=np.int32)

    # 1. Sculpted Ebbmouth Harbor Loft Silhouette
    floor = np.zeros((H, W), dtype=bool)
    floor[5:13, 3:18] = True       # Main harbor loft floor (x=3..17, y=5..12)
    floor[12, 3:5] = False         # SW timber wharf chamfer
    floor[12, 16:18] = False       # SE timber wharf chamfer
    floor[13, 9:12] = True         # Recessed wharf door vestibule around Exit (10,13)
    floor[6:11, 2] = True          # West Net-Hoist & Hawser Bay (x=2, y=6..10)
    floor[6:11, 18] = True         # East Tackle, Rods & Brine-Cask Bay (x=18, y=6..10)

    _seam_room(L, floor, style='timber', wall_rows=2)

    # 2. Multi-Zone Coastal Slate Wharf Aprons, Oak Loft Floor & Maritime Blue Runner (ZERO plain red dining rug!):
    _put_9slice(L, SLATE, 3, 5, 5, 11, z=0)                 # West wet-net & tar-hoist slate apron
    for y in range(6, 11):
        L[0, y, 2] = SLATE[0 if y == 6 else (2 if y == 10 else 1)][0]
    _put_9slice(L, SLATE, 15, 5, 17, 10, z=0)               # East brine-cask & tackle slate apron
    for y in range(6, 11):
        L[0, y, 18] = SLATE[0 if y == 6 else (2 if y == 10 else 1)][2]
    for y in (12, 13):
        for x in (9, 10, 11):
            L[0, y, x] = SLATE[0 if y == 12 else 2][x - 9]
    for i, x in enumerate((9, 10, 11)):
        L[1, 13, x] = 5512 + i
    # Weathered maritime cobalt-blue loft work runner under the net-mending workbenches (x=7..14, y=8..10)
    _put_9slice(L, BLUE_CARPET, 7, 8, 14, 10, z=1)

    # 3. Harbor Loft North Wall: Coastal Charts, Maritime Portholes & Intact 2x2 Lifebuoy (ZERO overlap!):
    for px in (6, 11, 16):
        L[0, 3, px] = 5548; L[0, 4, px] = 5556
    for wx in (5, 10):
        L[0, 3, wx] = 5544; L[0, 4, wx] = 5552
    L[0, 3, 3] = 5560; L[0, 4, 3] = 5568                    # West maritime porthole
    L[0, 3, 17] = 5560; L[0, 4, 17] = 5568                  # East maritime porthole
    _put_grid(L, [[4730, 4731], [4738, 4739]], 8, 3, z_rows=(1, 1))   # Framed coastal chart behind Tally Mast (9,5)
    _put_grid(L, [[4118, 4119], [4126, 4127]], 14, 3, z_rows=(1, 1))  # COMPLETE 2x2 maritime lifebuoy!

    # 4. Exact Story Anchors & Authentic Net-Mender's Craft (100% intact sprites, MAX 1 beacon lamp!):
    # Tally Mast (9,5), Bersi Gullsong (10,6), Tally board (13,6) all remain cell_pas=True!
    _put_tf(L, 'shelf_bottles', 6, 4)                       # (6..7, 4..5) Pitch, varnish & tally bottle shelf
    L[2, 4, 8] = 2245; L[1, 5, 8] = 2253                    # Single radiant crystal beacon flanking Tally Mast (9,5)
    L[1, 5, 11] = 4101                                      # Oak tar & pitch bucket (replaces 2nd standing lamp!)
    _put_tf(L, 'shelf_wood', 12, 4)                         # (12..13, 4..5) Net-tally & twine shelf backing (13,6)

    # Central Long Timber Net-Mending Workbench & Float-Sorting Table (replaces red feast dining room!):
    _put_dressed_workbench(L, 8, 8, 4546, 3428, 4528)       # (8..10, 8..9) Long net-mending bench w/ blue twine, log & oil jar!
    L[2, 9, 7] = 4077                                       # West net-mender's wooden stool
    L[2, 10, 9] = 4077                                      # South net-mender's wooden stool
    L[2, 9, 11] = 4077                                      # Center net-mender's wooden stool
    _put_dressed_table(L, 12, 9, 4548, 4529)                # (12..13, 9..10) Cork-float & wax-seal tally table!
    L[2, 9, 14] = 2605                                      # Backed sailor's chair east of sorting table

    # West Net-Hoist, Coiled Hawser Sacks & Cork-Float Wharf Bay (x=2..6, y=5..11):
    _put_tf(L, 'crates3', 3, 5)                             # (3..5, 5..7) Stacked harbor cork-float & fish crates
    L[2, 5, 2] = 5475; L[1, 6, 2] = 5483                    # Intact tied hawser-rope & net-cordage burlap sack
    L[2, 7, 2] = 5476; L[1, 8, 2] = 5484                    # Bundled dried kelp-cord & trawl netting bale
    _put_tf(L, 'pallet', 2, 9)                              # (2..3, 9..10) Stacked timber wharf cargo pallet
    _put_tf(L, 'crate_i', 5, 9)                             # (5..6, 9..10) Open crate brimming with cork floats & coiled line!
    L[1, 11, 5] = 4101                                      # Oak caulking & pitch bucket
    L[2, 11, 6] = 5475; L[1, 12, 6] = 5483                  # Tied spare net-mending twine sack by door

    # East Tackle, Hanging Line Poles, Brine Casks & Sailor's Sea Chest (x=15..18, y=5..11):
    L[2, 4, 16] = 4823; L[1, 5, 16] = 4831                  # Tall salt-brine barrel
    L[2, 4, 17] = 4822; L[1, 5, 17] = 4830                  # Tall pine-tar & oil cask
    _put_tf(L, 'rodbucket', 18, 6)                          # (18, 6..7) Bundle of Ebbmouth fishing rods & gaffs!
    L[2, 6, 17] = 4061; L[1, 7, 17] = 4069                  # Hanging fishing-line & float-rigging pole beside rods!
    _put_tf(L, 'crate_i2', 15, 7)                           # (15..16, 7..8) Dyed buoy-flag & colored float crate!
    _put_grid(L, [[5584, 5585, 5586], [5592, 5593, 5594]], 16, 9, z_rows=(1, 1))  # 3-wide iron-bound maritime sea chest!
    L[1, 12, 14] = 5580                                     # Rigger's leather marlinspike & needle satchel!

    PG.guard(L, TID_INT, [(10, 13), (10, 6), (9, 5), (13, 6)], 'map 168')
    if save:
        out = os.path.join(HERE, 'data', 'raw', '168.npy')
        np.save(out, L)
        print('wrote', out, L.shape)
    return L


def build_542(save=True):
    """Wave 14 craft of Map 542 (The Brinewife's Rest, 20x16, Tileset 34).
    Void-sculpted storm-weathered stone-and-timber marsh wayside inn with twin tucked-in
    sleeper bunk alcoves, simmering salt-broth stone hearth kitchenette, crimson hearth carpet
    & guestbook table below Rest house keeper (9,7), warm bedside candle stands & marsh ferns."""
    W, H = 20, 16
    L = np.zeros((3, H, W), dtype=np.int32)

    # 1. Sculpted Stone-and-Timber Marsh Wayside Refuge Silhouette
    floor = np.zeros((H, W), dtype=bool)
    floor[5:12, 3:14] = True       # Core hearth lodge (x=3..13, y=5..11)
    floor[11, 3:5] = False         # SW stone lodge chamfer
    floor[11, 12:14] = False       # SE stone lodge chamfer
    floor[12, 7:10] = True         # Recessed storm-porch vestibule around Exit (8,12)
    floor[6:10, 2] = True          # West Traveler's Bunk Alcove (x=2, y=6..9)
    floor[6:10, 14:16] = True      # East Traveler's Bunk Alcove (x=14..15, y=6..9)

    _seam_room(L, floor, style='stone', wall_rows=2)

    # 2. Multi-Zone Stone Mudroom, Hearth Apron, Warm Timber & Crimson Hearth Carpet
    _put_9slice(L, SLATE, 6, 5, 10, 6, z=0)
    for y in (11, 12):
        for x in (7, 8, 9):
            L[0, y, x] = SLATE[0 if y == 11 else 2][x - 7]
    for i, x in enumerate((7, 8, 9)):
        L[1, 12, x] = 5512 + i
    # Cozy crimson braided hearth carpet (6..10, 8..10) right below Rest house keeper (9,7)!
    _put_9slice(L, SHER_RUG, 6, 8, 10, 10, z=1)

    # 3. Weathered Stone North Wall Windows & Clean Overhead Marsh Trail Map (ZERO kitchen overlap!)
    _put_grid(L, [[2086, 2087], [2094, 2095]], 4, 3, z_rows=(1, 1))
    _put_grid(L, [[2086, 2087], [2094, 2095]], 11, 3, z_rows=(1, 1))
    _put_tf(L, 'map_wall', 7, 3)                                      # 1-row marsh trail chart cleanly above kitchen!
    L[1, 4, 2] = 2105; L[1, 5, 2] = 2113                              # West alcove glass casement (zero beige panel!)
    L[1, 4, 15] = 2105; L[1, 5, 15] = 2113                            # East alcove glass casement

    # 4. Cozy Wayside Healing Refuge Props (100% intact sprites, wide circulation around Keeper (9,7)!)
    _put_tf(L, 'kitchen', 6, 4)
    _put_tf(L, 'shelf_bottles', 10, 4)
    # West Sleeper Alcove: warm orange traveler's bunk (3..4, 5..7), bedside candle stand (2, 7..8), satchel (2, 9) & barrel!
    _put_tf(L, 'bunk_o', 3, 5)
    L[1, 6, 2] = 3391                        # marsh-herb drying pot
    L[2, 7, 2] = 2247; L[1, 8, 2] = 2255    # warm bedside indoor candle stand
    L[1, 9, 2] = 5580                        # traveler's leather pack
    L[2, 9, 3] = 4822; L[1, 10, 3] = 4830   # salt-brine barrel (leaves (3..4, 8) open beside bunk!)
    # East Sleeper Alcove: cool blue traveler's bunk (12..13, 5..7), supply crate (14..15, 5..6), fern & candle stand!
    _put_tf(L, 'bunk_b', 12, 5)
    _put_tf(L, 'crate_i', 14, 5)             # (14..15, 5..6) spare marsh wool & rations trunk
    L[2, 7, 15] = 2247; L[1, 8, 15] = 2255  # warm east bedside candle stand
    L[2, 8, 14] = 5431; L[1, 9, 14] = 5439  # intact marsh fern palm
    L[1, 9, 15] = 4101                       # rainwater bucket
    # Central Salt-Broth Table on crimson hearth carpet (7..8, 8..9) + guestbook + stools!
    _put_tf(L, 'table_dark', 7, 8)
    L[2, 8, 7] = 3428                        # open marsh wayfarers' guestbook on table!
    L[2, 9, 6] = 4077                        # stool west of broth table
    L[2, 9, 9] = 4077                        # stool east of broth table
    # Storm-porch entry welcome accents (no outdoor street lamps!)
    L[1, 11, 5] = 4101                       # boot-wash brine bucket
    L[1, 11, 11] = 5580                      # traveler's spare pack
    L[1, 10, 4] = 3391
    L[1, 10, 12] = 4168                      # coiled marsh-rope basket

    PG.guard(L, TID_INT, [(8, 12), (9, 7)], 'map 542')
    if save:
        out = os.path.join(HERE, 'data', 'raw', '542.npy')
        np.save(out, L)
        print('wrote', out, L.shape)
    return L


# ==============================================================================
# YAML SPEC UPDATERS (110 in 109_dovetail.yaml; 148/126/168/542 in 148_trial_interiors.yaml)
# (Note: 132, 134, 151, 152, 153 are automatically updated via hallkit.py -> gen_loomhouse/gen_playhouse!)
# ==============================================================================
def update_yaml_110():
    spec_path = os.path.join(HERE, 'specs', '109_dovetail.yaml')
    with open(spec_path, 'r', encoding='utf-8') as f:
        text = f.read()
    raw_docs = text.split('\n---\n')
    out_docs = []
    updated = False
    for chunk in raw_docs:
        doc = yaml.safe_load(chunk)
        if doc and doc.get('id') == 110:
            new_doc = {
                'id': 110,
                'name': doc['name'],
                'parent': doc['parent'],
                'bgm': doc['bgm'],
                'metadata': doc['metadata'],
                'tone': [12, 4, -12, 0],
                'biome': doc['biome'],
                'raw': 'data/raw/110.npy',
                'tileset': TID_INT,
                'events': doc['events'],
            }
            out_docs.append(yaml.safe_dump(new_doc, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True).rstrip())
            updated = True
        else:
            out_docs.append(chunk)
    assert updated, 'Map 110 not found in 109_dovetail.yaml'
    with open(spec_path, 'w', encoding='utf-8') as f:
        f.write('\n---\n'.join(out_docs))
        if not out_docs[-1].endswith('\n'):
            f.write('\n')
    print('updated Map 110 in', spec_path)


def update_yaml_trial_interiors():
    spec_path = os.path.join(HERE, 'specs', '148_trial_interiors.yaml')
    with open(spec_path, 'r', encoding='utf-8') as f:
        text = f.read()
    tones = {
        148: [10, 5, -8, 2],
        126: [8, 7, -10, 0],
        168: [8, 4, -8, 4],
        542: [14, 6, -12, 0],
    }
    raw_docs = text.split('\n---\n')
    out_docs = []
    updated = set()
    for i, chunk in enumerate(raw_docs):
        doc = yaml.safe_load(chunk)
        if doc and doc.get('id') in tones:
            mid = doc['id']
            new_doc = {
                'id': mid,
                'name': doc['name'],
                'parent': doc['parent'],
                'bgm': doc['bgm'],
                'metadata': doc.get('metadata', {}),
                'tone': tones[mid],
                'biome': doc.get('biome', 'interior'),
                'raw': f'data/raw/{mid}.npy',
                'tileset': TID_INT,
                'events': doc['events'],
            }
            dumped = yaml.safe_dump(new_doc, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True).rstrip()
            if i == 0:
                dumped = '# Trial interiors 148 / 126 / 168 / 542. Wave 14 Rejuvenation V14 craft (wave14_setpieces_craft.py).\n' + dumped
            out_docs.append(dumped)
            updated.add(mid)
        else:
            out_docs.append(chunk)
    assert updated == {148, 126, 168, 542}, f'Expected 4 trial interiors, got {updated}'
    with open(spec_path, 'w', encoding='utf-8') as f:
        f.write('\n---\n'.join(out_docs))
        if not out_docs[-1].endswith('\n'):
            f.write('\n')
    print('updated Maps 148, 126, 168, 542 in', spec_path)


# ==============================================================================
# HALLKIT HOOK + CLI ENTRYPOINT
# ==============================================================================
BUILDERS = {
    109: build_109,
    110: build_110,
    132: build_132,
    134: build_134,
    151: build_151,
    152: build_152,
    153: build_153,
    148: build_148,
    126: build_126,
    168: build_168,
    542: build_542,
}


def apply_craft(mid, L_out):
    """Apply Wave 14 craft in-place inside hallkit.Hall.write() for 132, 134, 151, 152, 153."""
    fn = {132: build_132, 134: build_134, 151: build_151, 152: build_152, 153: build_153}.get(mid)
    if fn is not None:
        L_out[:] = fn(save=False)


def main(which=None):
    os.makedirs(os.path.join(HERE, 'data', 'raw'), exist_ok=True)
    sel = {int(a) for a in (which or [])}
    for mid, fn in BUILDERS.items():
        if not sel or mid in sel:
            fn(save=True)
    if not sel or 110 in sel:
        update_yaml_110()
    if not sel or bool(sel & {148, 126, 168, 542}):
        update_yaml_trial_interiors()


if __name__ == '__main__':
    main(sys.argv[1:])
