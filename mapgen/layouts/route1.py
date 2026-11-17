#!/usr/bin/env python3
"""Route 1 (520): the farm lane over the sea-cliff heath north of Ferrow's Landing.  44 x 68.
South gate (x 15-17) joins Ferrow's Landing; north gate (x 25-27) joins Route 2.  Three levels: the low meadow by the
town, the heath terrace, and the Beacon Knoll in the north-west with its pond.  A brook crosses the terrace to the sea.
Run:  python3 -I layouts/route1.py && python3 -I build.py 520"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wildkit import Wild, save, say, trainer, once, vnoise, FLOWERS, TUFTS, MUSH, CU

W, H = 44, 68


def build():
    c = Wild(W, H, 520)
    coast = lambda y: 36 + 2.2 * math.sin(y / 6.5) + 2.0 * (vnoise(3, y, 11, 4.0) - 0.5)
    # ---- heights: terrace (1) and knoll (2) as noise-edged masses
    def hf(x, y):
        if ((x - 10) / 11.0) ** 2 + ((y - 9) / 9.5) ** 2 <= 1.0 + 0.35 * (vnoise(x, y, 5, 4.0) - 0.5): return 2
        if y < 44 + 2.2 * math.sin(x / 5.0) + 1.5 * (vnoise(x, 2, 3, 3.0) - 0.5): return 1
        return 0
    c.set_heights(hf)
    for y in range(H):
        for x in range(W):
            if x >= coast(y): c.g[y][x] = '~'; c.ht[y][x] = -1
    c.notch(8, 10, 45, 1, depth=6); c.notch(9, 11, 19, 2, depth=5); c.notch(21, 23, 42, 1, depth=6)
    # ---- brook from the knoll's foot across the terrace to the sea, and the knoll pond
    c.pond(7, 9, 3.6, 2.6, 2)
    c.pond(19, 27, 3.0, 2.2, 3)
    c.stream([(21, 28), (25, 31), (31, 32), (36, 33), (41, 33)], 2, 4)
    # ---- the lane: south gate -> bend west -> steps -> heath -> bridge -> north gate; spurs to the lookout and knoll
    c.path([(16, 67), (16, 60), (13, 55), (9.5, 52), (9.5, 49)], 2, 'd', 1, only='.')
    c.path([(9.5, 43), (11, 40), (17, 38), (22, 38), (27.5, 36)], 2, 'd', 2, only='.')
    c.path([(27.5, 36), (27.5, 29), (30, 25), (30, 21), (27, 14), (26, 8), (26, 0)], 2, 'd', 3, only='.')
    c.path([(30, 26), (33, 26)], 2, 'd', 4, only='.')                       # lookout spur
    c.path([(27, 16), (22, 21), (16, 24), (10.5, 25), (10.5, 23)], 2, 'd', 5, only='.')   # to the knoll steps
    c.path([(10.5, 18), (11, 14), (13, 12)], 2, 'd', 6, only='.')           # knoll top, to the waystone
    c.path([(21, 38), (22, 41)], 3, 'd', 7, only='.'); c.path([(22, 46), (24, 47), (27, 47)], 2, 'd', 8, only='.')
    for y in range(28, 38):
        for x in range(26, 29):
            if c.g[y][x] == '~': c.g[y][x] = '='
    for y in range(H):
        for x in range(W):
            if c.g[y][x] == 'd' and x >= coast(y) - 1: c.g[y][x] = '.' if x < coast(y) else '~'
    c.stairs(8, 45); c.stairs(9, 19); c.stairs(21, 42)
    c.cliffs(face=2, keep='~=')
    for y in range(H):
        for x in range(W):
            if c.g[y][x] == 'C' and c.ht[y][x] < 0: c.g[y][x] = '~'; c.taken[y][x] = False
    # ---- forest border (west and north), noise-edged, 2-5 deep
    for y in range(H):
        for x in range(W):
            if c.g[y][x] != '.': continue
            wd = 2.5 + 2.5 * vnoise(1, y, 21, 5.0)
            nd = 2.0 + 2.5 * vnoise(x, 1, 22, 5.0)
            if x < wd or (y < nd and not 22 <= x <= 30) or (y > H - 1 - nd * 0.8 and not 12 <= x <= 20 and x < 30):
                c.g[y][x] = 'T'
    gate_s, gate_n = (16, 66), (26, 1)
    c.need(gate_s, gate_n, (31, 26), (12, 13), (25, 47))
    P = {'sign': c.spot(18, 62, '.'), 'pim': c.spot(13, 50, 'd.'), 'dory': c.spot(19, 38, 'd.'), 'farmhand': c.spot(23, 46, 'd.'),
         'stile': c.spot(12, 57, '.'), 'potion': c.spot(33, 33, '.', r=4), 'ball': c.spot(6, 13, '.'), 'cache': c.spot(36, 47, '.', r=8),
         'berry': c.spot(34, 47, '.')}
    c.ledge(22, 33, 62); c.ledge(5, 12, 31); c.ledge(30, 34, 15)
    # ---- tall grass shaped by the terrain (meadow pocket, heath, under the knoll, brook bank)
    c.grassfill([(26, 60, 5, 4), (6, 60, 3, 4), (16, 43, 4.5, 2.5), (33, 44, 3, 4), (20, 27, 3, 3), (33, 18, 2.5, 4), (12, 30, 4, 3), (6, 17, 2.5, 2)])
    c.seal()
    # ---- landmarks
    # the stile: a rail fence across the lane mouth with a gap; hedge banks either side
    for x in range(10, 24):
        if c.g[56][x] == '.' and not c.taken[56][x]:
            c.o[1][56][x] = 2073 if x % 3 else 2072; c.taken[56][x] = True; c.sol[56][x] = True
    # Hale's field: fenced crops, scarecrow, hay
    c.fence_ring(24, 48, 10, 7, gaps={(26, 48), (27, 48)})
    for y in range(50, 54):
        for x in range(26, 32):
            if (x + y) % 2 == 0 and c.g[y][x] == '.': c.obj('crop', x, y - 1, check=False)
    c.obj('scarecrow', 31, 49, check=False)
    c.land('haystack', 20, 49); c.land('hay', 34, 51); c.land('haycart', 21, 52); c.land('hay_loose', 19, 51)
    c.land('kennel', 24, 46); c.land('sack', 25, 47)
    # the lookout over the sea: bench, signboard, lamp
    c.land('st:t_bench', 33, 25); c.land('signboard', 31, 24); c.land('st:t_lamp', 35, 23)
    # Beacon Knoll: old waystone by the pond, a well below
    c.land('tablet', 12, 10); c.land('pillar_moss', 10, 11); c.land('pillar_moss2', 14, 10)
    c.land('well', 13, 39); c.land('stump_moss', 5, 13)
    c.land('boulder', 20, 31); c.land('crag', 36, 3) or c.land('crag', 33, 3)
    for i, (gx, gy, rx, ry) in enumerate(((36, 60, 3.2, 3.5), (7, 34, 2.5, 3.0), (33, 3, 3.5, 2.5), (15, 5, 3, 2.5), (4, 53, 2.5, 3.5), (34, 19, 2.0, 2.0), (17, 15, 2.5, 2.2), (23, 55, 2.5, 2.0), (36, 40, 2, 3))):
        c.blob(gx, gy, rx, ry, 'T', 70 + i, only='.', rough=0.7)
    for hx, hy, hw in ((18, 64, 2), (11, 63, 3), (4, 46, 3), (13, 47, 5), (26, 44, 7), (32, 22, 3), (22, 10, 3), (28, 5, 2), (14, 41, 4)):
        c.hedge(hx, hy, hw, 2)
    # ---- trees: great broadleafs on the meadow and heath, small ones in clumps
    for nm, x, y in (('r_tree_l', 20, 58), ('r_tree_d', 3, 49), ('r_tree_l2', 31, 55), ('r_tree_l', 13, 31), ('r_tree_d2', 33, 12),
                     ('r_tree_l3', 4, 22), ('r_tree_l4', 16, 22), ('r_cherry', 2, 3), ('r_tree_l5', 30, 38), ('r_tree_d', 20, 2)):
        c.obj(nm, x, y)
    c.trees(['t_round', 't_leafy', 't_bright', 't_olive', 't_yellow', 'r_tree_l', 'r_tree_d', 'r_pine_d', 'r_tree_l2', 'r_tree_d2'], 80, seed=1, pad=0)
    c.trees(['smalltree', 'bushtree', 'bushtree_f', 'sapling', 'sapling_f', 'pine_s'], 22, seed=2)
    c.trees(['log', 'stump', 'log_moss', 'stump_moss', 'rock_b1', 'rock_b2', 'rock_big', 'log_big'], 16, seed=3)
    c.trees(['fern_big'], 6, seed=4, near='T~')
    # ---- ground detail
    c.scatter([([1024], 0.80, 2.4, 0.8), ([1035], 0.82, 2.2, 0.8), ([968, 969, 976, 977, 984], 0.80, 2.6, 0.7), ([1041, 1042], 0.83, 2.0, 0.8),
               ([947, 939, 947, 955], 0.60, 3.4, 0.85), ([950, 958, 951], 0.78, 3.0, 0.7)],
              [(1164, 16), (1172, 7), (1180, 2), (1170, 1), (1189, 2), (1165, 1), (1173, 1)], density=0.30)
    c.edge_decor(MUSH, 0.10, by='T', seed=1)
    c.edge_decor([1685, 950, 958, 1180], 0.35, by='~', seed=2)
    c.water_decor(0.14, where=lambda x, y: x < coast(y) - 4)
    c.sea_rocks(9)
    c.path_decor([1170, 1164, 1170, 1171], 0.05)
    # ---- events (story/20_SCRIPT_CH0-2.md, "Map 520")
    E = []
    E.append({'type': 'sign', 'at': P['sign'], 'text': "ROUTE 1\nFerrow's Landing - Hale's Bramble - Route 2.\nMind the hedges. The hedges mind you."})
    pim, dory = P['pim'], P['dory']
    E.append(trainer(pim, 'YOUNGSTER', 'Pim', 'trainer_YOUNGSTER', 'down', 4,
                     "A trainer! With a real partner! Fight me, I've got a Bidoof and a dream!", "The dream's fine. The Bidoof needs a minute."))
    E.append(trainer(dory, 'LASS', 'Dory', 'trainer_LASS', 'left', 4, "My Fletchling only knows Tackle and judgment.", "It's judging me now."))
    E.append({'type': 'npc', 'name': 'Farmhand', 'at': P['farmhand'], 'sprite': 'NPC 03', 'dir': 'down', 'move': 'random',
              'text': "Farmhand: Tall grass is where the wild ones are. Juno'll tell you their Latin names. Nobody asked her to learn those."})
    # Juno's catching tutorial: a touch strip across the lane just north of the stile, once, while she follows
    jx = [x for x in range(8, 22) if c.g[54][x] in 'd.' and not c.taken[54][x] and not c.sol[54][x]]
    for i, x in enumerate(jx):
        E.append({'type': 'event', 'name': 'Juno tutorial' + (' %d' % (i + 1) if i else ''), 'at': [x, 54],
                  'pages': [{'cond': {'switch': 'CH1_K1_DONE'}, 'trigger': 'touch',
                             'commands': once(520, 'TUT', [
                                 say('JUNO', 'happy', "Catching tutorial! Weaken it, then throw. Don't throw the Ball AT it, throw it NEAR it."),
                                 say('JUNO', 'happy', "I learned that the hard way. Sorry, Biscuit."),
                                 {'script': 'pbReceiveItem(:POKEBALL, 5)'}])}]})
    E.append({'type': 'item', 'at': P['stile'], 'item': 'POTION', 'hidden': True, 'name': 'Under the stile'})
    E.append({'type': 'sign', 'at': [10, 56], 'post': False, 'name': 'Stile', 'text': "A stile over the hedge bank. Somebody has carved a tally of Wingull into the top rail."})
    E.append({'type': 'sign', 'at': [31, 50], 'post': False, 'name': 'Scarecrow', 'text': "It's wearing a Meridian linesman's cap. Somebody has a sense of humor."})
    E.append({'type': 'sign', 'at': [31, 25], 'post': False, 'name': 'Lookout board', 'text': "GULLWATCH LOOKOUT\nOn a clear day you can see the Dovetail turn for home."})
    E.append({'type': 'sign', 'at': [12, 11], 'post': False, 'name': 'Waystone', 'text': "A waystone, older than the lane. EIGHTEEN IN CONCORD, it says. The last line has been chiselled off."})
    E.append({'type': 'sign', 'at': [13, 40], 'post': False, 'name': 'Old well', 'text': "A dry well. Something small has made a nest of ferry tickets at the bottom."})
    E.append({'type': 'item', 'at': P['potion'], 'item': 'POTION'})
    E.append({'type': 'item', 'at': P['ball'], 'item': 'POKEBALL'})
    E.append({'type': 'item', 'at': P['cache'], 'item': 'REPEL', 'hidden': True, 'name': 'Cliff-foot cache'})
    E.append({'type': 'berry', 'at': P['berry'], 'berry': 'ORANBERRY'})
    E.append(c.fog_event('prismfall_seamist', 36, 0, 200, 1, 0))
    # Chapter 2 opener (story/20_SCRIPT_CH0-2.md, "CHAPTER 2"): Larch sees the PC off at the stile
    ch2 = [say('LARCH', 'neutral', "Eighteen gyms. Briarwick's first, up through the Gossamer Wood. The Warden's a girl called Tamsin Loom. Go easy on her, she inherited the seat in spring and hasn't slept since."),
           say('LARCH', 'neutral', "Write to me. I mean it. Gale Post, every town. If I don't hear from you in a week I start Lecture Two by post."),
           say('JUNO', 'happy', "I'm coming as far as Briarwick! Uncle Rowan wants silk-moth eggs, and I want to see a gym!"),
           {'script': 'pbReceiveItem(:TOWNMAP)'},
           "(Larch has drawn a skull on the Glassed Orchard, and a smaller skull on her own kettle.)",
           "QUEST: \"Eighteen Roads\" - Earn the first badge in Briarwick.",
           {'script': '$game_variables[102] = 2 if $game_variables[102] < 2'},
           {'script': "ev = $game_map.events.values.find { |e| e.name == 'Professor Larch' }\n$game_self_switches[[520, ev.id, 'A']] = true if ev\n$game_map.need_refresh = true"}]
    lx, ly = P['stile']
    E.append({'type': 'event', 'name': 'Professor Larch', 'at': c.spot(lx + 3, ly - 1, '.d', r=3), 'pages': [
        {'commands': []},
        {'cond': {'switch': 'CH1_ORCHARD_DONE'}, 'graphic': {'sprite': 'trainer_PROFESSOR', 'dir': 'down'}, 'commands': once(520, 'CH2', ch2)},
        {'cond': {'self': 'A'}, 'commands': []}]})
    for i, x in enumerate(x for x in range(8, 22) if c.g[ly + 3][x] in 'd' and not c.sol[ly + 3][x]):
        E.append({'type': 'event', 'name': 'Stile send-off %d' % (i + 1), 'at': [x, ly + 3], 'pages': [
            {'cond': {'switch': 'CH1_ORCHARD_DONE'}, 'trigger': 'touch', 'commands': once(520, 'CH2', ch2)}]})
    c.events = E
    
    head = {'id': 520, 'name': 'Route 1', 'bgm': 'Route 1', 'parent': 0, 'tone': [4, 6, -8, 0],
            'metadata': {'Outdoor': True, 'ShowArea': True, 'MapPosition': [0, 14, 24], 'BattleBack': 'field'},
            'connections': [{'dir': 'S', 'offset': 10, 'to': 100, 'to_offset': 28}, {'dir': 'N', 'offset': 25, 'to': 521, 'to_offset': 40}]}
    return c.write('520_route1.yaml', head, "# Route 1 (520). WRITTEN BY layouts/route1.py - edit that, not this file.\n")


if __name__ == '__main__':
    save('520_route1.yaml', build())
