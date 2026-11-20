"""story_early: every scripted event of story/20_SCRIPT_CH0-2.md that lives on the towns builder's maps
(109-110 the Dovetail, 100-108 Ferrow's Landing, 120-125 Briarwick), written out by hand from the FINAL script.
Layout scripts seat them: `ev = EVENTS[map_id]`; `place(map_id, name, (x, y))` returns the event dict with `at`;
`unplaced(map_id)` lists anything a layout forgot (layouts abort on it, so nothing in the script goes missing).

Conventions: portrait lines are `\\pf[ID,expr,emotes,event]Name: text` (design/CUTSCENES.md §6); emotes from the script's
*(anger vein)* etc. map to anger / sweat / shock / question / dots. Choice keys are NARRATIVE_KEYS' lowercase ones and
are applied only through pf_choose. Small scene state (who you've talked to, quest steps) uses the pfm_* helpers in
mapgen/ruby/006_MapStory.rb instead of new Game Switch ids. Story items without PBS data go through pfm_item."""
import copy
import scriptpour as SP

NAMES = {'EDDA': 'Edda', 'VOSS': 'Voss', 'CALLA': 'Calla', 'LARCH': 'Larch', 'JUNO': 'Juno', 'KESTREL': 'Kestrel',
         'ROWAN': 'Rowan', 'WENNA': 'Wenna', 'COLL': 'Coll', 'HESPER': 'Hesper', 'TAMSIN': 'Tamsin', 'THISTLE': 'Thistle'}
SPR = {'EDDA': 'NPC 14', 'VOSS': 'trainer_GENTLEMAN', 'CALLA': 'trainer_SCIENTIST', 'LARCH': 'trainer_PROFESSOR',
       'JUNO': 'trainer_RIVAL2', 'KESTREL': 'trainer_RIVAL1', 'ROWAN': 'trainer_POKEMONRANGER_M', 'WENNA': 'NPC 19',
       'COLL': 'NPC 03', 'HESPER': 'NPC 11', 'TAMSIN': 'trainer_LASS', 'THISTLE': 'trainer_BURGLAR'}


def P(who, expr, text, emote='', ev=''):
    """Portrait line (the script's [portrait: WHO, expr])."""
    tag = who + ',' + expr + ((',' + emote) if (emote or ev) else '') + ((',' + ev) if ev else '')
    return '\\pf[%s]%s: %s' % (tag, NAMES.get(who, who.title()), text)


def N(name, text): return '%s: %s' % (name, text)
def S(code): return {'script': code}
def IF(cond, then, els=None): return {'if': cond, 'then': then, **({'else': els} if els is not None else {})}
def CH(opts, branches, cancel=0): return {'choices': opts, 'branches': branches, 'cancel': cancel}
def MV(who, route, wait=True): return {'move': {'who': who, 'route': route, 'wait': wait}}
def ITEM(i, n=1, name=None): return S('pfm_item(:%s, %d%s)' % (i, n, (', "%s"' % name) if name else ''))
def SW(name, on=True): return {'switch': [name, on]}
def SELF(evname, ch='A', on=True): return S('pbSetSelfSwitch(%%EV[%s]%%, "%s", %s)' % (evname, ch, 'true' if on else 'false'))
def QUEST(qid, title, text): return S('pfm_quest(:%s, "%s", "%s")' % (qid, title, text.replace('"', '\\"')))


def page(cmds, sprite='', d='down', cond=None, trigger='action', move='fixed', through=False, tile=0, step=False):
    p = {'commands': cmds, 'trigger': trigger, 'move': move}
    if sprite or tile: p['graphic'] = {'sprite': sprite, 'dir': d, **({'tile': tile} if tile else {})}
    if cond: p['cond'] = cond
    if through: p['through'] = True
    if step: p['step_anime'] = True
    return p


def ev(name, *pages): return {'type': 'event', 'name': name, 'pages': list(pages)}
def sign(name, text, post=True): return {'type': 'sign', 'name': name, 'post': post, 'text': text}
def warp(name, **kw): return dict({'type': 'warp', 'name': name}, **kw)


def hidden(name, item, text):
    """Hidden item with the script's flavour line. Named HiddenItem* so the Itemfinder sees it."""
    return ev(name, page([IF('pbItemBall(:%s)' % item, [text, {'selfswitch': ['A', True]}])]), page([], cond={'self': 'A'}))


def talk(name, sprite, d, cmds, again=None, move='fixed', after=()):
    """NPC with optional (again) page and [after X] variants: after = [(cond, cmds)] in rising priority."""
    ps = [page(cmds + ([{'selfswitch': ['A', True]}] if again else []), sprite, d, move=move)]
    if again: ps.append(page(again, sprite, d, cond={'self': 'A'}, move=move))
    for c, cm in after: ps.append(page(cm, sprite, d, cond=c, move=move))
    return ev(name, *ps)


def strip(base, n):
    """n copies of a touch event (a trigger line across a path), named base 1..n."""
    out = []
    for i in range(n):
        e = copy.deepcopy(base); e['name'] = '%s %d' % (base['name'], i + 1); out.append(e)
    return out


EVENTS = {}


def add(mid, *evs):
    for e in evs:
        EVENTS.setdefault(mid, {})[e['name']] = e


def place(mid, name, at, **kw):
    e = copy.deepcopy(EVENTS[mid][name]); e['at'] = list(at); e.update(kw); EVENTS[mid][name]['_placed'] = True
    e.pop('_placed', None)
    return e


def unplaced(mid):
    return [n for n, e in EVENTS.get(mid, {}).items() if not e.get('_placed')]


def parsed(lines_start, lines_end, per_speaker=False):
    return SP.parse(SP.section(lines_start, lines_end), per_speaker=per_speaker)


def npc_from(n, sprite=None, d='down', move='fixed'):
    """scriptpour npc -> event with (again) page."""
    return talk(n['name'], sprite or SP.sprite(n['name']), d, list(n['first']), again=list(n['again']) or None, move=move)


# ===================================================================================================== 109 / 110 the Dovetail
EDDA_RAIL = [
    MV('Captain Edda', ['toward_player', 'toward_player']),
    P('EDDA', 'angry', 'Oi! Sprog! Can you read?', 'anger', 'Captain Edda'),
    CH(['Yes.', 'No.', '...'], [
        [P('EDDA', 'deadpan', "Then you're doing it on purpose. That's worse.", '', 'Captain Edda')],
        [P('EDDA', 'shocked', "...Oh. Oh, stars. Right. That's a D. That one's an O.", 'sweat', 'Captain Edda')],
        [P('EDDA', 'deadpan', "Strong silent type. Wonderful. I'll just talk to the rail, shall I?", '', 'Captain Edda'),
         P('EDDA', 'angry', 'Rail! Tell the sprog to get off you!', '', 'Captain Edda')]], cancel=3),
    MV('Captain Edda', ['toward_player']),
    {'anim': ['Captain Edda', 3]}, {'wait': 40},
    P('EDDA', 'shocked', "Don't lean on my rail like that, you'll— huh.", 'dots', 'Captain Edda'),
    P('EDDA', 'neutral', '...Never mind. You stand how you like.', '', 'Captain Edda'),
    P('EDDA', 'neutral', "Mind the gap when we dock. And don't look down at the water after dark.", '', 'Captain Edda'),
    CH(['Why not?', '...'], [
        [P('EDDA', 'deadpan', "Because I said, and it's my boat.", '', 'Captain Edda')],
        [P('EDDA', 'sad', '...Good. Somebody used to ask me that every crossing.', '', 'Captain Edda')]], cancel=2),
    MV('Captain Edda', ['through_on', {'script': 'moveto(EDDA_HOME)'}, 'through_off', 'turn_down']),
    S('pfm_set(:dove_edda)')]

VOSS_RAIL = [
    MV('Aurelian Voss', ['toward_player', 'toward_player', 'toward_player', 'face_player']),
    'He leans on the rail right next to the sign. He holds a chipped white mug with a faded sunburst.',
    P('VOSS', 'happy', 'First crossing? Everyone goes quiet when they see the lights.', '', 'Aurelian Voss'),
    P('EDDA', 'angry', 'RAIL!', 'anger', 'Captain Edda'),
    P('VOSS', 'happy', 'I believe the rail has no objection, Captain.', '', 'Aurelian Voss'),
    P('EDDA', 'angry', 'Nobody asked the passengers in the nice coats!', '', 'Captain Edda'),
    P('VOSS', 'neutral', "She's been shouting at me since I was a linesman. It's how I know I'm home.", '', 'Aurelian Voss'),
    P('VOSS', 'neutral', "I've spent a month in a marble room asking the Concert not to do this. They did it anyway. Politely.", '', 'Aurelian Voss'),
    P('VOSS', 'neutral', "So. You're coming in on the day everyone else wishes they could get out. That takes nerve or bad luck.", '', 'Aurelian Voss'),
    CH(['Nerve.', 'Bad luck.', '...'], [
        [P('VOSS', 'happy', 'Good. Velmora runs on it.', '', 'Aurelian Voss')],
        [P('VOSS', 'happy', "Then you'll fit right in.", '', 'Aurelian Voss')],
        [P('VOSS', 'neutral', "Or grief. Forgive me. I shouldn't guess.", '', 'Aurelian Voss')]], cancel=3),
    P('VOSS', 'neutral', "Are you challenging the gyms? You've got the look. Eighteen Wardens, eighteen badges. Nobody's done all eighteen in ten years.", '', 'Aurelian Voss'),
    P('VOSS', 'happy', "Here. You'll want one of these.", '', 'Aurelian Voss'),
    ITEM('BADGECASE', 1, 'Badge Case'),
    'A slim brass case with eighteen empty settings. Stamped on the hinge: MERIDIAN CONCORD.',
    P('VOSS', 'neutral', 'We make them for the League anyway. Call it a welcome from a fellow traveler.', '', 'Aurelian Voss'),
    P('VOSS', 'neutral', 'And this, if you\'ll take it. A Meridian Fellowship. A little money each month, a discount at any Mart. We give them to young trainers with promise.', '', 'Aurelian Voss'),
    CH(['Thank you.', 'No, thank you.', '...'], [
        [S('pf_choose(:pro_fellowship, :accept)'), ITEM('FELLOWSHIPCARD', 1, 'Fellowship Card'), S('pfm_money(3000)'),
         P('VOSS', 'happy', 'No, I insist. Somebody should be kind to you on a day like this.', '', 'Aurelian Voss')],
        [S('pf_choose(:pro_fellowship, :decline)'),
         P('VOSS', 'happy', "Independent. Good. Keep that. It's worth more than the card.", '', 'Aurelian Voss')],
        [S('pf_choose(:pro_fellowship, :silent)'), P('VOSS', 'neutral', 'Think about it.', '', 'Aurelian Voss'),
         'He sets the card on the rail.', ITEM('FELLOWSHIPCARD', 1, 'Fellowship Card'),
         'It is not activated. A Mart clerk could switch it on.', S('pfm_set(:fellowship_off)')]], cancel=0),
    'The ship\'s horn sounds, long and low.',
    P('VOSS', 'neutral', "That's the Landing. Aurelian Voss. If you ever need anything in Lumen City, ask for me by name. They'll laugh, and then they'll fetch me.", '', 'Aurelian Voss'),
    MV('Aurelian Voss', ['through_on', 'away_player', 'away_player', 'away_player', 'turn_180', 'wait 20', 'turn_180',
                         'away_player', 'away_player', {'opacity': 0}]),
    S('pfm_set(:dove_voss)'), SW('PRO_FERRY_DONE'),
    {'tone': [-255, -255, -255, 0, 20]}, {'wait': 24},
    'The Dovetail noses in against an old stone pier. Ropes thump. The gangway clatters down aft.',
    {'tone': [14, -4, -24, 10, 20]}, {'wait': 20},
    S('Prismfall.checkpoint')]

