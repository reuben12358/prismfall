#!/usr/bin/env python3
"""layouts/wave15_act1_interiors_craft.py - Wave 15 Rejuvenation V14 Redesign of ALL 20 Act I Town Interiors
(Ferrow's Landing, Briarwick & Gossamer Wood, Saltmere, Ebbmouth) on Tileset 34 ("Prismfall Interior").

20 Exclusive Target Maps (ZERO overlap with Waves 12-14, ZERO edits to 103/105/106/108/145):
  Ferrow's Landing (Warm Coastal Timber, Cream Wainscot & Lantern Glow):
    - 101 Ferrow's Landing Pokémon Center (20x17)
    - 102 Ferrow's Landing Mart           (20x16)
    - 104 Tidewater Inn                   (21x18)
    - 107 Dockmaster's House              (20x16)
  Briarwick & Gossamer Wood (Silk-Loom Cedar, Blossom Shoji, Bonsai & Hearth):
    - 121 Briarwick Pokémon Center        (20x17)
    - 122 Briarwick Mart                  (20x16)
    - 123 Weavers' Guildhall + Loft       (41x18)
    - 124 Treetop House + Chapel          (40x18)
    - 125 Cutter's House                  (20x16)
    - 523 Hale Farmhouse                  (21x17)
    - 526 Woodward's Hut                  (20x16)
  Saltmere (Theatrical Crimson-Brass, Chrisola Marble, Velvet Curtains & Grand Piano):
    - 141 Saltmere Pokémon Center         (15x10, upgraded from stock Gen-3 template!)
    - 142 Saltmere Mart                   (11x9,  upgraded from stock Gen-3 template!)
    - 143 Saltmere Harbour Office         (23x17)
    - 144 Saltwife's House                (20x16)
  Ebbmouth (Weathered Maritime Stonework, Coastal Slate, Blue-Steel Counters & Ocean Rugs):
    - 161 Ebbmouth Pokémon Center         (15x10, upgraded from stock Gen-3 template!)
    - 162 Ebbmouth Mart                   (11x9,  upgraded from stock Gen-3 template!)
    - 163 Anglers' Guild                  (13x10, upgraded from stock Gen-3 template!)
    - 164 Reyes House                     (10x9,  upgraded from stock Gen-3 template!)
    - 165 Net-mender's House              (10x9,  upgraded from stock Gen-3 template!)

Writes mapgen/data/raw/{id}.npy for all 20 maps and wires their 5 spec files while preserving 100% of HEAD
Event IDs (EvID_exact), Nurse Joy / Mart clerk / PC / Town Map template events, warps, and untouched maps
(103, 105, 106, 108, 145).
"""
import os
import sys
import numpy as np
import yaml

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import passguard as PG
from interiorkit import TF

TID = 34
VOID = 5437
FLOOR_GLASS = 501  # Luminous emerald-diamond botanical floor tile

# ---------------------------------------------------------------------------
# Verified 9-Slice Floors & Rugs on Tileset 34 (all p=00, r=0)
# ---------------------------------------------------------------------------
CREAM_STONE = [
    [5920, 5921, 5922],
    [5928, 5929, 5930],
    [5936, 5937, 5938],
]
BLUE_STONE = [
    [5768, 5769, 5770],
    [5776, 5777, 5778],
    [5784, 5785, 5786],
]
SLATE_STONE = [
    [1152, 1153, 1154],
    [1152, 1153, 1154],
    [1160, 1161, 1162],
]
HOTEL_MARBLE = [
    [7752, 7753, 7754],
    [7760, 7761, 7762],
    [7768, 7769, 7770],
]
SHER_RUG = [
    [5411, 5412, 5413],
    [5419, 5420, 5421],
    [5427, 5428, 5429],
]
HOTEL_CRIMSON_RUG = [
    [7172, 7173, 7174],
    [7180, 7181, 7182],
    [7188, 7189, 7190],
]
BLUE_MARITIME_RUG = [
    [7496, 7497, 7498],
    [7504, 7505, 7506],
    [7512, 7513, 7514],
]

# ---------------------------------------------------------------------------
# Verified Multi-Tile Stamps (visually proofed from ts34_sheets/stamp_proof.png)
# ---------------------------------------------------------------------------
LOFT_STAIRS = [
    [5675, 5676, 5677],
    [5683, 5684, 5685],
    [5691, 5692, 5693],
    [5699, 5700, 5701],
]
SHER_BOOKCASE = [
    [5350, 5351],
    [5358, 5359],
    [5366, 5367],
]
SHER_CHEST = [
    [5584, 5585, 5586],
    [5592, 5593, 5594],
]
SHER_DESK = [
    [5694, 5695],
    [5702, 5703],
]
HOTEL_DESK_BOOKS = [
    [7384, 7385],
    [7392, 7393],
]
SOFA_BLK = [
    [5581, 5582, 5583],
    [5589, 5590, 5591],
]
SOFA_GREY = [
    [6024, 6025, 6026],
    [6032, 6033, 6034],
]
WOOD_BENCH = [
    [7875, 7876, 7877],
    [7883, 7884, 7885],
]
FLOWER_CART = [
    [5446, 5447],
    [5454, 5455],
]
BULLETIN_BOARD = [
    [5795, 5796, 5797],
    [5803, 5804, 5805],
]
HELP_HEAL = [
    [6035, 6036],
    [6043, 6044],
]
GRAND_PIANO = [
    [7336, 7337, 7338],
    [7344, 7345, 7346],
    [7352, 7353, 7354],
]
SHOJI_BLOSSOM = [
    [8547, 8548, 8549],
    [8555, 8556, 8557],
]
BONSAI = [
    [8571, 8572],
    [8579, 8580],
]
HOTEL_PORTRAIT = [
    [7356, 7357],
    [7364, 7365],
]
HOTEL_FLOWER_STAND = [
    [7375],
    [7383],
    [7391],
]
HOTEL_VASE = [
    [7558],
    [7566],
]
HOTEL_RED_WINDOW = [
    [7124, 7125],
    [7132, 7133],
]
COASTAL_ARCH_WIN = [
    [2086, 2087],
    [2094, 2095],
]
SEA_CHART = [
    [4730, 4731],
    [4738, 4739],
]
SHER_BED_FULL = [
    [5597, 5598, 5599],
    [5605, 5606, 5607],
    [5613, 5614, 5615],
]
SHER_BED_SINGLE = [
    [5330, 5331],
    [5338, 5339],
    [5346, 5347],
]


# ---------------------------------------------------------------------------
# Painting & Seaming Primitives
# ---------------------------------------------------------------------------
def _put_tf(L, name, x, y):
    rows, top = TF[name]
    H, W = L.shape[1:]
    for dy, row in enumerate(rows):
        for dx, t in enumerate(row):
            if not t:
                continue
            yy, xx = y + dy, x + dx
            if not (0 <= yy < H and 0 <= xx < W):
                continue
            z = 2 if dy < top else 1
            if z == 1 and L[1, yy, xx]:
                z = 2
            L[z, yy, xx] = t


def _put_grid(L, grid, x, y, z_rows=None):
    H, W = L.shape[1:]
    for dy, row in enumerate(grid):
        z_def = z_rows[dy] if z_rows is not None else 1
        for dx, t in enumerate(row):
            if not t:
                continue
            yy, xx = y + dy, x + dx
            if not (0 <= yy < H and 0 <= xx < W):
                continue
            z = z_def
            if z == 1 and L[1, yy, xx]:
                z = 2
            L[z, yy, xx] = t


def _put_9slice(L, tiles9, x0, y0, x1, y1, z=0, mask=None):
    H, W = L.shape[1:]
    for y in range(max(0, y0), min(H, y1 + 1)):
        ry = 0 if y == y0 else (2 if y == y1 else 1)
        for x in range(max(0, x0), min(W, x1 + 1)):
            if mask is not None and not mask[y, x]:
                continue
            rx = 0 if x == x0 else (2 if x == x1 else 1)
            L[z, y, x] = tiles9[ry][rx]


def _put_tree(L, x, y, style='parlor'):
    """Intact 1x2 indoor parlor tree (top z=2, pot z=1 -> ZERO clipping!)."""
    pairs = {
        'parlor': (5415, 5423),
        'fern': (5431, 5439),
        'ficus': (7126, 7134),
        'palm': (7874, 7882),
    }
    top_t, bot_t = pairs[style]
    H, W = L.shape[1:]
    if 0 <= y < H and 0 <= x < W:
        L[2, y, x] = top_t
    if 0 <= y + 1 < H and 0 <= x < W:
        L[1, y + 1, x] = bot_t


