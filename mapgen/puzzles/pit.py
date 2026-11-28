"""Gym 8, the Pit (Ironreach; Kaito Ren, Fighting, :COLOSSEUM, cap 43): GYM_PUZZLES "Gym 8", built by Gemini
(mapgen/layouts/ironreach_gym.py, maps 270-274).  One rule: EVERY STEP YOU TAKE, THEY TAKE.  Sparring partners
(pursuers) step one tile toward you after each of your steps (the larger gap first, else the other axis, else they
wait); they never cross a golden rope, a boulder or each other.  A partner next to you ends the round ("Stand up.
Again."): partners and boulders go back to their marks and you to the room's foot, unless you are standing on a rope
(a rope break).  Strength boulders hold plates; so does a partner.
  271 Sparring Floor  TEACH (west, the pillar: ring the West Pillar Bell, S344) + TWIST (east, the rope lines: ring the
                      East Rope-Line Bell, S340)
  272 Boulders & Plates  COMBINE: both plates held (boulders or partners), then the Central Ring Bell (S341)
  273 The Gauntlet    plates P1 + P2 held at once opens the arena gate (S342); MASTERY: the Marrowgate alcove (S343)

The proof is engine-level and step by step (a pursuer room cannot use core.Model, where walking is free): it reads
the zones from the maps' OWN step-hook event (the Ruby the engine runs: box, ropes, partners, boulders, plates, reset
tile), the boulders' push rules from their own scripts, and walkability from maps_out/Data/MapNNN.rxdata through
puzzles/built.Built (layers, tile events, standing NPCs, gates by switch).  Then a breadth-first search over
(you, every partner, every boulder, switches), one step or one push or one bell at a time, proves:
  1. the room's switch can be reached from the door (shortest solution: steps + pushes + uses);
  2. no soft-lock: from EVERY reachable state the switch, a reset (Hiro, a reset bell) or a tag (which is a reset)
     can still be reached.
SOLUTIONS[mid] keeps the solver's route as a move string (U/D/L/R a step, u/d/l/r a push or a use facing that way)
for the real-engine walk (tools/harness/visual/ch9/010_Ch9StoryCapture.rb)."""
import ast, os, re
from collections import deque

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIRV = {'D': (0, 1), 'L': (-1, 0), 'R': (1, 0), 'U': (0, -1)}
RB_DIR = {2: (0, 1), 4: (-1, 0), 6: (1, 0), 8: (0, -1)}
ROOMS = {}
CHECKS = []
SOLUTIONS = {}
CAP = 4000000


def _rb_list(s):
    return ast.literal_eval(s.replace('nil', 'None'))


def _script(ev, page=0):
    out = []; lst = ev.pages[page].list; i = 0
    while i < len(lst):
        if lst[i].code == 355:
            s = [lst[i].parameters[0]]; i += 1
            while i < len(lst) and lst[i].code == 655: s.append(lst[i].parameters[0]); i += 1
            out.append('\n'.join(s)); continue
        i += 1
    return '\n'.join(out)


