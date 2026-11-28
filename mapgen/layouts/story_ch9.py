#!/usr/bin/env python3
"""story_ch9: Chapter 9 "The Iron Conclave" (story/27_SCRIPT_CH9.md) on Gemini's built Ironreach maps
(layouts/ironreach_town.py 260-263, layouts/ironreach_gym.py 270-274) and the Heartgarden (layouts/verdance_wards.py
294). A STORY LAYER (storylayer.py): it upserts its events by name, adds tagged pages to a few of Gemini's events and
leaves every tile, header and other event alone.

  260 Ironreach          arrival at the cage-foot (CH9_STEP 2: the announcer, the miner); the Pit's door is shut
                         until K4 (5); the Gutter Book board and Ottoline close while CH9_STEP is 6-9
  263 The Iron Pit       "The Conclave Opens" (2 -> 3: the roll-call, eighteen Wardens, Odessa's skiff), the free-roam
                         Warden lines (3-5), "The Bracket" (Nell; Kestrel and his Scizor, -> 4), the Open (Dunmore,
                         Ysa, Gristle: Gemini's three trainers, now rounds called from Nell's crate) and K4 (-> 5, S122),
                         "The Vote" (6 -> 7: the hands, lights out, Sable on the speakers, the tag battle, the
                         rockfall, Corvin), "Mandate Jurisdiction" (9 -> 10: Rowan on the stretcher, Kestrel, Juno,
                         :ch9_rowan_words, S123, V113 1, V111 1) and "A Seat to Fill" (10 -> 11)
  270 / 274 Gym 8        Kaito's words from the script on Gemini's fight (single, Prismfall.gym_battle), the badge,
                         TM31, CH9_STEP 6; Odessa's Fly; the gym guide's lines
  261 Ironreach PC       the night bulletin and the nurse (11), then sleep: Interlude II
  294 The Heartgarden    INTERLUDE II "The Bride Tree" as Rowan (V119 2): the tree, Glasswood, the potting shed and the
                         Gale Post box, the stair; END OF ACT II, V130 12, STORY_ACT 3, STORY_CHAPTER 10, back to 261

Not built, so not here (TODO_QUOTA / REFINE_QUEUE): 660 the Ashmarch (0 -> 1, Larch's goodbye), 661, 602, 672 the
Long Drop (1 -> 2, the cage), 264 the Reliquary (7 -> 9: the Mourner, IR-1, S124, :ch9_teo_sable), 265 the Old
Aurel Shafts (Teo, Sable / GO_PULL_THE_NAIL), 275 Marrowgate (Gemini's 273 holds a Marrowgate alcove, S343).
`pfm_cutscene(:CH9_UNMASK)` belongs to 264 and is not called here.

Run after ironreach_town.py / ironreach_gym.py / verdance_wards.py (they rewrite these specs from scratch):
    python3 -I layouts/story_ch9.py && python3 -I build.py 260 261 263 270 274 294 --no-preview"""
import copy, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from story_early import P, N, S, IF, CH, MV, SW, page, ev
import story_early as SE
import storylayer as SL

TAG = 'ch9'
STEP, IL = 'CH9_STEP', 'INTERLUDE_ACTIVE'
SE.NAMES.update({'HOLLIS': 'Hollis', 'VALEN': 'Valen', 'DORIAN': 'Dorian', 'MARISOL': 'Marisol', 'ROOK': 'Rook',
                 'SAHAR': 'Sahar', 'CORVIN': 'Corvin', 'BRANN': 'Brann', 'KAITO': 'Kaito', 'ANJA': 'Anja',
                 'ODESSA': 'Odessa', 'BASTIAN': 'Bastian', 'MAGNUS': 'Magnus', 'NYX': 'Nyx', 'CELESTINE': 'Celestine',
                 'SIGRUN': 'Sigrun', 'ILSA': 'Ilsa', 'MARCHETTI': 'Marchetti', 'SABLE': 'Sable', 'MOURNER': 'The Mourner'})
DIRECTORATE, HAMMER_M, HAMMER_F = 'trainer_MERIDIAN_DIRECTORATE', 'trainer_HOLLOW_GRUNT_M', 'trainer_HOLLOW_GRUNT_F'


def V(n, **kw): return dict({'var': [STEP, n]}, **kw)
def at(e, x, y): e['at'] = [x, y]; return e
def show(sheet, d=2): return [{'graphic': [sheet, 0, d, 0]}, {'opacity': 255}]
def to(x, y, face='turn_down'): return [{'script': 'moveto(%d, %d)' % (x, y)}, face]
def B(who, expr, emote, ev_name, text):
    """the script's [bubble: WHO, expr, emote] line (Cutscenes 014, SPINE Rev 22)"""
    return '\\pfb[%s,%s,%s,%s]%s: %s' % (who, expr, emote, ev_name, SE.NAMES.get(who, who.title()), text)
def walk_on(name, x, y): return at(ev(name, page([], through=True)), x, y)
def choice_is(key, val): return 'pf_choice(:%s) == :%s' % (key, val)
def by_choice(key, table, default=None):
    """IF chain over a Core choice: table = [(value, cmds), ...]; default = cmds when none match (or unset)"""
    (v, cmds), rest = table[0], table[1:]
    if not rest: return IF(choice_is(key, v), cmds, default) if default is not None else IF(choice_is(key, v), cmds)
    return IF(choice_is(key, v), cmds, [by_choice(key, rest, default)])
def cam(d, n, speed=4):
    """scroll the camera n tiles (the event waits for it): the roll-call's sweep along the table, the galleries"""
    return S('$game_map.start_scroll(%d, %d, %d)\npbWait(0.05) while $game_map.scrolling?' % ({'down': 2, 'left': 4, 'right': 6, 'up': 8}[d], n, speed))
HOME = S('pfm_pan_home(16)')
def act(who, kind): return S('pf_act("%s", :%s) rescue nil' % (who, kind))


def actor(name, x, y, sprite, d, spans, move='fixed'):
    """one cast member on 263: spans = [(CH9_STEP from, cmds | None), ...] in rising order; None = not there.
    The event stands at its free-roam spot; scenes move it to its seat (moveto) and back."""
    pages = [page([], through=True)]
    for n, cmds in spans:
        pages.append(page([], cond=V(n), through=True) if cmds is None else page(cmds, sprite, d, cond=V(n), move=move))
    return at(ev(name, *pages), x, y)


# ============================================================================================ 260 Ironreach
ARRIVAL = [   # CH9_STEP 2 (story/27 "Map 260 - Ironreach: arrival", autorun at the cage-foot)
    S('pfm_fade_out(0)'),
    MV('player', to(20, 7, 'turn_down')),
    S('pbSEPlay("Elevator end", 90, 80)\npfm_shake(3, 14, 10)'), {'wait': 16},       # the cage stops with a bang
    S('pbSEPlay("Door slide", 80, 60)'),                                               # the gate opens onto noise
    S('pbSEPlay("Crowd cheer", 70, 90)'),
    S('pfm_fade_in(24)'),
    {'wait': 20},
    MV('Pit Announcer', ['turn_up']), {'anim': ['Pit Announcer', 3]},
    N('Pit Announcer', "AND HERE COMES A NEW ARRIVAL OFF THE LONG DROP, FOLKS. FIFTEEN, MAYBE SIXTEEN. GOOD SHOES."),
    N('Pit Announcer', "IT'S... THE NULL KID! THE NULL KID IS IN IRONREACH!"),
    S('pfm_face(:player, "Pit Announcer")'), {'wait': 20},                              # you look at him
    N('Pit Announcer', "AND THE NULL KID IS... LOOKING AT ME, FOLKS."),
    {'wait': 16},
    N('Pit Announcer', "THE NULL KID HAS A VERY STRAIGHT FACE."),
    MV('Old Miner', ['turn_up']),
    N('Miner', "He does that. He narrates. He's done it for thirty years."),
    N('Miner', "He narrated my wedding. He narrated my divorce. It was the same speech."),
    MV('Old Miner', ['turn_right']),
    {'selfswitch': ['A', True]}]

# the Pit's door (21, 35) is reached only from (21, 36): shut until K4 (CH9_STEP 5), "Kaito sits at a table" up in the Pit
BACK = MV('player', ['dir_fix_on', 'backward', 'dir_fix_off'])
PIT_DOOR = [S('pbSEPlay("Door slide", 70, 50)'), BACK,
            "A chalk note on the Pit's iron door: GONE TO THE CONCLAVE. OPEN AFTER THE OPEN. — K."]


def events_260():
    return [at(ev('Ironreach Arrival', page([]), page(ARRIVAL, cond=V(2), trigger='autorun'),
                  page([], cond={'self': 'A'}), page([], cond=V(3))), 0, 0),
            at(ev('Pit door (shut)', page(PIT_DOOR, trigger='touch', through=True),
                  page([], cond=V(5), through=True)), 21, 36)]


def pages_260(spec_events):
    """the Gutter Book's board and Ottoline close while CH9_STEP is 6-9 (story/27: nothing sends the player away
    between the gym and the vote), then open again with Gemini's own pages"""
    g = {e['name']: e for e in spec_events}
    closed = {'Gutter Book Chalk Board': ["The Gutter Book's board has been wiped clean. Chalked across it, big: SHUT FOR THE VOTE."],
              'Six-Fingers Ottoline': [N('Six-Fingers Ottoline', "Board's shut, love. Nobody takes a chalk job with the whole Conclave voting over their heads.")]}
    out = {}
    for name, cmds in closed.items():
        p0 = g[name]['pages'][0]
        gr = p0.get('graphic') or {}
        out[name] = [page(cmds, gr.get('sprite', ''), gr.get('dir', 'down'), cond=V(6)),
                     dict({k: v for k, v in copy.deepcopy(p0).items() if k != 'story'}, cond=V(10))]
    return out


