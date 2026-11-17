#!/usr/bin/env python3
"""The Rimewood borderland stretch (Borderland A, WORLD.md 10; maps.json 560-576), on PF Rejuv tileset 52 "PF Rejuv
Snow" (Kristiline Town (Frozen) snow, ice and A-frame longhouses; Reborn Route 4 pines; snowified Sheridan cliffs,
forest and Prismfall's giant trees, rcustom.SNOW).  MAPGEN 2h.

Chain (each link is an edge connection; spans match maps.json):
  140 Saltmere --W(32)/E(12)--> 560 Route 5 --W(10)/E(18)--> 570 Frostwick --N(20)/S(22)--> 562 The Rimewood
  --N(12)/S(10)--> 561 Route 6 --N(12)/S(22)--> 160 Ebbmouth;   562 (47,24) <-RIME_GLADE-> 563 (0,15)
Interiors 571-576 are Sheridan timber rooms (interiorkit, tileset 34).
Run: python3 -I layouts/rimewood.py && python3 -I build.py 560 561 562 563 570 571 572 573 574 575 576"""
import os, sys, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, yaml
import rkit as K
from rkit import C, STAMPS
from terrain import vnoise
HERE = K.HERE
ICE = C('kf', 2476)                                  # walkable ice, terrain tag 12 (slides)
CAVE = [[624, 625, 626], [632, 633, 634], [640, 641, 642]]


def snowmap(W, H, mid, kit='shs', sea=False):
    m = K.RMap(W, H, 52, mid, water='Still water snow', kit=kit, grass=K.SNOW_GROUND, decor=K.DECOR_SNOW)
    m.tall = K.SNOW_TALL
    m.grass2 = [[K.SN('grass_sh', 647), K.SN('grass_sh', 646)], [K.SN('grass_sh', 655), K.SN('grass_sh', 654)]]
    m.lattice = K.RMap.TREES_SNOW
    m.auto = {'d': ('KristilineDirt', 'rejuvenation'), 'w': ('Still water snow', 'reborn'),
              'o': ('KristilineWatersFrozen', 'rejuvenation'), 'S': ('Sand shore(Terajuma)', 'rejuvenation'),
              'W': ('Sea deep', 'rejuvenation')}
    if sea: m.auto['w'] = ('Sea deep', 'rejuvenation'); m.auto.pop('W')
    m.JOIN = dict(K.RMap.JOIN, o='o', S='S'); m.AUTO_Z = dict(K.RMap.AUTO_Z, o=0, S=1)
    return m


def ice_over(m, cls='w', edge=True):
    """walkable ice over the interior of a water body; the rim stays open water (fishing holes, the ice edge)"""
    for y in range(m.H):
        for x in range(m.W):
            if m.cls[y, x] != cls: continue
            nb = [(x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)]
            if not edge or all(not m.inb(a, b) or m.cls[b, a] == cls for a, b in nb):
                m.L[1, y, x] = ICE


def cave_mouth(m, x, y):
    """3x3 snowy rock arch whose dark opening's bottom cell is (x, y); drawn over a cliff face (layer 3)"""
    for dy in range(3):
        for dx in range(3):
            m.L[2, y - 2 + dy, x - 1 + dx] = K.SN('cave_sh', CAVE[dy][dx])


def trainer(at, cls, name, intro, after, d='down', sight=4, sprite=None, double=False):
    e = {'type': 'trainer', 'at': list(at), 'sight': sight, 'dir': d, 'sprite': sprite or 'trainer_' + cls,
         'trainer': [cls, name], 'intro': intro, 'after': after}
    if double: e['rules'] = ['setBattleRule("double")']
    return e


def npc(at, name, sprite, lines, d='down', move='fixed', again=None):
    pages = [{'graphic': {'sprite': sprite, 'dir': d}, 'trigger': 'action', 'move': move, 'commands': list(lines)}]
    if again:
        pages[0]['commands'] = pages[0]['commands'] + [{'selfswitch': ['A', True]}]
        pages.append({'cond': {'self': 'A'}, 'graphic': {'sprite': sprite, 'dir': d}, 'trigger': 'action', 'move': move, 'commands': list(again)})
    return {'type': 'event', 'name': name, 'at': list(at), 'pages': pages}


def sign(at, name, text): return {'type': 'sign', 'name': name, 'at': list(at), 'text': text, 'post': False}


def item(at, it, hidden=False): return {'type': 'item', 'at': list(at), 'item': it, **({'hidden': True} if hidden else {})}


def flat(m, x, y):
    """no height change in the 3x3 around (x, y) and no higher ground in the 4 rows above (cliff faces hang there)"""
    h = m.ht[y, x]
    for dy in range(-4, 2):
        for dx in (-1, 0, 1):
            X, Y = x + dx, y + dy
            if not m.inb(X, Y): continue
            if (dy >= -1 and m.ht[Y, X] != h) or (dy < -1 and dx == 0 and m.ht[Y, X] > h): return False
    return True


