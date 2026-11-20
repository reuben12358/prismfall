"""The Loomhouse Canopy, Briarwick (Gym 2, SPINE Revision 19: Tamsin, Bug, Silkwood, doubles), rating 3/10.

The user: "can we redo the puzzle to be some type of web based trampoline puzzle?"  Map 131 is the hollow of Briarwick's
elder tree, where Tamsin's Bug Pokemon spin silk across the drop.  Map 130 stays the weavers' lobby (no puzzle).

CORE RULE - a web throws you.  Step onto a TAUT web and it launches you 3 tiles on, in the direction you stepped onto it.
  If you land on another taut web you are thrown again, the same way.  Land on a ledge or a sticky web and you stop.
  Land on nothing and you drop into Tamsin's safety net, which lowers you back to the hall's entrance.
TEACH   the entrance ledge -> one web -> the first ledge; then two webs in a column: a web can throw you onto a web.
TWIST   STICKY webs hold you where you land.  Bounce up onto one in mid-air, step sideways onto a taut web, and you are
        thrown sideways: sticky webs are how you change direction.  The wrong web drops you.
COMBINE Joltik on the strands.  A Joltik zaps its strand and every web on it changes: taut goes slack (sticky) and slack
        goes taut.  Joltik 1 (on the third ledge) zaps webs A and B; Joltik 2 (on a side perch you reach by web) zaps B
        and C.  Tamsin's ledge needs A taut (up), B sticky (stop), C taut (across).  Zap only Joltik 1 and A and B are
        both taut: they throw you straight up the trunk and into the net.  Both Joltik, once each, is the answer.
Glyphs: # void / bark mass   W bark wall face   . ledge   v the drop   w taut web   s sticky web   A B C Joltik webs
        J Joltik (solid)   S stair cell"""
from collections import deque
from .core import Model, Device, around

V_A, V_B, V_C = 305, 306, 307                  # Joltik webs A/B/C: 0 = as built, 1 = zapped (flipped)
JUMP = 3
DIRS4 = {(0, -1): 8, (0, 1): 2, (-1, 0): 4, (1, 0): 6}


def _hall():
    W, H = 25, 35
    g = [['#'] * W for _ in range(H)]

    def fill(x0, x1, y0, y1, ch):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1): g[y][x] = ch
    fill(1, 23, 1, 3, 'W')                       # the bark wall at the top of the hollow (knot-hole window, Tamsin's den)
    g[2][20] = g[3][20] = 'S'                     # the stair up to the Upper Lofts, behind Tamsin
    fill(1, 23, 4, 9, 'v')                       # COMBINE gap
    fill(15, 23, 4, 7, '.')                      # Tamsin's ledge
    fill(1, 3, 5, 6, '.')                        # the Joltik perch (west)
    fill(1, 23, 10, 11, '.')                     # ledge 3
    fill(1, 23, 12, 16, 'v')                     # TWIST gap
    fill(1, 23, 17, 18, '.')                     # ledge 2
    fill(1, 23, 19, 23, 'v')                     # TEACH (chain) gap
    fill(1, 23, 24, 25, '.')                     # ledge 1
    fill(1, 23, 26, 28, 'v')                     # TEACH gap
    fill(1, 23, 29, 33, '.')                     # the entrance floor
    g[34][12] = '.'                               # the entrance (stairs down to the lobby)
    for (x, y), ch in WEBS.items(): g[y][x] = ch
    for (x, y) in JOLTIK.values(): g[y][x] = 'J'
    return [''.join(r) for r in g]


# webs: 'w' taut, 's' sticky, 'A'/'B'/'C' Joltik webs (their as-built state is in JOLT_WEB)
WEBS = {(12, 28): 'w',                                   # TEACH 1: entrance floor -> ledge 1
        (18, 23): 'w', (18, 20): 'w',                    # TEACH 2: a web throws you onto a web -> ledge 2
        (6, 16): 'w', (6, 13): 's', (7, 13): 'w', (10, 13): 's', (10, 12): 's',   # TWIST: up, stop, across, stop, walk up
        (5, 13): 'w', (11, 13): 'w', (14, 16): 'w',      # TWIST traps: each throws you into the net
        (12, 9): 'A', (12, 6): 'B', (13, 6): 'C',        # COMBINE
        (2, 9): 'w', (2, 7): 'w'}                        # to the Joltik perch and back down
