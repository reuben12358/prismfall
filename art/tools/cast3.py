"""cast3.py - protagonist + first-hour cast (data on top of the cast2 kit)."""
from cast2 import *
from cast2 import PH, PO, TH, TG

SHORT_T = [(-6.5, -2), (-5, -3.4), (-3, -2.4), (-1, -3.6), (1.5, -3), (3, -0.5), (3.8, 3), (7, 4)]
HIGH_T = [(-6.5, -3.4), (-4, -4.6), (-1, -4.8), (2, -3.6), (3.4, -0.8), (3.8, 3), (7, 4)]

# ------------------------------------------------------------ PLAYER A / B
PC_MATS = dict(top='#e6e4ec', trim='#2f9c94', shirt='#3b4258', legs='#4a5068', shoes='#2f9c94', bag='#8a6a4a', strap='#6a5040', tights='#3b4258')


def pc_outfit(b):
    c = b.c
    collar_high(b, 'top', lift=-1)
    c.poly([(14, 39), (20, 37.5), (31, 37.5), (35, 39.5), (36, 44), (26, 46), (13, 44)], 'trim', lo=0.3, hi=0.95)     # scarf
    c.stroke([(16, 41), (24, 43), (33, 41)], dt=-0.3, only='trim')
    c.poly([(30, 43), (35, 43), (36, 48), (31, 48)], 'trim', lo=0.25, hi=0.7)


def pc_T_detail(f):
    c = f.c
    sx, sy = f.J['sh']
    c.poly([(sx - 4.5, sy - 1.5), (sx + 4, sy - 1.5), (sx + 4.5, sy + 1.5), (sx - 1, sy + 2.6), (sx - 5, sy + 1.2)], 'trim', lo=0.3, hi=0.95)
    c.poly([(sx + 2, sy + 1.5), (sx + 4.4, sy + 1.5), (sx + 5, sy + 6), (sx + 3, sy + 6)], 'trim', lo=0.25, hi=0.7)
    wx, wy = f.J['waist']
    c.stroke([(wx - 5, wy + 3), (wx + 5, wy + 3.5)], new='trim', only='top', tone=0.6)
    satchel(f)


add('PLAYER_A', tt=['PLAYER_A'], exprs=STD, P=dict(
    skin='#f3cda8', hair='#5d5868', eye='#3f8f96', age='teen', jaw='soft', mats=PC_MATS, outfit=pc_outfit,
    **PH([(8, 27), (11, 28), (12, 21), (15, 18), (18, 21.5), (21, 16.5), (25, 20.5), (28, 15.5), (32, 19.5), (35, 15.5), (38, 19), (40, 22)], vol=2.5, top=1,
         back=[[(9, 10), (2, 7), (7, 16)], [(7, 16), (1, 18), (7, 23)], [(16, 5), (13, -1), (22, 3.5)]], front=[[(30, 5), (37, 0), (36, 7)], [(37, 9), (43, 7), (40, 14)]],
         sh=[[(12, 14), (15, 11), (19, 9)], [(23, 9), (27, 8)]], st=[[(21, 12), (21, 16)], [(28, 10), (28, 15)]])))
T('PLAYER_A', skin='#f3cda8', hair='#5d5868', eye='#2f7f86', H=49, sw=5.4, hw=4.2, ra=1.7, rl=2.3, head=(5.5, 6.0), pose='ball', eye_h=3, mats=PC_MATS,
  garment=TG(), detail=pc_T_detail,
  hairdo=TH(SHORT_T, 1.3, 0.6, locks=[[(2, -6.5), (7.5, -8.5), (6, -3)], [(5, -3), (9.5, -1.5), (6, 1)], [(-4, -6.2), (-1.5, -9.5), (1.5, -6.6)]], hi=[(-3, -6), (-2, -6), (-1, -7), (1, -6)]))
O('PLAYER_A', garment='trousers', shirt_v=2, shirt_mat='trim',
  ow_hair=dict(fringe=[1, 0, 1, 1, 0, 1, 0, 1, 0, 1], sides=1, vol=1.5, top=1, spikes=[(-2, -8), (2, -8), (-7, -2), (6, -2), (6, -5)]))

add('PLAYER_B', tt=['PLAYER_B'], exprs=STD, P=dict(
    skin='#f3cda8', hair='#8a4a62', eye='#3f8f96', age='teen', jaw='soft', lashes=True, mats=PC_MATS, outfit=pc_outfit,
    **PH([(8, 31), (11, 32), (12.5, 22), (16, 19.5), (21, 17), (26, 21), (30, 15.5), (35, 17), (38, 20), (40, 24)], vol=2.2, top=0.5,
         back=[[(7, 14), (3, 40), (12, 47), (17, 30)], [(38, 18), (43, 30), (41, 40), (36, 30)]], front=[[(4, 31), (11, 33), (13, 47), (4, 47)], [(37, 21), (40, 21), (40, 31), (38, 30)]],
         sh=[[(12, 14), (16, 10), (21, 8)], [(25, 8), (30, 8)]], st=[[(26, 11), (26, 20)], [(17, 12), (15, 18)], [(8, 36), (10, 44)]],
         after=lambda b: b.c.poly([(5, 30), (11, 31), (11, 34), (5, 33)], 'trim', tone=0.7))))
T('PLAYER_B', skin='#f3cda8', hair='#8a4a62', eye='#2f7f86', H=48, sw=5.0, hw=4.2, ra=1.6, rl=2.2, head=(5.5, 6.0), pose='ball', eye_h=3, mats=PC_MATS,
  legs='shorts', tights=True, boots=3, garment=TG(), detail=pc_T_detail,
  hairdo=TH([(-6.5, -2), (-5, -3.4), (-3, -1.6), (-1, -3.4), (1.5, -3), (3, 0), (3.6, 6), (7, 7)], 1.2, 0.3,
            locks=[[(4, 4), (8, 5), (9.5, 16), (5.5, 17)], [(-6.6, -2), (-5.6, -2), (-5.8, 4), (-6.6, 4)]], hi=[(-3, -6), (-2, -6), (-1, -6), (1, -6), (6, 9), (7, 11)],
            after=lambda f: hlock(f, [(4.5, 5.5), (8, 6), (8, 7.5), (4.5, 7)], 'trim', tone=0.7)))
