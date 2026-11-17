"""fs.py - frankensprite toolkit.  Every edit is explicit: whole-colour
remaps, masked copies from other stock sprites, and ASCII pixel patches.
Native resolution (64x64 fronts, 64x96 charsets); saved doubled."""
import numpy as np
from PIL import Image
REF_T = '/home/claude/ref/ebdx_renovation/Graphics/Trainers/'
REF_C = '/home/claude/ref/ebdx_renovation/Graphics/Characters/'


def load(path):
    im = Image.open(path).convert('RGBA')
    a = np.array(im)
    if im.width % 2 == 0 and (a[0::2, 0::2] == a[1::2, 1::2]).all():
        a = a[0::2, 0::2]
    return a.copy()


def T(name):
    return load(REF_T + name + '.png')


def C(name):
    return load(REF_C + name + '.png')


def hx(c):
    if isinstance(c, str):
        c = c.lstrip('#')
        return (int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16))
    return tuple(c[:3])


def palette(a):
    """[(rgb, count, (x0,y0,x1,y1))] opaque colours sorted by luminance."""
    op = a[..., 3] > 0
    cols = {}
    ys, xs = np.nonzero(op)
    for y, x in zip(ys, xs):
        k = tuple(int(v) for v in a[y, x, :3])
        if k not in cols:
            cols[k] = [0, x, y, x, y]
        e = cols[k]; e[0] += 1; e[1] = min(e[1], x); e[2] = min(e[2], y); e[3] = max(e[3], x); e[4] = max(e[4], y)
    out = [(k, v[0], tuple(v[1:])) for k, v in cols.items()]
    out.sort(key=lambda t: 0.3 * t[0][0] + 0.59 * t[0][1] + 0.11 * t[0][2])
    return out


def rect(a, x0, y0, x1, y1):
    m = np.zeros(a.shape[:2], bool)
    m[y0:y1 + 1, x0:x1 + 1] = True
    return m


def poly(a, pts):
    h, w = a.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w] + 0.5
    inside = np.zeros((h, w), bool)
    n = len(pts)
    for i in range(n):
        x0, y0 = pts[i]; x1, y1 = pts[(i + 1) % n]
        if y0 == y1:
            continue
        cond = ((y0 <= yy) & (yy < y1)) | ((y1 <= yy) & (yy < y0))
        inside ^= cond & (xx < x0 + (yy - y0) * (x1 - x0) / (y1 - y0))
    return inside


def colmask(a, cols):
    cols = [hx(c) for c in cols]
    m = np.zeros(a.shape[:2], bool)
    for c in cols:
        m |= (a[..., 0] == c[0]) & (a[..., 1] == c[1]) & (a[..., 2] == c[2]) & (a[..., 3] > 0)
    return m


def remap(a, mapping, mask=None):
    """mapping: {old: new}.  Applied simultaneously."""
    out = a.copy()
    for old, new in mapping.items():
        m = colmask(a, [old])
        if mask is not None:
            m &= mask
        out[m, :3] = hx(new)
        out[m, 3] = 255
    return out


def ramp_map(a, olds, news, mask=None):
    """Map an old ramp (dark->light list) onto a new ramp by rank."""
    mp = {}
    for i, o in enumerate(olds):
        j = round(i * (len(news) - 1) / max(1, len(olds) - 1))
        mp[o] = news[j]
    return remap(a, mp, mask)


def copy(dst, src, mask, dx=0, dy=0, clear_first=None):
    """Copy src pixels under `mask` (in src coords) into dst shifted by dx,dy."""
    out = dst.copy()
    if clear_first is not None:
        out[clear_first] = 0
    ys, xs = np.nonzero(mask & (src[..., 3] > 0))
    for y, x in zip(ys, xs):
        X, Y = x + dx, y + dy
        if 0 <= X < out.shape[1] and 0 <= Y < out.shape[0]:
            out[Y, X] = src[y, x]
    return out


def clear(a, mask):
    out = a.copy(); out[mask] = 0; return out


def patch(a, x, y, rows, legend):
    """ASCII patch: '.' leaves a pixel, '_' clears it, others = legend colour."""
    out = a.copy()
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch == '.' or ch == ' ':
                continue
            X, Y = x + i, y + j
            if not (0 <= X < out.shape[1] and 0 <= Y < out.shape[0]):
                continue
            if ch == '_':
                out[Y, X] = 0
            else:
                out[Y, X, :3] = hx(legend[ch]); out[Y, X, 3] = 255
    return out


def pix(a, pts, col):
    out = a.copy()
    for x, y in pts:
        out[y, x, :3] = hx(col); out[y, x, 3] = 255
    return out


def ncol(a):
    op = a[..., 3] > 0
    return len({tuple(v) for v in a[op][:, :3]})


def to_img(a, scale=2):
    im = Image.fromarray(a.astype(np.uint8), 'RGBA')
    return im.resize((im.width * scale, im.height * scale), Image.NEAREST)


def swatch(a, path, S=16):
    from PIL import ImageDraw
    p = palette(a)
    im = Image.new('RGBA', (360, S * len(p) + 4), (200, 200, 200, 255)); d = ImageDraw.Draw(im)
    for i, (c, n, bb) in enumerate(p):
        d.rectangle([2, 2 + i * S, 2 + S * 2, 2 + i * S + S - 2], fill=c + (255,))
        d.text((40, 2 + i * S + 2), f'#{c[0]:02x}{c[1]:02x}{c[2]:02x} n={n} bb={bb}', fill=(0, 0, 0, 255))
    im.save(path)
