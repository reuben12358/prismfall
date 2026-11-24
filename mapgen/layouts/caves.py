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
    ST = __import__('cavekit').STAMPS
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
    # Rich mining depot & gallery hardware: salt stacks, crates, barrels, lanterns, timber supports, & tools
    for name, x, y in (
        ('cv_saltblocks', 4, 28), ('cv_saltblocks', 22, 32), ('cv_saltblocks', 31, 6), ('cv_saltblocks', 39, 27),
        ('hb_crates4', 27, 32), ('hb_barrels', 3, 25), ('hb_barrels', 45, 9), ('hb_barrels', 38, 25),
        ('hb_boxes', 25, 26), ('hb_boxes', 13, 30),
        ('cv_lamp_on', 12, 24), ('cv_lamp_on', 27, 24), ('cv_lamp_on', 37, 26), ('cv_lamp_on', 44, 26),
        ('cv_lamp_on', 6, 31), ('cv_lamp_on', 45, 22), ('cv_lamp_on', 2, 9), ('cv_lamp_on', 39, 8),
        ('cv_lamp_on', 24, 7), ('cv_lamp_on', 23, 5), ('cv_lamp_on', 14, 7),
        ('cv_post', 33, 29), ('cv_post', 17, 30), ('cv_post', 9, 23), ('cv_post', 34, 25), ('cv_post', 41, 24), ('cv_post', 28, 7),
        ('cv_tools', 26, 6), ('cv_tools', 11, 28),
    ):
        L = ST[name]['layers']; w, h = len(L[0][0]), len(L[0])
        if m.free(x, y, w, h, on='.:') and not any((xx, yy) in m.keep_clear for xx in range(x, x + w) for yy in range(y, y + h)):
            m.put(name, x, y)
    for x, y, n in ((8, 29, 'cv_tools'), (26, 31, 'wr_sacks'), (40, 30, 'cv_tools'), (13, 32, 'wr_sacks'),
                    (35, 28, 'wr_sacks'), (5, 7, 'wr_sacks'), (34, 9, 'wr_sacks'), (45, 16, 'cv_tools')):
        if m.free(x, y, 1, 1, on='.') and (x, y) not in m.keep_clear: m.tile(P1(n), x, y)
    # Rich halite, rose, blue, & sea crystal formations (matching 545 B1F crystal cavern directly below!)
    m.solid_props(['cv_xsalt', 'cv_xblue', 'cv_xsea', p + '_rock0', p + '_rock1'], 18, seed=1, box=(2, 23, 47, 37))
    m.solid_props(['cv_xsalt', 'cv_xblue', 'cv_xsea', p + '_rock1'], 15, seed=2, box=(2, 3, 47, 13))
    m.solid_props(['cv_xsalt', 'cv_xblue', 'cv_xsea', p + '_rock0'], 6, seed=3, box=(42, 13, 47, 26))
    for name, x, y in (
        # Tall rose/blue/sea crystal spires framing the drifts, ladder gallery down to 545, and depot walls
        ('cv_xrose2', 3, 10), ('cv_xblue2', 8, 5), ('cv_xsea2', 14, 5), ('cv_xrose2', 22, 5),
        ('cv_xblue2', 27, 5), ('cv_xrose2', 33, 5), ('cv_xsea2', 37, 7), ('cv_xrose2', 46, 10),
        ('cv_xblue2', 45, 19), ('cv_xrose2', 2, 29), ('cv_xsea2', 4, 33), ('cv_xblue2', 15, 32),
        ('cv_xrose2', 24, 30), ('cv_xsea2', 32, 31), ('cv_xblue2', 42, 29), ('cv_xrose2', 46, 26),
        ('cv_xsea2', 14, 15), ('cv_xblue2', 17, 16),
    ):
        if m.free(x, y, 1, 2, on='.:') and (x, y) not in m.keep_clear and (x, y + 1) not in m.keep_clear:
            m.put(name, x, y)
    # Bioluminescent brine fungi dotting the Cut chasm rims & damp salt drifts
    for x, y in ((5, 11), (8, 11), (15, 11), (24, 11), (31, 11), (38, 11), (45, 11),
                 (6, 23), (11, 23), (24, 23), (33, 23), (41, 23), (14, 21), (17, 21), (4, 31), (36, 31)):
        if m.free(x, y, 1, 1, on='.') and (x, y) not in m.keep_clear:
            m.over.append((2, x, y, P1('cv_fung0'))); m.taken[y, x] = True
    # Miners' wall sconces across every gallery cliff face
    for x, y in ((8, 23), (19, 23), (31, 24), (40, 25), (6, 4), (18, 4), (29, 4), (40, 4),
                 (3, 23), (15, 4), (24, 4), (35, 4), (45, 4), (44, 23)):
        if m.inb(x, y) and m.cliff[y, x]:
            m.over.append((2, x, y, P1('cv_walllamp')))
    m.dress(11, seed=1)


