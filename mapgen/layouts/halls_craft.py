#!/usr/bin/env python3
"""layouts/halls_craft.py - Rejuvenation V14 Mapcraft sculpts for Tileset 54 Gym Halls:
  131 Loomhouse Gym - The Canopy  (Sculpted Treetop Canopy Pavilion, 25x35)
  154 Pell Playhouse - Auditorium (Sculpted Art-Deco Opera House, 25x30)

Writes mapgen/data/raw/131.npy and mapgen/data/raw/154.npy cleanly while preserving 100% of
specs/130_loomhouse_gym.yaml & specs/150_pell_playhouse.yaml events, warps, and puzzle proofs.

    PRISMFALL_GFX=/home/antigravity/pf_engine_run/game/Graphics python3 -I mapgen/layouts/halls_craft.py [131] [154]"""
import os, sys, random
import numpy as np

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hallkit as K
from puzzles import canopy as C
from puzzles import playhouse as P

CU, MI, MG, NM, CH, PF = K.CU, K.MI, K.MG, K.NM, K.CH, K.PF


def put_mi_rug(h, x0, y0, x1, y1, z=1):
    """9-slice woven crimson-and-gold Briarwick silk tapestry carpet (MI 1040..1058, pas=0, pri=0)."""
    for y in range(y0, y1 + 1):
        r = 0 if y == y0 else (2 if y == y1 else 1)
        for x in range(x0, x1 + 1):
            c = 0 if x == x0 else (2 if x == x1 else 1)
            if y0 == y1:
                t = MI(1041) if x0 < x < x1 else MI(1040 if x == x0 else 1042)
            elif x0 == x1:
                t = MI(1049)
            else:
                t = MI([[1040, 1041, 1042], [1048, 1049, 1050], [1056, 1057, 1058]][r][c])
            h.put(t, x, y, z)


def put_deco_frame(h, x0, y0, x1, y1, z=1):
    """Walkable Art-Deco gold-filigree promenade frame (NM 1560..1578, pas=0, pri=0)."""
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if y0 == y1:
                t = NM(1560 if x == x0 else 1562 if x == x1 else 1561)
            else:
                r = 0 if y == y0 else (2 if y == y1 else 1)
                c = 0 if x == x0 else (2 if x == x1 else 1)
                t = NM([[1560, 1561, 1562], [1568, 1569, 1570], [1576, 1577, 1578]][r][c])
            if h.L[z, y, x] == 0:
                h.put(t, x, y, z)


def canopy_sunbeam(h, x0, y0, y1, rows):
    """Diagonal warm canopy sunlight shaft (uses pas=0 light_* on walkable tiles, pas=15 light_*_x on pits!)."""
    for y in range(y0, y1 + 1):
        c = x0 + (y - y0)
        for dx, k in ((0, 'l'), (1, 'full'), (2, 'r')):
            x = c + dx
            if not (1 <= x < h.W - 1) or not (1 <= y < h.H - 1):
                continue
            ch = rows[y][x]
            if ch in 'vwsABC':
                if h.L[1, y, x] == 0 and h.L[2, y, x] == 0:
                    h.put(CU('light_%s_x' % k), x, y, 1)
            elif ch in '.S' and h.L[2, y, x] == 0 and h.L[1, y, x] == 0:
                h.put(CU('light_' + k), x, y, 2)


