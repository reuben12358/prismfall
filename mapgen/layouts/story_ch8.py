#!/usr/bin/env python3
"""story_ch8: the Chapter 8 story beats on Gemini's Cindervault maps (mapgen/layouts/cindervault_town.py), from
story/29_SCRIPT_CH8.md. A STORY LAYER (storylayer.py): it upserts its events by name into the specs of

  244 Hearthguild Hall   "My Father" (CH8_STEP 4: Envoy Haskar in Brann's chair, Sigrun from the yard, the four
                         bells; the step stays 4 and Gym 7 opens), "Whose Is It" (CH8_STEP 6 with S120: the
                         :ch8_lightstone choice, -> 7) and "Chestnuts" (-> 8, Brann's slip about the Crown's stone)
  249 Slag Ward          the Five Bells evacuation while the crisis runs (CH8_STEP 5-6: families up the stairs
                         against you, the child with the Litwick jar) and the ward afterwards by V110 (vent / dampers /
                         shutdown)

and leaves the tiles, the headers and Gemini's own events alone (pages are only ADDED to three of its NPCs).

CH8_STEP agreement with 255 (layouts/cindervault.py): the Tap Chamber crisis runs at CH8_STEP >= 5 (the script's
Five Bells may already have set 6) and ends with S120 on, CH8_STEP 6 and a transfer to 244 (10,8). "Whose Is It"
needs BOTH CH8_STEP >= 6 and S120, so passing through the Hall during the crisis plays nothing.

Not here: Brann's Gym 7 (LOCKED; maps 250-253 unbuilt), the Five Bells in the square (240 unbuilt), the Ch17 Trials
quest AS_FORGE_REMEMBERS (the Trials owner's).

Run after cindervault_town.py (which rewrites both specs from scratch):
    python3 -I layouts/story_ch8.py && python3 -I build.py 244 249 --no-preview"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from story_early import P, N, S, IF, CH, MV, page, ev
import story_early as SE
import storylayer as SL

TAG = 'ch8'
STEP = 'CH8_STEP'
SE.NAMES.update({'BRANN': 'Brann', 'SIGRUN': 'Sigrun', 'LARCH': 'Larch'})
HASKAR, GUARD_M, GUARD_F = 'trainer_ASHKAAR_OFFICER', 'trainer_ASHKAAR_SOLDIER_M', 'trainer_ASHKAAR_SOLDIER_F'


def V(n, **kw): return dict({'var': [STEP, n]}, **kw)
def at(e, x, y): e['at'] = [x, y]; return e
def show(sheet, d=8): return [{'graphic': [sheet, 0, d, 0]}, {'opacity': 255}]
def bells(n, pitch=70): return S('%d.times { pbSEPlay("Anim/HealBell", 90, %d); pbWait(0.9) }' % (n, pitch))
def walk_on(name, x, y):
    """an actor with no look of its own: a scene's move route gives it one (and takes it away)"""
    return at(ev(name, page([], through=True)), x, y)
def actor(name, x, y, sheet, d, lines, cond, gone):
    return at(ev(name, page([]), page(list(lines), sheet, d, cond=cond), page([], cond=gone)), x, y)


