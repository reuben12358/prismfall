#!/usr/bin/env python3
"""routes_craft.py - the crafted Chapter 0-3 roads (map builder 10) on craftkit: elevation with stairs and one-way
ledges, water with a shore, organic tall grass, mixed woods with undergrowth, meadows, and at least two landmarks and
several places with a purpose per map.  Same ids, sizes, connections, crossings and story events as map builder 9's
routes_early.py (whose helpers this module reuses); routes_early.main() dispatches these ids here.

    python3 -I layouts/routes_early.py 527 [--preview]   then   python3 -I build.py --strict"""
import os, sys, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import rkit as K
from rkit import STAMPS
import routekit as RK
from routekit import Route, trainer, npc, sign, item, hidden, talk, head
import craftkit as CK
import routes_early as RE
from routes_early import once, obj, trial, P, old_events, at, line_events, barrier_tile, cave_mouth
from terrain import vnoise
import rcompose as RC
RC_VBASE = RC.VBASE

PREV = RE.PREV
J = lambda e, t: P('JUNO', e, t)


def rock(at_, name='Chalk rubble', text='Chalk rubble from the fallen arch, too heavy to shift by hand.'):
    """a plain solid boulder event (rubble beside a Rock Smash rock)"""
    return {'type': 'event', 'name': name, 'at': list(at_), 'fixed': True,
            'pages': [{'graphic': {'sprite': 'Object rock', 'dir': 'down'}, 'trigger': 'action', 'commands': [text]}]}


def smash(at_):
    return {'type': 'rock_smash', 'at': list(at_), 'name': 'Rock', 'fixed': True}


def colmap(r, f):
    """per-column profile f(x) -> int"""
    return [int(round(f(x))) for x in range(r.W)]


def bump(x, c, half, depth):
    """a smooth bump of `depth` centred on c, half-width `half` (0 outside)"""
    t = (x - c) / float(half)
    return depth * max(0.0, 1 - t * t) if abs(t) < 1 else 0.0