add(109,
    ev('Prologue intro',
       page([{'tone': [-255, -255, -255, 0, 0]},
             S('pfm_card(:PF_PROLOGUE_CARD, "Spring, AF 300.", "The Concert of Regions has sealed the borders of Velmora.", "This is the final civilian crossing.")'),
             'In the black porthole glass, a reflection looks back at you.',
             CH(["That's me. (Style A)", "That's me. (Style B)"], [[S('pbChangePlayer(1)')], [S('pbChangePlayer(2)')]], cancel=0),
             {'tone': [14, -4, -24, 10, 30]}, {'wait': 30},
             'The deck. You stand at the port rail, one bag at your feet. Gulls. On the horizon, a low line of eighteen colored glows.',
             N('Deckhand', 'Twenty minutes to the Landing! Mind your bags, mind your feet, mind the Captain!'),
             N('Deckhand', "And the manifest. Captain's orders: last crossing, nobody goes missing off her books. Name?"),
             {'label': 'Manifest name'}, S('pbTrainerName'),
             N('Deckhand', '\\PN. That right?'),
             CH(["That's right.", 'No, let me spell it.'], [[], [{'jump_label': 'Manifest name'}]], cancel=0),
             MV('Deckhand', ['left', 'left', 'left']),
             S('$player.has_running_shoes = true'), S('Prismfall.choose_difficulty'),
             SW('LARCH_AT_TIDEWATCH'), {'var': ['STORY_ACT', 0]}, {'var': ['STORY_CHAPTER', 0]},
             {'selfswitch': ['A', True]}], trigger='autorun'),
       page([], cond={'self': 'A'})),
    sign('Rail sign', None) | {'commands': ['DO NOT LEAN ON RAIL. — Capt. E. Morrow',
                                            IF('$game_player.direction == 8', ['You are leaning on it.'])]},
    *strip(ev('Rail watch',
              page([IF('!pfm?(:dove_edda)', EDDA_RAIL, [IF('!pfm?(:dove_voss)', VOSS_RAIL)])], trigger='touch'),
              page([], cond={'switch': 'PRO_FERRY_DONE'})), 5),
    ev('Captain Edda',
       page([P('EDDA', 'neutral', "Thirty-one years on this strait. Never thought I'd see them close it."),
             P('EDDA', 'deadpan', "Don't touch the wheel. Don't touch the rail. Touch the horizon if you like, it's free.")],
            SPR['EDDA'], 'down'),
       page([P('EDDA', 'neutral', "That's the Landing. Down the gangway, sprog. Mind the gap.")], SPR['EDDA'], 'down',
            cond={'switch': 'PRO_FERRY_DONE'})),
    ev('Aurelian Voss',
       page(["A man in a good coat watches the lights over the rim of a chipped mug. He hasn't noticed you yet."], SPR['VOSS'], 'left'),
       page([], cond={'switch': 'PRO_FERRY_DONE'})),
    ev('Mug ring', page([]), page(['A ring of cold tea. He drank it black.'], cond={'switch': 'PRO_FERRY_DONE'})),
    ev('Gangway',
       page(["The gangway is roped off. It's a sailor's knot. It's a good knot.", MV('player', ['up'])], trigger='touch'),
       page([{'se': 'Door exit'}, {'tone': [-255, -255, -255, 0, 12]}, {'wait': 14},
             {'transfer': {'map': 100, 'x': 34, 'y': 55, 'dir': 'up'}}, {'tone': [0, 0, 0, 0, 12]}],
            cond={'switch': 'PRO_FERRY_DONE'}, trigger='touch')),
    sign('Horizon', 'Eighteen lights sit low over the sea, each a different color.\nOne of them, far to the north, flickers.', post=False),
    hidden('HiddenItem coiled rope', 'POTION', "Someone's seasick remedy. It's just a Potion with a lemon drawn on it."),
    talk('Deckhand', 'NPC 15', 'right', [N('Deckhand', "Twenty minutes, I said! It's been twenty minutes for an hour. The Captain's going slow on purpose.")], move='random'),
    talk('Old Man', 'NPC 06', 'up', [N('Old Man', "See the colors on the skyline? Eighteen of 'em. That's Velmora."),
                                     N('Old Man', "When I was a lad you only saw the Imprints on a clear night. Now you see 'em through fog.")]),
    talk('Woman with crate', 'NPC 22', 'down', [N('Woman with crate', "I'm going home to Saltmere. My sister says don't. I said, where else would I go? I get ill anywhere else."),
                                                N('Woman with crate', "Three weeks abroad and I was grey as dishwater. They call it wilting. You'll see.")]),
    talk('Boy', 'NPC 02', 'up', [N('Boy', 'Mum says when we land a machine tells you what color you are! I want to be red.'),
                                 N("Boy's Mother", "You'll be green like the rest of us, love. We're Briarwick."),
                                 N('Boy', '...Can I be green AND red?')], move='random'),
    talk("Boy's Mother", 'NPC 04', 'left', [N("Boy's Mother", "You'll be green like the rest of us, love. We're Briarwick."),
                                            N('Boy', '...Can I be green AND red?')]),
    talk('Sailor', 'trainer_SAILOR', 'down', [N('Sailor', "Last crossing. After tonight the Concert's cutters turn back anything bigger than a gull."),
                                              N('Sailor', "Captain says she'll tie up at the Landing and learn to knit. She won't.")]),
    talk('Seasick Man', 'NPC 05', 'right', [N('Seasick Man', "Don't talk to me. If I open my mouth, more than words come out.")]),
    warp('Cabin hatch', link='DOVE_CABIN', se='Door exit'))
EVENTS[109]['Rail sign']['text'] = 'DO NOT LEAN ON RAIL.'

add(110,
    warp('Up to deck', link='DOVE_CABIN', se='Door exit'),
    sign('Bunk', "Your bunk. You didn't sleep in it.", post=False),
    sign('Porthole', 'Dark water. Far down, for a moment, something glows. Then it doesn\'t.', post=False),
    talk('Cook', 'NPC 09', 'down', [N('Cook', 'Last bowl of chowder on the last ferry. Historic chowder. Eat it slow.'),
                                    ITEM('OLDCHOWDER', 1, 'Old Chowder'), 'Restores 20 HP. Tastes like the end of an era.'],
         again=[N('Cook', 'Last bowl on the last ferry. You had it. Historic.')]),
    sign('Bookshelf', '"Passenger Notice: Persons of Velmoran birth are advised that prolonged absence from one\'s home Imprint may cause fatigue, pallor and low spirits. The line accepts no liability for wilting."', post=False),
    sign('Locked trunk', "It's locked. Scratched into the lid, very small: I.A. + child, night crossing, 290. Paid in full.", post=False),
    sign("Mum's letter", 'A letter in your mother\'s handwriting. The ink runs where the sea got at it.\n"Go to Imelda Larch at Ferrow\'s Landing, before they close the strait.\nDon\'t let anyone scan you. Don\'t go to Crownhaven.\nI\'m sorry I never told you why. I wanted one of us to have an ordinary life.\n— Mum."', post=False))


# ===================================================================================================== 100 Ferrow's Landing
GATE = 'Customs gate'
DOCKING = [
    'The gangway is down. Passengers queue toward a brass-and-glass gate bolted to the old stone pier. Beside it stands a green bronze plaque.',
    P('CALLA', 'neutral', "Welcome to Velmora. Step through one at a time, please. Hold still. It doesn't hurt.", '', 'Calla'),
    MV('Boy (pier)', ['up', 'up']), {'se': 'Pkmn exp full'}, 'A bar on the gate glows green.',
    P('CALLA', 'neutral', 'Insect tint. Briarwick. Thank you.', '', 'Calla'),
    MV('Boy (pier)', ['up', 'turn_down'], wait=False),
    N('Boy', 'MUM. I\'M GREEN.'), N("Boy's Mother", 'I know, love.'),
    MV("Boy's Mother (pier)", ['up', 'up', 'up']),
    MV('Woman with crate (pier)', ['up', 'up']), {'se': 'Pkmn exp full'}, 'The bar glows white.',
    P('CALLA', 'neutral', 'Blank tint. Saltmere. Welcome home.', '', 'Calla'),
    MV('Woman with crate (pier)', ['up', 'up', 'up']),
    {'selfswitch': ['A', True]}]

SCAN = [
    P('CALLA', 'neutral', 'Next, please. Hold still.', '', 'Calla'),
    {'se': 'Pkmn exp full'}, {'wait': 20}, 'The bar stays dark.', {'wait': 40},
    P('CALLA', 'neutral', 'One moment.', '', 'Calla'),
    {'se': 'GUI sel buzzer'}, 'The bar flickers, and a word scrolls across it: NULL.',
    P('CALLA', 'shocked', "...That's not a tint.", 'question', 'Calla'),
    P('CALLA', 'neutral', "I'm sorry, could you step out and in again?", '', 'Calla'),
    MV('player', ['backward', 'forward']), {'se': 'GUI sel buzzer'}, 'NULL.',
    N('Boy', "Mum, that one's got no color!"), N("Boy's Mother", "Don't point."),
    'The queue behind you murmurs.',
    MV('Aurelian Voss (dock)', ['through_on', 'up', 'up', 'up', 'turn_up', 'through_off']),
    P('VOSS', 'happy', 'Faulty unit. These things hate sea air.', '', 'Aurelian Voss (dock)'),
    P('VOSS', 'neutral', 'Let them through, Calla.', '', 'Aurelian Voss (dock)'),
    P('CALLA', 'neutral', 'Sir, the protocol says—', '', 'Calla'),
    P('VOSS', 'neutral', 'The protocol was written by me, on a train. Let them through.', '', 'Aurelian Voss (dock)'),
    P('CALLA', 'neutral', '...Yes, sir. Welcome to Velmora.', '', 'Calla'),
    MV('player', ['up']),
    MV('Aurelian Voss (dock)', ['through_on', 'up', 'turn_left']),
    P('VOSS', 'happy', 'There. Ordinary as anyone. Enjoy the Landing. Try the bramble tarts.', '', 'Aurelian Voss (dock)'),
    MV('Aurelian Voss (dock)', ['up', 'up', 'turn_down', 'wait 30', 'up', 'up', 'up', 'up', 'up', {'opacity': 0}]),
    MV('Calla', ['turn_right', 'wait 10']), {'se': 'Voltorb Flip tile'}, {'wait': 20},
    SW('PRO_SCANNED_NULL'),
    "The ship's horn sounds, long. Behind you the Dovetail pulls back from the pier and stops. A chain is drawn across the harbor mouth.",
    N('Harbor Crier', 'By order of the Concert of Regions, the Hallow Strait is closed! The Hallow Strait is closed!'),
    {'var': ['STORY_ACT', 1]}, {'var': ['STORY_CHAPTER', 1]},
    S('pfm_card(:PF_ACT1_TITLE, "ACT I — THE LAST FERRY")'),
    QUEST('mums_letter', "Mum's Letter", 'Find Imelda Larch at the research station on the headland.')]