# ============================================================================================ 263 the cast
# seats (the roll-call and the vote) and free-roam spots (3-5); story/27 places each one
SEATS = {'Hollis': (19, 5), 'Valen': (20, 5),
         'Dorian': (10, 6), 'Tamsin': (11, 6), 'Marisol': (12, 6), 'Rook': (13, 6), 'Sahar': (14, 6),
         'Corvin': (16, 6), 'Brann': (17, 6), 'Kaito': (18, 6),
         'Rowan': (22, 6), 'Anja': (23, 6), 'Odessa': (24, 6), 'Bastian': (26, 6), 'Magnus': (27, 6),
         'Celestine': (28, 6), 'Sigrun': (29, 6), 'Ilsa': (30, 6)}
ROAM = {'Rowan': (17, 10), 'Corvin': (24, 7), 'Dorian': (9, 6), 'Marisol': (28, 28), 'Anja': (21, 2),
        'Celestine': (28, 10), 'Bastian': (4, 13), 'Magnus': (27, 7), 'Sigrun': (8, 7), 'Rook': (5, 27),
        'Sahar': (31, 6), 'Odessa': (18, 5), 'Kaito': (14, 28)}
SHEET = {n: n.upper() for n in SEATS}


def seat_all(names=None, face='turn_down'):
    return [MV(n, to(*SEATS[n], face=face), wait=False) for n in (names or SEATS)] + [{'waitmove': True}]


def unseat_all():
    return [MV(n, to(*ROAM[n]), wait=False) for n in ROAM] + [{'waitmove': True}]


# ---------------------------------------------------------------------------------- "The Conclave Opens" (2 -> 3)
def tamsin_line():
    return by_choice('ch2_tamsin', [
        ('help_confess', [P('TAMSIN', 'panic', "Present! Sorry. I renegotiated a contract last spring and I've been apologising to paper ever since.", '', 'Tamsin')]),
        ('keep_secret', [P('TAMSIN', 'sad', "...Present.", '', 'Tamsin'),
                         MV('Tamsin', ['turn_down', 'wait 40'])])],          # she doesn't look up from her hands
        [P('TAMSIN', 'neutral', "Present. Sorry. Present. ...Briarwick's books are open, if the Conclave wants to read them. Everyone else has.", '', 'Tamsin')])


def brann_line():
    return by_choice('ch8_caldera', [
        ('vent', [P('BRANN', 'sad', "HERE. With cold forges, a grumble, and a great deal of respect for the person who made them cold.", '', 'Brann')]),
        ('dampers', [P('BRANN', 'happy', "HERE! Forges lit, all of them. Ask me how. Ask the challenger how.", '', 'Brann')])],
        [P('BRANN', 'happy', "HERE. The tap's shut and the Dominar's still talking about who shut it. Look at the bench, Ambrose.", '', 'Brann'),
         S('pfm_face("Brann", :player)')])


ROLLCALL = [
    S('pfm_fade_out(0)'),
    MV('player', to(20, 11, 'turn_up')),                                         # the challengers' bench, at the floor's edge
    MV('Kestrel (bench)', show('KESTREL', 8) + to(24, 11, 'turn_up')),
    MV('Odessa', [{'opacity': 0}, {'script': 'moveto(24, 2)'}]),                 # not yet: she comes down a rope
    MV('Ysolde', ['turn_left']),
    *seat_all([n for n in SEATS if n != 'Odessa']),
    cam('up', 3, 6),
    S('pfm_fade_in(30)'),
    S('pbSEPlay("Crowd cheer", 60, 70)'), {'wait': 30},                          # tier on tier of galleries, all full
    P('HOLLIS', 'smug', "Chancellor Ambrose Hollis, for the Accord.", '', 'Hollis'),
    N('Hollis', "The Conclave of AF 300 is in session."),
    N('Hollis', "The first held in Nadir in a hundred and four years."),
    N('Hollis', "I'm told the acoustics are extraordinary."),
    N('Hollis', "I'm told a great many things down here. Most of them through a trumpet."),
    N('Pit Announcer', "AND THE CHANCELLOR IS MAKING A JOKE, FOLKS."),
    {'wait': 20},
    P('HOLLIS', 'deadpan', "...The roll of the Wardens.", '', 'Hollis'),
    cam('left', 5, 4),                                                           # along the table, west
    N('Hollis', "Saltmere."),
    P('DORIAN', 'happy', "Present, darling, and lit from the left, if anybody's asking.", '', 'Dorian'),
    N('Dorian', "Nobody ever asks."),
    N('Hollis', "Briarwick."),
    tamsin_line(),
    N('Hollis', "Ebbmouth."),
    P('MARISOL', 'neutral', "Present. For the Guild.", '', 'Marisol'),
    N('Marisol', "The Guild votes no on anything with \"Mandate\" in it, and you can write that down before you ask."),
    N('Hollis', "Lumen."),
    MV('Rook', ['turn_left', 'wait 8', 'turn_down']),                            # no drone; a plain hooded jacket
    P('ROOK', 'sad', "Here. Chat's off. Don't ask.", '', 'Rook'),
    N('Hollis', "Duneholt."),
    P('SAHAR', 'neutral', "Present, with a cough, and a well that's dropped four rungs since spring.", '', 'Sahar'),
    N('Sahar', "I'd like that in the minutes. Spell it with an H."),
    N('Hollis', "Mirefen."),
    P('CORVIN', 'deadpan', "Present. I've brought my apprentice's best friend as my plus-one, since my apprentice can't be trusted with stairs.", '', 'Corvin'),
    S('pfm_face("Corvin", :player)'), {'wait': 10}, MV('Corvin', ['turn_down']),
    N('Hollis', "Cindervault."),
    brann_line(),
    N('Hollis', "Ironreach."),
    P('KAITO', 'neutral', "Here.", '', 'Kaito'),
    {'wait': 30}, MV('Hollis', ['turn_left', 'wait 30', 'turn_down']),          # Hollis waits for more. There isn't any.
    cam('right', 10, 4),                                                         # and east
    N('Hollis', "Verdance."),
    MV('Rowan', ['turn_right', 'wait 6', 'turn_down']),                          # soil under his nails; a white bandage on the right hand
    P('ROWAN', 'happy', "Present. Forgive the hand. Kettle.", '', 'Rowan'),
    N('Hollis', "Rimeholt."),
    P('ANJA', 'deadpan', "Here. It's forty degrees and there's a ceiling.", '', 'Anja'),
    N('Anja', "Southerners call this a city."),
    N('Hollis', "Skyreach."),
    # a propeller, very close; a courier skiff over the rim; a woman slides down the rope onto the table
    S('pbSEPlay("Anim/Wind1", 90, 60)\npfm_shadow_pass(40, 60)'),
    S('pbSEPlay("Fly", 80, 70)\npfm_shake(2, 12, 8)'),
    MV('Odessa', [{'opacity': 255}, 'through_on', {'speed': 5}, 'down', 'down', 'down', 'down', 'through_off', 'turn_down']),
    P('ODESSA', 'happy', "Present! Courier's privilege.", '', 'Odessa'),
    N('Odessa', "The cage queue was forty minutes. I'm not queueing for a vote."),
    N('Hollis', "Lucent."),
    {'wait': 20}, act('Ilsa', 'nod'), {'wait': 30},                              # earmuffs on; she lifts one hand and doesn't speak
    N('Hollis', "The Provost is present. Cragholm."),
    act('Bastian', 'hop'),
    P('BASTIAN', 'happy', "Eh?", '', 'Bastian'),
    N('Hollis', "Cragholm, Warden Ore."),
    N('Bastian', "No, I've had my supper, son. Thank you."),
    N('Hollis', "Gravenmoor."),
    act('Ysolde', 'hop'), {'wait': 10},                                          # in the lowest gallery a veiled woman stands up
    "...Present.",
    {'wait': 16}, S('pfm_face("Ysolde", "Kestrel (bench)")'), {'wait': 40},     # looking at the bench. Past you.
    N('Hollis', "Cogsworth."),
    P('MAGNUS', 'neutral', "Present. Strade.", '', 'Magnus'),
    N('Magnus', "I have the Mandate's technical annex in front of me, Chancellor, and I've corrected the arithmetic on page nine."),
    N('Hollis', "Underveil."),
    MV('Nyx', ['turn_left', 'wait 6', 'turn_down']),
    P('NYX', 'smug', "Oh, I'm not on the table, darling. I'm in the gallery.", '', 'Nyx'),
    N('Nyx', "Underveil isn't seated. It just attends."),
    N('Hollis', "Gloaming."),
    P('CELESTINE', 'happy', "Present. I'm always present. That's rather the problem with me.", '', 'Celestine'),
    N('Hollis', "Wyrmrest."),
    MV('Sigrun', ['turn_up', 'wait 20', 'turn_down']),                           # a look up at the observers' gallery
    P('SIGRUN', 'neutral', "Here. And my father's envoy is in the gallery, so if the Conclave hears shouting from up there, it isn't me.", '', 'Sigrun'),
    cam('left', 5, 4),
    N('Hollis', "Eighteen Wardens present."),
    N('Hollis', "Sixteen at the table, which is a quorum, and two who prefer the galleries, which is a tradition."),
    MV('Valen', ['down', 'turn_down']),                                          # he stands; at the far end Ilsa gets up
    MV('Ilsa', ['turn_right', 'right', 'turn_down'], wait=False),
    P('VALEN', 'neutral', "Thank you, Chancellor.", '', 'Valen'),
    N('Valen', "We are here for one question."),
    N('Valen', "The Mandate was granted in Lumen, in a night, for Lumen."),
    N('Valen', "The Directorate asks for it everywhere, for as long as it takes."),
    N('Valen', "We'll hear it, and argue it, and vote on it when the Fist Plate is brought up for the oath."),
    N('Valen', "In the meantime, I'm told the Ironreach Open is the best thing in Nadir."),
    N('Valen', "Go and watch it. That's not a suggestion from the Accord. It's one from a man who used to fight in it."),
    {'var': [STEP, 3]},
    S('pbSEPlay("Crowd cheer", 60, 100)'),
    S('pfm_fade_out(24)'),                                                       # the Wardens leave the table
    MV('Valen', ['up', 'turn_down']), MV('Ilsa', to(*SEATS['Ilsa'])),
    MV('Kestrel (bench)', [{'opacity': 0}]), MV('Ysolde', [{'opacity': 0}]),
    *unseat_all(),
    HOME,
    S('pfm_fade_in(24)')]

