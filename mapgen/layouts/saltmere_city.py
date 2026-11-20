#!/usr/bin/env python3
"""Saltmere, the free port, as three linked 88x72 district maps on the composite city tileset (palette `city`):
  140 Promenade & Market  (north gate -> The Grey Saltings, west gate -> Frostflat Causeway, east gate -> 147, harbour stairs -> 146)
  146 Harbour & Breakwater (warehouse rows, four piers, lighthouse headland, breakwater arm, salt pans)
  147 Old Town             (the Playhouse quarter: timber lanes on a bluff, Pell Playhouse on the top terrace)
Run:  python3 -I layouts/saltmere_city.py && python3 -I build.py 140 146 147
Story events for 140 live in layouts/saltmere_events.yaml (keyed by name / first words) and are re-seated here."""
import os, sys, math, yaml
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from citykit import City, STAMPS, POOL_TECT, POOL_TIMBER, POOL_SHOPS, POOL_DOCK, UMBRELLAS, HERE, vnoise
TIMBER = [n + s for n in ('w_longhouse', 'w_cot', 'w_ell_a', 'w_manor_a', 'w_manor_b', 'w_ell_b', 'w_house', 'w_house', 'w_cot') for s in ('', '_s', '_m')]
SMALL = [n + s for n in ('w_cot', 'w_house') for s in ('', '_s', '_m')]
FURN = ['t_lamp', 't_lamp', 't_barrel', 't_barrel2', 't_board', 't_bench', 't_lamp', 't_crate_pair']
W, H = 88, 72
EV = yaml.safe_load(open(os.path.join(HERE, 'layouts', 'saltmere_events.yaml')))


def ev(key, at):
    if key == 'Juno J1':                             # map builder 10: the one live J1 (S105 + :sm_arrived) is saltmere_rj's
        import saltmere_rj as SR
        e = SR.juno_j1(); e['at'] = list(at); return e
    for e in EV:
        if e.get('name') == key or str(e.get('text', '')).startswith(key):
            e = dict(e); e['at'] = list(at); return e
    raise KeyError(key)


def flat(x, spans, pad=2): return any(a - pad <= x <= b + pad for a, b in spans)


def market_stalls(c, x0, y0, x1, y1, n, seed):
    import random
    r = random.Random(seed); k = 0
    for _ in range(400):
        if k >= n: break
        x, y = r.randint(x0, x1 - 1), r.randint(y0, y1 - 2)
        if not c.free(x - 1, y - 1, 4, 5, 'b', level=False): continue
        c.block(r.choice(UMBRELLAS), x, y, 2, 2, layer=1)
        c.block(r.choice([3536, 3538]), x, y + 2, 2, 1, layer=1); k += 1


def street_lamps(c, pts):
    for x, y in pts:
        if c.free(x, y - 2, 1, 3, level=False): c.stamp('t_lamp', x, y - 2)


