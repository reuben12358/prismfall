"""JUNO v3 - drawn by hand on May's stance (pose skeleton only).
Design: leaf green + marigold; huge frizzy auburn hair-cloud bursting out of
a marigold kerchief (bunny-ear knot); green dungarees with a patched knee,
rolled cream shirt, oversized gardening gloves, satchel spilling seed packets."""
LEG = {
    '0': '#24180f',
    'a': '#5e2412', 'A': '#8e3c1e', 'B': '#bd5a2c', 'C': '#e8864a',
    'k': '#a06a18', 'K': '#e2a93a', 'L': '#f8d67c', 'u': '#fff6dc',
    's': '#c47a5a', 'S': '#eeb08c', 'T': '#fcd8b6', 'f': '#c8664a',
    'e': '#ffffff', 'i': '#3f8a34', 'I': '#22481c', 'r': '#c8343c', 'R': '#f0705e',
    'w': '#cfc3a2', 'W': '#f6f0de',
    'g': '#2c4620', 'G': '#4a6a32', 'H': '#6c8c4a', 'J': '#90b268', 'y': '#f0c040',
    'q': '#b07a44', 'n': '#8a6a44', 'N': '#c9a46a', 'O': '#e8cc96',
    'm': '#5e3a20', 'M': '#94603a', 'x': '#e84a5a', 'z': '#5a98e0',
    'o': '#3a281c', 'Q': '#6e4c34', 'v': '#ece4d2',
}
# hair cloud: hand-placed lobes (cx, cy, r) - frizz comes from the bumps
LOBES = [(31, 11, 10.5), (22, 14, 6.5), (20, 20, 5), (23, 25, 3.6), (41, 14, 6.5), (43, 20, 5), (40, 25, 3.6),
         (25, 5, 4.2), (32, 3.6, 4.2), (38, 5.4, 4.2), (18, 16, 3.6), (45, 16, 3.4)]
import math as _m
# frizz: small bumps around the main mass (top and sides), irregular radii
for _k, _ang in enumerate(range(150, 400, 19)):
    _r = 2.6 + (0.9 if _k % 3 == 0 else 0.0) - (0.5 if _k % 4 == 1 else 0.0)
    _cx = 31 + 12.0 * _m.cos(_m.radians(_ang)); _cy = 13 - 11.5 * _m.sin(_m.radians(_ang)) * -1
    LOBES.append((_cx, 13 + 11.5 * _m.sin(_m.radians(_ang)), _r))
# curl marks: (x, y, char) - light curls on the lit side, dark creases between clumps
CURLS = [(19, 6, 'a'), (20, 7, 'a'), (17, 11, 'a'), (18, 12, 'a'), (16, 17, 'a'), (17, 18, 'a'), (18, 22, 'a'), (19, 23, 'a'),
         (44, 7, 'a'), (45, 8, 'a'), (46, 12, 'a'), (46, 13, 'a'), (45, 18, 'a'), (46, 19, 'a'), (43, 22, 'a'), (44, 23, 'a'),
         (16, 9, 'C'), (17, 9, 'C'), (15, 14, 'C'), (16, 15, 'C'), (15, 20, 'C'), (18, 25, 'C'), (22, 3, 'C'), (23, 3, 'C'), (30, 2, 'C'),
(20, 12, 'C'), (21, 11, 'C'), (19, 17, 'C'), (18, 18, 'C'), (24, 9, 'C'), (25, 8, 'C'), (35, 8, 'C'), (36, 8, 'C'),
         (22, 15, 'A'), (21, 19, 'A'), (20, 22, 'A'), (42, 12, 'A'), (43, 17, 'A'), (41, 21, 'A'), (44, 22, 'A'), (40, 9, 'A'),
         (23, 21, 'C'), (17, 14, 'C'), (39, 15, 'B'), (21, 24, 'A'), (42, 25, 'A')]
