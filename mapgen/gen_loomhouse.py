#!/usr/bin/env python3
"""Writes specs/130_loomhouse_gym.yaml: the Loomhouse, Briarwick (map IDs 130-134).
SPINE Revision 14: this is GYM 2 (Tamsin Loom, Bug, Silkwood, DOUBLE battle, cap 19), the first real puzzle (3/10):
  130 Foyer        TEACH: one heddle, one pull (a plank slides into the aisle); Nell and Orla
  131 Weaving Hall TWIST: three linked heddles (each lifts two loom beds; all three once); Bram; Tamsin on the top ledge
  132 / 134        the optional Upper Lofts after her badge: spools + the brass Meridian wire, Granny's Knot
Layouts and puzzle logic come from mapgen/puzzles/loomhouse.py - the same grids the solver proves - and are painted on
tileset 54 "PF Rejuv Halls" (compose_halls.py: Rejuvenation's timber-hall tiles + Prismfall's silk props) with
layouts/hallkit.py.  Story dialogue is story/20_SCRIPT_CH0-2.md, unchanged.  Edit this script, then run build.py."""
import os, sys
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'layouts'))
FIELD_RULE = 'setBattleRule("field", :SILKWOOD)'
CLS = {'#': 'void', 'W': 'wall', '.': 'floor', 'v': 'pit', 'S': 'stair', 'o': 'floor'}
M = {'MapPosition': [0, 12, 22]}


def say(who, expr, text):
    return '\\pf[%s,%s]%s: %s' % (who.upper(), expr, who.capitalize(), text)


def key(m, k): return "$game_self_switches[[%d, 0, '%s']]" % (m, k)


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


def sign(name, at, text, tile=None):
    pg = {'commands': [text]}
    if tile: pg['graphic'] = {'tile': tile}
    return {'type': 'event', 'name': name, 'at': list(at), 'pages': [pg]}


def head(mid, name, parent, tone, extra=None):
    d = {'id': mid, 'name': name, 'parent': parent, 'biome': 'canopy_gym', 'bgm': 'Gym', 'field': 'SILKWOOD', 'tone': tone, 'metadata': M}
    d.update(extra or {})
    return d


