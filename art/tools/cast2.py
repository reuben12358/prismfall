"""cast2.py - data-driven kit + the rest of the early-game cast."""
import numpy as np
from px import shift, ramp, hx
from portrait import hair_cap, lock, shine, strands, hair_tone, INK, WHITE
from trainer import hcap, hlock, hblob, hpx, GY
from overworld import R
from cast import (CAST, add, T, O, FULL, STD, collar_high, v_neck, strap, glasses, freckles, jp, satchel, band, mug)

GOLD = (236, 200, 96)


# ----------------------------------------------------------- portrait kit
def PH(line, vol=2.0, top=0.0, back=(), front=(), blobs_b=(), blobs_f=(), sh=(), st=(), after=None, mat='hair'):
    """Hair as data.  back/front: polygons; blobs: (cx, cy, rx, ry)."""
    def hb(b):
        for cx, cy, rx, ry in blobs_b:
            b.c.ell(cx, cy, rx, ry, mat, tone=hair_tone(b, None, 0.1, 0.8), edge=False)
        for p in back:
            lock(b, p, mat=mat)

    def hf(b):
        hair_cap(b, line, vol=vol, top=top, mat=mat)
        for cx, cy, rx, ry in blobs_f:
            b.c.ell(cx, cy, rx, ry, mat, tone=hair_tone(b, None), edge=False)
        for p in front:
            lock(b, p, mat=mat)
        for s_ in sh:
            shine(b, s_, mat=mat)
        strands(b, st, mat=mat)
        if after:
            after(b)
    return dict(hair_back=hb, hair_front=hf)


def beard(mat='hair', full=True, tone=0.5, stache=True):
    def fn(b):
        c = b.c
        cy = {'soft': 39.6, 'sharp': 41.2, 'broad': 41, 'long': 42.2, 'round': 40}[b.jaw]
        pts = [(10.5, 28), (14, 31), (19, 33.5), (22, 32.5), (30, 32.5), (33, 33.5), (36.5, 30), (38.5, 26), (38.5, 33), (34, cy - 1), (30, cy + 2.5 + (3 if full else 0)),
               (23, cy + 2.5 + (3 if full else 0)), (16, cy - 2), (11.5, 33)]
        mk = c.m_poly(pts) & (b.head_mask | (c.m_poly([(18, 36), (36, 36), (32, cy + 6), (22, cy + 6)]) if full else False))
        c.paint(mk, mat, c.t_lin(mk, 0.3, 0.85), edge=False)
        if stache:
            my = b.ey + 11 + (1 if b.age != 'teen' else 0)
            c.poly([(20, my - 1.2), (26, my - 3), (32, my - 1.2), (33, my + 0.6), (26, my - 1), (19.5, my + 0.6)], mat, tone=0.6, edge=False)
    return fn


def wrinkles(b, expr=None, heavy=False):
    c = b.c
    col = b.skin[1]
    y = b.ey + b.eh + 1
    pts = [(13, y), (14, y + 1), (35, y), (22, y + 4), (21, y + 5), (31, y + 4), (32, y + 5)]
    if heavy:
        pts += [(18, b.ey - 6), (19, b.ey - 6), (20, b.ey - 6), (27, b.ey - 7), (28, b.ey - 7), (29, b.ey - 7), (13, y - 1), (20, y + 6), (33, y + 6)]
    for x, yy in pts:
        if c.ovr[yy, x, 3] == 0 and c.mat[yy, x] == c.m('skin'):
            c.px(x, yy, col)


def hood_P(mat='hood', open_line=None, vol=4.5):
    """Hood: bulk behind the head, edge framing the face."""
    line = open_line or [(6, 44), (10, 38), (11.5, 24), (15, 15.5), (23, 11.5), (31, 12.5), (37, 18), (39.5, 28), (41, 40), (44, 44)]

    def back(b):
        b.c.ell(24, 22, 19.5, 20.5, mat, lo=0.15, hi=0.75)

    def front(b):
        c = b.c
        outer = c.m_ell(24, 21, 14 + vol, 15.5 + vol) | c.m_poly([(4, 30), (44, 30), (46, 46), (2, 46)])
        pts = [(-2, -2), (50, -2), (50, 50), (line[-1][0], 50)] + list(reversed(line)) + [(line[0][0], 50), (-2, 50)]
        mk = outer & c.m_poly(pts)
        c.paint(mk, mat, c.t_sph(21, 15, 22, 24, 0.2, 0.95))
        c.stroke([(x + 1, y) for x, y in line[1:5]], line=True, only=mat)
    return back, front


