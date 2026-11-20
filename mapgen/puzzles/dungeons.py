"""Early dungeons (DUNGEON_PUZZLES Part 1, Chapters 1-2): D1 the Glassed Orchard chime rows, D2 the Deepwood lantern
cocoons, D3 Cocoonfall Hollow's crystal-silk anchors.  These have no walking in their logic (the devices stand on
always-reachable ground and every action is its own undo or a free reset), so they are proved as state machines."""
import os
from .core import machine, Model, Device, around

V_CHIME = 501                       # D1: notes rung in order (0-3)
S_COCOON = (506, 507, 508)          # D2: lantern cocoons 1-3 lit
S_BRIDGE = (511, 512, 513)          # D3: bridges a, b, c taut
CHIME_ORDER = ('L', 'M', 'H')       # the gate phrase: low, middle, high
POSTS = {'alpha': (0, 1), 'beta': (1, 2)}                      # D2 anchor post -> cocoons it lights/douses
ANCHORS = {1: (0, 1), 2: (1, 2), 3: (0, 2)}                    # D3 anchor -> bridges it re-threads


def d1():
    def actions(v):
        return [('ring ' + n, v + 1 if CHIME_ORDER[v] == n else 0) for n in CHIME_ORDER] if v < 3 else []
    return machine('d1_chime (522)', 0, actions, lambda v: v == 3, moves=3, rating=2)


def d2():
    def actions(v):
        return [(n + ' post', tuple(b ^ (i in c) for i, b in enumerate(v))) for n, c in POSTS.items()]
    return machine('d2_cocoons (525)', (0, 0, 0), actions, lambda v: v == (1, 0, 1), moves=2, rating=2)


def d3():
    """Design fix: the spec started with ONE bridge taut and claimed 'never all three', but an anchor flips two, so
    one taut -> three taut in a single pull (anchor 2).  Starting with TWO taut (a and b) makes the parity argument
    true: every reachable state has two taut bridges or none, never all three, so opening the nest (c) always costs a or b."""
    def actions(v):
        return [('anchor %d' % n, tuple(b ^ (i in c) for i, b in enumerate(v))) for n, c in ANCHORS.items()]
    return machine('d3_anchors (548)', (1, 1, 0), actions, lambda v: v[2] == 1, moves=1, invariant=lambda v: sum(v) in (0, 2), rating=2)


# ---- D2 the Deepwood (525): the lantern hollow ------------------------------------------------------------------------
# Silk leans one way: a curtain lets you through only the way its threads lean (a chevron in the sag); from the other side
# it is a wall.  A lit lantern cocoon makes its curtain lean the other way.  Post alpha lights cocoons 1 and 2, post beta
# 2 and 3 (a Joltik on each post sends the spark along the strand: Electroweb runs the threads, the field's own rule).
# The hollow is walled with silk round the Deepwood's north-east pocket: outside -> C1 -> the thicket -> C3 -> the island
# (Silver Powder and TM19).  Post alpha stands outside, post beta inside the thicket, so the order is forced: alpha then
# beta.  Cocoon 2 is lit twice and goes dark again, so C2 (the thicket's back door) is open the way out at the end.
D2_COCOONS = {1: (29, 7), 2: (30, 10), 3: (33, 6)}                            # hung in the silk wall beside their curtains
D2_WALLS = [c for c in [(30, 5), (29, 7), (29, 9), (30, 10), (32, 10), (37, 7), (37, 8), (37, 9)] + [(x, 6) for x in range(30, 41) if x != 34]
            if c not in D2_COCOONS.values()]
D2_CURTAINS = {1: ((29, 8), 'W'), 2: ((31, 10), 'S'), 3: ((34, 6), 'S')}      # cocoon n -> (cell, natural lean)
D2_EXIT = ((30, 4), 'W')                                                        # the island's one-way way home
D2_POSTS = {'alpha': ((25, 7), (0, 1)), 'beta': ((33, 9), (1, 2))}
D2_START, D2_GOAL = (24, 8), (39, 1)
D2_LEAN = {'N': (0, -1), 'S': (0, 1), 'E': (1, 0), 'W': (-1, 0)}
D2_FLIP = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
MAP525 = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'maps_out', 'Data', 'Map525.rxdata')


