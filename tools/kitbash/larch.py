"""Professor Imelda Larch battle fronts (80-px art, 160x160 export). python3 -I tools/kitbash/larch.py [variant ...]
Concept: the woman who lit up the region and thinks she is killing it; gruff, guilty, kind; holds out a mug of
disgusting kelp tea like a peace offering. Oilskin mustard + slate; a rope-thick grey braid; glasses on a chain.
  body : sd veteranf-gen6 (XY Veteran F: knee coat, scarf, arm held out)  -> mustard oilskin, slate stole and trousers
  head : sd madame-gen6 (XY Madame class, older face)                       -> grey hair, mouth set flat, hand-set brows
  hand : braid (repeating 3-px plait), kelp-tea mug with steam, reading glasses on a chain
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, mat, show
from mat import H, CLEAR, BLACK
from PIL import Image

OUT = kb.WORK + '/passes'
NAME, SHEET = 'LARCH', '20_larch.png'
TITLE = ('PROFESSOR IMELDA LARCH - 56, ex-Meridian chief engineer. Battle front kitbash (80-px art, file 160x160). Concept: gruff, guilty '
         'and kind, holding out a mug of disgusting kelp tea. Oilskin mustard + slate, a rope-thick grey braid, glasses on a chain.')


def sd(n):
    return show.get_native('sd:' + n)[0]


COAT = {H('3d6393'): H('c89a30'), H('294464'): H('9a7020'), H('13222d'): H('5a3e10'), H('5e86ba'): H('ecc65a'),
        H('e25565'): H('7a8898'), H('863c4f'): H('4a5664'), H('ef5a3f'): H('a4b2c0'), H('54373b'): H('3a4250'),
        H('7c495a'): H('4a5664'), H('5d666c'): H('3a4250'), H('848e95'): H('5a6676')}
HAIR = {H('ffffff'): H('d6d6dc'), H('e1e0e3'): H('b6b6c0'), H('cecece'): H('a6a6b2'), H('a8a8b9'): H('888896'),
        H('6b7275'): H('5a5e6a')}
X = {'k': BLACK, 'a': H('5a5e6a'), 'b': H('888896'), 'c': H('b6b6c0'), 'd': H('d6d6dc'), 's': H('ffd7be'), 'S': H('dfa67c'),
     'm': H('7b4242'), 'w': H('f2f2f6'), 'W': H('b8bcc8'), 'g': H('3e7a3a'), 'G': H('6aa04a'), 'h': H('2a4a22'),
     'v': H('e8eef4'), 'V': H('c0c8d0'), 'y': H('c8a040'), 'Y': H('f0d070'), 'o': H('6a5a3a')}


def head():
    m = sd('madame-gen6')
    h = mat.keep(m, mat.region(m.size, [[(29, 5), (48, 5), (48, 24), (40, 25), (30, 24)]]))
    p = h.load()
    for y in range(80):
        for x in range(80):
            if p[x, y][3] and (x >= 46 and y >= 20):
                p[x, y] = CLEAR                      # her hand / ball at the chin
    h = mat.recolour(h, HAIR)
    return h


def braid(im, pts):
    """a plait: alternating 3x2 segments, lit on the left, along pts (top of each segment)."""
    for i, (x, y) in enumerate(pts):
        im = mat.patch(im, x - 1, y, (['kcdk', 'kbck'] if i % 2 == 0 else ['kdck', 'kabk']), X)
    return im


def mug(im, x, y):
    # enamel mug of murky green kelp tea, a strand of kelp over the rim, steam rising
    im = mat.patch(im, x, y - 6, ['.v..v', 'v..v.', '.v..v', '..v..'], X)
    return mat.patch(im, x - 1, y - 2, ['..h.....',
                                        'kkgkkkk.',
                                        'kGggGgk.',
                                        'kwwwwWkk',
                                        'kwwwwWk.k',
                                        'kwwwwWkk',
                                        'kWWWWWk.',
                                        '.kkkkk..'], X)


def build(var='A'):
    v = sd('veteranf-gen6')
    v = mat.erase(v, mat.region(v.size, [[(28, 0), (50, 0), (50, 15), (45, 21), (34, 21), (28, 15)]]))
    legs = mat.region(v.size, rect=(0, 53, 79, 79))
    v = mat.recolour(v, {H('3d6393'): H('5a6676'), H('294464'): H('3a4250'), H('13222d'): H('1e232c'), H('5e86ba'): H('7a8898')}, legs)
    v = mat.recolour(v, COAT)
    # the held-out hand: ball away
    p = v.load()
    for y in range(32, 46):
        for x in range(58, 70):
            if p[x, y][3] and p[x, y] not in (H('ffd7be'), H('dfa67c'), H('be7c62'), BLACK):
                p[x, y] = CLEAR
    t = Image.new('RGBA', (80, 80), CLEAR); t.paste(head(), (2, -4)); v.alpha_composite(t)
    out = v
    # gruff: flat mouth, low brows
    out = mat.patch(out, 36, 15, ['sssss', 'sssss', 'smmms', 'sssS.'], X)
    out = mat.patch(out, 35, 11, ['a...a'], X)
    # rope-thick grey braid over her right shoulder down to the waist
    out = braid(out, [(31, 18), (30, 20), (30, 22), (29, 24), (29, 26), (29, 28), (29, 30), (29, 32), (30, 34), (30, 36), (30, 38)])
    out = mat.patch(out, 28, 40, ['.kyk', 'kbak', '.kk.'], X)            # mustard tie at the braid's end
    # reading glasses dangling on a chain
    out = mat.patch(out, 38, 22, ['o....o', '.o..o.', '..oo..', 'kk.kk.', 'Vk.Vk.'], X)
    out = mug(out, 60, 34)
    return out


VARIANTS = [('A', 'A: "Drink your tea." Holding out a steaming mug of murky kelp tea like a peace offering; mustard oilskin knee coat '
                  'with a slate stole flying, rope-thick grey braid over the shoulder, glasses on a chain, mouth set flat.')]
PICK = 'A'
REFS = [('sd:juniper', 'Juniper (official BW professor)'), ('sd:bertha', 'Bertha (official)'), ('sd:veteranf', 'Veteran F (official BW)'),
        ('reborn:093', 'Reborn front (Julia)')]
DONORS = [('sd:veteranf-gen6', 'veteranf-gen6: body, knee coat, stole, held-out arm'), ('sd:madame-gen6', 'madame-gen6: older head, hair repainted grey')]
NOTE = 'Hand pixels: the braid (repeating plait), mug + kelp + steam, glasses and chain, flat mouth and brows.'

if __name__ == '__main__':
    vs = sys.argv[1:] or ['A']
    ims = [build(v) for v in vs]
    row = Image.new('RGBA', (len(ims) * 330, 330), (40, 40, 48, 255))
    for i, im in enumerate(ims):
        im.save(OUT + '/lar_%s.png' % vs[i])
        row.paste(kb.up(kb.on_bg(im, (150, 160, 170, 255)), 4), (i * 330, 0))
    row.save('/tmp/lar.png')