def _doormat(L, cx, y):
    """3-wide Sheridan entry doormat centered on cx at row y."""
    H, W = L.shape[1:]
    for i, x in enumerate((cx - 1, cx, cx + 1)):
        if 0 <= y < H and 0 <= x < W:
            L[1, y, x] = 5512 + i


def _sher_window(L, x, y_top):
    """Sheridan arched harbour/woodland window on 2-row wall face."""
    L[0, y_top, x] = 5544
    L[0, y_top + 1, x] = 5552


def _sher_porthole(L, x, y_top):
    """Maritime diamond porthole on 2-row wall face."""
    L[0, y_top, x] = 5560
    L[0, y_top + 1, x] = 5568


def _sher_pilaster(L, x, y_top):
    """Vertical Sheridan timber wall pilaster."""
    L[0, y_top, x] = 5548
    L[0, y_top + 1, x] = 5556


def _seam_room(L, floor, wall_style='sheridan', floor_style='oak', wall_rows=2):
    """Auto-seam a void-sculpted interior room (or multi-room mask) on Tileset 34."""
    H, W = floor.shape
    L[0, :, :] = VOID

    wall_face = np.zeros((H, W), dtype=bool)
    for y in range(1, H):
        for x in range(0, W):
            if floor[y, x] and not floor[y - 1, x]:
                for k in range(1, wall_rows + 1):
                    if y - k >= 0 and not floor[y - k, x]:
                        wall_face[y - k, x] = True

    interior = floor | wall_face

    for y in range(H):
        for x in range(W):
            if floor[y, x]:
                top_row = (y == 0) or (not floor[y - 1, x])
                left_edge = (x == 0) or (not floor[y, x - 1])
                right_edge = (x + 1 >= W) or (not floor[y, x + 1])
                bot_edge = (y + 1 >= H) or (not floor[y + 1, x])
                if floor_style == 'oak':
                    if top_row:
                        L[0, y, x] = 5352 if left_edge else 5353 + (x - 3) % 3
                    else:
                        L[0, y, x] = 5360 if left_edge else 5361 + (x - 3) % 3
                elif floor_style == 'slate':
                    ry = 0 if top_row else (2 if bot_edge else 1)
                    rx = 0 if left_edge else (2 if right_edge else 1)
                    L[0, y, x] = SLATE_STONE[ry][rx]
                elif floor_style == 'marble':
                    ry = 0 if top_row else (2 if bot_edge else 1)
                    rx = 0 if left_edge else (2 if right_edge else 1)
                    L[0, y, x] = HOTEL_MARBLE[ry][rx]
            elif wall_face[y, x]:
                is_lower = (y + 1 < H and floor[y + 1, x])
                left_end = (x == 0) or (not wall_face[y, x - 1])
                right_end = (x + 1 >= W) or (not wall_face[y, x + 1])
                if wall_style == 'stone':
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


def _finalize(L, mid, event_cells=()):
    PG.guard(L, TID, event_cells, f'map {mid}')
    return L


# ===========================================================================
# GROUP A: FERROW'S LANDING (101, 102, 104, 107) — Warm Coastal Timber
# ===========================================================================

def build_101():
    """101: Ferrow's Landing Pokémon Center (20x17).
    Events: #2 Nurse (9,5), #3 PC (13,5), #4 Healing balls (7,5), #5 Exit (9,13), #6 Trainer at PC (13,10).
    """
    W, H = 20, 17
    L = np.zeros((3, H, W), dtype=np.int32)
    floor = np.zeros((H, W), dtype=bool)
    floor[5:13, 3:17] = True       # Main coastal timber center x=3..16, y=5..12
    floor[4, 6:12] = True          # Stepped north healing apse x=6..11, y=4
    floor[12, 3:5] = False         # SW chamfer
    floor[12, 15:17] = False       # SE chamfer
    floor[13, 8:11] = True         # Recessed entry vestibule around Exit (9,13)
    _seam_room(L, floor, wall_style='sheridan', floor_style='oak')

    # Floor zoning: weathered coastal slate vestibule pad + ornate crimson-gold arrival runner + cozy east lounge rug!
    _put_9slice(L, SLATE_STONE, 8, 12, 10, 13, z=0, mask=floor)
    _put_9slice(L, HOTEL_CRIMSON_RUG, 8, 7, 10, 11, z=1, mask=floor)
    _put_9slice(L, SHER_RUG, 12, 8, 15, 11, z=1, mask=floor)
    _doormat(L, 9, 13)

    # North wall architectural details: harbour arched windows, diamond portholes, pilasters, coastal chart
    _sher_window(L, 7, 2)
    _sher_window(L, 10, 2)
    _sher_pilaster(L, 8, 2)
    _sher_pilaster(L, 9, 2)
    _sher_porthole(L, 4, 3)
    _sher_window(L, 15, 3)
    _put_tf(L, 'map_wall', 3, 3)
    L[1, 2, 8] = 5453; L[1, 3, 8] = 5461

    # Healing apse: Rejuv heal pod at (6..7, 4..5) -> solid on Healing balls (7,5)!
    _put_grid(L, HELP_HEAL, 6, 4, z_rows=(2, 1))
    # Seamless Sheridan mahogany + pink-blossom reception counter wrapping Nurse (9,5)!
    L[1, 5, 11] = 5658  # East wing blossom return (p=8f)
    for x, t in ((7, 5664), (8, 5665), (9, 5665), (10, 5665), (11, 5666)):
        L[1, 6, x] = t  # ALL 0x80 counter tiles!
    # Clean compact 2-row PC terminal at (13, 4..5) (ZERO ceiling clip!) + bulletin board cleanly at (14..16, 3..4)
    L[2, 4, 13] = 5959; L[1, 5, 13] = 5967
    _put_grid(L, BULLETIN_BOARD, 14, 3, z_rows=(1, 1))

    # West timber reading & tea nook (x=3..6, y=5..11)
    _put_grid(L, SHER_BOOKCASE, 4, 4, z_rows=(2, 1, 1))
    _put_grid(L, SOFA_BLK, 3, 8, z_rows=(2, 1))
    _put_tf(L, 'table_tea', 4, 10)
    L[1, 11, 6] = 4077
    # East trainer lounge (clear of Trainer at PC @ (13,10)!)
    _put_tf(L, 'table_dark', 14, 7)
    L[2, 7, 14] = 3428
    L[1, 9, 15] = 4077
    _put_grid(L, FLOWER_CART, 15, 5, z_rows=(2, 1))
    L[1, 12, 12] = 5580
    # Intact parlor trees
    _put_tree(L, 3, 5, 'parlor')
    _put_tree(L, 16, 10, 'fern')
    _put_tree(L, 6, 11, 'ficus')
    L[1, 12, 11] = 3391

    return _finalize(L, 101, [(9, 5), (13, 5), (7, 5), (9, 13), (13, 10)])


def build_102():
    """102: Ferrow's Landing Mart (20x16).
    Events: #2 Mart (4,5), #3 Exit (8,12), #4 Shopper (10,10).
    """
    W, H = 20, 16
    L = np.zeros((3, H, W), dtype=np.int32)
    floor = np.zeros((H, W), dtype=bool)
    floor[5:12, 3:16] = True
    floor[11, 3:5] = False
    floor[11, 14:16] = False
    floor[5, 15] = False
    floor[12, 7:10] = True
    _seam_room(L, floor, wall_style='sheridan', floor_style='oak')

    # Floor zoning: warm coastal oak planks + slate entry pad + braided crimson aisle rug (ZERO white glare!)
    _put_9slice(L, SLATE_STONE, 7, 11, 9, 12, z=0, mask=floor)
    _put_9slice(L, SHER_RUG, 7, 7, 11, 10, z=1, mask=floor)
    _doormat(L, 8, 12)

    # North wall features
    _sher_window(L, 7, 3)
    _sher_window(L, 12, 3)
    _sher_porthole(L, 4, 3)
    _put_tf(L, 'map_wall', 8, 3)
    _put_tf(L, 'shelf_bottles', 5, 4)

    # Seamless Sheridan mahogany checkout counter wrapping Mart (4,5) -> ALL 0x80 counter!
    L[1, 5, 6] = 5658
    for x, t in ((3, 5664), (4, 5665), (5, 5665), (6, 5666)):
        L[1, 6, x] = t
    # Stocked coastal goods shelves & synthetic seed display
    _put_tf(L, 'shelf_goods', 9, 4)
    _put_tf(L, 'shelf_goods', 12, 4)
    _put_tf(L, 'shelf_green', 8, 8)
    _put_tf(L, 'shelf_green', 12, 8)
    _put_tf(L, 'display', 4, 8)
    _put_tf(L, 'crate_i', 12, 10)
    _put_tf(L, 'barrel_y', 14, 6)
    _put_tf(L, 'barrel_b', 14, 8)
    _put_tf(L, 'bucket', 6, 10)
    _put_tree(L, 3, 9, 'fern')
    _put_tree(L, 14, 9, 'parlor')
    L[1, 11, 10] = 3391

    return _finalize(L, 102, [(4, 5), (8, 12), (10, 10)])


