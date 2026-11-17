"""Underpainting for the Juno block-in: turns flat regions into 3-4 tone volumes lit from the upper left.
This is the 'blocking in lights' step from Saint11's portrait tutorial: a starting point, cleaned by hand afterwards.
- hair: the cloud is split into puffs (Voronoi on puff centres); each puff is a sphere lit from upper-left; crevices
  between puffs get the dark tone on the lower/right puff.
- everything else: directional distance ratio (distance to the region edge toward the light vs away from it).
python3 -I underpaint.py BLOCK.spr OUT.spr"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from px4 import Sprite, outline
import numpy as np

LX, LY = -0.62, -0.78   # light comes FROM the upper left (vector pointing toward the light)

PUFFS = [(33.5, 6.5, 3.6), (40, 5, 3.6), (46.5, 5.5, 3.6), (28.5, 11.5, 3.6), (27, 18, 3.6), (28, 24.5, 3.6), (31.5, 28, 3),
         (52, 9.5, 3.6), (54.5, 16, 3.8), (54, 22.5, 3.8), (51.5, 27.5, 3.4), (47.5, 29, 2.6),
         (36, 11, 4), (44, 11, 4), (40, 17, 5), (33, 18, 4), (48, 18, 4.5), (35, 25, 3.5), (46, 25, 3.5)]

RAMPS = {  # dark -> light
    'h': ['R', 'r', 'h', 'H'],
    'y': ['o', 'o', 'y', 'Y'],
    'S': ['r', 's', 'S', 'S'],
    'W': ['v', 'w', 'W', 'W'],
    'g': ['E', 'e', 'g', 'G'],
    'G': ['e', 'g', 'G', 'G'],
    'T': ['o', 'o', 'T', 'T'],
    'b': ['d', 'd', 'b', 'B'],
    'B': ['d', 'b', 'B', 'B'],
}


def ray(mask, x, y, dx, dy, maxd=30):
    d = 0.0
    fx, fy = x + 0.5, y + 0.5
    while d < maxd:
        fx += dx * 0.5; fy += dy * 0.5; d += 0.5
        ix, iy = int(math.floor(fx)), int(math.floor(fy))
        if not (0 <= ix < mask.shape[1] and 0 <= iy < mask.shape[0]) or not mask[iy, ix]:
            return d
    return maxd


def main():
    sp = Sprite.load(sys.argv[1])
    g = sp.compose()
    H_, W_ = sp.h, sp.w
    arr = np.array(g)
    out = [row[:] for row in g]
    # ---------------- hair puffs
    hm = (arr == 'h')
    owner = -np.ones((H_, W_), int)
    for y in range(H_):
        for x in range(W_):
            if hm[y, x]:
                best, bi = 1e9, -1
                for i, (cx, cy, r) in enumerate(PUFFS):
                    dd = math.hypot(x - cx, y - cy) / r
                    if dd < best:
                        best, bi = dd, i
                owner[y, x] = bi
    for y in range(H_):
        for x in range(W_):
            if not hm[y, x]:
                continue
            cx, cy, r = PUFFS[owner[y, x]]
            nx, ny = (x - cx) / r, (y - cy) / r
            L = nx * LX + ny * LY
            # global falloff: lower and right puffs darker (the hair mass is a big sphere too)
            gx, gy = (x - 40.5) / 15, (y - 16) / 13
            G = gx * LX + gy * LY
            v = 0.55 * L + 0.55 * G
            ramp = RAMPS['h']
            if v > 0.42:
                c = ramp[3]
            elif v > -0.12:
                c = ramp[2]
            elif v > -0.6:
                c = ramp[1]
            else:
                c = ramp[0]
            # crevice: pixel whose upper-left neighbour belongs to another puff -> dark line
            for ddx, ddy in ((-1, 0), (0, -1)):
                xx, yy = x + ddx, y + ddy
                if 0 <= xx < W_ and 0 <= yy < H_ and hm[yy, xx] and owner[yy, xx] != owner[y, x]:
                    ocx, ocy, _ = PUFFS[owner[yy, xx]]
                    # only where the other puff sits in front (above-left) of this one
                    if (ocx + ocy) < (cx + cy):
                        c = ramp[1] if c in (ramp[3], ramp[2]) else ramp[0]
            out[y][x] = c
    # ---------------- other materials: directional ratio
    for base in ['y', 'S', 'W', 'g', 'G', 'T', 'b', 'B']:
        m = (arr == base)
        if not m.any():
            continue
        ramp = RAMPS[base]
        for y in range(H_):
            for x in range(W_):
                if not m[y, x]:
                    continue
                dl = ray(m, x, y, LX, LY)      # distance toward the light
                dd = ray(m, x, y, -LX, -LY)    # distance away from the light
                t = dd / (dl + dd)             # 1 near the lit edge, 0 near the shadow edge
                if t > 0.8 and dl <= 1.0 and base not in ('S', 'W', 'T'):
                    c = ramp[3]
                elif t > 0.3:
                    c = ramp[2]
                elif t > 0.12 or dd > 1.0:
                    c = ramp[1]
                else:
                    c = ramp[1]
                out[y][x] = c
    sp.layers.clear()
    sp.layers['main'] = out
    # outline: selective
    DARK = {'h': 'R', 'H': 'R', 'r': 'R', 'R': 'R', 'y': 'r', 'Y': 'r', 'o': 'r', 'S': 'r', 's': 'r',
            'W': 'v', 'w': 'v', 'v': 'v', 'g': 'E', 'G': 'E', 'e': 'E', 'E': 'E', 'T': 'b', 'b': 'd', 'B': 'd', 'd': 'd',
            'P': 'K', 'p': 'K', 'X': 'K', 'x': 'K', 'K': 'K'}

    def col(x, y, nb):
        shadow = any(dx == -1 or dy == -1 for dx, dy, _ in nb)
        mats = [ch for _, _, ch in nb]
        if shadow and not any(m in 'hHrR' for m in mats):
            return 'K'
        return DARK.get(mats[0], 'K')
    outline(out, col)
    sp.save(sys.argv[2])


if __name__ == '__main__':
    main()