class Room:
    """one built room as the engine runs it"""
    def __init__(self, mid):
        from .built import Built, active_page
        self.mid = mid
        self.b = Built([mid]); self.m = self.b.maps[mid]; self.W, self.H = self.m.width, self.m.height
        self.active_page = active_page
        evs = {e.name: e for e in self.m.events.values()}
        hook = next(e for e in self.m.events.values() if e.name.startswith('Pit Step Hook'))
        src = _script(hook)
        heads = list(re.finditer(r"if !\$game_switches\[(\d+)\] && plx >= (\d+) && plx <= (\d+) && ply >= (\d+) && ply <= (\d+)\n", src))
        self.zones = []
        for k, h in enumerate(heads):
            body = src[h.end(): heads[k + 1].start() if k + 1 < len(heads) else len(src)]
            z = dict(sw=int(h.group(1)), box=tuple(int(h.group(i)) for i in (2, 3, 4, 5)),
                     ropes={tuple(p) for p in _rb_list(re.search(r"_ropes = (\[.*?\])\n", body).group(1))},
                     purs=_rb_list(re.search(r"_purs = (\[.*?\])\n", body).group(1)),
                     blds=_rb_list(re.search(r"_blds = (\[.*?\])\n", body).group(1)),
                     reset=tuple(int(v) for v in re.search(r"\$game_player\.moveto\((\d+), ?(\d+)\)", body).groups()))
            pm = re.search(r"_plates = (\[.*?\])\n", body)
            z['plates'] = [tuple(p[1:]) for p in _rb_list(pm.group(1))] if pm else []
            z['auto'] = bool(re.search(r"if _all_held && !\$game_switches\[%d\]" % z['sw'], body))
            self.zones.append(z)
        self.purs = [n for z in self.zones for n, _, _ in z['purs']]
        self.blds = [n for z in self.zones for n, _, _ in z['blds']]
        self.start_of = {n: (x, y) for z in self.zones for n, x, y in z['purs'] + z['blds']}
        self.zone_of = {n: i for i, z in enumerate(self.zones) for n, _, _ in z['purs'] + z['blds']}
        moving = set(self.purs) | set(self.blds)
        for key in list(self.b.ev):                          # moving events are tracked by the search, not the map
            self.b.ev[key] = [e for e in self.b.ev[key] if e.name not in moving]
        self.static_events = {k: v for k, v in self.b.ev.items() if v}
        # boulders: rope / sill rules and whether a push can open the zone (273)
        self.push = {}
        for n in self.blds:
            s = _script(evs[n])
            blocked = {tuple(p) for p in _rb_list(re.search(r"_blocked = (\[.*?\])\n", s).group(1))}
            ropes = {tuple(p) for p in _rb_list(re.search(r"_ropes = (\[.*?\])\n", s).group(1))}
            auto = re.search(r"if _all_held && !\$game_switches\[(\d+)\]", s)
            self.push[n] = dict(blocked=blocked, ropes=ropes, auto=int(auto.group(1)) if auto else None)
        # bells: action events that turn a switch on; resets: events that move the player and partners back
        self.bells = []; self.resets = []
        for e in self.m.events.values():
            if e.name.startswith('Pit Step Hook') or e.name in moving: continue
            s = _script(e)
            if not s: continue
            mv = re.findall(r"\$game_player\.moveto\((\d+), ?(\d+)\)", s)
            names = re.findall(r"\['(\w+)', (\d+), (\d+)\]", s)
            if mv and any(n in moving for n, _, _ in names):
                objs = {n for n, _, _ in names if n in moving}
                self.resets.append((e.name, (e.x, e.y), objs, tuple(int(v) for v in mv[-1])))
                continue
            on = re.findall(r"\$game_switches\[(\d+)\] = true", s)
            if on and 'Bell' in e.name:
                need = re.findall(r"_heavy = \[(.*?)\]", s)
                heavy = re.findall(r'"(\w+)"', need[0]) if need else None
                self.bells.append((e.name, (e.x, e.y), int(on[0]), heavy))
        self._pass = {}

    # ---- static walkability (layers + standing events), per switch set
    def tables(self, sw):
        key = frozenset(sw)
        if key in self._pass: return self._pass[key]
        swd = {s: True for s in sw}
        b, mid = self.b, self.mid
        def block_ev(x, y):                       # PrismfallPuzzles.blocked_by_event?: any solid char / tile event
            for e in self.static_events.get((mid, x, y), []):
                pg = self.active_page(e, {}, swd)
                if pg is None or pg.through: continue
                if pg.graphic.character_name or pg.graphic.tile_id > 0: return True
            return False
        pl, mv = {}, {}
        for y in range(self.H):
            for x in range(self.W):
                for d, (dx, dy) in DIRV.items():
                    n = (x + dx, y + dy)
                    if not (0 <= n[0] < self.W and 0 <= n[1] < self.H): continue
                    ok = b.can_move((mid, x, y), (mid,) + n, {}, swd)
                    pl[(x, y, d)] = ok
                    mv[(x, y, d)] = ok and not block_ev(*n)
        self._pass[key] = (pl, mv)
        return pl, mv

    # ---- the engine's rules
    def in_box(self, z, p):
        x0, x1, y0, y1 = z['box']
        return x0 <= p[0] <= x1 and y0 <= p[1] <= y1

    def held(self, plates, heavy, pos):
        return all(any(pos[h] == pl for h in heavy) for pl in plates)

    def step_hook(self, p, pos, sw):
        """after a player step: every live zone's partners move; plates; a tag resets the zone"""
        sw = set(sw)
        for zi, z in enumerate(self.zones):
            if z['sw'] in sw or not self.in_box(z, p): continue
            _, mv = self.tables(sw)
            occ = {pos[n] for n in pos}
            for n, _, _ in z['purs']:
                ex, ey = pos[n]; dx, dy = p[0] - ex, p[1] - ey
                if abs(dx) + abs(dy) <= 1: continue
                horiz = 'R' if dx > 0 else ('L' if dx < 0 else None)
                vert = 'D' if dy > 0 else ('U' if dy < 0 else None)
                order = [horiz, vert] if abs(dx) >= abs(dy) else [vert, horiz]
                for d in order:
                    if d is None: continue
                    nx, ny = ex + DIRV[d][0], ey + DIRV[d][1]
                    if (nx, ny) == p or (nx, ny) in z['ropes']: continue
                    if not mv.get((ex, ey, d)) or (nx, ny) in occ: continue
                    occ.discard((ex, ey)); occ.add((nx, ny)); pos[n] = (nx, ny)
                    break
            heavy = [n for n, _, _ in z['purs'] + z['blds']]
            if z['auto'] and z['plates'] and self.held(z['plates'], heavy, pos):
                sw.add(z['sw'])
            if z['sw'] not in sw and p not in z['ropes']:
                if any(abs(pos[n][0] - p[0]) + abs(pos[n][1] - p[1]) <= 1 for n, _, _ in z['purs']):
                    for n, _, _ in z['purs'] + z['blds']: pos[n] = self.start_of[n]
                    p = z['reset']
        return p, frozenset(sw)

    def start_state(self, p0, sw0=()):
        names = self.purs + self.blds
        return (p0, tuple(self.start_of[n] for n in names), frozenset(sw0))

    def moves(self, st):
        p, poss, sw = st
        names = self.purs + self.blds
        pl, mv = self.tables(sw)
        occ = set(poss)
        for d, (dx, dy) in DIRV.items():
            n = (p[0] + dx, p[1] + dy)
            if pl.get((p[0], p[1], d)) and n not in occ:
                pos = dict(zip(names, poss))
                p2, sw2 = self.step_hook(n, pos, sw)
                yield d, (p2, tuple(pos[k] for k in names), sw2)
            elif n in occ:                                    # facing a boulder: push it
                k = poss.index(n); name = names[k]
                if name not in self.push: continue
                rule = self.push[name]; r = (n[0] + dx, n[1] + dy)
                if r in rule['ropes'] or r in rule['blocked'] or r == p or r in occ: continue
                if not mv.get((n[0], n[1], d)): continue
                pos = dict(zip(names, poss)); pos[name] = r
                sw2 = set(sw)
                if rule['auto']:
                    z = self.zones[self.zone_of[name]]
                    if self.held(z['plates'], [m for m, _, _ in z['purs'] + z['blds']], pos): sw2.add(rule['auto'])
                yield d.lower(), (p, tuple(pos[k] for k in names), frozenset(sw2))
        for name, at, s, heavy in self.bells:                 # ring a bell you're facing (no step: the partners stay put)
            if s in sw: continue
            for d, (dx, dy) in DIRV.items():
                if (p[0] + dx, p[1] + dy) != at: continue
                if heavy:
                    z = next(z for z in self.zones if z['sw'] == s)
                    if not self.held(z['plates'], heavy, dict(zip(names, poss))): continue
                yield d.lower(), (p, poss, frozenset(set(sw) | {s}))
        for name, at, objs, tgt in self.resets:               # Hiro / a reset bell
            for d, (dx, dy) in DIRV.items():
                if (p[0] + dx, p[1] + dy) != at: continue
                pos = dict(zip(names, poss))
                for o in objs: pos[o] = self.start_of[o]
                yield 'reset', (tgt, tuple(pos[k] for k in names), sw)