# ====================================================================================================== 545
def build_545():
    import numpy as np
    from terrain import vnoise
    m = Cave(40, 30, 'S', seed=545, pool='Salt Lake')
    B = m.box

    # ---- 1. Elevated NW Ladder Terrace (TER, ht=2) descending cleanly via stone stairs into West Pump Bay (FLOOR, ht=1) ----
    # TER ends cleanly on y=8 -> 3-row salt cliff occupies y=8 (lip), y=9 (face), y=10 (base), leaving y=11..12 open!
    m.room(8.0, 5.6, 5.0, 2.8, h=TER, c='.', rough=0.28, seed=11)
    B(4, 4, 12, 8, TER, '.')
    B(5, 3, 10, 4, TER, '.')
    # Ensure y=9..12 below the ladder terrace is FLOOR so stairs(5, 8, w=3, n=3) open straight onto walkable Pump Bay floor!
    B(3, 9, 10, 12, FLOOR, '.')

    # ---- 2. West Pump Bay & SW Lagoon Overlook (FLOOR, ht=1) ----
    m.room(6.2, 16.5, 4.4, 5.0, h=FLOOR, c='.', rough=0.30, seed=17)
    B(3, 11, 10, 21, FLOOR, '.')
    B(4, 21, 10, 24, FLOOR, '.')
    # Sunken glowing turquoise brine drainage channel carved into the far west rock beside the Pump Wheel!
    B(1, 14, 2, 18, FLOOR, 'w')

    # ---- 3. Organic Jagged Subterranean Salt Lagoon (ZERO rectangular swimming pool!) ----
    for y in range(8, 23):
        for x in range(11, 36):
            q = ((x - 22.8) / 12.6) ** 2 + ((y - 15.2) / 6.9) ** 2
            q += 0.22 * (vnoise(x, y, 5459, 3.5) - 0.5)
            if q <= 1.0:
                m.cls[y, x] = 'w'; m.ht[y, x] = FLOOR
    # Guarantee clean water corridor across causeway (x=11..29, y=14..16) & ring around Amber Islet (29..34, 11..18)
    B(11, 14, 29, 16, FLOOR, 'w')
    B(29, 11, 34, 18, FLOOR, 'w')
    # Recessed north waterfall spring pool (TER opened back to y=2 so y=5..6 shows sparkling brine spilling over y=7 waterfall!)
    B(21, 9, 25, 13, FLOOR, 'w')
    B(22, 2, 23, 6, TER, 'w')

    # Carve dramatic asymmetric ROCK-MASS HEADLANDS & STEPPED CRYSTAL REEFS (no blocky piano-key stubs or twin square boxes!)
    # Bold sculpted NW headland (solid mass tapering organically into lagoon)
    m.mass_at([(x, y) for x in range(12, 17) for y in range(7, 10)] + [(13, 10), (14, 10), (15, 10), (14, 11)])
    # Tapered NE stalagmite cape flanking the waterfall grotto
    m.mass_at([(x, y) for x in range(26, 30) for y in range(7, 10)] + [(27, 10), (28, 10)])
    # Asymmetric south-center curved rock buttress (ends at y=20 so cliff base sits on y=22, leaving y=23 walkable!)
    m.mass_at([(x, y) for x in range(20, 23) for y in range(18, 21)])
    # TWO ASYMMETRIC CARVED ROCK-MASS CRYSTAL ISLETS rising organically from the lagoon (different shapes & offsets!):
    m.mass_at([(14, 18), (15, 18), (16, 18), (14, 19), (15, 19), (16, 19)])             # SW stepped crystal reef (base y=21)
    m.mass_at([(25, 17), (26, 17), (25, 18), (26, 18), (27, 18), (26, 19), (27, 19)])   # SE diagonal staggered crystal reef

    # Amber Islet (30..33, 12..17): surrounded by impassable water on W/N/S and rock MASS on E!
    B(30, 12, 33, 17, FLOOR, '.')
    m.mass_at([(34, y) for y in range(9, 21)] + [(35, y) for y in range(8, 16)])

    # ---- 4. Open Waterfront South Minecart Promenade & East Old Workings (FLOOR, ht=1) ----
    # Water laps naturally along y=21..22; south promenade y=23..26 overlooks the glowing lagoon & crystal islets!
    B(11, 21, 33, 22, FLOOR, 'w')
    B(4, 23, 14, 27, FLOOR, '.')
    B(11, 23, 29, 27, FLOOR, '.')
    B(28, 23, 38, 27, FLOOR, '.')
    B(35, 17, 38, 26, FLOOR, '.')
    B(35, 16, 37, 17, FLOOR, '.')
    # Sculpt asymmetric rock alcoves & ceiling-pillar buttresses along the south outer wall (y=27..28)
    m.mass_at([(10, 27), (11, 27), (11, 28)])
    m.mass_at([(19, 27), (20, 27), (21, 27), (20, 28)])
    m.mass_at([(31, 27), (32, 27), (32, 28)])
    # Natural rocky headland separating lagoon SE bay from East Workings (x=34, y=18..22 -> cliff faces east/south cleanly)
    m.mass_at([(34, 18), (34, 19), (34, 20), (34, 21)])
    # Ensure Lamps 3 (17,23) & 4 (24,23) stand right on the walkable waterfront promenade overlooking the lagoon!
    for lx in (17, 24):
        m.cls[23, lx] = '.'; m.ht[23, lx] = FLOOR
        m.cls[24, lx] = '.'; m.ht[24, lx] = FLOOR
    # Ensure Pump Bay shore around (10, 12..22) is clean walkable FLOOR (so Lamp 2 (10,12) & south turn are wide open!)
    for y in range(11, 24):
        for x in (8, 9, 10):
            if m.ht[y, x] == FLOOR:
                m.cls[y, x] = '.'

    m.tidy()
    # Re-assert strict seal around Amber Islet & clean waterfall/causeway/south-promenade geometry after tidy()
    for y in range(11, 21):
        m.cls[y, 34] = 'x'; m.ht[y, 34] = MASS
    for x in range(11, 30):
        m.cls[15, x] = 'w'; m.ht[15, x] = FLOOR
    for x in range(29, 34):
        m.cls[11, x] = 'w'; m.ht[11, x] = FLOOR
        m.cls[18, x] = 'w'; m.ht[18, x] = FLOOR
    for y in range(12, 18):
        m.cls[y, 29] = 'w'; m.ht[y, 29] = FLOOR
    # Keep Lamp 2 (10,12) and its neighbours (9,12), (10,13) clean open FLOOR
    for xx, yy in ((9, 11), (10, 11), (9, 12), (10, 12), (9, 13), (10, 13)):
        m.cls[yy, xx] = '.'; m.ht[yy, xx] = FLOOR
    # Keep South Waterfront Promenade (x=10..33, y=23..26) & East Workings (35..37, 17..26) cleanly walkable FLOOR
    for x in range(11, 34):
        if m.ht[22, x] == FLOOR:
            m.cls[22, x] = 'w'
        for y in (23, 24, 25, 26):
            m.cls[y, x] = '.'; m.ht[y, x] = FLOOR
    for y in range(17, 27):
        for x in (35, 36, 37):
            m.cls[y, x] = '.'; m.ht[y, x] = FLOOR
    # Keep upper waterfall spring pool cleanly open water on (22..23, 2..6) so y=5..6 shines above the cliff!
    for xx in (22, 23):
        for yy in range(2, 7):
            m.cls[yy, xx] = 'w'; m.ht[yy, xx] = TER
    # Keep west brine drainage channel cleanly turquoise brine (1..2, 14..18)
    for xx in (1, 2):
        for yy in range(14, 19):
            m.cls[yy, xx] = 'w'; m.ht[yy, xx] = FLOOR

    # Stone stairway cleanly spanning the 3-row TER->FLOOR cliff (y=8 lip, y=9 face, y=10 base -> opens onto y=11 FLOOR!)
    m.stairs(5, 8, w=3, n=3, c='.')
    m.causeway = [(x, 15) for x in range(11, 30)]
    m.patch_args = (0.56, 4.2)
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
    m.keep_clear |= ({(7, 5), (6, 5), (8, 5), (5, 7), (6, 7), (7, 7), (5, 8), (6, 8), (7, 8),
                      (5, 11), (6, 11), (7, 11), (6, 12), (8, 12), (9, 12), (10, 12), (10, 13),
                      (8, 15), (9, 14), (9, 15), (10, 15), (9, 19), (10, 18), (10, 20),
                      (30, 15), (31, 15), (31, 14), (31, 16), (32, 15),
                      (17, 23), (17, 24), (24, 23), (24, 24), (25, 25), (26, 25),
                      (35, 17), (35, 18), (36, 17), (36, 18), (36, 26), (37, 25), (37, 26)}
                     | {(x, 25) for x in range(8, 37)}
                     | {(x, 24) for x in range(8, 15)}
                     | {(36, y) for y in range(17, 27)}
                     | set(m.causeway))


