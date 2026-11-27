"""Gym 6, the Infirmary (Mirefen; Corvin Mott, Poison, :CORROSIVE_MIRE, cap 35): GYM_PUZZLES "Gym 6", as Gemini built
it (mapgen/layouts/mirefen_gym.py, maps 230-233; commit efed7468).  These proofs run on the BUILT maps only: the
geometry, the bridges and the gate are read from maps_out/Data/MapNNN.rxdata exactly as Essentials decides them
(puzzles/built.py), and the devices do what the events' own Ruby does (the bench, funnel, socket, basin, tray and
sludge scripts in the specs).  No design grid: Gemini's layout is the source, so the proof follows it.

One rule all the way up: DOSE MAKES THE CURE.  Two unmarked flasks, 3 and 5 (V330 / V331, shared by every room); a
tap bench fills, pours between and tips them; funnels take a whole flask and want an exact amount (a wrong dose is
wasted, never a lock).
  230 Entrance (TEACH): the funnel wants 3 -> S334 lowers the bridge.                         fill 3, pour: 2 moves
  231 Dispensary (TWIST, four from three and five): the purge funnel wants 4 -> S330.             7 moves
  232 Sludge Gallery (COMBINE): socket A on the island wants exactly 1 (S331 opens the sluice gate); basin B on the far
      dais adds up and wants exactly 7 (S332 lowers the arena bridge; more than 7 drains it to 0).  Only the west bench
      fills.  The sludge spans are 6 and 7 steps; the mask filter (V332) lasts 10 sludge steps, refills at the west end
      (5,10) and on the island (13,16); at 10 the fumes drive you back to the west end (4,13), flasks and doses kept.
      Modelled as crossings (a device: the cheapest straight walk, which costs the filter its width) plus a "wade" of one
      sludge step and back (+1), so every filter value is explored; spent -> the west end.
  Quiet Alcove (232's south hall, optional MASTERY): flasks of 4 and 9 (V430 / V431), the vat wants 1, then 3, then 6
      (V432; S333, Synthetic Seed x2 + Black Sludge).
Wenlow (231 / 232) is the apprentice: hint tiers and a rinse (flasks 0, filter fresh, back to the entrance mat).

Rating (GYM_PUZZLES 0b: Gym 6 is 6/10 = 16 moves, 4 096 states a required room; the Mastery may sit two above).  The
solver's 232 route is 16 device uses: make 1 in the 3 (the 5 stays full), cross, refill, dose A, pour 5>3 on the tray,
cross, put the 2 into B, wade back (the fumes carry you home), fill the 5, cross, refill, cross, pour 5: 7.  Exactly at
the cap, so a later change to 232 that adds a step fails the rating.

Speed: no event page here has a variable condition, so walking depends on the switches only; regions and passability
are cached per switch state (the whole module runs in a few seconds)."""
from .core import Model, Device, machine, verify, DIRS

V3, V5, VF, VB = 330, 331, 332, 333
S_VALVE4, S_A, S_B, S_QUIET, S_TEACH = 330, 331, 332, 333, 334
V4, V9, VP = 430, 431, 432
RATING = 6

START = {230: (10, 15), 231: (14, 23), 232: (4, 13)}       # where the warps in land
GOAL = {230: (10, 5), 231: (14, 5), 232: (14, 5)}          # the tile in front of the next room's door
BENCH = {230: (6, 9), 231: (7, 14), 232: (3, 10)}
FUNNEL = {230: ((14, 9), 3), 231: ((14, 10), 4)}
WENLOW = {231: (9, 19), 232: (4, 16)}
WEST_END = (4, 13)                                           # the fumes / the recall cord / Wenlow's rinse put you here
REFILL = [(5, 10), (13, 16)]
SOCKET_A, BASIN_B = (13, 10), (25, 10)
TRAYS = [(15, 10), (27, 11)]
RECALL = (27, 15)
SPAN1 = (6, 11)                                              # x range of the two sludge spans, rows 12-14
SPAN2 = (17, 23)
SLUDGE_ROWS = (12, 13, 14)
# (from, to, sludge steps): the straight walks across the spans
CROSSINGS = [((5, 13), (12, 13), 6, 'cross span 1 east'), ((12, 13), (5, 13), 6, 'cross span 1 west'),
             ((16, 13), (24, 13), 7, 'cross span 2 east'), ((24, 13), (16, 13), 7, 'cross span 2 west')]


def pour(a, b, cap_b):
    amt = min(a, cap_b - b)
    return a - amt, b + amt


