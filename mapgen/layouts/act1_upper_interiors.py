#!/usr/bin/env python3
"""layouts/act1_upper_interiors.py - Batch 1A Brand-New Canonical Act 1 Interiors on Tileset 34 (Prismfall Interior).

Builds 2 brand-new canonical Act 1 interiors (ZERO edits to any existing built map or shared file!):
  - 166 Reyes Cellar (Hollow cell)       (17x13, subterranean Ebbmouth stone vault beneath 164 Reyes House)
  - 184 Lumen Arcade Dept. Store 2F      (21x15, metropolitan TM/Battle Gear, Poké Doll & Rooftop Café floor above 183)

Writes mapgen/data/raw/{166,184}.npy and mapgen/specs/{166_reyes_cellar,184_lumen_arcade_2f}.yaml.

Usage:
    PRISMFALL_GFX=/home/antigravity/pf_engine_run/game/Graphics \\
      /usr/bin/python3 -I mapgen/layouts/act1_upper_interiors.py
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

# ---------------------------------------------------------------------------
# Verified Tileset 34 9-slice Floors & Rugs (all pas=0, pri=0)
# ---------------------------------------------------------------------------
CREAM_STONE = [
    [5920, 5921, 5922],
    [5928, 5929, 5930],
    [5936, 5937, 5938],
]
MODERN_TILE = [
    [640, 641, 642],
    [648, 649, 650],
    [656, 657, 658],
]
ALPINE_SLATE = [
    [1152, 1153, 1154],
    [1160, 1161, 1162],
    [1168, 1169, 1170],
]
# Pure seamless honey parquet (ONLY center 1068 — NEVER dotted-track border 1067/1069 or striped 1059..1061!)
SEAMLESS_PARQUET = [
    [1068, 1068, 1068],
    [1068, 1068, 1068],
    [1068, 1068, 1068],
]
# True TS34 9-slice brown woven rug (NEVER off-by-1!)
BROWN_WOVEN_RUG = [
    [8620, 8621, 8622],
    [8628, 8629, 8630],
    [8636, 8637, 8638],
]
RED_CARPET = [
    [7172, 7173, 7174],
    [7180, 7181, 7182],
    [7188, 7189, 7190],
]
BLUE_CARPET = [
    [7496, 7497, 7498],
    [7504, 7505, 7506],
    [7512, 7513, 7514],
]

# ---------------------------------------------------------------------------
# Verified Multi-Tile Stamps (visually confirmed from TS34 contact sheet)
# ---------------------------------------------------------------------------
CHALKBOARD = [
    [3276, 3277, 3278],
    [3284, 3285, 3286],
]
SEA_CHART = [
    [4730, 4731],
    [4738, 4739],
]
SKYLINE_WIN = [
    [2086, 2087],
    [2094, 2095],
]
SCOREBOARD_WALL = [
    [7312, 7313, 7314],
    [7320, 7321, 7322],
]
# Intact walkable ascending interior stairs (col 0 = 5683/5691/5699 walkable steps; cols 1..2 = stairwell & rail)
LOFT_STAIRS = [
    [5683, 5684, 5685],
    [5691, 5692, 5693],
    [5699, 5700, 5701],
]
VITAMIN_SHELF = [
    [2750, 2751],
    [2758, 2759],
    [2766, 2767],
]
PASTRY_CASE = [
    [7373, 7374],
    [7381, 7382],
]
FLOWER_STAND = [
    [7375],
    [7383],
    [7391],
]
SOFA_MODERN = [
    [7571, 7572, 7573],
    [7579, 7580, 7581],
]
GIANT_PLUSH_ROW = [
    [4424, 4425, 4426],
    [4432, 4433, 4434],
]
PRIZE_CASE = [
    [4408, 4409],
    [4416, 4417],
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


def _put_oak_inlay(L, x0, y0, x1, y1, mask=None):
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


def _put_lamp(L, x, y):
    """Intact 1x2 indoor brass floor lamp (2247 pri=1 over 2255 pas=15)."""
    L[2, y - 1, x] = 2247
    L[1, y, x] = 2255


def _put_plant(L, x, y, top_t=7126, bot_t=7134):
    """Intact 1x2 tall potted ficus/palm (top pri=5 on L2, pot pas=15 on L1)."""
    L[2, y - 1, x] = top_t
    L[1, y, x] = bot_t


def _put_dressed_table(L, x, y, item_l=0, item_r=0):
    """Intact 2x2 wooden table (3466..3475) on L1 with L2 tabletop props."""
    L[1, y, x] = 3466
    L[1, y, x + 1] = 3467
    L[1, y + 1, x] = 3474
    L[1, y + 1, x + 1] = 3475
    if item_l:
        L[2, y, x] = item_l
    if item_r:
        L[2, y, x + 1] = item_r


def _put_dressed_workbench(L, x, y, i0=0, i1=0, i2=0):
    """Intact 3x2 timber workbench (4082..4092) on L1 with L2 dispatch props."""
    L[1, y, x] = 4082
    L[1, y, x + 1] = 4083
    L[1, y, x + 2] = 4084
    L[1, y + 1, x] = 4090
    L[1, y + 1, x + 1] = 4091
    L[1, y + 1, x + 2] = 4092
    for dx, t in enumerate((i0, i1, i2)):
        if t:
            L[2, y, x + dx] = t


def _seam_ts34(L, floor, wall_style='stone', floor_style='slate', wall_rows=2):
    """Void-sculpted interior seamer on Tileset 34 with crisp dark charcoal architectural casing (5533..5562)."""
    H, W = floor.shape
    L[0, :, :] = VOID

    wall_face = np.zeros((H, W), dtype=bool)
    for y in range(1, H):
        for x in range(W):
            if floor[y, x] and not floor[y - 1, x]:
                for k in range(1, wall_rows + 1):
                    if y - k >= 0 and not floor[y - k, x]:
                        wall_face[y - k, x] = True

    interior = floor | wall_face

    for y in range(H):
        for x in range(W):
            if floor[y, x]:
                top_row = (y == 0) or not floor[y - 1, x]
                left_edge = (x == 0) or not floor[y, x - 1]
                right_edge = (x + 1 >= W) or not floor[y, x + 1]
                bot_edge = (y + 1 >= H) or not floor[y + 1, x]
                if floor_style == 'slate':
                    ry = 0 if top_row else (2 if bot_edge else 1)
                    rx = 0 if left_edge else (2 if right_edge else 1)
                    L[0, y, x] = ALPINE_SLATE[ry][rx]
                elif floor_style == 'diamond':
                    L[0, y, x] = 7737 if (x + y) % 2 == 0 else 7745
                else:
                    L[0, y, x] = 7099
            elif wall_face[y, x]:
                is_lower = (y + 1 < H and floor[y + 1, x])
                left_end = (x == 0) or not wall_face[y, x - 1]
                right_end = (x + 1 >= W) or not wall_face[y, x + 1]
                if wall_style == 'stone':
                    if is_lower:
                        L[0, y, x] = 1219 if left_end else (1221 if right_end else 1220)
                    else:
                        L[0, y, x] = 1211 if left_end else (1213 if right_end else 1212)
                elif wall_style == 'steel':
                    if left_end:
                        L[0, y, x] = 7536 if is_lower else 7520
                    elif right_end:
                        L[0, y, x] = 7538 if is_lower else 7522
                    else:
                        L[0, y, x] = 7537 if is_lower else 7521
                else:
                    if left_end:
                        L[0, y, x] = 1795 if is_lower else 1787
                    elif right_end:
                        L[0, y, x] = 1797 if is_lower else 1789
                    else:
                        L[0, y, x] = 1796 if is_lower else 1788
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


def _save_raw(mid, L):
    os.makedirs(RAW_DIR, exist_ok=True)
    path = os.path.join(RAW_DIR, f'{mid:03d}.npy')
    np.save(path, L.astype(np.int32))
    return f'data/raw/{mid:03d}.npy'


def _write_spec(fn, spec, header):
    path = os.path.join(SPEC_DIR, fn)
    body = yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=150, allow_unicode=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(header + body)
    return path


# ==============================================================================
# MAP 166: REYES CELLAR (HOLLOW CELL) — 17x13, TS 34 Prismfall Interior
# ==============================================================================
def build_166():
    """166: Reyes Cellar (Hollow cell) (17x13, TS 34).
    Secret subterranean Hollow resistance cell beneath 164 Reyes House (Ebbmouth).
    Return stairs at [14, 3] -> Map 164 [3, 6] down (verified walkable right next to 164's cellar hatch [1..2, 5..6]!).
    """
    W, H = 17, 13
    L = np.zeros((3, H, W), dtype=np.int32)

    # ---- 1. Void-Sculpted Subterranean Stone Vault Silhouette ----
    floor = np.zeros((H, W), dtype=bool)
    floor[4:10, 2:6] = True       # West Resistance Cot & Contraband Alcove (x=2..5, y=4..9)
    floor[9, 2] = False           # SW vault chamfer
    floor[3:11, 6:13] = True      # Central Stone Command Vault (x=6..12, y=3..10)
    floor[10, 6] = False          # South vault SW chamfer
    floor[10, 12] = False         # South vault SE chamfer
    floor[3:10, 13:16] = True     # East Stairwell & Salt-Damp Cargo Bay (x=13..15, y=3..9)
    floor[9, 15] = False          # SE vault chamfer

    _seam_ts34(L, floor, wall_style='stone', floor_style='slate', wall_rows=2)

    # ---- 2. Multi-Zone Subterranean Cellar Flooring ----
    # Damp oak duckboards in sleeping niche & beneath cellar stairwell
    _put_oak_inlay(L, 2, 4, 4, 7, mask=floor)
    _put_oak_inlay(L, 13, 3, 15, 5, mask=floor)
    # True TS34 9-slice worn brown woven rug anchoring the Hollow dispatch table (x=7..11, y=5..8)
    _put_9slice(L, BROWN_WOVEN_RUG, 7, 5, 11, 8, z=1, mask=floor)

    # ---- 3. Stone North Wall Dressings (Cipher Chalkboard, Intake Chart & Cellar Cobwebs) ----
    # Complete 3x2 green cipher chalkboard w/ chalk tray (x=7..9, y=1..2)
    _put_grid(L, CHALKBOARD, 7, 1, z_rows=(1, 1))
    # Complete 2x2 Ebbmouth Tidal Intake chart (x=10..11, y=1..2)
    _put_grid(L, SEA_CHART, 10, 1, z_rows=(1, 1))
    # Cellar cobweb tucked in NW dark masonry corner (clear of NE ascending stairwell!)
    _put_grid(L, TF['web'][0], 2, 2, z_rows=(2, 2))

    # ---- 4. Intact Ascending Cellar Staircase (x=13..15, y=2..4 -> warp at [13, 3], arrival at [13, 4]) ----
    _put_grid(L, LOFT_STAIRS, 13, 2, z_rows=(2, 1, 1))

    # ---- 5. Cold Cast-Iron Forge, Hollow Dispatch Table, Cot & Salt-Damp Contraband Crates ----
    # Cold dark cast-iron workshop forge stove (x=6, y=2..3: 4102/4110, ZERO pink kitchen towel!) w/ Framed Photograph!
    L[2, 2, 6] = 4102
    L[1, 3, 6] = 4110
    L[1, 3, 12] = 4101  # Quench & brine bucket near east stair cheek

    # West Resistance Bedroll / Quilted Cot (x=2..3, y=4..6) + Contraband Brass Floor Lantern (4,4) + Satchel (4,6)
    _put_tf(L, 'bunk_b', 2, 4)
    _put_lamp(L, 4, 4)
    L[1, 6, 4] = 5580  # Weathered Hollow courier satchel

    # Hollow Dispatch Table (x=8..10, y=6..7) on woven rug: open cipher ledger (3428), coastal chart (3429) & blueprint (3430)!
    _put_dressed_workbench(L, 8, 6, 3428, 3429, 3430)
    L[1, 8, 8] = 4077   # Resistance meeting stool W
    L[1, 8, 10] = 4077  # Resistance meeting stool E

    # Salt-Damp Contraband Crates, Brine Barrels & Smuggled Trunks (ZERO potted trees, ZERO chopped 4168!)
    _put_tf(L, 'barrel_b', 2, 7)      # (2, 7..8) Lamp-oil & brine barrel W
    _put_tf(L, 'crate_i', 4, 8)       # (4..5, 8..9) Intact banded contraband crate SW
    _put_tf(L, 'crate_i2', 14, 6)     # (14..15, 6..7) Intact salt-damp cargo crate E
    _put_tf(L, 'barrel_y', 14, 8)     # (14, 8..9) Powder & wire cask SE
    L[1, 9, 13] = 7501                # Smuggled Hollow leather courier trunk SE
    _put_tf(L, 'barrel_b', 7, 9)      # (7, 9..10) Salt-brine & wire cask at south vault wall
    L[1, 10, 8] = 4101                # Copper-wire & stencil paint bucket beside barrel

    # ---- 6. Events (Static Lore Ready for Claude Ch4 Scripting; Zero Invented Switches/Vars) ----
    events = [
        {
            'type': 'warp',
            'name': 'Cellar stairs up',
            'at': [13, 3],
            'to': {'map': 164, 'x': 3, 'y': 6, 'dir': 'down'},
            'se': 'Door exit',
        },
        {
            'type': 'sign',
            'name': 'Cipher chalkboard',
            'at': [8, 2],
            'post': False,
            'text': 'Chalked patrol schedules for the Ebbmouth Tidal Lattice intake, written in a tidy, familiar hand and half-erased in haste.',
        },
        {
            'type': 'sign',
            'name': 'Tidal intake chart',
            'at': [10, 2],
            'post': False,
            'text': 'A salt-curled chart of Ebbmouth River. Red pins trace the Meridian intake conduit under the Guild Mill.',
        },
        {
            'type': 'sign',
            'name': 'Framed photograph',
            'at': [6, 3],
            'post': False,
            'text': 'Resting on the cold forge hood: two children on the Guild Mill platform with a big man between them. On the back: "Da, Mari, Teo. AF 291."',
        },
        {
            'type': 'sign',
            'name': 'Hollow dispatch table',
            'at': [9, 7],
            'post': False,
            'text': 'Coils of copper wire, grey stencil paint, and a folded note pinned under a wrench: "Sis — they\'ll come here first. Don\'t lie for me. — T."',
        },
        {
            'type': 'npc',
            'name': 'Bereaved Lookout',
            'at': [6, 8],
            'sprite': 'trainer_HOLLOW_GRUNT_M',
            'dir': 'right',
            'text': 'Bereaved: Keep your voice down. You can hear boots on the flagstones upstairs when the tide drops.',
        },
        {
            'type': 'npc',
            'name': 'Bereaved Courier',
            'at': [11, 9],
            'sprite': 'trainer_HOLLOW_GRUNT_F',
            'dir': 'left',
            'text': 'Bereaved: We\'re packing the charts and the wire before Meridian sweeps the locks. Teo\'s already gone south.',
        },
        {
            'type': 'item',
            'name': 'Item',
            'at': [3, 9],
            'item': 'NETBALL',
        },
    ]

    ev_cells = [tuple(e['at']) for e in events] + [(13, 4), (13, 5)]
    PG.guard(L, TID, ev_cells, 'map 166')
    raw_rel = _save_raw(166, L)

    spec = {
        'id': 166,
        'name': 'Reyes Cellar (Hollow cell)',
        'parent': 164,
        'bgm': 'Cave',
        'field': 'CAVE',
        'tone': [-14, -12, 4, 24],
        'biome': 'interior',
        'metadata': {
            'MapPosition': [0, 3, 7],
        },
        'raw': raw_rel,
        'tileset': TID,
        'events': events,
    }
    hdr = '# GENERATED by mapgen/layouts/act1_upper_interiors.py (Batch 1A Act 1 Craft): 166 Reyes Cellar.\n'
    _write_spec('166_reyes_cellar.yaml', spec, hdr)
    print(f'Built 166 Reyes Cellar {L.shape} -> {raw_rel} ({len(events)} events)')
    return L


# ==============================================================================
# MAP 184: LUMEN ARCADE DEPT. STORE 2F — 21x15, TS 34 Prismfall Interior
# ==============================================================================
def build_184():
    """184: Lumen Arcade Dept. Store 2F (21x15, TS 34).
    Sleek upper department floor above 183 Lumen Arcade 1F:
      - NW: TM & Battle Gear Boutique w/ 0x80 blue-marble counter
      - NE: Vitamin & Training Counter (0x80) + Silver Escalator [19, 2] -> 183 [16, 6] left
      - SW: Plush & Poké Doll Showcase Lounge
      - SE: Rooftop-View Café Nook on seamless honey parquet
    """
    W, H = 21, 15
    L = np.zeros((3, H, W), dtype=np.int32)

    # ---- 1. Void-Sculpted Metropolitan Department Floor Silhouette ----
    floor = np.zeros((H, W), dtype=bool)
    floor[2:9, 1:20] = True       # North Retail Mezzanine & Central Concourse (x=1..19, y=2..8)
    floor[9:14, 2:19] = True      # South Boutique & Rooftop-View Café Wings (x=2..18, y=9..13)
    floor[13, 2] = False          # SW architectural chamfer
    floor[13, 18] = False         # SE architectural chamfer

    _seam_ts34(L, floor, wall_style='steel', floor_style='diamond', wall_rows=2)

    # ---- 2. Multi-Zone Metropolitan Department Flooring ----
    # NW TM & Battle Gear Boutique: sleek modern steel-blue boutique tile
    _put_9slice(L, MODERN_TILE, 1, 2, 9, 6, z=0, mask=floor)
    # NE Vitamin Counter & Escalator Mezzanine: bright cream department stone (starts x=10 so VITAMIN_SHELF at 11..12 sits inside border!)
    _put_9slice(L, CREAM_STONE, 10, 2, 19, 6, z=0, mask=floor)
    # Central Promenade Spine: crisp electric-blue carpet runner
    _put_9slice(L, BLUE_CARPET, 2, 7, 18, 8, z=1, mask=floor)
    # SW Plush & Poké Doll Showcase Lounge: plush royal crimson carpet
    _put_9slice(L, RED_CARPET, 3, 9, 9, 12, z=1, mask=floor)
    # SE Rooftop-View Café Nook: pure seamless honey parquet (1068 only — ZERO dotted seams!)
    _put_9slice(L, SEAMLESS_PARQUET, 11, 9, 18, 13, z=0, mask=floor)

    # ---- 3. Panoramic Skyline Windows & Illuminated Floor Directory (y=0..1, ZERO clipped windows!) ----
    _put_grid(L, SKYLINE_WIN, 2, 0, z_rows=(1, 1))       # x=2..3
    _put_grid(L, SKYLINE_WIN, 6, 0, z_rows=(1, 1))       # x=6..7
    _put_grid(L, SCOREBOARD_WALL, 9, 0, z_rows=(1, 1))   # x=9..11 (illuminated 2F directory!)
    _put_grid(L, SKYLINE_WIN, 13, 0, z_rows=(1, 1))      # x=13..14
    _put_grid(L, SKYLINE_WIN, 16, 0, z_rows=(1, 1))      # x=16..17 (1-tile gap before escalator at x=19!)

    # ---- 4. Sleek Silver Escalator to 1F at [19, 2] (walkable p=0x0, r=0!) ----
    L[1, 1, 19] = 7431
    L[1, 2, 19] = 7439

    # ---- 5. NW TM & Battle Gear Boutique (Symmetrical Enclosed 5-Wide U-Counter, Clerk @ [4, 3], 0x80 Counter!) ----
    # Flush against north wall (y=2..4) with both top arms capped (7224/7227) & stocked back-cabinets (ZERO walk-behind leak!)
    L[1, 2, 2] = 7224; L[1, 2, 6] = 7227
    L[1, 2, 3] = 4520; L[1, 2, 4] = 4521; L[1, 2, 5] = 4520   # Stocked steel TM inventory drawers behind clerk
    L[1, 3, 2] = 7232; L[1, 3, 6] = 7235                      # Potted pink roses on side arms (0x8f)
    L[1, 3, 3] = 4522; L[1, 3, 5] = 4522                      # Sleek steel counter lockers flanking clerk (0 cut-off tiles!)
    L[1, 4, 2] = 7240; L[1, 4, 3] = 7241; L[1, 4, 4] = 7242; L[1, 4, 5] = 7241; L[1, 4, 6] = 7243  # Front 0x80 counter!
    # Stocked TM racks & low glass battle-gear showcase
    _put_tf(L, 'shelf_goods', 8, 2)    # (8..9, 2..4) TM & Evo Stone boutique rack
    _put_tf(L, 'display', 8, 5)        # (8..9, 5..6) Glass Battle Gear showcase

    # ---- 6. NE Vitamin & Training Counter (Symmetrical Enclosed 5-Wide U-Counter, Clerk @ [15, 3], 0x80 Counter!) ----
    # Glass Pharmacy / Vitamin Showcase cleanly inside CREAM_STONE border (x=11..12, y=2..4)
    _put_grid(L, VITAMIN_SHELF, 11, 2, z_rows=(2, 1, 1))
    # Matching symmetrical 5-wide U-counter (x=13..17, y=2..4) leaving x=18..19 wide open for Escalator!
    L[1, 2, 13] = 7224; L[1, 2, 17] = 7227
    L[1, 2, 14] = 4520; L[1, 2, 15] = 4521; L[1, 2, 16] = 4520  # Stocked pharmacy cabinets behind clerk
    L[1, 3, 13] = 7232; L[1, 3, 17] = 7235                      # Potted pink roses on side arms (0x8f)
    L[1, 3, 14] = 4522; L[1, 3, 16] = 4522                      # Sleek pharmacy lockers flanking clerk (0 cut-off tiles!)
    L[1, 4, 13] = 7240; L[1, 4, 14] = 7241; L[1, 4, 15] = 7242; L[1, 4, 16] = 7241; L[1, 4, 17] = 7243  # Front 0x80 counter!

    # ---- 7. SW Plush & Poké Doll Showcase Lounge (x=2..9, y=9..13) ----
    # Showstopper Giant Charizard/Magikarp Poké Dolls on crimson showcase carpet (x=3..5, y=9..10)
    _put_grid(L, GIANT_PLUSH_ROW, 3, 9, z_rows=(2, 1))
    # Plushie Display Table 1 (x=7..8, y=9..10) topped with intact Lapras Poké Doll (4411) & Plush Catalog (4544)!
    _put_dressed_table(L, 7, 9, 4411, 4544)
    # Colorful Toy & Plushie Capsule Rack (x=4..5, y=12..13) + Plushie Display Table 2 (7..8, 12..13) w/ Eevee (4410) & Piplup (4414)!
    _put_grid(L, PRIZE_CASE, 4, 12, z_rows=(2, 1))
    _put_dressed_table(L, 7, 12, 4410, 4414)
    _put_plant(L, 2, 12)  # Parlor ficus framing plush lounge

    # ---- 8. SE Rooftop-View Café Nook (x=11..18, y=9..13 on pure seamless 1068 honey parquet!) ----
    # Illuminated Glass Bakery & Pastry Showcase (x=12..13, y=9..10)
    _put_grid(L, PASTRY_CASE, 12, 9, z_rows=(1, 1))
    # Dressed Café Bistro Table (x=15..16, y=9..10) w/ steaming white espresso cup (4541) & pastry plate (4537)!
    _put_dressed_table(L, 15, 9, 4541, 4537)
    L[1, 10, 14] = 4077  # Café bistro stool W
    L[1, 10, 17] = 4077  # Café bistro stool E
    # Plush Modern Silver Café Lounge Sofa (x=13..15, y=12..13) + Tall Flower Bouquet Stand (18, 9..11)
    _put_grid(L, SOFA_MODERN, 13, 12, z_rows=(2, 1))
    _put_grid(L, FLOWER_STAND, 18, 9, z_rows=(2, 1, 1))

    # ---- 9. Warm Modern Lighting & Metropolitan Parlor Greenery ----
    _put_lamp(L, 1, 3)     # NW boutique brass floor lamp
    _put_lamp(L, 17, 13)   # SE café warm corner lamp
    _put_plant(L, 1, 8)    # West promenade ficus
    _put_plant(L, 19, 8)   # East promenade ficus
    _put_plant(L, 10, 13)  # South divider parlor fern (5431/5439)
    L[2, 12, 10] = 5431
    L[1, 13, 10] = 5439

    # ---- 10. Events (Static Lore + Authentic Marts; Zero Invented Switches/Vars) ----
    events = [
        {
            'type': 'warp',
            'name': 'Escalator to 1F',
            'at': [19, 2],
            'to': {'map': 183, 'x': 16, 'y': 6, 'dir': 'left'},
            'se': 'Door exit',
        },
        {
            'type': 'mart',
            'name': 'TM & Evo Clerk',
            'at': [4, 3],
            'sprite': 'NPC 22',
            'dir': 'down',
            'greeting': 'Welcome to Lumen Arcade 2F! Looking for Technical Machines or Evolution Stones?',
            'items': ['TM17', 'TM73', 'TM10', 'THUNDERSTONE', 'FIRESTONE', 'WATERSTONE', 'LEAFSTONE', 'LINKINGCORD'],
        },
        {
            'type': 'mart',
            'name': 'Vitamin Clerk',
            'at': [15, 3],
            'sprite': 'NPC 17',
            'dir': 'down',
            'greeting': 'Keep your Pokémon in peak Zenith form with our premium training supplements!',
            'items': ['HPUP', 'PROTEIN', 'IRON', 'CALCIUM', 'ZINC', 'CARBOS'],
        },
        {
            'type': 'npc',
            'name': 'Plush Collector',
            'at': [6, 11],
            'sprite': 'NPC 19',
            'dir': 'up',
            'text': 'Shopper: These Tenth Year of Light Poké Dolls sell out before noon! I queued all morning for the Lapras.',
        },
        {
            'type': 'npc',
            'name': 'Café Barista',
            'at': [12, 11],
            'sprite': 'NPC 09',
            'dir': 'right',
            'text': 'Barista: Best view of the Concourse airships right from the café counter. Care for a warm Lumen roast?',
        },
        {
            'type': 'npc',
            'name': 'Battle Shopper',
            'at': [10, 7],
            'sprite': 'trainer_COOLTRAINER_M',
            'dir': 'left',
            'text': 'Trainer: Rook\'s Circuit Gym runs on the Neon Grid. Protect and Thunder Wave TMs from this floor are lifesavers.',
        },
        {
            'type': 'sign',
            'name': 'Floor Directory',
            'at': [10, 1],
            'post': False,
            'text': 'LUMEN ARCADE 2F — WEST: TM & Battle Gear | SW: Poké Doll Showcase | EAST: Vitamins & Rooftop-View Café.',
        },
    ]

    ev_cells = [tuple(e['at']) for e in events] + [(18, 2), (19, 3), (4, 5), (15, 5)]
    PG.guard(L, TID, ev_cells, 'map 184')
    raw_rel = _save_raw(184, L)

    spec = {
        'id': 184,
        'name': 'Lumen Arcade Dept. Store 2F',
        'parent': 180,
        'bgm': 'Poke Mart',
        'field': 'NONE',
        'tone': [-4, -2, 8, 2],
        'biome': 'interior',
        'metadata': {
            'MapPosition': [0, 16, 16],
        },
        'raw': raw_rel,
        'tileset': TID,
        'events': events,
    }
    hdr = '# GENERATED by mapgen/layouts/act1_upper_interiors.py (Batch 1A Act 1 Craft): 184 Lumen Arcade Dept. Store 2F.\n'
    _write_spec('184_lumen_arcade_2f.yaml', spec, hdr)
    print(f'Built 184 Lumen Arcade 2F {L.shape} -> {raw_rel} ({len(events)} events)')
    return L


def main():
    build_166()
    build_184()


if __name__ == '__main__':
    main()