# ============================================================================================ 131 The Canopy
def build_131(save=True):
    CLS = {'#': 'void', 'W': 'wall', '.': 'floor', 'v': 'pit', 'S': 'stair', 'o': 'floor',
           'J': 'floor', 'w': 'pit', 's': 'pit', 'A': 'pit', 'B': 'pit', 'C': 'pit'}
    rows = C.HALL
    h = K.Hall(rows, 'loom', CLS, seed=131)
    rnd = h.r

    BARK = [CU('bark_%d' % t) for t in (18044, 18045, 18046, 18047)]
    BARK_HI = [CU('bark_%d' % t) for t in (18036, 18037, 18038, 18039)]
    BARK_DIM = [CU('bark_dim_%d' % t) for t in (18044, 18045, 18046, 18047)]
    BARK_LO = [CU('bark_%d' % t) for t in (18052, 18053, 18054, 18055)]

    # ---- 1. Organic Living Elder-Tree Hollow Silhouette (Void-Sculpted Bark Buttresses Overhanging the Abyss!) ----
    # Solid living-bark ribs curving organically inward on non-puzzle outer flanks (zero puzzle/trainer impact!)
    bark_buttresses = (
        # Sculpted hollow-trunk waist bulges inside the abyssal drops (between decks, well clear of webs & moths)
        {(1, y) for y in range(12, 17)} | {(2, y) for y in (13, 14, 15)} | {(23, y) for y in range(12, 17)} | {(22, y) for y in (13, 14, 15)}
        | {(1, y) for y in range(19, 24)} | {(2, y) for y in (20, 21, 22)} | {(23, y) for y in range(19, 24)} | {(22, y) for y in (20, 21)}
        | {(1, y) for y in range(26, 29)} | {(2, y) for y in (27, 28)} | {(23, y) for y in range(26, 29)} | {(22, y) for y in (27, 28)}
        # Sculpted living-bark deck-edge corner chamfers (strictly avoiding all NPCs, webs, Joltiks & landings!)
        | {(1, 32), (1, 33), (2, 33), (3, 33), (1, 25), (2, 25), (1, 24), (23, 25),
           (1, 18), (2, 18), (1, 17), (23, 18), (1, 11), (23, 11), (23, 7)}
    )

    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch == '#':
                h.put(CU('hollow_0_%d' % rnd.randrange(3)), x, y, 0)
            if ch == 'W':
                h.put(rnd.choice(BARK_HI if y < 2 else BARK if y < 3 else BARK_LO), x, y, 0)
            if ch in 'vwsABC':
                k = 0
                while y - k - 1 >= 0 and rows[y - k - 1][x] in 'vwsABC':
                    k += 1
                above = rows[y - k - 1][x] if y - k - 1 >= 0 else '#'
                if (x, y) in bark_buttresses and ch == 'v':
                    # Organic curved living-bark tree-trunk wall protruding into the canopy hollow!
                    inner = (x in (2, 22))
                    h.put(rnd.choice(BARK_DIM if inner else BARK), x, y, 0)
                    h.put(0, x, y, 1); h.put(0, x, y, 2)
                    continue
                if k == 0 and above in '.J':
                    # Curved sky-bridge timber fascia with endcaps beside bark buttresses or open ends!
                    l_end = (x <= 1 or rows[y - 1][x - 1] not in '.J' or (x - 1, y - 1) in bark_buttresses)
                    r_end = (x >= h.W - 2 or rows[y - 1][x + 1] not in '.J' or (x + 1, y - 1) in bark_buttresses)
                    t = 'ledge_face_l' if l_end else ('ledge_face_r' if r_end else 'ledge_face_mid')
                    h.put(CU(t), x, y, 0)
                elif x in (1, 23) and ch == 'v':
                    h.put(rnd.choice(BARK_DIM), x, y, 0)
                else:
                    h.put(CU('hollow_%d_%d' % (min(2, max(0, k - 1)), rnd.randrange(3))), x, y, 0)
                h.put(0, x, y, 1); h.put(0, x, y, 2)
                if ch == 'v' and k > 0 and 2 < x < 22 and rnd.random() < 0.11 and all(rows[y][x + dx] == 'v' for dx in (-1, 1)):
                    h.put(CU('root_%d' % rnd.randrange(4)), x, y, 1)
            if ch in '.J':
                if (x, y) in bark_buttresses:
                    # Solid curved bark buttress framing the outer edge of the timber catwalk!
                    h.put(rnd.choice(BARK), x, y, 0)
                    h.put(0, x, y, 1); h.put(0, x, y, 2)
                else:
                    # Warm timber decking with subtle parquet inlays along the central catwalk spine
                    if y in (5, 6, 10, 17, 24, 30, 31) and (x + y) % 5 == 0 and 4 <= x <= 20:
                        h.put(MI(1224), x, y, 0)
                    else:
                        h.put(rnd.choice([MI(1241), MI(1242), MI(1243)]), x, y, 0)

    # ---- 2. Structural Timber Pier Supports Anchoring Every Sky-Bridge into the Elder Hollow ----
    for px, y0, y1 in (
        (6, 27, 28), (18, 27, 28),
        (7, 20, 23), (14, 20, 23), (21, 20, 23),
        (4, 13, 16), (17, 13, 16), (21, 13, 16),
        (16, 8, 9), (21, 8, 9),
    ):
        for yy in range(y0, y1 + 1):
            if rows[yy][px] == 'v' and (px, yy) not in bark_buttresses and (px, yy) not in C.WEBS:
                part = 'tpost_base' if yy == y1 else ('tpost_band' if yy == y0 else 'tpost_mid')
                h.put(CU(part), px, yy, 1)

    # ---- 3. Woven Briarwick Crimson-Gold Silk Tapestry Runners Guiding the Player Up the Canopy ----
    # Entrance foyer royal carpet leading eyes straight from Down-stairs (12,34) to Teach Web (12,28)!
    put_mi_rug(h, 11, 29, 13, 33, z=1)
    # Ledge 1 silk runner guiding eyes from landing (12,25) east to chain-web launch (18,24)!
    for x in range(12, 19):
        h.put(MI(1040 if x == 12 else 1042 if x == 18 else 1041), x, 24, 1)
        h.put(MI(1056 if x == 12 else 1058 if x == 18 else 1057), x, 25, 1)
    # Ledge 2 silk runner guiding eyes from landing (18,17) west to TWIST launch (6,17)!
    for x in range(6, 19):
        h.put(MI(1040 if x == 6 else 1042 if x == 18 else 1041), x, 17, 1)
        h.put(MI(1056 if x == 6 else 1058 if x == 18 else 1057), x, 18, 1)
    # Ledge 3 silk runner connecting West Perch launch (2,10), COMBINE launch (12,10) & Joltik 1 (16,10)!
    for x in range(3, 16):
        h.put(MI(1040 if x == 3 else 1042 if x == 15 else 1041), x, 10, 1)
        h.put(MI(1056 if x == 3 else 1058 if x == 15 else 1057), x, 11, 1)
    # Tamsin's Elevated Canopy Pavilion grand woven tapestry sanctuary (16..21, 4..7)!
    put_mi_rug(h, 16, 4, 21, 7, z=1)

    # ---- 4. Web Guy-Lines, High Bark Knot-Hole Windows & Glowing Joltik Circuit Strands (100% Preserved!) ----
    for (x, y), ch in C.WEBS.items():
        if rows[y][x - 1] == 'v' and (x - 1, y) not in bark_buttresses:
            h.put(CU('web_anchor_l'), x - 1, y, 1)
        if rows[y][x + 1] == 'v' and (x + 1, y) not in bark_buttresses:
            h.put(CU('web_anchor_r'), x + 1, y, 1)
    for part, (dx, dy) in (('tl', (0, 0)), ('tr', (1, 0)), ('bl', (0, 1)), ('br', (1, 1))):
        for x0 in (5, 11, 16):
            h.put(CU('knot_hole_' + part), x0 + dx, 1 + dy, 1)
    h.obj('web', 1, 1); h.obj('web', 21, 1); h.obj('web', 15, 1)
    # Gold & Blue Joltik power strands (exact puzzle cue lines!)
    for x in (13, 14, 15): h.put(CU('thread_gold_h'), x, 9, 2)
    for y in (7, 8): h.put(CU('thread_gold_v'), 12, y, 2)
    h.put(CU('thread_blue_ne'), 1, 4, 2)
    for x in range(2, 12): h.put(CU('thread_blue_h'), x, 4, 2)
    h.put(CU('thread_blue_sw'), 12, 4, 2); h.put(CU('thread_blue_v'), 12, 5, 2)
    h.put(CU('thread_blue_sw'), 13, 4, 2); h.put(CU('thread_blue_v'), 13, 5, 2)
    h.put(CU('thread_blue_h'), 12, 4, 2)

    # ---- 5. Hanging Silk Cocoons, Dyed Silk Skeins & Lush Moss/Foliage Clusters Framing Every Tier ----
    for x, y in ((3, 14), (19, 13), (20, 21), (3, 21), (8, 27), (17, 27), (22, 8), (8, 8)):
        if rows[y][x] == 'v' and rows[y + 1][x] == 'v' and (x, y) not in bark_buttresses and (x, y + 1) not in bark_buttresses:
            h.put(CU('cocoon_top'), x, y, 1); h.put(CU('cocoon_bot'), x, y + 1, 1)
    for x, y, c in ((4, 12, 'p'), (15, 12, 'w'), (19, 19, 'p'), (9, 19, 'w'), (3, 26, 'p'), (21, 26, 'w'), (19, 8, 'p'), (8, 4, 'w')):
        if rows[y][x] == 'v' and rows[y + 1][x] == 'v' and (x, y) not in C.WEBS and (x, y + 1) not in C.WEBS and (x, y) not in bark_buttresses:
            h.put(CU('strand_%s_top' % c), x, y, 1); h.put(CU('strand_%s_bot' % c), x, y + 1, 1)
    h.put(CU('cocoon_top'), 23, 4, 1); h.put(CU('cocoon_bot'), 23, 5, 1)

    # Weaver's craft stations, dye vats, silk bales & warm hanging lanterns
    h.obj('silk1', 15, 7); h.obj('lantern', 15, 4)
    h.stamp('hb_dyeline', 1, 29); h.stamp('hb_rugline', 20, 29)
    h.obj('lantern', 6, 30); h.obj('lantern', 18, 30); h.obj('lantern', 3, 22); h.obj('lantern', 22, 15)
    h.obj('lantern', 19, 8) if False else None
    h.obj('silk1', 23, 17); h.obj('silk', 2, 24); h.obj('silk1', 23, 10); h.obj('vat_y', 22, 24); h.obj('vat_r', 23, 24)
    h.obj('mat_mi', 11, 34)

    # Lush canopy foliage clusters, potted woodland ferns & mossy planters framing every sky-bridge!
    # Keep 100% clear of all puzzle landings, webs, trainers, NPCs & Joltiks!
    ferns = [
        (8, 31), (16, 31), (4, 32), (20, 32),         # entrance foyer canopy garden framing
        (8, 25), (15, 25), (20, 25),                  # ledge 1 woodland accents
        (11, 18), (15, 18), (3, 18),                  # ledge 2 woodland accents
        (19, 11), (20, 10),                           # ledge 3 east mossy nook
        (22, 4), (15, 5),                             # Tamsin's canopy pavilion sanctuary
    ]
    for fx, fy in ferns:
        if rows[fy][fx] == '.' and (fx, fy) not in bark_buttresses:
            h.put(MI(2618 if (fx + fy) % 2 == 0 else 584), fx, fy - 1, 2)
            h.put(MI(2626 if (fx + fy) % 2 == 0 else 592), fx, fy, 1)
    # Soft walkable forest clover/moss tufts (MI 996, pas=0, pri=0) dotting catwalk edges
    for mx, my in ((5, 29), (19, 29), (9, 32), (14, 31), (6, 25), (14, 24), (9, 17), (16, 18),
                   (7, 11), (18, 11), (18, 4), (21, 5), (3, 5)):
        if rows[my][mx] == '.' and h.L[2, my, mx] == 0 and h.L[1, my, mx] == 0:
            h.put(MI(996), mx, my, 2)

    # ---- 6. Multi-Tier Dappled Canopy Sunbeams Streaming Through the Elder Tree ----
    canopy_sunbeam(h, 5, 4, 11, rows)      # NW knot-hole beam across COMBINE abyss onto Ledge 3
    canopy_sunbeam(h, 15, 4, 10, rows)     # NE knot-hole beam across Tamsin's canopy pavilion!
    canopy_sunbeam(h, 11, 12, 18, rows)    # Mid-canopy beam cutting across TWIST abyss onto Ledge 2
    canopy_sunbeam(h, 4, 20, 26, rows)     # Lower canopy beam illuminating Ledge 1 & Nell's lookout
    canopy_sunbeam(h, 8, 29, 33, rows)     # Entrance foyer sunbeam illuminating Pim & Teach launch

    if save:
        out = os.path.join(HERE, 'data', 'raw', '131.npy')
        np.save(out, h.L)
        print('wrote', out, h.L.shape)
    return h.L


