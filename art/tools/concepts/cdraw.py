"""cdraw: quick concept-thumbnail helpers on top of art/tools/v4/px4.py.
A concept is drawn back-to-front with flat base colours (Canvas primitives), then
shade() adds a directional cel shade (light from upper left), then outline() a 1-px dark rim.
Faces and small accents are hand-placed with put() rows. Output: a px4 .spr (single 'main' layer) + PNGs."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'v4'))
from px4 import Sprite, Canvas, outline as _outline  # noqa: E402
from collections import OrderedDict

COMMON = [
    ('K', '#1b1320', 'outline'),
    ('S', '#ffd8bc', 'skin'),
    ('s', '#e79f7e', 'skin shadow'),
    ('q', '#a8574a', 'skin deep / mouth line / freckle'),
    ('m', '#6e1c2c', 'mouth inside'),
    ('n', '#e8707a', 'tongue'),
    ('X', '#ffffff', 'white / catchlight / teeth'),
    ('e', '#2a1828', 'eye dark'),
    ('H', '#e98a4a', 'hair light'),
    ('h', '#c0532c', 'hair base (auburn)'),
    ('r', '#86302a', 'hair shadow'),
    ('R', '#521c22', 'hair deep'),
    ('p', '#c42f3a', 'ball red'),
    ('P', '#ef5a52', 'ball red light'),
    ('x', '#c9ccd8', 'ball grey'),
]

BASE_RAMPS = {
    'S': (None, 's'),
    'h': ('H', 'r'),
    'p': ('P', None),
}


class C:
    def __init__(self, pal, ramps, w=80, h=80):
        self.w, self.h = w, h
        self.pal = OrderedDict()
        for c, hx, n in COMMON + pal:
            self.pal[c] = (hx, n)
        self.ramps = dict(BASE_RAMPS)
        self.ramps.update(ramps)
        self.cv = Canvas(w, h)

    # shorthand primitives
    def poly(self, pts, c): self.cv.poly(pts, c)
    def ell(self, cx, cy, rx, ry, c): self.cv.ellipse(cx, cy, rx, ry, c)
    def disc(self, cx, cy, r, c): self.cv.disc(cx, cy, r, c)
    def line(self, x0, y0, x1, y1, c, w=1): self.cv.line(x0, y0, x1, y1, c, w)
    def limb(self, pts, widths, c): self.cv.limb(pts, widths, c)
    def px(self, x, y, c): self.cv.px(x, y, c)
    def rect(self, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.cv.px(x, y, c)

    def put(self, x0, y0, rows):
        """Hand-place pixels: rows of chars, '.' = leave, '_' = clear."""
        for j, row in enumerate(rows):
            for i, ch in enumerate(row):
                if ch == '.':
                    continue
                self.cv.px(x0 + i, y0 + j, '.' if ch == '_' else ch)

    def get(self, x, y): return self.cv.get(x, y)

    # ---- passes
    def shade(self, width=None):
        """Directional cel shade. For every base colour with a ramp (light, shadow):
        shadow where the form ends within `w` px to the lower right; light on the upper-left rim."""
        width = width or {}
        g = self.cv.g
        src = [row[:] for row in g]
        groups = {}
        for b, (hi, sh) in self.ramps.items():
            groups[b] = {b} | ({hi} if hi else set()) | ({sh} if sh else set())

        def inside(x, y, grp):
            return 0 <= x < self.w and 0 <= y < self.h and src[y][x] in grp

        for y in range(self.h):
            for x in range(self.w):
                c = src[y][x]
                if c not in self.ramps:
                    continue
                hi, sh = self.ramps[c]
                grp = groups[c]
                w = width.get(c, 1)
                if sh:
                    offs = [(1, 0), (0, 1), (1, 1)]
                    if w >= 2:
                        offs += [(2, 0), (0, 2), (2, 1), (1, 2), (2, 2)]
                    if any(not inside(x + dx, y + dy, grp) for dx, dy in offs):
                        g[y][x] = sh
                        continue
                if hi and not inside(x - 1, y - 1, grp) and (not inside(x - 1, y, grp) or not inside(x, y - 1, grp)):
                    g[y][x] = hi

    def outline(self, c='K'):
        _outline(self.cv.g, lambda x, y, nb: c)

    # ---- output
    def sprite(self):
        sp = Sprite(self.w, self.h)
        sp.pal = self.pal
        sp.layers['main'] = [row[:] for row in self.cv.g]
        return sp

    def save(self, path):
        sp = self.sprite()
        sp.save(path)
        return sp


def ball(c, cx, cy, r=4):
    """A Poke Ball: red top, grey-white bottom, dark band, white button (call after shade, before outline)."""
    for y in range(int(cy - r - 1), int(cy + r + 2)):
        for x in range(int(cx - r - 1), int(cx + r + 2)):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r * r + 0.3:
                if y < cy:
                    ch = 'P' if (x - cx) + (y - cy) < -r * 0.9 else 'p'
                elif y > cy:
                    ch = 'x'
                else:
                    ch = 'K'
                c.px(x, y, ch)
    c.px(cx, cy, 'X'); c.px(cx - 1, cy, 'K'); c.px(cx + 1, cy, 'K')
    c.px(cx, cy - 1, 'K'); c.px(cx, cy + 1, 'K')


def png(c, path, x2=False):
    """Write the concept as a PNG (works for any canvas size; px4's CLI loader assumes 80x80)."""
    from PIL import Image
    im = c.sprite().image()
    if x2:
        im = im.resize((im.width * 2, im.height * 2), Image.NEAREST)
    im.save(path)
    return im
