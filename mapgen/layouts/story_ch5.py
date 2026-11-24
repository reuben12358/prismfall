"""story_ch5: the scripted events of story/24_SCRIPT_CH5.md that live on map builder 15's Lumen maps (180, 181, 608,
182, 183, 185, 186, 582, 951, 952), written out by hand from the script ("Map events needed (Chapter 5)").
Layouts seat them with `place(mid, name, (x, y))`; `unplaced(mid)` lists anything a layout forgot.
Counter: V125 CH5_STEP (design/FLAGS.md).  Conventions as story_early (portrait lines \\pf[ID,expr]Name: text)."""
import copy
import story_early as SE
from story_early import P, N, S, IF, CH, MV, SW, page, ev, sign
from rkit import P1
S_SPLICE, S_BOXES, S_BLACKOUT, V_BOXES = 422, 423, 424, 321

SE.NAMES.update({'ROOK': 'Rook', 'DEX': 'Dex', 'VALEN': 'Valen', 'MARCHETTI': 'Marchetti', 'SABLE': 'Sable',
                 'MOURNER': 'The Mourner', 'QUENT': 'Quent', 'HOLLIS': 'Hollis', 'RENATA': 'Councillor Sallow'})
STEP = 'CH5_STEP'
EVENTS = {}
SPR = {'DEX': 'NPC 02', 'ROOK': 'trainer_ROCKER', 'JUNO': 'trainer_RIVAL2', 'LARCH': 'trainer_PROFESSOR', 'VOSS': 'trainer_GENTLEMAN',
       'VALEN': 'trainer_GENTLEMAN', 'OFFICER': 'trainer_SCIENTIST'}


def add(mid, *evs):
    for e in evs: EVENTS.setdefault(mid, {})[e['name']] = e


def place(mid, name, at, **kw):
    e = copy.deepcopy(EVENTS[mid][name]); e['at'] = list(at); e.update(kw); EVENTS[mid][name]['_placed'] = True
    e.pop('_placed', None)
    return e


def unplaced(mid):
    return [n for n, e in EVENTS.get(mid, {}).items() if not e.get('_placed')]


def talk(name, sprite, d, lines, again=None, cond=None, gone=None):
    """a townsperson: lines, an optional (again) page, shown only while cond holds and gone after `gone` (var >=)"""
    ps = [page(list(lines) + ([{'selfswitch': ['A', True]}] if again else []), sprite, d, cond=cond)]
    if again: ps.append(page(list(again), sprite, d, cond=dict(cond or {}, self='A')))
    if gone: ps.append(page([], cond={'var': [STEP, gone]}))
    return ev(name, *ps)


def once(name, cmds, trigger='touch', cond=None, sprite='', d='down'):
    return ev(name, page(list(cmds) + [{'selfswitch': ['A', True]}], sprite, d, cond=cond, trigger=trigger),
              page([], cond=dict(cond or {}, self='A')))


def vcond(n): return {'var': [STEP, n]}


