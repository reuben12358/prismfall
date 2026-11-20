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
    CK.clear_around(r)
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
    r.forest_band('N', 5, wobble=2.0)
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
          once('The Saltmere Beacon', (55, 9), ['From the top of the dune the free port opens out below you: a white town on a salt lake, striped awnings, lantern masts, and a theatre on every second corner.',
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
                   'A theatre barge lies half-buried in the dune. Its name board still reads THE WANDERING CHORUS.', 'You dig at the stern with the shovel...',
                   {'script': 'pfm_item(:PROMPTERSSCRIPT, 1, "Prompter\'s Script")'}, {'script': 'pfm_item(:NORMALGEM, 1, "Normal Gem")'},
                   {'script': 'pfm_set(:sm_prompter)'}],
                   'else': ['A theatre barge lies half-buried in the dune. Its costume hampers have burst open in the sand, and a prop throne with three legs still stands on the deck.',
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
    CK.clear_around(r)
    # playtest round 3 item 5: Saltmere's East Gate meets the down properly - gateposts at the road's mouth on the W edge
    # and a drystone wall running off north and south from them, the road widened into a trodden apron before the gate
    for y in range(34, 46):
        for x in range(0, 4):
            if 38 <= y <= 41 and x < 4: m.cls[y, x] = 'd'
    for y in list(range(28, 37)) + list(range(43, 52)):
        if m.free(0, y, 1, 1, on='.tu') and not r.road_mask[y, 0]: m.stamp('nr_wall_v', 0, y, mark='B')
    for y in (36, 42):
        if m.free(1, y - 1, 1, 2, on='.tud'): m.stamp('nr_col', 1, y - 1, mark='B')
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
    CK.fringe(r, CK.FRINGE['coast'], 230, seed=1, near_forest=6)
    CK.fringe(r, ['nt_pine_a', 'nt_pine_b', 'nt_dpine_sh', 'nt_teal_a'], 55, box=(0, 12, W, 56), seed=2, near_forest=0)
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


# ====================================================================================================== 541 The Grey Saltings
LOW = None


def low_water(name, at_, tile):
    """a cell of the drowned road or a night plank: water by day; at low water (night) an event shows the shoal / plank
    tile, whose passage makes the cell walkable (the Tidelock raft habit).  Self switch A is set by the Tide event."""
    return {'type': 'event', 'name': name, 'at': list(at_), 'fixed': True, 'pages': [
        {'commands': []}, {'cond': {'self': 'A'}, 'graphic': {'tile': tile}, 'commands': []}]}


def tide_controller(mid, at_):
    """a parallel event: every second, low-water events follow the clock (self switch A = night), refresh on change"""
    return {'type': 'event', 'name': 'Tide', 'at': list(at_), 'fixed': True, 'pages': [{'trigger': 'parallel', 'commands': [
        {'script': "night = PBDayNight.isNight?\nchanged = false\n$game_map.events.each_value do |e|\n"
                   "  next if !e.name.start_with?('Low water')\n  key = [%d, e.id, 'A']\n"
                   "  next if $game_self_switches[key] == night\n  $game_self_switches[key] = night\n  changed = true\nend\n"
                   "$game_map.need_refresh = true if changed" % mid}, {'wait': 40}]}]}


def build_541():
    """The Grey Saltings (70x110, BEACH): Saltmere's salt marsh.  The gravel causeway runs north from the North Gate
    between the estuary (west: mudflats, the tidal channel, the wreckers' islet) and the chalk cliff of Brinecut (east,
    two levels; the mine's timbered back door in its face).  South-west: the salt pans, white stacks, the boiling-house
    and the Brinewife's Rest.  Middle: the boardwalk maze over the marsh pools (planks laid only at low water, night),
    the bird hide, the Crabrawler ring, the Sandygast castles, the salt barge sunk in the mud.  Secret: the Drowned Lane,
    an old cart road across the channel that only shows at night, to the wreckers' cache on the islet."""
    global LOW
    W, H = 70, 110
    r = Route(541, W, H, 'shore', kit={1: 'akc', 2: 'akc', 'default': 'akc'}, base='.')
    m = r.m
    m.gv_dark = 0.44                                                   # mottled wet ground
    # ---- the estuary (west): channel, deep water, mud
    for y in range(H):
        cw = 9 + 3.0 * (vnoise(0, y, 5411, 12.0) - 0.5) * 2 + bump(y, 84, 12, 5) - bump(y, 20, 10, 3)
        for x in range(W):
            if x < cw: m.cls[y, x] = 'W' if x < cw - 4 else 'w'
            elif x < cw + 3 + 2 * vnoise(x, y, 5412, 4.0): m.cls[y, x] = 'd'
    CK.smooth_sea(m, 2)
    # the wreckers' islet in the channel
    m.blob(4, 84, 3.5, 3.0, '.', seed=5, rough=0.3, only='wWd')
    m.blob(4, 84, 4.8, 4.2, 's', seed=6, rough=0.3, only='wW')
    m.blob(4, 84, 3.2, 2.6, '.', seed=5, rough=0.2, only='s')
    # ---- Brinecut: the chalk shelf across the north-east, two levels, faces to the south
    for x in range(W):
        f1 = 34 + 3 * (vnoise(x, 0, 5414, 10.0) - 0.5) * 2 - bump(x, 40, 5, 10)
        f2 = 19 + 2 * (vnoise(x, 1, 5416, 9.0) - 0.5) * 2 - bump(x, 48, 6, 8)
        for y in range(H):
            if x >= 39 and y <= f1: m.ht[y, x] = 1
            if x >= 47 and y <= f2: m.ht[y, x] = 2
    for h in (1, 2): CK.smooth_ht(m, h, 3)
    # ---- the marsh: pools (grass-edged water) in clusters, mudflats; the salt flats (class S) in the south-west
    for i, (cx, cy, rx, ry) in enumerate(((21, 38, 6.5, 3.6), (28, 46, 4.5, 3), (18, 54, 5.5, 3.2), (24, 64, 4, 2.6),
                                          (44, 52, 5, 3.4), (50, 60, 3.5, 2.4), (44, 74, 5, 3), (52, 84, 4, 2.6), (40, 90, 3.5, 2.2))):
        CK.pond(r, cx, cy, rx, ry, c='p', rough=0.7, seed=i)
        CK.pond(r, cx + rx * 0.6, cy + ry * 0.5, rx * 0.5, ry * 0.6, c='p', rough=0.7, seed=i + 20)
    for i, (cx, cy, rx, ry) in enumerate(((18, 72, 6, 4), (16, 92, 4, 3), (24, 28, 4, 2.5), (54, 96, 5, 3), (48, 42, 4, 2),
                                          (30, 56, 3, 2), (56, 70, 4, 2.5))):
        m.blob(cx, cy, rx, ry, 'd', seed=5420 + i, rough=0.75, only='.')
    for y in range(90, 107):
        for x in range(10, 30):
            if m.cls[y, x] in '.d' and ((x - 20) / 10.0) ** 2 + ((y - 98) / 8.0) ** 2 <= 1.0 + 0.3 * (vnoise(x, y, 5430, 3.0) - 0.5): m.cls[y, x] = 'S'
    # ---- tidal creeks meander in from the estuary (the causeway bridges them)
    creeks = [[(11, 44), (16, 46), (13, 50), (20, 52)], [(12, 66), (18, 68), (26, 70), (30, 68), (38, 66), (46, 68), (54, 66)],
              [(12, 24), (18, 26), (24, 24), (30, 26)], [(14, 80), (22, 82), (30, 80), (40, 82), (48, 80)]]
    pre = m.cls == 'p'
    for i, pts in enumerate(creeks): CK.stream(r, pts, w=1.7, c='p', seed=i, only='.tdT')
    creek = (m.cls == 'p') & ~pre
    # ---- the causeway (gravel), the mine path, the Rest, the hide
    road = [(32.5, 109), (33, 100), (36, 90), (34, 80), (32, 70), (35, 60), (32, 50), (30, 40), (33, 28), (37, 16), (35.5, 0)]
    r.road(road, w=3.0, c='g', open_=None, only='.tTdp')
    for y, x in np.argwhere(creek & (m.cls == 'g')): m.cls[y, x] = 'p'; r.deck.append((x, y))    # little bridges over the creeks
    r.exit('S', 30, 6); r.exit('N', 34, 4)
    for y in range(H):
        for x in range(W):
            if m.cls[y, x] == 'd' and ((y > H - 5 and 30 <= x < 36) or (y < 4 and 34 <= x < 38)): m.cls[y, x] = 'g'
    r.lane([(35, 40), (44, 42), (52, 40)], w=2.0, c='g', open_=None, only='.tTd')         # to the mine's back door
    yy = max(y for y in range(H) if m.ht[y, 61] == 1); CK.stair(r, 60, yy, w=3, h=1)    # up onto Brinecut
    r.lane([(61, yy + 3), (58, 44), (52, 42)], w=2.0, c='g', open_=None, only='.tTd')
    y2 = max(y for y in range(H) if m.ht[y, 56] == 2); CK.stair(r, 55, y2, w=2, h=2)       # up onto the top
    r.lane([(56, y2 + 3), (58, yy - 2), (61, yy - 1)], w=2.0, c='g', open_=None, only='.tTd')
    r.lane([(33, 74), (22, 76), (14, 66), (13, 60)], w=2.0, c='g', open_=None, only='.tTd')  # to the Brinewife's Rest
    r.lane([(33, 60), (40, 62), (44, 64)], w=2.0, c='g', open_=None, only='.tTd')         # to the bird hide
    # the boardwalk maze over the pools (planks; three only laid at low water)
    walks = [((22, 44), (22, 33)), ((15, 38), (30, 38)), ((18, 49), (18, 60)), ((18, 49), (30, 49)), ((27, 42), (27, 49)),
             ((39, 52), (50, 52)), ((44, 47), (44, 58)), ((40, 74), (50, 74)), ((44, 70), (44, 80)), ((20, 64), (30, 64)), ((48, 84), (56, 84))]
    for (x0, y0), (x1, y1) in walks:
        for y in range(min(y0, y1), max(y0, y1) + 1):
            for x in range(min(x0, x1), max(x0, x1) + 1):
                if m.cls[y, x] == 'p': r.deck.append((x, y))
                elif m.cls[y, x] in '.t': m.cls[y, x] = 'd'
    night_planks = [(25, 38), (27, 45), (44, 77)]
    r.deck = [c for c in r.deck if c not in night_planks]
    # the Drowned Lane: from the mudflat to the islet, a cart road under the channel
    lane_y = 84
    drowned = [(x, lane_y) for x in range(5, 20) if m.cls[lane_y, x] in 'wW']
    for x, y in drowned: m.cls[y, x] = 'w'
    r.finish_plan(border=0)
    r.forest_band('E', 6, wobble=2.0)
    for y in range(0, 4):
        for x in range(40, W):
            if m.cls[y, x] in '.t' and y < 2 + 2 * vnoise(x, 0, 5440, 5.0): m.cls[y, x] = 'T'
    for cx, cy, rx, ry in ((44, 8, 5, 3), (16, 10, 6, 4), (60, 62, 4, 3), (14, 34, 2.5, 3), (26, 14, 4, 3), (60, 106, 5, 3), (50, 92, 3, 2.5), (40, 58, 2.5, 2), (24, 76, 2.5, 2), (40, 16, 3, 2.5), (62, 40, 3, 3), (60, 76, 5, 4), (58, 96, 6, 6), (40, 104, 4, 3), (12, 44, 3, 4),
                           (62, 8, 5, 4), (54, 28, 3, 2), (64, 50, 3, 4), (36, 82, 3, 2)):
        r.copse(cx, cy, rx, ry)
    # tall grass: sea-lavender and cord-grass patches on the marsh
    CK.grass_fields(r, [(40, 46, 3), (26, 20, 3.5), (52, 66, 3.5), (28, 84, 4), (48, 78, 3), (14, 46, 2.5), (40, 64, 3),
                        (28, 8, 3), (46, 104, 3), (14, 30, 2.5), (38, 96, 3), (54, 46, 3), (48, 26, 3), (60, 14, 3), (30, 72, 3),
                        (22, 80, 2.5), (58, 90, 3), (36, 54, 2.5), (54, 10, 2.5)])
    CK.earth(r, [(36, 84, 2.5, 1.5), (30, 56, 2, 1.2), (36, 22, 2, 1.2)], c='u')
    CK.woods(r, CK.COAST, scale=10.0)
    LOW = [K.P1('cs_shoal0'), K.P1('cs_shoal1')]
    plank = K.P1('bw_h')
    # ---- events
    mx = 52; my = max(y for y in range(H) if m.ht[y, mx] == 1) + 2
    r.add({'type': 'warp', 'name': 'Mine back door', 'at': [mx, my], 'link': 'R4_MINE', 'arrive': [mx, my + 1, 'down'], 'se': 'Door exit', 'fixed': True},
          sign((36, 104), 'Road sign', "THE GREY SALTINGS -- The Weavers' Road. v Saltmere (North Gate) - ^ The Dyers' Ford, Thistledown Lea & Briarwick.\nMind the pans. The pans do not mind you."),
          once('The Saltings', (33, 99), ['Salt pans run to the horizon between white stacks and the smoke of the boiling-house. Behind them stands a chalk cliff with a mine mouth in it.',
               J('neutral', 'This is where Saltmere\'s salt comes from. "Grey" is the salt before it\'s washed.'), J('neutral', "...And the weather. It's mostly the weather.")]),
          trainer((28, 58), 'SAILOR', 'Morrow', "Salt barge went down in the mud in '88. Still there. Still salty.", "You're heavier than you look. In battle, I mean.", d='right'),
          trainer((38, 72), 'TUBER_F', 'Pip', "My floaty is a Wailmer! No it's not. It's a floaty.", 'Waaah! My floaty popped!', d='left'),
          trainer((36, 34), 'CAMPER', 'Ned', 'Sand in my tent! Sand in my boots! Sand in my battle!', 'Sand in my tent AND I lost. Great day.', d='down'),
          talk('Salt Raker', (18, 94), 'NPC 19', ["Salt Raker: You're the ones from the Pageant? Everyone's heard.",
               "Salt Raker: The rakers say the Mourner's a Saltmere man. The boilers say he's from Verdance. Nobody says it loud."], move='random'),
          talk('Samphire Picker', (16, 70), 'NPC 27', ["Samphire Picker: Pick from the edges. The middle's the Plate's. Don't ask me what that means. My mother said it."]),
          talk('Children building Sandygast castles', (20, 74), 'NPC 16', ["Children: Don't step on that one! That one's ALIVE. ...That one too."]),
          talk('Sandygast', (21, 76), 'Followers/SANDYGAST', ['(A sand castle. It is watching you.)']),
          talk('Squawkabilly watcher', (45, 65), 'NPC 09', ['Watcher: Squawkabilly. Four colours, one flock, and every one of them thinks it\'s the real one.',
               J('happy', 'Squawkabilly! Four colors! In the wild they argue about which one\'s the real one!')]),
          obj('Salt-barge wreck', (14, 20), ["The wreck of a salt barge, sunk to the gunwales in the mud. The name board says HONEST WEIGHT."]),
          hidden((16, 22), 'BIGPEARL', 'HiddenItem (salt-barge wreck)'),
          {'type': 'event', 'name': 'Ring Boss', 'at': [45, 101], 'pages': [{'graphic': {'sprite': 'NPC 21', 'dir': 'down'}, 'trigger': 'action', 'commands': [
              {'if': 'pfm?(:crab_ring)', 'then': ["Ring Boss: Champion of the mudflat! The bucket's yours. The glory's mine."],
               'else': ['Ring Boss: Crabrawler ring! Three bouts, no biting, best of three, winner gets the bucket!',
                        {'choices': ['Step into the ring.', 'Not now.'], 'cancel': 1, 'branches': [
                            [{'script': 'WildBattle.start(:CRABRAWLER, 15)'}, {'script': 'WildBattle.start(:CRABRAWLER, 15)'},
                             {'script': 'WildBattle.start(:CRABRAWLER, 16)'}, "Ring Boss: Champion! Here's the bucket.", '(It contains a KING\'S ROCK.)',
                             {'script': 'pbReceiveItem(:KINGSROCK)'}, {'script': 'pfm_set(:crab_ring)'}],
                            ['Ring Boss: The ring is always open. The ring never closes. The tide closes it, twice a day.']]}]}]}]},
          obj('Road Stone II', (38, 6), ['ROAD STONE II. THE WEAVERS\' ROAD. "Saltmere 1, Briarwick 4." A ribbon of undyed silk is tied round it.']),
          obj('The boiling-house', (28, 88), ['THE BOILING-HOUSE. Brine in, salt out, smoke up. A notice: "NO SWIMMING IN THE PANS. THIS MEANS YOU, TERRENCE."']),
          obj('The Drowned Lane', (20, lane_y - 1), ['Ruts in the mud run straight into the channel and on under the water, toward the islet.',
               {'if': 'PBDayNight.isNight?', 'then': ['The tide is out. The old cart road shows above the water, all the way across.'],
                'else': ['The rakers say the old cart road comes up at night, when the tide goes out.']}]),
          obj("Wreckers' cache", (4, 83), ["A wreckers' cache: a tarred chest, padlocked. The lock is stamped SALTMERE HARBOUR OFFICE."]),
          item((3, 85), 'BIGPEARL'), hidden((5, 82), 'STARDUST', 'HiddenItem (the Drowned Lane)'),
          item((10, 34), 'POTION'), item((60, 12), 'GREATBALL'), hidden((52, 6), 'NUGGET', 'HiddenItem (Brinecut top)'), hidden((14, 100), 'PEARL', 'HiddenItem (salt pans)'),
          obj('Low-water planks', (25, 34), ['Plank rests on the boardwalk posts, empty. The salt-rakers lay the missing boards at low water, when the pools drain.']),
          tide_controller(541, (1, 1)))
    for i, (x, y) in enumerate(drowned): r.events.append(low_water('Low water lane %d' % (i + 1), (x, y), LOW[i % 2]))
    for i, (x, y) in enumerate(night_planks): r.events.append(low_water('Low water plank %d' % (i + 1), (x, y), plank))
    for x, y in drowned + night_planks: m.taken[y, x] = True
    r.seat_events(on='.dtgSu')
    CK.clear_around(r)
    fd = m.front('sh_cot', 12, 58, 'R4_REST', "The Brinewife's Rest door")
    r.events += [e for e in m.events if e.get('link') == 'R4_REST']; m.events = []
    m.stamp('pf_minemouth', mx - 1, my - 2, mark='B')
    m.cls[my, mx] = 'g'
    r.near('gl_flat2', 26, 82, on='.dgS', r=3)                                           # the boiling-house
    r.near('fw_smoke_a', 28, 80, on='.dg', r=3)
    r.near('gl_shed', 46, 60, on='.', r=4)                                               # the bird hide over the pools
    hiker = None
    CK.pans_varied(r, 11, 91, 30, 106, pw=(2, 5), ph=(2, 3), seed=541, gap=(1, 1))
    for n, x, y in (('hb_salt0', 14, 90), ('hb_salt1', 26, 102), ('hb_salt2', 12, 102), ('hb_salt0', 30, 94), ('hb_tubs', 10, 98),
                    ('hb_barrel', 22, 88), ('hb_salt1', 18, 104)):
        r.near(n, x, y, on='S', r=3)
    for (x, y) in ((42, 99), (48, 99), (42, 104), (48, 104), (40, 101), (50, 101)):          # the Crabrawler ring
        r.near('dk_pebbles', x, y, on='.dt', r=1)
    ship_part_sand(r, -26, -32, 53)                                                     # HONEST WEIGHT, sunk in the mud
    CK.props(r, ['ck_boulder', 'ck_pebbles', 'nt_rocks_s0'], 18, box=(38, 0, W, 40), clump=3, seed=7)
    for (x, y) in ((44, 14), (58, 6), (64, 26)):
        r.near('ck_rock_big', x, y, on='.t', r=3)
    CK.props(r, ['nt_reed1', 'nt_reed0', 'nt_reed1'], 130, box=(10, 20, 62, 96), on='.d', clump=2, seed=8)
    CK.props(r, ['nt_log', 'dk_pebbles'], 10, box=(8, 20, 30, 110), on='d', clump=2, seed=9)
    CK.fringe(r, CK.FRINGE['coast'], 230, seed=1, near_forest=5)
    CK.fringe(r, ['nt_pine_a', 'nt_teal_a', 'nt_dpine_sh'], 16, box=(14, 4, 60, 100), seed=2, near_forest=0)
    CK.undergrowth(r, 160, kinds=('nt_fern0', 'nt_fern1', 'nt_bush0', 'nt_bush1', 'nt_reed1', 'ak_fern'), seed=3)
    r.dress(trees=('nt_pine_a',), n_trees=0, copses=0, scatter=0)
    r.paint(glint=0.35)
    ship_part_sand(r, -26, -32, 53, draw=True)
    CK.paint_extras(r)
    CK.crust_ground(r, [(x, y) for y, x in np.argwhere((m.cls == 'S') | ((m.cls == 'B') & (m.under == 'S')))])
    CK.boardwalks(r, r.deck)
    CK.shore(r, wet=1, wet_noise=0.5, wrack=0.4, shallows=0.02, chalk_rocks=False)
    for i, (cx, cy, rx, ry) in enumerate(((42, 32, 4, 2), (46, 56, 3, 2), (28, 78, 4, 2), (40, 100, 3, 2))):
        CK.meadow(r, cx, cy, rx, ry, tiles=[K.DECOR_SH['flowers'][k] for k in (5, 9)], p=0.6, seed=i)      # sea lavender
    CK.scatter_quiet(r, 8)
    h = head(541, 'The Grey Saltings', field='BEACH', bgm='Route 2', biome='route',
             connections=[{'dir': 'S', 'offset': 30, 'to': 140, 'to_offset': 43}, {'dir': 'N', 'offset': 34, 'to': 552, 'to_offset': 38}],
             tone=[0, 0, 4, 18], fog={'name': 'prismfall_seamist', 'opacity': 40, 'blend': 0, 'zoom': 200, 'sx': 1, 'sy': 0})
    h['walk_from'] = [[4, 84]]                                                     # the islet (over the low-water lane)
    r.write(h, '541_grey_saltings.yaml', '# The Grey Saltings (541). WRITTEN BY layouts/routes_craft.py - edit that script.\n', '/tmp/rt/541.png' if PREV else None)


C_SH497 = K.C('sh', 497)
BUILD[541] = build_541


# ====================================================================================================== 552 The Dyers' Ford
def sluice_stone(name, at_, idx, colour):
    """one of the vat-yard sluice stones (touch): stepped in the river's own order (red, blue, yellow) it opens the gate"""
    scr = ("v = $game_variables[602]\n"
           "if v < 4\n"
           "  if v == %d\n"
           "    $game_variables[602] = v + 1\n"
           "    pbSEPlay('Door exit') rescue nil\n"
           "    if v + 1 >= 3\n"
           "      $game_variables[602] = 4\n"
           "      pbMessage(_INTL('Clunk. Somewhere under the vats the sluice gate grinds open, and the white water runs free.'))\n"
           "      $game_map.need_refresh = true\n"
           "    end\n"
           "  elsif v > 0\n"
           "    $game_variables[602] = 0\n"
           "    pbMessage(_INTL('The stones sink back. The sluice shudders and stays shut.'))\n"
           "  end\n"
           "end" % idx)
    return {'type': 'event', 'name': name, 'at': list(at_), 'fixed': True, 'pages': [
        {'graphic': {'tile': K.P1('df_slab_' + colour)}, 'trigger': 'touch', 'through': True, 'commands': [{'script': scr}]}]}


def build_552():
    """The Dyers' Ford (80x72, MEADOW): the River Selvedge in three dyed bands below Briarwick's dye-works.  North: the
    works on their terrace (three vat sheds, the vats, drying lines over the road you walk under like corridors, the
    vat-yard sluice: step the colour stones in the river's own order); the white water falls off the terrace in the
    one undyed stream.  The stepping-stone ford.  South: the madder, woad and weld fields, three colours of tall grass;
    the fulling mill on the bank; the sheep-wash and shearers; the Smeargle's boundary stone; the shrine of the Fourth
    Colour.  East: the cloth barge's jetty (it rows you back to Saltmere once the sluice runs).  Secret: through the
    culvert grate (opened by the sluice), up the white water to the Bleachfield."""
    W, H = 80, 72
    r = Route(552, W, H, 'meadow', base='.')
    m = r.m
    # ---- the north terrace (h1) with the works; the river Selvedge
    lipy = colmap(r, lambda x: 20 + 2 * (vnoise(x, 0, 5521, 9.0) - 0.5) * 2 + bump(x, 8, 7, 3))
    for x in range(W):
        m.ht[:lipy[x] + 1, x] = 1
    CK.smooth_ht(m, 1, 2)
    cy = colmap(r, lambda x: 35 + 2 * (vnoise(x, 1, 552, 14.0) - 0.5) * 2)
    for x in range(W):
        for y in range(cy[x] - 5, cy[x] + 6): m.cls[y, x] = 'w'
    # the white water: down from the Bleachfield (NE) to the river, over the terrace lip
    CK.stream(r, [(69, 0), (68, 8), (69, 16), (68, 26), (68, cy[68] - 4)], w=2.2, c='w', only='.tT')
    sx = 67
    # ---- the road: from the North exit down the stairs, through the meadow, over the ford, south between the fields
    road = [(40.5, 0), (40, 10), (40, lipy[40] - 1)]
    r.road(road, w=3.0, open_=None, only='.tT')
    CK.stair(r, 39, max(y for y in range(H) if m.ht[y, 40] == 1), w=3, h=1)
    r.road([(40, lipy[40] + 3), (38, 26), (39, cy[39] - 6)], w=3.0, open_=None, only='.tT')
    r.road([(39, cy[39] + 6), (37, 50), (40, 60), (39.5, 71)], w=3.0, open_=None, only='.tT')
    r.exit('N', 39, 4); r.exit('S', 38, 4)
    stones_ = [(x, y) for y in range(cy[39] - 5, cy[39] + 6) for x in (38, 39, 40) if m.cls[y, x] == 'w' and (x + y) % 3 != 0 or (m.cls[y, x] == 'w' and x == 39)]
    # side paths: the vat yard, the jetty, the mill, the sheep-wash, the white-water bank
    r.lane([(42, 12), (50, 13), (60, 14)], w=2.0, open_=None)
    r.lane([(42, 27), (56, 28), (72, cy[72] - 6)], w=2.0, open_=None)
    r.lane([(37, 50), (22, 48), (12, 46)], w=2.0, open_=None)
    r.lane([(41, 58), (56, 58), (66, 56)], w=2.0, open_=None)
    r.lane([(60, 14), (64, 11), (64, 5)], w=1.6, open_=None)
    # the Bleachfield (on the terrace, up the white water's west bank)
    r.clearing(60, 3, 5, 2.6, c='.')
    # the sheep-wash pool; the mill race
    CK.pond(r, 70, 57, 4, 2.5, c='w', rough=0.3)
    r.forest_band('W', 4, wobble=2.0); r.forest_band('E', 3, wobble=2.0); r.forest_band('N', 2, wobble=1.0)
    for cx, cy_, rx, ry in ((10, 8, 7, 5), (24, 6, 6, 4), (6, 62, 5, 6), (74, 66, 5, 4), (60, 4, 3, 2.5), (26, 30, 4, 2.5),
                            (54, 44, 3, 2.5), (14, 32, 4, 2.5), (66, 44, 3, 2), (32, 8, 4, 3), (4, 50, 3, 4), (48, 70, 4, 2),
                            (76, 56, 2.5, 4)):
        r.copse(cx, cy_, rx, ry)
    r.finish_plan(border=0)
    CK.waterfall(r, sx, sx + 2, lipy[sx + 1])
    # the madder, woad and weld fields (organic, dyed later), and plain tall grass on the banks
    fields = {'r': [(14, 54, 5), (20, 60, 4)], 'b': [(52, 52, 4.5), (58, 62, 4)], 'y': [(28, 64, 4), (16, 66, 3.5)]}
    for k, spots in fields.items(): CK.grass_fields(r, spots)
    dyemask = {k: np.zeros((H, W), bool) for k in fields}
    for k, spots in fields.items():
        for (fx, fy, s_) in spots:
            for y in range(max(0, int(fy - 2.5 * s_)), min(H, int(fy + 2.5 * s_))):
                for x in range(max(0, int(fx - 2.5 * s_)), min(W, int(fx + 2.5 * s_))):
                    if m.cls[y, x] == 't' and ((x - fx) / (2.2 * s_)) ** 2 + ((y - fy) / (1.8 * s_)) ** 2 <= 1.0: dyemask[k][y, x] = True
    CK.grass_fields(r, [(20, 26, 3), (56, 24, 3), (8, 28, 2.5), (30, 14, 3), (16, 16, 3), (74, 26, 2.5), (48, 66, 3)])
    CK.ledge(r, 26, 35, 47)
    for y in (46, 47, 48):
        for x in (25, 36):
            if m.cls[y, x] in '.t': m.cls[y, x] = 'T'
    CK.woods(r, CK.ELOWEN, scale=12.0)
    # ---- events
    flag = lambda i, x, y, extra=(): {'type': 'event', 'name': 'Survey flag %d' % i, 'at': [x, y], 'pages': [{'trigger': 'action',
                                     'commands': ['An orange survey flag on a stake. MERIDIAN LATTICE - LINE 7.'] + list(extra)}]}
    grate_t = K.P1('nr_wall_v')
    r.add(sign((36, 66), 'Road sign', "THE DYERS' FORD -- The Weavers' Road. Briarwick Dye-Works. Do not drink the river. Do not bathe in the river. Do not stand in the red."),
          once("The Dyers' Ford", (39, cy[39] + 7), ['Below the three vat-sheds the River Selvedge runs in three bands: madder red, woad blue, weld yellow. Cloth dries on lines across the road, so you walk under it as if down corridors.',
               J('happy', "The Briarwick dyers wash their cloth here, so the river runs in three colors! There's a fourth band nobody's allowed to dye. It's just water. People leave ribbons for it.")]),
          talk('Meridian Surveyor', (44, 24), 'trainer_SCIENTIST', ['Meridian Surveyor: Mind the orange flags. Survey line for the new Lattice. Straight up the river and through to the wood.',
               'Meridian Surveyor: Trees aren\'t in the plan, but trees rarely are.'], d='left'),
          flag(1, 43, 26, [J('neutral', "These go right toward the Glasswood. That's..."), '(She stops. Two nights ago a man in a mask asked a theater why nothing in Verdance ever rots.)',
                           J('sad', "...That's probably fine. Isn't it?")]),
          flag(2, 43, 10), flag(3, 43, 4), hidden((44, 3), 'ANTIDOTE', 'HiddenItem (base of the third flag)'),
          trainer((52, 16), 'PAINTER', 'Morwenna', "Red's my color! Red's everyone's color, eventually, if you work the madder vat.", "Look at my hands. They'll be red till Fallmorn.", d='left'),
          trainer((60, 10), 'PAINTER', 'Ash', "Woad blue. The Queen's Elowen green is woad and weld together. She's never paid for a yard of it.", 'Bill her. Somebody bill her.', d='down'),
          {'type': 'event', 'name': 'Dye Foreman', 'at': [54, 19], 'pages': [{'graphic': {'sprite': 'NPC 20', 'dir': 'down'}, 'trigger': 'action', 'commands': [
              {'if': '$game_variables[602] >= 4', 'then': ["Dye Foreman: You opened the sluice? In the right order? Which order was it?",
                                                          '(You tell him. He hums it. He hums it wrong.)',
                                                          "Dye Foreman: Tell the bargee the cloth's ready. She'll row you down to Saltmere, she owes me."],
               'else': ["Dye Foreman: The sluice stones. Step them in the order I hum. Red, blue, yellow. No -- that's blue, red, yellow.",
                        "Dye Foreman: I've been humming it wrong for thirty years and nobody's told me. The river knows. Ask the river."]}]}]},
          sluice_stone('Sluice stone red', (49, 18), 0, 'r'), sluice_stone('Sluice stone blue', (51, 18), 1, 'b'), sluice_stone('Sluice stone yellow', (53, 18), 2, 'y'),
          {'type': 'event', 'name': 'Culvert grate', 'at': [64, 8], 'fixed': True, 'pages': [
              {'graphic': {'tile': grate_t}, 'trigger': 'action', 'commands': ['A grate over the culvert where the white water comes down. It is chained to the sluice gate below.']},
              {'cond': {'var': ['ROAD_SLUICE', 4]}, 'through': True, 'commands': []}]},
          talk('Smeargle owner', (24, 62), 'NPC 18', ["Smeargle owner: My Smeargle paints a mark on the boundary stone for every trainer who passes.",
               "Smeargle owner: Yours is... it's left yours blank. It's never done that."]),
          talk('Smeargle', (25, 63), 'Followers/SMEARGLE', ['(It looks at you, then at its brush, then at you. It puts the brush away.)'], move='random'),
          obj('Boundary stone', (22, 61), ['A boundary stone painted with a hundred small marks in every colour. One square, near the bottom, is left blank.']),
          talk('Shearer', (64, 54), 'NPC 03', ["Shearer: Briarwick's dyers, Saltmere's salt, Ferrow's fish. Every town in Elowen's got a thing the Plate gives it.",
               "Shearer: We've got colors. Lovely colors. You can't eat them."]),
          talk('Mareep', (62, 56), 'Followers/MAREEP', ['Baa-zzt.'], move='random'), talk('Mareep ', (62, 61), 'Followers/MAREEP', ['Baa.'], move='random'),
          obj('Shrine of the Fourth Colour', (64, cy[64] - 6), ['A plain white ribbon tied to a stake where the undyed white water meets the river. Dozens more are tied beside it.',
              'A card in a child\'s hand: "for the color nobody gets".']),
          trial('Hound shrine', (61, cy[61] - 6), 'SHRINE_FORD'),
          {'type': 'berry', 'at': [26, 50], 'berry': 'PECHABERRY'},
          obj('Fulling mill', (12, 44), ['THE FULLING MILL. Hammers the size of Snorlax beat the cloth soft. Not today: the wheel is waiting on the river.']),
          {'type': 'event', 'name': 'Bargee', 'at': [72, cy[72] - 7], 'pages': [{'graphic': {'sprite': 'NPC 25', 'dir': 'down'}, 'trigger': 'action', 'commands': [
              {'if': '$game_variables[602] >= 4', 'then': [
                  "Bargee: The foreman says the cloth's ready and you're the reason. Want a lift down to Saltmere? It's all downstream.",
                  {'choices': ['Ride the barge.', 'Not yet.'], 'cancel': 1, 'branches': [
                      ['(You sit on the bolts of red and blue cloth. The Selvedge carries you down past the Saltings to the salt lake.)',
                       {'tone': [-255, -255, -255, 0, 12]}, {'wait': 14}, {'transfer': {'map': 140, 'x': 40, 'y': 61, 'dir': 'down'}},
                       {'tone': [0, 0, 0, 0, 12]}],
                      ["Bargee: I'll be here. The river's not going anywhere. Well. It is. But slowly."]]}],
               'else': ["Bargee: Cloth barge to Saltmere. When the foreman's errand's done, I'll row you down. Till then I'm 'on my break'."]}]}]},
          obj('The Bleachfield', (60, 2), ['(Through the culvert: a small meadow where the undyed water spreads out. Every flower is white. The air rings, very faintly.)']),
          item((57, 3), 'TM44'), item((10, 50), 'POTION'), item((68, 45), 'SUPERPOTION'),
          obj('Madder field', (12, 58), ['MADDER (red). The dyers grow their own colours. Please stay on the path. The path is also madder.']),
          obj('Woad field', (50, 60), ['WOAD (blue). Do not eat. Do not roll in. Do not let the Mareep roll in.']),
          obj('Weld field', (30, 68), ['WELD (yellow). It looks like a weed because it is a weed. A very valuable weed.']))
    stones_ = [c for c in stones_ if m.cls[c[1], c[0]] == 'w']
    CK.stones(r, stones_)
    for x, y in ((49, 18), (51, 18), (53, 18), (64, 8)): m.taken[y, x] = True
    for y in range(6, 11):                                                               # the grate closes the bank path
        for x in (62, 63, 65, 66):
            if m.cls[y, x] in '.t' and m.cls[y, x] != 'w': m.cls[y, x] = 'T'
    r.seat_events(on='.dt')
    CK.clear_around(r)
    # ---- the works: vat sheds, vats, drying lines across the road, barrels; the mill; the jetty; the sheep-wash pen
    for nm, x, y in (('gl_shed', 46, 4), ('gl_shed', 53, 3), ('gl_shed', 59, 5)):
        r.near(nm, x, y, on='.d', r=3)
    for n, x, y in (('pf_p_vat_r', 47, 14), ('pf_p_vat_b', 53, 14), ('pf_p_vat_y', 58, 16), ('pf_p_vat_r', 49, 11), ('pf_p_vat_b', 56, 11),
                    ('hb_dyeline', 44, 7), ('hb_rugline', 49, 8), ('hb_rugline2', 55, 8), ('hb_barrels', 62, 16), ('hb_crates4', 60, 18),
                    ('hb_shed', 12, 41), ('pf_logbench', 30, 46), ('hb_tubs', 63, 58), ('df_sluice', 64, 17)):
        r.near(n, x, y, on='.d', r=3)
    r.near('gl_flat2', 6, 40, on='.', r=4)                                               # the fulling mill
    m.fence(58, 68, 51, gaps=((62, 64),)); m.fence(58, 68, 64, gaps=((60, 62),))
    for i, yy in enumerate((6, 10, 14)):                                                # drying lines over the road
        xs = [x for x in range(34, 48) if m.cls[yy, x] in 'd.t' and not m.taken[yy, x] or r.road_mask[yy, x]]
        if not xs: continue
        x0, x1 = min(xs), max(xs)
        for x in range(x0, x1 + 1):
            if x in (x0, x1):
                if m.free(x, yy, 1, 1, on='.t'): m.stamp('dl_post', x, yy, mark='B')
            else:
                m.over.append((2, x, yy, K.P1('dl_cloth_%s%d' % ('rby'[(x + i) % 3], (x * 3 + yy) % 2))))
    jetty = [(x, y) for x in (70, 71, 72) for y in range(cy[71] - 5, cy[71] - 1) if m.cls[y, x] == 'w']
    r.deck += jetty
    # walls between the fields
    for (x0, x1, y) in ((4, 22, 51), (44, 62, 46), (12, 32, 70)):
        for x in range(x0, x1 + 1):
            if abs(x - (x0 + x1) // 2) <= 1: continue                                    # a gate in every wall
            if m.free(x, y, 1, 1, on='.t') and vnoise(x, y, 5522, 3.0) > 0.25:
                m.stamp('nr_wall_' + ('w' if x == x0 else 'e' if x == x1 else 'm'), x, y, mark='B')
    CK.props(r, ['nt_boulder', 'nt_rocks_s0', 'nt_rocks_s1', 'nt_log', 'nt_stump'], 22, box=(0, 0, W, H), clump=3, seed=7)
    for (x, y) in ((36, 30), (44, 30), (30, 42), (48, 42), (60, 29), (20, 29), (8, 44), (76, 30)):
        r.near(random.Random(x * 7 + y).choice(['nt_reed1', 'nt_reed0']), x, y, on='.', r=2)
    CK.fringe(r, CK.FRINGE['meadow'], 150, seed=1, near_forest=5)
    CK.fringe(r, CK.FRINGE['orchard'], 12, box=(2, 24, 78, 70), seed=2, near_forest=0)
    CK.undergrowth(r, 220, seed=3)
    r.dress(trees=('tr_oak',), n_trees=0, copses=0, scatter=0)
    r.paint(glint=0.0)
    CK.paint_extras(r)
    CK.boardwalks(r, r.deck)
    T = {k: K._ST['_dyegrass']['tall_' + k] for k in 'rby'}
    for k, msk in dyemask.items():
        for y, x in np.argwhere(msk & (m.cls == 't')): m.L[1, y, x] = T[k]
    for y, x in np.argwhere(m.cls == 'w'):                                              # the three colours, and the clear band
        c = cy[x]
        band = (y - (c - 5)) / 11.0
        if x >= 66 and y < c - 5: continue                                              # the white water stays white
        nm = 'red' if band < 0.3 else 'blue' if band < 0.58 else 'yellow' if band < 0.86 else None
        if nm and m.L[1, y, x] == 0 and m.L[2, y, x] == 0 and 0 <= band <= 1: m.L[1, y, x] = K.P1('dye_%s%d' % (nm, (x * 7 + y) % 2))
    CK.water_stamp(r, 'hb_boat2', 73, cy[73] - 3)
    CK.meadow(r, 60, 3, 4, 2.0, tiles=[K.DECOR_SH['flowers'][2], K.DECOR_SH['flowers'][11]], p=0.9, seed=1)    # the Bleachfield's white flowers
    for i, (cx_, cy_, rx, ry) in enumerate(((22, 24, 5, 2), (56, 26, 5, 2), (8, 22, 3, 2), (28, 46, 4, 1.5), (68, 46, 3, 2), (46, 68, 4, 2))):
        CK.meadow(r, cx_, cy_, rx, ry, p=0.65, seed=i + 3)
    CK.scatter_quiet(r, 12)
    h = head(552, "The Dyers' Ford", field='MEADOW', bgm='Route 3',
             connections=[{'dir': 'S', 'offset': 38, 'to': 541, 'to_offset': 34}, {'dir': 'N', 'offset': 39, 'to': 540, 'to_offset': 20}], tone=[6, 4, -2, 0])
    h['walk_from'] = [[60, 4]]
    r.write(h, '552_dyers_ford.yaml', "# The Dyers' Ford (552). WRITTEN BY layouts/routes_craft.py - edit that script.\n", '/tmp/rt/552.png' if PREV else None)


BUILD[552] = build_552


# ====================================================================================================== 540 Thistledown Lea
def build_540():
    """Thistledown Lea (130x64, MEADOW): the extinct House Thistledown's river meadows, unmown for sixty years.  The road
    comes up from the Dyers' Ford over the old stone bridge (a fisherman keeps the toll nobody collects) and runs east to
    the Gossamer Wood.  North: Thistledown Manor on its terraced hill (ruined wall, gateposts, the overgrown topiary
    garden), and behind it the Ha-ha, a sunken ditch round the hill to the back garden and the cellar door (secret).  West:
    the outcrop with the Brinecut mine mouth.  The Ponyta paddock (its ledges drop to the road, one way); the mowers' camp
    with hay-ricks (heal once); the bamboo stand and its Pancham; the broken mill on the mill-race; four fields of tall
    grass and the wildflower meadows in bands; the Selvedge along the south with two islets."""
    W, H = 130, 64
    r = Route(540, W, H, 'meadow', base='.')
    m = r.m
    # ---- the river Selvedge along the south, two islets
    cy = colmap(r, lambda x: 53 + 2.0 * (vnoise(x, 0, 540, 16.0) - 0.5) * 2)
    for x in range(W):
        for y in range(cy[x] - 4, cy[x] + 5):
            if 0 <= y < H: m.cls[y, x] = 'w'
    m.blob(70, 53, 4, 1.6, '.', seed=3, rough=0.3, only='w'); m.blob(104, 54, 3, 1.4, '.', seed=4, rough=0.3, only='w')
    # ---- the manor hill (h1, h2) and the west outcrop
    CK.plateau(r, 66, 10, 20, 11, 1, rough=0.3, seed=1)
    CK.plateau(r, 66, 6, 11, 6, 2, rough=0.25, seed=2)
    for y in range(0, 28):
        for x in range(0, 20):
            if x < 15 + 3 * vnoise(0, y, 541, 7.0) and y < 22 + 2 * vnoise(x, 0, 543, 7.0): m.ht[y, x] = max(m.ht[y, x], 1)
    CK.smooth_ht(m, 1, 2); CK.smooth_ht(m, 2, 2, box=(40, 0, 95, 20))
    # the Ha-ha: the hill's back is cut off from the meadows except by the ditch path (forest closes the rest)
    # ---- the road: bridge, then east along the middle
    road = [(21.5, 63), (21, cy[21] + 5), (21, cy[21] - 5), (24, 42), (36, 36), (56, 34), (76, 33), (96, 34), (112, 31.5), (129, 31.5)]
    r.road(road, w=3.0, open_=None, only='T.tw')
    bridge = [(x, y) for y in range(H) for x in range(19, 25) if r.road_mask[y, x] and m.cls[y, x] == 'd' and cy[x] - 5 <= y <= cy[x] + 5]
    r.exit('S', 20, 4); r.exit('E', 30, 4)
    # the manor drive and stairs (h1, then h2), the mine path, the mill path, the Ha-ha
    y1 = max(y for y in range(H) if m.ht[y, 65] == 1)
    CK.stair(r, 64, y1, w=3, h=1)
    r.lane([(65, 33), (65, y1 + 3)], w=2.0, open_=None)
    y2 = max(y for y in range(H) if m.ht[y, 67] == 2)
    CK.stair(r, 66, y2, w=2, h=2)
    r.lane([(65, y1 - 1), (67, y2 + 3)], w=2.0, open_=None)
    ym = max(y for y in range(H) if m.ht[y, 9] == 1)
    r.lane([(24, 40), (14, 32), (9, ym + 3)], w=2.0, open_=None)
    r.lane([(96, 34), (98, 42), (96, cy[96] - 5)], w=2.0, open_=None)
    r.lane([(92, 33), (90, 24), (88, 14), (86, 3)], w=1.7, open_=None)            # the Ha-ha's ditch, round the hill's back
    r.clearing(82, 3, 4, 2.2)
    # fields and meadows
    r.clearing(38, 22, 9, 6)                                                      # the Ponyta paddock
    r.lane([(24, 38), (26, 31), (27, 25), (31, 21)], w=2.0, open_=None)           # the drove-way into it (the ledges are the way out)
    r.forest_band('N', 4, wobble=2.0); r.forest_band('S', 3, wobble=1.5); r.forest_band('E', 2, wobble=1.0)
    for cx, cy_, rx, ry in ((118, 12, 10, 7), (100, 46, 6, 3), (6, 40, 5, 5), (36, 6, 8, 3), (124, 46, 5, 4), (100, 14, 4, 3),
                            (14, 8, 5, 4), (50, 46, 4, 2.5), (82, 44, 3, 2), (30, 46, 3, 2)):
        r.copse(cx, cy_, rx, ry)
    for x in range(44, 92):                                                       # woods close the hill's sides (the ditch is the way)
        for y in range(0, 22):
            if m.ht[y, x] == 0 and m.cls[y, x] in '.t' and not r.road_mask[y, x] and (x < 50 or x > 80): m.cls[y, x] = 'T'
    r.finish_plan(border=0)
    # ledges: the paddock's bank drops to the road (one way)
    CK.ledge(r, 30, 46, 30)
    for y in (29, 30, 31):
        for x in (29, 47):
            if m.cls[y, x] in '.t': m.cls[y, x] = 'T'
    CK.grass_fields(r, [(30, 40, 4), (46, 40, 4.5), (78, 38, 4), (106, 38, 4.5), (110, 26, 3.5), (16, 34, 3), (52, 28, 3),
                        (88, 46, 3), (118, 38, 3), (8, 48, 3), (62, 46, 3), (74, 26, 3)])
    CK.woods(r, CK.ELOWEN, scale=12.0, accents={'blossom': 0.02, 'red': 0.01})
    ev = old_events('540_route3_route4.yaml', 540)
    # ---- events
    r.add({'type': 'warp', 'name': 'Mine mouth', 'at': [9, ym + 2], 'link': 'R3_MINE', 'arrive': [9, ym + 3, 'down'], 'se': 'Door exit', 'fixed': True},
          sign((25, 44), 'Road sign', "THISTLEDOWN LEA -- The lands of House Thistledown (extinct). v The Dyers' Ford - -> Gossamer Wood & Briarwick - ^ Thistledown Manor (PRIVATE. DECEASED.)"),
          once('The Lea', (22, 46), [J('happy', 'Mum says the Thistledowns were actors. All of them. Even the dog. They played Saltmere for a hundred years and then they all died in the same winter.'),
               J('neutral', "People say they're still up there. Rehearsing. I'd like to see that. From a distance. A long distance.")]),
          sign((63, y1 + 2), 'Manor sign', 'THISTLEDOWN MANOR\nHome of the Thistledown Players. Closed since AF 211.'),
          talk('Drover', (40, 26), 'NPC 25', ['Drover: Race you to the fence!', '(He wins. He always wins. He has a Ponyta.)']),
          talk('Ponyta', (36, 22), 'Followers/PONYTA', ['(It tosses its mane. Show-off.)'], move='random'),
          talk('Fisherman on the bridge', (25, cy[25] - 6), 'trainer_FISHERMAN', ["Fisherman: Bridge toll's a copper. Nobody's collected it since the house died. I just tell people. Habit."], d='left'),
          hidden((26, cy[26] + 6), 'GREATBALL', 'HiddenItem (under the bridge)'),
          {'type': 'event', 'name': 'Mower', 'at': [80, 40], 'pages': [
              {'graphic': {'sprite': 'NPC 03', 'dir': 'down'}, 'trigger': 'action', 'commands': [
                  "Mower: Nobody's mown the Lea in sixty years. You can't buy land off a dead family. They won't come to the door.",
                  {'if': '!pfm?(:mowers_heal)', 'then': ['Mower: Sit by the fire a bit. Kettle\'s on.', {'heal': True}, {'script': 'pfm_set(:mowers_heal)'}]}]},
              {'cond': {'switch': 'CH2_THISTLE_DONE'}, 'graphic': {'sprite': 'NPC 03', 'dir': 'down'}, 'trigger': 'action', 'commands': [
                  'Mower: Woman in grey came through at dawn with two others. Shears in her belt. Nodded to me. Mannerly. Went toward the wood.']}]},
          trainer((52, 38), 'PICNICKER', 'Edie', "Ada beat me on Windfall Row last year. I've been training on the Lea all spring.", "...I'll write to Ada. I'll lie.", d='down'),
          at(ev['Bryony'], 36, 32), trainer((74, 46), 'FISHERMAN', 'Hale', 'You scared the fish! Now you owe me a battle.', 'Reeled in a loss. Happens.', d='down'),
          trainer((92, 28), 'TWINS', 'Bel & Bea', 'Twins: We battle together! Always together!', "Twins: Saltmere's south. They do plays there!", d='down', double=True),
          trainer((112, 34), 'YOUNGSTER', 'Corin', "Saltmere badge? Prove it!", "My team's the coolest! ...Was.", d='left'),
          obj('Broken mill', (96, cy[96] - 6), ['The broken mill. The wheel is stuck half in the race. Someone has fished it clean of Magikarp.']),
          obj('Bamboo stand', (112, 23), ['A bamboo stand, planted by a Thistledown who wanted "something foreign". The Pancham agree.']),
          talk('Pancham', (108, 23), 'Followers/PANCHAM', ['(It glares at you over a bamboo shoot. Respect.)'], move='random'),
          obj('Road Stone II-b', (122, 29), ["ROAD STONE II-b. THE WEAVERS' ROAD. \"Briarwick 1.\" The '1' has been scratched to a '2' and back again."]),
          obj('Gateposts', (64, y1 - 2), ['Two stone gateposts with the Thistledown thistle carved on them. No gate. Gates are for people who expect visitors.']),
          obj('The Ha-ha', (82, 2), ['(The sunken wall\'s ditch runs round the back of the hill to an overgrown garden. A cellar door, barred from inside. Something is digging behind it.)']),
          talk('Greavard', (80, 4), 'Followers/GREAVARD', ['(It is digging very seriously. It does not want to be interrupted. It wags anyway.)'], move='random'),
          hidden((84, 3), 'RAREBONE', 'HiddenItem (the Ha-ha)'),
          obj('Topiary', (58, 14), ['A topiary garden gone wild. One bush was a Ponyta once. Now it is a Ponyta that has seen things.']),
          {'type': 'berry', 'at': [30, 34], 'berry': 'CHERIBERRY'}, item((118, 27), 'SUPERPOTION'), item((4, 34), 'POKEBALL'), item((70, 52), 'GREATBALL'))
    r.seat_events(on='.dt')
    CK.clear_around(r)
    fd = m.front('sh_big', 66, y2 - 3, 'R3_MANOR', 'Manor door')
    r.events += [e for e in m.events if e.get('link') == 'R3_MANOR' or e.get('name') == 'Locked door']; m.events = []
    m.stamp('pf_minemouth', 8, ym, mark='B'); m.cls[ym + 2, 9] = 'd'
    # the manor's ruined wall round its terrace, gateposts at the stair, the topiary garden
    for x in range(52, 82):
        y = y1 - 3
        if abs(x - 65) <= 2: continue
        if m.free(x, y, 1, 1, on='.t') and vnoise(x, 0, 5401, 3.0) > 0.3: m.stamp('nr_wall_' + ('w' if x == 52 else 'e' if x == 81 else 'm'), x, y, mark='B')
    for gx in (63, 67): r.near('nr_col', gx, y1 - 3, on='.t', r=1)
    for (x, y) in ((56, 14), (59, 15), (56, 17), (59, 18), (73, 14), (76, 15), (73, 17), (76, 18)):
        r.near(random.Random(x + y).choice(['nt_bush0', 'nt_bush1', 'nt_azalea0', 'nt_shrub0']), x, y, on='.t', r=1)
    r.near('nr_ruin', 94, 44, on='.t', r=3)                                       # the broken mill
    for n, x, y in (('sh_campfire', 78, 41), ('hb_tables', 83, 41), ('pf_hayrick', 76, 37), ('pf_hayrick', 86, 37), ('pf_logbench', 80, 44)):
        r.near(n, x, y, on='.d', r=3)
    for (x, y) in ((110, 16), (113, 15), (116, 17), (107, 18), (114, 20)):
        r.near('pf_bamboo', x, y, on='.t', r=2)
    m.fence(29, 47, 17, gaps=((37, 38),)); m.fence(29, 47, 27, gaps=((42, 43),))
    m.cls[bridge and 0 or 0, 0] = m.cls[0, 0]
    CK.props(r, ['nt_boulder', 'nt_rocks_s0', 'nt_rocks_s1', 'nt_log', 'nt_stump'], 24, box=(0, 20, W, 50), clump=3, seed=7)
    for (x, y) in ((40, cy[40] - 5), (60, cy[60] - 5), (84, cy[84] - 5), (114, cy[114] - 5), (50, cy[50] + 5), (10, cy[10] - 5)):
        r.near(random.Random(x).choice(['nt_reed1', 'nt_reed0']), x, y, on='.', r=2)
    CK.fringe(r, CK.FRINGE['meadow'], 200, seed=1, near_forest=5)
    CK.fringe(r, CK.FRINGE['orchard'], 14, box=(2, 20, W - 2, 50), seed=2, near_forest=0)
    CK.undergrowth(r, 320, seed=3)
    CK.props(r, ['nt_reed1', 'nt_reed1', 'nt_fern1'], 40, box=(0, 40, W, 62), clump=2, seed=13)
    r.dress(trees=('tr_oak',), n_trees=0, copses=0, scatter=0)
    for x, y in bridge: m.cls[y, x] = 'w'
    r.paint(glint=0.0)
    CK.paint_extras(r)
    bx = sorted({x for x, y in bridge})
    for x, y in bridge:
        if m.inb(x, y): m.L[1, y, x] = K.P1('sb_w' if x == bx[0] else 'sb_e' if x == bx[-1] else 'sb_m')
    # wildflower meadows in bands of colour
    FL = K.DECOR_SH['flowers']
    for i, (cx_, cy_, rx, ry, ks) in enumerate(((28, 14, 6, 3, (0, 4)), (44, 46, 7, 2, (2, 3)), (90, 40, 6, 2, (1, 5)), (108, 44, 6, 2, (6, 7)),
                                                (120, 26, 5, 3, (8, 9)), (16, 42, 4, 2, (10, 11)), (62, 40, 5, 2, (0, 1)), (74, 18, 4, 2, (2, 6)))):
        CK.meadow(r, cx_, cy_, rx, ry, tiles=[FL[k] for k in ks], p=0.75, seed=i)
    CK.shore(r, wet=0, wrack=0, shallows=0.05, kelp=0.05, chalk_rocks=False)
    CK.scatter_quiet(r, 16)
    h = head(540, 'Thistledown Lea', field='MEADOW', bgm='Route 3',
             connections=[{'dir': 'S', 'offset': 20, 'to': 552, 'to_offset': 39}, {'dir': 'E', 'offset': 30, 'to': 524, 'to_offset': 50}], tone=[6, 4, -2, 0])
    h['walk_from'] = [[70, 53]]                                                        # the islet (Surf, later)
    r.write(h, '540_thistledown_lea.yaml', '# Thistledown Lea (540). WRITTEN BY layouts/routes_craft.py - edit that script.\n', '/tmp/rt/540.png' if PREV else None)


BUILD[540] = build_540


# ====================================================================================================== 524 Gossamer Wood
def build_524():
    """Gossamer Wood (90x110, SILKWOOD): the silk forest that gives Briarwick its trade; ancient trees hung with silk.
    From Thistledown Lea (W) the trail climbs to the upper wood (stairs) and on to Briarwick's gate (N).  A white stream
    falls off the upper wood and runs south-west through the trees: the Weft Bridge, a span of spun silk as thick as a
    road, carries the east path over it to Woodward's Hut in the central clearing (canopy walkways between the giant
    trunks); on the corded forest road south the fallen giant is the bridge.  Side loops: the mushroom ring (NW, upper
    wood), the cocoon grove with its racks and weavers (SW), the Giga Drain grove (NE, over the stepping stones).  East:
    the Cut tree and the Veil to the Deepwood.  Secret: the Unpicked Seam (SE), a silk wall that parts only at night.
    Two one-tile pinch points wait for the puzzle engineer's silk curtains (REQUESTS 19)."""
    W, H = 90, 110
    r = Route(524, W, H, 'forest', base='T')
    m = r.m
    # ---- the upper wood (h1) across the north
    lipy = colmap(r, lambda x: 26 + 2.5 * (vnoise(x, 0, 5241, 10.0) - 0.5) * 2 + bump(x, 80, 8, 3))
    for x in range(W):
        m.ht[:lipy[x] + 1, x] = 1
    CK.smooth_ht(m, 1, 2)
    # ---- the white stream: from the north edge, over the terrace lip (waterfall), south-west through the wood
    stream = [(68, 0), (66, 12), (64, lipy[64] - 3), (64, lipy[64] + 4), (60, 36), (58, 46), (54, 58), (48, 70), (40, 80), (28, 92), (16, 102), (8, 109)]
    CK.stream(r, stream, w=3.2, c='w', only='T.t')
    # ---- trails
    main = [(0, 51.5), (12, 51), (22, 48), (28, 40), (31, lipy[31] + 4)]
    r.road(main, w=3.0, open_=(2, 4))
    CK.stair(r, 30, lipy[31], w=3, h=1)
    r.road([(31, lipy[31] - 2), (34, 20), (40, 13), (45, 6), (45, 0)], w=3.0, open_=(2, 4))
    r.exit('W', 50, 4)
    m.cls[0:3, 44:47] = 'd'
    # the fork round the great tree (the east branch narrows to one tile: the teach curtain)
    r.lane([(31, 20), (26, 15), (30, 9), (40, 13)], w=2.2, open_=(1, 2))
    # east: over the Weft Bridge to Woodward's clearing, the Cut tree and the Veil
    r.lane([(28, 40), (40, 44), (52, 46)], w=2.6, open_=(1, 3))
    r.lane([(64, 46), (72, 47), (84, 48), (89, 48)], w=2.4, open_=(1, 3))
    r.clearing(70, 52, 8, 6)
    # the corded forest road south, over the fallen giant
    r.lane([(22, 48), (22, 60), (30, 72), (39, 77)], w=2.6, open_=(1, 3))
    r.lane([(39, 84), (41, 96), (41, 106), (41, 109)], w=2.6, open_=(1, 3))
    # the cocoon grove (SW) and its loop; the one-tile twist run back to the road
    r.lane([(22, 60), (12, 68), (10, 80), (16, 88), (26, 84)], w=2.0, open_=(1, 3))
    r.clearing(12, 80, 6, 5)
    # the mushroom ring (NW, upper wood); the Giga Drain grove (NE, over the stepping stones)
    r.lane([(34, 20), (20, 16), (12, 10)], w=2.0, open_=(1, 3)); r.clearing(14, 10, 6, 4)
    r.lane([(45, 8), (56, 9), (70, 12), (76, 14)], w=2.0, open_=(1, 2)); r.clearing(77, 14, 6, 4)
    # the Unpicked Seam (SE): a pocket behind a night silk wall
    r.lane([(74, 56), (74, 66), (74, 76), (74, 79)], w=2.0, open_=(1, 2))
    r.pocket(77, 85, 6, 5, gate=None)
    CK.grass_fields(r, [(14, 48, 3), (24, 66, 3), (36, 42, 3), (70, 58, 3), (16, 76, 2.5), (38, 92, 2.5), (14, 12, 2.5), (38, 20, 2.5), (78, 16, 2.5)])
    r.finish_plan(border=0)
    m.cls[106:110, 40:43] = 'd'
    sx = 63
    CK.waterfall(r, sx, sx + 2, lipy[sx + 1])
    # the Weft Bridge (E-W, spun silk) and the fallen giant (N-S)
    weft_y = None
    for y in range(40, 52):
        xs = [x for x in range(50, 68) if m.cls[y, x] == 'w']
        if xs and 46 <= y <= 48: weft_y = 46; break
    weft_y = 46
    wxs = [x for x in range(48, 70) if m.cls[weft_y, x] == 'w' or m.cls[weft_y - 1, x] == 'w' or m.cls[weft_y + 1, x] == 'w']
    wx0, wx1 = min(wxs) - 1, max(wxs) + 1
    weft = []
    for x in range(wx0, wx1 + 1):
        for k, y in enumerate((weft_y - 1, weft_y, weft_y + 1)):
            weft.append((x, y, 'nms'[k]))
            if m.cls[y, x] != 'w': m.cls[y, x] = 'w'
    r.lane([(52, 46), (wx0 - 1, weft_y)], w=2.6, open_=(1, 2)); r.lane([(wx1 + 1, weft_y), (64, 46)], w=2.6, open_=(1, 2))
    lys = [y for y in range(70, 90) if m.cls[y, 39] == 'w' or m.cls[y, 40] == 'w']
    ly0, ly1 = min(lys) - 1, max(lys) + 1
    giant = [(x, y) for y in range(ly0, ly1 + 1) for x in (39, 40)]
    for x, y in giant: m.cls[y, x] = 'w'
    for x in (38, 41):                                                   # the log's flanks: rough water, no wading
        for y in range(ly0, ly1 + 1):
            if m.cls[y, x] in '.dt': m.cls[y, x] = 'T'
    # stepping stones to the Giga Drain grove
    st = [(x, 11) for x in range(56, 78) if m.cls[11, x] == 'w']
    CK.stones(r, st)
    # one-tile pinch points for the puzzle engineer's silk curtains
    PINCH = {'teach': (28, 12), 'twist': (21, 86)}
    for (px, py) in PINCH.values():
        for dx in (-1, 1):
            if m.cls[py, px + dx] in '.t' and not r.road_mask[py, px + dx]: m.cls[py, px + dx] = 'T'
        m.cls[py, px] = 'd'
    CK.woods(r, CK.GOSSAMER, scale=10.0, accents={'blossom': 0.01})
    J_ = J
    ev = old_events('524_reskin.yaml', 524)
    entry = ev['Wood entry 1']['pages']
    for i, y in enumerate((50, 51, 52, 53)):
        r.events.append({'type': 'event', 'name': 'Wood entry %d' % (i + 1), 'at': [4, y], 'pages': entry, 'fixed': True}); m.taken[y, 4] = True
    veil = ev['Juno at the Veil 1']['pages']
    tape = lambda i, x: {'type': 'event', 'name': 'Accord cordon %d' % i, 'at': [x, 104], 'fixed': True, 'pages': [
        {'graphic': {'tile': barrier_tile()}, 'trigger': 'action', 'commands': [
            'ACCORD CORDON: The forest road back to Windfall Row and the Landing, taped off. A sign faces the farms: CLOSED BY ORDER OF THE ACCORD.',
            J_('sad', "That's the way I used to come. Four hours with Parsnip. Now it's two days and a pageant.")]},
        {'cond': {'var': ['BRIARWICK_GLASSWOOD', 1]}, 'through': True, 'commands': []}]}
    for i, x in enumerate((40, 41, 42)): r.events.append(tape(i + 1, x)); m.taken[104, x] = True
    silk = int(np.array(STAMPS['pf_p_silk1']['layers']).max()); logt = int(np.array(STAMPS['fw_log_m']['layers']).max())
    r.add({'type': 'warp', 'name': 'To Windfall Row', 'at': [41, 109], 'to': {'map': 521, 'x': 1, 'y': 10, 'dir': 'left'}, 'fixed': True},
          {'type': 'warp', 'name': 'To Windfall Row b', 'at': [40, 109], 'to': {'map': 521, 'x': 1, 'y': 9, 'dir': 'left'}, 'fixed': True},
          {'type': 'warp', 'name': 'To Windfall Row c', 'at': [42, 109], 'to': {'map': 521, 'x': 1, 'y': 11, 'dir': 'left'}, 'fixed': True},
          {'type': 'warp', 'name': 'To Briarwick', 'at': [44, 0], 'link': 'WOOD_BRIAR', 'arrive': [44, 1, 'down'], 'fixed': True},
          {'type': 'warp', 'name': 'To Briarwick b', 'at': [45, 0], 'to': {'map': 120, 'x': 36, 'y': 62, 'dir': 'up'}, 'fixed': True},
          {'type': 'warp', 'name': 'To Briarwick c', 'at': [46, 0], 'to': {'map': 120, 'x': 36, 'y': 62, 'dir': 'up'}, 'fixed': True},
          {'type': 'cut_tree', 'at': [82, 48], 'name': 'CutTree'},
          {'type': 'warp', 'name': 'To Deepwood', 'at': [89, 48], 'link': 'WOOD_DEEP', 'arrive': [88, 48, 'left'], 'fixed': True},
          sign((44, 103), 'Cordon notice', 'CLOSED BY ORDER OF THE ACCORD. From this side you can see the glass across the lane, a mile on.'),
          at(ev['Silk-picker'], 66, 48), at(ev['Old Weaver'], 18, 64),
          obj('Shrine stone', (12, 8), ['A small mossy shrine stone. A carving of three beasts chasing a masked figure. Someone has left a honey bun in front of the masked one, not the three.',
              J('neutral', "That's the Pageant. That's the play we saw. ...Somebody likes the Ogre better.")]),
          talk('Kestrel', (44, 6), 'trainer_RIVAL1', ["Kestrel: Briarwick's just ahead. Try not to get lost in the webs. ...Not that I'd come looking."]),
          trainer((36, 30), 'TWINS', 'Mo & Jo', 'We battle together!', 'We lose together.', d='right', double=True),
          trainer((26, 68), 'BUGCATCHER', 'Tobin', 'My bugs love the silk here!', 'Careful in the webs past here!', d='down'),
          trainer((46, 45), 'BUGCATCHER', 'Reed', 'You walked right into my web!', "The wood's full of better bugs than mine, huh.", d='left'),
          trainer((40, 16), 'AROMALADY', 'Petra', 'Smell that? Night-blooming gossamer.', 'What a lovely, fierce scent you have.', d='down'),
          trainer((14, 52), 'CAMPER', 'Bram', 'Camping in Gossamer? Battle first, questions later!', "Lost to a tourist. Don't tell anyone.", d='down'),
          item((78, 14), 'TM19'), item((8, 82), 'REPEL'), item((74, 50), 'POTION'), item((34, 36), 'ETHER'),
          {'type': 'event', 'name': 'HiddenItem', 'at': [18, 12], 'pages': ev['HiddenItem']['pages']},
          obj('Cocoon grove', (12, 77), ['A grove of silk cocoons the size of lanterns, hung in rows. Each has a weaver\'s knot-mark tied to it.']),
          talk('Weaver (harvest)', (16, 81), 'NPC 13', ['Weaver: One cocoon in three. Always leave two. The wood counts.']),
          talk('Weaver (racks)', (8, 83), 'NPC 27', ['Weaver: The racks dry the silk in the dark. Sun makes it brittle. Like Kestrel.']),
          talk('Weaver (spool)', (66, 56), 'NPC 18', ["Weaver: The Weft Bridge? Spun in my great-grandmother's day. Every guild in Briarwick gave a thread. It's stronger than stone. It's ruder than stone, too. Mind the bounce."]),
          obj('Mushroom ring', (14, 11), ['A ring of pale mushrooms. At night, they say, it glows, and the Morelull dance.']),
          trial('Monkey shrine', (19, 9), 'SHRINE_WOOD'),
          obj('The Weft Bridge', (wx0 - 1, weft_y + 1), ['THE WEFT BRIDGE. A rope of spun silk as thick as a road, woven by every guild in Briarwick. It hums when you walk on it.']),
          obj('Fallen giant', (42, ly0 - 1), ['A fallen giant tree, hollow end to end, lying across the stream. The weavers use it as a bridge. The Venonat use it as a hotel.']),
          {'type': 'event', 'name': 'Silk seam', 'at': [74, 80], 'fixed': True, 'pages': [{'graphic': {'tile': K.P1('pf_p_silk1') if False else silk}, 'trigger': 'action', 'commands': [
              {'if': 'PBDayNight.isNight?', 'then': ['The silk wall has loosened in the dark. It parts like a curtain.', {'selfswitch': ['A', True]}],
               'else': ['A wall of silk, tight as a drum. At night, the weavers say, the seams unpick themselves.']}]},
              {'cond': {'self': 'A'}, 'through': True, 'commands': []}]},
          {'type': 'event', 'name': 'Sap tree duel', 'at': [78, 86], 'pages': [{'commands': []},
              {'graphic': {'sprite': 'Followers/HERACROSS', 'dir': 'left'}, 'trigger': 'action',
               'commands': [{'comment': 'Condition: badges >= 2 && !quest_done(:EL_HORN_AND_PINCER)'}, {'script': 'pf_trial_talk(:SAP_TREE)'}]}]},
          obj('Sap tree', (80, 85), ['A weeping sap tree. Two very large beetles are disputing ownership of it.']))
    # the two Horn-and-Pincer shortcuts (TRIAL_EVENTS 524): a silk wall and a fallen log, each gone when its beetle clears it
    r.lane([(64, 42), (60, 36), (54, 30)], w=1.6, open_=None) if False else None
    r.events.append({'type': 'event', 'name': 'Silk wall', 'at': [31, 25], 'fixed': True, 'pages': [{'commands': []},
        {'graphic': {'tile': silk}, 'trigger': 'action', 'commands': [{'comment': "Condition: quest_flag(:EL_HORN_AND_PINCER, :helper) != :heracross"},
                                                                       'A wall of silk, tight as a drum. Something with a horn could tear it.']}]})
    r.events.append({'type': 'event', 'name': 'Fallen log', 'at': [20, 87], 'fixed': True, 'pages': [{'commands': []},
        {'graphic': {'tile': logt}, 'trigger': 'action', 'commands': [{'comment': "Condition: quest_flag(:EL_HORN_AND_PINCER, :helper) != :pinsir"},
                                                                       'A fallen log across the path. Something with pincers could crush it.']}]})
    for i, y in enumerate((47, 48, 49)): r.events.append({'type': 'event', 'name': 'Juno at the Veil %d' % (i + 1), 'at': [79, y], 'pages': veil, 'fixed': True}); m.taken[y, 79] = True
    for x, y in ((31, 25), (20, 87), (74, 80)): m.taken[y, x] = True
    r.seat_events(on='.dt')
    CK.clear_around(r)
    fd = m.front('gl_shed', 70, 51, 'WOOD_HUT', "Woodward's Hut door")
    r.events += [e for e in m.events if e.get('link') == 'WOOD_HUT']; m.events = []
    # ---- the weavers' wood: giant silk-hung trees, racks, spools, looms, webs, drapes, cocoons
    for n, x, y in (('pf_g_tree4p', 58, 50), ('pf_g_tree2', 79, 52), ('pf_g_tree4p', 22, 28), ('pf_g_tree2', 46, 22), ('pf_g_tree6', 4, 58),
                    ('pf_g_tree4p', 50, 86), ('pf_g_tree2', 6, 30), ('pf_g_tree4p', 72, 26), ('pf_g_tree2', 30, 98), ('pf_g_tree4p', 78, 94)):
        if m.free(x, y, STAMPS[n]['w'], STAMPS[n]['h'], on='.tT'): m.stamp(n, x, y, mark='B', blend=True)
    for n, x, y in (('gw_rack', 6, 76), ('gw_rack', 16, 74), ('gw_spool', 18, 84), ('pf_p_loom', 66, 54), ('gw_spool', 76, 55),
                    ('pf_p_net', 62, 56), ('pf_logbench', 68, 58), ('pf_p_lantern', 64, 50), ('gw_rack', 76, 58), ('sh_campfire', 72, 60)):
        r.near(n, x, y, on='.d', r=3)
    rng = random.Random(524)
    CK.drapes_along(r, every=4, seed=1)
    for _ in range(W * H // 28):                                                    # silk: webs across gaps, drapes, cocoons
        nm = rng.choice(['pf_p_web', 'pf_p_web1', 'gw_drape0', 'gw_drape1', 'gw_cocoons', 'gw_cocoons', 'pf_p_strand_w', 'pf_p_strand_p'])
        x, y = rng.randrange(W), rng.randrange(H); st_ = STAMPS[nm]
        if nm.startswith('gw_drape') or nm == 'gw_cocoons':               # drapes hang from the canopy at the wood's edge
            if y + st_['h'] < H and (m.cls[y, x:x + st_['w']] == 'T').all() and m.free(x, y + 1, st_['w'], st_['h'] - 1, on='.dt'):
                m.stamp(nm, x, y, mark=None)
        elif m.free(x, y, st_['w'], st_['h'], on='.'): m.stamp(nm, x, y, mark=None)
    CK.props(r, ['nt_log', 'nt_stump', 'nt_birch_h', 'nt_rocks_s0', 'nt_stump_big'], 26, box=(0, 0, W, H), clump=3, seed=7)
    CK.fringe(r, CK.FRINGE['wood'], 120, seed=1, near_forest=3)
    CK.undergrowth(r, 300, kinds=('nt_fern0', 'nt_fern1', 'nt_bush0', 'nt_bush1', 'nt_shrub0', 'ak_fern', 'nt_shrub1'), seed=3)
    for (x, y) in ((44, 50), (36, 56), (52, 62), (30, 80), (50, 74), (62, 24), (66, 32)):
        r.near(rng.choice(['nt_reed1', 'nt_reed0']), x, y, on='.', r=2)
    r.dress(trees=('tr_oak',), n_trees=0, copses=0, scatter=0)
    r.paint(glint=0.0)
    CK.paint_extras(r)
    for x, y, k in weft: m.L[1, y, x] = K.P1('gw_bridge_' + k); m.L[2, y, x] = 0
    for x, y in giant:
        k = 'n' if y == ly0 else 's' if y == ly1 else 'm'
        L = STAMPS['fw_log_' + k]['layers']
        m.L[1, y, x] = int(L[1][0][x - 39]) or int(L[2][0][x - 39]) or int(L[0][0][x - 39])
    # canopy walkways between the clearing's giant trunks (overhead rope bridges)
    for x in range(62, 79): m.L[2, 49, x] = K.P1('fw_walk_h') if m.L[2, 49, x] == 0 else m.L[2, 49, x]
    for i, (cx_, cy_, rx, ry) in enumerate(((70, 60, 4, 2), (14, 12, 3, 2), (78, 16, 3, 2), (26, 70, 3, 2), (36, 44, 3, 1.5))):
        CK.meadow(r, cx_, cy_, rx, ry, tiles=[K.DECOR_SH['flowers'][k] for k in (2, 11, 4)], p=0.6, seed=i)
    CK.scatter_quiet(r, 12)
    h = head(524, 'Gossamer Wood', field='SILKWOOD', bgm='Route 3', biome='forest',
             connections=[{'dir': 'W', 'offset': 50, 'to': 540, 'to_offset': 30}], tone=[-28, -8, -30, 25],
             fog={'name': 'prismfall_spores', 'opacity': 40, 'blend': 1, 'zoom': 100, 'sx': 1, 'sy': -1})
    h['metadata']['BattleBack'] = 'forest'
    h['walk_from'] = [[78, 86]]                                                    # the Unpicked Seam (behind the night silk wall)
    r.pinch = PINCH
    r.write(h, '524_gossamer_wood.yaml', '# Gossamer Wood (524). WRITTEN BY layouts/routes_craft.py - edit that script.\n', '/tmp/rt/524.png' if PREV else None)
    print('524 silk-curtain pinch points:', PINCH)


BUILD[524] = build_524


# ====================================================================================================== 520 The Ferrymen's Mile
def build_520():
    """The Ferrymen's Mile (64x110, MEADOW): the lane north from Ferrow's Landing over the stile, along the chalk sea
    cliff (Wingull posts, the Gullwatch lookout) to the Hale Bell on its post above the sea, where the Strand Road turns
    west (the quarantine roadblock).  East of the lane Hale's Bramble climbs in three berry terraces to the picking shed;
    west, the Minding Hedges (a three-turn maze with a hidden Potion); Juno's fenced catching clearing; the duck pond; the
    sheepfold of drystone walls where three Wooloo keep getting out; ledges drop from the fold to the lane (the shortcut
    home); the old ferry-toll booth; Road Stone I.  Secret: the Smuggler's Stair behind the booth (Cut), down to the
    Ferryman's Rest on the beach under the cliff."""
    W, H = 64, 110
    r = Route(520, W, H, 'shore', kit={1: 'akc', 2: 'sh3', 3: 'sh3', 4: 'sh3', 'default': 'sh3'}, base='.')
    m = r.m
    m.ht[:, :] = 1
    # ---- the sea under the cliff walk (south-west)
    for y in range(80, H):
        d = 7 + int(3 * (vnoise(0, y, 520, 9.0) - 0.5) * 2) + max(0, (y - 96) // 3)
        for x in range(0, d + 3):
            m.ht[y, x] = 0
            m.cls[y, x] = ('W' if x < d - 4 else 'w') if x < d else 's'
    CK.smooth_sea(m, 2)
    # the Ferryman's Rest: a beach pocket under the toll booth's cliff
    m.ht[93:102, 0:12] = 0
    for y in range(93, 102):
        for x in range(0, 12):
            if m.cls[y, x] not in 'wW': m.cls[y, x] = 's'
    # ---- Hale's Bramble: three terraces east of the lane
    for (x0, x1, y0, y1, h) in ((36, 60, 34, 60, 2), (40, 60, 34, 52, 3), (44, 60, 34, 45, 4)):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if x - x0 + (y1 - y) * 0.15 > 1.5 * vnoise(x, y, 5201 + h, 4.0): m.ht[y, x] = max(m.ht[y, x], h)
    for h in (2, 3, 4): CK.smooth_ht(m, h, 2, box=(30, 28, 64, 64))
    road = [(16, 109), (16, 101), (19, 93), (24, 85), (22, 77), (22, 72), (27, 62), (31, 52), (28, 41), (33, 29), (31, 16), (31, 0)]
    r.road(road, w=3.0, open_=None)
    r.road([(22, 74), (12, 73), (0, 73.5)], w=3.0, open_=None)
    r.exit('S', 15, 4); r.exit('N', 30, 4); r.exit('W', 72, 4)
    for (sx, h) in ((38, 2), (42, 3), (46, 4)):
        yy = max(y for y in range(H) if m.ht[y, sx + 1] == h)
        CK.stair(r, sx, yy, w=2, h=h)
    r.lane([(32, 56), (38, 62)], w=2.0, open_=None)
    r.lane([(22, 84), (14, 84), (10, 86)], w=2.0, open_=None)                     # to the toll booth
    r.lane([(26, 60), (17, 62)], w=2.0, open_=None)                                # into the Minding Hedges
    r.lane([(32, 24), (44, 22), (48, 18)], w=2.0, open_=None)                      # to the sheepfold
    CK.stair(r, 12, 92, w=3, h=1)                                                  # the Smuggler's Stair
    CK.pond(r, 48, 72, 4.5, 2.6, c='p', rough=0.4)                                  # the duck pond
    r.forest_band('E', 6, wobble=3.0); r.forest_band('N', 4, wobble=2.0)
    for cx, cy_, rx, ry in ((52, 26, 4, 4), (8, 14, 6, 5), (46, 92, 7, 6), (56, 78, 4, 5), (10, 44, 5, 4), (20, 6, 5, 3),
                            (40, 100, 4, 3), (6, 30, 4, 4), (44, 6, 5, 3)):
        r.copse(cx, cy_, rx, ry)
    r.finish_plan(border=0)
    m.cls[86:92, 12:15] = np.where(m.cls[86:92, 12:15] == 'T', '.', m.cls[86:92, 12:15])
    # the sheepfold's ledges: down to the lane, the shortcut home (one way)
    CK.ledge(r, 36, 50, 31)
    for y in (30, 31, 32):
        for x in (35, 51):
            if m.cls[y, x] in '.t': m.cls[y, x] = 'T'
    CK.grass_fields(r, [(28, 90, 3), (32, 84, 3), (38, 70, 3.5), (24, 44, 3.5), (20, 30, 3), (40, 40, 3), (48, 50, 2.5), (14, 52, 3),
                        (26, 104, 2.5), (54, 64, 3), (38, 16, 3), (12, 36, 2.5)])
    CK.woods(r, CK.ELOWEN, scale=12.0, accents={'blossom': 0.02})
    ev = old_events('520_reskin.yaml', 520)
    tut = [{'cond': {'switch': 'CH1_K1_DONE'}, 'trigger': 'touch', 'commands': [{'if': "$game_self_switches[[520, 0, 'TUT']]", 'then': [], 'else': [
        J('happy', "Catching tutorial! Weaken it, then throw. Don't throw the Ball AT it, throw it NEAR it."),
        J('happy', 'I learned that the hard way. Sorry, Biscuit.'), {'script': 'pbReceiveItem(:POKEBALL, 5)'},
        {'script': "$game_self_switches[[520, 0, 'TUT']] = true"}]}]}]
    send = [{'commands': []}, {'cond': {'var': ['STORY_CHAPTER', 2]}, 'trigger': 'touch', 'commands': [{'if': 'pfm?(:ch2_sendoff)', 'then': [], 'else': RE.SENDOFF_520}]}]
    r.events += [dict(e, fixed=True) for e in line_events(r, 'Juno tutorial', 90, 10, 30, tut)]
    r.events += [dict(e, fixed=True) for e in line_events(r, 'Stile send-off', 98, 8, 24, send)]
    # playtest round 3 items 15-16: the send-off plays at the Hale Bell fork too (the farm is north of it, so a player who
    # rests at the Hale Farmhouse never passes the stile): touch lines across the lane north and south of the fork
    r.events += [dict(e, fixed=True) for e in line_events(r, 'Hale Bell send-off N', 68, 16, 30, send)]
    r.events += [dict(e, fixed=True) for e in line_events(r, 'Hale Bell send-off S', 79, 16, 30, send)]
    # the roadblock: the barricade spans the whole Strand Road (x 2, rows 72-75) and the ground either side of it is woods
    # down to the map edge, so the barricade is the only way to the W edge; it opens on the Chapter 1 rest (V102 >= 2), not
    # on the orchard (build.py `gates:` proves it shut)
    for y in list(range(64, 72)) + list(range(76, 81)):
        for x in range(0, 6):
            if m.cls[y, x] not in 'wWs': m.cls[y, x] = 'T'; r.road_mask[y, x] = False
    B = barrier_tile()
    bar = lambda i, y: {'type': 'event', 'name': 'Accord barrier %d' % i, 'at': [2, y], 'fixed': True, 'pages': [
        {'graphic': {'tile': B}, 'trigger': 'action', 'commands': ['Accord Guard: Hold. Quarantine order: nobody leaves the Landing without papers.']},
        {'cond': {'var': ['STORY_CHAPTER', 2]}, 'through': True, 'commands': []}]}
    for i, y in enumerate((72, 73, 74, 75)): r.events.append(bar(i + 1, y)); m.taken[y, 2] = True
    r.add({'type': 'event', 'name': 'Professor Larch', 'at': [19, 70], 'pages': [
              {'commands': []}, {'cond': {'var': ['STORY_CHAPTER', 2]}, 'graphic': {'sprite': 'trainer_PROFESSOR', 'dir': 'down'}, 'commands': [
                  {'if': 'pfm?(:ch2_sendoff)', 'then': [P('LARCH', 'neutral', 'Off you go. Lecture Two is already drafted.')], 'else': RE.SENDOFF_520}]},
              {'cond': {'self': 'A'}, 'commands': []}]},
          {'type': 'event', 'name': 'Accord guard', 'at': [6, 71], 'pages': [                  # story/20_SCRIPT_CH0-2.md (Ch1 close, 2026-11-20)
              {'graphic': {'sprite': 'NPC 07', 'dir': 'down'}, 'commands': [
                  'Accord Guard: Hold. Quarantine order: nobody west of the Bell without papers.',
                  "Accord Guard: ...A Badge Case. A challenger. Challengers pass, that's older law than the quarantine. But they pass at first light, with the cliff patrol. Not a minute before.",
                  "Accord Guard: Go and get some sleep. The cliffs'll still be there in the morning. Mostly. They're chalk."]},
              {'cond': {'switch': 'CH1_ORCHARD_DONE'}, 'graphic': {'sprite': 'NPC 07', 'dir': 'down'}, 'commands': [
                  'Accord Guard: Hold. Quarantine order: nobody west of the Bell without papers.',
                  "Accord Guard: ...A Badge Case. A challenger. Challengers pass, that's older law than the quarantine. But they pass at first light, with the cliff patrol. Not a minute before.",
                  "Accord Guard: Go and get some sleep. The cliffs'll still be there in the morning. Mostly. They're chalk.",
                  "Accord Guard: You're the one stopping at the Hales'? Then eat whatever Wenna puts in front of you. That's an order. Hers, not mine."]},
              {'cond': {'var': ['STORY_CHAPTER', 2]}, 'graphic': {'sprite': 'NPC 07', 'dir': 'right'}, 'commands': [
                  'Accord Guard: Hold. Quarantine order: nobody leaves the Landing without papers.',
                  "Accord Guard: ...You've got a Badge Case. A challenger. Right. Challengers pass, that's older law than the quarantine.",
                  'Accord Guard: "Eighteen in Concord, One in Keeping." On you go. Saltmere\'s two days west. Mind the cliff path in wind.']}]},
          {'type': 'event', 'name': 'Accord guard (aside)', 'at': [7, 76], 'pages': [
              {'graphic': {'sprite': 'NPC 07', 'dir': 'up'}, 'commands': ['Second Guard: Nobody past. Orders came down this morning.']},
              {'cond': {'var': ['STORY_CHAPTER', 2]}, 'graphic': {'sprite': 'NPC 07', 'dir': 'right'}, 'commands': [
                  "Second Guard: (low) That's the null one from the dock. Captain said let them through, whatever happens.", 'Accord Guard: Which captain?',
                  "Second Guard: Didn't say. Came down from Crownhaven with a white seal on it.", '\\\\pf[ACCORD_GUARD,deadpan,sweat,Accord guard](They notice you listening.)',
                  'Accord Guard: Lovely weather.']}]},
          obj('The Hale Bell', (16, 70), ['THE HALE BELL: A ship\'s bell on a post above the sea cliff. The ferrymen rang it once the last boat was in.',
              'A cloth has been tied round the clapper.', J('sad', 'Dad tied that. The night they closed the strait.'),
              J('happy', "He's never untied a knot in his life. He cuts them. So if he says he'll untie it, he's been practising.")]),
          talk('Hay-cart Driver', (26, 70), 'NPC 11', ["Hay-cart Driver: Used to take me four hours to Briarwick and back by the forest road.",
               "Hay-cart Driver: Now it's all glass and I go round by Saltmere. Two days. Glass doesn't pay my horse."]),
          sign((10, 76), 'Hale Bell fork sign', "THE HALE BELL. <- LACECLIFF WALK, Marram Down and SALTMERE (the Strand Road). ^ Windfall Row. v Ferrow's Landing."),
          sign((18, 104), 'Road sign', "THE FERRYMEN'S MILE\nFerrow's Landing - Hale's Bramble - Windfall Row.\nMind the hedges. The hedges mind you."),
          at(ev['Pim'], 26, 66), at(ev['Dory'], 29, 46), at(ev['Farmhand'], 34, 64), at(ev['Under the stile'], 11, 99), at(ev['Stile'], 12, 98),
          at(ev['Scarecrow'], 44, 58), at(ev['Lookout board'], 10, 80), at(ev['Waystone'], 33, 8), at(ev['Old well'], 20, 52),
          trainer((36, 22), 'YOUNGSTER', 'Pip', "My squad's undefeated on this lane! It's a short lane.", 'Aw, my squad lost!', d='left'),
          trainer((25, 34), 'LASS', 'Wren', 'Birdies! Go!', 'My birdies! Oh, well done.', d='right'),
          obj('Ferry-toll booth', (13, 87), ['THE OLD FERRY-TOLL BOOTH. Fare board: "Landing to Saltmere, 3 coppers. Landing to the Strait, 5. Return, ask the captain."',
              'Under it, chalked: "STRAIT CLOSED." Under that, smaller: "for now"']),
          obj('Road Stone I', (19, 107), ['ROAD STONE I. THE STRAND ROAD. "Ferrow 0." Someone has taken a rubbing of it. Many someones.']),
          obj("Hale's Bramble", (36, 60), ["HALE'S BRAMBLE. Three terraces of bramble and berry. Wenna's cousin sells tarts at the shed. The tarts are better than Wenna's. Don't tell Wenna."]),
          talk("Wenna's cousin", (52, 38), 'NPC 16', ["Wenna's cousin: Berries are picked by the terrace. Bottom terrace is for tourists. Top terrace is for family.",
               "Wenna's cousin: You look like family. ...No, you look tired. Here."], again=["Wenna's cousin: Mind the brambles on the way down."]),
          {'type': 'berry', 'at': [40, 56], 'berry': 'ORANBERRY'}, {'type': 'berry', 'at': [46, 50], 'berry': 'PECHABERRY'},
          {'type': 'berry', 'at': [52, 43], 'berry': 'CHERIBERRY'}, {'type': 'berry', 'at': [56, 39], 'berry': 'ORANBERRY'},
          obj('The Minding Hedges', (16, 64), ['THE MINDING HEDGES. "Mind the hedges. The hedges mind you." A maze of three turns, planted by a ferryman who missed the sea.']),
          hidden((12, 59), 'POTION', 'HiddenItem (hedge maze)'),
          talk('Shepherd', (46, 20), 'NPC 20', ['Shepherd: Three of my Wooloo got out again. They roll. Downhill. Always downhill.',
               "Shepherd: If you see a Wooloo, walk it uphill. It'll be so surprised it'll follow you."]),
          talk('Wooloo', (40, 14), 'Followers/WOOLOO', ['Baaa. (It is rolling, very slowly, in no direction.)'], move='random'),
          talk('Wooloo ', (50, 26), 'Followers/WOOLOO', ['Baaa.'], move='random'),
          talk('Wooloo  ', (30, 78), 'Followers/WOOLOO', ['Baaa. (It has rolled a long way downhill. It looks pleased about it.)'], move='random'),
          obj('Duck pond', (44, 75), ['A duck pond with no ducks. A Ducklett is sitting on the reeds, looking as if it is waiting for some.']),
          item((50, 12), 'POKEBALL'), item((8, 50), 'POTION'), hidden((8, 98), 'BIGPEARL', 'HiddenItem (Ferryman\'s Rest)'),
          item((10, 97), 'REVIVE'), obj("The Ferryman's Rest", (9, 95), ["A rowboat hauled up in a sea cave. A name on the bow, painted out. Bootprints, small, going in and not out."]),
          {'type': 'cut_tree', 'at': [13, 89], 'name': 'CutTree'})
    r.seat_events(on='.dts')
    CK.clear_around(r)
    # the Minding Hedges: three hedge lines with alternating gaps (a three-turn maze)
    for y, gap in ((57, (17, 18)), (61, (10, 11)), (65, (17, 18))):
        for x in range(8, 21):
            if gap[0] <= x <= gap[1]: continue
            if m.free(x, y, 1, 1, on='.t'): m.stamp('nt_bush0' if (x + y) % 3 else 'nt_bush1', x, y, mark='B')
    for x in (7, 21):
        for y in range(57, 66):
            if m.free(x, y, 1, 1, on='.t') and not r.road_mask[y, x]: m.stamp('nt_bush0', x, y, mark='B')
    # Juno's catching clearing (fenced), the sheepfold's drystone walls, the bramble rows, the booth, the bell, carts
    for y in (82, 87): m.fence(26, 34, y, gaps=((29, 30),) if y == 87 else ())
    for (x0, x1, y) in ((38, 54, 10), (38, 54, 29)):
        for x in range(x0, x1 + 1):
            if abs(x - 46) <= 1 and y == 10: continue
            if m.free(x, y, 1, 1, on='.t'): m.stamp('nr_wall_' + ('w' if x == x0 else 'e' if x == x1 else 'm'), x, y, mark='B')
    for x in range(38, 60, 2):
        for y in range(34, 62):
            if m.ht[y, x] >= 2 and m.free(x, y, 2, 2, on='.t') and (y + x) % 5 == 0: m.stamp('ak_fern', x, y, mark='B')
    r.near('gl_shed', 52, 34, on='.t', r=3)                                         # the picking shed
    r.near('hb_shed', 11, 84, on='.d', r=2)                                         # the toll booth
    r.near('pf_bellpost', 15, 68, on='.d', r=2)
    r.near('pf_roadstone', 20, 106, on='.', r=2)
    for n, x, y in (('pf_sledge', 26, 74), ('hb_crates4', 24, 40), ('hb_barrel', 36, 64), ('pf_hayrick', 40, 64)):
        r.near(n, x, y, on='.', r=3)
    for y in range(78, 106, 6):                                                     # Wingull posts along the cliff walk
        xs = [x for x in range(2, 20) if m.ht[y, x] == 1 and m.cls[y, x] == '.' and m.ht[y, x - 1] == 0] if True else []
        if xs: r.near('hb_post1', xs[0] + 1, y, on='.', r=1)
    CK.props(r, ['ck_boulder', 'ck_pebbles', 'nt_rocks_s0', 'nt_stump', 'nt_log'], 20, box=(0, 40, W, H), clump=3, seed=7)
    for (x, y) in ((43, 70), (53, 71), (44, 75), (52, 74)): r.near('nt_reed1', x, y, on='.', r=2)
    CK.fringe(r, CK.FRINGE['meadow'], 160, seed=1, near_forest=5)
    CK.fringe(r, ['nt_pine_a', 'nt_pine_b', 'nt_teal_a'], 10, box=(0, 70, 30, H), seed=2, near_forest=0)
    CK.undergrowth(r, 220, seed=3)
    r.dress(trees=('tr_oak',), n_trees=0, copses=0, scatter=0)
    r.paint(glint=0.25)
    CK.paint_extras(r)
    CK.shore(r, wet=1, wet_noise=0.5, wrack=0.5)
    FL = K.DECOR_SH['flowers']
    for i, (cx_, cy_, rx, ry, ks) in enumerate(((30, 86, 4, 2, (2, 3)), (12, 30, 4, 2, (0, 4)), (40, 78, 4, 2, (5, 6)), (20, 56, 3, 2, (8, 9)),
                                                (52, 66, 3, 2, (1, 10)), (16, 80, 3, 1.5, (2, 3)), (34, 6, 4, 1.5, (11, 12)))):
        CK.meadow(r, cx_, cy_, rx, ry, tiles=[FL[k] for k in ks], p=0.7, seed=i)
    CK.scatter_quiet(r, 12)
    h = head(520, "The Ferrymen's Mile", field='MEADOW', bgm='Route 1',
             connections=[{'dir': 'S', 'offset': 11, 'to': 100, 'to_offset': 28}, {'dir': 'N', 'offset': 30, 'to': 521, 'to_offset': 58},
                          {'dir': 'W', 'offset': 72, 'to': 527, 'to_offset': 22}],
             fog={'name': 'prismfall_seamist', 'opacity': 30, 'blend': 0, 'zoom': 200, 'sx': 1, 'sy': 0}, tone=[4, 4, -4, 0])
    h['walk_from'] = [[9, 97]]                                                    # the Ferryman's Rest (behind the Cut bramble)
    # playtest round 3 item 15: with the barricade shut, nothing on the W edge (Lacecliff Walk) is reachable on foot from the
    # Landing (S edge) or from Windfall Row (N edge); build.py checks it on every build
    h['gates'] = [{'name': 'Hale Bell roadblock', 'from': [[16, 109], [31, 0]], 'sealed_edge': 'W'}]
    r.write(h, '520_ferrymens_mile.yaml', "# The Ferrymen's Mile (520). WRITTEN BY layouts/routes_craft.py - edit that script.\n", '/tmp/rt/520.png' if PREV else None)


BUILD[520] = build_520


# ====================================================================================================== 577 Frostwick Pass
def gust_event(i, at_):
    """a wind-gap cell: while the gap gusts (ROAD_GUST 1) the drift shows and stepping in throws you back down the gap"""
    push = ("pbSEPlay('Wind1') rescue nil\n"
            "PrismfallPuzzles.push_line(2, 'Gust')\n"
            "pbMessage(_INTL('A gust tears down the gap and throws you back!')) if !$PokemonGlobal.instance_variable_get(:@pf_gust_told)\n"
            "$PokemonGlobal.instance_variable_set(:@pf_gust_told, true)")
    return {'type': 'event', 'name': 'Gust %d' % i, 'at': list(at_), 'fixed': True, 'pages': [
        {'trigger': 'touch', 'through': True, 'commands': []},
        {'cond': {'var': ['ROAD_GUST', 1]}, 'graphic': {'tile': K.P1('fw_gust%d' % (i % 3))}, 'trigger': 'touch', 'through': True,
         'commands': [{'script': push}]}]}


def build_577():
    """Frostwick Pass (72x96, SNOWY_MOUNTAIN): the low pass over the hoar downs into Frostwick, claimed by both
    kingdoms.  The drove road climbs north from Spinners' Rise in three levels: past the bothy (rest, a hot drink) and the
    empty toll hut with its two disagreeing ledgers; up through the wind gap, a cut between two crags where the gusts
    throw you back unless you move between them (ROAD_GUST, a real timing crossing); onto the upper down by the frozen
    tarn (ice-fishing hole) and the frozen fall, behind which lies the Hollow of the Handfast (secret); then west under
    the Handfast Arch to Frostwick's East Gate.  Avalanche fences, trappers' racks, the snowmen (one is a Snorunt), the
    snow-buried signpost in two scripts, Road Stone III-b."""
    W, H = 72, 96
    r = Route(577, W, H, 'snow', base='.', kit='shs')
    m = r.m
    lips = [(74, 1), (50, 2)]
    r.terraces(lips, wobble=2.5, scale=14.0)
    for h in (1, 2): CK.smooth_ht(m, h, 3)
    r.forest_band('E', 9, wobble=4.0); r.forest_band('S', 5, wobble=3.0); r.forest_band('N', 7, wobble=3.0); r.forest_band('W', 4, wobble=2.0)
    # the wind gap: two crags (forest and rock) close the slope above the toll hut to a three-wide cut
    GX, GY0, GY1 = 40, 54, 66
    road = [(31.5, 95), (33, 86), (40, 79), (41, 72), (41, GY1 + 2), (41, GY0 - 2), (36, 46), (26, 41), (14, 38.5), (0, 38.5)]
    r.road(road, w=3.0, c='d', open_=(2, 5))
    r.exit('S', 30, 4); r.exit('W', 37, 4)
    for y in range(GY0, GY1 + 1):
        for x in range(GX - 12, GX + 13):
            if abs(x - (GX + 1)) >= 2 and m.cls[y, x] in '.td': m.cls[y, x] = 'T'
        for x in (GX, GX + 1, GX + 2): m.cls[y, x] = 'd'
    for yl, h in lips:
        xs = [x for x in range(W) if r.road_mask[yl, x]]
        if xs: CK.stair(r, min(xs) + max(0, (len(xs) - 3) // 2), yl, w=3, h=h)
    # the frozen tarn, the frozen fall on its north shore, the Hollow behind; side paths
    m.blob(54, 32, 7.5, 4.2, 'p', seed=7, rough=0.35, only='.tT')
    r.lane([(38, 46), (46, 36), (52, 28)], w=2.0, c='d', open_=(1, 3))
    r.pocket(58, 20, 4, 2.6, gate=None)
    r.lane([(30, 82), (20, 84), (14, 80)], w=2.0, c='d', open_=(1, 3))           # to the bothy
    r.lane([(42, 70), (54, 70), (60, 66)], w=2.0, c='d', open_=(1, 2))           # to the trappers' racks
    for cx, cy_, rx, ry in ((14, 86, 6, 4), (12, 20, 8, 6), (60, 46, 4, 4), (22, 60, 5, 3), (50, 86, 4, 3), (28, 24, 4, 3)):
        r.copse(cx, cy_, rx, ry)
    r.finish_plan(border=0)
    CK.grass_fields(r, [(18, 46, 3.5), (30, 54, 3), (54, 58, 3), (24, 70, 3.5), (50, 80, 3), (14, 28, 3), (40, 28, 3), (34, 88, 2.5)])
    CK.woods(r, CK.SNOWWOOD, scale=10.0)
    m.cls[20:23, 57:59] = '.'
    r.add(sign((34, 90), 'Road sign', "FROSTWICK PASS -- The Hoar Road. v Spinners' Rise - <- Frostwick (East Gate). Two scripts on one post; the Isenmar half is longer."),
          obj('The Handfast Arch', (8, 36), ['THE HANDFAST ARCH: half whale-jaw, half living briar, raised when the border was last agreed.',
              'A brass Meridian sunburst has been bolted across the keystone. The bolts are new and very shiny.']),
          obj('Toll hut ledgers', (36, 76), ['Two ledgers on the empty toll hut\'s counter, one per kingdom. They disagree about everything, including the date.']),
          talk('Bothy keeper', (16, 82), 'NPC 26', ['Bothy keeper: Sit. Drink. It\'s hot and it\'s brown. That\'s all I promise.', {'heal': True}]),
          obj('Ice-fishing hole', (52, 35), ['A round hole cut in the tarn ice, a line still in it. Face the water and use a rod.']),
          obj('Snowmen', (24, 49), ['A row of snowmen built by Frostwick children. One of them is blinking.']),
          talk('Snorunt', (27, 49), 'Followers/SNORUNT', ['(It is pretending very hard to be a snowman.)']),
          obj('Avalanche fence', (56, 62), ['Avalanche fences of split larch. Somebody has painted EAT MORE CHEESE on one in Isenmar.']),
          obj('Snow-buried signpost', (46, 44), ['A signpost buried to its arms in snow. One arm says FROSTWICK. The other says it in runes, and adds "AND NOT ELOWEN".']),
          obj('Road Stone III-b', (30, 92), ['ROAD STONE III-b. THE HOAR ROAD. "Frostwick 1." The \'1\' is in Isenmar runes; the Elowen side says "nearly".']),
          obj('Wind gap', (GX - 1, GY1 + 2), ['THE WIND GAP. The pass funnels the north wind through this cut in gusts. Walk between them, or it walks you back down.']),
          obj('Frozen fall', (58, 18), ['(Behind the frozen fall, a hollow: carvings of a forester and a huscarl, their hands joined, and a bell on a ribbon.)']),
          item((59, 20), 'SOOTHEBELL'), item((8, 56), 'ICEHEAL'), item((62, 48), 'SUPERPOTION'), hidden((47, 28), 'NEVERMELTICE', 'HiddenItem (tarn)'),
          talk('Huscarl', (20, 41), 'NPC 21', ['Huscarl: Elowen side, Isenmar side. The arch doesn\'t care. Nor do I, mostly. Pass.'], d='right'),
          talk('Forester', (44, 73), 'NPC 14', ['Forester: The wind gap above the toll hut. Walk between the gusts or it walks you back down.']),
          {'type': 'event', 'name': 'Wind', 'at': [1, 1], 'fixed': True, 'pages': [{'trigger': 'parallel', 'commands': [
              {'script': 'pfp_metronome(601, 48, 2)'}]}]})
    k = 0
    for y in range(GY0, GY1 + 1):
        for x in (GX, GX + 1, GX + 2):
            r.events.append(gust_event(k, (x, y))); m.taken[y, x] = True; k += 1
    r.seat_events(on='.dtp')
    CK.clear_around(r)
    m.stamp('wb_gate', 7, 33)                                                      # the Handfast Arch, feet on the road's verge
    for n, x, y in (('wb_hut', 32, 72), ('wb_short', 12, 78), ('fw_rack', 58, 66), ('fw_rack', 54, 64), ('fw_sled', 36, 80),
                    ('fw_fall', 56, 14), ('fw_brazier', 20, 80)):
        if m.free(x, y, STAMPS[n]['w'], STAMPS[n]['h'], on='.dt'): m.stamp(n, x, y)
        else: r.near(n, x, y, on='.td', r=7)
    for x in range(50, 64):
        if m.free(x, 60, 1, 1, on='.t'): m.stamp('fw_pal_h', x, 60, mark='B')
    for (x, y) in ((GX - 2, GY0 - 1), (GX + 3, GY0 - 1), (GX - 2, GY1 + 1), (GX + 4, GY1 + 1)):
        r.near('fw_stone', x, y, on='.t', r=1)
    CK.fringe(r, ['pine2', 'kf_tree', 'pf_g_tree2_ice'], 70, seed=1, near_forest=4)
    CK.props(r, ['fw_stone', 'fw_wood', 'fw_log_m', 'fw_drift2'], 24, box=(0, 0, W, H), clump=3, seed=7)
    r.dress(trees=('pine2',), n_trees=0, copses=0, scatter=0)
    r.paint(glint=0.0)
    CK.paint_extras(r)
    CK.snow_ground_var(r, thr=0.45)
    RW.drifts(m, 0.3, seed=577); RW.road_tracks(m, 0.12, seed=577); RW.dress_ice(m, 0.5, seed=577); RW.reed_beds(m, 50, seed=577)
    h = head(577, 'Frostwick Pass', field='SNOWY_MOUNTAIN', bgm='Route 2', weather=['Snow', 20],
             connections=[{'dir': 'S', 'offset': 30, 'to': 566, 'to_offset': 42}, {'dir': 'W', 'offset': 37, 'to': 570, 'to_offset': 23}],
             tone=[-6, -2, 10, 10])
    h['metadata']['BattleBack'] = 'snow'
    r.write(h, '577_frostwick_pass.yaml', '# Frostwick Pass (577). WRITTEN BY layouts/routes_craft.py - edit that script.\n', '/tmp/rt/577.png' if PREV else None)


RW = RE.RW
BUILD[577] = build_577


# ====================================================================================================== 568 The Rehearsal
def frame_pages(k, gfx, cmds, solid=False):
    """event pages that show `gfx` exactly while D8_FRAME == k (RMXP pages only test >=): one page per frame 0-4"""
    pages = []
    for j in range(5):
        pg = {'cond': {'var': ['D8_FRAME', j]}} if j else {}
        if j == k:
            pg.update({'graphic': gfx, 'trigger': 'touch' if not solid else 'action', 'through': not solid, 'commands': list(cmds)})
        else:
            pg.update({'through': True, 'commands': []})
        pages.append(pg)
    return pages


def gust_pages(parity, tile):
    """a frozen salt gust: solid on the frames of the given parity (0: frames 0, 2, 4; 1: frames 1, 3), gone otherwise"""
    pages = []
    for j in range(5):
        pg = {'cond': {'var': ['D8_FRAME', j]}} if j else {}
        if j % 2 == parity:
            pg.update({'graphic': {'tile': tile}, 'trigger': 'action', 'commands': ['Salt spray, frozen in mid-air. It hangs exactly where it hung a moment ago.']})
        else:
            pg.update({'through': True, 'commands': []})
        pages.append(pg)
    return pages


def build_568():
    """The Rehearsal (34x26, BLEED, optional; D8): a stretch of the old salt road off the Frostflat Causeway where five
    seconds of a wagon crash replay forever.  Through the Bleed Veil (N, from 560's spur) the road runs down past the
    wheel-rut where the wagon tips and the four onlookers who watch it every time, through bleached tall grass to the
    drowned pier village (W); east, the salt flat is frozen mid-gust.  One frame per step (D8_FRAME, a step clock): the
    Tauros and the driver come down the road a frame at a time; the gust walls stand on even frames (the salt-flat wall,
    the pier neck) or odd ones (the second wall, the pier end), so the TM and the Bleed Shard need you to step in rhythm.
    Pink crystals of the Bleed grow along the Veil and round the rut."""
    W, H = 34, 26
    r = Route(568, W, H, 'shore', kit={1: 'akc', 'default': 'akc'}, base='.')
    m = r.m
    # ---- the sea: south and the drowned pier village (W), the salt flat's shore (E)
    for x in range(W):
        for y in range(H):
            coast = 21 + 1.5 * (vnoise(x, 0, 5681, 5.0) - 0.5) * 2 - (2 if x > 18 else 0) - (3 if x > 25 else 0)
            if y >= coast: m.cls[y, x] = 'W' if y >= coast + 3 else 'w'
            elif y >= coast - 1.2: m.cls[y, x] = 's'
    for y in range(16, H):                                                       # the pier inlet (W): shallow water round the pilings
        for x in range(0, 9):
            if m.cls[y, x] == '.' and y >= 19 + 1.5 * vnoise(x, y, 5682, 3.0): m.cls[y, x] = 'w'
    # ---- the salt flat (E), frozen mid-gust
    for y in range(2, 16):
        for x in range(18, W):
            if m.cls[y, x] == '.' and x >= 18 + 2 * vnoise(0, y, 5683, 4.0): m.cls[y, x] = 'S'
    # ---- the old salt road from the Veil to the pier, the wheel-rut, the tall grass
    road = [(16, 0), (16, 4), (14.5, 8), (12.5, 11), (10, 15), (7, 18), (5, 20)]
    r.road(road, w=3.0, open_=None, only='.tTS')
    r.lane([(17, 6), (20, 8), (22, 9)], w=2.0, c='d', open_=None, only='.tS')    # onto the salt flat
    r.exit('N', 15, 3)
    for x in range(3, 6):                                                        # the pier: planks over the shallows to the end
        for y in range(20, 26):
            if m.cls[y, x] in 'wWs.': m.cls[y, x] = 'w'; r.deck.append((x, y))
    r.forest_band('N', 2, wobble=1.0); r.forest_band('W', 2, wobble=1.0)
    for y in range(0, 2):                                                        # chalk rock hems the salt flat's north
        for x in range(18, W):
            if m.cls[y, x] in '.S': m.cls[y, x] = 'T'
    r.finish_plan(border=1)
    CK.grass_fields(r, [(8, 13, 3.5), (12, 17, 3.0), (4, 12, 2.5), (14, 13, 2.0)])
    # ---- events
    gtile = STAMPS['bl_gust0']['layers'][2][0][0]
    pass_ = ['You pass through the moment, and it shivers.']
    ev = [{'type': 'warp', 'name': 'Bleed Veil', 'at': [16, 0], 'link': 'R5_REHEARSAL', 'arrive': [16, 1, 'down'], 'se': 'Door exit', 'fixed': True},
          {'type': 'event', 'name': 'Frame clock', 'at': [0, 0], 'fixed': True, 'pages': [
              {'trigger': 'parallel', 'commands': [
                  {'script': 'pfp_step_hook(568, :rehearsal) { pfp_step_clock(536, 5); $game_map.need_refresh = true }'}, {'wait': 120}]}]},
          obj('Wheel-rut', (12, 12), ['An old wheel-rut, worn deep, where the road bends. The frost in it is broken fresh, every five seconds.']),
          sign((19, 4), 'Veil sign', 'THE OLD SALT ROAD. (Somebody has chalked under it: "it does it again".)'),
          obj('Drowned pier', (6, 19), ['The pier of a village the sea took back. Pilings in a row, houses to the sills in water. The planks still hold.']),
          obj('The tipped wagon', (11, 9), ['The wagon on its side, wheel still turning. Spilled salt sacks. It is always just now.'])]
    T, D = 'Followers/TAUROS', 'NPC 11'
    for k, (tx, ty) in enumerate(((16, 2), (16, 4), (15, 6), (14, 8), (13, 10))):            # the bolting Tauros, frame by frame
        ev.append({'type': 'event', 'name': 'Tauros f%d' % k, 'at': [tx, ty], 'fixed': True,
                   'pages': frame_pages(k, {'sprite': T, 'dir': 'down'}, pass_)})
    for k, (tx, ty) in enumerate(((17, 1), (17, 3), (16, 5), (15, 7), (14, 9))):             # the driver hauling on the reins
        ev.append({'type': 'event', 'name': 'Driver f%d' % k, 'at': [tx, ty], 'fixed': True,
                   'pages': frame_pages(k, {'sprite': D, 'dir': 'down'}, pass_)})
    ev.append({'type': 'event', 'name': 'The girl in the road (replay)', 'at': [12, 13], 'fixed': True, 'pages': [
        {'graphic': {'sprite': 'NPC 07', 'dir': 'up'}, 'through': True, 'trigger': 'touch', 'commands': pass_},
        {'cond': {'var': ['D8_FRAME', 3]}, 'graphic': {'sprite': 'NPC 07', 'dir': 'right'}, 'through': True, 'trigger': 'touch', 'commands': pass_}]})
    words = [('left', 'centre', 'right'), ('first', 'second', 'third'), ('pink', 'grey', 'white'), ('soon', 'now', 'again')]
    for i, (x, y) in enumerate(((8, 7), (9, 8), (7, 9), (9, 10))):                         # the onlookers: one word different each visit
        opts = ', '.join('"Onlooker: It tips at the %s wheel. It always tips at the %s wheel."' % (w, w) if i == 0 else
                         '"Onlooker: Step %s, step %s. That is how you cross the white."' % (w, w) if i == 1 else
                         '"Onlooker: The horse is %s this time. It was %s last time. It is always %s."' % (w, w, w) if i == 2 else
                         '"Onlooker: It will end %s. It never ends %s."' % (w, w) for w in words[i])
        ev.append({'type': 'event', 'name': 'Onlooker %d' % (i + 1), 'at': [x, y], 'fixed': True, 'pages': [
            {'graphic': {'sprite': ['NPC 02', 'NPC 13', 'NPC 24', 'NPC 09'][i], 'dir': 'right'}, 'trigger': 'action',
             'commands': [{'script': 'pbMessage(_INTL([%s].sample))' % opts}]}]})
    # the gust walls: across the salt flat (x 23 even, x 26 odd) and across the pier (row 22 even, row 24 odd)
    walls = [(23, y, 0) for y in range(2, 16)] + [(26, y, 1) for y in range(2, 16)] + [(x, 22, 0) for x in (3, 4, 5)] + [(x, 24, 1) for x in (3, 4, 5)]
    for i, (x, y, par) in enumerate(walls):
        if m.cls[y, x] in 'Sdw.s':
            ev.append({'type': 'event', 'name': 'Frozen gust %d' % (i + 1), 'at': [x, y], 'fixed': True, 'pages': gust_pages(par, gtile)})
    ev += [item((31, 9), 'TM10'), item((4, 25), 'BLEEDSHARD') if False else
           obj('Bleed Shard', (4, 25), ['A shard of something like glass, pink at the edges, humming one note.',
                                         {'if': '!pfm?(:bleed_shard_3)', 'then': [{'script': 'pfm_set(:bleed_shard_3)'}, '(Bleed Shard #3. You pocket it. It keeps humming.)'],
                                          'else': ['Only the hum is left.']}]),
           hidden((29, 4), 'STARDUST', 'HiddenItem (salt flat)')]
    for e in ev: e.setdefault('fixed', True)
    r.add(*ev)
    r.seat_events(on='.dtgS')
    # ---- props: the drowned village, the Bleed's pink crystals, salt and frost
    for nm, x, y in (('sh_small', 0, 13), ('gl_cot', 8, 18) if False else ('nr_ruin', 8, 21), ('hb_boat3', 0, 22), ('hb_posts3', 7, 23), ('hb_posts2', 1, 24)):
        if nm.startswith('hb_'): continue
        r.near(nm, x, y, on='.tsw', r=2)
    m.stamp('pf_wagon', 9, 10) if m.free(9, 10, 3, 2, on='.dtg') else r.near('pf_wagon', 9, 10, on='.dtg', r=2)
    for nm, x, y in (('cr_pink_t', 13, 2), ('cr_pink_c', 19, 3), ('cr_purple_e', 12, 3), ('cr_pink_e', 18, 1), ('cr_teal_c', 10, 12),
                     ('cr_pink_c', 15, 13), ('cr_purple_c', 7, 15), ('cr_clear_t', 21, 12), ('cr_pink_t', 30, 13), ('cr_teal_e', 32, 4),
                     ('cr_pink_c', 28, 7), ('cr_clear_c', 20, 6), ('cr_purple_t', 2, 9), ('cr_pink_c', 4, 6)):
        r.near(nm, x, y, on='.tgS', r=2)
    for (x0, y0, w, h, k) in ((20, 4, 2, 3, 'brx'), (20, 9, 2, 2, 'brp'), (20, 12, 2, 2, 'brx'), (24, 3, 2, 2, 'brp'), (24, 7, 2, 3, 'brx'),
                              (24, 12, 2, 2, 'brx'), (28, 3, 3, 2, 'brx'), (28, 11, 2, 3, 'brp'), (31, 6, 2, 2, 'brx'), (29, 14, 3, 1, 'brx')):
        if (m.cls[y0:y0 + h, x0:x0 + w] == 'S').all() and not m.taken[y0:y0 + h, x0:x0 + w].any():
            for yy in range(y0, y0 + h):
                for xx in range(x0, x0 + w):
                    v = ('n' if yy == y0 else 's' if yy == y0 + h - 1 else '') + ('w' if xx == x0 else 'e' if xx == x0 + w - 1 else '')
                    m.tile(K.P1('%s_%s' % (k, v or 'c')), xx, yy, 1); m.cls[yy, xx] = 'B'; m.under[yy, xx] = 'S'
    CK.props(r, ['hb_salt0', 'hb_salt1', 'hb_salt2'], 5, box=(18, 2, 33, 16), on='S', clump=1, seed=5)
    CK.props(r, ['nt_rocks_s0', 'ck_pebbles', 'nt_stump', 'nt_log'], 6, box=(0, 0, 18, 20), clump=1, seed=6)
    CK.woods(r, [{'purp': 3, 'pinepurp': 2}, {'dead': 2, 'purp': 2}], scale=8.0) if False else None
    CK.fringe(r, ['nt_deadtree', 'nt_birch_v', 'nt_dpine_sh', 'nt_tree_purp', 'nt_pine_purp'], 60, seed=1, near_forest=6)
    CK.undergrowth(r, 140, kinds=('nt_reed0', 'nt_reed1', 'nt_fern1', 'nt_bush1', 'nt_shrub1'), seed=3)
    for i, (cx, cy, rx, ry) in enumerate(((5, 8, 3, 2), (14, 16, 3, 2), (2, 15, 2, 2), (11, 5, 2, 1.5))):      # bleached sea-pinks
        CK.meadow(r, cx, cy, rx, ry, tiles=[K.DECOR_SH['flowers'][k] for k in (8, 9, 10)], p=0.6, seed=i)
    r.dress(trees=('nt_deadtree',), n_trees=0, copses=0, scatter=0)
    r.paint(glint=0.25)
    CK.paint_extras(r)
    CK.crust_ground(r, [(x, y) for y, x in np.argwhere((m.cls == 'S') | ((m.cls == 'B') & (m.under == 'S')))])
    CK.boardwalks(r, r.deck)
    rng = random.Random(568)
    for y in range(1, 4):                                                        # the Veil's shimmer across the road
        for x in range(13, 20):
            if m.L[2, y, x] == 0 and not m.taken[y, x] and m.cls[y, x] != 'B': m.L[2, y, x] = K.P1('bl_veil%d' % ((x + y) % 2))
    for y, x in np.argwhere(m.cls == 'S'):                                       # salt spray frozen all over the flat
        if m.L[2, y, x] == 0 and rng.random() < 0.34: m.L[2, y, x] = K.P1('bl_gust%d' % rng.randrange(3))
    for y, x in np.argwhere(np.isin(m.cls, ['.', 'g'])):                         # the Bleed's shimmer drifts over the road's edges
        if m.L[2, y, x] == 0 and vnoise(x, y, 5684, 3.0) > 0.72: m.L[2, y, x] = K.P1('bl_veil%d' % ((x * 3 + y) % 2))
    for nm, x, y in (('hb_posts3', 6, 23), ('hb_posts2', 1, 21), ('hb_post1', 7, 20), ('hb_boat3', 0, 24)):
        L = np.array(STAMPS[nm]['layers'])
        for j in range(L.shape[1]):
            for i in range(L.shape[2]):
                t = int(L[:, j, i].max())
                if t and m.inb(x + i, y + j) and m.cls[y + j, x + i] in 'wW' and m.L[2, y + j, x + i] == 0 and (x + i, y + j) not in r.deck:
                    m.L[2, y + j, x + i] = t
    CK.scatter_quiet(r, 24)
    h = head(568, 'The Rehearsal', field='BLEED', bgm='Radio - Lullaby', biome='bleed', parent=560,
             tone=[-10, -22, 20, 60], fog={'name': 'prismfall_seamist', 'opacity': 50, 'blend': 0, 'zoom': 100, 'sx': 1, 'sy': 0})
    h['metadata']['MapPosition'] = [0, 4, 15]
    h['gates'] = [{'name': 'Salt-flat gust walls (frame 0)', 'from': [[16, 1]], 'sealed': [[31, 9]]}]
    r.write(h, '568_the_rehearsal.yaml', '# The Rehearsal (568, :BLEED). WRITTEN BY layouts/routes_craft.py (map builder 10) - edit that script.\n',
            '/tmp/craft/568.png' if PREV else None)


BUILD[568] = build_568