def dress_545(m):
    p = 'S'
    import rcompose as RC
    ST = __import__('cavekit').STAMPS
    m.put('cv_ladder', 7, 3)
    m.put('cv_pump', 7, 13)

    # ---- 1. Subterranean Brine Waterfall cascading cleanly from TER spring ledge (y=6) down cliff (y=7..9) into lagoon (y=10)! ----
    wf_crest = RC.vauto('rejuvenation', 'Waterfall crest', 0)
    wf_mid = RC.vauto('rejuvenation', 'Waterfall', 0)
    wf_bot = RC.vauto('rejuvenation', 'Waterfall bottom', 0)
    for wx in (22, 23):
        m.over.append((2, wx, 7, wf_crest))
        m.over.append((2, wx, 8, wf_mid))
        m.over.append((2, wx, 9, wf_mid))
        m.over.append((2, wx, 10, wf_bot))

    # ---- 2. Atmospheric Subterranean Light Shafts (cv_shaft, pri=2) & Warm Glow Pools (pf_glow, pri=5) ----
    for sx, sy in ((12, 12), (22, 11), (31, 12), (18, 23)):
        if m.inb(sx + 1, sy + 2):
            m.stamps.append(('cv_shaft', sx, sy))
    m.stamps.append(('pf_glow', 31, 13))        # golden bioluminescent aura illuminating Old Amber on the islet!
    m.stamps.append(('pf_glow', 8, 15))         # warm pool of light beside the brine pump & causeway head

    # ---- 3. Timber Causeway Launch Pier (x=10, y=14..16) & South Minecart Hauling Siding (y=24) ----
    m.over.append((1, 10, 14, P1('cv_raft_t')))
    m.over.append((1, 10, 15, P1('cv_raft_m')))
    m.over.append((1, 10, 16, P1('cv_raft_b')))
    for x in range(16, 24):
        m.tile(P1('cv_rail_h'), x, 24)
    m.tile(P1('cv_rail_end'), 15, 24)
    m.tile(P1('cv_rail_end'), 24, 24)
    m.tile(P1('cv_cart_salt'), 18, 24)
    m.tile(P1('cv_cart'), 21, 24)

    # ---- 4. Lived-In Subterranean Salt-Mine Vignettes (Timber Frames, Barrels, Salt Stacks, Sump Sluice & Posts) ----
    for name, x, y in (
        ('cv_frame', 28, 23), ('cv_frame', 35, 21),
        ('cv_saltblocks', 4, 25), ('cv_saltblocks', 35, 25), ('cv_saltblocks', 4, 6),
        ('cv_tools', 9, 4), ('cv_tools', 4, 15),
        ('wr_sacks', 12, 26), ('wr_sacks', 3, 20), ('wr_sacks', 37, 22),
        ('cv_post', 3, 13), ('cv_post', 3, 17), ('cv_post', 15, 26), ('cv_post', 26, 26), ('cv_post', 35, 23),
        ('hb_barrels', 3, 5), ('hb_barrels', 37, 19), ('hb_boxes', 4, 21),
        ('cv_sluice', 3, 15), ('cv_chain', 6, 13),
    ):
        L = ST[name]['layers']; w, h = len(L[0][0]), len(L[0])
        if m.free(x, y, w, h, on='.') and not any((xx, yy) in m.keep_clear for xx in range(x, x + w) for yy in range(y, y + h)):
            m.put(name, x, y)

    # ---- 5. Warm Miners' Wall Sconces along Cavern Cliff Faces ----
    for x, y in ((4, 2), (10, 2), (8, 9), (14, 10), (27, 9), (36, 15), (34, 19)):
        if m.inb(x, y) and m.cliff[y, x]:
            m.over.append((2, x, y, P1('cv_walllamp')))

    # ---- 6. Clustered Stalagmites & Tall Crystal Spires ANCHORED ON SOLID ROCK (Shorelines, Promontories, Rock Islets!) ----
    def rock_cluster_spire(name, x, y):
        L = ST[name]['layers']; h = len(L[0])
        if all(m.inb(x, y + dy) and (x, y + dy) not in m.causeway for dy in range(h)):
            for dy in range(h):
                for z in (1, 2):
                    if L[z][dy][0]:
                        m.over.append((z, x, y + dy, L[z][dy][0]))
                        if z == 1:
                            m.taken[y + dy, x] = True

    for name, x, y in (
        # NW sculpted rock headland (x=12..16, y=7..11)
        ('cv_xrose2', 13, 8), ('cv_xblue2', 14, 9), ('cv_xsea2', 15, 9), ('S_stal', 12, 8),
        # NE stalagmite cape flanking the waterfall grotto (x=26..29, y=7..10)
        ('cv_xsea2', 27, 8), ('cv_xrose2', 28, 9), ('S_stal', 26, 8),
        # SW stepped crystal reef rock islet (x=14..16, y=18..19)
        ('cv_xrose2', 14, 17), ('cv_xblue2', 15, 18), ('cv_xsea2', 16, 18),
        # SE diagonal staggered crystal reef islet (x=25..27, y=17..19)
        ('cv_xblue2', 25, 16), ('cv_xrose2', 26, 17), ('S_stal', 27, 18),
        # South-center rock buttress (x=20..22, y=18..20)
        ('cv_xsea2', 20, 17), ('cv_xrose2', 21, 18), ('S_stal', 22, 18),
    ):
        rock_cluster_spire(name, x, y)

    # Low crystal skirts & halite cubes hugging ONLY solid rock-islet bases & cliff shores (ZERO mid-water stickers!)
    for x, y, n in (
        (13, 10, 'cv_xsalt'), (15, 10, 'cv_xsea'), (14, 11, 'cv_xblue'),
        (26, 9, 'cv_xsalt'), (29, 9, 'cv_xblue'),
        (14, 19, 'cv_xsalt'), (16, 19, 'cv_xsea'), (25, 18, 'cv_xsalt'), (27, 19, 'cv_xblue'),
        (20, 20, 'cv_xsalt'), (22, 20, 'cv_xblue'), (21, 9, 'cv_xsea'), (24, 9, 'cv_xblue'),
    ):
        if m.inb(x, y) and (x, y) not in m.causeway:
            m.over.append((1, x, y, P1(n)))
            m.taken[y, x] = True

    # Walkable-chamber tall crystal spires & stalagmites framing Ladder Terrace, Pump Bay, Amber Islet, & South/East Workings
    for name, x, y in (
        ('cv_xrose2', 3, 5), ('cv_xblue2', 12, 4), ('S_stal', 3, 11),
        ('cv_xrose2', 3, 18), ('cv_xsea2', 9, 20),
        ('cv_xrose2', 30, 12), ('cv_xsea2', 33, 12), ('cv_xblue2', 33, 16), ('cv_xrose2', 30, 16),
        ('cv_xblue2', 38, 17), ('cv_xsea2', 38, 23), ('S_stal', 35, 26),
        ('cv_xrose2', 5, 26), ('cv_xblue2', 13, 26), ('S_stal', 29, 26),
    ):
        if m.free(x, y, 1, 2, on='.') and (x, y) not in m.keep_clear and (x, y + 1) not in m.keep_clear:
            m.put(name, x, y)

    # Clustered wall-foot salt crystals & rocks
    m.solid_props(['cv_xsalt', 'cv_xblue', 'cv_xsea', p + '_rock0'], 14, seed=4)

    # Bioluminescent cold-glow fungus hugging wet lagoon shores, sump rim, & Amber Islet
    for x, y in ((3, 15), (4, 18), (7, 20), (9, 21), (32, 13), (31, 16), (33, 15), (16, 26), (25, 26), (37, 24), (9, 7), (4, 7)):
        if m.free(x, y, 1, 1, on='.') and (x, y) not in m.keep_clear:
            m.over.append((2, x, y, P1('cv_fung0' if (x + y) % 2 == 0 else 'cv_fung1')))
            m.taken[y, x] = True

    m.dress(14, seed=2)


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
    ST = __import__('cavekit').STAMPS
    m.tile(P1('cv_hole'), 29, 5)
    m.over.append((2, 40, 18, P1('cv_kelp1')))
    # Dramatic coastal sea-cave sunbeam shafts across the tide basin
    for x, y in ((14, 15), (27, 20), (21, 27)):
        if m.inb(x + 1, y + 2): m.stamps.append(('cv_shaft', x, y))
    # Coastal wreckage, driftwood, whalebones, mine-mouth timber, barrels & lanterns
    for name, x, y in (
        ('cv_drift', 4, 35), ('cv_drift', 33, 30), ('cv_drift', 22, 6), ('cv_drift', 6, 11),
        ('pf_whalebone', 2, 32), ('pf_whalebone', 36, 22), ('pf_whalebone', 25, 3),
        ('cv_frame', 31, 0), ('cv_post', 4, 21), ('cv_post', 9, 32), ('cv_post', 35, 12),
        ('hb_barrels', 4, 31), ('hb_barrels', 37, 27), ('wr_sacks', 12, 34), ('wr_sacks', 34, 25),
        ('cv_lamp_on', 10, 31), ('cv_lamp_on', 8, 15), ('cv_lamp_on', 22, 11), ('cv_lamp_on', 35, 19),
    ):
        L = ST[name]['layers']; w, h = len(L[0][0]), len(L[0])
        if m.free(x, y, w, h, on='.:') and not any((xx, yy) in m.keep_clear for xx in range(x, x + w) for yy in range(y, y + h)):
            m.put(name, x, y)
    # Barnacles, tide-cave rocks, gull nests, & sea crystals along cavern walls
    m.solid_props(['cv_barn', 'cv_barn', p + '_rock0', 'cv_nest', 'cv_xsea', 'cv_xblue'], 22, seed=5)
    m.solid_props(['cv_nest', 'cv_nest', 'cv_barn', 'cv_xsea'], 9, seed=6, box=(20, 1, 38, 10))
    # Tall emerald-sea & sapphire-blue crystal spires across the chambers & hidden grotto
    for name, x, y in (
        ('cv_xsea2', 12, 13), ('cv_xsea2', 31, 13), ('cv_xblue2', 10, 20),
        ('cv_xsea2', 3, 29), ('cv_xblue2', 14, 34), ('cv_xsea2', 3, 14),
        ('cv_xblue2', 11, 5), ('cv_xsea2', 21, 3), ('cv_xblue2', 36, 4),
        ('cv_xsea2', 38, 12), ('cv_xblue2', 37, 33), ('cv_xsea2', 43, 15), ('cv_xblue2', 45, 19),
    ):
        if m.free(x, y, 1, 2, on='.:') and (x, y) not in m.keep_clear and (x, y + 1) not in m.keep_clear:
            m.put(name, x, y)
    # Bioluminescent sea-cave fungi hugging the wet tide-pool rims & grotto walls
    for x, y in ((5, 36), (13, 35), (16, 29), (24, 34), (22, 14), (29, 13), (35, 24), (32, 32), (43, 20), (8, 7)):
        if m.free(x, y, 1, 1, on='.') and (x, y) not in m.keep_clear:
            m.over.append((2, x, y, P1('cv_fung0'))); m.taken[y, x] = True
    # Sea-crystal & barnacle reefs rising from the open tide basin (strictly NEVER touching m.bars or adjacent crossings!)
    bar_excl = {(bx + dx, by + dy) for bx, by in m.bars for dx in (-1, 0, 1) for dy in (-1, 0, 1)}
    def basin_spire(name, x, y):
        L = ST[name]['layers']; h = len(L[0])
        if all(m.inb(x, y + dy) and m.cls[y + dy, x] == 'w' and (x, y + dy) not in bar_excl for dy in range(h)):
            for dy in range(h):
                for z in (1, 2):
                    if L[z][dy][0]:
                        m.over.append((z, x, y + dy, L[z][dy][0]))
    for name, x, y in (
        # West sea basin reefs (x=11..15, y=15..25)
        ('cv_xsea2', 11, 16), ('cv_xblue2', 14, 19), ('cv_xsea2', 12, 23), ('cv_xblue2', 18, 16),
        # East sea basin reefs (x=27..32, y=14..26)
        ('cv_xblue2', 31, 15), ('cv_xsea2', 29, 21), ('cv_xblue2', 32, 24), ('cv_xsea2', 26, 24),
    ):
        basin_spire(name, x, y)
    for x, y, n in (
        (12, 17, 'cv_xblue'), (15, 20, 'cv_xsea'), (11, 24, 'cv_xsalt'), (13, 24, 'cv_barn'),
        (17, 17, 'cv_xsea'), (19, 17, 'cv_barn'), (12, 15, 'cv_barn'), (15, 25, 'cv_xblue'),
        (30, 16, 'cv_xsea'), (32, 17, 'cv_barn'), (28, 22, 'cv_xblue'), (30, 22, 'cv_xsalt'),
        (31, 25, 'cv_xsea'), (27, 25, 'cv_barn'), (29, 26, 'cv_xblue'), (32, 20, 'cv_xsea'),
    ):
        if m.inb(x, y) and m.cls[y, x] == 'w' and (x, y) not in bar_excl:
            m.over.append((1, x, y, P1(n)))
    # Gull guano streaks & warm cliff sconces along cavern rock overhangs
    for x, y in ((24, 3), (35, 6), (8, 12), (5, 21), (36, 14), (27, 2), (14, 5)):
        if m.inb(x, y) and m.cliff[y, x]: m.over.append((2, x, y, P1('cv_guano')))
    for x, y in ((6, 28), (12, 28), (6, 17), (14, 4), (23, 2), (33, 2), (36, 10)):
        if m.inb(x, y) and m.cliff[y, x]: m.over.append((2, x, y, P1('cv_walllamp')))
    m.dress(12, groups=[(['L_fd0', 'L_fd1', 'L_fd2', 'cv_kelp0', 'cv_kelp1', 'cv_wrack'], 6), (['L_rubble0', 'L_rubble1'], 2)], seed=3)


