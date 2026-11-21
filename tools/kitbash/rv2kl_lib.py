"""rv2kl_lib.py - shared helpers for the redo-v2 Kestrel + Larch art (brief art/REDO_V2_BRIEF.md).
Original construction (STYLE_GUIDE 3.11): designed polygons -> materials with ramps -> light from the upper left
-> outline + material boundaries -> hand stamps (ASCII) for faces, hands and details. No donor pixels.
python3 -I only; PIL only."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', 'art', 'research', 'scripts'))
from PIL import Image, ImageDraw
from pxbuild import Canvas as _Canvas, hx

G = '/home/claude/fangame/'
N4 = ((1, 0), (-1, 0), (0, 1), (0, -1))
N8 = tuple((dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy)


class Canvas(_Canvas):
    def ramp(self, name, *tones):
        self.ramps[name] = [hx(t) if isinstance(t, str) else t for t in tones]

    def ellipse(self, name, box):
        m = Image.new('L', (self.w, self.h), 0)
        ImageDraw.Draw(m).ellipse(box, fill=255)
        p = m.load()
        for y in range(self.h):
            for x in range(self.w):
                if p[x, y]: self.mat[y][x] = name

    def rect(self, name, x0, y0, x1, y1):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if 0 <= x < self.w and 0 <= y < self.h: self.mat[y][x] = name

    def where(self, name):
        return [(x, y) for y in range(self.h) for x in range(self.w) if self.mat[y][x] == name]

    def where_pref(self, pref):
        return [(x, y) for y in range(self.h) for x in range(self.w) if (self.mat[y][x] or '').startswith(pref)]

    def rename(self, old, new, box=None):
        for y in range(self.h):
            for x in range(self.w):
                if self.mat[y][x] == old and (box is None or (box[0] <= x <= box[2] and box[1] <= y <= box[3])):
                    self.mat[y][x] = new

    def ink(self, pts, colour, only=None):
        """set colour on figure pixels (optionally only where material startswith `only`)."""
        c = hx(colour) if isinstance(colour, str) else colour
        for (x, y) in pts:
            if 0 <= x < self.w and 0 <= y < self.h and self.mat[y][x] is not None:
                if only is None or (self.mat[y][x] or '').startswith(only):
                    self.col[y][x] = c

    def line_pts(self, a, b):
        (x0, y0), (x1, y1) = a, b
        pts = []; dx = abs(x1 - x0); dy = -abs(y1 - y0); sx = 1 if x0 < x1 else -1; sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            pts.append((x0, y0))
            if x0 == x1 and y0 == y1: break
            e2 = 2 * err
            if e2 >= dy: err += dy; x0 += sx
            if e2 <= dx: err += dx; y0 += sy
        return pts

    def path_pts(self, pts):
        out = []
        for a, b in zip(pts, pts[1:]):
            for q in self.line_pts(a, b):
                if q not in out: out.append(q)
        return out

    def drop_lone(self, keep=()):
        lone = [(x, y) for y in range(self.h) for x in range(self.w) if self.mat[y][x] and (x, y) not in keep and
                sum(1 for dx, dy in N8 if self.inside(x + dx, y + dy)) < 2]
        self.clear(lone)
        return lone


def up(im, k):
    return im.resize((im.width * k, im.height * k), Image.NEAREST)


def lint(im):
    p = im.load(); w, h = im.size
    cols = set(); semi = 0; orph = []
    for y in range(h):
        for x in range(w):
            c = p[x, y]
            if 0 < c[3] < 255: semi += 1
            if c[3] == 255: cols.add(c)
    for y in range(h):
        for x in range(w):
            if p[x, y][3] == 0: continue
            same = sum(1 for dx, dy in N8 if 0 <= x + dx < w and 0 <= y + dy < h and p[x + dx, y + dy] == p[x, y])
            fig = sum(1 for dx, dy in N8 if 0 <= x + dx < w and 0 <= y + dy < h and p[x + dx, y + dy][3])
            if fig < 2: orph.append((x, y))
    return {'colours': len(cols), 'semi': semi, 'orphans': orph, 'bbox': im.getbbox()}


def zoom_sheet(items, k=8, cols=4, bg=(150, 150, 165, 255), gap=8, grid=0):
    """items: list of images -> one zoomed contact image (study)."""
    cw = max(i.width for i in items) * k + gap; ch = max(i.height for i in items) * k + gap
    rows = (len(items) + cols - 1) // cols
    S = Image.new('RGBA', (cols * cw, rows * ch), bg); d = ImageDraw.Draw(S)
    for n, im in enumerate(items):
        x, y = (n % cols) * cw, (n // cols) * ch
        S.alpha_composite(up(im, k), (x, y))
        if grid:
            for g in range(0, im.width + 1, grid): d.line([(x + g * k, y), (x + g * k, y + im.height * k)], fill=(255, 0, 0, 50))
            for g in range(0, im.height + 1, grid): d.line([(x, y + g * k), (x + im.width * k, y + g * k)], fill=(255, 0, 0, 50))
    return S


def black(im):
    out = Image.new('RGBA', im.size, (0, 0, 0, 0)); p, q = im.load(), out.load()
    for y in range(im.height):
        for x in range(im.width):
            if p[x, y][3]: q[x, y] = (0, 0, 0, 255)
    return out


def mirror(im):
    return im.transpose(Image.FLIP_LEFT_RIGHT)


def charset(frames):
    """frames[row][col] = 16x24 RGBA (rows: down, left, right, up) -> 128x192 sheet (doubled), like JUNO.png."""
    S = Image.new('RGBA', (64, 96), (0, 0, 0, 0))
    for r in range(4):
        for c in range(4):
            S.alpha_composite(frames[r][c], (c * 16, r * 24))
    return up(S, 2)


def ascii_img(rows, legend, w=None, h=None):
    """ASCII art -> RGBA. '.' or ' ' = transparent."""
    w = w or max(len(r) for r in rows); h = h or len(rows)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); p = im.load()
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch in '. ': continue
            c = legend[ch]
            p[x, y] = hx(c) if isinstance(c, str) else c
    return im


def diff_regions(a, b):
    pa, pb = a.load(), b.load()
    return [(x, y) for y in range(a.height) for x in range(a.width) if pa[x, y] != pb[x, y]]


def lock_shade(c, locks, ramp, crease, front_order, band=2, right_band=(), occl=True):
    """Hair as designed locks (STYLE_GUIDE 3.7). locks: names back->front already painted as materials.
    ramp = (hi, light, mid, shadow). Base = light; a `band`-px mid band on each lock's underside (where the lock ends
    above another lock or the face), a mid band on the right edge for locks in `right_band` (away from the light);
    crease (darkest tone) on the tucked-under (behind) lock where it meets a lock in front; the pixel above a crease = shadow."""
    hi, li, mi, sh = [hx(t) if isinstance(t, str) else t for t in ramp]
    rank = {n: i for i, n in enumerate(front_order)}
    def m(x, y): return c.mat[y][x] if 0 <= x < c.w and 0 <= y < c.h else None
    for y in range(c.h):
        for x in range(c.w):
            n = m(x, y)
            if n not in rank: continue
            col = li
            for k in range(1, band + 1):
                b = m(x, y + k)
                if b != n and b is not None: col = mi; break
            if n in right_band and m(x + 1, y) != n: col = mi
            c.col[y][x] = col
    # creases: behind-lock pixels touching a lock in front
    cr = []
    for y in range(c.h):
        for x in range(c.w):
            n = m(x, y)
            if n not in rank: continue
            for dx, dy in N4:
                o = m(x + dx, y + dy)
                if o in rank and rank[o] > rank[n]: cr.append((x, y)); break
    crease = hx(crease) if isinstance(crease, str) else crease
    for x, y in cr: c.col[y][x] = crease
    if occl:
        for x, y in cr:
            if y > 0 and m(x, y - 1) in rank and c.col[y - 1][x] == li: c.col[y - 1][x] = sh
    return cr


def denoise(c, mats=None, min_cluster=2, passes=2, protect=()):
    """absorb clusters of one colour smaller than min_cluster (4-connected) into the most common 4-neighbour colour
    of the same material set (never outline-coloured neighbours). Clean clusters, no 'mud' (STYLE_GUIDE 3.4)."""
    K = None
    for _ in range(passes):
        seen = set(); changes = []
        for y in range(c.h):
            for x in range(c.w):
                if (x, y) in seen or c.mat[y][x] is None or (x, y) in protect: continue
                if mats is not None and c.mat[y][x] not in mats: continue
                col = c.col[y][x]; stack = [(x, y)]; comp = []
                seen.add((x, y))
                while stack:
                    a, b = stack.pop(); comp.append((a, b))
                    for dx, dy in N4:
                        q = (a + dx, b + dy)
                        if 0 <= q[0] < c.w and 0 <= q[1] < c.h and q not in seen and c.mat[q[1]][q[0]] is not None \
                                and c.col[q[1]][q[0]] == col and (mats is None or c.mat[q[1]][q[0]] in mats):
                            seen.add(q); stack.append(q)
                if len(comp) >= min_cluster: continue
                for (a, b) in comp:
                    cnt = {}
                    for dx, dy in N4:
                        q = (a + dx, b + dy)
                        if 0 <= q[0] < c.w and 0 <= q[1] < c.h and c.mat[q[1]][q[0]] is not None and (mats is None or c.mat[q[1]][q[0]] in mats):
                            o = c.col[q[1]][q[0]]
                            if o != col and sum(o[:3]) > 60: cnt[o] = cnt.get(o, 0) + 1
                    if cnt: changes.append((a, b, max(cnt, key=cnt.get)))
        for a, b, o in changes: c.col[b][a] = o