def build_104():
    """104: Tidewater Inn (21x18).
    Events: #1 Exit (10,14), #2 Innkeeper (4,6), #3 Inn Guest (8,11), #4 Inn Guest 2 (13,7).
    """
    W, H = 21, 18
    L = np.zeros((3, H, W), dtype=np.int32)
    floor = np.zeros((H, W), dtype=bool)
    floor[5:14, 3:18] = True
    floor[13, 3:5] = False
    floor[13, 16:18] = False
    floor[14, 9:12] = True
    _seam_room(L, floor, wall_style='sheridan', floor_style='oak')

    # Floor zoning: coastal slate hearth kitchen + grand crimson-gold dining rug + east guest carpet
    _put_9slice(L, SLATE_STONE, 10, 5, 14, 6, z=0, mask=floor)
    _put_9slice(L, HOTEL_CRIMSON_RUG, 7, 8, 13, 12, z=1, mask=floor)
    _put_9slice(L, SHER_RUG, 14, 8, 17, 11, z=1, mask=floor)
    _doormat(L, 10, 14)

    for wx in (6, 10, 15):
        _sher_window(L, wx, 3)
    _sher_pilaster(L, 8, 3)
    _sher_pilaster(L, 13, 3)
    _put_tf(L, 'painting3', 4, 3)
    _put_tf(L, 'clock', 7, 3)
    _put_tf(L, 'shelf_bottles', 5, 4)

    # Seamless Sheridan innkeeper counter wrapping Innkeeper (4,6)
    L[1, 6, 6] = 5658
    for x, t in ((3, 5664), (4, 5665), (5, 5665), (6, 5666)):
        L[1, 7, x] = t
    _put_tf(L, 'kitchen', 11, 4)
    _put_tf(L, 'food_table', 9, 5)
    _put_tf(L, 'dining', 9, 8)
    L[2, 9, 8] = 4077
    L[2, 10, 12] = 4077
    L[2, 8, 12] = 4077

    # COMPLETE 3x3 Sheridan mahogany guest beds with headboards on east alcove!
    _put_grid(L, SHER_BED_FULL, 15, 5, z_rows=(2, 1, 1))   # North guest bed (15..17, 5..7)
    _put_grid(L, SHER_BED_FULL, 15, 9, z_rows=(2, 1, 1))   # South guest bed (15..17, 9..11)
    L[1, 8, 17] = 5580
    L[1, 12, 15] = 5580
    _put_tf(L, 'bunk_b', 3, 9)
    _put_grid(L, SHER_CHEST, 5, 12, z_rows=(2, 1))
    _put_tf(L, 'barrel_y', 13, 12)
    _put_tree(L, 14, 12, 'fern')
    _put_tree(L, 3, 4, 'ficus')
    L[1, 13, 8] = 3391

    return _finalize(L, 104, [(10, 14), (4, 6), (8, 11), (13, 7)])


def build_107():
    """107: Dockmaster's House (20x16).
    Events: #1 Exit (8,12), #2 Dockmaster (5,7), #3 Dockmaster's ledger (7,5).
    """
    W, H = 20, 16
    L = np.zeros((3, H, W), dtype=np.int32)
    floor = np.zeros((H, W), dtype=bool)
    floor[5:12, 3:16] = True
    floor[11, 3:5] = False
    floor[11, 14:16] = False
    floor[12, 7:10] = True
    _seam_room(L, floor, wall_style='sheridan', floor_style='oak')

    # Floor zoning: neat slate freight corner (3..5, 8..10) + warm braided study rug (7..10, 7..10)
    _put_9slice(L, SLATE_STONE, 3, 8, 5, 10, z=0, mask=floor)
    _put_9slice(L, SHER_RUG, 7, 7, 10, 10, z=1, mask=floor)
    _doormat(L, 8, 12)

    _sher_porthole(L, 4, 3)
    _sher_window(L, 10, 3)
    _put_tf(L, 'map_wall', 6, 3)
    _put_tf(L, 'lifering', 11, 3)

    # Dockmaster's office: desk north of Dockmaster (5,7), ledger desk cleanly at (7..8, 5..6) -> Dockmaster's ledger (7,5)!
    _put_grid(L, SHER_BOOKCASE, 3, 3, z_rows=(2, 1, 1))   # Tall shipping archive bookcase NW (3..4, 3..5)
    _put_grid(L, SHER_DESK, 7, 4, z_rows=(2, 1))          # Ledger desk (7..8, 4..5) cleanly on Dockmaster's ledger (7,5)!
    L[2, 5, 7] = 3428                                     # Open unscheduled crossing ledger on desk!
    _put_tf(L, 'table_dark', 8, 8)
    L[2, 9, 10] = 4077
    # Unclaimed harbour freight on slate pad (west)
    _put_tf(L, 'crate_i', 3, 8)
    _put_tf(L, 'barrel_y', 5, 10)
    _put_tf(L, 'rodbucket', 6, 10)
    # East cozy sleeping alcove
    _put_tf(L, 'bigbed', 12, 5)
    _put_tf(L, 'drawer', 10, 5)
    L[1, 9, 13] = 5580
    _put_tree(L, 15, 5, 'parlor')
    _put_tree(L, 14, 9, 'fern')
    L[1, 11, 11] = 3391

    return _finalize(L, 107, [(8, 12), (5, 7), (7, 5)])


# ===========================================================================
# GROUP B: BRIARWICK & GOSSAMER WOOD (121, 122, 123, 124, 125, 523, 526)
# ===========================================================================

def build_121():
    """121: Briarwick Pokémon Center (20x17).
    Events: #2 Nurse (9,5), #3 PC (5,5), #4 Healing balls (11,5), #5 Exit (9,13),
            #6 Trainer (5,10), #7 Trainer 2 (12,10), #8 Gale Post desk (6,6).
    """
    W, H = 20, 17
    L = np.zeros((3, H, W), dtype=np.int32)
    floor = np.zeros((H, W), dtype=bool)
    floor[5:13, 3:17] = True
    floor[4, 7:13] = True          # Stepped woodland healing apse
    floor[12, 3:5] = False
    floor[12, 15:17] = False
    floor[13, 8:11] = True
    _seam_room(L, floor, wall_style='sheridan', floor_style='oak')

    # Floor zoning: emerald botanical conservatory side-bays + warm cedar planks + braided crimson rug (ZERO white glare!)
    for y in range(5, 13):
        for x in (3, 4, 15, 16):
            if floor[y, x]:
                L[0, y, x] = FLOOR_GLASS
    _put_9slice(L, SHER_RUG, 8, 8, 10, 12, z=1, mask=floor)
    _doormat(L, 9, 13)

    _sher_window(L, 8, 2)
    _sher_window(L, 11, 2)
    _sher_pilaster(L, 9, 2)
    _sher_pilaster(L, 10, 2)
    _put_grid(L, SHOJI_BLOSSOM, 13, 3, z_rows=(1, 1))
    _sher_window(L, 4, 3)

    # Warm copper-terracotta reception counter wrapping Nurse (9,5) & Healing balls (11,5)!
    L[1, 5, 8] = 5952
    L[1, 5, 12] = 5955
    for x, t in ((8, 5960), (9, 5961), (10, 5962), (11, 5961), (12, 5963)):
        L[1, 6, x] = t
    _put_grid(L, HELP_HEAL, 10, 4, z_rows=(2, 1))
    # Clean compact 2-row copper PC terminal at (5, 4..5) (ZERO ceiling clip!)
    L[2, 4, 5] = 5959; L[1, 5, 5] = 5967
    # Gale Post writing desk cleanly at (6,6) with intact 1-wide hanging postal chart above
    L[1, 6, 6] = 5702
    L[2, 6, 6] = 3428
    L[1, 3, 6] = 5453; L[1, 4, 6] = 5461

    _put_grid(L, BONSAI, 14, 5, z_rows=(2, 1))
    _put_grid(L, FLOWER_CART, 3, 6, z_rows=(2, 1))
    _put_tf(L, 'table_tea', 13, 8)
    L[1, 9, 12] = 4077
    _put_tf(L, 'bench_v', 3, 8)
    _put_tree(L, 16, 6, 'parlor')
    _put_tree(L, 15, 10, 'fern')
    _put_tree(L, 6, 11, 'parlor')
    L[1, 12, 12] = 7178

    return _finalize(L, 121, [(9, 5), (5, 5), (11, 5), (9, 13), (5, 10), (12, 10), (6, 6)])