# =============================================================================== 140 Promenade & Market
def build_140():
    c = City(W, H, 140)
    c.hills([(20, 13, 23, 8.5, 2, 1), (73, 12, 15, 8, 2, 2)])
    def ys(x): return 65 if 53 <= x <= 64 else 65 + int(round(1.4 * math.sin(x / 6.0) + 1.6 * (vnoise(x, 0, 9, 5.0) - 0.5)))
    for y in range(H):
        for x in range(W):
            if 41 <= x <= 50 and y < 30: c.ht[y][x] = 1          # the Grey Saltings road runs up a valley between the two hills
            if y >= ys(x): c.ht[y][x] = 0
    c.notch(22, 24, 22, 2); c.notch(68, 70, 19, 2)
    # streets: gate roads in setts, the bending high street in brick, hill lanes and alleys in cobblestones
    c.rect(0, 68, 88, 4, 'b'); c.rect(53, 68, 12, 4, 'c')
    c.path([(45, 0), (45, 12), (42, 20), (38, 28)], 3, 'k', 1)
    c.blob(35, 37, 12, 8, 'b', 3, only='.k', rough=0.9); c.blob(45, 41, 7, 5, 'b', 4, only='.k', rough=0.9)
    c.blob(35, 36, 5, 3, 'c', 5, only='b')
    c.path([(46, 42), (52, 50), (58, 57), (58, 64)], 3, 'b', 6)
    c.rect(0, 31, 6, 4, 'k'); c.path([(0, 32.5), (12, 33), (22, 35), (28, 36)], 3, 'k', 7)
    c.rect(82, 42, 6, 4, 'k'); c.path([(48, 40), (60, 41), (74, 44), (87, 43.5)], 3, 'k', 8)
    c.path([(6, 14), (18, 12), (30, 15), (23, 21)], 2, 'o', 9); c.path([(60, 12), (72, 9), (83, 13)], 2, 'o', 10); c.path([(70, 10), (69, 18)], 2, 'o', 11)
    c.path([(23, 26), (24, 35)], 2, 'k', 12); c.path([(69, 23), (67, 31), (62, 41)], 2, 'k', 13)
    c.path([(12, 34), (10, 46), (18, 55), (30, 60)], 2, 'o', 14); c.path([(30, 44), (28, 53), (30, 60)], 2, 'k', 15)
    c.path([(4, 61), (30, 60), (54, 61)], 2, 'c', 16); c.path([(62, 61), (84, 59)], 2, 'c', 17)
    c.path([(74, 44), (76, 55), (70, 60)], 2, 'o', 18); c.path([(40, 46), (42, 54), (50, 60)], 2, 'o', 19)
    # walls: the north wall kinks at the Saltgate; towers at gates and corners
    c.wall_h(0, 42, 0, face=3); c.wall_h(48, 87, 2, face=3)
    c.wall_v(0, 5, 67, gaps=[(31, 34)]); c.wall_v(86, 7, 67, gaps=[(42, 45)])
    c.tower(38, 0, 5, 3, 5); c.tower(48, 1, 5, 3, 6); c.tower(0, 0, 4, 3, 4); c.tower(84, 2, 4, 3, 4); c.tower(14, 0, 4, 2, 4); c.tower(66, 2, 4, 2, 4)
    c.tower(0, 25, 3, 3, 3); c.tower(0, 35, 3, 3, 3); c.tower(85, 36, 3, 3, 3); c.tower(85, 46, 3, 3, 3); c.tower(0, 54, 3, 3, 3)
    c.stairs(22, 22); c.stairs(68, 19); c.stairs(56, 64, 2)
    c.cliffs(face=2, keep='WFKG')
    d = {}
    d['SM_PC'] = c.front_place('t_pokecenter', (27, 31), 'SM_PC', 'Poke Center door')
    d['SM_MART'] = c.front_place('t_mart', (47, 35), 'SM_MART', 'Mart door')
    d['SM_PAGEANT'] = c.front_place('t_theatre', (60, 39), 'SM_PAGEANT', 'Pageant Hall door')
    d['SM_HOUSE1'] = c.front_place('t_house_red', (10, 12), 'SM_HOUSE1', "Saltwife's House door", street='o')
    kx, ky = d['SM_PAGEANT']
    E = [dict(ev('SALTMERE', (0, 0)), at=[43, 8]), ev('Juno J1', c.snap(36, 38, 'b')), ev('Busker', c.snap(31, 40, 'b')),
         ev('Caramel seller', c.snap(42, 35, 'b')), ev('Eevee breeder', c.snap(40, 61, 'c')), ev('Kestrel', c.snap(kx + 2, ky + 2)),
         ev('Royal notice', c.snap(kx - 2, ky + 1))]
    c.taken[8][43] = True
    E.append({'type': 'sign', 'at': c.snap(54, 62, 'bc'), 'text': 'HARBOUR STAIRS\nDown to the quays and the breakwater.'})
    E.append({'type': 'sign', 'at': c.snap(82, 46, 'k'), 'text': "PLAYERS' GATE\nOld Town and the Pell Playhouse."})
    c.stamp('t_cart', 28, 31); c.stamp('t_stall', 39, 29)
    market_stalls(c, 26, 31, 46, 43, 7, 1)
    for x, y in ((33, 35), (37, 36)): c.stamp('t_bench', x, y)
    c.frontage(TIMBER, (2, 5, 42, 27), 'o', 1); c.frontage(TIMBER, (56, 6, 85, 20), 'o', 2)
    c.frontage(POOL_TECT + POOL_SHOPS, None, 'kbco', 3)
    c.backfill(POOL_TECT, (2, 27, 85, 63), 0.55, 4); c.backfill(SMALL, (2, 5, 40, 22), 0.5, 5); c.backfill(SMALL, (58, 6, 85, 19), 0.5, 6)
    c.edge_props(FURN, 46, 'kbc', 1); c.scatter_props(1, 68, 86, 70, ['t_crate_a', 't_cont_long', 't_crate_pair', 't_barrel', 't_cont_green'], 12, 'b', 4)
    c.inlay(0, 0, 87, 71, 'b', [3859], 0.07); c.inlay(0, 0, 87, 71, 'c', [3916], 0.09)
    c.greenfill(0.30, 1)
    c.events = E
    c.warp_line([(x, 71) for x in range(56, 62)], 146, [(x, 4) for x in range(42, 48)])
    c.warp_line([(87, y) for y in range(42, 46)], 147, [(1, y) for y in range(36, 40)])
    head = {'id': 140, 'name': 'Saltmere', 'palette': 'city', 'bgm': 'Lerucean Town', 'parent': 0, 'rubric': True,
            'tone': [10, 4, -14, 0], 'yards_ok': True,
            'metadata': {'Name': 'Saltmere', 'Outdoor': True, 'ShowArea': True, 'MapPosition': [0, 10, 25], 'BattleBack': 'field',
                         'Weather': ['Rain', 10]},
            'connections': [{'dir': 'N', 'offset': 44, 'to': 541, 'to_offset': 13}, {'dir': 'W', 'offset': 32, 'to': 560, 'to_offset': 12}]}
    c.write('140_saltmere.yaml', head, '# Saltmere - Promenade & Market (140). WRITTEN BY layouts/saltmere_city.py - edit that script.\n')
    return d