def search(room, start, goal_sw, cap=CAP):
    dist = {start: 0}; prev = {start: None}; q = deque([start]); edges = {}; found = None
    while q:
        s = q.popleft()
        if goal_sw in s[2]:                                   # solved: the room's story ends here
            if found is None: found = s
            edges[s] = []; continue
        lst = []
        for a, t in room.moves(s):
            lst.append(t)
            if t not in dist:
                if len(dist) >= cap: return None, dist, prev, edges, True
                dist[t] = dist[s] + 1; prev[t] = (s, a); q.append(t)
        edges[s] = lst
    return found, dist, prev, edges, False


def solve_guided(room, start, goal_sw, cap=1500000, w=4):
    """weighted best-first search over the exact states (for rooms too big to enumerate): h = pushes still owed
    (each unheld plate: its nearest boulder's distance) + the player's distance to the nearest boulder. Returns
    the action string or None. The route is then replayed through the same rules (replay), which is the proof."""
    import heapq
    names = room.purs + room.blds
    z = next(z for z in room.zones if z['sw'] == goal_sw or any(s == goal_sw for _, _, s, _ in room.bells))
    bl = [names.index(n) for n, _, _ in z['blds']]
    bell = next((at for _, at, s, _ in room.bells if s == goal_sw), None)
    def h(st):
        p, poss, _ = st
        owe = 0
        for pl in z['plates']:
            if any(poss[i] == pl for i in range(len(names))): continue
            owe += min(abs(poss[i][0] - pl[0]) + abs(poss[i][1] - pl[1]) for i in bl) if bl else 0
        near = min((abs(poss[i][0] - p[0]) + abs(poss[i][1] - p[1]) for i in bl), default=0)
        tail = abs(bell[0] - p[0]) + abs(bell[1] - p[1]) if bell and owe == 0 else 0
        return owe * 6 + near + tail
    g = {start: 0}; prev = {start: None}; heap = [(w * h(start), 0, start)]; n = 0
    while heap:
        _, gs, s = heapq.heappop(heap)
        if gs > g[s]: continue
        if goal_sw in s[2]: return route(prev, s), n
        n += 1
        if n > cap: return None, n
        for a, t in room.moves(s):
            if a == 'reset': continue
            if t not in g or gs + 1 < g[t]:
                g[t] = gs + 1; prev[t] = (s, a); heapq.heappush(heap, (gs + 1 + w * h(t), gs + 1, t))
    return None, n


