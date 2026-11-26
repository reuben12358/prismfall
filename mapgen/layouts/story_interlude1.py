#!/usr/bin/env python3
"""story_interlude1: Interlude I "Lamplight" (story/24_SCRIPT_CH5.md, "Maps 105/106 - Ferrow Lighthouse"), the end
of Act I. A STORY LAYER: it does not draw maps. It writes its events into the specs of maps other layouts own,
by name, and leaves every tile, header and foreign event as it finds them:

  952 Plate Vault        "Larch (3 a.m.)"   the whole "Already Cracking" scene, staged (CH5_STEP 11 -> 12), then bed
  182 Lumen Pokémon Center "Lamplight"      CH5_STEP 12: the swap to Kestrel, the title card, off to the lighthouse
  106 Lamp Room          the opening (the wireless), Hesper asleep, the gallery (Edda's boat), the goodbye, the
                         end of Act I (V119 0, CH5_STEP 13, STORY_ACT 2, STORY_CHAPTER 6, S162) and back to 182
  105 Lighthouse 1F      the trunk and the veil, the memory flash, the Bleed-touched Haunter, the bag

Run it after any layout that REGENERATES one of those specs from scratch (the map-craft scripts that carry
`doc['events']` over keep these events on their own):

    python3 -I layouts/story_interlude1.py        # patches the four specs in place (idempotent)
    python3 -I build.py 105 106 182 952 --no-preview

Ruby side: plugins/Prismfall Core/028_Interludes.rb (the swap), mapgen/ruby/016_Staging.rb (pfm_fade_out ...),
mapgen/ruby/017_Lamplight.rb (pfm_il1_*: the memory flash, the Haunter, Edda's boat, the lamp's sweep).
Bracketed narration in the script is stage direction: it is played (move routes, tones, SEs, the drawn scenes), and
only what a picture can't carry stays as a line of text."""
import os, sys
import yaml
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from story_early import P, N, S, IF, CH, MV, SW, page, ev
import story_early as SE

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAG = 'interlude1'                     # marks what this layer owns (events: `story:`; added pages: `story:`)
STEP, IL = 'CH5_STEP', 'INTERLUDE_ACTIVE'
ON = {'var': [IL, 1]}                  # page condition: an interlude is running (V119 >= 1)
SE.NAMES.setdefault('HESPER', 'Hesper'); SE.NAMES.setdefault('KESTREL', 'Kestrel'); SE.NAMES.setdefault('LARCH', 'Larch')
LARCH, HESPER, HAUNTER = 'trainer_PROFESSOR', 'NPC 11', 'Followers/HAUNTER'
WAKE = {'map': 182, 'x': 7, 'y': 6, 'dir': 'down'}        # "The PC wakes in the Lumen Pokémon Center." (25_SCRIPT_CH6)


def K(expr, text, emote=''): return P('KESTREL', expr, text, emote, 'PLAYER')     # the player IS Kestrel here
def own(e): e['story'] = TAG; return e
def at(e, x, y): e['at'] = [x, y]; return e
def mine(p): p['story'] = TAG; return p
def fade_steps(*vals): return [s for v in vals for s in ({'opacity': v}, 'wait 2')]


# ============================================================================================ 952 "Already Cracking"
def events_952():
    scene = [
        S('pfm_tone(-64, -56, -20, 44, 16)'),                    # 3 a.m.: the vault by one torch
        MV('player', ['left'] * 6 + ['up'] * 8),                 # in from the service door, up the catwalk to the cradle's foot
        {'anim': ['Larch (3 a.m.)', 3]}, MV('Larch (3 a.m.)', ['turn_down']),
        P('LARCH', 'neutral', "Don't tell the Director. I told her I was a cleaner. She looked at my oilskin and believed me, which hurt.", '', 'Larch (3 a.m.)'),
        MV('Larch (3 a.m.)', ['turn_right']), {'se': 'Mining ping'}, S('pfm_flash(255, 240, 190, 6, 70)'),   # the torch on the crystal
        P('LARCH', 'neutral', "Look. Here. The stress lines in the crystal. A Splitter makes a star: one point, everything running out from it. There's the star, where she clamped it.", '', 'Larch (3 a.m.)'),
        N('Larch', "But these. The long ones, the length of the cradle, under the star. They're old. Months. Years. That's not a blast. That's fatigue, the kind you get in a bridge that's carried too much for too long."),
        P('LARCH', 'sad', "That wasn't the Hollow's hammer. The Plate was already cracking. Something's been drinking from it for ten years.", '', 'Larch (3 a.m.)'),
        MV('Larch (3 a.m.)', ['turn_up', 'wait 14', 'turn_left', 'wait 14', 'turn_down', 'wait 10', 'turn_right']),   # her eyes follow the conduits in
        P('LARCH', 'sad', "Something I built.", '', 'Larch (3 a.m.)'),
        {'wait': 40},
        MV('Larch (3 a.m.)', ['turn_down']),
        N('Larch', "Twelve people, child. Twelve."),
        CH(["It wasn't your hand on the Plate.", "What do we do?", "..."], [
            [P('LARCH', 'sad', "No. It was my hand on everything else.", '', 'Larch (3 a.m.)')],
            [P('LARCH', 'neutral', "We write it down. All of it. And one day we say it out loud, somewhere nobody can switch off.", '', 'Larch (3 a.m.)')],
            [P('LARCH', 'sad', "Yes. That's about all there is to say.", '', 'Larch (3 a.m.)')]], cancel=3),
        P('LARCH', 'neutral', "Go back to bed. I'm going to sit here and look at it until it stops being true.", '', 'Larch (3 a.m.)'),
        MV('Larch (3 a.m.)', ['turn_right']),
        {'var': [STEP, 12]},
        MV('player', ['down'] * 3, wait=True),
        S('pfm_fade_out(24)'),
        {'transfer': dict(WAKE, dir='up')}]                      # 182's "Lamplight" autorun takes it from here, in the dark
    return [own(at(ev('Larch (3 a.m.)', page([]),
                      page(scene, LARCH, 'right', cond={'var': [STEP, 11]}, trigger='autorun'),
                      page([], cond={'var': [STEP, 12]})), 11, 7))]