# ====================================================================================================== 527 Lacecliff Walk
def build_527():
    """Lacecliff Walk (140x64, BEACH): white chalk cliffs over the sea.  The cliff path weaves through two Lace Arches
    (south through the first onto the cliff edge, north through the second); the third arch fell long ago and its rubble
    (Rock Smash) blocks the old way up onto the West Down, whose chalk ledges drop back to the road (one-way, the
    shortcut home).  East: the high down (stairs) with the dew pond, the smugglers' signal pole and the hidden field of
    sea-pinks.  South: the Wrecker's Lamp headland with the hermit's hut; the Lacemakers' Bench headland; two coves down
    chalk stairs (rock pools, wet sand, a tide line, the fishers' camp, a beached rowboat); the Lost Thread pocket beach
    (night tide-rock, secret).  The sea: a Wingull stack, two sea arches, rocks in the shallows, kelp."""
    W, H = 140, 64
    r = Route(527, W, H, 'shore', kit={1: 'akc', 2: 'akc', 'default': 'akc'}, base='.')
    m = r.m
    m.ht[:, :] = 1
    # ---- the coast: the cliff lip per column (headlands push it south, coves pull it north)
    def lip(x):
        y = 42 + 2.5 * (vnoise(x, 0, 527, 9.0) - 0.5) * 2
        y += bump(x, 118, 9, 11) + bump(x, 57, 8, 6) + bump(x, 8, 7, 3)
        y -= bump(x, 91, 10, 3) + bump(x, 32, 11, 4)
        return y
    yl = colmap(r, lip)
    coves = {'B': (81, 101, 9), 'A': (21, 43, 8), 'L': (66, 76, 5)}           # x0, x1, beach depth
    for x in range(W):
        sea0 = yl[x] + 1
        beach = 0
        for k, (a, b, dep) in coves.items():
            if a <= x <= b: beach = int(round(dep * (1 - ((x - (a + b) / 2) / ((b - a) / 2 + 1)) ** 2)) + 1)
        deep = sea0 + beach + 6 + int(3 * vnoise(x, 1, 528, 7.0))
        for y in range(sea0, H):
            m.ht[y, x] = 0
            m.cls[y, x] = 's' if y < sea0 + 2 + beach and beach else ('W' if y >= deep else 'w')
    CK.smooth_sea(m, 3)
    # the pocket beach of the Lost Thread is cut off from cove B by a tide-rock neck
    neck = max(yl[x] for x in range(77, 81)) + 3
    for x in range(77, 81):
        for y in range(yl[x] + 1, H):
            if m.cls[y, x] == 's': m.cls[y, x] = 'w'
        m.cls[neck, x] = 's'
    for x in (74, 75, 76, 81, 82, 83):                    # the neck meets both beaches
        if m.cls[neck, x] in 'wW': m.cls[neck, x] = 's'
    # ---- the high down (east, h2) with its dew pond; the West Down (h1, behind ledges)
    for x in range(88, W):
        yd = 11 + 2.2 * (vnoise(x, 3, 529, 8.0) - 0.5) * 2 + bump(x, 92, 6, -3)
        for y in range(0, int(yd) + 1): m.ht[y, x] = 2
    CK.smooth_ht(m, 2, 2, box=(84, 0, W, 20))
    r.forest_band('N', 6, wobble=2.5)
    for cx, cy, rx, ry in ((132, 6, 6, 3), (20, 5, 8, 3), (60, 4, 9, 3), (5, 31, 4, 5), (136, 30, 4, 6), (49, 37, 4, 2.5),
                           (86, 26, 3.5, 2.2), (109, 31, 3, 2.5), (100, 41, 2.5, 2), (35, 33, 3, 2), (24, 30, 2.5, 2), (74, 12, 5, 3), (84, 12, 3, 2.5)):
        r.copse(cx, cy, rx, ry)
    # ---- the road (chalky sand lane), weaving through arch A (south) and arch B (north)
    AX, BX = 101, 75                                  # arch stamps: walkable columns ax+2..ax+4, rows ay..ay+4
    AY, BY = 25, 26
    road = [(139, 23.5), (131, 23), (124, 21), (114, 20), (107, 21), (104, 23), (104, 30), (104, 33), (99, 35), (90, 34),
            (84, 35), (78, 33), (78, 29), (78, 23), (73, 20), (66, 22), (58, 24), (50, 23), (42, 20), (34, 21), (26, 24), (17, 24), (9, 21), (0, 19.5)]
    r.road(road, w=3.0, c='u', open_=None, only='.tT')
    r.exit('E', 22, 4); r.exit('W', 18, 4)
    for y in range(H):                                 # straight through the arches
        for x in (AX + 2, AX + 3, AX + 4):
            if AY - 2 <= y <= AY + 6: m.cls[y, x] = 'u'
        for x in (BX + 2, BX + 3, BX + 4):
            if BY - 2 <= y <= BY + 6: m.cls[y, x] = 'u'
    # side paths: the Lamp headland, the Bench headland, the stairs up the high down, cove stairs
    r.lane([(118, 21), (119, 30), (118, 40), (118, 47)], w=2.0, c='u', open_=None)
    r.lane([(57, 22), (57, 32), (57, 41)], w=2.0, c='u', open_=None)
    for (sx, x0) in ((125, 124), (96, 95)):                              # stairs up onto the high down
        yy = max(y for y in range(H) if m.ht[y, sx] == 2)
        CK.stair(r, x0, yy, w=3, h=2)
        r.lane([(x0 + 1, yy + 3), (x0 + 1, yy + 6)], w=2.0, c='u', open_=None)
    for cx in (91, 32):                                                  # chalk stairs down to the coves
        CK.stair(r, cx - 1, yl[cx], w=3, h=1)
        r.lane([(cx, 34), (cx, yl[cx])], w=2.0, c='u', open_=None)
    # the dew pond on the high down
    CK.pond(r, 113, 6, 5.0, 3.0, c='p', rough=0.25)
    # ---- the West Down's ledges (one-way, jump south onto the road heath) and the fallen third arch
    CX, CY = 41, 11
    for x in range(0, 70):
        for y in range(0, 16):
            if m.cls[y, x] == 'u' and y < 15: m.cls[y, x] = '.'
    r.finish_plan(border=0)
    for x in range(63, 72):                              # the down's east end closes in woods
        for y in range(0, 16): m.cls[y, x] = 'T' if m.cls[y, x] in '.tu' else m.cls[y, x]
    CK.ledge(r, 6, 40, 15, chalk=True); CK.ledge(r, 48, 62, 14, chalk=True)
    # tall grass: organic patches on the heath, the downs and the headlands
    CK.grass_fields(r, [(14, 27, 4), (30, 28, 3.5), (47, 30, 4), (66, 30, 3), (86, 27, 3), (128, 30, 4), (112, 32, 3),
                        (20, 9, 4), (36, 8, 3), (54, 9, 3.5), (122, 8, 3), (100, 9, 2.5), (8, 25, 2.5), (60, 37, 2.5), (114, 42, 2.5),
                        (94, 30, 2.5), (40, 36, 2.5), (22, 36, 2.5), (72, 36, 2), (132, 9, 2.5), (82, 15, 3), (46, 18, 2), (106, 38, 2)])
    # earth: worn chalky patches beside the road and on the headlands
    CK.earth(r, [(110, 24, 3, 1.5), (70, 22, 2.5, 1.2), (26, 25, 3, 1.2), (118, 44, 2.5, 2), (57, 38, 2, 2), (88, 31, 2, 1)])
    CK.woods(r, CK.COAST, scale=11.0)
    # ---- landmarks
    m.stamp('pf_lacearch', AX, AY, mark='B'); m.stamp('pf_lacearch', BX, BY, mark='B')
    m.stamp('pf_lacearch', CX, CY, mark='B')
    for n, x, y, on in (('pf_wlamp', 120, 47, '.t'), ('pf_sigpole', 104, 3, '.t'), ('pf_stonebench', 55, 42, '.t'),
                        ('pf_roadstone', 128, 26, '.t'), ('gl_shed', 111, 37, '.t')):
        r.near(n, x, y, on=on, r=4)
    # ---- events (map builder 9's, re-seated)
    arches = [(AX + 3, AY + 4), (BX + 3, BY + 4)]
    r.add(sign((136, 21), 'Road sign', "LACECLIFF WALK - The Strand Road. -> The Ferrymen's Mile - <- Marram Down & Saltmere.\nThe arches are older than the Accord. Please do not improve them."),
          once('The Lace Arches', arches[0], ['(Chalk cliffs worn by the sea into arches as fine as lace. The path goes through three of them. Well -- two and a half.)',
               J('happy', 'The Briarwick weavers copy these cliffs for their lace. Not the other way round. The sea did it first.'),
               J('happy', "The sea does most things first. It's very annoying of it.")]),
          trainer((93, 46), 'FISHERMAN', 'Bryn', "The strait's closed and the fish haven't been told.", 'The fish win again.', d='left'),
          trainer((38, 44), 'PICNICKER', 'Moll', "I found a bottle with a letter in it! It's from my sister. She lives forty yards that way.",
                  "She writes every week. She's never once walked over.", d='right'),
          trainer((30, 9), 'HIKER', 'Dunstan', "Cliff path in a gale's a fine way to die. Cliff path in sun's a fine way to live.", "Today's a sun day. Lucky you.", d='down'),
          talk('Lass on the heath', (112, 28), 'NPC 16', ["Lass: The Wrecker's Lamp? It's only for the gulls. Everyone says so. Everyone says it a bit fast."]),
          talk('Painter at an easel', (59, 40), 'NPC 18', ["Painter: Hold still. No -- you're in the light. No -- you ARE the light.",
               "Painter: Hm. You don't really show up on the canvas, do you? Odd."]),
          talk('Hermit at the Wrecker\'s Lamp', (120, 45), 'NPC 26', ["Hermit: It's for the gulls. The lamp. Not for ships.",
               "Hermit: I don't know anything about ships. Who said ships?"]),
          obj("Wrecker's Lamp", (118, 48), ["A lamp on a tall pole at the very tip of the headland, trimmed and full. It faces the sea, where the rocks are."]),
          talk('Birder', (108, 7), 'NPC 09', ["Birder: Wingull nest on that stack. Two hundred of them. I've named eleven. The rest won't hold still."]),
          obj("Smugglers' signal pole", (104, 6), ["A tall pole with a lantern hook. From here you can see the Ferrow lighthouse.",
               "Its beam sweeps past, then stops on you for a second longer than it should, then moves on."]),
          obj('Dew pond', (112, 9), ['A dew pond, lined with chalk and clay by shepherds long gone. It never quite dries. The Wingull drink here and argue.']),
          obj('Road Stone I-b', (129, 27), ['ROAD STONE I-b. THE STRAND ROAD. "Ferrow 2, Saltmere 6." Someone has chalked a seventh mile on, for the arches.']),
          {'type': 'event', 'name': "Lacemakers' Bench", 'at': [57, 41], 'pages': [{'trigger': 'action', 'commands': [
              J('happy', "Sit! You have to sit! It's the Lacemakers' Bench. Everyone who walks the Strand sits here or the cliffs fall in."),
              {'choices': ['Is that true?', '(Sit.)'], 'cancel': 1, 'branches': [
                  [J('deadpan', "No. But they haven't fallen in, have they.")],
                  ['(You sit. Juno sits. A Wingull lands on the end of the bench. Nobody says anything for a while. The sea does most of the talking.)',
                   J('neutral', "...This is nice. I don't get to sit. I'm always going somewhere with a basket."),
                   J('happy', "Right! That's enough nice! Saltmere!"), {'heal': True}]]}]}]},
          obj('The fallen arch', (CX + 3, CY + 4), ['(The third arch. Its span fell in a winter storm before anyone alive was born, and took the old way up onto the down with it.)']),
          rock((CX + 2, CY + 3)), smash((CX + 3, CY + 3)), rock((CX + 4, CY + 3)),
          hidden((CX + 3, CY + 1), 'PEARL', 'HiddenItem (third arch)'),
          obj('Sea-pinks', (22, 4), ['(A hollow on the down, hidden by gorse: a whole field of sea-pinks. On clear mornings, they say, the Flabebe come to dance here.)']),
          item((121, 41), 'POTION'), item((14, 5), 'POKEBALL'), item((97, 48), 'SUPERPOTION'), hidden((126, 6), 'NUGGET', 'HiddenItem (high down)'), item((68, 33), 'ETHER'),
          trial('Dobbs the shell-gatherer', (28, 45), 'DOBBS', 'NPC 27', d='down'),
          talk('Fisher at the camp', (36, 46), 'NPC 25', ["Fisher: The cove's ours till the tide says otherwise. Sit by the fire. Mind the crab, he's ours as well."]),
          {'type': 'event', 'name': 'Tide-rock', 'at': [78, neck], 'fixed': True, 'pages': [
              {'graphic': {'sprite': 'Object rock', 'dir': 'down'}, 'trigger': 'action', 'commands': [
                  {'if': 'PBDayNight.isNight?', 'then': ['The tide is out. The rock stands in a dry hollow now, and you can squeeze past it.', {'selfswitch': ['A', True]}],
                   'else': ['The sea fills the gap behind this rock. At low tide, maybe.']}]},
              {'cond': {'self': 'A'}, 'commands': []}]},
          obj('Drowned sample-book', (71, yl[71] + 3), ['A weaver\'s sample-book, swollen with seawater. Every page is a lace pattern copied from these cliffs.',
              'On the last page, in a different hand: "Found the Thread. Going home by the forest road." It is dated the winter the road closed.']),
          hidden((73, yl[73] + 3), 'SHELLBELL', 'HiddenItem (the Lost Thread)'))
    r.seat_events(on='.dtsu')
    # ---- the coves' purpose: the fishers' camp (cove A), rock pools, a beached rowboat; nets and posts in cove B
    for n, x, y in (('sh_campfire', 34, 43), ('hb_rope', 40, 42), ('hb_plank', 26, 43), ('hb_post1', 30, 42), ('hb_boxes', 88, 43), ('hb_barrel', 99, 44), ('hb_rope', 95, 45)):
        r.near(n, x, y, on='s', r=3)
    CK.rock_pools(r, [(23, 45, 'a'), (41, 46, 'b'), (84, 46, 'a'), (97, 44, 'b'), (69, yl[69] + 2, 'b')])
    # the West Down: gorse (shrubs) round the sea-pink hollow, standing stones on the crest
    for (x, y) in ((16, 3), (27, 3), (15, 7), (28, 7), (21, 9)):
        r.near('nt_shrub1', x, y, on='.', r=2)
    CK.props(r, ['nr_col'], 3, box=(44, 3, 60, 9), clump=3, seed=5)
    # chalk outcrops and boulders on the heath and the cliff tops
    for (x, y) in ((66, 31), (14, 32), (126, 33), (44, 30), (90, 26), (106, 12), (30, 11)):
        r.near('ck_rock_big', x, y, on='.t', r=3)
    CK.props(r, ['ck_boulder', 'ck_pebbles', 'ck_boulder', 'nt_rocks_s0'], 34, box=(0, 22, W, 44), clump=4, seed=7)
    CK.props(r, ['ck_pebbles', 'ck_boulder'], 10, box=(88, 0, W, 14), clump=3, seed=8)
    CK.props(r, ['ck_pebbles', 'ck_boulder'], 10, box=(0, 0, 64, 14), clump=3, seed=9)
    for (x, y) in ((107, 5), (119, 4), (108, 8), (119, 9)):
        r.near('nt_reed1', x, y, on='.', r=2)
    # gorse hedgerows along the road's seaward side, with gaps (the heath is broken into fields, not one lawn)
    rng = random.Random(527)
    for x in range(2, 136):
        ys = [y for y in range(16, 40) if r.road_mask[y, x]]
        if not ys or vnoise(x, 0, 5270, 6.0) < 0.42: continue
        y = max(ys) + 2
        if m.free(x, y, 1, 1, on='.') and not m.cliff[y, x] and rng.random() < 0.8:
            m.stamp(rng.choice(['nt_bush0', 'nt_bush1', 'nt_fern0', 'nt_bush1']), x, y, mark='B')
    # trees: a wind-bent fringe of coast pines and teal oaks in front of the woods and copses; undergrowth
    CK.fringe(r, CK.FRINGE['coast'], 150, seed=1, near_forest=4)
    CK.fringe(r, ['nt_pine_a', 'nt_pine_b', 'nt_dpine_sh'], 10, box=(0, 24, W, 40), seed=2, near_forest=0)
    CK.undergrowth(r, 220, seed=3)
    r.dress(trees=('nt_pine_a',), n_trees=0, copses=0, scatter=0)
    r.paint(glint=0.4)
    CK.paint_extras(r)
    for n, x, y in (('pf_seastack', 50, 53), ('pf_seastack2', 131, 54), ('pf_seaarch', 11, 52), ('pf_seaarch', 100, 55),
                    ('pf_seastack2', 76, 53), ('pf_seastack', 22, 57), ('pf_seastack2', 64, 58), ('hb_boat3', 34, 50)):
        if not CK.water_stamp(r, n, x, y): print('  (no water for %s at %d,%d)' % (n, x, y))
    CK.shore(r, wet=1, wet_noise=0.45, wrack=0.6)
    # meadows: the sea-pinks hollow (the secret), thrift along the cliff tops, clover and buttercups on the downs
    pinks = [K.DECOR_SH['flowers'][i] for i in (2, 3)]
    CK.meadow(r, 22, 5, 6, 2.5, tiles=pinks, p=0.95, seed=1)
    CK.meadow(r, 66, 38, 5, 2, tiles=pinks, p=0.6, seed=2); CK.meadow(r, 125, 38, 5, 3, tiles=pinks, p=0.6, seed=3)
    CK.meadow(r, 46, 9, 5, 2, p=0.6, seed=4); CK.meadow(r, 118, 9, 6, 2.5, p=0.6, seed=5); CK.meadow(r, 8, 28, 4, 2, p=0.5, seed=6)
    CK.meadow(r, 84, 22, 4, 2, p=0.5, seed=7)
    CK.scatter_quiet(r, 8)
    h = head(527, 'Lacecliff Walk', field='BEACH', bgm='Route 3', weather=None,
             connections=[{'dir': 'W', 'offset': 18, 'to': 528, 'to_offset': 30}, {'dir': 'E', 'offset': 22, 'to': 520, 'to_offset': 72}],
             tone=[6, 4, -6, 0])
    h['walk_from'] = [[72, yl[72] + 3]]                                     # the Lost Thread pocket (past the night tide-rock)
    r.write(h, '527_lacecliff_walk.yaml', '# Lacecliff Walk (527). WRITTEN BY layouts/routes_craft.py - edit that script.\n',
            '/tmp/rt/527.png' if PREV else None)


