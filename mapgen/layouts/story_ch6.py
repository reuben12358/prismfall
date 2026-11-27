#!/usr/bin/env python3
"""story_ch6: the Chapter 6 story beats ("What the Sand Keeps", story/25_SCRIPT_CH6.md) on the maps that are built:
Gemini's Duneholt / Ossaria layouts (duneholt_exterior.py, duneholt_interiors.py, duneholt_gym.py, ossaria_routes.py,
ossaria_landmarks.py), the Ch5 Lowlight 608 (wave8_story_craft.py + story_ch5.py) and the Concourse 180
(wave10_towns_craft.py). A STORY LAYER (storylayer.py): events are upserted by name, Gemini's own story events get new
pages with set_pages (they keep their place), and nothing else in those specs changes.

CH6_STEP (V126, design/FLAGS.md), map by map:
  608 the Lowlight      the Act II opener (STORY_CHAPTER >= 6, once): dawn, the barrier, Rook on the vault stair;
                        Dex's glass warms under your hand (an inspect page on Ch5's "Glass Dex"); Marlo at the shrine;
                        Juno's goodbye (talk to her)                                              0 -> 1
  180 the Concourse     the Meridian Mainline leaves from the Concourse's west avenue (warps x 0, y 32-37 <-> 612's
                        south edge; Gemini's 612 had no way in from Lumen). At step 0 a porter points you to the
                        Lowlight instead (the one functional line this layer adds).
  612 the Mainline      "The Checkpoint" as you join the queue (Gemini's touch scanners retired)  1 -> 2
  203 the Sandgate      arrival (Gemini's autorun, restaged; the caravan-mother and the gate guard speak in it) 2 -> 3
  209 the Dig Lab       Sahar, first meeting (warning 1); a tremor from the east sends you to the well
  204 Aquifer Quarter   "The Deep-works" and :ch6_drillsite, the first time you come after meeting Sahar
                        (Sergeant / Bereaved Duneholt versions; MANDATE PASS on :directorate)  3 -> 4
  206 -> 207           the Mural Gallery stays shut through Chapter 6 (it would show the Ossuary's murals first)
  200 / 210-213 Gym 5   the Dig's door opens at step 4; the guide and the aide say the script's lines; Sahar in 213
                        (three openers by :ch6_drillsite, the badge, TM83, the lift up to the excavators) 4 -> 5
  620 Marrow Road       "The Door in the Skull" (Gemini's touch column at x 55)                    5 -> 6
  624 the Ossuary       Field Notes, Sahar follows you (pf_echo_follow convoy), the four murals, the rubbing
                        (DUNEHOLT RUBBING, S116)                                                  6 -> 7
  620 Marrow Road       "Lecture, Archaeological" and K3 as you come out (S117; KESTREL_STAGE stays 1)  7 -> 8
  620 Marrow Road       Juno's letter (the Gale Post courier); STORY_CHAPTER 7                     8 -> 9
Unbuilt: 602 Candle Down and 603 the Highwold (no step lives there); their guarded exits on 612 / 600 / 601 turn you
back with a spoken line instead of a bracketed box (STAGE), and so does 200's west gate (810).

Run after the layouts that write these specs:
    python3 -I layouts/story_ch6.py && python3 -I build.py 180 200 203 204 206 209 210 213 600 601 608 612 620 624 --no-preview"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from story_early import P, N, S, IF, CH, MV, ITEM, page, ev
import story_early as SE
import storylayer as SL

TAG = 'ch6'
STEP = 'CH6_STEP'
SE.NAMES.update({'ROOK': 'Rook', 'SAHAR': 'Sahar', 'JUNO': 'Juno', 'KESTREL': 'Kestrel'})
OFFICER = 'trainer_MERIDIAN_DIRECTORATE'
BEREAVED_M, BEREAVED_F = 'trainer_HOLLOW_GRUNT_M', 'trainer_HOLLOW_GRUNT_F'


def V(n, **kw): return dict({'var': [STEP, n]}, **kw)
def CHAP(n, **kw): return dict({'var': ['STORY_CHAPTER', n]}, **kw)
def at(e, x, y): e['at'] = [x, y]; return e
def show(sheet, d=2): return [{'graphic': [sheet, 0, d, 0]}, {'opacity': 255}]
def walk_on(name, x, y):
    """an actor with no look of its own: a scene's move route gives it one (and takes it away)"""
    return at(ev(name, page([], through=True)), x, y)
def actor(name, x, y, sheet, d, lines, cond, gone=None, through=False):
    ps = [page([]), page(list(lines), sheet, d, cond=cond, through=through)]
    if gone: ps.append(page([], cond=gone))
    return at(ev(name, *ps), x, y)
def quest(text):
    """the chapter's one quest line, rewritten (pfm_quest only logs a new id)"""
    return [S('$PokemonGlobal.pf_quests.delete(:ch6_eighteen_roads) rescue nil'),
            S('pfm_quest(:ch6_eighteen_roads, "Eighteen Roads", "%s")' % text.replace('"', '\\"'))]
BACK = MV('player', ['dir_fix_on', 'backward', 'dir_fix_off'])
def shut(se, line, pitch=80):
    """for Gemini's guarded exits: its own script steps the player back after the line"""
    return [S('pbSEPlay("%s", 80, %d)' % (se, pitch)), line]
def gone(name, dur=16): return S('pfm_vanish("%s", %d)' % (name, dur))
def say(who, text, ev_name=None, expr='neutral', emote=''):
    return P(who, expr, text, emote, ev_name or '')


# ============================================================================================ 608 the Lowlight, dawn
ROOK_EV, JUNO_EV, MARLO_EV = 'Rook (dawn)', 'Juno (goodbye)', 'Marlo (shrine)'
OFF1, OFF2 = 'Directorate Officer (barrier) 1', 'Directorate Officer (barrier) 2'

OPENER = [
    S('pbBGMFade(1.0)\npbBGSFade(1.0)'),                                          # BGM: none
    S('pfm_fade_out(8)'), MV('player', [{'script': 'moveto(7, 7)'}, 'turn_up']),
    S('pfm_tone(-14, -26, -10, 44, 30)'),                                         # dawn, two weeks on
    S('pbSEPlay("Ring Glass Harmonic", 40, 150)'), {'wait': 24},                  # a wind-chime on a glass washing line
    S('pbSEPlay("Ring Glass Harmonic", 30, 135)'), {'wait': 16},
    # the glass ring under the Spire's foot, grey and silent; the shrine round its edge
    {'raw': [203, [6, 8, 2]]}, {'wait': 30}, S('pbSEPlay("Anim/Ice1", 35, 60)'), {'wait': 20},
    S('pfm_pan_home(30)'),
    # at the Veil's edge: two officers in white-and-gold by a new brass barrier
    MV(OFF1, ['turn_left', 'wait 20', 'turn_right'], wait=False), MV(OFF2, ['wait 10', 'turn_left', 'wait 20', 'turn_right']),
    {'wait': 10},
    # Rook on the bottom step of the vault stair, hood up, no lights, no drone
    MV('player', ['up', 'up']), {'wait': 20},
    say('ROOK', "I'm not filming. I'm just sitting.", ROOK_EV, 'sad'),
    N('Rook', "I come down every night. The guards let me."),
    N('Rook', "I think they think I'm doing a segment."),
    N('Rook', "Chat would say something."),
    MV(ROOK_EV, ['turn_left', 'wait 30', 'turn_down']),                            # the unopened Fizzbolt in his hands
    N('Rook', "I don't know what chat would say. I haven't asked."),
    {'selfswitch': ['A', True]}]

DEX_WARM = [
    # you step through; the officers don't stop you; they don't know how to
    S('pfm_face("%s", :player)' % OFF1), S('pfm_face("%s", :player)' % OFF2), {'wait': 24},
    MV(OFF1, ['turn_right'], wait=False), MV(OFF2, ['turn_right']),
    # Dex, mid-wave, his mouth open on a word; a soda can leaned on the shimmer as close as anyone could reach
    S('pfm_flash(190, 190, 255, 6, 40)\npbSEPlay("Anim/Ice1", 40, 70)'), {'wait': 40},
    S('pfm_face(:player, "Glass Dex")'), {'wait': 50},                            # you stand with him; your hand on his shoulder
    S('pbSEPlay("Heartbeat Sub-Pulse", 80, 45)'), {'wait': 30},                   # one very low note, under your ribs
    S('pfm_glow(70, 40, 0, 40, 30)'),                                             # cold, and then it isn't: warm, barely
    {'wait': 60},
    MV('player', ['dir_fix_on', 'backward', 'dir_fix_off']),                       # you take your hand away
    S('pbSEPlay("Ring Glass Harmonic", 25, 60)'), {'wait': 40},
    {'selfswitch': ['A', True]}]