# ============================================================================================ 182 the hand-over
def events_182():
    begin = [
        S('pfm_fade_out(0)'), {'wait': 16},
        IF('pfm_il1_start', [
            S('pfm_card(:PF_IL1_CARD, "The same night. Ferrow\'s Landing.")'),
            {'transfer': {'map': 106, 'x': 2, 'y': 5, 'dir': 'up'}}], [
            # the swap could not start (a plugin missing): close Act I anyway rather than strand the save at step 12
            S('pfm_card(:PF_ACT1_END, "END OF ACT I")'),
            {'var': [STEP, 13]}, {'var': ['STORY_ACT', 2]}, {'var': ['STORY_CHAPTER', 6]}, SW('EDDA_SMUGGLER'),
            S('pf_chapter_card(6) if defined?(pf_chapter_card)'),
            S('pfm_fade_in(30)')])]
    return [own(at(ev('Lamplight', page([]),
                      page(begin, cond={'var': [STEP, 12]}, trigger='autorun'),
                      page([], cond={'var': [STEP, 13]})), 0, 0))]


# ============================================================================================ 106 the lamp room
def events_106():
    opening = [
        S('pfm_fade_in(30)'),                                    # up out of black into the night (017's tone rule); the lamp sweeps on its own
        {'wait': 30},
        N('Wireless', '"...the Lowlight... twelve... the Mandate..."'),
        {'wait': 16}, MV('player', ['turn_up']), {'se': 'GUI storage put down'}, {'wait': 24},   # he turns the wireless off
        K('neutral', "Twelve."),
        MV('player', ['turn_right']), {'wait': 10},              # toward Gran, asleep by the lamp
        N('Kestrel', "She'd never. She'd NEVER. Not a city. Not children."),
        MV('player', ['turn_down']), {'wait': 14},
        K('sad', "...So it isn't her. Good. That's good. That's what I wanted."),
        {'selfswitch': ['A', True]}]
    finale = [
        MV('player', ['right', 'down', 'down', 'turn_down']),    # to the south gallery glass
        {'wait': 20},
        S('pfm_il1_boat'),                                       # a small boat with no lights slips under the harbour chain
        K('deadpan', "Edda. Of course it's Edda."),
        SW('EDDA_SMUGGLER'),
        MV('player', ['up', 'up', 'up', 'turn_right']),          # he stops at her chair
        {'wait': 40},
        "He tucks the blanket up round her. She doesn't wake. Or she lets him think she doesn't.",
        K('neutral', "If you're alive, I'll find you."),
        N('Kestrel', "And if you're not, I'll find whoever said you weren't."),
        MV('player', ['down', 'left', 'turn_down', {'se': 'Door exit'}] + fade_steps(170, 90, 0)),   # down the stairs
        {'wait': 44}, S('pbSEPlay("Door enter", 80, 80)'), {'wait': 50},                            # the door shuts, below
        MV('Hesper Vane', ['wait 10', 'turn_left']),             # in her chair, Hesper opens her eyes
        {'wait': 16},
        P('HESPER', 'sad', "Oh, my boy. Don't.", '', 'Hesper Vane'),
        {'wait': 30},
        S('pfm_fade_out(30)'),
        S('pfm_il1_end'),
        S('pfm_card(:PF_ACT1_END, "END OF ACT I")'),             # the act's closing beat, then the next chapter's card
        {'var': [STEP, 13]}, {'var': ['STORY_ACT', 2]}, {'var': ['STORY_CHAPTER', 6]},
        S('pf_chapter_card(6) if defined?(pf_chapter_card)'),     # Chapter 6 names ACT II (Cutscenes 020): no "II — IMPRINTS" card
        MV('player', [{'opacity': 255}]),
        {'selfswitch': ['A', False]},
        {'transfer': WAKE},
        {'heal': 0},                                             # a night's sleep at the Center
        S('pfm_fade_in(40)')]
    out = [own(at(ev('Lamplight (lamp room)', page([]),
                     page(opening, cond=ON, trigger='autorun'),
                     page([], cond=dict(ON, self='A'))), 0, 0)),
           own(at(ev('Wireless', page([]),
                     page([IF("$game_self_switches[[106, %EV[Lamplight (lamp room)]%, 'A']]",
                              ["The wireless. Off. It can stay off."],
                              [N('Wireless', '"...twelve... the Mandate..."')])], cond=ON)), 2, 4)),
           own(at(ev('Lamplight finale', page([]),
                     page(finale, cond=dict(ON, self='A'), trigger='autorun')), 1, 0))]
    # the gallery: back up the stairs with the bag packed, the first step off the landing starts the finale
    for name, (x, y), back in (('Gallery W', (3, 8), 'right'), ('Gallery E', (5, 8), 'left'), ('Gallery N', (4, 7), 'down')):
        out.append(own(at(ev(name, page([], through=True),
                             page([IF('pfm?(:il1_packed) && !pfm?(:il1_boat)', [
                                 S('pfm_set(:il1_boat)'), MV('player', [back, 'turn_down']),
                                 S('pbSetSelfSwitch(%EV[Lamplight finale]%, "A", true)')])],
                                  cond=ON, trigger='touch', through=True)), x, y)))
    return out


