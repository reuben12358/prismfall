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
    # Use dark volcanic slate/basalt ('L') rock kit with PF Magma autotile for moody volcanic depth!
    m = Cave(27, 21, 'L', seed=255, pool='Magma', tid=TID)
    m.STAIRS = CK.K.STAIRS_STONE
    # Jagged, asymmetrical volcanic caldera chamber hollowed out of black void
    m.room(13, 11.5, 11.2, 7.0, rough=0.32)               # jagged basalt caldera walls
    m.box(11, 16, 15, 19)                                 # service stair approach from Slag Ward
    m.box(4, 9, 9, 16)                                    # west sluice cavern (Wick's old lava-channel sluices)
    m.box(17, 9, 22, 16)                                  # east damper cavern (Quent's geothermal dampers)
    m.box(9, 5, 20, 8)                                    # north Meridian bulkhead gauge gallery & NE emergency-lever niche

    # Carve dramatic jagged basalt promontories & volcanic rock buttresses into perimeter (ZERO boxy rectangle!)
    m.mass_at([
        (3, 8), (4, 8), (5, 7), (6, 6), (7, 5), (8, 5),
        (23, 8), (22, 8), (21, 7), (21, 6),
        (2, 11), (2, 12), (24, 11), (24, 12),
        (3, 16), (4, 17), (5, 17), (6, 17), (7, 17),
        (23, 16), (22, 17), (21, 17), (20, 17), (19, 17),
        (9, 18), (10, 18), (16, 18), (17, 18),
    ])

    # ---- Organically sculpted Central Magma Cauldron + Branching Subterranean Lava Fissures!
    # Central Tap No. 7 magma cauldron (x=10..16, y=9..13) with stepped basalt corners so it never reads as a flat box
    m.box(10, 10, 16, 12, FLOOR, 'w')
    m.box(11, 9, 15, 13, FLOOR, 'w')
    # Organic corner basalt piers jutting into the magma edge (anchors for Tap bollards & railings!)
    for px, py in ((10, 9), (16, 9), (10, 13), (16, 13)):
        m.cls[py, px] = '.'
    # West lava-channel sluice fissure (Wick's channel visually overlooking glowing molten magma!)
    for fx, fy in ((4, 14), (5, 14), (6, 14), (4, 15), (5, 15), (6, 15), (5, 16)):
        m.cls[fy, fx] = 'w'
    # East geothermal vent fissure (feeding Quent's heat dampers!)
    for fx, fy in ((20, 14), (21, 14), (22, 14), (20, 15), (21, 15), (22, 15), (21, 16)):
        m.cls[fy, fx] = 'w'
    # Small glowing NW volcanic fissure pocket under the cliff
    for fx, fy in ((5, 9), (6, 9)):
        m.cls[fy, fx] = 'w'

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
    vent = [
            say('QUENT', 'sad', "Oh, don't. Don't. Do you know what that'll do to my DATA?"),
            {'script': 'setBattleRule("field", :%s)\nsetBattleRule("fieldChange", [3, :ASHEN_WASTE, "Lake water roars down the old channels! The fire goes grey!"])' % FIELD},
            {'if': 'TrainerBattle.start(:MERIDIAN_QUENT, "Percival", 0)', 'then': [
                {'script': 'pf_choose(:ch8_caldera, :vent)'},
                say('QUENT', 'neutral', 'Fine. Fine. I\'ll write it up as a natural experiment. "Subject vents mountain." Do you know how rare that is?'),
                "(Lake water roars down the stone. Steam fills the chamber, white and then grey, and then the grey comes down as ash, soft, everywhere.)",
                "(The gauges fall. Out of the red. Through the amber. Into the green.)",
                say('WICK', 'sad', "There. It's asleep. It'll be cross when it wakes up."),
                {'var': ['CINDERVAULT_STATE', 1]}, {'selfswitch': ['B', True]}], 'else': []}]
    dampers = [
               say('WICK', 'sad', "Then hold its mouth shut, if you must. It'll still have a fever."),
               "(The Hollow pick up their hose and go. But the Hammers come back down the stair with a third, and this time they're after the dampers.)",
               {'script': 'pbRegisterPartner(:MERIDIAN_QUENT, "Percival", 0)\nsetBattleRule("field", :%s)\nsetBattleRule("double")' % FIELD},
               {'if': 'TrainerBattle.start(:HOLLOW_GRUNT_M, "Hammer", 8, :HOLLOW_GRUNT_F, "Hammer", 8)', 'then': [
                   {'script': 'pbDeregisterPartner rescue ($PokemonGlobal.partner = nil)'},
                   {'script': 'pf_choose(:ch8_caldera, :dampers)'},
                   "(The engineers lock the brass rings round the pipe. The draw evens out. The gauges fall to the amber and stay there, humming.)",
                   say('QUENT', 'happy', "Done by supper. I said! We should do this again. You're very good at holding things."),
                   {'var': ['CINDERVAULT_STATE', 2]}, {'selfswitch': ['B', True]}],
                'else': [{'script': 'pbDeregisterPartner rescue ($PokemonGlobal.partner = nil)'}]}]
    shutdown = [
                "Directorate Lieutenant: That's Sovereign's property. Step back from it.",
                say('QUENT', 'shocked', "Oh, you CAN'T, that's - that's a whole tap, that's MONTHS-"),
                {'script': 'setBattleRule("field", :%s)\nsetBattleRule("double")' % FIELD},
                {'if': 'TrainerBattle.start(:MERIDIAN_QUENT, "Percival", 0, :MERIDIAN_DIRECTORATE, "Lieutenant", 8)', 'then': [
                    {'script': 'pf_choose(:ch8_caldera, :shutdown)'},
                    "(You break the glass and pull. The lever takes your whole weight. Somewhere far down, something very large stops turning.)",
                    "(The gauges shudder, and drop, and keep dropping, and stop in the green. The forges up the walls stay lit.)",
                    say('QUENT', 'sad', "Seven taps in the realm. Now six. Someone's going to be so cross with me."),
                    "Directorate Lieutenant: This goes to the Directorate. With your name on it.",
                    say('WICK', 'neutral', "Spell it right."),
                    {'var': ['CINDERVAULT_STATE', 0]}, {'selfswitch': ['B', True]}], 'else': []}]
    after = [{'if': "$game_self_switches[[255, @event_id, 'B']]", 'then': [
        "(Up the stair, out into the night. From the bell-tower, slowly, a single bell: one. All clear.)",
        {'switch': ['CH8_CALDERA_DONE', True]}, {'var': ['CH8_STEP', 6]}, {'selfswitch': ['A', True]},
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
        # 249 (the Slag Ward) isn't built yet: a plain warp to a missing map crashes, so guard it
        {'type': 'event', 'name': 'Up to the Slag Ward', 'at': [13, 19], 'pages': [{'trigger': 'touch', 'commands': [
            {'if': 'pbRgssExists?("Data/Map249.rxdata")', 'then': [{'transfer': {'map': 249, 'x': 20, 'y': 12, 'dir': 'up'}}],
             'else': ["(The stair up to the Slag Ward is roped off. Not built yet.)"]}]}]},
        {'type': 'event', 'name': 'Atmosphere', 'at': [0, 0], 'pages': [{'trigger': 'parallel', 'commands': [{'script': 'pfm_cave_light'}, {'wait': 12}]}]},
        {'type': 'event', 'name': 'The Caldera Crisis', 'at': [13, 16], 'pages': [
            {'commands': []},
            # Gym 7 won (CH8_STEP 5) opens the crisis. Self A is set only once it's resolved (see `after`), so a
            # whiteout or a lost branch battle replays the crisis from the checkpoint instead of bricking Ch8.
            {'cond': {'var': ['CH8_STEP', 5]}, 'trigger': 'autorun', 'commands': crisis_commands()},
            {'cond': {'self': 'A'}, 'commands': []},
            {'cond': {'switch': 'CH8_CALDERA_DONE'}, 'commands': []}]},
        # Tightened cinematic staging: all actors sit clearly inside the 16x12 camera viewport from (13, 17)
        {'type': 'npc', 'name': 'Quent', 'at': [18, 13], 'sprite': 'trainer_SCIENTIST', 'dir': 'left', 'commands': [
            say('QUENT', 'happy', "The gauges are SO pretty when they're red. I mean that as a scientist.")]},
        {'type': 'npc', 'name': 'Wick', 'at': [8, 13], 'sprite': 'trainer_CHANNELER', 'dir': 'right', 'commands': [
            say('WICK', 'neutral', "Hello. Mind the hose. It's the only thing in here that isn't hot.")]},
        {'type': 'npc', 'name': 'Larch', 'at': [15, 16], 'sprite': 'trainer_PROFESSOR', 'dir': 'up', 'commands': [
            say('LARCH', 'neutral', "Don't touch anything that glows. Which is everything. Don't touch anything.")]},
        {'type': 'npc', 'name': 'Directorate soldier', 'at': [18, 10], 'sprite': 'trainer_COOLTRAINER_M', 'dir': 'down', 'commands': [
            "Directorate Soldier: Sovereign's property. Move along."]},
        {'type': 'npc', 'name': 'Directorate soldier b', 'at': [19, 10], 'sprite': 'trainer_COOLTRAINER_F', 'dir': 'down', 'commands': [
            "Directorate Soldier: Don't look at the lever. Looking's how it starts."]},
        {'type': 'npc', 'name': 'Hammer Bomber', 'at': [13, 14], 'sprite': 'trainer_BURGLAR', 'dir': 'down', 'commands': []},
        {'type': 'sign', 'name': 'Gauge ring', 'at': [11, 8], 'post': False, 'text':
         "MERIDIAN STANDARD TAP No. 7. DRAW: ------>|. The needles lean into the red like they're trying to get out of it."},
        {'type': 'sign', 'name': 'Emergency lever', 'at': [18, 9], 'post': False, 'text':
         "TAP 7 - EMERGENCY CLOSE. DIRECTORATE AUTHORISATION ONLY. BREAK GLASS. (The glass has a fingerprint on it already.)"},
    ]
    m.keep_clear |= {
        (13, 19), (13, 18), (13, 17), (13, 16), (13, 15), (13, 14), (12, 14), (14, 14),
        (8, 13), (9, 13), (18, 13), (17, 13), (15, 16), (18, 10), (19, 10),
        (11, 8), (12, 8), (13, 8), (14, 8), (18, 9), (19, 9),
        # Continuous walkway loop around the magma pit
        (9, 9), (9, 10), (9, 11), (9, 12), (9, 14), (10, 14), (11, 14), (15, 14), (16, 14), (17, 14),
        (17, 12), (17, 11), (17, 10), (17, 9), (16, 8), (15, 8), (10, 8),
    }


def _place_stamp_over(m, name, x, y, base_z=1, top_z=2, top_rows=0, solid=True):
    """Force-composite a PF Rejuv stamp into m.over (works cleanly over magma or custom decking)."""
    L = CK.STAMPS[name]['layers']
    h, w = len(L[0]), len(L[0][0])
    for dy in range(h):
        for dx in range(w):
            for sz in (0, 1, 2):
                t = int(L[sz][dy][dx])
                if t:
                    tz = top_z if (dy < top_rows or sz == 2) else base_z
                    m.over.append((tz, x + dx, y + dy, t))
            if solid:
                m.taken[y + dy, x + dx] = True


def _steel_deck_cells(m):
    """Sculpted octagonal/cruciform riveted-steel catwalk gantry framing the central magma cauldron
    and extending walkways to the West Sluice Bay, East Damper Bay, and South Slag Ward approach."""
    cells = []
    for y in range(7, 19):
        for x in range(7, 20):
            if m.cls[y, x] != '.' or m.cliff[y, x]:
                continue
            # Core octagonal gantry ring around the magma pit (chamfering corners!)
            in_ring = (8 <= x <= 18 and 8 <= y <= 15) and (x, y) not in {(8, 8), (8, 15), (18, 15)}
            # South catwalk bridge down toward the Slag Ward stairs (x=11..15, y=15..17)
            in_south = (11 <= x <= 15 and 15 <= y <= 17)
            # East emergency-lever catwalk extension (x=17..19, y=8..10)
            in_ne = (17 <= x <= 19 and 8 <= y <= 10)
            # West & East bridge arms to Wick (8,13) and Quent (18,13)
            in_arms = (y in (11, 12, 13) and (x == 7 or x == 19))
            if in_ring or in_south or in_ne or in_arms:
                cells.append((x, y))
    return cells


def dress_255(m):
    # ---- 1. Industrial floor grates, heavy high-voltage conduits & volcanic fissures
    grate, cab_h, cab_v = P1('lm_grate'), P1('lm_cable_h'), P1('lm_cable_v')
    for x, y in ((11, 15), (15, 15), (9, 11), (17, 11), (10, 8), (16, 8), (12, 17), (14, 17), (9, 13), (17, 13)):
        if m.cls[y, x] == '.' and not m.cliff[y, x]:
            m.over.append((1, x, y, grate))
    for x in (8, 9):
        m.over.append((1, x, 11, cab_h)); m.over.append((1, x, 12, cab_h))
    for x in (17, 18):
        m.over.append((1, x, 11, cab_h)); m.over.append((1, x, 12, cab_h))
    for y in (15, 16, 17):
        m.over.append((1, 11, y, cab_v)); m.over.append((1, 15, y, cab_v))

    # Molten basalt cracks, glowing embers & volcanic steam wisps scattered around the outer caldera floor!
    for x, y, k in ((7, 14, 0), (8, 15, 1), (18, 15, 0), (19, 14, 1), (10, 17, 0), (16, 17, 1),
                    (7, 9, 1), (8, 8, 0), (19, 16, 0), (7, 16, 1)):
        if m.cls[y, x] == '.' and not m.cliff[y, x] and (x, y) not in m.keep_clear:
            m.over.append((1, x, y, P1('gd_crack%d' % k)))
    for i, (x, y) in enumerate(((4, 12), (7, 10), (8, 16), (10, 16), (16, 16), (19, 15), (22, 12), (20, 10), (9, 15), (17, 15))):
        if m.cls[y, x] == '.' and not m.cliff[y, x] and (x, y) not in m.keep_clear:
            m.over.append((1, x, y, P1('wr_ember%d' % (i % 3))))
    for i, (x, y) in enumerate(((6, 13), (20, 13), (11, 18), (15, 18), (5, 11), (21, 10))):
        if m.cls[y, x] == '.' and not m.cliff[y, x] and (x, y) not in m.keep_clear:
            m.over.append((2, x, y, P1('wr_steam%d' % (i % 3))))

    # ---- 2. Colossal Meridian Standard Tap No. 7 rising straight out of the molten cauldron!
    _place_stamp_over(m, 'lm_pylon', 12, 8, base_z=1, top_z=2, top_rows=2, solid=True)
    _place_stamp_over(m, 'cv_ladder', 14, 10, base_z=1, top_z=2, top_rows=1, solid=True)
    # Heavy yellow-steel safety bollards anchored on the 4 jutting basalt piers at the corners of the magma pit!
    for bx, by in ((10, 9), (16, 9), (10, 13), (16, 13)):
        _place_stamp_over(m, 'lm_bollard', bx, by, base_z=1, top_z=2, top_rows=0, solid=True)
    # Billowing volcanic steam plumes rising from the magma throat
    _place_stamp_over(m, 'lm_steam0', 11, 9, base_z=2, top_z=2, top_rows=2, solid=False)
    _place_stamp_over(m, 'lm_steam1', 15, 9, base_z=2, top_z=2, top_rows=2, solid=False)
    # Brass safety railings overlooking the magma drop (south lip leaving (13, 14) open for Hammer Bomber + north lip!)
    m.over.append((1, 11, 13, P1('lm_railing_w')))
    m.over.append((1, 12, 13, P1('lm_railing_m')))
    m.over.append((1, 14, 13, P1('lm_railing_m')))
    m.over.append((1, 15, 13, P1('lm_railing_e')))
    m.over.append((1, 11, 9, P1('lm_railing_w')))
    m.over.append((1, 15, 9, P1('lm_railing_e')))

    # ---- 3. West Sluice Cavern (Wick's old lava-channel sluices overlooking the SW magma fissure!)
    # Replaces the old awkward flat lm_vault square with a rugged rotary iron sluice pump & crimson valves!
    _place_stamp_over(m, 'cv_pump', 5, 10, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'cv_sluice_hi', 7, 11, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'cv_sluice', 6, 12, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'cv_sluice', 7, 12, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'lm_gearbox', 5, 12, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'lm_steam0', 4, 12, base_z=2, top_z=2, top_rows=2, solid=False)
    _place_stamp_over(m, 'lm_steam1', 5, 14, base_z=2, top_z=2, top_rows=2, solid=False)

    # ---- 4. East Damper Bay (Quent's Meridian damper generators & racks overlooking the SE vent fissure!)
    _place_stamp_over(m, 'lm_gen', 19, 11, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'lm_rack', 21, 11, base_z=1, top_z=2, top_rows=1, solid=True)
    _place_stamp_over(m, 'cv_tools', 20, 13, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'lm_junction_on', 19, 13, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'lm_steam1', 21, 13, base_z=2, top_z=2, top_rows=2, solid=False)

    # ---- 5. North Riveted-Iron Meridian Bulkhead, Gauge Ring (11,8) & NE Emergency Lever (18,9)
    # Sleek industrial consoles, glowing gauges & alert lamps bolted cleanly into the dark steel north bulkhead
    # (replaces glaring neon-pink/cyan boxes on sandy dirt!)
    _place_stamp_over(m, 'lm_desk', 10, 7, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'lm_desk', 14, 7, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'lm_junction_on', 12, 7, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'lm_alarm_on', 9, 7, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'lm_alarm_on', 16, 7, base_z=1, top_z=1, top_rows=0, solid=True)
    # Warm industrial wall lamps along the riveted north bulkhead
    for wx in (10, 13, 15, 18):
        m.over.append((2, wx, 6, P1('cv_walllamp')))
    # Emergency lever right behind the two Directorate soldiers at (18..19, 10)
    _place_stamp_over(m, 'cv_lever_l', 18, 9, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'lm_alarm_on', 19, 9, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'lm_railing_w', 17, 8, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'lm_railing_m', 18, 8, base_z=1, top_z=1, top_rows=0, solid=True)
    _place_stamp_over(m, 'lm_railing_e', 19, 8, base_z=1, top_z=1, top_rows=0, solid=True)

    # ---- 6. Forge Braziers, Industrial Lanterns, Heavy Steel Entry Bollards & Volcanic Lighting!
    for bx, by in ((11, 17), (15, 17)):
        if m.cls[by, bx] == '.' and (bx, by) not in m.keep_clear:
            _place_stamp_over(m, 'lm_bollard', bx, by, base_z=1, top_z=2, top_rows=0, solid=True)
    for bx, by in ((10, 15), (16, 15), (8, 9), (20, 9)):
        if m.cls[by, bx] == '.' and (bx, by) not in m.keep_clear:
            _place_stamp_over(m, 'fw_brazier', bx, by - 1, base_z=1, top_z=2, top_rows=1, solid=True)
    for lx, ly in ((11, 18), (15, 18)):
        if m.cls[ly, lx] == '.' and (lx, ly) not in m.keep_clear:
            _place_stamp_over(m, 'cv_lamp_on', lx, ly - 1, base_z=1, top_z=2, top_rows=1, solid=True)

    # Glowing amber furnace heat halos (pf_glow, p0/r5 overhead) across the magma cauldron, fissures & braziers!
    for gx, gy in ((11, 10), (14, 10), (12, 11), (10, 14), (16, 14), (8, 8), (20, 8),
                   (5, 9), (5, 14), (20, 14), (11, 17), (15, 17)):
        m.stamps.append(('pf_glow', gx, gy))
    # Subtle volcanic heat shafts descending from the caldera vent onto Meridian Tap No. 7
    for sx, sy in ((11, 7), (14, 7)):
        m.stamps.append(('cv_shaft', sx, sy))

    m.solid_props(['E_rock0', 'E_rock1'], 6, seed=8)
    m.dress(6, seed=3)


def apply_steel_deck(m):
    """Apply riveted steel catwalk gantry & dark-iron Meridian north bulkhead cleanly AFTER Cave.paint()."""
    qf0, qf1 = P1('Q_f0'), P1('Q_f1')
    floorpatch_ids = {P1(k) for k in CK.STAMPS if k.startswith(('E_floorpatch_', 'E_fd', 'L_floorpatch_', 'L_fd'))}
    for x, y in _steel_deck_cells(m):
        m.L[0, y, x] = qf0 if (x + y) % 2 == 0 else qf1
        if int(m.L[1, y, x]) in floorpatch_ids:
            m.L[1, y, x] = 0
    # Clad the north gauge gallery cliff face (x=9..19, y=5..6) in solid dark riveted-iron Meridian bulkhead plates,
    # reserving hazard stripes (Q_basem) deliberately for the Emergency Lever bay (x=18..19)!
    q_lip, q_face, q_base = P1('Q_lipm'), P1('Q_facem'), P1('Q_basem')
    for x in range(9, 20):
        if m.cliff[5, x]:
            m.L[0, 5, x] = q_lip
            m.L[1, 5, x] = 0
        if m.cliff[6, x]:
            m.L[0, 6, x] = q_base if x in (18, 19) else q_face
            m.L[1, 6, x] = 0
    # Guarantee 0 passability hits on Tileset 61
    import passguard as PG
    PG.guard(m.L, TID)


def main():
    m = build_255(); events_255(m); dress_255(m); m.paint(); apply_steel_deck(m)
    os.makedirs('/tmp/cv255', exist_ok=True)
    m.preview('/tmp/cv255/p255.png', scale=1.0)
    head = {'id': 255, 'name': 'Cindervault - Tap Chamber', 'parent': 249, 'bgm': 'Cave', 'field': FIELD,
            'metadata': {'Name': 'Cindervault', 'SnapEdges': True, 'MapPosition': [0, 24, 8], 'BattleBack': 'cave1'},
            'tone': [28, 2, -22, 12], 'fog': {'name': 'prismfall_cave', 'opacity': 30, 'blend': 1, 'zoom': 100, 'sx': 1, 'sy': 0},
            '_file': '255_cindervault_tap.yaml'}
    m.write(255, head, comment='# GENERATED by mapgen/layouts/cindervault.py (Ch8): the Tap Chamber, the Caldera Crisis (story/29_SCRIPT_CH8.md).\n'
                              '# Edit the layout script, not this file.\n')


if __name__ == '__main__':
    main()
