"""Gym 1, the Loomhouse (GYM_PUZZLES 'Gym 1'): layouts, engine-level models and the runtime room registry.
The map generator (gen_gym1.py) draws these same grids, so the proof and the map cannot drift apart.
Glyphs: # void / wall mass   W wall face   . floor   v loom bed (drop)   S stair cell (floor)   o loom (solid)."""
from .core import Model, Device, grid_cells, around

V_A, V_B, V_C, V_FOYER, V_BRIDGE = 305, 306, 307, 308, 309
S_ALPHA, S_BRASS, S_GAMMA, S_KNOT = 305, 306, 307, 308

# ------------------------------------------------------------------------------------------------ 130 Foyer
FOYER = ["####################",
         "####################",
         "##WWW##WWW##WSW#####",
         "##WWW##WWW##WSW#####",
         "##...##...##...#####",
         "##...##...##...#####",
         "#vvvvvvvvvvvvvvvv###",
         "#vvvvvvvvvvvvvvvv###",
         "#................###",
         "#................###",
         "#................###",
         "#................###",
         "#................###",
         "#................###",
         "########.###########",
         "####################"]
FOYER_PLANKS = {0: 3, 1: 8, 2: 13}          # V308 -> plank column (rows 6-7)
FOYER_AT = dict(heddle=(3, 10), exit=(8, 14), stair=(13, 2), pim=(9, 12), guide=(11, 10), tamsin=(8, 9), loom=(14, 11),
                item=(2, 4), card_b=(9, 4), card_s=(5, 12), portrait=(8, 3), start=(8, 13))


def foyer_model():
    cells, _ = grid_cells(130, FOYER, '#W')
    solid = {FOYER_AT[k] for k in ('heddle', 'pim', 'guide', 'loom', 'item', 'card_b', 'card_s')} | {(14, 10), (15, 10), (15, 11)}
    cells -= {(130, x, y) for x, y in solid}

    def passable(c, v):
        _, x, y = c
        if FOYER[y][x] == 'v': return FOYER_PLANKS[v[0]] == x
        return True
    hx, hy = FOYER_AT['heddle']
    dev = [Device('Training heddle', [c for c in around(130, hx, hy) if c in cells], lambda v, c: (((v[0] + 1) % 3,), c))]
    return Model('g1_foyer (130)', cells, passable, (130,) + FOYER_AT['start'], (0,), dev, [(130,) + FOYER_AT['stair']],
                 resets=around(130, *FOYER_AT['pim']))


# ------------------------------------------------------------------------------------------------ 131 Weaving Hall
def _hall():
    W = 25
    full, gap = '#' + '.' * 23 + '#', '#' + 'v' * 23 + '#'
    seg = '#....oooooo...oooooo....#'
    wall = '#' + 'W' * 11 + 'S' + 'W' * 11 + '#'
    return (['#' * W, wall, wall, full, full] + [gap] * 4 + [seg, seg] + [gap] * 3 + [seg, seg] + [gap] * 4 +
            [full, full, '#' * 12 + '.' + '#' * 12, '#' * W])


HALL = _hall()
HALL_COLS = (3, 12, 21)
HALL_GAPS = {'A': (range(5, 9), V_A, (3, 12, 21)), 'B': (range(11, 14), V_B, (None, 12, 21)), 'C': (range(16, 20), V_C, (3, 12, 21))}
HALL_HEDDLES = {'Red': ((1, 21), (V_A, V_B), 'A and B'), 'Gold': ((9, 21), (V_B, V_C), 'B and C'), 'Green': ((23, 21), (V_C, V_A), 'C and A')}
HALL_AT = dict(stair=(12, 1), entrance=(12, 22), start=(12, 21), pim=(15, 21), bram=(2, 3), orla=(22, 9), nell=(11, 15),
               sign=(2, 10), juno=(10, 21), net=(17, 21))


def hall_model():
    cells, _ = grid_cells(131, HALL, '#Wo')
    solid = {HALL_AT[k] for k in ('pim', 'bram', 'orla', 'nell', 'sign', 'juno', 'net')} | {h[0] for h in HALL_HEDDLES.values()}
    cells -= {(131, x, y) for x, y in solid}
    idx = {V_A: 0, V_B: 1, V_C: 2}

    def passable(c, v):
        _, x, y = c
        if HALL[y][x] != 'v': return True
        for rows, var, cols in HALL_GAPS.values():
            if y in rows: return cols[v[idx[var]]] == x
        return False

    def pull(a, b):
        def act(v, c):
            v = list(v); v[idx[a]] = (v[idx[a]] + 1) % 3; v[idx[b]] = (v[idx[b]] + 1) % 3
            return tuple(v), c
        return act
    dev = [Device('%s heddle' % n, [c for c in around(131, *pos) if c in cells], pull(*vs), n) for n, (pos, vs, _) in HALL_HEDDLES.items()]
    return Model('g1_hall (131)', cells, passable, (131,) + HALL_AT['start'], (0, 0, 0), dev, [(131,) + HALL_AT['stair']],
                 resets=around(131, *HALL_AT['pim']))


