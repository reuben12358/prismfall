"""Gym 7, the Foundry (Cindervault; Brann Holloway, Fire, :VOLCANIC, cap 39): GYM_PUZZLES "Gym 7".

One rule: POUR, THEN QUENCH. A trench is EMPTY (a dark gap), a pour makes it MOLTEN (impassable, glowing), a quench makes
it IRON (a bridge).  Crucibles pour once, through a spout aimed at one of two trenches; the foundry has ONE quench.  A
trench still molten when you go down a slag chute DRAINS into the mould below it: a gap upstairs, a bridge downstairs.
  250 Gate Hall (TEACH, 2 moves): one crucible, one trench, the wheel.  Pour, quench, cross.
  251 Pour Floor + 252 Mould Floor (TWIST + COMBINE, 7 moves): three trenches X1..X3 (south to north) in the walls
      between four bands; crucibles K1..K3 aim at (X1|X2), (X2|X3), (X1|X3).  Below, moulds M1..M3 under each trench.
      Shortest solution (the solver's): pour K1 > X1 and K2 > X2 as they stand, quench X2 only, turn K3 to X3 and pour,
      chute C1 (X1 and X3 drain: M1, M3 iron), below cross M1, ladder up into mid1, cross X2, chute C2 in mid2, below
      cross M3, ladder up into the north band.  (GYM_PUZZLES' hand solution, K3 > X1 / K1 > X2 / K2 > X3, is the same
      idea with one more aim: 8 moves.)
      The aha: quenching X1 to cross it is the natural move, and it leaves M1 a pit and X2 unquenchable.
  MASTERY (252's vault, optional, 3 moves): leave X2 molten too when you take C1, M2 casts and the cracked mould opens.
The maps (mapgen/layouts/foundry_gym.py) are drawn from the grids below, so map and proof cannot drift."""
from .core import Model, Device, machine, verify, DIRS

# ids (GYM_PUZZLES Gym 7, mapgen/flags.yaml)
V_AIM = {1: 335, 2: 336, 3: 337}
V_QUENCHED, V_TEACH = 338, 339
S_POURED = {1: 335, 2: 336, 3: 337}
S_TEACH_DONE, S_VAULT = 338, 339
V_X = {1: 435, 2: 436, 3: 437}
S_M = {1: 435, 2: 436, 3: 437}

# crucible k: aim 0 -> first, 1 -> second
AIMS = {1: (1, 2), 2: (2, 3), 3: (1, 3)}

# ------------------------------------------------------------------ 251 Pour Floor (29x25)
#   bands: N rows 1-3 · mid2 rows 6-9 · mid1 rows 12-15 · S rows 18-23; the walls between them (rows 4-5, 10-11,
#   16-17) are solid except each trench, X3 / X2 / X1, three wide at x 13-15.
W, H = 29, 25
TRENCH_X = (13, 14, 15)
X_ROWS = {3: (4, 5), 2: (10, 11), 1: (16, 17)}
BANDS = {'N': (1, 3), 'mid2': (6, 9), 'mid1': (12, 15), 'S': (18, 23)}
EXIT_251 = (14, 0)            # up to the Warden Arena (253)
GOAL_251 = (14, 1)
START_251 = (14, 23)          # arriving from 250's door; the stair down to 250 is (14, 24)
CRUCIBLE = {1: (3, 19), 2: (7, 19), 3: (11, 19)}
VALVE = {1: (26, 19), 2: (24, 20), 3: (26, 21)}
CHUTE = {1: (8, 22), 2: (24, 7)}
SOOTY = (21, 19)
HATCH_251 = {'H': (4, 13), 'N': (24, 2)}          # ladders down to 252 (land beside the foot)

