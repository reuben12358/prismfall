"""The Mourner, pass 2 (sheet 24b): the silhouette gets drama. python3 -I tools/kitbash/sheet_cast.py mourner_p2
  - The figure moves down 12 px. Above the cowl, a crown of bare branches (B:trevenant's two antler branches, leaves cut,
    recoloured ash dead-wood) rises like antlers: the outline of his ace.
  - The robe's hem runs into roots (B:trevenant's root legs, recoloured to the robe's ash) spreading on the ground; the
    sandals and white under-robe are gone under them.
  - The mask is smaller and curved, with deep eye hollows and woodgrain (the pass-1 square read as No-Face).
  - The lily still offered out to the side in a long gardener's hand (Rowan's hands stay visible).
C = crown + roots + mask; D = the same with the lily held at his heart and the free hand open toward the viewer."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, mat, show, sheet09 as s9, mourner as m1
from mat import H, CLEAR, BLACK
from PIL import Image

NAME, SHEET = 'MOURNER', '24b_mourner_p2.png'
TITLE = ('THE MOURNER, pass 2 - battle front kitbash (80-px art, file 160x160). Grief as liturgy, now with his ace\'s outline: a crown '
         'of bare ash branches rising from the cowl, the robe running into roots at the hem, a smaller curved bark mask with deep '
         'eye hollows, the lily offered in a long gardener\'s hand.')
C, X = m1.C, m1.X
DEAD = {H('9f8b72'): C['r1'], H('8f6450'): C['r2'], H('6e4345'): C['r3'], H('421c2e'): C['r4'], H('1a181b'): BLACK,
        H('5b442d'): C['r3'], H('2d3142'): C['r4'], H('565963'): C['r3']}
GREENS = [H('4cc87c'), H('436b44'), H('3a985f'), H('2b442c'), H('bf3c3c'), H('fa8350')]
DY = 12

MASK2 = ['..kkkkk..',
         '.kmMmmmk.',
         'kmmmMmmmk',
         'kNkkmkkNk',
         'kmkkmkkmk',
         'kmmNmmmmk',
         '.kmmMmmk.',
         '.kmNkNmk.',
         '..kmmmk..',
         '...kkk...']


def mask2():
    t = s9.donor_img('B:trevenant')
    bark = mat.recolour(t.crop((43, 36, 54, 50)), {H('9f8b72'): C['m1'], H('8f6450'): C['m2'], H('6e4345'): C['m3'],
                                                    H('421c2e'): C['m3'], H('1a181b'): C['m3']})
    w, h = len(MASK2[0]), len(MASK2)
    m = Image.new('RGBA', (w, h), CLEAR); p = m.load(); bp = bark.load()
    for y, row in enumerate(MASK2):
        for x, ch in enumerate(row):
            if ch == '.':
                continue
            if ch in 'mM':
                c = bp[(x + 2) % bark.size[0], y % bark.size[1]]
                p[x, y] = c if c[3] and ch == 'm' else X[ch]
            else:
                p[x, y] = X[ch]
    return m


def parts():
    t = s9.donor_img('B:trevenant')
    crown = t.crop((30, 0, 72, 21))
    crown = mat.erase(crown, mat.colour_mask(crown, GREENS))
    crown = mat.recolour(mat.drop_specks(mat.clean_orphans(crown), 6), DEAD)
    crown = mat.outline_outer(crown, BLACK)
    roots = t.crop((16, 48, 80, 77))
    roots = mat.erase(roots, mat.colour_mask(roots, GREENS))
    roots = mat.erase(roots, mat.region(roots.size, rect=(0, 0, 10, 6)))
    roots = mat.recolour(mat.drop_specks(mat.clean_orphans(roots), 8), DEAD)
    return crown, roots


def build(var='C'):
    a = m1.build('A')
    # rebuild the head with the smaller curved mask: pass-1's mask area -> cowl shadow first
    p = a.load()
    for y in range(4, 18):
        for x in range(34, 45):
            if p[x, y][3]:
                p[x, y] = C['r5']
    a = mat.paste(a, mask2(), 35, 6)
    # the figure down DY px, its lowest rows (sandals, white under-robe) cut
    body = Image.new('RGBA', a.size, CLEAR)
    body.paste(a.crop((0, 0, 80, 80 - DY)), (0, DY))
    pb = body.load()
    for y in range(80 - DY - 2, 80):
        for x in range(80):
            if pb[x, y] in (C['m1'], C['m2'], H('f6c5a9'), H('cf8d62'), H('a9624a'), H('b2251f')):
                pb[x, y] = CLEAR
    crown, roots = parts()
    out = mat.under(body, crown, 41 - crown.size[0] // 2 + 1, 0)
    out = mat.under(out, roots, 41 - roots.size[0] // 2, 80 - roots.size[1])
    if var == 'D':
        # lily lowered to the heart, the raised hand opened toward the viewer (the lily's place cleared)
        out = mat.erase(out, mat.region(out.size, rect=(12, 4 + DY, 22, 14 + DY)))
        out = mat.patch(out, 39, 22 + DY, ['.k.k.', 'kwkwk', 'kwywk', '.kck.', '.kgk.'], X)
    return mat.drop_specks(out, 6)


VARIANTS = [('C', 'C (pass 2): a crown of bare ash branches rising from the cowl like his Trevenant\'s antlers, the robe running '
                  'into roots on the ground, a smaller curved bark mask with deep eye hollows, the lily offered out in a long '
                  'gardener\'s hand. Sage body, Pearl Clan hood, Trevenant branches, roots and bark.'),
            ('D', 'D (pass 2): the same, the lily held at his heart and the long empty hand open toward you.'),
            ('A', 'A (pass 1, sent): for comparison.')]
PICK = 'C'
REFS = m1.REFS
DONORS = m1.DONORS + [('B:trevenant', 'Trevenant again: the two antler branches (leaves cut) and the root legs, ash dead-wood')]
NOTE = ('Hand pixels: the curved mask outline and carving (eye hollows, grain marks, small mouth), the lily, cowl shadow. The branches '
        'and roots are Trevenant\'s own, recoloured.')


def _a():
    return m1.build('A')


if __name__ == '__main__':
    vs = sys.argv[1:] or ['C']
    ims = [build(v) if v != 'A' else _a() for v in vs]
    row = Image.new('RGBA', (len(ims) * 330, 330), (40, 40, 48, 255))
    for i, im in enumerate(ims):
        row.paste(kb.up(kb.on_bg(im, (150, 160, 170, 255)), 4), (i * 330, 0))
    row.save('/tmp/mou2.png')