def build_122():
    """122: Briarwick Mart (20x16).
    Events: #2 Mart (12,5), #3 Exit (8,12), #4 Customer (6,10).
    """
    W, H = 20, 16
    L = np.zeros((3, H, W), dtype=np.int32)
    floor = np.zeros((H, W), dtype=bool)
    floor[5:12, 3:16] = True
    floor[11, 3:5] = False
    floor[11, 14:16] = False
    floor[5, 3] = False
    floor[12, 7:10] = True
    _seam_room(L, floor, wall_style='sheridan', floor_style='oak')

    # Warm cedar planks + subtle emerald botanical trim on east bay + braided crimson rug (ZERO white glare!)
    for y in range(6, 11):
        for x in (14, 15):
            if floor[y, x]:
                L[0, y, x] = FLOOR_GLASS
    _put_9slice(L, SHER_RUG, 7, 7, 10, 10, z=1, mask=floor)
    _doormat(L, 8, 12)

    _put_grid(L, SHOJI_BLOSSOM, 11, 3, z_rows=(1, 1))
    _sher_window(L, 5, 3)
    _sher_window(L, 9, 3)
    _put_tf(L, 'shelf_bottles', 10, 4)

    # Warm copper-terracotta checkout counter wrapping Mart (12,5)
    L[1, 5, 11] = 5952
    L[1, 5, 14] = 5955
    for x, t in ((11, 5960), (12, 5961), (13, 5962), (14, 5963)):
        L[1, 6, x] = t
    _put_tf(L, 'shelf_goods', 4, 4)
    _put_tf(L, 'shelf_goods', 7, 4)
    _put_tf(L, 'shelf_green', 4, 8)
    _put_tf(L, 'shelf_green', 8, 8)
    _put_tf(L, 'display2', 11, 8)
    _put_grid(L, HOTEL_FLOWER_STAND, 15, 5, z_rows=(2, 1, 1))
    _put_grid(L, BONSAI, 13, 9, z_rows=(2, 1))
    _put_tf(L, 'crate_i2', 11, 10)
    _put_tree(L, 3, 9, 'parlor')
    L[1, 11, 6] = 7177

    return _finalize(L, 122, [(12, 5), (8, 12), (6, 10)])


def build_123():
    """123: Weavers' Guildhall (Ground x=3..17) + Warden's Loft (East x=24..34), 41x18."""
    W, H = 41, 18
    L = np.zeros((3, H, W), dtype=np.int32)
    floor = np.zeros((H, W), dtype=bool)
    floor[5:14, 3:18] = True
    floor[13, 3:5] = False
    floor[13, 16:18] = False
    floor[14, 9:12] = True
    floor[5:12, 24:35] = True
    floor[4, 27:32] = True
    floor[11, 33:35] = False
    floor[11, 24] = False

    _seam_room(L, floor, wall_style='sheridan', floor_style='oak')

    # Ground floor zoning: emerald silk alcoves + ornate crimson-silver guild runner
    for y in range(6, 11):
        for x in (3, 4, 16, 17):
            if floor[y, x]:
                L[0, y, x] = FLOOR_GLASS
    _put_9slice(L, HOTEL_CRIMSON_RUG, 8, 9, 12, 13, z=1, mask=floor)
    _doormat(L, 10, 14)

    _put_grid(L, BULLETIN_BOARD, 3, 3, z_rows=(1, 1))
    L[1, 5, 4] = 3456
    _sher_window(L, 7, 3)
    _sher_window(L, 12, 3)
    _put_grid(L, SHOJI_BLOSSOM, 8, 3, z_rows=(1, 1))
    # Complete Sheridan stairs finishing cleanly with bottom landing rows above Loft stairs up (16,6)!
    _put_grid(L, LOFT_STAIRS[1:], 15, 3, z_rows=(2, 1, 1))

    _put_grid(L, SHER_CHEST, 3, 11, z_rows=(2, 1))
    _put_tf(L, 'workbench', 5, 8)
    _put_tf(L, 'workbench', 12, 7)
    _put_tf(L, 'easel1', 14, 4)
    _put_tf(L, 'wardrobe', 6, 4)
    _put_grid(L, BONSAI, 11, 5, z_rows=(2, 1))
    _put_grid(L, FLOWER_CART, 15, 9, z_rows=(2, 1))
    L[1, 12, 13] = 4077
    L[1, 12, 6] = 4101
    _put_tree(L, 3, 6, 'parlor')
    _put_tree(L, 14, 11, 'fern')

    # Warden's Loft (warm cedar planks + rich crimson woven rug — ZERO white glare!)
    _put_9slice(L, SHER_RUG, 27, 7, 31, 10, z=1, mask=floor)
    _sher_window(L, 28, 2)
    _sher_window(L, 30, 2)
    _put_tf(L, 'clock', 33, 3)
    _put_grid(L, SHER_BOOKCASE, 24, 3, z_rows=(2, 1, 1))
    _put_tf(L, 'bookshelf_s', 26, 4)
    _put_grid(L, SHER_DESK, 28, 5, z_rows=(2, 1))
    L[2, 6, 28] = 3428
    L[2, 8, 29] = 4077
    # Grounded woven pot framing Loft stairs down (25,9) without blocking (25,9) or arrival (27,9)!
    L[1, 8, 24] = 4101
    _put_tf(L, 'crates3', 32, 8)
    _put_tree(L, 34, 5, 'parlor')
    L[1, 11, 29] = 7178

    return _finalize(
        L, 123,
        [(10, 14), (8, 7), (12, 10), (4, 5), (3, 11), (17, 12),
         (28, 6), (30, 6), (26, 10), (16, 6), (15, 7), (25, 9), (27, 9)]
    )


def build_124():
    """124: Treetop House (West x=3..11) + Briarwick Chapel (East x=23..35), 40x18.
    Events: House Exit (7,12), Retired Weaver (8,8), Bookshelf (9,5), Loom (3,8);
            Chapel Exit (29,14), Chapel mural (29,5), Child in pew (28,9), Chapel window (33,5).
    """
    W, H = 40, 18
    L = np.zeros((3, H, W), dtype=np.int32)
    floor = np.zeros((H, W), dtype=bool)
    floor[5:12, 3:12] = True
    floor[11, 3] = False
    floor[11, 11] = False
    floor[12, 6:9] = True
    floor[5:14, 23:36] = True
    floor[4, 26:33] = True
    floor[13, 23:25] = False
    floor[13, 34:36] = False
    floor[14, 28:31] = True

    _seam_room(L, floor, wall_style='sheridan', floor_style='oak')

    # --- ROOM 1: TREETOP HOUSE (x=3..11) ---
    _put_9slice(L, SHER_RUG, 5, 7, 9, 10, z=1, mask=floor)
    _doormat(L, 7, 12)
    _sher_window(L, 7, 3)
    _put_tf(L, 'bunk_o', 3, 5)                              # Complete 2x3 warm quilted weaver's bed (3..4, 5..7)
    # Loom at (3,8): narrow 1-wide tape loom easel (3, 8..9) so (4,8) & (4,9) are WIDE OPEN & REACHABLE!
    _put_tf(L, 'easel1', 3, 8)
    _put_grid(L, SHER_BOOKCASE, 9, 3, z_rows=(2, 1, 1))
    _put_tf(L, 'dresser', 6, 4)
    _put_tf(L, 'table_tea', 6, 8)
    L[2, 9, 8] = 4077
    _put_tree(L, 11, 5, 'parlor')
    _put_tree(L, 4, 10, 'fern')
    L[1, 10, 10] = 7178

    # --- ROOM 2: BRIARWICK CHAPEL (x=23..35) — STATELY SLATE-MARBLE SANCTUARY ---
    # Rich dark-slate diamond marble (7752..7770) framing the glowing crimson-silver velvet aisle runner!
    _put_9slice(L, HOTEL_MARBLE, 23, 5, 35, 13, z=0, mask=floor)
    _put_9slice(L, HOTEL_MARBLE, 26, 4, 32, 5, z=0, mask=floor)
    _put_9slice(L, HOTEL_CRIMSON_RUG, 28, 5, 30, 13, z=1, mask=floor)
    _doormat(L, 29, 14)

    _put_grid(L, HOTEL_PORTRAIT, 28, 2, z_rows=(1, 1))
    _put_tf(L, 'table_dark', 28, 4)
    _put_tf(L, 'shelf_low', 30, 5)
    _sher_pilaster(L, 27, 2)
    _sher_pilaster(L, 31, 2)
    _put_grid(L, COASTAL_ARCH_WIN, 33, 3, z_rows=(1, 1))
    _put_grid(L, COASTAL_ARCH_WIN, 24, 3, z_rows=(1, 1))
    L[1, 5, 33] = 7178
    L[1, 5, 25] = 7178

    for py in (7, 10):
        _put_grid(L, WOOD_BENCH, 24, py, z_rows=(2, 1))
        _put_grid(L, WOOD_BENCH, 32, py, z_rows=(2, 1))
    _put_grid(L, HOTEL_FLOWER_STAND, 26, 4, z_rows=(2, 1, 1))
    _put_grid(L, HOTEL_FLOWER_STAND, 32, 4, z_rows=(2, 1, 1))
    _put_grid(L, HOTEL_VASE, 23, 5, z_rows=(2, 1))
    _put_grid(L, HOTEL_VASE, 35, 5, z_rows=(2, 1))
    _put_tree(L, 25, 12, 'parlor')
    _put_tree(L, 33, 12, 'parlor')

    return _finalize(
        L, 124,
        [(7, 12), (8, 8), (9, 5), (3, 8), (29, 14), (29, 5), (28, 9), (33, 5)]
    )


