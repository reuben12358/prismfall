"""Gym 2, Pell Playhouse (GYM_PUZZLES 'Gym 2'): layouts, models and the room registry.
151 and 152 are proved as ONE model: the loft's flats are the stage's flats.
Stage glyphs (151): # wall mass  W wall face  . stage/house floor  v pit / trap void  x mark (floor)
  s f t  scenery drop: a wall only in scene 1 / 2 / 3        S F T  bridge: floor only in scene 1 / 2 / 3
  A B    loft flat: a wall while it is IN (not flown)        C      rostrum: floor while IN, void once flown
  1 2 3  cue rope posts (solid)   L K ladders to the loft   E the upstage stair (goal)   D stair cell"""
from .core import Model, Device, grid_cells, around

V_SCENE, V_TURN, V_OVERTURE = 310, 312, 313
S_A, S_B, S_C, S_TRAP = 310, 311, 312, 314

# ------------------------------------------------------------------------------------------------ 150 Foyer
FOYER = ["####################",
         "####################",
         "#WWWWWWWWDWWWWWWWWW#",
         "#WWWWWWWWDWWWWWWWWW#",
         "#.......hhh.......##",
         "#...#.............##",
         "#..x1#............##",
         "#...#.............##",
         "#.................##",
         "#.................##",
         "#.................##",
         "#.................##",
         "#.................##",
         "#########.##########",
         "####################"]
FOYER_AT = dict(rope=(4, 6), mark=(3, 6), usher=(12, 6), script=(3, 9), wren=(14, 9), lady=(15, 11), exit=(9, 13), start=(9, 12), stair=(9, 2))


def foyer_model():
    cells, w = grid_cells(150, FOYER, '#W1')
    cells -= {(150,) + FOYER_AT[k] for k in ('usher', 'script', 'wren', 'lady')}
    passable = lambda c, v: FOYER[c[2]][c[1]] != 'h' or v[0] == 1
    dev = [Device('Cue: Overture', [c for c in around(150, *FOYER_AT['rope']) if c in cells], lambda v, c: ((1 - v[0],), c))]
    return Model('g2_foyer (150)', cells, passable, (150,) + FOYER_AT['start'], (0,), dev, [(150,) + FOYER_AT['stair']],
                 resets=around(150, *FOYER_AT['wren']))


# ------------------------------------------------------------------------------------------------ 151 + 152
STAGE = ["#########################",
         "#WWWWWWWWWWWDWWWWWWWWWWW#",
         "#WWWWWWWWWWWDWWWWWWWWWWW#",
         "#...s....###T###..#.....#",
         "#.L.s....#.....#.#3#..K.#",
         "#...s....#AAAAA#..x.....#",
         "#ssss....#.....#.....ttt#",
         "#....ffff#vvCvv#........#",
         "#........#.....#fffff...#",
         "#......#.#.....#....f...#",
         "#.....x2##.....B....f...#",
         "#......#.#.....#ttttf...#",
         "#fff.ffff#.....#....f...#",
         "#........#.....#....f...#",
         "#vvvSvvvvvvvFvvvvvvvTvvv#",
         "#vvvSvvvvvvvFvvvvvvvTvvv#",
         "#.......................#",
         "##x.....................#",
         "##1#........@.....P.....#",
         "#########################"]
LOFT = ["#########################",
        "#WWWWWWWWWWWWWWWWWWWWWWW#",
        "#WWWWWWWWWWWWWWWWWWWWWWW#",
        "#.....a....b....c.......#",
        "#.L...a.i..b..p.c.....K.#",
        "#.....a....b....c.......#",
        "#.123.a....b....c...123.#",
        "#########################",
        "#########################",
        "#########################",
        "#########################",
        "#########################",
        "#########################",
        "#########################",
        "#########################"]
ROPE_FLATS = {1: (0,), 2: (1, 2), 3: (0, 2)}             # counterweight coupling: rope -> flats A=0 B=1 C=2
STAGE_AT = dict(start=(12, 18), pip=(18, 18), goal=(12, 2), ferdie=(2, 8), rosalind=(2, 11), crewe=(21, 8))
LOFT_AT = dict(dot=(5, 4), item=(8, 4), trap=(14, 4), juggler=(18, 3))
SCENES = ['work lights', 'the Shipwreck', 'the Forest', 'the Throne']


