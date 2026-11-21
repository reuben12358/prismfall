#!/usr/bin/env python3
"""Fill data placeholders in the walkthrough template from the dumps in /tmp/wt.
Placeholders (one per line or inline):
  {{ENC:id}}            encounter table (base v0 + badge tiers + Bleed-spread v1 note)
  {{ENCLINE:id}}        one-line encounter summary (design-only maps)
  {{ITEMS:id}}          item balls and hidden items on a built map
  {{TRAINERS:id}}       route / gym trainers on a built map
  {{TEAM:TYPE|Name|v}}  full team table (Standard) + Hard / Casual lines
  {{TEAMLINE:TYPE|Name|v}} one-line team
  {{QUESTS:ch}}         side quests from the Trials catalogue for that chapter
  {{STONES:ch}}         Mega Stones / Z-crystals placed for that chapter (design tables)
  {{FIELD:id}}          the map's default field (FIELD_DEFAULTS.yaml)
"""
import json, re, sys

W = '/tmp/wt/'
names = json.load(open(W + 'names.json'))
enc = json.load(open(W + 'enc.json'))
evs = json.load(open(W + 'map_events.json'))
trs = json.load(open(W + 'trainers.json'))
quests = json.load(open(W + 'quests.json'))
stones = json.load(open(W + 'stones.json'))
maps = {m['id']: m for m in json.load(open('/home/claude/fangame/design/maps.json'))['maps']}
built = set(json.load(open('/home/claude/fangame/maps_out/manifest.json'))['built'])

# field display names from FIELDS.md headers
FIELDNAME = {'NONE': 'none'}
for line in open('/home/claude/fangame/design/FIELDS.md', encoding='utf-8'):
    m = re.match(r'^## (.+?) \(`:(\w+)`\)', line)
    if m: FIELDNAME[m.group(2)] = m.group(1).replace(' Field', '')
FIELDNAME['ASHEN_WASTE'] = 'Cinderglass (`:ASHEN_WASTE`)'

def fname(fid):
    if not fid: return 'none'
    n = FIELDNAME.get(fid, fid)
    return n if '`' in n else '%s (`:%s`)' % (n, fid) if fid != 'NONE' else 'none'

FORMNAMES = {}
_cur = None
for _l in open('/home/claude/ref/ebdx/PBS/pokemon_forms.txt', encoding='utf-8-sig'):
    _m = re.match(r'^\[(\w+),(\d+)\]', _l)
    if _m: _cur = '%s_%s' % (_m.group(1), _m.group(2)); continue
    _m = re.match(r'^FormName\s*=\s*(.+)$', _l.strip())
    if _m and _cur: FORMNAMES[_cur] = _m.group(1).strip()

def sp(s):
    if s in names['species']: return names['species'][s]
    m = re.match(r'^(\w+?)_(\d+)$', s)
    if m and m.group(1) in names['species']:
        fn = FORMNAMES.get(s)
        base = names['species'][m.group(1)]
        if fn:
            fn = fn.replace(' Form', '').replace(' Forme', '')
            return '%s %s' % (fn, base) if fn.split()[0] in ('Alolan', 'Galarian', 'Hisuian', 'Paldean') else '%s (%s)' % (base, fn)
        return '%s (form %s)' % (base, m.group(2))
    return s.title()

def item(i):
    if not i: return ''
    if re.match(r'^(TM|HM)\d+$', i):
        return '%s %s' % (i, names['tm_moves'].get(i, ''))
    return names['items'].get(i, i.title())

def mv(m): return names['moves'].get(m, m.title())
def ab(a): return names['abilities'].get(a, a.title())
def tclass(t): return names['ttypes'].get(t, t.replace('_', ' ').title())

SWITCH = {}
for line in open('/home/claude/fangame/design/FLAGS.md', encoding='utf-8'):
    m = re.match(r'^\| S(\d+) \| (\w+) \|', line)
    if m: SWITCH[m.group(1)] = m.group(2)