LAST_CALL = [
    P('EDDA', 'neutral', "That's it, then. Once I cast off the Concert's cutters won't let me back across.", '', 'Captain Edda'),
    P('EDDA', 'neutral', 'Last chance, sprog. Anyone who wants off this rock rides with me now.', '', 'Captain Edda'),
    CH(["I'm staying.", 'I want to go back.'], [
        [P('EDDA', 'happy', 'Thought so. Go on. Mind the gap.', '', 'Captain Edda')],
        [P('EDDA', 'neutral', "...You sure? I'll ask once more, because nobody asked her. Once I cast off, that's it.", '', 'Captain Edda'),
         CH(["I'm staying.", 'Take me back.'], [
             [P('EDDA', 'happy', "Good. Stars. Don't frighten an old woman.", '', 'Captain Edda')],
             [P('EDDA', 'sad', 'Right. Get aboard, then.', '', 'Captain Edda'), {'tone': [-255, -255, -255, 0, 30]},
              "The horn. The eighteen lights recede.", S('Prismfall.game_over(:GO_HOMEWARD)')]], cancel=0)]], cancel=0),
    S('pfm_set(:edda_lastcall)')]

K1 = [
    MV('Kestrel K1', ['face_player']),
    P('KESTREL', 'neutral', "You came in on the last ferry? Great. Velmora's sinking and they're still letting tourists on.", '', 'Kestrel K1'),
    CH(['I was born here.', "I'm not a tourist.", '...'], [
        [P('KESTREL', 'shocked', "...Then you left, and came BACK? That's worse.", 'question', 'Kestrel K1')],
        [P('KESTREL', 'smug', 'Prove it.', '', 'Kestrel K1')],
        [P('KESTREL', 'angry', 'Say something! Gran does that. The staring. I hate the staring.', 'anger', 'Kestrel K1')]], cancel=3),
    IF('Prismfall.rival_battle(:RIVAL_KESTREL, "Kestrel", 1, can_lose: true)',
       [P('KESTREL', 'shocked', '...With the type disadvantage.', 'shock', 'Kestrel K1'),
        P('KESTREL', 'angry', "Fine. You're not a tourist. You're a problem.", '', 'Kestrel K1'), S('pf_bond_add(:KESTREL, 1)')],
       [P('KESTREL', 'smug', 'Boat fare: wasted.', '', 'Kestrel K1'),
        P('KESTREL', 'neutral', "...Your partner didn't quit, though. Mine would've bitten me. Huh.", '', 'Kestrel K1')]),
    {'heal': True},
    MV('Juno (lab yard)', [{'graphic': [SPR['JUNO'], 0, 2, 0]}, {'opacity': 255}, 'through_on', 'down', 'down', 'through_off', 'face_player']),
    P('JUNO', 'happy', 'That was amazing! Both of you! We should have a team name!', 'sparkle', 'Juno (lab yard)'),
    P('KESTREL', 'deadpan', "There's no team.", '', 'Kestrel K1'),
    P('JUNO', 'happy', 'Team Compost! Because we break things down and make them better!', '', 'Juno (lab yard)'),
    P('KESTREL', 'deadpan', "I'm not in it.", '', 'Kestrel K1'),
    P('JUNO', 'happy', "He's in it.", '', 'Juno (lab yard)'),
    {'anim': ['Kestrel K1', 3]},
    MV('Kestrel K1', ['through_on', 'left', 'left', 'left', 'left', 'left', 'left', {'opacity': 0}]),
    SW('CH1_K1_DONE')]

ERRAND = [
    P('JUNO', 'panic', "\\PN! Mum's Skwovet's got out again. Biscuit. He's gone to the Pruett orchard and I'm not— nobody's supposed to go in there.", '', 'Juno (lab yard)'),
    P('JUNO', 'neutral', "Will you come and look? Just LOOK. From the outside. I'll show you the way.", '', 'Juno (lab yard)'),
    QUEST('biscuit', 'Biscuit', "Go with Juno to the old orchard on Windfall Row."),
    P('JUNO', 'happy', "Up the lane, past the stile! I'll be right behind you. Probably in front of you.", '', 'Juno (lab yard)'),
    S('pfm_set(:juno_errand)'), S('pfm_juno_join(:errand, "Juno (lab yard)")')]   # (Juno becomes a follower.)

SENDOFF = [   # story/20_SCRIPT_CH0-2.md, Chapter 2 "Chapter start" (Revision 14: Saltmere is first; map builder 9 re-pour)
    P('LARCH', 'neutral', "Eighteen gyms. Saltmere's first. The forest road to Briarwick's corded off -- the Glasswood's walked across it -- so you go round by the coast.", '', 'Larch (sendoff)'),
    P('LARCH', 'neutral', 'Two days on foot. Chalk cliffs, then dunes, then the free port. The Warden\'s Dorian Pell. He\'ll call you "darling" and mean it about a third of the time.', '', 'Larch (sendoff)'),
    P('LARCH', 'neutral', "Write to me. I mean it. Gale Post, every town. If I don't hear from you in a week I start Lecture Two by post.", '', 'Larch (sendoff)'),
    P('JUNO', 'happy', "I'm coming as far as Saltmere! Mum's promised forty tarts to the Pageant crowd and I'm the cart!", '', 'Juno (sendoff)'),
    P('JUNO', 'happy', "And I've wanted to see the Pageant since I was six. There's a bit where the Plates fall and they use REAL glitter.", '', 'Juno (sendoff)'),
    P('LARCH', 'deadpan', 'They use salt.', '', 'Larch (sendoff)'),
    P('JUNO', 'shocked', '...Why would you tell me that.', 'shock', 'Juno (sendoff)'),
    ITEM('TOWNMAP'), 'Larch has drawn a skull on the Glassed Orchard, a skull on the forest road, and a smaller skull on her own kettle.',
    QUEST('eighteen_roads', 'Eighteen Roads', 'Earn the first badge in Saltmere, west along the coast.'),
    S('pfm_set(:ch2_sendoff)'), SELF('Larch (sendoff)'), SELF('Juno (sendoff)'), S('pfm_juno_join(:saltmere)')]

WINGULL_GIRL = [IF('pfm?(:wingull_back)', [N('Girl', "Captain Edda's grounded. She doesn't know what that means. Neither do I.")], [
    IF('pfm?(:wingull_found)', [
        N('Girl', "CAPTAIN! You're in so much trouble. Here, ferry person, she wants you to have this."),
        'The Wingull drops the bottle cap at your feet, then changes its mind and takes it back.',
        ITEM('SHARPBEAK'), "A Wingull's idea of a fair trade.",
        P('EDDA', 'deadpan', '...What did she call that bird?', '', 'Captain Edda'),
        S('pfm_set(:wingull_back)'), S('pfm_quest_done(:wingull)'), SELF('Wingull (with girl)')], [
        IF('pfm_quest?(:wingull)', [N('Girl', "She's on the lighthouse rocks! I'm not allowed there! You're allowed everywhere, you're a ferry person!")], [
            IF('$game_switches[@@PRO_SCANNED_NULL] && pfm?(:wingull_talked)', [
                N('Girl', "Captain Edda flew off! The gate went BING and she got scared! She's on the lighthouse rocks and I'm not allowed there!"),
                QUEST('wingull', 'Captain Edda', 'Find the Wingull on the lighthouse rocks.'), SELF('Wingull (rocks)')], [
                N('Girl', "She's called Captain Edda. The real Captain Edda doesn't know. Don't tell her."), S('pfm_set(:wingull_talked)')])])])])]

LAMPLIGHTER = [IF('pfm?(:lamps_done)', [N('Lamplighter', "Forty years. And the gulls came to mine. That'll do.")], [
    IF('pfm_count(:lamps) >= 6', [
        S('pfm_dusk(30)'), 'Dusk. Above the six small yellow flames, the Meridian lamps switch on, white and humming.',
        N('Lamplighter', 'There. Look at that. You can hardly see mine under theirs.'),
        N('Lamplighter', "...But the gulls came to mine. Did you see? Here. I won't need it."),
        ITEM('CHARCOAL'), 'It kept a harbor lit for forty years.', S('pfm_day(30)'),
        S('pfm_set(:lamps_done)'), S('pfm_quest_done(:last_round)')], [
        IF('pfm_quest?(:last_round)', [N('Lamplighter', 'Six lamps on the quay. The proper way. Off you go.'), S('pbMessage(_INTL("({1} of 6 lit.)", pfm_count(:lamps)))')], [
            IF('pfm?(:lamp_talked)', [
                N('Lamplighter', 'The pole lights itself tonight. Do an old man a kindness? Light the six quay lamps by hand, the proper way. Last time anyone will.'),
                ITEM('LAMPTAPER', 1, "Lamplighter's Taper"),
                QUEST('last_round', 'The Last Round', 'Light the six old lamps along the quay (0/6).')], [
                N('Lamplighter', "Forty years I've lit this quay. Now a pole does it. The pole doesn't know the fishwives' names."),
                S('pfm_set(:lamp_talked)')])])])])]


# "Biscuit comes home" (story/20_SCRIPT_CH0-2.md, Map 523): Wenna, first talk after S105. The same scene plays here at
# her quay stall when the PC finds her before the farm; both copies share the 523 BISCUIT self switch
# (layouts/b3_interiors_523_526.yaml has the farm copy). Juno is following, so her lines point at the follower.
BISCUIT_HOME = [
    "(Biscuit hops off your head and into Wenna's apron pocket. He rattles.)",
    P('WENNA', 'happy', 'Oh, you wretched animal. Thank you. Both of you. Here. And another tart, for the nerves. Mine.'),
    ITEM('ORANBERRY', 3), S('pfm_quest_done(:biscuit)'), S("$game_self_switches[[523, 0, 'BISCUIT']] = true"),
    P('WENNA', 'neutral', "Now. It's getting dark, you've glass in your hair, and the inn's full of people with nowhere to be."),
    N('Wenna', "You're sleeping here tonight. That wasn't a question. I don't do questions after sundown."),
    P('JUNO', 'happy', "You can have my bed! I'll take the hayloft. I always take the hayloft when we have guests."),
    N('Juno', "We've never had guests. I'm very excited about the hayloft."),
    P('COLL', 'deadpan', "Hayloft's got a Skiddo in it.", '', 'Coll Hale'),
    N('Juno', "I'm excited about the Skiddo."),
    P('WENNA', 'happy', "Supper's whenever you come in. Coll made the bed, so it's made badly. But it's made."),
    'OBJECTIVE: Sleep at the Hale Farmhouse. (Nobody takes the Strand Road west after dark.)']

WENNA_FIRST = [
    P('WENNA', 'happy', 'Tarts! Bramble tarts! Last of the— oh. You came off the ferry.'),
    P('WENNA', 'shocked', "You're the one Imelda's been pacing about. Look at you. You're a coat hanger with a bag."),
    P('WENNA', 'happy', "Eat this. No, don't pay me. Eat it where I can see you."),
    ITEM('BRAMBLETART', 1, 'Bramble Tart'), "Restores 30 HP. Still warm. Tastes like somebody's kitchen.",
    P('WENNA', 'neutral', "My Juno works up at the station. Talks like a kettle. You'll like her. Everyone does, it's exhausting."),
    P('WENNA', 'neutral', "And take Juno's old Pokégear. She's upgraded. You'll want a map and a phone in this place."),
    S('$player.has_pokegear = true'), '\\PN received a Pokégear!', S('pfm_set(:wenna_tart)')]


def quay_lamp(i):
    lit = page(['The old lamp burns, small and yellow.'], tile=0, cond={'self': 'A'})
    lit['graphic'] = {'sprite': '', 'dir': 'down', 'tile': 'LAMP_LIT'}
    return ev('Quay lamp %d' % i,
              page([IF('pfm_has?(:LAMPTAPER) && !pfm?(:lamps_done)',
                       ["You light it. The flame is small and yellow and smells of whale oil.", {'selfswitch': ['A', True]},
                        S('n = pfm_add(:lamps)\npbMessage(_INTL("({1} of 6 lit.)", n))')],
                       ['An old oil lamp on an iron post. Cold. The new Meridian pole beside it hums.'])]),
              lit)


