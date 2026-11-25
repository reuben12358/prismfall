#!/usr/bin/env python3
"""layouts/wave16_final12_craft.py - Final Map Craft Wave 16 (117 / 117 = 100% of Pokemon Prismfall!).

Upgrades the final 12 interiors & exhibition arena to Rejuvenation V14 / B2W2 void-sculpted interior craft
on Tileset 34 (Prismfall Interior), preserving 100% HEAD event IDs, coordinates, warps, and gameplay parity
(and leaving Wave 8's Map 183 Lumen Arcade 1F 100% byte-identical!):

  Lumen Metropolis Interiors (3 maps):
    1. 182 Lumen Pokemon Center       (15x11, template: pokecenter + tile_edits; ONLY 182 touched!)
    2. 188 Lumen Fossil Lab           (19x12, raw: data/raw/188.npy; intact 3-wide Specimen Incubator!)
    3. 189 Lumen Apartment            (19x12, raw: data/raw/189.npy; metropolitan skyline loft!)
  Verdance Royal Botanical Interiors (2 maps):
    4. 281 Verdance Pokemon Center    (15x11, template: pokecenter + tile_edits)
    5. 282 Verdance Mart              (17x11, template: mart + tile_edits)
  Frostwick Alpine Timber Interiors (6 maps):
    6. 571 Frostwick Pokemon Center   (20x17, palette: interior + tiles + take_events + raw/571.npy)
    7. 572 The Exchange               (21x16, palette: interior + tiles + take_events + raw/572.npy)
    8. 573 The Two Hearths            (27x18, raw: data/raw/573.npy; twin Elowen/Isenmar hearths!)
    9. 574 Rime-silk Loft             (20x17, raw: data/raw/574.npy; tree-hollow atelier + steaming kettle!)
   10. 575 Border House               (21x16, raw: data/raw/575.npy; three-seal customs hall!)
   11. 576 Halvard's Smokehouse       (20x15, raw: data/raw/576.npy; L-shaped curing lodge!)
  Exhibition Arena (1 map):
   12. 990 Prismfall Test Arena       (21x13, template: arena + tile_edits; championship battle pavilion!)

Usage:
    PRISMFALL_GFX=/home/antigravity/pf_engine_run/game/Graphics \\
      /usr/bin/python3 -I mapgen/layouts/wave16_final12_craft.py
"""
import os
import sys
import numpy as np
import yaml

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAY_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, LAY_DIR)

import passguard as PG
from interiorkit import TF

TID = 34
VOID = 5437
RAW_DIR = os.path.join(HERE, 'data', 'raw')
SPEC_DIR = os.path.join(HERE, 'specs')

# Verified Tileset 34 9-slice floor & rug palettes (all pas=0, pri=0)
CREAM_STONE = [[5920, 5921, 5922], [5928, 5929, 5930], [5936, 5937, 5938]]
BLUE_STONE = [[5768, 5769, 5770], [5776, 5777, 5778], [5784, 5785, 5786]]
SAGE_MARBLE = [[1104, 1105, 1106], [1112, 1113, 1114], [1120, 1121, 1122]]
IVORY_MARBLE = [[1107, 1108, 1109], [1115, 1116, 1117], [1123, 1124, 1125]]
ALPINE_SLATE = [[1152, 1153, 1154], [1160, 1161, 1162], [1168, 1169, 1170]]
BLUE_CARPET = [[7496, 7497, 7498], [7504, 7505, 7506], [7512, 7513, 7514]]
RED_CARPET = [[7172, 7173, 7174], [7180, 7181, 7182], [7188, 7189, 7190]]
SHER_RUG = [[5411, 5412, 5413], [5419, 5420, 5421], [5427, 5428, 5429]]
NORDIC_RUG = [[1008, 1009, 1010], [1016, 1017, 1018], [1024, 1025, 1026], [1032, 1033, 1034]]
POKEBALL_MEDAL = [
    [536, 537, 538, 539],
    [544, 545, 546, 547],
    [552, 553, 554, 555],
    [560, 561, 562, 563],
]
ARENA_BLUE_COURT = [
    [5616, 5617, 5618, 5619, 5620, 5621, 5622],
    [5624, 5625, 5626, 5627, 5628, 5629, 5630],
    [5632, 5633, 5634, 5635, 5636, 5637, 5638],
    [5640, 5641, 5642, 5643, 5644, 5645, 5646],
    [5648, 5649, 5650, 5651, 5652, 5653, 5654],
]
LABTANK_FULL = [
    [4784, 4785, 4786],
    [4792, 4793, 4794],
    [4800, 4801, 4802],
    [4808, 4809, 4810],
]
FLOOR_EMERALD = 501  # luminous emerald-diamond conservatory tile (pas=0)
FLOOR_CYAN = 725     # glowing electric-cyan Lattice floor accent (pas=0)


# ==============================================================================
# SHARED HELPERS
# ==============================================================================
def _put_tf(L, name, x, y):
    rows, top = TF[name]
    H, W = L.shape[1], L.shape[2]
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


def _put_grid(L, grid, x, y, z_rows=None):
    H, W = L.shape[1], L.shape[2]
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


def _put_9slice(L, tiles9, x0, y0, x1, y1, z=0, mask=None):
    for y in range(y0, y1 + 1):
        ry = 0 if y == y0 else (2 if y == y1 else 1)
        for x in range(x0, x1 + 1):
            if mask is not None and not mask[y, x]:
                continue
            rx = 0 if x == x0 else (2 if x == x1 else 1)
            L[z, y, x] = tiles9[ry][rx]


def _put_nordic_rug(L, x0, y0, x1, y1, z=1):
    """Place the fringed Nordic alpine rug (1008..1034, 3x4) scaled cleanly to any >=3x2 box."""
    for y in range(y0, y1 + 1):
        if y == y0:
            ry = 0
        elif y == y1:
            ry = 3
        else:
            ry = 1 if (y - y0) % 2 == 1 else 2
        for x in range(x0, x1 + 1):
            rx = 0 if x == x0 else (2 if x == x1 else 1)
            L[z, y, x] = NORDIC_RUG[ry][rx]


def _put_plant(L, x, y, top_t=7126, bot_t=7134):
    """Place an intact 1x2 tall potted plant/palm (top pri=5 on layer 2, pot pas=15 on layer 1)."""
    L[2, y - 1, x] = top_t
    L[1, y, x] = bot_t


def _put_lamp(L, x, y, ruby=True):
    """Place an intact 1x2 brass floor lamp (ruby=2244/2252, warm candle=2247/2255)."""
    L[2, y - 1, x] = 2244 if ruby else 2247
    L[1, y, x] = 2252 if ruby else 2255


def _put_stove(L, x, y, kettle=False):
    """Place an intact 1x2 crackling cast-iron woodstove (kettle=2470/2478, plain=2464/2472)."""
    L[2, y - 1, x] = 2470 if kettle else 2464
    L[1, y, x] = 2478 if kettle else 2472


def _put_doormat(L, cx, y, style='sheridan'):
    """Place a 3-wide or 1-wide entry mat centered on Exit (cx, y)."""
    if style == 'sheridan':
        for i, xx in enumerate((cx - 1, cx, cx + 1)):
            L[1, y, xx] = 5512 + i
    elif style == 'red':
        L[1, y, cx] = 444
    elif style == 'blue':
        L[1, y, cx] = 392


def _seam_sheridan(L, floor, wall_rows=2, stone_walls=False):
    """Paint warm Sheridan timber (or alpine stone) north walls & dark-timber void border around `floor`."""
    H, W = floor.shape
    L[0, :, :] = VOID
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
                top_row = (y == 0) or not floor[y - 1, x]
                left_edge = (x == 0) or not floor[y, x - 1]
                if top_row:
                    L[0, y, x] = 5352 if left_edge else 5353 + (x - 3) % 3
                else:
                    L[0, y, x] = 5360 if left_edge else 5361 + (x - 3) % 3
            elif wall_face[y, x]:
                is_lower = (y + 1 < H and floor[y + 1, x])
                left_end = (x == 0) or not wall_face[y, x - 1]
                right_end = (x + 1 >= W) or not wall_face[y, x + 1]
                if stone_walls:
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
    return wall_face


def _seam_cyber(L, floor, wall_rows=2, base_floor='diamond'):
    """Paint sleek Lumen Chrisola dark-steel & electric-blue walls/trim around `floor` (matching Wave 8's 183)."""
    H, W = floor.shape
    L[0, :, :] = VOID
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
                if base_floor == 'slate':
                    L[0, y, x] = 7091 if (x + y) % 2 == 0 else 7092
                else:
                    L[0, y, x] = 7737 if (x + y) % 2 == 0 else 7745
            elif wall_face[y, x]:
                is_lower = (y + 1 < H and floor[y + 1, x])
                left_end = (x == 0) or not wall_face[y, x - 1]
                right_end = (x + 1 >= W) or not wall_face[y, x + 1]
                if left_end:
                    L[0, y, x] = 7536 if is_lower else 7520
                elif right_end:
                    L[0, y, x] = 7538 if is_lower else 7522
                else:
                    L[0, y, x] = 7537 if is_lower else 7521
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
                    L[0, y, x] = 7564
                elif S and W_:
                    L[0, y, x] = 7563
                elif N and E:
                    L[0, y, x] = 7556
                elif N and W_:
                    L[0, y, x] = 7555
                elif S:
                    L[0, y, x] = 7569
                elif N:
                    L[0, y, x] = 7553
                elif E:
                    L[0, y, x] = 7562
                elif W_:
                    L[0, y, x] = 7560
                elif SE:
                    L[0, y, x] = 7570
                elif SW:
                    L[0, y, x] = 7568
                elif NE:
                    L[0, y, x] = 7554
                elif NW:
                    L[0, y, x] = 7552
    return wall_face


