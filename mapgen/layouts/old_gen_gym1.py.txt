#!/usr/bin/env python3
"""Writes specs/130_loomhouse_gym.yaml (Gym 1, rooms 130-133) from design/GYM_PUZZLES.md 'Gym 1'.
The puzzle events are repetitive, so they are generated here; edit this script, then run build.py."""
import os, json, random
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
V_A, V_B, V_C = 305, 306, 307           # = flags.yaml GYM1_A/B/C           # heddle variables (gym 1 block 305-309)
S_ALPHA, S_BETA, S_GAMMA = 305, 306, 307  # cord switches for the Canopy Lofts
FIELD_RULE = 'setBattleRule("field", :SILKWOOD)'


CU = json.load(open(os.path.join(HERE, 'data', 'compose_wilds_offsets.json')))['custom']['names']
PLANK = 3807                      # cross-board walkway tile (passable, priority 0) used as the plank event graphic


def say(who, expr, text):
    return '\\pf[%s,%s]%s: %s' % (who.upper(), expr, who.capitalize(), text)


def key(m, k): return "$game_self_switches[[%d, 0, '%s']]" % (m, k)


def decorate(rows, seed, extra=()):
    """Builder 3: canopy-gym dressing on tileset 40 for a glyph grid (palettes/loom.yaml).
    Deck lips on the drop below every deck edge, treetops far below in the dark, silk webs in the corners,
    curtains on 'o' cells. Returns a `tiles:` list."""
    r = random.Random(seed); g = [list(l) for l in rows]; H, W = len(g), len(g[0]); out = []; used = set()
    walk = lambda x, y: 0 <= x < W and 0 <= y < H and g[y][x] in '._o'
    def put(t, x, y, z):
        if (x, y, z) in used or not (0 <= x < W and 0 <= y < H): return
        used.add((x, y, z)); out.append({'tile': t, 'at': [x, y], 'layer': z})
    for y in range(H):
        for x in range(W):
            c = g[y][x]
            if c == 'o':
                put(CU['curtain'] + 8, x, y, 1)
                if y > 0 and g[y - 1][x] != 'o': put(CU['curtain'], x, y - 1, 2)
            elif c in 'v#':
                if walk(x, y - 1):                                   # the deck's front lip with its posts
                    put(3811 if not walk(x - 1, y - 1) else (3813 if not walk(x + 1, y - 1) else 3812), x, y, 1)
                elif r.random() < 0.06:
                    put(CU['strand_h'] if r.random() < 0.5 else CU['strand_d1'], x, y, 2)
            elif c in '._' and r.random() < 0.05:
                put(r.choice([1164, 1172, 8136]) if c == '.' else 1164, x, y, 1)
    for y in range(H):                                              # web fans where the deck meets the drop at corners
        for x in range(W):
            if g[y][x] in '._' and not walk(x - 1, y) and not walk(x, y - 1) and r.random() < 0.6: put(CU['web_nw'], x, y, 2)
            elif g[y][x] in '._' and not walk(x + 1, y) and not walk(x, y - 1) and r.random() < 0.6: put(CU['web_ne'], x, y, 2)
    MAT = json.load(open(os.path.join(HERE, 'data', 'compose_wilds_offsets.json')))['materials']
    LANT, GLOW = MAT['offset'] + MAT['names']['lantern'], MAT['offset'] + MAT['names']['glow']
    for y in range(2, H - 1):                                        # lantern posts on outer deck corners, a warm pool beside each
        for x in range(1, W - 1):
            corner = g[y][x] == '.' and g[y + 1][x] in 'v#' and (g[y][x - 1] in 'v#' or g[y][x + 1] in 'v#')
            if corner and g[y - 1][x] == '.' and g[y - 2][x] in '.v#' and (x, y, 1) not in used and r.random() < 0.8:
                put(LANT + 16, x, y, 1); put(LANT + 8, x, y - 1, 2); put(LANT, x, y - 2, 2)
                gx = x + 1 if g[y][x + 1] == '.' else x - 2
                for dx in (0, 1):
                    for dy in (0, 1):
                        if 0 <= gx + dx < W and g[y - 1 + dy][gx + dx] in '._': put(GLOW + dy * 8 + dx, gx + dx, y - 1 + dy, 2)
    for y in range(1, H - 1):                                        # sacks of raw silk, jars of dye, spare cocoons along the deck edges
        for x in range(1, W - 1):
            if g[y][x] == '.' and (g[y - 1][x] in 'v#') and (x, y, 1) not in used and r.random() < 0.18:
                put(r.choice([3507, 3521, 3523, 3507, CU['cocoon_low']]), x, y, 1)
    for name, x, y in extra:                                         # looms, cocoons: multi-tile custom objects
        w, h, base = {'loom': (3, 3, 1), 'cocoon': (1, 2, 1), 'cocoon_big': (2, 3, 2), 'web_big': (3, 3, 0), 'shaft': (2, 4, 0)}[name]
        for dy in range(h):
            for dx in range(w):
                put(CU[name] + dy * 8 + dx, x + dx, y + dy, 1 if (dy >= h - base and base) else 2)
    return out


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
            pages = [{'cond': ({'var': [var, k]} if k else None), 'graphic': {'tile': PLANK}}]
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
                'to': {'map': 133, 'x': 8, 'y': 13, 'dir': 'up'}, 'arrive': [21, 3, 'down']})
    evs.append({'type': 'item', 'at': [13, 5], 'item': 'SILVERPOWDER'})
    evs.append(trainer((13, 21), 'BUGCATCHER', 'Hollis', 3, 'left'))
    evs.append(trainer((20, 15), 'POKEMONRANGER_M', 'Ash', 3, 'left'))
    return '\n'.join(''.join(r) for r in g), evs


