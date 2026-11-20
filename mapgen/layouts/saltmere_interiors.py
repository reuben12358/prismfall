#!/usr/bin/env python3
"""Saltmere interiors 143-145, map builder 10 (job 5: the last stock templates in Saltmere re-skinned).

  143 Saltmere Harbour Office   the customs house's long room (tileset 34, interiorkit): the harbourmaster's counter, the
                                tide board and the chart table, ledgers to the ceiling, the free port's seized crates
  144 Saltwife's House          a salt-raker's cottage (tileset 34): the hearth, the salt crocks, Sella's bed and rug
  145 Pageant Hall              the Lantern Theatre (tileset 54 "PF Rejuv Halls", hallkit 'stage'): the stalls under a
                                chandelier, the stage with its painted drop, the wings - backstage left (the chorus, the
                                prop room shelf, Vesper and Lyra after the Pageant) and right (Dorian's dressing room and
                                Marguerite Fane's paint loft under the torn backdrop)
Doors: SM_HARBOUR (146), SM_HOUSE1 (140), SM_PAGEANT (140) - the same links, so nothing moves outside.
Story: story/20_SCRIPT_CH0-2.md (the Pageant; Map 145 backstage EV "Vesper", S190, SPINE Rev 19: Lyra is her partner).
Run: python3 -I layouts/saltmere_interiors.py && python3 -I build.py 143 144 145"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from interiorkit import Room, write, HERE
import hallkit as K
from hallkit import MI, MG, NM, CH, CU
import yaml

M = {'MapPosition': [0, 10, 25]}


def talk(at, name, sprite, lines, d='down', move=None):
    pg = {'graphic': {'sprite': sprite, 'dir': d}, 'trigger': 'action', 'commands': list(lines)}
    if move: pg['move'] = move
    return {'type': 'event', 'name': name, 'at': list(at), 'pages': [pg]}


def obj(at, name, lines):
    return {'type': 'event', 'name': name, 'at': list(at), 'pages': [{'trigger': 'action', 'commands': list(lines)}]}


# ====================================================================================================== 143
def harbour_office():
    r = Room(17, 8)
    for fx in (3, 13): r.window(fx)
    r.tf('map_wall', 6, -1); r.tf('clock', 10, -2); r.tf('bookcase', 0, -1); r.tf('bookcase', 15, -1); r.sf('shelves2', 1, -3) if False else None
    r.tf('counter4', 5, 2); r.tf('counter4', 9, 2)                             # the long counter across the room
    r.tf('desk_dark', 7, 0); r.tf('books_open', 9, 0); r.tf('console', 12, 0)    # the clerk's desk; the brass kiosk's alcove
    r.rug(5, 4, 7, 3); r.tf('table_dark', 7, 5)                                   # the chart table on the waiting rug
    r.tf('crates3', 0, 4); r.tf('crate', 14, 5); r.tf('crate_i', 15, 3); r.tf('barrel_b', 3, 6); r.tf('barrel_y', 4, 6)
    r.tf('lifering', 13, -1); r.tf('bench_v', 0, 1); r.tf('fern_big', 16, 1); r.tf('shelf_low', 2, 2)
    s = r.spec({'id': 143, 'name': 'Saltmere Harbour Office', 'parent': 140, 'bgm': 'Lerucean Town', 'biome': 'interior',
                'tone': [6, 2, -8, 0], 'metadata': M}, [
        {'type': 'npc', 'name': 'Harbourmaster', 'at': r.at(8, 1), 'sprite': 'trainer_SAILOR', 'dir': 'down',
         'commands': [{'script': 'pfm_audience(:harbourmaster)'},
                      'Harbourmaster: Free port means free. No Crown tariffs, no Meridian tolls. Long may it last.']},
        talk(r.at(12, 2), 'Customs clerk', 'NPC 12', ['Customs clerk: Manifests to the left, complaints to the right, the kiosk to the far right.',
                                                     'Customs clerk: The kiosk is a Meridian grant. It counts people. We count crates. One of us is happier.']),
        obj(r.at(7, 4), 'Tide board', ["THE TIDE BOARD. High water 6:12 and 18:40. Under it in chalk: 'Legion barge expected. Do not stare.'"]),
        obj(r.at(1, 3), 'Seized crates', ['Crates stamped SEIZED - ISENMAR CUSTOMS. Someone has added, in pencil, "...in Saltmere? Seized by whom?"']),
        talk(r.at(2, 5), 'Sailor waiting', 'trainer_SAILOR', ['Sailor: Three hours for a stamp. In Isenmar it takes three days. I am, therefore, delighted.'], d='right'),
    ], 'SM_HARBOUR')
    return s


# ====================================================================================================== 144
def saltwife_house():
    r = Room(12, 7)
    for fx in (2, 9): r.window(fx)
    r.tf('kitchen', 0, -1); r.tf('shelf_bottles', 5, -1); r.tf('painting3', 7, -2); r.tf('clock', 11, -2)
    r.rug(3, 2, 5, 3); r.tf('table_tea', 4, 3)
    r.tf('bed_blue', 9, 0); r.tf('barrel_y', 0, 4); r.tf('barrel_b', 1, 5); r.tf('bucket', 2, 5); r.tf('rodbucket', 11, 5)
    r.tf('stool', 6, 4); r.tf('plant_s', 8, 5); r.tf('dresser', 5, 5) if False else None
    s = r.spec({'id': 144, 'name': "Saltwife's House", 'parent': 140, 'bgm': 'Lerucean Town', 'biome': 'interior',
                'tone': [6, 2, -6, 0], 'metadata': M}, [
        {'type': 'npc', 'name': 'Saltwife', 'at': r.at(6, 2), 'sprite': 'NPC 28', 'dir': 'down',
         'commands': [{'script': 'pfm_audience(:saltwife)'},
                      'Saltwife: Forty years raking the pans. The salt tastes the same as ever. Only place in Velmora that can say so.']},
        obj(r.at(1, 3), 'Salt crocks', ['Salt crocks, one per year, labelled in a careful hand. The oldest says AF 260. It is still full.']),
        obj(r.at(9, 4), 'Rake', ["A salt rake worn pale at the grip. The teeth are filed to the exact gap of the Upper Town's pan bunds."]),
    ], 'SM_HOUSE1')
    return s


# ====================================================================================================== 145
W, H = 38, 26
WL = (1, 8); ST = (11, 26); WR = (29, 36)          # the left wing, the stage, the right wing (floor columns, inclusive)


def theatre_grid():
    g = [['#'] * W for _ in range(H)]
    def fill(x0, x1, y0, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1): g[y][x] = c
    for a, b in (WL, ST, WR):
        fill(a, b, 1, 2, 'W'); fill(a, b, 3, 9, '.')
    fill(9, 10, 7, 8, '.'); fill(27, 28, 7, 8, '.')                              # the wing openings
    fill(ST[0], ST[1], 10, 10, 'p'); fill(18, 19, 10, 10, 'S')                   # the stage lip and the steps down
    fill(1, 10, 11, 12, 'W'); fill(27, 36, 11, 12, 'W')                          # the house's north wall beside the stage
    fill(ST[0], ST[1], 11, 12, ',')                                              # the apron
    fill(1, 36, 13, 23, ',')                                                     # the stalls
    for y in list(range(14, 18)) + list(range(19, 23)):
        for x in list(range(3, 16)) + list(range(22, 35)): g[y][x] = 's'
    fill(17, 20, 24, 24, ',')                                                    # the lobby step and the doors
    return [''.join(r) for r in g]


def pageant_hall(old145):
    rows = theatre_grid()
    cls = {'#': 'void', 'W': 'wall', 'p': 'lip', 'S': 'stair', 's': 'seat', ',': 'floor2', '.': 'floor'}
    h = K.Hall(rows, 'stage', cls, seed=145)
    rnd = h.r
    BOARDS = [MI(1241), MI(1242), MI(1243)]
    for y, row in enumerate(rows):                                               # the house carpet: dark red damask
        for x, ch in enumerate(row):
            if ch in ',s': h.put(NM(685), x, y, 0)
    for y in range(3, 10):                                                       # the stage: polished boards, the drop behind
        for x in range(ST[0], ST[1] + 1): h.put(rnd.choice(BOARDS), x, y, 0)
    for x in range(ST[0] + 1, ST[1] + 1):                                        # the painted drop: Saltmere at dusk
        for y in range(3, 6): h.put(CU('backdrop_%d_%d' % (x - ST[0] - 1, y - 3)), x, y, 0)
        h.put(NM(904) if x == ST[0] + 1 else NM(906) if x == ST[1] else NM(905), x, 3, 2)
    for x in range(ST[0], ST[1] + 1):                                            # the gilded beam over the proscenium
        h.put(NM(393), x, 1, 0); h.put(CU('beam_l') if x == ST[0] else CU('beam_r') if x == ST[1] else CU('beam_mid'), x, 1, 1)
    h.block([[CU('crest_0'), CU('crest_1'), CU('crest_2')]], 17, 1, 2)
    for y in range(4, 10):                                                       # the house curtain, gathered both sides
        h.put(NM(920) if y == 9 else NM(912), ST[0], y, 2); h.put(NM(922) if y == 9 else NM(914), ST[1], y, 2)
    for x, y in ((14, 7), (18, 8), (23, 7)): h.put(CU('mark'), x, y, 1)
    h.put(CU('rostrum'), 21, 6, 1)
    for x in range(ST[0], ST[1] + 1):                                            # footlights along the lip, their glow above
        if x not in (18, 19): h.put(CU('footlight'), x, 10, 0); h.put(0, x, 10, 1)
        h.put(CU('glow'), x, 9, 2)
    for x in range(ST[0], ST[1] + 1):                                            # the apron boards
        for y in (11, 12): h.put(rnd.choice(BOARDS), x, y, 0)
    # the stalls: a red runner up the centre aisle, the chandeliers, urns and palms at the side aisles
    for y in range(13, 25):
        r_ = 0 if y == 13 else (2 if y == 24 else 1)
        for i in range(4): h.put(NM([[773, 774, 774, 775], [781, 782, 782, 783], [789, 790, 790, 791]][r_][i]), 17 + i, y, 1)
    for cx in (8, 28):
        h.block([[0, NM(779), 0], [0, NM(779), 0], [NM(776), NM(787), NM(778)], [NM(784), NM(785), NM(786)]], cx, 15, 2)
    for x in (1, 36): h.obj('urn', x, 14); h.obj('urn', x, 21)
    h.block([[NM(518), NM(519)], [NM(526), NM(527)]], 1, 17, 1); h.block([[NM(518), NM(519)], [NM(526), NM(527)]], 35, 17, 1)
    h.obj('poster_lady', 3, 11); h.obj('poster_rain', 7, 11) if False else None
    h.obj('poster_green', 29, 11); h.obj('poster_rain', 33, 11)
    h.put(MG(1731), 17, 24, 1); h.put(MG(1732), 18, 24, 1); h.put(MG(1732), 19, 24, 1); h.put(MG(1733), 20, 24, 1)
    # the left wing: the chorus's prop crates, the prop room shelf, flats stacked against the wall, a costume rail
    for x in range(WL[0], WL[1] + 1):
        for y in range(3, 10): h.put(rnd.choice(BOARDS), x, y, 0)
    for x in range(9, 11):
        for y in (7, 8): h.put(rnd.choice(BOARDS), x, y, 0)
    h.obj('shelf', 1, 2); h.obj('shelf', 3, 2)
    h.block([[CU('flat_A'), CU('flat_B'), CU('flat_C')]], 5, 3, 1)
    h.stamp('hb_crates4', 6, 7) if False else None
    for x, y, n in ((2, 8, 'hb_crates4'), (6, 8, 'hb_boxes'), (8, 5, 'hb_barrel')):
        h.stamp(n, x, y, zmap={0: 1, 1: 1, 2: 2})
    h.obj('lantern', 1, 6)
    h.obj('rope_h', 5, 9) if False else None
    # the right wing: Dorian's dressing room (couch, rug, mirror-lights) and the paint loft under the torn drop
    for x in range(WR[0], WR[1] + 1):
        for y in range(3, 10): h.put(rnd.choice(BOARDS), x, y, 0)
    for x in range(27, 29):
        for y in (7, 8): h.put(rnd.choice(BOARDS), x, y, 0)
    h.obj('rug_mg', 30, 5); h.obj('couch_l', 29, 5); h.obj('plant', 36, 3)
    for x, n in ((33, 'drop_forest_top'), (34, 'drop_throne_top'), (35, 'drop_forest_top')):
        h.put(CU(n), x, 3, 2)
    for x, n in ((33, 'drop_forest_bot'), (35, 'drop_ship_bot')):
        h.put(CU(n), x, 4, 2)
    for x, n in ((33, 'vat_r'), (34, 'vat_b'), (35, 'vat_y')): h.obj(n, x, 8)
    h.put(CU('easel') if False else CU('flat_B_hung'), 36, 6, 1)
    spec = {'id': 145, 'name': 'Pageant Hall', 'parent': 140, 'biome': 'interior', 'bgm': 'Lerucean Town', 'tone': [4, 0, -6, 0],
            'metadata': M}
    spec.update(h.write(145))
    # ---- events
    ev = [{'type': 'exit', 'at': [18, 24], 'link': 'SM_PAGEANT'}, {'type': 'exit', 'at': [19, 24], 'link': 'SM_PAGEANT'}]
    pg = [e for e in old145['events'] if e.get('name') == 'Pageant'][0]
    pg = dict(pg); pg['at'] = [18, 7]
    ev.append(pg)
    ev += [obj([2, 3], 'Prop shelf', ['The prop room shelf: crowns, a papier-mache Plate, three identical daggers and a labelled jar of "STAGE BLOOD (JAM)".']),
           obj([34, 4], 'Torn backdrop', ["An old drop, torn top to bottom: a forest on one side, a throne room on the other. Someone has been painting the tear shut, leaf by leaf."]),
           obj([31, 3], "Dorian's mirror", ["Dorian's mirror, ringed with bulbs. Telegrams tucked in the frame: 'BREAK A LEG', 'BREAK BOTH', 'PAY YOUR RENT'."]),
           talk([4, 6], 'Chorus singer', 'NPC 13', ['Chorus singer: We sing the hymns between the scenes. Tonight the hymn was screaming. We were very good at it.'], d='right'),
           talk([7, 4], 'Chorus singer 2', 'NPC 17', ['Chorus singer: The Octave lend us their voices for the Pageant. They make the rest of us sound like gulls.'], d='down'),
           talk([25, 12], 'Usher', 'NPC 18', ['Usher: Programmes, a copper! The Pageant of the Prismfall! Dorian Pell in the role of everyone!'], d='down')]
    # Vesper and Lyra, backstage left after the Pageant (S190; SPINE Rev 19: Lyra replaces Carol)
    V = lambda t: '\\PN... ' if False else t
    duet = [{'script': 'setBattleRule("double")'}, {'script': 'setBattleRule("canLose")'},
            {'script': 'TrainerBattle.start(:OCTAVE_VESPER, "Vesper", 0, :OCTAVE_SINGER, "Lyra", 0)'},
            'Vesper: There. Your hands have stopped shaking. So have mine.']
    ev.append({'type': 'event', 'name': 'Vesper', 'at': [5, 5], 'pages': [
        {'commands': []},
        {'cond': {'switch': 'CH3_PAGEANT_DONE'}, 'graphic': {'sprite': 'NPC 14', 'dir': 'down'}, 'trigger': 'action', 'commands': [
            '(Chorus singers in Prism Choir white sit on prop crates with blankets round them. A young woman in the same white kneels on the boards - not to you. To Understudy.)',
            "Vesper: Oh. Hello, little one. You're new.",
            "Vesper: I'm Vesper. Vesper Lindqvist. We're the Octave: eight singers, eight Eevee. I just conduct. The Choir lends us to the Pageant for the hymns.",
            "Vesper: (to Understudy) It hasn't decided which Imprint it belongs to yet.",
            'Vesper: (to you, after a long look) Neither have you, I think.',
            {'choices': ['What does that mean?', '...'], 'cancel': 1, 'branches': [
                ["Vesper: Only what it says. I sing; I don't explain. The Hierophant says I'd make a terrible priest."],
                ["Vesper: You don't have to answer. Nobody answers me. It's restful."]]},
            'Vesper: We all lost our homes in the Glassfall. The Choir raised us, and when the others were grown it sent each of them to live beside a Plate, one each. They say an Eevee becomes what it lives beside.',
            'Vesper: Would you sing a duet with us before we go? It helps, after a fright. Lyra, come here.',
            "(A girl in Choir grey, humming, with an Eevee at her heels: the Octave's Elowen singer, going home to Briarwick.)",
            {'choices': ['Sing.', 'Not tonight.'], 'cancel': 1, 'branches': [
                duet, ["Vesper: Then at the Festival. We'll all be there. We always are."]]},
            "Vesper: Look after it. Whatever it becomes, it'll become it because of you.",
            {'switch': ['VESPER_MET_SALTMERE', True]},
            {'script': 'pf_trial_talk(:VESPER_SALTMERE)'}]},
        {'cond': {'switch': 'VESPER_MET_SALTMERE'}, 'graphic': {'sprite': 'NPC 14', 'dir': 'down'}, 'trigger': 'action', 'commands': [
            {'script': 'pf_trial_talk(:VESPER_SALTMERE)'}]}]})
    ev.append({'type': 'event', 'name': 'Lyra', 'at': [6, 5], 'pages': [
        {'commands': []},
        {'cond': {'switch': 'CH3_PAGEANT_DONE'}, 'graphic': {'sprite': 'NPC 16', 'dir': 'left'}, 'trigger': 'action', 'commands': [
            "Lyra: (humming) Sorry - it's the Briarwick tune. The Wood hums it back if you sing it right. My Eevee thinks so, anyway."]}]})
    ev.append({'type': 'event', 'name': 'Eevee (Lyra)', 'at': [7, 6], 'pages': [
        {'commands': []},
        {'cond': {'switch': 'CH3_PAGEANT_DONE'}, 'graphic': {'sprite': 'Followers/EEVEE', 'dir': 'left'}, 'trigger': 'action',
         'commands': ['(The Eevee sniffs at Understudy, then sits very straight, as if it has been told to.)']}]})
    # the audience before the show (sit facing the stage)
    seats = [(x, y) for y in (14, 15, 16, 17, 19, 20, 21, 22) for x in (3, 4, 6, 9, 11, 14, 15, 22, 23, 26, 28, 31, 33, 34)]
    rnd.shuffle(seats)
    SP = ['NPC 02', 'NPC 04', 'NPC 06', 'NPC 09', 'NPC 10', 'NPC 13', 'trainer_LADY', 'trainer_GENTLEMAN', 'trainer_BEAUTY', 'NPC 21', 'NPC 24', 'NPC 26']
    LINES = ['Shh! It\'s starting!', 'The Loyal Three piece is my favourite.', "Is that the real Dorian Pell? Of course it is. Who else would wear that coat.",
             'I come every year. The Plates fall a little differently every time.', "(whispering) The chandelier is new. The rope isn't."]
    for i, (x, y) in enumerate(seats[:18]):
        talkable = rows[y][x - 1] == ',' or rows[y][x + 1] == ',' or rows[y - 1][x] == ',' or rows[y + 1][x] == ','
        e = {'type': 'event', 'name': 'Audience' if i == 0 else 'Audience %d' % (i + 1), 'at': [x, y],
             'pages': [{'graphic': {'sprite': SP[i % len(SP)], 'dir': 'up'}, 'trigger': 'action',
                        'commands': [LINES[i % len(LINES)]] if talkable else []}]}
        ev.append(e)
    spec['events'] = ev
    return spec


def main():
    p = os.path.join(HERE, 'specs', '141_saltmere_interiors.yaml')
    docs = [d for d in yaml.safe_load_all(open(p)) if d]
    old = {d['id']: d for d in docs}
    keep = [d for d in docs if d['id'] in (141, 142)]
    if len(keep) != len(docs):                                                    # 143-145 move to this script's file
        hdr = '# Saltmere interiors (141-142). Story: story/04_ACT_I.md Chapter 3. 143-145: specs/143_saltmere_rooms.yaml (layouts/saltmere_interiors.py).\n'
        open(p, 'w').write(hdr + '\n---\n'.join(yaml.safe_dump(d, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True) for d in keep))
        json_old = old[145]
        yaml.safe_dump(json_old, open(os.path.join(HERE, 'layouts', 'old_145_pageant_hall.yaml'), 'w'), sort_keys=False, width=160, allow_unicode=True)
    old145 = yaml.safe_load(open(os.path.join(HERE, 'layouts', 'old_145_pageant_hall.yaml')))
    specs = [harbour_office(), saltwife_house(), pageant_hall(old145)]
    write('143_saltmere_rooms.yaml', specs, '# Saltmere 143-145. WRITTEN BY layouts/saltmere_interiors.py (map builder 10) - edit that script.\n')
    print('wrote specs/143_saltmere_rooms.yaml (143, 144, 145)')


if __name__ == '__main__':
    main()
