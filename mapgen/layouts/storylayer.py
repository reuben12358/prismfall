"""storylayer: write a story layer's events into specs another layout owns, without touching anything else.

A story layer (story_interlude1.py, story_ch8.py) is a list of events plus extra pages for events the map's own
layout placed. `patch(spec_file, map_id, events, pages, tag)` upserts them by name into that map's `events:` list:
  * an event of the layer replaces the event of the same name (or is appended); its dict gets `story: <tag>`;
  * an event the layer tagged before and no longer makes is dropped;
  * `pages` = {event name: [page, ...]}: appended to that (foreign) event, each page tagged `story: <tag>` so a
    re-run replaces them instead of stacking;
  * every other key, tile and event of the spec stays byte for byte (only the `events:` block is re-dumped).
Idempotent. Run the layer again after any layout that regenerates the spec from scratch."""
import copy, os
import yaml

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def merge(evs, events, pages, tag):
    names = {e['name'] for e in events}
    evs[:] = [e for e in evs if e.get('story') != tag or e.get('name') in names]
    for new in events:
        new = dict(new, story=tag)
        i = next((k for k, e in enumerate(evs) if e.get('name') == new['name']), None)
        if i is None: evs.append(new)
        else: evs[i] = new
    for name, extra in (pages or {}).items():
        e = next((e for e in evs if e.get('name') == name), None)
        if e is None: raise SystemExit('storylayer %s: no event %r to add pages to' % (tag, name))
        if e.get('type') != 'event': raise SystemExit('storylayer %s: %r is not a paged event' % (tag, name))
        e['pages'] = [p for p in e['pages'] if p.get('story') != tag] + [dict(p, story=tag) for p in extra]
    return evs


def patch(spec_file, mid, events, pages=None, tag='story'):
    path = os.path.join(HERE, 'specs', spec_file)
    chunks = open(path, encoding='utf-8').read().split('\n---\n')
    for i, chunk in enumerate(chunks):
        doc = yaml.safe_load(chunk)
        if not doc or doc.get('id') != mid: continue
        lines = chunk.split('\n')
        k = next(n for n, l in enumerate(lines) if l.startswith('events:'))
        # a top-level key after `events:` (261's `take_events:`) stays where it is, byte for byte
        end = next((n for n in range(k + 1, len(lines)) if lines[n] and not lines[n].startswith((' ', '-', '#'))), len(lines))
        rest = lines[end:]
        evs = merge(doc.get('events') or [], events, pages, tag)
        body = yaml.safe_dump({'events': evs}, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True)
        chunks[i] = ('\n'.join(lines[:k]) + '\n' + body.rstrip('\n') + ('\n' + '\n'.join(rest) if rest else '')
                     + ('\n' if i == len(chunks) - 1 and not rest else ''))
        open(path, 'w', encoding='utf-8').write('\n---\n'.join(chunks))
        return len(evs)
    raise SystemExit('storylayer %s: no map %d in %s' % (tag, mid, path))


def sync_pages(spec_file, mid, source, names, tag='story'):
    """For a map whose spec another layout regenerates WITHOUT re-reading the story source (608: Gemini's craft carries
    the old events over): copy the pages of the named events from `source` ({name: event}, e.g. story_ch5.EVENTS[608])
    into the spec's events of the same name. Position, type and every other event stay as they are."""
    path = os.path.join(HERE, 'specs', spec_file)
    text = open(path, encoding='utf-8').read()
    doc = yaml.safe_load(text)
    if doc.get('id') != mid: raise SystemExit('storylayer %s: %s is not map %d' % (tag, spec_file, mid))
    evs = doc['events']
    for n in names:
        e = next((e for e in evs if e.get('name') == n), None)
        if e is None: raise SystemExit('storylayer %s: no event %r on map %d' % (tag, n, mid))
        e['pages'] = [{k: v for k, v in p.items() if k != '_placed'} for p in source[n]['pages']]
    lines = text.split('\n')
    k = next(i for i, l in enumerate(lines) if l.startswith('events:'))
    body = yaml.safe_dump({'events': evs}, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True)
    open(path, 'w', encoding='utf-8').write('\n'.join(lines[:k]) + '\n' + body)
    return len(names)


def _splice(cmds, mapping, hits):
    out = []
    for c in cmds or []:
        if isinstance(c, str) and c in mapping:
            out.extend(mapping[c]); hits[c] = hits.get(c, 0) + 1
            continue
        if isinstance(c, dict):
            c = dict(c)
            for k in ('then', 'else'):
                if k in c: c[k] = _splice(c[k], mapping, hits)
            if 'branches' in c: c['branches'] = [_splice(b, mapping, hits) for b in c['branches']]
        out.append(c)
    return out


