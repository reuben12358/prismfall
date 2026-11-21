"""Tamsin Loom, Gym 2 Warden (Bug) - redo v2 (art/REDO_V2_BRIEF.md).
Concept: "the girl wrapped in her grandmother's last weave". 19, Briarwick's weaver: apologetic, meticulous, fierce
when her people are threatened. Kept from the user's pick A: the moth-wing shawl woven by Granny Loom, the measuring
tape round her neck, needles through a messy bun, worried brows. Changed: the shawl is silk cream with a gold
border (the brown wings read muddy), her dress is indigo (the weaver's dye), and one berry-red thread is the accent.
Bug = thread and silk; Elowen = cream linen + lantern-gold thread. Original construction, no donor pixels.
python3 -I tools/kitbash/rv2dt_tamsin.py  -> art/work/redo_v2/TAMSIN/"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rv2dt_px import Art, hx, up, lint, limb

OUT = '/home/claude/fangame/art/work/redo_v2/TAMSIN/'

# ---------------------------------------------------------------- colour plan (3 + 1)
K = '1a1220'
SKIN = ('f8d6b8', 'eab48e', 'c98a6c', '9c5e4e')
HAIR = ('b8727a', '8a4a54', '68343e', '4a2230', '2e1420')       # hi, light, mid, shadow, crease (cocoa-rose)
SILK = ('fffaf0', 'f4e6cc', 'dcc4b4', 'b39aa4')                  # 1 silk cream: the shawl (main)
INDIGO = ('6878c0', '46529c', '323a7a', '20245a')                # 2 indigo linen: the dress
GOLD = ('ffe49a', 'f2bc4e', 'c88a32', '8a5626')                  # 3 lantern gold: tape, border, needles
BERRY = ('ff7a96', 'e2365a', 'a8203e')                           # accent: the one red thread
EYE_W, IRIS, IRIS_D, HL = 'f8f4f4', '8a7ad0', '4a3c8e', 'ffffff'
LIP_D, MOUTH_IN, TONGUE, TEETH = '9a3e48', '4a1424', 'd0606a', 'fbf6f2'
BLUSH = 'e8907c'


# ================================================================= PORTRAIT (48-px art, 96x96 file)
def portrait(expr='neutral'):
    a = Art(48, 48, K)
    a.ramp('skin', *SKIN); a.ramp('hair', HAIR[0], HAIR[1], HAIR[2], HAIR[3]); a.ramp('silk', *SILK)
    a.ramp('ind', *INDIGO); a.ramp('gold', *GOLD); a.ramp('berry', BERRY[0], BERRY[1], BERRY[2], BERRY[2])

    # ---- back to front
    a.poly('skin.neck', [(20, 36), (30, 36), (31, 47), (19, 47)])
    a.line('gold.needle1', [(2, 1), (14, 12)], 2)                    # knitting needles through the bun
    a.line('gold.needle2', [(9, 0), (11, 13)], 2)
    a.poly('hair.mass', [(12, 8), (18, 4), (26, 3), (34, 5), (39, 9), (42, 14), (42, 21), (40, 27), (38, 20),
                         (36, 16), (30, 14), (22, 15), (17, 19), (16, 24), (15, 32), (14, 39), (10, 41), (8, 34),
                         (8, 24), (9, 15)])
    a.ell('hair.bun', (2, 3, 16, 15))
    a.poly('skin.ear', [(16, 25), (13, 24), (12, 27), (13, 31), (16, 32)])
    # J2 soft V: turns from the cheekbone in straight lines to a small chin at x 27-30
    a.poly('skin.face', [(16, 19), (21, 15), (30, 14), (36, 16), (39, 20), (39, 27), (37, 33), (34, 38), (30, 41),
                         (27, 42), (23, 40), (19, 36), (16, 31), (15, 25)])
    a.poly('hair.side', [(13, 15), (17, 16), (18, 22), (17, 30), (15, 38), (13, 34), (12, 26)])
    a.poly('hair.fr1', [(19, 7), (27, 4), (35, 6), (41, 12), (42, 20), (40, 28), (38, 22), (36, 18), (32, 16), (28, 13)])
    a.poly('hair.fr2', [(21, 9), (27, 8), (32, 11), (34, 15), (32, 20), (29, 16), (25, 14), (21, 13)])
    a.poly('hair.fr3', [(16, 11), (20, 9), (24, 12), (25, 16), (23, 20), (21, 16), (17, 15)])
    a.poly('hair.strand', [(5, 14), (7, 14), (6, 19), (7, 23), (5, 23), (4, 19)])  # one loose strand from the bun
    a.poly('hair.fly1', [(24, 5), (28, 1), (33, 0), (38, 1), (39, 4), (34, 3), (30, 5), (28, 7)])   # a cowlick: the bun is messy
    # ---- shoulders: indigo dress neckline, the silk shawl over both shoulders, the tape round the neck
    a.poly('ind.dress', [(10, 47), (12, 42), (19, 40), (31, 40), (38, 42), (40, 47)])
    a.poly('silk.l', [(0, 47), (0, 41), (6, 38), (13, 37), (18, 40), (16, 44), (14, 47)])
    a.poly('silk.r', [(47, 47), (47, 41), (42, 38), (35, 37), (32, 40), (34, 44), (36, 47)])
    a.poly('gold.edgeL', [(13, 37), (18, 40), (16, 44), (14, 47), (12, 47), (14, 43), (15, 40)])
    a.poly('gold.edgeR', [(35, 37), (32, 40), (34, 44), (36, 47), (38, 47), (36, 43), (35, 40)])
    a.poly('gold.tapeL', [(20, 39), (21, 39), (22, 47), (21, 47)])
    a.poly('gold.tapeR', [(29, 39), (30, 39), (29, 47), (28, 47)])

    a.base()
    # ---- light from the upper left
    for m in ('hair.mass', 'hair.bun', 'hair.side', 'hair.fr1', 'hair.fr2', 'hair.fr3', 'hair.strand', 'hair.fly1'):
        a.band('hair', 2, 'b', 2, mats=[m]); a.band('hair', 2, 'r', 1, mats=[m])
    a.band('skin', 2, 'r', 2, mats=['skin.face'], only=[(31, 26), (47, 26), (47, 43), (31, 43)])
    a.band('skin', 2, 'r', 1, mats=['skin.face'], only=[(31, 15), (47, 15), (47, 25), (31, 25)])
    a.tone('skin', 2, [(x, y) for y in range(36, 48) for x in range(18, 32)], mats=['skin.neck'])
    for m in ('silk.l', 'silk.r', 'ind.dress'):
        a.band(m.split('.')[0], 2, 'r', 2, mats=[m])
    a.band('silk', 0, 't', 1, mats=['silk.l', 'silk.r'])
    a.band('gold', 2, 'r', 1, mats=['gold.edgeL', 'gold.edgeR', 'gold.tapeL', 'gold.tapeR'])
    a.lines(fold_groups=('hair', 'silk', 'ind'))
    a.tone('skin', 3, [(x, y) for y in range(30, 47) for x in range(14, 36) if a.at(x, y) == 'skin.neck' and a.at(x, y - 1) == 'skin.face'])
    under = [(x, y) for y in range(13, 25) for x in range(16, 40)
             if a.at(x, y) == 'skin.face' and a.is_g(x, y - 1, 'hair') and a.col[y][x] == a.ramps['skin'][1]]
    a.tone('skin', 2, under)
    a.drop_orphans()
    hair_pass(a)
    costume_pass(a)
    face_pass(a, expr)
    return a


def hair_pass(a):
    W, L, M, S, C = (hx(c) for c in HAIR)
    arcs = [(5, 6), (6, 5), (7, 4), (8, 4), (9, 4),                                   # bun
            (21, 7), (22, 6), (23, 6), (24, 5), (25, 5), (26, 5),                    # fringe lock over the crown
            (33, 8), (34, 9), (35, 10), (36, 11), (37, 13),                          # fringe lock, front edge
            (18, 13), (19, 12), (20, 12),                                             # short lock
            (13, 19), (13, 20), (13, 21)]                                             # side lock
    a.paint([p for p in arcs if a.is_g(*p, 'hair') and a.col[p[1]][p[0]] != hx(K)], W)
    occ = [(x, y) for y in range(47) for x in range(48) if a.is_g(x, y, 'hair') and a.col[y][x] == M
           and a.col[y + 1][x] in (C, hx(K)) and a.is_g(x, y + 1, 'hair')]
    a.paint(occ, S)
    # the berry thread wound round the bun (accent #1)
    a.paint([(4, 11), (5, 12), (6, 12), (7, 13), (8, 13), (9, 13), (10, 13), (11, 12)], BERRY[1])


def costume_pass(a):
    G = [hx(c) for c in GOLD]
    # tick marks on the tape: every other pixel in the deep gold
    a.paint([(20, 41), (21, 43), (21, 45), (29, 41), (29, 43), (28, 45)], G[3])
    # the shawl's woven band: one thin gold vein following each shoulder (the moth-wing border, with restraint)
    a.paint([(2, 44), (3, 43), (4, 43), (5, 42), (6, 42), (7, 41), (8, 41), (9, 41)], G[2])
    a.paint([(45, 44), (44, 43), (43, 43), (42, 42), (41, 42), (40, 41), (39, 41), (38, 41)], G[2])


# E1 big round, but Tamsin's own: the outer corner droops (gentle, anxious), heavy 2-row lash, violet iris
EYES = {
    'neutral':   (['..KKKKK.', '.KKKKKKK', 'KKEaaaaK', '.KEaaWaK', '..EaAAaE', '..EaAAaE', '..EEAAE.', '...sss..'],
                  ['.KKKK..', 'KKKKKKK', 'KEaaaaK', 'KEaaWaK', '.EaAAa.', '.EaAAa.', '.EEAA..', '..ss...']),
    'happy':     (['........', '........', '..KKKK..', '.K....K.', 'K......K', '.ssssss.'],
                  ['.......', '.......', '.KKKK..', 'K....K.', '.ssss..']),
    'sad':       (['........', '.KKKKKK.', 'KKKKKKKK', '.KEaaWaK', '..EaAAaE', '..EaAAaE', '..EEAAE.', '...sss..'],
                  ['.......', '.KKKKK.', 'KKKKKKK', 'KEaaWaK', '.EaAAa.', '.EaAAa.', '.EEAA..', '..ss...']),
    'angry':     (['........', '........', 'KKKKKKKK', '.KEaaWaK', '..EaAAaE', '..saAAs.', '...sss..'],
                  ['.......', '.......', 'KKKKKKK', 'KEaaWaK', '.EaAAa.', '.saAs..', '..ss...']),
    'surprised': (['..KKKKK.', '.KKKKKKK', 'KKEEEEEK', '.KEEaWEK', '.KEaAaEE', '..EEAAE.', '..EEEE..', '...sss..'],
                  ['.KKKK..', 'KKKKKKK', 'KEEEEEK', 'KEaWEEK', '.EaAaE.', '.EEAE..', '.EEE...', '..ss...']),
    'flustered': (['........', 'KKK.....', '...KKK..', '.....KKK', '...KKK..', 'KKK.....', '........'],
                  ['.......', '....KKK', '..KKK..', 'KKK....', '..KKK..', '....KKK', '.......']),
}


def face_pass(a, expr):
    L = {'K': hx(K), 'B': hx(HAIR[3]), 'b': hx(HAIR[2]), 'E': hx(EYE_W), 'A': hx(IRIS), 'a': hx(IRIS_D), 'W': hx(HL),
         's': hx(SKIN[2]), 'd': hx(SKIN[3]), 'h': hx(SKIN[0]), 'R': hx(LIP_D), 'o': hx(MOUTH_IN), 't': hx(TONGUE),
         'T': hx(TEETH), 'r': hx(BLUSH), 'w': hx('d8eefa'), 'n': hx(INDIGO[2])}
    # brows B1 soft, but her resting brows lift at the inner end (she is always a little worried)
    near = {'neutral': (18, 19, ['   BBb', 'bBB   ']), 'happy': (18, 18, ['  BBBb', 'bBB   ']),
            'sad': (18, 19, ['    BB', '  BBb ', 'bB    ']), 'angry': (18, 19, ['bBB   ', '  BBBB']),
            'surprised': (18, 17, ['  BBBb', 'bBB   ']), 'flustered': (18, 18, ['    BB', '  BBb ', 'bB    '])}[expr]
    far = {'neutral': (31, 19, ['bBB   ', '   BBb']), 'happy': (31, 18, ['bBBB  ', '    Bb']),
           'sad': (31, 19, ['BB    ', ' bBB  ', '    Bb']), 'angry': (31, 19, ['   BBb', 'BBBB  ']),
           'surprised': (31, 17, ['bBBB  ', '    Bb']), 'flustered': (31, 18, ['BB    ', ' bBB  ', '    Bb'])}[expr]
    for x0, y0, rows in (near, far):
        a.stamp(x0, y0, rows, L)
    e_near, e_far = EYES[expr]
    ey = 21 if expr != 'surprised' else 20
    a.stamp(17, ey, e_near, L); a.stamp(31, ey, e_far, L)
    # nose: one shadow pixel pair, young
    a.stamp(30, 30, ['s', 'ds'], L)
    # mouths (STYLE_GUIDE 3.6)
    M = {
        'neutral':   (25, 35, ['R    ', '.RRRR', '..ss ']),                    # nervous: one corner lower
        'happy':     (24, 34, ['K     K', 'KTTTTK.', '.KoooK.', '..KtK..', '...s...']),
        'sad':       (25, 35, ['.RRR.', 'R   R', '.sss.']),
        'angry':     (24, 34, ['KKKKKK', 'KTTTTK', 'KooooK', 'KTTTTK', '.KKKK.']),
        'surprised': (26, 34, ['.KK.', 'KooK', 'KotK', '.KK.', '.ss.']),
        'flustered': (25, 34, ['.K.K.', 'KoKoK', 'KoooK', '.KKK.', '.sss.']),
    }[expr]
    a.stamp(*M, L)
    if expr in ('flustered', 'happy'):
        a.paint([(19, 29), (21, 29), (23, 29), (33, 29), (35, 29)], BLUSH)               # blush hatch
    if expr == 'flustered':
        a.stamp(40, 16, ['.w.', 'wwK', 'wwK', '.K.'], {'w': hx('d8eefa'), 'K': hx('5a8ab8')})   # sweat drop
    if expr == 'sad':
        a.paint([(19, 29), (19, 30)], 'd8eefa')                                           # a tear starting
    a.paint([(19, 17), (20, 17), (21, 17)], SKIN[0])                                      # forehead light


PORTRAIT_EXPRS = ('neutral', 'happy', 'sad', 'angry', 'surprised', 'flustered')


def portrait_img(expr='neutral'):
    return portrait(expr).image()


def export_all():
    """writes the work files in the Graphics layout (nothing is installed):
    Trainers/LEADER_TAMSIN.png (160x160) + _native80, Characters/TAMSIN.png (128x192) + _native,
    Portraits/TAMSIN_<expr>.png (96x96) + Portraits/native/*_48.png. Returns lint results."""
    res = {}
    for d in ('Trainers', 'Characters', 'Portraits', 'Portraits/native'):
        os.makedirs(OUT + d, exist_ok=True)
    for e in PORTRAIT_EXPRS:
        im = portrait_img(e)
        im.save(OUT + 'Portraits/native/TAMSIN_%s_48.png' % e); up(im, 2).save(OUT + 'Portraits/TAMSIN_%s.png' % e)
        res['portrait ' + e] = lint(im)
    fr = front_img()
    fr.save(OUT + 'Trainers/LEADER_TAMSIN_native80.png'); up(fr, 2).save(OUT + 'Trainers/LEADER_TAMSIN.png')
    res['front'] = lint(fr, keep=FRONT_KEEP)
    ow = ow_sheet()
    ow.save(OUT + 'Characters/TAMSIN_native.png'); up(ow, 2).save(OUT + 'Characters/TAMSIN.png')
    res['overworld'] = lint(ow)
    return res


# ================================================================= BATTLE FRONT (80x80 art, 160x160 file)
# Pose: "sorry - sorry -": she spreads one wing of Granny Loom's shawl like a moth showing its pattern, the other hand
# holds the spool of berry thread to her chest; knees together, toes in, an apologetic smile. Facing 3/4 left.
FRONT_HEAD = (31, 0, [
    '...................gK.',
    '..............gK..gK..',
    '..........KK..gKKgK...',
    '......KKKKHHKKgHgK....',
    '....KKHHHWWHHKHHMMK...',
    '...KHHWWHHHHHKHMMSSK..',
    '..KHHWHHHHHHHHKMSSSK..',
    '..KHHHHHMMHHHHMKKKK...',
    '.KHHHMMKMMHHHHMMSK....',
    '.KHHMKKfKMHHHMMMSK....',
    '.KHMKfffffKMHHMMSK....',
    '..KKffffffffKMMSSK....',
    '..KfKKffKKKKfKMSK.....',
    '..KfawffaawEfKSK......',
    '..KfAAffaAAEfKSK......',
    '..KffffffffsfK........',
    '...KrrffffrssK........',
    '...KffffRRfssK........',
    '....KffffffsK.........',
    '.....KKffssK..........',
    '.......KKKK...........',])
SHOE = ('8a4a54', '68343e', '4a2230', '2e1420')       # soft cocoa leather = the hair ramp


def front_shapes(a):
    # ---- legs (knees together, toes in) and shoes
    a.poly('ind.legL', limb((38, 55), (36, 73), 5, 4))
    a.poly('ind.legR', limb((42, 55), (45, 73), 5, 4))
    a.poly('shoe.l', [(32, 77), (32, 75), (34, 73), (38, 73), (39, 77)])
    a.poly('shoe.r', [(42, 77), (42, 73), (46, 73), (48, 75), (48, 77)])
    # ---- the far drape of the shawl (behind the far arm), then the dress
    a.poly('ind.skirt', [(34, 35), (46, 35), (49, 44), (52, 55), (47, 57), (40, 56), (33, 57), (28, 55), (31, 45)])
    a.poly('ind.body', [(33, 22), (46, 22), (48, 29), (46, 36), (34, 36), (32, 29)])
    a.poly('skin.neck', [(37, 19), (41, 19), (41, 23), (37, 23)])
    a.poly('silk.collar', [(35, 22), (43, 22), (43, 24), (41, 26), (39, 25), (37, 26), (35, 24)])
    a.poly('skin.headarea', [(34, 8), (44, 8), (44, 20), (34, 20)])
    # ---- the near sleeve under the wing, reaching up to the wing's corner
    a.poly('ind.armN', limb((47, 24), (56, 22), 6, 5) + limb((56, 22), (62, 21), 5, 4))
    # ---- the spread wing (near side): forewing to the raised hand, hindwing lobe below, a notch between
    a.poly('silk.wing', [(44, 22), (50, 21), (57, 20), (63, 20), (67, 22), (69, 27), (68, 33), (65, 36), (62, 37),
                         (64, 41), (64, 46), (61, 51), (56, 53), (52, 50), (50, 44), (49, 37), (47, 30), (45, 26)])
    # ---- the far drape of the shawl hangs over the far shoulder; the far hand comes out of it with the spool
    a.poly('silk.far', [(33, 21), (37, 21), (36, 28), (35, 36), (34, 44), (32, 50), (28, 52), (25, 49), (26, 42),
                        (24, 37), (25, 30), (28, 24)])
    a.poly('ind.armF', limb((32, 24), (31, 33), 6, 5), clip=('ind', None))
    a.poly('ind.foreF', limb((31, 32), (37, 31), 5, 5))
    a.poly('skin.handF', [(35, 28), (40, 28), (41, 33), (36, 34)])
    # ---- the near hand holding the wing's top corner
    a.poly('skin.handN', [(62, 18), (66, 18), (67, 22), (63, 23)])
    a.poly('ind.cuffN', [(58, 20), (61, 19), (62, 23), (59, 24)])


def front():
    a = Art(80, 80, K)
    a.ramp('skin', *SKIN); a.ramp('hair', HAIR[0], HAIR[1], HAIR[2], HAIR[3]); a.ramp('silk', *SILK)
    a.ramp('ind', *INDIGO); a.ramp('gold', *GOLD); a.ramp('shoe', *SHOE)
    front_shapes(a)
    a.base()
    for g in ('ind', 'silk', 'shoe'):
        a.band(g, 2, 'r', 2)
    a.band('skin', 2, 'r', 1)
    a.band('ind', 0, 'l', 1, mats=['ind.body', 'ind.skirt', 'ind.armF'])
    a.band('silk', 0, 'l', 1, mats=['silk.far'])
    a.tone_line('silk', 2, [(26, 37), (30, 38), (34, 37)], mats=['silk.far'])
    a.band('silk', 0, 't', 1, mats=['silk.wing'])
    a.tone('ind', 2, [(x, y) for y in range(56, 80) for x in range(30, 50)], mats=['ind.legL', 'ind.legR'])
    a.tone('ind', 1, [(x, y) for y in range(56, 80) for x in range(30, 50) if a.at(x, y) in ('ind.legL', 'ind.legR')
                      and a.at(x - 1, y) not in ('ind.legL', 'ind.legR')])
    # skirt folds (two soft pleats) and the waist seam
    a.tone_line('ind', 2, [(38, 40), (36, 54)]); a.tone_line('ind', 2, [(44, 40), (47, 54)])
    a.tone_line('ind', 3, [(34, 35), (46, 35)])
    # the wing: the hindwing lobe turns away from the light; one curved band crosses the forewing (moth pattern)
    a.tone_poly('silk', 2, [(49, 37), (62, 37), (64, 41), (64, 46), (61, 51), (56, 53), (52, 50), (50, 44)], mats=['silk.wing'])
    a.tone_line('silk', 3, [(49, 36), (55, 37), (62, 37)], mats=['silk.wing'])
    a.tone_line('silk', 2, [(48, 27), (53, 26), (58, 27), (63, 30), (66, 33)], mats=['silk.wing'])
    a.lines(fold_groups=('ind', 'silk'))
    wing_border(a)
    a.drop_orphans()
    front_head(a)
    return a


def wing_border(a):
    """the woven gold border: 1 px inside the wing's outline along its outer (right and lower) edge"""
    g = hx(GOLD[1]); g2 = hx(GOLD[2]); k = hx(K)
    pts = []
    for y in range(80):
        for x in range(80):
            m = a.at(x, y)
            if m not in ('silk.wing', 'silk.far') or a.col[y][x] == k: continue
            out = 1 if m == 'silk.wing' else -1                     # the outer edge: right for the wing, left for the drape
            if (a.at(x + out, y) == m and a.col[y][x + out] == k and a.at(x + 2 * out, y) is None) or \
               (a.at(x, y + 1) == m and a.col[y + 1][x] == k and a.at(x, y + 2) is None and (x > 50 or x < 34)):
                pts.append((x, y))
    a.paint(pts, GOLD[1])
    a.paint([p for p in pts if p[1] > 40], GOLD[2])
    # one moth eyespot on the hindwing: gold ring, indigo centre
    a.stamp(55, 42, ['.GG.', 'GnnG', 'GnnG', '.GG.'], {'G': g2, 'n': hx(INDIGO[2])})
    # the skirt's embroidered hem: a lantern-gold thread band one row above the hem (Elowen embroidery)
    hem = [(x, y) for y in range(50, 58) for x in range(26, 54) if a.at(x, y) == 'ind.skirt' and a.col[y][x] != k
           and a.at(x, y + 2) is None and a.at(x, y + 1) == 'ind.skirt']
    a.paint(hem, GOLD[2])


def front_head(a):
    L = {'K': hx(K), 'W': hx(HAIR[0]), 'H': hx(HAIR[1]), 'M': hx(HAIR[2]), 'S': hx(HAIR[3]), 'C': hx(HAIR[4]),
         'f': hx(SKIN[1]), 's': hx(SKIN[2]), 'h': hx(SKIN[0]), 'd': hx(SKIN[3]), 'E': hx(EYE_W), 'A': hx(IRIS),
         'a': hx(IRIS_D), 'w': hx(HL), 'R': hx(LIP_D), 'g': hx(GOLD[1]), 'G': hx(GOLD[2]), 'x': hx(BERRY[1]),
         'r': hx(BLUSH), 'y': hx(BERRY[2]), 'o': hx(GOLD[3]), 'n': hx(INDIGO[2])}
    x0, y0, rows = FRONT_HEAD
    for j, r in enumerate(rows):
        for i, ch in enumerate(r):
            if a.at(x0 + i, y0 + j) == 'skin.headarea': a.erase([(x0 + i, y0 + j)])
    a.stamp(x0, y0, rows, L, mat='head')
    # the berry thread wound round the bun (accent #1, visible from the back too)
    a.paint([(45, 8), (46, 8), (47, 9)], BERRY[1])
    # the spool (wood = gold ramp) with the berry thread, held at her chest; the loose end trails down (accent #2)
    a.stamp(35, 27, ['.KKKK.', 'KoggoK', 'KxxxyK', 'KxxyyK', 'KoggoK', '.KKKK.'], L)
    a.paint([(36, 33), (35, 34), (35, 35), (34, 36), (34, 37), (34, 38), (35, 39)], BERRY[1], lock=True)
    # the measuring tape round her neck, hanging down both sides of the bodice
    a.paint([(36, 23), (36, 24), (35, 25), (35, 26)], GOLD[1]); a.paint([(42, 23), (42, 24), (43, 25), (43, 26), (43, 27), (43, 28), (43, 29)], GOLD[1])
    a.paint([(43, 26), (43, 28)], GOLD[3])
    # ink on the fingertips of the far hand
    a.paint([(41, 31), (41, 32)], INDIGO[2])
    # the near hand pinching the wing's corner: knuckles over the edge
    a.stamp(61, 17, ['.KKKK.', 'KhfffK', 'KffffK', '.KfsK.'], L)
    # sweat drop (sorry - sorry -)
    a.stamp(30, 9, ['.w', 'ww', 'wK'], {'w': hx('d8eefa'), 'K': hx('5a8ab8')})


FRONT_KEEP = ()


def front_img():
    return front().image()


# ================================================================= OVERWORLD (16x24 art per frame, sheet 128x192)
# designed at true size; rows: down, left, right (= left mirrored), up; frames: stand, step, stand, step.
# The hook survives at 16 px: the bun with two needles (antennae), the cream shawl with its gold hem; the berry
# thread shows from the front (the spool) and the back (wound round the bun).
OW_DOWN = [
    '.........g.g....',
    '.........KgKK...',
    '......KKKHHMMK..',
    '....KKHWWHKMMSK.',
    '...KHWHHHHHKSSK.',
    '..KHWHHHHHHHKSK.',
    '..KHHHMMHHHHHMK.',
    '.KHHMKKMMKHHHMK.',
    '.KHMKffKfffKHMK.',
    '.KMKfffffffffKK.',
    '.KSKfaffffafKK..',
    '..KKfKffffKfK...',
    '...KrffffffrK...',
    '....KffssffK....',
    '.....KKffKK.....',
    '...KKiigKiiKK...',
    '..KIiiiNNiiijK..',
    '..KIiiNxxNiijK..',
    '..KjiKNxxNKijK..',
    '..KgjKNNNNKjgK..',
    '...KKgNNNNgKK...',
    '.....KnK.KnK....',
    '.....KSK.KSK....',
    '................',]

OW_LEFT = [
    '.........g.g....',
    '.........KgKK...',
    '......KKKHHMMK..',
    '.....KHWWHHKMSK.',
    '....KHWHHHHKSSK.',
    '...KHWHHHHHHKSK.',
    '..KHHHHMMHHHHMK.',
    '..KHHHKKMMHHHMK.',
    '...KKffKMMHHMSK.',
    '...KfffffKMMSK..',
    '...KaffffKSSK...',
    '..KfKffffffK....',
    '...KffffrrK.....',
    '....KsfffK......',
    '.....KKKK.......',
    '....KiiigK......',
    '...KIiiiijK.....',
    '...KIiNxNijK....',
    '...KIiNNNijK....',
    '...KjiNNNjjK....',
    '...KgjNNNjgK....',
    '....KKNNNKK.....',
    '.....KnnK.......',
    '.....KSSK.......',]

OW_UP = [
    '......g...g.....',
    '......KgKgK.....',
    '.....KHWHHMK....',
    '.....KHHHMSK....',
    '.....KxxxxxK....',
    '....KKKKKKKKK...',
    '...KHWHHHHHHMK..',
    '..KHWHHHMHHHMSK.',
    '..KHHHMHHHMMMSK.',
    '..KHHMHHHMMSMSK.',
    '..KSMMHHMMSSSK..',
    '...KSSMMMSSSK...',
    '....KKSSSSKK....',
    '...KKiiiiiiKK...',
    '..KIiiiiiiiijK..',
    '..KIiiiiiiiijK..',
    '..KIiiiGGiiijK..',
    '..KiiiGnnGiijK..',
    '..KjiiiGGiijjK..',
    '..KgjjjjjjjjgK..',
    '...KKgggggggK...',
    '.....KnK.KnK....',
    '.....KSK.KSK....',
    '................',]

OW_LEG = {'K': K, 'W': HAIR[0], 'H': HAIR[1], 'M': HAIR[2], 'S': HAIR[3], 'f': SKIN[1], 's': SKIN[2],
          'a': IRIS_D, 'I': SILK[0], 'i': SILK[1], 'j': SILK[2], 'g': GOLD[1], 'G': GOLD[2],
          'N': INDIGO[1], 'n': INDIGO[2], 'q': INDIGO[3], 'x': BERRY[1], 'r': BLUSH}


def _step(rows, kind, which, mirror=False):
    body = ['................'] + list(rows[:21])
    if kind == 'front':
        sole = {0: '.....KSK........', 1: '.........KSK....'}[which]
        out = body[:22] + [sole]
    else:
        legs = {0: ['....KnKKnK......', '...KSK..KSK.....'], 1: ['....KnKKnK......', '...KSK..KSK.....']}[which]
        if which == 1: legs = ['.....KnnK.......', '.....KSSK.......']
        if mirror: legs = [r[::-1] for r in legs]
        out = body[:21] + legs
    return (out + ['................'] * 24)[:24]


def ow_frame(rows):
    from PIL import Image
    im = Image.new('RGBA', (16, 24), (0, 0, 0, 0)); p = im.load()
    for y, r in enumerate(rows[:24]):
        for x, ch in enumerate(r[:16]):
            if ch in OW_LEG: p[x, y] = hx(OW_LEG[ch])
    return im


def ow_sheet():
    from PIL import Image
    right = [r[::-1] for r in OW_LEFT]
    dirs = [('front', OW_DOWN, False), ('side', OW_LEFT, False), ('side', right, True), ('front', OW_UP, False)]
    sheet = Image.new('RGBA', (64, 96), (0, 0, 0, 0))
    for d, (kind, rows, mir) in enumerate(dirs):
        frames = [rows, _step(rows, kind, 0, mir), rows, _step(rows, kind, 1, mir)]
        for f, fr in enumerate(frames):
            sheet.paste(ow_frame(fr), (16 * f, 24 * d))
    return sheet


# ================================================================= SILHOUETTES (guide 2.1: 6-10 at true size)
def silhouettes():
    from PIL import Image, ImageOps
    from rv2dt_px import sil_edit, silhouette
    KB = '/home/claude/fangame/art/work/kitbash/tamsin/'
    f = front_img()
    old = lambda n: Image.open(KB + 'TAMSIN_%s_native80.png' % n).convert('RGBA')
    wing = [(44, 22), (50, 21), (57, 20), (63, 20), (67, 22), (69, 27), (68, 33), (65, 36), (62, 37), (64, 41),
            (64, 46), (61, 51), (56, 53), (52, 50), (50, 44), (49, 37), (47, 30), (45, 26)]
    mirror = [(80 - x, y) for x, y in wing]                      # the far wing spread the same way
    both = sil_edit(f, add=[mirror])
    wrapped = sil_edit(f, sub=[[(48, 14), (80, 14), (80, 60), (48, 60)]],
                       add=[[(44, 21), (50, 24), (52, 36), (53, 50), (49, 53), (45, 46), (44, 30)]])
    hood = sil_edit(f, add=[[(32, 4), (38, 0), (46, 0), (52, 5), (53, 14), (50, 22), (31, 22), (30, 12)]])
    plain = sil_edit(f, sub=[wing, [(24, 20), (34, 20), (34, 54), (24, 54)], [(44, 0), (56, 0), (56, 12), (44, 12)]],
                     add=[[(30, 24), (34, 23), (33, 36), (30, 36)]],
                     lines=[([(48, 25), (52, 33), (50, 40)], 4), ([(45, 10), (48, 18), (47, 30)], 3)])
    return [('A one wing spread (chosen)', silhouette(f), 'wing + bun/needles + toes-in: shy and showing at once'),
            ('B hugging the plush (old pick A)', silhouette(old('A')), 'symmetric wings = a moth costume; read muddy'),
            ('C needle thrust (old B)', silhouette(old('B')), 'off-character for her default; keep for anger'),
            ('D both wings spread', both, 'a costume, not a shawl; too literal for Bug'),
            ('E wrapped up, peeking', wrapped, 'a soft blob: fewer than 3 breaks'),
            ('F hood up', hood, 'hoods belong to Thistle and the Mourner'),
            ('G no shawl, braid', plain, 'generic villager; loses the hook')]


if __name__ == '__main__':
    what = sys.argv[1] if len(sys.argv) > 1 else 'all'
    for k, (n, semi, orph) in export_all().items():
        print('%-20s colours %2d  semi %d  orphans %s' % (k, n, semi, orph))
