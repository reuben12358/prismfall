#!/usr/bin/env python3
"""Ferrow's Landing (100): a weathered timber ferry village at the edge of the realm, 68x60, palette `village`.
Three levels: Tidewatch hill (NE, Larch's observatory-cottage with its lantern turret), the village bluff (narrow
lanes that wind down from the Route 1 lane to the square and the quay stairs), and the quay and beach with the ferry
pier. The lighthouse stands on the west headland ("<- Lighthouse" on the lane sign); the Dovetail is moored east of
the pier, drawn as a plank hull with rails and a wheelhouse (no sheet has a timber ship).
Every story event comes from layouts/story_early.py; this script only seats them.
Run: python3 -I layouts/ferrow.py && python3 -I build.py 100"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from villagekit import Village, STAMPS, WS, GARDEN, HERE, vnoise, C2
import story_early as SE
W, H = 68, 60
SHORE = 48                 # first water row at the pier (the gate row is SHORE - 1)
LAMP_OFF, LAMP_ON = C2 + 166, C2 + 167


def build():
    c = Village(W, H, 100)
    def shore(x): return SHORE + (0 if 22 <= x <= 47 else int(round(1.4 * math.sin(x / 6.0) + 1.2 * (vnoise(x, 0, 3, 5.0) - 0.5))))
    def bluff(x):
        base = 35 if 16 <= x <= 31 else (37 if 32 <= x <= 56 else 40)
        return base + int(round(0.8 * math.sin(x / 8.0 + 1) + 1.0 * (vnoise(x, 0, 4, 6.0) - 0.5)))
    c.hills([(50, 7, 13, 7, 2, 1), (9, 5, 10, 5, 2, 3)], base=1)
    for y in range(H):
        for x in range(W):
            head = ((x - 6) / 8.5) ** 2 + ((y - 41) / 11.0) ** 2 <= 1.0 + 0.3 * (vnoise(x, y, 5, 4.0) - 0.5)
            if y >= bluff(x) and not head: c.ht[y][x] = 0
            if y >= shore(x) and not head: c.ht[y][x] = -1
            if head and c.ht[y][x] < 1: c.ht[y][x] = 1
            if y >= 54 and x < 14: c.ht[y][x] = -1
    c.notch(32, 36, bluff(34), 1); c.notch(41, 43, 14, 2); c.notch(51, 53, bluff(52), 1); c.notch(14, 16, 9, 2)
    for y in range(H):
        for x in range(W):
            if c.ht[y][x] < 0: c.g[y][x] = '~'
            elif c.ht[y][x] == 0: c.g[y][x] = 's'
    # ---- lanes: narrow, winding, 2 wide (3 only in the square)
    c.path([(34.5, 0), (34, 6), (36, 11), (35, 16), (32, 22), (30, 27)], 2, 'd', 1, only='.')
    c.blob(30, 29, 5.5, 3.2, 'd', 2, only='.', rough=0.9); c.blob(30, 29, 2.5, 1.5, 'k', 3, only='d')
    c.path([(30, 31), (32, 34), (34, 37)], 2, 'd', 4, only='.')
    c.path([(26, 30), (20, 31), (14, 32), (9, 33), (5, 35)], 2, 'd', 5, only='.')
    c.path([(34, 29), (40, 31), (47, 33), (54, 31), (61, 28)], 2, 'd', 6, only='.')
    c.path([(35, 16), (39, 16), (42, 16)], 2, 'd', 7, only='.')
    c.path([(42, 12), (47, 12), (52, 12)], 2, 'd', 8, only='.')
    c.path([(12, 31), (11, 27)], 2, 'd', 9, only='.')
    c.path([(47, 33), (51, 35), (52, 37)], 2, 'd', 10, only='.')
    c.path([(15, 12), (16, 15), (22, 17), (31, 21)], 2, 'd', 11, only='.')
    # ---- quay: cobbles around the pier head, a stone breakwater west, the pier
    for y in range(36, SHORE):
        for x in range(17, 50):
            if c.g[y][x] == 's' and ((x - 33) / 16.0) ** 2 + ((y - 47) / 7.5) ** 2 < 1.0 + 0.3 * (vnoise(x, y, 8, 3.0) - 0.5): c.g[y][x] = 'k'
    c.rect(33, SHORE, 3, H - SHORE, '=', '~s'); c.rect(18, shore(18), 2, 56 - shore(18), '=', '~s')
    c.stairs(33, bluff(34)); c.stairs(41, 14); c.stairs(51, bluff(52)); c.stairs(14, 9)
    c.cliffs(face=2, keep='~=')
    for y in range(H):
        for x in range(W):
            if c.g[y][x] == 'C' and c.ht[y][x] < 0: c.g[y][x] = '~'; c.taken[y][x] = False
    # ---- the Dovetail: a plank hull with rails, moored east of the pier
    def hull(x, y):           # round stern at the pier, long waist, pointed bow to the east
        if not 50 <= y <= 56 or not 37 <= x <= 55: return False
        if x < 40: half = 3.2 * math.sqrt(max(0.0, 1 - ((40 - x) / 3.4) ** 2))
        elif x < 48: half = 3.2
        else: half = 3.2 * max(0.0, 1 - ((x - 48) / 7.5) ** 1.5)
        return abs(y - 53) <= half + 0.15
    for y in range(H):
        for x in range(W):
            if hull(x, y):
                rim = not all(hull(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                c.g[y][x] = 'w' if rim else 'D'; c.taken[y][x] = True
                if rim: c.tile(3831, x, y, 0)
    for nm, x, y in (('hs_jonquil_12', 39, 51), ('p_crates', 43, 51), ('tp_barrel_06', 46, 52), ('tp_barrel_02', 47, 51),
                     ('tp_stall_13', 42, 54), ('hs_jonquil_07', 50, 52), ('p_banner3', 45, 52), ('tp_barrel_09', 49, 54)):
        c.stamp(nm, x, y, force=True)            # wheelhouse, freight, a pennant mast, a life ring on the rail
    # ---- named buildings
    d = {}
    d['lab'] = c.stamp('w_house_m', 45, 5, 'FL_LAB', 'Lab door', force=True)
    c.stamp('hs_jonquil_11', 51, 5, force=True)                  # Tidewatch's lantern turret (the "observatory")
    c.stamp('hs_jonquil_09', 55, 9, force=True)                  # brass sea-glass on the terrace
    d['pc'] = c.stamp('w_longhouse_r', 17, 20, 'FL_PC', 'Poke Center door', force=True)
    d['mart'] = c.stamp('w_house_s', 38, 21, 'FL_MART', 'Mart door', force=True)
    d['inn'] = c.stamp('w_ell_a', 3, 16, 'FL_INN', 'Inn door', force=True)
    d['customs'] = c.stamp('w_longhouse_s', 19, 38, 'FL_CUSTOMS', 'Customs door', force=True)
    d['dock'] = c.stamp('w_house', 42, 27, 'FL_DOCK', 'Dockmaster door', force=True)
    c.stamp('lh_ferrow', 2, 31, force=True); light_door = (4, 39)
    c.stamp('t_stall', 41, 40, force=True)                       # the Hales' bramble-tart stall on the quay
    for nm, x, y in (('hs_jonquil_16', 32, 45), ('hs_jonquil_16', 36, 45)):   # the customs gate's brass posts
        c.stamp(nm, x, y, force=True)
    for k, dd in d.items():
        for dy in (1, 2):
            if c.g[dd[1] + dy][dd[0]] in '.,': c.g[dd[1] + dy][dd[0]] = 'd'
    for x, y in ((d['pc'][0] + 1, d['pc'][1] - 1), (d['mart'][0] + 1, d['mart'][1] - 1)):
        c.tile(STAMPS['hs_jonquil_28']['layers'][1][0][0] or STAMPS['hs_jonquil_28']['layers'][2][0][0], x, y, 2)   # Poke Ball plaques
    c.stamp('p_banner', d['pc'][0] + 3, d['pc'][1] - 1, force=True); c.stamp('p_banner', d['mart'][0] + 2, d['mart'][1] - 1, force=True)
    # ---- events
    E = []
    P = lambda n, at, **kw: E.append(SE.place(100, n, at, **kw))
    for i, x in enumerate((33, 34, 35)): P('Customs gate %d' % (i + 1), (x, SHORE - 1))
    for i, x in enumerate((33, 34, 35)): P("Edda's last call %d" % (i + 1), (x, SHORE + 3))
    P('Docking', (1, 58)); P('Calla', (31, SHORE - 1)); P('Captain Edda', (35, SHORE + 5)); P('Aurelian Voss (dock)', (33, SHORE + 6))
    P('Boy (pier)', (34, SHORE)); P("Boy's Mother (pier)", (33, SHORE + 1)); P('Woman with crate (pier)', (35, SHORE + 1))
    P('Accord plaque', (37, SHORE - 1)); P('Odo', (34, 58))
    P('Lighthouse door', light_door)
    gx, gy = d['lab']
    P('Kestrel K1', (gx - 2, gy + 2)); P('Juno (lab yard)', (gx, gy + 1))
    for i, x in enumerate((33, 34, 35, 36)): P('Sendoff %d' % (i + 1), (x, 4))
    P('Larch (sendoff)', c.snap(37, 3, '.,', r=3)); P('Juno (sendoff)', c.snap(31, 3, '.,', r=3))
    P('Wenna Hale', (46, 43)); P('Coll Hale', (47, 45)); P('HiddenItem tart stall', (40, 41))
    P('HiddenItem breakwater', (18, 55)); P('Wingull (rocks)', c.snap(12, 49, '.,s', r=4))
    P('Girl with Wingull', c.snap(26, 44, 'sk', r=4)); P('Wingull (with girl)', c.snap(27, 44, 'sk', r=3))
    P('Lamplighter', c.snap(29, 46, 'k', r=3))
    for i, (x, y) in enumerate(((24, 44), (28, 42), (38, 42), (45, 47), (49, 45), (55, 44))):
        x, y = c.snap(x, y, 'ks', r=3)
        e = SE.place(100, 'Quay lamp %d' % (i + 1), (x, y))
        e['pages'][0]['graphic'] = {'tile': LAMP_OFF, 'dir': 'down'}; e['pages'][1]['graphic'] = {'tile': LAMP_ON, 'dir': 'down'}
        E.append(e)
    for e in E: c.taken[e['at'][1]][e['at'][0]] = True
    for x in range(32, 37):
        for y in range(SHORE - 1, H): c.taken[y][x] = True
    S = lambda n, ax, ay, on='dko', r=8: P(n, c.snap(ax, ay, on, r=r))
    S('Harbor Crier', 30, 28); S('Town sign', 34, 2); S('Lane sign', 33, 26); S('Notice board', 28, 26)
    S('Festival poster', 27, 31); S('Fish barrels', 44, 46, 'ks')
    town = [('Rope-skipping Girl 1', 26, 29), ('Rope-skipping Girl 2', 27, 29), ('Kelp-drier', 38, 45), ('Old Sailor', 30, 45),
            ('Meridian Linesman', 26, 45), ('Fishwife', 46, 44), ('Woman hanging washing', 12, 33), ('Boy with toy boat', 22, 44),
            ('Accord Clerk', 24, 38), ('Drunk on the steps', 37, 39), ('Old Woman on bench', 32, 31), ('Net-mender', 16, 44),
            ('Twin 1', 45, 31), ('Twin 2', 46, 31), ('Meridian Recruiter', 36, 30), ('Boy (town)', 31, 24),
            ("Boy's Mother (town)", 33, 23), ('Woman with crate (town)', 41, 30)]
    for n, x, y in town: S(n, x, y, 'dkos')
    missing = SE.unplaced(100)
    if missing: raise SystemExit('ferrow: script events not placed: %s' % missing)
    # ---- houses along the lanes, then yards
    c.frontage([n for n in WS if 'ell' not in n and not n.endswith('_r')], (1, 15, 66, 36), 'd', 1, skip=0.45)
    c.backfill([n for n in WS if ('cot' in n or 'house' in n) and not n.endswith('_r')], (1, 15, 66, 36), 0.25, 2)
    # ---- dressing
    c.dress(['hs_jonquil_26', 'hs_jonquil_29', 'hs_jonquil_31', 'hs_jonquil_33'], 6, 's', 1, (2, 42, 31, 47), pad=1)
    c.dress(['p_net', 'p_net', 'p_crates', 't_barrel', 't_barrel2', 'hs_jonquil_36', 'hs_jonquil_35', 'tp_stall_13', 't_crate_pair',
             'p_stump', 'hs_jonquil_19', 'tp_barrel_06', 'tp_barrel_09'], 24, 'sk', 2, (2, 41, 64, 47))
    c.dress(['p_laundry', 'tp_stall_08', 'p_laundry'], 7, '.', 4, near='#')
    c.dress(GARDEN + ['tp_stall_01', 'p_crates', 't_barrel', 'tp_stall_16', 'tp_barrel_01', 'tp_garden_09'], 50, '.', 5, near='#', pad=0)
    c.dress(['p_lantern'], 10, '.', 6, near='dk')
    c.dress(['p_cherry', 'p_rocks', 'p_bush_w', 'p_pinkbush', 'fo_rock_01' if 'fo_rock_01' in STAMPS else 'p_rocks'], 16, '.', 7)
    c.dress(['p_sign'], 2, '.', 8, near='d', pad=0); c.dress(['t_bench'], 2, 'k', 9, pad=0)
    c.fence_run([(43, 17), (60, 17)]); c.fence_run([(26, 2), (26, 10)]); c.fence_run([(57, 3), (57, 13)])
    c.fence_run([(2, 29), (8, 29)]); c.fence_run([(44, 34), (44, 38)])
    c.borders(p=0.7); c.meadow(0.74, 1)
    c.greenfill(0.30, 1, beds=0.05)
    c.sea_rocks(24, avoid=[(30, 44, 56, 59)])
    c.events = E
    head = {'id': 100, 'name': "Ferrow's Landing", 'parent': 0, 'bgm': 'Lappet Town', 'palette': 'village', 'rubric': True, 'yards_ok': True,
            'metadata': {'Outdoor': True, 'ShowArea': True, 'MapPosition': [0, 14, 26], 'BattleBack': 'field'},
            'tone': [6, 2, -10, 0], 'fog': {'name': 'prismfall_seamist', 'opacity': 40, 'blend': 0, 'zoom': 100, 'sx': 2, 'sy': 0},
            'connections': [{'dir': 'N', 'offset': 28, 'to': 520, 'to_offset': 10}]}
    c.write('100_ferrows_landing.yaml', head, "# Ferrow's Landing (100). WRITTEN BY layouts/ferrow.py - edit that script.\n")
    print('doors', d)
    return d


if __name__ == '__main__':
    build()
