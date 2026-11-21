"""rv2dt_ascii.py in.png [x0 y0 x1 y1] - print native pixels as letters with a palette legend (critique aid)"""
import sys
from PIL import Image
im = Image.open(sys.argv[1]).convert('RGBA'); p = im.load()
x0, y0, x1, y1 = (int(v) for v in sys.argv[2:6]) if len(sys.argv) > 5 else (0, 0, im.width, im.height)
pal = {}
sym = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#$%&*+=?@'
print('    ' + ''.join(str((x // 10) % 10) if x % 10 == 0 else ' ' for x in range(x0, x1)))
print('    ' + ''.join(str(x % 10) for x in range(x0, x1)))
for y in range(y0, y1):
    s = ''
    for x in range(x0, x1):
        c = p[x, y]
        if c[3] == 0: s += '.'; continue
        if c not in pal: pal[c] = sym[len(pal)]
        s += pal[c]
    print('%3d %s' % (y, s))
print(' '.join('%s=%02x%02x%02x' % (k, c[0], c[1], c[2]) for c, k in pal.items()))
