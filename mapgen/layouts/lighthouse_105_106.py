#!/usr/bin/env python3
"""layouts/lighthouse_105_106.py - Wave 7 Rejuvenation V14 redesign of Ferrow Lighthouse:
  - Map 105: Ferrow Lighthouse 1F (20x16, Tileset 34)
      Sculpted octagonal weathered-stone & warm coastal-timber lighthouse ground floor:
      storm entry vestibule around Exit (7,12), cozy crimson hearth living nook, Kestrel's
      west cot alcove (3,6), stone-wall cracked mirror (5,5), iron-bound locked sea trunk (8,10),
      maritime rope & rigging station (10,10), timber lighthouse stairwell (9..11, 3..6) up to
      Lamp Room (11,6), and an eastern Keeper's Chart & Lantern Watch Bay (x=12..15).
  - Map 106: Ferrow Lighthouse Lamp Room (20x15, Tileset 34)
      Breathtaking symmetric octagonal panoramic glass-and-stone Fresnel Beacon Rotunda
      centered dead-on x=6 directly behind Hesper Vane (6,7): 7-tile continuous coastal
      glass lantern windows, radiant golden sunburst dais (585..603) surrounded by cool
      slate gallery stone, towering 3x3 Starlight Crystal Fresnel Great Lamp (3872..3890)
      flanked by brass reflector lamps, keeper's lamp-oil drums, logbook & globe alcove,
      and a crisp wooden stairwell landing at Warp (4,9) -> 105 (10,7).

Updates ONLY Maps 105 & 106 inside mapgen/specs/101_ferrows_landing_interiors.yaml and
writes mapgen/data/raw/105.npy & 106.npy, leaving 101-104 and 107-108 100% untouched.
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


def _seam_stone_room(L, floor, wall_rows=2, base_floor_fn=None):
    """Paint weathered coastal stone-brick north walls (1203..1221) + crisp dark-timber
    perimeter void casing (5533..5562) around any sculpted boolean floor mask."""
    H, W = floor.shape
    L[0, :, :] = VOID

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
                if is_lower:
                    L[0, y, x] = 1219 if left_end else (1221 if right_end else 1220)
                else:
                    L[0, y, x] = 1211 if left_end else (1213 if right_end else 1212)
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


# ====================================================================================== MAP 105: FERROW LIGHTHOUSE 1F
def build_105_layers():
    W, H = 20, 16
    L = np.zeros((3, H, W), dtype=np.int32)

    # 1. Void-sculpted Octagonal Stone-and-Timber Coastal Lighthouse Ground Floor:
    #    Main tower chamber x=3..14, y=5..11 with SW (3..4, 11) & SE (13..14, 11) chamfers,
    #    recessed storm entry vestibule around Exit @ (7, 12) (x=6..8, y=12),
    #    and a projecting East Keeper's Watch Bay (x=15..16, y=6..10) so the tower fills the
    #    canvas dramatically while keeping every single event at its exact HEAD coordinate!
    floor = np.zeros((H, W), dtype=bool)
    floor[5:12, 3:15] = True       # Core tower floor x=3..14, y=5..11
    floor[11, 3:5] = False         # SW octagonal tower chamfer
    floor[11, 13:15] = False       # SE octagonal tower chamfer
    floor[12, 6:9] = True          # Storm entry vestibule around Exit (7, 12)
    floor[6:11, 15:17] = True      # East Keeper's Watch & Chart Bay (x=15..16, y=6..10)

    _seam_stone_room(L, floor, wall_rows=2)

    # 2. Architectural Floor Zoning:
    #    - Cool weathered coastal slate stone vestibule at Entry (x=6..8, y=11..12)
    #    - Warm Sheridan crimson braided living rug in center hearth (x=5..8, y=7..9)
    #    - Slate watch alcove under East Keeper's bay (x=14..16, y=6..10)
    SLATE = [
        [1152, 1153, 1154],
        [1160, 1161, 1162],
        [1168, 1169, 1170],
    ]
    SHER_RUG = [
        [5411, 5412, 5413],
        [5419, 5420, 5421],
        [5427, 5428, 5429],
    ]
    for y in (11, 12):
        for x in (6, 7, 8):
            L[0, y, x] = SLATE[0 if y == 11 else 2][x - 6]
    # Warm timber entry mat at (6..8, 12) framing Exit (7, 12)
    for i, x in enumerate((6, 7, 8)):
        L[1, 12, x] = 5512 + i

    # East watch bay stone flagstones (x=14..16, y=6..10)
    _put_9slice(L, SLATE, 14, 6, 16, 10, z=0)

    # Cozy crimson woven parlor rug under hearth table (x=5..8, y=7..9)
    _put_9slice(L, SHER_RUG, 5, 7, 8, 9, z=1)

    # 3. Weathered Stone North Wall Features (y=3..4 on main tower; y=4..5 on east bay):
    #    - Sunlit 2x2 coastal sky arched window above Kestrel's sleeping alcove (3..4, 3..4)
    _put_grid(L, [[2086, 2087], [2094, 2095]], 3, 3, z_rows=(1, 1))
    #    - Cracked stone-wall mirror right above Cracked mirror @ (5, 5): (5, 3..4)!
    L[1, 3, 5] = 5250
    L[1, 4, 5] = 5258
    #    - Arched sunlit coastal window beside the staircase (12..13, 3..4)
    _put_grid(L, [[2086, 2087], [2094, 2095]], 12, 3, z_rows=(1, 1))
    #    - Framed coastal sea chart on the East Watch Bay stone wall (15..16, 4..5)
    _put_grid(L, [[4730, 4731], [4738, 4739]], 15, 4, z_rows=(1, 1))
    #    - Warm single lighthouse window on the galley bay (7, 3..4)
    L[1, 3, 7] = 2073
    L[1, 4, 7] = 2081

    # 4. Exact Story Anchors & Authentic Keeper's Lighthouse Props (100% HEAD Events Preserved!):
    #    - Cot @ (3, 6): Kestrel's cozy weathered wooden cot (bunk_o at (3..4, 5..7) -> 4148 squarely on (3, 6)!)
    _put_tf(L, 'bunk_o', 3, 5)
    #    - Warm bedside brass ruby lamp at (3, 8..9) illuminating Kestrel's cot & SW alcove
    L[2, 8, 3] = 2244
    L[1, 9, 3] = 2252
    #    - Coastal kettle & hearth shelf (6..8, 4..5) tucked neatly between Cracked mirror (5,5) and Stairs (9..11, 3..6)!
    #      Keep (5, 5) 100% open & walkable so Cracked mirror @ (5, 5) works identically to HEAD!
    _put_tf(L, 'shelf_bottles', 6, 4)     # (6..7, 4..5) oil bottles & keeper's tea shelf
    L[1, 5, 8] = 4077                     # wooden keeper's stool beside stove/stairs

    #    - Lighthouse Timber Staircase ascending cleanly to Lamp Room Warp @ (11, 6)!
    #      Arrival from 106 lands cleanly at (10, 7); stepping UP from (11, 7) bumps (11, 6) Warp!
    TOWER_STAIRS = [
        [5675, 5676, 5677],
        [5683, 5684, 5685],
        [5691, 5692, 5693],
        [5699, 5700, 5701],
    ]
    _put_grid(L, TOWER_STAIRS, 9, 3, z_rows=(2, 1, 1, 1))

    #    - Cozy Center Hearth Table & Open Keeper's Logbook on the crimson rug (x=6..7, y=7..8)
    _put_tf(L, 'table_tea', 6, 7)
    L[2, 7, 6] = 3428                     # open lighthouse logbook centered cleanly on table!

    #    - Locked Sea Trunk @ (8, 10): genuine 2x2 iron-bound wooden sea chest at (7..8, 9..10)!
    #      (Wait: (7, 9) overlaps rug edge cleanly; let's check (7..8, 9..10) vs table (6..7, 7..8):
    #       y=8 is table bottom, y=9 is trunk top — leaving (5, 9..10), (6, 9..10), (9, 9..10), (7..8, 11) ALL open!)
    #      Wait: leave a 1-tile gap between table (6..7, 7..8) and trunk so nothing looks cramped!
    #      Move table_tea 1 tile north to (6..7, 6..7) OR place trunk cleanly at (7..8, 9..10) with table at (6..7, 7..8)?
    #      Even cleaner: table at (6..7, 6..7) (wait: (6, 5) has shelf_bottles, so (6..7, 6..7) sits right below shelf,
    #      leaving y=8 completely open promenade between table and Trunk @ (7..8, 9..10)!)
    #      Wait: check (5, 5) Cracked mirror and (5, 6) walkable: (6..7, 6..7) leaves (5, 5..10) AND (8, 6..8) wide open!
    L[1, 7:9, 6:8] = 0
    L[2, 7:9, 6:8] = 0
    # Re-stamp crimson rug cleanly across (5..8, 7..9), and put a crisp 1x1 stool/tea table or keep hearth rug open at (5..8, 7..8)
    _put_9slice(L, SHER_RUG, 5, 7, 8, 9, z=1)
    _put_tf(L, 'table_dark', 6, 7)        # (6..7, 7..8) warm dark coastal table on hearth rug
    L[2, 7, 6] = 3428
    # Put our 2x2 iron-bound sea trunk cleanly at (7..8, 10..11)? NO! Trunk event is at (8, 10)!
    # Wait: (7..8, 9..10) has 5585/5586 at y=9 and 5593/5594 at y=10 (so brass lock sits right on (8, 10)!).
    # Let's move table 1 tile west to (5..6, 7..8) so there is a wide diagonal gap to Trunk (7..8, 9..10)!
    L[1, 7:9, 6:8] = 0; L[2, 7:9, 6:8] = 0
    _put_9slice(L, SHER_RUG, 5, 7, 8, 9, z=1)
    _put_tf(L, 'table_tea', 5, 7)         # (5..6, 7..8) cozy hearth tea table on west half of rug!
    L[2, 7, 5] = 3428                     # open logbook cleanly centered on table!
    # Genuine 2x2 iron-bound sea chest right at (7..8, 9..10) — brass lock squarely on Trunk @ (8, 10)!
    _put_grid(L, [[5585, 5586], [5593, 5594]], 7, 9, z_rows=(1, 1))

    #    - Rope coils @ (10, 10): coiled nautical rope basket (4168) right at (10, 10) + coiled maritime gear!
    #      Keep (9, 10) & (10, 9) & (10, 11) wide open so player walks cleanly around BOTH Trunk (8,10) & Rope coils (10,10)!
    L[1, 10, 10] = 4168                   # coiled nautical rope & rigging basket right on (10, 10)
    L[1, 10, 11] = 4101                   # weathered oak pitch bucket beside the spliced rope!

    #    - SW Alcove Maritime Detail (x=3..5, y=10): lifebuoy & brass storm lantern flanking vestibule
    L[1, 10, 4] = 4118; L[1, 10, 5] = 4119
    L[2, 9, 5] = 0                        # keep (5, 9) clean walkable
    # Wait: lifering is 2x2 (4118..4127)! Don't slice it in half!! Put COMPLETE 2x2 lifering on wall at (13..14, 4..5)
    # or at (3..4, 9..10) (wait: (3, 9) has lamp)! Put lamp at (5, 10..11) and complete 2x2 lifering at (3..4, 9..10)?
    # Even cleaner: put COMPLETE 2x2 lifering at (13..14, 5..6) on the stone wall/floor — wait: (13, 4) has window!
    # Let's clear (4..5, 10) and place COMPLETE intact props ONLY (ZERO half-sliced tiles!):
    L[1, 10, 4] = 0; L[1, 10, 5] = 0
    _put_grid(L, [[4118, 4119], [4126, 4127]], 3, 9, z_rows=(1, 1))  # COMPLETE 2x2 maritime lifebuoy at (3..4, 9..10)!
    # Warm indoor brass candle lamp flanking the SW stone vestibule (5, 10..11)
    L[2, 8, 3] = 0; L[1, 9, 3] = 0
    L[2, 10, 5] = 2247; L[1, 11, 5] = 2255

    #    - East Keeper's Watch & Chart Bay (x=12..16, y=6..10):
    #      Keep (12..13, 6..10) open circulation beside stairs (11,6) and arrival (10,7)!
    _put_tf(L, 'bookcase', 13, 5)         # (13..14, 5..6) tall maritime ledger bookcase against stone wall
    _put_tf(L, 'desk', 15, 6)             # (15..16, 6..7) Keeper's Navigation Desk beneath framed sea chart!
    L[2, 6, 15] = 3428                    # open navigation chart on desk!
    L[2, 6, 16] = 3151; L[1, 7, 16] = 3143  #Wait: check globe_3143! 3143 is top (pas=15) or bottom? Keep desk clean & put intact plant/drums!
    L[2, 6, 16] = 0; L[1, 7, 16] = 0
    _put_tf(L, 'desk', 15, 6)
    L[2, 6, 15] = 3428
    # Tall brass oil drums (COMPLETE 1x2 pairs: 4822/4830 & 4823/4831) + fishing rods bucket (4060/4068) in SE bay!
    L[2, 8, 16] = 4822; L[1, 9, 16] = 4830
    L[2, 9, 15] = 4060; L[1, 10, 15] = 4068  # COMPLETE 1x2 fishing rods bucket
    L[2, 9, 16] = 0; L[1, 10, 16] = 4101     # oak oil bucket in SE corner
    # Weathered brass tool satchel flanking SE vestibule chamfer (12, 11) + lush intact coastal fern (14, 9..10)!
    L[1, 11, 12] = 5580
    L[2, 9, 14] = 5431; L[1, 10, 14] = 5439  # COMPLETE intact coastal fern palm!

    PG.guard(L, TID, [(7, 12), (11, 6), (10, 10), (3, 6), (5, 5), (8, 10)], 'map 105')
    return L


# ====================================================================================== MAP 106: LIGHTHOUSE LAMP ROOM
def build_106_layers():
    W, H = 20, 15
    L = np.zeros((3, H, W), dtype=np.int32)

    # 1. Void-sculpted SYMMETRIC OCTAGONAL PANORAMIC LANTERN ROTUNDA!
    #    Centered DEAD-ON x=6 directly behind Hesper Vane @ (6, 7) and the Great Fresnel Lamp @ (5..7, 4..6)!
    #    - Walkable Octagon Interior:
    #        y=4:    x=3..9   (chamfered NW (2,4) & NE (10,4) stone tower bevels!)
    #        y=5..8: x=2..10  (full 9-wide octagonal lantern gallery — 360-degree walkable loop around the Great Lamp!)
    #        y=9:    x=3..9   (chamfered SW (2,9) & SE (10,9) stone tower bevels; Warp @ (4,9) sits cleanly inside!)
    #        y=10:   x=4..8   (south panoramic glass/stone watch parapet!)
    #    Wait: check Warp @ (4, 9) and Arrival @ (4, 8): BOTH sit squarely inside the octagonal gallery with generous clearance!
    #    Wait: also expand East & West by 1 tile symmetrically (x=2..12? No, center of 1..11 is 6!):
    #      y=4:    x=2..10
    #      y=5..8: x=1..11
    #      y=9:    x=2..10
    #      y=10:   x=3..9
    #    Let's verify symmetry of that 11-wide Octagon (x=1..11, center x=6!):
    #      - Left margin x=0 (void casing), Right margin x=12 (void casing), Top wall y=2..3 (panoramic glass windows across x=2..10!),
    #      - Top roof rim y=1, Bottom roof rim y=11 -> 100% PERFECT SYMMETRIC OCTAGONAL LIGHTHOUSE TOWER!
    floor = np.zeros((H, W), dtype=bool)
    floor[4, 2:11] = True          # y=4, x=2..10 (width 9, center 6)
    floor[5:9, 1:12] = True        # y=5..8, x=1..11 (width 11, center 6)
    floor[9, 2:11] = True          # y=9, x=2..10 (width 9, center 6) — contains Warp (4, 9) cleanly!
    floor[10, 3:10] = True         # y=10, x=3..9 (width 7, center 6) — south watch gallery!

    # Cool twilight coastal slate stone floor across the outer octagonal gallery
    def slate_floor(x, y, fl):
        top = not fl[y - 1, x]
        bot = y + 1 >= H or not fl[y + 1, x]
        lft = not fl[y, x - 1]
        rgt = x + 1 >= W or not fl[y, x + 1]
        ry = 0 if top else (2 if bot else 1)
        rx = 0 if lft else (2 if rgt else 1)
        return [[1152, 1153, 1154], [1160, 1161, 1162], [1168, 1169, 1170]][ry][rx]

    _seam_stone_room(L, floor, wall_rows=2, base_floor_fn=slate_floor)

    # 2. Concentric Radiant Golden Fresnel Beacon Light Floor (585..603 outer glow + 960..978 ornate gold turntable dais)!
    #    Bathes the central 5x4 beacon dais (x=4..8, y=4..7) in concentric sunlit golden light,
    #    framing Hesper Vane @ (6, 7) and the Great Octagonal Fresnel Lighthouse Beacon @ (5..7, 4..6)!
    GOLD_DAIS = [
        [585, 586, 587],
        [593, 594, 595],
        [601, 602, 603],
    ]
    _put_9slice(L, GOLD_DAIS, 4, 4, 8, 7, z=0)
    GOLD_RING = [
        [960, 961, 962],
        [968, 969, 970],
        [976, 977, 978],
    ]
    _put_grid(L, GOLD_RING, 5, 4, z_rows=(0, 0, 0))

    # Crisp timber stairwell hatch landing right at Warp (4, 9) (with (3..5, 9) timber stair deck)!
    for x in (3, 4, 5):
        L[0, 9, x] = 5361 + (x - 3)
    L[1, 9, 3] = 5512
    L[1, 9, 4] = 5513                      # Crisp visible descending stairwell threshold right at Warp (4, 9)!
    L[1, 9, 5] = 5514
    # Symmetrical warm timber keeper's watch rug on SE side (7..9, 9) balancing the SW stairwell!
    SHER_RUG = [
        [5411, 5412, 5413],
        [5419, 5420, 5421],
        [5427, 5428, 5429],
    ]
    for i, x in enumerate((7, 8, 9)):
        L[1, 8, x] = SHER_RUG[0][i]
        L[1, 9, x] = SHER_RUG[2][i]

    # 3. 360-Degree Panoramic Glass Lighthouse Lantern Wall (y=2..3, x=2..10)!
    #    - Center 3-wide multi-pane lantern glasshouse window (5..7, 2..3) directly behind the Great Beacon!
    _put_grid(L, [[2107, 2108, 2109], [2115, 2116, 2117]], 5, 2, z_rows=(1, 1))
    #    - Flanking 2-wide sunlit coastal sky arched windows (3..4, 2..3) & (8..9, 2..3)!
    _put_grid(L, [[2086, 2087], [2094, 2095]], 3, 2, z_rows=(1, 1))
    _put_grid(L, [[2086, 2087], [2094, 2095]], 8, 2, z_rows=(1, 1))
    #    - Outer lantern sidelights at (2, 2..3) & (10, 2..3) — continuous 9-tile glass lighthouse cupola!
    L[1, 2, 2] = 2105; L[1, 3, 2] = 2113
    L[1, 2, 10] = 2105; L[1, 3, 10] = 2113
    #    - Stepped outer octagonal bay windows on NW (1, 3..4) & NE (11, 3..4)!
    L[1, 3, 1] = 2073; L[1, 4, 1] = 2081
    L[1, 3, 11] = 2073; L[1, 4, 11] = 2081

    # 4. CENTERPIECE: OCTAGONAL CRYSTAL-AND-BRASS FRESNEL LIGHTHOUSE BEACON HOUSING (x=5..7, y=4..6)!
    #    Replaces the grey Pokémon statue with an unmistakable revolving lighthouse lens & flame housing:
    #    - Base turntable: 3x3 Octagonal Stone & Crystal Lens Housing (8139..8157, pas=15) centered dead-on x=6!
    #    - Glowing Beacon Flame Core: Blazing golden lighthouse lantern/brazier (4886 top / 4894 flame bowl) at (6, 4..5)
    #      rising directly from the heart of the crystal Fresnel drum!
    FRESNEL_PLINTH = [
        [8139, 8140, 8141],
        [8147, 8148, 8149],
        [8155, 8156, 8157],
    ]
    _put_grid(L, FRESNEL_PLINTH, 5, 4, z_rows=(1, 1, 1))
    L[2, 4, 6] = 7718                      # Roaring golden beacon flame rising from the brass Fresnel optic!
    L[2, 5, 6] = 2470                      # Gleaming golden-brass trunnioned Fresnel lantern orb at dead center (6, 5)!

    # Flanking warm golden brass Fresnel reflector stands (2247/2255) & brass stanchion guard posts (3958/3966)!
    # (Leaves (3, 4..9), (4, 7..9), (5..7, 7..8), (8, 7..9), (9, 4..9) 100% open walkable 360-degree lantern gallery!)
    L[2, 5, 4] = 2247; L[1, 6, 4] = 2255   # West golden brass reflector lamp stand
    L[2, 5, 8] = 2247; L[1, 6, 8] = 2255   # East golden brass reflector lamp stand
    L[1, 4, 4] = 3966                      # NW brass turntable stanchion post
    L[1, 4, 8] = 3966                      # NE brass turntable stanchion post

    # Subtle coastal watch gallery detail at (2, 8) & (10, 8) instead of outdoor street lamp posts!
    L[1, 8, 2] = 4168
    L[1, 8, 10] = 4077

    # 5. Authentic Keeper's Lamp-Room Gallery Props (100% COMPLETE intact sprites, 360-degree walkable loop!):
    #    - West Gallery (x=1, y=5..8): Keeper's lamp-oil canisters (4822/4830) & spare Fresnel polishing gear crate!
    L[2, 5, 1] = 4822; L[1, 6, 1] = 4830   # tall blue-gold lamp-oil canister
    L[2, 6, 1] = 0
    L[2, 7, 1] = 4823; L[1, 8, 1] = 4831   # second matching lamp-oil canister
    #    - East Gallery (x=11, y=5..8): Keeper's spare wick & oil-bottle shelf + maritime pitch bucket!
    L[2, 5, 11] = 4822; L[1, 6, 11] = 4830
    L[1, 7, 11] = 4168                      # coiled maintenance rope basket
    L[1, 8, 11] = 4101                      # keeper's rag & polishing bucket!
    #    - South Watch Parapet (x=4..9, y=10): keeper's watch stool, tool satchel & coastal fern palm!
    L[1, 10, 6] = 4077                      # keeper's wooden stool facing north toward the Great Beacon
    L[1, 10, 8] = 5580                      # keeper's weathered brass-buckled tool satchel
    L[2, 9, 9] = 5431; L[1, 10, 9] = 5439  # intact coastal lantern-room fern palm on SE corner!
    #    - NW/NE Gallery Balancing Accents (2, 4) [Wireless event!] & (10, 4): keep (2, 4) clear + intact herb pot at (10, 4)
    L[1, 4, 2] = 4077
    L[1, 4, 10] = 3391

    PG.guard(L, TID, [(4, 9), (4, 8), (6, 7), (3, 8), (5, 8), (4, 7)], 'map 106')
    return L


def update_yaml_105_106():
    spec_path = os.path.join(HERE, 'specs', '101_ferrows_landing_interiors.yaml')
    with open(spec_path, 'r', encoding='utf-8') as f:
        text = f.read()

    raw_docs = text.split('\n---\n')
    out_docs = []
    updated = set()
    for i, chunk in enumerate(raw_docs):
        doc = yaml.safe_load(chunk)
        if doc and doc.get('id') in (105, 106):
            mid = doc['id']
            new_doc = {
                'id': mid,
                'name': doc['name'],
                'parent': doc['parent'],
                'biome': doc['biome'],
                'bgm': doc['bgm'],
                'tone': [12, 4, -12, 0] if mid == 105 else [16, 10, -8, 0],
                'metadata': doc['metadata'],
                'raw': f'data/raw/{mid}.npy',
                'tileset': TID,
                'events': doc['events'],
            }
            dumped = yaml.safe_dump(new_doc, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True).rstrip()
            out_docs.append(dumped)
            updated.add(mid)
        else:
            out_docs.append(chunk)

    assert updated == {105, 106}, f'Expected to update 105 & 106, got {updated}'
    with open(spec_path, 'w', encoding='utf-8') as f:
        f.write('\n---\n'.join(out_docs))
        if not out_docs[-1].endswith('\n'):
            f.write('\n')
    print(f'updated Maps 105 & 106 in {spec_path}')


def main():
    os.makedirs(os.path.join(HERE, 'data', 'raw'), exist_ok=True)
    for mid, fn in ((105, build_105_layers), (106, build_106_layers)):
        L = fn()
        out_npy = os.path.join(HERE, 'data', 'raw', f'{mid}.npy')
        np.save(out_npy, L)
        print(f'wrote {out_npy} {L.shape}')
    update_yaml_105_106()


if __name__ == '__main__':
    main()
