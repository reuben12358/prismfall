"""Gym 3, the Tidelock Gym (Ebbmouth, Marisol): GYM_PUZZLES Gym 3 after its trim (map builder 13).

The trim (GYM_PUZZLES 0b: rating 4, at most 8 required moves): the practice lock, then ONE basin worked with the level
wheels and the drifting raft.  The tide bell is gone from the required route (it and the gate's bell combination are
the Overflow Culvert Mastery's).  Two rules carry both rooms, so the practice lock teaches exactly what the basin asks:
  * raise the water and the raft drifts inland (east) until the end or a shut lock gate stops it;
  * lower the water and the chain winds the raft home to its berth (slot 0).
170 Lock Hall (TEACH): practice raft slots 0-6, the gate between 4 and 5, only slot 4 meets the pier.  Shut the gate,
raise the water: the raft stops at 4, walk it to the door.  2 moves.
171/172/173 Basins (Low / Mid / High: the level is the map you are on; the Lock Hall door always opens on Low):
raft slot 0 = the west pier (the gate lever), 1 = the island jetty (wheel C, the Race), 2 = the east pier.  At Mid the
raft bridges the walkway and the pier it lies against; at Low the beds are trenches (ladders at x 8 and x 24; the shut
gate walls the trench); at High the Race carries you from the island north to the Warden's door.  5 moves:
E (Mid) > gate > E (High: the raft parks at the island) > W (Mid) > C on the island (High) > the Race."""
from .core import machine

V_RAFT, V_PRACTICE = 315, 316
S_GATE, S_PRACTICE_GATE, S_PRACTICE_HIGH = 316, 317, 318
PRACTICE_SLOTS = {0: 2, 1: 4, 2: 6, 3: 8, 4: 11, 5: 16, 6: 19}     # slot -> raft column on 170
PRACTICE_GATE_X, PRACTICE_PIER = 14, 4                           # the gate stands between slots 4 and 5
BASIN_SLOTS = {0: 3, 1: 14, 2: 25}                               # slot -> raft column on 171-173
BASIN_GATE_X = 19
LOW, MID, HIGH = 0, 1, 2
MAPS = {LOW: 171, MID: 172, HIGH: 173}


def practice_drift(slot, gate):
    return PRACTICE_PIER if gate and slot <= PRACTICE_PIER else 6


def basin_drift(slot, gate):
    return 1 if gate and slot <= 1 else 2


def practice():
    def actions(v):
        slot, gate, high = v
        out = [('gate', (slot, 1 - gate, high))]
        out.append(('wheel', (0, gate, 0) if high else (practice_drift(slot, gate), gate, 1)))
        return out
    return machine('g3_practice (170)', (0, 0, 0), actions, lambda v: v[2] == 1 and v[0] == PRACTICE_PIER, moves=2, rating=2)


def basin_regions(level, raft, gate, at):
    """where you can walk from `at` (walking is free)"""
    if level == MID:
        pier = {0: 'WP', 1: 'IS', 2: 'EP'}[raft]
        if at in ('SW', pier): return {'SW', pier}
        return {at}
    if level == LOW:
        if at in ('SW', 'TR', 'EP'):
            return {'SW', 'TR', 'EP'} if not gate else ({'SW', 'TR'} if at != 'EP' else {'EP'})
        return {at}
    if at == 'IS': return {'IS', 'ND'}                         # the Race (High only)
    return {at}


def basin():
    def actions(v):
        level, raft, gate, at = v; out = []
        for p in basin_regions(level, raft, gate, at):
            if p == 'SW':
                if level > LOW: out.append(('W', (level - 1, 0 if level - 1 == LOW else raft, gate, 'SW')))
                if level < HIGH: out.append(('E', (level + 1, basin_drift(raft, gate) if level + 1 == HIGH else raft, gate, 'SW')))
            if p == 'WP' and level == MID:
                out.append(('gate', (level, raft, 1 - gate, 'WP')))
            if p == 'IS' and level == MID:
                out.append(('C', (HIGH, basin_drift(raft, gate), gate, 'IS')))
            if p == 'IS' and level == HIGH:
                out.append(('C', (MID, raft, gate, 'IS')))
            if p == 'ND':
                out.append(('the Race', (level, raft, gate, 'ND')))
        return out
    return machine('g3_basin (171-173)', (LOW, 0, 0, 'SW'), actions, lambda v: v[3] == 'ND', moves=6, rating=4)


def budget():
    a, la = practice(); b, lb = basin()
    n = int(la[0].split('shortest solution ')[1].split(' ')[0]) + int(lb[0].split('shortest solution ')[1].split(' ')[0])
    ok = n <= 8
    return ok, ['%s g3 required route: %d moves in all (practice + basin; rating 4 allows 8)' % ('  ' if ok else 'FAIL', n)]


CHECKS = []
EXTRA = [practice, basin, budget]

ROOMS = {
    'g3_practice': dict(name='The practice lock', map=170, start=[11, 13, 8], home=False,
                        reset=dict(switches={S_PRACTICE_GATE: False, S_PRACTICE_HIGH: False}, vars={V_PRACTICE: 0}),
                        solved=dict(switches={S_PRACTICE_GATE: True, S_PRACTICE_HIGH: True}, vars={V_PRACTICE: PRACTICE_PIER}),
                        hints=["Water lifts what floats. Current takes what's loose. Raise it and watch where the raft ends up.",
                               "A shut gate stops what's drifting. The pier is just this side of the gate.",
                               "Shut the gate with the lever, then turn the wheel: the raft drifts to the gate and lies against the pier."]),
    'g3_basin': dict(name='The basins', map=None, start=[14, 21, 8], home=False,
                     reset=dict(switches={S_GATE: False}, vars={V_RAFT: 0}),
                     solved=dict(switches={S_GATE: True}, vars={V_RAFT: 1}),
                     hints=["Same rules as the practice lock. High water takes the raft inland; low water winds it home.",
                            "Ma shuts the gate when she wants a boat to stop halfway: at the island.",
                            "Raise to mid, cross the raft to the west pier and shut the gate. Raise to high: the raft parks at the "
                            "island. Lower to mid, cross to the island, turn wheel C to high and ride the Race north."]),
}