# ===================================================================================================== 180 the Concourse
add(180,
    ev('Arrival', page([], cond=None),
       page(["(White-stone boulevards between towers of glass and brass. Holograms of the Meridian sunburst turn slowly over the plaza. Rotom drones zip overhead with parcels. An airship slides across the sky, so low its shadow crosses the fountain. Every window is lit, and it's noon.)",
             P('JUNO', 'shocked', "..."),
             P('JUNO', 'happy', "Everything's ON. Everything's on at the same TIME."),
             N('Juno', "In Verdance you light a lamp when it gets dark and you're careful with it. Here they've just left everything on. Like it's free."),
             N('Pin-seller', "It IS free! Ten years of free! Light for Everyone! Anniversary pins, only ₽200!"),
             P('JUNO', 'deadpan', "The light's free. The pin's two hundred."),
             {'selfswitch': ['A', True]}], cond=vcond(3), trigger='autorun'),
       page([], cond={'var': [STEP, 3], 'self': 'A'})),
    talk('Pin-seller', 'NPC 17', 'down', [N('Pin-seller', "Anniversary pins! Ten years of light! Only ₽200! Light for Everyone!")]),
    sign('Plaza banner', "TEN YEARS OF LIGHT. LIGHT FOR EVERYONE. - MERIDIAN CONCORD", post=False),
    ev('Gym sign', page(["CIRCUIT GYM: CLOSED FOR FILMING. \"Warden on location: THE LOWLIGHT. Stay charged! - R.C.\"",
                         "A hologram of Rook winks at you. It's on a loop. It winks every four seconds.", MV(-1, ['down'])], trigger='touch'),
       page([], cond=vcond(5))),
    talk('Gym attendant', 'NPC 21', 'down', [N('Gym attendant', "Closed for filming! Rook's down in the Lowlight doing a community special. East side, down the steps. You can't miss the floodlights.")], gone=5),
    ev('Lift-grille', page(["LIFT-GRILLE: A grille in the pavement over a shaft that goes down out of sight. The air coming up is warm and tastes of pennies. Painted on the inside of the bars, where you'd only see it looking down: a grey ring, broken at the top."])),
    ev('Grille scene', page(["(A Nadir kid in a cut-down boiler suit is sitting on the grille. A Zenith officer in white-and-gold walks up.)",
                             N('Zenith Officer', "You. Back downstairs."), N('Nadir Kid', "I'm just sitting."), N('Zenith Officer', "Sit downstairs."),
                             "(The kid drops through a gap in the bars and is gone.)",
                             P('JUNO', 'angry', "He wasn't doing anything!"),
                             N('Zenith Officer', "It's the anniversary, miss. Nadir's very welcome to watch the fireworks. From Nadir."),
                             S('PrismfallPuzzles.event("Nadir Kid").erase rescue nil'), {'selfswitch': ['A', True]}], trigger='touch', cond=vcond(3)),
       page([], cond={'var': [STEP, 3], 'self': 'A'})),
    talk('Nadir Kid', 'NPC 09', 'down', ["(He's sitting on the grille, swinging his boots over the shaft.)"], gone=4),
    talk('Zenith Officer', SPR['OFFICER'], 'left', [N('Zenith Officer', "Move along. Anniversary. Big day. Lots of light.")]),
    talk('Office Worker', 'NPC 14', 'down', [N('Office Worker', "I haven't seen the stars in ten years. I don't miss them. I can see the Spire from my bed.")]),
    talk('Old Man', 'NPC 03', 'left', [N('Old Man', "I remember Lumen before the Lattice. Gas lamps and smog. It was worse. I just liked it more.")]),
    talk('Airship Spotter', 'NPC 16', 'up', [N('Airship Spotter', "That's the Sallow Line's Dauntless. Then the Meridian Courier. Then — no, that's a cloud. They're getting hard to tell apart.")]),
    ev('Rotom Drone', page([N('Rotom Drone', "(bzzt) PARCEL FOR: NOT YOU. (bzzt)")], move='random', tile=P1('lm_drone'))),
    talk('Tourist from Briarwick', 'NPC 19', 'right', [N('Tourist from Briarwick', "Everything's so bright I keep thinking it's morning. I've had four breakfasts.")]),
    talk('Meridian Lineman', 'NPC 25', 'down', [N('Meridian Lineman', "The Spire's lit gold for the gala. You can see it from the Crownwall, they say. And the Sovereign's coming. Valen Corrigan. HERE.")]),
    talk('Street Performer', 'NPC 22', 'down', [N('Street Performer', "Neon Grid's in the pavement, kid. Every cobble's on the circuit. Electric moves sing here, and anything that conducts sings louder.")]),
    ev('Fizzbolt machine', page(["A Fizzbolt vending machine, humming to itself. A brass plate: COMPLIMENTS ACCEPTED."])),
    ev('P-3NNY kiosk', page(["P-3NNY: GREETINGS, CITIZEN. LUMEN THANKS YOU FOR YOUR LIGHT. (The kiosk's screen shows a smiling sunburst.)"])),
    talk('Council guard', 'trainer_SCIENTIST', 'down', [N('Meridian Security', "Council Ward's closed to the public for the anniversary. Councillors only. Try again in Act Two. ...I mean, next week.")]),
    talk('Skyport guard', 'trainer_SCIENTIST', 'down', [N('Meridian Security', "Skyport Terrace is ticketed passengers only today. The Dauntless is coming in for the gala.")]),
    talk('Spire guard', 'trainer_SCIENTIST', 'down', [N('Meridian Security', "Meridian Spire. The gala is by invitation, tomorrow night. Lobby's open to visitors.")]),
    sign('Lowlight stairs', "THE LOWLIGHT. STEPS DOWN. (Someone has scratched under it: MIND THE SHADOW.)", post=False),
    sign('Founders statue', "THE FOUNDERS' LAMP. \"Light is work.\" Unveiled in the First Year of Light.", post=False),
)

