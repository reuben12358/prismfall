"""KESTREL v3 - drawn by hand on Lance's lunge (pose skeleton only).
Design: black + crimson; oversized black greatcoat (sleeves past the hands,
flipped-up collar, tail split like a raptor's); long lock over one eye."""
LEG = {
    '0': '#16141c', '1': '#1d1b25', '2': '#2f2d3b', '3': '#484660', '4': '#6a688c',
    'r': '#5c1c28', 'R': '#922f3c', 'Q': '#cc5660',
    'h': '#1b1a28', 'H': '#2f2d44', 'J': '#4a4866', 'K': '#7a78a0',
    's': '#a86c52', 'S': '#dda080', 'T': '#f6cfaa',
    'e': '#f4f2f6', 'i': '#7a7ab4',
    'p': '#22202a', 'P': '#363444', 'b': '#2a2228', 'B': '#4c4048', 'g': '#c8c8d8',
}
# rows: y -> list of (x, pixels).  '.' inside a span = leave transparent.
S = {
 2: [(30, "0")],
 3: [(29, "0K0"), (37, "00")],
 4: [(28, "0JKJ0"), (35, "00HJ0")],
 5: [(26, "00HJKJH00HJJH0"), (42, "0")],
 6: [(25, "0HHJJKJJHHJJHH0"), (41, "0J0")],
 7: [(24, "0HHJJJKJJHHHHHHH0JH0")],
 8: [(23, "0hHHJJJJJHHHHHHHHHHH0")],
 9: [(22, "0hHHHHJJHHHHHHhhhHHHH0")],
 10: [(21, "0hhHHHHHHHHHHHHhhhhhHH0")],
 11: [(21, "0hhhhHHHHhhHHHHHhhhhhh0")],
 12: [(21, "00hhhhhhhhhHHHhhhhhhh0")],
 13: [(22, "0hSTThhSSSHHhhhhhs0")],
 14: [(20, "0.0sTTTTTSSHHhhhss0")],
 15: [(19, "0R0shTTTTShHHhhs0R0")],
 16: [(19, "0RR0Se0TTs0eHhhss0R30")],
 17: [(19, "0RR0STsTTTsTHSSss0R30")],
 18: [(19, "0RR0STTTTSSSSsSS0R330")],
 19: [(20, "0RR0sTTsSSSSsS0R330")],
 20: [(20, "0rR00ssRsSs0SS0R30")],
 21: [(21, "0rR300sss0sS0RR30")],
 22: [(21, "03r33300000RRRr3320")],
}
# arm rows overlay the left side of rows 14-23
ARM = {
 14: [(3, "00"), (11, "000")],
 15: [(2, "0TS0000"), (10, "02220000"), (18, "000")],
 16: [(2, "0TTTTTSs0"), (10, "0233322222100")],
 17: [(3, "00STTSs0"), (10, "0333332222211")],
 18: [(5, "0STSs0"), (10, "0234433322221")],
 19: [(5, "0sSss0"), (10, "02333333322221")],
 20: [(6, "0ss0"), (10, "0222222222222")],
 21: [(7, "00"), (10, "001111111111")],
 22: [(11, "0000000000")],
}
# torso, right arm, coat tail, front flap, legs
BODY = {
 23: [(22, "03r333000RRRRr3332220000000000"), (52, "000")],
 24: [(21, "033r3330RRQQRr33332222222222222220")],
 25: [(21, "0333r330RQQRRr3333332222222222222220")],
 26: [(20, "03333r330RQRRr33333333222222221122220")],
 27: [(20, "033333r30RRRRr3332222000333222222112210")],
 28: [(20, "0333333r0RRRRr3322203330332222222221110")],
 29: [(19, "0r333333r0RRRr33222033330032222222222211110")],
 30: [(19, "0rr33333r0RRRr33222032220S0222222222222111110")],
 31: [(19, "0rrr3333r0RRRr332220022200S022222222222221111110")],
 32: [(18, "0Rrr3333r0RRRr3322220000022222222222222111110")],
 33: [(18, "0RRr33333r0RRr332222222222222222222222221110")],
 34: [(18, "0RRRr3333r0gg0332222222222222222222222221110")],
 35: [(18, "0QRRr3333r0000332222222222222222222111111110")],
 36: [(18, "0QRRRr333r0pP0322222222222222111111111000"), (60, "00")],
 37: [(18, "0QRRRr333r0ppPP02222222222222111111110"), (58, "0010")],
 38: [(18, "0QRRRRr33r0pPPPP02222222222111111111100"), (57, "01110")],
 39: [(19, "0QRRRr33r0pPPPPP02222222211111111111100111110")],
 40: [(19, "0QRRRr33r0pPPPPPP0222222111111111111111111110")],
 41: [(20, "0QRRr33r0ppPPPPP0222221111111110001111111110")],
 42: [(20, "0QRRr33r0pppPPPP022221111111110..0011111110")],
 43: [(21, "0QRr33r0pppPPPP0222111111110......0111110")],
 44: [(21, "0QRr33r0ppppPPP02211111110.........01110")],
 45: [(22, "0Qr33r0ppppPPP0p0111110............010")],
 46: [(22, "0Rr3r0pppppPP0..0ppPP0..............0")],
 47: [(23, "0rr0.0ppppPP0...0ppPP0")],
 48: [(24, "00..0pppPPP0....0pppPP0")],
 49: [(28, "0ppPPP0.....0pppP0")],
 50: [(27, "0ppPP0......0pppP0")],
 51: [(26, "0bBBB0.......0bbBB0")],
 52: [(25, "0bbBBB0.......0bbBB0")],
 53: [(24, "0bgbBB0........0bgbB0")],
 54: [(24, "0bbbBB0........0bbBB0")],
 55: [(23, "0bbbBB0..........0bbB0")],
 56: [(23, "0bbbBB0..........0bbBB0")],
 57: [(22, "0bbbbB0...........0bbBB0")],
 58: [(21, "0bbbbbB0...........0bbbB0")],
 59: [(19, "00bbbbbB0............0bbbbB0")],
 60: [(18, "0bbbbbbb0.............00000000")],
 61: [(18, "000000000")],
}


