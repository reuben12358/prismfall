"""Gym 7, the Foundry (Cindervault; Brann Holloway, Fire, :VOLCANIC, cap 39): GYM_PUZZLES "Gym 7", as Gemini built it.

The maps are Gemini's crafted Cindervault Gym (mapgen/layouts/cindervault_gym.py, 2026-11-26, commit 6cb085b3): every
device is an inline-Ruby event on those maps (crucibles, quench valves, chutes, Hessa, the Mould-Runner). This file is
the MODEL of them: the grids below are Gemini's floors as built (walls, decor, NPCs and devices in their places), the
devices do what Gemini's Ruby does, and `build.py` proves it twice, on these grids and on the built
maps_out/Data/Map250-252.rxdata (puzzles/built.py).  If Gemini moves an event, the built proof says so.

One rule: POUR, THEN QUENCH. A trench is EMPTY (a dark trough), a pour makes it MOLTEN (impassable), a quench makes it
IRON (a bridge).  Crucibles pour once, through a spout aimed at one of two trenches; the floor has ONE quench charge,
shared by the three valves (V338: 0 ready, 1 dry).  A trench still molten when you drop down a slag chute DRAINS into
the mould below it: a trough upstairs, a bridge downstairs.
  250 Entrance (TEACH, 2 moves): the crucible lever (7,13), the 5-wide trench x 10-14 rows 10-11, the quench wheel (17,13).
  251 Pour Floor + 252 Mould Floor (TWIST + COMBINE, 7 moves): trenches X1..X3 (rows 17-18, 11-12, 5-6; x 12-16)
      between four bands; crucibles K1..K3 aim at (X1|X2), (X2|X3), (X1|X3).  Below, moulds M1 / M2 under X1 / X2 and
      M3 (x 20-24, rows 5-6) between the C2 landing bay and the north band.
      Shortest (the solver's): pour K1 > X1 and K2 > X2 as they stand, quench X2, turn K3 to X3 and pour, chute C1 (X1
      and X3 drain: M1, M3 iron), below cross M1, ladder H up into mid1, cross X2, chute C2, below cross M3, the north
      ladder up into the north band.  (Hessa's spoken solution, K1 > X2 / K2 > X3 / K3 > X1, is 8 moves: one more aim.)
      The aha: quenching X1 to cross it is the natural move, and it leaves M1 a pit and X2 unquenchable.
  MASTERY (252's west vault, optional, 3 moves): leave X2 molten too when you take C1; M2 casts and the cracked mould's
      hoard opens (S339).  That run can't finish (X2 is gone upstairs): Hessa or the Mould-Runner resets.
Resets: Apprentice Hessa (251 S band) and the Mould-Runner (252 S floor, sends you up to 251).  Escapes that need no
reset: 252's ladders C1 (14,22) and C2 (23,8) go back up beside the chutes."""
from .core import Model, Device, grid_cells, DIRS

# ids (GYM_PUZZLES Gym 7, mapgen/flags.yaml; Gemini's cindervault_gym.py uses the same)
V_AIM = {1: 335, 2: 336, 3: 337}
V_QUENCHED, V_TEACH = 338, 339             # V338: the cistern's one charge, 0 ready / 1 dry
S_POURED = {1: 335, 2: 336, 3: 337}
S_TEACH_DONE, S_VAULT = 338, 339
V_X = {1: 435, 2: 436, 3: 437}
S_M = {1: 435, 2: 436, 3: 437}

# crucible k: aim 0 -> first, 1 -> second
AIMS = {1: (1, 2), 2: (2, 3), 3: (1, 3)}

