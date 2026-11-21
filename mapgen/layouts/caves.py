#!/usr/bin/env python3
"""layouts/caves.py - the caves on tileset 57 "PF Rejuv Cave" (map builder 13; cavekit.py, cdraw.py):

  544 Brinecut Mine 1F   (salt) DUNGEON_PUZZLES D4 "points and brine": the depot, the Cut (a chasm crossed only by
                         the cart on its trestles), points P1-P3, ends A (the dead-end drift) / B (the ladder gallery)
                         / C (the Thistledown mouth) / D (the buffer: BUMP, back to the depot).  The hidden passage is
                         the old crawlway from drift A up to the points gallery (a chalk X marks it).
  545 Brinecut Mine B1F  (salt) dark (DarkMap): miners' lamps widen the light; the salt lake drains to a causeway only
                         while the 1F cart is parked at B (S519) and the pump is worked (S520).
  564 Gullcry Caves      (slate) D6 "the tide counts your steps": tide clock (V526 / S526), sand bars under water at
                         high tide, the gull roost, a hidden passage behind the weed curtain.

    python3 -I layouts/caves.py [544 545 564]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cavekit import Cave, PIT, FLOOR, TER, TER2, MASS, P1
import hallkit as HK

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S_P1, S_P2, S_P3, S_CART_B, S_LAKE = 516, 517, 518, 519, 520
V_CART = 516
S_TIDE, V_TIDE = 526, 526


def lever(name, x, y, sw, left_txt, right_txt):
    flip = [{'script': 'pfp_flip(%d)' % sw}, {'se': 'Strength push'}]
    return {'type': 'event', 'name': name, 'at': [x, y], 'pages': [
        {'graphic': {'tile': P1('cv_lever_l')}, 'commands': flip + [right_txt]},
        {'cond': {'switch': sw}, 'graphic': {'tile': P1('cv_lever_r')}, 'commands': flip + [left_txt]}]}


def lamp(name, x, y, key):
    return {'type': 'event', 'name': name, 'at': [x, y], 'pages': [
        {'graphic': {'tile': P1('cv_walllamp_off')}, 'commands': [
            {'if': 'pfm_light_lamp(:%s)' % key, 'then': [{'selfswitch': ['A', True]},
                                                         "You trim the old wick and strike a light. The drift opens up around you."],
             'else': ["The lamp is already burning."]}]},
        {'cond': {'self': 'A'}, 'graphic': {'tile': P1('cv_walllamp')}, 'commands': ["The miner's lamp burns steady."]}]}


def atmosphere(script=None, fog='prismfall_cave', opacity=50):
    cmds = [{'raw': [204, [1, fog, 0, opacity, 1, 200, 0, 1]]}] if fog else []
    if script: cmds += [{'script': script}, {'wait': 20}]
    else: cmds += [{'selfswitch': ['A', True]}]
    pages = [{'trigger': 'parallel', 'commands': cmds}]
    if not script: pages.append({'cond': {'self': 'A'}})
    return {'type': 'event', 'name': 'Atmosphere', 'at': [0, 0], 'pages': pages}


# ====================================================================================================== 544
def build_544():
    m = Cave(48, 38, 'S', seed=544, pool='Salt Lake')
    B = m.box
    # --- north: drift A (FLOOR), the points gallery + ladder gallery (TERRACE), C (FLOOR) and the Thistledown adit
    B(3, 5, 9, 13); B(2, 8, 10, 12); B(4, 4, 7, 4)                                   # A, the blind drift
    B(15, 5, 22, 13, TER); B(14, 7, 23, 12, TER); B(17, 4, 20, 4, TER)               # the points gallery
    B(25, 5, 34, 13, TER); B(26, 4, 32, 4, TER); B(24, 8, 26, 11, TER); B(35, 8, 35, 12, TER)   # the ladder gallery
    B(38, 4, 45, 13); B(37, 6, 46, 12); B(41, 0, 43, 3)                              # C, and the adit to the Lea
    # --- the Cut (PIT), the rib across it, the east gallery
    B(2, 14, 41, 22, PIT, 'p'); B(4, 13, 4, 13, PIT, 'p'); B(11, 13, 12, 13, PIT, 'p'); B(36, 13, 36, 13, PIT, 'p')
    B(13, 14, 17, 22)                                                                # the rib (FLOOR)
    B(43, 13, 46, 26); B(42, 20, 46, 25)                                             # C's long way down
    m.mass_at([(42, y) for y in range(13, 20)])
    # --- the depot hall (FLOOR) and its east arm, the south adit to the Saltings
    B(3, 23, 41, 31); B(2, 25, 44, 30); B(5, 32, 34, 33); B(36, 26, 46, 31); B(6, 34, 13, 34)
    B(9, 35, 11, 37)
    B(39, 32, 44, 34)                                                                # the rock-smash alcove
    m.mass_at([(x, 32) for x in range(35, 39)] + [(38, 33), (38, 34), (45, 32), (45, 33), (45, 34)])
    for cells in ([(24, 31), (25, 31), (24, 30)], [(8, 26), (9, 26)], [(33, 33), (34, 33), (34, 32)]):   # rock pillars
        m.mass_at(cells)
    # --- the crawlway: drift A's east wall to the points gallery (the hidden passage)
    m.crawl([(11, 10), (12, 10), (13, 10)])
    m.stairs(14, 13, w=3, n=3, c='.')
    m.ledge(14, 16, 21)
    m.ledge(43, 46, 19)
    # --- the line: depot -> F1 -> A | F2 -> D | F3 -> B | C
    DEPOT, F1, F2, F3 = (20, 25), (20, 18), (29, 18), (34, 18)
    A_END, B_END, C_END, D_END = (6, 12), (34, 12), (40, 12), (29, 22)
    lines = {'A': [DEPOT, F1, (6, 18), A_END], 'D': [DEPOT, F1, F2, D_END],
             'B': [DEPOT, F1, F2, F3, B_END], 'C': [DEPOT, F1, F2, F3, (40, 18), C_END]}
    for pts in lines.values(): m.rails(pts)
    m.junctions |= {F1, F2, F3}
    m.rails([(20, 25), (20, 26)])
    paths = {k: Cave.path(v) for k, v in lines.items()}
    off = {'A': 'U', 'B': 'U', 'C': 'U'}
    m.plan_cliffs(rows=3)
    m.geo = dict(DEPOT=DEPOT, A_END=A_END, B_END=B_END, C_END=C_END, D_END=D_END)
    return m, paths, off


def events_544(m, paths, off):
    E = m.events
    rb = '{' + ', '.join('"%s" => "%s"' % kv for kv in paths.items()) + '}'
    ro = '{' + ', '.join('"%s" => "%s"' % kv for kv in off.items()) + '}'
    E += [
        {'type': 'warp', 'name': 'To the Grey Saltings', 'at': [10, 37], 'link': 'R4_MINE', 'arrive': [10, 36, 'up'], 'se': 'Door exit'},
        {'type': 'warp', 'name': 'To Thistledown Lea', 'at': [42, 0], 'link': 'R3_MINE', 'arrive': [42, 1, 'down'], 'se': 'Door exit'},
        {'type': 'warp', 'name': 'Ladder down', 'at': [30, 6], 'to': {'map': 545, 'x': 7, 'y': 5, 'dir': 'down'}, 'se': 'Door exit'},
        {'type': 'event', 'name': 'Depot cart', 'at': list(m.geo['DEPOT']), 'pages': [
            {'graphic': {'tile': P1('cv_cart_salt')}, 'commands': [
                "A salt cart on the depot line, empty and greased. The line runs north into the Cut.",
                {'choices': ['Ride it', 'Leave it'], 'cancel': 2, 'branches': [
                    [{'script': 'pfm_cart_ride(%s, %s)' % (rb, ro)}], []]}]}]},
        {'type': 'event', 'name': 'Ride cart', 'at': [0, 0], 'pages': [{'graphic': {'sprite': 'pf_minecart', 'dir': 'up'}, 'through': True}]},
    ]
    for k, (x, y), val in (('A', m.geo['A_END'], 1), ('B', m.geo['B_END'], 2), ('C', m.geo['C_END'], 3)):
        pages = [(None, None)] + [({'var': [V_CART, val]}, P1('cv_cart_salt'))] + ([({'var': [V_CART, val + 1]}, None)] if val < 3 else [])
        E.append(HK.tile_event('Cart at ' + k, x, y, pages))
    E += [
        lever('Points P1', 22, 25, S_P1, 'The points clack over. The line now runs WEST, to the dead-end drift.',
              'The points clack over. The line now runs EAST, out across the Cut.'),
        lever('Points P2', 18, 9, S_P2, 'Points P2 clack over. The east line now drops to the buffer stop.',
              'Points P2 clack over. The east line now runs on to the far junction.'),
        lever('Points P3', 21, 9, S_P3, 'Points P3 clack over. The far junction now turns north, to the ladder gallery.',
              'Points P3 clack over. The far junction now runs on east, to the Thistledown adit.'),
        {'type': 'sign', 'name': 'Points board', 'at': [23, 24], 'post': False, 'text':
         "A tin board, painted by hand: P1 WEST = THE BLIND DRIFT. P1 EAST = OUT OVER THE CUT. P2 and P3 are thrown from the points gallery up top. Nobody walks the Cut."},
        {'type': 'sign', 'name': 'Chalk mark', 'at': [10, 10], 'post': False, 'text':
         "A big chalk X on the wall, and under it, in a miner's hand: CRAWL. A thin cold draught comes out of the rock."},
        {'type': 'event', 'name': 'Salt Miner Ebb', 'at': [7, 30], 'pages': [
            {'graphic': {'sprite': 'trainer_HIKER', 'dir': 'right'}, 'commands': [
                "Salt Miner Ebb: Salt mine. Mind your tongue on the walls. Everyone licks the walls once.",
                {'if': 'pfm_gym_won?(:LEADER_DORIAN)', 'then': [
                    "Salt Miner Ebb: That's Dorian's badge on you? Good enough for salt. Here.",
                    {'script': 'pbReceiveItem(:TM98)'},
                    "Salt Miner Ebb: It'll break rock for you once a second Warden's signed off on you. Briarwick's, likely. The Accord likes two opinions about smashing things.",
                    {'selfswitch': ['A', True]}],
                 'else': ["Salt Miner Ebb: Come back with Dorian's badge and I'll show you how we clear rubble."]}]},
            {'cond': {'self': 'A'}, 'graphic': {'sprite': 'trainer_HIKER', 'dir': 'right'}, 'commands': [
                "Salt Miner Ebb: The carts go where the points send them. Throw P1 east and you'll go over the Cut. Where after that is P2's business, and P3's.",
                "Salt Miner Ebb: The pump down in the lake gallery wants a full cart standing over the ladder. Weighs the lever down."]}]},
        {'type': 'trainer', 'at': [30, 28], 'sight': 4, 'dir': 'left', 'sprite': 'trainer_HIKER', 'trainer': ['HIKER', 'Bram'],
         'intro': "Salt in the walls, salt in my boots! Let's go!", 'after': "The lake down there glows at night. Pretty. Don't drink it."},
        {'type': 'trainer', 'at': [17, 6], 'sight': 3, 'dir': 'down', 'sprite': 'trainer_BLACKBELT', 'trainer': ['BLACKBELT', 'Taro'],
         'intro': "I train by punching chalk. Want to see?", 'after': "Chalk wins. Usually."},
        {'type': 'trainer', 'at': [44, 7], 'sight': 4, 'dir': 'left', 'sprite': 'trainer_BLACKBELT', 'trainer': ['BLACKBELT', 'Saul'],
         'intro': "I train in the salt. Builds character. Also thirst.", 'after': "I need a drink. Not salt."},
        {'type': 'item', 'at': [4, 5], 'item': 'HARDSTONE'},
        {'type': 'item', 'at': [37, 29], 'item': 'ESCAPEROPE'},
        {'type': 'item', 'at': [45, 13], 'item': 'REVIVE', 'hidden': True},
        {'type': 'rock_smash', 'name': 'Rock', 'at': [43, 32], 'sprite': 'pf_cave_rock_S'},
        {'type': 'item', 'at': [43, 34], 'item': 'ETHER'},
    ]
    m.keep_clear |= {(20, 26), (10, 36), (42, 1), (6, 11), (34, 11), (40, 11), (21, 25), (19, 25), (10, 10), (14, 10), (43, 31), (43, 33)}


def dress_544(m):
    p = 'S'
    m.tile(P1('cv_hole'), 30, 6)
    m.over.append((2, 10, 9, P1('cv_chalkx')))
    m.mass_at([(39, 32), (40, 32), (41, 32), (39, 33), (40, 33), (41, 33), (39, 34), (40, 34), (41, 34), (42, 32), (44, 32)])
    m.tile(P1('cv_rail_end'), 29, 23)
    # pit-prop frames over the adits
    m.put('cv_frame', 9, 34); m.put('cv_frame', 41, 1)
    # the depot siding: salt carts waiting on a spur west of the main line
    for x in range(14, 20): m.tile(P1('cv_rail_h'), x, 27)
    m.tile(P1('cv_rail_end'), 13, 27)
    for x in (15, 16, 18): m.tile(P1('cv_cart_salt'), x, 27)
    for name, x, y in (('cv_saltblocks', 4, 28), ('cv_saltblocks', 22, 32), ('hb_crates4', 27, 32), ('hb_barrels', 3, 25),
                       ('hb_boxes', 25, 26), ('cv_lamp_on', 12, 24), ('cv_lamp_on', 27, 24), ('cv_lamp_on', 37, 26),
                       ('cv_lamp_on', 6, 31), ('cv_lamp_on', 45, 22), ('cv_lamp_on', 2, 9), ('cv_lamp_on', 39, 8),
                       ('cv_lamp_on', 24, 7), ('cv_lamp_on', 23, 5), ('cv_post', 33, 29), ('cv_post', 17, 30), ('cv_post', 9, 23),
                       ('cv_saltblocks', 31, 6), ('cv_tools', 26, 6), ('hb_barrels', 45, 9)):
        w, h = (2, 1) if name == 'cv_saltblocks' else (4, 1) if name == 'hb_crates4' else (2, 2) if name == 'hb_boxes' else \
            (1, 1) if name == 'cv_tools' else (1, 2)
        if m.free(x, y, w, h, on='.:') and not any((xx, yy) in m.keep_clear for xx in range(x, x + w) for yy in range(y, y + h)):
            m.put(name, x, y)
    for x, y, n in ((8, 29, 'cv_tools'), (26, 31, 'wr_sacks'), (40, 30, 'cv_tools'), (13, 32, 'wr_sacks'), (35, 28, 'wr_sacks')):
        if m.free(x, y, 1, 1, on='.'): m.tile(P1(n), x, y)
    # salt: halite clusters and rose crystal spires against the walls, thickest in the old drifts
    m.solid_props(['cv_xsalt', 'cv_xsalt', p + '_rock0', p + '_rock1'], 9, seed=1, box=(2, 23, 47, 37))
    m.solid_props(['cv_xsalt', 'cv_xsalt', 'cv_xsalt', p + '_rock1'], 9, seed=2, box=(2, 3, 47, 13))
    for x, y in ((3, 10), (37, 7), (46, 10), (33, 5), (2, 29)):
        if m.free(x, y, 1, 2, on='.:') and (x, y + 1) not in m.keep_clear: m.put('cv_xrose2', x, y)
    m.solid_props(['cv_xsalt', p + '_rock0'], 3, seed=3, box=(43, 13, 47, 26))
    for x, y in ((8, 23), (19, 23), (31, 24), (40, 25), (6, 4), (18, 4), (29, 4), (40, 4)):
        if m.cliff[y, x]: m.over.append((2, x, y, P1('cv_walllamp')))
    m.dress(9, seed=1)


# ====================================================================================================== 545
def build_545():
    m = Cave(40, 30, 'S', seed=545, pool='Salt Lake')
    B = m.box
    B(3, 4, 12, 9); B(4, 3, 10, 3); B(2, 5, 13, 8)                    # the ladder chamber
    B(4, 9, 9, 13)                                                    # down to the pump bay
    B(2, 13, 10, 21); B(3, 12, 8, 22)                                 # the pump bay on the west shore
    B(11, 9, 35, 22, FLOOR, 'w'); B(13, 8, 30, 8, FLOOR, 'w'); B(14, 23, 26, 23, FLOOR, 'w')   # the salt lake
    B(30, 12, 33, 17); B(31, 11, 32, 18)                              # the amber islet
    B(4, 23, 13, 27); B(5, 24, 37, 27); B(27, 23, 37, 23); B(30, 28, 34, 28)   # the south gallery
    B(34, 18, 38, 27); B(36, 17, 38, 17)                              # the old workings
    m.mass_at([(36, y) for y in range(9, 17)] + [(37, y) for y in range(9, 17)])
    m.mass_at([(11, 22), (12, 22), (11, 23), (12, 23), (13, 23)])
    m.mass_at([(20, 26), (21, 26), (21, 27)])                         # a fallen block in the south gallery
    m.tidy()
    m.causeway = [(x, 15) for x in range(11, 30)]
    m.plan_cliffs(rows=3)
    return m


def events_545(m):
    from terrain import NB2AUTO
    E = m.events
    E += [
        {'type': 'warp', 'name': 'Ladder up', 'at': [7, 4], 'to': {'map': 544, 'x': 30, 'y': 7, 'dir': 'down'}, 'se': 'Door exit'},
        {'type': 'event', 'name': 'Atmosphere', 'at': [0, 0], 'pages': [{'trigger': 'parallel', 'commands': [{'script': 'pfm_cave_light'}, {'wait': 12}]}]},
        {'type': 'event', 'name': 'Pump wheel', 'at': [8, 14], 'pages': [
            {'commands': [
                "An old brine pump: a big spoked wheel over a sump, and a counterweight lever that runs up a shaft to the ladder gallery above.",
                {'if_switch': [S_LAKE, True], 'then': ["The lake is drained to its salt bed. The wheel is chocked."], 'else': [
                    {'if_switch': [S_CART_B, True], 'then': [
                        "The counterweight lever is down: something heavy is standing on it up above.",
                        "You lean on the wheel. It bites. Somewhere below, a sluice coughs open...",
                        {'se': 'Anim/Water1'}, {'tone': [40, 40, 40, 0, 10]}, {'wait': 10}, {'tone': [0, 0, 0, 0, 20]},
                        {'switch': [S_LAKE, True]},
                        "The glowing brine sinks away down the sump. A ridge of white salt rises out of the lake, all the way to the islet."],
                     'else': ["You lean on the wheel. It spins free: the counterweight lever above is up.",
                              "Painted on the frame: CART ON THE LADDER LINE BEFORE PUMPING. B."]}]}]}]},
        {'type': 'trainer', 'at': [27, 25], 'sight': 4, 'dir': 'left', 'sprite': 'trainer_HIKER', 'trainer': ['HIKER', 'Gorse'],
         'intro': "Down here the salt sings. You hear it?", 'after': "Old miners say the singing started the night of the Prismfall."},
        {'type': 'trainer', 'at': [11, 6], 'sight': 3, 'dir': 'left', 'sprite': 'trainer_HIKER', 'trainer': ['HIKER', 'Holt'],
         'intro': "Three days I've been down here. Nobody told me it was a shortcut.", 'after': "It IS a shortcut? To WHERE?"},
        {'type': 'item', 'at': [32, 14], 'item': 'OLDAMBER'},
        {'type': 'item', 'at': [31, 17], 'item': 'NUGGET', 'hidden': True},
        {'type': 'item', 'at': [37, 26], 'item': 'SUPERPOTION'},
        {'type': 'sign', 'name': 'Salt lake', 'at': [10, 19], 'post': False, 'text':
         "The salt lake glows a soft, cold blue-white. Far out on the water there's a low islet, and something amber catches the light on it."},
    ]
    for i, (x, y) in enumerate(((5, 4), (10, 12), (17, 23), (24, 23), (35, 17)), 1):
        E.append(lamp('Lamp %d' % i, x, y, 'bc_lamp_%d' % i))
    n = len(m.causeway)
    for i, (x, y) in enumerate(m.causeway):
        b = (64 if i > 0 else 0) | (4 if i < n - 1 else 0)
        E.append({'type': 'event', 'name': 'Causeway %d,%d' % (x, y), 'at': [x, y], 'pages': [
            {}, {'cond': {'switch': S_LAKE}, 'graphic': {'tile': P1('S_floorpatch_%02d' % NB2AUTO[b])}}]})
    m.keep_clear |= {(7, 5), (8, 15), (9, 15), (10, 15), (30, 15), (24, 24)} | set(m.causeway)


def dress_545(m):
    p = 'S'
    m.put('cv_ladder', 7, 3)
    m.put('cv_pump', 7, 13)
    for x, y in ((20, 24), (21, 24), (22, 24), (23, 24), (24, 24)): m.tile(P1('cv_rail_h'), x, y)
    m.tile(P1('cv_rail_end'), 19, 24); m.tile(P1('cv_cart'), 23, 24)
    for name, x, y in (('cv_frame', 30, 25), ('cv_saltblocks', 4, 25), ('cv_tools', 3, 7), ('wr_sacks', 12, 26),
                       ('cv_post', 16, 25), ('cv_post', 34, 21), ('hb_barrels', 37, 19)):
        L = __import__('cavekit').STAMPS[name]['layers']; w, h = len(L[0][0]), len(L[0])
        if m.free(x, y, w, h, on='.') and not any((xx, yy) in m.keep_clear for xx in range(x, x + w) for yy in range(y, y + h)):
            m.put(name, x, y)
    m.solid_props(['cv_xsalt', 'cv_xsalt', p + '_rock0'], 10, seed=4)
    for x, y in ((3, 18), (30, 12), (33, 16), (38, 22), (12, 5)):
        if m.free(x, y, 1, 2, on='.') and (x, y + 1) not in m.keep_clear: m.put('cv_xrose2', x, y)
    for x, y in ((2, 15), (6, 21), (33, 13), (25, 27), (36, 25), (13, 27)):        # cold-glow fungus by the brine
        if m.free(x, y, 1, 1, on='.') and (x, y) not in m.keep_clear: m.over.append((2, x, y, P1('cv_fung0'))); m.taken[y, x] = True
    # halite cubes and rose spires standing in the brine (solid; never on the causeway)
    for x, y, n in ((14, 11, 'cv_xsalt'), (21, 19, 'cv_xsalt'), (26, 11, 'cv_xsalt'), (34, 20, 'cv_xsalt'), (17, 21, 'cv_xsalt'),
                    (28, 19, 'cv_xsalt'), (12, 20, 'cv_xsalt')):
        if m.cls[y, x] == 'w' and (x, y) not in m.causeway: m.over.append((2, x, y, P1(n)))
    m.dress(10, seed=2)


# ====================================================================================================== 564
def build_564():
    m = Cave(46, 40, 'L', seed=564, pool='Sea Cave')
    B = m.box
    # the south chamber (FLOOR), the mouth to the cliffs below
    B(3, 29, 15, 37); B(2, 31, 16, 36); B(6, 38, 9, 39)
    # TEACH: the little inlet east of the south chamber, its bar and the far alcove
    B(17, 30, 23, 35, FLOOR, 'w'); B(24, 31, 28, 35)
    # the west gallery climbing north (FLOOR -> stairs -> TERRACE) and the high gallery across the north-west
    B(3, 18, 8, 28); B(2, 20, 9, 26)
    B(3, 7, 9, 17, TER); B(2, 9, 10, 15, TER)
    B(10, 4, 18, 9, TER); B(9, 5, 19, 8, TER)
    # the north chamber (TERRACE) and its landing on the basin (FLOOR)
    B(20, 2, 37, 9, TER); B(22, 1, 35, 10, TER); B(31, 0, 34, 0, TER)
    # the basin: sea water with deep holes, sand bars that dry at low tide
    B(10, 14, 33, 27, FLOOR, 'w'); B(12, 13, 31, 28, FLOOR, 'w')
    B(21, 11, 30, 15); B(22, 16, 26, 16)                              # the landing under the north chamber
    B(15, 28, 18, 29)                                                 # the bar head in the south chamber
    B(34, 10, 39, 24); B(35, 25, 38, 27)                              # the east shelf (a side way off the north chamber)
    B(31, 28, 38, 33); B(33, 34, 38, 36)                              # its lobe
    B(42, 15, 45, 21); B(43, 14, 44, 22)                              # the hidden grotto
    m.mass_at([(11, 28), (12, 29), (10, 27), (31, 11), (32, 11)])
    m.tidy()
    m.crawl([(40, 18), (41, 18)])
    m.stairs(4, 17, w=3, n=3, c='.')
    m.stairs(25, 10, w=3, n=3, c='.')
    m.stairs(35, 9, w=3, n=3, c='.')
    m.ledge(3, 6, 25)
    teach = [(x, 33) for x in range(17, 24)]
    twist = [(17, 27), (17, 26), (17, 25), (18, 25), (19, 25), (20, 25), (20, 24), (20, 23), (21, 23), (22, 23), (23, 23),
             (23, 22), (23, 21), (23, 20), (23, 19), (24, 19), (24, 18), (24, 17), (24, 16)]
    spit = [(25, 17), (26, 17)]
    for x, y in teach + twist + spit:
        m.cls[y, x] = 'b'; m.ht[y, x] = FLOOR
    m.cls[17, 27] = '.'; m.ht[17, 27] = FLOOR                          # the pearl rock at the end of the spit
    assert len(twist) == 19
    m.bars = teach + twist + spit
    m.plan_cliffs(rows=3)
    return m


def events_564(m):
    E = m.events
    E += [
        {'type': 'warp', 'name': 'South mouth', 'at': [7, 39], 'link': 'R6_CAVE_S', 'arrive': [7, 38, 'up'], 'se': 'Door exit'},
        {'type': 'warp', 'name': 'North mouth', 'at': [32, 0], 'link': 'R6_CAVE_N', 'arrive': [32, 1, 'down'], 'se': 'Door exit'},
        {'type': 'event', 'name': 'Tide clock', 'at': [0, 39], 'pages': [{'trigger': 'parallel', 'commands': [
            {'script': 'pfp_step_hook(564, :tide) { pfm_tide_tick }'}, {'wait': 120}]}]},
        {'type': 'event', 'name': 'Gull roost', 'at': [14, 28], 'pages': [{'graphic': {'tile': P1('cv_nest')}, 'commands': [{'script': 'pfm_gulls'}]}]},
        {'type': 'event', 'name': 'Tide mark', 'at': [13, 30], 'pages': [
            {'graphic': {'tile': P1('cv_tide_dry')}, 'commands': ["A rock with a pale tide-mark band. It's dry: the sea is out."]},
            {'cond': {'switch': S_TIDE}, 'graphic': {'tile': P1('cv_tide_wet')}, 'commands': ["The rock is black and running wet to the band. The sea is in."]}]},
        {'type': 'sign', 'name': 'Old Asta\'s board', 'at': [10, 34], 'post': False, 'text':
         "Chalked on a plank: TIDE TURNS EVERY 24 STEPS (OR SO). BARS DRY ON THE EBB. WATCH THE GULLS: THEY LIFT ON THE TURN. - A."},
        {'type': 'sign', 'name': 'Shaft', 'at': [29, 5], 'post': False, 'text':
         "A shaft drops toward the tide pools below. The ladder's rungs are rusted away under the third one. Nobody's been down in years."},
        {'type': 'trainer', 'at': [36, 15], 'sight': 4, 'dir': 'down', 'sprite': 'trainer_HIKER', 'trainer': ['HIKER', 'Torvald'],
         'intro': "Gull droppings and sea spray - my favourite cave!", 'after': "Hear them? Gullcry. Every tide."},
        {'type': 'item', 'at': [44, 17], 'item': 'REVIVE'},
        {'type': 'item', 'at': [27, 33], 'item': 'PEARL', 'hidden': True},
        {'type': 'item', 'at': [27, 17], 'item': 'BIGPEARL'},
        {'type': 'item', 'at': [36, 31], 'item': 'POTION'},
        {'type': 'item', 'at': [26, 34], 'item': 'HEARTSCALE'},
        {'type': 'sign', 'name': 'Weed curtain', 'at': [39, 18], 'post': False, 'text':
         "Dried kelp hangs over a crack in the rock like a curtain. There's a draught behind it, and the sound of the sea."},
    ]
    for x, y in m.bars:
        E.append({'type': 'event', 'name': 'Tide %d,%d' % (x, y), 'at': [x, y], 'pages': [
            {}, {'cond': {'switch': S_TIDE}, 'graphic': {'tile': P1('cv_flood')}}]})
    m.keep_clear |= {(7, 38), (32, 1), (14, 27), (13, 31), (10, 35), (29, 6), (39, 18), (39, 17), (39, 19), (17, 28), (14, 29), (24, 15)} | set(m.bars)


def dress_564(m):
    p = 'L'
    m.tile(P1('cv_hole'), 29, 5)
    m.over.append((2, 40, 18, P1('cv_kelp1')))
    for x, y in ((14, 15), (27, 20), (21, 27)):
        if m.inb(x + 1, y + 2): m.stamps.append(('cv_shaft', x, y))
    for name, x, y in (('cv_drift', 4, 35), ('cv_drift', 33, 30), ('pf_whalebone', 2, 32), ('cv_frame', 31, 0)):
        L = __import__('cavekit').STAMPS[name]['layers']; w, h = len(L[0][0]), len(L[0])
        if m.free(x, y, w, h, on='.:') and not any((xx, yy) in m.keep_clear for xx in range(x, x + w) for yy in range(y, y + h)):
            m.put(name, x, y)
    m.solid_props(['cv_barn', 'cv_barn', p + '_rock0', 'cv_nest', 'cv_xsea'], 14, seed=5)
    m.solid_props(['cv_nest', 'cv_nest', 'cv_barn'], 5, seed=6, box=(20, 1, 38, 10))
    for x, y in ((12, 13), (31, 13), (10, 20)):
        if m.free(x, y, 1, 2, on='.:') and (x, y + 1) not in m.keep_clear: m.put('cv_xsea2', x, y)
    for x, y in ((24, 3), (35, 6), (8, 12), (5, 21), (36, 14)):
        if m.cliff[y, x]: m.over.append((2, x, y, P1('cv_guano')))
    m.dress(10, groups=[(['L_fd0', 'L_fd1', 'L_fd2', 'cv_kelp0', 'cv_kelp1', 'cv_wrack'], 6), (['L_rubble0', 'L_rubble1'], 2)], seed=3)


def main(which):
    import yaml
    if '544' in which:
        m, paths, off = build_544()
        events_544(m, paths, off)
        dress_544(m)
        m.paint()
        m.preview('/tmp/mb13/p544.png', scale=0.5)
        head = {'id': 544, 'name': 'Brinecut Mine 1F', 'parent': 540, 'bgm': 'Cave', 'field': 'CAVE',
                'metadata': {'Name': 'Brinecut Mine', 'MapPosition': [0, 11, 23], 'BattleBack': 'cave1'},
                'tone': [-8, -10, -4, 10], 'fog': {'name': 'prismfall_cave', 'opacity': 36, 'blend': 1, 'zoom': 100, 'sx': 1, 'sy': 0},
                'gates': [{'name': 'the Cut is crossed only by cart', 'from': [[10, 36]],
                           'sealed': [[6, 9], [18, 10], [30, 9], [41, 9], [44, 15], [15, 16]]},
                          {'name': 'from the Thistledown adit the drift and the points gallery are shut', 'from': [[42, 1]],
                           'sealed': [[6, 9], [18, 10], [30, 9]]}],
                '_file': '544_brinecut_mine.yaml'}
        m.write(544, head, comment='# GENERATED by mapgen/layouts/caves.py (map builder 13): Brinecut Mine 1F, DUNGEON_PUZZLES D4.\n'
                                  '# Edit the layout script, not this file.\n')
        print(paths)
    if '564' in which:
        m = build_564(); events_564(m); dress_564(m); m.paint()
        m.preview('/tmp/mb13/p564.png', scale=0.5)
        head = {'id': 564, 'name': 'Gullcry Caves', 'parent': 561, 'bgm': 'Cave', 'field': 'CAVE',
                'metadata': {'Name': 'Gullcry Caves', 'MapPosition': [0, 8, 21], 'BattleBack': 'cave1'},
                'tone': [-12, -6, 6, 16], 'fog': {'name': 'prismfall_seamist', 'opacity': 34, 'blend': 1, 'zoom': 100, 'sx': 1, 'sy': 0},
                '_file': '564_gullcry_caves.yaml'}
        m.write(564, head, comment='# GENERATED by mapgen/layouts/caves.py (map builder 13): Gullcry Caves, DUNGEON_PUZZLES D6 (the tide).\n'
                                  '# Tide clock: V526 steps since the turn, S526 high tide (pfm_tide_tick).  Edit the layout script.\n')
    if '545' in which:
        m = build_545(); events_545(m); dress_545(m); m.paint()
        m.preview('/tmp/mb13/p545.png', scale=0.5)
        head = {'id': 545, 'name': 'Brinecut Mine B1F', 'parent': 544, 'bgm': 'Cave', 'field': 'CAVE',
                'metadata': {'Name': 'Brinecut Mine', 'MapPosition': [0, 11, 23], 'BattleBack': 'cave1', 'DarkMap': True},
                'tone': [-14, -12, -2, 20], 'fog': {'name': 'prismfall_cave', 'opacity': 44, 'blend': 1, 'zoom': 100, 'sx': 1, 'sy': 0},
                'gates': [{'name': 'the amber islet only over the drained lake', 'from': [[7, 5]], 'sealed': [[32, 15], [31, 13]]}],
                '_file': '545_brinecut_mine_b1f.yaml'}
        m.write(545, head, comment='# GENERATED by mapgen/layouts/caves.py (map builder 13): Brinecut Mine B1F, the salt lake (D4 combine).\n'
                                  '# Dark map: the miners\' lamps widen the light (pfm_light_lamp).  Edit the layout script, not this file.\n')


if __name__ == '__main__':
    main(sys.argv[1:] or ['544', '545', '564'])