def PO(kind, inner=None, extra=None, lift=0):
    def fn(b):
        c = b.c
        if inner:
            v_neck(b, inner, lapel='top' if kind == 'lapel' else None)
        if kind == 'high':
            collar_high(b, 'top', lift=lift)
        if kind == 'shawl':
            c.poly([(1, 48), (5, 42), (16, 38.5), (22, 44), (25, 48)], 'shawl', lo=0.4, hi=0.95)
            c.poly([(25, 48), (29, 43), (34, 38.5), (42, 42), (47, 48)], 'shawl', lo=0.2, hi=0.7)
        if extra:
            extra(b)
    return fn


def pin(x, y, col=GOLD):
    return lambda b: (b.c.px(x, y, col), b.c.px(x + 1, y, shift(col, dv=-0.2)), b.c.px(x, y + 1, shift(col, dv=-0.2)))


# ------------------------------------------------------------ trainer kit
def TH(line, vol=1.0, top=0.0, locks=(), blobs=(), hi=(), mat='hair', after=None, pre=None):
    def fn(f):
        if pre:
            pre(f)
        for dx, dy, rx, ry in blobs:
            hblob(f, dx, dy, rx, ry, mat)
        for p in locks:
            hlock(f, p, mat)
        hcap(f, line, vol, top, mat)
        hpx(f, hi, mat=mat)
        if after:
            after(f)
    return fn


def TG(hem=None, flare=2.5, open_front=True, shirt=None, shirt_len=7, tie=None, belt=None, extra=None, mat='top', lapel=False):
    def fn(f):
        c, J = f.c, f.J
        if hem is not None:
            f.skirt(hem, flare, mat, open_front=open_front)
        sx, sy = J['sh']
        if shirt:
            c.poly([(sx - 2.6, sy - 1), (sx + 1.6, sy - 1), (sx - 1.2, sy + shirt_len), (sx - 2.5, sy + shirt_len)], shirt, lo=0.4, hi=0.9)
            if tie:
                c.stroke([(sx - 1, sy), (sx - 1.6, sy + shirt_len - 1)], new=tie, only=shirt, tone=0.6)
            if lapel:
                c.stroke([(sx + 1.8, sy - 1), (sx - 1, sy + shirt_len)], line=True, only='top')
        if belt:
            wx, wy = J['waist']
            c.stroke([(wx - 6, wy + 1), (wx + 6, wy + 1.5)], new=belt, only=mat, tone=0.5)
        if extra:
            extra(f)
    return fn


def T_collar(mat='top', h=4.5):
    def fn(f):
        c = f.c
        sx, sy = f.J['sh']
        c.poly([(sx - 5.5, sy + 1), (sx - 4.5, sy - h), (sx - 1.5, sy - 1.5), (sx - 2.5, sy + 2)], mat, lo=0.45, hi=0.95)
        c.poly([(sx + 1.5, sy - 1), (sx + 5, sy - h), (sx + 6, sy + 1.5), (sx + 2.5, sy + 2.5)], mat, lo=0.2, hi=0.7)
    return fn


def T_shawl(mat='shawl', drop=7, spots=None):
    def fn(f):
        c = f.c
        sx, sy = f.J['sh']
        mk = c.poly([(sx - f.sw - 2.5, sy + drop), (sx - f.sw - 1, sy), (sx - 2, sy - 2), (sx + 2, sy - 2), (sx + f.sw + 1.5, sy + 0.5), (sx + f.sw + 3, sy + drop + 1),
                     (sx + 2, sy + drop - 1.5), (sx - 1, sy + drop + 2.5), (sx - 3, sy + drop - 1)], mat, lo=0.3, hi=0.95)
        if spots:
            for dx, dy in ((-5, 3), (5, 4)):
                c.px(sx + dx, sy + dy, spots); c.px(sx + dx + 1, sy + dy, spots); c.px(sx + dx, sy + dy + 1, shift(spots, dv=-0.2))
    return fn


def T_hood(mat='hood', vol=2.0):
    """Hood drawn as the hair layer; a little real hair shows at the brow."""
    def fn(f):
        hblob(f, 1.5, 0.5, f.hr[0] + vol - 0.5, f.hr[1] + vol, mat)
        f.c.paint(f.head_mask, 'skin', f.c.t_sph(f.J['head'][0] + 1, f.J['head'][1] + 1, 8, 9, 0.36, 0.8), edge=False)
        f.face()
        hcap(f, [(-6.5, -1), (-5, -3), (-3, -1.5), (-1, -3.2), (1.5, -1.5), (2.6, 0), (3, 5), (6, 7)], 0.4, 0, 'hair')
        hcap(f, [(-7.5, -2), (-5.5, -4.6), (-2, -5.4), (1.5, -4.2), (3.2, -1), (3.6, 4.5), (2.6, 8), (8, 9)], vol, 1.0, mat)
    return fn