def seat(m, events, on='.dt'):
    """move every event onto the nearest free walkable cell (off cliffs) and reserve it"""
    out = []
    for e in events:
        x, y = e['at']
        if not (m.inb(x, y) and m.cls[y, x] in on and not m.taken[y, x] and not m.overm[y, x] and flat(m, x, y)):
            best = None
            for r in range(1, 10):
                for yy in range(y - r, y + r + 1):
                    for xx in range(x - r, x + r + 1):
                        if m.inb(xx, yy) and m.cls[yy, xx] in on and not m.taken[yy, xx] and not m.overm[yy, xx] and flat(m, xx, yy):
                            d = abs(xx - x) + abs(yy - y)
                            if best is None or d < best[0]: best = (d, xx, yy)
                if best: break
            if best is None: raise SystemExit('seat: no place for %s near %d,%d' % (e.get('name', e['type']), x, y))
            x, y = best[1], best[2]
        e['at'] = [x, y]; m.taken[y, x] = True; out.append(e)
    return out


def signboard(m, e):
    x, y = e['at']; m.tile(4847, x, y, 1)


def head(mid, name, **kw):
    h = {'id': mid, 'name': name, 'parent': 0, 'rubric': True, 'yards_ok': True}
    h.update(kw); return h


# =================================================================================================== 560 Route 5
def route5(prev=None):
    W, H = 64, 30
    m = snowmap(W, H, 560)
    # north: the sea dyke under reed beds (a snowy bank, h=1) with frozen lagoon behind; south: the brine lagoon, iced
    for x in range(W):
        top = 3 + int(round(1.2 * math.sin(x / 7.0) + vnoise(x, 0, 2, 5.0)))
        bot = 26 - int(round(1.0 * math.sin(x / 9.0 + 2) + 1.2 * vnoise(x, 0, 3, 6.0)))
        for y in range(H):
            if y <= top: m.ht[y, x] = 1
            if y <= top - 2: m.cls[y, x] = 'o'
            if y >= bot: m.cls[y, x] = 'o' if y >= bot + 1 else 'w'
    m.lane([(-1, 13), (10, 13), (20, 12.5), (28, 13.5), (40, 13), (52, 12.5), (64, 13)], 'd', 3.2, seed=11, only='.', wobble=0.5)
    m.rect(0, 12, 2, 3, 'd'); m.rect(W - 2, 12, 2, 3, 'd')          # the edge rows line up with 570 / 140
    m.street([(30, 14), (30, 27)], 2, 'd', only='.ow')               # spur S to the old salt road (the Rehearsal, 568)
    m.rect(29, 27, 4, 3, 'd')
    # east half: salt pans and salt crust; west half: frost pans (ice) and frosted grass
    for cx, cy, rx, ry in ((40, 6, 3.5, 1.6), (47, 7, 2.6, 1.4), (55, 5, 3.0, 1.3), (44, 20, 3.0, 1.5), (58, 19, 2.6, 1.6), (52, 23, 2.2, 1.0)):
        m.blob(cx, cy, rx, ry, 't', seed=cx, only='.', rough=0.6)
    for cx, cy, rx, ry in ((7, 6, 3.0, 1.4), (16, 6, 2.0, 1.0), (22, 19, 2.0, 1.2)):
        m.blob(cx, cy, rx, ry, 'w', seed=cx + 50, only='.', rough=0.4)
    m.blob(13, 19.5, 5.5, 2.2, 'i', seed=21, only='.t', rough=0.5)      # the first slide tiles (teaches sliding)
    lagoon(m, 0.5)
    for (x0, y0, w, h) in ((42, 4, 10, 5), (48, 20, 10, 5), (10, 4, 8, 6), (6, 22, 10, 4)):
        m.rect(x0, y0, w, h, 't', only='.')
    E = []
    stones = [(30, 10), (36, 10)]                                     # the Border Stones flank the road
    for x, y in stones: m.stamp('ak_rock2', x - 1, y - 2)
    E.append(sign((33, 11), 'Border Stones', "Two old stones. One bears Elowen's briar crown, the other Isenmar's whale and axe.\n"
                  "A brass Meridian sunburst has been bolted across both of them. The bolts are new."))
    E.append(sign((60, 11), 'Route sign', "ROUTE 5 - THE FROSTFLAT CAUSEWAY\nW: Frostwick   E: Saltmere"))
    E.append(sign((31, 26), 'Old salt road', "The old salt road dips toward a drowned pier village. Something replays there, over and over.\n"
                  "[The Rehearsal, map 568: not built yet]"))
    E += [npc((31, 9), 'Royal forester', 'NPC 14', ["Past the stones the trees wear coats. Ice ones. You'll see.",
                                                     "Elowen ends here, officially. Unofficially it ends wherever the honey runs out."],
              again=["Mind the frost-pans west of here. They're slick as a courtier."]),
          npc((22, 15), 'Fur-trader', 'NPC 22', ["My Spheal pulls the sled. Lovely creature. Round.",
                                                  "...The problem is the sled is on a SLOPE, and Spheal is ALSO round.",
                                                  "If you see a sled rolling toward Saltmere with a Spheal on it, wave. It likes that."],
              again=["Still no sled. Still no Spheal. Still a lovely day."]),
          npc((20, 7), 'Meridian surveyor', 'NPC 16', ["*tink* *tink* Survey peg. Lattice line. Don't touch.",
                                                       "Who authorised it? The Meridian. Who authorised the Meridian? ...Move along, please."],
              d='left')]
    E += [trainer((50, 8), 'PICNICKER', 'Sela', "Salt-flat picnic! Bring your own shade!", "Isenmar's colder than I thought.", 'down'),
          trainer((40, 17), 'HIKER', 'Torvald', "Thirty years I've carted salt down this road! Show me something new!",
                  "Salt in my boots, frost in my beard. Good trade.", 'up'),
          trainer((14, 17), 'LASS', 'Tilde', "Did you slide here too? Everyone slides here.", "My Swinub slid farther than me.", 'right'),
          trainer((20, 10), 'SAILOR', 'Haakon', "Sealer out of Ebbmouth! The sea's too thick to row, so I walk!",
                  "Ice'll break by summer. Probably.", 'down'),
          trainer((26, 22), 'BIRDKEEPER', 'Ailsa', "The gulls change colour past the stones. Watch!",
                  "Frostwick's gulls wear little ice hats. Not really.", 'up'),
          item((62, 4), 'SUPERPOTION'), item((5, 7), 'ICEHEAL'), item((56, 27), 'SOFTSAND', True)]
    # overturned salt wagon (HEALPOWDER inside), survey pegs, salt cedars, fence posts along the causeway
    m.near('sh_crates', 44, 20, on='.tS', r=3); m.near('pf_barricade', 46, 21, on='.tS', r=3)
    E.append(item((45, 22), 'HEALPOWDER'))
    pegs = [(20, 6), (22, 7), (24, 8), (26, 9), (18, 5), (28, 10)]
    E = seat(m, E, on='.dtSi')
    for x, y in pegs:
        if m.free(x, y, 1, 1, on='.t'): m.tile(4847, x, y, 1)
    for cx, cy in ((38, 18), (41, 21), (36, 22), (54, 16), (57, 8), (60, 21)):
        m.trees(cx, cy, 1, ['pine2', 'tr_teal'], r=2, on='.tS', seed=cx)
    for cx, cy in ((4, 9), (12, 10), (2, 18), (24, 4), (18, 23), (8, 24), (34, 6), (46, 4), (60, 7), (36, 20), (48, 17),
                   (62, 22), (1, 24), (28, 20), (54, 24)):
        m.trees(cx, cy, 2, ['pine2', 'kf_tree', 'pine2'], r=3, on='.tS', seed=cx)
    for cx, cy in ((10, 9), (26, 17), (44, 9), (56, 17), (16, 16), (50, 10)):     # salt cedars and frosted pines along the road
        m.trees(cx, cy, 1, ['pine2', 'kf_tree', 'tr_teal'], r=2, on='.tS', seed=cx * 5)
    for e in E:
        if e['type'] == 'sign' and e['name'] != 'Border Stones': signboard(m, e)
    m.events = E
    m.greenfill(3, on='.')
    m.paint(); ice(m); m.scatter(15, seed=5)
    if prev: m.preview(prev, 0.5)
    m.write(560, head(560, 'Route 5', biome='route', display_name='Route 5 - Frostflat Causeway', bgm='Route 2',
                      metadata={'Outdoor': True, 'ShowArea': True, 'MapPosition': [0, 7, 22], 'BattleBack': 'snow', 'Weather': ['Snow', 10]},
                      tone=[-6, -2, 10, 10],
                      connections=[{'dir': 'E', 'offset': 12, 'to': 140, 'to_offset': 32}, {'dir': 'W', 'offset': 10, 'to': 570, 'to_offset': 18}],
                      _file='560_route5.yaml'), '# Route 5 (560). WRITTEN BY layouts/rimewood.py - edit that script.\n')
    return m