def replay(room, start, sw0, actions):
    """walk an action string through the engine's rules; -> the final state"""
    st = room.start_state(start, sw0)
    for a in actions:
        nxt = dict(room.moves(st))
        if a not in nxt: return None
        st = nxt[a]
    return st


def boulder_traps(room, start, sw0, goal_sw, cap=CAP):
    """soft-lock check for boulder rooms, exhaustive over every boulder arrangement the player can make (partners
    left out: they only restrict where you walk, and a partner that reaches you tags you, which is a reset).
    A pocket you can stand in is SAFE when it touches a reset (Hiro, a reset bell), a door out (leaving the map puts
    every boulder back: Essentials forgets moved events) or the solved room.  -> (arrangements, pockets that are not
    safe but lie in a live partner zone (a tag can still free you there; listed, not failed), bad pockets)"""
    import numpy as np
    from scipy import ndimage
    names = room.purs + room.blds
    gz = next(z for z in room.zones if z['sw'] == goal_sw or any(s == goal_sw for _, _, s, _ in room.bells))
    bl = [names.index(n) for n, _, _ in gz['blds']]        # the goal zone's boulders; another zone's stay put
    if not bl: return 0, [], []
    sw = frozenset(sw0)
    pl, mv = room.tables(sw)
    W, H = room.W, room.H
    walk = np.zeros((H, W), bool)
    for (x, y, d), ok in pl.items():
        if ok: walk[y, x] = True; walk[y + DIRV[d][1], x + DIRV[d][0]] = True
    asym = [(x, y, d) for (x, y, d), ok in pl.items() if ok and not pl.get((x + DIRV[d][0], y + DIRV[d][1], {'U': 'D', 'D': 'U', 'L': 'R', 'R': 'L'}[d]))]
    safe = np.zeros((H, W), bool)
    for _, at, _, _ in room.resets:
        for dx, dy in DIRV.values():
            if 0 <= at[0] - dx < W and 0 <= at[1] - dy < H: safe[at[1] - dy, at[0] - dx] = True
    for (m, x, y), es in room.b.ev.items():                 # a door out
        if any(c.code == 201 or (c.code == 355 and 'player_new_map_id' in str(c.parameters[0])) for e in es for pg in e.pages for c in pg.list):
            for dx, dy in list(DIRV.values()) + [(0, 0)]:
                if 0 <= x - dx < W and 0 <= y - dy < H: safe[y - dy, x - dx] = True
    x0, x1, y0, y1 = gz['box']
    zone = np.zeros((H, W), bool); zone[y0:y1 + 1, x0:x1 + 1] = True
    s4 = ndimage.generate_binary_structure(2, 1)
    s0 = room.start_state(start, sw0)
    pos0 = dict(zip(names, s0[1]))
    heavy = [m for m, _, _ in gz['purs'] + gz['blds']]
    def labels(bs):
        g = walk.copy()
        for b in bs: g[b[1], b[0]] = False
        return ndimage.label(g, structure=s4)[0]
    start_bs = tuple(s0[1][i] for i in bl)
    lab = labels(start_bs)
    seen = {(start_bs, lab[start[1], start[0]])}; q = [(start_bs, start)]; in_zone = []; bad = []
    while q:
        bs, p = q.pop()
        lab = labels(bs); comp = lab[p[1], p[0]]
        mask = lab == comp
        pos = dict(pos0)
        for i, b in zip(bl, bs): pos[names[i]] = b
        if not (mask & safe).any() and not (gz['plates'] and room.held(gz['plates'], heavy, pos)):
            (in_zone if (mask & zone).any() else bad).append((bs, p))
        for k, i in enumerate(bl):
            b = bs[k]; rule = room.push[names[i]]
            for d, (dx, dy) in DIRV.items():
                c = (b[0] - dx, b[1] - dy); r = (b[0] + dx, b[1] + dy)
                if not (0 <= c[0] < W and 0 <= c[1] < H) or not mask[c[1], c[0]]: continue
                if r in rule['ropes'] or r in rule['blocked'] or r in bs or not mv.get((b[0], b[1], d)): continue
                nb = list(bs); nb[k] = r; nb = tuple(nb)
                key = (nb, ('at', c))
                if key in seen: continue
                seen.add(key)
                if len(seen) >= cap: return len(seen), in_zone, bad + ['capped']
                q.append((nb, c))
    if asym: bad = bad  # directional edges exist: the labels treat them as two-way (noted by the caller)
    return len(seen), in_zone, bad