def flask_ops(s, b, fill=True, caps=(3, 5)):
    """the bench menu (the trays drop the two Fill lines): [(label, (s, b))], unchanged results left out"""
    c3, c5 = caps
    out = []
    if fill:
        out += [('fill %d' % c3, (c3, b)), ('fill %d' % c5, (s, c5))]
    s2, b2 = pour(s, b, c5); out.append(('pour %d>%d' % (c3, c5), (s2, b2)))
    b3, s3 = pour(b, s, c3); out.append(('pour %d>%d' % (c5, c3), (s3, b3)))
    out += [('tip %d' % c3, (0, b)), ('tip %d' % c5, (s, 0))]
    return [(l, r) for l, r in out if r != (s, b)]


def around(mid, x, y): return [(mid, x + dx, y + dy) for dx, dy in DIRS]


def _built(mid):
    from . import built as BUILT
    try:
        return BUILT.Built([mid])
    except FileNotFoundError:
        return None


class SwitchModel(Model):
    """walking depends on the switches only (no variable page conditions on these maps): regions are cached per
    (cell, switch state)"""
    def region(self, cell, v):
        k = (cell, self.swkey(v))
        r = self._regions.get(k)
        if r is None:
            r = self._regions[k] = Model.region(self, cell, v)
        return r


def room(mid, name, v0, game, devices, extra_solid=(), resets=()):
    """a Model whose walking is the built map's (events by page, directional passage), with `extra_solid` cells
    (the sludge: crossed only through the crossing devices) taken out"""
    b = _built(mid)
    if b is None: return None
    m0 = b.maps[mid]
    cells = {(mid, x, y) for y in range(m0.height) for x in range(m0.width)}
    solid = {(mid, x, y) for x, y in extra_solid}
    swkey = lambda v: tuple(sorted(game(v)[1].items()))
    pcache, mcache = {}, {}

    def passable(c, v):
        if c in solid: return False
        k = (c, swkey(v))
        if k not in pcache:
            pcache[k] = b.passable(c, {}, dict(k[1]))
        return pcache[k]
    m = SwitchModel(name, cells, passable, (mid,) + START[mid], v0, devices, goal=[(mid,) + GOAL[mid]], resets=resets)
    m.swkey, m._regions = swkey, {}

    def move_ok(c, n, v):
        k = (c, n, swkey(v))
        if k not in mcache:
            mcache[k] = b.can_move(c, n, {}, dict(k[2]))
        return mcache[k]
    m.move_ok = move_ok
    return m


def bench_devices(mid, idx, caps=(3, 5), at=None, fill=True, label='bench'):
    """one Device per menu line; idx = the positions of the two flasks in the state tuple"""
    i, j = idx
    devs = []
    names = ['fill %d' % caps[0], 'fill %d' % caps[1], 'pour %d>%d' % caps, 'pour %d>%d' % (caps[1], caps[0]),
             'tip %d' % caps[0], 'tip %d' % caps[1]]
    for want in (names if fill else names[2:]):
        def act(v, c, want=want):
            for l, (s, b) in flask_ops(v[i], v[j], fill, caps):
                if l == want:
                    t = list(v); t[i], t[j] = s, b
                    return (tuple(t), c)
            return None
        devs.append(Device('%s: %s' % (label, want), around(mid, *(at or BENCH[mid])), act, label='%s %s' % (label, want)))
    return devs


def funnel_devices(mid, at, want, k):
    """pour a whole flask into a funnel that wants exactly `want`; v[k] = its switch. A wrong dose empties the flask."""
    devs = []
    for f in (0, 1):
        def act(v, c, f=f):
            if v[k] or v[f] == 0: return None          # done already / an empty flask: a message, nothing else
            t = list(v); amt = t[f]; t[f] = 0
            if amt == want: t[k] = 1
            return (tuple(t), c)
        devs.append(Device('funnel: pour the %d' % (3, 5)[f], around(mid, *at), act, label='funnel <- %d-flask' % (3, 5)[f]))
    return devs


# ------------------------------------------------------------------ 230 / 231: bench + funnel
def model_funnel_room(mid):
    at, want = FUNNEL[mid]
    sw = {230: S_TEACH, 231: S_VALVE4}[mid]
    game = lambda v: ({V3: v[0], V5: v[1]}, {sw: bool(v[2])})
    devs = bench_devices(mid, (0, 1)) + funnel_devices(mid, at, want, 2)
    name = {230: 'g6_230 (Entrance, TEACH: 3)', 231: 'g6_231 (Dispensary, TWIST: 4 from 3 and 5)'}[mid]
    resets = around(mid, *WENLOW[mid]) if mid in WENLOW else ()
    return room(mid, name, (0, 0, 0), game, devs, resets=resets)


def model_230(): return model_funnel_room(230)
def model_231(): return model_funnel_room(231)


# ------------------------------------------------------------------ 232 Sludge Gallery
# state: (3-flask, 5-flask, filter steps used, socket A done, basin B total 0-7)
def game_232(v):
    s, b, f, a, bb = v
    return {V3: s, V5: b, VF: f, VB: bb}, {S_A: bool(a), S_B: bb == 7}


