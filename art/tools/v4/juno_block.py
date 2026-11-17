"""Juno Hale, trainer front v4: BLOCK-IN (underdrawing) only.
Flat base colours, no shading, no outline. Its only job is pose, proportions and silhouette.
After approval it is baked to juno.spr and every pixel is then edited by hand in that file.
python3 -I juno_block.py OUT.spr"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from px4 import Sprite, Canvas

PAL = [
    ('K', '#1c1424', 'outline near-black'),
    ('R', '#4a1a22', 'hair dark / hair outline'),
    ('r', '#8a3428', 'hair shadow / skin deep'),
    ('h', '#c0552e', 'hair base'),
    ('H', '#e8904c', 'hair highlight'),
    ('o', '#b8601a', 'marigold shadow / glove shadow'),
    ('y', '#f39c1e', 'marigold base'),
    ('Y', '#ffd04a', 'marigold light'),
    ('s', '#eca282', 'skin shadow'),
    ('S', '#ffdcc0', 'skin'),
    ('v', '#8e7e88', 'cream deep (cool)'),
    ('w', '#d4c4ac', 'cream shadow'),
    ('W', '#f8f0d8', 'cream'),
    ('E', '#1f4636', 'green deep / eye'),
    ('e', '#3a7838', 'green shadow'),
    ('g', '#5ea83a', 'green base'),
    ('G', '#9ad050', 'green light'),
    ('T', '#e8bc78', 'glove'),
    ('d', '#42221e', 'leather dark'),
    ('b', '#74402a', 'leather'),
    ('B', '#a86a3e', 'leather light'),
    ('p', '#8c2238', 'ball red dark'),
    ('P', '#e43c3c', 'ball red'),
    ('x', '#b8bccc', 'ball grey'),
    ('X', '#ffffff', 'white'),
]


def build():
    c = Canvas()
    # ---- hair cloud (back mass): off-centre ellipse + frizz bumps; more volume behind (viewer's right)
    c.ellipse(40.5, 17, 13.5, 12, 'h')
    for (bx, by, br) in [(28.5, 11.5, 3.6), (27, 18, 3.6), (28, 24.5, 3.6), (31.5, 28, 3), (33.5, 6.5, 3.6), (40, 5, 3.6),
                         (46.5, 5.5, 3.6), (52, 9.5, 3.6), (54.5, 16, 3.8), (54, 22.5, 3.8), (51.5, 27.5, 3.4), (47.5, 29, 2.6)]:
        c.disc(bx, by, br, 'h')
    # ---- kerchief band arching over the crown, knot + two tails at upper right
    for x in range(28, 54):
        t = (x - 40.5) / 13.0
        ytop = 9.8 + 4.0 * t * t
        for y in range(int(round(ytop)), int(round(ytop + 3))):
            c.px(x, y, 'y')
    c.poly([(50, 7), (53, 2), (55, 4), (53, 9)], 'y')
    c.poly([(52, 9), (58, 7), (58, 10), (54, 11)], 'y')
    c.disc(52, 9, 1.7, 'y')
    # ---- neck
    c.poly([(38, 24), (41, 24), (41, 29), (38, 29)], 'S')
    # ---- face (12 wide, chin slightly left: head turned a touch toward viewer's left)
    c.poly([(34, 13), (45, 13), (45, 19), (44, 22), (41, 25), (38, 25), (35, 22), (34, 19)], 'S')
    c.poly([(33, 11), (46, 11), (46, 14), (44, 15), (42, 14), (40, 16), (38, 14), (36, 15), (34, 14), (33, 16)], 'h')
    c.poly([(32, 13), (35, 13), (35, 20), (33, 24), (31, 22)], 'h')
    c.poly([(44, 13), (47, 13), (48, 22), (46, 24), (45, 20)], 'h')
    # ---- torso: cream shirt (14 px shoulders, 3/4 turn: near side wider)
    c.poly([(33, 29), (46, 29), (46, 35), (45, 41), (35, 41), (34, 35)], 'W')
    # ---- far arm (viewer's right): shoulder -> elbow -> glove on the satchel
    c.limb([(45.5, 31), (49.5, 36.5)], [4.6, 4.2], 'W')
    c.limb([(49.3, 36.2), (50.2, 37.6)], [5.4, 5.4], 'W')
    c.limb([(50.3, 38), (51.3, 42.5)], [3.4, 3.2], 'S')
    # ---- satchel at the far hip
    c.poly([(46, 41), (56, 40), (57, 49), (47, 50)], 'b')
    c.poly([(46, 40), (56, 39), (56, 43), (46, 44)], 'B')
    c.ellipse(52, 44, 3.2, 3, 'T')
    # ---- dungarees: hips + bib + straps
    c.poly([(35, 41), (45, 41), (47, 48), (33, 48)], 'g')
    c.poly([(36, 32), (44, 32), (45, 42), (35, 42)], 'g')
    c.line(36, 32, 34, 29, 'g'); c.line(37, 32, 35, 29, 'g')
    c.line(44, 32, 45, 29, 'g'); c.line(43, 32, 44, 29, 'g')
    c.line(34, 30, 47, 41, 'd'); c.line(35, 30, 48, 41, 'd')
    # ---- legs: near leg planted out, far leg bent at the knee
    c.limb([(37.5, 47), (35, 57), (32.5, 65)], [7, 6.4, 6], 'g')
    c.limb([(42.8, 47), (46.5, 56.5), (46.5, 65)], [7, 6.4, 6], 'g')
    c.limb([(32.4, 64), (32.2, 66)], [7.4, 7.4], 'G')
    c.limb([(46.5, 64), (46.6, 66)], [7.4, 7.4], 'G')
    c.poly([(34, 55), (37, 55), (37, 58), (34, 58)], 'y')
    # ---- boots (chunky, toes out)
    c.poly([(28, 67), (36, 67), (36, 73), (37, 77), (25, 77), (26, 72)], 'b')
    c.poly([(43, 67), (50, 67), (51, 72), (54, 77), (43, 77), (43, 72)], 'b')
    # ---- near arm (viewer's left): raised, ball at shoulder height
    c.limb([(34.5, 31), (29.5, 36.5)], [4.6, 4.2], 'W')
    c.limb([(30, 36.2), (28.6, 37.4)], [5.4, 5.4], 'W')
    c.limb([(28.5, 37), (26, 31.5)], [3.4, 3.2], 'S')
    c.ellipse(25, 29.5, 3.2, 2.8, 'T')
    c.disc(24, 25, 3.2, 'P')
    for y in range(25, 29):
        for x in range(20, 29):
            if (x - 24) ** 2 + (y - 25) ** 2 <= 3.2 ** 2 + .25:
                c.px(x, y, 'X' if y > 25 else 'K')
    c.poly([(22, 27), (27, 26), (28, 29), (23, 30)], 'T')
    # ---- seed packets falling from the satchel
    for (x, y, col) in [(57, 50, 'Y'), (55, 54, 'P'), (58, 57, 'G')]:
        c.poly([(x, y), (x + 2, y), (x + 2, y + 3), (x, y + 3)], col)
    return c


def main():
    sp = Sprite()
    for ch, hx, name in PAL:
        sp.pal[ch] = (hx, name)
    sp.layers['main'] = build().g
    sp.save(sys.argv[1])


if __name__ == '__main__':
    main()
