#!/usr/bin/env python3
"""Learn example-based tiling tables from the Tectonic reference maps (safe parser).
  tlearn.py <name> <layer> <ids...>   -> data/learned/t_<name>.json
For each cell whose tile on <layer> is in the id set: key = raw 8-neighbour membership bits (off-map = member),
value = Counter of the tile. Also records the majority tile found on the other two layers (for stacks)."""
import sys, os, json, glob
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rmarshal as M, probe as P
TD = '/home/claude/ref/art/tectonic/Data'
NB = [(0, -1, 1), (1, -1, 2), (1, 0, 4), (1, 1, 8), (0, 1, 16), (-1, 1, 32), (-1, 0, 64), (-1, -1, 128)]


def learn(layer, ids, tileset=24):
    ids = set(ids)
    tab = defaultdict(Counter); other = defaultdict(lambda: defaultdict(Counter))
    for f in sorted(glob.glob(TD + '/Map[0-9]*.rxdata')):
        m = M.load_file(f)
        if m.tileset_id != tileset:
            continue
        d = m.data.data; H, W = m.height, m.width
        mem = lambda x, y: True if not (0 <= x < W and 0 <= y < H) else int(d[layer, y, x]) in ids
        for y in range(H):
            for x in range(W):
                t = int(d[layer, y, x])
                if t not in ids:
                    continue
                b = 0
                for dx, dy, bit in NB:
                    if mem(x + dx, y + dy): b |= bit
                tab[b][t] += 1
                for z in range(3):
                    if z != layer:
                        other[b][z][int(d[z, y, x])] += 1
    return tab, other


def main():
    name, layer = sys.argv[1], int(sys.argv[2])
    ids = P.parse_ids(sys.argv[3:])
    tab, other = learn(layer, ids)
    out = {'name': name, 'layer': layer, 'ids': sorted(set(ids)),
           'table': {str(b): dict(c.most_common(4)) for b, c in tab.items()},
           'other': {str(b): {str(z): dict(c.most_common(3)) for z, c in o.items()} for b, o in other.items()}}
    json.dump(out, open(os.path.join(P.R.HERE, 'data', 'learned', 't_%s.json' % name), 'w'))
    tot = Counter()
    for c in tab.values(): tot.update(c)
    print(name, 'keys', len(tab), 'cells', sum(tot.values()), 'top', tot.most_common(12))


if __name__ == '__main__':
    main()
