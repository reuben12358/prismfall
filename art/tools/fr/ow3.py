"""v3 overworlds: stock charset walking bodies as skeleton, hand-drawn heads
per direction, outfit repainted to the design."""
import numpy as np
from fs import C, hx, remap, rect
FW, FH = 16, 24


def stamp(a, x0, y0, lines, leg):
    for j, line in enumerate(lines):
        for i, ch in enumerate(line):
            if ch == '.':
                continue
            X, Y = x0 + i, y0 + j
            if 0 <= X < a.shape[1] and 0 <= Y < a.shape[0]:
                if ch == '_':
                    a[Y, X] = 0
                else:
                    a[Y, X, :3] = hx(leg[ch]); a[Y, X, 3] = 255


def mirror(lines):
    return [l[::-1] for l in lines]


def assemble(base, heads, leg, clear_rows=16, head_y=0, bob=(0, 1, 0, 1)):
    """heads: {'down','left','up'} -> lines; right = mirror(left)."""
    a = base.copy()
    for d, key in enumerate(('down', 'left', 'right', 'up')):
        lines = heads[key] if key != 'right' else mirror(heads['left'])
        for f in range(4):
            x0, y0 = f * FW, d * FH
            a[y0:y0 + clear_rows + bob[f], x0:x0 + FW] = 0
            stamp(a, x0, y0 + head_y + bob[f], lines, leg)
    return a


JLEG = {'0': '#24180f', 'a': '#5e2412', 'A': '#8e3c1e', 'B': '#c05e2e', 'C': '#e8864a',
        'k': '#a06a18', 'K': '#e2a93a', 'L': '#f8d67c', 'u': '#fff6dc',
        's': '#c47a5a', 'T': '#fcd8b6', 'f': '#c8664a', 'r': '#c8343c', 'i': '#2c5a24'}
J_HEADS = {
    'down': [
        "....00.000.0LK0.",
        "..00BB0BBB00KLK0",
        ".0BBBBBBBBBBBkk0",
        "0BBLLLLLLLLLLBB0",
        "0BKuKKKuKKKuKKB0",
        "0BkkkkkkkkkkkkB0",
        "0BCBBABBBBABBBA0",
        "0BB0B0BBB0B0BAB0",
        "0BA0TTTTTTTT0AB0",
        "0BA0T0TTTT0T0AB0",
        "0BA0TiTTTTiT0AB0",
        "0BBATfTTTTfTAAB0",
        ".0BAsTTrrTTsAB0.",
        ".0BA0ssssss0AB0.",
        "..00A000000A00..",
        "....00....00....",
    ],
    'left': [
        ".....00.000.....",
        "...00BB0BBB00...",
        "..0BBBBBBBBBB0..",
        ".0LLLLLLLLLBBB0.",
        ".0KuKKKuKKkBBB0K",
        ".0kkkkkkkkkBBBkL",
        "0BCB0BBBBABBBB0K",
        "0B0TT0BBBBBABBB0",
        "0TTTTT0BBBBBBAB0",
        "0Ti0TTT0BBBBBAB0",
        ".0TTfTTT0ABBBAB0",
        ".0TTTTT0ABBBBAB0",
        "..0rsTT0AABBBA0.",
        "...0ss0.0AABA0..",
        "....00...0AA0...",
        "..........00....",
    ],
    'up': [
        "....00.000.00...",
        "..00BB0BBB0BB0..",
        ".0BBBBBBBBBBBB0.",
        "0BBLLLLLLLLLLBB0",
        "0BKKuKKKuKKKKKB0",
        "0BkkkkkkkkkkkkB0",
        "0BBBBBBkkBBBBBB0",
        "0BCBBBkLLkBBBBA0",
        "0BBABBBkkBBBABB0",
        "0BABBBBBBBBBBAB0",
        "0BBABBBBBBBBABB0",
        ".0BBAABBBBAABB0.",
        ".0BAABBBBBBAAB0.",
        "..0BBAAAAAABB0..",
        "...0000000000...",
        "................",
    ],
}


