"""Vesper Lindqvist (24, leader of the Eevee Octave, Prism Choir) battle fronts (80-px art, 160x160 export).
python3 -I tools/kitbash/vesper.py [variant ...]; sheet: sheet_cast.py vesper
Concept: THE CHOIR'S LANTERN. A gentle cantor who raised eight Glassfall orphans, kneeling to an Eevee as she knelt to
Understudy ("It hasn't decided which Imprint it belongs to yet"). White choir robe with gold trim, Eevee's own cream ruff as
her collar, Eevee-brown hair, and eight ribbon tails from her stole, one per Eeveelution (the Octave), fanned on the floor.
  A body : sd pokefanf-gen4 (BW-style class, kneeling, eyes closed, hugging a Pokemon) -> white choir robe, gold trim
     Eevee: I:eevee in her arms (the hugged doll cut); the two dolls beside her cut
     ruff : B:eevee's neck ruff (cream fur) laid on her shoulders as a collar
     ribbons: eight 1-px tails in the eight Eeveelution colours (hand-drawn straps), fanned behind her
  B : the ribbons gathered over one shoulder and falling in front (a stole), less floor, more vertical
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, mat, show, sheet09 as s9
from mat import H, CLEAR, BLACK
from PIL import Image

OUT = kb.WORK + '/passes'
NAME, SHEET = 'VESPER', '25_vesper.png'
TITLE = ('VESPER LINDQVIST (24, leader of the Eevee Octave, Prism Choir) - battle front kitbash (80-px art, file 160x160). Concept: '
         'the choir\'s lantern. Kneeling to an Eevee in a white choir robe, Eevee\'s cream ruff for a collar, and eight ribbon '
         'tails from her stole, one per Eeveelution. Gentle, devout, a little in love with the Festival.')

OCTAVE = [H('4aa0e8'), H('f8d030'), H('f07830'), H('e09ce8'), H('383040'), H('70c050'), H('98e0f0'), H('f8a0c8')]
ROBE = {H('de5a39'): H('f8f8f8'), H('8b4139'): H('c8cce0'), H('7b4a5a'): H('8a8ea8'), H('e6d54a'): H('e8c050'),
        H('ffffff'): H('fffef0'), H('c5cdd5'): H('e8c050')}


def sd(n):
    return show.get_native('sd:' + n)[0]


def ribbons(im, starts, ends):
    """eight 1-px ribbon tails, each from starts[i] to ends[i], in the Octave colours, outlined as one bundle."""
    out = im.copy(); p = out.load(); W, Hh = im.size; drawn = set()
    for i, ((x0, y0), (x1, y1)) in enumerate(zip(starts, ends)):
        mine = set()
        n = max(abs(x1 - x0), abs(y1 - y0))
        for t in range(n + 1):
            x = round(x0 + (x1 - x0) * t / n); y = round(y0 + (y1 - y0) * t / n)
            if 0 <= x < W and 0 <= y < Hh and (x, y) not in drawn and not (p[x, y][3] and p[x, y] != BLACK and (x, y) not in drawn and t < 2):
                p[x, y] = OCTAVE[i]; drawn.add((x, y)); mine.add((x, y))
                if 0 <= x + 1 < W and (x + 1, y) not in drawn:          # 2 px wide: a ribbon, not a thread
                    p[x + 1, y] = OCTAVE[i]; drawn.add((x + 1, y)); mine.add((x + 1, y))
        for (x, y) in list(mine):
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                q = (x + dx, y + dy)
                if q not in drawn and 0 <= q[0] < W and 0 <= q[1] < Hh and not p[q][3]:
                    p[q] = BLACK
    return out


def build(var='A'):
    b = sd('pokefanf-gen4')
    # cut the two dolls beside her and the one in her arms (keep her arms/hands)
    b = mat.erase(b, mat.region(b.size, [[(12, 55), (29, 55), (29, 79), (12, 79)]]))
    b = mat.erase(b, mat.region(b.size, [[(49, 57), (66, 57), (66, 79), (49, 79)]]))
    doll = mat.region(b.size, [[(20, 32), (33, 32), (36, 40), (35, 50), (30, 57), (21, 53), (19, 44)]])
    p = b.load(); dr = doll.load()
    skin = {H('ffd5bd'), H('dea47b'), H('bd7b62')}
    for y in range(b.size[1]):
        for x in range(b.size[0]):
            if dr[x, y] and p[x, y] not in skin:
                p[x, y] = CLEAR
    b = mat.erase(b, mat.region(b.size, [[(20, 55), (33, 55), (33, 66), (20, 66)]]) if False else
                  mat.mask_and(mat.region(b.size, rect=(24, 55, 33, 66)), mat.colour_mask(b, [H('ffffff'), H('c5cdd5'), BLACK, H('a47331'),
                                                                                               H('734a29'), H('62944a'), H('395a4a')])))
    b = mat.drop_specks(mat.clean_orphans(b), 6)
    b = mat.recolour(b, ROBE, mat.region(b.size, rect=(0, 44, 79, 79)))
    # the Eevee in her arms (behind her hands: under-layer, so her fingers stay on top)
    ev = s9.donor_img('I:eevee')
    b = mat.under(b, ev, 20, 37)
    # Eevee's ruff as her collar
    E = s9.donor_img('B:eevee')
    ruff = mat.keep(E.crop((16, 22, 39, 33)), mat.colour_mask(E.crop((16, 22, 39, 33)),
                    [H('ffe6ac'), H('e6c594'), H('bd9c7b'), H('e6bd7b'), H('000000'), H('734a4a')]))
    ruff = mat.drop_specks(ruff, 4)
    b = mat.paste(b, ruff, 31, 45)
    # the Octave's ribbons
    if var == 'A':
        starts = [(46 + i % 2, 49 + i) for i in range(8)]
        ends = [(50 + 4 * i if i < 7 else 76, 78 - (i % 3)) for i in range(8)]
    else:
        starts = [(44 + (i % 2), 47 + i // 2) for i in range(8)]
        ends = [(30 + 4 * i, 78) for i in range(8)]
    b = ribbons(b, starts, ends) if var == 'A' else mat.paste(b, ribbons(Image.new('RGBA', b.size, CLEAR), starts, ends), 0, 0)
    return b


VARIANTS = [('A', 'A: kneeling to the Eevee in her arms, eyes closed, Eevee\'s cream ruff as her collar, a white choir robe with '
                  'gold trim, and the Octave\'s eight ribbon tails (one per Eeveelution) fanned on the floor behind her. Poke Fan '
                  '(gen 4) body, Eevee icon, Eevee battler ruff, hand-drawn ribbons.'),
            ('B', 'B: the same with the eight ribbons gathered as a stole falling in front of her robe.')]
PICK = 'A'
REFS = [('sd:pokefanf-gen4', 'Poke Fan F (donor class)'), ('sd:lady', 'Lady (official BW)'), ('sd:jasmine', 'Jasmine (official)'),
        ('file:' + kb.WORK + '/thistle/THISTLE_A.png', 'Thistle (ours, sheet 23)')]
DONORS = [('sd:pokefanf-gen4', 'pokefanf-gen4: body, kneel, face, hair (dolls cut)'), ('I:eevee', 'Eevee icon: the Eevee in her arms'),
          ('B:eevee', 'Eevee battler: the cream neck ruff -> her collar')]
NOTE = 'Hand pixels: eight 1-px ribbon tails in the Eeveelution colours (straps), outlined as a bundle.'

if __name__ == '__main__':
    vs = sys.argv[1:] or ['A']
    ims = [build(v) for v in vs]
    row = Image.new('RGBA', (len(ims) * 330, 330), (40, 40, 48, 255))
    for i, im in enumerate(ims):
        im.save(OUT + '/ves_%s.png' % vs[i])
        row.paste(kb.up(kb.on_bg(im, (150, 160, 170, 255)), 4), (i * 330, 0))
    row.save('/tmp/ves.png')
