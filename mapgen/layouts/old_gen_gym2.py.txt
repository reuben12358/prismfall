#!/usr/bin/env python3
"""Writes specs/150_pell_playhouse.yaml (Gym 2, rooms 150-154) from design/GYM_PUZZLES.md 'Gym 2'
and story/04_ACT_I.md Chapter 3. Edit this script, then run build.py."""
import os
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
# flags.yaml gym-2 block (variables / switches 310-314)
V_SCENE, V_ACTS, V_S1, V_S2, V_S3 = 310, 311, 312, 313, 314
S_LADDER, S_MASK, S_TRAP, S_SPOTS = 'GYM2_LADDER', 'GYM2_MASK', 'GYM2_TRAP', 'GYM2_SPOTS_SET'
ACTORS = [('JUGGLER', 'Florian'), ('BEAUTY', 'Rosalind'), ('JUGGLER', 'Ambrose')]
SCENES = ['the Shipwreck', 'the Forest', 'the Throne']


def room(W, H, floor_rect, extra=()):
    g = [['#'] * W for _ in range(H)]
    x0, y0, w, h = floor_rect
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            g[y][x] = '.'
    for (x0, y0, w, h, c) in extra:
        for y in range(y0, y0 + h):
            for x in range(x0, x0 + w):
                g[y][x] = c
    return '\n'.join(''.join(r) for r in g)


def revolving_stage():
    W, H = 25, 19
    grid = room(W, H, (1, 2, 23, 16), [(4, 4, 17, 10, '_'), (12, 18, 1, 1, '.'), (12, 1, 1, 1, '.')])
    ev = []
    # set pieces: which columns of row 9 are blocked in each scene (1 Shipwreck, 2 Forest, 3 Throne)
    blocked = {1: set(range(4, 11)) | set(range(14, 21)), 2: set(range(4, 16)), 3: set(range(9, 21))}
    for x in range(4, 21):
        pages = [{}]
        for k in (1, 2, 3):
            pg = {'cond': {'var': ['GYM2_SCENE', k]}}
            if x in blocked[k]:
                pg['graphic'] = {'tile': 436}
            pages.append(pg)
        ev.append({'type': 'event', 'name': 'Set piece %d' % x, 'at': [x, 9], 'pages': pages})
    for i, y in enumerate((5, 7, 9)):
        ev.append({'type': 'event', 'name': 'Lamp %s' % ('I' * (i + 1)), 'at': [1, y], 'pages': [
            {'commands': ['A stage lamp, dark.']},
            {'cond': {'var': ['GYM2_ACTS', i + 1]}, 'graphic': {'sprite': 'Object ball'},
             'commands': ['Act %s is lit.' % ('I' * (i + 1))]}]})
    wheel = '''s = pbGet(%d) %% 3 + 1
pbSet(%d, s)
$game_map.need_refresh = true
names = ["", "the Shipwreck", "the Forest", "the Throne"]
pbMessage(_INTL("The stage turns... the set is now {1}.", names[s]))
acts = pbGet(%d)
if s == acts + 1
  key = [@map_id, @event_id, ["B", "C", "D"][s - 1]]
  if $game_self_switches[key]
    pbMessage(_INTL("The actor from Act {1} steps out and bows. A lamp flares.", s))
  else
    actors = [[:JUGGLER, "Florian"], [:BEAUTY, "Rosalind"], [:JUGGLER, "Ambrose"]]
    pbMessage(_INTL("Act {1}! An actor strides onstage to perform against you!", s))
    if TrainerBattle.start(actors[s - 1][0], actors[s - 1][1])
      $game_self_switches[key] = true
    end
  end
  pbSet(%d, s) if $game_self_switches[key]
  if pbGet(%d) >= 3 && !$game_switches[@@GYM2_LADDER]
    $game_switches[@@GYM2_LADDER] = true
    pbMessage(_INTL("Applause from the empty seats! Somewhere in the wings, a ladder rattles down."))
  end
else
  pbMessage(_INTL("A voice from the dark: \\"CUT! Wrong scene!\\" The lamps go out."))
  pbSet(%d, 0)
end
$game_map.need_refresh = true''' % (V_SCENE, V_SCENE, V_ACTS, V_ACTS, V_ACTS, V_ACTS)
    ev.append({'type': 'event', 'name': "Stage manager's wheel", 'at': [22, 16], 'pages': [
        {'graphic': {'sprite': 'Object boulder'}, 'commands': [
            'The stage-manager\'s wheel. Turn it?',
            {'choices': ['Turn', 'Leave it'], 'cancel': 2, 'branches': [[{'script': wheel}], []]}]}]})
    ev.append({'type': 'event', 'name': 'Wing ladder', 'at': [2, 2], 'pages': [
        {'commands': ['A ladder to the fly loft, chained up. "Cast only - after the third act."']},
        {'cond': {'switch': S_LADDER}, 'trigger': 'touch', 'commands': [
            {'se': 'Door exit'}, {'transfer': {'map': 152, 'x': 2, 'y': 3, 'dir': 'down'}}]}]})
    ev.append({'type': 'event', 'name': 'Upstage doors', 'at': [12, 1], 'pages': [
        {'commands': ['The upstage doors are painted on. Very convincing.']},
        {'cond': {'switch': S_TRAP}, 'trigger': 'touch', 'commands': [
            {'se': 'Door exit'}, {'transfer': {'map': 153, 'x': 2, 'y': 5, 'dir': 'right'}}]}]})
    ev.append({'type': 'warp', 'name': 'To Foyer', 'at': [12, 18], 'to': {'map': 150, 'x': 6, 'y': 6, 'dir': 'down'}})
    return grid, ev