class SilkModel(Model):
    """One-way silk: stepping into a curtain moving the way it leans carries you through to the far side."""
    rebuild_same_class = True

    def leans(self, v):
        out = {c: lean for c, lean in [D2_EXIT]}
        for n, (c, lean) in D2_CURTAINS.items():
            out[c] = D2_FLIP[lean] if v[n - 1] else lean
        return out

    def region(self, cell, v):
        lean = self.leans(v)
        seen = {cell}; q = [cell]
        while q:
            m, x, y = q.pop()
            for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                c = (x + dx, y + dy)
                if c in lean:
                    if D2_LEAN[lean[c]] != (dx, dy): continue
                    n = (m, c[0] + dx, c[1] + dy)
                    if n not in self.cells or not self.passable(n, v): continue
                elif (m,) + c in self.cells and self.passable((m,) + c, v):
                    n = (m,) + c
                else:
                    continue
                if n not in seen: seen.add(n); q.append(n)
        return frozenset(seen)


def silk_model():
    from .built import load
    import render as R, build as B
    m = load(525); ts = R.tilesets()[m.tileset_id]; L = m.data.data
    block = set(D2_WALLS) | {c for c, _ in D2_CURTAINS.values()} | {D2_EXIT[0]} | {p for p, _ in D2_POSTS.values()} | set(D2_COCOONS.values())
    ev = {(e.x, e.y) for e in m.events.values() if e.name in ('Item', 'HiddenItem') or e.name.startswith('Trainer(')} | {D2_GOAL}
    cells = {(525, x, y) for y in range(m.height) for x in range(m.width)
             if B.cell_passable(L, ts, x, y) and (x, y) not in block and (x, y) not in ev}

    def lights(lines):
        def act(v, c):
            v = list(v)
            for i in lines: v[i] ^= 1
            return tuple(v), c
        return act
    dev = [Device('post %s' % n, [c for c in around(525, *p) if c in cells], lights(lines), 'post %s' % n) for n, (p, lines) in D2_POSTS.items()]
    mdl = SilkModel('d2_lantern_hollow (525)', cells, lambda c, v: True, (525,) + D2_START, (0, 0, 0), dev,
                    [c for c in around(525, *D2_GOAL) if c in cells], resets=[(525,) + D2_START])
    mdl.game = lambda v: ({}, {S_COCOON[i]: bool(v[i]) for i in range(3)})
    return mdl


# ---- D7 the Rimewood (562): the Frost Loom ------------------------------------------------------------------------
# Three frozen threads (pegs) hold three icicle curtains across the east side path, a dead end whose pocket hides the
# trapper's cache.  Pulling a thread runs frost along it: every curtain on its line cracks if frozen, refreezes if broken.
# Left: curtains 1 and 2 · middle: 2 and 3 · right: 3.  Unique answer over Z2: left + right (middle would refreeze 2).
S_CURTAIN = (531, 532, 533)
D7_CURTAINS = [(47, 16), (47, 17), (47, 18)]                 # the 1-wide corridor up the east edge
D7_THREADS = {'left': ((40, 19), (0, 1)), 'middle': ((41, 19), (1, 2)), 'right': ((42, 19), (2,))}
D7_CACHE, D7_START = (44, 12), (36, 21)
MAP562 = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'maps_out', 'Data', 'Map562.rxdata')


