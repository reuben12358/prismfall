#!/usr/bin/env python3
"""Writes specs/150_pell_playhouse.yaml (Gym 2, rooms 150-154) from design/GYM_PUZZLES.md 'Gym 2' (Revision 10 rewrite):
the revolving stage whose marks never move.  Layouts and logic come from mapgen/puzzles/g2.py (the grids the solver
proves); painted on tileset 54 "PF Rejuv Halls" (Rejuvenation's Goldenleaf Theatre tiles) with layouts/hallkit.py.
Edit this script, then run build.py."""
import os, sys
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'layouts'))
FIELD_RULE = 'setBattleRule("field", :GRAND_STAGE)'
M = {'MapPosition': [0, 10, 25]}


def head(mid, name, parent, extra=None):
    d = {'id': mid, 'name': name, 'parent': parent, 'biome': 'interior', 'bgm': 'Gym', 'field': 'GRAND_STAGE', 'metadata': M}
    d.update(extra or {})
    return d


def trainer(at, ttype, name, sight, d, intro, after, cond=None):
    e = {'type': 'trainer', 'at': list(at), 'sight': sight, 'dir': d, 'sprite': 'trainer_' + ttype,
         'trainer': [ttype, name], 'intro': intro, 'after': after, 'rules': [FIELD_RULE]}
    if cond: e['cond'] = cond
    return e


def sign(name, at, text, tile=None):
    pg = {'commands': [text] if isinstance(text, str) else text}
    if tile: pg['graphic'] = {'tile': tile}
    return {'type': 'event', 'name': name, 'at': list(at), 'pages': [pg]}


