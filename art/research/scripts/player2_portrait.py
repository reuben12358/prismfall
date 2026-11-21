"""player2_portrait.py - PLAYER_A / PLAYER_B dialogue portraits, 48-px art exported 96x96 (STYLE_GUIDE 3).
Original construction: shapes -> light from the upper left -> lines -> feature stamps. One base face per character;
expressions only move or swap brow, eye and mouth pixels (+ tear / sweat / blush marks).
PLAYER_A: J1 round jaw, E1 big round eyes (6 rows, flat top lash), B2 strong brows. Hook: the sailcloth bucket hat.
PLAYER_B: J2 soft V chin, E1 big round eyes (7 rows, lash flick), B1 soft brows. Hook: the high side tail + teal tie.
python3 -I art/research/scripts/player2_portrait.py [A|B] [scheme] -> art/work/redo_v2/PLAYER_X/portraits/"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from p2kit import Spr, hx, up, ell, capsule
import player2_palette as P

EXPRS = ['neutral', 'happy', 'sad', 'angry', 'surprised', 'shocked', 'smug', 'deadpan', 'panic', 'crying', 'blush']
SIGNATURE = {'A': 'determined', 'B': 'grin'}
OUT = '/home/claude/fangame/art/work/redo_v2/'


def ramps(c, sc):
    c.ramp('skin', *P.SKIN); c.ramp('ear', *P.SKIN); c.ramp('neck', *P.SKIN)
    c.ramp('cream', *sc['cream']); c.ramp('hat', *sc['cream']); c.ramp('brim', *sc['cream']); c.ramp('hood', *sc['cream'])
    c.ramp('slate', *sc['slate']); c.ramp('teal', *sc['teal']); c.ramp('band', *sc['teal']); c.ramp('tie', *sc['teal'])
    c.ramp('knot', *sc['teal'])
    h = sc['hair']
    for i in range(8):
        c.ramp('hair%d' % i, h[1], h[2], h[3], h[4])


# =============================================================================== PLAYER_A (boy)
HAT_TEAL = True        # the bucket hat in faded teal canvas (the hook in colour) with a cream band


def base_A(sc):
    c = Spr(48, 48); ramps(c, sc)
    if HAT_TEAL:
        c.ramp('hat', *sc['teal']); c.ramp('brim', *sc['teal']); c.ramp('band', *sc['cream'])
    K = hx(P.K); h = sc['hair']
    # --- back to front
    c.poly('neck', [(20, 36), (30, 37), (30, 47), (20, 47)])
    c.poly('hair0', [(9, 15), (7, 20), (8, 26), (10, 31), (13, 35), (16, 35), (16, 27), (17, 20), (24, 18), (33, 18), (38, 20),
                     (41, 25), (42, 18), (40, 14)])                                         # one mass, no holes
    c.poly('hair1', [(10, 14), (7, 20), (8, 26), (10, 31), (12, 35), (14, 33), (13, 27), (14, 21), (17, 16)])   # side lock over the ear
    c.poly('ear', [(15, 26), (12, 25), (11, 27), (11, 31), (12, 33), (15, 34)])
    c.poly('skin', [(15, 17), (37, 17), (38, 21), (39, 27), (38, 32), (36, 36), (33, 39), (30, 41), (26, 41), (23, 41), (20, 39),
                    (18, 37), (16, 33), (15, 29), (14, 23)])
    # fringe clumps under the brim: tips point down, the far ones lean with the turn of the head (screen right)
    c.poly('hair2', [(15, 15), (22, 15), (21, 17), (19, 19), (17, 21), (17, 18), (15, 18)])
    c.poly('hair3', [(21, 15), (29, 15), (28, 17), (26, 19), (24, 21), (23, 18), (21, 17)])
    c.poly('hair4', [(28, 15), (36, 15), (35, 17), (33, 18), (31, 20), (30, 17), (28, 17)])
    c.poly('hair5', [(35, 15), (41, 15), (41, 19), (40, 23), (39, 26), (38, 20), (36, 17)])
    # the bucket hat: a soft crown with sloped sides, a band, a brim that droops at both ends
    c.poly('hat', [(12, 11), (14, 6), (17, 3), (23, 2), (30, 2), (35, 3), (38, 6), (40, 11)])
    c.poly('band', [(12, 8), (40, 8), (40, 11), (12, 11)], only={'hat'})
    c.poly('brim', [(5, 15), (9, 12), (14, 11), (38, 11), (42, 12), (45, 16), (44, 18), (40, 16), (36, 15), (16, 15), (10, 16), (5, 18)])
    # body: jacket shoulders, the hood rolled behind the neck, slate tee, the bag rope over the far shoulder
    c.poly('hood', [(11, 41), (15, 37), (21, 38), (21, 42)]); c.poly('hood', [(29, 39), (35, 37), (39, 40), (31, 42)])
    c.poly('cream', [(0, 47), (0, 44), (6, 41), (15, 39), (21, 42), (24, 47)])
    c.poly('cream', [(47, 47), (47, 44), (42, 41), (35, 40), (30, 43), (27, 47)])
    c.poly('slate', [(20, 42), (30, 42), (29, 47), (22, 47)])
    # --- light
    for n in ('neck', 'ear', 'hood', 'slate', 'band'):
        c.shade(n)
    c.shade('cream', hi=1, sh=1)
    c.shade('hat', hi=1, sh=2); c.shade('brim', hi=1, sh=1)
    c.shade('skin', hi=1, sh=2)
    c.fill('teal', 2)
    for i in range(6):
        c.shade('hair%d' % i, hi=0, sh=2)
    # --- lines
    HD = hx(h[4]); hd = c.ramps['hat'][3]
    pairs = []
    order = ['hair0', 'hair1', 'hair2', 'hair3', 'hair4', 'hair5']
    for a in range(len(order)):
        for b in range(a + 1, len(order)):
            pairs.append((order[a], order[b], HD))
    for i in range(6):
        pairs += [('hair%d' % i, 'skin', K), ('hair%d' % i, 'ear', K), ('hair%d' % i, ('hat', 'brim', 'band'), K)]
    pairs += [('skin', 'neck', hx(P.SKIN[3])), ('ear', 'skin', hx(P.SKIN[3])), ('neck', ('slate', 'cream', 'hood'), K),
              ('hood', 'cream', hx(sc['cream'][3])), ('slate', ('cream', 'hood'), K), ('hat', 'brim', K), ('band', 'brim', K),
              ('hat', 'band', hd), ('teal', 'cream', K), ('cream', 'teal', hx(sc['cream'][3]))]
    c.outline(K, pairs)
    c.drop_lone()
    # --- hand passes: under-brim shadow, neck under the jaw, hair arcs, hat stitching
    s1, s2, s0 = hx(P.SKIN[2]), hx(P.SKIN[3]), hx(P.SKIN[0])
    c.paint([(x, y) for y in range(36, 42) for x in range(18, 33) if c.mat[y][x] == 'neck'], s1)
    c.paint([(x, y) for y in (17, 18) for x in range(16, 39) if c.mat[y][x] == 'skin'], s1)
    W = hx(h[0])
    arcs = [(23, 16), (24, 17), (30, 16), (31, 17),
            (10, 18), (10, 19), (10, 20), (11, 22), (11, 23)]
    c.paint([(x, y) for (x, y) in arcs if (c.mat[y][x] or '').startswith('hair') and c.col[y][x] not in (K, HD)], W)
    hr = c.ramps['brim']
    c.paint([(19, 5), (20, 4), (21, 4), (22, 4)], c.ramps['hat'][0])
    c.paint([(31, 4), (32, 5), (33, 6), (33, 7)], c.ramps['hat'][2])
    rope(c, sc, [(34, 40), (41, 47)])
    Y = sc['yel']
    c.stamp(37, 41, ['.K..', 'KYYK', 'KYyK', 'KyyK', '.KK.'], {'K': K, 'Y': hx(Y[1]), 'y': hx(Y[2])})   # the ferry tag on the rope
    return c


def features_A(c, expr, sc):
    L = legend(sc)
    # eye boxes: near (screen-left) x16-23, far x29-35; lash top row at y=23 (eye line 26)
    E = EYES_A[expr if expr in EYES_A else {'blush': 'neutral', 'crying': 'sad', 'panic': 'surprised'}.get(expr, 'neutral')]
    ny = E.get('y', 24)
    c.stamp(17, ny, E['near'], L)
    c.stamp(29, ny, E['far'], L)
    B = BROWS_A[expr if expr in BROWS_A else 'neutral']
    c.stamp(17, B[0], B[1], L); c.stamp(29, B[2], B[3], L)
    c.stamp(27, 31, ['s.', 'sd'], L)                                                  # nose: far-side shadow, dark underside
    m = MOUTHS_A[expr]
    c.stamp(m[0], m[1], m[2], L)
    for (x, y, rows) in MARKS.get(expr, []):
        c.stamp(x, y, rows, L)


EYES_A = {
    # E1: 7 wide, 2-row top lash with the outer flick, 5-row opening, a 2x2 pupil with the highlight top-right, lower lid in skin shadow
    'neutral': {'near': ['..KKKKK.', '.KKKKKKK', 'KEEaaaaK', '.EEaKKWE', '.EEAKKAE', '.EEAAAAE', '..EEAAE.', '...ssss.'],
                'far': ['.KKKKK..', 'KKKKKKK.', 'KEaaaaEK', 'EEaKKWE.', 'EEAKKAE.', 'EEAAAAE.', '.EAAEE..', '.ssss...']},
    'happy': {'y': 26, 'near': ['..KKKK..', '.K....K.', 'K......K', '.ssssss.'], 'far': ['.KKKK...', 'K....K..', '......K.', 'ssssss..']},
    'surprised': {'y': 22, 'near': ['..KKKKK.', '.KKKKKKK', '.EEEEEEK', '.EEaaaaE', '.EEaKWAE', '.EEAAAAE', '..EEAAE.', '...EEE..', '...sss..'],
                  'far': ['.KKKKK..', 'KKKKKKK.', 'EEEEEEK.', 'EaaaaEE.', 'EaKWAEE.', 'EAAAAEE.', '.EAAEE..', '..EEE...', '..sss...']},
    'shocked': {'y': 22, 'near': ['..KKKKK.', '.KKKKKKK', '.EEEEEEK', '.EEEEEEE', '.EEEaEEE', '.EEEEEEE', '..EEEEE.', '...EEE..', '...sss..'],
                'far': ['.KKKKK..', 'KKKKKKK.', 'EEEEEEK.', 'EEEEEEE.', 'EEEaEEE.', 'EEEEEEE.', '.EEEEE..', '..EEE...', '..sss...']},
    'smug': {'near': ['........', '........', '..KKKKK.', 'KKKKKKKK', '.EEaKKWE', '.EEAKKAE', '..EAAAE.', '...ssss.'],
             'far': ['........', '........', '.KKKKK..', 'KKKKKKKK', 'EEaKKWE.', 'EEAKKAE.', '.EAAAE..', '.ssss...']},
    'sad': {'near': ['........', '.....KK.', '..KKKKKK', 'KKEaaaaK', '.EEaKKWE', '.EEAKKAE', '.EEAAAAE', '..EEAAE.', '...ssss.'],
            'far': ['........', '.KK.....', 'KKKKKK..', 'KEaaaaKK', 'EEaKKWE.', 'EEAKKAE.', 'EEAAAAE.', '.EAAEE..', '.ssss...']},
    'angry': {'near': ['........', 'KK......', '.KKKKKKK', 'KKKKKKKK', '.EEaKKWE', '.EEAKKAE', '..EAAAE.', '...sss..'],
              'far': ['........', '......KK', 'KKKKKKK.', 'KKKKKKKK', 'EEaKKWE.', 'EEAKKAE.', '.EAAAE..', '..sss...']},
}
EYES_A['determined'] = {'near': ['........', '..KKKKK.', 'KKKKKKKK', 'KEEaKKWK', '.EEAKKAE', '.EEAAAAE', '..EEAAE.', '...ssss.'],
                        'far': ['........', '.KKKKK..', 'KKKKKKKK', 'KEaKKWEK', 'EEAKKAE.', 'EEAAAAE.', '.EAAEE..', '.ssss...']}
EYES_A['deadpan'] = {'near': ['........', '........', '........', 'KKKKKKKK', '.EEaKKaE', '.EEAKKAE', '..ssss..'],
                     'far': ['........', '........', '........', 'KKKKKKKK', 'EEaKKaE.', 'EEAKKAE.', '.ssss...']}

BROWS_A = {   # (near y, rows, far y, rows) - B2 strong, 2 rows, thick at the inner end (near brow's inner end is on its right)
    'neutral': (20, ['.bBBBBB.', 'BBb.....'], 20, ['.BBBBBb.', '......bB']),
    'happy': (19, ['.bBBBBB.', 'BBb.....'], 19, ['.BBBBBb.', '......bB']),
    'blush': (20, ['....bBB.', '.BBBb...'], 20, ['.BBb....', '...bBBB.']),
    'surprised': (18, ['.bBBBB..', 'Bb......'], 18, ['..BBBBb.', '......bB']),
    'shocked': (18, ['.bBBBB..', 'Bb......'], 18, ['..BBBBb.', '......bB']),
    'panic': (19, ['....bBB.', '.BBBb...'], 19, ['.BBb....', '...bBBB.']),
    'sad': (20, ['....bBB.', '.BBBb...'], 20, ['.BBb....', '...bBBB.']),
    'crying': (20, ['....bBB.', '.BBBb...'], 20, ['.BBb....', '...bBBB.']),
    'angry': (20, ['BBb.....', '.bBBBB..', '....bBBB'], 20, ['......bB', '..BBBBb.', 'BBBb....']),
    'determined': (21, ['BBBb....', '..bBBBBB'], 21, ['.....bBB', 'BBBBBb..']),
    'smug': (21, ['.bBBBBB.', 'BB......'], 19, ['.BBBBB..', 'B.....Bb']),
    'deadpan': (21, ['.BBBBBB.'], 21, ['BBBBBBB.']),
}

MOUTHS_A = {   # (x, y, rows): closed = line + corners, open = outlined hole + dark interior + teeth/tongue rows
    'neutral': (25, 37, ['R....R', '.RRRR.', '..ss..']),
    'happy': (23, 36, ['KKKKKKKK', 'KTTTTTTK', '.KoooooK', '..KtttK.', '...KKK..']),
    'blush': (25, 37, ['.RRR..', 'R...R.', '.ss...']),
    'sad': (25, 37, ['.RRRR.', 'R....R', '.ss...']),
    'crying': (24, 36, ['..KKKK..', '.KooooK.', 'KoooooK.', 'KttttK..', '.KKKK...']),
    'angry': (24, 36, ['KKKKKKK', 'KTTTTTK', 'KoooooK', 'KTTTTTK', '.KKKKK.']),
    'determined': (24, 36, ['K......', 'KKKKKKK', '.KTTTTK', '..KKKK.', '...ss..']),
    'surprised': (26, 36, ['.KKK.', 'KoooK', 'KoooK', 'KtttK', '.KKK.', '.sss.']),
    'shocked': (25, 36, ['.KKKK.', 'KooooK', 'KooooK', 'KottoK', '.KKKK.']),
    'panic': (24, 36, ['.KKKKKK.', 'KTTTTTTK', 'KooooooK', '.KttttK.', '..KKKK..']),
    'smug': (25, 36, ['......R', '.....R.', 'RRRRR..', '.sss...']),
    'deadpan': (26, 37, ['RRRR', '.ss.']),
}

MARKS = {
    'blush': [(17, 32, ['.p.p.p', 'p.p.p.']), (31, 32, ['.p.p.p', 'p.p.p.'])],
    'crying': [(17, 29, ['w', 'w', '.w', '.w', '.w']), (35, 29, ['w', 'w', 'w', 'w'])],
    'panic': [(41, 21, ['.w', 'wx', 'ww'])],
    'shocked': [(41, 21, ['.w', 'wx', 'ww'])],
}


def rope(c, sc, pts):
    """a 2-px twisted cord: light upper strand, dark lower strand, a deep twist pixel every third step, black ends."""
    T = sc['teal']; K = hx(P.K)
    seen = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = max(abs(x1 - x0), abs(y1 - y0))
        for i in range(n + 1):
            x = round(x0 + (x1 - x0) * i / n); y = round(y0 + (y1 - y0) * i / n)
            if (x, y) not in seen: seen.append((x, y))
    for i, (x, y) in enumerate(seen):
        if not c.inside(x, y): continue
        c.paint([(x, y)], hx(T[1]) if i % 3 else hx(T[3]))
        c.paint([(x, y + 1)], hx(T[2]) if i % 3 != 1 else hx(T[3]))
        c.paint([(x, y - 1)], K) if c.inside(x, y - 1) and (x, y - 1) not in seen else None


def legend(sc):
    return {'K': hx(P.K), 'B': hx(sc['brow']), 'b': hx(sc['hair'][2]), 'E': hx(P.EYE_W), 'a': hx(sc['iris'][1]),
            'A': hx(sc['iris'][0]), 'W': hx(P.HL), 's': hx(P.SKIN[2]), 'd': hx(P.SKIN[3]), 'h': hx(P.SKIN[0]),
            'R': hx(P.MOUTH[0]), 'o': hx(P.MOUTH[1]), 'T': hx(P.MOUTH[2]), 't': hx(P.MOUTH[3]), 'p': hx(P.BLUSH),
            'w': hx('bfe8f4'), 'x': hx('6aa8c8')}


def build(ch, expr, scheme='main'):
    sc = P.SCHEMES[ch][scheme]
    if ch == 'A':
        c = base_A(sc); features_A(c, expr, sc)
    else:
        c = base_B(sc); features_B(c, expr, sc)
    return c


# =============================================================================== PLAYER_B (girl)
def base_B(sc):
    c = Spr(48, 48); ramps(c, sc)
    K = hx(P.K); h = sc['hair']
    c.poly('neck', [(21, 36), (30, 37), (30, 47), (21, 47)])
    # one hair silhouette first (no holes): crown, the far face-framing lock, the near side pulled up to the tie
    c.poly('hair0', [(10, 10), (14, 5), (21, 2), (30, 2), (36, 5), (40, 9), (42, 15), (42, 24), (41, 32), (39, 37), (37, 30),
                     (37, 21), (34, 16), (20, 15), (16, 17), (14, 22), (13, 26), (11, 23), (10, 17)])
    # the high side tail: from the tie it arcs out past the head and falls to the shoulder; air between tail and head
    c.poly('hair1', [(11, 7), (7, 4), (3, 5), (1, 10), (0, 17), (0, 25), (1, 33), (4, 41), (6, 44), (7, 37), (7, 29), (7, 21),
                     (8, 14), (10, 11)])
    c.poly('ear', [(15, 26), (12, 25), (11, 27), (11, 31), (12, 33), (15, 34)])
    c.poly('skin', [(15, 17), (36, 15), (38, 20), (39, 26), (38, 31), (36, 35), (33, 38), (30, 40), (27, 42), (25, 42), (22, 40),
                    (19, 37), (16, 33), (15, 28), (14, 22)])
    # side-swept fringe: parted above the near eye, sweeping to the far side, tips down and right
    c.poly('hair3', [(14, 10), (19, 6), (26, 5), (27, 9), (26, 13), (22, 16), (19, 20), (17, 16), (15, 14)])
    c.poly('hair4', [(22, 6), (30, 4), (35, 7), (34, 11), (31, 14), (28, 18), (27, 21), (25, 16), (23, 12)])
    c.poly('hair5', [(31, 6), (37, 8), (41, 13), (42, 20), (41, 28), (40, 35), (38, 30), (37, 22), (35, 15), (33, 11)])
    # the tie: a teal sailcloth bow at the root of the tail
    c.poly('tie', [(2, 2), (8, 4), (8, 8), (4, 10), (1, 7)])
    c.poly('tie', [(12, 4), (17, 1), (19, 4), (17, 8), (12, 8)])
    c.poly('knot', [(8, 4), (11, 4), (11, 8), (8, 8)])
    # body: jacket, hood roll, slate tee, the bag rope across the chest
    c.poly('hood', [(12, 41), (16, 37), (22, 38), (22, 42)]); c.poly('hood', [(29, 39), (34, 37), (38, 40), (31, 42)])
    c.poly('cream', [(0, 47), (0, 44), (6, 41), (16, 39), (22, 42), (24, 47)])
    c.poly('cream', [(47, 47), (47, 44), (42, 41), (34, 40), (29, 43), (27, 47)])
    c.poly('slate', [(21, 42), (30, 42), (29, 47), (22, 47)])
    for n in ('neck', 'ear', 'hood', 'slate', 'tie'):
        c.shade(n)
    c.fill('knot', 2)
    c.shade('cream', hi=1, sh=1); c.shade('skin', hi=1, sh=2); c.fill('teal', 2)
    for i in range(6):
        c.shade('hair%d' % i, hi=0, sh=2)
    HD = hx(h[4])
    pairs = []
    order = ['hair0', 'hair1', 'hair3', 'hair4', 'hair5']
    for a in range(len(order)):
        for b in range(a + 1, len(order)):
            pairs.append((order[a], order[b], HD))
    for i in range(6):
        pairs += [('hair%d' % i, 'skin', K), ('hair%d' % i, 'ear', K), ('hair%d' % i, ('tie', 'knot'), K)]
    pairs += [('tie', 'knot', K)]
    pairs += [('skin', 'neck', hx(P.SKIN[3])), ('ear', 'skin', hx(P.SKIN[3])), ('neck', ('slate', 'cream', 'hood', 'teal'), K),
              ('hood', 'cream', hx(sc['cream'][3])), ('slate', ('cream', 'hood'), K), ('teal', ('cream', 'slate', 'hood'), K),
              ('cream', 'teal', hx(sc['cream'][3]))]
    c.outline(K, pairs)
    c.drop_lone()
    s1 = hx(P.SKIN[2])
    c.paint([(x, y) for y in range(36, 42) for x in range(20, 32) if c.mat[y][x] == 'neck'], s1)
    W = hx(h[0])
    arcs = [(17, 10), (18, 9), (19, 9), (20, 8), (21, 8), (27, 8), (28, 7), (29, 7), (30, 7), (37, 11), (38, 12), (39, 14), (39, 15),
            (3, 12), (3, 13), (3, 14), (3, 15), (3, 16), (4, 21), (4, 22), (4, 23), (24, 3), (25, 3), (26, 3), (32, 4), (33, 4)]
    c.paint([(x, y) for (x, y) in arcs if (c.mat[y][x] or '').startswith('hair') and c.col[y][x] not in (K, HD)], W)
    rope(c, sc, [(10, 39), (19, 44), (25, 47)])
    Y = sc['yel']
    c.stamp(16, 42, ['.K..', 'KYYK', 'KYyK', 'KyyK', '.KK.'], {'K': K, 'Y': hx(Y[1]), 'y': hx(Y[2])})
    return c


def features_B(c, expr, sc):
    L = legend(sc)
    key = {'blush': 'neutral', 'crying': 'sad', 'panic': 'surprised', 'grin': 'neutral'}.get(expr, expr)
    E = EYES_B[key if key in EYES_B else 'neutral']
    ny = E.get('y', 24)
    c.stamp(17, ny, E['near'], L)
    c.stamp(29, ny, E['far'], L)
    B = BROWS_B[expr if expr in BROWS_B else 'neutral']
    c.stamp(17, B[0], B[1], L); c.stamp(30, B[2], B[3], L)
    c.stamp(27, 31, ['s.', 'sd'], L)
    m = MOUTHS_B[expr]
    c.stamp(m[0], m[1], m[2], L)
    for (x, y, rows) in MARKS.get(expr, []):
        c.stamp(x, y, rows, L)


EYES_B = {
    # E1 with a longer lash: an upturned flick at the outer corner, a lash tick under it
    'neutral': {'near': ['K.KKKK..', '.KKKKKKK', 'KEEaaaaK', '.EEaKKWE', '.EEAKKAE', '.EEAAAAE', '..EEAAE.', '...ssss.'],
                'far': ['..KKKK.K', 'KKKKKKK.', 'KEaaaaEK', 'EEaKKWE.', 'EEAKKAE.', 'EEAAAAE.', '.EAAEE..', '.ssss...']},
    'happy': {'y': 26, 'near': ['..KKKK..', '.K....K.', 'K......K', '.ssssss.'], 'far': ['.KKKK...', 'K....K..', '......K.', 'ssssss..']},
    'surprised': {'y': 22, 'near': ['K.KKKK..', '.KKKKKKK', '.EEEEEEK', '.EEaaaaE', '.EEaKWAE', '.EEAAAAE', '..EEAAE.', '...EEE..', '...sss..'],
                  'far': ['..KKKK.K', 'KKKKKKK.', 'EEEEEEK.', 'EaaaaEE.', 'EaKWAEE.', 'EAAAAEE.', '.EAAEE..', '..EEE...', '..sss...']},
    'shocked': {'y': 22, 'near': ['K.KKKK..', '.KKKKKKK', '.EEEEEEK', '.EEEEEEE', '.EEEaEEE', '.EEEEEEE', '..EEEEE.', '...EEE..', '...sss..'],
                'far': ['..KKKK.K', 'KKKKKKK.', 'EEEEEEK.', 'EEEEEEE.', 'EEEaEEE.', 'EEEEEEE.', '.EEEEE..', '..EEE...', '..sss...']},
    'smug': {'near': ['........', '........', 'K.KKKK..', '.KKKKKKK', 'KEEaKKWE', '.EEAKKAE', '..EAAAE.', '...ssss.'],
             'far': ['........', '........', '..KKKK.K', 'KKKKKKK.', 'EEaKKWEK', 'EEAKKAE.', '.EAAAE..', '.ssss...']},
    'sad': {'near': ['........', '.....KK.', '..KKKKKK', 'KKEaaaaK', '.EEaKKWE', '.EEAKKAE', '.EEAAAAE', '..EEAAE.', '...ssss.'],
            'far': ['........', '.KK.....', 'KKKKKK..', 'KEaaaaKK', 'EEaKKWE.', 'EEAKKAE.', 'EEAAAAE.', '.EAAEE..', '.ssss...']},
    'angry': {'near': ['........', 'KK......', '.KKKKKKK', 'KKKKKKKK', '.EEaKKWE', '.EEAKKAE', '..EAAAE.', '...sss..'],
              'far': ['........', '......KK', 'KKKKKKK.', 'KKKKKKKK', 'EEaKKWE.', 'EEAKKAE.', '.EAAAE..', '..sss...']},
}

EYES_B['deadpan'] = {'near': ['........', '........', '........', 'KKKKKKKK', '.EEaKKaE', '.EEAKKAE', '..ssss..'],
                     'far': ['........', '........', '........', 'KKKKKKKK', 'EEaKKaE.', 'EEAKKAE.', '.ssss...']}

BROWS_B = {   # B1 soft: 1 row, 4-5 px, hair-dark tone
    'neutral': (21, ['.bBBB.'], 21, ['.BBBb.']),
    'happy': (20, ['.bBBB.'], 20, ['.BBBb.']),
    'blush': (21, ['...bB.', '.BBb..'], 21, ['.Bb...', '..bBB.']),
    'surprised': (19, ['bBBB..'], 19, ['..BBBb']),
    'shocked': (19, ['bBBB..'], 19, ['..BBBb']),
    'panic': (19, ['...bB.', '.BBb..'], 19, ['.Bb...', '..bBB.']),
    'sad': (20, ['...bB.', '.BBb..'], 20, ['.Bb...', '..bBB.']),
    'crying': (20, ['...bB.', '.BBb..'], 20, ['.Bb...', '..bBB.']),
    'angry': (20, ['.Bb...', '..bBBB'], 20, ['...bB.', 'BBBb..']),
    'grin': (19, ['.bBBB.'], 19, ['..BBBb']),
    'smug': (21, ['.bBBB.'], 19, ['.BBBb.']),
    'deadpan': (22, ['.BBBB.'], 22, ['.BBBB.']),
}

MOUTHS_B = {
    'neutral': (25, 37, ['R...R', '.RRR.', '..s..']),
    'happy': (24, 36, ['KKKKKKK', 'KTTTTTK', '.KoooK.', '..KtK..', '...K...']),
    'blush': (25, 37, ['.RR..', 'R..R.', '.ss..']),
    'sad': (25, 37, ['.RRR.', 'R...R', '.ss..']),
    'crying': (24, 36, ['..KKK..', '.KoooK.', 'KoooooK', 'KtttttK', '.KKKKK.']),
    'angry': (24, 36, ['KKKKKK', 'KTTTTK', 'KooooK', 'KTTTTK', '.KKKK.']),
    'grin': (24, 36, ['K.....K', 'KKKKKKK', 'KTTTTTK', '.KoooK.', '..KKK..', '...s...']),
    'surprised': (26, 36, ['.KK.', 'KooK', 'KooK', 'KttK', '.KK.', '.ss.']),
    'shocked': (25, 36, ['.KKKK.', 'KooooK', 'KooooK', 'KottoK', '.KKKK.']),
    'panic': (24, 36, ['.KKKKK.', 'KTTTTTK', 'KoooooK', '.KtttK.', '..KKK..']),
    'smug': (25, 36, ['.....R', '....R.', 'RRRR..', '.ss...']),
    'deadpan': (26, 37, ['RRR', '.s.']),
}


if __name__ == '__main__':
    ch = sys.argv[1] if len(sys.argv) > 1 else 'A'
    scheme = sys.argv[2] if len(sys.argv) > 2 else 'main'
    d = OUT + 'PLAYER_%s/portraits/' % ch; os.makedirs(d, exist_ok=True)
    for e in EXPRS + [SIGNATURE[ch]]:
        im = build(ch, e, scheme).image()
        im.save(d + 'PLAYER_%s_%s_48%s.png' % (ch, e, '' if scheme == 'main' else '_' + scheme))
        up(im, 2).save(d + 'PLAYER_%s_%s%s.png' % (ch, e, '' if scheme == 'main' else '_' + scheme))
    print('ok', d)