add(100,
    ev('Docking', page(DOCKING, trigger='autorun', cond={'switch': 'PRO_FERRY_DONE'}), page([], cond={'self': 'A'})),
    *strip(ev(GATE, page(SCAN, trigger='touch', cond={'switch': 'PRO_FERRY_DONE'}), page([], cond={'switch': 'PRO_SCANNED_NULL'})), 3),
    *strip(ev("Edda's last call", page([IF('!pfm?(:edda_lastcall)', LAST_CALL)], trigger='touch', cond={'switch': 'PRO_FERRY_DONE'})), 3),
    ev('Captain Edda',
       page([P('EDDA', 'neutral', 'Go on, sprog. Through the gate. I\'ll be here till they chain her.')], SPR['EDDA'], 'left', cond={'switch': 'PRO_FERRY_DONE'}),
       page([P('EDDA', 'angry', 'Impounded! Thirty-one years and they chain her up like a stray Growlithe!', 'anger'),
             P('EDDA', 'deadpan', "I'm told I may apply for compensation. In writing. To the people who did it."),
             P('EDDA', 'neutral', "...You've somewhere to go, sprog? Larch? Good. Up the headland. She'll feed you something terrible."),
             P('EDDA', 'sad', 'You stand at the rail like somebody I used to know. That\'s all. Go on.')],
            SPR['EDDA'], 'left', cond={'switch': 'PRO_SCANNED_NULL'})),
    ev('Calla',
       page([P('CALLA', 'neutral', 'One at a time, please. Hold still.')], SPR['CALLA'], 'down'),
       page([P('CALLA', 'neutral', "The unit's been logged as faulty. Please don't worry about it."),
             P('CALLA', 'neutral', '...Are you feeling well? No fatigue? No pallor?'),
             CH(["I'm fine.", 'Why?'], [[P('CALLA', 'neutral', "Good. That's good. Welcome to Velmora.")],
                                       [P('CALLA', 'panic', "No reason! It's a standard question. It's on the form.", 'sweat')]], cancel=1)],
            SPR['CALLA'], 'down', cond={'switch': 'PRO_SCANNED_NULL'})),
    ev('Aurelian Voss (dock)', page(['A man in a good coat waits at the back of the queue, mug in hand.'], SPR['VOSS'], 'up',
                                    cond={'switch': 'PRO_FERRY_DONE'}), page([], cond={'switch': 'PRO_SCANNED_NULL'})),
    ev('Boy (pier)', page([N('Boy', "I'm going to be red. I've decided.")], 'NPC 02', 'up', cond={'switch': 'PRO_FERRY_DONE'}, through=True),
       page([], cond={'switch': 'PRO_SCANNED_NULL'})),
    ev("Boy's Mother (pier)", page([N("Boy's Mother", "Stay in the queue, love.")], 'NPC 04', 'up', cond={'switch': 'PRO_FERRY_DONE'}, through=True),
       page([], cond={'switch': 'PRO_SCANNED_NULL'})),
    ev('Woman with crate (pier)', page([N('Woman with crate', 'Home. Already I feel less grey.')], 'NPC 22', 'up', cond={'switch': 'PRO_FERRY_DONE'}, through=True),
       page([], cond={'switch': 'PRO_SCANNED_NULL'})),
    sign('Accord plaque', 'A bronze plaque, green with age.\n"EIGHTEEN IN CONCORD, ONE IN KEEPING."\n— The Accord of Velmora, AF 4\nSomeone has bolted a Meridian sunburst to the post beside it. The bolts are new.'),
    # ---- named residents
    ev('Wenna Hale',
       page([IF('!pfm?(:wenna_tart)', WENNA_FIRST, [
           P('WENNA', 'neutral', "My Juno works up at the station. Talks like a kettle. You'll like her. Everyone does, it's exhausting.")])],
           SPR['WENNA'], 'down'),
       page([IF('!pfm?(:wenna_tart)', WENNA_FIRST, [
           P('WENNA', 'happy', 'She named your little group? Of course she did. She named the kettle.')])], SPR['WENNA'], 'down', cond={'switch': 'CH1_STARTER_GOT'}),
       page([IF('!pfm?(:wenna_tart)', WENNA_FIRST), IF("!$game_self_switches[[523, 0, 'BISCUIT']]", BISCUIT_HOME + [S('pfm_set(:biscuit_reward)')], [
           IF('$game_variables[102] < 2', [
               P('WENNA', 'neutral', "Going up to the lighthouse? Give Hesper my love, and don't let her give you any back. Bed's yours whenever.")], [
               P('WENNA', 'sad', "She told me about the orchard. That was the Pruetts' place. They had apples when I was a girl.")])])],
           SPR['WENNA'], 'down', cond={'switch': 'CH1_ORCHARD_DONE'})),
    talk('Coll Hale', SPR['COLL'], 'down',
         [P('COLL', 'neutral', 'Mm. Ferry child.'),
          P('COLL', 'neutral', "Farm's up the lane if you need a bed. Wenna'll say the same but with more words."),
          P('COLL', 'deadpan', "...Did she give you a tart? Then you're family. That's how it works. I didn't make the rules.")],
         after=[({'switch': 'CH1_ORCHARD_DONE'}, [IF("$game_self_switches[[523, 0, 'BISCUIT']] && $game_variables[102] < 2", [
             P('COLL', 'neutral', "Skiddo's called Parsnip. Second Parsnip. First one was a Mudbray. Juno doesn't hold with new names.")], [
             P('COLL', 'neutral', "Orchard went glass the same week my hens stopped laying. Don't know that it's connected. Don't know that it isn't.")])])]),
    ev('Odo',
       page([IF('!pfm?(:odo_rod)', [N('Odo', "You fish? No? Everybody fishes. You just haven't yet."), ITEM('OLDROD'),
                                    N('Odo', "Catch a Magikarp, throw it back, feel superior. That's the whole sport."), S('pfm_set(:odo_rod)')],
                [N('Odo', "Catch a Magikarp, throw it back, feel superior. That's the whole sport.")])], 'trainer_FISHERMAN', 'left'),
       page([IF('!pfm?(:odo_rod)', [N('Odo', "You fish? No? Everybody fishes. You just haven't yet."), ITEM('OLDROD'), S('pfm_set(:odo_rod)')]),
             N('Odo', "Heard the gate went quiet on you. My rod goes quiet on me all the time. Doesn't mean there's nothing there.")],
            'trainer_FISHERMAN', 'left', cond={'switch': 'PRO_SCANNED_NULL'})),
    talk('Harbor Crier', 'NPC 01', 'down', [N('Crier', 'Hear ye! The Strait is closed! The Festival of Champions proceeds as planned, in the autumn, by grace of the Sovereign!'),
                                            N('Crier', "...I don't know how both of those are true either. I just read the card.")]),
    # ---- the station yard: K1, Juno, the send-off
    ev('Kestrel K1', page(K1, SPR['KESTREL'], 'up', cond={'switch': 'CH1_STARTER_GOT'}, trigger='autorun'),
       page([], cond={'switch': 'CH1_K1_DONE'})),
    ev('Juno (lab yard)', page([], cond={'switch': 'CH1_STARTER_GOT'}, through=True),
       page([IF('!pfm?(:juno_errand)', ERRAND, [P('JUNO', 'happy', "Up the lane, past the stile! Biscuit won't wait. Biscuit never waits.")])],
            SPR['JUNO'], 'down', cond={'switch': 'CH1_K1_DONE'}),
       page([], cond={'switch': 'CH1_ORCHARD_DONE'}), page([], cond={'self': 'B'})),
    *strip(ev('Sendoff', page([IF('!pfm?(:ch2_sendoff)', SENDOFF)], trigger='touch', cond={'var': ['STORY_CHAPTER', 2]})), 4),
    ev('Larch (sendoff)', page([]), page([P('LARCH', 'neutral', 'Off you go. Lecture Two is already drafted.')], SPR['LARCH'], 'down', cond={'var': ['STORY_CHAPTER', 2]}),
       page([], cond={'self': 'A'})),
    ev('Juno (sendoff)', page([]), page([P('JUNO', 'happy', 'Saltmere! Forty tarts! A PAGEANT!')], SPR['JUNO'], 'down', cond={'var': ['STORY_CHAPTER', 2]}),
       page([], cond={'self': 'A'})),
    # ---- sidequests
    ev('Girl with Wingull', page(WINGULL_GIRL, 'NPC 16', 'down')),
    ev('Wingull (with girl)', page([]), page(['The Wingull has a bottle cap. It is not sharing.'], 'Followers/WINGULL', 'left', cond={'self': 'A'}, step=True)),
    ev('Wingull (rocks)', page([]),
       page(['The Wingull eyes you. It has a bottle cap in its beak and is very proud of it.',
             CH(['Hold out a Bramble Tart crumb.', 'Just pick it up.'],
                [['It hops onto your arm. It keeps the bottle cap.'], ['It bites you. Then it hops onto your arm anyway.']], cancel=0),
             S('pfm_set(:wingull_found)'), {'selfswitch': ['B', True]}], 'Followers/WINGULL', 'down', cond={'self': 'A'}, step=True),
       page([], cond={'self': 'B'})),
    ev('Lamplighter', page(LAMPLIGHTER, 'NPC 10', 'down')),
    *[quay_lamp(i) for i in range(1, 7)],
    # ---- the lighthouse door (locked until S105)
    {'type': 'door', 'name': 'Lighthouse door', 'link': 'FL_LIGHT', 'locked': {'until': 'CH1_ORCHARD_DONE', 'text': 'Locked. A note: "KESTREL. NO."'}},
    # ---- signs, objects, hidden items
    sign('Town sign', "FERROW'S LANDING — Elowen's Door on the Sea. Pop. 212 and one lighthouse."),
    sign('Festival poster', '"THE FESTIVAL OF CHAMPIONS, AF 300. All Kingdoms. One Blessing." A painted crown floats over eighteen colored banners. The stone in the crown has a tiny dark fleck. Probably a printing fault.', post=False),
    sign('Lane sign', '↑ Tidewatch Station (Prof. I. Larch) · → Hale\'s Bramble · ← Lighthouse (KEEP OUT. THIS MEANS YOU, KESTREL.)'),
    sign('Notice board', '"LOST: one Skwovet, answers to Biscuit. Last seen heading for the old Pruett orchard. Do NOT follow it in. — W. Hale"', post=False),
    sign('Fish barrels', 'Magikarp. They look resigned.', post=False),
    hidden('HiddenItem tart stall', 'ORANBERRY', 'It rolled off the stall. Finders keepers is an old harbor law.'),
    hidden('HiddenItem breakwater', 'PEARL', 'Stuck in a mooring ring. The sea was saving it.'))

# flavor townsfolk straight from the script (the Wingull girl and the Lamplighter are the sidequest events above)
_fl, _, _ = parsed(r'^### Flavor townsfolk \(each', r'^### Signs and objects')
for n in _fl:
    if n['name'] in ('Girl with Wingull', 'Lamplighter'): continue
    add(100, npc_from(n, move='random' if n['name'] in ('Boy with toy boat', 'Twin 1') else 'fixed'))
EVENTS[100]['Twin 2'] = copy.deepcopy(EVENTS[100]['Twin 1']); EVENTS[100]['Twin 2']['name'] = 'Twin 2'
EVENTS[100]['Rope-skipping Girl 2'] = copy.deepcopy(EVENTS[100]['Rope-skipping Girl 1']); EVENTS[100]['Rope-skipping Girl 2']['name'] = 'Rope-skipping Girl 2'
for nm in ('Twin 2', 'Rope-skipping Girl 2', 'Twin 1', 'Rope-skipping Girl 1'):
    for p in EVENTS[100][nm]['pages']: p['move'] = 'fixed'
