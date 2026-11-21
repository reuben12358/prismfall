"""player2_design.py - silhouette thumbnails (STYLE_GUIDE 2.1) for the player pair, v2 redo.
Same body and pose per character, eight head/prop ideas each, filled black at true front size (80x80).
python3 -I art/research/scripts/player2_design.py  -> art/work/redo_v2/PLAYER_A|B/sil_*.png"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from p2kit import Spr, capsule, ell, black

OUT = '/home/claude/fangame/art/work/redo_v2/'


def body_m(s):
    s.poly('x', ell(40, 17, 8, 9))
    s.rect('x', 37, 25, 43, 28)
    s.poly('x', [(29, 28), (51, 28), (52, 36), (50, 46), (30, 46), (28, 36)])
    s.poly('x', [(31, 45), (49, 45), (50, 52), (30, 52)])
    s.poly('x', capsule((35, 50), (33, 62), 4, 3.5)); s.poly('x', capsule((33, 62), (32, 73), 3.5, 3))
    s.poly('x', capsule((45, 50), (47, 62), 4, 3.5)); s.poly('x', capsule((47, 62), (48, 73), 3.5, 3))
    s.poly('x', ell(30, 75, 4.5, 2.5)); s.poly('x', ell(50, 75, 4.5, 2.5))
    s.poly('x', capsule((30, 30), (25, 39), 3, 2.5)); s.poly('x', capsule((25, 39), (24, 46), 2.5, 2.2))
    s.poly('x', ell(24, 47, 2.6, 2.6)); s.poly('x', ell(21, 48, 3, 3))           # hand + ball
    s.poly('x', capsule((50, 30), (55, 37), 3, 2.5)); s.poly('x', capsule((55, 37), (52, 29), 2.5, 2.2))  # hand on the rope


def body_f(s):
    s.poly('x', ell(40, 17, 7.5, 8.5))
    s.rect('x', 37, 24, 42, 28)
    s.poly('x', [(31, 28), (49, 28), (50, 35), (48, 44), (32, 44), (30, 35)])
    s.poly('x', [(31, 43), (49, 43), (52, 52), (28, 52)])                          # skirt / shorts
    s.poly('x', capsule((36, 50), (33, 62), 3, 2.6)); s.poly('x', capsule((33, 62), (31, 73), 2.6, 2.3))
    s.poly('x', capsule((44, 50), (48, 61), 3, 2.6)); s.poly('x', capsule((48, 61), (51, 72), 2.6, 2.3))
    s.poly('x', ell(30, 75, 4, 2.5)); s.poly('x', ell(52, 74, 4, 2.5))
    s.poly('x', capsule((32, 30), (27, 25), 2.6, 2.2)); s.poly('x', capsule((27, 25), (24, 17), 2.2, 2))  # waving arm up
    s.poly('x', ell(24, 15, 2.8, 2.6))
    s.poly('x', capsule((48, 30), (51, 38), 2.6, 2.2)); s.poly('x', capsule((51, 38), (49, 44), 2.2, 2))
    s.poly('x', ell(48, 45, 2.4, 2.4))


def duffel(s, x=56, y=34, rx=8, ry=12, rot=0.25):
    s.poly('x', ell(x, y, rx, ry, rot=rot)); s.line('x', [(52, 29), (54, 23)], 2)


BOY = {
    'A1 bucket hat + duffel': lambda s: (s.poly('x', [(30, 15), (31, 9), (36, 5), (44, 5), (49, 9), (50, 15), (53, 17), (27, 17)]), duffel(s)),
    'A2 docker cap + duffel': lambda s: (s.poly('x', [(31, 13), (32, 6), (38, 3), (45, 4), (49, 8), (49, 13)]), duffel(s)),
    'A3 swept hair + duffel': lambda s: (s.poly('x', [(30, 18), (30, 10), (35, 5), (43, 4), (50, 6), (54, 4), (51, 10), (50, 18), (46, 12), (38, 12)]), duffel(s)),
    'A4 hood bunched + cowlick': lambda s: (s.poly('x', [(31, 14), (33, 7), (39, 4), (41, 1), (43, 4), (48, 8), (49, 14)]),
                                           s.poly('x', [(27, 26), (33, 23), (47, 23), (53, 26), (52, 31), (28, 31)])),
    'A5 long scarf tail (v3)': lambda s: (s.poly('x', [(31, 14), (32, 7), (38, 3), (44, 4), (49, 9), (49, 14)]),
                                          s.poly('x', [(36, 26), (46, 26), (58, 30), (70, 27), (76, 31), (66, 34), (56, 34), (46, 30)])),
    'A6 cap backward + satchel': lambda s: (s.poly('x', [(31, 12), (33, 6), (40, 4), (47, 6), (49, 12), (55, 13), (55, 15), (49, 15)]),
                                            s.poly('x', ell(52, 48, 6, 5))),
    'A7 goggles up + duffel': lambda s: (s.poly('x', [(31, 14), (32, 7), (38, 4), (45, 4), (49, 9), (49, 14)]),
                                         s.poly('x', ell(35, 9, 3, 3)), s.poly('x', ell(45, 9, 3, 3)), duffel(s)),
    'A8 sou\'wester + duffel': lambda s: (s.poly('x', [(29, 14), (31, 7), (37, 4), (45, 4), (49, 8), (51, 14), (56, 22), (50, 20), (30, 17)]), duffel(s)),
}

GIRL = {
    'B1 bucket hat + low tails': lambda s: (s.poly('x', [(31, 14), (32, 8), (37, 4), (44, 4), (48, 8), (49, 14), (52, 16), (28, 16)]),
                                           s.poly('x', capsule((33, 22), (28, 29), 2.5, 1.5)), s.poly('x', capsule((47, 22), (52, 29), 2.5, 1.5))),
    'B2 long side braid': lambda s: (s.poly('x', [(32, 16), (32, 9), (37, 6), (44, 6), (48, 10), (48, 18)]),
                                    s.poly('x', capsule((47, 20), (50, 44), 2.5, 1.5))),
    'B3 high side tail': lambda s: (s.poly('x', [(32, 16), (32, 9), (37, 6), (44, 6), (48, 10), (48, 18)]),
                                   s.poly('x', [(46, 8), (53, 5), (60, 10), (62, 20), (59, 30), (56, 20), (50, 12)])),
    'B4 wind-blown hair': lambda s: (s.poly('x', [(32, 20), (31, 10), (37, 6), (45, 6), (52, 9), (62, 12), (70, 18), (60, 20), (64, 26), (52, 24), (49, 22)])),
    'B5 sailcloth bow + long': lambda s: (s.poly('x', [(31, 26), (31, 10), (37, 6), (44, 6), (49, 10), (50, 28), (46, 30), (46, 20), (35, 20), (34, 30)]),
                                         s.poly('x', [(41, 6), (47, 0), (52, 2), (49, 7), (53, 10), (48, 12)])),
    'B6 hooded anorak, hood up': lambda s: (s.poly('x', [(30, 22), (30, 12), (34, 6), (40, 4), (46, 6), (50, 12), (51, 26), (46, 28), (34, 28)])),
    'B7 twin rope tails + band': lambda s: (s.poly('x', [(31, 16), (32, 9), (37, 6), (44, 6), (48, 10), (49, 16)]),
                                           s.poly('x', capsule((31, 16), (25, 30), 2.6, 1.6)), s.poly('x', capsule((49, 16), (55, 30), 2.6, 1.6)),
                                           s.poly('x', ell(32, 15, 2, 2)), s.poly('x', ell(48, 15, 2, 2))),
    'B8 short tails + duffel': lambda s: (s.poly('x', [(31, 16), (32, 9), (37, 6), (44, 6), (48, 10), (49, 16)]),
                                         s.poly('x', [(31, 14), (25, 12), (23, 17), (30, 18)]), s.poly('x', [(49, 14), (55, 12), (57, 17), (50, 18)]),
                                         s.poly('x', ell(57, 42, 7, 10, rot=0.2))),
}


def thumbs(kind):
    table, body = (BOY, body_m) if kind == 'A' else (GIRL, body_f)
    out = {}
    for name, f in table.items():
        s = Spr(80, 80); s.ramp('x', '000000', '000000', '000000', '000000')
        body(s); f(s); s.fill('x')
        out[name] = black(s.image())
    return out


if __name__ == '__main__':
    for k in 'AB':
        d = OUT + 'PLAYER_%s/' % k; os.makedirs(d, exist_ok=True)
        for n, im in thumbs(k).items():
            im.save(d + 'sil_%s.png' % n.split()[0])
    print('ok')