def frost_model():
    """On the Rimewood's own terrain (the built map's layers; the curtains are this module's events)."""
    from .built import load
    import render as R, build as B
    m = load(562); ts = R.tilesets()[m.tileset_id]; L = m.data.data
    cells = {(562, x, y) for y in range(m.height) for x in range(m.width) if B.cell_passable(L, ts, x, y)}
    cells |= {(562,) + c for c in D7_CURTAINS}
    cells -= {(562,) + p for p, _ in D7_THREADS.values()} | {(562,) + D7_CACHE}

    def passable(c, v):
        if (c[1], c[2]) in D7_CURTAINS: return bool(v[D7_CURTAINS.index((c[1], c[2]))])
        return True

    def pull(lines):
        def act(v, c):
            v = list(v)
            for i in lines: v[i] ^= 1
            return tuple(v), c
        return act
    dev = [Device('%s thread' % n, [c for c in around(562, *p) if c in cells], pull(lines), '%s thread' % n)
           for n, (p, lines) in D7_THREADS.items()]
    mdl = Model('d7_frost_loom (562)', cells, passable, (562,) + D7_START, (0, 0, 0), dev,
                [c for c in around(562, *D7_CACHE) if c in cells], resets=[(562,) + D7_START])
    mdl.game = lambda v: ({}, {S_CURTAIN[i]: bool(v[i]) for i in range(3)})
    return mdl


def d7_unique():
    sols = []
    for mask in range(8):
        v = [0, 0, 0]
        for i, (_, lines) in enumerate(D7_THREADS.values()):
            if mask >> i & 1:
                for l in lines: v[l] ^= 1
        if v == [1, 1, 1]: sols.append([n for i, n in enumerate(D7_THREADS) if mask >> i & 1])
    ok = sols == [['left', 'right']]
    return ok, ['%s d7_frost_loom: unique answer over Z2: %r' % ('ok  ' if ok else 'FAIL', sols)]


CHECKS = ([(frost_model, dict(moves=2, rating=3, without={'the right thread': ['right thread']}))] if os.path.exists(MAP562) else []) + \
         ([(silk_model, dict(moves=2, rating=2, without={'post alpha': ['post alpha'], 'post beta': ['post beta']}))] if os.path.exists(MAP525) else [])
EXTRA = [d1, d2, d3, d7_unique]

ROOMS = {
    'd1_chime': dict(name='The Chime Rows', map=522, reset=dict(vars={V_CHIME: 0}), home=False, solved=dict(vars={V_CHIME: 3}),
                     hints=["The chime post by the gate plays a little phrase. The cracked trees each ring one note of it.",
                            "Low, middle, high. Walk past the cracked trees in that order; a wrong note starts the phrase over.",
                            "Ring the west tree, then the middle one, then the north-east one. The glass hedge will shatter."]),
    'd2_cocoons': dict(name='The Deepwood lanterns', map=525, home=False,
                       reset=dict(switches={S_COCOON[0]: False, S_COCOON[1]: False, S_COCOON[2]: False}),
                       solved=dict(switches={S_COCOON[0]: True, S_COCOON[1]: False, S_COCOON[2]: True}),
                       hints=["A spark runs along a whole thread. Count the cocoons on each one.",
                              "The middle cocoon hangs on both threads. Touch both posts and it has been lit twice.",
                              "Touch the alpha post, then the beta post: the first and third curtains lean the other way."]),
    'd7_frost_loom': dict(name='The Frost Loom', map=562, home=False,
                          reset=dict(switches={S_CURTAIN[0]: False, S_CURTAIN[1]: False, S_CURTAIN[2]: False}),
                          solved=dict(switches={S_CURTAIN[0]: True, S_CURTAIN[1]: True, S_CURTAIN[2]: True}),
                          hints=["Each thread runs to more than one curtain. Count the cracks, not the pulls.",
                                 "The middle thread would refreeze the second curtain if anything else had broken it.",
                                 "Pull the left thread and the right thread, once each."]),
    'd2_lantern_hollow': dict(name='The lantern hollow', map=525, home=False,
                              reset=dict(switches={S_COCOON[0]: False, S_COCOON[1]: False, S_COCOON[2]: False}),
                              solved=dict(switches={S_COCOON[0]: True, S_COCOON[1]: False, S_COCOON[2]: True}),
                              hints=["The chevron in each curtain's sag points the way it lets you through.",
                                     "Each post lights two cocoons. One post is outside the thicket, one inside it.",
                                     "Touch the outside post, go in by the first curtain, touch the inside post, and go on north."]),
    'd3_anchors': dict(name='Cocoonfall anchors', map=548, home=False,
                       reset=dict(switches={S_BRIDGE[0]: True, S_BRIDGE[1]: True, S_BRIDGE[2]: False}),
                       hints=["Every anchor pulls two threads at once. Three threads can't all be tight.",
                              "Cross the two bridges that are already taut before you touch anything.",
                              "Visit both houses first. Then pull the middle or the right anchor: one house bridge goes slack and the nest's pulls tight."]),
}