# ============================================================================================ 244 "My Father"
MY_FATHER = [
    MV('player', ['up', 'up']),                                                   # in from the yard, up the hall
    MV('Larch', show('LARCH') + ['up', 'up', 'turn_up'], wait=False),
    MV('Brann', show('BRANN') + ['up', 'up', 'right', 'right', 'right', 'up', 'up', 'up', 'turn_left']),
    {'raw': [203, [8, 4, 3]]}, {'wait': 30}, {'raw': [203, [2, 4, 3]]}, {'wait': 20},   # the Light Stone behind its grille
    N('Envoy Haskar', "Warden. The Dominar's patience is a coal."),
    N('Envoy Haskar', "It glows a long while. It is not endless."),
    P('BRANN', 'angry', "And my answer's a hammer, Haskar. It doesn't glow at all.", '', 'Brann'),
    N('Brann', "The Light Stone is the Hearthguild's."),
    N('Brann', "It's been the Hearthguild's since before your Dominar's great-grandmother learned to ride."),
    N('Envoy Haskar', "The Stone is Reshiram's. Reshiram is Ashkaar's."),
    N('Envoy Haskar', "The Hearthguild is in Ashkaar. You see how it follows."),
    N('Brann', "The Concordance says a Warden keeps what was put in their keeping."),
    N('Brann', "Say true, Haskar."),
    N('Brann', "Was the Stone put in your keeping?"),
    {'wait': 30},
    N('Envoy Haskar', "...No."),
    P('BRANN', 'happy', "There! See! Honesty! Isn't it marvellous!", '', 'Brann'),
    # wingbeats, close, like a sail cracking; dust from the rafters
    S('pbSEPlay("Fly", 100, 70)\npfm_shake(3, 10, 12)'), {'wait': 20},
    MV('player', ['turn_down'], wait=False), MV('Larch', ['turn_down'], wait=False),
    MV('Sigrun', show('SIGRUN') + ['up', 'left', 'left', 'left', 'up', 'up', 'up', 'turn_up'], wait=False),
    {'wait': 6}, MV('Salamence', show('Followers/SALAMENCE') + ['step_anime_on', 'turn_up']),
    {'waitmove': True},
    P('SIGRUN', 'neutral', "Haskar. Get out of the Warden's chair.", '', 'Sigrun'),
    MV('Envoy Haskar', ['left', 'turn_right']),                                    # he gets out of the chair
    N('Envoy Haskar', "Wardeness. The Dominar sent me to—"),
    P('SIGRUN', 'angry', "I know what my father sent you to do.", '', 'Sigrun'),
    N('Sigrun', "I read the letter before he sealed it. Sit somewhere else."),
    S('pfm_face("Sigrun", :player)'), S('pfm_face(:player, "Sigrun")'), {'wait': 40},   # a rider sizing up a horse
    N('Sigrun', "So you're the ferry child everyone's whispering about."),
    N('Sigrun', "Hm. Smaller than I expected."),
    CH(["I've been told.", "Smaller than what?", "..."], [
        [P('SIGRUN', 'smug', "By Brann, I imagine. Loudly.", '', 'Sigrun')],
        [P('SIGRUN', 'smug', "Than the whispering.", '', 'Sigrun')],
        [P('SIGRUN', 'smug', "Good. You don't talk to fill the air. Neither do I.", '', 'Sigrun')]], cancel=3),
    P('SIGRUN', 'smug', "I'm Sigrun Ashfall. Wyrmrest. The Dragon Warden.", '', 'Sigrun'),
    N('Sigrun', "I'm here to keep two stubborn men from starting a war over a rock, which is the most Ashkaar sentence anyone will say to you this week."),
    P('BRANN', 'happy', "She's very good. She's been doing it since she was nine.", '', 'Brann'),
    N('Sigrun', "Since I was eleven. At nine I was starting them."),
    MV('Larch', ['turn_right']), S('pfm_face(:player, "Larch")'),
    P('LARCH', 'neutral', "Watch her.", '', 'Larch'),
    N('Larch', "She's the only person in this room who isn't scared of the mountain."),
    N('Larch', "That's either very brave or she knows something."),
    bells(4), {'wait': 10},                                                       # four bells
    P('BRANN', 'sad', "Four. That's four.", '', 'Brann'),
    S('pfm_face(:player, "Brann")'),
    N('Brann', "Go and get your badge while I've still got a gym that isn't on fire."),
    N('Brann', "I'll be down in the Foundry."),
    N('Brann', "Sigrun, keep him out of my chair."),
    MV('Brann', ['through_on', {'speed': 4}, 'down', 'down', 'down', 'left', 'left', 'left', 'down', 'down', 'down',
                 {'se': 'Door exit'}, {'opacity': 0}, 'through_off']),
    S('pfm_set(:gym7_open)'),                                                    # V129 stays 4: "Gym 7 opens"
    {'selfswitch': ['A', True]}]

