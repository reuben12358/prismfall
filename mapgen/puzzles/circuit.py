"""Gym 4, the Circuit Gym (Lumen City; Rook Calder, Electric, :NEON_GRID): GYM_PUZZLES Gym 4 after its trim (map builder 15).

The trim (GYM_PUZZLES 0b: rating 5, at most 12 required moves, at most 1 024 states a room).  One rule all the way up:
power floods from the generator through every pair of facing ports (nodes, strips, lamps); a lit lamp does its job.
  190 Switchroom (TEACH, 2 moves): three straight nodes on one strip; turn the two sideways ones, the door lamp lights.
  191 Breadboard Hall (TWIST "tees, and the alarm", 3 moves): a 4x3 breadboard.  The generator's tee sends power east
      along the middle row, straight into Rook's camera flash (the ALARM: every node snaps back to where it started).
      The door route bends north at the generator, runs the top row and turns up at the end; turning the last corner
      wrong also feeds the alarm.  Four nodes turn; the rest are soldered.
  192 Live Wire Hall (COMBINE "the drone is a wire; the latch remembers", 6 moves): the west circuit has a gap at the
      drone socket; docking Rook's Rotom drone closes it and lights the gate's latch (it stays open for good).  Live
      strips shock, so you call the drone back to cross.  The east board has no generator: it is fed THROUGH the
      latched gate, so you set its tee on the far side, walk back and dock again.  The tee's third port faces the alarm
      (it trips the breakers: nothing latches, the tee snaps back, the drone comes home).
  193 The Core (1 move): the Plate's cradle is cold; the arena door runs on a Meridian main - splice it.
Ports: N=1 E=2 S=4 W=8, rotated clockwise per state (PrismfallPuzzles.rot_mask).  Shapes at rotation 0: I = N+S,
L = N+E, T = N+E+S."""
from .core import Model, Device, machine, verify, rating_check

N_, E_, S_, W_ = 1, 2, 4, 8
PORTS = {'I': N_ | S_, 'L': N_ | E_, 'T': N_ | E_ | S_}
NROT = {'I': 2, 'L': 4, 'T': 4}
DXY = {N_: (0, -1), E_: (1, 0), S_: (0, 1), W_: (-1, 0)}
OPP = {N_: S_, S_: N_, E_: W_, W_: E_}
H, V = E_ | W_, N_ | S_

# Switch / variable ids (GYM_PUZZLES Gym 4 block 320-324; mapgen/flags.yaml)
S_190_DOOR, S_LATCH_GATE, S_LATCH_CORE, S_DOCKED, S_191_DOOR, S_SPLICE = 320, 321, 322, 323, 324, 325
V_ALARMS = 320


def rotm(m, k):
    for _ in range(k % 4): m = ((m << 1) & 15) | (m >> 3)
    return m


def strips(cells, pts, mask):
    for p in pts: cells[p] = ('S', mask)


def hrun(y, x0, x1): return [(x, y) for x in range(x0, x1 + 1)]
def vrun(x, y0, y1): return [(x, y) for y in range(y0, y1 + 1)]


# ------------------------------------------------------------------ 190 Switchroom (21x15)
def board_190():
    c = {}
    strips(c, hrun(9, 3, 4) + hrun(9, 6, 8) + hrun(9, 10, 12) + hrun(9, 14, 16), H)
    c[(5, 9)] = ('N', 'I', 0, True); c[(9, 9)] = ('N', 'I', 1, True); c[(13, 9)] = ('N', 'I', 0, True)
    c[(17, 9)] = ('L', 'door190', W_)
    return dict(map=190, source=((2, 9), E_), cells=c)


# ------------------------------------------------------------------ 191 Breadboard Hall (27x21)
COLS191, ROWS191 = (6, 11, 16, 21), (10, 15, 20)
GRID191 = {(0, 0): ('L', 1, False), (1, 0): ('I', 0, True), (2, 0): ('I', 1, False), (3, 0): ('L', 2, True),
           (0, 1): ('T', 1, True), (1, 1): ('I', 1, False), (2, 1): ('I', 0, True), (3, 1): ('T', 3, False),
           (0, 2): ('L', 0, False), (1, 2): ('I', 1, False), (2, 2): ('L', 3, False), (3, 2): ('L', 3, False)}


