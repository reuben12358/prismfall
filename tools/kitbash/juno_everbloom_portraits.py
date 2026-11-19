"""Juno Ever-Bloom bubble portraits (48-px art -> 96x96): happy, surprised, sad (+neutral).
Donors: Desolation Faces/08a,08e,08d,08b (face set: base, brows, tears), Faces/13 (open grin).
Kitbash: hair repaint, 08's own hair flower repainted and repeated as the wreath, sheer veil blend
on her left (viewer's right), ivory collar, freckles. python3 -I tools/kitbash/juno_everbloom_portraits.py"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, mat
import juno_portrait as jp
from mat import H, CLEAR
from PIL import Image

J = kb.WORK + '/juno'
BLOOM = {(90, 0, 0, 255): H('7a2a44'), (145, 18, 28, 255): H('c0506e'), (173, 26, 35, 255): H('ec8aa2'), (214, 40, 46, 255): H('fcd2da')}
IVORY = {(36, 22, 42, 255): H('8a5a6a'), (53, 37, 55, 255): H('b88a98'), (64, 52, 70, 255): H('d6b4bc'), (79, 79, 91, 255): H('f4e4e2')}
SHEER = (255, 232, 238)


def build(expr):
    src = {'happy': '08a', 'neutral': '08b', 'surprised': '08e', 'sad': '08d'}[expr]
    a = jp.face(src)
    if expr == 'happy':
        e = jp.face('08e')
        a = Image.composite(e, a, mat.region(a.size, rect=(12, 9, 44, 15)))
    eyes = mat.region(a.size, [[(15, 18), (24, 18), (24, 24), (15, 24)], [(34, 19), (40, 19), (40, 23), (34, 23)]])
    a = mat.recolour(a, jp.EYEMAP, eyes)
    a = mat.recolour(a, jp.HAIRMAP, mat.mask_not(eyes))
    a = mat.recolour(a, BLOOM, mat.region(a.size, rect=(36, 0, 48, 12)))
    a = mat.recolour(a, IVORY, mat.region(a.size, rect=(0, 38, 48, 48)))
    # wreath: the bloom repeated along the crown (mirrored / offset), smaller toward her right
    bloom = a.crop((38, 0, 48, 10))
    for (x, y, fl) in [(27, -3, 1), (16, -4, 0), (6, -2, 1)]:
        b = mat.flip(bloom) if fl else bloom
        a.alpha_composite(b, (x, max(y, 0)), (0, max(-y, 0)))
    # veil: sheer cloth falling from the wreath on the right edge; hair shows through
    p = a.load()
    for y in range(9, 48):
        x0 = 41 - (y - 9) // 9
        for x in range(x0, 48):
            if p[x, y][3]:
                p[x, y] = mat.blend(p[x, y], SHEER, 0.55 if x > x0 else 0.8)
    a = mat.reduce_colours(a, 40)
    F = {'f': H('c88a74'), 'g': H('b87462')}
    for (x, y, c) in [(19, 27, 'f'), (21, 28, 'g'), (17, 29, 'f'), (27, 26, 'f'), (34, 27, 'g'), (36, 28, 'f')]:
        a = mat.patch(a, x, y, [c], F)
    if expr == 'happy':
        m13 = jp.face('13').crop((13, 27, 27, 33)); mp = m13.load()
        for y in range(m13.size[1]):
            for x in range(m13.size[0]):
                c = mp[x, y][:3]
                if c not in ((255, 255, 255), (197, 197, 224), (145, 48, 62), (110, 39, 32), (111, 13, 0)):
                    mp[x, y] = CLEAR
        m13 = mat.clean_orphans(m13)
        for y in range(30, 35):
            for x in range(22, 35):
                c = a.getpixel((x, y))
                if c[0] < 200 and c[0] > c[2] + 20 and c[1] < 140:
                    a.putpixel((x, y), (248, 208, 184, 255))
        a.alpha_composite(m13, (20, 29))
    return a


if __name__ == '__main__':
    items = []
    for e in ['happy', 'surprised', 'sad', 'neutral']:
        im = build(e)
        kb.up(im, 2).save(J + '/JUNO_%s.png' % e if e != 'happy' else J + '/JUNO_everbloom_happy.png')
        im.save(kb.WORK + '/passes/eb_portrait_%s_48.png' % e); items.append((e, kb.on_bg(im, (150, 160, 170, 255))))
    kb.contact(items, 4, (49 * 6, 49 * 6), k=6, fs=11).save(kb.WORK + '/sheets/eb_portraits.png')