# ============================================================================================ 244 "Whose Is It"
WHOSE = [
    S('pfm_tone(-58, -56, -30, 46, 20)'),                                          # after midnight
    {'wait': 20},
    N('Envoy Haskar', "The Warden was occupied. The city was in danger."),
    N('Envoy Haskar', "The Stone was safest with—"),
    S('pbSEPlay("Cries/SALAMENCE", 90, 60)\npfm_shake(2, 12, 8)'),                 # a Salamence's growl, very close
    MV('Sigrun', show('SIGRUN')), MV('Haskar (night)', ['turn_down']),
    P('SIGRUN', 'angry', "Say true, Haskar.", '', 'Sigrun'),
    {'wait': 20},
    N('Envoy Haskar', "...The Dominar told me to take it while everyone was looking at the mountain."),
    N('Sigrun', "Thank you. Put it down."),
    MV('Haskar (night)', ['left', 'turn_right'], wait=False), MV('Sigrun', ['up'], wait=False),
    MV('Oath-guard (night) 1', ['down', 'down', 'down', 'down', 'turn_down'], wait=False),
    MV('Oath-guard (night) 2', ['down', 'down', 'down', 'turn_down']),
    S('pbSEPlay("GUI storage put down", 90, 70)\npfm_glow(70, 76, 96, 16, 30)'),  # on the basalt, cold and white
    MV('Brann', show('BRANN') + ['up', 'up', 'right', 'right', 'up', 'up', 'turn_left']),   # in, and down on the bench
    {'wait': 24},
    P('BRANN', 'sad', "Thirty years it's been on that wall. Nobody touched it.", '', 'Brann'),
    N('Brann', "And tonight I'd have let them, if they'd asked nicely."),
    N('Brann', "I was carrying a woman's grandmother up four hundred steps."),
    N('Sigrun', "This won't stop."),
    N('Sigrun', "My father will send another envoy, and another, and one day he'll send a legion."),
    S('pfm_face("Sigrun", :player)'), S('pfm_face(:player, "Sigrun")'),
    N('Sigrun', "You've stood in three kingdoms' business this year."),
    N('Sigrun', "You might as well stand in a fourth."),
    N('Sigrun', "Say it. Who should keep it?"),
    CH(["The Hearthguild. It's Brann's to keep.", "Wyrmrest. A Warden's neutral ground.", "The Dominar. It's his people's."], [
        [S('pf_choose(:ch8_lightstone, :hearthguild)'),
         P('BRANN', 'crying', "Thank you.", '', 'Brann'),
         # he puts it back in the cradle and closes the grille himself
         MV('Brann', ['through_on', 'right', 'up', 'up', 'up', 'left', 'left', 'left', 'up', 'up', 'up', 'left', 'turn_up', 'through_off']),
         S('pbSEPlay("Door slide", 90, 60)\npfm_glow(50, 54, 70, 10, 10)'),
         P('SIGRUN', 'neutral', "Then my father's grudge gets heavier, and Brann carries it.", '', 'Sigrun'),
         N('Sigrun', "He's strong."),
         MV('Sigrun', ['turn_left']),
         N('Sigrun', "Go home and say true."),
         MV('Haskar (night)', ['through_on', 'down', 'right', 'down', {'se': 'Door exit'}, {'opacity': 0}])],
        [S('pf_choose(:ch8_lightstone, :wyrmrest)'),
         P('SIGRUN', 'shocked', "...Mine?", '', 'Sigrun'),
         MV('Brann', ['turn_down', 'wait 16', 'turn_left']),
         P('BRANN', 'neutral', "Hers. Aye. Not the Dominar's. Not mine. A Warden's, with dragons round it.", '', 'Brann'),
         N('Brann', "That's the Concordance done properly. I'm too fond of the thing to have thought of it."),
         N('Sigrun', "My father will hate it. He can't argue with it."),
         P('SIGRUN', 'smug', "You think like a rider.", '', 'Sigrun')],
        [S('pf_choose(:ch8_lightstone, :dominar)'),
         # Brann looks at the PC for a long time, then at the stone, then at his hands
         S('pfm_face("Brann", :player)'), {'wait': 50}, MV('Brann', ['turn_left']), {'wait': 40}, MV('Brann', ['turn_down']), {'wait': 40},
         P('BRANN', 'crying', "...Take it, then, Haskar.", '', 'Brann'),
         N('Brann', "Tell him the ferry child said."),
         MV('Oath-guard (night) 1', ['through_on', {'speed': 4}, 'up', 'left', 'left', 'left', 'down', 'down', 'down', 'down', 'down',
                                     'right', 'right', 'down', {'opacity': 0}], wait=False),
         MV('Haskar (night)', ['through_on', 'down', 'right', 'down', {'se': 'Door exit'}, {'opacity': 0}], wait=False),
         P('SIGRUN', 'angry', "You've just told a man who wants a war that the war's right.", '', 'Sigrun'),
         N('Sigrun', "Remember you did."),
         S('pfm_fade_out(20)'), {'wait': 16},                                    # later, on the steps
         P('LARCH', 'sad', "He'll forgive you. He forgives everybody."),
         N('Larch', "He won't forget, though. Smiths don't.")]], cancel=0),
    S('pfm_fade_out(30)'),                                                        # "Chestnuts" takes it from here, in the dark
    MV('Brann', [{'opacity': 0}], wait=False), MV('Sigrun', [{'opacity': 0}], wait=False),
    MV('Haskar (night)', [{'opacity': 0}], wait=False), MV('Oath-guard (night) 1', [{'opacity': 0}]),
    {'var': [STEP, 7]}]