def replace_lines(spec_file, mid, mapping, tag='story'):
    """Stage directions in events another layout writes: every message line equal to a key of `mapping` (anywhere in
    any page, inside ifs and choices) is replaced by that key's list of commands. Re-runnable: once replaced, the old
    line is gone, so a second run changes nothing; after the owning layout regenerates the spec, run it again.
    Returns {old line: times replaced}."""
    path = os.path.join(HERE, 'specs', spec_file)
    chunks = open(path, encoding='utf-8').read().split('\n---\n')
    for i, chunk in enumerate(chunks):
        doc = yaml.safe_load(chunk)
        if not doc or doc.get('id') != mid: continue
        hits = {}
        evs = doc.get('events') or []
        for e in evs:
            if 'pages' in e:
                e['pages'] = [dict(p, commands=_splice(p.get('commands'), mapping, hits)) for p in e['pages']]
            elif 'commands' in e:
                e['commands'] = _splice(e['commands'], mapping, hits)
        if not hits: return hits
        lines = chunk.split('\n')
        k = next(n for n, l in enumerate(lines) if l.startswith('events:'))
        tail = [l for l in lines[k + 1:] if l and not l.startswith((' ', '-', '#'))]
        if tail: raise SystemExit('storylayer %s: `events:` is not the last key of map %d (%s)' % (tag, mid, tail[0]))
        body = yaml.safe_dump({'events': evs}, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True)
        chunks[i] = '\n'.join(lines[:k]) + '\n' + body.rstrip('\n') + ('\n' if i == len(chunks) - 1 else '')
        open(path, 'w', encoding='utf-8').write('\n---\n'.join(chunks))
        return hits
    raise SystemExit('storylayer %s: no map %d in %s' % (tag, mid, path))


def set_pages_at(spec_file, mid, at, pages, tag='story', name=None):
    """set_pages for ONE event found by its position (several of a map's events can share a name, e.g. Gemini's
    "Trainer(3)"): it becomes a paged event with these pages, tagged, at the same position; `name` renames it (so
    scenes can address it). Re-runnable."""
    path = os.path.join(HERE, 'specs', spec_file)
    chunks = open(path, encoding='utf-8').read().split('\n---\n')
    for i, chunk in enumerate(chunks):
        doc = yaml.safe_load(chunk)
        if not doc or doc.get('id') != mid: continue
        evs = doc.get('events') or []
        e = next((e for e in evs if list(e.get('at') or []) == list(at)), None)
        if e is None: raise SystemExit('storylayer %s: no event at %r on map %d' % (tag, at, mid))
        new = [dict(copy.deepcopy(p), story=tag) for p in pages]
        if e.get('pages') == new and e.get('type') == 'event' and (name is None or e.get('name') == name): return 0
        for k in [k for k in e if k not in ('name', 'at')]: del e[k]
        if name: e['name'] = name
        e['type'] = 'event'; e['pages'] = new          # pages tagged, the event not: patch() must never drop it
        lines = chunk.split('\n')
        k = next(j for j, l in enumerate(lines) if l.startswith('events:'))
        body = yaml.safe_dump({'events': evs}, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True)
        chunks[i] = '\n'.join(lines[:k]) + '\n' + body.rstrip('\n') + ('\n' if i == len(chunks) - 1 else '')
        open(path, 'w', encoding='utf-8').write('\n---\n'.join(chunks))
        return 1
    raise SystemExit('storylayer %s: no map %d in %s' % (tag, mid, path))


def set_pages(spec_file, mid, name, pages, tag='story'):
    """Give EVERY event called `name` on the map (a door three tiles wide is three events) these pages, tagged; the
    events keep their position and type. Re-runnable. Returns how many events changed."""
    path = os.path.join(HERE, 'specs', spec_file)
    chunks = open(path, encoding='utf-8').read().split('\n---\n')
    for i, chunk in enumerate(chunks):
        doc = yaml.safe_load(chunk)
        if not doc or doc.get('id') != mid: continue
        evs = doc.get('events') or []
        n = 0
        for e in evs:
            if e.get('name') != name: continue
            new = [dict(copy.deepcopy(p), story=tag) for p in pages]     # a copy each: no YAML anchors between doors
            if e.get('pages') != new or e.get('type') != 'event':
                e['type'] = 'event'; e['pages'] = new; n += 1
        if not n: return 0
        lines = chunk.split('\n')
        k = next(j for j, l in enumerate(lines) if l.startswith('events:'))
        body = yaml.safe_dump({'events': evs}, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True)
        chunks[i] = '\n'.join(lines[:k]) + '\n' + body.rstrip('\n') + ('\n' if i == len(chunks) - 1 else '')
        open(path, 'w', encoding='utf-8').write('\n---\n'.join(chunks))
        return n
    raise SystemExit('storylayer %s: no map %d in %s' % (tag, mid, path))
