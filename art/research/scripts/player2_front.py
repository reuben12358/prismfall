"""player2_front.py - PLAYER_A / PLAYER_B battle fronts: 80x80 art, exported 160x160 + _native80 (STYLE_GUIDE 4).
Original construction from designed shapes (no donor pixels): polygons and tapered limbs back to front -> light from the upper
left -> black silhouette + material lines -> hand stamps for face, hands and small hardware.
A: weight on the near leg, the sea bag slung over his left shoulder on its rope, a ball held out low in the other hand.
B: mid-step, her right hand up at the side tail's bow (a salute to the ferry), the bag across her back on a rope sling.
python3 -I art/research/scripts/player2_front.py [A|B] [scheme]"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from p2kit import Spr, hx, up, ell, capsule
import player2_palette as P

OUT = '/home/claude/fangame/art/work/redo_v2/'
BALL = ('ff8a80', 'e8423a', 'a82a30', 'fbf8f4', 'cdc6d8')        # ball: red hi/base/shadow, white, white shadow


def ramps(c, sc):
    c.ramp('skin', *P.SKIN); c.ramp('neck', *P.SKIN); c.ramp('ear', *P.SKIN); c.ramp('arm', *P.SKIN); c.ramp('hand', *P.SKIN)
    c.ramp('arm2', *P.SKIN); c.ramp('hand2', *P.SKIN); c.ramp('leg', *P.SKIN); c.ramp('leg2', *P.SKIN)
    for n in ('jacket', 'jacketf', 'sleeve', 'sleeve2', 'hood', 'brimc', 'band', 'sock', 'sock2'):
        c.ramp(n, *sc['cream'])
    for n in ('tee', 'trou', 'trou2', 'cuff', 'cuff2', 'shorts'):
        c.ramp(n, *sc['slate'])
    for n in ('bag', 'hat', 'brim', 'tie', 'knot', 'rope'):
        c.ramp(n, *sc['teal'])
    h = sc['hair']
    for i in range(8):
        c.ramp('hair%d' % i, h[1], h[2], h[3], h[4])
    for n in ('boot', 'boot2'):
        c.ramp(n, h[1], h[2], h[3], h[4])              # leather boots share the hair's brown ramp (no extra colours)


# =============================================================================== PLAYER_A
def build_A(sc):
    c = Spr(80, 80); ramps(c, sc)
    K = hx(P.K); h = sc['hair']
    # ---- the sea bag behind his left side (screen right): cinched neck at the shoulder, tilted, round seamed bottom
    c.spans('bag', {26: (53, 56), 27: (52, 57), 28: (52, 58), 29: (52, 59), 30: (53, 60), 31: (53, 61), 32: (53, 62), 33: (53, 62),
                    34: (53, 63), 35: (53, 63), 36: (53, 63), 37: (54, 64), 38: (54, 64), 39: (54, 64), 40: (54, 64), 41: (54, 64),
                    42: (54, 65), 43: (54, 65), 44: (55, 65), 45: (55, 65), 46: (55, 65), 47: (55, 65), 48: (56, 65), 49: (56, 65),
                    50: (56, 64), 51: (57, 64), 52: (57, 63), 53: (58, 62), 54: (59, 61)})
    # ---- trousers: seat, near leg (screen left, planted), far leg (stepping out); rolled cuffs; boots with the toes out
    c.spans('trou', {y: (33, 47) for y in range(45, 52)})
    c.spans('trou', {**{y: (33, 39) for y in range(50, 55)}, **{y: (33, 38) for y in range(55, 59)},
                     **{y: (32, 38) for y in range(59, 63)}, **{y: (32, 37) for y in range(63, 67)}})
    c.spans('trou2', {50: (41, 47), 51: (41, 47), 52: (41, 47), 53: (42, 48), 54: (42, 48), 55: (43, 48), 56: (43, 49), 57: (44, 49),
                      58: (44, 50), 59: (44, 50), 60: (44, 50), 61: (44, 50), 62: (44, 49), 63: (44, 49), 64: (44, 49), 65: (44, 49), 66: (44, 49)})
    c.spans('cuff', {y: (31, 38) for y in range(67, 70)})
    c.spans('cuff2', {y: (43, 50) for y in range(67, 70)})
    c.spans('boot', {70: (31, 38), 71: (31, 38), 72: (30, 38), 73: (29, 38), 74: (28, 38), 75: (27, 38), 76: (27, 38), 77: (27, 38)})
    c.spans('boot2', {70: (43, 50), 71: (43, 50), 72: (43, 51), 73: (43, 52), 74: (43, 53), 75: (43, 54), 76: (43, 54), 77: (43, 54)})
    # ---- torso: the hood rolled behind the neck, slate tee, the open jacket (two panels), hip length
    c.spans('hood', {27: (34, 46), 28: (33, 46), 29: (33, 47)})
    c.spans('tee', {**{y: (38, 42) for y in range(29, 47)}})
    c.spans('jacket', {30: (31, 38), **{y: (30, 38) for y in range(31, 36)}, **{y: (31, 38) for y in range(36, 46)}, 46: (32, 38), 47: (32, 38)})
    c.spans('jacketf', {30: (42, 48), **{y: (42, 49) for y in range(31, 42)}, **{y: (42, 48) for y in range(42, 48)}})
    # ---- far arm (his left): upper arm down the side, fist at the chest on the bag rope
    c.spans('sleeve2', {31: (48, 51), 32: (48, 52), 33: (48, 52), 34: (49, 52), 35: (49, 53), 36: (49, 53), 37: (49, 53), 38: (49, 54),
                        39: (49, 54), 40: (50, 54)})
    c.spans('arm2', {39: (47, 50), 40: (47, 51), 41: (48, 51)})
    c.spans('hand2', {35: (45, 48), 36: (44, 49), 37: (44, 49), 38: (44, 49), 39: (45, 48)})
    # ---- head: neck, ear, face, hair, hat
    c.poly('neck', [(37, 25), (43, 25), (43, 30), (37, 30)])
    c.poly('hair0', [(31, 14), (30, 19), (31, 24), (33, 27), (35, 26), (36, 20), (44, 15), (48, 18), (48, 23), (50, 19), (49, 13)])
    c.poly('ear', [(46, 19), (49, 18), (49, 23), (46, 24)])
    c.poly('skin', [(33, 15), (46, 15), (47, 19), (46, 23), (44, 26), (40, 28), (37, 28), (34, 26), (32, 22), (32, 17)])
    c.poly('hair1', [(32, 14), (37, 14), (36, 17), (34, 20), (33, 18)])                    # fringe, tips toward screen left
    c.poly('hair2', [(36, 14), (42, 14), (41, 16), (38, 19), (37, 17)])
    c.poly('hair3', [(41, 14), (48, 14), (48, 18), (46, 21), (45, 17), (43, 16)])
    c.poly('hat', [(31, 12), (33, 7), (37, 5), (43, 5), (47, 7), (49, 12)])
    c.poly('band', [(31, 10), (49, 10), (49, 12), (31, 12)], only={'hat'})
    c.poly('brim', [(27, 15), (29, 12), (51, 12), (53, 15), (52, 17), (48, 15), (32, 15), (28, 17)])
    # ---- near arm (his right): sleeve pushed to the elbow, forearm out, the ball held low and forward
    c.spans('sleeve', {31: (29, 31), 32: (28, 31), 33: (27, 31), 34: (27, 31), 35: (26, 30), 36: (26, 30), 37: (25, 30), 38: (25, 30)})
    c.spans('arm', {39: (25, 29), 40: (24, 28), 41: (24, 28), 42: (23, 27), 43: (23, 27)})
    c.spans('ball', {42: (18, 22), 43: (17, 23), 44: (16, 24), 45: (16, 24), 46: (16, 24), 47: (16, 24), 48: (17, 23), 49: (18, 22)})
    c.spans('hand', {43: (22, 26), 44: (21, 26), 45: (21, 26), 46: (21, 25), 47: (22, 25)})
    # ---- the rope: from the fist up over the shoulder to the bag's neck
    c.spans('rope', {34: (46, 47), 33: (47, 48), 32: (47, 48), 31: (48, 49), 30: (48, 50), 29: (49, 51), 28: (50, 52), 27: (51, 53)})

    # ---- light (upper left)
    c.ramp('ball', BALL[1], BALL[1], BALL[2], BALL[2])
    for n in ('neck', 'ear', 'hood', 'tee', 'band', 'cuff', 'cuff2', 'arm', 'arm2', 'hand', 'hand2'):
        c.shade(n)
    c.shade('skin', hi=1, sh=1)
    c.shade('jacket', sh=2, group={'jacket', 'tee', 'jacketf'}); c.shade('jacketf', sh=2, group={'jacket', 'tee', 'jacketf'})
    c.shade('sleeve', sh=2); c.shade('sleeve2', sh=2)
    c.fill('rope', 2)
    c.shade('trou', sh=2, group={'trou', 'cuff'}); c.shade('trou2', sh=2, group={'trou2', 'cuff2'})
    c.shade('boot', sh=1); c.shade('boot2', sh=1)
    c.shade('bag', hi=1, sh=3); c.shade('hat', sh=2); c.shade('brim')
    for i in range(4):
        c.shade('hair%d' % i, hi=0, sh=1)
    # ---- lines
    HD = hx(h[4]); sd = hx(P.SKIN[3]); cd = hx(sc['cream'][3]); td = hx(sc['slate'][3]); bd = hx(sc['teal'][3])
    pairs = [('hair0', ('hair1', 'hair2', 'hair3'), HD), ('hair1', 'hair2', HD), ('hair2', 'hair3', HD),
             (('hair0', 'hair1', 'hair2', 'hair3'), ('skin', 'ear', 'hat', 'brim', 'band'), K),
             ('hat', 'brim', K), ('band', 'brim', K), ('hat', 'band', bd), ('skin', 'neck', sd), ('ear', 'skin', sd),
             ('neck', ('tee', 'hood', 'jacket'), K), ('hood', ('jacket', 'tee'), cd), ('tee', 'jacket', K),
             (('jacket', 'jacketf'), ('trou', 'trou2'), K), ('sleeve', ('jacket', 'arm', 'tee'), K), ('sleeve2', ('jacketf', 'arm2', 'bag'), K),
             ('jacketf', ('tee', 'hand2', 'arm2'), K), ('jacket', 'tee', K), ('rope', ('jacketf', 'hood', 'sleeve2', 'hand2', 'bag'), K),
             ('arm', ('hand', 'sleeve'), sd), ('arm2', ('hand2', 'sleeve2'), sd), ('hand', 'ball', K), ('hand2', ('bag', 'hood', 'jacket'), K),
             ('trou', 'trou2', K), ('trou', 'cuff', td), ('trou2', 'cuff2', td), ('cuff', 'boot', K), ('cuff2', 'boot2', K),
             ('boot', 'boot2', K), ('trou', 'boot2', K),
             ('bag', ('jacketf', 'sleeve2', 'arm2', 'hand2', 'hood', 'trou2', 'tee', 'rope'), K),
             ('ball', ('hand', 'arm'), K)]
    c.outline(K, pairs)
    c.drop_lone()
    # ---- hand passes
    T = sc['teal']; C = sc['cream']; S = sc['slate']; Y = sc['yel']
    L = {'K': K, 'E': hx(P.EYE_W), 'a': hx(sc['iris'][1]), 'A': hx(sc['iris'][0]), 'W': hx(P.HL), 's': hx(P.SKIN[2]),
         'd': sd, 'h': hx(P.SKIN[0]), 'k': hx(P.SKIN[1]), 'R': hx(P.MOUTH[0]), 'B': hx(sc['brow']),
         't': hx(T[0]), 'T': hx(T[1]), 'u': hx(T[2]), 'U': bd, 'c': hx(C[0]), 'C': hx(C[1]), 'v': hx(C[2]), 'V': cd,
         'Y': hx(Y[1]), 'y': hx(Y[2]), 'r': hx(BALL[1]), 'q': hx(BALL[2]), 'w': hx(BALL[3]), 'x': hx(BALL[4]),
         'S': hx(S[1]), 'z': hx(S[2]), 'Z': td, 'H': hx(h[0]), 'n': hx(h[1]), 'N': hx(h[2]), 'm': hx(h[3])}
    # face (3/4 toward screen left): eyes 2x3 with a catchlight, brows, small mouth
    c.stamp(33, 18, ['BBB....BB.', '.........', 'KK....KK', 'aW....aW', 'AA....AA'], L)
    c.stamp(35, 20, ['.'], L)
    c.stamp(37, 24, ['R..R', '.RR.'], L)
    c.paint([(33, 17), (34, 17), (35, 17), (36, 17), (37, 17), (38, 17), (39, 17), (40, 17), (41, 17), (42, 17), (43, 17), (44, 17), (45, 17)],
            hx(P.SKIN[2]), only={'skin'})
    # hair arcs
    c.paint([(33, 15), (34, 16), (38, 15), (39, 15), (44, 15), (45, 16)], hx(h[0]), only={'hair1', 'hair2', 'hair3'})
    # hat: crown light, crease
    c.paint([(36, 7), (37, 6), (38, 6)], hx(T[0]), only={'hat'})
    # ball: red top, black band, white bottom, button
    c.stamp(16, 42, ['..KKKKK..', '.KrrrrrK.', 'KrrrrrrqK', 'KrrrrrqqK', 'KKKKwKKKK', 'KwwKwKwxK', '.KwwwwxK.', '..KKKKK..'], L)
    # bag: cinched neck, drawstring, the ferry tag, a fold and the bottom seam
    c.stamp(52, 24, ['.KKKK.', 'KtTTuK', 'KTuuUK', '.KUUK.'], L)                       # cinched neck
    c.stamp(57, 29, ['KKK', 'KYK', 'KyK', 'KKK'], L)                                   # the ferry tag
    c.paint([(55, 30), (56, 31), (57, 33), (59, 31), (60, 32), (61, 33)], hx(T[2]), only={'bag'})   # gathers under the cinch
    c.paint([(57, 40), (58, 41), (59, 42), (60, 43)], hx(T[2]), only={'bag'})                       # a soft fold
    c.paint([(56, 50), (57, 51), (58, 51), (59, 51), (60, 51), (61, 51), (62, 50), (63, 49)], bd, only={'bag'})   # bottom seam
    c.paint([(55, 36), (55, 37), (55, 38), (56, 39)], hx(T[0]), only={'bag'})
    # jacket: toggles, pocket line, hem fold
    c.stamp(37, 33, ['T', '.', '.', 'T'], L)
    c.paint([(32, 42), (33, 42), (34, 42), (35, 42)], cd, only={'jacket'})
    c.paint([(45, 43), (46, 43), (47, 43)], cd, only={'jacketf'})
    # trousers: knee creases, the crotch fold, a lit edge on the near leg
    c.paint([(35, 58), (36, 59), (36, 60)], td, only={'trou'})
    c.paint([(46, 57), (47, 58), (47, 59)], td, only={'trou2'})
    c.paint([(39, 49), (40, 50), (41, 49)], td, only={'trou'})
    c.paint([(34, y) for y in range(52, 66)], hx(S[0]), only={'trou'})
    # the far fist on the rope: knuckles and finger splits
    c.stamp(45, 36, ['sss.', '.d.d'], L)
    c.stamp(22, 45, ['.d', 'd.'], L)
    # boots: dark soles, a lit toe cap, lace line
    for x in range(27, 39):
        if c.mat[76][x] == 'boot' and c.col[76][x] != K: c.col[76][x] = hx(h[3])
    for x in range(43, 55):
        if c.mat[76][x] == 'boot2' and c.col[76][x] != K: c.col[76][x] = hx(h[3])
    c.paint([(28, 74), (29, 73), (30, 73)], hx(h[0]), only={'boot'})
    c.paint([(51, 73), (52, 74)], hx(h[0]), only={'boot2'})
    c.paint([(33, 72), (34, 72), (35, 72)], hx(h[3]), only={'boot'})
    c.paint([(45, 72), (46, 72), (47, 72)], hx(h[3]), only={'boot2'})
    # jacket: a fold at the near elbow and the waist
    c.paint([(28, 36), (29, 37)], cd, only={'sleeve'})
    c.paint([(33, 46), (34, 46), (35, 47)], cd, only={'jacket'})
    return c


def build(ch, scheme='main'):
    sc = P.SCHEMES[ch][scheme]
    return build_A(sc) if ch == 'A' else build_B(sc)


def build_B(sc):
    c = Spr(80, 80); ramps(c, sc)
    for n in ('boot', 'boot2'):
        c.ramp(n, *sc['slate'])                         # her boots are slate (the plum hair stays on the head)
    K = hx(P.K); h = sc['hair']
    # ---- the side tail behind the head (her right = screen left), arcing out and down past the shoulder
    c.poly('hair6', [(32, 7), (28, 5), (24, 7), (22, 12), (21, 19), (21, 27), (22, 34), (24, 40), (26, 44), (27, 38), (26, 31),
                     (26, 24), (26, 17), (28, 12), (30, 10)])
    # ---- the bag at her left hip (screen right), on the sling
    c.spans('bag', {42: (48, 52), 43: (47, 55), 44: (47, 57), 45: (47, 58), 46: (47, 59), 47: (47, 59), 48: (47, 60), 49: (47, 60),
                    50: (47, 60), 51: (48, 60), 52: (48, 59), 53: (49, 59), 54: (51, 58)})
    # ---- legs: near/far by depth: her left leg (screen right) planted, her right leg (screen left) stepping out
    c.spans('leg2', {**{y: (43, 47) for y in range(49, 56)}, **{y: (43, 47) for y in range(56, 61)}, **{y: (44, 47) for y in range(61, 64)}})
    c.spans('sock2', {**{y: (43, 48) for y in range(61, 70)}})
    c.spans('boot2', {70: (43, 48), 71: (43, 48), 72: (43, 49), 73: (43, 50), 74: (43, 51), 75: (43, 52), 76: (43, 52), 77: (43, 52)})
    c.spans('leg', {49: (34, 38), 50: (34, 38), 51: (33, 38), 52: (33, 37), 53: (33, 37), 54: (32, 37), 55: (32, 36), 56: (31, 36),
                    57: (31, 36), 58: (31, 35), 59: (31, 35), 60: (30, 35)})
    c.spans('sock', {61: (30, 35), 62: (30, 35), 63: (29, 35), 64: (29, 34), 65: (29, 34), 66: (28, 34), 67: (28, 34), 68: (28, 34)})
    c.spans('boot', {69: (27, 34), 70: (27, 34), 71: (27, 34), 72: (26, 34), 73: (25, 34), 74: (24, 34), 75: (24, 34), 76: (24, 34)})
    c.spans('shorts', {**{y: (33, 47) for y in range(43, 49)}, 49: [(33, 38), (42, 48)], 50: [(33, 38), (42, 48)], 51: [(32, 38), (42, 48)]})
    # ---- torso: hood roll, tee (shows under the cropped jacket), jacket panels
    c.spans('hood', {27: (35, 45), 28: (34, 46), 29: (34, 46)})
    c.spans('tee', {**{y: (39, 41) for y in range(29, 43)}})
    c.spans('jacket', {30: (32, 39), **{y: (31, 39) for y in range(31, 38)}, **{y: (32, 39) for y in range(38, 42)}, 42: (33, 39)})
    c.spans('jacketf', {30: (41, 48), **{y: (41, 49) for y in range(31, 38)}, **{y: (41, 48) for y in range(38, 42)}, 42: (41, 47)})
    # ---- far arm (her right, screen left): down the side, hand on the sling at her chest
    c.spans('sleeve2', {31: (29, 32), 32: (28, 32), 33: (28, 32), 34: (28, 32), 35: (28, 32), 36: (28, 32), 37: (28, 32), 38: (28, 33)})
    c.spans('arm2', {39: (29, 33), 40: (30, 34), 41: (31, 35)})
    c.spans('hand2', {38: (34, 37), 39: (34, 38), 40: (35, 38), 41: (35, 38)})
    # ---- the sling: from her right shoulder across the chest to the bag at her left hip
    c.spans('rope', {29: (33, 34), 30: (34, 35), 31: (35, 36), 32: (36, 37), 33: (37, 38), 34: (38, 39), 35: (39, 40), 36: (40, 41),
                     37: (41, 42), 38: (42, 43), 39: (43, 44), 40: (44, 45), 41: (45, 46), 42: (46, 47), 43: (47, 48)}, only=None)
    # ---- head
    c.poly('neck', [(37, 25), (42, 25), (42, 30), (37, 30)])
    c.poly('hair0', [(31, 12), (34, 8), (39, 6), (45, 7), (49, 11), (50, 17), (50, 24), (49, 29), (47, 29), (47, 22), (44, 16),
                     (36, 15), (33, 19), (32, 25), (30, 24), (30, 17)])
    c.poly('ear', [(31, 19), (30, 18), (29, 20), (30, 23), (32, 23)])
    c.poly('skin', [(33, 15), (46, 15), (47, 19), (46, 23), (44, 26), (41, 28), (38, 28), (35, 26), (33, 22), (32, 18)])
    c.poly('hair1', [(32, 13), (36, 9), (42, 8), (42, 11), (39, 13), (37, 16), (36, 19), (35, 16), (33, 16)])   # side-swept fringe
    c.poly('hair2', [(39, 9), (45, 8), (48, 11), (47, 14), (45, 16), (43, 19), (42, 15), (40, 13)])
    c.poly('hair3', [(45, 9), (49, 12), (50, 18), (50, 24), (49, 29), (47, 25), (47, 19), (46, 14)])          # far-side lock
    c.poly('tie', [(28, 4), (32, 6), (32, 9), (28, 10), (27, 7)]); c.poly('tie', [(34, 5), (38, 2), (39, 5), (37, 8), (34, 8)])
    c.poly('knot', [(32, 5), (34, 5), (34, 9), (32, 9)])
    # ---- near arm (her left, screen right): raised, a ball held up by her shoulder
    c.spans('sleeve', {30: (48, 51), 31: (48, 52), 32: (49, 53), 33: (50, 54), 34: (51, 55), 35: (52, 56), 36: (52, 56)})
    c.spans('arm', {27: (54, 57), 28: (54, 57), 29: (54, 57), 30: (54, 57), 31: (54, 57), 32: (54, 57), 33: (54, 57), 34: (55, 57)})
    c.spans('hand', {22: (53, 57), 23: (53, 58), 24: (53, 58), 25: (53, 58), 26: (54, 57)})
    c.spans('ball', {17: (54, 58), 18: (53, 59), 19: (52, 60), 20: (52, 60), 21: (52, 60), 22: (52, 60), 23: (53, 59), 24: (54, 58)})
    c.spans('hand', {21: (55, 58), 22: (54, 58), 23: (54, 58), 24: (54, 58), 25: (54, 57)})

    # ---- light
    c.ramp('ball', BALL[1], BALL[1], BALL[2], BALL[2])
    for n in ('neck', 'ear', 'hood', 'tee', 'arm', 'arm2', 'hand', 'hand2', 'tie'):
        c.shade(n)
    c.fill('knot', 2)
    c.shade('skin', hi=1, sh=1); c.shade('leg'); c.shade('leg2', sh=2)
    c.shade('sock'); c.shade('sock2', sh=2)
    c.shade('jacket', sh=2, group={'jacket', 'tee', 'jacketf'}); c.shade('jacketf', sh=2, group={'jacket', 'tee', 'jacketf'})
    c.shade('sleeve', sh=2); c.shade('sleeve2', sh=2); c.fill('rope', 2)
    c.shade('shorts', sh=1); c.shade('boot'); c.shade('boot2'); c.shade('bag', hi=1, sh=2)
    for i in (0, 1, 2, 3, 6):
        c.shade('hair%d' % i, hi=0, sh=1)
    HD = hx(h[4]); sd = hx(P.SKIN[3]); cd = hx(sc['cream'][3]); td = hx(sc['slate'][3]); bd = hx(sc['teal'][3])
    H = ('hair0', 'hair1', 'hair2', 'hair3', 'hair6')
    pairs = [('hair6', ('hair0', 'hair1', 'hair2', 'hair3'), HD), ('hair0', ('hair1', 'hair2', 'hair3'), HD), ('hair1', 'hair2', HD), ('hair2', 'hair3', HD),
             (H, ('skin', 'ear', 'tie', 'knot', 'hood', 'neck'), K), ('tie', 'knot', K),
             ('skin', 'neck', sd), ('ear', 'skin', sd), ('neck', ('tee', 'hood', 'jacket', 'jacketf', 'rope'), K), ('hood', ('jacket', 'jacketf', 'tee'), cd),
             ('tee', ('jacket', 'jacketf'), K), (('jacket', 'jacketf', 'tee'), ('shorts',), K), ('sleeve', ('jacketf', 'arm'), K),
             ('sleeve2', ('jacket', 'arm2', 'hand2'), K), ('jacket', ('tee', 'hand2', 'arm2'), K), ('jacketf', 'tee', K),
             ('rope', ('jacket', 'jacketf', 'tee', 'hood', 'hand2', 'bag', 'shorts'), K), ('arm', ('hand', 'sleeve'), sd), ('arm2', ('hand2',), sd),
             ('hand', 'ball', K), ('ball', ('hand', 'arm'), K), ('leg', ('shorts', 'sock'), K), ('leg2', ('shorts', 'sock2'), K),
             ('sock', 'boot', K), ('sock2', 'boot2', K), ('boot', 'boot2', K), ('leg', 'leg2', K),
             ('shorts', ('leg', 'leg2'), K), ('bag', ('shorts', 'jacketf', 'leg2', 'tee', 'rope', 'sleeve'), K), ('hair6', ('jacket', 'sleeve2'), K)]
    c.outline(K, pairs)
    c.drop_lone()
    T = sc['teal']; C = sc['cream']; S = sc['slate']; Y = sc['yel']
    L = {'K': K, 'E': hx(P.EYE_W), 'a': hx(sc['iris'][1]), 'A': hx(sc['iris'][0]), 'W': hx(P.HL), 's': hx(P.SKIN[2]),
         'd': sd, 'R': hx(P.MOUTH[0]), 'B': hx(sc['brow']), 't': hx(T[0]), 'T': hx(T[1]), 'u': hx(T[2]), 'U': bd,
         'Y': hx(Y[1]), 'y': hx(Y[2]), 'r': hx(BALL[1]), 'q': hx(BALL[2]), 'w': hx(BALL[3]), 'x': hx(BALL[4])}
    # face (3/4 toward screen left)
    c.stamp(34, 18, ['.BB...BB', '........', 'KK....KK', 'aW....aW', 'AA....AA'], L)
    c.stamp(38, 24, ['R..R', '.RR.'], L)
    c.paint([(x, 17) for x in range(33, 47)], hx(P.SKIN[2]), only={'skin'})
    c.paint([(35, 9), (36, 9), (37, 9), (42, 9), (43, 9), (44, 9), (47, 13), (48, 14), (48, 15), (25, 12), (24, 13), (24, 14), (24, 15),
             (24, 16), (24, 20), (24, 21)], hx(h[0]), only=set(H))
    c.stamp(51, 16, ['..KKKKK..', '.KrrrrrK.', 'KrrrrrqqK', 'KKKKwKKKK', 'KwwKwKxKK', '.KwwwxK..', '..KKKK...'], L)
    c.stamp(46, 40, ['.KKK.', 'KtTuK', '.KUK.'], L)                                    # cinched neck at the sling
    c.stamp(50, 41, ['KKK', 'KYK', 'KyK', 'KKK'], L)                                    # the ferry tag
    c.paint([(51, 46), (52, 47), (53, 47), (54, 48)], hx(T[2]), only={'bag'})
    c.paint([(57, 44), (58, 45), (59, 46), (59, 47), (59, 48)], bd, only={'bag'})
    c.paint([(36, 46), (37, 47)], td, only={'shorts'})
    C = sc['cream']
    # socks: a ribbed top band; boots: dark soles and a lit toe
    c.paint([(x, 61) for x in range(29, 37)], hx(C[2]), only={'sock'}); c.paint([(x, 61) for x in range(43, 49)], hx(C[2]), only={'sock2'})
    for x in range(22, 56):
        for n in ('boot', 'boot2'):
            if c.mat[76][x] == n and c.col[76][x] != K: c.col[76][x] = td
            if c.mat[77][x] == n and c.col[77][x] != K: c.col[77][x] = td
    c.paint([(25, 73), (26, 72), (27, 72)], hx(S[0]), only={'boot'}); c.paint([(50, 74), (51, 75)], hx(S[0]), only={'boot2'})
    c.paint([(29, 70), (30, 70), (31, 70)], td, only={'boot'}); c.paint([(45, 71), (46, 71), (47, 71)], td, only={'boot2'})
    # the hand on the sling: finger splits; the tail: a second clump crease down its length
    c.stamp(35, 40, ['.d.d'], L)
    c.paint([(25, 16), (25, 17), (25, 18), (24, 22), (24, 23), (24, 24), (24, 25), (25, 30), (25, 31), (26, 36)], hx(h[3]), only={'hair6'})
    return c


if __name__ == '__main__':
    ch = sys.argv[1] if len(sys.argv) > 1 else 'A'
    scheme = sys.argv[2] if len(sys.argv) > 2 else 'main'
    d = OUT + 'PLAYER_%s/' % ch; os.makedirs(d, exist_ok=True)
    im = build(ch, scheme).image(); suf = '' if scheme == 'main' else '_' + scheme
    im.save(d + 'PLAYER_%s%s_native80.png' % (ch, suf)); up(im, 2).save(d + 'PLAYER_%s%s.png' % (ch, suf))
    print('ok', d)