# ============================================================================================ 244 "Chestnuts"
CHESTNUTS = [
    MV('player', [{'script': 'moveto(12, 5)'}, 'turn_right']),
    IF('$game_variables[@@CINDERVAULT_STATE] == 1',                              # :vent: the forge is out, a brazier
       [S('pfm_tone(-70, -66, -48, 60, 30)')], [S('pfm_tone(-30, -52, -72, 30, 30)')]),
    {'wait': 20},
    MV('Brann (chestnuts)', ['turn_left']),
    P('BRANN', 'happy', "I'll tell you a thing about chestnuts, ferry child.", '', 'Brann (chestnuts)'),
    N('Brann', "You've to cut a cross in 'em first."),
    N('Brann', "Else they go off like a Voltorb."),
    S('pbSEPlay("Anim/Explosion7", 35, 160)'),
    P('LARCH', 'deadpan', "He told me that in AF 271. And AF 280. And AF 288.", '', 'Larch (chestnuts)'),
    N('Brann', "And it's still TRUE!"),
    S('pbSEPlay("Water1", 60, 120)'), {'wait': 14},                               # he pours; three cups in
    MV('Brann (chestnuts)', ['turn_up']), {'wait': 60},                           # he looks at the forge for a while
    N('Brann', "Thirty years at this anvil. You know the best thing I ever made?"),
    N('Brann', "Not a blade. A setting."),
    N('Brann', "A little gold setting for a little white stone."),
    P('BRANN', 'sad', "I reset the Crown's stone myself, y'know. After the accident. Ten years back.", '', 'Brann (chestnuts)'),
    N('Brann', "It was smaller than it should've been."),
    # under the PC's ribs, as if flicked with a fingernail: a single note, too low to hear. Then nothing.
    S('pbSEPlay("Anim/Saint7", 50, 40)\npfm_shake(1, 20, 4)'), {'wait': 30},
    MV('Larch (chestnuts)', ['turn_right']),
    P('LARCH', 'neutral', "...", 'dots', 'Larch (chestnuts)'),
    MV('Brann (chestnuts)', ['turn_left']),
    P('BRANN', 'shocked', "Ach. Ach, I'm an old fool.", '', 'Brann (chestnuts)'),
    N('Brann', "Forget it. Cider talking. Forget it."),
    P('BRANN', 'neutral', "Have a chestnut. Cross on top.", '', 'Brann (chestnuts)'),
    MV('Brann (chestnuts)', ['turn_up']), {'wait': 50},                           # he doesn't look at either of them
    S('pfm_fade_out(20)'),                                                        # later, alone, at the door
    MV('player', [{'script': 'moveto(10, 14)'}, 'turn_right']),
    MV('Larch (chestnuts)', [{'script': 'moveto(11, 14)'}, 'turn_left']),
    IF('$game_variables[@@CINDERVAULT_STATE] == 1', [S('pfm_tone(-70, -66, -48, 60, 20)')], [S('pfm_tone(-30, -52, -72, 30, 20)')]),
    P('LARCH', 'neutral', "You flinched. Just then. When he said \"smaller\".", '', 'Larch (chestnuts)'),
    CH(["It was nothing.", "I don't know what it was.", "..."], [
        [P('LARCH', 'neutral', "It's always nothing.", '', 'Larch (chestnuts)'),
         N('Larch', "I've got a notebook full of nothings. They're starting to rhyme.")],
        [P('LARCH', 'sad', "No. Neither do I. That's the bit I don't like.", '', 'Larch (chestnuts)')],
        [P('LARCH', 'sad', "All right. Go to bed.", '', 'Larch (chestnuts)'),
         N('Larch', "I'm going to write something down and then pretend I didn't.")]], cancel=3),
    "FIELD NOTES: \"Brann reset the Crown's stone ten years ago. It was 'smaller than it should've been'. Something in me answered when he said it. I don't know what that means. I'm writing it down so I can't pretend I didn't hear it.\"",
    {'var': [STEP, 8]},
    S('pfm_fade_in(30)')]


