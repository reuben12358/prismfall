#!/usr/bin/env python3
"""Verdance, seat of Elowen (the "castle city" showpiece), on the composite city tileset:
  280 Verdance - Market Terraces  (104x88): Kingsgate in the south curtain wall, market terrace, cathedral close,
                                   high town, and the front of Briar Hall across the top (keep, towers, palace arch)
  285 Briar Hall - Upper Court    (84x64): the palace ward on the Thornhill: keep, corner towers, gardens, wall stairs
  286 Briar Hall - Great Hall     (33x25, interior built from the castle kit)
  287 Briar Hall - Throne Room    (27x27, interior; Queen Maelis's Thorn Throne)
Run:  python3 -I layouts/verdance_city.py && python3 -I build.py 280 285 286 287
Act III content: events here are signs, doors and placeholder court NPCs ([TODO story])."""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from citykit import City, STAMPS, POOL_TECT, POOL_TIMBER, POOL_SHOPS, UMBRELLAS, vnoise
from saltmere_city import market_stalls, street_lamps, flat, TIMBER, SMALL, FURN
NOBLE = [n + s for n in ('w_longhouse', 'w_house', 'w_manor_a', 'w_ell_a', 'w_cot') for s in ('', '_s', '_m')]
BIGT = [n + s for n in ('w_manor_a', 'w_manor_b', 'w_ell_a', 'w_longhouse', 'w_ell_b') for s in ('', '_s', '_m')]
BAN = 14384          # Elowen banner (custom sheet): top tile; bottom = +8
THRONE = 14400
META = {'Outdoor': True, 'ShowArea': True, 'MapPosition': [0, 14, 12], 'BattleBack': 'field'}


def banner(c, x, y, layer=2):
    c.tile(BAN, x, y, layer); c.tile(BAN + 8, x, y + 1, layer)


def pillar(c, x, y):
    """No column art exists yet ([TODO art]); a potted shrub marks the bay instead."""
    c.tile(914, x, y + 2, 1); c.taken[y + 2][x] = True


