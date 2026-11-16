#!/usr/bin/env python3
"""Layout script for Saltmere (140) on the Tectonic tileset (palette `tectonic`): rewrites the map / heights /
stamps blocks of specs/140_saltmere.yaml (events are kept and edited in the spec).
Three levels: the upper town (Playhouse plaza), a middle terrace (services and houses) and the harbour quay,
separated by wobbling cliff lines with stairways; a lighthouse headland closes the lagoon to the east."""
import os, math, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import yaml
from terrain import vnoise
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 64, 58
STAIRS_UP = [(30, 34)]                    # x ranges (inclusive) kept flat for stairways, upper <-> middle
STAIRS_LOW = [(19, 23), (41, 45)]         # middle <-> quay


def flat(x, ranges, pad=2):
    return any(a - pad <= x <= b + pad for a, b in ranges)


def y_upper(x):      # first row of the middle terrace
    if flat(x, STAIRS_UP): return 25
    return 25 + int(round(1.6 * math.sin(x / 9.0 + 0.6) + 2.0 * (vnoise(x, 0, 11, 8.0) - 0.5)))


def y_lower(x):      # first row of the quay level
    if flat(x, STAIRS_LOW): return 39
    return 39 + int(round(1.4 * math.sin(x / 11.0 + 2.0) + 2.0 * (vnoise(x, 0, 23, 9.0) - 0.5)))


def shore(x):        # first water row
    if x < 6: return 48 + int(round(3 * (1 - x / 6.0)))       # west cove
    return 49


def height(x, y):
    """-1 water, 0 quay, 1 middle terrace, 2 upper town."""
    hx, hy = 58.0, 41.0                                          # lighthouse headland (level 1), an oval into the sea
    if y < y_upper(x): return 2
    if ((x - hx) / 6.5) ** 2 + ((y - hy) / 13.0) ** 2 <= 1.0 + 0.3 * (vnoise(x, y, 5, 4.0) - 0.5):
        return 1
    if y < y_lower(x): return 1
    if ((x - 44.0) / 9.5) ** 2 + ((y - 55.5) / 1.7) ** 2 <= 1.0 + 0.3 * (vnoise(x, y, 6, 3.0) - 0.5) and x < 53:
        return 1                                                 # the breakwater: a rock arm closing the lagoon
    if x >= 51: return -1
    if y < shore(x): return 0
    return -1


ht = [[height(x, y) for x in range(W)] for y in range(H)]
g = [['.' if ht[y][x] >= 0 else '~' for x in range(W)] for y in range(H)]


def rect(x0, y0, w, h, c, only=None):
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            if 0 <= x < W and 0 <= y < H and (only is None or g[y][x] in only):
                g[y][x] = c


def blob(cx, cy, rx, ry, c, seed, only='.', level=None):
    for y in range(int(cy - ry - 2), int(cy + ry + 3)):
        for x in range(int(cx - rx - 2), int(cx + rx + 3)):
            if not (0 <= x < W and 0 <= y < H) or g[y][x] not in only:
                continue
            if level is not None and ht[y][x] != level:
                continue
            if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1.0 + 0.5 * (vnoise(x, y, seed, 3.0) - 0.5):
                g[y][x] = c


def path(points, width, c, seed, only='.'):
    """Curving path through way-points; the width breathes between `width` and width+1."""
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        n = int(max(abs(x1 - x0), abs(y1 - y0)) * 2) + 1
        for i in range(n + 1):
            t = i / n
            x = x0 + (x1 - x0) * t; y = y0 + (y1 - y0) * t
            w = width + (1 if vnoise(x, y, seed, 4.0) > 0.55 else 0)
            rect(int(round(x - w / 2.0)), int(round(y - w / 2.0)), w, w, c, only)


