#!/usr/bin/env python3
"""Writes specs/170_tidelock_gym.yaml (Gym 3, rooms 170-174) from design/GYM_PUZZLES.md 'Gym 3'.
Basins 171 (Low) / 172 (Mid) / 173 (High) are variant maps with identical walls on the Harbour tileset
(Sea autotile water). Sluice wheels move you to the same x,y on another variant; Mid has raft events
(tile graphic = passable plank) out to the bell-rope; High has current lanes (forced moves) and the
north lane only reaches the exit while S315 (tide bell) is ON. Edit this script, then run build.py."""
import os
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 29, 23
LEVEL_MAP = {0: 171, 1: 172, 2: 173}
WHEEL_W, WHEEL_C, WHEEL_E = (3, 20), (14, 10), (25, 20)
ROPE, BELL, EXIT = (4, 4), (14, 3), (14, 0)
S_BELL = 315    # GYM_PUZZLES: S315 flips the current


def basin(level):
    g = [['#'] * W for _ in range(H)]
    def fill(x0, y0, w, h, c):
        for y in range(y0, y0 + h):
            for x in range(x0, x0 + w):
                g[y][x] = c
    fill(1, 1, W - 2, H - 2, '.' if level == 0 else '~')   # basin: mud at Low, water otherwise
    fill(1, 19, W - 2, 3, '.')                             # south walkway (entrance, wheels W and E)
    fill(12, 9, 5, 3, '.')                                 # centre platform (wheel C)
    fill(2, 2, 5, 4, '.')                                  # bell-rope platform (NW)
    fill(12, 1, 5, 3, '.')                                 # exit platform (bell, north door)
    g[0][EXIT[0]] = '.'
    g[22][14] = '.'
    if level == 0:   # Low: drained mud; a rock wall rings the two upper platforms (too high to climb)
        fill(1, 6, 7, 1, 'f'); fill(7, 1, 1, 6, 'f'); fill(11, 4, 7, 1, 'f'); fill(11, 1, 1, 4, 'f'); fill(17, 1, 1, 4, 'f')
    return '\n'.join(''.join(r) for r in g)


def wheel(level, pos, name, delta):
    x, y = pos
    target = (level + delta) if delta in (-1, 1) else (2 if level == 0 else 0 if level == 2 else None)
    if target is None or not (0 <= target <= 2):
        msg = {'W': 'The water is as low as it goes.', 'E': 'The water is as high as it goes.',
               'C': 'Wheel C only swings between low and high water.'}[name]
        return {'type': 'event', 'name': 'Wheel %s' % name, 'at': [x, y], 'pages': [
            {'graphic': {'sprite': 'Object boulder'}, 'commands': ['Sluice wheel %s. %s' % (name, msg)]}]}
    lvl = ['low', 'mid', 'high'][target]
    return {'type': 'event', 'name': 'Wheel %s' % name, 'at': [x, y], 'pages': [
        {'graphic': {'sprite': 'Object boulder'}, 'commands': [
            'Sluice wheel %s. Turn it?' % name,
            {'choices': ['Turn it', 'Leave it'], 'cancel': 2, 'branches': [[
                {'se': 'Door exit'}, {'tone': [-255, -255, -255, 0, 10]}, {'wait': 10},
                {'transfer': {'map': LEVEL_MAP[target], 'x': x, 'y': y - 1, 'dir': 'up'}},
                {'tone': [0, 0, 0, 0, 10]}, 'The basins roar - the water is %s now.' % lvl], []]}]}]}


def current(at, steps, direction, name, cond_switch=None, back=None):
    """Player-touch lane entry: carries the player `steps` tiles. With cond_switch, flows only when it is ON
    (otherwise pushes the player `back` tiles the other way)."""
    ride = [{'move': {'who': -1, 'route': ['through_on'] + ['%s %d' % (direction, steps)] + ['through_off']}}]
    if cond_switch:
        opp = {'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'}[direction]
        cmds = [{'if_switch': [cond_switch, True], 'then': [{'se': 'Door exit'}] + ride,
                 'else': ['The current here runs the wrong way! It shoves you back.',
                          {'move': {'who': -1, 'route': ['turn_%s' % opp]}}]}]
    else:
        cmds = [{'se': 'Door exit'}] + ride
    return {'type': 'event', 'name': name, 'at': list(at), 'pages': [{'trigger': 'touch', 'commands': cmds}]}


