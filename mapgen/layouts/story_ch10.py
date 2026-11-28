#!/usr/bin/env python3
"""story_ch10: Chapter 10 "The Seat That Blooms" (story/28_SCRIPT_CH10.md) on the built Verdance maps (Gemini's
layouts/verdance_wards.py 283/284/294, layouts/verdance_gym.py 290-293; the Market Terraces 280 and the Verdance
interiors 281/282 from the wave crafts) and the Ironreach Pokémon Center 261. A STORY LAYER (storylayer.py).

  261 Ironreach PC       "Morning" (CH10_STEP 0, after Interlude II): Nell on the bench, Juno's note; the Mandate
                         scanner arch on the door (from STORY_ACT 3)
  284 Kingsgate Barbican arrival (2 -> 3): the bloom, the gate clerk's pollen cloth, the unrotted leaf; S165, V106 1
  280 Market Terraces    the florist and the Rootward boy; the royal herald (10, S126); the inbound warps to 283 / 284
                         / 296 Gemini's batch note asked for
  281 Verdance PC        the scanner arch; the Wardens' Circular (post one); the Gazette (10+); sleep (11): the night
  283 Glasshouse Ward    the Thornguard at the Heartgarden way; the gym's doors shut until the Plate (8); "on leaving
                         the gym" (9) -> the Heartgarden
  294 The Heartgarden    "Three Claimants" (3 -> 4: the testament, the ring, Tamsin and the Greenward, "You Knew" on
                         :ch2_tamsin == :keep_secret), "She's Listening" (4 -> 5, Venam's Testimony on S182), "Little
                         Gardener" (9 -> 10, :ch10_succession_stance), "Dear Uncle Rowan" (11 -> 12, STORY_CHAPTER 11)
  290 / 293 Gym 9        the guide's lines; Juno's J3 with the script's words (Prismfall.gym_battle(pfm_gym(:LEADER_JUNO)):
                         GYMS rival_battle 3 = LEADER_JUNO 30 + the starter slot; field stage 1 + min(V345, 4)), the
                         Meadow Badge, TM53, CH10_STEP 9

Not built, so not here (TODO_QUOTA / REFINE_QUEUE): 692 / 688 / 680 / 690 (0 -> 2: the Lift Road branch, Calla /
Wick / the refugees, Kestrel's envelope), 699 / 698 / 684 / 685, 681, 693, 708 the Bride Grove (5 -> 8: the Veil, the
Ogre, the Loyal Three and :ch10_ogre, the Plate accepts Juno: S127, S125, V106 2, S165 off; Valen and Tamsin at the
stairhead), 682 the Royal Chase (10 -> 11: the Queen's garden; "The Royal We"). `pfm_cutscene(:CH10_BRIDE_GROVE)`
belongs to 708 and is not called here. Gemini's 294 "South to Bride Grove" guard stays as the stairhead until 708.

Run after verdance_wards.py / verdance_gym.py / wave10_towns_craft.py 280 / wave16_final12_craft.py / ironreach_town.py:
    python3 -I layouts/story_ch10.py && python3 -I build.py 261 280 281 283 284 290 293 294 --no-preview"""
import copy, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from story_early import P, N, S, IF, CH, MV, SW, page, ev
import story_early as SE
import storylayer as SL
from story_ch9 import V as V9, at, show, to, walk_on, choice_is, by_choice, cam, HOME, act, spec_events, gem_page

TAG = 'ch10'
STEP = 'CH10_STEP'
SE.NAMES.update({'VALEN': 'Valen', 'MAELIS': 'Maelis', 'TAMSIN': 'Tamsin', 'CORVIN': 'Corvin', 'CELESTINE': 'Celestine'})
THORN = 'trainer_THORNGUARD'


def V(n, **kw): return dict({'var': [STEP, n]}, **kw)
def guard(text, se='Door slide'):
    return [S('pbSEPlay("%s", 70, 60)' % se), MV('player', ['dir_fix_on', 'backward', 'dir_fix_off']), text]


# ============================================================================================ the scanner arch
ARCH = [S('pbSEPlay("Mining ping", 60, 130)\npbWait(0.12)\npbSEPlay("Mining ping", 60, 110)'),   # a soft two-note chime
        IF('!pfm?(:pc_arch)', [
            IF(choice_is('pro_fellowship', 'accept'),
               ["◆ FELLOWSHIP PRIORITY GUEST ◆ Welcome back, \\PN. Meridian is glad you're safe."],
               ["◆ PRIORITY GUEST ◆ Welcome back, \\PN. Meridian is glad you're safe."]),
            N('Nurse', "They put them in every Center last week. Under the Mandate."),
            N('Nurse', "It's very polite. It says hello to everyone by name."),
            N('Nurse', "It says hello to me by name."),
            '\\pfe[dots]Nurse: I\'ve never told it my name.',
            S('pfm_set(:pc_arch)')])]


def arch_events(cells):
    return [at(ev('Mandate scanner arch %d' % i, page([], through=True),
                  page(ARCH, cond={'var': ['STORY_ACT', 3]}, trigger='touch', through=True)), x, y)
            for i, (x, y) in enumerate(cells, 1)]