def _compress_tile_edits(L):
    """Encode (3, H, W) array cleanly as compact build.py tile_edits."""
    _, H, W = L.shape
    edits = [[0, 0, 0, W, H, 0], [1, 0, 0, W, H, 0], [2, 0, 0, W, H, 0]]
    for z in range(3):
        for y in range(H):
            x = 0
            while x < W:
                t = int(L[z, y, x])
                if t == 0:
                    x += 1
                    continue
                x1 = x + 1
                while x1 < W and int(L[z, y, x1]) == t:
                    x1 += 1
                w = x1 - x
                if w == 1:
                    edits.append([z, x, y, t])
                else:
                    edits.append([z, x, y, w, 1, t])
                x = x1
    return edits


def _layers_to_tiles_list(L):
    """Encode (3, H, W) array as explicit `tiles:` entries for `palette: interior` + `take_events` specs."""
    _, H, W = L.shape
    out = []
    for z in range(3):
        for y in range(H):
            for x in range(W):
                t = int(L[z, y, x])
                if (z == 0 and t == VOID) or (z > 0 and t == 0):
                    continue
                out.append({'tile': t, 'at': [x, y], 'layer': z})
    return out


def _save_raw(mid, L):
    os.makedirs(RAW_DIR, exist_ok=True)
    np.save(os.path.join(RAW_DIR, f'{mid:03d}.npy'), L.astype(np.int16))


# ==============================================================================
# MAP 1: 182 Lumen Pokemon Center (15x11, TS 34) — LEAVES 183 100% BYTE-IDENTICAL!
# ==============================================================================
def build_182():
    # Exact HEAD events (7/7):
    #   #2 Nurse @(7,2), #3 PC @(11,1), #4 Healing balls @(5,2),
    #   #6 Town Map @(12,1), #7 Exit @(7,9) [arrival (7,8)],
    #   #8 Gale Post desk @(3,6) [NPC 16 down], #9 News screen @(11,6)
    W, H = 15, 11
    L = np.zeros((3, H, W), dtype=np.int32)

    floor = np.zeros((H, W), dtype=bool)
    floor[2:8, 1:14] = True        # Main neon-marble lobby (x=1..13, y=2..7)
    floor[7, 1] = False            # SW void chamfer
    floor[7, 13] = False           # SE void chamfer
    floor[8, 5:10] = True          # Stepped foyer vestibule (x=5..9, y=8)
    floor[9, 6:9] = True           # Recessed entry door notch (x=6..8, y=9; Exit @ 7,9!)

    _seam_cyber(L, floor, wall_rows=2, base_floor='diamond')

    # Multi-zone metropolitan floor: luminous pale blue-marble heart + 4x4 Pokeball Medallion + cyan Lattice pads!
    _put_9slice(L, BLUE_STONE, 4, 2, 10, 7, z=0, mask=floor)
    _put_grid(L, POKEBALL_MEDAL, 5, 4, z_rows=(0, 0, 0, 0))
    # Electric-blue welcome carpet runner from Exit (7,9) up to Pokeball medallion
    _put_9slice(L, BLUE_CARPET, 6, 8, 8, 9, z=1)
    L[1, 9, 7] = 444  # crisp red-white welcome mat on Exit (7,9)
    # Dark slate floor pads under West Gale Post bay & East News Lounge + glowing cyan Lattice floor accents!
    for y in range(4, 7):
        for x in (1, 2, 3):
            L[0, y, x] = 7091 if (x + y) % 2 == 0 else 7092
        for x in (11, 12, 13):
            L[0, y, x] = 7091 if (x + y) % 2 == 0 else 7092
    for gx, gy in ((4, 4), (10, 4), (4, 7), (10, 7), (5, 8), (9, 8)):
        L[0, gy, gx] = FLOOR_CYAN

    # North wall architectural detail (y=0..1): sleek telemetry monitors, authentic PC @(11,1), full 2x2 Town Map @(12,1)
    _put_grid(L, [[7136, 7137], [7144, 7145]], 2, 0, z_rows=(1, 1))
    L[1, 0, 7] = 7312; L[1, 0, 8] = 7313; L[1, 0, 9] = 7314  # Illuminated header display above Nurse
    L[1, 1, 7] = 7320; L[1, 1, 8] = 7321; L[1, 1, 9] = 7322
    # #3 PC @(11,1): authentic Pokemon Center PC (7076/7084) cleanly interactable from (11,2) facing UP!
    L[1, 0, 11] = 7076; L[1, 1, 11] = 7084
    # #6 Town Map @(12,1): complete 2x2 framed Velmora transit map (4730..4739) cleanly interactable from (12,2)!
    _put_grid(L, [[4730, 4731], [4738, 4739]], 12, 0, z_rows=(1, 1))

    # Healing Machine (2706..2723) at (4..5, 1..3) -> ball tray 2715 squarely on #4 Healing balls @(5,2)!
    _put_tf(L, 'heal', 4, 1)
    # Help Center Sleek Blue Curved Counter (0x80 flags!) wrapping Nurse @(7,2):
    #   (6,3)=5849, (7,3)=5850, (8,3)=5852, (9,3)=5851, (9,2)=5843 (flower vase right corner!)
    L[1, 3, 6] = 5849
    L[1, 3, 7] = 5850  # 0x80 counter directly in front of #2 Nurse @(7,2) -> heal from (7,4)!
    L[1, 3, 8] = 5852
    L[1, 3, 9] = 5851
    L[1, 2, 9] = 5843

    # West Gale Post Express Bay (x=1..3, y=4..6): mail crates & desk beside #8 Gale Post desk @(3,6)!
    # Keep (3,6), (3,7), (4,6), (2,7) open walkable so player talks smoothly to Gale Post NPC!
    L[1, 5, 1] = 4170; L[1, 5, 2] = 4171  # Express parcel crates
    L[1, 6, 1] = 4178; L[1, 6, 2] = 4179
    L[2, 4, 1] = 5580                     # Gale Post mail satchel on parcel stack
    _put_plant(L, 1, 3, 7126, 7134)       # Sleek parlor ficus in NW corner

    # East Anniversary News Kiosk (x=11..13, y=5..6):
    # #9 News screen @(11,6): crisp blue widescreen terminal (2704..2713) squarely at (11..12, 5..6)!
    _put_tf(L, 'tv', 11, 5)
    L[1, 6, 13] = 2255; L[2, 5, 13] = 2247  # Warm floor lamp framing east kiosk
    _put_plant(L, 13, 3, 7126, 7134)        # Matching parlor ficus in NE corner

    # Cozy vestibule framing (x=5,8 & x=9,8)
    _put_lamp(L, 5, 8, ruby=False)
    _put_lamp(L, 9, 8, ruby=False)

    PG.guard(L, TID, [(7, 9), (7, 8), (7, 4), (7, 2), (5, 2), (11, 2), (12, 2), (3, 6), (3, 7), (11, 7)], 'map 182')
    _save_raw(182, L)

    # CRITICAL: Update ONLY Map 182 in 182_lumen_pc_arcade.yaml; keep Map 183 100% BYTE-IDENTICAL!
    spec_path = os.path.join(SPEC_DIR, '182_lumen_pc_arcade.yaml')
    raw_txt = open(spec_path, 'r', encoding='utf-8').read()
    parts = raw_txt.split('\n---\n')
    assert len(parts) == 2, f"Expected 2 docs in 182_lumen_pc_arcade.yaml, got {len(parts)}"
    old182 = yaml.safe_load(parts[0])
    doc183_verbatim = parts[1]
    assert old182.get('id') == 182

    new182 = {
        'id': 182,
        'name': old182['name'],
        'parent': old182['parent'],
        'template': 'pokecenter',
        'exit_link': old182['exit_link'],
        'drop_template_events': old182['drop_template_events'],
        'tileset': TID,
        'bgm': old182['bgm'],
        'tone': [-6, -4, 10, 4],
        'metadata': old182['metadata'],
        'stretch': [['y', 9, 1]],
        'tile_edits': _compress_tile_edits(L),
        'events': old182['events'],
    }
    doc182_txt = (
        "# Map 182 revamped by layouts/wave16_final12_craft.py (Wave 16 Final Map Craft; data/raw/182.npy).\n"
        "# Map 183 below is preserved 100% byte-identical from Wave 8.\n"
        + yaml.safe_dump(new182, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True)
    )
    open(spec_path, 'w', encoding='utf-8').write(doc182_txt + '\n---\n' + doc183_verbatim)
    print(f"Built 182 {L.shape} ({len(new182['tile_edits'])} edits); 183 preserved verbatim.")
    return L


