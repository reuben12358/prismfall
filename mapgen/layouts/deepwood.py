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
                  {'if': 'Prismfall.cameo_battle(:FESTIVAL_SHELLY, "Shelly", 1, double: true, field: :SILKWOOD)',
                   'then': [
                       say('SHELLY', 'happy', "Your forest sounds like home used to, before the city got sick. Look after it?"),
                       {'script': 'pbReceiveItem(:SILVERPOWDER)'}, {'script': struggle},
                       {'switch': ['CAMEO_SHELLY_DONE', True]}, {'script': '$game_variables[123] += 1'},
                       "(She steps into the pond's reflection and is gone. One pink ribbon floats on the water.)", {'selfswitch': ['A', True]}],
                   'else': [
                       {'script': '$player.heal_party'},
                       say('SHELLY', 'panic', "Oh! I'm so sorry, I got carried away—here, let me patch your team up! We can try again whenever you're ready.")]}]
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
                {'script': 'setBattleRule("field", :BLEED)\nsetBattleRule("canLose")'},
                {'if': 'WildBattle.start(:MASQUERAIN, 19)',
                 'then': ["The Masquerain folds its glass wings and settles on the water. The ringing stops.", setk(525, 'MASQ'), {'selfswitch': ['A', True]}],
                 'else': [{'script': '$player.heal_party'}, "The ringing glass drives you back. You catch your breath by the dew pond."]}],
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
    cx, cy = 19, 17
    NX, NY = 19, 5

    # Crisp 3-row frosted Sheridan crater rim cliff (lip / face / base, all pas=15)
    if 'shs3' not in K.KITS:
        K.KITS['shs3'] = dict(K.KITS['shs'], rows=[K.KITS['shs']['rows'][0],
                                                   K.KITS['shs']['rows'][1],
                                                   K.KITS['shs']['rows'][3]])

    r = Route(548, W, H, theme='snow', kit='shs3', base='.')
    m = r.m
    # Calm Kristiline snow base (texture lives in layered crystal turf, packed snow, drifts, and canopies — NOT blinding flat white!)
    m.grass = K.SNOW_GROUND
    m.tall = K.SNOW_TALL
    m.STAIRS = tuple(STAMPS['fw_stair_' + k]['layers'][1][0][0] for k in 'lmr')
    m.grass2 = None
    m.lattice = K.RMap.TREES_SNOW
    # Use KristilineWatersFrozen ('o') for the jagged glowing crystal-rimmed Glass Ravine,
    # Packed Snow ('d') for winding frosted footpaths, KristilineDirt ('e') for living entry, Frozen Pond ('p') for side melt-pools
    m.auto = {
        'd': ('Packed Snow', 'pf'),
        'e': ('KristilineDirt', 'rejuvenation'),
        'w': ('KristilineWatersFrozen', 'rejuvenation'),
        'o': ('KristilineWatersFrozen', 'rejuvenation'),
        'p': ('Frozen Pond', 'pf'),
        'W': ('Sea deep', 'rejuvenation'),
    }
    m.JOIN = dict(K.RMap.JOIN, w='woW', o='woW', p='p', e='e')
    m.AUTO_Z = dict(K.RMap.AUTO_Z, w=0, o=0, p=0, e=1)
    m.keep_under = 'de'
    rng = random.Random(5488)

    def in_living(x, y):
        return (x <= 3 and 13 <= y <= 19) or (x == 4 and 14 <= y <= 18)

    # ---- 1. Sculpted Asymmetric Crater Bowl + Three Recessed North Cathedral Cliff Alcoves ----
    # Continuous smooth amphitheater rim (ht=1) with ZERO floating 2-wide interior cliff stubs!
    m.ht[:, :] = 1
    # Main organic asymmetric basin floor (x 5..32, y 11..27, wider on W/E, narrower curving waist south)
    for y in range(11, 29):
        for x in range(5, 34):
            # Asymmetric bulge: SW opens slightly for frozen pond cove, SE pinches inward with crystal grove
            shift_x = -0.8 if y >= 23 else 0.4 * math.sin((y - 11) * 0.45)
            rx = 13.6 - (1.8 if y >= 24 else 0.0)
            ry = 8.8
            q = ((x - (19.0 + shift_x)) / rx) ** 2 + ((y - 18.8) / ry) ** 2
            q += 0.14 * (vnoise(x, y, 5481, 4.0) - 0.5)
            if q <= 1.0:
                m.ht[y, x] = 0

    # Carve clean sacred depressed zones:
    m.ht[13:20, 0:9] = 0                    # West living grove entry through Veil
    m.ht[9:14, 6:33] = 0                    # Full Glass Ravine & bridgehead terrace
    m.ht[14:24, 6:32] = 0                   # Clean interior bowl (trees & crystals shape internal sightlines!)
    m.ht[24:29, 6:16] = 0                   # SW curved frozen melt-pond cove
    m.ht[24:28, 22:30] = 0                  # SE sunken crystal-shrine alcove
    m.ht[24:34, 16:21] = 0                  # South glass-choked gorge

    # THREE RECESSED NORTH CATHEDRAL ALCOVES (y=1..8) separated by SOLID RAISED CLIFF SPURS (ht=1)
    m.ht[0, :] = 1
    m.ht[1:9, 9:15] = 0                     # NW Cocooned Cottage alcove
    m.ht[1:9, 17:22] = 0                    # Center Glass Matriarch Cathedral alcove
    m.ht[1:9, 24:30] = 0                    # NE Cocoon-House & TM81 alcove
    m.ht[0:7, 15:17] = 1; m.ht[7:9, 15:17] = 0
    m.ht[0:7, 22:24] = 1; m.ht[7:9, 22:24] = 0
    m.ht[0:7, 0:9] = 1; m.ht[0:7, 30:38] = 1
    m.ht[7:9, 6:9] = 0; m.ht[7:9, 30:33] = 0

    # Clean any 1-cell jagged cliff spurs so shs3 walls read as smooth continuous natural ridges
    for _ in range(3):
        hi = (m.ht == 1)
        pad = np.pad(hi, 1, constant_values=True)
        n4 = pad[:-2, 1:-1].astype(int) + pad[2:, 1:-1] + pad[1:-1, :-2] + pad[1:-1, 2:]
        m.ht[hi & (n4 <= 1)] = 0
        m.ht[~hi & (n4 >= 3)] = 1

    # Re-assert sacred flat zones & solid cliff spurs
    m.ht[0, :] = 1
    m.ht[1:9, 9:15] = 0; m.ht[1:9, 17:22] = 0; m.ht[1:9, 24:30] = 0
    m.ht[0:7, 15:17] = 1; m.ht[7:9, 15:17] = 0
    m.ht[0:7, 22:24] = 1; m.ht[7:9, 22:24] = 0
    m.ht[0:7, 0:9] = 1; m.ht[0:7, 30:38] = 1
    m.ht[9:14, 6:33] = 0; m.ht[14:24, 6:32] = 0
    m.ht[13:20, 0:9] = 0; m.ht[24:34, 16:21] = 0

    # ---- 2. The Jagged Glass Ravine (KristilineWatersFrozen 'w') & Asymmetric SW Frozen Melt-Pond ('p') ----
    for y in RAVINE:
        for x in range(W):
            if m.ht[y, x] == 0:
                m.cls[y, x] = 'w'
    # Organic jagged ravine coves curving into y=11..12 between the 3 bridgeheads (NEVER touching x in {9..11, 18..20, 27..29})
    for x in range(6, 33):
        if any(abs(x - bx) <= 1 for bx in XING.values()):
            continue
        if m.ht[11, x] == 0 and x in (6, 7, 8, 12, 13, 14, 15, 16, 22, 23, 24, 25, 26, 30, 31, 32):
            m.cls[11, x] = 'w'
        if m.ht[12, x] == 0 and x in (13, 14, 15, 23, 24, 25):
            m.cls[12, x] = 'w'
    # Deep twilight water core along center of wider ravine bays
    for y, x in ((10, 14), (10, 15), (10, 23), (10, 24), (11, 14), (11, 24)):
        if m.cls[y, x] == 'w':
            m.cls[y, x] = 'W'

    # Asymmetric organic SW Frozen Melt-Pond curving around (8..13, 25..28) (SE is a completely different crystal-shrine grove!)
    for y in range(25, 29):
        for x in range(6, 15):
            if m.ht[y, x] == 0 and m.cls[y, x] == '.':
                if ((x - 10.2) / 3.4) ** 2 + ((y - 26.8) / 1.9) ** 2 + 0.25 * (vnoise(x, y, 5484, 2.2) - 0.5) <= 1.0:
                    m.cls[y, x] = 'p'

    # ---- 3. Sinuous Organic Winding Footpaths ----
    def lane(pts, width=1.75, cls='d', wobble=0.35):
        P_pts = [pts[0]] + list(pts) + [pts[-1]]
        for i in range(1, len(P_pts) - 2):
            p0, p1, p2, p3 = P_pts[i - 1], P_pts[i], P_pts[i + 1], P_pts[i + 2]
            steps = max(abs(p2[0] - p1[0]), abs(p2[1] - p1[1]), 1) * 4
            for k in range(steps + 1):
                t = k / float(steps); t2, t3 = t * t, t * t * t
                px = 0.5 * (2 * p1[0] + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
                py = 0.5 * (2 * p1[1] + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
                rad = width * 0.50 + wobble * (vnoise(px, py, 5486, 3.0) - 0.5)
                for yy in range(int(py) - 2, int(py) + 3):
                    for xx in range(int(px) - 2, int(px) + 3):
                        if not m.inb(xx, yy) or m.cls[yy, xx] in 'wWp' or m.ht[yy, xx] != 0:
                            continue
                        if (xx - px) ** 2 + (yy - py) ** 2 <= rad * rad:
                            m.cls[yy, xx] = cls
                            r.road_mask[yy, xx] = True

    for x in range(0, 5):
        for y in (15, 16, 17):
            m.cls[y, x] = 'e'
            r.road_mask[y, x] = True

    lane([(5, 16), (9, 16), (13, 17), (19, 17)], width=1.9)                    # Veil -> central crystal heart
    lane([(9, 16), (10, 14), (10, 11)], width=1.55)                            # NW spur to Bridge b
    lane([(19, 17), (19, 14), (19, 11)], width=1.7)                            # ceremonial axis to Bridge c
    lane([(19, 17), (24, 16), (28, 14), (28, 11)], width=1.55)                 # NE curve to Bridge a
    lane([(9, 16), (8, 19), (8, 22), (12, 23), (16, 22), (20, 23), (24, 22), (27, 22)], width=1.8)  # Anchor terrace arc
    lane([(19, 17), (17, 22), (19, 27), (18, 32)], width=1.7)                  # gently curving south choked way
    lane([(10, 8), (10, 6), (13, 6)], width=1.55)
    lane([(19, 8), (19, 6)], width=1.7)
    lane([(28, 8), (27, 6), (25, 6)], width=1.55)
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
        (27, 22), (26, 22), (26, 21), (25, 21), (25, 22),
    ] + list(ANCHORS) + [(bx, y) for bx in XING.values() for y in (8, 11, 12)]
    for x, y in must_keep:
        r.road_mask[y, x] = True
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                xx, yy = x + dx, y + dy
                if m.inb(xx, yy) and m.cls[yy, xx] not in 'wWp' and m.ht[yy, xx] == 0:
                    if (xx, yy) not in ((15, 6), (16, 6), (22, 6), (23, 6), (15, 7), (16, 7), (22, 7), (23, 7), (15, 8), (16, 8), (22, 8), (23, 8)):
                        r.road_mask[yy, xx] = True

    # ---- 5. Dense Interlocking Perimeter Forest (class 'T' -> TREES_SNOW lattice!) ----
    m.plan_cliffs(rows=3)
    for y in range(H):
        for x in range(W):
            if m.ht[y, x] == 1 and not m.cliff[y, x] and not in_living(x, y):
                if not (x in (15, 16, 22, 23) and y <= 8):
                    m.cls[y, x] = 'T'
    # Organic woodland peninsulas sweeping into the lower flanks to hug the basin snugly
    for cx_t, cy_t, rx_t, ry_t in ((5, 24, 2.4, 3.2), (32, 20, 2.6, 4.0), (14, 31, 2.6, 2.6), (23, 30, 3.0, 3.2)):
        for y in range(max(0, int(cy_t - ry_t - 1)), min(H, int(cy_t + ry_t + 2))):
            for x in range(max(0, int(cx_t - rx_t - 1)), min(W, int(cx_t + rx_t + 2))):
                if m.ht[y, x] == 0 and m.cls[y, x] == '.' and not r.road_mask[y, x] and not m.cliff[y, x]:
                    if ((x - cx_t) / rx_t) ** 2 + ((y - cy_t) / ry_t) ** 2 <= 1.0:
                        m.cls[y, x] = 'T'

    # ---- 6. Frosted Tall Grass Pockets tucked naturally beside trails & crystal groves ----
    for cx_g, cy_g, rx, ry in ((12, 19, 2.2, 1.5), (24, 18, 2.5, 1.6), (15, 26, 2.0, 1.5), (22, 25, 2.2, 1.5)):
        for y in range(max(12, int(cy_g - ry - 1)), min(H - 3, int(cy_g + ry + 2))):
            for x in range(max(6, int(cx_g - rx - 1)), min(W - 4, int(cx_g + rx + 2))):
                if m.cls[y, x] == '.' and m.ht[y, x] == 0 and not r.road_mask[y, x] and not m.cliff[y, x]:
                    if ((x - cx_g) / rx) ** 2 + ((y - cy_g) / ry) ** 2 + 0.22 * (vnoise(x, y, 5489, 2.8) - 0.5) <= 1.0:
                        m.cls[y, x] = 't'

    # ---- 7. Paint Base Terrain, Autotiles, Cliffs, and Interlocking Snow-Forest Lattice ----
    m.paint_ground()
    m.autotiles()
    m.cliffs()
    m.forest(K.RMap.TREES_SNOW, vstep=2)

    # ---- 8. Seamless Layered Crystalline Ground (White Snow -> Lavender Crystal -> Deep Amethyst Core) ----
    def paint_bordered_turf(mask, tiles_3x3, inner_4, center_alts=()):
        nw, n_, ne, w_, c_, e_, sw, s_, se = tiles_3x3
        in_nw, in_ne, in_sw, in_se = inner_4
        for y in range(H):
            for x in range(W):
                if not mask[y, x]:
                    continue
                up = y > 0 and mask[y - 1, x]
                dn = y + 1 < H and mask[y + 1, x]
                lf = x > 0 and mask[y, x - 1]
                rt = x + 1 < W and mask[y, x + 1]
                if not up and not lf: t = nw
                elif not up and not rt: t = ne
                elif not dn and not lf: t = sw
                elif not dn and not rt: t = se
                elif not up: t = n_
                elif not dn: t = s_
                elif not lf: t = w_
                elif not rt: t = e_
                else:
                    ul = y > 0 and x > 0 and mask[y - 1, x - 1]
                    ur = y > 0 and x + 1 < W and mask[y - 1, x + 1]
                    dl = y + 1 < H and x > 0 and mask[y + 1, x - 1]
                    dr = y + 1 < H and x + 1 < W and mask[y + 1, x + 1]
                    if not ul and in_nw: t = in_nw
                    elif not ur and in_ne: t = in_ne
                    elif not dl and in_sw: t = in_sw
                    elif not dr and in_se: t = in_se
                    elif center_alts and ((x * 7 + y * 13) % 3 == 0):
                        t = center_alts[(x + y) % len(center_alts)]
                    else:
                        t = c_
                m.L[0, y, x] = t

    # White-snow-bordered lavender crystal turf (9901..9934): organic Bleed aura spreading across the hollow floor & north alcoves!
    lav_mask = np.zeros((H, W), dtype=bool)
    for cx_l, cy_l, rx_l, ry_l in (
        (19, 17, 6.2, 4.4),   # wide central crystal heart
        (10, 13, 2.5, 2.2),   # Bridge b crystal verge
        (19, 12, 2.6, 2.2),   # Bridge c crystal verge
        (28, 13, 2.5, 2.2),   # Bridge a crystal verge
        (8, 22, 3.4, 2.4),    # Anchor 1 crystalline ring
        (16, 22, 3.8, 2.5),   # Anchor 2 crystalline ring
        (25, 22, 4.4, 2.8),   # Anchor 3 + Glass cocoons grove
        (11, 6, 3.4, 3.0),    # NW cottage shelf
        (19, 6, 3.4, 3.2),    # Center Matriarch shelf
        (27, 6, 3.4, 3.0),    # NE cottage shelf
    ):
        for y in range(3, H - 2):
            for x in range(5, W - 2):
                if m.ht[y, x] == 0 and m.cls[y, x] in '.dt' and not m.cliff[y, x]:
                    if ((x - cx_l) / rx_l) ** 2 + ((y - cy_l) / ry_l) ** 2 + 0.16 * (vnoise(x, y, 5491, 2.8) - 0.5) <= 1.0:
                        lav_mask[y, x] = True
    # Native seamless frosted snow variation across the crater floor (replaces hard-edged lavender rectangles!)
    sn_g = [K.P1('sn_g%d' % i) for i in range(4)]
    for y in range(3, H - 2):
        for x in range(5, W - 2):
            if m.ht[y, x] == 0 and m.cls[y, x] == '.' and not m.cliff[y, x] and vnoise(x, y, 5491, 4.5) > 0.42:
                m.L[0, y, x] = sn_g[int(vnoise(x, y, 5497, 2.6) * 3.999)]

    # Keep twilight-amethyst sanctuary floor strictly inside the walled Matriarch cathedral alcove (x=17..21, y=4..8)
    ame_mask = np.zeros((H, W), dtype=bool)
    for y in range(4, 9):
        for x in range(17, 22):
            if m.ht[y, x] == 0 and not m.cliff[y, x] and m.cls[y, x] not in 'wWp':
                ame_mask[y, x] = True
    paint_bordered_turf(
        ame_mask,
        (9488, 9489, 9490, 9496, 9497, 9498, 9504, 9505, 9506),
        (9491, 9492, 9499, 9500),
        center_alts=(9497, 9500),
    )

    # Soft shaded snow variation on remaining plain snow tiles
    for y in range(H):
        for x in range(W):
            if m.cls[y, x] == '.' and not in_living(x, y) and not m.cliff[y, x] and not lav_mask[y, x] and not ame_mask[y, x]:
                if vnoise(x, y, 5485, 3.0) > 0.54:
                    m.L[0, y, x] = 10395

    # Living Sheridan emerald forest pocket west of the Bleed Veil (x <= 3, y 12..20)
    for y in range(11, 22):
        for x in range(0, 5):
            if in_living(x, y) or (x <= 3 and 11 <= y <= 21 and m.ht[y, x] == 0):
                if m.cls[y, x] in '.tT':
                    m.L[0, y, x] = K.GRASS_DARK[y & 1][x & 1] if (x <= 1 or y in (12, 13, 19, 20)) else K.SH_GRASS[y & 1][x & 1]
                    if not r.road_mask[y, x] and m.L[1, y, x] == 0:
                        if (x * 7 + y * 11) % 3 == 0:
                            m.L[1, y, x] = K.DECOR_SH['flowers'][(x + y) % len(K.DECOR_SH['flowers'])]
                        elif (x * 5 + y * 3) % 2 == 0:
                            m.L[1, y, x] = K.DECOR_SH['green'][(x + y) % len(K.DECOR_SH['green'])]

    # Helper to place raw Rejuvenation Kristiline multi-tile hero sprites cleanly with exact passability/priority
    def put_kf_sprite(x0, y0, top_rows, bot_rows, force=False, allow_canopy_overlap=True):
        h_top, h_bot = len(top_rows), len(bot_rows)
        w = len(bot_rows[0])
        if x0 < 0 or y0 < 0 or x0 + w > W or y0 + h_top + h_bot > H:
            return False
        if not force:
            for dy in range(h_bot):
                for dx in range(w):
                    t = bot_rows[dy][dx]
                    if t == 0: continue
                    xx, yy = x0 + dx, y0 + h_top + dy
                    if m.taken[yy, xx] or m.cliff[yy, xx] or m.cls[yy, xx] in 'wWpe' or r.road_mask[yy, xx]:
                        return False
        for dy in range(h_top):
            for dx in range(w):
                t = top_rows[dy][dx]
                if t and m.inb(x0 + dx, y0 + dy):
                    m.over.append((2, x0 + dx, y0 + dy, t))
        for dy in range(h_bot):
            for dx in range(w):
                t = bot_rows[dy][dx]
                if t and m.inb(x0 + dx, y0 + h_top + dy):
                    m.over.append((1, x0 + dx, y0 + h_top + dy, t))
                    m.taken[y0 + h_top + dy, x0 + dx] = True
        return True

    KF_TEAL_PINE_A = ([[0, 9833, 9834, 0], [0, 9841, 9842, 0]], [[0, 9849, 9850, 0], [0, 9857, 9858, 0]])
    KF_TEAL_PINE_B = ([[0, 9837, 9838, 0], [0, 9845, 9846, 0]], [[0, 9853, 9854, 0], [0, 9861, 9862, 0]])
    KF_SPRUCE_A = ([[9944, 9945, 9946], [9952, 9953, 9954]], [[9960, 9961, 9962], [9968, 9969, 9970]])
    KF_SPRUCE_B = ([[9947, 9948, 9949], [9955, 9956, 9957]], [[9963, 9964, 9965], [9971, 9972, 9973]])
    KF_CRYS_STAR = ([[9884, 9887]], [[9892, 9895]])
    KF_CRYS_BLADES = ([[9886, 9885]], [[9894, 9893]])
    KF_CRYS_MONO = ([[9868, 9869]], [[9876, 9877]])
    KF_CRYS_SHRUB_A = ([[9864, 9865]], [[9872, 9873]])
    KF_CRYS_SHRUB_B = ([[9880, 9881]], [[9888, 9889]])

    # ---- 9. North Cathedral Architecture: Cocooned Cottages, Matriarch Dais, Cliff-Spur Crystal Spines ----
    m.stamp('kf_flat', 10, 2)
    m.stamp('kf_flat', 25, 2)
    m.over.append((2, 11, 4, 22751))
    m.over.append((2, 28, 4, 22751))
    for wx, wy in ((11, 2), (26, 2)):
        st = STAMPS['pf_p_web']
        for dy in range(st['h']):
            for dx in range(st['w']):
                t = st['layers'][2][dy][dx]
                if t:
                    m.over.append((2, wx + dx, wy + dy, t))
    m.stamp('cr_purple_c', 9, 5); m.stamp('cr_teal_c', 14, 5)
    m.stamp('cr_blue_c', 29, 5); m.stamp('cr_purple_c', 24, 5)
    m.stamp('pf_lantern', 9, 6); m.stamp('pf_lantern', 29, 6)

    # Glass Matriarch Cathedral Dais at (19, 5)
    m.stamp('pf_glow', NX - 1, NY)
    m.stamp('cr_purple_t', 17, 4); m.stamp('cr_teal_t', 21, 4)
    m.stamp('fw_brazier', 17, 6); m.stamp('fw_brazier', 21, 6)
    m.stamp('cr_blue_c', 17, 8); m.stamp('cr_pink_c', 21, 8)
    st = STAMPS['pf_p_web']
    for dy in range(st['h']):
        for dx in range(st['w']):
            t = st['layers'][2][dy][dx]
            if t:
                m.over.append((2, NX - 1 + dx, NY - 2 + dy, t))
    # Frozen waterfall cascades pouring down the outer cliff shoulders into the Glass Ravine flanks
    m.stamp('fw_fall', 5, 4)
    m.stamp('fw_fall', 30, 4)

    # Crown the two raised north cliff dividers (x=15..16 & x=22..23) with GIANT LAVENDER CRYSTAL STAR CLUSTERS
    for sx in (15, 22):
        put_kf_sprite(sx, 2, *KF_CRYS_STAR, force=True)
        put_kf_sprite(sx, 4, *KF_CRYS_BLADES, force=True)
        for dx, cnm in ((0, 'cr_purple_c'), (1, 'cr_teal_c')):
            m.L[1, 8, sx + dx] = P1(cnm)
            m.taken[8, sx + dx] = True

    # ---- 10. West Living Forest Framing (Lush Green Oaks + Giant Tree + Mossy Ruin Gateposts) ----
    m.stamp('nr_col', VX, 12)
    m.stamp('nr_col', VX, 19)
    m.stamp('pf_g_tree2', 0, 8)
    m.stamp('tr_oak2', 0, 19)
    m.stamp('nt_bush0', 2, 13); m.stamp('nt_bush1', 2, 19)
    m.stamp('pf_lantern', 2, 14)

    # ---- 11. Pure Wild Giant Frosted Trees & Dense Overlapping Crystal-Spruce Groves (NO treehouses!) ----
    for nm, tx, ty in (
        ('pf_g_tree2_ice', 0, 0),     # NW ancient frosted giant tree
        ('pf_g_tree2_ice', 34, 0),    # NE ancient frosted giant tree
        ('pf_g_tree2_ice', 1, 21),    # W-SW tall frosted giant tree
        ('pf_g_tree2_ice', 33, 14),   # E tall frosted giant tree
        ('pf_g_tree2_ice', 1, 27),    # SW corner ancient frosted giant tree (no doors!)
        ('pf_g_tree2_ice', 33, 27),   # SE corner ancient frosted giant tree (no doors!)
    ):
        s = STAMPS[nm]
        if tx + s['w'] <= W and ty + s['h'] <= H:
            m.stamp(nm, tx, ty)

    # SE Asymmetric Focal Landmark: Ancient Ruined Frost Shrine + Fallen Column placed FIRST so spruces frame it cleanly!
    for nm, sx, sy in (('pf_shrine', 24, 24), ('nr_colfall', 21, 28)):
        s = STAMPS[nm]
        if all(m.inb(sx + dx, sy + dy) and not m.taken[sy + dy, sx + dx] and not m.cliff[sy + dy, sx + dx]
               and m.cls[sy + dy, sx + dx] not in 'wWp' and not r.road_mask[sy + dy, sx + dx]
               for dy in range(s['h']) for dx in range(s['w'])):
            m.stamp(nm, sx, sy)

    # Dense overlapping interior groves (clusters of 3-5 trees + crystal stars) framing intimate sightlines!
    for tx, ty, sp in (
        # NW-center & NE-center twin pine-spruce clusters framing the Bridge c ceremonial axis
        (12, 12, KF_TEAL_PINE_A), (14, 13, KF_SPRUCE_B),
        (22, 12, KF_TEAL_PINE_B), (20, 13, KF_SPRUCE_A),
        # Outer west & east flank groves hugging the crater cliffs
        (5, 11, KF_SPRUCE_A), (30, 11, KF_SPRUCE_B),
        (5, 17, KF_TEAL_PINE_B), (30, 16, KF_TEAL_PINE_A),
        # Lower-mid groves pinching the anchor terrace from the south coves
        (11, 22, KF_SPRUCE_A), (19, 23, KF_TEAL_PINE_A),
        # SE Crystal-Shrine grove (asymmetric dense evergreen-crystal wood framing the ruined shrine at (24,24)!)
        (27, 23, KF_SPRUCE_B), (28, 25, KF_TEAL_PINE_B), (22, 25, KF_SPRUCE_A),
        # SW pond bank overhanging spruces
        (5, 25, KF_TEAL_PINE_A), (13, 27, KF_SPRUCE_B),
        # South gorge flanks
        (13, 29, KF_TEAL_PINE_B), (20, 28, KF_TEAL_PINE_A),
    ):
        put_kf_sprite(tx, ty, *sp)

    # Rich kf_tree & purple/blue bleed trees woven into the grove clusters
    for nm, tx, ty in (
        ('kf_tree', 5, 10), ('kf_tree', 29, 10),
        ('nt_tree_purp', 11, 16), ('nt_tree_blue', 24, 15),
        ('nt_pine_purp', 12, 18), ('nt_pine_blue', 23, 17),
        ('nt_tree_blue', 5, 20), ('nt_tree_purp', 29, 18),
        ('nt_pine_purp', 21, 29), ('nt_pine_blue', 15, 29),
    ):
        s = STAMPS[nm]
        if tx >= 0 and ty >= 0 and tx + s['w'] <= W and ty + s['h'] <= H:
            foot_ok = True
            for dy in range(max(0, s['h'] - 2), s['h']):
                for dx in range(s['w']):
                    xx, yy = tx + dx, ty + dy
                    if m.taken[yy, xx] or m.cliff[yy, xx] or m.cls[yy, xx] in 'wWpe' or r.road_mask[yy, xx]:
                        foot_ok = False
            if foot_ok:
                m.stamp(nm, tx, ty)

    # Clustered giant Rejuvenation crystal star-bursts, sapphire monoliths & frosted berry-crystal shrubs
    for tx, ty, sp in (
        (13, 15, KF_CRYS_STAR), (23, 15, KF_CRYS_BLADES),
        (6, 17, KF_CRYS_MONO), (30, 15, KF_CRYS_STAR),
        (9, 23, KF_CRYS_SHRUB_A), (21, 23, KF_CRYS_SHRUB_B),
        (28, 24, KF_CRYS_MONO), (26, 26, KF_CRYS_STAR), (23, 27, KF_CRYS_MONO),  # SE crystal-shrine cluster!
        (14, 29, KF_CRYS_SHRUB_B), (21, 30, KF_CRYS_BLADES),
    ):
        put_kf_sprite(tx, ty, *sp)
    # Dramatic twin giant crystal bursts choking the south road shut around (18, 33) (cleanly off x=18 path!)
    put_kf_sprite(15, 31, *KF_CRYS_STAR, force=True)
    put_kf_sprite(20, 31, *KF_CRYS_STAR, force=True)

    # South Glass-Choked Road barricade crystal clusters framing (18, 33)
    for nm, sx, sy in (('cr_purple_c', 16, 33), ('cr_teal_c', 17, 33),
                       ('cr_blue_c', 19, 33), ('cr_purple_c', 20, 33),
                       ('gd_shard0', 16, 28), ('gd_shard1', 20, 28)):
        if m.inb(sx, sy) and not m.taken[sy, sx] and not r.road_mask[sy, sx]:
            m.stamp(nm, sx, sy)

    # Warm braziers, lanterns, silk racks, glowing crystal obelisks & frosted reeds
    for nm, sx, sy in (
        ('gw_spool', 29, 20), ('gw_rack', 29, 22),
        ('fw_brazier', 17, 12), ('fw_brazier', 21, 12),
        ('fw_brazier', 23, 25),                                # warm brazier beside the SE crystal shrine!
        ('pf_lantern', 8, 12), ('pf_lantern', 30, 12),
        ('pf_lantern', 6, 15), ('pf_lantern', 16, 26), ('pf_lantern', 20, 26),
        ('cr_purple_t', 7, 21), ('cr_teal_t', 15, 20), ('cr_blue_t', 23, 20),
        ('cr_pink_t', 29, 21), ('gd_shard0', 11, 21), ('gd_shard1', 25, 20),
        ('fw_reeds0', 7, 25), ('fw_reeds1', 12, 28), ('fw_reeds0', 8, 28), ('fw_reeds1', 13, 25),
    ):
        s = STAMPS[nm]
        ok = True
        for dy in range(s['h']):
            for dx in range(s['w']):
                xx, yy = sx + dx, sy + dy
                if not m.inb(xx, yy) or m.taken[yy, xx] or m.cliff[yy, xx] or m.cls[yy, xx] in 'wWp' or r.road_mask[yy, xx]:
                    ok = False
        if ok:
            m.stamp(nm, sx, sy)

    # Seal EVERY remaining walkable rim pocket (ht == 1) with solid pines/crystals/stones so ZERO stranded rim tiles exist!
    for ty in range(0, H):
        for tx in range(0, W):
            if m.ht[ty, tx] != 1 or m.taken[ty, tx] or m.cliff[ty, tx]:
                continue
            if tx == 0 and ty in (0, 1, 2):
                continue
            # Even if L2 has a tree canopy overhang, put solid rock/crystal on L1 if L1 is empty so the cell is truly impassable
            if m.L[1, ty, tx] == 0:
                m.over.append((1, tx, ty, P1(rng.choice(['cr_purple_c', 'cr_teal_c', 'cr_blue_c', 'fw_stone']))))
                m.taken[ty, tx] = True

    # Hanging crystal-silk cocoons & glowing aura tucked naturally around the interior groves & Glass cocoons (27, 22)
    m.stamp('pf_glow', 26, 21)
    for gx, gy in ((6, 13), (31, 13), (13, 14), (24, 14), (6, 21), (26, 20), (28, 20), (14, 25), (24, 25)):
        if m.inb(gx, gy + 1) and not m.cliff[gy, gx]:
            m.over.append((2, gx, gy, 22751))
            m.over.append((2, gx, gy + 1, 22752))

    # Shimmering crystal-silk harp threads tracing north from Anchors 1-3 toward the Glass Ravine
    for ax, ay in ANCHORS:
        for ty in range(12, ay):
            if m.ht[ty, ax] == 0 and m.cls[ty, ax] in '.d' and not m.taken[ty, ax] and not m.cliff[ty, ax]:
                m.L[2, ty, ax] = 25824 + ((ax + ty) % 3)

    # Glass-sheen glints on the jagged frozen ravine surface
    for y in range(H):
        for x in range(W):
            if m.cls[y, x] in 'wW' and (x * 7 + y * 13) % 6 == 0 and x not in XING.values():
                m.L[2, y, x] = 25824 + ((x + y) % 3)

    # Ground micro-detailing: snowdrifts, ice cracks, frosted flora & subtle Bleed glints
    drifts = [P1('fw_drift0'), P1('fw_drift1'), P1('fw_drift2')]
    cracks = [P1('fw_crack0'), P1('fw_crack1'), P1('fw_crack2')]
    for y in range(4, H - 2):
        for x in range(5, W - 2):
            if m.ht[y, x] != 0 or m.taken[y, x] or m.cliff[y, x] or m.cls[y, x] in 'wWptT':
                continue
            if m.L[1, y, x] == 0 and m.L[2, y, x] == 0:
                rv = rng.random()
                if m.cls[y, x] == '.' and not r.road_mask[y, x] and rv < 0.04:
                    m.stamp(rng.choice(['cr_purple_c', 'cr_teal_c', 'cr_blue_c', 'gd_shard2']), x, y)
                elif m.cls[y, x] == '.' and rv < 0.13:
                    m.L[1, y, x] = rng.choice(drifts + [9725, 10620])
                elif lav_mask[y, x] and rv < 0.15:
                    m.L[1, y, x] = rng.choice(cracks)
                elif rv < 0.21:
                    m.L[2, y, x] = rng.choice([25824, 25825, 25826])

    # ---- 12. Commit stamps & draw the shimmering Bleed Veil down x = 4 ----
    m.put_stamps()
    veil_tiles = [26048, 26049, 26050]
    bleed_tiles = [25824, 25825, 25826]
    for y in range(14, 19):
        m.L[2, y, VX] = veil_tiles[y % 3]
        if m.L[2, y, VX + 1] == 0:
            m.L[2, y, VX + 1] = bleed_tiles[y % 3]

    # ---- 13. Events (100% contract-preserved; cancel=2 fix on D3 anchors; Juno cleanly west of Veil) ----
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
