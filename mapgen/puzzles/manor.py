"""D5 Thistledown Manor (546): "don't turn your back" (DUNGEON_PUZZLES D5), map builder 14.

The rule, exactly as the runtime plays it (`PrismfallPuzzles.pursue(ev, :creep)`, 005_Puzzles_Hooks.rb, called for
every chair of the room after each step): a chair that is strictly in the half-plane BEHIND you (the way you just
walked) and more than one tile away steps one tile toward you, the longer axis first, then the other; it never moves
through furniture, another chair or you.  Walking toward a chair or sideways past it keeps it in view: it freezes.
After the chairs move, a chair standing on an unused trapdoor drops into the wine cellar (gone).  Then any chair next
to you (Manhattan distance 1) has caught you: a ghost pours out of the stuffing (a wild battle), every chair of the
room goes home, the room resets (the portraits swing crooked) and you are put back at the room's door.  Leaving a room
resets it the same way.  Setting a portrait or pulling the attic cord turns you to face the wall: the chairs creep once.

TEACH  the stair hall (10 x 7): one chair between the vestibule arch and the grand stairs.  Sidestep while it is still
       far, so you pass it with a clear tile between you; it trails behind and can never close the gap.
TWIST  the portrait gallery (16 x 5): set the four portraits in curtain-call order (the Fool, Laertes, Dame Rosamund,
       the Old King: wall positions 3, 1, 4, 2).  One chair already sits in the west alcove under its curio case; it
       can't climb out while you are north of it.  The other is wedged between the cases.  Walk down past the east case
       and back up: it follows you round and backs itself into the empty east alcove.  Then the portraits are safe.
COMBINE the dining room: both chairs sit in the back-stair nook under the attic hatch.  Draw them out (step back,
       step in: each step away pulls them one closer), lead them over the trapdoors (the boards hold you, not an
       armchair), then pull the cord: pulling it turns your back on the room, so no chair may be left.

Every proof runs on these grids, which the layout script (layouts/manor.py) carves the rooms from, and on the built
map's passability (the zone cells must be floor, the solid cells must be solid)."""
from collections import deque
import os

S_TRAP = (521, 522)          # trapdoors used (each drops one chair, then jams shut)
S_GALLERY = 523              # the portraits are set: the gallery's chairs slump
S_HATCH = 524                # the attic ladder is down
V_PORTRAIT = 521             # portraits set in order (0-4)
S_CLEARED = 176              # THISTLEDOWN_CLEARED: every chair is still
ORDER = (3, 1, 4, 2)         # wall positions west -> east: 1 Laertes, 2 the Old King, 3 the Fool, 4 Dame Rosamund
WHO = {1: 'L', 2: 'K', 3: 'F', 4: 'Q'}
D = {'U': (0, -1), 'D': (0, 1), 'L': (-1, 0), 'R': (1, 0)}

# Zone grids in MAP coordinates: (origin x, origin y, rows).  '#' solid, '.' floor, 'C' a chair's home (in name order),
# 'S' the room's door (the reset spot), 'G' the stair foot (TEACH goal), '1'-'4' portrait stand cells, '5' the hatch
# stand, 'T' a trapdoor.
ZONES = {
    'f': (23, 18, [
        "####GGGG####",
        "#..........#",
        "#..........#",
        "#....C.....#",
        "#..........#",
        "#..........#",
        "#..........#",
        "#..........#",
        "#####SS#####"]),
    'g': (2, 8, [
        "##################",
        "#.1...2...3...4..S",
        "#................#",
        "#..........###...#",
        "#......###C#.#...#",
        "#......#C#.......#",
        "##################"]),
    'd': (39, 23, [
        "################",
        "##########5#####",
        "##########C#####",
        "##########C#####",
        "#######........#",
        "#######...T....#",
        "#######........#",
        "#.........T....#",
        "S..............#",
        "################"]),
}
RATING = {'f': 3, 'g': 4, 'd': 4}
NAMES = {'f': 'd5_stair_hall (546)', 'g': 'd5_portrait_gallery (546)', 'd': 'd5_dining_room (546)'}


