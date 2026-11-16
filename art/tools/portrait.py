"""portrait.py - 48x48 head-and-shoulders busts with swappable expressions.

The bust faces three-quarters RIGHT (toward the message text).  Order:
hair_back -> neck/shoulders -> head -> face features -> hair_front -> extras.
All coordinates are native 48x48; files are saved doubled (96x96).
"""
import numpy as np
from px import Canvas, hx, shift, skin_ramp, ramp

EXPRESSIONS = ['neutral', 'happy', 'smug', 'angry', 'crying', 'shocked', 'deadpan', 'panic', 'sad', 'blush']
INK = (38, 28, 46)
WHITE = (250, 248, 242)
WSH = (196, 204, 224)

JAWS = {
    'soft':  [(10.5, 20), (10.8, 27), (13.5, 32.5), (18.5, 37), (24.5, 39.6), (29, 39.6), (33, 37), (36.4, 32), (38, 26), (38, 20)],
    'sharp': [(10.5, 20), (11.2, 27), (14.5, 33), (20, 38), (26, 41.2), (29, 41.2), (32.5, 37.2), (36, 31.5), (37.6, 25), (38, 20)],
    'broad': [(10, 20), (10.2, 29), (12.5, 35), (17.5, 39.5), (24, 41), (31, 41), (35.5, 38.5), (38.4, 33), (39, 27), (38.6, 20)],
    'long':  [(10.8, 20), (11.2, 28), (14, 34.5), (19.5, 39.5), (25.5, 42.2), (29.5, 42.2), (33, 38.5), (36.2, 32.5), (37.6, 26), (38, 20)],
    'round': [(10, 20), (10.2, 28), (12.6, 33.6), (17.5, 38), (24, 40), (30, 40), (34.6, 37.6), (37.8, 32.6), (38.8, 26), (38.5, 20)],
}
CHIN_Y = {'soft': 39.6, 'sharp': 41.2, 'broad': 41, 'long': 42.2, 'round': 40}