GOODBYE = [
    # her hatbox, a sack of seed packets, the old flower-girl dress with the hem let down; her eyes are red
    S('pfm_face("%s", :player)' % JUNO_EV), {'wait': 20},
    say('JUNO', "I'm not going home.", JUNO_EV, 'sad'),
    N('Juno', "There's a doctor in Mirefen, down in Nadir. Dr Mott."),
    N('Juno', "He's got a whole ward of people turning to glass, slowly, and Uncle Rowan sends him seed stock every month for the medicine."),
    N('Juno', "I was going to send it by post this time."),
    N('Juno', "I'm not sending it by post. I'm taking it."),
    N('Juno', "I couldn't do anything for Dex. I can't even walk in there."),
    N('Juno', "But I can carry a sack."),
    CH(["I'll come with you.", "Be careful.", "..."], [
        [say('JUNO', "You can't, silly. You've got a badge to get.", JUNO_EV, 'happy'),
         N('Juno', "Duneholt's north, and Mirefen's down, and they're not letting anyone down the lifts any more."),
         N('Juno', "I'll find a way down. Verdancers always find the way down."),
         N('Juno', "It's up we're bad at.")],
        [say('JUNO', "I'm always careful. I'm careful about everything.", JUNO_EV),
         N('Juno', "It's very tiring.")],
        [say('JUNO', "I know. Me too.", JUNO_EV)]], cancel=3),
    say('JUNO', "Write to me! Gale Post.", JUNO_EV, 'happy'),
    N('Juno', "\"Juno, Mirefen, the one wearing a tree.\""),
    # she hugs you, hard and quick, and goes off along the Concourse toward the lift-shafts with the sack on her shoulder
    MV(JUNO_EV, [{'jump': [0, 0]}], wait=False), MV('player', [{'jump': [0, 0]}]), {'wait': 10},
    MV(JUNO_EV, ['through_on', 'turn_left', 'left', {'opacity': 0}]),
    {'var': [STEP, 1]}] + quest("Earn the fifth badge in Duneholt, up the Brass Road north (the Meridian Mainline out of the Concourse).")

MARLO = [N('Marlo', "You're the one who walks in. I saw you, that night."),
         N('Marlo', "Tell him— no. You can't tell him anything."),
         MV(MARLO_EV, ['turn_left', 'wait 30']),                                 # back to her candles
         N('Marlo', "...Tell him anyway.")]


def events_608():
    return [
        at(ev('Act II Opener', page([]), page(OPENER, cond=CHAP(6), trigger='autorun'),
              page([], cond=CHAP(6, self='A')), page([], cond=V(1))), 2, 0),
        actor(ROOK_EV, 7, 3, 'ROOK', 'down', [say('ROOK', "I don't know what chat would say. I haven't asked.", ROOK_EV, 'sad')],
              CHAP(6), CHAP(7)),
        actor(OFF1, 1, 5, OFFICER, 'right', [], CHAP(6), CHAP(7)),
        actor(OFF2, 1, 10, OFFICER, 'right', [], CHAP(6), CHAP(7)),
        at(ev('Directorate barrier', page([]), page(["MERIDIAN SECURITY DIRECTORATE — BY MANDATE OF THE ACCORD — NO ENTRY."], cond=CHAP(6))), 2, 3),
        actor(MARLO_EV, 1, 9, 'NPC 22', 'left', MARLO, CHAP(6), CHAP(7)),
        at(ev(JUNO_EV, page([]), page(GOODBYE, 'JUNO', 'right', cond=CHAP(6)), page([], cond=V(1))), 1, 7)]


def pages_608():
    dex = "Dex, mid-wave, soda crate on his hip. His mouth is open. He was about to tell you the rest."
    return {'Glass Dex': [page(DEX_WARM, cond=CHAP(6)), page([dex], cond=CHAP(6, self='A'))]}


# ============================================================================================ 180 / 612 the Mainline link
MAINLINE_IN = [IF('$game_variables[126] == 0',
                  [N('Concourse Porter', "A girl with a hatbox was asking after you. Down at the Lowlight, at the stairs."), BACK],
                  [S('pfm_fade_out(10)'),
                   IF('$game_variables[126] == 1', [{'transfer': {'map': 612, 'x': 55, 'y': 36, 'dir': 'right'}}],
                      [{'transfer': {'map': 612, 'x': 57, 'y': 61, 'dir': 'up'}}]),
                   S('pfm_fade_in(10)')])]


def events_180():
    return [at(ev('To the Meridian Mainline %d' % y, page([]), page(MAINLINE_IN, cond=CHAP(6), trigger='touch')), 0, y)
            for y in range(32, 38)]


CHECKPOINT = [
    # a brass barrier across the service road, a tent, a scanner plate on a post, two officers; the queue, hands out
    S('pbBGSPlay("Anim/Wind1", 30, 60) rescue nil'), {'wait': 20},
    MV('Queued Drover', ['turn_right'], wait=False), MV('Queued Pedlar', ['turn_right']),
    N('Directorate Officer', "Mandate checkpoint. Papers and tint. Hand on the plate."),
    MV('Queued Drover', ['turn_up']),
    N('Drover', "Two weeks ago this was a road."),
    N('Directorate Officer', "It's still a road, sir. It's a road with a checkpoint on it."),
    MV('player', ['right', 'turn_right']), {'wait': 16},                          # your turn
    S('pbSEPlay("Voltorb Flip mark", 80, 130)'), {'wait': 40},                    # chime... nothing
    S('pfm_flash(255, 90, 90, 6, 50)'),                                           # NULL
    N('Directorate Officer', "...Hold on."),
    # she turns to a ledger on the tent pole, runs a finger down it, and stops
    MV('Directorate Checkpoint Officer', ['turn_left']), S('2.times { pbSEPlay("GUI menu open", 50, 70); pbWait(0.4) }'), {'wait': 40},
    S('pfm_face("Directorate Checkpoint Officer", :player)'),
    IF('pf_choice(:ch5_lowlight_testimony) == :someone_else', [
        N('Directorate Officer', "You're flagged. By the Director herself."),
        N('Directorate Officer', "\"Do not obstruct. Report movements.\" That's all it says."),
        N('Directorate Officer', "So I'm not obstructing you."),
        N('Directorate Officer', "And I'm reporting that you went north. Have a nice trip.")], [
        N('Directorate Officer', "You're on the Chair's guest list. Gala, Lumen."),
        N('Directorate Officer', "...You were THERE?"),
        N('Directorate Officer', "Go on through. And — I'm sorry. About the Lowlight."),
        N('Directorate Officer', "My sister's on the Spire feeds. She was off that night."),
        N('Directorate Officer', "She's not been off since.")]),
    # the barrier swings up
    S('pbSEPlay("Door slide", 90, 70)'), {'switch': [576, True]}, S('$game_map.need_refresh = true'), {'wait': 20},
    S('pfm_face("Queued Drover", :player)'),                                       # behind you
    N('Drover', "Oh, very nice. Very fair."),
    N('Drover', "Some of us have been here since six."),
    S('pbBGSFade(1.0)'),
    {'var': [STEP, 2]}]


def events_612():
    return [at(ev('The Checkpoint', page([]), page(CHECKPOINT, cond=V(1), trigger='autorun'), page([], cond=V(2))), 1, 0)] + \
           [at({'type': 'warp', 'name': 'South to Lumen %d' % x, 'to': {'map': 180, 'x': 1, 'y': 34, 'dir': 'right'}}, x, 63)
            for x in range(54, 61)]


def setpages_612():
    plate = N('Directorate Officer', "Mandate checkpoint. Papers and tint. Hand on the plate.")
    cleared = "Directorate Officer: You're cleared through the Mainline checkpoint. Keep to the service road — freight trains still run the brass track."
    return {'Checkpoint Scanner Trigger': [page([], through=True)],
            'Directorate Checkpoint Officer': [page([plate], OFFICER, 'down'), page([cleared], OFFICER, 'down', cond={'switch': 576})],
            'Checkpoint Brass Barrier': [page([plate], tile=25935), page([], tile=25936, through=True, cond={'switch': 576})]}