# ------------------------------------------------------------------------------------------------ 132 Canopy Lofts
DECKS = {1: (1, 21), 2: (11, 19), 3: (3, 11), 4: (18, 13), 5: (11, 5), 6: (19, 2)}      # top-left of each 4x3 deck (P6: 4x4)
CENTRE = {1: (2, 22), 2: (12, 20), 3: (4, 12), 4: (19, 14), 5: (12, 6), 6: (20, 3)}
SPOOLS = {'s1': ((4, 22), 'alpha', 3, 2), 's2': ((14, 20), 'gamma', 5, 4), 's3': ((6, 12), 'brass', 4, 1),
          's4': ((21, 14), 'brass', 2, 3), 's5': ((14, 6), 'gamma', 3, 2)}                 # pos, cord, ON -> deck, OFF -> deck
CORDS = {'alpha': (1, 21), 'gamma': (18, 13), 'brass': (3, 11)}
LADDERS = {2: (11, 21), 3: (3, 13), 4: (18, 15), 5: (11, 7)}
BRIDGE = {1: [(x, 5) for x in range(15, 19)], 2: [(20, y) for y in range(6, 13)]}
LOFT_AT = dict(arrive=(2, 22), down=(2, 24), door=(12, 4), warp=(22, 2), mossy=(1, 23), hollis=(13, 21), ash=(20, 15), item=(11, 5))


def _lofts():
    W, H = 25, 26
    g = [['#'] * W for _ in range(H)]
    for p, (x0, y0) in DECKS.items():
        for y in range(y0, y0 + (4 if p == 6 else 3)):
            for x in range(x0, x0 + 4): g[y][x] = '.'
    for cells in BRIDGE.values():
        for x, y in cells: g[y][x] = 'v'
    g[LOFT_AT['down'][1]][LOFT_AT['down'][0]] = 'S'
    g[LOFT_AT['door'][1]][LOFT_AT['door'][0]] = 'S'
    return [''.join(r) for r in g]


LOFTS = _lofts()


def lofts_model():
    cells, _ = grid_cells(132, LOFTS, '#')
    solid = {s[0] for s in SPOOLS.values()} | set(CORDS.values()) | set(LADDERS.values()) | {LOFT_AT[k] for k in ('mossy', 'hollis', 'ash', 'item')}
    cells -= {(132, x, y) for x, y in solid}
    cells -= {(132,) + LOFT_AT['down'], (132,) + LOFT_AT['door']}      # exits to other rooms: not part of this proof
    ci = {'alpha': 0, 'brass': 1, 'gamma': 2}

    def passable(c, v):
        _, x, y = c
        if LOFTS[y][x] == 'v': return v[3] in BRIDGE and (x, y) in BRIDGE[v[3]]
        return True

    def cord(name):
        def act(v, c):
            v = list(v); v[ci[name]] ^= 1
            if name == 'brass': v[3] = (v[3] + 1) % 3
            return tuple(v), c
        return act

    def spool(name):
        _, cd, on, off = SPOOLS[name]
        return lambda v, c: (v, (132,) + CENTRE[on if v[ci[cd]] else off])
    dev = [Device('Cord ' + n, [c for c in around(132, *p) if c in cells], cord(n), n + ' cord') for n, p in CORDS.items()]
    dev += [Device('Spool ' + n, [c for c in around(132, *s[0]) if c in cells], spool(n), n) for n, s in SPOOLS.items()]
    dev += [Device('Ladder P%d' % p, [c for c in around(132, *pos) if c in cells], lambda v, c: (v, (132,) + CENTRE[1]), 'ladder P%d' % p)
            for p, pos in LADDERS.items()]
    return Model('g1_lofts (132)', cells, passable, (132,) + LOFT_AT['arrive'], (0, 0, 0, 0), dev, [(132,) + LOFT_AT['warp']],
                 resets=around(132, *LOFT_AT['mossy']))


# ------------------------------------------------------------------------------------------------ 134 Granny's Knot
KNOT = ["####################",
        "####################",
        "###WWWWWWWWWWWWW####",
        "###WWWWWWWWWWWWW####",
        "###.............####",
        "###.............####",
        "###.............####",
        "###.............####",
        "###.............####",
        "###.............####",
        "###.............####",
        "###.............####",
        "#########.##########",
        "####################",
        "####################"]