def build_280():
    W, H = 104, 88
    c = City(W, H, 280)
    c.hills([(70, 23, 30, 18, 1, 5), (74, 15, 19, 9.5, 2, 6)], base=0)          # the Thornhill, off-centre to the north-east
    def yr(x): return 52 + int(round(4 * math.sin(x / 16.0) + 2.5 * (vnoise(x, 0, 7, 9.0) - 0.5)))
    for y in range(H):
        for x in range(W):
            if y < 13 and 52 <= x <= 97: c.ht[y][x] = 2
            if abs(y - yr(x)) <= 2: c.ht[y][x] = -1                             # the Briarwater cuts the city in two
            if c.ht[y][x] < 0: c.g[y][x] = '~'
    c.notch(58, 60, 40, 1); c.notch(75, 77, 25, 2)
    # the Kingsway: gate -> slum edge -> bridge -> cathedral fork -> switchback up the Thornhill -> palace arch
    c.path([(36.5, 87), (36.5, 72), (42, 62), (44, 58)], 3, 'k', 1)
    c.rect(43, yr(44) - 4, 3, 9, '=', '~.'); c.rect(61, yr(62) - 4, 3, 9, '=', '~.')
    c.path([(44, 48), (50, 46), (59, 46), (59, 44)], 3, 'k', 2)
    c.path([(59, 38), (62, 33), (70, 30), (76, 29)], 2, 'c', 3); c.path([(76, 23), (74, 16), (71, 12)], 2, 'c', 4); c.rect(66, 10, 11, 3, 'c')
    c.blob(19, 28, 13, 2.5, 'c', 5, only='.'); c.path([(18, 29), (28, 36), (43, 46)], 3, 'c', 6)           # cathedral close and its avenue
    c.path([(3, 40), (16, 40), (30, 40)], 2, 'k', 7); c.path([(3, 49), (18, 49), (32, 49), (42, 48)], 2, 'k', 8)
    c.path([(16, 40), (17, 48)], 2, 'o', 21); c.path([(30, 40), (31, 48)], 2, 'o', 22); c.path([(34, 27), (42, 26), (46, 30)], 2, 'o', 23)
    for i, pts in enumerate(([(3, 67), (16, 67), (34, 67)], [(3, 76), (14, 76), (27, 76), (34, 76)], [(10, 67), (9, 76)], [(22, 67), (23, 76)])):
        c.path(pts, 2, 'o', 30 + i)                                                                         # Rootward alleys
    c.blob(60, 69, 11, 6, 'b', 9, only='.', rough=0.9); c.blob(71, 65, 6, 4, 'b', 10, only='.', rough=0.9); c.blob(60, 69, 5, 2.6, 'c', 11, only='b')
    c.path([(38, 70), (50, 69)], 3, 'k', 12); c.path([(72, 67), (86, 65), (101, 68)], 3, 'k', 13)
    c.path([(62, 62), (62, 57)], 3, 'k', 14); c.path([(62, 47), (60, 45)], 3, 'k', 15)
    c.path([(47, 36), (56, 36), (61, 35)], 2, 'o', 16); c.path([(64, 36), (74, 36), (86, 36), (96, 35)], 2, 'o', 17)
    c.path([(72, 75), (84, 75), (99, 74)], 2, 'o', 18); c.path([(84, 66), (84, 75)], 2, 'o', 19); c.path([(42, 77), (52, 77), (62, 76)], 2, 'o', 20)
    # Briar Hall's front on the hilltop; outer walls with kinks; the Kingsgate west of centre
    for y in range(H):                                   # streets never ford the river: only the two bridges cross
        for x in range(W):
            if c.ht[y][x] < 0 and c.g[y][x] != '=': c.g[y][x] = '~'
    c.wall_h(56, 91, 0, face=6, top='Q', fc='R', thick=4)
    c.tower(50, 0, 6, 5, 7); c.tower(91, 0, 6, 5, 7); c.tower(66, 0, 4, 2, 0, top='K'); c.tower(78, 0, 4, 2, 0, top='K')
    c.gate_arch(70, 9)
    c.wall_h(0, 49, 2, face=3); c.wall_v(0, 7, 84); c.wall_v(102, 9, 80); c.wall_h(97, 103, 5, face=3)
    c.wall_h(0, 45, 80, face=3, gaps=[(34, 39)]); c.wall_h(46, 103, 77, face=3)
    c.tower(28, 77, 6, 4, 6); c.tower(40, 77, 6, 4, 6); c.tower(0, 76, 5, 4, 5); c.tower(99, 73, 5, 4, 5)
    c.tower(12, 78, 4, 3, 5); c.tower(66, 75, 4, 3, 5); c.tower(84, 75, 4, 3, 5); c.tower(0, 0, 5, 4, 5); c.tower(24, 0, 4, 3, 5)
    c.tower(0, 38, 3, 3, 3); c.tower(101, 40, 3, 3, 3); c.tower(0, 58, 3, 3, 3); c.tower(101, 56, 3, 3, 3)
    c.stairs(58, 40); c.stairs(75, 25)
    c.cliffs(face=2, keep='WFKGQR~=')
    for y in range(H):
        for x in range(W):
            if c.g[y][x] == 'C' and c.ht[y][x] < 0: c.g[y][x] = '~'; c.taken[y][x] = False
    d = {}
    # landmarks: the cathedral is a composite (great hall + domed chapter house + bell tower), the biggest mass on the low town
    d['cath'] = c.stamp('t_hall', 9, 10, 'C280_CATH', 'Cathedral door', force=True)
    c.stamp('h_dome', 25, 17, force=True); c.tower(3, 12, 5, 3, 10)
    d['pc'] = c.front_place('t_pokecenter', (52, 64), 'C280_PC', 'Poke Center door')
    d['mart'] = c.front_place('t_mart', (68, 61), 'C280_MART', 'Mart door')
    for x, y in ((58, 14), (84, 13), (92, 18), (60, 20)): c.stamp('t_greenhouse', x, y)
    for x0, y0 in ((62, 17), (80, 18), (86, 22)):
        for xx in range(x0, x0 + 7):
            for yy in (y0, y0 + 1):
                if c.g[yy][xx] == '.' and not c.taken[yy][xx]: c.g[yy][xx] = 'h'; c.taken[yy][xx] = True
    cx, cy = d['cath']; px, py = d['pc']
    E = [{'type': 'sign', 'at': c.snap(38, 78, 'k'), 'text': 'VERDANCE\nSeat of the Evergreen Crown. The Kingsgate closes at dusk.'},
         {'type': 'sign', 'at': c.snap(cx + 3, cy + 2, 'c'), 'text': 'CATHEDRAL OF THE EVERGREEN\nEighteen windows, and one left clear.'},
         {'type': 'sign', 'at': c.snap(68, 11, 'c'), 'text': 'BRIAR HALL\nBy leave of Queen Maelis.'},
         {'type': 'npc', 'name': 'Gate serjeant', 'at': c.snap(73, 11, 'c'), 'sprite': 'NPC 07', 'dir': 'down',
          'text': 'Gate serjeant: The Queen holds court in the Thorn Throne room. Mind the roses. [TODO story]'},
         {'type': 'npc', 'name': 'Flower seller', 'at': c.snap(58, 70, 'bc'), 'sprite': 'NPC 11', 'dir': 'right', 'move': 'random',
          'text': 'Flower seller: Everything blooms in Verdance. Nobody asks what it costs the soil. [TODO story]'},
         {'type': 'npc', 'name': 'Rootward child', 'at': c.snap(15, 66, 'o'), 'sprite': 'NPC 05', 'dir': 'down', 'move': 'random',
          'text': 'Rootward child: Dig under any step here and the soil comes up grey. [TODO story]'},
         {'type': 'npc', 'name': 'Bridge warden', 'at': c.snap(45, 49, 'k'), 'sprite': 'NPC 12', 'dir': 'down',
          'text': 'Bridge warden: Low town south of the Briarwater, high town north. Know which you belong to. [TODO story]'}]
    c.stamp('t_cart', 53, 66); c.stamp('t_stall', 64, 61)
    market_stalls(c, 50, 64, 74, 74, 9, 1)
    for x, y in ((58, 68), (62, 70)): c.stamp('t_bench', x, y)
    for x in (67, 75): banner(c, x, 6, 2)
    for x in (31, 42): banner(c, x, 82, 2)
    # districts of different grain
    c.frontage(SMALL, (2, 56, 35, 79), 'ok', 1); c.backfill(SMALL, (2, 56, 34, 79), 0.9, 2)              # Rootward: tight
    c.frontage(NOBLE, (44, 13, 100, 42), 'oc', 3, skip=0.1)                                               # noble hill: spacious
    c.frontage(TIMBER, (2, 28, 58, 50), 'kco', 4); c.backfill(TIMBER, (2, 31, 44, 48), 0.6, 5)            # burgher quarter
    c.frontage(POOL_TECT + POOL_SHOPS, (36, 54, 101, 79), 'kbo', 6); c.backfill(POOL_TECT, (40, 58, 101, 76), 0.6, 7)
    c.edge_props(FURN, 54, 'kbc', 1)
    c.inlay(0, 0, W - 1, H - 1, 'b', [3859], 0.07); c.inlay(0, 0, W - 1, H - 1, 'c', [3916], 0.08)
    c.greenfill(0.24, 1)
    c.events = E
    c.warp_line([(71, 9)], 285, [(24, 60)], 'up')
    head = {'id': 280, 'name': 'Verdance - Market Terraces', 'palette': 'city', 'bgm': 'Natural Park', 'parent': 0, 'rubric': True,
            'tone': [-6, 10, -12, 0], 'yards_ok': True, 'metadata': dict(META, Name='Verdance')}
    c.write('280_verdance.yaml', head, '# Verdance - Market Terraces (280). WRITTEN BY layouts/verdance_city.py.\n')
    return d