def trainer(at, ttype, name, sight, d, intro=None, after=None, sprite=None):
    return {'type': 'trainer', 'at': list(at), 'sight': sight, 'dir': d, 'sprite': sprite or 'trainer_' + ttype,
            'trainer': [ttype, name], 'rules': [FIELD_RULE],
            'intro': intro or 'Every thread has its place. Let me show you mine!',
            'after': after or 'The Warden says the loom remembers every knot.'}


def reveal_if(cond, names):
    """Parallel helper: once per map load, if `cond` holds, switch on self switch A of the named events (they appear)."""
    rb = ("%%w[%s].each do |n|\n  ev = $game_map.events.values.find { |e| e.name == n }\n"
          "  $game_self_switches[[$game_map.map_id, ev.id, 'A']] = true if ev\nend\n$game_map.need_refresh = true") % ' '.join(names)
    return {'type': 'event', 'name': 'Reveal helper', 'at': [0, 0], 'pages': [
        {'trigger': 'parallel', 'commands': [{'if': cond, 'then': [{'script': rb}], 'else': []}, {'selfswitch': ['A', True]}]},
        {'cond': {'self': 'A'}}]}


FOYER = ["vvvvvvvvvvvvvvv",
         "vvvvvv...vvvvvv",
         "vvv.........vvv",
         "vv...........vv",
         "v.............v",
         "v.............v",
         "v......._.....v",
         "v......._.....v",
         "vv......_....vv",
         "vv......_....vv",
         "vvv....._...vvv",
         "vvvvvv..._vvvvv",
         "vvvvvvv...vvvvv"]
SPINDLE = ["vvvvvvvvvvvvvvv",
           "vvvvv.....vvvvv",
           "vvv.........vvv",
           "vv...........vv",
           "vv...........vv",
           "v.............v",
           "v.............v",
           "v.............v",
           "vv...........vv",
           "vv...........vv",
           "vvv.........vvv",
           "vvvvv.....vvvvv",
           "vvvvvv._._vvvvv",
           "vvvvvvv_._vvvvv",
           "vvvvvvv...vvvvv"]


