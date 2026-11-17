"""Juno concept 3: SEED BOMBER (guerrilla gardener, pitcher's windup). Quick 80x80 thumbnail.
python3 -I c3_seedbomb.py OUT.spr"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cdraw import C, ball

PAL = [
    ('j', '#f2c03a', 'dandelion jacket'), ('J', '#ffe68a', 'dandelion light'), ('u', '#b07e26', 'dandelion shadow'),
    ('y', '#c4623a', 'terracotta'), ('Y', '#ee915c', 'terracotta light'), ('o', '#7e3426', 'terracotta dark / strap'),
    ('t', '#3e5f7c', 'denim'), ('T', '#5f84a6', 'denim light'), ('v', '#283e55', 'denim shadow'),
    ('b', '#7a5236', 'clay ball'), ('B', '#a9774e', 'clay light'), ('k', '#4a2f22', 'clay shadow'),
    ('l', '#5fae48', 'sprout'), ('w', '#f2efe6', 'sock white'), ('W', '#cfcadb', 'sock shadow'),
    ('g', '#2f3a52', 'sneaker'), ('d', '#3b6e3a', 'iris green'),
]
RAMPS = {'j': ('J', 'u'), 'y': ('Y', 'o'), 't': ('T', 'v'), 'b': ('B', 'k'), 'w': (None, 'W')}


def build():
    c = C(PAL, RAMPS)
    # ---------------- one huge frizzy ponytail flung out behind (under the throwing arm): counter-line to the throw
    c.poly([(45, 12), (58, 13), (72, 14), (66, 18), (75, 22), (63, 23), (68, 28), (55, 24), (46, 22)], 'h')
    for (x, y, r) in [(58, 16, 3), (64, 20, 2.6), (60, 24, 2), (69, 17, 2)]:
        c.disc(x, y, r, 'h')
    # ---------------- throwing arm cocked back (behind the head)
    c.limb([(47, 28), (57, 23), (61, 13)], [7, 6, 5], 'j')
    c.limb([(58, 21), (61, 13)], [5, 4.5], 'S')
    # ---------------- planted back leg
    c.limb([(43, 46), (48, 60), (52, 71)], [9, 7, 6], 'S')
    c.limb([(48, 61), (52, 71)], [6, 5.5], 'w')
    c.poly([(47, 70), (57, 70), (62, 75), (61, 77), (46, 77)], 'g')
    # ---------------- torso coiled back, jacket
    c.poly([(33, 25), (48, 24), (49, 38), (47, 47), (35, 48), (32, 38)], 'j')
    c.poly([(34, 41), (48, 40), (50, 50), (33, 51)], 't')                 # cut-off shorts
    # slingshot in the back pocket
    c.put(48, 39, ['o.o', 'oo.', '.o.', '.o.'])
    # ---------------- raised front leg (knee high, pointing at the target)
    c.limb([(37, 47), (27, 43), (29, 55)], [9, 7, 6], 'S')
    c.limb([(37, 47), (29, 44)], [9, 7.5], 't')
    c.limb([(28, 47), (29, 55)], [6, 5.5], 'w')
    c.poly([(23, 54), (33, 54), (34, 59), (21, 59)], 'g')
    # ---------------- glove arm pointing at the target
    c.limb([(34, 28), (24, 31), (15, 27)], [7, 6, 5], 'j')
    c.limb([(22, 30), (15, 27)], [4.5, 4], 'S')
    c.disc(14, 27, 2.4, 'S'); c.line(9, 25, 13, 26, 'S')               # pointing finger
    # ---------------- head: two frizzy space-bun puffs, sweatband
    c.ell(40, 15, 9.5, 9, 'h')
    for (x, y, r) in [(30, 16, 2.8), (30, 22, 2.6), (32, 26, 2), (50, 15, 2.8), (50, 21, 2.8), (48, 26, 2.2)]:
        c.disc(x, y, r, 'h')
    c.poly([(33, 13), (46, 13), (46, 20), (43, 24), (39, 26), (35, 24), (33, 20)], 'S')
    c.poly([(38, 24), (42, 24), (42, 28), (38, 28)], 'S')
    c.poly([(30, 10), (50, 10), (50, 13), (30, 13)], 'y')               # terracotta sweatband
    # ---------------- bandolier of seed bombs (one is a Poke Ball)
    c.line(33, 26, 47, 45, 'o', 3)
    c.shade({'j': 2, 't': 1, 'h': 1, 'y': 1, 'S': 1})
    for i, (x, y) in enumerate([(35, 29), (38, 33), (41, 37), (44, 41)]):
        if i == 2:
            ball(c, x, y, 2)
        else:
            c.disc(x, y, 2.1, 'b'); c.px(x - 1, y - 1, 'B'); c.px(x, y - 3, 'l'); c.px(x + 1, y - 3, 'l')
    # seed bomb in the cocked hand, sprouting
    c.disc(61, 9, 3.4, 'b'); c.put(59, 7, ['B.', '.B']); c.put(61, 3, ['.l', 'll', 'l.'])
    # face: aiming squint, tongue out of the corner of the mouth
    c.put(33, 14, [
        'RRR...RRRR..',
        '.......RR...',
        '.ee...eqqe..',
        '.Xd.........',
        '.dd.........',
        'q.q...q.q...',
        '..qqqqn.....',
        '......nn....',
    ])
    c.put(45, 16, ['s', 's', 's', 's', 's'])
    # dust kicked up at the planted foot
    c.put(63, 72, ['.W.', 'W.W'])
    c.put(66, 74, ['W'])
    c.outline()
    return c


if __name__ == '__main__':
    c = build()
    c.save(sys.argv[1])