# ------------------------------------------------------------------ 252 Mould Floor (29x25, under 251)
#   north side rows 1-3 · M3 rows 4-5 (x 23-25) · east landing rows 6-9 x 21-27 · vault rows 6-9 x 10-18 ·
#   M2 rows 10-11 (x 13-15) · M1 side rows 12-15 · M1 rows 16-17 (x 13-15) · south part rows 18-23
M_COLS = {1: (13, 14, 15), 2: (13, 14, 15), 3: (23, 24, 25)}
M_ROWS = {1: (16, 17), 2: (10, 11), 3: (4, 5)}
VAULT = (10, 6, 18, 9)
EAST = (21, 6, 27, 9)
LADDER_252 = {'H': (4, 13), 'N': (24, 2), 'S': (4, 21)}     # up: H -> 251 mid1, N -> 251 N band, S -> 251 S band
BELLS = {'M1 side': (2, 14), 'east landing': (27, 8)}       # ring for Sooty (a reset), where a pit can strand you
CHEST = (14, 7)

# ------------------------------------------------------------------ 250 Gate Hall (21x17)
W0, H0 = 21, 17
TEACH_X, TEACH_ROWS = (9, 10, 11), (8, 9)
CRUCIBLE_250, WHEEL_250 = (6, 13), (14, 13)
DOOR_250 = (10, 2)            # to 251
START_250 = (10, 15)          # arriving from Cindervault (exit at (10, 16))


def floor_251():
    f = set()
    for name, (y0, y1) in BANDS.items():
        for y in range(y0, y1 + 1):
            for x in range(1, W - 1): f.add((x, y))
    for k, rows in X_ROWS.items():
        for y in rows:
            for x in TRENCH_X: f.add((x, y))
    f.add(GOAL_251)
    return f


def floor_252():
    f = set()
    for y in range(1, 4):
        for x in range(1, W - 1): f.add((x, y))
    for x0, y0, x1, y1 in (VAULT, EAST):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1): f.add((x, y))
    for y in range(12, 16):
        for x in range(1, W - 1): f.add((x, y))
    for y in range(18, 24):
        for x in range(1, W - 1): f.add((x, y))
    for k in M_COLS:
        for y in M_ROWS[k]:
            for x in M_COLS[k]: f.add((x, y))
    return f


def trench_of(x, y):
    if x not in TRENCH_X: return None
    for k, rows in X_ROWS.items():
        if y in rows: return k
    return None


def mould_of(x, y):
    for k in M_COLS:
        if x in M_COLS[k] and y in M_ROWS[k]: return k
    return None


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


def solid_251():
    s = set(CRUCIBLE.values()) | set(VALVE.values()) | {SOOTY}
    return s


def solid_252():
    return set(BELLS.values()) | {CHEST}


def model_foundry(goal='exit'):
    f1, f2 = floor_251(), floor_252()
    s1, s2 = solid_251(), solid_252()
    cells = {(251, x, y) for x, y in f1 if (x, y) not in s1} | {(252, x, y) for x, y in f2 if (x, y) not in s2}

    def passable(cell, v):
        mid, x, y = cell
        if mid == 251:
            if (x, y) not in f1 or (x, y) in s1: return False
            k = trench_of(x, y)
            return k is None or v[6 + k] == 2
        if (x, y) not in f2 or (x, y) in s2: return False
        k = mould_of(x, y)
        return k is None or bool(v[9 + k])

    links = {(252,) + LADDER_252['H']: (251, HATCH_251['H'][0] + 1, HATCH_251['H'][1]),
             (251,) + HATCH_251['H']: (252, LADDER_252['H'][0] + 1, LADDER_252['H'][1]),
             (252,) + LADDER_252['N']: (251, HATCH_251['N'][0] + 1, HATCH_251['N'][1]),
             (251,) + HATCH_251['N']: (252, LADDER_252['N'][0] + 1, LADDER_252['N'][1]),
             (252,) + LADDER_252['S']: (251, LADDER_252['S'][0], LADDER_252['S'][1] + 1)}   # one-way: the service stair up

    def around1(p): return [(251, p[0] + dx, p[1] + dy) for dx, dy in DIRS]
    devs = []
    for k in (1, 2, 3):
        def aim(v, c, k=k):
            if v[2 + k]: return None                                   # spent: the spout is cold
            t = list(v); t[k - 1] = 1 - t[k - 1]; return (tuple(t), c)
        def pour(v, c, k=k):
            if v[2 + k]: return None
            tgt = AIMS[k][v[k - 1]]
            t = list(v); t[2 + k] = 1
            if t[6 + tgt] != 1: t[6 + tgt] = 1                        # empty or iron -> molten
            return (tuple(t), c)
        def quench(v, c, k=k):
            if v[6] or v[6 + k] != 1: return None
            t = list(v); t[6] = 1; t[6 + k] = 2; return (tuple(t), c)
        devs += [Device('aim K%d' % k, around1(CRUCIBLE[k]), aim), Device('pour K%d' % k, around1(CRUCIBLE[k]), pour),
                 Device('quench X%d' % k, around1(VALVE[k]), quench)]
    for k, (cx, cy) in CHUTE.items():
        def chute(v, c, cx=cx, cy=cy):
            t = list(v)
            for j in (1, 2, 3):
                if t[6 + j] == 1: t[6 + j] = 0; t[9 + j] = 1         # the moulds fill
            return (tuple(t), (252, cx, cy))
        devs.append(Device('chute C%d' % k, [(251, cx, cy)], chute))
    resets = [(251, SOOTY[0] + dx, SOOTY[1] + dy) for dx, dy in DIRS]
    for bx, by in BELLS.values(): resets += [(252, bx + dx, by + dy) for dx, dy in DIRS]
    goal_cells = [(251,) + GOAL_251] if goal == 'exit' else [(252, CHEST[0] + dx, CHEST[1] + dy) for dx, dy in DIRS]
    m = Model('g7_foundry (Pour Floor + Mould Floor)' + ('' if goal == 'exit' else ' MASTERY vault'), cells, passable,
              (251,) + START_251, V0, devs, goal_cells, links=links, resets=resets)
    m.game = game
    m.exits = [(251,) + EXIT_251]
    return m


