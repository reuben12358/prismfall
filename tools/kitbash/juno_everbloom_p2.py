"""Juno Ever-Bloom front, PASS 2. python3 -I tools/kitbash/juno_everbloom_p2.py
vs pass 1: floor train = a second length of the Diantha cape (cloth folds continue), deeper veil ramp with a rose
outline, wreath bloom rotated/recoloured so it differs from the bouquet bloom, and (variant ARM) the Parasol Lady's
open reaching arm grafted on with a blossom drifting from the hand."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, mat, show
import juno_everbloom as eb
import juno_v2_everbloom as v2
from mat import H, BLACK, CLEAR
from PIL import Image

OUT = kb.WORK + '/passes'
eb.SHEER.update({'o': H('9a4064'), 's': H('d88aa2'), 'm': H('f0bcc8'), 'l': H('ffe6ea')})


def arm():
    n, f = show.get_native('sd:parasollady')
    a = mat.keep(n, mat.region(n.size, [[(16, 18), (30, 18), (36, 24), (36, 29), (24, 29), (16, 27)]]))
    pink = {(152, 56, 104, 255): H('8a5a6a'), (184, 80, 112, 255): H('d6b4bc'), (200, 80, 128, 255): H('d6b4bc'),
            (232, 136, 168, 255): H('f4e4e2'), (184, 104, 144, 255): H('d6b4bc'), (112, 64, 80, 255): H('8a5a6a')}
    a = mat.recolour(a, pink)
    p = a.load()
    for y in range(80):
        for x in range(80):
            if p[x, y] in ((80, 72, 104, 255), (128, 128, 128, 255), (48, 48, 64, 255)):
                p[x, y] = CLEAR
    return mat.clean_orphans(a)


def build(with_arm, ax=-4, ay=4, ribbon=False, head='lass'):
    b = eb.lady_body(keep_head=(head == 'lady'))
    fig = Image.new('RGBA', b.size, CLEAR); fig.paste(b, (eb.SHIFT, 0))
    if head == 'lass':
        h = Image.new('RGBA', b.size, CLEAR); h.paste(eb.lass_head(), (-2, -4)); fig.alpha_composite(h)
    V = Image.new('RGBA', fig.size, CLEAR)
    c = eb.cape()
    if ribbon:
        V.alpha_composite(eb.tail(), (43, 40)); V.alpha_composite(c, (43, 9)); V = mat.erase(V, mat.region(V.size, rect=(0, 66, 58, 80)))
        c = Image.new('RGBA', (1, 1), CLEAR)
    V.alpha_composite(c, (48, 43))          # floor length: same cloth
    V.alpha_composite(c, (45, 26))          # middle length overlaps both, so the folds run on
    V.alpha_composite(c, (43, 9))           # upper length: from the wreath
    out = mat.under(fig, V, 0, 0)
    vp = V.load(); fp = fig.load(); op = out.load()
    hair = set(eb.HAIR) | {eb.HAIR_HI}
    for y in range(80):
        for x in range(80):
            if vp[x, y][3] and fp[x, y] in hair and x >= 40 and y > 12:
                op[x, y] = mat.blend(fp[x, y], vp[x, y], 0.3)
    out = mat.reduce_colours(out, 44)
    fl = v2.red_flower()
    white = mat.recolour(fl, {H('c0506e'): H('c48a98'), H('ec8aa2'): H('f2d8dc'), H('fcc8d2'): H('ffffff'), H('fff8f0'): H('f2c46a')})
    wre = mat.recolour(fl.transpose(Image.ROTATE_90), {H('c0506e'): H('a83a5c'), H('ec8aa2'): H('e06a8c'), H('fcc8d2'): H('f8a8bc'), H('fff8f0'): H('ffe9a8')})
    s = eb.SHIFT + 8
    out.alpha_composite(wre, (46 + s, 2))
    for (x, y) in [(31, 5), (36, 3), (41, 2)]:
        out = v2.stamp(out, x + s, y, v2.F5)
    out = v2.stamp(out, 29 + s, 9, v2.BUD)
    out = v2.stamp(out, 19 + s, 30, v2.LEAF)
    out = v2.stamp(out, 30 + s, 38, ['g....', 'Gg...', 'hGg..', '.gGg.', '..gg.'])
    out = v2.stamp(out, 21 + s, 38, ['..gg', '.gGg', 'gGh.', 'gg..'])
    for (x, y) in [(22, 27), (31, 29), (20, 34), (29, 35)]:
        out = v2.stamp(out, x + s, y, v2.F5)
    out.alpha_composite(white, (24 + s, 29))
    if with_arm:
        A = Image.new('RGBA', out.size, CLEAR); A.paste(arm(), (ax, ay))
        out.alpha_composite(A)
        for (x, y) in [(8, 17), (4, 11)]:
            out = v2.stamp(out, x, y, v2.F5)
        out = v2.stamp(out, 12, 12, v2.BUD)
    for (x, y) in ([(62, 28), (64, 58)] if ribbon else [(62, 28), (68, 62)]):
        out = v2.stamp(out, x, y, v2.F5)
    return out


if __name__ == '__main__':
    items = []
    build(False, ribbon=True).save(OUT + '/eb_P3.png')
    for k, w in [('P2', False), ('P2arm', True)]:
        o = build(w); o.save(OUT + '/eb_%s.png' % k); items.append((k, o))
    items.append(('pass1 A', Image.open(OUT + '/eb_A.png')))
    kb.contact(items, 3, (80 * 5, 80 * 5), k=5).save(kb.WORK + '/sheets/eb_p2_variants.png')
