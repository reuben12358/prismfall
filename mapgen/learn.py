#!/usr/bin/env python3
"""Learn 'blob terrain' tiling rules from reference maps (safe parser).
For a terrain class (a set of layer-0 tile ids), records for every cell of that class:
  key = (x % P, y % P, 8-neighbour membership bits)  ->  Counter(tile id)
plus overlays written on layers 1/2 in the cells around the class.
usage: python3 -I learn.py <tileset_id> <class_name> <period> <ids...> [--out file.json] [--phase]
"""
import sys, os, json
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rmarshal as M
import probe as P

REF = P.REF
NB = [(0, -1, 1), (1, -1, 2), (1, 0, 4), (1, 1, 8), (0, 1, 16), (-1, 1, 32), (-1, 0, 64), (-1, -1, 128)]


def maps_for(tsid):
    mi = json.load(open(os.path.join(P.R.HERE, 'data', 'maps_summary.json')))
    for k, v in mi.items():
        if v['tileset_id'] == tsid:
            yield int(k), M.load_file(os.path.join(REF, 'Data', 'Map%03d.rxdata' % int(k)))


def learn(tsid, ids, period, layer=0, phase_of=None):
    ids = set(ids)
    table = defaultdict(Counter)
    inner = defaultdict(Counter)     # key of a class cell -> (layer, tile) on layers 1/2 (0 = none)
    overlay = defaultdict(Counter)   # key=(x%P,y%P,bits) of a NON-class cell -> (layer, tile) of layers 1/2
    phase = defaultdict(Counter)
    for mid, m in maps_for(tsid):
        d = m.data.data
        H, W = m.height, m.width
        inc = lambda x, y: True if not (0 <= x < W and 0 <= y < H) else int(d[layer, y, x]) in ids
        for y in range(H):
            for x in range(W):
                t = int(d[layer, y, x])
                bits = 0
                for dx, dy, b in NB:
                    if inc(x + dx, y + dy):
                        bits |= b
                if phase_of:
                    if t in ids:
                        px, py = phase_of[t]
                    else:  # overlay cell: phase from the class cell below (else right/left)
                        below = int(d[layer, y + 1, x]) if y + 1 < H else 0
                        px, py = phase_of.get(below, (x % period, (y + 1) % period))
                        py = (py + 1) % period
                else:
                    px, py = x % period, y % period
                if t in ids:
                    table[(px, py, bits)][t] += 1
                    for z in (1, 2):
                        inner[(px, py, bits)][(z, int(d[z, y, x]))] += 1
                    phase[t][(x % period, y % period)] += 1
                elif bits:
                    for z in (1, 2):
                        u = int(d[z, y, x])
                        if u:
                            overlay[(px, py, bits)][(z, u)] += 1
    return table, overlay, phase, inner


def main():
    a = sys.argv[1:]
    tsid, name, period = int(a[0]), a[1], int(a[2])
    rest = [x for x in a[3:] if x[0].isdigit()]
    ids = P.parse_ids(rest[:rest.index('|')] if '|' in rest else rest)
    phase_of = None
    if '--treephase' in a:
        phase_of = {808: (0, 0), 809: (1, 0), 810: (0, 0), 811: (1, 0), 800: (0, 1), 801: (1, 1), 802: (0, 1),
                    803: (1, 1), 818: (0, 1), 819: (1, 1), 816: (0, 1), 817: (1, 1)}
        ids = [i for i in ids if i in phase_of]
    table, overlay, phase, inner = learn(tsid, ids, period, phase_of=phase_of)
    if '--phase' in a:
        for t, c in sorted(phase.items()):
            print(t, dict(c))
    print('%s: %d keys' % (name, len(table)))
    out = {'name': name, 'period': period, 'ids': sorted(ids),
           'table': {'%d,%d,%d' % k: dict(v.most_common()) for k, v in table.items()},
           'inner': {'%d,%d,%d' % k: {'%d:%d' % zt: n for zt, n in v.most_common()} for k, v in inner.items()},
           'overlay': {'%d,%d,%d' % k: {'%d:%d' % zt: n for zt, n in v.most_common()} for k, v in overlay.items()}}
    if '--out' in a:
        json.dump(out, open(a[a.index('--out') + 1], 'w'), indent=0)
        print('wrote', a[a.index('--out') + 1])


if __name__ == '__main__':
    main()
