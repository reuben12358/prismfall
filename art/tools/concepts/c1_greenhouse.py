"""Juno concept 1: UNDER GLASS (the walking greenhouse). Quick 80x80 thumbnail.
python3 -I c1_greenhouse.py OUT.spr"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cdraw import C, ball

PAL = [
    ('b', '#c8963c', 'brass'), ('B', '#f2cf72', 'brass light'), ('o', '#7e5524', 'brass shadow'),
    ('g', '#a9ddd6', 'glass'), ('G', '#effffb', 'glass glint'), ('a', '#6fb0ad', 'glass shadow'),
    ('l', '#4f9c4a', 'leaf'), ('L', '#9fd35a', 'leaf light'), ('d', '#2c6438', 'leaf dark'),
    ('j', '#6d3b7e', 'blackberry knit'), ('J', '#9d62ad', 'knit light'), ('u', '#43224f', 'knit shadow'),
    ('t', '#3d4868', 'trouser'), ('T', '#5a6890', 'trouser light'), ('v', '#262c45', 'trouser shadow'),
    ('w', '#6b3c22', 'leather'), ('W', '#a0663a', 'leather light'), ('k', '#40241a', 'boot dark'),
    ('y', '#f0c43a', 'sock yellow'), ('f', '#e86fa0', 'bounsweet pink'), ('F', '#ffb0cc', 'bounsweet light'),
    ('c', '#fff4e0', 'label paper'),
]
RAMPS = {'b': ('B', 'o'), 'g': ('G', 'a'), 'l': ('L', 'd'), 'j': ('J', 'u'), 't': ('T', 'v'), 'w': ('W', 'k'),
         'f': ('F', None)}


def build():
    c = C(PAL, RAMPS)
    # ---------------- greenhouse pack (behind everything)
    c.poly([(37, 12), (69, 12), (69, 45), (37, 45)], 'g')          # body
    c.poly([(35, 12), (52, 1), (54, 1), (71, 12)], 'g')            # roof
    # plants inside: a tangle of leaves rising from pots at the bottom
    for (x, y, r) in [(42, 40, 4), (48, 36, 4.5), (55, 39, 4), (63, 37, 4.5), (60, 28, 4), (45, 27, 3.5), (52, 21, 3.5), (64, 18, 3)]:
        c.disc(x, y, r, 'l')
    c.rect(39, 41, 46, 44, 'w'); c.rect(58, 41, 66, 44, 'w')      # clay pots
    c.disc(66, 25, 2.2, 'f'); c.disc(43, 34, 1.6, 'f')            # little blossoms
    # frame
    for x in (37, 47, 58, 69):
        c.line(x, 12, x, 45, 'b')
    for y in (12, 28, 45):
        c.line(37, y, 69, y, 'b')
    c.line(35, 12, 53, 1, 'b'); c.line(53, 1, 71, 12, 'b'); c.line(53, 1, 53, 12, 'b')
    c.line(36, 46, 70, 46, 'o')
    # glints on the panes (diagonal strokes)
    for (x0, y0) in [(39, 15), (60, 15), (49, 31), (61, 31), (44, 6)]:
        c.line(x0, y0 + 4, x0 + 3, y0, 'G')
    # Bounsweet peeking out of the roof vent
    c.ell(53, 0.5, 3.2, 2.6, 'f')
    c.put(51, -2, ['.LdL.'])
    # sprout out of the side vent
    c.poly([(70, 20), (76, 15), (77, 18), (71, 23)], 'l')
    # paper labels on strings
    c.line(41, 28, 41, 31, 'K'); c.rect(40, 31, 43, 33, 'c')
    c.line(66, 12, 66, 15, 'K'); c.rect(65, 15, 68, 17, 'c')

    # ---------------- back leg (kicked up behind, running)
    c.limb([(37, 52), (43, 60), (51, 58)], [7, 6, 5], 't')
    c.limb([(43, 60), (51, 57)], [4.5, 4], 'y')                    # yellow sock
    c.poly([(49, 53), (55, 52), (57, 57), (52, 60), (49, 59)], 'k')   # boot sole up
    # ---------------- torso (leaning forward-left)
    c.poly([(25, 31), (40, 30), (43, 43), (40, 53), (27, 53), (23, 43)], 'j')
    # back arm: hand gripping the chest strap
    # straps: near shoulder strap down the side, chest strap with a brass buckle
    c.line(38, 30, 41, 47, 'w', 2)
    c.line(25, 40, 41, 38, 'w', 2)
    c.rect(31, 38, 33, 40, 'b')
    # ---------------- front leg (planted, stepping forward-left)
    c.limb([(30, 52), (25, 61), (22, 70)], [8, 6.5, 5], 't')
    c.limb([(25, 62), (22, 70)], [5, 4.5], 'l')                    # green sock (mismatched)
    c.poly([(16, 70), (26, 69), (27, 76), (14, 76), (14, 73)], 'k')   # big boot
    # shorts hem rolled
    c.line(20, 60, 29, 61, 'T')
    # ---------------- front arm flung out, presenting the ball
    c.limb([(26, 33), (17, 37), (10, 31)], [6, 5, 4], 'j')
    c.limb([(16, 36), (10, 31)], [4, 3.5], 'S')
    c.disc(10, 31, 2.6, 'S')
    # ---------------- head
    c.disc(42, 14, 7.5, 'h')                                       # hair puff (back), over the glass
    c.line(46, 5, 37, 17, 'c', 1)                                  # pencil through the puff
    c.px(46, 5, 'p')
    c.ell(30, 20, 9.5, 10, 'h')                                    # skull + hair
    for (x, y, r) in [(21, 16, 2.6), (21, 21, 2.2), (22, 26, 2.4), (25, 10, 2.8), (28, 8, 2.4), (31, 9, 2.8), (35, 10, 2.4), (37, 12, 2.6), (38, 23, 2.5)]:
        c.disc(x, y, r, 'h')
    c.poly([(23, 17), (35, 16), (36, 26), (32, 30), (27, 30), (23, 26)], 'S')   # face (3/4 left)
    c.poly([(22, 14), (36, 13), (37, 17), (33, 16), (30, 18), (27, 16), (24, 18)], 'h')  # bangs
    c.poly([(31, 29), (35, 29), (35, 32), (31, 32)], 'S')         # neck
    c.shade({'g': 1, 'j': 2, 't': 2, 'h': 2, 'l': 1})
    # ---- face details (after shading so they stay crisp)
    c.put(23, 17, [
        '.RR....RRR...',
        'R..e...e..e..',
        '..ee...ee....',
        '..Xd...Xd....',
        '..dd...dd....',
        '.s.....s.....',
        '.q.q.....q.q.',
        '...qmmmmq....',
        '....mnnm.....',
        '.....qq......',
    ])
    c.put(36, 20, ['s', 's', 's', 's', 's', 's'])
    ball(c, 6, 27, 4)
    c.disc(9, 31, 1.6, 'S'); c.px(10, 30, 'S'); c.px(8, 32, 's')
    # sweat drop (the greenhouse is heavy)
    c.put(19, 9, ['.X.', 'XgX', 'XaX', '.X.'])
    # a crack in one pane (what she is afraid of) and leaves trailing behind her run
    c.put(60, 30, ['K....', '.K...', '.KK..', '...K.', '...KK'])
    c.put(58, 50, ['.L.', 'Lld', '.d.'])
    c.put(66, 56, ['Ll', 'ld'])
    c.put(72, 47, ['cc', 'cc'])
    c.outline()
    return c


if __name__ == '__main__':
    c = build()
    c.save(sys.argv[1])