def model_vault(): return model_foundry('vault')


def model_250():
    f = set()
    for y in range(3, 8):
        for x in range(2, W0 - 2): f.add((x, y))
    for y in range(10, 16):
        for x in range(2, W0 - 2): f.add((x, y))
    for y in TEACH_ROWS:
        for x in TEACH_X: f.add((x, y))
    f.add((DOOR_250[0], DOOR_250[1] + 1))
    solid = {CRUCIBLE_250, WHEEL_250}
    cells = {(250, x, y) for x, y in f if (x, y) not in solid}
    def passable(cell, v):
        _, x, y = cell
        if (x, y) not in f or (x, y) in solid: return False
        if x in TEACH_X and y in TEACH_ROWS: return v == 2
        return True
    def around0(p): return [(250, p[0] + dx, p[1] + dy) for dx, dy in DIRS]
    devs = [Device('pour', around0(CRUCIBLE_250), lambda v, c: (1, c) if v == 0 else None),
            Device('quench', around0(WHEEL_250), lambda v, c: (2, c) if v == 1 else None)]
    m = Model('g7_250 (Gate Hall)', cells, passable, (250,) + START_250, 0, devs, [(250, DOOR_250[0], DOOR_250[1] + 1)])
    m.game = lambda v: ({V_TEACH: v}, {})
    return m


def traps():
    """the twist is real: quench X1 (the natural move) and the exit can no longer be reached without a reset"""
    m = model_foundry()
    v = (0, 0, 0, 1, 0, 0, 1, 2, 0, 0, 0, 0, 0)                     # K1 poured into X1 and X1 quenched
    m2 = Model(m.name, m.cells, m.passable, m.start, v, m.devices, m.goal, links=m.links, resets=m.resets)
    path = m2.solve()[0]
    ok = path is None
    return ok, ['%s g7 trap: after quenching X1 the exit is out of reach (Sooty has to reset the floor)' % ('  ' if ok else 'FAIL')]


CHECKS = [(model_250, dict(moves=2, rating=2)),
          (model_foundry, dict(moves=7, rating=6, without={'the second chute': ['chute C2'], 'a quench': ['quench X1', 'quench X2', 'quench X3']})),
          (model_vault, dict(moves=3, rating=6))]
EXTRA = [traps]

