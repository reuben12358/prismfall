#!/usr/bin/env python3
"""Trials wiring audit: is every Trial quest and event Pokemon actually on a map?  Writes design/TRIALS_WIRING.md.

    python3 -I tools/trials_wiring.py [--baseline scan.json] [--baseline-data data.json] [--save-scan scan.json]

For every quest (plugins/Prismfall Trials, read through `ruby tools/trials_docs.rb --json`) it follows the TALK keys its
scenes are reached by to the map events that call them:
  * built     - the key is called by an event in a built map (maps_out/Data/Map*.rxdata),
  * queued    - the key is in that map's spec (mapgen/specs) or in mapgen/trial_overlay.py, so the next build.py run lays
                it (the spec exists; the built file predates the data),
  * requested - the key's map (design/TRIAL_EVENTS.yaml) has no spec yet: a map builder places it (mapgen/REQUESTS.md),
  * missing   - the map has a spec but nothing calls the key: the quest is "not placed" (fix the overlay/layout or post
                a request). The exit status is 1 when a Chapter 0-5 quest is not placed.
A quest is "in maps" when all its keys are built, "next build" when they're built or queued, "needs maps" when any key
waits on an unbuilt map. --baseline compares with an earlier --save-scan of maps_out (the "before" column), and
--baseline-data with an earlier `trials_docs.rb --json` (quests that didn't exist then read "new", stubs "designed").
"""
import json, os, re, subprocess, sys, glob
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MG = os.path.join(ROOT, 'mapgen')
sys.path.insert(0, MG)
import rmarshal as M                      # noqa: E402  (our own pure-Python RXDATA reader)

KEY_RE = re.compile(r'pf_trial_(?:talk|ready\?)\(:(\w+)\)')


def s(x):
    return x.decode('utf-8', 'replace') if isinstance(x, bytes) else str(x)


def scan_built():
    """map id -> set of TALK keys called by its built events"""
    out = {}
    for fn in sorted(glob.glob(os.path.join(ROOT, 'maps_out', 'Data', 'Map*.rxdata'))):
        mid = int(re.search(r'Map(\d+)\.rxdata$', fn).group(1))
        mp = None
        for _ in range(5):                    # a map builder may be writing the file right now: wait and retry
            try:
                mp = M.load_file(fn)
                break
            except (ValueError, EOFError, IndexError):
                import time
                time.sleep(2)
        if mp is None:
            print('warning: could not read %s' % fn)
            continue
        keys = set()
        for ev in mp.events.values():
            for pg in ev.pages:
                for c in pg.list:
                    if c.code in (355, 655) or (c.code == 111 and c.parameters and c.parameters[0] == 12):
                        keys |= set(KEY_RE.findall(s(c.parameters[1] if c.code == 111 else c.parameters[0])))
        out[mid] = keys
    return out


def scan_specs():
    """map id -> set of TALK keys in its spec, plus the trial_overlay events and patches laid over it"""
    out = {}
    for f in sorted(glob.glob(os.path.join(MG, 'specs', '*.yaml'))):
        for sp in yaml.safe_load_all(open(f, encoding='utf-8')):
            if sp and 'id' in sp:
                out.setdefault(sp['id'], set()).update(KEY_RE.findall(json.dumps(sp.get('events', []))))
    import trial_overlay as T
    for mid, evs in T.EVENTS.items():
        if mid in out:
            out[mid].update(KEY_RE.findall(json.dumps(evs, default=str)))
    for mid, pats in T.PATCHES.items():
        if mid in out:
            out[mid].update(pats.values())
    return out


def badge_tier(unlock):
    return max([int(n) for n in re.findall(r'badges\s*>=\s*(\d+)', unlock or '')] or [0])


