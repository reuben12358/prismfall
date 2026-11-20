"""Dorian Pell battle fronts (80-px art, 160x160 export). python3 -I tools/kitbash/dorian.py [variant ...]
Concept: a 56-year-old matinee idol who never left the curtain call. Plum velvet + silver; the cape and the cane he doesn't need.
  body       : sd owner (BW2 class: old gentleman, arm flung out)  -> plum velvet suit
  cape       : sd lance-lgpe cape only (body cut away)            -> deep plum outside, gold satin lining
  head edits : owner's head: glasses removed (eyes/brows hand-set), pencil moustache, pompadour wave, laugh kept
  cane       : hand-drawn straight shaft (black lacquer) + silver knob (hardware), in the hand that held the ball
  B body     : sd juggler (performer, three balls in the air) with the same head and palette
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, mat, show
from mat import H, CLEAR, BLACK
from PIL import Image

OUT = kb.WORK + '/passes'
NAME, SHEET = 'DORIAN', '18_dorian.png'
TITLE = ('DORIAN PELL - Gym 1 Warden (Normal), 56, former matinee idol. Battle front kitbash (80-px art, file 160x160). '
         'Concept: the curtain call that never ended. Plum velvet + silver, gold-lined cape, a silver-topped cane he doesn\'t need.')


def sd(n):
    return show.get_native('sd:' + n)[0]


VEL_SRC = [H('2e0e0e'), H('412a2e'), H('654550'), H('794657'), H('a86075'), H('623f49')]
VEL = [H('1e0618'), H('3c0e34'), H('64205a'), H('8c3a7e'), H('b860a6'), H('4e1446')]
SILVER = {H('ffffff'): H('f4f4fa'), H('b6b6b6'): H('c4c4d4'), H('8c8c8c'): H('8e8ea4'), H('cec6c6'): H('dcdce8'),
          H('bebec6'): H('c4c4d4'), H('84848c'): H('6e6e84'), H('515162'): H('50506a')}
X = {'k': BLACK, 's': H('ffd6be'), 'S': H('dfa57c'), 'm': H('b56251'), 'w': H('f4f4fa'), 'g': H('c4c4d4'), 'G': H('8e8ea4'),
     'd': H('50506a'), 'e': H('2a2a3a'), 'l': H('c060a0'), 'y': H('e8c060'), 'Y': H('fff0b0'), 'o': H('a07020')}


def cape():
    l = sd('lance-lgpe')
    body = mat.region(l.size, [[(36, 0), (60, 0), (60, 80), (36, 80)]])
    outer = [H('404c6e'), H('082952'), H('476984'), H('789ab6'), H('313142')]
    lining = [H('737373'), H('4d4d4d')]
    p = l.load(); b = body.load()
    for y in range(80):
        for x in range(80):
            c = p[x, y]
            if not c[3]:
                continue
            keepit = (c in outer + lining) or (c == BLACK and not b[x, y])
            if not keepit or (b[x, y] and c not in lining):
                p[x, y] = CLEAR
    l = mat.recolour(l, {H('404c6e'): H('241020'), H('082952'): H('120610'), H('476984'): H('3a1a36'), H('789ab6'): H('5a2a54'),
                         H('313142'): H('2a0626'), H('737373'): H('cfcadf'), H('4d4d4d'): H('9690ae')})
    l = mat.erase(l, mat.region(l.size, rect=(58, 0, 79, 52)))     # Lance's hand and loose outline on the right
    return mat.clean_orphans(l)


def head_edits(im, ox, oy):
    """owner's head at offset (ox, oy): glasses off, eyes + brows, moustache, pompadour."""
    P = lambda x, y, rows: mat.patch(im, x + ox, y + oy, rows, X)
    im = P(24, 12, ['.s.....s.....',
                    'sSs...sSss...',
                    '.ss.s.ss.s...'])                 # wipe frames across the eye line (skin)
    im = P(25, 11, ['.dd....dd.', '..........', '.ke.....ke'])   # silver brows, then dark eyes
    im = P(26, 14, ['S.....S'])                       # lower-lid shading
    im = P(28, 18, ['GgggG.'])                       # pencil moustache over the laugh
    im = P(25, 0, ['...wwg..', '.wwwwggd', 'wwgg..d.'])  # the pompadour wave
    return im