# ===================================================================================================== 181 the Lowlight
RES = [  # the twelve (name, sprite, dir, lines, glass piece on 608, glass inspect line)
    ('Marta Vell', 'NPC 11', 'up', ["(pegging out washing between two windows) Mind the sheets, love. Everything I own is on this line. Including my husband's dignity. (A pair of very large long johns.)"], 0),
    ('Old Jory', 'NPC 03', 'down', ["(the cobbler, laughing on his step) Hah! Rook Calder in the Lowlight! Ten years that Spire's been up there and this is the first time it's sent anybody DOWN. (He laughs till he coughs.)"], 4),
    ('Nessa', 'NPC 18', 'down', ["(on the hopscotch) You can't stand on seven. Seven's the Spire. Everybody knows you can't stand on the Spire."], 5),
    ('Hob Carrow', 'NPC 25', 'down', ["(the lamp-tender, up a ladder) These are the old gas lamps. The Lattice ones don't reach the Lowlight; the shadow eats them. So I light ours by hand, every dusk. Ten years of light! Not down here."], 6),
    ('Linesman Aldo Fisk', 'NPC 20', 'left', ["(helmet under his arm) Twelve-hour shift on the Spire feeds. They've had the Plate vault running hot all month for the gala. My hands still hum. Listen. (He holds out his hand. It does, faintly.)"], 1),
    ('Sukie', 'NPC 06', 'right', ["(the lift-girl at the Nadir grille) Lift down's at six, love, checkpoint or no checkpoint. Tell your friend in the flowers to hold her skirts, the draught's terrible."], 3),
    ('Ilo', 'NPC 04', 'right', ["Ilo: We got married Tuesday.", "Mattie: He keeps telling people.", "Ilo: I'll stop telling people when I stop being married.", "Mattie: ...That's a very long time.", "Ilo: That's the idea."], 1),
    ('Mattie', 'NPC 15', 'left', ["Mattie: He keeps telling people we got married Tuesday. It was Tuesday. He's not wrong."], 0),
    ('Gran Osk', 'NPC 27', 'down', ["(feeding a Pidove) Forty years I've fed the birds in the Spire's shadow. Same birds, I'm sure of it. Look at that one. He's got my late husband's face."], 7),
    ('Benno', 'NPC 10', 'down', ["(the noodle cart) Slag-fried noodles! Nadir recipe, topside prices! That's a joke. They're Nadir prices. Nobody topside buys noodles in the shadow."], 1),
    ('Mr Imrie', 'NPC 23', 'down', ["(a schoolteacher on a bench, marking) \"What does light mean to you?\" For the anniversary. Eleven of my pupils wrote \"free\". One wrote \"my mum's face when she gets home\". Guess which one gets the prize."], 4),
]
GLASS_LINE = {  # 608: inspect lines for the twelve in glass (the script's "Twelve"; placeholder text where it is still being written)
    'Marta Vell': "Marta Vell, arms up to the line. The long johns are glass too.",
    'Old Jory': "Old Jory, mid-laugh, his head thrown back. The cough never came.",
    'Nessa': "Nessa, on one leg. She's on six. Not seven. She never stood on the Spire.",
    'Hob Carrow': "Hob Carrow, up his ladder, his taper an inch from the gas lamp.",
    'Linesman Aldo Fisk': "Aldo Fisk, holding out his hand. It doesn't hum any more.",
    'Sukie': "Sukie at the grille, her hand on the lift lever.",
    'Ilo': "Ilo and Mattie, on their doorstep, still holding hands.",
    'Mattie': "Mattie, turning to say something to Ilo.",
    'Gran Osk': "Gran Osk, bending to the Pidove. The bird flew. She didn't.",
    'Benno': "Benno, ladle raised over the noodle pot. The steam is glass.",
    'Mr Imrie': "Mr Imrie, red pen on a page. The page says \"my mum's face\".",
    'Dex': "Dex, mid-wave, soda crate on his hip. His mouth is open. He was about to tell you the rest.",
}
for nm, spr, d, lines, gp in RES:
    add(181, talk(nm, spr, d, [l if ':' in l[:14] else N(nm, l) for l in lines], gone=None))