# ============================================================================================ 203 the Sandgate
ARRIVAL = [
    # a canyon mouth walled across in sandstone, gate-towers cut from the cliff; through it, the terraces and the well
    S('pbSEPlay("Anim/Wind1", 50, 70)'), {'raw': [203, [8, 6, 3]]}, {'wait': 40}, S('pfm_pan_home(30)'),
    # the caravan-mother spits at the notices
    MV('Caravan-mother', ['turn_up']), {'wait': 12}, S('pbSEPlay("Water1", 40, 150)'), {'wait': 10},
    MV('Caravan-mother', ['turn_down']),
    N('Caravan-mother', "Two notices. One from a man we elected for life and can't get rid of."),
    N('Caravan-mother', "One from a company we never elected at all."),
    N('Caravan-mother', "And the western wells have changed hands twice this year."),
    N('Caravan-mother', "Both times the new owners had an accent."),
    S('pfm_face("Gate Guard", :player)'),
    N('Gate Guard', "Welcome to Duneholt. Water's a bone a cup."),
    N('Gate Guard', "It was free last year.")] + quest("Earn the fifth badge at the Dig, Duneholt's gym.") + [{'var': [STEP, 3]}]


def setpages_203():
    return {'Sandgate Arrival (Ch6)': [page([]), page(ARRIVAL, cond=V(2), trigger='autorun'), page([], cond=V(3))],
            'Caravan-mother': [page([N('Caravan-mother', "Two notices. One from a man we elected for life and can't get rid of."),
                                     N('Caravan-mother', "One from a company we never elected at all."),
                                     N('Caravan-mother', "And the western wells have changed hands twice this year."),
                                     N('Caravan-mother', "Both times the new owners had an accent.")], 'NPC 04', 'down')]}


# ============================================================================================ 209 Sahar's Dig Lab
REMIND = [IF('(pf_trial_ready?(:SAHAR_DIGLAB) rescue false)', [S('pf_trial_talk(:SAHAR_DIGLAB)')],
             [say('SAHAR', "Walk the bones, never the sand.", 'Sahar')])]
FIRST_MEETING = [
    # at the back, brushing dust off a skull the size of a cart, one stroke at a time
    S('3.times { pbSEPlay("Anim/Wind1", 25, 160); pbWait(0.6) }'),
    say('SAHAR', "Don't come any closer. You'll breathe on it.", 'Sahar'),
    {'wait': 20}, S('pfm_face("Sahar", :player)'), {'wait': 10},
    N('Sahar', "...You're the challenger. The Lumen one."),
    N('Sahar', "The one who walks in the glass. Everyone's heard."),
    N('Sahar', "Sahar Ostrand. I keep the Dig, and the Earth Plate, and a well that's falling into itself a rung a week while a man in a palace sells the water underneath it."),
    say('SAHAR', "You'll have read his notice. He has a lovely hand.", 'Sahar', 'deadpan'),
    N('Sahar', "He should have been a calligrapher. We'd all be happier."),
    say('SAHAR', "One thing, before you go anywhere in Ossaria.", 'Sahar'),
    N('Sahar', "Walk the bones, never the sand."),
    N('Sahar', "Where there's a rib or a road of bone, walk on it."),
    N('Sahar', "Where there's only sand, don't. The desert keeps everything."),
    N('Sahar', "It just doesn't keep it where you left it."),
    S('pfm_set(:ch6_met_sahar)'),
    {'wait': 20}, S('pbSEPlay("Anim/Earth4", 60, 45)\npfm_shake(1, 20, 14)'),   # deep under the town, east: the well
    MV('Sahar', ['turn_right', 'wait 30', 'turn_up']),
    {'selfswitch': ['A', True]}]


def setpages_209():
    return {'Sahar': [page(REMIND, 'SAHAR', 'down'),
                      page(FIRST_MEETING, 'SAHAR', 'up', cond=V(3)),
                      page(REMIND, 'SAHAR', 'up', cond=V(3, self='A')),
                      page([], cond=V(4)),                                       # at the Dig, then the Marrow Road
                      page(REMIND, 'SAHAR', 'down', cond=V(9))]}


# ============================================================================================ 204 the Aquifer Quarter
SAHAR_D, SERG, OFFA, OFFB = 'Sahar (drill)', 'Sergeant (drill)', 'Officer (drill) 1', 'Officer (drill) 2'
BER1, BER2, BOY, GIRL, MOTHER, OCHRE = 'Bereaved (fence) 1', 'Bereaved (fence) 2', 'Caravan boy (drill)', 'Caravan girl (drill)', 'Mother (terrace)', 'Excadrill (Ochre)'
DRIL = ['Drilbur %d' % i for i in (1, 2, 3)]
SHAFT = (37, 21)
OUT_WEST = ['through_on', {'speed': 5}] + ['left'] * 9 + [{'opacity': 0}]

SAHAR_COMES = [MV(SAHAR_D, show('SAHAR', 2) + ['through_on', {'speed': 3}, 'down', 'down', 'down', 'down', 'down', 'right', 'down', 'turn_right', 'through_off'])]
ALL_END = [
    S('pfm_face("%s", :player)' % SAHAR_D), MV(SAHAR_D, ['turn_left']),             # looking down the well
    S('pbSEPlay("Anim/Earth4", 70, 40)\npfm_shake(1, 16, 20)'), {'wait': 10}, S('pbSEPlay("Water1", 60, 50)'),
    say('SAHAR', "It dropped again. Did you feel it?", SAHAR_D, 'sad'),
    N('Sahar', "A whole rung, just now."),
    S('pfm_face("%s", :player)' % SAHAR_D),
    N('Sahar', "They put collars on diggers and sent them down to drink my well for a man in Lumen. And now the Hollow have let them go, and the shaft's open, and the water will run down it like a drain."),
    N('Sahar', "Come to the Dig when you're ready."),
    N('Sahar', "I'd like to hit something that's allowed to hit back."),
    MV(SAHAR_D, ['through_on', 'left', 'up', 'up', 'up', 'up', 'up', {'opacity': 0}]),
    S('pfm_fade_out(16)')] + [MV(n, [{'opacity': 0}], wait=False) for n in [SERG, OFFA, OFFB, BER1, BER2, BOY, GIRL, MOTHER, OCHRE] + DRIL] + [
    {'var': [STEP, 4]}, S('pfm_fade_in(16)')]

HOLLOW = [
    S('pf_choose(:ch6_drillsite, :hollow)'),
    S('setBattleRule("field", :DESERT)'),
    IF('TrainerBattle.start(:MERIDIAN_DIRECTORATE, "Sergeant", 6)', [
        N('Directorate Sergeant', "This is obstruction of the Mandate. You'll be in a report by tonight."),
        # the Hollow and the children run the Drilbur out through the Sandgate; Ochre goes last, looks back once, digs
        MV(DRIL[0], OUT_WEST, wait=False), MV(DRIL[1], ['wait 6'] + OUT_WEST, wait=False), MV(DRIL[2], ['wait 12'] + OUT_WEST, wait=False),
        MV(BER2, ['wait 4'] + OUT_WEST, wait=False), MV(GIRL, ['wait 10'] + OUT_WEST, wait=False),
        MV(OCHRE, ['wait 30', 'turn_right', 'wait 30', 'turn_left']),
        S('pbSEPlay("Anim/Earth4", 80, 70)\npfm_shake(2, 12, 10)'), gone(OCHRE, 20),
        S('pfm_face("%s", :player)' % BER1),
        N('Bereaved', "The red giant thanks you. So do we."),
        N('Bereaved', "...So does Ochre, the big one."),
        N('Bereaved', "That was her name, before they put a number on her."),
        MV(BER1, OUT_WEST, wait=False),
        # the sergeant lets the caravan boy go; nobody's told her what else to do
        MV(BOY, ['through_on', {'speed': 5}, 'left', 'left', 'up', 'up', {'opacity': 0}], wait=False),
        MV(SERG, ['turn_down', 'wait 40', 'turn_left']), {'wait': 10}] + SAHAR_COMES + ALL_END,
       [{'exit': True}])]

