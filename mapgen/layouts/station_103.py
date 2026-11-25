#!/usr/bin/env python3
"""layouts/station_103.py - Wave 6 Rejuvenation V14 redesign of Map 103 (Larch Research Station, 28x19, Tileset 34).

Transforms Chapter 0's iconic Starter-Pokemon Laboratory from a boxy split-floor rectangle (with a half-clipped
labtank, clipped floating clock, broken sliced plant pots, and a staircase blocking the front door!) into a warm,
void-sculpted three-zone Coastal Field-Research Laboratory & Wayfarer Botanical Starter Conservatory:
  - West Coastal Research Library & Study (x=3..11): warm Sheridan timber, floor-to-ceiling field bookcases,
    framed tide charts, Larch's long research & seed-packet bench, cozy crimson-rug study nook & Kestrel's hayloft stairs
  - Central Vaulted Arrival Foyer & Telemetry Spine (x=12..16): warm cream-and-gold lobby stone, ornate crimson-silver
    arrival runner opening directly from the front door (14,15) toward the Meridian Imprint scanner & kelp kettle
  - East Vaulted Wayfarer Botanical Starter Conservatory (x=17..24): stepped 1 tile north with tall sunlit arched
    glasshouse windows, luminous emerald-diamond conservatory tile framing a sunlit cream-gold Starter Presentation
    Podium (Starter table @ (20,10)), COMPLETE FIXED 3-wide Specimen Incubator (4784..4810), starter pen, and lush
    intact botanical parlor trees & flowering planters (ZERO clipped sprites or Rowan pot overlap!).

Updates ONLY Map 103 in mapgen/specs/101_ferrows_landing_interiors.yaml and writes mapgen/data/raw/103.npy,
leaving maps 101-102, 104-107, and Wave 5's 108 untouched and preserving 100% of all 11 HEAD events & cutscene paths.
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
FLOOR_GLASS = 501       # luminous emerald-diamond Wayfarer glasshouse tile
W, H = 28, 19


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


def build_103_layers():
    L = np.zeros((3, H, W), dtype=np.int32)
    L[0, :, :] = VOID

    # ------------------------------------------------------------------ 1. Void-sculpted Multi-Bay Silhouette
    # Three distinct architectural bays carved into pure black void (ZERO flat rectangular box!):
    #   - West Coastal Research Library & Study: x=3..11, y=5..13 (SW chamfer at (3..4, 13)!)
    #   - Central Foyer & Telemetry Spine:       x=12..16, y=5..14 + recessed Entry Door Notch x=13..15, y=15
    #   - East Vaulted Botanical Conservatory:   x=17..24, y=4..13 (steps 1 tile higher north for sunlit glasshouse bay,
    #                                            with SE chamfer at (23..24, 13)!)
    floor = np.zeros((H, W), dtype=bool)
    floor[5:14, 3:12] = True       # West study (x=3..11, y=5..13)
    floor[13, 3:5] = False         # SW corner chamfer carved into void
    floor[5:15, 12:17] = True      # Central foyer & telemetry spine (x=12..16, y=5..14)
    floor[15, 13:16] = True        # Recessed entry door notch (x=13..15, y=15)
    floor[4:14, 17:25] = True      # East vaulted botanical conservatory (x=17..24, y=4..13)
    floor[13, 23:25] = False       # SE corner chamfer carved into void

    # ------------------------------------------------------------------ 2. Sheridan Perimeter Wall Auto-Seamer
    wall_face = np.zeros((H, W), dtype=bool)
    for y in range(3, H):
        for x in range(1, W - 1):
            if floor[y, x] and not floor[y - 1, x]:
                wall_face[y - 1, x] = True
                wall_face[y - 2, x] = True

    interior = floor | wall_face

    for y in range(H):
        for x in range(W):
            if floor[y, x]:
                top_row = not floor[y - 1, x]
                left_edge = not floor[y, x - 1]
                if top_row:
                    L[0, y, x] = 5352 if left_edge else 5353 + (x - 4) % 3
                else:
                    L[0, y, x] = 5360 if left_edge else 5361 + (x - 4) % 3
            elif wall_face[y, x]:
                is_lower = (y + 1 < H and floor[y + 1, x])
                left_end = not wall_face[y, x - 1]
                right_end = not wall_face[y, x + 1]
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

    # ------------------------------------------------------------------ 3. Rich Three-Zone Floor Craft
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

    # Zone A: West Research Study (x=3..11) keeps warm Sheridan timber planks + cozy woven crimson study rug!
    _put_9slice(L, SHER_RUG, 6, 10, 9, 12, z=1)

    # Zone B: Central Arrival Foyer Spine (x=13..15, y=6..14) - warm cream-gold stone framing a continuous
    # ornate crimson-and-silver Arrival Runner (y=7..14) straight from Exit (14,15) toward Larch & the Sanctuary!
    # Keeping x=12 & x=16 in warm Sheridan timber eliminates the stark white empty patch while framing the runner!
    _put_9slice(L, CREAM_STONE, 13, 6, 15, 14, z=0)
    # Sleek blue-slate telemetry pad right under the Meridian Imprint Scanner (x=11..12, y=5..6)
    _put_9slice(L, BLUE_STONE, 11, 5, 12, 6, z=0)
    _put_9slice(L, HOTEL_RUG, 13, 7, 15, 14, z=1)
    # Entry doormat at (13..15, 15)
    for i, x in enumerate((13, 14, 15)):
        L[1, 15, x] = 5512 + i

    # Zone C: East Vaulted Wayfarer Botanical Starter Conservatory (x=17..24, y=4..13)
    for y in range(4, 14):
        for x in range(17, 25):
            if floor[y, x]:
                L[0, y, x] = FLOOR_GLASS
    # Warm Crimson-and-Gold Woven Starter Showcase Carpet directly framing the Starter Table (x=18..21, y=8..11)
    # over sunlit emerald conservatory tiles (ZERO stark white square!)
    _put_9slice(L, SHER_RUG, 18, 8, 21, 11, z=1)

    # ------------------------------------------------------------------ 4. Architectural North Wall Features
    # Vertical timber pilasters separating bays
    for px, py in ((6, 3), (10, 3), (13, 3), (19, 2), (22, 2)):
        L[0, py, px] = 5548
        L[0, py + 1, px] = 5556
    # Arched sunlit harbor windows on study & vaulted conservatory walls + diamond maritime porthole!
    for wx, wy in ((9, 3), (15, 3), (18, 2), (21, 2), (23, 2)):
        L[0, wy, wx] = 5544
        L[0, wy + 1, wx] = 5552
    L[0, 3, 5] = 5560; L[0, 4, 5] = 5568  # Maritime diamond porthole above field library

    # Wall research charts & maps (ZERO clipping!)
    _put_tf(L, 'map_wall', 6, 3)          # Velmora coastal tide chart (6..8, 3)
    L[1, 3, 10] = 5453; L[1, 4, 10] = 5461  # Framed deep-ocean chart beside Larch's workspace
    L[1, 2, 20] = 5453; L[1, 3, 20] = 5461  # Botanical specimen chart on vaulted conservatory wall

    # ------------------------------------------------------------------ 5. West Wing: Coastal Research Library & Study
    # Grand floor-to-ceiling Field Library Bookcases backing `Station bookshelf @ (4, 5)`!
    _put_tf(L, 'bookcase', 3, 4)          # (3..4, 4..5) -> solid bookcase at (4,5) matching Station bookshelf!
    _put_tf(L, 'bookshelf_s', 5, 4)       # (5, 4..5) -> tall field shelf right beside it!
    _put_tf(L, 'cabinet', 3, 11)          # (3..4, 11..12) sample specimen cabinet in SW study corner
    _put_tf(L, 'desk', 3, 8)              # (3..4, 8..9) coastal chart writing desk against west wall
    L[2, 8, 3] = 3428                     # open tide chart ledger cleanly centered ON the desktop!
    # Larch's Long Seed-Packet & Research Workbench (x=6..9, y=7..8):
    # Positioned directly between Professor Larch @ (9, 6) and Juno @ (8, 9), leaving Juno's entire cutscene walk
    # (8..11, 9) and Larch's entire cutscene walk (9..15, 6) 100% OPEN & UNOBSTRUCTED!
    _put_tf(L, 'table_dark', 6, 7)        # (6..7, 7..8) west research bench
    _put_tf(L, 'table_dark', 8, 7)        # (8..9, 7..8) east research bench right above Juno @ (8, 9)!
    L[2, 7, 7] = 3428                     # open field notes on Larch's bench!
    # Cozy crimson-rug study table & stools (x=6..9, y=10..12)
    _put_tf(L, 'table_tea', 7, 10)        # (7..8, 10..11) tea table on study rug
    L[2, 11, 6] = 4077                    # wooden stool west of study table
    L[2, 11, 9] = 4077                    # wooden stool east of study table
    _put_tf(L, 'crate_i', 5, 12)          # (5..6, 12..13) packed field equipment crate
    L[1, 13, 7] = 5580                    # vintage expedition leather suitcase
    L[1, 13, 8] = 3391                    # brass potted herb

    # ------------------------------------------------------------------ 6. Central Spine: Imprint Scanner, Kelp Kettle & Hayloft Stairs!
    # Imprint Scanner @ (12, 5): sleek blue Meridian diagnostic console at (11..12, 5) + telemetry notices on wall (11..12, 3..4)!
    # ZERO overlap with Larch's kitchenette!
    L[1, 5, 11] = 5849                    # blue Meridian readout desk
    L[1, 5, 12] = 5855                    # green-screen Meridian Imprint Scanner terminal right at (12, 5)!
    _put_grid(L, [[5795, 5796], [5803, 5804]], 11, 3, z_rows=(1, 1))
    # Larch's Kitchenette & Blackened Kelp Kettle (`kitchen`, 4x2) cleanly at (13..16, 4..5) backing `Kettle @ (14, 5)`!
    _put_tf(L, 'kitchen', 13, 4)
    # Kestrel's Hayloft Staircase (3x4) tucked cleanly at (10..12, 10..13) — opening a wide central foyer runner (13..15, 10..15)
    # directly from Exit (14, 15) AND keeping Kestrel's entire drop & walk route ((13,8)->(13,10)->(13,11)->(14,11))
    # and Nickit (loft) @ (12, 7) 100% OPEN & CLEAR!
    LOFT_STAIRS = [
        [5675, 5676, 5677],
        [5683, 5684, 5685],
        [5691, 5692, 5693],
        [5699, 5700, 5701],
    ]
    _put_grid(L, LOFT_STAIRS, 10, 10, z_rows=(2, 1, 1, 1))
    # Welcoming potted parlor tree & brass flowerpot flanking the recessed Entry Vestibule!
    L[2, 13, 16] = 7126; L[1, 14, 16] = 7134
    L[1, 14, 12] = 3391

    # ------------------------------------------------------------------ 7. East Wing: Wayfarer Botanical Starter Conservatory!
    # COMPLETE FIXED 3-WIDE Specimen Incubator (`LABTANK_FULL`, 4784..4810) at (18..20, 3..6)!
    # (Tucked against the vaulted north conservatory wall y=3, base at y=6 -> ZERO clipping, ALL 3 columns intact!)
    LABTANK_FULL = [
        [4784, 4785, 4786],
        [4792, 4793, 4794],
        [4800, 4801, 4802],
        [4808, 4809, 4810],
    ]
    _put_grid(L, LABTANK_FULL, 18, 3, z_rows=(2, 1, 1, 1))

    # Heroic Starter Presentation Table (`table_tea`, 2x2) at (19..20, 9..10) supporting `Starter table @ (20, 10)`!
    # Stands proudly on the sunlit cream-gold stone podium & crimson presentation mat, with Rowan Ashby @ (17, 10)
    # and Juno (station) @ (19, 11) standing cleanly on open floor!
    _put_tf(L, 'table_tea', 19, 9)

    # Cozy Wooden Wayfarer Starter Pen (`pen`, 3x3) at (22..24, 9..11) right beside the Starter Presentation Podium!
    _put_tf(L, 'pen', 22, 9)

    # Lush Intact Botanical Conservatory Trees, Flowering Planters & Seed Trays (ZERO broken sliced pots!)
    # Verified clean Sheridan/Hotel 1x2 trees (top r5, pot p15/r0):
    #   - (5415, 5423) lush parlor tree
    #   - (5431, 5439) lush fern palm
    #   - (7126, 7134) tall hotel ficus
    #   - (7874, 7882) grand conservatory palm
    for tx, ty, top_t, bot_t in (
        (17, 4, 5415, 5423),              # NW conservatory entrance tree
        (21, 4, 7874, 7882),              # North sunlit conservatory palm beside incubator
        (23, 4, 5431, 5439),              # NE conservatory fern palm
        (24, 6, 7126, 7134),              # East wall tall conservatory ficus
        (17, 12, 5431, 5439),             # SW conservatory fern palm framing entry
        (22, 12, 5415, 5423),             # SE chamfer corner conservatory tree
    ):
        L[2, ty, tx] = top_t
        L[1, ty + 1, tx] = bot_t

    # Flowering botanical stone planters (7177/7178) & watering bucket/seed trays!
    L[1, 5, 22] = 7177                    # flowering moss planter along north glasshouse wall
    L[1, 5, 24] = 7178                    # blooming pink flower planter in NE corner
    L[1, 8, 17] = 7178                    # blooming seed tray right north of Rowan Ashby (17, 10) — NO overlap!
    L[1, 13, 18] = 7177                   # south glasshouse botanical planter
    L[1, 13, 21] = 7178                   # south glasshouse blooming planter
    _put_tf(L, 'bucket', 22, 7)           # conservatory watering bucket beside starter pen!
    _put_tf(L, 'stool', 18, 12)           # caretaker stool near Rowan & Juno
    # Keep (16, 13..14) parlor tree intact (re-assert cleanly after clearing barrel_b)
    L[2, 13, 16] = 7126; L[1, 14, 16] = 7134

    # Passguard sweep guarantees 0 passability conflicts on Tileset 34!
    PG.guard(L, TID)
    return L


def main():
    L = build_103_layers()
    raw_dir = os.path.join(HERE, 'data', 'raw')
    os.makedirs(raw_dir, exist_ok=True)
    np.save(os.path.join(raw_dir, '103.npy'), L.astype(np.int16))

    # Update ONLY Map 103 in mapgen/specs/101_ferrows_landing_interiors.yaml, preserving 101-102, 104-108!
    spec_path = os.path.join(HERE, 'specs', '101_ferrows_landing_interiors.yaml')
    docs = [d for d in yaml.safe_load_all(open(spec_path)) if d]
    new_docs = []
    found = False
    for d in docs:
        if d.get('id') == 103:
            found = True
            s103 = {
                'id': 103,
                'name': d['name'],
                'parent': d['parent'],
                'bgm': d['bgm'],
                'metadata': d['metadata'],
                'tone': [12, 6, -10, 0],
                'biome': 'interior',
                'tileset': TID,
                'raw': 'data/raw/103.npy',
                'events': d['events'],
            }
            new_docs.append(s103)
        else:
            new_docs.append(d)
    assert found, 'Map 103 not found in 101_ferrows_landing_interiors.yaml!'

    header = "# Ferrow's Landing interiors (101-108). 103 by station_103.py; 108 by customs_108.py; others by early_interiors.py.\n"
    out = header + '\n---\n'.join(
        yaml.safe_dump(s, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True)
        for s in new_docs
    )
    open(spec_path, 'w').write(out)
    print(f'Wrote data/raw/103.npy ({L.shape}) and updated map 103 in {spec_path}')


if __name__ == '__main__':
    main()
