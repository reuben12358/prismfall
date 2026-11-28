"""Gym 9, the Heartgarden Gym (Verdance; Juno Hale, Grass, :FLOWER_GARDEN, cap 47): GYM_PUZZLES "Gym 9", built by
Gemini (mapgen/layouts/verdance_gym.py, maps 290-293).  One rule: WATER SPREADS.  A spigot waters its plot and the
plot's neighbours, each one stage on, mod 4: 0 bare bed, 1 sprouts, 2 vine bridge (walkable over the canal),
3 rose hedge (solid).  Every hedge left in 291 / 292 raises Juno's Flower Garden one stage (V345; field stage
1 + min(V345, 4)), so the cheap route is also the hard fight.
  290 Gate Hall      TEACH: P0 (+ its neighbour P0N): one watering makes the bridge
  291 Hedge Garden   TWIST "the ring of six": P1, P3, P5 must be bridges (S345)
  292 Glasshouse     COMBINE "two rings, one heart": J, A2, A3, B2, B3 must be bridges (S346)
  292 Bride Bower    MASTERY (optional): M1..M5 = 2, 3, 2, 3, 2 (S347)

Engine-level and exhaustive: the rooms are read from the BUILT maps (maps_out/Data): each spigot's own script
(its plot list, start stages, the plots it waters, the room's done test), each plot event's four pages (the tile
its stage shows, so a bridge is walkable exactly when the engine says so), walkability from puzzles/built.Built.
A move is one watering (walking is free; core.Model); a spigot refuses while you stand on a plot it would change,
as the script does.  verify() proves: the exit (or the mastery's switch) is reachable from the door in the design's
minimum number of waterings, and no reachable state is a soft-lock (Bram's / the valve's reset counts)."""
import ast, os, re
from .core import Model, Device, verify, DIRS

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOMS = {}
CHECKS = []
BIT = {(0, 1): 1, (-1, 0): 2, (1, 0): 4, (0, -1): 8}


def _script(ev, page=0):
    out = []; lst = ev.pages[page].list; i = 0
    while i < len(lst):
        if lst[i].code == 355:
            s = [lst[i].parameters[0]]; i += 1
            while i < len(lst) and lst[i].code == 655: s.append(lst[i].parameters[0]); i += 1
            out.append('\n'.join(s)); continue
        i += 1
    return '\n'.join(out)


def _arrive(mid, frm):
    import yaml
    files = {283: '283_verdance_glasshouse_ward.yaml', 290: '290_verdance_gym.yaml', 291: '291_verdance_gym_291.yaml'}
    for d in yaml.safe_load_all(open(os.path.join(HERE, 'specs', files[frm]))):
        for e in (d or {}).get('events') or []:
            t = e.get('to') or {}
            if t.get('map') == mid: return (t['x'], t['y'])