# ------------------------------------------------------------------ 251 Pour Floor (29x27), as built
#   . floor   # wall / decor   1 2 3 trench X1..X3   K crucible   Q quench valve   C slag chute (walk onto it)
#   H ladder H down   N north ladder down   E up to the Warden Arena (253)   D down to 250   A Apprentice Hessa
#   T trainer (Garran 17,20 / Ivar 19,14)   o Full Heal   | sign
GRID_251 = [
    '#############################',   # 0
    '#############################',   # 1
    '##############E##############',   # 2
    '####...................N.####',   # 3   N band
    '###......#.#.....#.#......###',   # 4
    '############33333############',   # 5   X3
    '############33333############',   # 6
    '#####......#.....#........###',   # 7   mid2
    '#####...|..............C..###',   # 8   C2 (23,8)
    '###...#...#.......#.#.....###',   # 9
    '###........#.....#........###',   # 10
    '############22222############',   # 11  X2
    '############22222############',   # 12
    '###........#.....#........###',   # 13  mid1
    '###..H.............T...o..###',   # 14  ladder H (5,14)
    '###.....#.................###',   # 15
    '###.#......#.....#......#.###',   # 16
    '############11111############',   # 17  X1
    '############11111############',   # 18
    '###..K..K..K.........Q....###',   # 19  S band: K1 (5,19) K2 (8,19) K3 (11,19), Q1 (21,19)
    '###.......#......T....Q.#####',   # 20  Q2 (22,20)
    '####.................Q..#####',   # 21  Q3 (21,21)
    '###....|......C...A.....#.###',   # 22  C1 (14,22), Hessa (18,22)
    '####.....................####',   # 23
    '#####.....#.......#.....#####',   # 24  arrival from 250 (14,24)
    '############.DDD.############',   # 25
    '#############################']   # 26
START_251 = (14, 24)
GOAL_251 = (14, 3)                       # in front of the arena portal (14,2); 253's way back lands here
CRUCIBLE = {1: (5, 19), 2: (8, 19), 3: (11, 19)}
VALVE = {1: (21, 19), 2: (22, 20), 3: (21, 21)}
CHUTE = {1: (14, 22), 2: (23, 8)}
CHUTE_LANDS = {1: (14, 23), 2: (23, 9)}  # on 252
HESSA = (18, 22)
LADDER_251 = {'H': (5, 14), 'N': (23, 3)}
LADDER_251_TO = {'H': (6, 14), 'N': (22, 3)}             # where 252's way up lands on 251

# ------------------------------------------------------------------ 252 Mould Floor (29x27, under 251), as built
#   1 2 3 mould M1..M3   H ladder H up   N north ladder up   U ladder C1 up (beside the C1 landing)
#   V ladder C2 up (beside the C2 landing)   $ the cracked-mould hoard   R the Mould-Runner (reset)
#   T trainer (Dain 18,3 / Oda 8,21)   | sign
GRID_252 = [
    '#############################',   # 0
    '#############################',   # 1
    '#############################',   # 2
    '################..T....N.####',   # 3   north band; north ladder up (23,3)
    '###############.#..#.....####',   # 4
    '####################33333####',   # 5   M3 (x 20-24)
    '####################33333####',   # 6
    '####################......###',   # 7   C2 landing bay (lands 23,9)
    '#####..|#.$.#...####...V..###',   # 8   west: the vault, hoard (10,8) | east: ladder C2 up (23,8)
    '####.##.......##.###......###',   # 9
    '####.............###.#....###',   # 10  the bulkhead x 17-19 keeps vault and bay apart
    '############22222############',   # 11  M2
    '############22222############',   # 12
    '###........#.....#........###',   # 13  M1 side
    '###..H.................#..###',   # 14  ladder H up (5,14)
    '###.#...#............#....###',   # 15
    '###.#......#.....#........###',   # 16
    '############11111############',   # 17  M1
    '############11111############',   # 18
    '###........#.....#........###',   # 19  S floor (C1 lands 14,23)
    '###.......................###',   # 20
    '###.#...T..............#..###',   # 21
    '###........|..U...R.......###',   # 22  ladder C1 up (14,22), Mould-Runner (18,22)
    '####..#...............#..####',   # 23
    '#####...................#####',   # 24
    '#############################',   # 25
    '#############################']   # 26
