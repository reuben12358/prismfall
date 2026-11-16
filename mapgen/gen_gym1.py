#!/usr/bin/env python3
"""Writes specs/130_loomhouse_gym.yaml (Gym 1, rooms 130-133) from design/GYM_PUZZLES.md 'Gym 1'.
The puzzle events are repetitive, so they are generated here; edit this script, then run build.py."""
import os
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
V_A, V_B, V_C = 305, 306, 307           # heddle variables (gym 1 block 305-309)
S_ALPHA, S_BETA, S_GAMMA = 305, 306, 307  # cord switches for the Canopy Lofts
FIELD_RULE = 'setBattleRule("field", :SILKWOOD)'


def grid(rows, w):
    return '\n'.join(r.ljust(w, '#')[:w] for r in rows)


def weaving_hall():
    W, H = 25, 21
    g = [['#'] * W for _ in range(H)]
    def fill(x0, y0, w, h, c):
        for y in range(y0, y0 + h):
            for x in range(x0, x0 + w):
                g[y][x] = c
    fill(1, 1, 23, 19, '.')        # room
    g[0][12] = '.'                 # exit north (to the Canopy Lofts)
    fill(1, 3, 23, 4, 'v')         # gap A
    fill(1, 9, 23, 3, 'v')         # gap B
    fill(1, 14, 23, 4, 'v')        # gap C
    fill(5, 7, 6, 2, 'o')          # silk wall on ledge 2 (between x3 and x12)
    fill(14, 12, 6, 2, 'o')        # silk wall on ledge 1 (between x12 and x21)
    g[20][12] = '.'                # entrance south
    return '\n'.join(''.join(r) for r in g)


def plank_events(var, rows, prefix):
    evs = []
    for k, x in enumerate((3, 12, 21)):
        for y in rows:
            pages = [{'cond': ({'var': [var, k]} if k else None), 'graphic': {'tile': 452}}]
            if pages[0]['cond'] is None:
                del pages[0]['cond']
            if k < 2:
                pages.append({'cond': {'var': [var, k + 1]}})   # later page wins: plank gone
            evs.append({'type': 'event', 'name': '%s plank %d,%d' % (prefix, x, y), 'at': [x, y], 'pages': pages})
    return evs


def lever(name, x, y, a, b, colour):
    script = ('pbSet(%d, (pbGet(%d) + 1) %% 3)\npbSet(%d, (pbGet(%d) + 1) %% 3)\n$game_map.need_refresh = true'
              % (a, a, b, b))
    return {'type': 'event', 'name': name, 'at': [x, y], 'pages': [{'graphic': {'sprite': 'Object ball'}, 'commands': [
        {'se': 'Door exit'}, {'script': script}, 'You pulled the %s heddle. Threads shift somewhere above...' % colour]}]}


def spool(pid, plats, off_to, on_to, sw, label):
    """Player-touch zipline: jumps the player to another platform; destination depends on switch `sw`."""
    cx, cy = plats[pid]
    def ride(dest):
        dx, dy = plats[dest][0] - (cx + 2), plats[dest][1] - cy
        return [{'se': 'Door exit'}, {'move': {'who': -1, 'route': ['through_on', {'jump': [dx, dy]}, 'through_off']}}]
    return {'type': 'event', 'name': 'Spool %s' % label, 'at': [cx + 2, cy], 'pages': [{'trigger': 'touch', 'commands': [
        {'if_switch': [sw, True], 'then': ride(on_to), 'else': ride(off_to)}]}]}