# ---------------------------------------------------------------------------------- free roam (3-5)
JUNO_ROWAN = [
    IF("pfm?(:ch9_juno_rowan)", [
        P('ROWAN', 'happy', "Somebody down here should be here for a game.", '', 'Rowan')], [
        # Juno has her arms round the Grass Warden's middle and hasn't let go
        by_choice('ch7_ledger', [
            ('name_him', [P('JUNO', 'neutral', "Hello.", '', 'Juno (with Rowan)'),
                          MV('Juno (with Rowan)', ['turn_left', 'wait 30']),        # at his bandaged hand, not at you
                          P('ROWAN', 'neutral', "Juno says you've been to Mirefen.", '', 'Rowan'),
                          N('Rowan', "She says you were very honest with her there. She didn't say about what.")]),
            ('ask_corvin', [P('JUNO', 'happy', "\\PN! He's here!", '', 'Juno (with Rowan)'),
                            N('Juno', "Uncle Rowan, this is the one I write about!"),
                            MV('Corvin', ['turn_left']), {'wait': 24}, S('pfm_face(:player, "Corvin")'), {'wait': 10},
                            MV('Corvin', ['turn_up']), {'wait': 16}, S('pfm_face(:player, "Juno (with Rowan)")')])],
            [P('JUNO', 'happy', "\\PN! Look who's here!", 'exclaim', 'Juno (with Rowan)'),
             N('Juno', "He came all this way and he didn't even write first!"),
             MV('Juno (with Rowan)', ['turn_left']),                              # holding his bandaged hand up, very gently
             N('Juno', "The kettle. The famous kettle."),
             N('Juno', "You've had forty years of kettles."),
             P('ROWAN', 'happy', "Forty years and one bad morning. Leave it be, love.", '', 'Rowan')]),
        P('ROWAN', 'happy', "You've grown. Juno's letters are half seeds and half you, did you know?", '', 'Rowan'),
        N('Rowan', "I've been reading about your Pokémon for a season."),
        N('Rowan', "I feel I could pick them out of a crowd."),
        N('Rowan', "You held that Phantump at the station. It's grown too. It still won't go near anyone else."),
        N('Rowan', "You're here for the Open. Good. Somebody down here should be here for a game."),
        MV('Rowan', ['turn_right', 'wait 20']),                                     # his left hand tucks a blossom back into her wreath
        "On the third finger of his left hand there's a pale band of skin where a ring was.",
        MV('Juno (with Rowan)', ['turn_left']),
        P('JUNO', 'happy', "Where's your ring?", '', 'Juno (with Rowan)'),
        N('Rowan', "Being sized."),
        MV('Rowan', ['turn_down']), MV('Juno (with Rowan)', ['turn_down']),
        S('pfm_set(:ch9_juno_rowan)')])]

ROAM_LINES = {
    'Corvin': [P('CORVIN', 'neutral', "I'm a doctor.", '', 'Corvin'),
               N('Corvin', "I have one professional observation to make about the Grass Warden's hand, and I'm not making it."),
               N('Corvin', "Juno's been brilliant all week. She restarted my stills twice. Let her have tonight.")],
    'Dorian': [P('DORIAN', 'happy', "Act Two, scene the last: the Wardens descend into the underworld.", '', 'Dorian'),
               N('Dorian', "Oh, don't look at me like that."),
               N('Dorian', "Somebody has to say these things out loud, or they just happen."),
               IF(choice_is('ch5_lowlight_testimony', 'mourner'),
                  [P('DORIAN', 'neutral', "I had your telegram's reply by heart before I sent it. The pageant version. Well. It sells.", '', 'Dorian')])],
    'Marisol': [IF(choice_is('ch4_teo', 'report'),
                   [P('MARISOL', 'angry', "Kid. You told a Meridian guard my brother's name with me standing there. I'm not going to hit you, because Kaito's watching. Keep walking.", '', 'Marisol')],
                   [P('MARISOL', 'neutral', "Teo's not here, before you ask. I don't know where he is. That's the truth, and I hate it. Last letter said \"somewhere useful\".", '', 'Marisol'),
                    N('Marisol', "Useful. He's nineteen. Nobody's useful at nineteen. You're just loud.")])],
    'Celestine': [P('CELESTINE', 'happy', "We've met. You didn't know it yet.", '', 'Celestine'),
                  CH(["At Briarwick? The old woman at the shrine?", "I don't think so."], [
                      [P('CELESTINE', 'smug', "I can't lie, so I'll only say:", '', 'Celestine'),
                       N('Celestine', "she was very old, and she was very fond of you.")],
                      [P('CELESTINE', 'smug', "That's the nicest thing about you. You'll find out anyway.", '', 'Celestine')]], cancel=2)],
    'Bastian': [MV('Bastian', ['turn_down', 'wait 10']),                                # one eye open
                P('BASTIAN', 'happy', "Hollis can't hear me if I can't hear him.", '', 'Bastian'),
                N('Bastian', "It's an old Cragholm law. I made it up."),
                MV('Bastian', ['turn_left'])],
    'Magnus': [P('MAGNUS', 'neutral', "A null reading.", '', 'Magnus'),
               N('Magnus', "I've built machines that would give a great deal to be wrong in that particular way."),
               N('Magnus', "...Good luck in the Open.")],
    'Sigrun': [S('pfm_face("Sigrun", :player)'),
               P('SIGRUN', 'neutral', "You again. Still small. Still standing in the middle of everything.", '', 'Sigrun'),
               N('Sigrun', "Stop it. You'll get trampled."),
               MV('Sigrun', ['turn_up'])],
    'Rook': [P('ROOK', 'sad', "I go down to the Lowlight every night.", '', 'Rook'),
             N('Rook', "Then I came here and I thought, it'll be different underground."),
             N('Rook', "It isn't. Everyone's still made of glass if you look long enough.")],
    'Sahar': [IF(choice_is('ch6_drillsite', 'sanctuary'),
                 [P('SAHAR', 'neutral', "The child you made me shout for has started digging. Holes, mostly. He says he's looking for the red giant. I've told him to stop when it answers.", '', 'Sahar')],
                 [P('SAHAR', 'neutral', "They'll vote the Mandate everywhere tonight. I'll vote no. The sand will vote with me. The sand always loses votes and always wins arguments.", '', 'Sahar')])],
    'Odessa': [P('ODESSA', 'smug', "I carry everybody's post, including the Directorate's, and I read none of it, and I can tell you exactly what's in all of it. Ask me after the vote.", '', 'Odessa')],
    'Ilsa': [act('Ilsa', 'shudder'),                                                      # she flinches before you're close
             MV('Ilsa', ['turn_right', 'through_on', 'right', 'through_off', 'turn_left']),  # three seats down; there aren't any
             P('ILSA', 'deadpan', "...Not you. Them. All of them. Excuse me.", '', 'Ilsa')],
    'Nyx': [MV('Nyx', ['turn_left', 'wait 6', 'turn_down']),                             # she waves you over
            P('NYX', 'smug', "There it is. The child everyone's whispering about.", '', 'Nyx'),
            N('Nyx', "Sit. I've bought you a drink."),
            S('pbSEPlay("GUI storage put down", 70, 110)'),
            "It's a glass of milk.",
            N('Nyx', "I'm told you're fifteen. I'm told everything about you, sweetheart."),
            N('Nyx', "It's very dull for me. Drink up.")],
}

ENVOYS = [   # 14_WAR_AND_BLESSING's Ch9 insert: the Elector's Lease; later the papers and both seals are gone
    IF("pfm?(:ch9_lease)", [
        "Both papers are gone. Both envoys' seals are missing from their sashes. The man in silk has left."], [
        N('Envoy of the Dominar', "Our fire warms our enemies' beds, Warden. Every ember in Rimeholt's towers was dug out of the Cinderhorn."),
        P('ANJA', 'angry', "Then send me a bill, and I'll send you a bill for every child who'd have died this winter without it, and we'll see whose is longer.", '', 'Anja'),
        N('Envoy of the Dominar', "You'll get a bill. It won't be written in ink."),
        act('Anja', 'hop'), act('Envoy of the Dominar', 'hop'),                           # both on their feet; the man in silk stays seated
        {'wait': 20},
        P('VALEN', 'neutral', "Warden Sorrel. Envoy. Sit down.", '', 'Valen'),
        {'wait': 20},
        MV('Envoy of Ossaria', ['turn_left', 'wait 12', 'turn_right', 'wait 12', 'turn_down']),   # a paper to each
        S('pbSEPlay("GUI storage put down", 60, 120)'),
        N('Envoy of Ossaria', "For your masters, with the Prince-Elector's compliments."),
        N('Envoy of Ossaria', "A small matter of land. Sand, really. Nobody's using it."),
        S('pfm_set(:ch9_lease)'),
        S('pfm_fade_out(12)'), MV('Envoy of Ossaria', [{'opacity': 0}]), {'selfswitch': ['A', True]}, S('pfm_fade_in(12)')])]

VOSS = [P('VOSS', 'happy', "Our ferry passenger.", '', 'Voss'),
        N('Voss', "I keep finding you in the middle of history. It's becoming a habit, for both of us."),
        N('Voss', "Zenith sits as an observer. Meridian, as a petitioner. I'm both, which means I don't get a vote and I get to watch everyone else's faces while they cast theirs. It's the best seat in the house."),
        P('VOSS', 'neutral', "Seven notes now, isn't it? In the case.", '', 'Voss'),
        N('Voss', "It must be quite a chord."),
        P('CALLA', 'neutral', "Sir, the Chancellor.", '', 'Calla'),
        N('Voss', "Of course. Excuse me. Enjoy the Open.")]

