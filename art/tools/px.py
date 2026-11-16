"""px.py - tiny pixel-art rasteriser for Prismfall character art.

A Canvas stores, per native pixel, a material id and a tone (0..1).  Shapes
write both; render() maps tone -> the material's colour ramp (hard bands, no
dithering), then adds a selective outline.  Explicit RGB pixels (faces, eyes)
go on an override layer.  Everything is drawn at native resolution and
nearest-neighbour doubled on save, the same way the stock sprites are stored.
"""
import colorsys
import numpy as np
from PIL import Image

LIGHT = np.array([-0.55, -0.83])  # light comes from the upper left


def hx(c):
    if isinstance(c, str):
        c = c.lstrip('#')
        return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))
    return tuple(c)


def shift(rgb, dv=0.0, ds=0.0, dh=0.0):
    """Move a colour in HSV; dh is degrees."""
    r, g, b = [v / 255.0 for v in hx(rgb)]
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    h = (h + dh / 360.0) % 1.0
    s = min(1.0, max(0.0, s + ds))
    v = min(1.0, max(0.0, v + dv))
    return tuple(int(round(c * 255)) for c in colorsys.hsv_to_rgb(h, s, v))


def _toward(h, target, amount):
    d = ((target - h + 180) % 360) - 180
    if abs(d) < amount:
        return target
    return (h + amount * (1 if d > 0 else -1)) % 360


def ramp(base, n=4, contrast=1.0, cool=255.0, warm=48.0):
    """[darkest .. lightest] ramp around `base` with hue-shifted shadows
    (toward blue-violet) and highlights (toward yellow).  The base colour sits
    at index n-2."""
    r, g, b = [v / 255.0 for v in hx(base)]
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    h *= 360
    out = []
    for i in range(n):
        k = i - (n - 2)  # negative = shadow steps, +1 = light
        if k < 0:
            hh = _toward(h, cool, 9 * -k) if s > 0.08 else cool
            ss = min(1.0, s + 0.07 * -k + (0.06 if s <= 0.08 else 0))
            vv = v * (1 - 0.21 * contrast) ** (-k)
        elif k == 0:
            hh, ss, vv = h, s, v
        else:
            hh = _toward(h, warm, 8)
            ss = max(0.0, s - 0.14)
            vv = min(1.0, v + 0.12 * contrast + (1 - v) * 0.25)
        out.append(tuple(int(round(c * 255)) for c in colorsys.hsv_to_rgb(hh / 360.0, ss, vv)))
    return out


def skin_ramp(base):
    """Skin gets redder, more saturated shadows."""
    r, g, b = [v / 255.0 for v in hx(base)]
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    h *= 360
    out = []
    for k, (dh, ds, dv) in enumerate([(-16, 0.20, 0.60), (-9, 0.11, 0.80), (0, 0, 1.0), (5, -0.10, 1.10)]):
        out.append(tuple(int(round(c * 255)) for c in
                         colorsys.hsv_to_rgb(((h + dh) % 360) / 360.0, min(1, max(0, s + ds)), min(1, v * dv))))
    return out


