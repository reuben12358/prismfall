#!/usr/bin/env python3
"""Gossamer Deepwood (525, :SILKWOOD) and Cocoonfall Hollow (548, :BLEED).
525 (44 x 40): past the Cut tree.  Older, darker wood; the glass seeps in from the east.  Shelly's dew-pond clearing in the
south (small Veil, glassed Masquerain).  East: the crystal-silk mouth to the Hollow (opens once :ch2_tamsin is chosen).
548 (38 x 34): a crater of crystal trees strung with glass thread like a harp; the Glass Matriarch on her nest at the centre.
Entries: west from the Deepwood (DEEP_COCOON, through the Veil where Juno and Tamsin wait) and south from Thistledown Lea (R3_COCOON).
Run:  python3 -I layouts/deepwood.py && python3 -I build.py 525 548"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wildkit import Wild, save, say, trainer, once, vnoise, MUSH, CU, B


def key(m, k): return "$game_self_switches[[%d, 0, '%s']]" % (m, k)
def setk(m, k): return {'script': key(m, k) + ' = true'}
def reveal(*names):
    return {'script': "%%w[%s].each do |n|\n  ev = $game_map.events.values.find { |e| e.name == n.tr('_', ' ') }\n"
                      "  $game_self_switches[[$game_map.map_id, ev.id, 'A']] = true if ev\nend\n$game_map.need_refresh = true" % ' '.join(n.replace(' ', '_') for n in names)}


def deepwood():
    W, H = 44, 40
    c = Wild(W, H, 525)
    def hf(x, y):
        if ((x - 30) / 12.0) ** 2 + ((y - 8) / 7.0) ** 2 < 1 + 0.4 * (vnoise(x, y, 3, 4.0) - 0.5): return 1
        return 0
    c.set_heights(hf)
    c.notch(22, 24, 13, 1, depth=5)
    c.pond(14, 31, 4.5, 3.0, 6)                                   # Shelly's dew pond
    c.stream([(10, 0), (12, 8), (8, 16), (6, 24), (10, 29)], 2, 4)
    c.path([(0, 18), (8, 19), (16, 18), (23, 19), (31, 21), (38, 20), (43, 20)], 2, 'd', 1, only='.~')
    c.path([(16, 18), (18, 25), (19, 27)], 2, 'd', 2, only='.')          # down to the dew pond
    c.path([(23, 19), (23, 18)], 2, 'd', 3, only='.'); c.path([(23, 12), (27, 8), (34, 6)], 2, 'd', 4, only='.')
    c.path([(31, 21), (30, 30), (36, 34)], 2, 'd', 5, only='.')
    for y in range(H):
        for x in range(W):
            if c.g[y][x] == 'd' and False: pass
    c.stairs(22, 13)
    c.cliffs(face=2, keep='~=')
    for y in range(H):
        for x in range(W):
            if c.g[y][x] == '.': c.g[y][x] = 'T'
    for i, (cx, cy, rx, ry) in enumerate(((16, 30, 7, 5), (9, 18, 4, 3), (24, 20, 5, 3.5), (30, 7, 6, 3.5), (35, 31, 5, 4.5), (38, 20, 5, 4.5), (17, 23, 3, 2.5))):
        c.blob(cx, cy, rx, ry, '.', 60 + i, only='T', rough=0.7)
    # the glass seeps in from the east: ash ground and glassed wood beyond x ~ 34
    for y in range(H):
        for x in range(W):
            edge = 34 + 3 * math.sin(y / 4.0) + 3 * (vnoise(x, y, 9, 4.0) - 0.5)
            if x > edge:
                c.g[y][x] = {'.': 'a', 'T': 'U', 'd': 'D'}.get(c.g[y][x], c.g[y][x])
    for y in range(18, 23):                                   # the Hollow's mouth: one tile wide at the crystal silk
        if c.g[y][41] in 'aD' and y != 20: c.g[y][41] = 'U'
    west, east = (0, 18), (43, 20)
    c.need(west, east, (18, 25))
    c.keep_clear([(0, 18), (1, 18), (43, 20), (42, 20)], 2)
    # Shelly's Veil: a small glassed pocket on the far side of the dew pond
    c.blob(22, 34, 3.6, 2.8, 'a', 91, only='.T', rough=0.9)
    P = {'shelly': c.spot(15, 26, '.'), 'masq': c.spot(22, 34, 'a'), 'ferris': c.spot(26, 20, 'd.'), 'linden': c.spot(31, 7, 'd.'),
         'sorrel': c.spot(34, 30, 'd.'), 'silver': c.spot(37, 4, '.', r=5), 'great': c.spot(9, 16, '.'), 'stump': c.spot(39, 32, '.a', r=5)}
    P['caterpie'] = c.spot(P['shelly'][0] + 1, P['shelly'][1] - 1, '.', r=2)
    c.need(P['masq'])
    c.seal()
    c.land('gstump_dark', 6, 21); c.land('gstump', 26, 2); c.land('log_big', 20, 17); c.land('roots', 12, 22); c.land('crag', 30, 4)
    c.land('stump_tall', P['stump'][0] + 1, P['stump'][1] - 1, on='.a')
    c.trees(['crystal_tree', 'crystal_tree', 'cry_violet', 'r_cry_spray', 'cry_teal_m', 'r_cry_big'], 9, on='a', seed=9)
    c.trees(['cocoon', 'cocoon', 'cocoon_big', 'silk_tree', 'cocoon_low'], 16, seed=1)
    c.trees(['fern_big', 'log', 'log_moss', 'stump_moss', 'rafflesia', 'creep1', 'dead1', 'corpse'], 18, seed=2)
    c.trees(['t_dark', 't_leafy', 'r_tree_d', 'r_tree_d2', 'smalltree', 'pine_s2'], 18, seed=3)
    c.trees(['cry_violet_s', 'cry_blue_s', 'dead3', 'stump_grey', 'log_grey'], 10, on='a', seed=4, bleed=True)
    c.overhang(0.3, seed=2)
    for x, y in ((12, 15), (27, 16), (4, 30), (33, 12), (29, 26)):
        c.overlay('web_big', x, y)
    for x, y in ((14, 27), (27, 5), (36, 28)):
        c.overlay('shaft', x, y)
    for y in range(31, 38):
        for x in range(18, 21):
            if c.inb(x, y) and c.g[y][x] == 'a' and (x == 19 or (x + y) % 3 == 0): c.o[2][y][x] = c.o[2][y][x] or CU['veil']
    c.scatter([([1172, 1164, 1180, 1189], 0.55, 3.0, 0.8), (MUSH[4:], 0.70, 2.4, 0.75), ([1048, 1057, 1056], 0.74, 2.6, 0.75)],
              [(1164, 10), (1172, 6), (1180, 3), (1189, 3), (1263, 2), (1148, 2)], density=0.38, seed=6)
    c.scatter([([8136, 8144, 8152], 0.60, 2.6, 0.7)], [(1164, 4), (1172, 3)], density=0.25, on='a', bleed=True, seed=7)
    c.edge_decor([1263, 1148, 1158, 1150], 0.25, by='T', seed=1)
    c.water_decor(0.2)
    E = []
    E.append({'type': 'warp', 'name': 'To Gossamer Wood', 'at': [0, 18], 'link': 'WOOD_DEEP', 'arrive': [1, 18, 'right']})
    E.append({'type': 'warp', 'name': 'To Cocoonfall Hollow', 'at': [43, 20], 'link': 'DEEP_COCOON', 'arrive': [42, 20, 'left']})
    E.append(c.fog_event('prismfall_spores', 70, 0, 200, 1, 0))
    E.append({'type': 'event', 'name': 'Crystal silk', 'at': [41, 20], 'pages': [       # map builder 10 (REQUESTS 17): a charset, so it blocks
        {'graphic': {'sprite': 'pf_silk_curtain', 'dir': 'left'}, 'dir_fix': True, 'commands': [
            {'if': 'pf_choice(:ch2_tamsin)', 'then': [
                "You hold up Mother Loom's shuttle. The crystal silk unpicks itself, thread by thread, and lets you through.",
                setk(548, 'ESCORT'), {'selfswitch': ['A', True]}],
             'else': ["Silk turned to glass, hard as a pane. Something beyond it is ringing. Tamsin might know how to open it."]}]},
        {'cond': {'self': 'A'}, 'through': True}]})
    E.append(trainer(P['ferris'], 'POKEMANIAC', 'Ferris', 'trainer_POKEMANIAC', 'left', 4,
                     "The bugs in here have gone STRANGE and I love them!", "That one hummed. Did you hear it hum?"))
    E.append(trainer(P['linden'], 'BUGCATCHER', 'Linden', 'trainer_BUGCATCHER', 'left', 4,
                     "Deepwood's my secret spot! How'd you get past the big tree?", "The pond glows at night. Don't tell anyone."))
    E.append(trainer(P['sorrel'], 'POKEMONRANGER_F', 'Sorrel', 'trainer_POKEMONRANGER_F', 'up', 4,
                     "Rangers patrol here since the silk went strange. Let's see your team.", "Leave the webs as you found them, please."))
    E.append({'type': 'item', 'at': P['silver'], 'item': 'SILVERPOWDER'})
    E.append({'type': 'item', 'at': P['great'], 'item': 'GREATBALL'})
    E.append({'type': 'event', 'name': 'HiddenItem', 'at': P['stump'], 'pages': [
        {'commands': [{'if': 'pbItemBall(:SUPERPOTION)', 'then': ["The stump kept it dry.", {'selfswitch': ['A', True]}], 'else': []}]},
        {'cond': {'self': 'A'}}]})
    # Shelly's cameo sidequest "Lost in the Gossamer" (CAMEOS.md 1): S181 CAMEO_SHELLY_DONE, V123 CAMEO_QUESTS_DONE
    struggle = "pbReceiveItem(:BRIGHTPOWDER)"   # was TM Struggle Bug, which the base project has no TM for (Gemini review)
    shelly_end = [say('SHELLY', 'neutral', "You just... walked in. Where I'm from, nobody walks into the sick places and comes out the same."),
                  say('SHELLY', 'happy', "Before I go, could we have one practice battle? Doubles? I'm supposed to be good at this and I don't want to be rusty when I get home."),
                  {'script': 'Prismfall.cameo_battle(:FESTIVAL_SHELLY, "Shelly", 1, double: true, field: :SILKWOOD)'},
                  say('SHELLY', 'happy', "Your forest sounds like home used to, before the city got sick. Look after it?"),
                  {'script': 'pbReceiveItem(:SILVERPOWDER)'}, {'script': struggle},
                  {'switch': ['CAMEO_SHELLY_DONE', True]}, {'script': '$game_variables[123] += 1'},
                  "(She steps into the pond's reflection and is gone. One pink ribbon floats on the water.)", {'selfswitch': ['A', True]}]
    E.append({'type': 'event', 'name': 'Shelly', 'at': P['shelly'], 'pages': [
        {'graphic': {'sprite': 'NPC 11', 'dir': 'left'}, 'commands': [
            {'if': key(525, 'MASQ'), 'then': shelly_end, 'else': [
                {'if': key(525, 'SHELLY'), 'then': [say('SHELLY', 'sad', "The pond's behind that shimmer. I can't go near it. You can, can't you?")], 'else': [
                    "(A pink-haired girl is crouched in front of a Caterpie, bowing to it.)",
                    say('SHELLY', 'panic', "I'm so sorry, was this your leaf? I didn't know it was your leaf."),
                    "\\pf[SHELLY,shocked,sweat]Shelly: Oh! A person! Um. Hello. Is this— this isn't the Rhodochrine Jungle, is it.",
                    say('SHELLY', 'sad', "I looked into a pond at home and then I was looking OUT of this one. That was three days ago. The paths keep re-weaving."),
                    {'choices': ["I'll help you get back."], 'cancel': 1, 'branches': [[
                        say('SHELLY', 'happy', "Really? You don't have to. I mean please do. I mean thank you."), setk(525, 'SHELLY')]]}]}]}]},
        {'cond': {'self': 'A'}}]})
    E.append({'type': 'npc', 'name': 'Caterpie', 'at': P['caterpie'], 'sprite': 'Followers/CATERPIE', 'dir': 'right',
              'text': "The Caterpie is very solemnly eating its leaf. It has accepted the apology."})
    E.append({'type': 'event', 'name': 'Glassed Masquerain', 'at': P['masq'], 'pages': [
        {'graphic': {'sprite': 'Followers/MASQUERAIN', 'dir': 'left'}, 'commands': [
            {'if': key(525, 'SHELLY'), 'then': [
                "Its wings are panes of glass. The eye-spots are the only things on it still moving.",
                {'script': 'setBattleRule("field", :BLEED)\nsetBattleRule("canLose")\nWildBattle.start(:MASQUERAIN, 19)'},
                "The Masquerain folds its glass wings and settles on the water. The ringing stops.", setk(525, 'MASQ'), {'selfswitch': ['A', True]}],
             'else': ["A glassed Masquerain hovers over the dew pond. It hasn't noticed you."]}]},
        {'cond': {'self': 'A'}, 'graphic': {'sprite': 'Followers/MASQUERAIN', 'dir': 'left'}, 'through': True,
         'commands': ["It rests on the water, calm."]}]})
    c.events = E
    head = {'id': 525, 'biome': 'forest', 'name': 'Gossamer Deepwood', 'bgm': 'Route 3', 'parent': 524, 'field': 'SILKWOOD', 'tone': [-40, -24, -30, 40],
            'metadata': {'ShowArea': True, 'MapPosition': [0, 13, 23], 'BattleBack': 'forest'}}
    return c.write('', head, "# Gossamer Deepwood (525) and Cocoonfall Hollow (548). WRITTEN BY layouts/deepwood.py - edit that, not this file.\n")


RAVINE = (9, 10)                                               # 548's glass ravine rows (map builder 10)
XING = {'a': 28, 'b': 10, 'c': 19}                              # D3 bridges: a NE cocoon-house, b NW Shard house, c the nest
ANCHORS = ((8, 22), (16, 22), (24, 22))                         # D3 anchors 1-3 at the hamlet's south edge
BRIDGE_TILE = 23057                                             # tileset 52: gd_ford_v (vertical crystal-silk bridge, pas=0, pri=0)


def _fog_event_548(name, opacity=74, blend=1, zoom=200, sx=1, sy=1, hue=0):
    return {'type': 'event', 'name': 'Atmosphere', 'at': [0, 0],
            'pages': [{'trigger': 'parallel', 'commands': [
                {'comment': 'fog: %s (see REQUESTS.md item 3)' % name},
                {'raw': [204, [1, name, hue, opacity, blend, zoom, sx, sy]]},
                {'selfswitch': ['A', True]}]},
                {'cond': {'self': 'A'}}]}


def hollow():
    import random
    import numpy as np
    import rkit as K
    from rkit import STAMPS, P1
    from routekit import Route

    W, H = 38, 34
    VX = 4
    cx, cy = 19, 16
    NX, NY = 19, 5

    # Crisp 3-row frosted Sheridan crater rim cliff (matching 522 Glassed Orchard)
    if 'shs3' not in K.KITS:
        K.KITS['shs3'] = dict(K.KITS['shs'], rows=[K.KITS['shs']['rows'][0],
                                                   K.KITS['shs']['rows'][1],
                                                   K.KITS['shs']['rows'][3]])

    r = Route(548, W, H, theme='snow', kit='shs3', base='.')
    m = r.m
    m.grass = [[18442, 18443], [18444, 18445]]
    m.tall = 18446
    m.STAIRS = K.STAIRS_STONE
    m.grass2 = None
    m.auto['e'] = ('KristilineDirt', 'rejuvenation')
    m.keep_under = 'de'
    rng = random.Random(5482)

    def in_living(x, y):
        return (x <= 3 and 13 <= y <= 19) or (x == 4 and 14 <= y <= 18)

    # ---- 1. Heightmap: dramatic frosted crater rim (ht=1) ringing the depressed hollow (ht=0) ----
    for y in range(H):
        for x in range(W):
            rad = math.hypot((x - cx) / 15.2, (y - cy) / 13.0) + 0.08 * (vnoise(x, y, 5481, 3.2) - 0.5)
            m.ht[y, x] = 0 if rad < 1.0 else 1

    # Carve clean openings & flats:
    # West living entry through the Bleed Veil (x <= 6, y in 13..19)
    m.ht[13:20, 0:7] = 0
    # South glass-choked road pocket (x in 16..20, y >= 27)
    m.ht[26:34, 16:21] = 0
    # North crater amphitheater shelves behind the ravine (rows 1..8, x 8..30):
    # row 0 stays ht=1 so the 3-row frosted cliff face hangs cleanly on rows 1..3, leaving rows 4..8 flat & open
    m.ht[0, :] = 1
    m.ht[1:9, 8:31] = 0
    # Guarantee full crater bowl across the ravine & anchor terrace
    m.ht[9:13, 6:33] = 0
    m.ht[13:25, 5:33] = 0
    # Majority-clean single-cell height spurs so shs3 cliff walls stay crisp and unbroken
    for _ in range(2):
        hi = (m.ht == 1)
        pad = np.pad(hi, 1, constant_values=True)
        n4 = pad[:-2, 1:-1].astype(int) + pad[2:, 1:-1] + pad[1:-1, :-2] + pad[1:-1, 2:]
        m.ht[hi & (n4 <= 1)] = 0
        m.ht[~hi & (n4 >= 3)] = 1
    # Re-assert sacred flat zones after smoothing
    m.ht[0, :] = 1
    m.ht[1:9, 8:31] = 0
    m.ht[9:13, 6:33] = 0
    m.ht[13:20, 0:7] = 0
    m.ht[26:34, 16:21] = 0

    # ---- 2. The Glass Ravine (rows 9..10 across the entire walkable crater width) ----
    # Seals the north sanctum shelves from the south crater floor except across D3 bridges a (28), b (10), c (19).
    for y in RAVINE:
        for x in range(W):
            if m.ht[y, x] == 0:
                m.cls[y, x] = 'w'
    # Gentle organic ravine widening away from the 3 bridgeheads (never touching x in {9..11, 18..20, 27..29})
    for x in range(6, 33):
        if any(abs(x - bx) <= 1 for bx in XING.values()):
            continue
        if m.ht[11, x] == 0 and (x in (13, 14, 15, 23, 24, 25)):
            m.cls[11, x] = 'w'
        if m.ht[8, x] == 0 and (x in (15, 16, 22, 23)):
            m.cls[8, x] = 'w'

    # ---- 3. Paths & clearings ----
    def lane(pts, width=1.9, cls='d'):
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            steps = max(abs(x1 - x0), abs(y1 - y0), 1) * 3
            for i in range(steps + 1):
                t = i / float(steps)
                px = x0 + (x1 - x0) * t
                py = y0 + (y1 - y0) * t
                for yy in range(int(py) - 2, int(py) + 3):
                    for xx in range(int(px) - 2, int(px) + 3):
                        if not m.inb(xx, yy) or m.cls[yy, xx] == 'w' or m.ht[yy, xx] != 0:
                            continue
                        if (xx - px) ** 2 + (yy - py) ** 2 <= (width * 0.58) ** 2:
                            m.cls[yy, xx] = cls
                            r.road_mask[yy, xx] = True

    # Living dirt path through the west gate right up to the Veil
    for x in range(0, 5):
        for y in (15, 16, 17):
            m.cls[y, x] = 'e'
            r.road_mask[y, x] = True
    # Frosted crystal paths inside the hollow: Veil -> central clearing -> all 3 bridges, 3 anchors, cocoons, south way
    lane([(5, 16), (11, 16), (19, 16)], width=2.2)
    lane([(19, 16), (19, 11)], width=1.8)                       # to Bridge c
    lane([(13, 16), (10, 14), (10, 11)], width=1.8)             # to Bridge b
    lane([(19, 16), (25, 14), (28, 12), (28, 11)], width=1.8)   # to Bridge a
    lane([(11, 16), (8, 20), (8, 22), (16, 22), (24, 22), (27, 22)], width=2.0)   # anchor terrace & cocoons
    lane([(19, 16), (18, 22), (18, 28), (18, 32)], width=2.0)   # south glass-choked way
    # North sanctum paths behind each bridge
    lane([(10, 8), (10, 6), (13, 6)], width=1.7)                # NW cocooned cottage
    lane([(19, 8), (19, 6)], width=1.9)                         # Center Matriarch nest
    lane([(28, 8), (27, 6), (25, 6)], width=1.7)                # NE cocoon-house & TM81

    # Keep living west entry cleanly on 'e'
    for x in range(0, 5):
        for y in (15, 16, 17):
            m.cls[y, x] = 'e'

    # ---- 4. Reserve ALL sacred event / puzzle / trial / bridge coordinates ----
    P = {
        'matriarch': [NX, NY],
        'house': [13, 6],
        'tm': [25, 6],
        'cocoons': [27, 22],
        'juno': [3, 15],
        'tamsin': [3, 18],
    }
    must_keep = [
        (0, 16), (1, 16), (2, 16), (3, 16), (4, 15), (4, 16), (4, 17), (4, 18), (5, 16),
        (3, 15), (3, 18), (2, 15), (2, 18),
        (18, 33), (18, 32), (18, 31),
        (NX, NY), (NX, NY + 1), (NX, NY + 2), (NX - 1, NY + 2), (NX + 1, NY + 2), (NX, 8),
        (13, 6), (12, 6), (11, 6), (10, 6), (10, 7), (10, 8),
        (25, 6), (26, 6), (27, 6), (28, 6), (28, 7), (28, 8),
        (27, 22), (26, 22), (26, 21), (25, 21), (25, 22),       # Glass cocoons + trial_overlay Humming cocoon (26,21)
    ] + list(ANCHORS) + [(bx, y) for bx in XING.values() for y in (8, 11, 12)]
    for x, y in must_keep:
        r.road_mask[y, x] = True
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                xx, yy = x + dx, y + dy
                if m.inb(xx, yy) and m.cls[yy, xx] != 'w':
                    if (xx, yy) not in ((15, 6), (16, 6), (22, 6), (23, 6)):
                        r.road_mask[yy, xx] = True

    # ---- 5. Subtle frosted tall grass pockets on crater floor (for authentic Bleed encounters) ----
    for cx_g, cy_g, rx, ry in ((11, 26, 3.0, 2.0), (26, 26, 3.0, 2.0), (13, 19, 2.6, 1.8), (25, 17, 2.8, 1.8)):
        for y in range(max(12, int(cy_g - ry - 1)), min(H - 3, int(cy_g + ry + 2))):
            for x in range(max(6, int(cx_g - rx - 1)), min(W - 4, int(cx_g + rx + 2))):
                if m.cls[y, x] == '.' and m.ht[y, x] == 0 and not r.road_mask[y, x]:
                    if ((x - cx_g) / rx) ** 2 + ((y - cy_g) / ry) ** 2 + 0.22 * (vnoise(x, y, 5489, 2.8) - 0.5) <= 1.0:
                        m.cls[y, x] = 't'

    # ---- 6. Paint base terrain (ground, water autotiles, frosted shs3 crater cliffs) ----
    m.paint_ground()
    m.autotiles()
    m.cliffs()

    # Subtle crystalline snow-drift variation across frosted crater floor & rim
    for y in range(H):
        for x in range(W):
            if m.cls[y, x] == '.' and not in_living(x, y) and not m.cliff[y, x]:
                if vnoise(x, y, 5485, 3.2) > 0.60:
                    m.L[0, y, x] = 10395

    # Living Sheridan green pocket west of the Bleed Veil (x <= 3, y in 13..19)
    for y in range(12, 21):
        for x in range(0, 5):
            if in_living(x, y) or (x <= 3 and 12 <= y <= 20 and m.ht[y, x] == 0):
                if m.cls[y, x] in '.t':
                    m.L[0, y, x] = K.SH_GRASS[y & 1][x & 1]
                    if not r.road_mask[y, x] and (x * 7 + y * 11) % 4 == 0:
                        m.L[1, y, x] = K.DECOR_SH['flowers'][(x + y) % 4]
                    elif not r.road_mask[y, x] and (x * 5 + y * 3) % 3 == 0:
                        m.L[1, y, x] = K.DECOR_SH['green'][(x + y) % len(K.DECOR_SH['green'])]

    # Glass-sheen sparkles & frozen shards gleaming on the Glass Ravine surface
    for y in range(H):
        for x in range(W):
            if m.cls[y, x] == 'w' and (x * 7 + y * 13) % 7 == 0 and x not in XING.values():
                m.L[2, y, x] = 25824 + ((x + y) % 3)

    # ---- 7. North Sanctum Architecture: Cocooned Cottages, Matriarch's Nest, and D3 Shelf Dividers ----
    # NW Cocooned Cottage (kf_flat 5x4 at (10, 2) -> front wall at y=5, door at (12,5), Cocooned house event at (13,6))
    m.stamp('kf_flat', 10, 2)
    # NE Cocoon-House (kf_flat 5x4 at (25, 2) -> aligned cleanly on the NE shelf, TM81 at (25,6) right in its yard!)
    m.stamp('kf_flat', 25, 2)
    # Drape silk webs & hanging cocoons over both cocooned cottages (Layer 2 overhead, pri=2)
    m.over.append((2, 11, 4, 22751))
    m.over.append((2, 28, 4, 22751))
    for wx, wy in ((11, 2), (26, 2)):
        st = STAMPS['pf_p_web']
        for dy in range(st['h']):
            for dx in range(st['w']):
                t = st['layers'][2][dy][dx]
                if t:
                    m.over.append((2, wx + dx, wy + dy, t))

    # Matriarch's Glass-Silk Nest at (19, 5): crystalline floor dais, green root-glow, flanking crystal obelisks & web canopy
    for dy in range(-1, 3):
        for dx in range(-2, 3):
            xx, yy = NX + dx, NY + dy
            if m.inb(xx, yy) and not m.cliff[yy, xx]:
                m.L[0, yy, xx] = 10395
    m.stamp('cr_purple_t', 17, 4)
    m.stamp('cr_teal_t', 21, 4)
    m.stamp('cr_blue_c', 17, 6)
    m.stamp('cr_pink_c', 21, 6)
    m.stamp('pf_glow', NX - 1, NY)       # faint eerie glow under the roots beneath the Matriarch!
    # Overhanging silk web arch framing the nest above the Matriarch (leaving (19, 5) crisp and readable)
    st = STAMPS['pf_p_web']
    for dy in range(st['h']):
        for dx in range(st['w']):
            t = st['layers'][2][dy][dx]
            if t:
                m.over.append((2, NX - 1 + dx, NY - 2 + dy, t))

    # Solid crystal-spine dividers separating the 3 north shelves (enforces D3 anchor puzzle — zero row-4/6/8 bypass!)
    # Every cell in x in (15,16,22,23), y in 3..8 gets a solid pas=15 base on Layer 1 so players can NEVER slip behind tall crystal tips or along cliff-foot row 3!
    for sx, c_tid in ((15, P1('cr_purple_c')), (16, P1('cr_teal_c')), (22, P1('cr_teal_c')), (23, P1('cr_purple_c'))):
        for sy in (3, 4, 6):
            m.L[1, sy, sx] = c_tid
            m.taken[sy, sx] = True
    # Divider 1 (between NW Cocooned Cottage and Center Matriarch Nest): x = 15..16, y = 4..8
    for nm, sx, sy in (('cr_purple_t', 15, 4), ('cr_teal_t', 16, 4),
                       ('cr_teal_t', 15, 6), ('cr_purple_t', 16, 6),
                       ('cr_purple_c', 15, 8), ('cr_blue_c', 16, 8)):
        m.stamp(nm, sx, sy)
    # Divider 2 (between Center Matriarch Nest and NE Cocoon-House/TM81): x = 22..23, y = 4..8
    for nm, sx, sy in (('cr_teal_t', 22, 4), ('cr_purple_t', 23, 4),
                       ('cr_purple_t', 22, 6), ('cr_teal_t', 23, 6),
                       ('cr_blue_c', 22, 8), ('cr_purple_c', 23, 8)):
        m.stamp(nm, sx, sy)
    # Seal outer flanks of the north amphitheater (x=8 and x=30 on rows 4..8) cleanly
    for sx, c_tid in ((8, P1('cr_blue_c')), (30, P1('cr_teal_c'))):
        for sy in (4, 5):
            m.L[1, sy, sx] = c_tid
            m.taken[sy, sx] = True
    for nm, sx, sy in (('cr_blue_t', 8, 5), ('cr_purple_c', 8, 7), ('cr_teal_c', 8, 8),
                       ('cr_teal_t', 30, 5), ('cr_purple_c', 30, 7), ('cr_blue_c', 30, 8)):
        m.stamp(nm, sx, sy)

    # ---- 8. West Living Gateposts, Trees, South Choked Road Crystals & Anchor Shimmer Lines ----
    # Mossy living gateposts framing the Bleed Veil (x=4, y=12..13 and y=19..20; leaves 14..18 clear!)
    m.stamp('nr_col', VX, 12)
    m.stamp('nr_col', VX, 19)
    # Living green oaks/pines west of the Veil
    m.stamp('tr_oak2', 0, 11)
    m.stamp('tr_pine', 0, 18)
    m.stamp('nt_bush0', 2, 13)
    m.stamp('nt_bush1', 2, 19)

    # South Glass-Choked Road barricade framing (18, 33) (old road to Thistledown Lea choked shut with crystal!)
    for nm, sx, sy in (('cr_purple_t', 16, 31), ('cr_teal_t', 20, 31),
                       ('cr_purple_c', 16, 33), ('cr_teal_c', 17, 33),
                       ('cr_blue_c', 19, 33), ('cr_purple_c', 20, 33),
                       ('gd_shard0', 15, 29), ('gd_shard1', 21, 29)):
        if m.inb(sx, sy) and not m.taken[sy, sx]:
            m.stamp(nm, sx, sy)

    # Crystal obelisks, warm trail lanterns, silk racks & shards anchoring the crater clearing
    for nm, sx, sy in (('gw_spool', 29, 20), ('gw_rack', 29, 22),
                       ('pf_lantern', 16, 14), ('pf_lantern', 22, 14),
                       ('pf_lantern', 8, 12), ('pf_lantern', 30, 12),
                       ('pf_lantern', 16, 27), ('pf_lantern', 20, 27),
                       ('cr_purple_t', 13, 12), ('cr_teal_t', 24, 12),
                       ('cr_teal_t', 7, 17), ('cr_purple_t', 30, 17),
                       ('cr_blue_t', 12, 23), ('cr_pink_t', 22, 23),
                       ('cr_purple_t', 14, 27), ('cr_teal_t', 22, 27),
                       ('gd_shard0', 11, 20), ('gd_shard1', 25, 19)):
        s = STAMPS[nm]
        ok = True
        for dy in range(s['h']):
            for dx in range(s['w']):
                xx, yy = sx + dx, sy + dy
                if not m.inb(xx, yy) or m.taken[yy, xx] or m.cliff[yy, xx] or m.cls[yy, xx] == 'w' or r.road_mask[yy, xx]:
                    ok = False
        if ok:
            m.stamp(nm, sx, sy)

    # Prismatic crystal-silk glints tracing north from Anchors 1-3 toward the ravine (clean translucent shimmer!)
    for ax, ay in ANCHORS:
        for ty in range(12, ay):
            if m.ht[ty, ax] == 0 and m.cls[ty, ax] in '.d' and not m.taken[ty, ax] and not m.cliff[ty, ax]:
                m.L[2, ty, ax] = 25824 + ((ax + ty) % 3)

    # ---- 9. Frosted Crystal Crater Rim Forest & Ring of Crystal Trees (zero overlaps!) ----
    def can_put_tree(nm, tx, ty, rim_only=False):
        s = STAMPS[nm]
        w, h = s['w'], s['h']
        if tx < 0 or ty < 0 or tx + w > W or ty + h > H:
            return False
        if tx < 5 and 11 <= ty + h and ty <= 21:
            return False
        for dy in range(h):
            for dx in range(w):
                xx, yy = tx + dx, ty + dy
                if m.taken[yy, xx] or m.cls[yy, xx] in 'we':
                    return False
                if dy >= h - 2:
                    if m.cliff[yy, xx] or r.road_mask[yy, xx]:
                        return False
                    if rim_only and m.ht[yy, xx] != 1:
                        return False
                else:
                    # Keep canopy off key north landmarks, Veil, anchors, bridges, and existing cliffs/cottage roofs
                    if (xx, yy) in ((NX, NY), (13, 6), (25, 6), (26, 21), (27, 22), (18, 33)) or yy in RAVINE:
                        return False
        return True

    # Hand-placed interior crystal grove trees ringing the crater clearing like a frosted harp amphitheater
    interior_grove = [
        ('kf_tree', 5, 11), ('kf_tree', 30, 11),
        ('nt_tree_purp', 12, 12), ('nt_tree_blue', 23, 12),
        ('nt_tree_blue', 5, 19), ('nt_tree_purp', 30, 18),
        ('nt_pine_purp', 12, 17), ('nt_pine_blue', 22, 17),
        ('kf_tree', 8, 24), ('kf_tree', 26, 24),
        ('nt_tree_purp', 13, 25), ('nt_tree_blue', 22, 25),
        ('nt_pine_blue', 6, 24), ('nt_pine_purp', 30, 23),
    ]
    for nm, tx, ty in interior_grove:
        if can_put_tree(nm, tx, ty, rim_only=False):
            m.stamp(nm, tx, ty)

    # Dense frosted crystal canopy crowning the raised crater rim (ht == 1; strictly non-overlapping!)
    rim_trees = ['kf_tree', 'nt_tree_purp', 'nt_tree_blue', 'nt_pine_purp', 'nt_pine_blue']
    for ty in range(0, H - 2):
        for tx in range(0, W - 1):
            if m.ht[min(H - 1, ty + 2), min(W - 1, tx + 1)] != 1:
                continue
            nm = rng.choice(rim_trees)
            if can_put_tree(nm, tx, ty, rim_only=True):
                m.stamp(nm, tx, ty)
    # Fill remaining rim gaps with smaller frosted pines & crystal clusters so ZERO isolated rim tiles remain
    for ty in range(0, H):
        for tx in range(0, W):
            if m.ht[ty, tx] != 1 or m.taken[ty, tx] or m.cliff[ty, tx]:
                continue
            if tx == 0 and ty in (0, 1, 2):
                continue
            placed = False
            for nm in ('nt_pine_purp', 'nt_pine_blue'):
                if can_put_tree(nm, tx, max(0, ty - 2), rim_only=True):
                    m.stamp(nm, tx, max(0, ty - 2))
                    placed = True
                    break
            if not placed:
                m.stamp(rng.choice(['cr_purple_c', 'cr_teal_c', 'cr_blue_c', 'cr_pink_c']), tx, ty)

    # Hanging crystal-silk cocoons tucked naturally beneath interior crystal tree canopies & around Glass cocoons (27, 22)
    for gx, gy in ((6, 13), (31, 13), (13, 14), (24, 14), (6, 21), (26, 20), (28, 20), (9, 26), (27, 26)):
        if m.inb(gx, gy + 1) and not m.cliff[gy, gx]:
            m.over.append((2, gx, gy, 22751))
            m.over.append((2, gx, gy + 1, 22752))

    # Subtle frosted ground flowers, crystal clusters & Bleed shimmer sparkles
    for y in range(4, H - 2):
        for x in range(5, W - 2):
            if m.ht[y, x] != 0 or m.taken[y, x] or m.cliff[y, x] or m.cls[y, x] == 'w':
                continue
            if m.L[1, y, x] == 0 and m.L[2, y, x] == 0:
                rv = rng.random()
                if m.cls[y, x] == '.' and not r.road_mask[y, x] and rv < 0.045:
                    m.stamp(rng.choice(['cr_purple_c', 'cr_teal_c', 'cr_blue_c', 'cr_pink_c', 'gd_shard2']), x, y)
                elif m.cls[y, x] == '.' and rv < 0.14:
                    m.L[1, y, x] = rng.choice([9725, 9725, 10620])
                elif rv < 0.22:
                    m.L[2, y, x] = rng.choice([25824, 25825, 25826])

    # ---- 10. Commit stamps & draw the shimmering Bleed Veil down x = 4 ----
    m.put_stamps()
    veil_tiles = [26048, 26049, 26050]
    bleed_tiles = [25824, 25825, 25826]
    for y in range(14, 19):
        m.L[2, y, VX] = veil_tiles[y % 3]
        if m.L[2, y, VX + 1] == 0:
            m.L[2, y, VX + 1] = bleed_tiles[y % 3]

    # ---- 11. Events (100% contract-preserved; cancel=2 fix on D3 anchors; Juno cleanly west of Veil) ----
    E = []
    E.append({'type': 'sign', 'name': 'Glass-choked way', 'at': [18, 33], 'post': False, 'text': 'The old way south to Thistledown Lea is choked with glass. The Deepwood is the only way in or out now.'})   # map builder 9: Rev 14, no R3_COCOON
    E.append({'type': 'warp', 'name': 'To the Deepwood', 'at': [0, 16], 'link': 'DEEP_COCOON', 'arrive': [1, 16, 'right']})
    E.append(_fog_event_548('prismfall_glass', 74, 1, 200, 1, 1))
    E.append({'type': 'event', 'name': 'Escort setup', 'at': [0, 1], 'pages': [
        {'trigger': 'parallel', 'commands': [{'if': key(548, 'ESCORT') + ' && !$game_switches[107]', 'then': [reveal('Juno', 'Tamsin')], 'else': []},
                                             {'selfswitch': ['A', True]}]},
        {'cond': {'self': 'A'}}]})
    E.append({'type': 'event', 'name': 'Juno', 'at': P['juno'], 'pages': [
        {'commands': []},
        {'cond': {'self': 'A'}, 'graphic': {'sprite': 'trainer_RIVAL2', 'dir': 'right'}, 'commands': [
            say('JUNO', 'neutral', "Shout if— no. You can't hear through it, can you. Just come back.")]}]})
    E.append({'type': 'event', 'name': 'Tamsin', 'at': P['tamsin'], 'pages': [
        {'commands': []},
        {'cond': {'self': 'A'}, 'graphic': {'sprite': 'trainer_LASS', 'dir': 'right'}, 'commands': [
            say('TAMSIN', 'sad', "I can't cross it. Nobody can. ...Except you, apparently. Gran would have had words for that.")]}]})
    outro = [{'if': "pf_choice(:ch2_matriarch) == :soothe", 'then': [
                 say('TAMSIN', 'crying', "Half the grove. ...Half. And the moths that are left are *singing*. I'll take half. I'll take it."),
                 say('JUNO', 'happy', "You stayed all night! We could see you through the shimmer, just sitting there! Kestrel would've hated it!")],
              'else': [
                 say('TAMSIN', 'shocked', "It just... stopped. All of it."),
                 "(The Matriarch walks out through the Veil, past them, into the wood. It doesn't react to anything.)",
                 say('TAMSIN', 'neutral', "Oh. Oh, that's — thank you. I think."),
                 say('JUNO', 'sad', "...It didn't look at me. They always look at me.")]},
             say('TAMSIN', 'neutral', "The next Warden's Marisol Reyes, in Ebbmouth. North over Spinners' Rise, through the Rimewood and over the border. She'll swear at you. It's a compliment."),
             say('TAMSIN', 'happy', "Come back, will you? I'd like to show you the room when it isn't tangled."),
             say('JUNO', 'neutral', "I've got to take the eggs to Uncle Rowan in Verdance. Forty eggs, one hatbox, no running."),
             say('JUNO', 'sad', "I'm going to tell him about the Pageant. About what the man said about Verdance. I want to see his face when I tell him."),
             {'script': "%w[Juno Tamsin].each do |n|\n  ev = $game_map.events.values.find { |e| e.name == n }\n  ev.erase if ev\nend"}]
    for i, y in enumerate((14, 15, 16, 17, 18)):
        E.append({'type': 'event', 'name': 'Veil %d' % (i + 1), 'at': [VX, y], 'pages': [
            {'cond': {'switch': 'CH2_MATRIARCH_DONE'}, 'trigger': 'touch', 'through': True, 'commands': once(548, 'OUTRO', outro)}]})
    boss = [
        "(At the center, a Galvantula the size of a cart, half crystal, sits on a nest of glass silk wound around something that glows faintly green beneath the roots.)",
        "It turns eight eyes on you. Four of them are glass.",
        {'boss': {'id': 'GLASS_MATRIARCH', 'species': 'GALVANTULA', 'level': 21, 'field': 'BLEED'}},   # segment 2 boss: cap 23 - 2
        "The Matriarch collapses onto the nest. The ringing drops by half. It thrashes, shedding slivers of crystal.",
        {'choices': ["Stay with it.", "Put your hand on it. Make it stop."], 'cancel': 0, 'branches': [
            [{'script': 'pf_choose(:ch2_matriarch, :soothe)'},
             "You sit down in the glass. You hold Mother Loom's shuttle because you don't know what else to hold.",
             {'tone': [-120, -120, -80, 0, 40]}, {'wait': 60}, {'tone': [-20, -10, 10, 30, 60]},
             "The Matriarch is asleep against your knee. Around you, half the grove has gone to glass in the night. The other half hasn't.",
             "The ringing has stopped."],
            [{'script': 'pf_choose(:ch2_matriarch, :silence)'},
             "You press your palm to its crystal side.",
             "Something goes out of it, like water down a drain. Through you. To nowhere.",
             "The crystal falls away as dust. The grove stops ringing at once. Not one more tree turns.",
             "The Matriarch stands. It is whole. Its eyes are dull as buttons. It doesn't look at you. It doesn't look at anything."]]},
        {'switch': ['CH2_MATRIARCH_DONE', True]}, {'switch': ['GLOAMING_DISGUISED_CELESTINE', False]}, {'var': ['BRIARWICK_GLASSWOOD', 1]},
        "(Under the nest, a sliver of green light sinks back into the roots as you watch.)",
        "FIELD NOTES: \"Something under the Hollow is holding the wood together. I think I was standing on it. — note to self: ask Tamsin where the Plate is.\"",
        {'selfswitch': ['A', True]}]
    E.append({'type': 'event', 'name': 'Glass Matriarch', 'at': P['matriarch'], 'pages': [
        {'graphic': {'sprite': 'Followers/GALVANTULA', 'dir': 'down'}, 'move': 'fixed', 'commands': boss},
        {'cond': {'self': 'A'}, 'commands': []}]})
    E.append({'type': 'npc', 'name': 'Cocooned house', 'at': P['house'], 'sprite': '',
              'text': "A cottage wrapped whole in crystal silk. Something inside is breathing slowly."})
    E.append({'type': 'sign', 'at': P['cocoons'], 'post': False, 'name': 'Glass cocoons',
              'text': "Dozens of glass cocoons, hanging. Inside each, a moth, wings spread, perfectly still.\nOne of them twitches."})
    E.append({'type': 'item', 'at': P['tm'], 'item': 'TM81'})
    # D3 (DUNGEON_PUZZLES): the bridges are taut while their switch is on (S511-S513, D3_BRIDGE_A/B/C) or once the
    # Matriarch is done (the nest's thread snaps all three taut: the way home); every anchor flips two bridges
    for k, sw in (('a', 'D3_BRIDGE_A'), ('b', 'D3_BRIDGE_B'), ('c', 'D3_BRIDGE_C')):
        for y in RAVINE:
            E.append({'type': 'event', 'name': 'Bridge %s %d' % (k, y - RAVINE[0] + 1), 'at': [XING[k], y], 'pages': [
                {'through': True, 'commands': []},
                {'cond': {'switch': sw}, 'graphic': {'tile': BRIDGE_TILE}, 'commands': []},
                {'cond': {'switch': 'CH2_MATRIARCH_DONE'}, 'graphic': {'tile': BRIDGE_TILE}, 'commands': []}]})
    flip = {1: (511, 512), 2: (512, 513), 3: (511, 513)}
    for n, (ax, ay) in enumerate(ANCHORS, 1):
        a, b = flip[n]
        E.append({'type': 'event', 'name': 'Anchor %d' % n, 'at': [ax, ay], 'pages': [{'graphic': {'sprite': 'Object ball', 'dir': 'down'}, 'commands': [
            'A cocoon anchor, its crystal threads running north to the ravine. %s' % ('The left one.' if n == 1 else 'The middle one.' if n == 2 else 'The right one.'),
            {'if': 'pfm_has?(:MOTHERLOOMSSHUTTLE) || pf_choice(:ch2_tamsin)', 'then': [
                {'choices': ['Re-thread it.', 'Leave it.'], 'cancel': 2, 'branches': [
                    [{'script': '$game_switches[%d] = !$game_switches[%d]\n$game_switches[%d] = !$game_switches[%d]\n$game_map.need_refresh = true' % (a, a, b, b)},
                     {'se': 'Mining reveal'}, 'Two threads sing as they change: one draws taut, one falls slack.'], []]}],
             'else': ['The threads are glass. You would need something to re-thread them.']}]}]})
    E.append({'type': 'event', 'name': 'D3 start', 'at': [0, 2], 'pages': [   # first entry: bridges a and b start taut
        {'trigger': 'autorun', 'commands': [{'switch': ['D3_BRIDGE_A', True]}, {'switch': ['D3_BRIDGE_B', True]}, {'selfswitch': ['A', True]}]},
        {'cond': {'self': 'A'}, 'trigger': 'parallel', 'commands': []}]})

    m.events = E
    head = {
        '_file': '525_deepwood_cocoonfall.yaml',
        'id': 548,
        'biome': 'bleed',
        'name': 'Cocoonfall Hollow',
        'bgm': 'Route 3',
        'parent': 540,
        'field': 'BLEED',
        'tone': [-18, -22, 18, 42],
        'metadata': {'ShowArea': True, 'SnapEdges': True, 'MapPosition': [0, 11, 22], 'BattleBack': 'forest'},
        'walk_from': [[NX, NY + 2], [XING['b'], 8], [XING['a'], 8]],
        'rubric': True,
    }
    m.write(548, head, '# Cocoonfall Hollow (548, ts=52 PF Rejuv Snow). WRITTEN BY layouts/deepwood.py hollow() - edit that, not this file.\n')
    print('  wrote 525_deepwood_cocoonfall.yaml (548, ts=52 PF Rejuv Snow)')


if __name__ == '__main__':
    if sys.argv[1:] == ['548']:                                 # map builder 10: 548 alone (525 is routes_craft.py's)
        hollow()
        raise SystemExit(0)
    raise SystemExit('superseded by layouts/reskin.py (MAPGEN 2h): running this would overwrite the PF Rejuv spec')
if False:
    save('525_deepwood_cocoonfall.yaml', deepwood(), hollow())
