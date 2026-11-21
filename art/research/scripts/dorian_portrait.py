"""Dorian Pell - 48-px portrait (exported 96x96), original construction per art/STYLE_GUIDE.md.
Concept: the curtain call that never ended. A 56-year-old ex-matinee idol, still handsome and very aware of it:
swept-back silver mane in five sculpted clumps + one matinee lock, strong dark brows (far one arched),
hooded amber eyes, pencil moustache, a knowing closed smile, plum velvet coat with silver satin lapels,
ivory silk cravat, one red rose (the accent).
python3 -I art/research/scripts/dorian_portrait.py [out_dir]"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pxbuild import Canvas, hx

OUT = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/fangame/art/research/style_test'
K = hx('1a1220')                      # outline: near-black, warm violet tint (guide 4.4)

# palette (guide 3: plum / silver / ivory + rose accent; skin and eyes are not counted)
SK = ('fde0c8', 'f3c4a2', 'd9957a', 'a95f4d')
HAIR = ('fbfaff', 'cdc8e6', 'a29bc6', '6e6698')
HD = hx('4a4274')                     # hair crease
COAT = ('a0549a', '773372', '522360', '351640')
IVORY = ('ffffff', 'f8f0e4', 'dccfbf', 'b8a596')
BROW = hx('3e3656'); BROW2 = hx('5e5680')
EYE_W, IRIS, IRIS_D, HL = hx('f8f4f0'), hx('dc9a36'), hx('8a4c1c'), hx('ffffff')
LIP, LIP_D = hx('c86a62'), hx('8e3a40')
MOUTH_IN, TONGUE, TEETH = hx('4a1424'), hx('c4545e'), hx('fbf6f2')
STACHE = hx('4a4274'); STACHE2 = hx('7c74a2')
ARCS = True
ROSE = (hx('ff8a96'), hx('e33a4c'), hx('a51d36'), hx('6a1028'))
LEAF = (hx('5cae62'), hx('2f7a48'))


def build(expr='knowing'):
    c = Canvas()
    for n, r in (('skin', SK), ('ear', SK), ('neck', SK), ('coat', COAT), ('lining', HAIR), ('ivory', IVORY)):
        c.ramp(n, *r)
    for i in range(6):
        c.ramp('hair%d' % i, *HAIR)

    # --- back to front -------------------------------------------------------------------------
    c.poly('neck', [(18, 34), (31, 36), (32, 46), (17, 46)])
    # the mane: one silhouette (hair0) first, so there are no holes; clumps on top only add creases
    c.poly('hair0', [(42, 6), (40, 3), (36, 1), (30, 0), (22, 0), (14, 1), (8, 4), (4, 8), (1, 13), (6, 14),
                     (2, 21), (7, 21), (3, 28), (8, 27), (11, 29), (13, 26), (13, 21), (15, 17),
                     (20, 13), (27, 12), (35, 14), (37, 18), (38, 15), (38, 9), (39, 6)])
    c.poly('hair4', [(17, 13), (12, 15), (9, 18), (7, 21), (5, 25), (3, 28), (8, 27), (11, 24), (13, 21), (15, 17)])
    c.poly('hair3', [(23, 6), (15, 7), (9, 10), (6, 14), (4, 18), (2, 21), (7, 21), (10, 17), (15, 14),
                     (21, 12), (24, 11)])                                                       # side sweep
    c.poly('hair2', [(30, 0), (22, 0), (14, 1), (8, 4), (4, 8), (1, 13), (5, 13), (9, 10), (15, 7), (23, 6),
                     (30, 5)])                                                                   # crown sweep
    c.poly('hair1', [(21, 12), (22, 7), (25, 3), (30, 1), (36, 1), (40, 3), (42, 6), (39, 6), (38, 9),
                     (38, 15), (37, 18), (35, 14), (31, 12), (27, 12)])                         # crest / pompadour
    c.poly('ear', [(14, 22), (11, 21), (10, 23), (10, 28), (11, 30), (13, 31), (14, 30)])
    c.poly('skin', [(15, 17), (19, 14), (26, 13), (32, 13), (36, 15), (37, 18), (38, 22), (38, 26), (37, 29),
                    (36, 32), (34, 35), (32, 38), (29, 41), (25, 42), (22, 41), (19, 38), (17, 35), (15, 31),
                    (14, 26), (14, 21)])
    c.poly('hair0', [(23, 12), (27, 11), (28, 14), (26, 17), (25, 14)])                      # matinee lock
    c.poly('coat', [(0, 47), (0, 43), (7, 40), (15, 38), (20, 41), (24, 47)])
    c.poly('coat', [(47, 47), (47, 43), (41, 40), (34, 38), (30, 41), (27, 47)])
    c.poly('lining', [(14, 38), (17, 38), (23, 47), (19, 47)])
    c.poly('lining', [(35, 38), (32, 38), (27, 47), (31, 47)])
    c.poly('ivory', [(19, 39), (31, 39), (28, 47), (22, 47)])

    # --- light from upper left ---------------------------------------------------------------------
    for n in ('neck', 'coat', 'lining', 'ivory', 'ear'):
        c.shade(n)
    c.shade('skin', hi_depth=1, sh_depth=2)
    for i in range(6):
        c.shade('hair%d' % i, hi_depth=0, sh_depth=2)

    # --- lines: silhouette black, clump creases in the deepest hair tone, materials meet in black --------
    pairs = []
    order = ['hair0', 'hair4', 'hair3', 'hair2', 'hair1']          # back to front
    for a in range(len(order)):
        for b in range(a + 1, len(order)):
            pairs.append((order[a], order[b], HD))                  # the tucked-under clump carries the crease
    for i in range(6):
        pairs += [('hair%d' % i, 'skin', K), ('hair%d' % i, 'ear', K)]
    pairs += [('skin', 'neck', hx(SK[3])), ('ear', 'skin', hx(SK[3])), ('neck', 'ivory', K), ('coat', 'lining', K),
              ('lining', 'ivory', K), ('coat', 'neck', K), ('coat', 'ivory', K), ('neck', 'hair5', K)]
    c.outline(K, between=pairs)
    # drop lone pixels (fewer than 2 figure neighbours): they read as dirt at 1x
    lone = [(x, y) for y in range(48) for x in range(48) if c.mat[y][x] and
            sum(1 for dx in (-1, 0, 1) for dy in (-1, 0, 1) if (dx or dy) and c.inside(x + dx, y + dy)) < 2]
    c.clear(lone)

    # --- form shading by hand: cast shadows and planes ------------------------------------------------
    s1, s2, s3 = hx(SK[2]), hx(SK[3]), hx(SK[0])
    c.paint([(x, y) for y in range(35, 40) for x in range(17, 33) if c.mat[y][x] == 'neck'], s1)   # under the jaw
    c.paint([(x, 14) for x in range(18, 36) if c.mat[14][x] == 'skin'], s1)                         # hairline shadow
    hair_detail(c)
    costume(c)
    features(c, expr)
    return c


def costume(c):
    """plum velvet + silver satin lapels + ivory silk cravat; the rose is the one accent."""
    I = {'K': K, 'I': hx(IVORY[0]), 'i': hx(IVORY[1]), 'j': hx(IVORY[2]), 'J': hx(IVORY[3]),
         'X': ROSE[1], 'Y': ROSE[0], 'x': ROSE[2], 'z': ROSE[3], 'G': LEAF[0], 'g': LEAF[1],
         'P': hx(COAT[1]), 'p': hx(COAT[2]), 'q': hx(COAT[3]), 'Q': hx(COAT[0])}
    # cravat: a knot under the jaw, then a puffed fold with two creases
    c.stamp(21, 39, ['.jiiiiiij',
                     '..jIIij..',
                     '..KjijK..',
                     '..iIiiij.',
                     '.iIiijiij',
                     '.iIiijiij',
                     'iiIiijiij',
                     'iiiijjiij',
                     'iiiijjijj'], I)
    # coat: a fold line on each shoulder, velvet sheen on the near shoulder
    c.paint([(5, 45), (6, 44), (7, 43)], hx(COAT[3]))
    c.paint([(41, 44), (42, 45), (43, 46)], hx(COAT[3]))
    c.paint([(3, 44), (4, 43), (5, 42), (8, 41), (9, 41)], hx(COAT[0]))
    # the rose on the near lapel
    c.stamp(8, 40, ['  KKK  ',
                    ' KYXxK ',
                    'KYXzXxK',
                    'KXxXxzK',
                    ' KxxzKg',
                    '  KKKgG',
                    '     gK'], I)


def hair_detail(c):
    """creases split the crest; one crisp highlight arc per clump, broken where the clump turns;
    the deepest shade only where a clump tucks under the next (occlusion)."""
    W, N, D = hx(HAIR[0]), hx(HAIR[3]), HD
    c.paint([(28, 10), (29, 9), (30, 8), (31, 7), (32, 6), (33, 5)], D)                        # crest split
    arcs = [(22, 3), (21, 3), (20, 3), (19, 3), (18, 3), (17, 4), (16, 4), (15, 4), (12, 5), (11, 6), (10, 6),
            (7, 8), (6, 9),                                                                          # crown
            (20, 9), (19, 9), (18, 9), (17, 10), (16, 10), (15, 10), (12, 12), (11, 13), (10, 13), (7, 16), (6, 17),
            (13, 17), (12, 18), (11, 19), (9, 22), (8, 23),                                          # over the ear
            (32, 3), (33, 3), (34, 3), (35, 3), (36, 4), (37, 4), (38, 5),                           # crest, front lock
            (27, 4), (26, 5), (25, 6), (24, 7), (24, 8)]                                             # crest, back lock
    c.paint([(x, y) for (x, y) in arcs if (c.mat[y][x] or '').startswith('hair')], W) if ARCS else None
    occ = []
    for y in range(47):
        for x in range(47):
            if (c.mat[y][x] or '').startswith('hair') and c.col[y][x] == hx(HAIR[2]) and c.col[y + 1][x] in (D, K):
                occ.append((x, y))
    c.paint(occ, N)


def features(c, expr):
    L = {'K': K, 'B': BROW, 'b': BROW2, 'E': EYE_W, 'A': IRIS, 'a': IRIS_D, 'W': HL, 's': hx(SK[2]), 'd': hx(SK[3]),
         'h': hx(SK[0]), 'm': STACHE, 'n': STACHE2, 'R': LIP_D, 'r': LIP, 'o': MOUTH_IN, 't': TONGUE, 'T': TEETH}
    up = {'knowing': 0, 'laugh': 1, 'surprised': 2}[expr]          # how far the brows lift
    # brows: near one level and heavy, far one arched high (the vain, knowing look)
    c.stamp(16, 18 - up, ['   bBBBB',
                          'bBBBBBB '], L)
    c.stamp(29, 16 - min(up, 1), ['   BBB  ',
                                  ' BBBBBBb',
                                  'B      B'], L)
    if expr == 'knowing':
        # hooded (lid crease), 3-px opening, iris looking toward the text box (screen right)
        c.stamp(16, 20, [' ssssss ', 'KKKKKKKK', 'KEEEaWEs', ' EEEAAE ', '  EEAas ', '  sssss '], L)
        c.stamp(30, 20, [' ssss  ', 'KKKKKKK', ' EEaWK', ' EEAAK', '  EAa ', '  sss '], L)
    elif expr == 'laugh':
        # eyes squeezed shut into arcs; cheeks push up (shadow under the arc)
        c.stamp(16, 20, ['  KKKK  ', ' K    K ', 'K      K', ' ssssss ', '        '], L)
        c.stamp(30, 20, ['  KKK  ', ' K   K ', 'K     K', ' sssss ', '       '], L)
    else:
        # surprised: lids lift, white shows all round the iris, brows high
        c.stamp(16, 19, ['KKKKKKKK', 'KEEaaWEK', 'KEEAAAE ', ' EEAAaE ', '  EEEE  ', '  ssss  '], L)
        c.stamp(30, 19, ['KKKKKKK', ' EaaWEK', ' EAAAEK', ' EAAaE ', '  EEE  ', '  sss  '], L)
    # nose: one shadow line down the far side of the bridge, a dark underside
    c.stamp(28, 25, ['s  ', 's  ', '.s ', '.s ', '..d', 'sdd'], L)
    if expr == 'knowing':
        # pencil moustache: one crisp line, philtrum gap, tips lifted
        c.stamp(23, 32, ['m    nn.n m', '.mmmmm.mmm '], L)
        # knowing smile: far corner lifted, lower lip = a skin-shadow dash, smile creases
        c.stamp(22, 34, ['s          R ', 's.R       R  ', '...RRRRRRR   ', '.....sss     '], L)
    elif expr == 'laugh':
        # the laugh that fills rooms: moustache rides up, a wide D-shaped mouth:
        # dark outline, one row of teeth under the top lip, dark interior, tongue at the bottom
        c.stamp(23, 31, ['m    nn.n m', '.mmmmm.mmm '], L)
        c.stamp(22, 33, ['s.KKKKKKKKKK',
                         's.KTTTTTTTTK',
                         '...KooooooK ',
                         '....KottoK  ',
                         '.....KKKK   ',
                         '.....sss    '], L)
    else:
        # surprised: a small upright oval, dark inside (never a red dot), moustache unchanged
        c.stamp(23, 32, ['m    nn.n m', '.mmmmm.mmm '], L)
        c.stamp(26, 34, ['.KKK.', 'KoooK', 'KotoK', '.KKK.', '.sss.'], L)
    c.stamp(27, 40, ['s'], L)                                                           # chin cleft
    c.paint([(17, 16), (18, 16), (19, 16), (18, 17)], hx(SK[0]))                        # forehead catches the light
    c.paint([(27, 26), (27, 27)], hx(SK[0]))                                            # nose bridge
    c.paint([(17, 30), (18, 31), (19, 32)], hx(SK[2]))                                  # under the cheekbone
    c.stamp(11, 24, ['d', 'ds', '.s'], L)                                              # inner ear


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for e in ('knowing', 'laugh', 'surprised'):
        im = build(e).image()
        suf = '' if e == 'knowing' else '_' + e
        im.save(OUT + '/DORIAN_st%s_48.png' % suf)
        im.resize((96, 96), 0).save(OUT + '/DORIAN_st%s.png' % suf)
    print('ok')


# ---- silhouette exploration (guide 2.1): same head and shoulders, five hair/headwear ideas, filled black ----
HEAD = [(15, 17), (19, 14), (26, 13), (32, 13), (36, 15), (37, 18), (38, 22), (38, 26), (37, 29), (36, 32), (34, 35),
        (32, 38), (29, 41), (25, 42), (22, 41), (19, 38), (17, 35), (15, 31), (14, 26), (14, 21)]
EAR = [(14, 22), (11, 21), (10, 23), (10, 28), (11, 30), (13, 31), (14, 30)]
BODY = [[(18, 34), (31, 36), (32, 46), (17, 46)], [(0, 47), (0, 43), (7, 40), (15, 38), (20, 41), (24, 47)],
        [(47, 47), (47, 43), (41, 40), (34, 38), (30, 41), (27, 47)], [(19, 39), (31, 39), (28, 47), (22, 47)]]
MANE = [(42, 6), (40, 3), (36, 1), (30, 0), (22, 0), (14, 1), (8, 4), (4, 8), (1, 13), (6, 14), (2, 21), (7, 21),
        (3, 28), (8, 27), (11, 29), (13, 26), (13, 21), (15, 17), (20, 13), (27, 12), (35, 14), (37, 18), (38, 15),
        (38, 9), (39, 6)]
SKULL = [(13, 24), (13, 12), (20, 8), (30, 8), (37, 12), (37, 18), (15, 17)]
SIL = {
    'A mane (chosen)': [MANE],
    'B slicked flat': [[(13, 24), (12, 13), (16, 7), (24, 4), (32, 5), (37, 8), (39, 14), (38, 18), (35, 14), (27, 12), (20, 13), (15, 17)]],
    'C top hat': [[(13, 24), (12, 13), (16, 8), (24, 6), (32, 7), (37, 10), (39, 15), (38, 18), (35, 14), (27, 12), (20, 13), (15, 17)],
                  [(9, 13), (41, 7), (42, 9), (10, 15)], [(15, 11), (13, 0), (33, 0), (36, 9)]],
    'D crest only': [[(13, 24), (12, 13), (17, 7), (22, 4), (25, 1), (33, 0), (40, 3), (42, 6), (39, 7), (39, 15), (37, 18), (35, 14), (27, 12), (20, 13), (15, 17)]],
    'E long mane': [[(42, 6), (40, 3), (34, 0), (22, 0), (12, 2), (6, 7), (3, 14), (2, 24), (3, 34), (6, 42), (11, 40), (13, 32), (15, 24), (15, 17), (20, 13), (27, 12), (35, 14), (37, 18), (38, 15), (38, 9), (39, 6)]],
}


def silhouette(kind):
    c = Canvas()
    for poly in SIL[kind] + [HEAD, EAR, SKULL] + BODY:
        c.poly('x', poly)
    c.ramp('x', '000000', '000000', '000000', '000000'); c.fill('x')
    return c.image()