def build_285():
    W, H = 84, 64
    c = City(W, H, 285)
    c.hills([(48, 14, 27, 15, 1, 7)], base=0)
    for y in range(H):
        for x in range(W):
            if y < 27 and 26 <= x <= 70: c.ht[y][x] = 1
            if ((x - 15) / 8.0) ** 2 + ((y - 42) / 5.0) ** 2 < 1.0 + 0.5 * (vnoise(x, y, 4, 3.0) - 0.5): c.ht[y][x] = -1   # the lily pond
            if c.ht[y][x] < 0: c.g[y][x] = '~'
    c.notch(46, 51, 30, 1)
    c.rect(34, 22, 30, 5, 'g'); c.rect(44, 27, 10, 4, 'c')
    c.path([(24.5, 63), (25, 54), (34, 46), (48, 40), (48.5, 35)], 3, 'c', 1)                # the approach bends up to the keep
    c.blob(40, 44, 6, 3.5, 'b', 2, only='.c', rough=0.8)
    c.path([(26, 52), (16, 50), (8, 46)], 2, 'o', 3); c.path([(48, 40), (62, 42), (78, 41)], 2, 'o', 4); c.path([(54, 50), (66, 51), (78, 50)], 2, 'o', 5); c.path([(78, 41), (78, 50)], 2, 'o', 7)
    c.path([(62, 42), (60, 52)], 2, 'o', 6)
    c.wall_h(0, 83, 0, face=3); c.wall_v(0, 5, 58); c.wall_v(82, 5, 55)
    c.wall_h(0, 40, 57, face=3, gaps=[(22, 27)]); c.wall_h(41, 83, 54, face=3)
    c.tower(0, 0, 5, 4, 5); c.tower(79, 0, 5, 4, 5); c.tower(0, 54, 5, 4, 5); c.tower(79, 51, 5, 4, 5)
    c.tower(16, 54, 6, 4, 6); c.tower(28, 54, 6, 4, 6); c.tower(39, 52, 4, 3, 6); c.tower(60, 52, 4, 3, 5)
    c.wall_h(32, 64, 3, face=9, top='Q', fc='R', thick=10)                                 # the keep
    c.tower(28, 1, 6, 5, 18); c.tower(62, 1, 6, 5, 18); c.tower(37, 8, 5, 4, 5); c.tower(54, 8, 5, 4, 5); c.tower(44, 3, 8, 4, 3)
    c.gate_arch(47, 21)
    for x in (42, 44, 51, 53): banner(c, x, 16, 2)
    c.stairs(46, 30, 2)
    c.cliffs(face=2, keep='WFKGQR~')
    for y in range(H):
        for x in range(W):
            if c.g[y][x] == 'C' and c.ht[y][x] < 0: c.g[y][x] = '~'; c.taken[y][x] = False
    for y in range(40, 46):
        for x in range(2, 5): c.g[y][x] = 'S'; c.taken[y][x] = True
    c.stamp('t_greenhouse', 6, 30); c.stamp('t_greenhouse', 12, 29)
    E = [{'type': 'sign', 'at': c.snap(44, 28, 'c'), 'text': 'BRIAR HALL - THE GREAT HALL\nSeat of the Thorne line.'},
         {'type': 'npc', 'name': 'Hall guard', 'at': [46, 23], 'sprite': 'NPC 07', 'dir': 'down',
          'text': 'Hall guard: Petitioners wait in the Great Hall. Her Majesty sees whom she pleases. [TODO story]'},
         {'type': 'npc', 'name': 'Gardener', 'at': c.snap(18, 50, 'o'), 'sprite': 'NPC 05', 'dir': 'left', 'move': 'random',
          'text': 'Gardener: The Bride Tree never drops a petal. I rake anyway. [TODO story]'}]
    c.taken[23][46] = True
    for x, y in ((38, 43), (41, 45)): c.stamp('t_bench', x, y)
    c.frontage(NOBLE, (50, 28, 81, 56), 'o', 1); c.backfill(SMALL, (56, 30, 80, 50), 0.5, 2)   # stable court, barracks
    for x0, y0 in ((6, 34), (22, 36), (8, 50), (30, 34)):
        for xx in range(x0, x0 + 6):
            for yy in (y0, y0 + 1):
                if c.g[yy][xx] == '.' and not c.taken[yy][xx]: c.g[yy][xx] = 'h'; c.taken[yy][xx] = True
    c.edge_props(['t_lamp', 't_lamp', 't_bench', 't_barrel'], 14, 'cgb', 1)
    c.inlay(0, 0, W - 1, H - 1, 'c', [3916], 0.08)
    c.greenfill(0.26, 3)
    c.sea_rocks(3)
    c.events = E
    c.warp_line([(48, 21)], 286, [(16, 22)], 'up')
    c.warp_line([(x, 63) for x in range(22, 28)], 280, [(71, 11)] * 6, 'down')
    head = {'id': 285, 'name': 'Briar Hall - Upper Court', 'palette': 'city', 'bgm': 'Natural Park', 'parent': 280, 'rubric': True,
            'tone': [-6, 10, -12, 0], 'yards_ok': True, 'metadata': dict(META, Name='Briar Hall')}
    c.write('285_briar_hall_court.yaml', head, '# Briar Hall - Upper Court (285). WRITTEN BY layouts/verdance_city.py.\n')