class Bust:
    def __init__(self, spec):
        self.s = s = dict(spec)
        self.c = c = Canvas(48, 48)
        self.skin = skin_ramp(s['skin'])
        c.material('skin', self.skin)
        c.material('hair', ramp(s['hair'], 4, contrast=s.get('hair_contrast', 1.0)))
        for k, v in s.get('mats', {}).items():
            c.material(k, v if isinstance(v, list) else ramp(v, 4))
        self.jaw = s.get('jaw', 'soft')
        self.age = s.get('age', 'teen')
        self.eh = s.get('eye_h', {'teen': 4, 'adult': 3, 'old': 2}[self.age])
        self.ey = s.get('eye_y', {'teen': 23, 'adult': 22, 'old': 22}[self.age])
        self.hair_mask = np.zeros((48, 48), bool)

    # ----------------------------------------------------------------- body
    def head(self):
        c, s = self.c, self.s
        cran = c.m_ell(24, 20, 14, 14)
        jaw = c.m_poly(JAWS[self.jaw])
        mk = cran | jaw
        tone = c.t_sph(26, 24, 15, 19, lo=0.36, hi=0.80)
        tone = np.minimum(tone, 0.80)
        c.paint(mk, 'skin', tone)
        self.head_mask = mk
        # near ear
        c.ell(11.2, 25.5, 2.4, 3.6, 'skin', tone=0.6)
        c.stroke([(11, 24), (11, 26)], tone=0.4)
        c.stroke([(12, 27), (12, 27)], tone=0.4)
        if self.jaw in ('sharp', 'long') or s.get('gaunt'):
            c.stroke([(33, 31), (31, 35)], tone=0.4, only='skin')   # cheek hollow
        if s.get('gaunt'):
            c.stroke([(15, 30), (17, 34)], tone=0.4, only='skin')

    def neck(self):
        c, s = self.c, self.s
        w = s.get('neck_w', 5)
        cy = CHIN_Y[self.jaw]
        c.poly([(24.5 - w, 33), (24.5 + w, 33), (25 + w, 47), (23.5 - w, 47)], 'skin', tone=0.6)
        c.shade(c.m_poly([(24.5 - w, 33), (24.5 + w, 33), (25 + w, cy + 3.2), (23 - w, cy + 1.2)]), -0.25)

    def shoulders(self):
        """Returns the shoulder mask.  Width by build."""
        c, s = self.c, self.s
        b = {'narrow': 0, 'normal': 2, 'broad': 5}[s.get('shoulders', 'normal')]
        top = s.get('shoulder_y', 42)
        pts = [(4 - b, 48), (5 - b, top + 3.5), (9 - b * 0.6, top + 1), (17, top - 1.5), (32, top - 1.5),
               (39 + b * 0.6, top + 1.2), (43 + b, top + 4), (44 + b, 48)]
        mk = c.poly(pts, 'top', lo=0.34, hi=0.9)
        self.sh_mask = mk
        return mk

    # ----------------------------------------------------------------- face
    def eye(self, near, kind, lid=0, slant=0, gaze=1, shine=True, small_iris=False):
        """near eye is the left one.  x,y = top-left of the lash row."""
        c, s = self.c, self.s
        w = 7 if near else 5
        x = 15 if near else 29
        h = self.eh
        y = self.ey + (4 - h) // 2
        iris = hx(s.get('eye', '#5a4632'))
        iris_d = shift(iris, dv=-0.22, ds=0.08, dh=-8)
        lash = s.get('lash_col', INK)
        sk1 = self.skin[1]
        outer, inner = (x, x + w - 1) if near else (x + w - 1, x)
        tilt = s.get('eye_tilt', 0)

        def P(px_, py_, col):
            c.px(px_, py_, col)

        if kind == 'happy':      # ^ arcs
            for i in range(w):
                d = min(i, w - 1 - i)
                P(x + i, y + 2 - min(d, 2) + (1 if d == 0 else 0), lash)
            return
        if kind == 'shut':       # calm closed, u arcs
            for i in range(w):
                d = min(i, w - 1 - i)
                P(x + i, y + 2 + min(d, 1), lash)
            return
        if kind == 'cry':        # > <
            tip = (x + w - 2) if near else (x + 1)
            base = (x + 1) if near else (x + w - 2)
            c.pline([(base, y), (tip, y + 2)], lash)
            c.pline([(base, y + 4), (tip, y + 2)], lash)
            P(base, y + 1 if False else y, lash)
            return
        if kind in ('shock', 'blank'):
            hh = h + 1
            y0 = y - 1
            for i in range(1, w - 1):
                P(x + i, y0, lash)
                P(x + i, y0 + hh + 1, lash if kind == 'blank' else sk1)
            for j in range(1, hh + 1):
                P(x, y0 + j, lash)
                P(x + w - 1, y0 + j, lash)
                for i in range(1, w - 1):
                    P(x + i, y0 + j, WHITE)
            if kind == 'shock':
                cx = x + w // 2 + (0 if near else 0)
                cyy = y0 + 1 + hh // 2
                for i in (0, 1) if near else (0,):
                    P(cx - 1 + i + (0 if near else 1), cyy - 1 if hh > 2 else cyy, iris_d)
                    P(cx - 1 + i + (0 if near else 1), cyy, INK)
            else:
                P(x + w // 2, y0 + 1 + hh // 2, INK)
            return
        # ---- open eye
        top = y + lid
        rows = h - lid
        # lash line
        a, b = (0, w - 2) if near else (1, w - 1)
        if lid:
            a, b = 0, w - 1
        for i in range(a, b + 1):
            P(x + i, top, lash)
        # outer corner drop / lift
        if not lid:
            P(outer, top + 1, lash)
            if tilt > 0:
                P(outer, top - 1 if False else top, lash)
                P(outer + (-1 if near else 1), top - 1, lash) if s.get('lashes') else None
            if s.get('lashes'):
                P(outer + (-1 if near else 1), top, lash)
        if tilt < 0:
            P(outer, top + 2, lash)
        if slant > 0:   # angry: inner end pressed down
            P(inner, top + 1, lash)
            P(inner + (-1 if near else 1), top + 1, lash)
        if slant < 0:   # sad: outer end pressed down
            P(outer, top + 1, lash)
            P(outer, top + 2, lash)
        # eyeball
        iw = (4 if near else 3) - (1 if small_iris else 0)
        ex0, ex1 = (x + 1, x + w - 2) if near else (x, x + w - 2)
        if gaze > 0:
            ix0 = ex1 - iw + 1
        elif gaze < 0:
            ix0 = ex0
        else:
            ix0 = (ex0 + ex1 - iw + 1) // 2
        for j in range(rows):
            yy = top + 1 + j
            for xx in range(ex0, ex1 + 1):
                if slant > 0 and j == 0 and xx in (inner, inner + (-1 if near else 1)):
                    continue
                P(xx, yy, WSH if (j == rows - 1 and rows > 1) or (j == 0 and lid) else WHITE)
            for i in range(iw):
                xx = ix0 + i
                col = iris_d if j == 0 else iris
                if 0 < i < iw - (0 if iw < 4 else 1) and (rows < 3 or 0 < j < rows - (1 if rows > 3 else 0) or rows == 2):
                    col = INK if (j >= (1 if rows > 2 else 0)) else iris_d
                if slant > 0 and j == 0 and xx in (inner, inner + (-1 if near else 1)):
                    continue
                P(xx, yy, col)
        if shine and rows >= 2:
            P(ix0, top + 1 + (1 if rows > 2 else 0), (255, 255, 255))
            if s.get('sparkle') and rows > 3:
                P(ix0 + iw - 1, top + rows, shift(iris, dv=0.25, ds=-0.2))
        # lower lid
        if s.get('lower_lid', True):
            for xx in range(x + 2, x + w - 2 + (0 if near else 1)):
                P(xx, top + rows + 1, sk1)
        if s.get('bags'):
            for xx in range(x + 1, x + w - 1):
                P(xx, top + rows + 2, sk1)

    def brow(self, near, dy_in=0, dy_out=0, lift=0):
        """dy_in / dy_out: vertical offset of the inner / outer end (down = +)."""
        c, s = self.c, self.s
        col = s.get('brow', shift(s['hair'], dv=-0.18))
        base = self.ey - 3 + (4 - self.eh) // 2 - lift + s.get('brow_y', 0)
        r_in, r_out = s.get('rest_brow', (0, 0))
        dy_in += r_in
        dy_out += r_out
        if near:
            p0, p1 = (15, base + dy_out), (21, base + dy_in)
        else:
            p0, p1 = (29, base + dy_in), (33, base + dy_out)
        c.pline([p0, p1], col)
        if s.get('brow_thick'):
            c.pline([(p0[0], p0[1] - 1), (p1[0], p1[1] - 1)], col)

    def nose(self):
        c, s = self.c, self.s
        sk1, sk0 = self.skin[1], self.skin[0]
        y = self.ey + 7 + (1 if self.age != 'teen' else 0)
        if s.get('nose', 'small') == 'small':
            c.pxs([(28, y), (29, y)], sk1)
        elif s['nose'] == 'strong':
            c.pline([(27, y - 5), (28, y - 2)], sk1)
            c.pxs([(29, y - 1), (29, y), (28, y + 1), (27, y + 1), (26, y)], sk1)
            c.px(30, y - 1, self.skin[3])
        else:  # medium
            c.pxs([(28, y - 2), (28, y - 1), (29, y), (28, y + 1), (27, y + 1)], sk1)
        self.nose_y = y

    def mouth(self, kind):
        c, s = self.c, self.s
        mx, my = 26, self.ey + 11 + (1 if self.age != 'teen' else 0) + s.get('mouth_y', 0)
        dark = s.get('lip_dark', (112, 46, 52))
        inside = (126, 40, 52)
        tongue = (226, 112, 112)
        sk1 = self.skin[1]
        lip = s.get('lip')

        def L(pts, col=dark):
            c.pxs(pts, col)

        if kind == 'line':
            L([(mx - 2, my), (mx - 1, my), (mx, my), (mx + 1, my)])
            L([(mx - 1, my + 2), (mx, my + 2)], sk1)
        elif kind == 'smile':
            L([(mx - 3, my - 1), (mx - 2, my), (mx - 1, my), (mx, my), (mx + 1, my), (mx + 2, my - 1)])
            L([(mx - 1, my + 2), (mx, my + 2)], sk1)
        elif kind == 'grin':     # open smile
            for i in range(-3, 4):
                L([(mx + i, my - 1)])
            for i in range(-2, 3):
                L([(mx + i, my)], WHITE)
                L([(mx + i, my + 1)], inside)
            L([(mx - 1, my + 2), (mx, my + 2), (mx + 1, my + 2)], tongue)
            L([(mx - 3, my), (mx + 3, my), (mx - 2, my + 2), (mx + 2, my + 2), (mx - 3, my + 1), (mx + 3, my + 1)])
            L([(mx - 1, my + 3), (mx, my + 3), (mx + 1, my + 3)])
        elif kind == 'smirk':
            L([(mx - 2, my), (mx - 1, my), (mx, my), (mx + 1, my), (mx + 2, my - 1), (mx + 3, my - 2)])
            L([(mx + 4, my - 2)], sk1)
            L([(mx - 1, my + 2), (mx, my + 2)], sk1)
        elif kind == 'grit':
            for i in range(-3, 4):
                L([(mx + i, my - 1), (mx + i, my + 2)])
                L([(mx + i, my), (mx + i, my + 1)], WHITE)
            L([(mx - 4, my), (mx - 4, my + 1), (mx + 4, my), (mx + 4, my + 1)])
            L([(mx - 1, my), (mx - 1, my + 1), (mx + 1, my), (mx + 1, my + 1)], WSH)
        elif kind == 'frown':
            L([(mx - 2, my + 1), (mx - 1, my), (mx, my), (mx + 1, my), (mx + 2, my + 1)])
            L([(mx - 1, my + 2), (mx, my + 2)], sk1)
        elif kind == 'snarl':    # angry open frown
            L([(mx - 3, my + 1), (mx - 2, my), (mx - 1, my - 1), (mx, my - 1), (mx + 1, my - 1), (mx + 2, my), (mx + 3, my + 1)])
            L([(mx - 1, my), (mx, my), (mx + 1, my)], WHITE)
            L([(mx - 2, my + 1), (mx - 1, my + 1), (mx, my + 1), (mx + 1, my + 1), (mx + 2, my + 1)], inside)
            L([(mx - 2, my + 2), (mx - 1, my + 2), (mx, my + 2), (mx + 1, my + 2), (mx + 2, my + 2)])
        elif kind == 'wail':     # crying-yelling: big wobbly mouth
            for j in range(0, 5):
                half = [4, 4, 4, 3, 2][j]
                for i in range(-half, half + 1):
                    L([(mx + i, my - 2 + j)], inside)
            for i in range(-3, 4):
                L([(mx + i, my - 2)], WHITE)
            L([(mx - 1, my + 1), (mx, my + 1), (mx + 1, my + 1), (mx - 2, my + 2), (mx - 1, my + 2), (mx, my + 2), (mx + 1, my + 2)], tongue)
            for i in range(-4, 5):
                L([(mx + i, my - 3)])
            L([(mx - 5, my - 2), (mx - 5, my - 1), (mx - 5, my), (mx + 5, my - 2), (mx + 5, my - 1), (mx + 5, my),
               (mx - 4, my + 1), (mx + 4, my + 1), (mx - 3, my + 2), (mx + 3, my + 2),
               (mx - 2, my + 3), (mx - 1, my + 3), (mx, my + 3), (mx + 1, my + 3), (mx + 2, my + 3)])
        elif kind == 'o':
            L([(mx - 1, my - 1), (mx, my - 1), (mx - 2, my), (mx + 1, my), (mx - 2, my + 1), (mx + 1, my + 1), (mx - 1, my + 2), (mx, my + 2)])
            L([(mx - 1, my), (mx, my), (mx - 1, my + 1), (mx, my + 1)], inside)
        elif kind == 'flat':
            L([(mx + i, my) for i in range(-3, 3)])
        elif kind == 'wobble':   # panic: zigzag box with teeth
            for i in range(-4, 5):
                L([(mx + i, my - 1 + (i % 2)), (mx + i, my + 2 + (i % 2))])
                L([(mx + i, my + (i % 2))], WHITE)
                L([(mx + i, my + 1 + (i % 2))], inside)
            L([(mx - 5, my), (mx - 5, my + 1), (mx + 5, my), (mx + 5, my + 1)])
        elif kind == 'wavy':     # blush: tiny squiggle
            L([(mx - 2, my), (mx - 1, my + 1), (mx, my), (mx + 1, my + 1), (mx + 2, my)])
        if lip and kind in ('line', 'smile', 'smirk', 'flat', 'frown'):
            L([(mx - 1, my + 1), (mx, my + 1)], lip)

    def expression(self, expr):
        c, s = self.c, self.s
        E, B, M = self.eye, self.brow, self.mouth
        sk = self.skin
        tear = (150, 208, 248)
        tear_l = (222, 242, 255)
        blush = s.get('blush_col', shift(sk[1], ds=0.12, dh=-12, dv=0.06))
        if s.get('masked'):
            return self.mask_face(expr)
        if expr == 'neutral':
            E(1, 'open'); E(0, 'open'); B(1); B(0); M(s.get('rest_mouth', 'line'))
        elif expr == 'happy':
            E(1, 'happy'); E(0, 'happy'); B(1, lift=1); B(0, lift=1); M('grin')
            c.pxs([(16, self.ey + 6), (17, self.ey + 6), (33, self.ey + 6), (34, self.ey + 6)], blush)
        elif expr == 'smug':
            E(1, 'open', lid=max(1, self.eh // 2), gaze=1, shine=False); E(0, 'open', lid=max(1, self.eh // 2), shine=False)
            B(1, dy_in=1, dy_out=-1); B(0, dy_in=-1, dy_out=-2, lift=1); M('smirk')
        elif expr == 'angry':
            E(1, 'open', slant=1); E(0, 'open', slant=1)
            B(1, dy_in=3, dy_out=-1); B(0, dy_in=3, dy_out=-1); M('snarl')
            c.pxs([(24, self.ey), (25, self.ey - 1), (26, self.ey)], sk[1])  # knitted brow crease
        elif expr == 'crying':
            E(1, 'cry'); E(0, 'cry'); B(1, dy_in=-2, dy_out=1); B(0, dy_in=-2, dy_out=1); M('wail')
            for (x0, x1) in ((17, 18), (31, 32)):
                for y in range(self.ey + 5, self.ey + 15):
                    if not c.head_ok(x0, y):
                        break
                    c.px(x0, y, tear_l if (y % 3) else tear)
                    c.px(x1, y, tear)
            c.pxs([(14, self.ey + 3), (22, self.ey + 3), (28, self.ey + 3), (34, self.ey + 3)], tear_l)
        elif expr == 'shocked':
            E(1, 'shock'); E(0, 'shock'); B(1, lift=3); B(0, lift=3); M('o')
        elif expr == 'deadpan':
            E(1, 'open', lid=max(1, self.eh - 2), gaze=0, shine=False); E(0, 'open', lid=max(1, self.eh - 2), gaze=0, shine=False)
            B(1, lift=-1); B(0, lift=-1); M('flat')
        elif expr == 'panic':
            E(1, 'blank'); E(0, 'blank'); B(1, dy_in=-2, dy_out=0, lift=3); B(0, dy_in=-2, dy_out=0, lift=3); M('wobble')
            # blue dread on the brow
            gl = (120, 132, 190)
            for x in range(13, 37, 2):
                for y in range(self.ey - 12, self.ey - 7 + (x % 4)):
                    if c.head_ok(x, y) and c.ovr[y, x, 3] == 0 and c.mat[y, x] == c.m('skin'):
                        c.px(x, y, gl)
        elif expr == 'sad':
            E(1, 'open', lid=1, slant=-1, gaze=0); E(0, 'open', lid=1, slant=-1, gaze=0)
            B(1, dy_in=-2, dy_out=1); B(0, dy_in=-2, dy_out=1); M('frown')
        elif expr == 'blush':
            E(1, 'open', gaze=-1); E(0, 'open', gaze=-1); B(1, dy_in=-1, lift=1); B(0, dy_in=-1, lift=1); M('wavy')
            for bx in (14, 17, 20, 30, 33):
                c.pline([(bx, self.ey + 7), (bx + 1, self.ey + 6)], blush)
            c.pxs([(x, self.ey + 8) for x in range(14, 22)] + [(x, self.ey + 8) for x in range(30, 35)], shift(sk[2], ds=0.12, dh=-10))
        else:
            raise KeyError(expr)

    def mask_face(self, expr):
        """Masked speakers: expression carried by the eye slits only."""
        self.s['mask_fn'](self, expr)

    # ---------------------------------------------------------------- build
    def build(self, expr='neutral'):
        c, s = self.c, self.s
        c.head_ok = lambda x, y: 0 <= x < 48 and 0 <= y < 48 and self.head_mask[y, x] and not self.hair_mask[y, x]
        if s.get('hair_back'):
            s['hair_back'](self)
        self.neck()
        self.shoulders()
        if s.get('outfit'):
            s['outfit'](self)
        self.head()
        if s.get('under_face'):
            s['under_face'](self)
        self.nose()
        # hair first into a scratch mask so tears etc. know where skin shows
        if s.get('hair_front'):
            before = c.mat.copy()
            s['hair_front'](self)
            self.hair_mask = (c.mat != before)
            # cast shadow: skin directly below the fringe drops one tone
            sk = (c.mat == c.m('skin')) & self.head_mask
            up1 = np.zeros_like(sk); up1[1:] = self.hair_mask[:-1]
            up2 = np.zeros_like(sk); up2[2:] = self.hair_mask[:-2]
            c.tone[sk & (up1 | up2)] = 0.4
            # far-side form shadow down the right contour of the face
            edge = np.zeros_like(sk); edge[:, :-2] = ~self.head_mask[:, 2:]
            rows = np.zeros_like(sk); rows[self.ey + 3:, :] = True
            c.tone[sk & edge & rows & (c.xx > 30)] = 0.4
        # face features are override pixels; they must not sit on top of hair
        self._features(expr)
        if s.get('over_face'):
            s['over_face'](self, expr)
        return c.render()

    def _features(self, expr):
        c = self.c
        ov_before = c.ovr.copy()
        self.expression(expr)
        if self.s.get('extras'):
            self.s['extras'](self, expr)
        # hide feature pixels that landed on hair (fringe covers eyes/brows)
        cover = self.hair_mask & ~self.s.get('see_through', np.zeros((48, 48), bool))
        if self.s.get('fringe_over_brows', True):
            c.ovr[cover] = ov_before[cover]


# ----------------------------------------------------------------- hair kit
def hair_tone(b, mask, lo=0.18, hi=0.92):
    c = b.c
    return c.t_sph(22, 16, 19, 19, lo, hi)


def hair_cap(b, hairline, vol=2.0, top=0.0, left=None, right=None, mat='hair'):
    """Hair covering the skull above `hairline` (points listed left -> right,
    x from ~8 to ~40).  vol = thickness beyond the skull."""
    c = b.c
    outer = c.m_ell(24, 20 - top / 2, 14 + vol, 14 + vol + top / 2)
    pts = [(-2, -2), (50, -2), (50, hairline[-1][1])] + list(reversed(hairline)) + [(-2, hairline[0][1])]
    mk = outer & c.m_poly(pts)
    c.paint(mk, mat, hair_tone(b, mk))
    return mk


def lock(b, pts, lo=None, hi=None, mat='hair', tone=None):
    c = b.c
    mk = c.m_poly(pts)
    if tone is None:
        tone = hair_tone(b, mk)
    c.paint(mk, mat, tone)
    return mk


def shine(b, pts, mat='hair'):
    """Zig-zag highlight band: list of (x, y) pixel runs."""
    c = b.c
    for i in range(len(pts) - 1):
        c.stroke([pts[i], pts[i + 1]], tone=0.95, only=mat)
        c.stroke([(pts[i][0], pts[i][1] + 1), (pts[i + 1][0], pts[i + 1][1] + 1)], tone=0.95, only=mat)


def strands(b, lines, mat='hair'):
    for ln in lines:
        b.c.stroke(ln, line=True, only=mat)


def render_set(spec, exprs=None):
    out = {}
    for e in exprs or EXPRESSIONS:
        out[e] = Bust(spec).build(e)
    return out