HOARD = (10, 8)
RUNNER = (18, 22)
LADDER_252 = {'H': (5, 14), 'N': (23, 3), 'U': (14, 22), 'V': (23, 8)}
LADDER_252_TO = {'H': (6, 14), 'N': (22, 3), 'U': (14, 23), 'V': (22, 8)}   # where they land on 251

# ------------------------------------------------------------------ 250 Entrance (25x24), as built
#   X the teach trench   L crucible lever   W quench wheel   E up to 251   D out to 240 (arrival 12,22)
#   o Hyper Potion   p people (Gym Guide, Foreman, Medic, Flint)   | sign / statue
GRID_250 = [
    '#########################',   # 0
    '#########################',   # 1
    '#########################',   # 2
    '#########################',   # 3
    '##########.#E#.##########',   # 4   portal to 251 (12,4)
    '#####...............#####',   # 5
    '####...o.#.....#.#...####',   # 6
    '####.............#...####',   # 7
    '####.....#.....#.....####',   # 8
    '####.....#.....#.....####',   # 9
    '##########XXXXX##########',   # 10  the teach trench x 10-14
    '##########XXXXX##########',   # 11
    '####.....#.....#.....####',   # 12
    '######.L.........W.#.####',   # 13  lever (7,13), wheel (17,13)
    '###.##........|p...#..###',   # 14  drain grate sign, Foreman
    '###...................###',   # 15
    '###.#..p..............###',   # 16  Camper Flint (7,16)
    '###................#..###',   # 17
    '###...................###',   # 18
    '###.##...p.....p...##.###',   # 19  Gym Guide, Medic
    '####...#.........#...####',   # 20
    '#####.....|...|.....#####',   # 21  statues
    '#########.......#########',   # 22  arrival (12,22)
    '##########.DDD.##########']   # 23
START_250 = (12, 22)
GOAL_250 = (12, 5)                       # in front of the portal; 251's way back lands here
LEVER_250, WHEEL_250 = (7, 13), (17, 13)


def _where(grid, ch):
    return sorted((x, y) for y, row in enumerate(grid) for x, c in enumerate(row) if c == ch)


def _check_grids():
    """the constants above are the letters in the grids (a typo in one of them fails the import)"""
    for g, w, h in ((GRID_251, 29, 27), (GRID_252, 29, 27), (GRID_250, 25, 24)):
        assert len(g) == h and all(len(r) == w for r in g), 'foundry grid size'
    assert _where(GRID_251, 'K') == sorted(CRUCIBLE.values()) and _where(GRID_251, 'Q') == sorted(VALVE.values())
    assert _where(GRID_251, 'C') == sorted(CHUTE.values()) and _where(GRID_251, 'A') == [HESSA]
    assert _where(GRID_251, 'H') == [LADDER_251['H']] and _where(GRID_251, 'N') == [LADDER_251['N']]
    assert _where(GRID_252, '$') == [HOARD] and _where(GRID_252, 'R') == [RUNNER]
    for k, p in LADDER_252.items(): assert _where(GRID_252, k) == [p]
    assert _where(GRID_250, 'L') == [LEVER_250] and _where(GRID_250, 'W') == [WHEEL_250]
    for g, p in ((GRID_251, START_251), (GRID_251, GOAL_251), (GRID_250, START_250), (GRID_250, GOAL_250)):
        assert g[p[1]][p[0]] == '.', p
    for p in CHUTE_LANDS.values(): assert GRID_252[p[1]][p[0]] == '.', p
    for p in list(LADDER_252_TO.values()): assert GRID_251[p[1]][p[0]] == '.', p
    for p in LADDER_251_TO.values(): assert GRID_252[p[1]][p[0]] == '.', p


_check_grids()


# state: (aim1, aim2, aim3, poured1, poured2, poured3, quenched, x1, x2, x3, m1, m2, m3)
V0 = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)