# ---- in-engine pieces -------------------------------------------------------------------------------------------
# D1 is built with events only, laid over the existing Orchard (build.py appends EVENTS[map] to that map's spec, so
# the layout owner's script is untouched).  The three "rows" are the Orchard's own rows of glass apple trees.
T40 = dict(glow=22968, signpost=8114, crystal=8098)          # tileset 40 "Prismfall Wilds"
D1_TREES = {'L': (4, 16), 'M': (23, 16), 'H': (35, 25)}       # touch tile beside each cracked tree
D1_POST, D1_HEDGE, D1_PRIZE = (19, 33), (38, 3), (38, 1)


def _d1_events():
    ev = [{'type': 'event', 'name': 'Chime post', 'at': list(D1_POST), 'pages': [{'graphic': {'tile': T40['signpost']}, 'commands': [
        "A spur of green glass by the gate. Three glass apples hang from it like wind chimes: small, middling and large.",
        {'se': 'Mining reveal'}, "It rings a little phrase: LOW ... MIDDLE ... HIGH.",
        "\\pf[JUNO,happy]Juno: (from beyond the Veil) It's the bit before the chorus in Wingull Shanty! Low, middle, high!",
        {'if': 'PrismfallPuzzles.room_log(:d1_chime)[:fails] >= 1', 'then': [{'script': 'pfp_hint(:d1_chime)'}]}]}]}]
    for n, (x, y) in D1_TREES.items():
        ev.append({'type': 'event', 'name': 'Cracked tree ' + n, 'at': [x, y], 'pages': [
            {'graphic': {'tile': T40['glow']}, 'trigger': 'touch', 'commands': [{'script': 'pfp_chime(:%s)' % n}]},
            {'cond': {'var': ['D1_CHIME', 3]}}]})
    ev.append({'type': 'event', 'name': 'Glass hedge', 'at': list(D1_HEDGE), 'pages': [
        {'graphic': {'tile': T40['crystal']}, 'commands': [
            "A hedge of glass apple boughs, fused shut. Something is caught on the far side.",
            "Hairline cracks run through it, as if one clear note would finish the job."]},
        {'cond': {'var': ['D1_CHIME', 3]}}]})
    ev.append({'type': 'event', 'name': 'Lost satchel', 'at': list(D1_PRIZE), 'pages': [
        {'graphic': {'sprite': 'Object ball'}, 'commands': [
            "A child's satchel, half glassed over. Inside: a wooden Wingull whistle and a sliver of something that hums.",
            {'script': 'pfm_item(:BLEEDSHARD, 1, "Bleed Shard")'}, {'script': 'pfm_set(:d1_satchel)'}, {'selfswitch': ['A', True]}]},
        {'cond': {'self': 'A'}}]})
    return ev


