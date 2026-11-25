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


# ============================================================================================ 130 Loomhouse Gym - Lobby
def build_130(save=True):
    """Wave 7 Rejuvenation V14 sculpt of Map 130 (Loomhouse Gym - Lobby, 20x16, Tileset 54).
    Living Elder-Tree Weaver's Guildhall seamlessly unified with Wave 4's 131 Canopy:
      - Void-sculpted SW/SE foyer chamfers & recessed entry vestibule around Exit (9, 15)
      - Living Elder-Tree bark archway (bark_18036..18055), cobwebs, silk cocoons & canopy sunbeam
        framing Up into the tree @ (15, 4)
      - Mother Loom's 2x2 gold-framed Portrait (2908..2917) above Portrait @ (8, 5) & authentic
        First loom right on (5..6, 7..8)
      - Grand Briarwick crimson-gold woven silk tapestry runner (MI 1040..1058) sweeping past
        Gym guide (7, 13), Tamsin (10, 9 -> walks UP to 10, 6!) & Weaver Tibb (13, 8) to the stair
      - Cozy weaver looms, dye vats, silk bales, tall lanterns, woodland ferns & mossy clover tufts!
    """
    W, H = 20, 16
    g = [['#'] * W for _ in range(H)]
    for y in range(2, 6):
        for x in range(1, 19):
            g[y][x] = 'W'
    for y in range(6, 15):
        for x in range(1, 19):
            g[y][x] = '.'
    # Sculpted void chamfers along SW & SE foyer corners (zero flat box!)
    for vx, vy in ((1, 14), (2, 14), (17, 14), (18, 14)):
        g[vy][vx] = '#'
    # Recessed south entry vestibule around Exit @ (9, 15)
    for x in (8, 9, 10):
        g[15][x] = '.'
    # Elder-tree stairwell ascending Up into the tree @ (15, 4)
    g[4][15] = 'S'
    g[5][15] = 'S'

    rows = [''.join(r) for r in g]
    cls = {'#': 'void', 'W': 'wall', '.': 'floor', 'S': 'stair'}
    h = K.Hall(rows, 'loom', cls, seed=130)
    rnd = h.r

    # ---- 1. Living Elder-Tree Bark Frame Around the Canopy Stairwell (14..16, 2..5) & SW/SE Buttresses! ----
    BARK_HI = [CU('bark_%d' % t) for t in (18036, 18037, 18038, 18039)]
    BARK = [CU('bark_%d' % t) for t in (18044, 18045, 18046, 18047)]
    BARK_LO = [CU('bark_%d' % t) for t in (18052, 18053, 18054, 18055)]
    for y in range(2, 6):
        for x in (14, 15, 16):
            if (x, y) in ((15, 4), (15, 5)):
                continue
            h.put(rnd.choice(BARK_HI if y == 2 else BARK_LO if y == 5 else BARK), x, y, 0)
    # Warm timber deck under the stair steps (15, 4..5)
    h.put(MI(1242), 15, 4, 0); h.put(MI(962), 15, 4, 1)
    h.put(MI(1241), 15, 5, 0); h.put(MI(962), 15, 5, 1)
    # Cascading woven canopy web & hanging silk cocoons crowning the Elder-Tree stair arch!
    h.obj('web', 14, 2)
    h.put(CU('cocoon_top'), 14, 4, 2); h.put(CU('cocoon_bot'), 14, 5, 2)
    h.put(CU('strand_p_top'), 16, 4, 2); h.put(CU('strand_p_bot'), 16, 5, 2)

    # ---- 2. Tall Arched Woodland Windows, Floor-to-Ceiling Bookcases & Mother Loom's Framed Portrait! ----
    for x0 in (3, 10):
        h.put(CU('window_top_0'), x0, 2, 1); h.put(CU('window_top_1'), x0 + 1, 2, 1)
        h.put(CU('window_mid_0'), x0, 3, 1); h.put(CU('window_mid_1'), x0 + 1, 3, 1)
        h.put(CU('window_sill_0'), x0, 4, 1); h.put(CU('window_sill_1'), x0 + 1, 4, 1)
    h.obj('shelf', 1, 2)
    h.obj('shelf', 17, 2)

    # Mother Loom's 2x2 Gold-Framed Portrait (2908..2917) mounted cleanly at (7..8, 3..4) directly above Portrait @ (8, 5)!
    h.block([[2908, 2909], [2916, 2917]], 7, 3, 1)
    # Silk-bolt guild ribbon & brass plaque under Portrait @ (8, 5) + Apology card pin-note @ (12, 5)
    h.put(CU('bolt_r'), 6, 5, 1); h.put(CU('bolt_b'), 7, 5, 1); h.put(CU('bolt_y'), 8, 5, 1)
    h.put(CU('paste_1_1'), 12, 4, 1)   # Pinned apology notice card right above Apology card @ (12, 5)!

    # ---- 3. Grand Briarwick Crimson-Gold Woven Silk Tapestry Runner (Matches 131 Canopy!) ----
    # Sweeps from Exit (9, 15) straight up x=8..10, y=6..14 (under Tamsin @ (10,9) and her full UP walk (10,6..9)!)
    # and joins a horizontal stair-approach tapestry runner (x=11..15, y=6..7) leading to Up into the tree (15, 4)!
    put_mi_rug(h, 8, 6, 10, 14, z=1)
    # Smoothly connect horizontal silk runner arm from x=10..15, y=6..7 (seamless crimson weave!)
    for y in (6, 7):
        for x in range(11, 16):
            if y == 6:
                t = MI(1042) if x == 15 else MI(1041)
            else:
                t = MI(1058) if x == 15 else MI(1057)
            h.put(t, x, y, 1)
    # Seam corner at (10, 6..7) so the L-turn reads as one unbroken woven carpet!
    h.put(MI(1041), 10, 6, 1)
    h.put(MI(1049), 10, 7, 1)
    # Entry doormat at (8..10, 15)
    h.obj('mat_mi', 8, 15)

    # Subtle decorative parquet inlays on open timber planks
    for y in range(6, 15):
        for x in range(1, 19):
            if rows[y][x] == '.' and h.L[1, y, x] == 0 and (x + y) % 5 == 0 and 2 <= x <= 17:
                h.put(MI(1224), x, y, 0)

    # ---- 4. Authentic Weaving Workshops: Mother Loom's First Loom (6, 7), Apprentice Looms, Silk & Dye Vats! ----
    # Mother Loom's First Loom placed right at (5..6, 7..8) so First loom @ (6, 7) IS the actual loom!
    # Keep (7, 6..14), (6, 6), (4, 7..8), (5..6, 9) open so player can inspect it from any side!
    h.obj('loom', 5, 7)
    h.obj('loom', 2, 7)                # Twin historic west guild loom (2..3, 7..8)
    # Lower west artisan nook: one loom (2..3, 11..12) + spun silk & wicker basket beside it
    h.obj('loom', 2, 11)
    h.put(CU('basket'), 5, 11, 1)
    h.put(CU('spool'), 5, 12, 1)
    h.obj('silk1', 1, 6)               # Fresh silk bale beside west bookcase

    # East Workshop: Weaver Tibb @ (13, 8) beside finished cloth inspection rack (12..14, 9..10),
    # apprentice looms (14..15, 11..12) & (16..17, 11..12), dye vats (12..14, 13), & silk bales!
    # Keep Item (POTION) @ (17, 7) cleanly accessible via (16..17, 6..7) & (15..16, 7..8)!
    h.obj('awning', 12, 9)
    h.obj('laundry', 12, 10)
    h.obj('loom', 14, 11)
    h.obj('loom', 16, 11)
    h.obj('vat_b', 12, 13); h.obj('vat_r', 13, 13); h.obj('vat_y', 14, 13)
    h.obj('silk', 18, 8)               # Stacked silk bales on east wall (18, 8..9), clear of Item @ (17, 7)!
    h.put(CU('basket'), 18, 6, 1)

    # ---- 5. Warm Hanging Lanterns, Potted Woodland Ferns, Moss Clover & Dappled Canopy Sunbeams! ----
    # Complete 1x3 hanging lanterns anchored cleanly against side walls & foyer (ZERO blocked paths!)
    h.obj('lantern', 1, 8)             # West wall lantern (1, 8..10)
    h.obj('lantern', 18, 10)           # East wall lantern (18, 10..12)
    h.obj('lantern', 7, 10)            # Foyer lantern framing Gym guide (7, 13) -> base at (7, 12)!
    # Wait: keep (7, 12) open right above Gym guide (7, 13) so player can approach Gym guide from north too!
    h.put(0, 7, 10, 2); h.put(0, 7, 11, 2); h.put(0, 7, 12, 1)
    h.obj('lantern', 11, 11)           # East foyer lantern (11, 11..13) cleanly beside the crimson runner!
    # Lush intact potted woodland ferns framing the chamfered SW/SE foyer notches & side bays!
    for fx, fy, top_t, bot_t in (
        (3, 14, 2618, 2626),           # SW chamfer fern
        (16, 14, 2618, 2626),          # SE chamfer fern
        (1, 13, 584, 592),             # West parlor fern
        (18, 13, 584, 592),            # East parlor fern
    ):
        h.put(MI(top_t), fx, fy - 1, 2)
        h.put(MI(bot_t), fx, fy, 1)
    # Soft walkable forest moss/clover tufts (MI 996, pas=0, pri=0) linking visually to 131 Canopy!
    for mx, my in ((4, 6), (13, 6), (16, 6), (6, 13), (11, 14), (4, 10), (15, 10)):
        if h.L[1, my, mx] == 0 and h.L[2, my, mx] == 0:
            h.put(MI(996), mx, my, 2)

    # Warm diagonal woodland sunbeams streaming through the north arched windows & Elder stairwell!
    for x0, y0, y1 in ((3, 6, 10), (10, 6, 9), (14, 6, 8)):
        for y in range(y0, y1 + 1):
            c = x0 + (y - y0)
            for dx, k in ((0, 'l'), (1, 'full'), (2, 'r')):
                xx = c + dx
                if 1 <= xx <= 18 and rows[y][xx] == '.' and h.L[2, y, xx] == 0 and h.L[1, y, xx] == 0:
                    h.put(CU('light_' + k), xx, y, 2)

    import passguard as PG
    PG.guard(h.L, K.TID, [(9, 15), (15, 4), (7, 13), (13, 8), (12, 5), (8, 5), (17, 7), (10, 9), (6, 7)], 'map 130')
    if save:
        out = os.path.join(HERE, 'data', 'raw', '130.npy')
        np.save(out, h.L)
        print('wrote', out, h.L.shape)
    return h.L