# ------------------------------------------------------------------ cliffs from the height map
def lower_near(x, y):
    h = ht[y][x]
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            xx, yy = x + dx, y + dy
            if 0 <= xx < W and 0 <= yy < H and max(ht[yy][xx], 0) < h:
                return True
    return False


rim = [[ht[y][x] >= 1 and lower_near(x, y) for x in range(W)] for y in range(H)]
cl = [[rim[y][x] for x in range(W)] for y in range(H)]
for y in range(H):
    for x in range(W):
        if rim[y][x] and y + 1 < H and max(ht[y + 1][x], 0) < ht[y][x]:      # south-facing: a 3-row stacked face
            for k in (1, 2):
                if y + k < H and ht[y + k][x] >= 0:
                    cl[y + k][x] = True

# ------------------------------------------------------------------ paving and paths (before cliffs are stamped in)
blob(32, 21, 10.5, 3.6, 'c', 3, level=2); rect(28, 17, 9, 3, 'c')         # Playhouse forecourt (cream flagstones)
path([(45, 0), (46, 6), (44, 13), (41, 19)], 3, 'c', 4)                   # north road from Route 4, round the Playhouse
path([(22, 21), (17, 19), (13, 18)], 2, 'o', 5)                           # stepping stones to Saltwife's garden
path([(13, 18), (9, 20), (6, 19)], 2, 'o', 15)
path([(42, 20), (48, 18), (52, 18)], 3, 'c', 6)                           # lane to the Pageant Hall
rect(30, 22, 5, 3, 'c')                                                   # head of the upper stairs
path([(32, 28), (32, 33)], 4, 'b', 7)                                     # middle terrace: brick high street
path([(0, 33), (8, 34), (14, 33), (21, 35), (32, 34), (43, 35), (50, 33)], 3, 'b', 8)
path([(21, 35), (21, 38)], 4, 'b', 9); path([(43, 35), (43, 38)], 4, 'b', 10)
path([(50, 33), (53, 36), (54, 43), (56, 47), (59, 48)], 2, 'o', 12)       # stones round to the lighthouse door
for y in range(H):                                                        # the quay: brick from the cliff foot to the water
    for x in range(6, 51):
        if ht[y][x] == 0 and y >= 43:
            g[y][x] = 'b'