add(181,
    ev('Dex', page([P('DEX', 'happy', "FIZZBOLT! Fizzbolt, ice-cold, colder than the Thane's heart! You two! You're new! You've got new faces!"),
                    N('Dex', "I'm Dex. That's Spark. Spark makes them cold. Watch."),
                    "(The Pichu lays a paw on a bottle. A tiny zap. Frost blooms up the glass.)", {'se': 'Anim/Thunder1'},
                    P('JUNO', 'happy', "That's AMAZING."),
                    P('DEX', 'happy', "Fifty a bottle. Thirty for you, because you said \"amazing\". Nobody says \"amazing\" down here. They say \"how much\"."),
                    S('pfm_item(:FIZZBOLT, 2, "FIZZBOLT") rescue nil'), S('$player.money = [$player.money - 60, 0].max'),
                    N('Dex', "You want the best airship view in Lumen? Not the Skyport, everyone goes to the Skyport. The laundry roof, there. You get the Spire's top and the Crownwall and the Dauntless coming in, all at once."),
                    P('DEX', 'happy', "My sister Marlo works the night lift down to Nadir, and she says one night the cage didn't stop at the bottom, it went right on down past it, into the old—"),
                    {'se': 'Bell'}, P('DEX', 'shocked', "That's the hour! The crew'll want their sodas! Rook's filming down here today, did you know? ROOK CALDER. In the LOWLIGHT."),
                    P('DEX', 'happy', "Tell you the rest tomorrow!"), {'var': [STEP, 4]}], SPR['DEX'], 'down', cond=vcond(3), trigger='touch'),
       page([N('Dex', "Fizzbolt! Ice-cold! Spark says hi! (The Pichu does not say hi.)")], SPR['DEX'], 'down', cond=vcond(4))),
    ev('Spark the Pichu', page(["Pichu: Pi! (It crackles at you, friendly.)"], 'Followers', 'down', cond=vcond(4))),
    ev('Rook', page([P('ROOK', 'happy', "Chat, look at that! New faces in the Lowlight!")], SPR['ROOK'], 'down'),
       page([P('ROOK', 'happy', "—and THIS is the Lowlight, chat! The REAL Lumen! Ten years of light, and tonight we've brought it all the way down here—"),
             N('Director', "Rook. You're blocking the noodle cart."),
             P('ROOK', 'happy', "—brought it all the way down here AND we're supporting local noodles! Hi, Benno! Chat loves Benno!"),
             N('Benno', "I don't know what that means!"),
             P('DEX', 'happy', "Rook! Your sodas! That's eleven you owe me now. Chat owes me eleven."),
             P('ROOK', 'happy', "Chat, pay the man! ...Chat says it'll pay you in exposure. Chat is a terrible person, Dex."),
             P('ROOK', 'neutral', "(He sees you.) Oh. Challengers. Hi. Gym's shut, sorry. The Spire wanted a \"community special\", and when the Spire wants a thing, the thing happens."),
             P('ROOK', 'happy', "Chat says you look tired. Chat says—"),
             {'se': 'Anim/Thunder3'}, {'tone': [80, 80, 80, 0, 6]},
             N('Director', "Rook, we're pulling too much off the—"),
             {'tone': [-120, -120, -90, 40, 20]},
             "(The floodlights die. Then the street lamps. Then every window, block by block. The Lowlight goes black. Somewhere a Pidove panics.)",
             P('ROOK', 'shocked', "—CHAT? Chat, are you there? Rotom, are we live?"),
             N('Rotom Drone', "(bzzt) ...signal lost."),
             P('ROOK', 'panic', "We're not live. We're not LIVE. I haven't been not-live since I was fourteen."),
             "(In the dark, the junction boxes on the street corners start to glow from the inside, one after another. Something in each of them is giggling.)",
             N('Hob Carrow', "(from his ladder) Rotom! The floods pulled 'em out of the Spire feed! They're in the boxes, they'll drink the whole block!"),
             P('ROOK', 'neutral', "Okay. Okay. I can do this. This is fine. This is content."),
             P('ROOK', 'panic', "I can't do this, my drone's dead. You. You've got Pokémon that aren't plugged into anything, right? Boxes. Corners. GO."),
             {'switch': [S_BLACKOUT, True]}, {'selfswitch': ['A', True]}], SPR['ROOK'], 'down', cond=vcond(4)),
       page([P('ROOK', 'panic', "Boxes! Corners! GO! I'll hold the... I'll hold the camera. It's off. I'll hold it anyway.")], SPR['ROOK'], 'down', cond={'var': [STEP, 4], 'self': 'A'}),
       page([], cond=vcond(5))),
    talk('Director', 'NPC 12', 'left', [N('Director', "Rook. Rook. The noodle cart. Rook.")], gone=5),
    talk('Boom operator', 'NPC 24', 'up', [N('Boom operator', "(holding a microphone on a pole over nothing) I've been holding this for four hours.")], gone=5),
    ev('Service door', page(["SERVICE DOOR: A steel door in the cliff under the Spire. \"MERIDIAN CONCORD — AUTHORIZED PERSONNEL.\" Locked. It's warm."])),
    ev('Lowlight lift', page(["The Nadir lift: an iron cage on a cable, going down into warm dark. A board: LIFT DOWN AT SIX. CHECKPOINT AT THE BOTTOM."])),
)
for i in range(4):
    lv = 26 if i == 3 else 24
    add(181, ev('Junction box %d' % (i + 1),
                page(["A junction box on the corner. It hums normally."], tile=P1('lm_junction')),
                page(["The box glows from inside. Something in it is giggling.",
                      S('setBattleRule("field", :NEON_GRID)'), S('WildBattle.start(:ROTOM, %d)' % lv),
                      "The glow goes out. The box hums normally. Somewhere a window comes back on.",
                      S('pfm_lumen_box(%d)' % (i + 1)), {'selfswitch': ['A', True]}], tile=P1('lm_junction_on'), cond={'var': [STEP, 4], 'switch': S_BLACKOUT}),
                page(["The box hums normally."], tile=P1('lm_junction'), cond={'var': [STEP, 4], 'self': 'A'}),
                page(["A junction box on the corner. It hums normally."], tile=P1('lm_junction'), cond=vcond(5))))