def room(W, H, seed, wallrows=5):
    """Interior shell from the castle kit: black surround, a tall windowed north wall, parapet side/south walls."""
    c = City(W, H, seed, base='x')
    c.set_heights(lambda x, y: 0)
    c.rect(2, wallrows + 2, W - 4, H - wallrows - 4, 'g')
    for x in range(1, W - 1):
        c.g[1][x] = 'Q'; c.g[H - 2][x] = 'W'
        for y in range(2, wallrows + 2): c.g[y][x] = 'R'
    for y in range(1, H - 1):
        c.g[y][1] = c.g[y][W - 2] = 'W' if y > wallrows + 1 else c.g[y][1]
    c.g[1][1] = c.g[1][W - 2] = 'Q'
    for y in range(H):
        for x in range(W):
            if c.g[y][x] in 'QWR': c.taken[y][x] = True
    return c


def build_286():
    W, H = 33, 25
    c = room(W, H, 286)
    c.rect(14, 7, 5, 16, 'p'); c.rect(3, 9, 9, 12, 'c'); c.rect(21, 9, 9, 12, 'c')
    for x in (4, 22):
        for y in (10, 13, 16): c.stamp('t_table', x, y, force=True); c.stamp('t_table', x + 4, y, force=True)
    for x in (12, 20):
        for y in (8, 13, 18): pillar(c, x, y)
    for x in (5, 9, 13, 19, 23, 27): banner(c, x, 3, 2)
    c.gate_arch(15, 6)
    for x in (15, 16, 17): c.g[H - 2][x] = 'p'; c.taken[H - 2][x] = False
    c.scatter_props(3, 7, 29, 22, ['t_barrel', 't_barrel2'], 6, 'g', 1)
    c.inlay(0, 0, W, H, 'c', [3916], 0.08)
    c.events = [
        {'type': 'npc', 'name': 'Steward', 'at': [18, 9], 'sprite': 'NPC 12', 'dir': 'down',
         'text': 'Steward: The throne room lies beyond the arch. Speak when spoken to. [TODO story]'},
        {'type': 'npc', 'name': 'Courtier', 'at': [9, 12], 'sprite': 'NPC 08', 'dir': 'right',
         'text': 'Courtier: Living-wood rafters. They say the hall grows a hand taller every reign. [TODO story]'}]
    c.warp_line([(16, 6)], 287, [(13, 23)], 'up')
    c.warp_line([(x, H - 2) for x in (15, 16, 17)], 285, [(48, 23)] * 3, 'down')
    head = {'id': 286, 'name': 'Briar Hall - Great Hall', 'palette': 'city', 'bgm': 'Natural Park', 'parent': 285,
            'tone': [8, 4, -10, 0], 'metadata': {'Name': 'Briar Hall', 'Outdoor': False, 'MapPosition': [0, 14, 12]}}
    c.write('286_briar_hall_great_hall.yaml', head, '# Briar Hall - Great Hall (286). WRITTEN BY layouts/verdance_city.py.\n', mirror_max=1.0)


