#!/usr/bin/env python3
"""Saltmere, the free port, as three linked 88x72 district maps on the composite city tileset (palette `city`):
  140 Promenade & Market  (north gate -> Route 4, west gate -> Route 5, east gate -> 147, harbour stairs -> 146)
  146 Harbour & Breakwater (warehouse rows, four piers, lighthouse headland, breakwater arm, salt pans)
  147 Old Town             (the Playhouse quarter: timber lanes on a bluff, Pell Playhouse on the top terrace)
Run:  python3 -I layouts/saltmere_city.py && python3 -I build.py 140 146 147
Story events for 140 live in layouts/saltmere_events.yaml (keyed by name / first words) and are re-seated here."""
import os, sys, math, yaml
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from citykit import City, STAMPS, POOL_TECT, POOL_TIMBER, POOL_SHOPS, POOL_DOCK, UMBRELLAS, HERE, vnoise
W, H = 88, 72
EV = yaml.safe_load(open(os.path.join(HERE, 'layouts', 'saltmere_events.yaml')))


def ev(key, at):
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
    c = City(W, H, 140, base='k')
    ST = [(43, 48), (14, 16), (70, 72)]
    def yu(x): return 22 if flat(x, ST) else 22 + int(round(0.8 * math.sin(x / 8.0 + 0.5) + 1.4 * (vnoise(x, 0, 11, 7.0) - 0.5)))
    c.set_heights(lambda x, y: 2 if y < yu(x) else (1 if y < 66 else 0))
    # --- greens: belt inside the walls, cliff-top and cliff-foot strips, pocket parks
    c.rect(2, 5, 84, 3, '.'); c.rect(2, 5, 2, 60, '.'); c.rect(84, 5, 2, 60, '.')
    for x in range(2, 86):
        for y in range(yu(x) - 2, yu(x) + 4): c.g[y][x] = '.'
    c.rect(43, 0, 5, 26, 'k'); c.rect(14, 19, 3, 9, 'k'); c.rect(70, 19, 3, 9, 'k')
    c.blob(24, 40, 4.5, 3.2, '.', 7, only='k'); c.blob(66, 55, 5, 3, '.', 8, only='k'); c.blob(11, 53, 3, 2.5, '.', 9, only='k')
    c.blob(78, 38, 4, 2.4, '.', 10, only='k')
    # --- squares: the market (brick, off-centre, stepped outline) with a cream inlay ring; the promenade
    c.rect(29, 28, 27, 17, 'b'); c.rect(25, 31, 5, 9, 'b'); c.rect(55, 34, 4, 8, 'b'); c.rect(33, 44, 16, 3, 'b')
    c.rect(33, 32, 19, 9, 'c'); c.rect(35, 34, 15, 5, 'b')
    c.rect(3, 61, 83, 3, 'c'); c.rect(0, 68, 88, 4, 'b'); c.rect(42, 68, 18, 4, 'c')
    for x in range(3, 86):
        if not 47 <= x <= 54: c.g[64][x] = 'f'
    c.rect(2, 65, 84, 1, '.')
    # --- town walls
    c.wall_h(0, 87, 0, face=3, gaps=[(43, 47)])
    c.wall_v(0, 5, 67, gaps=[(31, 34)]); c.wall_v(86, 5, 67, gaps=[(42, 45)])
    for tx in (38, 49): c.tower(tx, 0, 4, 2, 5)
    c.tower(0, 0, 4, 3, 4); c.tower(84, 0, 4, 3, 4); c.tower(18, 0, 4, 2, 4); c.tower(68, 0, 4, 2, 4)
    c.tower(0, 25, 3, 3, 3); c.tower(0, 35, 3, 3, 3); c.tower(85, 36, 3, 3, 3); c.tower(85, 46, 3, 3, 3); c.tower(0, 52, 3, 3, 3)
    c.stairs(43, 21, 2); c.stairs(14, 21); c.stairs(70, 21); c.stairs(48, 65, 2)
    c.cliffs(face=2, keep='WFKG')
    # --- quarters (kerbed pads packed with houses); named buildings sit on their front rows
    d = {}
    d.update(c.quarter(5, 8, 20, 15, POOL_TECT, 'p', first=[('t_house_red', 7, 'SM_HOUSE1', "Saltwife's House door")]))
    c.quarter(23, 8, 41, 15, POOL_TECT, 'c'); c.quarter(49, 8, 66, 15, POOL_TECT, 'c'); c.quarter(69, 8, 83, 15, POOL_TECT, 'p')
    for x0, x1 in ((5, 12), (19, 40), (50, 67), (75, 83)):           # upper promenade: lawn, beds and trees above the cliff
        c.rect(x0, 17, x1 - x0 + 1, 3, '.', 'k'); c.trees(x0 + 1, 18, x1 - x0 - 1)
    d.update(c.quarter(4, 26, 23, 30, POOL_TECT, 'c', first=[('t_pokecenter', 17, 'SM_PC', 'Poke Center door')]))
    d.update(c.quarter(59, 26, 69, 31, POOL_SHOPS, 'p', first=[('t_mart', 61, 'SM_MART', 'Mart door')]))
    c.quarter(72, 27, 83, 33, POOL_TECT, 'c')
    d.update(c.quarter(61, 34, 72, 40, POOL_TECT, 'c', first=[('t_theatre', 63, 'SM_PAGEANT', 'Pageant Hall door')]))
    c.quarter(75, 35, 83, 40, POOL_TECT, 'p')
    c.quarter(4, 36, 19, 50, POOL_TECT + POOL_SHOPS, 'p'); c.quarter(4, 53, 23, 59, POOL_TECT, 'c')
    c.quarter(27, 48, 45, 59, POOL_TECT, 'c'); c.quarter(56, 47, 70, 53, POOL_SHOPS + POOL_TECT, 'p')
    c.quarter(73, 47, 83, 59, POOL_TECT, 'c'); c.quarter(56, 55, 70, 59, POOL_TECT, 'c', beds=False)
    # --- market furniture
    c.stamp('t_cart', 30, 29); c.stamp('t_stall', 50, 28)
    market_stalls(c, 26, 32, 32, 40, 2, 1); market_stalls(c, 52, 34, 58, 42, 2, 2); market_stalls(c, 38, 28, 49, 31, 3, 3)
    market_stalls(c, 34, 42, 48, 46, 3, 4)
    for x, y in ((36, 35), (47, 35), (36, 37), (47, 37)): c.stamp('t_bench', x, y)
    c.trees(41, 36, 3)
    c.scatter_props(26, 28, 58, 46, ['t_barrel', 't_barrel2', 't_crate_pair', 't_barrel'], 10, 'b', 1)
    c.inlay(25, 28, 59, 46, 'b', [3859], 0.07); c.inlay(33, 32, 52, 41, 'c', [3916], 0.10)
    c.inlay(3, 61, 85, 63, 'c', [3916], 0.06); c.inlay(0, 68, 87, 71, 'b', [3859], 0.08)
    # --- street furniture and trees
    street_lamps(c, [(42, 8), (48, 8), (42, 26), (49, 26), (28, 28), (56, 28), (28, 46), (56, 46), (46, 52), (55, 56),
                     (46, 64), (55, 64), (10, 33), (22, 33), (72, 43), (82, 43), (8, 60), (30, 60), (62, 60), (78, 60),
                     (12, 14), (30, 14), (58, 14), (76, 14), (22, 52), (50, 20)])
    for x in (6, 18, 34, 60, 72, 80): c.stamp('t_bench', x, 62)
    c.scatter_props(2, 68, 86, 70, ['t_crate_a', 't_cont_long', 't_crate_pair', 't_barrel', 't_barrel2', 't_cont_green'], 12, 'b', 4)
    c.trees(4, 6, 14); c.trees(24, 6, 13); c.trees(53, 6, 14); c.trees(72, 6, 11)
    for y0 in (8, 16, 38, 46, 56): c.trees(2, y0, 2, 4); c.trees(84, y0 + 2, 2, 4)
    for i, (x, y, rx, ry) in enumerate([(24, 40, 3.5, 2.2), (66, 55, 4, 2), (11, 53, 2, 1.6), (78, 38, 3, 1.5), (8, 24, 5, 1.2),
                                        (30, 25, 6, 1.2), (58, 25, 6, 1.3), (80, 24, 4, 1.3)]):
        c.blob(x, y, rx, ry, 'T', 20 + i)
    # --- events
    E = [ev('SALTMERE', (41, 9)), ev('Juno J1', (42, 40)), ev('Busker', (38, 43)), ev('Caramel seller', (50, 42)),
         ev('Eevee breeder', (40, 62)), ev('Kestrel', (68, 42)), ev('Royal notice', (62, 41))]
    E.append({'type': 'sign', 'at': [46, 63], 'text': 'HARBOUR STAIRS\nDown to the quays and the breakwater.'})
    E.append({'type': 'sign', 'at': [83, 46], 'text': "PLAYERS' GATE\nOld Town and the Pell Playhouse."})
    c.events = E
    c.warp_line([(x, 71) for x in range(48, 54)], 146, [(x, 4) for x in range(42, 48)])
    c.warp_line([(87, y) for y in range(42, 46)], 147, [(1, y) for y in range(36, 40)])
    head = {'id': 140, 'name': 'Saltmere', 'palette': 'city', 'bgm': 'Lerucean Town', 'parent': 0, 'rubric': True,
            'tone': [10, 4, -14, 0],
            'metadata': {'Name': 'Saltmere', 'Outdoor': True, 'ShowArea': True, 'MapPosition': [0, 10, 25], 'BattleBack': 'field',
                         'Weather': ['Rain', 10]},
            'connections': [{'dir': 'N', 'offset': 44, 'to': 541, 'to_offset': 13}, {'dir': 'W', 'offset': 32, 'to': 560, 'to_offset': 12}]}
    c.write('140_saltmere.yaml', head, '# Saltmere - Promenade & Market (140). WRITTEN BY layouts/saltmere_city.py - edit that script.\n')
    return d


