#!/usr/bin/env python3
"""The Glassed Orchard (522, :BLEED): the Pruetts' orchard, turned to glass in one winter night.  44 x 40.
Built on PF Rejuv Snow (tileset 52) with a living Sheridan meadow pocket west of the Bleed Veil (x <= 4, y >= 31)
and a frosted crystal orchard rising across two stone-stair terraces to the glassed Pruett farmhouse in the NE.
Entry from Windfall Row on the west edge (0, 36-38).  D1 Chime Rows overlay (puzzles/dungeons.py) and Glass Foal
trial overlay (trial_overlay.py) attach on build.
Run:  /usr/bin/python3 -I mapgen/layouts/orchard.py && /usr/bin/python3 -I mapgen/build.py --strict 522"""
import os, sys, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import rkit as K
from rkit import STAMPS
import routekit as RK
from routekit import Route
import craftkit as CK
from terrain import vnoise
from wildkit import say

W, H = 44, 40
VX = 4                                     # the Veil column


def key(k): return "$game_self_switches[[522, 0, '%s']]" % k
def setk(k): return {'script': key(k) + ' = true'}
def show_larch():
    return {'script': "ev = $game_map.events.values.find { |e| e.name == 'Professor Larch' }\n"
                      "$game_self_switches[[522, ev.id, 'A']] = true if ev\n$game_map.need_refresh = true"}


def fog_event(name, opacity=58, blend=1, zoom=200, sx=2, sy=1, hue=0):
    """Parallel event that sets the map fog once (RMXP command 204, subtype 1)."""
    return {'type': 'event', 'name': 'Atmosphere', 'at': [0, 0],
            'pages': [{'trigger': 'parallel', 'commands': [{'comment': 'fog: %s (see REQUESTS.md item 3)' % name},
                                                           {'raw': [204, [1, name, hue, opacity, blend, zoom, sx, sy]]},
                                                           {'selfswitch': ['A', True]}]},
                      {'cond': {'self': 'A'}}]}


def _in_living(x, y):
    """Living Sheridan grass pocket west of the Bleed Veil (x <= 4, y >= 31, feathering gently NW)."""
    if x <= 3 and y >= 31:
        return True
    if x == 4 and y >= 32:
        return True
    return False