# the town copies of the ferry passengers (after the scan they are in the village)
add(100, talk('Boy (town)', 'NPC 02', 'down', [N('Boy', 'I\'M GREEN. Did you see? Mum says I can\'t be red as well. I\'m going to be red on Saturdays.')], move='random'),
    talk("Boy's Mother (town)", 'NPC 04', 'down', [N("Boy's Mother", "Two more hours on the road to Briarwick. He'll be green the whole way, and loud about it.")]),
    talk('Woman with crate (town)', 'NPC 22', 'left', [N('Woman with crate', "Home. Already I feel less grey. Don't tell my sister.")]))
for nm in ('Boy (town)', "Boy's Mother (town)", 'Woman with crate (town)'):
    for p in EVENTS[100][nm]['pages']: p['cond'] = {'switch': 'PRO_SCANNED_NULL'}
    EVENTS[100][nm]['pages'].insert(0, page([]))


# ===================================================================================================== 101-108 interiors
NURSE_FL = 'Welcome! We heal Pokémon for free. We can\'t do anything about feelings, but there\'s tea.'
NURSE_BW = 'We heal for free. The scanner at the door is new. It told me I\'m "Insect, Briarwick". I\'ve lived here forty years, I\'d worked it out.'
NO_MON = [IF('$player.party_count == 0', ["\\rOh, you don't have one yet! Come back when you do. I'll act surprised.", {'exit': True}])]

add(101, talk('Trainer at PC', 'NPC 17', 'down', [N('Trainer', 'They put a scanner on our door last week too. Mine says "Insect, Briarwick" every time I come in. I KNOW, door.')]))
MART_FL = [IF('pfm?(:fellowship_off) && !pfm?(:fellowship_on)', [
    N('Mart Clerk', "Want me to switch that card on? ...Signed by WHO?"), {'anim': [0, 3]}, S('pfm_money(3000)'), S('pfm_set(:fellowship_on)')]),
    IF('!pfm?(:fl_mart_hi)', [N('Mart Clerk', "Potions, Poké Balls, Synthetic Seeds. The Seeds are new. Meridian grows them in a lab. Don't plant one. A man planted one. We don't talk about his garden."),
                              S('pfm_set(:fl_mart_hi)')])]
add(102, talk('Shopper', 'NPC 24', 'up', [N('Shopper', 'Synthetic Seeds, a copper each. I bought six. I have not planted them. I look at them.')]))

LARCH_INTRO = [
    'A cluttered station: tide charts, brass instruments, a stove with a blackened kettle. Juno is at a bench, labeling seed packets, back turned.',
    P('LARCH', 'neutral', "If that's the kelp man, the answer is still yes, and I don't care what he's offering.", '', 'Professor Larch'),
    MV('Professor Larch', ['turn_down']), {'wait': 40},
    P('LARCH', 'shocked', '...Oh.', '', 'Professor Larch'),
    P('LARCH', 'neutral', "You've got her chin. Give me the letter.", '', 'Professor Larch'),
    'You hand over Mum\'s letter. Larch reads it.', {'wait': 90}, 'She folds it very carefully and puts it on the bench.',
    P('LARCH', 'sad', 'Last winter. And nobody told me until you were already on a boat.', '', 'Professor Larch'),
    P('LARCH', 'neutral', 'Your mother was the bravest coward I ever knew. Sit.', '', 'Professor Larch'),
    'Larch pours two cups from the kettle. The liquid is dark green.',
    P('LARCH', 'neutral', "Drink. It's disgusting.", '', 'Professor Larch'),
    CH(['Drink it.', 'Pretend to drink it.', '...'], [
        ['It tastes like a harbor at low tide. You keep it down. Barely.',
         P('LARCH', 'happy', "Ha! Nobody finishes the first one. Ines didn't.", '', 'Professor Larch')],
        [P('LARCH', 'deadpan', "I've watched forty people pretend. You're the worst at it.", '', 'Professor Larch')],
        [P('LARCH', 'deadpan', "It doesn't get better if you stare at it. I've tried.", '', 'Professor Larch')]], cancel=3),
    P('LARCH', 'neutral', 'She told you nothing, I take it. "Go to Imelda." That\'s Ines. Hand me a child and a mystery and die before I can shout at her.', '', 'Professor Larch'),
    P('LARCH', 'neutral', 'Did they scan you at the dock?', '', 'Professor Larch'),
    CH(['Yes.', 'It said NULL.'], [
        [P('LARCH', 'angry', "She wrote ONE instruction about that. ...Not your fault. What did it say?", 'anger', 'Professor Larch')],
        [P('LARCH', 'neutral', '...', '', 'Professor Larch')]], cancel=0),
    P('LARCH', 'neutral', 'Null. Right. Well. That\'s that, then.', '', 'Professor Larch'),
    MV('Juno', ['turn_down']), 'A seed packet slides off the bench.',
    P('JUNO', 'shocked', 'Professor, is this— are they— is this the ferry person?!', '', 'Juno'),
    P('LARCH', 'deadpan', "This is \\PN. \\PN, this is Juno Hale, my assistant. She'll tell you about larches now. I can't stop her. Nobody can.", '', 'Professor Larch'),
    P('JUNO', 'happy', "Did you know larches are the only conifers that drop their needles? Every winter they look dead. They're not!", '', 'Juno'),
    P('JUNO', 'happy', "They're just letting go so they don't snap. Professor says it's the most sensible thing a tree's ever done.", '', 'Juno'),
    P('LARCH', 'deadpan', 'I said it once. In 296.', '', 'Professor Larch'),
    P('LARCH', 'neutral', "Right. You can't walk Velmora with empty pockets. Come through to the Sanctuary. Both of you.", '', 'Professor Larch'),
    MV('Professor Larch', ['through_on', 'right', 'right', 'right', 'right', 'right', 'right', 'through_off', 'turn_down']),
    S('pfm_quest_done(:mums_letter)'), SELF('Starter table'), {'selfswitch': ['A', True]}]

STARTER_PICK = (
    "gens = (1..9).to_a\n"
    "g = pbMessage(_INTL(\"Which region's partners?\"), gens.map { |n| _INTL(\"Generation {1}\", n) }, -1)\n"
    "if g >= 0\n"
    "  gen = gens[g]\n"
    "  lines = (0..2).map { |s| Prismfall::Rival.line(gen, s) }\n"
    "  names = lines.each_with_index.map { |l, i| [_INTL(\"Grass: \"), _INTL(\"Fire: \"), _INTL(\"Water: \")][i] + GameData::Species.get(l[0]).name }\n"
    "  s = pbMessage(_INTL(\"Pick a partner.\"), names + [_INTL(\"Back\")], 3)\n"
    "  if s >= 0 && s < 3 && pbAddPokemon(lines[s][0], 5)\n"
    "    Prismfall.record_starter($player.party[-1], gen: gen, slot: s)\n"
    "    pfm_set(:starter_picked)\n"
    "  end\n"
    "end\n")
STARTER_SCENE = [IF('!pfm?(:sanctuary_speech)', [S('pfm_set(:sanctuary_speech)'),
    'A glasshouse full of small Pokémon from every corner of the world, in pens and on perches.',
    P('LARCH', 'neutral', 'The Wayfarer Sanctuary. Twenty years of colleagues abroad sending me Pokémon that weren\'t born here, so I could watch how the Imprints take hold of them.', '', 'Professor Larch'),
    P('LARCH', 'neutral', "They all pick up a tint in a few weeks. Every one. I've never had one that didn't.", '', 'Professor Larch'),
    P('LARCH', 'neutral', '...Never had one.', 'dots', 'Professor Larch'),
    P('LARCH', 'neutral', "Pick a partner. Any of them. Take your time, it's the only decision today I trust you with.", '', 'Professor Larch')]),
    S(STARTER_PICK),
    IF('!pfm?(:starter_picked)', [P('LARCH', 'neutral', 'Take your time. They\'re not going anywhere. Most of them can\'t.', '', 'Professor Larch'), {'exit': True}]),
    P('LARCH', 'happy', 'Good. It liked you before you chose it. I was watching.', '', 'Professor Larch'),
    S('$player.has_pokedex = true'), '\\me[Key item get]\\PN received the Pokédex!',
    'Fitted with a Meridian Imprint Reader. Larch has put tape over half of it.',
    P('JUNO', 'happy', 'My turn! Um. Um um um.', '', 'Juno'),
    MV('Juno', ['right', 'right', 'turn_up', 'wait 10', 'right', 'turn_up']),
    S('sp = GameData::Species.get(Prismfall::Rival.rival_starter_species(:JUNO)).name\n'
      'pbMessage("\\\\pf[JUNO,happy,,Juno]Juno: " + _INTL("This one. {1}. It was looking at me.", sp))'),
    P('LARCH', 'deadpan', "That one's at a disadvantage against \\PN's, Juno.", '', 'Professor Larch'),
    P('JUNO', 'happy', 'Somebody should give the underdog a chance! Also it was LOOKING at me.', '', 'Juno'),
    {'se': 'Player fall'}, 'A crash from the loft. Hay falls.',
    MV('Kestrel (loft)', [{'graphic': [SPR['KESTREL'], 0, 2, 0]}, {'opacity': 255}, 'through_on', 'down', 'down', 'through_off']),
    P('LARCH', 'angry', 'Kestrel Vane. How long have you been sleeping in my hayloft?', 'shock', 'Professor Larch'),
    P('KESTREL', 'deadpan', 'Since Gran changed the lighthouse lock. So, Tuesday.', '', 'Kestrel (loft)'),
    P('KESTREL', 'neutral', "You're handing out partners to ferry tourists now? I've asked you for one for two years.", '', 'Kestrel (loft)'),
    P('LARCH', 'neutral', "You asked me twice, and both times you'd just set something on fire.", '', 'Professor Larch'),
    P('KESTREL', 'smug', 'One of those was an accident.', '', 'Kestrel (loft)'),
    MV('Kestrel (loft)', ['down', 'right', 'turn_up']),
    S('sp = GameData::Species.get(Prismfall::Rival.rival_starter_species(:KESTREL)).name\n'
      'pbMessage("\\\\pf[KESTREL,smug,,Kestrel (loft)]Kestrel: " + _INTL("This one. {1}.", sp))'),
    P('JUNO', 'angry', 'You only picked that because it beats theirs!', '', 'Juno'),
    P('KESTREL', 'deadpan', 'Yes. Fair fights are for people who can afford to lose.', '', 'Kestrel (loft)'),
    {'anim': ['Professor Larch', 3]}, {'wait': 30},
    P('LARCH', 'sad', "...Take it. Your mother would've done the same thing, with the same face.", 'dots', 'Professor Larch'),
    P('KESTREL', 'angry', "Don't talk about her.", 'anger', 'Kestrel (loft)'),
    MV('Kestrel (loft)', ['through_on', 'down', 'down', 'down', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'down', 'down', 'turn_up']),
    P('KESTREL', 'neutral', "Ferry kid. Outside. Let's see if you're worth the boat fare.", '', 'Kestrel (loft)'),
    MV('Kestrel (loft)', ['down', {'opacity': 0}]),
    SW('CH1_STARTER_GOT')]