DIRECTORATE = [
    S('pf_choose(:ch6_drillsite, :directorate)'),
    S('setBattleRule("field", :DESERT)'),
    IF('TrainerBattle.start(:HOLLOW_GRUNT_M, "Bereaved", 7)', [
        # the Hollow scatter over the terrace walls; handlers loop new cables on and lead the Drilbur back down
        MV(BER1, ['through_on', {'jump': [-1, -2]}, {'opacity': 0}], wait=False), MV(BER2, ['through_on', {'jump': [-1, 2]}, {'opacity': 0}], wait=False),
        S('3.times { pbSEPlay("Mining pick", 50, 140); pbWait(0.3) }'),
        MV(OFFB, ['through_on', 'right', 'right', 'turn_left'], wait=False),
        MV(DRIL[0], ['through_on', 'right', 'right', 'right', {'opacity': 0}], wait=False),
        MV(DRIL[1], ['wait 8', 'through_on', 'right', 'right', 'right', {'opacity': 0}], wait=False),
        MV(DRIL[2], ['wait 16', 'through_on', 'right', 'right', 'right', {'opacity': 0}]),
        # the Excadrill fights all the way down
        S('pbSEPlay("Cries/EXCADRILL", 90, 90) rescue nil\npfm_shake(3, 14, 16)'),
        MV(OCHRE, [{'jump': [0, 0]}, 'through_on', 'right', {'jump': [0, 0]}, 'right', {'opacity': 0}]),
        S('pfm_face("%s", :player)' % SERG),
        N('Directorate Sergeant', "Good work. Very good work."),
        N('Directorate Sergeant', "The Directorate remembers its friends."),
        ITEM('MANDATEPASS', 1, 'Mandate Pass'),
        # they take the caravan boy anyway; his mother doesn't scream this time; she just watches you
        MV(OFFA, ['through_on', 'up', 'up', 'up', {'opacity': 0}], wait=False),
        MV(BOY, ['through_on', 'wait 4', 'up', 'up', 'up', {'opacity': 0}], wait=False),
        S('pfm_face("%s", :player)' % MOTHER), {'wait': 60}] + SAHAR_COMES + ALL_END,
       [{'exit': True}])]

SANCTUARY = [
    S('pf_choose(:ch6_drillsite, :sanctuary)'),
    # you shout her name; it goes up the terraces and round the well and comes back to you three times
    MV('player', ['turn_up']),
    S('[90, 55, 30].each { |v| pbSEPlay("Anim/Saint7", v, 90); pbWait(0.55) }'),
    # Sahar comes down the terrace stairs, not fast, sand on her sleeves, spectacles up on her head; everyone stops
] + SAHAR_COMES + [
    S('pfm_face("%s", "%s")' % (SERG, SAHAR_D)), S('pfm_face("%s", "%s")' % (BER1, SAHAR_D)), S('pfm_face(:player, "%s")' % SAHAR_D),
    say('SAHAR', "Sergeant. Let go of that child.", SAHAR_D, 'angry'),
    N('Directorate Sergeant', "Warden, with respect, the Mandate—"),
    N('Sahar', "The Mandate is two weeks old."),
    N('Sahar', "The Warden's right of sanctuary is two hundred and ninety-six years old."),
    N('Sahar', "\"Any child of the city who stands within sight of its Plate stands under its Warden.\""),
    N('Sahar', "The Earth Plate is in that well. That child is in sight of it."),
    N('Sahar', "Under the Concordance, Sergeant. Read it sometime."),
    N('Sahar', "It's short. I'll lend you mine."),
    # the sergeant looks at her squad; her squad looks at the well; she lets go
    MV(SERG, ['turn_up', 'wait 24'], wait=False), MV(OFFA, ['wait 12', 'turn_left', 'wait 24']), MV(SERG, ['turn_left']),
    MV(BOY, ['through_on', {'speed': 4}, 'left', 'left', 'left', 'turn_right', 'through_off']),
    N('Directorate Sergeant', "This goes in my report."),
    say('SAHAR', "Spell my name right. It has an H in it nobody hears.", SAHAR_D, 'deadpan'),
    say('SAHAR', "That law covers children, Sergeant.", SAHAR_D, 'sad'),
    S('pfm_face("%s", "%s")' % (SAHAR_D, DRIL[0])),
    N('Sahar', "It doesn't cover them."),
    N('Sahar', "I can't stop you. I'm sorry."),
    # the Hollow are gone; half the Drilbur go back down the shaft; Ochre fights all the way down; the rest scatter
    MV(BER1, OUT_WEST, wait=False), MV(BER2, OUT_WEST, wait=False),
    S('2.times { pbSEPlay("Mining pick", 50, 140); pbWait(0.3) }'),
    MV(DRIL[0], ['through_on', 'right', 'right', 'right', {'opacity': 0}], wait=False),
    MV(DRIL[2], OUT_WEST, wait=False),
    S('pbSEPlay("Cries/EXCADRILL", 90, 90) rescue nil\npfm_shake(3, 14, 16)'),
    MV(OCHRE, [{'jump': [0, 0]}, 'through_on', 'right', {'jump': [0, 0]}, 'right', {'opacity': 0}]),
    MV(DRIL[1], ['through_on', 'right', 'right', 'right', {'opacity': 0}]),
    MV(GIRL, ['through_on', {'speed': 4}, 'left', 'left', 'turn_right', 'through_off']),   # the children stay close to her
    MV(SAHAR_D, ['turn_up']), {'wait': 30},                                       # to no one, after
    N('Sahar', "Two hundred and ninety-six years, and the law still thinks a digger is a shovel."),
    {'wait': 20}] + ALL_END

DEEP_WORKS = [
    S('pfm_fade_out(8)'), MV('player', [{'script': 'moveto(30, 20)'}, 'turn_right']), S('pfm_fade_in(16)'),
    # the great well: terraces, caravanserai, washing, goats; across it, a brass derrick over a shaft, a fence, a pipe
    {'raw': [203, [4, 5, 3]]}, {'wait': 30}, S('pfm_pan_home(30)'),
    # as you come to the rail the ground shakes; deep down, something shifts its weight; the water slops in the well
    S('pbSEPlay("Anim/Earth4", 80, 45)\npfm_shake(2, 8, 30)'), {'wait': 24}, S('pbSEPlay("Water1", 70, 60)'), {'wait': 20},
    # a heavy WHUMP from the deep-works; sand and steam out of the shaft; the derrick leans
    S('pbSEPlay("Anim/Explosion7", 80, 60)\npfm_shake(5, 14, 16)\npfm_glow(70, 60, 40, 16, 10)'), {'wait': 10},
    # out of the shaft: three Drilbur and an Excadrill, brass collars with the sunburst, cables trailing
    MV(DRIL[0], show('Followers/DRILBUR', 4) + ['through_on', {'speed': 4}, 'left', 'left', 'up', 'turn_left'], wait=False),
    MV(DRIL[1], ['wait 8'] + show('Followers/DRILBUR', 4) + ['through_on', {'speed': 4}, 'left', 'left', 'turn_left'], wait=False),
    MV(DRIL[2], ['wait 16'] + show('Followers/DRILBUR', 4) + ['through_on', {'speed': 4}, 'left', 'left', 'down', 'turn_left'], wait=False),
    MV(OCHRE, ['wait 24'] + show('Followers/EXCADRILL', 4) + ['through_on', {'speed': 3}, 'left', 'turn_left']),
    MV('Meridian Foreman', ['turn_right']),
    N('Meridian Foreman', "The cores! The CORES are loose!"),
    N('Meridian Foreman', "Somebody's cut the collars—"),
    # grey cowls at the fence, bark masks with sad faces: Hollow, cutting the cables; the caravan children run out laughing
    MV(BER1, show(BEREAVED_M, 6)), MV(BER2, show(BEREAVED_F, 6)),
    S('3.times { pbSEPlay("Mining pick", 50, 150); pbWait(0.35) }'),
    MV(BOY, show('NPC 05', 6) + ['through_on', {'speed': 5}, 'right', 'right', 'right', 'turn_right'], wait=False),
    MV(GIRL, ['wait 6'] + show('NPC 09', 6) + ['through_on', {'speed': 5}, 'right', 'right', 'turn_right']),
    MV(DRIL[0], ['left'], wait=False), MV(DRIL[1], ['left'], wait=False), MV(DRIL[2], ['left']),
    N('Bereaved', "Go on! Go on, you're free, GO!"),
    N('Caravan Boy', "This way! This way, little one!"),
    # and then the white-and-gold: a Directorate squad down the terrace steps at a run
    MV(SERG, show(OFFICER, 2) + ['through_on', {'speed': 5}, 'down', 'down', 'down', 'down', 'turn_down'], wait=False),
    MV(OFFA, ['wait 6'] + show(OFFICER, 2) + ['through_on', {'speed': 5}, 'down', 'down', 'down', 'down', 'turn_down'], wait=False),
    MV(OFFB, ['wait 12'] + show(OFFICER, 2) + ['through_on', {'speed': 5}, 'down', 'down', 'down', 'down', 'turn_down']),
    N('Directorate Sergeant', "By Mandate of the Accord! Everyone STOP!"),
    N('Directorate Sergeant', "Those are Meridian assets!"),
    N('Directorate Sergeant', "Those children are aiding saboteurs. Take them."),
    # an officer grabs the boy; his mother screams from a terrace above; Ochre plants herself in front of the children
    MV(OFFA, ['down', 'left', 'turn_left']), MV(BOY, [{'jump': [0, 0]}], wait=False),
    MV(MOTHER, show('NPC 04', 2)), S('pfm_emote("%s", 3)' % MOTHER), S('pbSEPlay("Anim/Scream", 70, 100) rescue nil'),
    MV(OCHRE, ['through_on', 'left', 'turn_right']), S('pbSEPlay("Cries/EXCADRILL", 80, 110) rescue nil'), {'wait': 10},
    S('pfm_face("%s", :player)' % BER1),                                          # to you, across the terrace
    N('Bereaved', "You! The one from the Lowlight!"),
    N('Bereaved', "Help us get them into the dunes!"),
    S('pfm_face("%s", :player)' % SERG),
    N('Directorate Sergeant', "You! Guest of the Chair!"),
    N('Directorate Sergeant', "Help us secure the site!"),
    CH(["Help the Hollow get the freed Pokémon into the dunes.", "Help the Directorate secure the site.", "Shout for Sahar."],
       [HOLLOW, DIRECTORATE, SANCTUARY], cancel=0)]