def ice(m):
    """class i / I: walkable ice ground (slides); class w interiors iced over"""
    for y, x in np.argwhere(np.isin(m.cls, ['i', 'I'])):
        m.L[0, y, x] = ICE
    ice_over(m, 'w')


# =================================================================================================== 570 Frostwick
def frostwick(prev=None):
    W, H = 60, 48
    m = snowmap(W, H, 570)
    BX = 30                                                          # the frozen Hoar Brook, x 30-33
    for y in range(H):
        bx = BX + int(round(1.0 * math.sin(y / 6.0)))
        for x in range(bx, bx + 4): m.cls[y, x] = 'w'
    for y in range(40, H):                                           # the salt lagoon to the south, frozen
        for x in range(W):
            if y >= 41 + 2 * vnoise(x, 0, 4, 6.0): m.cls[y, x] = 'o'
    lagoon(m, 0.55)
    # north-west terrace (h=1): the treehouse quarter in the ice-glazed giants
    for y in range(H):
        for x in range(W):
            if x < 18 and y <= 14: m.ht[y, x] = 1
    for y in range(H):                                               # rimewood edge: N and W, ragged
        for x in range(W):
            if m.cls[y, x] != '.': continue
            edge = min(y + 2 * vnoise(x, 0, 5, 4.0), x + 2 * vnoise(0, y, 6, 4.0))
            if edge < 3.5 or (x > 54 and y < 14) or (y < 4 and 36 < x < 59): m.cls[y, x] = 'T'
    # streets: the east road from the gate, the square, the north path into the Rimewood
    m.rect(36, 20, 24, 3, 'd')                                        # east road (rows 20-22) from the gate
    m.rect(20, 18, 18, 9, 'd', only='.T')                             # the square, astride the brook
    m.rect(26, 0, 3, 19, 'd', only='.T')                              # north path (x 26-28) to the Rimewood
    m.rect(8, 26, 14, 3, 'd'); m.rect(8, 18, 3, 11, 'd')             # west lane and the stair to the terrace
    m.rect(36, 30, 3, 10, 'd'); m.rect(36, 37, 16, 3, 'd')            # south lane to the pens and the jetty
    m.stairs(8, 14, w=3, kit_rows=4)
    for y in range(H):                                               # brook under the roads: a plank bridge (rows 20-22, 37-39)
        pass
    # buildings
    E = []
    d = {}
    d['pc'] = m.front('kf_aframe2', 13, 25, 'FW_PC', 'Poke Center door')
    d['exch'] = m.front('kf_aframe', 44, 19, 'FW_EXCH', 'Exchange door')
    d['inn'] = m.front('kf_aframe2', 22, 17, 'FW_INN', 'Two Hearths door')
    d['border'] = m.front('kf_flat', 52, 19, 'FW_BORDER', 'Border House door')
    d['smoke'] = m.front('kf_flat', 44, 29, 'FW_SMOKE', "Smokehouse door")
    d['loft'] = m.front('pf_g_tree6_ice', 12, 12, 'FW_LOFT', 'Loft door')
    for nm, x, y in (('pf_g_tree4_ice', 1, 3), ('pf_g_tree4p_ice', 18, 1), ('pf_g_tree2_ice', 6, 30), ('pf_g_tree4p_ice', 40, 3),
                     ('pf_g_tree2_ice', 50, 6), ('kf_flat', 13, 34), ('kf_aframe', 46, 9)):
        if m.free(x, y, STAMPS[nm]['w'], STAMPS[nm]['h'], on='.dT'): m.stamp(nm, x, y)
        else: print('  (frostwick: no room for %s at %d,%d)' % (nm, x, y))
    for k, (dx, dy) in d.items():
        for yy in (dy + 1, dy + 2):
            if m.inb(dx, yy) and m.cls[yy, dx] in '.tT' and m.ht[yy, dx] == m.ht[dy, dx]: m.cls[yy, dx] = 'd'
    m.stamp('sh_gate', 56, 18)                                        # the east gate: whale-rib arch wrapped in briar
    for y in range(8, 40):                                            # palisade along the east edge, gate open at rows 20-22
        if not (19 <= y <= 23) and m.cls[y, 58] in '.T': m.fence(58, 58, y)
    E += [sign((28, 25), 'Hearth Stone', "THE HEARTH STONE\nCarved twice: once in Elowen's knotwork, once in Isenmar's runes.\n"
                                         "Both say the same thing. \"Here, no one is a foreigner by the fire.\""),
          sign((40, 23), 'Town sign', "FROSTWICK\nWhere the Rimewood meets the salt."),
          sign((12, 30), 'PC sign', "POKEMON CENTER"), sign((43, 24), 'Exchange sign', "THE EXCHANGE\nHoney for furs. Silk for oil. Coin if you must."),
          npc((21, 23), 'Brannagh', 'NPC 25', ["Brannagh, Elowen side of the Two Hearths. Applewood fire, honey cakes, no shouting.",
                                               "Halvard's lot burn whale oil on the other hearth. Smells like a shipwreck. We get on fine."],
              again=["Find me an applewood log in the Rimewood and I'll show that whale-oil man what a fire is."]),
          npc((27, 23), 'Halvard', 'NPC 28', ["Halvard. Sealer. Isenmar side of the Two Hearths.",
                                              "Brannagh's applewood smells like a pudding. A man can't think by a pudding."],
              again=["Ask her about the log. Go on. I want to watch her face."]),
          npc((40, 33), 'Girl in ogre mask', 'NPC 07', ["We're playing Kingdoms! I'm Elowen! RAAAH! Briar curse!"], move='random'),
          npc((41, 34), 'Boy in whale mask', 'NPC 03', ["I'm Isenmar! Whale curse! ...There's no whale curse. I'm making it up."], move='random'),
          npc((57, 23), 'Huscarl', 'NPC 11', ["Gate's open. Wipe your boots. Declare any honey."], d='left'),
          npc((57, 17), 'Forester', 'NPC 14', ["Elowen's watch. Isenmar's watch. Same gate, same cold. We split the shifts."], d='left'),
          npc((32, 14), 'Ice-fisher', 'trainer_FISHERMAN', ["See the dark holes along the brook? Fish come up to breathe.",
                                                             "Face the open water and use a rod. Even an Old Rod works here."], d='down'),
          npc((48, 38), 'Swinub herder', 'NPC 17', ["The sled-pens. Swinub now, Mamoswine by spring if they eat their greens.",
                                                     "They don't eat greens. They eat everything else."]),
          item((40, 41), 'SNOWBALL', True)]
    E = seat(m, E, on='.d')
    for e in E:
        if e['type'] == 'sign' and e['name'] != 'Hearth Stone': signboard(m, e)
        if e.get('name') == 'Hearth Stone': m.tile(10371, e['at'][0], e['at'][1], 1)
    # market stalls, pens, lamps, yard trees
    for nm, x, y in (('pf_p_awning', 14, 29), ('sh_crates', 15, 30), ('sh_crates', 19, 29), ('pf_p_laundry', 3, 26),
                     ('pf_lantern', 36, 24), ('pf_lantern', 22, 27), ('pf_lantern', 11, 23), ('pf_lantern', 50, 23)):
        m.near(nm, x, y, on='.', r=3)
    m.fence(40, 50, 35, gaps=((44, 45),)); m.fence(40, 50, 41)
    for cx, cy, n in ((4, 22, 2), (18, 37, 2), (26, 32, 2), (52, 30, 2), (55, 34, 1), (46, 14, 2), (36, 10, 2), (5, 40, 2), (24, 40, 1)):
        m.trees(cx, cy, n, ['pine2', 'kf_tree', 'pine2'], r=3, on='.', seed=cx * 7 + cy)
    m.greenfill(3)
    m.events = [e for e in m.events if e['type'] == 'door'] + E
    m.paint()
    bridges(m, ((20, 22), (37, 39)))

    ice(m)
    rime_silk(m, ((4, 4), (8, 6), (14, 3), (20, 8), (36, 6), (44, 4), (52, 9), (6, 18)))
    m.scatter(8, seed=8)
    if prev: m.preview(prev, 0.5)
    m.write(570, head(570, 'Frostwick', biome='village', bgm='Lerucean Town',
                      metadata={'Outdoor': True, 'ShowArea': True, 'MapPosition': [0, 7, 21], 'BattleBack': 'snow', 'Weather': ['Snow', 20]},
                      tone=[-8, -4, 12, 12], fog={'name': 'prismfall_seamist', 'opacity': 30, 'blend': 0, 'zoom': 100, 'sx': 1, 'sy': 0},
                      connections=[{'dir': 'N', 'offset': 20, 'to': 562, 'to_offset': 22}, {'dir': 'E', 'offset': 18, 'to': 560, 'to_offset': 10}],
                      _file='570_frostwick.yaml'), '# Frostwick (570). WRITTEN BY layouts/rimewood.py - edit that script.\n')
    print('frostwick doors', d)
    return m