def room_model(mid, group, start, goal, minimum, fixed=None, fixed_other=None):
    """group: the spigots whose plot list this proof covers (a prefix of plot ids, e.g. 'M' for the Bower);
    goal: ('exit', (x, y)) or ('done', switch). fixed: other plots' stages held as given (k offsets)"""
    from .built import Built
    b = Built([mid]); m = b.maps[mid]; ts = b.ts[mid]
    spig = []
    for e in m.events.values():
        s = _script(e)
        t = re.search(r"targets = (\[.*?\])", s); p = re.search(r"plots = (\[.*?\]\n\])", s, re.S)
        if not (t and p): continue
        plots = ast.literal_eval(p.group(1).replace('\n', ''))
        if not group(plots[0][0]) and not any(group(pid) for pid, _, _ in plots): continue
        done = re.search(r"(?:done|ok) = \((.*?)\)\n", s)
        sw = re.search(r"\$game_switches\[(\d+)\] = (?:done|true if ok)", s)
        spig.append((e.name, (e.x, e.y), plots, ast.literal_eval(t.group(1)),
                     done.group(1) if done else None, int(sw.group(1)) if sw else None))
    plots = spig[0][2]
    ids = [pid for pid, _, _ in plots]
    s0 = {pid: st for pid, st, _ in plots}
    evname = {n: pid for pid, _, evs in plots for n in evs}
    plot_ev = {}
    for e in m.events.values():
        if e.name in evname:
            plot_ev[(mid, e.x, e.y)] = (evname[e.name], [pg.graphic.tile_id for pg in e.pages])
    for key in list(b.ev):                                  # the plots are drawn by the search, not the map
        b.ev[key] = [e for e in b.ev[key] if e.name not in evname]
    plot_static = {}
    if fixed_other:                                         # another puzzle's plots, held at a given state (as tiles)
        for e in m.events.values():
            for pid, k in fixed_other.items():
                if re.match(r'^%s_[LR]$' % pid, e.name):
                    b.ev[(mid, e.x, e.y)] = [x for x in b.ev.get((mid, e.x, e.y), []) if x is not e]
                    g = e.pages[k].graphic.tile_id
                    plot_static[(mid, e.x, e.y)] = g
    done_expr = spig[0][4]; done_sw = spig[0][5]
    cells = {(mid, x, y) for y in range(m.height) for x in range(m.width)}

    def stage(v, pid): return (s0[pid] + v[ids.index(pid)]) % 4

    def tile_ok(cell, v, bit=None):
        pid, tiles = plot_ev[cell]
        g = tiles[v[ids.index(pid)]]
        p = ts['passages'][g]
        if bit is None: return not (p & 0x0f == 0x0f)
        return not (p & bit or p & 0x0f == 0x0f)

    def tile_pass(g, bit=None):
        p = ts['passages'][g]
        return not (p & 0x0f == 0x0f) if bit is None else not (p & bit or p & 0x0f == 0x0f)
    static_pass = {c: (tile_pass(plot_static[c]) if c in plot_static else b.passable(c, {}, {})) for c in cells if c not in plot_ev}     # the map without the plots, once
    static_dir = {(c, bit): (tile_pass(plot_static[c], bit) if c in plot_static else b.dir_ok(c, bit, {}, {}))
                  for c in cells if c not in plot_ev for bit in (1, 2, 4, 8)}

    def passable(c, v):
        if c in plot_ev: return tile_ok(c, v)
        return static_pass.get(c, False)

    def move_ok(c, n, v):
        d = (n[1] - c[1], n[2] - c[2])
        if d not in BIT: return True
        out_bit, in_bit = BIT[d], BIT[(-d[0], -d[1])]
        a = tile_ok(c, v, out_bit) if c in plot_ev else static_dir[(c, out_bit)]
        z = tile_ok(n, v, in_bit) if n in plot_ev else static_dir.get((n, in_bit), False)
        return a and z

    devs = []
    for name, (x, y), _, targets, _, _ in spig:
        on = {c for c, (pid, _) in plot_ev.items() if pid in targets}
        def act(v, c, targets=targets, on=on):
            if c in on: return None                          # "Step off the vine bridge onto dry stone before watering!"
            v2 = list(v)
            for t in targets: v2[ids.index(t)] = (v2[ids.index(t)] + 1) % 4
            return tuple(v2), c
        devs.append(Device(name, [(mid, x + dx, y + dy) for dx, dy in DIRS], act, label=name.replace('Spigot ', 'water ')))
    v0 = tuple((fixed or {}).get(pid, 0) for pid in ids)
    resets = []
    for e in m.events.values():                             # Bram / the Bower's valve: "Reset all ... beds"
        if e.name.startswith('Apprentice Bram') or 'Reset' in e.name:
            resets += [(mid, e.x + dx, e.y + dy) for dx, dy in DIRS]
    if goal[0] == 'exit':
        goal_cells = [(mid,) + goal[1]]
        model = Model('Gym 9 %d [built map]' % mid, cells, passable, (mid,) + start, v0, devs, goal_cells, resets=resets)
    else:
        expr = re.sub(r'cur\["(\w+)"\]', r"stg('\1')", done_expr).replace('&&', ' and ')
        ok_states = '__done__'
        model = DoneModel('Gym 9 %d Bride Bower [built map]' % mid, cells, passable, (mid,) + start, v0, devs, [], resets=resets)
        model.done = lambda v, expr=expr: eval(expr, {'stg': lambda pid: stage(v, pid)})
    model.move_ok = move_ok
    model.stage = stage; model.ids = ids
    model.fast = dict(W=m.width, H=m.height, static_pass=static_pass, plot_ev=plot_ev, tile_ok=tile_ok, mid=mid,
                      asym=sum(1 for (c, bit), ok in static_dir.items() if ok and c in static_pass and static_pass[c]
                               and not static_dir.get((((c[0], c[1] + {1: 0, 2: -1, 4: 1, 8: 0}[bit], c[2] + {1: 1, 2: 0, 4: 0, 8: -1}[bit])),
                                                       {1: 8, 2: 4, 4: 2, 8: 1}[bit]), True)))
    return model


