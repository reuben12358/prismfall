"""Pallbearer Thistle (Mara Thistlewood, HOLLOW_THISTLE) battle fronts (80-px art, 160x160 export).
python3 -I tools/kitbash/thistle.py [variant ...]; sheet: python3 -I tools/kitbash/sheet_cast.py thistle
Concept: THE WEAVER WHO CUTS. A grieving ex-weaver from Lowmarsh (Fixed) who now cuts what binds: curtain ropes, survey
flags. Ash-grey Hollow cowl and coat, one long thistle-purple sash streaming off her like a loose thread, big tailor's shears
held point-down like a blade, a torn orange survey flag tucked at her belt, a thistle brooch. "I know where a thread will fall."
  A body : sd veteranf-gen6 (coat, high collar, a scarf in the wind) -> charcoal Hollow coat, the scarf -> purple sash
     hood : sd pearlclanmember's hood (cloth only) -> ash-grey cowl around veteranf-gen6's own face (embroidery painted out)
     shears: hand-drawn straight hardware (steel blades, brass pivot, black bow handle) in the ball hand
  B the cut: the same, with the shears raised open across the body (about to cut)
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, mat, show
from mat import H, CLEAR, BLACK
from PIL import Image

OUT = kb.WORK + '/passes'
NAME, SHEET = 'THISTLE', '23_thistle.png'
TITLE = ('PALLBEARER THISTLE (Mara Thistlewood, 40, HOLLOW_THISTLE) - battle front kitbash (80-px art, file 160x160). Concept: the '
         'weaver who cuts. Ash-grey Hollow cowl and coat, one thistle-purple sash streaming like a loose thread, tailor\'s shears '
         'held like a blade, a torn orange survey flag at her belt. Grieving, careful, fierce.')


def sd(n, flip=False):
    im = show.get_native('sd:' + n)[0]
    return im.transpose(Image.FLIP_LEFT_RIGHT) if flip else im


C = {'k': BLACK,
     'g1': H('d4d0cc'), 'g2': H('aaa5a0'), 'g3': H('7c7672'), 'g4': H('524c4a'), 'g5': H('302c2c'),     # ash cowl
     'c1': H('6e6a6a'), 'c2': H('4a4646'), 'c3': H('2e2a2c'), 'c4': H('8a8684'),                       # charcoal coat
     'p1': H('d08ce6'), 'p2': H('a052c4'), 'p3': H('6e2c92'), 'p4': H('421a5c'),                       # thistle purple
     's1': H('f4f8fc'), 's2': H('b8c4d0'), 's3': H('74808e'), 's4': H('3c4450'),                       # steel
     'b1': H('f8d060'), 'b2': H('b08020'),                                                             # brass
     'o1': H('ff8a30'), 'o2': H('c85418'), 'v1': H('70b050'), 'v2': H('3c7030')}                      # flag, thistle leaf
X = {'k': BLACK, 's': C['s1'], 'S': C['s2'], 'm': C['s3'], 'M': C['s4'], 'y': C['b1'], 'Y': C['b2'], 'o': C['o1'],
     'O': C['o2'], 'p': C['p1'], 'P': C['p2'], 'q': C['p3'], 'Q': C['p4'], 'v': C['v1'], 'V': C['v2'], 'w': H('ffffff'),
     'g': C['g2'], 'G': C['g3'], 'h': C['g4'], 'x': C['g5']}

VF_HAIR = [H('c7be9f'), H('918d72'), H('575b44')]
COAT = {H('5e86ba'): C['c4'], H('3d6393'): C['c1'], H('294464'): C['c2'], H('13222d'): C['c3']}
SASH = {H('ef5a3f'): C['p1'], H('e25565'): C['p2'], H('863c4f'): C['p3'], H('7c495a'): C['p3'], H('54373b'): C['p4']}
HOOD = {H('ffffff'): C['g1'], H('f4dde4'): C['g1'], H('bc91b6'): C['g2'], H('a776a2'): C['g3'], H('6d516f'): C['g4'],
        H('613d63'): C['g5'], H('b4c0d5'): C['g2'], H('576673'): C['g4'],
        H('d76557'): C['g3'], H('b1323c'): C['g4'], H('9c2931'): C['g4'], H('764247'): C['g5']}   # embroidery -> plain


def hooded_head():
    """veteranf-gen6 with her bob erased and the Pearl Clan hood (cloth only) wrapped round her own face."""
    b = sd('veteranf-gen6')
    p = b.load()
    for y in range(0, 22):
        for x in range(26, 54):
            if p[x, y] in VF_HAIR:
                p[x, y] = CLEAR
    b = mat.clean_orphans(b)
    pc = sd('pearlclanmember')
    face = set([H('ffd6bd'), H('dea57b'), H('9c6b52'), H('8c6c57'), H('433029'), H('5b433c'), H('414a52'), H('282830')])
    hood = mat.keep(pc, mat.region(pc.size, [[(34, 2), (56, 2), (56, 27), (52, 30), (36, 30), (34, 27)]]))
    hp = hood.load()
    for y in range(hood.size[1]):
        for x in range(hood.size[0]):
            if hp[x, y] in face:
                hp[x, y] = CLEAR
    # the face opening: pearl clan rows 16-26 between the hood's sides; leave it open so her own face shows
    for y in range(15, 27):
        for x in range(36, 47):
            if hp[x, y][3] and (hp[x, y] != BLACK or y in (16, 17)):
                hp[x, y] = CLEAR                     # incl. the hood's visor band (a black line across the brow)
    hood = mat.recolour(hood, HOOD)
    b = mat.under(b, hood, -2, -6) if False else mat.paste(b, hood, -2, -6)
    # the shadow inside the cowl where her bob used to be (gaps between face and hood)
    p = b.load()
    for y in range(4, 20):
        for x in range(30, 50):
            if not p[x, y][3]:
                l = any(p[xx, y][3] for xx in range(26, x)); r = any(p[xx, y][3] for xx in range(x + 1, 54))
                u = any(p[x, yy][3] for yy in range(0, y))
                if l and r and u:
                    p[x, y] = C['g5']
    return b


def shears(im, hx, hy, tx, ty, open_px=3):
    """two straight steel blades from the pivot (hx, hy) to tips around (tx, ty), opened by open_px at the tip; a brass
    pivot; outlined in black. Drawn as 1-px lines, each with a 1-px shadow side."""
    out = im.copy(); p = out.load(); W, Hh = im.size
    pts = {}

    def line(x0, y0, x1, y1, col, col2):
        n = max(abs(x1 - x0), abs(y1 - y0))
        for i in range(n + 1):
            x = round(x0 + (x1 - x0) * i / n); y = round(y0 + (y1 - y0) * i / n)
            pts[(x, y)] = col
            if (x + 1, y) not in pts:
                pts[(x + 1, y)] = col2

    line(hx, hy, tx - open_px, ty, C['s1'], C['s2'])
    line(hx, hy, tx + open_px, ty - 1, C['s2'], C['s3'])
    for (x, y), c in pts.items():
        if 0 <= x < W and 0 <= y < Hh:
            p[x, y] = c
    # outline round the blades
    blade = set(pts)
    for (x, y) in list(blade):
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            q = (x + dx, y + dy)
            if q not in blade and 0 <= q[0] < W and 0 <= q[1] < Hh and not p[q][3]:
                p[q] = BLACK
    p[hx, hy] = C['b1']; p[hx + 1, hy] = C['b2']
    return out


def build(var='A'):
    b = hooded_head()
    b = mat.recolour(b, COAT)
    b = mat.recolour(b, {H('54373b'): C['c3'], H('7c495a'): C['c2'], H('863c4f'): C['c2']},
                     mat.region(b.size, rect=(26, 50, 56, 80)))                         # stockings -> charcoal
    b = mat.recolour(b, SASH, mat.region(b.size, rect=(0, 21, 79, 79)))
    # inside the cowl, right of her face: the old embroidery's black rings -> cowl shadow (the silhouette keeps its line)
    p = b.load()
    for y in range(0, 21):
        for x in range(46, 56):
            if p[x, y] == BLACK and all(p[x + dx, y + dy][3] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                p[x, y] = C['g4']
    b = mat.drop_specks(b, 6)
    # the ball goes; the hand closes on the shears' bow
    b = mat.recolour(b, {H('ffffff'): C['s2'], H('b1b1b9'): C['s3'], H('cec6c6'): C['s2'], H('df743f'): C['p2']},
                     mat.region(b.size, rect=(58, 32, 70, 44)))
    if var == 'A':
        b = mat.patch(b, 61, 33, ['.kkk.', 'k...k', 'k...k', '.kkk.'], X)            # the bow (handle) above the fist
        b = shears(b, 63, 41, 68, 66, 3)
    else:
        b = shears(b, 62, 37, 40, 58, 4)
    # thistle brooch at the collar, the torn survey flag tucked at the belt
    b = mat.patch(b, 38, 21, ['.k.', 'kpk', 'kPk', 'vVv'], X)
    b = mat.patch(b, 47, 44, ['kkkk.', 'kook.', 'kOok.', '.kOk.', '..kk.'], X)
    return b


VARIANTS = [('A', 'A: the weaver who cuts. Grey cowl round a tired, steady face, one thistle-purple sash streaming off her like a '
                  'loose thread, tailor\'s shears hanging point-down from her fist like a blade, a torn orange survey flag at '
                  'her belt, a thistle brooch. Veteran (gen 6) body, Pearl Clan hood (cloth only), hand-drawn shears.'),
            ('B', 'B: the cut. Same, with the shears raised open across her body, about to cut.')]
PICK = 'A'
REFS = [('sd:veteranf-gen6', 'Veteran F (donor class)'), ('sd:pearlclanmember', 'Pearl Clan (hood donor)'),
        ('sd:shauntal', 'Shauntal (official BW)'), ('sd:grimsley', 'Grimsley (official BW)'), ('reborn:093', 'Reborn front (Julia)')]
DONORS = [('sd:veteranf-gen6', 'veteranf-gen6: body, face, coat, scarf -> sash'),
          ('sd:pearlclanmember', 'pearlclanmember: hood cloth -> ash cowl (embroidery painted out)')]
NOTE = ('Hand pixels: shears (two 1-px steel lines with a shadow side, brass pivot, bow handle), cowl shadow inside the hood, '
        'thistle brooch (4 px), torn survey flag (5 px).')

if __name__ == '__main__':
    vs = sys.argv[1:] or ['A']
    ims = [build(v) for v in vs]
    row = Image.new('RGBA', (len(ims) * 330, 330), (40, 40, 48, 255))
    for i, im in enumerate(ims):
        im.save(OUT + '/thi_%s.png' % vs[i])
        row.paste(kb.up(kb.on_bg(im, (150, 160, 170, 255)), 4), (i * 330, 0))
    row.save('/tmp/thi.png')
    kb.grid(ims[0], k=9).save('/tmp/thi_grid.png')