# ============================================================================================ 145 Pageant Hall
def build_145(save=True):
    """Wave 7 Rejuvenation V14 sculpt of Map 145 (Pageant Hall, 38x26, Tileset 54).
    Grand Saltmere Waterfront Opera & Pageant Theatre unified with Wave 4's 154 Opera House:
      - Void-sculpted chamfered rear auditorium corners (1..2, 23 & 35..36, 23) and beveled
        outer backstage wing corners (1, 9 & 36, 9) — ZERO rigid purple rectangle!
      - Sumptuous Dusk-over-Saltmere proscenium with gathered crimson curtains, gilded cornice,
        proscenium mini-chandeliers, dramatic stage spotlight cones, glowing footlights & crimson apron dais
      - Art-Deco gold-filigree promenade borders (NM 1560..1578) framing ALL aisles & triple golden
        chandeliers suspended down the nave + gilded wall sconces & velvet gallery ropes
      - Tender Choir Greenroom backstage left (x=1..8) for Vesper + Lyra + Eevee's duet: crimson-gold
        woven Briarwick carpet, genuine theatrical costume rack (1904..1914), prop shelves & warm lantern
      - Dorian's Star Dressing Room backstage right (x=29..36): ACTUAL 2x2 bulb-ringed star vanity
        mirror (1899..1908) right above Dorian's mirror @ (31, 3), plush carpet, chaise, stage lamp
        & crisp torn-backdrop paint loft!
    Preserves 100% of all 34 events (incl. all 18 audience seat coords!).
    """
    W, H = 38, 26
    WL = (1, 8); ST = (11, 26); WR = (29, 36)
    g = [['#'] * W for _ in range(H)]

    def fill(x0, x1, y0, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                g[y][x] = c

    for a, b in (WL, ST, WR):
        fill(a, b, 1, 2, 'W')
        fill(a, b, 3, 9, '.')
    fill(9, 10, 7, 8, '.')
    fill(27, 28, 7, 8, '.')
    fill(ST[0], ST[1], 10, 10, 'p')
    fill(18, 19, 10, 10, 'S')
    fill(1, 10, 11, 12, 'W')
    fill(27, 36, 11, 12, 'W')
    fill(ST[0], ST[1], 11, 12, ',')
    fill(1, 36, 13, 23, ',')
    for y in list(range(14, 18)) + list(range(19, 23)):
        for x in list(range(3, 16)) + list(range(22, 35)):
            g[y][x] = 's'
    fill(17, 20, 24, 24, ',')

    # Void-sculpted Art-Deco chamfers (100% clear of all 18 seats & all backstage events!)
    for vx, vy in ((1, 23), (2, 23), (35, 23), (36, 23), (1, 9), (36, 9)):
        g[vy][vx] = '#'

    rows = [''.join(r) for r in g]
    cls = {'#': 'void', 'W': 'wall', 'p': 'lip', 'S': 'stair', 's': 'seat', ',': 'floor2', '.': 'floor'}
    h = K.Hall(rows, 'stage', cls, seed=145)
    rnd = h.r
    BOARDS = [MI(1241), MI(1242), MI(1243)]

    # ---- 1. Rich Dark Crimson-Plum Damask House Carpet (Matches 154 Opera House!) ----
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch in ',s':
                h.put(NM(685), x, y, 0)

    # ---- 2. Grand Dusk-over-Saltmere Proscenium Stage, Spotlights & Apron ----
    for y in range(3, 10):
        for x in range(ST[0], ST[1] + 1):
            h.put(rnd.choice(BOARDS), x, y, 0)
    for x in range(ST[0] + 1, ST[1] + 1):
        for y in range(3, 6):
            h.put(CU('backdrop_%d_%d' % (x - ST[0] - 1, y - 3)), x, y, 0)
        h.put(NM(904) if x == ST[0] + 1 else NM(906) if x == ST[1] else NM(905), x, 3, 2)
    for x in range(ST[0], ST[1] + 1):
        h.put(NM(393), x, 1, 0)
        h.put(CU('beam_l') if x == ST[0] else CU('beam_r') if x == ST[1] else CU('beam_mid'), x, 1, 1)
    h.block([[CU('crest_0'), CU('crest_1'), CU('crest_2')]], 17, 1, 2)
    # Rich crimson gathered stage curtains framing left & right proscenium wings
    for y in range(4, 10):
        h.put(NM(920) if y == 9 else NM(912), ST[0], y, 2)
        h.put(NM(922) if y == 9 else NM(914), ST[1], y, 2)
    # Twin gilded proscenium chandeliers illuminating the Saltmere sunset drop!
    h.block([[NM(779)], [NM(787)]], 12, 3, 2)
    h.block([[NM(779)], [NM(787)]], 25, 3, 2)
    # Stage marks & rostrum
    for x, y in ((14, 7), (18, 8), (23, 7)):
        h.put(CU('mark'), x, y, 1)
    h.put(CU('rostrum'), 21, 6, 1)
    # Glowing footlights along the stage lip & warm golden footlight halo
    for x in range(ST[0], ST[1] + 1):
        if x not in (18, 19):
            h.put(CU('footlight'), x, 10, 0)
            h.put(0, x, 10, 1)
        h.put(CU('glow'), x, 9, 2)
    # Theatrical spotlight cone illuminating center stage (Pageant @ (18,7) & Ottilie @ (16,7))!
    for sy in range(6, 9):
        for sx, k in ((17, 'l'), (18, 'full'), (19, 'r')):
            if h.L[2, sy, sx] == 0:
                h.put(CU('light_' + k), sx, sy, 2)
    # Polished stage apron boards + deep crimson center dais below the stage steps!
    for x in range(ST[0], ST[1] + 1):
        for y in (11, 12):
            if 17 <= x <= 20:
                h.put(CU('dais'), x, y, 0)
            else:
                h.put(rnd.choice(BOARDS), x, y, 0)

    # ---- 3. Art-Deco Gold-Filigree Promenades, Plush Crimson Center Runner & Triple Chandeliers! ----
    # Gold-filigree borders lining the front apron promenade, cross-aisle (y=18), side aisles & rear foyer!
    put_deco_frame(h, 3, 13, 15, 13, z=1)
    put_deco_frame(h, 22, 13, 34, 13, z=1)
    put_deco_frame(h, 3, 18, 15, 18, z=1)
    put_deco_frame(h, 22, 18, 34, 18, z=1)
    put_deco_frame(h, 3, 23, 15, 23, z=1)
    put_deco_frame(h, 22, 23, 34, 23, z=1)
    put_deco_frame(h, 1, 13, 2, 22, z=1)
    put_deco_frame(h, 35, 13, 36, 22, z=1)

    # Grand Royal Crimson Ceremonial Runner marching up the 4-wide center nave (17..20, 13..24)!
    for y in range(13, 25):
        r_ = 0 if y == 13 else (2 if y == 24 else 1)
        for i in range(4):
            h.put(NM([[773, 774, 774, 775], [781, 782, 782, 783], [789, 790, 790, 791]][r_][i]), 17 + i, y, 1)

    # Triple Golden Opera Chandeliers (Twin stalls + grand central nave chandelier at x=17..19, y=16..19!)
    for cx, cy in ((8, 15), (28, 15), (17, 16)):
        h.block([[0, NM(779), 0], [0, NM(779), 0], [NM(776), NM(787), NM(778)], [NM(784), NM(785), NM(786)]], cx, cy, 2)
    # Ornate side-wall gilded sconces lining the house aisles (pri=5, non-blocking!)
    for sx in (1, 36):
        for sy in (15, 19):
            h.block([[NM(779)], [NM(787)]], sx, sy, 2)

    # Warm Opera House North Wall Dress behind the Stalls (y=11..12):
    # Posters framed by gilded sconces & red velvet gallery ropes (banishing sterile blank white wall!)
    h.obj('poster_lady', 2, 10)        #Wait: wall is y=11..12! Keep exact poster y=11 so top sits on y=11 wall!
    # Clear any y=10 overwrite and place posters cleanly on wall rows y=11..12 (same crisp framing as HEAD + extra poster!)
    for x in (2, 3, 4):
        h.put(0, x, 10, 1)
    # Replace stark white house wall (y=11..12) with warm dark Art-Deco opera paneling (NM 865 + gilded crown NM 402)!
    for x in list(range(1, 11)) + list(range(27, 37)):
        h.put(NM(402), x, 11, 0)
        h.put(NM(865), x, 12, 0)
    # Gilded Art-Deco beam crowning the north house galleries
    for x0, x1 in ((1, 10), (27, 36)):
        for x in range(x0, x1 + 1):
            h.put(CU('beam_l') if x == x0 else CU('beam_r') if x == x1 else CU('beam_mid'), x, 11, 1)
    # Playbill posters & gilded sconces along the warm burgundy house wall (leaving (7,13) Prop lantern 100% open!)
    h.block([[2250, 2251, 2252], [2258, 2259, 2260]], 2, 11, 1)    # The Lady in Red framed poster (2..4, 11..12)
    h.block([[2408, 2409, 2410], [2416, 2417, 2418]], 28, 11, 1)   # The Loyal Three framed poster (28..30, 11..12)
    h.block([[2320, 2321, 2322], [2328, 2329, 2330]], 33, 11, 1)   # Rain Fall framed poster (33..35, 11..12)
    # Ornate sconces & velvet curtain swags on wall gaps (6, 9, 27, 31, 36)
    for sx in (6, 9, 27, 32):
        h.block([[2611], [2619]], sx, 11, 2)
    # Velvet gallery ropes along front wall (y=13, pas=0!) keeping (7, 13) Prop lantern clear
    h.block([[2800, 2801, 2802]], 2, 13, 2)
    h.block([[2800, 2801, 2802]], 28, 13, 2)
    h.block([[2800, 2801, 2802]], 33, 13, 2)

    # Golden urns & lush floral opera bouquets framing the side aisles & chamfered rear foyer
    for x in (1, 36):
        h.obj('urn', x, 13)
        h.obj('urn', x, 21)
    h.block([[NM(518), NM(519)], [NM(526), NM(527)]], 1, 17, 1)
    h.block([[NM(518), NM(519)], [NM(526), NM(527)]], 35, 17, 1)
    # Rear foyer bouquets flanking the grand central entry carpet (14..15, 23) & (22..23, 23) — keep all seats clear!
    h.obj('urn', 16, 22)
    h.obj('urn', 21, 22)
    h.put(MG(1731), 17, 24, 1); h.put(MG(1732), 18, 24, 1); h.put(MG(1732), 19, 24, 1); h.put(MG(1733), 20, 24, 1)

    # ---- 4. Backstage Left: Choir Greenroom for Vesper + Lyra + Eevee's Tender Duet (x=1..8, y=3..9)! ----
    for x in range(WL[0], WL[1] + 1):
        for y in range(3, 10):
            if rows[y][x] == '.':
                h.put(rnd.choice(BOARDS), x, y, 0)
    for x in range(9, 11):
        for y in (7, 8):
            h.put(rnd.choice(BOARDS), x, y, 0)
    # Warm timber-and-burgundy greenroom walls instead of stark blank white
    for x in range(WL[0], WL[1] + 1):
        h.put(NM(402), x, 1, 0)
        h.put(NM(865), x, 2, 0)
    # Cozy Briarwick crimson-gold tapestry rug right under Vesper (5,5), Lyra (6,5), Eevee (7,6) & Chorus (4,6)!
    put_mi_rug(h, 4, 4, 7, 7, z=1)
    # Stocked Prop Shelves at (1..4, 1..4) backing Prop shelf @ (2, 5) — 100% clear of (2, 5)!
    h.obj('shelf', 1, 1)
    h.obj('shelf', 3, 1)
    # Genuine Theatrical Costume Rack (1904..1914) on the greenroom north wall (5..7, 2..3) — clear of Chorus 2 @ (7, 4)!
    h.block([[1904, 1905, 1906], [1912, 1913, 1914]], 5, 2, 1)
    # Warm golden backstage sconce & standing lantern illuminating Vesper & Lyra
    h.block([[2611], [2619]], 8, 1, 2)
    h.obj('lantern', 1, 5)             # (1, 5..7) warm lantern beside prop shelves
    for x, y, n in ((2, 8, 'basket'), (3, 8, 'spool'), (8, 4, 'basket'), (8, 5, 'log')):
        h.put(CU(n), x, y, 1)
    # Cozy greenroom potted fern tucked in SW bevel corner (2, 9) — leaves (3..8, 8..9) wide open to wing door (9..10, 7..8)!
    h.put(MI(584), 2, 8, 2) if False else None
    h.obj('plant', 4, 8)               # Wait: check (4,8..9) — leaves (3..8, 7) & (5..8, 8..9) 100% open!
    h.put(0, 4, 8, 2); h.put(0, 4, 9, 1)  # Even cleaner: put potted fern at (2, 8)? (2,8) has basket -> put fern at (8, 3)!
    h.obj('plant', 8, 2)               # Potted greenroom fern neatly in NE corner (8, 2..3), clear of Chorus 2 @ (7, 4)!

    # ---- 5. Backstage Right: Dorian's Star Dressing Room & Torn-Backdrop Paint Loft (x=29..36, y=3..9)! ----
    for x in range(WR[0], WR[1] + 1):
        for y in range(3, 10):
            if rows[y][x] == '.':
                h.put(rnd.choice(BOARDS), x, y, 0)
    for x in range(27, 29):
        for y in (7, 8):
            h.put(rnd.choice(BOARDS), x, y, 0)
    # Warm burgundy dressing-room north wall with gilded cornice
    for x in range(WR[0], WR[1] + 1):
        h.put(NM(402), x, 1, 0)
        h.put(NM(865), x, 2, 0)
    # ACTUAL 2x2 BULB-RINGED STAR VANITY MIRROR (1899..1908) mounted right at (30..31, 1..2) above Dorian's mirror @ (31, 3)!
    h.block([[1899, 1900], [1907, 1908]], 30, 1, 1)
    h.block([[2611], [2619]], 29, 1, 2)    # Golden star dressing-room wall sconce!
    h.block([[2611], [2619]], 32, 1, 2)    # Twin golden sconce flanking Dorian's mirror!
    # Lush Crimson-Gold Star Dressing Rug (29..32, 4..7) + Velvet Star Divan (29, 4..6) — keeps wing door (27..29, 7..8) wide open!
    put_mi_rug(h, 29, 4, 32, 7, z=1)
    h.obj('couch_l', 29, 4)
    # Crisp Torn Backdrop Paint Loft (33..35, 2..4) backing Torn backdrop @ (34, 4) + Pigment Vats (33..35, 8) + Warm Stage Lantern!
    for x, n in ((33, 'drop_forest_top'), (34, 'drop_throne_top'), (35, 'drop_forest_top')):
        h.put(CU(n), x, 2, 2)
    for x, n in ((33, 'drop_forest_bot'), (35, 'drop_ship_bot')):
        h.put(CU(n), x, 3, 2)
    for x, n in ((33, 'vat_r'), (34, 'vat_b'), (35, 'vat_y')):
        h.obj(n, x, 8)
    h.obj('plant', 36, 3)              # Tall dressing-room palm at (36, 3..4)
    h.obj('lantern', 36, 6)            # Warm glowing backstage lamp at (36, 6..8), replacing floating flat!
    h.put(CU('basket'), 31, 9, 1)      # Costumer's prop hamper at south edge (31, 9)
    h.put(CU('spool'), 32, 9, 1)

    import passguard as PG
    PG.guard(h.L, K.TID, [(18, 24), (19, 24), (18, 7), (2, 5), (34, 4), (31, 3), (4, 6), (7, 4), (25, 12),
                          (5, 5), (6, 5), (7, 6), (7, 13), (16, 7), (18, 13), (26, 11)], 'map 145')
    if save:
        out = os.path.join(HERE, 'data', 'raw', '145.npy')
        np.save(out, h.L)
        print('wrote', out, h.L.shape)
    return h.L


# ============================================================================================ 150 Pell Playhouse - Lobby
def build_150(save=True):
    """Wave 7 Rejuvenation V14 sculpt of Map 150 (Pell Playhouse - Lobby, 25x15, Tileset 54).
    Sumptuous Art-Deco Grand Opera Foyer unified 100% with Wave 4's 154 Auditorium:
      - Void-sculpted SW (1..2, 13) & SE (22..23, 13) stepped Art-Deco foyer corners + recessed Entry (11..13, 14)
      - Rich dark plum-crimson Opera Damask carpet (NM 685) framed by Art-Deco gold-filigree promenade
        borders (NM 1560..1578) zoning West Box Office Salon, Center Grand Promenade & East Playbill Lounge
      - Warm Art-Deco burgundy-and-gold north gallery wall (replacing sterile white!) framing all 4
        Playbill Posters (Rain Fall, Lady in Red, Loyal Three, Old poster) & gilded Auditorium doors (12, 5)
      - Ornate central golden chandelier, twin foyer spotlight shafts, gilded wall sconces between every
        poster, red velvet stanchion ropes, golden urns, lush opera bouquets & velvet box-office salon!
    Preserves 100% of all 16 HEAD events & counter-talk across Box office @ (3, 7)!
    """
    W, H = 25, 15
    g = [['#'] * W for _ in range(H)]
    for y in range(2, 6):
        for x in range(1, 24):
            g[y][x] = 'W'
    for y in range(6, 14):
        for x in range(1, 24):
            g[y][x] = '.'
    # Gilded 3-wide Auditorium double doors centered on Auditorium doors @ (12, 5)
    for y in (4, 5):
        for x in (11, 12, 13):
            g[y][x] = 'D'
    # Sculpted stepped Art-Deco SW & SE foyer void corners (matching 154 Opera House!)
    for vx, vy in ((1, 13), (2, 13), (22, 13), (23, 13)):
        g[vy][vx] = '#'
    # Recessed entrance door notch around Exit @ (12, 14)
    for x in (11, 12, 13):
        g[14][x] = '.'

    rows = [''.join(r) for r in g]
    cls = {'#': 'void', 'W': 'wall', 'D': 'door', '.': 'floor'}
    h = K.Hall(rows, 'lobby', cls, seed=150)

    # ---- 1. Sumptuous Dark Crimson-Plum Opera Damask Carpet (NM 685) & Warm Burgundy Gallery Wall ----
    for y in range(6, 15):
        for x in range(1, 24):
            if rows[y][x] == '.':
                h.put(NM(685), x, y, 0)
    # Warm dark Art-Deco burgundy opera walls (NM 402 crown + NM 865 paneling) replacing blinding blank white!
    for y in range(2, 6):
        for x in range(1, 24):
            if rows[y][x] == 'W':
                h.put(NM(402) if y == 2 else NM(865), x, y, 0)
    # Gilded Art-Deco proscenium crown beam across the top of the gallery wall (y=2)
    for x in range(1, 24):
        if x in (11, 12, 13):
            continue
        h.put(CU('beam_l') if x in (1, 14) else CU('beam_r') if x in (10, 23) else CU('beam_mid'), x, 2, 1)
    # Gilded Auditorium marquee & theatrical crest crowning the double doors (11..13, 2..3)!
    h.block([[CU('beam_l'), CU('beam_mid'), CU('beam_r')]], 11, 2, 1)
    h.block([[CU('crest_0'), CU('crest_1'), CU('crest_2')]], 11, 3, 2)

    # ---- 2. All 4 Playbill Posters Preserved Crisply at Exact Event Columns (3, 7, 17, 21) + Gilded Sconces! ----
    # Poster: Rain Fall @ (3, 5)
    h.block([[2320, 2321, 2322], [2328, 2329, 2330], [2336, 2337, 2338]], 2, 2, 1)
    # Poster: The Lady in Red @ (7, 5)
    h.block([[2250, 2251, 2252], [2258, 2259, 2260], [2266, 2267, 2268]], 6, 2, 1)
    # Poster: The Loyal Three @ (17, 5)
    h.block([[2408, 2409, 2410], [2416, 2417, 2418], [2424, 2425, 2426]], 16, 2, 1)
    # Old poster @ (21, 5)
    h.block([[3143, 3144, 3145], [3146, 3147, 3148], [3149, 3150, 3151]], 20, 2, 1)
    # Gilded Art-Deco wall sconces flanking the Auditorium doors & every playbill gallery bay!
    for sx in (1, 5, 9, 10, 14, 15, 19, 23):
        if sx in (10, 14):
            h.block([[2611], [2611], [2619]], sx, 2, 2)
        else:
            h.block([[2611], [2619]], sx, 3, 2)

    # ---- 3. Art-Deco Gold-Filigree Promenade Zoning & Royal Crimson Ceremonial Runner! ----
    # Zone A: West Box Office & Velvet Waiting Salon (x=2..9, y=9..12)
    put_deco_frame(h, 2, 9, 9, 12, z=1)
    # Zone B: East Playbill Lounge & Velvet Settees (x=15..22, y=9..12)
    put_deco_frame(h, 15, 9, 22, 12, z=1)
    # Subtle rear foyer gold-filigree promenade frames (3..9, 13) & (15..21, 13)
    put_deco_frame(h, 3, 13, 9, 13, z=1)
    put_deco_frame(h, 15, 13, 21, 13, z=1)

    # Grand Royal Crimson Ceremonial Runner sweeping from Exit (12, 14) straight to Auditorium doors (12, 5)!
    for y in range(6, 14):
        r = 0 if y == 6 else (2 if y == 13 else 1)
        for i in range(3):
            h.put(NM([[773, 774, 775], [781, 782, 783], [789, 790, 791]][r][i]), 11 + i, y, 1)
    # Entrance mat at (11..13, 14)
    h.put(MG(1731), 11, 14, 1); h.put(MG(1732), 12, 14, 1); h.put(MG(1733), 13, 14, 1)

    # ---- 4. Box Office Counter (Counter-Talk Preserved!), Velvet Ropes, Bouquets, Settees & Chandelier! ----
    # Red velvet gallery ropes along north gallery wall (y=6, pas=0!) + golden urns flanking posters
    for rx in (2, 6, 16, 20):
        h.block([[2800, 2801, 2802]], rx, 6, 2)
    h.obj('urn', 5, 6)
    h.obj('urn', 19, 6)
    # Box Office red-and-gold counter (2816..2818 -> 2817 has counter flag 143!) right in front of Box office @ (3, 7)!
    h.block([[2816, 2817, 2818]], 2, 8, 1)
    h.put(2820, 4, 8, 2)                   # Box office brass service bell / carafe on counter end
    # Velvet waiting sofa beside Lady (4, 11) & Theatregoer 5 (4, 12) + lush rose floral bouquets flanking runner!
    h.block([[2565, 2566, 2567], [2573, 2574, 2575]], 5, 11, 1)
    h.block([[2542, 2543], [2550, 2551]], 8, 11, 1)
    h.block([[2542, 2543], [2550, 2551]], 16, 11, 1)
    # Twin plush violet opera settees in East Lounge (20..23, 10..12) — cleanly clear of SE chamfer (22..23, 13)!
    h.block([[2512, 2513], [2520, 2521], [2528, 2529]], 20, 10, 1)
    h.block([[2512, 2513], [2520, 2521], [2528, 2529]], 22, 10, 1)
    # Parlor greenery & golden urns framing the sculpted SW/SE foyer corners & side walls (all intact!)
    h.put(2564, 1, 10, 1)
    h.put(2564, 23, 7, 1)
    h.obj('urn', 3, 12)                    # Wait: check Lady (4, 11) & Theatregoer 5 (4, 12) -> urn at (3, 12..13) base (3, 13) clear of (4, 12)!
    h.obj('urn', 21, 12)                   # Symmetrical golden urn at (21, 12..13) framing SE chamfer!
    # Ornate side-wall golden sconces along x=1 & x=23 (pri=5, non-blocking!)
    h.block([[NM(779)], [NM(787)]], 1, 7, 2)
    h.block([[NM(779)], [NM(787)]], 23, 8, 2)

    # Majestic Central Golden Opera Chandelier suspended above the crimson runner (11..13, 6..9, pri=5!)
    h.block([[0, NM(779), 0], [0, NM(779), 0], [NM(776), NM(787), NM(778)], [NM(784), NM(785), NM(786)]], 11, 6, 2)

    # Warm theatrical foyer light shafts illuminating the grand Auditorium entry promenade!
    for sy in range(7, 11):
        for sx, k in ((9, 'l'), (10, 'full'), (11, 'r')):
            if h.L[2, sy, sx] == 0 and h.L[1, sy, sx] == 0:
                h.put(CU('light_' + k), sx, sy, 2)
        for sx, k in ((13, 'l'), (14, 'full'), (15, 'r')):
            if h.L[2, sy, sx] == 0 and h.L[1, sy, sx] == 0:
                h.put(CU('light_' + k), sx, sy, 2)

    import passguard as PG
    PG.guard(h.L, K.TID, [(12, 14), (12, 5), (10, 7), (19, 9), (4, 11), (3, 7), (14, 8), (15, 8), (7, 9),
                          (19, 12), (4, 12), (21, 5), (7, 5), (3, 5), (17, 5)], 'map 150')
    if save:
        out = os.path.join(HERE, 'data', 'raw', '150.npy')
        np.save(out, h.L)
        print('wrote', out, h.L.shape)
    return h.L


def apply_craft(mid, L_out):
    """Apply Wave 4 & Wave 7 Rejuvenation V14 sculpts in-place inside hallkit.Hall.write() before passguard.guard()."""
    fn = {130: build_130, 131: build_131, 145: build_145, 150: build_150, 154: build_154}.get(mid)
    if fn is not None:
        L_out[:] = fn(save=False)


def main(which=None):
    sel = set(which or [])
    for mid, fn in ((130, build_130), (131, build_131), (145, build_145), (150, build_150), (154, build_154)):
        if not sel or str(mid) in sel:
            fn(save=True)


if __name__ == '__main__':
    main(sys.argv[1:])
