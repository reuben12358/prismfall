"""player2_back.py - PLAYER_A / PLAYER_B EBDX back sprites in the installed format of art/out/Graphics/Trainers/PLAYER_A_back.png:
800x160 = 5 frames of 160x160 (80x80 art doubled at even offsets), the bust cut by the bottom edge.
Frame 0 idle, 1 wind-up (ball raised), 2 cocked high, 3 and 4 the throw (arm out toward the foe, hand open; 4 = 3, as installed).
Original construction (designed shapes, no donor pixels). A throws right-handed (screen right); B is left-handed (screen left),
as her front shows, so her throwing arm never fights the side tail (her right, screen right from behind).
python3 -I art/research/scripts/player2_back.py [A|B] [scheme]"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from p2kit import Spr, hx, up, ell, capsule
import player2_palette as P
from PIL import Image

OUT = '/home/claude/fangame/art/work/redo_v2/'
BALL = ('ff8a80', 'e8423a', 'a82a30', 'fbf8f4', 'cdc6d8')


def ramps(c, sc):
    for n in ('skin', 'neck', 'ear', 'arm', 'hand', 'cheek'):
        c.ramp(n, *P.SKIN)
    for n in ('jacket', 'sleeve', 'sleeve2', 'hood'):
        c.ramp(n, *sc['cream'])
    for n in ('lining', 'tee'):
        c.ramp(n, *sc['slate'])
    for n in ('bag', 'hat', 'brim', 'tie', 'knot', 'rope'):
        c.ramp(n, *sc['teal'])
    c.ramp('band', *sc['cream'])
    h = sc['hair']
    for i in range(8):
        c.ramp('hair%d' % i, h[1], h[2], h[3], h[4])
    c.ramp('ball', BALL[1], BALL[1], BALL[2], BALL[2])


# arm poses per frame: (shoulder, elbow, hand) for the throwing arm; None = hanging at the side, out of frame
ARM_A = {0: None, 1: ((61, 60), (68, 66), (66, 50)), 2: ((61, 60), (69, 52), (70, 36)), 3: ((60, 59), (68, 48), (75, 38)),
         4: ((60, 59), (68, 48), (75, 38))}
ARM_B = {0: None, 1: ((19, 60), (12, 66), (14, 50)), 2: ((19, 60), (11, 52), (10, 36)), 3: ((19, 59), (13, 44), (16, 27)),
         4: ((19, 59), (13, 44), (16, 27))}


HAND_BALL = ['...bbbbb...',
             '..bbbbbbb..',
             '.bbbbbbbbb.',
             '.bbbbbbbbb.',
             '.bbbbbbbbb.',
             '..hbbbbbh..',
             '.hhhbbbhhh.',
             '.hhhhhhhhh.',
             '.hhhhhhhhh.',
             '..hhhhhhh..',
             '...hhhhh...']
HAND_OPEN = ['.hhhh...',
             'hhhhhh..',
             'hhhhhh..',
             'hhhhhhh.',
             'hhhhhhhh',
             'hhhhhhh.',
             '.hhhhh..',
             '..hhh...']


def arm(c, pose, frame, open_hand):
    """sleeve (shoulder -> elbow, bunched where it is pushed up), forearm, then a designed hand: a fist under the ball
    (wind-up) or an open hand, fingers up, at the release."""
    (sx, sy), (ex, ey), (hx_, hy) = pose
    c.poly('sleeve', capsule((sx, sy), (ex, ey), 5.2, 4.6))
    c.poly('sleeve', ell(ex, ey, 5.0, 5.0))
    wx, wy = hx_ + (ex - hx_) * 0.25, hy + (ey - hy) * 0.25
    c.poly('arm', capsule((ex, ey), (wx, wy), 3.4, 3.0))
    if open_hand:
        rows = HAND_OPEN if hx_ < 40 else [r[::-1] for r in HAND_OPEN]       # back of the hand: thumb toward the body's midline
        c.mstamp(hx_ - (4 if hx_ < 40 else 3), hy - 5, rows, {'h': 'hand'})
    else:
        c.mstamp(hx_ - 5, hy - 9, HAND_BALL, {'h': 'hand', 'b': 'ball'})
    c.hand_at = (hx_, hy, open_hand)


def body_common(c, sc, ch):
    # neck, hood folded on the upper back (slate lining showing), jacket back, sleeves at the sides
    c.poly('neck', [(33, 46), (47, 46), (48, 58), (32, 58)])
    c.poly('jacket', [(8, 80), (9, 69), (14, 62), (25, 58), (40, 57), (55, 58), (66, 62), (71, 69), (72, 80)])
    c.poly('hood', [(23, 59), (28, 55), (40, 54), (52, 55), (57, 59), (55, 65), (48, 70), (40, 72), (32, 70), (25, 65)])
    c.poly('lining', [(28, 57), (32, 55), (40, 55), (48, 55), (52, 57), (48, 59), (40, 60), (32, 59)])


def build_A(sc, frame):
    c = Spr(80, 80); ramps(c, sc)
    K = hx(P.K); h = sc['hair']
    pose = ARM_A[frame]
    body_common(c, sc, 'A')
    # the sea bag on his back over the left shoulder (screen left): neck at the shoulder, body down the left side
    c.poly('bag', capsule((19, 61), (15, 80), 8.0, 9.5))
    c.poly('bag', [(17, 52), (23, 51), (26, 56), (22, 60), (15, 59)])
    c.poly('rope', [(20, 54), (26, 56), (34, 58), (33, 60), (25, 59), (19, 57)])
    # far arm at the side (screen right), hanging, when not throwing
    if pose is None:
        c.poly('sleeve', [(60, 61), (67, 63), (71, 69), (73, 80), (62, 80), (60, 70)])
    # head from behind, turned a little to the right: hair at the nape, the right ear and a sliver of cheek
    c.poly('cheek', [(50, 40), (55, 41), (56, 47), (53, 52), (49, 51)])
    c.poly('hair0', [(24, 39), (55, 39), (55, 44), (51, 48), (49, 53), (44, 52), (40, 55), (36, 52), (31, 54), (28, 49), (24, 45)])
    c.poly('hair1', [(26, 39), (35, 39), (35, 46), (32, 51), (30, 48), (27, 45)])
    c.poly('hair2', [(34, 39), (45, 39), (45, 47), (40, 54), (37, 48)])
    c.poly('hair3', [(44, 39), (54, 39), (53, 44), (49, 49), (46, 51), (45, 45)])
    c.poly('ear', [(51, 42), (55, 41), (56, 46), (52, 48)])
    c.poly('hat', [(25, 37), (26, 30), (31, 26), (40, 25), (49, 26), (54, 30), (55, 37)])
    c.poly('band', [(25, 33), (55, 33), (55, 37), (25, 37)], only={'hat'})
    c.poly('brim', [(17, 42), (21, 37), (59, 37), (63, 42), (62, 45), (57, 42), (23, 42), (18, 45)])
    if pose is not None:
        arm(c, pose, frame, frame >= 3)
    finish(c, sc, frame, 'A')
    return c


def build_B(sc, frame):
    c = Spr(80, 80); ramps(c, sc)
    pose = ARM_B[frame]
    behind = False
    if pose is not None and behind:
        arm(c, pose, frame, True)
    body_common(c, sc, 'B')
    # the sling: from her right shoulder (screen right) down across the back to the bag at her left hip
    c.poly('rope', [(56, 57), (60, 59), (26, 80), (21, 80)])
    if pose is None or behind:
        c.poly('sleeve2', [(20, 61), (13, 63), (9, 69), (7, 80), (18, 80), (20, 70)])
    c.poly('sleeve', [(60, 61), (67, 63), (71, 69), (73, 80), (62, 80), (60, 70)])
    # head from behind: hair gathered up toward the tie at the upper right; the nape shows
    c.poly('neck', [(34, 46), (46, 46), (47, 58), (33, 58)])
    c.poly('cheek', [(50, 40), (55, 41), (56, 47), (53, 51), (49, 50)])
    c.poly('hair0', [(25, 44), (24, 36), (28, 29), (35, 25), (44, 25), (51, 28), (55, 34), (55, 42), (51, 47), (46, 50), (40, 51),
                     (33, 50), (28, 48)])
    c.poly('ear', [(51, 41), (55, 40), (56, 45), (52, 47)])
    c.poly('hair1', [(25, 44), (26, 36), (31, 30), (39, 27), (47, 27), (52, 31), (43, 33), (36, 38), (31, 43)])   # strands sweep up-right
    c.poly('hair2', [(30, 49), (35, 42), (43, 36), (53, 32), (55, 38), (50, 44), (42, 49)])
    # the side tail: from the tie it arcs out to the right and falls over the shoulder
    c.poly('hair6', [(52, 27), (58, 23), (64, 24), (68, 29), (70, 37), (70, 46), (68, 55), (65, 63), (62, 68), (61, 62), (63, 54),
                     (64, 45), (63, 37), (60, 32), (55, 31)])
    c.poly('tie', [(49, 22), (54, 20), (56, 24), (53, 27), (49, 26)]); c.poly('tie', [(58, 19), (63, 16), (65, 20), (62, 24), (58, 23)])
    c.poly('knot', [(54, 21), (58, 21), (58, 26), (54, 26)])
    if pose is not None and not behind:
        arm(c, pose, frame, frame >= 3)
    finish(c, sc, frame, 'B')
    return c


def finish(c, sc, frame, ch):
    K = hx(P.K); h = sc['hair']
    for n in ('neck', 'ear', 'cheek', 'hood', 'lining', 'band', 'arm', 'hand', 'tie'):
        if any(c.mat[y][x] == n for y in range(80) for x in range(80)):
            c.shade(n)
    c.fill('knot', 2); c.fill('rope', 2)
    c.shade('jacket', hi=2, sh=3, group={'jacket', 'hood', 'lining', 'sleeve', 'sleeve2'})
    c.shade('hood', hi=1, sh=2)
    c.shade('sleeve', sh=2); c.shade('sleeve2', sh=1)
    c.shade('bag', hi=1, sh=3); c.shade('hat', sh=2); c.shade('brim', sh=1)
    c.shade('ball')
    for i in (0, 1, 2, 3, 6):
        c.shade('hair%d' % i, hi=0, sh=2)
    HD = hx(h[4]); sd = hx(P.SKIN[3]); cd = hx(sc['cream'][3])
    HA = ('hair0', 'hair1', 'hair2', 'hair3', 'hair6')
    pairs = [('hair0', ('hair1', 'hair2', 'hair3'), HD), ('hair1', ('hair2', 'hair3'), HD), ('hair2', 'hair3', HD),
             (('hair0', 'hair1', 'hair2'), 'hair6', HD),
             (HA, ('ear', 'cheek', 'hat', 'brim', 'band', 'neck', 'hood', 'jacket', 'tie', 'knot', 'sleeve', 'lining'), K),
             ('hat', ('brim', 'band'), K), ('band', 'brim', K), ('hat', 'band', hx(sc['teal'][3])), ('tie', 'knot', K),
             ('cheek', 'ear', sd), ('neck', ('hood', 'lining', 'jacket'), K), ('hood', ('jacket', 'sleeve', 'sleeve2'), K),
             ('lining', 'hood', hx(sc['slate'][3])), ('jacket', ('sleeve', 'sleeve2'), cd),
             ('bag', ('jacket', 'hood', 'rope', 'sleeve2', 'lining', 'neck'), K), ('rope', ('jacket', 'hood', 'lining', 'sleeve', 'sleeve2', 'neck'), K),
             ('sleeve', ('arm', 'jacket', 'hood', 'hair6', 'brim', 'hat'), K), ('arm', ('hand', 'sleeve'), sd), ('hand', 'ball', K),
             ('ball', 'hand', K), (('arm', 'hand', 'sleeve'), HA + ('hat', 'brim', 'ear', 'cheek', 'neck', 'hood', 'jacket'), K)]
    c.outline(K, pairs)
    c.drop_lone()
    # the bottom edge is a cut, not a silhouette: restore the fill colour on row 79
    for x in range(80):
        if c.mat[79][x] is not None and c.mat[78][x] is not None:
            c.col[79][x] = c.col[78][x] if c.col[78][x] != K else c.col[79][x]
    T = sc['teal']; C = sc['cream']
    L = {'K': K, 'r': hx(BALL[1]), 'q': hx(BALL[2]), 'w': hx(BALL[3]), 'x': hx(BALL[4]), 'Y': hx(sc['yel'][1]), 'y': hx(sc['yel'][2]),
         't': hx(T[0]), 'T': hx(T[1]), 'u': hx(T[2]), 'U': hx(T[3]), 'v': hx(C[2]), 'V': cd}
    # jacket back seam and the hood's fold
    c.paint([(40, 74), (40, 75), (40, 76), (40, 77), (40, 78), (40, 79)], hx(C[2]), only={'jacket'})
    c.paint([(x, 73) for x in range(16, 34)] + [(x, 73) for x in range(47, 64)], hx(C[2]), only={'jacket'})
    c.paint([(40, 61), (40, 62), (40, 63), (40, 64), (40, 65), (40, 66), (40, 67), (40, 68), (40, 69)], hx(C[2]), only={'hood'})
    under = [(x, y + k) for y in range(78) for x in range(80) for k in (1, 2) if c.mat[y][x] == 'hood' and c.mat[y + 1][x] == 'jacket']
    c.paint([(x, y) for (x, y) in under if y < 80 and c.col[y][x] != K], hx(C[2]), only={'jacket'})
    # cloth folds pulled toward the shoulders
    c.paint([(14, 70), (15, 69), (16, 68), (17, 67), (64, 67), (65, 68), (66, 69), (67, 70)], hx(C[2]), only={'jacket'})
    c.paint([(20, 76), (21, 75), (22, 74), (58, 74), (59, 75), (60, 76)], hx(C[2]), only={'jacket'})
    # hood drawstring toggles
    c.stamp(33, 58, ['T'], L); c.stamp(47, 58, ['T'], L)
    if ch == 'A':
        c.stamp(15, 50, ['.KKKKK.', 'KtTTTuK', 'KTuuuUK', '.KKUKK.'], L)              # the duffel's cinched neck
        c.stamp(12, 54, ['KKK', 'KYK', 'KyK', 'KKK'], L)                               # the ferry tag
        c.paint([(18, 62), (19, 63), (20, 65), (21, 67)], hx(T[2]), only={'bag'})
    else:
        c.stamp(2, 74, ['KKK', 'KYK', 'KyK'], L) if False else None
    if ch == 'B':
        arcs = [(30, 33), (31, 32), (32, 31), (33, 30), (34, 29), (35, 29), (36, 28), (44, 30), (45, 30), (46, 29), (47, 29),
                (34, 41), (35, 40), (36, 39), (37, 38), (38, 38), (39, 37), (64, 31), (65, 32), (66, 34), (66, 35), (66, 36), (66, 37)]
        c.paint(arcs, hx(h[0]), only={'hair0', 'hair1', 'hair2', 'hair6'})
        c.paint([(65, 44), (65, 45), (65, 46), (64, 50), (64, 51), (63, 56)], hx(h[3]), only={'hair6'})
    else:
        c.paint([(30, 44), (31, 43), (38, 44), (39, 43), (46, 44), (47, 43)], hx(h[0]), only={'hair1', 'hair2', 'hair3'})
    # fingers: splits in the skin's deep tone
    if getattr(c, 'hand_at', None):
        hx_, hy, op = c.hand_at
        sd_ = hx(P.SKIN[3]); s2 = hx(P.SKIN[2])
        if op:
            c.paint([(hx_ - 2, hy - 4), (hx_ - 2, hy - 3), (hx_, hy - 4), (hx_, hy - 3), (hx_ - 1, hy + 1), (hx_, hy + 1), (hx_ + 1, hy + 1)], sd_, only={'hand'})
        else:
            c.paint([(hx_ - 3, hy - 2), (hx_ - 1, hy - 2), (hx_ + 1, hy - 2), (hx_ + 3, hy - 2)], sd_, only={'hand'})
            c.paint([(hx_ - 3, hy), (hx_ - 2, hy), (hx_ - 1, hy), (hx_, hy), (hx_ + 1, hy), (hx_ + 2, hy)], s2, only={'hand'})
    # ball detail (red top, band, white bottom)
    bpx = [(x, y) for y in range(80) for x in range(80) if c.mat[y][x] == 'ball']
    if bpx:
        ys = [y for _, y in bpx]; my = (min(ys) + max(ys)) // 2
        for (x, y) in bpx:
            if c.col[y][x] == K: continue
            if y == my: c.col[y][x] = K
            elif y > my: c.col[y][x] = hx(BALL[3]) if (x, y + 1) in bpx and c.col[y + 1][x] != K else hx(BALL[4])
        xs = sorted(x for x, y in bpx if y == my); mx = (xs[0] + xs[-1]) // 2
        c.stamp(mx - 1, my - 1, ['KKK', 'KwK', 'KKK'], L)


def strip(ch, scheme='main'):
    sc = P.SCHEMES[ch][scheme]
    b = build_A if ch == 'A' else build_B
    frames = [b(sc, f).image() for f in range(5)]
    out = Image.new('RGBA', (400, 80), (0, 0, 0, 0))
    for i, f in enumerate(frames):
        out.alpha_composite(f, (i * 80, 0))
    return out, frames


if __name__ == '__main__':
    ch = sys.argv[1] if len(sys.argv) > 1 else 'A'
    scheme = sys.argv[2] if len(sys.argv) > 2 else 'main'
    d = OUT + 'PLAYER_%s/' % ch; os.makedirs(d, exist_ok=True)
    s, _ = strip(ch, scheme); suf = '' if scheme == 'main' else '_' + scheme
    s.save(d + 'PLAYER_%s_back%s_native.png' % (ch, suf)); up(s, 2).save(d + 'PLAYER_%s_back%s.png' % (ch, suf))
    print('ok', d, up(s, 2).size)