def fast_verify(model, moves=None, rating=None):
    """verify() for a plot room, with the walking regions labelled by scipy (one label pass per plot state instead of a
    flood per state and device): the same proof, minutes faster on the Glasshouse's 4^9 plot states."""
    import numpy as np
    from scipy import ndimage
    from collections import deque
    from .core import rating_check
    F = model.fast; W, H, mid = F['W'], F['H'], F['mid']
    base = np.zeros((H, W), bool)
    for (m_, x, y), ok in F['static_pass'].items():
        if ok: base[y, x] = True
    plots = list(F['plot_ev'])
    s4 = ndimage.generate_binary_structure(2, 1)
    cache = {}
    def labels(v):
        if v in cache: return cache[v]
        g = base.copy()
        for c in plots: g[c[2], c[1]] = F['tile_ok'](c, v)
        lab = ndimage.label(g, structure=s4)[0]
        if len(cache) > 4000: cache.clear()
        cache[v] = lab
        return lab
    goal_cells = [c for c in model.goal if isinstance(c, tuple)] if not hasattr(model, 'done') else []
    def is_goal(v, lab, comp):
        if hasattr(model, 'done'): return model.done(v)
        return any(lab[c[2], c[1]] == comp for c in goal_cells)
    def rep(lab, comp):
        return int(np.flatnonzero(lab.ravel() == comp)[0])
    start = model.start
    lab0 = labels(model.vars0); c0 = lab0[start[2], start[1]]
    k0 = (model.vars0, rep(lab0, c0))
    dist = {k0: 0}; prev = {k0: None}; q = deque([k0]); edges = {}; goals = []
    reset_cells = [c for c in model.resets]
    while q:
        k = q.popleft(); v, r = k
        lab = labels(v); comp = lab.ravel()[r]
        if is_goal(v, lab, comp): goals.append(k); edges[k] = []; continue
        out = []
        for d in model.devices:
            stands = [c for c in d.stand if 0 <= c[1] < W and 0 <= c[2] < H and lab[c[2], c[1]] == comp]
            res = {}
            for c in stands:
                rr = d.act(v, c)
                if rr is not None: res.setdefault(rr[0], []).append(c)
            for v2, cs in res.items():
                lab2 = labels(v2)
                for c in cs:
                    comp2 = lab2[c[2], c[1]]
                    if comp2 == 0: continue                        # a hedge grew under you (refused by the script)
                    k2 = (v2, rep(lab2, comp2))
                    out.append(k2)
                    if k2 not in dist: dist[k2] = dist[k] + 1; prev[k2] = (k, d.label); q.append(k2)
        if any(lab[c[2], c[1]] == comp for c in reset_cells if 0 <= c[1] < W and 0 <= c[2] < H):
            out.append(k0)
        edges[k] = out
    name = model.name
    if not goals: return False, ['FAIL %s: the goal cannot be reached (%d states)' % (name, len(dist))]
    best = min(goals, key=lambda k: dist[k]); path = []; k = best
    while prev[k]: path.append(prev[k][1]); k = prev[k][0]
    path = path[::-1]; ok = True; out = []
    if moves is not None and len(path) != moves:
        ok = False; out.append('FAIL %s: shortest solution is %d waterings, the design says %d' % (name, len(path), moves))
    good = set(goals); rev = {}
    for k, ns in edges.items():
        for n in ns: rev.setdefault(n, []).append(k)
    st = list(good)
    while st:
        k = st.pop()
        for p in rev.get(k, []):
            if p not in good: good.add(p); st.append(p)
    dead = [k for k in dist if k not in good]
    if dead:
        ok = False; out.append('FAIL %s: %d of %d reachable states are soft-locks, e.g. plots %r' % (name, len(dead), len(dist), dead[0][0]))
    if rating is not None:
        kk, line = rating_check(name, rating, len(path), len(dist)); ok &= kk; out.append(line)
    if F['asym']:
        # the labels read the map's one-way edges as two-way: walk the solution again with the exact, directional
        # regions (core.Model.region, Game_Map#passable? both ways) so the route itself is proved on the real map
        v, cell = model.vars0, model.start
        for lab_ in path:
            d = next(x for x in model.devices if x.label == lab_)
            reg = model.region(cell, v)
            step = next((d.act(v, c) for c in d.stand if c in reg and d.act(v, c) is not None), None)
            if step is None:
                ok = False; out.append('FAIL %s: %s cannot be used on the directional map' % (name, lab_)); break
            v, cell = step
        else:
            reach = model.region(cell, v)
            fin = model.done(v) if hasattr(model, 'done') else bool(reach & set(goal_cells))
            if not fin: ok = False; out.append('FAIL %s: the route does not end at the goal on the directional map' % name)
            else: out.append('  the route replayed with directional walking: every spigot reached, the goal reached')
        out.append('  note: %d one-way edges (bank and rail tiles) are two-way in the soft-lock search' % F['asym'])
    out.insert(0, '%s %s: %d reachable states, shortest solution %d waterings: %s' % ('ok  ' if ok else 'FAIL', name, len(dist), len(path), ' > '.join(path)))
    return ok, out