def main():
    import hallkit as K
    from puzzles import g2
    CU, MG, MI = K.CU, K.MG, K.MI
    docs = []
    # ---------------------------------------------------------------- 150 Foyer (TEACH: hit your mark)
    A = g2.FOYER_AT
    cls = {'#': 'void', 'W': 'wall', 'D': 'stair'}
    cls.update({c: 'floor2' for c in '.hx1'})
    rows = [r for r in g2.FOYER]
    h = K.Hall(rows, 'stage', cls, seed=150)
    for y, r in enumerate(rows):                         # the rope post's box: low plinths, not holes in the floor
        for x, ch in enumerate(r):
            if ch == '#' and 0 < y < len(rows) - 1 and 0 < x < 18 and all(rows[y + dy][x + dx] not in '#W' or (dx, dy) == (0, 0) for dx, dy in ((0, 1), (0, -1)) if 0 <= y + dy < len(rows)) :
                pass
    for x, y in ((4, 5), (5, 6), (4, 7)):
        h.put(MG(4702), x, y, 0); h.put(MG(4489), x, y, 1)
    mx, my = A['mark']; h.put(CU('mark'), mx, my, 1)
    h.obj('door_mg', 3, 2); h.obj('door_mg', 13, 2); h.obj('mat_mg', 8, 12)
    for x in (1, 17): h.put(MG(4683), x, 10, 2); h.put(MG(4691), x, 11, 1)
    ev = [{'type': 'exit', 'at': list(A['exit']), 'link': 'SM_GYM', 'se': 'Door exit'}]
    for x in (8, 9, 10):
        ev.append(K.tile_event('Curtain h %d' % x, x, 4, [(None, MG(4689)), ({'var': ['GYM2_OVERTURE', 1]}, None)]))
    ev += [
        {'type': 'event', 'name': 'Cue: Overture', 'at': list(A['rope']), 'pages': [{'graphic': {'tile': CU('post_gold')}, 'commands': [
            {'se': 'Door exit'}, {'script': 'pbSet(%d, 1 - pbGet(%d))\n$game_map.need_refresh = true' % (g2.V_OVERTURE, g2.V_OVERTURE)},
            {'if': 'pbGet(%d) == 1' % g2.V_OVERTURE, 'then': ['Cue: Overture! The curtain flies out.'], 'else': ['Cue: curtain. It drops back in.']}]}]},
        {'type': 'npc', 'name': 'Usher', 'at': list(A['usher']), 'sprite': 'trainer_GENTLEMAN', 'dir': 'down', 'commands': [
            "Usher: Ah, our understudy! Tonight's play is The Gilded King.",
            "Usher: On this stage, darling, the scenery moves and the marks don't. Call a cue from anywhere but your mark and "
            "you'll be wearing a forest."]},
        sign('The Script', A['script'], 'The Script, on a lectern: "Act I, the Shipwreck. Act II, the Forest. Act III, the Throne. Places, understudy."', CU('post_silk')),
        K.apprentice('Wren', 'NPC 03', A['wren'][0], A['wren'][1], 'g2_foyer', "Stagehand Wren. Missed your cue? I can strike the set."),
        {'type': 'npc', 'name': 'Lady', 'at': list(A['lady']), 'sprite': 'NPC 11', 'dir': 'up',
         'text': "I come every night. Every. Night. He's never done the Throne act the same way twice."},
        {'type': 'warp', 'name': 'Auditorium doors', 'at': list(A['stair']), 'to': {'map': 151, 'x': 12, 'y': 18, 'dir': 'up'}}]
    d = head(150, 'Pell Playhouse - Foyer', 147); d.update(h.write(150)); d['events'] = ev; docs.append(d)

    # ---------------------------------------------------------------- 151 Revolving Stage (TWIST: three scenes, in order)
    A = g2.STAGE_AT
    S = g2.STAGE
    cls = {'#': 'void', 'W': 'wall', 'D': 'stair', 'v': 'pit', 'S': 'pit', 'F': 'pit', 'T': 'pit', 'C': 'pit'}
    h = K.Hall(S, 'stage', cls, seed=151)
    for y, r in enumerate(S):
        for x, ch in enumerate(r):
            if y >= 16 and ch not in '#': h.put(MG(4702), x, y, 0)                 # the house: carpet
            if y == 14 and ch in 'vSFT': h.put(MG(4489), x, y, 0)                  # the stage front over the orchestra pit
            if ch == 'x': h.put(CU('mark'), x, y, 1)
            if ch in 'LK': h.put(MG(3151), x, y, 1)
    h.obj('mat_mg', 11, 18)
    for x in (4, 5, 6, 7, 14, 15, 16, 20, 21, 22):                                   # front-row seats along the back wall of the house
        pass
    DROP = {'s': ('ship', 1), 'f': ('forest', 2), 't': ('throne', 3)}
    BRIDGE = {'S': ('gangplank', 1), 'F': ('log', 2), 'T': ('dais', 3)}
    ev = []
    for y, r in enumerate(S):
        for x, ch in enumerate(r):
            if ch in DROP:
                n, k = DROP[ch]
                ev.append(K.tile_event('%s %d,%d' % (ch, x, y), x, y, K.exact('GYM2_SCENE', k, CU('drop_' + n), 3)))
            elif ch in BRIDGE:
                n, k = BRIDGE[ch]
                ev.append(K.tile_event('%s %d,%d' % (ch, x, y), x, y, K.exact('GYM2_SCENE', k, CU(n), 3)))
            elif ch in 'AB':
                ev.append(K.tile_event('%s %d,%d' % (ch, x, y), x, y, [(None, CU('flat_' + ch)), ({'switch': 'GYM2_FLAT_' + ch}, None)]))
            elif ch == 'C':
                ev.append(K.tile_event('C %d,%d' % (x, y), x, y, [(None, CU('rostrum')), ({'switch': 'GYM2_FLAT_C'}, None)]))
            elif ch in '123':
                n = int(ch); scene = g2.SCENES[n]
                mark = [c for c in g2.find(S, 'x') if abs(c[0] - x) + abs(c[1] - y) == 1][0]
                ev.append({'type': 'event', 'name': 'Rope %d' % n, 'at': [x, y], 'pages': [{'graphic': {'tile': CU('post_' + ('silk', 'red', 'green', 'gold')[n])}, 'commands': [
                    {'if': '[$game_player.x, $game_player.y] != [%d, %d]' % mark, 'then': [
                        {'script': 'pfp_fail(:g2_stage, "You can\'t call a cue from here: the rope only reaches the painted mark.")'}],
                     'else': [{'if': 'pbGet(%d) == %d' % (g2.V_SCENE, n), 'then': ['The stage is already set for %s.' % scene], 'else': [
                         {'var': [g2.V_SCENE, n]}, {'se': 'Door exit'}, {'raw': [225, [2, 8, 12]]}, {'wait': 12},
                         'Cue: %s! The revolve groans round, and the whole set changes.' % scene]}]}]}]})
            elif ch in 'LK':
                lx, ly = g2.find(g2.LOFT, ch)[0]
                ev.append({'type': 'warp', 'name': 'Ladder %s' % ch, 'at': [x, y], 'to': {'map': 152, 'x': lx, 'y': ly + 1, 'dir': 'down'}})
    ev += [
        {'type': 'warp', 'name': 'Upstage door', 'at': list(A['goal']), 'to': {'map': 154, 'x': 9, 'y': 11, 'dir': 'up'}},
        {'type': 'warp', 'name': 'To Foyer', 'at': list(A['exit']), 'to': {'map': 150, 'x': 9, 'y': 3, 'dir': 'down'}},
        K.apprentice('Pip', 'NPC 07', A['pip'][0], A['pip'][1], 'g2_stage', "Stage manager Pip. I can strike the whole set, loft and all, back to work lights."),
        trainer(A['ferdie'], 'JUGGLER', 'Florian', 2, 'right', "Act One! I drown beautifully. Watch!", "Glub.", cond={'var': ['GYM2_SCENE', 1]}),
        trainer(A['rosalind'], 'BEAUTY', 'Rosalind', 2, 'right', "Act Two: the Forest. I play a tree with opinions.", "Timber.", cond={'var': ['GYM2_SCENE', 2]}),
        trainer(A['crewe'], 'JUGGLER', 'Ambrose', 2, 'left', "Act Three! Kneel before the Gilded King's understudy's understudy!", "Long live... you, I suppose.",
                cond={'var': ['GYM2_SCENE', 3]})]
    d = head(151, 'Pell Playhouse - Revolving Stage', 150); d.update(h.write(151)); d['events'] = ev; docs.append(d)

    # ---------------------------------------------------------------- 152 Fly Loft (COMBINE: a flat is in one place at a time)
    B = g2.LOFT_AT
    Lf = g2.LOFT
    h = K.Hall(Lf, 'stage', {'#': 'void', 'W': 'wall'}, seed=152)
    ev = []
    FL = {1: 'A', 2: 'B and C', 3: 'A and C'}
    for y, r in enumerate(Lf):
        for x, ch in enumerate(r):
            if ch in 'abc':
                ev.append(K.tile_event('%s %d,%d' % (ch, x, y), x, y, [(None, None), ({'switch': 'GYM2_FLAT_' + ch.upper()}, CU('flat_%s_hung' % ch.upper()))]))
            elif ch in '123':
                n = int(ch)
                sc = '\n'.join('pfp_flip(%d)' % (g2.S_A + i) for i in g2.ROPE_FLATS[n])
                ev.append({'type': 'event', 'name': 'Loft rope %d %s' % (n, 'L' if x < 12 else 'R'), 'at': [x, y], 'pages': [{'graphic': {'tile': CU('post_' + ('red', 'green', 'gold')[n - 1])}, 'commands': [
                    {'se': 'Door exit'}, {'script': sc},
                    'Counterweight rope %d: flat%s. Whatever was on the stage flies up here, and whatever hung here drops back in.' % (n, (' ' + FL[n]) if n == 1 else ('s ' + FL[n]))]}]})
            elif ch in 'LK':
                sx, sy = g2.find(S, ch)[0]
                h.put(MG(3151), x, y, 1)
                ev.append({'type': 'warp', 'name': 'Ladder %s' % ch, 'at': [x, y], 'to': {'map': 151, 'x': sx, 'y': sy + 1, 'dir': 'down'}})
    tx, ty = B['trap']
    h.put(MI(962), tx, ty, 1)
    ev += [
        {'type': 'warp', 'name': 'Trapdoor', 'at': [tx, ty], 'to': {'map': 153, 'x': g2.TRAP_AT['start'][0] + g2.TRAP_OFF[0], 'y': g2.TRAP_AT['start'][1] + g2.TRAP_OFF[1], 'dir': 'up'}},
        {'type': 'item', 'at': list(B['item']), 'item': 'SUPERPOTION'},
        K.apprentice('Dot', 'NPC 03', B['dot'][0], B['dot'][1], 'g2_loft', "Dot. Flyman. Flywoman. I can drop every flat back onto the stage if you've boxed yourself in."),
        trainer(B['juggler'], 'GENTLEMAN', 'Reginald', 2, 'down', 'The finest seats in the house are up here. Shall we?', 'Bravo. Mind the ropes.')]
    d = head(152, 'Pell Playhouse - Fly Loft', 150); d.update(h.write(152)); d['events'] = ev; docs.append(d)

    # ---------------------------------------------------------------- 153 The Trap Room (MASTERY: ride the revolve)
    T = g2.TRAP_AT; ox, oy = g2.TRAP_OFF
    rows = [['#'] * 20 for _ in range(15)]
    for y, r in enumerate(g2.TRAP):
        for x, ch in enumerate(r): rows[y + oy][x + ox] = '.' if ch in '.@o*' else '#'
    x0, y0, n = g2.TABLE
    for y in range(y0, y0 + n):
        for x in range(x0, x0 + n): rows[y + oy][x + ox] = '.'
    rows[T['chest'][1] + oy][T['chest'][0] + ox] = '.'
    rows = [''.join(r) for r in rows]
    h = K.Hall(rows, 'stage', {'#': 'void'}, seed=153)
    ev = []
    for y in range(y0, y0 + n):
        for x in range(x0, x0 + n):
            if (x, y) == T['crank']: continue
            pages = [(None, CU('gear') if g2.table_solid(x, y, 0) else None)]
            for rot in (1, 2, 3): pages.append(({'var': ['GYM2_TURNTABLE', rot]}, CU('gear') if g2.table_solid(x, y, rot) else None))
            ev.append(K.tile_event('Table %d,%d' % (x, y), x + ox, y + oy, pages))
    cx, cy = T['crank'][0] + ox, T['crank'][1] + oy
    ev += [
        {'type': 'event', 'name': 'Crank', 'at': [cx, cy], 'pages': [{'graphic': {'tile': CU('post_brass')}, 'commands': [
            {'se': 'Door exit'}, {'raw': [225, [2, 8, 10]]},
            {'script': 'pfp_cycle(%d, 4)\npfp_turntable_ride(%d, %d)' % (g2.V_TURN, cx, cy)},
            "You lean on the crank. The whole floor, and you with it, swings a quarter-turn."]}]},
        {'type': 'event', 'name': 'Prop chest', 'at': [T['chest'][0] + ox, T['chest'][1] + oy], 'pages': [
            {'graphic': {'sprite': 'Object ball'}, 'commands': [
                {'script': 'pfm_item(:MAGICALSEED, 2, "Magical Seed")'}, {'script': 'pfm_item(:PPUP, 1, "PP Up")'},
                "Under the seeds: a dented prop crown. \"THE GILDED KING - Act III\".", {'script': 'pfm_set(:gilded_crown)'},
                {'switch': [g2.S_TRAP, True]}, {'selfswitch': ['A', True]}]},
            {'cond': {'self': 'A'}}]},
        K.apprentice('Old Joss', 'NPC 11', T['joss'][0] + ox, T['joss'][1] + oy, 'g2_trap', "Old Joss. I built the revolve. Dizzy? I'll wind it back."),
        {'type': 'warp', 'name': 'Ladder up', 'at': [T['ladder'][0] + ox, T['ladder'][1] + oy], 'to': {'map': 152, 'x': tx, 'y': ty + 1, 'dir': 'down'}}]
    h.put(MG(3151), T['ladder'][0] + ox, T['ladder'][1] + oy, 1)
    d = head(153, 'Pell Playhouse - The Trap Room', 150); d.update(h.write(153)); d['events'] = ev; docs.append(d)

    # ---------------------------------------------------------------- 154 The Grand Stage (arena)
    AR = ["####################", "#WWWWWWWWWWWWWWWWWW#", "#WWWWWWWWWWWWWWWWWW#"] + ["#..................#"] * 5 + ["#aaaaaaaaDDaaaaaaaa#"] + \
         ["#,,,,,,,,,,,,,,,,,,#"] * 4 + ["#########,##########", "####################"]
    h = K.Hall(AR, 'stage', {'#': 'void', 'W': 'wall', 'a': 'void', 'D': 'stair', ',': 'floor2'}, seed=154)
    for x in range(1, 19):
        if AR[8][x] == 'a': h.put(MG(4489), x, 8, 0)
        h.put(MG(4681), x, 1, 1); h.put(MG(4689), x, 2, 1)                              # the house curtain, flown up against the back wall
    for x in (2, 3, 4, 5, 6, 12, 13, 14, 15, 16, 17):
        for y in (10, 11):
            h.put(MG(4683), x, y - 1, 2); h.put(MG(4691), x, y, 1)
    win = ['Dorian Pell: Bravo! BRAVO! The house is on its feet!',
           {'script': 'Prismfall.award_badge(2)'},
           {'script': 'pbReceiveItem(:TM42)'},
           "Dorian Pell: Facade - the art of turning a bad night into a standing ovation.",
           {'if': 'pfm?(:gilded_crown)', 'then': ["Dorian Pell: You found the old crown! Keep it. Every understudy should own one thing that doesn't fit."]},
           "Dorian Pell: And one more gift, from the whole troupe. Forty auditions, never cast. You two are a matched set.",
           {'script': 'pkmn = Pokemon.new(:EEVEE, 10)\npkmn.name = "Understudy"\npbAddPokemon(pkmn)'},
           {'switch': ['CH3_UNDERSTUDY_GOT', True]},
           "Dorian Pell: Opening night of the Pageant is at the Hall. Come. Bring Juno. Bring everyone.",
           {'selfswitch': ['A', True]}]
    audience = [{'type': 'npc', 'name': 'Audience %d' % i, 'at': [x, y], 'sprite': spr, 'dir': 'up', 'text': line} for i, (x, y, spr, line) in enumerate([
        (8, 10, 'NPC 03', 'Ooh, a new face!'), (10, 10, 'NPC 11', 'Dorian never loses gracefully. He wins gracefully.'),
        (7, 12, 'NPC 07', 'Is it a comedy or a tragedy tonight?')])]
    ev = [{'type': 'warp', 'name': 'To the stage door', 'at': [9, 13], 'to': {'map': 151, 'x': 12, 'y': 4, 'dir': 'down'}},
          {'type': 'event', 'name': 'Dorian', 'at': [9, 4], 'pages': [
              {'graphic': {'sprite': 'trainer_GENTLEMAN', 'dir': 'down'}, 'commands': [
                  'Dorian Pell: Enter, stage left, our brave challenger! You performed the whole of The Gilded King to get here. Did you notice?',
                  "Dorian Pell: The stage tells the truth the throne won't. A duet, then - two by two!",
                  {'script': 'setBattleRule("double")'},
                  {'if': 'Prismfall.gym_battle(2)', 'then': win}]},
              {'cond': {'self': 'A'}, 'graphic': {'sprite': 'trainer_GENTLEMAN', 'dir': 'down'},
               'commands': ['Dorian Pell: The Pageant, darling! The Hall, tonight!']}]}] + audience
    d = head(154, 'Pell Playhouse - The Grand Stage', 150); d.update(h.write(154)); d['events'] = ev; docs.append(d)

    with open(os.path.join(HERE, 'specs', '150_pell_playhouse.yaml'), 'w') as f:
        f.write('# GENERATED by gen_gym2.py from design/GYM_PUZZLES.md + mapgen/puzzles/g2.py (Gym 2 on tileset 54). Edit the script, then run build.py.\n')
        yaml.safe_dump_all(docs, f, sort_keys=False, allow_unicode=True, width=120)
    print('wrote specs/150_pell_playhouse.yaml')


if __name__ == '__main__':
    main()
