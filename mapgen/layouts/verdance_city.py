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
from saltmere_city import market_stalls, street_lamps, flat
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
    c = City(W, H, 280, base='k')
    SA = [(48, 56)]; SB = [(48, 56), (16, 18), (84, 86)]
    def ya(x): return 30 if flat(x, SA, 3) else 30 + int(round(1.2 * math.sin(x / 9.0) + 1.6 * (vnoise(x, 0, 3, 7.0) - 0.5)))
    def yb(x): return 55 if flat(x, SB) else 55 + int(round(1.2 * math.sin(x / 7.0 + 1.0) + 1.6 * (vnoise(x, 0, 4, 7.0) - 0.5)))
    c.set_heights(lambda x, y: 3 if y < ya(x) else (2 if y < yb(x) else 1))
    # greens: wall belts, terrace lips, palace lawns
    c.rect(2, 12, 2, 66, '.'); c.rect(100, 12, 2, 66, '.'); c.rect(2, 75, 100, 3, '.')
    for x in range(2, 102):
        for y in list(range(ya(x) - 3, ya(x) + 4)) + list(range(yb(x) - 3, yb(x) + 4)): c.g[y][x] = '.'
    c.rect(2, 12, 44, 15, '.'); c.rect(58, 12, 44, 15, '.')
    # the Kingsway: gate -> market -> cathedral close -> palace arch
    c.rect(49, 10, 6, 78, 'k'); c.rect(46, 12, 12, 16, 'c'); c.rect(47, 14, 2, 11, 'h'); c.rect(55, 14, 2, 11, 'h')
    c.rect(36, 60, 32, 14, 'b'); c.rect(32, 63, 5, 8, 'b'); c.rect(67, 64, 5, 7, 'b'); c.rect(41, 63, 22, 8, 'c'); c.rect(43, 65, 18, 4, 'b')
    c.rect(4, 66, 28, 3, 'k'); c.rect(72, 66, 28, 3, 'k')
    c.rect(22, 36, 24, 14, 'c'); c.rect(24, 38, 20, 10, 'g')                 # cathedral close
    c.rect(16, 52, 3, 8, 'k'); c.rect(84, 52, 3, 8, 'k')
    # Briar Hall's front: keep, flanking towers, curtain walls, the palace arch
    c.wall_h(2, 101, 4, face=4)
    c.wall_h(34, 69, 0, face=6, top='Q', fc='R', thick=4)
    c.tower(28, 0, 6, 5, 7); c.tower(70, 0, 6, 5, 7); c.tower(0, 2, 5, 4, 6); c.tower(99, 2, 5, 4, 6)
    c.tower(14, 3, 4, 3, 5); c.tower(86, 3, 4, 3, 5)
    c.gate_arch(51, 9)
    # outer walls and the Kingsgate
    c.wall_v(0, 12, 82); c.wall_v(102, 12, 82)
    c.wall_h(0, 103, 80, face=3, gaps=[(49, 54)])
    c.tower(43, 77, 6, 4, 6); c.tower(55, 77, 6, 4, 6); c.tower(0, 76, 5, 4, 5); c.tower(99, 76, 5, 4, 5)
    c.tower(22, 78, 4, 3, 5); c.tower(78, 78, 4, 3, 5); c.tower(0, 40, 3, 3, 3); c.tower(101, 44, 3, 3, 3)
    c.stairs(48, 29, 3); c.stairs(48, 54, 3); c.stairs(16, 54); c.stairs(84, 54)
    c.cliffs(face=2, keep='WFKGQR')
    d = {}
    # level 3: palace lawns with glasshouses, beds and tree rows
    for x in (8, 20, 62, 76, 90): c.stamp('t_greenhouse', x, 14)
    for x0 in (6, 34, 60, 88):
        for y0 in (20, 23):
            for xx in range(x0, x0 + 8):
                for yy in (y0, y0 + 1):
                    if c.g[yy][xx] == '.' and not c.taken[yy][xx]: c.g[yy][xx] = 'h'; c.taken[yy][xx] = True
    c.trees(4, 12, 4, 2); c.trees(26, 18, 8); c.trees(60, 18, 2); c.trees(70, 20, 16); c.trees(16, 20, 14); c.trees(96, 14, 4, 6)
    for x in (47, 56): 
        for y in (13, 18, 23): c.stamp('t_lamp', x, y)
    # level 2: cathedral, guild halls (timber), manors
    d['cath'] = c.stamp('h_dome', 29, 37, 'C280_CATH', 'Cathedral door')
    BIG = ['w_manor_a', 'w_manor_b', 'w_ell_a', 'w_longhouse', 'w_ell_b', 'w_house']
    c.house_row(5, 20, 49, BIG); c.house_row(60, 99, 41, BIG); c.house_row(5, 19, 38, ['w_house', 'w_cot', 'w_longhouse'])
    c.trees(23, 34, 22); c.trees(60, 44, 2); c.trees(84, 44, 4); c.house_row(58, 82, 51, ['h_manor', 'w_longhouse', 'w_house', 'w_manor_b'])
    c.house_row(89, 99, 51, POOL_TIMBER); c.house_row(5, 20, 39, ['w_house', 'w_cot', 'w_longhouse'])
    # level 1: market terrace quarters
    d.update(c.quarter(5, 58, 14, 64, POOL_TECT, 'c')); d.update(c.quarter(20, 58, 31, 64, POOL_SHOPS, 'p', first=[('t_pokecenter', 24, 'C280_PC', 'Poke Center door')]))
    d.update(c.quarter(72, 58, 83, 64, POOL_SHOPS, 'p', first=[('t_mart', 75, 'C280_MART', 'Mart door')])); c.quarter(89, 58, 99, 64, POOL_TECT, 'c')
    c.quarter(5, 70, 30, 76, POOL_TECT + POOL_SHOPS, 'c'); c.quarter(73, 70, 99, 76, POOL_TECT + POOL_SHOPS, 'p')
    c.quarter(33, 74, 46, 77, [], 'c'); c.quarter(57, 74, 70, 77, [], 'c')
    c.stamp('t_cart', 37, 61); c.stamp('t_stall', 62, 59); c.stamp('t_greenhouse', 33, 71); c.stamp('t_greenhouse', 64, 75 - 4)
    market_stalls(c, 37, 66, 41, 73, 2, 1); market_stalls(c, 62, 65, 71, 72, 3, 2); market_stalls(c, 44, 60, 60, 63, 3, 3); market_stalls(c, 44, 70, 60, 73, 3, 4)
    for x, y in ((44, 66), (58, 66), (44, 67), (58, 67)): c.stamp('t_bench', x, y)
    c.trees(51, 66, 3)
    c.scatter_props(32, 60, 71, 73, ['t_barrel', 't_barrel2', 't_crate_pair', 't_barrel'], 12, 'b', 1)
    c.inlay(32, 60, 71, 73, 'b', [3859], 0.07); c.inlay(0, 0, 103, 87, 'c', [3916], 0.07)
    street_lamps(c, [(48, 34), (55, 34), (48, 44), (55, 44), (48, 59), (55, 59), (48, 76), (55, 76), (21, 37), (46, 37),
                     (21, 50), (46, 50), (10, 68), (26, 68), (78, 68), (94, 68), (62, 44), (80, 44), (96, 44)])
    banner(c, 50, 6, 1); banner(c, 54, 6, 1); banner(c, 46, 82, 1); banner(c, 57, 82, 1)
    c.pits(26, 'k', 1); c.pits(4, 'c', 2); c.groves(260, 5, 1.8, 3.6)
    cx, cy = d['cath']
    c.events = [
        {'type': 'sign', 'at': [48, 75], 'text': 'VERDANCE\nSeat of the Evergreen Crown. The Kingsgate closes at dusk.'},
        {'type': 'sign', 'at': [cx + 2, cy + 1], 'text': 'CATHEDRAL OF THE EVERGREEN\nEighteen windows, and one left clear.'},
        {'type': 'sign', 'at': [47, 11], 'text': 'BRIAR HALL\nBy leave of Queen Maelis.'},
        {'type': 'npc', 'name': 'Gate serjeant', 'at': [48, 12], 'sprite': 'NPC 07', 'dir': 'down',
         'text': 'Gate serjeant: The Queen holds court in the Thorn Throne room. Mind the roses. [TODO story]'},
        {'type': 'npc', 'name': 'Flower seller', 'at': [46, 67], 'sprite': 'NPC 11', 'dir': 'right', 'move': 'random',
         'text': 'Flower seller: Everything blooms in Verdance. Nobody asks what it costs the soil. [TODO story]'},
        {'type': 'npc', 'name': 'Glasshouse keeper', 'at': [12, 19], 'sprite': 'NPC 12', 'dir': 'down',
         'text': 'Glasshouse keeper: These beds feed the palace. The Rootward gets the trimmings. [TODO story]'}]
    c.warp_line([(52, 9)], 285, [(42, 60)], 'up')
    head = {'id': 280, 'name': 'Verdance - Market Terraces', 'palette': 'city', 'bgm': 'Natural Park', 'parent': 0, 'rubric': True,
            'tone': [-6, 10, -12, 0], 'metadata': dict(META, Name='Verdance')}
    c.write('280_verdance.yaml', head, '# Verdance - Market Terraces (280). WRITTEN BY layouts/verdance_city.py.\n')


