"""cast.py - every Prismfall character as data + small drawing closures.

Each entry: dict(id=portrait id, tt=[trainer types], P=portrait spec,
T=trainer-sprite spec, O=overworld spec, exprs=[...]).
"""
import numpy as np
from px import shift, ramp, hx
from portrait import hair_cap, lock, shine, strands, hair_tone, INK, WHITE

FULL = ['neutral', 'happy', 'smug', 'angry', 'crying', 'shocked', 'deadpan', 'panic', 'sad', 'blush']
STD = ['neutral', 'happy', 'angry', 'sad', 'shocked', 'deadpan']
CAST = {}


def add(cid, **kw):
    kw['id'] = cid
    CAST[cid] = kw
    return kw


# ------------------------------------------------------------ bust outfits
def collar_high(b, mat='top', lift=0, line=True):
    c = b.c
    c.poly([(13, 45), (14, 35 - lift), (19, 37.5), (23, 46)], mat, lo=0.3, hi=0.85)
    c.poly([(28, 46), (31, 38), (36.5, 35 - lift), (37.5, 44)], mat, lo=0.2, hi=0.6)


def v_neck(b, inner, depth=48, lapel=None, lw=3):
    """Open front showing an inner layer; optional lapels."""
    c = b.c
    c.poly([(18, 40.5), (32, 40.5), (26 + 1, depth), (24, depth)], inner, lo=0.45, hi=0.9, only=b.sh_mask | (c.mat == c.m('skin')))
    if lapel:
        c.poly([(18 - lw, 40.5), (18.5, 40), (25, 48), (20 - lw, 48)], lapel, lo=0.35, hi=0.9)
        c.poly([(32 + lw, 40.5), (31.5, 40), (26, 48), (31 + lw, 48)], lapel, lo=0.2, hi=0.7)


def strap(b, mat, x0=10, x1=30):
    b.c.poly([(x0, 41), (x0 + 3.2, 41), (x1 + 3.2, 48), (x1, 48)], mat, lo=0.3, hi=0.8, only=b.sh_mask)


