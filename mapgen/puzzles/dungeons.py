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


EVENTS = {522: _d1_events()}

RUBY = """
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