def events_244():
    return [
        at(ev('My Father', page([]), page(MY_FATHER, cond=V(4), trigger='autorun'), page([], cond={'self': 'A'}),
              page([], cond=V(5))), 0, 0),
        actor('Envoy Haskar', 6, 10, HASKAR, 'right', [N('Envoy Haskar', "The Dominar's patience is a coal. I am merely holding it.")], V(4), V(5)),
        actor('Oath-guard 1', 5, 9, GUARD_M, 'right', [N('Oath-guard', "I'm not here. I'm the Envoy's nothing's escort.")], V(4), V(5)),
        actor('Oath-guard 2', 5, 11, GUARD_F, 'right', [N('Oath-guard', "Lying's a crime. So I'll just say nothing. Loudly.")], V(4), V(5)),
        walk_on('Brann', 11, 15), walk_on('Larch', 9, 15), walk_on('Sigrun', 10, 15), walk_on('Salamence', 11, 16),
        # "Whose Is It": after the crisis (S120) and only then; the night actors are there for it alone
        at(ev('Whose Is It', page([]), page(WHOSE, cond=V(6, switch='CH8_CALDERA_DONE'), trigger='autorun'),
              page([], cond=V(7))), 1, 0),
        actor('Haskar (night)', 10, 14, HASKAR, 'down', [], V(6, switch='CH8_CALDERA_DONE'), V(7)),
        actor('Oath-guard (night) 1', 9, 5, GUARD_M, 'up', [], V(6, switch='CH8_CALDERA_DONE'), V(7)),
        actor('Oath-guard (night) 2', 11, 6, GUARD_F, 'up', [], V(6, switch='CH8_CALDERA_DONE'), V(7)),
        # "Chestnuts": two in the morning
        at(ev('Chestnuts', page([]), page(CHESTNUTS, cond=V(7), trigger='autorun'), page([], cond=V(8))), 2, 0),
        actor('Brann (chestnuts)', 13, 5, 'BRANN', 'up', [], V(7), V(8)),
        actor('Larch (chestnuts)', 11, 5, 'LARCH', 'right', [], V(7), V(8)),
    ]


