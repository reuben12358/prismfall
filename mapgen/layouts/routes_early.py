#!/usr/bin/env python3
"""routes_early.py - the Chapter 1-4 road legs at ROUTES.yaml's sizes (map builder 9), on routekit:
  Road 1 the Strand Road: 520 The Ferrymen's Mile (64x110), 521 Windfall Row (120x70), 527 Lacecliff Walk (140x64),
         528 Marram Down (110x80)
  Road 2 the Weavers' Road: 541 The Grey Saltings (70x110), 552 The Dyers' Ford (80x72), 540 Thistledown Lea
         (130x64), 524 Gossamer Wood (90x110)
  Road 3 the Hoar Road: 566 Spinners' Rise (80x120), 577 Frostwick Pass (72x96), 578 Rimewood Path (80x88)
Each leg: a landmark, a side path that pays, a secret, the script's events (story/20_SCRIPT_CH0-2.md, 21_SCRIPT_CH3.md),
the Trial events of design/TRIAL_EVENTS.yaml, and the connections of design/SWAP_GYM1_GYM2.md 1A.
Run: python3 -I layouts/routes_early.py [ids] [--preview]  then  python3 -I build.py --strict"""
import os, sys, re, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, yaml
import rkit as K
from rkit import C, STAMPS
import routekit as RK
import rimewood as RW
from routekit import Route, trainer, npc, sign, item, hidden, talk, head
import story_early as SE
HERE = K.HERE
P = SE.P
PREV = '--preview' in sys.argv
os.makedirs('/tmp/rt', exist_ok=True)


def once(name, at, cmds, trigger='touch', sprite=None):
    """a touch (or action) event that runs once (self switch A)"""
    pg = {'trigger': trigger, 'commands': list(cmds) + [{'selfswitch': ['A', True]}]}
    if sprite: pg['graphic'] = {'sprite': sprite, 'dir': 'down'}
    return {'type': 'event', 'name': name, 'at': list(at), 'pages': [pg, {'cond': {'self': 'A'}, 'commands': []}]}


def obj(name, at, lines, trigger='action'):
    return {'type': 'event', 'name': name, 'at': list(at), 'pages': [{'trigger': trigger, 'commands': list(lines)}]}


def trial(name, at, key, sprite=None, cond=None, d='down'):
    pg = {'trigger': 'action', 'commands': [{'script': 'pf_trial_talk(:%s)' % key}]}
    if sprite: pg['graphic'] = {'sprite': sprite, 'dir': d}
    if cond: pg['cond'] = cond
    return {'type': 'event', 'name': name, 'at': list(at), 'pages': [pg]}


def flowers(r, cx, cy, rx, ry, tiles=None, p=0.55):
    """a drift of flowers (sea-pinks, meadow bands) laid over open grass after painting"""
    m = r.m; tiles = tiles or K.DECOR_SH['flowers']
    for y in range(int(cy - ry), int(cy + ry) + 1):
        for x in range(int(cx - rx), int(cx + rx) + 1):
            if m.inb(x, y) and ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1 and m.cls[y, x] in '.t' and not m.taken[y, x] \
                    and m.L[1, y, x] == 0 and m.L[2, y, x] == 0 and r.rng.random() < p:
                m.L[1, y, x] = r.rng.choice(tiles)


def water_stamp(r, n, x, y):
    """a stamp standing in water (sea stacks, rocks, boats): only where every cell is water and free"""
    m = r.m; L = np.array(STAMPS[n]['layers']); hh, ww = L.shape[1:]
    if all(m.inb(x + i, y + j) and m.cls[y + j, x + i] in 'wW' for i in range(ww) for j in range(hh)):
        for j in range(hh):
            for i in range(ww):
                t = int(L[:, j, i].max())
                if t: m.L[2, y + j, x + i] = t
        return True
    return False