def canopy_lofts():
    W, H = 25, 25
    plats = {1: (2, 22), 2: (12, 20), 3: (4, 12), 4: (19, 14), 5: (12, 6), 6: (20, 3)}
    g = [['v'] * W for _ in range(H)]
    for x in range(W):
        g[0][x] = '#'
    for p, (cx, cy) in plats.items():
        for y in range(cy - 1, cy + 2):
            for x in range(cx - 1, cx + 3):
                g[y][x] = '.'
    evs = []
    # (spool, off destination, on destination, switch)
    evs.append(spool(1, plats, 2, 3, S_ALPHA, 's1'))
    evs.append(spool(2, plats, 4, 1, S_GAMMA, 's2'))
    evs.append(spool(3, plats, 5, 4, S_BETA, 's3'))
    evs.append(spool(4, plats, 2, 6, S_BETA, 's4'))
    evs.append(spool(5, plats, 6, 3, S_GAMMA, 's5'))   # gamma "starts ON" for s5 = un-pulled cord leads to P6
    for name, sw, p in (('alpha', S_ALPHA, 1), ('beta', S_BETA, 3), ('gamma', S_GAMMA, 2)):
        cx, cy = plats[p]
        evs.append({'type': 'event', 'name': 'Cord %s' % name, 'at': [cx - 1, cy - 1], 'pages': [
            {'graphic': {'sprite': 'Object ball'}, 'commands': [
                {'if_switch': [sw, True], 'then': [{'switch': [sw, False]}, 'You let the %s cord go slack.' % name],
                 'else': [{'switch': [sw, True]}, 'You pull the %s cord taut.' % name]}]}]})
    for p in (2, 3, 4, 5):
        cx, cy = plats[p]
        evs.append({'type': 'event', 'name': 'Rope ladder P%d' % p, 'at': [cx - 1, cy + 1], 'pages': [{'commands': [
            'A rope ladder. Climb down to the loft floor?',
            {'choices': ['Yes', 'No'], 'cancel': 2, 'branches': [[
                {'tone': [-255, -255, -255, 0, 8]}, {'wait': 8},
                {'transfer': {'map': 132, 'x': plats[1][0], 'y': plats[1][1], 'dir': 'up'}},
                {'tone': [0, 0, 0, 0, 8]}], []]}]}]})
    evs.append({'type': 'warp', 'name': 'Down to Weaving Hall', 'at': [1, 23], 'to': {'map': 131, 'x': 12, 'y': 1, 'dir': 'down'}})
    evs.append({'type': 'warp', 'name': 'To the Spindle', 'at': [22, 2], 'link': 'GYM1_SPINDLE',
                'to': {'map': 133, 'x': 6, 'y': 11, 'dir': 'up'}, 'arrive': [21, 3, 'down']})
    evs.append({'type': 'item', 'at': [13, 5], 'item': 'SILVERPOWDER'})
    evs.append(trainer((13, 21), 'BUGCATCHER', 'Hollis', 3, 'left'))
    evs.append(trainer((20, 15), 'POKEMONRANGER_M', 'Ash', 3, 'left'))
    return '\n'.join(''.join(r) for r in g), evs


def trainer(at, ttype, name, sight, d):
    return {'type': 'trainer', 'at': list(at), 'sight': sight, 'dir': d, 'sprite': 'trainer_' + ttype,
            'trainer': [ttype, name], 'rules': [FIELD_RULE],
            'intro': '[TODO story] Every thread has its place. Let me show you mine!',
            'after': '[TODO story] The Warden says the loom remembers every knot.'}