def T_cane(col=(96, 70, 52), top=(226, 228, 240)):
    def fn(f):
        c = f.c
        x, y = [int(round(v)) for v in f.J['haL']]
        for yy in range(y - 2, GY + 1):
            c.px(x - 1, yy, col if yy > y else top)
            c.mat[yy, x - 1] = c.m('shoes'); c.tone[yy, x - 1] = 0.5
        c.px(x - 1, y - 3, top); c.px(x - 2, y - 2, top)
    return fn


def T_hat(crown, brim, mat='hat', band_=None, badge=None):
    def fn(f):
        hlock(f, crown, mat, lo=0.3, hi=0.95)
        hlock(f, brim, mat, lo=0.15, hi=0.6)
        if band_:
            hx_, hy_ = f.J['head']
            f.c.stroke([(hx_ + band_[0], hy_ + band_[2]), (hx_ + band_[1], hy_ + band_[2])], new=band_[3], only=mat, tone=0.5)
        if badge:
            hx_, hy_ = f.J['head']
            f.c.px(hx_ + badge[0], hy_ + badge[1], GOLD)
    return fn


def T_beard(mat='hair', length=3):
    def fn(f):
        hlock(f, [(-5.6, 2), (-3, 3.4), (1, 3.4), (4, 1.5), (4.5, 4), (1, 6.5 + length), (-3.5, 6.5 + length), (-5.6, 5)], mat, lo=0.25, hi=0.85)
        x0, y0 = f.face_xy
        f.c.pxs([(x0 - 3, y0 + 4), (x0 - 2, y0 + 4)], (128, 60, 60))
    return fn


def chain(*fns):
    def fn(x, *a):
        for g in fns:
            if g:
                g(x, *a)
    return fn


# ----------------------------------------------------------- overworld kit
def ow_hat(mat, brim=1, crown=3, wide=False):
    def acc(c, d, hx_, iy, step):
        top = iy - 4 - crown
        m = c.m_ell(hx_, iy - 3, 5.6, crown + 1.6) & R(c, 0, top, 15, iy - 4)
        c.paint(m, mat, c.t_lin(m, 0.4, 1.0), edge=False)
        if d == 'left':
            c.paint(R(c, 1 if brim else 2, iy - 3, 13 if wide else 9, iy - 3), mat, 0.3, edge=False)
        elif d == 'down':
            c.paint(R(c, 2 - (1 if wide else 0), iy - 3, 13 + (1 if wide else 0), iy - 3), mat, 0.3, edge=False)
        elif wide:
            c.paint(R(c, 1, iy - 3, 14, iy - 3), mat, 0.3, edge=False)
    return acc


def ow_hood(mat):
    def acc(c, d, hx_, iy, step):
        if d == 'up':
            m = c.m_ell(hx_, iy - 0.3, 6.2, 6.4)
        elif d == 'down':
            m = c.m_ell(hx_, iy - 0.3, 6.4, 6.4) & ~c.m_ell(hx_, iy + 1.2, 4.3, 4.2)
        else:
            m = c.m_ell(hx_ + 0.5, iy - 0.3, 6.2, 6.4) & ~(c.m_ell(hx_ - 2.4, iy + 1.2, 3.6, 4.0))
        c.paint(m, mat, c.t_sph(hx_ - 1, iy - 2, 8, 8, 0.2, 1.0), edge=False)
    return acc


def ow_beard(mat='hair'):
    def acc(c, d, hx_, iy, step):
        if d == 'down':
            c.paint(R(c, 5, iy + 3, 10, iy + 4) | R(c, 4, iy + 2, 4, iy + 3) | R(c, 11, iy + 2, 11, iy + 3), mat, 0.5, edge=False)
        elif d == 'left':
            c.paint(R(c, 3, iy + 3, 7, iy + 4), mat, 0.5, edge=False)
    return acc


def ow_px(pts_down=(), pts_left=(), pts_up=()):
    """Explicit accent pixels: (dx from head centre, dy from eye row, colour)."""
    def acc(c, d, hx_, iy, step):
        for dx, dy, col in {'down': pts_down, 'left': pts_left, 'up': pts_up}[d]:
            c.px(int(hx_ + dx), iy + dy, col)
    return acc


def ow_body(fn_down=None, fn_any=None):
    def body(c, d, step, tor_top, x0, x1):
        if d == 'down' and fn_down:
            fn_down(c, tor_top, x0, x1)
        if fn_any:
            fn_any(c, d, tor_top, x0, x1)
    return body


def ow_cape(mat, rows=4):
    def fn(c, d, tor_top, x0, x1):
        m = R(c, x0 - 1 if d != 'left' else 5, tor_top, x1 + 1 if d != 'left' else 10, tor_top + rows - (0 if d == 'up' else 1))
        if d == 'down':
            m &= ~R(c, 7, tor_top + 1, 8, 23)
        c.paint(m, mat, c.t_lin(m, 0.35, 0.95), edge=False)
    return fn
