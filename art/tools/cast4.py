"""cast4.py - rest of Act I, the remaining Wardens, Valen, generics."""
from cast2 import *
from cast2 import PH, PO, TH, TG
from cast3 import SHORT_T, HIGH_T

MID_T = [(-6.5, -1.5), (-5, -3), (-3, -1.6), (-1, -3.4), (1.5, -2.6), (3, 0), (3.6, 4), (7, 5)]


# --------------------------------------------------------- accessory kit
def p_scar(pts, col=(214, 132, 130)):
    def fn(b, e=None):
        for x, y in pts:
            if b.c.ovr[y, x, 3] == 0:
                b.c.px(x, y, col)
    return fn


def p_pipe(col=(120, 80, 60)):
    def fn(b, e=None):
        my = b.ey + 12 + b.s.get('mouth_y', 0)
        b.c.pxs([(30, my), (31, my + 1), (32, my + 1), (33, my + 1), (34, my), (34, my - 1), (35, my - 1), (35, my), (36, my - 1)], col)
        b.c.pxs([(34, my - 2), (35, my - 2), (36, my - 2)], shift(col, dv=-0.25))
    return fn


def p_goggles(lens='#7ab8c8', frame='#8a6a4a'):
    def fn(b):
        c = b.c
        c.material('gogf', ramp(frame, 3)); c.material('gogl', ramp(lens, 3))
        c.poly([(8, 13), (40, 9.5), (41, 12.5), (8, 16.5)], 'gogf', lo=0.3, hi=0.8)
        for cx, cy, r in ((19, 11.5, 4.6), (31, 10.2, 4.0)):
            c.ell(cx, cy, r, r * 0.85, 'gogf', lo=0.25, hi=0.9)
            c.ell(cx, cy, r - 1.5, r * 0.85 - 1.4, 'gogl', lo=0.3, hi=1.0)
            c.px(int(cx) - 1, int(cy) - 1, (255, 255, 255))
    return fn


def p_earmuffs(mat='muff'):
    def fn(b):
        c = b.c
        c.poly([(8, 22), (11, 6), (24, 0), (37, 4), (41, 18), (39, 19), (35, 6), (24, 2.5), (13, 8), (10.5, 22)], mat, lo=0.3, hi=0.9)
        c.ell(9.5, 25, 4.6, 5.4, mat, lo=0.25, hi=0.95)
        c.ell(40, 22, 2.6, 4.6, mat, lo=0.2, hi=0.7)
    return fn


def p_lamp_hat(b):
    c = b.c
    c.poly([(6, 17), (8, 7), (16, 2), (32, 2), (40, 7), (42, 16)], 'hat', lo=0.3, hi=0.95)
    c.poly([(3, 17.5), (44, 15.5), (45, 18.5), (3, 20)], 'hat', lo=0.2, hi=0.6)
    c.ell(27, 9, 4.2, 3.8, 'lampc', lo=0.3, hi=0.9)
    c.ell(27, 9, 2.6, 2.3, 'lamp', lo=0.6, hi=1.0)
    c.px(26, 8, (255, 255, 240))


def p_veil(b):
    c = b.c
    lace = (60, 52, 72)
    for x in range(12, 38):
        for y in range(13, 19):
            if (x + y) % 3 == 0 and c.mat[y, x] in (c.m('skin'), c.m('hair')):
                c.px(x, y, lace)
    c.pline([(12, 19), (24, 20), (37, 18)], lace)


def p_flowers(cols=((214, 150, 230), (250, 220, 120), (150, 200, 250)), spots=((10, 14), (16, 8), (34, 7), (39, 13), (6, 21))):
    def fn(b, e=None):
        c = b.c
        for i, (x, y) in enumerate(spots):
            col = cols[i % len(cols)]
            for dx, dy in ((0, -1), (-1, 0), (1, 0), (0, 1)):
                c.px(x + dx, y + dy, col)
            c.px(x, y, (255, 246, 200))
    return fn


def p_braid_crown(mat='hair'):
    def fn(b):
        c = b.c
        for i, x in enumerate(range(10, 40, 4)):
            y = 9 + abs(x - 24) * 0.28
            c.ell(x + 2, y, 2.8, 2.3, mat, tone=0.85 if i % 2 == 0 else 0.5)
    return fn


def p_beak_up(b):
    """Plague mask pushed up onto the head, beak pointing up-right."""
    c = b.c
    c.poly([(14, 10), (22, 4), (32, 4), (37, 10), (30, 13), (18, 13)], 'beak', lo=0.3, hi=0.9)
    c.poly([(30, 5), (44, -2), (46, 1), (35, 10)], 'beak', lo=0.25, hi=0.8)
    for cx in (21, 29):
        c.ell(cx, 8.5, 2.2, 2.0, 'lens', lo=0.3, hi=1.0)


def p_earring(col=(232, 214, 140)):
    def fn(b, e=None):
        b.c.pxs([(10, 29), (11, 30), (11, 31), (10, 32), (9, 31)], col)
    return fn


def p_armor(b):
    c = b.c
    c.poly([(2, 48), (3, 41), (9, 37), (17, 37.5), (19, 44), (15, 48)], 'armor', lo=0.35, hi=0.95)
    c.poly([(31, 37.5), (39, 37), (45, 41), (46, 48), (33, 48), (30, 44)], 'armor', lo=0.2, hi=0.7)
    for x, y in ((6, 41), (10, 40), (14, 40), (35, 40), (39, 40), (42, 42)):
        c.px(x, y, shift(hx('#c8a050'), dv=0.1))


def t_px(pts, col):
    """Trainer accent pixels relative to the face anchor."""
    def fn(f):
        x0, y0 = f.face_xy
        f.c.pxs([(x0 + dx, y0 + dy) for dx, dy in pts], col)
    return fn


def t_glasses(col=(90, 84, 110)):
    return t_px([(-5, 0), (-3, 0), (-2, 0), (0, 0), (-4, 1), (-1, 1)], col)


def t_drone(f):
    c = f.c
    x, y = [int(v) for v in jp(f, 'head', -13, -3)]
    c.stamp(["..kkk..", ".kOOOk.", "kOoeoOk", ".kOOOk.", "k..k..k"], x, y,
            {'k': (40, 36, 52), 'O': (236, 120, 60), 'o': (250, 170, 110), 'e': (120, 230, 250)})


def t_lantern(f):
    c = f.c
    x, y = [int(round(v)) for v in f.J['haL']]
    c.stamp([".k.", "kkk", "kyk", "kYk", "kkk"], x - 1, y - 1, {'k': (50, 44, 56), 'y': (250, 220, 120), 'Y': (240, 170, 70)})


def t_sword_scar(pts, col=(214, 132, 130)):
    return t_px(pts, col)


def ow_goggles(col=(140, 200, 210)):
    return ow_px(pts_down=[(-3, -3, col), (2, -3, col), (-2, -3, col), (3, -3, col)], pts_left=[(-4, -3, col), (-3, -3, col)])