PARALLEL_204 = [S('if pfm_get(:ch6_met_sahar)\n  $game_self_switches[[@map_id, @event_id, "B"]] = true\n  $game_map.need_refresh = true\nend'),
                {'wait': 10}]


def events_204():
    sx, sy = SHAFT
    return [at(ev('The Deep-works', page([]), page(PARALLEL_204, cond=V(3), trigger='parallel'),
                  page(DEEP_WORKS, cond=V(3, self='B'), trigger='autorun'), page([], cond=V(4))), 1, 0),
            walk_on(DRIL[0], sx, sy), walk_on(DRIL[1], sx + 1, sy), walk_on(DRIL[2], sx, sy + 1), walk_on(OCHRE, sx + 1, sy + 1),
            walk_on(BER1, 33, 18), walk_on(BER2, 33, 22), walk_on(BOY, 26, 21), walk_on(GIRL, 26, 19),
            walk_on(SERG, 36, 12), walk_on(OFFA, 37, 12), walk_on(OFFB, 38, 12),
            walk_on(MOTHER, 30, 12), walk_on(SAHAR_D, 27, 12)]


def pages_204(spec_events):
    g = next(e for e in spec_events if e.get('name') == 'Directorate Sergeant')
    lines = g['pages'][0]['commands']
    return {'Directorate Sergeant': [page([], cond=V(3)), page(list(lines), OFFICER, 'down', cond=V(4))]}


# ============================================================================================ Gym 5: 200 door, 210, 213
DIG_DOOR = [IF('$game_variables[126] >= 4',
               [{'se': 'Door enter'}, S('pfm_fade_out(8)'), {'transfer': {'map': 210, 'x': 10, 'y': 15, 'dir': 'up'}}, S('pfm_fade_in(8)')],
               [S('pbSEPlay("Player bump", 80, 80)'), N("Sahar's Aide", "The Warden's up at her Dig Lab, on the northwest terrace."), BACK])]

GYM_GUIDE = [N('Gym Guide', "The Dig: Ground-types on the Desert field."),
             N('Gym Guide', "Water, Grass and Ice dig in. Electric doesn't, ever, at all."),
             N('Gym Guide', "Sun hardens and shade sinks. The mirrors pick which lanes are in the sun."),
             N('Gym Guide', "Falling isn't failing in here."),
             N('Gym Guide', "Sahar says falling's how you find the second floor.")]
AIDE = [N("Sahar's Aide", "Everyone tries the door. The door's painted on."), N("Sahar's Aide", "The way in is down.")]

ARENA_INTRO = [
    # a pit of sand under a shaft of sunlight, the walls lined with labelled bones; Sahar in the light, Claydol drifting
    S('pfm_glow(70, 56, 20, 24, 30)'), {'wait': 10},
    MV('Warden Sahar', ['turn_left', 'wait 12', 'turn_down']), {'wait': 10},       # she coughs, once, into her sleeve
    IF('pf_choice(:ch6_drillsite) == :sanctuary', [say('SAHAR', "You shouted my name across the well.", 'Warden Sahar'),
                                                   N('Sahar', "Nobody's shouted my name since I was a girl."),
                                                   N('Sahar', "It was very loud. Thank you.")]),
    IF('pf_choice(:ch6_drillsite) == :hollow', [say('SAHAR', "You let the Hollow take Meridian's diggers into my dunes.", 'Warden Sahar'),
                                                N('Sahar', "I've been told to be angry about it. I'm working on it.")]),
    IF('pf_choice(:ch6_drillsite) == :directorate', [say('SAHAR', "You helped them put the collars back on. I saw.", 'Warden Sahar'),
                                                     N('Sahar', "I'm not going to say anything about it. The sand will.")]),
    say('SAHAR', "The desert keeps everything.", 'Warden Sahar'),
    N('Sahar', "It just doesn't keep it where you left it."),
    say('SAHAR', "Patience is a Ground-type's whole art.", 'Warden Sahar', 'deadpan'),
    N('Sahar', "I'm fifty-eight and I have a cough. Let's see who runs out first.")]
ARENA_WIN = [
    say('SAHAR', "...", 'Warden Sahar', 'shocked'),
    say('SAHAR', "Well. You found the bottom. Most people stop one layer short.", 'Warden Sahar'),
    S('Prismfall.award_badge(pfm_gym(:LEADER_SAHAR))'),
    # the case's five notes, one after another and then together; the light along its seams is steadier now
    S('5.times { |i| pbSEPlay("Anim/HealBell", 70, 70 + i * 9); pbWait(0.24) }\n3.times { pbSEPlay("Anim/HealBell", 60, 88) }\npfm_flash(255, 240, 200, 10, 60)'),
    {'wait': 20},
    N('Sahar', "It sings. ...Of course it does."),
    N('Sahar', "Everything you carry is strange, isn't it."),
    S('pbReceiveItem(:TM83)'),
    N('Sahar', "Bulldoze. Shake the ground, slow whatever's standing on it. And that badge means Pokémon up to level thirty-five will heed you."),
    N('Sahar', "My excavators will teach yours Strength."),
    N('Sahar', "They've been waiting for an excuse."),
    IF('$game_switches[325]', [say('SAHAR', "I buried that. The sand dug it up. I'd rather not argue with sand twice.", 'Warden Sahar')]),
    S('pfm_fade_out(20)'), {'var': [STEP, 5]},
    {'se': 'Door exit'}, {'transfer': {'map': 210, 'x': 14, 'y': 11, 'dir': 'right'}},   # the lift up to the excavators
    S('pfm_fade_in(20)')]
ARENA = [IF('pfm_get(:ch6_sahar_tried)', [say('SAHAR', "Again. Good. The second dig always finds more.", 'Warden Sahar')], ARENA_INTRO),
         S('pfm_set(:ch6_sahar_tried)'),
         IF('Prismfall.gym_battle(pfm_gym(:LEADER_SAHAR), double: false)', ARENA_WIN)]