CLOUD_X, CLOUD_Y = 14, 1
CLOUD = [
    "..........###..####..###...........",
    "........######.#####.######........",
    "......#########################....",
    "....###########################....",
    "...#############################...",
    "..###############################..",
    "..###############################..",
    ".#################################.",
    "##################################.",
    "##################################.",
    ".##################################",
    ".#################################.",
    "##################################.",
    "###################################",
    "###################################",
    ".#################################.",
    "##################################.",
    "##################################.",
    ".#################################.",
    "..################################.",
    "..################################.",
    ".################################..",
    "..##########............########...",
    "..#########..............######....",
    "...#######...............#####.....",
    "....#####.................###......",
    ".....###...........................",
]
KERCHIEF = [  # (x, y, row)
    (23, 4, "0LLLLLLLLLLLLLLL0"),
    (21, 5, "0kKKuKKKuKKKuKKKuKk0"),
    (20, 6, "0kkkkkkkkkkkkkkkkkkkk0"),
]
KNOT = (40, 0, ["...00..00.", "..0LK00LK0", ".0KLKkKLk0", "0kKKkKKk0.", "0kkKK0k0..", ".0kk0.0...", "..00......"])
FACE = (25, 12, [
    "0BB0B0BBB0B0B0",
    "0STT0TTTT0TTS0",
    "0STTTTTTTTTTS0",
    "0S000TTTT000S0",
    "0S0ie0TT0ie0S0",
    "0SSIi0TT0IiTS0",
    "0sSTfTTTTfTSs0",
    ".0sSTTrRrTSs0.",
    ".0ssSTTrTTs0..",
    "..00ssSSSs0...",
    "....0000......",
])
S = {}
BODY = {
 # torso: cream shirt, dungaree bib + straps; ball arm reaches left
 25: [(25, "0000"), (37, "0000")],
 26: [(9, "000"), (22, "00wWWW0GG0sss0GG0WWw00")],
 27: [(8, "0RRR0"), (21, "0wWWWW0GG0TT0GGG0WWWWw0")],
 28: [(7, "0RReRR0"), (20, "0wWWWWW0GGGGGGGGG0WWWWWw0")],
 29: [(7, "0eeeee0nN0"), (19, "0WWWww0GHHHHyHHHHG0wWWWWw0")],
 30: [(7, "00000NNNNO0"), (18, "0SSTww00GHHHHHHHHHG0wwWWWWw0")],
 31: [(7, "0eWWe0nNNOO0"), (17, "0SSTT0.0GHHJHHHHHHHG00wwWWw0")],
 32: [(8, "0eee0nNNNO0"), (16, "0sSSS0..0GHHHHHHHHHHG0.0wWWw0")],
 33: [(9, "000.0nNNO0SSTTTS0...0GGHHHHHHHHHGG0.0SSTS0")],
 34: [(13, "0nN00ssSSS0....0GGGGGGGGGGGGGG0.0xySTS0")],
 35: [(14, "00..0000.....0GHHHHHHHHHHHHG0MMxyzSs0")],
 36: [(27, "0GHHJHHHHHHHHHHG0mMMMMnNNO0")],
 37: [(27, "0GHHHHHHHHHHHHHHG0mMyMnNNNO0")],
 38: [(27, "0GHHHHHHH0GHHHHHG0mmMMnNNO0")],
 39: [(27, "0GGHHHHH00GHHHHHG0mmmmm000")],
 40: [(27, "0GGHHHHH0.0GHHHHHG000000")],
 41: [(28, "0GHHHHH0..0GHHHHG0")],
 42: [(28, "0GHHHHH0..0GHHHHG0"), (52, "0z0")],
 43: [(28, "0GHHHHG0...0GHHHG0"), (51, "0zuz0")],
 44: [(28, "0qqqHHG0...0GHHHG0"), (52, "0z0")],
 45: [(28, "0qNqHHG0...0GHHHG0")],
 46: [(28, "0qqqHHG0...0GHHHG0")],
 47: [(28, "0GHHHHG0...0GHHHG0")],
 48: [(28, "0GHHHHG0...0GHHHG0")],
 49: [(28, "0GHHHG0.....0GHHG0")],
 50: [(27, "0JJJJJJ0....0JJJJJ0")],
 51: [(27, "0GGGGGG0....0GGGGG0")],
 52: [(28, "0vvvv0......0vvvv0")],
 53: [(28, "0SSS0.......0SSS0")],
 54: [(28, "0sSS0.......0sSS0")],
 55: [(27, "0ooQQ0......0ooQQ0")],
 56: [(27, "0ooQQ0......0ooQQ0")],
 57: [(26, "0oooQQ0......0ooQQ0")],
 58: [(25, "0ooooQQ0......0oooQQ0")],
 59: [(24, "0ooooooQ0......0oooooQ0")],
 60: [(24, "0QQQQQQQ0......0QQQQQQQ0")],
 61: [(24, "000000000......000000000")],
}


def grid():
    import math
    rows = [['.'] * 64 for _ in range(64)]
    cloud = [[False] * 64 for _ in range(64)]
    for j, line in enumerate(CLOUD):
        for i, ch in enumerate(line):
            if ch == '#':
                cloud[CLOUD_Y + j][CLOUD_X + i] = True
    for y in range(64):
        for x in range(64):
            if cloud[y][x]:
                edge = any(not (0 <= x + dx < 64 and 0 <= y + dy < 64) or not cloud[y + dy][x + dx] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                t = (x - 31) * 0.55 + (y - 12) * 0.85
                rows[y][x] = '0' if edge else ('B' if t < -5 else 'A' if t < 7 else 'a')
    # cloud must sit in front of the shoulders but behind the face: body is drawn after, so clear the body area

    def stamp(x0, y0, lines):
        for j, line in enumerate(lines):
            for i, ch in enumerate(line):
                if ch != '.' and 0 <= x0 + i < 64 and 0 <= y0 + j < 64:
                    rows[y0 + j][x0 + i] = ch
    for x, y, line in KERCHIEF:
        stamp(x, y, [line])
    stamp(*KNOT)
    for x, y, ch in CURLS:
        if rows[y][x] == 'B':
            rows[y][x] = ch
    stamp(*FACE)
    for table in (BODY,):
        for y, spans in table.items():
            for x, s in spans:
                for i, ch in enumerate(s):
                    if ch != '.' and 0 <= x + i < 64:
                        rows[y][x + i] = ch
    return [''.join(r) for r in rows]


def final():
    from shade import rim
    g = grid()
    g = rim(g, [['a', 'A', 'B', 'C'], ['g', 'G', 'H', 'J'], ['w', 'w', 'W', 'W'], ['n', 'N', 'O', 'O'], ['o', 'o', 'Q', 'Q'], ['m', 'm', 'M', 'M']],
            keep=('u', 'y', 'q', 'x', 'z'), keep_interior=('a', 'B', 'C'))
    return g


def build():
    import numpy as np
    from fs import hx
    a = np.zeros((64, 64, 4), np.uint8)
    for y, r in enumerate(final()):
        for x, ch in enumerate(r):
            if ch != '.':
                a[y, x, :3] = hx(LEG[ch]); a[y, x, 3] = 255
    return a