def bridges(m, rows):
    """plank bridges where a road crosses the brook: Sheridan deck planks (layer 2) over the water"""
    T, B = C('sh', 489), C('sh', 505)
    for y0, y1 in rows:
        for y in range(y0, y1 + 1):
            for x in range(m.W):
                if m.cls[y, x] == 'w':
                    m.L[1, y, x] = T if y == y0 else B if y == y1 else C('sh', 497)


def lagoon(m, thr=0.55, seed=12):
    """Kristiline's frozen sea: walkable ice (class I, terrain tag 12) with dark open-water holes (class o, the
    KristilineWatersFrozen autotile, whose rims carry the ice texture).  Call before paint; ice() lays the ice."""
    for y, x in np.argwhere(m.cls == 'o'):
        if vnoise(x, y, seed, 3.5) < thr: m.cls[y, x] = 'I'


def floes(m, cls, thr):
    for y, x in np.argwhere(m.cls == cls):
        if vnoise(x, y, 7, 3.0) > thr and m.L[1, y, x] == 0 and m.L[2, y, x] == 0: m.L[1, y, x] = ICE


def rime_silk(m, spots):
    """frozen silk curtains hanging from the giants' branches (layer 3 strands, icy white)"""
    for x, y in spots:
        if m.inb(x, y) and m.inb(x, y + 1) and m.L[2, y, x] == 0:
            st = STAMPS['pf_p_strand_w']['layers']
            for dy in range(2):
                t = st[1][dy][0] or st[2][dy][0]
                if t and m.L[2, y + dy, x] == 0: m.L[2, y + dy, x] = t