# =============================================================================== 146 Harbour & Breakwater
def build_146():
    c = City(W, H, 146)
    def shore(x): return 44 + int(round(1.5 * math.sin(x / 7.0) + 2.0 * (vnoise(x, 0, 31, 6.0) - 0.5))) if x < 66 else 40
    def hgt(x, y):
        if y < 1: return 1
        if ((x - 79.0) / 8.5) ** 2 + ((y - 44.0) / 17.0) ** 2 <= 1.0 + 0.3 * (vnoise(x, y, 5, 4.0) - 0.5): return 1     # headland
        if ((x - 52.0) / 30.0) ** 2 + ((y - 65.0) / 2.6) ** 2 <= 1.0 + 0.5 * (vnoise(x, y, 6, 3.0) - 0.5) and x > 26: return 1  # breakwater
        if y < shore(x) and x < 72: return 0
        return -1
    c.set_heights(hgt)
    for y in range(H):
        for x in range(W):
            if c.ht[y][x] < 0: c.g[y][x] = '~'
            elif c.ht[y][x] == 0: c.g[y][x] = 'k'
    # quay paving: cobbled streets, brick wharf along the water, brick aprons under the sheds, cream loading bays
    for x in range(W):
        for y in range(shore(x) - 7, shore(x)):
            if c.g[y][x] == 'k': c.g[y][x] = 'b'
    for x0, y0, w, h in ((41, 15, 8, 5), (58, 16, 9, 5), (40, 30, 8, 5)): c.rect(x0, y0, w, h, 'c', 'kb')
    c.rect(2, 5, 18, 18, '.', 'k')                                    # salt works on the west side
    for x0, y0, w, h in ((3, 7, 7, 4), (12, 6, 6, 5), (3, 13, 5, 5), (10, 13, 8, 4), (4, 19, 12, 3)): c.rect(x0, y0, w, h, 'p')
    c.rect(41, 1, 8, 6, 'c')
    # piers
    for x0, w, ln in ((9, 3, 11), (25, 3, 15), (43, 4, 10), (60, 3, 12)):
        c.rect(x0, shore(x0 + 1) - 1, w, ln, '=', '~')
    c.path([(72, 38), (76, 44), (79, 56)], 2, 'o', 12, only='.')
    c.wall_v(0, 0, 40); c.tower(0, 38, 3, 3, 3)
    c.stairs(42, 0, 2)
    c.cliffs(face=2, keep='WFKG~=')
    for y in range(H):                                               # rock arm and headland stand in the sea
        for x in range(W):
            if c.g[y][x] == 'C' and c.ht[y][x] < 0: c.g[y][x] = '~'; c.taken[y][x] = False
    d = {}
    d['office'] = c.stamp('t_lodge', 50, 27, 'SM_HARBOUR', 'Harbour Office door')
    c.stamp('t_lighthouse', 77, 36)
    c.stamp('t_ship', 48, shore(46) + 3, force=True); c.stamp('t_ship', 64, 50, force=True)
    c.quarter(22, 6, 40, 13, POOL_DOCK + ['t_house_blue2'], 'b', beds=False); c.quarter(50, 6, 71, 13, POOL_DOCK, 'b', beds=False)
    c.quarter(4, 25, 37, 33, POOL_DOCK + POOL_TECT[:6], 'b', beds=False); c.quarter(57, 25, 70, 32, POOL_TECT[:8], 'p')
    c.quarter(22, 17, 38, 23, POOL_TECT + ['t_stall'], 'p')
    c.scatter_props(3, 14, 70, 43, ['t_cont_green', 't_cont_brown', 't_cont_long', 't_crate_pair', 't_crate_a', 't_crates_b',
                                    't_barrel', 't_barrel2', 't_barrel', 't_table'], 38, 'bck', 1)
    c.inlay(0, 0, 87, 50, 'b', [3859], 0.07); c.inlay(0, 0, 87, 50, 'c', [3916], 0.12)
    street_lamps(c, [(40, 8), (49, 8), (20, 25), (38, 22), (48, 22), (72, 22), (8, 40), (24, 39), (42, 40), (58, 40), (70, 34)])
    for x in (16, 34, 54): c.stamp('t_bench', x, 37)
    for i, (x, y, rx, ry) in enumerate([(80, 30, 5, 3), (82, 52, 4, 5), (74, 50, 2, 3), (11, 11, 1.5, 1.5), (40, 65, 6, 1.2),
                                        (62, 65, 8, 1.2), (19, 20, 1.5, 2)]):
        c.blob(x, y, rx, ry, 'T', 40 + i)
    for x in range(72, 86):
        if c.g[60][x] == '.' and c.ht[60][x] == 1: c.g[60][x] = 'f'
    c.sea_rocks(46, avoid=[(44, 44, 78, 58)])
    ox, oy = d['office']
    E = [ev('The breakwater', (75, 58)),
         {'type': 'sign', 'at': [ox + 2, oy + 1], 'text': 'SALTMERE HARBOUR OFFICE\nAll ferries suspended by order of the quarantine.'},
         {'type': 'npc', 'name': 'Stevedore', 'at': [30, 38], 'sprite': 'NPC 07', 'dir': 'down', 'move': 'random',
          'text': "Stevedore: Tax-barges tie up outside the breakwater and no further.\nFree port means free. [TODO story]"},
         {'type': 'npc', 'name': 'Salt raker', 'at': [10, 12], 'sprite': 'NPC 11', 'dir': 'right',
          'text': 'Salt raker: The pans glitter best at low sun. Mind the brine. [TODO story]'},
         {'type': 'npc', 'name': 'Old angler', 'at': [26, 52], 'sprite': 'NPC 05', 'dir': 'down',
          'text': 'Old angler: Something big has been circling the breakwater since the Shatter talk began. [TODO story]'}]
    c.events = E
    c.warp_line([(x, 3) for x in range(42, 48)], 140, [(x, 70) for x in range(48, 54)])
    head = {'id': 146, 'name': 'Saltmere - Harbour & Breakwater', 'palette': 'city', 'bgm': 'Lerucean Town', 'parent': 140,
            'rubric': True, 'tone': [6, 4, -8, 0],
            'metadata': {'Name': 'Saltmere Harbour', 'Outdoor': True, 'ShowArea': True, 'MapPosition': [0, 10, 25],
                         'BattleBack': 'field', 'Weather': ['Rain', 10]}}
    c.write('146_saltmere_harbour.yaml', head, '# Saltmere - Harbour & Breakwater (146). WRITTEN BY layouts/saltmere_city.py.\n')