def build_125():
    """125: Cutter's House (20x16).
    Events: #1 Exit (7,12), #2 Cutter (8,8), #3 Axe rack (6,5).
    """
    W, H = 20, 16
    L = np.zeros((3, H, W), dtype=np.int32)
    floor = np.zeros((H, W), dtype=bool)
    floor[5:12, 3:12] = True
    floor[11, 3] = False
    floor[11, 11] = False
    floor[12, 6:9] = True
    _seam_room(L, floor, wall_style='sheridan', floor_style='oak')

    _put_9slice(L, SLATE_STONE, 8, 5, 11, 7, z=0, mask=floor)
    _put_9slice(L, SHER_RUG, 5, 7, 9, 10, z=1, mask=floor)
    _doormat(L, 7, 12)

    _sher_window(L, 4, 3)
    _sher_window(L, 9, 3)
    _put_tf(L, 'workbench', 5, 4)
    _put_tf(L, 'bunk_o', 3, 5)
    _put_tf(L, 'kitchen', 8, 4)
    _put_tf(L, 'table_dark', 6, 8)
    L[2, 9, 8] = 4077
    _put_tf(L, 'crate_i', 3, 9)
    _put_tf(L, 'barrel_y', 10, 9)
    _put_tf(L, 'bucket', 9, 11)
    _put_tree(L, 11, 7, 'fern')

    return _finalize(L, 125, [(7, 12), (8, 8), (6, 5)])


def build_523():
    """523: Hale Farmhouse (21x17).
    Events: #1 Exit (10,13), #2 Kitchen table (9,6), #3 Wenna (7,8), #4 Parsnip (11,12),
            #5 Farmer Hale (13,10), #6 Bookshelf (13,5), #7 Juno's seed packets (11,5), #8 Bed (16,7).
    """
    W, H = 21, 17
    L = np.zeros((3, H, W), dtype=np.int32)
    floor = np.zeros((H, W), dtype=bool)
    floor[5:13, 3:18] = True
    floor[12, 3:5] = False
    floor[12, 16:18] = False
    floor[13, 9:12] = True
    _seam_room(L, floor, wall_style='sheridan', floor_style='oak')

    for y in range(9, 12):
        for x in (15, 16, 17):
            if floor[y, x]:
                L[0, y, x] = FLOOR_GLASS
    _put_9slice(L, SHER_RUG, 6, 6, 12, 10, z=1, mask=floor)
    _doormat(L, 10, 13)

    _sher_window(L, 5, 3)
    _sher_window(L, 16, 3)
    _put_tf(L, 'painting1', 7, 3)
    _put_tf(L, 'kitchen', 3, 4)
    # Complete 3x2 bulletin board for Juno's pinned seed packets (10..12, 3..4) + planter box at (11,5)!
    _put_grid(L, BULLETIN_BOARD, 10, 3, z_rows=(1, 1))
    L[1, 5, 11] = 7178
    _put_grid(L, SHER_BOOKCASE, 13, 3, z_rows=(2, 1, 1))

    _put_tf(L, 'dining', 8, 6)
    L[2, 7, 7] = 4077
    L[2, 7, 11] = 4077
    L[2, 9, 11] = 4077
    # COMPLETE 3x3 Sheridan mahogany double bed at (15..17, 5..7) -> Bed (16,7) has walkable (16,8) directly below!
    _put_grid(L, SHER_BED_FULL, 15, 5, z_rows=(2, 1, 1))
    _put_tf(L, 'sideboard', 3, 7)
    _put_tf(L, 'crate_i', 5, 11)
    _put_tf(L, 'barrel_y', 3, 10)
    _put_grid(L, FLOWER_CART, 15, 9, z_rows=(2, 1))
    _put_tree(L, 14, 11, 'parlor')
    L[1, 12, 8] = 7177

    return _finalize(L, 523, [(10, 13), (9, 6), (7, 8), (11, 12), (13, 10), (13, 5), (11, 5), (16, 7)])


def build_526():
    """526: Woodward's Hut (20x16).
    Events: #1 Exit (7,12), #2 Woodward (8,8), #3 Bookshelf (5,5).
    """
    W, H = 20, 16
    L = np.zeros((3, H, W), dtype=np.int32)
    floor = np.zeros((H, W), dtype=bool)
    floor[5:12, 3:12] = True
    floor[11, 3] = False
    floor[11, 11] = False
    floor[12, 6:9] = True
    _seam_room(L, floor, wall_style='sheridan', floor_style='oak')

    _put_9slice(L, SLATE_STONE, 3, 5, 5, 7, z=0, mask=floor)
    _put_9slice(L, SHER_RUG, 5, 7, 9, 10, z=1, mask=floor)
    _doormat(L, 7, 12)

    _sher_window(L, 7, 3)
    _put_grid(L, SHER_BOOKCASE, 4, 3, z_rows=(2, 1, 1))
    _put_grid(L, SHER_DESK, 6, 5, z_rows=(2, 1))
    _put_tf(L, 'bunk_o', 9, 5)
    _put_tf(L, 'table_dark', 6, 8)
    L[2, 9, 8] = 4077
    _put_tf(L, 'crate', 3, 8)
    _put_tf(L, 'rodbucket', 10, 8)
    _put_tree(L, 11, 5, 'fern')
    L[1, 10, 4] = 3391

    return _finalize(L, 526, [(7, 12), (8, 8), (5, 5)])


# ===========================================================================
# GROUP C: SALTMERE (141, 142, 143, 144) — Theatrical Crimson-Brass & Marble
# ===========================================================================

def build_141():
    """141: Saltmere Pokémon Center (15x10 — UPGRADED from stock Gen-3 template to Tileset 34!).
    Exact HEAD events: #2 Nurse (7,2), #3 PC (11,1), #4 Healing balls (5,2),
                       #6 Town Map, size(2,1) (12,1), #7 Exit (7,9), #8 Actor (12,6).
    """
    W, H = 15, 10
    L = np.zeros((3, H, W), dtype=np.int32)
    floor = np.zeros((H, W), dtype=bool)
    floor[2:9, 1:14] = True
    floor[8, 1] = False
    floor[8, 13] = False
    floor[9, 6:9] = True
    _seam_room(L, floor, wall_style='hotel', floor_style='marble')

    _put_9slice(L, HOTEL_CRIMSON_RUG, 6, 4, 8, 8, z=1, mask=floor)
    _doormat(L, 7, 9)

    _put_grid(L, HOTEL_RED_WINDOW, 2, 0, z_rows=(1, 1))
    _put_grid(L, HOTEL_RED_WINDOW, 9, 0, z_rows=(1, 1))
    _sher_pilaster(L, 6, 0)
    _sher_pilaster(L, 8, 0)
    L[1, 0, 11] = 5847; L[1, 1, 11] = 5855
    _put_grid(L, SEA_CHART, 12, 0, z_rows=(1, 1))

    _put_grid(L, HELP_HEAL, 4, 1, z_rows=(2, 1))
    L[1, 2, 8] = 7235
    for x, t in ((5, 7240), (6, 7241), (7, 7242), (8, 7243)):
        L[1, 3, x] = t

    _put_grid(L, GRAND_PIANO, 1, 5, z_rows=(2, 1, 1))
    L[1, 6, 4] = 4077
    _put_grid(L, HOTEL_FLOWER_STAND, 1, 2, z_rows=(2, 1, 1))
    _put_grid(L, HOTEL_VASE, 13, 2, z_rows=(2, 1))
    _put_grid(L, HOTEL_DESK_BOOKS, 10, 4, z_rows=(2, 1))
    _put_tree(L, 12, 7, 'ficus')
    _put_tree(L, 4, 7, 'parlor')

    return _finalize(L, 141, [(7, 2), (11, 1), (5, 2), (12, 1), (7, 9), (12, 6)])


