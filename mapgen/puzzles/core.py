"""mapgen/puzzles/core.py - the puzzle solver every room model runs on (GYM_PUZZLES section 4 item 10).

A Model is a room (or a set of linked rooms) as the ENGINE sees it:
  cells       {(map, x, y)}: every tile that can ever be stood on
  passable    f(cell, vars) -> bool: is the tile walkable in this puzzle state (planks, flats, bridges ...)
  links       {cell: cell}: touch warps between rooms (ladders); walking onto the key lands on the value
  devices     [Device]: things the player operates. `stand` = the tiles it can be used from (for a lever: its walkable
              neighbours; for a bump/touch device the same), act(vars, cell) -> (vars, cell) or None when it refuses
  goal        cells: reaching any of them solves the room
  resets      cells: standing on one, the room can be reset (tiles next to the apprentice / reset lever)
State = (the player's connected walk region, vars). A MOVE is one device use; walking is free.
verify() proves, by exhaustive BFS over every reachable state:
  1. the goal is reachable from the start, in exactly `moves` device uses when given (the intended minimum);
  2. no soft-lock: every reachable state can still reach the goal, or can reach a reset;
  3. no state leaves the player standing inside a wall (a flat or plank appearing/vanishing under them);
  4. optional `without`: {label: device names}: with those devices removed the goal must be UNreachable."""
from collections import deque

DIRS = ((0, 1), (0, -1), (1, 0), (-1, 0))


class Device:
    def __init__(self, name, stand, act, label=None):
        self.name, self.stand, self.act, self.label = name, list(stand), act, label or name


class Model:
    def __init__(self, name, cells, passable, start, vars0, devices, goal, links=None, resets=(), reset_to=None):
        self.name, self.cells, self.passable = name, set(cells), passable
        self.start, self.vars0, self.devices = start, vars0, list(devices)
        self.goal, self.links, self.resets = set(goal), dict(links or {}), set(resets)
        self.reset_to = reset_to or (start, vars0)

    def region(self, cell, v):
        seen = {cell}; q = [cell]
        while q:
            m, x, y = q.pop()
            for dx, dy in DIRS:
                n = (m, x + dx, y + dy)
                if n in self.cells and self.passable(n, v):
                    n = self.links.get(n, n)             # stepping onto a ladder / warp tile lands on its far end
                    if n not in seen:
                        seen.add(n); q.append(n)
        return frozenset(seen)

    def key(self, cell, v):
        r = self.region(cell, v)
        return (min(r), v), r

    def moves(self, r, v, skip=()):
        for d in self.devices:
            if d.name in skip: continue
            done = set()
            for c in d.stand:
                if c not in r: continue
                res = d.act(v, c)
                if res is None or res in done: continue
                done.add(res)
                yield d, c, res

    def explore(self, skip=()):
        k0, r0 = self.key(self.start, self.vars0)
        dist = {k0: 0}; prev = {k0: None}; regs = {k0: r0}; edges = {}; q = deque([k0]); embedded = []
        while q:
            k = q.popleft(); r = regs[k]; v = k[1]
            edges[k] = []
            for d, c, (v2, c2) in self.moves(r, v, skip):
                if not self.passable(c2, v2):
                    embedded.append((d.name, c, v, v2)); continue
                k2, r2 = self.key(c2, v2)
                edges[k].append(k2)
                if k2 not in dist:
                    dist[k2] = dist[k] + 1; prev[k2] = (k, d.label, c); regs[k2] = r2; q.append(k2)
        return dist, prev, regs, edges, embedded

    def solve(self, skip=()):
        dist, prev, regs, edges, emb = self.explore(skip)
        goals = [k for k in dist if regs[k] & self.goal]
        if not goals: return None, dist, regs, edges, emb
        best = min(goals, key=lambda k: dist[k]); path = []; k = best
        while prev[k]:
            path.append(prev[k][1]); k = prev[k][0]
        return path[::-1], dist, regs, edges, emb


