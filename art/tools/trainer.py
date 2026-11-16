"""trainer.py - 64x64 (saved 128x128) battle front sprites.

A figure is a posed skeleton (joints in native pixels) dressed in tapered
capsule limbs and garment polygons, facing three-quarters LEFT like the stock
fronts.  Per-character closures add hair, face and signature details.
"""
import numpy as np
from px import Canvas, hx, shift, skin_ramp, ramp

INK = (38, 28, 46)
GX, GY = 33, 61

POSES = {
    # arms: (elbow dx,dy, hand dx,dy, drawn over torso?)  L = viewer's left (far) arm
    'ball':    dict(lean=-2, feet=(-5.5, 4.5), L=(-5, 5, -10, 3, False), R=(4.5, 6.5, 2, 12, True), held='L'),
    'relaxed': dict(lean=0, feet=(-3, 3), L=(-2, 7, -2.5, 14, False), R=(2, 7, 2.5, 14, True)),
    'crossed': dict(lean=0, feet=(-4, 4), L=(-2.5, 7, 5, 6.5, True), R=(3, 7.5, -5, 8, True)),
    'cane':    dict(lean=-1, feet=(-3.5, 4), L=(-3, 6.5, -8, 11, False), R=(3, 7, 2, 13.5, True), held='L'),
    'raise':   dict(lean=0, feet=(-3.5, 3.5), L=(-5.5, 3.5, -8.5, -3, False), R=(2.5, 7, 2.5, 14, True), held='L'),
    'hips':    dict(lean=0, feet=(-5, 5), L=(-5.5, 6, -2, 11.5, True), R=(5.5, 6, 2, 11.5, True)),
    'clasp':   dict(lean=0, feet=(-2.5, 2.5), L=(-3, 7, 0.5, 10, True), R=(3.5, 7, -0.5, 10.5, True)),
    'fist':    dict(lean=-2, feet=(-6, 5), L=(-6, 3, -8, -3, False), R=(4.5, 5, -1, 5, True)),
    'point':   dict(lean=-1, feet=(-5, 4.5), L=(-6, 1.5, -12, 0, False), R=(4, 7, 4, 13, True)),
    'chin':    dict(lean=0, feet=(-3, 3.5), L=(-3.5, 7, 3.5, 8.5, True), R=(4.5, 7.5, -1, 0.5, True)),
    'lantern': dict(lean=0, feet=(-3, 3), L=(-4.5, 5.5, -8.5, 6, False), R=(2, 7, 2, 14, True), held='L'),
    'stoop':   dict(lean=-3, feet=(-3.5, 4), L=(-3, 6, -6.5, 11, False), R=(3, 6.5, 2.5, 13, True), held='L'),
}