def build_142():
    """142: Saltmere Mart (11x9 — UPGRADED from stock Gen-3 template to Tileset 34!).
    Exact HEAD events: #2 Mart (2,3) [dir=6 facing right], #3 Exit (4,8).
    """
    W, H = 11, 9
    L = np.zeros((3, H, W), dtype=np.int32)
    floor = np.zeros((H, W), dtype=bool)
    floor[2:8, 1:10] = True
    floor[7, 9] = False
    floor[7, 1] = False
    floor[8, 3:6] = True
    _seam_room(L, floor, wall_style='hotel', floor_style='marble')

    _put_9slice(L, HOTEL_CRIMSON_RUG, 4, 3, 6, 7, z=1, mask=floor)
    _doormat(L, 4, 8)

    _put_grid(L, HOTEL_RED_WINDOW, 5, 0, z_rows=(1, 1))
    _put_grid(L, HOTEL_PORTRAIT, 2, 0, z_rows=(1, 1))

    # Crisp Hotel rose counter wrapping Mart (2,3): plain marble cap at (3,2), single pink rose at (3,3) (p=8f)!
    L[1, 2, 3] = 5835
    L[1, 3, 3] = 7235
    L[1, 4, 1] = 7240; L[1, 4, 2] = 7241; L[1, 4, 3] = 7243
    _put_tf(L, 'shelf_goods', 7, 1)
    _put_tf(L, 'shelf_green', 7, 5)
    _put_grid(L, HOTEL_FLOWER_STAND, 9, 2, z_rows=(2, 1, 1))
    _put_grid(L, HOTEL_VASE, 1, 5, z_rows=(2, 1))
    _put_tree(L, 9, 5, 'parlor')

    return _finalize(L, 142, [(2, 3), (4, 8)])


def build_143():
    """143: Saltmere Harbour Office (23x17).
    Events: #1 Exit (11,13), #2 Harbourmaster (11,6), #3 Customs clerk (15,7), #4 Tide board (10,9),
            #5 Seized crates (4,8), #6 Sailor waiting (5,10), #7 Grant Kiosk P-3NNY/1 (14,8) [trial_overlay].
    """
    W, H = 23, 17
    L = np.zeros((3, H, W), dtype=np.int32)
    floor = np.zeros((H, W), dtype=bool)
    floor[5:13, 3:20] = True
    floor[4, 9:16] = True
    floor[12, 3:5] = False
    floor[12, 18:20] = False
    floor[13, 10:13] = True
    _seam_room(L, floor, wall_style='sheridan', floor_style='oak')

    # Rich Saltmere civic stone zoning: slate customs freight bay + Chrisola marble desk pad + royal blue waiting rug!
    _put_9slice(L, SLATE_STONE, 3, 5, 7, 11, z=0, mask=floor)
    _put_9slice(L, HOTEL_MARBLE, 9, 5, 17, 9, z=0, mask=floor)
    _put_9slice(L, BLUE_MARITIME_RUG, 8, 10, 14, 12, z=1, mask=floor)
    _doormat(L, 11, 13)

    _put_grid(L, COASTAL_ARCH_WIN, 4, 3, z_rows=(1, 1))
    _put_grid(L, SEA_CHART, 7, 3, z_rows=(1, 1))
    _put_tf(L, 'map_wall', 10, 2)
    _put_tf(L, 'lifering', 14, 2)
    _put_grid(L, HOTEL_RED_WINDOW, 17, 3, z_rows=(1, 1))

    # Blue-steel customs counter fronting Harbourmaster (11,6) & ending cleanly beside Customs clerk (15,7)!
    # Vase at (14,5..6) + ledger desk at (16,5..6) frame clerk & ensure trial_overlay seats Grant Kiosk dead-on (14,8)!
    L[1, 6, 9] = 5840
    for x, t in ((9, 5848), (10, 5849), (11, 5850), (12, 5849), (13, 5849), (14, 5851)):
        L[1, 7, x] = t
    _put_grid(L, HOTEL_VASE, 14, 5, z_rows=(2, 1))
    _put_grid(L, HOTEL_VASE, 16, 5, z_rows=(2, 1))
    L[1, 9, 10] = 3456; L[2, 9, 10] = 3428

    _put_tf(L, 'crates3', 3, 6)
    _put_tf(L, 'barrel_b', 6, 6)
    _put_tf(L, 'barrel_y', 7, 6)
    _put_grid(L, SHER_BOOKCASE, 18, 4, z_rows=(2, 1, 1))
    _put_grid(L, SOFA_GREY, 16, 10, z_rows=(2, 1))
    _put_grid(L, WOOD_BENCH, 5, 11, z_rows=(2, 1))
    L[1, 11, 15] = 5580
    _put_tree(L, 3, 9, 'fern')
    _put_tree(L, 19, 8, 'palm')
    _put_tree(L, 14, 12, 'parlor')

    return _finalize(L, 143, [(11, 13), (11, 6), (15, 7), (10, 9), (4, 8), (5, 10), (14, 8)])


def build_144():
    """144: Saltwife's House (20x16).
    Events: #1 Exit (9,12), #2 Saltwife (9,7), #3 Salt crocks (4,8), #4 Rake (12,9).
    """
    W, H = 20, 16
    L = np.zeros((3, H, W), dtype=np.int32)
    floor = np.zeros((H, W), dtype=bool)
    floor[5:12, 3:16] = True
    floor[11, 3:5] = False
    floor[11, 14:16] = False
    floor[12, 8:11] = True
    _seam_room(L, floor, wall_style='sheridan', floor_style='oak')

    _put_9slice(L, SLATE_STONE, 3, 6, 6, 10, z=0, mask=floor)
    _put_9slice(L, HOTEL_CRIMSON_RUG, 7, 7, 11, 10, z=1, mask=floor)
    _doormat(L, 9, 12)

    _put_grid(L, HOTEL_RED_WINDOW, 10, 3, z_rows=(1, 1))
    _sher_window(L, 4, 3)
    _put_tf(L, 'kitchen', 5, 4)
    _put_tf(L, 'shelf_bottles', 3, 4)
    _put_tf(L, 'barrel_b', 4, 7)
    _put_tf(L, 'barrel_y', 3, 7)
    _put_tf(L, 'bucket', 5, 9)
    _put_tf(L, 'rodbucket', 12, 8)
    _put_tf(L, 'table_tea', 8, 8)
    L[2, 9, 7] = 4077
    _put_tf(L, 'bed_blue', 13, 5)
    _put_grid(L, HOTEL_VASE, 12, 4, z_rows=(2, 1))         # Tucked neatly against north wall beside bed
    _put_tree(L, 14, 9, 'fern')
    _put_tree(L, 5, 10, 'parlor')

    return _finalize(L, 144, [(9, 12), (9, 7), (4, 8), (12, 9)])


# ===========================================================================
# GROUP D: EBBMOUTH (161, 162, 163, 164, 165) — Weathered Maritime Stonework
# ===========================================================================

def build_161():
    """161: Ebbmouth Pokémon Center (15x10 — UPGRADED from stock Gen-3 template to Tileset 34!).
    Exact HEAD events: #2 Nurse (7,2), #3 PC (11,1), #4 Healing balls (5,2),
                       #6 Town Map, size(2,1) (12,1), #7 Exit (7,9), #8 Professor Larch (12,6).
    """
    W, H = 15, 10
    L = np.zeros((3, H, W), dtype=np.int32)
    floor = np.zeros((H, W), dtype=bool)
    floor[2:9, 1:14] = True
    floor[8, 1] = False
    floor[8, 13] = False
    floor[9, 6:9] = True
    _seam_room(L, floor, wall_style='stone', floor_style='slate')

    _put_9slice(L, BLUE_MARITIME_RUG, 6, 4, 8, 8, z=1, mask=floor)
    _doormat(L, 7, 9)

    _put_grid(L, COASTAL_ARCH_WIN, 2, 0, z_rows=(1, 1))
    _put_tf(L, 'lifering', 9, 0)
    L[1, 0, 11] = 5847; L[1, 1, 11] = 5855
    _put_grid(L, SEA_CHART, 12, 0, z_rows=(1, 1))

    _put_grid(L, HELP_HEAL, 4, 1, z_rows=(2, 1))
    L[1, 2, 8] = 5843
    for x, t in ((5, 5848), (6, 5849), (7, 5850), (8, 5851)):
        L[1, 3, x] = t

    _put_grid(L, WOOD_BENCH, 1, 5, z_rows=(2, 1))
    _put_tf(L, 'rodbucket', 1, 3)
    _put_grid(L, SHER_DESK, 10, 4, z_rows=(2, 1))
    L[2, 4, 10] = 3428
    L[1, 6, 10] = 4077
    _put_tree(L, 13, 4, 'fern')
    _put_tree(L, 4, 7, 'parlor')
    _put_tree(L, 12, 7, 'palm')

    return _finalize(L, 161, [(7, 2), (11, 1), (5, 2), (12, 1), (7, 9), (12, 6)])


