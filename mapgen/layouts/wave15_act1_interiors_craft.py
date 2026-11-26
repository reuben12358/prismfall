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
ALPINE_SLATE = [
    [1152, 1153, 1154],
    [1160, 1161, 1162],
    [1168, 1169, 1170],
]
SAGE_MARBLE = [
    [1104, 1105, 1106],
    [1112, 1113, 1114],
    [1120, 1121, 1122],
]
HONEY_PARQUET = [
    [1051, 1052, 1053],
    [1059, 1060, 1061],
    [1067, 1068, 1069],
]
BROWN_WOVEN_RUG = [
    [8620, 8621, 8622],
    [8628, 8629, 8630],
    [8636, 8637, 8638],
]
CREAM_MEDALLION_RUG = [
    [960, 961, 962],
    [968, 969, 970],
    [976, 977, 978],
]
NORDIC_RUG = [
    [1008, 1009, 1010],
    [1016, 1017, 1018],
    [1024, 1025, 1026],
    [1032, 1033, 1034],
]

# ---------------------------------------------------------------------------
# Verified Multi-Tile Stamps (visually proofed from ts34 atlas scans)
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
CREAM_BED = [
    [3600, 3601, 3602],
    [3608, 3609, 3610],
    [3616, 3617, 3618],
    [3624, 3625, 3626],
]
TAPESTRY_GOLD = [
    [5531, 5532],
    [5539, 5540],
]
HERB_RACK = [
    [5422],
    [5430],
    [5438],
]
LOOM_FRAME_A = [[3305], [3313]]
LOOM_FRAME_B = [[3306], [3314]]
LOOM_FRAME_C = [[3307], [3315]]
LOOM_WARP_RAIL = [[4174, 4175], [4182, 4183]]
LOOM_THREAD_CAB = [
    [3308, 3309, 3310, 3311],
    [3316, 3317, 3318, 3319],
]
TEXTILE_RACK = [[7484, 7485], [7492, 7493]]
LUGGAGE_CLOTH_RACK = [[7486, 7487], [7494, 7495]]
SALT_FIBER_CRATE = [[4186, 4187], [4194, 4195]]
BLUE_DYE_CATCH_CRATE = [[4188, 4189], [4196, 4197]]
RODBUCKET_FULL = [[4060, 4061], [4068, 4069]]
TIMBER_STACK = [[4826, 4827, 4828], [4834, 4835, 4836]]
RAKE_TOOLS = [[4870, 4871], [4878, 4879]]
TOOL_RACK = [[4869, 4870, 4871], [4877, 4878, 4879]]
SPICE_SHELF = [[3440, 3441], [3448, 3449]]
CHALKBOARD = [
    [3276, 3277, 3278],
    [3284, 3285, 3286],
]
PAINTING_HARBOR_A = [[7137], [7145]]
PAINTING_HARBOR_B = [[7138], [7146]]
COAT_STAND = [[2271], [2279]]


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


def _put_oak_inlay(L, x0, y0, x1, y1, mask=None):
    """Warm Sheridan coastal oak timber floorboards (5352..5363) inlaid cleanly inside weathered slate rooms."""
    H, W = L.shape[1:]
    for y in range(max(0, y0), min(H, y1 + 1)):
        top_row = (y == y0)
        for x in range(max(0, x0), min(W, x1 + 1)):
            if mask is not None and not mask[y, x]:
                continue
            left_edge = (x == x0)
            if top_row:
                L[0, y, x] = 5352 if left_edge else 5353 + (x - x0) % 3
            else:
                L[0, y, x] = 5360 if left_edge else 5361 + (x - x0) % 3


def _put_nordic_rug(L, x0, y0, x1, y1, z=1, mask=None):
    """Fringed woven hearth/tavern rug (1008..1034, all pas=0)."""
    H, W = L.shape[1:]
    for y in range(max(0, y0), min(H, y1 + 1)):
        ry = 0 if y == y0 else (3 if y == y1 else (1 if (y - y0) % 2 == 1 else 2))
        for x in range(max(0, x0), min(W, x1 + 1)):
            if mask is not None and not mask[y, x]:
                continue
            rx = 0 if x == x0 else (2 if x == x1 else 1)
            L[z, y, x] = NORDIC_RUG[ry][rx]


def _put_lamp(L, x, y):
    """Subtle 1x2 warm indoor brass floor lamp (2247 pri=1 over 2255 pas=15; MAX 1 per room!)."""
    H, W = L.shape[1:]
    if 0 <= y - 1 < H and 0 <= x < W:
        L[2, y - 1, x] = 2247
    if 0 <= y < H and 0 <= x < W:
        L[1, y, x] = 2255


def _put_stove(L, x, y, kettle=True):
    """Crackling cast-iron hearth stove (kettle=2470/2478, plain=2464/2472)."""
    H, W = L.shape[1:]
    if 0 <= y - 1 < H and 0 <= x < W:
        L[2, y - 1, x] = 2470 if kettle else 2464
    if 0 <= y < H and 0 <= x < W:
        L[1, y, x] = 2478 if kettle else 2472


def _put_dressed_table(L, x, y, item_l=0, item_r=0):
    """2x2 timber table (3466..3475) cleanly dressed with L2 tabletop items (plates, mugs, ledgers, cloth)."""
    L[1, y, x] = 3466; L[1, y, x + 1] = 3467
    L[1, y + 1, x] = 3474; L[1, y + 1, x + 1] = 3475
    if item_l:
        L[2, y, x] = item_l
    if item_r:
        L[2, y, x + 1] = item_r


