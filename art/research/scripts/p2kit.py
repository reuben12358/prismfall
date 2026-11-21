"""p2kit.py - construction kit for the player redo (v2): designed shapes -> materials -> light -> lines -> stamps.
Extends the pxbuild idea (STYLE_GUIDE 3.11) to any canvas size (80x80 fronts and backs, 48x48 portraits, 16x24 walkers).
No donor pixels. PIL only. Used by player2_*.py.  python3 -I only."""
import math
from PIL import Image, ImageDraw

CLEAR = (0, 0, 0, 0)
N4 = ((1, 0), (-1, 0), (0, 1), (0, -1))
N8 = N4 + ((1, 1), (1, -1), (-1, 1), (-1, -1))


def hx(s, a=255):
    s = s.lstrip('#'); return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16), a)


def capsule(p0, p1, r0, r1=None, n=10):
    """tapered limb polygon from p0 (radius r0) to p1 (radius r1)."""
    r1 = r0 if r1 is None else r1
    (x0, y0), (x1, y1) = p0, p1
    a = math.atan2(y1 - y0, x1 - x0)
    pts = []
    for i in range(n + 1):
        t = a + math.pi / 2 + math.pi * i / n
        pts.append((x1 + r1 * math.cos(t - math.pi), y1 + r1 * math.sin(t - math.pi)))
    for i in range(n + 1):
        t = a + math.pi / 2 + math.pi * i / n
        pts.append((x0 + r0 * math.cos(t), y0 + r0 * math.sin(t)))
    return pts


def ell(cx, cy, rx, ry, n=24, rot=0.0):
    c, s = math.cos(rot), math.sin(rot)
    out = []
    for i in range(n):
        t = 2 * math.pi * i / n
        x, y = rx * math.cos(t), ry * math.sin(t)
        out.append((cx + x * c - y * s, cy + x * s + y * c))
    return out