def juno_ow():
    b = C('trainer_POKEMONTRAINER_May')
    body = np.zeros(b.shape[:2], bool)
    for d in range(4):
        body[d * FH + 16: d * FH + 24, :] = True
    feet = np.zeros(b.shape[:2], bool)
    for d in range(4):
        feet[d * FH + 21: d * FH + 24, :] = True
    b = remap(b, {'#904028': '#5a3a22', '#501000': '#3a281c'}, feet)
    b = remap(b, {'#e07050': '#5a7a40', '#904028': '#3e5a2c', '#501000': '#2c3a1c', '#484858': '#4a6a32',
                  '#ffffff': '#e8cc96', '#c0c8d8': '#c9a46a', '#383818': '#5e2412', '#787040': '#8e3c1e', '#c8b068': '#c05e2e',
                  '#889090': '#f2ead2'}, body)
    return assemble(b, J_HEADS, JLEG)


KLEG = {'0': '#16141c', 'h': '#1b1a28', 'H': '#2f2d44', 'J': '#4a4866', 'K': '#7a78a0',
        'T': '#f6cfaa', 's': '#c88a68', 'R': '#922f3c', 'r': '#5c1c28', '1': '#1d1b25', '2': '#2f2d3b', '3': '#484660'}
K_HEADS = {
    'down': [
        "................",
        "......0...0.....",
        "...0.0J0.0J0.0..",
        "..0H0HJH0HJH0H0.",
        "..0HJHHJHHJHHJ0.",
        ".0HHJJHHHHHHHHH0",
        ".0HHHHHHHHHHHHH0",
        "0hHHHHhHHHhHHHh0",
        "0hhhHhhhhhhhhhh0",
        "0Rh0TTTTTThhhh0R",
        "0RR0TTTTTThhTT0R",
        "0RR0T0TTTThh0TRR",
        "0RR0TTTTTTTTTRR0",
        ".0RR0sTTTTTs0RR0",
        ".03RR000000RR30.",
        "..033RRRRRR330..",
    ],
    'left': [
        "................",
        "........0..0....",
        ".....00J00J0.0..",
        "....0HJJHJJH0J0.",
        "...0HJJHHHHHHHH0",
        "..0HJHHHHHHHHHHH",
        ".0hHHHHHHHHHHHH0",
        "0hhhhHHhHHHHHHh0",
        "0hTThhhhhHHHHh0.",
        ".0TTThTThhHHh0R0",
        ".0T0TTThhHHh0RR0",
        "0TTTTTTThhh0RRR0",
        ".0sTTTTT0h0RRR0.",
        "..0sTTT0RRRRR30.",
        "...000RRRR3330..",
        "....03333333300.",
    ],
    'up': [
        "................",
        "......0...0.....",
        "...0.0J0.0J0.0..",
        "..0H0HJH0HJH0H0.",
        "..0HJHHJHHJHHJ0.",
        ".0HHJJHHHHHHHHH0",
        ".0HHHHHHHHHHHHH0",
        "0hHHHHHHHHHHHHh0",
        "0hHHHHhHHhHHHHh0",
        "0hhHhhhhhhhhHhh0",
        "0Rhhhhhhhhhhhh0R",
        "0RR0hhhhhhhh0RR0",
        "0RRR00hhhh00RRR0",
        ".0RRRR0000RRRR0.",
        ".03RRRRRRRRRR30.",
        "..033333333330..",
    ],
}


def kestrel_ow():
    b = C('trainer_ELITEFOUR_Lance')
    body = np.zeros(b.shape[:2], bool)
    for d in range(4):
        body[d * FH + 16: d * FH + 24, :] = True
    b = remap(b, {'#8c8c94': '#2f2d3b', '#4a4a5a': '#1d1b25', '#e66b4a': '#922f3c', '#943a29': '#5c1c28',
                  '#521000': '#16141c', '#7b4242': '#a86c52'}, body)
    return assemble(b, K_HEADS, KLEG)