def _put_dressed_workbench(L, x, y, i0=0, i1=0, i2=0):
    """3x2 timber artisan workbench (4082..4092) dressed with L2 craft props (cloth bolts, tools, ledgers)."""
    L[1, y, x] = 4082; L[1, y, x + 1] = 4083; L[1, y, x + 2] = 4084
    L[1, y + 1, x] = 4090; L[1, y + 1, x + 1] = 4091; L[1, y + 1, x + 2] = 4092
    for dx, t in enumerate((i0, i1, i2)):
        if t:
            L[2, y, x + dx] = t


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
    """104: Tidewater Inn (21x18) — Cozy Coastal Harbor Inn & Maritime Tavern.
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

    # Floor zoning: herringbone slate hearth kitchen + fringed Nordic tavern rug + warm brown woven guest alcove rug!
    _put_9slice(L, ALPINE_SLATE, 8, 5, 13, 6, z=0, mask=floor)
    _put_nordic_rug(L, 7, 8, 12, 12, z=1, mask=floor)
    _put_9slice(L, BROWN_WOVEN_RUG, 14, 8, 16, 11, z=1, mask=floor)
    _doormat(L, 10, 14)

    # Maritime tavern north wall: harbor chart (clear of shelf_bottles & kitchen!), clock at (14,3), arched windows, pilasters & life ring
    _put_grid(L, SEA_CHART, 6, 3, z_rows=(1, 1))
    _put_tf(L, 'clock', 14, 3)
    _sher_window(L, 10, 3)
    _sher_pilaster(L, 8, 3)
    _sher_pilaster(L, 13, 3)
    _sher_window(L, 15, 3)
    _put_tf(L, 'lifering', 16, 3)
    _put_tf(L, 'shelf_bottles', 4, 4)

    # Innkeeper's mahogany reception counter & registry wrapping Innkeeper (4,6) -> pure 0x80 at (4,7)!
    L[1, 5, 6] = 5662
    L[1, 6, 6] = 5658
    for x, t in ((3, 5664), (4, 5665), (5, 5665), (6, 5666)):
        L[1, 7, x] = t
    L[2, 7, 3] = 3428                                     # Open guest registry ledger on left end of reception counter!
    L[2, 7, 5] = 4528                                     # Warm tavern mug & bell on right side of counter (4,7 stays pure 0x80!)

    # Warm hearth kitchen & steaming kettle stove (clear of Inn Guest 2 @ (13,7)!)
    _put_stove(L, 8, 5, kettle=True)
    _put_tf(L, 'kitchen', 9, 4)
    L[1, 6, 8] = 4101                                     # Oak kindling & wash bucket beside hearth

    # Cozy dressed maritime tavern dining tables & backed wooden chairs (clear of Inn Guest @ (8,11)!)
    _put_dressed_table(L, 9, 8, 4537, 4528)               # North tavern table w/ roast plate & steaming cider mug
    L[2, 9, 8] = 2604; L[2, 9, 11] = 2605; L[1, 7, 10] = 2606
    _put_dressed_table(L, 9, 11, 4529, 4537)              # South tavern table beside Inn Guest (8,11) w/ goblet & supper
    L[2, 11, 11] = 2605

    # West hearthside lounge & maritime storage
    _put_grid(L, SOFA_GREY, 3, 9, z_rows=(2, 1))          # Cozy parlor lounge sofa
    _put_lamp(L, 6, 10)                                   # Single warm reading lamp beside parlor sofa (max 1!)
    _put_tf(L, 'barrel_y', 3, 11)                         # Spiced cider keg
    _put_grid(L, SHER_CHEST, 5, 12, z_rows=(2, 1))        # Guest luggage chest

    # Calm coastal guest sleeping alcove (warm cream-quilt timber bed + ocean-blue bunk — zero neon-red clash!)
    _put_grid(L, CREAM_BED, 15, 5, z_rows=(2, 1, 1, 1))   # North cream-quilt inn bed (15..17, 5..8)
    _put_tf(L, 'bunk_b', 16, 10)                          # South calm coastal guest bed (16..17, 10..12)
    _put_grid(L, COAT_STAND, 13, 12, z_rows=(2, 1))       # Guest cloak & hat stand by foyer (clear of clock at 14,3!)
    L[1, 11, 15] = 5580                                   # Traveler's leather satchel
    _put_tree(L, 14, 11, 'fern')
    _put_tree(L, 3, 4, 'parlor')
    L[1, 13, 12] = 7178                                   # Blooming potted coastal flowers by foyer

    return _finalize(L, 104, [(10, 14), (4, 6), (8, 11), (13, 7)])


def build_107():
    """107: Dockmaster's House (20x16) — Coastal Harbor Charts, Manifest Ledger & Freight Office.
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

    # Floor zoning: herringbone coastal slate freight bay + distinct sea-blue maritime study rug (zero red rug!)
    _put_9slice(L, ALPINE_SLATE, 3, 8, 5, 10, z=0, mask=floor)
    _put_9slice(L, BLUE_MARITIME_RUG, 7, 7, 10, 10, z=1, mask=floor)
    _doormat(L, 8, 12)

    # Decluttered maritime harbor wall: shipping map, unclipped life ring, arched window & complete 1x2 harbor painting
    _put_tf(L, 'map_wall', 6, 3)
    _put_tf(L, 'lifering', 10, 3)
    _sher_window(L, 12, 3)
    _put_grid(L, PAINTING_HARBOR_A, 14, 3, z_rows=(1, 1)) # Complete 1x2 framed harbor painting (7137/7145)

    # Dockmaster's office: shipping archives NW + manifest ledger desk cleanly on Dockmaster's ledger (7,5)!
    _put_grid(L, SHER_BOOKCASE, 3, 3, z_rows=(2, 1, 1))
    _put_grid(L, SHER_DESK, 7, 4, z_rows=(2, 1))
    L[2, 5, 7] = 3428                                     # Open unscheduled crossing manifest ledger!
    _put_lamp(L, 9, 6)                                    # Single subtle lantern cleanly clear of north wall & desk (max 1!)
    _put_dressed_table(L, 8, 8, 3428, 4528)               # Coastal chart & tea table on blue maritime rug
    L[2, 9, 7] = 2604; L[2, 9, 10] = 2605                 # Backed timber chairs flanking chart table

    # Unclaimed harbour cargo bay on west slate pad
    _put_tf(L, 'crate_i', 3, 8)
    _put_tf(L, 'barrel_b', 5, 8)
    L[1, 10, 3] = 4101                                    # Tar & oak deck bucket
    _put_grid(L, RODBUCKET_FULL, 5, 10, z_rows=(2, 1))    # Intact fishing/sounding pole bucket (5,11 solid; 6,11 line)

    # East cozy maritime quarters & barometer/log drawer (shifted below lifering so lifering hangs 100% unclipped!)
    _put_tf(L, 'drawer', 10, 5)                           # Barometer & log drawer
    _put_tf(L, 'bed_blue', 12, 5)                         # Calm ocean-blue harbormaster's bed
    L[1, 10, 12] = 5580                                   # Sea chest & satchel
    _put_tree(L, 15, 5, 'parlor')
    _put_tree(L, 14, 9, 'fern')
    L[1, 11, 11] = 3391                                   # Coastal houseplant beside foyer

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
    """123: Weavers' Guildhall (Ground x=3..17) + Warden's Loft (East x=24..34), 41x18.
    Bustling silk-weaving studio with upright timber looms, yarn-spool cabinets, dressed workbenches & tapestries!
    """
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

    # --- GROUND FLOOR: BRIARWICK WEAVERS' GUILDHALL (x=3..17) ---
    # Warm cedar oak planks + soft sage botanical dye pad + rich woven walnut-tan guild runner (ZERO generic red box!)
    _put_9slice(L, SAGE_MARBLE, 14, 9, 17, 11, z=0, mask=floor)
    _put_9slice(L, BROWN_WOVEN_RUG, 8, 9, 12, 13, z=1, mask=floor)
    _doormat(L, 10, 14)

    # North wall: Moth tally board (4,5), colorful yarn-spool thread cabinet, golden woven tapestry, shoji & loft stairs!
    _put_grid(L, BULLETIN_BOARD, 3, 3, z_rows=(1, 1))
    L[1, 5, 3] = 3456; L[1, 5, 4] = 3457                  # Complete 2-wide tally ledge squarely under Moth tally board (4,5)!
    _put_grid(L, LOOM_THREAD_CAB, 6, 3, z_rows=(1, 1))    # 4x2 colorful yarn-spool & warp-thread wall cabinet!
    _put_grid(L, TAPESTRY_GOLD, 10, 3, z_rows=(1, 1))     # Hanging golden woven Briarwick silk tapestry!
    _put_grid(L, SHOJI_BLOSSOM, 12, 3, z_rows=(1, 1))
    # Complete Sheridan stairs finishing cleanly above Loft stairs up (16,6)!
    _put_grid(L, LOFT_STAIRS[1:], 15, 3, z_rows=(2, 1, 1))

    # Upright Timber Weaving Looms, Warp Frames & Dyed Fiber Baskets (west loom gallery — zero oil-painting easels!)
    _put_grid(L, LOOM_WARP_RAIL, 5, 5, z_rows=(2, 1))     # Upright timber warp loom frame #1 (5..6, 5..6)
    _put_grid(L, LOOM_FRAME_B, 3, 8, z_rows=(2, 1))       # Upright blank tapestry loom frame (3, 8..9)
    _put_grid(L, SALT_FIBER_CRATE, 3, 10, z_rows=(2, 1))  # Raw white silk bolts basket squarely on Silk bolts (3,11)!
    _put_grid(L, BLUE_DYE_CATCH_CRATE, 6, 11, z_rows=(2, 1))  # Dyed indigo fiber basket (leaves 3..5,12 WIDE OPEN!)
    L[1, 13, 5] = 2256                                    # Stacked folded white silk cloth bolts in SW corner

    # Twin Dressed Artisan Weaving Workbenches (folded cloth bolts, pattern books & dye jars — NOT blank brown slabs!)
    _put_dressed_workbench(L, 5, 8, 4546, 4547, 3428)     # West loom cutting & pattern bench (5..7, 8..9)
    L[1, 10, 7] = 4077                                    # Weaver's bobbin-winding stool
    _put_dressed_workbench(L, 11, 7, 4547, 4546, 4528)    # East silk-dyeing & folding workbench (11..13, 7..8)
    L[1, 8, 10] = 4077                                    # Companion weaver's stool (leaves Hett 8,7 & Apprentice 12,10 open!)
    _put_lamp(L, 10, 5)                                   # Single warm studio lamp beneath golden tapestry (max 1!)

    # East Loom Warp Frame, Botanical Dye Cart & Indigo Vat (1-tile breathing space clear of FLOWER_CART 15..16,9..10!)
    _put_grid(L, LOOM_WARP_RAIL, 16, 7, z_rows=(2, 1))    # Second upright timber warp loom frame (16..17, 7..8)!
    _put_grid(L, FLOWER_CART, 15, 9, z_rows=(2, 1))       # Dyed-petal & floral mordant cart (15..16, 9..10)
    _put_tf(L, 'barrel_b', 17, 9)                         # Indigo silk dye vat (17, 9..10)
    L[1, 12, 14] = 4101                                   # Oak dye-rinse bucket
    _put_tree(L, 13, 11, 'fern')
    L[1, 13, 13] = 7178                                   # Blooming guild planter beside foyer

    # --- EAST ROOM: WARDEN'S LOFT (x=24..34) ---
    # Warm cedar planks + slate stairwell landing + cream-and-gold medallion woven rug (distinct from ground hall!)
    _put_9slice(L, ALPINE_SLATE, 24, 8, 26, 9, z=0, mask=floor)
    _put_9slice(L, CREAM_MEDALLION_RUG, 27, 7, 31, 10, z=1, mask=floor)
    _sher_window(L, 27, 2)
    _put_grid(L, TAPESTRY_GOLD, 28, 2, z_rows=(1, 1))     # Warden's ceremonial golden woven tapestry!
    _sher_window(L, 31, 2)
    _put_grid(L, SHER_BOOKCASE, 24, 3, z_rows=(2, 1, 1))  # Guild pattern & dye archive bookcase
    _put_tf(L, 'clock', 26, 3)                            # Un-cramped grandfather clock beside archive bookcase!
    _put_lamp(L, 27, 5)                                   # Single warm reading lamp cleanly in apse NW corner (max 1!)
    _put_grid(L, SHER_DESK, 28, 5, z_rows=(2, 1))         # Master Guild ledger desk cleanly on (28,6)!
    L[2, 6, 28] = 3428                                    # Open Guild ledger!
    _put_grid(L, LOOM_FRAME_B, 32, 5, z_rows=(2, 1))      # Warden's upright master loom (32, 5..6)
    _put_grid(L, BLUE_DYE_CATCH_CRATE, 33, 6, z_rows=(2, 1))  # Dyed indigo silk skein crate (33..34, 6..7)
    _put_grid(L, SALT_FIBER_CRATE, 32, 8, z_rows=(2, 1))  # Fine combed white silk bolt basket (32..33, 8..9)
    _put_dressed_table(L, 29, 8, 4546, 4528)              # Swatch inspection & tea table on medallion rug (29..30, 8..9)
    L[2, 9, 28] = 4077                                    # Weaver's stool beside swatch table
    # Visible descending Loft stairwell hatch (24..25, 7..8) + unmistakable step-down threshold mat (24..26, 9) at E11 (25, 9)!
    _put_grid(L, [[4824, 4825], [4832, 4833]], 24, 7, z_rows=(2, 1))
    L[1, 9, 24] = 5512; L[1, 9, 25] = 5513; L[1, 9, 26] = 5514
    L[1, 11, 25] = 2256                                   # Folded white silk stack south of stairwell landing
    L[1, 11, 26] = 4101                                   # Rinse pot cleanly off stairwell landing
    _put_tree(L, 34, 4, 'parlor')
    L[1, 11, 31] = 7178                                   # Blooming potted botanical accent

    return _finalize(
        L, 123,
        [(10, 14), (8, 7), (12, 10), (4, 5), (3, 11), (17, 12),
         (28, 6), (30, 6), (26, 10), (16, 6), (15, 7), (25, 9), (27, 9)]
    )


