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


def say(who, expr, text):
    return '\\pf[%s,%s]%s: %s' % (who.upper(), expr, who.capitalize(), text)


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
    # ---------------------------------------------------------------- 150 Lobby (art pass 2026-11-19: a grand foyer)
    NM, CH = K.NM, K.CH
    A = P.LOBBY_AT
    h = K.Hall(P.LOBBY, 'lobby', {'#': 'void', 'W': 'wall', 'D': 'door'}, seed=150)
    for y in range(6, 14):                                            # the foyer carpet: Nightbox's dark patterned red
        for x in range(1, 24): h.put(NM(685), x, y, 0)
    for y in range(6, 14):                                            # a red runner from the street doors to the auditorium
        r = 0 if y == 6 else (2 if y == 13 else 1)
        for i, x in enumerate((11, 12, 13)): h.put(NM([[773, 774, 775], [781, 782, 783], [789, 790, 791]][r][i]), x, y, 1)
    for x in (1, 5, 9, 15, 19, 23):                                    # purple pilasters between the wall bays
        for y in (2, 3, 4, 5): h.put(MG(1704), x, y, 0)
    h.obj('poster_rain', 2, 2); h.obj('poster_lady', 6, 2); h.obj('poster_green', 16, 2)
    h.block([[CU('paste_%d_%d' % (c, r)) for c in range(3)] for r in range(3)], 20, 2, 1)   # pasted over, years ago ("...ED K...")
    h.block([[CU('crest_0'), CU('crest_1'), CU('crest_2')]], 11, 3, 2)  # the comedy-and-tragedy crest over the auditorium doors
    h.block([[CU('beam_l'), CU('beam_mid'), CU('beam_r')]], 11, 2, 1)
    for x in (10, 14): h.block([[NM(779)], [NM(779)], [NM(787)]], x, 2, 2)   # small chandeliers either side of the doors
    h.block([[0, NM(779), 0], [0, NM(779), 0], [NM(776), NM(787), NM(778)], [NM(784), NM(785), NM(786)]], 11, 6, 2)   # the great one
    for x in (2, 6, 16, 20): h.block([[NM(1016), NM(1017), NM(1018)]], x, 6, 2)        # velvet ropes under the posters
    h.block([[NM(1288), NM(1289), NM(1290)]], 2, 8, 1)                # the box office counter (the clerk stands behind it)
    h.put(NM(1292), 4, 8, 2)
    h.block([[NM(472), NM(473)], [NM(480), NM(481)], [NM(488), NM(489)]], 20, 10, 1)   # high-backed velvet loveseats
    h.block([[NM(472), NM(473)], [NM(480), NM(481)], [NM(488), NM(489)]], 22, 10, 1)
    h.block([[NM(541), NM(542), NM(543)], [NM(549), NM(550), NM(551)]], 5, 11, 1)     # a sofa for the regulars
    h.block([[NM(518), NM(519)], [NM(526), NM(527)]], 16, 11, 1)                      # flowers for the leading lady
    h.block([[NM(518), NM(519)], [NM(526), NM(527)]], 8, 11, 1)
    h.put(NM(538), 1, 13, 1); h.put(NM(539), 23, 13, 1); h.put(NM(540), 1, 10, 1); h.put(NM(540), 23, 7, 1)
    h.obj('urn', 5, 6); h.obj('urn', 19, 6)
    h.obj('mat_mg', 11, 14)
    ev = [{'type': 'exit', 'at': list(A['exit']), 'link': 'SM_GYM', 'se': 'Door exit'},
          {'type': 'warp', 'name': 'Auditorium doors', 'at': list(A['doors']),
           'to': {'map': 154, 'x': P.THEATRE_AT['start'][0], 'y': P.THEATRE_AT['start'][1], 'dir': 'up'}},
          {'type': 'event', 'name': 'House count', 'at': [0, 1], 'pages': [{'trigger': 'parallel', 'commands': [
              {'script': 'pf_audience_sync'}, {'raw': [116, []]}]}]},
          {'type': 'npc', 'name': 'Usher', 'at': list(A['usher']), 'sprite': 'trainer_GENTLEMAN', 'dir': 'down', 'commands': [
              "Usher: Ah, our challenger! Tonight's bill: Dorian Pell, in person. Through the doors, up the aisle, onto the stage.",
              {'script': 'pbMessage(_INTL("Usher: And tonight we have {1}. Everyone you shake hands with in Saltmere ends up in a seat, you know. It\'s that sort of town.", pf_house_name))'},
              "Usher: The cast may want a word on your way. Actors. They always want a word."]},
          {'type': 'npc', 'name': 'Gym guide', 'at': list(A['guide']), 'sprite': 'NPC 01', 'dir': 'left', 'commands': [
              "Gym Guide: Your first Warden! Dorian uses Normal-types, on the Grand Stage field.",
              "Gym Guide: Here's the trick of a field: the house loves a show. Sound moves and dances get a cheer, and the cheer makes "
              "the next move hit harder. It works for you too.",
              "Gym Guide: Normal-types don't fear much. Fighting-types, they fear. Rock shrugs them off. And Ghosts just don't care, "
              "which Dorian finds very rude."]},
          {'type': 'npc', 'name': 'Lady', 'at': list(A['lady']), 'sprite': 'trainer_LADY', 'dir': 'right',
           'text': "I come every night. Every. Night. He has never once taken a bow the same way twice."},
          {'type': 'npc', 'name': 'Box office', 'at': list(A['clerk']), 'sprite': 'NPC 12', 'dir': 'down', 'commands': [
              "Box Office: Challengers go in free. Everyone else pays. Dorian says a challenger IS the show."]},
          {'type': 'npc', 'name': 'Theatregoer 1', 'at': [14, 8], 'sprite': 'trainer_BEAUTY', 'dir': 'left',
           'text': "We saw the matinee. He did the whole second act as a Ditto. Nobody knew what was happening. It was wonderful."},
          {'type': 'npc', 'name': 'Theatregoer 2', 'at': [15, 8], 'sprite': 'trainer_GENTLEMAN', 'dir': 'left',
           'text': "Dear, the challenger is HERE. Stop talking about the Ditto."},
          {'type': 'npc', 'name': 'Theatregoer 3', 'at': [7, 9], 'sprite': 'NPC 08', 'dir': 'up',
           'text': "Queue for the box office. Queue for the cloakroom. Queue for the queue. Saltmere loves a queue."},
          {'type': 'npc', 'name': 'Theatregoer 4', 'at': [19, 12], 'sprite': 'trainer_PAINTER', 'dir': 'right',
           'text': "I'm sketching the audience. Nobody ever sketches the audience. They make the better faces."},
          {'type': 'npc', 'name': 'Theatregoer 5', 'at': [4, 12], 'sprite': 'NPC 16', 'dir': 'right',
           'text': "Sound moves get a cheer in there. My Jigglypuff got a standing ovation once. Then everyone fell asleep."},
          sign('Old poster', (21, 5), 'An old poster, under the others. A title has been pasted over, years ago. Where the paste has lifted, two letters show through: "...ED K..."'),
          sign('Poster: The Lady in Red', (7, 5), 'A poster: "THE LADY IN RED. Dorian Pell, Rosalind Vane. Held over by popular demand." (Popular demand: D. Pell.)'),
          sign('Poster: Rain Fall', (3, 5), 'A poster: "RAIN FALL. A comedy in one wet act. Umbrellas will not be provided."'),
          sign('Poster: The Loyal Three', (17, 5), 'A poster: "THE LOYAL THREE - the Festival-year companion piece to the Pageant of the Prismfall. Three faithful hounds! One wicked Ogre! Bring the children!"')]
    d = head(150, 'Pell Playhouse - Lobby', 147, {'metadata': dict(M, SnapEdges=True)}); d.update(h.write(150, [tuple(e['at']) for e in ev if e.get('at')])); d['events'] = ev; docs.append(d)

    # ---------------------------------------------------------------- 154 Auditorium (GYM 1; art pass 2026-11-19)
    T = P.THEATRE_AT
    rows = P.THEATRE
    cls = {'#': 'void', 'K': 'wall', 'P': 'wall', 'B': 'wall', 'D': 'wall', 'p': 'lip', 'S': 'stair', 's': 'seat', ',': 'floor2',
           'r': 'floor2', 'o': 'floor2', 'g': 'floor2', 'a': 'floor', '.': 'floor'}
    h = K.Hall(rows, 'stage', cls, seed=154)
    BOARDS = [MI(1241), MI(1242), MI(1243)]
    rnd = h.r
    for y, r in enumerate(rows):                                      # the house carpet: Nightbox's dark red damask
        for x, ch in enumerate(r):
            if ch in ',rgs': h.put(NM(685), x, y, 0)
            if ch == 'p': h.put(0, x, y, 1)                           # (the footlights replace the plain stage lip)
    for y in range(2, 11):                                            # the side walls: Nightbox's dark striped panelling
        for x in list(range(1, 4)) + list(range(21, 24)):
            h.put(NM(402) if y == 2 else NM(865), x, y, 0)
    for x0 in (1, 21):                                                 # a box in each side wall, curtained, a chair inside
        h.block([[NM(685)] * 3] * 3, x0, 3, 0)
        h.block([[0, 0, 0], [NM(654)] * 3, [NM(920), NM(921), NM(922)], [NM(888), 0, NM(890)], [NM(896), NM(897), NM(898)]], x0, 3, 1)
        h.block([[NM(904), NM(905), NM(906)], [NM(912), NM(867), NM(914)], [NM(880), NM(875), NM(882)], [0, NM(889), 0], [0, NM(897), 0]], x0, 3, 2)
        h.block([[NM(842), NM(843), NM(844)], [NM(850), NM(851), NM(852)]], x0, 9, 1)   # stage-left wing door / dressing rooms
        h.put(NM(779), x0 + 1, 8, 2)                                  # a small chandelier between box and door
    for y in range(2, 11):                                            # the proscenium: gilded pilasters, and behind them the wall
        for x in (4, 20):
            h.put(NM(865), x, y, 0)
            h.put(CU('column_cap') if y == 3 else CU('column_base') if y == 10 else CU('column_shaft'), x, y, 1)
    for x in range(4, 21):                                            # the gilded beam across the top of the opening
        h.put(NM(393), x, 2, 0)
        h.put(CU('beam_l') if x == 4 else CU('beam_r') if x == 20 else CU('beam_mid'), x, 2, 1)
    h.block([[CU('crest_0'), CU('crest_1'), CU('crest_2')]], 11, 2, 2)
    for x in range(5, 20):                                            # the painted drop: Saltmere harbour at dusk
        for y in range(3, 6): h.put(CU('backdrop_%d_%d' % (x - 5, y - 3)), x, y, 0)
    for x in range(5, 20):                                            # the valance swag along the top of the drop
        h.put(NM(904) if x == 5 else NM(906) if x == 19 else NM(905), x, 3, 2)
    for y in range(6, 12):                                            # the stage and the apron: polished boards
        for x in range(1 if y == 11 else 5, 24 if y == 11 else 20): h.put(rnd.choice(BOARDS), x, y, 0)
    for y in range(4, 11):                                            # the house curtain's legs, gathered either side
        h.put(NM(920) if y == 10 else NM(912), 5, y, 2); h.put(NM(922) if y == 10 else NM(914), 19, y, 2)
    h.put(CU('mark'), 12, 8, 1); h.put(CU('mark'), 8, 9, 1); h.put(CU('mark'), 16, 9, 1)     # tape marks on the boards
    for x in range(1, 24):                                            # the footlights along the stage front, their glow on the apron
        if x != 12: h.put(CU('footlight'), x, 12, 0)
        h.put(CU('glow'), x, 11, 2)
    h.put(BOARDS[0], 12, 12, 0); h.put(MG(3151), 12, 12, 1)
    for y in range(13, 16):                                           # the orchestra pit, a storey down
        for x in list(range(1, 11)) + list(range(14, 24)): h.put(CU('pit_%d' % rnd.randrange(3)), x, y, 0)
    h.block([[CH(1464), CH(1465), CH(1466)], [CH(1472), CH(1473), CH(1474)], [CH(1480), CH(1481), CH(1482)]], 2, 13, 1)   # the grand
    for x, y in ((6, 14), (8, 15), (16, 14), (18, 15), (21, 14)): h.put(CU('music_stand'), x, y, 1)
    for x in range(1, 24):                                            # the pit rail
        if 11 <= x <= 13: continue
        h.put(CU('pit_rail_l') if x in (1, 14) else CU('pit_rail_r') if x in (10, 23) else CU('pit_rail_mid'), x, 16, 1)

    def runner(x0, y0, y1):                                           # the red, gold-edged runner up the centre aisle
        for y in range(y0, y1 + 1):
            r = 0 if y == y0 else (2 if y == y1 else 1)
            for i in range(3): h.put(NM([[773, 774, 775], [781, 782, 783], [789, 790, 791]][r][i]), x0 + i, y, 1)
    runner(11, 13, 28)
    for y in (18, 23):                                                # brass row plates at the aisle ends
        pass
    h.block([[0, NM(779), 0], [0, NM(779), 0], [NM(776), NM(787), NM(778)], [NM(784), NM(785), NM(786)]], 11, 19, 2)   # the chandelier
    for x in (1, 23): h.block([[NM(779)], [NM(787)]], x, 23, 2)
    h.obj('urn', 1, 27); h.obj('urn', 23, 27)
    h.block([[NM(518), NM(519)], [NM(526), NM(527)]], 2, 27, 1); h.block([[NM(518), NM(519)], [NM(526), NM(527)]], 21, 27, 1)
    h.put(MG(1731), 11, 29, 1); h.put(MG(1732), 12, 29, 1); h.put(MG(1733), 13, 29, 1)
    ev = []
    for (x, y) in P.CURTAIN:                                         # the house curtain: in until the rope flies it out
        if (x, y) == T['dorian']: continue                            # Dorian's own event wears the curtain until it flies
        t = MG(4697) if y == P.CURTAIN[-1][1] else MG(4681) if y == 3 else MG(4689)
        ev.append(K.tile_event('Curtain %d,%d' % (x, y), x, y, [(None, t), ({'var': ['STAGE_CURTAIN', 1]}, None)]))
    # --- the house: an audience in the stalls, musicians in the pit, a couple in each box
    SEATED = ['NPC 02', 'NPC 04', 'NPC 06', 'NPC 09', 'NPC 10', 'NPC 13', 'NPC 14', 'NPC 17', 'NPC 19', 'NPC 21', 'NPC 23',
              'NPC 24', 'NPC 26', 'NPC 27', 'trainer_LADY', 'trainer_GENTLEMAN', 'trainer_BEAUTY', 'trainer_AROMALADY',
              'trainer_PAINTER', 'trainer_SCIENTIST', 'trainer_SAILOR', 'trainer_GAMBLER', 'trainer_POKEMANIAC', 'trainer_PICNICKER']
    LINES = ["Shh! It's about to start.", "Is he on yet? Is that him? That's the curtain. I knew that.",
             "Third night running. I know every line. Don't tell him.", "Sound moves get a cheer in here. Watch the crowd when someone sings.",
             "The footlights make everyone look braver. Even me.", "I came for the chandelier, honestly.",
             "My seat's the best in the house. Everyone's seat is the best in the house. He wrote that on the tickets.",
             "Psst. If you're the challenger: he hates being boring more than he hates losing."]
    # SPINE Rev 19: the Saltmere audience (V313 STAGE_AUDIENCE; plugins/Prismfall Puzzles/007_Puzzles_SaltmereCrowd.rb).
    # Three layers: ten regulars who are always in; every townsperson you met, in their own seat by the aisle (event
    # "Fan <key>", shown by the house manager on self switch A); and the rest of the town, four more seats per head
    # counted ([V313 >= k]).  Sparse house 0-6, good house 7-13, full house 14+.
    seats = [(x, y) for y in list(range(18, 22)) + list(range(23, 27)) for x in list(range(2, 11)) + list(range(14, 23))]
    busy = {T['ferdie'], T['rosalind'], T['juno']}
    talkable = lambda x, y: any(rows[y + dy][x + dx] == ',' for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
    FANS = [('caramel_seller', 'NPC 29', "Caramel Seller: Salt-caramel for the interval! You're my best customer, so you get the crunchy bits."),
            ('busker', 'NPC 27', "Busker: I'll play you on. Quietly. The conductor glares."),
            ('ogre_child', 'NPC 17', "Child with an Ogre puppet: The Ogre came to watch you! He says GRAAH. That means good luck."),
            ('retired_actor', 'NPC 24', "Retired Actor: Breathe from the belly. Stand like you own the boards. You do, tonight."),
            ('hound_two', 'NPC 23', "Hound Number Two: GRR. On the beat. For you!"),
            ('fishwife', 'trainer_FISHERMAN', "Fishwife: No tint at all, and look at you, top of the bill. I'll gossip about you for a WEEK."),
            ('ferry_woman', 'NPC 13', "Woman from the ferry: From the Dovetail to the Playhouse! I told everyone on the quay."),
            ('eevee_breeder', 'NPC 25', "Breeder: The troupe's Eevee is in the wings tonight. Forty auditions. Maybe forty-one."),
            ('salt_raker', 'NPC 19', "Salt raker: Rake it white, cheer it loud."),
            ('harbourmaster', 'trainer_SAILOR', "Harbourmaster: Free port, free seats. Don't tell Dorian I said that."),
            ('saltwife', 'NPC 28', "Saltwife: Forty years raking and I've never missed an opening night. Win it."),
            ('stevedore', 'NPC 07', "Stevedore: I can shout over a crane. I'll shout over HIM."),
            ('old_angler', 'NPC 05', "Old angler: Something big's circling the breakwater. Something big's on that stage. Same advice: patience."),
            ('fisherman', 'trainer_FISHERMAN', "Fisherman: Ordinary night. Extraordinary seats."),
            ('old_sailor', 'trainer_SAILOR', "Old Sailor: Born here, live anywhere. Tonight I live in row three."),
            ('smoke_stagehand', 'NPC 20', "Stagehand: I'm off shift. I'm watching like a civilian. A loud civilian."),
            ('costumier', 'NPC 12', "Costumier: I stitched his cape. If you tear it I'll stitch you a worse one."),
            ('street_player', 'NPC 08', "Street player: A stage is anywhere two people stop to look. Two hundred people stopped. Go on."),
            ('quest_EL_LANTERNS', 'NPC 26', "Lantern-bearer: Sister Hollin sent us. We brought our own lanterns. We're keeping them."),
            ('quest_EL_LANTERNS', 'NPC 26', "Sister Hollin: The lanterns came home. So did we. Listen to the house, child."),
            ('quest_EL_LANTERNS', 'NPC 14', "Lantern-bearer: We're the quiet section. Mostly.")]
    fan_seats = [c for c in seats if c not in busy and talkable(*c) and c[0] in (10, 14)]
    fan_seats += [c for c in seats if c not in busy and talkable(*c) and c[0] in (2, 22)]
    for (key, spr, line), (x, y) in zip(FANS, fan_seats):
        ev.append({'type': 'event', 'name': 'Fan %s' % key, 'at': [x, y], 'pages': [
            {}, {'cond': {'self': 'A'}, 'graphic': {'sprite': spr, 'dir': 'up'}, 'commands': [line]}]})
    free = [c for c in seats if c not in busy and c not in fan_seats[:len(FANS)]]
    rnd.shuffle(free)
    regulars, rest = free[:10], free[10:]
    for i, (x, y) in enumerate(regulars + rest[:84]):
        spr = SEATED[rnd.randrange(len(SEATED))]
        pg = {'graphic': {'sprite': spr, 'dir': 'up'}}
        if talkable(x, y): pg['commands'] = ['(whispering) ' + LINES[rnd.randrange(len(LINES))]]
        if i < 10:
            ev.append({'type': 'event', 'name': 'Audience %d' % i, 'at': [x, y], 'pages': [pg]})
        else:                                                         # the rest of the town: 4 seats per head counted
            k = (i - 10) // 4 + 1
            ev.append({'type': 'event', 'name': 'Audience %d' % i, 'at': [x, y], 'pages': [{}, dict(pg, cond={'var': ['STAGE_AUDIENCE', k]})]})
    ev.append({'type': 'event', 'name': 'House manager', 'at': [0, 2], 'pages': [   # counts the quests, seats the people you met
        {'trigger': 'parallel', 'commands': [{'script': 'pf_audience_sync'}, {'raw': [116, []]}]}]})
    for i, (x, y, spr) in enumerate(((6, 13, 'NPC 05'), (8, 14, 'NPC 18'), (16, 13, 'NPC 20'), (18, 14, 'NPC 03'), (21, 13, 'NPC 22'))):
        ev.append({'type': 'event', 'name': 'Musician %d' % i, 'at': [x, y], 'pages': [{'graphic': {'sprite': spr, 'dir': 'down'}}]})
    ev.append({'type': 'npc', 'name': 'Conductor', 'at': [10, 15], 'sprite': 'trainer_GENTLEMAN', 'dir': 'up', 'commands': [
        "Conductor: The orchestra is tuning. Someone in the brass is playing the Wingull Shanty, very quietly, as a joke.",
        "Conductor: When Dorian's Pokémon sing, we play under them. The house goes wild for it. It's in the field notes, apparently."]})
    for i, (x, y, spr) in enumerate(((2, 5, 'trainer_LADY'), (22, 5, 'trainer_GENTLEMAN'))):
        ev.append({'type': 'npc', 'name': 'Box %d' % i, 'at': [x, y], 'sprite': spr, 'dir': 'down',
                   'text': "(Opera glasses glint in the box.)"})
    win = [say('DORIAN', 'shocked', "...They're standing. Look at them. They're on their FEET."),
           say('DORIAN', 'crying', "Bravo! BRAVO! Oh, I'm crying, don't look, it's the footlights."),
           {'script': 'Prismfall.award_badge(pfm_gym(:LEADER_DORIAN))'},
           "(You open the Badge Case and set the badge in. A faint hum: one clear note. The whole house goes quiet.)",
           "\\pf[JUNO,happy,question]Juno: Ooh. Is it supposed to do that?",
           "\\pf[DORIAN,shocked,shock]Dorian: Darling, in Saltmere nothing is supposed to do ANYTHING. That's the whole charter.",
           say('DORIAN', 'neutral', "..."), say('DORIAN', 'happy', "Do it again."),
           "(Nothing. The case is quiet.)",
           say('DORIAN', 'deadpan', "One night only. The best kind."),
           {'if': 'pf_audience > 0', 'then': [{'script': 'n = pf_audience * 150\n$player.money += n\npbMessage(_INTL("(The box office sends up your share of the takings: ${1}.)", n.to_s_formatted))'}]},
           {'script': 'pbReceiveItem(:TM42)'},
           say('DORIAN', 'neutral', "Facade. The art of turning a bad night into a standing ovation. You'll need it more often than you'd think."),
           say('DORIAN', 'neutral', "That badge is the Accord's word that Pokémon up to level nineteen will heed you. Briarwick's will let you cut the dead wood, when you've earned it. They have a man for that."),
           "(The troupe files on from the wings. The smallest actor is carrying an Eevee in a ruff.)",
           say('DORIAN', 'happy', "And one more gift, from the whole company. Forty auditions. Never cast. A tragedy in a ruff."),
           say('DORIAN', 'neutral', "You came off that ferry with no color at all, I hear, and this one's never picked one either. You two are a matched set."),
           {'script': 'pkmn = Pokemon.new(:EEVEE, 10)\npkmn.name = "Understudy"\npbAddPokemon(pkmn)'},
           {'switch': ['CH3_UNDERSTUDY_GOT', True]},
           say('DORIAN', 'happy', "Rehearsal at the Lantern Theatre this afternoon, opening night at eight. Come to both. Bring Juno. Bring everyone."),
           {'selfswitch': ['A', True]}]
    dx, dy = T['dorian']
    wx, wy = T['wing']
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
        {'type': 'event', 'name': 'Dressing rooms', 'at': [22, 10], 'pages': [{'commands': [
            'A door in the wings, gilt letters on black: "DRESSING ROOMS. Company only." Someone inside is warming up: "Mi-mi-mi-MEE."']}]},
        {'type': 'event', 'name': 'Dorian', 'at': [dx, dy], 'pages': [
            {'graphic': {'tile': MG(4689)}},
            {'cond': {'var': ['STAGE_CURTAIN', 1]}, 'graphic': {'sprite': 'trainer_GENTLEMAN', 'dir': 'down'}, 'commands': [
                {'if': "$game_self_switches[[154, 0, 'TRIED']]", 'then': [say('DORIAN', 'happy', "Act Two! I adore an Act Two. Everyone's warmed up.")], 'else': [
                    "(Dorian stands center stage in a single spotlight, cane raised, as if he has been standing there for an hour. He may have.)",
                    say('DORIAN', 'happy', "Enter, stage left, our brave challenger! To thunderous applause!"),
                    "(The audience applauds, thunderously.)",
                    say('DORIAN', 'neutral', "Your first Warden. Your first field. Your first audience. I envy you, darling. You only get one of each."),
                    say('DORIAN', 'smug', "On my stage the house loves a show. Sing, dance, dazzle them, and they'll carry you. Bore them, and they'll let you fall."),
                    say('DORIAN', 'happy', "Shall we give them something to remember?")]},
                {'if': 'pf_house_stage >= 3', 'then': [
                    say('DORIAN', 'shocked', "...A FULL house. Darling, did you shake every hand in Saltmere? They're here for YOU."),
                    say('DORIAN', 'happy', "Then we start at a standing ovation. Don't let them sit down.")],
                 'else': [{'if': 'pf_house_stage == 2', 'then': [
                    say('DORIAN', 'happy', "A good house tonight! Half the town seems to know your name already. We'll open on an encore."),
                    ], 'else': [
                    say('DORIAN', 'neutral', "A sparse house. Intimate. Every seat a front-row seat. We'll make them remember us anyway.")]}]},
                {'script': "$game_self_switches[[154, 0, 'TRIED']] = true"},
                {'script': 'pf_house_rules'},
                {'if': 'Prismfall.gym_battle(pfm_gym(:LEADER_DORIAN), double: false)', 'then': win}]},
            {'cond': {'self': 'A'}, 'graphic': {'sprite': 'trainer_GENTLEMAN', 'dir': 'down'}, 'commands': [
                say('DORIAN', 'happy', "Rehearsal at the Lantern Theatre, darling! Opening night at eight!"),
                {'if': 'pfm_gym_won?(:LEADER_TAMSIN)', 'then': [
                    say('DORIAN', 'smug', "And a second badge! Then the old stage-left wing is yours. The revolve back there hasn't turned since "
                        "my debut. Get it through all three acts. There's a prompt-book in the prop room I'd rather you found than the Crown's inspectors.")]}]}]},
        {'type': 'event', 'name': 'Stage-left wing', 'at': [wx, wy], 'pages': [{'trigger': 'touch', 'commands': [
            {'if': 'pfm_gym_won?(:LEADER_TAMSIN)', 'then': [
                {'se': 'Door exit'}, {'transfer': {'map': 151, 'x': P.STAGE_AT['exit'][0], 'y': P.STAGE_AT['exit'][1] - 1, 'dir': 'up'}}],
             'else': ['A door in the wings, chalked: "OLD REVOLVE - CREW ONLY. Come back with a second badge, darling. - D.P."']}]}]},
        {'type': 'event', 'name': 'Field Notes', 'at': [0, 1], 'pages': [    # the first field's pop-up, once, on the first step up the aisle
            {'trigger': 'parallel', 'commands': [
                {'if': '!pfm?(:fn_grand_stage) && $game_player.y <= %d && !$game_temp.message_window_showing' % (T['start'][1] - 1), 'then': [
                    {'script': 'pfm_set(:fn_grand_stage)'},
                    "FIELD NOTES: GRAND STAGE - the audience reacts. Sound moves and dances earn applause, and applause lifts the next move. "
                    "Nothing on this stage is real, which is the point.",
                    "(Larch, in the margin: 'Saltmere. The one place I never worry about you. Don't make me start.')"]},
                {'wait': 6}]}]},
        {'type': 'event', 'name': 'Juno reveal', 'at': [0, 0], 'pages': [   # Juno comes into the stalls once one actor is beaten
            {'trigger': 'parallel', 'commands': [
                {'if': "$game_map.events.values.count { |e| e.name[/^Trainer\\(/] && $game_self_switches[[154, e.id, 'A']] } >= 1",
                 'then': [{'script': "ev = $game_map.events.values.find { |e| e.name == 'Juno' }\n$game_self_switches[[154, ev.id, 'A']] = true if ev\n$game_map.need_refresh = true"}]},
                {'wait': 20}]}]},
        {'type': 'event', 'name': 'Juno', 'at': list(T['juno']), 'pages': [
            {},
            {'cond': {'self': 'A'}, 'graphic': {'sprite': 'JUNO', 'dir': 'right'}, 'commands': [
                {'if': "$game_self_switches[[154, 0, 'JUNO']]", 'then': [say('JUNO', 'happy', "(whispering) I'll be loud quietly.")], 'else': [
                    "(Juno is in the front row with a paper cone of salt-caramel.)",
                    say('JUNO', 'happy', "I made it! I'm AUDIENCE! Go on! I'll be loud!"),
                    "Audience Member: Shh!",
                    say('JUNO', 'happy', "(whispering) I'll be loud quietly."),
                    {'script': "$game_self_switches[[154, 0, 'JUNO']] = true"}]}]}]},
        trainer(T['ferdie'], 'JUGGLER', 'Florian', 2, 'right', "A challenger in the aisle! The show starts NOW!",
                "I'll be in the bar. There is no bar. I'll be in the lobby."),
        trainer(T['rosalind'], 'BEAUTY', 'Rosalind', 2, 'left', "Every great entrance needs a rival. Tonight, that's me.",
                "...Upstaged. In my own aisle."),
        trainer(T['crewe'], 'JUGGLER', 'Ambrose', 3, 'down', "Side aisle, cheap seats, best view! Let's have a scene!", "Encore? No? No.")]
    d = head(154, 'Pell Playhouse - Auditorium', 150, {'metadata': dict(M, SnapEdges=True)}); d.update(h.write(154, [tuple(e['at']) for e in ev if e.get('at')])); d['events'] = ev; docs.append(d)

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
                "Behind the dais, a prop room no one has opened in years. On the throne's cushion: an old Pageant prompt-book. "
                "Every line about the old capital has been struck out in red. In the margin, in Dorian's hand: \"The stage tells the truth the throne won't.\"",
                {'script': 'pfm_item(:MAGICALSEED, 2, "Magical Seed")'}, {'script': 'pfm_item(:PPUP, 1, "PP Up")'},
                {'script': 'pfm_set(:backstage_done)'}]},
            {'se': 'Door exit'}, {'transfer': {'map': 154, 'x': P.THEATRE_AT['wing'][0], 'y': P.THEATRE_AT['wing'][1] + 1, 'dir': 'down'}}]}]},
        {'type': 'warp', 'name': 'To the auditorium', 'at': list(A['exit']), 'to': {'map': 154, 'x': P.THEATRE_AT['wing'][0], 'y': P.THEATRE_AT['wing'][1] + 1, 'dir': 'down'}},
        K.apprentice('Pip', 'NPC 07', A['pip'][0], A['pip'][1], 'pb_stage', "Stage manager Pip. I can strike the whole set, loft and all, back to work lights."),
        trainer(A['ferdie'], 'JUGGLER', 'Pierrot', 2, 'right', "Act One! I drown beautifully. Watch!", "Glub.", cond={'var': ['STAGE_SCENE', 1]}),
        trainer(A['rosalind'], 'LADY', 'Odette', 2, 'right', "Act Two: the Forest. I play a tree with opinions.", "Timber.", cond={'var': ['STAGE_SCENE', 2]}),
        trainer(A['crewe'], 'GENTLEMAN', 'Reginald', 2, 'left', "Act Three! Kneel before the Gilded King's understudy's understudy!", "Long live... you, I suppose.",
                cond={'var': ['STAGE_SCENE', 3]})]
    d = head(151, 'Pell Playhouse Backstage - The Old Revolve', 150); d.update(h.write(151, [tuple(e['at']) for e in ev if e.get('at')])); d['events'] = ev; docs.append(d)

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
    d = head(152, 'Pell Playhouse Backstage - Fly Loft', 150); d.update(h.write(152, [tuple(e['at']) for e in ev if e.get('at')])); d['events'] = ev; docs.append(d)

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
                "Under the seeds: the old Crown prop. Its paste jewels are long gone, but the centre stone is real, and whole.", {'script': 'pfm_set(:old_crown_prop)'},
                {'switch': ['STAGE_TRAP_DONE', True]}, {'selfswitch': ['A', True]}]},
            {'cond': {'self': 'A'}}]},
        K.apprentice('Old Joss', 'NPC 11', T['joss'][0] + ox, T['joss'][1] + oy, 'pb_trap', "Old Joss. I built the revolve. Dizzy? I'll wind it back."),
        {'type': 'warp', 'name': 'Ladder up', 'at': [T['ladder'][0] + ox, T['ladder'][1] + oy], 'to': {'map': 152, 'x': tx, 'y': ty + 1, 'dir': 'down'}}]
    h.put(MG(3151), T['ladder'][0] + ox, T['ladder'][1] + oy, 1)
    d = head(153, 'Pell Playhouse Backstage - The Trap Room', 150); d.update(h.write(153, [tuple(e['at']) for e in ev if e.get('at')])); d['events'] = ev; docs.append(d)

    with open(os.path.join(HERE, 'specs', '150_pell_playhouse.yaml'), 'w') as f:
        f.write('# GENERATED by gen_playhouse.py from design/GYM_PUZZLES.md + mapgen/puzzles/playhouse.py (Gym 1 + Playhouse Backstage, tileset 54). Edit the script, then run build.py.\n')
        yaml.safe_dump_all(docs, f, sort_keys=False, allow_unicode=True, width=120)
    print('wrote specs/150_pell_playhouse.yaml')


if __name__ == '__main__':
    main()