def main(which):
    import yaml
    if '544' in which:
        m, paths, off = build_544()
        events_544(m, paths, off)
        dress_544(m)
        m.paint()
        m.preview('/tmp/mb13/p544.png', scale=0.5)
        head = {'id': 544, 'name': 'Brinecut Mine 1F', 'parent': 540, 'bgm': 'Cave', 'field': 'CAVE',
                'metadata': {'Name': 'Brinecut Mine', 'MapPosition': [0, 11, 23], 'BattleBack': 'cave1', 'SnapEdges': True},
                'tone': [-6, -8, 2, 10], 'fog': {'name': 'prismfall_cave', 'opacity': 36, 'blend': 1, 'zoom': 100, 'sx': 1, 'sy': 0},
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
                'metadata': {'Name': 'Gullcry Caves', 'MapPosition': [0, 8, 21], 'BattleBack': 'cave1', 'SnapEdges': True},
                'tone': [-10, -4, 8, 14], 'fog': {'name': 'prismfall_seamist', 'opacity': 34, 'blend': 1, 'zoom': 100, 'sx': 1, 'sy': 0},
                '_file': '564_gullcry_caves.yaml'}
        m.write(564, head, comment='# GENERATED by mapgen/layouts/caves.py (map builder 13): Gullcry Caves, DUNGEON_PUZZLES D6 (the tide).\n'
                                  '# Tide clock: V526 steps since the turn, S526 high tide (pfm_tide_tick).  Edit the layout script.\n')
    if '545' in which:
        m = build_545(); events_545(m); dress_545(m); m.paint()
        m.preview('/tmp/mb13/p545.png', scale=0.5)
        head = {'id': 545, 'name': 'Brinecut Mine B1F', 'parent': 544, 'bgm': 'Cave', 'field': 'CAVE',
                'metadata': {'Name': 'Brinecut Mine', 'MapPosition': [0, 11, 23], 'BattleBack': 'cave1', 'DarkMap': True, 'SnapEdges': True},
                'tone': [-10, -8, 4, 16], 'fog': {'name': 'prismfall_cave', 'opacity': 40, 'blend': 1, 'zoom': 100, 'sx': 1, 'sy': 0},
                'gates': [{'name': 'the amber islet only over the drained lake', 'from': [[7, 5]], 'sealed': [[32, 15], [31, 13]]}],
                '_file': '545_brinecut_mine_b1f.yaml'}
        m.write(545, head, comment='# GENERATED by mapgen/layouts/caves.py (map builder 13): Brinecut Mine B1F, the salt lake (D4 combine).\n'
                                  '# Dark map: the miners\' lamps widen the light (pfm_light_lamp).  Edit the layout script, not this file.\n')


if __name__ == '__main__':
    main(sys.argv[1:] or ['544', '545', '564'])
