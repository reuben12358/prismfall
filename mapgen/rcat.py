#!/usr/bin/env python3
"""rcat.py - catalogue the objects of reference maps (connected components of layer 2/3 tiles), as a numbered contact
sheet, so stamps can be picked by eye and named in rstamps.yaml (MAPGEN 2h).  Read-only on the games.

    python3 -I rcat.py <game> <map[,map...]> out.png [--drop 600-618,1504-1530] [--min 2] [--keep0]
Prints `#n map x y w h` per component; the sheet shows the same numbers."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw
import rref as RR


def ids(spec):
    out = set()
    for part in spec.split(','):
        if not part: continue
        if '-' in part: a, b = part.split('-'); out |= set(range(int(a), int(b) + 1))
        else: out.add(int(part))
    return out


def components(L, drop, minsz=2):
    _, H, W = L.shape
    obj = np.zeros((H, W), bool)
    for z in (1, 2):
        obj |= (L[z] >= 384) & ~np.isin(L[z], list(drop))
    seen = np.zeros_like(obj); comps = []
    for y in range(H):
        for x in range(W):
            if obj[y, x] and not seen[y, x]:
                st = [(x, y)]; cells = []
                seen[y, x] = True
                while st:
                    cx, cy = st.pop(); cells.append((cx, cy))
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nx, ny = cx + dx, cy + dy
                        if 0 <= nx < W and 0 <= ny < H and obj[ny, nx] and not seen[ny, nx]:
                            seen[ny, nx] = True; st.append((nx, ny))
                if len(cells) >= minsz:
                    xs = [c[0] for c in cells]; ys = [c[1] for c in cells]
                    comps.append((min(xs), min(ys), max(xs) - min(xs) + 1, max(ys) - min(ys) + 1, len(cells)))
    return comps


def main():
    a = sys.argv[1:]
    game, maps, out = a[0], [int(m) for m in a[1].split(',')], a[2]
    drop = ids(a[a.index('--drop') + 1]) if '--drop' in a else set()
    minsz = int(a[a.index('--min') + 1]) if '--min' in a else 2
    tiles = []; n = 0
    for mid in maps:
        L, m = RR.load(game, mid); tc = RR.tilecache(game, m.tileset_id)
        for (x, y, w, h, k) in sorted(components(L, drop, minsz), key=lambda c: (c[1], c[0])):
            n += 1
            im = RR.render_layers(L, tc, 1.0, (x, y, w, h))
            sc = 0.5 if max(w, h) <= 6 else 0.34
            tiles.append(('%d' % n, im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))))))
            print('#%d map %d at %d %d size %d %d' % (n, mid, x, y, w, h))
    rows = []; row = []; wsum = 0
    for t in tiles:
        if wsum + t[1].width > 1500: rows.append(row); row = []; wsum = 0
        row.append(t); wsum += t[1].width + 6
    rows.append(row)
    Ht = sum(max(i.height for _, i in r) + 14 for r in rows if r)
    sh = Image.new('RGB', (1500, Ht), (40, 40, 50)); d = ImageDraw.Draw(sh); y = 0
    for r in rows:
        if not r: continue
        x = 0
        for nm, i in r:
            sh.paste(i.convert('RGB'), (x, y + 12)); d.text((x + 1, y), nm, fill=(255, 255, 0)); x += i.width + 6
        y += max(i.height for _, i in r) + 14
    sh.save(out); print(out, sh.size)


if __name__ == '__main__':
    main()
