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


if __name__ == "__main__" and (len(sys.argv) < 2 or sys.argv[1] == "cut"):
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


# ---------------------------------------------------------------- recolour
SKIN = None  # donor skin kept
HAIR_SRC = [(88, 80, 56, 255), (152, 128, 112, 255), (192, 176, 128, 255)]
HAIR = [H('5a2418'), H('a8442a'), H('e07a44')]
SHIRT_SRC = [(120, 56, 48, 255), (160, 72, 64, 255), (216, 88, 56, 255)]
KNIT = [H('3a2048'), H('663a7c'), H('9a62a8')]
SHORTS = [H('2c3a48'), H('46607a'), H('6c8ca0')]   # slate
SHOE_SRC = [(48, 80, 64, 255), (96, 160, 152, 255)]
BOOT = [H('4a2a1e'), H('8a5634')]
STRAP_SRC = [(176, 176, 184, 255)]
LEATHER = [H('8a5634')]


def stage_recolour(body):
    b = body
    hair_r = mat.region(b.size, [[(36, 0), (66, 0), (66, 34), (46, 34), (36, 20)]])
    face_keep = None
    b = mat.recolour(b, dict(zip(HAIR_SRC, HAIR)), hair_r)
    torso_r = mat.region(b.size, [[(40, 31), (60, 31), (60, 44), (40, 44)], [(40, 26), (47, 26), (47, 31), (40, 31)]])
    b = mat.recolour(b, dict(zip(SHIRT_SRC, KNIT)), torso_r)
    shorts_r = mat.region(b.size, rect=(28, 42, 52, 62))
    b = mat.recolour(b, {(120, 72, 88, 255): SHORTS[0], (152, 128, 112, 255): SHORTS[1], (192, 176, 128, 255): SHORTS[2]}, shorts_r)
    feet_r = mat.region(b.size, rect=(20, 56, 54, 80))
    b = mat.recolour(b, dict(zip(SHOE_SRC, BOOT)), feet_r)
    b = mat.recolour(b, {STRAP_SRC[0]: LEATHER[0]}, torso_r)
    return b


def compose():
    import wardian
    b, body, pack = stage_cut()
    body = stage_recolour(body)
    case, top, inside = wardian.build()
    out = mat.under(body, case, 0, 0)
    out.alpha_composite(top)
    return out


if __name__ == '__main__' and len(sys.argv) > 1 and sys.argv[1] == 'compose':
    out = compose()
    out.save(OUT + '/v1_r1.png')
    kb.grid(out, 8).save(kb.WORK + '/sheets/v1_r1_grid.png')
