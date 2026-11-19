#!/usr/bin/env python3
"""Gossamer Wood (524, :SILKWOOD): the Crown's old-growth wood between Windfall Row and Briarwick, hung with silver silk.  50 x 58.
South gate x 22-24 (from Windfall Row, warp R2_WOOD).  North gate x 24-26 on the root terrace (Briarwick, WOOD_BRIAR).
The direct climb north is walled by silk at the top of the east stairs, so the trail loops west past the dew pond.
East: the Woodward's hut (526), then a Cut tree and the Bleed Veil before the Deepwood (525, WOOD_DEEP).
Run:  python3 -I layouts/gossamer.py && python3 -I build.py 524"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wildkit import Wild, save, say, trainer, once, vnoise, MUSH, CU, B

W, H = 50, 58


def hut(c, x, y):
    """The Woodward's cabin (Tectonic 6840 block, 6x6): roof rows overhead and solid, walls solid, door cells left open."""
    for dy in range(6):
        for dx in range(6):
            if dx == 4 and dy >= 4: continue
            t = 6840 + dy * 8 + dx; z = 2 if dy < 4 else 1
            c.o[z][y + dy][x + dx] = t; c.taken[y + dy][x + dx] = True; c.sol[y + dy][x + dx] = True
            if c.g[y + dy][x + dx] in '.T': c.g[y + dy][x + dx] = '#'
    for dy in (4, 5):
        c.taken[y + dy][x + 4] = True; c.sol[y + dy][x + 4] = True
    return (x + 4, y + 5)


def giant(c, x, y, dark=True):
    """A giant hollow tree: the 3x4 great stump with a crown of canopy around and above it, silk in its arms."""
    for yy in range(y, y + 4):
        for xx in range(x - 1, x + 4):
            if c.inb(xx, yy) and c.g[yy][xx] == 'T': c.g[yy][xx] = '.'
    if not c.obj('gstump_dark' if dark else 'gstump', x, y):
        print('  giant tree failed at', x, y); return False
    for dx, dy, n in ((-1, 1, 'web_nw'), (3, 1, 'web_ne')):
        xx, yy = x + dx, y + dy
        if c.inb(xx, yy) and not c.o[2][yy][xx]: c.o[2][yy][xx] = CU[n]
    return True