# ---------------------------------------------------------------------------------- "The Bracket" (3) and Kestrel (-> 4)
BRACKET = [
    S('pfm_fade_out(10)'),
    MV('player', to(17, 28, 'turn_left')),
    MV('Kaito', to(14, 28, 'turn_right')),
    MV('Kestrel (bracket)', show('KESTREL', 4) + to(22, 28, 'turn_left')),         # the far end of the bench
    S('pfm_fade_in(10)'),
    N('Nell', "I'm Nell. I do the board. I've done it since I was six."),
    N('Nell', "I've got the neatest S in Ironreach and I'll fight anyone who says I haven't."),
    P('KAITO', 'neutral', "Names for the bracket.", '', 'Kaito'),
    MV('Juno (bracket)', show('JUNO', 8) + to(20, 31, 'turn_up') +
       ['through_on', {'speed': 5}, 'up', 'up', 'left', 'left', 'turn_up', 'through_off']),   # at a run, wreath askew
    P('JUNO', 'happy', "Team Compost!", 'exclaim', 'Juno (bracket)'),
    act('Kestrel (bracket)', 'hop'),                                                  # he stands up very fast
    P('KESTREL', 'angry', "We are NOT— it's a singles bracket!", '', 'Kestrel (bracket)'),
    N('Kaito', "Team Compost. Two entrants."),
    P('KESTREL', 'panic', "Don't write that down. Why are you writing that down.", '', 'Kestrel (bracket)'),
    P('KAITO', 'deadpan', "A fist is a promise. So is a form.", '', 'Kaito'),
    MV('Nell the Chalk-Girl', ['turn_up']), S('pbSEPlay("Mining pick", 60, 130)'), {'wait': 10},
    S('pbSEPlay("Mining pick", 60, 120)'), {'wait': 16},                              # her neatest hand
    "KESTREL VANE (TEAM COMPOST)",
    MV('Nell the Chalk-Girl', ['turn_right']),
    B('KESTREL', 'crying', 'sweat', 'Kestrel (bracket)', "My mother was a Warden."),
    N('Nell', "Is that with one L or two?"),
    S('pfm_face("Juno (bracket)", :player)'),
    N('Juno', "I'm not entering. I'm the team."),
    N('Juno', "Every team needs someone who isn't in it to shout."),
    MV('Kestrel (bracket)', ['through_on', 'up', 'up', {'opacity': 0}], wait=False),  # off to the Pit's wall
    MV('Juno (bracket)', ['through_on', 'right', 'right', 'down', 'down', {'opacity': 0}]),
    S('pbSetSelfSwitch(%EV[Kestrel]%, "A", true)'),
    S('pfm_set(:ch9_bracket)')]

KESTREL_TALK = [
    P('KESTREL', 'neutral', "Don't. Whatever you're going to say about the board.", '', 'Kestrel'),
    N('Kestrel', "I'm not here for a title."),
    N('Kestrel', "Word in every inn from Mirefen to here: the Mourner's going to hit the Conclave."),
    N('Kestrel', "Every Warden in one hole. He'd never get a better shot."),
    N('Kestrel', "So I'm here. Closest seat in the house."),
    by_choice('ch6_kestrel_rumor', [
        ('encourage', [P('KESTREL', 'happy', "You said go. So I went. All the way down.", '', 'Kestrel')]),
        ('warn', [P('KESTREL', 'angry', "And before you say it might not be her: I know. I KNOW. I'm still going to be standing there when the mask comes off.", '', 'Kestrel')]),
        ('silent', [P('KESTREL', 'deadpan', "You're doing the silence. Gran does the silence. I can hear it from here.", '', 'Kestrel')])]),
    MV('Scizor', show('Followers/SCIZOR', 4) + ['turn_left']),                        # red and polished, one pincer chipped
    S('pbSEPlay("Cries/SCIZOR", 70, 100)'),
    P('KESTREL', 'deadpan', "Won him off a pit-boss in the undercard on Tuesday.", '', 'Kestrel'),
    N('Kestrel', "He was a Scyther with a cracked blade. Pit-boss said he was finished."),
    N('Kestrel', "He wasn't. See you in the final. Don't make me wait."),
    {'var': [STEP, 4]}]

# ---------------------------------------------------------------------------------- the Open and K4 (4 -> 5)
FIGHTERS = {1: ('Pit Brawler Dunmore', (14, 23), 'right', 'trainer_BLACKBELT',
                [N('Pit Brawler Dunmore', "We're both wearing shorts. That's psychological.")],
                [N('Pit Announcer', "AND THE NULL KID TAKES ROUND ONE, FOLKS. DUNMORE WILL BE LOOKING FOR A SHIRT.")],
                "...I'm going to need a shirt."),
            2: ('Crush Kin Ysa', (26, 23), 'left', 'trainer_CRUSHGIRL',
                [N('Crush Kin Ysa', "Gran's watching. If I lose, I've got to do the washing for a month.")], [],
                "GRAN. I did my BEST. ...She's saying \"the washing\". I can't hear her but I know."),
            3: ('Old Gristle', (20, 15), 'down', 'trainer_BLACKBELT',
                [N('Old Gristle', "I fought Valen Corrigan in this Pit when he was nineteen."),
                 N('Old Gristle', "He was a good boy. He cried when he won. Don't you cry.")],
                [S('pbSEPlay("Crowd cheer", 80, 70)'), {'wait': 10},                    # the crowd, all round the Pit, starting low
                 N('The crowd', "NULL. KID. NULL. KID."), S('pbSEPlay("Crowd cheer", 100, 90)')],
                "You didn't cry. That's worse. Go on. The boy in the coat's waiting, and he's been staring at you for three rounds.")}
NELL_HEAL = [S('pbSEPlay("Anim/HealBell", 85, 100)\n$player.heal_party'),
             N('Nell', "Here, take a breather by my chalk crate — every Ironreach Open entrant gets patched up between bouts!")]


def open_round(n):
    name, home, d, _, intro, after, _ = FIGHTERS[n]
    return IF('!pfm?(:ch9_open%d)' % n, [
        S('pfm_fade_out(10)'),
        MV('player', to(18, 19, 'turn_right')), MV(name, to(22, 19, 'turn_left')),
        S('pfm_fade_in(10)'),
        *intro,
        IF('pfm_ch9_open(%d)' % n, [
            *after,
            S('pfm_set(:ch9_open%d)' % n),
            S('pfm_fade_out(10)'),
            MV(name, to(home[0], home[1], 'turn_' + d)), MV('player', to(17, 28, 'turn_left')),
            S('pfm_fade_in(10)'),
            *NELL_HEAL], [{'exit': True}])])                                           # lost: whiteout; Nell calls it again


K4 = [
    S('pfm_fade_out(12)'),
    MV('player', to(18, 19, 'turn_right')), MV('Kestrel', to(22, 19, 'turn_left')),
    MV('Juno (with Rowan)', ['turn_down']),
    S('pfm_fade_in(12)'),
    S('pbSEPlay("Crowd cheer", 90, 80)'),                                             # every gallery full
    cam('up', 8, 5), act('Juno (with Rowan)', 'hop'), {'wait': 24}, HOME,             # in the Wardens' row, Juno on her feet
    N('Pit Announcer', "FOLKS. THE FINAL."),
    N('Pit Announcer', "ON THE LEFT: THE NULL KID. ON THE RIGHT: KESTREL VANE, OF TEAM COMPOST—"),
    MV('Kestrel', ['turn_down']),                                                     # at the gantry
    P('KESTREL', 'angry', "I WILL COME UP THERE.", 'anger', 'Kestrel'),
    MV('Kestrel', ['turn_left']),
    IF('pfm?(:ch9_k4_lost)', [N('Kestrel', "Again. The crowd's had its warm-up.")], [
        N('Kestrel', "Every one of those people is here to watch me lose to you."),
        N('Kestrel', "Let's disappoint them.")]),
    IF('Prismfall.rival_battle(:RIVAL_KESTREL, "Kestrel", 4, field: :COLOSSEUM)', [
        N('Pit Announcer', "THE NULL KID! THE NULL KID TAKES THE IRONREACH OPEN!"),
        S('pbSEPlay("Crowd cheer", 100, 100)\npfm_shake(2, 10, 12)'),                # the crowd comes down the galleries
        S('pbSEPlay("Mining pick", 70, 120)'), {'wait': 8}, S('pbSEPlay("Mining pick", 70, 110)'),   # your name at the top, with a crown
        N('Kestrel', "Keep the title. I told you I'm not here for a title."),
        MV('Kestrel', ['turn_up']),                                                   # he looks up at the lowest gallery
        cam('up', 8, 5), cam('right', 8, 5), {'wait': 10},
        S('pfm_vanish("Ysolde", 24)'),
        S('pbSEPlay("Mining ping", 40, 150)'), {'wait': 30},
        "There's only a lantern-hook, swinging.",
        HOME,
        P('KESTREL', 'shocked', "...Who was that?", 'question', 'Kestrel'),
        N('Kestrel', "Never mind. Doesn't matter. Nothing matters till the vote."),
        SW('CH9_K4_DONE'), {'var': [STEP, 5]},
        S('pfm_item(:OPENCHAMPIONSCHALK, 1, "Open Champion\'s Chalk")'),
        "A stub of Nell's chalk, wrapped in a strip of red cloth. Ironreach's trophy. It's worth nothing, and nobody in Nadir would sell you one.",
        S('pfm_fade_out(12)'), MV('Kestrel', to(23, 26)), MV('player', to(18, 20)), S('pfm_fade_in(12)')],
       [S('pfm_set(:ch9_k4_lost)')])]

NELL = [IF('$game_variables[@@CH9_STEP] == 4', [open_round(1), open_round(2), open_round(3), *K4], [
            IF('$game_variables[@@CH9_STEP] == 3 && !pfm?(:ch9_bracket)', BRACKET, NELL_HEAL)])]


