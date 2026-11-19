"""Juno "Ever-Bloom" - the chosen direction, finished front. python3 -I tools/kitbash/juno_everbloom.py
Donors: sd:lady (body, gown, back hair), sd:lass (head: laugh + flying hair), sd:diantha (cape -> veil cloth),
sd:miku-flying (tail -> floor train), Reborn battler comfey (bloom). Variants A/B/C, see VARIANTS."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, mat, show
import juno_v2_everbloom as v2
from mat import H, BLACK, CLEAR
from PIL import Image

OUT = kb.WORK + '/passes'
HAIR = v2.HAIR; HAIR_HI = v2.HAIR_HI
SHEER = {'o': H('b05a78'), 's': H('e2a2b6'), 'm': H('f4ccd6'), 'l': H('fff2f2')}
SHIFT = -13


def lady_body(keep_head):
    b = v2.lady()
    b = mat.erase(b, mat.region(b.size, [[(0, 18), (37, 18), (37, 52), (0, 52)]]))
    hair_r = mat.region(b.size, rect=(36, 6, 70, 50))
    b = mat.recolour(b, {v2.L_HAIR[0]: HAIR[0], v2.L_HAIR[1]: HAIR[1], v2.L_HAIR[2]: HAIR[2]},
                     mat.mask_and(hair_r, mat.mask_not(mat.region(b.size, rect=(36, 14, 52, 36)))))
    b = mat.recolour(b, {v2.L_HAIR[0]: HAIR[0], v2.L_HAIR[2]: HAIR[2]}, mat.region(b.size, rect=(40, 6, 60, 14)))
    dress_r = mat.mask_not(mat.region(b.size, rect=(30, 6, 58, 30)))
    b = mat.recolour(b, dict(zip(v2.L_DRESS, [H('8a5a6a'), H('d6b4bc'), H('f4e4e2'), H('fffaf6')])), dress_r)
    b = mat.recolour(b, {v2.L_RIB[0]: v2.BLUSH[0], v2.L_RIB[1]: v2.BLUSH[1]})
    if not keep_head:
        b = mat.erase(b, mat.region(b.size, [[(38, 6), (62, 6), (62, 22), (56, 27), (47, 27), (40, 24)]]))
    return b


def lass_head():
    n, f = show.get_native('sd:lass')
    reg = mat.region(n.size, [[(27, 11), (47, 11), (51, 20), (52, 33), (46, 33), (45, 30), (40, 32), (31, 32), (27, 27)]])
    h = mat.keep(n, reg)
    drop = {(144, 136, 40, 255), (192, 176, 56, 255), (232, 240, 136, 255), (104, 104, 104, 255), (152, 152, 152, 255),
            (192, 192, 192, 255)}
    p = h.load()
    for y in range(80):
        for x in range(80):
            if p[x, y] in drop:
                p[x, y] = CLEAR
    h = mat.recolour(h, {(64, 40, 8, 255): HAIR[1], (88, 56, 40, 255): HAIR[2]})
    return mat.clean_orphans(h)


def cape():
    """Diantha's cape: real cloth folds. Repainted as sheer veil."""
    n, f = show.get_native('sd:diantha')
    reg = mat.region(n.size, [[(33, 18), (51, 18), (52, 27), (47, 29), (47, 36), (58, 40), (65, 44), (62, 51), (52, 55),
                               (40, 55), (34, 50), (33, 38)]])
    c = mat.keep(n, reg)
    m = {(255, 255, 255, 255): SHEER['l'], (249, 230, 228, 255): SHEER['l'], (219, 193, 217, 255): SHEER['m'],
         (170, 156, 180, 255): SHEER['s'], (142, 104, 138, 255): SHEER['o'], (123, 74, 90, 255): SHEER['o'],
         (120, 72, 88, 255): SHEER['o'], (0, 0, 0, 255): SHEER['o']}
    p = c.load()
    for y in range(80):
        for x in range(80):
            if p[x, y][3] and p[x, y] not in m:
                p[x, y] = CLEAR
    c = mat.clean_orphans(mat.recolour(c, m))
    return c.crop(kb.bbox(c))