class Zone:
    def __init__(self, key, traps=True, door=0):
        ox, oy, rows = ZONES[key]
        self.key = key; self.floor = set(); self.chairs = []; self.goal = set(); self.trap = []; self.start = None
        self.doors = []; self.portrait = {}
        for y, r in enumerate(rows):
            for x, ch in enumerate(r):
                c = (ox + x, oy + y)
                if ch == '#': continue
                self.floor.add(c)
                if ch == 'C': self.chairs.append(c)
                elif ch == 'S': self.doors.append(c)
                elif ch == 'G': self.goal.add(c)
                elif ch == 'T': self.trap.append(c)
                elif ch in '12345': self.portrait[c] = int(ch)
        self.start = self.doors[door]
        self.pfloor = None
        self.order = list(ORDER) if key == 'g' else [5] if key == 'd' else []
        if not self.goal: self.goal = set(self.floor)
        self.use_traps = traps

    def tick(self, p, f, cs, fallen):
        cs = list(cs); fallen = list(fallen); moved = 0
        fx, fy = D[f]
        for i, c in enumerate(cs):
            if c is None: continue
            dx, dy = c[0] - p[0], c[1] - p[1]
            if dx * fx + dy * fy >= 0 or abs(dx) + abs(dy) <= 1: continue
            h = (1 if -dx > 0 else -1, 0) if dx else None
            v = (0, 1 if -dy > 0 else -1) if dy else None
            for s in ([h, v] if abs(dx) >= abs(dy) else [v, h]):
                if s is None: continue
                n = (c[0] + s[0], c[1] + s[1])
                if n not in self.floor or n == p or n in cs: continue
                cs[i] = n; moved += 1; break
        for i, c in enumerate(cs):
            if c is not None and self.use_traps and c in self.trap and not fallen[self.trap.index(c)]:
                fallen[self.trap.index(c)] = True; cs[i] = None
        caught = any(c is not None and abs(c[0] - p[0]) + abs(c[1] - p[1]) <= 1 for c in cs)
        return tuple(cs), tuple(fallen), caught, moved

    def s0(self):
        return (self.start, tuple(self.chairs), tuple(False for _ in self.trap), 0)

    def reset(self, s):
        p, cs, fallen, prog = s
        return (self.start, tuple(None if c is None else h for c, h in zip(cs, self.chairs)), fallen, 0)

    def succ(self, s):
        """(label, next state, chairs moved, kind) kind: 'move' / 'act' / 'reset'"""
        p, cs, fallen, prog = s
        out = []
        for d, (dx, dy) in D.items():
            n = (p[0] + dx, p[1] + dy)
            if n not in self.floor or (self.pfloor is not None and n not in self.pfloor):
                if n not in self.floor and p in self.doors: out.append(('leave', self.reset(s), 0, 'reset'))
                continue
            if n in cs: continue
            cs2, f2, caught, mv = self.tick(n, d, cs, fallen)
            if caught: out.append(('caught', self.reset((n, cs2, f2, 0)), mv, 'reset'))
            else: out.append((d, (n, cs2, f2, prog), mv, 'move'))
        if p in self.portrait and prog < len(self.order):
            k = self.portrait[p]
            prog2 = prog + 1 if self.order[prog] == k else 0
            cs2, f2, caught, mv = self.tick(p, 'U', cs, fallen)
            if caught: out.append(('P%d caught' % k, self.reset((p, cs2, f2, 0)), mv, 'reset'))
            else: out.append(('P%d' % k, (p, cs2, f2, prog2), mv, 'act'))
        return out

    def is_goal(self, s):
        return s[0] in self.goal and s[3] >= len(self.order)

    def explore(self):
        s0 = self.s0(); dist = {s0: 0}; q = deque([s0]); edges = {}
        while q:
            s = q.popleft(); edges[s] = []
            if self.is_goal(s): continue
            for lab, t, mv, kind in self.succ(s):
                edges[s].append((t, kind))
                if t not in dist: dist[t] = dist[s] + 1; q.append(t)
        return dist, edges

    def solve(self):
        """the fewest moves (portrait / cord actions + lure runs: a straight run in which a chair moves), no resets"""
        k0 = (self.s0(), None, False); best = {k0: (0, 0)}; prev = {k0: None}; dq = deque([k0])
        found = None
        while dq:
            k = dq.popleft(); s, last, lm = k
            if self.is_goal(s):
                if found is None or best[k] < best[found]: found = k
                continue
            for lab, t, mv, kind in self.succ(s):
                if kind == 'reset': continue
                if kind == 'act': w, nm = 1, False
                else: w, nm = (1 if mv and not (lm and lab == last) else 0), bool(mv)
                k2 = (t, lab, nm); c2 = (best[k][0] + w, best[k][1] + 1)
                if k2 not in best or c2 < best[k2]:
                    best[k2] = c2; prev[k2] = (k, lab)
                    (dq.appendleft if w == 0 else dq.append)(k2)
        if found is None: return None, None
        path = []; k = found
        while prev[k]: path.append(prev[k][1]); k = prev[k][0]
        return best[found][0], path[::-1]