add(103,
    ev('Professor Larch',
       page([P('LARCH', 'neutral', 'Customs first, child. Meridian gets cross if anyone skips the queue.')], SPR['LARCH'], 'up', cond={'switch': 'LARCH_AT_TIDEWATCH'}),
       page(LARCH_INTRO, SPR['LARCH'], 'up', cond={'switch': 'PRO_SCANNED_NULL'}, trigger='autorun'),
       page([P('LARCH', 'neutral', "Through here. The Sanctuary. Pick a partner, I've got kelp boiling.")], SPR['LARCH'], 'down', cond={'self': 'A'}),
       page([P('LARCH', 'neutral', "Look after that one. And mind Kestrel. He bites, but only when he's frightened.")], SPR['LARCH'], 'down', cond={'switch': 'CH1_STARTER_GOT'}),
       page([P('LARCH', 'neutral', 'Lecture One. I\'m numbering them. Sit down before you fall down.')], SPR['LARCH'], 'down', cond={'switch': 'CH1_ORCHARD_DONE'})),
    ev('Juno', page([P('JUNO', 'happy', 'Seed packets! Every one labelled! Mostly correctly!')], SPR['JUNO'], 'up'),
       page([P('JUNO', 'happy', "You've got a partner! I've got a partner! Everyone's got a partner except the kettle!")], SPR['JUNO'], 'down', cond={'switch': 'CH1_STARTER_GOT'}),
       page([], cond={'switch': 'CH1_K1_DONE'})),
    ev('Kestrel (loft)', page([], through=True), page([], cond={'switch': 'CH1_STARTER_GOT'})),
    ev('Starter table',
       page(['Small Pokémon from every corner of the world, in pens and on perches. Better wait for the Professor.']),
       page(STARTER_SCENE, cond={'self': 'A'}),
       page(['The pens are quieter now. One of the little ones keeps looking at the door.'], cond={'switch': 'CH1_STARTER_GOT'})),
    ev('Rowan Ashby', page([]),
       page([IF('!pfm?(:rowan_met)', [
           'A tall, weathered man is sorting seed trays. Soil under his nails. A small, sickly Phantump sits on his shoulder.',
           P('JUNO', 'happy', "Uncle Rowan! This is \\PN! They came on the ferry and they beat Kestrel — or nearly — and we're a team now!", '', 'Juno (station)'),
           P('ROWAN', 'happy', "Are you, now. Rowan Ashby. I keep the garden at Verdance, and this one's aunt kept me.", '', 'Rowan Ashby'),
           P('ROWAN', 'neutral', "I came down for seed stock. And to check on the Professor's tea plants. They're thriving. I can't account for it.", '', 'Rowan Ashby'),
           P('LARCH', 'deadpan', 'Spite.', '', 'Professor Larch'),
           P('ROWAN', 'neutral', "This is a Phantump. I found it up past Briarwick, in a wood that's gone to glass. It was sitting in a glass tree, crying.", '', 'Rowan Ashby'),
           P('ROWAN', 'sad', "Its tree couldn't die properly, you see. So it couldn't either.", '', 'Rowan Ashby'),
           P('JUNO', 'sad', "That's so sad...", '', 'Juno (station)'),
           P('ROWAN', 'neutral', "It's not sad that things die, Juno. Everything that grows must be allowed to. That's what makes room.", '', 'Rowan Ashby'),
           P('ROWAN', 'neutral', "What's sad is when they're not let.", '', 'Rowan Ashby'),
           'The Phantump drifts off his shoulder and hovers in front of you. It stops shivering.',
           P('ROWAN', 'shocked', "...Well. It hasn't gone near anyone but me in a month.", '', 'Rowan Ashby'),
           P('ROWAN', 'neutral', "She'd have liked you.", '', 'Rowan Ashby'),
           CH(['Who?', '...'], [[P('ROWAN', 'sad', "My wife. Elin. ...She's still in the garden. Come and see it someday.", '', 'Rowan Ashby')],
                                [P('ROWAN', 'neutral', "Hm. You're a good listener. It's rarer than badges.", '', 'Rowan Ashby')]], cancel=2),
           ITEM('MIRACLESEED'), "From the Warden of Verdance's own stock.", S('pfm_set(:rowan_met)')], [
           P('ROWAN', 'neutral', 'The gate at the dock gave me green, same as every year. Twenty-four years of green. A man could get tired of a color.')])],
           SPR['ROWAN'], 'right', cond={'switch': 'CH1_K1_DONE'})),
    ev('Juno (station)', page([]), page([P('JUNO', 'happy', 'Uncle Rowan says the Phantump likes you. It only likes him and compost.')], SPR['JUNO'], 'left', cond={'switch': 'CH1_K1_DONE'}),
       page([], cond={'switch': 'CH1_ORCHARD_DONE'})),
    sign('Station bookshelf', '"Field safety, rule one, underlined three times: NEVER TAKE A TINTED PERSON PAST A VEIL."', post=False),
    sign('Imprint scanner', 'An Imprint scanner hums quietly. Its last reading: NULL.', post=False),
    sign('Kettle', 'A blackened kettle. Something dark green is stewing in it. It smells like low tide, on purpose.', post=False))

INN_REST = [N('Innkeeper', 'Rooms are full of people who came home on the last boat with nowhere to be. First time I\'ve been full since the wedding of \'91.'),
            IF('$game_switches[@@CH1_ORCHARD_DONE] && $game_variables[@@STORY_CHAPTER] < 2', [   # Ch1 close (2026-11-20): no inn bed, the Hales' farm
                N('Innkeeper', "And Wenna Hale's been in. Said if I find you so much as a cot, she stops selling me tarts. I'm not risking the tarts. Farm's up the lane.")], [])]
add(104, ev('Innkeeper', page(INN_REST, 'NPC 21', 'down')),
    talk('Inn Guest', 'NPC 26', 'right', [N('Inn Guest', "I left Velmora nine years ago to be a famous painter. I'm back to be a tired one.")]),
    talk('Inn Guest 2', 'NPC 13', 'left', [N('Inn Guest 2', "The Concert says we carry the Bleed. We don't carry it. It's not a cold. It's the ground.")]))

add(105, sign('Rope coils', 'Coils of rope, older than you. Somebody has spliced every frayed end.', post=False),
    sign('Cot', "A cot with a boy's coat on it. The coat is much too big for the cot.", post=False),
    ev('Cracked mirror', page(['Your reflection, split down the middle by an old crack.', S('pfm_set(:saw_mirror)')])),
    sign('Trunk', 'Locked. A black lace veil is caught in the lid.', post=False))
add(106, ev('Hesper Vane',
            page(['An old woman is polishing the great lamp with a rag. She is shouting down the stairwell.',
                  P('HESPER', 'angry', "—and if I find straw in my good boots AGAIN, Kestrel Vane, I'll—", '', 'Hesper Vane'),
                  MV('Hesper Vane', ['turn_down']), {'anim': ['Hesper Vane', 3]}, 'The rag drops.', {'wait': 60},
                  P('HESPER', 'shocked', '...', 'shock', 'Hesper Vane'),
                  P('HESPER', 'angry', "Who let you up here? Get out. Lighthouse is closed. Sea's closed. Everything's closed.", '', 'Hesper Vane'),
                  CH(['Do you know me?', "I'm sorry.", '...'], [
                      [P('HESPER', 'angry', "I don't know anybody. I'm seventy-eight. I've forgotten more people than you've met.", '', 'Hesper Vane')],
                      [P('HESPER', 'sad', "...Don't be sorry. Sorry's no use to a lamp.", '', 'Hesper Vane')],
                      [P('HESPER', 'sad', 'Stars. You even stand like— no.', '', 'Hesper Vane')]], cancel=3),
                  P('HESPER', 'neutral', "You're the one the boy fought on the quay. He came home swearing. That means he liked it.", '', 'Hesper Vane'),
                  P('HESPER', 'neutral', "Keep away from him. Everyone who gets near that boy's mother's ghost gets hurt.", '', 'Hesper Vane'),
                  MV('Hesper Vane', ['turn_up']), {'selfswitch': ['A', True]}], SPR['HESPER'], 'up', trigger='autorun'),
            page([IF('pfm?(:saw_mirror) && !pfm?(:hesper_mirror)',
                     [P('HESPER', 'angry', 'Leave it. It shows the truth crooked, same as everything.'), S('pfm_set(:hesper_mirror)')],
                     [P('HESPER', 'angry', "Lighthouse is closed. Sea's closed. Everything's closed.")])], SPR['HESPER'], 'up', cond={'self': 'A'})))
add(107, talk('Dockmaster', 'NPC 12', 'down', [N('Dockmaster', "Thirty ferries a month, then one, then none. I'm the Dockmaster of a dock that's master of nothing.")]),
    sign("Dockmaster's ledger", '"AF 290, night crossing, unscheduled. Capt. Morrow. Two passengers, one a child. Fare: paid in kind."\nThe entry has been crossed out twice. You can still read it.', post=False))


# ===================================================================================================== 120 Briarwick
TAMSIN_MEET = [
    MV('Tamsin (square)', ['toward_player']), {'se': 'Player bump'},
    'Silk everywhere.', {'anim': ['Tamsin (square)', 3]},
    P('TAMSIN', 'panic', "Sorry! Sorry — I wasn't — are you hurt? You're not hurt. Sorry.", 'shock', 'Tamsin (square)'),
    P('TAMSIN', 'neutral', "You've a Badge Case. Oh. Oh no. You're a challenger. TODAY?", '', 'Tamsin (square)'),
    P('TAMSIN', 'panic', "It's fine! It's fine. The gym's open. It's just a bit— the moths are— there was a meeting.", 'sweat', 'Tamsin (square)'),
    P('TAMSIN', 'neutral', "I'm Tamsin. Loom. The Warden. Since spring. Come to the Loomhouse when you're ready. Take your time. Please take your time.", '', 'Tamsin (square)'),
    MV('Tamsin (square)', ['through_on', 'right', 'right', 'right', 'right', 'right', 'right', 'right', {'opacity': 0}]),
    S('pfm_set(:met_tamsin)'), {'selfswitch': ['A', True]}]

THISTLE = [
    S('pfm_dusk(30)'),
    'Night. Two grey-cowled figures in carved bark masks are cutting survey stakes with shears. A third stands at the pylon with a hand flat on the brass.',
    MV('Bereaved 1', [{'graphic': ['trainer_CHANNELER', 0, 4, 0]}, {'opacity': 255}], wait=False),
    MV('Bereaved 2', [{'graphic': ['trainer_CHANNELER', 0, 6, 0]}, {'opacity': 255}], wait=False),
    MV('Pallbearer Thistle', [{'graphic': [SPR['THISTLE'], 0, 8, 0]}, {'opacity': 255}]),
    N('Bereaved', "That's the last of the south line."),
    P('THISTLE', 'neutral', 'Leave soil where they stood. Bare. Let something rot there for once.', '', 'Pallbearer Thistle'),
    {'se': 'Voltorb Flip mark'}, 'Snap. A twig, under your foot.',
    {'anim': ['Bereaved 1', 3]}, {'anim': ['Bereaved 2', 3]}, MV('Pallbearer Thistle', ['turn_toward_player'.replace('turn_toward_player', 'face_player')]),
    P('THISTLE', 'angry', "A watcher. Meridian's, or the Warden's?", 'shock', 'Pallbearer Thistle'),
    CH(['Neither.', 'Who are you?', '...'], [
        [P('THISTLE', 'neutral', "Everyone's somebody's. You just haven't been told whose yet.", '', 'Pallbearer Thistle')],
        [P('THISTLE', 'neutral', 'The Hollow. We mourn what this land was. Somebody has to.', '', 'Pallbearer Thistle')],
        [P('THISTLE', 'neutral', "No answer. Then I'll assume the worst. It saves time.", '', 'Pallbearer Thistle')]], cancel=3),
    P('THISTLE', 'sad', "I was a weaver once. Lowmarsh. You won't find it on a map now. It had looms too.", '', 'Pallbearer Thistle'),
    P('THISTLE', 'angry', 'Ask your Warden what she signed!', '', 'Pallbearer Thistle'),
    S('setBattleRule("cannotRun")'),
    IF('TrainerBattle.start(:HOLLOW_THISTLE, "Thistle")', [
        P('THISTLE', 'shocked', "...Your partner doesn't fight like the Wood's got hold of it. It fights like it's standing nowhere at all.", '', 'Pallbearer Thistle'),
        P('THISTLE', 'neutral', 'Let the land grieve, child. And look at the grass by that pylon in daylight.', '', 'Pallbearer Thistle'),
        MV('Bereaved 1', ['through_on', 'right', 'right', {'opacity': 0}], wait=False),
        MV('Bereaved 2', ['through_on', 'right', 'right', {'opacity': 0}], wait=False),
        MV('Pallbearer Thistle', ['through_on', 'right', 'right', 'right', {'opacity': 0}]),
        'The three vanish into the trees. A bark mask is left on the ground.',
        ITEM('BARKMASK', 1, 'Bark Mask'), 'Carved to look like the Gossamer Ogre. It does look sad.',
        SW('CH2_THISTLE_DONE'), S('pfm_day(30)')], [S('pfm_day(10)')])]

