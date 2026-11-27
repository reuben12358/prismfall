"""mapgen/reach.py - post-paint reachability on the BUILT maps (build.py calls check() after the other checks).

Two warnings, both read maps_out/Data/MapNNN.rxdata exactly as Essentials v21.1 does:

STANDON  an action-button page that Essentials treats as "over_trigger" (Game_Event#over_trigger?: no charset, or
         Through, and Game_Map#passable?(x, y, 0) on its tile, its own tile graphic included) runs ONLY when the player
         stands on the event and presses USE (Game_Player#check_event_trigger_here([0])); check_event_trigger_there
         skips it, so facing it from the next tile does nothing (Gym 7's cracked mould, 2026-11-26).  Warned when such a
         page SHOWS something (a tile graphic, or a Through charset): the player sees an object and faces it.  An
         invisible one is fine if its tile can be walked onto; REACH says when it can't.  Fix: a solid tile
         (passage 0x0f) for the graphic, or a non-Through charset, or move the event onto the solid object.

REACH    every warp, door and action-button event must be reachable from the map's arrival points: Transfer Player
         targets from every built map (and literal `$game_temp.player_new_*` / `$game_player.moveto` scripts),
         HealingSpot / fly spots, connected map edges and the spec's `walk_from`.  Same-map warps and movetos open
         their target once their source is reached.  The flood fill is a SUPERSET of what the player can reach in
         any story state: each event counts as whichever of its pages lets the player through (an event whose pages
         are all conditional, that erases itself, moves or is moved also counts as absent), Surf and waterfalls are
         allowed, bridge tiles pass on and off the bridge, ledges jump two tiles (Game_Player#move_generic).  So an
         event it can't reach can't be reached at all, unless the map moves the player in ways the fill can't see
         (scripted relocations it can't parse, Through/jump routes on the player, tile edits, puzzle rooms).  Those
         maps are "approximate": their REACH lines are warnings only.  On the others ("exact") `--strict` fails.
         A target is reached when the player can stand where Essentials triggers it: on its tile if its page is
         over_trigger, else on a 4-neighbour (or across a counter tile, Game_Player#check_event_trigger_there).
         Trainers (they walk to you) and events that move are not targets; a spec's `reach_ignore: [regex, ...]`
         names events that are meant to be out of reach (scenery NPCs behind a rope).

    python3 -I mapgen/reach.py [ids]      # the same check on maps_out as it stands, without a build"""
import os, re, itertools
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), 'maps_out')
NONE, SOLID = 'none', 'solid'
BIT = {(0, 1): 1, (-1, 0): 2, (1, 0): 4, (0, -1): 8}          # Essentials' passage bits: down, left, right, up
DIRS = ((0, 1), (0, -1), (1, 0), (-1, 0))
WATER = (5, 6, 7, 8, 9)                                         # DeepWater, StillWater, Water, Waterfall, WaterfallCrest
MOVE_CODES = set(range(1, 15))                                   # RPG::MoveCommand 1-14: steps, random, toward, jump
TRAINER = re.compile(r'(?:sight|trainer)\(\d+\)', re.I)
# scripts that can put the player somewhere the flood fill can't follow, or change tiles (Prismfall Puzzles 001-008:
# forced lines, web throws, turntables, saved positions, a solve skip; raw tile writes; jumps; Through on the player)
DYNAMIC = re.compile(r'pfp_(?:turntable_ride|push_line|web|solve|load|restore!)\b|PrismfallPuzzles\.(?:push_line|web_throw|'
                     r'turntable_ride|solve|load_positions|restore!)|\$game_player\.through\s*=|\$game_map\.data|set_tile|'
                     r'jumpForward|jumpBackward|\.jump\(|\$game_player\.moveto\((?!\s*\d+\s*,\s*\d+\s*\))|'
                     r'(?<!\$game_player)\.moveto\(|pfp_ride\((?!\s*\d+\s*,\s*\d+\s*\))')