# ============================================================================================ 261 "Morning"
MORNING = [
    S('pfm_fade_out(0)'),
    MV('player', to(7, 6, 'turn_down')),
    S('pfm_fade_in(30)'), {'wait': 20},                                              # morning; the Center is quiet
    S('pfm_face("Nell (morning)", :player)'),
    N('Nell', "You're awake."),
    N('Nell', "Mum said not to wake you. I didn't. I just waited very loudly."),
    N('Nell', "The lady with the flowers. Juno."),
    N('Nell', "She went up with the Sovereign's people in the night. In the Sovereign's own cage."),
    N('Nell', "She didn't want to go and she didn't want to stay."),
    N('Nell', "She left you this."),
    MV('Nell (morning)', ['up', 'turn_up']), S('pbSEPlay("GUI storage pick up", 70, 110)'),
    '"\\PN — They\'re taking me to Verdance. The Sovereign says I have to be there when they open his letter. I don\'t know what letter. I don\'t know anything any more. Come the long way if you want. I\'d understand. I\'d come the long way. — J."',
    act('Nell (morning)', 'hop'),                                                    # holding up her chalk
    N('Nell', "She saved me."),
    N('Nell', "The roots came up and she had her arms round me and I couldn't see anything but flowers."),
    N('Nell', "Tell her I've got the neatest S in Ironreach and she can have it."),
    MV('Nell (morning)', ['down', 'turn_up']),
    S('pfm_quest(:eighteen_roads, "Eighteen Roads", "Go to Verdance. Up the Root Road: the Tailings, the Rootdeep\'s Lift Road, then the Crown Road west.")'),
    {'selfswitch': ['A', True]}]


def events_261():
    return [at(ev('Morning', page([]), page(MORNING, cond=V9(12), trigger='autorun'), page([], cond={'self': 'A'}),
                  page([], cond=V(1))), 1, 0),
            at(ev('Nell (morning)', page([], through=True),
                  page([N('Nell', "Tell her I've got the neatest S in Ironreach and she can have it.")], 'NPC 06', 'up', cond=V9(12)),
                  page([], cond=V(1), through=True)), 7, 8)] + arch_events([(6, 9), (7, 9), (8, 9)])


# ============================================================================================ 284 arrival (2 -> 3)
ARRIVAL = [
    S('pfm_fade_out(0)'),
    MV('player', to(19, 20, 'turn_up')),
    S('pfm_fade_in(24)'),
    S('pbSEPlay("Sweet Scent", 70, 80)\npfm_tone(34, 26, -18, 0, 40)'),             # the air gold with pollen, drifting like snow
    cam('up', 7, 4), {'wait': 50}, HOME,                                             # terraces of white stone under roses and vines
    MV('Gate Clerk', ['through_on', 'right', 'right', 'down', 'down', 'down', 'down', 'through_off', 'turn_down']),
    S('pbSEPlay("GUI storage pick up", 60, 110)'),                                  # a cloth mask, without being asked
    N('Gate Clerk', "Pollen. Wear it. It's not poison. It just won't stop."),
    N('Gate Clerk', "Since the Warden went, the Meadow Plate's had nobody to hold it in."),
    N('Gate Clerk', "It's... spilling. Three days, the whole city."),
    N('Gate Clerk', "The bakers can't keep the bread from sprouting."),
    MV('Gate Clerk', ['through_on', 'up', 'up', 'up', 'up', 'left', 'left', 'through_off', 'turn_down'], wait=False),
    S('pfm_face(:player, "Woman with a Trowel")'),
    S('3.times { pbSEPlay("Mining pick", 45, 140); pbWait(0.35) }'),               # scraping at the bloom on the cobbles
    "Under the flowers the soil is grey and dry. The dead leaf she lifts out of it isn't rotten. It's exactly as it fell.",
    N('Woman with a Trowel', "Nothing rots in Verdance. My nan used to say it like it was a blessing."),
    SW('THORNGUARD_HEARTGARDEN'), {'var': ['VERDANCE_BLOOM', 1]}, {'var': [STEP, 3]},
    S('pfm_quest(:eighteen_roads, "Eighteen Roads", "The Sovereign is in the Heartgarden. Go up through the Market Terraces.")')]


def events_284():
    return [at(ev('Kingsgate Arrival', page([]), page(ARRIVAL, cond=V(2), trigger='autorun'), page([], cond=V(3))), 0, 0)]


# ============================================================================================ 280 the Market Terraces
HERALD = [   # "The next morning" (10): S126
    MV('Royal Herald', show(THORN, 2) + [{'script': 'moveto($game_player.x, $game_player.y - 2)'}, 'turn_down']),
    S('pbSEPlay("Anim/HealBell", 60, 120)'), S('pfm_face(:player, "Royal Herald")'), {'wait': 16},   # a scroll with a lot of ribbon
    N('Royal Herald', "Her Majesty Queen Maelis Thorne, in these troubled times, of Her great love for Her people, throws open to them the Royal Chase, Her Majesty's own hunting reserve, for their recreation and the catching of game."),
    N('Royal Herald', "God save the Queen."),
    N('Florist', "That's for the papers. It's still a lovely park."),
    SW('CH10_ROYAL_CHASE_OPEN'),
    MV('Royal Herald', ['through_on', 'up', 'up', 'up', {'opacity': 0}]),
    {'selfswitch': ['A', True]}]
ROOTWARD_BOY = [N('Rootward Boy', "Mum says the old Warden was a bad man."),
                N('Rootward Boy', "Gran says he watered our street's trees every year for nothing."),
                N('Rootward Boy', "Mum says that's what bad men do, to make you like them."),
                N('Rootward Boy', "Gran says Mum's never watered anything.")]
FLORIST = [N('Florist', "I'm the only florist in Velmora going out of business because of flowers.")]


def warp(name, x, y, to_map, tx, ty, d):
    return {'type': 'warp', 'name': name, 'at': [x, y], 'to': {'map': to_map, 'x': tx, 'y': ty, 'dir': d}, 'se': 'Door exit'}


