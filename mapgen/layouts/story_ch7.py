#!/usr/bin/env python3
"""story_ch7: the Chapter 7 story beats ("The Quiet Ward", story/26_SCRIPT_CH7.md) on Gemini's Mirefen maps
(mapgen/layouts/mirefen_town.py 220-223, mirefen_gym.py 230-233; commit efed7468). A STORY LAYER (storylayer.py): it
upserts its events by name into those specs and replaces the pages of a few of Gemini's events; the tiles, headers
and every other event stay as Gemini built them.

V127 CH7_STEP (design/FLAGS.md) on the built maps:
  1 -> (633 "Down", the Gutterfall lift: NOT BUILT; it sets 1)
  220 "Arrival (Mirefen)"    V127 >= 1, once: the establishing look over the stilt-town from the lift's foot
  223 "The Quiet Ward"       1 -> 2: Wenlow and his tray, the introductions bed by bed, Corvin at his ledger
  223 Juno Hale (talk)       2 -> 3: "R.A." -> J2 (RIVAL_JUNO v20 + slot, :CORROSIVE_MIRE, her ace line through
                             EBDX's lastOpp) -> :ch7_ledger (Prismfall::Choices.make via pf_choose: name_him JUNO-3 /
                             reassure JUNO+2 / ask_corvin, the ward scene with Corvin) -> S118 CH7_J2_DONE
  220 "Sweet Vendor (walkway)"  S118: Sweetrot offer 2 (the vendor walks up to you; Wenlow's panic at V128 >= 2)
  3 -> 4 (648 the Weeping Fen, Brother Wick: NOT BUILT; it sets S119 and 4)
  223 "Invoice"              V127 4, once: Corvin's bill (comedy scene Ch7; INVOICE through pfm_item)
  220 Sweet Vendor (Center Steps)  V127 >= 4: Sweetrot offer 3 (checkpoint, the GO_SWEET_TOOTH chain at V128 >= 2;
                             refused: Mother Gutter's one line from her barge). Repeats every visit (the missability note)
  220 the Gym door slate     V127 < 4: the Infirmary gym is shut (so J2 and Wick can't be skipped)
  230 Gym Guide / 233 Warden Corvin Mott   the script's words; Prismfall.gym_battle(pfm_gym(:LEADER_CORVIN),
                             double: true) (his ace line via lastOpp), the Remedy Badge, six notes, TM84, 4 -> 5
  220 "Ward Night (roof)"    V127 5, touch in front of the Infirmary door: night on the "roof" (the courtyard: 223 has
                             no roof; queued for Gemini), the lamp-screens, Sable's broadcast, the lights go out, the
                             chime, Wenlow -> 223
  223 "The Ward Night (Veil)" the Veil across the Quiet Ward door (mapgen/ruby/021_QuietWard.rb draws it), Corvin's
                             burned hand, Juno and the stills, the walk in, Ama's moving eyes (a drawn close-up), out
                             through the Veil, the stills take, the Veil sinks, Old Fen winks -> 220
  220 "Ward Night (after)"   the roof again: "They're not dying. They're dreaming." Juno, the second INVOICE, 5 -> 6
  220 "Chapter 7 close"      6 -> 7: morning, the hammered rings and the Hollow's chalk, the woman, the ferryman,
                             Wenlow waving at the lift, the quest log, V102 STORY_CHAPTER = 8 (the Ch8 card follows)
The Ward Night's three parts hand over through pfm flag :ch7_ward_night (1 = into the ward, 2 = back on the roof,
3 = done); an autorun whose part is not due erases itself for the visit.

Not here: 632 / 621 / 630 / 634 / 633 / 648 / 644-645 (not built: mapgen/REFINE_QUEUE.md lists what each needs);
Gemini's Trials hooks (pf_trial_*), the Gutter Book board, the ferryman's Surf (mirefen_town.py has them).

Run after mirefen_town.py / mirefen_gym.py (they rewrite these specs from scratch):
    python3 -I layouts/story_ch7.py && python3 -I build.py 220 223 230 233 --no-preview"""
import copy, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from story_early import P, N, S, IF, CH, MV, page, ev
import story_early as SE
import storylayer as SL
import yaml

TAG = 'ch7'
STEP = 'CH7_STEP'
SWEET = '@@SWEETROT_TAKEN'
SE.NAMES.update({'CORVIN': 'Corvin', 'WENLOW': 'Wenlow', 'SABLE': 'Sable', 'GUTTER': 'Mother Gutter', 'JUNO': 'Juno'})
FILES = {220: '220_mirefen.yaml', 223: '223_corvin_infirmary.yaml', 230: '230_mirefen_gym.yaml', 233: '233_mirefen_gym_233.yaml'}
NIGHT = 'pfm_tone(-56, -46, -8, 50, %d)'           # night over the blue-glowing marsh
DARK = 'pfm_tone(-96, -92, -50, 100, %d)'           # the Infirmary's lamps out


def V(n, **kw): return dict({'var': [STEP, n]}, **kw)
def at(e, x, y): e['at'] = [x, y]; return e
def show(sheet, d=8): return [{'graphic': [sheet, 0, d, 0]}, {'opacity': 255}]
def hide(): return [{'opacity': 0}]
def walk_on(name, x, y):
    """an actor with no look of its own: a scene's move route gives it one (and takes it away)"""
    return at(ev(name, page([], through=True)), x, y)
def ghost(name, x, y, sheet, d='down'):
    """an actor with a look but opacity 0 until a scene fades it in (pfm_approach / pfm_appear)"""
    e = at(ev(name, page([], sheet, d, through=True)), x, y)
    e['pages'][0]['graphic']['opacity'] = 0
    return e
def moveto(who, x, y, face):
    return MV(who, [{'script': 'moveto(%d, %d)' % (x, y)}, 'turn_' + face])
def ebdx_ace(line):
    """the ace's line (the script's "when her/his ace enters"): EBDX's lastOpp speech, when EBDX is installed"""
    return S('EliteBattle.set(:nextBattleScript, { "lastOpp" => "%s" }) if defined?(EliteBattle)' % line.replace('"', '\\"'))
def taste(n):
    """the Sweetrot: a heart, the peach-pink wash; then it goes and you want another (a greyer drain, the dots)"""
    return [S('$game_variables[%s] += 1' % SWEET), S('pf_emote(:player, :heart)\npfm_sweetrot(%d)' % n),
            S('pf_emote(:player, :dots, wait: true)')]
