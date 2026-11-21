"""pxbuild.py - original construction of 48-px portrait art from designed shapes (STYLE_GUIDE 3.11).
Shapes (polygons) -> flat materials -> light from upper-left (hi / base / shadow / deep per material)
-> black silhouette + material-boundary lines -> hand-authored feature stamps (eyes, brows, nose, mouth).
No donor pixels. python3 -I only; PIL only."""
from PIL import Image, ImageDraw

CLEAR = (0, 0, 0, 0)


def hx(s, a=255):
    s = s.lstrip('#'); return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16), a)


class Canvas:
    def __init__(self, w=48, h=48):
        self.w, self.h = w, h
        self.mat = [[None] * w for _ in range(h)]      # material name per pixel
        self.col = [[None] * w for _ in range(h)]      # final colour override
        self.ramps = {}

    def ramp(self, name, hi, base, sh, deep):
        self.ramps[name] = [hx(hi), hx(base), hx(sh), hx(deep)]

    def poly(self, name, pts):
        m = Image.new('L', (self.w, self.h), 0)
        ImageDraw.Draw(m).polygon(pts, fill=255)
        p = m.load()
        for y in range(self.h):
            for x in range(self.w):
                if p[x, y]: self.mat[y][x] = name

    def put(self, name, pts):
        for (x, y) in pts:
            if 0 <= x < self.w and 0 <= y < self.h: self.mat[y][x] = name

    def clear(self, pts):
        for (x, y) in pts:
            if 0 <= x < self.w and 0 <= y < self.h: self.mat[y][x] = None; self.col[y][x] = None

    def inside(self, x, y, name=None):
        if not (0 <= x < self.w and 0 <= y < self.h): return False
        m = self.mat[y][x]
        return m is not None if name is None else m == name

    def shade(self, name, hi_depth=1, sh_depth=1, light=(-1, -1)):
        """base everywhere; hi where the pixel faces the light (neighbour toward light is outside the material);
        shadow where the pixel faces away. depth = how many px the band reaches."""
        lx, ly = light; r = self.ramps[name]
        for y in range(self.h):
            for x in range(self.w):
                if self.mat[y][x] != name: continue
                c = r[1]
                for k in range(1, sh_depth + 1):
                    if not self.inside(x - lx * k, y - ly * k, name) or not self.inside(x - lx * k, y, name) and not self.inside(x, y - ly * k, name):
                        c = r[2]; break
                for k in range(1, hi_depth + 1):
                    if not self.inside(x + lx * k, y + ly * k, name) and c == r[1]:
                        c = r[0]; break
                self.col[y][x] = c

    def fill(self, name, idx=1):
        for y in range(self.h):
            for x in range(self.w):
                if self.mat[y][x] == name: self.col[y][x] = self.ramps[name][idx]

    def paint(self, pts, colour):
        for (x, y) in pts:
            if 0 <= x < self.w and 0 <= y < self.h and self.mat[y][x] is not None: self.col[y][x] = colour

    def outline(self, colour, between=()):
        """silhouette: pixels of the figure that touch empty space (4-neighbour) -> colour.
        between: pairs (a, b): pixels of a touching b -> colour (or per-pair colour)."""
        out = []
        for y in range(self.h):
            for x in range(self.w):
                m = self.mat[y][x]
                if m is None: continue
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    if not self.inside(x + dx, y + dy):
                        out.append((x, y, colour)); break
                else:
                    for pair in between:
                        a, b = pair[0], pair[1]; c = pair[2] if len(pair) > 2 else colour
                        if m == a and any(self.inside(x + dx, y + dy, b) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                            out.append((x, y, c)); break
        for x, y, c in out: self.col[y][x] = c

    def stamp(self, x0, y0, rows, legend):
        """ASCII stamp: '.' = leave, ' ' = leave, other chars -> legend colour (or None = erase)."""
        for j, row in enumerate(rows):
            for i, ch in enumerate(row):
                if ch in '. ': continue
                x, y = x0 + i, y0 + j
                if not (0 <= x < self.w and 0 <= y < self.h): continue
                c = legend[ch]
                if c is None: self.mat[y][x] = None; self.col[y][x] = None
                else:
                    if self.mat[y][x] is None: self.mat[y][x] = 'stamp'
                    self.col[y][x] = c

    def image(self):
        im = Image.new('RGBA', (self.w, self.h), CLEAR); p = im.load()
        for y in range(self.h):
            for x in range(self.w):
                if self.mat[y][x] is not None and self.col[y][x] is not None: p[x, y] = self.col[y][x]
        return im