def build_124():
    """124: Treetop House (West x=3..11) + Briarwick Canopy Lodge / Sanctuary (East x=23..35), 40x18.
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

    # --- ROOM 1: TREETOP HOUSE (x=3..11) — Warm Living-Wood Weaver's Canopy Cottage ---
    _put_9slice(L, BROWN_WOVEN_RUG, 5, 7, 9, 10, z=1, mask=floor)
    _doormat(L, 7, 12)
    _sher_window(L, 7, 3)
    _put_tf(L, 'bunk_o', 3, 5)                              # Warm quilted weaver's bed (3..4, 5..7)
    _put_grid(L, LOOM_FRAME_B, 3, 8, z_rows=(2, 1))         # Upright tapestry loom cleanly on Loom (3,8)!
    _put_grid(L, SHER_BOOKCASE, 9, 3, z_rows=(2, 1, 1))     # Timber bookshelf cleanly on Bookshelf (9,5)!
    _put_stove(L, 6, 5, kettle=True)                        # Cozy steaming canopy kettle hearth!
    L[1, 5, 5] = 4101                                       # Kindling & herbal tea bucket
    _put_dressed_table(L, 6, 8, 3428, 4528)                 # Canopy tea & pattern table (6..7, 8..9)
    L[2, 9, 5] = 2604                                       # Backed wooden chair (Retired Weaver @ 8,8 wide open!)
    _put_lamp(L, 10, 7)                                     # Single reading lamp tucked beside bookshelf (max 1!)
    _put_grid(L, HERB_RACK, 11, 7, z_rows=(2, 1, 1))        # Botanical hanging herb planter along east timber wall
    _put_tree(L, 11, 4, 'parlor')
    L[1, 10, 4] = 7178                                      # Blooming botanical planter
    L[1, 10, 10] = 3391                                     # Cozy potted fern by doorway

    # --- ROOM 2: BRIARWICK CANOPY LODGE & SANCTUARY (x=23..35) ---
    # Warm living-wood Sheridan oak planks across the entire canopy lodge + soft sage botanical planter alcoves
    # + warm cream-and-gold woven sanctuary carpet (ZERO clashing diamond checker floor, ZERO bright mustard!)
    _put_9slice(L, SAGE_MARBLE, 23, 5, 25, 7, z=0, mask=floor)
    _put_9slice(L, SAGE_MARBLE, 33, 5, 35, 7, z=0, mask=floor)
    _put_9slice(L, CREAM_MEDALLION_RUG, 27, 6, 31, 12, z=1, mask=floor)
    _doormat(L, 29, 14)

    # North living-wood apse: central sanctuary mural (29,5) flanked by timber bookshelves & sunlit arched windows!
    _put_grid(L, HOTEL_PORTRAIT, 28, 2, z_rows=(1, 1))
    _put_tf(L, 'table_dark', 28, 4)                         # Sanctuary altar/table cleanly backing Chapel mural (29,5)!
    _put_grid(L, SHER_BOOKCASE, 26, 2, z_rows=(2, 1, 1))    # West apse timber bookshelf (26..27, 2..4)
    _put_grid(L, SHER_BOOKCASE, 31, 2, z_rows=(2, 1, 1))    # East apse timber bookshelf (31..32, 2..4)
    _put_grid(L, COASTAL_ARCH_WIN, 24, 3, z_rows=(1, 1))    # West sunlit canopy window (100% unobstructed!)
    _put_grid(L, COASTAL_ARCH_WIN, 33, 3, z_rows=(1, 1))    # East sunlit canopy window backing Chapel window (33,5)!

    # Cozy Hearth (clear of NW arched window 24..25,3..4!), Living Botanical Planters, Timber Benches & Tea Table!
    _put_lamp(L, 23, 5)                                     # Single warm hearthside reading lamp against west wall (clear of window!)
    _put_stove(L, 24, 6, kettle=True)                       # Cozy crackling hearth stove below window on sage pad (24,5..6)!
    L[1, 6, 25] = 4101                                      # Intact oak kindling bucket beside hearth (replaces chopped 4168!)
    _put_grid(L, BONSAI, 31, 5, z_rows=(2, 1))              # Living canopy bonsai tree beside Chapel window (33,5)
    L[1, 5, 34] = 7178                                      # Blooming botanical planter framing window (33,5 open!)
    _put_grid(L, HERB_RACK, 23, 7, z_rows=(2, 1, 1))        # West wall vertical botanical herb planter (1-tile gap from lamp & tree!)
    _put_grid(L, HERB_RACK, 35, 6, z_rows=(2, 1, 1))        # East wall vertical botanical herb planter!

    # Warm timber lodge benches framing Child in pew (28,9) + cozy canopy tea table in SE reading bay!
    _put_grid(L, WOOD_BENCH, 24, 8, z_rows=(2, 1))
    _put_grid(L, WOOD_BENCH, 32, 8, z_rows=(2, 1))
    _put_grid(L, WOOD_BENCH, 24, 10, z_rows=(2, 1))
    _put_dressed_table(L, 32, 10, 4528, 3428)               # Cozy canopy tea & reading table (32..33, 10..11)!
    L[1, 11, 31] = 2604; L[1, 11, 34] = 2605                # Backed wooden chairs flanking tea table
    L[1, 12, 25] = 7178                                     # SW blooming botanical planter
    L[1, 13, 27] = 7177                                     # Botanical accent framing sanctuary nave
    _put_tree(L, 23, 11, 'parlor')
    _put_tree(L, 35, 11, 'fern')

    return _finalize(
        L, 124,
        [(7, 12), (8, 8), (9, 5), (3, 8), (29, 14), (29, 5), (28, 9), (33, 5)]
    )


def build_125():
    """125: Cutter's House (20x16) — Warm Woodcutter's Cottage w/ Firewood, Timber Workbench, Hearth & Herbs.
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

    # Warm oak planks + compact herringbone slate hearth apron + rustic brown woven rug cleanly under dining area!
    _put_9slice(L, ALPINE_SLATE, 9, 5, 11, 6, z=0, mask=floor)
    _put_9slice(L, BROWN_WOVEN_RUG, 6, 7, 9, 10, z=1, mask=floor)
    _doormat(L, 7, 12)

    # North wall: woodland windows & hanging woodcutter tool rack!
    _sher_window(L, 4, 3)
    _put_grid(L, RAKE_TOOLS, 8, 3, z_rows=(1, 1))           # Hanging woodcutter axes/shovels on timber wall!
    _sher_window(L, 10, 3)

    # Timber woodcutter's workbench & Axe rack squarely on (6,5) (leaves (6,6) 100% open & reachable!)
    _put_dressed_workbench(L, 5, 4, 3428, 4528, 0)          # Timber workbench w/ tally book & whetstone oil jar
    _put_tf(L, 'bunk_o', 3, 5)                              # Warm quilted woodcutter's cot (3..4, 5..7)

    # Crackling hearth stove with steaming kettle & intact oak bucket + stacked firewood lumber in SW!
    _put_stove(L, 10, 5, kettle=True)
    L[1, 5, 11] = 4101                                      # Intact oak hearth water bucket (replaces chopped 4168!)
    _put_grid(L, TIMBER_STACK, 3, 9, z_rows=(2, 1))         # Stacked cut firewood & timber planks on bare oak (3..5, 9..10)!
    _put_lamp(L, 10, 8)                                     # Single warm lamp cleanly clear of bed footboard & stove (max 1!)
    _put_grid(L, HERB_RACK, 11, 7, z_rows=(2, 1, 1))        # Dried woodland herbs hanging on east wall!

    # Cozy dressed cottage supper table (clear of Cutter @ (8,8)!)
    _put_dressed_table(L, 6, 8, 4537, 4528)                 # Hot stew plate & mug on rustic woven rug
    L[1, 8, 5] = 2604                                       # Backed wooden chair facing supper table
    _put_tf(L, 'barrel_y', 10, 9)                           # Cider & resin keg
    L[1, 11, 9] = 3391                                      # Woodland fern pot by foyer

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
    """144: Saltwife's House (20x16) — Unmistakable Coastal Salt-Curing Cottage.
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

    # Floor zoning: herringbone coastal slate salt-curing bay + sea-blue coastal runner (ZERO generic red box!)
    _put_9slice(L, ALPINE_SLATE, 3, 5, 6, 10, z=0, mask=floor)
    _put_9slice(L, BLUE_MARITIME_RUG, 7, 7, 11, 10, z=1, mask=floor)
    _doormat(L, 9, 12)

    # North wall: maritime porthole, coastal arched window & complete 1x2 sea painting (buried SPICE_SHELF removed!)
    _sher_porthole(L, 4, 3)
    _put_grid(L, COASTAL_ARCH_WIN, 10, 3, z_rows=(1, 1))
    _put_grid(L, PAINTING_HARBOR_A, 13, 3, z_rows=(1, 1))    # Complete 1x2 coastal salt-marsh painting (7137/7145)

    # Brine-curing shelf, oak brine tub & salt-evaporation kitchen (zero duplicate ovens!)
    _put_tf(L, 'shelf_bottles', 3, 4)                        # Brine & cure bottle shelf (3..4, 4..5)
    L[1, 5, 5] = 4101                                        # Oak brine-evaporation soaking bucket beside kitchen
    _put_tf(L, 'kitchen', 6, 4)                              # Salt-curing hearth counter (6..9, 4..5)

    # Coastal salt-curing corner around Salt crocks (4,8): burlap salt sacks, white coarse-salt crate & curing barrels!
    _put_grid(L, SALT_FIBER_CRATE, 3, 7, z_rows=(2, 1))      # Coarse white sea-salt crate squarely on Salt crocks (4,8)!
    L[1, 9, 3] = 2256                                        # Tied white burlap sea-salt sack
    L[1, 10, 3] = 2257                                       # Companion burlap coarse-salt bag
    _put_tf(L, 'barrel_b', 5, 9)                             # Blue brine-curing barrel (5, 9..10; 100% clear of ferns!)
    L[1, 10, 6] = 4101                                       # Oak brine-rinse bucket

    # Freestanding salt-raking equipment crate cleanly on Rake (12,9) + dried coastal herbs + ocean-blue sleeping nook!
    _put_tf(L, 'crate_i', 12, 8)                             # Freestanding salt-pan rake & gear crate solidly on Rake (12,9)!
    _put_grid(L, SHER_DESK, 11, 4, z_rows=(2, 1))            # Salt-harvest tally desk
    _put_lamp(L, 13, 6)                                      # Single warm bedside/desk lamp cleanly clear of painting (max 1!)
    _put_tf(L, 'bunk_b', 14, 5)                              # Calm sea-blue cottage bed (14..15, 5..7)
    _put_grid(L, HERB_RACK, 15, 8, z_rows=(2, 1, 1))         # Dried kelp & curing-herb rack on east wall!

    # Cozy coastal supper table on sea-blue runner (clear of Saltwife @ (9,7)!)
    _put_dressed_table(L, 8, 8, 4528, 4537)                  # Steaming tea mug & cured-fish plate
    L[2, 9, 7] = 2604                                        # Backed wooden chair
    _put_tree(L, 7, 10, 'fern')                              # Potted coastal fern cleanly clear of barrel_b (5,9..10)!
    L[1, 11, 11] = 3391                                      # Coastal potted herb by doorway

    return _finalize(L, 144, [(9, 12), (9, 7), (4, 8), (12, 9)])


# ===========================================================================
# GROUP D: EBBMOUTH (161, 162, 163, 164, 165) — Weathered Maritime Stone & Timber
# ===========================================================================

def build_161():
    """161: Ebbmouth Pokémon Center (15x10) — Coastal Slate, Warm Timber Lounges & Cream-Gold Runner.
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

    # Warm coastal Sheridan oak lounge wings inlaid into weathered slate + soft cream-gold welcome runner!
    _put_oak_inlay(L, 1, 4, 4, 7, mask=floor)
    _put_oak_inlay(L, 10, 4, 13, 7, mask=floor)
    _put_9slice(L, CREAM_MEDALLION_RUG, 6, 5, 8, 8, z=1, mask=floor)
    _doormat(L, 7, 9)

    # Stone north wall: coastal arched window, harbor art, life ring, PC (11,1) & Town Map Sea Chart (12,1)
    _put_grid(L, COASTAL_ARCH_WIN, 2, 0, z_rows=(1, 1))
    _put_tf(L, 'lifering', 9, 0)
    L[1, 0, 11] = 5847; L[1, 1, 11] = 5855
    _put_grid(L, SEA_CHART, 12, 0, z_rows=(1, 1))

    # Healing machine on (5,2) & crisp maritime blue-steel reception counter wrapping Nurse (7,2) (ALL 0x80!)
    _put_grid(L, HELP_HEAL, 4, 1, z_rows=(2, 1))
    L[1, 2, 8] = 5843
    for x, t in ((5, 5848), (6, 5849), (7, 5850), (8, 5851)):
        L[1, 3, x] = t

    # West sailors' warming lounge: steaming kettle stove, timber bench, kindling bucket & parlor tree!
    _put_stove(L, 1, 3, kettle=True)
    _put_grid(L, WOOD_BENCH, 1, 5, z_rows=(2, 1))
    L[1, 7, 1] = 4101                                        # Rain-boot & kindling oak bucket
    _put_tree(L, 4, 6, 'parlor')

    # East Professor Larch research nook (keeps (11,2), (12,2) & Larch @ (12,6) 100% OPEN!)
    _put_grid(L, SHER_DESK, 10, 4, z_rows=(2, 1))
    L[2, 4, 10] = 3428                                       # Larch's coastal tide notes
    _put_lamp(L, 12, 4)                                      # Single warm desk lamp beside Larch's study desk (max 1!)
    L[1, 6, 10] = 4077                                       # Study stool
    _put_tree(L, 13, 3, 'palm')
    L[1, 7, 13] = 7178                                       # Blooming coastal planter

    return _finalize(L, 161, [(7, 2), (11, 1), (5, 2), (12, 1), (7, 9), (12, 6)])


