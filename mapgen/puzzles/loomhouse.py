"""The Loomhouse, Briarwick (Gym 2 since SPINE Revision 14: Tamsin, Bug, Silkwood, doubles): layouts, engine-level
models and the runtime room registry.  Rating 3/10 (GYM_PUZZLES section 2b):
  130 Lobby        the weavers' hall at the elder's foot (no puzzle since SPINE Rev 19)
  131 The Canopy   the gym's puzzle, web trampolines: puzzles/canopy.py
  132 Canopy Lofts + 134 Granny's Knot: the optional Upper Lofts (after the badge): spools, the brass Meridian wire, the knot
The map generator (gen_gym1.py) draws these same grids, so the proof and the map cannot drift apart.
Glyphs: # void / wall mass   W wall face   . floor   v loom bed (drop)   S stair cell (floor)   o loom (solid)."""
from .core import Model, Device, grid_cells, around

V_BRIDGE = 309                      # (305-307 are the Canopy's Joltik webs now: puzzles/canopy.py; 308 is free)
S_ALPHA, S_BRASS, S_GAMMA, S_KNOT = 305, 306, 307, 308

# ------------------------------------------------------------------------------------------------ 130 Lobby
# SPINE Revision 19: the puzzle moved up into the tree (131, puzzles/canopy.py).  The lobby at the elder's foot keeps the
# weavers: looms, Granny Loom's first loom and portrait, dye vats, silk drying, the gym guide, Tamsin's apology spiral.
# (The Rev 14 heddle-and-plank teach and the linked-heddle Weaving Hall are retired here; the linked-heddle idea is
# parked for a later dungeon, DUNGEON_PUZZLES.md.)
LOBBY = ['#' * 20, '#' * 20] + ['#' + 'W' * 18 + '#'] * 2 + ['#' + 'W' * 14 + 'S' + 'W' * 3 + '#'] * 2 + \
        ['#' + '.' * 18 + '#'] * 9 + ['#########.##########']
LOBBY_LOOMS = [(2, 8), (4, 8), (2, 11), (4, 11), (14, 11), (16, 11)]        # 2x2 each
LOBBY_AT = dict(exit=(9, 15), start=(9, 14), stair=(15, 4), arrive=(15, 6), guide=(7, 13), tamsin=(10, 9),
                first_loom=(6, 7), item=(17, 7), card=(12, 5), portrait=(8, 5), weaver=(13, 8))


# ------------------------------------------------------------------------------------------------ 132 Canopy Lofts
DECKS = {1: (1, 21), 2: (11, 19), 3: (3, 11), 4: (18, 13), 5: (11, 5), 6: (19, 2)}      # top-left of each 4x3 deck (P6: 4x4)
CENTRE = {1: (2, 22), 2: (12, 20), 3: (4, 12), 4: (19, 14), 5: (12, 6), 6: (20, 3)}
SPOOLS = {'s1': ((4, 22), 'alpha', 3, 2), 's2': ((14, 20), 'gamma', 5, 4), 's3': ((6, 12), 'brass', 4, 1),
          's4': ((21, 14), 'brass', 2, 3), 's5': ((14, 6), 'gamma', 3, 2)}                 # pos, cord, ON -> deck, OFF -> deck
CORDS = {'alpha': (1, 21), 'gamma': (18, 13), 'brass': (3, 11)}
LADDERS = {2: (11, 21), 3: (3, 13), 4: (18, 15), 5: (11, 7)}
BRIDGE = {1: [(x, 5) for x in range(15, 19)], 2: [(20, y) for y in range(6, 13)]}
LOFT_AT = dict(arrive=(2, 22), down=(2, 24), warp=(22, 2), mossy=(1, 23), hollis=(13, 21), ash=(20, 15), item=(11, 5))


def _lofts():
    W, H = 25, 26
    g = [['#'] * W for _ in range(H)]
    for p, (x0, y0) in DECKS.items():
        for y in range(y0, y0 + (4 if p == 6 else 3)):
            for x in range(x0, x0 + 4): g[y][x] = '.'
    for cells in BRIDGE.values():
        for x, y in cells: g[y][x] = 'v'
    g[LOFT_AT['down'][1]][LOFT_AT['down'][0]] = 'S'
    return [''.join(r) for r in g]


LOFTS = _lofts()


def lofts_model():
    cells, _ = grid_cells(132, LOFTS, '#')
    solid = {s[0] for s in SPOOLS.values()} | set(CORDS.values()) | set(LADDERS.values()) | {LOFT_AT[k] for k in ('mossy', 'hollis', 'ash', 'item')}
    cells -= {(132, x, y) for x, y in solid}
    cells -= {(132,) + LOFT_AT['down']}      # exits to other rooms: not part of this proof
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
    m = Model('lh_lofts (132)', cells, passable, (132,) + LOFT_AT['arrive'], (0, 0, 0, 0), dev, [(132,) + LOFT_AT['warp']],
              resets=around(132, *LOFT_AT['mossy']))
    m.game = lambda v: ({V_BRIDGE: v[3]}, {S_ALPHA: bool(v[0]), S_BRASS: bool(v[1]), S_GAMMA: bool(v[2])})
    m.exits = [(132,) + LOFT_AT['down']]
    return m


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
    m = Model('lh_knot (134)', cells_all, passable, (134,) + KNOT_AT['start'], (0,) * 5, dev, [GOAL], resets=around(134, *KNOT_AT['lever']))
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


CHECKS = [(lofts_model, dict(moves=7, rating=4, without={'the brass wire': ['Cord brass']})),   # optional Upper Lofts
          (knot_model, dict(moves=3, rating=3))]                    # optional Granny's Knot

# Runtime registry (emitted as Ruby by puzzles/__init__.py -> Plugins/Prismfall Maps/007_PuzzleRooms.rb)
ROOMS = {
    'lh_lofts': dict(name='Canopy Lofts', map=132, start=list(LOFT_AT['arrive']) + [8],
                     reset=dict(vars={V_BRIDGE: 0}, switches={S_ALPHA: False, S_BRASS: False, S_GAMMA: False}),
                     solved=dict(vars={V_BRIDGE: 1}, switches={S_ALPHA: True, S_BRASS: True, S_GAMMA: True}, at=[20, 4, 8]),
                     hints=["The pattern card lists three cords. Count the cords up here.",
                            "The brass one isn't Gran's. Pull it and watch the far side of the canopy.",
                            "Pull the alpha cord, ride the spool to the west deck, pull the brass wire (a bridge swings out up "
                            "north). Ride on east, pull gamma, ride the spool there, then the next, and walk the bridge to Gran's door."]),
    'lh_knot': dict(name="Granny's Knot", map=134, start=list(KNOT_AT['start']) + [8],
                    reset=dict(states={'T%d' % (i + 1): 0 for i in range(5)}),
                    hints=["The sampler on the wall is the row Gran never finished: up, down, up, down, up.",
                           "Every treadle lifts the first thread. An odd number of presses leaves it up.",
                           "Press the first, fourth and fifth treadles, once each, in any order."]),
}

RUBY = """
PrismfallPuzzles.checker(:lh_knot, :lh_knot, {
  :first_down => "The chest is tied shut with one unfinished row. The first warp thread is down: the sampler starts UP.",
  :wrong_row  => "The chest is tied shut with one unfinished row. The threads don't match the sampler yet: up, down, up, down, up."
}) do
  ups = (1..5).map { |i| PrismfallPuzzles.state_of("T#{i}") == 1 }
  next [:ok] if ups == [true, false, true, false, true]
  next [:fail, ups[0] ? :wrong_row : :first_down]
end
"""