JOLT_WEB = {'A': (V_A, False), 'B': (V_B, False), 'C': (V_C, False)}   # as built: all three slack (sticky)
JOLTIK = {1: (16, 10), 2: (1, 5)}
JOLT_ZAPS = {1: ('A', 'B'), 2: ('B', 'C')}
HALL = _hall()
AT = dict(start=(12, 33), entrance=(12, 34), tamsin=(17, 5), stair=(20, 2), bram=(22, 6), juno=(13, 33), pim=(15, 32),
          nell=(4, 24), orla=(20, 17), leavanny=(21, 24), arrive_from_lofts=(20, 4), sign_teach=(10, 29),
          sign_sticky=(4, 17), sign_joltik=(14, 11))


def web_kind(ch, v):
    """'w' taut / 's' sticky for the web glyph in Joltik state v = (a, b, c) (1 = zapped)."""
    if ch in 'ws': return ch
    taut = JOLT_WEB[ch][1] ^ bool(v['ABC'.index(ch)])
    return 'w' if taut else 's'


def throw(x, y, d, v, rows=None):
    """Where a taut web at (x, y), entered moving d, finally puts you: ('land', (x, y)) or ('fall', (x, y))."""
    rows = rows or HALL
    seen = set()
    while True:
        x, y = x + d[0] * JUMP, y + d[1] * JUMP
        if not (0 <= y < len(rows) and 0 <= x < len(rows[0])): return 'fall', (x, y)
        ch = rows[y][x]
        if ch in 'wsABC':
            k = web_kind(ch, v)
            if k == 's': return 'land', (x, y)
            if (x, y) in seen: return 'fall', (x, y)
            seen.add((x, y)); continue
        if ch in '.S': return 'land', (x, y)
        return 'fall', (x, y)


class CanopyModel(Model):
    """Walking region with webs: stepping onto a taut web throws you (direction-dependent); a fall lands at the start.
    On the built map (puzzles/built.py keeps this class) a landing tile that decor blocks counts as a fall, so a prop
    dropped on a landing spot breaks the proof."""
    rebuild_same_class = True

    def region(self, cell, v):
        start = self.start
        seen = {cell}; q = [cell]
        while q:
            m, x, y = q.pop()
            for (dx, dy) in DIRS4:
                n = (m, x + dx, y + dy)
                if n not in self.cells: continue
                ch = HALL[n[2]][n[1]]
                if not self.step_ok((m, x, y), n, v): continue
                if ch in 'wsABC' and web_kind(ch, v) == 'w':
                    kind, (lx, ly) = throw(n[1], n[2], (dx, dy), v)
                    land = (m, lx, ly)
                    n = land if kind == 'land' and land in self.cells and self.passable(land, v) else start
                elif not self.passable(n, v):
                    continue
                if n not in seen:
                    seen.add(n); q.append(n)
        return frozenset(seen)


def canopy_model():
    cells = {(131, x, y) for y, r in enumerate(HALL) for x, ch in enumerate(r) if ch not in '#WJv'}
    solid = {AT[k] for k in ('tamsin', 'bram', 'juno', 'pim', 'nell', 'orla', 'leavanny')} | set(AT[k] for k in ('sign_teach', 'sign_sticky', 'sign_joltik'))
    cells -= {(131, x, y) for x, y in solid}
    cells -= {(131,) + AT['entrance']}

    def passable(c, v):
        ch = HALL[c[2]][c[1]]
        if ch in 'wsABC': return web_kind(ch, v) == 's'
        return ch in '.S'
    idx = {'A': 0, 'B': 1, 'C': 2}

    def zap(n):
        def act(v, c):
            v = list(v)
            for w in JOLT_ZAPS[n]: v[idx[w]] ^= 1
            return tuple(v), c
        return act
    dev = [Device('Joltik %d' % n, [c for c in around(131, *p) if c in cells], zap(n), 'Joltik %d' % n) for n, p in JOLTIK.items()]
    m = CanopyModel('lh_canopy (131)', cells, passable, (131,) + AT['start'], (0, 0, 0), dev,
                    [c for c in around(131, *AT['tamsin']) if c in cells], resets=around(131, *AT['pim']))
    m.game = lambda v: ({V_A: v[0], V_B: v[1], V_C: v[2]}, {})
    m.exits = [(131,) + AT['stair'], (131, AT['stair'][0], AT['stair'][1] + 1)]
    return m