def events_280():
    return ([at(ev('Royal Herald (scene)', page([]), page(HERALD, cond=V(10), trigger='autorun'), page([], cond={'self': 'A'}),
                   page([], cond=V(11))), 0, 0), walk_on('Royal Herald', 1, 0)] +
            # Gemini's batch note: 283 / 284 / 296 lead back here; these lead there
            [warp('To Glasshouse Ward %d' % y, 99, y, 283, 2, 19, 'right') for y in (66, 67)] +
            [warp('To Kingsgate Barbican %d' % x, x, 87, 284, 19, 8, 'down') for x in range(33, 40)] +
            [warp('To Rootward %d' % y, 4, y, 296, 2, 15, 'right') for y in (74, 75)])


# ============================================================================================ 281 the Verdance PC
CIRCULAR = ["WARDEN CIRCULAR — GALE POST RELAY, WARDENS ONLY. (Somebody has left it on the public board.)",
            "ODESSA: relay test. is this thing on. who's still talking to who after ironreach",
            "DORIAN: *Enter, stage left, seventeen Wardens, not looking at each other.*",
            "ILSA: Corvin, stop composing that. We can all feel you composing it.",
            "CORVIN: I wasn't going to send it.", "CORVIN: I've sent it.", "CORVIN: Disregard.",
            "BASTIAN: Re: Saltmere harvest supper invitation (AF 299). Yes please.",
            "ANJA: Toes."]
GAZETTE = ["GAZETTE: JUNO HALE CONFIRMED: PLATE ACCEPTS 15-YEAR-OLD",
           by_choice('ch10_succession_stance', [('accord', ["GAZETTE: NULL WITNESS BACKS SOVEREIGN"]),
                                                ('kingdoms', ["GAZETTE: NULL WITNESS: GIVE THEM TO THE CROWNS"]),
                                                ('nobody', ["GAZETTE: 'NOBODY', SAYS THE NULL"])])]
SLEEP_281 = [   # "autorun on sleeping at 281 with V131 == 11": the night in the Heartgarden
    S('pfm_fade_out(0)'), MV('player', to(7, 4, 'turn_up')), S('pfm_fade_in(16)'),
    N('Nurse', "You look done in. There's a cot in the back. Go on."),
    S('pfm_fade_out(40)'), {'wait': 20},
    S('pfm_set(:ch10_night)'),
    {'selfswitch': ['A', True]},
    {'transfer': {'map': 294, 'x': 11, 'y': 8, 'dir': 'up'}}]


def events_281():
    return ([at(ev("Wardens' Circular", page(CIRCULAR)), 13, 3),
             at(ev('Gazette board', page(["The Gazette board is papered over with notices about the pollen."]),
                   page(GAZETTE, cond=V(10))), 12, 7),
             at(ev('Sleep (night)', page([]), page(SLEEP_281, cond=V(11), trigger='autorun'), page([], cond={'self': 'A'}),
                   page([], cond=V(12))), 0, 0)] + arch_events([(6, 8), (7, 8), (8, 8)]))


# ============================================================================================ 283 the Glasshouse Ward
TO_HEARTGARDEN = [S('pfm_fade_out(24)'), {'transfer': {'map': 294, 'x': 21, 'y': 8, 'dir': 'right'}}]   # "on leaving the gym"


def events_283():
    return [at(ev('Thornguard (Heartgarden way)', page([], through=True),
                  page([N('Thornguard', "The Heartgarden's closed by order of Her Majesty, Queen Maelis Thorne, pending the succession."),
                        S('pfm_face("Thornguard (Heartgarden way)", :player)'), {'wait': 16},
                        N('Thornguard', "— Oh. You're expected. Go up.")], THORN, 'left', cond=V(3)),
                  page([], cond=V(8), through=True)), 45, 10),
            at(ev('Gym 9 doors (shut)', page(guard("The Heartgarden Gym's glass doors are shut. Nobody has opened them since the Warden went."),
                                             trigger='touch', through=True),
                  page([], cond=V(8), through=True)), 24, 9),
            at(ev('Little Gardener (way up)', page([]), page(TO_HEARTGARDEN, cond=V(9), trigger='autorun'), page([], cond=V(10))), 0, 0)]


