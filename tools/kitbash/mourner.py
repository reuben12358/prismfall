"""The Mourner (HOLLOW_MOURNER; secretly Rowan Ashby, the Grass Warden, 52, a rangy gentle gardener) battle fronts
(80-px art, 160x160 export). python3 -I tools/kitbash/mourner.py [variant ...]; sheet: sheet_cast.py mourner
Concept: GRIEF AS LITURGY. A tall ash-grey robe and cowl, a carved ash-bark mask (pale, one sorrowful carved face), one
white lily held up like a censer in a gardener's hand. Theatrical and gentle at once: the gesture is an offering, not a
threat. Ash grey + bone white; the lily the only living colour. The build under the robe is lean and long-handed (Rowan).
  A body : sd sage (BW class: tall robe, wide sleeves, a ritual swing of prayer beads) -> ash robe; beads -> one lily
     cowl : sd pearlclanmember's hood (cloth only) in a darker ash than Thistle's (the Hollow's cowl, rank by shade)
     mask : an oval of B:trevenant's lower-trunk bark recoloured pale ash; carved eye slits and a frown stamped on
     lily : hand-drawn (6 px trumpet, stem)
  B the address: the same with the hem frayed into strips and the lily lowered to the chest ("Let the land grieve").
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, mat, show, sheet09 as s9, thistle as th
from mat import H, CLEAR, BLACK
from PIL import Image

OUT = kb.WORK + '/passes'
NAME, SHEET = 'MOURNER', '24_mourner.png'
TITLE = ('THE MOURNER (HOLLOW_MOURNER; secretly Rowan Ashby, 52, the Grass Warden) - battle front kitbash (80-px art, file 160x160). '
         'Concept: grief as liturgy. Ash-grey robe and cowl, a pale carved ash-bark mask, one white lily raised like a censer in '
         'a gardener\'s hand. Ash + bone white; the lily the only living colour.')


def sd(n, flip=False):
    im = show.get_native('sd:' + n)[0]
    return im.transpose(Image.FLIP_LEFT_RIGHT) if flip else im


C = {'r1': H('c4bfb8'), 'r2': H('9a9590'), 'r3': H('6e6a66'), 'r4': H('4a4644'), 'r5': H('2e2a2a'),       # ash robe
     'm1': H('f2ece0'), 'm2': H('d6ccb8'), 'm3': H('a89c88'), 'm4': H('6c6052'),                         # bark mask
     'l1': H('ffffff'), 'l2': H('e8eef0'), 'l3': H('b8c8c8'), 'ly': H('f0d050'), 'lg': H('6cb050'), 'lG': H('3c7038')}
X = {'k': BLACK, 'w': C['l1'], 'W': C['l2'], 'c': C['l3'], 'y': C['ly'], 'g': C['lg'], 'G': C['lG'],
     'r': C['r2'], 'R': C['r3'], 'q': C['r4'], 'Q': C['r5'], 'm': C['m1'], 'M': C['m2'], 'n': C['m3'], 'N': C['m4']}
ROBE = {H('626273'): C['r2'], H('5a6273'): C['r2'], H('423b4a'): C['r3'], H('3b334a'): C['r3'], H('25252c'): C['r4'],
        H('191325'): C['r5'], H('848d8d'): C['m2'], H('a9a9a9'): C['m1'], H('e2e2f6'): C['m1']}
HOOD = {H('ffffff'): C['r1'], H('f4dde4'): C['r1'], H('bc91b6'): C['r2'], H('a776a2'): C['r3'], H('6d516f'): C['r4'],
        H('613d63'): C['r5'], H('b4c0d5'): C['r2'], H('576673'): C['r4'], H('d76557'): C['r3'], H('b1323c'): C['r4'],
        H('9c2931'): C['r4'], H('764247'): C['r5']}
BARK = {H('9f8b72'): C['m1'], H('8f6450'): C['m2'], H('6e4345'): C['m3'], H('421c2e'): C['m4'], H('5b442d'): C['m3'],
        H('2d3142'): BLACK, H('565963'): C['m4'], H('bf3c3c'): BLACK, H('fa8350'): BLACK}
SKIN = {H('f6c5a9'), H('cf8d62'), H('a9624a')}
BEADS = {H('623342'), H('3b0d0d'), H('b2251f'), H('a9a9a9'), H('848d8d')}


MASK_SHAPE = ['...kkkkk...',
              '.kk.....kk.',
              'k.........k',
              'k.........k',
              'k.........k',
              'k.kkk.kkk.k',
              'k.k.....k.k',
              'k.........k',
              'k.........k',
              'k...kkk...k',
              'k..k...k..k',
              '.k.......k.',
              '.kk.....kk.',
              '...kkkkk...']


def mask():
    """an oval mask of pale ash bark: the grain is Trevenant's lower trunk (recoloured), the carving is stamped on:
    eye slits drooping at the outer corners, a downturned mouth (a sorrowful face, like the Ogre masks of Briarwick)."""
    t = s9.donor_img('B:trevenant')
    bark = mat.recolour(t.crop((43, 36, 54, 50)), {H('9f8b72'): C['m1'], H('8f6450'): C['m2'], H('6e4345'): C['m3'],
                                                    H('421c2e'): C['m4'], H('1a181b'): C['m3'], H('2d3142'): C['m3'],
                                                    H('565963'): C['m3']})
    w, h = len(MASK_SHAPE[0]), len(MASK_SHAPE)
    m = Image.new('RGBA', (w, h), CLEAR); p = m.load(); bp = bark.load()
    for y, row in enumerate(MASK_SHAPE):
        inside = [x for x, ch in enumerate(row) if ch == 'k']
        for x, ch in enumerate(row):
            if ch == 'k':
                p[x, y] = BLACK
            elif inside and min(inside) < x < max(inside) and y not in (0, h - 1):
                c = bp[x % bark.size[0], y % bark.size[1]]
                p[x, y] = c if c[3] else C['m1']
    # outline shapes on the top/bottom rows that are not closed inside
    return m


def build(var='A'):
    b = sd('sage')
    # --- the prayer beads go (the raised hand stays)
    p = b.load()
    for y in range(12, 40):
        for x in range(4, 26):
            if p[x, y] in BEADS or (p[x, y] == BLACK and x < 20 and y > 20):
                p[x, y] = CLEAR
    # what is left of the string round the raised hand: keep only the hand and its own outline
    p = b.load()
    keep = set()
    for y in range(2, 26):
        for x in range(2, 26):
            if p[x, y] in SKIN:
                keep.add((x, y))
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        keep.add((x + dx, y + dy))
    for y in range(2, 26):
        for x in range(2, 22):
            if (x, y) not in keep and p[x, y][3] and p[x, y] not in ROBE and p[x, y] not in (H('423b4a'), H('25252c'), H('191325')):
                p[x, y] = CLEAR
    p = b.load()
    for y in range(21, 40):
        for x in range(4, 21):
            if p[x, y] in SKIN:                      # bead-brown dashes down the sleeve (same colours as the hand)
                p[x, y] = H('423b4a') if any(p[x + 1, yy] in (H('423b4a'), H('25252c')) for yy in (y,)) else CLEAR
    for _ in range(2):
        p = b.load()
        for y in range(4, 26):
            for x in range(4, 16):
                if p[x, y] == BLACK and not any(p[x + dx, y + dy][3] and p[x + dx, y + dy] != BLACK
                                                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    p[x, y] = CLEAR
    b = mat.drop_specks(mat.clean_orphans(b), 6)
    b = mat.recolour(b, ROBE)
    # --- head: shaved head + face -> cowl + mask
    b = mat.erase(b, mat.region(b.size, [[(31, 0), (51, 0), (51, 16), (47, 21), (40, 22), (34, 20), (31, 14)]]))
    pc = sd('pearlclanmember')
    hood = mat.keep(pc, mat.region(pc.size, [[(34, 2), (56, 2), (56, 27), (52, 30), (36, 30), (34, 27)]]))
    hp = hood.load()
    for y in range(hood.size[1]):
        for x in range(hood.size[0]):
            if hp[x, y] in (H('ffd6bd'), H('dea57b'), H('9c6b52'), H('8c6c57'), H('433029'), H('5b433c'), H('414a52')):
                hp[x, y] = CLEAR
            elif 36 <= x <= 46 and 15 <= y <= 26 and hp[x, y][3]:
                hp[x, y] = CLEAR
    hood = mat.recolour(hood, HOOD)
    b = mat.paste(b, hood, -2, -10)
    mk = mask()
    b = mat.paste(b, mk, 34, 4)
    # cowl shadow round the mask
    p = b.load()
    for y in range(2, 22):
        for x in range(32, 52):
            if not p[x, y][3]:
                l = any(p[xx, y][3] for xx in range(28, x)); r = any(p[xx, y][3] for xx in range(x + 1, 56))
                u = any(p[x, yy][3] for yy in range(0, y))
                if l and r and u:
                    p[x, y] = C['r5']
    # --- the lily
    if var == 'A':
        b = mat.patch(b, 14, 5, ['..k.k..',
                                 '.kwkwk.',
                                 'kwWwWwk',
                                 'kWwywWk',
                                 '.kwywk.',
                                 '..kck..',
                                 '..kgk..',
                                 '..kgk..',
                                 '..kGk..'], X)
    else:
        b = mat.patch(b, 40, 22, ['.k.k.', 'kwkwk', 'kwywk', '.kck.', '.kgk.'], X)
        # the hem frays into strips
        p = b.load()
        for x in range(26, 60):
            top = None
            for y in range(60, 72):
                if p[x, y][3] and p[x, y] in (C['r2'], C['r3'], C['r4'], C['r5']):
                    top = y
            if top and x % 4 == 1:
                for y in range(top - 2, top + 1):
                    p[x, y] = CLEAR
                p[x, top - 3] = BLACK
    return b


VARIANTS = [('A', 'A: grief as liturgy. Tall ash robe and cowl, the pale carved ash-bark mask, one white lily raised like a censer in a '
                  'long gardener\'s hand; the other hand on his heart. Sage (BW) body, Pearl Clan hood (darker ash than Thistle\'s), '
                  'Trevenant bark for the mask, hand-drawn lily.'),
            ('B', 'B: "Let the land grieve." The lily lowered to the chest, the robe\'s hem frayed into strips.')]
PICK = 'A'
REFS = [('sd:sage', 'Sage (donor class)'), ('sd:ghetsis', 'Ghetsis (official BW)'), ('sd:grimsley', 'Grimsley (official BW)'),
        ('file:' + kb.WORK + '/thistle/THISTLE_A.png', 'Thistle (ours, sheet 23)'), ('reborn:093', 'Reborn front (Julia)')]
DONORS = [('sd:sage', 'sage: body, pose, robe, hands (beads cut)'), ('sd:pearlclanmember', 'pearlclanmember: hood cloth -> dark ash cowl'),
          ('B:trevenant', 'Trevenant battler: lower-trunk bark grain -> the mask\'s surface (pale ash)')]
NOTE = 'Hand pixels: the mask outline and carving (drooping eye slits, frown), the lily (6 px trumpet + stem), cowl shadow, B\'s hem notches.'

if __name__ == '__main__':
    vs = sys.argv[1:] or ['A']
    ims = [build(v) for v in vs]
    row = Image.new('RGBA', (len(ims) * 330, 330), (40, 40, 48, 255))
    for i, im in enumerate(ims):
        im.save(OUT + '/mou_%s.png' % vs[i])
        row.paste(kb.up(kb.on_bg(im, (150, 160, 170, 255)), 4), (i * 330, 0))
    row.save('/tmp/mou.png')
    kb.grid(ims[0], k=9).save('/tmp/mou_grid.png')