O('PLAYER_B', garment='shorts', tights=True, shirt_v=2, shirt_mat='trim',
  ow_hair=dict(fringe=[1, 1, 0, 1, 0, 0, 1, 0, 1, 1], sides=4, back=3, vol=1.4, top=0))


# -------------------------------------------------------------------- EDDA
def edda_cap(b):
    c = b.c
    c.poly([(6, 16), (7, 6), (16, 1.5), (32, 1.5), (41, 6), (42, 15)], 'cap', lo=0.3, hi=0.95)
    c.poly([(6, 12.5), (42, 11.5), (42, 15.5), (6, 16.5)], 'capband', lo=0.3, hi=0.8)
    c.poly([(17, 15.5), (43, 14), (47, 18.5), (31, 20), (17, 18)], 'capband', lo=0.15, hi=0.55)
    for x, y in ((29, 6), (30, 5), (31, 6), (30, 7), (30, 8), (29, 8), (31, 8)):
        c.px(x, y, GOLD)


def edda_extras(b, expr):
    wrinkles(b, expr, heavy=False)
    if expr == 'happy':
        b.c.px(25, b.ey + 12, GOLD); b.c.px(24, b.ey + 12, shift(GOLD, dv=0.1))


EDDA_M = dict(top='#2f3e5c', shirt='#d8d2c0', cap='#34446a', capband='#1f2940', hat='#34446a', legs='#3a3f4c', shoes='#2a2630')
add('EDDA', exprs=STD + ['smug'], P=dict(
    skin='#d9a47e', hair='#b9bac4', eye='#4f6a86', age='old', jaw='broad', shoulders='broad', nose='strong', brow_thick=True, brow='#8a8c98', neck_w=6,
    mats=EDDA_M, outfit=PO('high', inner='shirt'), extras=edda_extras,
    **PH([(8, 27), (11, 28), (12, 21), (20, 20), (40, 21)], vol=1.6, after=edda_cap, st=[[(10, 22), (10, 26)]])))
T('EDDA', skin='#d9a47e', hair='#b9bac4', eye='#3f5a76', H=45, sw=7.0, hw=6.0, ww=6.0, ra=2.3, rl=3.0, head=(5.8, 5.8), pose='hips', eye_h=2, brow_t=0, brow='#77788a',
  nose_t=2, mats=EDDA_M, boots=4, garment=TG(hem=0.30, flare=1.5, shirt='shirt', shirt_len=5, belt='capband',
                                             extra=lambda f: [f.c.px(f.J['waist'][0] + 2, f.J['waist'][1] - 4 + i * 3, GOLD) for i in range(3)]),
  collar=T_collar('top', 3.5),
  hairdo=TH([(-6.5, -1), (-3, -1.6), (2, -1.4), (3.4, 0), (3.8, 3), (7, 4)], 0.8,
            after=T_hat([(-6.5, -3.2), (-6, -7.5), (-2, -9.5), (3, -9), (6.5, -6), (6.5, -2.8)], [(-10, -3.8), (-4, -4.6), (2, -4.2), (2, -2.8), (-9, -2.0)], 'hat', (-6, 6, -4, 'capband'), (-3, -7))))
O('EDDA', garment='coat', broad=1, shirt_v=2, ow_hair=dict(fringe=[0] * 10, sides=1, vol=0.8), ow_acc=ow_hat('hat', brim=1, crown=2))


# -------------------------------------------------------------------- VOSS
def voss_silver(b):
    for ln in ([(9, 21), (10, 26)], [(11, 19), (11, 26)], [(12, 21), (12, 25)], [(38, 18), (39, 21)]):
        b.c.stroke(ln, new='silver', only='hair', tone=0.7)


def voss_outfit(b):
    c = b.c
    v_neck(b, 'shirt', lapel='top', lw=4)
    c.poly([(23.5, 41), (27, 41), (27.5, 44), (26, 48), (24.6, 48), (23, 44)], 'tie', lo=0.3, hi=0.9)
    c.poly([(18, 40), (23.5, 38), (25, 42), (21, 44.5)], 'shirt', lo=0.6, hi=0.95); c.poly([(26, 42), (28, 38), (32, 40), (30, 44.5)], 'shirt', lo=0.45, hi=0.8)
    for x, y in ((13, 44), (14, 43), (14, 45), (15, 44), (14, 44)):
        c.px(x, y, GOLD if (x, y) != (14, 44) else (255, 240, 170))


VOSS_M = dict(top='#4b4d5c', shirt='#eef0f4', tie='#b88a2a', silver='#b4b6c4', legs='#44465a', shoes='#2a2832')
add('VOSS', tt=['MERIDIAN_VOSS'], exprs=FULL, P=dict(
    skin='#eac3a0', hair='#3b3742', eye='#7a6238', age='adult', jaw='long', nose='medium', rest_mouth='smile', shoulders='broad', hair_contrast=1.2,
    mats=VOSS_M, outfit=voss_outfit, extras=lambda b, e: wrinkles(b, e),
    **PH([(8, 26), (11, 27), (12, 19), (15, 14.5), (21, 12.5), (28, 13), (34, 14.5), (38, 18), (40, 21)], vol=1.6, top=0.6, after=voss_silver,
         sh=[[(14, 10), (18, 7), (23, 6)]], st=[[(17, 8), (14, 14)], [(26, 6), (30, 12)]])))