def build_287():
    W, H = 27, 27
    c = room(W, H, 287, wallrows=6)
    c.rect(11, 8, 5, 17, 'p'); c.rect(9, 8, 9, 4, 'c'); c.rect(3, 13, 6, 10, 'c'); c.rect(18, 13, 6, 10, 'c')
    for dy in range(3):
        for dx in range(2): c.tile(THRONE + dy * 8 + dx, 12 + dx + (0 if True else 0), 7 + dy, 1)
    c.taken[9][12] = c.taken[9][13] = True
    for x in (9, 17):
        for y in (9, 14, 19): pillar(c, x, y)
    for x in (4, 7, 10, 16, 19, 22): banner(c, x, 3, 2)
    for x in (12, 13, 14): c.g[H - 2][x] = 'p'; c.taken[H - 2][x] = False
    for x in (4, 6, 19, 21):
        for y in (14, 17, 20): c.stamp('t_bench', x, y, force=True)
    c.inlay(0, 0, W, H, 'c', [3916], 0.08)
    c.events = [
        {'type': 'npc', 'name': 'Queen Maelis', 'at': [14, 10], 'sprite': 'NPC 25', 'dir': 'down',
         'text': 'Queen Maelis: You stand before the Thorn Throne of Elowen. [TODO story: court audience, Festival delegation]'},
        {'type': 'npc', 'name': 'Thorn Guard', 'at': [10, 13], 'sprite': 'NPC 07', 'dir': 'right', 'text': 'Thorn Guard: ...'},
        {'type': 'npc', 'name': 'Thorn Guard', 'at': [16, 13], 'sprite': 'NPC 07', 'dir': 'left', 'text': 'Thorn Guard: ...'}]
    c.warp_line([(x, H - 2) for x in (12, 13, 14)], 286, [(16, 8)] * 3, 'down')
    head = {'id': 287, 'name': 'Briar Hall - Throne Room', 'palette': 'city', 'bgm': 'Natural Park', 'parent': 285,
            'tone': [8, 4, -10, 0], 'metadata': {'Name': 'Briar Hall', 'Outdoor': False, 'MapPosition': [0, 14, 12]}}
    c.write('287_briar_hall_throne.yaml', head, '# Briar Hall - Throne Room (287). WRITTEN BY layouts/verdance_city.py.\n', mirror_max=1.0)


