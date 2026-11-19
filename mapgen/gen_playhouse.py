#!/usr/bin/env python3
"""Writes specs/150_pell_playhouse.yaml: the Pell Playhouse, Saltmere (map IDs 150-154).
SPINE Revision 14: this is GYM 1 (Dorian Pell, Normal, Grand Stage, single battle, cap 15).
  150 Lobby       the theatre's foyer: posters, ushers, the gym guide
  154 Auditorium  the gym (rating 1/10, Jasmine-style): up the aisle between the seat rows, past the actors, onto the
                  apron; ONE interaction, the curtain rope; the house curtain flies out and Dorian is on stage
  151-153         PLAYHOUSE BACKSTAGE, an optional dungeon (DUNGEON_PUZZLES D9, after Tamsin's badge): the Revision 10
                  revolving-stage puzzle, whole; entered by the stage-left wing door
Layouts and logic come from mapgen/puzzles/playhouse.py (the grids the solver proves), painted on tileset 54
"PF Rejuv Halls" (Rejuvenation's Goldenleaf Theatre tiles) with layouts/hallkit.py.  Edit this script, run build.py."""
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


def rug(h, MG, x0, y0, w, hh):
    for y in range(y0, y0 + hh):
        r = 0 if y == y0 else (2 if y == y0 + hh - 1 else 1)
        for x in range(x0, x0 + w):
            c = 0 if x == x0 else (2 if x == x0 + w - 1 else 1)
            h.put(MG([[4645, 4646, 4647], [4653, 4654, 4655], [4661, 4662, 4663]][r][c]), x, y, 1)