def chime(n=1, vol=60, pitch=70):
    return S('%d.times { |i| pbSEPlay("Ring Glass Harmonic", %d + i * 15, %d + i * 12); pbWait(0.6) }' % (n, vol, pitch))


# ============================================================================================ 220 arrival
ARRIVAL = [   # (Stilt-houses over a marsh, walkways, cranes on the roofs; graffiti; brown water glowing blue at the edges)
    {'wait': 20},
    {'raw': [203, [2, 9, 3]]},                                                      # the camera goes down over the town
    S('3.times { pbSEPlay("Anim/Bubble1", 45, 70); pbWait(0.5) }'),               # the drips off the city on the lid
    {'raw': [203, [6, 8, 3]]}, {'wait': 30},                                        # to the Ogre in his sad mask
    S('pfm_glow(-10, 20, 60, 24, 16)'),                                             # the water's faint blue at the edges
    S('pfm_pan_home(30)'),
    {'selfswitch': ['A', True]}]

# ============================================================================================ 220 the Sweet Market
OFFER1 = [
    MV('Sweetrot Vendor', ['face_player']),
    S('pbSEPlay("Sweet Scent", 45, 120)'), {'wait': 16},                           # peaches, and something under them
    N('Sweet Vendor', "Sweetrot! Try one. First one's free."),
    N('Sweet Vendor', "First one's always free, sweetling."),
    CH(['Take one.', 'No, thank you.'], [
        taste(1),
        [N('Sweet Vendor', "Next time. There's always a next time, down here.")]], cancel=2),
    MV('Singing Child', ['turn_right']), S('pf_emote("Singing Child", :music)'),
    N('Child', "♪ One for the sweet and two for the tongue,"),
    N('Child', "the peach that keeps you, keeps you young... ♪"),
    {'selfswitch': ['A', True]}]
VENDOR1_AFTER = [MV('Sweetrot Vendor', ['face_player']),
                 IF('$game_variables[%s] >= 1' % SWEET, [N('Sweet Vendor', "First one's always free, sweetling.")],
                    [N('Sweet Vendor', "Next time. There's always a next time, down here.")])]

OFFER2 = [   # after J2: the vendor walks up the walkway to you
    S('pfm_approach("Sweet Vendor (walkway)", 3, 1)'),
    N('Sweet Vendor', "You look like you've had a day."),
    N('Sweet Vendor', "Here. This one's half price. Because I like you."),
    CH(['Take one.', 'No.'], [
        taste(2) + [IF('$game_variables[%s] >= 2' % SWEET, [
            S('pfm_approach("Wenlow (walkway)", 4, 3)'),                                 # from the walkway above
            P('WENLOW', 'panic', "NO. No no no. That's two. Please. That's two.", 'sweat', 'Wenlow (walkway)'),
            MV('Wenlow (walkway)', ['through_on', 'away_player', 'away_player', {'opacity': 0}], wait=False)])],
        [{'wait': 24},                                                                      # smiling the same smile
         N('Sweet Vendor', "Third time's the charm, sweetling.")]], cancel=2),
    MV('Sweet Vendor (walkway)', ['through_on', 'away_player', 'away_player', 'away_player', {'opacity': 0}]),
    {'selfswitch': ['A', True]}]

GUTTER_BARGE = [   # a vast shape on a barge passing under the walkway, a Muk the size of a cart asleep beside her
    MV('Mother Gutter', [{'opacity': 255}, 'turn_right'], wait=False), MV('Muk (barge)', [{'opacity': 255}, 'step_anime_on']),
    MV('Mother Gutter', [{'speed': 2}, 'down'], wait=False), MV('Muk (barge)', [{'speed': 2}, 'down']),
    P('GUTTER', 'happy', "No she won't, dear. She's patient. Peaches are patient.", '', 'Mother Gutter'),
    MV('Mother Gutter', ['down', 'down', {'opacity': 0}], wait=False), MV('Muk (barge)', ['down', 'down', {'opacity': 0}])]
REFUSE3 = [N('Sweet Vendor', "Mother Gutter will be so disappointed.")] + GUTTER_BARGE
OFFER3 = [   # outside the Mirefen Pokemon Center, the evening before the gym; repeats every visit (missability)
    IF('$game_variables[%s] >= 2' % SWEET, [S('Prismfall.checkpoint')]),              # GO_SWEET_TOOTH's checkpoint
    MV('Sweet Vendor (Center Steps)', ['face_player']),
    S('pbSEPlay("GUI storage pick up", 60, 110)'), {'wait': 12},                    # a little paper box tied with ribbon
    N('Sweet Vendor', "I saved you the best one. The pink."),
    N('Sweet Vendor', "Nobody else gets the pink."),
    IF('$game_variables[%s] >= 2' % SWEET, [
        CH(['Take it.', 'No.'], [
            ["...Really?",
             CH(['Take it.', 'No.'], [
                 [S('$game_variables[%s] += 1' % SWEET),
                  # Peaches. And then nothing is ever wrong again, and you never wonder why again
                  S('pf_emote(:player, :heart)\npfm_tone(110, 50, 80, 0, 50)'), {'wait': 40},
                  S('pfm_tone(255, 220, 230, 0, 60)'),
                  S('Prismfall.game_over(:GO_SWEET_TOOTH)')],
                 REFUSE3], cancel=2)],
            REFUSE3], cancel=2)],
       [CH(['Take it.', 'No.'], [taste(1), REFUSE3], cancel=2)])]