def build_295():
    W, H = 31, 29
    c = room(W, H, 295, wallrows=7)
    c.rect(13, 9, 5, 18, 'p'); c.rect(9, 9, 13, 4, 'c'); c.rect(3, 14, 9, 12, 'c'); c.rect(19, 14, 9, 12, 'c')
    for x in (4, 7, 20, 23, 26):
        for y in (15, 18, 21, 24):
            if x != 26 or True: c.stamp('t_bench', min(x, 26), y, force=True)
    for x in (10, 20): c.tile(914, x, 10, 1); c.taken[10][x] = True
    for x in (3, 6, 9, 12, 18, 21, 24, 27): banner(c, x, 4, 2)
    for x in (14, 15, 16): c.g[H - 2][x] = 'p'; c.taken[H - 2][x] = False
    c.inlay(0, 0, W, H, 'c', [3916], 0.08)
    c.events = [{'type': 'exit', 'at': [15, H - 2], 'link': 'C280_CATH'},
                {'type': 'npc', 'name': 'Evergreen prior', 'at': [15, 11], 'sprite': 'NPC 12', 'dir': 'down',
                 'text': 'Prior: Eighteen windows for eighteen Plates. The nineteenth pane is clear, and we do not say why. [TODO story]'}]
    head = {'id': 295, 'name': 'Cathedral of the Evergreen', 'palette': 'city', 'bgm': 'Natural Park', 'parent': 280,
            'tone': [4, 8, -6, 0], 'metadata': {'Name': 'Cathedral of the Evergreen', 'Outdoor': False, 'MapPosition': [0, 14, 12]}}
    c.write('295_cathedral.yaml', head, '# Cathedral of the Evergreen (295). WRITTEN BY layouts/verdance_city.py.\n', mirror_max=1.0)


if __name__ == '__main__':
    d = build_280(); build_285(); build_286(); build_287(); build_295()
    import re
    p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'specs', '281_verdance_interiors.yaml')
    s = open(p).read(); s = re.sub(r'HealingSpot: \[280, \d+, \d+\]', 'HealingSpot: [280, %d, %d]' % (d['pc'][0], d['pc'][1] + 1), s); open(p, 'w').write(s)