def fly_loft():
    W, H = 25, 15
    grid = room(W, H, (1, 2, 23, 3), [(1, 5, 23, 10, 'v')])
    ev = [{'type': 'event', 'name': 'Rigging init', 'at': [0, 0], 'pages': [
        {'trigger': 'autorun', 'commands': [{'var': ['GYM2_SPOT2', 1]}, {'var': ['GYM2_SPOT3', 1]},
                                            {'switch': [S_SPOTS, True]}]},
        {'cond': {'switch': S_SPOTS}}]}]
    marks = [(5, 'Hero', 'trainer_YOUNGSTER'), (12, 'King', 'trainer_GENTLEMAN'), (19, 'Beast', 'trainer_BLACKBELT')]
    for x, n, spr in marks:
        ev.append({'type': 'event', 'name': 'Mark %s' % n, 'at': [x, 13], 'pages': [
            {'graphic': {'sprite': spr, 'dir': 'up'}}]})
    check = ('if pbGet(%d) == 2 && pbGet(%d) == 2 && pbGet(%d) == 2 && !$game_switches[@@GYM2_TRAP]\n'
             '  pbSEPlay("Door exit")\n'
             '  pbMessage(_INTL("Every light upon the Beast! The curtain rises - and a trapdoor springs open on the catwalk."))\n'
             '  $game_switches[@@GYM2_TRAP] = true\n'
             'end\n$game_map.need_refresh = true') % (V_S1, V_S2, V_S3)
    turns = {1: [V_S1], 2: [V_S2, V_S3], 3: [V_S3]}   # rigging: spotlight 2 drags spotlight 3 with it
    for i, x in ((1, 6), (2, 12), (3, 18)):
        sc = '\n'.join('pbSet(%d, (pbGet(%d) + 1) %% 3)' % (v, v) for v in turns[i])
        ev.append({'type': 'event', 'name': 'Spotlight %d' % i, 'at': [x, 2], 'pages': [
            {'graphic': {'sprite': 'Object ball'}, 'commands': [
                'Spotlight %d. Swing it to the next mark?' % i,
                {'choices': ['Swing', 'Leave it'], 'cancel': 2, 'branches': [[{'script': sc + '\n' + check}], []]}]}]})
        var = 'GYM2_SPOT%d' % i
        for k, (tx, _, _) in enumerate(marks):   # beam on the stage: shown while the aim == k
            pages = [{'cond': {'var': [var, k]}, 'graphic': {'sprite': 'Object ball'}}] if k else \
                [{'graphic': {'sprite': 'Object ball'}}]
            if k < 2:
                pages.append({'cond': {'var': [var, k + 1]}})
            ev.append({'type': 'event', 'name': 'Beam %d-%d' % (i, k), 'at': [tx + i - 2, 6 + 2 * i],
                       'pages': pages})
    ev.append({'type': 'event', 'name': 'Trapdoor', 'at': [12, 4], 'pages': [
        {}, {'cond': {'switch': S_TRAP}, 'trigger': 'touch', 'commands': [
            {'se': 'Door exit'}, {'transfer': {'map': 153, 'x': 2, 'y': 5, 'dir': 'right'}}]}]})
    ev.append({'type': 'warp', 'name': 'Ladder down', 'at': [2, 3], 'to': {'map': 151, 'x': 2, 'y': 3, 'dir': 'down'}})
    ev.append(trainer((9, 3), 'GENTLEMAN', 'Reginald', 3, 'right',
                      'The finest seats in the house are up here. Shall we?', 'Bravo. Mind the ropes.'))
    ev.append({'type': 'sign', 'at': [22, 2], 'post': False, 'name': 'Script page',
               'text': '"At the curtain, every light upon the Beast."'})
    return grid, ev