# scripts on an event that make it vanish, move or turn passable (so it may be out of the way)
REMOVES = re.compile(r'pbSmashEvent|pbEraseThisEvent|\berase\b|pbPushThisBoulder|pfp_push\b|pfp_slide|moveto|\.through\s*=|'
                     r'character_name\s*=|opacity\s*=|transparent\s*=')
# events moved by name from another event's script (blocks, pew pairs, followers, pursuers, resets)
MOVED_BY_NAME = re.compile(r'pfp_(?:slide|follow|pursue|push_pair)\(\s*[\'"]([^\'"]+)[\'"](?:\s*,\s*[\'"]([^\'"]+)[\'"])?|'
                           r'pfp_ev\(\s*[\'"]([^\'"]+)[\'"]\s*\)\.moveto')


def scripts(pg):
    """Every script string on a page: Script commands and Conditional Branch scripts."""
    out = []
    for c in pg.list:
        if c.code in (355, 655) and c.parameters: out.append(str(c.parameters[0]))
        elif c.code == 111 and c.parameters and c.parameters[0] == 12: out.append(str(c.parameters[1]))
    return '\n'.join(out)


def real_cmds(pg):
    return any(c.code not in (0, 108, 408) for c in pg.list)


def route_moves(route):
    return any(c.code in MOVE_CODES for c in route.list)


def has_cond(pg):
    c = pg.condition
    return c.switch1_valid or c.switch2_valid or c.variable_valid or c.self_switch_valid


def page_option(pg):
    if pg.through: return NONE
    g = pg.graphic
    if g.tile_id > 0: return ('tile', g.tile_id)
    if g.character_name: return SOLID
    return NONE


def is_door(ev):
    return any(c.code == 209 for p in ev.pages for c in p.list) and any(c.code == 201 for p in ev.pages for c in p.list) \
        and any('follow_into_door' in scripts(p) or 'onEvent?' in scripts(p) for p in ev.pages)


