"""Juno V2 "Ever-Bloom" - kitbash recipe.

Base body/pose : official BW Lady (sd:lady) - turned 3/4, holding out her sun hat (the hat becomes the bouquet).
Veil/train     : Hatsune Miku Flying-type (sd:miku-flying, Gen-5-style) flowing twin tail, flipped,
                 repainted as a sheer blossom train.
Blossoms       : Comfey's flowers (Reborn battler), repainted to the Bride Tree's ivory/blush ramp.
python3 -I tools/kitbash/juno_v2_everbloom.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, mat, show
from mat import H, BLACK, CLEAR
from PIL import Image

OUT = kb.WORK + '/passes'
R = '/home/claude/ref/games/reborn/Graphics/'

# donor colours (sd:idol)
I_BLK = (0, 0, 0, 255)
I_HAIR = [(57, 41, 41, 255), (90, 65, 57, 255), (139, 90, 57, 255)]
I_DRESS = [(123, 74, 90, 255), (205, 90, 131, 255), (238, 131, 172, 255)]
I_PANEL = [(205, 172, 115, 255), (255, 230, 131, 255)]
I_WHITE = [(164, 164, 189, 255), (222, 222, 230, 255), (255, 255, 255, 255)]

# designed ramps
HAIR = [H('4a1c16'), H('8e3624'), H('c8582e')]       # auburn: shadow, mid, light
HAIR_HI = H('f0945a')
IVORY = [H('8a6a78'), H('d8c4c4'), H('fbf1ea')]      # pinafore: shade (mauve), mid, light
BLUSH = [H('a8506a'), H('e0889c'), H('f8c4cc')]      # sash / blossom pink
PETTI = [H('9c8aa8'), H('e6dcea'), H('ffffff')]


def base():
    n, f = show.get_native('sd:idol')
    return n


def strip_ribbon(b):
    pts = mat.pts_of(b, [I_BLK, I_HAIR[0]], (17, 40, 23, 50))
    pts += [(30, 41), (30, 42), (31, 43), (32, 43), (33, 44), (34, 44), (35, 44)]
    return mat.dissolve(b, pts)


def recolour(b):
    hair_r = mat.region(b.size, rect=(28, 10, 58, 34))
    b = mat.recolour(b, dict(zip(I_HAIR, HAIR)), hair_r)
    b = mat.recolour(b, {I_PANEL[1]: HAIR_HI, I_PANEL[0]: HAIR[2]}, mat.region(b.size, rect=(28, 10, 58, 22)))
    b = mat.recolour(b, {I_PANEL[1]: BLUSH[2], I_PANEL[0]: BLUSH[1]}, mat.region(b.size, rect=(28, 22, 58, 34)))
    # heart clip (pink in hair) -> hair
    clip_r = mat.region(b.size, rect=(44, 13, 51, 20))
    b = mat.recolour(b, {I_DRESS[0]: HAIR[0], I_DRESS[1]: HAIR[1], I_DRESS[2]: HAIR[2]}, clip_r)
    body_r = mat.region(b.size, rect=(18, 30, 70, 64))
    b = mat.recolour(b, dict(zip(I_DRESS, IVORY)), body_r)
    b = mat.recolour(b, {I_PANEL[0]: BLUSH[1], I_PANEL[1]: BLUSH[2]}, body_r)
    b = mat.recolour(b, dict(zip(I_WHITE, PETTI)), mat.region(b.size, rect=(18, 50, 70, 64)))
    feet_r = mat.region(b.size, rect=(30, 64, 70, 80))
    b = mat.recolour(b, dict(zip(I_DRESS, [H('5a2a2a'), H('9a4a3a'), H('c87a5a')])), feet_r)
    return b


M_TAIL = [(255, 255, 255, 255), (208, 222, 235, 255), (192, 221, 233, 255), (181, 203, 221, 255),
          (139, 157, 185, 255), (93, 111, 140, 255), (67, 83, 109, 255)]
VEIL = [H('6a2238'), H('9a3e5a'), H('cc6a88'), H('ea9eb2'), H('f8ccd4'), H('fff0f0')]   # outline .. light


def veil():
    n, f = show.get_native('sd:miku-flying')
    reg = mat.region(n.size, [[(0, 40), (34, 40), (34, 50), (28, 60), (27, 79), (0, 79)]])
    t = mat.keep(n, reg)
    # skin/other colours that are not tail -> drop
    p = t.load()
    tail = set(M_TAIL) | {(0, 0, 0, 255)}
    for y in range(80):
        for x in range(80):
            if p[x, y][3] and p[x, y] not in tail:
                p[x, y] = CLEAR
    t = mat.recolour(t, {M_TAIL[0]: VEIL[5], M_TAIL[1]: VEIL[4], M_TAIL[2]: VEIL[4], M_TAIL[3]: VEIL[3],
                         M_TAIL[4]: VEIL[2], M_TAIL[5]: VEIL[1], M_TAIL[6]: VEIL[0], (0, 0, 0, 255): VEIL[0]})
    t = t.crop(kb.bbox(t))
    return mat.flip(t)


def comfey_flowers():
    n, f = kb.native(kb.load(R + 'Battlers/comfey.png').crop((0, 0, 192, 192)))
    n = n.crop(kb.bbox(n))
    boxes = {'red': (1, 22, 17, 38), 'yellow': (3, 36, 18, 51), 'orange': (35, 25, 47, 39), 'pinkL': (14, 41, 27, 54)}
    out = {}
    for k, bx in boxes.items():
        fl = n.crop(bx)
        # petals by luminance -> blossom ramp; keep black outline
        p = fl.load()
        cols = [c for c in set(fl.getdata()) if c[3] and c != (0, 0, 0, 255)]
        cols = [c for c in cols if not (c[1] > c[0] + 10 and c[1] > c[2])]   # drop leaf greens
        m = mat.lumrank_map(cols, [BLUSH[0], BLUSH[1], VEIL[4], VEIL[5]])
        fl = mat.recolour(fl, m)
        for y in range(fl.size[1]):
            for x in range(fl.size[0]):
                c = p[x, y]
                if c[3] and c[1] > c[0] + 10 and c[1] > c[2]:
                    p[x, y] = CLEAR
        out[k] = fl.crop(kb.bbox(fl))
    return out



L_HAIR = [(80, 48, 40, 255), (120, 72, 88, 255), (152, 112, 88, 255), (184, 120, 96, 255)]
L_DRESS = [(96, 56, 96, 255), (160, 128, 152, 255), (224, 200, 224, 255), (248, 248, 248, 255)]
L_RIB = [(80, 72, 104, 255), (208, 152, 224, 255)]


def lady():
    n, f = show.get_native('sd:lady')
    return n


def red_flower():
    n, f = kb.native(kb.load(R + 'Battlers/comfey.png').crop((0, 0, 192, 192)))
    n = n.crop(kb.bbox(n))
    import colorsys
    c = n.crop((1, 22, 17, 38)); p = c.load()
    for y in range(c.size[1]):
        for x in range(c.size[0]):
            r, g, b, a = p[x, y]
            if not a:
                continue
            h, sat, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            ok = (r, g, b) == (0, 0, 0) or (sat < 0.18 and v > 0.7) or h * 360 <= 15 or h * 360 >= 340
            if not ok:
                p[x, y] = CLEAR
    c = mat.clean_orphans(c)
    c = c.crop(kb.bbox(c))
    cols = [k for k in mat.palette_of(c) if k != (0, 0, 0, 255)]
    reds = [k for k in cols if k[0] > k[1] + 30]
    whites = [k for k in cols if k not in reds]
    c = mat.recolour(c, mat.lumrank_map(reds, [H('c0506e'), H('ec8aa2'), H('fcc8d2')]))
    c = mat.recolour(c, {w: H('fff8f0') for w in whites})          # white heart of the blossom
    c = mat.recolour(c, {(0, 0, 0, 255): H('6a2238')})
    return c


VEIL_Y = 12
VEIL_F5 = [(60, 26), (70, 36), (64, 44), (72, 52), (66, 62), (74, 70)]
VEIL_BUD = [(56, 36), (68, 46), (62, 56), (70, 64), (64, 74)]
SMALL = {'m': H('b0485e'), 'l': H('ec8aa2'), 'w': H('fcd2da'), 'c': H('f2c46a'), 'o': H('6a2238'),
         'g': H('2e5a3a'), 'G': H('5c9a5a'), 'h': H('9ccc7a')}
F5 = ['.m.m.', 'mlwlm', '.wcw.', 'mlwlm', '.m.m.']
BUD = ['.m.', 'mwm', '.m.']
LEAF = ['...gg', '..gGg', '.gGh.', 'gGg..', 'g....']


def stamp(img, x, y, rows):
    return mat.patch(img, x, y, rows, SMALL)


def compose(stage='all'):
    b = lady()
    hat_r = mat.region(b.size, [[(0, 18), (37, 18), (37, 52), (0, 52)]])
    b = mat.erase(b, hat_r)
    hair_r = mat.region(b.size, rect=(36, 6, 70, 50))
    b = mat.recolour(b, {L_HAIR[0]: HAIR[0], L_HAIR[1]: HAIR[1], L_HAIR[2]: HAIR[2]},
                     mat.mask_and(hair_r, mat.mask_not(mat.region(b.size, rect=(36, 14, 52, 36)))))
    b = mat.recolour(b, {L_HAIR[0]: HAIR[0], L_HAIR[2]: HAIR[2]}, mat.region(b.size, rect=(40, 6, 60, 14)))
    dress_r = mat.mask_not(mat.region(b.size, rect=(30, 6, 58, 30)))
    b = mat.recolour(b, dict(zip(L_DRESS, [H('8a5a6a'), H('d6b4bc'), H('f4e4e2'), H('fffaf6')])), dress_r)
    b = mat.recolour(b, {L_RIB[0]: BLUSH[0], L_RIB[1]: BLUSH[1]})
    # shift the figure left to make room for the train
    sh = Image.new('RGBA', b.size, CLEAR); sh.alpha_composite(b, (-8, 0)) if False else sh.paste(b, (-8, 0)); b = sh
    v = veil()                                   # miku-flying tail, flipped: sheer veil from the wreath
    out = mat.under(b, v, 44, VEIL_Y)
    # blossoms caught in the veil and falling from it to the floor (hand-placed 5x5 stamps)
    for (x, y) in VEIL_F5:
        out = stamp(out, x, y, F5)
    for (x, y) in VEIL_BUD:
        out = stamp(out, x, y, BUD)
    fl = red_flower(); ff = mat.flip(fl)
    # wreath: one big bloom over her right ear + a thin arc of small ones across the crown
    out.alpha_composite(ff, (45, 4))
    for (x, y) in [(31, 5), (36, 3), (41, 2)]:
        out = stamp(out, x, y, F5)
    out = stamp(out, 29, 9, BUD)
    # bouquet held at the chest: one white bloom (the Bride Tree's), small pink blossoms, leaves, ribbon tails
    white = mat.recolour(fl, {H('c0506e'): H('c48a98'), H('ec8aa2'): H('f2d8dc'), H('fcc8d2'): H('ffffff'),
                              H('fff8f0'): H('f2c46a')})
    out = stamp(out, 19, 30, LEAF)
    out = stamp(out, 30, 38, ['g....', 'Gg...', 'hGg..', '.gGg.', '..gg.'])
    out = stamp(out, 21, 38, ['..gg', '.gGg', 'gGh.', 'gg..'])
    for (x, y) in [(22, 27), (31, 29), (20, 34), (29, 35)]:
        out = stamp(out, x, y, F5)
    out = stamp(out, 27, 26, BUD)
    out.alpha_composite(white, (24, 29))
    R2 = {'r': BLUSH[0], 'p': BLUSH[1]}
    out = mat.patch(out, 30, 42, ['rp..', '.rp.', '.rp.', '..rp', '..r.'], R2)
    out = mat.patch(out, 27, 42, ['r.', 'pr', 'p.', 'r.'], R2)
    return out


if __name__ == '__main__':
    out = compose()
    out.save(OUT + '/v2_final.png')
    kb.grid(out, 8).save(kb.WORK + '/sheets/v2_final_grid.png')
