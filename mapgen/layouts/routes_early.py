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
    r.sea('W', 9, wobble=3.0, beach=3, deep=4, cliff=1, scale=10.0)
    for y in range(0, 62): m.cls[y, :] = np.where(np.isin(m.cls[y, :], ['w', 'W', 's']), '.', m.cls[y, :]); m.ht[y, :] = np.where(m.ht[y, :] == 1, 0, m.ht[y, :])
    m.ht[62:, :] = np.where(np.isin(m.cls[62:, :], ['w', 'W', 's']), 0, 1)
    m.ht[62:66, :] = np.where(np.isin(m.cls[62:66, :], ['w', 'W', 's']), 0, m.ht[62:66, :])
    r.forest_band('E', 9, wobble=4.0); r.forest_band('N', 4, wobble=2.0)
    for cx, cy, rx, ry in ((52, 30, 6, 5), (8, 14, 6, 5), (46, 92, 7, 6), (54, 70, 5, 6), (10, 46, 5, 4)):
        r.copse(cx, cy, rx, ry)
    # Hale's Bramble: berry terraces climbing east of the lane (h1-h3), each with a stair
    for (x0, x1, y0, y1, h) in ((36, 58, 36, 58, 1), (40, 58, 36, 51, 2), (44, 58, 36, 45, 3)):
        m.ht[y0:y1 + 1, x0:x1 + 1] = np.maximum(m.ht[y0:y1 + 1, x0:x1 + 1], h)
    road = [(15, 109), (15, 101), (19, 93), (24, 85), (22, 77), (22, 72), (27, 62), (31, 52), (28, 41), (33, 29), (31, 16), (31, 0)]
    r.road(road, w=3.0, open_=None)
    r.road([(22, 74), (12, 73), (0, 73)], w=3.0, open_=None)                        # the Hale Bell fork: west to Lacecliff Walk
    r.exit('S', 14, 4); r.exit('N', 30, 4); r.exit('W', 72, 4)
    for (sx, yl) in ((38, 58), (42, 51), (46, 45)):                                  # terrace stairs
        r.crossing(sx, yl, w=2, rows=3)
    r.lane([(32, 56), (38, 61)], w=2.0, open_=None)
    # Minding Hedges (NW), Juno's clearing (S), the sheepfold (NE), the lookout path to the cliff edge
    r.lane([(22, 84), (14, 84), (10, 86)], w=2.0, open_=None)
    r.lane([(26, 60), (16, 62)], w=2.0, open_=None)
    r.lane([(32, 24), (44, 22), (48, 18)], w=2.0, open_=None)
    # the Smuggler's Stair: a pocket on the beach below the toll booth's cliff, behind a bramble (Cut)
    r.pocket(5, 96, 3, 3, gate=None)
    m.ht[93:100, 1:9] = 0; m.cls[93:100, 2:8] = 's'
    r.flatten(8, 10, 92, 1); r.crossing(8, 92, w=3, rows=3)
    r.grass(thr=0.6, scale=6.0)
    r.finish_plan()
    m.cls[86:89, 9:11] = '.'
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
          item((50, 12), 'POKEBALL'), item((8, 50), 'POTION'), hidden((4, 97), 'BIGPEARL', 'HiddenItem (Ferryman\'s Rest)'),
          item((6, 95), 'REVIVE'), obj("The Ferryman's Rest", (3, 95), ["A rowboat hauled up in a sea cave. A name on the bow, painted out. Bootprints, small, going in and not out."]),
          {'type': 'cut_tree', 'at': [9, 88], 'name': 'CutTree'})
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
    h = head(520, "The Ferrymen's Mile", field='MEADOW', bgm='Route 1',
             connections=[{'dir': 'S', 'offset': 10, 'to': 100, 'to_offset': 28}, {'dir': 'N', 'offset': 30, 'to': 521, 'to_offset': 58},
                          {'dir': 'W', 'offset': 72, 'to': 527, 'to_offset': 22}],
             fog={'name': 'prismfall_seamist', 'opacity': 30, 'blend': 0, 'zoom': 200, 'sx': 1, 'sy': 0}, tone=[4, 4, -4, 0])
    r.write(h, '520_ferrymens_mile.yaml', "# The Ferrymen's Mile (520). WRITTEN BY layouts/routes_early.py - edit that script.\n", '/tmp/rt/520.png' if PREV else None)


def vn_mask(r, thr):
    from terrain import vnoise
    return np.array([[vnoise(x, y, r.seed + 9, 4.0) > thr for x in range(r.W)] for y in range(r.H)])


BUILD = {520: build_520, 527: build_527, 528: build_528}


def main():
    ids = [int(a) for a in sys.argv[1:] if a.isdigit()] or sorted(BUILD)
    for i in ids:
        BUILD[i](); print('built', i)


if __name__ == '__main__':
    main()
