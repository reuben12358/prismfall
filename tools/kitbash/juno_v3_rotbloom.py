"""Juno V3 "Rot & Bloom" - kitbash recipe.

Base body/pose : official BW Parasol Lady (sd:parasollady) - parasol on the shoulder, free hand out.
Canopy         : Shiinotic's cap (Reborn battler, 96-px art = same pixel size) replaces the parasol.
Lantern        : Morelull (Reborn icon, 32-px art) held up in the free hand.
python3 -I tools/kitbash/juno_v3_rotbloom.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, mat, show
from mat import H, BLACK, CLEAR
from PIL import Image

OUT = kb.WORK + '/passes'
R = '/home/claude/ref/games/reborn/Graphics/'

P_CANOPY = [(152, 56, 104, 255), (184, 80, 112, 255), (200, 80, 128, 255), (232, 136, 168, 255),
            (184, 104, 144, 255), (112, 64, 80, 255), (120, 72, 88, 255), (80, 72, 104, 255), (128, 128, 128, 255)]
P_HAIR = [(48, 48, 64, 255), (80, 72, 104, 255)]
P_PINK = [(112, 64, 80, 255), (152, 56, 104, 255), (184, 80, 112, 255), (200, 80, 128, 255), (232, 136, 168, 255),
          (184, 104, 144, 255), (120, 72, 88, 255)]

HAIR = [H('4a1c16'), H('8e3624'), H('c8582e'), H('f0945a')]
LOAM = [H('2e1c18'), H('4c3024'), H('6e4a34'), H('94704c'), H('b89468')]     # coat
MOSS = [H('2a3020'), H('46502e'), H('6a7444')]                                  # boots/tights
CAP = [H('3a1a4a'), H('5e2a78'), H('8a44a2'), H('b874c4'), H('e0aee2')]        # spore violet
GILL = [H('3e3058'), H('6a5a8c'), H('9a8cc0'), H('c4b8e8')]                    # glowing gills


def base():
    n, f = show.get_native('sd:parasollady')
    return n


def cut_canopy(b):
    keep_r = mat.region(b.size, [
        [(31, 8), (49, 8), (49, 34), (31, 34)],          # head + hair
        [(16, 18), (36, 18), (36, 30), (16, 30)],        # waving arm
        [(26, 30), (50, 30), (50, 80), (26, 80)],        # body
    ])
    canopy_r = mat.mask_not(keep_r)
    b = mat.erase(b, mat.mask_and(canopy_r, mat.colour_mask(b, P_CANOPY + [BLACK])))
    # canopy pixels inside the kept boxes but outside the figure: by colour, above the shoulders, right of the head
    extra = mat.region(b.size, [[(47, 8), (50, 8), (50, 37), (44, 37), (44, 25), (47, 25)]])
    b = mat.erase(b, mat.mask_and(extra, mat.colour_mask(b, P_CANOPY)))
    pinks = [(152, 56, 104, 255), (184, 80, 112, 255), (200, 80, 128, 255), (232, 136, 168, 255), (184, 104, 144, 255)]
    b = mat.erase(b, mat.mask_and(mat.region(b.size, rect=(26, 8, 49, 29)), mat.colour_mask(b, pinks)))
    return b


def cap():
    s, f = kb.native(kb.load(R + 'Battlers/shiinotic.png').crop((0, 0, 192, 192)))
    s = s.crop(kb.bbox(s))
    c = s.crop((0, 0, s.size[0], 29))
    # remove the face/stem in the middle of the underside, patch with gill texture from the left
    face = mat.region(c.size, [[(19, 19), (37, 19), (37, 29), (19, 29)]])
    c = mat.erase(c, face)
    gills = s.crop((5, 17, 19, 25))
    c = mat.under(c, gills, 19, 17)
    c = mat.under(c, mat.flip(gills), 25, 17)
    m = {(149, 87, 131, 255): CAP[0], (203, 122, 156, 255): CAP[1], (241, 182, 226, 255): CAP[2],
         (131, 92, 143, 255): CAP[2], (155, 124, 176, 255): CAP[3], (192, 153, 219, 255): CAP[4],
         (51, 52, 45, 255): GILL[0], (111, 113, 99, 255): GILL[0], (112, 131, 86, 255): GILL[1],
         (141, 179, 132, 255): GILL[2], (163, 215, 151, 255): GILL[3], (28, 28, 28, 255): CAP[0]}
    c = mat.recolour(c, m)
    # cream spots on the cap (small, hand-placed): light top-left, shade bottom-right
    SP = {'a': H('fff6e0'), 'b': H('e8d8b8'), 'c': H('b8a088')}
    for (x, y) in [(9, 9), (22, 4), (33, 7), (44, 10), (15, 13), (39, 2)]:
        c = mat.patch(c, x, y, ['ab', 'bc'], SP)
    return c


def recolour(b):
    hair_r = mat.region(b.size, rect=(24, 8, 50, 30))
    b = mat.recolour(b, {P_HAIR[0]: HAIR[0], P_HAIR[1]: HAIR[1]}, hair_r)
    body_r = mat.region(b.size, rect=(14, 28, 52, 56))
    b = mat.recolour(b, mat.lumrank_map(P_PINK, LOAM), body_r)
    # spore-violet neckerchief ties the coat to the cap
    b = mat.recolour(b, dict(zip(LOAM, [CAP[0], CAP[1], CAP[2], CAP[3], CAP[4]])), mat.region(b.size, rect=(32, 30, 44, 33)))
    legs_r = mat.region(b.size, rect=(20, 56, 60, 80))
    b = mat.recolour(b, mat.lumrank_map(P_PINK, MOSS + [MOSS[2]]), legs_r)
    return b


def compose():
    b = base()
    b = cut_canopy(b)
    b = recolour(b)
    c = cap()
    out = Image.new('RGBA', (80, 80), CLEAR)
    out.alpha_composite(c, (14, 0))
    out = mat.under(b, out, 0, 0)
    return out


if __name__ == '__main__':
    out = compose()
    out.save(OUT + '/v3_final.png')
    kb.grid(out, 8).save(kb.WORK + '/sheets/v3_final_grid.png')