def build_162():
    """162: Ebbmouth Mart (11x9) — Coastal Slate & Warm Timber General Outfitter.
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

    # Warm coastal Sheridan oak shopping aisle inlaid into weathered slate + woven coir runner (NO stark blue slab!)
    _put_oak_inlay(L, 4, 2, 8, 6, mask=floor)
    _put_9slice(L, BROWN_WOVEN_RUG, 4, 4, 6, 6, z=1, mask=floor)
    _doormat(L, 4, 8)

    _put_tf(L, 'lifering', 1, 0)
    _put_grid(L, COASTAL_ARCH_WIN, 4, 0, z_rows=(1, 1))
    _put_grid(L, PAINTING_HARBOR_A, 9, 0, z_rows=(1, 1))     # Complete 4-sided 1x2 framed Ebbmouth seascape (7137/7145, clear of lamp!)

    # Crisp maritime blue-steel checkout counter wrapping Mart (2,3) (ALL 0x80 at (3,3) & (1..3,4)!)
    L[1, 2, 3] = 5835
    L[1, 3, 3] = 5843
    L[1, 4, 1] = 5848; L[1, 4, 2] = 5849; L[1, 4, 3] = 5851

    # Stocked maritime outfitter shelves, coarse salt/rope crate & harbor supplies (cramped rodbucket removed!)
    _put_lamp(L, 6, 2)                                       # Single warm window-corner lamp beside shelves (max 1!)
    _put_tf(L, 'shelf_goods', 7, 1)
    _put_tf(L, 'shelf_green', 7, 5)
    _put_grid(L, SALT_FIBER_CRATE, 1, 5, z_rows=(2, 1))      # White sea-salt & hemp rope crate in SW bay
    _put_tf(L, 'barrel_b', 9, 4)
    L[1, 6, 9] = 7178                                        # Potted coastal blooms
    L[1, 7, 6] = 3391                                        # Small coastal fern pot

    return _finalize(L, 162, [(2, 3), (4, 8)])


def build_163():
    """163: Anglers' Guild (13x10) — Lively Ebbmouth Anglers' Guildhall w/ Tackle, Charts, Catch Displays & Hearth!
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

    # Herringbone slate wet-tackle landing + warm walnut-tan hemp guild carpet (breaks generic Ebbmouth blue boxes!)
    _put_9slice(L, ALPINE_SLATE, 1, 6, 4, 9, z=0, mask=floor)
    _put_9slice(L, BROWN_WOVEN_RUG, 5, 4, 9, 7, z=1, mask=floor)
    _doormat(L, 3, 9)

    # Rich Anglers' Guild north wall (strictly inside x=1..11): window, full 2-row chalkboard, chart, life ring & 1x2 print!
    _put_grid(L, COASTAL_ARCH_WIN, 1, 0, z_rows=(1, 1))
    _put_grid(L, CHALKBOARD, 3, 0, z_rows=(1, 1))            # Complete 2-row daily catch & tide-tally chalkboard w/ chalk tray!
    _put_grid(L, SEA_CHART, 7, 0, z_rows=(1, 1))             # Coastal shoals & reef fishing chart
    _put_tf(L, 'lifering', 9, 0)
    _put_grid(L, PAINTING_HARBOR_A, 11, 0, z_rows=(1, 1))    # Complete 1x2 framed harbor trophy print (7137/7145)

    # Fishing rod bucket, hanging tackle/netting rack, fresh-catch crate, salt/bait crate & bait barrels!
    _put_grid(L, RODBUCKET_FULL, 1, 2, z_rows=(2, 1))        # NW intact fishing rod & bobber bucket (1..2, 2..3)
    _put_grid(L, BLUE_DYE_CATCH_CRATE, 1, 4, z_rows=(2, 1))  # Fresh blue coastal catch crate (1..2, 4..5)
    _put_tf(L, 'barrel_b', 1, 6)                             # Salted bait & brine cask (1, 6..7)
    _put_lamp(L, 6, 2)                                       # Single warm chart lamp cleanly between chalkboard & chart (max 1!)
    _put_grid(L, LOOM_WARP_RAIL, 8, 2, z_rows=(2, 1))        # Upright hanging tackle & net-drying rack (8..9, 2..3)!
    _put_grid(L, SALT_FIBER_CRATE, 10, 2, z_rows=(2, 1))     # NE sea-salt & bait-line crate (replaces mirrored twin rod bucket!)

    # Trophy catch & guild chart table + sailor's hearth lounge (clear of Guildmaster @ (5,4)!)
    _put_dressed_table(L, 6, 5, 4537, 3428)                  # Trophy catch supper platter & Anglers' logbook
    L[2, 5, 8] = 2605; L[2, 4, 7] = 2606                     # Backed wooden guild chairs
    _put_grid(L, WOOD_BENCH, 6, 7, z_rows=(2, 1))            # Cozy sailor's bench along south edge
    _put_stove(L, 11, 5, kettle=True)                        # Crackling guildhall kettle stove on east wall!
    L[1, 6, 11] = 4101                                       # Intact oak kindling/water bucket beside stove (replaces chopped 4168!)
    L[1, 8, 5] = 4101                                        # Bait & deck-wash oak bucket
    L[1, 8, 9] = 3391                                        # Potted coastal plant beside sailor's bench

    return _finalize(L, 163, [(3, 9), (5, 4)])


