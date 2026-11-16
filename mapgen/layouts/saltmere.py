#!/usr/bin/env python3
"""Layout script for Saltmere (140): writes the `map:` ASCII and decoration lists into specs/140_saltmere.yaml
(between the LAYOUT-BEGIN / LAYOUT-END markers). Art-direction pilot: cliff-top upper town around the Pell
Playhouse plaza, a stepped cliff with two stairways, and a harbour lower town with quay, piers, moored boats,
salt pans, a fish market and a lighthouse on the breakwater."""
import os
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 40, 34
g = [['.'] * W for _ in range(H)]


def rect(x0, y0, w, h, c):
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            if 0 <= x < W and 0 <= y < H:
                g[y][x] = c


# ---------------------------------------------------------------- lower town (drawn first)
rect(0, 18, 6, 4, '_'); rect(1, 19, 2, 2, 's'); rect(4, 19, 2, 2, 's')        # salt pans in white sand
rect(0, 23, 34, 2, 'c'); rect(0, 25, 8, 1, 'c'); rect(22, 25, 12, 1, 'c')       # harbour street (W exit y 23-25)
rect(8, 25, 14, 1, '_')                                                        # quay widens by the market
rect(9, 18, 4, 5, 'c'); rect(17, 19, 2, 4, 'c'); rect(25, 18, 4, 5, 'c')       # lanes up to the stairs
rect(0, 26, 34, 2, '_')                                                        # quay
rect(0, 28, 40, 6, '~')                                                        # harbour
rect(8, 28, 3, 6, '='); rect(19, 28, 3, 5, '=')                                # piers
rect(34, 17, 6, 14, '_')                                                       # lighthouse breakwater
rect(38, 17, 2, 3, 'T'); rect(36, 17, 2, 2, 'T')
# ---------------------------------------------------------------- upper town
rect(0, 0, 40, 2, 'T'); rect(0, 0, 9, 4, 'T'); rect(28, 0, 12, 3, 'T'); rect(34, 0, 6, 6, 'T')
rect(0, 0, 3, 15, 'T'); rect(37, 0, 3, 16, 'T'); rect(3, 2, 2, 2, '.')
rect(14, 0, 6, 2, '.'); rect(15, 0, 3, 7, 'c')                                 # north gate + road (Route 4)
rect(13, 6, 16, 7, 'c'); rect(15, 13, 12, 1, 'c'); rect(12, 8, 1, 4, 'c')     # Playhouse plaza
rect(13, 6, 2, 1, '.'); rect(27, 6, 2, 1, '.'); rect(13, 12, 1, 1, '.'); rect(28, 12, 1, 1, '.')
rect(17, 12, 2, 1, '*'); rect(22, 12, 2, 1, '*'); rect(17, 8, 2, 1, '*'); rect(22, 8, 2, 1, '*')  # flowers at the fountain corners
rect(13, 11, 3, 2, '.'); rect(26, 11, 3, 2, '.'); rect(13, 7, 2, 2, '.'); rect(27, 7, 2, 2, '.')  # grass corners
rect(30, 9, 3, 2, 'c')                                                         # to the Pageant Hall
rect(4, 11, 8, 2, ':'); rect(6, 11, 2, 3, ':')                                 # garden lane
rect(3, 5, 9, 1, 'f'); rect(3, 5, 1, 6, 'f'); rect(11, 5, 1, 6, 'f')           # Saltwife's garden fence
rect(4, 13, 2, 1, '*'); rect(8, 13, 3, 1, '*'); rect(9, 8, 2, 2, '*'); rect(33, 12, 3, 2, '*'); rect(13, 4, 2, 2, '*')
rect(10, 2, 2, 2, 'T'); rect(30, 4, 2, 2, 'T')
rect(3, 14, 7, 1, 'f'); rect(12, 14, 2, 1, 'f'); rect(22, 14, 4, 1, 'f'); rect(28, 14, 9, 1, 'f')   # cliff-top rail
# ---------------------------------------------------------------- the cliff (stepped) + stairways
rect(0, 15, 14, 2, 'C'); rect(14, 16, 9, 2, 'C'); rect(23, 15, 14, 2, 'C')   # stepped cliff line
rect(10, 15, 2, 3, 'S'); rect(26, 15, 2, 3, 'S')
rect(0, 15, 3, 2, 'T'); rect(14, 15, 9, 1, '.'); rect(15, 14, 7, 2, '*')
# ---------------------------------------------------------------- building footprints
for (x, y, w, h) in [(21, 2, 7, 4), (31, 6, 5, 4), (5, 6, 5, 5), (5, 18, 5, 5), (12, 19, 4, 4), (29, 19, 6, 4),
                     (19, 18, 6, 4)]:
    rect(x, y, w, h, '#')
rows = [''.join(r) for r in g]