add(181, ev('Blackout ends', page([], cond=None),
            page([{'se': 'PC open'}, {'tone': [0, 0, 0, 0, 20]},
                  "(The hum of a whole block coming back. The floodlights flicker up, then the lamps, then the windows. The Lowlight cheers.)",
                  P('ROOK', 'happy', "We're back. WE'RE BACK. Chat! Chat, are you— (bzzt) —chat is saying \"WHAT HAPPENED\". Chat, you would not BELIEVE what happened."),
                  P('ROOK', 'neutral', "(quieter, with the drone pointed away) Thanks. Really. I'm not good in the dark. Nobody up there's good in the dark. That's kind of the whole problem with up there."),
                  P('ROOK', 'happy', "Gym's open! Circuit Gym, west side of the Concourse. Come and lose on camera. It's the best way to lose!"),
                  P('JUNO', 'happy', "He's lovely! Is he always like that?"),
                  P('ROOK', 'deadpan', "Chat says yes. Chat says I'm \"a lot\"."),
                  {'var': [STEP, 5]}, {'switch': [S_BLACKOUT, False]}, {'selfswitch': ['A', True]}], cond={'var': [STEP, 4], 'switch': S_BOXES}, trigger='autorun'),
            page([], cond={'self': 'A'})))

# ===================================================================================================== 608 the Lowlight, Shattered
for nm, spr, d, lines, gp in RES + [('Dex', '', 'down', [], 2)]:
    add(608, ev('Glass ' + nm, page([GLASS_LINE[nm]])))