T('VOSS', skin='#eac3a0', hair='#3b3742', eye='#5a4628', H=57, sw=6.6, hw=4.6, ra=1.9, rl=2.5, head=(5.2, 6.1), pose='ball', ball=False, eye_h=2, brow_t=1, chin=0.8,
  mouth_t='smile', nose_t=2, mats=VOSS_M, hair_contrast=1.2,
  garment=TG(hem=0.44, flare=0.6, shirt='shirt', shirt_len=8, tie='tie', lapel=True,
             extra=lambda f: (f.c.px(f.J['sh'][0] + 3, f.J['sh'][1] + 4, GOLD), f.c.stroke([jp(f, 'hip', -4, 0), jp(f, 'hip', 4, 0.5)], dt=-0.3, only='top'))),
  hairdo=TH(HIGH_T, 0.9, 0.3, hi=[(-3, -6), (-2, -7), (-1, -7), (0, -7)],
            after=lambda f: hlock(f, [(2.6, -1.5), (4.4, -1), (4.4, 2.5), (3.4, 2.5)], 'silver', tone=0.8)))
O('VOSS', garment='trousers', tall=1, shirt_v=3, ow_hair=dict(fringe=[0] * 10, line=-3, sides=1, vol=0.8),
  ow_acc=ow_px(pts_down=[(-5, -2, (180, 182, 196)), (5, -2, (180, 182, 196)), (-1, 6, (184, 138, 42)), (-1, 7, (184, 138, 42))], pts_left=[(1, -1, (180, 182, 196)), (1, 0, (180, 182, 196))]))


# ------------------------------------------------------------------ TAMSIN
def tam_outfit(b):
    c = b.c
    c.poly([(1, 48), (4, 42), (15, 38.5), (21, 43.5), (24.5, 48)], 'shawl', lo=0.45, hi=0.95)
    c.poly([(25.5, 48), (29, 43.5), (34, 38.5), (43, 42), (47, 48)], 'shawl', lo=0.25, hi=0.75)
    for x, y in ((8, 44), (40, 45)):                                    # moth eyespots
        for dx, dy in ((0, 0), (1, 0), (2, 0), (0, 1), (2, 1), (0, 2), (1, 2), (2, 2)):
            c.px(x + dx, y + dy, (150, 104, 70))
        c.px(x + 1, y + 1, (60, 44, 50))
    tape = (232, 200, 74)
    for i, (x, y) in enumerate([(17, 38), (17, 39), (18, 40), (18, 41), (19, 42), (19, 43), (20, 44), (20, 45), (21, 46), (21, 47), (31, 38), (31, 39), (30, 40), (30, 41), (30, 42), (29, 43), (29, 44), (29, 45), (29, 46), (28, 47)]):
        c.px(x, y, tape if i % 2 else (140, 110, 40)); c.px(x + 1, y, tape)


TAM_M = dict(top='#a58cb8', shawl='#eadfc6', legs='#6a5a7a', shoes='#6a4a3c', tape='#e8c84a')
add('TAMSIN', tt=['LEADER_TAMSIN'], exprs=FULL, P=dict(
    skin='#f4d3b6', hair='#a07e5e', eye='#7a5a9a', age='teen', jaw='soft', shoulders='narrow', eye_tilt=-1, lashes=True, rest_brow=(-1, 1), mats=TAM_M, outfit=tam_outfit,
    **PH([(8, 29), (11, 30), (12, 23), (14.5, 19.5), (18, 22.5), (22, 17.5), (27, 21.5), (31, 17.5), (36, 20.5), (40, 23)], vol=1.9, top=0.4,
         blobs_b=[(8, 6, 6.5, 5.5)], front=[[(9.5, 24), (12.5, 24), (12, 37), (10, 35)], [(37.4, 22), (39.6, 22), (39.4, 33), (38.2, 32)], [(4, 3), (2, -2), (8, 1)]],
         sh=[[(12, 15), (16, 11), (21, 9)], [(5, 4), (8, 2)]], st=[[(22, 11), (22, 16)], [(30, 10), (31, 16)], [(11, 28), (11, 34)]])))