deco = {
    'tileblocks': [
        {'tile': 1501, 'size': [3, 4], 'at': [19, 8], 'layer': 1, 'skip': [1510, 1518]},     # plaza fountain
        {'tile': 3941, 'size': [3, 8], 'at': [35, 21], 'layer': 1},                         # lighthouse
        # The stock ship/boat art is cut at the tileset's right edge (the hulls continue off-sheet), so ships may
        # only sit flush against the map's right edge, where the missing half is off-map.
        {'tile': 4349, 'size': [3, 3], 'at': [37, 31], 'layer': 1},                         # moored ship (edge)
        {'tile': 1437, 'size': [3, 1], 'at': [14, 10], 'layer': 1},                         # plaza benches
        {'tile': 1437, 'size': [3, 1], 'at': [24, 10], 'layer': 1},
        {'tile': 1437, 'size': [3, 1], 'at': [28, 26], 'layer': 1},                         # quay bench
        {'tile': 1485, 'size': [3, 2], 'at': [0, 16], 'layer': 1},
        {'tile': 1408, 'size': [1, 3], 'at': [25, 3], 'layer': 1},
        {'tile': 1485, 'size': [3, 2], 'at': [13, 5], 'layer': 1},                          # planters
        {'tile': 1485, 'size': [3, 2], 'at': [32, 13], 'layer': 1},
        {'tile': 1408, 'size': [1, 3], 'at': [13, 7], 'layer': 1},                          # street lamps
        {'tile': 1408, 'size': [1, 3], 'at': [28, 7], 'layer': 1},
        {'tile': 1408, 'size': [1, 3], 'at': [16, 22], 'layer': 1},
        {'tile': 1408, 'size': [1, 3], 'at': [33, 22], 'layer': 1},
        {'tile': 1408, 'size': [1, 3], 'at': [7, 24], 'layer': 1},
    ],
    'tiles': [
        {'tile': 378, 'at': [20, 9], 'layer': 2}, {'tile': 380, 'at': [20, 10], 'layer': 2},  # fountain water
        {'tile': 1376, 'at': [13, 26], 'layer': 1}, {'tile': 1378, 'at': [14, 26], 'layer': 1},
        {'tile': 1379, 'at': [6, 27], 'layer': 1}, {'tile': 1380, 'at': [7, 27], 'layer': 1},
        {'tile': 1328, 'at': [13, 18], 'layer': 1}, {'tile': 1329, 'at': [23, 18], 'layer': 1},
        {'tile': 1331, 'at': [34, 13], 'layer': 1}, {'tile': 1331, 'at': [4, 9], 'layer': 1},
        {'tile': 1331, 'at': [30, 2], 'layer': 1},
        {'tile': 1331, 'at': [14, 8], 'layer': 1}, {'tile': 1331, 'at': [27, 8], 'layer': 1},
        {'tile': 1331, 'at': [14, 12], 'layer': 1}, {'tile': 1331, 'at': [27, 12], 'layer': 1},
        {'tile': 1536, 'at': [11, 26], 'layer': 1}, {'tile': 1537, 'at': [18, 27], 'layer': 1},
        {'tile': 1538, 'at': [22, 26], 'layer': 1},
        {'tile': 1536, 'at': [18, 22], 'layer': 1}, {'tile': 1537, 'at': [25, 21], 'layer': 1},
        {'tile': 1538, 'at': [25, 20], 'layer': 1}, {'tile': 1536, 'at': [3, 25], 'layer': 1},
        {'tile': 1537, 'at': [3, 27], 'layer': 1}, {'tile': 1536, 'at': [22, 27], 'layer': 1},
        {'tile': 1538, 'at': [11, 27], 'layer': 1}, {'tile': 1537, 'at': [12, 27], 'layer': 1},
        {'tile': 1376, 'at': [16, 26], 'layer': 1}, {'tile': 1377, 'at': [17, 26], 'layer': 1},
        {'tile': 1328, 'at': [3, 17], 'layer': 1}, {'tile': 1329, 'at': [33, 18], 'layer': 1},
        {'tile': 1331, 'at': [7, 4], 'layer': 1}, {'tile': 1331, 'at': [26, 7], 'layer': 1},
        {'tile': 1340, 'at': [12, 8], 'layer': 1}, {'tile': 1340, 'at': [29, 8], 'layer': 1},
        {'tile': 1341, 'at': [24, 13], 'layer': 1}, {'tile': 1341, 'at': [17, 13], 'layer': 1},
    ],
}

spec_path = os.path.join(HERE, 'specs', '140_saltmere.yaml')
s = open(spec_path).read()
a = s.index('map: |\n') + len('map: |\n'); b = s.index('stamps:')
s = s[:a] + '\n'.join('  ' + r for r in rows) + '\n' + s[b:]
import yaml
start = s.find('# LAYOUT-DECO-BEGIN'); end = s.find('# LAYOUT-DECO-END')
block = '# LAYOUT-DECO-BEGIN (written by layouts/saltmere.py)\n' + yaml.safe_dump(deco, sort_keys=False, width=140) + '# LAYOUT-DECO-END\n'
if start >= 0:
    s = s[:start] + block + s[end + len('# LAYOUT-DECO-END\n'):]
else:
    s = s.replace('events:\n', block + 'events:\n', 1)
open(spec_path, 'w').write(s)
print('\n'.join(rows))
