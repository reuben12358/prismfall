"""kb.py - kitbash toolkit (Prismfall).

Shared helpers for indexing donor sprites, cutting parts, compositing layers and
rendering comparison sheets. PIL only. Run every script that reads /home/claude/ref
with `python3 -I`; keep scripts in tools/kitbash (never inside ref/ or downloads).
"""
import os, sys, glob, json, math, colorsys
from PIL import Image, ImageDraw, ImageFont

REF = '/home/claude/ref'
GAME = '/home/claude/fangame'
WORK = GAME + '/art/work/kitbash'


# ----------------------------------------------------------------- loading
def load(path):
    im = Image.open(path)
    im = im.convert('RGBA')
    # hard alpha: treat semi transparent as opaque/transparent
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a < 128:
                px[x, y] = (0, 0, 0, 0)
            elif a != 255:
                px[x, y] = (r, g, b, 255)
    return im


def is_doubled(im, k=2):
    """True if every kxk block (aligned at 0,0) is a single colour."""
    w, h = im.size
    if w % k or h % k:
        return False
    px = im.load()
    for y in range(0, h, k):
        for x in range(0, w, k):
            c = px[x, y]
            for dy in range(k):
                for dx in range(k):
                    if px[x + dx, y + dy] != c:
                        return False
    return True


def doubled_ratio(im, k=2):
    """fraction of opaque kxk blocks that are uniform (for messy rips)."""
    w, h = im.size
    px = im.load()
    tot = ok = 0
    for y in range(0, h - h % k, k):
        for x in range(0, w - w % k, k):
            c = px[x, y]
            if c[3] == 0 and px[x + 1, y + 1][3] == 0:
                continue
            tot += 1
            if all(px[x + dx, y + dy] == c for dy in range(k) for dx in range(k)):
                ok += 1
    return ok / tot if tot else 1.0


def native(im):
    """Return (native_image, factor). Halves repeatedly while blocks are uniform."""
    f = 1
    while is_doubled(im, 2) and im.size[0] >= 32:
        im = im.resize((im.size[0] // 2, im.size[1] // 2), Image.NEAREST)
        f *= 2
    return im, f


def bbox(im):
    return im.getchannel('A').getbbox()


def colours(im):
    c = im.getcolors(1 << 20) or []
    return [(n, rgba) for n, rgba in c if rgba[3] > 0]


def up(im, k):
    return im.resize((im.size[0] * k, im.size[1] * k), Image.NEAREST)


def lum(c):
    r, g, b = c[:3]
    return 0.299 * r + 0.587 * g + 0.114 * b


def outline_colours(im):
    """colours of opaque pixels that touch transparency (the silhouette edge)."""
    px = im.load(); w, h = im.size
    cnt = {}
    for y in range(h):
        for x in range(w):
            c = px[x, y]
            if c[3] == 0:
                continue
            edge = False
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                xx, yy = x + dx, y + dy
                if not (0 <= xx < w and 0 <= yy < h) or px[xx, yy][3] == 0:
                    edge = True; break
            if edge:
                cnt[c] = cnt.get(c, 0) + 1
    return sorted(cnt.items(), key=lambda t: -t[1])


# ----------------------------------------------------------------- layers
class Canvas:
    """Simple layered compositor at native resolution."""

    def __init__(self, w, h):
        self.w, self.h = w, h
        self.layers = []  # (name, image RGBA w x h)

    def add(self, name, part, x, y, flip=False):
        L = Image.new('RGBA', (self.w, self.h), (0, 0, 0, 0))
        if flip:
            part = part.transpose(Image.FLIP_LEFT_RIGHT)
        L.paste(part, (x, y), part)
        self.layers.append([name, L])
        return L

    def get(self, name):
        for n, L in self.layers:
            if n == name:
                return L
        raise KeyError(name)

    def flat(self):
        out = Image.new('RGBA', (self.w, self.h), (0, 0, 0, 0))
        for n, L in self.layers:
            out.alpha_composite(L)
        return out


def crop_mask(im, mask_fn):
    """keep pixels where mask_fn(x,y,c) is true"""
    out = Image.new('RGBA', im.size, (0, 0, 0, 0))
    a = im.load(); b = out.load()
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            c = a[x, y]
            if c[3] and mask_fn(x, y, c):
                b[x, y] = c
    return out


def poly_mask(size, polys):
    m = Image.new('L', size, 0)
    d = ImageDraw.Draw(m)
    for p in polys:
        d.polygon(p, fill=255)
    return m


def cut(im, polys=None, rect=None, invert=False):
    """cut a part by polygon(s) or rect (x0,y0,x1,y1 inclusive-exclusive)."""
    if rect:
        polys = [[(rect[0], rect[1]), (rect[2] - 1, rect[1]), (rect[2] - 1, rect[3] - 1), (rect[0], rect[3] - 1)]]
    m = poly_mask(im.size, polys)
    if invert:
        m = m.point(lambda v: 255 - v)
    out = Image.new('RGBA', im.size, (0, 0, 0, 0))
    out.paste(im, (0, 0), m)
    # paste with mask multiplies alpha only where mask; ensure hard alpha
    px = out.load()
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            if px[x, y][3] < 128:
                px[x, y] = (0, 0, 0, 0)
            else:
                c = px[x, y]; px[x, y] = (c[0], c[1], c[2], 255)
    return out


# ----------------------------------------------------------------- recolour
def hexc(s):
    s = s.lstrip('#')
    return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16), 255)