class Spr:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.mat = [[None] * w for _ in range(h)]
        self.col = [[None] * w for _ in range(h)]
        self.ramps = {}

    # ------------------------------------------------------------------ shapes
    def ramp(self, name, *tones):
        self.ramps[name] = [hx(t) if isinstance(t, str) else t for t in tones]

    def _mask(self, draw):
        m = Image.new('L', (self.w, self.h), 0); draw(ImageDraw.Draw(m)); return m.load()

    def poly(self, name, pts, only=None):
        p = self._mask(lambda d: d.polygon([(round(x), round(y)) for x, y in pts], fill=255))
        self._apply(p, name, only)

    def rect(self, name, x0, y0, x1, y1, only=None):
        p = self._mask(lambda d: d.rectangle([x0, y0, x1, y1], fill=255)); self._apply(p, name, only)

    def line(self, name, pts, width=1, only=None):
        p = self._mask(lambda d: d.line([(round(x), round(y)) for x, y in pts], fill=255, width=width)); self._apply(p, name, only)

    def _apply(self, p, name, only):
        for y in range(self.h):
            for x in range(self.w):
                if p[x, y] and (only is None or self.mat[y][x] in only):
                    self.mat[y][x] = name; self.col[y][x] = None

    def put(self, name, pts):
        for (x, y) in pts:
            if 0 <= x < self.w and 0 <= y < self.h: self.mat[y][x] = name; self.col[y][x] = None

    def spans(self, name, rows, only=None):
        """rows: {y: (x0, x1)} or {y: [(x0, x1), ...]} inclusive spans -> material."""
        for y, sp in rows.items():
            if isinstance(sp[0], int): sp = [sp]
            for (x0, x1) in sp:
                for x in range(x0, x1 + 1):
                    if 0 <= x < self.w and 0 <= y < self.h and (only is None or self.mat[y][x] in only):
                        self.mat[y][x] = name; self.col[y][x] = None

    def mstamp(self, x0, y0, rows, legend):
        """material stamp: char -> material name ('' / None = erase); '.' and ' ' leave."""
        for j, row in enumerate(rows):
            for i, ch in enumerate(row):
                if ch in '. ': continue
                x, y = x0 + i, y0 + j
                if 0 <= x < self.w and 0 <= y < self.h:
                    m = legend[ch]
                    self.mat[y][x] = m if m else None; self.col[y][x] = None

    def erase(self, pts):
        for (x, y) in pts:
            if 0 <= x < self.w and 0 <= y < self.h: self.mat[y][x] = None; self.col[y][x] = None

    def inside(self, x, y, name=None):
        if not (0 <= x < self.w and 0 <= y < self.h): return False
        m = self.mat[y][x]
        if name is None: return m is not None
        if isinstance(name, (set, tuple, list)): return m in name
        return m == name

    def pixels(self, name):
        return [(x, y) for y in range(self.h) for x in range(self.w) if self.mat[y][x] == name]

    def replace(self, old, new):
        for y in range(self.h):
            for x in range(self.w):
                if self.mat[y][x] == old: self.mat[y][x] = new

    # ------------------------------------------------------------------ light
    def shade(self, name, hi=1, sh=1, light=(-1, -1), group=None, hi_edge_only=True):
        """base everywhere; shadow band (sh px) on the side away from the light, highlight band (hi px) on the lit side.
        group: the set of materials that count as 'the same surface' (default: just this one)."""
        g = group or {name}
        lx, ly = light; r = self.ramps[name]
        for y in range(self.h):
            for x in range(self.w):
                if self.mat[y][x] != name: continue
                c = r[1]
                for k in range(1, sh + 1):
                    if not self.inside(x - lx * k, y - ly * k, g) or (not self.inside(x - lx * k, y, g) and not self.inside(x, y - ly * k, g)):
                        c = r[2]; break
                if c == r[1]:
                    for k in range(1, hi + 1):
                        if not self.inside(x + lx * k, y + ly * k, g):
                            c = r[0]; break
                self.col[y][x] = c

    def fill(self, name, idx=1):
        for y in range(self.h):
            for x in range(self.w):
                if self.mat[y][x] == name: self.col[y][x] = self.ramps[name][idx]

    def tone(self, name, idx, pts):
        c = self.ramps[name][idx]
        for (x, y) in pts:
            if 0 <= x < self.w and 0 <= y < self.h and self.mat[y][x] == name: self.col[y][x] = c

    def paint(self, pts, colour, only=None):
        c = hx(colour) if isinstance(colour, str) else colour
        for (x, y) in pts:
            if 0 <= x < self.w and 0 <= y < self.h and self.mat[y][x] is not None and (only is None or self.mat[y][x] in only):
                self.col[y][x] = c

    # ------------------------------------------------------------------ lines
    def outline(self, K, pairs=(), skip=()):
        """silhouette pixels (touching empty, 4-neighbour) -> K; pairs (a, b[, colour]): pixels of a touching b -> colour."""
        K = hx(K) if isinstance(K, str) else K
        out = []
        for y in range(self.h):
            for x in range(self.w):
                m = self.mat[y][x]
                if m is None or m in skip: continue
                if any(not self.inside(x + dx, y + dy) for dx, dy in N4):
                    out.append((x, y, K)); continue
                for pr in pairs:
                    a, b = pr[0], pr[1]
                    c = pr[2] if len(pr) > 2 else K
                    c = hx(c) if isinstance(c, str) else c
                    am = m == a if isinstance(a, str) else m in a
                    if am and any(self.inside(x + dx, y + dy, b) for dx, dy in N4):
                        out.append((x, y, c)); break
        for x, y, c in out: self.col[y][x] = c

    def stamp(self, x0, y0, rows, legend, mat='stamp'):
        """colour stamp: char -> colour (None = erase); '.' and ' ' leave. New pixels get material `mat`."""
        for j, row in enumerate(rows):
            for i, ch in enumerate(row):
                if ch in '. ': continue
                x, y = x0 + i, y0 + j
                if not (0 <= x < self.w and 0 <= y < self.h): continue
                c = legend[ch]
                if c is None: self.mat[y][x] = None; self.col[y][x] = None
                else:
                    if self.mat[y][x] is None: self.mat[y][x] = mat
                    self.col[y][x] = hx(c) if isinstance(c, str) else c

    def drop_lone(self, protect=()):
        lone = [(x, y) for y in range(self.h) for x in range(self.w) if self.mat[y][x] and (x, y) not in protect and
                sum(1 for dx, dy in N8 if self.inside(x + dx, y + dy)) < 2]
        self.erase(lone)

    def image(self):
        im = Image.new('RGBA', (self.w, self.h), CLEAR); p = im.load()
        for y in range(self.h):
            for x in range(self.w):
                if self.mat[y][x] is not None and self.col[y][x] is not None: p[x, y] = self.col[y][x]
        return im

    def matimage(self, colours):
        """flat material view, for checking shapes."""
        im = Image.new('RGBA', (self.w, self.h), CLEAR); p = im.load()
        for y in range(self.h):
            for x in range(self.w):
                m = self.mat[y][x]
                if m is not None: p[x, y] = colours.get(m, (255, 0, 255, 255))
        return im


# ---------------------------------------------------------------------- image helpers
def up(im, k): return im.resize((im.width * k, im.height * k), Image.NEAREST)


def black(im, c=(0, 0, 0, 255)):
    out = Image.new('RGBA', im.size, CLEAR); p, q = im.load(), out.load()
    for y in range(im.height):
        for x in range(im.width):
            if p[x, y][3]: q[x, y] = c
    return out


def ncolours(im):
    return len({p for p in im.getdata() if p[3]})


def mirror(im): return im.transpose(Image.FLIP_LEFT_RIGHT)


def recolour(im, table):
    """exact colour map (hex or tuple keys)."""
    t = {}
    for k, v in table.items():
        t[hx(k) if isinstance(k, str) else k] = hx(v) if isinstance(v, str) else v
    out = im.copy(); p = out.load()
    for y in range(im.height):
        for x in range(im.width):
            c = p[x, y]
            if c[3] and c in t: p[x, y] = t[c]
    return out


def lint(im):
    p = im.load(); w, h = im.size
    semi = sum(1 for y in range(h) for x in range(w) if 0 < p[x, y][3] < 255)
    orph = [(x, y) for y in range(h) for x in range(w) if p[x, y][3] and
            not any(0 <= x + dx < w and 0 <= y + dy < h and p[x + dx, y + dy][3] for dx, dy in N4)]
    return {'colours': ncolours(im), 'semi': semi, 'orphans': orph, 'bbox': im.getbbox()}