def tail():
    t = v2.veil()
    return mat.recolour(t, {v2.VEIL[0]: SHEER['o'], v2.VEIL[1]: SHEER['o'], v2.VEIL[2]: SHEER['s'], v2.VEIL[3]: SHEER['s'],
                            v2.VEIL[4]: SHEER['m'], v2.VEIL[5]: SHEER['l']})


def build(head='lass', veil='cape+tail', hx=-2, hy=-4):
    b = lady_body(keep_head=(head == 'lady'))
    fig = Image.new('RGBA', b.size, CLEAR); fig.paste(b, (SHIFT, 0))
    if head == 'lass':
        h = Image.new('RGBA', b.size, CLEAR); h.paste(lass_head(), (hx, hy))
        fig.alpha_composite(h)
    V = Image.new('RGBA', fig.size, CLEAR)
    if veil == 'cape+tail':
        V.alpha_composite(tail(), (43, 40))
        V.alpha_composite(cape(), (43, 9))
    else:
        V.alpha_composite(tail(), (43, 40)); V.alpha_composite(tail(), (39, 10))
    V = mat.erase(V, mat.region(V.size, rect=(0, 66, 58, 80)))
    out = mat.under(fig, V, 0, 0)
    vp = V.load(); fp = fig.load(); op = out.load()
    hair = set(HAIR) | {HAIR_HI}
    for y in range(80):
        for x in range(80):
            if vp[x, y][3] and fp[x, y] in hair and x >= 40 and y > 12:
                op[x, y] = mat.blend(fp[x, y], vp[x, y], 0.3)       # sheer: hair shows through
    out = mat.reduce_colours(out, 44)
    fl = v2.red_flower(); ff = mat.flip(fl)
    white = mat.recolour(fl, {H('c0506e'): H('c48a98'), H('ec8aa2'): H('f2d8dc'), H('fcc8d2'): H('ffffff'), H('fff8f0'): H('f2c46a')})
    s = SHIFT + 8
    # wreath: big bloom anchoring the veil at the back of the head, small arc over the crown
    out.alpha_composite(ff, (45 + s, 3))
    for (x, y) in [(31, 5), (36, 3), (41, 2)]:
        out = v2.stamp(out, x + s, y, v2.F5)
    out = v2.stamp(out, 29 + s, 9, v2.BUD)
    # bouquet
    out = v2.stamp(out, 19 + s, 30, v2.LEAF)
    out = v2.stamp(out, 30 + s, 38, ['g....', 'Gg...', 'hGg..', '.gGg.', '..gg.'])
    out = v2.stamp(out, 21 + s, 38, ['..gg', '.gGg', 'gGh.', 'gg..'])
    for (x, y) in [(22, 27), (31, 29), (20, 34), (29, 35)]:
        out = v2.stamp(out, x + s, y, v2.F5)
    out = v2.stamp(out, 27 + s, 26, v2.BUD)
    out.alpha_composite(white, (24 + s, 29))
    R2 = {'r': v2.BLUSH[0], 'p': v2.BLUSH[1]}
    out = mat.patch(out, 30 + s, 42, ['rp..', '.rp.', '.rp.', '..rp', '..r.'], R2)
    # blossoms caught in the veil
    for (x, y) in [(62, 28), (64, 58)]:
        out = v2.stamp(out, x, y, v2.F5)
    return out


VARIANTS = {'A': dict(head='lass', veil='cape+tail'), 'B': dict(head='lady', veil='cape+tail'), 'C': dict(head='lass', veil='tails')}

if __name__ == '__main__':
    items = []
    for k, kw in VARIANTS.items():
        o = build(**kw); o.save(OUT + '/eb_%s.png' % k); items.append((k, o))
    kb.contact(items, 3, (80 * 5, 80 * 5), k=5).save(kb.WORK + '/sheets/eb_variants.png')