# ---------------------------------------------------------------- encounters
METHOD = {
    'Land': 'Grass', 'LandDay': 'Grass (day)', 'LandNight': 'Grass (night)', 'LandMorning': 'Grass (morning)',
    'Cave': 'Cave', 'Water': 'Surf (Surf from Badge 6)', 'OldRod': 'Old Rod', 'GoodRod': 'Good Rod (Ebbmouth, Ch4)',
    'SuperRod': 'Super Rod (Rimeholt, Ch11; planned)', 'HeadbuttLow': 'Headbutt (low trees)',
    'HeadbuttHigh': 'Headbutt (high trees)', 'RockSmash': 'Rock Smash (from Badge 2)',
}

def lvl(a, b): return '%d' % a if a == b else '%d–%d' % (a, b)

def merge_rows(rows):
    """Combine duplicate species in one table (same species listed twice)."""
    out = {}
    order = []
    for c, s, a, b in rows:
        if s in out:
            oc, oa, ob = out[s]; out[s] = (oc + c, min(oa, a), max(ob, b))
        else:
            out[s] = (c, a, b); order.append(s)
    return [(out[s][0], s, out[s][1], out[s][2]) for s in order]

def enc_cells(types, pct=True, night_split=False):
    cells = []
    for t, rows in types.items():
        rows = merge_rows(rows)
        meth = METHOD.get(t, t)
        if t == 'Land' and 'LandNight' in types: meth = 'Grass (morning / day)'
        body = ', '.join('%s %s (%s)' % (sp(s), lvl(a, b), ('%d%%' % c) if pct else ('≈%d%%' % c)) for c, s, a, b in sorted(rows, key=lambda r: -r[0]))
        cells.append((meth, body))
    return cells

def ENC(mid):
    k = '%d,0' % mid
    if k not in enc['base']:
        return '_No wild table for this map in `pbs/encounters.txt` yet._'
    v = enc['base'][k]
    out = ['| Method | Pokémon (levels, rate) |', '|---|---|']
    for meth, body in enc_cells(v['types']):
        out.append('| %s | %s |' % (meth, body))
    tiers = sorted((int(t.split(',')[1]), tv) for t, tv in enc['tiers'].items() if int(t.split(',')[0]) == mid)
    for ver, tv in tiers:
        b = ver % 100
        parts = []
        for t, rows in tv['types'].items():
            lab = {'Land': '', 'LandNight': 'night: ', 'Cave': '', 'OldRod': 'Old Rod: ', 'GoodRod': 'Good Rod: ', 'HeadbuttHigh': 'Headbutt (high): ', 'HeadbuttLow': 'Headbutt (low): ', 'Water': 'Surf: '}.get(t, t + ': ')
            parts.append(lab + ', '.join('%s %s (rare, +%d)' % (sp(s), lvl(a, bb), c) for c, s, a, bb in rows))
        out.append('| **After Badge %d** (added) | %s |' % (b, '; '.join(parts)))
    k1 = '%d,1' % mid
    if k1 in enc['base']:
        v1 = enc['base'][k1]
        allrows = [r for rows in v1['types'].values() for r in rows]
        lo = min(r[2] for r in allrows); hi = max(r[3] for r in allrows)
        out.append('| **Act IV on** (Bleed-spread table, version 1) | %s (Lv %s) |' % (', '.join(sp(r[1]) for r in merge_rows(allrows)[:8]), lvl(lo, hi)))
    return '\n'.join(out)

def ENCLINE(mid):
    k = '%d,0' % mid
    if k not in enc['base']:
        return '_no wild table yet_'
    v = enc['base'][k]
    parts = []
    for t, rows in v['types'].items():
        rows = merge_rows(rows)
        meth = METHOD.get(t, t).split(' (')[0]
        if t == 'LandNight': meth = 'night'
        if t in ('SuperRod',): continue
        top = sorted(rows, key=lambda r: -r[0])
        parts.append('%s: %s' % (meth, ', '.join('%s %s' % (sp(s), lvl(a, b)) for c, s, a, b in top)))
    return '; '.join(parts)

# ---------------------------------------------------------------- items
def hidden_desc(name):
    n = name
    n = re.sub(r'^HiddenItem\s*', '', n).strip()
    n = n.strip('()').strip()
    return n