path([(21, 41), (21, 44)], 4, 'b', 13); path([(43, 41), (43, 44)], 4, 'b', 14)
rect(2, 28, 6, 3, 'p'); rect(2, 36, 5, 2, 'p'); rect(9, 36, 4, 2, 'p')    # salt pans on the west terrace
# ------------------------------------------------------------------ water structures
rect(16, 49, 3, 7, '=', '~'); rect(28, 49, 3, 4, '=', '~'); rect(48, 49, 2, 4, '=', '~')
# ------------------------------------------------------------------ fenced yards
rect(8, 10, 9, 1, 'f', '.'); rect(8, 10, 1, 8, 'f', '.'); rect(16, 10, 1, 5, 'f', '.')      # Saltwife's garden
rect(47, 9, 11, 1, 'f', '.'); rect(57, 9, 1, 8, 'f', '.')                                     # Pageant Hall yard
rect(5, 26, 1, 5, 'f', '.'); rect(40, 27, 5, 1, 'f', '.')
rect(53, 52, 8, 1, 'f', '.')
# ------------------------------------------------------------------ greenery (mixed clumps, never a wall)
blob(4, 5, 5, 5, 'T', 21, level=2); blob(59, 4, 5, 4.5, 'T', 22, level=2); blob(52, 3, 3, 2.5, 'T', 23, level=2)
blob(20, 12, 3, 3.5, 'T', 24, level=2); blob(2, 16, 3, 4, 'T', 25, level=2); blob(61, 17, 3, 5, 'T', 26, level=2)
blob(42, 9, 2.5, 3, 'T', 32, level=2); blob(10, 22, 4, 2, 'T', 33, level=2); blob(55, 22, 4, 2, 'T', 34, level=2)
blob(27, 30, 2.5, 2, 'T', 28, level=1); blob(38, 37, 3, 1.5, 'T', 35, level=1); blob(4, 32, 2, 2, 'T', 36, level=1)
blob(61, 33, 3, 4, 'T', 29, level=1); blob(55, 47, 2.5, 3, 'T', 31, level=1); blob(15, 37, 3, 1.5, 'T', 37, level=1)
blob(30, 12, 0.1, 0.1, 'T', 30, level=0)
blob(8, 8, 3, 2, 'T', 40, level=2); blob(23, 20, 2.5, 1.6, 'T', 41, level=2); blob(46, 22, 3, 1.6, 'T', 42, level=2)
blob(38, 14, 1.6, 2.5, 'T', 43, level=2); blob(60, 11, 3.5, 3, 'T', 44, level=2); blob(18, 31, 1.6, 2, 'T', 45, level=1)
blob(44, 31, 1.5, 2.5, 'T', 46, level=1); blob(57, 30, 1.5, 2, 'T', 47, level=1); blob(2, 24, 2.5, 1.5, 'T', 48, level=2)
blob(33, 37, 3, 1.4, 'T', 49, level=1); blob(49, 38, 2, 1.5, 'T', 50, level=1); blob(60, 44, 2.5, 3, 'T', 51, level=1)
path([(15, 9), (18, 10), (21, 10)], 2, 'o', 52); path([(21, 10), (23, 15), (24, 19)], 2, 'o', 53)   # lanes to the townhouses
for x in range(W):                                                        # promenade railings along both cliff tops
    for yb, rng_ in ((y_upper(x), STAIRS_UP), (y_lower(x), STAIRS_LOW)):
        y = yb - 2
        if not flat(x, rng_, 0) and 0 <= y < H and g[y][x] == '.' and not cl[y][x] and vnoise(x, yb, 77, 5.0) > 0.3:
            g[y][x] = 'f'
for y in range(H):
    for x in range(W):
        if cl[y][x]:
            g[y][x] = 'C'

stamps = [
    ('t_hall', 25, 2, 'SM_GYM', "Playhouse door", (7, 15)),
    ('t_theatre', 48, 11, 'SM_PAGEANT', "Pageant Hall door", (3, 5)),
    ('t_house_red', 10, 12, 'SM_HOUSE1', "Saltwife's House door", (2, 4)),
    ('t_pokecenter', 9, 28, 'SM_PC', "Poke Center door", (2, 4)),
    ('t_mart', 46, 29, 'SM_MART', "Mart door", (1, 3)),
    ('t_lodge', 37, 28, 'SM_HARBOUR', "Harbour Office door", (1, 5)),
    ('t_townhouse', 13, 3, None, None, None), ('t_townhouse', 19, 4, None, None, None),
    ('t_house_orange', 41, 2, None, None, None), ('t_house_blue', 4, 20, None, None, None),
    ('t_house_blue', 15, 27, None, None, None), ('t_house_blue2', 51, 27, None, None, None),
    ('t_stall', 22, 28, None, None, None), ('t_shop_purple', 25, 41, None, None, None),
    ('t_warehouse', 7, 42, None, None, None),
    ('t_lighthouse', 57, 29, None, None, None),
    ('t_ship', 33, 49, None, None, None),
    ('t_stairs', 31, 24, None, None, None), ('t_stairs', 20, 38, None, None, None), ('t_stairs', 42, 38, None, None, None),
    ('t_cont_green', 17, 43, None, None, None), ('t_cont_brown', 31, 43, None, None, None),
    ('t_cont_long', 33, 46, None, None, None), ('t_crate_pair', 21, 46, None, None, None),
    ('t_crate_a', 46, 43, None, None, None), ('t_crates_b', 38, 43, None, None, None),
    ('t_bench', 24, 22, None, None, None), ('t_bench', 39, 22, None, None, None), ('t_table', 50, 36, None, None, None),
    ('t_rock', 3, 44, None, None, None), ('t_rock', 25, 36, None, None, None),
    ('t_lamp', 28, 19, None, None, None), ('t_lamp', 36, 19, None, None, None), ('t_lamp', 29, 31, None, None, None),
    ('t_lamp', 35, 31, None, None, None), ('t_lamp', 12, 34, None, None, None), ('t_lamp', 48, 35, None, None, None),
    ('t_lamp', 24, 45, None, None, None), ('t_lamp', 45, 46, None, None, None), ('t_lamp', 47, 7, None, None, None),
    ('t_barrel', 15, 46, None, None, None), ('t_barrel2', 16, 46, None, None, None), ('t_barrel', 33, 46, None, None, None),
    ('t_barrel2', 49, 45, None, None, None), ('t_barrel', 21, 33, None, None, None), ('t_trellis', 9, 15, None, None, None),
]
slist = []
for name, x, y, link, dname, door in stamps:
    d = {'stamp': name, 'at': [x, y]}
    if link:
        d.update({'link': link, 'name': dname, 'door': list(door)})
    slist.append(d)

