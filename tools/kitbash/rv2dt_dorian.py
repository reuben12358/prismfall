"""Dorian Pell, Gym 1 Warden (Normal) - redo v2 (art/REDO_V2_BRIEF.md).
Concept: "the curtain call that never ended". 56, ex-matinee idol: flamboyant, vain, generous.
Design = the style-test portrait (sheet 27), cleaned: swept-back silver mane in five clumps + matinee lock,
arched dark brows, hooded amber eyes, pencil moustache, plum velvet coat with silver satin lapels, ivory cravat,
one red rose (the accent). Original construction, no donor pixels.
python3 -I tools/kitbash/rv2dt_dorian.py  -> art/work/redo_v2/DORIAN/"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rv2dt_px import Art, hx, up, lint

OUT = '/home/claude/fangame/art/work/redo_v2/DORIAN/'

# ---------------------------------------------------------------- colour plan (3 + 1)
K = '1a1220'
SKIN = ('fde0c8', 'f3c4a2', 'd9957a', 'a95f4d')
HAIR = ('fbfaff', 'cdc8e6', 'a29bc6', '6e6698', '4a4274')       # hi, light, mid, shadow, crease
PLUM = ('a0549a', '773372', '522360', '351640')                  # 1 plum velvet (main)
SILK = ('fbfaff', 'cdc8e6', 'a29bc6', '6e6698')                  # 2 silver satin (lapels, lining) = hair ramp
IVORY = ('ffffff', 'f8efe2', 'e2cdc6', 'b897a0')                 # 3 ivory silk (cravat, shirt, gloves)
ROSE = ('ff8a96', 'e33a4c', 'a51d36', '6a1028')                  # accent
LEAF = '2f7a48'
EYE_W, IRIS, IRIS_D, HL = 'f8f4f0', 'dc9a36', '8a4c1c', 'ffffff'
BROW, BROW2 = HAIR[4], HAIR[3]
STACHE, STACHE2 = HAIR[4], HAIR[3]
LIP_D, MOUTH_IN, TONGUE, TEETH = '8e3a40', '4a1424', 'c4545e', 'fbf6f2'


# ================================================================= PORTRAIT (48-px art, 96x96 file)
PDY = 2          # the head sits 2 rows lower than in the style test: crown closes at row 2, chin at row 44


def portrait_img(expr='neutral'):
    return portrait(expr).image().crop((0, -PDY, 48, 48 - PDY))


def portrait(expr='neutral'):
    a = Art(48, 48, K)
    a.ramp('skin', *SKIN); a.ramp('hair', HAIR[0], HAIR[1], HAIR[2], HAIR[4]); a.ramp('plum', *PLUM)
    a.ramp('silk', *SILK); a.ramp('ivory', *IVORY)

    # back to front
    a.poly('skin.neck', [(18, 34), (31, 36), (32, 46), (17, 46)])
    a.poly('hair.0', [(42, 6), (40, 3), (36, 1), (30, 0), (22, 0), (14, 1), (8, 4), (4, 8), (1, 13), (6, 14),
                      (2, 21), (7, 21), (3, 28), (8, 27), (11, 29), (13, 26), (13, 21), (15, 17),
                      (20, 13), (27, 12), (35, 14), (37, 18), (38, 15), (38, 9), (39, 6)])
    a.poly('hair.4', [(17, 13), (12, 15), (9, 18), (7, 21), (5, 25), (3, 28), (8, 27), (11, 24), (13, 21), (15, 17)])
    a.poly('hair.3', [(23, 6), (15, 7), (9, 10), (6, 14), (4, 18), (2, 21), (7, 21), (10, 17), (15, 14),
                      (21, 12), (24, 11)])
    a.poly('hair.2', [(30, 0), (22, 0), (14, 1), (8, 4), (4, 8), (1, 13), (5, 13), (9, 10), (15, 7), (23, 6), (30, 5)])
    a.poly('hair.1', [(21, 12), (22, 7), (25, 3), (30, 1), (36, 1), (40, 3), (42, 6), (39, 6), (38, 9),
                      (38, 15), (37, 18), (35, 14), (31, 12), (27, 12)])
    a.poly('skin.ear', [(14, 22), (11, 21), (10, 23), (10, 27), (11, 29), (13, 30), (14, 29)])
    # J3 square jaw: the turn at the mouth row, a 6-px flat chin
    a.poly('skin.face', [(15, 17), (19, 14), (26, 13), (32, 13), (36, 15), (37, 18), (38, 22), (38, 27), (37, 31),
                         (36, 34), (34, 37), (31, 40), (28, 42), (22, 42), (19, 39), (17, 35), (15, 31),
                         (14, 26), (14, 21)])
    a.poly('hair.lock', [(23, 12), (27, 11), (28, 14), (26, 17), (25, 14)])            # the matinee lock
    a.poly('plum.l', [(0, 47), (0, 43), (7, 40), (15, 38), (20, 41), (24, 47)])
    a.poly('plum.r', [(47, 47), (47, 43), (41, 40), (34, 38), (30, 41), (27, 47)])
    a.poly('silk.l', [(14, 38), (17, 38), (23, 47), (19, 47)])
    a.poly('silk.r', [(35, 38), (32, 38), (27, 47), (31, 47)])
    a.poly('ivory.crav', [(19, 39), (31, 39), (28, 47), (22, 47)])

    a.base()
    # ---- light from the upper left: even bands, no neighbour speckle
    # hair: each clump takes a 2-px mid band on its lower/right edge
    for m in ('hair.0', 'hair.4', 'hair.3', 'hair.2', 'hair.1', 'hair.lock'):
        a.band('hair', 2, 'b', 2, mats=[m]); a.band('hair', 2, 'r', 1, mats=[m])
    # skin: far side of the face in one clean 2-px band below the brow, a 1-px band above it
    a.band('skin', 2, 'r', 2, mats=['skin.face'], only=[(30, 24), (47, 24), (47, 41), (30, 41)])
    a.band('skin', 2, 'r', 1, mats=['skin.face'], only=[(30, 15), (47, 15), (47, 23), (30, 23)])
    a.tone('skin', 2, [(x, y) for y in range(34, 47) for x in range(17, 33)], mats=['skin.neck'])            # neck in the jaw's shadow
    a.tone('skin', 1, [(x, y) for y in range(41, 47) for x in range(17, 21)], mats=['skin.neck'])            # lit edge of the neck
    for m in ('plum.l', 'plum.r', 'silk.l', 'silk.r', 'ivory.crav'):
        g = m.split('.')[0]; a.band(g, 2, 'r', 1, mats=[m])
    # ---- lines
    a.lines(fold_groups=('hair', 'plum', 'silk'))
    # the ear meets the cheek in skin shadow (a deep line here reads as a sideburn stripe)
    a.tone('skin', 3, [(x, y) for y in range(30, 47) for x in range(14, 36) if a.at(x, y) == 'skin.neck' and a.at(x, y - 1) == 'skin.face'])
    # hairline shadow: a 1-px skin-shadow band directly under the hair, across the forehead
    under = [(x, y) for y in range(13, 22) for x in range(15, 38)
             if a.is_g(x, y, 'skin') and a.at(x, y) == 'skin.face' and a.is_g(x, y - 1, 'hair') and a.col[y][x] == a.ramps['skin'][1]]
    a.tone('skin', 2, under)
    a.drop_orphans()

    hair_pass(a)
    costume_pass(a)
    face_pass(a, expr)
    return a


def hair_pass(a):
    W, L, M, S, C = (hx(c) for c in HAIR)
    a.paint([(28, 10), (29, 9), (30, 8), (31, 7), (32, 6), (33, 5)], C)                    # the crest splits in two
    arcs = [(22, 3), (21, 3), (20, 3), (19, 3), (18, 3), (17, 4), (16, 4), (15, 4), (12, 5), (11, 6), (10, 6),
            (7, 8), (6, 9),                                                                  # crown sweep
            (20, 9), (19, 9), (18, 9), (17, 10), (16, 10), (15, 10), (12, 12), (11, 13), (10, 13), (7, 16), (6, 17),
            (13, 17), (12, 18), (11, 19), (9, 22), (8, 23),                                  # over the ear
            (32, 3), (33, 3), (34, 3), (35, 3), (36, 4), (37, 4), (38, 5),                   # crest, front lock
            (27, 4), (26, 5), (25, 6), (24, 7), (24, 8)]                                     # crest, back lock
    a.paint([p for p in arcs if a.is_g(*p, 'hair') and a.col[p[1]][p[0]] != hx(K)], W)
    # occlusion: the mid tone just above a crease darkens one step
    occ = [(x, y) for y in range(47) for x in range(48) if a.is_g(x, y, 'hair') and a.col[y][x] == M
           and a.col[y + 1][x] in (C, hx(K)) and a.is_g(x, y + 1, 'hair')]
    a.paint(occ, S)


def costume_pass(a):
    I = {'K': hx(K), 'I': hx(IVORY[0]), 'i': hx(IVORY[1]), 'j': hx(IVORY[2]), 'J': hx(IVORY[3]),
         'X': hx(ROSE[1]), 'Y': hx(ROSE[0]), 'x': hx(ROSE[2]), 'z': hx(ROSE[3]), 'g': hx(LEAF)}
    # cravat: knot under the jaw, then a puffed fold with two creases (shadows hue-shift to rose-lilac)
    a.stamp(20, 39, ['.jiiiiiij..',
                     '..jIIIj....',
                     '..KIiijK...',
                     '..iIiijj...',
                     '.iIIiiijj..',
                     '.iIIiijjj..',
                     'iIIiiijiij.',
                     'iIIiijjiij.',
                     'iIiiijiiij.'], I)
    P = [hx(c) for c in PLUM]
    a.paint([(5, 45), (6, 44), (7, 43)], P[3]); a.paint([(41, 44), (42, 45), (43, 46)], P[3])      # shoulder folds
    a.paint([(3, 44), (4, 43), (5, 42), (8, 41), (9, 41)], P[0])                                   # velvet sheen
    a.stamp(8, 40, ['  KKK  ',
                    ' KYXxK ',
                    'KYXzXxK',
                    'KXxXxzK',
                    ' KxxzKg',
                    '  KKKgK'], I)


# eye stamps (E3 hooded, adult): K lash, E white, A iris, a iris dark (top, under the lid), W highlight, s lid crease
EYES = {
    'neutral':   ([' ssssss ', 'KKKKKKKK', 'KEEEaWEs', ' EEEAAE ', '  EEAas ', '  sssss '],
                  [' ssss  ', 'KKKKKKK', ' EEaWK ', ' EEAAK ', '  EAa  ', '  sss  ']),
    'happy':     ([' ssssss ', 'KKKKKKKK', 'KEEEaWEs', ' sEEAAs ', '  ssss  '],
                  [' ssss  ', 'KKKKKKK', ' EEaWK ', ' sEAAs ', '  sss  ']),
    'sad':       (['  sssss ', ' KKKKKKK', 'KKEEaWEs', ' EEEAAE ', '  EEAas ', '  sssss '],
                  ['  sss  ', 'KKKKKK ', ' EEaWKK', ' EEAAK ', '  EAa  ', '  sss  ']),
    'angry':     (['        ', 'KKKKKKKK', 'KEEEaWEK', ' EEEAAs ', '  ssss  '],
                  ['       ', 'KKKKKKK', ' EEaWK ', ' sEAAs ', '  sss  ']),
    'surprised': (['KKKKKKKK', 'KEEaaWEK', 'KEEAAAEK', ' EEAAAE ', '  EEEE  ', '  ssss  '],
                  ['KKKKKKK', ' EaaWEK', ' EAAAEK', ' EAAAE ', '  EEE  ', '  sss  ']),
    'laugh':     ([' ssssss ', '  KKKK  ', ' K    K ', 'K      K', ' ssssss '],
                  [' ssss  ', '  KKK  ', ' K   K ', 'K     K', ' sssss ']),
}


def face_pass(a, expr):
    L = {'K': hx(K), 'B': hx(BROW), 'b': hx(BROW2), 'E': hx(EYE_W), 'A': hx(IRIS), 'a': hx(IRIS_D), 'W': hx(HL),
         's': hx(SKIN[2]), 'd': hx(SKIN[3]), 'h': hx(SKIN[0]), 'k': hx(SKIN[1]), 'm': hx(STACHE), 'n': hx(STACHE2),
         'R': hx(LIP_D), 'o': hx(MOUTH_IN), 't': hx(TONGUE), 'T': hx(TEETH)}
    # ---- brows: near one heavy and level, far one arched (B2 + B3); expressions move them as whole stamps
    near = {'neutral': (16, 18, ['   bBBBB', 'bBBBBBB ']),
            'happy': (16, 17, ['   bBBBB', 'bBBBBBB ']),
            'laugh': (16, 17, ['   bBBBB', 'bBBBBBB ']),
            'surprised': (16, 16, ['  bBBBB ', 'bBBBBBB ']),
            'sad': (16, 18, ['     BBB', '  bBBBb ', 'bbb     ']),
            'angry': (16, 18, ['bBB     ', ' bBBBBB ', '    BBBB'])}[expr]
    far = {'neutral': (29, 16, ['   BBB  ', ' BBBBBBb', 'B      B']),
           'happy': (29, 15, ['   BBB  ', ' BBBBBBb', 'B      B']),
           'laugh': (29, 15, ['   BBB  ', ' BBBBBBb', 'B      B']),
           'surprised': (29, 14, ['   BBB  ', ' BBBBBBb', 'B      B']),
           'sad': (29, 17, ['BBB     ', ' bBBBBb ', '     bbb']),
           'angry': (29, 17, ['     BBb', ' BBBBBb ', 'BBB     '])}[expr]
    for x0, y0, rows in (near, far):
        a.stamp(x0, y0, rows, L)
    e_near, e_far = EYES[expr]
    ey = {'surprised': 20, 'angry': 20}.get(expr, 20)
    a.stamp(16, ey, e_near, L); a.stamp(30, ey, e_far, L)
    # ---- nose: bridge shadow on the far side, a dark 3-px underside with a nostril
    a.stamp(28, 25, ['s  ', 's  ', '.s ', '.s ', '.sd', 'sdd'], L)
    a.paint([(27, 26), (27, 27)], SKIN[0])                                                     # bridge catches light
    # ---- moustache (pencil, dyed: vanity) - rides up 1 row when the mouth opens
    sy = 31 if expr in ('laugh', 'surprised', 'angry') else 32
    a.stamp(23, sy, ['m    nn.n m', '.mmmmm.mmm '], L)
    # ---- mouths (STYLE_GUIDE 3.6): closed = line + corners, open = outlined hole + interior + teeth/tongue
    M = {
        'neutral':   (22, 34, ['s          R ', 's.R       R  ', '...RRRRRRR   ', '.....sss     ']),
        'happy':     (22, 34, ['s.R        R ', 's..R      R  ', '....RRRRRR   ', '.....ssss    ']),
        'sad':       (22, 35, ['s...RRRRRR   ', 's..R      R  ', '.......sss   ']),
        'angry':     (23, 33, ['s.KKKKKKK ', 's.KTTTTTK ', '..KoooooK ', '..KTTTTTK ', '...KKKKK  ', '....sss   ']),
        'surprised': (25, 33, ['.KKKK.', 'KooooK', 'KoootK', 'KottoK', '.KKKK.', '.ssss.']),
        'laugh':     (22, 33, ['s.KKKKKKKKKK', 's.KTTTTTTTTK', '...KooooooK ', '....KottoK  ', '.....KKKK   ', '.....sss    ']),
    }[expr]
    a.stamp(*M, L)
    # ---- planes: forehead light, a 2-px cheekbone shadow on the near side (not a speckle line), chin cleft 2 px
    a.paint([(17, 16), (18, 16), (19, 16), (18, 17)], SKIN[0])
    a.paint([(17, 28), (18, 28)], SKIN[0])                                              # the near cheek catches light
    a.stamp(11, 23, ['.ss', '.s.', '.s.', '.ss'], L)                                            # inner ear: one C-curve
    if expr == 'sad':
        a.paint([(21, 27), (22, 27), (23, 27)], SKIN[2])                                      # under-eye line
    if expr == 'angry':
        a.paint([(26, 21), (27, 22)], SKIN[2])                                                # glabella crease


PORTRAIT_EXPRS = ('neutral', 'happy', 'sad', 'angry', 'surprised', 'laugh')


def export_all():
    """writes the work files in the Graphics layout (nothing is installed):
    Trainers/LEADER_DORIAN.png (160x160) + _native80, Characters/DORIAN.png (128x192) + _native,
    Portraits/DORIAN_<expr>.png (96x96) + Portraits/native/*_48.png. Returns lint results."""
    res = {}
    for d in ('Trainers', 'Characters', 'Portraits', 'Portraits/native'):
        os.makedirs(OUT + d, exist_ok=True)
    for e in PORTRAIT_EXPRS:
        im = portrait_img(e)
        im.save(OUT + 'Portraits/native/DORIAN_%s_48.png' % e); up(im, 2).save(OUT + 'Portraits/DORIAN_%s.png' % e)
        res['portrait ' + e] = lint(im)
    fr = front_img()
    fr.save(OUT + 'Trainers/LEADER_DORIAN_native80.png'); up(fr, 2).save(OUT + 'Trainers/LEADER_DORIAN.png')
    res['front'] = lint(fr, keep=FRONT_KEEP)
    ow = ow_sheet()
    ow.save(OUT + 'Characters/DORIAN_native.png'); up(ow, 2).save(OUT + 'Characters/DORIAN.png')
    res['overworld'] = lint(ow)
    return res


# ================================================================= BATTLE FRONT (80x80 art, 160x160 file)
TROU = ('5a3a6a', '3e2448', '2c1836', '1e0e26')        # trousers: the plum family, two steps darker than the coat
HAT = TROU                                               # top hat + shoes: the trousers' plum-black
CANE = ('6e6698', '3e2448', '1e0e26')


def front_shapes(a):
    from rv2dt_px import limb
    # ---- legs (weight on the screen-left leg; the other steps out), then shoes
    a.poly('trou.hip', [(34, 37), (47, 37), (48, 45), (33, 45)])
    a.poly('trou.thighL', limb((37, 42), (36, 58), 9, 7))
    a.poly('trou.shinL', limb((36, 57), (35, 72), 7, 6))
    a.poly('trou.thighR', limb((44, 42), (48, 57), 9, 7))
    a.poly('trou.shinR', limb((48, 56), (51, 72), 7, 6))
    a.poly('hat.shoeL', [(29, 77), (29, 75), (32, 72), (38, 71), (39, 77)])
    a.poly('hat.shoeR', [(48, 71), (53, 71), (57, 74), (58, 77), (48, 77)])
    # ---- the near tail's silver lining (behind the near panel), then the two skirt panels over the thighs
    a.poly('silk.lining', [(47, 44), (53, 48), (59, 52), (63, 57), (56, 58), (49, 57), (47, 50)])
    a.poly('plum.skirtL', [(34, 37), (39, 37), (39, 44), (38, 56), (34, 58), (29, 57), (31, 46)])
    a.poly('plum.skirtR', [(43, 37), (48, 37), (54, 43), (60, 49), (63, 55), (57, 53), (50, 52), (47, 54), (44, 46)])
    # ---- torso: padded shoulders, open front (dark velvet waistcoat), slim silver lapels, then the cravat on top
    a.poly('plum.body', [(31, 23), (36, 20), (46, 20), (50, 22), (52, 26), (51, 31), (48, 35), (47, 39), (34, 39),
                         (33, 35), (31, 30)])
    a.poly('trou.vest', [(37, 21), (45, 21), (44, 32), (42, 38), (39, 38), (37, 32)])
    a.poly('silk.lapL', [(36, 20), (38, 20), (41, 34), (40, 35), (35, 25)])
    a.poly('silk.lapR', [(44, 20), (46, 20), (47, 25), (42, 35), (41, 34)])
    a.poly('ivory.crav', [(38, 19), (44, 19), (44, 22), (43, 27), (41, 29), (39, 27), (38, 22)])
    # ---- neck (the head itself is a designed pixel block, FRONT_HEAD, stamped after shading)
    a.poly('skin.neck', [(39, 17), (43, 17), (43, 20), (39, 20)])
    a.poly('skin.headarea', [(36, 6), (44, 6), (44, 18), (36, 18)])
    # ---- the raised (far) arm: upper arm out level, forearm up (a toast to the house); hat + glove are stamps
    a.poly('plum.upperL', limb((34, 24), (25, 21), 7, 6))
    a.poly('plum.foreL', limb((24, 22), (22, 14), 6, 6))
    # ---- the near arm holds the cane out at its side; knob + glove are stamps
    a.poly('plum.upperR', limb((48, 24), (55, 31), 7, 6))
    a.poly('plum.foreR', limb((55, 30), (57, 36), 6, 6))
    a.line('cane.shaft', [(60, 42), (66, 76)], 2)


HAT_STAMP = (15, 0, ['...KKKKKKKKK..',
                     '...KUuuuuuvK..',
                     '...KUuuuuuvK..',
                     '...KUuuuuuvK..',
                     '...KHHHHHHMK..',
                     'KKKKUuuuuuvKKK',
                     'KUuuuuuuuuuuvK',
                     '.KKKKKKKKKKKK.'])
GLOVE_L = (19, 8, ['.KKKKK.',
                   'KIiiijK',
                   'KIiijjK',
                   '.KijjK.',
                   'KIIiijK',
                   'KiiijjK',
                   '.KKKKK.'])
GLOVE_R = (55, 33, ['....KKK.',
                    '...KWHMK',
                    '...KHMSK',
                    '.KKKKMK.',
                    'KIiiijjK',
                    'KIiijjJK',
                    '.KijjJK.',
                    '..KKKSV.'])
CUFF_R = (54, 34, ['KK.', 'IiK', 'ijK'])
ROSE_F = (34, 24, ['.KKK.',
                   'KXxyK',
                   'KxyYK',
                   '.KKLK'])
SHOE_HI = [(31, 73), (32, 73), (33, 72), (50, 72), (51, 72), (52, 72)]


def front():
    a = Art(80, 80, K)
    a.ramp('skin', *SKIN); a.ramp('hair', HAIR[0], HAIR[1], HAIR[2], HAIR[4]); a.ramp('plum', *PLUM)
    a.ramp('silk', *SILK); a.ramp('ivory', *IVORY); a.ramp('trou', *TROU); a.ramp('hat', *HAT)
    a.ramp('cane', CANE[0], CANE[1], CANE[2], CANE[2])
    front_shapes(a)
    a.base()
    # light from the upper left: 2-px shadow on the right of every form, 1-px lit edge on the left of the big ones
    for g in ('plum', 'trou', 'hat'):
        a.band(g, 2, 'r', 2)
    for g in ('silk', 'ivory', 'skin'):
        a.band(g, 2, 'r', 1)
    a.band('plum', 0, 'l', 1, mats=['plum.upperL', 'plum.foreL', 'plum.body', 'plum.skirtL'])
    a.band('plum', 0, 't', 1, mats=['plum.body', 'plum.upperR'])
    a.band('trou', 0, 'l', 1, mats=['trou.thighL', 'trou.shinL'])
    a.band('hat', 0, 't', 1, mats=['hat.shoeL', 'hat.shoeR', 'hat.brim'])
    a.band('hat', 0, 'l', 1, mats=['hat.crown'])
    # designed folds: elbow creases, the waist seam, a fold down each skirt panel, knee creases
    a.tone_line('plum', 3, [(26, 20), (27, 23)]); a.tone_line('plum', 3, [(53, 29), (55, 32)])
    a.tone_line('plum', 3, [(34, 37), (39, 37)]); a.tone_line('plum', 3, [(43, 37), (48, 37)])
    a.tone_line('plum', 2, [(35, 42), (34, 55)]); a.tone_line('plum', 2, [(50, 44), (55, 50)])
    a.tone_line('trou', 3, [(37, 58), (38, 60)]); a.tone_line('trou', 3, [(47, 57), (48, 59)])
    a.lines(fold_groups=('plum', 'trou', 'hair', 'silk', 'ivory', 'hat'))
    a.paint([(41, 31), (41, 34)], HAIR[1])                                    # silver waistcoat buttons
    cane_pass(a)
    a.drop_orphans()
    front_face(a)
    return a


# the head at front scale: 3/4 toward screen left, swept silver mane (crest forward, four clumps swept back to
# tapering tips), arched brows, hooded amber eyes looking at the challenger, pencil moustache, an open grin.
# K outline, W/H/M/S/C hair hi/light/mid/shadow/crease, f/s/d/h skin, a/A iris, w catchlight, E white, R/T mouth
FRONT_HEAD = (33, 2, [
    '...KKKKKKK............',
    '.KKHHWWWHHKKKK........',
    'KHHWHHHHHHHHHHKKK.....',
    'KHWHHHMMMHHHWWHHHKK...',
    'KHHHMCCKKMMHHHHWHHHKK.',
    '.KKKfhfKCCMMHHHHHHMMMK',
    '..KfffffKCMMHHHHMMKKK.',
    '..KffffffKCMHHWWHHHKK.',
    '..KCCffCCKKCMHHHHMMMMK',
    '..KKKfffKKKCMMHHMMKKK.',
    '...KawfawEfKCMHHHMSK..',
    '...KAAfAAsdKCMMHHMMSK.',
    '...KfffsffsKKCMMMSSSK.',
    '...KfffdsfsK.KCMSSKK..',
    '....KCCfCCsK..KKSK....',
    '....KfRTTRsK...KK.....',
    '.....KfRRsK...........',
    '......KffK............',
    '.......KK.............',])


def front_face(a):
    L = {'K': hx(K), 'W': hx(HAIR[0]), 'H': hx(HAIR[1]), 'M': hx(HAIR[2]), 'S': hx(HAIR[3]), 'C': hx(HAIR[4]),
         'f': hx(SKIN[1]), 's': hx(SKIN[2]), 'h': hx(SKIN[0]), 'd': hx(SKIN[3]), 'E': hx(EYE_W), 'A': hx(IRIS),
         'a': hx(IRIS_D), 'w': hx(HL), 'o': hx(MOUTH_IN), 'T': hx(TEETH), 'R': hx(LIP_D)}
    x0, y0, rows = FRONT_HEAD
    # clear what the block covers (head area only), then stamp it
    for j, r in enumerate(rows):
        for i, ch in enumerate(r):
            x, y = x0 + i, y0 + j
            if a.at(x, y) in ('skin.headarea',) or (ch == '.' and a.at(x, y) == 'skin.headarea'):
                a.erase([(x, y)])
    a.stamp(x0, y0, rows, L, mat='head')
    G = dict(L); G.update({'U': hx(TROU[0]), 'u': hx(TROU[1]), 'v': hx(TROU[2]), 'V': hx(TROU[3]), 'I': hx(IVORY[0]),
                           'i': hx(IVORY[1]), 'j': hx(IVORY[2]), 'J': hx(IVORY[3]), 'X': hx(ROSE[0]), 'x': hx(ROSE[1]),
                           'y': hx(ROSE[2]), 'Y': hx(ROSE[3]), 'L': hx(LEAF), 'S': hx(CANE[0])})
    for st in (HAT_STAMP, GLOVE_L, CUFF_R, GLOVE_R, ROSE_F):
        a.stamp(st[0], st[1], st[2], G, mat='prop')
    a.paint(SHOE_HI, TROU[0])
    # the neck under the jaw: in shadow, lit edge on the left
    a.paint([(x, y) for y in range(19, 22) for x in range(39, 44) if a.at(x, y) == 'skin.neck' and a.col[y][x] != hx(K)], SKIN[2])


def cane_pass(a):
    """the cane is 2 px: a lit left pixel and a dark right one, no outline (BW props)"""
    C = [hx(c) for c in CANE]
    for y in range(80):
        xs = [x for x in range(80) if a.at(x, y) == 'cane.shaft']
        if not xs: continue
        a.paint([(xs[0], y)], C[0]); a.paint([(x, y) for x in xs[1:]], C[2])
    tip = [(x, y) for y in range(74, 80) for x in range(80) if a.at(x, y) == 'cane.shaft']
    a.paint(tip, SILK[1])


FRONT_KEEP = ()


def front_img():
    return front().image()


# ================================================================= OVERWORLD (16x24 art per frame, sheet 128x192)
# designed at true size; rows: down, left, right (= left mirrored, rose shown), up; frames: stand, step, stand, step.
# Step frames drop the body 1 row (as Juno's sheet does) and plant one foot.
OW_DOWN = [
    '................',
    '.......KKKK.....',
    '.....KKHWWHK....',
    '....KHWHHHHHK...',
    '...KHWHHHHMHKK..',
    '...KHHMMHHHMMSK.',
    '..KSHKKKKKKKMSK.',
    '..KSKffffffffKK.',
    '..KSKffffffffK..',
    '...KfeffffffefK.',
    '...KfKffffffKfK.',
    '...KffffSSffffK.',
    '....KffffffffK..',
    '.....KKffffKK...',
    '....KPKiiiKpK...',
    '...KQPxiijPPpK..',
    '..KQPPPiijPPPpK.',
    '..KPKPPPjPPPKpK.',
    '..KiKPPPPPPPKjK.',
    '...KKPPuuvPPKK..',
    '....KPKuKvKpK...',
    '.....KUK.KUK....',
    '.....KKK.KKK....',
    '................',]

OW_LEFT = [
    '................',
    '.......KKKK.....',
    '.....KKHWWHK....',
    '....KHWHHHHHK...',
    '...KHWHHHMMHHKK.',
    '...KHHKKKMHHHMSK',
    '....KKffKMHHMMSK',
    '....KffffKSMMSSK',
    '....KeffffKSSSK.',
    '...KfKfffffKSSK.',
    '...KSSfffffKKK..',
    '....KKfffffK....',
    '.....KKfffK.....',
    '.....KiiiPK.....',
    '....KiiPPPpK....',
    '....KiPPPPpK....',
    '....KPQPPPpK....',
    '....KPQPPPPpK...',
    '....KPiKPPPpK...',
    '....KKKKPPPHpK..',
    '.....KuuvKKHKK..',
    '.....KUuvK......',
    '.....KKKKK......',
    '................',]

OW_UP = [
    '................',
    '.......KKKK.....',
    '.....KKHWWHK....',
    '....KHWHHHHHK...',
    '...KHWHHMHHHMK..',
    '...KHHHMHHHMMK..',
    '..KSHHMHHHMMSSK.',
    '..KSHMHHHMMMSSK.',
    '..KSMHHHMMSMSSK.',
    '.KSSMHHMMSMSSSK.',
    'KSSKSMMMSSMSKSSK',
    '.KK.KSMMSSSKK.KK',
    '....KKSSSKK.....',
    '....KPKKKKKpK...',
    '...KQPPPPPPPpK..',
    '..KQPPPPPPPPPpK.',
    '..KPKPPPPPPPKpK.',
    '..KiKPPPqPPPKjK.',
    '...KKPPPqPPPKK..',
    '....KHPPqPPHK...',
    '.....KuK.KvK....',
    '.....KUK.KUK....',
    '.....KKK.KKK....',
    '................',]


OW_LEG = {'K': K, 'W': HAIR[0], 'H': HAIR[1], 'M': HAIR[2], 'S': HAIR[3], 'C': HAIR[4], 'e': HAIR[4],
          'f': SKIN[1], 's': SKIN[2], 'Q': PLUM[0], 'P': PLUM[1], 'p': PLUM[2], 'q': PLUM[3],
          'i': IVORY[1], 'j': IVORY[2], 'U': TROU[0], 'u': TROU[1], 'v': TROU[2], 'x': ROSE[1]}


def _step(rows, kind, which, mirror=False):
    """a step frame: rows 0..20 drop one row (the bob); one foot planted, the other lifted.
    kind 'front' (down/up) or 'side'; which 0/1 = which foot is planted."""
    body = ['................'] + list(rows[:21])          # -> rows 0..21
    if kind == 'front':
        sole = {0: '.....KKK........', 1: '.........KKK....'}[which]
        shoe = {0: (5, 7), 1: (9, 11)}[which]
        r21 = list(body[21])
        r21[shoe[0] + 1] = 'U'
        out = body[:21] + [''.join(r21), sole]
    else:
        legs = {0: ['....KuuKvKKHKK..', '...KUK..KvK.....', '...KKK..KKK.....'],
                1: ['....KvvKuKKHKK..', '...KvK..KUK.....', '...KKK..KKK.....']}[which]
        if mirror: legs = [r[::-1] for r in legs]
        out = body[:20] + legs
    return (out + ['................'] * 24)[:24]


def ow_frame(rows):
    from PIL import Image
    im = Image.new('RGBA', (16, 24), (0, 0, 0, 0)); p = im.load()
    for y, r in enumerate(rows[:24]):
        for x, ch in enumerate(r[:16]):
            if ch in OW_LEG: p[x, y] = hx(OW_LEG[ch])
    return im


def ow_sheet():
    from PIL import Image, ImageOps
    right = [r[::-1] for r in OW_LEFT]
    right = [r if i != 15 else r[:9] + 'x' + r[10:] for i, r in enumerate(right)]       # the rose shows on his right
    dirs = [('front', OW_DOWN, False), ('side', OW_LEFT, False), ('side', right, True), ('front', OW_UP, False)]
    sheet = Image.new('RGBA', (64, 96), (0, 0, 0, 0))
    for d, (kind, rows, mir) in enumerate(dirs):
        frames = [rows, _step(rows, kind, 0, mir), rows, _step(rows, kind, 1, mir)]
        for f, fr in enumerate(frames):
            sheet.paste(ow_frame(fr), (16 * f, 24 * d))
    return sheet


# ================================================================= SILHOUETTES (guide 2.1: 6-10 at true size)
def silhouettes():
    """(label, image, verdict). The chosen front and the earlier explorations, filled black."""
    from PIL import Image
    from rv2dt_px import sil_edit, silhouette
    KB = '/home/claude/fangame/art/work/kitbash/dorian/'
    f = front_img()
    old = lambda n: Image.open(KB + 'DORIAN_%s_native80.png' % n).convert('RGBA')
    hat_on = sil_edit(f, sub=[[(12, 0), (29, 0), (29, 22), (12, 22)]], add=[[(36, 0), (45, 0), (45, 4), (48, 5), (48, 7), (33, 7), (33, 5), (36, 4)]],
                      lines=[([(33, 25), (30, 34), (31, 40)], 6)])
    cape = sil_edit(f, add=[[(31, 21), (50, 21), (56, 40), (60, 62), (24, 62), (26, 40)], [(36, 8), (31, 22), (29, 30), (34, 24)]])
    fence = sil_edit(f, sub=[[(53, 28), (70, 28), (70, 80), (53, 80)]], lines=[([(49, 25), (57, 27), (63, 27)], 5), ([(60, 27), (78, 22)], 2)])
    return [('A hat aloft + cane (chosen)', silhouette(f), 'diagonal from hat to cane tip: showman energy; mane + hat + cane = 3 breaks'),
            ('B arms wide (old pick S)', silhouette(old('S')), "pose is Sycamore's; kept only the hat aloft"),
            ('C leaning on the cane', silhouette(old('B')), "reads old and frail: the cane he doesn't need"),
            ('D cane as a baton', silhouette(old('A')), 'reads conductor; no hat, weaker top break'),
            ('E hat on his head', hat_on, 'the hat hides the mane, the hook'),
            ('F opera cape + mane', cape, 'cape + plum + mane = the vampire read (guide 2.1)'),
            ('G cane pointed (fencer)', fence, 'aggressive; a first Warden makes you look good')]


if __name__ == '__main__':
    what = sys.argv[1] if len(sys.argv) > 1 else 'all'
    for k, (n, semi, orph) in export_all().items():
        print('%-20s colours %2d  semi %d  orphans %s' % (k, n, semi, orph))
