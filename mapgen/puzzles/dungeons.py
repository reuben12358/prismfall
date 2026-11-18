"""Early dungeons (DUNGEON_PUZZLES Part 1, Chapters 1-2): D1 the Glassed Orchard chime rows, D2 the Deepwood lantern
cocoons, D3 Cocoonfall Hollow's crystal-silk anchors.  These have no walking in their logic (the devices stand on
always-reachable ground and every action is its own undo or a free reset), so they are proved as state machines."""
from .core import machine

V_CHIME = 501                       # D1: notes rung in order (0-3)
S_COCOON = (506, 507, 508)          # D2: lantern cocoons 1-3 lit
S_BRIDGE = (511, 512, 513)          # D3: bridges a, b, c taut
CHIME_ORDER = ('L', 'M', 'H')       # the gate phrase: low, middle, high
POSTS = {'alpha': (0, 1), 'beta': (1, 2)}                      # D2 anchor post -> cocoons it lights/douses
ANCHORS = {1: (0, 1), 2: (1, 2), 3: (0, 2)}                    # D3 anchor -> bridges it re-threads


def d1():
    def actions(v):
        return [('ring ' + n, v + 1 if CHIME_ORDER[v] == n else 0) for n in CHIME_ORDER] if v < 3 else []
    return machine('d1_chime (522)', 0, actions, lambda v: v == 3, moves=3)


def d2():
    def actions(v):
        return [(n + ' post', tuple(b ^ (i in c) for i, b in enumerate(v))) for n, c in POSTS.items()]
    return machine('d2_cocoons (525)', (0, 0, 0), actions, lambda v: v == (1, 0, 1), moves=2)


def d3():
    """Design fix: the spec started with ONE bridge taut and claimed 'never all three', but an anchor flips two, so
    one taut -> three taut in a single pull (anchor 2).  Starting with TWO taut (a and b) makes the parity argument
    true: every reachable state has two taut bridges or none, never all three, so opening the nest (c) always costs a or b."""
    def actions(v):
        return [('anchor %d' % n, tuple(b ^ (i in c) for i, b in enumerate(v))) for n, c in ANCHORS.items()]
    return machine('d3_anchors (548)', (1, 1, 0), actions, lambda v: v[2] == 1, moves=1, invariant=lambda v: sum(v) in (0, 2))


CHECKS = []
EXTRA = [d1, d2, d3]

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
    'd3_anchors': dict(name='Cocoonfall anchors', map=548, home=False,
                       reset=dict(switches={S_BRIDGE[0]: True, S_BRIDGE[1]: True, S_BRIDGE[2]: False}),
                       hints=["Every anchor pulls two threads at once. Three threads can't all be tight.",
                              "Cross the two bridges that are already taut before you touch anything.",
                              "Visit both houses first. Then pull the middle or the right anchor: one house bridge goes slack and the nest's pulls tight."]),
}
