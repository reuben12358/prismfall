#!/usr/bin/env python3
"""layouts/customs_108.py - Ch0 Opening Rethink (Pass 2) of Map 108 (Quarantine Customs Hall, 25x19, Tileset 34).

A grounded, bilaterally symmetrical Gen 5 / Rejuvenation Maritime Customs Immigration Terminal:
  - Central Concourse (x=10..14, y=4..14): Vaulted cream-and-gold marble concourse centered
    symmetrically on x=12, framing the 3-tile crimson-gold runner (x=11..13), arched harbor
    windows (x=10, 14), maritime tariff notice board (x=11..13), and 4 symmetrical parlor trees
    at (10,5), (14,5), (10,14), (14,14).
  - West Wing (Immigration & Baggage Bay, x=3..9): Mirror-symmetrical 5-tile polished mahogany
    customs counter (x=5..9, y=8, ALL 0x8f counter flags + pri=5 top rims) strictly on timber
    flooring for Customs officer (6,7), NW cargo crates preserving exact trial_overlay seating
    (Grant Kiosk P-3NNY (7,6), Crate 7-B (6,5), Two mice (8,7)), enclosed brass bellhop luggage
    cart (3..4, 8..10), baggage inspection table with open declaration ledger squarely on top
    (6,11), and pure-solid leather trunks (7501).
  - East Wing (Meridian Quarantine Inspection & Arrivals Lounge, x=15..21): Exact mirror 5-tile
    polished mahogany customs counter (x=15..19, y=8, ALL 0x8f counter flags + pri=5 top rims)
    strictly on timber flooring for Meridian tech (15,7) & Calla (16,7), cleanly framed wall
    telemetry panel & compact desktop Imprint-Scanner workstation, tall oak manifest archive
    bookcases, and a cozy SE Arrivals Waiting Alcove with framed rug, steaming tea table,
    matching warm mahogany bookcase (20..21, 10..11), low reading rack, and parlor fern.

Writes ONLY mapgen/data/raw/108.npy (101_ferrows_landing_interiors.yaml already references
raw: data/raw/108.npy on tileset 34 and preserves 100% of all events).
"""
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import passguard as PG
from interiorkit import TF

TID = 34
VOID = 5437
W, H = 25, 19


def _put_tf(L, name, x, y, solid_base=False):
    """Stamp a Tectonic Inside piece from interiorkit.TF onto L (3, H, W)."""
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
    """Stamp a 2D list of tile IDs at (x, y); optional per-row layer tuple."""
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
    """Paint a 3x3 9-slice block across [x0..x1] x [y0..y1]."""
    for y in range(y0, y1 + 1):
        ry = 0 if y == y0 else (2 if y == y1 else 1)
        for x in range(x0, x1 + 1):
            rx = 0 if x == x0 else (2 if x == x1 else 1)
            L[z, y, x] = tiles9[ry][rx]