# =================================================================================================== 562 The Rimewood
def rimewood(prev=None):
    W, H = 48, 56
    m = snowmap(W, H, 562)
    # the path climbs N from Frostwick (S edge x 26-28) to the Isenmar cliffs (N edge x 14-16)
    for y in range(H):
        for x in range(W):
            m.cls[y, x] = 'T'
    path = [(29, 56), (29, 50), (22, 46), (14, 44), (10, 38), (12, 30), (20, 27), (30, 26), (38, 22), (30, 22), (25, 20),
            (24.5, 13), (24, 10), (18, 8), (15, 4), (15, -1)]
    m.lane(path, '.', 6.5, seed=3, only='T', wobble=1.6)
    for cx, cy, rx, ry in ((26, 3, 5, 2.6), (34, 9, 5, 3.6), (10, 41, 5, 4), (40, 44, 5, 4), (20, 32, 8, 4.5), (44, 24, 4, 3),
                           (35, 36, 6, 4), (12, 26, 4, 3), (8, 48, 5, 3.5)):
        m.blob(cx, cy, rx, ry, '.', seed=cx + cy, only='T', rough=0.6)
    m.lane([(29, 56), (29, 50), (22, 46), (14, 44), (10, 38), (12, 30), (20, 27), (30, 26), (38, 22), (30, 22), (25, 21), (24.5, 14),
            (24, 11), (18, 8), (15, 4), (15, -1)], 'd', 2.6, seed=4, only='.T', wobble=0.4)
    m.lane([(24, 11), (30, 10), (35, 9)], 'd', 2.2, seed=6, only='.T', wobble=0.3)        # to the Frost Loom shelf
    m.lane([(38, 22), (44, 24), (46, 24)], 'd', 2.0, seed=5, only='.T')       # to the frosted sapling (Cut) and the glade
    # the ravine (rows 15-18) under the fallen giant: frozen water, the trunk bridge at x 24-25
    for x in range(3, 45):
        a = 15 + int(round(1.2 * (vnoise(x, 0, 9, 4.0) - 0.5) * 2)); b = 18 + int(round(1.2 * (vnoise(x, 0, 10, 4.0) - 0.5) * 2))
        for y in range(a, b + 1):
            if m.cls[y, x] in '.dT': m.cls[y, x] = 'o'
    # the frozen Hoar Brook slide (18,30) 12x6: ice with 3 rock stoppers
    m.rect(18, 30, 12, 6, 'i', only='.dT')
    for cls_ in 'it': pass
    for (x0, y0, w, h) in ((6, 46, 10, 6), (30, 36, 10, 6), (10, 10, 10, 6)):
        m.rect(x0, y0, w, h, 't', only='.')
    # terraces: the aurora clearing (N) and the Frost Loom shelf (NE) stand one level up
    E = []
    trunk = [(24, y) for y in range(14, 20)] + [(25, y) for y in range(14, 20)]
    for x, y in trunk: m.cls[y, x] = 'D'
    m.cls[24:26, 14:20] = 'D'
    E += [trainer((14, 48), 'BUGCATCHER', 'Pell', "Bugs sleep in the ice here! I'm waking them up!", "They were NOT happy to be woken.", 'right'),
          trainer((30, 40), 'POKEMONRANGER_F', 'Orla', "Elowen forester. These woods are frozen, not dead. Prove you respect that.",
                  "You'll do. Mind the silk curtains, they cut.", 'left'),
          trainer((10, 26), 'HIKER', 'Ulf', "Trapping season! You look like you'd fit in a trap.", "Ha! No, no traps for you.", 'down'),
          trainer((36, 20), 'CAMPER', 'Rook', "I've camped here three nights. I can't feel my ears!", "...Is that what the aurora's for?", 'left'),
          trainer((22, 8), 'TWINS', 'Ana & Ida', "Two of us! Two Pokémon! Two kingdoms! Two-on-two!", "We split the loss. Half each.", 'down',
                  double=True),
          npc((40, 44), 'Lost trapper child', 'NPC 02', ["I'm not LOST. I'm... scouting. In circles.",
                                                          "...Can you tell Frostwick I'm by the big tree? Any big tree. They're all big."],
              again=["Still scouting! Still circles!"]),
          npc((8, 41), 'Trapper', 'NPC 22', ["Sit by the lean-to. Warm your Pokémon.", {'heal': True}, "There. Back to it."]),
          sign((33, 10), 'Frost Loom', "THE FROST LOOM\nA giant tree where drifting silk froze mid-weave. The warp still hums in a wind."),
          sign((24, 21), 'Fallen giant', "A fallen giant spans the ravine. Its bark is glazed in clear ice. Watch your step."),
          item((44, 52), 'ICEHEAL'), item((4, 30), 'GREATBALL'), item((40, 4), 'TM07', True),
          {'type': 'event', 'name': 'Applewood log', 'at': [35, 9], 'pages': [
              {'graphic': {'sprite': 'Object ball', 'dir': 'down'}, 'trigger': 'action', 'commands': [
                  'A seasoned applewood log, wrapped in sacking. Someone in Frostwick will want this.',
                  {'script': 'pfm_item(:APPLEWOODLOG, 1, "Applewood Log")'}, {'selfswitch': ['A', True]}]},
              {'cond': {'self': 'A'}, 'graphic': {'sprite': '', 'dir': 'down'}, 'trigger': 'action', 'commands': []}]},
          {'type': 'cut_tree', 'name': 'Frosted sapling', 'at': [46, 24]},
          {'type': 'warp', 'name': 'To Rimewood Glade', 'at': [47, 24], 'link': 'RIME_GLADE', 'arrive': [45, 24, 'left'], 'se': 'Door exit'}]
    pegs = [(28, 26), (30, 25), (32, 24), (34, 23), (26, 27)]
    E = seat(m, E[:-2], on='.dti') + E[-2:]
    for x, y in E[-2]['at'], E[-1]['at']:
        m.cls[y, x] = 'd'; m.taken[y, x] = True
    for e in E:
        if e['type'] == 'sign': signboard(m, e)
    for x, y in pegs:
        if m.free(x, y, 1, 1, on='.dt'): m.tile(4847, x, y, 1)
    m.near('kf_flat', 6, 37, on='.t', r=3)                                # the trapper's lean-to
    m.near('pf_g_tree4_ice', 31, 5, on='.tT', r=3)                         # the Frost Loom (a giant, silk frozen mid-weave)
    m.near('pf_p_loom', 34, 11, on='.t', r=2)
    for x, y in ((10, 32), (12, 33), (14, 31), (16, 33), (11, 35), (15, 36)):    # frozen silk curtains (soft walls)
        if m.free(x, y, 1, 2, on='.t'): m.stamp('pf_p_silk', x, y)
    for nm, x, y in (('pf_g_tree6_ice', 2, 2), ('pf_g_tree4p_ice', 38, 28), ('pf_g_tree2_ice', 2, 18), ('pf_g_tree4_ice', 40, 46),
                     ('pf_g_tree2_ice', 18, 50), ('pf_g_tree6_ice', 36, 0)):
        if m.free(x, y, STAMPS[nm]['w'], STAMPS[nm]['h'], on='T.t'): m.stamp(nm, x, y)
    for cx, cy, n in ((20, 40, 2), (8, 12, 1), (40, 38, 1), (30, 46, 2), (16, 22, 2), (42, 14, 1)):
        m.trees(cx, cy, n, ['pine2', 'kf_tree'], r=3, on='.t', seed=cx + cy)
    m.events = E
    m.paint()
    for x in (24, 25):                                                     # the fallen giant: an ice-glazed log bridge
        for y in range(14, 20):
            m.L[1, y, x] = C('sh', 497)
    ice(m); ice_floor(m, 'i')
    for x, y in ((21, 31), (26, 33), (23, 35)):                             # rock stoppers on the slide
        m.L[1, y, x] = 10551
    m.L[2, 0:4, 22:30][m.L[2, 0:4, 22:30] == 0] = 0
    rime_silk(m, ((6, 8), (12, 20), (30, 30), (40, 20), (20, 44), (34, 50)))
    m.scatter(8, seed=6)
    if prev: m.preview(prev, 0.5)
    m.write(562, head(562, 'The Rimewood', biome='forest', bgm='Natural Park',
                      metadata={'Outdoor': True, 'ShowArea': True, 'MapPosition': [0, 7, 20], 'BattleBack': 'snow', 'Weather': ['Snow', 30]},
                      tone=[-10, -4, 14, 16], fog={'name': 'prismfall_spores', 'opacity': 30, 'blend': 1, 'zoom': 100, 'sx': 1, 'sy': 1},
                      connections=[{'dir': 'N', 'offset': 12, 'to': 561, 'to_offset': 10}],
                      _file='562_rimewood.yaml'), '# The Rimewood (562). WRITTEN BY layouts/rimewood.py - edit that script.\n')
    return m