# ============================================================================================ 154 Pell Playhouse - Auditorium
def build_154(save=True):
    rows = P.THEATRE
    cls = {'#': 'void', 'K': 'wall', 'P': 'wall', 'B': 'wall', 'D': 'wall', 'p': 'lip', 'S': 'stair', 's': 'seat',
           ',': 'floor2', 'r': 'floor2', 'o': 'floor2', 'g': 'floor2', 'a': 'floor', '.': 'floor'}
    h = K.Hall(rows, 'stage', cls, seed=154)
    BOARDS = [MI(1241), MI(1242), MI(1243)]
    rnd = h.r

    # ---- 1. Base House Damask Carpet & Clean Stage Lip ----
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch in ',rgs':
                h.put(NM(685), x, y, 0)
            if ch == 'p':
                h.put(0, x, y, 1)

    # ---- 2. Void-Sculpted Stepped Art-Deco Rear Foyer Corners (Breaks Rectangular Box Silhouette!) ----
    # Carve far SW (1..3, 28) & SE (21..23, 28) dead foyer corners into sleek purple-framed void bays
    # while leaving x=4..20, y=28 and ALL of y=27 (x=1..23) 100% open & navigable!
    for vx in (1, 2, 3, 21, 22, 23):
        h.put(MG(4500), vx, 28, 0); h.put(0, vx, 28, 1); h.put(0, vx, 28, 2)
    h.put(MG(4501), 3, 28, 0)        # stepped inner corner N+E facing (4,28) foyer
    h.put(MG(4499), 21, 28, 0)       # stepped inner corner N+W facing (20,28) foyer
    for vx in (1, 2, 3, 21, 22, 23):
        h.put(MG(4508), vx, 29, 0)

    # ---- 3. Side Walls, Ornate Opera Box Balconies & Stage Proscenium ----
    for y in range(2, 11):
        for x in list(range(1, 4)) + list(range(21, 24)):
            h.put(NM(402) if y == 2 else NM(865), x, y, 0)
    for x0 in (1, 21):
        h.block([[NM(685)] * 3] * 3, x0, 3, 0)
        h.block([[0, 0, 0], [NM(654)] * 3, [NM(920), NM(921), NM(922)], [NM(888), 0, NM(890)], [NM(896), NM(897), NM(898)]], x0, 3, 1)
        h.block([[NM(904), NM(905), NM(906)], [NM(912), NM(867), NM(914)], [NM(880), NM(875), NM(882)], [0, NM(889), 0], [0, NM(897), 0]], x0, 3, 2)
        h.block([[NM(842), NM(843), NM(844)], [NM(850), NM(851), NM(852)]], x0, 9, 1)
        # Ornate gilded mini-chandelier between opera box & stage-wing door!
        h.block([[NM(779)], [NM(787)]], x0 + 1, 7, 2)
        # Gilded Art-Deco crown cornice across the top of each opera box
        h.block([[CU('beam_l'), CU('beam_mid'), CU('beam_r')]], x0, 2, 1)
    for y in range(2, 11):
        for x in (4, 20):
            h.put(NM(865), x, y, 0)
            h.put(CU('column_cap') if y == 3 else CU('column_base') if y == 10 else CU('column_shaft'), x, y, 1)
    for x in range(4, 21):
        h.put(NM(393), x, 2, 0)
        h.put(CU('beam_l') if x == 4 else CU('beam_r') if x == 20 else CU('beam_mid'), x, 2, 1)
    h.block([[CU('crest_0'), CU('crest_1'), CU('crest_2')]], 11, 2, 2)
    for x in range(5, 20):
        for y in range(3, 6): h.put(CU('backdrop_%d_%d' % (x - 5, y - 3)), x, y, 0)
    for x in range(5, 20):
        h.put(NM(904) if x == 5 else NM(906) if x == 19 else NM(905), x, 3, 2)

    # ---- 4. Polished Stage Boards, Footlights, Dramatic Spotlight Cones & Orchestra Pit ----
    for y in range(6, 12):
        for x in range(1 if y == 11 else 5, 24 if y == 11 else 20):
            if y == 11 and x in (11, 12, 13):
                h.put(CU('dais'), x, y, 0)     # rich deep-crimson central stage apron focus!
            else:
                h.put(rnd.choice(BOARDS), x, y, 0)
    for y in range(4, 11):
        h.put(NM(920) if y == 10 else NM(912), 5, y, 2)
        h.put(NM(922) if y == 10 else NM(914), 19, y, 2)
    h.put(CU('mark'), 12, 8, 1); h.put(CU('mark'), 8, 9, 1); h.put(CU('mark'), 16, 9, 1)
    for x in range(1, 24):
        if x != 12: h.put(CU('footlight'), x, 12, 0)
        h.put(CU('glow'), x, 11, 2)
    h.put(BOARDS[0], 12, 12, 0); h.put(MG(3151), 12, 12, 1)

    # Warm theatrical spotlights converging on Dorian's center stage mark (12,7..11)!
    for sy in range(6, 11):
        for sx, k in ((11, 'l'), (12, 'full'), (13, 'r')):
            if h.L[2, sy, sx] == 0:
                h.put(CU('light_' + k), sx, sy, 2)

    # Orchestra Pit + Grand Piano + Music Stands + Pit Rail
    for y in range(13, 16):
        for x in list(range(1, 11)) + list(range(14, 24)):
            h.put(CU('pit_%d' % rnd.randrange(3)), x, y, 0)
    h.block([[CH(1464), CH(1465), CH(1466)], [CH(1472), CH(1473), CH(1474)], [CH(1480), CH(1481), CH(1482)]], 2, 13, 1)
    for x, y in ((6, 14), (8, 15), (16, 14), (18, 15), (21, 14)):
        h.put(CU('music_stand'), x, y, 1)
    for x in range(1, 24):
        if 11 <= x <= 13: continue
        h.put(CU('pit_rail_l') if x in (1, 14) else CU('pit_rail_r') if x in (10, 23) else CU('pit_rail_mid'), x, 16, 1)

    # ---- 5. Sumptuous Art-Deco Gold-Filigree Promenades & Royal Crimson Center Runner ----
    put_deco_frame(h, 2, 17, 10, 17, z=1)
    put_deco_frame(h, 14, 17, 22, 17, z=1)
    put_deco_frame(h, 2, 22, 10, 22, z=1)
    put_deco_frame(h, 14, 22, 22, 22, z=1)
    put_deco_frame(h, 4, 27, 10, 28, z=1)
    put_deco_frame(h, 14, 27, 20, 28, z=1)

    # Royal crimson-and-gold velvet runner marching straight up the center aisle to the stage steps!
    for y in range(13, 29):
        r = 0 if y == 13 else (2 if y == 28 else 1)
        for i in range(3):
            h.put(NM([[773, 774, 775], [781, 782, 783], [789, 790, 791]][r][i]), 11 + i, y, 1)

    # ---- 6. Majestic Triple-Chandelier Nave, Side-Wall Opera Sconces & Sumptuous Rear Foyer Dress ----
    h.block([[0, NM(779), 0], [0, NM(779), 0], [NM(776), NM(787), NM(778)], [NM(784), NM(785), NM(786)]], 11, 19, 2)
    h.block([[0, NM(779), 0], [NM(776), NM(787), NM(778)], [NM(784), NM(785), NM(786)]], 11, 13, 2)
    for sx in (1, 23):
        for sy in (16, 22, 25):
            h.block([[NM(779)], [NM(787)]], sx, sy, 2)

    # Golden opera urns flanking the chamfered foyer steps (4, 27..28) & (20, 27..28)
    h.obj('urn', 4, 27); h.obj('urn', 20, 27)
    # Lush rose & floral opera bouquets nestled neatly against the south foyer wall (6..7, 27..28) & (17..18, 27..28)
    h.block([[NM(518), NM(519)], [NM(526), NM(527)]], 6, 27, 1)
    h.block([[NM(518), NM(519)], [NM(526), NM(527)]], 17, 27, 1)
    # Potted opera greenery & gold-stanchioned red velvet foyer ropes flanking the center crimson entry!
    h.put(NM(538), 9, 28, 1); h.put(NM(539), 15, 28, 1)
    h.block([[NM(1016), NM(1017), NM(1018)]], 1, 27, 2)
    h.block([[NM(1016), NM(1017), NM(1018)]], 21, 27, 2)
    # Entrance mat at Lobby doors (11..13, 29)
    h.put(MG(1731), 11, 29, 1); h.put(MG(1732), 12, 29, 1); h.put(MG(1733), 13, 29, 1)

    if save:
        out = os.path.join(HERE, 'data', 'raw', '154.npy')
        np.save(out, h.L)
        print('wrote', out, h.L.shape)
    return h.L


def apply_craft(mid, L_out):
    """Apply Wave 4 Rejuvenation V14 sculpts in-place inside hallkit.Hall.write() before passguard.guard()."""
    if mid == 131:
        L_out[:] = build_131(save=False)
    elif mid == 154:
        L_out[:] = build_154(save=False)


def main(which=None):
    sel = set(which or [])
    if not sel or '131' in sel:
        build_131(save=True)
    if not sel or '154' in sel:
        build_154(save=True)


if __name__ == '__main__':
    main(sys.argv[1:])