def game(v):
    """model state -> the engine's variables and switches (for the built-map proof)"""
    vars_ = {V_AIM[k]: v[k - 1] for k in (1, 2, 3)}
    vars_[V_QUENCHED] = v[6]
    vars_.update({V_X[k]: v[6 + k] for k in (1, 2, 3)})
    sw = {S_POURED[k]: bool(v[2 + k]) for k in (1, 2, 3)}
    sw.update({S_M[k]: bool(v[9 + k]) for k in (1, 2, 3)})
    return vars_, sw


def _around(mid, p): return [(mid, p[0] + dx, p[1] + dy) for dx, dy in DIRS]


def model_foundry(goal='exit', vars0=V0, start=None):
    c1, _ = grid_cells(251, GRID_251)
    c2, _ = grid_cells(252, GRID_252)
    cells = c1 | c2

    def passable(cell, v):
        mid, x, y = cell
        ch = (GRID_251 if mid == 251 else GRID_252)[y][x]
        if ch in '123':
            k = int(ch)
            return v[6 + k] == 2 if mid == 251 else bool(v[9 + k])
        return ch == '.' or ch in ('HN' if mid == 251 else 'HNUV')

    links = {(251,) + LADDER_251[k]: (252,) + LADDER_251_TO[k] for k in LADDER_251}
    links.update({(252,) + LADDER_252[k]: (251,) + LADDER_252_TO[k] for k in LADDER_252})
    devs = []
    for k in (1, 2, 3):
        def aim(v, c, k=k):
            if v[2 + k]: return None                                   # spent: the spout is cold
            t = list(v); t[k - 1] = 1 - t[k - 1]; return (tuple(t), c)
        def pour(v, c, k=k):
            if v[2 + k]: return None
            tgt = AIMS[k][v[k - 1]]
            t = list(v); t[2 + k] = 1
            if t[6 + tgt] != 1: t[6 + tgt] = 1                        # empty or iron -> molten (iron re-melts)
            return (tuple(t), c)
        def quench(v, c, k=k):
            if v[6] or v[6 + k] != 1: return None                       # the cistern is dry / nothing molten there
            t = list(v); t[6] = 1; t[6 + k] = 2; return (tuple(t), c)
        devs += [Device('aim K%d' % k, _around(251, CRUCIBLE[k]), aim), Device('pour K%d' % k, _around(251, CRUCIBLE[k]), pour),
                 Device('quench X%d' % k, _around(251, VALVE[k]), quench)]
    for k, p in CHUTE.items():
        def chute(v, c, k=k):
            t = list(v)
            for j in (1, 2, 3):
                if t[6 + j] == 1: t[6 + j] = 0; t[9 + j] = 1         # the moulds fill
            return (tuple(t), (252,) + CHUTE_LANDS[k])
        devs.append(Device('chute C%d' % k, _around(251, p), chute))    # walk onto it and say Yes (No steps you back)
    resets = _around(251, HESSA) + _around(252, RUNNER)
    goal_cells = [(251,) + GOAL_251] if goal == 'exit' else _around(252, HOARD)
    m = Model('g7_foundry (Pour Floor + Mould Floor)' + ('' if goal == 'exit' else ' MASTERY vault'), cells, passable,
              start or (251,) + START_251, vars0, devs, goal_cells, links=links, resets=resets)
    m.game = game
    m.exits = [(251,) + p for p in _where(GRID_251, 'E') + _where(GRID_251, 'D')] + [(251,) + p for p in CHUTE.values()]
    return m


def model_vault(): return model_foundry('vault')


def model_250():
    cells, _ = grid_cells(250, GRID_250)

    def passable(cell, v):
        _, x, y = cell
        ch = GRID_250[y][x]
        return v == 2 if ch == 'X' else ch == '.'
    devs = [Device('pour', _around(250, LEVER_250), lambda v, c: (1, c) if v == 0 else None),
            Device('quench', _around(250, WHEEL_250), lambda v, c: (2, c) if v == 1 else None)]
    m = Model('g7_250 (Entrance)', cells, passable, (250,) + START_250, 0, devs, [(250,) + GOAL_250])
    m.game = lambda v: ({V_TEACH: v}, {S_TEACH_DONE: v == 2})
    m.exits = [(250,) + p for p in _where(GRID_250, 'E') + _where(GRID_250, 'D')]
    return m


