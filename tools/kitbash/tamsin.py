"""Tamsin Loom battle fronts (80-px art, 160x160 export). python3 -I tools/kitbash/tamsin.py [variant ...]
Concept: a 19-year-old who inherited a legend and a loom; she hides inside her late grandmother's moth-wing shawl.
Cream + moth rose-brown; the shawl's two big eyespots are the silhouette.
  A body : sd pokefanf (Poke Fan F class, shy hug)          -> cream smock; plush recoloured as a Sewaddle she sewed herself
  wings  : reborn Battlers/dustox right wing pair, mirrored  -> moth rose-brown shawl with two cream-and-umber eyespots
  B body : sd pokemonrangerf (arm thrust forward)            -> ferocious: a giant needle held like a rapier, shawl flared
  hand   : messy bun stabbed with two needles, yellow measuring tape round the neck, worried/angry faces
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, mat, show
from mat import H, CLEAR, BLACK
from PIL import Image

OUT = kb.WORK + '/passes'
B = '/home/claude/ref/games/reborn/Graphics/Battlers/'
NAME, SHEET = 'TAMSIN', '19_tamsin.png'
TITLE = ('TAMSIN LOOM - Gym 2 Warden (Bug), 19, anxious weaver. Battle front kitbash (80-px art, file 160x160). Concept: she hides inside '
         'her late grandmother\'s moth-wing shawl. Cream + moth rose-brown; two big eyespots; measuring tape, needles in the bun.')


def sd(n):
    return show.get_native('sd:' + n)[0]


X = {'k': BLACK, 'y': H('f0c838'), 'Y': H('b08a20'), 'n': H('3a3440'), 'w': H('e8e8f4'), 'W': H('a8a8bc'),
     's': H('f8d0b8'), 'S': H('d8a078'), 'm': H('784858'), 'c': H('b8e4f8'), 'C': H('ffffff'), 'i': H('2a2a4a'),
     'h': H('5a2e2a'), 'H': H('7a443a'), 'e': H('3a1c1a')}


def wings():
    d = kb.native(kb.load(B + 'dustox.png').crop((0, 0, 192, 192)))[0]
    keepc = [H('6e8f4e'), H('9ccd6a'), H('8bb45a'), H('acee94'), H('d53962'), H('ff6a5a'), H('181818')]
    r = mat.keep(d, mat.region(d.size, [[(52, 44), (80, 44), (80, 80), (50, 80), (50, 60)]]))
    p = r.load()
    for y in range(96):
        for x in range(96):
            if p[x, y][3] and p[x, y] not in keepc:
                p[x, y] = CLEAR
    r = mat.clean_orphans(r)
    r = mat.recolour(r, {H('6e8f4e'): H('7a4e42'), H('8bb45a'): H('9e6a54'), H('9ccd6a'): H('c08e70'), H('acee94'): H('e0bc98'),
                         H('d53962'): H('3a2420'), H('ff6a5a'): H('f6e8cc'), H('181818'): H('2a1614')})
    pair = Image.new('RGBA', (96, 96), CLEAR)
    pair.alpha_composite(r)
    pair.alpha_composite(mat.flip(r), (-2, 0))            # mirrored wing on the other side of x=47
    return pair.crop((18, 40, 82, 82))                    # 64 x 42, centre at x=32


SMOCK = {H('d890e8'): H('f2e8d6'), H('a86890'): H('cbb89c'), H('e0b850'): H('e6d6ba'), H('f8e010'): H('f2e8d6'),
         H('f08000'): H('b89a7a'), H('b87860'): H('a07e64')}


def head_edits(im, ox, oy, mood='worried'):
    P = lambda x, y, rows: mat.patch(im, x + ox, y + oy, rows, X)
    # messy bun at the back of the head, two needles stabbed through it
    im = P(53, 9, ['..w....', '...W.kk', '.kkWhHk', 'khHhhHk', 'khHHhk.', '.kkkk..'])
    im = P(49, 7, ['W', '.W', '..'])
    return im


def body_a():
    b = sd('pokefanf')
    b = mat.recolour(b, {H('d890e8'): H('f2e8d6'), H('a86890'): H('cbb89c')})
    b = mat.recolour(b, SMOCK, mat.region(b.size, rect=(36, 34, 70, 70)))
    return b


def head_pf():
    b = sd('pokefanf')
    h = mat.keep(b, mat.region(b.size, [[(38, 10), (62, 10), (62, 34), (50, 35), (38, 30)]]))
    plush = [H(c) for c in ('68c038', '487038', '284820', 'f8e010', 'e0b850', 'f08000', 'f8f8f8')]
    p = h.load()
    for y in range(80):
        for x in range(80):
            if p[x, y] in plush or (x < 43 and p[x, y] == BLACK and y > 22):
                p[x, y] = CLEAR
    return mat.clean_orphans(h)


RANGER = {H('d85040'): H('f2e8d6'), H('a83820'): H('cbb89c'), H('703020'): H('8e7258'), H('884838'): H('8e7258'),
          H('182030'): H('3a2420'), H('304060'): H('6a4438'), H('583848'): H('4a2c28'),
          H('b86830'): H('784858'), H('502810'): H('502838'), H('301808'): H('2a1420')}


def body_b():
    r = sd('pokemonrangerf')
    r = mat.erase(r, mat.region(r.size, [[(27, 9), (53, 9), (53, 22), (47, 31), (31, 31), (27, 24)]]))
    r = mat.recolour(r, RANGER)
    t = Image.new('RGBA', (80, 80), CLEAR); t.paste(head_pf(), (-8, -2))
    return mat.under(t, r, 0, 0) if False else _over(r, t)


def _over(a, b):
    a = a.copy(); a.alpha_composite(b); return a


def needle(im, x0, y0, x1, y1):
    n = max(abs(x1 - x0), abs(y1 - y0)); p = im.load()
    for i in range(n + 1):
        x = round(x0 + (x1 - x0) * i / n); y = round(y0 + (y1 - y0) * i / n)
        p[x, y] = X['w']
        if 0 <= y + 1 < 80:
            p[x, y + 1] = X['W']
    return im


def tape(im, pts):
    """yellow measuring tape: a 1-px ribbon along pts with black tick marks every 3 px."""
    p = im.load()
    for i, (x, y) in enumerate(pts):
        p[x, y] = X['n'] if i % 3 == 0 else X['y']
    return im


def build(var='A'):
    if var == 'A':
        fig = body_a()
        out = mat.under(fig, wings(), 14, 24)
        out = head_edits(out, 0, 0)
        # tape over the shoulders, hanging down both sides of the smock
        out = tape(out, [(45, 35), (45, 36), (44, 37), (44, 38), (44, 39), (44, 40), (44, 41), (44, 42), (45, 43)])
        out = tape(out, [(52, 35), (53, 36), (53, 37), (53, 38), (53, 39), (54, 40), (54, 41)])
        # worried face: inner brows up, small wobbly mouth, a sweat drop
        out = mat.patch(out, 44, 22, ['k...', '.k..'], X)
        out = mat.patch(out, 47, 28, ['m.m', '.m.'], X)
        out = mat.patch(out, 58, 18, ['.C', 'cc', '.c'], X)
        return out
    if var == 'B':
        fig = body_b()
        out = mat.under(fig, wings(), 8, 16)
        out = head_edits(out, -8, -2)
        out = needle(out, 1, 27, 15, 32)                               # a weaver's needle held like a rapier
        out = mat.patch(out, 13, 30, ['.WW', 'W.W', '.WW'], X)         # the needle's eye at her fist
        out = mat.patch(out, 10, 34, ['q..', '.q.', '..q', '.q.', 'q..'], {'q': H('d8506a')})  # silk thread trailing
        out = tape(out, [(37, 31), (37, 32), (36, 33), (36, 34), (36, 35), (36, 36)])
        out = tape(out, [(44, 31), (45, 32), (45, 33), (45, 34), (46, 35)])
        out = mat.patch(out, 36, 20, ['kk..', '.kk.'], X)              # brows down: ferocious
        out = mat.patch(out, 39, 26, ['mmm', 'mqm'], {'m': H('784858'), 'q': H('c04050')})
        return out
    return build('A')


VARIANTS = [('A', 'A: sorry, sorry. Hugging the Sewaddle plush she sewed, hiding inside Granny Loom\'s moth-wing shawl '
                  '(two eyespots), measuring tape round her neck, needles through a messy bun, worried brows and a sweat drop.'),
            ('B', 'B: "Don\'t you dare tear it." Battle stance, the shawl flared, a weaver\'s needle thrust like a rapier with '
                  'red silk trailing. Ranger class body (stance), same head.')]
PICK = 'A'
REFS = [('sd:burgh', 'Burgh (official BW Bug leader)'), ('sd:shauntal', 'Shauntal (official BW)'), ('sd:bianca', 'Bianca (official BW)'),
        ('reborn:093', 'Reborn front (Julia)')]
DONORS = [('sd:pokefanf', 'pokefanf: body, shy hug, head; smock repainted cream'), ('sd:pokemonrangerf', 'pokemonrangerf: B body (stance, thrust arm)'), ('B:dustox', 'Reborn battler dustox: right wing pair, mirrored, repainted moth rose-brown')]
NOTE = 'Hand pixels: bun and needles, measuring tape, worried brows, mouth, sweat drop.'

if __name__ == '__main__':
    vs = sys.argv[1:] or ['A']
    ims = [build(v) for v in vs]
    row = Image.new('RGBA', (len(ims) * 330, 330), (40, 40, 48, 255))
    for i, im in enumerate(ims):
        im.save(OUT + '/tam_%s.png' % vs[i])
        row.paste(kb.up(kb.on_bg(im, (150, 160, 170, 255)), 4), (i * 330, 0))
    row.save('/tmp/tam.png')