def ITEMS(mid):
    rows = evs.get(str(mid), [])
    vis, hid = [], []
    for e in rows:
        for s in e['scripts']:
            m = re.search(r'pbItemBall\(:(\w+)(?:,\s*(\d+))?', s)
            if not m: continue
            nm = item(m.group(1)) + (' ×%s' % m.group(2) if m.group(2) else '')
            at = '%d,%d' % tuple(e['at'])
            if e['g'] == '':
                d = hidden_desc(e['name'])
                if d.lower() in (item(m.group(1)).lower(), 'item', m.group(1).lower()): d = ''
                hid.append('%s (%s%s)' % (nm, (d + ', ') if d and d.lower() != 'item' else '', at))
            else:
                vis.append('%s (%s)' % (nm, at))
            break
    out = []
    out.append('- **Items:** ' + (' · '.join(vis) if vis else 'none on the map'))
    out.append('- **Hidden items:** ' + (' · '.join(hid) if hid else 'none'))
    return '\n'.join(out)

# ---------------------------------------------------------------- trainers
def team_short(key, starter=False):
    t = trs[key]
    parts = []
    for m in t['mons']:
        s = sp(m['sp'])
        if starter and m['sp'] in STARTERS: s = '*rival starter* (%s line)' % sp(STARTER_ROOT[m['sp']])
        parts.append('%s %d' % (s, m['lv']))
    return ', '.join(parts)

def tlabel(t, n):
    c = tclass(t)
    return c if n.lower() == c.split()[-1].lower() else '%s %s' % (c, n)

def TRAINERS(mid):
    rows = evs.get(str(mid), [])
    seen = []
    out = []
    for e in rows:
        for s in e['scripts']:
            m = re.search(r'TrainerBattle\.start\((.*)\)\s*$', s)
            if not m: continue
            parts = re.findall(r':(\w+),\s*"([^"]+)"(?:,\s*(\d+))?', m.group(1))
            key = tuple(parts)
            if not parts or key in seen: continue
            seen.append(key)
            if len(parts) == 2:
                (t1, n1, v1), (t2, n2, v2) = parts
                k1 = '%s|%s|%d' % (t1, n1, int(v1 or 0)); k2 = '%s|%s|%d' % (t2, n2, int(v2 or 0))
                out.append('- **%s** + **%s** (double): %s / %s' % (tlabel(t1, n1), tlabel(t2, n2), team_short(k1), team_short(k2)))
            else:
                t1, n1, v1 = parts[0]
                k1 = '%s|%s|%d' % (t1, n1, int(v1 or 0))
                dbl = ' (double)' if t1 == 'TWINS' or '&' in n1 else ''
                out.append('- **%s**%s: %s' % (tlabel(t1, n1), dbl, team_short(k1)))
    if not out: return '- **Trainers:** none on the map'
    return '- **Trainers** (Standard; Hard +1 level, Casual −1):\n' + '\n'.join('    ' + o for o in out)

# ---------------------------------------------------------------- teams
STARTER_ROOT = {}
for root, line in (('BULBASAUR', ['BULBASAUR', 'IVYSAUR', 'VENUSAUR']), ('CHARMANDER', ['CHARMANDER', 'CHARMELEON', 'CHARIZARD']), ('SQUIRTLE', ['SQUIRTLE', 'WARTORTLE', 'BLASTOISE'])):
    for x in line: STARTER_ROOT[x] = root
STARTERS = set(STARTER_ROOT)
RIVALS = ('RIVAL_KESTREL', 'RIVAL_JUNO', 'LEADER_JUNO')

def moves_of(m):
    return ', '.join(mv(x) for x in m.get('Moves', '').split(',') if x) or '(level-up moves)'

