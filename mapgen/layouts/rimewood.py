#!/usr/bin/env python3
"""The Rimewood borderland stretch (Borderland A, WORLD.md 10; maps.json 560-576), on PF Rejuv tileset 52 "PF Rejuv
Snow" (Kristiline Town (Frozen) snow, ice and A-frame longhouses; Reborn Route 4 pines; snowified Sheridan cliffs,
forest and Prismfall's giant trees, rcustom.SNOW).  MAPGEN 2h.

Chain (each link is an edge connection; spans match maps.json):
  140 Saltmere --W(32)/E(12)--> 560 Frostflat Causeway --W(10)/E(18)--> 570 Frostwick --N(20)/S(22)--> 562 The Rimewood
  --N(12)/S(10)--> 561 Gullcry Cliffs --N(12)/S(22)--> 160 Ebbmouth;   562 (47,24) <-RIME_GLADE-> 563 (0,15)
Interiors 571-576 are Sheridan timber rooms (interiorkit, tileset 34).
Run: python3 -I layouts/rimewood.py && python3 -I build.py 560 561 562 563 570 571 572 573 574 575 576"""
import os, sys, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, yaml
import rkit as K
from rkit import C, STAMPS
from terrain import vnoise
HERE = K.HERE
ICES = [STAMPS['fw_ice%d' % v]['layers'][1][0][0] for v in range(4)]   # soft lagoon ice (rdraw.soft_ice), terrain tag 12
ICE = ICES[0]


def ice_at(x, y):
    n = vnoise(x, y, 77, 1.7)
    return ICES[0] if n < 0.45 else ICES[1] if n < 0.62 else ICES[2] if n < 0.82 else ICES[3]
CAVE = [[624, 625, 626], [632, 633, 634], [640, 641, 642]]


def snowmap(W, H, mid, kit='shs', sea=False):
    """a PF Rejuv Snow map: plain Kristiline snow ground (texture lives in decor, not in noisy ground), packed-snow
    lanes (class d, PF Packed Snow), exposed earth only where feet wear it through (class e, KristilineDirt: door
    aprons, stalls), frozen ponds you slide on (class p, PF Frozen Pond, terrain tag 12), Kristiline's frozen sea
    (o / I), the snow lattice forest"""
    m = K.RMap(W, H, 52, mid, water='Still water snow', kit=kit, grass=K.SNOW_GROUND, decor=K.DECOR_SNOW)
    m.tall = K.SNOW_TALL
    m.STAIRS = tuple(STAMPS['fw_stair_' + k]['layers'][1][0][0] for k in 'lmr')      # snowy timber stairs (rdraw)
    m.grass2 = None
    m.lattice = K.RMap.TREES_SNOW
    m.auto = {'d': ('Packed Snow', 'pf'), 'e': ('KristilineDirt', 'rejuvenation'), 'w': ('Still water snow', 'reborn'),
              'o': ('KristilineWatersFrozen', 'rejuvenation'), 'p': ('Frozen Pond', 'pf'), 'W': ('Sea deep', 'rejuvenation')}
    if sea: m.auto['w'] = ('Sea deep', 'rejuvenation'); m.auto.pop('W')
    m.JOIN = dict(K.RMap.JOIN, o='o', p='p', e='e'); m.AUTO_Z = dict(K.RMap.AUTO_Z, o=0, p=0, e=1)
    return m