class MapView:
    """One built map: tiles, events and their possible states, as the flood fill sees them."""

    def __init__(self, mid, m, ts):
        self.mid, self.m, self.ts = mid, m, ts
        self.W, self.H, self.L = m.width, m.height, m.data.data
        self.tt, self.pas, self.pri = ts['terrain_tags'], ts['passages'], ts['priorities']
        self.dynamic = []                                       # why this map is approximate
        moved = set(); names = set()                            # events some route / 202 / script moves
        for ev in m.events.values():
            for pg in ev.pages:
                s = scripts(pg)
                for c in pg.list:
                    if c.code == 209:
                        who, route = c.parameters[0], c.parameters[1]
                        tgt = ev.id if who == 0 else who
                        if who == -1:
                            if not is_door(ev) and any(mc.code in (14, 37) for mc in route.list):
                                self.dynamic.append('"%s" moves the player Through / jumping' % ev.name)
                        elif route_moves(route) or any(mc.code in (37, 41, 42, 45) for mc in route.list):
                            moved.add(tgt)
                    elif c.code == 202:
                        moved.add(ev.id if c.parameters[0] == 0 else c.parameters[0])
                        self.dynamic.append('"%s" sets an event location' % ev.name)
                    elif c.code == 201 and c.parameters[0] != 0:
                        self.dynamic.append('"%s" transfers by variables' % ev.name)
                d = DYNAMIC.search(s)
                if d: self.dynamic.append('"%s" runs %s' % (ev.name, d.group(0)))
                for mm in MOVED_BY_NAME.finditer(s):
                    names.update(n for n in mm.groups() if n)
        moved |= {ev.id for ev in m.events.values() if ev.name in names}
        self.opts = {}; self.at = {}; self.mobile = set(); self._ok = {}
        for ev in m.events.values():
            o = {page_option(pg) for pg in ev.pages}
            if all(has_cond(pg) for pg in ev.pages): o.add(NONE)
            if ev.id in moved or any(pg.move_type != 0 for pg in ev.pages): o.add(NONE); self.mobile.add(ev.id)
            if any(c.code == 214 for pg in ev.pages for c in pg.list) or any(REMOVES.search(scripts(pg)) for pg in ev.pages):
                o.add(NONE)
            if any(pg.move_route and any(mc.code in (37, 41, 42, 45) for mc in pg.move_route.list) for pg in ev.pages):
                o.add(NONE)
            self.opts[ev.id] = o
            self.at.setdefault((ev.x, ev.y), []).append(ev)

    def valid(self, x, y):
        return 0 <= x < self.W and 0 <= y < self.H

    def tag(self, t):
        return self.tt[t] if t < len(self.tt) else 0

    def layers_ok(self, x, y, bit, bridge=False, surf=False):
        """Game_Map#playerPassable?(x, y, d): layers top down.  bridge: on a bridge (its tile decides); surf: surfing."""
        for z in (2, 1, 0):
            t = int(self.L[z, y, x])
            if t == 0: continue
            tg = self.tag(t); p = self.pas[t]
            if tg == 15:
                if not bridge: continue
                return p & bit == 0 and p & 0x0f != 0x0f
            if surf and tg in WATER: return True
            if tg == 13: continue
            if p & bit or p & 0x0f == 0x0f: return False
            if self.pri[t] == 0: return True
        return True

    def combos(self, x, y):
        evs = self.at.get((x, y), [])
        if not evs: return [()]
        return list(itertools.product(*[sorted(self.opts[e.id], key=str) for e in evs]))

    def tile_ok(self, combo, x, y, bit, surf=False):
        """Game_Map#passable?(x, y, d, $game_player) for one choice of event states."""
        for o in combo:
            if isinstance(o, tuple):
                t = o[1]
                if self.tag(t) == 13: continue
                p = self.pas[t]
                if p & bit or p & 0x0f == 0x0f: return False
                if self.pri[t] == 0: return True
        return self.layers_ok(x, y, bit, surf=surf) or self.layers_ok(x, y, bit, bridge=True, surf=surf)

    def ok(self, x, y, bit, enter, surf=False):
        """Some event state lets the player leave (enter=False) or enter (enter=True) the tile through `bit`."""
        k = (x, y, bit, enter, surf)
        r = self._ok.get(k)
        if r is None:
            r = False
            if self.valid(x, y):
                for combo in self.combos(x, y):
                    if enter and SOLID in combo: continue
                    if self.tile_ok(combo, x, y, bit, surf): r = True; break
            self._ok[k] = r
        return r

    def water(self, x, y):
        for z in (2, 1, 0):
            t = int(self.L[z, y, x])
            if t == 0: continue
            tg = self.tag(t)
            if tg in (0, 13) or tg == 15: continue
            return tg in WATER
        return False

    def ledge(self, x, y):
        for z in (2, 1, 0):
            t = int(self.L[z, y, x])
            if t == 0: continue
            tg = self.tag(t)
            if tg in (0, 13, 15): continue
            return tg == 1
        return False

    def counter(self, x, y):
        return self.valid(x, y) and any(int(self.L[z, y, x]) and self.pas[int(self.L[z, y, x])] & 0x80 for z in (2, 1, 0))

    def steps(self, x, y):
        """Cells one move away (a ledge jump lands two away); surfing included."""
        for dx, dy in DIRS:
            nx, ny = x + dx, y + dy
            if not self.valid(nx, ny): continue
            b, ob = BIT[(dx, dy)], BIT[(-dx, -dy)]
            foot = self.ok(x, y, b, False) and self.ok(nx, ny, ob, True)
            if foot and self.ledge(nx, ny):
                lx, ly = x + 2 * dx, y + 2 * dy
                if self.ok(lx, ly, 0, True): yield (lx, ly)
                continue
            if foot:
                yield (nx, ny); continue
            if self.water(nx, ny) and self.ok(nx, ny, ob, True, surf=True) and \
                    (not self.water(x, y) or self.ok(x, y, b, False, surf=True)):
                yield (nx, ny); continue
            if self.water(x, y) and self.ok(nx, ny, ob, True): yield (nx, ny)

    def over_trigger(self, ev, pg):
        """Game_Event#over_trigger? for this page (its own tile graphic counts; other events at the tile don't)."""
        g = pg.graphic
        if g.character_name and not pg.through: return False
        if re.search(r'hiddenitem', ev.name or '', re.I): return False
        if g.tile_id > 0 and not pg.through and self.tag(g.tile_id) != 13:
            p = self.pas[g.tile_id]
            if p & 0x0f == 0x0f: return False
            if self.pri[g.tile_id] == 0: return True
        return self.layers_ok(ev.x, ev.y, 0)


