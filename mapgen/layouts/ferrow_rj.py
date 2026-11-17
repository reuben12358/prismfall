#!/usr/bin/env python3
"""Ferrow's Landing (100) on the PF Rejuv sheet (tileset 51 "PF Rejuv Coast"), 68x60.  MAPGEN 2h.
Spring on the south coast: Goldenleaf's timber-and-stone houses on Sheridan's green bluff, Akuwa's grass-capped sea
cliffs and white beach, blossom trees.  Three levels: Tidewatch hill (NE, Larch's station), the village bluff (gravel
street from the Route 1 lane down to the square, side streets to the lighthouse headland and the east houses), and the
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
    """last row of the village bluff (h=1) in column x"""
    if 18 <= x <= 52: return 37
    if x < 18: return 45 + int(round(1.0 * math.sin(x / 3.0)))
    return 43 + int(round(1.5 * math.sin(x / 4.0) + 1.5 * (vnoise(x, 0, 4, 5.0) - 0.5)))


def shore(x):
    if 18 <= x <= 52: return SHORE + (0 if 21 <= x <= 49 else -1)
    return lip(x) + 2


def hill(x, y):
    """Tidewatch hill (h=2) in the north-east: a clean south face at row 14, west side at x 44"""
    return x >= 44 and y <= (16 if x < 61 else 18)


def terrace(x, y):
    """the north-west terraces: two stepped levels above the bluff (long straight faces, few corners), woods on top"""
    if x <= 7 and y <= 5: return 3
    if (x <= 16 and y <= 9) or (x <= 9 and y <= 12): return 2
    return 1


TREES = ['tr_oak', 'tr_oak2', 'tr_pink', 'tr_oak', 'tr_pink']


def build(preview=None):
    m = K.RMap(W, H, 51, 100, water='Ocean', kit={1: 'ak', 2: 'sh', 3: 'sh'})
    # ---------------------------------------------------------------- terrain: bluff, hill, beach, sea
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
    for y in range(H):                      # woods: north-west corner, the hill's east end, thin east edge
        for x in range(W):
            if m.ht[y, x] < 1: continue
            nw = m.ht[y, x] == 3 or (m.ht[y, x] == 2 and x < 4)
            ne = m.ht[y, x] == 2 and (x > 61 + 2 * vnoise(0, y, 8, 4.0) or (y < 1 and x > 56))
            east = x > 64 + 2 * vnoise(0, y, 11, 4.0) and y < 40
            west = x < 3 + 3 * vnoise(0, y, 12, 4.0) and y < 25
            if nw or ne or east or west: m.cls[y, x] = 'T'
    # ---------------------------------------------------------------- streets (orthogonal, Goldenleaf style)
    m.rect(32, 0, 5, 25, 'g')                                          # Route 1 lane (x 33-36 at the edge) -> square
    m.rect(26, 24, 17, 7, 'g')                                         # the square
    m.street([(33, 30), (33, 37)], 3)                                  # down to the quay stairs
    m.street([(9, 19), (32, 19)], 3)                                   # upper street (Poke Center)
    m.street([(35, 20), (46, 20)], 3, 'd')                             # to the Tidewatch stairs
    m.street([(26, 32), (6, 32), (6, 41)], 3)                          # west street, past the inn to the lighthouse
    m.street([(42, 32), (61, 32)], 3)                                  # east street
    m.street([(49, 33), (49, 37)], 3)                                  # second quay stairs
    m.street([(46, 15), (46, 13), (51, 13)], 2, 'd', only='.')         # Tidewatch yard
    m.stairs(45, 16, w=3, kit_rows=4)
    m.street([(13, 13), (13, 18)], 2, 'd', only='.')                   # up the terrace to the lookout
    m.stairs(12, 9, w=2, kit_rows=4)
    m.stairs(32, 37, w=3, kit_rows=3)
    m.stairs(48, 37, w=3, kit_rows=3)
    for y in range(SHORE, H):
        for x in range(PIER[0], PIER[1] + 1): m.cls[y, x] = 'w'
    E = []
    P = lambda n, at, **kw: E.append(SE.place(100, n, at, **kw))
    # ---------------------------------------------------------------- buildings (doors on the streets)
    d = {}
    d['pc'] = m.stamp('gl_pc', 18, 4, 'FL_PC', 'Poke Center door')
    d['inn'] = m.stamp('gl_ell', 9, 21, 'FL_INN', 'Inn door')
    d['mart'] = m.stamp('gl_mart', 37, 18, 'FL_MART', 'Mart door')
    d['lab'] = m.stamp('gl_hall', 48, 0, 'FL_LAB', 'Lab door')
    d['customs'] = m.stamp('gl_flat1', 19, 40, 'FL_CUSTOMS', 'Customs door')
    d['dock'] = m.stamp('gl_shed', 43, 39, 'FL_DOCK', 'Dockmaster door')
    m.stamp('lighthouse', 3, 25)
    light_door = (5, 40)
    m.cls[light_door[1], light_door[0]] = 'B'
    for nm, x, y in (('gl_cot', 45, 22), ('gl_emblem', 54, 25), ('gl_flat2', 37, 8), ('gl_shed', 20, 25), ('gl_flat2', 54, 34)):
        m.stamp(nm, x, y)
    for k, (dx, dy) in d.items():
        for yy in (dy + 1, dy + 2):
            if m.cls[yy, dx] in '.tT' and m.ht[yy, dx] == m.ht[dy, dx] and (yy + 1 >= H or m.ht[yy + 1, dx] == m.ht[dy, dx]): m.cls[yy, dx] = 'd'
    # ---------------------------------------------------------------- events (seated by name)
    for i, x in enumerate(range(PIER[0], PIER[1] + 1)): P('Customs gate %d' % (i + 1), (x, SHORE - 1))
    for i, x in enumerate(range(PIER[0], PIER[1] + 1)): P("Edda's last call %d" % (i + 1), (x, SHORE + 3))
    P('Docking', (33, 58)); P('Calla', (31, SHORE - 1)); P('Captain Edda', (35, SHORE + 5)); P('Aurelian Voss (dock)', (33, SHORE + 6))
    P('Boy (pier)', (34, SHORE)); P("Boy's Mother (pier)", (33, SHORE + 1)); P('Woman with crate (pier)', (35, SHORE + 1))
    P('Accord plaque', (37, SHORE - 1)); P('Odo', (34, 58))
    P('Lighthouse door', light_door)
    gx, gy = d['lab']
    P('Kestrel K1', (gx - 2, gy + 2)); P('Juno (lab yard)', (gx, gy + 1))
    for i, x in enumerate((33, 34, 35, 36)): P('Sendoff %d' % (i + 1), (x, 4))
    for e in E: m.taken[e['at'][1], e['at'][0]] = True
    P('Larch (sendoff)', m.snap(38, 3, '.')); P('Juno (sendoff)', m.snap(30, 3, '.'))
    P('Wenna Hale', (39, 44)); P('Coll Hale', (41, 46)); P('HiddenItem tart stall', (37, 43))
    P('HiddenItem breakwater', (52, 46)); P('Wingull (rocks)', (19, 47))
    for e in E: m.taken[e['at'][1], e['at'][0]] = True
    lamps = ((21, 47), (29, 41), (37, 41), (46, 47), (52, 41), (30, 46))
    for i, (x, y) in enumerate(lamps):
        x, y = m.snap(x, y, 's', r=3)
        e = SE.place(100, 'Quay lamp %d' % (i + 1), (x, y))
        e['pages'][0]['graphic'] = {'tile': K.SINGLE['lamp_off'], 'dir': 'down'}; e['pages'][1]['graphic'] = {'tile': K.SINGLE['lamp_on'], 'dir': 'down'}
        E.append(e); m.taken[y, x] = True
    def S(n, ax, ay, on='.gds', r=8):
        e = SE.place(100, n, m.snap(ax, ay, on, r=r)); E.append(e); m.taken[e['at'][1], e['at'][0]] = True
    S('Girl with Wingull', 27, 47, 's', 4); S('Wingull (with girl)', 28, 47, 's', 3); S('Lamplighter', 30, 43, 's', 3)
    S('Harbor Crier', 31, 26); S('Town sign', 37, 2, '.'); S('Lane sign', 31, 34); S('Notice board', 27, 24)
    S('Festival poster', 36, 24); S('Fish barrels', 47, 44, 's')
    town = [('Rope-skipping Girl 1', 29, 27), ('Rope-skipping Girl 2', 30, 27), ('Kelp-drier', 27, 42), ('Old Sailor', 36, 44),
            ('Meridian Linesman', 29, 47), ('Fishwife', 48, 45), ('Woman hanging washing', 14, 37), ('Boy with toy boat', 31, 47),
            ('Accord Clerk', 25, 47), ('Drunk on the steps', 35, 36), ('Old Woman on bench', 39, 30), ('Net-mender', 51, 44),
            ('Twin 1', 47, 29), ('Twin 2', 48, 29), ('Meridian Recruiter', 31, 21), ('Boy (town)', 36, 12),
            ("Boy's Mother (town)", 32, 11), ('Woman with crate (town)', 43, 30)]
    for n, x, y in town: S(n, x, y)
    for e in E:
        if e.get('type') == 'sign':
            e['post'] = False; x, y = e['at']
            if e['name'] == 'Town sign': m.tile(C('sh', 4833 - 4448), x, y - 1, 2); m.tile(C('sh', 4841 - 4448), x, y, 1)
            else: m.tile(C('sh', 4847 - 4448), x, y, 1)
    missing = SE.unplaced(100)
    if missing: raise SystemExit('ferrow: script events not placed: %s' % missing)
    m.events += E
    # ---------------------------------------------------------------- dressing: yard trees, lamps, fences, props
    m.cliffs_preview = True
    for cx, cy, n in ((16, 10, 2), (32 - 1, 7, 1), (42, 4, 3), (40, 15, 1), (14, 16, 1), (3, 18, 2), (22, 27, 1), (8, 10, 2),
                      (2, 22, 3), (28, 22, 1), (51, 23, 2), (64, 22, 2), (40, 37, 1), (20, 37, 2), (13, 41, 2), (60, 35, 2),
                      (24, 36, 2), (14, 36, 2), (38, 35, 2), (44, 35, 2), (58, 22, 2), (62, 28, 2), (60, 38, 2), (63, 44, 2),
                      (52, 20, 2), (60, 16, 2), (8, 44, 2), (29, 36, 1), (41, 27, 1)):
        m.trees(cx, cy, n, TREES, r=3, seed=cx * 3 + cy)
    for x, y in ((31, 6), (36, 12), (31, 17), (25, 21), (37, 22), (25, 31), (43, 30), (12, 31), (55, 31), (35, 35), (8, 37), (51, 35)):
        if m.free(x, y - 1, 1, 2, on='.'): m.stamp('gl_lamp', x, y - 1)
    dress_beach(m)
    dress_square(m)
    m.fence(9, 18, 31, gaps=((11, 11),))                       # the inn's front garden
    m.fence(45, 51, 31, gaps=((48, 48),)); m.fence(54, 61, 31, gaps=((58, 58),))
    m.beds()
    # ---------------------------------------------------------------- paint
    m.paint()
    pier_paint(m)
    ship(m, 0, 0)
    sea_rocks(m)
    m.scatter(6, seed=12)
    if preview: m.preview(preview, 0.5)
    head = {'id': 100, 'biome': 'village', 'name': "Ferrow's Landing", 'parent': 0, 'bgm': 'Lappet Town', 'rubric': True, 'yards_ok': True,
            'metadata': {'Outdoor': True, 'ShowArea': True, 'MapPosition': [0, 14, 26], 'BattleBack': 'field'},
            'tone': [6, 2, -10, 0], 'fog': {'name': 'prismfall_seamist', 'opacity': 34, 'blend': 0, 'zoom': 100, 'sx': 2, 'sy': 0},
            'connections': [{'dir': 'N', 'offset': 28, 'to': 520, 'to_offset': 10}], '_file': '100_ferrows_landing.yaml'}
    m.write(100, head, "# Ferrow's Landing (100). WRITTEN BY layouts/ferrow_rj.py (PF Rejuv) - edit that script.\n")
    print('doors', d)
    return m


def dress_beach(m):
    """the quay: the Hales' tart stall (awning over crates), freight, nets, boulders and ferns against the bluff"""
    for nm, x, y in (('pf_p_awning', 36, 41), ('sh_crates', 37, 42), ('sh_crates', 52, 40), ('sh_crates', 27, 40),
                     ('pf_p_net', 30, 40), ('pf_p_net', 55, 42), ('ak_boulder', 18, 40) , ('ak_rock2', 51, 44), ('ak_fern', 39, 40),
                     ('ak_fern', 46, 40), ('ak_fern', 25, 41), ('pf_p_laundry', 41, 40)):
        m.near(nm, x, y, on='s', r=3)
    rng = __import__('random').Random(8)
    for y in range(40, SHORE):
        for x in range(18, 54):
            if m.cls[y, x] == 's' and not m.taken[y, x] and rng.random() < 0.05:
                m.tile(rng.choice([C('ak', 414), C('ak', 427), C('ak', 435)]), x, y, 2); m.taken[y, x] = False


def dress_square(m):
    """the square: picnic tables under the lamps, market crates, flower tubs at the corners"""
    for nm, x, y in (('gl_tables', 27, 25), ('gl_tables', 40, 25), ('sh_crates', 29, 25), ('sh_crates', 38, 26)):
        m.near(nm, x, y, on='g', r=2)


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


def pier_paint(m):
    head, body, end, legs = ([C('ak', 1516 + i) for i in range(3)], [C('ak', 1524 + i) for i in range(3)],
                             [C('ak', 1532 + i) for i in range(3)], [C('ak', 1540 + i) for i in range(3)])
    for y in range(SHORE - 1, H):
        row = head if y == SHORE - 1 else body
        for i, x in enumerate(range(PIER[0], PIER[1] + 1)):
            m.L[1, y, x] = row[i]


def ship(m, dx, dy):
    for x, y, z, t in K.SHIP:
        x += dx; y += dy
        if m.inb(x, y): m.L[1 if z == 0 else 2, y, x] = t


if __name__ == '__main__':
    build(sys.argv[1] if len(sys.argv) > 1 else None)