# ==============================================================================
# MAP 2: 188 Lumen Fossil Lab (19x12, TS 34) — Paleontology Museum & 3-Wide Incubator!
# ==============================================================================
def build_188():
    # Exact HEAD events (2/2): #1 Exit @(6,9) [arrival (6,8)], #2 Fossil scientist @(5,5)
    W, H = 19, 12
    L = np.zeros((3, H, W), dtype=np.int32)

    floor = np.zeros((H, W), dtype=bool)
    floor[3:9, 1:8] = True         # West Field Intake & Excavation Bay (x=1..7, y=3..8)
    floor[8, 1] = False            # SW void chamfer
    floor[9, 5:8] = True           # Recessed entry door notch (x=5..7, y=9; Exit @ 6,9!)
    floor[2:11, 8:14] = True       # Central Vaulted Paleontology Museum Gallery (x=8..13, y=2..10)
    floor[10, 8] = False           # Beveled gallery SW shoulder
    floor[10, 13] = False          # Beveled gallery SE shoulder
    floor[3:10, 14:18] = True      # East Lattice-Current Revival Chamber (x=14..17, y=3..9)
    floor[9, 17] = False           # SE chamber chamfer

    _seam_cyber(L, floor, wall_rows=2, base_floor='slate')

    # Multi-zone museum flooring:
    # Central Gallery: luminous cream-gold museum stone framed by dark diamond perimeter
    for y in range(2, 11):
        for x in range(8, 14):
            if floor[y, x]:
                L[0, y, x] = 7737 if (x + y) % 2 == 0 else 7745
    _put_9slice(L, CREAM_STONE, 9, 3, 12, 9, z=0)
    # West entry crimson museum carpet leading from Exit (6,9) to Fossil Scientist @(5,5)
    _put_9slice(L, RED_CARPET, 5, 6, 7, 9, z=1)
    L[1, 9, 6] = 444  # welcome mat right on Exit (6,9)
    # East Lattice-Current glowing cyan conduits feeding the 3-wide Revival Incubator!
    for gx, gy in ((13, 5), (14, 6), (15, 6), (16, 6), (14, 7), (16, 7), (15, 8)):
        L[0, gy, gx] = FLOOR_CYAN

    # North wall architectural dressings:
    # West Bay wall (y=1..2): Velmora Bone Sands excavation map & sleek telemetry displays
    _put_grid(L, [[4730, 4731], [4738, 4739]], 2, 1, z_rows=(1, 1))
    _put_grid(L, [[7136, 7137], [7144, 7145]], 5, 1, z_rows=(1, 1))
    # Central Vaulted Gallery wall (y=0..1): Ancient Fossil Museum Bookcases & complete 2x2 geology frame!
    _put_grid(L, [[4650, 4651, 4652], [4658, 4659, 4660], [4666, 4667, 4668]], 9, 0, z_rows=(2, 2, 1))
    _put_grid(L, [[7141, 7142], [7149, 7150]], 12, 0, z_rows=(1, 1))
    # East Revival Chamber wall (y=1..2): intact 1x2 telemetry chart above server rack
    _put_grid(L, [[7140], [7148]], 17, 1, z_rows=(1, 1))

    # West Excavation & Scientist Intake Desk (around #2 Fossil scientist @(5,5)):
    # Scientist stands cleanly at (5,5) facing down -> keep (5,5), (5,6), (6,5), (6,6) open!
    _put_grid(L, [[2515, 2516], [2523, 2524]], 2, 4, z_rows=(2, 1))  # (2..3, 4..5) Solid mahogany intake desk!
    # Ancient fossil rock samples & stone specimen plinths in SW alcove (x=1..3, y=6..8) — pure amber rock, ZERO flowers!
    _put_grid(L, [[4749, 4750, 4751], [4757, 4750, 4765]], 1, 6, z_rows=(1, 1))
    L[1, 8, 2] = 4763; L[1, 8, 3] = 4764   # Intact fossil display plinths
    _put_plant(L, 1, 4, 7126, 7134)        # NW specimen hall ficus

    # Central Paleontology Specimen Gallery (x=8..13, y=3..10):
    # Twin Glass Museum Showcase Cases (7120..7122 pri=5 top, 7128..7130 solid showcase base!)
    _put_grid(L, [[7120, 7121, 7122], [7128, 7129, 7130]], 9, 4, z_rows=(2, 1))   # North Fossil Display Case
    _put_grid(L, [[7120, 7121, 7122], [7128, 7129, 7130]], 9, 7, z_rows=(2, 1))   # South Amber & Bone Display Case
    _put_lamp(L, 8, 3, ruby=False)
    _put_lamp(L, 13, 3, ruby=False)
    _put_plant(L, 9, 10, 5431, 5439)       # South gallery botanical fern
    _put_plant(L, 12, 10, 5431, 5439)

    # East Lattice-Current Revival Chamber (x=14..17, y=3..9):
    # COMPLETE INTACT 3-WIDE SPECIMEN REVIVAL INCUBATOR (4784..4810) cleanly at (14..16, 2..5)!
    _put_grid(L, LABTANK_FULL, 14, 2, z_rows=(2, 1, 1, 1))
    # Authentic Tall Blue Lattice Telemetry Server Rack (2795/2803/2811) at (17, 3..5)
    L[2, 3, 17] = 2795; L[1, 4, 17] = 2803; L[1, 5, 17] = 2811
    # Scientific Revival Control Console (4779..4789) at (14..16, 8..9) (leaves (14..16, 6..7) wide open!)
    _put_grid(L, [[4779, 4780, 4781], [4787, 4788, 4789]], 14, 8, z_rows=(2, 1))

    PG.guard(L, TID, [(6, 9), (6, 8), (5, 5), (5, 6)], 'map 188')
    _save_raw(188, L)

    spec_path = os.path.join(SPEC_DIR, '188_lumen_fossil_lab.yaml')
    old = yaml.safe_load(open(spec_path))
    new_spec = {
        'id': 188,
        'name': old['name'],
        'parent': old['parent'],
        'metadata': old['metadata'],
        'bgm': old.get('bgm', ''),
        'tone': [-6, -2, 6, 2],
        'raw': 'data/raw/188.npy',
        'tileset': TID,
        'events': old['events'],
    }
    hdr = "# GENERATED by mapgen/layouts/wave16_final12_craft.py (Wave 16 Final Map Craft): Lumen Fossil Lab (188).\n"
    open(spec_path, 'w').write(hdr + yaml.safe_dump(new_spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))
    print(f"Built 188 {L.shape} -> data/raw/188.npy")
    return L


# ==============================================================================
# MAP 3: 189 Lumen Apartment (19x12, TS 34) — High-Rise Skyline Metropolitan Loft!
# ==============================================================================
def build_189():
    # Exact HEAD events (2/2): #1 Exit @(6,9) [arrival (6,8)], #2 Retired pilot @(4,5)
    W, H = 19, 12
    L = np.zeros((3, H, W), dtype=np.int32)

    floor = np.zeros((H, W), dtype=bool)
    floor[3:9, 1:8] = True         # West Pilot's Living Room & Study (x=1..7, y=3..8)
    floor[8, 1] = False            # SW chamfer
    floor[9, 5:8] = True           # Recessed entry hall (x=5..7, y=9; Exit @ 6,9!)
    floor[3:10, 8:13] = True       # Central Open-Plan Kitchen & Dining Nook (x=8..12, y=3..9)
    floor[2:10, 13:18] = True      # East Elevated Metropolitan Bedroom Suite (x=13..17, y=2..9)
    floor[9, 17] = False           # SE chamfer

    _seam_sheridan(L, floor, wall_rows=2)

    # Multi-zone metropolitan loft flooring:
    # Central Kitchen Nook: crisp ivory marble tile (x=8..12, y=3..6) contrasting warm hardwood planks!
    _put_9slice(L, IVORY_MARBLE, 8, 3, 12, 6, z=0)
    # Entry stone pad & doormat at (5..7, 9)
    for xx in (5, 6, 7):
        L[0, 9, xx] = IVORY_MARBLE[2][xx - 5]
    _put_doormat(L, 6, 9, 'sheridan')
    # Plush crimson living rug in West Lounge (x=2..5, y=6..8)
    _put_9slice(L, RED_CARPET, 2, 6, 5, 8, z=1)
    # Soft royal-blue carpet in East Bedroom Suite (x=13..16, y=5..8)
    _put_9slice(L, BLUE_CARPET, 13, 5, 16, 8, z=1)

    # Panoramic Skyline Windows & Pilot's Wall Art along North Walls:
    # Sunlit arched metropolitan skyline window (2086..2095) centered over Pilot's living room at (3..4, 1..2)!
    _put_grid(L, [[2086, 2087], [2094, 2095]], 3, 1, z_rows=(1, 1))
    # Complete 2x2 framed Skyreach flight route chart on wall (6..7, 1..2)
    _put_grid(L, [[4730, 4731], [4738, 4739]], 6, 1, z_rows=(1, 1))
    # Crisp Sheridan kitchen window cleanly to the right of fridge (12, 1..2)
    L[0, 1, 12] = 5544; L[0, 2, 12] = 5552
    # Sunlit arched high-rise bedroom window (2086..2095) cleanly at (15..16, 0..1)
    _put_grid(L, [[2086, 2087], [2094, 2095]], 15, 0, z_rows=(1, 1))

    # West Pilot's Living Room & Study (around #2 Retired pilot @(4,5)):
    # Keep (4,5), (4,6), (5,5), (3,5) completely open!
    _put_tf(L, 'bookcase', 1, 3)           # (1..2, 3..4) Aviation logbook shelf
    _put_tf(L, 'table_tea', 2, 6)          # (2..3, 6..7) Coffee table on plush crimson rug
    L[1, 7, 1] = 5580                      # Retired pilot's leather flight suitcase
    _put_lamp(L, 4, 8, ruby=True)          # Warm ruby floor lamp framing entry
    _put_plant(L, 7, 4, 7126, 7134)        # Tall metropolitan parlor ficus dividing living & kitchen

    # Central Open-Plan Kitchen & Dining Terrace (x=8..12, y=3..9):
    # Modern white-and-wood kitchen counter, stove & fridge (3504..3515) at (8..11, 2..3)
    _put_grid(L, [[3504, 3505, 3506, 3507], [3512, 3513, 3514, 3515]], 8, 2, z_rows=(2, 1))
    _put_tf(L, 'table_w', 9, 5)            # (9..10, 5..7) Modern wood dining table
    L[1, 6, 8] = 4077                      # Dining stool west
    L[1, 6, 11] = 4077                     # Dining stool east
    # Sleek modern hotel sofa (7571..7581) at (9..11, 8..9)
    _put_grid(L, [[7571, 7572, 7573], [7579, 7580, 7581]], 9, 8, z_rows=(2, 1))

    # East Elevated Metropolitan Bedroom Suite (x=13..17, y=2..9):
    # Cozy modern amber-quilt bed (3509..3535, 3x4) cleanly at (15..17, 2..5)
    _put_grid(L, [[3509, 3510, 3511], [3517, 3518, 3519], [3525, 3526, 3527], [3533, 3534, 3535]], 15, 2, z_rows=(2, 1, 1, 1))
    # Grandfather clock (3633..3649, 1x3) flush against north bedroom wall at (13, 0..2)!
    _put_tf(L, 'clock', 13, 0)
    # Mirrored vanity dresser (3621..3638, 2x3) at (15..16, 6..8)
    _put_tf(L, 'dresser_mirror', 15, 6)
    _put_plant(L, 14, 9, 5431, 5439)       # Lush bedroom fern beside SE chamfer
    _put_lamp(L, 13, 8, ruby=False)

    PG.guard(L, TID, [(6, 9), (6, 8), (4, 5), (4, 6)], 'map 189')
    _save_raw(189, L)

    spec_path = os.path.join(SPEC_DIR, '189_lumen_apartment.yaml')
    old = yaml.safe_load(open(spec_path))
    new_spec = {
        'id': 189,
        'name': old['name'],
        'parent': old['parent'],
        'metadata': old['metadata'],
        'bgm': old.get('bgm', ''),
        'tone': [8, 4, -4, 0],
        'raw': 'data/raw/189.npy',
        'tileset': TID,
        'events': old['events'],
    }
    hdr = "# GENERATED by mapgen/layouts/wave16_final12_craft.py (Wave 16 Final Map Craft): Lumen Apartment (189).\n"
    open(spec_path, 'w').write(hdr + yaml.safe_dump(new_spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))
    print(f"Built 189 {L.shape} -> data/raw/189.npy")
    return L