def proof_big(mid, start, goal_sw, label, sw0=(), trap_cap=CAP):
    try:
        room = Room(mid)
    except FileNotFoundError as e:
        return True, ['skip Gym 8 %d %s: %s' % (mid, label, e)]
    name = 'Gym 8 %d %s [built map]' % (mid, label)
    r, n = solve_guided(room, room.start_state(start, sw0), goal_sw)
    if r is None:
        return False, ['FAIL %s: no solution found (%d states expanded)' % (name, n)]
    end = replay(room, start, sw0, r)
    ok = end is not None and goal_sw in end[2]
    SOLUTIONS[(mid, label)] = r
    out = ['%s %s: solved, %d actions (%d steps, %d pushes/uses), replayed through the engine rules from the door: %s' % (
        'ok  ' if ok else 'FAIL', name, len(r), sum(c in 'UDLR' for c in r), sum(c in 'udlr' for c in r), r)]
    states, in_zone, bad = boulder_traps(room, start, sw0, goal_sw, cap=trap_cap)
    capped = 'capped' in bad
    bad = [x for x in bad if x != 'capped']
    if capped and not bad:
        out.append('  bounded: the first %d boulder arrangements (of more) leave no pocket outside the partner zone cut off from a reset or a door; NOT exhaustive' % states)
    elif bad:
        ok = False; out.append('FAIL %s: %d boulder arrangements strand you away from every reset and door, e.g. %r' % (name, len(bad), bad[0]))
    else:
        out.append('  proved: over all %d reachable boulder arrangements, no pocket outside the partner zone is cut off from a reset or a door' % states)
    if in_zone:
        out.append('  note: %d pockets inside the partner zone have no reset or door; there a partner that reaches you tags you (a reset), e.g. %r' % (len(in_zone), in_zone[0]))
    return ok, out


