"""rv2dt_px.py - designed-shape pixel construction for the redo v2 of Dorian Pell and Tamsin Loom.
(STYLE_GUIDE 3.11 method, generalised to 80-px fronts and 16x24 overworlds.)

Shapes are painted back to front as named materials ("coat", "coat.tail", "skin.hand" ...; the part before the
dot is the material's GROUP, which owns the ramp). Then:
  base fill -> designed tone polygons / run-based edge bands (light from the upper left) ->
  lines: silhouette in the outline colour, boundaries between groups in the outline colour on the BEHIND side
  (so the front shape keeps its full size), folds inside one group in that group's deep tone ->
  hand passes (stamps, single pixels) -> lint (colours, orphans).
python3 -I only; PIL only. No donor pixels."""
from PIL import Image, ImageDraw

CLEAR = (0, 0, 0, 0)
N4 = ((1, 0), (-1, 0), (0, 1), (0, -1))
N8 = N4 + ((1, 1), (1, -1), (-1, 1), (-1, -1))


def hx(s, a=255):
    s = s.lstrip('#'); return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16), a)


def grp(name):
    return None if name is None else name.split('.')[0]


class Art:
    def __init__(self, w, h, outline='1a1220'):
        self.w, self.h = w, h
        self.mat = [[None] * w for _ in range(h)]
        self.col = [[None] * w for _ in range(h)]
        self.z = {}                      # material -> paint order (first paint)
        self.ramps = {}                  # group -> [hi, base, shadow, deep] (+ optional extra)
        self.K = hx(outline)
        self.noline = set()              # group pairs that meet without a line
        self.lock = set()                # pixels whose colour is final (stamps)

    # ---------------------------------------------------------------- shapes
    def ramp(self, group, *tones):
        self.ramps[group] = [hx(t) for t in tones]

    def _mask(self, draw_fn):
        m = Image.new('L', (self.w, self.h), 0)
        draw_fn(ImageDraw.Draw(m))
        p = m.load()
        return [(x, y) for y in range(self.h) for x in range(self.w) if p[x, y]]

    def _set(self, name, pts, clip=None, under=False):
        if name not in self.z: self.z[name] = len(self.z)
        for x, y in pts:
            if not (0 <= x < self.w and 0 <= y < self.h): continue
            cur = self.mat[y][x]
            if clip is not None and grp(cur) not in clip and cur not in clip: continue
            if under and cur is not None: continue
            self.mat[y][x] = name

    def poly(self, name, pts, clip=None, under=False):
        self._set(name, self._mask(lambda d: d.polygon(pts, fill=255)), clip, under)

    def ell(self, name, box, clip=None, under=False):
        self._set(name, self._mask(lambda d: d.ellipse(box, fill=255)), clip, under)

    def line(self, name, pts, width=1, clip=None, under=False):
        self._set(name, self._mask(lambda d: d.line(pts, fill=255, width=width)), clip, under)

    def px(self, name, pts, clip=None, under=False):
        self._set(name, pts, clip, under)

    def erase(self, pts):
        for x, y in pts:
            if 0 <= x < self.w and 0 <= y < self.h: self.mat[y][x] = None; self.col[y][x] = None

    def erase_poly(self, pts):
        self.erase(self._mask(lambda d: d.polygon(pts, fill=255)))

    def rows(self, spec):
        """spec: {y: [(x0, x1), ...]} -> list of points (inclusive)"""
        return [(x, y) for y, runs in spec.items() for a, b in runs for x in range(a, b + 1)]

    # ---------------------------------------------------------------- queries
    def at(self, x, y):
        return self.mat[y][x] if 0 <= x < self.w and 0 <= y < self.h else None

    def is_g(self, x, y, g):
        m = self.at(x, y)
        return m is not None and (grp(m) == g if isinstance(g, str) else grp(m) in g)

    def pts_of(self, g):
        return [(x, y) for y in range(self.h) for x in range(self.w) if self.is_g(x, y, g)]

    # ---------------------------------------------------------------- tones
    def base(self):
        for y in range(self.h):
            for x in range(self.w):
                m = self.mat[y][x]
                if m is not None and (x, y) not in self.lock: self.col[y][x] = self.ramps[grp(m)][1]

    def tone(self, g, idx, pts, mats=None):
        """set ramp tone idx on the pixels of group g (or only of the given materials) among pts"""
        r = self.ramps[g]; c = r[idx] if isinstance(idx, int) else hx(idx)
        for x, y in pts:
            if (x, y) in self.lock or not self.is_g(x, y, g): continue
            if mats and self.at(x, y) not in mats: continue
            self.col[y][x] = c

    def tone_poly(self, g, idx, poly, mats=None):
        self.tone(g, idx, self._mask(lambda d: d.polygon(poly, fill=255)), mats)

    def tone_line(self, g, idx, pts, width=1, mats=None):
        self.tone(g, idx, self._mask(lambda d: d.line(pts, fill=255, width=width)), mats)

    def band(self, g, idx, side, depth=1, mats=None, only=None):
        """run-based edge band: for each row (side 'r'/'l') or column ('t'/'b') take each run of the group
        (or of the given materials) and tone its last/first `depth` pixels. Gives even bands along curved
        edges, without the stair-step speckle of neighbour tests."""
        sel = (lambda x, y: self.at(x, y) in mats) if mats else (lambda x, y: self.is_g(x, y, g))
        out = []
        if side in 'lr':
            for y in range(self.h):
                x = 0
                while x < self.w:
                    if sel(x, y):
                        x0 = x
                        while x < self.w and sel(x, y): x += 1
                        run = list(range(x0, x))
                        pick = run[-depth:] if side == 'r' else run[:depth]
                        if len(run) > depth: out += [(i, y) for i in pick]
                    else: x += 1
        else:
            for x in range(self.w):
                y = 0
                while y < self.h:
                    if sel(x, y):
                        y0 = y
                        while y < self.h and sel(x, y): y += 1
                        run = list(range(y0, y))
                        pick = run[-depth:] if side == 'b' else run[:depth]
                        if len(run) > depth: out += [(x, i) for i in pick]
                    else: y += 1
        if only is not None:
            s = set(self._mask(lambda d: d.polygon(only, fill=255))); out = [p for p in out if p in s]
        self.tone(g, idx, out, mats)
        return out

    def despeckle(self, g, keep_min=2):
        """tone clusters (4-connected, same colour) smaller than keep_min inside group g -> the colour of the
        majority of their neighbours inside the group."""
        seen = set()
        for y in range(self.h):
            for x in range(self.w):
                if (x, y) in seen or not self.is_g(x, y, g) or (x, y) in self.lock: continue
                c = self.col[y][x]; comp = [(x, y)]; seen.add((x, y)); i = 0
                while i < len(comp):
                    a, b = comp[i]; i += 1
                    for dx, dy in N4:
                        q = (a + dx, b + dy)
                        if q not in seen and self.is_g(*q, g) and self.col[q[1]][q[0]] == c:
                            seen.add(q); comp.append(q)
                if len(comp) < keep_min:
                    nb = {}
                    for a, b in comp:
                        for dx, dy in N4:
                            if self.is_g(a + dx, b + dy, g) and self.col[b + dy][a + dx] != c:
                                k = self.col[b + dy][a + dx]; nb[k] = nb.get(k, 0) + 1
                    if nb:
                        new = max(nb, key=nb.get)
                        for a, b in comp: self.col[b][a] = new

    # ---------------------------------------------------------------- lines
    def lines(self, fold_groups=(), soft=None, silhouette=True, inner=None):
        """silhouette: figure pixels 4-touching empty -> K.
        between groups: the BEHIND pixel (lower z) gets K, unless the pair is in self.noline.
        fold_groups: groups whose different materials meet with the group's deep tone (on the behind side).
        soft: {(behind_group, front_group): colour} overrides for specific pairs."""
        inner = inner or {}; soft = soft or {}
        out = []
        for y in range(self.h):
            for x in range(self.w):
                m = self.mat[y][x]
                if m is None or (x, y) in self.lock: continue
                g = grp(m); c = None
                if silhouette and any(self.at(x + dx, y + dy) is None for dx, dy in N4):
                    c = self.K
                else:
                    for dx, dy in N4:
                        n = self.at(x + dx, y + dy)
                        if n is None or n == m: continue
                        gn = grp(n)
                        if self.z.get(n, 0) < self.z.get(m, 0): continue          # neighbour is behind: its job
                        if gn == g:
                            if g in fold_groups: c = self.ramps[g][3]
                            continue
                        if (g, gn) in self.noline or (gn, g) in self.noline: continue
                        c = soft.get((g, gn), self.K); break
                if c is not None: out.append((x, y, c))
        for x, y, c in out: self.col[y][x] = c

    def outline_colour(self, colour_fn):
        """recolour existing silhouette pixels: colour_fn(x, y, material) -> colour or None (keep)"""
        for y in range(self.h):
            for x in range(self.w):
                m = self.mat[y][x]
                if m is None: continue
                if any(self.at(x + dx, y + dy) is None for dx, dy in N4):
                    c = colour_fn(x, y, m)
                    if c is not None: self.col[y][x] = c

    # ---------------------------------------------------------------- hand passes
    def stamp(self, x0, y0, rows, legend, mat='stamp', lock=True):
        """'.' and ' ' leave the pixel; '_' erases; other characters -> legend colour."""
        for j, row in enumerate(rows):
            for i, ch in enumerate(row):
                if ch in '. ': continue
                x, y = x0 + i, y0 + j
                if not (0 <= x < self.w and 0 <= y < self.h): continue
                if ch == '_':
                    self.mat[y][x] = None; self.col[y][x] = None; continue
                c = legend[ch]
                if self.mat[y][x] is None:
                    if mat not in self.z: self.z[mat] = len(self.z)
                    self.mat[y][x] = mat
                self.col[y][x] = c
                if lock: self.lock.add((x, y))

    def paint(self, pts, colour, lock=True):
        c = hx(colour) if isinstance(colour, str) else colour
        for x, y in pts:
            if 0 <= x < self.w and 0 <= y < self.h and self.mat[y][x] is not None:
                self.col[y][x] = c
                if lock: self.lock.add((x, y))

    def drop_orphans(self):
        """figure pixels with fewer than 2 figure neighbours (8-way) are removed"""
        lone = [(x, y) for y in range(self.h) for x in range(self.w) if self.mat[y][x] is not None and
                sum(1 for dx, dy in N8 if self.at(x + dx, y + dy) is not None) < 2]
        self.erase(lone)
        return lone

    # ---------------------------------------------------------------- output
    def image(self):
        im = Image.new('RGBA', (self.w, self.h), CLEAR); p = im.load()
        for y in range(self.h):
            for x in range(self.w):
                if self.mat[y][x] is not None and self.col[y][x] is not None: p[x, y] = self.col[y][x]
        return im