# ================================================================ ACT I
# ---- Marisol
MAR_M = dict(top='#2f5a74', shirt='#efe8d8', legs='#3a4658', shoes='#4a3a30', band='#d0503c')
add('MARISOL', tt=['LEADER_MARISOL'], exprs=FULL, P=dict(
    skin='#c98a5e', hair='#33262a', eye='#5a3a22', age='adult', jaw='broad', shoulders='broad', neck_w=6, rest_mouth='smile', brow_thick=True, mats=MAR_M,
    outfit=PO('none', inner='shirt', extra=chain(lambda b: strap(b, 'top', 8, 12), pin(34, 43, (220, 70, 60)))),
    **PH([(8, 26), (11, 27), (12, 19), (16, 16), (21, 18), (25, 14.5), (30, 17), (35, 15), (38, 19), (40, 22)], vol=1.8,
         back=[[(34, 2), (44, 4), (47, 18), (42, 26), (40, 12)]], sh=[[(13, 13), (17, 9), (22, 8)]], st=[[(24, 7), (25, 14)]],
         after=lambda b: b.c.poly([(7, 13), (14, 6), (26, 3.5), (37, 5), (41, 11), (40, 14), (26, 8), (12, 11.5), (8, 17)], 'band', lo=0.3, hi=0.9))))
T('MARISOL', skin='#c98a5e', hair='#33262a', eye='#4a2a12', H=54, sw=7.2, hw=5.0, ra=2.3, rl=2.8, head=(5.4, 5.9), pose='fist', eye_h=2, brow_t=2, mouth_t='open', mats=MAR_M,
  sleeve='shirt', sleeve_len=0.45, boots=5,
  garment=TG(shirt='shirt', shirt_len=8, belt='legs', extra=lambda f: f.c.px(f.J['sh'][0] + 3, f.J['sh'][1] + 3, (220, 70, 60))),
  hairdo=TH(SHORT_T, 1.0, 0.3, locks=[[(3, -6), (9, -5), (10, 6), (7, 7), (5, -2)]], hi=[(-3, -6), (-2, -6), (-1, -7)],
            after=lambda f: hlock(f, [(-6.6, -3), (-3, -6), (2, -6.2), (5.6, -4), (5.4, -2.6), (2, -4.4), (-3, -4.4), (-6.4, -1.6)], 'band', lo=0.3, hi=0.9)))
O('MARISOL', garment='trousers', tall=1, broad=1, shirt_v=3, shirt_mat='shirt', ow_acc=band('band', -6, -5, knot=False),
  ow_hair=dict(fringe=[1, 0, 1, 0, 1, 0, 1, 0, 1, 0], sides=1, back=3, vol=1.2))

# ---- Teo
TEO_M = dict(top='#5c5f6e', scarf='#8a8c98', shirt='#a8483c', legs='#3a3a48', shoes='#3a3440')
add('TEO', tt=['HOLLOW_TEO'], exprs=STD + ['smug'], P=dict(
    skin='#c98a5e', hair='#2a2026', eye='#5a3a22', age='teen', jaw='sharp', shoulders='normal', rest_mouth='smirk', mats=TEO_M,
    outfit=PO('none', extra=lambda b: (b.c.poly([(10, 40), (20, 37), (30, 37), (39, 40), (37, 46), (24, 47), (12, 46)], 'scarf', lo=0.3, hi=0.95),
                                        b.c.stroke([(14, 42), (24, 44), (35, 42)], dt=-0.3, only='scarf'))),
    **PH([(8, 27), (11, 28), (12, 21), (15, 17), (19, 20), (22, 16), (26, 19), (30, 15.5), (34, 18), (38, 18), (40, 23)], vol=3.2, top=1.2,
         blobs_f=[(14, 6, 4, 3.6), (22, 3, 4.2, 3.6), (31, 3.5, 4, 3.6), (38, 9, 3.6, 3.6), (9, 12, 3.6, 3.6)], sh=[[(12, 6), (14, 4)], [(20, 2), (23, 1)]])))
T('TEO', skin='#c98a5e', hair='#2a2026', eye='#4a2a12', H=51, sw=5.6, hw=4.4, ra=1.8, rl=2.3, head=(5.4, 6.0), pose='point', eye_h=2, brow_t=1, mouth_t='smile', mats=TEO_M,
  garment=TG(hem=0.36, flare=1.2, shirt='shirt', shirt_len=6), collar=T_shawl('scarf', 4),
  hairdo=TH(MID_T, 1.8, 1.0, blobs=[(-4, -6, 2.6, 2.4), (0, -7.5, 2.8, 2.4), (4, -6, 2.6, 2.4)], hi=[(-4, -7), (0, -9), (1, -9)]))
O('TEO', garment='coat', tall=1, ow_hair=dict(fringe=[1, 0, 1, 0, 1, 0, 1, 0, 1, 0], sides=1, vol=2.0, top=1, spikes=[(-6, -6), (-3, -8), (1, -9), (4, -8), (6, -5)]),
  ow_body=ow_body(fn_any=ow_cape('scarf', 2)))

# ---- Rook
ROOK_M = dict(top='#5a6ae0', holo='#e070c8', shirt='#26222e', legs='#26222e', shoes='#f0f0f4', under='#5a4a40')


def rook_hair_after(b):
    c = b.c
    c.poly([(8, 22), (12, 21), (14, 13), (10, 12)], 'under', lo=0.2, hi=0.6)     # shaved side


def rook_outfit(b):
    c = b.c
    v_neck(b, 'shirt', depth=48)
    collar_high(b, 'top', lift=1)
    c.stroke([(13, 44), (18, 38)], new='holo', only='top', tone=0.8); c.stroke([(33, 38), (36, 45)], new='holo', only='top', tone=0.6)
    c.pxs([(8, 45), (9, 46), (40, 44)], (120, 240, 250))


add('ROOK', tt=['LEADER_ROOK'], exprs=FULL, P=dict(
    skin='#efc9a8', hair='#f2e6b8', eye='#3a70c0', age='teen', jaw='sharp', sparkle=True, rest_mouth='smile', mats=ROOK_M, outfit=rook_outfit,
    **PH([(8, 20), (12, 20), (14, 14), (18, 18), (22, 13), (27, 17), (31, 12), (35, 15), (38, 12), (41, 17)], vol=2.6, top=2.4,
         front=[[(24, 2), (40, -2), (44, 6), (38, 13), (30, 8)], [(30, 12), (36, 12), (34, 24), (31, 22)]], after=rook_hair_after,
         sh=[[(16, 6), (22, 2), (30, 0)]], st=[[(22, 6), (20, 13)], [(30, 4), (31, 12)]])))
T('ROOK', skin='#efc9a8', hair='#f2e6b8', eye='#2a60b0', H=51, sw=5.8, hw=4.2, ra=1.8, rl=2.2, head=(5.4, 6.0), pose='raise', eye_h=2, brow_t=1, mouth_t='open', mats=ROOK_M,
  cuff=0.8, garment=TG(shirt='shirt', shirt_len=8, extra=lambda f: (f.c.stroke([jp(f, 'sh', -4, 2), jp(f, 'hip', -4, 0)], new='holo', only='top', tone=0.8),
                                                                   f.c.stroke([jp(f, 'sh', 4, 2), jp(f, 'hip', 4, 0)], new='holo', only='top', tone=0.6))),
  collar=T_collar('top', 3.5), detail=t_drone,
  hairdo=TH(HIGH_T, 1.6, 1.6, locks=[[(-3, -8), (5, -10), (7, -5), (2, -4)], [(2, -2), (4.6, -2), (4, 4), (2.6, 3)]], hi=[(-2, -9), (0, -10), (2, -10), (4, -9)],
            after=lambda f: hlock(f, [(-6.5, -2), (-5.6, -6), (-4.4, -6), (-5, -1)], 'under', lo=0.2, hi=0.6)))