def main():
    docs = []
    M = {'MapPosition': [0, 12, 22]}
    # ---------------------------------------------------------------- 130 Foyer
    spiral = [
        say('TAMSIN', 'panic', "Sorry — the gym's a bit tangled today — sorry —"),
        {'choices': ["It's fine.", "Stop apologizing."], 'cancel': 1, 'branches': [
            ["\\pf[TAMSIN,panic,sweat]Tamsin: Sorry for saying sorry so much. That's annoying. Sorry."],
            ["\\pf[TAMSIN,shocked,shock]Tamsin: Right! Yes! Sorr—", say('TAMSIN', 'panic', "I nearly did it again. I'm so sorry.")]]},
        say('TAMSIN', 'sad', "..."),
        say('TAMSIN', 'deadpan', "I'm going to go and stand in the web now."),
        {'move': {'who': 0, 'route': ['up', 'up', 'up', 'up', 'up']}}, {'selfswitch': ['A', True]}]
    docs.append({'id': 130, 'name': 'Loomhouse Gym - Foyer', 'parent': 120, 'palette': 'loom', 'biome': 'canopy_gym', 'bgm': 'Gym', 'field': 'SILKWOOD',
                 'rubric': True, 'tone': [-10, -6, -18, 10], 'metadata': M, 'map': '\n'.join(FOYER),
                 'tiles': decorate(FOYER, 130, [('loom', 2, 3), ('loom', 10, 3), ('cocoon', 1, 4), ('cocoon', 13, 4), ('web_big', 6, 0)]),
                 'events': [
                     {'type': 'exit', 'at': [8, 12], 'link': 'BW_GYM', 'se': 'Door exit'},
                     {'type': 'npc', 'name': 'Gym guide', 'at': [10, 8], 'sprite': 'NPC 01', 'dir': 'left', 'commands': [
                         "Gym Guide: Challenger! This is the Loomhouse. Bug-types, and the Silkwood field. Fire and Flying do well. Grass does not. "
                         "I say this to everyone and half of them bring a Bulbasaur.",
                         "Gym Guide: The puzzle: three looms, three colors of plank. Pull a shuttle and one color extends while another retracts. "
                         "Old Mother Loom built it to teach patience. Tamsin added the safety nets. And the apology cards.",
                         "The pattern card reads: \"Red lifts the warp and the weft. Gold lifts the weft and the woof. Green lifts the woof and the warp.\""]},
                     {'type': 'sign', 'at': [4, 9], 'name': 'Apology card',
                      'text': "A card pinned by the trapdoor: \"If you have fallen, I'm so sorry. Stairs are to your left. — T.L.\""},
                     {'type': 'sign', 'at': [12, 6], 'name': 'Portrait',
                      'text': "A fierce old woman at a loom. Brass plate: \"Mother Loom, Warden AF 247–299. 'Twist it or lose it.'\""},
                     {'type': 'event', 'name': 'Tamsin', 'at': [7, 4], 'pages': [
                         {'graphic': {'sprite': 'trainer_LASS', 'dir': 'down'}, 'commands': spiral},
                         {'cond': {'self': 'A'}}]},
                     {'type': 'event', 'name': 'First loom', 'at': [3, 5], 'pages': [{'commands': [
                         {'if': 'pfm_quest?(:locked_ledger) && !pfm_has?(:LEDGERKEY)',
                          'then': ['A small brass key is tied into the very first warp thread.', {'script': 'pfm_item(:LEDGERKEY, 1, "Ledger Key")'}],
                          'else': ["Mother Loom's first loom. The warp is still strung, and the pattern stops mid-row, as if she meant to come back to it."]}]}]},
                     {'type': 'warp', 'name': 'To Weaving Hall', 'at': [7, 1], 'link': 'GYM1_HALL',
                      'to': {'map': 131, 'x': 12, 'y': 19, 'dir': 'up'}, 'arrive': [7, 2, 'down']}]})
    # ---------------------------------------------------------------- 131 Weaving Hall (heddle bridges)
    hall_events = plank_events(V_A, range(3, 7), 'A') + plank_events(V_B, range(9, 12), 'B') + \
        plank_events(V_C, range(14, 18), 'C')
    juno_hall = ("$game_map.events.values.count { |e| e.name[/^Trainer\\(/] && $game_self_switches[[131, e.id, 'A']] } >= 2")
    hall_events += [lever('Red lever', 3, 18, V_A, V_B, 'red'), lever('Gold lever', 12, 18, V_B, V_C, 'gold'),
                    lever('Green lever', 21, 18, V_C, V_A, 'green'),
                    {'type': 'warp', 'name': 'Back to Foyer', 'at': [12, 20], 'to': {'map': 130, 'x': 7, 'y': 2, 'dir': 'down'}},
                    {'type': 'warp', 'name': 'Up to Canopy Lofts', 'at': [12, 0], 'to': {'map': 132, 'x': 2, 'y': 22, 'dir': 'up'}},
                    trainer((12, 13), 'BUGCATCHER', 'Nell', 3, 'down', "A thread alone is just string!", "Two of us would've had you."),
                    trainer((21, 7), 'LASS', 'Orla', 3, 'down', "I pulled the red shuttle. Don't pull the red shuttle first.",
                            "...Did you pull the red shuttle?"),
                    trainer((3, 1), 'GENTLEMAN', 'Bram', 3, 'down', "Granny Loom taught me this hall. Tamsin taught me to say sorry when I win.",
                            "I don't need to say it, then."),
                    {'type': 'sign', 'at': [14, 19], 'name': 'Safety net',
                     'text': "A safety net is strung under the ledge. A card is pinned to it: \"Sorry! — T.L.\""},
                    reveal_if(juno_hall, ['Juno']),
                    {'type': 'event', 'name': 'Juno', 'at': [11, 19], 'pages': [
                        {'commands': []},
                        {'cond': {'self': 'A'}, 'graphic': {'sprite': 'trainer_RIVAL2', 'dir': 'up'}, 'commands': [
                            {'if': key(131, 'JUNO'), 'then': [say('JUNO', 'happy', "Go on! I'm being loud! In my head!")],
                             'else': ["(Juno is at the hall's entrance, eating a honey-silk bun.)",
                                      say('JUNO', 'happy', "I made it! Go on! I'll be loud!"), {'script': key(131, 'JUNO') + ' = true'}]}]}]}]
    hall = weaving_hall()
    docs.append({'id': 131, 'name': 'Loomhouse Gym - Weaving Hall', 'parent': 130, 'palette': 'loom', 'biome': 'canopy_gym', 'bgm': 'Gym', 'rubric': True,
                 'field': 'SILKWOOD', 'tone': [-10, -6, -18, 10], 'metadata': M, 'map': hall,
                 'tiles': decorate(hall.split('\n'), 131, [('loom', 15, 0), ('loom', 6, 0), ('cocoon', 1, 7), ('cocoon', 23, 12), ('shaft', 9, 13)]),
                 'events': hall_events})
    # ---------------------------------------------------------------- 132 Canopy Lofts (spool ziplines)
    lofts, loft_events = canopy_lofts()
    plats = {1: (2, 22), 2: (12, 20), 3: (4, 12), 4: (19, 14), 5: (12, 6), 6: (20, 3)}
    lrows = lofts.split('\n'); zip_tiles = []; seen = set()
    for a, b in ((1, 2), (1, 3), (2, 4), (3, 5), (3, 4), (4, 2), (4, 6), (5, 3), (5, 6)):     # every spool route (GYM_PUZZLES table)
        (x0, y0), (x1, y1) = plats[a], plats[b]
        n = max(abs(x1 - x0), abs(y1 - y0))
        for i in range(1, n):
            x = round(x0 + (x1 - x0) * i / n) + 1; y = round(y0 + (y1 - y0) * i / n)
            if lrows[y][x] != 'v' or (x, y) in seen: continue
            dx, dy = x1 - x0, y1 - y0
            t = CU['strand_h'] if abs(dx) > 2 * abs(dy) else (CU['strand_v'] if abs(dy) > 2 * abs(dx) else (CU['strand_d1'] if dx * dy > 0 else CU['strand_d2']))
            seen.add((x, y)); zip_tiles.append({'tile': t, 'at': [x, y], 'layer': 2})
    for e in loft_events:
        if e.get('type') == 'trainer' and e['trainer'][1] == 'Hollis':
            e.update(intro="Ride the spools wrong and you go in circles. I've been going in circles since lunch.",
                     after="...Lunch was a while ago.")
        if e.get('type') == 'trainer' and e['trainer'][1] == 'Ash':
            e.update(intro="Rangers learn the high lines first. Let's see if you can keep your feet up here.",
                     after="You've got canopy legs. Tamsin'll like that.")
    docs.append({'id': 132, 'name': 'Loomhouse Gym - Canopy Lofts', 'parent': 130, 'palette': 'loom', 'biome': 'canopy_gym', 'bgm': 'Gym', 'rubric': True,
                 'field': 'SILKWOOD', 'tone': [-14, -8, -20, 15], 'metadata': M, 'map': lofts,
                 'tiles': zip_tiles + decorate(lofts.split('\n'), 132, [('web_big', 7, 9), ('web_big', 15, 17), ('web_big', 5, 2), ('web_big', 16, 9), ('web_big', 1, 16), ('shaft', 16, 7)]), 'events': loft_events})
    # ---------------------------------------------------------------- 133 The Spindle (Warden battle, confession)
    win = [
        say('TAMSIN', 'shocked', "...It held, and you still came through it."),
        say('TAMSIN', 'happy', "That's allowed. Granny said the room's meant to lose to the right person. I didn't think I'd ever meet one."),
        {'script': 'Prismfall.award_badge(1)'},
        "(You open the Badge Case and set the badge in. A faint hum: one clear note.)",
        "\\pf[JUNO,happy,question]Juno: Ooh. Is it supposed to do that?",
        say('TAMSIN', 'neutral', "I don't think they do that. ...Do they do that?"),
        {'script': 'pbReceiveItem(:TM89)'},
        say('TAMSIN', 'neutral', "That's the Accord's word that you may use Cut, and that Pokémon up to level nineteen will heed you."),
        say('TAMSIN', 'sad', "\\PN... could you come up to the loft? There's something I should say to someone, and you've an honest sort of silence."),
        {'tone': [-255, -255, -255, 0, 12]}, {'wait': 14}, {'tone': [-30, -20, -10, 30, 12]},
        "(The loft above the Spindle: a ledger open on a table, a contract with a gold sunburst seal. Tamsin won't sit.)",
        say('TAMSIN', 'sad', "That masked woman at the pylon. She was right. I signed it."),
        say('TAMSIN', 'sad', "Briarwick's bankrupt. It has been for three years. Gran hid it. I found the accounts the week I buried her."),
        say('TAMSIN', 'sad', "Meridian offered four hundred thousand for \"stewardship rights\". One pylon. Free light. I signed it by myself, at night, so nobody would have to know how bad it was."),
        say('TAMSIN', 'crying', "And now the Glasswood's walking up the survey line like it was invited. Fourteen moths this week. I count them. I count them every morning."),
        say('TAMSIN', 'sad', "The guild meets tonight. Tell me what to do. Please. I've run out of thread."),
        {'if': 'pf_choice(:ch2_tamsin)', 'then': ["(You've already given her your answer.)"], 'else': [
            {'choices': ["Tell them the truth. I'll stand next to you.", "They deserve to know. If you won't say it, I will.", "It's your secret. I won't tell."],
             'cancel': 0, 'branches': [
                [{'script': 'pf_choose(:ch2_tamsin, :help_confess)'},
                 say('TAMSIN', 'shocked', "Next to me. Not in front?"),
                 say('TAMSIN', 'neutral', "...A thread holds because it's twisted with others. I've had that on the SIGN."),
                 "(That night, at the guild meeting, Tamsin speaks. Her voice cracks twice. Hett stands up first: \"Then we sign it WITH you, girl, and then we tear it up together.\" The contract is renegotiated: a smaller pylon, off the grove.)"],
                [{'script': 'pf_choose(:ch2_tamsin, :expose)'},
                 say('TAMSIN', 'panic', "No— wait— not like—"),
                 "(At the guild meeting you lay the contract on the table. Uproar. The looms stop. Tamsin stands very still, then tears the contract in half herself, in front of them.)",
                 say('TAMSIN', 'sad', "I'm sorry. I'm so sorry. That's the last time I'll say it tonight.")],
                [{'script': 'pf_choose(:ch2_tamsin, :keep_secret)'},
                 say('TAMSIN', 'sad', "...Thank you. I think. I'll fix it quietly. I'll find the money somewhere."),
                 "(No meeting. Within the week, the pylon is finished.)"]]}]},
        say('TAMSIN', 'neutral', "Whatever's making the wood ring, it's in Cocoonfall Hollow, at the Glasswood's heart. I can't cross the Veil. Nobody can."),
        "\\pf[JUNO,neutral,dots]Juno: (from the stairs) ...They can.",
        "\\pf[TAMSIN,shocked,shock]Tamsin: What?",
        say('TAMSIN', 'neutral', "Then take this. It was Gran's shuttle. It's only wood. But she never dropped a thread while she held it."),
        {'if': 'GameData::Item.exists?(:MOTHERLOOMSSHUTTLE)', 'then': [{'script': 'pbReceiveItem(:MOTHERLOOMSSHUTTLE)'}],
         'else': ["\\me[Key item get]You received MOTHER LOOM'S SHUTTLE!\\nWorn smooth by fifty years of one hand."]},
        "QUEST: \"The Ringing Wood\" - Cut through the Deepwood to Cocoonfall Hollow.",
        {'tone': [0, 0, 0, 0, 20]}, {'selfswitch': ['A', True]}]
    tamsin_fight = [
        {'if': key(133, 'TRIED'), 'then': [say('TAMSIN', 'neutral', "Again? Good. I mean— sorry. I mean good.")], 'else': [
            "(Tamsin stands at the great loom at the hall's end. She has stopped fidgeting.)",
            say('TAMSIN', 'neutral', "My grandmother wove this room. Every plank, every web. She held this village together for fifty years with thread and shouting."),
            say('TAMSIN', 'sad', "I've had it since spring. I can't shout."),
            say('TAMSIN', 'angry', "But I can weave. Granny Loom wove this room. Don't you dare tear it.")]},
        {'script': key(133, 'TRIED') + ' = true'},
        {'if': 'Prismfall.gym_battle(1)', 'then': win}]
    docs.append({'id': 133, 'name': 'Loomhouse Gym - The Spindle', 'parent': 130, 'palette': 'loom', 'biome': 'canopy_gym', 'bgm': 'Gym', 'field': 'SILKWOOD',
                 'rubric': True, 'tone': [-16, -10, -20, 15], 'metadata': M, 'map': '\n'.join(SPINDLE),
                 'tiles': decorate(SPINDLE, 133, [('loom', 6, 1), ('cocoon_big', 2, 3), ('cocoon_big', 11, 3), ('web_big', 1, 6), ('web_big', 11, 6), ('shaft', 6, 5)]),
                 'events': [
                     {'type': 'exit', 'at': [8, 14], 'link': 'GYM1_SPINDLE', 'se': 'Door exit'},
                     {'type': 'event', 'name': 'Tamsin', 'at': [7, 5], 'pages': [
                         {'graphic': {'sprite': 'trainer_LASS', 'dir': 'down'}, 'commands': tamsin_fight},
                         {'cond': {'self': 'A'}, 'graphic': {'sprite': 'trainer_LASS', 'dir': 'down'}, 'commands': [
                             say('TAMSIN', 'neutral', "The Cutter in town owes me a favour. Tell him I sent you. And— thank you. Not sorry. Thank you.")]}]},
                     reveal_if(key(131, 'JUNO'), ['Juno']),
                     {'type': 'event', 'name': 'Juno', 'at': [10, 9], 'pages': [
                         {'commands': []},
                         {'cond': {'self': 'A'}, 'graphic': {'sprite': 'trainer_RIVAL2', 'dir': 'left'},
                          'commands': [say('JUNO', 'happy', "I'm being SO quiet. Look at me. Quiet.")]}]}]})
    with open(os.path.join(HERE, 'specs', '130_loomhouse_gym.yaml'), 'w') as f:
        f.write('# GENERATED by gen_gym1.py from design/GYM_PUZZLES.md + story/20_SCRIPT_CH0-2.md (Gym 1; builder 3: canopy look on tileset 40, palettes/loom.yaml). Edit the script, then run build.py.\n')
        yaml.safe_dump_all(docs, f, sort_keys=False, allow_unicode=True, width=120)
    print('wrote specs/130_loomhouse_gym.yaml')


if __name__ == '__main__':
    main()