def build_164():
    """164: Reyes House (10x9) — Cozy Coastal Family Cottage w/ Hearth, Supper Table & Cellar Hatch.
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

    # Herringbone slate cellar bay + warm cream-and-gold family rug (ZERO generic S7 red box!)
    _put_9slice(L, ALPINE_SLATE, 1, 5, 2, 6, z=0, mask=floor)
    _put_9slice(L, CREAM_MEDALLION_RUG, 4, 4, 7, 6, z=1, mask=floor)
    _doormat(L, 6, 8)

    # North stone wall: complete 1x2 family painting above bed, unobstructed arched window (6..7,0..1) clear of pantry shelf!
    _put_grid(L, PAINTING_HARBOR_A, 2, 0, z_rows=(1, 1))     # Complete 1x2 framed coastal family painting (7137/7145)
    _put_grid(L, COASTAL_ARCH_WIN, 6, 0, z_rows=(1, 1))      # Shifted to (6..7,0..1) — 100% clear of shelf_bottles (4..5,1..2)!
    _put_tf(L, 'bunk_b', 1, 2)                               # Cozy blue quilted bed (1..2, 2..4)
    _put_stove(L, 3, 2, kettle=True)                         # Crackling family kitchen kettle stove!
    _put_tf(L, 'shelf_bottles', 4, 1)                        # Preserves & spice pantry shelf (4..5, 1..2)
    _put_tf(L, 'bookshelf_s', 8, 1)                          # Family bookshelf in NE corner (8, 1..2)
    _put_lamp(L, 8, 4)                                       # Single warm reading lamp cleanly clear of window & bookshelf (max 1!)

    # COMPLETE 2x2 barred wooden cellar hatch cleanly at (1..2, 5..6) -> solid on Cellar door (1,6)!
    _put_grid(L, [[4824, 4825], [4832, 4833]], 1, 5, z_rows=(2, 1))

    # Dressed family supper table (clear of Mrs Reyes @ (7,4)!)
    _put_dressed_table(L, 4, 4, 4537, 4528)                  # Warm supper plate & teacup on cream medallion rug
    L[2, 5, 6] = 2605                                        # Backed wooden family chair
    _put_tree(L, 8, 5, 'parlor')
    L[1, 7, 3] = 4101                                        # Kindling & wash bucket
    L[1, 7, 7] = 3391                                        # Potted window flower beside entry

    return _finalize(L, 164, [(6, 8), (7, 4), (1, 6)])


def build_165():
    """165: Net-mender's House (10x9) — Coiled Rope/Twine Workbench, Netting Rack, Buoy Crates & Brine Barrels!
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

    # Herringbone slate wet-netting workbay + tailored sea-blue maritime runner
    _put_9slice(L, ALPINE_SLATE, 1, 2, 3, 6, z=0, mask=floor)
    _put_9slice(L, BLUE_MARITIME_RUG, 4, 4, 7, 6, z=1, mask=floor)
    _doormat(L, 6, 8)

    # Balanced stone north wall: arched harbor window, life ring & coastal rigging chart (ZERO overhang!)
    _put_grid(L, COASTAL_ARCH_WIN, 1, 0, z_rows=(1, 1))
    _put_tf(L, 'lifering', 4, 0)
    _put_grid(L, SEA_CHART, 6, 0, z_rows=(1, 1))

    # Net-mender's workshop props: upright netting/rigging frame, rigging poles, buoy crate & coiled rope bench!
    _put_grid(L, LOOM_WARP_RAIL, 1, 2, z_rows=(2, 1))        # Upright wooden fishing-net mending frame (1..2, 2..3)!
    _put_grid(L, RODBUCKET_FULL, 3, 2, z_rows=(2, 1))        # Rigging poles & twine-line bucket (3..4, 2..3)!
    _put_lamp(L, 6, 2)                                       # Single warm workshop lamp beneath rigging chart (max 1!)
    _put_grid(L, BLUE_DYE_CATCH_CRATE, 7, 2, z_rows=(2, 1))  # Cork buoys & net-float crate (7..8, 2..3; clear of 7,4!)
    _put_tf(L, 'bunk_o', 1, 4)                               # Warm quilted sailor's cot (1..2, 4..6)

    # Coiled hawser rope & sailcloth mending workbench (cleanly below fishing line tip, clear of Net-mender @ (7,4)!)
    _put_dressed_table(L, 4, 5, 4546, 3428)                  # Folded mending canvas & rigging logbook (4..5, 5..6)
    L[2, 6, 6] = 4077                                        # Net-mender's wooden stool
    L[1, 6, 3] = 2256                                        # Coiled white hawser rope & hemp twine stack on slate!
    _put_tf(L, 'barrel_b', 8, 5)                             # Tar & brine waterproofing barrel (8, 5..6)
    L[1, 7, 3] = 4101                                        # Oak brine-soaking bucket

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