def fmt(path):
    out = []
    for x in path:
        if len(x) == 1 and out and out[-1][0] == x: out[-1][1] += 1
        else: out.append([x, 1])
    return ' '.join(('%s%d' % (a, n) if n > 1 else a) if len(a) == 1 else '[%s]' % a for a, n in out)


def verify_zone(key):
    z = Zone(key); name = NAMES[key]
    dist, edges = z.explore()
    moves, path = z.solve()
    lines = []; ok = True
    if path is None:
        return False, ['FAIL %s: the room cannot be solved (%d states)' % (name, len(dist))]
    configs = {(s[1], s[2], s[3]) for s in dist}
    # no soft-lock: from every reachable state the goal or a reset (caught / walking out) can be reached
    good = {s for s in dist if z.is_goal(s)}
    resettable = {s for s, es in edges.items() if any(k == 'reset' for t, k in es)}
    good |= resettable
    rev = {}
    for s, es in edges.items():
        for t, k in es: rev.setdefault(t, []).append(s)
    st = list(good)
    while st:
        s = st.pop()
        for p in rev.get(s, []):
            if p not in good: good.add(p); st.append(p)
    dead = [s for s in dist if s not in good]
    if dead:
        ok = False; lines.append('FAIL %s: %d soft-locked states, e.g. %r' % (name, len(dead), dead[0]))
    # the trick is needed
    if key == 'f':                                  # walking straight up the middle is caught
        for i, dc in enumerate(z.doors):
            zz = Zone('f', door=i); zz.pfloor = {c for c in zz.floor if c[0] == dc[0]}
            r = zz.solve()[1] is None; ok &= r
            lines.append('  proved: walking straight up from %r is caught' % (dc,) if r else 'FAIL %s: the straight walk from %r works' % (name, dc))
            if i:
                m2, p2 = Zone('f', door=i).solve(); ok &= p2 is not None
                lines.append('  also solvable from the other arch cell %r: %s' % (dc, fmt(p2)) if p2 else 'FAIL %s: unsolvable from %r' % (name, dc))
    if key == 'g':                                  # without the empty east alcove (filled) the room cannot be solved
        zz = Zone('g'); a = (2 + 12, 8 + 4); zz.floor.discard(a)
        r = zz.solve()[1] is None; ok &= r
        lines.append('  proved: unsolvable without the empty alcove' if r else 'FAIL %s: solvable without the alcove' % name)
        zz = Zone('g'); zz.pfloor = {c for c in zz.floor if c[1] == 9}
        r = zz.solve()[1] is None; ok &= r
        lines.append('  proved: the portraits alone (never leaving the wall) are caught' if r else 'FAIL %s: the wall walk works' % name)
    if key == 'd':
        for i in range(len(z.trap)):
            zz = Zone('d'); zz.trap = [t for j, t in enumerate(zz.trap) if j != i]
            r = zz.solve()[1] is None; ok &= r
            lines.append('  proved: unsolvable without trapdoor %d' % (i + 1) if r else 'FAIL %s: solvable without trapdoor %d' % (name, i + 1))
    from .core import rating_check
    k, line = rating_check(name, RATING[key], moves, len(configs)); ok &= k; lines.append(line)
    lines.insert(0, '%s %s: %d step states, %d chair/room states, %d moves (actions + lure runs), %d steps: %s' % (
        'ok  ' if ok else 'FAIL', name, len(dist), len(configs), moves, len(path), fmt(path)))
    return ok, lines


def d5_f(): return verify_zone('f')
def d5_g(): return verify_zone('g')
def d5_d(): return verify_zone('d')


MAP546 = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'maps_out', 'Data', 'Map546.rxdata')


