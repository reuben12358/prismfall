"""Juno Ever-Bloom portraits, PASS 2 (48-px art -> 96x96). New donor: official B2W2 VS bust of Burgh
(soft face, big green eyes, open beam, wavy hair) cropped 48x48 at 1:1. Hair repainted to the front's auburn,
wreath = the front's own blossoms (Comfey bloom + 5-px stamps), veil = sheer blend behind/over the hair on the right.
Surprised and sad are small hand patches on the same face (mouth, brows, tear). python3 -I tools/kitbash/juno_everbloom_portraits_p2.py"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, mat
import juno_v2_everbloom as v2
from mat import H, CLEAR
from PIL import Image

V = '/home/claude/ref/art/sprites_gen5_vs_tech/extracted/Gen 5 VS Sprites/vsTrainer_LEADER_Burgh.png'
J, P = kb.WORK + '/juno', kb.WORK + '/passes'
HAIRMAP = {(192, 128, 72, 255): H('c8582e'), (160, 104, 72, 255): H('a8442a'), (136, 88, 72, 255): H('8e3624'), (96, 64, 56, 255): H('5a2018')}
SKIN = H('f8e0c8'); SK = (248, 224, 200, 255)
X = {'k': H('202020'), 'm': H('803840'), 'd': H('5a2030'), 's': SK, 'w': H('f8f8f8'), 't': H('9ad8f0'), 'T': H('e8f8ff'), 'p': H('c84868')}


def base():
    im = kb.native(kb.load(V))[0].crop((20, 0, 68, 48))
    hair_r = mat.mask_not(mat.region(im.size, [[(22, 8), (40, 8), (44, 30), (40, 44), (24, 44), (22, 30)]]))
    im = mat.recolour(im, HAIRMAP)                       # hair + its shade lines (face lines share 2 tones: kept below)
    return im


def expr(im, e):
    if e == 'happy':
        return im
    # close/clear the open mouth
    for y in range(31, 41):
        for x in range(27, 39):
            c = im.getpixel((x, y))
            if c[3] and c[:3] in ((128, 56, 64), (200, 72, 104), (248, 248, 248), (168, 168, 168), (32, 32, 32)) or c[:3] == (90, 32, 24):
                im.putpixel((x, y), SK)
    if e == 'surprised':
        im = mat.patch(im, 30, 32, ['.mmm.', 'mdddm', 'mdddm', 'mdpdm', '.mmm.'], X)
        # brows lifted
        im = mat.patch(im, 33, 18, ['sssss', 'sssss'], X)
        im = mat.patch(im, 22, 20, ['sssss'], X)
        im = mat.patch(im, 33, 16, ['.kkk.', 'k...k'], X)
        im = mat.patch(im, 22, 18, ['.kkk.'], X)
    if e == 'sad':
        im = mat.patch(im, 29, 34, ['.m...m.', 'm.m.m.m', '...m...'], X)
        im = mat.patch(im, 33, 18, ['sssss', 'sssss'], X)
        im = mat.patch(im, 33, 16, ['kk...', '..kk.', '....k'], X)
        im = mat.patch(im, 22, 20, ['sssss'], X)
        im = mat.patch(im, 22, 17, ['....k', '..kk.', 'kk...'], X)
        im = mat.patch(im, 38, 27, ['T', 't', 't'], X)
        im = mat.patch(im, 25, 29, ['T', 't'], X)
    if e == 'neutral':
        im = mat.patch(im, 29, 34, ['m.....m', '.mmmmm.'], X)
    return im


def dress(im):
    # wreath over the crown (same blossoms as the front), then the veil
    p = im.load()
    for y in range(4, 48):                      # sheer veil down the right side, hair shows through
        x0 = 44 - (y // 16)
        for x in range(x0, 48):
            c = p[x, y]
            if c[3] and c[0] > 235 and c[1] > 200:
                continue                           # never over her face
            if c[3]:
                p[x, y] = mat.blend(c, (255, 226, 234), 0.5 if x > x0 else 0.75)
            else:
                p[x, y] = H('ffe6ec') if x > x0 else H('e2a2b6')
    im = mat.reduce_colours(im, 36)
    fl = v2.red_flower()
    im.alpha_composite(mat.flip(fl), (33, 0))
    for (x, y) in [(26, 0), (19, 2), (13, 5), (8, 9)]:
        im = v2.stamp(im, x, y, v2.F5)
    im = v2.stamp(im, 23, 5, v2.BUD); im = v2.stamp(im, 5, 14, v2.BUD)
    # freckles
    F = {'f': H('d8a088')}
    for (x, y) in [(29, 27), (31, 28), (33, 27), (41, 26), (43, 27)]:
        im = mat.patch(im, x, y, ['f'], F)
    return im


if __name__ == '__main__':
    items = []
    for e in ['happy', 'surprised', 'sad', 'neutral']:
        im = dress(expr(base(), e))
        im.save(P + '/eb_portrait_p2_%s_48.png' % e); kb.up(im, 2).save(J + '/JUNO_%s_p2.png' % e)
        items.append((e, kb.on_bg(im, (150, 160, 170, 255))))
    kb.contact(items, 4, (49 * 6, 49 * 6), k=6, fs=11).save(kb.WORK + '/sheets/eb_portraits_p2.png')