def pages_106():
    """pages added to events the lighthouse layout owns: {event name: [pages]}"""
    return {'Hesper Vane': [mine(page(["Gran's asleep in her chair. The blanket's slipped, and her pipe's gone out in her hand."],
                                      HESPER, 'down', cond=ON))]}


# ============================================================================================ 105 the keeper's room
def events_105():
    cold = S('pfm_tone(-96, -78, -4, 72, 30)')                   # the room goes cold
    pack = [
        # he packs: the coat off his cot, the veil; the eels and the tea from the shelf
        MV('player', ['left'] * 4 + ['up'] + ['left'] * 2 + ['up'] + ['left'] * 2 + ['turn_down']),
        {'se': 'GUI storage pick up'}, {'wait': 16},
        "A coat. The veil.",
        MV('player', ['right', 'right', 'turn_right']),
        {'se': 'GUI storage pick up'}, {'wait': 12},
        "Five smoked eels, in newspaper.",
        "And a cup of cold kelp tea he's been saving for later since spring.",
        {'wait': 70},                                            # he looks at the tea for a long time
        {'se': 'GUI storage put down'}, {'wait': 10},
        "He packs it.",
        S('pfm_set(:il1_packed)')]
    trunk = [IF('pfm?(:il1_trunk)', ["The trunk. Open, and empty of the one thing that mattered."], [
        IF('$game_player.y >= 11', [MV('player', ['right', 'up', 'turn_left'])]),     # stand at its east end
        S('pbSEPlay("Door enter", 80, 70)'), {'wait': 12},
        "It isn't locked. It hasn't been locked for years. He just never tried.",
        "Inside, folded small: a black lace veil. A Ghost Warden's veil, with Gravenmoor's ghost-lantern stitched in silver at the hem.",
        K('shocked', "...", 'shock'),
        MV('player', ['turn_down']), {'wait': 30},               # he holds it up
        "It smells of candle-smoke, and something else. Something he knew once.",
        S('pfm_il1_memory'),                                     # MEMORY: no control
        S('pfm_shake(3, 14, 8)'), MV('player', ['dir_fix_on', {'speed': 5}, 'backward', {'speed': 3}, 'dir_fix_off']),   # it stops; he's on the floor
        {'wait': 44},
        K('angry', "Not again. Not AGAIN.", 'sweat'),
        N('Kestrel', "It's a dream. It's the same stupid dream. There's no kid made of light. Kids aren't made of light."),
        S('pbSEPlay("Door enter", 90, 50)'), {'wait': 18},       # a creak on the stair
        cold,
        MV('player', ['turn_right']), {'anim': ['player', 3]},
        MV('Haunter', ['through_on', 'step_anime_on', {'graphic': [HAUNTER, 150, 8, 0]}, {'opacity': 0}, {'speed': 2},
                       {'opacity': 70}, 'up', {'opacity': 130}, 'up', {'opacity': 190}, 'left', {'opacity': 230}, 'left', 'up']),
        MV('player', ['up', 'up', 'right', 'right', 'turn_up']),
        K('neutral', "Morwen. Up."),
        {'label': 'stair'},
        IF('pfm_il1_haunter', [
            {'se': 'Anim/Ice8'}, S('pfm_flash(190, 230, 255, 10, 170)'),          # it comes apart into cold sparks
            MV('Haunter', [{'opacity': 190}, 'right', {'opacity': 130}, 'right', {'opacity': 70}, 'up', {'opacity': 0}]),   # out by the window, to the sea
            S('pfm_fade_in(40)'),
            K('sad', "Good. Good, Morwen."),
            N('Kestrel', "Gran won't say. Ysolde won't answer my letters. The Accord sent a box."),
            K('angry', "Fine. Then I'll find out myself."),
            S('pfm_set(:il1_trunk)')] + pack, [
            S('pfm_fade_out(14)'), {'wait': 12}, cold,                             # lost: back at the stair
            {'jump_label': 'stair'}])])]
    blockers = []
    for name, (x, y), route in (('Night door W', (6, 12), ['up']), ('Night door E', (8, 12), ['up']),
                                ('Night door N', (7, 11), ['backward'])):
        blockers.append(own(at(ev(name, page([], through=True),
                                  page([{'se': 'Player bump'}, MV('player', route)], cond=ON, trigger='touch', through=True)), x, y)))
    return [own(at(ev('Trunk', page(['Locked. A black lace veil is caught in the lid.']),
                      page(trunk, cond=ON)), 8, 10)),
            own(at(ev('Haunter', page([], through=True)), 13, 9))] + blockers


