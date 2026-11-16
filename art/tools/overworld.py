"""overworld.py - 16x24 native frames, 4 directions x 4 walk frames, saved as
the stock 128x192 charset (rows: down, left, right, up; columns: stand, step,
stand, other step).  Right is the left row mirrored.
"""
import numpy as np
from PIL import Image
from px import Canvas, hx, shift, skin_ramp, ramp

INK = (38, 28, 46)


def R(c, x0, y0, x1, y1):
    m = np.zeros((c.h, c.w), bool)
    m[max(0, int(y0)):int(y1) + 1, max(0, int(x0)):int(x1) + 1] = True
    return m


class OW:
    def __init__(self, spec):
        self.s = dict(spec)

    def canvas(self):
        s = self.s
        c = Canvas(16, 24)
        c.material('skin', skin_ramp(s['skin']))
        c.material('hair', ramp(s['hair'], 3, contrast=s.get('hair_contrast', 1.0)))
        mats = dict(legs='#4a4e62', shoes='#3a3440')
        mats.update(s.get('mats', {}))
        for k, v in mats.items():
            c.material(k, v if isinstance(v, list) else ramp(v, 3))
        return c

    def frame(self, d, f):
        s = self.s
        c = self.canvas()
        step = {0: 0, 1: 1, 2: 0, 3: -1}[f]
        tall = s.get('tall', 0)                 # 0 teen, 1 adult, 2 giant
        broad = s.get('broad', 0)
        bob = 1 if step else 0
        base = 22
        leg_top = base - 2
        tor_top = 15 - tall + bob
        hy = 9.5 - tall + bob                    # head centre
        hx_ = 8.0
        g = s.get('garment', 'trousers')        # trousers | shorts | coat | dress | robe
        top = 'top'
        sleeve = s.get('sleeve', 'top')
        if s.get('sleeve_len', 1.0) <= 0.01:
            sleeve = 'skin'
        legm = 'skin' if (g in ('shorts', 'dress') and not s.get('tights')) else ('tights' if s.get('tights') else 'legs')
        x0, x1 = 5 - broad, 10 + broad
        lit = lambda m: c.t_lin(m, 0.3, 0.95)
        if d in ('down', 'up'):
            sgn = 1 if d == 'down' else -1
            # legs: (x range, lift)
            for side, (lx0, lx1) in enumerate(((x0, 7), (8, x1))):
                fwd = step * sgn == (1 if side == 0 else -1)
                back = step * sgn == (-1 if side == 0 else 1)
                lift = 1 if back else 0
                if g == 'robe':
                    continue
                c.paint(R(c, lx0, leg_top, lx1, base - 1 - lift), legm, 0.6 if side == 0 else 0.4)
                c.paint(R(c, lx0, base - lift, lx1, base - lift), 'shoes', 0.6 if side == 0 else 0.4)
                if s.get('boots') and g != 'robe':
                    c.paint(R(c, lx0, base - 1 - lift, lx1, base - lift), 'shoes', 0.6 if side == 0 else 0.4)
            c.line[leg_top:base, 7] |= (c.mat[leg_top:base, 7] >= 0) & (g not in ('robe',)) & (step == 0)
            # torso
            m = R(c, x0, tor_top, x1, leg_top - 1 + (1 if g == 'shorts' else 0))
            c.paint(m, top, lit(m))
            if g == 'shorts':
                c.paint(R(c, x0, leg_top - 1, x1, leg_top), 'legs', 0.5)
            if g in ('coat', 'dress', 'robe'):
                hem = {'coat': base - 2, 'dress': base - 2, 'robe': base}[g] + s.get('hem', 0)
                gm = R(c, x0 - (1 if g != 'coat' else 0), leg_top - 2, x1 + (1 if g != 'coat' else 0), hem)
                c.paint(gm, s.get('skirt_mat', top), lit(gm))
                if g == 'coat' and d == 'down':
                    c.stroke([(7, tor_top + 2), (7, hem)], line=True, only=top)
                if g == 'robe' and step:
                    c.paint(R(c, x0 if step * sgn > 0 else 8, base, 7 if step * sgn > 0 else x1, base), 'shoes', 0.5)
                if g == 'robe' and not step:
                    c.paint(R(c, x0 + 1, base, x1 - 1, base), 'shoes', 0.4)
            if d == 'down' and s.get('shirt_v'):
                c.paint(R(c, 7, tor_top, 8, tor_top + s['shirt_v'] - 1), s.get('shirt_mat', 'shirt'), 0.7)
            # arms
            for side, ax in enumerate((x0 - 1, x1 + 1)):
                fwd = step * sgn == (-1 if side == 0 else 1)
                bk = step * sgn == (1 if side == 0 else -1)
                a0, a1 = tor_top, tor_top + 3 + (1 if fwd else 0) - (1 if bk else 0)
                c.paint(R(c, ax, a0, ax, a1 - 1), sleeve, 0.38, edge=False)
                c.paint(R(c, ax, a1, ax, a1), s.get('gloves', 'skin'), 0.6, edge=False)
                if s.get('sleeve_len', 1.0) < 1.0 and sleeve != 'skin':
                    c.paint(R(c, ax, a0 + 2, ax, a1), 'skin', 0.6, edge=False)
        else:   # left
            if g != 'robe':
                if step == 0:
                    c.paint(R(c, 6, leg_top, 9, base - 1), legm, 0.55)
                    c.paint(R(c, 5, base, 9, base), 'shoes', 0.55)
                else:
                    a, b = (4, 9) if step > 0 else (5, 10)
                    c.paint(R(c, b - 1, leg_top, b + 1, base - 2), legm, 0.35)       # back leg
                    c.paint(R(c, b, base - 1, b + 2, base - 1), 'shoes', 0.35)
                    c.paint(R(c, a + 1, leg_top, a + 3, base - 1), legm, 0.6)        # front leg
                    c.paint(R(c, a, base, a + 3, base), 'shoes', 0.6)
                if s.get('boots') and step == 0:
                    c.paint(R(c, 6, base - 1, 9, base), 'shoes', 0.55)
            m = R(c, 6 - (1 if broad else 0), tor_top, 9 + (1 if broad else 0), leg_top - 1 + (1 if g == 'shorts' else 0))
            c.paint(m, top, lit(m))
            if g == 'shorts':
                c.paint(R(c, 6, leg_top - 1, 9, leg_top), 'legs', 0.5)
            if g in ('coat', 'dress', 'robe'):
                hem = {'coat': base - 2, 'dress': base - 2, 'robe': base}[g] + s.get('hem', 0)
                gm = R(c, 5, leg_top - 2, 10, hem)
                c.paint(gm, s.get('skirt_mat', top), lit(gm))
                if g == 'robe':
                    c.paint(R(c, 5 if step >= 0 else 6, base, 8 if step >= 0 else 9, base), 'shoes', 0.4)
            ax = 7 - step * 2
            c.paint(R(c, ax, tor_top + 1, ax + 1, tor_top + 3), sleeve, 0.5)
            if s.get('sleeve_len', 1.0) < 1.0 and sleeve != 'skin':
                c.paint(R(c, ax, tor_top + 2, ax + 1, tor_top + 3), 'skin', 0.6, edge=False)
            c.paint(R(c, ax, tor_top + 4, ax + 1, tor_top + 4), s.get('gloves', 'skin'), 0.6)
        if s.get('ow_body'):
            s['ow_body'](c, d, step, tor_top, x0, x1)
        # ---- head
        hxc = hx_ if d != 'left' else 7.5
        head = c.m_ell(hxc, hy, 5.2, 5.0)
        c.paint(head, 'skin', 0.6)
        iy = int(hy + 0.5)
        if d == 'down':
            c.paint(head & R(c, 0, iy + 4, 15, 23), 'skin', 0.4, edge=False)
            for ex in (5, 10):
                c.px(ex, iy, INK); c.px(ex, iy + 1, shift(hx(s.get('eye', '#4a3a30')), dv=-0.15))
            if s.get('ow_mouth'):
                c.px(7, iy + 3, (150, 70, 70)); c.px(8, iy + 3, (150, 70, 70))
        elif d == 'left':
            c.px(4, iy, INK); c.px(4, iy + 1, shift(hx(s.get('eye', '#4a3a30')), dv=-0.15))
            c.paint(head & R(c, 5, iy + 4, 15, 23), 'skin', 0.4, edge=False)
        # ---- hair
        h = dict(fringe=[1, 0, 1, 0, 0, 1, 0, 1, 0, 1], line=-2, sides=1, back=0, vol=1.0, top=0, spikes=[], mat='hair')
        h.update(s.get('ow_hair', {}))
        if not s.get('bald'):
            hm = h['mat']
            outer = c.m_ell(hxc, hy - 0.3 - h['top'] / 2, 5.2 + h['vol'] * 0.6, 5.0 + h['vol'] * 0.7 + h['top'] / 2)
            ht = c.t_sph(hxc - 1, hy - 2, 7, 7, 0.2, 1.0)
            fl = iy + h['line']                  # last fully-haired row on the forehead
            if d == 'down':
                m = outer & R(c, 0, 0, 15, fl)
                for i, extra in enumerate(h['fringe']):
                    if extra:
                        m |= R(c, 3 + i, fl + 1, 3 + i, fl + extra) & head
                if h['sides']:
                    w = 1 if h['sides'] > 3 else 0
                    m |= (R(c, 2, fl, 3, iy + h['sides']) | R(c, 12, fl, 13, iy + h['sides'])) & (c.m_ell(hxc, hy + 1, 6.2, 5 + h['sides']) | R(c, 3 - w, iy + 3, 12 + w, 23))
                c.paint(m, hm, ht)
            elif d == 'up':
                m = outer | (head & True)
                if h['back']:
                    m |= R(c, 3, iy, 12, iy + 4 + h['back'])
                c.paint(m, hm, ht)
            else:
                m = outer & R(c, 0, 0, 15, fl)
                m |= (outer | head) & R(c, 8, 0, 15, iy + 4)
                m |= R(c, 5, fl, 7, fl + 1) & outer & R(c, 6, 0, 15, 23)
                fr = h['fringe']
                for i in range(3):
                    if fr[i]:
                        m |= R(c, 3 + i, fl + 1, 3 + i, fl + fr[i]) & head
                if h['sides'] > 1:
                    m |= R(c, 7, fl, 9, iy + h['sides']) & (head | outer | R(c, 0, iy + 4, 15, 23))
                if h['back']:
                    m |= R(c, 9, iy, 12, iy + 4 + h['back'])
                c.paint(m, hm, ht)
        if not s.get('bald'):
            for dx, dy in h['spikes']:
                if d == 'up':
                    dx = -dx
                if d == 'left' and dx < -1:
                    continue
                X, Y = int(round(hxc + dx)), int(iy + dy)
                if 0 <= X < 16 and 0 <= Y < 24:
                    c.mat[Y, X] = c.m(h['mat']); c.tone[Y, X] = 0.9 if dy < -4 else 0.5; c.line[Y, X] = False
        if s.get('ow_acc'):
            s['ow_acc'](c, d, hxc, iy, step)
        return c.render()

    def sheet(self):
        sh = Image.new('RGBA', (64, 96), (0, 0, 0, 0))
        for row, d in enumerate(('down', 'left', 'right', 'up')):
            for f in range(4):
                im = self.frame('left' if d == 'right' else d, f)
                if d == 'right':
                    im = im.transpose(Image.FLIP_LEFT_RIGHT)
                sh.paste(im, (f * 16, row * 24))
        return sh