def spent(v):
    """the fumes: back to the west end, a fresh filter, flasks and doses kept"""
    return (v[0], v[1], 0, v[3], v[4]), (232,) + WEST_END


def model_232(wade=True):
    devs = bench_devices(232, (0, 1))
    for i, t in enumerate(TRAYS):
        devs += bench_devices(232, (0, 1), at=t, fill=False, label='tray %s' % 'AB'[i])
    for r in REFILL:
        devs.append(Device('mask refill %d,%d' % r, around(232, *r),
                           lambda v, c: None if v[2] == 0 else ((v[0], v[1], 0, v[3], v[4]), c), label='refill'))
    for frm, to, cost, lab in CROSSINGS:
        def cross(v, c, to=to, cost=cost):
            if v[2] + cost >= 10: return spent(v)
            return (v[0], v[1], v[2] + cost, v[3], v[4]), (232,) + to
        devs.append(Device(lab, [(232,) + frm], cross, label=lab))
    if wade:   # one sludge step in and back out, from any bank tile beside a span
        banks = [(232, 5, y) for y in SLUDGE_ROWS] + [(232, 12, y) for y in SLUDGE_ROWS] + \
                [(232, 16, y) for y in SLUDGE_ROWS] + [(232, 24, y) for y in SLUDGE_ROWS]
        devs.append(Device('wade', banks, lambda v, c: spent(v) if v[2] + 1 >= 10 else ((v[0], v[1], v[2] + 1, v[3], v[4]), c),
                           label='wade a step'))
    for f in (0, 1):
        def socket(v, c, f=f):
            if v[3] or v[f] == 0: return None
            t = list(v); amt = t[f]; t[f] = 0
            if amt == 1: t[3] = 1
            return (tuple(t), c)
        devs.append(Device('socket A: pour the %d' % (3, 5)[f], around(232, *SOCKET_A), socket, label='socket A <- %d-flask' % (3, 5)[f]))

        def basin(v, c, f=f):
            if v[4] == 7 or v[f] == 0: return None
            t = list(v); amt = t[f]; t[f] = 0
            tot = t[4] + amt
            t[4] = tot if tot <= 7 else 0               # overflow drains it
            return (tuple(t), c)
        devs.append(Device('basin B: pour the %d' % (3, 5)[f], around(232, *BASIN_B), basin, label='basin B <- %d-flask' % (3, 5)[f]))
    devs.append(Device('recall cord', around(232, *RECALL), lambda v, c: spent(v), label='recall cord'))
    sludge = [(x, y) for y in SLUDGE_ROWS for x in list(range(SPAN1[0], SPAN1[1] + 1)) + list(range(SPAN2[0], SPAN2[1] + 1))]
    m = room(232, 'g6_232 (Sludge Gallery, COMBINE: 1 then 7, carried)' + ('' if wade else ' [straight walks only]'),
             (0, 0, 0, 0, 0), game_232, devs, extra_solid=sludge)
    return m


def proof_232():
    """no soft-lock with every filter value (wading), and the route against the gym's rating"""
    m = model_232(True)
    if m is None: return True, ['skip g6_232: Map232.rxdata is not built']
    return verify(m, rating=RATING)


# ------------------------------------------------------------------ the Quiet Alcove (optional MASTERY, 232 south hall)
def proof_quiet():
    """flasks 4 and 9 at the alcove tap, the vat wants 1, then 3, then 6; a wrong dose empties the flask"""
    want = (1, 3, 6)

    def actions(st):
        s, b, k = st
        if k >= 3: return []
        out = [(l, (s2, b2, k)) for l, (s2, b2) in flask_ops(s, b, True, (4, 9))]
        for f, amt in ((0, s), (1, b)):
            if amt == 0: continue
            t = [s, b]; t[f] = 0
            out.append(('vat <- %d-flask' % (4, 9)[f], (t[0], t[1], k + 1 if amt == want[k] else k)))
        return out
    return machine('g6_quiet (Quiet Alcove, MASTERY: 1, 3, 6 from 4 and 9)', (0, 0, 0), actions, lambda st: st[2] == 3,
                   rating=RATING + 2)


def check_230(): m = model_230(); return (True, ['skip g6_230: not built']) if m is None else verify(m, moves=2, rating=RATING)
def check_231(): m = model_231(); return (True, ['skip g6_231: not built']) if m is None else verify(m, moves=7, rating=RATING)


# The walking proofs read the built maps themselves (there is no design grid to re-prove), so they live in EXTRA and
# built.run() has nothing to rebuild here.
CHECKS = []
EXTRA = [check_230, check_231, proof_232, proof_quiet]
ROOMS = {}       # Gemini's rooms keep their own runtime (the events' Ruby); nothing generated into the registry
RUBY = ''