def board_191():
    c = {}
    for (ci, ri), (sh, r0, rot) in GRID191.items():
        c[(COLS191[ci], ROWS191[ri])] = ('N', sh, r0, rot)
    for y in ROWS191:
        for a, b in zip(COLS191, COLS191[1:]): strips(c, hrun(y, a + 1, b - 1), H)
    for x in COLS191:
        for a, b in zip(ROWS191, ROWS191[1:]): strips(c, vrun(x, a + 1, b - 1), V)
    strips(c, hrun(15, 3, 5), H)                     # generator feed
    strips(c, vrun(21, 6, 9), V)                     # up to the door
    strips(c, hrun(15, 22, 25), H)                   # out to the camera flash
    c[(21, 5)] = ('L', 'door191', S_)
    c[(26, 15)] = ('L', 'alarm', W_)
    return dict(map=191, source=((2, 15), E_), cells=c)


# ------------------------------------------------------------------ 192 Live Wire Hall (27x25)
FENCE_X, GATE_Y = 13, 16
C192, CORE_DOOR = (17, 16), (20, 5)


def board_192():
    c = {}
    strips(c, [(3, 10)] + hrun(10, 5, 7), H)
    c[(4, 10)] = ('N', 'I', 1, False)                 # a: soldered E-W
    c[(8, 10)] = ('N', 'L', 2, False)                 # b: soldered S-W
    strips(c, vrun(8, 11, 15), V)
    c[(8, GATE_Y)] = ('B', N_ | E_, S_DOCKED)         # g1: the drone socket (a conductor only with Rotom docked)
    strips(c, hrun(GATE_Y, 9, 12), H)
    c[(FENCE_X, GATE_Y)] = ('L', 'latch1', W_ | E_)   # the inner gate's lock L1: lights, and passes power east
    strips(c, hrun(GATE_Y, 14, 16), H)
    c[C192] = ('N', 'T', 0, True)                     # c: the east tee (needs W+N; its E port faces the alarm)
    c[(18, GATE_Y)] = ('L', 'alarm', W_)
    strips(c, vrun(17, 11, 15), V)
    c[(17, 10)] = ('N', 'L', 1, False)                # d: soldered E-S
    strips(c, hrun(10, 18, 19), H)
    c[(20, 10)] = ('N', 'L', 3, False)                # e: soldered W-N
    strips(c, vrun(20, 6, 9), V)
    c[CORE_DOOR] = ('L', 'latch2', S_)                # the Core door's lock L2
    return dict(map=192, source=((2, 10), E_), cells=c)


BOARDS = {190: board_190(), 191: board_191(), 192: board_192()}


def masks(board, rots, sw):
    out = {}
    for p, k in board['cells'].items():
        if k[0] == 'S': out[p] = k[1]
        elif k[0] == 'N': out[p] = rotm(PORTS[k[1]], rots.get(p, k[2]))
        elif k[0] == 'L': out[p] = k[2]
        elif k[0] == 'B' and sw.get(k[2]): out[p] = k[1]
    src, sm = board['source']; out[src] = sm
    return out


def flood(board, rots, sw=None):
    """the same flood as PrismfallPuzzles.power: a neighbour is live when both facing ports exist"""
    m = masks(board, rots, sw or {}); src = board['source'][0]
    live = {src}; q = [src]
    while q:
        x, y = q.pop()
        for bit, (dx, dy) in DXY.items():
            if not m[(x, y)] & bit: continue
            n = (x + dx, y + dy)
            if n in live or n not in m or not m[n] & OPP[bit]: continue
            live.add(n); q.append(n)
    return live


def lit(board, rots, sw=None):
    live = flood(board, rots, sw)
    return {k[1] for p, k in board['cells'].items() if k[0] == 'L' and p in live}, live