def d5_built():
    """the grids against the built map: every zone floor cell is passable floor, every '#' inside a zone is solid"""
    if not os.path.exists(MAP546): return True, ['  d5 built check skipped (no Map546 yet)']
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import rmarshal as M, render as Rn, build as B
    m = M.load_file(MAP546); ts = Rn.tilesets()[m.tileset_id]; lay = m.data.data
    bad = []
    for key, (ox, oy, rows) in ZONES.items():
        for y, r in enumerate(rows):
            for x, ch in enumerate(r):
                X, Y = ox + x, oy + y
                p = B.cell_passable(lay, ts, X, Y)
                if ch == '#' and 0 < x < len(r) - 1 and 0 < y < len(rows) - 1 and p: bad.append((key, X, Y, 'open'))
                if ch != '#' and ch not in 'G' and not p: bad.append((key, X, Y, 'blocked'))
    if bad: return False, ['FAIL d5 built map: %d zone cells disagree with the grids, e.g. %r' % (len(bad), bad[:4])]
    return True, ['  d5 built map: every zone cell matches its grid (floor walkable, furniture solid)']


CHECKS = []
EXTRA = [d5_f, d5_g, d5_d, d5_built]


def zone_cells():
    out = {}
    for key in ZONES:
        for c in Zone(key).floor: out['%d,%d' % c] = key
    return out


ROOMS = {
    'd5_gallery': dict(name='The portrait gallery', map=546, home=False,
                       reset=dict(vars={V_PORTRAIT: 0}), solved=dict(switches={S_GALLERY: True}, vars={V_PORTRAIT: 4}),
                       hints=["The company bowed in order of billing, smallest part first. Dame Rosamund's diary says who was who.",
                              "A chair can't climb out of an alcove while you stand north of it. One of the two alcoves is empty.",
                              "Walk down past the east case and back up: the loose chair follows you round into the empty alcove. "
                              "Then straighten the Fool, Laertes, Dame Rosamund and the Old King."]),
    'd5_dining': dict(name='The dining room', map=546, home=False,
                      reset=dict(switches={S_TRAP[0]: False, S_TRAP[1]: False}), solved=dict(switches={S_HATCH: True}),
                      hints=["Pulling the attic cord means turning your back on the room.",
                             "The trapdoors hold you. They won't hold an armchair.",
                             "Step back from the nook and in again to draw the chairs out, then walk so each one has to cross a trapdoor to follow you."]),
}


