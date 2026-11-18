"""Juno V2 "Ever-Bloom" - PASS 2: the Miku tail "scarf" is replaced by a translucent veil that falls from
the wreath behind her to the floor (hand-built flat tints: over her hair it is a 45% blend so the hair
shows through; beside her it is two sheer tints with fold lines). Confetti cut to three blossoms caught
in the veil. python3 -I tools/kitbash/juno_v2_p2.py"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, mat
import juno_v2_everbloom as v2
from mat import H, BLACK, CLEAR
from PIL import Image, ImageDraw

OUT = kb.WORK + '/passes'
SHEER = [H('f6d4dc'), H('ffeef0')]        # veil in shade / in light
EDGE = H('c8788e')
FOLD = H('e8a8b8')
POLY = [(42, 6), (50, 7), (58, 20), (64, 40), (72, 60), (79, 76), (79, 79), (50, 79), (56, 60), (58, 40), (56, 20)]


def compose():
    v2.VEIL_F5, v2.VEIL_BUD = [], []
    saved = v2.veil
    v2.veil = lambda: Image.new('RGBA', (1, 1), CLEAR)
    fig = v2.compose()                          # figure, wreath, bouquet - no veil yet
    v2.veil = saved
    tail = saved()                              # Miku-Flying tail (flipped, repainted)
    veil = Image.new('RGBA', fig.size, CLEAR)
    veil.alpha_composite(tail, (48, 40))        # lower length: reaches the floor behind her heels
    veil.alpha_composite(tail, (44, 10))        # upper length: leaves the wreath
    out = mat.under(fig, veil, 0, 0)
    # translucency: where the veil crosses her hair, the hair shows through at 50%
    vp = veil.load(); fp = fig.load(); op = out.load()
    hair = set(v2.HAIR) | {v2.HAIR_HI}
    for y in range(80):
        for x in range(80):
            if vp[x, y][3] and fp[x, y] in hair and x >= 46:
                op[x, y] = mat.blend(fp[x, y], vp[x, y], 0.5)
    out = mat.reduce_colours(out, 40)
    for (x, y) in [(62, 30), (70, 56), (60, 70)]:
        out = v2.stamp(out, x, y, v2.F5)
    return out


if __name__ == '__main__':
    out = compose()
    out.save(OUT + '/v2_p2.png')