# ============================================================================================ 220 the Ward Night, roof
ROOF1 = [
    IF('pfm_get(:ch7_ward_night).to_i == 0', [
        S('pfm_fade_out(16)'),
        moveto('player', 32, 13, 'right'),
        MV('Corvin (roof)', show('CORVIN', 4) + [{'script': 'moveto(33, 13)'}]),    # mask off, two tin mugs, a lamp
        S(NIGHT % 40),
        P('CORVIN', 'neutral', "Sit. It's bog coffee. It tastes exactly like it sounds.", '', 'Corvin (roof)'),
        N('Corvin', "I haven't slept properly since AF 288. You get used to it."),
        N('Corvin', "You don't, actually. You get used to saying you've got used to it."),
        S('pfm_screens(3)'), {'wait': 10},                                             # every lamp-screen flickers
        S('pbSEPlay("Glitch Tear Static", 60, 70)'), {'wait': 16},                    # static, then a half-masked face
        P('SABLE', 'happy', "Evening, Nadir!"),
        N('Sable', "The Mourner's gone soft. You can tell; he's stopped turning up."),
        N('Sable', "He wants to \"carry them home\". Bless."),
        N('Sable', "The Hammer hasn't gone soft. The Hammer doesn't carry things."),
        N('Sable', "The Hammer breaks them, until somebody up there listens."),
        N('Sable', "Cindervault's next. Light for everyone, right?"),
        N('Sable', "Let's start with you."),
        S('pbSEPlay("PC close", 90, 50)\n' + DARK % 4), {'wait': 24},                 # the Infirmary's lamps go out
        chime(3, 45, 64),                                                              # a wet finger on a glass, louder
        MV('Corvin (roof)', ['turn_up']),
        P('CORVIN', 'shocked', "The dampers.", 'jolt', 'Corvin (roof)'),
        N('Corvin', "The ward's dampers run on Zenith current off the Gutterfall junction."),
        N('Corvin', "Somebody's CUT the junction—"),
        S('pbSEPlay("Door exit")'),                                                    # Wenlow bursts out, white
        MV('Wenlow (roof)', show('WENLOW', 2) + [{'script': 'moveto(31, 11)'}, 'through_on', {'speed': 5}, 'down', 'turn_right', 'through_off']),
        P('WENLOW', 'panic', "Doctor! Doctor, the ward, the Bleed's coming up off the beds, it's — it's a Veil, Doctor, it's a Veil across the door, I can't get IN—", '', 'Wenlow (roof)'),
        MV('Corvin (roof)', ['through_on', {'speed': 5}, 'left', 'up', 'left', 'up', {'opacity': 0}], wait=False),
        MV('Wenlow (roof)', ['through_on', {'speed': 5}, 'up', {'opacity': 0}]),
        S('pfm_set(:ch7_ward_night, 1)'),
        S('pfm_fade_out(14)'),
        {'transfer': {'map': 223, 'x': 13, 'y': 11, 'dir': 'up'}}])]

# ============================================================================================ 223 the Ward Night, the Veil
VEIL = [
    S('pfm_set(:ch7_ward_night, 2)'),
    MV('Juno Hale', hide() + ['through_on'], wait=False), MV('Wenlow', hide() + ['through_on'], wait=False),
    moveto('Corvin Mott', 12, 9, 'up'),
    moveto('player', 13, 11, 'up'),
    MV('Wenlow (night)', show('WENLOW', 8) + [{'script': 'moveto(14, 11)'}]),
    S('pfm_veil(11, 8, 3, 1, 1)'),                                                     # across the door: heat over a road
    S(DARK % 30),
    chime(2, 60, 58),
    {'raw': [203, [8, 4, 2]]},                                                          # behind it, the ward in grey
    S('pbSEPlay("Anim/Ice1", 60, 70)'), {'wait': 20},                                 # Old Fen's glass, climbing
    {'wait': 24},                                                                       # Mister Garrod has stopped humming
    S('pfm_pan_home(24)'),
    # Corvin puts his hand to the Veil and snatches it back, burned
    MV('Corvin Mott', [{'speed': 4}, 'turn_up', 'wait 10']),
    S('pbSEPlay("Anim/Fire1", 70, 120)\npfm_shake(1, 20, 4)'),
    MV('Corvin Mott', ['dir_fix_on', 'backward', 'dir_fix_off']),
    # Juno arrives at a run with a lamp, sees it, and stops
    MV('Juno (night)', show('JUNO', 8) + ['through_on', {'speed': 5}, 'up', 'up', 'up', 'up', 'up', 'left', 'up', 'turn_up', 'through_off']),
    P('JUNO', 'shocked', "It's the same. It's the Lowlight. It's the—", '', 'Juno (night)'),
    S('pfm_face("Corvin Mott", "Juno (night)")'),
    P('CORVIN', 'neutral', "The dampers hold the ward's Bleed down.", '', 'Corvin Mott'),
    N('Corvin', "Without them it goes up like this, and in an hour every patient on that floor is stage four."),
    N('Corvin', "Stage four doesn't come back."),
    N('Corvin', "The stills. Juno. The seed-medicine stills run on peat, not current."),
    N('Corvin', "If we can get the stills to the damper coils, the medicine might hold them — might—"),
    P('JUNO', 'neutral', "I'll do it. I know where the stills are.", '', 'Juno (night)'),
    N('Juno', "I've been sorting this building for a week."),
    MV('Juno (night)', ['through_on', {'speed': 5}, 'down', 'right', 'down', 'down', 'down', 'down', 'down', {'opacity': 0}], wait=False),
    MV('Wenlow (night)', ['through_on', {'speed': 5}, 'wait 6', 'down', 'left', 'left', 'down', 'down', 'down', 'down', 'down', {'opacity': 0}]),
    S('pfm_face("Corvin Mott", :player)'), S('pfm_face(:player, "Corvin Mott")'), {'wait': 20},
    N('Corvin', "I've heard about you. The Lowlight. You walked in."),
    P('CORVIN', 'sad', "The child nearest the window. Ama.", '', 'Corvin Mott'),
    N('Corvin', "She's the furthest along and she's the smallest."),
    N('Corvin', "If anyone goes past three tonight, it's her."),
    N('Corvin', "I'm a doctor. I can't ask you to walk into that."),
    N('Corvin', "So I'm not asking."),
    # You walk in. The chime is everywhere; the light is grey and comes from every direction.
    MV('player', ['through_on', 'up', 'up', 'up', 'up', 'up']),
    S('pfm_tone(-70, -70, -60, 230, 16)'), chime(1, 85, 52),
    {'wait': 30}, S('pbSEPlay("Anim/Saint7", 45, 40)'), {'wait': 40},                 # under your ribs, something very still
    MV('player', ['left'] * 10 + ['up', 'turn_up', 'through_off']),                     # Ama's bed by the window
    S('pbSEPlay("Anim/Ice1", 55, 60)'), {'wait': 24},                                 # the salt turning clear
    # You lift her: too light for nine, heavy and cold as stone where the salt has her; glass and salt crackle
    S('pfm_fade_out(12)'), S('pbSEPlay("Anim/Ice5", 70, 70)'), {'wait': 16},
    moveto('player', 12, 7, 'down'), S(DARK % 1), S('pfm_tone(-70, -70, -60, 230, 16)'),
    # at the Veil's edge, with Ama in your arms, you look down: under the clear salt, her eyes are moving
    S('pfm_dreaming_eyes(3.4)'),
    {'wait': 60},                                                                       # WAIT 60.
    MV('player', ['through_on', 'down', 'down', 'through_off', 'turn_down']),          # out through the Veil
    MV('Ama', [{'graphic': ['NPC 29', 0, 2, 0]}, {'opacity': 255}]),                    # he takes her
    MV('Corvin Mott', ['turn_left']),
    S(DARK % 10),
    P('CORVIN', 'shocked', "...", '', 'Corvin Mott'),
    S('pfm_tone(-40, -58, -96, 70, 16)'), {'wait': 50}, S(DARK % 16),               # the lamp to her face, a long time
    S('pfm_face("Corvin Mott", :player)'),
    N('Corvin', "You saw that. Tell me you saw that."),
    S('pbSEPlay("Mining hammer", 80, 60)\npbWait(0.35)\npbSEPlay("Anim/Smokescreen", 70, 90)'),   # iron, steam: the chime falters
    P('JUNO', 'neutral', "The stills are on the coils!"),                               # from the stairwell, shouting
    N('Juno', "It's — it's taking! Is it taking?"),
    S('pfm_veil_off(70)'),                                                              # thins, wavers, sinks like mist
    S(DARK % 30),
    S('pbSEPlay("Anim/Saint1", 30, 60)\npf_emote("Ward bed 2 (Mister Garrod), size(2,2)", :music)'),   # the same tune
    {'wait': 30},                                                                       # Old Fen's glass has stopped
    MV('Wenlow (night)', show('WENLOW', 8) + [{'script': 'moveto(12, 12)'}, 'through_on', {'speed': 5},
                                              'right', 'up', 'up', 'up', 'up', 'up', 'up', 'right', 'right', 'right', 'up', 'turn_up', 'through_off']),
    P('WENLOW', 'crying', "Old Fen? Old Fen, can you hear me?", '', 'Wenlow (night)'),
    {'wait': 40},
    N('Wenlow', "...He winked. Doctor, he WINKED."),
    S('pfm_set(:ch7_ward_night, 2)'),
    S('pfm_fade_out(30)'),
    {'transfer': {'map': 220, 'x': 32, 'y': 13, 'dir': 'right'}}]