def find(rows, ch):
    return [(x, y) for y, r in enumerate(rows) for x, c in enumerate(r) if c == ch]


def stage_passable(ch, scene, flown):
    if ch in 'sft': return scene != 'sft'.index(ch) + 1
    if ch in 'SFT': return scene == 'SFT'.index(ch) + 1
    if ch in 'AB': return flown['AB'.index(ch)]
    if ch == 'C': return not flown[2]
    return ch not in 'v'


def stage_model(with_loft=True, actors=True):
    """vars = (scene, A flown, B flown, C flown)."""
    sc, _ = grid_cells(151, STAGE, '#W123')
    lc, _ = grid_cells(152, LOFT, '#W123')
    solid = {(151,) + STAGE_AT['pip']} | {(152,) + LOFT_AT[k] for k in ('dot', 'item', 'juggler')}
    cells = (sc | lc) - solid

    def passable(c, v):
        m, x, y = c
        if m == 151:
            if actors and (x, y) in (STAGE_AT['ferdie'], STAGE_AT['rosalind'], STAGE_AT['crewe']):   # actors stand only in their scene
                who = [STAGE_AT['ferdie'], STAGE_AT['rosalind'], STAGE_AT['crewe']].index((x, y))
                if v[0] >= who + 1: return False
            return stage_passable(STAGE[y][x], v[0], v[1:])
        ch = LOFT[y][x]
        if ch in 'abc': return not v[1 + 'abc'.index(ch)]
        return True
    links = {}
    if with_loft:
        for ch in 'LK':
            (sx, sy), (lx, ly) = find(STAGE, ch)[0], find(LOFT, ch)[0]
            links[(151, sx, sy)] = (152, lx, ly + 1)          # ladder tiles: arrive one step below the ladder head
            links[(152, lx, ly)] = (151, sx, sy + 1)
    dev = []
    for n in (1, 2, 3):
        (rx, ry), = find(STAGE, str(n))
        dev.append(Device('Cue %d' % n, [c for c in around(151, rx, ry) if c in cells],
                          (lambda n: lambda v, c: None if v[0] == n else ((n,) + v[1:], c))(n), 'cue ' + SCENES[n]))
    for n in (1, 2, 3):
        def pull(v, c, n=n):
            f = list(v[1:])
            for i in ROPE_FLATS[n]: f[i] = not f[i]
            return (v[0],) + tuple(f), c
        for side, (rx, ry) in zip(('left', 'right'), find(LOFT, str(n))):
            dev.append(Device('Loft rope %d %s' % (n, side), [c for c in around(152, rx, ry) if c in cells], pull, 'loft rope %d (%s rail)' % (n, side)))
    m = Model('g2_stage (151+152)', cells, passable, (151,) + STAGE_AT['start'], (0, False, False, False), dev,
              [(151,) + STAGE_AT['goal']], links=links, resets=around(151, *STAGE_AT['pip']) + around(152, *LOFT_AT['dot']))
    return m


def stage_extra():
    """Script order is forced by the geometry: no Ship, no Forest or no loft = no way through."""
    from .core import verify
    out = []; ok = True
    for label, skip in (('the Shipwreck cue', {'Cue 1'}), ('the Forest cue', {'Cue 2'}), ('the Throne cue', {'Cue 3'})):
        if stage_model().solve(skip=skip)[0] is not None: ok = False; out.append('FAIL g2_stage: solvable without ' + label)
        else: out.append('  proved: g2_stage unsolvable without ' + label)
    if stage_model(with_loft=False).solve()[0] is not None: ok = False; out.append('FAIL g2_stage: solvable without the Fly Loft')
    else: out.append('  proved: g2_stage unsolvable without the Fly Loft')
    # the trapdoor (Mastery) can be reached
    m = stage_model(); m.goal = {(152,) + LOFT_AT['trap']}; m.name = 'g2_loft trapdoor (152)'
    k, o = verify(m, softlock=False); ok &= k; out += o
    return ok, out


# ------------------------------------------------------------------------------------------------ 153 Trap Room
TRAP = ["###########",
        "########*##",
        "#######..##",
        "##..####.##",
        "##.#####.##",
        "##.#.o.#.##",
        "##.#.#...##",
        "##.#..#..##",
        "####...####",
        "####...####",
        "#####@#####"]       # found by search (the spec's pattern opened after ONE turn): exactly 3 cranks, riding required