def transfers(m):
    """(event, page, map or None for this map, x, y) for every Transfer Player and literal scripted transfer, moveto
    and pfp_ride on a built map."""
    for ev in m.events.values():
        for pg in ev.pages:
            for c in pg.list:
                if c.code == 201 and c.parameters[0] == 0:
                    yield ev, pg, c.parameters[1], c.parameters[2], c.parameters[3]
            s = scripts(pg)
            for mm in re.finditer(r'player_new_map_id\s*=\s*(\d+)\s*[;\n]\s*\$game_temp\.player_new_x\s*=\s*(\d+)\s*[;\n]\s*'
                                  r'\$game_temp\.player_new_y\s*=\s*(\d+)', s):
                yield ev, pg, int(mm.group(1)), int(mm.group(2)), int(mm.group(3))
            for mm in re.finditer(r'(?:\$game_player\.moveto|pfp_ride)\(\s*(\d+)\s*,\s*(\d+)\s*\)', s):
                yield ev, pg, None, int(mm.group(1)), int(mm.group(2))


def swaps(m):
    """(event, target map, fix-up landings) for scripts that put the player on another map at the spot they stood on
    (pfp_swap_map, player_new_x = $game_player.x)."""
    for ev in m.events.values():
        for pg in ev.pages:
            s = scripts(pg)
            for mm in re.finditer(r'pfp_swap_map\(\s*(\d+)\s*(?:,\s*(\{[^}]*\}))?', s):
                fix = [(int(a), int(b)) for a, b in re.findall(r'=>\s*\[\s*(\d+)\s*,\s*(\d+)\s*\]', mm.group(2) or '')]
                yield ev, int(mm.group(1)), fix
            for mm in re.finditer(r'player_new_map_id\s*=\s*(\d+)\s*[;\n]\s*\$game_temp\.player_new_x\s*=\s*(?![\s\d])', s):
                yield ev, int(mm.group(1)), []


def load_all(specs):
    import rmarshal as M
    maps = {}
    for s in specs:
        p = os.path.join(OUT, 'Data', 'Map%03d.rxdata' % s['id'])
        if os.path.exists(p): maps[s['id']] = M.load_file(p)
    return maps


def puzzle_maps():
    try:
        import puzzles
    except ImportError:
        return set()
    out = set()
    for mod in puzzles.modules():
        for r in getattr(mod, 'ROOMS', {}).values():
            if isinstance(r.get('map'), int): out.add(r['map'])
        for make, kw in getattr(mod, 'CHECKS', []):
            try:
                mdl = make() if callable(make) else None
            except Exception:
                continue
            for c in getattr(mdl, 'cells', ()) or ():
                if isinstance(c, tuple) and len(c) == 3 and c[1] >= 0: out.add(c[0])
    return out


# Maps the engine moves the player onto at the spot they stood on elsewhere (plugins / mapgen/ruby code, not events)
PLUGIN_SWAPS = [(181, 608, 'the Lowlight swap (mapgen/ruby/012_Lumen.rb)')]