def setpages_gym():
    return {
        200: {'The Dig (Duneholt Gym)': [page(DIG_DOOR, trigger='touch')]},     # a walkable door tile: walk into it
        210: {'Gym Guide': [page(GYM_GUIDE, 'NPC 21', 'right')], "Sahar's Aide": [page(AIDE, 'NPC 14', 'down')]},
        213: {'Warden Sahar': [page([]), page(ARENA, 'SAHAR', 'down', cond=V(4)), page([], cond=V(5))]}}


def events_213():
    e = ev('Claydol (Sahar)', page([]), page([], 'Followers/CLAYDOL', 'down', cond=V(4), step=True), page([], cond=V(5)))
    return [at(e, 11, 4)]


# ============================================================================================ 620 the Marrow Road
SAHAR_M = 'Sahar (Door in the Skull)'
KES, COURIER = 'Kestrel (brow)', 'Gale Post courier'
DOOR = [
    # the dig terraces; at their end a skull the size of a house, the sand slid off its brow overnight: a doorway
    S('pbSEPlay("Anim/Earth4", 50, 120)'), {'raw': [203, [6, 6, 3]]}, {'wait': 30},
    S('pfm_glow(60, 40, 10, 20, 20)'),                                            # Sahar's lamp; she has gone very pale
    MV(SAHAR_M, ['turn_up']), {'wait': 30},
    S('pfm_fade_out(10)'), MV('player', [{'script': 'moveto(63, 37)'}, 'turn_left']), S('pfm_pan_home(1)'), S('pfm_fade_in(14)'),
    say('SAHAR', "...", SAHAR_M, 'shocked', 'dots'),
    S('pfm_face("%s", :player)' % SAHAR_M),
    say('SAHAR', "I know this door.", SAHAR_M, 'sad'),
    N('Sahar', "AF 281. I was thirty-nine."),
    N('Sahar', "My team took four months and a Claydol to open it. Nine of us."),
    N('Sahar', "I was so proud I couldn't sleep."),
    N('Sahar', "I made rubbings. I wrote a report. I sent it to the Sovereign, because that's what you do when you find something that changes the history of the world."),
    N('Sahar', "You tell the Accord."),
    MV(SAHAR_M, ['turn_up']), {'wait': 20},
    N('Sahar', "He came himself. Valen."),
    N('Sahar', "He walked through it with a lamp, all the way to the end, alone. And when he came out he said, \"Seal it, Sahar. For the realm.\""),
    N('Sahar', "So we sealed it. I burned the rubbings."),
    N('Sahar', "I told my team we'd found a collapsed granary."),
    N('Sahar', "Two of them still don't speak to me."),
    S('pfm_face("%s", :player)' % SAHAR_M),
    say('SAHAR', "I buried the truth once because I was told to.", SAHAR_M),
    N('Sahar', "The sand has dug it up."),
    N('Sahar', "I'd rather not argue with sand twice."),
    N('Sahar', "Walk the bones in there, the way I told you."),
    N('Sahar', "The floor's older than the rules about floors. Come on."),
    {'var': [STEP, 6]},
    MV(SAHAR_M, ['through_on', 'right', 'right', 'right', 'up', {'opacity': 0}]),
    MV('player', ['right', 'right', 'up']),
    S('pfm_fade_out(12)'), {'se': 'Door enter'}, {'transfer': {'map': 624, 'x': 21, 'y': 37, 'dir': 'up'}}, S('pfm_fade_in(12)')]

K3_AFTER = [
    say('KESTREL', "...", KES, 'sad'),
    N('Kestrel', "No. Not closer."),
    # he sits on a rib of bone, his back to the skull; after a while, the lace from under his coat: a black veil
    MV(KES, ['turn_down']), {'wait': 50}, S('pbSEPlay("GUI menu open", 40, 60)\npfm_glow(26, 26, 40, 20, 20)'), {'wait': 20},
    N('Kestrel', "Gran's trunk. It was hers. Her Warden's veil."),
    N('Kestrel', "Gran kept it in a trunk that wasn't even locked, for six years, and never said."),
    S('pfm_face("%s", :player)' % KES),
    say('KESTREL', "Everyone keeps telling me to let it go.", KES, 'angry'),
    N('Kestrel', "My mother had a seat, and a Plate, and a city that loved her."),
    N('Kestrel', "Then one night she had nothing. Let WHAT go?"),
    N('Kestrel', "They say she died in exile. Of the wilting. They sent a box."),
    N('Kestrel', "Nobody saw a body."),
    N('Kestrel', "Nobody in Gravenmoor will say where she's buried."),
    say('KESTREL', "And now there's a man in a mask who talks like her, and the whole realm's saying it. Every inn from here to Ebbmouth.", KES, 'sad'),
    N('Kestrel', "The Mourner's Morwen Vane. She didn't die."),
    N('Kestrel', "She was made to disappear, and she came back."),
    N('Kestrel', "She wasn't killed by the Bleed. She was made to disappear."),
    CH(["Then go and find out.", "It might not be her, Kestrel.", "..."], [
        [S('pf_choose(:ch6_kestrel_rumor, :encourage)'),
         say('KESTREL', "...You think it's her.", KES, 'shocked', 'jolt'),
         say('KESTREL', "You think it could be her.", KES, 'happy'),
         N('Kestrel', "Everyone else says \"let it go\". You said \"go\"."),
         N('Kestrel', "Then I'm going. All the way."),
         N('Kestrel', "Wherever he turns up next, I'll be closest.")],
        [S('pf_choose(:ch6_kestrel_rumor, :warn)'),
         say('KESTREL', "I know it might not be her. I KNOW.", KES, 'angry'),
         N('Kestrel', "Don't you think I know?"),
         say('KESTREL', "...I just need it not to be nobody.", KES, 'sad'),
         MV(KES, ['turn_up'])],                                                     # he stands up and won't look at you
        [S('pf_choose(:ch6_kestrel_rumor, :silent)'),
         say('KESTREL', "Yeah. That's what Gran says, too.", KES, 'sad'),
         N('Kestrel', "Nothing, very loudly.")]], cancel=3),
    say('KESTREL', "The cell's gone south and down, to Nadir.", KES),
    N('Kestrel', "Mirefen, the char-burners said. I'm going after them."),
    N('Kestrel', "Don't follow me. You will anyway."),
    N('Kestrel', "Just don't do it where I can see."),
    # east along the Marrow Road toward the Kneeling Stones, the veil back under his coat
    MV(KES, ['through_on', 'down', 'down', 'down', 'down'] + ['right'] * 12 + [{'opacity': 0}]),
    {'switch': ['CH6_K3_DONE', True]}, {'var': [STEP, 8]}]
K3_BATTLE = [S('pfm_set(:ch6_k3_tried)'), IF('Prismfall.rival_battle(:RIVAL_KESTREL, "Kestrel", 3, field: :DESERT)', K3_AFTER)]

LECTURE = [
    S('pfm_tone(34, -6, -40, 10, 30)'),                                             # outside, in the evening light
    MV(SAHAR_M, [{'opacity': 255}, 'turn_up']), {'wait': 30},                        # looking at the seal-stone you came out past
    S('pfm_face(:player, "%s")' % SAHAR_M),
    say('SAHAR', "The seal on that inner door was three hundred years old.", SAHAR_M),
    N('Sahar', "It took a team of nine and a Claydol four months to shift it in AF 281."),
    S('pfm_face("%s", :player)' % SAHAR_M),
    say('SAHAR', "You leaned on it.", SAHAR_M, 'deadpan', 'dots'),
    CH(["It was loose.", "I was tired.", "..."], [
        [say('SAHAR', "It was not loose.", SAHAR_M, 'deadpan'), N('Sahar', "Things are not \"loose\" around you. Things give up.")],
        [say('SAHAR', "You were tired, and a three-hundred-year-old seal fell over.", SAHAR_M, 'deadpan'),
         N('Sahar', "I'll put that in the report. \"The challenger was tired.\"")],
        [say('SAHAR', "Don't do the silence at me. I'm an archaeologist.", SAHAR_M, 'deadpan'),
         N('Sahar', "I've been stared at by better skulls than you.")]], cancel=3),
    # a voice from the top of the skull
    MV(KES, show('KESTREL', 2)), {'raw': [203, [8, 2, 4]]},
    say('KESTREL', "Told you. Things give up around them.", KES, 'smug'),
    N('Kestrel', "Rivers. Plates. Me. Twice."),
    MV(SAHAR_M, ['turn_up']),
    say('SAHAR', "...Twice?", SAHAR_M, 'shocked', 'question'),
    say('KESTREL', "Don't.", KES, 'deadpan'),
    # K3: he drops off the skull's brow onto the sand in front of you; thinner, the coat dusty to the knee, lace at his neck
    MV(KES, ['through_on', {'jump': [0, 3]}, 'through_off']), S('pbSEPlay("Anim/Earth4", 50, 110)\npfm_shake(1, 16, 6)'),
    S('pfm_pan_home(16)'), S('pfm_face(:player, "%s")' % KES), S('pfm_face("%s", :player)' % KES),
    say('KESTREL', "I saw them. Over your shoulder. The king and the chain.", KES),
    N('Kestrel', "I was in there before you, in the dark."),
    N('Kestrel', "I couldn't read it till you brought the lamp."),
    N('Kestrel', "I left the lighthouse the night of the Lowlight and I've been on the Hollow's trail ever since."),
    N('Kestrel', "They've got a cell out here. They came through Duneholt last week asking about old doors."),
    say('KESTREL', "And everywhere I go there's you. In front of me.", KES, 'angry'),
    N('Kestrel', "Getting there first. Leaning on things."),
    N('Kestrel', "Fight me. I need to know if I'm getting closer.")] + K3_BATTLE