TRAP_OFF = (4, 2)                       # where the 11x11 board sits on the 20x15 map
TABLE = (3, 3, 5)                       # x0, y0, size (board coordinates); crank at its centre
TRAP_AT = dict(crank=(5, 5), chest=(8, 1), start=(5, 9), ladder=(5, 10), joss=(4, 9))


def table_solid(x, y, rot):
    """Is turntable cell (x, y) machinery after `rot` clockwise quarter turns? (board coordinates)"""
    x0, y0, n = TABLE; cx, cy = x0 + n // 2, y0 + n // 2
    dx, dy = x - cx, y - cy
    for _ in range(rot): dx, dy = dy, -dx            # undo one clockwise turn: (dx, dy) came from (dy, -dx)
    return TRAP[cy + dy][cx + dx] in '#o'


def trap_model():
    x0, y0, n = TABLE
    cells = {(153, x, y) for y in range(11) for x in range(11)
             if (x0 <= x < x0 + n and y0 <= y < y0 + n) or TRAP[y][x] not in '#*'}
    cx, cy = TRAP_AT['crank']
    cells -= {(153, cx, cy), (153,) + TRAP_AT['joss']}

    def passable(c, v):
        _, x, y = c
        if x0 <= x < x0 + n and y0 <= y < y0 + n: return not table_solid(x, y, v[0])
        return True

    def crank(v, c):
        dx, dy = c[1] - cx, c[2] - cy
        return ((v[0] + 1) % 4,), (153, cx - dy, cy + dx)
    dev = [Device('Crank', around(153, cx, cy), crank, 'crank')]
    gx, gy = TRAP_AT['chest']
    return Model('g2_trap (153)', cells, passable, (153,) + TRAP_AT['start'], (0,), dev, [(153, gx, gy + 1)],
                 resets=around(153, *TRAP_AT['joss']))


CHECKS = [(foyer_model, dict(moves=1)), (stage_model, dict(moves=5)), (trap_model, dict(moves=3))]
EXTRA = [stage_extra]

ROOMS = {
    'g2_foyer': dict(name='Playhouse Foyer', map=150, start=list(FOYER_AT['start']) + [8], reset=dict(vars={V_OVERTURE: 0}),
                     solved=dict(vars={V_OVERTURE: 1}),
                     hints=["The rope post is boxed in. Where's the only place you can stand to reach it?",
                            "Stand on the painted mark beside the rope and call the cue.",
                            "Stand on the X left of the rope post, face the post and pull: the curtain flies out. Walk through."]),
    'g2_stage': dict(name='Revolving Stage', map=151, start=[12, 17, 8],
                     reset=dict(vars={V_SCENE: 0}, switches={S_A: False, S_B: False, S_C: False}),
                     solved=dict(vars={V_SCENE: 3}, switches={S_A: True, S_B: True, S_C: False}, at=[12, 3, 8]),
                     hints=["Script order, love. The stage won't let you skip an act.",
                            "The Throne cue's on the far side. Seen the stage from above yet?",
                            "Cue the Shipwreck from the house mark and cross the gangplank. Cue the Forest from the stage-left "
                            "mark, climb the ladder, cross the loft and, at the RIGHT rail, pull rope 2 then rope 3. Climb down, "
                            "cue the Throne, and walk in through the gap: across the rostrum, up the dais."]),
    'g2_loft': dict(name='Fly Loft', map=152, start=[2, 5, 2], reset=dict(switches={S_A: False, S_B: False, S_C: False}),
                    hints=["Whatever leaves the stage comes up here. Where do you want to be standing when it does?",
                           "Rope 2 drags two flats. Rope 3 also catches the rostrum.",
                           "Walk to the right rail first. Pull rope 2, then rope 3: flats A and B hang up here, the rostrum stays "
                           "on the stage. Then take the right-hand ladder down."]),
    'g2_trap': dict(name='Trap Room', map=153, start=[TRAP_AT['start'][0] + TRAP_OFF[0], TRAP_AT['start'][1] + TRAP_OFF[1], 8],
                    reset=dict(vars={V_TURN: 0}),
                    hints=["The crank turns the floor, and whoever is leaning on it.",
                           "You don't have to walk to the far side. Ride there.",
                           "Stand left of the crank and turn it three times: you ride from west round to south. Then walk east "
                           "and up the right-hand corridor."]),
}