def fighter_pages(n):
    name, home, d, sprite, intro, _, lose = FIGHTERS[n]
    talk = [IF('pfm?(:ch9_open%d)' % n, [N(name, lose)], intro)]
    return [page([], through=True), page(talk, sprite, d, cond=V(3)), page([], cond=V(6), through=True)]


# ---------------------------------------------------------------------------------- "The Vote" (6 -> 7)
VOTE = [
    S('pfm_fade_out(0)'),
    MV('player', to(20, 11, 'turn_up')),
    *seat_all([n for n in SEATS if n != 'Rowan']),                                    # Rowan's chair is empty
    MV('Kaito', to(20, 7, 'turn_down')),                                              # below the reliquary, his hand on his chest
    MV('Juno (vote)', show('JUNO', 2) + to(15, 7)), MV('Nell (asleep)', show('NPC 06', 4) + to(16, 7, 'turn_left')),
    MV('Marchetti', show('MARCHETTI', 8) + to(24, 9, 'turn_up')),                     # the petitioners' box
    MV('Kestrel (bench)', show('KESTREL', 8) + to(24, 11, 'turn_up')),
    cam('up', 8, 8),
    S('pfm_fade_in(30)'),
    S('pbSEPlay("Ring Glass Harmonic", 50, 60)\npfm_glow(70, 8, -20, 24, 30)'),     # high above, the Fist Plate's case: a coal held in a fist
    HOME,
    P('HOLLIS', 'neutral', "The question before the Conclave.", '', 'Hollis'),
    N('Hollis', "That the Mandate granted at Lumen be extended to every land where a Lattice stands, and held by the Meridian Security Directorate until the Sovereign revokes it."),
    P('MARCHETTI', 'neutral', "The Directorate asks for the leash so it can keep the dog off the children, Chancellor.", '', 'Marchetti'),
    N('Marchetti', "That's all a leash is."),
    P('CORVIN', 'deadpan', "I've treated a great many people who were kept off things with leashes.", '', 'Corvin'),
    N('Hollis', "The Warden of Mirefen is out of order and correct."),
    N('Hollis', "The Conclave will vote. Wardens, by hand."),
    N('Hollis', "For the Mandate—"),
    {'wait': 24}, act('Magnus', 'hop'), {'wait': 24}, act('Anja', 'hop'), {'wait': 40},   # Magnus's first and steady; Anja's, slowly
    {'wait': 30},                                                                     # not Marisol's, not Sahar's, not Kaito's
    act('Rook', 'nod'), {'wait': 24},                                                 # Rook's goes halfway and stops
    by_choice('ch8_caldera', [('shutdown', [S('pfm_face("Brann", "Valen")'), {'wait': 30}, S('pfm_face("Brann", :player)'),
                                            {'wait': 40}, MV('Brann', ['turn_down'])])],   # both fists on the table
              [S('pfm_face("Brann", "Valen")'), {'wait': 50}, MV('Brann', ['turn_down']), {'wait': 10}, act('Brann', 'hop')]),
    {'wait': 10},
    S('pfm_tone(-255, -255, -255, 0, 0)'), {'wait': 30},                             # every lamp in the Iron Pit at once
    S('pbSEPlay("Crowd gasp", 90, 80)'), {'wait': 50},
    S('pbSEPlay("Glitch Tear Static", 80, 100)'),                                    # the speakers crackle
    P('SABLE', 'happy', "Vote yes on the Mandate. Go on. Give them the leash."),
    N('Sable', "We'll give you a reason."),
    S('pbSEPlay("Anim/Explosion7", 100, 60)\npbSEPlay("Mining collapse", 90, 70)\npfm_shake(9, 12, 24)'), {'wait': 24},
    S('pfm_tone(70, -60, -70, 60, 10)'),                                              # emergency lamps, red
    cam('up', 4, 6),
    MV('Cowl 1', show(HAMMER_M, 6) + to(19, 2, 'turn_right') + ['through_on', {'speed': 5}, 'right', 'right', 'right'], wait=False),
    MV('Cowl 2', show(HAMMER_F, 4) + to(27, 2, 'turn_left') + ['through_on', {'speed': 5}, 'left', 'left', 'left']),
    HOME,
    MV('Hammer porter 1', show(HAMMER_M, 8) + to(19, 22, 'turn_up') + ['through_on', {'speed': 5}] + ['up'] * 8 + ['through_off'], wait=False),
    MV('Hammer porter 2', show(HAMMER_F, 8) + to(21, 22, 'turn_up') + ['through_on', {'speed': 5}] + ['up'] * 8 + ['through_off'], wait=False),
    MV('Kestrel (bench)', ['through_on', {'speed': 5}, 'left', 'left', 'left', 'through_off', 'turn_down']),   # already moving, coat flying
    P('KESTREL', 'angry', "That's not him. That's NOT the Mourner.", '', 'Kestrel (bench)'),
    N('Kestrel', "That's the Hammer."),
    N('Kestrel', "With me. Now. Don't argue."),
    {'waitmove': True},
    MV('Sable', show('SABLE', 8) + to(20, 17, 'turn_up')), MV('Brisk', show('trainer_HOLLOW_ADMIN', 8) + to(21, 17, 'turn_up')),
    MV('Hammer porter 1', ['through_on', 'left', 'left', 'turn_right'], wait=False), MV('Hammer porter 2', ['through_on', 'right', 'right', 'turn_left'], wait=False),
    MV('player', ['through_on', 'down', 'down', 'down', 'down', 'through_off', 'turn_down'], wait=False),
    MV('Kestrel (bench)', ['through_on', 'down', 'down', 'down', 'down', 'through_off', 'turn_down']),
    {'waitmove': True},
    P('SABLE', 'happy', "Oh, it's the walking one, and the Vane boy.", '', 'Sable'),
    N('Sable', "This is going to be a lovely story afterward."),
    N('Sable', "I'll tell it on every screen in Velmora."),
    N('Captain Brisk', "Until they listen."),
    IF('pfm_ch9_tag', [
        S('pbSEPlay("Mining collapse", 100, 50)\npfm_shake(7, 8, 40)'),               # a long, grinding roar
        S('pfm_flash(150, 140, 120, 30, 255)'),                                        # half the gallery stair comes down
        *[MV('Rubble %d' % i, show('Object boulder')) for i in (1, 2, 3)],
        MV('Sable', [{'opacity': 0}]), MV('Brisk', [{'opacity': 0}]),
        MV('Hammer porter 1', [{'opacity': 0}]), MV('Hammer porter 2', [{'opacity': 0}]),
        MV('Kestrel (bench)', to(20, 7, 'turn_down')),                                 # on the far side of the fall, on his knees
        {'wait': 40},
        cam('up', 3, 5),
        P('KESTREL', 'angry', "Go UP. Go, I'll find a way round. GO.", '', 'Kestrel (bench)'),
        MV('Kestrel (bench)', ['through_on', 'left', 'left', 'left', 'left', {'opacity': 0}], wait=False),
        HOME,
        MV('Corvin', ['through_on', 'right', 'right', 'right', 'right'] + ['down'] * 8 + ['through_off']),   # over the rubble, his bag open
        MV('player', ['turn_up']),
        P('CORVIN', 'deadpan', "Hold still. I'm not asking.", '', 'Corvin'),
        S('pbSEPlay("Use item in party", 80, 100)\n$player.heal_party'), {'wait': 10},   # every Pokémon sprayed; a field dressing on your arm
        N('Corvin', "There. Now go and get hurt somewhere else."),
        S('Prismfall.checkpoint rescue nil'),                                          # losing upstairs restarts at the top of the stair
        {'var': [STEP, 7]}], [{'exit': True}])]                                        # lost: whiteout; "The Vote" again

# ---------------------------------------------------------------------------------- "Mandate Jurisdiction" (9 -> 10)
STRETCHER = ['Rowan (stretcher)', 'Squad 1', 'Squad 2', 'Squad 3', 'Squad 4']
JUNO_TALK = [
    by_choice('ch3_juno_talk', [('told', [
        P('JUNO', 'sad', "You told me a secret once. On the breakwater. About the scanner.", '', 'Juno (dust)'),
        N('Juno', "I kept it. I'm good at secrets. I just don't look it."),
        N('Juno', "I didn't know he was keeping one too."),
        N('Juno', "I didn't know everybody was.")])],
        [{'wait': 60}, S('pfm_face("Corvin", "Juno (dust)")'), {'wait': 40}]),     # a long while; Corvin sits a little way off
    by_choice('ch7_ledger', [
        ('name_him', [P('JUNO', 'sad', "You said his name in Mirefen and I ran away from you.", '', 'Juno (dust)'),
                      N('Juno', "I knew then. I knew in the dispensary."),
                      N('Juno', "I just wanted one more week of not knowing.")]),
        ('reassure', [P('JUNO', 'sad', "You said there were loads of R.A.s. You were being kind.", '', 'Juno (dust)'),
                      N('Juno', "I know you were. I wish you hadn't been.")]),
        ('ask_corvin', [P('JUNO', 'sad', "Dr Mott knew. Didn't he.", '', 'Juno (dust)'),
                        N('Juno', "He treats hands. He doesn't ask whose.")])]),
    P('JUNO', 'crying', "Don't go. Don't say anything. Just don't go.", '', 'Juno (dust)')]

