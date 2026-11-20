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
    r = Route(527, W, H, 'coast', kit={1: 'ak', 'default': 'ak'})
    m = r.m
    r.sea('S', 13, wobble=3.0, beach=7, deep=5, cliff=1, scale=16.0)
    # the coves: the beach bites into the cliff where the stairs come down
    for cx, cy, rx, ry in ((40, 44, 9, 5), (98, 45, 10, 4)):
        for y in range(H):
            for x in range(W):
                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1.0 and m.ht[y, x] == 1: m.ht[y, x] = 0; m.cls[y, x] = 's'
    road = [(139, 24), (126, 22), (112, 26), (100, 24), (88, 19), (74, 21), (62, 27), (50, 25), (38, 21), (24, 18), (12, 21), (0, 20)]
    r.road(road, w=3.0, open_=(4, 11))
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
    r.dress(trees=('tr_pine', 'tr_pine2', 'tr_oak2'), n_trees=W * H // 260, copses=10, scatter=10, greenfill=None)
    r.paint(glint=0.12)
    flowers(r, 70, 9, 10, 4); flowers(r, 22, 9, 7, 3); flowers(r, 118, 9, 8, 4, p=0.3)
    for x, y in ((20, 55), (60, 56), (120, 54), (84, 58), (8, 52), (132, 57)): water_stamp(r, 'ak_rock2', x, y)
    water_stamp(r, 'ak_boulder', 26, 51)
    for x, y in ((48, 47), (100, 50)): water_stamp(r, 'hb_boat3', x, y)
    h = head(527, 'Lacecliff Walk', field='BEACH', bgm='Route 3', weather=None,
             connections=[{'dir': 'W', 'offset': 18, 'to': 528, 'to_offset': 30}, {'dir': 'E', 'offset': 22, 'to': 520, 'to_offset': 72}],
             tone=[6, 4, -6, 0])
    r.write(h, '527_lacecliff_walk.yaml', '# Lacecliff Walk (527). WRITTEN BY layouts/routes_early.py - edit that script.\n',
            '/tmp/rt/527.png' if PREV else None)


BUILD = {527: build_527}


def main():
    ids = [int(a) for a in sys.argv[1:] if a.isdigit()] or sorted(BUILD)
    for i in ids:
        BUILD[i](); print('built', i)


if __name__ == '__main__':
    main()
