"""PLAYER_A v3 - Red's throw as pose skeleton (legs + ball hand repainted);
head, windbreaker, scarf, satchel hand-drawn.  Design: chalk white + prism
teal, a long teal scarf whose frayed tail streams out behind."""
import numpy as np
from fs import T, remap, rect, hx
LEG = {
    '0': '#1a1820', 'h': '#3a3648', 'H': '#5e5a70', 'J': '#8a84a2', 'K': '#b8b2cc',
    's': '#c48466', 'S': '#eab496', 'T': '#fcd8bc', 'e': '#ffffff', 'i': '#1e8a84', 'I': '#4cc4b4', 'q': '#145e5a',
    'w': '#a8a8bc', 'W': '#e6e6ee', 'X': '#ffffff', 'v': '#7c7c94',
    'm': '#6a4a30', 'M': '#9a7048', 'g': '#d8c070',
}
S = {
 4: [(29, "0"), (34, "0")],
 5: [(28, "0J0"), (33, "0J0"), (38, "0")],
 6: [(25, "0.0HJH00HJH00J0")],
 7: [(24, "0J00HJJHHHJJHHJH0")],
 8: [(24, "0HJJHHJJHHHHJHHH0")],
 9: [(23, "0HHHJJHHHHHHHHHHHh0")],
 10: [(23, "0hHHHHHHHHHHHHHHhh0")],
 11: [(22, "0hhHHHHHhHHHHHHHhhh0")],
 12: [(23, "0hhHhHhhhhHHhhhhhh0")],
 13: [(24, "0hh0hhTThhhhThhs0")],
 14: [(24, "0h0TTTTTTThhTTss0")],
 15: [(25, "0STTTTTTTTTTSss0")],
 16: [(25, "0Sh0TTTTh0TTSs0")],
 17: [(25, "0S0ie0TT0ie0Ss0")],
 18: [(25, "0STiiTTTTiiTSs0")],
 19: [(25, "0sSTTTTTTTTSs0")],
 20: [(26, "0sSTTs0TTSs0")],
 21: [(26, "0ssSTTTTSs0")],
 22: [(27, "00ssSSs00")],
}
SCARF = {
 12: [(51, "00"), (55, "0")],
 13: [(48, "00Ii0"), (54, "0I0")],
 14: [(45, "00IiiI00iI0")],
 15: [(42, "00IIiiiiiIIi0")],
 16: [(40, "0IIiiiiiiiI00")],
 17: [(39, "0IiiiiIiq00")],
 18: [(38, "0Iiiiq00")],
 19: [(38, "0iiq0")],
 20: [(37, "0Iiq0")],
 21: [(36, "0IIiq0")],
 22: [(25, "0IIIIiii0"), (35, "0IIiiq0")],
 23: [(24, "0IIIIIiiiiiIIIIiq0")],
 24: [(24, "0qIIiiiiiiiiiiiq0")],
 25: [(25, "00qqiIi000qqq00")],
 26: [(29, "0Iiq0")],
 27: [(29, "0Iiq0")],
 28: [(30, "0q0")],
}
ARM = {  # raised fist, white sleeve, teal cuff
 17: [(12, "000")],
 18: [(11, "0STT0")],
 19: [(10, "0STTTS0")],
 20: [(10, "0STTTS0")],
 21: [(10, "0sSSSs0")],
 22: [(11, "0iIIi0")],
 23: [(11, "0WWWW0")],
 24: [(12, "0WWWWW00")],
 25: [(13, "0WWWWWWW00")],
 26: [(15, "00WWWWWWW0")],
 27: [(17, "00WWWWWW0")],
}
BODY = {
 25: [(22, "0WWWW"), (39, "W0")],
 26: [(23, "0WWWW0WWWmWWWWWWW0")],
 27: [(22, "0WWWWWW0WWmWWWWWWWW0")],
 28: [(22, "0WWWWWWW0mWWWWWWWWWW0")],
 29: [(21, "0WWWWWWWWmiWWWWWWWWWWW0")],
 30: [(21, "0WWWWWWWmWiWWWWWWWWWWWW0000")],
 31: [(21, "0WWWWWWmWWiWWWWWWWWWWWWWWWIi0")],
 32: [(21, "0WWWWWmWWWiWWWWWWWWWwwwwwwIq0")],
 33: [(21, "0WWWWmWWWWiWWWWWWWWw00000000")],
 34: [(21, "0WWWmWWWWWiWWWWWWWWw0")],
 35: [(20, "0MMmmWWWWWWiWWWWWWWWw0")],
 36: [(19, "0MMMMm0WWWWWiWWWWWWWw0")],
 37: [(19, "0MgMMm0WWWWWiWWWWWWWw0")],
 38: [(19, "0MMMMm0WWWWWiWWWWWWww0")],
 39: [(19, "0mmmmm0wWWWWiWWWWWwww0")],
 40: [(20, "00000.0wwwwwwwwwwwww0")],
}


def base():
    """Red's legs and throwing hand, repainted (pose skeleton)."""
    r = T('POKEMONTRAINER_Red')
    keep = rect(r, 0, 40, 63, 63) | rect(r, 41, 28, 56, 38)
    a = np.zeros_like(r)
    a[keep] = r[keep]
    a = remap(a, {'#182850': '#1e1e2a', '#306888': '#2e3042', '#5088b0': '#44485e', '#78b8d8': '#5e6680'}, rect(a, 0, 40, 63, 63))
    a = remap(a, {'#c04040': '#1e8a84', '#f86058': '#4cc4b4', '#d0d0d8': '#c8c8d4', '#785850': '#3a3040'}, rect(a, 0, 54, 63, 63))
    a = remap(a, {'#182850': '#7c7c94', '#306888': '#a8a8bc', '#5088b0': '#e6e6ee', '#78b8d8': '#ffffff'}, rect(a, 41, 28, 56, 38))
    return a


def build():
    from shade import rim
    a = base()
    rows = [['.'] * 64 for _ in range(64)]
    for table in (ARM, BODY, SCARF, S):
        for y, spans in table.items():
            for x, s_ in spans:
                for i, ch in enumerate(s_):
                    if ch != '.' and 0 <= x + i < 64:
                        rows[y][x + i] = ch
    rows = rim([''.join(r) for r in rows], [['h', 'H', 'J', 'K'], ['v', 'w', 'W', 'X'], ['q', 'i', 'I', 'I'], ['m', 'm', 'M', 'M']],
               keep=('g', 'e'), keep_interior=('i',))
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch != '.':
                a[y, x, :3] = hx(LEG[ch]); a[y, x, 3] = 255
    return a