def build_162():
    """162: Ebbmouth Mart (11x9 — UPGRADED from stock Gen-3 template to Tileset 34!).
    Exact HEAD events: #2 Mart (2,3) [dir=6 facing right], #3 Exit (4,8).
    """
    W, H = 11, 9
    L = np.zeros((3, H, W), dtype=np.int32)
    floor = np.zeros((H, W), dtype=bool)
    floor[2:8, 1:10] = True
    floor[7, 1] = False
    floor[7, 9] = False
    floor[8, 3:6] = True
    _seam_room(L, floor, wall_style='stone', floor_style='slate')

    _put_9slice(L, BLUE_MARITIME_RUG, 4, 3, 6, 7, z=1, mask=floor)
    _doormat(L, 4, 8)

    _put_grid(L, COASTAL_ARCH_WIN, 4, 0, z_rows=(1, 1))
    _put_tf(L, 'lifering', 1, 0)

    # Crisp blue-steel maritime counter wrapping Mart (2,3): plain top cap (3,2), single hydrangea corner at (3,3)!
    L[1, 2, 3] = 5835
    L[1, 3, 3] = 5843
    L[1, 4, 1] = 5848; L[1, 4, 2] = 5849; L[1, 4, 3] = 5851

    _put_tf(L, 'shelf_goods', 7, 1)
    _put_tf(L, 'shelf_green', 7, 5)
    _put_tf(L, 'rodbucket', 9, 2)
    _put_tf(L, 'barrel_b', 9, 4)
    _put_tf(L, 'crate_i', 1, 5)
    L[1, 7, 8] = 3391

    return _finalize(L, 162, [(2, 3), (4, 8)])


def build_163():
    """163: Anglers' Guild (13x10 — UPGRADED from stock Gen-3 house to Tileset 34!).
    Exact HEAD events: #1 Exit (3,9), #2 Guildmaster (5,4).
    """
    W, H = 13, 10
    L = np.zeros((3, H, W), dtype=np.int32)
    floor = np.zeros((H, W), dtype=bool)
    floor[2:9, 1:12] = True
    floor[8, 10:12] = False
    floor[8, 1] = False
    floor[9, 2:5] = True
    _seam_room(L, floor, wall_style='stone', floor_style='oak')

    _put_9slice(L, SLATE_STONE, 2, 7, 4, 9, z=0, mask=floor)
    _put_9slice(L, BLUE_MARITIME_RUG, 5, 4, 9, 7, z=1, mask=floor)
    _doormat(L, 3, 9)

    # Keep ALL wall hangings cleanly inside stone wall x=1..11 (ZERO overhang onto east void rim!)
    _put_grid(L, COASTAL_ARCH_WIN, 2, 0, z_rows=(1, 1))
    _put_grid(L, BULLETIN_BOARD, 4, 0, z_rows=(1, 1))
    _put_grid(L, SEA_CHART, 8, 0, z_rows=(1, 1))
    _put_tf(L, 'lifering', 10, 0)                          # (10..11, 0..1) cleanly inside stone wall!

    _put_tf(L, 'table_dark', 6, 5)
    L[2, 5, 6] = 3428
    L[2, 6, 8] = 4077
    L[2, 4, 7] = 4077
    _put_tf(L, 'rodbucket', 1, 2)
    _put_tf(L, 'barrel_b', 1, 4)
    _put_tf(L, 'barrel_y', 1, 6)
    _put_grid(L, SHER_CHEST, 8, 2, z_rows=(2, 1))
    _put_tf(L, 'rodbucket', 11, 2)
    _put_grid(L, WOOD_BENCH, 6, 7, z_rows=(2, 1))
    _put_tree(L, 11, 5, 'fern')
    L[1, 8, 5] = 4101

    return _finalize(L, 163, [(3, 9), (5, 4)])


def build_164():
    """164: Reyes House (10x9 — UPGRADED from stock Gen-3 house2 to Tileset 34!).
    Exact HEAD events: #1 Exit (6,8), #2 Mrs Reyes (7,4), #3 Cellar door (1,6).
    """
    W, H = 10, 9
    L = np.zeros((3, H, W), dtype=np.int32)
    floor = np.zeros((H, W), dtype=bool)
    floor[2:8, 1:9] = True
    floor[7, 1] = False
    floor[7, 8] = False
    floor[8, 5:8] = True
    _seam_room(L, floor, wall_style='stone', floor_style='oak')

    _put_9slice(L, SLATE_STONE, 1, 5, 2, 6, z=0, mask=floor)
    _put_9slice(L, SHER_RUG, 4, 4, 7, 6, z=1, mask=floor)
    _doormat(L, 6, 8)

    _put_grid(L, COASTAL_ARCH_WIN, 6, 0, z_rows=(1, 1))
    _put_tf(L, 'kitchen', 2, 1)
    _put_tf(L, 'bookshelf_s', 8, 1)
    # COMPLETE 2x2 barred wooden cellar hatch cleanly at (1..2, 5..6) -> solid on Cellar door (1,6), walkable at (1,5)/(2,5)/(3,6)!
    _put_grid(L, [[4824, 4825], [4832, 4833]], 1, 5, z_rows=(2, 1))
    _put_tf(L, 'table_tea', 4, 4)
    L[2, 5, 6] = 4077
    _put_tf(L, 'bunk_b', 1, 2)
    _put_tree(L, 8, 5, 'parlor')
    L[1, 7, 3] = 4101

    return _finalize(L, 164, [(6, 8), (7, 4), (1, 6)])


def build_165():
    """165: Net-mender's House (10x9 — UPGRADED from stock Gen-3 house2 to Tileset 34!).
    Exact HEAD events: #1 Exit (6,8), #2 Net-mender (7,4).
    """
    W, H = 10, 9
    L = np.zeros((3, H, W), dtype=np.int32)
    floor = np.zeros((H, W), dtype=bool)
    floor[2:8, 1:9] = True
    floor[7, 1] = False
    floor[7, 8] = False
    floor[8, 5:8] = True
    _seam_room(L, floor, wall_style='stone', floor_style='oak')

    _put_9slice(L, SLATE_STONE, 1, 2, 3, 6, z=0, mask=floor)
    _put_9slice(L, BLUE_MARITIME_RUG, 4, 4, 7, 6, z=1, mask=floor)
    _doormat(L, 6, 8)

    # Balanced stone north wall: arched windows flanking central life ring (ZERO wall overhang!)
    _put_grid(L, COASTAL_ARCH_WIN, 1, 0, z_rows=(1, 1))
    _put_tf(L, 'lifering', 4, 0)
    _put_grid(L, COASTAL_ARCH_WIN, 6, 0, z_rows=(1, 1))

    _put_tf(L, 'crate_i', 1, 2)
    _put_tf(L, 'barrel_y', 2, 2)
    _put_tf(L, 'bunk_o', 1, 4)
    _put_tf(L, 'rodbucket', 3, 2)
    _put_tf(L, 'barrel_b', 8, 2)
    _put_tf(L, 'table_dark', 4, 4)
    L[2, 4, 5] = 3428
    L[2, 5, 6] = 4077
    L[1, 7, 3] = 4101
    _put_tree(L, 8, 5, 'fern')

    return _finalize(L, 165, [(6, 8), (7, 4)])


# ===========================================================================
# Spec Wiring Helpers (100% EvID_exact & Untouched-Map Parity!)
# ===========================================================================
BUILDERS = {
    101: build_101,
    102: build_102,
    104: build_104,
    107: build_107,
    121: build_121,
    122: build_122,
    123: build_123,
    124: build_124,
    125: build_125,
    523: build_523,
    526: build_526,
    141: build_141,
    142: build_142,
    143: build_143,
    144: build_144,
    161: build_161,
    162: build_162,
    163: build_163,
    164: build_164,
    165: build_165,
}

# Tone profiles tuned per town atmosphere
TONES = {
    101: [10, 4, -10, 0],   # Warm Ferrow coastal lantern glow
    102: [8, 3, -10, 0],
    104: [14, 6, -12, 0],   # Cozy Tidewater hearth warmth
    107: [6, 2, -10, 0],
    121: [8, 6, -8, 0],     # Briarwick sunlit cedar & silk warmth
    122: [8, 5, -8, 0],
    123: [8, 4, -10, 0],
    124: [10, 6, -8, 0],
    125: [6, 2, -10, 0],
    523: [12, 6, -10, 0],   # Warm Hale farmhouse morning
    526: [4, 2, -10, 0],
    141: [8, 2, -6, 0],     # Saltmere theatrical crimson-brass luster
    142: [8, 2, -6, 0],
    143: [4, 4, -4, 0],
    144: [6, 4, -8, 0],
    161: [-6, 0, 8, 4],     # Ebbmouth cool weathered maritime stone
    162: [-6, 0, 8, 4],
    163: [-4, 0, 6, 4],
    164: [-2, 0, 6, 4],
    165: [-4, 0, 6, 4],
}