LOOM_WEAVER_AFTER = [N('Weaver at loom', 'She told us. All of it, or you did. Either way the looms stopped for a whole minute. First time since the funeral.')]
GRANDMOTHER = [IF('pfm?(:sleeves_done)', [N('Grandmother', 'Sixteen sleeves. I\'m on the fifth. Don\'t rush me.')], [
    IF('pfm_quest?(:sixteen_sleeves)', [
        IF('$bag.quantity(:TINYMUSHROOM) >= 3', [
            S('$bag.remove(:TINYMUSHROOM, 3)'), 'You hand over three Tiny Mushrooms.',
            N('Grandmother', "Lovely. Smells dreadful. Here, I made this one first. It was meant for a Weedle. He evolved. Ungrateful."),
            ITEM('SILKSCARF'), 'Two sleeves. A Kakuna has no use for it.', S('pfm_set(:sleeves_done)'), S('pfm_quest_done(:sixteen_sleeves)')], [
            N('Grandmother', 'Three Tiny Mushrooms. From the wood. Green dye doesn\'t boil itself.'),
            S('pbMessage(_INTL("({1} of 3.)", [$bag.quantity(:TINYMUSHROOM), 3].min))')])], [
        IF('pfm?(:gran_talked)', [
            N('Grandmother', "I've run out of green. The dyer won't sell me less than a bolt. Fetch me three Tiny Mushrooms from the wood and I'll boil my own."),
            QUEST('sixteen_sleeves', 'Sixteen Sleeves', 'Bring three Tiny Mushrooms (0/3).')], [
            N('Grandmother', "It's a jumper for my Caterpie. Sixteen sleeves. I'm on the fourth. Don't rush me."), S('pfm_set(:gran_talked)')])])])]

add(120,
    ev('Arrival', page([
        'A village lashed between tree trunks: rope bridges, treetop houses, bolts of silk drying like flags. At the east edge, orange survey flags march to a half-built brass pylon.',
        S('pfm_juno_part("Juno (arrival)")'),   # (She stops following.)
        MV('Juno (arrival)', [{'graphic': [SPR['JUNO'], 0, 8, 0]}, {'opacity': 255}]),
        P('JUNO', 'happy', "Briarwick! Smell that? That's mulberry and lanolin and— oh, the egg-seller's open. I'll find you at the gym! Don't start without me! Or do! I'll catch up!", 'sparkle', 'Juno (arrival)'),
        MV('Juno (arrival)', ['through_on', 'up', 'up', 'up', 'up', 'up', 'up', {'opacity': 0}]),
        IF('!pfm_gym_won?(:LEADER_TAMSIN)', [SW('GLOAMING_DISGUISED_CELESTINE')]),
        {'selfswitch': ['A', True]}], trigger='autorun'), page([], cond={'self': 'A'})),
    ev('Juno (arrival)', page([], through=True)),
    ev('Stage manager', page([S('if pfm_gym_won?(:LEADER_TAMSIN)\n'
                                '  $game_switches[@@GLOAMING_DISGUISED_CELESTINE] = false if $game_switches[@@GLOAMING_DISGUISED_CELESTINE]\n'
                                '  pbSetSelfSwitch(%EV[Dusk petal]%, "A", true)\n'
                                'end\n'
                                'pbSetSelfSwitch(%EV[Charcoal child]%, "A", true) if $game_switches[@@CH2_MATRIARCH_DONE] && !pfm?(:ch2_close)'),
                              {'erase': True}], trigger='parallel')),
    ev('Tamsin (square)', page(TAMSIN_MEET, SPR['TAMSIN'], 'left', trigger='event_touch'), page([], cond={'self': 'A'})),
    *strip(ev('Pylon watch', page([IF('pfm?(:met_tamsin) && !$game_switches[@@CH2_THISTLE_DONE]', THISTLE)], trigger='touch')), 3),
    ev('Pallbearer Thistle', page([], through=True), page([], cond={'switch': 'CH2_THISTLE_DONE'})),
    ev('Bereaved 1', page([], through=True), page([], cond={'switch': 'CH2_THISTLE_DONE'})),
    ev('Bereaved 2', page([], through=True), page([], cond={'switch': 'CH2_THISTLE_DONE'})),
    talk('Finch', 'NPC 07', 'right', [N('Finch', 'Fourteen dead this week. They fly east at dusk and come back with glass on their wings. Then they don\'t come back.'),
                                      N('Finch', 'Meridian says the Lattice will "stabilize" it. The line they\'ve drawn for it goes straight through my grove.')],
         after=[({'switch': 'CH2_MATRIARCH_DONE'}, [N('Finch', "The ringing's stopped. The moths flew east at dusk and came back clean. Whatever you did in there: thank you. And don't tell me. I don't want to know.")])]),
    ev('Old woman at the shrine',
       page([], through=True),
       page(['A stone shrine: three carved beasts, a dog, a monkey and a pheasant, standing over a broken ogre mask. An old woman in a grey shawl is sweeping it. She is barefoot.',
             N('Old Woman', 'Three loyal hounds and an ogre so bold...'),
             N('Old Woman', '...but who was the thief, when the story was told?'),
             CH(['Who was?', "That's not how the story goes.", '...'], [
                 [N('Old Woman', "Oh, I couldn't say. I could sing it, but I couldn't say.")],
                 [N('Old Woman', "Isn't it? I've only ever told it true. That's the trouble with me.")],
                 [N('Old Woman', "Quiet. Good. You'll hear more that way. Most of it's under the floor.")]], cancel=3),
             N('Old Woman', "You've no color on you, child. Did you know? Like water in a glass."),
             N('Old Woman', 'Walk carefully. Eighteen roads is a long way, and people will want to carry you.'),
             'She goes back to sweeping.'], 'NPC 28', 'up', cond={'switch': 'GLOAMING_DISGUISED_CELESTINE'})),
    ev('Dusk petal', page([]), page([IF('!pfm?(:dusk_petal)', ['A single dusk-colored flower lies on the shrine.', ITEM('DUSKPETAL', 1, 'Dusk Petal'),
                                                             "It's only open at twilight. It's open now. It's noon.", S('pfm_set(:dusk_petal)')],
                                        ['The old woman is gone. The shrine has been swept very clean.'])], cond={'self': 'A'})),
    ev('Charcoal child', page([]), page([
        N('Child', "I circled it. The Crown in the chapel's got a whole stone. This one's got a bit gone. See?"),
        N('Child', 'Mum says the Crown got hurt once.'), N('Child', 'How do you hurt a crown?'), {'wait': 20},
        'Your hand moves, unprompted, to your chest.', {'wait': 40}, S('pfm_set(:ch2_close)'), {'selfswitch': ['B', True]}],
        'NPC 08', 'up', cond={'self': 'A'}),
       page([N('Child', 'How do you hurt a crown? Nobody will tell me.')], 'NPC 08', 'up', cond={'self': 'B'})),
    talk('Rope-bridge Boy', 'NPC 02', 'down', [
        N('Boy', "If you jump on the bridge it goes BWOING. I'm not allowed. You're a grown-up. YOU do it."),
        CH(['Jump.', "Don't."], [[{'se': 'Player jump'}, 'Bwoing.', N('Boy', 'HA!'), N('Voice below', "WHO'S JUMPING?!")],
                                 [N('Boy', 'Coward.')]], cancel=2)]),
    ev('Grandmother knitting', page(GRANDMOTHER, 'NPC 11', 'down')),
    # ---- signs and objects
    sign('Town sign', 'BRIARWICK — Where the Thread Never Tangles.\n(Carved under it, smaller: "Unlike the Guild Accounts.")'),
    sign('Loomhouse sign', 'LOOMHOUSE GYM. WARDEN: Old Mother Loom (painted over) TAMSIN LOOM.\n"A thread holds because it\'s twisted with others."'),
    sign('Festival poster', 'The same poster as the Landing. Here the dark fleck in the Crown\'s stone has been circled in charcoal. Someone has written: "SEE CHAPEL."', post=False),
    ev('Lattice pylon', page([IF('pf_choice(:ch2_tamsin) == :keep_secret',
                                 ['A finished brass pylon, humming. A plate reads: MERIDIAN CONCORD — LATTICE 15 (BRIARWICK) — "Light for Everyone." The grass around it has gone stiff as spun sugar for three yards.'],
                                 [IF('pf_choice(:ch2_tamsin)', ['The half-built pylon stands where it stood. A new chalk line marks a smaller footing, well off the grove.'],
                                     ['Half a brass pylon. A plate reads: MERIDIAN CONCORD — LATTICE 15 (BRIARWICK) — "Light for Everyone." It is faintly warm, and the grass around it is stiff, like spun sugar.'])])])),
    sign('Survey flags', 'Orange cloth on stakes. Four of the stakes have been neatly cut. The cuts are very clean. A weaver\'s shears.', post=False),
    sign('Silk racks', 'The silk moves in no wind at all.', post=False),
    sign('Loyal Three shrine', 'A stone shrine: three carved beasts, a dog, a monkey and a pheasant, standing over a broken ogre mask. Someone keeps it swept.', post=False),
    hidden('HiddenItem rope bridge', 'XATTACK', 'It fell out of someone\'s pocket mid-bwoing.'),
    hidden('HiddenItem dye vats', 'TINYMUSHROOM', 'Dyed Elowen green. Still a mushroom.'),
    warp('To Gossamer Wood', link='WOOD_BRIAR', arrive=[35, 62, 'up']),
    warp('To Gossamer Wood b', to={'map': 524, 'x': 45, 'y': 1, 'dir': 'down'}))   # map builder 9: 524 rebuilt at 90x110

_bt, _, _ = parsed(r'^### Flavor townsfolk$', r'^\*\[after gym, village-wide')
AFTER_GYM = {'Weaver at loom': LOOM_WEAVER_AFTER, 'Dyer': [N('Dyer', "Contract's a contract, says the linesman. So's a pitchfork, says I.")],
             'Tired Mother': [N('Tired Mother', 'Still sleeping well.')]}
for n in _bt:
    if n['name'] in ('Rope-bridge Boy', 'Grandmother knitting'): continue
    e = npc_from(n, move='random' if n['name'] in ('Youngster', 'Apprentice') else 'fixed')
    if n['name'] in AFTER_GYM:    # [after gym]: badge 1 is not a switch, so the reactive line is a branch in each page
        for p in e['pages']:
            p['commands'] = [IF('pfm_gym_won?(:LEADER_TAMSIN)', AFTER_GYM[n['name']], p['commands'])]
    add(120, e)
EVENTS[120]['Boy in dog mask'] = copy.deepcopy(EVENTS[120]['Girl in ogre mask']); EVENTS[120]['Boy in dog mask']['name'] = 'Boy in dog mask'
for nm in ('Girl in ogre mask', 'Boy in dog mask'):
    for i, p in enumerate(EVENTS[120][nm]['pages']):
        p['graphic']['sprite'] = 'NPC 16' if nm.startswith('Girl') else 'NPC 02'