def build_285():
    W, H = 84, 64
    c = City(W, H, 285, base='g')
    c.set_heights(lambda x, y: 1)
    c.rect(4, 30, 30, 26, '.'); c.rect(50, 30, 30, 26, '.'); c.rect(39, 26, 6, 38, 'c'); c.rect(4, 6, 18, 20, '.'); c.rect(62, 6, 18, 20, '.')
    c.rect(34, 40, 16, 8, 'c'); c.rect(36, 42, 12, 4, 'b')
    c.path([(8, 34), (20, 44), (34, 44)], 2, 'o', 1, only='.'); c.path([(76, 34), (64, 44), (50, 44)], 2, 'o', 2, only='.')
    # outer ward walls
    c.wall_h(0, 83, 0, face=3); c.wall_v(0, 5, 58); c.wall_v(82, 5, 58)
    c.wall_h(0, 83, 57, face=3, gaps=[(39, 44)])
    c.tower(0, 0, 5, 4, 5); c.tower(79, 0, 5, 4, 5); c.tower(0, 54, 5, 4, 5); c.tower(79, 54, 5, 4, 5)
    c.tower(33, 54, 6, 4, 6); c.tower(45, 54, 6, 4, 6)
    # the keep: roof terrace, tall windowed face, four corner towers, the hall arch
    c.wall_h(24, 59, 3, face=9, top='Q', fc='R', thick=10)
    c.tower(20, 1, 6, 5, 18); c.tower(58, 1, 6, 5, 18); c.tower(30, 8, 5, 4, 5, top='K', fc='G'); c.tower(49, 8, 5, 4, 5, top='K', fc='G')
    c.gate_arch(41, 21)
    for x in (36, 38, 45, 47): banner(c, x, 16, 2)
    # wall stairs up to the west wall-walk, barracks, stable court, gardens
    for y in range(44, 50):
        for x in range(2, 5): c.g[y][x] = 'S'; c.taken[y][x] = True
    c.house_row(6, 20, 24, ['w_longhouse', 'w_house', 'w_cot']); c.house_row(63, 78, 24, ['w_manor_b', 'w_house', 'w_cot'])
    for x0, y0 in ((8, 36), (22, 36), (8, 50), (22, 50), (54, 36), (68, 36), (54, 50), (68, 50)):
        for xx in range(x0, x0 + 6):
            for yy in (y0, y0 + 1):
                if c.g[yy][xx] == '.' and not c.taken[yy][xx]: c.g[yy][xx] = 'h'; c.taken[yy][xx] = True
    c.stamp('t_greenhouse', 14, 40); c.stamp('t_greenhouse', 62, 40)
    c.trees(6, 30, 26); c.trees(52, 30, 26); c.trees(6, 54, 26); c.trees(52, 54, 26); c.trees(4, 8, 2, 14); c.trees(78, 8, 2, 14)
    for x, y in ((38, 30), (45, 30), (38, 38), (45, 38), (38, 50), (45, 50)): c.stamp('t_lamp', x, y - 2)
    for x, y in ((35, 43), (47, 43)): c.stamp('t_bench', x, y)
    c.trees(41, 44, 3, only='b')
    c.inlay(0, 0, 83, 63, 'c', [3916], 0.08)
    c.groves(120, 3, 1.6, 3.0)
    c.events = [
        {'type': 'sign', 'at': [46, 26], 'text': 'BRIAR HALL - THE GREAT HALL\nSeat of the Thorne line.'},
        {'type': 'npc', 'name': 'Hall guard', 'at': [40, 25], 'sprite': 'NPC 07', 'dir': 'down',
         'text': 'Hall guard: Petitioners wait in the Great Hall. Her Majesty sees whom she pleases. [TODO story]'},
        {'type': 'npc', 'name': 'Gardener', 'at': [26, 46], 'sprite': 'NPC 05', 'dir': 'left', 'move': 'random',
         'text': 'Gardener: The Bride Tree never drops a petal. I rake anyway. [TODO story]'}]
    c.warp_line([(42, 21)], 286, [(16, 22)], 'up')
    c.warp_line([(x, 63) for x in range(39, 45)], 280, [(52, 11)] * 6, 'down')
    head = {'id': 285, 'name': 'Briar Hall - Upper Court', 'palette': 'city', 'bgm': 'Natural Park', 'parent': 280, 'rubric': True,
            'tone': [-6, 10, -12, 0], 'metadata': dict(META, Name='Briar Hall')}
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
    c.warp_line([(x, H - 2) for x in (15, 16, 17)], 285, [(42, 23)] * 3, 'down')
    head = {'id': 286, 'name': 'Briar Hall - Great Hall', 'palette': 'city', 'bgm': 'Natural Park', 'parent': 285,
            'tone': [8, 4, -10, 0], 'metadata': {'Name': 'Briar Hall', 'Outdoor': False, 'MapPosition': [0, 14, 12]}}
    c.write('286_briar_hall_great_hall.yaml', head, '# Briar Hall - Great Hall (286). WRITTEN BY layouts/verdance_city.py.\n')


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
    c.write('287_briar_hall_throne.yaml', head, '# Briar Hall - Throne Room (287). WRITTEN BY layouts/verdance_city.py.\n')


if __name__ == '__main__':
    build_280(); build_285(); build_286(); build_287()
