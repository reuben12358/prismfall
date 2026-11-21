"""Dialogue faces v1: Kestrel Vane and Dorian Pell (48-px art -> 96x96, Juno pass-3 geometry).

    python3 -I tools/kitbash/faces_v1.py      -> art/work/kitbash/passes/faces_v1/{KESTREL,DORIAN}_<expr>.png (+ _48 natives)

Style anchor: art/out/Graphics/Portraits/JUNO_*.png (pass 3: official B2W2 VS-bust family, Rosa face, black 1-px outline,
flat bright skin, transparent where nothing is drawn). Juno's landmarks at 48 px: eyes x13-20 / x30-37 from y24, mouth
y37-38 around x26, chin y44, crown outline at y2 (2 px clear above), eyes mirrored about x=25.

Method (KITBASH_PIPELINE lessons 9-12):
  * one official B2W2 VS face per character, placed so its eyes, mouth and chin land on Juno's rows;
  * everything that identifies the donor goes: hair rebuilt as shaped locks (Bezier spines tapering to points, flat
    B2W2 2-tone + cast-shadow lines, black only on the silhouette, one crown highlight arc), new eye colour, new
    clothes, donor blush/shine removed;
  * the eyes are one stamp per character (mirrored), in the construction of Juno's accepted eye;
  * EXPRESSIONS: one base face per character. An expression only swaps the brow/eye/mouth stamps, and every variant
    is the base stamp with rows or pixels moved (lid lowered = lash rows moved down, surprise = lash moved up, ...).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, mat
from mat import H, CLEAR, BLACK
from PIL import Image

V5 = '/home/claude/ref/art/sprites_gen5_vs_tech/extracted/Gen 5 VS Sprites/vsTrainer_'
OUT = kb.WORK + '/passes/faces_v1'
EYE_WHITE, SHINE = H('e8e8f8'), H('fff8f0')
SKIN, SKS, SKD = H('f8d0b8'), H('d8a078'), H('b08058')          # Juno's skin ramp
MOUTH, MOUTH_D, LIP = H('983840'), H('702838'), H('b88878')     # Juno's mouth colours
TEETH, TONGUE = H('f8f8f8'), H('e06880')


def bust(n):
    return kb.native(kb.load(V5 + n + '.png'))[0]


def place(src, box, dx, dy):
    """crop src box and put it on a clear 48x48 canvas at canvas = src + (dx, dy)."""
    out = Image.new('RGBA', (48, 48), CLEAR)
    part = src.crop(box)
    out.paste(part, (box[0] + dx, box[1] + dy), part)
    return out


def stamp(im, x0, y0, rows, legend, mirror=False):
    """ASCII stamp; mirror=True puts it mirrored about x=25 (the face centre), box x0..x0+w-1 -> 51-x0-w.."""
    if mirror:
        w = max(len(r) for r in rows)
        rows = [r.ljust(w, '.')[::-1] for r in rows]
        x0 = 51 - x0 - w
    return mat.patch(im, x0, y0, rows, legend)


# ------------------------------------------------------------------ hair locks
def bez(pts, t):
    while len(pts) > 1:
        pts = [((1 - t) * a[0] + t * b[0], (1 - t) * a[1] + t * b[1]) for a, b in zip(pts, pts[1:])]
    return pts[0]


def lock_cover(pts, w, taper=1.0, n=40):
    """{(x, y): (t, side)}: pixels at least half covered by a lock whose spine is the Bezier `pts` and whose width
    tapers from w at the root to a point at the tip ((1-t)**taper). 4x4 supersampling decides coverage only."""
    samp = [bez(list(pts), i / n) for i in range(n + 1)]
    rad = [w / 2 * (1 - i / n) ** taper for i in range(n + 1)]
    xs = [q[0] for q in samp]; ys = [q[1] for q in samp]
    out = {}
    for y in range(int(min(ys) - w), int(max(ys) + w) + 1):
        for x in range(int(min(xs) - w), int(max(xs) + w) + 1):
            hit = 0; tb = None; sb = 0
            for sy in range(4):
                for sx in range(4):
                    px, py = x + (sx + .5) / 4, y + (sy + .5) / 4
                    best = None
                    for i, (qx, qy) in enumerate(samp):
                        d2 = (px - qx) ** 2 + (py - qy) ** 2
                        if d2 <= rad[i] ** 2 and (best is None or d2 < best[0]):
                            best = (d2, i)
                    if best:
                        hit += 1; i = best[1]
                        tb = i if tb is None else min(tb, i)
                        j, k = min(i + 1, n), max(i - 1, 0)
                        dx, dy = samp[j][0] - samp[k][0], samp[j][1] - samp[k][1]
                        sb += (px - samp[i][0]) * dy - (py - samp[i][1]) * dx      # > 0: right of travel
            if hit >= 8:
                out[(x, y)] = (tb / n, sb / hit)
    return out


_LOCK_CACHE = {}


def render_locks(locks, clip=None):
    """later locks are in front. -> {(x, y): (lock_index, t, side)} (cached per lock list)"""
    key = (repr(locks), getattr(clip, 'key', None))
    if key in _LOCK_CACHE:
        return dict(_LOCK_CACHE[key])
    idm = {}
    for k, L in enumerate(locks):
        for (x, y), (t, sd) in lock_cover(L['pts'], L['w'], L.get('taper', 1.0)).items():
            if 0 <= x < 48 and 0 <= y < 48 and (clip is None or clip(x, y)):
                idm[(x, y)] = (k, t, sd)
    _LOCK_CACHE[key] = idm
    return dict(idm)


def dome(cx=24.5, cy=23, rx=22.5, ry=21):
    f = lambda x, y: y >= cy or ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2 <= 1
    f.key = (cx, cy, rx, ry)
    return f


def hair_paint(im, idm, old_hair, ramp, arc=(0.80, 0.88), arc_c=(24.5, 25, 23, 22), arc_rows=14, tip_dark=0.72,
               shade_side=2.2, tone=None, lines=lambda k, j: 0 < j < k):
    """Paint the locks of idm over im. ramp = [outline, line, dark, mid, light]. old_hair: donor hair pixels that stay
    hair (already recoloured by the caller); they count as hair for the silhouette."""
    p = im.load()
    hair = set(idm) | set(old_hair)
    for (x, y), (k, t, sd) in idm.items():
        if tone:
            p[x, y] = ramp[tone(x, y, k, t, sd)]
        else:
            p[x, y] = ramp[2] if k and (t > tip_dark or sd > shade_side) else ramp[3]
    for (x, y), (k, t, sd) in idm.items():                  # cast-shadow line on the lock behind a front lock's edge
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            q = (x + dx, y + dy)
            if q in idm and lines(k, idm[q][0]):
                p[q] = ramp[1]
    if arc:
        cx, cy, rx, ry = arc_c                              # one highlight arc over the crown
        for (x, y), (k, t, sd) in idm.items():
            r = (((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2) ** .5
            if arc[0] <= r <= arc[1] and p[x, y] in (ramp[3], ramp[2]) and y < arc_rows:
                p[x, y] = ramp[4]
    for (x, y) in idm:                                      # black only on the silhouette
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            q = (x + dx, y + dy)
            if not (0 <= q[0] < 48 and 0 <= q[1] < 48):
                if q[1] < 0:
                    p[x, y] = ramp[0]
                continue
            if q not in hair:
                p[x, y] = ramp[0]
                break
    return im


def seg_d(a, b, x, y):
    ax, ay = a; bx, by = b
    t = max(0, min(1, ((x - ax) * (bx - ax) + (y - ay) * (by - ay)) / ((bx - ax) ** 2 + (by - ay) ** 2)))
    return ((x - ax - t * (bx - ax)) ** 2 + (y - ay - t * (by - ay)) ** 2) ** .5, t


# ------------------------------------------------------------------ expression stamps (shared operators)
def lid(eye, n=1):
    """upper lid lowered n rows: the lash rows move down, covering the top of the iris (squint / half-lidded)."""
    w = len(eye[0])
    return ['s' * w] * n + eye[:2] + eye[2 + n:]


def wide(eye, rows_up=1):
    """lash moved up one row: the top iris row becomes a row of eye white (surprise)."""
    return eye[1:2] + [eye[1]] + [eye[2].replace('a', 'w')] + eye[3:]


# ============================================================== KESTREL
# Base face: official B2W2 VS Cheren (Leader), the sharpest frontal male face. What makes it Cheren goes: the hair is
# rebuilt as a side-swept fringe with a long lock over his right eye (screen left), teal eyes -> steel grey, blush
# and forehead shine gone, half-face shadow lifted (Juno's skin is flat and bright), white shirt and tie -> his mother's
# black greatcoat with the collar flipped up, crimson lining and a crimson undershirt (CHARACTER_ART.md).
CH = {'A': H('182028'), 'B': H('404860'), 'C': H('f8d8c0'), 'D': H('586068'), 'E': H('987058'), 'F': H('808080'),
      'G': H('d8a878'), 'W': H('f8f8f8'), 'I': H('b8b8b8'), 'J': H('407080'), 'K': H('f8b8b0'), 'L': H('783838'),
      'M': H('b88878')}
K_HAIR = [BLACK, H('141824'), H('262c40'), H('384060'), H('525e84')]      # outline, line, dark, mid, light
K_EYES = [H('263040'), H('62748e'), H('a8bccc')]     # steel grey (amber read as Kieran next to the fringe)
K_COAT = [BLACK, H('0f0f14'), H('24232e'), H('3d3c4c'), H('5a5a6e')]
K_CRIM = [H('4a0e1a'), H('6e1020'), H('b0202e'), H('e04048')]
K_LOCKS = [
    dict(pts=[(24, -14), (24, 2), (24, 12)], w=44),                 # dome
    dict(pts=[(35, 2), (44, 6), (45, 22)], w=14, taper=.6),         # right side, swept back from the part
    dict(pts=[(22, 2), (7, 7), (4, 28)], w=14, taper=.6),           # left back
    dict(pts=[(29, 2), (21, 7), (19, 18)], w=12, taper=.7),         # fringe D
    dict(pts=[(31, 3), (26, 8), (25, 17)], w=11, taper=.7),         # fringe C
    dict(pts=[(34, 3), (32, 9), (31, 16)], w=10, taper=.7),         # fringe B
    dict(pts=[(36, 3), (38, 9), (40, 16)], w=10, taper=.6),         # temple lock at the part
    dict(pts=[(28, 2), (15, 7), (13, 31)], w=12, taper=.55),        # the long lock over his right eye
]
KX = {'#': BLACK, 'w': EYE_WHITE, 'a': K_EYES[0], 'A': K_EYES[1], 'L': K_EYES[2], 'K': SHINE, 's': SKIN,
      'h': SKS, 'd': SKD, 'b': K_HAIR[1], 'm': MOUTH, 'M': MOUTH_D, 'l': LIP, 't': TEETH, 'T': TONGUE}
# screen-right eye at x30-37 from y23; the left eye is its mirror (x13-20)
K_EYE = ["ss#####s",
         "s#######",
         "#waaaa##",
         "swa##Aw#",
         "swA#KAws",
         "shLLLLhs",
         "sssddds."]
K_BROW_R = {                                # x29-37, y17-21 (left brow mirrored)
    'neutral':   ["sssssssss", "sssssssss", "sssssbbbs", "ssbbbbbss", "sbbssssss"],
    'smug_up':   ["sssssssss", "sssbbbbss", "sbbsssbbs", "sssssssss", "sssssssss"],
    'smug_flat': ["sssssssss", "sssssssss", "sssssssss", "sbbbbbbbs", "sssssssss"],
    'angry':     ["sssssssss", "sssssssss", "sssssbbbs", "sssbbbbss", "sbbbsssss"],
    'sad':       ["sssssssss", "sbbbsssss", "ssbbbbsss", "ssssssbbs", "sssssssss"],
    'surprised': ["sssbbbbss", "sbbssssbs", "sssssssss", "sssssssss", "sssssssss"],
}
K_MOUTH = {                                 # x23-31, y36-40
    'neutral':   ["sssssssss", "sssmmmmss", "ssssssdss", "sssssssss", "sssssssss"],
    'smirk':     ["sssssssms", "sssmmmmds", "sssssddss", "sssssssss", "sssssssss"],
    'angry':     ["sssssssss", "sssmmmmss", "ssmttttms", "ssmMMMMms", "sssmmmmss"],
    'sad':       ["sssssssss", "ssssmmmss", "sssmsssms", "sssssssss", "sssssssss"],
    'surprised': ["sssssssss", "ssssmmsss", "sssmMMmss", "sssmMMmss", "ssssmmsss"],
}


def laugh_eye(eye):
    """eyes shut in a laugh: the base lash row (7 px) moved into an upward arch over a closed lid; crease kept."""
    w = len(eye[0])
    return [eye[0], 's' * w, 's' * w, 'ss####ss', 's#ssss#s', 'ssssssss', 'ssssssss', 'ssssssss']


def pin_pupils(eye, mid='A'):
    """shock: the 2x2 pupil shrinks to one pixel; the other three become iris. Lash rows are left alone."""
    e = list(eye); first = True
    for i, r in enumerate(e):
        if 'w' in r and '##' in r[2:6]:
            j = r.index('##', 2)
            e[i] = r[:j] + ('#' + mid if first else mid * 2) + r[j + 2:]
            first = False
    return e


K_EXPR = {   # brows (right, left), eye op, mouth
    'neutral':   ('neutral', 'neutral', lambda e: e, 'neutral'),
    'smug':      ('smug_up', 'smug_flat', lambda e: lid(e, 2), 'smirk'),
    'angry':     ('angry', 'angry', lambda e: lid(e, 1), 'angry'),
    'sad':       ('sad', 'sad', lambda e: lid(e, 1), 'sad'),
    'surprised': ('surprised', 'surprised', lambda e: pin_pupils(wide(e, 1)), 'surprised'),
}


def kestrel_raw():
    return place(bust('LEADER_Cheren'), (24, 0, 86, 43), -30, 5)


def kestrel_face():
    """the donor face classified and repainted, before stamps, hair and collar. -> (im, old_hair)"""
    im = kestrel_raw()
    q = im.copy().load(); p = im.load()
    hairc = {CH['B'], CH['D'], CH['F']}
    skin_src = {CH['C'], CH['G'], CH['E'], CH['K'], CH['L'], CH['M']}

    def near_skin(x, y):
        return any(0 <= x + dx < 48 and 0 <= y + dy < 48 and q[x + dx, y + dy] in skin_src
                   for dx in (-1, 0, 1) for dy in (-1, 0, 1))
    features = mat.region((48, 48), rect=(13, 17, 37, 29)).load()      # brows + eyes: stamped later
    old_hair = set()
    for y in range(48):
        for x in range(48):
            c = q[x, y]
            if not c[3] or features[x, y]:
                continue
            if c in hairc or (c == CH['A'] and not near_skin(x, y)):
                old_hair.add((x, y))
    for y in range(48):
        for x in range(48):
            c = q[x, y]
            if not c[3] or (x, y) in old_hair:
                continue
            if features[x, y] or (23 <= x <= 31 and 36 <= y <= 40):
                p[x, y] = SKIN
            elif c == CH['A']:
                p[x, y] = BLACK
            elif c == CH['G']:
                p[x, y] = SKS if (x >= 37 and y >= 28) or y >= 41 else SKIN
            elif c == CH['E']:
                p[x, y] = SKD
            else:
                p[x, y] = SKIN if c in (CH['C'], CH['K'], CH['W']) else c
    return im, old_hair


def kestrel(expr='neutral'):
    br, bl, eyeop, mo = K_EXPR[expr]
    im, old_hair = kestrel_face()
    eye = eyeop(K_EYE)
    im = stamp(im, 29, 17, K_BROW_R[br], KX)
    im = stamp(im, 29, 17, K_BROW_R[bl], KX, mirror=True)
    im = stamp(im, 30, 23, eye, KX)
    im = stamp(im, 30, 23, eye, KX, mirror=True)
    im = stamp(im, 23, 36, K_MOUTH[mo], KX)
    idm = render_locks(K_LOCKS, dome())
    p = im.load()
    for (x, y) in list(old_hair):                     # donor hair: recolour, or forehead skin where the old bangs were
        if (x, y) in idm:
            continue
        if 13 <= x <= 37 and 6 <= y <= 22:
            p[x, y] = SKIN; old_hair.discard((x, y)); continue
        p[x, y] = {CH['B']: K_HAIR[3], CH['D']: K_HAIR[4], CH['F']: K_HAIR[4], CH['A']: K_HAIR[1]}[p[x, y]]
    im = hair_paint(im, idm, old_hair, K_HAIR)
    return kestrel_collar(im)


def kestrel_collar(im):
    """his mother's greatcoat, collar flipped up to the jaw, crimson lining; crimson undershirt at the throat."""
    OT, IT, IB = (3, 31), (14, 38), (20, 48)            # outer top, inner top, inner bottom (left flap)
    L = [(0, 35), OT, IT, IB, (0, 48)]
    R = [(50 - x, y) for (x, y) in L]
    flap = mat.region((48, 48), [L, R]).load()
    p = im.load()
    for y in range(45, 48):
        for x in range(17, 33):
            if not flap[x, y]:
                p[x, y] = K_CRIM[2] if y > 45 else K_CRIM[0]
    for y in range(48):
        for x in range(48):
            if not flap[x, y]:
                continue
            m = (lambda v: (50 - v[0], v[1])) if x >= 25 else (lambda v: v)
            di, ti = seg_d(m(IT), m(IB), x + .5, y + .5)
            dt, _ = seg_d(m(OT), m(IT), x + .5, y + .5)
            if di < 3.8 - 2.2 * ti:                      # lining wedge, widest under the jaw
                c = K_CRIM[1] if di < 1.0 else K_CRIM[2]
                if dt < 1.5:
                    c = K_CRIM[3]
            elif dt < 1.5:
                c = K_COAT[4]                            # the fold catches the light
            elif dt < 2.5:
                c = K_COAT[3]
            else:
                c = K_COAT[2] if y < 44 else K_COAT[1]
            p[x, y] = c
    for y in range(48):
        for x in range(48):
            if flap[x, y] and any(0 <= x + dx < 48 and 0 <= y + dy < 48 and not flap[x + dx, y + dy]
                                  for dx, dy in ((1, 0), (-1, 0), (0, -1))):
                p[x, y] = BLACK
    return im


