"""Juno concept 2: ROT & BLOOM (the compost forager / living toadstool). Quick 80x80 thumbnail.
python3 -I c2_compost.py OUT.spr"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cdraw import C, ball

PAL = [
    ('v', '#8c4aa0', 'cap violet'), ('V', '#c77fd6', 'cap light'), ('u', '#58306c', 'cap shadow'),
    ('c', '#f4e7c8', 'spot cream'), ('C', '#fffaf0', 'glow white'), ('g', '#f0a6ff', 'spore glow'),
    ('l', '#6a4932', 'loam coat'), ('L', '#956a48', 'loam light'), ('d', '#40291e', 'loam shadow'),
    ('w', '#5b6838', 'welly olive'), ('W', '#7f8f4c', 'welly light'), ('o', '#353d21', 'welly shadow'),
    ('t', '#c79a5c', 'wicker'), ('T', '#e6c182', 'wicker light'), ('k', '#8a6034', 'wicker shadow'),
    ('j', '#a03c3c', 'scarf'), ('J', '#d0605a', 'scarf light'), ('z', '#6c2430', 'scarf shadow'),
    ('i', '#b0e86a', 'eye glow green'),
]
RAMPS = {'v': ('V', 'u'), 'l': ('L', 'd'), 'w': ('W', 'o'), 't': ('T', 'k'), 'j': ('J', 'z')}


def build():
    c = C(PAL, RAMPS)
    # ---------------- basket (behind, right)
    c.poly([(55, 62), (75, 62), (73, 76), (57, 76)], 't')
    c.ell(61, 60, 3.5, 2.5, 'v'); c.rect(60, 61, 62, 63, 'c')      # mushrooms in the basket
    c.ell(68, 59, 3, 2.2, 'l'); c.rect(67, 60, 69, 62, 'c')
    c.line(54, 61, 76, 61, 'k')
    c.line(65, 56, 72, 50, 'x'); c.line(72, 50, 74, 49, 'w', 2)     # trowel handle sticking out
    # ---------------- crouched body: knees wide, coat pooled (the toadstool stalk), leaning left
    c.poly([(24, 31), (44, 31), (52, 46), (56, 68), (50, 74), (20, 74), (14, 68), (17, 46)], 'l')
    c.ell(18, 58, 8, 6.5, 'l'); c.ell(53, 59, 8, 6.5, 'l')             # knees out wide
    c.poly([(11, 66), (24, 65), (25, 76), (8, 76), (8, 72)], 'w')       # wellies, toes out
    c.poly([(48, 66), (60, 65), (64, 76), (47, 76)], 'w')
    c.poly([(33, 44), (37, 44), (39, 72), (31, 72)], 'd')              # coat parting between the knees
    # scarf, one tail flying back
    c.poly([(23, 30), (45, 30), (44, 36), (24, 36)], 'j')
    c.poly([(42, 33), (49, 31), (60, 36), (58, 40), (47, 38)], 'j')
    # back hand on the knee, a worm wriggling over the fingers
    c.limb([(46, 38), (54, 47), (54, 54)], [6, 5, 4.5], 'l')
    c.disc(54, 55, 2.6, 'S')
    # ---------------- front arm thrust at the viewer (foreshortened), glowing mushroom
    c.limb([(26, 37), (16, 43), (12, 44)], [8, 7, 6], 'l')
    c.disc(11, 44, 3.6, 'S')
    # ---------------- head under a huge toadstool cap, tilted
    c.ell(34, 26, 10, 9, 'h')
    for (x, y, r) in [(23, 25, 3), (24, 31, 2.6), (45, 24, 3), (45, 30, 2.6), (22, 29, 2)]:
        c.disc(x, y, r, 'h')
    c.poly([(27, 20), (41, 20), (42, 30), (38, 34), (30, 34), (26, 30)], 'S')
    # cap: wide dome with a wavy lip, tilted (left side low)
    c.poly([(9, 23), (14, 12), (24, 5), (38, 2), (52, 4), (61, 10), (63, 17), (60, 19), (50, 19), (40, 20), (30, 21), (20, 23), (12, 25)], 'v')
    c.shade({'l': 2, 'v': 2, 'w': 1, 'h': 1})
    # cap underside (gills) and spots
    c.line(12, 25, 30, 22, 'd'); c.line(30, 22, 61, 19, 'd')
    c.line(14, 26, 30, 23, 'u'); c.line(30, 23, 58, 20, 'u')
    for (x, y, r) in [(24, 11, 2.4), (37, 7, 2.2), (50, 9, 2.2), (16, 18, 1.8), (32, 15, 1.6), (57, 14, 1.5), (44, 14, 1.4)]:
        c.disc(x, y, r, 'c')
    # baby mushrooms sprouting on the cap
    c.put(42, 0, ['.vv.', 'vVvv', '.c..', '.c..'])
    # face in the brim's shadow, lit from below by the mushroom
    c.rect(27, 23, 41, 24, 's')
    c.put(27, 23, [
        'RRR.....RRR..',
        '.............',
        '.eee....eee..',
        '.eXe....eXe..',
        '.eie....eie..',
        '.............',
        'qXXXXXXXXq...',
        '.qmmmmmmq....',
        '..qnnnnq.....',
    ])
    # glowing mushroom thrust out + spores
    c.rect(9, 40, 12, 45, 'c')
    c.ell(10, 36, 7, 4.2, 'g'); c.line(4, 38, 17, 38, 'v'); c.put(6, 33, ['CCC.', 'CC..'])
    for (x, y) in [(2, 29), (15, 28), (7, 26), (19, 32), (1, 35), (20, 27), (11, 24), (4, 23)]:
        c.px(x, y, 'g')
    c.px(3, 30, 'C'); c.px(16, 31, 'C'); c.px(12, 25, 'C')
    c.disc(11, 44, 2.2, 'S')
    # a jar of worms on the belt + a labelled pocket
    c.put(19, 45, ['.KKKK.', 'KggggK', 'KgnngK', 'KnggnK', '.KKKK.'])
    c.rect(41, 52, 46, 56, 'L'); c.line(41, 52, 46, 52, 'd'); c.rect(42, 54, 45, 54, 'c')
    # worm over the knee hand
    c.put(51, 52, ['.nn..', 'n..n.', '....n'])
    c.outline()
    return c


if __name__ == '__main__':
    c = build()
    c.save(sys.argv[1])
