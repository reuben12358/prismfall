"""Kestrel Vane battle fronts (80-px art, 160x160 export). python3 -I tools/kitbash/kestrel.py [variant ...]
Concept: a broke 16-year-old drowning in his dead mother's greatcoat, her blade's child (Honedge) at his side.
  body/coat   : sd veteran (BW Veteran class): long greatcoat, raised collar; teen head on it = the coat is a size too big
  head        : sd acetrainer (BW Ace Trainer class): long fringe over one eye; hair repainted slate-black, scowl hand-set
  Honedge     : reborn Battlers/honedge (96-px native = front density): sword + cloth, sheath rings dropped
  sponsor jkt : sd kieran-champion jacket (variant C), repainted Meridian ivory/cobalt with a gold sunburst
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, mat, show
from mat import H, CLEAR, BLACK
from PIL import Image

OUT = kb.WORK + '/passes'
NAME, SHEET = 'KESTREL', '17_kestrel.png'
TITLE = ('KESTREL VANE - battle front kitbash (80-px art, file 160x160, same as Juno). Concept: a broke 16-year-old drowning in '
         'his dead mother\'s greatcoat, with her blade\'s child (Honedge) at his side. Black + crimson, split coat tails.')
VARIANTS = [('A', "A: the inheritance. Teen head on a grown man's greatcoat (a size too big), sleeves past the hands, collar up, "
                  "split crimson-lined tails; Honedge hangs from his hand, its cloth wound across the coat. One-sided sneer."),
            ('B', 'B: the tic. Angry, two fingers jabbing his own sternum, the empty sleeve flung out, Honedge riding '
                  'his back with the hilt over the shoulder.'),
            ('C', 'C: K5+ Meridian-sponsored. Ivory/cobalt sponsor jacket with the gold sunburst, the Resonance Gauntlet '
                  'on the raised fist; he still wears the crimson feather pin.')]
PICK = 'A'
REFS = [('sd:hugh', 'Hugh (official BW2 rival)'), ('sd:silver', 'Silver (official rival)'), ('sd:n', 'N (official BW)'),
        ('reborn:093', 'Reborn front (Julia)')]
DONORS = [('sd:veteran', 'veteran: body, greatcoat, raised collar (A, B)'), ('sd:acetrainer', 'acetrainer: head, fringe over one eye; hair repainted, mouth/brow hand-set'),
          ('B:honedge', 'Reborn battler honedge: sword + cloth (sheath dropped)'), ('sd:leaguestaff', 'leaguestaff: body for C, jacket repainted, fist -> gauntlet')]
NOTE = ('Hand pixels: mouths, brow, crimson collar lining and feather pin, split tails (polygons in the coat ramp), B\'s folded forearm '
        'and sleeve end, C\'s gauntlet core and sunburst. Who does it look like? Not a named character: the donors are trainer classes.')
B = '/home/claude/ref/games/reborn/Graphics/Battlers/'
c4 = lambda *t: tuple(t) + (255,)


def sd(n):
    return show.get_native('sd:' + n)[0]


# palettes
HAIR_SRC = [H('202040'), H('303858'), H('506080'), H('407898'), H('50a8d8')]
HAIR = [H('08080e'), H('12131c'), H('1e2130'), H('2c3146'), H('434c68')]
COAT_SRC = [H('181818'), H('303038'), H('383028'), H('505050'), H('504838'), H('604848')]
COAT = [H('0f0f14'), H('24232e'), H('2a2733'), H('3d3c4c'), H('443f50'), H('5a3040')]
CRIMSON = {H('784040'): H('6e1020'), H('b84848'): H('b0202e'), H('604848'): H('4a0e1a')}
BRASS = {H('c8a840'): H('5a5866')}           # coat buttons: dull pewter, not gold
SKIN = [H('f8d0b8'), H('d8a078'), H('b08058'), H('b87860')]


def head():
    a = sd('acetrainer')
    reg = mat.region(a.size, [[(26, 0), (44, 0), (44, 18), (39, 18), (38, 22), (30, 22), (26, 18)]])
    h = mat.keep(a, reg)
    h = mat.recolour(h, dict(zip(HAIR_SRC, HAIR)))
    return h


FX = {'k': BLACK, 's': H('f8d0b8'), 'S': H('d8a078'), 'm': H('b08058'), 'n': H('784858'), 'r': H('b0202e'),
      'R': H('6e1020'), 'q': H('e04858')}


def face(im, mood='brood'):
    return face_at(im, 0, 0, mood)


def face_at(im, dx, dy, mood='brood'):
    p = im.load()
    for y in range(16 + dy, 18 + dy):
        for x in range(41 + dx, 47 + dx):
            if p[x, y][3] and p[x, y] != BLACK:
                p[x, y] = FX['s']
    if mood == 'brood':
        im = mat.patch(im, 42 + dx, 16 + dy, ['...n', 'nnn.'], FX)        # one-sided sneer
        im = mat.patch(im, 38 + dx, 11 + dy, ['kkk'], FX)                 # brow pressed onto the visible eye
    elif mood == 'angry':
        im = mat.patch(im, 42 + dx, 16 + dy, ['nnnn', 'nqqn'], FX)        # bared, shouting
        im = mat.patch(im, 38 + dx, 11 + dy, ['kk..', '.kk.'], FX)
    return im


def body():
    v = sd('veteran')
    v = mat.erase(v, mat.region(v.size, [[(30, 0), (54, 0), (54, 16), (50, 21), (38, 21), (34, 16)]]))
    v = mat.recolour(v, dict(zip(COAT_SRC, COAT)))
    v = mat.recolour(v, CRIMSON); v = mat.recolour(v, BRASS)
    return v


def honedge():
    n = kb.native(kb.load(B + 'honedge.png').crop((0, 0, 192, 192)))[0]
    sheath = [H('604536'), H('3d2d27'), H('976d43'), H('c0985c')]
    # drop the wooden sheath rings (right of the cloth), keep sword + cloth
    p = n.load()
    for y in range(96):
        for x in range(96):
            c = p[x, y]
            if c[3] and ((x >= 40 and y >= 52 and c in sheath + [H('101010')] and not (54 <= x <= 70 and y <= 72 and c == H('101010'))) or x > 72):
                p[x, y] = CLEAR
    return mat.clean_orphans(n)


K = {'k': BLACK, 'a': COAT[0], 'b': COAT[1], 'c': COAT[3], 'd': COAT[4], 'r': H('b0202e'), 'R': H('6e1020'),
     'q': H('e04858'), 's': H('f8d0b8'), 'S': H('d8a078')}


def coat_details(im):
    p = im.load()
    # sleeve past the hanging hand
    for y in range(40, 50):
        for x in range(46, 60):
            if p[x, y] in [H(c) for c in ('f8d0b8', 'd8a078', 'b08058')]:
                p[x, y] = COAT[1]
    # crimson: shirt in the collar's V, lining of the flipped-up collar, feather pin
    im = mat.patch(im, 36, 18, ['R', 'r', 'r'], K)
    im = mat.patch(im, 51, 18, ['R', 'r', 'R'], K)
    im = mat.patch(im, 50, 26, ['..q', '.rq', 'rR.', 'R..'], K)
    # split tails flaring behind the legs, like a kestrel's tail (polygons, coat ramp, crimson lining underneath)
    tails = Image.new('RGBA', (80, 80), CLEAR)
    for poly, lin in [([(30, 52), (30, 67), (20, 76), (23, 66)], -1), ([(53, 52), (53, 67), (63, 76), (60, 66)], 1)]:
        reg = mat.region((80, 80), [poly]).load(); tp = tails.load()
        for y in range(80):
            for x in range(80):
                if reg[x, y]:
                    tp[x, y] = COAT[1]
        for y in range(80):
            for x in range(80):
                if reg[x, y]:
                    below = reg[x, y + 1] if y < 79 else 0
                    side = reg[x + lin, y] if 0 <= x + lin < 80 else 0
                    if not below:
                        tp[x, y] = H('6e1020')
                    elif not side:
                        tp[x, y] = COAT[3]
    tails = mat.outline_outer(tails, BLACK)
    tp = tails.load()
    for y in range(80):
        for x in range(80):
            if tp[x, y] == BLACK:
                continue
    return mat.under(im, tails, 0, 0)


TAP = ['.ss...........',
       'kssk..........',
       '.kSkkk........',
       '..kccckk......',
       '..kbccccdk....',
       '...kbbccccdkk.',
       '....kabbbcccck',
       '.....kaabbbcck',
       '......kkaabbck',
       '........kkabck',
       '..........kkk.']


def tap_arm(im):
    # forearm folded across the chest, two fingers out of the sleeve on the sternum; old forearm removed
    p = im.load()
    for y in range(38, 54):
        for x in range(51, 62):
            if p[x, y][3]:
                p[x, y] = BLACK if x == 51 else CLEAR
    for y in range(38, 54):
        if p[50, y][3] and p[50, y] != BLACK:
            p[50, y] = COAT[3]
    return mat.patch(im, 43, 27, TAP, K)


def sleeve_end(im):
    # the outstretched arm: ball and hand gone, the sleeve hangs past the hand
    p = im.load()
    for y in range(30, 46):
        for x in range(14, 30):
            if p[x, y][3]:
                p[x, y] = CLEAR
    return mat.patch(im, 21, 31, ['....kkkkk',
                                  '..kkbbbck',
                                  '.kbbbbcck',
                                  'kabbbbcck',
                                  'kaabbbbck',
                                  'kkaabbbk.',
                                  '.kkaaakk.',
                                  '...kkkk..'], K)


SPONSOR = {H('ffffff'): H('f6f1e2'), H('bdbdc5'): H('d6cdb4'), H('bdb7bf'): H('d6cdb4'), H('83838b'): H('9c937c'),
           H('fd1956'): H('3c64c8'), H('df515a'): H('3c64c8'), H('cd5a5a'): H('2848a8'), H('96072c'): H('182c70'),
           H('7b4141'): H('5a1626'), H('106fb4'): H('e8b030'), H('373740'): H('17161c'), H('55595a'): H('2c2b36')}
GAUNT = {H('ffd5bd'): H('8aa2d8'), H('dea47b'): H('3c64c8'), H('b88060'): H('2848a8'), H('bd7b62'): H('182c70'),
         H('7b4141'): H('101830'), H('957d69'): H('182c70'), H('a86a31'): H('e8b030'), H('cf8f34'): H('e8b030')}


def sponsored():
    b = sd('leaguestaff')
    b = mat.erase(b, mat.region(b.size, [[(26, 0), (52, 0), (52, 20), (46, 23), (34, 23), (28, 20)]]))
    b = mat.recolour(b, SPONSOR)
    b = mat.recolour(b, GAUNT, mat.region(b.size, rect=(50, 22, 64, 36)))     # raised fist -> Resonance Gauntlet
    b = mat.patch(b, 55, 26, ['.y.', 'yty', '.y.'], {'y': H('e8b030'), 't': H('7ff0e0')})
    # gold Meridian sunburst on the chest, his crimson feather pin kept on the other side
    b = mat.patch(b, 41, 29, ['y.y', '.Y.', 'y.y'], {'y': H('e8b030'), 'Y': H('fff0a0')})
    b = mat.patch(b, 33, 27, ['.q', 'rq', 'R.'], K)
    hd = head()
    t = Image.new('RGBA', (80, 80), CLEAR); t.paste(hd, (6, 2)); b.alpha_composite(t)
    return b


def build(var='A'):
    if var == 'C':
        out = sponsored()
        return face_at(out, -4, 3, 'brood')
    fig = body()
    hd = head()
    t = Image.new('RGBA', (80, 80), CLEAR); t.paste(hd, (10, -1)); fig.alpha_composite(t)
    out = coat_details(face(fig, 'angry' if var == 'B' else 'brood'))
    if var == 'A':
        hn = honedge()
        t = Image.new('RGBA', (80, 80), CLEAR); t.paste(hn, (-18, -6)); out.alpha_composite(t)
    if var == 'B':
        out = sleeve_end(tap_arm(out))
        hn = mat.flip(honedge())
        hp = hn.load()
        for y in range(96):
            for x in range(96):
                if x < 46 and hp[x, y][3]:
                    hp[x, y] = CLEAR          # the cloth stays hidden behind the coat
        out = mat.under(out, mat.clean_orphans(hn), -2, -18)
    return out


if __name__ == '__main__':
    vs = sys.argv[1:] or ['A']
    ims = [build(v) for v in vs]
    for v, im in zip(vs, ims):
        im.save(OUT + '/kes_%s.png' % v)
    row = Image.new('RGBA', (len(ims) * 330, 330), (40, 40, 48, 255))
    for i, im in enumerate(ims):
        row.paste(kb.up(kb.on_bg(im, (150, 160, 170, 255)), 4), (i * 330, 0))
    row.save('/tmp/kes.png')
