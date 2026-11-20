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
    CK.clear_around(r)
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
          once('The Saltings', (33, 99), ['(Salt pans to the horizon, white stacks, the smoke of the boiling-house, and a chalk cliff behind with a mine mouth in it.)',
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
          once("The Dyers' Ford", (39, cy[39] + 7), ['(Below three vat-sheds, the River Selvedge runs in three bands: madder red, woad blue, weld yellow. Cloth dries on lines across the road.)',
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
    r.forest_band('N', 4, wobble=2.0); r.forest_band('S', 3, wobble=1.5); r.forest_band('E', 2, wobble=1.0)
    for cx, cy_, rx, ry in ((118, 12, 10, 7), (100, 46, 6, 3), (6, 40, 5, 5), (36, 6, 8, 3), (124, 46, 5, 4), (100, 14, 4, 3),
                            (14, 8, 5, 4), (50, 46, 4, 2.5), (82, 44, 3, 2), (110, 22, 3, 3), (30, 46, 3, 2)):
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
          obj('Bamboo stand', (112, 18), ['A bamboo stand, planted by a Thistledown who wanted "something foreign". The Pancham agree.']),
          talk('Pancham', (108, 20), 'Followers/PANCHAM', ['(It glares at you over a bamboo shoot. Respect.)'], move='random'),
          obj('Road Stone II-b', (122, 29), ["ROAD STONE II-b. THE WEAVERS' ROAD. \"Briarwick 1.\" The '1' has been scratched to a '2' and back again."]),
          obj('Gateposts', (64, y1 - 2), ['Two stone gateposts with the Thistledown thistle carved on them. No gate. Gates are for people who expect visitors.']),
          obj('The Ha-ha', (82, 2), ['(The sunken wall\'s ditch runs round the back of the hill to an overgrown garden. A cellar door, barred from inside. Something is digging behind it.)']),
          talk('Greavard', (80, 4), 'Followers/GREAVARD', ['(It is digging very seriously. It does not want to be interrupted. It wags anyway.)'], move='random'),
          hidden((84, 3), 'RAREBONE', 'HiddenItem (the Ha-ha)'),
          obj('Topiary', (58, 14), ['A topiary garden gone wild. One bush was a Ponyta once. Now it is a Ponyta that has seen things.']),
          {'type': 'berry', 'at': [30, 34], 'berry': 'CHERIBERRY'}, item((126, 20), 'SUPERPOTION'), item((4, 34), 'POKEBALL'), item((70, 52), 'GREATBALL'))
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