def remap(im, table, region=None):
    """exact colour substitution. table: {src_rgba: dst_rgba}. region: optional L mask."""
    out = im.copy(); px = out.load()
    rm = region.load() if region else None
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            c = px[x, y]
            if c[3] and c in table and (rm is None or rm[x, y]):
                px[x, y] = table[c]
    return out


def ramp_map(im, src_cols, ramp, region=None, outline=None, outline_thresh=None):
    """Map a set of source colours onto a designed ramp by luminance rank.
    src_cols: list of rgba in the material; ramp: list dark->light of rgba.
    Source colours are sorted by luminance and bucketed onto the ramp, keeping the
    donor's shading structure (which pixel is light/dark) while replacing hues."""
    src = sorted(set(src_cols), key=lum)
    n = len(src)
    table = {}
    lo, hi = lum(src[0]), lum(src[-1])
    for i, c in enumerate(src):
        if outline is not None and outline_thresh is not None and lum(c) <= outline_thresh:
            table[c] = outline
            continue
        t = (lum(c) - lo) / (hi - lo) if hi > lo else 0.5
        k = min(len(ramp) - 1, int(round(t * (len(ramp) - 1))))
        table[c] = ramp[k]
    return remap(im, table, region), table


def lum_ramp(im, ramp, region, breaks=None):
    """recolour every opaque pixel inside region by its luminance into ramp
    (dark->light). breaks: luminance thresholds len(ramp)-1, else even split
    over the region's luminance range."""
    px = im.load(); rm = region.load()
    vals = []
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            if rm[x, y] and px[x, y][3]:
                vals.append(lum(px[x, y]))
    if not vals:
        return im
    out = im.copy(); o = out.load()
    if breaks is None:
        lo, hi = min(vals), max(vals)
        breaks = [lo + (hi - lo) * (i + 1) / len(ramp) for i in range(len(ramp) - 1)]
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            if rm[x, y] and px[x, y][3]:
                l = lum(px[x, y]); k = 0
                while k < len(breaks) and l > breaks[k]:
                    k += 1
                o[x, y] = ramp[k]
    return out


# ----------------------------------------------------------------- render
_font = None


def font(sz=10):
    for p in ['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
              '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf']:
        if os.path.exists(p):
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def grid(im, k=8, line=(0, 0, 0, 40), bg=(200, 200, 210, 255), every=10):
    """zoomed pixel grid with coordinate ticks for planning edits."""
    w, h = im.size
    out = Image.new('RGBA', (w * k + 30, h * k + 20), (255, 255, 255, 255))
    base = Image.new('RGBA', (w, h), bg)
    base.alpha_composite(im)
    out.paste(up(base, k), (30, 20))
    d = ImageDraw.Draw(out)
    f = font(9)
    for x in range(0, w + 1):
        col = (0, 0, 0, 120) if x % every == 0 else line
        d.line([(30 + x * k, 20), (30 + x * k, 20 + h * k)], fill=col)
        if x % every == 0 and x < w:
            d.text((30 + x * k + 1, 5), str(x), fill=(0, 0, 0, 255), font=f)
    for y in range(0, h + 1):
        col = (0, 0, 0, 120) if y % every == 0 else line
        d.line([(30, 20 + y * k), (30 + w * k, 20 + y * k)], fill=col)
        if y % every == 0 and y < h:
            d.text((2, 20 + y * k + 1), str(y), fill=(0, 0, 0, 255), font=f)
    return out


def on_bg(im, bg):
    out = Image.new('RGBA', im.size, bg)
    out.alpha_composite(im)
    return out


def contact(items, cols, cell, k=1, bg=(150, 160, 170, 255), label_h=12, fs=9):
    """items: list of (label, image). Each image shown at k x, centred bottom in cell."""
    rows = (len(items) + cols - 1) // cols
    W, H = cols * cell[0], rows * (cell[1] + label_h)
    out = Image.new('RGBA', (W, H), (40, 42, 50, 255))
    d = ImageDraw.Draw(out); f = font(fs)
    for i, (lab, im) in enumerate(items):
        cx, cy = (i % cols) * cell[0], (i // cols) * (cell[1] + label_h)
        d.rectangle([cx + 1, cy + 1, cx + cell[0] - 2, cy + cell[1] - 2], fill=bg)
        z = up(im, k) if k != 1 else im
        if z.size[0] > cell[0] - 2 or z.size[1] > cell[1] - 2:
            s = min((cell[0] - 2) / z.size[0], (cell[1] - 2) / z.size[1])
            z = z.resize((max(1, int(z.size[0] * s)), max(1, int(z.size[1] * s))), Image.NEAREST)
        out.alpha_composite(z, (cx + (cell[0] - z.size[0]) // 2, cy + cell[1] - z.size[1] - 1))
        d.text((cx + 2, cy + cell[1]), lab, fill=(230, 230, 230, 255), font=f)
    return out