O('ROOK', garment='trousers', shirt_v=3, ow_hair=dict(fringe=[0, 0, 0, 1, 1, 2, 1, 0, 0, 0], line=-3, sides=0, vol=1.6, top=2, spikes=[(1, -10), (2, -10), (3, -9), (4, -9)]),
  ow_body=ow_body(fn_any=lambda c, d, t, x0, x1: c.stroke([(x0, t + 1), (x0, t + 4)], new='holo', tone=0.8) if d != 'up' else None))

# ---- Dex
DEX_M = dict(top='#e86a3a', cap='#3a8ac8', legs='#5a6a8a', shoes='#e8e0d0', can='#e84a5a')
add('DEX', exprs=['neutral', 'happy', 'shocked'], P=dict(
    skin='#a8704a', hair='#2a2024', eye='#3a2a1a', age='teen', jaw='round', sparkle=True, rest_mouth='smile', mats=DEX_M, extras=freckles,
    outfit=PO('none', extra=lambda b: v_neck(b, 'cap', depth=46)),
    **PH([(8, 26), (12, 27), (12, 20), (22, 18), (36, 18), (40, 22)], vol=1.6,
         after=lambda b: (b.c.poly([(7, 18), (8, 7), (16, 2), (32, 2), (40, 7), (41, 17)], 'cap', lo=0.3, hi=0.95),
                          b.c.poly([(-2, 14), (8, 11), (10, 18), (0, 19)], 'cap', lo=0.2, hi=0.6)))))
T('DEX', skin='#a8704a', hair='#2a2024', eye='#2a1a0a', H=40, sw=4.4, hw=3.6, ra=1.5, rl=2.0, head=(5.6, 5.8), pose='raise', ball=False, eye_h=3, mouth_t='open', mats=DEX_M,
  legs='shorts', sleeve_len=0.5, detail=lambda f: f.c.stamp(["kk", "rr", "Rr", "rr", "kk"], int(f.J['haL'][0]) - 1, int(f.J['haL'][1]) - 4,
                                                             {'k': (200, 200, 210), 'r': (232, 74, 90), 'R': (255, 150, 150)}),
  hairdo=TH(SHORT_T, 0.8, after=T_hat([(-5.6, -3), (-5, -7), (-1, -8.4), (3.5, -7.6), (5.6, -5), (6, -2.6)], [(5, -4), (10, -3.6), (10, -2), (5, -2.4)], 'cap')))
O('DEX', garment='shorts', sleeve_len=0.5, ow_hair=dict(fringe=[0] * 10, sides=1, vol=0.6), ow_acc=ow_hat('cap', crown=2))

# ---- Sable / Kroll
SAB_M = dict(top='#4a4c5a', shirt='#2a2832', legs='#2a2832', shoes='#1f1d26', band='#c8504a')
add('SABLE', tt=['HOLLOW_SABLE', 'MERIDIAN_KROLL'], exprs=STD + ['smug'], P=dict(
    skin='#efd6c4', hair='#e2dccb', eye='#5a8a9a', age='adult', jaw='sharp', rest_mouth='smile', eye_tilt=1, lashes=True, mats=SAB_M,
    outfit=PO('high', inner='shirt', extra=lambda b: b.c.stroke([(12, 44), (16, 41), (20, 44)], new='band', only='top', tone=0.6)),
    extras=p_scar([(33, 17), (33, 18), (32, 19), (32, 20)]),
    **PH([(8, 33), (11, 34), (12, 22), (16, 15.5), (24, 13), (30, 16), (34, 22), (36, 26), (38, 29), (40, 33)], vol=1.6,
         front=[[(26, 13), (36, 15), (40, 30), (37, 34), (33, 22)]], sh=[[(12, 14), (17, 10), (22, 9)]], st=[[(30, 15), (34, 26)], [(14, 18), (11, 30)]])))
T('SABLE', skin='#efd6c4', hair='#e2dccb', eye='#4a7a8a', H=53, sw=5.4, hw=4.4, ra=1.7, rl=2.3, head=(5.2, 6.0), pose='crossed', ball=False, eye_h=2, brow_t=1, mouth_t='smile', mats=SAB_M,
  boots=6, gloves='shirt', garment=TG(hem=0.30, flare=1.6, shirt='shirt', shirt_len=6, belt='shirt'),
  hairdo=TH([(-6.5, 2), (-5.6, 0), (-4, -3.4), (0, -4.4), (2.4, -2), (3.6, 1), (4, 5.6), (7, 6)], 0.9, 0.2, locks=[[(1, -4), (5, -2.6), (5.6, 6), (3.6, 6.6)]], hi=[(-3, -6), (-2, -6), (-1, -6)]))
O('SABLE', garment='coat', tall=1, gloves='shirt', ow_hair=dict(fringe=[0, 0, 1, 1, 1, 2, 2, 2, 1, 1], line=-2, sides=3, vol=1.0))

# ---- Valen
VAL_M = dict(top='#eceae4', trim='#c8a050', glove='#8a8c98', legs='#d8d6d0', shoes='#6a6070', shirt='#c8a050')


def valen_outfit(b):
    c = b.c
    collar_high(b, 'top', lift=2)
    c.stroke([(14, 33), (19, 36), (23, 46)], new='trim', only='top', tone=0.7)
    c.stroke([(36, 33), (31, 37), (28, 46)], new='trim', only='top', tone=0.5)
    c.poly([(22, 45), (29, 45), (28, 48), (23, 48)], 'trim', lo=0.4, hi=0.9)


add('VALEN', tt=['CHAMPION_VALEN'], exprs=FULL, P=dict(
    skin='#dcae8a', hair='#e4e4ea', eye='#6a7a8a', age='old', jaw='broad', shoulders='broad', neck_w=6, nose='strong', bags=True, brow_thick=True, brow='#a8a8b8',
    rest_brow=(1, 0), mats=VAL_M, outfit=valen_outfit, extras=lambda b, e: wrinkles(b, e),
    **PH([(8, 22), (11, 22), (12, 16.5), (18, 14.5), (26, 14), (33, 15), (38, 17.5), (40, 20)], vol=0.8, st=[[(16, 10), (16, 14)], [(22, 8), (22, 13)], [(30, 9), (30, 13)]])))