# ===================================================================================================== 121-125 interiors
GALE = [IF('$game_switches[@@CH2_MATRIARCH_DONE] && pfm?(:ch2_close) && !pfm?(:gale2)', [
    'GALE POST. A letter is waiting.', '"Heard about the Hollow. Lecture Two enclosed. It is nine pages. Page nine says I\'m proud of you. Do not skip to page nine. — I.L."',
    S('pfm_set(:gale2)'), {'var': ['STORY_CHAPTER', 4]}], [
    IF('!pfm?(:gale1)', ['GALE POST. A letter is waiting.', '"Lecture Two is drafted. Do not make me send it. Eat something. — I.L."',
                         ITEM('POTION', 2), ITEM('KELPTEABAG', 1, 'Kelp Tea Bag'), 'You could throw it away. You don\'t.', S('pfm_set(:gale1)')],
       ['GALE POST. Write to Tidewatch Station, Ferrow\'s Landing. Larch reads every letter twice and answers half.'])])]
add(121, talk('Trainer', 'NPC 20', 'down', [N('Trainer', "The gym's all webs. Step on the wrong one and it throws you into the net. Tamsin apologises to you all the way down.")]),
    talk('Trainer 2', 'NPC 22', 'left', [N('Trainer', "She fights two at once. Two! Bring a partner that likes company.")]),
    ev('Gale Post desk', page(GALE)))
add(122, talk('Customer', 'NPC 23', 'up', [N('Customer', 'I asked for a Synthetic Seed and the old ladies in the queue went silent. I put it back.')]))
MART_BW = [IF('!pfm?(:bw_mart_hi)', [N('Clerk', "Antidotes go fast here. The moths don't mean it."), S('pfm_set(:bw_mart_hi)')])]

HETT = [IF('$game_switches[@@CH2_MATRIARCH_DONE] && pfm?(:ledger_read) && !pfm?(:hett_reward)', [
    N('Hett', 'From the guild\'s teaching chest. Old Mother Loom would\'ve wanted a stranger to have it. She never trusted us with it.'),
    S('pfm_money(2000)'), ITEM('TMSTRINGSHOT', 1, 'TM String Shot'), S('pfm_set(:hett_reward)'), S('pfm_quest_done(:locked_ledger)')], [
    IF('pfm_gym_won?(:LEADER_TAMSIN)', [N('Hett', "She signed WHAT? Alone? ...Poor fool child. Her gran would've made the whole village sign it with her, and then it'd be all our fault. That's what a guild's FOR.")], [
        IF('pfm?(:ledger_read) && !pfm?(:ledger_told)', [
            N('Hett', "...Alone. She signed it alone. Don't say anything yet. Let me think how to say it kindly. I'm out of practice."), S('pfm_set(:ledger_told)')], [
            IF('pfm?(:hett_talked) && !pfm_quest?(:locked_ledger)', [
                N('Hett', "You're a stranger, so you can do what I can't. The guild ledger's in the Warden's loft and it's locked. Old Mother Loom kept the key in the gym. \"Where the first thread starts,\" she used to say."),
                QUEST('locked_ledger', 'The Locked Ledger', 'Find the ledger key in the Loomhouse.')], [
                IF('pfm_quest?(:locked_ledger)', [N('Hett', 'Where the first thread starts. In the Loomhouse. Mind the planks.')], [
                    N('Hett', 'Old Mother Loom ran this guild forty years and never once missed a moth-count. The girl\'s missed three.'),
                    N('Hett', "I'm not saying she's hiding something. I'm saying the ledger's locked and it never used to be."),
                    S('pfm_set(:hett_talked)')])])])])])]

CONFESS = [
    'The loft: a ledger open on a table, a contract with a gold sunburst seal. Tamsin won\'t sit.',
    IF('pfm?(:ledger_read)', [P('TAMSIN', 'sad', "You've read it. Hett has too. I can tell by how gently she's speaking to me.", '', 'Tamsin (loft)')]),
    P('TAMSIN', 'sad', 'That masked woman at the pylon. She was right. I signed it.', '', 'Tamsin (loft)'),
    P('TAMSIN', 'sad', "Briarwick's bankrupt. It has been for three years. Gran hid it. I found the accounts the week I buried her.", '', 'Tamsin (loft)'),
    P('TAMSIN', 'sad', 'Meridian offered four hundred thousand for "stewardship rights". One pylon. Free light. I signed it by myself, at night, so nobody would have to know how bad it was.', '', 'Tamsin (loft)'),
    P('TAMSIN', 'crying', "And now the Glasswood's walking up the survey line like it was invited. Fourteen moths this week. I count them. I count them every morning.", '', 'Tamsin (loft)'),
    P('TAMSIN', 'sad', "The guild meets tonight. Tell me what to do. Please. I've run out of thread.", '', 'Tamsin (loft)'),
    CH(["Tell them the truth. I'll stand next to you.", "They deserve to know. If you won't say it, I will.", "It's your secret. I won't tell."], [
        [S('pf_choose(:ch2_tamsin, :help_confess)'),
         P('TAMSIN', 'shocked', 'Next to me. Not in front?', '', 'Tamsin (loft)'),
         P('TAMSIN', 'neutral', "...A thread holds because it's twisted with others. I've had that on the SIGN.", '', 'Tamsin (loft)'),
         {'tone': [-255, -255, -255, 0, 20]}, {'wait': 24},
         'The guild meeting. Tamsin speaks. Her voice cracks twice.',
         N('Hett', 'Then we sign it WITH you, girl, and then we tear it up together.'),
         'The contract is renegotiated: a smaller pylon, off the grove.', {'tone': [-8, 8, -18, 0, 20]}, {'wait': 20}],
        [S('pf_choose(:ch2_tamsin, :expose)'),
         P('TAMSIN', 'panic', 'No— wait— not like—', '', 'Tamsin (loft)'),
         {'tone': [-255, -255, -255, 0, 20]}, {'wait': 24},
         'The guild meeting. You lay the contract on the table. Uproar. The looms stop.',
         'Tamsin stands very still, then tears the contract in half herself, in front of them.',
         P('TAMSIN', 'sad', "I'm sorry. I'm so sorry. That's the last time I'll say it tonight.", '', 'Tamsin (loft)'),
         {'tone': [-8, 8, -18, 0, 20]}, {'wait': 20}],
        [S('pf_choose(:ch2_tamsin, :keep_secret)'),
         P('TAMSIN', 'sad', "...Thank you. I think. I'll fix it quietly. I'll find the money somewhere.", '', 'Tamsin (loft)')]], cancel=0),
    P('TAMSIN', 'neutral', "Whatever's making the wood ring, it's in Cocoonfall Hollow, at the Glasswood's heart. I can't cross the Veil. Nobody can.", '', 'Tamsin (loft)'),
    MV('Juno (loft)', [{'graphic': [SPR['JUNO'], 0, 8, 0]}, {'opacity': 255}]),
    P('JUNO', 'neutral', '...They can.', '', 'Juno (loft)'),
    P('TAMSIN', 'shocked', 'What?', 'shock', 'Tamsin (loft)'),
    P('TAMSIN', 'neutral', "Then take this. It was Gran's shuttle. It's only wood. But she never dropped a thread while she held it.", '', 'Tamsin (loft)'),
    ITEM('MOTHERLOOMSSHUTTLE', 1, "Mother Loom's Shuttle"), 'Worn smooth by fifty years of one hand.',
    QUEST('ringing_wood', 'The Ringing Wood', 'Cut through the Deepwood to Cocoonfall Hollow.'),
    {'selfswitch': ['B', True]}]

LEDGER = [IF('pfm?(:ledger_read)', ['The last page: "Received of the Meridian Concord, for stewardship rights, Lattice 15: ₽400,000. Signed, T. Loom, Warden." The line for "Guild witnesses" is blank.'], [
    IF('pfm_has?(:LEDGERKEY)', ['The brass key turns.',
                                'LEDGER, last page: "Received of the Meridian Concord, for stewardship rights, Lattice 15: ₽400,000. Signed, T. Loom, Warden."',
                                'One signature. The line for "Guild witnesses" is blank.', S('pfm_set(:ledger_read)')],
       ['The guild ledger. It\'s locked. It never used to be.'])])]

add(123, ev('Hett', page(HETT, 'NPC 14', 'down')),
    talk('Apprentice (guild)', 'NPC 24', 'right', [N('Apprentice', 'The loft is the Warden\'s. We\'re not to go up. I go up to look at the moths\' tally board. Don\'t tell Hett.')]),
    ev('Guild ledger', page(LEDGER)),
    ev('Loft manager', page([S('pbSetSelfSwitch(%EV[Tamsin (loft)]%, "A", true) if pfm_gym_won?(:LEADER_TAMSIN) && pf_choice(:ch2_tamsin).nil?'), {'erase': True}], trigger='parallel')),
    ev('Tamsin (loft)', page([]), page(CONFESS, SPR['TAMSIN'], 'down', cond={'self': 'A'}),
       page([P('TAMSIN', 'neutral', "Cocoonfall Hollow. Through the Deepwood. The Cutter will open the way. ...Come back, will you?")], SPR['TAMSIN'], 'down', cond={'self': 'B'})),
    ev('Juno (loft)', page([], through=True)),
    sign('Moth tally board', 'A board of chalk tallies, one column per morning. The last column has fourteen strokes, and then the chalk was pressed so hard it snapped.', post=False),
    sign('Silk bolts', 'Bolts of Briarwick silk, every shade of green. None of them has ever tangled. Somebody has labelled one "THE QUEEN\'S (UNPAID)".', post=False))

add(124, talk('Retired Weaver', 'NPC 10', 'down', [N('Retired Weaver', 'I wove Old Mother Loom\'s shroud. She\'d picked the pattern at thirty. "Plan ahead," she said. Tamsin plans ahead too. She plans for everything to go wrong.')]),
    sign('Bookshelf', '"A Child\'s Pageant of the Loyal Three." The last page, where the Ogre is driven out, has been torn away. Someone has drawn the Ogre a little house instead.', post=False),
    sign('Loom', 'A narrow tape loom, threaded with a shroud pattern half a century old. Nobody has woven on it since spring.', post=False),
    # the chapel (second room of 124, own door on 120)
    sign('Chapel mural', 'Eighteen colored stones falling from a white sky into green land. Above them, a silver crown with one clear stone. The stone is whole.', post=False),
    talk('Child in pew', 'NPC 07', 'up', [N('Child', "Mum says the Crown got hurt once. She says don't ask the chaplain. So I'm asking you.")]),
    sign('Chapel window', 'Eighteen panes of colored glass around one clear pane. The clear one has no lead around it, as if it were added first.', post=False))

add(125, ev('Cutter', page([N('Cutter', 'No.'), {'selfswitch': ['A', True]}], 'trainer_HIKER', 'down'),
            page([N('Cutter', "...What's the tree?"),
                  IF('pfm_gym_won?(:LEADER_TAMSIN)',
                     [IF('!pfm?(:hm_cut)', [N('Cutter', "Right. Here. Cut the dead ones. If you cut a live one I'll know. I won't know how. I'll just know."),
                                            ITEM('HM01'), S('pfm_set(:hm_cut)')],
                         [N('Cutter', "Dead ones only. I'll know.")])],
                     [N('Cutter', "Come back with the Warden's badge. I don't hand Cut to people the wood hasn't met.")])],
                 'trainer_HIKER', 'down', cond={'self': 'A'})),
    sign('Axe rack', 'Four axes, sharpened to different moods.', post=False))