def main():
    import hallkit as K
    from puzzles import loomhouse as g1
    CU, MI, PF = K.CU, K.MI, K.PF
    PLANK = CU('plank')
    docs = []
    # ---------------------------------------------------------------- 130 Foyer (TEACH: the first thread)
    spiral = [
        say('TAMSIN', 'panic', "Sorry — the gym's a bit tangled today — sorry —"),
        {'choices': ["It's fine.", "Stop apologizing."], 'cancel': 1, 'branches': [
            ["\\pf[TAMSIN,panic,sweat]Tamsin: Sorry for saying sorry so much. That's annoying. Sorry."],
            ["\\pf[TAMSIN,shocked,shock]Tamsin: Right! Yes! Sorr—", say('TAMSIN', 'panic', "I nearly did it again. I'm so sorry.")]]},
        say('TAMSIN', 'sad', "..."),
        say('TAMSIN', 'deadpan', "I'm going to go and stand in the web now."),
        {'move': {'who': 0, 'route': ['up', 'up', 'up', 'up', 'up']}}, {'selfswitch': ['A', True]}]
    # story/21_SCRIPT_CH3.md, Map 131 (Revision 14 lines)
    win = [
        say('TAMSIN', 'shocked', "...It held, and you still came through it."),
        say('TAMSIN', 'happy', "That's allowed. Granny said the room's meant to lose to the right person. I didn't think I'd ever meet one."),
        {'script': 'Prismfall.award_badge(pfm_gym(:LEADER_TAMSIN))'},
        "(You open the Badge Case and set the badge beside Dorian's. The first note, then a second, higher, in tune with it. The two hang in the air together.)",
        "\\pf[JUNO,shocked,shock]Juno: It's doing a CHORD.",
        say('TAMSIN', 'neutral', "I don't think they do that. ...Do they do that?"),
        say('JUNO', 'happy', "It did one note in Saltmere! Dorian asked it to do it again and it wouldn't!"),
        say('TAMSIN', 'deadpan', "It's a very sensible box."),
        {'script': 'pbReceiveItem(:TM89)'},
        say('TAMSIN', 'neutral', "That's the Accord's word that Pokémon up to level twenty-three will heed you. And the Cutter will give you Cut now. He'll say no first. Wait for the second answer."),
        say('TAMSIN', 'sad', "\\PN... could you come up to the loft? There's something I should say to someone, and you've an honest sort of silence."),
        {'tone': [-255, -255, -255, 0, 12]}, {'wait': 14}, {'tone': [-30, -20, -10, 30, 12]},
        "(The loft above the hall: a ledger open on a table, a contract with a gold sunburst seal. Tamsin won't sit.)",
        say('TAMSIN', 'sad', "That woman at the pylon. With the shears. She was right. I signed it."),
        say('TAMSIN', 'sad', "Briarwick's bankrupt. It has been for three years. Gran hid it. I found the accounts the week I buried her."),
        say('TAMSIN', 'sad', "Meridian offered four hundred thousand for \"stewardship rights\". One pylon. Free light. I signed it by myself, at night, so nobody would have to know how bad it was."),
        say('TAMSIN', 'neutral', "And it WORKS. That's the thing. The looms ran till midnight for a week. Everyone was so happy. Nobody had been happy since the funeral."),
        say('TAMSIN', 'crying', "And now the Glasswood's walking up the survey line like it was invited. Fourteen moths this week. I count them. I count them every morning."),
        say('TAMSIN', 'sad', "The man in Saltmere told everyone to ask their Warden. Nobody's asked me yet. They're all too kind. The guild meets tonight."),
        say('TAMSIN', 'sad', "Tell me what to do. Please. I've run out of thread."),
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
        "\\pf[JUNO,neutral,dots]Juno: (from the stairs, hatbox in her arms) ...They can.",
        "\\pf[TAMSIN,shocked,shock]Tamsin: What?",
        say('TAMSIN', 'neutral', "Then take this. It was Gran's shuttle. It's only wood. But she never dropped a thread while she held it."),
        {'if': 'GameData::Item.exists?(:MOTHERLOOMSSHUTTLE)', 'then': [{'script': 'pbReceiveItem(:MOTHERLOOMSSHUTTLE)'}],
         'else': ["\\me[Key item get]You received MOTHER LOOM'S SHUTTLE!\\nWorn smooth by fifty years of one hand."]},
        {'script': 'pfm_quest(:ringing_wood, "The Ringing Wood", "Get Cut from the Cutter, then cut through the Deepwood to Cocoonfall Hollow.")'},
        {'tone': [0, 0, 0, 0, 20]}, {'selfswitch': ['A', True]}]
    tamsin_fight = [
        {'if': key(131, 'TRIED'), 'then': [say('TAMSIN', 'neutral', "Again? Good. I mean— sorry. I mean good.")], 'else': [
            "(Tamsin stands at the great loom on the top ledge. She has stopped fidgeting.)",
            say('TAMSIN', 'neutral', "My grandmother wove this room. Every plank, every web. She held this village together for fifty years with thread and shouting."),
            say('TAMSIN', 'sad', "I've had it since spring. I can't shout."),
            say('TAMSIN', 'neutral', "Dorian goes first because he makes people brave. I go second because by then you think you know what a gym is."),
            say('TAMSIN', 'angry', "But I can weave. Granny Loom wove this room. Don't you dare tear it.")]},
        {'script': key(131, 'TRIED') + ' = true'},
        {'if': 'Prismfall.gym_battle(pfm_gym(:LEADER_TAMSIN), double: true)', 'then': win}]
    A = g1.GYM_AT
    h = K.Hall(g1.GYM, 'loom', CLS, seed=130)
    for x, y in g1.GYM_LOOMS: h.obj('loom', x, y)
    for y in range(4, 8):                               # the Warden's rug, and a runner all the way up the aisle
        for x in range(7, 13): h.put(MI(1049), x, y, 0)
    for y in range(10, 22):
        for x in (9, 10): h.put(MI(1049), x, y, 0)
    for x in (3, 6, 10): h.obj('laundry', x, 3)
    h.obj('web', 3, 1); h.obj('web', 14, 1); h.obj('plant', 3, 3); h.obj('plant', 16, 3)
    h.obj('vat_b', 12, 6); h.obj('vat_r', 13, 6); h.obj('vat_y', 14, 6); h.obj('silk', 16, 6); h.obj('silk1', 16, 5)
    h.obj('lantern', 3, 20); h.obj('lantern', 16, 20); h.obj('silk', 15, 20); h.obj('silk1', 3, 13); h.obj('silk1', 16, 14)
    h.obj('plant', 3, 9); h.obj('plant', 16, 9); h.obj('mat_mi', 8, 21)
    hx, hy = A['heddle']
    for x in range(7, hx): h.put(CU('thread_silk_h'), x, 9, 2)      # the silk from the heddle to the plank, across the bed
    ev = [{'type': 'exit', 'at': list(A['exit']), 'link': 'BW_GYM', 'se': 'Door exit'}]
    for k, cols in g1.GYM_PLANKS.items():
        for x in cols:
            for y in (8, 9): ev.append(K.tile_event('Plank %d,%d' % (x, y), x, y, K.exact('LOOM_FOYER', k, PLANK, 1)))
    ev += [
        {'type': 'event', 'name': 'Heddle', 'at': [hx, hy], 'pages': [{'graphic': {'tile': CU('post_silk')}, 'commands': [
            {'se': 'Door exit'}, {'script': 'pfp_cycle(%d, 2)' % g1.V_FOYER},
            {'if': 'pbGet(%d) == 1' % g1.V_FOYER, 'then': [
                'You pull the heddle. The silk thread running out over the loom bed twitches, and the plank slides along it, right into the aisle.'],
             'else': ['You pull the heddle again. The plank slides back to the left.']}]}]},
        {'type': 'npc', 'name': 'Gym guide', 'at': list(A['guide']), 'sprite': 'NPC 01', 'dir': 'right', 'commands': [
            "Gym Guide: Challenger! This is the Loomhouse. Bug-types, and the Silkwood field. Fire and Flying do well. Grass does not. "
            "I say this to everyone and half of them bring a Bulbasaur.",
            "Gym Guide: Every heddle in this house is tied by silk to what it moves, so follow the thread. Down here it's one heddle, "
            "one plank. In the Weaving Hall each heddle lifts TWO beds. Count lifts, not pulls.",
            "Gym Guide: And Tamsin fights two at a time. A thread holds because it's twisted with others. Old Mother Loom built the room "
            "to teach patience. Tamsin added the safety nets. And the apology cards."]},
        K.apprentice('Pim', 'NPC 05', A['pim'][0], A['pim'][1], 'lh_foyer', "Weaver Pim, loom-minder. Stuck at the loom bed? It happens."),
        sign('Apology card', A['card_a'], "A card pinned by the loom bed: \"If the plank is in the wrong place, I'm so sorry. The heddle by the aisle moves it. — T.L.\""),
        sign('Apology card B', A['card_b'], "A card: \"The Weaving Hall is upstairs. If you fall, the nets are soft. Sorry! — T.L.\""),
        sign('Portrait', A['portrait'], "A fierce old woman at a loom. Brass plate: \"Mother Loom, Warden AF 247–299. 'Twist it or lose it.'\""),
        {'type': 'item', 'at': list(A['item']), 'item': 'POTION'},
        trainer(A['nell'], 'BUGCATCHER', 'Nell', 2, 'right', "A thread alone is just string!", "Two of us would've had you."),
        trainer(A['orla'], 'LASS', 'Orla', 2, 'left', "Mind the loom bed. I fell in twice. The net's very comfortable.", "...I'm going back to the net."),
        {'type': 'event', 'name': 'Tamsin (foyer)', 'at': list(A['tamsin_foyer']), 'pages': [
            {'graphic': {'sprite': 'trainer_LASS', 'dir': 'down'}, 'commands': spiral},
            {'cond': {'self': 'A'}}]},
        {'type': 'event', 'name': 'First loom', 'at': list(A['first_loom']), 'pages': [{'commands': [
            {'if': 'pfm_quest?(:locked_ledger) && !pfm_has?(:LEDGERKEY)',
             'then': ['A small brass key is tied into the very first warp thread.', {'script': 'pfm_item(:LEDGERKEY, 1, "Ledger Key")'}],
             'else': ["Mother Loom's first loom. The warp stops mid-row: up, down, up, down, up - and then nothing, as if she meant "
                      "to come back to it."]}]}]},
        {'type': 'warp', 'name': 'Stairs to the Weaving Hall', 'at': list(A['stair']),
         'to': {'map': 131, 'x': g1.HALL_AT['start'][0], 'y': g1.HALL_AT['start'][1], 'dir': 'up'}}]
    d = head(130, 'Loomhouse Gym - Foyer', 120, [-10, -6, -18, 10]); d.update(h.write(130)); d['events'] = ev; docs.append(d)

    # ---------------------------------------------------------------- 131 Weaving Hall (TWIST: two threads per heddle)
    A = g1.HALL_AT
    h = K.Hall(g1.HALL, 'loom', CLS, seed=131)
    for y in (9, 14):                                   # looms shoulder to shoulder between the three walkways
        for x in (5, 7, 9, 14, 16, 18): h.obj('loom', x, y)
    for x in (2, 6, 16, 20): h.obj('laundry', x, 2)
    h.obj('web', 0, 0); h.obj('web', 22, 0); h.obj('plant', 1, 2); h.obj('plant', 23, 2)
    h.obj('vat_b', 6, 3); h.obj('vat_r', 7, 3); h.obj('vat_y', 17, 3); h.obj('silk', 19, 3 - 1); h.obj('silk1', 18, 3)
    h.obj('lantern', 4, 19); h.obj('lantern', 20, 19); h.obj('mat_mi', 11, 21)
    COL = {'Red': 'red', 'Gold': 'gold', 'Green': 'green'}
    side = {'A': ('Red', 'Green'), 'B': ('Red', 'Gold'), 'C': ('Gold', 'Green')}        # which two heddles lift each loom bed
    for g, (rows, var, cols) in g1.HALL_GAPS.items():   # a tag of each heddle's colour at both ends of the beds it lifts
        mid = list(rows)[len(rows) // 2]
        h.put(CU('thread_%s_h' % COL[side[g][0]]), 0, mid, 2); h.put(CU('thread_%s_h' % COL[side[g][1]]), 24, mid, 2)
        h.put(CU('thread_%s_h' % COL[side[g][0]]), 1, mid, 2); h.put(CU('thread_%s_h' % COL[side[g][1]]), 23, mid, 2)
    ev = []
    for g, (rows, var, cols) in g1.HALL_GAPS.items():
        name = {g1.V_A: 'LOOM_A', g1.V_B: 'LOOM_B', g1.V_C: 'LOOM_C'}[var]
        for k, x in enumerate(cols):
            if x is None: continue
            for y in rows: ev.append(K.tile_event('Plank %s %d,%d' % (g, x, y), x, y, K.exact(name, k, PLANK, 2)))
    for n, (pos, (a, b), what) in g1.HALL_HEDDLES.items():
        ev.append({'type': 'event', 'name': '%s heddle' % n, 'at': list(pos), 'pages': [{'graphic': {'tile': CU('post_' + COL[n])}, 'commands': [
            {'se': 'Door exit'}, {'script': 'pfp_cycle(%d, 3)\npfp_cycle(%d, 3)' % (a, b)},
            'The %s heddle rises. Two threads lift with it: loom beds %s shift.' % (n.lower(), what)]}]})
    ev += [
        {'type': 'warp', 'name': 'Back down to the gym', 'at': list(A['entrance']), 'to': {'map': 130, 'x': 15, 'y': 4, 'dir': 'down'}},
        {'type': 'event', 'name': 'Tamsin', 'at': list(g1.HALL_AT['tamsin']), 'pages': [
            {'graphic': {'sprite': 'trainer_LASS', 'dir': 'down'}, 'commands': tamsin_fight},
            {'cond': {'self': 'A'}, 'graphic': {'sprite': 'trainer_LASS', 'dir': 'down'}, 'commands': [
                {'if_switch': [g1.S_KNOT, True], 'then': [
                    say('TAMSIN', 'crying', "You finished Gran's row. ...She'd have shouted. Happily. Sorry — I'm crying, that's the Silkwood, it's very dusty.")]},
                say('TAMSIN', 'neutral', "The Cutter in town owes me a favour. Tell him I sent you. And— thank you. Not sorry. Thank you."),
                say('TAMSIN', 'neutral', "The stairs behind me go up to Gran's practice lofts. They're open to you now. Mind the brass wire. It isn't hers.")]}]},
        {'type': 'event', 'name': 'Upper lofts stair', 'at': list(A['stair']), 'pages': [{'trigger': 'touch', 'commands': [
            {'if': 'pfm_gym_won?(:LEADER_TAMSIN)', 'then': [{'se': 'Door exit'},
                {'transfer': {'map': 132, 'x': g1.LOFT_AT['arrive'][0], 'y': g1.LOFT_AT['arrive'][1], 'dir': 'up'}}],
             'else': ["A silk rope across the stairs, and a card: \"Upper lofts: Gran's old practice rooms. After your badge. Sorry! — T.L.\"",
                      {'move': {'who': -1, 'route': ['down']}}]}]}]},
        trainer(A['bram'], 'GENTLEMAN', 'Bram', 3, 'right', "Granny Loom taught me this hall. Tamsin taught me to say sorry when I win.",
                "I don't need to say it, then."),
        sign('Torn-net sign', A['sign'], "A card on a post: \"The left warp of the middle bed snapped. Sorry! Use the other two. — T.L.\"",
             CU('post_silk')),
        K.apprentice('Pim', 'NPC 05', A['pim'][0], A['pim'][1], 'lh_hall', "Pim again. I run between rooms. Want it put back, or a nudge?"),
        reveal_if("$game_map.events.values.count { |e| e.name[/^Trainer\\(/] && $game_self_switches[[131, e.id, 'A']] } >= 1", ['Juno']),
        {'type': 'event', 'name': 'Juno', 'at': [13, 21], 'pages': [
            {'commands': []},
            {'cond': {'self': 'A'}, 'graphic': {'sprite': 'trainer_RIVAL2', 'dir': 'up'}, 'commands': [
                {'if': key(131, 'JUNO'), 'then': [say('JUNO', 'happy', "Go on, I'll be loud. Quietly. I learned that in Saltmere.")],
                 'else': ["(Juno is at the hall's entrance, holding a hatbox with great care.)",
                          say('JUNO', 'happy', "Forty eggs! In a hatbox! Don't knock the hatbox!"),
                          say('JUNO', 'happy', "Go on, I'll be loud. Quietly. I learned that in Saltmere."), {'script': key(131, 'JUNO') + ' = true'}]}]}]}]
    d = head(131, 'Loomhouse Gym - Weaving Hall', 130, [-10, -6, -18, 10]); d.update(h.write(131)); d['events'] = ev; docs.append(d)

    # ---------------------------------------------------------------- 132 Canopy Lofts (COMBINE: spools, cords, the brass wire)
    A = g1.LOFT_AT
    h = K.Hall(g1.LOFTS, 'loom', dict(CLS, v='void'), seed=132)
    seen = set()
    STR = {'h': PF(17758), 'v': PF(17753)}
    for name, (pos, cord, on, off) in g1.SPOOLS.items():           # a silk line from every spool to both of its landings
        for dest in (on, off):
            (x0, y0), (x1, y1) = pos, g1.CENTRE[dest]
            n = max(abs(x1 - x0), abs(y1 - y0))
            for i in range(1, n):
                x, y = round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n)
                if g1.LOFTS[y][x] != '#' or (x, y) in seen: continue
                if any(g1.LOFTS[y + dy][x + dx] != '#' for dx in (-1, 0, 1) for dy in (-1, 0, 1) if 0 <= y + dy < h.H and 0 <= x + dx < h.W): continue
                seen.add((x, y)); h.put(CU('thread_silk_h') if abs(x1 - x0) > abs(y1 - y0) else CU('thread_silk_v'), x, y, 2)
    h.obj('web', 6, 1); h.obj('web', 15, 16); h.obj('web', 0, 15); h.obj('web1', 21, 9); h.obj('web1', 7, 22)
    ev = []
    sw = {'alpha': g1.S_ALPHA, 'brass': g1.S_BRASS, 'gamma': g1.S_GAMMA}
    for name, (pos, cord, on, off) in g1.SPOOLS.items():
        a, b = g1.CENTRE[on], g1.CENTRE[off]
        ev.append({'type': 'event', 'name': 'Spool ' + name, 'at': list(pos), 'pages': [{'graphic': {'tile': CU('spool')}, 'trigger': 'touch', 'commands': [
            {'se': 'Door exit'},
            {'script': '$game_switches[%d] ? pfp_ride(%d, %d) : pfp_ride(%d, %d)' % (sw[cord], a[0], a[1], b[0], b[1])}]}]})
    for name in ('alpha', 'gamma'):
        ev.append({'type': 'event', 'name': 'Cord ' + name, 'at': list(g1.CORDS[name]), 'pages': [{'graphic': {'tile': CU('post_silk')}, 'commands': [
            {'if': 'pfp_flip(%d)' % sw[name], 'then': ['You pull the %s cord taut. Somewhere a spool turns to face a new line.' % name],
             'else': ['You let the %s cord go slack. The spool swings back.' % name]}]}]})
    ev.append({'type': 'event', 'name': 'Cord brass', 'at': list(g1.CORDS['brass']), 'pages': [{'graphic': {'tile': CU('post_brass')}, 'commands': [
        {'if_self': ['A', False], 'then': [
            "This one isn't silk. It's brass wire, stamped with a little gold sunburst.", {'selfswitch': ['A', True]}]},
        {'se': 'Door exit'}, {'script': 'pfp_flip(%d)\npfp_cycle(%d, 3)' % (g1.S_BRASS, g1.V_BRIDGE)},
        {'if': 'pbGet(%d) == 0' % g1.V_BRIDGE, 'then': ['The wire hums. Far across the canopy, a plank bridge folds away.'],
         'else': ['The wire hums. Somewhere ahead, something heavy slides: a plank bridge swings out over the drop.']}]}]})
    for p, pos in g1.LADDERS.items():
        ev.append({'type': 'event', 'name': 'Rope ladder P%d' % p, 'at': list(pos), 'pages': [{'graphic': {'tile': MI(962)}, 'commands': [
            'A rope ladder. Climb down and back round to the first deck?',
            {'choices': ['Yes', 'No'], 'cancel': 2, 'branches': [[
                {'tone': [-255, -255, -255, 0, 8]}, {'wait': 8},
                {'transfer': {'map': 132, 'x': g1.CENTRE[1][0], 'y': g1.CENTRE[1][1], 'dir': 'up'}},
                {'tone': [0, 0, 0, 0, 8]}], []]}]}]})
    for k, cells in g1.BRIDGE.items():
        for x, y in cells: ev.append(K.tile_event('Bridge %d %d,%d' % (k, x, y), x, y, K.exact('LOOM_BRIDGE', k, PLANK, 2)))
    ev += [
        {'type': 'warp', 'name': 'Down to Weaving Hall', 'at': list(A['down']), 'to': {'map': 131, 'x': 12, 'y': 3, 'dir': 'down'}},
        {'type': 'warp', 'name': "Granny's door", 'at': list(A['warp']), 'to': {'map': 134, 'x': g1.KNOT_AT['start'][0], 'y': g1.KNOT_AT['start'][1], 'dir': 'up'}},
        {'type': 'item', 'at': list(A['item']), 'item': 'SILVERPOWDER'},
        K.apprentice('Mossy', 'NPC 07', A['mossy'][0], A['mossy'][1], 'lh_lofts', "Mossy. I oil the spools. If you're going round in circles, say."),
        trainer(A['hollis'], 'BUGCATCHER', 'Hollis', 2, 'left', "Ride the spools wrong and you go in circles. I've been going in circles since lunch.",
                "...Lunch was a while ago."),
        trainer(A['ash'], 'POKEMONRANGER_M', 'Ash', 2, 'left', "Rangers learn the high lines first. Let's see if you can keep your feet up here.",
                "You've got canopy legs. Tamsin'll like that.")]
    d = head(132, 'Loomhouse Upper Lofts - Canopy Lofts', 130, [-14, -8, -20, 15]); d.update(h.write(132)); d['events'] = ev; docs.append(d)

    # ---------------------------------------------------------------- 134 Granny's Knot (MASTERY, optional)
    A = g1.KNOT_AT
    h = K.Hall(g1.KNOT, 'loom', CLS, seed=134)
    h.obj('web', 3, 1); h.obj('shelf', 13, 2); h.obj('plant', 3, 3); h.obj('silk', 15, 5 - 1); h.obj('vat_y', 3, 7); h.obj('mat_mi', 8, 11)
    for x, y in g1.KNOT_THREADS: h.put(MI(1049), x, y, 0)
    ev = [{'type': 'warp', 'name': 'Back to the Lofts', 'at': list(A['exit']), 'to': {'map': 132, 'x': 21, 'y': 3, 'dir': 'down'}},
          sign('Sampler', A['sampler'], "A sampler in Mother Loom's hand, one row of five threads: UP, down, UP, down, UP. Under it: \"Twist it or lose it.\"")]
    for i, (x, y) in enumerate(g1.KNOT_THREADS):
        ev.append(K.tile_event('T%d' % (i + 1), x, y, [(None, CU('knot_down')), ({'self': 'A'}, CU('knot_up'))]))
    for i, (x, y) in enumerate(g1.KNOT_TREADLES):
        names = ' '.join('T%d' % (t + 1) for t in g1.KNOT_FLIPS[i])
        ev.append({'type': 'event', 'name': 'Treadle %d' % (i + 1), 'at': [x, y], 'pages': [{'graphic': {'tile': CU('treadle_down')}, 'commands': [
            {'se': 'Door exit'}, {'script': 'pfp_flip_self(%%w[%s])' % names},
            {'if': '!$game_switches[%d] && pfp_check(:lh_knot)[0] == :ok' % g1.S_KNOT, 'then': [
                {'switch': [g1.S_KNOT, True]}, {'se': 'Door exit'},
                "Up, down, up, down, up. The row Granny Loom never finished is finished. A knot on the chest lets go."]}]}]})
    ev += [
        {'type': 'event', 'name': "Granny's chest", 'at': list(A['chest']), 'pages': [
            {'graphic': {'sprite': 'Object ball'}, 'commands': [
                {'if_switch': [g1.S_KNOT, True], 'then': [
                    {'script': 'pfm_item(:TELLURICSEED, 2, "Telluric Seed")'}, {'script': 'pfm_item(:SILKSCARF, 1, "Silk Scarf")'},
                    "A note in Mother Loom's hand: \"Twist it or lose it.\"", {'selfswitch': ['A', True]}],
                 'else': [{'script': 'pfp_check!(:lh_knot)'}]}]},
            {'cond': {'self': 'A'}}]},
        {'type': 'event', 'name': 'Re-thread lever', 'at': list(A['lever']), 'pages': [{'graphic': {'tile': CU('post_silk')}, 'commands': [
            'The re-thread lever. Lower every thread?',
            {'choices': ['Yes', 'No'], 'cancel': 2, 'branches': [[{'script': 'pfp_reset(:lh_knot, false)'}, 'Every thread drops.'], []]},
            {'if': 'PrismfallPuzzles.room_log(:lh_knot)[:resets] >= 1', 'then': [{'script': 'pfp_hint(:lh_knot)'}]}]}]}]
    d = head(134, "Loomhouse Upper Lofts - Granny's Knot", 130, [-16, -10, -20, 15]); d.update(h.write(134)); d['events'] = ev; docs.append(d)

    with open(os.path.join(HERE, 'specs', '130_loomhouse_gym.yaml'), 'w') as f:
        f.write('# GENERATED by gen_loomhouse.py from design/GYM_PUZZLES.md + mapgen/puzzles/loomhouse.py + story/20_SCRIPT_CH0-2.md (Gym 2 since SPINE Rev 14, tileset 54). Edit the script, then run build.py.\n')
        yaml.safe_dump_all(docs, f, sort_keys=False, allow_unicode=True, width=120)
    print('wrote specs/130_loomhouse_gym.yaml')


if __name__ == '__main__':
    main()