# =============================================================================== 146 Harbour & Breakwater
def build_146():
    c = City(W, H, 146)
    def shore(x): return 45 + int(round(2.5 * math.sin(x / 9.0 + 1.0) + 2.5 * (vnoise(x, 0, 31, 6.0) - 0.5))) if x < 66 else 41
    def hgt(x, y):
        if y < 1: return 1
        if ((x - 79.0) / 8.5) ** 2 + ((y - 46.0) / 19.0) ** 2 <= 1.0 + 0.3 * (vnoise(x, y, 5, 4.0) - 0.5): return 0
        if ((x - 54.0) / 30.0) ** 2 + ((y - 64.5) / 2.4) ** 2 <= 1.0 + 0.5 * (vnoise(x, y, 6, 3.0) - 0.5) and x > 26: return 0
        if y < shore(x) and x < 74: return 0
        return -1
    c.set_heights(hgt)
    for y in range(H):
        for x in range(W):
            if c.ht[y][x] < 0: c.g[y][x] = '~'
    for x in range(0, 74):                                              # brick wharf along the water
        for y in range(shore(x) - 5, shore(x)):
            if c.g[y][x] == '.': c.g[y][x] = 'b'
    c.rect(41, 1, 8, 5, 'c')
    c.path([(45, 4), (44, 14), (37, 24), (39, 39)], 3, 'k', 1)             # Stair Street down to the wharf
    c.path([(22, 12), (34, 13), (44, 14), (58, 11), (71, 13)], 2, 'k', 2); c.path([(4, 26), (20, 23), (37, 24), (56, 26), (70, 24)], 2, 'k', 3)
    c.path([(22, 12), (20, 23), (24, 38)], 2, 'o', 4); c.path([(58, 11), (56, 26), (58, 37)], 2, 'o', 5); c.path([(8, 26), (10, 38)], 2, 'o', 6)
    c.path([(70, 24), (70, 38)], 2, 'k', 7)
    for x0, y0, w, h in ((47, 16, 7, 5), (26, 29, 8, 5), (61, 29, 7, 5)): c.rect(x0, y0, w, h, 'c', '.')
    for x0, y0, w, h in ((3, 7, 7, 4), (12, 6, 6, 5), (3, 13, 5, 5), (10, 13, 8, 4), (4, 19, 12, 2)): c.rect(x0, y0, w, h, 'p')
    for x0, w, ln in ((9, 3, 11), (25, 3, 15), (43, 4, 10), (60, 3, 12)):
        c.rect(x0, shore(x0 + 1) - 1, w, ln, '=', '~')
    c.path([(72, 38), (76, 44), (78, 56), (74, 63), (60, 65), (40, 65), (28, 64)], 2, 'o', 12, only='.')
    c.wall_v(0, 0, 40); c.tower(0, 38, 3, 3, 3)
    c.stairs(42, 0, 2)
    c.cliffs(face=2, keep='WFKG~=')
    d = {}
    d['office'] = c.front_place('t_lodge', (41, 36), 'SM_HARBOUR', 'Harbour Office door', street='kb')
    c.stamp('t_lighthouse', 77, 36)
    c.stamp('t_ship', 48, shore(46) + 3, force=True); c.stamp('t_ship', 13, 54, force=True)
    ox, oy = d['office']
    E = [dict(ev('The breakwater', (0, 0)), at=c.snap(72, 63, 'o')),
         {'type': 'sign', 'at': c.snap(ox + 2, oy + 1, 'kb'), 'text': 'SALTMERE HARBOUR OFFICE\nAll ferries suspended by order of the quarantine.'},
         {'type': 'npc', 'name': 'Stevedore', 'at': c.snap(30, 41, 'b'), 'sprite': 'NPC 07', 'dir': 'down', 'move': 'random',
          'text': "Stevedore: Tax-barges tie up outside the breakwater and no further.\nFree port means free. [TODO story]"},
         {'type': 'npc', 'name': 'Salt raker', 'at': [10, 12], 'sprite': 'NPC 11', 'dir': 'right',
          'text': 'Salt raker: The pans glitter best at low sun. Mind the brine. [TODO story]'},
         {'type': 'npc', 'name': 'Old angler', 'at': [26, 54], 'sprite': 'NPC 05', 'dir': 'down',
          'text': 'Old angler: Something big has been circling the breakwater since the Shatter talk began. [TODO story]'}]
    c.taken[12][10] = True
    for x, y in ((47, 14), (25, 27), (60, 27)): c.stamp('t_warehouse', x, y, force=True)
    c.frontage(POOL_DOCK + POOL_TECT[:8], (20, 5, 73, 44), 'kbo', 1); c.frontage(SMALL + POOL_TECT[:6], (2, 22, 20, 44), 'kbo', 2)
    c.backfill(POOL_DOCK + POOL_TECT[:6], (18, 5, 73, 40), 0.8, 3); c.backfill(SMALL, (2, 24, 20, 40), 0.6, 4)
    c.scatter_props(3, 14, 72, 46, ['t_cont_green', 't_cont_brown', 't_cont_long', 't_crate_pair', 't_crate_a', 't_crates_b',
                                    't_barrel', 't_barrel2'], 26, 'bc', 1)
    c.edge_props(FURN, 26, 'kb', 2)
    c.inlay(0, 0, 87, 50, 'b', [3859], 0.07); c.inlay(0, 0, 87, 50, 'c', [3916], 0.12)
    c.greenfill(0.20, 2)
    c.sea_rocks(46, avoid=[(44, 44, 62, 58), (10, 50, 26, 62)])
    c.events = E
    c.warp_line([(x, 3) for x in range(42, 48)], 140, [(x, 70) for x in range(56, 62)])
    head = {'id': 146, 'name': 'Saltmere - Harbour & Breakwater', 'palette': 'city', 'bgm': 'Lerucean Town', 'parent': 140,
            'rubric': True, 'tone': [6, 4, -8, 0], 'yards_ok': True,
            'metadata': {'Name': 'Saltmere Harbour', 'Outdoor': True, 'ShowArea': True, 'MapPosition': [0, 10, 25],
                         'BattleBack': 'field', 'Weather': ['Rain', 10]}}
    c.write('146_saltmere_harbour.yaml', head, '# Saltmere - Harbour & Breakwater (146). WRITTEN BY layouts/saltmere_city.py.\n', mirror_max=0.5)


