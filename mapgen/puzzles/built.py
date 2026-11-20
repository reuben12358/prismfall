"""mapgen/puzzles/built.py - the engine-level proof: every room model is re-proved on the BUILT map.

The model keeps its logic (devices, start, goal, resets) but its geometry is thrown away: walkability comes from
maps_out/Data/MapNNN.rxdata exactly as Essentials decides it (Game_Map#passable?):
  - an event on the tile whose active page shows a tile graphic: that tile's passage / priority decides;
  - an event whose active page shows a character (NPC, item ball, trainer) and is not Through: solid;
  - otherwise the three map layers, top down (build.cell_passable).
The active page is the last one whose switch / variable conditions hold in the puzzle state (self switches count as
OFF, so one-shot NPCs stay solid: the conservative case).  If decor is dropped on a tile the solution needs, a plank
event is missing, or a device cannot be reached, the proof fails and `build.py --strict` stops."""
import os
from .core import Model, Device, verify, DIRS

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(os.path.dirname(HERE), 'maps_out')
_maps = {}


def load(mid):
    if mid not in _maps:
        import rmarshal as M
        p = os.path.join(OUT, 'Data', 'Map%03d.rxdata' % mid)
        _maps[mid] = M.load_file(p) if os.path.exists(p) else None
    return _maps[mid]


def active_page(ev, vars_, sw):
    for pg in reversed(ev.pages):
        c = pg.condition
        if c.switch1_valid and not sw.get(c.switch1_id, False): continue
        if c.switch2_valid and not sw.get(c.switch2_id, False): continue
        if c.variable_valid and vars_.get(c.variable_id, 0) < c.variable_value: continue
        if c.self_switch_valid: continue
        return pg
    return None


class Built:
    def __init__(self, mids):
        import render as R, build as B
        self.B = B; self.maps = {m: load(m) for m in mids}; self.ts = {}; self.ev = {}
        for mid, m in self.maps.items():
            if m is None: raise FileNotFoundError('Map%03d.rxdata is not built' % mid)
            self.ts[mid] = R.tilesets()[m.tileset_id]
            for e in m.events.values(): self.ev.setdefault((mid, e.x, e.y), []).append(e)

    def passable(self, cell, vars_, sw):
        mid, x, y = cell
        m = self.maps[mid]; ts = self.ts[mid]
        if not (0 <= x < m.width and 0 <= y < m.height): return False
        for e in self.ev.get(cell, []):
            pg = active_page(e, vars_, sw)
            if pg is None or pg.through: continue
            g = pg.graphic
            if g.tile_id > 0:
                if ts['passages'][g.tile_id] & 0x0f: return False
                if ts['priorities'][g.tile_id] == 0: return True
            elif g.character_name:
                return False
        return self.B.cell_passable(m.data.data, ts, x, y)

    BIT = {(0, 1): 1, (-1, 0): 2, (1, 0): 4, (0, -1): 8}            # Essentials' passage bits: down, left, right, up

    def dir_ok(self, cell, bit, vars_, sw):
        """Game_Map#passable?(x, y, d) for one tile and one direction bit: events first, then layers top down."""
        mid, x, y = cell
        m = self.maps[mid]; ts = self.ts[mid]
        if not (0 <= x < m.width and 0 <= y < m.height): return False
        for e in self.ev.get(cell, []):
            pg = active_page(e, vars_, sw)
            if pg is None or pg.through: continue
            g = pg.graphic
            if g.tile_id > 0:
                p = ts['passages'][g.tile_id]
                if p & bit or p & 0x0f == 0x0f: return False
                if ts['priorities'][g.tile_id] == 0: return True
            elif g.character_name:
                return False
        L = m.data.data
        for z in (2, 1, 0):
            t = int(L[z, y, x])
            if t == 0: continue
            tag = ts['terrain_tags'][t] if t < len(ts['terrain_tags']) else 0
            if tag in (13, 15): continue
            p = ts['passages'][t]
            if p & bit or p & 0x0f == 0x0f: return False
            if ts['priorities'][t] == 0: return True
        return True

    def can_move(self, c, n, vars_, sw):
        """Game_Character#passable?: the tile you leave must let you out that way, the tile you enter must let you in."""
        d = (n[1] - c[1], n[2] - c[2])
        if d not in self.BIT: return True
        return self.dir_ok(c, self.BIT[d], vars_, sw) and self.dir_ok(n, self.BIT[(-d[0], -d[1])], vars_, sw)


def rebuild(model):
    """The same puzzle with the built maps' geometry."""
    off = getattr(model, 'offset', (0, 0))
    sh = lambda c: (c[0], c[1] + off[0], c[2] + off[1])
    un = lambda c: (c[0], c[1] - off[0], c[2] - off[1])
    mids = sorted({c[0] for c in model.cells if c[1] >= 0})
    b = Built(mids)
    cells = {(mid, x, y) for mid in mids for y in range(b.maps[mid].height) for x in range(b.maps[mid].width)}
    extra = {c for c in model.cells if c[1] < 0}                       # abstract goal cells (a chest that opens)
    exits = {sh(c) for c in getattr(model, 'exits', [])}               # doors to other rooms are not part of the proof

    def passable(c, v):
        if c in extra: return model.passable(c, v)
        if c in exits: return False
        vars_, sw = model.game(v)
        return b.passable(c, vars_, sw)
    devs = []
    for d in model.devices:
        def act(v, c, d=d):
            r = d.act(v, un(c))
            return None if r is None else (r[0], sh(r[1]))
        stand = [sh(c) for c in d.stand]
        devs.append(Device(d.name, stand, act, d.label))
    cls = model.__class__ if getattr(model, 'rebuild_same_class', False) else Model   # e.g. the Canopy's web throws
    def move_ok(c, n, v):                                               # directional passage bits (cliff edges, ledges, rails)
        if c in extra or n in extra or c[0] != n[0]: return True
        vars_, sw = model.game(v)
        return b.can_move(c, n, vars_, sw)
    m = cls(model.name + ' [built map]', cells | extra, passable, sh(model.start), model.vars0, devs,
              [sh(c) if c[1] >= 0 else c for c in model.goal], links={sh(k): sh(v) for k, v in model.links.items()},
              resets=[sh(c) for c in model.resets])
    m.move_ok = move_ok
    return m, b


def run(mods):
    bad = 0; lines = []
    for mod in mods:
        for make, kw in mod.CHECKS:
            model = make()
            if not hasattr(model, 'game'): continue
            try:
                m, b = rebuild(model)
            except FileNotFoundError as e:
                lines.append('skip %s: %s' % (model.name, e)); continue
            ok, out = verify(m, **kw)
            # where the design grid and the built map disagree in the start state (information for the builder)
            diff = [c for c in model.cells if c[1] >= 0 and model.passable(c, model.vars0) and not m.passable((c[0], c[1] + getattr(model, 'offset', (0, 0))[0], c[2] + getattr(model, 'offset', (0, 0))[1]), model.vars0)]
            if diff: out.append('  note: %d design-floor tiles are blocked on the built map (decor), e.g. %r' % (len(diff), sorted(diff)[:4]))
            lines += out; bad += 0 if ok else 1
    return bad, lines