def pages_105():
    return {'Cracked mirror': [mine(page(["The crack runs right down the middle of his face. He doesn't look for long."], cond=ON))]}


EVENTS = {952: events_952, 182: events_182, 106: events_106, 105: events_105}
PAGES = {106: pages_106, 105: pages_105}
SPECS = {952: '952_meridian_plate_vault.yaml', 182: '182_lumen_pc_arcade.yaml',
         106: '101_ferrows_landing_interiors.yaml', 105: '101_ferrows_landing_interiors.yaml'}


def events(mid):
    """this layer's events for a map (for a layout that regenerates the spec to append)"""
    return EVENTS[mid]()


def merge(evs, mid):
    """upsert this layer's events (by name) and pages into a spec's event list, in place"""
    evs[:] = [e for e in evs if e.get('story') != TAG or e.get('name') in {n['name'] for n in EVENTS[mid]()}]
    for new in EVENTS[mid]():
        i = next((k for k, e in enumerate(evs) if e.get('name') == new['name']), None)
        if i is None: evs.append(new)
        else: evs[i] = new
    for name, pages in (PAGES[mid]() if mid in PAGES else {}).items():
        e = next((e for e in evs if e.get('name') == name), None)
        if e is None: raise SystemExit('story_interlude1: map %d has no event %r to add a page to' % (mid, name))
        if e.get('type') != 'event': raise SystemExit('story_interlude1: %r on map %d is not a paged event' % (name, mid))
        e['pages'] = [p for p in e['pages'] if p.get('story') != TAG] + pages
    return evs


def patch(mid):
    path = os.path.join(HERE, 'specs', SPECS[mid])
    chunks = open(path, encoding='utf-8').read().split('\n---\n')
    for i, chunk in enumerate(chunks):
        doc = yaml.safe_load(chunk)
        if not doc or doc.get('id') != mid: continue
        lines = chunk.split('\n')
        k = next(n for n, l in enumerate(lines) if l.startswith('events:'))
        tail = [l for l in lines[k + 1:] if l and not l.startswith((' ', '-', '#'))]
        if tail: raise SystemExit('story_interlude1: `events:` is not the last key of map %d (%s)' % (mid, tail[0]))
        evs = merge(doc.get('events') or [], mid)
        body = yaml.safe_dump({'events': evs}, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True)
        chunks[i] = '\n'.join(lines[:k]) + '\n' + body.rstrip('\n') + ('\n' if i == len(chunks) - 1 else '')
        open(path, 'w', encoding='utf-8').write('\n---\n'.join(chunks))
        return len(evs)
    raise SystemExit('story_interlude1: no map %d in %s' % (mid, path))


def main():
    for mid in (952, 182, 106, 105):
        print('map %d: %d events in %s' % (mid, patch(mid), SPECS[mid]))


if __name__ == '__main__':
    main()