def ice_floor(m, cls):
    for y, x in np.argwhere(m.cls == cls):
        m.L[0, y, x] = ICE; m.L[1, y, x] = 0


# =================================================================================================== 563 Rimewood Glade
def glade(prev=None):
    W, H = 34, 30
    m = snowmap(W, H, 563)
    m.cls[:, :] = 'T'
    m.blob(18, 16, 14.5, 12.0, '.', seed=2, only='T', rough=0.9)
    m.lane([(0, 15), (6, 15), (8, 21), (14, 25), (24, 25), (28, 21)], 'd', 2.0, seed=3, only='.T')
    m.rect(0, 14, 3, 3, 'd', only='.T')
    m.blob(19, 14, 8.0, 5.0, 'i', seed=4, only='.', rough=0.55)                # the frozen pond (slide puzzle)
    for y in range(0, 6):                                                   # the Silk-fall pours from the ridge at x 14-19
        for x in list(range(9, 17)) + list(range(23, 29)): m.ht[y, x] = 1
    for y in range(0, 9):
        for x in range(17, 23): m.cls[y, x] = 'f'
    m.rect(2, 22, 10, 6, 't', only='.')
    E = [trainer((20, 24), 'POKEMONRANGER_M', 'Sigurd', "Isenmar ranger. Nobody finds this glade by accident.", "...So you cut your way in. Fair.", 'left'),
         item((19, 14), 'NEVERMELTICE'), item((30, 3), 'REVIVE', True),
         sign((28, 21), 'Snowveil Shrine', "THE SNOWVEIL SHRINE\nA pot of honey and a smoked eel sit side by side on the altar.\nNeither has been touched by the other."),
         sign((16, 9), 'Silk-fall', "THE SILK-FALL\nA waterfall of Gossamer silk, frozen as it fell. It rings faintly when the wind moves."),
         {'type': 'warp', 'name': 'To the Rimewood', 'at': [0, 15], 'link': 'RIME_GLADE', 'arrive': [1, 15, 'right'], 'se': 'Door exit'}]
    m.cls[15, 0] = 'd'
    E = seat(m, E[:-1], on='.dti') + E[-1:]
    m.taken[15, 0] = True
    for e in E:
        if e['type'] == 'sign': signboard(m, e)
    m.near('sh_gate', 27, 17, on='.d', r=2)
    for x, y in ((25, 4), (27, 5), (29, 4)):                                # the sleeping Stantler herd (decor events)
        if m.free(x, y, 1, 1, on='.t'): E.append({'type': 'event', 'name': 'Sleeping Stantler', 'at': [x, y], 'pages': [
            {'graphic': {'sprite': 'Followers/STANTLER', 'dir': 'down'}, 'trigger': 'action', 'commands': ['Zzz... The Stantler sleeps in the snow.']}]})
    m.greenfill(3, on='.')
    m.events = E
    m.auto['f'] = ('Waterfall (1)', 'rejuvenation'); m.AUTO_Z = dict(m.AUTO_Z, f=0); m.JOIN = dict(m.JOIN, f='f')
    m.paint()
    ice_floor(m, 'i')
    for x, y in ((14, 12), (22, 11), (25, 16), (16, 17), (20, 18), (13, 15)):  # stoppers on the pond
        if m.cls[y, x] == 'i': m.L[1, y, x] = 10371
    for y in range(0, 9):                                                   # frozen silk over the fall
        for x in range(17, 23):
            if (x + y) % 2 == 0: m.L[2, y, x] = STAMPS['pf_p_strand_w']['layers'][1][0][0] or m.L[2, y, x]
    m.scatter(10, seed=9)
    if prev: m.preview(prev, 0.5)
    m.write(563, head(563, 'Rimewood Glade', biome='forest', parent=562, bgm='Natural Park',
                      metadata={'Outdoor': True, 'ShowArea': True, 'MapPosition': [0, 8, 20], 'BattleBack': 'snow', 'Weather': ['Snow', 20]},
                      tone=[-6, -2, 16, 12], _file='563_rimewood_glade.yaml'),
            '# Rimewood Glade (563). WRITTEN BY layouts/rimewood.py - edit that script.\n')
    return m