class Canvas:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.mat = np.full((h, w), -1, np.int16)
        self.tone = np.zeros((h, w), np.float32)
        self.line = np.zeros((h, w), bool)        # forced darkest tone
        self.ovr = np.zeros((h, w, 4), np.uint8)  # explicit pixels
        self.yy, self.xx = np.mgrid[0:h, 0:w].astype(np.float32)
        self.ramps = []
        self.names = {}

    # ---- materials -------------------------------------------------------
    def material(self, name, colours):
        """colours: a base colour (ramp is derived) or an explicit ramp list."""
        if name in self.names:
            return self.names[name]
        if isinstance(colours, (list,)) and isinstance(colours[0], (tuple, list, str)) and len(colours) >= 3 \
                and not isinstance(colours[0], int):
            r = [hx(c) for c in colours]
        else:
            r = ramp(colours)
        self.ramps.append(r)
        self.names[name] = len(self.ramps) - 1
        return self.names[name]

    def m(self, name):
        return self.names[name]

    # ---- masks -----------------------------------------------------------
    def m_poly(self, pts):
        """Even-odd polygon fill sampled at pixel centres."""
        x, y = self.xx + 0.5, self.yy + 0.5
        inside = np.zeros((self.h, self.w), bool)
        n = len(pts)
        for i in range(n):
            x0, y0 = pts[i]
            x1, y1 = pts[(i + 1) % n]
            if y0 == y1:
                continue
            cond = ((y0 <= y) & (y < y1)) | ((y1 <= y) & (y < y0))
            xi = x0 + (y - y0) * (x1 - x0) / (y1 - y0)
            inside ^= cond & (x < xi)
        return inside

    def m_ell(self, cx, cy, rx, ry):
        return ((self.xx + 0.5 - cx) / rx) ** 2 + ((self.yy + 0.5 - cy) / ry) ** 2 <= 1.0

    def _seg(self, p0, p1):
        x, y = self.xx + 0.5, self.yy + 0.5
        dx, dy = p1[0] - p0[0], p1[1] - p0[1]
        L2 = dx * dx + dy * dy or 1e-6
        t = np.clip(((x - p0[0]) * dx + (y - p0[1]) * dy) / L2, 0, 1)
        qx, qy = p0[0] + t * dx, p0[1] + t * dy
        return t, x - qx, y - qy

    def m_cap(self, p0, p1, r0, r1=None):
        r1 = r0 if r1 is None else r1
        t, ox, oy = self._seg(p0, p1)
        return np.hypot(ox, oy) <= r0 + (r1 - r0) * t

    # ---- tone fields -----------------------------------------------------
    def t_lin(self, mask, lo=0.3, hi=0.9, d=LIGHT):
        """Linear gradient across the mask's extent along the light direction."""
        if not mask.any():
            return np.zeros_like(self.tone)
        p = -(self.xx * d[0] + self.yy * d[1])  # big = far from light
        a, b = p[mask].min(), p[mask].max()
        k = (p - a) / (b - a + 1e-6)
        return hi + (lo - hi) * k

    def t_cap(self, p0, p1, r0, r1=None, lo=0.2, hi=0.95):
        r1 = r0 if r1 is None else r1
        t, ox, oy = self._seg(p0, p1)
        r = np.maximum(r0 + (r1 - r0) * t, 0.5)
        k = (ox * LIGHT[0] + oy * LIGHT[1]) / r  # +1 = facing the light
        return np.clip(lo + (hi - lo) * (k * 0.5 + 0.55), 0, 1)

    def t_sph(self, cx, cy, rx, ry, lo=0.2, hi=0.95):
        k = ((self.xx + 0.5 - cx) / rx) * LIGHT[0] + ((self.yy + 0.5 - cy) / ry) * LIGHT[1]
        return np.clip(lo + (hi - lo) * (k * 0.5 + 0.55), 0, 1)

    # ---- painting --------------------------------------------------------
    def paint(self, mask, mat, tone=0.6, edge=True, only=None):
        if isinstance(mat, str):
            mat = self.names[mat]
        if only is not None:
            mask = mask & only
        prev_opaque = self.mat >= 0
        self.mat[mask] = mat
        self.tone[mask] = tone[mask] if isinstance(tone, np.ndarray) else tone
        self.line[mask] = False
        self.ovr[mask] = 0
        if edge:
            # where this shape overlaps older paint, darken the older paint just
            # outside the shape's lower/right edge (a 1px contact shadow line
            # belongs to the thing behind) and our own lower/right rim.
            m = mask
            dn = np.zeros_like(m); dn[:-1] = m[1:]      # pixel below is in mask
            rt = np.zeros_like(m); rt[:, :-1] = m[:, 1:]  # pixel right is in mask
            rim = m & ~(dn & rt)                          # our lower/right rim
            below = np.zeros_like(m); below[1:] = prev_opaque[:-1] & ~m[:-1]
            # our rim only becomes a line where something opaque lies beyond it
            nb_dn = np.zeros_like(m); nb_dn[:-1] = (prev_opaque & ~m)[1:]
            nb_rt = np.zeros_like(m); nb_rt[:, :-1] = (prev_opaque & ~m)[:, 1:]
            self.line |= rim & (nb_dn | nb_rt)
        return mask

    def poly(self, pts, mat, tone=None, lo=0.3, hi=0.9, **kw):
        mk = self.m_poly(pts)
        if tone is None:
            tone = self.t_lin(mk, lo, hi)
        return self.paint(mk, mat, tone, **kw)

    def ell(self, cx, cy, rx, ry, mat, tone=None, lo=0.2, hi=0.95, **kw):
        mk = self.m_ell(cx, cy, rx, ry)
        if tone is None:
            tone = self.t_sph(cx, cy, rx, ry, lo, hi)
        return self.paint(mk, mat, tone, **kw)

    def cap(self, p0, p1, r0, r1=None, mat=0, lo=0.2, hi=0.95, **kw):
        mk = self.m_cap(p0, p1, r0, r1)
        return self.paint(mk, mat, self.t_cap(p0, p1, r0, r1, lo, hi), **kw)

    def limb(self, pts, radii, mat, **kw):
        """Chain of tapered capsules through joints."""
        mk = np.zeros((self.h, self.w), bool)
        for i in range(len(pts) - 1):
            mk |= self.cap(pts[i], pts[i + 1], radii[i], radii[i + 1], mat, **kw)
        return mk

    def _linepix(self, pts):
        out = []
        for i in range(len(pts) - 1):
            (x0, y0), (x1, y1) = pts[i], pts[i + 1]
            n = int(max(abs(x1 - x0), abs(y1 - y0))) or 1
            for k in range(n + 1):
                out.append((int(round(x0 + (x1 - x0) * k / n)), int(round(y0 + (y1 - y0) * k / n))))
        return out

    def stroke(self, pts, tone=None, dt=None, line=False, mat=None, only=None, new=None):
        """1px polyline.  tone=absolute, dt=relative, line=True forces darkest.
        `only`: restrict to that material; `new`: paint a new material."""
        for x, y in self._linepix(pts):
            if not (0 <= x < self.w and 0 <= y < self.h):
                continue
            if new is not None:
                if only is None or self.mat[y, x] == self.names.get(only, only):
                    self.mat[y, x] = self.names[new] if isinstance(new, str) else new
                    self.tone[y, x] = 0.6 if tone is None else tone
                    self.line[y, x] = False
                    self.ovr[y, x] = 0
                continue
            if self.mat[y, x] < 0:
                continue
            if only is not None and self.mat[y, x] != (self.names[only] if isinstance(only, str) else only):
                continue
            if line:
                self.line[y, x] = True
            elif tone is not None:
                self.tone[y, x] = tone
            elif dt is not None:
                self.tone[y, x] = np.clip(self.tone[y, x] + dt, 0, 1)

    def px(self, x, y, rgb, a=255):
        x, y = int(x), int(y)
        if 0 <= x < self.w and 0 <= y < self.h:
            self.ovr[y, x] = (*hx(rgb), a)

    def pxs(self, pts, rgb):
        for x, y in pts:
            self.px(x, y, rgb)

    def pline(self, pts, rgb):
        for x, y in self._linepix(pts):
            self.px(x, y, rgb)

    def stamp(self, rows, x, y, legend, flip=False):
        """ASCII stamp.  legend: char -> rgb, or ('m', material, tone)."""
        for j, row in enumerate(rows):
            if flip:
                row = row[::-1]
            for i, ch in enumerate(row):
                if ch in '. ' or ch not in legend:
                    continue
                v = legend[ch]
                X, Y = x + i, y + j
                if not (0 <= X < self.w and 0 <= Y < self.h):
                    continue
                if isinstance(v, tuple) and len(v) == 3 and v[0] == 'm':
                    self.mat[Y, X] = self.names[v[1]] if isinstance(v[1], str) else v[1]
                    self.tone[Y, X] = v[2]
                    self.line[Y, X] = False
                    self.ovr[Y, X] = 0
                else:
                    self.px(X, Y, v)

    def shade(self, mask, dt):
        mk = mask & (self.mat >= 0)
        self.tone[mk] = np.clip(self.tone[mk] + dt, 0, 1)

    # ---- output ----------------------------------------------------------
    BANDS = {3: (0.36, 0.80), 4: (0.24, 0.47, 0.83), 5: (0.18, 0.36, 0.56, 0.84)}

    def render(self, outline=True, ink=(26, 20, 34)):
        h, w = self.h, self.w
        img = np.zeros((h, w, 4), np.uint8)
        for mi, r in enumerate(self.ramps):
            sel = self.mat == mi
            if not sel.any():
                continue
            idx = np.zeros((h, w), np.int32)
            for th in self.BANDS[len(r)]:
                idx += (self.tone >= th)
            idx[self.line] = 0
            cols = np.array(r, np.uint8)
            img[sel, :3] = cols[idx[sel]]
            img[sel, 3] = 255
        o = self.ovr[..., 3] > 0
        img[o] = self.ovr[o]
        if outline:
            opq = img[..., 3] > 0
            pad = np.pad(opq, 1)
            matp = np.pad(self.mat, 1, constant_values=-1)
            out = np.zeros_like(img)
            done = np.zeros((h, w), bool)
            # neighbour order decides which material tints the outline pixel;
            # 'lit' outline pixels sit above / left of the form (selout).
            for dy, dx, lit in ((1, 0, True), (0, 1, True), (-1, 0, False), (0, -1, False)):
                nb = pad[1 + dy:h + 1 + dy, 1 + dx:w + 1 + dx]
                nm = matp[1 + dy:h + 1 + dy, 1 + dx:w + 1 + dx]
                sel = ~opq & nb & ~done
                for mi, r in enumerate(self.ramps):
                    s2 = sel & (nm == mi)
                    if not s2.any():
                        continue
                    d = np.array(r[0], float)
                    k = 0.62 if lit else 0.38
                    c = d * k + np.array(ink, float) * (1 - k)
                    out[s2, :3] = c.astype(np.uint8)
                    out[s2, 3] = 255
                s3 = sel & (nm < 0)   # neighbour is an override pixel without material
                out[s3, :3] = ink
                out[s3, 3] = 255
                done |= sel
            img[done] = out[done]
        return Image.fromarray(img, 'RGBA')


def save2x(img, path, scale=2):
    img.resize((img.width * scale, img.height * scale), Image.NEAREST).save(path)


def ncolours(img):
    return len(img.convert('RGBA').getcolors(1 << 20))