BUILD = {527: build_527}


# ====================================================================================================== 528 Marram Down
def build_528():
    """Marram Down (110x80, BEACH): dune-down held by marram grass, in terraces.  The road winds through the slack
    between the dune belt (north, three levels to the Saltmere Beacon on the highest dune: heals once, the first view
    of the port) and the foredune ridge over the beach.  The sledge run slides from the Beacon to the shore (a real
    slide: one way, down).  In a dune hollow, the players' camp of wagons rehearsing; the theatre barge half-buried in
    the foredune (the Prompter's Box); the bird hide over the brackish pool (Old Rod); marram ledges drop from the
    slack to the camp (one way); the toll-free stile into Saltmere with the Free Port charter stone."""
    W, H = 110, 80
    r = Route(528, W, H, 'shore', kit={1: 'akd', 2: 'akd', 3: 'akd', 'default': 'akd'}, base='.')
    m = r.m
    # ---- the sea, the beach and the foredune ridge (h1)
    for x in range(W):
        sea = 67 + 2.0 * (vnoise(x, 0, 5281, 10.0) - 0.5) * 2 + bump(x, 20, 10, 2) - bump(x, 70, 12, 2)
        fd = 54 + 1.6 * (vnoise(x, 1, 5282, 14.0) - 0.5) * 2 + bump(x, 28, 7, 3) + bump(x, 92, 8, 2)
        for y in range(H):
            if y >= sea: m.cls[y, x] = 'W' if y >= sea + 6 + 2 * vnoise(x, 2, 5283, 6.0) else 'w'
            elif y >= fd + 3: m.cls[y, x] = 's'
        for y in range(int(fd) - 5, int(fd) + 1):
            if 0 <= y < H: m.ht[y, x] = 1
    CK.smooth_sea(m, 3)
    # ---- the dune belt (north): three levels up to the Beacon
    for x in range(W):
        d1 = 26 + 2.0 * (vnoise(x, 4, 5285, 14.0) - 0.5) * 2 - bump(x, 14, 9, 6) - bump(x, 100, 8, 5)
        d2 = 18 + 1.6 * (vnoise(x, 5, 5286, 14.0) - 0.5) * 2 - bump(x, 20, 12, 8) - bump(x, 96, 12, 6)
        for y in range(H):
            if y <= d1: m.ht[y, x] = max(m.ht[y, x], 1)
            if y <= d2: m.ht[y, x] = max(m.ht[y, x], 2)
    CK.plateau(r, 55, 10, 9, 5, 3, rough=0.35, seed=1)
    for h in (1, 2): CK.smooth_ht(m, h, 4)
    CK.smooth_ht(m, 3, 2, box=(40, 0, 72, 20))
    # ---- sand: dune tops and slopes are bare sand (the Dirt autotile), slacks are grass
    for i, (cx, cy, rx, ry) in enumerate(((55, 10, 10, 6), (36, 18, 9, 4), (76, 17, 8, 4), (20, 26, 7, 3), (92, 24, 8, 3),
                                          (48, 26, 6, 2.5), (64, 46, 6, 3), (40, 50, 9, 3), (86, 52, 9, 3), (14, 52, 7, 3),
                                          (102, 40, 5, 4), (30, 40, 5, 3))):
        m.blob(cx, cy, rx, ry, 'u', seed=5300 + i, rough=0.75, only='.')
    # ---- the road through the slack, the stairs up the belt, the beach path through the foredune
    road = [(109, 31.5), (100, 33), (90, 36), (80, 34), (70, 36), (58, 38), (46, 36), (34, 37), (22, 40), (12, 39), (0, 39.5)]
    r.road(road, w=3.0, c='d', open_=None, only='.tTu')
    r.exit('E', 30, 4); r.exit('W', 38, 4)
    for x0, h in ((61, 1), (57, 2), (53, 3)):
        yy = max(y for y in range(H) if m.ht[y, x0 + 1] == h)
        CK.stair(r, x0, yy, w=3, h=h)
    r.lane([(62, 36), (62, 30), (58, 26), (58, 21), (54, 17)], w=2.0, c='d', open_=None, only='.tTu')
    r.lane([(98, 33), (99, 26), (96, 22)], w=2.0, c='d', open_=None, only='.tTu')       # to the bird hide
    yy = max(y for y in range(H) if m.ht[y, 99] == 1); CK.stair(r, 98, yy, w=3, h=1)
    for x0 in (29, 84):                                                                 # down through the foredune to the beach
        yy = max(y for y in range(H) if m.ht[y, x0 + 1] == 1)
        CK.stair(r, x0, yy, w=3, h=1)
    r.lane([(30, 38), (30, 46)], w=2.0, c='d', open_=None, only='.tTu')
    r.lane([(85, 36), (85, 47)], w=2.0, c='d', open_=None, only='.tTu')
    # the brackish pool and the bird hide (on the belt, north-east)
    CK.pond(r, 96, 15, 5.5, 2.6, c='p', rough=0.3)
    # the players' camp: a trodden hollow in the slack south of the road
    m.blob(72, 44, 7, 3.2, 'd', seed=44, rough=0.45, only='.tu')
    r.finish_plan(border=0)
    r.forest_band('N', 3, wobble=1.5)
    for cx, cy, rx, ry in ((8, 6, 7, 4), (104, 6, 6, 4), (30, 8, 5, 3), (84, 8, 5, 3), (4, 30, 3, 6), (106, 46, 3, 5),
                           (40, 44, 4, 2.5), (20, 30, 3, 2), (86, 28, 3, 2.5), (104, 20, 3, 3), (12, 48, 3, 2), (72, 12, 4, 3), (40, 12, 4, 3), (26, 46, 3, 2)):
        r.copse(cx, cy, rx, ry)
    # marram ledges: from the slack south of the road, one way down to the camp's hollow
    CK.ledge(r, 44, 60, 41, face='dune'); CK.ledge(r, 88, 96, 42, face='dune')
    for y in (40, 41, 42):
        for x in (43, 61, 87, 97):
            if m.cls[y, x] in '.tu': m.cls[y, x] = 'T'
    # marram tall grass in the slacks and hollows
    CK.grass_fields(r, [(12, 33, 4), (26, 33, 3), (40, 30, 3.5), (76, 28, 3), (88, 30, 3), (104, 36, 3), (50, 46, 3.5),
                        (18, 46, 4), (96, 46, 3), (60, 50, 2.5), (36, 22, 3), (72, 20, 3), (88, 20, 2.5), (22, 18, 3),
                        (46, 8, 2.5), (66, 6, 2.5), (8, 44, 3), (78, 50, 2.5)])
    CK.woods(r, CK.COAST, scale=10.0)
    # ---- events
    SLIDE = 'mr_sledge'
    def slide_page(n):
        return [{'trigger': 'action', 'commands': [
            '(A waxed sledge at the top of the run. The sand drops away to the sea.)',
            {'choices': ['Ride it down!', 'Not today.'], 'cancel': 1, 'branches': [
                [{'move': {'who': -1, 'route': ['turn_down', 'dir_fix_on', 'through_on', {'speed': 5}, 'down %d' % n,
                                                {'speed': 4}, 'through_off', 'dir_fix_off']}},
                 {'se': 'Slots stop'}, {'script': 'pfm_add(:sledge_runs, 1) rescue nil'},
                 '(Nine seconds, maybe ten. The record is seven, and a broken arm.)'],
                ["(You'd need a running start. And a will.)"]]}]}]
    bx = 52
    top_y = max(y for y in range(H) if m.ht[y, bx] == 3) - 1
    land_y = min(y for y in range(H) if m.cls[y, bx] in 'wW') - 3
    r.chute = (bx, top_y + 1, land_y)
    r.add(sign((105, 29), 'Road sign', 'MARRAM DOWN - Free Port of Saltmere, 1 mile. Pulling up the marram grass is fined. Yes, even that one.'),
          obj('Free Port charter stone', (4, 36), ['FREE PORT CHARTER STONE: "By grant of Sovereign Maren, AF 41: SALTMERE ANSWERS TO THE ACCORD AND TO NO CROWN."',
              'Someone has carved underneath, smaller: "AND BOOS THE REST."']),
          obj('The stile', (2, 42), ['A toll-free stile into Saltmere. A painted board: "FREE PORT. NO TOLL. NO KINGS. MIND THE STEP."']),
          once('The Saltmere Beacon', (55, 9), ['(From the top of the dune, the free port opens below: a white town on a salt lake, striped awnings, lantern masts, and a theater on every second corner.)',
               J('happy', "Saltmere! Look at it! Everything's ordinary! Isn't it WONDERFUL?"),
               J('happy', "The Blank Plate's under there somewhere. Nothing strange ever happens in Saltmere. No Bleed, no glowing rivers, nothing."),
               J('happy', 'So they make it all up instead. Every night. On purpose.')]),
          {'type': 'event', 'name': 'Beacon Keeper', 'at': [58, 9], 'pages': [
              {'graphic': {'sprite': 'NPC 26', 'dir': 'down'}, 'trigger': 'action', 'commands': [
                  "Beacon Keeper: Tea? It's not kelp. I've heard about the kelp.", {'heal': True}, '(The party is rested.)', {'selfswitch': ['A', True]}]},
              {'cond': {'self': 'A'}, 'graphic': {'sprite': 'NPC 26', 'dir': 'down'}, 'trigger': 'action', 'commands': [
                  'Beacon Keeper: The pot\'s cold. Come back when I\'ve forgotten you.']}]},
          {'type': 'event', 'name': 'Sledge run', 'at': [bx, top_y], 'fixed': True, 'pages': slide_page(land_y - top_y)},
          obj('Sledge run sign', (bx + 2, top_y), ['THE SLEDGE RUN. Down the Beacon to the shore in nine seconds. The record is seven, and a broken arm.',
              'One way only. The sand does not go back up, and neither do you.']),
          talk('Sledge boy', (bx + 1, land_y + 1), 'NPC 05', ["Sledge boy: You came down the run? Leave the sledge, I drag them back up. Two coppers a drag. ...Fine. Free. This once."]),
          talk('Hound Number One', (68, 44), 'NPC 03', ['Hound Number One: And SO the Loyal Three drove the Gossamer Ogre from the wood--']),
          talk('Ogre', (71, 43), 'NPC 25', ["Ogre: (muffled) Can I take the mask off? It's very hot in the Ogre.", 'Ogre: (muffled) Why does he look so sad, though? He\'s the villain.'], move='random'),
          talk('Director with script', (75, 44), 'NPC 18', ['Director: The Ogre does NOT take the mask off. The Ogre has never taken the mask off. It\'s in the text.',
               'Director: Because the carver was having a bad week in AF 140! Places!']),
          trainer((73, 41), 'JUGGLER', 'Hounds', 'A rehearsal audience! Quick, a scene!', 'Notes: we were bitten. Again.', d='down', double=True),
          talk('Prop-mistress', (66, 46), 'NPC 27', ["Prop-mistress: If you're digging in the old barge, there's a shovel by the wagon.",
               "Prop-mistress: The prompter's box went down with it in '71. Nobody's had the heart.",
               {'if': '!pfm_has?(:SANDSHOVEL)', 'then': [{'script': 'pfm_item(:SANDSHOVEL, 1, "Sand Shovel")'}]}]),
          {'type': 'event', 'name': "The Prompter's Box", 'at': [24, 61], 'pages': [{'trigger': 'action', 'commands': [
              {'if': 'pfm?(:sm_prompter)', 'then': ['Only sand now. The barge has given up its secret.'],
               'else': [{'if': 'pfm_has?(:SANDSHOVEL)', 'then': [
                   '(A theater barge lies half-buried in the dune, its name board reading THE WANDERING CHORUS.)', 'You dig at the stern with the shovel...',
                   {'script': 'pfm_item(:PROMPTERSSCRIPT, 1, "Prompter\'s Script")'}, {'script': 'pfm_item(:NORMALGEM, 1, "Normal Gem")'},
                   {'script': 'pfm_set(:sm_prompter)'}],
                   'else': ['(A theater barge lies half-buried in the dune. Costume hampers. A prop throne with three legs.)',
                            'Something square is buried at the stern. You\'d need a shovel.']}]}]}]},
          trainer((92, 26), 'BIRDKEEPER', 'Lark', "Wind off the lake's the best in Elowen.", 'My kite won. You beat the kite-flier, which is different.', d='left'),
          trainer((10, 40), 'POKEMONRANGER_F', 'Sedge', "Free port starts at the stile. Past that, the Queen's writ doesn't run, and neither do I.",
                  "I'm going to sit down now. That's allowed in a free port.", d='right'),
          talk('Sand-sculptor', (44, 63), 'NPC 15', ["Sand-sculptor: It's the Sovereign's Crown! In sand!", "Sand-sculptor: ...Don't look at the stone. I ran out of the good sand."]),
          talk('Birdwatcher', (93, 18), 'NPC 09', ['Birdwatcher: Brackish pool. Half sea, half rain. The Wingull come to wash the salt off. Shh.']),
          hidden((bx - 1, land_y), 'SOFTSAND', 'HiddenItem (sledge run)'),
          item((8, 64), 'POTION'), item((101, 18), 'GREATBALL'), item((24, 24), 'REPEL'), item((36, 15), 'ESCAPEROPE'), hidden((70, 4), 'STARDUST', 'HiddenItem (dune crest)'))
    ship_part_sand(r, -24, 10, 53)                                                   # the Wandering Chorus, half-buried
    # keep the chute clear: nothing may stand on the slide column
    for y in range(top_y, land_y + 1):
        m.taken[y, bx] = True
    r.seat_events(on='.dtus')
    # ---- the camp's purpose: wagons (stalls), the fire, the washing line, the props barrels, the morris column
    for n, x, y in (('pf_stall4', 64, 41), ('pf_stall2', 77, 41), ('pf_stall0', 79, 45), ('sh_campfire', 70, 45),
                    ('hb_washline', 66, 48), ('hb_tables', 75, 47), ('hb_barrels', 81, 43), ('pf_morris', 63, 44)):
        r.near(n, x, y, on='d.u', r=3)
    r.near('gl_shed', 99, 17, on='.u', r=4)                                          # the bird hide
    r.near('pf_beacon', 54, 5, on='.u', r=3)                                         # the Saltmere Beacon
    r.near('pf_sledge', bx + 1, top_y - 1, on='.u', r=2)
    r.near('pf_roadstone', 5, 34, on='.u', r=3)
    m.fence(0, 6, 43, gaps=((2, 2),)); m.fence(0, 6, 34)
    # dune rocks, driftwood, pebbles; reeds round the brackish pool
    CK.props(r, ['dk_boulder', 'dk_pebbles', 'dk_boulder', 'nt_log'], 30, box=(0, 12, W, 60), clump=4, seed=7)
    for (x, y) in ((40, 26), (82, 22), (16, 48), (100, 50), (48, 14)):
        r.near('dk_rock_big', x, y, on='.ut', r=3)
    for (x, y) in ((90, 14), (101, 14), (91, 17), (102, 16), (95, 18)):
        r.near('nt_reed1', x, y, on='.u', r=2)
    CK.fringe(r, CK.FRINGE['coast'], 200, seed=1, near_forest=6)
    CK.fringe(r, ['nt_pine_a', 'nt_pine_b', 'nt_dpine_sh', 'nt_teal_a'], 40, box=(0, 12, W, 56), seed=2, near_forest=0)
    CK.props(r, ['nt_log', 'dk_boulder', 'dk_pebbles', 'nt_log'], 16, box=(0, 56, W, 68), on='s', clump=3, seed=11)
    CK.props(r, ['nt_reed1', 'nt_reed1', 'nt_fern1'], 26, box=(0, 55, W, 62), on='s', clump=2, seed=12)
    CK.undergrowth(r, 160, kinds=('nt_fern0', 'nt_fern1', 'nt_bush0', 'nt_bush1', 'ak_fern', 'nt_reed1'), seed=3)
    r.dress(trees=('nt_pine_a',), n_trees=0, copses=0, scatter=0)
    r.paint(glint=0.35)
    ship_part_sand(r, -24, 10, 53, draw=True)
    CK.paint_extras(r)
    for y in range(top_y + 1, land_y + 1):                                           # the polished chute (walkable decal)
        if m.cls[y, bx] in '.ust' and not m.cliff[y, bx] and m.L[2, y, bx] == 0: m.L[2, y, bx] = K.P1('mr_chute%d' % (y % 2))
    for n, x, y in (('dk_rock_big', 60, 73), ('hb_boat2', 94, 70), ('dk_rock_big', 12, 72), ('dk_boulder', 34, 71), ('dk_boulder', 80, 72)):
        CK.water_stamp(r, n, x, y)
    CK.shore(r, wet=1, wet_noise=0.45, wrack=0.7, chalk_rocks=False)
    sea_pinks = [K.DECOR_SH['flowers'][i] for i in (2, 3)]
    for i, (cx, cy, rx, ry) in enumerate(((26, 30, 5, 2), (84, 36, 4, 2), (46, 20, 4, 2), (100, 28, 3, 2), (14, 36, 3, 2), (70, 26, 4, 2))):
        CK.meadow(r, cx, cy, rx, ry, p=0.65, seed=i)
    CK.meadow(r, 36, 57, 6, 1.6, tiles=sea_pinks, p=0.6, seed=9)
    CK.scatter_quiet(r, 8)
    h = head(528, 'Marram Down', field='BEACH', bgm='Route 3',
             connections=[{'dir': 'E', 'offset': 30, 'to': 527, 'to_offset': 18}, {'dir': 'W', 'offset': 38, 'to': 140, 'to_offset': 44}],
             tone=[8, 4, -8, 0])
    r.write(h, '528_marram_down.yaml', '# Marram Down (528). WRITTEN BY layouts/routes_craft.py - edit that script.\n', '/tmp/rt/528.png' if PREV else None)


def ship_part_sand(r, dx, dy, max_row, draw=False):
    """the moored two-master's hull (rows up to max_row) laid on the sand: a wreck half-buried on the beach.  Call once
    at plan time (marks the hull solid so nothing is seated under it) and once after painting with draw=True (the
    ground autotile moves down a layer so the sand shows through the hull's gaps)"""
    m = r.m
    for x, y, z, t in K.SHIP:
        if y > max_row: continue
        X, Y = x + dx, y + dy
        if not m.inb(X, Y): continue
        if not draw:
            if z == 0 and m.cls[Y, X] in 'su.d' and not m.taken[Y, X]:
                m.taken[Y, X] = True; m.under[Y, X] = m.cls[Y, X]; m.cls[Y, X] = 'B'
            continue
        if z == 0:
            if m.cls[Y, X] != 'B': continue
            if m.L[1, Y, X] >= RC_VBASE: m.L[0, Y, X] = m.L[1, Y, X]
            m.L[1, Y, X] = t
        elif m.cls[Y, X] in 'Bsu.d':
            m.L[2, Y, X] = t


BUILD[528] = build_528