def build():
    c = Wild(W, H, 524)
    # ---- heights: the root terrace (1) across the north, a root knoll (1) in the south-east
    def hf(x, y):
        edge = 20 + 2.5 * math.sin(x / 5.5) + 2 * (vnoise(x, y, 4, 4.0) - 0.5)
        if x > 34: edge -= min(6, (x - 34) * 1.5)
        return 1 if y < edge else 0
    c.set_heights(hf)
    c.notch(11, 13, 21, 1, depth=5); c.notch(26, 28, 21, 1, depth=5)
    # ---- water: a brook from the terrace falls past the dew pond and out to the south-east
    c.stream([(4, 26), (8, 30), (15, 40), (24, 44), (33, 50), (40, 57)], 2, 3)
    c.pond(7, 31, 4.0, 3.0, 5)
    # ---- the trail
    water = {(x, y) for y in range(H) for x in range(W) if c.g[y][x] == '~'}
    c.path([(23, 57), (23, 51), (19, 46), (16, 40), (19, 34), (25, 30)], 2, 'd', 1, only='.~')
    c.path([(25, 30), (27.5, 27), (27.5, 25)], 2, 'd', 2, only='.')                         # to the east stairs (silk wall above)
    c.path([(27.5, 20), (27.5, 15), (25, 9), (25, 0)], 2, 'd', 3, only='.')                 # terrace trail north
    c.path([(25, 30), (17, 28), (12.5, 26), (12.5, 25)], 2, 'd', 4, only='.~')              # the loop: west past the pond
    c.path([(12.5, 20), (12, 15), (17, 11), (24, 10)], 2, 'd', 5, only='.')
    c.path([(25, 30), (33, 29), (40, 28), (49, 27)], 2, 'd', 6, only='.')                   # east trail: hut, Cut tree, Veil
    c.path([(33, 29), (38, 35), (40, 40)], 2, 'd', 7, only='.')                             # spur to the knoll
    c.path([(27.5, 15), (36, 13), (42, 9)], 2, 'd', 8, only='.')                            # terrace spur, east lookout
    for y in range(H):
        for x in range(W):
            if c.g[y][x] == 'd' and c.ht[y][x] < 0: c.g[y][x] = '='
    for (x, y) in water:
        if c.g[y][x] == 'd': c.g[y][x] = '='
    c.stairs(11, 21); c.stairs(26, 21)
    c.cliffs(face=2, keep='~=')
    # ---- the old-growth: deep forest everywhere off the trail, clearings cut where the story happens
    for y in range(H):
        for x in range(W):
            if c.g[y][x] == '.': c.g[y][x] = 'T'
    for i, (cx, cy, rx, ry) in enumerate(((25, 31, 6.5, 4.5), (17, 41, 4, 3.5), (9, 30, 6, 5), (14, 14, 5, 4), (25, 11, 5, 4), (38, 29, 6, 4.5),
                                          (40, 42, 5, 4), (44, 27, 5, 6.5), (23, 52, 4, 4), (40, 12, 5, 3.5), (30, 5, 4, 3), (32, 37, 3, 3))):
        c.blob(cx, cy, rx, ry, '.', 40 + i, only='T', rough=0.7)
    for yy in (25, 26, 28, 29):
        if c.g[yy][45] in '.d': c.g[yy][45] = 'T'
    gate_s, gate_n, gate_e = (23, 57), (25, 0), (49, 27)
    c.need(gate_s, gate_n, gate_e)
    c.keep_clear([(22, 57), (23, 57), (24, 57), (25, 0), (24, 0), (26, 0), (49, 27), (48, 27)], 2)
    P = {'tobin': c.spot(21, 47, 'd.'), 'reed': c.spot(31, 30, 'd.'), 'petra': c.spot(26, 14, 'd.'), 'bram': c.spot(13, 18, 'd.'),
         'twins': c.spot(20, 31, '.'), 'picker': c.spot(14, 32, '.'), 'weaver': c.spot(27, 33, '.'), 'kestrel': c.spot(25, 4, 'd.'),
         'shrine': c.spot(14, 12, '.'), 'potion': c.spot(42, 44, '.'), 'repel': c.spot(8, 27, '.', r=2), 'tm': c.spot(43, 10, '.'),
         'ether': c.spot(33, 36, '.'), 'netball': c.spot(36, 5, '.', r=6), 'silksign': [27, 25]}
    c.taken[25][27] = True
    c.seal()
    # ---- the silk wall across the top of the east stairs: curtains, webs and a cocoon
    for x in range(25, 31):
        if c.g[19][x] in 'd.' and not c.o[1][19][x]:
            c.obj('curtain', x, 18, on='d.', force=True); c.o[2][17][x] = c.o[2][17][x] or CU['strand_h']
    # ---- landmarks
    hd = hut(c, 38, 20)                                       # the Woodward's hut, door south onto the east trail
    giant(c, 19, 23); giant(c, 41, 38, dark=False); giant(c, 7, 11); giant(c, 31, 2, dark=False)
    c.land('tablet', 13, 10); c.land('pillar_moss', 11, 11); c.land('stump_moss', 16, 12)       # the shrine stone
    c.land('log_big', 25, 35); c.land('log_moss2', 29, 34)                                          # the weaver's resting log
    c.land('pf_fairy_38', 38, 11, r=3)                                    # the felled great tree (lookout)
    c.land('boulder_dark', 31, 6); c.land('crag', 36, 40)
    # glass creeping in from the Veil: crystal trunks beyond the shimmer
    for nm, x, y in (('crystal_tree', 46, 22), ('crystal_tree', 46, 29), ('cry_violet', 44, 24), ('cry_teal_s', 45, 31), ('cry_blue_s', 47, 25)):
        c.land(nm, x, y, r=2)
    for y in range(23, 32):
        c.o[2][y][47] = c.o[2][y][47] or CU['veil']
    # ---- under the canopy: cocoons, webs between trunks, ferns, mushrooms, logs; light shafts in the clearings
    c.trees(['cocoon', 'cocoon', 'cocoon_low', 'silk_tree'], 16, seed=1)
    c.trees(['fern_big', 'log', 'log_moss', 'stump_moss', 'roots', 'rafflesia', 'log_big', 'creep1'], 22, seed=2)
    c.trees(['t_dark', 't_leafy', 't_round', 'r_tree_d', 'r_tree_d2', 'r_pine_d', 'smalltree', 'pine_s2'], 30, seed=3)
    c.trees(['bushtree', 'sapling', 'pine_s'], 12, seed=4)
    for i, (x, y) in enumerate(((23, 29), (8, 27), (36, 26), (14, 39), (24, 8), (38, 40), (41, 10), (22, 50))):
        c.overlay('shaft', x, y)
    import random
    r = random.Random(524)
    for y in range(1, H - 1):                                  # silk between trunks: strands over the trail edges, web fans in corners
        for x in range(1, W - 1):
            if c.o[2][y][x] or not c.walkable(x, y): continue
            l, rr = c.g[y][x - 1] == 'T', c.g[y][x + 1] == 'T'
            u, d = c.g[y - 1][x] == 'T', c.g[y + 1][x] == 'T'
            if (l and u or rr and u) and r.random() < 0.22:
                c.o[2][y][x] = CU['web_nw' if l else 'web_ne']
            elif l and rr and r.random() < 0.35:
                c.o[2][y][x] = CU['strand_h']
    c.overhang(0.28, seed=3)
    for x, y in ((16, 21), (31, 30), (9, 36), (36, 11), (21, 46), (42, 33), (4, 20), (29, 52), (15, 6)):
        c.overlay('web_big', x, y)
    c.scatter([([1172, 1164, 1180, 1189], 0.55, 3.0, 0.8), (MUSH[4:], 0.78, 2.4, 0.7), ([1048, 1057, 1056], 0.74, 2.6, 0.75)],
              [(1164, 10), (1172, 6), (1180, 3), (1189, 3), (1263, 1), (1148, 1)], density=0.36, seed=6)
    c.edge_decor([1263, 1148, 1158, 1150, 1180], 0.22, by='T', seed=1)
    c.edge_decor([950, 958, 1180], 0.35, by='~', seed=2)
    c.water_decor(0.18)
    c.grassfill([(16, 44, 3, 2), (31, 31, 2.5, 2), (9, 15, 3, 2.5), (39, 13, 3, 2), (41, 43, 2.5, 2)], only='.')
    # ---- events (story/20_SCRIPT_CH0-2.md, "Map 524")
    E = []
    E.append({'type': 'warp', 'name': 'To Windfall Row', 'at': [23, 57], 'link': 'R2_WOOD', 'arrive': [23, 56, 'up']})
    E.append({'type': 'warp', 'name': 'To Windfall Row b', 'at': [22, 57], 'to': {'map': 521, 'x': 1, 'y': 9, 'dir': 'left'}})
    E.append({'type': 'warp', 'name': 'To Windfall Row c', 'at': [24, 57], 'to': {'map': 521, 'x': 1, 'y': 11, 'dir': 'left'}})
    E.append({'type': 'warp', 'name': 'To Briarwick', 'at': [25, 0], 'link': 'WOOD_BRIAR', 'arrive': [25, 1, 'down']})
    E.append({'type': 'cut_tree', 'at': [45, 27]})
    E.append({'type': 'warp', 'name': 'To Deepwood', 'at': [49, 27], 'link': 'WOOD_DEEP', 'arrive': [48, 27, 'left']})
    E.append({'type': 'door', 'name': "Woodward's Hut door", 'at': list(hd), 'link': 'WOOD_HUT', 'gfx': ['doors1', 0, 2]})
    E.append({'type': 'sign', 'at': P['silksign'], 'post': False, 'name': 'Silk wall', 'text': "Thick silk blocks the trail. Maybe there's a way around."})
    E.append(c.fog_event('prismfall_spores', 55, 0, 200, 1, 1))
    entry = [say('JUNO', 'happy', "Silk-moths! The Insect Plate's somewhere under Briarwick, and it makes the silk never tangle. Ever! You could knot it for a week!"),
             "FIELD NOTES: SILKWOOD - Bug moves bite deeper. Webs slow the careless. Fire here is rude and effective."]
    for i, x in enumerate((22, 23, 24)):
        E.append({'type': 'event', 'name': 'Wood entry %d' % (i + 1), 'at': [x, 54], 'pages': [
            {'cond': {'switch': 'CH1_ORCHARD_DONE'}, 'trigger': 'touch', 'commands': once(524, 'ENTRY', entry)}]})
    for i, y in enumerate((26, 27, 28)):
        if c.walkable(43, y):
            E.append({'type': 'event', 'name': 'Juno at the Veil %d' % (i + 1), 'at': [43, y], 'pages': [
                {'cond': {'switch': 'CH1_ORCHARD_DONE'}, 'trigger': 'touch', 'commands': once(524, 'GLASS', [
                    "(A shimmer hangs between two trees. Beyond it, the trunks are clear crystal.)",
                    say('JUNO', 'sad', "That's the Glasswood. It was three fields away at midwinter.")])}]})
    E.append({'type': 'npc', 'name': 'Silk-picker', 'at': P['picker'], 'sprite': 'NPC 11', 'dir': 'up', 'move': 'random',
              'text': "Silk-picker: Don't cut the low strands, they're this year's. Cut the high ones. No, higher. No— you know what, I'll do it."})
    E.append({'type': 'npc', 'name': 'Old Weaver', 'at': P['weaver'], 'sprite': 'NPC 13', 'dir': 'down',
              'text': "Old Weaver: Sixty years I've walked this wood. This spring it rings. Hear it? East. Like someone tapping a glass."})
    E.append({'type': 'sign', 'at': P['shrine'], 'post': False, 'name': 'Shrine stone',
              'text': "A small mossy shrine stone. A carving of three beasts chasing a masked figure. Someone has left a honey bun in front of the masked one, not the three."})
    E.append({'type': 'npc', 'name': 'Kestrel', 'at': P['kestrel'], 'sprite': 'trainer_RIVAL1', 'dir': 'down',
              'text': "Kestrel: Briarwick's just ahead. Try not to get lost in the webs. ...Not that I'd come looking."})
    E.append(trainer(P['twins'], 'TWINS', 'Mo & Jo', 'trainer_YOUNGSTER', 'right', 3, "We battle together!", "We lose together.",
                     rules=['setBattleRule("double")']))
    E.append(trainer(P['tobin'], 'BUGCATCHER', 'Tobin', 'trainer_BUGCATCHER', 'right', 3, "My bugs love the silk here!", "The webs move at night. I swear it."))
    E.append(trainer(P['reed'], 'BUGCATCHER', 'Reed', 'trainer_BUGCATCHER', 'left', 3, "You walked right into my web!", "Tamsin catches bugs bigger than me."))
    E.append(trainer(P['petra'], 'AROMALADY', 'Petra', 'trainer_AROMALADY', 'down', 3, "Smell that? Night-blooming gossamer.", "It's lovely here. Mostly."))
    E.append(trainer(P['bram'], 'CAMPER', 'Bram', 'trainer_CAMPER', 'down', 4, "Camping in Gossamer? Battle first, questions later!", "Watch for the silk walls."))
    E.append({'type': 'item', 'at': P['potion'], 'item': 'POTION'})
    E.append({'type': 'item', 'at': P['repel'], 'item': 'REPEL'})
    E.append({'type': 'item', 'at': P['tm'], 'item': 'TM19'})
    E.append({'type': 'item', 'at': P['ether'], 'item': 'ETHER'})
    E.append({'type': 'event', 'name': 'HiddenItem', 'at': P['netball'], 'pages': [
        {'commands': [{'if': 'pbItemBall(:NETBALL, 2)', 'then': ["The web gave them up without a fight.", {'selfswitch': ['A', True]}], 'else': []}]},
        {'cond': {'self': 'A'}}]})
    c.overlay('web_s', P['netball'][0], P['netball'][1] - 1)
    c.events = E
    head = {'id': 524, 'biome': 'forest', 'name': 'Gossamer Wood', 'bgm': 'Route 3', 'parent': 0, 'field': 'SILKWOOD', 'tone': [-28, -8, -30, 25],
            'metadata': {'ShowArea': True, 'MapPosition': [0, 13, 23], 'BattleBack': 'forest'}}
    return c.write('524_gossamer_wood.yaml', head, "# Gossamer Wood (524). WRITTEN BY layouts/gossamer.py - edit that, not this file.\n")


if __name__ == '__main__':
    raise SystemExit('superseded by layouts/reskin.py (MAPGEN 2h): running this would overwrite the PF Rejuv spec')
if False:
    save('524_gossamer_wood.yaml', build())