MANDATE = [
    S('pfm_fade_out(0)'),
    MV('player', to(20, 22, 'turn_up')),
    MV('Rowan (stretcher)', show('ROWAN', 8) + to(20, 18, 'turn_up')),               # awake, looking at the roof
    MV('Squad 1', show(DIRECTORATE, 2) + to(19, 18)), MV('Squad 2', show(DIRECTORATE, 2) + to(21, 18)),
    MV('Squad 3', show(DIRECTORATE, 8) + to(19, 19, 'turn_up')), MV('Squad 4', show(DIRECTORATE, 2) + to(20, 17)),   # at the stretcher's head
    MV('Marchetti', show('MARCHETTI', 2) + to(20, 19)),
    MV('Hollis', to(20, 5)), MV('Sahar', to(*SEATS['Sahar'])),
    MV('Kaito', to(22, 17, 'turn_left')), MV('Valen', to(17, 19, 'turn_right')), MV('Corvin', to(18, 21, 'turn_right')),
    MV('Brann', to(16, 21, 'turn_right')), MV('Calla', to(25, 3)), MV('Nyx', to(27, 3)),
    MV('Juno (dust)', show('JUNO', 2) + to(22, 22)),
    S('pfm_tone(40, -50, -60, 60, 30)'),                                              # the emergency lamps; dust
    S('pbSEPlay("Crowd gasp", 60, 60)'),
    P('HOLLIS', 'neutral', "In the matter before the Conclave, under the emergency articles:", '', 'Hollis'),
    N('Hollis', "the Mandate is carried by acclamation—"),
    P('SAHAR', 'angry', "By WHOSE acclamation? We were under the—", '', 'Sahar'),
    N('Hollis', "—by acclamation, and in force from this hour. Director."),
    MV('Marchetti', ['through_on', 'down', 'through_off', 'turn_down']),              # she steps out of the squad
    P('MARCHETTI', 'neutral', "Rowan Ashby.", '', 'Marchetti'),
    N('Marchetti', "You're detained under the Mandate for the Lumen Shatter and the attack on this Conclave."),
    P('KAITO', 'angry', "He was pulling the wires out. I saw him.", '', 'Kaito'),
    N('Marchetti', "Then he'll say so, Warden. In custody."),
    S('pfm_face("Marchetti", "Valen")'), {'wait': 10},
    N('Marchetti', "Mandate jurisdiction, Sovereign."),
    S('pfm_face("Valen", "Rowan (stretcher)")'), {'wait': 50}, MV('Valen', ['turn_down']), {'wait': 30},
    S('pfm_face("Valen", "Juno (dust)")'), {'wait': 40},
    P('VALEN', 'sad', "...Take him.", '', 'Valen'),
    *[MV(n, ['turn_down'], wait=False) for n in STRETCHER[1:]], {'wait': 20},     # the squad lifts the stretcher
    {'var': ['ROWAN_STATUS', 1]}, {'var': ['NADIR_STATE', 1]},
    # Kestrel comes in over the fallen stair, filthy, and pushes through to the stretcher
    MV('Kestrel (bench)', show('KESTREL', 2) + to(20, 13) + ['through_on', 'down', 'down', 'down', 'right', 'down', 'through_off', 'turn_down']),
    S('pfm_face("Kestrel (bench)", "Rowan (stretcher)")'),
    {'wait': 60},                                                                     # he stares down at Rowan's face; Rowan looks back
    P('KESTREL', 'shocked', "...", '', 'Kestrel (bench)'),
    P('KESTREL', 'sad', "...It's not her.", '', 'Kestrel (bench)'),
    {'wait': 30},
    S('pfm_face("Kestrel (bench)", :player)'),
    by_choice('ch6_kestrel_rumor', [
        ('encourage', [S('pf_bond_add(:KESTREL, -3)'),
                       P('KESTREL', 'angry', "You said go. You said \"go\".", '', 'Kestrel (bench)'),
                       N('Kestrel', "I went all the way down a hole for this."),
                       N('Kestrel', "It's a GARDENER.")]),
        ('warn', [S('pf_bond_add(:KESTREL, 2)'),
                  P('KESTREL', 'angry', "You said it might not be.", '', 'Kestrel (bench)'),
                  N('Kestrel', "I hate that you were right.")]),
        ('silent', [P('KESTREL', 'angry', "Don't. Don't say anything now either.", '', 'Kestrel (bench)')])]),
    MV('Kestrel (bench)', ['through_on', 'up', 'left', 'left', 'left', 'left', 'left', 'left', {'opacity': 0}], wait=False),   # into the shafts
    # Juno, in the glass dust where the roots came up (Nell taken by her mother)
    by_choice('ch7_ledger', [('name_him', [S('pf_bond_add(:JUNO, 2)')]), ('reassure', [S('pf_bond_add(:JUNO, -2)')])]),
    MV('player', ['through_on', 'right', 'through_off', 'turn_right']),                # to Juno, in the dust
    *JUNO_TALK,
    MV('player', ['turn_down']), {'wait': 50},                                        # you sit down in the glass dust beside her
    # the stretcher passes you on its way to the cage-lift; the squad stops for him
    *[MV(n, ['through_on'] + ['down'] * (2 if n == 'Squad 2' else 4), wait=False) for n in STRETCHER],
    MV('Marchetti', ['through_on', 'down', 'down', 'down', 'down', 'down', 'down'], wait=False),
    {'waitmove': True}, {'wait': 20},
    MV('Rowan (stretcher)', ['turn_right']), S('pfm_face(:player, "Rowan (stretcher)")'), {'wait': 30},
    CH(['"Why?"', '"I\'ll look after her."', '...'], [
        [S('pf_choose(:ch9_rowan_words, :why)'), P('ROWAN', 'neutral', "Ask the Drowned Crown.", '', 'Rowan (stretcher)')],
        [S('pf_choose(:ch9_rowan_words, :look_after)'), P('ROWAN', 'sad', "I know.", '', 'Rowan (stretcher)'),
         N('Rowan', "That's why I'm not afraid.")],
        [S('pf_choose(:ch9_rowan_words, :silent)'),
         P('ROWAN', 'neutral', "You saw what I saw. In the Lowlight. Didn't you?", '', 'Rowan (stretcher)')]], cancel=3),
    *[MV(n, ['through_on'] + (['left'] if n == 'Squad 2' else []) + ['down'] * 9 + [{'opacity': 0}], wait=False) for n in STRETCHER],
    MV('Marchetti', ['through_on'] + ['down'] * 6 + [{'opacity': 0}]),
    {'waitmove': True},
    S('pbSEPlay("Door slide", 70, 60)'), {'wait': 20}, S('pbSEPlay("Elevator moving", 70, 80)'),   # the gate; the cage goes up
    SW('CH9_CONCLAVE_DONE'), {'var': [STEP, 10]}]

SEAT_TO_FILL = [
    {'wait': 30},
    MV('Valen', ['through_on', 'right', 'right', 'right', 'right', 'down', 'down', 'through_off', 'turn_down']),   # people get out of his way
    S('pfm_face(:player, "Valen")'),
    S('pbSEPlay("Ring Glass Harmonic", 40, 150)\npfm_flash(230, 240, 255, 6, 60)'),   # the glass dust on your shoulder glitters
    {'wait': 40},
    P('VALEN', 'neutral', "...", '', 'Valen'),
    P('VALEN', 'sad', "Come to Verdance.", '', 'Valen'),
    N('Valen', "There's a seat to fill."),
    N('Valen', "And I think you should see what it costs."),
    MV('Valen', ['through_on', 'left'] + ['down'] * 9 + [{'opacity': 0}], wait=False),   # to the cage-lift
    MV('Brann', ['wait 20', 'through_on', 'right', 'right', 'right', 'right', 'down', 'down', 'down', 'down', 'down', 'through_off', 'turn_up']),
    {'wait': 70},                                                                     # grief, as plain as if someone had died
    MV('Brann', ['through_on', 'down', 'down', 'down', 'down', 'down', {'opacity': 0}]),
    cam('up', 14, 6), {'wait': 20},                                                   # the observers' gallery: Voss gone, Calla the last
    MV('Calla', ['turn_down', 'wait 24', 'turn_up']),
    {'wait': 20},
    P('NYX', 'neutral', "Everything has a price, sweetheart.", '', 'Nyx'),
    N('Nyx', "Yours just went up."),
    HOME,
    {'var': [STEP, 11]},
    S('pfm_quest(:eighteen_roads, "Eighteen Roads", "Go to Verdance, as the Sovereign asked. Up the Root Road.")')]


# ---------------------------------------------------------------------------------- 263 events
def events_263():
    silent = []
    out = [at(ev('The Conclave Opens', page([]), page(ROLLCALL, cond=V(2), trigger='autorun'), page([], cond=V(3))), 0, 0),
           at(ev('The Vote', page([]), page(VOTE, cond=V(6), trigger='autorun'), page([], cond=V(7))), 1, 0),
           at(ev('Mandate Jurisdiction', page([]), page(MANDATE, cond=V(9), trigger='autorun'), page([], cond=V(10))), 2, 0),
           at(ev('A Seat to Fill', page([]), page(SEAT_TO_FILL, cond=V(10), trigger='autorun'), page([], cond=V(11))), 3, 0)]
    spans = {
        'Hollis': [(2, silent), (7, None), (9, silent), (11, None)],
        'Valen': [(2, silent), (7, None), (9, silent), (11, None)],
        'Tamsin': [(2, silent), (7, None)],
        'Brann': [(2, silent), (7, None), (9, silent), (11, None)],
        'Kaito': [(2, silent), (5, None), (6, silent), (7, None), (9, silent), (11, None)],
        'Rowan': [(2, JUNO_ROWAN), (6, None)],
        'Anja': [(2, ENVOYS), (6, silent), (7, None)],
        'Sahar': [(2, ROAM_LINES['Sahar']), (6, silent), (7, None), (9, silent), (11, None)],
        'Corvin': [(2, ROAM_LINES['Corvin']), (6, silent), (7, None), (9, silent), (11, None)],
    }
    for n in ('Dorian', 'Marisol', 'Rook', 'Odessa', 'Ilsa', 'Bastian', 'Magnus', 'Celestine', 'Sigrun'):
        spans[n] = [(2, ROAM_LINES[n]), (6, silent), (7, None)]
    for n, sp in spans.items():
        x, y = ROAM.get(n, SEATS[n])
        out.append(actor(n, x, y, SHEET[n], 'down', sp))
    out += [actor('Nyx', 31, 3, 'NYX', 'down', [(2, ROAM_LINES['Nyx']), (6, silent), (7, None), (9, silent), (11, None)]),
            actor('Voss', 24, 3, 'VOSS', 'down', [(2, VOSS), (6, silent), (7, None)]),
            actor('Calla', 25, 3, 'CALLA', 'down', [(2, VOSS), (6, silent), (7, None), (9, silent), (11, None)]),
            actor('Ysolde', 31, 9, 'YSOLDE', 'left', [(2, silent), (3, None), (4, silent), (5, None)]),
            actor('Juno (with Rowan)', 18, 10, 'JUNO', 'down', [(3, JUNO_ROWAN), (6, None)]),
            actor('Envoy of the Dominar', 23, 2, 'trainer_ASHKAAR_OFFICER', 'down', [(2, ENVOYS), (7, None)]),
            at(ev('Envoy of Ossaria', page([], through=True), page(ENVOYS, 'trainer_GENTLEMAN', 'down', cond=V(2)),
                  page([], cond={'self': 'A'}, through=True), page([], cond=V(7), through=True)), 22, 2),
            # Kestrel: by the Pit's wall once "The Bracket" has sent him there (its self switch A), then waiting for the final
            at(ev('Kestrel', page([], through=True), page(KESTREL_TALK, 'KESTREL', 'down', cond=V(3, self='A')),
                  page([N('Kestrel', "See you in the final. Don't make me wait.")], 'KESTREL', 'down', cond=V(4)),
                  page([], cond=V(5), through=True)), 23, 26),
            at(ev('Scizor', page([], through=True),
                  page([S('pbSEPlay("Cries/SCIZOR", 70, 100)')], 'Followers/SCIZOR', 'left', cond=V(4)),
                  page([], cond=V(5), through=True)), 24, 26)]
    for i, x in enumerate((19, 20, 21), 1):                                           # the fallen gallery stair
        out.append(at(ev('Rubble %d' % i, page([], through=True), page([], 'Object boulder', 'down', cond=V(7))), x, 8))
    walk_ons = ['Kestrel (bench)', 'Kestrel (bracket)', 'Juno (bracket)', 'Juno (vote)', 'Nell (asleep)', 'Marchetti',
                'Cowl 1', 'Cowl 2', 'Hammer porter 1', 'Hammer porter 2', 'Sable', 'Brisk', 'Juno (dust)'] + STRETCHER
    out += [walk_on(n, 4 + i, 0) for i, n in enumerate(walk_ons)]
    return out


