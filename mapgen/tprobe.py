#!/usr/bin/env python3
"""Research helper for the Tectonic reference maps (safe parser).
  tprobe.py freq <mapid...>            most common tiles per layer
  tprobe.py region <mapid> x y w h     per-layer ids
  tprobe.py sheet out.png ids...       labelled sheet from tileset 30
  tprobe.py crop <mapid> out.png x y w h [--grid]"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from collections import Counter
import rmarshal as M, render as R, probe as P
TD = '/home/claude/ref/art/tectonic/Data'
def load(i): return M.load_file('%s/Map%03d.rxdata' % (TD, int(i)))
a = sys.argv[1:]
if a[0] == 'freq':
    for z in range(3):
        c = Counter()
        for i in a[1:]:
            c.update(int(t) for t in load(i).data.data[z].reshape(-1))
        print('L%d' % z, ' '.join('%d:%d' % kv for kv in c.most_common(45)))
elif a[0] == 'region':
    m = load(a[1]); x0, y0, w, h = map(int, a[2:6])
    for z in range(3):
        print('layer', z)
        for y in range(y0, y0 + h):
            print('%3d: ' % y + ' '.join('%5d' % m.data[x, y, z] for x in range(x0, x0 + w)))
elif a[0] == 'sheet':
    P.sheet(30, a[1], P.parse_ids(a[2:]), cols=8)
elif a[0] == 'crop':
    m = load(a[1]); m.ivars['tileset_id'] = 30
    x, y, w, h = map(int, a[3:7])
    im = R.render(m, events=False, grid='--grid' in a).crop((x * 32, y * 32, (x + w) * 32, (y + h) * 32))
    im.convert('RGB').save(a[2]); print(im.size)