# ------------------------------------------------------------------ runtime registry (007_PuzzleRooms.rb)
RESET = dict(vars={V_AIM[1]: 0, V_AIM[2]: 0, V_AIM[3]: 0, V_QUENCHED: 0, V_X[1]: 0, V_X[2]: 0, V_X[3]: 0},
             switches={S_POURED[1]: False, S_POURED[2]: False, S_POURED[3]: False, S_M[1]: False, S_M[2]: False, S_M[3]: False})
ROOMS = {
    'g7_250': dict(name='The Gate Hall', map=250, start=[START_250[0], START_250[1], 8], home=False,
                   reset=dict(vars={V_TEACH: 0}, switches={S_TEACH_DONE: False}),
                   solved=dict(vars={V_TEACH: 2}, switches={S_TEACH_DONE: True}),
                   hints=["Pour first. The crucible's spout runs straight into the trench.",
                          "Molten iron's a wall. Turn the wheel and the cistern quenches it.",
                          "Pour the crucible, turn the quench wheel, walk across."]),
    'g7_foundry': dict(name='The Pour Floor', map=251, start=[START_251[0], START_251[1], 8], home=False,
                       reset=RESET,
                       solved=dict(vars={V_AIM[1]: 0, V_AIM[2]: 0, V_AIM[3]: 1, V_QUENCHED: 1, V_X[1]: 0, V_X[2]: 2, V_X[3]: 0},
                                   switches={S_POURED[1]: True, S_POURED[2]: True, S_POURED[3]: True,
                                             S_M[1]: True, S_M[2]: False, S_M[3]: True},
                                   at=[GOAL_251[0], GOAL_251[1] + 1, 8]),
                       hints=["Brann never wastes a pour. Whatever's still hot when you go down, the moulds get.",
                              "You only need one bridge up here. Which one can't the moulds give you?",
                              "Pour the first crucible into the near trench and the second into the middle one. Quench the middle "
                              "one only. Turn the third spout to the far trench and pour it. Then take the near chute."]),
}