# ============================================================================================ 220 the roof, later
ROOF2 = [
    moveto('player', 32, 13, 'right'),
    MV('Corvin (roof)', show('CORVIN', 4) + [{'script': 'moveto(33, 13)'}]),
    S(NIGHT % 40),                                                                       # later; the coffee is cold
    {'wait': 20},
    P('CORVIN', 'sad', "Do you know why nobody in my Ward is dead?", '', 'Corvin (roof)'),
    N('Corvin', "They're not dying. They're dreaming."),
    N('Corvin', "I've watched their eyes move under the glass for twelve years, and I've never said it out loud, because a doctor who says \"dreaming\" about a stage-three Fixing gets laughed out of the Accord's medical college."),
    N('Corvin', "You saw it too. So now there's two of us. Two's a study."),
    N('Corvin', "Somebody should find out what they're dreaming about."),
    # Juno sits down on the roof's edge next to you, soot on her face, blossoms singed
    S('pbSEPlay("Door exit")'),
    MV('Juno (roof)', show('JUNO', 2) + [{'script': 'moveto(31, 11)'}, 'through_on', 'down', 'down', 'turn_right', 'through_off']),
    P('JUNO', 'sad', "The Hammer did this. Sable did this. On purpose. To a ward full of people who can't run.", '', 'Juno (roof)'),
    N('Juno', "The man in the mask, in Saltmere. He never hurt anyone."),
    N('Juno', "He said \"let the land grieve\". He sounded sad."),
    P('JUNO', 'angry', "She doesn't sound sad. She sounds like she's enjoying it.", '', 'Juno (roof)'),
    P('CORVIN', 'deadpan', "That's how you tell them apart, in my experience.", '', 'Corvin (roof)'),
    N('Corvin', "The ones who are enjoying it."),
    S('pfm_item(:INVOICE, 1, "Invoice")'),
    'INVOICE: "Item: one (1) ward, carried. Item: one (1) child, carried. Item: the look on my face. TOTAL: ₽0."',
    {'var': [STEP, 6]},
    S('pfm_set(:ch7_ward_night, 3)'),
    S('pfm_fade_out(30)'),
    MV('Corvin (roof)', hide(), wait=False), MV('Juno (roof)', hide()),
    moveto('player', 16, 8, 'down')]

# ============================================================================================ 220 chapter close
CLOSE = [
    S('pfm_tone(-12, -12, -6, 90, 40)'),                                                 # morning; the marsh grey again
    {'raw': [203, [2, 6, 4]]}, {'raw': [203, [6, 8, 4]]},                                # to the walls
    S('2.times { pbSEPlay("Mining hammer", 70, 80); pbWait(0.4) }'),                     # every ring hammered over
    'Chalked under a hammered ring: "NOT OURS. — the Hollow".',
    S('pfm_pan_home(30)'),
    MV('Mirefen Woman (morning)', show('NPC 12', 4) + [{'script': 'moveto(13, 9)'}, 'right', 'turn_right']),
    N('Mirefen Woman', "The Hammer did the ward. The Hollow did the chalk."),
    N('Mirefen Woman', "I didn't know there were two kinds. Now there's two kinds."),
    MV('Ferryman (morning)', show('trainer_SAILOR', 8) + [{'script': 'moveto(16, 11)'}, 'up', 'up', 'turn_up']),
    N('Ferryman', "Surf's yours, if the Doctor says so."),
    N('Ferryman', "Lake Sallow's east, past Leechman's Walk. Then up into Ashkaar."),
    N('Ferryman', "Mind the sulfur. Mind the dragons. Mind everything."),
    MV('Mirefen Woman (morning)', ['left', 'left', 'down', {'opacity': 0}], wait=False),
    MV('Ferryman (morning)', ['down', 'down', 'down', {'opacity': 0}], wait=False),
    MV('player', ['turn_up']),
    MV('Wenlow (lift)', show('WENLOW', 2) + [{'script': 'moveto(16, 6)'}, 'step_anime_on'] + ['turn_left', 'wait 4', 'turn_right', 'wait 4'] * 3 + ['turn_down']),
    P('WENLOW', 'happy', "Come back! Bring Juno! Bring snacks! Bring weather!", '', 'Wenlow (lift)'),
    S('if !pfm_quest(:eighteen_roads, "Eighteen Roads", "Earn the seventh badge in Cindervault, across Lake Sallow into Ashkaar.")\n'
      '  $PokemonGlobal.pf_quests[:eighteen_roads][:text] = "Earn the seventh badge in Cindervault, across Lake Sallow into Ashkaar."\n'
      '  pbMessage("\\\\se[GUI save choice]" + _INTL("QUEST LOG: \\"Eighteen Roads\\" — Earn the seventh badge in Cindervault, across Lake Sallow into Ashkaar."))\n'
      'end'),
    {'var': [STEP, 7]}, {'var': ['STORY_CHAPTER', 8]}]


