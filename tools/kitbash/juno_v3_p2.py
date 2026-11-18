"""Juno V3 "Rot & Bloom" - PASS 2: head swapped for the BW Lass's (sd:lass: long flying hair, open laugh),
so the figure is no longer the Parasol Lady's face and bob. python3 -I tools/kitbash/juno_v3_p2.py"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, mat, show
import juno_v3_rotbloom as v3
from mat import H, BLACK, CLEAR
from PIL import Image

OUT = kb.WORK + '/passes'


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
    h = mat.recolour(h, {(64, 40, 8, 255): v3.HAIR[0], (88, 56, 40, 255): v3.HAIR[1]})
    return mat.clean_orphans(h)


def compose(dx=5, dy=0):
    b = v3.base()
    b = v3.cut_canopy(b)
    b = v3.recolour(b)
    # remove the Parasol Lady's head (hair + face) above the collar
    head = mat.region(b.size, [[(31, 8), (49, 8), (49, 29), (44, 30), (36, 30), (31, 27)]])
    b = mat.erase(b, head)
    h = Image.new('RGBA', b.size, CLEAR); h.paste(lass_head(), (dx, dy))
    b.alpha_composite(h)
    out = Image.new('RGBA', (80, 80), CLEAR)
    out.alpha_composite(v3.cap(), (14, 0))
    return mat.under(b, out, 0, 0)


if __name__ == '__main__':
    out = compose()
    out.save(OUT + '/v3_p2.png')
    kb.contact([('p2', out.crop((10, 0, 74, 48)))], 1, (64 * 8, 48 * 8), k=8).save(kb.WORK + '/sheets/v3_p2_8x.png')
