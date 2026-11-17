"""Overworld frankensprites: 64x96 native charsets, 16x24 frames."""
import sys
import numpy as np
from fs import *
from pc_a import JACK, TEAL
FW, FH = 16, 24


def rows(a, y0, y1):
    """Mask of frame-relative rows y0..y1 in every frame."""
    m = np.zeros(a.shape[:2], bool)
    for fy in range(4):
        m[fy * FH + y0: fy * FH + y1 + 1, :] = True
    return m


def frame_rect(a, fx, fy, x0, y0, x1, y1):
    return rect(a, fx * FW + x0, fy * FH + y0, fx * FW + x1, fy * FH + y1)


def interior(a):
    op = a[..., 3] > 0
    p = np.pad(op, 1)
    return op & p[:-2, 1:-1] & p[2:, 1:-1] & p[1:-1, :-2] & p[1:-1, 2:]


def player_a():
    from pc_a import HAIR
    r = C('trainer_RIVAL1')
    b = C('trainer_POKEMONTRAINER_Brendan')
    # body recolour (Brendan rows 15..23): dark jacket -> white, orange -> teal, gold -> leather
    body = rows(b, 15, 23)
    legs = rows(b, 21, 23)
    b = remap(b, {'#484858': '#3e4258', '#e07050': '#3e4258', '#904028': '#232436', '#501000': '#232436'}, legs)
    b = remap(b, {'#e07050': JACK[2], '#904028': JACK[1], '#501000': JACK[0], '#484858': TEAL[1], '#889090': TEAL[0],
                  '#c0c8d8': JACK[2], '#ffffff': JACK[2], '#c8b068': '#b08458', '#787040': '#7a5a3e'}, body & ~legs)
    # head (RIVAL1 rows 0..14) with the PC hair colour
    head = rows(r, 0, 14)
    r = remap(r, {'#dfb840': HAIR[3], '#a08020': HAIR[2], '#505020': HAIR[1], '#502040': HAIR[0]}, head)
    out = b.copy()
    out[head] = 0
    out = copy(out, r, head)
    return out


def player_b():
    from pc_b import HAIR
    l = C('trainer_LASS')
    l = remap(l, {'#d0b028': HAIR[3], '#806000': HAIR[2], '#483030': HAIR[0]}, rows(l, 0, 16))
    l = remap(l, {'#483030': HAIR[1], '#806000': HAIR[2], '#d0b028': HAIR[3]}, rows(l, 17, 23) & colmask(l, ['#806000', '#d0b028']))
    l = remap(l, {'#a090f0': JACK[1], '#6850b8': '#3e4258', '#403860': '#232436', '#a84038': TEAL[0], '#e87840': '#b08458', '#ffffff': JACK[2]})
    # teal neckerchief: first body row under the chin, down/left/right frames
    for fx in range(4):
        l = patch(l, fx * FW + 6, 16, ["TT"], {'T': TEAL[1]})
        l = patch(l, fx * FW + 5, 2 * FH + 16, ["T"], {'T': TEAL[1]}) if False else l
    return l


def larch():
    from larch import HAIR, OIL
    s = C('trainer_SCIENTIST')
    face = rows(s, 9, 13)
    hair = rows(s, 0, 13)
    s = remap(s, {'#383818': HAIR[0], '#787040': HAIR[1], '#c8b068': HAIR[2]}, hair)
    s = remap(s, {'#ffffff': OIL[3], '#c0c8d8': OIL[2], '#889090': OIL[1]}, ~face)
    s = remap(s, {'#484858': '#46584f', '#383818': '#2c3a38', '#787040': OIL[1]}, rows(s, 14, 23))
    L = {'k': '#000000', 'd': HAIR[0], 'm': HAIR[1], 'l': HAIR[2], 'r': '#a8453a'}
    for fx in range(4):
        bob = 0 if fx % 2 == 0 else 1
        # up (row 3): braid down the back
        s = patch(s, fx * FW + 6, 3 * FH + 12 + bob, ["kmlk", "kdmk", "kmlk", "kdmk", ".rr.", ".kk."], L)
        # left (row 1): braid behind the head, hanging down the back
        s = patch(s, fx * FW + 11, 1 * FH + 9 + bob, ["kk.", "mlk", "dmk", "mlk", "dmk", "rk."], L)
        # right (row 2): mirrored
        s = patch(s, fx * FW + 2, 2 * FH + 9 + bob, [".kk", "klm", "kmd", "klm", "kmd", ".kr"], L)
    return s


if __name__ == '__main__':
    tag = sys.argv[1] if len(sys.argv) > 1 else 'r1'
    for name, fn in (('pca', player_a), ('pcb', player_b), ('larch', larch)):
        to_img(fn()).save(f'/home/claude/fangame/art/previews/fr/ow_{name}_{tag}.png')