add(608,
    ev('Aftermath', page([
        "(The vault's service door opens onto the Lowlight. It's quiet. The lamps are out. The light that's left is violet and comes from the glass.)",
        "(Twelve people stand in the street where they stood this afternoon. They are glass.)",
        P('JUNO', 'shocked', "..."),
        "(Beyond the edge of the district a shimmer hangs in the air like heat over a road. On the far side of it, people are shouting. Nobody comes in.)",
        "(You can stand here. Nobody else can.)",
        {'selfswitch': ['A', True]}], cond=vcond(9), trigger='autorun'),
       page([], cond={'var': [STEP, 9], 'self': 'A'})),
    talk('Rook (off camera)', SPR['ROOK'], 'down', [P('ROOK', 'sad', "...Turn it off. Rotom. Turn it *off*.")], cond=vcond(9), gone=11),
    # Valen's line is the script's "V125 = 10" (Wave 0 softlock 1: nothing set 10, so the Testimony never appeared).
    ev('Valen at the Veil',
       page([P('VALEN', 'neutral', "You were in the Lowlight when it went? And you're... standing."),
             "(He looks a beat too long, then turns away.)",
             N('Valen', "Who's in charge here?"), P('MARCHETTI', 'neutral', "Director Marchetti, Sovereign. Meridian Security Directorate."),
             N('Valen', "Then take statements. All of them. Including that one."), {'var': [STEP, 10]}], SPR['VALEN'], 'up', cond=vcond(9)),
       page([N('Valen', "Take statements. All of them.")], SPR['VALEN'], 'up', cond=vcond(10)),
       page([], cond={'var': [STEP, 11]})),
    talk('Voss with the crate', SPR['VOSS'], 'down', ["(Voss, in shirtsleeves, carrying a glassed child's soda crate out of the Lowlight himself. Every screen in Lumen is showing him.)"],
         cond=vcond(9), gone=11),
    ev('Testimony', page([N('Directorate Officer', "You were inside. What did you see?"),
                          CH(['"The Mourner broke the Plate."', '"Someone else was there."', '"I don\'t know."'],
                             [[S('pf_choose(:ch5_lowlight_testimony, :mourner) rescue nil'), N('Directorate Officer', "Thank you. That's very clear.")],
                              [S('pf_choose(:ch5_lowlight_testimony, :someone_else) rescue nil'), N('Director Marchetti', "(She writes your name down.)"),
                               P('LARCH', 'neutral', "(quietly) Good.")],
                              [S('pf_choose(:ch5_lowlight_testimony, :unknown) rescue nil'), N('Directorate Officer', "Nobody does, tonight.")]]),
                          {'var': [STEP, 11]}, {'switch': ['CH5_MANDATE', True]}], 'trainer_SCIENTIST', 'down', cond=vcond(10)),
       page([N('Directorate Officer', "Thank you for your statement.")], 'trainer_SCIENTIST', 'down', cond=vcond(11))),
    talk("Spark the Pichu", 'Followers', 'down', ["Pichu: ...pi. (It won't leave Dex's feet.)"]),
    sign('Lowlight screen', "A street screen at the edge of the Veil. Tonight it will carry the Sovereign's broadcast: THE MANDATE. VELMORA ENDURES.", post=False),
)