# ==============================================================================
# MAPS 4 & 5: 281 Verdance Pokemon Center (15x11) & 282 Verdance Mart (17x11)
# Unified seamlessly with Wave 10's 280 Verdance Royal Botanical Terraces!
# ==============================================================================
def build_281_layers():
    # Exact HEAD events (6/6):
    #   #2 Nurse @(7,2), #3 PC @(11,1), #4 Healing balls @(5,2),
    #   #6 Town Map @(12,1), #7 Exit @(7,9) [arrival (7,8)], #8 Pilgrim @(12,6) [dir=left]
    W, H = 15, 11
    L = np.zeros((3, H, W), dtype=np.int32)

    floor = np.zeros((H, W), dtype=bool)
    floor[2:8, 1:14] = True        # Main botanical lobby (x=1..13, y=2..7)
    floor[7, 1] = False            # SW chamfer
    floor[7, 13] = False           # SE chamfer
    floor[8, 5:10] = True          # Stepped foyer (x=5..9, y=8)
    floor[9, 6:9] = True           # Recessed entry door notch (x=6..8, y=9; Exit @ 7,9!)

    _seam_sheridan(L, floor, wall_rows=2)

    # Multi-zone Royal Botanical Flooring:
    # Emerald-diamond conservatory wings (x=1..3 & x=11..13) framing Royal Sage & Ivory Marble Center!
    for y in range(2, 8):
        for x in (1, 2, 3, 11, 12, 13):
            if floor[y, x]:
                L[0, y, x] = FLOOR_EMERALD
    _put_9slice(L, SAGE_MARBLE, 4, 2, 10, 7, z=0, mask=floor)
    _put_9slice(L, IVORY_MARBLE, 5, 8, 9, 8, z=0)
    _put_9slice(L, IVORY_MARBLE, 6, 9, 8, 9, z=0)
    # 4x4 Cream-and-Gold Pokeball Medallion dead-center (5..8, 4..7)!
    _put_grid(L, POKEBALL_MEDAL, 5, 4, z_rows=(0, 0, 0, 0))
    # Royal Crimson-and-Gold Sheridan Welcome Runner from Exit (7,9) to Medallion
    _put_9slice(L, SHER_RUG, 6, 8, 8, 9, z=1)
    L[1, 9, 7] = 444

    # Sunlit Arched Verdance Windows, authentic PC @(11,1), full 2x2 Town Map @(12,1) along North Wall (y=0..1):
    for wx in (2, 8, 10):
        L[0, 0, wx] = 5544; L[0, 1, wx] = 5552
    L[1, 0, 11] = 7076; L[1, 1, 11] = 7084  # #3 PC @(11,1) cleanly interactable from (11,2)!
    _put_grid(L, [[4730, 4731], [4738, 4739]], 12, 0, z_rows=(1, 1))  # #6 Town Map @(12,1)!
    _put_tf(L, 'painting1', 6, 0)           # Pastoral botanical artwork behind Nurse

    # Healing Machine (2706..2723) at (4..5, 1..3) -> ball tray 2715 squarely on #4 Healing balls @(5,2)!
    _put_tf(L, 'heal', 4, 1)
    # Warm Royal Botanical Reception Counter (5944..5967, REAL 0x80 flags + floral bouquet!):
    L[1, 3, 6] = 5961
    L[1, 3, 7] = 5962  # 0x80 counter directly in front of #2 Nurse @(7,2) -> heal from (7,4)!
    L[1, 3, 8] = 5964
    L[1, 3, 9] = 5963
    L[1, 2, 9] = 5955  # Blooming bouquet counter corner!

    # West Botanical Conservatory Lounge (x=1..3, y=3..6):
    _put_grid(L, [[5422], [5430], [5438]], 1, 2, z_rows=(2, 1, 1))  # Potted herb & flower rack
    _put_tf(L, 'table_tea', 2, 5)          # (2..3, 5..6) Botanical tea table
    L[1, 6, 1] = 7178                      # Blooming rose planter
    _put_plant(L, 3, 3, 7874, 7882)        # Grand conservatory palm

    # East Pilgrim Sanctuary Reading Alcove (around #8 Pilgrim @(12,6) facing LEFT):
    # Keep (12,6), (11,6), (12,5), (12,7), (11,5), (11,7) open!
    _put_plant(L, 13, 3, 7874, 7882)       # NE grand conservatory palm
    L[1, 5, 13] = 7177                     # Moss floral planter beside Pilgrim
    L[1, 6, 13] = 7178                     # Blooming rose planter behind Pilgrim
    L[1, 7, 12] = 7177                     # South conservatory flower planter below Pilgrim
    _put_lamp(L, 5, 8, ruby=True)          # Warm vestibule lamps
    _put_lamp(L, 9, 8, ruby=True)

    PG.guard(L, TID, [(7, 9), (7, 8), (7, 4), (7, 2), (5, 2), (11, 2), (12, 2), (12, 6), (11, 6)], 'map 281')
    _save_raw(281, L)
    return L


def build_282_layers():
    # Exact HEAD events (2/2): #2 Mart @(2,3) [dir=right], #3 Exit @(4,8) [arrival (4,7)]
    # Stretched from mart.json (11x9) via stretch: [['x', 10, 6], ['y', 8, 2]] -> 17x11 (ZERO events shifted!)
    W, H = 17, 11
    L = np.zeros((3, H, W), dtype=np.int32)

    floor = np.zeros((H, W), dtype=bool)
    floor[2:8, 1:7] = True         # West Apothecary Counter & Vestibule (x=1..6, y=2..7)
    floor[7, 1] = False            # SW void chamfer
    floor[8, 3:6] = True           # Recessed entry door notch (x=3..5, y=8; Exit @ 4,8!)
    floor[2:10, 7:12] = True       # Central Provision & Potion Aisle (x=7..11, y=2..9)
    floor[9, 7] = False            # Beveled south aisle SW shoulder
    floor[9, 11] = False           # Beveled south aisle SE shoulder
    floor[3:9, 12:16] = True       # East Sunlit Botanical Herbarium Conservatory (x=12..15, y=3..8)
    floor[8, 15] = False           # SE herbarium chamfer

    _seam_sheridan(L, floor, wall_rows=2)

    # Multi-Zone Royal Botanical Apothecary Flooring:
    _put_9slice(L, SAGE_MARBLE, 1, 2, 11, 9, z=0, mask=floor)
    _put_9slice(L, IVORY_MARBLE, 3, 5, 5, 8, z=0, mask=floor)
    for y in range(3, 9):
        for x in range(12, 16):
            if floor[y, x]:
                L[0, y, x] = FLOOR_EMERALD
    # Crimson welcome runner from Exit (4,8) north into the Apothecary
    _put_9slice(L, SHER_RUG, 3, 5, 5, 7, z=1)
    L[1, 8, 4] = 444
    # Center showcase crimson medallion carpet (8..10, 7..9)
    _put_9slice(L, RED_CARPET, 8, 7, 10, 9, z=1)

    # Sunlit Arched Verdance Windows & Apothecary Wall Shelving:
    for wx in (2, 6, 9, 13):
        wy = 1 if wx >= 12 else 0
        L[0, wy, wx] = 5544; L[0, wy + 1, wx] = 5552
    _put_tf(L, 'painting3', 4, 0)

    # Warm Royal Botanical Mart Counter (5944..5967, REAL 0x80 flags!) backing #2 Mart @(2,3) facing RIGHT!
    # Vertical counter at (3, 2..4) + front return at (2, 4) — leaves (1,4) passable so BOTH (4,3) across 0x80 AND (1,3) direct BFS pass!
    L[1, 2, 3] = 5948  # upper counter arm (0x80)
    L[1, 3, 3] = 5955  # bouquet vertical counter right in front of Mart @(2,3) (0x80!)
    L[1, 4, 3] = 5963  # SE curved counter corner (0x80)
    L[1, 4, 2] = 5961  # front counter under clerk (0x80)
    L[1, 6, 1] = 7178  # blooming rose planter tucked in SW corner (leaves (1,4) & (1,5) open!)
    _put_lamp(L, 2, 7, ruby=True)

    # Central Potion & Apothecary Provision Isles (x=7..11, y=2..9):
    _put_tf(L, 'shelf_goods', 7, 1)        # (7..8, 1..3) Tall stocked Pokeball & Potion shelf against north wall
    _put_tf(L, 'shelf_goods', 10, 1)       # (10..11, 1..3) Second stocked provision shelf
    _put_tf(L, 'shelf_green', 7, 5)        # (7..8, 5..6) Emerald apothecary herb display rack
    _put_tf(L, 'display', 10, 5)           # (10..11, 5..6) Glass botanical tincture showcase
    _put_tf(L, 'table_tea', 9, 8)          # (9..10, 8..9) South bouquet & tea sampling table on crimson carpet

    # East Sunlit Botanical Herbarium Conservatory (x=12..15, y=3..8):
    _put_tf(L, 'china', 13, 2)             # (13..15, 2..4) Ornate antique apothecary glass cabinet!
    _put_grid(L, [[5422], [5430], [5438]], 15, 4, z_rows=(2, 1, 1))  # East flowering shelf
    _put_grid(L, [[5446, 5447], [5454, 5455]], 13, 7, z_rows=(1, 1)) # Blooming flower-box bench
    _put_plant(L, 12, 4, 7874, 7882)       # Grand conservatory palm
    _put_plant(L, 12, 8, 5431, 5439)       # Conservatory fern framing SE arch

    PG.guard(L, TID, [(4, 8), (4, 7), (4, 3), (2, 3), (1, 3), (1, 4)], 'map 282')
    _save_raw(282, L)
    return L