def rotatable(board):
    return [(p, k[1], k[2]) for p, k in sorted(board['cells'].items()) if k[0] == 'N' and k[3]]


# ------------------------------------------------------------------ proofs
def proof_rotations(mid, goal_lamp, moves, rating):
    """190 / 191: a click-machine over the rotatable nodes; the alarm sends every node back to its start"""
    b = BOARDS[mid]; rot = rotatable(b)
    start = tuple(r0 for _, _, r0 in rot)
    def actions(s):
        out = []
        for i, (p, sh, r0) in enumerate(rot):
            t = list(s); t[i] = (t[i] + 1) % NROT[sh]; t = tuple(t)
            lamps, _ = lit(b, {rot[j][0]: t[j] for j in range(len(rot))})
            if 'alarm' in lamps: t = start
            out.append(('node %d,%d' % p, t))
        return out
    def goal(s):
        lamps, _ = lit(b, {rot[j][0]: s[j] for j in range(len(rot))})
        return goal_lamp in lamps and 'alarm' not in lamps
    return machine('g4_%d (%s)' % (mid, b and {190: 'Switchroom', 191: 'Breadboard Hall'}[mid]), start, actions, goal,
                   moves=moves, rating=rating)


def traps_191():
    """the twist really is there: one click on the middle row's straight node lights the alarm, and so does the top
    row with the last corner left unturned"""
    b = BOARDS[191]; rot = dict(((p, r0) for p, _, r0 in rotatable(b)))
    r1 = dict(rot); r1[(16, 15)] = 1
    r2 = dict(rot); r2[(6, 15)] = 2; r2[(11, 10)] = 1
    ok = 'alarm' in lit(b, r1)[0] and 'alarm' in lit(b, r2)[0] and 'door191' not in lit(b, r2)[0]
    return ok, ['%s g4_191 traps: the straight middle row (1 click) and the unturned last corner both light the alarm'
                % ('  ' if ok else 'FAIL')]


# 192 walking model -------------------------------------------------------------------------------
W192, H192 = 27, 28
START192 = (192, 6, 26)
APPRENTICE192 = (3, 24)
GEN192 = [(1, 9), (2, 9), (1, 10), (2, 10)]


def model_192():
    b = BOARDS[192]; cells_b = b['cells']
    floor = set()
    for y in range(6, H192 - 1):
        for x in range(1, W192 - 1):
            if x == FENCE_X and y != GATE_Y: continue
            floor.add((x, y))
    floor.add(CORE_DOOR)
    solid = {p for p, k in cells_b.items() if k[0] in ('N', 'B') or (k[0] == 'L' and k[1] == 'alarm')}
    solid |= set(GEN192) | {APPRENTICE192}                                         # the generator, Spark
    cells = {(192, x, y) for x, y in floor if (x, y) not in solid}
    c_cell = C192
    def state_rots(v): return {c_cell: v[0]}
    def live_of(v): return flood(b, state_rots(v), {S_DOCKED: bool(v[1])})
    cache = {}
    def live(v):
        if v not in cache: cache[v] = live_of(v)
        return cache[v]
    def passable(cell, v):
        _, x, y = cell
        if (x, y) not in floor or (x, y) in solid: return False
        if (x, y) in live(v) and cells_b.get((x, y), ('',))[0] in ('S', 'L'): return False      # live metal shocks
        if (x, y) == (FENCE_X, GATE_Y): return bool(v[2])
        if (x, y) == CORE_DOOR: return bool(v[3])
        return True
    # vars: (c rotation, docked, latch1, latch2)
    def power(v):
        lamps, _ = lit(b, state_rots(v), {S_DOCKED: bool(v[1])})
        c, d, l1, l2 = v
        if 'alarm' in lamps: return (0, 0, l1, l2)                # breakers trip: nothing latches, the tee snaps back
        return (c, d, l1 or ('latch1' in lamps), l2 or ('latch2' in lamps))
    def dock(v, cell):
        return (power((v[0], 1 - v[1], v[2], v[3])), cell)
    def turn(v, cell):
        return (power(((v[0] + 1) % 4, v[1], v[2], v[3])), cell)
    devs = [Device('dock / recall', [(192, 7, GATE_Y), (192, 8, GATE_Y + 1)], dock),
            Device('turn c', [(192, 16, GATE_Y), (192, 17, GATE_Y - 1), (192, 17, GATE_Y + 1)], turn)]
    v0 = (0, 0, 0, 0)
    m = Model('g4_192 (Live Wire Hall)', cells, passable, START192, v0, devs, goal=[(192,) + CORE_DOOR],
              resets=[(192, APPRENTICE192[0] + dx, APPRENTICE192[1] + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))])
    return m


