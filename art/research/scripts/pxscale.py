# usage: python3 -I pxscale.py <png> ... ; detects integer upscale factor of pixel art (run lengths gcd), reports native size + colour count
import sys
from math import gcd
from PIL import Image
for f in sys.argv[1:]:
    im = Image.open(f).convert('RGBA'); w, h = im.size; px = im.load()
    g = 0
    for y in range(0, h, max(1, h//40)):
        run = 1
        for x in range(1, w):
            if px[x, y] == px[x-1, y]: run += 1
            else: g = gcd(g, run); run = 1
    cols = len(set(im.getdata()))
    print(f.split('/')[-1], im.size, 'factor~', g, 'native~', (w//g if g else None, h//g if g else None), 'colours', cols)