def _rb():
    zc = zone_cells()
    homes = {}
    for key in ZONES:
        z = Zone(key)
        for i, c in enumerate(z.chairs): homes['Armchair %s%d' % (key, i + 1)] = list(c)
    starts = {}
    for key in ZONES:
        z = Zone(key); ox, oy, rows = ZONES[key]
        sx, sy = z.start
        d = 8 if key == 'f' else 4 if key == 'g' else 6
        starts[key] = [sx, sy, d]
    traps = [list(t) for t in Zone('d').trap]
    from . import rb
    return """
# D5 Thistledown Manor (546): the creeping armchairs (GENERATED from mapgen/puzzles/manor.py, the grids the proofs run on)
module PFManor
  ZONE   = %s
  HOME   = %s
  START  = %s
  TRAPS  = %s
  ORDER  = %s
  module_function

  def zone_at(x, y);  return ZONE["#{x},#{y}"]; end
  def live?(z)
    return false if !z || $game_switches[%d]
    return false if z == "g" && $game_switches[%d]
    return false if z == "d" && $game_switches[%d]
    return true
  end
  def chairs(z)
    return $game_map.events.values.select { |e| e.name.start_with?("Armchair #{z}") && e.character_name != "" }.sort_by { |e| e.name }
  end

  # after every step on 546 (and after a portrait or the cord): leaving a room resets it; in a live room the chairs creep
  def step(acted = false)
    return if !$game_map || $game_map.map_id != 546
    pl = $game_player
    z = zone_at(pl.x, pl.y)
    reset_room(@zone) if !acted && @zone && @zone != z
    @zone = z
    return if !live?(z)
    cs = chairs(z)
    cs.each { |ev| PrismfallPuzzles.pursue(ev, :creep) }
    if z == "d"
      cs.each do |ev|
        TRAPS.each_with_index do |t, i|
          next if ev.x != t[0] || ev.y != t[1] || $game_switches[%d + i]
          $game_switches[%d + i] = true
          $game_self_switches[[546, ev.id, "A"]] = true
          ev.refresh
          pbSEPlay("Battle damage weak", 90) rescue nil
          pbMessage(_INTL("CRASH! The trapdoor gives under the armchair, and it drops into the wine cellar. The lid slams shut and jams."))
        end
      end
      $game_map.need_refresh = true
    end
    if chairs(z).any? { |ev| (ev.x - pl.x).abs + (ev.y - pl.y).abs <= 1 }
      caught(z)
      return true
    end
    return false
  end

  def caught(z)
    pbSEPlay("Exclaim", 100) rescue nil
    pbMessage(_INTL("The armchair lunges! Its cushion splits, and something pours out of the stuffing!"))
    sp = [[:GASTLY, 15], [:SHUPPET, 15], [:DUSKULL, 15]][rand(3)]
    WildBattle.start(sp[0], sp[1])
    return if $game_map.map_id != 546
    pbFadeOutIn {
      reset_room(z)
      s = START[z]
      $game_player.moveto(s[0], s[1])
      $game_player.direction = s[2]
      $game_player.straighten
      $game_map.need_refresh = true
    }
    @zone = z
    pbMessage(_INTL("...You come to by the door. Every chair is back where it started, as if nothing happened."))
  end

  def reset_room(z)
    return if !z
    chairs(z).each { |ev| h = HOME[ev.name]; next if !h; ev.moveto(h[0], h[1]); ev.direction = 2 }
    $game_variables[%d] = 0 if z == "g" && !$game_switches[%d]
    $game_map.need_refresh = true
  end

  def enter
    @zone = nil
    $game_variables[%d] = 0 if !$game_switches[%d]
  end
end

# a portrait in the gallery: straighten it (the curtain-call order), then the chairs creep: your back is to the room
def pfm_portrait(k)
  if $game_switches[%d]
    pbMessage(_INTL("The portrait hangs straight. The painted eyes look pleased with you."))
    return
  end
  v = $game_variables[%d]
  if PFManor::ORDER[v] == k
    $game_variables[%d] = v + 1
    pbSEPlay("Door slide", 70, 120) rescue nil
    pbMessage(_INTL("You straighten the portrait. It stays put."))
  else
    $game_variables[%d] = 0
    pbSEPlay("Battle damage weak", 70) rescue nil
    pbMessage(_INTL("The moment you touch it, every portrait on the wall swings crooked again. Somewhere, a woman tuts."))
  end
  $game_map.need_refresh = true
  $game_player.turn_up
  return if PFManor.step(true)
  if $game_variables[%d] >= 4
    $game_switches[%d] = true
    $game_map.need_refresh = true
    pbSEPlay("Mining reveal") rescue nil
    pbMessage(_INTL("The whole company hangs straight at last. The armchairs sag, ordinary furniture again."))
    pbMessage(_INTL("Far below, in the vestibule, a key turns in the dining-room door."))
  end
end

# the attic cord in the back-stair nook: pulling it turns your back on the dining room (the event's next page climbs)
def pfm_manor_hatch
  return if !pbConfirmMessage(_INTL("A cord hangs from a hatch in the ceiling. Pull it?"))
  $game_player.turn_up
  return if PFManor.step(true)
  $game_switches[%d] = true
  $game_map.need_refresh = true
  pbSEPlay("Door open") rescue nil
  pbMessage(_INTL("The hatch drops open and a folding ladder clatters down into the nook."))
end

EventHandlers.add(:on_player_step_taken, :pf_manor_chairs, proc { PFManor.step })
EventHandlers.add(:on_enter_map, :pf_manor_enter, proc { |_old| PFManor.enter if $game_map && $game_map.map_id == 546 })
""" % (rb(zc), rb(homes), rb(starts), rb(traps), rb(list(ORDER)),
       S_CLEARED, S_GALLERY, S_HATCH, S_TRAP[0], S_TRAP[0],
       V_PORTRAIT, S_GALLERY, V_PORTRAIT, S_GALLERY,
       S_GALLERY, V_PORTRAIT, V_PORTRAIT, V_PORTRAIT, V_PORTRAIT, S_GALLERY,
       S_HATCH)


RUBY = _rb()
