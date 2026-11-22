#!/usr/bin/env python3
"""layouts/cindervault.py - Cindervault (Ch8, story/29_SCRIPT_CH8.md). For now: 255 the Tap Chamber [NEW], the
Caldera Crisis set piece under the Slag Ward (249).

A round iron-and-basalt room around Meridian Standard Tap No. 7: the pipe going down into a glowing magma pit, the gauge
ring on the north wall, Wick's hose at the old lava-channel sluices (west), Quent's damper valves (east) and the red
emergency lever under glass (north-east), in front of two Directorate soldiers. Built on tileset 61 "PF Rejuv Forge":
the earth cave kit (cdraw 'E') with the Magma autotile (rcompose.py).

The whole crisis is one autorun (CH8_STEP == 6, until CH8_CALDERA_DONE): the Hammer double battle, the detonator
(GO_LET_THEM_LISTEN), the three-way :ch8_caldera choice with its battle per branch, V110 and S120.

    python3 -I layouts/cindervault.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cavekit import Cave, FLOOR, MASS, P1
import cavekit as CK
from story_early import P

TID = 61
FIELD = 'VOLCANIC'


def say(who, e, t, emote=''): return P(who, e, t, emote)


def battle(call, field=FIELD, extra=()):
    """a story battle: the rules, then the call (TrainerBattle returns true on a win)"""
    rules = ['setBattleRule("field", :%s)' % field] + list(extra)
    return [{'script': '\n'.join(rules)}], call


def build_255():
    m = Cave(27, 21, 'E', seed=255, pool='Magma', tid=TID)
    m.STAIRS = CK.K.STAIRS_STONE
    m.room(13, 10, 10.5, 7.0, rough=0.25)                 # the round chamber
    m.box(11, 17, 15, 19)                                 # the service stair down from the Slag Ward
    m.box(10, 7, 16, 11, FLOOR, 'w')                      # the tap pit: magma round the pipe
    m.box(11, 6, 15, 6, FLOOR, 'w'); m.box(11, 12, 15, 12, FLOOR, 'w')
    m.box(2, 8, 4, 11)                                    # the old lava-channel sluices (west alcove)
    m.box(22, 8, 24, 11)                                  # Quent's valve bay (east alcove)
    m.box(19, 3, 22, 5)                                   # the emergency-lever niche (north-east)
    m.mass_at([(12, 9), (13, 9), (14, 9)])                # the pipe's collar (solid, in the pit)
    m.tidy()
    m.plan_cliffs(rows=2)
    return m


def crisis_commands():
    S = []
    S += [{'script': 'Prismfall.checkpoint'},
          "(The Tap Chamber: a round iron room around a pipe the width of a well, going down into rock that glows. A ring of gauges. A heat that pushes on your face. Three groups, and nobody listening to anybody.)",
          say('QUENT', 'happy', "Oh, it's YOU! The null reading! *giggling* Hold still, I've only got one probe."),
          say('QUENT', 'neutral', "Dr. Percival Quent, Meridian Applied Sciences. These are dampers. We fit them, the draw evens out, the pressure drops, and Tap Seven keeps running. Everyone keeps their lights. It's terribly simple."),
          say('WICK', 'neutral', "Hello."),
          say('WICK', 'sad', "We open the old channels and run Lake Sallow down them, onto the Imprint. The fever breaks. The mountain sleeps. And the forges go cold for a season, and the ash comes down on the Ashmarch like snow."),
          say('WICK', 'neutral', "It isn't kind. It's only safe."),
          "(Halfway up the iron ladder on the pipe, a figure in a grey cowl and a hammer-painted mask is strapping a brass-and-glass device to the collar. A Splitter. It's ticking.)",
          "Hammer Bomber: Stay back! All of you! The Hollow, the Meridian, the lot!",
          "Hammer Bomber: They'll cover up a fever. They can't cover up a mountain. When this goes, every screen in Velmora will show it, and THEN they'll listen.",
          say('WICK', 'angry', "There are families on the stairs, child."),
          "Hammer Bomber: There were families in the Lowlight!",
          {'script': 'setBattleRule("field", :%s)\nsetBattleRule("double")' % FIELD}]
    detonator = [
        "(The bomber is cornered on the ladder. The Splitter is still ticking. He holds out his hand: a brass detonator with one red key.)",
        "Hammer Bomber: You saw the Lowlight. I know you did. You were there.",
        "Hammer Bomber: Do it. They'll finally listen.",
        {'choices': ["(Turn the key.)", "(Throw it into the glow.)", "(Don't take it.)"], 'cancel': 3, 'branches': [
            [{'script': 'Prismfall.game_over(:GO_LET_THEM_LISTEN)'}],
            ["(It goes down the pipe's throat without a sound. The bomber watches it go.)", "Hammer Bomber: ...Coward.",
             say('WICK', 'sad', "No. That was the brave one, child. You'll understand in about ten years. I'm sorry it takes so long.")],
            ["Hammer Bomber: ...No. No, I can't either. I can't either.", "(He drops it. Quent's engineer stamps on it, hard, three times.)"]]},
        "(The bomber is gone up the stair. Quent unstraps the dead Splitter with two fingers and pockets it, humming. And the gauges keep climbing.)",
        say('LARCH', 'shocked', "The bomb was never the problem. The tap's still drawing. It's still going UP."),
        say('QUENT', 'happy', "Dampers, then! Help me fit them and we're done by supper!"),
        say('WICK', 'neutral', "Or help me open the channels and we're done by supper, and nobody's done anything to the mountain it didn't ask for."),
        "(Through the steam, on the Meridian side: a red lever under a glass cover. TAP 7 - EMERGENCY CLOSE - DIRECTORATE AUTHORISATION ONLY. Two Directorate soldiers stand in front of it.)",
        say('LARCH', 'neutral', "Three doctors. Your call, I'm afraid. I'm only a professor."),
    ]
    vent = [{'script': 'pf_choose(:ch8_caldera, :vent)'},
            say('QUENT', 'sad', "Oh, don't. Don't. Do you know what that'll do to my DATA?"),
            {'script': 'setBattleRule("field", :%s)\nsetBattleRule("fieldChange", [3, :ASHEN_WASTE, "Lake water roars down the old channels! The fire goes grey!"])' % FIELD},
            {'if': 'TrainerBattle.start(:MERIDIAN_QUENT, "Percival", 0)', 'then': [
                say('QUENT', 'neutral', 'Fine. Fine. I\'ll write it up as a natural experiment. "Subject vents mountain." Do you know how rare that is?'),
                "(Lake water roars down the stone. Steam fills the chamber, white and then grey, and then the grey comes down as ash, soft, everywhere.)",
                "(The gauges fall. Out of the red. Through the amber. Into the green.)",
                say('WICK', 'sad', "There. It's asleep. It'll be cross when it wakes up."),
                {'var': ['CINDERVAULT_STATE', 1]}, {'selfswitch': ['B', True]}], 'else': []}]
    dampers = [{'script': 'pf_choose(:ch8_caldera, :dampers)'},
               say('WICK', 'sad', "Then hold its mouth shut, if you must. It'll still have a fever."),
               "(The Hollow pick up their hose and go. But the Hammers come back down the stair with a third, and this time they're after the dampers.)",
               {'script': 'pbRegisterPartner(:MERIDIAN_QUENT, "Percival", 0)\nsetBattleRule("field", :%s)\nsetBattleRule("double")' % FIELD},
               {'if': 'TrainerBattle.start(:HOLLOW_GRUNT_M, "Hammer", 8, :HOLLOW_GRUNT_F, "Hammer", 8)', 'then': [
                   {'script': 'pbDeregisterPartner rescue ($PokemonGlobal.partner = nil)'},
                   "(The engineers lock the brass rings round the pipe. The draw evens out. The gauges fall to the amber and stay there, humming.)",
                   say('QUENT', 'happy', "Done by supper. I said! We should do this again. You're very good at holding things."),
                   {'var': ['CINDERVAULT_STATE', 2]}, {'selfswitch': ['B', True]}],
                'else': [{'script': 'pbDeregisterPartner rescue ($PokemonGlobal.partner = nil)'}]}]
    shutdown = [{'script': 'pf_choose(:ch8_caldera, :shutdown)'},
                "Directorate Lieutenant: That's Sovereign's property. Step back from it.",
                say('QUENT', 'shocked', "Oh, you CAN'T, that's - that's a whole tap, that's MONTHS-"),
                {'script': 'setBattleRule("field", :%s)\nsetBattleRule("double")' % FIELD},
                {'if': 'TrainerBattle.start(:MERIDIAN_QUENT, "Percival", 0, :MERIDIAN_DIRECTORATE, "Lieutenant", 8)', 'then': [
                    "(You break the glass and pull. The lever takes your whole weight. Somewhere far down, something very large stops turning.)",
                    "(The gauges shudder, and drop, and keep dropping, and stop in the green. The forges up the walls stay lit.)",
                    say('QUENT', 'sad', "Seven taps in the realm. Now six. Someone's going to be so cross with me."),
                    "Directorate Lieutenant: This goes to the Directorate. With your name on it.",
                    say('WICK', 'neutral', "Spell it right."),
                    {'var': ['CINDERVAULT_STATE', 0]}, {'selfswitch': ['B', True]}], 'else': []}]
    after = [{'if': "$game_self_switches[[255, @event_id, 'B']]", 'then': [
        "(Up the stair, out into the night. From the bell-tower, slowly, a single bell: one. All clear.)",
        {'switch': ['CH8_CALDERA_DONE', True]}, {'var': ['CH8_STEP', 6]},
        # on to Hearthguild Hall for the Light Stone; guarded until 244 is built (a missing map would crash)
        {'if': 'pbRgssExists?("Data/Map244.rxdata")', 'then': [{'transfer': {'map': 244, 'x': 10, 'y': 8, 'dir': 'up'}}], 'else': []}],
        'else': []}]
    S += [{'if': 'TrainerBattle.start(:HOLLOW_GRUNT_M, "Hammer", 8, :HOLLOW_GRUNT_F, "Hammer", 8)', 'then': detonator + [
        {'choices': ["Help Wick vent it.", "Help Quent fit the dampers.", "Shut the tap down."], 'cancel': 0,
         'branches': [vent, dampers, shutdown]}] + after, 'else': []}]
    return S


def events_255(m):
    E = m.events
    E += [
        {'type': 'warp', 'name': 'Up to the Slag Ward', 'at': [13, 19], 'to': {'map': 249, 'x': 20, 'y': 12, 'dir': 'up'}, 'se': 'Door exit'},
        {'type': 'event', 'name': 'Atmosphere', 'at': [0, 0], 'pages': [{'trigger': 'parallel', 'commands': [{'script': 'pfm_cave_light'}, {'wait': 12}]}]},
        {'type': 'event', 'name': 'The Caldera Crisis', 'at': [13, 16], 'pages': [
            {'commands': []},
            {'cond': {'var': ['CH8_STEP', 6]}, 'trigger': 'autorun', 'commands': crisis_commands() + [{'selfswitch': ['A', True]}]},
            {'cond': {'self': 'A'}, 'commands': []},
            {'cond': {'switch': 'CH8_CALDERA_DONE'}, 'commands': []}]},
        {'type': 'npc', 'name': 'Quent', 'at': [21, 10], 'sprite': 'trainer_SCIENTIST', 'dir': 'left', 'commands': [
            say('QUENT', 'happy', "The gauges are SO pretty when they're red. I mean that as a scientist.")]},
        {'type': 'npc', 'name': 'Wick', 'at': [5, 10], 'sprite': 'trainer_CHANNELER', 'dir': 'right', 'commands': [
            say('WICK', 'neutral', "Hello. Mind the hose. It's the only thing in here that isn't hot.")]},
        {'type': 'npc', 'name': 'Larch', 'at': [15, 15], 'sprite': 'trainer_PROFESSOR', 'dir': 'up', 'commands': [
            say('LARCH', 'neutral', "Don't touch anything that glows. Which is everything. Don't touch anything.")]},
        {'type': 'npc', 'name': 'Directorate soldier', 'at': [20, 6], 'sprite': 'trainer_COOLTRAINER_M', 'dir': 'down', 'commands': [
            "Directorate Soldier: Sovereign's property. Move along."]},
        {'type': 'npc', 'name': 'Directorate soldier b', 'at': [21, 6], 'sprite': 'trainer_COOLTRAINER_F', 'dir': 'down', 'commands': [
            "Directorate Soldier: Don't look at the lever. Looking's how it starts."]},
        {'type': 'npc', 'name': 'Hammer Bomber', 'at': [13, 13], 'sprite': 'trainer_BURGLAR', 'dir': 'up', 'commands': []},
        {'type': 'sign', 'name': 'Gauge ring', 'at': [8, 6], 'post': False, 'text':
         "MERIDIAN STANDARD TAP No. 7. DRAW: ------>|. The needles lean into the red like they're trying to get out of it."},
        {'type': 'sign', 'name': 'Emergency lever', 'at': [20, 4], 'post': False, 'text':
         "TAP 7 - EMERGENCY CLOSE. DIRECTORATE AUTHORISATION ONLY. BREAK GLASS. (The glass has a fingerprint on it already.)"},
    ]
    m.keep_clear |= {(13, 18), (13, 17), (13, 16), (13, 15), (13, 14), (13, 13), (5, 10), (21, 10), (15, 15), (20, 5), (21, 5), (8, 7), (20, 5)}


def dress_255(m):
    for name, x, y in (('cv_sluice', 3, 9), ('cv_sluice', 3, 10), ('cv_lever_l', 20, 3), ('cv_tools', 23, 9)):
        if name in CK.STAMPS:
            L = CK.STAMPS[name]['layers']; w, h = len(L[0][0]), len(L[0])
            if m.free(x, y, w, h, on='.') and not any((xx, yy) in m.keep_clear for xx in range(x, x + w) for yy in range(y, y + h)):
                m.put(name, x, y)
    # the tap itself: the pithead frame straddling the magma, the pipe column under it (forced: it stands in the pit)
    m.put('cv_frame', 12, 7)
    for y in (9, 10):
        m.over.append((2, 13, y, P1('cv_post')))
    m.solid_props(['E_rock0', 'E_rock0'], 4, seed=8)
    m.dress(6, seed=3)


def main():
    m = build_255(); events_255(m); dress_255(m); m.paint()
    os.makedirs('/tmp/cv255', exist_ok=True)
    m.preview('/tmp/cv255/p255.png', scale=1.0)
    head = {'id': 255, 'name': 'Cindervault - Tap Chamber', 'parent': 249, 'bgm': 'Cave', 'field': FIELD,
            'metadata': {'Name': 'Cindervault', 'MapPosition': [0, 24, 8], 'BattleBack': 'cave1'},
            'tone': [34, 4, -26, 10], 'fog': {'name': 'prismfall_cave', 'opacity': 30, 'blend': 1, 'zoom': 100, 'sx': 1, 'sy': 0},
            '_file': '255_cindervault_tap.yaml'}
    m.write(255, head, comment='# GENERATED by mapgen/layouts/cindervault.py (Ch8): the Tap Chamber, the Caldera Crisis (story/29_SCRIPT_CH8.md).\n'
                              '# Edit the layout script, not this file.\n')


if __name__ == '__main__':
    main()