def glasses(b, col=(70, 60, 80), low=0, lens=None, chain=None):
    """Wire spectacles.  low>0 pushes them down the nose (reading glasses)."""
    c = b.c
    y = b.ey + low
    h = max(3, b.eh + 1)
    for (x0, x1) in ((14, 22), (28, 34)):
        for x in range(x0 + 1, x1):
            c.px(x, y - 1 if low == 0 else y, col) if low == 0 else None
            c.px(x, y + h + (0 if low == 0 else 0), col)
        for yy in range(y, y + h):
            if low == 0:
                c.px(x0, yy, col); c.px(x1, yy, col)
        if low:
            c.px(x0, y + h - 1, col); c.px(x1, y + h - 1, col)
            c.px(x0, y + h - 2, col); c.px(x1, y + h - 2, col)
    for x in range(23, 28):
        c.px(x, y + (1 if low == 0 else h - 1), col)
    if lens:
        for (x0, x1) in ((14, 22), (28, 34)):
            c.px(x0 + 2, y + (h - 2 if low else 0), lens); c.px(x0 + 3, y + (h - 1 if low else 1), lens) if not low else None
    if chain:
        for i, yy in enumerate(range(y + h - 1, 44)):
            if i % 2 == 0:
                c.px(13 - min(2, i // 3), yy, chain)


def freckles(b, expr=None):
    c = b.c
    col = shift(b.skin[1], ds=0.05)
    y = b.ey + 6
    for x, yy in ((16, y), (18, y + 1), (20, y), (25, y - 1), (31, y), (33, y + 1), (23, y)):
        if c.ovr[yy, x, 3] == 0:
            c.px(x, yy, col)


# =================================================================== JUNO
def juno_back(b):
    c = b.c
    for cx, cy, r in ((7, 22, 6), (5, 30, 5.5), (8, 37, 5), (41, 23, 4.5), (43, 30, 4), (41, 36, 3.5), (12, 41, 4), (12, 5, 4), (20, 2.5, 4), (29, 2, 4), (37, 5, 3.5)):
        c.ell(cx, cy, r, r + 0.5, 'hair', tone=hair_tone(b, None, lo=0.1, hi=0.8), edge=False)


def juno_front(b):
    c = b.c
    # frizzy fringe under the kerchief
    hair_cap(b, [(8, 26), (11, 27), (12, 22), (15, 21), (17, 17.5), (21, 20), (24, 16.5), (28, 19.5), (31, 16.5), (35, 20), (38, 18), (40, 24)], vol=2.5)
    for cx, cy, r in ((8.5, 25, 3.6), (7, 31, 3.4), (40.5, 26, 2.6), (41.5, 31, 2.4)):
        c.ell(cx, cy, r, r, 'hair', tone=hair_tone(b, None), edge=False)
    shine(b, [(13, 19), (15, 17), (17, 16)]); shine(b, [(22, 16), (24, 15)]); shine(b, [(5, 28), (6, 30)])
    strands(b, [[(21, 17), (21, 19)], [(28, 16), (28, 18)], [(35, 17), (35, 19)], [(9, 27), (10, 29)]])
    # kerchief: a folded band across the crown, bow knot behind the near ear;
    # frizz escapes above it at the back and below it as the fringe
    band = c.m_ell(24, 19.2, 17.2, 16.8) & c.m_poly([(-2, 12), (10, 8.5), (20, 5.2), (30, 4.6), (40, 6.5), (50, 9), (50, 14.5), (40, 13.5), (30, 11.8), (20, 12.2), (10, 15.5), (-2, 19)])
    c.paint(band, 'kerchief', c.t_sph(22, 10, 20, 8, lo=0.25, hi=0.95))
    c.stroke([(9, 15), (20, 11), (30, 10.6), (40, 12.4)], line=True, only='kerchief')
    for x, y in ((14, 10), (19, 8), (25, 7), (31, 8), (36, 9)):
        c.px(x, y, (250, 240, 200)); c.px(x + 1, y + 1, (250, 240, 200))
    c.poly([(1, 12), (6, 11), (8, 15), (4, 17)], 'kerchief', lo=0.4, hi=0.9)      # bow loops
    c.poly([(5, 15), (9, 15), (8, 21), (5, 22)], 'kerchief', lo=0.2, hi=0.7)
    c.poly([(1, 18), (4, 17), (4, 25), (2, 26)], 'kerchief', lo=0.2, hi=0.6)


def juno_outfit(b):
    c = b.c
    v_neck(b, 'shirt', depth=47)
    c.poly([(15, 41.5), (19.5, 38.5), (24, 43.5), (20, 45.5)], 'shirt', lo=0.5, hi=0.95)     # collar points
    c.poly([(26, 43.5), (30.5, 38.8), (34, 41.5), (30, 45.5)], 'shirt', lo=0.4, hi=0.8)
    strap(b, 'strap', 9, 12); 
    c.poly([(33, 41.5), (36, 41.5), (37.5, 48), (34.5, 48)], 'strap', lo=0.3, hi=0.7, only=b.sh_mask)
    c.px(11, 44, (232, 200, 96)); c.px(35, 45, (232, 200, 96))    # brass buttons


add('JUNO', tt=['RIVAL_JUNO', 'LEADER_JUNO'], exprs=FULL, P=dict(
    skin='#f7cfa8', hair='#b9542a', eye='#4f8a3a', age='teen', jaw='round', shoulders='narrow', eye_tilt=-1, lashes=True,
    sparkle=True, mats=dict(top='#6f8f4e', kerchief='#e2a93a', shirt='#f2ead2', strap='#8a5a34'),
    hair_back=juno_back, hair_front=juno_front, outfit=juno_outfit, extras=freckles))


# ================================================================ KESTREL
def kes_back(b):
    c = b.c
    for pts in ([(9, 12), (1, 10), (8, 18)], [(8, 18), (0, 20), (8, 25)], [(9, 24), (3, 31), (11, 31)], [(14, 6), (9, 0), (20, 4)],
                [(22, 5), (24, -1), (30, 5)]):
        lock(b, pts)


def kes_front(b):
    c = b.c
    hair_cap(b, [(8, 28), (11, 30), (12.5, 21), (15, 23.5), (17, 18.5), (20, 22), (23, 17.5), (25.5, 27.5), (28, 17), (32, 20), (35, 15.5), (38, 19.5), (41, 18)], vol=2.2, top=1)
    lock(b, [(30, 6), (38, 2), (36, 8)]); lock(b, [(36, 9), (44, 9), (39, 14)]); lock(b, [(39, 15), (45, 19), (40, 21)])
    shine(b, [(11, 15), (14, 11), (18, 9)]); shine(b, [(22, 9), (26, 8)])
    strands(b, [[(18, 12), (17, 17)], [(24, 12), (25, 24)], [(31, 10), (30, 16)]])


def kes_outfit(b):
    c = b.c
    v_neck(b, 'shirt', depth=48)
    collar_high(b, 'top', lift=1)
    c.stroke([(14, 35), (19, 38), (23, 46)], dt=0.3, only='top')
    c.px(21, 45, (176, 182, 204)); c.px(22, 45, (236, 238, 246)); c.px(29, 45, (176, 182, 204))   # clasp


add('KESTREL', tt=['RIVAL_KESTREL'], exprs=FULL, P=dict(
    skin='#f1d6c2', hair='#34334a', eye='#7a7fb0', age='teen', jaw='sharp', shoulders='normal', eye_tilt=1,
    rest_brow=(1, -1), rest_mouth='frown', hair_contrast=1.25,
    mats=dict(top='#3e3c4e', shirt='#8c2f3a'),
    hair_back=kes_back, hair_front=kes_front, outfit=kes_outfit))


# ================================================================== LARCH
def larch_back(b):
    pass


def larch_front(b):
    c = b.c
    hair_cap(b, [(8, 27), (11, 27), (12, 19), (16, 14.5), (21, 12.5), (27, 13), (33, 14.5), (37, 18), (40, 21)], vol=1.2)
    strands(b, [[(22, 6), (21, 12)], [(15, 9), (13, 17)], [(30, 7), (32, 13)]])
    shine(b, [(13, 13), (16, 10), (19, 8)])
    lock(b, [(21, 12.5), (23, 10), (26, 13), (24, 16)])        # stray wisp
    # braid over the near shoulder
    for i, y in enumerate(range(28, 47, 4)):
        c.ell(8.5 + (i % 2) * 1.2 - 0.5 + i * 0.5, y + 1.5, 2.8, 2.6, 'hair', tone=0.75 if i % 2 == 0 else 0.5)
    c.poly([(9, 45), (13, 45), (13, 47), (9, 47)], 'tie', tone=0.6)


def larch_outfit(b):
    c = b.c
    v_neck(b, 'shirt', depth=48)
    collar_high(b, 'top', lift=0)
    c.poly([(11, 48), (13, 43), (20, 44), (24, 48)], 'top', lo=0.4, hi=0.95)   # storm flap
    c.px(30, 46, (96, 78, 60)); c.px(30, 47, (96, 78, 60))


def larch_over(b, expr):
    glasses(b, col=(92, 84, 110), low=2, chain=(206, 190, 130))


add('LARCH', exprs=FULL, P=dict(
    skin='#e3b891', hair='#a4a6b4', eye='#56707a', age='adult', jaw='long', gaunt=True, nose='medium', bags=True,
    brow='#77788a', rest_brow=(0, 0), shoulders='narrow',
    mats=dict(top='#c9a13c', shirt='#5b6e78', tie='#a8453a'),
    hair_back=larch_back, hair_front=larch_front, outfit=larch_outfit, over_face=larch_over))


# ======================================================== trainer sprites
from trainer import hcap, hlock, hblob, hpx, GY


def T(cid, **kw):
    CAST[cid]['T'] = kw


def jp(f, name, dx=0, dy=0):
    x, y = f.J[name]
    return (x + dx, y + dy)


def satchel(f, mat='bag', strap='strap', side=1):
    c, J = f.c, f.J
    sx, sy = J['sh']
    hx_, hy_ = J['hip']
    c.stroke([(sx - f.sw * 0.6, sy), (hx_ + f.hw + 1, hy_ - 1)], new=strap, only='top', tone=0.5)
    c.stroke([(sx - f.sw * 0.6, sy + 1), (hx_ + f.hw + 1, hy_)], new=strap, only='top', tone=0.3)
    c.poly([(hx_ + f.hw - 0.5, hy_ - 1.5), (hx_ + f.hw + 5, hy_ - 1), (hx_ + f.hw + 5.5, hy_ + 5), (hx_ + f.hw - 0.5, hy_ + 5)], mat, lo=0.25, hi=0.9)
    c.stroke([(hx_ + f.hw, hy_ + 1), (hx_ + f.hw + 5, hy_ + 1.4)], line=True, only=mat)
    c.px(hx_ + f.hw + 2, hy_ + 2, (236, 206, 110))


# ---- Juno
def juno_T_hair(f):
    c = f.c
    for dx, dy, r in ((6, -2, 3.4), (7.5, 2, 3.2), (6.5, 6, 3), (4, -6, 3), (-1, -7.5, 3), (-5, -5.5, 2.4), (4, 8.5, 2.4)):
        hblob(f, dx, dy, r, r)
    hcap(f, [(-6.5, -1), (-5, -3), (-3.5, -1.2), (-2, -3.2), (-0.5, -1.4), (1.5, -3), (3, 0), (3.5, 3), (7, 4)], vol=1.3)
    hlock(f, [(-6.8, -3.4), (-3, -6.2), (2, -6.4), (6.2, -4.6), (6.6, -2.2), (2, -4), (-3, -3.8), (-6.4, -1.4)], mat='kerchief', lo=0.3, hi=0.95)
    hlock(f, [(6, -4.5), (9.5, -5.5), (9, -2.5), (6.5, -2.4)], mat='kerchief', lo=0.2, hi=0.7)
    hlock(f, [(7.5, -2.5), (9.5, -2), (9.5, 1.5), (8, 1)], mat='kerchief', lo=0.2, hi=0.6)
    hpx(f, [(5, -1), (6, 0), (7, 3), (-1, -8), (0, -8)])
    x0, y0 = f.face_xy
    for dx, dy in ((-3, 2), (-1, 3), (1, 2)):
        c.px(x0 + dx, y0 + dy, shift(f.skin[1], ds=0.05))


def juno_T_garment(f):
    c, J = f.c, f.J
    f.skirt(0.36, 2.2, 'top')
    sx, sy = J['sh']
    # shirt shows at the neck and sides: the green is a pinafore bib with straps
    c.poly([(sx - 3, sy - 1.5), (sx + 3, sy - 1.5), (sx + 0.5, sy + 3.5), (sx - 1, sy + 3.5)], 'shirt', lo=0.5, hi=0.95)
    c.stroke([jp(f, 'waist', -5, 0), jp(f, 'waist', 5, 0.5)], new='strap', only='top', tone=0.45)
    c.px(*[int(v) for v in jp(f, 'waist', -1, 0)], (236, 206, 110))
    # gardening gloves clipped at the belt
    c.poly([jp(f, 'waist', -5.5, 1), jp(f, 'waist', -3, 1), jp(f, 'waist', -3.4, 4.5), jp(f, 'waist', -5.6, 4)], 'glove', lo=0.3, hi=0.9)
    c.stroke([jp(f, 'hip', -4, 5), jp(f, 'hip', 4.5, 5.5)], dt=0.3, only='top')


def juno_T_detail(f):
    satchel(f)
    c = f.c
    for side in 'LR':     # sock cuffs above the boots
        ax, ay = f.J['an' + side]
        c.stroke([(ax - 2, ay - 4.2), (ax + 2, ay - 4.2)], new='shirt', only='skin', tone=0.85)
        c.stroke([(ax - 2, ay - 3.2), (ax + 2, ay - 3.2)], new='shirt', only='skin', tone=0.5)


T('JUNO', skin='#f7cfa8', hair='#b9542a', eye='#3f7a34', H=48, sw=5.0, hw=4.0, ra=1.6, rl=2.2, head=(5.6, 6.0), pose='ball',
  eye_h=3, mouth_t='smile', legs='dress', sleeve='shirt', sleeve_len=0.55, boots=3,
  mats=dict(top='#6f8f4e', kerchief='#e2a93a', shirt='#f2ead2', strap='#8a5a34', bag='#a8713e', glove='#d9b77c', shoes='#7a4c30'),
  garment=juno_T_garment, hairdo=juno_T_hair, detail=juno_T_detail)


# ---- Kestrel
def kes_T_hair(f):
    for pts in ([(3, -6), (8.5, -8.5), (6, -3)], [(5, -3.5), (10.5, -2.5), (6, 0.5)], [(5, 0), (9.5, 3.5), (5, 3.5)],
                [(-2.5, -6), (0.5, -10.5), (2.5, -6)], [(-5.5, -4.5), (-7, -9), (-2, -6)]):
        hlock(f, pts)
    hcap(f, [(-6.5, -3), (-5.2, -1.6), (-4.2, -3.4), (-2.6, -1.8), (-1.6, -3.6), (0.4, -3.4), (2.2, 0.2), (3.2, -2.5), (4.2, 3.5), (7, 4)], vol=1.2, top=1)
    hpx(f, [(-3, -6), (-2, -6), (-1, -7), (0, -7), (2, -6), (-4, -5)])


def kes_T_garment(f):
    c, J = f.c, f.J
    f.skirt(0.27, 3.2, 'top', open_front=True)
    sx, sy = J['sh']
    c.poly([(sx - 2.5, sy - 1), (sx + 1.5, sy - 1), (sx - 1.5, sy + 9), (sx - 2.5, sy + 9)], 'shirt', lo=0.35, hi=0.8)
    c.stroke([(sx + 1.5, sy - 1), (sx - 1.2, sy + 9)], line=True, only='top')
    c.px(int(sx - 2), int(sy + 9), (200, 204, 222))


def kes_T_collar(f):
    c, J = f.c, f.J
    sx, sy = J['sh']
    c.poly([(sx - 5.5, sy + 1), (sx - 4.5, sy - 4.5), (sx - 1.5, sy - 1.5), (sx - 2.5, sy + 2)], 'top', lo=0.45, hi=0.95)
    c.poly([(sx + 1.5, sy - 1), (sx + 5, sy - 4.5), (sx + 6, sy + 1.5), (sx + 2.5, sy + 2.5)], 'top', lo=0.2, hi=0.7)


T('KESTREL', skin='#f1d6c2', hair='#34334a', eye='#6a6fa8', H=52, sw=5.6, hw=4.2, ra=1.8, rl=2.3, head=(5.3, 6.0), pose='ball', hair_contrast=1.25,
  brow_t=0, eye_h=2, mouth_t='frown', cuff=0.7, boots=4, chin=0.6,
  mats=dict(top='#3e3c4e', shirt='#8c2f3a', legs='#2c2b38', shoes='#57586e'),
  garment=kes_T_garment, collar=kes_T_collar, hairdo=kes_T_hair)


# ---- Larch
def larch_T_hair(f):
    c = f.c
    hcap(f, [(-6.5, -3), (-4, -4.4), (-1, -4.6), (2, -3.4), (3.4, -0.5), (3.8, 3), (7, 4)], vol=0.8)
    hx_, hy_ = f.J['head']
    for i in range(5):     # braid down the near shoulder
        c.ell(hx_ + 5.2 + (i % 2) * 0.8, hy_ + 5 + i * 2.6, 1.7, 1.7, 'hair', tone=0.8 if i % 2 == 0 else 0.45)
    c.px(int(hx_ + 5), int(hy_ + 18), (190, 70, 60)); c.px(int(hx_ + 6), int(hy_ + 18), (190, 70, 60))
    hpx(f, [(-3, -6), (-2, -6), (-1, -6), (0, -7)])
    x0, y0 = f.face_xy
    g = (86, 80, 108)
    for dx, dy in ((-5, 2), (-4, 2), (-3, 2), (-2, 2), (-1, 2), (0, 2), (1, 2), (2, 1), (3, 0)):
        c.px(x0 + dx, y0 + dy, g)
    c.px(x0 - 3, y0 + 2, (214, 226, 238)); c.px(x0, y0 + 2, (214, 226, 238))


def larch_T_garment(f):
    c, J = f.c, f.J
    f.skirt(0.20, 2.6, 'top', open_front=True)
    sx, sy = J['sh']
    c.poly([(sx - 2.5, sy - 1), (sx + 1.5, sy - 1), (sx - 1, sy + 6), (sx - 2.4, sy + 6)], 'shirt', lo=0.35, hi=0.8)
    for i in range(3):
        c.px(int(J['waist'][0] + 1), int(J['waist'][1] - 3 + i * 4), (110, 84, 50))
    c.stroke([jp(f, 'hip', 2, 1), jp(f, 'hip', 5, 1.5)], line=True, only='top')        # pocket flap
    c.stroke([jp(f, 'hip', -2, 14), jp(f, 'hip', 6, 14.5)], dt=0.3, only='top')


def mug(f, col=(232, 226, 214)):
    c = f.c
    x, y = [int(round(v)) for v in f.J['haL']]
    c.stamp(["WWWw", "WWWwk", "WWWwk", "WWww."], x - 3, y - 4, {'W': col, 'w': shift(col, dv=-0.18, dh=-10, ds=0.05), 'k': shift(col, dv=-0.3)})
    c.px(x - 2, y - 6, (236, 240, 244)); c.px(x - 1, y - 7, (236, 240, 244)); c.px(x - 2, y - 9, (236, 240, 244))


T('LARCH', skin='#e3b891', hair='#a4a6b4', eye='#44606a', H=53, sw=5.4, hw=4.2, ra=1.7, rl=2.2, head=(5.2, 6.1), pose='lantern', ball=False,
  eye_h=2, brow_t=1, brow='#77788a', nose_t=2, chin=0.8, boots=6,
  mats=dict(top='#c9a13c', shirt='#5b6e78', legs='#4c5560', shoes='#3d4a44'),
  garment=larch_T_garment, collar=None, hairdo=larch_T_hair, detail=mug)


# ============================================================ overworld
def O(cid, **kw):
    """Overworld spec: inherits skin/hair/eye/mats from the trainer spec."""
    base = CAST[cid]['T']
    d = dict(skin=base['skin'], hair=base['hair'], eye=base.get('eye', '#4a3a30'), mats=base.get('mats', {}),
             hair_contrast=base.get('hair_contrast', 1.0), sleeve=base.get('sleeve', 'top'), sleeve_len=base.get('sleeve_len', 1.0),
             boots=base.get('boots', 0), gloves=base.get('gloves', 'skin'))
    d.update(kw)
    CAST[cid]['O'] = d


def band(mat, y0=-5, y1=-3, knot=True):
    """Head band / kerchief across the crown (all directions)."""
    def acc(c, d, hx_, iy, step):
        from overworld import R
        m = c.m_ell(hx_, iy - 0.3, 6.0, 6.0) & R(c, 0, iy + y0, 15, iy + y1)
        c.paint(m, mat, c.t_lin(m, 0.4, 1.0), edge=False)
        if knot and d == 'up':
            c.paint(R(c, 7, iy + y1 + 1, 8, iy + y1 + 2), mat, 0.4)
        if knot and d == 'left':
            c.paint(R(c, 13, iy + y1, 13, iy + y1 + 2), mat, 0.4)
    return acc


O('JUNO', garment='dress', shirt_v=2, ow_mouth=True,
  ow_hair=dict(fringe=[1, 1, 0, 1, 0, 1, 0, 1, 1, 1], sides=5, back=2, vol=2.4, top=1, spikes=[(-7, 1), (-7, 3), (6, 1), (6, 3), (-6, 5), (5, 5)]), ow_acc=band('kerchief', -6, -4))
O('KESTREL', garment='coat', tall=1, shirt_v=3,
  ow_hair=dict(fringe=[1, 1, 0, 1, 2, 0, 1, 0, 1, 1], sides=2, back=0, vol=1.4, top=1, spikes=[(-3, -8), (0, -9), (3, -8), (-7, -3), (6, -3), (-7, 0), (6, 0), (6, -6), (-6, -6), (7, -1)]))
def larch_ow(c, d, hx_, iy, step):
    from overworld import R
    g = (92, 84, 110)
    if d == 'down':
        c.px(4, iy, g); c.px(6, iy, g); c.px(9, iy, g); c.px(11, iy, g); c.px(7, iy, g); c.px(8, iy, g)
        c.paint(R(c, 2, iy + 2, 3, iy + 8), 'hair', 0.7, edge=False)
        c.stroke([(2, iy + 4), (3, iy + 4)], tone=0.3, only='hair'); c.stroke([(2, iy + 6), (3, iy + 6)], tone=0.3, only='hair')
        c.px(2, iy + 9, (168, 69, 58)); c.px(3, iy + 9, (168, 69, 58))
    elif d == 'left':
        c.px(3, iy, g); c.px(5, iy, g); c.px(6, iy, g)
        c.paint(R(c, 10, iy + 1, 11, iy + 7), 'hair', 0.6, edge=False)
        c.stroke([(10, iy + 3), (11, iy + 3)], tone=0.3, only='hair'); c.stroke([(10, iy + 5), (11, iy + 5)], tone=0.3, only='hair')
    else:
        c.paint(R(c, 7, iy + 2, 8, iy + 9), 'hair', 0.6, edge=False)
        for k in range(iy + 3, iy + 9, 2):
            c.stroke([(7, k), (8, k)], tone=0.3, only='hair')
        c.px(7, iy + 10, (168, 69, 58)); c.px(8, iy + 10, (168, 69, 58))


O('LARCH', garment='coat', tall=1, shirt_v=2, hem=1, ow_acc=larch_ow,
  ow_hair=dict(fringe=[0] * 10, line=-3, sides=0, back=0, vol=0.6))

import cast3  # noqa: E402,F401  (registers the rest of the cast)
import cast4  # noqa: E402,F401