def build_verdance_281_282():
    L281 = build_281_layers()
    L282 = build_282_layers()
    spec_path = os.path.join(SPEC_DIR, '281_verdance_interiors.yaml')
    docs = [d for d in yaml.safe_load_all(open(spec_path)) if d]
    by_id = {d['id']: d for d in docs}

    d281 = by_id[281]
    s281 = {
        'id': 281,
        'name': d281['name'],
        'parent': d281['parent'],
        'template': 'pokecenter',
        'exit_link': d281['exit_link'],
        'drop_template_events': d281['drop_template_events'],
        'tileset': TID,
        'bgm': d281['bgm'],
        'tone': [6, 8, -6, 0],
        'metadata': d281['metadata'],
        'stretch': [['y', 9, 1]],
        'tile_edits': _compress_tile_edits(L281),
        'events': d281['events'],
    }
    d282 = by_id[282]
    s282 = {
        'id': 282,
        'name': d282['name'],
        'parent': d282['parent'],
        'template': 'mart',
        'exit_link': d282['exit_link'],
        'drop_template_events': d282['drop_template_events'],
        'tileset': TID,
        'bgm': d282['bgm'],
        'tone': [6, 8, -6, 0],
        'metadata': d282['metadata'],
        'stretch': [['x', 10, 6], ['y', 8, 2]],
        'tile_edits': _compress_tile_edits(L282),
        'events': d282['events'],
    }
    hdr = "# GENERATED by mapgen/layouts/wave16_final12_craft.py (Wave 16 Final Map Craft): Verdance Botanical Interiors (281-282).\n"
    out = hdr + '\n---\n'.join(
        yaml.safe_dump(s, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True)
        for s in (s281, s282)
    )
    open(spec_path, 'w').write(out)
    print(f"Built 281 {L281.shape} & 282 {L282.shape} -> {spec_path}")


# ==============================================================================
# MAPS 6-11: 571-576 Frostwick Alpine Timber Interiors (TS 34)
# Unified seamlessly with Wave 11's 570 Frostwick!
# ==============================================================================
def build_571_layers():
    # 20x17 Frostwick Pokemon Center — Alpine Mountain Refuge Lodge
    # Exact HEAD events (5/5): #2 Nurse @(9,5), #3 PC @(13,5), #4 Healing balls @(7,5),
    #                          #5 Exit @(9,13) [arrival (9,12)], #6 Local @(5,10)
    W, H = 20, 17
    L = np.zeros((3, H, W), dtype=np.int32)

    floor = np.zeros((H, W), dtype=bool)
    floor[5:13, 2:7] = True        # West Hearthside Lounge (x=2..6, y=5..12)
    floor[12, 2] = False           # SW log-cabin chamfer
    floor[4:13, 7:13] = True       # Central Vaulted Healing Hall (x=7..12, y=4..12)
    floor[13, 8:11] = True         # Recessed Entry Vestibule (x=8..10, y=13; Exit @ 9,13!)
    floor[5:13, 13:18] = True      # East Trail & Rest Alcove (x=13..17, y=5..12)
    floor[12, 17] = False          # SE log-cabin chamfer

    _seam_sheridan(L, floor, wall_rows=2)

    # Multi-Zone Alpine Timber & Slate Hearth Flooring:
    # Slate hearthstone apron beneath West Woodstove (x=2..4, y=5..7)
    _put_9slice(L, ALPINE_SLATE, 2, 5, 4, 7, z=0)
    # Cool alpine stone entry vestibule (x=8..10, y=11..13)
    _put_9slice(L, ALPINE_SLATE, 8, 11, 10, 13, z=0)
    _put_doormat(L, 9, 13, 'sheridan')
    # Warm Nordic Fringed Alpine Rug in center lounge (x=7..11, y=8..11)
    _put_nordic_rug(L, 7, 8, 11, 11, z=1)
    # Cozy crimson reading rug under West Hearthside Lounge (x=3..5, y=8..10)
    _put_9slice(L, SHER_RUG, 3, 8, 5, 10, z=1)

    # Frosted Arched Alpine Windows on North Walls:
    _put_grid(L, [[2086, 2087], [2094, 2095]], 4, 3, z_rows=(1, 1))      # West arched frosted alpine window
    _put_grid(L, [[2086, 2087], [2094, 2095]], 10, 2, z_rows=(1, 1))     # Vaulted arched snow window above Nurse
    _put_grid(L, [[2086, 2087], [2094, 2095]], 15, 3, z_rows=(1, 1))     # East arched frosted alpine window

    # Central Rustic Sheridan Healing Counter (5656..5671, REAL 0x80 flags!) wrapping Nurse @(9,5):
    # Healing Machine (2706..2723) at (6..7, 4..6) -> ball tray 2715 squarely on #4 Healing balls @(7,5)!
    _put_tf(L, 'heal', 6, 4)
    # Rustic Sheridan Counter front at y=6 (x=8..11, ALL p=143 = 0x80+15!) + flush right return (11,4..5)!
    L[1, 6, 8] = 5665
    L[1, 6, 9] = 5666  # 0x80 directly in front of #2 Nurse @(9,5) -> heal from (9,7)!
    L[1, 6, 10] = 5667
    L[1, 6, 11] = 5668
    L[1, 5, 11] = 5662  # Right return counter arm
    L[1, 4, 11] = 5662  # Flush to north wall!
    # #3 PC @(13,5): crisp blue PC terminal (2704..2713) at (13..14, 4..5) -> solid at (13,5), talk from (13,6)!
    _put_tf(L, 'tv', 13, 4)

    # West Hearthside Lounge (around #6 Local @(5,10)):
    _put_stove(L, 3, 5, kettle=True)       # Crackling cast-iron woodstove with steaming copper kettle!
    L[1, 6, 2] = 4101                      # Oak kindling bucket beside woodstove!
    _put_tf(L, 'bench_v', 2, 8)            # (2, 8..10) Timber hearth bench facing the fire
    _put_tf(L, 'table_tea', 4, 8)          # (4..5, 8..9) Warm tea table right above Local @(5,10)!
    _put_lamp(L, 3, 12, ruby=True)         # Warm ruby lodge lamp

    # Central Nordic Rug Coffee Table (8..9, 9..10)
    _put_tf(L, 'table_dark', 8, 9)         # (8..9, 9..10) Center lodge cocoa table (leaves y=7, y=8, y=11 wide open!)

    # East Trail & Rest Alcove (x=13..17, y=5..12):
    _put_tf(L, 'bookcase', 16, 4)          # (16..17, 4..5) Alpine guidebooks & field shelf
    _put_tf(L, 'bench_v', 17, 7)           # (17, 7..9) East waiting bench
    _put_tf(L, 'crate_i', 14, 11)          # (14..15, 11..12) Mountain rescue pack crate
    _put_plant(L, 16, 11, 5431, 5439)      # Intact lodge fern
    _put_lamp(L, 12, 12, ruby=True)        # Companion vestibule lamp

    PG.guard(L, TID, [(9, 13), (9, 12), (9, 7), (9, 5), (7, 5), (13, 6), (5, 10)], 'map 571')
    _save_raw(571, L)
    return L