T('TAMSIN', skin='#f4d3b6', hair='#a07e5e', eye='#6a4a8a', H=49, sw=4.8, hw=4.2, ra=1.5, rl=2.1, head=(5.5, 6.0), pose='clasp', eye_h=3, brow_t=3, mats=TAM_M, legs='dress', tights=False,
  garment=chain(TG(hem=0.17, flare=3.4, open_front=False), T_shawl('shawl', 6, spots=(150, 104, 70))),
  detail=lambda f: [f.c.px(f.J['sh'][0] - 2 + (i // 4), f.J['sh'][1] + 1 + i, (232, 200, 74) if i % 2 else (150, 120, 44)) for i in range(9)],
  hairdo=TH([(-6.5, -1.5), (-5, -3), (-3, -1.6), (-1, -3.4), (1.5, -2.6), (3, 0), (3.6, 4), (7, 5)], 1.1, 0.2, blobs=[(4.5, -6.5, 3.2, 3.0)],
            locks=[[(-6.4, -1), (-5.4, -1), (-5.6, 5), (-6.4, 4)], [(2.6, 0), (4, 0), (3.8, 6), (2.8, 6)]], hi=[(-3, -6), (-2, -6), (-1, -6), (4, -8), (5, -8)]))
O('TAMSIN', garment='dress', hem=1, ow_hair=dict(fringe=[1, 1, 0, 1, 0, 1, 0, 1, 1, 1], sides=3, vol=1.2, top=0, spikes=[(-1, -8), (0, -8), (1, -8), (-1, -9), (0, -9)]),
  ow_body=ow_body(fn_any=ow_cape('shawl', 3)))


# ----------------------------------------------------------- ROWAN / MOURNER
ROW_M = dict(top='#58724c', shirt='#d9cdb0', stubble='#c2977a', legs='#6a5642', shoes='#4a3a30', hood='#8a8c98', mask='#b7aa94', lily='#f4f4ee')
ROW_H = PH([(8, 30), (11, 31), (12, 22), (15, 18), (19, 20.5), (23, 15.5), (27, 19.5), (31, 15.5), (35, 18.5), (38, 17), (40, 23)], vol=2.6, top=0.5,
           back=[[(7, 22), (4, 31), (9, 34), (12, 26)]], sh=[[(12, 15), (16, 11), (21, 9)]],
           st=[[(19, 12), (18, 19)], [(27, 11), (27, 18)], [(34, 12), (35, 18)]])
add('ROWAN', tt=['LEADER_ROWAN'], exprs=STD + ['smug', 'crying'], P=dict(
    skin='#d6a57c', hair='#7b6a58', eye='#5f7a48', age='adult', jaw='long', nose='medium', shoulders='broad', rest_mouth='smile', mats=ROW_M,
    outfit=PO('high', inner='shirt', extra=pin(10, 44, (150, 200, 110))), under_face=beard('stubble', full=False, stache=False), extras=lambda b, e: wrinkles(b, e), **ROW_H))
T('ROWAN', skin='#d6a57c', hair='#7b6a58', eye='#4f6a38', H=55, sw=6.4, hw=4.6, ra=1.9, rl=2.5, head=(5.3, 6.1), pose='cane', ball=False, eye_h=2, brow_t=1, chin=0.8, mouth_t='smile',
  nose_t=2, mats=ROW_M, boots=4, garment=TG(hem=0.24, flare=2.6, shirt='shirt', shirt_len=6, belt='legs'), collar=T_collar('top', 3),
  detail=T_cane((120, 90, 60), (150, 200, 110)),
  hairdo=TH([(-6.5, -1.5), (-5, -3), (-3, -1.8), (-1, -3.4), (1.5, -2.6), (3, 0.5), (3.6, 5), (7, 6)], 1.5, 0.3, locks=[[(3, 3), (7.5, 4), (6.5, 8), (3.5, 7)]],
            hi=[(-3, -6), (-2, -7), (-1, -7), (1, -6)], after=lambda f: f.c.pxs([(f.face_xy[0] + dx, f.face_xy[1] + dy) for dx, dy in ((-5, 4), (-4, 5), (-2, 5), (0, 5), (2, 4), (-3, 6), (-1, 6))], (176, 138, 106))))
O('ROWAN', garment='coat', tall=1, shirt_v=2, ow_hair=dict(fringe=[1, 0, 1, 0, 1, 1, 0, 1, 0, 1], sides=3, back=1, vol=1.6))

_hb, _hf = hood_P('hood')


def mourner_mask(b):
    c = b.c
    mk = c.m_poly([(13, 13.5), (24, 11.5), (36, 13.5), (38.4, 22), (37.4, 30), (33, 37.5), (28, 41.5), (24, 41.5), (18, 37.5), (13, 30), (11.8, 22)])
    c.paint(mk, 'mask', c.t_lin(mk, 0.3, 0.95))
    for ln in ([(17, 15), (16, 24)], [(22, 13), (22, 19)], [(30, 14), (31, 21)], [(34, 26), (33, 34)], [(19, 31), (20, 37)], [(26, 33), (26, 40)]):
        c.stroke(ln, dt=-0.25, only='mask')
    c.stroke([(25, 27), (25, 31)], line=True, only='mask'); c.stroke([(22, 36), (29, 36)], line=True, only='mask')


def mourner_lily(b, expr):
    c = b.c
    for cx, cy, rx, ry in ((14, 15, 3.2, 1.8), (17.5, 12, 1.8, 3.0), (12.5, 11, 1.8, 2.8), (10, 14.5, 2.8, 1.7), (14.5, 18.5, 1.7, 2.6)):
        c.ell(cx, cy, rx, ry, 'lily', tone=0.9 if cy < 15 else 0.6)
    c.px(14, 14, (236, 200, 96)); c.px(14, 15, (236, 200, 96)); c.px(13, 14, (236, 200, 96))


def mourner_eyes(b, expr):
    c, ey = b.c, b.ey
    glow = (170, 220, 170)
    shapes = {
        'neutral': ([(15, ey + 2), (21, ey + 1)], [(29, ey + 1), (33, ey + 2)]),
        'angry': ([(15, ey), (21, ey + 3)], [(29, ey + 3), (33, ey)]),
        'sad': ([(15, ey + 3), (21, ey)], [(29, ey), (33, ey + 3)]),
    }
    if expr == 'shocked':
        for cx, w in ((18, 2.6), (31, 2.1)):
            for x in range(13, 36):
                for y in range(ey - 2, ey + 6):
                    if ((x + 0.5 - cx - 0.5) / w) ** 2 + ((y + 0.5 - ey - 2) / 2.8) ** 2 <= 1:
                        c.px(x, y, INK)
            c.px(int(cx), ey + 2, glow)
        return
    for (p0, p1) in shapes.get(expr, shapes['neutral']):
        c.pline([p0, p1], INK); c.pline([(p0[0], p0[1] + 1), (p1[0], p1[1] + 1)], INK)
        c.px((p0[0] + p1[0]) // 2 + 1, (p0[1] + p1[1]) // 2 + 1, glow)


add('MOURNER', tt=['HOLLOW_MOURNER'], exprs=['neutral', 'angry', 'sad', 'shocked'], P=dict(
    skin='#d6a57c', hair='#7b6a58', age='adult', jaw='long', shoulders='broad', masked=True, mask_fn=mourner_eyes, mats=dict(ROW_M, top='#74768a'),
    hair_back=_hb, hair_front=_hf, under_face=mourner_mask, over_face=mourner_lily, outfit=lambda b: b.c.poly([(10, 48), (14, 40), (34, 40), (38, 48)], 'hood', lo=0.25, hi=0.8)))


def mourner_T_mask(f):
    c = f.c
    hlock(f, [(-5.6, -3.4), (0, -4), (2.6, -2), (2.6, 3), (0, 6.2), (-3.4, 6), (-5.6, 2)], 'mask', lo=0.3, hi=0.95)
    x0, y0 = f.face_xy
    c.pxs([(x0 - 4, y0), (x0 - 4, y0 + 1), (x0 - 1, y0), (x0, y0), (x0 - 1, y0 + 1), (x0, y0 + 1)], INK)
    c.pxs([(x0 + 2, y0 - 3), (x0 + 3, y0 - 4), (x0 + 3, y0 - 2), (x0 + 4, y0 - 3)], (244, 244, 238)); c.px(x0 + 3, y0 - 3, GOLD)
    c.stroke([(x0 - 2, y0 + 3), (x0 - 2, y0 + 5)], dt=-0.3, only='mask')


T('MOURNER', skin='#d6a57c', hair='#7b6a58', H=57, sw=6.6, hw=5.0, ra=2.0, rl=2.5, head=(5.3, 6.1), pose='point', ball=False, mats=dict(ROW_M, top='#74768a', shoes='#4a4c5a'), legs='robe',
  cuff=1.0, gloves='top', garment=TG(hem=0.02, flare=3.6, open_front=False, belt='hood', extra=lambda f: f.c.stroke([jp(f, 'hip', 0, 2), jp(f, 'hip', -1, 24)], dt=-0.3, only='top')),
  hairdo=chain(T_hood('hood', 2.2), mourner_T_mask))


def mourner_ow(c, d, hx_, iy, step):
    ow_hood('hood')(c, d, hx_, iy, step)
    if d == 'down':
        m = c.m_ell(hx_, iy + 1.2, 4.3, 4.2)
        c.paint(m, 'mask', c.t_lin(m, 0.4, 0.95), edge=False)
        for ex in (5, 10):
            c.px(ex, iy, INK); c.px(ex, iy + 1, INK)
        c.px(11, iy - 2, (244, 244, 238)); c.px(12, iy - 3, (244, 244, 238))
    elif d == 'left':
        m = c.m_ell(hx_ - 2.4, iy + 1.2, 3.6, 4.0)
        c.paint(m, 'mask', c.t_lin(m, 0.4, 0.95), edge=False)
        c.px(4, iy, INK); c.px(4, iy + 1, INK)


O('MOURNER', garment='robe', tall=1, gloves='top', ow_hair=dict(fringe=[0] * 10, sides=0, vol=0.4), ow_acc=mourner_ow)

# ------------------------------------------------------------------- CALLA
CAL_M = dict(top='#ece6d6', shirt='#4b4d5c', legs='#4b4d5c', skirtm='#4b4d5c', tights='#3a3440', shoes='#2a2832', trim='#b88a2a')
add('CALLA', exprs=STD + ['panic', 'crying'], P=dict(
    skin='#c8906a', hair='#2f2b38', eye='#7a4a32', age='adult', jaw='soft', eye_h=3, lashes=True, shoulders='narrow', hair_contrast=1.25, lip=(168, 84, 80), mats=CAL_M,
    outfit=PO('lapel', inner='shirt', extra=pin(11, 44)),
    **PH([(8, 26), (11, 27), (12, 20), (16, 15.5), (22, 13.5), (26, 17.5), (30, 13.5), (35, 15.5), (38, 19), (40, 22)], vol=1.4, blobs_b=[(6.5, 11, 5.5, 5.5)],
         sh=[[(13, 12), (17, 9), (22, 8)]], st=[[(26, 7), (26, 16)]])))
T('CALLA', skin='#c8906a', hair='#2f2b38', eye='#5a3a22', H=51, sw=4.8, hw=4.2, ra=1.5, rl=2.1, head=(5.2, 5.9), pose='lantern', ball=False, eye_h=2, mats=CAL_M, legs='dress', tights=True,
  hair_contrast=1.25, garment=chain(lambda f: f.skirt(0.34, 0.8, 'skirtm', top_y=f.J['hip'][1] - 1), TG(shirt='shirt', shirt_len=5, lapel=True, belt=None,
                                    extra=lambda f: (f.c.px(f.J['sh'][0] + 3, f.J['sh'][1] + 3, GOLD), f.c.stroke([jp(f, 'hip', -4.5, -1), jp(f, 'hip', 4.5, -0.5)], new='trim', only='top', tone=0.6)))),
  detail=lambda f: f.c.stamp(["kkkk", "kggk", "kggk", "kkkk"], int(f.J['haL'][0]) - 3, int(f.J['haL'][1]) - 4, {'k': (60, 62, 76), 'g': (140, 230, 200)}),
  hairdo=TH(HIGH_T, 0.8, 0.2, blobs=[(5.5, -4.5, 2.8, 2.8)], hi=[(-3, -6), (-2, -7), (-1, -7), (5, -6)]))
O('CALLA', garment='dress', skirt_mat='skirtm', tights=True, tall=1, shirt_v=2,
  ow_hair=dict(fringe=[0] * 10, line=-3, sides=1, vol=0.8, spikes=[(0, -8), (1, -8), (0, -9)]))

# ----------------------------------------------------------------- THISTLE
THI_M = dict(top='#6a6c7a', hood='#80828e', shirt='#3a3440', legs='#4a4a58', shoes='#3a3440', pin='#9a5ab8')
_tb, _tf = hood_P('hood', open_line=[(6, 44), (10, 38), (11, 25), (14, 15), (23, 10.5), (32, 11.5), (38, 18), (40, 28), (41, 40), (44, 44)])
_th = PH([(8, 29), (12, 29), (13, 20), (16.5, 21.5), (20, 16.5), (24, 20.5), (28, 16), (32, 19.5), (36, 17), (40, 22)], vol=1.0, st=[[(20, 13), (20, 18)], [(28, 13), (28, 17)]])


def thistle_pin(b):
    for x, y, col in ((34, 44, (154, 90, 184)), (35, 43, (190, 130, 214)), (36, 44, (154, 90, 184)), (35, 44, (154, 90, 184)), (35, 45, (90, 140, 80)), (35, 46, (90, 140, 80))):
        b.c.px(x, y, col)


add('THISTLE', tt=['HOLLOW_THISTLE'], exprs=STD, P=dict(
    skin='#e2b592', hair='#7a3038', eye='#6b8a3a', age='adult', jaw='sharp', rest_brow=(1, -1), rest_mouth='frown', eye_tilt=1, bags=True, mats=THI_M,
    hair_back=_tb, hair_front=chain(_th['hair_front'], _tf), outfit=PO('high', inner='shirt', extra=thistle_pin)))
T('THISTLE', skin='#e2b592', hair='#7a3038', eye='#5b7a2a', H=52, sw=5.4, hw=4.6, ra=1.8, rl=2.4, head=(5.3, 6.0), pose='ball', eye_h=2, brow_t=2, mouth_t='frown', mats=THI_M, boots=4,
  garment=TG(hem=0.22, flare=3.0, shirt='shirt', shirt_len=5, belt='shirt', extra=lambda f: f.c.px(f.J['sh'][0] + 3, f.J['sh'][1] + 3, (190, 130, 214))),
  hairdo=T_hood('hood', 2.0))
O('THISTLE', garment='coat', tall=1, ow_hair=dict(fringe=[1, 0, 1, 1, 0, 1, 0, 1, 0, 1], sides=0, vol=0.4), ow_acc=ow_hood('hood'))

# ------------------------------------------------------------ WENNA / COLL
WEN_M = dict(top='#b85a4a', apron='#efe6d0', legs='#7a4a3c', shoes='#6a4a3c')


def wenna_outfit(b):
    c = b.c
    c.poly([(17, 42.5), (33, 42.5), (34, 48), (16, 48)], 'apron', lo=0.5, hi=0.95)
    c.poly([(15, 40), (18, 39.5), (20, 43), (17, 43)], 'apron', lo=0.5, hi=0.9); c.poly([(31, 39.5), (34, 40), (33, 43), (30, 43)], 'apron', lo=0.4, hi=0.8)


add('WENNA', exprs=STD, P=dict(
    skin='#f5cfae', hair='#a85a34', eye='#4f7a3a', age='adult', jaw='round', eye_h=3, lashes=True, rest_mouth='smile', mats=WEN_M, outfit=wenna_outfit,
    extras=lambda b, e: (freckles(b), wrinkles(b)),
    **PH([(8, 27), (11, 28), (12, 21), (16, 17), (22, 15), (28, 16), (34, 17.5), (38, 20.5), (40, 23)], vol=2.4, blobs_b=[(23, 3.5, 8, 5)], blobs_f=[(23, 3.5, 7, 4)],
         sh=[[(12, 14), (16, 11), (21, 10)], [(19, 2), (24, 1)]], st=[[(17, 8), (15, 15)], [(27, 8), (30, 14)], [(16, 6), (30, 6)]])))
T('WENNA', skin='#f5cfae', hair='#a85a34', eye='#3f6a2a', H=47, sw=5.8, hw=5.6, ww=5.4, ra=2.0, rl=2.6, head=(5.6, 5.9), pose='hips', eye_h=2, mouth_t='smile', mats=WEN_M, legs='dress',
  sleeve_len=0.55, garment=chain(TG(hem=0.16, flare=3.2, open_front=False),
                                 lambda f: f.c.poly([jp(f, 'sh', -3.5, 3), jp(f, 'sh', 2.5, 3), jp(f, 'hip', 3.5, 0), jp(f, 'hip', 4.5, 13), jp(f, 'hip', -5.5, 13), jp(f, 'hip', -4.5, 0)], 'apron', lo=0.4, hi=0.95)),
  hairdo=TH(SHORT_T, 1.4, 0.2, blobs=[(0.5, -7.5, 3.6, 2.6)], hi=[(-3, -6), (-2, -6), (0, -9), (1, -9)]))
O('WENNA', garment='dress', hem=1, broad=0, sleeve_len=0.5, ow_hair=dict(fringe=[1, 0, 0, 1, 0, 0, 1, 0, 0, 1], sides=2, vol=1.5, spikes=[(-1, -8), (0, -8), (1, -8), (0, -9), (-2, -8), (2, -8)]),
  ow_body=ow_body(fn_down=lambda c, t, x0, x1: c.paint(R(c, x0 + 1, t + 2, x1 - 1, 19), 'apron', 0.8, edge=False)))

COL_M = dict(top='#5a7a8a', bib='#6b5a44', legs='#6b5a44', hat='#dcc07a', shoes='#4a3a30')


def coll_hat(b):
    c = b.c
    c.poly([(8, 13), (10, 4), (18, 0.5), (31, 0.5), (39, 4), (41, 12.5)], 'hat', lo=0.35, hi=0.95)
    c.poly([(-2, 16), (6, 12), (24, 11), (42, 11.5), (50, 15), (50, 18), (30, 16.5), (10, 17.5), (-2, 20)], 'hat', lo=0.2, hi=0.8)
    c.stroke([(9, 11), (24, 9.5), (40, 10.5)], new='bib', only='hat', tone=0.5)
    for x in range(12, 38, 4):
        c.stroke([(x, 2), (x + 1, 8)], dt=-0.25, only='hat')


add('COLL', exprs=STD, P=dict(
    skin='#e0ad84', hair='#6a4a34', eye='#5a4a36', age='adult', jaw='broad', shoulders='broad', nose='strong', neck_w=6, mats=COL_M, under_face=beard('hair', full=True),
    outfit=lambda b: (b.c.poly([(13, 40), (17, 39.5), (20, 48), (15, 48)], 'bib', lo=0.4, hi=0.9), b.c.poly([(32, 39.5), (36, 40), (35, 48), (30, 48)], 'bib', lo=0.3, hi=0.7)),
    **PH([(8, 27), (11, 28), (12, 21), (22, 19), (34, 19), (40, 22)], vol=1.8, after=coll_hat)))
T('COLL', skin='#e0ad84', hair='#6a4a34', eye='#4a3a26', H=55, sw=7.6, hw=5.6, ww=5.6, ra=2.4, rl=2.9, head=(5.5, 6.0), pose='relaxed', ball=False, eye_h=2, brow_t=0, mats=COL_M, sleeve_len=0.55,
  garment=lambda f: (f.c.poly([jp(f, 'sh', -3.5, 3), jp(f, 'sh', 3, 3), jp(f, 'hip', 5.6, 0), jp(f, 'hip', 5.6, 2), jp(f, 'hip', -5.6, 2), jp(f, 'hip', -5.6, 0)], 'bib', lo=0.35, hi=0.9),
                     f.c.stroke([jp(f, 'sh', -3, 0), jp(f, 'sh', -3, 3)], new='bib', only='top', tone=0.6), f.c.stroke([jp(f, 'sh', 2.6, 0), jp(f, 'sh', 2.6, 3)], new='bib', only='top', tone=0.4)),
  hairdo=chain(TH([(-6.5, -1), (-3, -1.6), (2, -1.4), (3.4, 0), (3.8, 3), (7, 4)], 0.9), T_beard('hair', 1),
               T_hat([(-5.5, -4), (-5, -8.5), (-1, -10), (3.5, -9.4), (5.6, -7), (6, -3.6)], [(-11, -3.4), (-4, -4.8), (4, -4.6), (10, -2.6), (10, -1.6), (2, -2.8), (-10, -2.0)], 'hat', (-5, 6, -5, 'bib'))))
O('COLL', garment='trousers', tall=1, broad=1, sleeve_len=0.5, ow_hair=dict(fringe=[0] * 10, sides=1, vol=0.8), ow_acc=chain(ow_beard('hair'), ow_hat('hat', crown=2, wide=True)),
  ow_body=ow_body(fn_down=lambda c, t, x0, x1: c.paint(R(c, x0 + 1, t + 2, x1 - 1, 19), 'bib', 0.6, edge=False)))

# ------------------------------------------------------------------ HESPER
HES_M = dict(top='#35324a', shawl='#4a4560', shirt='#8a86a0', legs='#35324a', shoes='#2a2832')
add('HESPER', exprs=STD, P=dict(
    skin='#ecd0bc', hair='#e6e6ee', eye='#7a7fb0', age='old', jaw='sharp', gaunt=True, nose='strong', rest_brow=(1, -1), rest_mouth='frown', eye_tilt=1, brow='#9a9aac',
    shoulders='narrow', mats=HES_M, outfit=PO('shawl', extra=lambda b: collar_high(b, 'top', lift=1)), extras=lambda b, e: wrinkles(b, e, heavy=True),
    **PH([(8, 26), (11, 27), (12, 19), (16, 14), (22, 12), (28, 12.5), (34, 14.5), (38, 18), (40, 21)], vol=1.0, blobs_b=[(5.5, 13, 4.5, 4.5)],
         sh=[[(13, 11), (17, 8), (22, 7)]], st=[[(15, 9), (13, 17)], [(22, 6), (22, 11)], [(30, 7), (32, 13)]])))
T('HESPER', skin='#ecd0bc', hair='#e6e6ee', eye='#6a6fa0', H=46, sw=4.8, hw=4.4, ra=1.5, rl=2.0, head=(5.2, 5.9), pose='stoop', ball=False, eye_h=1, brow_t=2, brow='#8a8a9c', mouth_t='frown', nose_t=2,
  mats=HES_M, legs='robe', garment=chain(TG(hem=0.04, flare=2.6, open_front=False), T_shawl('shawl', 8)), detail=T_cane((70, 60, 70), (90, 80, 90)),
  hairdo=TH(HIGH_T, 0.7, 0.1, blobs=[(5.6, -2.5, 2.4, 2.4)], hi=[(-3, -6), (-2, -6), (-1, -6)]))
O('HESPER', garment='robe', ow_hair=dict(fringe=[0] * 10, line=-3, sides=0, vol=0.6, spikes=[(0, -8), (1, -8)]), ow_body=ow_body(fn_any=ow_cape('shawl', 4)))

# ------------------------------------------------------------------ SHELLY
SHE_M = dict(top='#f0c93c', shirt='#f4f0e0', legs='#5a6a9a', shoes='#d05a4a', book='#7a4a8a', tie='#d05a4a')


def shelly_outfit(b):
    c = b.c
    c.poly([(4, 46), (8, 37), (18, 35.5), (22, 42), (14, 47)], 'top', lo=0.45, hi=0.95)       # hood lying on the shoulders
    c.poly([(27, 42), (31, 35.5), (40, 37), (44, 45), (34, 47)], 'top', lo=0.25, hi=0.75)
    v_neck(b, 'shirt', depth=47)
    c.px(24, 44, (120, 100, 40)); c.px(26, 44, (120, 100, 40)); c.px(24, 46, (120, 100, 40))


add('SHELLY', tt=['FESTIVAL_SHELLY'], exprs=['neutral', 'happy', 'angry', 'sad', 'panic', 'shocked', 'blush'], P=dict(
    skin='#f6d2b4', hair='#3a4a72', eye='#4a6aa8', age='teen', jaw='round', shoulders='narrow', eye_tilt=-1, lashes=True, sparkle=True, rest_brow=(-1, 0), mats=SHE_M,
    outfit=shelly_outfit,
    **PH([(8, 30), (11, 31), (12, 24), (15, 21), (19, 24), (23, 19), (27, 23.5), (31, 19), (35, 22), (38, 20), (40, 25)], vol=2.2, top=0.4,
         back=[[(8, 24), (1, 30), (0, 41), (6, 45), (11, 36)], [(39, 24), (45, 30), (46, 40), (41, 43), (38, 34)]],
         front=[[(9, 26), (12.5, 26), (12, 34), (9.5, 33)], [(37.4, 24), (39.8, 24), (39.6, 32), (38.2, 31)]],
         sh=[[(12, 16), (16, 12), (21, 10)], [(25, 10), (29, 10)]], st=[[(19, 13), (19, 20)], [(27, 13), (27, 19)], [(35, 13), (35, 18)]],
         after=lambda b: (b.c.poly([(6, 25), (10, 24), (11, 27), (7, 28)], 'tie', tone=0.7), b.c.poly([(39, 24.5), (42, 25), (42, 28), (39, 27.5)], 'tie', tone=0.5)))))
T('SHELLY', skin='#f6d2b4', hair='#3a4a72', eye='#3a5a98', H=44, sw=4.6, hw=4.0, ra=1.6, rl=2.1, head=(5.7, 6.0), pose='clasp', ball=False, eye_h=3, brow_t=3, mats=SHE_M, boots=4, cuff=0.6,
  garment=TG(hem=0.30, flare=2.8, shirt='shirt', shirt_len=4, extra=lambda f: [f.c.px(f.J['waist'][0] + 1, f.J['waist'][1] - 2 + i * 3, (120, 100, 40)) for i in range(3)]),
  collar=T_collar('top', 2.5),
  detail=lambda f: f.c.poly([jp(f, 'haL', -3, -3), jp(f, 'haL', 3.4, -3), jp(f, 'haL', 3.4, 3), jp(f, 'haL', -3, 3)], 'book', lo=0.3, hi=0.9),
  hairdo=TH([(-6.5, -1), (-5, -2.8), (-3.4, -1.4), (-1.6, -3.2), (0.5, -1.6), (2, -3), (3.2, 0.5), (3.8, 4), (7, 5)], 1.3, 0.3,
            locks=[[(4, 2), (8.5, 4), (9, 10), (6, 11), (4, 6)], [(-6.6, 1), (-5.6, 1), (-6.6, 8), (-8.4, 7)]], hi=[(-3, -6), (-2, -6), (-1, -7), (1, -6)],
            after=lambda f: hlock(f, [(4.2, 2.6), (6.4, 3), (6.2, 4.6), (4.2, 4.2)], 'tie', tone=0.7)))
O('SHELLY', garment='coat', shirt_v=2, ow_hair=dict(fringe=[1, 1, 0, 1, 0, 1, 0, 1, 1, 1], sides=4, back=0, vol=1.4, spikes=[(-7, 3), (-7, 4), (-7, 5), (6, 3), (6, 4), (6, 5), (-6, 6), (5, 6)]))


# ------------------------------------------------------------------ DORIAN
def dorian_outfit(b):
    c = b.c
    v_neck(b, 'shirt', lapel='top', lw=4)
    c.poly([(19, 39), (31, 39), (30, 44), (26.5, 47), (23.5, 47), (20, 44)], 'shirt', lo=0.5, hi=0.95)        # cravat
    c.stroke([(22, 41), (25, 44)], dt=-0.3, only='shirt'); c.stroke([(29, 41), (26, 44)], dt=-0.3, only='shirt')
    c.px(25, 42, (120, 220, 200)); c.px(25, 43, (60, 150, 140))
    c.stroke([(12, 42), (17, 47)], new='trim', only='top', tone=0.7); c.stroke([(38, 42), (34, 47)], new='trim', only='top', tone=0.5)


def dorian_extras(b, expr):
    wrinkles(b, expr)
    c = b.c
    my = b.ey + 12
    col = shift(b.s['hair'], dv=-0.05)
    c.pxs([(22, my - 2), (23, my - 3), (24, my - 3), (25, my - 3), (26, my - 3), (27, my - 3), (28, my - 3), (29, my - 3), (30, my - 2), (21, my - 2), (31, my - 2), (20, my - 3), (32, my - 3)], col)


DOR_M = dict(top='#7a2f5c', shirt='#f2ead8', trim='#d8b04a', silver='#c4c4d2', legs='#3a3446', shoes='#2a2630')
add('DORIAN', tt=['LEADER_DORIAN'], exprs=FULL, P=dict(
    skin='#f0c8a6', hair='#4a3a48', eye='#3f8a96', age='adult', jaw='long', nose='medium', rest_mouth='smile', rest_brow=(0, -1), eye_h=3, mats=DOR_M, outfit=dorian_outfit, extras=dorian_extras,
    **PH([(8, 26), (11, 27), (12, 19), (15, 15), (20, 12.5), (26, 14.5), (31, 11.5), (36, 14), (39, 18), (40, 21)], vol=3.0, top=2.0,
         front=[[(28, 3), (40, 1), (43, 8), (38, 13), (34, 8)]], sh=[[(12, 11), (17, 6), (24, 4)], [(30, 4), (36, 4)]], st=[[(18, 5), (14, 13)], [(24, 3), (22, 11)], [(31, 5), (33, 10)]],
         after=lambda b: lock(b, [(26, 2), (30, 1.5), (34, 10), (31, 11)], mat='silver'))))
T('DORIAN', skin='#f0c8a6', hair='#4a3a48', eye='#2f7a86', H=55, sw=6.2, hw=4.6, ra=1.9, rl=2.4, head=(5.3, 6.1), pose='cane', ball=False, eye_h=2, brow_t=0, mouth_t='line', chin=0.6, mats=DOR_M,
  cuff=0.6, garment=TG(hem=0.26, flare=3.4, shirt='shirt', shirt_len=5, lapel=True, extra=lambda f: (f.c.stroke([jp(f, 'hip', -7, 12), jp(f, 'hip', 7.5, 12.6)], new='trim', only='top', tone=0.6),
                                                                                                       f.c.px(f.J['sh'][0] - 1, f.J['sh'][1] + 2, (120, 220, 200)))),
  detail=T_cane((70, 50, 60), (226, 228, 240)),
  hairdo=TH(HIGH_T, 1.6, 1.4, locks=[[(-6, -5), (-8.5, -8), (-2, -8.5), (-3, -5)]], hi=[(-4, -8), (-3, -8), (-2, -8), (-1, -8), (1, -7)],
            after=lambda f: (hlock(f, [(-3, -9), (-1.4, -9), (-0.4, -5), (-1.6, -5)], 'silver', tone=0.8),
                             f.c.pxs([(f.face_xy[0] - 3, f.face_xy[1] + 3), (f.face_xy[0] - 2, f.face_xy[1] + 3)], (74, 58, 72)))))
O('DORIAN', garment='coat', tall=1, shirt_v=3, ow_hair=dict(fringe=[0] * 10, line=-3, sides=1, vol=1.4, top=2),
  ow_acc=ow_px(pts_down=[(-1, 3, (74, 58, 72)), (0, 3, (74, 58, 72)), (-1, -8, (196, 196, 210)), (0, -8, (196, 196, 210))]))