def up(im, k):
    return im.resize((im.width * k, im.height * k), Image.NEAREST)


def colours(im):
    return len(set(c for c in im.convert('RGBA').getdata() if c[3]))


def lint(im, keep=()):
    """returns (colours, semi-transparent count, orphan list) for native art"""
    im = im.convert('RGBA'); p = im.load(); w, h = im.size
    semi = sum(1 for y in range(h) for x in range(w) if 0 < p[x, y][3] < 255)
    orph = []
    for y in range(h):
        for x in range(w):
            if p[x, y][3] == 0 or (x, y) in keep: continue
            n = sum(1 for dx, dy in N8 if 0 <= x + dx < w and 0 <= y + dy < h and p[x + dx, y + dy][3])
            if n < 2: orph.append((x, y))
    return colours(im), semi, orph


def silhouette(im, colour=(0, 0, 0, 255)):
    out = Image.new('RGBA', im.size, CLEAR); p, q = im.load(), out.load()
    for y in range(im.height):
        for x in range(im.width):
            if p[x, y][3]: q[x, y] = colour
    return out


def limb(p0, p1, w0, w1):
    """tapered quad from p0 to p1 (widths w0 at p0, w1 at p1) -> polygon points"""
    import math
    (x0, y0), (x1, y1) = p0, p1
    dx, dy = x1 - x0, y1 - y0; L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L, dx / L
    return [(x0 + nx * w0 / 2, y0 + ny * w0 / 2), (x1 + nx * w1 / 2, y1 + ny * w1 / 2),
            (x1 - nx * w1 / 2, y1 - ny * w1 / 2), (x0 - nx * w0 / 2, y0 - ny * w0 / 2)]


def sil_edit(base, add=(), sub=(), lines=(), ells=()):
    """silhouette exploration: black copy of `base` (RGBA image) with polygons added / erased, thick lines and
    ellipses added. Thumbnails for the review sheet, not art."""
    from PIL import ImageDraw
    m = Image.new('L', base.size, 0); p = base.load(); q = m.load()
    for y in range(base.height):
        for x in range(base.width):
            if p[x, y][3]: q[x, y] = 255
    d = ImageDraw.Draw(m)
    for poly in sub: d.polygon(poly, fill=0)
    for poly in add: d.polygon(poly, fill=255)
    for pts, w in lines: d.line(pts, fill=255, width=w)
    for box in ells: d.ellipse(box, fill=255)
    out = Image.new('RGBA', base.size, CLEAR); o = out.load(); q = m.load()
    for y in range(base.height):
        for x in range(base.width):
            if q[x, y]: o[x, y] = (0, 0, 0, 255)
    return out