class Fig:
    def __init__(self, spec):
        self.s = s = dict(spec)
        self.c = c = Canvas(64, 64)
        self.skin = skin_ramp(s['skin'])
        c.material('skin', self.skin)
        c.material('hair', ramp(s['hair'], 4, contrast=s.get('hair_contrast', 1.0)))
        mats = dict(legs='#4a4e62', shoes='#3a3440')
        mats.update(s.get('mats', {}))
        for k, v in mats.items():
            c.material(k, v if isinstance(v, list) else ramp(v, 4 if k in ('top', 'coat', 'legs') else 3))
        self.H = H = s.get('H', 52)
        self.sw = s.get('sw', 6.2)       # shoulder half width
        self.hw = s.get('hw', 4.6)       # hip half width
        self.ra = s.get('ra', 1.9)       # arm radius
        self.rl = s.get('rl', 2.6)       # leg radius
        self.hr = s.get('head', (5.4, 6.0))
        self.pose = p = dict(POSES[s.get('pose', 'ball')])
        k = H / 52.0
        gx = GX + s.get('dx', 0)
        lean = p['lean'] + s.get('lean', 0)
        J = {}
        J['hip'] = (gx, GY - 0.47 * H)
        J['sh'] = (gx + lean, GY - 0.775 * H)
        J['waist'] = (gx + lean * 0.4, GY - 0.57 * H)
        J['head'] = (gx + lean * 1.3 - 0.5 + s.get('head_dx', 0), GY - H + self.hr[1] + 0.5)
        J['shL'] = (J['sh'][0] - self.sw, J['sh'][1] + 1.2)
        J['shR'] = (J['sh'][0] + self.sw, J['sh'][1] + 1.6)
        for side in 'LR':
            ex, ey, hx_, hy_, over = p[side]
            sx, sy = J['sh' + side]
            J['el' + side] = (sx + ex * k, sy + ey * k)
            J['ha' + side] = (sx + hx_ * k, sy + hy_ * k)
        fl, fr = p['feet']
        J['hipL'] = (J['hip'][0] - self.hw * 0.5, J['hip'][1])
        J['hipR'] = (J['hip'][0] + self.hw * 0.5, J['hip'][1])
        J['anL'] = (gx + fl * k, GY - 2.2)
        J['anR'] = (gx + fr * k, GY - 1.4)
        J['knL'] = ((J['hipL'][0] + J['anL'][0]) / 2 - 0.8, GY - 0.25 * H)
        J['knR'] = ((J['hipR'][0] + J['anR'][0]) / 2 - 0.3, GY - 0.245 * H)
        self.J = J

    # ------------------------------------------------------------ pieces
    def leg(self, side):
        c, J, s = self.c, self.J, self.s
        bare = s.get('legs', 'trousers') in ('shorts', 'skirt', 'dress') and not s.get('tights')
        mat = 'skin' if bare else ('tights' if s.get('tights') else 'legs')
        r = self.rl * (0.82 if mat != 'legs' else 1.0)
        wide = s.get('leg_flare', 0)
        c.limb([J['hip' + side], J['kn' + side], J['an' + side]], [r, r * 0.86 + wide * 0.3, r * 0.72 + wide], mat)
        ax, ay = J['an' + side]
        if s.get('barefoot'):
            c.cap((ax + 0.5, ay + 1.2), (ax - 2.2, ay + 1.6), 1.3, 1.1, 'skin')
        else:
            c.cap((ax + 0.8, ay + 1.0), (ax - 2.6, ay + 1.6), 1.9, 1.6, 'shoes', lo=0.25, hi=0.9)
            if s.get('boots'):
                c.cap((ax, ay - s['boots']), (ax, ay), r * 0.72 + 0.3, r * 0.72 + 0.2, 'shoes')
        if s.get('legs') == 'shorts':
            hx_, hy_ = J['hip' + side]
            kx, ky = J['kn' + side]
            t = s.get('shorts_len', 0.55)
            c.cap((hx_, hy_), (hx_ + (kx - hx_) * t, hy_ + (ky - hy_) * t), self.rl + 0.4, self.rl + 0.6, 'legs')

    def torso(self):
        c, J, s = self.c, self.J, self.s
        sx, sy = J['sh']
        wx, wy = J['waist']
        hx_, hy_ = J['hip']
        ww = s.get('ww', self.hw * 0.92)
        pts = [(sx - self.sw - 0.6, sy + 0.6), (sx - self.sw * 0.5, sy - 1.2), (sx + self.sw * 0.5, sy - 1.0), (sx + self.sw + 0.6, sy + 1.2),
               (wx + ww, wy), (hx_ + self.hw, hy_ + 1.5), (hx_ - self.hw, hy_ + 1.5), (wx - ww, wy)]
        mk = c.poly(pts, 'top', lo=0.3, hi=0.92)
        self.torso_mask = mk
        return mk

    def skirt(self, hem, flare, mat='top', open_front=False, top_y=None):
        """Garment hanging from the waist to height `hem` (fraction of H above ground)."""
        c, J = self.c, self.J
        wx, wy = J['waist']
        hx_, hy_ = J['hip']
        ty = wy if top_y is None else top_y
        ww = self.s.get('ww', self.hw * 0.92)
        y1 = GY - hem * self.H
        pts = [(wx - ww - 0.3, ty), (wx + ww + 0.3, ty), (hx_ + self.hw + 0.6, hy_), (hx_ + self.hw + flare, y1),
               (hx_ - self.hw - flare * 0.8, y1 - 0.8), (hx_ - self.hw - 0.6, hy_)]
        mk = c.poly(pts, mat, lo=0.25, hi=0.9)
        # a couple of long folds
        c.stroke([(hx_ + self.hw * 0.4, hy_ + 2), (hx_ + self.hw * 0.4 + flare * 0.5, y1 - 1)], dt=-0.3, only=mat)
        c.stroke([(hx_ - self.hw * 0.5, hy_ + 3), (hx_ - self.hw * 0.5 - flare * 0.45, y1 - 2)], dt=0.25, only=mat)
        if open_front:
            c.stroke([(wx - 1, ty), (hx_ - 1.5 - flare * 0.2, y1 - 1)], line=True, only=mat)
        return mk

    def arm(self, side):
        c, J, s = self.c, self.J, self.s
        mat = s.get('sleeve', 'top')
        ra = self.ra
        sh, el, ha = J['sh' + side], J['el' + side], J['ha' + side]
        sl = s.get('sleeve_len', 1.0)   # 1 = to the wrist, 0.5 = to the elbow, 0 = bare
        cuff = s.get('cuff', 0)
        if sl < 1.0:
            c.limb([sh, el, ha], [ra * 0.9, ra * 0.82, ra * 0.7], 'skin')
            if sl > 0:
                t = min(1.0, sl * 2)
                c.cap(sh, (sh[0] + (el[0] - sh[0]) * t, sh[1] + (el[1] - sh[1]) * t), ra + 0.3, ra + 0.2, mat)
        else:
            c.limb([sh, el, ha], [ra + 0.3, ra + cuff * 0.5, ra * 0.85 + cuff], mat)
            # elbow crease
            c.stroke([(el[0] + 1, el[1] - 1), (el[0] + 1, el[1] + 1)], dt=-0.3, only=mat)
        c.ell(ha[0], ha[1], 1.9, 1.9, s.get('glove_' + side, s.get('gloves', 'skin')), lo=0.35, hi=0.9)

    def neck(self):
        c, J = self.c, self.J
        hx_, hy_ = J['head']
        sx, sy = J['sh']
        c.cap((hx_ + 0.8, hy_ + self.hr[1] - 1.5), (sx + 0.3, sy - 0.5), 1.7, 2.0, 'skin', lo=0.15, hi=0.6)

    def head(self):
        c, J, s = self.c, self.J, self.s
        hx_, hy_ = J['head']
        rx, ry = self.hr
        cran = c.m_ell(hx_, hy_ - 0.6, rx, ry - 0.6)
        jaw = c.m_poly([(hx_ - rx + 0.3, hy_), (hx_ - rx + 0.9, hy_ + 2.6), (hx_ - 2.6, hy_ + ry - 0.4 + s.get('chin', 0)),
                        (hx_ + 0.6, hy_ + ry + s.get('chin', 0)), (hx_ + rx - 1.2, hy_ + 3.2), (hx_ + rx, hy_)])
        mk = cran | jaw
        tone = c.t_sph(hx_ + 1, hy_ + 1, rx + 2, ry + 3, lo=0.36, hi=0.80)
        c.paint(mk, 'skin', np.minimum(tone, 0.8))
        self.head_mask = mk
        # ear on the near (right) side
        c.ell(hx_ + rx - 0.8, hy_ + 1.2, 1.2, 1.6, 'skin', tone=0.42)

    def face(self):
        c, J, s = self.c, self.J, self.s
        hx_, hy_ = J['head']
        x0 = int(round(hx_))
        y0 = int(round(hy_)) + s.get('face_y', 0)
        iris = hx(s.get('eye', '#4a3a30'))
        eh = s.get('eye_h', 2)
        lash = INK
        fx, nx = x0 - 4, x0 - 1      # far eye column, near eye column
        for (ex, near) in ((fx, False), (nx, True)):
            if eh >= 2:
                c.px(ex, y0, lash)
                c.px(ex, y0 + 1, shift(iris, dv=-0.1))
                if eh == 3:
                    c.px(ex, y0 - 1, lash)
                if near:
                    c.px(ex + 1, y0, lash)
                    c.px(ex + 1, y0 + 1, (250, 248, 242))
                    if eh == 3:
                        c.px(ex + 1, y0 - 1, lash)
            else:
                c.px(ex, y0, lash)
                if near:
                    c.px(ex + 1, y0, lash)
        brow = s.get('brow', shift(s['hair'], dv=-0.15))
        bt = s.get('brow_t', 0)       # 0 none, 1 flat, 2 scowl, 3 worried
        by = y0 - (2 if eh < 3 else 3)
        if bt == 1:
            c.pxs([(fx, by), (nx, by), (nx + 1, by)], brow)
        elif bt == 2:
            c.pxs([(fx, by + 1) if eh < 2 else (fx, by), (fx - 1, by - 1), (nx - 1, by), (nx, by), (nx + 1, by - 1)], brow)
        elif bt == 3:
            c.pxs([(fx, by - 1), (fx - 1, by), (nx, by - 1), (nx + 1, by)], brow)
        m = s.get('mouth_t', 'line')
        my = y0 + 4
        dark = (128, 60, 60)
        if m == 'line':
            c.pxs([(x0 - 3, my), (x0 - 2, my)], dark)
        elif m == 'smile':
            c.pxs([(x0 - 4, my - 1), (x0 - 3, my), (x0 - 2, my), (x0 - 1, my - 1)], dark)
        elif m == 'open':
            c.pxs([(x0 - 3, my), (x0 - 2, my)], (140, 50, 60)); c.pxs([(x0 - 3, my - 1), (x0 - 2, my - 1)], dark)
        elif m == 'frown':
            c.pxs([(x0 - 4, my), (x0 - 3, my - 1), (x0 - 2, my - 1), (x0 - 1, my)], dark)
        if s.get('nose_t', 1):
            c.px(x0 - 4, y0 + 2, self.skin[1])
            if s.get('nose_t') == 2:
                c.px(x0 - 4, y0 + 1, self.skin[1]); c.px(x0 - 5, y0 + 2, self.skin[1])
        self.face_xy = (x0, y0)

    def ball(self, at=None):
        c = self.c
        x, y = at or self.J['ha' + self.pose.get('held', 'L')]
        x, y = int(round(x)) - 2, int(round(y)) - 3
        rows = ["..rr..", ".rRRr.", "kkwwkk", ".WwwW.", "..WW.."]
        c.stamp([".rRr.", "rRRRr", "kkwkk", "WWWWw", ".Www."], x, y,
                {'r': (206, 60, 56), 'R': (238, 104, 88), 'k': (50, 40, 54), 'w': (206, 206, 220), 'W': (250, 250, 250)})

    # ------------------------------------------------------------- build
    def build(self):
        c, s, J, p = self.c, self.s, self.J, self.pose
        call = lambda k: s[k](self) if s.get(k) else None
        call('behind')                       # capes, back hair, long braids
        for side in 'LR':
            if not p[side][4]:
                self.arm(side)
        if s.get('legs', 'trousers') != 'robe':
            self.leg('L'); self.leg('R')
        self.torso()
        call('garment')                      # coats, skirts, aprons
        self.neck()
        call('collar')
        self.head()
        self.face()
        call('hairdo')
        for side in 'LR':
            if p[side][4]:
                self.arm(side)
        call('detail')
        if s.get('ball', True) and p.get('held'):
            self.ball()
        return c.render()