KNOT_THREADS = [(7 + i, 6) for i in range(5)]
KNOT_TREADLES = [(7 + i, 9) for i in range(5)]
KNOT_FLIPS = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 1, 2)]
KNOT_TARGET = (1, 0, 1, 0, 1)
KNOT_AT = dict(sampler=(7, 3), chest=(5, 10), lever=(12, 10), exit=(9, 12), start=(9, 11))


def knot_model():
    cells, _ = grid_cells(134, KNOT, '#W')
    cells -= {(134, x, y) for x, y in KNOT_THREADS + KNOT_TREADLES + [KNOT_AT['chest'], KNOT_AT['lever']]}
    GOAL = (134, -1, -1)
    cells_all = cells | {GOAL}

    def passable(c, v): return c != GOAL or v == KNOT_TARGET     # the chest opens when the row reads up-down-up-down-up

    def press(i):
        def act(v, c):
            v = list(v)
            for t in KNOT_FLIPS[i]: v[t] ^= 1
            return tuple(v), c
        return act
    dev = [Device('Treadle %d' % (i + 1), [c for c in around(134, *p) if c in cells], press(i), 'P%d' % (i + 1)) for i, p in enumerate(KNOT_TREADLES)]
    cx, cy = KNOT_AT['chest']
    m = Model('g1_knot (134)', cells_all, passable, (134,) + KNOT_AT['start'], (0,) * 5, dev, [GOAL], resets=around(134, *KNOT_AT['lever']))
    m.links = {}
    # the chest: an abstract goal cell hung off the tile below the chest
    real_region = m.region

    def region(cell, v):
        r = set(real_region(cell, v))
        if v == KNOT_TARGET and any(c in r for c in around(134, cx, cy)): r.add(GOAL)
        return frozenset(r)
    m.region = region
    return m


def knot_unique():
    """Over Z2 the five treadles have full rank: exactly one subset gives the target."""
    sols = []
    for mask in range(32):
        v = [0] * 5
        for i in range(5):
            if mask >> i & 1:
                for t in KNOT_FLIPS[i]: v[t] ^= 1
        if tuple(v) == KNOT_TARGET: sols.append([i + 1 for i in range(5) if mask >> i & 1])
    return sols


CHECKS = [(foyer_model, dict(moves=2)),
          (hall_model, dict(moves=3)),
          (lofts_model, dict(moves=7, without={'the brass wire': ['Cord brass']})),
          (knot_model, dict(moves=3))]

# Runtime registry (emitted as Ruby by puzzles/__init__.py -> Plugins/Prismfall Maps/007_PuzzleRooms.rb)
ROOMS = {
    'g1_foyer': dict(name='Loomhouse Foyer', map=130, start=list(FOYER_AT['start']) + [8], reset=dict(vars={V_FOYER: 0}),
                     solved=dict(vars={V_FOYER: 2}),
                     hints=["See the silk running up from the heddle? Follow it with your eyes when you pull.",
                            "One pull moves the plank one balcony along. The stairs are behind the last balcony.",
                            "Pull the heddle twice. The plank ends up on the right, under the stairs. Walk it."]),
    'g1_hall': dict(name='Weaving Hall', map=131, start=list(HALL_AT['start']) + [8], reset=dict(vars={V_A: 0, V_B: 0, V_C: 0}),
                    solved=dict(vars={V_A: 2, V_B: 2, V_C: 2}),
                    hints=["Every heddle lifts two rows. Count lifts, not pulls.",
                           "Three heddles, three rows: what if each row got lifted the same number of times?",
                           "Pull Red, Gold and Green once each. Every row has been lifted twice, so all three planks sit on the "
                           "right. Climb the right-hand column."]),
    'g1_lofts': dict(name='Canopy Lofts', map=132, start=list(LOFT_AT['arrive']) + [8],
                     reset=dict(vars={V_BRIDGE: 0}, switches={S_ALPHA: False, S_BRASS: False, S_GAMMA: False}),
                     solved=dict(vars={V_BRIDGE: 1}, switches={S_ALPHA: True, S_BRASS: True, S_GAMMA: True}, at=[20, 4, 8]),
                     hints=["The pattern card lists three cords. Count the cords up here.",
                            "The brass one isn't Gran's. Pull it and watch the far side of the canopy.",
                            "Pull the alpha cord, ride the spool to the west deck, pull the brass wire (a bridge swings out up "
                            "north). Ride on east, pull gamma, ride the spool there, then the next, and walk the bridge."]),
    'g1_knot': dict(name="Granny's Knot", map=134, start=list(KNOT_AT['start']) + [8],
                    reset=dict(states={'T%d' % (i + 1): 0 for i in range(5)}),
                    hints=["The sampler on the wall is the row Gran never finished: up, down, up, down, up.",
                           "Every treadle lifts the first thread. An odd number of presses leaves it up.",
                           "Press the first, fourth and fifth treadles, once each, in any order."]),
}