def build_108_layers():
    L = np.zeros((3, H, W), dtype=np.int32)
    L[0, :, :] = VOID

    # ------------------------------------------------------------------ 1. Void-sculpted floor mask
    # Bilaterally symmetrical three-bay Maritime Customs Hall centered cleanly on x=12:
    #   - Central vaulted arrival concourse: x=10..14, y=4..14 + recessed door notch x=11..13, y=15
    #   - West immigration & baggage bay:    x=3..9,   y=5..12 + SW chamfered bay x=5..9,  y=13
    #   - East quarantine & waiting wing:    x=15..21, y=5..12 + SE chamfered bay x=15..19, y=13
    floor = np.zeros((H, W), dtype=bool)
    floor[4:15, 10:15] = True      # central vaulted hall (x=10..14, y=4..14)
    floor[15, 11:14] = True        # recessed entry door notch (x=11..13, y=15)
    floor[5:13, 3:10] = True       # west customs & baggage wing (x=3..9, y=5..12)
    floor[13, 5:10] = True         # SW chamfered baggage bay (x=5..9, y=13)
    floor[5:13, 15:22] = True      # east Meridian & arrivals wing (x=15..21, y=5..12)
    floor[13, 15:20] = True        # SE chamfered lounge bay (x=15..19, y=13)

    # ------------------------------------------------------------------ 2. Perimeter wall auto-seamer (Sheridan timber)
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

    # ------------------------------------------------------------------ 3. Unified Multi-Zone Maritime Flooring
    # Central Vaulted Arrival Concourse (x=10..14, y=4..14) - exact bilateral symmetry centered on x=12!
    CREAM_STONE = [
        [5920, 5921, 5922],
        [5928, 5929, 5930],
        [5936, 5937, 5938],
    ]
    _put_9slice(L, CREAM_STONE, 10, 4, 14, 14, z=0)

    # Entry doormat at (11..13, 15) over warm timber threshold
    for i, x in enumerate((11, 12, 13)):
        L[1, 15, x] = 5512 + i

    # Grand Crimson-and-Gold Arrival Runner down the central concourse (x=11..13, y=6..14)
    HOTEL_RUG = [
        [7172, 7173, 7174],
        [7180, 7181, 7182],
        [7188, 7189, 7190],
    ]
    _put_9slice(L, HOTEL_RUG, 11, 6, 13, 14, z=1)

    # Cozy Woven Red-and-Gold Lounge Rug in SE Arrivals Waiting Alcove (x=16..19, y=10..12)
    SHER_RUG = [
        [5411, 5412, 5413],
        [5419, 5420, 5421],
        [5427, 5428, 5429],
    ]
    _put_9slice(L, SHER_RUG, 16, 10, 19, 12, z=1)

    # ------------------------------------------------------------------ 4. Architectural North Wall Features
    # Clean symmetrical timber pilasters strictly on bare wall bays (ZERO pilasters clipped behind console/map!)
    for px, py in ((9, 3), (15, 3)):
        L[0, py, px] = 5548
        L[0, py + 1, px] = 5556
    # Arched sunlit harbor windows on central vaulted north wall (x=10, 14; y=2..3) & maritime diamond portholes on wings (x=5, 19; y=3..4)
    for wx in (10, 14):
        L[0, 2, wx] = 5544
        L[0, 3, wx] = 5552
    for wx in (5, 19):
        L[0, 3, wx] = 5560
        L[0, 4, wx] = 5568
    # Freight shutter in far NW wall (x=3, y=3..4)
    L[0, 3, 3] = 5565
    L[0, 4, 3] = 5573

    # Central Vaulted Wall: Harbor Tariff & Immigration Notice Board (x=11..13, y=2..3)
    _put_grid(L, [[5795, 5796, 5797], [5803, 5804, 5805]], 11, 2, z_rows=(1, 1))
    # West Customs Wall: Velmora Nautical Route Map (6..8, 3) + Framed Coastal Chart (4, 3..4)
    _put_tf(L, 'map_wall', 6, 3)
    L[1, 3, 4] = 5453
    L[1, 4, 4] = 5461
    # East Quarantine Wall: Framed Coastal Chart (20, 3..4) — clean paneling behind console (16..18, 3..4)!
    L[1, 3, 20] = 5453
    L[1, 4, 20] = 5461

    # Symmetrical Potted Parlor Trees framing ALL 4 corners of the x=10..14 central vaulted concourse!
    L[2, 13, 10] = 7126; L[1, 14, 10] = 7134
    L[2, 13, 14] = 7126; L[1, 14, 14] = 7134
    L[2, 4, 10] = 5415; L[1, 5, 10] = 5423
    L[2, 4, 14] = 5415; L[1, 5, 14] = 5423
    # Twin brass flowerpots framing the central Harbor Tariff Notice Board (11,4) & (13,4)
    L[1, 4, 11] = 3391
    L[1, 4, 13] = 3391

    # ------------------------------------------------------------------ 5. West Wing: Immigration Counter & Baggage Bay
    # Exact trial_overlay._seat() contract around Customs officer (6, 7):
    #   Grant Kiosk P-3NNY @ (7, 6); Crate 7-B @ (6, 5); Two mice @ (8, 7).
    #   Requires (5, 6), (4, 7), and (5..8, 8) SOLID, while (6..8, 5..6) and (7..9, 7) WALKABLE!
    _put_tf(L, 'crates3', 3, 5)  # Neat NW maritime cargo stack (3..5, 5..7)

    # Mirror-Symmetrical 5-tile Polished Mahogany West Customs Counter strictly on timber wing (x=5..9, y=8, ALL 0x8f!)
    # Rounded left end (5668), open customs ledger directly in front of officer (5664),
    # smooth mahogany middle (5665, 5665), and rounded right end (5667)!
    L[1, 8, 5] = 5668; L[2, 7, 5] = 5660
    L[1, 8, 6] = 5664; L[2, 7, 6] = 5656
    L[1, 8, 7] = 5665; L[2, 7, 7] = 5657
    L[1, 8, 8] = 5665; L[2, 7, 8] = 5657
    L[1, 8, 9] = 5667; L[2, 7, 9] = 5659

    # West Baggage Inspection Bay (x=3..9, y=8..13) — ZERO industrial oil drums!
    # Complete 2x3 Brass Bellhop Luggage Cart nestled at (3..4, 8..10): its pri=5 top arch (3..4, 8) is
    # 100% enclosed on all 4 sides by crates3 (3..4, 7), west wall (2, 8), counter (5, 8) & cart body (3..4, 9)!
    _put_grid(L, [[7476, 7477], [7486, 7487], [7494, 7495]], 3, 8, z_rows=(2, 1, 1))
    # Potted parlor fern cleanly framing SW west-wall corner (3, 11..12)
    L[2, 11, 3] = 5431; L[1, 12, 3] = 5439
    # Wooden baggage inspection table (6..7, 11..12): tabletop on L[1, 11, 6..7] so open declaration book
    # (3428) sits SQUARELY ON TOP of the table at L[2, 11, 6] (NEVER floating on the floor)!
    L[1, 11, 6] = 3408; L[1, 11, 7] = 3409
    L[1, 12, 6] = 3416; L[1, 12, 7] = 3417
    L[2, 11, 6] = 3428   # open red-bound customs declaration ledger squarely on tabletop!
    L[1, 12, 5] = 4077   # passenger stool west of declaration table
    L[1, 12, 8] = 7501   # pure-solid vintage leather suitcase (0x0f) beside declaration table
    L[1, 13, 5] = 7501   # pure-solid traveler sea trunk in SW chamfer
    L[1, 13, 8] = 3391   # brass flowerpot framing SW chamfer cleanly

    # ------------------------------------------------------------------ 6. East Wing: Meridian Quarantine Desk & Arrivals Lounge
    # Exact Mirror-Symmetrical 5-tile Polished Mahogany Quarantine Counter strictly on timber wing (x=15..19, y=8, ALL 0x8f!)
    # Meridian tech stands at (15, 7) & Calla stands at (16, 7) strictly on warm timber floor behind 0x80 counter;
    # open staff aisles at (14, 7..8) & (20, 7..8) for 100% 4-bit BFS reachability!
    L[1, 8, 15] = 5668; L[2, 7, 15] = 5660
    L[1, 8, 16] = 5664; L[2, 7, 16] = 5656
    L[1, 8, 17] = 5665; L[2, 7, 17] = 5657
    L[1, 8, 18] = 5665; L[2, 7, 18] = 5657
    L[1, 8, 19] = 5667; L[2, 7, 19] = 5659

    # Compact Official Meridian Imprint-Scanner Desk & Telemetry Back-Office (x=16..21, y=4..7)
    # 1) Compact Meridian Registry Telemetry Panel flush on clean north timber wall (x=16..18, y=4..5)
    _put_tf(L, 'console', 16, 4)
    # 2) Sleek Compact Desktop Imprint Scanner Workstation cleanly below north wall chart (x=19..20, y=5..6)
    _put_grid(L, [[2792, 2793], [2800, 2801]], 19, 5, z_rows=(2, 1))
    # 3) Slim Oak Customs Manifest Archive Shelf in NE corner (x=21, y=4..5)
    _put_tf(L, 'bookshelf_s', 21, 4)
    # 4) Potted harbor fern framing the SE waiting entrance (x=21, y=8..9)
    L[2, 8, 21] = 5431; L[1, 9, 21] = 5439

    # SE Cozy Arrivals Waiting Alcove (x=16..21, y=10..13)
    # Warm tea/coffee station on woven crimson-gold rug (17..18, 10..11) + twin wooden stools
    _put_tf(L, 'table_tea', 17, 10)
    L[2, 11, 16] = 4077
    L[2, 11, 19] = 4077
    # Warm Dark-Oak Customs & Travel Archive Bookcase along east wall (20..21, 10..11) — ALL 4 tiles solid 0x0f!
    # Replaces stark white/cyan supermarket rack & leaves (20..21, 12) clean breathing room!
    _put_grid(L, [[3309, 3310], [3317, 3318]], 20, 10, z_rows=(1, 1))
    # Low maritime reading & manifest rack (17..18, 13), pure-solid suitcase (16, 13), brass flowerpot (19, 13)
    _put_tf(L, 'shelf_low', 17, 13)
    L[1, 13, 16] = 7501
    L[1, 13, 19] = 3391

    # Run passguard to guarantee 0 passability conflicts on Tileset 34!
    PG.guard(L, TID)
    return L


def main():
    L = build_108_layers()
    raw_dir = os.path.join(HERE, 'data', 'raw')
    os.makedirs(raw_dir, exist_ok=True)
    out_path = os.path.join(raw_dir, '108.npy')
    np.save(out_path, L.astype(np.int16))
    print(f'Wrote {out_path} ({L.shape})')


if __name__ == '__main__':
    main()

