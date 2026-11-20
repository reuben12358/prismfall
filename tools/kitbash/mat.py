"""mat.py - material masks, ramps and ASCII patching for kitbash recipes."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb
from PIL import Image, ImageDraw

H = kb.hexc
BLACK = (0, 0, 0, 255)
CLEAR = (0, 0, 0, 0)


def region(size, polys=None, rect=None):
    m = Image.new('L', size, 0)
    d = ImageDraw.Draw(m)
    if rect:
        d.rectangle(rect, fill=255)
    for p in polys or []:
        d.polygon(p, fill=255)
    return m


def mask_and(a, b):
    from PIL import ImageChops
    return ImageChops.multiply(a, b)


def mask_or(a, b):
    from PIL import ImageChops
    return ImageChops.lighter(a, b)


def mask_not(a):
    return a.point(lambda v: 255 - v)


def colour_mask(im, cols, reg=None):
    cols = set(tuple(c) for c in cols)
    m = Image.new('L', im.size, 0)
    p = im.load(); q = m.load(); r = reg.load() if reg else None
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            c = p[x, y]
            if c[3] and c[:4] in cols and (r is None or r[x, y]):
                q[x, y] = 255
    return m


def recolour(im, mapping, reg=None):
    """mapping: {src_rgba: dst_rgba} applied only inside reg."""
    out = im.copy(); p = out.load(); r = reg.load() if reg else None
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            c = p[x, y]
            if c[3] and c in mapping and (r is None or r[x, y]):
                p[x, y] = mapping[c]
    return out


def erase(im, reg):
    out = im.copy(); p = out.load(); r = reg.load()
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            if r[x, y]:
                p[x, y] = CLEAR
    return out


def keep(im, reg):
    return erase(im, mask_not(reg))


def paste(dst, src, x, y):
    """alpha-over paste of hard-alpha src at (x,y) (can be negative)."""
    out = dst.copy()
    out.alpha_composite(src, (0, 0), (0, 0)) if False else None
    tmp = Image.new('RGBA', dst.size, CLEAR)
    tmp.paste(src, (x, y))
    out.alpha_composite(tmp)
    return out


def under(dst, src, x, y):
    """paste src *behind* dst."""
    tmp = Image.new('RGBA', dst.size, CLEAR)
    tmp.paste(src, (x, y))
    tmp.alpha_composite(dst)
    return tmp


def patch(im, x0, y0, rows, legend):
    """ASCII patch. '.' or ' ' keeps the pixel, '_' clears it, other chars map via legend."""
    out = im.copy(); p = out.load()
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch in '. ':
                continue
            x, y = x0 + i, y0 + j
            if not (0 <= x < im.size[0] and 0 <= y < im.size[1]):
                continue
            p[x, y] = CLEAR if ch == '_' else legend[ch]
    return out


def palette_of(im, reg=None):
    p = im.load(); r = reg.load() if reg else None
    s = {}
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            c = p[x, y]
            if c[3] and (r is None or r[x, y]):
                s[c] = s.get(c, 0) + 1
    return s


def lumrank_map(src_cols, ramp):
    """sorted by luminance; spread evenly over ramp (dark->light)."""
    src = sorted(set(src_cols), key=kb.lum)
    n = len(src)
    out = {}
    for i, c in enumerate(src):
        k = 0 if n == 1 else round(i * (len(ramp) - 1) / (n - 1))
        out[c] = ramp[k]
    return out


def blend(c, t, a):
    return tuple(int(round(c[i] * (1 - a) + t[i] * a)) for i in range(3)) + (255,)


def flip(im):
    return im.transpose(Image.FLIP_LEFT_RIGHT)


def crop_part(im, box, reg=None):
    """crop box (x0,y0,x1,y1 exclusive) optionally masked by region polygon in full coords."""
    src = keep(im, reg) if reg else im
    return src.crop(box)


def clean_orphans(im, protect=None):
    """remove single opaque pixels with no opaque 4-neighbours."""
    out = im.copy(); p = out.load(); w, h = im.size
    for y in range(h):
        for x in range(w):
            if p[x, y][3] == 0:
                continue
            n = 0
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                xx, yy = x + dx, y + dy
                if 0 <= xx < w and 0 <= yy < h and p[xx, yy][3]:
                    n += 1
            if n == 0:
                p[x, y] = CLEAR
    return out


def outline_outer(im, col=BLACK, only_missing=True):
    """add a 1px outline where an opaque pixel touches transparency and is not already dark."""
    out = im.copy(); p = im.load(); q = out.load(); w, h = im.size
    for y in range(h):
        for x in range(w):
            if p[x, y][3]:
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                xx, yy = x + dx, y + dy
                if 0 <= xx < w and 0 <= yy < h and p[xx, yy][3] and kb.lum(p[xx, yy]) > 70:
                    q[x, y] = col
                    break
    return out


def shear_rows(im, y_anchor, k, direction=1):
    """lean an object: shift each row above y_anchor by (y_anchor-y)//k pixels (integer row shifts,
    so straight verticals become clean 1:k stairs and horizontals stay crisp)."""
    out = Image.new('RGBA', im.size, CLEAR)
    for y in range(im.size[1]):
        s = max(0, (y_anchor - y)) // k * direction
        row = im.crop((0, y, im.size[0], y + 1))
        out.paste(row, (s, y))
    return out


def dissolve(im, pts):
    """remove a thin line: each listed pixel takes the majority colour of its non-listed
    8-neighbours (transparent if most neighbours are transparent). Iterates inward."""
    out = im.copy(); p = out.load(); w, h = im.size
    todo = set(pts)
    for _ in range(6):
        nxt = set()
        for (x, y) in sorted(todo):
            cnt = {}
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if dx == dy == 0:
                        continue
                    xx, yy = x + dx, y + dy
                    if not (0 <= xx < w and 0 <= yy < h) or (xx, yy) in todo:
                        continue
                    c = p[xx, yy]
                    c = c if c[3] else CLEAR
                    cnt[c] = cnt.get(c, 0) + (2 if dx == 0 or dy == 0 else 1)
            if not cnt:
                nxt.add((x, y)); continue
            best = max(cnt.items(), key=lambda t: t[1])[0]
            p[x, y] = best
        todo = nxt
        if not todo:
            break
    return out


def pts_of(im, cols, box):
    cols = set(cols); p = im.load(); out = []
    for y in range(box[1], box[3] + 1):
        for x in range(box[0], box[2] + 1):
            if p[x, y][3] and p[x, y] in cols:
                out.append((x, y))
    return out


def component(im, seed, stop=lambda c: False, outline_cols=((0, 0, 0, 255),)):
    """flood-fill the connected non-transparent, non-outline region from seed, then add the
    outline pixels that touch it. Returns a new image with only that part."""
    w, h = im.size; p = im.load()
    oc = set(outline_cols)
    seen = set(); st = [seed]
    while st:
        x, y = st.pop()
        if (x, y) in seen or not (0 <= x < w and 0 <= y < h):
            continue
        c = p[x, y]
        if not c[3] or c in oc or stop(c):
            continue
        seen.add((x, y))
        st += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    out = Image.new('RGBA', im.size, CLEAR); q = out.load()
    for (x, y) in seen:
        q[x, y] = p[x, y]
    for (x, y) in list(seen):
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                xx, yy = x + dx, y + dy
                if 0 <= xx < w and 0 <= yy < h and p[xx, yy] in oc:
                    q[xx, yy] = p[xx, yy]
    return out


def reduce_colours(im, n, protect=()):
    """median-cut the opaque colours of im down to n (no dithering); protected colours are kept exactly."""
    prot = set(protect)
    p = im.load(); w, h = im.size
    pix = [(x, y) for y in range(h) for x in range(w) if p[x, y][3] and p[x, y] not in prot]
    if not pix:
        return im
    strip = Image.new('RGB', (len(pix), 1))
    sp = strip.load()
    for i, (x, y) in enumerate(pix):
        sp[i, 0] = p[x, y][:3]
    q = strip.quantize(colors=n, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert('RGB')
    qp = q.load(); out = im.copy(); op = out.load()
    for i, (x, y) in enumerate(pix):
        op[x, y] = qp[i, 0] + (255,)
    return out


def drop_specks(im, min_px=8):
    """remove 8-connected opaque components smaller than min_px (stray bits left after a cut)."""
    out = im.copy(); p = out.load(); w, h = im.size
    seen = set()
    for y in range(h):
        for x in range(w):
            if (x, y) in seen or not p[x, y][3]:
                continue
            comp = []; st = [(x, y)]; seen.add((x, y))
            while st:
                cx, cy = st.pop(); comp.append((cx, cy))
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        nx, ny = cx + dx, cy + dy
                        if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in seen and p[nx, ny][3]:
                            seen.add((nx, ny)); st.append((nx, ny))
            if len(comp) < min_px:
                for (cx, cy) in comp:
                    p[cx, cy] = CLEAR
    return out
