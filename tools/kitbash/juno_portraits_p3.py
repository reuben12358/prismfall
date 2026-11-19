"""Juno portraits, PASS 3: composite faces (>=3 female donors each), 48-px art -> 96x96.
A: Rosa face/fringe + Hilda hair mass + Skyla open smile.  B: Hilda face + Caitlin wavy hair + Iris grin.
C: Bianca face + Hilda hair mass + Skyla smile.   python3 -I tools/kitbash/juno_portraits_p3.py"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, mat
import juno_v2_everbloom as v2
from mat import H, CLEAR, BLACK
from PIL import Image

V = '/home/claude/ref/art/sprites_gen5_vs_tech/extracted/Gen 5 VS Sprites/vsTrainer_'
J, P = kb.WORK + '/juno', kb.WORK + '/passes'
HD, HM, HL, HH = H('5a2018'), H('963a24'), H('c8582e'), H('f0945a')
SKIN, SKS = (248, 208, 184, 255), (216, 160, 120, 255)
GR = {'d': H('1e5a3c'), 'g': H('48a060'), 'l': H('8ed07a')}
c4 = lambda *t: tuple(t) + (255,)


def bust(n):
    return kb.native(kb.load(V + n + '.png'))[0]


def only(im, cols):
    cols = set(cols); im = im.copy(); p = im.load()
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            if p[x, y][3] and p[x, y] not in cols:
                p[x, y] = CLEAR
    return mat.clean_orphans(im)


def hilda_mass():
    h = only(bust('POKEMONTRAINER_Hilda').crop((10, 0, 42, 50)), [c4(48, 16, 8), c4(72, 40, 32), c4(96, 64, 56), BLACK])
    return mat.recolour(h, {c4(48, 16, 8): HD, c4(72, 40, 32): HM, c4(96, 64, 56): HL})


def caitlin_hair():
    h = only(bust('ELITEFOUR_Caitlin').crop((24, 6, 96, 64)), [c4(232, 192, 112), c4(200, 144, 88), c4(176, 120, 80), c4(128, 80, 48), c4(248, 224, 152), c4(24, 24, 24)])
    return mat.recolour(h, {c4(232, 192, 112): HL, c4(200, 144, 88): HM, c4(176, 120, 80): HM, c4(128, 80, 48): HD, c4(248, 224, 152): HH, c4(24, 24, 24): BLACK})


def mouth(kind):
    if kind == 'skyla':
        m = only(bust('LEADER_Skyla').crop((57, 28, 71, 35)), [c4(112, 40, 56), c4(152, 56, 64), c4(192, 72, 80), c4(248, 248, 248)])
    else:
        m = only(bust('LEADER_Iris').crop((48, 40, 60, 48)), [c4(112, 56, 72), c4(184, 64, 64), c4(224, 104, 128), c4(248, 248, 248), c4(96, 64, 64)])
    return m.crop(kb.bbox(m))


def dress(im, blooms, veil_x=40):
    p = im.load()
    for y in range(6, 48):
        x0 = veil_x + (y // 14)
        for x in range(x0, 48):
            c = p[x, y]
            if c[3] and c[0] > 235 and c[1] > 195:
                continue
            p[x, y] = mat.blend(c, (255, 226, 234), 0.5 if x > x0 else 0.8) if c[3] else (H('ffe6ec') if x > x0 else H('d88aa2'))
    im = mat.reduce_colours(im, 36)
    fl = v2.red_flower()
    big = blooms[0]; im.alpha_composite(mat.flip(fl), big)
    for (x, y) in blooms[1:]:
        im = v2.stamp(im, x, y, v2.F5)
    return im


def freckles(im, pts):
    for (x, y) in pts:
        if im.getpixel((x, y)) == SKIN:
            im.putpixel((x, y), H('e0a488'))
    return im


MOUTH, MPOS = 'iris', (21, 34)


def cand_A(expr='happy'):
    r = bust('POKEMONTRAINER_Rosa').crop((40, 2, 88, 50))
    r = mat.erase(r, mat.region(r.size, [[(0, 0), (11, 0), (11, 8), (8, 22), (4, 30), (0, 30)], [(37, 0), (47, 0), (47, 30), (42, 30), (39, 20), (37, 8)]]))
    r = mat.erase(r, mat.region(r.size, [[(39, 33), (47, 33), (47, 47), (36, 47), (36, 40)]]))
    top = mat.region(r.size, rect=(0, 0, 47, 23))
    r = mat.recolour(r, {c4(232, 232, 248): HL, c4(216, 104, 136): HM, c4(160, 64, 88): HD, c4(128, 72, 72): HD, c4(168, 152, 80): HL}, top)
    r = mat.recolour(r, {c4(216, 104, 136): HM, c4(160, 64, 88): HD}, mat.region(r.size, rect=(30, 20, 47, 30)))
    r = mat.recolour(r, {c4(64, 56, 40): HM, c4(104, 72, 56): HL})
    eyes = mat.region(r.size, [[(15, 23), (25, 23), (25, 33), (15, 33)], [(31, 23), (39, 23), (39, 33), (31, 33)]])
    r = mat.recolour(r, {c4(96, 120, 128): GR['l'], c4(48, 48, 56): GR['g']}, eyes)
    for (x, y) in [(19, 28), (20, 28), (19, 29), (34, 28), (35, 28), (34, 29)]:
        if r.getpixel((x, y)) == BLACK:
            r.putpixel((x, y), GR['g'])
    back = Image.new('RGBA', (48, 48), CLEAR)
    hm = hilda_mass(); back.alpha_composite(hm, (-8, 0), (0, 0)); back.alpha_composite(mat.flip(hm), (26, 2))
    im = mat.under(r, back, 0, 0)
    # mouth
    mreg = [(x, y) for y in range(34, 41) for x in range(22, 33) if im.getpixel((x, y))[:3] in ((216, 104, 136), (160, 64, 88), (128, 72, 72), (0, 0, 0))]
    for (x, y) in mreg:
        im.putpixel((x, y), SKIN)
    X = {'m': H('983840'), 'd': H('702838'), 'p': H('e06880'), 'w': H('f8f8f8'), 'k': BLACK, 's': SKIN, 't': H('9ad8f0'), 'T': H('e8f8ff')}
    if expr == 'happy':
        im.alpha_composite(mouth(MOUTH), MPOS)
    elif expr == 'surprised':
        im = mat.patch(im, 25, 35, ['.mm.', 'mddm', 'mdpm', '.mm.'], X)
        im = mat.patch(im, 16, 20, ['.kkkk.'], X); im = mat.patch(im, 32, 20, ['.kkkk.'], X)
    elif expr == 'sad':
        im = mat.patch(im, 23, 37, ['.m...m.', 'm.mmm.m'], X)
        im = mat.patch(im, 15, 20, ['...kkk', 'kkk...'], X); im = mat.patch(im, 31, 20, ['kkk...', '...kkk'], X)
        im = mat.patch(im, 17, 33, ['T', 't', 't'], X); im = mat.patch(im, 37, 33, ['T', 't'], X)
    else:
        im = mat.patch(im, 24, 37, ['m....m', '.mmmm.'], X)
    im = freckles(im, [(20, 34), (22, 35), (18, 35), (30, 34), (32, 35), (34, 34), (26, 33)])
    return dress(im, [(30, 6), (22, 9), (15, 11), (9, 14), (26, 5)], veil_x=41)


XP = {'m': H('983840'), 'd': H('702838'), 'p': H('e06880'), 'w': H('f8f8f8'), 'k': BLACK, 't': H('9ad8f0'), 'T': H('e8f8ff')}
SMILE = ['mmmmmmmmm', 'mwwwwwwwm', '.mdddddm.', '..mpppm..', '...mmm...']


def final_A(expr):
    global mouth
    keep = mouth; mouth = lambda k: Image.new('RGBA', (1, 1), CLEAR)
    im = cand_A(expr); mouth = keep
    if expr == 'happy':
        im = mat.patch(im, 22, 35, SMILE, XP)
    if expr in ('happy', 'neutral'):
        im = mat.patch(im, 17, 20, ['.kkk.', 'k....'], XP); im = mat.patch(im, 32, 20, ['.kkk.', '....k'], XP)
    p = im.load()
    for y in range(22, 29):                       # lift the old visor shadow off her forehead
        for x in range(14, 40):
            if p[x, y] == SKS:
                p[x, y] = SKIN
    return im


def cand_B(expr='happy'):
    r = bust('POKEMONTRAINER_Hilda').crop((32, 0, 80, 48))
    r = mat.recolour(r, {c4(232, 232, 248): HL, c4(184, 184, 216): HM}, mat.region(r.size, rect=(0, 0, 47, 24)))
    r = mat.recolour(r, {c4(200, 88, 152): HM, c4(160, 48, 112): HD, c4(232, 136, 216): HL}, mat.region(r.size, rect=(0, 0, 47, 29)))
    r = mat.recolour(r, {c4(48, 16, 8): HD, c4(72, 40, 32): HM, c4(96, 64, 56): HL, c4(80, 120, 168): GR['g'], c4(64, 64, 80): GR['d']})
    back = Image.new('RGBA', (48, 48), CLEAR); back.alpha_composite(caitlin_hair(), (-14, -4))
    im = mat.under(r, back, 0, 0)
    for y in range(38, 44):
        for x in range(18, 32):
            if im.getpixel((x, y))[:3] in ((160, 112, 64), (0, 0, 0)):
                im.putpixel((x, y), (248, 216, 192, 255))
    if expr == 'happy':
        im = mat.patch(im, 20, 38, SMILE, XP)
    return dress(im, [(30, 8), (22, 12), (15, 13), (9, 16), (26, 8)], veil_x=42)


def cand_C(expr='happy'):
    r = bust('LEADER_Skyla').crop((38, 4, 86, 52))
    blues = [c4(40, 56, 64), c4(56, 88, 152), c4(56, 128, 152), c4(104, 144, 160), c4(88, 176, 200), c4(168, 216, 240), c4(168, 232, 208)]
    eyes = mat.region(r.size, [[(14, 15), (22, 15), (22, 25), (14, 25)], [(26, 13), (33, 13), (33, 23), (26, 23)]])
    r = mat.recolour(r, {c4(56, 88, 152): GR['g'], c4(104, 144, 160): GR['l'], c4(40, 56, 64): GR['d'], c4(56, 128, 152): GR['g']}, eyes)
    r = mat.erase(r, mat.mask_and(mat.mask_not(eyes), mat.colour_mask(r, blues)))
    r = mat.erase(r, mat.region(r.size, rect=(0, 36, 47, 47)))
    notmouth = mat.mask_not(mat.region(r.size, rect=(20, 25, 31, 31)))
    r = mat.recolour(r, {c4(112, 40, 56): HD, c4(152, 56, 64): HM, c4(192, 72, 80): HL}, notmouth)
    r = mat.clean_orphans(r)
    back = Image.new('RGBA', (48, 48), CLEAR); back.alpha_composite(caitlin_hair(), (-18, -2)); back.alpha_composite(hilda_mass(), (-10, 2))
    im = mat.under(r, back, 0, 0)
    return dress(im, [(30, 0), (22, 3), (15, 5), (10, 9), (26, 1)], veil_x=42)


if __name__ == '__main__':
    items = [(n, kb.on_bg(f('happy'), (150, 160, 170, 255))) for n, f in [('A', final_A), ('B', cand_B), ('C', cand_C)]]
    for n, f in [('A', final_A), ('B', cand_B), ('C', cand_C)]:
        f('happy').save(P + '/p3_cand_%s_48.png' % n)
    kb.contact(items, 3, (49 * 6, 49 * 6), k=6, fs=11).save(kb.WORK + '/sheets/p3_cands.png')
    items = []
    for e in ['happy', 'surprised', 'sad', 'neutral']:
        im = final_A(e); im.save(P + '/p3_A_%s_48.png' % e); kb.up(im, 2).save(J + '/JUNO_%s_p3.png' % e)
        items.append((e, kb.on_bg(im, (150, 160, 170, 255))))
    kb.contact(items, 4, (49 * 6, 49 * 6), k=6, fs=11).save(kb.WORK + '/sheets/p3_A.png')
