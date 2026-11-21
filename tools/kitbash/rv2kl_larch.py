"""Professor Imelda Larch - redo v2 (brief art/REDO_V2_BRIEF.md). Original construction, no donor pixels.
Concept: "the engineer who lit the region and now pours tea at the end of it". 56, wiry, gruff, guilty, kind, deadpan-funny.
Kept motifs: grey braid, glasses, field-scientist coat (pick A, sheet 20: mustard oilskin, slate, held-out mug of kelp tea).
Face kit (STYLE_GUIDE 2.3): J4 long jaw, E3 hooded eyes, B1 soft brows; crow's foot + nasolabial line; half-moon readers
perched low (she looks OVER them: the deadpan is built in).
python3 -I tools/kitbash/rv2kl_larch.py (lint); exports + sheet 29: python3 -I tools/kitbash/rv2kl_sheet29.py all"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rv2kl_lib import Canvas, hx, up, lint, G, lock_shade, zoom_sheet

OUTD = G + 'art/work/redo_v2/LARCH/'
K = hx('1e1418')                                   # outline: warm near-black
# ---- palette: 1 mustard oilskin / 2 slate knit / 3 silver-blue hair + accent coral (glasses, mug rim) --------------
SK = ('fbe4d0', 'f0c8a8', 'd29680', '9e5e56')      # skin: hi, base, shadow (rose), deep
HAIR = ('f4f7fc', 'c8d1e0', '98a4be', '6c7698')     # silver with blue-grey shadows (Dorian's is lavender)
HD = hx('474e6c')                                  # hair crease
OIL = ('f8d468', 'dea83c', 'b0782a', '784a22')      # mustard oilskin: hi, base, shadow (toward orange), deep
KNIT = ('8ca8be', '5e7c98', '425c7e', '2e3e5c')     # slate knit
CORAL = ('ff8c78', 'e8584a', 'b03a3c')              # accent: half-moon readers (and the mug rim on the front)
EYE_W, IRIS_D, IRIS, HL = hx('f8f4f0'), hx('1f5a5a'), hx('4fa294'), hx('ffffff')   # sea-glass eyes
BROW = hx('6e7898')
LIP_D = hx('93424a'); MOUTH_IN = hx('4a1424'); TEETH = hx('fbf6f2'); TONGUE = hx('c4545e')
TEAR, TEAR_D = hx('e8f6ff'), hx('9ac4ec')
BLUSH = hx('e8807a'); CHAIN = hx('d8dfea')

HL_ORDER = ['hA', 'hW', 'hL', 'hR', 'hF']
PLAITS = [(8, 31, 14, 36), (7, 35, 13, 40), (6, 39, 12, 44), (4, 43, 10, 48)]   # braid plaits (ellipse boxes), top to bottom


def portrait_base():
    c = Canvas()
    for n in ('skin', 'ear', 'neck'): c.ramp(n, *SK)
    c.ramp('coat', *OIL); c.ramp('colN', *OIL); c.ramp('colF', *OIL); c.ramp('knit', *KNIT); c.ramp('roll', *KNIT)
    for i in range(len(PLAITS)): c.ramp('pl%d' % i, *HAIR)
    # ---- back to front ----
    c.poly('coat', [(0, 47), (0, 40), (8, 37), (16, 38), (20, 47)])
    c.poly('coat', [(47, 47), (47, 40), (40, 37), (32, 38), (29, 47)])
    c.poly('neck', [(19, 33), (30, 33), (30, 44), (19, 44)])
    c.poly('knit', [(17, 44), (32, 44), (31, 47), (18, 47)])
    # hair: silhouette (back lock) first; flyaway wisps break the dome
    c.poly('hA', [(10, 14), (11, 9), (13, 6), (16, 4), (19, 3), (21, 1), (24, 0), (24, 2), (26, 2), (33, 3), (37, 5), (40, 10),
                  (41, 16), (40, 22), (38, 27), (37, 20), (36, 16), (33, 14), (27, 13), (22, 13), (17, 14), (14, 18),
                  (13, 21), (12, 26), (11, 31), (9, 29), (9, 20)])
    c.poly('ear', [(14, 22), (11, 21), (10, 23), (10, 28), (11, 30), (14, 31)])
    c.poly('skin', [(15, 15), (22, 13), (30, 13), (35, 15), (37, 19), (37, 25), (36, 30), (35, 34), (33, 37), (30, 40),
                    (27, 42), (24, 42), (21, 40), (18, 37), (16, 33), (15, 29), (14, 24), (14, 19)])
    # near side: two locks swept back over the ear toward the braid
    c.poly('hL', [(10, 14), (11, 9), (13, 6), (16, 4), (19, 3), (21, 1), (24, 0), (24, 3), (23, 6), (19, 9), (16, 12),
                  (14, 16), (13, 20), (12, 25), (11, 28), (10, 24), (10, 18)])
    # far side: two locks from the parting, the lower one covering the far temple
    c.poly('hR', [(24, 3), (26, 2), (33, 3), (37, 5), (40, 10), (41, 16), (40, 22), (38, 27), (37, 20), (36, 16), (33, 14),
                  (28, 13), (24, 12), (22, 10), (23, 6)])
    c.poly('hF', [(25, 3), (23, 7), (21, 10), (19, 13), (17, 14), (15, 17), (14, 20), (14, 16), (16, 12), (19, 8), (22, 4)])
    c.poly('hW', [(37, 16), (39, 20), (39, 25), (38, 30), (37, 32), (37, 26), (36, 21)])                   # loose far strand
    # coat collar (wide, oilskin), roll-neck knit
    c.poly('roll', [(17, 40), (20, 38), (25, 39), (30, 38), (33, 40), (32, 45), (25, 46), (17, 45)])
    c.poly('colN', [(0, 47), (0, 41), (5, 38), (11, 36), (16, 37), (19, 41), (21, 47)])
    c.poly('colF', [(47, 47), (47, 41), (42, 38), (36, 36), (32, 38), (30, 42), (28, 47)])
    # braid over the near shoulder: overlapping plaits, top to bottom (each in front of the one above)
    for i, b in enumerate(PLAITS):
        c.ellipse('pl%d' % i, b)

    for n in ('coat', 'colN', 'colF', 'knit', 'roll', 'ear', 'neck'):
        c.shade(n)
    for i in range(len(PLAITS)):
        c.shade('pl%d' % i, hi_depth=1, sh_depth=1)
    c.shade('skin', hi_depth=1, sh_depth=2)
    lock_shade(c, HL_ORDER, HAIR, HD, HL_ORDER, right_band=('hR', 'hW'))
    pairs = []
    pls = ['pl%d' % i for i in range(len(PLAITS))]
    for n in HL_ORDER + pls:
        pairs += [(n, 'skin', K), (n, 'ear', K), (n, 'colN', K), (n, 'coat', K), (n, 'neck', K), (n, 'roll', K)]
    for i in range(len(pls) - 1):
        pairs.append((pls[i], pls[i + 1], HD))
    pairs += [('skin', 'neck', hx(SK[3])), ('ear', 'skin', hx(SK[3])), ('neck', 'roll', K), ('coat', 'colN', K),
              ('coat', 'colF', K), ('colN', 'roll', K), ('colF', 'roll', K), ('knit', 'roll', hx(KNIT[3])),
              ('colN', 'knit', K), ('colF', 'knit', K), ('pl0', 'hA', HD), ('pl0', 'hL', HD)]
    c.outline(K, between=pairs)
    c.drop_lone()
    s1 = hx(SK[2])
    c.ink([(x, y) for y in range(33, 39) for x in range(18, 32) if c.mat[y][x] == 'neck'], s1)
    c.ink([(x, y) for y in range(2, 47) for x in range(48) if c.mat[y][x] == 'skin' and (
        ((c.mat[y - 1][x] or '').startswith('h') and c.col[y - 1][x] != K) or
        (c.col[y - 1][x] == K and (c.mat[y - 2][x] or '').startswith('h')))], s1)
    W = hx(HAIR[0])
    arcs = {'hL': [(19, 4), (18, 4), (17, 5), (16, 5), (15, 6), (14, 7), (13, 8)],
            'hR': [(27, 4), (28, 4), (29, 4), (30, 5), (31, 5), (32, 6)],
            'hF': [(22, 6), (21, 7), (20, 8)], 'hW': [(38, 20), (38, 21)]}
    # lock divisions that run from the hairline back toward the braid (tapered, deep hair tone)
    c.ink([q for q in [(15, 10), (14, 11), (13, 12), (12, 13), (12, 14)] if c.mat[q[1]][q[0]] == 'hL'], HD)
    c.ink([q for q in [(33, 9), (34, 10), (35, 11), (36, 12)] if c.mat[q[1]][q[0]] == 'hR'], HD)
    c.ink([q for q in [(32, 8), (33, 8)] if c.mat[q[1]][q[0]] == 'hR'], hx(HAIR[3]))
    for n, pts in arcs.items():
        c.ink([p for p in pts if c.mat[p[1]][p[0]] == n and c.col[p[1]][p[0]] not in (HD, K)], W)
    return c


def L():
    return {'K': K, 'B': BROW, 'E': EYE_W, 'A': IRIS, 'a': IRIS_D, 'W': HL, 's': hx(SK[2]), 'd': hx(SK[3]),
            'h': hx(SK[0]), 'k': hx(SK[1]), 'R': LIP_D, 'o': MOUTH_IN, 't': TONGUE, 'T': TEETH, 'q': TEAR, 'Q': TEAR_D,
            'b': BLUSH, 'G': hx(CORAL[1]), 'g': hx(CORAL[2]), 'Y': hx(CORAL[0]), 'c': CHAIN, 'l': hx('bfe6ec')}


# ---- feature stamps: one base face; expressions move brows, lids, mouth, marks (and knock the readers askew) -------
NEAR, FAR = (16, 19), (29, 19)                        # eye boxes 8 / 7 wide, rows 19-24
EYES = {
    'open':  (['kkkkkkkk', '.sssss..', 'KKKKKKKK', 'KEEaaWEK', '.EEaAAE.', '..ssss..'],
              ['kkkkkkk', '.ssss..', 'KKKKKKK', 'KEaaWEK', '.EaAAE.', '..sss..']),
    'lid':   (['kkkkkkkk', 'kkkkkkkk', '.sssss..', 'KKKKKKKK', '.EEEaWE.', '..ssss..'],
              ['kkkkkkk', 'kkkkkkk', '.ssss..', 'KKKKKKK', '.EEaWE.', '..sss..']),
    'flat':  (['kkkkkkkk', 'kkkkkkkk', 'ssssssss', 'KKKKKKKK', '.EEaWEE.', '..ssss..'],
              ['kkkkkkk', 'kkkkkkk', 'sssssss', 'KKKKKKK', '.EaWEE.', '..sss..']),
    'laugh': (['kkkkkkkk', 'kkkkkkkk', '..KKKK..', '.K....K.', 'K......K', 'kkkkkkkk'],
              ['kkkkkkk', 'kkkkkkk', '..KKK..', '.K...K.', 'K.....K', 'kkkkkkk']),
    'wide':  (['kkkkkkkk', 'KKKKKKKK', 'KEEEEEEK', '.EEEaWE.', '.EEEaAE.', '..EEEE..'],
              ['kkkkkkk', 'KKKKKKK', 'KEEEEEK', '.EEaWE.', '.EEaAE.', '..EEE..']),
    'pin':   (['KKKKKKKK', 'KEEEEEEK', 'KEEEEEEK', '.EEEaEE.', '.EEEaEE.', '..EEEE..'],
              ['KKKKKKK', 'KEEEEEK', 'KEEEEEK', '.EEaEE.', '.EEaEE.', '..EEE..']),
    'down':  (['kkkkkkkk', 'kkkkkkkk', '.sssss..', 'KKKKKKKK', '.EEEEEE.', '..EaaW..'],
              ['kkkkkkk', 'kkkkkkk', '.ssss..', 'KKKKKKK', '.EEEEE.', '..aaW..']),
    'squeeze': (['kkkkkkkk', 'kkkkkkkk', 'KKK.....', '..KKKKKK', 'kkkkkkkk', 'kkkkkkkk'],
                ['kkkkkkk', 'kkkkkkk', '....KKK', 'KKKKK..', 'kkkkkkk', 'kkkkkkk']),
    'glare': (['kkkkkkkk', 'kkkkkkkk', 'KK......', '.KKKKKKK', '..EEaWK.', '..ssss..'],
              ['kkkkkkk', 'kkkkkkk', '.....KK', 'KKKKKK.', 'KEaWE..', '.sss...']),
    'away':  (['kkkkkkkk', 'kkkkkkkk', '.sssss..', 'KKKKKKKK', '.EEEEaWE', '..ssss..'],
              ['kkkkkkk', 'kkkkkkk', '.ssss..', 'KKKKKKK', '.EEEaW.', '..sss..']),
}
BROWS = {  # B1: one soft row (two only where the brow bends)
    'neutral': ((16, 17), ['kkkkkkk', '.BBBBBB', 'kkkkkkk'], (29, 17), ['kkkkkk', 'BBBBBB', 'kkkkkk']),
    'up':      ((16, 15), ['..BBBB.', '.B....B', 'kkkkkkk', 'kkkkkkk'], (29, 15), ['.BBBB.', 'B....B', 'kkkkkk', 'kkkkkk']),
    'lift':    ((16, 16), ['.BBBBBB', 'kkkkkkk', 'kkkkkkk'], (29, 16), ['BBBBBB', 'kkkkkk', 'kkkkkk']),
    'angry':   ((16, 16), ['BB.....', '..BBB..', '.....BB'], (29, 16), ['.....BB', '..BBB..', 'BB.....']),
    'sad':     ((16, 16), ['....BBB', 'BBBB...', 'kkkkkkk'], (29, 16), ['BBB....', '...BBBB', 'kkkkkkk']),
    'low':     ((16, 17), ['kkkkkkk', 'kkkkkkk', 'BBBBBBB'], (29, 17), ['kkkkkk', 'kkkkkk', 'BBBBBB']),
    'smug':    ((16, 17), ['kkkkkkk', 'kkkkkkk', 'BBBBBBB'], (29, 15), ['..BBB.', '.B...B', 'B.....', 'kkkkkk']),
}
MOUTHS = {  # origin (22, 33), 9 wide x 7 rows
    'neutral': ['kkkkkkkkk', 'kkkkkkkkk', '..RRRRR..', '.R.....R.', '...sss...', 'kkkkkkkkk', 'kkkkkkkkk'],
    'laugh':   ['kkkkkkkkk', 'KKKKKKKKK', 'KTTTTTTTK', '.KoooooK.', '..KotoK..', '...KKK...', 'kkkkkkkkk'],
    'shout':   ['kkkkkkkkk', '.KKKKKKK.', 'KTTTTTTTK', 'KoooooooK', '.KotttoK.', '..KKKKK..', 'kkkkkkkkk'],
    'flat':    ['kkkkkkkkk', 'kkkkkkkkk', '..RRRRR..', 'kkkkkkkkk', '...sss...', 'kkkkkkkkk', 'kkkkkkkkk'],
    'smirk':   ['kkkkkkkkk', '.......Rs', '..RRRRR..', 'kkkkkkkkk', '...sss...', 'kkkkkkkkk', 'kkkkkkkkk'],
    'down':    ['kkkkkkkkk', 'kkkkkkkkk', '...RRR...', '.RR...RR.', '...sss...', 'kkkkkkkkk', 'kkkkkkkkk'],
    'oval':    ['kkkkkkkkk', '...KKK...', '..KoooK..', '..KotoK..', '...KKK...', '...sss...', 'kkkkkkkkk'],
    'gape':    ['...KKK...', '..KoooK..', '.KoooooK.', '.KoooooK.', '.KotttK.', '..KKKKK..', '...sss...'],
    'panic':   ['kkkkkkkkk', '.KKKKKKK.', 'KTTTTTTTK', '.KoooooK.', '..KKKKK..', 'kkkkkkkkk', 'kkkkkkkkk'],
    'wobble':  ['kkkkkkkkk', 'kkkkkkkkk', '..RR.RR..', '.R..R..R.', '...sss...', 'kkkkkkkkk', 'kkkkkkkkk'],
    'fluster': ['kkkkkkkkk', 'kkkkkkkkk', '.R.RR.R..', '..R..R...', '...sss...', 'kkkkkkkkk', 'kkkkkkkkk'],
}
EXPR = {   # eyes, brows, mouth, marks, glasses offset (near dy, far dy)
    'neutral':   ('open', 'neutral', 'neutral', (), (0, 0)),
    'happy':     ('laugh', 'lift', 'laugh', (), (0, 0)),
    'angry':     ('glare', 'angry', 'shout', ('vein',), (0, 0)),
    'blush':     ('away', 'sad', 'fluster', ('blush',), (0, 0)),
    'crying':    ('squeeze', 'sad', 'wobble', ('stream',), (0, 0)),
    'deadpan':   ('flat', 'low', 'flat', (), (0, 0)),
    'panic':     ('pin', 'sad', 'panic', ('sweat',), (0, 0)),
    'sad':       ('down', 'sad', 'down', (), (0, 0)),
    'shocked':   ('pin', 'up', 'gape', (), (-2, -1)),
    'smug':      ('lid', 'smug', 'smirk', (), (0, 0)),
    'surprised': ('wide', 'up', 'oval', (), (0, 0)),
}


def clear_box(c, x0, y0, rows):
    sk = hx(SK[1])
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            x, y = x0 + i, y0 + j
            if ch == 'k' and c.mat[y][x] == 'skin': c.col[y][x] = sk


def put(c, x0, y0, rows, l):
    clear_box(c, x0, y0, rows)
    c.stamp(x0, y0, [r.replace('k', '.') for r in rows], l)


def glasses(c, l, dn=0, df=0):
    """reading glasses pushed up on her head (she forgets they're there): coral frames, lens = glass over hair."""
    c.stamp(14, 7 + dn, ['.GGGGGG.', 'GllllWlG', 'GllllllG', '.gggggg.'], l)
    c.stamp(25, 7 + df, ['.GGGGG.', 'GlllWlG', 'GlllllG', '.ggggg.'], l)
    c.stamp(22, 8 + min(dn, df), ['GGG'], l)
    c.stamp(11, 8 + dn, ['GGG'], l)
    c.stamp(32, 8 + df, ['GG'], l)


def features(c, expr):
    l = L()
    ek, bk, mk, marks, (dn, df) = EXPR[expr]
    en, ef = EYES[ek]
    put(c, NEAR[0], NEAR[1], en, l); put(c, FAR[0], FAR[1], ef, l)
    (nx, ny), nrows, (fx, fy), frows = BROWS[bk]
    put(c, nx, ny, nrows, l); put(c, fx, fy, frows, l)
    # nose: bridge line on the far side, dark underside (adult)
    c.stamp(28, 21, ['s', 's', '.', '.', '.', '.', '.', 's', '.s', 'dd'], l)
    c.stamp(26, 30, ['d'], l)
    put(c, 22, 33, MOUTHS[mk], l)
    c.stamp(32, 31, ['s', 's', '.s'], l)          # nasolabial line
    c.stamp(14, 21, ['s', 's'], l)                # crow's foot (near)
    if 'stream' in marks:                         # "I'm not crying. It's the tea." - two comic streams under the readers
        for x0 in (16, 34):
            c.stamp(x0, 23, ['qQ', 'qQ', 'qQ', 'qQ', 'qQ', 'qQ', 'qQ', 'qQ', 'qQ', 'qQ', '.q'], l)
    if 'blush' in marks:
        c.stamp(17, 29, ['b.b.b.b', '.b.b.b.'], l)
        c.stamp(32, 29, ['b.b.b', '.b.b.'], l)
    if 'sweat' in marks:
        c.stamp(36, 13, ['.K.', 'KqK', 'KQK', '.K.'], l)
        c.stamp(12, 16, ['.K', 'Kq', 'KQ', '.K'], l)
    glasses(c, l, dn, df)
    if 'vein' in marks:                           # anger mark on the far forehead
        c.stamp(31, 12, ['.G.G.', 'GG.GG', '.....', 'GG.GG', '.G.G.'], l)


def portrait(expr='neutral'):
    c = portrait_base()
    features(c, expr)
    return c


# =====================================================================================================================
# OVERWORLD: 128x192 sheet like JUNO.png (4x4 frames of 16x24 art, doubled). Rows: down, left, right, up.
# The readers on her head are the accent from every side; the braid reads over the shoulder from the front and side.
# =====================================================================================================================
OW_STAND = {
    'down': ['................', '................', '................', '.....KKKKKK.....', '....KHHWWHHK....', '...KHGlGKGlGKK..', '..KHHGGGHGGGHSK.', '..KHHHHHHMMMMSK.', '..KHHHMMMMMMMSK.', '..KHHKkkkkkKMSK.', '..KHKkkkkkkkKSK.', '..KHkkekkekkKSK.', '..KHkkekkekkKSK.', '..KHKkkkkkksKSK.', '.KHMKKkkkksKKSK.', '.KHSKoONNNNOpKK.', 'KoKHKoONNNNOppK.', 'KoKMKOOmNNNOpPK.', 'KOKSKOONNNmOppK.', 'KkKMKOONNNmOpkK.', '.KKKKOOONmOOppK.', '..KOOOpKKKOOppK.', '..KTTTKK.KTTTK..', '..KBBBK..KBBBK..'],
    'left': ['................', '................', '................', '.....KKKKKK.....', '...KKHHWWHHK....', '..KGlGKGlGHHK...', '.KHGGGHGGGHHMK..', '.KHHHHMHHHHMMSK.', '.KHHMMMHHHMMSSK.', '.KHKkkKMMMMSSDK.', 'KkkkkkKMMMSSSK..', 'KekkkkKMMSSSK...', '.KkkkkksKSSDK...', '.KkkkksKKMSK....', '..KKkkKonOMSK...', '..KoONnNOOMSK...', '..KoOONNOOSMK...', '..KoOONNOpMSK...', '..KOOmNNOpSK....', '..KkOONNOppK....', '..KOOONNOppK....', '..KOOpKKOppK....', '..KTTTKKKTTK....', '..KBBBK.KBBK....'],
    'up': ['................', '................', '................', '.....KKKKKK.....', '....KHHWWHHK....', '...KHGGGGGGGKK..', '..KHHHHHHHHHMSK.', '..KHHHHHMMMMMSK.', '..KHHHHMMMMMSSK.', '..KHHHMMMMMSSSK.', '..KHHMMMMMSSSDK.', '..KMHMMMMMSSSDK.', '..KKMSMMMSSDKK..', '...KKMMMSSDK....', '..KoOKSMSDKOpK..', '.KoOOKHMSKOOppK.', 'KoOOOOKMKOOOppK.', 'KoOOOOOSOOOOppK.', 'KOOOOOOOOOOOppK.', 'KkOOOOOOOOOOpkK.', '.KOOOOOOOOOppK..', '..KOOOOpOOOppK..', '..KTTTKK.KTTTK..', '..KBBBK..KBBBK..'],
}
OW_STEP = {   # replacement rows (from y=21) for the two step frames, after the 1-px drop
    'down': (['..KOOOpKKKOOppK.', '..KTTTKK.KKKKK..', '..KBBBK.........'],
             ['..KOOOpKKKOOppK.', '..KKKKK.KKTTTK..', '.........KBBBK..']),
    'left': (['..KOOpKKOppK....', '.KTTTKKKKTTK....', 'KBBBK....KBBK...'],
             ['..KOOpKKOppK....', '..KTTKKKTTK.....', '..KBBK.KBBK.....']),
    'up':   (['..KOOOOpOOOppK..', '..KTTTKK.KKKKK..', '..KBBBK.........'],
             ['..KOOOOpOOOppK..', '..KKKKK.KKTTTK..', '.........KBBBK..']),
}


def _ow_legend():
    return {'K': K, 'W': HAIR[0], 'H': HAIR[1], 'M': HAIR[2], 'S': HAIR[3], 'D': HD, 'G': CORAL[1], 'g': CORAL[2],
            'l': 'e4f0f6', 'k': SK[1], 's': SK[2], 'e': IRIS_D, 'o': OIL[0], 'O': OIL[1], 'p': OIL[2], 'P': OIL[3],
            'n': KNIT[0], 'N': KNIT[1], 'm': KNIT[2], 'T': KNIT[3], 'B': '1e2840'}


def ow_frames():
    from rv2kl_lib import ascii_img, mirror
    lg = _ow_legend(); out = {}
    for d in ('down', 'left', 'up'):
        st = OW_STAND[d]
        f0 = ascii_img(st, lg, 16, 24)
        steps = []
        for rep in OW_STEP[d]:
            r = ['.' * 16] + st[:21]
            r = r[:21] + rep
            steps.append(ascii_img(r, lg, 16, 24))
        out[d] = [f0, steps[0], f0, steps[1]]
    out['right'] = [mirror(f) for f in out['left']]
    return [out['down'], out['left'], out['right'], out['up']]


def overworld():
    from rv2kl_lib import charset
    return charset(ow_frames())


PORTRAIT_EXPRS = list(EXPR)


# =====================================================================================================================
# BATTLE FRONT (80x80 art, exported 160x160). 3/4 toward screen left. "Drink your tea": the mug held out to the player,
# other fist on her hip, braid over the shoulder, readers pushed up on her head, knee-length oilskin, rubber boots.
# =====================================================================================================================
TEA = ('7a8a3a', '4e5a22')
ENAMEL = ('ffffff', 'e8eef4', 'b8c4d6')
TROUS = ('5e7c98', '425c7e', '2e3e5c', '1e2840')
BOOT = ('6a7e96', '3e4e68', '2a3650', '1a2236')
FHEAD = [                                            # 16x16 head, facing screen left; readers pushed up on her head
    '.....KKKKKK.....',
    '...KKHHWWHHKK...',
    '..KHHWHHHHHMMK.K',
    '.KHGlGKGlGHMMSKK',
    'KHHGGGKGGGMMSSK.',
    'KHHHHMHHHMMMSDK.',
    'KHHHHMMHHHMMSSK.',
    'KHKKkkkkkKMMSDK.',
    'KKkBBkkBBkKMSSK.',
    '.KkKKkkKKKskKSK.',
    '.KkewkkkewskKMK.',
    '.Kkkkkksksk.KSK.',
    '..KkkkkkksK.KSK.',
    '..KkkRRRksK..KK.',
    '...KkkkssK......',
    '....KKKKK.......']


def _flegend():
    return {'K': K, 'W': HAIR[0], 'H': HAIR[1], 'M': HAIR[2], 'S': HAIR[3], 'D': HD, 'h': SK[0], 'k': SK[1],
            's': SK[2], 'd': SK[3], 'e': IRIS_D, 'w': 'ffffff', 'R': LIP_D, 'G': CORAL[1], 'g': CORAL[2], 'Y': CORAL[0],
            'l': 'e4f0f6', 'B': BROW, 'o': OIL[0], 'O': OIL[1], 'p': OIL[2], 'P': OIL[3], 'n': KNIT[0], 'N': KNIT[1],
            'm': KNIT[2], 't': TEA[0], 'T': TEA[1], 'E': ENAMEL[0], 'F': ENAMEL[1], 'f': ENAMEL[2], 'q': 'f4f8ff'}


def front():
    c = Canvas(80, 80)
    R = {'legB': TROUS, 'legF': TROUS, 'bootB': BOOT, 'bootF': BOOT, 'armF': OIL, 'coat': OIL, 'flapL': OIL,
         'flapR': OIL, 'knit': KNIT, 'roll': KNIT, 'armN': OIL, 'upN': OIL, 'neck': SK, 'handF': SK, 'handN': SK,
         'pocket': OIL, 'colL': OIL, 'colR': OIL, 'cuffB': BOOT, 'cuffF': BOOT}
    for n, r in R.items(): c.ramp(n, *r)
    # ---- back to front ----
    c.poly('legB', [(43, 44), (48, 44), (49, 60), (45, 60), (44, 52)])
    c.poly('legF', [(37, 44), (42, 44), (39, 52), (36, 59), (32, 58), (35, 51)])
    c.poly('bootB', [(44, 61), (49, 61), (49, 72), (52, 74), (52, 77), (44, 77)])
    c.poly('bootF', [(32, 60), (37, 61), (35, 72), (34, 77), (25, 77), (25, 75), (30, 72)])
    c.poly('cuffB', [(43, 59), (50, 59), (50, 62), (43, 62)])
    c.poly('cuffF', [(31, 58), (38, 59), (37, 62), (30, 61)])
    c.poly('armF', [(36, 22), (39, 24), (36, 29), (31, 33), (27, 35), (25, 32), (29, 28), (33, 24)])
    c.poly('coat', [(36, 20), (42, 19), (48, 20), (51, 22), (52, 30), (51, 38), (35, 38), (34, 30), (35, 23)])
    c.poly('flapL', [(35, 37), (40, 37), (40, 44), (39, 50), (38, 56), (30, 57), (32, 48), (34, 42)])
    c.poly('flapR', [(44, 37), (51, 37), (52, 44), (54, 50), (57, 56), (48, 57), (46, 50), (44, 44)])
    c.poly('knit', [(39, 21), (46, 21), (45, 30), (45, 43), (39, 43), (39, 30)])
    c.poly('roll', [(39, 18), (46, 18), (46, 21), (39, 21)])
    c.poly('colL', [(35, 20), (40, 21), (40, 27), (38, 33), (36, 28), (34, 24)])
    c.poly('colR', [(46, 20), (51, 21), (52, 24), (49, 28), (47, 33), (46, 27)])
    c.poly('pocket', [(46, 44), (52, 44), (52, 49), (46, 49)])
    c.poly('upN', [(49, 21), (52, 23), (56, 30), (55, 35), (52, 36), (51, 28)])
    c.poly('armN', [(53, 31), (56, 31), (55, 36), (50, 40), (47, 39), (49, 36), (52, 34)])
    c.poly('handN', [(46, 37), (49, 37), (49, 40), (46, 40)])
    c.poly('handF', [(24, 31), (27, 31), (27, 35), (24, 35)])
    for n in R:
        if c.where(n): c.shade(n, hi_depth=1, sh_depth=1)
    c.outline(K, between=[(a, b, K) for a in R for b in R if a < b])
    lg = {k: (hx(v) if isinstance(v, str) else v) for k, v in _flegend().items()}
    c.stamp(36, 3, FHEAD, lg)
    # braid over her right shoulder (screen left), plaits down the chest, tied off at the end
    c.stamp(33, 17, ['.KKK..',
                     'KHHMK.',
                     'KWHHSK',
                     'KHHSMK',
                     'KMSHMK',
                     'KWHHSK',
                     'KHHSMK',
                     'KMSHMK',
                     'KWHHSK',
                     'KHHSMK',
                     'KMSHMK',
                     'KWHHSK',
                     '.KMMK.',
                     '.KNmK.',
                     'KHHMK.',
                     'KHMSMK',
                     '.KKKK.'], lg)
    # the mug of kelp tea held out, enamel with a coral rim
    c.stamp(17, 21, ['.........',
                     '.........',
                     '.........',
                     '.........',
                     '.........',
                     '.KKKKKKK.',
                     'KYGGGGGYK',
                     'KETTtTTFKK',
                     'KEFFFFFfK.K',
                     'KEFFFFFfKKK',
                     'KEFFFFFfK..',
                     '.KFFFffK...',
                     '..KKKKK....'], lg)
    # fold lines and sheen on the oilskin
    P, o = hx(OIL[3]), hx(OIL[0])
    folds = [[(37, 44), (36, 50)], [(49, 42), (51, 49), (53, 55)], [(37, 29), (37, 33)], [(54, 32), (52, 35)],
             [(32, 31), (29, 33)]]
    for f in folds: c.ink([q for q in c.path_pts(f) if c.mat[q[1]][q[0]] in R and c.col[q[1]][q[0]] != K], P)
    sheen = [[(36, 21), (38, 20)], [(33, 46), (32, 52)], [(35, 25), (33, 27)]]
    for f in sheen: c.ink([q for q in c.path_pts(f) if c.mat[q[1]][q[0]] in R and c.col[q[1]][q[0]] != K], o)
    c.drop_lone()
    # steam off the tea (after the lone-pixel pass: two soft curls)
    c.stamp(19, 17, ['.q....', 'qq..q.', '.q.qq.', '.qq.q.', '..q.qq', '.qq..q'], lg)
    return c


# =====================================================================================================================
# SILHOUETTES (guide 2.1): 80-px fronts filled black. The chosen one is A.
# =====================================================================================================================
_HEAD = [(38, 4), (45, 3), (50, 6), (51, 12), (48, 18), (40, 18), (36, 12)]
_BODY = [(36, 20), (42, 19), (48, 20), (51, 22), (52, 30), (51, 38), (35, 38), (34, 30), (35, 23)]
_SKIRT = [[(35, 37), (51, 37), (52, 44), (54, 51), (56, 57), (31, 58), (33, 48), (34, 42)]]
_LEGS = [[(36, 54), (42, 54), (42, 77), (31, 77), (31, 75), (36, 72)], [(44, 54), (50, 54), (50, 72), (53, 75), (53, 77), (44, 77)]]
_MUG = [[(36, 22), (39, 24), (36, 29), (31, 33), (27, 35), (25, 32), (29, 28), (33, 24)], [(17, 25), (27, 25), (28, 33), (19, 34), (17, 30)],
        [(19, 20), (21, 20), (21, 24), (19, 24)], [(23, 19), (25, 19), (25, 24), (23, 24)]]
_HIP = [[(49, 21), (52, 23), (56, 30), (55, 35), (52, 36), (51, 28)], [(53, 31), (56, 31), (55, 36), (50, 40), (47, 39), (49, 36), (52, 34)]]
_BRAID = [[(34, 18), (38, 18), (38, 31), (36, 32), (34, 30)]]
_GLASS = [[(37, 7), (50, 7), (50, 9), (37, 9)]]
_HANG = [[(36, 22), (38, 24), (37, 40), (34, 42), (33, 30)], [(49, 21), (52, 23), (53, 40), (50, 42), (49, 30)]]
_CLIP = [[(36, 22), (38, 24), (36, 32), (30, 36), (28, 33), (33, 28)], [(24, 26), (32, 24), (34, 38), (26, 40)]]
_LABCOAT = [[(34, 20), (52, 20), (56, 66), (30, 66)]]
_STOLE = [[(36, 20), (28, 28), (18, 34), (16, 40), (22, 38), (32, 30)], [(48, 20), (56, 24), (60, 30), (54, 28)]]
_BUN = [[(42, 0), (49, 0), (50, 5), (42, 5)]]
_CANE = [[(56, 38), (58, 38), (58, 77), (56, 77)]]
SILS = [
    ('A (chosen)', [_BODY] + _SKIRT + _LEGS + _MUG + _HIP + _BRAID + _GLASS, 'mug held out + elbow out + braid: 4 breaks'),
    ('B', [_BODY] + _SKIRT + _LEGS + _HANG + _BRAID, 'arms down: a column; no story'),
    ('C', [_BODY] + _SKIRT + _LEGS + _CLIP + _HIP + _BRAID, 'clipboard: every scientist (design study 5)'),
    ('D', _LABCOAT + _LEGS + _MUG + _HIP + _BRAID, 'lab coat to the shin: Juniper/Colress read'),
    ('E', [_BODY] + _SKIRT + _LEGS + _MUG + _HIP + _STOLE, 'stole flying (sheet 20 pick A): reads as a scarf, crowds the mug'),
    ('F', [_BODY] + _SKIRT + _LEGS + _MUG + _HIP + _BUN, 'hair in a bun: loses the braid, grandma read'),
    ('G', [_BODY] + _SKIRT + _LEGS + _HANG + _CANE + _BRAID, 'cane: elderly, not wiry (Magnolia read)'),
]


def silhouette(i):
    name, polys, why = SILS[i]
    c = Canvas(80, 80); c.ramp('x', '000000', '000000', '000000', '000000')
    c.poly('x', _HEAD)
    for pg in polys: c.poly('x', pg)
    c.fill('x')
    return c.image()


if __name__ == '__main__':
    # lint only; exports and the review sheet: python3 -I tools/kitbash/rv2kl_sheet29.py all
    for e in PORTRAIT_EXPRS:
        print(e, lint(portrait(e).image())['colours'])
    print('front', lint(front().image()))
    print('overworld', lint(overworld())['colours'])