def events_220():
    return [
        at(ev('Arrival (Mirefen)', page([]), page(ARRIVAL, cond=V(1), trigger='autorun'), page([], cond={'self': 'A'}),
              page([], cond=V(2))), 0, 0),
        # offer 2: the vendor walks up the walkway to you, once J2 is done
        at(ev('Offer 2 (walkway)', page([]), page(OFFER2, cond={'switch': 'CH7_J2_DONE'}, trigger='autorun'),
              page([], cond={'self': 'A'})), 1, 0),
        ghost('Sweet Vendor (walkway)', 28, 18, 'NPC 21', 'up'),
        ghost('Wenlow (walkway)', 28, 17, 'WENLOW', 'up'),
        ghost('Muk (barge)', 5, 20, 'Followers/MUK', 'right'),
        # the Gym's door is shut until Wick (V127 4): J2 and the Fen can't be skipped by winning the badge first
        at(ev('Gym door slate', page([IF('$game_variables[@@CH7_STEP] < 4', [
            S('pbSEPlay("Player bump", 80, 80)'),
            'A slate hangs on the Gym door, chalked in an impatient hand: "ON ROUNDS. — C. MOTT."',
            MV('player', ['dir_fix_on', 'backward', 'dir_fix_off'])])], trigger='touch', through=True),
            page([], cond=V(4), through=True)), 37, 30),
        # the Ward Night: in front of the Infirmary door, the first time back after Gym 6
        at(ev('Ward Night (roof)', page([], through=True), page(ROOF1, cond=V(5), trigger='touch', through=True),
              page([], cond=V(6), through=True)), 31, 12),
        at(ev('Ward Night (after)', page([]), page([IF('pfm_get(:ch7_ward_night).to_i == 2', ROOF2, [{'erase': True}])],
                                                    cond=V(5), trigger='autorun'), page([], cond=V(6))), 2, 0),
        walk_on('Corvin (roof)', 33, 13), walk_on('Wenlow (roof)', 33, 12), walk_on('Juno (roof)', 32, 12),
        at(ev('Chapter 7 close', page([]), page(CLOSE, cond=V(6), trigger='autorun'), page([], cond=V(7))), 3, 0),
        walk_on('Mirefen Woman (morning)', 13, 9), walk_on('Ferryman (morning)', 16, 11), walk_on('Wenlow (lift)', 16, 6),
    ]


def pages_220(spec):
    """Gemini's events on 220 whose pages this layer replaces (set_pages): the two Sweetrot vendors, Mother Gutter"""
    g = {e['name']: e for e in spec['events']}
    gr = lambda n: (g[n]['pages'][0].get('graphic') or {}) if g.get(n, {}).get('pages') else {}
    v1, v3, mg = gr('Sweetrot Vendor'), gr('Sweet Vendor (Center Steps)'), gr('Mother Gutter')
    return {
        'Sweetrot Vendor': [page(OFFER1, v1.get('sprite', 'NPC 21'), v1.get('dir', 'down')),
                            page(VENDOR1_AFTER, v1.get('sprite', 'NPC 21'), v1.get('dir', 'down'), cond={'self': 'A'})],
        'Sweet Vendor (Center Steps)': [page([]), page(OFFER3, v3.get('sprite', 'NPC 23'), v3.get('dir', 'left'), cond=V(4))],
        # canon: Mother Gutter has ONE line in Ch7, from her barge after offer 3 is refused (she returns in Act IV)
        'Mother Gutter': [dict(page([], mg.get('sprite', 'GUTTER'), mg.get('dir', 'right'), through=True))],
    }