def route(prev, s):
    out = []
    while prev[s]: s, a = prev[s][0], (prev[s][1], s); out.append(a[0])
    return ''.join('X' if a == 'reset' else a for a in reversed(out))


def proof(mid, start, goal_sw, label, sw0=(), extra_ok=(), only_zone=False):
    """-> (ok, lines). extra_ok: switches whose states also count as safe (another goal of the same room).
    only_zone: an optional room inside a room (273's Marrowgate): the other zones count as solved (sw0) and their
    boulders as fixed, so the search is the alcove's own"""
    try:
        room = Room(mid)
    except FileNotFoundError as e:
        return True, ['skip Gym 8 %d %s: %s' % (mid, label, e)]
    if only_zone:
        gz = next(z for z in room.zones if z['sw'] == goal_sw)
        room.push = {n: r for n, r in room.push.items() if n in {m for m, _, _ in gz['blds']}}
    s0 = room.start_state(start, sw0)
    found, dist, prev, edges, capped = search(room, s0, goal_sw)
    name = 'Gym 8 %d %s [built map]' % (mid, label)
    if capped:
        return False, ['FAIL %s: more than %d states; not proved' % (name, CAP)]
    if found is None:
        return False, ['FAIL %s: S%d cannot be reached from %r (%d states)' % (name, goal_sw, start, len(dist))]
    r = route(prev, found)
    SOLUTIONS[(mid, label)] = r
    good = {s for s in dist if goal_sw in s[2] or any(x in s[2] for x in extra_ok)}
    rev = {}
    for s, ns in edges.items():
        for n in ns: rev.setdefault(n, []).append(s)
    st = list(good)
    while st:
        s = st.pop()
        for p in rev.get(s, []):
            if p not in good: good.add(p); st.append(p)
    dead = [s for s in dist if s not in good]
    ok = not dead
    out = ['%s %s: %d reachable states, shortest %d actions (%d steps, %d pushes/uses): %s' % (
        'ok  ' if ok else 'FAIL', name, len(dist), len(r), sum(c in 'UDLR' for c in r), sum(c in 'udlr' for c in r), r)]
    if dead:
        out.append('FAIL %s: %d soft-locked states, e.g. you at %r, partners/boulders %r' % (name, len(dead), dead[0][0], dead[0][1]))
    else:
        out.append('  proved: every reachable state can still reach S%d (no soft-lock)' % goal_sw)
    return ok, out


def _arrive(mid):
    """the door you come in by: the previous room's warp target"""
    import yaml
    prev = {271: '270_ironreach_gym_270.yaml', 272: '271_ironreach_gym_271.yaml', 273: '272_ironreach_gym_272.yaml'}[mid]
    for d in yaml.safe_load_all(open(os.path.join(HERE, 'specs', prev))):
        if not d: continue
        for e in d.get('events') or []:
            t = e.get('to') or {}
            if t.get('map') == mid: return (t['x'], t['y'])


def p271w(): return proof(271, _arrive(271), 344, 'west (the pillar)')
def p271e(): return proof(271, _arrive(271), 340, 'east (the rope lines)', sw0=(344,))
def p272(): return proof_big(272, _arrive(272), 341, 'boulders and plates')
def p273(): return proof_big(273, _arrive(273), 342, 'the gauntlet', trap_cap=1000000)   # 3 boulders: > 12M; bounded
def p273m(): return proof(273, _arrive(273), 343, 'Marrowgate (mastery)', sw0=(342,), only_zone=True)


from .proofcache import cached
EXTRA = [lambda f=f, m=m: cached('gym8_' + f.__name__, __file__, m, f)
         for f, m in ((p271w, [270, 271]), (p271e, [270, 271]), (p272, [271, 272]), (p273, [272, 273]), (p273m, [272, 273]))]

if __name__ == '__main__':
    import sys, time
    for fn in ([p271w, p271e, p272, p273, p273m] if len(sys.argv) < 2 else [globals()[a] for a in sys.argv[1:]]):
        t = time.time(); ok, lines = fn()
        for l in lines: print(l)
        print('  (%.1fs)' % (time.time() - t))