def _d7_events():
    T52 = dict(icicles=19299, peg=19243, shards=19272)        # tileset 52: the frozen fall's icicles, a trapper's peg
    ev = []
    for i, (x, y) in enumerate(D7_CURTAINS):
        ev.append({'type': 'event', 'name': 'Icicle curtain %d' % (i + 1), 'at': [x, y], 'pages': [
            {'graphic': {'tile': T52['icicles']}, 'commands': [
                "A curtain of icicles, frozen solid to a silver thread that runs back down the path.",
                {'if': 'PrismfallPuzzles.room_log(:d7_frost_loom)[:fails] >= 1 || $game_switches[%d] || $game_switches[%d]' % (S_CURTAIN[0], S_CURTAIN[2]),
                 'then': [{'script': 'pfp_hint(:d7_frost_loom)'}]}]},
            {'cond': {'switch': S_CURTAIN[i]}, 'graphic': {'tile': T52['shards']}, 'through': True}]})
    LINE = {'left': 'the first and second curtains', 'middle': 'the second and third curtains', 'right': 'the third curtain'}
    for n, ((x, y), lines) in D7_THREADS.items():
        sc = '\n'.join('pfp_flip(%d)' % S_CURTAIN[l] for l in lines)
        ev.append({'type': 'event', 'name': 'Frozen thread (%s)' % n, 'at': [x, y], 'pages': [{'graphic': {'tile': T52['peg']}, 'commands': [
            "A frozen thread runs from this peg up the east path, to %s." % LINE[n],
            {'choices': ['Pull it', 'Leave it'], 'cancel': 2, 'branches': [[
                {'se': 'Anim/Ice1'}, {'script': sc}, {'raw': [225, [2, 3, 6]]},
                "Frost runs up the thread. Somewhere up the path, ice cracks... and ice sets again.",
                {'script': 'pbMessage(_INTL("(Curtains: {1})", [%s].map { |s| $game_switches[s] ? "broken" : "frozen" }.join(", ")))' % ', '.join(str(c) for c in S_CURTAIN)}],
                []]}]}]})
    ev.append({'type': 'event', 'name': "Trapper's cache", 'at': list(D7_CACHE), 'pages': [
        {'graphic': {'sprite': 'Object ball'}, 'commands': [
            "A trapper's cache, tucked under the roots: two Snowballs, wrapped in waxed cloth.",
            {'script': 'pfm_item(:SNOWBALL, 2, "Snowball")'}, {'selfswitch': ['A', True]}]},
        {'cond': {'self': 'A'}}]})
    ev.append({'type': 'npc', 'name': 'Trapper', 'at': [39, 21], 'sprite': 'NPC 19', 'dir': 'up', 'commands': [
        "Trapper: That's Tamsin's grandmother's trick, those threads. A frost loom. She strung it for us the winter the wolves came down.",
        "Trapper: Pull one and it cracks what's frozen on its line, and freezes what's broken. Like a heddle, she said. Whatever that is."]})
    return ev