# =============================================================================== 147 Old Town
def build_147():
    c = City(W, H, 147)
    c.hills([(56, 15, 23, 11, 2, 3), (15, 13, 14, 9, 2, 4)])
    def yl(x): return 63 + int(round(1.6 * math.sin(x / 6.0) + 2.0 * (vnoise(x, 0, 13, 5.0) - 0.5)))
    for y in range(H):
        for x in range(W):
            if y >= yl(x) or ((x - 66) / 9.0) ** 2 + ((y - 66) / 6.0) ** 2 < 1.0 + 0.4 * (vnoise(x, y, 8, 3.0) - 0.5): c.ht[y][x] = -1
            if c.ht[y][x] < 0: c.g[y][x] = '~'
    c.notch(50, 55, 28, 2); c.notch(13, 15, 22, 2)
    for y in range(8, 28):
        for x in range(44, 63): c.ht[y][x] = 2
    c.rect(47, 24, 13, 4, 'c'); c.rect(50, 28, 6, 1, 'c')                               # Playhouse forecourt on the hilltop
    c.rect(0, 36, 5, 4, 'k'); c.path([(0, 37.5), (14, 38), (26, 41), (32, 42)], 3, 'k', 1)
    c.blob(40, 42, 9, 6, 'b', 3, only='.k', rough=0.9); c.blob(47, 38, 5, 4, 'b', 4, only='.k', rough=0.9); c.blob(40, 42, 4.5, 2.5, 'c', 5, only='b')
    c.path([(52, 32), (51, 36), (48, 40)], 3, 'k', 6)
    c.path([(48, 44), (60, 47), (72, 44), (84, 46)], 3, 'k', 7)
    c.path([(14, 26), (15, 31), (14, 38)], 2, 'o', 8); c.path([(5, 15), (14, 16), (25, 14)], 2, 'o', 9); c.path([(14, 16), (14, 21)], 2, 'o', 16)
    c.path([(30, 44), (26, 54), (38, 59), (56, 57), (60, 47)], 2, 'o', 10); c.path([(14, 40), (10, 50), (16, 58), (26, 54)], 2, 'o', 11)
    c.path([(72, 44), (76, 54), (82, 58)], 2, 'o', 12); c.path([(26, 41), (28, 30), (34, 24)], 2, 'o', 13)
    c.path([(36, 12), (44, 9), (52, 8)], 2, 'o', 14); c.path([(66, 8), (76, 12), (72, 22)], 2, 'o', 15)
    c.wall_h(0, 30, 0, face=3); c.wall_h(31, 87, 2, face=3); c.wall_v(0, 5, 62, gaps=[(36, 39)]); c.wall_v(86, 7, 58)
    c.tower(0, 0, 4, 3, 4); c.tower(84, 2, 4, 3, 4); c.tower(28, 0, 5, 3, 5); c.tower(62, 2, 4, 2, 4)
    c.tower(0, 30, 3, 3, 3); c.tower(0, 40, 3, 3, 3); c.tower(85, 54, 3, 3, 4); c.tower(0, 58, 3, 3, 4)
    c.stairs(50, 28, 2); c.stairs(13, 22)
    c.cliffs(face=2, keep='WFKG~')
    for y in range(H):
        for x in range(W):
            if c.g[y][x] == 'C' and c.ht[y][x] < 0: c.g[y][x] = '~'; c.taken[y][x] = False
    d = {}
    d['gym'] = c.stamp('t_hall', 46, 8, 'SM_GYM', 'Playhouse door', force=True)
    gx, gy = d['gym']
    E = [dict(ev('Playhouse sign', (0, 0)), at=[gx - 3, gy + 2]),
         {'type': 'sign', 'at': c.snap(5, 40, 'k'), 'text': "PLAYERS' GATE\nWest: Saltmere market and the harbour stairs."},
         {'type': 'npc', 'name': 'Costumier', 'at': c.snap(22, 40, 'k'), 'sprite': 'NPC 12', 'dir': 'down',
          'text': 'Costumier: Every mask in the Pageant is stitched on this lane. Even the ones nobody ordered. [TODO story]'},
         {'type': 'npc', 'name': 'Street player', 'at': c.snap(41, 44, 'b'), 'sprite': 'NPC 08', 'dir': 'down', 'move': 'random',
          'text': 'Street player: A stage is anywhere two people stop to look. Dorian taught us that. [TODO story]'}]
    c.taken[gy + 2][gx - 3] = True
    c.stamp('t_cart', 34, 37); market_stalls(c, 32, 37, 50, 47, 5, 5)
    for x, y in ((38, 41), (42, 43)): c.stamp('t_bench', x, y)
    c.frontage(TIMBER + ['t_stall', 't_shop_purple'], None, 'kbco', 1)
    c.backfill(TIMBER, (2, 5, 85, 61), 0.5, 2)
    c.edge_props(FURN, 40, 'kbc', 1)
    c.inlay(0, 0, 87, 71, 'b', [3859], 0.07); c.inlay(0, 0, 87, 71, 'c', [3916], 0.10)
    c.greenfill(0.22, 3)
    c.sea_rocks(24)
    c.events = E
    c.warp_line([(0, y) for y in range(36, 40)], 140, [(86, y) for y in range(42, 46)])
    head = {'id': 147, 'name': 'Saltmere - Old Town', 'palette': 'city', 'bgm': 'Lerucean Town', 'parent': 140, 'rubric': True,
            'tone': [12, 4, -18, 0], 'yards_ok': True,
            'metadata': {'Name': 'Saltmere Old Town', 'Outdoor': True, 'ShowArea': True, 'MapPosition': [0, 10, 25],
                         'BattleBack': 'field', 'Weather': ['Rain', 10]}}
    c.write('147_saltmere_oldtown.yaml', head, '# Saltmere - Old Town (147). WRITTEN BY layouts/saltmere_city.py.\n')


if __name__ == '__main__':
    d = build_140(); build_146(); build_147()
    print('doors 140:', d)