def traps():
    """the twist is real: quench X1 (the natural move) and the exit is out of reach without a reset; and the mastery
    run (X2 drained into M2) can't finish either, as GYM_PUZZLES says"""
    from .built import rebuild
    out = []; ok = True
    for label, m in (('after quenching X1 the exit is out of reach (Hessa has to reset the floor)',
                      model_foundry(vars0=(0, 0, 0, 1, 0, 0, 1, 2, 0, 0, 0, 0, 0))),                 # K1 poured into X1, X1 quenched
                     ('after the vault (X2 drained) the exit is out of reach until a reset',
                      model_foundry(vars0=(0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0), start=(252, HOARD[0], HOARD[1] + 1)))):
        try:
            mb = rebuild(m)[0]
            where = [('', m), (' [built map]', mb)]
        except FileNotFoundError:
            where = [('', m)]
        for tag, mm in where:
            path, dist, regs = mm.solve()[:3]
            resets = any(regs[k] & mm.resets for k in dist)           # ...and a reset is in reach (no soft-lock)
            good = path is None and resets; ok &= good
            out.append('%s g7 trap%s: %s' % ('  ' if good else 'FAIL', tag, label))
    return ok, out


CHECKS = [(model_250, dict(moves=2, rating=2)),
          (model_foundry, dict(moves=7, rating=6, without={'the second chute': ['chute C2'], 'a quench': ['quench X1', 'quench X2', 'quench X3']})),
          (model_vault, dict(moves=3, rating=6))]
EXTRA = [traps]

# ------------------------------------------------------------------ runtime registry (007_PuzzleRooms.rb)
# Gemini's events do their own reset / hints / skip (Hessa, the Mould-Runner); this is the same state for the shared
# PrismfallPuzzles tools (debug skip / reset, the puzzle bots).
RESET = dict(vars={V_AIM[1]: 0, V_AIM[2]: 0, V_AIM[3]: 0, V_QUENCHED: 0, V_X[1]: 0, V_X[2]: 0, V_X[3]: 0},
             switches={S_POURED[1]: False, S_POURED[2]: False, S_POURED[3]: False, S_M[1]: False, S_M[2]: False, S_M[3]: False})
ROOMS = {
    'g7_250': dict(name='The Entrance', map=250, start=[START_250[0], START_250[1], 8], home=False,
                   reset=dict(vars={V_TEACH: 0}, switches={S_TEACH_DONE: False}),
                   solved=dict(vars={V_TEACH: 2}, switches={S_TEACH_DONE: True}),
                   hints=["Pull the west lever. The crucible pours straight into the trench.",
                          "Molten iron's a wall. Turn the east wheel and the quench hardens it.",
                          "Pull the crucible lever, turn the quench wheel, walk across."]),
    'g7_foundry': dict(name='The Pour Floor', map=251, start=[14, 23, 8], home=False,     # where Hessa's reset puts you
                       reset=RESET,
                       solved=dict(vars={V_QUENCHED: 1, V_X[1]: 0, V_X[2]: 2, V_X[3]: 0},     # Hessa's puzzleskip state
                                   switches={S_POURED[1]: True, S_POURED[2]: True, S_POURED[3]: True,
                                             S_M[1]: True, S_M[2]: False, S_M[3]: True},
                                   at=[GOAL_251[0], GOAL_251[1], 8]),
                       hints=["Brann never wastes a pour. Whatever's still molten when you drop down a chute casts the mould below it.",
                              "You only get one quench up here. M1 and M3 can carry you below; M2 only leads to the vault. "
                              "So which channel must be quenched upstairs?",
                              "Pour K1 into X1 and K2 into X2. Quench X2 only. Aim K3 at X3 and pour. Drop down Chute C1, "
                              "cross M1, climb Ladder H, cross X2, drop down Chute C2, cross M3 and climb the north ladder."]),
}