def TEAM(spec):
    typ, name, ver = spec.split('|'); ver = int(ver)
    key = '%s|%s|%d' % (typ, name, ver)
    if key not in trs: return '_Team `%s` not found in pbs/trainers.txt._' % key
    t = trs[key]
    rival = typ in RIVALS
    out = []
    bag = t.get('items', '')
    out.append('| Pokémon | Lv | Item | Ability | Moves |')
    out.append('|---|---|---|---|---|')
    for m in t['mons']:
        s = sp(m['sp'])
        if rival and m['sp'] in STARTERS:
            s = '**Starter**†'
        nick = (' "%s"' % m['Name']) if m.get('Name') else ''
        abil = ab(m['Ability']) if m.get('Ability') else ('(slot %s)' % m.get('AbilityIndex', 0))
        mvs = '(regenerated for the swapped species)' if (rival and m['sp'] in STARTERS) else moves_of(m)
        out.append('| %s%s | %d | %s | %s | %s |' % (s, nick, m['lv'], item(m.get('Item', '')) or '—', abil, mvs))
    extra = []
    if bag: extra.append('Bag: ' + ', '.join(item(x.strip()) for x in bag.split(',') if x.strip()))
    ivs = sorted(set(m.get('IV', '') for m in t['mons']) - {''})
    if ivs: extra.append('IV ' + '/'.join(ivs))
    if extra: out.append('\n*%s.*\n' % '; '.join(extra))
    for off, lab in ((100, 'Hard'), (200, 'Casual')):
        k2 = '%s|%s|%d' % (typ, name, ver + off)
        if k2 in trs:
            out.append('- **%s:** %s' % (lab, team_line(k2, rival)))
        elif off == 200 or off == 100:
            out.append('- **%s:** no separate team (Core falls back to Standard).' % lab)
    if rival:
        out.append('\n† The rival\'s starter is written as the Gen 1 line in PBS; Prismfall Core swaps it at battle start for the same-generation counterpart of your starter (same stage).')
    return '\n'.join(out)

def team_line(key, rival=False):
    t = trs[key]
    parts = []
    for m in t['mons']:
        s = sp(m['sp'])
        if rival and m['sp'] in STARTERS: s = 'Starter'
        it = item(m.get('Item', ''))
        parts.append('%s %d%s' % (s, m['lv'], (' @' + it) if it else ''))
    return ', '.join(parts)

def TEAMLINE(spec):
    typ, name, ver = spec.split('|'); ver = int(ver)
    key = '%s|%s|%d' % (typ, name, ver)
    if key not in trs: return '_`%s` not in pbs/trainers.txt_' % key
    return team_line(key, typ in RIVALS)

# ---------------------------------------------------------------- quests
def unlock_text(u):
    u = u.strip('`')
    u = re.sub(r'switch\((\d+)\)', lambda m: 'S%s %s' % (m.group(1), SWITCH.get(m.group(1), '')), u)
    u = u.replace('badges >= ', 'Badges ≥ ').replace('&&', 'and')
    return u

def REWARD(r):
    r = re.sub(r'\b([A-Z][A-Z0-9]{2,})\b', lambda m: item(m.group(1)) if m.group(1) in names['items'] or re.match(r'^(TM|HM)\d+$', m.group(1)) else m.group(1), r)
    return r

def QUESTS(ch):
    rows = [q for q in quests if q['ch'] == str(ch)]
    if not rows: return '_No Trial quests are catalogued for this chapter._'
    out = []
    for q in rows:
        what = re.sub(r'\*\*Twist:\*\*.*', '', q['what']).strip()
        status = 'wired (playable)' if q['status'] == 'wired' else 'designed (not wired yet)'
        out.append('- **%s** (`%s`, %s; %s). %s. Unlock: %s. %s Reward: %s.' % (
            q['name'], q['id'], q['trial'].split(' — ')[0], status, q['giver'].replace(' · ', ', '), unlock_text(q['unlock']), what if what.endswith(('.', '."', '!', '?', '!"', '?"')) else what + '.', REWARD(q['reward'])))
    return '\n'.join(out)

# ---------------------------------------------------------------- stones
def chap_of_map(mid):
    m = maps.get(mid)
    if not m: return 0
    s = m.get('segment')
    if s is None: return 0
    return 1 if s == 0 else s + 2