def verify(model, moves=None, without=None, softlock=True):
    """Returns (ok, lines). `moves`: the intended minimum number of device uses."""
    out = []; ok = True
    path, dist, regs, edges, emb = model.solve()
    if emb:
        ok = False; out.append('FAIL %s: %d moves leave the player inside a wall, e.g. %r' % (model.name, len(emb), emb[0]))
    if path is None:
        return False, out + ['FAIL %s: the goal cannot be reached from the start state (%d states searched)' % (model.name, len(dist))]
    if moves is not None and len(path) != moves:
        ok = False; out.append('FAIL %s: shortest solution is %d moves, the design says %d: %s' % (model.name, len(path), moves, ' > '.join(path)))
    if softlock:
        good = {k for k in dist if regs[k] & model.goal}
        good |= {k for k in dist if regs[k] & model.resets}
        rev = {}
        for k, ns in edges.items():
            for n in ns: rev.setdefault(n, []).append(k)
        q = list(good)
        while q:
            k = q.pop()
            for p in rev.get(k, []):
                if p not in good: good.add(p); q.append(p)
        dead = [k for k in dist if k not in good]
        if dead:
            ok = False; out.append('FAIL %s: %d of %d reachable states are soft-locks (no goal, no reset), e.g. at %r vars %r'
                                   % (model.name, len(dead), len(dist), dead[0][0], dead[0][1]))
    for label, names in (without or {}).items():
        p2 = model.solve(skip=set(names))[0]
        if p2 is not None:
            ok = False; out.append('FAIL %s: still solvable without %s: %s' % (model.name, label, ' > '.join(p2)))
        else:
            out.append('  proved: unsolvable without %s' % label)
    out.insert(0, '%s %s: %d reachable states, shortest solution %d moves: %s' % (
        'ok  ' if ok else 'FAIL', model.name, len(dist), len(path), ' > '.join(path)))
    return ok, out


def grid_cells(mid, rows, solid='#'):
    """ASCII rows -> ({(mid, x, y)} of non-solid chars, {char: [(x, y)]})."""
    cells = set(); where = {}
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            where.setdefault(ch, []).append((x, y))
            if ch not in solid: cells.add((mid, x, y))
    return cells, where


def around(mid, x, y):
    return [(mid, x + dx, y + dy) for dx, dy in DIRS]


def machine(name, start, actions, goal, moves=None, invariant=None):
    """Proof for a puzzle with no walking in it (chimes, anchors): a plain state machine.
    actions(state) -> [(label, state)]; goal(state) -> bool; invariant(state) -> bool must hold everywhere."""
    dist = {start: 0}; prev = {start: None}; q = deque([start]); edges = {}
    while q:
        s = q.popleft(); edges[s] = []
        for label, t in actions(s):
            edges[s].append(t)
            if t not in dist: dist[t] = dist[s] + 1; prev[t] = (s, label); q.append(t)
    goals = [s for s in dist if goal(s)]
    if not goals: return False, ['FAIL %s: goal unreachable (%d states)' % (name, len(dist))]
    best = min(goals, key=lambda s: dist[s]); path = []; s = best
    while prev[s]: path.append(prev[s][1]); s = prev[s][0]
    path = path[::-1]; ok = True; out = []
    if moves is not None and len(path) != moves:
        ok = False; out.append('FAIL %s: shortest is %d moves, design says %d' % (name, len(path), moves))
    good = set(goals); rev = {}
    for s, ns in edges.items():
        for n in ns: rev.setdefault(n, []).append(s)
    st = list(good)
    while st:
        s = st.pop()
        for p in rev.get(s, []):
            if p not in good: good.add(p); st.append(p)
    if len(good) != len(dist):
        ok = False; out.append('FAIL %s: %d soft-locked states' % (name, len(dist) - len(good)))
    if invariant and not all(invariant(s) for s in dist):
        ok = False; out.append('FAIL %s: invariant broken' % name)
    out.insert(0, '%s %s: %d reachable states, shortest solution %d moves: %s' % ('ok  ' if ok else 'FAIL', name, len(dist), len(path), ' > '.join(path)))
    return ok, out