# ============================================================================================ 249 the Slag Ward
UP_AND_OUT = lambda up, left: (['through_on', {'speed': 4}] + ['up'] * up + ['left'] * left + ['up'] * 5 + [{'opacity': 0}])
FIVE_BELLS = [
    S('pfm_tone(40, -12, -40, 20, 20)'),                                           # dusk, the wrong colour
    bells(5, 60),
    MV('Hearthguild Watchman', ['turn_down']),
    N('Hearthguild Watchman', "Five. FIVE! Up the stairs! Leave the bundles if they're heavy! UP!"),
    # families coming up the stairs against you, with bundles; a child with a Litwick in a jam jar like a lantern
    MV('Evacuee 1', show('NPC 13') + UP_AND_OUT(3, 8), wait=False),
    MV('Evacuee 2', show('NPC 21') + UP_AND_OUT(2, 9), wait=False),
    MV('Evacuating Mother', UP_AND_OUT(4, 7), wait=False),
    MV('Evacuee 3', show('NPC 26') + UP_AND_OUT(4, 9), wait=False),
    MV('Child with Litwick Jar', ['wait 20'] + UP_AND_OUT(4, 10), wait=False),
    MV('Litwick jar', ['wait 20', 'through_on', {'speed': 4}, {'opacity': 255}] + ['up'] * 5 + ['left'] * 10 + ['up'] * 5 + [{'opacity': 0}], wait=False),
    {'selfswitch': ['A', True]}]

AFTER_LINES = {
    'Evacuating Mother': ["Mother: Ash on the shutters, ash in the broth. Better than the alternative.",
                          "Mother: The grates hum all night now. The Warden says it'll hold. The Warden says.",
                          "Mother: The channels have gone quiet. First quiet night in a month. I keep waking up for it."],
    'Child with Litwick Jar': ["Child: It snowed grey! My Litwick ate some. He's fine. He's a bit grey.",
                               "Child: The steps are still warm! My Litwick likes it. Mama doesn't.",
                               "Child: My Litwick's sulking. Everything's gone cold and he liked the warm steps."],
    'Hearthguild Watchman': ["Hearthguild Watchman: One bell. Then nothing, all night. Forges are cold for a season. We'll live.",
                             "Hearthguild Watchman: One bell. The tap's still drawing, mind. Meridian's got brass rings on it now.",
                             "Hearthguild Watchman: One bell. Somebody shut Tap Seven. With their hands, they say."]}


def by_state(lines):
    vent, dampers, shutdown = lines
    return [IF('$game_variables[@@CINDERVAULT_STATE] == 1', [vent],
               [IF('$game_variables[@@CINDERVAULT_STATE] == 2', [dampers], [shutdown])])]


def events_249():
    out = [at(ev('Five Bells (ward)', page([]), page(FIVE_BELLS, cond=V(5), trigger='autorun'),
                 page([], cond={'self': 'A'}), page([], cond=V(7))), 0, 0),
           walk_on('Evacuee 1', 13, 12), walk_on('Evacuee 2', 14, 11), walk_on('Evacuee 3', 14, 13),
           at(ev('Litwick jar', page([], 'Followers/LITWICK', 'up', through=True, step=True)), 15, 14)]
    out[-1]['pages'][0]['graphic']['opacity'] = 0
    return out


def pages_249(spec_events):
    """pages for Gemini's NPCs: crisis lines while the bells ring (CH8_STEP 5-6), the ward afterwards by V110"""
    g = {e['name']: e['pages'][0].get('graphic') for e in spec_events if e.get('name') in AFTER_LINES}
    crisis = {'Evacuating Mother': ["Mother: Five bells! Up, love, up! Don't look at the grates!"],
              'Child with Litwick Jar': ["Child: My Litwick's not scared. I am. A bit."],
              'Hearthguild Watchman': ["Hearthguild Watchman: Five bells! Everyone up to the terraces! You — not DOWN, up!"]}
    out = {}
    for name, lines in AFTER_LINES.items():
        gr = g.get(name) or {}
        out[name] = [dict(page(crisis[name], gr.get('sprite', ''), gr.get('dir', 'down'), cond=V(5))),
                     dict(page(by_state(lines), gr.get('sprite', ''), gr.get('dir', 'down'), cond=V(7)))]
    return out


def main():
    import yaml
    print('map 244: %d events' % SL.patch('244_hearthguild_hall.yaml', 244, events_244(), None, TAG))
    spec = next(d for d in yaml.safe_load_all(open(os.path.join(SL.HERE, 'specs', '249_slag_ward.yaml'))) if d and d.get('id') == 249)
    print('map 249: %d events' % SL.patch('249_slag_ward.yaml', 249, events_249(), pages_249(spec['events']), TAG))


if __name__ == '__main__':
    main()