def proof_193():
    return machine('g4_193 (the Core)', 0, lambda s: [('splice', 1)], lambda s: s == 1, moves=1, rating=1)


def budget():
    n = 0; lines = []
    for ok, out in (proof_rotations(190, 'door190', 2, 2), proof_rotations(191, 'door191', 3, 4)):
        n += int(out[0].split('shortest solution ')[1].split(' ')[0])
    ok2, out2 = verify(model_192(), moves=6, rating=5)
    n += int(out2[0].split('shortest solution ')[1].split(' ')[0]) + 1
    ok = n <= 12
    return ok, ['%s g4 required route: %d moves in all (190 + 191 + 192 + the splice; rating 5 allows 12)' % ('  ' if ok else 'FAIL', n)]


CHECKS = [(model_192, dict(moves=6, rating=5))]
EXTRA = [lambda: proof_rotations(190, 'door190', 2, 2), lambda: proof_rotations(191, 'door191', 3, 4), traps_191,
         proof_193, budget]

# ------------------------------------------------------------------ runtime registry (007_PuzzleRooms.rb)
def _node_states(mid):
    """a node event's one-hot state counts clicks from its START rotation (self switches all off = as built)"""
    return {'Node %d,%d' % p: 0 for p, _, r0 in rotatable(BOARDS[mid])}


def _solved(mid, target):
    b = BOARDS[mid]
    return {'Node %d,%d' % p: (target[p] - r0) % NROT[sh] for p, sh, r0 in rotatable(b)}


ROOMS = {
    'g4_190': dict(name='The Switchroom', map=190, start=[10, 13, 8], home=False,
                   reset=dict(switches={S_190_DOOR: False}, states=_node_states(190)),
                   solved=dict(switches={S_190_DOOR: True}, states=_solved(190, {(5, 9): 1, (9, 9): 1, (13, 9): 1})),
                   hints=["Power runs along the wire like water down a gutter. A junction only passes it if both ends line up.",
                          "The middle junction already lies along the wire. The other two are standing on end.",
                          "Turn the first and the last junction once each. The lamp by the door lights."]),
    'g4_191': dict(name='The Breadboard Hall', map=191, start=[13, 23, 8], home=False,
                   reset=dict(switches={S_191_DOOR: False}, states=_node_states(191)),
                   solved=dict(switches={S_191_DOOR: True}, states=_solved(191, {(6, 15): 2, (11, 10): 1, (21, 10): 3, (16, 15): 0})),
                   hints=["A tee sends power three ways. Make sure the third way's a wall, not Rook's camera.",
                          "Go north at the generator, not east. The middle row is a straight line to the flash.",
                          "Turn the generator's tee once, the top row's sideways junction once, and the top-right corner once."]),
    'g4_192': dict(name='The Live Wire Hall', map=192, start=[6, 26, 8], home=False,
                   reset=dict(switches={S_LATCH_GATE: False, S_LATCH_CORE: False, S_DOCKED: False}, states=_node_states(192)),
                   solved=dict(switches={S_LATCH_GATE: True, S_LATCH_CORE: True, S_DOCKED: False}, states=_solved(192, {(17, 16): 2})),
                   hints=["Latches hold. Wires don't have to. Once a lock clicks open it stays open, power or no power.",
                          "The east board has no generator. Its power comes through the gate - from Rotom, on this side.",
                          "Dock Rotom, call it back, cross, turn the east tee twice so it points west and north, come back, "
                          "dock again, call it back, and walk through."]),
}