# ============================================================================================ 223 the Quiet Ward
WARD_LEFT = ['left'] * 6
QUIET_WARD = [
    MV('player', ['up', 'up', 'up']),                                                     # in, past the front ward
    MV('Wenlow', ['right', 'right', 'turn_down']),                                        # round a screen with a tray
    MV('Wenlow', [{'jump': [0, 0]}], wait=False), S('pbSEPlay("Anim/Crash", 50, 140)'),  # nearly drops all of it
    P('WENLOW', 'happy', "Oh! Visitors! Hello!", 'exclaim', 'Wenlow'),
    N('Wenlow', "I'm Wenlow, I'm the apprentice, mind the tray, mind the — there. Saved it."),
    N('Wenlow', "You're Juno's friend, aren't you? She said you'd come."),
    N('Wenlow', "She said you'd come and stand in a doorway looking serious."),
    N('Wenlow', "You're doing it now!"),
    IF('$game_variables[%s] >= 1' % SWEET, [
        P('WENLOW', 'panic', "Oh — oh no, you've had a Sweetrot. I can smell it. Peaches.", 'sweat', 'Wenlow'),
        N('Wenlow', "Don't have another one. Please. Don't have another one."),
        N('Wenlow', "We've a whole ward of people who had another one.")]),
    P('WENLOW', 'happy', "Doctor's in the Quiet Ward. Come up. You can meet everyone.", '', 'Wenlow'),
    N('Wenlow', "I'll introduce you. I always introduce people. It's polite."),
    S('pbBGMFade(1.5)'),                                                                  # the top floor, quiet as snow
    MV('Corvin Mott', ['turn_up'], wait=False),                                           # writing; he doesn't look up
    MV('Wenlow', ['through_on', {'speed': 4}] + ['up'] * 7 + WARD_LEFT + ['up', 'turn_up', 'through_off'], wait=False),
    MV('player', ['wait 12'] + ['up'] * 8),
    S('pfm_tone(-12, -8, 6, 40, 30)'),
    S('pfm_face(:player, "Wenlow")'),
    P('WENLOW', 'neutral', "This is Mister Garrod. He hums. We don't know the tune.", '', 'Wenlow'),
    S('pf_emote("Ward bed 2 (Mister Garrod), size(2,2)", :music)'),
    N('Wenlow', "If you know it, tell us; he'd like that."),
    MV('Wenlow', ['through_on', 'down'] + ['right'] * 10 + ['up', 'turn_up', 'through_off']), S('pfm_face(:player, "Wenlow")'),
    N('Wenlow', "That's Old Fen. Glass to the elbow on the left."),
    N('Wenlow', "Plays cards with his right. He cheats. We let him."),
    MV('Wenlow', ['through_on', 'down', 'right', 'right', 'right', 'turn_right', 'through_off']), S('pfm_face(:player, "Wenlow")'),
    N('Wenlow', "And the Tull twins, both at stage two, in the beds together because they cried when we split them up."),
    MV('Wenlow', ['through_on', {'speed': 5}] + ['left'] * 16 + ['up', 'turn_up', 'through_off']), S('pfm_face(:player, "Wenlow")'),
    N('Wenlow', "And this is Ama. She's nine."),
    S('pbSEPlay("Anim/Ice1", 35, 120)\npfm_tone(14, 22, 40, 20, 12)'), {'wait': 14}, S('pfm_tone(-12, -8, 6, 40, 16)'),   # salt hair catching the lamp
    P('WENLOW', 'happy', "She likes being told about the weather up top.", '', 'Wenlow'),
    N('Wenlow', "I tell her every morning. I make some of it up."),
    S('pfm_face(:player, "Corvin Mott")'), {'wait': 24},                                 # at the end of the ward, writing
    P('CORVIN', 'deadpan', "Wenlow, you've introduced them to every patient on the floor, haven't you.", '', 'Corvin Mott'),
    P('WENLOW', 'happy', "Yes, Doctor!", '', 'Wenlow'),
    N('Corvin', "Good. Somebody should."),
    MV('Corvin Mott', ['turn_down']),
    N('Corvin', "Corvin Mott. Warden, doctor, and the reason the Sump Barons don't sleep well."),
    N('Corvin', "The mask's for the smell, mostly."),
    N('Corvin', "I've a ward of forty patients slowly turning into garden furniture. Forgive me if I don't stand for the Sovereign's anthem."),
    N('Corvin', "Your friend's in the dispensary, doing something devastatingly cheerful to my filing."),
    N('Corvin', "Go and stop her. Or don't."),
    N('Corvin', "She found a ledger I'd lost in AF 296."),
    S('$game_map.autoplay'), S('pfm_fade_in(20)'),
    {'var': [STEP, 2]}]

# ============================================================================================ 223 "R.A." -> J2 -> :ch7_ledger
CORVIN_IN = ['through_on', {'speed': 6}] + ['down'] * 9 + ['right'] * 6 + ['turn_right']
CORVIN_OUT = ['left'] * 6 + ['up'] * 9 + ['turn_down', 'through_off']
LEDGER = [
    S('pfm_fade_out(8)'), moveto('player', 19, 14, 'up'), MV('Juno Hale', ['turn_down']), S('pfm_fade_in(10)'),
    P('JUNO', 'happy', "You came! You brought — you didn't bring snacks.", '', 'Juno Hale'),
    N('Juno', "That's fine. I've had noodles. Three out of ten, he gave me."),
    N('Juno', "He said I talked to the bowl."),
    N('Juno', "Dr Mott keeps every patient in these."),
    N('Juno', "Every burn, every Fixing, every Sweetrot. In no order at ALL."),
    N('Juno', "I'm putting them in order. He hates it. He hasn't stopped me."),
    N('Juno', "This one's this spring. The Shatter. The night of the gala."),
    N('Juno', "He was up all night, look, nineteen people—"),
    MV('Juno Hale', ['turn_up']), S('pbSEPlay("GUI storage put down", 50, 140)'), {'wait': 40},   # a page turns; she stops
    P('JUNO', 'neutral', "\"R.A. Second-degree Bleed-burn, right palm and fingers. Lightning pattern. Discretion.\"", '', 'Juno Hale'),
    P('JUNO', 'neutral', "...", 'dots', 'Juno Hale'),
    MV('Corvin Mott', CORVIN_IN),                                                          # in from the ward, three strides
    S('pbSEPlay("GUI storage pick up", 70, 80)'), {'wait': 10},                          # takes it out of her hands; closes it
    P('CORVIN', 'neutral', "That one's not filed yet. My handwriting. You'd never read it.", '', 'Corvin Mott'),
    MV('Corvin Mott', CORVIN_OUT, wait=False),                                            # back to the ward, ledger under his arm
    {'wait': 50},
    MV('Juno Hale', ['turn_down']),
    P('JUNO', 'happy', "R.A.! There's loads of R.A.s.", 'sweat', 'Juno Hale'),             # too brightly
    N('Juno', "Roberta Ash. Rufus... Ardley."),
    N('Juno', "There's a man on the stilt-walk called Ras."),
    N('Juno', "Right palm. Lightning."),
    P('JUNO', 'angry', "Fight me. On the stilt-walk. Now.", '', 'Juno Hale'),
    N('Juno', "I need to hit something that isn't a thought.")]

NAME_HIM = [
    S('pf_choose(:ch7_ledger, :name_him)'),
    P('JUNO', 'angry', "Don't. Don't you DARE say his name like it's an answer.", '', 'Juno Hale'),
    N('Juno', "You don't know him."),
    N('Juno', "You met him for ten minutes in a station with a sick Phantump."),
    N('Juno', "You don't KNOW him."),
    MV('Juno Hale', ['through_on', {'speed': 5}, 'left', 'down'] + ['left'] * 6 + ['down', 'down', 'down', {'opacity': 0}]),   # she doesn't look back
    S('pfm_vanish("Juno Hale", 1)')]
REASSURE = [
    S('pf_choose(:ch7_ledger, :reassure)'),
    P('JUNO', 'angry', "...There are. Aren't there. There are loads.", '', 'Juno Hale'),
    P('JUNO', 'happy', "Thank you. I'm being silly. I said in my letter, I'm being silly.", '', 'Juno Hale'),
    N('Juno', "I just needed somebody else to say it."),
    MV('player', [{'jump': [0, 0]}], wait=False), MV('Juno Hale', [{'jump': [0, 0]}]),    # a hug, too hard
    {'wait': 20}, MV('Juno Hale', ['turn_up'])]                                           # back to the ledgers; not that one