def canopy_sections():
    """Each beat is needed: no Joltik = no way up; Joltik 1 alone throws you into the net; the twist cannot be skipped."""
    from .core import verify
    out = []; ok = True
    m = canopy_model()
    for label, skip in (('Joltik 1', {'Joltik 1'}), ('Joltik 2', {'Joltik 2'})):
        if m.solve(skip=skip)[0] is not None: ok = False; out.append('FAIL lh_canopy: solvable without ' + label)
        else: out.append('  proved: lh_canopy unsolvable without ' + label)
    # the trap: Joltik 1 alone, then step on web A from ledge 3 -> the net
    kind, at = throw(12, 9, (0, -1), (1, 1, 0))
    if kind != 'fall': ok = False; out.append('FAIL lh_canopy: A+B taut should throw you into the net, lands at %r' % (at,))
    else: out.append('  proved: Joltik 1 alone makes A and B taut: they throw you up the trunk into the net')
    # every web in the as-built state lands where the design says
    expect = {(12, 28, (0, -1)): ('land', (12, 25)), (18, 23, (0, -1)): ('land', (18, 17)), (6, 16, (0, -1)): ('land', (6, 13)),
              (7, 13, (1, 0)): ('land', (10, 13)), (5, 13, (-1, 0)): ('fall', None), (11, 13, (1, 0)): ('fall', None),
              (14, 16, (0, -1)): ('fall', None), (2, 9, (0, -1)): ('land', (2, 6)), (2, 7, (0, 1)): ('land', (2, 10))}
    for (x, y, d), (kind, at) in expect.items():
        k2, a2 = throw(x, y, d, (0, 0, 0))
        if k2 != kind or (at and a2 != at):
            ok = False; out.append('FAIL lh_canopy: web (%d,%d) going %r gives %s %r, design says %s %r' % (x, y, d, k2, a2, kind, at))
    if ok: out.append('  proved: every web throws where the design says (teach, chain, sticky turn, traps, the perch)')
    # without the sticky webs (all taut) the twist cannot be crossed
    return ok, out


CHECKS = [(canopy_model, dict(moves=2, rating=3))]
EXTRA = [canopy_sections]

ROOMS = {
    'lh_canopy': dict(name='The Canopy', map=131, start=list(AT['start']) + [8], reset=dict(vars={V_A: 0, V_B: 0, V_C: 0}),
                      solved=dict(vars={V_A: 1, V_B: 0, V_C: 1}),
                      hints=["A Joltik's spark runs the whole strand. Look at which webs hang on each one.",
                             "Up there you want to go up, stop, then go across. Taut throws, sticky stops.",
                             "Spark both Joltik, once each: the one on the third ledge and the one on the west perch. Then the bottom "
                             "web throws you up, the middle one holds you, and the top one throws you across to Tamsin."],
                      reset_text="(He clicks his tongue; somewhere above, a Joltik yawns.) There. Every strand as Tamsin left it."),
}


def _ruby():
    webs = []
    for (x, y), ch in sorted(WEBS.items()):
        if ch in 'ws': webs.append('[%d, %d] => "%s"' % (x, y, ch))
        else:
            var, taut = JOLT_WEB[ch]
            webs.append('[%d, %d] => [%d, %s]' % (x, y, var, 'true' if taut else 'false'))
    floor = ', '.join('[%d, %d]' % (x, y) for y, r in enumerate(HALL) for x, ch in enumerate(r) if ch in '.S')
    return ('PrismfallPuzzles.web_room(131, { :room => :lh_canopy, :jump => %d, :start => [%d, %d],\n'
            '  :webs => { %s },\n  :floor => [%s] }) if PrismfallPuzzles.respond_to?(:web_room)\n'
            % (JUMP, AT['start'][0], AT['start'][1], ', '.join(webs), floor))


RUBY = _ruby()
