"""Juno V1 "Under Glass" - kitbash recipe.

Base body/pose : official BW Backpacker F (sd:backpackerf) - leaning run, thumbs-up.
The pack is cut away and replaced by a Wardian case (a travelling glass greenhouse).
python3 -I tools/kitbash/juno_v1_underglass.py [stage]
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, mat, show
from mat import H, BLACK, CLEAR
from PIL import Image

OUT = kb.WORK + '/juno'
W = 80


def base():
    n, f = show.get_native('sd:backpackerf')
    return n


PACK = [(0, 14), (47, 14), (47, 34), (44, 37), (44, 41), (40, 45), (37, 48), (26, 50), (0, 50)]


def stage_cut():
    b = base()
    pack = mat.region(b.size, [PACK])
    body = mat.erase(b, pack)
    return b, body, pack


if __name__ == '__main__':
    st = sys.argv[1] if len(sys.argv) > 1 else 'cut'
    if st == 'cut':
        b, body, pack = stage_cut()
        ov = b.copy(); p = ov.load(); r = pack.load()
        for y in range(80):
            for x in range(80):
                if r[x, y] and p[x, y][3]:
                    c = p[x, y]; p[x, y] = (min(255, c[0] // 2 + 128), c[1] // 2, c[2] // 2, 255)
        kb.grid(ov, 8).save(kb.WORK + '/sheets/v1_cutmask.png')
        kb.grid(body, 8).save(kb.WORK + '/sheets/v1_body.png')