def grid():
    rows = [['.'] * 64 for _ in range(64)]
    for table in (ARM, BODY, S):
        for y, spans in table.items():
            if not isinstance(y, int):
                continue
            for x, s in spans:
                for i, ch in enumerate(s):
                    if ch != '.' and 0 <= x + i < 64:
                        rows[y][x + i] = ch
    return [''.join(r) for r in rows]


TAIL_NOTCHES = [(63, 37), (62, 37), (61, 37), (60, 37), (62, 38), (63, 38), (59, 41), (58, 41), (57, 41), (56, 41), (58, 42), (57, 42),
                (59, 42), (60, 42), (61, 42), (60, 43), (61, 43), (62, 43)]


def final():
    from shade import rim, notch
    g = grid()
    g = notch(g, TAIL_NOTCHES)
    g = rim(g, [['1', '2', '3', '4'], ['h', 'H', 'J', 'K'], ['p', 'p', 'P', 'P'], ['b', 'b', 'B', 'B']])
    g = [list(r) for r in g]
    def put(pts, ch, only=None):
        for x, y in pts:
            if only is None or g[y][x] in only:
                g[y][x] = ch
    # coat folds: a lit ridge and a dark crease down the back panel, one on the front flap
    put([(42, 26), (42, 27), (43, 28), (43, 29), (44, 30), (44, 31), (45, 32)], '3', only='12')
    put([(38, 30), (38, 31), (39, 32), (39, 33), (39, 34), (40, 35), (40, 36)], '1', only='23')
    put([(48, 29), (49, 30), (50, 31), (51, 32), (52, 33), (53, 34)], '3', only='12')
    put([(46, 36), (47, 37), (48, 38), (49, 39)], '1', only='23')
    # crimson feather pin on the near lapel
    put([(28, 24), (28, 25), (27, 26)], 'Q'); put([(29, 25), (28, 26)], 'R'); put([(27, 27)], '0')
    # hair shine streak
    put([(27, 7), (28, 7), (29, 6), (30, 6), (33, 7), (34, 7), (35, 6)], 'K', only='HJ')
    return [''.join(r) for r in g]


def build():
    import numpy as np
    from fs import hx
    a = np.zeros((64, 64, 4), np.uint8)
    for y, r in enumerate(final()):
        for x, ch in enumerate(r):
            if ch != '.':
                a[y, x, :3] = hx(LEG[ch]); a[y, x, 3] = 255
    return a