# ---------------------------------------------------------------- hair kit
def hcap(f, line, vol=1.0, top=0.0, mat='hair'):
    """Hair over the skull above a hairline given as (dx, dy) offsets from the
    head centre, listed left -> right."""
    c = f.c
    hx_, hy_ = f.J['head']
    rx, ry = f.hr
    outer = c.m_ell(hx_, hy_ - 0.6 - top / 2, rx + vol, ry - 0.6 + vol + top / 2)
    pts = [(hx_ + dx, hy_ + dy) for dx, dy in line]
    poly = [(-2, -2), (66, -2), (66, pts[-1][1])] + list(reversed(pts)) + [(-2, pts[0][1])]
    mk = outer & c.m_poly(poly)
    c.paint(mk, mat, c.t_sph(hx_ - 1, hy_ - 2, rx + 3, ry + 3, lo=0.18, hi=0.95))
    return mk


def hlock(f, pts, mat='hair', lo=0.18, hi=0.95, tone=None):
    c = f.c
    hx_, hy_ = f.J['head']
    P = [(hx_ + dx, hy_ + dy) for dx, dy in pts]
    mk = c.m_poly(P)
    c.paint(mk, mat, c.t_sph(hx_ - 1, hy_ - 2, f.hr[0] + 3, f.hr[1] + 3, lo, hi) if tone is None else tone)
    return mk


def hblob(f, dx, dy, rx, ry, mat='hair', tone=None, edge=False):
    c = f.c
    hx_, hy_ = f.J['head']
    c.ell(hx_ + dx, hy_ + dy, rx, ry, mat, tone=c.t_sph(hx_ - 1, hy_ - 2, f.hr[0] + 4, f.hr[1] + 5, 0.15, 0.95) if tone is None else tone, edge=edge)


def hpx(f, pts, tone=0.95, mat='hair'):
    hx_, hy_ = f.J['head']
    for dx, dy in pts:
        x, y = int(round(hx_ + dx)), int(round(hy_ + dy))
        if 0 <= x < 64 and 0 <= y < 64 and f.c.mat[y, x] == f.c.m(mat):
            f.c.tone[y, x] = tone
            f.c.line[y, x] = False