class DoneModel(Model):
    """the goal is a state of the plots (the Bower's 2, 3, 2, 3, 2), wherever you stand"""
    def explore(self, skip=()):
        dist, prev, regs, edges, emb = Model.explore(self, skip)
        g = object()
        for k, r in regs.items():
            if self.done(k[1]): regs[k] = r | {g}
        self.goal = {g}
        return dist, prev, regs, edges, emb


def p290(): return verify(room_model(290, lambda pid: pid.startswith('P0'), _arrive(290, 283), ('exit', (10, 4)), 1), moves=1, rating=2)
def p291(): return verify(room_model(291, lambda pid: pid[0] == 'P', _arrive(291, 290), ('exit', (14, 4)), 2), moves=2, rating=4)
def p292(): return fast_verify(room_model(292, lambda pid: pid[0] in 'JAB', _arrive(292, 291), ('exit', (14, 4)), 7), moves=7)   # 4^9 states: 9/10 by the SPINE budget
def p292m():
    # the Bower lies past the figure-eight: its proof starts from the door with the eight solved (the 7-watering route)
    main = room_model(292, lambda pid: pid[0] in 'JAB', _arrive(292, 291), ('exit', (14, 4)), 7)
    sol = {'J': 0, 'A1': 2, 'A2': 0, 'A3': 1, 'A4': 0, 'B1': 1, 'B2': 0, 'B3': 1, 'B4': 2}   # GYM_PUZZLES' 7 waterings
    v = [0] * len(main.ids)
    for pid, n in sol.items():
        for _ in range(n):
            for t in next(d for d in main.devices if d.name == 'Spigot ' + pid).act.__defaults__[0]:
                v[main.ids.index(t)] = (v[main.ids.index(t)] + 1) % 4
    return fast_verify(room_model(292, lambda pid: pid[0] == 'M', _arrive(292, 291), ('done', 347), 6,
                                  fixed_other=dict(zip(main.ids, v))), moves=6, rating=4)


from .proofcache import cached
EXTRA = [lambda f=f, m=m: cached('gym9_' + f.__name__, __file__, m, f)
         for f, m in ((p290, [283, 290]), (p291, [290, 291]), (p292, [291, 292]), (p292m, [291, 292]))]

if __name__ == '__main__':
    for fn in (p290, p291, p292, p292m):
        ok, lines = fn()
        for l in lines: print(l)
