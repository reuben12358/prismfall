#!/usr/bin/env python3
"""check_b3.py <map id> [x,y start] - builder 3's post-build check on the written rxdata: flood-fill on foot from the
start cell (default: the first transfer event, else the bottom-most walkable cell) using build.py's passability rule,
then list events that are not reachable (standing on, or next to, a reached cell) and count stranded walkable tiles."""
import os, sys
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, HERE)
import numpy as np
import rmarshal as M, render as R
from build import cell_passable


def check(mid, start=None):
    m = M.load_file(os.path.join(os.path.dirname(HERE), 'maps_out', 'Data', 'Map%03d.rxdata' % mid))
    ts = R.tilesets()[m.tileset_id]; lay = m.data.data; H, W = m.height, m.width
    solid = {(e.x, e.y) for e in m.events.values() if e.pages[0].graphic.character_name and not e.pages[0].through}
    ok = np.array([[cell_passable(lay, ts, x, y) and (x, y) not in solid for x in range(W)] for y in range(H)])
    if start is None:
        tr = [(e.x, e.y) for e in m.events.values() if any(c.code == 201 for p in e.pages for c in p.list)]
        start = tr[0] if tr else next((x, y) for y in range(H - 1, -1, -1) for x in range(W) if ok[y, x])
    seen = np.zeros_like(ok); st = [(start[0] + dx, start[1] + dy) for dx, dy in ((0, 0), (0, 1), (0, -1), (1, 0), (-1, 0))]
    while st:
        x, y = st.pop()
        if not (0 <= x < W and 0 <= y < H) or seen[y, x] or not ok[y, x]: continue
        seen[y, x] = True; st += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    bad = []
    for e in m.events.values():
        if not any(c.code != 0 for p in e.pages for c in p.list): continue
        if e.pages[0].trigger in (3, 4) and e.x == 0 and e.y == 0: continue          # atmosphere event
        if not any(0 <= e.x + dx < W and 0 <= e.y + dy < H and seen[e.y + dy, e.x + dx] for dx, dy in ((0, 0), (0, 1), (0, -1), (1, 0), (-1, 0))):
            bad.append('%s (%d,%d)' % (e.name, e.x, e.y))
    stranded = int((ok & ~seen).sum())
    print('map %d: start %s, reached %d of %d walkable tiles (%d stranded, %.0f%%), events %d, unreachable: %s'
          % (mid, tuple(start), int(seen.sum()), int(ok.sum()), stranded, 100.0 * stranded / max(1, ok.sum()), len(m.events), bad or 'none'))
    if '--map' in sys.argv:
        for y in range(H): print(''.join('#' if not ok[y, x] else ('.' if seen[y, x] else '!') for x in range(W)))
    return not bad


if __name__ == '__main__':
    a = [v for v in sys.argv[1:] if not v.startswith('--')]
    good = True
    for v in a:
        if ',' in v: continue
        i = a.index(v); st = tuple(int(q) for q in a[i + 1].split(',')) if i + 1 < len(a) and ',' in a[i + 1] else None
        good &= check(int(v), st)
    sys.exit(0 if good else 1)
