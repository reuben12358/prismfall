"""Vesper Lindqvist, pass 2 (sheet 25b): standing, tall, calm authority. python3 -I tools/kitbash/sheet_cast.py vesper_p2
  body : sd aromalady (a gentle standing class, long Eevee-brown hair flowing) -> sparkles cut, skirt -> white choir robe
  ruff : B:eevee's cream neck ruff as a capelet collar
  ribbons: the Octave's eight 2-px ribbons hanging long from her stole down behind her to the floor, spaced so each one reads
  Eevee: I:eevee at her feet, on the side where her robe is white behind it (contrast)
C = ribbons straight down behind her; D = ribbons swept by a draught to one side (more movement)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, mat, show, sheet09 as s9, vesper as v1
from mat import H, CLEAR, BLACK
from PIL import Image

NAME, SHEET = 'VESPER', '25b_vesper_p2.png'
TITLE = ('VESPER LINDQVIST, pass 2 - battle front kitbash (80-px art, file 160x160). Standing: the choir leader who hosts the Eevee '
         'gauntlet. White choir robe, Eevee\'s cream ruff for a collar, Eevee-brown hair, the Octave\'s eight ribbons hanging long '
         'from her stole, an Eevee at her feet.')
ROBE = {H('4aac7b'): H('f8f8f8'), H('417b5a'): H('c8cce0'), H('294a39'): H('8a8ea8')}


def build(var='C'):
    if var in ('A', 'B'):
        return v1.build(var)
    b = show.get_native('sd:aromalady')[0]
    b = mat.drop_specks(b, 14)                                           # the floating sparkles
    b = mat.recolour(b, ROBE, mat.region(b.size, rect=(28, 38, 60, 64)))
    b = mat.recolour(b, {H('4aac7b'): H('5a4a39'), H('ffffff'): H('8b7341')}, mat.region(b.size, rect=(14, 24, 32, 44)))  # sparkle in hair
    E = s9.donor_img('B:eevee')
    rc = E.crop((16, 22, 39, 33))
    ruff = mat.drop_specks(mat.keep(rc, mat.colour_mask(rc, [H('ffe6ac'), H('e6c594'), H('bd9c7b'), H('e6bd7b'), H('000000'),
                                                               H('734a4a')])), 4)
    b = mat.paste(b, ruff, 31, 25)
    # the ribbons, behind her
    if var == 'C':
        starts = [(36 + 2 * i, 34) for i in range(8)]
        ends = [(36 + 5 * i if 36 + 5 * i < 78 else 77, 79 - (i % 2) * 2) for i in range(8)]
    else:
        starts = [(36 + 2 * i, 34) for i in range(8)]
        ends = [(48 + 4 * i if 48 + 4 * i < 78 else 77, 76 - 3 * i) for i in range(8)]
    rib = v1.ribbons(Image.new('RGBA', b.size, CLEAR), starts, ends)
    b = mat.under(b, rib, 0, 0)
    ev = s9.donor_img('I:eevee')
    b = mat.paste(b, ev, 13, 61)
    return b


VARIANTS = [('C', 'C (pass 2): standing tall, calm, eyes on you; white choir robe, Eevee\'s cream ruff as a capelet, Eevee-brown hair '
                  'flowing, the Octave\'s eight ribbons hanging from her stole to the floor behind her, an Eevee at her feet. Aroma '
                  'Lady body, Eevee battler ruff, Eevee icon, hand-drawn ribbons.'),
            ('D', 'D (pass 2): the same, the ribbons lifted by a draught to one side.'),
            ('A', 'A (pass 1, kneeling): for comparison.')]
PICK = 'C'
REFS = v1.REFS
DONORS = [('sd:aromalady', 'aromalady: body, face, hair (sparkles cut, skirt -> robe)')] + v1.DONORS[1:]
NOTE = v1.NOTE

if __name__ == '__main__':
    vs = sys.argv[1:] or ['C']
    ims = [build(v) for v in vs]
    row = Image.new('RGBA', (len(ims) * 330, 330), (40, 40, 48, 255))
    for i, im in enumerate(ims):
        row.paste(kb.up(kb.on_bg(im, (150, 160, 170, 255)), 4), (i * 330, 0))
    row.save('/tmp/ves2.png')