def _layers_to_palette_tiles(L):
    """Export a 3xHxW Tileset-34 array into palette:interior `map:` + `tiles:` entries
    (used ONLY for the 8 PC/Mart specs that rely on build.py's `take_events:` hook)."""
    Z, H, W = L.shape
    grid_str = '\n'.join('.' * W for _ in range(H)) + '\n'
    tiles = []
    for z in range(Z):
        for y in range(H):
            for x in range(W):
                t = int(L[z, y, x])
                if z == 0 and t == VOID:
                    continue
                if t == 0:
                    continue
                tiles.append({'tile': t, 'at': [x, y], 'layer': z})
    return grid_str, tiles


def _update_spec_file(fname, header, transform_fn):
    path = os.path.join(HERE, 'specs', fname)
    docs = [d for d in yaml.safe_load_all(open(path, encoding='utf-8')) if d]
    out_docs = [transform_fn(d) for d in docs]
    body = header + '\n---\n'.join(
        yaml.safe_dump(s, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True)
        for s in out_docs
    )
    with open(path, 'w', encoding='utf-8') as f:
        f.write(body)
    print(f'Updated spec {fname} ({len(out_docs)} maps)')


def _wire_raw(d, mid):
    """Replace palette/map/tiles (or template) with clean `tileset: 34` + `raw: data/raw/NNN.npy`."""
    s = {
        'id': mid,
        'name': d['name'],
        'parent': d['parent'],
        'bgm': d['bgm'],
        'metadata': d['metadata'],
        'tone': TONES[mid],
        'biome': 'interior',
        'tileset': TID,
        'raw': f'data/raw/{mid:03d}.npy',
        'events': d['events'],
    }
    if 'display_name' in d:
        s['display_name'] = d['display_name']
    return s


def _wire_take_events(d, mid, L):
    """Update a PC/Mart spec that uses `take_events:` using exact `L` exported to `palette: interior`."""
    grid_str, tiles = _layers_to_palette_tiles(L)
    s = {
        'id': mid,
        'name': d['name'],
        'parent': d['parent'],
        'bgm': d['bgm'],
        'metadata': d['metadata'],
        'tone': TONES[mid],
        'biome': 'interior',
        'palette': 'interior',
        'map': grid_str,
        'tiles': tiles,
        'events': d['events'],
        'take_events': d['take_events'],
    }
    return s


def main():
    raw_dir = os.path.join(HERE, 'data', 'raw')
    os.makedirs(raw_dir, exist_ok=True)
    arrays = {}
    for mid, fn in BUILDERS.items():
        L = fn()
        arrays[mid] = L
        out_p = os.path.join(raw_dir, f'{mid:03d}.npy')
        np.save(out_p, L.astype(np.int16))
        print(f'Saved {out_p} ({L.shape})')

    # 1. Ferrow's Landing (101_ferrows_landing_interiors.yaml):
    #    TOUCH ONLY 101, 102, 104, 107; LEAVE 103, 105, 106, 108 100% BYTE-IDENTICAL!
    def tf_101(d):
        mid = d.get('id')
        if mid in (101, 102):
            return _wire_take_events(d, mid, arrays[mid])
        if mid in (104, 107):
            return _wire_raw(d, mid)
        return d

    _update_spec_file(
        '101_ferrows_landing_interiors.yaml',
        "# Ferrow's Landing interiors (101-108). 101/102/104/107 by wave15_act1_interiors_craft.py; 103 by station_103.py; 105/106 by lighthouse_105_106.py; 108 by customs_108.py.\n",
        tf_101,
    )

    # 2. Briarwick (121_briarwick_interiors.yaml): ALL 7 (121, 122, 123, 124, 125, 523, 526)
    def tf_121(d):
        mid = d.get('id')
        if mid in (121, 122):
            return _wire_take_events(d, mid, arrays[mid])
        if mid in (123, 124, 125, 523, 526):
            return _wire_raw(d, mid)
        return d

    _update_spec_file(
        '121_briarwick_interiors.yaml',
        "# Briarwick & Gossamer Wood interiors (121-125, 523, 526). Crafted by layouts/wave15_act1_interiors_craft.py.\n",
        tf_121,
    )

    def _ensure_exit(evs, at, link):
        evs = list(evs or [])
        if evs and evs[0].get('type') == 'exit':
            return evs
        return [{'type': 'exit', 'at': at, 'link': link}] + evs

    # 3. Saltmere PC & Mart (141_saltmere_interiors.yaml): 141 & 142 (upgraded from stock templates with 100% EvID_exact!)
    def tf_141(d):
        mid = d.get('id')
        if mid == 141:
            nd = dict(d)
            nd['events'] = _ensure_exit(d.get('events'), [7, 9], 'SM_PC')
            nd['take_events'] = [
                {'template': 'pokecenter', 'name': 'Nurse', 'at': [7, 2]},
                {'template': 'pokecenter', 'name': 'Healing balls', 'at': [5, 2]},
                {'template': 'pokecenter', 'name': 'PC', 'at': [11, 1]},
                {'template': 'pokecenter', 'name': 'Town Map, size(2,1)', 'at': [12, 1]},
            ]
            return _wire_take_events(nd, 141, arrays[141])
        if mid == 142:
            nd = dict(d)
            nd['events'] = _ensure_exit(d.get('events'), [4, 8], 'SM_MART')
            nd['take_events'] = [
                {'template': 'mart', 'name': 'Mart', 'at': [2, 3]},
            ]
            return _wire_take_events(nd, 142, arrays[142])
        return d

    _update_spec_file(
        '141_saltmere_interiors.yaml',
        "# Saltmere Pokémon Center & Mart (141-142). Crafted on Tileset 34 by layouts/wave15_act1_interiors_craft.py.\n",
        tf_141,
    )

    # 4. Saltmere Rooms (143_saltmere_rooms.yaml): TOUCH ONLY 143 & 144; LEAVE 145 UNTOUCHED!
    def tf_143(d):
        mid = d.get('id')
        if mid in (143, 144):
            return _wire_raw(d, mid)
        return d

    _update_spec_file(
        '143_saltmere_rooms.yaml',
        "# Saltmere Harbour Office (143), Saltwife's House (144) by wave15_act1_interiors_craft.py; 145 Lantern Theatre preserved.\n",
        tf_143,
    )

    # 5. Ebbmouth Interiors (161_ebbmouth_interiors.yaml): ALL 5 (161, 162, 163, 164, 165 — upgraded from stock templates!)
    def tf_161(d):
        mid = d.get('id')
        if mid == 161:
            nd = dict(d)
            nd['events'] = _ensure_exit(d.get('events'), [7, 9], 'EB_PC')
            nd['take_events'] = [
                {'template': 'pokecenter', 'name': 'Nurse', 'at': [7, 2]},
                {'template': 'pokecenter', 'name': 'Healing balls', 'at': [5, 2]},
                {'template': 'pokecenter', 'name': 'PC', 'at': [11, 1]},
                {'template': 'pokecenter', 'name': 'Town Map, size(2,1)', 'at': [12, 1]},
            ]
            return _wire_take_events(nd, 161, arrays[161])
        if mid == 162:
            nd = dict(d)
            nd['events'] = _ensure_exit(d.get('events'), [4, 8], 'EB_MART')
            nd['take_events'] = [
                {'template': 'mart', 'name': 'Mart', 'at': [2, 3]},
            ]
            return _wire_take_events(nd, 162, arrays[162])
        if mid == 163:
            nd = dict(d)
            nd['events'] = _ensure_exit(d.get('events'), [3, 9], 'EB_ANGLER')
            return _wire_raw(nd, 163)
        if mid == 164:
            nd = dict(d)
            nd['events'] = _ensure_exit(d.get('events'), [6, 8], 'EB_REYES')
            return _wire_raw(nd, 164)
        if mid == 165:
            nd = dict(d)
            nd['events'] = _ensure_exit(d.get('events'), [6, 8], 'EB_HOUSE')
            return _wire_raw(nd, 165)
        return d

    _update_spec_file(
        '161_ebbmouth_interiors.yaml',
        "# Ebbmouth interiors (161-165). Crafted on Tileset 34 by layouts/wave15_act1_interiors_craft.py.\n",
        tf_161,
    )


if __name__ == '__main__':
    main()