RUBY = '''
# Gym 7 (mapgen/puzzles/foundry.py): pour, then quench.  The crucibles, valves and chutes of the Foundry.
module PFFoundry
  V_AIM = { 1 => %(a1)d, 2 => %(a2)d, 3 => %(a3)d }
  S_POURED = { 1 => %(p1)d, 2 => %(p2)d, 3 => %(p3)d }
  V_X = { 1 => %(x1)d, 2 => %(x2)d, 3 => %(x3)d }
  S_M = { 1 => %(m1)d, 2 => %(m2)d, 3 => %(m3)d }
  V_QUENCHED = %(q)d
  V_TEACH = %(t)d
  S_TEACH_DONE = %(td)d
  AIMS = { 1 => [1, 2], 2 => [2, 3], 3 => [1, 3] }
  NAMES = { 1 => "near", 2 => "middle", 3 => "far" }
  module_function

  def target(k); return AIMS[k][$game_variables[V_AIM[k]].to_i %% 2]; end

  def glow(strong = true)
    if defined?(PrismfallStaging)
      PrismfallStaging.flash(255, 140, 40, 10, strong ? 150 : 90)
    else
      $game_screen.start_flash(Color.new(255, 140, 40, 120), 10)
    end
  end

  def refresh; $game_map.need_refresh = true; end

  # a crucible: Aim the spout / Pour / Leave
  def crucible(k)
    if $game_switches[S_POURED[k]]
      pbMessage(_INTL("The crucible's empty. Its spout is cold."))
      return false
    end
    loop do
      cmd = pbMessage(_INTL("A crucible of molten iron. The spout points at the {1} trench.", NAMES[target(k)]),
                      [_INTL("Aim the spout"), _INTL("Pour"), _INTL("Leave")], 3)
      case cmd
      when 0
        $game_variables[V_AIM[k]] = 1 - $game_variables[V_AIM[k]].to_i
        pbSEPlay("Door slide", 70, 120) rescue nil
        refresh
      when 1
        x = target(k)
        $game_switches[S_POURED[k]] = true
        if $game_variables[V_X[x]] == 1
          pbSEPlay("Anim/Fire2", 70, 80) rescue nil
          pbMessage(_INTL("The iron runs into the {1} trench. It's already molten; it just gets hotter.", NAMES[x]))
        else
          $game_variables[V_X[x]] = 1
          pbSEPlay("Anim/Fire3", 90, 90) rescue nil
          glow
          refresh
          pbWait(0.3)
          pbMessage(_INTL("The iron runs down the spout and fills the {1} trench. It glows. Nobody's crossing that.", NAMES[x]))
        end
        return true
      else
        return false
      end
    end
  end

  # a quench valve: one charge for the whole floor
  def valve(k)
    if $game_variables[V_X[k]] != 1
      pbMessage(_INTL("Nothing to quench. The {1} trench isn't molten.", NAMES[k]))
      return false
    end
    if $game_variables[V_QUENCHED] > 0
      pbMessage(_INTL("The wheel spins and nothing comes. The cistern's dry."))
      return false
    end
    $game_variables[V_QUENCHED] = 1
    $game_variables[V_X[k]] = 2
    pbSEPlay("Anim/Water5", 90, 80) rescue nil
    $game_screen.start_tone_change(Tone.new(60, 60, 70, 60), 6)
    pbWait(0.35)
    $game_screen.start_tone_change(PrismfallStaging.map_tone, 20) rescue $game_screen.start_tone_change(Tone.new(0, 0, 0, 0), 20)
    refresh
    pbMessage(_INTL("Steam roars up from the {1} trench. When it clears, the iron's black and hard. A bridge.", NAMES[k]))
    return true
  end

  # a slag chute: whatever is still molten drains into the moulds below, then down you go
  def chute(dest_map = 252)
    drained = []
    [1, 2, 3].each do |k|
      next if $game_variables[V_X[k]] != 1
      $game_variables[V_X[k]] = 0
      $game_switches[S_M[k]] = true
      drained << k
    end
    if !drained.empty?
      pbSEPlay("Anim/Earth4", 90, 70) rescue nil
      $game_screen.start_shake(3, 9, 12)
      pbMessage(_INTL("A roar below: the moulds fill."))
    end
    refresh
    PrismfallPuzzles.swap_map(dest_map)
    return true
  end

  # 250: the one crucible and the wheel
  def teach_pour
    if $game_variables[V_TEACH] > 0
      pbMessage(_INTL("The crucible's empty."))
      return false
    end
    $game_variables[V_TEACH] = 1
    pbSEPlay("Anim/Fire3", 90, 90) rescue nil
    glow
    refresh
    pbMessage(_INTL("The iron fills the trench. It glows. Nobody's crossing that."))
    return true
  end

  def teach_quench
    case $game_variables[V_TEACH]
    when 0 then pbMessage(_INTL("Nothing to quench. The trench is empty."))
    when 2 then pbMessage(_INTL("The bridge is iron already."))
    else
      $game_variables[V_TEACH] = 2
      $game_switches[S_TEACH_DONE] = true
      pbSEPlay("Anim/Water5", 90, 80) rescue nil
      $game_screen.start_tone_change(Tone.new(60, 60, 70, 60), 6)
      pbWait(0.35)
      $game_screen.start_tone_change(PrismfallStaging.map_tone, 20) rescue $game_screen.start_tone_change(Tone.new(0, 0, 0, 0), 20)
      refresh
      pbMessage(_INTL("Steam. When it clears, the trench is iron. A bridge."))
    end
    return true
  end
end

def pfm_g7_crucible(k); return PFFoundry.crucible(k);   end
def pfm_g7_valve(k);    return PFFoundry.valve(k);      end
def pfm_g7_chute(m = 252); return PFFoundry.chute(m);   end
def pfm_g7_teach_pour;  return PFFoundry.teach_pour;    end
def pfm_g7_teach_quench; return PFFoundry.teach_quench; end
''' % dict(a1=V_AIM[1], a2=V_AIM[2], a3=V_AIM[3], p1=S_POURED[1], p2=S_POURED[2], p3=S_POURED[3], x1=V_X[1], x2=V_X[2],
           x3=V_X[3], m1=S_M[1], m2=S_M[2], m3=S_M[3], q=V_QUENCHED, t=V_TEACH, td=S_TEACH_DONE)