def trainer(at, ttype, name, d, intro, after):
    return {'type': 'trainer', 'at': list(at), 'sight': 3, 'dir': d, 'sprite': 'trainer_' + ttype,
            'trainer': [ttype, name], 'intro': intro, 'after': after}


def main():
    docs = [{'id': 170, 'name': 'Tidelock Gym - Lock Hall', 'parent': 160, 'template': 'gym', 'exit_link': 'EB_GYM',
             'drop_template_events': ['Brock', 'Trainer(3)', 'Gym Guy'], 'bgm': 'Gym', 'field': 'WATER_SURFACE',
             'metadata': {'MapPosition': [0, 8, 20]},
             'events': [
                 {'type': 'npc', 'name': 'Lock-keeper', 'at': [7, 12], 'sprite': 'NPC 25', 'dir': 'down', 'commands': [
                     "Lock-keeper: Three sluice wheels. West drops the water, east raises it, the centre one swings low to high.",
                     "Lock-keeper: And the tide bell turns the current. The Ebb runs both ways - so does this gym."]},
                 trainer((3, 9), 'FISHERMAN', 'Gunnar', 'right', "Mind the locks! And my line!", "Marisol learned to swim in these basins."),
                 {'type': 'warp', 'name': 'To the Basins', 'at': [6, 5], 'to': {'map': 171, 'x': 14, 'y': 21, 'dir': 'up'}}]}]
    for level in (0, 1, 2):
        mid = LEVEL_MAP[level]
        ev = [wheel(level, WHEEL_W, 'W', -1), wheel(level, WHEEL_C, 'C', 0), wheel(level, WHEEL_E, 'E', 1),
              {'type': 'warp', 'name': 'To Lock Hall', 'at': [14, 22], 'to': {'map': 170, 'x': 6, 'y': 6, 'dir': 'down'}}]
        if level == 0:
            for x, y in ((6, 12), (9, 15), (20, 13), (23, 8), (18, 16)):
                ev.append({'type': 'event', 'name': 'Rock %d,%d' % (x, y), 'at': [x, y], 'pages': [
                    {'graphic': {'sprite': 'Object rock'}, 'commands': ['A slick boulder, crusted with river-weed.']}]})
            ev.append(trainer((10, 17), 'SWIMMER_F', 'Ingrid', 'left', 'Low water means mud-wrestling!', 'I need a bath.'))
        if level == 1:   # rafts from the south walkway up the west side to the bell-rope platform
            for y in range(6, 19):
                ev.append({'type': 'event', 'name': 'Raft %d' % y, 'at': [4, y], 'pages': [{'graphic': {'tile': 457}}]})
            ev.append({'type': 'event', 'name': 'Bell-rope', 'at': list(ROPE), 'pages': [
                {'graphic': {'sprite': 'Object ball'}, 'commands': [
                    'A rope runs up into the dark, to the tide bell.',
                    {'choices': ['Pull it', 'Leave it'], 'cancel': 2, 'branches': [[
                        {'se': 'Door exit'},
                        {'if_switch': [S_BELL, True],
                         'then': [{'switch': [S_BELL, False]}, 'DONG. Somewhere above, the currents swing back toward the sea.'],
                         'else': [{'switch': [S_BELL, True]}, 'DONG. Somewhere above, the currents turn and run inland - north.']}],
                        []]}]}]})
            ev.append(trainer((5, 3), 'SWIMMER_M', 'Leif', 'down', 'Rafting is cheating! Battle!', 'Fine. The bell is yours.'))
            ev.append(trainer((13, 20), 'FISHERMAN', 'Oskar', 'right', 'Mid-water! Best fishing level!', 'Not a nibble.'))
        if level == 2:
            ev.append(current((14, 18), 6, 'up', 'Current to centre'))                 # south walkway -> centre platform
            ev.append(current((14, 8), 5, 'up', 'North current', cond_switch=S_BELL))  # centre -> exit platform
            ev.append({'type': 'event', 'name': 'Tide bell', 'at': list(BELL), 'pages': [
                {'graphic': {'sprite': 'Object ball'}, 'commands': [
                    'The tide bell. Ring it?',
                    {'choices': ['Ring it', 'Leave it'], 'cancel': 2, 'branches': [[
                        {'se': 'Door exit'},
                        {'if_switch': [S_BELL, True], 'then': [{'switch': [S_BELL, False]}, 'DONG. The currents swing seaward.'],
                         'else': [{'switch': [S_BELL, True]}, 'DONG. The currents run inland.']}], []]}]}]})
            ev.append({'type': 'warp', 'name': "To the Warden's Pool", 'at': list(EXIT), 'link': 'EBG_2',
                       'to': {'map': 174, 'x': 9, 'y': 15, 'dir': 'up'}})
            ev.append(trainer((16, 2), 'SAILOR', 'Bjorn', 'left', 'Top of the tide! Show me your sea legs!', 'Marisol rides the Ebb itself, you know.'))
        docs.append({'id': mid, 'name': 'Tidelock Gym - Basins (%s Water)' % ['Low', 'Mid', 'High'][level], 'parent': 170,
                     'palette': 'harbour', 'bgm': 'Gym', 'field': 'WATER_SURFACE', 'metadata': {'MapPosition': [0, 8, 20]},
                     'map': basin(level), 'events': ev})
    pool = [['#'] * 19 for _ in range(17)]
    for y in range(2, 16):
        for x in range(1, 18):
            pool[y][x] = '~' if (3 <= x <= 15 and 4 <= y <= 11) else '.'
    for y in range(6, 10):
        for x in range(7, 12):
            pool[y][x] = '.'
    pool[16][9] = '.'
    win = ["Marisol Reyes: Ha! You rode it both ways. Good.",
           {'script': 'Prismfall.award_badge(3)'}, {'script': 'pbReceiveItem(:TM03)'},
           "Marisol Reyes: Water Pulse. It hits like a wave and leaves them dizzy.",
           "Later, over smoked eel on the quay:",
           "Marisol Reyes: Meridian pays my people. Meridian's killing my river. Pick one, kid, I dare you.",
           {'selfswitch': ['A', True]}]
    docs.append({'id': 174, 'name': "Tidelock Gym - Warden's Pool", 'parent': 170, 'palette': 'harbour', 'bgm': 'Gym',
                 'field': 'WATER_SURFACE', 'metadata': {'MapPosition': [0, 8, 20]},
                 'map': '\n'.join(''.join(r) for r in pool),
                 'events': [{'type': 'warp', 'name': 'Back to the Basins', 'at': [9, 16], 'link': 'EBG_2',
                             'to': {'map': 173, 'x': 14, 'y': 1, 'dir': 'down'}},
                            {'type': 'event', 'name': 'Marisol', 'at': [9, 7], 'pages': [
                                {'graphic': {'sprite': 'trainer_SWIMMER_F', 'dir': 'down'}, 'commands': [
                                    "Marisol Reyes: The Ebb runs both ways. Always has. Lately it can't decide.",
                                    "Marisol Reyes: Let's see if you can!",
                                    {'if': 'Prismfall.gym_battle(3)', 'then': win}]},
                                {'cond': {'self': 'A'}, 'graphic': {'sprite': 'trainer_SWIMMER_F', 'dir': 'down'},
                                 'commands': ["Marisol Reyes: Go on. The river's still running. For now."]}]}]})
    with open(os.path.join(HERE, 'specs', '170_tidelock_gym.yaml'), 'w') as f:
        f.write('# GENERATED by gen_gym3.py from design/GYM_PUZZLES.md (Gym 3). Edit the script, then run build.py.\n')
        yaml.safe_dump_all(docs, f, sort_keys=False, allow_unicode=True, width=120)
    print('wrote specs/170_tidelock_gym.yaml')


if __name__ == '__main__':
    main()
