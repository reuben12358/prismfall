"""PLAYER_B v3 - Leaf's stance as pose skeleton (legs + hands repainted);
head, side tail, cropped windbreaker, satchel hand-drawn.
Design: chalk white + prism teal; long plum hair in one big side tail tied
with the teal scarf."""
import numpy as np
from fs import T, remap, rect, hx
from player_a import LEG as _LA
LEG = dict(_LA)
LEG.update({'h': '#4a1e36', 'H': '#7a3654', 'J': '#a8577a', 'K': '#d088a4', 'R': '#d06878', 'p': '#262838', 'P': '#3a3e54'})
HEAD = {
 5: [(28, "0000")],
 6: [(26, "00HJJH00")],
 7: [(25, "0HJKKJJHH00")],
 8: [(24, "0HJKKJJHHHHH0")],
 9: [(23, "0HHJJJHHHHHHHH0"), (40, "00")],
 10: [(23, "0hHHHHHHHHHHHHH0II0")],
 11: [(22, "0hHHhHHHHHhHHHHH0IiI00")],
 12: [(22, "0hhHhhHHHhhHHHHhh0iIi0HH00")],
 13: [(22, "0h0hh0hhTThhhHhhhh00HHJJHH00")],
 14: [(23, "0hTTTTTTTThhTThhh0HJJKJHHH0")],
 15: [(23, "0hSTTTTTTTTTTShhh0HHJJHHHHh0")],
 16: [(23, "0hS0000TT0000Shhh0HHHHHHhhh0")],
 17: [(23, "0hS0ie0TT0ie0Shhh0hHHHHHhhh0")],
 18: [(23, "0hSTiiTTTTiiTShh0..0hHHHHhhh0")],
 19: [(23, "0hsSTTTTTTTTSsh0...0hhHHHhhh0")],
 20: [(24, "0hsSTTRRTTSs0h0....0hhHHhhh0")],
 21: [(24, "0h0sSTTTTSs00h0....0hhHHhh0")],
 22: [(24, "0h00ssSSs0.0h0......0hHHhh0")],
 23: [(25, "0.000000..00.......0hHHh0")],
 24: [(45, "0hHHh0")],
 25: [(46, "0hHh0")],
 26: [(46, "0hHh0")],
 27: [(47, "0Hh0"), (51, "0")],
 28: [(47, "0HJ0"), (50, "0H0")],
 29: [(48, "0HJ00HJ0")],
 30: [(49, "00HJJ0")],
 31: [(50, "0000")],
}
BODY = {  # cropped windbreaker: lit left, folds, teal zip + hem trim
 23: [(27, "0WWWWWWWW0")],
 24: [(25, "00WXWWWWiWWW00")],
 25: [(24, "0WXWWWWWWiWWWWw0")],
 26: [(23, "0WXWWWmWWWiWWWWww0")],
 27: [(22, "0WXWWWWWmWWiWWwWWw0")],
 28: [(21, "0WXWWWWWWWmWiWWwWWWw0")],
 29: [(20, "0WXWW0WWWWWmiWWWwWWWw0")],
 30: [(19, "0WXWW0.0WWWWWimWWwWWWw0")],
 31: [(18, "0WWWW0..0WWwWWiWmWwWWww0")],
 32: [(17, "0WWWW0...0WWwWWiWWmwWWw0")],
 33: [(16, "0iII0....0WWWwWWiWWWMmww0")],
 34: [(16, "0IIi0....0wWWwWWiWWWwMmw0")],
 35: [(16, "000.....0IIIIIIIIIIIIMMm0")],
 36: [(24, "0iiiiiiiiiiiqqMMMm0")],
 37: [(25, "0pPPPPPPPpppMgMMm0")],
 38: [(25, "0pPPPPPPPpppmMMMm0")],
 39: [(25, "0pPPPPpppppp0mmmm0")],
 40: [(25, "0ppPPp0pppppp00000")],
 41: [(26, "000000.000000")],
}
RARM = {  # right sleeve reaching down-right to Leaf's hand
 30: [(41, "0w0")],
 31: [(41, "0wW0")],
 32: [(42, "0wWW0")],
 33: [(43, "0wWW0")],
 34: [(44, "0wWW0")],
 35: [(45, "0iIi0")],
 36: [(46, "0qi0")],
}


def base():
    l = T('POKEMONTRAINER_Leaf')
    keep = rect(l, 0, 41, 63, 63) | rect(l, 8, 29, 19, 38) | rect(l, 47, 34, 56, 40)
    a = np.zeros_like(l)
    a[keep] = l[keep]
    legs = rect(a, 0, 41, 63, 63)
    a = remap(a, {'#785850': '#1e1f2c', '#c89070': '#2c2e40', '#e0b898': '#3e4258', '#f8e0b0': '#555a74',
                  '#306888': '#145e5a', '#5088b0': '#1e8a84', '#78b8d8': '#4cc4b4', '#182850': '#145e5a',
                  '#c04040': '#145e5a', '#f86058': '#1e8a84'}, legs)
    return a


def build():
    from shade import rim
    a = base()
    rows = [['.'] * 64 for _ in range(64)]
    for table in (RARM, BODY, HEAD):
        for y, spans in table.items():
            for x, s_ in spans:
                for i, ch in enumerate(s_):
                    if ch != '.' and 0 <= x + i < 64:
                        rows[y][x + i] = ch
    rows = rim([''.join(r) for r in rows], [['h', 'H', 'J', 'K'], ['v', 'w', 'W', 'X'], ['q', 'i', 'I', 'I'], ['m', 'm', 'M', 'M'], ['p', 'p', 'P', 'P']],
               keep=('g', 'e', 'R'), keep_interior=('i', 'w', 'm', 'X', 'K', 'J'))
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch != '.':
                a[y, x, :3] = hx(LEG[ch]); a[y, x, 3] = 255
    return a