T('VALEN', skin='#dcae8a', hair='#e4e4ea', eye='#5a6a7a', H=58, sw=7.6, hw=5.4, ra=2.3, rl=2.7, head=(5.4, 6.0), pose='relaxed', ball=False, eye_h=1, brow_t=1, brow='#a8a8b8', nose_t=2,
  mats=VAL_M, legs='robe', glove_L='glove', cuff=1.0,
  garment=TG(hem=0.02, flare=3.4, open_front=True, belt='trim', extra=lambda f: (f.c.stroke([jp(f, 'sh', -1, 0), jp(f, 'hip', -2, 26)], new='trim', only='top', tone=0.7))),
  collar=T_collar('top', 4.5), hairdo=TH([(-6.5, -2.4), (-4, -4.0), (-1, -4.4), (2, -3.6), (3.4, -1), (3.8, 1.6), (7, 2)], 0.4, hi=[(-3, -6), (-2, -6), (-1, -6)]))
O('VALEN', garment='robe', tall=2, broad=1, gloves='glove', ow_hair=dict(fringe=[0] * 10, line=-3, sides=0, vol=0.3))
CAST['VALEN']['O']['gloves'] = 'skin'

# ================================================================ WARDENS
# ---- Sahar
SAH_M = dict(top='#8a6a4a', kef='#e4d6b4', shirt='#5a7a6a', legs='#6a5a48', shoes='#5a4636')
_kb, _kf = hood_P('kef', open_line=[(6, 44), (10, 38), (11.5, 23), (15, 14.5), (23, 11), (31, 12), (37, 17), (39.5, 27), (41, 40), (44, 44)], vol=3.5)