def pages_263():
    return {'Nell the Chalk-Girl': [page(NELL, 'NPC 06', 'right', cond=V(3)), page([], cond=V(6), through=True)]}


# ============================================================================================ 270 / 274 Gym 8
GUIDE = [N('Gym Guide', "Kaito's gym! Fighting-types on the Colosseum."),
         N('Gym Guide', "Every knockout gets the crowd going, and a roused crowd hits harder."),
         N('Gym Guide', "Psychic and Flying go over their heads. Fairies don't care how loud it gets."),
         N('Gym Guide', "The sparring partners chase you. Every step you take, they take one."),
         N('Gym Guide', "They can't cross a rope. You can."),
         N('Gym Guide', "That's the whole lesson, apparently. Kaito says it took him nine years.")]
ODESSA = [IF('pfm?(:ch9_fly)', [P('ODESSA', 'smug', "Courier's privilege. I deliver. In person, when I like the address.", '', 'Odessa (HM02 Fly)')], [
    P('ODESSA', 'happy', "There you are. Eight badges, says the board.", '', 'Odessa (HM02 Fly)'),
    N('Odessa', "Fly's allowed at eight, and I don't trust the post to deliver it."),
    S('pbReceiveItem(:HM02)'),
    P('ODESSA', 'smug', "Courier's privilege. I deliver. In person, when I like the address.", '', 'Odessa (HM02 Fly)'),
    N('Odessa', "Come to Skyreach sometime."),
    N('Odessa', "We've got a gym, and a storm, and the best dead-letter office in the realm."),
    N('Odessa', "Don't tell anyone I said \"best\". It's a sad sort of best."),
    S('pfm_set(:ch9_fly)')])]

KAITO_EV, MEMORY_EV = 'Warden Kaito Ren', "Kaito's Lucario (Memory)"
MARROWGATE = [IF('$game_switches[343]', [P('KAITO', 'sad', "You opened it. It was empty, wasn't it.", '', KAITO_EV),
                                         N('Kaito', "...I always hoped it would be.")])]
KAITO = [
    IF('pfm?(:ch9_kaito_lost)', [P('KAITO', 'neutral', "Stand up. Again.", '', KAITO_EV)], [
        P('KAITO', 'neutral', "You won the Open.", '', KAITO_EV),
        N('Kaito', "That was for them. This isn't."),
        N('Kaito', "There's nobody watching this one."),
        N('Kaito', "Ironreach's Warden is whoever wins the Iron Trial."),
        N('Kaito', "I won it nine years ago. Every year somebody tries to take it off me."),
        N('Kaito', "Every year I'm still here."),
        N('Kaito', "Stand up. Again. That's all I teach. Ready?")]),
    IF('Prismfall.gym_battle(pfm_gym(:LEADER_KAITO), double: false)', [               # LEADER_KAITO, :COLOSSEUM, cap 43, single
        # (his LoseText is the script's "...Good. Your Pokémon fight like they remember why.")
        S('Prismfall.award_badge(pfm_gym(:LEADER_KAITO))'),
        "You received the PROMISE BADGE!",
        S('8.times { |i| pbSEPlay("Anim/HealBell", 70, 64 + i * 8); pbWait(0.22) }\npfm_glow(60, 44, 10, 20, 20)'),   # eight notes; the light pools in the corners
        N('Kaito', "It sings."),
        N('Kaito', "Memory heard it too. Look."),
        S('pfm_face("%s", :player)' % MEMORY_EV), S('pbSEPlay("Cries/LUCARIO", 50, 90)'), {'wait': 40},   # its eyes open; on your chest
        N('Kaito', "Lucario feel what's alive in a room."),
        N('Kaito', "Sometimes what's alive in a room is more than the people in it."),
        S('pbReceiveItem(:TM31)'),
        N('Kaito', "Brick Break. It goes through walls."),
        N('Kaito', "And that badge says Pokémon up to level forty-seven will heed you."),
        *MARROWGATE,
        MV('player', ['turn_down']), {'wait': 20},                                       # as you turn to go
        P('KAITO', 'sad', "A fist is a promise.", '', KAITO_EV),
        N('Kaito', "Don't make one you won't keep."),
        S('$game_variables[@@CH9_STEP] = 6 if $game_variables[@@CH9_STEP] < 6'),
        {'selfswitch': ['A', True]}], [S('pfm_set(:ch9_kaito_lost)')])]
KAITO_AFTER = [IF('$game_switches[343]', MARROWGATE[0]['then'],
                  [P('KAITO', 'sad', "A fist is a promise.", '', KAITO_EV), N('Kaito', "Don't make one you won't keep.")])]


# ============================================================================================ 261 the bulletin, then sleep
BULLETIN = [
    S('pfm_fade_out(0)'),
    MV('player', to(7, 7, 'turn_up')),
    S('pfm_fade_in(20)'),
    S('pbSEPlay("PC access", 70, 80)'),                                                # every screen in the Center
    S('3.times { pfm_tone(-20, -16, 24, 30, 3); pfm_tone(-44, -36, -6, 40, 3) }'),
    N('Gazette Reader', "...unmasked as the Grass Warden, Rowan Ashby of Verdance, who is in Directorate custody."),
    N('Gazette Reader', "The Conclave has extended the Mandate to every Lattice in the realm."),
    N('Gazette Reader', "In Lumen, Chairman Voss said Meridian \"will carry this responsibility with the seriousness it deserves\"."),
    N('Gazette Reader', "One unidentified member of the public was seen to enter the Bleed."),
    N('Gazette Reader', "Witnesses report they were unharmed."),
    MV('player', ['through_on', 'down', 'left', 'left', 'through_off', 'turn_down']),  # the board by the door
    "GAZETTE: MOURNER IS GRASS WARDEN",
    by_choice('ch9_teo_sable', [('save_teo', ["GAZETTE: EBBMOUTH BOY PULLED FROM GLASS"]),
                                ('chase_sable', ["GAZETTE: WARDEN'S BROTHER LOST IN IRONREACH GLASS"])]),
    "GAZETTE: HAMMER BOMBER STILL AT LARGE",
    MV('player', ['through_on', 'up', 'right', 'right', 'right', 'up', 'up', 'through_off', 'turn_up']),   # to the counter
    N('Nurse', "The one who walked in. That was you."),
    N('Nurse', "...Here. Your Pokémon are fine."),
    S('pbSEPlay("Anim/HealBell", 80, 100)\n$player.heal_party'), {'wait': 20},
    N('Nurse', "I checked them twice. I don't know why I checked them twice."),
    S('pfm_fade_out(40)'), {'wait': 30},                                               # a cot in the back room; sleep
    {'selfswitch': ['A', True]},
    IF('pf_interlude_start(2)', [
        S('pfm_card(:PF_IL2_CARD, "Five days earlier. Verdance.")'),
        {'transfer': {'map': 294, 'x': 8, 'y': 7, 'dir': 'down'}}], [
        # the swap could not start (a plugin missing): close Act II anyway rather than strand the save at step 11
        S('pfm_card(:PF_ACT2_END, "END OF ACT II")'),
        {'var': [STEP, 12]}, {'var': ['STORY_ACT', 3]}, {'var': ['STORY_CHAPTER', 10]},
        S('pf_chapter_card(10) if defined?(pf_chapter_card)'),
        S('pfm_fade_in(30)')])]


def events_261():
    return [at(ev('Night Bulletin', page([]), page(BULLETIN, cond=V(11), trigger='autorun'),
                  page([], cond={'self': 'A'}), page([], cond=V(12))), 0, 0)]


# ============================================================================================ 294 Interlude II
ILON = {'var': [IL, 2]}
DAWN = S('pfm_tone(26, 8, -14, 10, 30)')
def R(expr, text, emote=''): return P('ROWAN', expr, text, emote, 'PLAYER')          # the player IS Rowan here