def dressing_rooms():
    W, H = 27, 11
    grid = room(W, H, (1, 5, 25, 2))
    doors = [(6, 'Comedy', None), (11, 'Tragedy', ('LADY', 'Odette')), (16, 'Crown', ('JUGGLER', 'Pierrot')),
             (21, 'Fool', None)]
    ev = []
    for x, name, tr in doors:
        if name == 'Comedy':
            cmds = ['A dressing-room door with a smiling mask. "COMEDY."',
                    {'if_switch': [S_MASK, True], 'then': ['The costume is already yours.'],
                     'else': ['"Tonight the truth wears a smile." The right costume!',
                              {'switch': [S_MASK, True]}, {'se': 'Door exit'},
                              'Down the corridor, a lock clicks open.']}]
        elif tr:
            cmds = ['A dressing-room door. "%s."' % name.upper(),
                    {'if_self': ['A', False], 'then': [
                        'An actor bursts out in full costume!',
                        {'if': 'TrainerBattle.start(:%s, "%s")' % tr, 'then': [{'selfswitch': ['A', True]}]}]},
                    'Wrong costume!']
        else:
            cmds = ['A dressing-room door. "FOOL." Inside, only a jester\'s cap on a hook. Wrong costume!']
        ev.append({'type': 'event', 'name': '%s door' % name, 'at': [x, 4], 'pages': [{'commands': cmds}]})
    ev.append({'type': 'warp', 'name': 'To Revolving Stage', 'at': [1, 5], 'to': {'map': 151, 'x': 12, 'y': 2, 'dir': 'down'}})
    ev.append({'type': 'event', 'name': 'Stage door', 'at': [25, 5], 'pages': [
        {'commands': ['Locked. A note: "Costume first, darling."']},
        {'cond': {'switch': S_MASK}, 'trigger': 'touch', 'commands': [
            {'se': 'Door exit'}, {'transfer': {'map': 154, 'x': 6, 'y': 11, 'dir': 'up'}}]}]})
    return grid, ev


def trainer(at, ttype, name, sight, d, intro, after):
    return {'type': 'trainer', 'at': list(at), 'sight': sight, 'dir': d, 'sprite': 'trainer_' + ttype,
            'trainer': [ttype, name], 'intro': intro, 'after': after}