# ============================================================================================ 294 "Three Claimants" (3 -> 4)
TESTAMENT = [
    S('pfm_fade_out(0)'),
    MV('player', to(21, 8, 'turn_right')),
    MV('Valen (chapel)', show('VALEN', 2) + to(30, 7)), MV('Juno (chapel)', show('JUNO', 8) + to(30, 8, 'turn_up')),
    MV('Maelis', show('MAELIS', 2) + to(27, 8, 'turn_right')),
    MV('Thornguard 1', show(THORN, 6) + to(25, 8, 'turn_right')), MV('Thornguard 2', show(THORN, 6) + to(26, 8, 'turn_right')),
    MV('Caedmon', show('NPC 21', 4) + to(32, 8, 'turn_left')), MV('Meridian Delegate', show('trainer_MERIDIAN_AGENT_F', 4) + to(33, 8, 'turn_left')),
    MV('Press Clerk', show('NPC 22', 6) + to(22, 7, 'turn_right')),
    S('pfm_tone(30, 22, -16, 0, 0)'),                                                # a jungle of blossom; the air gold
    cam('right', 7, 6),
    S('pfm_fade_in(30)'), {'wait': 20},
    P('MAELIS', 'neutral', "The Meadow Plate lies on Crown soil, Sovereign.", '', 'Maelis'),
    N('Maelis', "It has done since my great-great-grandmother planted this garden."),
    N('Maelis', "A Warden kept it for the Crown. There is no Warden."),
    N('Maelis', "So the Crown will keep it."),
    N('Meridian Delegate', "With respect, Majesty, the Plate is overflowing."),
    N('Meridian Delegate', "Meridian can offer temporary custody, for public safety."),
    N('Meridian Delegate', "Our dampers held the Quiet Ward through worse."),
    N('Meridian Delegate', "We'd ask nothing but the right to keep the city breathing."),
    MV('Caedmon', ['turn_down', 'wait 8', 'turn_left', 'wait 8', 'turn_up', 'wait 8', 'turn_left']),   # smiling at everyone, the Plate too
    N('Prince Caedmon', "Mother, it's a very generous offer."),
    P('MAELIS', 'deadpan', "Caedmon, you've called everything Meridian offers generous since you were twelve.", '', 'Maelis'),
    N('Maelis', "It's how I know what you're for."),
    P('VALEN', 'neutral', "A Warden's testament is law under the Concordance, Majesty.", '', 'Valen (chapel)'),
    N('Valen', "Older than either of us. Rowan Ashby left one."),
    N('Valen', "I'll read it now, in front of everyone, because nobody here trusts anybody to read it privately."),
    S('pbSEPlay("GUI storage pick up", 70, 90)'), {'wait': 16},                    # he breaks the seal: a letter, and a small ring
    P('VALEN', 'neutral', "\"To the Sovereign of the Accord, from the Warden of Verdance. To be opened if.\"", '', 'Valen (chapel)'),
    N('Valen', "\"If you are reading this, I didn't come back from Ironreach, or I came back in irons. Either way, the garden needs a gardener.\""),
    N('Valen', "\"I name as my heir to the seat of Verdance and the keeping of the Meadow Plate my niece, Juno Hale.\""),
    S('pbBGSFade(1.0) rescue nil'), {'wait': 60},                                     # the garden goes very quiet. Even the bees.
    N('Valen', "\"She has been talking to plants since she could talk, and they have been listening. She'll say she isn't ready. She is. She doesn't know it.\""),
    N('Valen', "\"Rowan Ashby, Warden of Verdance, twenty-fourth year.\""),
    P('VALEN', 'sad', "There's a postscript.", '', 'Valen (chapel)'),
    N('Valen', "\"Water Elin at dawn. She likes it before the bees are up.\""),
    act('Juno (chapel)', 'shudder'),                                                 # a stair that isn't there
    P('JUNO', 'crying', "...", 'dots', 'Juno (chapel)'),
    MV('Valen (chapel)', ['through_on', 'down', 'through_off', 'turn_down']),       # down the steps; the ring into her palm
    MV('Juno (chapel)', ['through_on', 'down', 'through_off', 'turn_up']),
    S('pbSEPlay("GUI storage put down", 60, 140)'), {'wait': 20},
    P('VALEN', 'neutral', "His ring. A Warden's ring, cut by the Hearthguild.", '', 'Valen (chapel)'),
    N('Valen', "It'll answer you, or it won't. Mine took a year."),
    P('JUNO', 'sad', "I didn't want this seat. I wanted HIM in it.", '', 'Juno (chapel)'),
    P('VALEN', 'sad', "I know.", '', 'Valen (chapel)'),
    N('Valen', "A Warden is confirmed when the Plate accepts them, Juno."),
    N('Valen', "The Plate is at the bottom of that stair, in the Bride Tree's roots, under that."),
    MV('Valen (chapel)', ['turn_left']), {'wait': 30},                               # at the Veil across the stairhead; then at you
    S('pfm_face("Valen (chapel)", :player)'), {'wait': 20},
    P('VALEN', 'neutral', "And only one person in Verdance can walk through that.", '', 'Valen (chapel)'),
    {'var': [STEP, 4]},
    # Tamsin, up the garden path from the gate at a run, out of breath, a moth-wing shawl and a satchel of thread
    MV('Tamsin', show('TAMSIN', 6) + to(16, 8, 'turn_right') + ['through_on', {'speed': 5}] + ['right'] * 12 + ['through_off', 'turn_right']),
    P('TAMSIN', 'panic', "Sorry — sorry — the Briarwick coach lost a wheel in the briar — sorry.", '', 'Tamsin'),
    N('Tamsin', "Am I late? I'm late."),
    S('pfm_face("Tamsin", "Juno (chapel)")'),
    P('TAMSIN', 'neutral', "Juno. Briarwick stands with Verdance. Whoever sits it.", '', 'Tamsin'),
    N('Tamsin', "That's all. I came to say it in front of people."),
    N('Tamsin', "A thread holds because it's twisted with others. Alone it's just string."),
    P('JUNO', 'sad', "...Thank you.", '', 'Juno (chapel)'),
    S('2.times { pbSEPlay("Mining pick", 30, 170); pbWait(0.2) }'),                 # scribbling at the garden wall
    N('Press Clerk', "\"Small-town Warden backs the niece.\""),
    N('Press Clerk', "Is it a bloc? Are you a bloc? Can I call it the Green Ward?"),
    P('TAMSIN', 'panic', "I— it's not a— we're not—", '', 'Tamsin'),
    N('Press Clerk', "\"The Greenward.\" Lovely. That'll sell."),
    IF(choice_is('ch2_tamsin', 'keep_secret'), [   # "You Knew": three Lowmarsh weavers push to the front
        *[MV('Weaver %d' % i, show('NPC 1%d' % (i + 3), 6) + to(15 + i, 8, 'turn_right') + ['through_on'] + ['right'] * 3 + ['through_off', 'turn_right'], wait=False) for i in (1, 2, 3)],
        {'waitmove': True},
        N('Lowmarsh Weaver', "Briarwick stands with Verdance? Briarwick signed with MERIDIAN."),
        N('Lowmarsh Weaver', "She signed alone. The Glasswood's at our looms because she signed."),
        N('Lowmarsh Weaver', "They took Mara at Lumen. She'd be stood here saying it."),
        N('Lowmarsh Weaver', "So we're saying it. You KNEW, Warden."),
        S('pfm_face("Tamsin", "Weaver 3")'),
        P('TAMSIN', 'sad', "...", 'dots', 'Tamsin'),
        CH(["Step between them.", "Let Tamsin answer."], [
            [P('TAMSIN', 'neutral', "No. No, don't.", '', 'Tamsin'),
             MV('Tamsin', ['through_on', 'left', 'left', 'left', 'left', 'left', 'through_off', 'turn_left'])],   # a hand on your arm; past you
            [MV('player', ['dir_fix_on', 'backward', 'dir_fix_off'])]], cancel=2),     # you step back
        P('TAMSIN', 'sad', "Yes. I knew.", '', 'Tamsin'),
        N('Tamsin', "I signed it alone, in the spring, and I've been sorry every day, and being sorry hasn't moved the glass an inch."),
        N('Tamsin', "I'm not here because I'm good. I'm here because she is."),
        N('Tamsin', "Stand with her too. Then shout at me after."),
        N('Tamsin', "I'll be at the Briarwick coach. It's got three wheels."),
        MV('Weaver 1', ['turn_right', 'wait 10', 'turn_left']), act('Weaver 2', 'nod'),   # one of them nods, once
        *[MV('Weaver %d' % i, ['through_on', 'left', 'left', 'left', 'left', {'opacity': 0}], wait=False) for i in (1, 2, 3)]]),
    S('pfm_fade_out(30)'),                                                           # later: the crowd goes down the hill
    *[MV(n, [{'opacity': 0}], wait=False) for n in ('Valen (chapel)', 'Juno (chapel)', 'Maelis', 'Thornguard 1', 'Thornguard 2',
                                                    'Caedmon', 'Meridian Delegate', 'Press Clerk', 'Tamsin')],
    HOME,
    S('pbBGSPlay($game_map.bgs) rescue nil'),
    S('pfm_fade_in(30)')]