def main():
    import hallkit as K
    from puzzles import playhouse as P
    CU, MG, MI = K.CU, K.MG, K.MI
    docs = []
    # ---------------------------------------------------------------- 150 Lobby
    A = P.LOBBY_AT
    h = K.Hall(P.LOBBY, 'lobby', {'#': 'void', 'W': 'wall', 'D': 'door'}, seed=150)
    for x in (3, 8, 13, 18):                                          # purple pillars between the wall panels
        for y in (2, 3, 4): h.put(MG(1704), x, y, 0)
    h.obj('poster_rain', 4, 2); h.obj('poster_lady', 14, 2)
    for x in (3, 8, 13, 18): h.obj('urn', x, 5)                      # gilded urns at the pillars' feet, velvet ropes between
    for x0 in (4, 14):
        h.put(MG(1802), x0, 5, 2); h.put(MG(1803), x0 + 1, 5, 2); h.put(MG(1803), x0 + 2, 5, 2); h.put(MG(1804), x0 + 3, 5, 2)
    rug(h, MG, 7, 7, 8, 3)
    h.obj('couch_l', 1, 6); h.obj('couch_r', 20, 6)
    h.obj('urn', 1, 10); h.obj('urn', 20, 10); h.obj('mat_mg', 10, 12)
    ev = [{'type': 'exit', 'at': list(A['exit']), 'link': 'SM_GYM', 'se': 'Door exit'},
          {'type': 'warp', 'name': 'Auditorium doors', 'at': list(A['doors']),
           'to': {'map': 154, 'x': P.THEATRE_AT['start'][0], 'y': P.THEATRE_AT['start'][1], 'dir': 'up'}},
          {'type': 'npc', 'name': 'Usher', 'at': list(A['usher']), 'sprite': 'trainer_GENTLEMAN', 'dir': 'down', 'commands': [
              "Usher: Ah, our challenger! Tonight's bill: Dorian Pell, in person. Through the doors, up the aisle, onto the stage.",
              "Usher: The cast may want a word on your way. Actors. They always want a word."]},
          {'type': 'npc', 'name': 'Gym guide', 'at': list(A['guide']), 'sprite': 'NPC 01', 'dir': 'left', 'commands': [
              "Gym Guide: Your first Warden! Dorian uses Normal-types on the Grand Stage field.",
              "Gym Guide: Here's the trick of a field: the stage loves a show. Flashy moves - sound moves, dances - get a cheer from "
              "the house, and the cheer makes them hit harder. That goes for your side too. Fighting-types are good. Ghosts don't care."]},
          {'type': 'npc', 'name': 'Lady', 'at': list(A['lady']), 'sprite': 'NPC 11', 'dir': 'right',
           'text': "I come every night. Every. Night. He has never once taken a bow the same way twice."},
          sign('Poster: The Gilded King', (5, 4), 'A poster: "THE GILDED KING - closed by order of the Crown." Someone has pasted "TONIGHT" over "closed".'),
          sign('Poster: The Lady in Red', (15, 4), 'A poster: "THE LADY IN RED. Dorian Pell, Rosalind Vane. Held over by popular demand."')]
    d = head(150, 'Pell Playhouse - Lobby', 147); d.update(h.write(150)); d['events'] = ev; docs.append(d)

    # ---------------------------------------------------------------- 154 Auditorium (GYM 1)
    T = P.THEATRE_AT
    rows = P.THEATRE
    cls = {'#': 'void', 'W': 'wall', 'p': 'lip', 'S': 'stair', 's': 'seat', ',': 'floor2'}
    h = K.Hall(rows, 'stage', cls, seed=154)
    for x in range(1, 24):                                           # the backdrop: a red drape across the back wall
        h.put(MG(4681), x, 2, 1); h.put(MG(4689), x, 3, 1)
    for y in range(11, 22):                                          # a velvet runner up the centre aisle
        for x in (11, 12, 13):
            r = 0 if y == 11 else (2 if y == 21 else 1)
            h.put(MG([[4645, 4646, 4647], [4653, 4654, 4655], [4661, 4662, 4663]][r][x - 11]), x, y, 1)
    h.put(MG(3151), T['wing'][0], T['wing'][1], 1)                  # steps down into the stage-left wing
    h.obj('urn', 1, 20); h.obj('urn', 23, 20)
    h.put(MG(1731), 11, 22, 1); h.put(MG(1732), 12, 22, 1); h.put(MG(1733), 13, 22, 1)
    ev = []
    for (x, y) in P.CURTAIN:                                         # the house curtain: in until the rope flies it out
        if (x, y) == T['dorian']: continue                            # Dorian's own event wears the curtain until it flies
        t = MG(4697) if y == P.CURTAIN[-1][1] else MG(4689)
        ev.append(K.tile_event('Curtain %d,%d' % (x, y), x, y, [(None, t), ({'var': ['STAGE_CURTAIN', 1]}, None)]))
    win = ['Dorian Pell: Bravo! BRAVO! The house is on its feet!',
           {'script': 'Prismfall.award_badge(pfm_gym(:LEADER_DORIAN))'},
           {'script': 'pbReceiveItem(:TM42)'},
           "Dorian Pell: Facade - the art of turning a bad night into a standing ovation.",
           "Dorian Pell: And one more gift, from the whole troupe. Forty auditions, never cast. You two are a matched set.",
           {'script': 'pkmn = Pokemon.new(:EEVEE, 10)\npkmn.name = "Understudy"\npbAddPokemon(pkmn)'},
           {'switch': ['CH3_UNDERSTUDY_GOT', True]},
           "Dorian Pell: Opening night of the Pageant is at the Hall. Come. Bring Juno. Bring everyone.",
           {'selfswitch': ['A', True]}]
    dx, dy = T['dorian']
    ev += [
        {'type': 'warp', 'name': 'To the lobby', 'at': list(T['doors']),
         'to': {'map': 150, 'x': P.LOBBY_AT['doors'][0], 'y': P.LOBBY_AT['doors'][1] + 1, 'dir': 'down'}},
        {'type': 'event', 'name': 'Curtain rope', 'at': list(T['rope']), 'pages': [
            {'graphic': {'tile': CU('post_gold')}, 'commands': [
                {'if': 'pbGet(%d) == 1' % P.V_CURTAIN, 'then': ['The rope is tied off. The curtain is out.'], 'else': [
                    {'se': 'Door exit'}, {'var': ['STAGE_CURTAIN', 1]}, {'raw': [225, [2, 6, 10]]}, {'wait': 10},
                    'You haul on the rope. The house curtain flies out, the footlights come up - and there he is.']}]}]},
        {'type': 'npc', 'name': 'Stagehand', 'at': list(T['stagehand']), 'sprite': 'NPC 03', 'dir': 'left', 'commands': [
            {'if': 'pbGet(%d) == 0' % P.V_CURTAIN,
             'then': ["Stagehand: Places! He won't come out till the curtain's up. That rope, there. Give it a good haul."],
             'else': ["Stagehand: Break a leg. Not literally. He gets very upset about the paperwork."]}]},
        {'type': 'event', 'name': 'Dorian', 'at': [dx, dy], 'pages': [
            {'graphic': {'tile': MG(4689)}},
            {'cond': {'var': ['STAGE_CURTAIN', 1]}, 'graphic': {'sprite': 'trainer_GENTLEMAN', 'dir': 'down'}, 'commands': [
                'Dorian Pell: Enter, challenger, to thunderous applause! Your first Warden. Your first field. Your first audience.',
                "Dorian Pell: On my stage the house loves a show: dance, sing, dazzle them, and they'll lift you. "
                "The stage tells the truth the throne won't.",
                {'if': 'Prismfall.gym_battle(pfm_gym(:LEADER_DORIAN), double: false)', 'then': win}]},
            {'cond': {'self': 'A'}, 'graphic': {'sprite': 'trainer_GENTLEMAN', 'dir': 'down'}, 'commands': [
                'Dorian Pell: The Pageant, darling! The Hall, tonight!',
                {'if': 'pfm_gym_won?(:LEADER_TAMSIN)', 'then': [
                    "Dorian Pell: And a second badge! Then the old stage-left wing is yours. The revolve back there hasn't turned "
                    "since my debut. Get it through all three acts and the old script is yours."]}]}]},
        {'type': 'event', 'name': 'Stage-left wing', 'at': list(T['wing']), 'pages': [{'trigger': 'touch', 'commands': [
            {'if': 'pfm_gym_won?(:LEADER_TAMSIN)', 'then': [
                {'se': 'Door exit'}, {'transfer': {'map': 151, 'x': P.STAGE_AT['exit'][0], 'y': P.STAGE_AT['exit'][1] - 1, 'dir': 'up'}}],
             'else': ['A door in the wings, chalked: "OLD REVOLVE - CREW ONLY. Come back with a second badge, darling. - D.P."',
                      {'move': {'who': -1, 'route': ['right']}}]}]}]},
        trainer(T['ferdie'], 'JUGGLER', 'Florian', 2, 'right', "A challenger in the aisle! The show starts NOW!",
                "I'll be in the bar. There is no bar. I'll be in the lobby."),
        trainer(T['rosalind'], 'BEAUTY', 'Rosalind', 2, 'left', "Every great entrance needs a rival. Tonight, that's me.",
                "...Upstaged. In my own aisle."),
        trainer(T['crewe'], 'JUGGLER', 'Ambrose', 3, 'down', "Side aisle, cheap seats, best view! Let's have a scene!", "Encore? No? No.")]
    d = head(154, 'Pell Playhouse - Auditorium', 150); d.update(h.write(154)); d['events'] = ev; docs.append(d)

    # ================================================================ PLAYHOUSE BACKSTAGE (optional dungeon, DUNGEON_PUZZLES D9)
    # ---------------------------------------------------------------- 151 the old revolve (three scenes, in Script order)
    A = P.STAGE_AT
    S = P.STAGE
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
                ev.append(K.tile_event('%s %d,%d' % (ch, x, y), x, y, K.exact('STAGE_SCENE', k, CU('drop_' + n), 3)))
            elif ch in BRIDGE:
                n, k = BRIDGE[ch]
                ev.append(K.tile_event('%s %d,%d' % (ch, x, y), x, y, K.exact('STAGE_SCENE', k, CU(n), 3)))
            elif ch in 'AB':
                ev.append(K.tile_event('%s %d,%d' % (ch, x, y), x, y, [(None, CU('flat_' + ch)), ({'switch': 'STAGE_FLAT_' + ch}, None)]))
            elif ch == 'C':
                ev.append(K.tile_event('C %d,%d' % (x, y), x, y, [(None, CU('rostrum')), ({'switch': 'STAGE_FLAT_C'}, None)]))
            elif ch in '123':
                n = int(ch); scene = P.SCENES[n]
                mark = [c for c in P.find(S, 'x') if abs(c[0] - x) + abs(c[1] - y) == 1][0]
                ev.append({'type': 'event', 'name': 'Rope %d' % n, 'at': [x, y], 'pages': [{'graphic': {'tile': CU('post_' + ('silk', 'red', 'green', 'gold')[n])}, 'commands': [
                    {'if': '[$game_player.x, $game_player.y] != [%d, %d]' % mark, 'then': [
                        {'script': 'pfp_fail(:pb_stage, "You can\'t call a cue from here: the rope only reaches the painted mark.")'}],
                     'else': [{'if': 'pbGet(%d) == %d' % (P.V_SCENE, n), 'then': ['The stage is already set for %s.' % scene], 'else': [
                         {'var': [P.V_SCENE, n]}, {'se': 'Door exit'}, {'raw': [225, [2, 8, 12]]}, {'wait': 12},
                         'Cue: %s! The revolve groans round, and the whole set changes.' % scene]}]}]}]})
            elif ch in 'LK':
                lx, ly = P.find(P.LOFT, ch)[0]
                ev.append({'type': 'warp', 'name': 'Ladder %s' % ch, 'at': [x, y], 'to': {'map': 152, 'x': lx, 'y': ly + 1, 'dir': 'down'}})
    ev += [
        {'type': 'event', 'name': 'Upstage door', 'at': list(A['goal']), 'pages': [{'trigger': 'touch', 'commands': [
            {'if': '!pfm?(:backstage_done)', 'then': [
                "Behind the dais, a prop room no one has opened in years. On the throne's cushion: the Gilded King's own script, "
                "annotated in Dorian's hand. \"The stage tells the truth the throne won't.\"",
                {'script': 'pfm_item(:MAGICALSEED, 2, "Magical Seed")'}, {'script': 'pfm_item(:PPUP, 1, "PP Up")'},
                {'script': 'pfm_set(:backstage_done)'}]},
            {'se': 'Door exit'}, {'transfer': {'map': 154, 'x': P.THEATRE_AT['wing'][0] + 1, 'y': P.THEATRE_AT['wing'][1], 'dir': 'right'}}]}]},
        {'type': 'warp', 'name': 'To the auditorium', 'at': list(A['exit']), 'to': {'map': 154, 'x': P.THEATRE_AT['wing'][0] + 1, 'y': P.THEATRE_AT['wing'][1], 'dir': 'right'}},
        K.apprentice('Pip', 'NPC 07', A['pip'][0], A['pip'][1], 'pb_stage', "Stage manager Pip. I can strike the whole set, loft and all, back to work lights."),
        trainer(A['ferdie'], 'JUGGLER', 'Pierrot', 2, 'right', "Act One! I drown beautifully. Watch!", "Glub.", cond={'var': ['STAGE_SCENE', 1]}),
        trainer(A['rosalind'], 'LADY', 'Odette', 2, 'right', "Act Two: the Forest. I play a tree with opinions.", "Timber.", cond={'var': ['STAGE_SCENE', 2]}),
        trainer(A['crewe'], 'GENTLEMAN', 'Reginald', 2, 'left', "Act Three! Kneel before the Gilded King's understudy's understudy!", "Long live... you, I suppose.",
                cond={'var': ['STAGE_SCENE', 3]})]
    d = head(151, 'Pell Playhouse Backstage - The Old Revolve', 150); d.update(h.write(151)); d['events'] = ev; docs.append(d)

    # ---------------------------------------------------------------- 152 Fly Loft (COMBINE: a flat is in one place at a time)
    B = P.LOFT_AT
    Lf = P.LOFT
    h = K.Hall(Lf, 'stage', {'#': 'void', 'W': 'wall'}, seed=152)
    ev = []
    FL = {1: 'A', 2: 'B and C', 3: 'A and C'}
    for y, r in enumerate(Lf):
        for x, ch in enumerate(r):
            if ch in 'abc':
                ev.append(K.tile_event('%s %d,%d' % (ch, x, y), x, y, [(None, None), ({'switch': 'STAGE_FLAT_' + ch.upper()}, CU('flat_%s_hung' % ch.upper()))]))
            elif ch in '123':
                n = int(ch)
                sc = '\n'.join('pfp_flip(%d)' % (P.S_A + i) for i in P.ROPE_FLATS[n])
                ev.append({'type': 'event', 'name': 'Loft rope %d %s' % (n, 'L' if x < 12 else 'R'), 'at': [x, y], 'pages': [{'graphic': {'tile': CU('post_' + ('red', 'green', 'gold')[n - 1])}, 'commands': [
                    {'se': 'Door exit'}, {'script': sc},
                    'Counterweight rope %d: flat%s. Whatever was on the stage flies up here, and whatever hung here drops back in.' % (n, (' ' + FL[n]) if n == 1 else ('s ' + FL[n]))]}]})
            elif ch in 'LK':
                sx, sy = P.find(S, ch)[0]
                h.put(MG(3151), x, y, 1)
                ev.append({'type': 'warp', 'name': 'Ladder %s' % ch, 'at': [x, y], 'to': {'map': 151, 'x': sx, 'y': sy + 1, 'dir': 'down'}})
    tx, ty = B['trap']
    h.put(MI(962), tx, ty, 1)
    ev += [
        {'type': 'warp', 'name': 'Trapdoor', 'at': [tx, ty], 'to': {'map': 153, 'x': P.TRAP_AT['start'][0] + P.TRAP_OFF[0], 'y': P.TRAP_AT['start'][1] + P.TRAP_OFF[1], 'dir': 'up'}},
        {'type': 'item', 'at': list(B['item']), 'item': 'SUPERPOTION'},
        K.apprentice('Dot', 'NPC 03', B['dot'][0], B['dot'][1], 'pb_loft', "Dot. Flyman. Flywoman. I can drop every flat back onto the stage if you've boxed yourself in.")]
    d = head(152, 'Pell Playhouse Backstage - Fly Loft', 150); d.update(h.write(152)); d['events'] = ev; docs.append(d)

    # ---------------------------------------------------------------- 153 The Trap Room (MASTERY: ride the revolve)
    T = P.TRAP_AT; ox, oy = P.TRAP_OFF
    rows = [['#'] * 20 for _ in range(15)]
    for y, r in enumerate(P.TRAP):
        for x, ch in enumerate(r): rows[y + oy][x + ox] = '.' if ch in '.@o*' else '#'
    x0, y0, n = P.TABLE
    for y in range(y0, y0 + n):
        for x in range(x0, x0 + n): rows[y + oy][x + ox] = '.'
    rows[T['chest'][1] + oy][T['chest'][0] + ox] = '.'
    rows = [''.join(r) for r in rows]
    h = K.Hall(rows, 'stage', {'#': 'void'}, seed=153)
    ev = []
    for y in range(y0, y0 + n):
        for x in range(x0, x0 + n):
            if (x, y) == T['crank']: continue
            pages = [(None, CU('gear') if P.table_solid(x, y, 0) else None)]
            for rot in (1, 2, 3): pages.append(({'var': ['STAGE_TURNTABLE', rot]}, CU('gear') if P.table_solid(x, y, rot) else None))
            ev.append(K.tile_event('Table %d,%d' % (x, y), x + ox, y + oy, pages))
    cx, cy = T['crank'][0] + ox, T['crank'][1] + oy
    ev += [
        {'type': 'event', 'name': 'Crank', 'at': [cx, cy], 'pages': [{'graphic': {'tile': CU('post_brass')}, 'commands': [
            {'se': 'Door exit'}, {'raw': [225, [2, 8, 10]]},
            {'script': 'pfp_cycle(%d, 4)\npfp_turntable_ride(%d, %d)' % (P.V_TURN, cx, cy)},
            "You lean on the crank. The whole floor, and you with it, swings a quarter-turn."]}]},
        {'type': 'event', 'name': 'Prop chest', 'at': [T['chest'][0] + ox, T['chest'][1] + oy], 'pages': [
            {'graphic': {'sprite': 'Object ball'}, 'commands': [
                {'script': 'pfm_item(:MAGICALSEED, 2, "Magical Seed")'}, {'script': 'pfm_item(:PPUP, 1, "PP Up")'},
                "Under the seeds: a dented prop crown. \"THE GILDED KING - Act III\".", {'script': 'pfm_set(:gilded_crown)'},
                {'switch': ['STAGE_TRAP_DONE', True]}, {'selfswitch': ['A', True]}]},
            {'cond': {'self': 'A'}}]},
        K.apprentice('Old Joss', 'NPC 11', T['joss'][0] + ox, T['joss'][1] + oy, 'pb_trap', "Old Joss. I built the revolve. Dizzy? I'll wind it back."),
        {'type': 'warp', 'name': 'Ladder up', 'at': [T['ladder'][0] + ox, T['ladder'][1] + oy], 'to': {'map': 152, 'x': tx, 'y': ty + 1, 'dir': 'down'}}]
    h.put(MG(3151), T['ladder'][0] + ox, T['ladder'][1] + oy, 1)
    d = head(153, 'Pell Playhouse Backstage - The Trap Room', 150); d.update(h.write(153)); d['events'] = ev; docs.append(d)

    with open(os.path.join(HERE, 'specs', '150_pell_playhouse.yaml'), 'w') as f:
        f.write('# GENERATED by gen_playhouse.py from design/GYM_PUZZLES.md + mapgen/puzzles/playhouse.py (Gym 1 + Playhouse Backstage, tileset 54). Edit the script, then run build.py.\n')
        yaml.safe_dump_all(docs, f, sort_keys=False, allow_unicode=True, width=120)
    print('wrote specs/150_pell_playhouse.yaml')


if __name__ == '__main__':
    main()
