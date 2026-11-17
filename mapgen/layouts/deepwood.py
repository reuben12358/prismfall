#!/usr/bin/env python3
"""Gossamer Deepwood (525, :SILKWOOD) and Cocoonfall Hollow (548, :BLEED).
525 (44 x 40): past the Cut tree.  Older, darker wood; the glass seeps in from the east.  Shelly's dew-pond clearing in the
south (small Veil, glassed Masquerain).  East: the crystal-silk mouth to the Hollow (opens once :ch2_tamsin is chosen).
548 (38 x 34): a crater of crystal trees strung with glass thread like a harp; the Glass Matriarch on her nest at the centre.
Entries: west from the Deepwood (DEEP_COCOON, through the Veil where Juno and Tamsin wait) and south from Route 3 (R3_COCOON).
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
    E.append({'type': 'event', 'name': 'Crystal silk', 'at': [41, 20], 'pages': [
        {'graphic': {'tile': CU['curtain'] + 8}, 'commands': [
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
    struggle = ("tm = GameData::Item.keys.find { |k| d = GameData::Item.get(k); d.is_TM? && d.move == :STRUGGLEBUG }\n"
                "tm ? pbReceiveItem(tm) : pbMessage(_INTL(\"You received a TM: Struggle Bug! [item data missing]\"))")
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
                {'script': 'setBattleRule("field", :BLEED)\nsetBattleRule("canLose")\nWildBattle.start(:MASQUERAIN, 14)'},
                "The Masquerain folds its glass wings and settles on the water. The ringing stops.", setk(525, 'MASQ'), {'selfswitch': ['A', True]}],
             'else': ["A glassed Masquerain hovers over the dew pond. It hasn't noticed you."]}]},
        {'cond': {'self': 'A'}, 'graphic': {'sprite': 'Followers/MASQUERAIN', 'dir': 'left'}, 'through': True,
         'commands': ["It rests on the water, calm."]}]})
    c.events = E
    head = {'id': 525, 'name': 'Gossamer Deepwood', 'bgm': 'Route 3', 'parent': 524, 'field': 'SILKWOOD', 'tone': [-40, -24, -30, 40],
            'metadata': {'ShowArea': True, 'MapPosition': [0, 13, 23], 'BattleBack': 'forest'}}
    return c.write('', head, "# Gossamer Deepwood (525) and Cocoonfall Hollow (548). WRITTEN BY layouts/deepwood.py - edit that, not this file.\n")


def hollow():
    W, H = 38, 34
    c = Wild(W, H, 548, base='a')
    cx, cy = 19, 15
    def hf(x, y):
        r = math.hypot((x - cx) / 15.5, (y - cy) / 13.0) + 0.12 * (vnoise(x, y, 4, 3.0) - 0.5)
        return 0 if r < 1.0 else 1
    c.set_heights(hf)
    for y in range(H):
        for x in range(W):
            if c.ht[y][x] == 1 and (y > 26 and 15 <= x <= 21): c.ht[y][x] = 0      # the south gap
            if c.ht[y][x] == 1 and (x < 5 and 14 <= y <= 18): c.ht[y][x] = 0       # the west gap (Veil)
    c.path([(0, 16), (6, 16), (12, 15), (cx, cy)], 2, 'D', 1, only='a')
    c.path([(18, 33), (18, 26), (cx, cy + 3)], 2, 'D', 2, only='a')
    c.cliffs(face=2)
    for y in range(H):
        for x in range(W):
            if c.g[y][x] == 'C': c.g[y][x] = 'B'
            elif c.ht[y][x] == 1 and c.g[y][x] in 'aD': c.g[y][x] = 'U'
    west, south = (0, 16), (18, 33)
    c.need(west, south, (cx, cy + 3))
    c.keep_clear([(0, 15), (0, 16), (0, 17), (18, 33), (17, 33), (19, 33)], 2)
    P = {'matriarch': [cx, cy], 'house': c.spot(8, 7, 'a', r=4), 'tm': c.spot(29, 6, 'a', r=4), 'cocoons': c.spot(27, 22, 'a'),
         'note': c.spot(cx + 2, cy + 2, 'aD')}
    P['juno'] = c.spot(2, 14, 'aD', r=2); P['tamsin'] = c.spot(2, 18, 'aD', r=2)
    for dy in range(-1, 3):                                     # the nest
        for dx in range(-2, 3):
            c.taken[cy + dy][cx + dx] = True
    c.seal()
    # the nest of glass silk; green light under the roots
    for dx, dy, t in ((-2, 0, CU['web_nw']), (2, 0, CU['web_ne']), (-2, 2, CU['web_sw']), (2, 2, CU['web_se'])):
        c.o[2][cy + dy][cx + dx] = t
    for dx in (-1, 0, 1):
        c.o[1][cy + 2][cx + dx] = 1338 + B if False else 8137
        c.o[1][cy - 1][cx + dx] = 8153
    c.o[1][cy + 1][cx - 1] = 8080; c.o[1][cy + 1][cx + 1] = 8081
    # crystal trees ringing the crater; glass thread strung between them like harp strings
    ring = []
    for k in range(18):
        a = k / 18.0 * 2 * math.pi
        x = int(round(cx + 11.5 * math.cos(a))) - 1; y = int(round(cy + 9.5 * math.sin(a))) - 2
        if c.obj('crystal_tree', x, y, on='a'): ring.append((x, y))
    for k in range(1, 9):
        y = cy - 8 + k * 2
        for x in range(cx - 10, cx + 11):
            if c.inb(x, y) and c.walkable(x, y) and not c.o[2][y][x] and (x + k) % 5 != 0:
                c.o[2][y][x] = CU['strand_h']
    c.trees(['cry_violet', 'cry_blue', 'cry_teal', 'r_cry_big', 'r_cry_spray', 'cry_violet_m', 'cry_blue_m'], 14, on='a', seed=2)
    c.trees(['cocoon', 'cocoon_big', 'cocoon_low', 'cocoon', 'cocoon_big'], 34, on='a', seed=3)
    c.trees(['cry_violet_s', 'cry_blue_s', 'cry_teal_s', 'r_cry_s', 'r_cry_s2'], 24, on='a', seed=5)
    c.overlay('web_big', cx - 1, cy - 2)
    for x, y in ((8, 9), (27, 8), (9, 21), (26, 22), (14, 4)):
        c.overlay('web_big', x, y)
    c.trees(['dead1', 'dead2', 'log_grey', 'stump_grey', 'gstump_dark'], 6, on='a', seed=4, bleed=True)
    c.scatter([([8136, 8137, 8144, 8145, 8152], 0.55, 2.4, 0.8)], [(8139, 3), (8146, 3), (8154, 2)], density=0.10, on='aD', seed=7)
    c.scatter([([1164, 1172], 0.6, 3.0, 0.6)], [(1164, 4), (1189, 2)], density=0.15, on='a', bleed=True, seed=8)
    for x in range(2, 7):
        for y in range(13, 20):
            if x == 4: c.o[2][y][x] = c.o[2][y][x] or CU['veil']
    E = []
    E.append({'type': 'warp', 'name': 'To Route 3', 'at': [18, 33], 'link': 'R3_COCOON', 'arrive': [18, 32, 'up']})
    E.append({'type': 'warp', 'name': 'To the Deepwood', 'at': [0, 16], 'link': 'DEEP_COCOON', 'arrive': [1, 16, 'right']})
    E.append(c.fog_event('prismfall_glass', 90, 1, 200, 1, 1))
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
             say('TAMSIN', 'neutral', "The next Warden's Dorian Pell, in Saltmere. He'll call you \"darling\" and mean it about a third of the time."),
             say('TAMSIN', 'happy', "Come back, will you? I'd like to show you the room when it isn't tangled."),
             say('JUNO', 'happy', "I've got to take the eggs to Uncle Rowan. Then Saltmere! There's a PAGEANT! Don't see it without me!"),
             {'script': "%w[Juno Tamsin].each do |n|\n  ev = $game_map.events.values.find { |e| e.name == n }\n  ev.erase if ev\nend"}]
    for i, y in enumerate((14, 15, 16, 17, 18)):
        if c.walkable(4, y):
            E.append({'type': 'event', 'name': 'Veil %d' % (i + 1), 'at': [4, y], 'pages': [
                {'cond': {'switch': 'CH2_MATRIARCH_DONE'}, 'trigger': 'touch', 'through': True, 'commands': once(548, 'OUTRO', outro)}]})
    boss = [
        "(At the center, a Galvantula the size of a cart, half crystal, sits on a nest of glass silk wound around something that glows faintly green beneath the roots.)",
        "It turns eight eyes on you. Four of them are glass.",
        {'boss': {'id': 'GLASS_MATRIARCH', 'species': 'GALVANTULA', 'level': 16, 'field': 'BLEED'}},
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
        {'switch': ['CH2_MATRIARCH_DONE', True]}, {'switch': ['GLOAMING_DISGUISED_CELESTINE', True]}, {'var': ['BRIARWICK_GLASSWOOD', 1]},
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
    c.events = E
    head = {'id': 548, 'name': 'Cocoonfall Hollow', 'palette': 'bleed', 'bgm': 'Route 3', 'parent': 540, 'field': 'BLEED', 'tone': [-46, -50, 4, 90],
            'metadata': {'ShowArea': True, 'MapPosition': [0, 11, 22], 'BattleBack': 'forest'}}
    return c.write('', head, '')


if __name__ == '__main__':
    save('525_deepwood_cocoonfall.yaml', deepwood(), hollow())
