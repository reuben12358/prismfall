#!/usr/bin/env python3
"""Ferrow's Landing (100) on the PF Rejuv sheet (tileset 51 "PF Rejuv Coast"), 68x60.  MAPGEN 2h.
Spring on the south coast: Goldenleaf's timber-and-stone houses on Sheridan's green bluff, Akuwa's grass-capped sea
cliffs and white beach, blossom trees.  Three levels: Tidewatch hill (NE, Larch's station), the village bluff (gravel
street from the Ferrymen's Mile lane down to the square, side streets to the lighthouse headland and the east houses), and the
harbour beach with the ferry pier (x 33-35, water from row 48: the docking choreography of story_early depends on it).
The Dovetail is moored east of the pier.  Story events come from layouts/story_early.py; this script seats them.
Run: python3 -I layouts/ferrow_rj.py && python3 -I build.py 100"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import rkit as K
from rkit import C, STAMPS
from terrain import vnoise
import story_early as SE
W, H = 68, 60
SHORE = 48
PIER = (33, 35)


def lip(x):
    """last row of the village bluff (h=1) in column x: the harbour is a shallow bay cut into the bluff"""
    if 24 <= x <= 46: return 35
    if 47 <= x <= 52: return 36
    if 18 <= x <= 23: return 37
    if x < 18: return 45 + int(round(1.0 * math.sin(x / 3.0)))
    return 43 + int(round(1.5 * math.sin(x / 4.0) + 1.5 * (vnoise(x, 0, 4, 5.0) - 0.5)))


def shore(x):
    if 18 <= x <= 52: return SHORE + (0 if 21 <= x <= 49 else -1)
    return lip(x) + 2


def hill(x, y):
    """Tidewatch hill (h=2) in the north-east: a clean south face at row 16, west side at x 44"""
    return x >= 44 and y <= (16 if x < 61 else 18)


def terrace(x, y):
    """the Center terrace (h=2) in the north-west, a wooded knoll (h=3) behind it"""
    if (x <= 9 and y <= 18) or (10 <= x <= 30 and y <= 20): return 2
    return 1


TREES = ['tr_oak', 'tr_oak2', 'tr_pink', 'tr_oak', 'tr_pink']
WHARF = (21, 49, 46, 47)                   # x0, x1, y0, y1: the timber wharf along the waterline


def build(preview=None):
    m = K.RMap(W, H, 51, 100, water='Ocean', kit={1: 'ak', 2: 'sh', 3: 'sh'})
    m.keep_under = 'sgd'
    # ---------------------------------------------------------------- terrain: bluff, hill, terrace, beach, sea
    for x in range(W):
        for y in range(H):
            if y <= lip(x): m.ht[y, x] = 1
            if hill(x, y): m.ht[y, x] = 2
            if terrace(x, y) >= 2: m.ht[y, x] = terrace(x, y)
            if y >= shore(x): m.cls[y, x] = 'w'
            elif y > lip(x): m.cls[y, x] = 's'
    for x in range(W):                      # deep water offshore, a smooth band
        for y in range(H):
            if m.cls[y, x] == 'w' and y >= 55 + 3 * vnoise(x, 0, 5, 9.0) and not (PIER[0] - 2 <= x <= PIER[1] + 2): m.cls[y, x] = 'W'
    for y in range(H):                      # woods: the knoll, the back of the terrace, the hill's east end, the edges
        for x in range(W):
            if m.ht[y, x] < 1: continue
            nw = m.ht[y, x] == 3 or (m.ht[y, x] == 2 and x < 31 and (y < 2 + 2 * vnoise(x, 0, 9, 4.0) or x < 3))
            ne = m.ht[y, x] == 2 and x >= 44 and (x > 61 + 2 * vnoise(0, y, 8, 4.0) or (y < 1 and x > 59))
            east = x > 64 + 2 * vnoise(0, y, 11, 4.0) and y < 41
            west = x < 2 + 2 * vnoise(0, y, 12, 4.0) and y < 25
            if nw or ne or east or west: m.cls[y, x] = 'T'
    # ---------------------------------------------------------------- stairs first (they cut the cliff lines)
    m.stairs(45, 16, w=3, kit_rows=4)                                  # Tidewatch hill
    m.stairs(23, 20, w=3, kit_rows=4)                                  # the Center terrace
    m.stairs(25, 35, w=3, kit_rows=3, kind="stone")                    # west quay stairs (dressed stone)
    m.stairs(47, 36, w=3, kit_rows=3, kind="stone")                    # east quay stairs (dressed stone)
    m.plan_cliffs()
    # ---------------------------------------------------------------- streets: curved lanes into one plaza
    G = dict(c='g', only='.tT')
    m.rect(32, 0, 3, 7, 'd')                                           # The Ferrymen's Mile's dirt lane (520 x 14-16 = our x 32-34)
    m.lane([(33.5, 6.5), (37.4, 8.8), (38.6, 13.5), (37, 19.5), (33.8, 24.5)], w=3.3, seed=31, wobble=0.2, **G)   # the valley road
    m.blob(32.5, 29.2, 8.6, 4.3, 'g', seed=32, rough=0.3, only='.tT')  # the plaza above the harbour
    m.rect(29, 31, 9, 3, 'g', only='.tT')                              # ... squared off along the overlook rail
    m.lane([(24.5, 24.5), (25.2, 27), (27, 28.5)], w=3.0, seed=33, wobble=0.3, **G)            # from the terrace stairs
    m.rect(23, 24, 3, 2, 'g', only='.tT')
    m.lane([(25.5, 30.5), (20, 31.6), (13, 31.2), (9.4, 32.5), (8.6, 36), (8.4, 40), (6, 41.6), (4.5, 41.5)], w=2.7, seed=34, wobble=0.2, **G)  # west lane
    m.lane([(8.6, 40.5), (11, 43), (15, 43.2), (17.4, 43)], c='d', w=2.1, seed=35, wobble=0.3, only='.tT')       # headland hamlet
    m.lane([(39.5, 30.4), (45, 31.3), (51, 30.4), (57, 29.6), (63, 30.4)], w=2.9, seed=36, wobble=0.2, **G)      # east lane
    m.lane([(46.4, 20.5), (46.2, 22.2), (42.6, 22.6), (41.4, 24), (40.6, 26.6)], c='d', w=2.2, seed=37, wobble=0.2, only='.tT')  # Tidewatch path
    m.rect(45, 20, 3, 1, 'd', only='.tT')
    m.rect(25, 32, 3, 3, 'g', only='.tT')   # to the west stairs
    m.lane([(48.4, 31.5), (48.4, 35)], w=3.0, seed=39, wobble=0.1, **G); m.rect(47, 32, 3, 4, 'g', only='.tT')   # to the east stairs
    m.lane([(59.5, 31), (60.5, 35), (59.6, 39), (55, 39.6), (53.6, 39.4)], c='d', w=2.1, seed=40, wobble=0.3, only='.tT')  # the sea-view loop
    m.lane([(12, 18.6), (18, 18.4), (24, 18.8), (29, 18.5)], c='d', w=2.0, seed=41, wobble=0.25, only='.tT')      # the terrace walk
    m.rect(23, 18, 3, 2, 'd', only='.tTg')
    m.street([(46, 15), (46, 13), (51, 13)], 2, 'd', only='.')         # Tidewatch yard
    for c in "gd": m.smooth(c, into=".", passes=2, only=".tT")
    for y in range(SHORE, H):
        for x in range(PIER[0], PIER[1] + 1): m.cls[y, x] = 'w'
    m.stamp('pf_anchor', 32, 29)                                       # the old anchor at the overlook, on the pier's axis
    E = []
    P = lambda n, at, **kw: E.append(SE.place(100, n, at, **kw))
    # ---------------------------------------------------------------- buildings (doors on the lanes)
    d = {}
    d['pc'] = m.stamp('gl_pc', 18, 4, 'FL_PC', 'Poke Center door')
    d['inn'] = m.stamp('gl_ell', 9, 24, 'FL_INN', 'Inn door')
    d['mart'] = m.stamp('gl_mart', 44, 24, 'FL_MART', 'Mart door')
    d['lab'] = m.stamp('gl_hall', 48, 0, 'FL_LAB', 'Lab door')
    d['customs'] = m.stamp('gl_flat1', 19, 40, 'FL_CUSTOMS', 'Customs door')
    d['dock'] = m.stamp('gl_shed', 43, 39, 'FL_DOCK', 'Dockmaster door')
    m.stamp('lighthouse', 3, 25)
    light_door = (5, 40)
    m.cls[light_door[1], light_door[0]] = 'B'
    houses = (('gl_shed', 11, 10), ('gl_shed', 31, 12), ('gl_shed', 19, 25), ('gl_cot', 52, 20), ('gl_shed', 60, 23),
              ('gl_emblem', 52, 33), ('gl_cot', 11, 34), ('gl_flat2', 36, 1))
    hd = []
    for nm, x, y in houses:
        m.stamp(nm, x, y); dd = STAMPS[nm]['door']; hd.append((x + dd[0], y + dd[1]))
    for dx, dy in list(d.values()) + hd: m.doorpath((dx, dy), depth=3 if (dx, dy) == (32, 16) else 6)
    # ---------------------------------------------------------------- events (seated by name)
    for i, x in enumerate(range(PIER[0], PIER[1] + 1)): P('Customs gate %d' % (i + 1), (x, SHORE - 1))
    for i, x in enumerate(range(PIER[0], PIER[1] + 1)): P("Edda's last call %d" % (i + 1), (x, SHORE + 3))
    P('Docking', (33, 58)); P('Calla', (31, SHORE - 1)); P('Captain Edda', (35, SHORE + 5)); P('Aurelian Voss (dock)', (33, SHORE + 6))
    P('Boy (pier)', (34, SHORE)); P("Boy's Mother (pier)", (33, SHORE + 1)); P('Woman with crate (pier)', (35, SHORE + 1))
    P('Accord plaque', (37, SHORE - 1)); P('Odo', (34, 58))
    P('Lighthouse door', light_door)
    gx, gy = d['lab']
    P('Kestrel K1', (gx - 2, gy + 2)); P('Juno (lab yard)', (gx, gy + 1))
    for i, x in enumerate((32, 33, 34, 35)): P('Sendoff %d' % (i + 1), (x, 4))        # across the dirt lane
    for e in E: m.taken[e['at'][1], e['at'][0]] = True
    P('Larch (sendoff)', m.snap(36, 6, '.')); P('Juno (sendoff)', m.snap(31, 3, '.'))
    P('Wenna Hale', (39, 44)); P('Coll Hale', (41, 45)); P('HiddenItem tart stall', (37, 43))
    P('HiddenItem breakwater', (52, 46)); P('Wingull (rocks)', (19, 47))
    for e in E: m.taken[e['at'][1], e['at'][0]] = True
    lamps = ((22, 46), (29, 41), (37, 40), (46, 46), (51, 41), (30, 46))
    for i, (x, y) in enumerate(lamps):
        x, y = m.snap(x, y, 's', r=3)
        e = SE.place(100, 'Quay lamp %d' % (i + 1), (x, y))
        e['pages'][0]['graphic'] = {'tile': K.SINGLE['lamp_off'], 'dir': 'down'}; e['pages'][1]['graphic'] = {'tile': K.SINGLE['lamp_on'], 'dir': 'down'}
        E.append(e); m.taken[y, x] = True
    def S(n, ax, ay, on='.gds', r=8):
        e = SE.place(100, n, m.snap(ax, ay, on, r=r)); E.append(e); m.taken[e['at'][1], e['at'][0]] = True
    S('Girl with Wingull', 27, 45, 's', 4); S('Wingull (with girl)', 28, 45, 's', 3); S('Lamplighter', 30, 43, 's', 3)
    S('Harbor Crier', 30, 28, 'g'); S('Town sign', 36, 8, '.'); S('Lane sign', 28, 34, '.g'); S('Notice board', 27, 27, 'g')
    S('Festival poster', 38, 27, 'g'); S('Fish barrels', 47, 44, 's')
    town = [('Rope-skipping Girl 1', 34, 27), ('Rope-skipping Girl 2', 35, 27), ('Kelp-drier', 27, 42), ('Old Sailor', 36, 45),
            ('Meridian Linesman', 29, 47), ('Fishwife', 48, 45), ('Woman hanging washing', 14, 44), ('Boy with toy boat', 31, 45),
            ('Accord Clerk', 25, 45), ('Drunk on the steps', 28, 35), ('Old Woman on bench', 38, 32), ('Net-mender', 51, 44),
            ('Twin 1', 55, 30), ('Twin 2', 56, 30), ('Meridian Recruiter', 35, 22), ('Boy (town)', 37, 12),
            ("Boy's Mother (town)", 35, 9), ('Woman with crate (town)', 42, 31)]
    for n, x, y in town: S(n, x, y)
    for e in E:
        if e.get('type') == 'sign':
            e['post'] = False; x, y = e['at']
            if e['name'] == 'Town sign': m.tile(C('sh', 4833 - 4448), x, y - 1, 2); m.tile(C('sh', 4841 - 4448), x, y, 1)
            else: m.tile(C('sh', 4847 - 4448), x, y, 1)
    missing = SE.unplaced(100)
    if missing: raise SystemExit('ferrow: script events not placed: %s' % missing)
    m.events += E
    # ---------------------------------------------------------------- dressing
    dress_plaza(m)
    dress_beach(m)
    dress_yards(m)
    for cx, cy, n in ((15, 8, 2), (8, 15, 2), (5, 10, 2), (29, 6, 1), (14, 16, 1), (4, 21, 2), (40, 12, 2), (41, 18, 2), (38, 22, 1),
                      (30, 22, 1), (22, 33, 2), (16, 22, 1), (20, 36, 1), (51, 18, 1), (64, 21, 2), (58, 20, 1), (50, 27, 1),
                      (43, 34, 2), (56, 36, 1), (63, 34, 2), (62, 40, 2), (56, 42, 2), (14, 30, 0), (3, 44, 1), (10, 46, 0),
                      (60, 8, 2), (58, 14, 1), (46, 4, 1), (42, 11, 2), (20, 22, 0), (36, 34, 0), (52, 11, 0), (8, 22, 2), (42, 17, 2),
                      (3, 30, 1), (22, 38, 1), (50, 36, 1), (64, 37, 2), (57, 33, 0), (33, 20, 1), (6, 46, 1), (20, 12, 0), (13, 5, 2),
                      (27, 9, 1), (63, 26, 1), (41, 3, 0), (30, 3, 1), (16, 46, 1)):
        if n: m.trees(cx, cy, n, TREES, r=3, seed=cx * 3 + cy)
    for x, y in ((31, 7), (36, 13), (38, 18), (32, 23), (26, 25), (40, 25), (22, 30), (15, 30), (10, 34), (7, 39), (44, 30),
                 (52, 29), (61, 29), (27, 33), (46, 33), (58, 38), (14, 18), (28, 18), (44, 21), (50, 14), (15, 42)):
        if m.free(x, y - 1, 1, 2, on='.') and not m.cliff[y - 1:y + 1, x].any(): m.stamp('gl_lamp', x, y - 1)
    m.beds()
    print('  street trees', m.autotrees(46, TREES + ['tr_oak2', 'tr_oak'], seed=5, gap=0, box=(0, 0, W, 45)))
    m.greenfill(1)
    # ---------------------------------------------------------------- paint
    m.paint_ground(); m.autotiles(); m.cliffs(); m.paint_stairs(); m.forest()
    wharf_paint(m)
    m.put_stamps()
    m.grass_variation()
    ship(m, 0, 0)
    sea_rocks(m)
    boats(m)
    m.scatter(10, seed=12, on=".T")
    m.seal_against([{'dir': 'N', 'offset': 28, 'to': 520, 'to_offset': 11}], spans=[('N', 32, 4)], keep=[tuple(e['at']) for e in m.events if e.get('type') == 'warp'] + [(x, y) for x in range(m.W) for y in range(m.H - 12, m.H)])   # map builder 9: only the lane meets the Ferrymen's Mile
    if preview: m.preview(preview, 0.5)
    head = {'id': 100, 'biome': 'village', 'name': "Ferrow's Landing", 'parent': 0, 'bgm': 'Lappet Town', 'rubric': True, 'yards_ok': True,
            'metadata': {'Outdoor': True, 'ShowArea': True, 'MapPosition': [0, 14, 26], 'BattleBack': 'field'},
            'tone': [6, 2, -10, 0], 'fog': {'name': 'prismfall_seamist', 'opacity': 34, 'blend': 0, 'zoom': 100, 'sx': 2, 'sy': 0},
            'connections': [{'dir': 'N', 'offset': 28, 'to': 520, 'to_offset': 11}], '_file': '100_ferrows_landing.yaml'}
    m.write(100, head, "# Ferrow's Landing (100). WRITTEN BY layouts/ferrow_rj.py (PF Rejuv) - edit that script.\n")
    print('doors', d)
    return m


def put(m, nm, x, y, on='.', r=2):
    """a prop at (x, y) if its footprint is free, level and off the cliffs; else the nearest such spot within r"""
    st = STAMPS[nm]
    for dd in range(r + 1):
        for yy in range(y - dd, y + dd + 1):
            for xx in range(x - dd, x + dd + 1):
                if max(abs(xx - x), abs(yy - y)) != dd: continue
                if m.free(xx, yy, st['w'], st['h'], on=on) and not m.cliff[yy:yy + st['h'], xx:xx + st['w']].any():
                    m.stamp(nm, xx, yy); return True
    return False


def dress_plaza(m):
    """the plaza: the overlook rail with the anchor, a market row under awnings, picnic tables, tubs, notice boards"""
    m.fence(28, 46, 34)                                        # the overlook rail above the harbour
    for nm, x, y in (('hb_tables', 27, 26), ('hb_tables', 36, 26), ('gl_tables', 39, 27), ('gl_tables', 25, 28),
                     ('sh_crates', 30, 25), ('hb_boxes', 40, 31), ('hb_barrel', 29, 32), ('hb_cask', 38, 32),
                     ('pf_logbench', 36, 32), ('pf_logbench', 29, 30), ('hb_keg', 35, 25)):
        put(m, nm, x, y, on='g', r=2)
    for x, y in ((27, 25), (36, 25)):                           # awnings over the market tables
        if all(m.inb(x + i, y) and not m.taken[y, x + i] for i in range(3)):
            st = STAMPS['pf_p_awning']
            m.over += [(2, x + i, y, t) for i in range(3) for t in [max(st['layers'][z][0][i] for z in range(3))] if t]


def dress_yards(m):
    """what makes the houses lived-in: washing lines, rug lines, kegs and casks by side walls, fenced front gardens"""
    for nm, x, y in (('hb_washline', 14, 39), ('hb_rugline', 55, 28), ('hb_washline', 57, 40), ('hb_cask', 23, 29),
                     ('hb_barrel', 15, 14), ('hb_shed', 35, 14), ('hb_boxes2', 51, 28), ('hb_barrel2', 42, 28), ('hb_keg', 64, 28),
                     ('hb_dyeline', 13, 22), ('pf_logbench', 15, 44), ('pf_logbench', 61, 37), ('hb_barrel', 19, 31),
                     ('hb_cask', 35, 8), ('pf_logbench', 13, 17), ('hb_shed', 59, 26), ('sh_crates', 49, 24), ('hb_rugline2', 41, 6)):
        put(m, nm, x, y, on='.', r=2)
    m.fence(9, 18, 34, gaps=((11, 12),)) if False else None
    m.fence(51, 58, 29, gaps=((54, 56),))                      # the cottage's front garden
    m.fence(10, 18, 43) if False else None


def dress_beach(m):
    """the harbour front: the Hales' tart stall, freight on the wharf, nets and fish tubs, boats hauled out, boulders
    and ferns against the bluff"""
    for nm, x, y in (('pf_p_awning', 36, 41), ('sh_crates', 37, 42), ('sh_crates', 51, 40), ('sh_crates', 28, 40),
                     ('pf_p_net', 30, 40), ('pf_p_net', 51, 39), ('ak_boulder', 18, 40), ('ak_rock2', 51, 44), ('ak_fern', 39, 39),
                     ('ak_fern', 33, 39), ('ak_fern', 25, 42), ('pf_p_laundry', 41, 40), ('hb_tubs', 31, 41), ('hb_fish', 40, 42),
                     ('hb_boat2', 26, 43), ('hb_boat4', 49, 43), ('hb_barrels', 40, 39), ('hb_barrel', 26, 40), ('hb_barrel2', 48, 44),
                     ('hb_boxes', 35, 39), ('hb_fish', 29, 44), ('hb_crates4', 38, 44), ('hb_boxes2', 23, 44), ('hb_keg', 32, 44)):
        m.near(nm, x, y, on='s', r=3)
    for x in (22, 27, 31, 37, 41, 45, 49):                      # bollards along the wharf edge
        if not m.taken[47, x] and not m.taken[46, x] and not m.taken[45, x]: m.stamp('hb_post1' if x % 2 else 'hb_post2', x, 46)
    rng = __import__('random').Random(8)
    for y in range(39, SHORE - 2):
        for x in range(18, 54):
            if m.cls[y, x] == 's' and not m.taken[y, x] and rng.random() < 0.05:
                m.tile(rng.choice([C('ak', 414), C('ak', 427), C('ak', 435)]), x, y, 2); m.taken[y, x] = False


def wharf_paint(m):
    """the timber wharf along the waterline and the ferry pier: planks on the ground layer (objects stand on them)"""
    top, body, end = ([C('ak', 1516 + i) for i in range(3)], [C('ak', 1524 + i) for i in range(3)], [C('ak', 1532 + i) for i in range(3)])
    x0, x1, y0, y1 = WHARF
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if m.eff[y, x] not in 'sw': continue
            row = top if y == y0 else end if (y == y1 and not PIER[0] <= x <= PIER[1]) else body
            m.L[0, y, x] = row[0 if x == x0 else 2 if x == x1 else 1]; m.L[1, y, x] = 0
    for y in range(SHORE, H):
        for i, x in enumerate(range(PIER[0], PIER[1] + 1)):
            m.L[0, y, x] = body[i]; m.L[1, y, x] = 0


def boats(m):
    """rowing boats moored along the wharf and the pier (solid, on the water)"""
    for nm, x, y in (('hb_boat1', 23, 48), ('hb_boat3', 28, 49), ('hb_boat2', 37, 49), ('hb_boat1', 43, 48), ('hb_boat4', 29, 52)):
        L = np.array(STAMPS[nm]['layers']); h, w = L.shape[1:]
        if all(m.cls[y + j, x + i] == 'w' and m.L[2, y + j, x + i] == 0 and m.L[1, y + j, x + i] == 0 for i in range(w) for j in range(h)):
            for j in range(h):
                for i in range(w):
                    t = int(L[:, j, i].max())
                    if t: m.L[2, y + j, x + i] = t


def sea_rocks(m):
    import numpy as _np
    small = [[[C('ak', 1644), C('ak', 1645)], [C('ak', 1652), C('ak', 1653)]], [[C('ak', 1646), C('ak', 1647)], [C('ak', 1654), C('ak', 1655)]]]
    rng = __import__('random').Random(5)
    for nm, x, y in (('ak_rock2', 10, 50), ('ak_boulder', 58, 50), ('ak_rock2', 25, 54), ('ak_rock2', 61, 45)):
        L = _np.array(STAMPS[nm]['layers']); h, w = L.shape[1:]
        if all(m.cls[y + j, x + i] in 'wW' for i in range(w) for j in range(h)):
            for j in range(h):
                for i in range(w):
                    for z in (1, 2):
                        if L[z, j, i]: m.L[2, y + j, x + i] = L[z, j, i]
    for x, y in ((15, 52), (5, 55), (44, 57), (64, 55), (20, 51), (53, 49)):
        r = rng.choice(small)
        if all(m.cls[y + j, x + i] in 'wW' and m.L[2, y + j, x + i] == 0 for i in range(2) for j in range(2)):
            for j in range(2):
                for i in range(2): m.L[2, y + j, x + i] = r[j][i]


def ship(m, dx, dy):
    for x, y, z, t in K.SHIP:
        x += dx; y += dy
        if m.inb(x, y): m.L[1 if z == 0 else 2, y, x] = t


if __name__ == '__main__':
    build(sys.argv[1] if len(sys.argv) > 1 else None)