# ---------------------------------------------------------------------------------- "She's Listening" (4 -> 5)
J = 'Juno Hale'
VENAM = [S('pbSEPlay("Glitch Tear Static", 50, 120)'), {'wait': 10},             # the little recording crackles
         N('Venam (recording)', "I was stone for— I don't know how long. And I could hear everything."),
         N('Venam (recording)', "Everyone who sat with me. Every stupid joke."),
         N('Venam (recording)', "I could hear all of it."),
         {'wait': 40},                                                               # Juno is very still
         P('JUNO', 'crying', "...Everything?", 'dots', J),
         MV(J, ['turn_up']), {'wait': 20},                                          # both hands flat on the bark
         N('Juno', "Aunt Elin. It's Juno. I'm fifteen."),
         N('Juno', "I've got a satchel of seeds and a friend who walks into things."),
         N('Juno', "Uncle Rowan's in prison."),
         N('Juno', "He did something terrible and something brave on the same day and I don't know which one he is."),
         P('JUNO', 'sad', "They want me to have your garden. I'm so frightened.", '', J),
         S('pfm_tone(-20, -20, -10, 20, 30)'), {'wait': 40},                         # she talks to the tree a long time; you sit with her
         S('3.times { pbSEPlay("Ring Glass Harmonic", 25, 160); pfm_flash(255, 215, 235, 8, 50); pbWait(0.6) }'),   # petals; they're falling now
         S('pfm_fade_in(30)'), MV(J, ['turn_down'])]
LISTENING = [
    S('pfm_face(:player, "%s")' % J),
    P('JUNO', 'neutral', "You've heard about her. Everyone has. This is her.", '', J),
    N('Juno', "Aunt Elin. AF 288."),
    N('Juno', "She was weeding the Heartgarden and the Bleed came up through the roots like a spring, and she stood up, and she put her arms up, like this, and that's how she stayed."),
    P('JUNO', 'sad', "I was three. They told me she'd gone away.", '', J),
    N('Juno', "I believed them till I was eight, and then he walked me up here at dawn and showed me, and held my hand, and watered her."),
    N('Juno', "Every dawn. Twelve years. He never missed one."),
    N('Juno', "Not even for Ironreach. He must have gone the morning he left."),
    N('Juno', "Sometimes I think she's listening. Isn't that stupid?"),
    IF('$game_switches[@@CAMEO_VENAM_DONE]',
       [CH(["Play her Venam's Testimony.", "Not now."], [VENAM, []], cancel=2)],
       [CH(["It isn't stupid.", "..."], [
           [P('JUNO', 'sad', "Dr Mott said they dream. In the Ward.", '', J),
            N('Juno', "He said he'd never said it out loud before. He said it to you."),
            P('JUNO', 'neutral', "So maybe she's dreaming. Maybe it's a nice one.", '', J),
            N('Juno', "I hope I'm in it, a bit.")],
           [P('JUNO', 'neutral', "Yes. That's what I think too, mostly.", '', J)]], cancel=2)]),
    act(J, 'hop'), MV(J, ['turn_down']),                                             # up, wiping her face with a glove (worse)
    P('JUNO', 'neutral', "Right. Right. Down the stairs. Into the horrible black flowers.", '', J),
    N('Juno', "You first, please. I'll be right behind you."),
    P('JUNO', 'sad', "I'll be RIGHT behind you.", '', J),
    {'var': [STEP, 5]}]

