"""scriptpour: read townsfolk, signs and hidden items out of story/20_SCRIPT_CH0-2.md (the final early-game script) and
turn them into event dicts for the layout scripts. Only the mechanical parts are parsed: `[name: X] line`,
`[portrait: X, expr] line`, `LABEL: text` object lines and `HIDDEN ITEM (...): ITEM. "text"`. Cutscenes (MOVE:, choices,
battle calls, reactive [after ...] variants) are NOT parsed; those stay hand-written in the layout scripts."""
import os, re, zlib
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# SPINE Revision 14 split the early script: 20_SCRIPT_CH0-2.md (Prologue, Ch1, Ch2 Saltmere) and 21_SCRIPT_CH3.md
# (Ch3 Briarwick). Both are read, in order, so section() finds Briarwick's "### Flavor townsfolk" in the second file.
SCRIPTS = ['20_SCRIPT_CH0-2.md', '21_SCRIPT_CH3.md']
LINES = []
for _name in SCRIPTS:
    _path = os.path.join(ROOT, 'story', _name)
    if os.path.exists(_path):
        LINES += open(_path, encoding='utf-8').read().split('\n')
SPR = ['NPC %02d' % i for i in (2, 4, 6, 9, 10, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 26, 27, 29)]
KEY = (('Meridian', 'trainer_SCIENTIST'), ('Sailor', 'trainer_SAILOR'), ('Deserter', 'trainer_SAILOR'), ('Fish', 'trainer_FISHERMAN'),
       ('Net-mender', 'trainer_FISHERMAN'), ('Youngster', 'trainer_YOUNGSTER'), ('Chaplain', 'trainer_GENTLEMAN'),
       ('Clerk', 'trainer_GENTLEMAN'), ('Merchant', 'trainer_GENTLEMAN'))


def section(start_pat, end_pat):
    a = next(i for i, l in enumerate(LINES) if re.search(start_pat, l))
    b = next(i for i in range(a + 1, len(LINES)) if re.search(end_pat, LINES[i]))
    return LINES[a + 1:b]


def sprite(name):
    for k, s in KEY:
        if k in name: return s
    return SPR[zlib.crc32(name.encode()) % len(SPR)]


def parse(lines, per_speaker=False):
    """-> (npcs, signs, items). npcs: {name, first: [text], again: [text]}; signs: {name, text}; items: {item, text, where}."""
    npcs, signs, items = [], [], []; cur = None; again = False
    for l in lines + ['']:
        l = l.strip()
        if not l or l.startswith('```') or l.startswith('#') or l.startswith('**') or l.startswith('*['):
            cur = None; again = False; continue
        if l.startswith('(Talk again'): again = True; continue
        m = re.match(r'HIDDEN ITEM \(([^)]*)\): ([A-Z ]+?)[.:] *"?(.*?)"?$', l)
        if m:
            items.append({'item': m.group(2).replace(' ', ''), 'where': m.group(1), 'text': m.group(3)}); continue
        parts = re.split(r'(?=\[(?:name|portrait|bubble): )', l)
        got = False
        for p in parts:
            m = re.match(r'\[(name|portrait|bubble): ([^\],]+)(?:, *([^\]]+))?\] *(.*)', p)
            if not m: continue
            got = True; kind, who, expr, text = m.groups(); text = text.strip(); ag = again
            m2 = re.match(r'\((again)\) *(.*)', text)
            if m2: ag = True; text = m2.group(2)
            if re.match(r'\((before|after|with|no ) ?[^)]*\)', text): text = re.sub(r'^\([^)]*\) *', '', text)
            text = re.sub(r'\*\(([^)]*)\)\*', '', text).strip()
            if kind == 'bubble':   # [bubble: WHO, expr, emote] -> the opt-in speech bubble (SPINE Rev 22)
                f = [x.strip() for x in (expr or 'neutral').split(',')]
                line = '\\pfb[%s,%s,%s]%s: %s' % (who.upper(), f[0], '+'.join(f[1:]), who.title(), text)
            else:
                line = ('\\pf[%s,%s]%s: %s' % (who.upper(), expr.strip(), who.title(), text)) if kind == 'portrait' else '%s: %s' % (who, text)
            if per_speaker and cur is not None and cur['name'].split(' (later)')[0] != who: cur = None
            if cur is None:
                if any(n['name'] == who for n in npcs): cur = {'name': who + ' (later)', 'first': [], 'again': [], 'dup': True}
                else: cur = {'name': who, 'first': [], 'again': []}
                npcs.append(cur)
            (cur['again'] if ag else cur['first']).append(line)
        if got: continue
        m = re.match(r'([A-Z][A-Z\' \-]+?)(?: \[NEW\])?(?: \(([^)]*)\))?: (.*)', l)
        if m and not l.startswith('MOVE') and not l.startswith('SE:') and not l.startswith('BGM'):
            signs.append({'name': m.group(1).title(), 'text': m.group(3)}); cur = None; continue
        if l.startswith('(Received') and cur is not None: cur['first'].append(l)
    return [n for n in npcs if not n.get('dup')], signs, items


def npc_event(n, at, sprite_name=None, d='down', move='fixed'):
    g = {'sprite': sprite_name or sprite(n['name']), 'dir': d}
    if n['again']:
        pages = [{'graphic': g, 'move': move, 'commands': n['first'] + [{'selfswitch': ['A', True]}]},
                 {'cond': {'self': 'A'}, 'graphic': g, 'move': move, 'commands': n['again']}]
    else:
        pages = [{'graphic': g, 'move': move, 'commands': n['first']}]
    return {'type': 'event', 'name': n['name'], 'at': list(at), 'pages': pages}


def sign_event(s, at, post=True):
    return {'type': 'sign', 'name': s['name'], 'at': list(at), 'post': post, 'text': s['text']}