IL2_OPEN = [DAWN, MV('player', ['turn_down']), {'wait': 24},
            S('pbSEPlay("GUI storage pick up", 70, 90)'), {'wait': 10},              # the watering can, in his left hand
            {'selfswitch': ['A', True]}]

BRIDE_TREE = [IF('pfm?(:il2_tree)', [R('neutral', "Morning, love.")], [
    MV('player', ['turn_up']),
    S('pbSEPlay("Anim/Water1", 60, 100)'), {'wait': 30}, S('pbSEPlay("Anim/Water1", 50, 90)'), {'wait': 20},   # he waters the roots
    R('neutral', "Morning, love."),
    N('Rowan', "The roses are coming in again. By the east wall."),
    N('Rowan', "They don't stop, love. They never stop."),
    N('Rowan', "Neither do you."),
    {'wait': 30},
    S('pbSEPlay("Ring Glass Harmonic", 30, 150)\npfm_flash(255, 210, 230, 8, 70)'),
    "A blossom comes down onto the back of his hand, and stays there.",
    R('shocked', "...", 'dots'),
    N('Rowan', "You've never done that before."),
    {'wait': 50},                                                                    # he doesn't brush it off
    S('pfm_set(:il2_tree)')])]

GLASSWOOD = [IF('pfm?(:il2_trev)', [R('happy', "Look at you.")], [
    S('pfm_face(:player, "Glasswood")'), S('pfm_face("Glasswood", :player)'),
    S('pbSEPlay("Cries/TREVENANT", 70, 90)'),
    R('happy', "Look at you."),
    N('Rowan', "In the spring you couldn't die and you couldn't grow. Now look."),
    N('Rowan', "You know what I'm going to do today. You've always known."),
    N('Rowan', "You never once said I shouldn't. Is that loyalty, or are you just a tree?"),
    S('pfm_face("Glasswood", "Bride Tree")'), {'wait': 24},                          # it reaches up into the Bride Tree's branches
    MV('Glasswood', [{'jump': [0, 0]}]), S('pbSEPlay("GUI storage pick up", 60, 120)'), {'wait': 20},   # one white lily
    S('pfm_face("Glasswood", :player)'), {'wait': 24},                               # it holds it out to him
    R('sad', "...Thank you."),
    "He tucks the lily into the band of his hat. Then, thinking better of it, into his coat.",
    S('pfm_set(:il2_trev)')])]

SHED = [IF('pfm?(:il2_shed)', ["The potting shed. The seed-tin labelled NOT SEEDS."], [
    MV('player', ['turn_up']), S('pfm_tone(-24, -28, -34, 24, 12)'),                 # inside: a bench, a seed-tin, an envelope
    "A seed-tin labelled NOT SEEDS. An envelope, already addressed in a careful hand: \"To the Sovereign of the Accord. From the Warden of Verdance. To be opened if.\"",
    R('neutral', "If."),
    S('pbSEPlay("Mining pick", 30, 150)'), act('PLAYER', 'shudder'), {'wait': 20},   # the ring, hard over a knuckle
    N('Rowan', "A mask can't hide a Warden's ring."),
    N('Rowan', "Everybody in Velmora knows what one looks like."),
    R('sad', "And if I don't come back, it oughtn't to be on me."),
    N('Rowan', "It ought to be on somebody who'll stay."),
    S('pbSEPlay("GUI storage put down", 60, 90)'), {'wait': 16},                    # the ring and the testament in; sealed
    "Under the address he writes: \"She's ready. She doesn't know it.\"",
    S('pbSEPlay("Cries/PIDGEY", 60, 100)'), {'wait': 24}, S('pbSEPlay("Anim/HealBell", 50, 60)'), {'wait': 20},   # a Pidgey; the Gale Post's bell
    S('pfm_fade_out(16)'), MV('player', to(3, 19, 'turn_up')), DAWN,                  # the post-box by the Heartgarden gate
    {'wait': 70},                                                                    # he holds it over the slot a long time
    S('pbSEPlay("GUI storage put down", 70, 70)'), {'wait': 20},                    # he posts it
    S('pfm_set(:il2_shed)')])]

STAIR = [IF('pfm?(:il2_tree) && pfm?(:il2_trev) && pfm?(:il2_shed)', [
    MV('player', ['turn_down']),
    S('pbSEPlay("Ring Glass Harmonic", 40, 70)\npfm_glow(10, 50, 10, 24, 30)'),     # the Meadow Plate in the roots below, warm, humming
    {'wait': 20},
    "He takes the mask out of his satchel. Ash-bark, one carved white lily. He doesn't put it on. He folds it into his coat, lily-side in, next to the real one.",
    R('sad', "One more."),
    N('Rowan', "Then I'll find the other way. I promise."),
    MV('player', ['turn_up']), {'wait': 24},                                         # to the tree
    N('Rowan', "I promise, love."),
    MV('player', ['through_on', 'left', 'left', 'left', 'left', 'through_off']),    # down the terraces toward the gate, and the road
    S('pfm_fade_out(24)'),
    MV('player', [{'opacity': 0}] + to(19, 24)), DAWN,                               # the Bride Tree, where the blossom came off
    S('pbSEPlay("Ring Glass Harmonic", 30, 160)\npfm_flash(255, 220, 235, 10, 60)'), {'wait': 70},   # a new bud already opening
    S('pfm_fade_out(30)'),
    S('pf_interlude_end'),
    S('pfm_card(:PF_ACT2_END, "END OF ACT II")'),                                     # the act's closing beat, then the next chapter's card
    {'var': [STEP, 12]}, {'var': ['STORY_ACT', 3]}, {'var': ['STORY_CHAPTER', 10]},
    S('pf_chapter_card(10) if defined?(pf_chapter_card)'),
    MV('player', [{'opacity': 255}]),
    {'transfer': {'map': 261, 'x': 7, 'y': 6, 'dir': 'down'}},                        # Chapter 10 opens there ("Morning")
    {'heal': 0},
    S('pfm_fade_in(40)')], [
    MV('player', ['dir_fix_on', 'backward', 'dir_fix_off']), N('Rowan', "Not yet.")])]


def events_294():
    out = [at(ev('Interlude II (dawn)', page([]), page(IL2_OPEN, cond=ILON, trigger='autorun'),
                 page([], cond=dict(ILON, self='A')), page([], cond={'var': [IL, 3]})), 0, 0),
           at(ev('Bride Tree', page([]), page(BRIDE_TREE, cond=ILON), page([], cond={'var': [IL, 3]})), 19, 20),
           at(ev('Glasswood', page([], through=True), page(GLASSWOOD, 'Followers/TREVENANT', 'down', cond=ILON, move='toward'),
                 page([], cond={'var': [IL, 3]}, through=True)), 9, 7)]
    for i, (x, y) in enumerate([(18, 34), (19, 34), (20, 34), (18, 35), (21, 35)], 1):
        out.append(at(ev('Stairhead (Interlude II) %d' % i, page([], through=True),
                         page(STAIR, cond=ILON, trigger='touch', through=True),
                         page([], cond={'var': [IL, 3]}, through=True)), x, y))
    return out


# ============================================================================================ main
def spec_events(fname, mid):
    import yaml
    for d in yaml.safe_load_all(open(os.path.join(SL.HERE, 'specs', fname))):
        if d and d.get('id') == mid: return d['events']


def gem_page(evs, name, i=0):
    e = next(e for e in evs if e['name'] == name)
    return {k: v for k, v in copy.deepcopy(e['pages'][i]).items() if k != 'story'}


def main():
    f260, f261, f263 = '260_ironreach.yaml', '261_ironreach_pc.yaml', '263_the_iron_pit.yaml'
    f270, f274, f294 = '270_ironreach_gym_270.yaml', '274_ironreach_gym_274.yaml', '294_the_heartgarden.yaml'
    print('map 260: %d events' % SL.patch(f260, 260, events_260(), pages_260(spec_events(f260, 260)), TAG))
    # Gemini's three Open trainers become rounds called from Nell's crate (renamed so the scenes can move them)
    for n, (name, home, d, *_rest) in FIGHTERS.items():
        SL.set_pages_at(f263, 263, list(home), fighter_pages(n), TAG, name=name)
    print('map 263: %d events' % SL.patch(f263, 263, events_263(), pages_263(), TAG))
    g270 = spec_events(f270, 270)
    guide = gem_page(g270, 'Gym Guide')
    guide['commands'] = GUIDE + [c for c in guide['commands'] if 'rope' in str(c).lower() or 'plate' in str(c).lower()]
    print('map 270: %d events' % SL.patch(f270, 270, [], {
        'Gym Guide': [guide],
        'Odessa (HM02 Fly)': [page(ODESSA, 'ODESSA', 'left', cond=V(6))]}, TAG))
    print('map 274: %d events' % SL.patch(f274, 274, [], {
        KAITO_EV: [page(KAITO, 'KAITO', 'down', cond=V(5)), page(KAITO_AFTER, 'KAITO', 'down', cond=V(5, self='A'))]}, TAG))
    print('map 261: %d events' % SL.patch(f261, 261, events_261(), None, TAG))
    g294 = spec_events(f294, 294)
    print('map 294: %d events' % SL.patch(f294, 294, events_294(), {
        'Thornguard Sentinel': [page([], cond=ILON, through=True)]}, TAG))
    shed = gem_page_or_sign(g294, 'Rowan Potting Shed Door')
    print('map 294: the potting shed (%d)' % SL.set_pages(f294, 294, 'Rowan Potting Shed Door',
                                                          [shed, page(SHED, cond=ILON), dict(shed, cond={'var': [IL, 3]})], TAG))


def gem_page_or_sign(evs, name):
    """a Gemini sign keeps its text as the first page once set_pages makes it a paged event"""
    e = next(e for e in evs if e['name'] == name)
    if e.get('type') == 'event':
        return {k: v for k, v in copy.deepcopy(e['pages'][0]).items() if k != 'story'}     # our first page IS the sign's text
    return page([e['text']])


if __name__ == '__main__':
    main()