# ====================================================================================================== 527 Lacecliff Walk
def build_527():
    """Lacecliff Walk (140x64, BEACH): the cliff-top path runs west from the Hale Bell through three sea-cut chalk arches;
    two stairs down to coves (shingle, rock pools, a beached rowboat); the Wrecker's Lamp; a Wingull stack; the gorse
    heath with its hidden field of sea-pinks; the Lacemakers' Bench; the smugglers' pole; the Lost Thread cove (secret)"""
    W, H = 140, 64
    r = Route(527, W, H, 'coast', kit={1: 'ak', 'default': 'ak'}, base='.')
    m = r.m
    r.sea('S', 13, wobble=3.0, beach=7, deep=5, cliff=1, scale=16.0)
    r.forest_band('N', 6, wobble=4.0)
    for cx, cy, rx, ry in ((8, 30, 6, 3), (30, 32, 5, 2.5), (58, 34, 4, 2), (84, 32, 6, 3), (128, 33, 7, 3), (112, 12, 5, 3), (44, 10, 7, 3), (92, 8, 6, 3)):
        r.copse(cx, cy, rx, ry)
    # the coves: the beach bites into the cliff where the stairs come down
    for cx, cy, rx, ry in ((40, 44, 9, 5), (98, 45, 10, 4)):
        for y in range(H):
            for x in range(W):
                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1.0 and m.ht[y, x] == 1: m.ht[y, x] = 0; m.cls[y, x] = 's'
    road = [(139, 24), (126, 22), (112, 26), (100, 24), (88, 19), (74, 21), (62, 27), (50, 25), (38, 21), (24, 18), (12, 21), (0, 20)]
    r.road(road, w=3.0, open_=None)
    r.exit('E', 22, 4); r.exit('W', 18, 4)
    # cliff-top heath north of the path, gorse banks and copses; the side path up to the Wrecker's Lamp
    r.clearing(118, 8, 10, 5); r.lane([(110, 24), (114, 15), (118, 9)], w=2.0)
    r.clearing(70, 9, 12, 5); r.clearing(22, 8, 9, 4)
    r.lane([(60, 26), (64, 16), (70, 10)], w=2.0)
    # stairs down to the coves (flatten the lip there)
    for x, yl in ((39, 37), (97, 38)):
        r.flatten(x, x + 2, yl, 1); r.crossing(x, yl, w=3, rows=3)
        r.lane([(x + 1, 28), (x + 1, yl)], w=2.0, open_=(1, 2))
    # rock pools on the coves' sand; a beached rowboat
    for cx, cy in ((34, 46), (46, 45), (92, 47), (104, 46)):
        r.water(cx, cy, 2.2, 1.2, rough=0.5)
    # the Lost Thread cove (secret): a beach pocket west of the second cove, behind a tide-rock that only moves at night
    for y in range(H):
        for x in range(W):
            if ((x - 72) / 6) ** 2 + ((y - 45) / 3) ** 2 <= 1.0 and m.ht[y, x] == 1: m.ht[y, x] = 0; m.cls[y, x] = 's'
    r.grass(thr=0.6, scale=6.0)
    r.finish_plan()
    # ---- landmark: the three Lace Arches straddle the path
    arches = []
    for ax in (100, 75, 50):
        ys = [y for y in range(H) if m.cls[y, ax + 3] == 'd']
        ay = (min(ys) + max(ys)) // 2 - 2 if ys else 20
        for yy in range(ay + 3, ay + 5):
            for xx in range(ax + 2, ax + 5): m.cls[yy, xx] = 'd'
        r.stamp('pf_chalkarch', ax, ay, mark='B'); arches.append((ax + 3, ay + 4))
    # ---- events
    J = lambda e, t: P('JUNO', e, t)
    r.add(sign((136, 21), 'Road sign', "LACECLIFF WALK - The Strand Road. -> The Ferrymen's Mile - <- Marram Down & Saltmere.\nThe arches are older than the Accord. Please do not improve them."),
          once('The Lace Arches', arches[0], ['(Chalk cliffs worn by the sea into arches as fine as lace. The path goes through three of them.)',
               J('happy', 'The Briarwick weavers copy these cliffs for their lace. Not the other way round. The sea did it first.'),
               J('happy', "The sea does most things first. It's very annoying of it.")]),
          trainer((104, 46), 'FISHERMAN', 'Bryn', "The strait's closed and the fish haven't been told.", 'The fish win again.', d='left'),
          trainer((40, 47), 'PICNICKER', 'Moll', "I found a bottle with a letter in it! It's from my sister. She lives forty yards that way.",
                  "She writes every week. She's never once walked over.", d='right'),
          trainer((86, 16), 'HIKER', 'Dunstan', "Cliff path in a gale's a fine way to die. Cliff path in sun's a fine way to live.", "Today's a sun day. Lucky you.", d='down'),
          talk('Painter at an easel', (58, 22), 'NPC 18', ["Painter: Hold still. No -- you're in the light. No -- you ARE the light.",
               "Painter: Hm. You don't really show up on the canvas, do you? Odd."]),
          talk('Hermit at the Wrecker\'s Lamp', (118, 8), 'NPC 26', ["Hermit: It's for the gulls. The lamp. Not for ships.",
               "Hermit: I don't know anything about ships. Who said ships?"]),
          obj("Wrecker's Lamp", (120, 6), ["A lamp on a tall pole, trimmed and full. It faces the sea, where the rocks are."]),
          talk('Birder', (24, 10), 'NPC 09', ['Birder: Wingull nest on that stack. Two hundred of them. I\'ve named eleven. The rest won\'t hold still.']),
          obj("Smugglers' signal pole", (70, 8), ["A tall pole with a lantern hook. From here you can see the Ferrow lighthouse.",
               "Its beam sweeps past, then stops on you for a second longer than it should, then moves on."]),
          obj('Road Stone I-b', (128, 21), ['ROAD STONE I-b. THE STRAND ROAD. "Ferrow 2, Saltmere 6." Someone has chalked a seventh mile on, for the arches.']),
          {'type': 'event', 'name': "Lacemakers' Bench", 'at': [62, 23], 'pages': [{'trigger': 'action', 'commands': [
              J('happy', "Sit! You have to sit! It's the Lacemakers' Bench. Everyone who walks the Strand sits here or the cliffs fall in."),
              {'choices': ['Is that true?', '(Sit.)'], 'cancel': 1, 'branches': [
                  [J('deadpan', "No. But they haven't fallen in, have they.")],
                  ['(You sit. Juno sits. A Wingull lands on the end of the bench. Nobody says anything for a while. The sea does most of the talking.)',
                   J('neutral', "...This is nice. I don't get to sit. I'm always going somewhere with a basket."),
                   J('happy', "Right! That's enough nice! Saltmere!"), {'heal': True}]]}]}]},
          hidden((50, 24), 'PEARL', 'HiddenItem (third arch)'),
          item((119, 11), 'POTION'), item((20, 9), 'POKEBALL'), item((96, 49), 'SUPERPOTION'),
          trial('Dobbs the shell-gatherer', (43, 41), 'DOBBS', 'NPC 27', d='down'),
          {'type': 'event', 'name': 'Tide-rock', 'at': [65, 45], 'pages': [
              {'graphic': {'sprite': 'Object rock', 'dir': 'down'}, 'trigger': 'action', 'commands': [
                  {'if': 'PBDayNight.isNight?', 'then': ['The tide is out. The rock stands in a dry hollow now, and you can squeeze past it.', {'selfswitch': ['A', True]}],
                   'else': ['The sea fills the gap behind this rock. At low tide, maybe.']}]},
              {'cond': {'self': 'A'}, 'commands': []}]},
          obj('Drowned sample-book', (74, 45), ['A weaver\'s sample-book, swollen with seawater. Every page is a lace pattern copied from these cliffs.',
              'On the last page, in a different hand: "Found the Thread. Going home by the forest road." It is dated the winter the road closed.']),
          hidden((76, 46), 'SHELLBELL', 'HiddenItem (the Lost Thread)'))
    r.seat_events(on='.dts')
    lipkeep = np.zeros((H, W), bool)
    for y in range(H - 1):
        for x in range(W):
            if m.ht[y, x] == 1 and m.ht[min(H - 1, y + 1), x] == 0: lipkeep[max(0, y - 2):y + 1, x] = True
    was = m.taken.copy(); m.taken |= lipkeep
    for _ in range(70):                                                    # gorse bushes on the heath
        x, y = r.rng.randrange(W - 2), r.rng.randrange(8, 40)
        if m.free(x, y, 2, 2, on='.'): m.stamp('ak_fern', x, y)
    r.dress(trees=('tr_pine', 'tr_pine2', 'tr_oak2'), n_trees=W * H // 200, copses=6, scatter=12, greenfill=None)
    m.taken = was | (m.taken & ~lipkeep)
    for n, x, y in (('ak_rock2', 12, 45), ('hb_plank', 56, 47), ('hb_rope', 31, 44), ('hb_buoy', 88, 48), ('ak_rock2', 118, 46),
                    ('hb_boxes', 70, 44), ('hb_plank', 126, 47), ('hb_barrel', 108, 44), ('ak_rock2', 136, 45), ('hb_post1', 50, 43)):
        r.near(n, x, y, on='s', r=4)
    r.paint(glint=0.25)
    flowers(r, 70, 9, 10, 4); flowers(r, 22, 9, 7, 3); flowers(r, 118, 9, 8, 4, p=0.3)
    for x, y in ((20, 55), (60, 56), (120, 54), (84, 58), (8, 52), (132, 57)): water_stamp(r, 'ak_rock2', x, y)
    water_stamp(r, 'ak_boulder', 26, 51)
    for x, y in ((48, 47), (100, 50)): water_stamp(r, 'hb_boat3', x, y)
    h = head(527, 'Lacecliff Walk', field='BEACH', bgm='Route 3', weather=None,
             connections=[{'dir': 'W', 'offset': 18, 'to': 528, 'to_offset': 30}, {'dir': 'E', 'offset': 22, 'to': 520, 'to_offset': 72}],
             tone=[6, 4, -6, 0])
    r.write(h, '527_lacecliff_walk.yaml', '# Lacecliff Walk (527). WRITTEN BY layouts/routes_early.py - edit that script.\n',
            '/tmp/rt/527.png' if PREV else None)


# ====================================================================================================== 528 Marram Down
def ship_part(r, dx, dy, max_row, on='su.'):
    """part of the moored two-master's hull (rows up to max_row of its art) laid on sand: a wreck half-buried in a dune"""
    m = r.m
    for x, y, z, t in K.SHIP:
        if y > max_row: continue
        X, Y = x + dx, y + dy
        if m.inb(X, Y) and m.cls[Y, X] in on:
            m.L[1 if z == 0 else 2, Y, X] = t
            if z == 0: m.taken[Y, X] = True; m.cls[Y, X] = 'B'


def build_528():
    """Marram Down (110x80, BEACH): dune-down held by marram grass; the Saltmere Beacon on the highest dune (heals once,
    the first view of the port); the players' camp of wagons; the theatre barge half-buried in the sand (the Prompter's
    Box); the bird-hide over a brackish pool; the stile and the Free Port charter stone at the East Gate"""
    W, H = 110, 80
    r = Route(528, W, H, 'dunes', kit={1: 'ak', 'default': 'ak'}, base='.')
    m = r.m
    r.sea('S', 11, wobble=3.5, beach=5, deep=4, scale=14.0)
    r.forest_band('N', 5, wobble=3.0)
    for cx, cy, rx, ry in ((14, 12, 8, 4), (90, 10, 7, 3), (102, 52, 5, 4), (6, 58, 5, 4)):
        r.copse(cx, cy, rx, ry)
    # dunes: sandy ground (RJ Dirt) in long drifts, marram tall grass in their hollows
    for cx, cy, rx, ry in ((30, 50, 22, 9), (72, 54, 24, 8), (50, 28, 14, 7), (88, 36, 12, 6), (14, 36, 10, 6), (60, 66, 40, 4)):
        m.blob(cx, cy, rx, ry, 'u', seed=int(cx * 7 + cy), rough=0.7, only='.')
    # the Beacon dune (raised) with stairs on its south face
    m.blob(54, 15, 10, 6, None, ht=1, seed=31, rough=0.35)
    r.flatten(52, 54, 20, 1); r.crossing(52, 20, w=3, rows=3)
    road = [(109, 31), (96, 30), (84, 36), (68, 34), (54, 37), (38, 35), (22, 40), (0, 39)]
    r.road(road, w=3.0, open_=None)
    r.exit('E', 30, 4); r.exit('W', 38, 4)
    r.lane([(53, 34), (53, 24)], w=2.0, open_=None)                                  # up to the Beacon
    r.lane([(84, 34), (90, 24), (92, 20)], w=2.0, open_=None)                        # side path to the bird hide
    r.water(95, 16, 5, 3)                                                            # the brackish pool
    r.lane([(30, 38), (28, 50), (30, 57)], w=2.0, open_=None)                        # down to the barge
    r.lane([(76, 37), (78, 46)], w=2.0, open_=None)                                  # into the players' camp
    m.blob(79, 49, 7, 4, 'd', seed=44, rough=0.4, only='.ut')
    r.grass(thr=0.63, scale=5.0)
    r.finish_plan()
    # ---- the camp, the barge, the hide, the beacon
    for n, x, y in (('pf_stall4', 74, 46), ('pf_stall2', 82, 45), ('pf_stall0', 85, 50), ('sh_campfire', 77, 50), ('hb_washline', 72, 50),
                    ('hb_tables', 80, 52), ('hb_barrels', 87, 47), ('pf_morris', 71, 47)):
        r.near(n, x, y, on='d.u', r=3)
    r.stamp('gl_shed', 55, 10, mark='B')                                             # the beacon keeper's hut
    r.near('fw_brazier', 50, 12, on='.', r=3)
    r.near('gl_shed', 99, 12, on='.', r=4)                                           # the bird hide
    J = lambda e, t: P('JUNO', e, t)
    r.add(sign((105, 29), 'Road sign', 'MARRAM DOWN - Free Port of Saltmere, 1 mile. Pulling up the marram grass is fined. Yes, even that one.'),
          obj('Free Port charter stone', (4, 37), ['FREE PORT CHARTER STONE: "By grant of Sovereign Maren, AF 41: SALTMERE ANSWERS TO THE ACCORD AND TO NO CROWN."',
              'Someone has carved underneath, smaller: "AND BOOS THE REST."']),
          once('The Saltmere Beacon', (53, 14), ['(From the top of the dune, the free port opens below: a white town on a salt lake, striped awnings, lantern masts, and a theater on every second corner.)',
               J('happy', "Saltmere! Look at it! Everything's ordinary! Isn't it WONDERFUL?"),
               J('happy', "The Blank Plate's under there somewhere. Nothing strange ever happens in Saltmere. No Bleed, no glowing rivers, nothing."),
               J('happy', 'So they make it all up instead. Every night. On purpose.')]),
          {'type': 'event', 'name': 'Beacon Keeper', 'at': [56, 13], 'pages': [
              {'graphic': {'sprite': 'NPC 26', 'dir': 'down'}, 'trigger': 'action', 'commands': [
                  "Beacon Keeper: Tea? It's not kelp. I've heard about the kelp.", {'heal': True}, '(The party is rested.)', {'selfswitch': ['A', True]}]},
              {'cond': {'self': 'A'}, 'graphic': {'sprite': 'NPC 26', 'dir': 'down'}, 'trigger': 'action', 'commands': [
                  'Beacon Keeper: The pot\'s cold. Come back when I\'ve forgotten you.']}]},
          talk('Hound Number One', (76, 48), 'NPC 03', ['Hound Number One: And SO the Loyal Three drove the Gossamer Ogre from the wood--']),
          talk('Ogre', (79, 47), 'NPC 25', ["Ogre: (muffled) Can I take the mask off? It's very hot in the Ogre.", 'Ogre: (muffled) Why does he look so sad, though? He\'s the villain.'], move='random'),
          talk('Director with script', (82, 48), 'NPC 18', ['Director: The Ogre does NOT take the mask off. The Ogre has never taken the mask off. It\'s in the text.',
               'Director: Because the carver was having a bad week in AF 140! Places!']),
          trainer((80, 44), 'JUGGLER', 'Hounds', 'A rehearsal audience! Quick, a scene!', 'Notes: we were bitten. Again.', d='down', double=True),
          talk('Prop-mistress', (73, 49), 'NPC 27', ["Prop-mistress: If you're digging in the old barge, there's a shovel by the wagon.",
               "Prop-mistress: The prompter's box went down with it in '71. Nobody's had the heart.",
               {'if': '!pfm_has?(:SANDSHOVEL)', 'then': [{'script': 'pfm_item(:SANDSHOVEL, 1, "Sand Shovel")'}]}]),
          {'type': 'event', 'name': "The Prompter's Box", 'at': [33, 57], 'pages': [{'trigger': 'action', 'commands': [
              {'if': 'pfm?(:sm_prompter)', 'then': ['Only sand now. The barge has given up its secret.'],
               'else': [{'if': 'pfm_has?(:SANDSHOVEL)', 'then': [
                   '(A theater barge lies half-buried in the dune, its name board reading THE WANDERING CHORUS.)', 'You dig at the stern with the shovel...',
                   {'script': 'pfm_item(:PROMPTERSSCRIPT, 1, "Prompter\'s Script")'}, {'script': 'pfm_item(:NORMALGEM, 1, "Normal Gem")'},
                   {'script': 'pfm_set(:sm_prompter)'}],
                   'else': ['(A theater barge lies half-buried in the dune. Costume hampers. A prop throne with three legs.)',
                            'Something square is buried at the stern. You\'d need a shovel.']}]}]}]},
          trainer((88, 33), 'BIRDKEEPER', 'Lark', "Wind off the lake's the best in Elowen.", 'My kite won. You beat the kite-flier, which is different.', d='left'),
          trainer((14, 37), 'POKEMONRANGER_F', 'Sedge', "Free port starts at the stile. Past that, the Queen's writ doesn't run, and neither do I.",
                  "I'm going to sit down now. That's allowed in a free port.", d='right'),
          talk('Sand-sculptor', (40, 44), 'NPC 15', ["Sand-sculptor: It's the Sovereign's Crown! In sand!", "Sand-sculptor: ...Don't look at the stone. I ran out of the good sand."]),
          talk('Birdwatcher', (97, 21), 'NPC 09', ['Birdwatcher: Brackish pool. Half sea, half rain. The Wingull come to wash the salt off. Shh.']),
          hidden((62, 64), 'SOFTSAND', 'HiddenItem (sledge run)'), obj('Sledge run', (58, 24), ['THE SLEDGE RUN. Down the Beacon to the shore in nine seconds. The record is seven, and a broken arm.']),
          item((8, 64), 'POTION'), item((100, 20), 'GREATBALL'), item((24, 26), 'REPEL'))
    r.seat_events(on='.dtus')
    r.dress(trees=('tr_pine', 'tr_pine2', 'tr_oak2'), n_trees=W * H // 260, copses=4, scatter=10)
    for _ in range(40):
        x, y = r.rng.randrange(W - 2), r.rng.randrange(6, 66)
        if m.free(x, y, 2, 2, on='.u'): m.stamp('ak_fern', x, y)
    ship_part(r, -6, 4, 53)                                                         # the Wandering Chorus, half-buried
    r.paint(glint=0.3)
    flowers(r, 20, 22, 8, 4, p=0.3)
    for x, y in ((14, 74), (44, 76), (86, 73), (100, 76)): water_stamp(r, 'ak_rock2', x, y)
    h = head(528, 'Marram Down', field='BEACH', bgm='Route 3',
             connections=[{'dir': 'E', 'offset': 30, 'to': 527, 'to_offset': 18}, {'dir': 'W', 'offset': 38, 'to': 140, 'to_offset': 44}],
             tone=[8, 4, -8, 0])
    r.write(h, '528_marram_down.yaml', '# Marram Down (528). WRITTEN BY layouts/routes_early.py - edit that script.\n', '/tmp/rt/528.png' if PREV else None)


# ====================================================================================================== 520 The Ferrymen's Mile
def old_events(fn, mid):
    out = {}
    p = os.path.join(HERE, 'layouts', 'old_' + fn)
    if not os.path.exists(p):                                         # first run: keep the old spec as the events' source
        os.rename(os.path.join(HERE, 'specs', fn), p)
    for d in yaml.safe_load_all(open(p)):
        if d and d['id'] == mid:
            for e in d.get('events', []):
                out[e.get('name') or (e.get('trainer') and e['trainer'][1]) or (e.get('text') or '')[:20] or '%s@%s' % (e['type'], e['at'])] = e
    return out


def at(e, x, y):
    e = dict(e); e['at'] = [x, y]; return e


def line_events(r, base, y, x0, x1, pages):
    """a touch line across the road at row y (every road cell from x0 to x1)"""
    out = []
    xs = [x for x in range(x0, x1 + 1) if r.m.cls[y, x] in 'dg']
    for i, x in enumerate(xs):
        out.append({'type': 'event', 'name': '%s %d' % (base, i + 1), 'at': [x, y], 'pages': pages})
        r.m.taken[y, x] = True
    return out


def barrier_tile():
    return int(np.array(STAMPS['pf_barricade']['layers']).max())


SENDOFF_520 = [P('LARCH', 'neutral', "Eighteen gyms. Saltmere's first. The forest road to Briarwick's corded off -- the Glasswood's walked across it -- so you go round by the coast.", '', 'Professor Larch'),
               P('LARCH', 'neutral', 'Two days on foot. Chalk cliffs, then dunes, then the free port. The Warden\'s Dorian Pell. He\'ll call you "darling" and mean it about a third of the time.', '', 'Professor Larch'),
               P('LARCH', 'neutral', "Write to me. I mean it. Gale Post, every town. If I don't hear from you in a week I start Lecture Two by post.", '', 'Professor Larch'),
               P('JUNO', 'happy', "I'm coming as far as Saltmere! Mum's promised forty tarts to the Pageant crowd and I'm the cart!"),
               P('JUNO', 'happy', "And I've wanted to see the Pageant since I was six. There's a bit where the Plates fall and they use REAL glitter."),
               P('LARCH', 'deadpan', 'They use salt.', '', 'Professor Larch'), P('JUNO', 'shocked', '...Why would you tell me that.', 'shock'),
               {'script': 'pfm_item(:TOWNMAP, 1, "Town Map")'}, '(Larch has drawn a skull on the Glassed Orchard, a skull on the forest road, and a smaller skull on her own kettle.)',
               {'script': 'pfm_quest(:eighteen_roads, "Eighteen Roads", "Earn the first badge in Saltmere, west along the coast.")'},
               {'script': '$game_variables[102] = 2 if $game_variables[102] < 2'}, {'script': 'pfm_set(:ch2_sendoff)'},
               {'script': "ev = $game_map.events.values.find { |e| e.name == 'Professor Larch' }\n$game_self_switches[[520, ev.id, 'A']] = true if ev\n$game_map.need_refresh = true"}]


def build_520():
    """The Ferrymen's Mile (64x110, MEADOW): the lane north from Ferrow's Landing over the stile; the sea-cliff walk on the
    south-west with Wingull posts and the Gullwatch lookout over the moored Dovetail; the old ferry-toll booth; the Hale
    Bell at the fork where the Strand Road turns west (the quarantine roadblock, from Windfall Row); Hale's Bramble, six
    berry terraces and a picking shed; the Minding Hedges; Juno's catching clearing; the sheepfold; Road Stone I; the
    Smuggler's Stair (secret, Cut) down to the Ferryman's Rest cove"""
    W, H = 64, 110
    r = Route(520, W, H, 'coast', kit={1: 'ak', 2: 'sh3', 3: 'sh3', 'default': 'sh3'}, base='.')
    m = r.m
    # the sea on the south-west, under the cliff-walk; woods on the east and north
    m.ht[:, :] = 1                                                                   # the whole down is cliff-top (h1)
    for y in range(80, H):                                                           # the sea under the cliff-walk, south-west
        d = 7 + int(3 * (RK.vnoise(0, y, 520, 9.0) - 0.5) * 2) + max(0, (y - 96) // 3)
        for x in range(0, d + 3):
            m.cls[y, x] = ('W' if x < d - 4 else 'w') if x < d else 's'; m.ht[y, x] = 0
    r.forest_band('E', 9, wobble=4.0); r.forest_band('N', 4, wobble=2.0)
    for cx, cy, rx, ry in ((52, 30, 6, 5), (8, 14, 6, 5), (46, 92, 7, 6), (54, 70, 5, 6), (10, 46, 5, 4)):
        r.copse(cx, cy, rx, ry)
    # Hale's Bramble: berry terraces climbing east of the lane (h1-h3), each with a stair
    for (x0, x1, y0, y1, h) in ((36, 58, 36, 58, 2), (40, 58, 36, 51, 3), (44, 58, 36, 45, 4)):
        m.ht[y0:y1 + 1, x0:x1 + 1] = np.maximum(m.ht[y0:y1 + 1, x0:x1 + 1], h)
    road = [(16, 109), (16, 101), (19, 93), (24, 85), (22, 77), (22, 72), (27, 62), (31, 52), (28, 41), (33, 29), (31, 16), (31, 0)]
    r.road(road, w=3.0, open_=None)
    r.road([(22, 74), (12, 73), (0, 73)], w=3.0, open_=None)                        # the Hale Bell fork: west to Lacecliff Walk
    r.exit('S', 15, 4); r.exit('N', 30, 4); r.exit('W', 72, 4)
    for (sx, yl) in ((38, 58), (42, 51), (46, 45)):                                  # terrace stairs
        r.crossing(sx, yl, w=2, rows=3)
    r.lane([(32, 56), (38, 61)], w=2.0, open_=None)
    # Minding Hedges (NW), Juno's clearing (S), the sheepfold (NE), the lookout path to the cliff edge
    r.lane([(22, 84), (14, 84), (10, 86)], w=2.0, open_=None)
    r.lane([(26, 60), (16, 62)], w=2.0, open_=None)
    r.lane([(32, 24), (44, 22), (48, 18)], w=2.0, open_=None)
    # the Smuggler's Stair: a pocket on the beach below the toll booth's cliff, behind a bramble (Cut)
    m.ht[93:101, 0:12] = 0; m.cls[93:101, 0:12] = np.where(np.isin(m.cls[93:101, 0:12], ['w', 'W']), m.cls[93:101, 0:12], 's')
    r.flatten(12, 14, 92, 1); r.crossing(12, 92, w=3, rows=3)
    r.grass(thr=0.6, scale=6.0)
    r.finish_plan()
    m.cls[86:92, 12:15] = np.where(m.cls[86:92, 12:15] == 'T', '.', m.cls[86:92, 12:15])
    ev = old_events('520_reskin.yaml', 520)
    J = lambda e, t: P('JUNO', e, t)
    tut = [{'cond': {'switch': 'CH1_K1_DONE'}, 'trigger': 'touch', 'commands': [{'if': "$game_self_switches[[520, 0, 'TUT']]", 'then': [], 'else': [
        J('happy', "Catching tutorial! Weaken it, then throw. Don't throw the Ball AT it, throw it NEAR it."),
        J('happy', 'I learned that the hard way. Sorry, Biscuit.'), {'script': 'pbReceiveItem(:POKEBALL, 5)'},
        {'script': "$game_self_switches[[520, 0, 'TUT']] = true"}]}]}]
    send = [{'commands': []}, {'cond': {'var': ['STORY_CHAPTER', 2]}, 'trigger': 'touch', 'commands': [{'if': 'pfm?(:ch2_sendoff)', 'then': [], 'else': SENDOFF_520}]}]
    r.events += line_events(r, 'Juno tutorial', 90, 10, 30, tut)
    r.events += line_events(r, 'Stile send-off', 98, 8, 24, send)
    B = barrier_tile()
    bar = lambda i, y: {'type': 'event', 'name': 'Accord barrier %d' % i, 'at': [3, y], 'pages': [
        {'graphic': {'tile': B}, 'trigger': 'action', 'commands': ['Accord Guard: Hold. Quarantine order: nobody leaves the Landing without papers.']},
        {'cond': {'switch': 'CH1_ORCHARD_DONE'}, 'through': True, 'commands': []}]}
    for i, y in enumerate((72, 73, 74, 75)): r.events.append(bar(i + 1, y)); m.taken[y, 3] = True
    r.add(at(ev['Professor Larch'], 18, 99) if False else {'type': 'event', 'name': 'Professor Larch', 'at': [19, 97], 'pages': [
              {'commands': []}, {'cond': {'var': ['STORY_CHAPTER', 2]}, 'graphic': {'sprite': 'trainer_PROFESSOR', 'dir': 'down'}, 'commands': [
                  {'if': 'pfm?(:ch2_sendoff)', 'then': [P('LARCH', 'neutral', 'Off you go. Lecture Two is already drafted.')], 'else': SENDOFF_520}]},
              {'cond': {'self': 'A'}, 'commands': []}]},
          {'type': 'event', 'name': 'Accord guard', 'at': [5, 71], 'pages': [
              {'graphic': {'sprite': 'NPC 07', 'dir': 'down'}, 'commands': ['Accord Guard: Hold. Quarantine order: nobody leaves the Landing without papers.']},
              {'cond': {'switch': 'CH1_ORCHARD_DONE'}, 'graphic': {'sprite': 'NPC 07', 'dir': 'right'}, 'commands': [
                  'Accord Guard: Hold. Quarantine order: nobody leaves the Landing without papers.',
                  "Accord Guard: ...You've got a Badge Case. A challenger. Right. Challengers pass, that's older law than the quarantine.",
                  'Accord Guard: "Eighteen in Concord, One in Keeping." On you go. Saltmere\'s two days west. Mind the cliff path in wind.']}]},
          {'type': 'event', 'name': 'Accord guard (aside)', 'at': [6, 77], 'pages': [
              {'graphic': {'sprite': 'NPC 07', 'dir': 'up'}, 'commands': ['Second Guard: Nobody past. Orders came down this morning.']},
              {'cond': {'switch': 'CH1_ORCHARD_DONE'}, 'graphic': {'sprite': 'NPC 07', 'dir': 'right'}, 'commands': [
                  "Second Guard: (low) That's the null one from the dock. Captain said let them through, whatever happens.", 'Accord Guard: Which captain?',
                  "Second Guard: Didn't say. Came down from Crownhaven with a white seal on it.", '\\pf[ACCORD_GUARD,deadpan,sweat,Accord guard](They notice you listening.)',
                  'Accord Guard: Lovely weather.']}]},
          obj('The Hale Bell', (16, 70), ['THE HALE BELL: A ship\'s bell on a post above the sea cliff. The ferrymen rang it once the last boat was in.',
              'A cloth has been tied round the clapper.', J('sad', "Dad tied that. The night they closed the strait. He said there wasn't anything left to ring for.")]),
          talk('Hay-cart Driver', (26, 70), 'NPC 11', ["Hay-cart Driver: Used to take me four hours to Briarwick and back by the forest road.",
               "Hay-cart Driver: Now it's all glass and I go round by Saltmere. Two days. Glass doesn't pay my horse."]),
          sign((10, 75), 'Hale Bell fork sign', "THE HALE BELL. <- LACECLIFF WALK, Marram Down and SALTMERE (the Strand Road). ^ Windfall Row. v Ferrow's Landing."),
          at(ev['THE FERRYMEN\'S MILE\nF'], 18, 104) if "THE FERRYMEN'S MILE\nF" in ev else sign((18, 104), 'Road sign', "THE FERRYMEN'S MILE\nFerrow's Landing - Hale's Bramble - Windfall Row.\nMind the hedges. The hedges mind you."),
          at(ev['Pim'], 26, 66), at(ev['Dory'], 29, 46), at(ev['Farmhand'], 40, 62), at(ev['Under the stile'], 11, 99), at(ev['Stile'], 12, 98),
          at(ev['Scarecrow'], 44, 56), at(ev['Lookout board'], 12, 62), at(ev['Waystone'], 33, 8), at(ev['Old well'], 20, 52),
          trainer((36, 22), 'YOUNGSTER', 'Pip', "My squad's undefeated on this lane! It's a short lane.", 'Aw, my squad lost!', d='left'),
          trainer((25, 34), 'LASS', 'Wren', 'Birdies! Go!', 'My birdies! Oh, well done.', d='right'),
          obj('Ferry-toll booth', (13, 88), ['THE OLD FERRY-TOLL BOOTH. Fare board: "Landing to Saltmere, 3 coppers. Landing to the Strait, 5. Return, ask the captain."',
              'Under it, chalked: "STRAIT CLOSED." Under that, smaller: "for now"']),
          obj('Road Stone I', (34, 104) if False else (19, 107), ['ROAD STONE I. THE STRAND ROAD. "Ferrow 0." Someone has taken a rubbing of it. Many someones.']),
          obj("Hale's Bramble", (36, 60), ["HALE'S BRAMBLE. Six terraces of bramble and berry. Wenna's cousin sells tarts at the shed. The tarts are better than Wenna's. Don't tell Wenna."]),
          talk("Wenna's cousin", (52, 38), 'NPC 16', ["Wenna's cousin: Berries are picked by the terrace. Bottom terrace is for tourists. Top terrace is for family.",
               "Wenna's cousin: You look like family. ...No, you look tired. Here."], again=["Wenna's cousin: Mind the brambles on the way down."]),
          {'type': 'berry', 'at': [40, 56], 'berry': 'ORANBERRY'}, {'type': 'berry', 'at': [46, 50], 'berry': 'PECHABERRY'},
          {'type': 'berry', 'at': [52, 43], 'berry': 'CHERIBERRY'}, {'type': 'berry', 'at': [56, 39], 'berry': 'ORANBERRY'},
          obj('The Minding Hedges', (16, 64), ['THE MINDING HEDGES. "Mind the hedges. The hedges mind you." A maze of three turns, planted by a ferryman who missed the sea.']),
          hidden((12, 60), 'POTION', 'HiddenItem (hedge maze)'),
          talk('Shepherd', (46, 20), 'NPC 20', ['Shepherd: Three of my Wooloo got out again. They roll. Downhill. Always downhill.',
               "Shepherd: If you see a Wooloo, walk it uphill. It'll be so surprised it'll follow you."]),
          talk('Wooloo', (40, 14), 'Followers/WOOLOO', ['Baaa. (It is rolling, very slowly, in no direction.)'], move='random'),
          talk('Wooloo ', (50, 26), 'Followers/WOOLOO', ['Baaa.'], move='random'),
          item((50, 12), 'POKEBALL'), item((8, 50), 'POTION'), hidden((8, 98), 'BIGPEARL', 'HiddenItem (Ferryman\'s Rest)'),
          item((10, 97), 'REVIVE'), obj("The Ferryman's Rest", (9, 95), ["A rowboat hauled up in a sea cave. A name on the bow, painted out. Bootprints, small, going in and not out."]),
          {'type': 'cut_tree', 'at': [13, 89], 'name': 'CutTree'})
    r.seat_events(on='.dts')
    for x in range(36, 59, 3):
        for y in (40, 47, 54):
            if m.free(x, y, 2, 1, on='.') and m.ht[y, x] == m.ht[y, x + 1]: m.stamp('pf_logbench', x, y, mark='B') if False else None
    for y in (82, 86):                                                                # Juno's clearing fence and the hedge maze
        m.fence(26, 34, y)
    m.fence(10, 20, 58, gaps=((14, 15),)); m.fence(10, 20, 66, gaps=((17, 18),)); m.fence(10, 18, 62, gaps=((11, 12),))
    m.fence(38, 54, 10, gaps=((44, 45),)); m.fence(38, 54, 28)
    r.stamp('gl_shed', 50, 31, mark='B') if m.free(50, 31, 4, 6, on='.') else None
    r.dress(trees=('tr_oak', 'tr_oak2', 'tr_pine', 'tr_pink'), n_trees=W * H // 140, copses=8, scatter=12)
    r.paint(glint=0.25)
    flowers(r, 30, 84, 4, 2, p=0.4)
    for y in range(82, 106, 5): water_stamp(r, 'hb_post1', 4, y) if False else None
    h = head(520, "The Ferrymen's Mile", field='MEADOW', bgm='Route 1',
             connections=[{'dir': 'S', 'offset': 11, 'to': 100, 'to_offset': 28}, {'dir': 'N', 'offset': 30, 'to': 521, 'to_offset': 58},
                          {'dir': 'W', 'offset': 72, 'to': 527, 'to_offset': 22}],
             fog={'name': 'prismfall_seamist', 'opacity': 30, 'blend': 0, 'zoom': 200, 'sx': 1, 'sy': 0}, tone=[4, 4, -4, 0])
    r.write(h, '520_ferrymens_mile.yaml', "# The Ferrymen's Mile (520). WRITTEN BY layouts/routes_early.py - edit that script.\n", '/tmp/rt/520.png' if PREV else None)


# ====================================================================================================== 521 Windfall Row
ORCH = ('tr_oak', 'tr_oak2', 'tr_pink')


def orchard_rows(r, x0, y0, x1, y1, kind, gap=5, name=None, sign_at=None, skip_row=None):
    """an orchard: rows of one species of fruit tree with grass lanes between (every tree a Headbutt tree)"""
    m = r.m; st = STAMPS[kind]; w, h = st['w'], st['h']; rows = 0
    m.rect(x0, y0, x1 - x0 + 1, y1 - y0 + 1, '.', only='T.t')
    y = y0
    while y + h - 1 <= y1:
        rows += 1
        if skip_row != rows:
            x = x0 + (rows % 2)
            while x + w - 1 <= x1:
                if m.can_tree(kind, x, y, on='.t'): m.stamp(kind, x, y, mark='B')
                x += w + 1
        y += gap
    if sign_at: r.add(sign(sign_at, name + ' sign', name))
    return rows


def build_521():
    """Windfall Row (120x70, MEADOW): the farm lanes north of the Mile.  The Hale orchards (apple, pear, plum, cherry,
    quince, medlar; Headbutt trees), the Cider Press yard, the farmhouse (R2_FARM), the duck pond, the old mill tower on
    its rise, the Glassed Orchard gate in the hedge (R2_ORCHARD, Chapter 1), the corded forest road west to the
    Gossamer (R2_WOOD, never opens from this side), the Thirteenth Row (secret walled garden with a sleeping Applin)"""
    W, H = 120, 70
    r = Route(521, W, H, 'meadow', base='.')
    m = r.m
    r.forest_band('N', 7, wobble=3.0); r.forest_band('W', 6, wobble=3.0)
    for cx, cy, rx, ry in ((12, 48, 8, 7), (34, 62, 9, 5), (110, 12, 8, 6), (8, 28, 5, 6)):
        r.copse(cx, cy, rx, ry)
    # the Glassed Orchard hedge: woods east of x 61 in the north, the gate at (61, 22-23)
    for y in range(8, 32):
        for x in range(62, 70): m.cls[y, x] = 'T'
    m.ht[34:48, 92:110] = 1                                                          # the mill rise
    road = [(59, 69), (59, 58), (56, 48), (58, 40), (54, 32), (57, 24), (60, 22)]
    r.road(road, w=3.0, open_=None)
    r.road([(57, 40), (44, 34), (30, 26), (18, 14), (6, 10), (0, 10)], w=3.0, open_=None)   # the forest road (corded)
    r.road([(58, 46), (74, 46), (90, 50), (104, 52)], w=3.0, open_=None)                     # the farm lane east
    r.exit('S', 58, 4)
    m.cls[9:12, 0:2] = 'd'
    r.flatten(98, 100, 47, 1); r.crossing(98, 47, w=3, rows=3)
    r.lane([(99, 50), (99, 49)], w=2.0, open_=None)
    r.water(30, 50, 6, 3.5)                                                          # the duck pond
    r.grass(thr=0.6, scale=6.0, box=(0, 0, 60, 70))
    r.finish_plan()
    m.cls[9:12, 0:3] = 'd'
    # ---- the six Hale orchards
    rows = {}
    rows['apple'] = orchard_rows(r, 72, 8, 90, 26, 'tr_oak', name='HALE ORCHARD: APPLE ROWS', sign_at=(71, 28))
    rows['pear'] = orchard_rows(r, 93, 18, 116, 30, 'tr_oak2', name='HALE ORCHARD: PEAR ROWS', sign_at=(92, 31))
    rows['plum'] = orchard_rows(r, 64, 52, 86, 66, 'tr_oak2', gap=4, name='HALE ORCHARD: PLUM ROWS (12 rows)', sign_at=(63, 51))
    rows['cherry'] = orchard_rows(r, 36, 6, 52, 20, 'tr_pink', name='HALE ORCHARD: CHERRY ROWS', sign_at=(48, 22))
    rows['quince'] = orchard_rows(r, 88, 56, 116, 66, 'tr_oak', gap=5, name='HALE ORCHARD: QUINCE ROWS', sign_at=(88, 55))
    rows['medlar'] = orchard_rows(r, 18, 30, 34, 42, 'tr_oak2', name='HALE ORCHARD: MEDLAR ROWS', sign_at=(20, 43))
    # the Thirteenth Row: a walled garden behind the plum rows (a gap in the hedge at the far end)
    m.rect(87, 58, 1, 2, '.')
    ev = old_events('521_reskin.yaml', 521)
    J = lambda e, t: P('JUNO', e, t)
    cord = {'type': 'event', 'name': 'Forest-road cordon', 'at': [3, 9], 'pages': [{'graphic': {'tile': barrier_tile()}, 'trigger': 'action', 'commands': [
        '(Tape across the forest lane. Beyond it, a mile into the trees, something catches the light the wrong way.)']},
        {'cond': {'var': ['BRIARWICK_GLASSWOOD', 1]}, 'through': True, 'commands': []}]}
    r.events += [dict(cord, at=[3, y], name='Forest-road cordon %d' % (i + 1)) for i, y in enumerate((9, 10, 11))]
    for y in (9, 10, 11): m.taken[y, 3] = True
    r.add({'type': 'door', 'at': [0, 0], 'name': 'placeholder'} if False else None,
          {'type': 'warp', 'name': 'To Gossamer Wood', 'at': [0, 10], 'to': {'map': 524, 'x': 41, 'y': 108, 'dir': 'up'}},
          {'type': 'warp', 'name': 'To Gossamer Wood 2', 'at': [0, 9], 'to': {'map': 524, 'x': 40, 'y': 108, 'dir': 'up'}},
          {'type': 'warp', 'name': 'To Gossamer Wood 3', 'at': [0, 11], 'to': {'map': 524, 'x': 42, 'y': 108, 'dir': 'up'}},
          {'type': 'warp', 'name': 'To the Glassed Orchard', 'at': [61, 23], 'link': 'R2_ORCHARD', 'arrive': [60, 23, 'left']},
          {'type': 'warp', 'name': 'To the Glassed Orchard 2', 'at': [61, 22], 'to': {'map': 522, 'x': 2, 'y': 37, 'dir': 'right'}},
          talk('Cordon Warden', (6, 12), 'NPC 07', ["Cordon Warden: Forest road's shut. The Glasswood's across it. Nobody walks it till the Warden in Briarwick says so.",
               "Cordon Warden: Go round by the coast like everyone else. Saltmere, then the Weavers' Road up the river. It's two days. It's a nice two days.",
               J('sad', 'It used to be four hours. Uncle Rowan and I walked it every summer with a donkey called Parsnip.'),
               J('neutral', 'Parsnip hated the forest. Parsnip was right, as it turns out.')], d='right') if False else
          {'type': 'event', 'name': 'Cordon Warden', 'at': [6, 12], 'pages': [
              {'graphic': {'sprite': 'NPC 07', 'dir': 'right'}, 'trigger': 'action', 'commands': [
                  "Cordon Warden: Forest road's shut. The Glasswood's across it. Nobody walks it till the Warden in Briarwick says so.",
                  "Cordon Warden: Go round by the coast like everyone else. Saltmere, then the Weavers' Road up the river. It's two days. It's a nice two days.",
                  J('sad', 'It used to be four hours. Uncle Rowan and I walked it every summer with a donkey called Parsnip.'),
                  J('neutral', 'Parsnip hated the forest. Parsnip was right, as it turns out.')]},
              {'cond': {'var': ['BRIARWICK_GLASSWOOD', 1]}, 'graphic': {'sprite': 'NPC 07', 'dir': 'right'}, 'trigger': 'action', 'commands': [
                  "Cordon Warden: The glass went back a mile overnight. Road's open. Don't ask me how. I just roll up tape."]}]},
          sign((56, 64), 'Road sign', 'WINDFALL ROW -- <- Gossamer Wood & Briarwick (ROAD CLOSED BY ORDER OF THE ACCORD).\nOrchard law: keep what has fallen, and nothing else.'),
          at(ev['Wim'], 46, 30), at(ev['Ada'], 76, 44), at(ev['Joss'], 22, 18),
          trainer((84, 36), 'BUGCATCHER', 'Dell', 'My Metapod is going to evolve THIS time. Watch!', 'My Metapod was supposed to evolve this time...', d='down'),
          trainer((104, 40), 'PICNICKER', 'Mae', 'Battle first, sandwich after! House rules.', 'You can have a sandwich anyway!', d='left'),
          talk('Hay-cart Driver', (62, 44), 'NPC 25', ["Hay-cart Driver: Used to take me four hours to Briarwick and back by the forest road.",
               "Hay-cart Driver: Now it's all glass and I go round by Saltmere. Two days. Glass doesn't pay my horse."]),
          at(ev['Coll (Headbutt tutor)'], 52, 50), at(ev['Wayside shrine'], 26, 22),
          {'type': 'berry', 'at': [36, 46], 'berry': 'PECHABERRY'}, {'type': 'berry', 'at': [70, 30], 'berry': 'ORANBERRY'},
          item((14, 36), 'POKEBALL'), item((114, 46), 'POTION'), hidden((80, 20), 'ORANBERRY', 'HiddenItem (windfall)'),
          obj('Cider press', (101, 54), ['THE CIDER PRESS. A screw press as big as a cart, smelling of last autumn. A sign: "WINDFALLS ONLY. WE CAN TELL."']),
          talk('Cider-maker', (98, 56), 'NPC 20', ['Cider-maker: Windfalls make the best cider. The tree already decided they were ready. Who am I to argue with a tree?'],
               again=['Cider-maker: Cellar door? Cellar\'s for the barrels. And the barrels are for later.']),
          obj('Cellar door', (106, 51), ['A cellar door, padlocked. Chalked on it: "NOT YET".']),
          obj('Old mill tower', (101, 40), ['The old mill. The sails came down in the Reform and nobody put them back. The Wingull live in it now. They pay no rent.']),
          talk('Farm stand keeper', (66, 49), 'NPC 16', ['Farm stand: Berries a copper a punnet! Apples two! Plums are free if you can reach them!']),
          obj('Beehive wall', (40, 24), ['A drystone wall with hives set into it like windows. The Combee inside sound busy and important.']),
          talk('Orchard hand', (82, 14), 'NPC 03', ['Orchard hand: Every tree here is a Headbutt tree, if you know how. Coll knows how. Coll knows too much about it.'], move='random'),
          {'type': 'event', 'name': 'Scarecrow', 'at': [75, 60], 'pages': [{'graphic': {'sprite': 'Followers/SUDOWOODO', 'dir': 'down'}, 'trigger': 'action',
                                                                             'commands': [{'script': 'pf_trial_talk(:SCARECROW)'}]}]},
          obj('Applin (sleeping)', (90, 60), ['(A walled garden behind the thirteenth row. An Applin is asleep in the long grass, curled up like a windfall.)',
              'It does not wake. Orchard law: keep what has fallen, and nothing else.'], trigger='action'),
          item((92, 62), 'MIRACLESEED'),
          obj('Thirteenth Row', (87, 57), ['The plum orchard has twelve rows on the sign. This is the thirteenth.']))
    r.seat_events(on='.dt')
    r.stamp('gl_cot', 47, 38, mark='B') if False else None
    fd = m.front('gl_cot', 50, 44, 'R2_FARM', 'Farmhouse door')
    r.events.append([e for e in m.events if e.get('link') == 'R2_FARM'][0]); m.events = []
    m.cls[45:47, 49:52] = np.where(m.cls[45:47, 49:52] == 'B', 'B', 'd')
    r.stamp('gt_tower', 99, 34, mark='B') if m.free(99, 34, 3, 6, on='.') else None
    for n, x, y in (('pf_stall2', 64, 47), ('hb_barrels', 104, 55), ('hb_tubs', 94, 53), ('hb_crates4', 96, 58), ('hb_shed', 106, 56),
                    ('pf_logbench', 34, 46), ('hb_washline', 44, 46)):
        r.near(n, x, y, on='.d', r=3)
    m.fence(84, 116, 54, gaps=((86, 88),)); m.fence(20, 34, 28, gaps=((26, 28),))
    r.dress(trees=ORCH, n_trees=W * H // 200, copses=4, scatter=12)
    r.paint(glint=0.0)
    flowers(r, 45, 60, 6, 3, p=0.4)
    h = head(521, 'Windfall Row', field='MEADOW', bgm='Route 2',
             connections=[{'dir': 'S', 'offset': 58, 'to': 520, 'to_offset': 30}], tone=[6, 4, -4, 0])
    r.write(h, '521_windfall_row.yaml', '# Windfall Row (521). WRITTEN BY layouts/routes_early.py - edit that script.\n', '/tmp/rt/521.png' if PREV else None)


# ====================================================================================================== 541 The Grey Saltings
def cave_mouth(m, x, y):
    """Sheridan's rock arch over a cliff face; the dark opening's bottom cell is (x, y)"""
    for dy in range(3):
        for dx in range(3):
            m.L[2, y - 2 + dy, x - 1 + dx] = C('sh', [[624, 625, 626], [632, 633, 634], [640, 641, 642]][dy][dx])


def salt_ground(r, cells):
    m = r.m; salt = [K.P1('salt%d' % i) for i in range(4)]
    for x, y in cells:
        m.L[0, y, x] = salt[0] if r.rng.random() < 0.55 else r.rng.choice(salt)


def pans(r, x0, y0, x1, y1, pw=(3, 5), ph=(2, 2)):
    """brine pans as tiles on salt ground (class S cells)"""
    m = r.m; y = y0
    while y < y1:
        h = r.rng.randint(*ph); x = x0 + r.rng.randint(0, 2)
        while x < x1:
            w = r.rng.randint(*pw)
            if x + w <= x1 and y + h <= y1 and (m.cls[y:y + h, x:x + w] == 'S').all() and not m.taken[y:y + h, x:x + w].any():
                for yy in range(y, y + h):
                    for xx in range(x, x + w):
                        v = ('n' if yy == y else 's' if yy == y + h - 1 else '') + ('w' if xx == x else 'e' if xx == x + w - 1 else '')
                        m.tile(K.P1('brine_' + (v or 'c')), xx, yy, 1); m.cls[yy, xx] = 'B'
            x += w + r.rng.choice((1, 1, 2))
        y += h + 1


def build_541():
    """The Grey Saltings (70x110, BEACH): salt pans to the horizon below the chalk cliff of Brinecut; the boiling-house
    and the Brinewife's Rest; a gravel causeway and boardwalks over tidal pools and mudflats; the wreck of a salt barge in
    the mud; the bird hide; the Sandygast castles; the Crabrawler ring; Road Stone II; the Drowned Lane (secret, night)"""
    W, H = 70, 110
    r = Route(541, W, H, 'marsh', kit={1: 'ak', 2: 'ak', 'default': 'ak'}, base='.')
    m = r.m
    # the chalk cliff of Brinecut (NE), its south face with the mine mouth
    for y in range(0, 50):
        for x in range(46, 70):
            if x >= 48 + 4 * RK.vnoise(0, y, 541, 8.0) and y < 46 + 3 * RK.vnoise(x, 0, 542, 8.0): m.ht[y, x] = 1
    m.ht[40:47, 54:62] = 1; m.ht[47:52, 54:62] = 0
    r.forest_band('W', 4, wobble=2.0); r.forest_band('N', 3, wobble=2.0)
    # tidal pools and mudflats in the middle, the salt flats in the south-west
    for cx, cy, rx, ry in ((22, 30, 7, 4), (36, 46, 6, 3), (14, 56, 5, 3), (40, 64, 8, 4), (26, 82, 5, 3), (52, 86, 6, 4), (48, 22, 4, 3)):
        r.water(cx, cy, rx, ry)
    for cx, cy, rx, ry in ((30, 38, 12, 6), (44, 74, 10, 6), (18, 68, 8, 5)):
        m.blob(cx, cy, rx, ry, 'd', seed=int(cx + cy), rough=0.8, only='.')
    for y in range(86, 106):
        for x in range(3, 30):
            if m.cls[y, x] == '.' and ((x - 16) / 13.0) ** 2 + ((y - 96) / 10.0) ** 2 <= 1.0: m.cls[y, x] = 'S'
    road = [(32, 109), (33, 100), (36, 90), (32, 78), (28, 64), (30, 52), (26, 40), (30, 28), (36, 16), (35, 0)]
    r.road(road, w=3.0, c='g', open_=None)
    r.exit('S', 30, 6); r.exit('N', 34, 4)
    for y in range(H):                                                                # gravel road stubs at the exits
        for x in range(W):
            if m.cls[y, x] == 'd' and ((y > H - 5 and 30 <= x < 36) or (y < 4 and 34 <= x < 38)): m.cls[y, x] = 'g'
    # boardwalks where the causeway crosses the pools (the cells stay water; planks over them)
    for y in range(H):
        for x in range(W):
            if r.road_mask[y, x] and m.cls[y, x] == 'w': r.deck.append((x, y))
    r.lane([(30, 50), (46, 50), (57, 50)], w=2.0, c='g', open_=None)                 # to the mine mouth
    r.lane([(32, 30), (44, 22), (52, 21)], w=2.0, c='g', open_=None)                 # to the bird hide
    r.lane([(30, 70), (14, 72), (10, 60)], w=2.0, c='g', open_=None)                  # to the Brinewife's Rest
    # the Drowned Lane: a tidal islet off the south-east, reached over a night-only shoal
    r.water(58, 100, 9, 7)
    m.blob(60, 100, 3.5, 2.5, '.', seed=5, rough=0.3, only='w')
    r.grass(thr=0.62, scale=6.0)
    r.finish_plan()
    for y in range(H):
        for x in range(W):
            if m.cls[y, x] == 'S' and m.ht[y, x] != 0: m.ht[y, x] = 0
    J = lambda e, t: P('JUNO', e, t)
    ev = old_events('540_route3_route4.yaml', 541)
    r.add({'type': 'warp', 'name': 'Mine back door', 'at': [57, 49], 'link': 'R4_MINE', 'arrive': [57, 50, 'down'], 'se': 'Door exit'},
          sign((36, 104), 'Road sign', "THE GREY SALTINGS -- The Weavers' Road. v Saltmere (North Gate) - ^ The Dyers' Ford, Thistledown Lea & Briarwick.\nMind the pans. The pans do not mind you."),
          once('The Saltings', (33, 98), ['(Salt pans to the horizon, white stacks, the smoke of the boiling-house, and a chalk cliff behind with a mine mouth in it.)',
               J('neutral', 'This is where Saltmere\'s salt comes from. "Grey" is the salt before it\'s washed.'), J('neutral', "...And the weather. It's mostly the weather.")]),
          trainer((24, 46), 'SAILOR', 'Morrow', "Salt barge went down in the mud in '88. Still there. Still salty.", "You're heavier than you look. In battle, I mean.", d='right'),
          trainer((40, 60), 'TUBER_F', 'Pip', "My floaty is a Wailmer! No it's not. It's a floaty.", 'Waaah! My floaty popped!', d='left'),
          trainer((36, 30), 'CAMPER', 'Ned', 'Sand in my tent! Sand in my boots! Sand in my battle!', 'Sand in my tent AND I lost. Great day.', d='down'),
          talk('Salt Raker', (16, 92), 'NPC 19', ["Salt Raker: You're the ones from the Pageant? Everyone's heard.",
               "Salt Raker: The rakers say the Mourner's a Saltmere man. The boilers say he's from Verdance. Nobody says it loud."], move='random'),
          talk('Samphire Picker', (44, 72), 'NPC 27', ["Samphire Picker: Pick from the edges. The middle's the Plate's. Don't ask me what that means. My mother said it."]),
          talk('Children building Sandygast castles', (20, 66), 'NPC 16', ["Children: Don't step on that one! That one's ALIVE. ...That one too."]),
          talk('Sandygast', (22, 67), 'Followers/SANDYGAST', ['(A sand castle. It is watching you.)']),
          talk('Squawkabilly watcher', (50, 24), 'NPC 09', ['Watcher: Squawkabilly. Four colours, one flock, and every one of them thinks it\'s the real one.',
               J('happy', 'Squawkabilly! Four colors! In the wild they argue about which one\'s the real one!')]),
          obj('Salt-barge wreck', (34, 39), ["The wreck of a salt barge, sunk to the gunwales in the mud. The name board says HONEST WEIGHT."]),
          hidden((36, 40), 'BIGPEARL', 'HiddenItem (salt-barge wreck)'),
          {'type': 'event', 'name': 'Ring Boss', 'at': [44, 76], 'pages': [{'graphic': {'sprite': 'NPC 21', 'dir': 'down'}, 'trigger': 'action', 'commands': [
              {'if': 'pfm?(:crab_ring)', 'then': ["Ring Boss: Champion of the mudflat! The bucket's yours. The glory's mine."],
               'else': ['Ring Boss: Crabrawler ring! Three bouts, no biting, best of three, winner gets the bucket!',
                        {'choices': ['Step into the ring.', 'Not now.'], 'cancel': 1, 'branches': [
                            [{'script': 'WildBattle.start(:CRABRAWLER, 15)'}, {'script': 'WildBattle.start(:CRABRAWLER, 15)'},
                             {'script': 'WildBattle.start(:CRABRAWLER, 16)'}, "Ring Boss: Champion! Here's the bucket.", '(It contains a KING\'S ROCK.)',
                             {'script': 'pbReceiveItem(:KINGSROCK)'}, {'script': 'pfm_set(:crab_ring)'}],
                            ['Ring Boss: The ring is always open. The ring never closes. The tide closes it, twice a day.']]}]}]}]},
          obj('Road Stone II', (29, 6), ['ROAD STONE II. THE WEAVERS\' ROAD. "Saltmere 1, Briarwick 4." A ribbon of undyed silk is tied round it.']),
          obj('The boiling-house', (22, 82), ['THE BOILING-HOUSE. Brine in, salt out, smoke up. A notice: "NO SWIMMING IN THE PANS. THIS MEANS YOU, TERRENCE."']),
          {'type': 'event', 'name': 'The Drowned Lane', 'at': [50, 96], 'pages': [{'trigger': 'action', 'commands': [
              {'if': 'PBDayNight.isNight?', 'then': ['The tide is out. An old cart road shows under an inch of water, all the way to the islet.',
                                                    {'script': 'pbFadeOutIn { $game_player.moveto(59, 100) }'}],
               'else': ['Water as far as the islet. The rakers say an old cart road runs under it, at night.']}]}]},
          obj("Wreckers' cache", (61, 99), ["A wreckers' cache: a tarred chest, padlocked. The lock is stamped SALTMERE HARBOUR OFFICE."]),
          item((59, 101), 'BIGPEARL'), hidden((62, 101), 'STARDUST', 'HiddenItem (the Drowned Lane)'),
          {'type': 'event', 'name': 'Back to the causeway', 'at': [58, 100], 'pages': [{'trigger': 'action', 'commands': [
              'Wade back along the drowned cart road?', {'choices': ['Yes', 'No'], 'cancel': 1, 'branches': [[{'script': 'pbFadeOutIn { $game_player.moveto(48, 96) }'}], []]}]}]},
          item((10, 30), 'POTION'), item((60, 34), 'GREATBALL'), hidden((14, 100), 'PEARL', 'HiddenItem (salt pans)'))
    r.seat_events(on='.dtgS')
    fd = m.front('sh_cot', 12, 58, 'R4_REST', "The Brinewife's Rest door")
    r.events += [e for e in m.events if e.get('link') == 'R4_REST']; m.events = []
    m.cls[59:61, 11:14] = np.where(m.cls[59:61, 11:14] == 'B', 'B', 'g')
    r.stamp('gl_flat2', 18, 76, mark='B') if m.free(18, 76, 7, 6, on='.dgS') else None   # the boiling-house
    r.near('fw_smoke_a', 22, 74, on='.dg', r=2)
    r.stamp('gl_shed', 52, 15, mark='B') if m.free(52, 15, 4, 6, on='.') else r.near('gl_shed', 52, 15, on='.', r=4)   # the bird hide
    for n, x, y in (('hb_salt0', 8, 92), ('hb_salt1', 24, 100), ('hb_salt2', 12, 102), ('hb_salt0', 26, 92), ('hb_tubs', 6, 98), ('hb_barrel', 20, 88)):
        r.near(n, x, y, on='S', r=3)
    pans(r, 4, 88, 29, 106)
    r.dress(trees=('tr_pine', 'tr_pine2'), n_trees=W * H // 400, copses=2, scatter=8)
    r.paint(glint=0.15)
    salt_ground(r, [(x, y) for y, x in np.argwhere(m.cls == 'S')])
    cave_mouth(m, 57, 49)
    ship_part(r, -14, -15, 51, on='d.')
    h = head(541, 'The Grey Saltings', field='BEACH', bgm='Route 2', biome='route',
             connections=[{'dir': 'S', 'offset': 30, 'to': 140, 'to_offset': 43}, {'dir': 'N', 'offset': 34, 'to': 552, 'to_offset': 38}],
             tone=[0, 0, 4, 18], fog={'name': 'prismfall_seamist', 'opacity': 40, 'blend': 0, 'zoom': 200, 'sx': 1, 'sy': 0})
    r.write(h, '541_grey_saltings.yaml', '# The Grey Saltings (541). WRITTEN BY layouts/routes_early.py - edit that script.\n', '/tmp/rt/541.png' if PREV else None)


# ====================================================================================================== 552 The Dyers' Ford
def build_552():
    """The Dyers' Ford (80x72, MEADOW): the River Selvedge in three dyed bands below the dye-works' three vat sheds;
    drying lines over the road; the stepping-stone ford; the madder, woad and weld fields; the fulling mill; the cloth
    barge at its jetty; the Smeargle's boundary stone; the sheep-wash; the shrine of the Fourth Colour; the survey
    flags; the Bleachfield behind a culvert (secret, Cut)"""
    W, H = 80, 72
    r = Route(552, W, H, 'meadow', base='.')
    m = r.m
    r.forest_band('E', 5, wobble=3.0); r.forest_band('W', 5, wobble=3.0)
    for cx, cy, rx, ry in ((10, 8, 7, 5), (70, 12, 6, 6), (12, 62, 7, 5), (68, 60, 7, 6)):
        r.copse(cx, cy, rx, ry)
    # the River Selvedge, west to east across the middle (rows ~31-42), wobbling
    for x in range(W):
        c = 36 + 3 * (RK.vnoise(x, 0, 552, 14.0) - 0.5) * 2
        for y in range(int(c - 5), int(c + 6)): m.cls[y, x] = 'w'
    road = [(38, 71), (40, 60), (36, 50), (38, 44), (40, 36), (40, 28), (44, 18), (42, 8), (40, 0)]
    r.road(road, w=3.0, open_=None, only='T.t')
    r.exit('S', 38, 4); r.exit('N', 39, 4)
    stones = [(x, y) for y in range(H) for x in range(38, 42) if m.cls[y, x] == 'w' and (x + y) % 3 != 0 or (m.cls[y, x] == 'w' and x == 39)]
    # the dye-works on the north bank; the fields south; the mill west; the jetty east
    m.blob(54, 20, 9, 5, 'd', seed=7, rough=0.4, only='.t')
    r.lane([(44, 20), (56, 20)], w=2.0, open_=None)
    r.lane([(38, 54), (22, 52), (16, 46)], w=2.0, open_=None)                       # to the fulling mill
    r.lane([(40, 26), (62, 28), (66, 30)], w=2.0, open_=None)                        # to the jetty
    # the Bleachfield (NE, behind the culvert; Cut)
    r.pocket(70, 4, 5, 3, gate=(70, 9))
    m.cls[7:10, 70] = '.'
    r.grass(thr=0.58, scale=6.0, box=(4, 44, 76, 70))
    r.finish_plan()
    for x, y in stones: m.cls[y, x] = 'w'; m.taken[y, x] = True
    J = lambda e, t: P('JUNO', e, t)
    flag = lambda i, x, y, extra=(): {'type': 'event', 'name': 'Survey flag %d' % i, 'at': [x, y], 'pages': [{'graphic': {'sprite': 'Object ball', 'dir': 'down'} if False else {}, 'trigger': 'action',
                                     'commands': ['An orange survey flag on a stake. MERIDIAN LATTICE - LINE 7.'] + list(extra)}]}
    r.add(sign((36, 66), 'Road sign', "THE DYERS' FORD -- The Weavers' Road. Briarwick Dye-Works. Do not drink the river. Do not bathe in the river. Do not stand in the red."),
          once("The Dyers' Ford", (38, 62), ['(Below three vat-sheds, the River Selvedge runs in three bands: madder red, woad blue, weld yellow. Cloth dries on lines across the road.)',
               J('happy', "The Briarwick dyers wash their cloth here, so the river runs in three colors! There's a fourth band nobody's allowed to dye. It's just water. People leave ribbons for it.")]),
          talk('Meridian Surveyor', (46, 26), 'trainer_SCIENTIST', ['Meridian Surveyor: Mind the orange flags. Survey line for the new Lattice. Straight up the river and through to the wood.',
               'Meridian Surveyor: Trees aren\'t in the plan, but trees rarely are.'], d='left'),
          flag(1, 44, 24, [J('neutral', "These go right toward the Glasswood. That's..."), '(She stops. Two nights ago a man in a mask asked a theater why nothing in Verdance ever rots.)',
                           J('sad', "...That's probably fine. Isn't it?")]),
          flag(2, 45, 14), flag(3, 43, 6),
          hidden((44, 5), 'ANTIDOTE', 'HiddenItem (base of the third flag)'),
          trainer((52, 24), 'PAINTER', 'Morwenna', "Red's my color! Red's everyone's color, eventually, if you work the madder vat.", "Look at my hands. They'll be red till Fallmorn.", d='left'),
          trainer((60, 18), 'PAINTER', 'Ash', "Woad blue. The Queen's Elowen green is woad and weld together. She's never paid for a yard of it.", 'Bill her. Somebody bill her.', d='down'),
          talk('Dye Foreman', (36, 44), 'NPC 20', ["Dye Foreman: Step the stones in the order I hum. Red, blue, yellow. No -- that's blue, red, yellow.",
               "Dye Foreman: I've been humming it wrong for thirty years and nobody's told me."]),
          talk('Smeargle owner', (24, 60), 'NPC 18', ["Smeargle owner: My Smeargle paints a mark on the boundary stone for every trainer who passes.",
               "Smeargle owner: Yours is... it's left yours blank. It's never done that."]),
          talk('Smeargle', (25, 62), 'Followers/SMEARGLE', ['(It looks at you, then at its brush, then at you. It puts the brush away.)'], move='random'),
          obj('Boundary stone', (22, 61), ['A boundary stone painted with a hundred small marks in every colour. One square, near the bottom, is left blank.']),
          talk('Shearer', (64, 52), 'NPC 03', ["Shearer: Briarwick's dyers, Saltmere's salt, Ferrow's fish. Every town in Elowen's got a thing the Plate gives it.",
               "Shearer: We've got colors. Lovely colors. You can't eat them."]),
          talk('Mareep', (66, 54), 'Followers/MAREEP', ['Baa-zzt.'], move='random'), talk('Mareep ', (60, 56), 'Followers/MAREEP', ['Baa.'], move='random'),
          obj('Shrine of the Fourth Colour', (30, 30), ['A plain white ribbon tied to a stake at the edge of the undyed band. Dozens more are tied beside it.',
              'A card in a child\'s hand: "for the color nobody gets".']),
          trial('Hound shrine', (33, 29), 'SHRINE_FORD'),
          {'type': 'berry', 'at': [26, 50], 'berry': 'PECHABERRY'},
          obj('Fulling mill', (16, 44), ['THE FULLING MILL. Hammers the size of Snorlax beat the cloth soft. Not today: the wheel is waiting on the river.']),
          talk('Bargee', (66, 30), 'NPC 25', ["Bargee: Cloth barge to Saltmere. When the foreman's errand's done, I'll row you down. Till then I'm 'on my break'."]),
          obj('The Bleachfield', (70, 3), ['(Through the culvert: a small meadow where the undyed water spreads out. Every flower is white. The air rings, very faintly.)']),
          item((72, 4), 'TM44'), item((10, 50), 'POTION'), item((74, 46), 'SUPERPOTION'),
          obj('Madder field', (14, 58), ['MADDER (red). The dyers grow their own colours. Please stay on the path. The path is also madder.']),
          obj('Woad field', (52, 60), ['WOAD (blue). Do not eat. Do not roll in. Do not let the Mareep roll in.']),
          obj('Weld field', (34, 54), ['WELD (yellow). It looks like a weed because it is a weed. A very valuable weed.']))
    r.seat_events(on='.dt')
    for i, (nm, x, y) in enumerate((('gl_shed', 48, 13), ('gl_shed', 54, 12), ('gl_shed', 60, 13))):
        if m.free(x, y, 4, 6, on='.d'): m.stamp(nm, x, y)
    for n, x, y in (('pf_p_vat_r', 49, 20), ('pf_p_vat_b', 55, 20), ('pf_p_vat_y', 61, 20), ('pf_p_vat_r', 51, 21), ('pf_p_vat_b', 57, 21),
                    ('hb_dyeline', 44, 12), ('hb_rugline', 44, 16), ('hb_dyeline', 36, 22), ('hb_rugline2', 48, 26), ('hb_barrels', 64, 22),
                    ('hb_crates4', 58, 25), ('gl_cot', 12, 37) if False else ('hb_shed', 14, 40), ('pf_logbench', 30, 46)):
        r.near(n, x, y, on='.d', r=3)
    r.stamp('gl_flat2', 10, 36, mark='B') if m.free(10, 36, 7, 6, on='.') else r.near('gl_flat2', 12, 36, on='.', r=4)
    for x in (40, 41, 42, 39): overs_tile(r, 'pf_p_laundry', x - 1, 23)
    r.dress(trees=('tr_oak', 'tr_oak2', 'tr_pink'), n_trees=W * H // 200, copses=4, scatter=12)
    r.paint(glint=0.0)
    ST = [K.P1('pf_stepstone0'), K.P1('pf_stepstone1')]
    for i, (x, y) in enumerate(stones): m.L[1, y, x] = ST[(x + y) % 2]
    for y, x in np.argwhere(m.cls == 'w'):                                           # the three colours, and the clear band
        c = 36 + 3 * (RK.vnoise(x, 0, 552, 14.0) - 0.5) * 2
        band = (y - (c - 5)) / 11.0
        nm = 'red' if band < 0.3 else 'blue' if band < 0.58 else 'yellow' if band < 0.86 else None
        if nm and m.L[1, y, x] == 0 and m.L[2, y, x] == 0: m.L[2, y, x] = K.P1('dye_%s%d' % (nm, (x * 7 + y) % 2))
    water_stamp(r, 'hb_boat2', 70, 34)
    flowers(r, 70, 4, 4, 2, tiles=[K.DECOR_SH['flowers'][2]] * 3, p=0.6)
    h = head(552, "The Dyers' Ford", field='MEADOW', bgm='Route 3',
             connections=[{'dir': 'S', 'offset': 38, 'to': 541, 'to_offset': 34}, {'dir': 'N', 'offset': 39, 'to': 540, 'to_offset': 20}], tone=[6, 4, -2, 0])
    r.write(h, '552_dyers_ford.yaml', "# The Dyers' Ford (552). WRITTEN BY layouts/routes_early.py - edit that script.\n", '/tmp/rt/552.png' if PREV else None)


def overs_tile(r, n, x, y):
    L = np.array(STAMPS[n]['layers'])
    for z in range(3):
        for dy in range(L.shape[1]):
            for dx in range(L.shape[2]):
                t = int(L[z, dy, dx])
                if t: r.m.over.append((2, x + dx, y + dy, t))


# ====================================================================================================== 540 Thistledown Lea
def build_540():
    """Thistledown Lea (130x64, MEADOW): the extinct House Thistledown's river meadows.  The Selvedge along the south with
    the old stone bridge (toll nobody collects) and two islets; wildflower bands and four tall-grass fields; Thistledown
    Manor on its hill (R3_MANOR) with ruined wall, gateposts and topiary; the Brinecut mine mouth (R3_MINE) in the west
    outcrop; the Ponyta paddock; the broken mill and mill-race; the mowers' camp (heals once); the bamboo stand; Road
    Stone II-b; the Ha-ha (secret: the sunken wall's ditch to the manor's back garden)"""
    W, H = 130, 64
    r = Route(540, W, H, 'meadow', base='.')
    m = r.m
    r.forest_band('N', 4, wobble=2.0)
    for cx, cy, rx, ry in ((116, 10, 9, 6), (100, 46, 6, 4), (6, 40, 5, 5), (40, 8, 7, 4)):
        r.copse(cx, cy, rx, ry)
    # the Selvedge along the south third, islets
    for x in range(W):
        c = 52 + 2.5 * (RK.vnoise(x, 0, 540, 16.0) - 0.5) * 2
        for y in range(int(c - 4), int(c + 5)):
            if 0 <= y < H: m.cls[y, x] = 'w'
    m.blob(70, 52, 4, 1.6, '.', seed=3, rough=0.3, only='w'); m.blob(100, 53, 3, 1.4, '.', seed=4, rough=0.3, only='w')
    # the manor hill (h1 / h2) and the west outcrop with the mine mouth
    m.blob(64, 9, 17, 10, None, ht=1, seed=11, rough=0.3)
    for y in range(0, 26):
        for x in range(0, 18):
            if x < 14 + 3 * RK.vnoise(0, y, 541, 7.0) and y < 22 + 2 * RK.vnoise(x, 0, 543, 7.0): m.ht[y, x] = max(m.ht[y, x], 1)
    road = [(21, 63), (21, 52), (24, 42), (40, 36), (60, 34), (84, 33), (104, 31), (129, 31)]
    r.road(road, w=3.0, open_=None, only='T.tw')
    bridge = [(x, y) for y in range(H) for x in range(W) if r.road_mask[y, x] and RK.np.isin(m.cls[y, x], ['d']) and 44 <= y <= 60]
    r.exit('S', 20, 4); r.exit('E', 30, 4)
    r.flatten(63, 65, 18, 1); r.crossing(63, 18, w=3, rows=3)
    r.lane([(64, 33), (64, 21)], w=2.0, open_=None)
    r.flatten(7, 9, 22, 1)
    r.lane([(24, 40), (14, 30), (8, 26)], w=2.0, open_=None)                          # to the mine mouth
    r.lane([(84, 33), (90, 42), (96, 44)], w=2.0, open_=None)                         # to the broken mill
    # the Ha-ha: a ditch round the back of the manor hill to the back garden (NE of the hill)
    r.pocket(86, 6, 4, 3, gate=None)
    r.lane([(84, 20), (88, 12), (87, 8)], w=1.6, open_=None)
    r.grass(thr=0.58, scale=7.0, box=(26, 20, 128, 46))
    r.finish_plan()
    for (x, y) in bridge: m.cls[y, x] = 'w'; r.deck.append((x, y))
    J = lambda e, t: P('JUNO', e, t)
    ev = old_events('540_route3_route4.yaml', 540)
    r.add({'type': 'warp', 'name': 'Mine mouth', 'at': [8, 24], 'link': 'R3_MINE', 'arrive': [8, 25, 'down'], 'se': 'Door exit'},
          sign((26, 58) if False else (25, 44), 'Road sign', "THISTLEDOWN LEA -- The lands of House Thistledown (extinct). <- The Dyers' Ford - -> Gossamer Wood & Briarwick - ^ Thistledown Manor (PRIVATE. DECEASED.)"),
          once('The Lea', (22, 46), [J('happy', 'Mum says the Thistledowns were actors. All of them. Even the dog. They played Saltmere for a hundred years and then they all died in the same winter.'),
               J('neutral', "People say they're still up there. Rehearsing. I'd like to see that. From a distance. A long distance.")]),
          sign((60, 22), 'Manor sign', 'THISTLEDOWN MANOR\nHome of the Thistledown Players. Closed since AF 211.'),
          talk('Drover', (40, 26), 'NPC 25', ['Drover: Race you to the fence!', '(He wins. He always wins. He has a Ponyta.)']),
          talk('Ponyta', (44, 22), 'Followers/PONYTA', ['(It tosses its mane. Show-off.)'], move='random'),
          talk('Fisherman on the bridge', (23, 50), 'trainer_FISHERMAN', ["Fisherman: Bridge toll's a copper. Nobody's collected it since the house died. I just tell people. Habit."], d='left'),
          hidden((19, 52) if False else (24, 57), 'GREATBALL', 'HiddenItem (under the bridge)'),
          {'type': 'event', 'name': 'Mower', 'at': [80, 40], 'pages': [
              {'graphic': {'sprite': 'NPC 03', 'dir': 'down'}, 'trigger': 'action', 'commands': [
                  "Mower: Nobody's mown the Lea in sixty years. You can't buy land off a dead family. They won't come to the door.",
                  {'if': '!pfm?(:mowers_heal)', 'then': ['Mower: Sit by the fire a bit. Kettle\'s on.', {'heal': True}, {'script': 'pfm_set(:mowers_heal)'}]}]},
              {'cond': {'switch': 'CH2_THISTLE_DONE'}, 'graphic': {'sprite': 'NPC 03', 'dir': 'down'}, 'trigger': 'action', 'commands': [
                  'Mower: Woman in grey came through at dawn with two others. Shears in her belt. Nodded to me. Mannerly. Went toward the wood.']}]},
          trainer((52, 40), 'PICNICKER', 'Edie', "Ada beat me on Windfall Row last year. I've been training on the Lea all spring.", "...I'll write to Ada. I'll lie.", d='down'),
          at(ev['Bryony'], 36, 30), at(ev['Hale'], 70, 48) if False else trainer((74, 46), 'FISHERMAN', 'Hale', 'You scared the fish! Now you owe me a battle.', 'Reeled in a loss. Happens.', d='down'),
          trainer((92, 28), 'TWINS', 'Bel & Bea', 'Twins: We battle together! Always together!', "Twins: Saltmere's south. They do plays there!", d='down', double=True),
          trainer((112, 36), 'YOUNGSTER', 'Corin', "Saltmere badge? Prove it!", "My team's the coolest! ...Was.", d='left'),
          obj('Broken mill', (96, 42), ['The broken mill. The wheel is stuck half in the race. Someone has fished it clean of Magikarp.']),
          obj('Bamboo stand', (110, 18), ['A bamboo stand, planted by a Thistledown who wanted "something foreign". The Pancham agree.']),
          talk('Pancham', (108, 20), 'Followers/PANCHAM', ['(It glares at you over a bamboo shoot. Respect.)'], move='random'),
          obj('Road Stone II-b', (120, 30), ["ROAD STONE II-b. THE WEAVERS' ROAD. \"Briarwick 1.\" The '1' has been scratched to a '2' and back again."]),
          obj('Gateposts', (62, 23), ['Two stone gateposts with the Thistledown thistle carved on them. No gate. Gates are for people who expect visitors.']),
          obj('The Ha-ha', (87, 8), ['(The sunken wall\'s ditch runs round the back of the hill to an overgrown garden. A cellar door, barred from inside. Something is digging behind it.)']),
          talk('Greavard', (85, 6), 'Followers/GREAVARD', ['(It is digging very seriously. It does not want to be interrupted. It wags anyway.)'], move='random'),
          hidden((88, 5), 'RAREBONE', 'HiddenItem (the Ha-ha)'),
          {'type': 'berry', 'at': [30, 34], 'berry': 'CHERIBERRY'}, item((126, 20), 'SUPERPOTION'), item((4, 34), 'POKEBALL'), item((70, 51), 'GREATBALL'))
    r.seat_events(on='.dt')
    fd = m.front('sh_big', 64, 14, 'R3_MANOR', 'Manor door')
    r.events += [e for e in m.events if e.get('link') == 'R3_MANOR' or e.get('name') == 'Locked door']; m.events = []
    for n, x, y in (('sh_campfire', 78, 42), ('hb_tables', 82, 42), ('hb_shed', 84, 38), ('pf_logbench', 76, 44)):
        r.near(n, x, y, on='.d', r=3)
    m.fence(36, 50, 20, gaps=((42, 44),)); m.fence(36, 50, 28, gaps=((40, 41),))
    r.dress(trees=('tr_oak', 'tr_oak2', 'tr_pink', 'tr_pine'), n_trees=W * H // 180, copses=6, scatter=12)
    r.paint(glint=0.0)
    cave_mouth(m, 8, 24)
    for (cx, cy, rx, ry, k) in ((40, 14, 10, 4, 0), (90, 22, 9, 3, 1), (108, 42, 8, 3, 2), (30, 26, 6, 2, 3)):
        flowers(r, cx, cy, rx, ry, tiles=[K.DECOR_SH['flowers'][k], K.DECOR_SH['flowers'][k + 4]], p=0.5)
    h = head(540, 'Thistledown Lea', field='MEADOW', bgm='Route 3',
             connections=[{'dir': 'S', 'offset': 20, 'to': 552, 'to_offset': 39}, {'dir': 'E', 'offset': 30, 'to': 524, 'to_offset': 50}], tone=[6, 4, -2, 0])
    r.write(h, '540_thistledown_lea.yaml', '# Thistledown Lea (540). WRITTEN BY layouts/routes_early.py - edit that script.\n', '/tmp/rt/540.png' if PREV else None)


# ====================================================================================================== 524 Gossamer Wood
def build_524():
    """Gossamer Wood (90x110, SILKWOOD): giant silk-hung trees.  The silk-curtain trail from Thistledown Lea's edge (W) to
    Briarwick's gate (N, WOOD_BRIAR) with two side loops; the central clearing with Woodward's Hut (WOOD_HUT); the cocoon
    grove and silk-harvest racks; the fallen giant used as a tunnel; the mushroom ring; the Bleed Veil to the Deepwood
    behind a Cut tree (E); the corded forest road south to Windfall Row (opens when V105 >= 1); the Unpicked Seam (secret)"""
    W, H = 90, 110
    r = Route(524, W, H, 'forest', base='T')
    m = r.m
    trail = [(0, 51), (12, 50), (22, 56), (30, 66), (40, 62), (46, 52), (44, 40), (36, 30), (40, 18), (45, 8), (45, 0)]
    r.road(trail, w=3.0, open_=(2, 5))
    r.exit('W', 50, 4)
    m.cls[0:3, 44:47] = 'd'
    r.clearing(58, 52, 9, 7)                                                         # the central clearing: Woodward's Hut
    r.lane([(46, 52), (56, 52)], w=2.0, open_=(1, 3))
    r.lane([(56, 52), (72, 48), (84, 48), (89, 48)], w=2.0, open_=(1, 3))            # east to the Veil (Cut) and the Deepwood
    r.lane([(30, 66), (34, 80), (40, 94), (41, 106), (41, 109)], w=2.5, open_=(1, 3))   # the corded forest road south
    r.lane([(22, 56), (12, 72), (14, 86), (26, 84), (34, 80)], w=2.0, open_=(1, 3))   # side loop SW: the cocoon grove
    r.clearing(12, 80, 6, 5)
    r.lane([(36, 30), (22, 24), (14, 14), (26, 10), (40, 18)], w=2.0, open_=(1, 3))  # side loop NW: the mushroom ring
    r.clearing(18, 14, 6, 4)
    r.lane([(44, 40), (62, 34), (70, 24)], w=2.0, open_=(1, 2))                       # to the Giga Drain grove
    r.clearing(72, 20, 6, 5)
    r.pocket(76, 84, 6, 5, gate=None)                                                # the Unpicked Seam (behind a night silk wall)
    r.lane([(58, 58), (66, 70), (74, 80)], w=2.0, open_=(1, 2))
    r.grass(thr=0.55, scale=5.0)
    r.finish_plan(border=0)
    m.cls[106:110, 40:43] = 'd'
    J = lambda e, t: P('JUNO', e, t)
    ev = old_events('524_reskin.yaml', 524)
    entry = ev['Wood entry 1']['pages']
    r.events += line_events(r, 'Wood entry', 52, 3, 3, entry) if False else []
    for i, y in enumerate((50, 51, 52, 53)):
        r.events.append({'type': 'event', 'name': 'Wood entry %d' % (i + 1), 'at': [4, y], 'pages': entry}); m.taken[y, 4] = True
    veil = ev['Juno at the Veil 1']['pages']
    tape = lambda i, x: {'type': 'event', 'name': 'Accord cordon %d' % i, 'at': [x, 104], 'pages': [
        {'graphic': {'tile': barrier_tile()}, 'trigger': 'action', 'commands': [
            'ACCORD CORDON: The forest road back to Windfall Row and the Landing, taped off. A sign faces the farms: CLOSED BY ORDER OF THE ACCORD.',
            J('sad', "That's the way I used to come. Four hours with Parsnip. Now it's two days and a pageant.")]},
        {'cond': {'var': ['BRIARWICK_GLASSWOOD', 1]}, 'through': True, 'commands': []}]}
    for i, x in enumerate((40, 41, 42)): r.events.append(tape(i + 1, x)); m.taken[104, x] = True
    r.add({'type': 'warp', 'name': 'To Windfall Row', 'at': [41, 109], 'to': {'map': 521, 'x': 1, 'y': 10, 'dir': 'left'}},
          {'type': 'warp', 'name': 'To Windfall Row b', 'at': [40, 109], 'to': {'map': 521, 'x': 1, 'y': 9, 'dir': 'left'}},
          {'type': 'warp', 'name': 'To Windfall Row c', 'at': [42, 109], 'to': {'map': 521, 'x': 1, 'y': 11, 'dir': 'left'}},
          {'type': 'warp', 'name': 'To Briarwick', 'at': [44, 0], 'link': 'WOOD_BRIAR', 'arrive': [44, 1, 'down']},
          {'type': 'warp', 'name': 'To Briarwick b', 'at': [45, 0], 'to': {'map': 120, 'x': 36, 'y': 62, 'dir': 'up'}},
          {'type': 'warp', 'name': 'To Briarwick c', 'at': [46, 0], 'to': {'map': 120, 'x': 36, 'y': 62, 'dir': 'up'}},
          {'type': 'cut_tree', 'at': [82, 48], 'name': 'CutTree'},
          {'type': 'warp', 'name': 'To Deepwood', 'at': [89, 48], 'link': 'WOOD_DEEP', 'arrive': [88, 48, 'left']},
          sign((44, 103), 'Cordon notice', 'CLOSED BY ORDER OF THE ACCORD. From this side you can see the glass across the lane, a mile on.'),
          at(ev['Silk-picker'], 54, 46), at(ev['Old Weaver'], 30, 62),
          obj('Shrine stone', (16, 12), ['A small mossy shrine stone. A carving of three beasts chasing a masked figure. Someone has left a honey bun in front of the masked one, not the three.',
              J('neutral', "That's the Pageant. That's the play we saw. ...Somebody likes the Ogre better.")]),
          talk('Kestrel', (44, 6), 'trainer_RIVAL1', ["Kestrel: Briarwick's just ahead. Try not to get lost in the webs. ...Not that I'd come looking."]),
          trainer((38, 32), 'TWINS', 'Mo & Jo', 'We battle together!', 'We lose together.', d='right', double=True),
          trainer((30, 70), 'BUGCATCHER', 'Tobin', 'My bugs love the silk here!', 'Careful in the webs past here!', d='down'),
          trainer((46, 46), 'BUGCATCHER', 'Reed', 'You walked right into my web!', "The wood's full of better bugs than mine, huh.", d='left'),
          trainer((40, 18), 'AROMALADY', 'Petra', 'Smell that? Night-blooming gossamer.', 'What a lovely, fierce scent you have.', d='down'),
          trainer((14, 52), 'CAMPER', 'Bram', 'Camping in Gossamer? Battle first, questions later!', "Lost to a tourist. Don't tell anyone.", d='down'),
          item((70, 18), 'TM19'), item((8, 82), 'REPEL'), item((62, 50), 'POTION'), item((34, 34), 'ETHER'),
          {'type': 'event', 'name': 'HiddenItem', 'at': [22, 16], 'pages': ev['HiddenItem']['pages']},
          obj('Cocoon grove', (12, 78), ['A grove of silk cocoons the size of lanterns, hung in rows. Each has a weaver\'s knot-mark tied to it.']),
          talk('Weaver (harvest)', (16, 82), 'NPC 13', ['Weaver: One cocoon in three. Always leave two. The wood counts.']),
          talk('Weaver (racks)', (8, 84), 'NPC 27', ['Weaver: The racks dry the silk in the dark. Sun makes it brittle. Like Kestrel.']),
          obj('Mushroom ring', (18, 15), ['A ring of pale mushrooms. At night, they say, it glows, and the Morelull dance.']),
          trial('Monkey shrine', (20, 12), 'SHRINE_WOOD'),
          obj('Fallen giant', (58, 66), ['A fallen giant tree, hollow end to end. The weavers use it as a shortcut. The Venonat use it as a hotel.']),
          {'type': 'event', 'name': 'Silk seam', 'at': [74, 79], 'pages': [{'graphic': {'tile': int(np.array(STAMPS['pf_p_silk1']['layers']).max())}, 'trigger': 'action', 'commands': [
              {'if': 'PBDayNight.isNight?', 'then': ['The silk wall has loosened in the dark. It parts like a curtain.', {'selfswitch': ['A', True]}],
               'else': ['A wall of silk, tight as a drum. At night, the weavers say, the seams unpick themselves.']}]},
              {'cond': {'self': 'A'}, 'through': True, 'commands': []}]},
          {'type': 'event', 'name': 'Sap tree duel', 'at': [78, 84], 'pages': [{'graphic': {'sprite': 'Followers/HERACROSS', 'dir': 'left'}, 'trigger': 'action',
                                                                                'commands': [{'script': 'pf_trial_talk(:SAP_TREE)'}]}]},
          obj('Sap tree', (80, 83), ['A weeping sap tree. Two very large beetles are disputing ownership of it.']))
    for i, y in enumerate((47, 48, 49)): r.events.append({'type': 'event', 'name': 'Juno at the Veil %d' % (i + 1), 'at': [79, y], 'pages': veil}); m.taken[y, 79] = True
    r.seat_events(on='.dt')
    fd = m.front('gl_shed', 58, 51, 'WOOD_HUT', "Woodward's Hut door")
    r.events += [e for e in m.events if e.get('link') == 'WOOD_HUT']; m.events = []
    for n, x, y in (('pf_p_loom', 60, 55), ('pf_p_net', 52, 56), ('pf_p_laundry', 62, 48), ('pf_logbench', 54, 54), ('pf_p_lantern', 64, 52)):
        r.near(n, x, y, on='.d', r=3)
    for x, y in ((56, 66), (58, 66), (60, 66)):
        pass
    gts = 0
    for n, x, y in (('pf_g_tree4p', 24, 36), ('pf_g_tree4p', 52, 24), ('pf_g_tree4p', 62, 88), ('pf_g_tree2', 20, 92), ('pf_g_tree2', 66, 40), ('pf_g_tree4p', 8, 26),
                    ('pf_g_tree2', 30, 46), ('pf_g_tree4p', 72, 60)):
        if m.free(x, y, STAMPS[n]['w'], STAMPS[n]['h'], on='.tT'):
            m.stamp(n, x, y, mark='B', blend=True); gts += 1
    r.dress(trees=('tr_oak', 'tr_oak2', 'tr_pine'), n_trees=W * H // 220, copses=0, scatter=10)
    for _ in range(W * H // 50):                                                     # the Gossamer's silk: webs and strands
        nm = r.rng.choice(['pf_p_web', 'pf_p_web1', 'pf_p_silk', 'pf_p_strand_w', 'pf_p_strand_p'])
        x, y = r.rng.randrange(W), r.rng.randrange(H); st = STAMPS[nm]
        if m.free(x, y, st['w'], st['h'], on='.'): m.stamp(nm, x, y, mark=None)
    r.paint(glint=0.0)
    for x, y in ((56, 65), (58, 65), (60, 65)): pass
    h = head(524, 'Gossamer Wood', field='SILKWOOD', bgm='Route 3', biome='forest',
             connections=[{'dir': 'W', 'offset': 50, 'to': 540, 'to_offset': 30}], tone=[-28, -8, -30, 25],
             fog={'name': 'prismfall_spores', 'opacity': 40, 'blend': 1, 'zoom': 100, 'sx': 1, 'sy': -1})
    h['metadata']['BattleBack'] = 'forest'
    r.write(h, '524_gossamer_wood.yaml', '# Gossamer Wood (524). WRITTEN BY layouts/routes_early.py - edit that script.\n', '/tmp/rt/524.png' if PREV else None)


# ====================================================================================================== the Hoar Road (Ch4)
def auto_crossings(r, lips, w=3):
    """a stairway wherever the road crosses each terrace lip row (the lip is straightened there)"""
    m = r.m
    for yl, h in lips:
        xs = [x for x in range(r.W) if r.road_mask[yl, x]]
        if not xs: continue
        x0 = min(xs) + max(0, (len(xs) - w) // 2)
        r.flatten(x0, x0 + w - 1, yl, h); r.crossing(x0, yl, w=w, rows=3)


def build_566():
    """Spinners' Rise (80x120, MEADOW): the switchback drove road from Briarwick's forest edge up onto the open fell (the
    trees thin as you climb); the shepherds' hamlet; the Fleece Cross; the hill-fort ring on the summit; the Ram Race;
    the stone sheep-wash and cold spring; the first hoar near the top; Road Stone III; the Shearing Cave (secret)"""
    W, H = 80, 120
    r = Route(566, W, H, 'meadow', base='.')
    m = r.m
    lips = [(96, 1), (72, 2), (46, 3), (22, 4)]
    r.terraces(lips, wobble=3.0)
    r.forest_band('S', 26, wobble=6.0); r.forest_band('W', 8, wobble=4.0); r.forest_band('E', 8, wobble=4.0)
    for cx, cy, rx, ry in ((20, 70, 6, 4), (62, 60, 5, 4), (16, 40, 4, 3)):
        r.copse(cx, cy, rx, ry)
    road = [(39, 119), (40, 108), (26, 100), (24, 88), (46, 82), (58, 74), (52, 62), (30, 56), (26, 44), (44, 36), (56, 28), (48, 14), (44, 0)]
    r.road(road, w=3.0, open_=(2, 5))
    r.exit('S', 38, 4); r.exit('N', 42, 4)
    auto_crossings(r, lips)
    r.clearing(62, 90, 7, 5); r.lane([(46, 84), (58, 90)], w=2.0)                    # the shepherds' hamlet
    r.water(18, 60, 4, 2.5)                                                            # the sheep-wash and the cold spring
    r.lane([(30, 58), (22, 60)], w=2.0)
    r.clearing(40, 9, 9, 6)                                                            # the hill-fort ring on the summit
    r.grass(thr=0.6, scale=6.0)
    r.finish_plan()
    J = lambda e, t: P('JUNO', e, t)
    r.add(sign((42, 112), 'Road sign', "SPINNERS' RISE -- The Hoar Road. v Briarwick (North Gate) - ^ Frostwick Pass. The drove road: sheep have right of way. Sheep know it."),
          obj('The Fleece Cross', (50, 34), ['THE FLEECE CROSS. A market cross from the old wool fairs, hung with yarn tied by every spinner who ever sold here.',
              'The newest ribbon is dyed with all three of the Ford\'s colours. It is still wet.']),
          talk('Ribbon-tier', (52, 36), 'NPC 27', ['Ribbon-tier: Tie one for the road. The cross remembers who passed. The tax-man does too, but the cross is kinder.']),
          talk('Shepherd', (60, 88), 'NPC 20', ['Shepherd: The hamlet sleeps anyone the fell catches out. Third cottage, door\'s never locked. Mind the dog. The dog is a Lillipup and it is in charge.']),
          talk('Shepherd boy', (56, 76), 'NPC 05', ['Shepherd boy: Race you to the cross! My Skiddo knows every rock!', '(He is gone in a scatter of gravel. You will see him at the top. He will pretend he was always there.)']),
          talk('Skiddo', (57, 77), 'Followers/SKIDDO', ['(It bleats, very pleased with itself.)'], move='random'),
          obj('Sheep-wash', (20, 58), ['A stone sheep-wash fed by a cold spring. The water comes out of the hill already freezing.']),
          obj('Hill-fort ring', (40, 6), ['A ring of old earthworks on the summit. From here the Gossamer is a grey-green sea, and beyond it, the real one.']),
          obj('Road Stone III', (40, 116), ['ROAD STONE III. THE HOAR ROAD. "Briarwick 0, Frostwick 2." The frost has started at the top of the stone.']),
          obj('Waterfall at the sheep-wash', (14, 58), ['Behind the little fall at the sheep-wash, the rock goes back further than it should. The shepherds say nothing. Shepherds never do.']),
          item((16, 61), 'SOFTSAND'), talk('Wooloo (lost lamb)', (13, 60), 'Followers/WOOLOO', ['(A Wooloo lamb, hidden in the cave with the best fleece. It looks at you as if you might be its shepherd.)']),
          item((60, 92), 'POTION'), item((24, 40), 'SUPERPOTION'), item((70, 20), 'REPEL'), hidden((36, 10), 'STARDUST', 'HiddenItem (hill fort)'),
          {'type': 'berry', 'at': [64, 94], 'berry': 'ASPEARBERRY'})
    r.seat_events(on='.dt')
    for n, x, y in (('gl_cot', 58, 86), ('sh_small', 66, 86), ('gl_shed', 70, 88)):
        if m.free(x, y, STAMPS[n]['w'], STAMPS[n]['h'], on='.'): m.stamp(n, x, y)
    m.fence(52, 74, 96, gaps=((60, 62),))
    for n, x, y in (('fw_stone', 34, 8), ('fw_stone', 46, 8), ('fw_stone', 40, 4), ('fw_stone', 36, 13), ('fw_stone', 45, 13)):
        r.near(n, x, y, on='.t', r=2)
    r.dress(trees=('tr_oak', 'tr_oak2', 'tr_pine', 'tr_pine2'), n_trees=W * H // 300, copses=4, scatter=10)
    r.paint(glint=0.0)
    for y in range(0, 22):                                                           # the first hoar on the summit grass
        for x in range(W):
            if m.cls[y, x] == '.' and m.L[1, y, x] == 0 and r.rng.random() < 0.18 * (1 - y / 22.0):
                m.L[1, y, x] = r.rng.choice([K.STAMPS['fw_drift0']['layers'][1][0][0], K.STAMPS['fw_drift1']['layers'][1][0][0]])
    h = head(566, "Spinners' Rise", field='MEADOW', bgm='Route 3',
             connections=[{'dir': 'S', 'offset': 38, 'to': 120, 'to_offset': 52}, {'dir': 'N', 'offset': 42, 'to': 577, 'to_offset': 30}], tone=[0, 0, 4, 6])
    r.write(h, '566_spinners_rise.yaml', "# Spinners' Rise (566). WRITTEN BY layouts/routes_early.py - edit that script.\n", '/tmp/rt/566.png' if PREV else None)


def build_577():
    """Frostwick Pass (72x96, SNOWY_MOUNTAIN): the climb through hoar-crusted downs from Spinners' Rise (S) to Frostwick's
    East Gate (W); the Handfast Arch with the Meridian sunburst bolted on; the wind gap; the empty toll hut with two
    ledgers; the frozen tarn and its ice-fishing hole; avalanche fences; the bothy (rest); trappers' racks; the snowmen
    (one is a Snorunt); Road Stone III-b; the Hollow of the Handfast behind the frozen fall (secret)"""
    W, H = 72, 96
    r = Route(577, W, H, 'snow', base='.', kit='shs')
    m = r.m
    lips = [(74, 1), (50, 2)]
    r.terraces(lips, wobble=3.0)
    r.forest_band('E', 10, wobble=4.0); r.forest_band('S', 6, wobble=3.0); r.forest_band('N', 8, wobble=3.0)
    for cx, cy, rx, ry in ((14, 86, 8, 5), (12, 20, 8, 6), (56, 30, 6, 6)):
        r.copse(cx, cy, rx, ry)
    road = [(31, 95), (33, 86), (46, 78), (48, 66), (34, 56), (26, 46), (20, 40), (10, 38), (0, 38)]
    r.road(road, w=3.0, open_=(2, 6))
    r.exit('S', 30, 4); r.exit('W', 37, 4)
    auto_crossings(r, lips)
    m.blob(46, 30, 7, 4, 'p', seed=7, rough=0.4, only='.t')                           # the frozen tarn
    r.lane([(30, 50), (40, 36)], w=2.0, open_=(1, 3))
    r.pocket(54, 22, 4, 3, gate=None)                                                 # the Hollow of the Handfast
    m.cls[24:28, 50:52] = '.'
    r.grass(thr=0.62, scale=6.0)
    r.finish_plan()
    J = lambda e, t: P('JUNO', e, t)
    r.add(sign((34, 90), 'Road sign', "FROSTWICK PASS -- The Hoar Road. v Spinners' Rise - <- Frostwick (East Gate). Two scripts on one post; the Isenmar half is longer."),
          obj('The Handfast Arch', (12, 37), ['THE HANDFAST ARCH: half whale-jaw, half living briar, raised when the border was last agreed.',
              'A brass Meridian sunburst has been bolted across the keystone. The bolts are new and very shiny.']),
          obj('Toll hut ledgers', (40, 70), ['Two ledgers on the empty toll hut\'s counter, one per kingdom. They disagree about everything, including the date.']),
          talk('Bothy keeper', (52, 84), 'NPC 26', ['Bothy keeper: Sit. Drink. It\'s hot and it\'s brown. That\'s all I promise.', {'heal': True}]),
          obj('Ice-fishing hole', (44, 33), ['A round hole cut in the tarn ice, a line still in it. Face the water and use a rod.']),
          obj('Snowmen', (24, 58), ['A row of snowmen built by Frostwick children. One of them is blinking.']),
          talk('Snorunt', (26, 58), 'Followers/SNORUNT', ['(It is pretending very hard to be a snowman.)']),
          obj('Avalanche fence', (60, 60), ['Avalanche fences of split larch. Somebody has painted EAT MORE CHEESE on one in Isenmar.']),
          obj('Road Stone III-b', (30, 92), ['ROAD STONE III-b. THE HOAR ROAD. "Frostwick 1." The \'1\' is in Isenmar runes; the Elowen side says "nearly".']),
          obj('Frozen fall', (54, 20), ['(Behind the frozen fall, a hollow: carvings of a forester and a huscarl, their hands joined, and a bell on a ribbon.)']),
          item((55, 23), 'SOOTHEBELL'), item((8, 56), 'ICEHEAL'), item((62, 46), 'SUPERPOTION'), hidden((47, 28), 'NEVERMELTICE', 'HiddenItem (tarn)'),
          talk('Huscarl', (20, 44), 'NPC 21', ['Huscarl: Elowen side, Isenmar side. The arch doesn\'t care. Nor do I, mostly. Pass.'], d='right'),
          talk('Forester', (42, 80), 'NPC 14', ['Forester: The wind gap above the toll hut. Walk between the gusts or it walks you back down.']))
    r.seat_events(on='.dtp')
    for n, x, y in (('wb_gate', 10, 34), ('wb_hut', 36, 64), ('wb_short', 50, 78), ('fw_rack', 58, 76), ('fw_rack', 30, 60), ('fw_sled', 36, 72),
                    ('fw_fall', 52, 15)):
        if m.free(x, y, STAMPS[n]['w'], STAMPS[n]['h'], on='.dt'): m.stamp(n, x, y)
        else: r.near(n, x, y, on='.t', r=3)
    for x in range(54, 66, 1):
        if m.free(x, 58, 1, 1, on='.'): m.stamp('fw_pal_h', x, 58, mark='B')
    r.dress(trees=('pine2', 'kf_tree', 'pine2'), n_trees=W * H // 260, copses=3, scatter=10)
    r.paint(glint=0.0)
    RW.drifts(m, 0.14, seed=577); RW.road_tracks(m, 0.08, seed=577)
    h = head(577, 'Frostwick Pass', field='SNOWY_MOUNTAIN', bgm='Route 2', weather=['Snow', 20],
             connections=[{'dir': 'S', 'offset': 30, 'to': 566, 'to_offset': 42}, {'dir': 'W', 'offset': 37, 'to': 570, 'to_offset': 23}],
             tone=[-6, -2, 10, 10])
    h['metadata']['BattleBack'] = 'snow'
    r.write(h, '577_frostwick_pass.yaml', '# Frostwick Pass (577). WRITTEN BY layouts/routes_early.py - edit that script.\n', '/tmp/rt/577.png' if PREV else None)


def build_578():
    """Rimewood Path (80x88, SILKWOOD under snow): from Frostwick's North Gate (S) into the Rimewood (N).  Hoar-birch
    outskirts thickening into ice-glazed giants; the frozen brook; the charcoal burners' clearing and kiln; the trapper's
    lean-to (heal); the snare line; honey-stump hives; the woodcutters' log sledge; the Lantern Birch; the Unblazed
    (secret: leave the path at the blue blaze, follow the Stantler tracks to the herd)"""
    W, H = 80, 88
    r = Route(578, W, H, 'snow', base='T', kit='shs')
    m = r.m
    road = [(42, 87), (44, 76), (36, 64), (40, 52), (50, 42), (44, 30), (38, 18), (38, 8), (38, 0)]
    r.road(road, w=3.0, open_=(2, 6))
    r.exit('S', 40, 4); r.exit('N', 36, 4)
    for x in range(W):                                                                 # the frozen brook, west to east
        c = 58 + 2 * (RK.vnoise(x, 0, 578, 12.0) - 0.5) * 2
        for y in range(int(c - 1), int(c + 2)):
            if m.cls[y, x] in 'T.t': m.cls[y, x] = 'p'
    r.clearing(20, 46, 7, 5); r.lane([(40, 50), (24, 46)], w=2.0, open_=(1, 2))     # charcoal burners
    r.clearing(60, 72, 6, 4); r.lane([(44, 74), (58, 72)], w=2.0, open_=(1, 2))     # trapper's lean-to
    r.clearing(62, 20, 6, 5); r.lane([(44, 28), (52, 24), (58, 22)], w=1.6, open_=(1, 2))   # the Unblazed (secret)
    r.clearing(28, 26, 5, 3)
    r.grass(thr=0.58, scale=5.0)
    r.finish_plan(border=0)
    r.add(sign((44, 82), 'Road sign', 'RIMEWOOD PATH -- The Hoar Road. v Frostwick (North Gate) - ^ The Rimewood. Blazes: white is the path. Blue is not.'),
          obj('The Lantern Birch', (42, 34), ['THE LANTERN BIRCH. Trappers hang a light here for whoever is late. Tonight it is out.',
              {'if': 'PBDayNight.isNight? && !pfm?(:lantern_birch)', 'then': ['You relight the lantern. Somewhere down the path, someone laughs with relief.',
                                                                              {'script': 'pbReceiveItem(:NEVERMELTICE)'}, {'script': 'pfm_set(:lantern_birch)'}]}]),
          obj('Charcoal kiln', (20, 44), ["The charcoal burners' kiln, banked and smoking. Warm, for once."]),
          talk('Charcoal burner', (22, 47), 'NPC 03', ['Charcoal burner: Elowen wood, Isenmar fire. Best charcoal in two kingdoms. Neither will admit it.']),
          talk('Trapper', (60, 74), 'NPC 22', ['Trapper: Lean-to\'s yours if you need it. The fire\'s honest.', {'heal': True}]),
          obj('Snare line', (56, 60), ['A snare line along the brook. One snare has caught a very cross Teddiursa.',
              {'if': '!pfm?(:teddiursa_freed)', 'then': ['You loosen the wire. The Teddiursa bolts, then stops, and looks back at you for a long moment.', {'script': 'pfm_set(:teddiursa_freed)'}]}]),
          obj('Honey-stump hives', (30, 70), ['Hives in old stumps, glazed with frost. The Combee inside are slow and very, very offended.']),
          talk('Woodcutter', (46, 62), 'NPC 25', ['Woodcutter: Sledge of logs for Frostwick. Pulling it uphill builds character. Pulling it downhill builds speed.']),
          obj('Blue blaze', (46, 28), ['A blue blaze on a birch. The path is the white ones. This one points off into the trees.']),
          obj('The Unblazed', (62, 18), ['(A clearing where the Stantler herd sleeps standing up. Stantler tracks lead in and out. One stag lowers its antlers at you.)']),
          talk('Stantler', (64, 20), 'Followers/STANTLER', ['(It watches you, unblinking. The herd does not move.)']),
          item((60, 16), 'ICEHEAL'), item((18, 48), 'CHARCOAL'), item((70, 74), 'SUPERPOTION'), hidden((28, 24), 'NEVERMELTICE', 'HiddenItem (birch hollow)'))
    r.seat_events(on='.dtp')
    for n, x, y in (('fw_wood', 18, 48), ('fw_rack', 24, 42), ('fw_sled', 48, 64), ('fw_wood', 50, 64), ('pf_lantern', 44, 32), ('fw_brazier', 58, 70)):
        r.near(n, x, y, on='.td', r=3)
    for n, x, y in (('pf_g_tree4p_ice', 8, 10), ('pf_g_tree2_ice', 64, 40), ('pf_g_tree4p_ice', 14, 66), ('pf_g_tree2_ice', 68, 4)):
        if m.free(x, y, STAMPS[n]['w'], STAMPS[n]['h'], on='.tT'): m.stamp(n, x, y, mark='B', blend=True)
    r.dress(trees=('pine2', 'kf_tree'), n_trees=W * H // 300, copses=0, scatter=10)
    r.paint(glint=0.0)
    RW.rime_silk(m, ((30, 12), (48, 22), (34, 40), (52, 50), (26, 78))) if hasattr(RW, 'rime_silk') else None
    RW.drifts(m, 0.12, seed=578)
    h = head(578, 'Rimewood Path', field='SILKWOOD', bgm='Natural Park', weather=['Snow', 10], biome='forest',
             connections=[{'dir': 'S', 'offset': 40, 'to': 570, 'to_offset': 20}, {'dir': 'N', 'offset': 36, 'to': 562, 'to_offset': 22}],
             tone=[-12, -8, 8, 16])
    h['metadata']['BattleBack'] = 'snow'
    r.write(h, '578_rimewood_path.yaml', '# Rimewood Path (578). WRITTEN BY layouts/routes_early.py - edit that script.\n', '/tmp/rt/578.png' if PREV else None)


def vn_mask(r, thr):
    from terrain import vnoise
    return np.array([[vnoise(x, y, r.seed + 9, 4.0) > thr for x in range(r.W)] for y in range(r.H)])


BUILD = {566: build_566, 577: build_577, 578: build_578, 520: build_520, 521: build_521, 524: build_524, 540: build_540, 541: build_541, 552: build_552, 527: build_527, 528: build_528}


def main():
    ids = [int(a) for a in sys.argv[1:] if a.isdigit()] or sorted(BUILD)
    for i in ids:
        BUILD[i](); print('built', i)


if __name__ == '__main__':
    main()
