"""Juno concept 4: EVER-BLOOM (the flower girl of a wedding that never ended). Quick 80x80 thumbnail.
python3 -I c4_everbloom.py OUT.spr"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cdraw import C, ball

PAL = [
    ('f', '#fff6f2', 'blossom white'), ('F', '#ffffff', 'blossom light'), ('a', '#e2bfd2', 'blossom shadow'),
    ('j', '#f19dbd', 'pinafore pink'), ('J', '#ffc7da', 'pink light'), ('u', '#b8608c', 'pink shadow'),
    ('w', '#eef0fb', 'blouse'), ('W', '#b9bde6', 'blouse shadow'),
    ('l', '#6fae58', 'leaf'), ('d', '#3e7446', 'leaf dark'),
    ('b', '#7a4a32', 'shoe'), ('i', '#9ff0ea', 'prism glint'), ('c', '#d9b07a', 'let-down hem band'),
]
RAMPS = {'f': ('F', 'a'), 'j': ('J', 'u'), 'w': (None, 'W')}


def build():
    c = C(PAL, RAMPS)
    # ---------------- trailing veil of blossoms (behind), sweeping right and down
    # a cascade of blossom clusters falling from the wreath like a bridal train (wisteria-like)
    import math
    for i in range(22):
        t = i / 21.0
        x = 46 + 26 * t + 3 * math.sin(t * 7)
        y = 10 + 62 * t
        r = 3.6 - 1.4 * t
        c.disc(x, y, r, 'f')
        if i % 3 == 1:
            c.disc(x + 4, y + 2, r * 0.7, 'f')
        if i % 4 == 2:
            c.disc(x - 3, y + 3, r * 0.6, 'f')
    # long frizzy hair down the back
    c.poly([(26, 14), (46, 12), (50, 30), (48, 46), (42, 50), (26, 50), (22, 40), (22, 24)], 'h')
    for (x, y, r) in [(22, 30, 3), (22, 40, 3), (25, 48, 2.8), (48, 40, 3), (46, 48, 2.6), (50, 24, 3)]:
        c.disc(x, y, r, 'h')
    # ---------------- legs + shoes (feet together, one toe turned in: shy)
    c.limb([(33, 60), (31, 72)], [5, 4], 'S'); c.limb([(40, 60), (37, 70)], [5, 4], 'S')
    c.limb([(33, 66), (31, 72)], [4.5, 4], 'w'); c.limb([(39, 65), (37, 70)], [4.5, 4], 'w')
    c.poly([(26, 72), (33, 72), (33, 76), (26, 76)], 'b'); c.poly([(34, 69), (40, 69), (39, 74), (34, 74)], 'b')
    # ---------------- outgrown flower-girl pinafore over a puff-sleeved blouse
    c.poly([(29, 30), (43, 30), (44, 40), (49, 60), (24, 60), (28, 40)], 'j')
    c.line(24, 59, 49, 59, 'c', 2)                                       # let-down hem band (she outgrew it)
    c.ell(28, 33, 4, 3.4, 'w'); c.ell(44, 33, 4, 3.4, 'w')               # puff sleeves
    # arms down, hands clasped low around the ball like a bouquet
    c.limb([(27, 35), (29, 44), (34, 49)], [4.5, 4, 3.6], 'S')
    c.limb([(45, 35), (43, 44), (38, 49)], [4.5, 4, 3.6], 'S')
    # ---------------- head tilted, wreath of never-wilting blossoms
    c.ell(36, 20, 9.5, 9.5, 'h')
    c.poly([(29, 17), (42, 16), (43, 25), (39, 29), (33, 29), (29, 25)], 'S')
    c.poly([(32, 28), (38, 28), (38, 31), (32, 31)], 'S')
    c.poly([(27, 14), (44, 12), (45, 17), (40, 16), (36, 18), (32, 16), (28, 19)], 'h')
    c.shade({'j': 2, 'h': 2, 'f': 1})
    # wreath: a ring of blossoms round the crown
    for (x, y) in [(25, 16), (28, 11), (33, 8), (38, 6), (43, 6), (47, 9), (24, 21), (49, 13)]:
        c.disc(x, y, 2.6, 'f'); c.px(x, y, 'j')
    for (x, y) in [(27, 13), (41, 7), (48, 11)]:
        c.put(x, y, ['l', 'd'])
    # bouquet: ball held in both hands with a sprig of blossom
    ball(c, 36, 50, 3)
    c.put(32, 44, ['.f.f.', 'fjfjf', '.l.l.'])
    c.disc(33, 49, 1.8, 'S'); c.disc(39, 49, 1.8, 'S')
    # face: tilted, smiling, eyes too bright (welling)
    c.put(30, 18, [
        '.RR...RR...',
        '...........',
        '.ee...ee...',
        '.XeX..XeX..',
        '.ii...ii...',
        '.s.....s...',
        '...q..q....',
        '....qq.....',
    ])
    c.put(42, 21, ['s', 's', 's'])
    # drifting petals with prism glints (imprinted: they never die)
    for (x, y) in [(12, 20), (17, 35), (8, 48), (20, 58), (60, 8), (14, 66), (56, 64), (6, 30)]:
        c.put(x, y, ['f.', 'fa'])
    for (x, y) in [(10, 18), (19, 33), (58, 6), (7, 46)]:
        c.px(x, y, 'i')
    c.outline()
    return c


if __name__ == '__main__':
    c = build()
    c.save(sys.argv[1])