ASK_CORVIN = [
    S('pf_choose(:ch7_ledger, :ask_corvin)'),
    P('JUNO', 'happy', "...Yes. Ask him. You ask him. I can't.", '', 'Juno Hale'),
    S('pfm_fade_out(20)'),                                                                 # later: the ward, Old Fen's good hand
    moveto('Corvin Mott', 16, 5, 'up'), moveto('player', 15, 5, 'right'), S('pfm_fade_in(20)'),
    S('pbSEPlay("GUI storage pick up", 40, 120)'), {'wait': 20},
    S('pfm_face("Corvin Mott", :player)'),
    P('CORVIN', 'neutral', "I'm a doctor. I treat hands. I don't ask whose.", '', 'Corvin Mott'),
    N('Corvin', "And I'd thank you not to ask me twice, because the second time I might tell you, and then it'd be yours to carry. Not mine."),
    S('pfm_fade_out(20)'),                                                                 # back in the dispensary
    moveto('Corvin Mott', 12, 4, 'down'), moveto('player', 19, 14, 'up'), MV('Juno Hale', ['turn_down']), S('pfm_fade_in(20)'),
    P('JUNO', 'sad', "...He wouldn't say. I can tell. Good. He's a good doctor.", '', 'Juno Hale'),
    MV('Juno Hale', ['turn_up']), S('pbSEPlay("GUI storage put down", 30, 90)'),          # closing the ledger very gently
    N('Juno', "I'm going to stop reading these now.")]
J2_WIN = [
    P('JUNO', 'sad', "...", '', 'Juno Hale'),
    N('Juno', "He burned his hand on the kettle. That's what he wrote."),
    N('Juno', "The right one. The same night."),
    N('Juno', "He's never burned himself on anything in his life."),
    N('Juno', "He picks up hot pots with his bare hands."),
    N('Juno', "Aunt Elin used to shout at him for it."),
    P('JUNO', 'crying', "Say it isn't. Say something.", '', 'Juno Hale'),
    CH(['"Rowan Ashby."', '"There\'s loads of R.A.s."', 'Ask Corvin. Later, alone.'], [NAME_HIM, REASSURE, ASK_CORVIN], cancel=0),
    {'switch': ['CH7_J2_DONE', True]}, {'var': [STEP, 3]}]
RA = [
    IF('pfm_get(:ch7_j2_tried)', [P('JUNO', 'angry', "Again. Please. I'm not done not thinking.", '', 'Juno Hale')], LEDGER),
    S('pfm_set(:ch7_j2_tried)'), ebdx_ace("He wouldn't. He WOULDN'T."),
    IF('Prismfall.rival_battle(:RIVAL_JUNO, "Juno", 2, field: :CORROSIVE_MIRE)', J2_WIN)]
JUNO_TALK = [IF('$game_variables[@@CH7_STEP] == 2', RA, [
    IF('$game_variables[@@CH7_STEP] >= 3', [N('Juno', "I'm putting them in order. He hates it. He hasn't stopped me.")], [
        N('Juno', "Dr Mott keeps every patient in these."),
        N('Juno', "Every burn, every Fixing, every Sweetrot. In no order at ALL.")])])]

# ============================================================================================ 223 "Invoice" (back from the Fen)
INVOICE = [
    S('pfm_fade_out(10)'),
    moveto('player', 12, 12, 'up'), moveto('Corvin Mott', 12, 11, 'down'), moveto('Wenlow', 13, 10, 'down'),
    S('pfm_fade_in(14)'),
    P('CORVIN', 'deadpan', "Sit. Tongue out. Follow the finger. Lovely.", '', 'Corvin Mott'),
    MV('player', ['turn_left', 'wait 8', 'turn_right', 'wait 8', 'turn_up']),               # follow the finger
    N('Corvin', "Your bill."),
    S('pfm_item(:INVOICE, 1, "Invoice")'),
    'INVOICE: "Item: one (1) heart attack, mine. Item: gauze. Item: the look on Wenlow\'s face. TOTAL: ₽0."',
    CH(["I'm fine.", 'The rain went up.'], [
        [P('CORVIN', 'angry', "You walked into a marsh that rains UPWARD.", '', 'Corvin Mott'),
         N('Corvin', "\"Fine\" is not on the menu, dear.")],
        [P('CORVIN', 'angry', "I'm aware of the direction of the rain.", '', 'Corvin Mott'),
         N('Corvin', "I'm a Warden. I get a memo.")]], cancel=1),
    P('WENLOW', 'happy', "Doctor, they did bring back the medicine-runner's sack—", '', 'Wenlow'),
    P('CORVIN', 'deadpan', "Wenlow, I'm having an emotion. Don't help.", '', 'Corvin Mott'),
    P('WENLOW', 'panic', "Sorry, Doctor!", 'sweat', 'Wenlow'),
    MV('Wenlow', [{'jump': [0, 0]}], wait=False), S('pbSEPlay("Anim/Crash", 80, 110)\npfm_shake(2, 14, 6)'),   # the tray
    {'wait': 20},
    N('Corvin', "...Item four. One tray."),
    {'selfswitch': ['A', True]}]

TRIAL = lambda key, rest: S('if (pf_trial_ready?(:%s) rescue false)\n  pf_trial_talk(:%s)\nelse\n%s\nend' % (
    key, key, '\n'.join('  ' + l for l in rest.split('\n'))))
WENLOW_TALK = [TRIAL('WENLOW_INFIRMARY',
                     'if $game_variables[%s].to_i >= 1\n'
                     '  pbMessage(_INTL("Wenlow: Don\'t have another one. Please. Don\'t have another one."))\n'
                     'else\n'
                     '  pbMessage(_INTL("Wenlow: I\'ll introduce you. I always introduce people. It\'s polite."))\n'
                     'end' % SWEET)]
CORVIN_TALK = [TRIAL('CORVIN_INFIRMARY',
                     'if (pfm_gym_won?(:LEADER_CORVIN) rescue false)\n'
                     '  pbMessage(_INTL("Corvin: Sit. Tongue out. Follow the finger. Lovely."))\n'
                     '  pbMessage(_INTL("Corvin: My Quiet Ward\'s stable tonight. If you\'re heading east past Lake Sallow into Ashkaar, keep your head down."))\n'
                     'else\n'
                     '  pbMessage(_INTL("Corvin: Your friend\'s in the dispensary, doing something devastatingly cheerful to my filing."))\n'
                     '  pbMessage(_INTL("Corvin: Go and stop her. Or don\'t."))\n'
                     'end')]