def STONES(ch):
    out = []
    for r in stones:
        if r['item'].startswith('Aggronite') or r['item'] == 'Eevium Z': continue
        c = max(r['badges'] + 2, chap_of_map(r['map']) if r['map'] else 0)
        if c != ch: continue
        kind = 'Mega Stone' if r['kind'] == 'stone' else 'Z-crystal'
        out.append('- **%s** (%s, from Badge %d): %s. %s.%s' % (r['item'], kind, r['badges'], re.sub(r'\s*\(\d+\)\s*$', '', r['where']), r['how'].replace('`', ''),
                   '' if r['map'] in built else ' *(planned: map not built)*' if r['map'] else ''))
    if not out: return '_None placed for this chapter._'
    return '\n'.join(out)

def TRLIST(spec):
    lines = []
    for i in [int(x) for x in spec.split(',')]:
        t = TRAINERS(i)
        for l in t.splitlines()[1:]:
            lines.append('- ' + l.strip()[2:] + ' *(map %d)*' % i)
    return '\n'.join(lines)

EVM = json.load(open(W + 'eventmons.json'))
def EVENTMONS(ch):
    out = []
    for r in EVM:
        if r['ch'] != str(ch): continue
        mon = re.sub(r'\s*`\w+`\s*$', '', r['mon']).strip()
        mon = re.sub(r' — .*$', '', mon)
        out.append('- %s: %s, %s. %s%s' % (mon, r['kind'], re.sub(r'\s*\(\d*\)\s*$', '', r['where']), r['how'].rstrip('.') + '.', '' if r['status'] == 'implemented' else ' *(designed, not implemented)*'))
    return '\n'.join(out) if out else '_None this chapter._'

def AREAS(spec):
    ids = [int(x) for x in spec.split(',') if x.strip()]
    out = ['| Map (ID) | Field | Built? | Wild Pokémon (from `pbs/encounters.txt`) |', '|---|---|---|---|']
    for i in ids:
        m = maps.get(i, {'name': '?'})
        out.append('| %s (%d) | %s | %s | %s |' % (m['name'], i, FIELD(i), 'yes' if i in built else 'no', ENCLINE(i)))
    return '\n'.join(out)

def FIELD(mid):
    return fname(names['fields'].get(str(mid)))

def BUILT(mid):
    return 'built' if int(mid) in built else 'not built'

FUN = {'ENC': lambda a: ENC(int(a)), 'ENCLINE': lambda a: ENCLINE(int(a)), 'ITEMS': lambda a: ITEMS(int(a)),
       'TRAINERS': lambda a: TRAINERS(int(a)), 'TEAM': TEAM, 'TEAMLINE': TEAMLINE, 'QUESTS': lambda a: QUESTS(int(a)),
       'STONES': lambda a: STONES(int(a)), 'FIELD': FIELD, 'BUILT': BUILT, 'AREAS': AREAS, 'TRLIST': TRLIST, 'EVENTMONS': lambda a: EVENTMONS(int(a))}

def render(text):
    def rep(m):
        f, a = m.group(1), m.group(2)
        return FUN[f](a)
    return re.sub(r'\{\{(\w+):([^}]+)\}\}', rep, text)

if __name__ == '__main__':
    src, dst = sys.argv[1], sys.argv[2]
    txt = render(open(src, encoding='utf-8').read())
    # Python-Markdown needs a blank line before a list that follows a paragraph or table
    lines, fixed, fence = txt.split('\n'), [], False
    LIST = re.compile(r'^(- |\d+\. )')
    for ln in lines:
        if ln.startswith('```'): fence = not fence
        if not fence and LIST.match(ln) and fixed:
            prev = fixed[-1]
            if prev.strip() and not LIST.match(prev) and not prev.startswith('    ') and not prev.startswith('>'):
                fixed.append('')
        fixed.append(ln)
    txt = '\n'.join(fixed)
    left = re.findall(r'\{\{[^}]+\}\}', txt)
    if left: print('UNRESOLVED', left[:10])
    open(dst, 'w', encoding='utf-8').write(txt)
    print('wrote', dst, len(txt.splitlines()), 'lines')