def _d2_events():
    DIR = {'S': 'down', 'W': 'left', 'E': 'right', 'N': 'up'}
    WAY = {'S': 'south', 'W': 'west', 'E': 'east', 'N': 'north'}
    ev = []
    for i, (x, y) in enumerate(D2_WALLS):
        ev.append({'type': 'event', 'name': 'Silk wall %d' % i, 'at': [x, y], 'pages': [
            {'graphic': {'sprite': 'pf_silk_wall', 'dir': 'down'}, 'dir_fix': True}]})
    curt = [(n, c, lean) for n, (c, lean) in D2_CURTAINS.items()] + [(0, D2_EXIT[0], D2_EXIT[1])]
    for n, (x, y), lean in curt:
        def page(l, cond=None):
            pg = {'graphic': {'sprite': 'pf_silk_curtain', 'dir': DIR[l]}, 'dir_fix': True, 'trigger': 'touch',
                  'commands': [{'script': 'pfp_silk("%s", %d)' % (lean, S_COCOON[n - 1] if n else 0)}]}
            if cond: pg['cond'] = cond
            return pg
        pages = [page(lean)]
        if n: pages.append(page(D2_FLIP[lean], {'switch': S_COCOON[n - 1]}))
        ev.append({'type': 'event', 'name': 'Silk curtain %d' % n if n else 'Silk curtain home', 'at': [x, y], 'pages': pages})
    for n, (x, y) in D2_COCOONS.items():
        ev.append({'type': 'event', 'name': 'Lantern cocoon %d' % n, 'at': [x, y], 'pages': [
            {'graphic': {'sprite': 'pf_lantern_cocoon', 'dir': 'down'}, 'dir_fix': True,
             'commands': ['A cocoon hung on a strand, dark. When it glows, the silk beside it leans the other way.']},
            {'cond': {'switch': S_COCOON[n - 1]}, 'graphic': {'sprite': 'pf_lantern_cocoon', 'dir': 'up'}, 'dir_fix': True,
             'commands': ['The cocoon glows like a lantern. The silk beside it has swung the other way.']}]})
    for name, ((x, y), lines) in D2_POSTS.items():
        sc = '\n'.join('pfp_flip(%d)' % S_COCOON[i] for i in lines)
        ev.append({'type': 'event', 'name': 'Anchor post %s' % name, 'at': [x, y], 'pages': [
            {'graphic': {'sprite': 'Followers/JOLTIK', 'dir': 'down'}, 'step_anime': True, 'dir_fix': True, 'commands': [
                "A Joltik clings to the anchor post where two silk strands are tied.",
                {'choices': ['Touch the strands', 'Leave it'], 'cancel': 2, 'branches': [[
                    {'se': 'Anim/Thunder1'}, {'script': sc},
                    "The Joltik sparks! The charge runs both strands, and every cocoon on them changes: dark ones glow, glowing ones go dark."], []]}]}]})
    ev.append({'type': 'item', 'at': list(D2_GOAL), 'item': 'TM19'})
    ev.append({'type': 'sign', 'at': [25, 9], 'text': '"SILK ONLY LETS YOU GO THE WAY IT\'S BEEN PULLED. A LIT COCOON PULLS IT THE OTHER WAY. -- Woodward"'})
    return ev


EVENTS = {522: _d1_events(), 562: _d7_events(), 525: _d2_events()}

RUBY = """
# D2 the Deepwood: one-way silk.  natural = the way the curtain leans when its cocoon is dark; sw = the cocoon (0 = none).
def pfp_silk(natural, sw)
  flip = { "N" => "S", "S" => "N", "E" => "W", "W" => "E" }
  lean = (sw > 0 && $game_switches[sw]) ? flip[natural] : natural
  d = { "N" => 8, "S" => 2, "E" => 6, "W" => 4 }[lean]
  if $game_player.direction == d
    dx, dy = { 8 => [0, -1], 2 => [0, 1], 6 => [1, 0], 4 => [-1, 0] }[d]
    pbSEPlay("Door slide", 60, 130) rescue nil
    PrismfallPuzzles.ride($game_player.x + dx * 2, $game_player.y + dy * 2)
  else
    pbMessage(_INTL("The silk holds fast. Its threads lean the other way."))
  end
end
# D1 the Glassed Orchard: ring the cracked trees in the gate phrase's order (low, middle, high).
def pfp_chime(note)
  order = [:L, :M, :H]
  names = { :L => "low", :M => "middle", :H => "high" }
  v = $game_variables[501].to_i
  return if v >= 3
  if order[v] == note
    $game_variables[501] = v + 1
    pbSEPlay("Mining reveal") rescue nil
    if v + 1 >= 3
      pbMessage(_INTL("The cracked tree rings the {1} note... and the whole phrase hangs in the air, finished.", names[note]))
      pbSEPlay("Battle damage super") rescue nil
      pbMessage(_INTL("Far to the north-east, a hedge of glass shatters."))
    else
      pbMessage(_INTL("The cracked tree rings as you pass: the {1} note. ({2} of 3)", names[note], v + 1))
    end
  elsif v > 0 || note != order[0]
    $game_variables[501] = 0
    PrismfallPuzzles.fail!(:d1_chime, _INTL("A sour chord: this tree rings the {1} note, but the gate phrase wanted the {2} one next. The rows fall silent. Start the phrase again.", names[note], names[order[v]]))
  end
  $game_map.need_refresh = true
end
"""