# ============================================================== DORIAN
# Base face: official B2W2 VS Hilbert (protagonist), a frontal face whose eye-to-mouth spacing is Juno's (13 rows).
# His identity is the cap and the brown hair: both go. Everything above the cap brim is rebuilt: forehead, a silver
# swept-back pompadour with one matinee forehead curl, combed-back greying sides. Age: warm hazel eyes with an
# upper-lid crease and crow's feet, nasolabial lines, a silver pencil moustache. Clothes from his battle sprite (pick S):
# plum velvet coat collar, white silk cravat, red rose.
HB = {'A': H('e8e8f8'), 'B': H('885048'), 'C': H('d05860'), 'D': H('585858'), 'E': H('b8b8d8'), 'F': H('404040'),
      'G': H('583830'), 'H': H('d8a888'), 'I': H('a07040'), 'J': H('f8d8c0'), 'K': H('184870'), 'L': H('1868a0'),
      'M': H('90c8e8')}
D_HAIR = [BLACK, H('6a6888'), H('aaa8c4'), H('dcdce8'), H('fafafe')]      # outline, line, dark, mid, light
D_BROW = H('5c5a78')
D_EYES = [H('3a2010'), H('8a5428'), H('c89058')]     # warm hazel (violet + silver + plum echoed Bede)
D_VEL = [H('1e0618'), H('3c0e34'), H('64205a'), H('8c3a7e'), H('b860a6')]
D_SILK = [H('9690ae'), H('cfcadf'), H('f8f6fc')]
D_ROSE = [H('7a1020'), H('d0304a'), H('ff6a7a'), H('2e5a3a')]
def D_HAIRLINE(x):
    """slight widow's peak at the centre, receded corners, temples running down into short sideburns."""
    d = abs(x + .5 - 25)
    return 14.5 - 1.6 * min(d, 7) / 7 + (max(0, d - 8) ** 1.6) * .55


