"""Print a sprite region as a character grid with a colour legend (for studying construction).
python3 -I dump.py FILE x0 y0 x1 y1"""
import sys, os, colorsys
from PIL import Image
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from contact import native

CH = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%&*+=?'


def main():
    f = sys.argv[1]
    x0, y0, x1, y1 = map(int, sys.argv[2:6])
    im, d = native(Image.open(f))
    a = np.array(im)
    full = a[a[..., 3] > 0][:, :3]
    cols = sorted(set(map(tuple, full)), key=lambda c: (0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]))
    idx = {c: CH[i] for i, c in enumerate(cols)}
    print('palette (%d colours, dark->light):' % len(cols))
    for c in cols:
        h, s, v = colorsys.rgb_to_hsv(*(np.array(c) / 255))
        n = int((full == c).all(axis=1).sum())
        print('  %s #%02x%02x%02x  H%3d S%3d V%3d  n=%d' % (idx[c], *c, h * 360, s * 100, v * 100, n))
    print('    ' + ''.join(str((x // 10) % 10) for x in range(x0, x1)))
    print('    ' + ''.join(str(x % 10) for x in range(x0, x1)))
    for y in range(y0, y1):
        row = ''
        for x in range(x0, x1):
            p = a[y, x]
            row += '.' if p[3] == 0 else idx[tuple(p[:3])]
        print('%3d %s' % (y, row))


if __name__ == '__main__':
    main()