def _rb_board(mid):
    b = BOARDS[mid]
    cells = []
    for (x, y), k in sorted(b['cells'].items()):
        if k[0] == 'S': cells.append('[%d, %d] => [:s, %d]' % (x, y, k[1]))
        elif k[0] == 'N': cells.append('[%d, %d] => [:n, %d, %d, %s, %d]' % (x, y, PORTS[k[1]], k[2], 'true' if k[3] else 'false', NROT[k[1]]))
        elif k[0] == 'L': cells.append('[%d, %d] => [:l, %d, :%s]' % (x, y, k[2], k[1]))
        elif k[0] == 'B': cells.append('[%d, %d] => [:b, %d, %d]' % (x, y, k[1], k[2]))
    (sx, sy), sm = b['source']
    return '    %d => { :source => [%d, %d, %d], :cells => { %s } },' % (mid, sx, sy, sm, ', '.join(cells))


RUBY = '''
# Gym 4 (map builder 15; mapgen/puzzles/circuit.py): the Circuit Gym's boards, generated from the proven model.
module PFCircuit
  BOARDS = {
%s
  }
  LAMP_SWITCH = { :door190 => %d, :door191 => %d }
  LATCH_SWITCH = { :latch1 => %d, :latch2 => %d }
  DOCKED = %d
  ALARMS = %d
  DXY = { 1 => [0, -1], 2 => [1, 0], 4 => [0, 1], 8 => [-1, 0] }
  OPP = { 1 => 4, 4 => 1, 2 => 8, 8 => 2 }
  module_function

  def rot(m, k)
    (k %% 4).times { m = ((m << 1) & 15) | (m >> 3) }
    return m
  end

  def ev_at(x, y, prefix)
    return $game_map.events.values.find { |e| e.x == x && e.y == y && e.name.start_with?(prefix) }
  end

  def masks(b)
    out = {}
    b[:cells].each do |(x, y), k|
      case k[0]
      when :s then out[[x, y]] = k[1]
      when :l then out[[x, y]] = k[1]
      when :b then out[[x, y]] = k[1] if $game_switches[k[2]]
      when :n
        e = k[3] ? ev_at(x, y, "Node") : nil
        out[[x, y]] = rot(k[1], e ? (k[2] + PrismfallPuzzles.state_of(e)) %% k[4] : k[2])
      end
    end
    sx, sy, sm = b[:source]
    out[[sx, sy]] = sm
    return out
  end

  def flood(b)
    m = masks(b)
    sx, sy, _ = b[:source]
    live = { [sx, sy] => true }
    q = [[sx, sy]]
    until q.empty?
      x, y = q.pop
      DXY.each do |bit, (dx, dy)|
        next if m[[x, y]] & bit == 0
        n = [x + dx, y + dy]
        next if live[n] || !m[n] || m[n] & OPP[bit] == 0
        live[n] = true
        q.push(n)
      end
    end
    return live
  end

  # recompute the board; returns the lit lamps.  The alarm wins: nothing latches, nodes snap back, Rotom comes home.
  def power(mid = $game_map.map_id, quiet = false)
    b = BOARDS[mid]
    return [] if !b
    live = flood(b)
    lamps = b[:cells].select { |(x, y), k| k[0] == :l && live[[x, y]] }.map { |_p, k| k[2] }
    if lamps.include?(:alarm)
      show_live(b, live)
      alarm!(mid, b) if !quiet
      return power(mid, true)
    end
    LAMP_SWITCH.each { |l, sw| $game_switches[sw] = lamps.include?(l) if b[:cells].any? { |_p, k| k[0] == :l && k[2] == l } }
    LATCH_SWITCH.each { |l, sw| $game_switches[sw] = true if lamps.include?(l) }
    show_live(b, live)
    return lamps
  end

  def show_live(b, live)
    $game_map.events.each_value do |e|
      next if !e.name.start_with?("Strip ") && !e.name.start_with?("Lock ")
      PrismfallPuzzles.set_self_switch(e, "A", live[[e.x, e.y]] ? true : false)
    end
    $game_map.need_refresh = true
  end

  def alarm!(mid, b)
    $game_screen.start_flash(Color.new(255, 255, 255, 220), 12)
    pbSEPlay("Thunder1") rescue nil
    pbWait(0.3) rescue nil
    $game_variables[ALARMS] += 1 if mid == 191
    b[:cells].each do |(x, y), k|
      next if k[0] != :n || !k[3]
      e = ev_at(x, y, "Node")
      PrismfallPuzzles.set_state(e.name, 0) if e
    end
    $game_switches[DOCKED] = false if mid == 192
    pbMessage(_INTL("Rotom: CHAT SAYS WRONG WIRE."))
    pbMessage(_INTL("The flash goes off in your face. Every junction snaps back to where it started."))
  end

  def turn(name, n = 4)
    PrismfallPuzzles.rotate(name, n)
    pbSEPlay("Battle ball shake") rescue nil
    power
  end

  def on_wire?
    x, y = $game_player.x, $game_player.y
    b = BOARDS[$game_map.map_id]
    return b && b[:cells][[x, y]] && [:s, :l].include?(b[:cells][[x, y]][0])
  end

  def socket
    if $game_switches[DOCKED]
      if pbConfirmMessage(_INTL("Rotom is humming in the socket. Call it back?"))
        $game_switches[DOCKED] = false
        pbSEPlay("PC close") rescue nil
        power
      end
    elsif on_wire?
      pbMessage(_INTL("Rotom: Bzzt! Not while you're standing on the wire, genius. Step off it first."))
    elsif pbConfirmMessage(_INTL("A drone-shaped gap in the wire. Dock Rotom here?"))
      $game_switches[DOCKED] = true
      pbSEPlay("PC open") rescue nil
      lamps = power
      pbMessage(_INTL("Rotom slots into the gap. The wire hums and the gate's latch clacks open.")) if lamps.include?(:latch1) && !lamps.include?(:latch2)
      pbMessage(_INTL("Power runs through the open gate and all the way across the hall. Somewhere north, a heavy lock clacks open.")) if lamps.include?(:latch2)
    end
  end

  # a live strip: the shock throws you back the way you came
  def shock
    $game_screen.start_flash(Color.new(120, 230, 255, 200), 8)
    pbSEPlay("Paralyze1") rescue nil
    back = { 2 => 8, 8 => 2, 4 => 6, 6 => 4 }[$game_player.direction]
    dx, dy = { 2 => [0, 1], 8 => [0, -1], 4 => [-1, 0], 6 => [1, 0] }[back]
    $game_player.moveto($game_player.x + dx, $game_player.y + dy) if $game_map.passable?($game_player.x + dx, $game_player.y + dy, back)
    pbMessage(_INTL("Zap! The wire is live."))
  end
end

def pfm_g4_power(mid = nil); return PFCircuit.power(mid || $game_map.map_id); end
def pfm_g4_turn(name, n = 4); return PFCircuit.turn(name, n);                end
def pfm_g4_socket;           return PFCircuit.socket;                          end
def pfm_g4_shock;            return PFCircuit.shock;                           end
PrismfallPuzzles.room(:g4_190)[:reset][:proc] = proc { PFCircuit.power(190, true) }
PrismfallPuzzles.room(:g4_191)[:reset][:proc] = proc { PFCircuit.power(191, true) }
PrismfallPuzzles.room(:g4_192)[:reset][:proc] = proc { PFCircuit.power(192, true) }
''' % ('\n'.join(_rb_board(m) for m in (190, 191, 192)), S_190_DOOR, S_191_DOOR, S_LATCH_GATE, S_LATCH_CORE, S_DOCKED, V_ALARMS)