def kef_pattern(b, e=None):
    c = b.c
    for y in range(2, 48, 4):
        for x in range(0, 48, 4):
            xx = x + (2 if (y // 4) % 2 else 0)
            if 0 <= xx < 48 and c.mat[y, xx] == c.m('kef') and c.ovr[y, xx, 3] == 0:
                c.px(xx, y, (170, 70, 60))


add('SAHAR', tt=['LEADER_SAHAR'], exprs=STD, P=dict(
    skin='#b07a52', hair='#6a6a72', eye='#4a3a2a', age='old', jaw='long', nose='strong', mats=SAH_M, rest_mouth='smile', gaunt=True,
    hair_back=_kb, hair_front=chain(PH([(8, 26), (12, 26), (13, 18), (24, 15), (36, 18), (40, 24)], vol=0.5)['hair_front'], _kf),
    outfit=PO('high', inner='shirt'), extras=lambda b, e: (wrinkles(b, e), kef_pattern(b), glasses(b, col=(160, 140, 90)))))
T('SAHAR', skin='#b07a52', hair='#6a6a72', eye='#3a2a1a', H=50, sw=5.4, hw=4.6, ra=1.7, rl=2.3, head=(5.2, 6.0), pose='chin', ball=False, eye_h=1, brow_t=1, nose_t=2, mats=SAH_M,
  garment=TG(hem=0.12, flare=2.6, shirt='shirt', shirt_len=5, belt='kef'), hairdo=chain(T_hood('kef', 2.0), t_glasses((160, 140, 90))))
O('SAHAR', garment='coat', tall=1, hem=1, ow_hair=dict(fringe=[0] * 10, sides=0, vol=0.4), ow_acc=ow_hood('kef'))

# ---- Corvin + Wenlow
COR_M = dict(top='#4a4a3a', shirt='#8a9a7a', legs='#3a3a32', shoes='#2a2826', beak='#d8ccb0', lens='#7ad0a0', hat='#2a2826')
add('CORVIN', tt=['LEADER_CORVIN'], exprs=FULL, P=dict(
    skin='#e6ccb4', hair='#2a2a30', eye='#6a9a5a', age='adult', jaw='long', gaunt=True, bags=True, nose='strong', rest_brow=(0, -1), rest_mouth='smirk', mats=COR_M,
    outfit=PO('high', inner='shirt', lift=2),
    **PH([(8, 30), (11, 31), (12, 20), (16, 17), (20, 21), (24, 15.5), (29, 20), (34, 16), (38, 20), (40, 26)], vol=1.6,
         front=[[(10, 21), (13, 21), (12, 33), (9, 31)]], st=[[(19, 12), (18, 19)], [(29, 11), (30, 18)]], after=p_beak_up)))
T('CORVIN', skin='#e6ccb4', hair='#2a2a30', eye='#5a8a4a', H=57, sw=5.4, hw=4.0, ra=1.6, rl=2.1, head=(5.0, 6.1), pose='chin', ball=False, eye_h=1, brow_t=1, nose_t=2, mats=COR_M,
  cuff=0.8, boots=6, garment=TG(hem=0.10, flare=3.4, shirt='shirt', shirt_len=5), collar=T_collar('top', 5),
  hairdo=TH(MID_T, 1.0, 0.4, hi=[(-3, -6), (-2, -6)],
            after=lambda f: (hlock(f, [(-5.8, 0.6), (-3, -0.6), (-1.2, 0.6), (-1, 2.6), (-7.8, 6.4), (-8.2, 5.6)], 'beak', lo=0.3, hi=0.9),
                             t_px([(-4, 0), (-1, 0)], (122, 208, 160))(f))))
O('CORVIN', garment='coat', tall=1, hem=1, ow_hair=dict(fringe=[1, 0, 1, 1, 0, 1, 0, 1, 1, 0], sides=3, vol=1.0),
  ow_acc=ow_px(pts_down=[(-1, 2, (216, 204, 176)), (0, 2, (216, 204, 176)), (-1, 3, (216, 204, 176)), (0, 3, (216, 204, 176)), (0, 4, (180, 170, 150))],
               pts_left=[(-5, 2, (216, 204, 176)), (-6, 2, (216, 204, 176)), (-6, 3, (180, 170, 150))]))

WEN2_M = dict(top='#e8e4d8', shirt='#8a9a7a', legs='#5a5a4a', shoes='#4a3a30', band='#6a8ab8')
add('WENLOW', exprs=STD + ['panic'], P=dict(
    skin='#f2d0b0', hair='#d8a050', eye='#4a6a9a', age='teen', jaw='round', rest_mouth='smile', sparkle=True, mats=WEN2_M, extras=freckles, outfit=PO('high', inner='shirt'),
    **PH([(8, 27), (11, 28), (12, 21), (15, 17), (19, 22), (23, 16.5), (27, 21), (31, 16), (35, 20), (38, 18), (40, 23)], vol=2.6, top=1.4,
         front=[[(22, 3), (25, -3), (29, 3)], [(30, 4), (36, -1), (35, 6)]], sh=[[(12, 13), (16, 9), (21, 7)]], st=[[(21, 10), (21, 17)], [(29, 10), (29, 16)]])))
T('WENLOW', skin='#f2d0b0', hair='#d8a050', eye='#3a5a8a', H=48, sw=5.0, hw=4.0, ra=1.6, rl=2.2, head=(5.5, 6.0), pose='raise', ball=False, eye_h=2, mouth_t='open', mats=WEN2_M,
  garment=TG(hem=0.30, flare=2.0, shirt='shirt', shirt_len=6),
  detail=lambda f: f.c.stamp(["ww", "gg", "gg"], int(f.J['haL'][0]) - 1, int(f.J['haL'][1]) - 4, {'w': (240, 240, 244), 'g': (122, 208, 160)}),
  hairdo=TH(MID_T, 1.6, 1.0, locks=[[(-1, -7), (2, -10.5), (3, -6)]], hi=[(-3, -7), (-2, -7), (-1, -8)]))
O('WENLOW', garment='coat', ow_hair=dict(fringe=[1, 1, 0, 1, 1, 0, 1, 1, 0, 1], sides=2, vol=1.6, top=1, spikes=[(0, -9), (1, -10), (-3, -8)]))

# ---- Brann
BRA_M = dict(top='#7a4a3a', apron='#5a4a40', legs='#4a3a32', shoes='#3a2a24', ring='#c8a050')


def brann_beard(b):
    beard('hair', full=True)(b)
    c = b.c
    c.poly([(19, 40), (31, 40), (29, 48), (21, 48)], 'hair', lo=0.3, hi=0.8, edge=False)
    for y in (42, 45):
        c.stroke([(21, y), (29, y)], new='ring', only='hair', tone=0.7)


add('BRANN', tt=['LEADER_BRANN'], exprs=FULL, P=dict(
    skin='#d08a62', hair='#c25a2a', eye='#4a3a2a', age='old', jaw='broad', shoulders='broad', neck_w=7, nose='strong', brow_thick=True, rest_mouth='smile', mats=BRA_M,
    under_face=brann_beard, outfit=lambda b: (b.c.poly([(10, 41), (15, 40), (19, 48), (12, 48)], 'apron', lo=0.3, hi=0.8),
                                              b.c.poly([(33, 40), (38, 41), (38, 48), (31, 48)], 'apron', lo=0.2, hi=0.6)),
    extras=lambda b, e: wrinkles(b, e),
    **PH([(8, 22), (11, 22), (12, 16), (18, 13.5), (26, 13), (33, 14), (38, 17), (40, 20)], vol=1.2, st=[[(16, 8), (14, 14)], [(24, 6), (24, 12)], [(31, 7), (33, 13)]])))
T('BRANN', skin='#d08a62', hair='#c25a2a', eye='#3a2a1a', H=60, sw=8.4, hw=6.0, ww=6.6, ra=2.7, rl=3.2, head=(5.8, 6.0), pose='hips', ball=False, eye_h=1, brow_t=1, nose_t=2, mats=BRA_M,
  sleeve_len=0.45, garment=lambda f: (f.c.poly([jp(f, 'sh', -4, 2), jp(f, 'sh', 3.5, 2), jp(f, 'hip', 6, 0), jp(f, 'hip', 6.5, 16), jp(f, 'hip', -6.5, 16), jp(f, 'hip', -6, 0)], 'apron', lo=0.3, hi=0.9),
                                      f.c.stroke([jp(f, 'hip', 0, 4), jp(f, 'hip', -0.5, 15)], dt=-0.3, only='apron')),
  hairdo=chain(TH([(-6.5, -2), (-4, -3.6), (-1, -4.0), (2, -3.4), (3.4, -1), (3.8, 2), (7, 3)], 0.8),
               lambda f: (hlock(f, [(-6, 1.5), (-3, 3), (1, 3), (4.2, 1), (4.6, 5), (1.4, 9), (0, 15), (-3, 15), (-3.4, 9), (-6, 5)], 'hair', lo=0.25, hi=0.85),
                          f.c.stroke([jp(f, 'head', -3.4, 11), jp(f, 'head', 0, 11)], new='ring', only='hair', tone=0.7),
                          t_px([(-3, 4), (-2, 4)], (120, 60, 50))(f))))
O('BRANN', garment='trousers', tall=2, broad=1, sleeve_len=0.5, ow_hair=dict(fringe=[0] * 10, line=-3, sides=1, vol=0.8), ow_acc=ow_beard('hair'),
  ow_body=ow_body(fn_down=lambda c, t, x0, x1: (c.paint(R(c, x0 + 1, t + 2, x1 - 1, 20), 'apron', 0.5, edge=False), c.paint(R(c, 6, t - 1, 9, t + 3), 'hair', 0.5, edge=False))))

# ---- Kaito
KAI_M = dict(top='#3a3a44', wrap='#e8e4d8', legs='#2e2e38', shoes='#26242c', shirt='#3a3a44')
add('KAITO', tt=['LEADER_KAITO'], exprs=STD + ['crying'], P=dict(
    skin='#d6a07a', hair='#2a2628', eye='#3a2a1a', age='adult', jaw='broad', shoulders='broad', neck_w=7, rest_brow=(1, 0), rest_mouth='line', mats=KAI_M,
    outfit=PO('none', extra=lambda b: b.c.poly([(17, 40), (32, 40), (27, 48), (23, 48)], 'skin', tone=0.45)),
    extras=p_scar([(33, 30), (34, 31), (35, 32), (35, 33), (34, 34), (33, 35), (32, 36)]),
    **PH([(9, 21), (11, 21), (12, 15.5), (24, 13), (37, 15), (39.6, 19)], vol=0.4, st=[[(14, 9), (14, 13)], [(20, 7), (20, 12)], [(26, 7), (26, 12)], [(32, 8), (32, 12)]])))
T('KAITO', skin='#d6a07a', hair='#2a2628', eye='#2a1a0a', H=55, sw=7.0, hw=4.8, ra=2.2, rl=2.7, head=(5.2, 5.9), pose='fist', ball=False, eye_h=1, brow_t=2, mats=KAI_M,
  sleeve_len=0.0, gloves='wrap', garment=TG(belt='wrap', extra=lambda f: f.c.poly([jp(f, 'sh', -2, -1), jp(f, 'sh', 2, -1), jp(f, 'sh', 0, 4)], 'skin', tone=0.45)),
  hairdo=chain(TH([(-6.5, -3), (-4, -4.4), (-1, -4.8), (2, -4), (3.4, -1.6), (3.8, 1), (7, 2)], 0.3), t_px([(1, 3), (0, 4), (-1, 5)], (214, 132, 130))))
O('KAITO', garment='trousers', tall=1, broad=1, sleeve_len=0.0, gloves='wrap', ow_hair=dict(fringe=[0] * 10, line=-4, sides=0, vol=0.3))

# ---- Anja
ANJ_M = dict(top='#6a5444', fur='#d8cfc0', legs='#4a4a5a', shoes='#3a3440', shirt='#5a7a9a')
add('ANJA', tt=['LEADER_ANJA'], exprs=STD + ['smug'], P=dict(
    skin='#efc8b0', hair='#c8c0a8', eye='#5a8aa8', age='adult', jaw='broad', shoulders='broad', neck_w=6, brow='#f0f4fa', brow_thick=True, rest_mouth='flat', mats=ANJ_M,
    outfit=PO('none', extra=lambda b: (b.c.poly([(2, 48), (4, 41), (14, 37), (22, 40), (24, 48)], 'fur', lo=0.4, hi=0.95), b.c.poly([(26, 48), (28, 40), (35, 37), (44, 41), (46, 48)], 'fur', lo=0.2, hi=0.7))),
    extras=lambda b, e: (wrinkles(b, e), p_pipe()(b) if e not in ('angry', 'crying', 'shocked', 'panic', 'happy') else None),
    **PH([(8, 26), (11, 27), (12, 19), (17, 15), (24, 14), (31, 15), (37, 18), (40, 22)], vol=1.4, back=[[(7, 24), (3, 38), (8, 44), (11, 30)]],
         st=[[(16, 9), (14, 16)], [(30, 8), (33, 15)]], sh=[[(13, 13), (17, 9), (22, 8)]])))
T('ANJA', skin='#efc8b0', hair='#c8c0a8', eye='#4a7a98', H=52, sw=7.4, hw=5.6, ww=6.0, ra=2.4, rl=2.8, head=(5.4, 5.9), pose='crossed', ball=False, eye_h=1, brow_t=1, brow='#f0f4fa', mats=ANJ_M,
  boots=7, garment=TG(hem=0.16, flare=3.0, open_front=True), collar=T_shawl('fur', 4),
  detail=t_px([(-3, 4), (-4, 5), (-5, 5), (-6, 4), (-6, 3)], (120, 80, 60)),
  hairdo=TH(HIGH_T, 0.8, locks=[[(3, 1), (6, 2), (6.6, 12), (4, 12)]], hi=[(-3, -6), (-2, -6)]))
O('ANJA', garment='coat', tall=1, broad=1, boots=1, ow_hair=dict(fringe=[0] * 10, line=-3, sides=2, back=2, vol=0.8), ow_body=ow_body(fn_any=ow_cape('fur', 2)))

# ---- Odessa
ODE_M = dict(top='#8a5a3a', scarf='#d84a3a', shirt='#e8dcc4', legs='#5a5048', shoes='#3a2a24')
add('ODESSA', tt=['LEADER_ODESSA'], exprs=STD + ['smug', 'panic'], P=dict(
    skin='#d8a882', hair='#2a3a5a', eye='#a0602a', age='adult', jaw='soft', lashes=True, eye_tilt=1, rest_mouth='smirk', rest_brow=(0, -1), mats=ODE_M,
    outfit=PO('none', extra=lambda b: (b.c.poly([(8, 41), (20, 37.5), (32, 37.5), (40, 40.5), (38, 46), (25, 47), (10, 46)], 'scarf', lo=0.3, hi=0.95),
                                        b.c.poly([(34, 42), (44, 38), (47, 44), (38, 47)], 'scarf', lo=0.2, hi=0.7))),
    extras=p_scar([(16, 17), (17, 18), (18, 19)]),
    **PH([(8, 27), (11, 28), (12, 21), (15, 18), (18, 22), (22, 17), (26, 20), (30, 16), (34, 19), (38, 17), (40, 22)], vol=2.6, top=1,
         front=[[(36, 8), (46, 4), (44, 12)], [(38, 14), (47, 14), (42, 19)]], after=p_goggles())))
T('ODESSA', skin='#d8a882', hair='#2a3a5a', eye='#904a1a', H=53, sw=5.8, hw=4.4, ra=1.8, rl=2.3, head=(5.3, 6.0), pose='ball', eye_h=2, brow_t=1, mouth_t='smile', mats=ODE_M,
  boots=5, garment=TG(hem=0.40, flare=1.4, shirt='shirt', shirt_len=6, belt='legs'), collar=T_shawl('scarf', 3),
  hairdo=TH(MID_T, 1.6, 0.8, locks=[[(3, -5), (10, -6), (6, -1)], [(4, -1), (10, 1), (5, 3)]],
            after=lambda f: (hlock(f, [(-6.6, -4.6), (4, -6.4), (4.4, -4.6), (-6.4, -2.8)], 'shoes', lo=0.3, hi=0.7),
                             f.c.pxs([(int(f.J['head'][0]) - 4, int(f.J['head'][1]) - 5), (int(f.J['head'][0]) - 1, int(f.J['head'][1]) - 5)], (150, 210, 220)))))
O('ODESSA', garment='coat', tall=1, ow_hair=dict(fringe=[1, 0, 1, 0, 1, 1, 0, 1, 0, 1], sides=2, vol=1.6, spikes=[(6, -3), (7, -2), (-7, -2)]), ow_acc=ow_goggles(),
  ow_body=ow_body(fn_any=ow_cape('scarf', 2)))

# ---- Ilsa
ILS_M = dict(top='#3a4a7a', trim='#c8b070', muff='#e8e4f0', legs='#2a3050', shoes='#2a2832')
add('ILSA', tt=['LEADER_ILSA'], exprs=FULL, P=dict(
    skin='#f2dcd0', hair='#e6dcc0', eye='#7a5ab0', age='adult', jaw='sharp', lashes=True, rest_mouth='flat', eye_tilt=1, rest_brow=(0, 0), mats=ILS_M,
    outfit=PO('high', lift=3, extra=lambda b: b.c.stroke([(14, 32), (19, 35)], new='trim', only='top', tone=0.7)),
    **PH([(8, 24), (11, 25), (12, 18), (17, 15), (22, 18), (27, 14), (33, 15), (38, 18), (40, 22)], vol=1.8, blobs_b=[(36, 6, 6, 5.5)],
         st=[[(22, 10), (21, 17)]], sh=[[(13, 13), (17, 9), (22, 8)]],
         after=chain(p_earmuffs(), lambda b: b.c.pline([(32, 1), (40, 8)], (220, 170, 70))))))
T('ILSA', skin='#f2dcd0', hair='#e6dcc0', eye='#6a4aa0', H=53, sw=5.0, hw=4.2, ra=1.6, rl=2.1, head=(5.2, 6.0), pose='clasp', ball=False, eye_h=2, brow_t=1, mouth_t='line', mats=ILS_M,
  legs='robe', garment=TG(hem=0.02, flare=2.8, open_front=False, belt='trim'), collar=T_collar('top', 5.5),
  hairdo=TH(HIGH_T, 0.9, 0.4, blobs=[(5, -5, 2.6, 2.6)], hi=[(-3, -6), (-2, -6), (-1, -6)],
            after=lambda f: (hblob(f, 5.2, 1.4, 1.8, 2.2, 'muff'), hlock(f, [(-4, -6.5), (4.6, -6.5), (5.4, 0), (4.4, 0), (3.6, -5.4), (-4, -5.4)], 'muff', lo=0.4, hi=0.9))))
O('ILSA', garment='robe', tall=1, ow_hair=dict(fringe=[1, 1, 0, 1, 1, 0, 0, 0, 0, 0], line=-3, sides=1, vol=1.0, spikes=[(4, -7), (5, -7), (5, -6)]),
  ow_acc=ow_px(pts_down=[(-6, 1, (232, 228, 240)), (-6, 2, (232, 228, 240)), (5, 1, (232, 228, 240)), (5, 2, (232, 228, 240))], pts_left=[(2, 1, (232, 228, 240)), (2, 2, (232, 228, 240))]))

# ---- Bastian
BAS_M = dict(top='#6a5a4a', shirt='#9a8a6a', legs='#4a4038', shoes='#3a2e26', hat='#c8a83a', lampc='#4a4a50', lamp='#f8e8a0')
add('BASTIAN', tt=['LEADER_BASTIAN'], exprs=STD, P=dict(
    skin='#d8a882', hair='#dcdce4', eye='#5a5040', age='old', jaw='broad', shoulders='broad', neck_w=6, nose='strong', brow_thick=True, brow='#e8e8f0', rest_mouth='smile', mats=BAS_M,
    under_face=beard('hair', full=False, stache=True), outfit=PO('none', inner='shirt'),
    extras=lambda b, e: (wrinkles(b, e, heavy=True), p_pipe((200, 190, 170))(b) if e in ('neutral', 'deadpan', 'sad') else None),
    **PH([(8, 26), (11, 27), (12, 21), (24, 20), (40, 22)], vol=1.4, after=p_lamp_hat)))
T('BASTIAN', skin='#d8a882', hair='#dcdce4', eye='#4a4030', H=48, sw=6.6, hw=5.6, ww=5.6, ra=2.3, rl=2.6, head=(5.6, 5.8), pose='stoop', ball=False, eye_h=1, brow_t=1, brow='#e8e8f0', nose_t=2,
  mats=BAS_M, garment=TG(hem=0.30, flare=1.6, shirt='shirt', shirt_len=5), hands=None,
  hairdo=chain(TH([(-6.5, -1), (-3, -1.6), (2, -1.4), (3.4, 0), (3.8, 3), (7, 4)], 0.9), T_beard('hair', 0),
               T_hat([(-6, -2.6), (-5.6, -7), (-1, -8.6), (4, -8), (6.2, -5), (6.4, -2)], [(-8.4, -2), (6.8, -2.6), (6.8, -1), (-8.4, -0.6)], 'hat'),
               lambda f: (hblob(f, -2, -6, 1.6, 1.5, 'lamp', tone=0.9))))
O('BASTIAN', garment='trousers', tall=0, broad=1, ow_hair=dict(fringe=[0] * 10, sides=1, vol=0.8), ow_acc=chain(ow_beard('hair'), ow_hat('hat', crown=2),
  ow_px(pts_down=[(-1, -6, (248, 232, 160)), (0, -6, (248, 232, 160))], pts_left=[(-4, -6, (248, 232, 160))])))

# ---- Ysolde
YSO_M = dict(top='#26222e', hood='#2e2a38', shirt='#4a4458', legs='#26222e', shoes='#1e1a24')
_yb, _yf = hood_P('hood', vol=3.5)
add('YSOLDE', tt=['LEADER_YSOLDE'], exprs=STD + ['crying'], P=dict(
    skin='#f2e0dc', hair='#3a2e40', eye='#7a8ab0', age='adult', jaw='soft', lashes=True, eye_tilt=-1, rest_brow=(-1, 1), rest_mouth='line', mats=YSO_M, blush_col=(220, 170, 180),
    hair_back=_yb, hair_front=chain(PH([(8, 30), (12, 31), (13, 21), (18, 17), (24, 20), (30, 17), (36, 20), (40, 28)], vol=1.0)['hair_front'], _yf, p_veil),
    outfit=PO('high', lift=2, extra=lambda b: [b.c.px(x, 46, (90, 80, 100)) for x in range(14, 36, 2)])))
T('YSOLDE', skin='#f2e0dc', hair='#3a2e40', eye='#6a7aa0', H=53, sw=5.0, hw=4.4, ra=1.6, rl=2.2, head=(5.2, 6.0), pose='lantern', ball=False, eye_h=2, brow_t=3, mouth_t='line', mats=YSO_M,
  legs='robe', cuff=1.2, garment=TG(hem=0.0, flare=3.8, open_front=False), detail=t_lantern, hairdo=T_hood('hood', 2.2))
O('YSOLDE', garment='robe', tall=1, ow_hair=dict(fringe=[1, 0, 1, 1, 0, 1, 0, 1, 1, 0], sides=3, vol=0.6), ow_acc=ow_hood('hood'))

# ---- Magnus
MAG_M = dict(top='#7a7c88', shirt='#eceef2', legs='#4a4c58', shoes='#2a2830', tie='#3a5a7a', metal='#b8bcc8', chainc='#d8c070')
add('MAGNUS', tt=['LEADER_MAGNUS'], exprs=STD + ['smug'], P=dict(
    skin='#e8c4a4', hair='#6a5a52', eye='#5a6a7a', age='adult', jaw='long', nose='medium', rest_mouth='flat', mats=MAG_M,
    under_face=beard('hair', full=False, stache=True),
    outfit=PO('none', inner='shirt', extra=lambda b: (b.c.poly([(24, 40), (27, 40), (27.5, 48), (23.5, 48)], 'tie', lo=0.3, hi=0.8),
                                                       b.c.pline([(32, 44), (36, 46), (40, 45)], (216, 192, 112)))),
    extras=lambda b, e: wrinkles(b, e),
    **PH([(8, 24), (11, 25), (12, 17), (16, 14), (24, 13), (31, 14), (36, 16), (39, 19), (40, 21)], vol=1.0,
         st=[[(20, 7), (32, 9)], [(15, 10), (13, 17)]], sh=[[(14, 11), (18, 8), (23, 7)]])))
T('MAGNUS', skin='#e8c4a4', hair='#6a5a52', eye='#4a5a6a', H=55, sw=6.0, hw=4.6, ra=1.8, rl=2.4, head=(5.2, 6.0), pose='chin', ball=False, eye_h=1, brow_t=1, mats=MAG_M,
  sleeve='shirt', glove_R='metal',
  garment=TG(shirt='shirt', shirt_len=4, tie='tie', extra=lambda f: f.c.stroke([jp(f, 'waist', -2, -2), jp(f, 'waist', 3, 0)], new='chainc', only='top', tone=0.7)),
  hairdo=chain(TH(HIGH_T, 0.6, hi=[(-3, -6), (-2, -6), (-1, -6)]), t_px([(-4, 3), (-3, 3), (-2, 3), (-1, 3)], (90, 74, 66))))
O('MAGNUS', garment='trousers', tall=1, shirt_v=3, sleeve='shirt', ow_hair=dict(fringe=[0] * 10, line=-3, sides=1, vol=0.6))

# ---- Nyx
NYX_M = dict(top='#4a2a5a', fur='#2a2236', legs='#2a2236', shoes='#1e1a24', shirt='#2a2236', tights='#2a2236')
add('NYX', tt=['LEADER_NYX'], exprs=FULL, P=dict(
    skin='#b8846a', hair='#1e1a2a', eye='#d0a040', age='adult', jaw='sharp', lashes=True, eye_tilt=1, rest_mouth='smirk', rest_brow=(0, -1), lip=(150, 60, 90), mats=NYX_M,
    hair_contrast=1.3, outfit=PO('none', extra=lambda b: (b.c.poly([(2, 48), (4, 41), (14, 37.5), (21, 42), (24, 48)], 'fur', lo=0.35, hi=0.9),
                                                         b.c.poly([(26, 48), (29, 42), (35, 37.5), (44, 41), (46, 48)], 'fur', lo=0.2, hi=0.7))),
    extras=p_earring((232, 214, 140)),
    **PH([(8, 34), (11, 35), (12, 24), (15, 17), (22, 13.5), (28, 15), (33, 19), (37, 24), (40, 32)], vol=2.4,
         back=[[(6, 22), (0, 46), (12, 48), (12, 32)], [(38, 22), (46, 44), (40, 48), (36, 34)]],
         front=[[(20, 13), (30, 14), (37, 26), (33, 30), (29, 20)]], sh=[[(13, 14), (18, 9), (24, 8)]], st=[[(28, 14), (33, 24)]])))
T('NYX', skin='#b8846a', hair='#1e1a2a', eye='#c09030', H=54, sw=5.2, hw=4.6, ra=1.6, rl=2.2, head=(5.2, 6.0), pose='hips', ball=False, eye_h=2, brow_t=1, mouth_t='smile', mats=NYX_M,
  hair_contrast=1.3, legs='dress', tights=True, garment=TG(hem=0.12, flare=2.0, open_front=True), collar=T_shawl('fur', 4),
  hairdo=TH([(-6.5, 2), (-5.6, 0), (-4, -3.4), (0, -4.4), (2.4, -2), (3.6, 1), (4, 5.6), (7, 6)], 1.4, 0.4,
            locks=[[(2, -4), (6.4, -2), (7.6, 12), (4.4, 13)], [(-6.6, 0), (-5.4, 0), (-6, 9), (-8, 8)]], hi=[(-3, -6), (-2, -6), (-1, -6), (5, 2)],
            after=t_px([(4, 4), (4, 5)], (232, 214, 140))))
O('NYX', garment='dress', tights=True, tall=1, ow_hair=dict(fringe=[0, 0, 1, 1, 2, 2, 2, 1, 1, 1], line=-2, sides=5, back=3, vol=1.4))

# ---- Celestine
CEL_M = dict(top='#5a4a8a', gown='#8a7ab8', legs='#5a4a8a', shoes='#5a4a8a', shirt='#c8b8e8')
add('CELESTINE', tt=['LEADER_CELESTINE'], exprs=FULL, P=dict(
    skin='#f6dccc', hair='#d8b8e8', eye='#e0a040', age='teen', jaw='soft', lashes=True, sparkle=True, eye_tilt=-1, rest_mouth='smile', mats=CEL_M,
    outfit=PO('none', extra=lambda b: (v_neck(b, 'shirt', depth=46), b.c.poly([(4, 48), (8, 42), (16, 40), (12, 48)], 'gown', lo=0.4, hi=0.9))),
    extras=p_flowers(),
    **PH([(8, 30), (11, 31), (12, 22), (16, 18), (21, 21), (25, 16.5), (30, 20), (34, 17), (38, 21), (40, 28)], vol=2.4, top=0.6,
         back=[[(6, 20), (0, 48), (14, 48), (12, 30)], [(38, 20), (48, 48), (36, 48), (37, 30)]], sh=[[(12, 14), (17, 10), (23, 8)], [(4, 34), (6, 40)]],
         st=[[(21, 12), (20, 19)], [(30, 12), (31, 18)]])))
T('CELESTINE', skin='#f6dccc', hair='#d8b8e8', eye='#d09030', H=51, sw=4.8, hw=4.2, ra=1.5, rl=2.0, head=(5.3, 6.0), pose='raise', ball=False, eye_h=3, mouth_t='smile', mats=CEL_M,
  legs='robe', barefoot=True, sleeve='gown', garment=TG(hem=0.0, flare=4.4, open_front=False, mat='gown'),
  detail=lambda f: [f.c.px(x, y, c_) for (x, y), c_ in zip([jp(f, 'head', -5, -5), jp(f, 'head', 1, -7), jp(f, 'head', 6, -2), jp(f, 'head', 7, 6)], [(214, 150, 230), (250, 220, 120), (150, 200, 250), (250, 220, 120)])],
  hairdo=TH(MID_T, 1.4, 0.4, locks=[[(2, -2), (6.6, -1), (9, 22), (5, 22)], [(-6.6, 0), (-5.4, 0), (-7, 14), (-9, 13)]], hi=[(-3, -6), (-2, -7), (-1, -7), (6, 6), (7, 9)]))
O('CELESTINE', garment='robe', skirt_mat='gown', sleeve='gown', ow_hair=dict(fringe=[1, 1, 0, 1, 1, 0, 1, 1, 1, 1], sides=6, back=4, vol=1.4),
  ow_acc=ow_px(pts_down=[(-5, -4, (214, 150, 230)), (4, -5, (250, 220, 120))], pts_left=[(2, -5, (214, 150, 230))], pts_up=[(-3, -4, (150, 200, 250)), (3, -5, (214, 150, 230))]))

# ---- Sigrun
SIG_M = dict(top='#5a3a3a', armor='#3a4a3e', legs='#3a3036', shoes='#2a2226', shirt='#3a3036')
add('SIGRUN', tt=['LEADER_SIGRUN'], exprs=FULL, P=dict(
    skin='#e2b294', hair='#c23a26', eye='#c88a2a', age='adult', jaw='sharp', shoulders='broad', eye_tilt=1, rest_brow=(1, -1), rest_mouth='line', brow_thick=True, mats=SIG_M,
    outfit=p_armor, extras=p_scar([(10, 26), (11, 27), (12, 29), (13, 30), (14, 32), (15, 33), (16, 34), (14, 35), (12, 36)], (230, 150, 140)),
    **PH([(8, 22), (11, 22), (12, 17), (17, 15.5), (24, 15), (31, 15.5), (37, 17), (40, 20)], vol=1.0, after=p_braid_crown(), back=[[(36, 16), (44, 20), (46, 40), (40, 42), (40, 26)]])))
T('SIGRUN', skin='#e2b294', hair='#c23a26', eye='#b87a1a', H=57, sw=6.8, hw=4.8, ra=2.0, rl=2.6, head=(5.2, 6.0), pose='point', ball=False, eye_h=2, brow_t=2, mouth_t='line', mats=SIG_M,
  sleeve='armor', boots=8, cuff=0.8,
  garment=TG(hem=0.30, flare=2.4, mat='armor', open_front=True, extra=lambda f: f.c.poly([jp(f, 'sh', -8.5, 2), jp(f, 'sh', -7, -2), jp(f, 'sh', -3, -1), jp(f, 'sh', -3, 4)], 'armor', lo=0.3, hi=0.9)),
  hairdo=chain(TH(HIGH_T, 0.8, locks=[[(3, 0), (6.8, 2), (8, 16), (5, 16)]], hi=[(-3, -6), (-1, -7)]),
               lambda f: [hblob(f, dx, -6.0 + abs(dx) * 0.1, 1.5, 1.3, tone=0.85 if i % 2 else 0.5) for i, dx in enumerate((-5, -3, -1, 1, 3, 5))],
               t_px([(1, 1), (1, 2), (0, 3), (0, 4)], (230, 150, 140))))
O('SIGRUN', garment='coat', tall=1, skirt_mat='armor', sleeve='armor', ow_hair=dict(fringe=[0] * 10, line=-3, sides=1, back=4, vol=0.8),
  ow_acc=band('hair', -6, -5, knot=False))