class Reach:
    """Arrivals and flood fills for every built map (a map's swaps need their source map's fill)."""

    def __init__(self, specs):
        import render as R
        self.tsets = R.tilesets(); self.maps = load_all(specs); self.by_id = {s['id']: s for s in specs}
        self.views = {}; self.seeds = {}; self.local = {}; self.swap_in = {}
        for sid, m in self.maps.items():
            for ev, pg, tm, x, y in transfers(m):
                tm = sid if tm is None else tm
                if tm == sid and pg.trigger not in (3, 4): self.local.setdefault(sid, []).append((ev.id, (x, y)))
                else: self.seeds.setdefault(tm, set()).add((x, y))
            for ev, tm, fix in swaps(m):
                self.swap_in.setdefault(tm, []).append((sid, '"%s" on %d' % (ev.name, sid)))
                self.seeds.setdefault(tm, set()).update(fix)
        for a, b, why in PLUGIN_SWAPS: self.swap_in.setdefault(b, []).append((a, why))
        for s in specs:                                          # HealingSpot (blacking out, Fly)
            hs = (s.get('metadata') or {}).get('HealingSpot')
            if hs: self.seeds.setdefault(int(hs[0]), set()).add((int(hs[1]), int(hs[2])))
        tm = os.path.join(os.path.dirname(HERE), 'pbs', 'town_map.txt')
        if os.path.exists(tm):
            for line in open(tm, encoding='utf-8'):
                if not line.startswith('Point'): continue
                f = [v.strip() for v in line.split('=', 1)[1].split(',')]
                if len(f) >= 7 and f[4] and f[5] and f[6]:
                    try: self.seeds.setdefault(int(f[4]), set()).add((int(f[5]), int(f[6])))
                    except ValueError: pass
        self.sides = {}
        for s in specs:
            for c in s.get('connections', []) or []:
                d = c['dir'][0].upper()
                self.sides.setdefault(s['id'], set()).add(d)
                self.sides.setdefault(c['to'], set()).add({'N': 'S', 'S': 'N', 'W': 'E', 'E': 'W'}[d])
        self.pz = puzzle_maps(); self.pz_cells = None; self.done = {}

    def view(self, mid):
        if mid not in self.views:
            m = self.maps[mid]; self.views[mid] = MapView(mid, m, self.tsets[m.tileset_id])
        return self.views[mid]

    def puzzle_cells(self):
        """Every tile a puzzle room's model can ever stand the player on (Model.cells, shifted by its offset onto the
        built map): planks, flats and bridges the room's own devices open count as floor."""
        if self.pz_cells is None:
            self.pz_cells = {}
            try:
                import puzzles
                for mod in puzzles.modules():
                    for make, kw in mod.CHECKS:
                        try:
                            mdl = make() if callable(make) else None
                        except Exception:
                            continue
                        off = getattr(mdl, 'offset', (0, 0))
                        for c in getattr(mdl, 'cells', ()) or ():
                            if isinstance(c, tuple) and len(c) == 3 and c[1] >= 0:
                                self.pz_cells.setdefault(c[0], set()).add((c[1] + off[0], c[2] + off[1]))
            except ImportError:
                pass
        return self.pz_cells

    def why(self, mid, depth=0):
        """Why this map's fill may miss cells the player can stand on ([] = exact)."""
        V = self.view(mid); out = list(V.dynamic)
        if mid in self.pz: out.insert(0, 'puzzle room (mapgen/puzzles)')
        for src, how in self.swap_in.get(mid, []):
            if src not in self.maps: out.append('%s: a map that is not built' % how)
            elif depth < 3 and self.why(src, depth + 1): out.append('%s, an approximate map' % how)
        return out

    def solve(self, mid):
        """(reached cells, arrival cells) on mid.  A swap seeds its target from the source map's fill, so the maps joined
        by swaps (171 <-> 172 <-> 173) are filled together to a fixed point (more seeds only ever add cells)."""
        if mid in self.done: return self.done[mid]
        group = set(); todo = [mid]
        while todo:
            g = todo.pop()
            if g in group or g not in self.maps: continue
            group.add(g); todo += [src for src, _h in self.swap_in.get(g, [])]
        res = {g: self.fill(g) for g in group}
        for _ in range(len(group) + 1):
            changed = False
            for g in group:
                extra = set()
                for src, _h in self.swap_in.get(g, []):
                    if src in res and src != g: extra |= res[src][0]
                if not extra: continue
                r = self.fill(g, extra)
                if r[0] != res[g][0]: res[g] = r; changed = True
            if not changed: break
        for g in group: self.done.setdefault(g, res[g])
        return self.done[mid]

    def fill(self, mid, extra=()):
        V = self.view(mid); m = V.m; s = self.by_id.get(mid, {})
        start = set()
        for x, y in self.seeds.get(mid, ()):
            start.add((x, y))
            if any(is_door(e) for e in V.at.get((x, y), [])): start.add((x, y + 1))
        for p in s.get('walk_from', []) or []: start.add(tuple(p))
        for d in self.sides.get(mid, ()):
            edge = [(0, y) for y in range(V.H)] if d == 'W' else [(V.W - 1, y) for y in range(V.H)] if d == 'E' else \
                   [(x, 0) for x in range(V.W)] if d == 'N' else [(x, V.H - 1) for x in range(V.W)]
            start |= {c for c in edge if V.ok(c[0], c[1], 0, True)}
        start |= {c for c in extra if V.valid(*c) and V.ok(c[0], c[1], 0, True)}
        if mid in self.pz: start |= self.puzzle_cells().get(mid, set())
        start = {c for c in start if V.valid(*c)}
        # sinks: a touch page that is always there and transfers the player away at its first level (exit mats)
        sink = set()
        for (x, y), evs in V.at.items():
            for e in evs:
                if all(p.trigger in (1, 2) and V.over_trigger(e, p) and any(c.code == 201 and c.indent == 0 for c in p.list)
                       for p in e.pages) and not all(has_cond(p) for p in e.pages):
                    sink.add((x, y))
        seen = set(); todo = list(start); landed = set(start); pending = list(self.local.get(mid, []))
        while True:
            while todo:
                c = todo.pop()
                if c in seen: continue
                seen.add(c)
                if c in sink and c not in landed: continue         # stepping onto an exit mat leaves; landing on one doesn't
                for n in V.steps(*c):
                    if n not in seen: todo.append(n)
            more = [t for eid, t in pending if t not in seen and reached(V, m.events[eid], seen)]
            pending = [(eid, t) for eid, t in pending if t not in seen and not reached(V, m.events[eid], seen)]
            if not more: break
            todo += more; landed |= set(more)
        # a strip of exit mats / wrong-turn warps: the first one sends you away, the rest of the strip is paint
        grow = [c for c in seen if c in sink]
        while grow:
            x, y = grow.pop()
            for dx, dy in DIRS:
                n = (x + dx, y + dy)
                if n in sink and n not in seen: seen.add(n); grow.append(n)
        return seen, start