def events_223():
    return [
        at(ev('The Quiet Ward', page([]), page(QUIET_WARD, cond=V(1), trigger='autorun'), page([], cond=V(2))), 0, 0),
        at(ev('Invoice', page([]), page(INVOICE, cond=V(4), trigger='autorun'), page([], cond={'self': 'A'}),
              page([], cond=V(5))), 1, 0),
        at(ev('The Ward Night (Veil)', page([]), page([IF('pfm_get(:ch7_ward_night).to_i == 1', VEIL, [{'erase': True}])],
                                                      cond=V(5), trigger='autorun'), page([], cond=V(6))), 2, 0),
        walk_on('Wenlow (night)', 14, 11), walk_on('Juno (night)', 12, 17), walk_on('Ama', 11, 10),
    ]


def first_page(name, commands):
    """Gemini's event keeps its graphic, conditions and later pages; its FIRST page gets these commands"""
    def fn(evs):
        e = next((e for e in evs if e.get('name') == name), None)
        if e is None or e.get('type') != 'event': raise SystemExit('story_ch7: no paged event %r' % name)
        e['pages'][0]['commands'] = copy.deepcopy(commands)
        e['pages'][0]['story'] = TAG
    return fn


# ============================================================================================ 230 / 233 Gym 6
GUIDE = [N('Gym Guide', "The Infirmary! Poison-types on the Corrosive Mire."),
         N('Gym Guide', "Ground and Psychic cut through it. Fairies melt."),
         N('Gym Guide', "The Doctor fights two at once."),
         N('Gym Guide', "He says it's because patients come in pairs.")]
CORVIN_ARENA = 'Warden Corvin Mott'
G6_WIN = [
    P('CORVIN', 'deadpan', "...Well. That's the correct dose.", 'dots', CORVIN_ARENA),
    S('Prismfall.award_badge(pfm_gym(:LEADER_CORVIN))'),                                   # the Remedy Badge
    S('6.times { |i| pbSEPlay("Anim/HealBell", 70, 76 + i * 9); pbWait(0.24) }\npfm_glow(30, 60, 90, 16, 12)'),   # six notes; water in a channel
    N('Corvin', "Your case sings. I'd have that looked at."),
    N('Corvin', "Not by me. I'm busy."),
    S('pbReceiveItem(:TM84)'),
    N('Corvin', "Poison Jab. Close in, quick, and they go home feeling worse."),
    N('Corvin', "It's the bedside manner I was never taught. And that badge says Pokémon up to level thirty-nine will heed you."),
    N('Corvin', "The ferrymen will teach yours Surf. Lake Sallow's that way."),
    N('Corvin', "Cindervault's past it. Don't drink the lake either."),
    IF('$game_switches[333]', [N('Corvin', "...And Wenlow told me you measured for the Quiet Alcove too. Four and nine isn't easy. Thank you. Don't tell him I said that.")]),
    S('$game_variables[@@CH7_STEP] = 5 if $game_variables[@@CH7_STEP] < 5'),
    {'selfswitch': ['A', True]}]
G6_FIGHT = [
    IF('pfm_get(:ch7_g6_tried)', [N('Corvin', "Back on the table. Good. Second opinions are healthy.")], [
        S('pbSEPlay("Battle ball shake", 60, 90)'), {'wait': 12},                         # two Poke Balls in one hand
        P('CORVIN', 'neutral', "Everything's poison, dear. Dose makes the cure.", '', CORVIN_ARENA),
        N('Corvin', "Two at once, because nobody in Nadir ever has only one thing wrong with them."),
        P('CORVIN', 'smug', "Don't worry. I'm a doctor. I know exactly how much this hurts.", '', CORVIN_ARENA)]),
    S('pfm_set(:ch7_g6_tried)'), ebdx_ace("Ward. The patient one. Hold them."),
    IF('Prismfall.gym_battle(pfm_gym(:LEADER_CORVIN), double: true)', G6_WIN)]


def edit(spec_file, mid, fns):
    """apply fn(events) for each fn to one map's events block (only that block is re-dumped, as storylayer does)"""
    path = os.path.join(SL.HERE, 'specs', spec_file)
    chunks = open(path, encoding='utf-8').read().split('\n---\n')
    for i, chunk in enumerate(chunks):
        doc = yaml.safe_load(chunk)
        if not doc or doc.get('id') != mid: continue
        evs = doc.get('events') or []
        for fn in fns: fn(evs)
        lines = chunk.split('\n')
        k = next(n for n, l in enumerate(lines) if l.startswith('events:'))
        body = yaml.safe_dump({'events': evs}, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True)
        chunks[i] = '\n'.join(lines[:k]) + '\n' + body.rstrip('\n') + ('\n' if i == len(chunks) - 1 else '')
        open(path, 'w', encoding='utf-8').write('\n---\n'.join(chunks))
        return
    raise SystemExit('story_ch7: no map %d in %s' % (mid, path))


def spec_of(mid):
    return next(d for d in yaml.safe_load_all(open(os.path.join(SL.HERE, 'specs', FILES[mid]))) if d and d.get('id') == mid)


def main():
    print('map 220: %d events' % SL.patch(FILES[220], 220, events_220(), None, TAG))
    for name, pages in pages_220(spec_of(220)).items():
        print('map 220: %s pages (%d)' % (name, SL.set_pages(FILES[220], 220, name, pages, TAG)))
    print('map 223: %d events' % SL.patch(FILES[223], 223, events_223(), None, TAG))
    edit(FILES[223], 223, [first_page('Juno Hale', JUNO_TALK), first_page('Wenlow', WENLOW_TALK),
                           first_page('Corvin Mott', CORVIN_TALK)])
    print('map 223: Juno / Wenlow / Corvin talk')
    edit(FILES[230], 230, [first_page('Gym Guide', GUIDE)])
    print('map 230: the gym guide')
    arena = next(e for e in spec_of(233)['events'] if e.get('name') == CORVIN_ARENA)
    after = [p for p in arena['pages'] if (p.get('cond') or {}).get('self') == 'A']
    after = after[0] if after else page([], 'CORVIN', 'down', cond={'self': 'A'})
    after = {k: v for k, v in after.items() if k != 'story'}
    print('map 233: Corvin (%d)' % SL.set_pages(FILES[233], 233, CORVIN_ARENA, [page(G6_FIGHT, 'CORVIN', 'down'), after], TAG))


if __name__ == '__main__':
    main()
