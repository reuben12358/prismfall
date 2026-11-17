#!/usr/bin/env python3
"""The Glassed Orchard (522, :BLEED): the Pruetts' orchard, turned to glass in one winter night.  44 x 40.
Entry from Route 2 on the west edge (0, 36-38).  The Bleed Veil is the shimmer line across the gate (x 4).  Orchard
terraces rise to the east; the Pruett house stands glassed at the top.  Everything here is the Bleed copy of the
Tectonic art (tileset 40, id + B): glass-blue foliage, ash-lilac ground, mauve-grey wood, a still gall-pink pond.
Run:  python3 -I layouts/orchard.py && python3 -I build.py 522"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wildkit import Wild, save, say, trainer, once, vnoise, B, OBJ, CU

W, H = 44, 40
VX = 4                                     # the Veil column


def key(k): return "$game_self_switches[[522, 0, '%s']]" % k
def setk(k): return {'script': key(k) + ' = true'}
def show_larch():
    return {'script': "ev = $game_map.events.values.find { |e| e.name == 'Professor Larch' }\n"
                      "$game_self_switches[[522, ev.id, 'A']] = true if ev\n$game_map.need_refresh = true"}


def build():
    c = Wild(W, H, 522, base='a')
    c.forest_glyph = 'U'
    c.stair_kind = 'stairs_stone@40'      # worn stone: wood would read wrong in the glass
    def hf(x, y):
        if x > 30 + 2 * math.sin(y / 4.0) and y < 18 + 2 * (vnoise(x, y, 3, 4.0) - 0.5): return 2
        if x > 14 + 3 * math.sin(y / 5.0) + 2 * (vnoise(x, y, 5, 4.0) - 0.5) and y < 31 + 2 * math.sin(x / 6.0): return 1
        return 0
    c.set_heights(hf)
    c.notch(18, 20, 30, 1, depth=6); c.notch(33, 35, 17, 2, depth=5)
    # the still pond: gall-pink water, a fallen glass branch across it
    c.pond(9, 21, 4.0, 3.0, 4, c='w', only='a')
    c.path([(0, 37), (3, 37), (8, 36), (14, 34), (19, 35), (19, 31)], 2, 'D', 1, only='a')
    c.path([(19, 26), (24, 22), (31, 21), (34, 19)], 2, 'D', 2, only='a')
    c.path([(34, 14), (34, 9), (30, 6)], 2, 'D', 3, only='a')
    c.path([(24, 22), (24, 12), (19, 8)], 2, 'D', 4, only='a')                           # orchard alley north
    c.path([(8, 36), (6, 30), (8, 26)], 2, 'D', 5, only='a')                              # pond walk
    c.stairs(18, 30); c.stairs(33, 17)
    c.cliffs(face=2, keep='w')
    for y in range(H):
        for x in range(W):
            if c.g[y][x] == 'C': c.g[y][x] = 'B'
    # border: glassed wood, thick on the north and east, a broken hedge line in the south
    for y in range(H):
        for x in range(W):
            if c.g[y][x] != 'a': continue
            if y < 2 + 3 * vnoise(x, 1, 21, 5.0) or x > W - 3 - 3 * vnoise(1, y, 22, 5.0) or y > H - 2 - 2 * vnoise(x, 2, 23, 4.0) \
               or (x < 2 + 2 * vnoise(3, y, 24, 4.0) and not 34 <= y <= 39):
                c.g[y][x] = 'U'
    # darker ash under the trees of each orchard row
    for y in range(H):
        for x in range(W):
            pass
    gate = (0, 37)
    c.need(gate, (30, 7), (11, 13), (38, 24))
    c.keep_clear([(0, 36), (0, 37), (0, 38), (2, 37), (VX, 37)], 2)
    P = {'juno': [2, 35], 'larch': [2, 39 - 1], 'farmhand': c.spot(27, 13, 'aA'), 'apple': c.spot(38, 24, 'aA'),
         'wurmple': c.spot(24, 18, 'D'), 'carbink': c.spot(40, 6, 'aA', r=4), 'biscuit': c.spot(11, 13, 'aA', r=4),
         'house_sign': c.spot(30, 8, 'aA')}
    for k in ('juno', 'larch'):
        c.taken[P[k][1]][P[k][0]] = True
    c.seal()
    # ---- the Pruett house, glassed whole, at the top of the orchard
    c.land('st:t_house_red', 28, 2, on='aA', bleed=True, r=3)
    c.land('st:t_bench', 36, 9, on='aA', bleed=True)
    # ---- the orchard: rows of glass apple trees on each terrace, gaps where trees have shattered
    placed = 0
    for row, y0 in enumerate(range(4, 34, 5)):
        for x0 in range(5 + (row % 2) * 2, 40, 4):
            k = (x0 * 13 + y0 * 7) % 9
            if k == 0:                                     # a shattered tree: stump or fallen trunk in the row
                c.obj('stump_grey' if row % 2 else 'fallen', x0, y0 + 1, on='aA', bleed=True); continue
            if c.obj('crystal_tree' if k > 2 else 't_round', x0, y0, on='aA', bleed=k <= 2):
                placed += 1
                for dx, dy in ((-1, 3), (2, 3), (0, 3), (1, 3)):          # fallen glass apples under the canopy
                    xx, yy = x0 + dx, y0 + dy
                    if c.inb(xx, yy) and c.g[yy][xx] in 'aA' and not c.o[1][yy][xx] and not c.taken[yy][xx] and (xx + yy) % 2:
                        c.o[1][yy][xx] = [8136, 8144, 8137, 8152][(xx * 3 + yy) % 4]
    print('  orchard trees in rows:', placed)
    # ---- crystal growth and dead trees; glass-thread webs strung between the rows
    c.trees(['cry_violet', 'cry_blue', 'cry_teal', 'cry_violet_m', 'cry_blue_m', 'r_cry_spray', 'r_cry_big'], 16, on='aA', seed=2)
    c.trees(['cry_violet_s', 'cry_blue_s', 'cry_teal_s', 'r_cry_s', 'r_cry_s2'], 26, on='aA', seed=3)
    c.trees(['dead1', 'dead2', 'dead3', 'dead4', 'log_big', 'roots', 'creep1'], 12, on='aA', seed=4, bleed=True)
    for nm, x, y in (('gstump_dark', 6, 4), ('crag_bare', 37, 31), ('boulder2', 14, 4), ('corpse', 40, 15)):
        c.land(nm, x, y, on='aA', bleed=True)
    # the gateposts at the Veil: two stone pillars, a broken arch of glass thread above
    c.obj('pillar_moss', VX, 33, on='aA', bleed=True, force=True); c.obj('pillar_moss2', VX, 38, on='aA', bleed=True, force=True)
    for i, (x, y) in enumerate(((22, 15), (27, 10), (31, 26), (12, 30), (38, 19), (17, 6))):
        c.overlay(['web_nw', 'web_ne', 'web_sw', 'web_se'][i % 4] if False else 'web_s', x, y, bleed=False)
    for x, y in ((21, 16), (22, 16), (26, 11), (27, 11), (30, 27), (31, 27), (37, 20), (38, 20)):
        if not c.o[2][y][x]: c.o[2][y][x] = CU['strand_h']
    # ---- ground: glass apples (crystal shards) in drifts, ash tufts, a few pale flowers that are wrong
    c.scatter([([8136, 8137, 8138, 8144, 8145, 8152, 8153], 0.66, 2.6, 0.75)], [(8139, 3), (8140, 3), (8146, 2), (8154, 2)], density=0.05, on='aA', seed=7)
    c.scatter([([947, 939, 955], 0.60, 3.0, 0.7), ([1024, 1035], 0.82, 2.0, 0.6)], [(1164, 10), (1172, 5), (1180, 2), (1189, 2)],
              density=0.22, on='aA', bleed=True, seed=8)
    c.edge_decor([8136, 8144, 8152, 8137], 0.25, on='aA', by='w', seed=2)
    c.water_decor(0.10, c='w')
    c.path_decor([8136, 8144], 0.04, on='D')
    # ---- the Veil: a shimmer line across the gate (events) and light-bending sparkles overhead
    for y in range(31, 40):
        if c.g[y][VX] in 'aAD' or y in (35, 36, 37, 38): c.o[2][y][VX] = CU['veil']
    for y in range(33, 40):
        for x in (VX - 1, VX + 1):
            if (x + y) % 3 == 0 and not c.o[2][y][x]: c.o[2][y][x] = CU['veil']
    # ---- events (story/20_SCRIPT_CH0-2.md, "Map 522")
    E = []
    E.append({'type': 'warp', 'name': 'To Route 2', 'at': [0, 37], 'link': 'R2_ORCHARD', 'arrive': [1, 37, 'right']})
    E.append({'type': 'warp', 'name': 'To Route 2 b', 'at': [0, 36], 'to': {'map': 521, 'x': 60, 'y': 22, 'dir': 'left'}})
    E.append({'type': 'warp', 'name': 'To Route 2 c', 'at': [0, 38], 'to': {'map': 521, 'x': 60, 'y': 23, 'dir': 'left'}})
    E.append(c.fog_event('prismfall_glass', 70, 1, 200, 2, 1))
    intro = [
        "(Rows of apple trees turned to clear glass. Glass apples chime in the wind. The air at the gate shimmers like heat.)",
        say('JUNO', 'sad', "There. That was the Pruetts'. It went last winter, in one night."),
        say('JUNO', 'neutral', "It's pretty, isn't it? I hate that it's pretty."),
        {'se': 'Voltorb Flip tile'}, "(A squeak from inside. A Skwovet is clinging to a glass branch.)",
        say('JUNO', 'panic', "Biscuit! Biscuit, come OUT!"),
        {'move': {'who': 'Juno', 'route': ['right', 'wait 4']}},
        "\\pf[JUNO,panic,shock]Juno: Ow— no. No. My skin's burning. I can't.",
        {'move': {'who': 'Juno', 'route': ['left']}},
        say('JUNO', 'sad', "That's the Veil. Nobody can cross one. You just... can't. Your body won't."),
        "(You step forward.)",
        {'move': {'who': -1, 'route': ['right', 'right', 'right']}}, {'wait': 40},
        "\\pf[JUNO,shocked,shock]Juno: ...How are you DOING that?",
        {'choices': ["I don't know.", "It doesn't hurt.", "..."], 'cancel': 3, 'branches': [[], [], []]},
        say('JUNO', 'shocked', "Doesn't it— aren't you— your HAIR isn't even standing up!"),
        setk('VEIL'), {'selfswitch': ['A', True]}]
    E.append({'type': 'event', 'name': 'Orchard arrival', 'at': [1, 39 - 1], 'pages': [
        {'cond': {'switch': 'CH1_K1_DONE'}, 'trigger': 'autorun', 'commands': intro}, {'cond': {'self': 'A'}}]})
    lecture = [
        show_larch(), {'wait': 20},
        "(Professor Larch is standing next to Juno with a notebook. She has clearly run the whole way.)",
        say('LARCH', 'neutral', "So. You walked through a Bleed Veil."),
        say('LARCH', 'neutral', "Into a Bleed zone. On your first day. To fetch a Skwovet."),
        {'choices': ["It was stuck."], 'cancel': 1, 'branches': [[]]},
        "\\pf[LARCH,angry,anger]Larch: IT LIVES IN A TREE. IT IS ALWAYS STUCK. THAT IS ITS ENTIRE ARRANGEMENT WITH TREES.",
        say('JUNO', 'happy', "Technically Skwovet are scansorial, so—"),
        say('LARCH', 'angry', "Juno."),
        "\\pf[JUNO,panic,sweat]Juno: Shutting up!",
        say('LARCH', 'crying', "Your mother wrote me one instruction. One! \"Keep them out of trouble, Imelda.\" It has been NINE HOURS."),
        say('LARCH', 'crying', "I'm not crying. It's the tea. The tea is very strong."),
        {'wait': 30}, "(Larch looks at the sleeping swarm in the glass trees, then at you.)",
        say('LARCH', 'neutral', "...They calmed down. When you went near them."),
        say('LARCH', 'neutral', "Well. That's that, then."),
        "(Larch writes something in the notebook.)",
        say('LARCH', 'neutral', "Listen to me, both of you. Never take a tinted person past a Veil. Never. It isn't pain that stops them. It's the body knowing."),
        say('LARCH', 'neutral', "And you. This is Lecture One. I'm numbering them. I have a feeling."),
        {'if': 'GameData::Item.exists?(:FIELDNOTES)', 'then': [{'script': 'pbReceiveItem(:FIELDNOTES)'}],
         'else': ["\\me[Key item get]You received the FIELD NOTES!\\nProfessor Larch's field encyclopedia. It fills in as you meet new fields."]},
        {'switch': ['CH1_ORCHARD_DONE', True]}, {'script': 'pf_bond_add(:JUNO, 1)'},
        "QUEST: \"Biscuit\" - bring Biscuit home to Wenna at Hale's Bramble."]
    for i, y in enumerate(range(35, 39)):
        if c.g[y][VX] not in 'aAD' or c.o[1][y][VX]: continue
        E.append({'type': 'event', 'name': 'Bleed Veil %d' % (i + 1), 'at': [VX, y], 'pages': [
            {'cond': {'switch': 'CH1_K1_DONE'}, 'trigger': 'touch', 'through': True, 'commands': [
                {'if': key('BISCUIT') + ' && ' + key('SWARM') + ' && !$game_switches[105]', 'then': lecture,
                 'else': [{'if': key('VEIL') + ' && !' + key('VEILMSG'), 'then': ["(The shimmer slides over you like warm water. Nothing else happens.)", setk('VEILMSG')], 'else': []}]}]},
            {'cond': {'switch': 'CH1_ORCHARD_DONE'}, 'through': True}]})
    E.append({'type': 'event', 'name': 'Juno', 'at': P['juno'], 'pages': [
        {'cond': {'switch': 'CH1_K1_DONE'}, 'graphic': {'sprite': 'trainer_RIVAL2', 'dir': 'right'}, 'commands': [
            {'if': key('VEIL') + ' && $game_player.x >= %d' % VX, 'then': [
                say('JUNO', 'neutral', "Can you pull me through? Just for a second? I only want to grab him."),
                {'choices': ["No. Stay there.", "Take her hand."], 'cancel': 1, 'branches': [
                    [say('JUNO', 'sad', "...Right. Yes. The Professor did say never. Sorry. Go on, I'll shout directions.")],
                    [{'script': 'Prismfall.checkpoint(false)'}, say('JUNO', 'happy', "On three. One, two—"),
                     {'se': 'Ice 1'}, "(Glass rings. Juno goes clear from the fingertips up.)", {'wait': 60},
                     say('JUNO', 'shocked', "\\PN, I can't feel my—"), {'script': 'Prismfall.game_over(:GO_ORCHARD)'}]]}],
             'else': [say('JUNO', 'sad', "Biscuit's in there somewhere. Past the farmhand. Please be careful.")]}]},
        {'cond': {'switch': 'CH1_ORCHARD_DONE'}, 'graphic': {'sprite': 'trainer_RIVAL2', 'dir': 'right'},
         'commands': [say('JUNO', 'happy', "You walked through the Bleed like it was fog. Nobody does that. NOBODY.")]}]})
    E.append({'type': 'event', 'name': 'Professor Larch', 'at': P['larch'], 'pages': [
        {'cond': {'switch': 'CH1_K1_DONE'}, 'commands': []},
        {'cond': {'self': 'A'}, 'graphic': {'sprite': 'trainer_PROFESSOR', 'dir': 'right'}, 'commands': [say('LARCH', 'neutral', "Lecture One stands. Out. Now. Home.")]},
        {'cond': {'switch': 'CH1_ORCHARD_DONE'}, 'graphic': {'sprite': 'trainer_PROFESSOR', 'dir': 'right'},
         'commands': [say('LARCH', 'neutral', "Field safety, rule one, underlined three times. I'll be at the station writing it four times.")]}]})
    E.append({'type': 'event', 'name': 'Glass farmhand', 'at': P['farmhand'], 'pages': [
        {'graphic': {'sprite': 'NPC 03', 'dir': 'down'}, 'move': 'fixed', 'commands': [
            "A man made of glass, mid-step, a glass basket on his arm. His mouth is open. He was calling someone.", {'selfswitch': ['A', True]}]},
        {'cond': {'self': 'A'}, 'graphic': {'sprite': 'NPC 03', 'dir': 'down'}, 'move': 'fixed', 'commands': [
            "Inside the glass, very faintly, his eyes are moving."]}]})
    E.append({'type': 'event', 'name': 'Glass apple', 'at': P['apple'], 'pages': [
        {'graphic': {'sprite': 'Object ball', 'dir': 'down'}, 'commands': [
            {'if': 'GameData::Item.exists?(:GLASSAPPLE)', 'then': [{'script': 'pbReceiveItem(:GLASSAPPLE)'}],
             'else': ["You found a GLASS APPLE.\\nIt rings when you flick it. Don't bite it.", {'script': '$player.money += 500'},
                      "(You sell it to yourself for ₽500. [item data missing: GLASSAPPLE])"]},
            {'selfswitch': ['A', True]}]}, {'cond': {'self': 'A'}}]})
    E.append({'type': 'event', 'name': 'Glassed Wurmple', 'at': P['wurmple'], 'pages': [
        {'cond': {'switch': 'CH1_K1_DONE'}, 'graphic': {'sprite': 'Followers/WURMPLE', 'dir': 'down'}, 'move': 'fixed', 'commands': [
            "It hisses. Its body grinds like a jar of marbles.",
            {'script': 'setBattleRule("field", :BLEED)\nsetBattleRule("canLose")\nWildBattle.start(:WURMPLE, 6)'},
            "FIELD NOTES: THE BLEED - unstable. Borrows effects from other fields. Do not trust the ground.",
            "The Wurmple stops grinding. It looks at you. Then it curls up against your shoe and goes to sleep.",
            "The rest of the swarm settles in the branches, one by one.", setk('SWARM'), {'selfswitch': ['A', True]}]},
        {'cond': {'self': 'A'}, 'graphic': {'sprite': 'Followers/WURMPLE', 'dir': 'down'}, 'move': 'fixed', 'through': True,
         'commands': ["It's asleep. Its crystal hums, very quietly, in time with your breathing."]}]})
    E.append({'type': 'event', 'name': 'Wild Carbink', 'at': P['carbink'], 'pages': [
        {'graphic': {'sprite': 'Followers/CARBINK', 'dir': 'left'}, 'commands': [
            "It is licking a glass tree. It seems very happy about the whole situation.",
            {'script': 'setBattleRule("field", :BLEED)\nWildBattle.start(:CARBINK, 8)'}, {'selfswitch': ['A', True]}]},
        {'cond': {'self': 'A'}}]})
    E.append({'type': 'event', 'name': 'Lost Skwovet', 'at': P['biscuit'], 'pages': [
        {'cond': {'switch': 'CH1_K1_DONE'}, 'graphic': {'sprite': 'Followers/SKWOVET', 'dir': 'down'}, 'move': 'random', 'commands': [
            "Biscuit has stuffed his cheeks with glass apple seeds. He rattles when he moves.",
            "He climbs onto your head. This is apparently how this works.", setk('BISCUIT'), {'selfswitch': ['A', True]}]},
        {'cond': {'self': 'A'}}]})
    E.append({'type': 'sign', 'at': P['house_sign'], 'post': False, 'name': 'Pruett house',
              'text': "The Pruett house. The door is glass, and so is the key in it. A child's coat hangs on the peg inside, perfectly clear."})
    c.events = E
    head = {'id': 522, 'biome': 'bleed', 'name': 'The Glassed Orchard', 'palette': 'bleed', 'bgm': 'Route 2', 'parent': 521, 'field': 'BLEED', 'tone': [-18, -22, 26, 70],
            'metadata': {'ShowArea': True, 'MapPosition': [0, 15, 22], 'BattleBack': 'field'}}
    return c.write('522_glassed_orchard.yaml', head, "# The Glassed Orchard (522). WRITTEN BY layouts/orchard.py - edit that, not this file.\n")


if __name__ == '__main__':
    save('522_glassed_orchard.yaml', build())
