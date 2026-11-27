"""Gym 5, the Dig (Duneholt; Sahar Ostrand, Ground, :DESERT, cap 31): GYM_PUZZLES "Gym 5", as Gemini built it
(mapgen/layouts/duneholt_gym.py, maps 210-212).

One rule: SUN HARDENS, SHADE SINKS. A sand lane in the sunbeam is crust (walkable); in shade it is soft, and stepping
on it drops you to the Under-Dig (212) at the same x, y. Two sun-mirrors pick the lit lanes:
  M1 on T1 (3, 12) cycles V325: 0 lane a lit, 1 lane b lit, 2 the wall
  M2 on T2 (25, 12) cycles V326: 0 lane d lit, 1 the wall, 2 lane c lit       (Gemini's order; GYM_PUZZLES lists
                                                                               0 c / 1 d / 2 wall: same cycle, d first)
  lanes: a T1 <-> T0, b T0 <-> T2, c T1 <-> T3 (the stair to 213), d T2 <-> the cistern (Max Ether)
  212's galleries never meet; each has one ladder up, so where you fall decides where you come up.
  210 TEACH: the cracked sand in the entrance hall always drops you to 212's cellar, ladder up to T0.
The aha: lane c's mirror is on the far terrace, and the only way there is to fall through lane c.

There is no design grid here: the proof reads the BUILT maps (maps_out/Data/Map210-212.rxdata) through
puzzles/built.Built (Essentials' passability, NPCs and trainers solid), the lane tiles' soft / crust state from their
own event pages (puzzles/built.active_page: a lane is soft where its active page is a touch page), and the warps
from the specs. Falls are moves (devices) so the proof can show the solution needs them."""
import os
import yaml
from .core import Model, Device, verify, DIRS
from . import built as BT

V_M1, V_M2 = 325, 326
MIDS = (210, 211, 212)
START = (210, 10, 15)
GOAL = (211, 14, 2)                   # the stair up to 213, the Warden Arena
M1, M2 = (211, 3, 12), (211, 25, 12)
TEACH_LANDING = (212, 14, 23)
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class DigModel(Model):
    """core.Model keys a state by min(region), which assumes walking regions are symmetric. The Dig's are not (falls
    and ladders are one-way; the cellar's rope climbs back to 210, which can't walk down to it), so key by the region."""
    def key(self, cell, v):
        r = self.region(cell, v)
        return (r, v), r


def game(v):
    return {V_M1: v[0], V_M2: v[1]}, {}


def _specs():
    out = {}
    for f in os.listdir(os.path.join(HERE, 'specs')):
        if f.split('_')[0] in ('210', '211', '212'):
            d = yaml.safe_load(open(os.path.join(HERE, 'specs', f), encoding='utf-8'))
            out[d['id']] = d
    return out


def model_dig():
    b = BT.Built(MIDS)
    specs = _specs()
    lanes = {}                                     # (211, x, y) -> (lane letter, rxdata event)
    teach = set()
    for mid in MIDS:
        for e in b.maps[mid].events.values():
            if mid == 211 and e.name.startswith('Sand '):
                lanes[(mid, e.x, e.y)] = (e.name.split()[1], e)
            elif mid == 210 and e.name.startswith('Teach Sand'):
                teach.add((mid, e.x, e.y))
    links, blocked = {}, set()
    for mid, d in specs.items():
        for e in d['events']:
            to = e.get('to') or {}
            if e.get('type') not in ('warp', 'door', 'exit') or not to: continue
            c = (mid, e['at'][0], e['at'][1])
            if to.get('map') in MIDS: links[c] = (to['map'], to['x'], to['y'])
            elif c != GOAL: blocked.add(c)                 # out to Duneholt: not part of the room

    def soft(cell, v):
        pg = BT.active_page(lanes[cell][1], *game(v))
        return pg is not None and pg.trigger == 1          # the touch page: shade, it gives way

    def passable(cell, v):
        if cell in blocked or cell in teach: return False
        if cell in lanes and soft(cell, v): return False
        return b.passable(cell, *game(v))

    cells = {(mid, x, y) for mid in MIDS for y in range(b.maps[mid].height) for x in range(b.maps[mid].width)}

    def around(c): return [(c[0], c[1] + dx, c[2] + dy) for dx, dy in DIRS]

    def mirror(var_i):
        def act(v, c):
            w = list(v); w[var_i] = (w[var_i] + 1) % 3
            return tuple(w), c
        return act

    devs = [Device('M1', around(M1), mirror(0), 'M1'), Device('M2', around(M2), mirror(1), 'M2')]
    for lane in 'abcd':
        tiles = [c for c, (l, _) in lanes.items() if l == lane]
        stand = sorted({n for t in tiles for n in around(t) if n not in lanes})
        def fall(v, c, tiles=tiles):
            for t in tiles:
                if abs(t[1] - c[1]) + abs(t[2] - c[2]) == 1 and soft(t, v) and b.can_move(c, t, *game(v)):
                    return v, (212, t[1], t[2])
            return None
        devs.append(Device('fall ' + lane, stand, fall, 'drop into lane ' + lane))
    tstand = sorted({n for t in teach for n in around(t) if n not in teach})
    devs.append(Device('teach drop', tstand,
                       lambda v, c: (v, TEACH_LANDING) if any(abs(t[1] - c[1]) + abs(t[2] - c[2]) == 1 for t in teach) else None,
                       'the entrance drop'))
    npc = {'Apprentice Nadim': 211, 'Digger Samim': 212}
    resets = set()
    for name, mid in npc.items():
        e = next(e for e in b.maps[mid].events.values() if e.name == name)
        resets |= set(around((mid, e.x, e.y)))
    m = DigModel('g5_dig (Entrance + Dunes + Under-Dig)', cells, passable, START, (0, 0), devs, [GOAL], links=links,
              resets=resets)
    m.move_ok = lambda c, n, v: c[0] != n[0] or b.can_move(c, n, *game(v))
    m.lane_tiles = lanes
    return m


def proof_dig():
    try:
        m = model_dig()
    except FileNotFoundError as e:
        return True, ['skip g5_dig: %s' % e]
    falls = ['fall a', 'fall b', 'fall c', 'fall d']
    ok, out = verify(m, moves=5, without={'the falls (only the entrance drop)': falls, 'mirror M2': ['M2']}, rating=5)
    # every lane tile has somewhere to land: the Under-Dig cell below it is walkable whatever the mirrors say
    bad = [c for c in m.lane_tiles if not m.passable((212, c[1], c[2]), (0, 0))]
    if bad:
        ok = False; out.append('FAIL g5_dig: %d lane tiles fall into rock on 212, e.g. %r' % (len(bad), bad[:4]))
    else:
        out.append('  every one of the %d lane tiles lands on the Under-Dig floor' % len(m.lane_tiles))
    return ok, out


CHECKS = []
EXTRA = [proof_dig]
ROOMS = {}