def main():
    args = sys.argv[1:]
    data = json.loads(subprocess.run(['ruby', os.path.join(ROOT, 'tools', 'trials_docs.rb'), '--json'],
                                     capture_output=True, text=True, check=True, cwd=ROOT).stdout)
    maps = {m['id']: m for m in json.load(open(os.path.join(ROOT, 'design', 'maps.json')))['maps']}
    spec = yaml.safe_load(open(os.path.join(ROOT, 'design', 'TRIAL_EVENTS.yaml'), encoding='utf-8'))
    key_maps = {}
    for mid, m in spec['maps'].items():
        for e in m.get('events') or []:
            if e.get('key'):
                key_maps.setdefault(e['key'], set()).add(int(mid))
    built = scan_built()
    if '--save-scan' in args:
        json.dump({k: sorted(v) for k, v in built.items()}, open(args[args.index('--save-scan') + 1], 'w'))
    base = None
    if '--baseline' in args:
        base = {int(k): set(v) for k, v in json.load(open(args[args.index('--baseline') + 1])).items()}
    specs = scan_specs()

    def keys_of(d):
        out = {}
        for key, t in d['talk'].items():
            for qid, _c, _sc in t['rows']:
                out.setdefault(qid, set()).add(key)
        return out
    q_keys = keys_of(data)
    old = None
    if '--baseline-data' in args:
        old = json.load(open(args[args.index('--baseline-data') + 1]))
        old_q = {q['id']: q for q in old['quests']}
        old_keys = keys_of(old)

    def key_state(key, scan):
        mids = key_maps.get(key, set())
        if any(key in scan.get(m, set()) for m in mids):
            return 'built'
        if any(key in specs.get(m, set()) for m in mids):
            return 'queued'
        if mids and all(m not in specs for m in mids):
            return 'requested'
        return 'missing'

    def quest_state(q, scan, qk=None):
        if q['stub']:
            return 'designed'
        ks = (qk if qk is not None else q_keys).get(q['id'], set())
        if not ks:
            return 'no events'
        st = {k: key_state(k, scan) for k in ks}
        if all(v == 'built' for v in st.values()):
            return 'in maps'
        if scan is not built:
            return 'partly' if any(v == 'built' for v in st.values()) else 'not in maps'
        if any(v == 'missing' for v in st.values()):
            return 'not placed'
        if any(v == 'requested' for v in st.values()):
            return 'needs maps' if not any(v == 'built' for v in st.values()) else 'partly, needs maps'
        return 'next build'

    rows = []
    for q in data['quests']:
        ks = sorted(q_keys.get(q['id'], set()))
        mids = sorted({m for k in ks for m in key_maps.get(k, set())} | ({q['map']} if q['map'] else set()))
        now = quest_state(q, built)
        before = ''
        if base is not None:
            if old is None:
                before = quest_state(q, base)
            elif q['id'] not in old_q:
                before = 'new'
            else:
                before = quest_state(old_q[q['id']], base, old_keys)
        waiting = sorted({m for k in ks for m in key_maps.get(k, set()) if m not in specs})
        rows.append(dict(q=q, ks=ks, mids=mids, now=now, before=before, waiting=waiting,
                         tier=badge_tier(q['unlock']), queued=[k for k in ks if key_state(k, built) == 'queued']))

    def mapcell(m):
        tag = 'built' if m in built else ('spec' if m in specs else ('planned' if m in maps else '?'))
        return '%d %s' % (m, tag)

    out = ['# TRIALS_WIRING - which Trial quests and event Pokemon are really on the maps', '',
           '> **Generated** by `python3 -I tools/trials_wiring.py` from the plugin data (`ruby tools/trials_docs.rb --json`), '
           '`design/TRIAL_EVENTS.yaml`, the built maps (`maps_out/Data`), the map specs (`mapgen/specs`) and '
           '`mapgen/trial_overlay.py`. Re-run it after a map build.',
           '> **Status:** *in maps* = every map event the quest needs is in a built map; *next build* = the events are in the '
           'specs or `trial_overlay.py` and the next `build.py` run lays them; *needs maps* = a map it needs is not built '
           'yet (its events are in `mapgen/REQUESTS.md`); *designed* = a `:stub`, no scenes yet. '
           '*not placed* = its map is built or specced but no event calls it. **Tier** = the badges its unlock needs. Maps: *built* / *spec* (spec, not built) / *planned* (maps.json only).', '']
    chapters = sorted({r['q']['chapter'] for r in rows if r['q']['chapter'] is not None and r['q']['chapter'] <= 5})
    out += ['## Chapters 0-5 at a glance', '',
            '| Ch | Quests | Designed only | In maps' + (' (before)' if base is not None else '') + ' | In maps now | Next build | Needs maps |',
            '|---|---|---|---|---|---|---|' if base is not None else '|---|---|---|---|---|---|']
    if base is None:
        out[-2] = '| Ch | Quests | Designed only | In maps now | Next build | Needs maps |'
    for ch in chapters:
        rs = [r for r in rows if r['q']['chapter'] == ch]
        c = lambda st, key='now': sum(1 for r in rs if r[key] == st)
        cells = [str(ch), str(len(rs)), str(c('designed'))]
        if base is not None:
            cells.append(str(c('in maps', 'before')))
        cells += [str(c('in maps')), str(c('next build')), str(sum(1 for r in rs if 'needs maps' in r['now']))]
        out.append('| ' + ' | '.join(cells) + ' |')
    out += ['', '## Every quest', '',
            '| Quest | Trial | Ch | Tier | Maps | Keys | ' + ('Before | ' if base is not None else '') + 'Now | Notes |',
            '|---|---|---|---|---|---|---|---|' + ('---|' if base is not None else '')]
    for r in sorted(rows, key=lambda r: (r['q']['chapter'] if r['q']['chapter'] is not None else 99, r['q']['trial'], r['q']['id'])):
        q = r['q']
        notes = []
        if r['queued']:
            notes.append('queued: ' + ', '.join(r['queued']))
        if r['waiting']:
            notes.append('waits on map ' + ', '.join(str(m) for m in r['waiting']))
        cells = ['**%s** `%s`' % (q['title'], q['id']), q['trial'].title(), str(q['chapter']), str(r['tier']),
                 ', '.join(mapcell(m) for m in r['mids']), ' '.join('`%s`' % k for k in r['ks'])]
        if base is not None:
            cells.append(r['before'])
        cells += [r['now'], '; '.join(notes)]
        out.append('| ' + ' | '.join(cells) + ' |')
    qstate = {r['q']['id']: r['now'] for r in rows}
    out += ['', '## Event and quest-reward Pokemon', '',
            '| Pokemon | Kind | Ch | Badges | Map | Quest | Quest now |', '|---|---|---|---|---|---|---|']
    for m in sorted(data['mons'], key=lambda m: (m['chapter'] if m['chapter'] is not None else 99, m['id'])):
        sp = m['species'].title() + (' (form %s)' % m['form'] if m['form'] else '')
        mp = mapcell(m['map']) if m['map'] else '(rank reward)'
        out.append('| `%s` %s | %s | %s | %s | %s | %s | %s |' % (
            m['id'], sp, m['kind'], m['chapter'], '' if m['badges'] is None else m['badges'], mp,
            '`%s`' % m['quest'] if m['quest'] else '', qstate.get(m['quest'], 'rank reward' if not m['quest'] else '?')))
    path = os.path.join(ROOT, 'design', 'TRIALS_WIRING.md')
    open(path, 'w', encoding='utf-8').write('\n'.join(out) + '\n')
    bad = [r['q']['id'] for r in rows if r['now'] == 'not placed']
    early_bad = [r['q']['id'] for r in rows if r['now'] == 'not placed' and (r['q']['chapter'] or 99) <= 5]
    print('design/TRIALS_WIRING.md: %d quests, %d in maps, %d next build, %d need maps, %d designed%s' % (
        len(rows), sum(r['now'] == 'in maps' for r in rows), sum(r['now'] == 'next build' for r in rows),
        sum('needs maps' in r['now'] for r in rows), sum(r['now'] == 'designed' for r in rows),
        ('; not placed: ' + ', '.join(bad)) if bad else ''))
    return 1 if early_bad else 0


if __name__ == '__main__':
    sys.exit(main())