def main():
    docs = []
    docs.append({'id': 150, 'name': 'Pell Playhouse - Foyer', 'parent': 140, 'template': 'gym', 'exit_link': 'SM_GYM',
                 'drop_template_events': ['Brock', 'Trainer(3)', 'Gym Guy'], 'bgm': 'Gym', 'field': 'GRAND_STAGE',
                 'metadata': {'MapPosition': [0, 10, 25]},
                 'events': [
                     {'type': 'npc', 'name': 'Usher', 'at': [7, 12], 'sprite': 'trainer_GENTLEMAN', 'dir': 'down', 'commands': [
                         "Usher: Ah, our understudy! Tonight's play is The Gilded King. Here's your Script.",
                         'The Script reads: "Act I, the Shipwreck. Act II, the Forest. Act III, the Throne. '
                         'At the curtain, every light upon the Beast. Tonight the truth wears a smile."']},
                     {'type': 'warp', 'name': 'To Revolving Stage', 'at': [6, 5],
                      'to': {'map': 151, 'x': 12, 'y': 17, 'dir': 'up'}}]})
    g, e = revolving_stage()
    docs.append({'id': 151, 'name': 'Pell Playhouse - Revolving Stage', 'parent': 150, 'palette': 'gym_rock',
                 'bgm': 'Gym', 'field': 'GRAND_STAGE', 'metadata': {'MapPosition': [0, 10, 25]}, 'map': g, 'events': e})
    g, e = fly_loft()
    docs.append({'id': 152, 'name': 'Pell Playhouse - Fly Loft', 'parent': 150, 'palette': 'gym_rock', 'bgm': 'Gym',
                 'field': 'GRAND_STAGE', 'metadata': {'MapPosition': [0, 10, 25]}, 'map': g, 'events': e})
    g, e = dressing_rooms()
    docs.append({'id': 153, 'name': 'Pell Playhouse - Dressing Rooms', 'parent': 150, 'palette': 'gym_rock',
                 'bgm': 'Gym', 'field': 'GRAND_STAGE', 'metadata': {'MapPosition': [0, 10, 25]}, 'map': g, 'events': e})
    win = ['Dorian Pell: Bravo! BRAVO! The house is on its feet!',
           {'script': 'Prismfall.award_badge(2)'},
           {'script': 'pbReceiveItem(:TM42)'},
           "Dorian Pell: Facade - the art of turning a bad night into a standing ovation.",
           "Dorian Pell: And one more gift, from the whole troupe. Forty auditions, never cast. You two are a matched set.",
           {'script': 'pkmn = Pokemon.new(:EEVEE, 10)\npkmn.name = "Understudy"\npbAddPokemon(pkmn)'},
           {'switch': ['CH3_UNDERSTUDY_GOT', True]},
           "Dorian Pell: Opening night of the Pageant is at the Hall. Come. Bring Juno. Bring everyone.",
           {'selfswitch': ['A', True]}]
    audience = [{'type': 'npc', 'name': 'Audience %d' % i, 'at': [x, y], 'sprite': spr, 'dir': d,
                 'text': line} for i, (x, y, spr, d, line) in enumerate([
                     (1, 4, 'NPC 03', 'right', 'Ooh, a new face!'), (11, 4, 'NPC 11', 'left', 'Dorian never loses gracefully. He wins gracefully.'),
                     (1, 8, 'NPC 07', 'right', 'Is it a comedy or a tragedy tonight?'),
                     (11, 8, 'NPC 25', 'left', 'I come every night. Every. Night.')])]
    docs.append({'id': 154, 'name': 'Pell Playhouse - The Grand Stage', 'parent': 150, 'template': 'arena',
                 'drop_template_events': ['Champion', 'Door', 'Entrance'], 'bgm': 'Gym', 'field': 'GRAND_STAGE',
                 'tile_edits': [[1, 6, 11, 0]],      # open the arena template's front wall at the door (arrival 6,11; playtest)
                 'metadata': {'MapPosition': [0, 10, 25]},
                 'events': [{'type': 'warp', 'name': 'To Dressing Rooms', 'at': [6, 12],
                             'to': {'map': 153, 'x': 24, 'y': 5, 'dir': 'left'}},
                            {'type': 'event', 'name': 'Dorian', 'at': [6, 5], 'pages': [
                                {'graphic': {'sprite': 'trainer_GENTLEMAN', 'dir': 'down'}, 'commands': [
                                    'Dorian Pell: Enter, stage left, our brave challenger!',
                                    "Dorian Pell: The stage tells the truth the throne won't. A duet, then - two by two!",
                                    {'script': 'setBattleRule("double")'},
                                    {'if': 'Prismfall.gym_battle(2)', 'then': win}]},
                                {'cond': {'self': 'A'}, 'graphic': {'sprite': 'trainer_GENTLEMAN', 'dir': 'down'},
                                 'commands': ['Dorian Pell: The Pageant, darling! The Hall, tonight!']}]}] + audience})
    with open(os.path.join(HERE, 'specs', '150_pell_playhouse.yaml'), 'w') as f:
        f.write('# GENERATED by gen_gym2.py from design/GYM_PUZZLES.md (Gym 2). Edit the script, then run build.py.\n')
        yaml.safe_dump_all(docs, f, sort_keys=False, allow_unicode=True, width=120)
    print('wrote specs/150_pell_playhouse.yaml')


if __name__ == '__main__':
    main()