def owner_body():
    o = sd('owner')
    o = mat.recolour(o, dict(zip(VEL_SRC, VEL)))
    o = mat.recolour(o, SILVER)
    # the ball hand: ball out, a fist round the cane
    keep_sleeve = set(VEL)
    reg = mat.region(o.size, rect=(8, 36, 18, 47)).load(); p = o.load()
    for y in range(80):
        for x in range(80):
            if reg[x, y] and p[x, y] not in keep_sleeve:
                p[x, y] = CLEAR
    return o


def cane(im, x0, y0, x1, y1):
    """straight lacquered shaft from (x0,y0) (knob end) to (x1,y1); silver knob at the top end."""
    n = max(abs(x1 - x0), abs(y1 - y0))
    p = im.load()
    for i in range(n + 1):
        x = round(x0 + (x1 - x0) * i / n); y = round(y0 + (y1 - y0) * i / n)
        for dx, c in ((0, H('1a1a24')), (1, H('4a4a60'))):
            if 0 <= x + dx < 80 and 0 <= y < 80:
                p[x + dx, y] = c
    return mat.patch(im, x0 - 1, y0 - 2, ['.kkk.', 'kwggk', 'kgGdk', '.kdk.'], X)


def clean_lines(im):
    # drop black runs left over from Lance's body that no longer border any colour
    p = im.load(); out = im.copy(); q = out.load()
    for y in range(80):
        for x in range(80):
            if p[x, y] == BLACK:
                ok = False
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        xx, yy = x + dx, y + dy
                        if 0 <= xx < 80 and 0 <= yy < 80 and p[xx, yy][3] and p[xx, yy] != BLACK:
                            ok = True
                if not ok:
                    q[x, y] = CLEAR
    return out


def build(var='A'):
    if var == 'A':
        fig = Image.new('RGBA', (80, 80), CLEAR)
        fig.paste(owner_body(), (6, 0))
        fig = head_edits(fig, 6, 0)
        out = mat.under(fig, cape(), -6, -2)
        out = cane(out, 10, 16, 26, 68)
        out = mat.patch(out, 15, 39, ['.kkkk', 'kssSk', 'ksSSk', 'kSSmk', '.kkk.'], X)     # fist round the shaft
        out = clean_lines(out)
        return out
    if var == 'B':
        return juggler()
    return build('A')


def juggler():
    j = sd('juggler')
    src = sorted(set(c for c in mat.palette_of(j)), key=kb.lum)
    reds = [c for c in src if c[0] > c[1] + 40 and c[0] > c[2] + 40 and kb.lum(c) < 150]
    j = mat.recolour(j, mat.lumrank_map(reds, VEL[:5]))
    o = sd('owner')
    hd = mat.keep(o, mat.region(o.size, [[(20, 0), (40, 0), (40, 22), (20, 22)]]))
    hd = mat.recolour(hd, SILVER)
    j = mat.erase(j, mat.region(j.size, [[(24, 2), (46, 2), (46, 24), (24, 24)]]))
    t = Image.new('RGBA', (80, 80), CLEAR); t.paste(hd, (5, 2)); j.alpha_composite(t)
    j = head_edits(j, 5, 2)
    return j


VARIANTS = [('A', "A: curtain call. One arm flung to the house, the cane hoisted like a baton, laughing; a gold-lined "
                  "plum cape fans out behind. Owner class body in velvet, Lance's cape, glasses off, moustache + pompadour."),
            ('B', 'B: the house loves a show. Juggling three Poke Balls in a velvet tailcoat (Juggler class body, same head).')]
PICK = 'A'
REFS = [('sd:gentleman', 'Gentleman (official BW)'), ('sd:grimsley', 'Grimsley (official BW)'), ('sd:alder', 'Alder (official BW)'),
        ('rejuv:139', 'Rejuvenation front (Angie)')]
DONORS = [('sd:owner', 'owner: body, arm flung out, head (laugh kept)'), ('sd:lance-lgpe', 'lance-lgpe: cape only, repainted plum/gold'),
          ('sd:juggler', 'juggler: body for B, balls')]
NOTE = 'Hand pixels: eyes and brows where the glasses were, pencil moustache, pompadour wave, the cane (straight shaft + silver knob) and the fist round it.'

if __name__ == '__main__':
    vs = sys.argv[1:] or ['A']
    ims = [build(v) for v in vs]
    row = Image.new('RGBA', (len(ims) * 330, 330), (40, 40, 48, 255))
    for i, im in enumerate(ims):
        im.save(OUT + '/dor_%s.png' % vs[i])
        row.paste(kb.up(kb.on_bg(im, (150, 160, 170, 255)), 4), (i * 330, 0))
    row.save('/tmp/dor.png')