def main():
    docs = []
    docs.append({'id': 130, 'name': 'Loomhouse Gym - Foyer', 'parent': 120, 'template': 'gym', 'exit_link': 'BW_GYM',
                 'drop_template_events': ['Brock', 'Trainer(3)', 'Gym Guy'], 'bgm': 'Gym', 'field': 'SILKWOOD',
                 'metadata': {'MapPosition': [0, 12, 22]},
                 'events': [
                     {'type': 'npc', 'name': 'Gym guide', 'at': [7, 12], 'sprite': 'NPC 01', 'dir': 'down', 'commands': [
                         '[TODO story] The Warden weaves her puzzles like cloth. Here, take this pattern card.',
                         'The card reads: "Red lifts the warp and the weft. Gold lifts the weft and the woof. '
                         'Green lifts the woof and the warp."']},
                     {'type': 'warp', 'name': 'To Weaving Hall', 'at': [6, 5], 'link': 'GYM1_HALL',
                      'to': {'map': 131, 'x': 12, 'y': 19, 'dir': 'up'}, 'arrive': [6, 6, 'down']}]})
    hall_events = plank_events(V_A, range(3, 7), 'A') + plank_events(V_B, range(9, 12), 'B') + \
        plank_events(V_C, range(14, 18), 'C')
    hall_events += [lever('Red lever', 3, 18, V_A, V_B, 'red'), lever('Gold lever', 12, 18, V_B, V_C, 'gold'),
                    lever('Green lever', 21, 18, V_C, V_A, 'green'),
                    {'type': 'warp', 'name': 'Back to Foyer', 'at': [12, 20], 'to': {'map': 130, 'x': 6, 'y': 6, 'dir': 'down'}},
                    {'type': 'warp', 'name': 'Up to Canopy Lofts', 'at': [12, 0], 'to': {'map': 132, 'x': 2, 'y': 22, 'dir': 'up'}},
                    trainer((12, 13), 'BUGCATCHER', 'Milo', 3, 'down'),
                    trainer((21, 7), 'LASS', 'Fern', 3, 'down')]
    docs.append({'id': 131, 'name': 'Loomhouse Gym - Weaving Hall', 'parent': 130, 'palette': 'gym_rock', 'bgm': 'Gym',
                 'field': 'SILKWOOD', 'metadata': {'MapPosition': [0, 12, 22]}, 'map': weaving_hall(),
                 'events': hall_events})
    lofts, loft_events = canopy_lofts()
    docs.append({'id': 132, 'name': 'Loomhouse Gym - Canopy Lofts', 'parent': 130, 'palette': 'gym_rock', 'bgm': 'Gym',
                 'field': 'SILKWOOD', 'metadata': {'MapPosition': [0, 12, 22]}, 'map': lofts, 'events': loft_events})
    win = ['Tamsin: ...It held. You held. Granny Loom would have liked you.',
           {'script': 'Prismfall.award_badge(1)'},
           'The badge settles into the case - and the case hums, faintly, as if something inside woke up.',
           {'script': 'pbReceiveItem(:TM89)'},
           'Tamsin: That\'s U-turn. Hit, then get out. ...I wish I were better at the second part.',
           {'var': ['STORY', 9]}, {'selfswitch': ['A', True]}]
    confess = [
        "Tamsin: Can I... tell you something? Not as a Warden. Just as me.",
        "Tamsin: Briarwick is bankrupt. I signed the Lattice contract. Alone. Nobody else knows.",
        "Tamsin: And the Glasswood grows fastest along the Lattice line. Thistle was right.",
        {'choices': ['Tell the village yourself', 'Tell them at the meeting', 'Keep it secret'], 'cancel': 0, 'branches': [
            [{'script': 'pf_choose(:CH2_TAMSIN, :helped)'},
             "Tamsin: ...Myself. Yes. It should be me. Thank you for not making it easy."],
            [{'script': 'pf_choose(:CH2_TAMSIN, :exposed)\npf_standing_add(:MERIDIAN, -1)\npf_standing_add(:ACCORD, 1)'},
             "Tamsin: You'd tell them? ...Then I suppose I can't hide behind the loom any more."],
            [{'script': 'pf_choose(:CH2_TAMSIN, :kept)\npf_standing_add(:MERIDIAN, 1)'},
             "Tamsin: You'd keep it? I... thank you. I'll find a way to fix this. I will."]]},
        "Tamsin: The Glasswood's heart is Cocoonfall Hollow, west of here past Route 3. I can't cross a Veil. You can.",
        "Tamsin: Take Granny's shuttle. For luck.",
        {'var': ['STORY', 10]}, {'selfswitch': ['B', True]}]
    docs.append({'id': 133, 'name': 'Loomhouse Gym - The Spindle', 'parent': 130, 'template': 'arena',
                 'drop_template_events': ['Champion', 'Door', 'Entrance'], 'bgm': 'Gym', 'field': 'SILKWOOD',
                 'metadata': {'MapPosition': [0, 12, 22]},
                 'events': [
                     {'type': 'exit', 'at': [6, 12], 'link': 'GYM1_SPINDLE', 'se': 'Door exit'},
                     {'type': 'event', 'name': 'Tamsin', 'at': [6, 5], 'pages': [
                         {'graphic': {'sprite': 'trainer_LASS', 'dir': 'down'}, 'commands': [
                             'Tamsin: Every thread has to line up. You made it through the loom, so... so now it\'s me.',
                             "Tamsin: Granny Loom wove this room. Don't you dare tear it.",
                             {'if': 'Prismfall.gym_battle(1)', 'then': win}]},
                         {'cond': {'self': 'A'}, 'graphic': {'sprite': 'trainer_LASS', 'dir': 'down'}, 'commands': confess},
                         {'cond': {'self': 'B'}, 'graphic': {'sprite': 'trainer_LASS', 'dir': 'down'}, 'commands': [
                             'Tamsin: The Cutter in town owes me a favour. Tell him I sent you.']}]}]})
    with open(os.path.join(HERE, 'specs', '130_loomhouse_gym.yaml'), 'w') as f:
        f.write('# GENERATED by gen_gym1.py from design/GYM_PUZZLES.md (Gym 1). Edit the script, then run build.py.\n')
        yaml.safe_dump_all(docs, f, sort_keys=False, allow_unicode=True, width=120)
    print('wrote specs/130_loomhouse_gym.yaml')


if __name__ == '__main__':
    main()