def build_572_layers():
    # 21x16 The Exchange — Two-Kingdom Border Trading Post
    # Exact HEAD events (3/3): #2 Mart @(4,5), #3 Exit @(10,12) [arrival (10,11)], #4 Barter-woman @(12,7)
    W, H = 21, 16
    L = np.zeros((3, H, W), dtype=np.int32)

    floor = np.zeros((H, W), dtype=bool)
    floor[5:12, 2:8] = True        # West Timber Trade Counter Wing (x=2..7, y=5..11)
    floor[11, 2] = False           # SW chamfer
    floor[4:12, 8:14] = True       # Central Vaulted Barter Floor (x=8..13, y=4..11)
    floor[12, 9:12] = True         # Recessed Entry Vestibule (x=9..11, y=12; Exit @ 10,12!)
    floor[5:12, 14:19] = True      # East Provisions & Oil Barrels Bay (x=14..18, y=5..11)
    floor[11, 18] = False          # SE chamfer

    _seam_sheridan(L, floor, wall_rows=2)

    # Multi-zone trading post flooring:
    _put_9slice(L, ALPINE_SLATE, 9, 10, 11, 12, z=0)
    _put_doormat(L, 10, 12, 'sheridan')
    _put_9slice(L, ALPINE_SLATE, 15, 5, 18, 8, z=0)  # Cold-storage stone bay under East warehouse!
    # Woven Nordic Barter Carpet under central market floor (x=8..13, y=7..10)
    _put_nordic_rug(L, 8, 7, 13, 10, z=1)

    # Frosted Arched Windows & Trading Notices on North Wall:
    _put_grid(L, [[2086, 2087], [2094, 2095]], 4, 3, z_rows=(1, 1))
    _put_grid(L, [[2086, 2087], [2094, 2095]], 10, 2, z_rows=(1, 1))
    _put_tf(L, 'map_wall', 15, 3)

    # West Timber Trade Counter (5656..5671, REAL 0x80 flags!) for #2 Mart @(4,5):
    # Counter front along y=6 (x=3..6, ALL p=143 = 0x80+15!) -> talk to Mart @(4,5) from (4,7)!
    # Leave (2,6) open so strict 4-neighbor BFS can ALSO reach (3,5) beside Mart!
    L[1, 6, 3] = 5664
    L[1, 6, 4] = 5666  # 0x80 right in front of #2 Mart @(4,5)!
    L[1, 6, 5] = 5667
    L[1, 6, 6] = 5668
    L[1, 5, 6] = 5662  # Right return counter arm flush to north wall!
    _put_stove(L, 2, 9, kettle=False)      # Warm cast-iron stove heating the west counter bay!
    _put_plant(L, 3, 11, 5431, 5439)       # SW lodge fern
    _put_lamp(L, 7, 11, ruby=True)

    # Central Barter Bazaar (around #4 Barter-woman @(12,7)):
    # Keep (12,7), (12,8), (11,7), (13,7) wide open!
    _put_tf(L, 'shelf_goods', 8, 3)        # (8..9, 3..5) Elowen honey & silk trade shelf
    _put_tf(L, 'shelf_goods', 12, 3)       # (12..13, 3..5) Isenmar provisions shelf (bottom at y=5, leaves y=6..7 open!)
    _put_tf(L, 'display', 8, 9)            # (8..9, 9..10) Glass barter-rates display case!
    _put_tf(L, 'shelf_green', 12, 9)       # (12..13, 9..10) Silk & herb display stand right below Barter-woman!

    # East Provisions & Whale-Oil Warehouse (x=14..18, y=5..11):
    _put_tf(L, 'crates3', 15, 4)           # (15..17, 4..6) Stacked trade crates
    _put_tf(L, 'barrel_b', 18, 6)          # (18, 6..7) Isenmar blue whale-oil drum
    _put_tf(L, 'barrel_y', 17, 8)          # (17, 8..9) Elowen golden honey cask
    _put_tf(L, 'barrel_b', 18, 9)          # (18, 9..10) Second whale-oil cask
    _put_tf(L, 'crate_i', 15, 10)          # (15..16, 10..11) Sealed fur & silk trunk
    _put_lamp(L, 14, 11, ruby=True)

    PG.guard(L, TID, [(10, 12), (10, 11), (4, 7), (4, 5), (3, 5), (12, 7), (12, 8)], 'map 572')
    _save_raw(572, L)
    return L


def build_573_layers():
    # 27x18 The Two Hearths — Iconic Twin-Kingdom Border Inn!
    # Exact HEAD events (7/7 — including 3 trial_overlay NPCs!):
    #   #1 Exit @(13,14) [arrival (13,13)], #2 Brannagh (inn) @(6,7), #3 Halvard (inn) @(20,7),
    #   #4 Guest @(12,11), #5 Ingrith @(4,6), #6 Sister Maelon @(12,6), #7 Brenna and Sigvald @(8,8)
    W, H = 27, 18
    L = np.zeros((3, H, W), dtype=np.int32)

    floor = np.zeros((H, W), dtype=bool)
    floor[5:13, 2:10] = True       # West Elowen Applewood Hearth Wing (x=2..9, y=5..12)
    floor[12, 2] = False           # SW chamfer
    floor[4:14, 10:17] = True      # Central Vaulted Neutral Feast Hall (x=10..16, y=4..13)
    floor[14, 12:15] = True        # Recessed Inn Porch Vestibule (x=12..14, y=14; Exit @ 13,14!)
    floor[5:13, 17:25] = True      # East Isenmar Whale-Oil Hearth Wing (x=17..24, y=5..12)
    floor[12, 24] = False          # SE chamfer

    _seam_sheridan(L, floor, wall_rows=2)

    # Dramatic Twin-Kingdom Material Contrast:
    # West Elowen Wing: warm timber planks + cozy Crimson Botanical Rug (x=4..8, y=9..11)
    _put_9slice(L, SHER_RUG, 4, 9, 8, 11, z=1)
    # Central Neutral Feast Hall: slate threshold + Grand Nordic Fringed Banquet Carpet (x=10..16, y=7..11)!
    _put_9slice(L, ALPINE_SLATE, 12, 12, 14, 14, z=0)
    _put_doormat(L, 13, 14, 'sheridan')
    _put_nordic_rug(L, 10, 7, 16, 11, z=1)
    # East Isenmar Wing: deep alpine slate hearth floor (x=18..24, y=5..12) + Royal Blue Woven Rug (x=18..22, y=8..11)!
    _put_9slice(L, ALPINE_SLATE, 18, 5, 24, 12, z=0, mask=floor)
    _put_9slice(L, BLUE_CARPET, 18, 8, 22, 11, z=1)

    # Frosted Arched Alpine Windows along North Walls (all intact 2x2 arched panes!):
    _put_grid(L, [[2086, 2087], [2094, 2095]], 7, 3, z_rows=(1, 1))      # West Elowen arched window
    _put_grid(L, [[2086, 2087], [2094, 2095]], 11, 2, z_rows=(1, 1))     # Central north arched window W
    _put_grid(L, [[2086, 2087], [2094, 2095]], 14, 2, z_rows=(1, 1))     # Central north arched window E
    _put_grid(L, [[2086, 2087], [2094, 2095]], 18, 3, z_rows=(1, 1))     # East Isenmar arched window

    # WEST WING — Brannagh's Elowen Applewood Hearth (keep Ingrith @(4,6), Brannagh @(6,7), Brenna/Sigvald @(8,8) CLEAR!):
    _put_tf(L, 'kitchen', 3, 4)            # (3..6, 4..5) Brannagh's applewood hearth & cooking range!
    _put_stove(L, 2, 5, kettle=True)       # Crackling applewood stove with steaming copper kettle!
    L[1, 7, 2] = 7178                      # Elowen blooming rose planter
    _put_grid(L, [[5422], [5430], [5438]], 2, 9, z_rows=(2, 1, 1))  # Dried herb & flower rack
    _put_tf(L, 'table_tea', 5, 10)         # (5..6, 10..11) West hearthside tea table on crimson rug
    _put_lamp(L, 3, 12, ruby=True)

    # CENTRAL NEUTRAL FEAST HALL (keep Sister Maelon @(12,6) & Guest @(12,11) CLEAR!):
    _put_tf(L, 'bookcase', 13, 3)          # (13..14, 3..4) Shared Accord chronicle bookcase dividing north wall
    _put_tf(L, 'table_w', 10, 8)           # (10..11, 8..10) West half of the long neutral feast table!
    _put_tf(L, 'table_w', 14, 8)           # (14..15, 8..10) East half of the long neutral feast table!
    # Guest @(12,11) sits right in the middle between them — leave (12..13, 7..12) open central walkway!
    _put_lamp(L, 11, 13, ruby=True)        # Warm lamps framing Entry Porch
    _put_lamp(L, 15, 13, ruby=True)

    # EAST WING — Halvard's Isenmar Whale-Oil Hearth (keep Halvard @(20,7) CLEAR!):
    _put_tf(L, 'kitchen', 20, 4)           # (20..23, 4..5) Halvard's whale-oil galley & hearth!
    _put_stove(L, 24, 5, kettle=False)     # Hot iron whale-oil stove!
    _put_tf(L, 'table_dark', 19, 9)        # (19..20, 9..10) Heavy dark-timber Isenmar drinking table on blue rug
    L[1, 10, 18] = 4077; L[1, 10, 21] = 4077  # Wooden stools flanking Halvard's table
    _put_tf(L, 'barrel_b', 24, 8)          # (24, 8..9) Blue whale-oil barrel
    _put_tf(L, 'barrel_y', 23, 10)         # (23, 10..11) Smoked provisions barrel
    _put_tf(L, 'crate', 21, 11)            # (21..22, 11..12) Sea-salt supply crate
    _put_tf(L, 'rodbucket', 24, 10)        # (24, 10..11) Fishing rods in corner
    _put_plant(L, 17, 12, 5431, 5439)      # Intact alpine fern

    PG.guard(
        L, TID,
        [(13, 14), (13, 13), (6, 7), (20, 7), (12, 11), (4, 6), (12, 6), (8, 8)],
        'map 573',
    )
    _save_raw(573, L)
    return L