# Dorian's hair is a sculpted pompadour, so it is built as one silhouette with tone bands and a few swept strand
# curves, not as free locks (locks cracked the roll into an eggshell pattern).
D_SIL = [(14, 25), (10.5, 24.6), (7.2, 22), (5.8, 17), (6.4, 11), (9, 6.6), (12.5, 4.6), (18, 3.6),
         (23, 3.2), (29, 3.1), (32, 3.3), (34, 2.6), (37.6, 2.6), (36.8, 4.1), (39.8, 5.6), (42.4, 8.6), (44, 13),
         (44, 18.5), (42.6, 22.4), (39.8, 24.6), (37.6, 25),
         (36.5, 22), (35.5, 18.5), (33.5, 16), (29.5, 15.2), (25.5, 16.6), (21.5, 15.2), (17.5, 16), (15.5, 18.5),
         (14.6, 22)]
D_STROKES = [   # (Bezier, t0, t1, ramp index): swept up from the hairline and back toward screen left
    ([(33.5, 14.5), (35, 8), (29, 4)], .05, .8, 2),
    ([(28.5, 14), (28.5, 8), (22, 4.5)], .05, .75, 2),
    ([(22, 14), (20, 8.5), (15, 7.5)], .05, .8, 2),
    ([(10, 23.5), (6.8, 17), (10.5, 8)], .1, .85, 2),
    ([(41, 23.5), (43.6, 17), (40.5, 8)], .1, .85, 2),
    ([(31, 15), (31.5, 12), (29, 9.5)], .0, .6, 1),
    ([(25.5, 16), (25, 12.5), (21.5, 10.5)], .0, .55, 1),
    ([(18.5, 16), (17, 13), (13.5, 12)], .0, .6, 1),
]