def main(only=None):
    sel = {int(x) for x in only} if only else set(BUILDERS)
    raw_dir = os.path.join(HERE, 'data', 'raw')
    os.makedirs(raw_dir, exist_ok=True)
    arrays = {}
    for mid, fn in BUILDERS.items():
        if mid not in sel:
            continue
        L = fn()
        arrays[mid] = L
        out_p = os.path.join(raw_dir, f'{mid:03d}.npy')
        np.save(out_p, L.astype(np.int16))
        print(f'Saved {out_p} ({L.shape})')

    # 1. Ferrow's Landing (101_ferrows_landing_interiors.yaml):
    #    TOUCH ONLY selected IDs in (101, 102, 104, 107); LEAVE 103, 105, 106, 108 100% BYTE-IDENTICAL!
    if sel & {101, 102, 104, 107}:
        def tf_101(d):
            mid = d.get('id')
            if mid not in sel:
                return d
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

    # 2. Briarwick (121_briarwick_interiors.yaml): TOUCH ONLY selected IDs!
    if sel & {121, 122, 123, 124, 125, 523, 526}:
        def tf_121(d):
            mid = d.get('id')
            if mid not in sel:
                return d
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

    # 3. Saltmere PC & Mart (141_saltmere_interiors.yaml): ONLY when 141 or 142 selected!
    if sel & {141, 142}:
        def tf_141(d):
            mid = d.get('id')
            if mid not in sel:
                return d
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

    # 4. Saltmere Rooms (143_saltmere_rooms.yaml): TOUCH ONLY selected IDs in (143, 144); LEAVE 145 UNTOUCHED!
    if sel & {143, 144}:
        def tf_143(d):
            mid = d.get('id')
            if mid not in sel:
                return d
            if mid in (143, 144):
                return _wire_raw(d, mid)
            return d

        _update_spec_file(
            '143_saltmere_rooms.yaml',
            "# Saltmere Harbour Office (143), Saltwife's House (144) by wave15_act1_interiors_craft.py; 145 Lantern Theatre preserved.\n",
            tf_143,
        )

    # 5. Ebbmouth Interiors (161_ebbmouth_interiors.yaml): TOUCH ONLY selected IDs!
    if sel & {161, 162, 163, 164, 165}:
        def tf_161(d):
            mid = d.get('id')
            if mid not in sel:
                return d
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
    main(sys.argv[1:] or None)