def build():
    # Crisp 3-row frosted Sheridan terrace cliff (top lip, mid wall, base) — proportional to a 44x40 orchard
    if 'shs3' not in K.KITS:
        K.KITS['shs3'] = dict(K.KITS['shs'], rows=[K.KITS['shs']['rows'][0],
                                                   K.KITS['shs']['rows'][1],
                                                   K.KITS['shs']['rows'][3]])

    r = Route(522, W, H, theme='snow', kit='shs3', base='.')
    m = r.m
    # Smooth pale frosted glass-sheet turf (18442..18445) + silver frosted tall grass (18446, encounter tag 2)
    m.grass = [[18442, 18443], [18444, 18445]]
    m.tall = 18446
    m.STAIRS = K.STAIRS_STONE
    m.grass2 = None
    m.auto['e'] = ('KristilineDirt', 'rejuvenation')
    m.keep_under = 'de'

    rng = random.Random(5222)

    # ---- 1. Heightmap: two crisp unbroken frosted orchard terraces climbing NE ----
    for y in range(H):
        for x in range(W):
            # Upper NE Pruett homestead terrace (h=2): clean unbroken west wall at x=25, south lip at y=14..15
            if x >= 25 and y <= (15 if x <= 31 else 14):
                m.ht[y, x] = 2
                continue
            # Mid central/east orchard terrace (h=1): clean unbroken west wall at x=15, gentle south lip around y=29
            if x >= 15 and y <= (29 if x <= 30 else 30):
                m.ht[y, x] = 1

    # Clean square shelves around the two stone stairs & key landings
    m.ht[26:30, 17:22] = 1
    m.ht[30:35, 16:23] = 0
    m.ht[11:15, 32:37] = 2
    m.ht[15:20, 31:38] = 1
    # Ensure Cracked tree M (23, 16), Glassed Wurmple (24, 18), and Glass farmhand (27, 13) sit cleanly flat
    m.ht[15:19, 21:25] = 1
    m.ht[11:16, 25:32] = 2
    # Ensure D1 NE nook (38, 1..4) and Carbink (38, 6) are flat on h=2
    m.ht[0:10, 35:43] = 2
    # Ensure SW entry + Veil + pond + NW grove are cleanly h=0
    m.ht[31:40, 0:15] = 0
    m.ht[0:32, 0:15] = 0

    # ---- 2. Stone stairs cutting the two terrace cliffs ----
    CK.stair(r, 18, 29, w=3, h=1)       # South orchard stair: rows 29..31, top 28, bottom 32 (Chime post 19,33!)
    CK.stair(r, 33, 14, w=3, h=2)       # Upper homestead stair: rows 14..16, top 13, bottom 17

    # ---- 3. Still Mirror Pond on lower west orchard ----
    px, py = 9, 23
    for y in range(19, 28):
        for x in range(4, 15):
            dx = (x - px) / 4.1
            dy = (y - py) / 2.7
            if dx * dx + dy * dy + 0.16 * (vnoise(x, y, 5221, 3.0) - 0.5) <= 1.0:
                if m.ht[y, x] == 0:
                    m.cls[y, x] = 'w'
    # Majority smooth pond shoreline for clean autotile edges
    for _ in range(2):
        cur = (m.cls == 'w')
        pad = np.pad(cur, 1)
        nb = sum(np.roll(np.roll(pad, dy, 0), dx, 1)[1:-1, 1:-1] for dy in (-1, 0, 1) for dx in (-1, 0, 1)) - cur
        m.cls[~cur & (nb >= 5) & (m.ht == 0)] = 'w'
        m.cls[cur & (nb <= 3)] = '.'

    # ---- 4. Orchard alleys & paths ----
    # Living dirt lane through SW gate right up to the Veil (soft organic country lane, not a rigid box)
    for x in range(0, 5):
        for y in (36, 37):
            m.cls[y, x] = 'e'
            r.road_mask[y, x] = True
    for x in (0, 1, 2):
        m.cls[38, x] = 'e'
        r.road_mask[38, x] = True

    def lane(pts, width=2, cls='d'):
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            steps = max(abs(x1 - x0), abs(y1 - y0), 1) * 3
            for i in range(steps + 1):
                t = i / float(steps)
                cx = x0 + (x1 - x0) * t
                cy = y0 + (y1 - y0) * t
                for yy in range(int(cy) - 2, int(cy) + 3):
                    for xx in range(int(cx) - 2, int(cx) + 3):
                        if not m.inb(xx, yy):
                            continue
                        if (xx - cx) ** 2 + (yy - cy) ** 2 <= (width * 0.60) ** 2:
                            if m.cls[yy, xx] != 'w':
                                m.cls[yy, xx] = cls
                                r.road_mask[yy, xx] = True

    # Lower lane from Veil to South Stair + West Pond & Biscuit Alley
    lane([(5, 37), (8, 35), (13, 35), (19, 34), (19, 32)], width=2.0)
    lane([(8, 35), (5, 30), (4, 24), (4, 16), (8, 13), (11, 13)], width=1.7)
    # Mid terrace lanes: South Stair -> Wurmple -> East Stair + SE Cracked tree H / Glass apple + NW mid alley
    lane([(19, 28), (19, 24), (24, 21), (24, 18), (30, 19), (34, 17)], width=2.0)
    lane([(19, 24), (18, 20), (22, 17), (23, 16)], width=1.6)
    lane([(24, 21), (30, 24), (35, 25), (38, 24)], width=1.8)
    # Upper homestead courtyard: East Stair -> Foal -> Pruett House -> Farmhand -> Carbink -> D1 Nook
    lane([(34, 13), (34, 10), (30, 10), (30, 9)], width=1.9)
    lane([(30, 12), (27, 13)], width=1.6)
    lane([(34, 10), (38, 7), (38, 4)], width=1.7)
    # Keep living SW entry cleanly on 'e'
    for x in range(0, 5):
        for y in (36, 37):
            m.cls[y, x] = 'e'
    for x in (0, 1, 2):
        m.cls[38, x] = 'e'

    # ---- 5. Reserve ALL sacred event / puzzle / trial / building coordinates ----
    # Exact baseline coordinates preserved 100%!
    P = {
        'juno': [2, 35],
        'larch': [2, 38],
        'farmhand': [27, 13],
        'apple': [38, 24],
        'wurmple': [24, 18],
        'carbink': [38, 6],
        'biscuit': [11, 13],
        'house_sign': [30, 8],
    }
    must_keep = [
        (0, 36), (0, 37), (0, 38), (1, 37), (1, 38), (2, 37), (3, 37),
        (4, 35), (4, 36), (4, 37), (5, 36), (5, 37), (6, 37), (7, 37),
        (2, 35), (2, 38),
        (19, 33), (19, 32), (19, 28),          # D1 Chime post + South stair
        (4, 16), (23, 16), (35, 25),           # D1 Cracked trees L, M, H
        (38, 4), (38, 3), (38, 2), (38, 1),    # D1 Glass hedge + Lost satchel alcove
        (8, 34), (18, 20), (30, 12), (34, 10), # Trial overlay Glass Foal coords
        (27, 13), (38, 24), (24, 18), (38, 6), (11, 13),
        (30, 9), (30, 10), (29, 9), (31, 9),   # Pruett house doorstep
        (34, 13), (34, 17),                    # Upper stair landings
    ]
    for x, y in must_keep:
        r.road_mask[y, x] = True
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                xx, yy = x + dx, y + dy
                if m.inb(xx, yy) and (x, y) not in ((38, 1), (38, 2), (38, 3)):
                    r.road_mask[yy, xx] = True

    # ---- 6. Outer crystal forest border & sealed D1 NE alcove ----
    for y in range(H):
        for x in range(W):
            if r.road_mask[y, x] or m.cls[y, x] in 'wde':
                continue
            if _in_living(x, y):
                continue
            if x == 38 and y <= 4:
                continue
            n_edge = 4 + int(round(1.6 * vnoise(x, 1, 21, 4.5)))
            s_edge = H - 4 - int(round(1.5 * vnoise(x, 2, 23, 4.5)))
            e_edge = W - 4 - int(round(1.6 * vnoise(1, y, 22, 4.5)))
            w_edge = 3 + int(round(1.4 * vnoise(3, y, 24, 4.5)))
            # Keep Pruett farmhouse yard (26..35, 2..11) clear of north woods
            if 26 <= x <= 35 and y <= 11:
                if y < 2:
                    m.cls[y, x] = 'T'
                continue
            # Tightly seal the D1 NE alcove sides around x=38, y=0..3!
            if y <= 3 and x in (36, 37, 39, 40):
                m.cls[y, x] = 'T'
                continue
            if y == 0 and x == 38:
                m.cls[y, x] = 'T'
                continue
            if y < n_edge or x > e_edge or (y > s_edge and x >= 6) or (x < w_edge and y < 30):
                m.cls[y, x] = 'T'

    # ---- 7. Frosted tall grass pockets tucked between orchard rows ----
    grass_pockets = [
        (8, 8, 4.8, 3.0),       # NW orchard wild drift
        (12, 18, 2.8, 2.8),     # East of pond
        (11, 30, 3.6, 2.4),     # SW frosted hollow
        (20, 7, 4.2, 3.4),      # North-center mid terrace
        (21, 13, 3.0, 2.4),     # Mid-north drift
        (29, 27, 4.4, 2.4),     # South-east mid terrace
        (36, 21, 3.0, 2.2),     # East bluff pocket
        (10, 37, 3.2, 1.8),     # South lower hollow
    ]
    for cx, cy, rx, ry in grass_pockets:
        for y in range(max(2, int(cy - ry - 1)), min(H - 2, int(cy + ry + 2))):
            for x in range(max(2, int(cx - rx - 1)), min(W - 2, int(cx + rx + 2))):
                if m.cls[y, x] == '.' and not r.road_mask[y, x] and not _in_living(x, y):
                    d2 = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
                    if d2 + 0.25 * (vnoise(x, y, 5229, 2.8) - 0.5) <= 1.0:
                        m.cls[y, x] = 't'

    # ---- 8. Paint terrain base (ground, autotiles, frosted cliffs, stone stairs) ----
    m.paint_ground()
    m.autotiles()
    m.cliffs()
    m.paint_stairs()

    # Subtle snow-drift variation on frosted glass ground (breaks up flat expanses gently)
    for y in range(H):
        for x in range(W):
            if m.cls[y, x] == '.' and not _in_living(x, y) and not m.cliff[y, x]:
                if vnoise(x, y, 5225, 3.4) > 0.62:
                    m.L[0, y, x] = 10395   # Kristiline crystalline snow drift

    # Delicate glass-sheen sparkles floating lightly on Still Mirror Pond
    for y in range(H):
        for x in range(W):
            if m.cls[y, x] == 'w' and (x * 7 + y * 13) % 11 == 0:
                m.L[2, y, x] = 25824 + ((x + y) % 3)

    # ---- 9. Living Sheridan green pocket west of the Bleed Veil ----
    for y in range(28, H):
        for x in range(0, 5):
            if _in_living(x, y) or (x <= 3 and y >= 29):
                if m.cls[y, x] in '.tT':
                    m.L[0, y, x] = K.SH_GRASS[y & 1][x & 1]
                    if m.cls[y, x] == 't':
                        m.L[1, y, x] = K.SH_TALL
                    elif not r.road_mask[y, x] and (x * 7 + y * 11) % 4 == 0:
                        m.L[1, y, x] = K.DECOR_SH['flowers'][(x + y) % 4]
                    elif not r.road_mask[y, x] and (x * 5 + y * 3) % 3 == 0:
                        m.L[1, y, x] = K.DECOR_SH['green'][(x + y) % len(K.DECOR_SH['green'])]

    # ---- 10. Place Pruett Farmhouse, landmarks, gateposts, and Veil ----
    # Frosted Pruett Farmhouse (kf_aframe 5x7, door at [2, 6] -> (30, 8) exact!)
    m.stamp('kf_aframe', 28, 2)
    # Stone bench & frosted orchard barrels beside the farmhouse
    m.stamp('pf_stonebench', 35, 9)
    m.stamp('hb_barrels', 26, 7)
    m.stamp('hb_barrel', 33, 7)
    # Stone doorstep apron under (30, 9)
    m.L[0, 9, 29] = 10395; m.L[0, 9, 30] = 10395; m.L[0, 9, 31] = 10395

    # Mossy living stone gateposts framing the Bleed Veil (x=4, y=33..34 and y=38..39; leaves 35,36,37 open!)
    m.stamp('nr_col', VX, 33)
    m.stamp('nr_col', VX, 38)

    # Living green oaks, pines & shrubs framing the SW pocket cleanly (zero overlap)
    m.stamp('tr_oak2', 0, 29)
    m.stamp('tr_pine', 3, 29)
    m.stamp('tr_pine', 0, 32)
    m.stamp('nt_bush0', 3, 33)
    m.stamp('nt_bush1', 0, 39)

    # Single pale fallen glass-frosted branch resting beside the Still Mirror Pond
    m.stamp('nt_birch_h', 8, 20)

    # ---- 11. Sealed D1 NE Alcove crystal walls (guaranteeing (38,3) blocks (38,1..2)) ----
    m.stamp('nt_pine_purp', 36, 0)
    m.stamp('nt_pine_blue', 39, 0)
    m.stamp('cr_purple_t', 37, 2)
    m.stamp('cr_teal_t', 39, 2)
    m.stamp('nt_pine_blue', 37, 0)
    m.stamp('cr_blue_c', 38, 0)
    for yy in range(1, 5):
        m.taken[yy, 38] = False

    # ---- 12. Reserve corridors before tree placement ----
    reserved = set(must_keep) | {(38, 1), (38, 2), (38, 3), (38, 4), (30, 8)}
    for rx, ry in reserved:
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if m.inb(rx + dx, ry + dy):
                    if (rx, ry) in ((38, 1), (38, 2), (38, 3), (38, 4)) and dx != 0:
                        continue
                    r.road_mask[ry + dy, rx + dx] = True

    def can_put_tree(nm, tx, ty, allow_border=False, strict_road=True):
        s = STAMPS[nm]
        w, h = s['w'], s['h']
        if tx < 0 or ty < 0 or tx + w > W or ty + h > H:
            return False
        # Do not place frosted crystal trees inside living SW pocket
        if tx < 5 and ty + h > 30:
            return False
        # Do not touch Pruett house or D1 alcove corridor (38, 1..4)
        if tx < 34 and tx + w > 27 and ty < 10 and ty + h > 1:
            return False
        if tx <= 38 < tx + w and ty <= 4 and ty + h > 0:
            return False
        h0 = int(m.ht[min(H - 1, ty + h - 1), min(W - 1, tx + w // 2)])
        # Check bottom 2 rows (solid trunk/base footprint) for collisions, roads, cliffs, water
        for dy in range(max(0, h - 2), h):
            for dx in range(w):
                xx, yy = tx + dx, ty + dy
                if m.taken[yy, xx] or m.cliff[yy, xx]:
                    return False
                if m.cls[yy, xx] in 'wde':
                    return False
                if strict_road and r.road_mask[yy, xx]:
                    return False
                if (xx, yy) in reserved:
                    return False
                if not allow_border and m.ht[yy, xx] != h0:
                    return False
        # Prevent tall crowns from overwriting already-placed trunks OR the two stone staircases
        for dy in range(0, max(0, h - 2)):
            for dx in range(w):
                xx, yy = tx + dx, ty + dy
                if m.bodym[yy, xx]:
                    return False
                if (18 <= xx <= 20 and 29 <= yy <= 31) or (33 <= xx <= 35 and 14 <= yy <= 16):
                    return False
        return True

    # ---- 13. Place Signature Frosted Glass Apple Orchard Rows FIRST (NW, Mid-North, SE, & D1 Anchors!) ----
    # Deliberate spaced rows of frosted apple trees (kf_tree, nt_tree_blue, nt_tree_purp, nt_deadtree)
    # including anchor trees beside D1 Cracked Trees L (4,16), M (23,16), and H (35,25)!
    hero_orchard = [
        # NW Orchard Grove (around Biscuit (11,13) & Cracked tree L (4,16))
        ('kf_tree', 5, 5), ('nt_tree_blue', 10, 6), ('nt_tree_purp', 5, 11),
        ('kf_tree', 10, 15), ('nt_deadtree', 6, 16),
        # Mid-North Orchard Terrace (around Cracked tree M (23,16) & Wurmple (24,18))
        ('kf_tree', 17, 5), ('nt_tree_purp', 21, 5), ('nt_tree_blue', 17, 10),
        ('kf_tree', 20, 10), ('nt_tree_purp', 17, 15), ('nt_deadtree', 21, 14),
        # Central & SE Orchard Terrace (around Cracked tree H (35,25) & Glass apple (38,24))
        ('kf_tree', 25, 22), ('nt_tree_blue', 29, 21), ('kf_tree', 33, 19),
        ('nt_tree_purp', 37, 18), ('nt_tree_blue', 30, 25),
        # South lower frosted grove
        ('kf_tree', 11, 29), ('nt_tree_purp', 8, 28),
    ]
    placed_orchard = 0
    for nm, ax, ay in hero_orchard:
        if can_put_tree(nm, ax, ay, allow_border=False, strict_road=False):
            m.stamp(nm, ax, ay)
            placed_orchard += 1
            # Drop gleaming ruby crystal glass apple beside select trunks on free grass
            s = STAMPS[nm]
            for dx, dy in ((0, s['h']), (s['w'] - 1, s['h']), (-1, s['h'] - 1)):
                rx, ry = ax + dx, ay + dy
                if m.inb(rx, ry) and m.cls[ry, rx] == '.' and not m.taken[ry, rx] and not r.road_mask[ry, rx] and not m.cliff[ry, rx]:
                    if (rx * 3 + ry * 5) % 2 == 0:
                        m.stamp('cr_red_c', rx, ry)
                        break

    # ---- 14. Lush Organic Multi-Species Crystal Canopy Border (N, E, S, NW — ZERO soldier rows!) ----
    border_big = ['nt_tree_blue', 'nt_tree_purp', 'kf_tree', 'nt_tree_blue', 'nt_tree_purp']
    border_small = ['nt_pine_blue', 'nt_pine_purp', 'nt_pine_blue', 'nt_pine_purp', 'nt_tree_purp']
    pts_border = []
    for ty in range(0, H - 2, 2):
        for tx in range(0, W - 2, 2):
            jx = (tx * 7 + ty * 13) % 2
            jy = (tx * 11 + ty * 5) % 2
            pts_border.append((min(W - 3, tx + jx), min(H - 3, ty + jy)))
    rng.shuffle(pts_border)
    for tx, ty in pts_border:
        cx, cy = min(W - 1, tx + 1), min(H - 1, ty + 2)
        if m.cls[cy, cx] != 'T':
            continue
        if _in_living(cx, cy) or (cx <= 4 and cy >= 28):
            continue
        nm = border_big[(tx * 5 + ty * 9) % len(border_big)]
        if can_put_tree(nm, tx, ty, allow_border=True):
            m.stamp(nm, tx, ty)
        else:
            nm2 = border_small[(tx * 3 + ty * 7) % len(border_small)]
            if can_put_tree(nm2, tx, ty, allow_border=True):
                m.stamp(nm2, tx, ty)

    # Organic infill for any remaining border gaps
    gap_pts = [(tx, ty) for ty in range(0, H - 2) for tx in range(0, W - 1) if m.cls[ty + 2, tx] == 'T']
    rng.shuffle(gap_pts)
    for tx, ty in gap_pts:
        if m.taken[ty + 2, tx] or (tx <= 4 and ty >= 27):
            continue
        nm = rng.choice(['nt_pine_blue', 'nt_pine_purp'])
        if can_put_tree(nm, tx, ty, allow_border=True):
            m.stamp(nm, tx, ty)

    # ---- 15. Additional Orchard Row Fillers ----
    for row_i, y0 in enumerate(range(4, 33, 4)):
        for x0 in range(5 + (row_i % 2) * 2, 39, 4):
            k = (x0 * 11 + y0 * 7) % 10
            if k == 0:
                nm = 'nt_deadtree'
            elif k in (1, 2, 3, 4):
                nm = 'kf_tree'
            elif k in (5, 6, 7):
                nm = 'nt_tree_blue'
            else:
                nm = 'nt_tree_purp'
            if can_put_tree(nm, x0, y0, allow_border=False):
                m.stamp(nm, x0, y0)
                placed_orchard += 1

    print('  522 orchard trees placed:', placed_orchard)

    # ---- 16. Crystal spires, Bleed shards, fallen ruby glass apples, & frosted undergrowth ----
    spires = [
        ('gd_spire', 25, 3), ('cr_purple_t', 34, 5), ('cr_teal_t', 26, 9),
        ('gd_shard0', 13, 21), ('gd_shard1', 5, 22), ('cr_teal_t', 13, 25),
        ('gd_spire', 22, 26), ('cr_purple_t', 15, 33), ('gd_shard0', 31, 18),
        ('cr_teal_t', 39, 26), ('nt_log', 12, 31),
    ]
    for nm, sx, sy in spires:
        s = STAMPS[nm]
        ok = True
        for dy in range(s['h']):
            for dx in range(s['w']):
                xx, yy = sx + dx, sy + dy
                if not m.inb(xx, yy) or m.taken[yy, xx] or m.cliff[yy, xx] or r.road_mask[yy, xx] or m.cls[yy, xx] in 'wdeT':
                    ok = False
        if ok:
            m.stamp(nm, sx, sy)

    # Scatter walkable frost-flowers (9725), frosted twigs (10620), bleed sparkles (25824..25826),
    # and sparse solid crystal clusters (avoiding cluttering Chime post (19,33))
    for y in range(2, H - 2):
        for x in range(2, W - 2):
            if _in_living(x, y) or m.taken[y, x] or m.cliff[y, x]:
                continue
            if abs(x - 19) <= 3 and abs(y - 33) <= 1:
                continue   # keep Chime post (19,33) framed cleanly
            if m.cls[y, x] == '.' and m.L[1, y, x] == 0 and m.L[2, y, x] == 0:
                rv = rng.random()
                if not r.road_mask[y, x] and rv < 0.032:
                    m.stamp(rng.choice(['cr_red_c', 'cr_red_c', 'cr_teal_c', 'cr_blue_c', 'gd_shard2']), x, y)
                elif rv < 0.16:
                    m.L[1, y, x] = rng.choice([9725, 9725, 10620])
                elif rv < 0.24:
                    m.L[2, y, x] = rng.choice([25824, 25825, 25826])
            elif m.cls[y, x] == 'd' and m.L[2, y, x] == 0 and rng.random() < 0.06:
                m.L[2, y, x] = rng.choice([25824, 25825, 25826])

    # ---- 17. Commit all stamps & post-paint fixes (Pruett base + Bleed Veil!) ----
    m.put_stamps()
    # Patch kf_aframe bottom-left wall tile (28, 8) with solid frost-base tile 9232
    m.L[1, 8, 28] = 9232
    # Guarantee (38, 1..3) D1 nook corridor is clear of stray blocking tiles on L1/L2 (keeping stone road at y=4!)
    for yy in range(1, 4):
        m.L[1, yy, 38] = 0
        m.L[2, yy, 38] = 0
    # Guarantee every critical walkable coordinate is unobstructed
    for rx, ry in [(4, 35), (4, 36), (4, 37), (1, 37), (2, 37), (3, 37), (5, 37), (6, 37),
                   (4, 16), (23, 16), (35, 25), (19, 33), (8, 34), (18, 20), (30, 12), (34, 10),
                   (27, 13), (38, 24), (24, 18), (38, 6), (11, 13), (30, 9)]:
        if m.L[1, ry, rx] in (22895, 22915, 22880, 10551, 10371):
            m.L[1, ry, rx] = 0

    # Shimmering Bleed Veil curtain right down x = VX (4) across the living/glass divide (y = 30..39)
    veil_tiles = [26048, 26049, 26050]
    bleed_tiles = [25824, 25825, 25826]
    for y in range(30, H):
        if y not in (33, 34, 38, 39):
            m.L[2, y, VX] = veil_tiles[y % 3]
        if y >= 30 and m.L[2, y, VX + 1] == 0:
            m.L[2, y, VX + 1] = bleed_tiles[y % 3]

    # ---- 16. Events (100% contract-preserved from story/20_SCRIPT_CH0-2.md, "Map 522") ----
    E = []
    E.append({'type': 'warp', 'name': 'To Windfall Row', 'at': [0, 37], 'link': 'R2_ORCHARD', 'arrive': [1, 37, 'right']})
    E.append({'type': 'warp', 'name': 'To Windfall Row b', 'at': [0, 36], 'to': {'map': 521, 'x': 60, 'y': 22, 'dir': 'left'}})
    E.append({'type': 'warp', 'name': 'To Windfall Row c', 'at': [0, 38], 'to': {'map': 521, 'x': 60, 'y': 23, 'dir': 'left'}})
    E.append(fog_event('prismfall_glass', 58, 1, 200, 2, 1))
    intro = [
        {'script': 'pfm_juno_part'},   # she stops at the gate: the map's own Juno event takes over
        "(Rows of apple trees turned to clear glass. Glass apples chime in the wind. The air at the gate shimmers like heat.)",
        say('JUNO', 'sad', "There. That was the Pruetts'. It went last winter, in one night."),
        say('JUNO', 'neutral', "It's pretty, isn't it? I hate that it's pretty."),
        {'se': 'Voltorb Flip tile'}, "(A squeak from inside. A Skwovet is clinging to a glass branch.)",
        say('JUNO', 'panic', "Biscuit! Biscuit, come OUT!"),
        {'move': {'who': 'Juno', 'route': ['right', 'wait 4']}},
        "\\pf[JUNO,panic,shock]Juno: Ow— no. No. My skin's burning. I can't.",
        {'move': {'who': 'Juno', 'route': ['left']}},
        say('JUNO', 'sad', "That's the Veil. Nobody can cross one. You just... can't. Your body won't."),
        "(You step forward.)",
        {'move': {'who': -1, 'route': ['right', 'right', 'right']}}, {'wait': 40},
        "\\pf[JUNO,shocked,shock]Juno: ...How are you DOING that?",
        {'choices': ["I don't know.", "It doesn't hurt.", "..."], 'cancel': 3, 'branches': [[], [], []]},
        say('JUNO', 'shocked', "Doesn't it— aren't you— your HAIR isn't even standing up!"),
        setk('VEIL'), {'selfswitch': ['A', True]}]
    E.append({'type': 'event', 'name': 'Orchard arrival', 'at': [1, 38], 'pages': [
        {'cond': {'switch': 'CH1_K1_DONE'}, 'trigger': 'autorun', 'commands': intro}, {'cond': {'self': 'A'}}]})
    lecture = [
        show_larch(), {'wait': 20},
        "(Professor Larch is standing next to Juno with a notebook. She has clearly run the whole way.)",
        say('LARCH', 'neutral', "So. You walked through a Bleed Veil."),
        say('LARCH', 'neutral', "Into a Bleed zone. On your first day. To fetch a Skwovet."),
        {'choices': ["It was stuck."], 'cancel': 1, 'branches': [[]]},
        "\\pfb[LARCH,angry,anger,Professor Larch]Larch: IT LIVES IN A TREE. IT IS ALWAYS STUCK. THAT IS ITS ENTIRE ARRANGEMENT WITH TREES.",
        say('JUNO', 'happy', "Technically Skwovet are scansorial, so—"),
        say('LARCH', 'angry', "Juno."),
        "\\pf[JUNO,panic,sweat]Juno: Shutting up!",
        say('LARCH', 'crying', "Your mother wrote me one instruction. One! \"Keep them out of trouble, Imelda.\" It has been NINE HOURS."),
        say('LARCH', 'crying', "I'm not crying. It's the tea. The tea is very strong."),
        {'wait': 30}, "(Larch looks at the sleeping swarm in the glass trees, then at you.)",
        say('LARCH', 'neutral', "...They calmed down. When you went near them."),
        say('LARCH', 'neutral', "Well. That's that, then."),
        "(Larch writes something in the notebook.)",
        say('LARCH', 'neutral', "Listen to me, both of you. Never take a tinted person past a Veil. Never. It isn't pain that stops them. It's the body knowing."),
        say('LARCH', 'neutral', "And you. This is Lecture One. I'm numbering them. I have a feeling."),
        {'if': 'GameData::Item.exists?(:FIELDNOTES)', 'then': [{'script': 'pbReceiveItem(:FIELDNOTES)'}],
         'else': ["\\me[Key item get]You received the FIELD NOTES!\\nProfessor Larch's field encyclopedia. It fills in as you meet new fields."]},
        {'switch': ['CH1_ORCHARD_DONE', True]}, {'script': 'pf_bond_add(:JUNO, 1)'},
        {'script': 'pfm_juno_join(:errand)'},   # she falls in again outside (hidden on 522 while she waits at the gate)
        "QUEST: \"Biscuit\" - bring Biscuit home to Wenna at Hale's Bramble."]
    for i, y in enumerate((35, 36, 37)):
        E.append({'type': 'event', 'name': 'Bleed Veil %d' % (i + 1), 'at': [VX, y], 'pages': [
            {'cond': {'switch': 'CH1_K1_DONE'}, 'trigger': 'touch', 'through': True, 'commands': [
                {'if': key('BISCUIT') + ' && ' + key('SWARM') + ' && !$game_switches[105]', 'then': lecture,
                 'else': [{'if': key('VEIL') + ' && !' + key('VEILMSG'), 'then': ["(The shimmer slides over you like warm water. Nothing else happens.)", setk('VEILMSG')], 'else': []}]}]},
            {'cond': {'switch': 'CH1_ORCHARD_DONE'}, 'through': True}]})
    E.append({'type': 'event', 'name': 'Juno', 'at': P['juno'], 'pages': [
        {'cond': {'switch': 'CH1_K1_DONE'}, 'graphic': {'sprite': 'trainer_RIVAL2', 'dir': 'right'}, 'commands': [
            {'if': key('VEIL') + ' && $game_player.x >= %d' % VX, 'then': [
                say('JUNO', 'neutral', "Can you pull me through? Just for a second? I only want to grab him."),
                {'choices': ["No. Stay there.", "Take her hand."], 'cancel': 1, 'branches': [
                    [say('JUNO', 'sad', "...Right. Yes. The Professor did say never. Sorry. Go on, I'll shout directions.")],
                    [{'script': 'Prismfall.checkpoint(false)'}, say('JUNO', 'happy', "On three. One, two—"),
                     {'se': 'Anim/Ice1'}, "(Glass rings. Juno goes clear from the fingertips up.)", {'wait': 60},
                     say('JUNO', 'shocked', "\\PN, I can't feel my—"), {'script': 'Prismfall.game_over(:GO_ORCHARD)'}]]}],
             'else': [say('JUNO', 'sad', "Biscuit's in there somewhere. Past the farmhand. Please be careful.")]}]},
        {'cond': {'switch': 'CH1_ORCHARD_DONE'}, 'graphic': {'sprite': 'trainer_RIVAL2', 'dir': 'right'},
         'commands': [say('JUNO', 'happy', "You walked through the Bleed like it was fog. Nobody does that. NOBODY.")]},
        {'cond': {'var': ['STORY_CHAPTER', 2]}}]})
    E.append({'type': 'event', 'name': 'Professor Larch', 'at': P['larch'], 'pages': [
        {'cond': {'switch': 'CH1_K1_DONE'}, 'commands': []},
        {'cond': {'self': 'A'}, 'graphic': {'sprite': 'trainer_PROFESSOR', 'dir': 'right'}, 'commands': [say('LARCH', 'neutral', "Lecture One stands. Out. Now. Home.")]},
        {'cond': {'switch': 'CH1_ORCHARD_DONE'}, 'graphic': {'sprite': 'trainer_PROFESSOR', 'dir': 'right'},
         'commands': [say('LARCH', 'neutral', "Field safety, rule one, underlined three times. I'll be at the station writing it four times.")]}]})
    E.append({'type': 'event', 'name': 'Glass farmhand', 'at': P['farmhand'], 'pages': [
        {'graphic': {'sprite': 'NPC 03', 'dir': 'down'}, 'move': 'fixed', 'commands': [
            "A man made of glass, mid-step, a glass basket on his arm. His mouth is open. He was calling someone.", {'selfswitch': ['A', True]}]},
        {'cond': {'self': 'A'}, 'graphic': {'sprite': 'NPC 03', 'dir': 'down'}, 'move': 'fixed', 'commands': [
            "Inside the glass, very faintly, his eyes are moving."]}]})
    E.append({'type': 'event', 'name': 'Glass apple', 'at': P['apple'], 'pages': [
        {'graphic': {'sprite': 'Object ball', 'dir': 'down'}, 'commands': [
            {'if': 'GameData::Item.exists?(:GLASSAPPLE)', 'then': [{'script': 'pbReceiveItem(:GLASSAPPLE)'}],
             'else': ["You found a GLASS APPLE.\\nIt rings when you flick it. Don't bite it.", {'script': '$player.money += 500'},
                      "(You sell it to yourself for ₽500. [item data missing: GLASSAPPLE])"]},
            {'selfswitch': ['A', True]}]}, {'cond': {'self': 'A'}}]})
    E.append({'type': 'event', 'name': 'Glassed Wurmple', 'at': P['wurmple'], 'pages': [
        {'cond': {'switch': 'CH1_K1_DONE'}, 'graphic': {'sprite': 'Followers/WURMPLE', 'dir': 'down'}, 'move': 'fixed', 'commands': [
            "It hisses. Its body grinds like a jar of marbles.",
            {'script': 'setBattleRule("field", :BLEED)\nsetBattleRule("canLose")\nWildBattle.start(:WURMPLE, 6)'},
            "FIELD NOTES: THE BLEED - unstable. Borrows effects from other fields. Do not trust the ground.",
            "The Wurmple stops grinding. It looks at you. Then it curls up against your shoe and goes to sleep.",
            "The rest of the swarm settles in the branches, one by one.", setk('SWARM'), {'selfswitch': ['A', True]}]},
        {'cond': {'self': 'A'}, 'graphic': {'sprite': 'Followers/WURMPLE', 'dir': 'down'}, 'move': 'fixed', 'through': True,
         'commands': ["It's asleep. Its crystal hums, very quietly, in time with your breathing."]}]})
    E.append({'type': 'event', 'name': 'Wild Carbink', 'at': P['carbink'], 'pages': [
        {'graphic': {'sprite': 'Followers/CARBINK', 'dir': 'left'}, 'commands': [
            {'if': 'pfm_gym_won?(:LEADER_TAMSIN)', 'then': [
                "It is licking a glass tree. It seems very happy about the whole situation.",
                {'script': 'setBattleRule("field", :BLEED)\nWildBattle.start(:CARBINK, 20)'}, {'selfswitch': ['A', True]}],
             'else': ['It licks a glass tree, sees you, and phases into the glass.']}]},
        {'cond': {'self': 'A'}}]})
    E.append({'type': 'event', 'name': 'Lost Skwovet', 'at': P['biscuit'], 'pages': [
        {'cond': {'switch': 'CH1_K1_DONE'}, 'graphic': {'sprite': 'Followers/SKWOVET', 'dir': 'down'}, 'move': 'random', 'commands': [
            "Biscuit has stuffed his cheeks with glass apple seeds. He rattles when he moves.",
            "He climbs onto your head. This is apparently how this works.", setk('BISCUIT'), {'selfswitch': ['A', True]}]},
        {'cond': {'self': 'A'}}]})
    E.append({'type': 'sign', 'at': P['house_sign'], 'post': False, 'name': 'Pruett house',
              'text': "The Pruett house. The door is glass, and so is the key in it. A child's coat hangs on the peg inside, perfectly clear."})

    m.events = E
    head = {
        '_file': '522_glassed_orchard.yaml',
        'id': 522,
        'biome': 'bleed',
        'name': 'The Glassed Orchard',
        'bgm': 'Route 2',
        'parent': 521,
        'field': 'BLEED',
        'tone': [-14, -18, 22, 46],
        'metadata': {'ShowArea': True, 'SnapEdges': True, 'MapPosition': [0, 15, 22], 'BattleBack': 'field'},
        'rubric': True,
    }
    m.write(522, head, "# The Glassed Orchard (522). WRITTEN BY layouts/orchard.py - edit that, not this file.\n")
    print('  wrote 522_glassed_orchard.yaml (ts=52 PF Rejuv Snow)')


if __name__ == '__main__':
    build()