# =================================================================================================== 561 Route 6
def route6(prev=None):
    W, H = 30, 60
    m = snowmap(W, H, 561, kit='aks', sea=True)
    old = yaml.safe_load_all(open(os.path.join(HERE, 'layouts', 'old_561.yaml')))
    old = next(s for s in old if s and s.get('id') == 561)
    # heath on the cliff-tops (h=1), the grey sea below them to the east with drift-ice
    for y in range(H):
        cx = 21 + int(round(1.5 * math.sin(y / 5.0) + 1.2 * (vnoise(0, y, 3, 5.0) - 0.5)))
        for x in range(W):
            if x < cx: m.ht[y, x] = 1
            else: m.cls[y, x] = 'w'
    for y in range(H):                                               # rock outcrops (h=2) where the Gullcry caves open (south faces)
        for x in range(0, 10):
            if y <= 20 or 24 <= y <= 35: m.ht[y, x] = 2
    m.rect(10, 56, 6, 4, '.')
    m.lane([(12, 60), (12, 50), (9, 44), (6, 39)], 'd', 2.4, seed=2, only='.')
    m.lane([(6, 24), (12, 22), (13, 14), (13, 4), (13, -1)], 'd', 2.4, seed=3, only='.')
    m.rect(4, 38, 4, 2, 'd'); m.rect(4, 23, 4, 2, 'd')
    for y in range(28, 33):                                          # the landslide: boulders across the cliff path
        for x in range(4, 22):
            if m.cls[y, x] == '.': m.cls[y, x] = 'B'
    m.rect(6, 44, 10, 8, 't', only='.'); m.rect(6, 6, 10, 8, 't', only='.')
    E = []
    for e in old['events']:
        e = dict(e)
        if e.get('name') == 'Gullcry north mouth': e['at'] = [5, 22]; e['arrive'] = [5, 23, 'down']
        elif e.get('name') == 'Gullcry south mouth': e['at'] = [5, 37]; e['arrive'] = [5, 38, 'down']
        elif e.get('name') == 'Trainer(4)': e['at'] = [13, 5]
        elif e['type'] == 'sign' and 'LANDSLIDE' in e.get('text', ''): e['at'] = [10, 34]; e['post'] = False
        E.append(e)
    E += [sign((13, 52), 'Whalebone waymarker', "A whale's rib, stood on end. Notches count the miles to Ebbmouth: four."),
          sign((16, 33), 'Cod-skull cairn', "A cairn of cod skulls. Isenmar fishers leave one for a good season and two for a bad one.\nThere are a lot of twos.")]
    for e in E:
        x, y = e['at']
        if e['type'] == 'warp': m.cls[y, x] = 'B'; m.cls[y + 1, x] = 'd'; m.taken[y, x] = True
    E = [e if e['type'] == 'warp' else e for e in E]
    E = seat(m, [e for e in E if e['type'] != 'warp'], on='.dt') + [e for e in E if e['type'] == 'warp']
    for e in E:
        if e['type'] == 'sign' and 'LANDSLIDE' in e.get('text', ''): signboard(m, e)
    m.near('kf_flat', 16, 40, on='.t', r=3); m.near('kf_flat', 17, 18, on='.t', r=3)        # fishing huts
    m.near('ak_boulder', 4, 12, on='.t', r=3)                                              # the ruined lookout
    for cx, cy, n in ((18, 55, 2), (6, 50, 1), (18, 8, 2), (8, 16, 1), (17, 46, 1), (16, 26, 2), (4, 56, 2), (19, 36, 1)):
        m.trees(cx, cy, n, ['pine2', 'kf_tree'], r=3, on='.t', seed=cx + cy)
    m.greenfill(3, on='.')
    m.events = E
    m.paint()
    for e in E:
        if e['type'] == 'warp': cave_mouth(m, e['at'][0], e['at'][1])
    rocks = [C('ak', 1644), C('ak', 1645), C('ak', 1652), C('ak', 1653)]
    for y, x in np.argwhere(m.cls == 'B'):
        if 28 <= y <= 32: m.L[1, y, x] = 10371 if (x + y) % 3 else 10551
    for y, x in np.argwhere(m.cls == 'w'):                        # drift-ice floes
        if vnoise(x, y, 7, 3.0) > 0.55 and m.L[1, y, x] == 0: m.L[1, y, x] = C('kf', 2476)
    m.scatter(10, seed=7)
    if prev: m.preview(prev, 0.5)
    h = head(561, 'Route 6', biome='route', display_name='Route 6 - Gullcry Cliffs', bgm='Route 3',
             metadata=old['metadata'], tone=[-10, -6, 6, 20], walk_from=[[5, 38]],
             connections=[{'dir': 'N', 'offset': 12, 'to': 160, 'to_offset': 22}, {'dir': 'S', 'offset': 10, 'to': 562, 'to_offset': 12}],
             _file='561_route6.yaml')
    m.write(561, h, '# Route 6 (561). WRITTEN BY layouts/rimewood.py - edit that script.\n')
    return m


def main():
    a = sys.argv[1:]
    which = [x for x in a if x.isdigit()] or ['560', '570', '562', '563', '561', 'int']
    pv = '--preview' in a
    if '560' in which: route5('/tmp/rj/m560.png' if pv else None)
    if '570' in which: frostwick('/tmp/rj/m570.png' if pv else None)
    if '562' in which: rimewood('/tmp/rj/m562.png' if pv else None)
    if '563' in which: glade('/tmp/rj/m563.png' if pv else None)
    if '561' in which: route6('/tmp/rj/m561.png' if pv else None)
    if 'int' in which or 'int' in a:
        import rimewood_interiors; rimewood_interiors.main()


if __name__ == '__main__':
    main()
