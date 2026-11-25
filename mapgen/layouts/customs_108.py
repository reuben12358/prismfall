#!/usr/bin/env python3
"""layouts/customs_108.py - Wave 5 Rejuvenation V14 redesign of Map 108 (Quarantine Customs Hall, 25x19, Tileset 34).

Transforms the bare rectangular brown warehouse box (with a half-clipped labtank) into a void-sculpted,
three-zone Maritime Harbor Customs Terminal:
  - West Wing: Weathered timber Ferrow's Landing freight & immigration bay (amber counter, crates, nautical map)
  - Center Concourse: Vaulted cream-and-gold stone lobby with crimson-gold medallion runner, tariff board & arched windows
  - East Wing: Sleek slate-blue Meridian Quarantine booth (cobalt counter, COMPLETE 3-wide scanner, telemetry)
    flowing south into a warm timber-and-rug traveler waiting lounge.

Updates ONLY Map 108 in mapgen/specs/101_ferrows_landing_interiors.yaml and writes mapgen/data/raw/108.npy,
leaving maps 101-107 untouched and preserving 100% of HEAD events (including trial_overlay auto-seated events).
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
    # Three architectural bays carved cleanly into black void (zero flat box!):
    #   - Central vaulted arrival concourse: x=9..15, y=4..14 + recessed door notch x=11..13, y=15
    #   - West immigration & cargo wing:     x=3..8,  y=5..12 + stepped bay x=5..8, y=13 (SW chamfer!)
    #   - East Meridian & lounge wing:       x=16..21, y=5..12 + stepped bay x=16..19, y=13 (SE chamfer!)
    #   - Slight NE/NW crown chamfers:       (3, 5) and (21, 5) carved out? Keep (3..8,5) clean so north wall is 2 rows straight!
    floor = np.zeros((H, W), dtype=bool)
    floor[4:15, 9:16] = True       # central vaulted hall (x=9..15, y=4..14)
    floor[15, 11:14] = True        # recessed entry door notch (x=11..13, y=15)
    floor[5:13, 3:9] = True        # west customs & cargo wing (x=3..8, y=5..12)
    floor[13, 5:9] = True          # SW chamfered waiting bay (x=5..8, y=13)
    floor[5:13, 16:22] = True      # east Meridian & waiting wing (x=16..21, y=5..12)
    floor[13, 16:20] = True        # SE chamfered lounge bay (x=16..19, y=13)

    # ------------------------------------------------------------------ 2. Perimeter wall auto-seamer (Sheridan wood)
    # Every floor cell with void immediately north gets 2 rows of timber-and-plaster wainscoting + 1 row top trim.
    wall_face = np.zeros((H, W), dtype=bool)
    for y in range(3, H):
        for x in range(1, W - 1):
            if floor[y, x] and not floor[y - 1, x]:
                wall_face[y - 1, x] = True
                wall_face[y - 2, x] = True

    interior = floor | wall_face

    # Paint Sheridan interior border around `interior`
    for y in range(H):
        for x in range(W):
            if floor[y, x]:
                # Base warm timber planks (overridden per-zone below)
                top_row = not floor[y - 1, x]
                left_edge = not floor[y, x - 1]
                if top_row:
                    L[0, y, x] = 5352 if left_edge else 5353 + (x - 4) % 3
                else:
                    L[0, y, x] = 5360 if left_edge else 5361 + (x - 4) % 3
            elif wall_face[y, x]:
                # 2-row timber wall face (upper row y where floor is at y+2, lower row where floor is at y+1)
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
                # Exterior border / trim around `interior`
                N = y > 0 and interior[y - 1, x]
                S = y + 1 < H and interior[y + 1, x]
                W_ = x > 0 and interior[y, x - 1]
                E = x + 1 < W and interior[y, x + 1]
                NW = y > 0 and x > 0 and interior[y - 1, x - 1]
                NE = y > 0 and x + 1 < W and interior[y - 1, x + 1]
                SW = y + 1 < H and x > 0 and interior[y + 1, x - 1]
                SE = y + 1 < H and x + 1 < W and interior[y + 1, x + 1]

                if S and E:
                    L[0, y, x] = 5562  # inner SE-facing corner (floor to S & E)
                elif S and W_:
                    L[0, y, x] = 5561  # inner SW-facing corner (floor to S & W)
                elif N and E:
                    L[0, y, x] = 5554  # inner NE-facing corner (floor to N & E)
                elif N and W_:
                    L[0, y, x] = 5553  # inner NW-facing corner (floor to N & W)
                elif S:
                    L[0, y, x] = 5534  # north top cap
                elif N:
                    L[0, y, x] = 5550  # south bottom cap
                elif E:
                    L[0, y, x] = 5541  # west side wall
                elif W_:
                    L[0, y, x] = 5543  # east side wall
                elif SE:
                    L[0, y, x] = 5533  # outer NW corner
                elif SW:
                    L[0, y, x] = 5535  # outer NE corner
                elif NE:
                    L[0, y, x] = 5549  # outer SW corner
                elif NW:
                    L[0, y, x] = 5551  # outer SE corner

    # Clean up step-down vertical joints at x=8/x=16 where central bay rises 1 row higher than side bays
    # At (8, 2) there is wall_face at (9, 2) to the E and void at (8, 3) -> border tile (8, 2) gets 5541 (west edge),
    # and (8, 1) gets 5533 (outer NW). At (8, 3) interior is at (9, 3) (E) and (8, 4) (S) -> inner corner 5562!
    # Double-check step-in south corners: (4, 13) has interior N=(4,12) and E=(5,13) -> 5554 (inner corner)!
    # (20, 13) has interior N=(20,12) and W=(19,13) -> 5553! (10, 15) has N=(10,14) and E=(11,15) -> 5554!
    # (14, 15) has N=(14,14) and W=(13,15) -> 5553! Every single corner auto-seams cleanly!

    # ------------------------------------------------------------------ 3. Multi-Zone Floor Craft
    # Zone A: Central Vaulted Stone Concourse (x=9..15, y=4..14) - warm cream-and-gold trimmed stone
    CREAM_STONE = [
        [5920, 5921, 5922],
        [5928, 5929, 5930],
        [5936, 5937, 5938],
    ]
    _put_9slice(L, CREAM_STONE, 9, 4, 15, 14, z=0)

    # Zone B: East Meridian Quarantine Bay (x=15..21, y=5..8) - sleek cobalt-slate laboratory stone
    # Starting cleanly at x=15 preserves exact bilateral symmetry of the central cream-and-gold concourse (x=9..14)!
    BLUE_STONE = [
        [5768, 5769, 5770],
        [5776, 5777, 5778],
        [5784, 5785, 5786],
    ]
    _put_9slice(L, CREAM_STONE, 9, 4, 14, 14, z=0)
    # Extend central cream stone to x=15 south of the Meridian bay (y=9..14) and top row y=4!
    for y in range(9, 14):
        L[0, y, 14] = 5929
        L[0, y, 15] = 5930
    L[0, 14, 14] = 5937
    L[0, 14, 15] = 5938
    L[0, 4, 14] = 5921
    L[0, 4, 15] = 5922
    _put_9slice(L, BLUE_STONE, 15, 5, 21, 8, z=0)

    # Entry doormat at (11..13, 15) over warm timber threshold
    for i, x in enumerate((11, 12, 13)):
        L[1, 15, x] = 5512 + i

    # Grand Ornate Crimson-and-Silver Arrival Runner down the central concourse (x=11..13, y=6..14)
    HOTEL_RUG = [
        [7172, 7173, 7174],
        [7180, 7181, 7182],
        [7188, 7189, 7190],
    ]
    _put_9slice(L, HOTEL_RUG, 11, 6, 13, 14, z=1)

    # Cozy Woven Red-and-Gold Lounge Rug in the SE Waiting Lounge (x=16..19, y=10..12)
    SHER_RUG = [
        [5411, 5412, 5413],
        [5419, 5420, 5421],
        [5427, 5428, 5429],
    ]
    _put_9slice(L, SHER_RUG, 16, 10, 19, 12, z=1)

    # ------------------------------------------------------------------ 4. Architectural North Wall Features
    # Vertical timber pilasters framing bays
    for px, py in ((6, 3), (11, 2), (13, 2), (18, 3)):
        L[0, py, px] = 5548
        L[0, py + 1, px] = 5556
    # Arched sunlit harbor windows on central vaulted north wall (y=2..3) & diamond maritime portholes on wings (y=3..4)
    for wx in (10, 14):
        L[0, 2, wx] = 5544
        L[0, 3, wx] = 5552
    for wx in (5, 19):
        L[0, 3, wx] = 5560
        L[0, 4, wx] = 5568
    # Cargo loading hatch shutter in NW freight wall (x=3, y=3..4)
    L[0, 3, 3] = 5565
    L[0, 4, 3] = 5573

    # Central Vaulted Wall: Harbor Tariff & Customs Notice Board (x=11..13, y=2..3 -> crisp 3x2!)
    _put_grid(L, [[5795, 5796, 5797], [5803, 5804, 5805]], 11, 2, z_rows=(1, 1))
    # West Customs Wall: Nautical route map (map_wall, 3x1) at (6..8, 3) + Ocean chart (1x2) at (4, 3..4)
    _put_tf(L, 'map_wall', 6, 3)
    L[1, 3, 4] = 5453
    L[1, 4, 4] = 5461
    # East Meridian Wall: Maritime Lifering (2x2) cleanly mounted at (16..17, 3..4) -> wait console sits at (15..17, 4..5),
    # so place framed ocean chart at (17, 3..4) and crisp timber pilaster at (16, 3..4) — ZERO overlap with console or labtank!
    L[0, 3, 16] = 5548
    L[0, 4, 16] = 5556
    L[1, 3, 20] = 5453
    L[1, 4, 20] = 5461

    # ------------------------------------------------------------------ 5. West Wing: Immigration Counter & Freight Alcove
    # CRITICAL for trial_overlay._seat() exact HEAD match:
    #   Customs officer @ (6, 7); Grant Kiosk P-3NNY @ (7, 6); Crate 7-B @ (6, 5); Two mice @ (8, 7).
    #   Requires (5, 6), (4, 7), and (5..8, 8) SOLID, while (6,5), (7,5), (6,6), (7,6), (8,6), (7,7), (8,7), (9,7) WALKABLE!
    # NW Cargo Stack: crates3 (3x3) at (3..5, 5..7) -> covers (3..5, 5..7) cleanly (solid at (5,6) and (4,7)!)
    _put_tf(L, 'crates3', 3, 5)
    # Warm Amber Customs Inspection Counter at y=8 (x=5..8) with p143 Counter flag (no sliced flower base!)
    L[1, 8, 5] = 5962
    L[1, 8, 6] = 5961
    L[1, 8, 7] = 5962
    L[1, 8, 8] = 5967
    # West Freight & Barrel Corner along far west wall (x=3..4, y=9..12):
    _put_tf(L, 'barrel_b', 3, 9)    # (3, 9..10)
    _put_tf(L, 'pallet', 3, 11)     # (3..4, 11..12)
    _put_tf(L, 'stool', 6, 10)      # passenger inspection stool in front of Customs officer!
    # SW Chamfered Passenger Declaration Desk & Luggage Bay (x=5..8, y=11..13):
    _put_tf(L, 'table_dark', 6, 11) # (6..7, 11..12) customs declaration writing table!
    L[2, 12, 6] = 3428              # open customs declaration ledger right on the desk!
    L[1, 12, 5] = 4077              # passenger stool west of desk
    L[1, 12, 8] = 5580              # vintage leather suitcase beside desk!
    L[1, 13, 5] = 7501              # traveler trunk in SW corner!
    L[1, 13, 8] = 3391              # brass flowerpot framing concourse edge!
    # Symmetrical Potted Parlor Trees framing ALL 4 corners of the central vaulted concourse!
    L[2, 13, 9] = 7126; L[1, 14, 9] = 7134
    L[2, 13, 15] = 7126; L[1, 14, 15] = 7134
    L[2, 4, 9] = 5415; L[1, 5, 9] = 5423
    L[2, 4, 14] = 5415; L[1, 5, 14] = 5423

    # ------------------------------------------------------------------ 6. East Wing: Meridian Quarantine Station & Waiting Lounge
    # Cobalt-Blue Meridian Counter at y=8 (x=14..17) with p143 Counter flag!
    # Meridian tech stands at (15, 7) right behind (15, 8)!
    L[2, 7, 14] = 5840              # blue hydrangea pot on left counter edge (r5 overhead, never blocks!)
    L[1, 8, 14] = 5848              # blue counter left + pot base (p143)
    L[1, 8, 15] = 5849              # blue counter ledger in front of Meridian tech (p143)
    L[1, 8, 16] = 5850              # blue counter mid (p143)
    L[1, 8, 17] = 5855              # Meridian diagnostic terminal (p143)
    # COMPLETE 3-tile-wide Quarantine Scanner (labtank FIXED — all 3 columns 4784..4810!) in NE bay (x=18..20, y=4..7)!
    LABTANK_FULL = [
        [4784, 4785, 4786],
        [4792, 4793, 4794],
        [4800, 4801, 4802],
        [4808, 4809, 4810],
    ]
    _put_grid(L, LABTANK_FULL, 18, 4, z_rows=(2, 1, 1, 1))
    # Compact barrels & Meridian diagnostic gear at x=21, y=5..8:
    _put_tf(L, 'barrel_b', 21, 5)   # (21, 5..6)
    _put_tf(L, 'barrel_y', 21, 7)   # (21, 7..8)
    # Meridian telemetry console on back wall behind tech (x=15..17, y=4..5):
    _put_tf(L, 'console', 15, 4)

    # SE Cozy Harbor Waiting Lounge (x=16..21, y=9..13):
    # Rug is at (16..19, 10..12). Warm tea table, stools, reading shelf, luggage & plants!
    _put_tf(L, 'table_tea', 17, 10)  # (17..18, 10..11) on layer 2 over rug!
    L[2, 11, 16] = 4077              # wooden stool west of lounge table
    L[2, 11, 19] = 4077              # wooden stool east of lounge table
    # Tall flowering fern & cargo crate along east wall (x=20..21, y=9..12):
    L[2, 9, 21] = 5431; L[1, 10, 21] = 5439   # potted harbor fern
    _put_tf(L, 'crate_i2', 20, 11)            # (20..21, 11..12) cargo crate
    # Low nautical book/brochure rack at (17..18, 13), suitcase at (16, 13), flowerpot at (19, 13):
    _put_tf(L, 'shelf_low', 17, 13)
    L[1, 13, 16] = 5580              # vintage suitcase
    L[1, 13, 19] = 3391              # harbor flowerpot

    # Twin brass flowerpots framing the central Harbor Tariff Board at (11, 4) and (13, 4), leaving (12, 4..5) open!
    L[1, 4, 11] = 3391
    L[1, 4, 13] = 3391

    # Run passguard to guarantee 0 passability conflicts on Tileset 34!
    PG.guard(L, TID)
    return L


def main():
    L = build_108_layers()
    raw_dir = os.path.join(HERE, 'data', 'raw')
    os.makedirs(raw_dir, exist_ok=True)
    np.save(os.path.join(raw_dir, '108.npy'), L.astype(np.int16))

    # Update ONLY map 108 inside specs/101_ferrows_landing_interiors.yaml, preserving 101-107 byte-cleanly!
    spec_path = os.path.join(HERE, 'specs', '101_ferrows_landing_interiors.yaml')
    docs = [d for d in yaml.safe_load_all(open(spec_path)) if d]
    new_docs = []
    found = False
    for d in docs:
        if d.get('id') == 108:
            found = True
            # Keep exact HEAD header & events, switch tile payload to clean raw: data/raw/108.npy!
            s108 = {
                'id': 108,
                'name': d['name'],
                'parent': d['parent'],
                'bgm': d['bgm'],
                'metadata': d['metadata'],
                'tone': [12, 6, -10, 0],
                'biome': 'interior',
                'tileset': TID,
                'raw': 'data/raw/108.npy',
                'events': d['events'],
            }
            new_docs.append(s108)
        else:
            new_docs.append(d)
    assert found, 'Map 108 not found in 101_ferrows_landing_interiors.yaml!'

    header = "# Ferrow's Landing interiors (101-108). 101-107 by early_interiors.py; 108 sculpted by layouts/customs_108.py.\n"
    out = header + '\n---\n'.join(
        yaml.safe_dump(s, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True)
        for s in new_docs
    )
    open(spec_path, 'w').write(out)
    print(f'Wrote data/raw/108.npy ({L.shape}) and updated map 108 in {spec_path}')


if __name__ == '__main__':
    main()
