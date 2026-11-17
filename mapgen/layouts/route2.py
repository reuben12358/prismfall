#!/usr/bin/env python3
"""Route 2 (521): Hale's Bramble farmstead in the south, the survey line across the terrace, the Accord checkpoint on the
west road into the Gossamer Wood, and the Glassed Orchard's gate in the east where the glass has started to creep.  62 x 48.
South gate x 40-42 (Route 1).  West road exit (0, 9-11) -> 524 (warp R2_WOOD).  East orchard gate (61, 23) -> 522 (R2_ORCHARD).
Run:  python3 -I layouts/route2.py && python3 -I build.py 521"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wildkit import Wild, save, say, trainer, once, vnoise, FLOWERS, MUSH, B, OBJ

W, H = 62, 48


def build():
    c = Wild(W, H, 521)
    # ---- heights: the farm hollow (0) in the south-west, the terrace (1) across the north, the orchard rise (2) east
    def hf(x, y):
        if x > 46 + 3 * math.sin(y / 5.0) + 2 * (vnoise(x, y, 4, 4.0) - 0.5) and y <= 32: return 1
        if y < 27 + 3.0 * math.sin(x / 7.0) + 2.0 * (vnoise(x, 1, 6, 4.0) - 0.5): return 1
        return 0
    c.set_heights(hf)
    c.notch(39, 41, 24, 1, depth=6)          # lane stairs from the farm up to the terrace
    # ---- water: a brook off the terrace into the farm pond
    c.stream([(30, 0), (29, 6), (25, 12), (22, 18), (21, 24), (19, 30)], 2, 7)
    c.pond(16, 34, 4.5, 3.0, 8)
    # ---- roads
    c.path([(41, 47), (41, 40), (38, 36), (40, 31), (40, 28)], 2, 'd', 1, only='.')         # south gate -> farm -> stairs
    c.path([(40, 22), (37, 18), (30, 14), (22, 11), (12, 10), (0, 10)], 2, 'd', 2, only='.~')    # terrace -> west road
    c.path([(40, 22), (47, 21), (53, 22), (61, 23)], 2, 'd', 3, only='.')                   # east road to the orchard gate
    c.path([(38, 36), (31, 36), (27, 38)], 2, 'd', 4, only='.')                            # farmyard
    for y in range(H):
        for x in range(W):
            if c.g[y][x] == 'd' and c.ht[y][x] < 0: c.g[y][x] = '='
    c.bridge(19, 7, 14, 7)
    for y in range(H):
        for x in range(W):
            if c.g[y][x] == '~' and c.g[y][x - 1 if x else 0] == '=' or (c.g[y][x] == '~' and 9 <= y <= 12 and 20 <= x <= 32):
                c.g[y][x] = '='
    c.stairs(39, 24)
    c.cliffs(face=2, keep='~=')
    # ---- the glass creep: ashen ground and a crystal hedge around the orchard gate
    for y in range(H):
        for x in range(W):
            r = math.hypot(x - 61, (y - 23) * 1.3)
            if r < 9 + 4 * vnoise(x, y, 12, 3.0) and c.g[y][x] == '.': c.g[y][x] = 'a'
            if r < 9 + 4 * vnoise(x, y, 12, 3.0) and c.g[y][x] == 'd': c.g[y][x] = 'D'
    # ---- forest: the wood rising in the north-west, a shelter belt on the east and south rims
    for y in range(H):
        for x in range(W):
            if c.g[y][x] != '.': continue
            if (x + y * 0.8 < 14 + 6 * vnoise(x, y, 21, 5.0)) and not 8 <= y <= 12: c.g[y][x] = 'T'
            elif y < 3 + 3 * vnoise(x, 2, 22, 5.0) and not 26 <= x <= 34: c.g[y][x] = 'T'
            elif x > W - 3 - 3 * vnoise(1, y, 23, 5.0) and not 18 <= y <= 28: c.g[y][x] = 'T'
            elif y > H - 2 - 2.5 * vnoise(x, 3, 24, 5.0) and not 38 <= x <= 44: c.g[y][x] = 'T'
            elif x < 3 + 2 * vnoise(2, y, 25, 4.0) and y > 12: c.g[y][x] = 'T'
    c.blob(7, 22, 5, 6, 'T', 31, only='.', rough=0.8); c.blob(56, 42, 4, 3, 'T', 32, only='.', rough=0.8)
    c.blob(33, 4, 3, 2, 'T', 33, only='.', rough=0.7)
    gate_s, west, east = (41, 47), (0, 10), (61, 23)
    P = {'wim': c.spot(31, 16, 'd.'), 'ada': c.spot(52, 20, 'd.'), 'joss': c.spot(10, 12, 'd.'), 'sign': c.spot(43, 44, '.'),
         'surveyor': c.spot(35, 19, '.'), 'driver': c.spot(54, 24, 'aD.'), 'tutor': c.spot(33, 39, '.d'),
         'guard2': c.spot(5, 8, '.'), 'ball': c.spot(9, 37, '.'), 'berry': c.spot(26, 41, '.'), 'shrine': c.spot(14, 5, '.')}
    c.need(gate_s, west, east)
    c.keep_clear([(0, 9), (0, 10), (0, 11), (1, 10), (61, 22), (61, 23), (41, 47)], 2)
    c.grassfill([(12, 15, 4, 2.5), (33, 26, 4, 2), (50, 13, 4, 3), (8, 42, 3, 3), (56, 37, 3, 3), (24, 22, 3, 2.5), (45, 6, 4, 2.5)])
    c.seal()
    # ---- the farmstead: farmhouse (door south onto the yard), barn, fields, hives, hay, a well, a duck pond
    fh = c.stamp('t_house_orange', 29, 31, 'R2_FARM', 'Farmhouse door', door=(1, 4))
    c.stamp('h_long_g', 22, 31)
    c.fence_ring(43, 34, 12, 8, gaps={(43, 37), (43, 38)})
    for y in range(36, 41):
        for x in range(45, 53):
            if (x + y) % 2 == 0: c.obj('crop', x, y - 1, check=False)
    c.obj('scarecrow', 50, 37, check=False)
    for nm, x, y in (('haystack', 35, 32), ('hay', 26, 37), ('hay_loose', 20, 39), ('haycart', 36, 40), ('beehive', 10, 40), ('beehive2', 13, 41),
                     ('kennel', 34, 34), ('sack', 37, 33), ('pumpkin', 44, 42), ('pumpkin', 46, 43), ('well', 23, 41)):
        c.land(nm, x, y)
    # ---- checkpoint on the west road: a barrier across the lane, fence wings, a lamp and a notice board
    c.land('lantern', 7, 5); c.land('signpost', 9, 6)
    # ---- the survey line: orange flags from the orchard glass, straight across the terrace towards the wood
    flags = []
    for i in range(9):
        fx = int(round(57 - i * 5.6)); fy = int(round(19 - i * 1.35))
        for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1), (1, 1)):
            if c.obj('survey_flag', fx + dx, fy + dy, on='.aD,g'):
                flags.append((fx + dx, fy + dy + 1)); break
    # ---- landmarks: the broken hay-cart on the east road, a roadside shrine, a lookout stump over the farm
    c.land('haycart', 55, 25, on='.a'); c.land('rock_big', 57, 26, on='.a'); c.land('sack', 54, 27, on='.a')
    c.land('tablet', 14, 4); c.land('pillar_moss', 12, 4); c.land('pillar_moss2', 17, 4)
    c.land('gstump', 44, 9); c.land('boulder', 26, 25); c.land('crag', 4, 30)
    # glassed trees by the gate (the creep), crystals in the ash
    for nm, x, y in (('crystal_tree', 55, 14), ('crystal_tree', 57, 30), ('crystal_tree', 51, 28), ('cry_violet', 58, 19), ('cry_teal_s', 53, 18),
                     ('cry_blue_s', 56, 28), ('r_cry_spray', 59, 26), ('cry_violet_m', 50, 16)):
        c.land(nm, x, y, on='.a', r=2)
    # ---- vegetation
    for nm, x, y in (('r_tree_l', 47, 42), ('r_tree_d', 4, 44), ('r_tree_l2', 26, 17), ('r_cherry', 12, 26), ('r_tree_d2', 37, 2), ('r_tree_l5', 52, 7)):
        c.land(nm, x, y)
    c.trees(['t_round', 't_leafy', 't_bright', 't_olive', 'r_tree_l', 'r_tree_d', 'r_pine_d', 'r_tree_l2'], 60, seed=1)
    c.trees(['smalltree', 'bushtree', 'bushtree_f', 'sapling', 'sapling_f', 'pine_s'], 26, seed=2)
    c.trees(['log', 'stump', 'log_moss', 'stump_moss', 'rock_b1', 'rock_b2', 'rock_big', 'log_big', 'fern_big'], 22, seed=3)
    c.trees(['dead3', 'dead4', 'cry_violet_s', 'cry_teal_s', 'stump_grey', 'log_grey'], 8, on='a', seed=4)
    for hx, hy, hw in ((27, 44, 4), (15, 45, 3), (34, 28, 3), (52, 44, 3), (18, 21, 3)):
        c.hedge(hx, hy, hw, 2)
    c.scatter([([1024], 0.80, 2.4, 0.8), ([1035], 0.82, 2.2, 0.8), ([968, 969, 976, 977, 984], 0.80, 2.6, 0.7), ([1041, 1042], 0.83, 2.0, 0.8),
               ([947, 939, 947, 955], 0.60, 3.4, 0.85), ([950, 958, 951], 0.78, 3.0, 0.7)],
              [(1164, 16), (1172, 7), (1180, 2), (1189, 2), (1165, 1), (1173, 1)], density=0.30)
    c.scatter([([1164, 1172, 947], 0.55, 3.0, 0.7)], [(1164, 6), (1172, 3), (1180, 1)], density=0.3, on='a', bleed=True, seed=5)
    c.edge_decor(MUSH, 0.10, by='T', seed=1)
    c.edge_decor([950, 958, 1180], 0.35, by='~', seed=2)
    c.water_decor(0.18)
    c.path_decor([1164], 0.015)
    # ---- events (story/20_SCRIPT_CH0-2.md, "Map 521")
    E = []
    E.append({'type': 'warp', 'name': 'To Gossamer Wood', 'at': [0, 10], 'link': 'R2_WOOD', 'arrive': [1, 10, 'right']})
    E.append({'type': 'warp', 'name': 'To Gossamer Wood 2', 'at': [0, 9], 'to': {'map': 524, 'x': 22, 'y': 56, 'dir': 'up'}})
    E.append({'type': 'warp', 'name': 'To Gossamer Wood 3', 'at': [0, 11], 'to': {'map': 524, 'x': 24, 'y': 56, 'dir': 'up'}})
    E.append({'type': 'warp', 'name': 'To the Glassed Orchard', 'at': [61, 23], 'link': 'R2_ORCHARD', 'arrive': [60, 23, 'left']})
    E.append({'type': 'warp', 'name': 'To the Glassed Orchard 2', 'at': [61, 22], 'to': {'map': 522, 'x': 2, 'y': 37, 'dir': 'right'}})
    E.append({'type': 'sign', 'at': P['sign'], 'text': "ROUTE 2\nBriarwick ahead. Travelers are reminded that the Gossamer Wood is the Crown's forest and the Warden's care. Litterers will be woven into something."})
    hold = "Accord Guard: Hold. Quarantine order: nobody leaves the Landing without papers."
    lifted = ["Accord Guard: Hold. Quarantine order: nobody leaves the Landing without papers.",
              "Accord Guard: ...You've got a Badge Case. A challenger. Right. Challengers pass, that's older law than the quarantine.",
              "Accord Guard: \"Eighteen in Concord, One in Keeping.\" On you go.", {'se': 'Door exit'},
              "The guard drags the barrier off the road."]
    for i, y in enumerate((9, 10, 11)):
        if c.g[y][3] not in 'dD.': continue
        E.append({'type': 'event', 'name': 'Accord barrier %d' % (i + 1), 'at': [3, y],
                  'pages': [{'graphic': {'tile': OBJ['barricade'][0]}, 'trigger': 'action', 'commands': [hold]},
                            {'cond': {'switch': 'CH1_ORCHARD_DONE'}, 'graphic': {'tile': OBJ['barricade'][0]}, 'trigger': 'action',
                             'commands': lifted + [{'script': "$game_self_switches[[521, 0, 'BAR']] = true; $game_map.need_refresh = true"}]},
                            {'cond': {'switch': 'CH1_ORCHARD_DONE'}, 'through': True,
                             'commands': [{'comment': 'gone once the barrier is lifted (see page 4 script condition)'}]}]})
    # page selection by the shared key: a parallel guard event flips each barrier's self switch A once the barrier is lifted
    E.append({'type': 'event', 'name': 'Accord guard', 'at': [4, 8], 'pages': [
        {'graphic': {'sprite': 'NPC 07', 'dir': 'down'}, 'commands': [hold]},
        {'cond': {'switch': 'CH1_ORCHARD_DONE'}, 'graphic': {'sprite': 'NPC 07', 'dir': 'down'}, 'commands': lifted[:3]}]})
    E.append({'type': 'event', 'name': 'Accord guard (aside)', 'at': P['guard2'], 'pages': [
        {'graphic': {'sprite': 'NPC 07', 'dir': 'right'}, 'commands': ["Second Guard: Nobody past. Orders came down this morning."]},
        {'cond': {'switch': 'CH1_ORCHARD_DONE'}, 'graphic': {'sprite': 'NPC 07', 'dir': 'right'}, 'commands': [
            "Second Guard: (low) That's the null one from the dock. Captain said let them through, whatever happens.",
            "Accord Guard: Which captain?",
            "Second Guard: Didn't say. Came down from Crownhaven with a white seal on it.",
            "\\pf[ACCORD_GUARD,deadpan,sweat,Accord guard](They notice you listening.)",
            "\\pf[ACCORD_GUARD,deadpan,sweat,Accord guard (aside)](Both of them, very interested in the sky.)",
            "Accord Guard: Lovely weather."]}]})
    E.append(trainer(P['wim'], 'BUGCATCHER', 'Wim', 'trainer_BUGCATCHER', 'down', 4, "I'm going to be Warden of Briarwick!", "...Assistant Warden."))
    E.append(trainer(P['ada'], 'PICNICKER', 'Ada', 'trainer_PICNICKER', 'left', 4, "My Budew sneezes pollen when it's nervous. It's nervous now.", "Bless you. Bless both of us."))
    E.append(trainer(P['joss'], 'CAMPER', 'Joss', 'trainer_CAMPER', 'right', 3, "Trainers have to battle when their eyes meet! It's in the Accord. Probably.",
                     "The wood's just west. Mind the silk walls."))
    E.append({'type': 'npc', 'name': 'Meridian Surveyor', 'at': P['surveyor'], 'sprite': 'trainer_SCIENTIST', 'dir': 'left',
              'text': "Meridian Surveyor: Mind the orange flags. Survey line for the new Lattice. Straight through to the wood. Trees aren't in the plan, but trees rarely are."})
    E.append({'type': 'npc', 'name': 'Hay-cart Driver', 'at': P['driver'], 'sprite': 'NPC 25', 'dir': 'down',
              'text': "Hay-cart Driver: Used to take me a day to Briarwick and back. Now the east road's all glass and I go round. Day and a half. Glass doesn't pay my horse."})
    E.append({'type': 'npc', 'name': 'Coll (Headbutt tutor)', 'at': P['tutor'], 'sprite': 'NPC 03', 'dir': 'down', 'commands': [
        "Coll: Want your partner to learn to headbutt trees? Things fall out. Usually Pokémon. Once, a boot.",
        {'script': 'pbMoveTutorChoice(:HEADBUTT)'}]})
    # Juno's follower chatter at the first flag (east end) and at the Pecha tree; once each, chapter 2 only
    fx, fy = flags[0] if flags else (55, 21)
    for i, (dx, dy) in enumerate(((0, 1), (-1, 1), (1, 1))):
        cell = (fx + dx, fy + dy)
        if c.walkable(*cell) and not c.o[1][cell[1]][cell[0]]:
            E.append({'type': 'event', 'name': 'Juno flags %d' % (i + 1), 'at': list(cell), 'pages': [
                {'cond': {'switch': 'CH1_ORCHARD_DONE'}, 'trigger': 'touch', 'commands': once(521, 'FLAG', [
                    say('JUNO', 'neutral', "These weren't here in winter. They go right toward the Glasswood. That's... probably fine?")])}]})
    if len(flags) > 2:
        E.append({'type': 'item', 'at': [flags[2][0], flags[2][1]], 'item': 'ANTIDOTE', 'hidden': True, 'name': 'Base of the third flag'})
    E.append({'type': 'berry', 'at': P['berry'], 'berry': 'PECHABERRY'})
    bx, by = P['berry']
    for i, cell in enumerate(((bx, by + 1), (bx - 1, by + 1), (bx + 1, by + 1))):
        if c.walkable(*cell) and not c.o[1][cell[1]][cell[0]]:
            E.append({'type': 'event', 'name': 'Juno pecha %d' % (i + 1), 'at': list(cell), 'pages': [
                {'cond': {'switch': 'CH1_ORCHARD_DONE'}, 'trigger': 'touch', 'commands': once(521, 'PECHA', [
                    say('JUNO', 'happy', "Pecha! Pick it gently. It bruises if you look at it wrong. Like Kestrel.")])}]})
    E.append({'type': 'item', 'at': P['ball'], 'item': 'POKEBALL'})
    E.append({'type': 'sign', 'at': [P['shrine'][0], P['shrine'][1]], 'post': False, 'name': 'Wayside shrine',
              'text': "A wayside shrine to the Loyal Three. Someone has tied a strand of silver silk around it. It hums, very faintly, if you hold your breath."})
    E.append({'type': 'sign', 'at': [9, 8], 'post': False, 'name': 'Checkpoint notice',
              'text': "ACCORD QUARANTINE NOTICE\nNo travel beyond the Landing without papers.\nUnderneath, in pencil: challengers excepted, obviously, it's the LAW."})
    c.events = E
    c.ledge(28, 37, 30)
    head = {'id': 521, 'biome': 'route', 'name': 'Route 2', 'bgm': 'Route 2', 'parent': 0, 'tone': [8, 4, -10, 0],
            'metadata': {'Outdoor': True, 'ShowArea': True, 'MapPosition': [0, 14, 23], 'BattleBack': 'field'},
            'connections': [{'dir': 'S', 'offset': 40, 'to': 520, 'to_offset': 25}]}
    return c.write('521_route2.yaml', head, "# Route 2 (521). WRITTEN BY layouts/route2.py - edit that, not this file.\n")


if __name__ == '__main__':
    save('521_route2.yaml', build())