# =============================================================================== 147 Old Town
def build_147():
    c = City(W, H, 147)
    ST = [(40, 45), (12, 14), (74, 76)]
    def yu(x): return 27 if flat(x, ST) else 27 + int(round(1.5 * math.sin(x / 9.0 + 2.0) + 1.8 * (vnoise(x, 0, 12, 7.0) - 0.5)))
    def yl(x): return 63 + int(round(1.2 * math.sin(x / 6.0) + 1.5 * (vnoise(x, 0, 13, 5.0) - 0.5)))
    c.set_heights(lambda x, y: 2 if y < yu(x) else (1 if y < yl(x) else -1))
    for y in range(H):
        for x in range(W):
            if c.ht[y][x] < 0: c.g[y][x] = '~'
    c.rect(34, 22, 19, 5, 'c'); c.rect(40, 27, 6, 4, 'k')              # Playhouse forecourt and stair head
    c.rect(30, 31, 28, 12, 'b'); c.rect(34, 34, 20, 6, 'c'); c.rect(36, 36, 16, 2, 'b')    # Playhouse Square
    c.rect(0, 36, 30, 4, 'k'); c.path([(58, 37), (70, 38), (84, 36)], 3, 'k', 2)
    c.path([(4, 13), (18, 12), (33, 14)], 2, 'o', 3); c.path([(54, 14), (70, 12), (84, 13)], 2, 'o', 4)
    c.path([(13, 14), (13, 26)], 2, 'o', 5); c.path([(75, 13), (75, 26)], 2, 'o', 6)
    c.rect(12, 30, 3, 6, 'k'); c.rect(74, 30, 3, 7, 'k')
    c.path([(6, 50), (20, 51), (30, 49), (43, 50), (60, 51), (72, 49), (84, 50)], 2, 'k', 7)
    c.path([(43, 43), (44, 50), (43, 59)], 3, 'k', 8)
    c.path([(20, 40), (21, 50)], 2, 'o', 9); c.path([(66, 40), (65, 50)], 2, 'o', 10)
    c.path([(4, 60), (30, 59), (58, 60), (84, 59)], 2, 'o', 11)
    c.wall_h(0, 87, 0, face=3); c.wall_v(0, 5, 62, gaps=[(36, 39)]); c.wall_v(86, 5, 62)
    c.tower(0, 0, 4, 3, 4); c.tower(84, 0, 4, 3, 4); c.tower(20, 0, 4, 2, 5); c.tower(64, 0, 4, 2, 5)
    c.tower(0, 30, 3, 3, 3); c.tower(0, 40, 3, 3, 3); c.tower(85, 56, 3, 3, 4); c.tower(0, 58, 3, 3, 4)
    c.stairs(40, 26, 2); c.stairs(12, 26); c.stairs(74, 26)
    c.cliffs(face=2, keep='WFKG~')
    for y in range(H):
        for x in range(W):
            if c.g[y][x] == 'C' and c.ht[y][x] < 0: c.g[y][x] = '~'; c.taken[y][x] = False
    d = {}
    d['gym'] = c.stamp('t_hall', 36, 6, 'SM_GYM', 'Playhouse door')
    c.stamp('t_cart', 31, 32); market_stalls(c, 50, 32, 57, 41, 2, 5)
    for x, y in ((36, 35), (50, 35), (36, 38), (50, 38)): c.stamp('t_bench', x, y)
    G = (0, 0, 1, 1, 2)
    c.quarter(5, 5, 33, 12, ['w_manor_a', 'w_manor_b', 'w_ell_a', 'w_longhouse', 'h_manor'], '', gaps=G)
    c.quarter(54, 5, 83, 12, ['w_manor_b', 'w_ell_b', 'w_longhouse', 'w_manor_a'], '', gaps=G)
    c.quarter(3, 15, 11, 25, POOL_TIMBER, '', gaps=G); c.quarter(16, 15, 34, 25, POOL_TIMBER, '', gaps=G)
    c.quarter(54, 15, 73, 25, POOL_TIMBER, '', gaps=G); c.quarter(78, 15, 85, 25, POOL_TIMBER, '', gaps=G)
    c.quarter(3, 30, 11, 35, POOL_TIMBER, '', gaps=G); c.quarter(16, 30, 29, 35, POOL_SHOPS + ['w_house'], 'c')
    c.quarter(59, 30, 72, 35, POOL_SHOPS + ['w_house', 'w_cot'], 'c'); c.quarter(78, 30, 85, 35, POOL_TIMBER, '', gaps=G)
    c.quarter(3, 41, 19, 48, POOL_TIMBER, '', gaps=G); c.quarter(23, 44, 41, 48, POOL_TIMBER + ['t_shop_purple'], '', gaps=G)
    c.quarter(46, 44, 64, 48, POOL_TIMBER, '', gaps=G); c.quarter(68, 41, 85, 48, POOL_TIMBER, '', gaps=G)
    c.quarter(3, 52, 41, 58, POOL_TIMBER, '', gaps=G); c.quarter(46, 52, 85, 58, POOL_TIMBER, '', gaps=G)
    c.scatter_props(30, 31, 57, 42, ['t_barrel', 't_crate_pair', 't_barrel2'], 5, 'b', 1)
    c.scatter_props(3, 14, 84, 60, ['t_barrel', 't_trellis', 't_rock', 't_barrel2', 't_table', 't_crate_pair'], 22, '.', 2)
    c.inlay(30, 31, 57, 42, 'b', [3859], 0.07); c.inlay(34, 22, 54, 40, 'c', [3916], 0.10)
    street_lamps(c, [(35, 26), (51, 26), (39, 31), (46, 31), (29, 35), (58, 35), (29, 43), (58, 43), (8, 41), (18, 41),
                     (64, 41), (80, 40), (41, 52), (46, 56), (10, 52), (30, 52), (60, 53), (78, 52), (8, 15), (26, 15), (60, 15), (80, 15)])
    for i, (x, y, rx, ry) in enumerate([(8, 18, 3, 2), (24, 17, 5, 1.6), (62, 17, 5, 1.6), (80, 18, 3, 2), (30, 8, 2.5, 3), (56, 8, 2.5, 3),
                                        (6, 44, 3, 1.6), (26, 43, 3, 1.5), (62, 43, 3, 1.5), (80, 44, 3, 1.6), (12, 54, 4, 1.4),
                                        (34, 54, 4, 1.4), (54, 54, 4, 1.4), (76, 54, 4, 1.4), (10, 30, 1.5, 2), (32, 28, 2, 1.5),
                                        (56, 29, 2.5, 1.5), (82, 29, 2, 2), (16, 61, 6, 1.2), (50, 61, 7, 1.2), (74, 61, 6, 1.2)]):
        c.blob(x, y, rx, ry, 'T', 60 + i)
    c.sea_rocks(22)
    gx, gy = d['gym']
    E = [ev('Playhouse sign', (gx - 3, gy + 2)),
         {'type': 'sign', 'at': [4, 41], 'text': "PLAYERS' GATE\nWest: Saltmere market and the harbour stairs."},
         {'type': 'npc', 'name': 'Costumier', 'at': [22, 37], 'sprite': 'NPC 12', 'dir': 'down',
          'text': 'Costumier: Every mask in the Pageant is stitched on this lane. Even the ones nobody ordered. [TODO story]'},
         {'type': 'npc', 'name': 'Street player', 'at': [44, 37], 'sprite': 'NPC 08', 'dir': 'down', 'move': 'random',
          'text': 'Street player: A stage is anywhere two people stop to look. Dorian taught us that. [TODO story]'}]
    c.events = E
    c.warp_line([(0, y) for y in range(36, 40)], 140, [(86, y) for y in range(42, 46)])
    head = {'id': 147, 'name': 'Saltmere - Old Town', 'palette': 'city', 'bgm': 'Lerucean Town', 'parent': 140, 'rubric': True,
            'tone': [12, 4, -18, 0],
            'metadata': {'Name': 'Saltmere Old Town', 'Outdoor': True, 'ShowArea': True, 'MapPosition': [0, 10, 25],
                         'BattleBack': 'field', 'Weather': ['Rain', 10]}}
    c.write('147_saltmere_oldtown.yaml', head, '# Saltmere - Old Town (147). WRITTEN BY layouts/saltmere_city.py.\n')


if __name__ == '__main__':
    d = build_140(); build_146(); build_147()
    print('doors 140:', d)
