#!/usr/bin/env python3
"""make_fogs.py (builder 3): tileable fog pictures for the early maps -> maps_out/Graphics/Fogs/.
Drawn on the 16-px logical grid (128x128) and doubled, like every other custom tile.  Run once."""
import os, math, random
from PIL import Image
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'maps_out', 'Graphics', 'Fogs')


def tnoise(n, seed, octaves=((8, 1.0), (16, 0.5), (32, 0.25))):
    """Periodic value noise on an n x n torus."""
    r = random.Random(seed); out = [[0.0] * n for _ in range(n)]; tot = 0
    for cells, amp in octaves:
        g = [[r.random() for _ in range(cells)] for _ in range(cells)]; tot += amp
        for y in range(n):
            for x in range(n):
                fx = x * cells / n; fy = y * cells / n; ix, iy = int(fx), int(fy); tx, ty = fx - ix, fy - iy
                tx = tx * tx * (3 - 2 * tx); ty = ty * ty * (3 - 2 * ty)
                a = g[iy % cells][ix % cells]; b = g[iy % cells][(ix + 1) % cells]
                c = g[(iy + 1) % cells][ix % cells]; d = g[(iy + 1) % cells][(ix + 1) % cells]
                out[y][x] += amp * ((a * (1 - tx) + b * tx) * (1 - ty) + (c * (1 - tx) + d * tx) * ty)
    return [[v / tot for v in row] for row in out]


def fog(name, col, lo, hi, amax, seed, motes=None):
    n = 128; nz = tnoise(n, seed); im = Image.new('RGBA', (n, n)); px = im.load()
    for y in range(n):
        for x in range(n):
            t = max(0.0, min(1.0, (nz[y][x] - lo) / (hi - lo)))
            t = round(t * 4) / 4.0                                 # 4 alpha steps: pixel-art banding, no smooth gradient
            px[x, y] = col + (int(amax * t),)
    if motes:
        r = random.Random(seed + 9); mc, k = motes
        for _ in range(k):
            x, y = r.randrange(n), r.randrange(n); px[x, y] = mc + (230,)
            if r.random() < 0.3: px[(x + 1) % n, y] = mc + (140,)
    im = im.resize((256, 256), Image.NEAREST); im.save(os.path.join(OUT, name + '.png')); print('fog', name)


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    fog('prismfall_seamist', (236, 244, 248), 0.45, 0.85, 150, 1)
    fog('prismfall_spores', (210, 236, 170), 0.50, 0.90, 110, 2, motes=((255, 248, 200), 70))
    fog('prismfall_glass', (196, 180, 255), 0.40, 0.85, 150, 3, motes=((255, 240, 255), 90))
    fog('prismfall_cave', (150, 120, 190), 0.35, 0.85, 170, 4, motes=((220, 200, 255), 40))