RETRY = [S('pfm_fade_out(8)'), MV(KES, show('KESTREL', 2) + [{'script': 'moveto(66, 36)'}]), MV(SAHAR_M, [{'opacity': 255}]),
         MV('player', [{'script': 'moveto(66, 38)'}, 'turn_up']), S('pfm_tone(34, -6, -40, 10, 14)'),
         say('KESTREL', "Again. I'm not done being right.", KES)] + K3_BATTLE
LECTURE_K3 = [IF('pfm_get(:ch6_k3_tried)', RETRY, LECTURE)]

LETTER_LINES = [
    "\\c[3]\\PN,",
    "\\c[3]I found a way down! There was a ferryman on the Leach and he knew Dr Mott, and now I'm in Mirefen and it's BLUE at night, the whole marsh glows, and the noodles are the best I've ever had and Dr Mott says they'll kill me.",
    "\\c[3]I'm helping him with his seed-medicine. His ward is very quiet. I'll tell you about it when you come. I don't want to write it.",
    "\\c[3]Uncle Rowan wrote. He burned his hand on the kettle, he says, the same night as the Lowlight. His right hand, all across the palm. He's made tea every morning for forty years.",
    "\\c[3]He's been \"away on Warden business\" every time something happens. Every time. I counted.",
    "\\c[3]I'm being silly. I know I'm being silly.",
    "\\c[3]Come to Mirefen? Bring snacks.",
    "\\c[3]— Juno"]
LETTER = [
    {'wait': 30},
    # a Gale Post courier in goggles, out of breath, sand to the eyebrows
    MV(COURIER, show('NPC 14', 8) + [{'script': 'moveto($game_player.x, $game_player.y + 5)'}, 'through_on', {'speed': 5},
                                     'up', 'up', 'up', 'up', 'turn_up', 'through_off']),
    S('pfm_face(:player, "%s")' % COURIER), MV(COURIER, [{'jump': [0, 0]}]),
    N('Gale Post Courier', "\\PN? Thought so. You're the only one in Ossaria nobody can describe."),
    N('Gale Post Courier', "Letter. It's been chasing you since Lumen."),
    S('pbSEPlay("GUI menu open", 60, 80)'), {'wait': 16}] + LETTER_LINES + \
    quest("Earn the sixth badge in Mirefen, down the Leach Road into Nadir.") + [
    MV(COURIER, ['through_on', {'speed': 5}, 'down', 'down', 'down', 'down', 'down', {'opacity': 0}], wait=False),
    S('pfm_fade_in(30)'),                                                             # the evening tone lets go
    {'var': [STEP, 9]}, {'var': ['STORY_CHAPTER', 7]}]


def events_620():
    return [at(ev('Lecture, Archaeological', page([]), page(LECTURE_K3, cond=V(7), trigger='autorun'), page([], cond=V(8))), 1, 0),
            at(ev("Juno's Letter", page([]), page(LETTER, cond=V(8), trigger='autorun'), page([], cond=V(9))), 2, 0),
            walk_on(KES, 66, 33), walk_on(COURIER, 64, 44)]


def setpages_620():
    return {'Door in the Skull Trigger': [page([], through=True), page(DOOR, cond=V(5), trigger='touch', through=True),
                                          page([], cond=V(6), through=True)],
            SAHAR_M: [page([]), page(DOOR, 'SAHAR', 'up', cond=V(5)), page([], cond=V(6)),
                      page([say('SAHAR', "The desert keeps everything. It just doesn't keep it where you left it.", SAHAR_M)],
                           'SAHAR', 'up', cond=V(7)), page([], cond=V(9))],
            'To Ossuary of Dunes (624)': [page([S('pbSEPlay("Anim/Earth4", 40, 130)'), BACK], trigger='touch'),
                                          page([{'se': 'Door enter'}, S('pfm_fade_out(8)'),
                                                {'transfer': {'map': 624, 'x': 21, 'y': 37, 'dir': 'up'}}, S('pfm_fade_in(8)')],
                                               cond=V(6), trigger='touch')],
            'Kestrel (Ossuary Mouth K3)': [page([])],               # retired: K3 is "Lecture, Archaeological"
            'Kestrel K3 Trigger': [page([], through=True)],
            'Gale Post Courier (Ch6 Close)': [page([])]}            # retired: "Juno's Letter"


# ============================================================================================ 624 the Ossuary of Dunes
COMP = 'Sahar (companion)'
ENTRY = [
    # a hall cut into bone and sandstone, running down; boulders choke the side passages; Unown drift in the walls
    {'raw': [203, [8, 8, 3]]}, {'wait': 30}, S('pbSEPlay("Anim/Saint7", 40, 140)'), {'wait': 20}, S('pfm_pan_home(30)'),
    MV(COMP, show('SAHAR', 8)),
    "FIELD NOTES: \"THE OSSUARY OF DUNES — CAVE. Unown in the walls. They aren't hiding. They're the words.\"",
    "Larch, in the margin: \"Copy everything. Twice.\"",
    say('SAHAR', "The Unown are the inscription. They move.", COMP),
    N('Sahar', "That's why nobody could read it, before."),
    N('Sahar', "You have to wait for the sentence to come round."),
    S('pf_echo_follow(:convoy, ["%s"], spacing: 1)' % COMP),
    {'selfswitch': ['A', True]}]

MURALS = {
    'Mural I — The Gilded King': (1, [
        "A king in gold, on a throne under a sun, one hand raised as if weighing the sky itself. Below him, his city: towers and domes and a harbour full of ships. His face has been scratched out, very carefully, by someone with a chisel and a lot of time: all but the corner of a smile they missed."], [
        say('SAHAR', "A golden king. There's only one golden king in the old songs.", COMP),
        N('Sahar', "Nobody sings that verse any more."),
        N('Sahar', "Look at the posture. He isn't praying."),
        N('Sahar', "He's giving the sun an order.")]),
    'Mural II — Year of Two Weathers': (2, [
        "Two titans tearing at the land: one red, rising out of the earth with fire in its back; one blue, rising out of the sea with the tide in its arms. Between them, the king's armies, very small, holding chains."], [
        N('Sahar', "The Year of Two Weathers."),
        N('Sahar', "The song says the sky and the earth went to war."),
        N('Sahar', "This says somebody started it."),
        # she steps closer and traces the coastline behind the titans with one finger, very slowly
        S('pfm_face("%s", "Mural II — Year of Two Weathers")' % COMP), MV(COMP, ['step_anime_on', 'wait 60', 'step_anime_off']),
        say('SAHAR', "That's our western dunes. Before the Dry Tide was dry.", COMP, 'sad'),
        N('Sahar', "The sea came that far once.")]),
    'Mural III — The Eighteen-Lit Beast': (3, [
        "A great beast with a ring of eighteen lights round its body, radiant, enormous, and round it a chain: eighteen golden locks, one on each light. The king's tiny figure holds the end of the chain."], [
        say('SAHAR', "...Eighteen locks. One for each.", COMP, 'shocked', 'dots'),
        N('Sahar', "He didn't pray to it. He tried to lock it up.")]),
    'Mural IV — The Falling Lights': (4, [
        "The beast breaking apart. The eighteen lights falling out of it like rain, each one a different colour. Under them, the golden city tipping into the sea, towers first."], [
        say('SAHAR', "And the lights fell. Eighteen of them. Onto all of us.", COMP, 'sad'),
        N('Sahar', "And the city went into the sea, and three hundred years later we built Zenith on its roof and called it progress.")])}

