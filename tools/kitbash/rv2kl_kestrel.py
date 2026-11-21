"""Kestrel Vane - redo v2 (brief art/REDO_V2_BRIEF.md). Original construction, no donor pixels.
Concept: "a boy holding his dead mother's coat closed against the wind". 16, lean, sharp, proud, guarded, a hint of grief.
Kept from the user's pick A2 (sheet 17): collar-up black greatcoat a size too big, crimson lining, side-swept navy fringe.
Face kit (STYLE_GUIDE 2.3): J2 sharp V jaw, E2 almond sharp eyes, B2 strong brows; under-eye line (he doesn't sleep).
python3 -I tools/kitbash/rv2kl_kestrel.py (lint); exports + sheet 29: python3 -I tools/kitbash/rv2kl_sheet29.py all"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rv2kl_lib import Canvas, hx, up, lint, G, lock_shade, denoise

OUTD = G + 'art/work/redo_v2/KESTREL/'
K = hx('140f1e')                                   # outline: near-black, cool violet tint
# ---- palette: 1 black greatcoat / 2 navy hair / 3 silver-grey shirt + accent crimson lining -----------------------
SK = ('fff0e2', 'f6d6c0', 'dca090', 'a8646a')      # skin: hi, base, shadow (rose), deep (rose-violet)
HAIR = ('8a9ad4', '4f5f9e', '36417a', '262c5a')     # navy: highlight (desaturated blue-violet), light, mid, shadow
HD = hx('181a3c')                                  # hair crease
COAT = ('5a5880', '3a3854', '282640', '18162a')     # black wool: sheen, base, shadow, deep (navy-plum, never grey)
CRIM = ('ec5a62', 'c02a3c', '861c34', '561226')     # crimson lining (the accent)
SHIRT = ('f4f4fa', 'd2d4e6', 'a2a4c4', '70709a')    # silver-grey shirt, lavender shadows
EYE_W, IRIS_D, IRIS, HL = hx('f4f2f6'), hx('2c3260'), hx('7282b8'), hx('ffffff')   # steel grey-blue eyes
BROW = hx('262c5a')
LIP_D = hx('8e3a48'); MOUTH_IN = hx('4a1424'); TEETH = hx('fbf6f2'); TONGUE = hx('c4545e')
TEAR, TEAR_D = hx('e8f4ff'), hx('9ac0e8')
BLUSH = hx('e88a8a')


HL_ORDER = ['hA', 'hE', 'hB1', 'hB2', 'hB3', 'hD']
# head shapes, designed on a 44-row head; T() scales them x1.1 into the portrait frame (crown y1, chin y43, 2 px air right)
HEAD = {
    'hA': [(13, 4), (19, 2), (31, 2), (32, 3), (33, 2), (37, 2), (39, 3), (41, 5), (42, 8), (42, 20), (41, 25), (40, 28),
           (39, 28), (38, 24), (38, 16), (37, 14), (33, 15), (29, 15), (27, 19), (26, 19), (25, 16), (22, 16), (19, 17),
           (16, 17), (15, 20), (14, 23), (13, 21), (12, 21), (11, 23), (11, 28), (10, 31), (9, 31), (8, 27), (6, 24),
           (2, 22), (5, 20), (6, 17), (1, 14), (4, 11), (6, 8), (9, 6)],
    'ear': [(15, 22), (12, 21), (11, 23), (11, 28), (12, 30), (15, 31)],
    'skin': [(16, 16), (24, 14), (33, 13), (37, 14), (38, 22), (37, 28), (36, 30), (31, 36), (28, 40), (25, 40), (19, 34),
             (16, 30), (15, 26), (15, 20)],
    'hE': [(33, 2), (37, 2), (39, 3), (41, 5), (42, 8), (42, 20), (41, 25), (40, 28), (39, 28), (38, 24), (38, 16), (37, 14),
           (37, 9), (35, 7), (34, 5), (32, 3)],                                                  # far lock
    'hB1': [(20, 2), (31, 2), (31, 4), (27, 6), (22, 8), (17, 10), (12, 12), (7, 14), (1, 14), (4, 11), (7, 8), (11, 5),
            (15, 3)],                                                                            # top lock -> back tip
    'hB2': [(31, 4), (34, 5), (35, 7), (30, 10), (25, 12), (20, 14), (16, 16), (13, 19), (12, 21), (11, 20), (11, 17),
            (13, 13), (17, 10), (22, 8), (27, 6)],                                               # middle lock, over the ear
    'hB3': [(35, 7), (37, 9), (37, 14), (33, 15), (29, 15), (25, 16), (22, 16), (19, 17), (16, 17), (15, 20), (14, 23),
            (13, 21), (13, 19), (16, 16), (20, 14), (25, 12), (30, 10)],                         # fringe lock -> near temple
    'hD': [(29, 11), (31, 12), (30, 14), (28, 17), (27, 19), (26, 19), (25, 16), (26, 13)],     # dip lock
}
ARCS = {'hB1': [(27, 4), (26, 4), (25, 5), (24, 5), (23, 6), (22, 6)],
        'hB2': [(30, 6), (29, 7), (28, 7), (27, 8), (26, 8)],
        'hB3': [(36, 10), (35, 11), (34, 11), (33, 12)],
        'hE': [(39, 6), (39, 7), (40, 8), (40, 9)],
        'hA': [(5, 19), (4, 20)],
        'hD': [(29, 12), (29, 13), (28, 14)]}


def T(pts, s=1.1):
    return [(27 + (x - 26) * s, 11.5 + (y - 11.5) * s) for x, y in pts]


def portrait_base():
    c = Canvas()
    c.ramp('skin', *SK); c.ramp('ear', *SK); c.ramp('neck', *SK)
    c.ramp('coat', *COAT); c.ramp('colN', *COAT); c.ramp('colF', *COAT); c.ramp('lining', *CRIM); c.ramp('shirt', *SHIRT)
    # ---- back to front ----
    c.poly('coat', [(0, 47), (0, 41), (6, 38), (13, 39), (18, 47)])
    c.poly('coat', [(47, 47), (47, 40), (42, 38), (36, 40), (31, 47)])
    c.poly('neck', [(22, 34), (31, 34), (31, 47), (22, 47)])
    c.poly('shirt', [(20, 44), (23, 42), (26, 46), (30, 42), (32, 44), (32, 47), (20, 47)])
    for n in ('hA', 'ear', 'skin', 'hE', 'hB1', 'hB2', 'hB3', 'hD'):
        c.poly(n, T(HEAD[n]))
    # collar: near side turned up behind the ear (outer face), far side up and flaring; crimson lining at the opening
    c.poly('colN', [(0, 47), (0, 41), (2, 35), (4, 30), (5, 27), (9, 27), (12, 30), (15, 35), (18, 41), (20, 47)])
    c.poly('lining', [(10, 28), (12, 30), (15, 35), (18, 41), (20, 47), (18, 47), (16, 42), (13, 36), (11, 31)])
    c.poly('colF', [(47, 47), (47, 33), (46, 27), (46, 24), (43, 25), (40, 28), (38, 32), (35, 38), (33, 42), (32, 47)])
    c.poly('lining', [(43, 25), (40, 28), (38, 32), (35, 38), (33, 42), (32, 47), (34, 47), (35, 43), (37, 39), (40, 34),
                      (42, 29), (45, 25)])

    for n in ('coat', 'colN', 'colF', 'lining', 'shirt', 'ear', 'neck'):
        c.shade(n)
    c.shade('skin', hi_depth=1, sh_depth=2)
    lock_shade(c, HL_ORDER, HAIR, HD, HL_ORDER, right_band=('hE',))
    pairs = []
    for n in HL_ORDER:
        pairs += [(n, 'skin', K), (n, 'ear', K), (n, 'colN', K)]
    pairs += [('skin', 'neck', hx(SK[3])), ('ear', 'skin', hx(SK[3])), ('neck', 'shirt', K), ('coat', 'colN', K),
              ('coat', 'colF', K), ('colF', 'lining', K), ('lining', 'shirt', K), ('colN', 'neck', K), ('colN', 'shirt', K),
              ('lining', 'neck', K), ('coat', 'shirt', K), ('neck', 'lining', K)]
    c.outline(K, between=pairs)
    c.drop_lone()
    s1 = hx(SK[2])
    c.ink([(x, y) for y in range(34, 40) for x in range(21, 32) if c.mat[y][x] == 'neck'], s1)       # under the jaw
    # hairline shadow: the fringe casts a 1-px band on the forehead and temple
    c.ink([(x, y) for y in range(2, 47) for x in range(48) if c.mat[y][x] == 'skin' and (
        ((c.mat[y - 1][x] or '').startswith('h') and c.col[y - 1][x] != K) or
        (c.col[y - 1][x] == K and (c.mat[y - 2][x] or '').startswith('h')))], s1)
    hair_detail(c)
    return c


def hair_detail(c):
    """one highlight arc per lock, on its lit (upper-left) third, following the flow."""
    W = hx(HAIR[0])
    for n, pts in ARCS.items():
        q = [(int(round(x)), int(round(y))) for x, y in T(pts)]
        c.ink([p for p in q if c.mat[p[1]][p[0]] == n and c.col[p[1]][p[0]] not in (HD, K)], W)


def L():
    return {'K': K, 'B': BROW, 'E': EYE_W, 'A': IRIS, 'a': IRIS_D, 'W': HL, 's': hx(SK[2]), 'd': hx(SK[3]),
            'h': hx(SK[0]), 'k': hx(SK[1]), 'R': LIP_D, 'o': MOUTH_IN, 't': TONGUE, 'T': TEETH, 'q': TEAR, 'Q': TEAR_D,
            'b': BLUSH}


# ---- feature stamps (STYLE_GUIDE 3.5 / 3.6 / 3.9): one base face; expressions move brows, lids and mouth ----------
NEAR, FAR = (15, 21), (30, 21)                       # eye boxes: near 10x8, far 9x8 (rows 21-28)
EYES = {   # (near rows, far rows), each 8 rows from y=21; 'k' = plain skin (clears the old lid)
    'open': (['kkkkkkkkkk', 'K.........', 'KKKKKKKKK.', '.KEEEaaWKK', '..EEEaaaE.', '...EEAAAE.', '....EAA...', '.....sss..'],
             ['kkkkkkkkk', '........K', '.KKKKKKKK', 'KKEaaWK..', '.EEaaaE..', '..EAAAE..', '...AA....', '...sss...']),
    'lid':  (['kkkkkkkkkk', 'kkkkkkkkkk', 'K.........', 'KKKKKKKKKK', '..EEEaaWE.', '...EEAAAE.', '....EAA...', '.....sss..'],
             ['kkkkkkkkk', 'kkkkkkkkk', '........K', 'KKKKKKKKK', '.EEaaWE..', '..EAAAE..', '...AA....', '...sss...']),
    'flat': (['kkkkkkkkkk', 'kkkkkkkkkk', '.sssssss..', 'KKKKKKKKKK', '..EEEaaWE.', '...EEAAAE.', '....EAA...', '.....sss..'],
             ['kkkkkkkkk', 'kkkkkkkkk', '..ssssss.', 'KKKKKKKKK', '.EEaaWE..', '..EAAAE..', '...AA....', '...sss...']),
    'soft': (['kkkkkkkkkk', 'K.........', 'KKKKKKKKK.', '.KEEEaaWKK', '..EEEaaaE.', '...ssAAss.', '....sss...', 'kkkkkkkkkk'],
             ['kkkkkkkkk', '........K', '.KKKKKKKK', 'KKEaaWK..', '.EEaaaE..', '..ssAAs..', '...sss...', 'kkkkkkkkk']),
    'down': (['kkkkkkkkkk', 'kkkkkkkkkk', 'K.........', 'KKKKKKKKKK', '..EEEEEEE.', '...EEaaWE.', '....EAA...', '.....sss..'],
             ['kkkkkkkkk', 'kkkkkkkkk', '........K', 'KKKKKKKKK', '.EEEEEE..', '..EaaWE..', '...AA....', '...sss...']),
    'wide': (['K.........', 'KKKKKKKKK.', '.KEEEEEEKK', '..EEEaaWE.', '..EEEAAAE.', '...EEAAE..', '....EEE...', '.....sss..'],
             ['........K', '.KKKKKKKK', 'KKEEEEK..', '.EEaaWE..', '.EEAAAE..', '..EAAE...', '...EE....', '...sss...']),
    'pin':  (['K.........', 'KKKKKKKKK.', '.KEEEEEEKK', '..EEEaWEE.', '..EEEaaEE.', '...EEEEE..', '....EEE...', '.....sss..'],
             ['........K', '.KKKKKKKK', 'KKEEEEK..', '.EEaWEE..', '.EEaaEE..', '..EEEE...', '...EE....', '...sss...']),
    'away': (['kkkkkkkkkk', 'kkkkkkkkkk', 'K.........', 'KKKKKKKKKK', '..EEEEaWa.', '...EEEAA..', '....EEE...', '.....sss..'],
             ['kkkkkkkkk', 'kkkkkkkkk', '........K', 'KKKKKKKKK', '.EEEaWa..', '..EEAAE..', '...EE....', '...sss...']),
}
BROWS = {  # (near origin, rows), (far origin, rows); B2 = 2 rows, thick at the inner end
    'neutral': ((16, 19), ['kkkkkkkk', 'BBBBBBB.', '....BBBB'], (30, 19), ['kkkkkkkk', '.BBBBBBB', 'BBBB....']),
    'up':      ((16, 19), ['BBBBBBB.', '....BBBB', 'kkkkkkkk'], (30, 19), ['.BBBBBBB', 'BBBB....', 'kkkkkkkk']),
    'arch':    ((16, 19), ['.BBBBBB.', 'BB....BB', 'kkkkkkkk'], (30, 19), ['.BBBBBB.', 'BB....BB', 'kkkkkkkk']),
    'sad':     ((16, 19), ['....BBBB', 'BBBBBB..', 'kkkkkkkk'], (30, 19), ['BBBB....', '..BBBBBB', 'kkkkkkkk']),
    'angry':   ((16, 19), ['BB......', '.BBBBB..', '....BBBB'], (30, 19), ['......BB', '..BBBBB.', 'BBBB....']),
    'flat':    ((16, 19), ['kkkkkkkk', 'BBBBBBBB', '.....BBB'], (30, 19), ['kkkkkkkk', 'BBBBBBBB', 'BBB.....']),
    'smug':    ((16, 19), ['kkkkkkkk', 'BBBBBBBB', '.....BBB'], (30, 18), ['...BBBB.', '.BBB..BB', 'BB......', 'kkkkkkkk']),
}
MOUTHS = {  # origin (25, 33), 8 wide x 6 rows; 'k' clears
    'neutral':  ['kkkkkkkk', 'kkkkkkkk', '.RRRRR.k', '......Rk', '..sss..k', 'kkkkkkkk'],
    'smile':    ['kkkkkkkk', '.R....Rk', '..RRRR.k', 'kkkkkkkk', '...sss.k', 'kkkkkkkk'],
    'smirk':    ['kkkkkkkk', '......Rs', '.RRRRR.k', 'kkkkkkkk', '..sss..k', 'kkkkkkkk'],
    'flat':     ['kkkkkkkk', 'kkkkkkkk', '..RRRR.k', 'kkkkkkkk', '..sss..k', 'kkkkkkkk'],
    'down':     ['kkkkkkkk', 'kkkkkkkk', '..RRRR.k', '.R....Rk', '..sss..k', 'kkkkkkkk'],
    'grit':     ['kkkkkkkk', 'KKKKKKKk', 'KTTTTTKk', 'KoooooKk', 'KTTTTTKk', '.KKKKK.k'],
    'oval':     ['kkkkkkkk', '..KKK..k', '.KoooK.k', '.KotoK.k', '..KKK..k', '..sss..k'],
    'shout':    ['kkkkkkkk', 'KKKKKKKk', 'KTTTTTKk', 'KoooooKk', '.KtttK.k', '..KKK..k'],
    'pout':     ['kkkkkkkk', 'kkkkkkkk', '..RRR..k', '.R...R.k', '..sss..k', 'kkkkkkkk'],
    'tight':    ['kkkkkkkk', 'kkkkkkkk', '.RRRRR.k', 'R.....Rk', '..sss..k', 'kkkkkkkk'],
}
EXPR = {   # eyes, brows, mouth, marks
    'neutral':   ('open', 'neutral', 'neutral', ()),
    'happy':     ('soft', 'up', 'smile', ()),
    'sad':       ('down', 'sad', 'down', ()),
    'angry':     ('lid', 'angry', 'grit', ()),
    'surprised': ('wide', 'arch', 'oval', ()),
    'smug':      ('lid', 'smug', 'smirk', ()),
    'deadpan':   ('flat', 'flat', 'flat', ()),
    'panic':     ('pin', 'sad', 'shout', ('sweat',)),
    'blush':     ('away', 'neutral', 'pout', ('blush',)),
    'crying':    ('down', 'sad', 'tight', ('tear',)),
}
ALIASES = {'shocked': 'surprised'}


def clear_box(c, x0, y0, rows):
    """stamp helper: 'k' -> the base skin tone, but only on skin (never over hair or outline)."""
    sk = hx(SK[1])
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            x, y = x0 + i, y0 + j
            if ch == 'k' and c.mat[y][x] == 'skin': c.col[y][x] = sk


def put(c, x0, y0, rows, l):
    clear_box(c, x0, y0, rows)
    c.stamp(x0, y0, [r.replace('k', '.') for r in rows], l)


def features(c, expr):
    l = L()
    ek, bk, mk, marks = EXPR[expr]
    (nx, ny), nrows, (fx, fy), frows = BROWS[bk]
    en, ef = EYES[ek]
    put(c, NEAR[0], NEAR[1], en, l); put(c, FAR[0], FAR[1], ef, l)
    put(c, nx, ny, nrows, l); put(c, fx, fy, frows, l)
    # nose: shadow down the far side of the tip, dark underside
    c.stamp(32, 29, ['s', 's'], l)
    c.stamp(31, 31, ['dd'], l)
    put(c, 25, 33, MOUTHS[mk], l)
    if 'sweat' in marks:
        c.stamp(37, 15, ['.K.', 'KqK', 'KQK', '.K.'], l)
    if 'blush' in marks:
        c.stamp(17, 30, ['.b.b.b', 'b.b.b.'], l)
        c.stamp(33, 30, ['.b.b', 'b.b.'], l)
    if 'tear' in marks:
        c.stamp(19, 28, ['qqQq'], l)
        c.stamp(20, 29, ['q', 'Q', 'q'], l)


def portrait(expr='neutral'):
    c = portrait_base()
    features(c, expr)
    return c


# =====================================================================================================================
# OVERWORLD: 128x192 sheet like JUNO.png (4 frames x 4 directions, 16x24 art doubled). Rows: down, left, right, up.
# Frames: stand, step, stand, step; step frames sit 1 px lower (Juno's convention) with the hem and boots swapped.
# Hook at 16 px: the collar tips stick out past the jaw on both sides; crimson shows from all four directions
# (collar opening front/side, collar tips and the split tail at the back).
# =====================================================================================================================
OW_STAND = {
    'down': ['................', '................', '................', '.....KKKKKK.....', '....KHHWWHHKK...', '...KHHWHHHHMSK..', '..KHHHHHHHMMSSK.', '..KHHHHHMMMSSSK.', '.KHHHHMMMMDSSK..', '.KMMMMMMMKkKSSK.', '.KMKMMKkkkkkKSK.', '.KMKkkkkkkkkKSK.', 'KVKKkekkkekkKKVK', 'KCrKkekkekkKKrCK', 'KCVrKkkkkkKrrVCK', 'KcCVrKssKKrVCCvK', 'KcCCCVKjjKVCCCvK', 'KcCKCCVjjVCCKCvK', 'KcCKCCCVVCCCKCvK', '.KkKCCCCVCCCKsK.', '..KCCCxVVxCCCK..', '..KCCxKTTKxCCK..', '..KVVKKBBKKVVK..', '...KK.KKKK.KK...'],
    'left': ['................', '................', '................', '......KKKKK.....', '....KKHWWHHKK...', '...KHHWHHHHHMK..', '..KHHHHHHHHMMSKK', '.KHHHHHHHMMMSSSK', '.KMHHHHMMMMDSSK.', 'KMMKMHMMMMMSDSSK', 'KMKkKMMMMMDSSSK.', '.KkkkKMMMMSSSSKK', '.KekkkKMMMSSSK..', '.KekkksKrVVVVK..', '.KkkkksKrVCCVK..', '..KKssKrVCCCvK..', '..KjjKrCCCCCvK..', '..KjKCCCCCCCvK..', '..KKCCCCKCCvvK..', '..KkCCCCKCCvvK..', '..KCCCCCKCvvxK..', '..KCCCCCKvvxrK..', '..KVVKKKKKVVKK..', '...KKK...KKK....'],
    'up': ['................', '................', '................', '.....KKKKKK.....', '....KHHWWHHK....', '...KHHWHHHHHKK..', '..KHHHHHHHHMSSK.', '..KHHHHHHHMMSK..', '.KHHHHHHHMMMSSK.', '.KMHHHHHMMMMSSK.', '.KMMHHHMMMMSSSK.', '.KSMMMMMMMSSSDK.', 'KVKSMMMMMSSSDKVK', 'KCrKSSKSKSSDKrCK', 'KCVKVVKSKVVKVVCK', 'KcCVVVVKVVVVVCvK', 'KcCCCCCCCCCCCCvK', 'KcCKCCCCCCCCKCvK', 'KcCKCCCCVCCCKCvK', '.KkKCCCCVCCCKsK.', '..KCCCCVxVCCCK..', '..KCCCVxrxVCCK..', '..KVVKKBBKKVVK..', '...KK.KKKK.KK...'],
}
OW_STEP = {   # replacement rows (from y=21) for the two step frames, after the 1-px drop
    'down': (['..KCCCxVVxCCCK..', '..KCCxKTKVVVK...', '..KVBBKK.KKK....'],
             ['..KCCCxVVxCCCK..', '...KVVVKTKxCCK..', '....KKK.KKBBVK..']),
    'left': (['..KCCCCCKvvxrK..', '.KKVVKKKKKVVKK..', 'KBBK.....KBBK...'],
             ['..KCCCCCKvvxrK..', '..KVVKKKKKVVKK..', '...KBBK.KBBK....']),
    'up':   (['..KCCCCVxVCCCK..', '..KCCVKxKVVVK...', '..KVBBKK.KKK....'],
             ['..KCCCCVxVCCCK..', '...KVVVKxKVCCK..', '....KKK.KKBBVK..']),
}


def _ow_legend():
    return {'K': K, 'W': HAIR[0], 'H': HAIR[1], 'M': HAIR[2], 'S': HAIR[3], 'D': HD, 'k': SK[1], 's': SK[2],
            'e': IRIS_D, 'c': COAT[0], 'C': COAT[1], 'v': COAT[2], 'V': COAT[3], 'r': CRIM[1], 'x': CRIM[2],
            'j': SHIRT[1], 'T': HAIR[3], 'B': COAT[3]}


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
# BATTLE FRONT (80x80 art, exported 160x160 like RIVAL_JUNO.png). 3/4 toward screen left (the player's side).
# Original construction: designed polygons -> ramps -> explicit fold lines -> hand stamps (head, Honedge, buckle).
# Pose: weight on the back leg, coat tail flaring behind; his right sleeve hides the hand that holds Honedge, blade
# down; his left hand at the sternum holding the too-big coat closed (his tic). Collar up, crimson at every opening.
# =====================================================================================================================
GOLD = ('f8e08a', 'd8a840', '8e6224')
HONE_EYE = 'a8e4f8'
TROUS = ('4f5f9e', '36417a', '262c5a', '181a3c')    # trousers: navy family
BOOT = ('5a5880', '3a3854', '282640', '18162a')
FHEAD = [                                            # 19x18 head, facing screen left; part on his left (screen right)
    '......KKKKK........',
    '....KKHHWWHKK......',
    '...KHHHWHHHHHKK....',
    '..KHHHWHHHHHMMSKK..',
    '.KHHHHHHHHHMMMSSSKK',
    '.KHHHHHHHHMMMSSDKK.',
    'KMHHHHHHMMMMSSDSSSK',
    'KMMHHMMMMKKSMSSDKK.',
    'KMKMMMKKKkkKMSSSSK.',
    '.KKMMKkkkkkkKMSDK..',
    '.KKKKkkkKKKKsKSSK..',
    '..KkeekkkeeksKKK...',
    '..Kkewkkkewks......',
    '..Kkkkkkkkkss......',
    '..KkkRRkkkksK......',
    '...KkkkkkksK.......',
    '....KkkssK.........',
    '.....KKKK..........']


def _legend():
    return {'K': K, 'W': HAIR[0], 'H': HAIR[1], 'M': HAIR[2], 'S': HAIR[3], 'D': HD, 'h': SK[0], 'k': SK[1], 's': SK[2],
            'd': SK[3], 'e': IRIS_D, 'w': 'ffffff', 'R': LIP_D, 'c': COAT[0], 'C': COAT[1], 'v': COAT[2], 'V': COAT[3],
            'r': CRIM[1], 'x': CRIM[2], 'X': CRIM[3], 'Q': CRIM[0], 'g': GOLD[0], 'G': GOLD[1], 'O': GOLD[2],
            'i': SHIRT[0], 'j': SHIRT[1], 'l': SHIRT[2], 'L': SHIRT[3], 'y': HONE_EYE, 'b': HAIR[1], 'B': HAIR[2],
            'n': HAIR[3]}


def front():
    c = Canvas(80, 80)
    R = {'tail': COAT, 'tlin': CRIM, 'legB': TROUS, 'legF': TROUS, 'bootB': BOOT, 'bootF': BOOT, 'armF': COAT,
         'coat': COAT, 'flapL': COAT, 'flapR': COAT, 'shirt': SHIRT, 'linL': CRIM, 'linR': CRIM, 'belt': COAT,
         'armN': COAT, 'upN': COAT, 'colF': COAT, 'colN': COAT, 'linF': CRIM, 'linN': CRIM, 'neck': SK, 'hand': SK,
         'lapL': COAT, 'lapR': COAT}
    for n, r in R.items(): c.ramp(n, *r)
    # ---- back to front ----
    c.poly('tail', [(48, 38), (55, 44), (62, 52), (68, 62), (62, 62), (57, 65), (52, 58), (49, 48)])
    c.poly('tlin', [(53, 47), (59, 53), (65, 61), (61, 61), (57, 62), (54, 55)])
    c.poly('legB', [(43, 44), (48, 44), (49, 56), (49, 67), (46, 67), (45, 57)])
    c.poly('legF', [(36, 44), (42, 44), (40, 55), (36, 67), (33, 66), (35, 55)])
    c.poly('bootB', [(45, 65), (49, 65), (50, 72), (53, 74), (53, 77), (45, 77)])
    c.poly('bootF', [(32, 64), (37, 65), (36, 77), (28, 77), (28, 75), (31, 72)])
    c.poly('armF', [(31, 23), (35, 25), (33, 31), (29, 37), (25, 42), (19, 44), (18, 40), (23, 35), (27, 29)])
    c.poly('coat', [(31, 22), (37, 21), (45, 21), (51, 22), (53, 27), (51, 33), (49, 37), (35, 37), (33, 32), (31, 27)])
    c.poly('flapL', [(35, 38), (41, 38), (41, 44), (39, 52), (38, 61), (33, 63), (28, 61), (31, 52), (33, 44)])
    c.poly('flapR', [(43, 38), (49, 38), (51, 44), (53, 52), (56, 60), (51, 62), (47, 61), (45, 52), (43, 44)])
    c.poly('linL', [(40, 44), (41, 44), (39, 52), (38, 61), (37, 61), (38, 52)])
    c.poly('linR', [(43, 44), (44, 44), (46, 52), (47, 61), (46, 61), (45, 53)])
    c.poly('shirt', [(39, 21), (43, 21), (42, 26), (41, 29), (40, 26)])
    c.poly('lapL', [(35, 22), (39, 21), (41, 30), (40, 35), (36, 30)])
    c.poly('lapR', [(43, 21), (48, 22), (46, 30), (42, 35), (41, 30)])
    c.poly('belt', [(34, 36), (50, 36), (50, 38), (34, 38)])
    c.poly('upN', [(49, 22), (53, 24), (57, 30), (56, 35), (52, 35), (51, 28)])
    c.poly('armN', [(52, 30), (56, 30), (55, 35), (50, 36), (45, 34), (44, 30), (48, 30)])
    c.poly('hand', [(44, 29), (46, 29), (46, 32), (44, 32)])
    c.poly('neck', [(39, 18), (43, 18), (43, 22), (39, 22)])
    for n in R:
        if c.where(n): c.shade(n, hi_depth=1, sh_depth=1)
    c.outline(K, between=[(a, b, K) for a in R for b in R if a < b and
                          not (a.startswith('lin') and b.startswith('flap')) and not (b.startswith('lin') and a.startswith('flap'))] +
                         [('flapL', 'linL', hx(CRIM[3])), ('flapR', 'linR', hx(CRIM[3]))])
    lg = {k: (hx(v) if isinstance(v, str) else v) for k, v in _legend().items()}
    # head, then the collar standing in front of the jaw sides
    c.stamp(34, 4, FHEAD, lg)
    col = Canvas(80, 80)
    for n in ('colN', 'colF', 'linF', 'linN'): col.ramp(n, *R[n])
    col.poly('colF', [(29, 24), (31, 18), (32, 13), (35, 11), (37, 16), (39, 22), (36, 25)])
    col.poly('linF', [(35, 11), (37, 15), (39, 21), (39, 23), (37, 22), (35, 17), (33, 13)])
    col.poly('colN', [(53, 24), (53, 18), (51, 12), (48, 11), (47, 16), (44, 22), (48, 25)])
    col.poly('linN', [(47, 15), (44, 22), (45, 23), (48, 17)])
    for n in ('colF', 'colN', 'linF', 'linN'): col.shade(n)
    col.outline(K, between=[('colF', 'linF', K), ('colN', 'linN', K)])
    col.ink([q for q in col.path_pts([(30, 22), (31, 18), (33, 14)]) if col.mat[q[1]][q[0]] == 'colF' and col.col[q[1]][q[0]] != K],
            COAT[0])
    col.ink([q for q in col.path_pts([(52, 22), (51, 16), (50, 13)]) if col.mat[q[1]][q[0]] == 'colN' and col.col[q[1]][q[0]] != K],
            COAT[2])
    for y in range(80):
        for x in range(80):
            if col.mat[y][x]: c.mat[y][x] = col.mat[y][x]; c.col[y][x] = col.col[y][x]
    # lapel edges catch the light
    c.ink([q for q in c.path_pts([(39, 23), (40, 28), (40, 33)]) if c.mat[q[1]][q[0]] == 'lapL' and c.col[q[1]][q[0]] != K], COAT[0])
    # buckle, fold lines (deep tone), sheen on the lit planes
    c.stamp(40, 35, ['KKKK', 'KllK', 'KLLK', 'KKKK'], lg)
    V, cS = hx(COAT[3]), hx(COAT[0])
    folds = [[(33, 43), (31, 50), (29, 57)], [(37, 43), (35, 50), (34, 57)], [(46, 42), (48, 49), (50, 56)],
             [(49, 41), (52, 48), (54, 55)], [(34, 27), (34, 33)], [(48, 25), (49, 31)],
             [(28, 33), (25, 37)], [(56, 32), (54, 34)], [(55, 50), (60, 57)]]
    for f in folds: c.ink([q for q in c.path_pts(f) if c.mat[q[1]][q[0]] in R and c.col[q[1]][q[0]] != K], V)
    sheen = [[(32, 23), (35, 22)], [(29, 46), (28, 52), (27, 58)], [(30, 26), (28, 30), (26, 33)], [(34, 40), (34, 42)],
             [(50, 24), (53, 27)]]
    for f in sheen: c.ink([q for q in c.path_pts(f) if c.mat[q[1]][q[0]] in R and c.col[q[1]][q[0]] != K], cS)
    c.stamp(44, 29, ['Kk.', 'kks', 'ss.'], lg)                       # two fingers at the sternum (the tic)
    # Honedge: hilt hanging from the right sleeve (hand hidden), cloth wound round the cuff, blade down-left
    blade = ['...KbbBnK...',
             '...KbBBnK...',
             '....KKKK....',
             '.KKKGgGKKK..',
             'KgGGyGGGOK..',
             '.KKOGOOKKK..',
             '...KjiK.....']
    c.stamp(14, 41, blade, lg)
    x0 = 17
    for i in range(18):
        x = x0 - i // 6
        c.stamp(x, 48 + i, ['KjilK' if i < 16 else ('KjlK' if i == 16 else '.KK')], lg)
    c.stamp(22, 42, ['KbK', 'KBK', 'KBnK', '.KnK', '.KBK', '..K'], lg)
    c.drop_lone()
    return c


# =====================================================================================================================
# SILHOUETTES (guide 2.1): 80-px fronts filled black. The chosen one is A.
# =====================================================================================================================
_HEAD = [(36, 4), (44, 3), (50, 6), (52, 10), (51, 14), (47, 20), (40, 21), (35, 17), (34, 10)]
_LEGS = [[(36, 44), (42, 44), (40, 55), (36, 68), (32, 67), (35, 55)], [(43, 44), (48, 44), (49, 56), (50, 68), (46, 69), (45, 57)],
         [(31, 66), (37, 67), (36, 77), (27, 77), (27, 75), (30, 72)], [(45, 67), (50, 67), (51, 72), (54, 74), (54, 77), (45, 77)]]
_TORSO = [(31, 22), (37, 21), (45, 21), (51, 22), (53, 27), (51, 33), (49, 37), (35, 37), (33, 32), (31, 27)]
_SKIRT = [[(35, 38), (41, 38), (41, 44), (39, 52), (38, 61), (33, 63), (28, 61), (31, 52), (33, 44)],
          [(43, 38), (49, 38), (51, 44), (53, 52), (56, 60), (51, 62), (47, 61), (45, 52), (43, 44)]]
_TAIL = [(48, 38), (55, 44), (62, 52), (68, 62), (62, 62), (57, 65), (52, 58), (49, 48)]
_COLLAR = [[(29, 24), (31, 18), (32, 13), (35, 11), (37, 16), (39, 22), (36, 25)], [(53, 24), (53, 18), (51, 12), (48, 11), (47, 16), (44, 22), (48, 25)]]
_ARMF_SWORD = [[(31, 23), (35, 25), (33, 31), (29, 37), (25, 42), (19, 44), (18, 40), (23, 35), (27, 29)],
               [(12, 45), (25, 45), (25, 48), (19, 48), (19, 66), (16, 70), (14, 66), (14, 48), (12, 48)]]
_ARMN_TIC = [[(49, 22), (53, 24), (57, 30), (56, 35), (52, 35), (51, 28)], [(52, 30), (56, 30), (55, 35), (50, 36), (45, 34), (44, 30), (48, 30)]]
_ARMF_HANG = [[(31, 23), (35, 25), (34, 34), (33, 44), (28, 48), (27, 40), (29, 30)]]
_ARMN_HANG = [[(49, 22), (53, 24), (57, 32), (57, 46), (52, 50), (51, 40), (51, 30)]]
_CROSS = [[(30, 27), (54, 27), (55, 34), (29, 34)]]
_SHORTJKT = [[(31, 22), (51, 22), (53, 30), (52, 44), (32, 44), (31, 30)]]
_CAPE = [[(28, 12), (36, 16), (46, 16), (55, 12), (60, 30), (62, 62), (22, 62), (24, 30)]]
_HOOD = [[(32, 6), (40, 1), (49, 2), (55, 8), (55, 20), (50, 24), (34, 24), (31, 16)]]
_SWORD_BACK = [[(52, 4), (55, 4), (44, 40), (41, 40)], [(49, 10), (58, 13), (57, 15), (48, 12)]]
SILS = [
    ('A (chosen)', _HEAD + [], [_TORSO] + _SKIRT + [_TAIL] + _COLLAR + _ARMF_SWORD + _ARMN_TIC + _LEGS,
     'collar + Honedge diagonal + tail flare + elbow out: 5 breaks'),
    ('B', None, [_TORSO] + _SKIRT + _COLLAR + _ARMF_HANG + _ARMN_HANG + _LEGS, 'both sleeves hanging: a column, no breaks'),
    ('C', None, [_TORSO] + _SKIRT + _COLLAR + _CROSS + _LEGS, 'arms crossed: stock rival pose'),
    ('D', None, [_TORSO] + _SKIRT + [_TAIL] + _COLLAR + _SWORD_BACK + _ARMF_HANG + _ARMN_HANG + _LEGS, 'blade over the back: hides the hook'),
    ('E', None, [_TORSO] + _SKIRT + [_TAIL] + _ARMF_SWORD + _ARMN_TIC + _LEGS, 'collar down: loses the hook'),
    ('F', None, _SHORTJKT + _ARMF_SWORD + _ARMN_TIC + _LEGS, 'short jacket: reads Hugh/Silver'),
    ('G', None, _CAPE + _COLLAR + _LEGS, 'cape collar: reads vampire'),
    ('H', 'hood', [_TORSO] + _SKIRT + [_TAIL] + _HOOD + _ARMF_SWORD + _ARMN_TIC + _LEGS, 'hood up: hides the face, generic'),
]


def silhouette(i):
    name, head, polys, why = SILS[i]
    c = Canvas(80, 80); c.ramp('x', '000000', '000000', '000000', '000000')
    if head != 'hood': c.poly('x', _HEAD)
    for pg in polys: c.poly('x', pg)
    c.fill('x')
    return c.image()


if __name__ == '__main__':
    # lint only; exports and the review sheet: python3 -I tools/kitbash/rv2kl_sheet29.py all
    for e in PORTRAIT_EXPRS:
        print(e, lint(portrait(e).image())['colours'])
    print('front', lint(front().image()))
    print('overworld', lint(overworld())['colours'])