def apron(m, door, w=3, h=2):
    """exposed earth worn through the snow in front of a door (class e), w wide, h deep"""
    x, y = door
    for yy in range(y + 1, y + 1 + h):
        for xx in range(x - w // 2, x - w // 2 + w):
            if m.inb(xx, yy) and m.cls[yy, xx] in '.dt' and not m.taken[yy, xx]: m.cls[yy, xx] = 'e'


def doorstep(m, door, depth=6):
    """earth at the doorstep, then packed snow straight down to the nearest lane"""
    x, y = door
    for k in range(1, depth + 1):
        yy = y + k
        if not m.inb(x, yy) or m.cls[yy, x] in 'dep' or m.taken[yy, x]: break
        if m.cls[yy, x] in '.tT':
            for xx in ((x - 1, x, x + 1) if k == 1 else (x, x + (1 if (x + y) % 2 else -1))):
                if m.inb(xx, yy) and m.cls[yy, xx] in '.tT' and not m.taken[yy, xx]: m.cls[yy, xx] = 'e' if k == 1 else 'd'


def smooth(m, c, into='.', passes=2, only=None):
    """majority-smooth a class region (no 1-cell spurs or notches) so autotile shorelines read as natural curves"""
    for _ in range(passes):
        cur = (m.cls == c)
        pad = np.pad(cur, 1)
        n = sum(np.roll(np.roll(pad, dy, 0), dx, 1)[1:-1, 1:-1] for dy in (-1, 0, 1) for dx in (-1, 0, 1)) - cur
        grow = ~cur & (n >= 5); shrink = cur & (n <= 3)
        if only is not None: grow &= np.isin(m.cls, list(only))
        m.cls[grow] = c; m.cls[shrink] = into


def ice_over(m, cls='w', edge=True):
    """walkable ice over the interior of a water body; the rim stays open water (fishing holes, the ice edge)"""
    for y in range(m.H):
        for x in range(m.W):
            if m.cls[y, x] != cls: continue
            nb = [(x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)]
            if not edge or all(not m.inb(a, b) or m.cls[b, a] == cls for a, b in nb):
                m.L[1, y, x] = ice_at(x, y)


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


# =================================================================================================== 560 Frostflat Causeway
def route5(prev=None):
    """Frostflat Causeway (560): a raised salt road (h=1, rows 12-14) on one long south-facing embankment,
    the salt half (east: brine pans with crusted rims, salt-cedars, the overturned salt wagon) turning to the frost half
    (west: frost-pans you slide on, frosted reeds); the Border Stones flank the road at mid-way under a bolted Meridian
    sunburst; Meridian survey pegs march across the flats.  The frozen lagoon (south) and the sea-ice (north) stay open."""
    W, H = 64, 30
    m = snowmap(W, H, 560)
    rng = random.Random(560)
    for x in range(W):
        top = 2 + int(round(1.0 * math.sin(x / 7.0) + vnoise(x, 0, 2, 5.0)))
        bot = 26 - int(round(1.0 * math.sin(x / 9.0 + 2) + 1.2 * vnoise(x, 0, 3, 6.0)))
        for y in range(H):
            if y <= (14 if 8 <= x <= 36 else 15): m.ht[y, x] = 1
            if y <= top: m.cls[y, x] = 'o'
            if y >= bot: m.cls[y, x] = 'o'
    lagoon(m, 0.5)
    m.rect(0, 12, W, 3, 'd', only='.')                                             # the causeway (rows 12-14 at both edges)
    m.rect(8, 11, 29, 1, 'd', only='.')                                            # ... riding a row higher mid-way
    m.rect(27, 11, 13, 1, 'd', only='.')                                           # it widens at the Border Stones
    for x0, w in ((4, 3), (17, 2), (44, 4), (55, 2)): m.rect(x0, 11, w, 1, 'd', only='.')   # lay-bys where carts pass
    for sx in (11, 29, 49):
        m.stairs(sx, 14 if 8 <= sx <= 36 else 15, w=3, kit_rows=4)                                          # three flights down the embankment
    m.rect(29, 18, 3, 8, 'd', only='.')                                            # the spur south to the old salt road
    for y in range(19, H):
        if m.cls[y, 30] in 'oI':
            for x in (29, 30, 31): m.cls[y, x] = 'D'
    m.lane([(12, 19), (13, 21), (18, 22)], 'd', 2.0, seed=4, only='.')
    m.lane([(50, 19), (50, 21), (44, 22)], 'd', 2.0, seed=5, only='.')
    # north flats (h=1): frost-pans west (slide), brine pans with crusted rims east, reeds between
    for cx, cy, rx, ry in ((6, 6, 3.4, 1.6), (15, 5, 2.6, 1.3), (21, 8, 2.2, 1.2)):
        m.blob(cx, cy, rx, ry, 'p', seed=cx + 50, only='.', rough=0.35)
    for x0, y0, w, h in ((41, 4, 4, 2), (46, 4, 5, 2), (52, 5, 4, 2), (43, 7, 4, 2), (49, 8, 5, 2), (56, 8, 4, 2)):
        m.rect(x0, y0, w, h, 'w', only='.')                                        # the salt-works' evaporation pans
    for cx, cy, rx, ry in ((26, 5, 3.0, 1.6), (34, 6, 3.4, 1.4), (11, 9, 2.6, 1.0), (60, 4, 2.0, 1.2)):
        m.blob(cx, cy, rx, ry, 't', seed=cx, only='.', rough=0.7)
    # south flats (h=0): the first slide (a frost-pan with two stoppers), salt crust, reeds
    m.blob(15, 23.0, 6.0, 2.2, 'p', seed=21, only='.', rough=0.35)
    smooth(m, 'p', into='.', passes=1)
    for cx, cy, rx, ry in ((40, 21, 3.0, 1.4), (57, 20, 2.6, 1.6), (6, 20, 2.0, 1.2), (23, 20, 2.2, 1.0)):
        m.blob(cx, cy, rx, ry, 't', seed=cx + 9, only='.', rough=0.6)
    E = []
    m.stamp('fw_stone', 30, 9); m.stamp('fw_stone', 36, 9)                         # the Border Stones
    E.append(sign((30, 10), 'Border Stones', "Two old stones. One bears Elowen's briar crown, the other Isenmar's whale and axe.\n"
                  "A brass Meridian sunburst has been bolted across both of them. The bolts are new."))
    E.append(sign((60, 11), 'Route sign', "FROSTFLAT CAUSEWAY\nW: Frostwick   E: Saltmere"))
    E.append(sign((32, 27), 'Old salt road', "The old salt road dips toward a drowned pier village. Something replays there, over and over.\n"
                  "[The Rehearsal, map 568: not built yet]"))
    E += [npc((33, 10), 'Royal forester', 'NPC 14', ["Past the stones the trees wear coats. Ice ones. You'll see.",
                                                     "Elowen ends here, officially. Unofficially it ends wherever the honey runs out."],
              again=["Mind the frost-pans west of here. They're slick as a courtier."]),
          npc((22, 15), 'Fur-trader', 'NPC 22', ["My Spheal pulls the sled. Lovely creature. Round.",
                                                  "...The problem is the sled is on a SLOPE, and Spheal is ALSO round.",
                                                  "If you see a sled rolling toward Saltmere with a Spheal on it, wave. It likes that."],
              again=["Still no sled. Still no Spheal. Still a lovely day."]),
          npc((20, 7), 'Meridian surveyor', 'NPC 16', ["*tink* *tink* Survey peg. Lattice line. Don't touch.",
                                                       "Who authorised it? The Meridian. Who authorised the Meridian? ...Move along, please."],
              d='left')]
    E += [trainer((48, 10), 'PICNICKER', 'Sela', "Salt-flat picnic! Bring your own shade!", "Isenmar's colder than I thought.", 'down'),
          trainer((42, 19), 'HIKER', 'Torvald', "Thirty years I've carted salt down this road! Show me something new!",
                  "Salt in my boots, frost in my beard. Good trade.", 'up'),
          trainer((9, 21), 'LASS', 'Tilde', "Did you slide here too? Everyone slides here.", "My Swinub slid farther than me.", 'right'),
          trainer((18, 10), 'SAILOR', 'Haakon', "Sealer out of Ebbmouth! The sea's too thick to row, so I walk!",
                  "Ice'll break by summer. Probably.", 'down'),
          trainer((26, 21), 'BIRDKEEPER', 'Ailsa', "The gulls change colour past the stones. Watch!",
                  "Frostwick's gulls wear little ice hats. Not really.", 'up'),
          item((62, 5), 'SUPERPOTION'), item((3, 8), 'ICEHEAL'), item((56, 23), 'SOFTSAND', True)]
    # the overturned salt wagon (HEALPOWDER inside): crates, a barricade, the sled on its side, spilled salt
    m.near('sh_crates', 44, 20, on='.t', r=3); m.near('pf_barricade', 46, 21, on='.t', r=3); m.near('fw_sled', 47, 19, on='.t', r=3)
    E.append(item((45, 23), 'HEALPOWDER'))
    E = seat(m, E, on='.dt')
    for e in E:
        if e['type'] == 'sign' and e['name'] != 'Border Stones': signboard(m, e)
    # the causeway's north verge: a rope-and-post rail with gaps where tracks lead onto the flats
    for x0, x1 in ((1, 7), (13, 19), (23, 26), (41, 46), (51, 58)):
        for x in range(x0, x1 + 1):
            vy = 10 if 8 <= x <= 36 else 11
            if m.cls[vy, x] == '.' and not m.taken[vy, x]: m.stamp('fw_pal_h', x, vy, mark='B')
    for x, y in ((5, 4), (9, 5), (13, 6), (17, 7), (21, 4), (25, 9), (37, 4), (52, 2 + 1), (55, 17), (36, 20), (20, 18), (8, 18)):
        if m.free(x, y, 1, 1, on='.t'): m.stamp('fw_peg', x, y)
    for cx, cy in ((38, 18), (41, 25), (36, 23), (54, 17), (57, 7), (60, 22), (3, 17), (24, 24)):
        m.trees(cx, cy, 1, ['pine2', 'tr_teal'], r=2, on='.t', seed=cx)
    for cx, cy in ((4, 9), (2, 18), (24, 4), (18, 24), (8, 25), (34, 6), (46, 2), (60, 8), (48, 17), (62, 22), (1, 24),
                   (28, 7), (54, 24), (39, 8), (13, 18)):
        m.trees(cx, cy, 2, ['pine2', 'kf_tree', 'pine2'], r=3, on='.t', seed=cx)
    for nm, x, y in (('fw_rack', 38, 9), ('fw_wood', 57, 10), ('fw_skull', 14, 9), ('pf_lantern', 27, 9), ('pf_lantern', 39, 9),
                     ('fw_sled', 7, 10), ('sh_crates', 61, 8), ('fw_brazier', 41, 10)):
        m.near(nm, x, y, on='.t', r=2)
    m.events = E
    m.greenfill(3, on='.')
    m.paint(); ice(m)
    for y in range(19, H):                                                         # the spur's boardwalk over the lagoon ice
        for i, x in enumerate((29, 30, 31)):
            if m.cls[y, x] == 'D': m.L[1, y, x] = C('ak', 1524 + i)
    for x, y in ((14, 23), (18, 22)):                                              # stoppers on the first slide
        if m.cls[y, x] == 'p': m.L[1, y, x] = 10371
    for y, x in np.argwhere(m.cls == 'w'):                                         # salt crust on the brine pans
        if vnoise(x, y, 61, 2.0) > 0.62: m.L[1, y, x] = ice_at(x, y)
    m.scatter(16, seed=5)
    icy_faces(m, 0.6, seed=560)
    dress_ice(m, 0.75, seed=560)
    reed_beds(m, 130, seed=561)
    road_tracks(m, 0.10, seed=560)
    drifts(m, 0.16, seed=560)
    if prev: m.preview(prev, 0.5)
    m.write(560, head(560, 'Frostflat Causeway', biome='route', display_name='Frostflat Causeway', bgm='Route 2',
                      metadata={'Outdoor': True, 'ShowArea': True, 'MapPosition': [0, 7, 22], 'BattleBack': 'snow', 'Weather': ['Snow', 10]},
                      tone=[-6, -2, 10, 10],
                      connections=[{'dir': 'E', 'offset': 12, 'to': 140, 'to_offset': 32}, {'dir': 'W', 'offset': 10, 'to': 570, 'to_offset': 21}],
                      _file='560_route5.yaml'), '# Frostflat Causeway (560). WRITTEN BY layouts/rimewood.py - edit that script.\n')
    return m


def ice(m):
    """class i / I: walkable ice ground (slides); class w interiors iced over"""
    for y, x in np.argwhere(np.isin(m.cls, ['i', 'I'])):
        m.L[0, y, x] = ice_at(x, y)
    ice_over(m, 'w')


# =================================================================================================== 570 Frostwick
TL, NL, EL = 12, 8, 5                    # lips: the Elowen treehouse terrace (NW), the north band, the north-east bench
SQ0, SQ1 = 22, 28                        # the square (rows) and the Hearth Road east to the gate (rows 23-25)
ROAD = (23, 25)
LANE = (36, 38)                          # the south lane along the lagoon


def fw_bx(y):
    return 29 + int(round(1.0 * math.sin(y / 6.0)))


def over_tiles(m, name, x, y, z=2):
    """paint a drawn piece straight onto a layer after paint() (walkways, smoke): only into empty cells"""
    L = np.array(STAMPS[name]['layers'])
    for dy in range(L.shape[1]):
        for dx in range(L.shape[2]):
            t = int(L[:, dy, dx].max())
            if t and m.inb(x + dx, y + dy) and m.L[z, y + dy, x + dx] == 0: m.L[z, y + dy, x + dx] = t


def frostwick(prev=None):
    """Frostwick (570): two peoples, one town.  The Elowen side lives UP in three ice-glazed giants on the north-west
    terrace (treehouses joined by rope walkways, applewood smoke from the crowns); the Isenmar side lives DOWN on the
    ground in whalebone longhouses with turf roofs under deep snow (whale-oil smoke).  The Hoar Brook comes off the north
    band as a frozen fall beside the stairs into town, runs through the square (walkable ice, fishing holes) and out to
    the frozen salt lagoon.  The centrepiece is the Hearth Elder: a huge ice-glazed elder on the square whose hollow is
    the Exchange; the shared market (Elowen honey and silk, Isenmar fish and furs) stands in the square below it with
    the Hearth Stone between the two stall rows.  The east gate is a briar-wrapped whale-rib arch."""
    W, H = 60, 48
    m = snowmap(W, H, 570)
    rng = random.Random(570)
    # ------------------------------------------------------------------ terrain: terraces, brook, lagoon, woods
    def lip(x):
        if x <= 24: return TL
        if x <= 35: return NL
        return EL + (1 if vnoise(x, 0, 3, 5.0) > 0.6 else 0)
    for x in range(W):
        for y in range(H):
            if y <= lip(x): m.ht[y, x] = 1
    for y in range(H):
        for x in range(fw_bx(y), fw_bx(y) + 4): m.cls[y, x] = 'p'           # the frozen Hoar Brook (walkable ice)
    m.blob(32.0, 13.6, 3.0, 1.9, "p", seed=31, rough=0.4, only=".")          # plunge pool under the fall
    for y in range(40, H):                                                   # the salt lagoon, frozen (Kristiline sea ice)
        for x in range(W):
            if y >= 40 + 2 * vnoise(x, 0, 4, 6.0): m.cls[y, x] = 'o'
    lagoon(m, 0.66)
    for y in range(H):                                                       # the Rimewood: north band, NE bench, west edge
        for x in range(W):
            if m.cls[y, x] != '.': continue
            north = m.ht[y, x] == 1 and (y <= lip(x) - 6 + 2 * vnoise(x, 0, 7, 4.0) or x >= 36)
            west = x <= 1 + 2 * vnoise(0, y, 6, 4.0) and y > TL
            if north or west: m.cls[y, x] = 'T'
    for y in range(0, 3):                                                    # NW terrace: woods along its back
        for x in range(0, 25):
            if m.cls[y, x] == '.': m.cls[y, x] = 'T'
    # ------------------------------------------------------------------ streets (packed snow): curved lanes of varying
    # width feeding one real plaza round the Hearth Stone and the Elder, not a grid
    m.rect(26, 0, 3, NL, 'd', only='.T')                                     # the path from the Rimewood (x 26-28)
    m.stairs(26, NL, w=3, kit_rows=4)
    m.lane([(27.5, NL + 4), (26.6, 15), (25.4, 18), (24.5, 22)], 'd', 2.6, seed=71, wobble=0.5)
    m.blob(19.5, 25.6, 12.0, 4.3, 'd', seed=72, rough=0.35, only='.T')       # the plaza, west of the brook
    m.blob(40.5, 26.2, 7.6, 4.2, 'd', seed=73, rough=0.35, only='.T')        # ... and its east half under the Hearth Elder
    m.lane([(46, 25.2), (51, 24), (55, 24.2), (60, 24)], 'd', 3.0, seed=74, wobble=0.4)   # the Hearth Road to the gate
    m.rect(56, ROAD[0], 4, 3, 'd', only='.T')
    m.lane([(3, TL - 1.2), (9, TL - 1.6), (15, TL - 1.0), (23, TL - 1.5)], 'd', 1.9, seed=75, wobble=0.3)   # the terrace walk
    m.rect(9, TL - 1, 3, 1, 'd', only='.T')
    m.stairs(9, TL, w=3, kit_rows=4)
    m.lane([(10.5, TL + 4), (9.2, 18.5), (10.5, 22)], 'd', 2.3, seed=76, wobble=0.5)
    m.lane([(2, 37.2), (11, 37.6), (21, 36.6), (29, 37.4), (40, 37.6), (50, 36.8), (57, 37.2)], 'd', 2.5, seed=77, wobble=0.7)   # the shore lane
    m.lane([(26.5, 29), (27.6, 32.5), (26.6, 36.5)], 'd', 2.2, seed=78, wobble=0.5)
    m.lane([(45, 38), (45.5, 41)], 'd', 2.6, seed=79, wobble=0.2)             # down to the jetty
    smooth(m, 'd', into='.', passes=1)
    # ------------------------------------------------------------------ the frozen fall (the brook leaves the north band)
    m.stamp('fw_fall', fw_bx(NL), NL - 1)
    # ------------------------------------------------------------------ buildings
    d = {}
    d['loft'] = m.stamp('pf_g_tree6_ice', 1, 2, 'FW_LOFT', 'Loft door', blend=True)
    m.stamp('pf_g_tree4_ice', 11, 3, blend=True)                             # two more treehouses (private)
    m.stamp('pf_g_tree4p_ice', 18, 2, blend=True)
    d['inn'] = m.stamp('wb_inn', 13, TL + 4, 'FW_INN', 'Two Hearths door')
    d['exch'] = m.stamp('pf_g_elder_ice', 34, SQ0 - 12, 'FW_EXCH', 'Exchange door')
    d['border'] = m.stamp('wb_long2', 46, SQ0 - 6, 'FW_BORDER', 'Border House door')
    m.stamp('wb_gate', 54, ROAD[1] - 4)
    d['pc'] = m.stamp('wb_pc', 2, LANE[0] - 7, 'FW_PC', 'Poke Center door')   # the Center keeps house the local way
    extra = [m.stamp('wb_hut', 14, LANE[0] - 6, None, 'x'), m.stamp('wb_long3', 33, LANE[0] - 7, None, 'x'),
             m.stamp('wb_short', 45, LANE[0] - 6, None, 'x')]
    d['smoke'] = m.stamp('wb_smoke', 52, LANE[0] - 7, 'FW_SMOKE', 'Smokehouse door')
    m.events = [e for e in m.events if e.get('name') != 'x']
    for k, (dx, dy) in d.items(): doorstep(m, (dx, dy))                      # earth at the doorsteps, a trodden line to the lane
    for nm, hx, hy in (('wb_hut', 14, LANE[0] - 6), ('wb_long3', 33, LANE[0] - 7), ('wb_short', 45, LANE[0] - 6)):
        dd = STAMPS[nm]['door']; doorstep(m, (hx + dd[0], hy + dd[1]))
    for y in range(7, 40):                                                   # the palisade along the east edge
        if not (ROAD[0] - 4 <= y <= ROAD[1]) and m.cls[y, 58] in '.T' and m.ht[y, 58] == 0 and not m.taken[y, 58]:
            m.stamp('fw_pal_v', 58, y, mark='B')
    # ------------------------------------------------------------------ the market, the Hearth Stone, braziers
    m.stamp('fw_stall_e', 11, 24); m.stamp('fw_stall_e', 16, 24)
    m.stamp('fw_stall_i', 37, 25); m.stamp('fw_stall_i', 41, 25)
    m.stamp('fw_stone', 24, 24)
    m.stamp('fw_stall_e', 6, 24)
    for nm, x, y in (('pf_logbench', 22, 27), ('pf_logbench', 25, 27), ('sh_campfire', 25, 21), ('fw_sled', 44, 28),
                     ('sh_crates', 45, 26), ('fw_wood', 34, 28), ('pf_logbench', 36, 28)):
        if m.free(x, y, STAMPS[nm]['w'], STAMPS[nm]['h'], on='.d'): m.stamp(nm, x, y)
        else: print('  (frostwick: no room for %s at %d,%d)' % (nm, x, y))
    for x, y in ((21, 23), (13, 28), (35, 23), (45, 24)): m.stamp('fw_brazier', x, y)
    for nm, x, y in (('fw_ban_e', 12, 21), ('fw_ban_i', 23, 21), ('fw_ban_e', 52, 21), ('fw_ban_i', 47, 26)):
        if m.free(x, y, 1, 2, on='.d'): m.stamp(nm, x, y)
    E = []
    E += [sign((24, 25), 'Hearth Stone', "THE HEARTH STONE\nCarved twice: once in Elowen's knotwork, once in Isenmar's runes.\n"
                                         "Both say the same thing. \"Here, no one is a foreigner by the fire.\""),
          sign((53, 26), 'Town sign', "FROSTWICK\nWhere the Rimewood meets the salt."),
          sign((10, 36), 'PC sign', "POKEMON CENTER"),
          sign((43, 22), 'Exchange sign', "THE EXCHANGE\nIn the hollow of the Hearth Elder. Honey for furs. Silk for oil. Coin if you must."),
          sign((22, 22), 'Inn sign', "THE TWO HEARTHS\nApplewood on the left. Whale oil on the right. Sit where you like."),
          npc((20, 23), 'Brannagh', 'NPC 25', ["Brannagh, Elowen side of the Two Hearths. Applewood fire, honey cakes, no shouting.",
                                               "Halvard's lot burn whale oil on the other hearth. Smells like a shipwreck. We get on fine."],
              again=["Find me an applewood log in the Rimewood and I'll show that whale-oil man what a fire is."]),
          npc((17, 23), 'Halvard', 'NPC 28', ["Halvard. Sealer. Isenmar side of the Two Hearths.",
                                              "Brannagh's applewood smells like a pudding. A man can't think by a pudding."],
              again=["Ask her about the log. Go on. I want to watch her face."]),
          npc((14, 27), 'Honey-seller', 'NPC 06', ["Rimewood honey! The bees sleep all winter, so every jar is a summer someone saved.",
                                                   "Isenmar folk pay in eel. I've learned to like eel. Mostly."], d='down'),
          npc((40, 28), 'Fishmonger', 'NPC 20', ["Lagoon char, smoked eel, a Spheal-fat candle if your nights are long.",
                                                 "The Elowen lot haggle in poetry. I haggle in fish. We both go home happy."], d='down'),
          npc((8, 26), 'Girl in ogre mask', 'NPC 07', ["We're playing Kingdoms! I'm Elowen! RAAAH! Briar curse!"], move='random'),
          npc((9, 27), 'Boy in whale mask', 'NPC 03', ["I'm Isenmar! Whale curse! ...There's no whale curse. I'm making it up."], move='random'),
          npc((57, 26), 'Huscarl', 'NPC 11', ["Gate's open. Wipe your boots. Declare any honey."], d='left'),
          npc((57, 22), 'Forester', 'NPC 14', ["Elowen's watch. Isenmar's watch. Same gate, same cold. We split the shifts."], d='left'),
          npc((32, 17), 'Ice-fisher', 'trainer_FISHERMAN', ["See the dark holes in the brook ice? Fish come up to breathe.",
                                                             "Face the open water and use a rod. Even an Old Rod works here."], d='down'),
          npc((50, 39), 'Swinub herder', 'NPC 17', ["The sled-Swinub. Mamoswine by spring if they eat their greens.",
                                                     "They don't eat greens. They eat everything else."]),
          npc((7, 10), 'Rime-silk weaver', 'NPC 09', ["Up here we weave the silk that froze in the Rimewood. It never thaws, so it never frays.",
                                                      "The walkways? Elowen children learn to cross them before they learn to read."]),
          item((40, 42), 'SNOWBALL', True), item((22, 10), 'NEVERMELTICE', True)]
    E = seat(m, E, on='.dpe')
    for e in E:
        if e['type'] == 'sign' and e['name'] != 'Hearth Stone': signboard(m, e)
    # ------------------------------------------------------------------ yards, the lagoon shore, the jetty
    for nm, x, y in (('fw_rack', 23, 31), ('fw_wood', 22, 34), ('fw_sled', 25, 33), ('fw_rack', 31, 39), ('fw_sled', 47, 39),
                     ('fw_rack', 54, 39), ('fw_skull', 33, 27), ('fw_wood', 5, 18), ('fw_wood', 47, 13), ('fw_rack', 51, 13),
                     ('fw_sled', 20, 39), ('fw_skull', 6, 39), ('sh_crates', 43, 27), ('sh_crates', 20, 27), ('fw_wood', 30, 32),
                     ('pf_lantern', 8, 20), ('pf_lantern', 25, 19), ('pf_lantern', 47, 22), ('pf_lantern', 12, 37), ('pf_lantern', 33, 35),
                     ('pf_lantern', 51, 35), ('pf_lantern', 4, 9), ('pf_lantern', 20, 9)):
        m.near(nm, x, y, on='.', r=3)
    m.stamp('fw_boat', 38, 42); m.stamp('fw_boat', 49, 43)                    # boats frozen in at the jetty
    for nm, x, y in (('fw_boat_over', 15, 39), ('fw_boat_over', 52, 39)): m.near(nm, x, y, on='.', r=3)
    for y in range(LANE[1] + 1, 46):                                         # the jetty out onto the ice (Akuwa pier planks)
        for i, x in enumerate((44, 45, 46)):
            m.tile(C('ak', (1516 if y == LANE[1] + 1 else 1524) + i), x, y, 1); m.cls[y, x] = 'D'
    for cx, cy, n in ((6, 31, 1), (29, 15, 1), (50, 9, 2), (56, 13, 2), (24, 34, 1), (11, 33, 1), (42, 12, 1), (3, 25, 2), (58, 34, 1),
                      (4, 18, 3), (7, 15, 1), (2, 22, 1)):
        m.trees(cx, cy, n, ['pine2', 'kf_tree', 'pine2'], r=2, on='.', seed=cx * 7 + cy)
    m.greenfill(3)
    m.events = [e for e in m.events if e['type'] == 'door'] + E
    m.paint()
    bridges(m, (ROAD, LANE), cls='p')
    ice(m)
    hole, holet = STAMPS['fw_hole']['layers'][1][0][0], STAMPS['fw_hole_t']['layers'][1][0][0]
    for i, (x, y) in enumerate(((31, 16), (30, 19), (32, 29), (30, 33), (31, 40))):   # fishing holes in the brook ice
        if m.cls[y, x] == 'p' and m.L[1, y, x] == 0 and m.L[2, y, x] == 0: m.L[1, y, x] = holet if i % 2 == 0 else hole
    for y, x in np.argwhere(m.cls == 'I'):                                   # ... and out on the lagoon
        if vnoise(x, y, 43, 2.0) > 0.86 and m.L[1, y, x] in ICES: m.L[1, y, x] = holet if (x + y) % 3 == 0 else hole
    # rope walkways between the treehouse boles (high overhead), with lanterns at the lashings
    for x0, x1, y in ((8, 11, 7), (16, 18, 7)):
        for x in range(x0, x1 + 1):
            over_tiles(m, 'fw_walk_e' if x == x0 else 'fw_walk_w' if x == x1 else 'fw_walk_h', x, y)
    # hearth smoke: applewood from the treehouse crowns and the inn's timber chimney, whale oil from the longhouses
    for nm, x, y in (('fw_smoke_a', 6, 0), ('fw_smoke_a', 14, 1), ('fw_smoke_w', 16, TL + 2), ('fw_smoke_a', 22, TL + 2),
                     ('fw_smoke_w', 18, LANE[0] - 8), ('fw_smoke_w', 40, LANE[0] - 8), ('fw_smoke_w', 48, LANE[0] - 8),
                     ('fw_smoke_w', 54, LANE[0] - 8), ('fw_smoke_w', 57, LANE[0] - 8), ('fw_smoke_w', 51, SQ0 - 8)):
        over_tiles(m, nm, x, y)
    rime_silk(m, ((3, 2), (9, 3), (17, 2), (23, 3), (35, 11), (45, 11)))
    m.scatter(6, seed=8)
    dress_ice(m, 0.30, seed=570)
    for y, x in np.argwhere(m.cls == 'p'):                                   # the brook ice: cracks and drifts, not a stripe
        if m.L[1, y, x] == 0 and m.L[2, y, x] == 0 and vnoise(x, y, 91, 1.5) > 0.6:
            m.L[1, y, x] = STAMPS['fw_crack%d' % ((x + y) % 3)]['layers'][1][0][0] if (x * 3 + y) % 2 else STAMPS['fw_drift%d' % ((x + y) % 3)]['layers'][1][0][0]
    road_tracks(m, 0.07, seed=570)
    drifts(m, 0.07, seed=570)
    if prev: m.preview(prev, 0.5)
    m.write(570, head(570, 'Frostwick', biome='village', bgm='Lerucean Town',
                      metadata={'Outdoor': True, 'ShowArea': True, 'MapPosition': [0, 7, 21], 'BattleBack': 'snow', 'Weather': ['Snow', 20]},
                      tone=[-8, -4, 12, 12], fog={'name': 'prismfall_seamist', 'opacity': 30, 'blend': 0, 'zoom': 100, 'sx': 1, 'sy': 0},
                      connections=[{'dir': 'N', 'offset': 20, 'to': 562, 'to_offset': 22}, {'dir': 'E', 'offset': 21, 'to': 560, 'to_offset': 10}],
                      _file='570_frostwick.yaml'), '# Frostwick (570). WRITTEN BY layouts/rimewood.py - edit that script.\n')
    print('frostwick doors', d)
    return m


def dress_ice(m, p=0.2, seed=2):
    """sea and lagoon ice is not blank: pressure cracks, drifts on the ice, a few fishing holes, frosted reeds where the
    ice meets the shore, loose floes on the open leads (all decals: nothing is filled in)"""
    rng = random.Random(seed)
    one = lambda n: STAMPS[n]['layers'][1][0][0]
    cracks = [one('fw_crack%d' % i) for i in range(3)]; ds = [one('fw_drift%d' % i) for i in range(3)]
    floes = [one('fw_floe%d' % i) for i in range(2)]; hole = one('fw_hole')
    land = ~np.isin(m.cls, ['I', 'o', 'p', 'w', 'W'])
    pad = np.pad(land, 1)
    for y, x in np.argwhere(m.cls == 'I'):
        if m.L[1, y, x] or m.L[2, y, x] or m.taken[y, x]: continue
        shore = pad[y:y + 3, x:x + 3].any()
        r = rng.random()
        if shore and r < 0.35 and m.inb(x, y - 1) and m.L[2, y - 1, x] == 0 and m.cls[y - 1, x] in 'I.t':
            st = STAMPS['fw_reeds%d' % rng.randrange(2)]['layers']
            m.L[1, y, x] = st[1][1][0]; m.L[2, y - 1, x] = st[2][0][0]
        elif r < p * 0.55: m.L[1, y, x] = rng.choice(cracks)
        elif r < p * 0.9: m.L[1, y, x] = rng.choice(ds)
        elif r < p: m.L[1, y, x] = hole
    for y, x in np.argwhere(m.cls == 'o'):
        if m.L[1, y, x] == 0 and rng.random() < p * 0.35 and not pad[y:y + 3, x:x + 3].any(): m.L[1, y, x] = rng.choice(floes)


def icy_faces(m, p=0.45, seed=4):
    """icicles down the snowy cliff faces (first face row under each lip), so long embankments are not one tile repeated"""
    rng = random.Random(seed)
    ic = [STAMPS['fw_icy%d' % i]['layers'][2][0][0] for i in range(3)]
    for (x, y), (kind, k, h) in getattr(m, 'pieces', {}).items():
        if kind == 'row' and k == 1 and m.L[2, y, x] == 0 and rng.random() < p: m.L[2, y, x] = rng.choice(ic)


def road_tracks(m, p=0.08, seed=5):
    """sled tracks and bootprints on the packed snow (very light decals; the road stays the clearest thing on the map)"""
    rng = random.Random(seed)
    tk = [STAMPS['fw_tracks%d' % i]['layers'][1][0][0] for i in range(2)]
    for y, x in np.argwhere(m.cls == 'd'):
        if m.L[2, y, x] == 0 and not m.taken[y, x] and not m.cliff[y, x] and rng.random() < p and m.L[1, y, x] >= 48 * 1:
            m.L[0, y, x] = m.L[1, y, x]; m.L[1, y, x] = rng.choice(tk)


def reed_beds(m, n, seed=3, on='.t'):
    """clumps of frosted bulrushes on open ground (1x2: seed heads on layer 3)"""
    rng = random.Random(seed)
    cells = [tuple(c) for c in np.argwhere((np.isin(m.cls, list(on))) & ~m.taken & (m.L[1] == 0) & (m.L[2] == 0))]
    rng.shuffle(cells); k = 0
    for y, x in cells:
        if k >= n: break
        if y > 0 and m.L[2, y - 1, x] == 0 and m.L[1, y - 1, x] == 0 and m.cls[y - 1, x] in on and not m.cliff[y, x] and not m.cliff[y - 1, x]:
            st = STAMPS['fw_reeds%d' % rng.randrange(2)]['layers']
            m.L[1, y, x] = st[1][1][0]; m.L[2, y - 1, x] = st[2][0][0]; k += 1


def drifts(m, p, seed=1):
    """snowdrifts and dry stalks on open snow (ground-layer decals), thicker along walls and woods"""
    rng = random.Random(seed)
    ds = [STAMPS['fw_drift%d' % i]['layers'][1][0][0] for i in range(3)]
    open_ = (m.cls == '.') & ~m.taken & (m.L[1] == 0) & (m.L[2] == 0)
    pad = np.pad(open_, 1, constant_values=True)
    for y, x in np.argwhere(open_):
        edge = not pad[y:y + 3, x:x + 3].all()
        if rng.random() < p * (2.2 if edge else 1.0): m.L[1, y, x] = rng.choice(ds)


def bridges(m, rows, cls='w'):
    """timber bridges where a road crosses the brook: split planks under trodden snow, a snow-capped post-and-beam
    rail along the north and south edges (rdraw `fw_bridge_*`; the rails block stepping off sideways)"""
    T = lambda k, x: STAMPS['fw_bridge_%s%d' % (k, x % 2)]['layers'][1][0][0]
    for y0, y1 in rows:
        for y in range(y0, y1 + 1):
            for x in range(m.W):
                if m.cls[y, x] == cls:
                    m.L[1, y, x] = T('n' if y == y0 else 's' if y == y1 else 'm', x)


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
    for x in range(1, 47):
        c = 16.5 + 1.6 * math.sin(x / 6.5) + 1.4 * (vnoise(x, 0, 9, 3.0) - 0.5)
        hw = 1.2 + 1.3 * vnoise(x, 0, 10, 4.0) + (0.8 if 20 <= x <= 29 else 0)
        for y in range(int(c - hw), int(round(c + hw)) + 1):
            if 0 <= y < m.H and m.cls[y, x] in '.dT': m.cls[y, x] = 'o'
    smooth(m, 'o', into='T', passes=3)
    bank = np.zeros((m.H, m.W), bool)                                          # a ragged open bank, not trees to the brink
    for y, x in np.argwhere(m.cls == 'o'): bank[max(0, y - 2):y + 3, max(0, x - 1):x + 2] = True
    for y, x in np.argwhere(bank & (m.cls == 'T')):
        if vnoise(x, y, 12, 2.5) > 0.42: m.cls[y, x] = '.'
    # the frozen Hoar Pond: an irregular pond (PF Frozen Pond, terrain tag 12) on the Hoar Brook, smoothed so the snow-bank
    # shoreline curves; a snowy islet in the middle holds the prize; ice blocks are the stoppers (slide_puzzle)
    for cx, cy, rx, ry, sd in ((22.5, 33.4, 6.2, 3.4, 19), (28.8, 34.8, 4.0, 2.6, 21), (17.6, 31.4, 2.8, 2.0, 23),
                               (25.5, 30.7, 3.2, 1.5, 25), (31.5, 32.2, 1.8, 1.4, 27)):   # a kidney of lobes, not a box
        m.blob(cx, cy, rx, ry, 'p', seed=sd, rough=0.35, only='.dT')
    smooth(m, 'p', into='.', passes=2)
    ISLET = [(25, 33), (26, 33), (24, 34), (25, 34), (26, 34), (25, 35)]
    for x, y in ISLET: m.cls[y, x] = '.'; m.taken[y, x] = True
    for (x0, y0, w, h) in ((6, 46, 10, 6), (30, 36, 10, 6), (10, 10, 10, 6)):                # frosted fern beds (encounters)
        m.blob(x0 + w / 2.0, y0 + h / 2.0, w / 2.0, h / 2.0, 't', seed=x0 + y0, rough=0.7, only='.')
    # terraces: the aurora clearing (N) and the Frost Loom shelf (NE) stand one level up
    E = []
    oy = [y for y in range(m.H) if m.cls[y, 24] == 'o' or m.cls[y, 25] == 'o']
    LOG = (min(oy) - 1, max(oy) + 1)                                          # the fallen giant spans the ravine at x 24-25
    for y in range(LOG[0], LOG[1] + 1): m.cls[y, 24] = m.cls[y, 25] = 'D'
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
    E = seat(m, E[:-2], on='.dt') + E[-2:] + [item((26, 33), 'ICESTONE')]   # the islet prize stays put (slide_puzzle)
    for x, y in E[-2]['at'], E[-1]['at']:
        m.cls[y, x] = 'd'; m.taken[y, x] = True
    for e in E:
        if e['type'] == 'sign': signboard(m, e)
    for x, y in pegs:
        if m.free(x, y, 1, 1, on='.dt'): m.tile(4847, x, y, 1)
    if m.free(1, 34, 7, 7, on='.tT'):                                      # the trapper's lodge (carchagui chalet, rimport.py)
        dd = m.stamp('ch_chalet_b', 1, 34, None, None); dx, dy = 1 + STAMPS['ch_chalet_b']['door'][0], 34 + STAMPS['ch_chalet_b']['door'][1]
        for yy in range(31, 42):
            for xx in range(0, 10):
                if m.cls[yy, xx] == 'T': m.cls[yy, xx] = '.'               # a clearing round it
        doorstep(m, (dx, dy)); m.cls[dy, dx] = 'B'
        E.append(sign((dx, dy), 'Lodge door', "The trapper's lodge. Fairy lights along the eaves, a note on the door:\n\"Out on the line. Kettle's by the fire. Sit.\""))
    else: print('  (rimewood: no room for the lodge)')
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
    for y in range(LOG[0], LOG[1] + 1):                                      # the fallen giant: an ice-glazed log bridge
        nm = 'fw_log_n' if y == LOG[0] else 'fw_log_s' if y == LOG[1] else 'fw_log_m'
        L_ = STAMPS[nm]['layers'][1][0]
        m.L[1, y, 24], m.L[1, y, 25] = L_[0], L_[1]; m.L[2, y, 24] = m.L[2, y, 25] = 0
    ice(m)
    pond = [tuple(c[::-1]) for c in np.argwhere(m.cls == 'p')]
    for x, y in slide_puzzle(m, pond, ISLET, (26, 33), seed=11):                # ice-block stoppers
        m.L[1, y, x] = 10371 if (x + y) % 3 else 10551
    m.L[2, 0:4, 22:30][m.L[2, 0:4, 22:30] == 0] = 0
    rime_silk(m, ((6, 8), (12, 20), (30, 30), (40, 20), (20, 44), (34, 50)))
    m.scatter(8, seed=6)
    dress_ice(m, 0.25, seed=562); reed_beds(m, 45, seed=562); drifts(m, 0.08, seed=562)
    if prev: m.preview(prev, 0.5)
    m.write(562, head(562, 'The Rimewood', biome='forest', bgm='Natural Park',
                      metadata={'Outdoor': True, 'ShowArea': True, 'MapPosition': [0, 7, 20], 'BattleBack': 'snow', 'Weather': ['Snow', 30]},
                      tone=[-10, -4, 14, 16], fog={'name': 'prismfall_spores', 'opacity': 30, 'blend': 1, 'zoom': 100, 'sx': 1, 'sy': 1},
                      connections=[{'dir': 'N', 'offset': 12, 'to': 561, 'to_offset': 10}],
                      _file='562_rimewood.yaml'), '# The Rimewood (562). WRITTEN BY layouts/rimewood.py - edit that script.\n')
    return m


DIRS4 = ((1, 0), (-1, 0), (0, 1), (0, -1))


def slide_solve(ice, land, start, goal):
    """Essentials' ice: step onto ice and you keep going until the next cell is blocked (you stop on the ice) or is
    not ice (you step onto it and stop).  ice / land: sets of cells; anything else blocks (rocks, trees, the item).
    BFS over stop positions from every `start` land cell; returns (fewest slides to any goal cell, parent map)."""
    from collections import deque

    def slide(p, d):
        x, y = p
        while True:
            n = (x + d[0], y + d[1])
            if n in ice: x, y = n; continue
            if n in land: return n
            return (x, y) if (x, y) != p else None

    best = {}; q = deque()
    for st in start:
        best[st] = (0, None); q.append(st)
    while q:
        p = q.popleft()
        k = best[p][0]
        for d in DIRS4:
            n = (p[0] + d[0], p[1] + d[1])
            if p in land and n not in ice: continue            # on land you walk; only a step onto ice is a slide
            r = slide(p, d)
            if r is None or r in best: continue
            if r in land and r not in goal and r not in start: continue   # stepped onto unrelated land: walking from there
            best[r] = (k + 1, p); q.append(r)
    g = [best[c][0] for c in goal if c in best]
    return (min(g) if g else None), best


def slide_puzzle(m, cells, islet, item_at, n_rocks=(6, 9), tries=4000, seed=7):
    """Seed-searched stopper layout for a frozen pond: the islet (with the item) must take >= 4 slides from the shore,
    and you must be able to slide back off it.  Returns the rocks (cells that get an ice block)."""
    rng = random.Random(seed)
    cells = set(cells); isl = set(islet) - {item_at}
    land_out = set()
    for (x, y) in cells:
        for d in DIRS4:
            n = (x + d[0], y + d[1])
            if n not in cells and n not in islet and m.inb(*n) and m.cls[n[1], n[0]] in '.dt' and not m.taken[n[1], n[0]]: land_out.add(n)
    inner = [c for c in cells if all((c[0] + dx, c[1] + dy) in cells for dx in (-1, 0, 1) for dy in (-1, 0, 1))]
    ring = [c for c in cells if c not in islet and min(abs(c[0] - a) + abs(c[1] - b) for a, b in islet) <= 2]
    best = None
    for _ in range(tries):
        rocks = set(rng.sample(ring, min(len(ring), rng.randint(3, 6)))) | set(rng.sample(inner, rng.randint(*n_rocks)))
        ice = cells - rocks - set(islet)
        k, _p = slide_solve(ice, land_out | isl, land_out, isl)
        if k is None or k < 4: continue
        back, _q = slide_solve(ice, land_out | isl, isl, land_out)
        if back is None: continue
        score = k * 10 - len(rocks)
        if best is None or score > best[0]: best = (score, rocks, k)
        if k >= 6: break
    if best is None: raise SystemExit('slide_puzzle: no solvable layout')
    print('  pond puzzle: %d stoppers, islet in %d slides (shore cells %d)' % (len(best[1]), best[2], len(land_out)))
    return best[1]


def ice_floor(m, cls):
    for y, x in np.argwhere(m.cls == cls):
        m.L[0, y, x] = ice_at(x, y); m.L[1, y, x] = 0


# =================================================================================================== 563 Rimewood Glade
def glade(prev=None):
    W, H = 34, 30
    m = snowmap(W, H, 563)
    m.cls[:, :] = 'T'
    m.blob(16.5, 16, 13.5, 12.0, '.', seed=2, only='T', rough=0.9)
    m.lane([(0, 15), (6, 15), (8, 21), (14, 25), (24, 25), (28, 21)], 'd', 2.0, seed=3, only='.T')
    m.rect(0, 14, 3, 3, 'd', only='.T')
    m.blob(19, 14, 8.0, 5.0, 'i', seed=4, only='.', rough=0.55)                # the frozen pond (slide puzzle)
    for y in range(0, 6):                                                   # the Silk-fall pours from the ridge at x 14-19
        for x in list(range(9, 17)) + list(range(23, 29)): m.ht[y, x] = 1
    for y in range(0, 9):
        for x in range(17, 23): m.cls[y, x] = 'f'
    m.rect(2, 22, 10, 6, 't', only='.')
    m.blob(27, 10, 3.5, 2.2, 't', seed=8, only='.', rough=0.6); m.blob(7, 9, 2.5, 2.0, 'p', seed=9, only='.T', rough=0.3)   # break the symmetry
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
    m.scatter(14, seed=12)
    drifts(m, 0.14, seed=564)
    if prev: m.preview(prev, 0.5)
    m.write(563, head(563, 'Rimewood Glade', biome='forest', parent=562, bgm='Natural Park',
                      metadata={'Outdoor': True, 'ShowArea': True, 'MapPosition': [0, 8, 20], 'BattleBack': 'snow', 'Weather': ['Snow', 20]},
                      tone=[-6, -2, 16, 12], _file='563_rimewood_glade.yaml'),
            '# Rimewood Glade (563). WRITTEN BY layouts/rimewood.py - edit that script.\n')
    return m


# =================================================================================================== 561 Gullcry Cliffs
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
        elif e.get('trainer') == ['FISHERMAN', 'Kjell']: e['at'] = [13, 20]; e['dir'] = 'right'      # (20,16) got boxed in by the hut
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
        if vnoise(x, y, 7, 3.0) > 0.55 and m.L[1, y, x] == 0: m.L[1, y, x] = ice_at(x, y)
    m.scatter(10, seed=7)
    if prev: m.preview(prev, 0.5)
    h = head(561, 'Gullcry Cliffs', biome='route', display_name='Gullcry Cliffs', bgm='Route 3',
             metadata=old['metadata'], tone=[-10, -6, 6, 20], walk_from=[[5, 38]],
             connections=[{'dir': 'N', 'offset': 12, 'to': 160, 'to_offset': 22}, {'dir': 'S', 'offset': 10, 'to': 562, 'to_offset': 12}],
             _file='561_route6.yaml')
    m.write(561, h, '# Gullcry Cliffs (561). WRITTEN BY layouts/rimewood.py - edit that script.\n')
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