# ---------------------------------------------------------------------------------- "Little Gardener" (9 -> 10)
GARDENER = [
    S('pfm_fade_out(0)'),
    MV('player', to(21, 8, 'turn_right')),
    MV('Juno (chapel)', show('JUNO', 6) + to(29, 8, 'turn_right')),
    MV('Maelis', show('MAELIS', 6) + to(26, 8, 'turn_right')),
    MV('Thornguard 1', show(THORN, 6) + to(24, 8, 'turn_right')), MV('Thornguard 2', show(THORN, 6) + to(25, 8, 'turn_right')),
    MV('Caedmon', show('NPC 21', 6) + to(27, 8, 'turn_right')),
    MV('Meridian Delegate', show('trainer_MERIDIAN_AGENT_F', 4) + to(31, 8, 'turn_left')),
    MV('Press Clerk', show('NPC 22', 6) + to(22, 7, 'turn_right')), MV('Press 2', show('NPC 25', 6) + to(23, 7, 'turn_right')),
    cam('right', 6, 6),
    S('pfm_fade_in(30)'), {'wait': 20},                                              # tamed: flowers that know where they're meant to be
    N('Meridian Delegate', "Warden Hale. Congratulations."),
    N('Meridian Delegate', "Meridian's offer stands: a Lattice for Verdance, to draw the excess from the Plate."),
    N('Meridian Delegate', "Verdance would never drown again. Free light for every terrace."),
    {'wait': 20}, MV('Juno (chapel)', ['turn_down', 'wait 20', 'turn_right', 'wait 20', 'turn_down', 'wait 20', 'turn_right']),   # the folder; the delegate; the ring
    P('JUNO', 'neutral', "No, thank you.", '', 'Juno (chapel)'),
    N('Meridian Delegate', "I'm sorry?"),
    P('JUNO', 'neutral', "I've been to Mirefen, where the Lattice runoff makes the marsh glow.", '', 'Juno (chapel)'),
    N('Juno', "I've been to Lumen, where it cracked the Plate."),
    N('Juno', "I've been to Briarwick, where it fed the Glasswood."),
    N('Juno', "I'm fifteen and I've seen three."),
    P('JUNO', 'angry', "Verdance doesn't need a Lattice to stop it drowning.", '', 'Juno (chapel)'),
    N('Juno', "It needed a Warden. It's got one. No, thank you."),
    S('pbSEPlay("GUI storage put down", 60, 80)'),                                  # the delegate closes the folder
    MV('Caedmon', ['turn_right', 'wait 10', 'turn_left', 'wait 10', 'turn_right']),   # Caedmon smiles at all of them, warmly
    MV('Juno (chapel)', ['turn_left']),
    P('JUNO', 'neutral', "And Majesty. Your Thornguard are standing in my garden.", '', 'Juno (chapel)'),
    P('MAELIS', 'neutral', "Our garden, child. The Heartgarden is on Crown soil.", '', 'Maelis'),
    P('JUNO', 'neutral', "Then your soil's in my garden. Please take your men off it.", '', 'Juno (chapel)'),
    N('Juno', "They're standing on the tulips."),
    {'wait': 70},                                                                    # a very long pause; the whole Heartgarden waits
    S('pbSEPlay("Crowd gasp", 40, 140)'),                                           # the Queen laughs, a dry little sound like a seed-pod
    P('MAELIS', 'smug', "Thornguard. Off the tulips.", '', 'Maelis'),
    MV('Thornguard 1', ['through_on', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', {'opacity': 0}], wait=False),
    MV('Thornguard 2', ['through_on', 'wait 8', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', {'opacity': 0}]),
    P('MAELIS', 'neutral', "Little gardener. We'll see how long you bloom.", '', 'Maelis'),
    MV('Caedmon', ['through_on', 'left', 'turn_right'], wait=False),
    MV('Maelis', ['through_on', {'speed': 2}] + ['left'] * 9 + [{'opacity': 0}], wait=False),   # slowly, on her cane; she doesn't lean on him
    MV('Caedmon', ['through_on', 'wait 4', {'speed': 2}] + ['left'] * 9 + [{'opacity': 0}]),
    {'waitmove': True},
    MV('Press Clerk', ['turn_down']), S('pfm_face("Press Clerk", :player)'), S('pfm_face(:player, "Press Clerk")'),
    N('Press Clerk', "You! You're the one from Ironreach. The one who walked into the glass. You were in the grove with her."),
    N('Press Clerk', "Everyone's asking. The Queen says the Plates are the Crown's. Meridian says they're everybody's, under Meridian. The Accord says they're the Wardens'. Who should own the Plates?"),
    CH(["The Wardens. The Accord.", "The kingdoms. The land they're in.", "Nobody."], [
        [S('pf_choose(:ch10_succession_stance, :accord)'),
         N('Press Clerk', "\"Null Witness Backs Sovereign.\" Good. Solid. Boring. Thank you.")],
        [S('pf_choose(:ch10_succession_stance, :kingdoms)'),
         N('Press Clerk', "\"Null Witness: Give Them to the Crowns.\""),
         N('Press Clerk', "Oh, the Queen'll like that. The Thane'll like that."),
         N('Press Clerk', "The Dominar'll LOVE that.")],
        [S('pf_choose(:ch10_succession_stance, :nobody)'),
         '\\pfe[question]Press Clerk: ...Nobody?',
         N('Press Clerk', "You mean... nobody should HAVE them? Then who keeps them?"),
         {'wait': 40}, S('4.times { pbSEPlay("Mining pick", 25, 170); pbWait(0.25) }'),   # you don't answer; the clerk writes a long time
         N('Press Clerk', "\"Nobody,\" says the null. Well. That's a headline."),
         N('Press Clerk', "I don't know what it means. I don't think I'm supposed to."),
         # at the back of the crowd an old woman in a moth-silk shawl, flowers in her hair, smiling at you
         MV('Old woman in moth-silk', show('NPC 11', 6) + to(17, 8, 'turn_right')),
         MV('player', ['turn_left']), {'wait': 50}, MV('player', ['turn_right']), {'wait': 10},
         MV('Old woman in moth-silk', [{'opacity': 0}]), MV('player', ['turn_left']), {'wait': 20}]], cancel=0),   # when you look again, she's gone
    {'var': [STEP, 10]},
    S('pfm_fade_out(24)'),
    *[MV(n, [{'opacity': 0}], wait=False) for n in ('Juno (chapel)', 'Meridian Delegate', 'Press Clerk', 'Press 2')],
    HOME, S('pfm_fade_in(24)')]

# ---------------------------------------------------------------------------------- "Dear Uncle Rowan" (11 -> 12)
NIGHT = [
    MV('player', [{'opacity': 0}] + to(11, 8, 'turn_up')),
    MV('Juno (night)', show('JUNO', 8) + to(8, 7, 'turn_up')),                       # at the shed bench, in her nightdress and her wreath
    S('pfm_tone(-90, -80, -30, 60, 0)'), {'wait': 10},
    S('pfm_tone(-70, -66, -20, 50, 40)'), {'wait': 30},                              # the flowers closed for the night; a lamp in the shed
    S('pbSEPlay("Mining pick", 25, 180)'), {'wait': 30}, S('pbSEPlay("Mining pick", 25, 180)'), {'wait': 20},   # three words; stop; crossed out
    'Dear Uncle Rowan,',
    'Crossed out: "How could you" — "Are you hurt" — "I took your seat, I\'m sorry" — "I watered her this morning. Before the bees."',
    *[x for _ in range(3) for x in (MV('Juno (night)', ['turn_down', {'jump': [0, 0]}, 'wait 6', 'turn_up']),     # the page, balled up, into the dark
                                    S('pbSEPlay("GUI storage put down", 40, 150)\npbWait(0.4)\npbSEPlay("Ring Glass Harmonic", 20, 170)\npfm_flash(240, 240, 255, 6, 40)'),
                                    {'wait': 24})],                                  # where each lands, a small white flower comes up
    {'wait': 30},
    MV('Juno (night)', ['turn_up']), {'wait': 60},                                   # her head down on the bench beside the lamp
    IF(choice_is('ch10_ogre', 'ogre'), [MV('Ogre (night)', show('Followers/OGERPON', 2) + to(9, 8)), {'wait': 60}]),   # a small masked shape keeps watch
    S('pfm_fade_out(40)'),
    S('pfm_set(:ch10_night, false)'),
    {'var': [STEP, 12]}, {'var': ['STORY_CHAPTER', 11]},
    S('pf_chapter_card(11) if defined?(pf_chapter_card)'),
    S('pfm_quest(:eighteen_roads, "Eighteen Roads", "Earn the tenth badge in Rimeholt, up the Hart Road through the Hoarwood into Isenmar. Juno wants to come.")'),
    MV('player', [{'opacity': 255}]),
    {'selfswitch': ['A', False]},
    {'transfer': {'map': 281, 'x': 7, 'y': 4, 'dir': 'down'}},
    {'heal': 0},
    S('pfm_fade_in(40)')]


def events_294():
    scene = lambda name, cmds, n, x: at(ev(name, page([]), page(cmds, cond=V(n), trigger='autorun'), page([], cond=V(n + 1))), x, 0)
    walk_ons = ['Valen (chapel)', 'Juno (chapel)', 'Maelis', 'Thornguard 1', 'Thornguard 2', 'Caedmon', 'Meridian Delegate',
                'Press Clerk', 'Press 2', 'Tamsin', 'Weaver 1', 'Weaver 2', 'Weaver 3', 'Old woman in moth-silk',
                'Juno (night)', 'Ogre (night)']
    return [scene('Three Claimants', TESTAMENT, 3, 1), scene('Little Gardener', GARDENER, 9, 2),
            # the night: 281's cot sets :ch10_night; a parallel page turns it into this autorun (walking in at 11 by day plays nothing)
            at(ev('Dear Uncle Rowan', page([]),
                  page([IF('pfm?(:ch10_night)', [{'selfswitch': ['A', True]}])], cond=V(11), trigger='parallel'),
                  page(NIGHT, cond=V(11, self='A'), trigger='autorun'),
                  page([], cond=V(12))), 3, 0)] + \
           [walk_on(n, 4 + i, 0) for i, n in enumerate(walk_ons)]


def pages_294(spec_events):
    """Gemini's Juno at the tree: hidden from K4 (S122) until "She's Listening" (4), which plays on her; Gemini's
    own page again once she is Warden (8)"""
    g0 = gem_page(spec_events, J)
    return {J: [page([], cond={'switch': 'CH9_K4_DONE'}, through=True),
                page(LISTENING, 'JUNO', 'up', cond=V(4)),
                page([], cond=V(5), through=True),
                dict(g0, cond=V(8))]}


# ============================================================================================ 290 / 293 Gym 9
GUIDE = [N('Gym Guide', "The Heartgarden Gym. Grass-types on a Flower Garden that grows while you fight."),
         N('Gym Guide', "Fire, Ice, Flying, Poison and Bug go straight through them."),
         N('Gym Guide', "Be honest with yourself about Fire: you'll burn the garden down at full bloom, and that's a strategy."),
         N('Gym Guide', "Every hedge you leave in the beds, the Warden's garden starts one stage taller."),
         N('Gym Guide', "Fewer waterings, harder fight. Your call."),
         N('Gym Guide', "She told me to say \"your call\". She feels very strongly about it being your call.")]
JE = 'Warden Juno Hale'
J3 = [
    IF('pfm?(:ch10_j3_lost)', [P('JUNO', 'happy', "Again! Sorry. That came out bossy. I'm practising being in charge.", '', JE)], [
        IF('$game_variables[345] >= 3', [P('JUNO', 'shocked', "You let it grow? For me?", '', JE),
                                         N('Juno', "...That's either kind or tactical and I'm too nervous to ask which.")]),
        P('JUNO', 'sad', "I didn't want this seat. I wanted him in it.", '', JE),
        P('JUNO', 'neutral', "But the city's drowning in flowers and nobody else is coming, so.", '', JE),
        P('JUNO', 'happy', "Hi. I'm the Warden of Verdance.", '', JE),
        N('Juno', "Please don't go easy on me. I'll cry either way.")]),
    S('setBattleRule("fieldStage", 1 + [$game_variables[345], 4].min)'),
    IF('Prismfall.gym_battle(pfm_gym(:LEADER_JUNO), double: false)', [            # J3: LEADER_JUNO 30 + slot; :FLOWER_GARDEN; cap 47
        P('JUNO', 'crying', "I'm crying. I said I would.", '', JE),
        P('JUNO', 'happy', "...Take it. The Meadow badge is yours.", '', JE),
        S('Prismfall.award_badge(pfm_gym(:LEADER_JUNO))'),
        "You received the MEADOW BADGE!",
        S('9.times { |i| pbSEPlay("Anim/HealBell", 70, 62 + i * 8); pbWait(0.22) }\npfm_tone(30, 40, 10, 0, 20)'),   # nine notes; the light stays, softly
        P('JUNO', 'neutral', "It's singing. Mine never sang.", '', JE),
        N('Juno', "I wrote to Uncle Rowan after Briarwick, about your case doing a chord."),
        N('Juno', "He wrote back: \"That one'll sing in every gym in the realm, Juno, mark me.\""),
        N('Juno', "I didn't know what he meant."),
        P('JUNO', 'sad', "I still don't.", '', JE),
        S('pfm_fade_in(30)'),                                                        # like a pilot light, back to the room's light
        S('pbReceiveItem(:TM53)'),
        P('JUNO', 'neutral', "Energy Ball. It's the first move I ever taught anything.", '', JE),
        N('Juno', "And that badge means Pokémon up to level fifty-one will listen to you."),
        N('Juno', "I checked. Twice. I'm very nervous about getting the numbers wrong."),
        S('$game_variables[@@CH10_STEP] = 9 if $game_variables[@@CH10_STEP] < 9'),
        {'selfswitch': ['A', True]}], [S('pfm_set(:ch10_j3_lost)')])]
J3_AFTER = [P('JUNO', 'neutral', "Energy Ball. It's the first move I ever taught anything.", '', JE)]


def main():
    f261, f280, f281 = '261_ironreach_pc.yaml', '280_verdance.yaml', '281_verdance_interiors.yaml'
    f283, f284, f290 = '283_verdance_glasshouse_ward.yaml', '284_verdance_kingsgate_barbican.yaml', '290_verdance_gym.yaml'
    f293, f294 = '293_verdance_gym_293.yaml', '294_the_heartgarden.yaml'
    print('map 261: %d events' % SL.patch(f261, 261, events_261(), None, TAG))
    print('map 284: %d events' % SL.patch(f284, 284, events_284(), None, TAG))
    print('map 280: %d events' % SL.patch(f280, 280, events_280(), None, TAG))
    # the wave craft's two [TODO story] townsfolk get the script's lines (a paged event in the same spot, same look)
    npcs = {e.get('name'): e for e in spec_events(f280, 280)}
    for name, cmds in (('Flower seller', FLORIST), ('Rootward child', ROOTWARD_BOY)):
        e = npcs[name]
        look = (e['pages'][0].get('graphic') or {}) if e.get('type') == 'event' else {'sprite': e.get('sprite', 'NPC 05'), 'dir': e.get('dir', 'down')}
        mv = (e['pages'][0].get('move') if e.get('type') == 'event' else e.get('move')) or 'fixed'
        print('map 280: %s (%d)' % (name, SL.set_pages(f280, 280, name, [page(cmds, look.get('sprite', 'NPC 05'), look.get('dir', 'down'), move=mv)], TAG)))
    print('map 281: %d events' % SL.patch(f281, 281, events_281(), None, TAG))
    print('map 283: %d events' % SL.patch(f283, 283, events_283(), None, TAG))
    g290 = spec_events(f290, 290)
    guide = gem_page(g290, 'Gym Guide'); guide['commands'] = GUIDE
    print('map 290: %d events' % SL.patch(f290, 290, [], {'Gym Guide': [guide]}, TAG))
    print('map 293: %d events' % SL.patch(f293, 293, [], {
        JE: [page(J3, 'JUNO', 'down', cond=V(8)), page(J3_AFTER, 'JUNO', 'down', cond=V(8, self='A'))]}, TAG))
    print('map 294: %d events' % SL.patch(f294, 294, events_294(), pages_294(spec_events(f294, 294)), TAG))


if __name__ == '__main__':
    main()