# sea rocks (layer 2 over water), seeded
import random
rng = random.Random(140)
tiles = []
taken = set()
for _ in range(400):
    x, y = rng.randrange(1, W - 2), rng.randrange(50, H - 2)
    if any(g[yy][xx] != '~' for xx in range(x - 1, x + 3) for yy in range(y - 1, y + 3)): continue
    if any((xx, yy) in taken for xx in range(x - 2, x + 4) for yy in range(y - 2, y + 4)): continue
    if 31 <= x <= 46 and 48 <= y <= 56: continue                       # the moored ship
    if rng.random() < 0.3:
        for dx, dy, t in ((0, 0, 1552), (1, 0, 1553), (0, 1, 1560), (1, 1, 1561)): tiles.append({'tile': t, 'at': [x + dx, y + dy], 'layer': 2})
    else:
        a = rng.choice([(1554, 1562), (1555, 1563)])
        tiles.append({'tile': a[0], 'at': [x, y], 'layer': 2}); tiles.append({'tile': a[1], 'at': [x, y + 1], 'layer': 2})
    taken.add((x, y))
    if len(taken) >= 26: break

rows = [''.join(r) for r in g]
hrows = [''.join(str(max(h, 0)) for h in r) for r in ht]
p = os.path.join(HERE, 'specs', '140_saltmere.yaml')
s = open(p).read()
ev = s[s.index('\nevents:\n'):]
head = '''# Saltmere (map 140): Elowen's free port; Pell Playhouse (Gym 2). Story: story/04_ACT_I.md Chapter 3.
# ART PILOT on the Tectonic tileset (palette `tectonic`). Map, heights and stamps are WRITTEN BY layouts/saltmere.py;
# edit that script, run it, then build.py. Events below are hand-edited.
id: 140
name: Saltmere
palette: tectonic
bgm: Lerucean Town
parent: 0
rubric: true
tone: [10, 4, -14, 0]                 # warm lantern-gold cast (ART_DIRECTION rubric 10)
metadata: {Outdoor: true, ShowArea: true, MapPosition: [0, 10, 25], BattleBack: field, Weather: [Rain, 10]}
connections:
  - {dir: N, offset: 44, to: 541, to_offset: 13}
  - {dir: W, offset: 32, to: 560, to_offset: 12}
'''
body = 'map: |\n' + '\n'.join('  ' + r for r in rows) + '\nheights: |\n' + '\n'.join('  ' + r for r in hrows) + '\n'
body += yaml.safe_dump({'stamps': slist, 'tiles': tiles}, sort_keys=False, default_flow_style=None, width=150)
open(p, 'w').write(head + body + ev.lstrip('\n').join(['', '']) if False else head + body + ev[1:])
print('\n'.join(rows))
