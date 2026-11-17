"""Juno concept 1 (UNDER GLASS) bubble portrait, 96x96, expression: happy / mid plant-fact. Quick, not polished.
python3 -I c1_portrait.py OUT.spr"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cdraw import C, png
from c1_greenhouse import PAL, RAMPS


def build():
    c = C(PAL, RAMPS, 96, 96)
    # ---------------- greenhouse behind her shoulder (top right)
    c.poly([(56, 6), (95, 6), (95, 70), (56, 70)], 'g')
    c.poly([(54, 6), (76, -8), (96, 4), (96, 6)], 'g')
    for (x, y, r) in [(66, 52, 7), (80, 46, 8), (90, 58, 6), (86, 28, 6), (70, 30, 5), (92, 16, 4)]:
        c.disc(x, y, r, 'l')
    c.disc(78, 24, 3, 'f'); c.disc(64, 40, 2.4, 'f')
    for x in (56, 74, 94):
        c.line(x, 6, x, 72, 'b', 2)
    for y in (6, 38, 72):
        c.line(56, y, 95, y, 'b', 2)
    for (x0, y0) in [(60, 12), (78, 12), (62, 44), (80, 44)]:
        c.line(x0, y0 + 7, x0 + 5, y0, 'G'); c.line(x0 + 2, y0 + 8, x0 + 6, y0 + 3, 'G')
    c.put(84, 42, ['K.....', '.K....', '.KK...', '...K..', '...KK.', '.....K'])   # the crack
    # ---------------- shoulders: blackberry knit, leather strap, brass buckle
    c.poly([(10, 96), (14, 82), (28, 74), (64, 74), (80, 82), (86, 96)], 'j')
    c.poly([(36, 72), (58, 72), (56, 80), (38, 80)], 'J')                      # knit collar roll
    c.line(66, 74, 74, 96, 'w', 4)
    c.rect(68, 84, 73, 89, 'b')
    # ---------------- raised hand, index finger up ("Did you know-")
    c.limb([(18, 96), (16, 82), (14, 66)], [12, 11, 9], 'j')
    c.limb([(15, 72), (14, 62)], [8, 7], 'S')
    c.ell(15, 59, 5.5, 5, 'S')                                               # fist
    c.limb([(12, 55), (11, 40)], [3.6, 3.2], 'S')                             # index finger up
    c.put(10, 39, ['.XX.'])                                                   # nail glint
    # ---------------- hair: big frizz + a puff with a pencil through it
    c.disc(70, 18, 13, 'h')
    c.line(80, 2, 58, 30, 'c', 2); c.disc(80, 3, 1.6, 'p')
    c.ell(46, 42, 25, 27, 'h')
    for (x, y, r) in [(22, 34, 6), (21, 48, 6), (24, 60, 5.5), (30, 20, 6), (40, 14, 6), (52, 14, 6), (62, 22, 6), (68, 40, 6), (66, 56, 5.5), (60, 66, 5)]:
        c.disc(x, y, r, 'h')
    # face (3/4 left) + neck
    c.poly([(27, 34), (60, 32), (62, 48), (59, 58), (51, 66), (42, 69), (34, 65), (28, 55)], 'S')
    c.poly([(42, 64), (54, 62), (54, 74), (42, 74)], 'S')
    # frizzy fringe
    c.poly([(25, 26), (62, 24), (64, 36), (57, 33), (52, 38), (46, 33), (40, 38), (34, 33), (28, 38)], 'h')
    c.shade({'h': 2, 'j': 3, 'g': 1, 'l': 2})
    # hand-placed shading under the fringe and down the near jaw
    for (x, y) in [(29, 39), (30, 39), (35, 35), (36, 35), (41, 39), (47, 35), (53, 39), (58, 35), (59, 36)]:
        c.px(x, y, 's')
    c.line(60, 40, 58, 58, 's'); c.line(58, 58, 50, 66, 's'); c.line(44, 69, 52, 69, 's')
    # ---------------- face: brows up, big green eyes, open mouth mid-sentence, freckles
    c.put(28, 37, [
        '..RRRRR.......RRRRRR..',
        '.R.....R.....R......R.',
        '......................',
        '..eeeee......eeeeeee..',
        '.eXXdde.....eXXXdddde.',
        '.eXXdde.....eXXddddde.',
        '.edddde.....edddLddde.',
        '.eddLde.....eddddLdde.',
        '.eddddde....eddddddde.',
        '..eeeee......eeeeeee..',
        '......................',
        '.nsnq.q.s....s.q.qnsn.',
        '..s.q..s.....q.q..s...',
        '......................',
        '.....qmmmmmmmmq.......',
        '....qmXXXXXXXXmq......',
        '....qmmmmmmmmmmq......',
        '....qmmnnnnnnmmq......',
        '.....qmnnnnnnmq.......',
        '......qmmmmmmq........',
        '.......qqqqqq.........',
    ])
    # tiny sweat drop of nervous energy
    c.put(64, 40, ['.X.', 'XgX', 'XaX', '.X.'])
    c.outline()
    return c


if __name__ == '__main__':
    c = build()
    c.save(sys.argv[1])
    png(c, os.path.splitext(sys.argv[1])[0] + '.png')