def build_574_layers():
    # 20x17 Rime-silk Loft — Giant Tree-Hollow Alpine Weaving Atelier
    # Exact HEAD events (3/3): #1 Exit @(8,13) [arrival (8,12)], #2 Weaver @(6,7), #3 Item SILKSCARF @(11,10)
    W, H = 20, 17
    L = np.zeros((3, H, W), dtype=np.int32)

    floor = np.zeros((H, W), dtype=bool)
    floor[5:13, 4:14] = True       # Core tree-hollow loft (x=4..13, y=5..12)
    floor[6:12, 3] = True          # West curved tree-bark alcove (x=3, y=6..11)
    floor[6:12, 14] = True         # East curved silk-spinning bay (x=14, y=6..11)
    floor[12, 4] = False           # SW organic chamfer
    floor[12, 13] = False          # SE organic chamfer
    floor[13, 7:10] = True         # Recessed loft entry hatch (x=7..9, y=13; Exit @ 8,13!)

    _seam_sheridan(L, floor, wall_rows=2)

    # Multi-Zone Rime-Silk Atelier Flooring:
    # Shimmering frosted blue-marble weaving pad under the East Rime-silk loom & SILKSCARF (x=10..14, y=6..11)!
    _put_9slice(L, BLUE_STONE, 10, 6, 14, 11, z=0)
    # Warm woven Nordic rug in center living/weaving studio (x=5..9, y=8..11)
    _put_nordic_rug(L, 5, 8, 9, 11, z=1)
    _put_doormat(L, 8, 13, 'sheridan')

    # Frosted Tree-Hollow Windows & Silk Patterns on North Wall (y=3..4):
    _put_grid(L, [[2086, 2087], [2094, 2095]], 8, 3, z_rows=(1, 1))
    L[1, 3, 6] = 5560; L[1, 4, 6] = 5568   # Circular tree-hollow porthole window

    # Weaving Atelier Storytelling (keep Weaver @(6,7) & Item SILKSCARF @(11,10) cleanly reachable!):
    _put_tf(L, 'bookcase', 4, 4)           # (4..5, 4..5) Spools & weaving pattern shelves
    # THE KETTLE THAT TRIED HARDEST TO THAW RIME-SILK! Steaming woodstove (2470/2478) at (7, 5)!
    _put_stove(L, 7, 5, kettle=True)
    # Rime-silk Loom & Spinning Workbench (4082..4092, 3x2) at (10..12, 4..5) right behind frosted weaving bay!
    _put_tf(L, 'workbench', 10, 4)
    _put_tf(L, 'shelf_wood', 3, 7)         # (3..4, 7..8) Raw drifted Briarwick silk bolts!
    _put_tf(L, 'table_tea', 6, 9)          # (6..7, 9..10) Tea & thread winding table on Nordic rug
    _put_tf(L, 'crate_i', 13, 7)           # (13..14, 7..8) Packed Rime-silk bolts right above SILKSCARF @(11,10)!
    _put_plant(L, 14, 11, 5431, 5439)      # Intact parlor fern in SE bay
    _put_plant(L, 3, 11, 5415, 5423)       # Intact parlor tree in SW bay
    _put_lamp(L, 5, 12, ruby=True)         # Warm brass lamp framing loft entry
    _put_lamp(L, 10, 12, ruby=True)        # Companion lamp cleanly clear of SILKSCARF @(11,10)!

    PG.guard(L, TID, [(8, 13), (8, 12), (6, 7), (6, 8), (11, 10), (10, 10)], 'map 574')
    _save_raw(574, L)
    return L


def build_575_layers():
    # 21x16 Border House — Three Clerks, Three Seals (Elowen, Meridian, Isenmar)
    # Exact HEAD events (4/4): #1 Exit @(10,12) [arrival (10,11)],
    #                          #2 Elowen clerk @(6,6), #3 Isenmar clerk @(14,6), #4 Meridian clerk @(10,6)
    W, H = 21, 16
    L = np.zeros((3, H, W), dtype=np.int32)

    floor = np.zeros((H, W), dtype=bool)
    floor[5:12, 3:8] = True        # West Elowen Briar Seal Bay (x=3..7, y=5..11)
    floor[11, 3] = False           # SW chamfer
    floor[4:12, 8:13] = True       # Central Vaulted Meridian Sunburst Bay (x=8..12, y=4..11)
    floor[12, 9:12] = True         # Recessed Border Entry Porch (x=9..11, y=12; Exit @ 10,12!)
    floor[5:12, 13:18] = True      # East Isenmar Whale Seal Bay (x=13..17, y=5..11)
    floor[11, 17] = False          # SE chamfer

    _seam_sheridan(L, floor, wall_rows=2)

    # Three-Kingdom Floor Storytelling:
    # Center Meridian bay: sleek blue-marble authority inlay (x=8..12, y=4..9) + formal crimson queue runner!
    _put_9slice(L, BLUE_STONE, 8, 4, 12, 9, z=0)
    # East Isenmar bay: cool alpine slate hearth floor (x=13..17, y=5..11)
    _put_9slice(L, ALPINE_SLATE, 13, 5, 17, 11, z=0, mask=floor)
    # West Elowen bay: warm timber + cozy crimson rug under waiting area (x=4..7, y=9..10)
    _put_9slice(L, RED_CARPET, 9, 9, 11, 11, z=1)
    _put_doormat(L, 10, 12, 'sheridan')

    # Three-Bay North Wall Dressings:
    _put_grid(L, [[2086, 2087], [2094, 2095]], 5, 3, z_rows=(1, 1))      # Elowen arched frosted window
    _put_grid(L, [[5795, 5796, 5797], [5803, 5804, 5805]], 9, 2, z_rows=(1, 1))  # Meridian official directive board!
    _put_grid(L, [[2086, 2087], [2094, 2095]], 14, 3, z_rows=(1, 1))     # Isenmar arched frosted window

    # Three Clerk Desks cleanly positioned 1 row south of each clerk (so clerks @(6,6), (10,6), (14,6) sit behind them,
    # while leaving wide vertical aisles at x=4, x=8, x=12, x=16 so EVERY clerk is directly talkable by 4-neighbor BFS!):
    _put_tf(L, 'desk', 5, 7)                                         # (5..6, 7..8) Elowen Briar clerk desk
    _put_grid(L, [[2515, 2516], [2523, 2524]], 9, 7, z_rows=(2, 1))  # (9..10, 7..8) Solid mahogany Meridian clerk desk!
    _put_tf(L, 'desk', 13, 7)                                        # (13..14, 7..8) Isenmar Whale clerk desk

    # Distinct Kingdom Corner Vignettes:
    _put_tf(L, 'bookshelf_s', 3, 4)        # (3, 4..5) Elowen archive shelf
    _put_plant(L, 3, 9, 7874, 7882)        # Elowen botanical palm
    L[1, 10, 4] = 7178                     # Blooming Elowen briar rose planter
    _put_lamp(L, 7, 11, ruby=True)

    _put_tf(L, 'bookshelf_s', 17, 4)       # (17, 4..5) Isenmar ledger shelf
    _put_stove(L, 17, 8, kettle=False)     # Warm iron woodstove heating the Isenmar desk!
    _put_tf(L, 'barrel_b', 16, 10)         # (16, 10..11) Isenmar seal-wax & lamp-oil cask
    _put_lamp(L, 13, 11, ruby=True)

    PG.guard(
        L, TID,
        [(10, 12), (10, 11), (6, 6), (7, 6), (10, 6), (11, 6), (14, 6), (15, 6)],
        'map 575',
    )
    _save_raw(575, L)
    return L


def build_576_layers():
    # 20x15 Halvard's Smokehouse — Cozy L-Shaped Alpine Curing Lodge
    # Exact HEAD events (2/2): #1 Exit @(7,11) [arrival (7,10)], #2 Halvard's daughter @(5,7)
    W, H = 20, 15
    L = np.zeros((3, H, W), dtype=np.int32)

    floor = np.zeros((H, W), dtype=bool)
    floor[5:11, 3:12] = True       # Main Smokehouse Curing Room (x=3..11, y=5..10)
    floor[10, 3] = False           # SW chamfer
    floor[10, 11] = False          # SE chamfer
    floor[11, 6:9] = True          # Recessed Entry Vestibule (x=6..8, y=11; Exit @ 7,11!)
    floor[6:10, 12:15] = True      # East Recessed Brine & Eel-Curing Alcove (x=12..14, y=6..9)

    _seam_sheridan(L, floor, wall_rows=2, stone_walls=True)

    # Multi-Zone Smokehouse Flooring:
    # Dark alpine slate hearth under north curing stoves & East Brine Alcove!
    _put_9slice(L, ALPINE_SLATE, 6, 5, 11, 6, z=0)
    _put_9slice(L, ALPINE_SLATE, 12, 6, 14, 9, z=0)
    # Warm Nordic tasting rug around Halvard's daughter @(5,7) & tasting table (x=4..8, y=7..10)
    _put_nordic_rug(L, 4, 7, 8, 9, z=1)
    _put_doormat(L, 7, 11, 'sheridan')

    # Frosted Smokehouse Arched Window & Wall Gear (cleanly clear of crates3 at x=3..5!):
    _put_grid(L, [[2086, 2087], [2094, 2095]], 6, 3, z_rows=(1, 1))
    _put_tf(L, 'map_wall', 9, 3)

    # Twin Crackling Curing Stoves & Brine Craft (keep Halvard's daughter @(5,7) & Exit @(7,11) CLEAR!):
    _put_stove(L, 8, 5, kettle=True)       # Primary smoked-eel curing stove with copper kettle!
    _put_stove(L, 10, 5, kettle=False)     # Companion hearth smoker firebox!
    _put_tf(L, 'crates3', 3, 4)            # (3..5, 4..6) Stacked oak curing crates (bottom at y=6, leaves (5,7) open!)
    _put_tf(L, 'food_table', 6, 7)         # (6..7, 7..9) Smoked-eel tasting table right beside Halvard's daughter @(5,7)!
    L[1, 8, 3] = 4101                      # Salt-brine bucket
    _put_lamp(L, 4, 10, ruby=True)         # Warm ruby smokehouse lantern
    _put_lamp(L, 10, 10, ruby=True)

    # East Brine & Fishing Gear Alcove (x=12..14, y=6..9):
    _put_tf(L, 'barrel_b', 14, 5)          # (14, 5..6) Blue eel-brine cask
    _put_tf(L, 'barrel_y', 13, 6)          # (13, 6..7) Smoked salt-oil cask
    _put_tf(L, 'rodbucket', 14, 8)         # (14, 8..9) Fishing rods beside brine barrels
    _put_tf(L, 'crate', 12, 8)             # (12..13, 8..9) Packed smoked-eel delivery crate

    PG.guard(L, TID, [(7, 11), (7, 10), (5, 7), (5, 8)], 'map 576')
    _save_raw(576, L)
    return L