def check(selected, specs, ctx, verbose=False):
    """STANDON + REACH warnings for the selected maps; returns the number of REACH problems on exact maps."""
    RC = Reach(specs)
    bad = 0; stats = []
    for s in selected:
        mid = s['id']; m = RC.maps.get(mid)
        if m is None: continue
        V = RC.view(mid)
        # ---- STANDON
        so = []
        for ev in m.events.values():
            for i, pg in enumerate(ev.pages):
                if pg.trigger != 0 or not real_cmds(pg): continue
                g = pg.graphic
                if g.tile_id > 0 and pg.through: continue          # a Through floor graphic is walked over on purpose
                if (g.tile_id > 0 or g.character_name) and V.over_trigger(ev, pg):
                    so.append('"%s" at %d,%d (page %d, %s)' % (ev.name, ev.x, ev.y, i + 1, ('tile %d' % g.tile_id) if g.tile_id > 0
                              else 'Through charset %s' % g.character_name))
                    break
        if so:
            ctx.warn(mid, 'STANDON: %d action event(s) show an object on a walk-on tile, so Essentials runs them only when the '
                     'player stands ON them, never from beside (over_trigger): %s%s. Give the graphic a solid tile (passage '
                     '0x0f) or a non-Through charset' % (len(so), '; '.join(so[:3]), '; +%d more' % (len(so) - 3) if len(so) > 3 else ''))
        # ---- REACH
        seen, start = RC.solve(mid)
        if not start:
            stats.append((mid, 'no arrivals')); continue
        why = RC.why(mid); exact = not why
        miss = []
        ign = [re.compile(r) for r in s.get('reach_ignore', []) or []]   # spec: names of events meant to be out of reach
        for ev in m.events.values():
            if TRAINER.search(ev.name or '') or ev.id in V.mobile: continue
            if any(r.search(ev.name or '') for r in ign): continue
            pages = [p for p in ev.pages if (p.trigger == 0 and real_cmds(p)) or
                     (p.trigger in (1, 2) and any(c.code == 201 for c in p.list))]
            if pages and not reached(V, ev, seen, pages): miss.append((ev, pages[0]))
        for ev, pg in miss:
            kind = 'warp/door' if any(c.code == 201 for p in ev.pages for c in p.list) else 'action event'
            how = 'standing on it (over_trigger)' if V.over_trigger(ev, pg) else 'a tile beside it'
            ctx.warn(mid, 'REACH%s: %s "%s" at %d,%d can\'t be reached from the arrivals (needs %s)%s' % (
                '' if exact else ' (approximate)', kind, ev.name, ev.x, ev.y, how,
                '' if exact else '; approximate because ' + why[0]))
        if exact: bad += len(miss)
        if verbose:
            if not hasattr(ctx, 'reach_seen'): ctx.reach_seen = {}
            ctx.reach_seen[mid] = (seen, start)
        stats.append((mid, '%s, %d arrivals, %d cells, %d unreachable%s' % ('exact' if exact else 'approx', len(start), len(seen),
                                                                         len(miss), '' if exact else ' (%s)' % why[0])))
    if verbose:
        for mid, st in stats: print('REACH %3d: %s' % (mid, st))
    ctx.reach_stats = stats
    return bad


def reached(V, ev, seen, pages=None):
    """Can the player, standing on a reached cell, trigger one of these pages (default: any page)?"""
    for pg in pages or ev.pages:
        if V.over_trigger(ev, pg):
            if (ev.x, ev.y) in seen: return True
            continue
        for dx, dy in DIRS:
            if (ev.x + dx, ev.y + dy) in seen: return True
            if V.counter(ev.x + dx, ev.y + dy) and (ev.x + 2 * dx, ev.y + 2 * dy) in seen: return True
    return False


if __name__ == '__main__':
    import sys, glob, yaml
    sys.path.insert(0, HERE)
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    specs = []
    for f in sorted(glob.glob(os.path.join(HERE, 'specs', '*.yaml'))):
        for s in yaml.safe_load_all(open(f)):
            if s: specs.append(s)

    class C:
        warnings = []
        def warn(self, mid, msg): self.warnings.append('map %s: %s' % (mid, msg))
    ctx = C()
    sel = [s for s in specs if not args or str(s['id']) in args]
    n = check(sel, specs, ctx, verbose='--verbose' in sys.argv)
    for w in ctx.warnings: print('WARN', w)
    print('%d REACH problem(s) on exact maps; %d warnings' % (n, len(ctx.warnings)))
