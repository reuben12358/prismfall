"""Juno portraits, PASS 5: composite A's look (auburn hair, tilted blossom wreath, big bloom at her left temple,
sheer veil, green eyes, freckles) rebuilt on a Rejuvenation VS-bust face so the shading and line quality match the
Rejuvenation/Desolation dialogue faces.  48-px art -> 96x96.
  face/eyes/fringe/collar : RJ vsTrainer150 (young girl, big eyes, 3/4 tilt)
  hair volume             : RJ vsPlayer6_2 (auburn curls; its ramp is Juno's hair ramp)
  big bloom               : RJ vsTrainer143 (Flora's flower) repainted Bride-Tree white/pink
  wreath blossoms+leaves  : RJ vsTrainer171 (pink blossoms in her braid)
  veil                    : RJ vsTrainer180 cloth bow (white folds), made sheer
  expressions             : mouths/brows hand-set in the base palette, shapes after RJ vsTrainer159 (open beam),
                            vsTrainer150 (O), vsTrainer180_1 (worried), Desolation Faces 02c (closed eye)
python3 -I tools/kitbash/juno_portraits_p5.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, mat
from mat import H, CLEAR, BLACK
from PIL import Image

RJ = '/home/claude/ref/games/rejuvenation/Graphics/Transitions/'
DSF = '/home/claude/ref/games/desolation/Graphics/Faces/'
J, P = kb.WORK + '/juno', kb.WORK + '/passes'
c4 = lambda *t: tuple(t) + (255,)


def nat(path):
    return kb.native(kb.load(path))[0]


def bust(n):
    return nat(RJ + n + '.png')


# ---------------------------------------------------------------- palettes
# T150 base colours
SK = {'l': H('ffead6'), 'm': H('edc6af'), 's': H('c99085'), 'd': H('995050')}
HAIR_T150 = [H('100c0f'), H('1a1418'), H('251e21'), H('332b2e'), H('453d3f')]
# Juno hair: vsPlayer6_2's auburn ramp pushed a little toward her battle sprite's orange (c8582e)
HAIR = [H('3a0f16'), H('6a1a1c'), H('8e3226'), H('b44a2e'), H('d8743e')]
HAIR_HI = H('f0a060')
EYE_T150 = {H('202230'): H('0e3a2a'), H('343a48'): H('1f6a40'), H('4d5c63'): H('4fa05a')}
EYE_HI = H('9ad88a')
BOW = [H('7e1c39'), H('ac273e'), H('f23333')]
PINK = {H('7e1c39'): H('a03c5c'), H('ac273e'): H('d86a8a'), H('f23333'): H('f4a6bc')}
MOUTH = {'o': H('42112a'), 'O': H('6c1449'), 'r': H('8a305c'), 't': H('a84b6f'), 'w': H('ffffff'), 'W': H('c0c1e7'),
         'k': BLACK, 'l': SK['l'], 'm': SK['m'], 's': SK['s'], 'd': SK['d'], 'h': H('100c0f')}
FRECK = H('d8a088')

WIN = (36, 3)          # crop window in T150 native coords (48x48)


def face_base():
    b = bust('vsTrainer150')
    # erase the raised arm (right of x=84) and anything outside the head column
    b = mat.erase(b, mat.region(b.size, rect=(84, 0, 127, 63)))
    b = mat.erase(b, mat.region(b.size, rect=(0, 0, 33, 63)))
    # hair -> auburn
    b = mat.recolour(b, dict(zip(HAIR_T150, HAIR)), mat.region(b.size, rect=(34, 0, 90, 56)))
    # eyes -> green
    b = mat.recolour(b, EYE_T150, mat.region(b.size, rect=(48, 22, 80, 34)))
    # bow + collar ribbon -> pink
    bowr = mat.region(b.size, rect=(68, 0, 90, 26))
    b = mat.erase(b, mat.mask_and(bowr, mat.colour_mask(b, BOW + [BLACK])))
    b = mat.recolour(b, PINK)
    return b


def win(im):
    return im.crop((WIN[0], WIN[1], WIN[0] + 48, WIN[1] + 48))


BLOOM_MAP = {H('f98e50'): H('fff6f8'), H('f3934e'): H('fff6f8'), H('ea6e3e'): H('fde0e8'), H('de6a3a'): H('fde0e8'),
             H('cc4745'): H('f4a6bc'), H('bf3735'): H('e888a4'), H('961527'): H('c85a7c'), H('720b23'): H('8a2a4c'),
             H('ffd470'): H('ffe08a'), BLACK: H('5a1830')}
BLOOM_SRC = [H(c) for c in ['f98e50', 'cc4745', '720b23', '961527', 'f3934e', 'ea6e3e', 'de6a3a', 'bf3735', 'ffd470', '000000']]


def bloom():
    f = bust('vsTrainer143').crop((40, 0, 80, 36)); p = f.load()
    for y in range(f.size[1]):
        for x in range(f.size[0]):
            if p[x, y] not in BLOOM_SRC or (y > 20 and x > 18) or x > 33 or y > 30:
                p[x, y] = CLEAR
    f = mat.recolour(f, BLOOM_MAP)
    return mat.clean_orphans(f)


# blossom shapes (hand, ~5 px), shaded like the bloom
BL = {'o': H('8a2a4c'), 'p': H('e888a4'), 'q': H('f4a6bc'), 'w': H('fff6f8'), 'v': H('fde0e8'), 'y': H('ffe08a'), 'Y': H('e8a848'),
      'g': H('1e4a2c'), 'G': H('3f7a3a'), 'L': H('71ab5a'), 'h': H('a8d47a')}
B5 = ['.oo.oo.', 'owwvwqo', 'owvyvqo', '.vyYyp.', 'oqvyqpo', 'oqqpppo', '.oo.oo.']
B4 = ['.oo.o', 'owvqo', 'ovyYo', 'oqqpo', '.ooo.']
B3 = ['.o.', 'owo', 'opo', '.o.']
LEAF_R = ['..ggg', '.gLhg', 'gLLg.', 'gGg..', '.g...']
LEAF_L = [r[::-1] for r in LEAF_R]


def wreath(im, items):
    for kind, x, y in items:
        im = mat.patch(im, x, y, {'5': B5, '4': B4, '3': B3, 'r': LEAF_R, 'l': LEAF_L}[kind], BL)
    return im


BLOOM_AT = (19, -4)
CURLS = (-4, 14)
WREATH = [('l', 3, 16), ('4', 5, 12), ('r', 9, 11), ('5', 11, 7), ('l', 16, 7), ('r', 17, 3), ('3', 19, 3),
          ('4', 39, 25), ('l', 41, 29), ('3', 43, 32)]


MOUTH_COLS = [H(c) for c in ['42112a', '6c1449', '8a305c', 'a84b6f', '7e1c39', '100c0f', '000000', 'c0c1e7', 'ffffff']]
T159_MAP = {H('ffdec6'): SK['l'], H('e7b594'): SK['m'], H('c78170'): SK['s'], H('7b3c3a'): H('7e2a34'),
            H('6c1449'): H('6c1449'), H('9b4865'): H('a84b6f'), H('ffffff'): H('ffffff'), H('c1cbd5'): H('c0c1e7'),
            H('110f19'): H('42112a'), H('1d1929'): H('42112a')}


def clear_mouth(im, box=(24, 33, 35, 44)):
    p = im.load()
    for y in range(box[1], box[3]):
        for x in range(box[0], box[2]):
            if p[x, y][3] and p[x, y] in MOUTH_COLS:
                p[x, y] = SK['l']
    return im


def t159_mouth():
    m = bust('vsTrainer159').crop((56, 35, 69, 45)); p = m.load()
    for y in range(m.size[1]):
        for x in range(m.size[0]):
            c = p[x, y]
            if c in (H('ffdec6'), H('e7b594'), H('c78170')) or c not in T159_MAP:
                p[x, y] = CLEAR
            else:
                p[x, y] = T159_MAP[c]
    return m


XP = {'L': H('42112a'), 'o': H('6c1449'), 't': H('a84b6f'), 'T': H('8a305c'), 'w': H('ffffff'), 'W': H('c0c1e7'),
      'k': BLACK, 'l': SK['l'], 'm': SK['m'], 's': SK['s'], 'd': SK['d'], 'n': H('7e2a34'), 'b': H('f6b8b0'),
      'e': H('3a0f16'), 'c': H('b8e4f8'), 'C': H('ffffff')}
MOUTHS = {
    'happy': (23, 33, ['..........L',
                       'L........L.',
                       '.LLLLLLLLW.',
                       '.LwwwwwwWL.',
                       '..LooooooL.',
                       '..LootttL..',
                       '...LtttL...',
                       '....LLL....',
                       '....mmm....']),
    'neutral': (25, 36, ['n......n',
                         '.nnnnnn.',
                         '..mmmm..']),
    'sad_old': (25, 35, ['...nnn..',
                     '..noooon',
                     '.n.mmm..',
                     'n.......']),
    'sad': (25, 35, ['...nnnn.',
                      '..nLooLn',
                      '.n.....n']),
    'sad3': (25, 36, ['..nnnn..',
                      '.n....n.',
                      'n......n']),
    'wink': (23, 33, ['..........L',
                      'L........L.',
                      '.LLLLLLLLW.',
                      '.LwwwwwwwL.',
                      '..LWWWWWL..',
                      '...LLLtTL..',
                      '......ttt..',
                      '.......t...']),
}
FRECKLES = [(20, 32), (22, 31), (24, 32), (21, 34), (27, 30), (29, 31), (34, 30), (36, 31), (35, 33)]


def freckles(im):
    for (x, y) in FRECKLES:
        if im.getpixel((x, y)) in (SK['l'], SK['m']):
            im.putpixel((x, y), FRECK)
    return im


def fill_skin(im, box):
    p = im.load()
    for y in range(box[1], box[3]):
        for x in range(box[0], box[2]):
            p[x, y] = SK['l']
    return im


def wink_eye(im):
    im = fill_skin(im, (18, 20, 25, 30))
    return mat.patch(im, 16, 22, ['...kkkk..',
                                  '..kkkkkk.',
                                  '.kk....kk',
                                  'kk......k',
                                  '.........',
                                  '...ssss..'], XP)


def sad_eyes(im):
    # heavier upper lids sloping down to the outer corners, inner brow ends lifted over the fringe, tears
    im = mat.patch(im, 18, 23, ['kkkkkk', '..kkk.'], XP)
    im = mat.patch(im, 32, 23, ['.kkkk', '.kk..'], XP)
    im = mat.patch(im, 18, 15, ['.mm...', '.m..kk', '.mkk..', 'kk.mm.', '.mmm..'], XP)
    im = mat.patch(im, 30, 17, ['kk....', '.kkk..', '...kkk'], XP)
    im = mat.patch(im, 22, 29, ['C.', 'cC', 'c.', 'c.'], XP)
    im = mat.patch(im, 36, 29, ['C', 'c'], XP)
    return im


def put(im, part, x, y):
    t = Image.new('RGBA', im.size, CLEAR); t.paste(part, (x, y)); im.alpha_composite(t); return im


def hair_fill(im):
    # the bow hole: hair in shadow under the bloom
    p = im.load()
    reg = mat.region(im.size, [[(33, 0), (47, 0), (47, 20), (37, 20), (33, 8)]]).load()
    for y in range(48):
        for x in range(48):
            if reg[x, y] and not p[x, y][3]:
                p[x, y] = HAIR[2]
    return mat.patch(im, 36, 13, ['.e....e', 'e....e.', '....e..'], XP)


P62_HAIR = [H('310c17'), H('5c101c'), H('7b1b1d'), H('943129'), H('ad4231'), H('cd7343')]


def curls():
    # vsPlayer6_2's left curl mass (auburn already): mapped onto Juno's ramp, black outline kept
    c = bust('vsPlayer6_2').crop((38, 12, 58, 50))
    c = mat.recolour(c, dict(zip(P62_HAIR, [HAIR[0]] + HAIR)))
    keep_cols = set(HAIR + [BLACK])
    p = c.load()
    for y in range(c.size[1]):
        for x in range(c.size[0]):
            if p[x, y] not in keep_cols:
                p[x, y] = CLEAR
    return mat.clean_orphans(c)


VEIL = True
VEIL_C = (255, 240, 246)


def veil(im):
    # sheer veil from the bloom down her right side: 45% white-pink over the hair, two fold lines, soft pink edge
    before = set(mat.palette_of(im))
    p = im.load()
    for y in range(14, 48):
        x0 = 43 - (y - 14) // 12
        for x in range(x0, 48):
            c = p[x, y]
            if not c[3]:
                p[x, y] = H('f6dce6') if x > x0 else H('d8a0b8')
                continue
            if c[0] > 230 and c[1] > 200:
                continue
            a = 0.62 if x == x0 else 0.45
            if (x - x0) in (2, 4) and y % 7 not in (0, 1):
                a = 0.3
            p[x, y] = mat.blend(c, VEIL_C, a)
    # keep the veil to a few tones: quantize only the colours it introduced
    return mat.reduce_colours(im, 8, protect=before)


def assemble(expr='surprised'):
    im = hair_fill(win(face_base()))
    if CURLS:
        im = mat.under(im, curls(), *CURLS)
    if expr != 'surprised':
        im = clear_mouth(im)
    if expr in MOUTHS:
        x, y, rows = MOUTHS[expr]
        im = mat.patch(im, x, y, rows, XP)
    if expr == 'wink':
        im = wink_eye(im)
    if expr.startswith('sad'):
        im = sad_eyes(im)
    if expr in ('happy', 'wink'):
        im = mat.patch(im, 18, 31, ['b.b.b', '.b.b.'], XP); im = mat.patch(im, 34, 31, ['b.b', '.b.'], XP)
    im = freckles(im)
    fl = mat.flip(bloom())
    t = Image.new('RGBA', (48, 48), CLEAR); t.paste(fl, BLOOM_AT); im.alpha_composite(t)
    if VEIL:
        im = veil(im)
    im = wreath(im, WREATH)
    return im


EXPR = ['happy', 'surprised', 'sad', 'neutral', 'wink']


def export():
    for e in EXPR:
        im = assemble(e)
        im.save(P + '/p5_%s_48.png' % e)
        kb.up(im, 2).save(J + '/JUNO_%s_p5.png' % e)


if __name__ == '__main__' and sys.argv[1:2] == ['export']:
    export(); sys.exit()
if __name__ == '__main__':
    ex = sys.argv[1:] or ['happy', 'surprised']
    ims = [assemble(e) for e in ex]
    ims[0].save('/tmp/p5_base.png')
    row = Image.new('RGBA', (len(ims) * 392, 384), (40, 40, 48, 255))
    for i, im in enumerate(ims):
        row.paste(kb.up(kb.on_bg(im, (150, 160, 170, 255)), 8), (i * 392, 0))
    row.save('/tmp/p5_base8.png')