def build_frostwick_571_576():
    L571 = build_571_layers()
    L572 = build_572_layers()
    L573 = build_573_layers()
    L574 = build_574_layers()
    L575 = build_575_layers()
    L576 = build_576_layers()

    spec_path = os.path.join(SPEC_DIR, '571_frostwick_interiors.yaml')
    docs = [d for d in yaml.safe_load_all(open(spec_path)) if d]
    by_id = {d['id']: d for d in docs}

    new_docs = []
    # 571 & 572 preserve `take_events:` via `palette: interior` + exact `tiles:` list!
    for mid, L in ((571, L571), (572, L572)):
        old = by_id[mid]
        _, H, W = L.shape
        new_docs.append({
            'id': mid,
            'name': old['name'],
            'parent': old['parent'],
            'bgm': old.get('bgm', ''),
            'biome': 'interior',
            'tone': [10, 4, -8, 0],
            'metadata': old['metadata'],
            'palette': 'interior',
            'map': '\n'.join('.' * W for _ in range(H)) + '\n',
            'tiles': _layers_to_tiles_list(L),
            'events': old['events'],
            'take_events': old['take_events'],
        })
    # 573-576 use clean `raw: data/raw/57X.npy` + `tileset: 34` (trial_overlay still injects 573's 3 NPCs natively!)
    for mid, L in ((573, L573), (574, L574), (575, L575), (576, L576)):
        old = by_id[mid]
        new_docs.append({
            'id': mid,
            'name': old['name'],
            'parent': old['parent'],
            'bgm': old.get('bgm', ''),
            'biome': 'interior',
            'tone': [10, 4, -8, 0],
            'metadata': old['metadata'],
            'tileset': TID,
            'raw': f'data/raw/{mid:03d}.npy',
            'events': old['events'],
        })

    hdr = "# Frostwick alpine interiors 571-576. GENERATED by layouts/wave16_final12_craft.py (Wave 16 Final Map Craft).\n"
    out = hdr + '\n---\n'.join(
        yaml.safe_dump(s, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True)
        for s in new_docs
    )
    open(spec_path, 'w').write(out)
    print("Built Frostwick 571-576 ->", spec_path)


# ==============================================================================
# MAP 12: 990 Prismfall Test Arena (21x13, TS 34) — Grand Championship Pavilion!
# ==============================================================================
def build_990():
    # Exact HEAD events (36/36):
    #   West Balcony NPCs: x=1..5, y=2, 4, 6; x=1..3, y=8; Healer @(4,8)
    #   East Balcony NPCs: x=15..19, y=2, 4, 6
    #   Center Pavilion:   Arena sign @(10,3), Exit @(10,12)
    W, H = 21, 13
    L = np.zeros((3, H, W), dtype=np.int32)

    floor = np.zeros((H, W), dtype=bool)
    floor[2:12, 1:20] = True       # Main Grand Exhibition Pavilion (x=1..19, y=2..11)
    floor[11, 1:3] = False         # SW sculpted pavilion chamfer
    floor[11, 18:20] = False       # SE sculpted pavilion chamfer
    floor[12, 9:12] = True         # Recessed Grand Entrance Portal (x=9..11, y=12; Exit @ 10,12!)

    _seam_cyber(L, floor, wall_rows=2, base_floor='diamond')

    # Tiered Stadium Pavilion Flooring:
    # West & East Challenger Pavilions (x=1..5 & x=15..19, y=2..9): sleek blue-marble dais terraces!
    _put_9slice(L, BLUE_STONE, 1, 2, 5, 9, z=0)
    _put_9slice(L, BLUE_STONE, 15, 2, 19, 9, z=0)
    # Dark obsidian aisle carpets along inner colonnades x=6 & x=14
    for y in range(2, 11):
        L[0, y, 6] = 7091 if y % 2 == 0 else 7092
        L[0, y, 14] = 7091 if y % 2 == 0 else 7092
    # Center Championship Court Apron: luminous cream-gold marble (x=7..13, y=2..11)!
    _put_9slice(L, CREAM_STONE, 7, 2, 13, 11, z=0)
    _put_9slice(L, CREAM_STONE, 9, 12, 11, 12, z=0)

    # CENTERPIECE: 7x5 GRAND CHAMPIONSHIP BLUE POKEBALL BATTLE COURT (5616..5654) at (7..13, 5..9)!
    _put_grid(L, ARENA_BLUE_COURT, 7, 5, z_rows=(0, 0, 0, 0, 0))

    # Royal Crimson Championship Runner from Exit (10,12) up to Court & from Court north to Arena sign (10,3)!
    _put_9slice(L, RED_CARPET, 9, 10, 11, 12, z=1)
    L[1, 12, 10] = 444  # Grand welcome mat on Exit (10,12)
    # Glowing electric-cyan championship beacon markers flanking court corners & aisles
    for gx, gy in ((6, 4), (14, 4), (6, 10), (14, 10), (8, 3), (12, 3), (8, 11), (12, 11)):
        L[0, gy, gx] = FLOOR_CYAN

    # Grand North Pavilion Wall (y=0..1): Symmetrical 3-Panel Stadium Jumbotron Triptych & Telemetry Monitors!
    _put_grid(L, [[7312, 7313, 7314], [7320, 7321, 7322]], 2, 0, z_rows=(1, 1))   # West Field Scoreboard
    _put_grid(L, [[7136, 7137], [7144, 7145]], 6, 0, z_rows=(1, 1))               # West Match Telemetry Monitor
    _put_grid(L, [[7312, 7313, 7314], [7320, 7321, 7322]], 9, 0, z_rows=(1, 1))   # Center Championship Scoreboard
    _put_grid(L, [[7136, 7137], [7144, 7145]], 13, 0, z_rows=(1, 1))              # East Match Telemetry Monitor
    _put_grid(L, [[7312, 7313, 7314], [7320, 7321, 7322]], 16, 0, z_rows=(1, 1))  # East Field Scoreboard

    # Illuminated Blue-Silver Arena Directory Stele (5792/5800) right on #36 Arena sign @(10,3)!
    # Cleanly solid & interactable from (10,4), (9,3), and (11,3)!
    L[1, 2, 10] = 5792
    L[1, 3, 10] = 5800

    # Perimeter Pavilion Framing (ZERO overlap with ANY of the 33 Field NPCs or Healer @(4,8)!):
    # Symmetrical Grand Palms, Parlor Ficus & Brass Arena Lamps framing the Entrance & Championship Court!
    _put_plant(L, 3, 11, 7874, 7882)
    _put_plant(L, 17, 11, 7874, 7882)
    _put_plant(L, 5, 11, 7126, 7134)
    _put_plant(L, 15, 11, 7126, 7134)
    _put_lamp(L, 7, 11, ruby=False)
    _put_lamp(L, 13, 11, ruby=False)
    _put_lamp(L, 7, 3, ruby=False)
    _put_lamp(L, 13, 3, ruby=False)
    # East open tech alcove below y=6 NPCs (x=17..19, y=8..9): holographic field simulator pod (7154..7171) + palm!
    _put_grid(L, [[7154, 7155], [7162, 7163], [7170, 7171]], 17, 8, z_rows=(2, 1, 1))
    _put_plant(L, 19, 9, 7126, 7134)

    event_cells = (
        [(x, y) for y in (2, 4, 6) for x in (1, 2, 3, 4, 5, 15, 16, 17, 18, 19)]
        + [(1, 8), (2, 8), (3, 8), (4, 8), (10, 12), (10, 11), (10, 4)]
    )
    PG.guard(L, TID, event_cells, 'map 990')
    _save_raw(990, L)

    spec_path = os.path.join(SPEC_DIR, '990_test_arena.yaml')
    old = yaml.safe_load(open(spec_path))
    new_spec = {
        'id': 990,
        'name': old['name'],
        'parent': old['parent'],
        'raw': 'data/raw/990.npy',
        'tileset': TID,
        'bgm': old['bgm'],
        'tone': [4, 2, 6, 0],
        'metadata': old['metadata'],
        'events': old['events'],
    }
    hdr = "# GENERATED by mapgen/layouts/wave16_final12_craft.py (Wave 16 Final Map Craft): Prismfall Test Arena (990).\n"
    open(spec_path, 'w').write(hdr + yaml.safe_dump(new_spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))
    print(f"Built 990 {L.shape} -> data/raw/990.npy")
    return L


def main(which=None):
    sel = set(str(w) for w in (which or []))
    groups = [
        ({'182'}, build_182),
        ({'188'}, build_188),
        ({'189'}, build_189),
        ({'281', '282'}, build_verdance_281_282),
        ({'571', '572', '573', '574', '575', '576'}, build_frostwick_571_576),
        ({'990'}, build_990),
    ]
    for ids, fn in groups:
        if not sel or (sel & ids):
            fn()


if __name__ == '__main__':
    main(sys.argv[1:])