def dorian_hair_map():
    m = mat.region((48, 48), [[(x + .0, y + .0) for (x, y) in D_SIL]]).load()
    hair = {(x, y) for y in range(48) for x in range(48) if m[x, y]}
    top = {x: min([y for (xx, y) in hair if xx == x] or [99]) for x in range(48)}
    bot = {x: max([y for (xx, y) in hair if xx == x and y < 20] or [-1]) for x in range(48)}
    tone = {}
    for (x, y) in hair:
        t = 3
        if 15 <= x <= 36 and top[x] + 1 <= y <= top[x] + 3:
            t = 4                                             # lit crown of the roll
        if 16 <= x <= 35 and y >= bot[x] - 1 and y >= 12:
            t = 2                                             # underside of the roll over the forehead
        if x <= 9 or x >= 41 or y >= 25:
            t = 2 if y > 10 else t                            # sides and nape fall back into shadow
        tone[(x, y)] = t
    for pts, t0, t1, c in D_STROKES:
        for i in range(61):
            t = t0 + (t1 - t0) * i / 60
            x, y = bez(list(pts), t)
            q = (int(x), int(y))
            if q in tone and tone[q] != 0:
                tone[q] = min(tone[q], c) if tone[q] != 4 else 3
    for (x, y) in hair:                                       # silhouette outline
        if any((x + dx, y + dy) not in hair for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            tone[(x, y)] = 0
    return tone


DX = {'#': BLACK, 'w': EYE_WHITE, 'v': D_EYES[0], 'V': D_EYES[1], 'L': D_EYES[2], 'K': SHINE, 's': SKIN, 'h': SKS,
      'd': SKD, 'g': D_BROW, 'G': H('54526e'), 'm': MOUTH, 'M': MOUTH_D, 'l': LIP, 't': TEETH, 'T': TONGUE}
D_EYE = ["sshhhhss",           # upper-lid crease
         "ssssssss",
         "s#######h",           # crow's foot off the outer corner
         "#wvvvv##",
         "swv##Vw#",
         "swV#KVws",
         "shLLLLhs",
         "sssssss."]
D_BROW_R = {                    # x29-38, y17-21
    'neutral':   ["ssssssssss", "ssssggggss", "sggggggsgs", "ssssssssss", "ssssssssss"],
    'up':        ["ssssggggss", "sggggggsgs", "ssssssssss", "ssssssssss", "ssssssssss"],
    'flat':      ["ssssssssss", "ssssssssss", "sgggggggss", "ssggggggss", "ssssssssss"],
    'angry':     ["ssssssssss", "ssssssgggs", "sssggggggs", "sggggsssss", "ssssssssss"],
    'surprised': ["sssggggsss", "sgggggsggs", "sgssssssss", "ssssssssss", "ssssssssss"],
}
D_MOUTH = {                     # x19-32, y36-41: pencil moustache (upturned tips) + mouth
    'neutral':   ["sgssssssssssgs", "ssGGGGssGGGGss", "ssssssssssssss", "sssssmsssmssss", "ssssssmmmsssss",
                  "ssssssssssssss"],
    'happy':     ["sgssssssssssgs", "ssGGGGssGGGGss", "ssssssssssssss", "ssssmmmmmmmsss", "ssssmttttTmsss",
                  "sssssmTTTmssss"],
    'smug':      ["sssssssssssgss", "sssGGGssGGGGss", "ssssssssssssmd", "sssssssmmmmmss", "ssssssssssssss",
                  "ssssssssssssss"],
    'angry':     ["ssssssssssssss", "sgGGGGssGGGGgs", "ssssssssssssss", "sssssmmmmsssss", "ssssmttttmssss",
                  "sssmMMMMMMmsss"],
    'surprised': ["sgssssssssssgs", "ssGGGGssGGGGss", "ssssssssssssss", "sssssmmmmsssss", "ssssmMMMMmssss",
                  "sssssmTTmsssss"],
}
D_EXPR = {
    'neutral':   ('neutral', 'neutral', lambda e: e, 'neutral'),
    'happy':     ('up', 'up', laugh_eye, 'happy'),
    'smug':      ('up', 'flat', lambda e: lid(e[1:], 1), 'smug'),
    'angry':     ('angry', 'angry', lambda e: lid(e[1:], 1), 'angry'),
    'surprised': ('surprised', 'surprised', lambda e: pin_pupils(wide(e[1:], 1), 'V'), 'surprised'),
}


D_JAW = [(13, 22), (13.5, 33), (15, 37), (18, 40.5), (22, 42.6), (25.5, 43.2), (29, 42.6), (33, 40.5),
         (36, 37), (37.5, 33), (38.5, 22)]


def dorian_raw():
    return place(bust('POKEMONTRAINER_Hilbert'), (39, 14, 89, 64), -41, -2)


def dorian_face():
    im = dorian_raw()
    q = im.copy().load(); p = im.load()
    for y in range(48):
        for x in range(48):
            c = q[x, y]
            if not c[3]:
                continue
            if y <= 23 or (13 <= x <= 37 and 16 <= y <= 33) or (19 <= x <= 32 and 36 <= y <= 40):
                if 14 <= x <= 37 and y >= 11:
                    p[x, y] = SKIN                       # cap brim, old eyes and mouth -> skin (forehead)
                else:
                    p[x, y] = CLEAR
            elif c == HB['J']:
                p[x, y] = SKIN
            elif c == HB['H']:
                p[x, y] = SKS if y >= 39 or x >= 35 else SKIN
            elif c == HB['I']:
                p[x, y] = SKD
            elif c[:3] == (0, 0, 0) and 13 <= x <= 38:
                p[x, y] = BLACK
            else:
                p[x, y] = CLEAR                          # cap, donor hair, jacket, hand
    for y in range(24, 33):                              # close the face edge where his hair used to cover it
        for x in (13, 38):
            if p[x, y][3] == 0 or p[x, y] == SKIN:
                p[x, y] = BLACK
    jaw = mat.region((48, 48), [D_JAW]).load()          # the jaw and chin lost their hair-coloured outline: rebuild
    for y in range(24, 48):
        for x in range(48):
            if not jaw[x, y]:
                p[x, y] = CLEAR
            elif p[x, y][3] == 0 or p[x, y] == BLACK:
                p[x, y] = SKS if y >= 40 or x >= 36 else SKIN
    for y in range(24, 48):
        for x in range(48):
            if jaw[x, y] and any(not jaw[x + dx, y + dy] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                                 if 0 <= x + dx < 48 and 0 <= y + dy < 48):
                p[x, y] = BLACK
    im = mat.patch(im, 10, 24, [".##.", "#ss#", "#hs#", "#hs#", "#ss#", ".#s#", "..#."], DX)   # ears
    im = mat.patch(im, 37, 24, [".##.", "#ss#", "#sh#", "#sh#", "#ss#", "#s#.", ".#.."], DX)
    return im


def dorian(expr='neutral'):
    br, bl, eyeop, mo = D_EXPR[expr]
    im = dorian_face()
    old_hair = set()
    eye = eyeop(D_EYE)
    oy = 24 - (len(eye) - 7)
    im = stamp(im, 29, 17, D_BROW_R[br], DX)
    im = stamp(im, 29, 17, D_BROW_R[bl], DX, mirror=True)
    im = stamp(im, 30, oy, eye, DX)
    im = stamp(im, 30, oy, eye, DX, mirror=True)
    im = stamp(im, 19, 36, D_MOUTH[mo], DX)
    im = stamp(im, 19, 35, ["shssssssssssh."], DX)      # a trace of the nasolabial lines
    p = im.load()
    for (x, y), t in dorian_hair_map().items():
        p[x, y] = D_HAIR[t]
    return dorian_collar(im)


def dorian_collar(im):
    """plum velvet coat collar standing up beside the neck, white silk cravat, a red rose on his left lapel."""
    p = im.load()
    for y in range(41, 48):                               # neck under the jaw in shadow
        for x in range(17, 34):
            if p[x, y][3] == 0:
                p[x, y] = SKS
    OT, IT, IB = (2, 33), (15, 39), (19, 48)
    L = [(0, 36), OT, IT, IB, (0, 48)]
    R = [(50 - x, y) for (x, y) in L]
    coat = mat.region((48, 48), [L, R]).load()
    for y in range(48):
        for x in range(48):
            if not coat[x, y]:
                continue
            m = (lambda v: (50 - v[0], v[1])) if x >= 25 else (lambda v: v)
            di, ti = seg_d(m(IT), m(IB), x + .5, y + .5)
            dt, _ = seg_d(m(OT), m(IT), x + .5, y + .5)
            if dt < 1.5:
                c = D_VEL[4]
            elif di < 1.6:
                c = D_SILK[0]                                     # the silver satin facing
            elif dt < 2.6:
                c = D_VEL[3]
            else:
                c = D_VEL[2] if y < 44 else D_VEL[1]
            p[x, y] = c
    im = mat.patch(im, 18, 43, [           # ascot of white silk with a gold stickpin, under the chin
        "...#wWWWWWWw#...",
        "..#wWWWWyWWWWw#.",
        ".#wWWWWWWwWWWWw#",
        "#wWWWWWWWwWWWWWw",
        "wWWWWWWWWwWWWWWw",
    ], {'w': D_SILK[0], 'W': D_SILK[2], 'y': H('e8c060'), '#': BLACK})
    im = mat.patch(im, 37, 42, [".qq.", "qQQq", "qQqq", ".qq.", "..g."], {'q': D_ROSE[1], 'Q': D_ROSE[2], 'g': D_ROSE[3]})
    p = im.load()
    for y in range(48):
        for x in range(48):
            if coat[x, y] and any(0 <= x + dx < 48 and 0 <= y + dy < 48 and not coat[x + dx, y + dy]
                                  for dx, dy in ((1, 0), (-1, 0), (0, -1))) and p[x, y] in D_VEL + D_SILK:
                p[x, y] = BLACK
    return im


SETS = {'KESTREL': (kestrel, list(K_EXPR)), 'DORIAN': (dorian, list(D_EXPR))}

ALIASES = {('KESTREL', 'smug'): ('happy',)}     # the brief's 'happy/smug' is one face


def export():
    os.makedirs(OUT, exist_ok=True)
    done = []
    for name, (fn, exprs) in SETS.items():
        for e in exprs:
            im = fn(e)
            im.save('%s/%s_%s_48.png' % (OUT, name, e))
            kb.up(im, 2).save('%s/%s_%s.png' % (OUT, name, e))
            done.append('%s_%s' % (name, e))
            for alias in ALIASES.get((name, e), ()):                  # same face under a second engine tag
                kb.up(im, 2).save('%s/%s_%s.png' % (OUT, name, alias))
                done.append('%s_%s (= %s)' % (name, alias, e))
    return done


if __name__ == '__main__':
    print(export())