RUBBING = [
    S('pf_echo_follow(:stop)'),
    # paper and a block of red wax from her satchel; she rubs the third mural, the chain, very fast, mouth set
    S('pfm_fade_out(10)'), MV(COMP, [{'script': 'moveto(34, 19)'}, 'turn_up']), MV('player', [{'script': 'moveto(33, 19)'}, 'turn_right']),
    S('pfm_fade_in(10)'),
    MV(COMP, ['step_anime_on'], wait=False), S('10.times { pbSEPlay("Anim/Wind1", 30, 175); pbWait(0.12) }'), MV(COMP, ['step_anime_off']),
    {'wait': 16},
    ITEM('DUNEHOLTRUBBING', 1, 'Duneholt Rubbing'),
    S('pfm_face("%s", :player)' % COMP),
    say('SAHAR', "I made two. Keep yours.", COMP),
    N('Sahar', "I burned the first one I ever made; I'm not burning a second."),
    {'switch': ['CH6_OSSUARY_DONE', True]}, {'var': [STEP, 7]},
    gone(COMP, 24)]                                                                  # she'll be outside, at the door
ALL4 = ' && '.join('pfm_get(:ch6_mural%d)' % i for i in (1, 2, 3, 4))


def mural_page(n, desc, sahar):
    return page(list(desc) + [IF('$game_variables[126] == 6', sahar + [S('pfm_set(:ch6_mural%d)' % n),
                                                                        IF(ALL4, RUBBING)])])


def events_624():
    unown = []
    for i, (x, y, span) in enumerate([(10, 16, 3), (30, 16, 3), (5, 22, 2), (38, 25, 2)], 1):
        p = page([], 'Followers/UNOWN', 'down', move='custom', through=True, step=True)
        p['graphic']['opacity'] = 150
        p['route'] = ['left'] * span + ['wait 20'] + ['right'] * span + ['wait 30']
        p['speed'], p['freq'] = 2, 3
        unown.append(at(ev('Unown in the wall %d' % i, p), x, y))
    return [at(ev('Into the Ossuary', page([]), page(ENTRY, cond=V(6), trigger='autorun'), page([], cond=V(6, self='A')),
                  page([], cond=V(7))), 1, 1),
            # a convoy follower: Through, so she never blocks the way back; no talk page (a Through action page only
            # runs when stood on, reach.py STANDON)
            at(ev(COMP, page([]), page([], 'SAHAR', 'up', cond=V(6), through=True), page([], cond=V(7))), 22, 37)] + unown


def setpages_624():
    out = {name: [mural_page(n, desc, sahar)] for name, (n, desc, sahar) in MURALS.items()}
    out['Sahar (Ossuary Sanctum)'] = [page([])]               # retired: she walks the hall with you (Sahar (companion))
    return out


# ============================================================================================ 206 -> 207, closed in Ch6
# The script's 207: "CLOSED FOR RESTORATION BY ORDER OF HIS EXCELLENCY. (The door is new. The lock is newer.)" Gemini's
# open gallery shows the Ossuary's four murals, which must stay the chapter's reveal; it opens with Chapter 7.
GALLERY_SHUT = ["CLOSED FOR RESTORATION BY ORDER OF HIS EXCELLENCY.",
                S('2.times { pbSEPlay("Player bump", 70, 55); pbWait(0.35) }'), BACK]     # a new door, a newer lock
GALLERY_OPEN = [{'se': 'Door enter'}, S('pfm_fade_out(8)'), {'transfer': {'map': 207, 'x': 38, 'y': 8, 'dir': 'left'}}, S('pfm_fade_in(8)')]


def setpages_206():
    return {'West to Mural Gallery': [page(GALLERY_SHUT, trigger='touch'), page(GALLERY_OPEN, cond=CHAP(7), trigger='touch')]}


# ============================================================================================ guarded exits to unbuilt maps
STAGE = {
    612: {"(West along the Crown Road cutting lies Candle Down and the pilgrimage cairns. Directorate rail-crews are inspecting a signal switch on the western trestle.)":
              shut('Player bump', N('Rail Ganger', "Western trestle's shut while they look at the signal switch. Candle Down'll keep."))},
    600: {"(North across the chalk rise lies the Highwold and Elowen's Crown Road. Wind-drifted scree has narrowed the pass above the broken viaduct.)":
              [S('pbSEPlay("Anim/Earth4", 50, 120)')] + shut('Player bump', N('Drover', "Scree's down across the pass. Nobody's going up to the Highwold till it's cleared."))},
    601: {"(West up the wind-scoured chalk canyon lies the Highwold. Red sandstorm drifts have choked the upper scree switchbacks.)":
              [S('pbSEPlay("Anim/Wind1", 70, 80)\npfm_shake(1, 10, 6)')] + shut('Player bump', N('Caravaneer', "Not up the switchbacks. Not in this. The red drifts have choked them."))},
    200: {"(Duneholt's West Gate out onto the Dry Tide is barred while dust-devils sweep the western flats.)":
              shut('Door slide', N('Gate Guard', "West Gate's barred while the dust-devils are out on the Dry Tide."), 60)}}


FILES = {180: '180_lumen_concourse.yaml', 200: '200_duneholt_terrace_bazaar.yaml', 203: '203_duneholt_sandgate.yaml',
         206: '206_electors_palace_hall.yaml',
         204: '204_duneholt_aquifer_quarter.yaml', 209: '209_sahars_dig_lab.yaml', 210: '210_duneholt_gym.yaml',
         213: '213_duneholt_gym_213.yaml', 600: '600_the_brass_dunes.yaml', 601: '601_the_rib_road.yaml',
         608: '608_lumen_lowlight_shattered.yaml', 612: '612_meridian_mainline.yaml', 620: '620_the_marrow_road.yaml',
         624: '624_ossuary_of_dunes.yaml'}


def spec_events(mid):
    import yaml
    for d in yaml.safe_load_all(open(os.path.join(SL.HERE, 'specs', FILES[mid]), encoding='utf-8')):
        if d and d.get('id') == mid: return d.get('events') or []


def main():
    print('map 608: %d events' % SL.patch(FILES[608], 608, events_608(), pages_608(), TAG))
    print('map 180: %d events' % SL.patch(FILES[180], 180, events_180(), None, TAG))
    print('map 612: %d events' % SL.patch(FILES[612], 612, events_612(), None, TAG))
    print('map 204: %d events' % SL.patch(FILES[204], 204, events_204(), pages_204(spec_events(204)), TAG))
    print('map 213: %d events' % SL.patch(FILES[213], 213, events_213(), None, TAG))
    print('map 620: %d events' % SL.patch(FILES[620], 620, events_620(), None, TAG))
    print('map 624: %d events' % SL.patch(FILES[624], 624, events_624(), None, TAG))
    sets = {612: setpages_612(), 203: setpages_203(), 206: setpages_206(), 209: setpages_209(), 620: setpages_620(),
            624: setpages_624()}
    sets.update(setpages_gym())
    for mid, table in sorted(sets.items()):
        names = [e.get('name') for e in spec_events(mid)]
        for name, pages in table.items():
            # Gemini keeps a multi-tile event's names unique with trailing spaces ("Trigger", "Trigger ", ...)
            same = sorted({n for n in names if n and n.rstrip() == name})
            if not same: raise SystemExit('story_ch6: no event %r on map %d' % (name, mid))
            n = sum(SL.set_pages(FILES[mid], mid, nm, pages, TAG) for nm in same)
            print('map %d: %-36s %d of %d event(s) changed' % (mid, name, n, len(same)))
    for mid, mapping in STAGE.items():
        print('map %d: stage directions %s' % (mid, sorted(SL.replace_lines(FILES[mid], mid, mapping, TAG).values())))


if __name__ == '__main__':
    main()
