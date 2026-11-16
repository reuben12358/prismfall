#!/usr/bin/env python3
"""Prismfall map generator: specs/*.yaml -> maps_out/Data/MapNNN.rxdata + previews + PBS + MapInfos entries.
usage: python3 -I build.py [spec ids or file names ...] [--no-preview]
Everything is regenerated from the specs; see design/MAPGEN.md."""
import sys, os, glob, json, copy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import yaml
import numpy as np
import rmarshal as M
import rjson
import rpg as G
import terrain as T

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, 'maps_out')
TILESET_NAMES = {'Outside': 1, 'Interior general': 3, 'Inside': 3, 'Poke Centre interior': 4, 'Poké Center': 4,
                 'Mart interior': 5, 'Poké Mart': 5, 'Caves': 6, 'Dungeon cave': 7, 'Boat': 9,
                 'Department store interior': 10, 'Factory interior': 11, 'Gyms interior': 14, 'Gyms': 14,
                 'Harbour interior': 15, 'Mansion interior': 16, 'Museum interior': 18, 'Ruins interior': 19,
                 'Trainer Tower interior': 20, 'Dungeon forest': 23, 'Bike shop interior': 8}
FACING = {'down': 2, 'left': 4, 'right': 6, 'up': 8}


class Ctx:
    def __init__(self):
        self.stamps = json.load(open(os.path.join(HERE, 'data', 'stamps.json')))
        self.palettes = {}
        self.specs = {}
        self.doors = {}   # link -> (map, x, y)   exterior door tiles
        self.exits = {}   # link -> (map, x, y)   interior exit mats
        self.warnings = []

    def palette(self, name):
        if name not in self.palettes:
            self.palettes[name] = yaml.safe_load(open(os.path.join(HERE, 'palettes', name + '.yaml')))
        return self.palettes[name]

    def warn(self, mid, msg):
        self.warnings.append('map %s: %s' % (mid, msg))


def load_template(name):
    return json.load(open(os.path.join(HERE, 'data', 'templates', name + '.json')))


def stretch(layers, events, axis, at, count):
    """Duplicate row/column `at` `count` times (axis 'x' or 'y'); shifts events after it."""
    if count <= 0:
        return layers
    if axis == 'x':
        col = layers[:, :, at:at + 1]
        layers = np.concatenate([layers[:, :, :at + 1]] + [col] * count + [layers[:, :, at + 1:]], axis=2)
        for e in events:
            if e.x > at: e.ivars['x'] = e.x + count
    else:
        row = layers[:, at:at + 1, :]
        layers = np.concatenate([layers[:, :at + 1, :]] + [row] * count + [layers[:, at + 1:, :]], axis=1)
        for e in events:
            if e.y > at: e.ivars['y'] = e.y + count
    return layers


# ----------------------------------------------------------------------------- pass 1: geometry + links
def prepare(spec, ctx):
    mid = spec['id']
    spec.setdefault('events', [])
    if 'template' in spec:
        t = load_template(spec['template'])
        layers = np.array(t['layers'], dtype=np.int32)
        evs = [rjson.from_j(e) for e in t['events']]
        drop = set(spec.get('drop_template_events', []))
        evs = [e for e in evs if e.name not in drop]
        for st in spec.get('stretch', []):
            layers = stretch(layers, evs, st[0], st[1], st[2])
        for ed in spec.get('tile_edits', []):   # [layer, x, y, tile] or [layer, x, y, w, h, tile]
            if len(ed) == 4: layers[ed[0], ed[2], ed[1]] = ed[3]
            else: layers[ed[0], ed[2]:ed[2] + ed[4], ed[1]:ed[1] + ed[3]] = ed[5]
        spec['_layers'] = layers
        spec['_tevents'] = evs
        spec['_tileset'] = t['tileset']
        spec.setdefault('bgm', t.get('bgm', ''))
        # template exit -> link
        if 'exit_link' in spec:
            ex = next((e for e in evs if e.name == 'Exit'), None)
            if ex is None:
                ctx.warn(mid, 'template has no Exit event')
            else:
                evs.remove(ex)
                ee = {'type': 'exit', 'at': [ex.x, ex.y], 'link': spec['exit_link']}
                if 'exit_arrive' in spec: ee['arrive'] = spec['exit_arrive']
                spec['events'].insert(0, ee)
    else:
        pal = ctx.palette(spec.get('palette', 'outside'))
        lines = [l for l in spec['map'].strip('\n').split('\n')]
        p = T.Painter(pal, lines, seed=spec.get('seed', mid), warn=lambda m: ctx.warn(mid, m))
        layers = p.paint()
        spec['_painter'] = p
        spec['_tileset'] = pal['tileset']
        for s in spec.get('stamps', []):
            st = ctx.stamps[s['stamp']]
            x, y = s['at']
            sl = np.array(st['layers'], dtype=np.int32)
            h, w = sl.shape[1:]
            if x < 0 or y < 0 or x + w > layers.shape[2] or y + h > layers.shape[1]:
                ctx.warn(mid, 'stamp %s at %s out of bounds' % (s['stamp'], s['at'])); continue
            for z in range(3):
                reg = layers[z, y:y + h, x:x + w]
                m = sl[z] > 0
                reg[m] = sl[z][m]
                if z == 0:  # building footprint: clear decorative layers the terrain put there
                    pass
            # clear tree canopy etc. on layer 2 where the stamp has layer-1 tiles but no layer-2 tile
            l2 = layers[2, y:y + h, x:x + w]; l2[(sl[1] > 0) & (sl[2] == 0)] = 0
            if 'door' in st:
                dx, dy = st['door']
                gfx = st.get('door_gfx', ['doors1', 0, 2])
                ev = {'type': 'door', 'at': [x + dx, y + dy], 'gfx': gfx, 'name': s.get('name', s['stamp'] + ' door')}
                if 'link' in s: ev['link'] = s['link']
                if 'to' in s: ev['to'] = s['to']
                if s.get('locked'):
                    ev = {'type': 'sign', 'at': [x + dx, y + dy], 'post': False, 'name': ev['name'],
                          'text': s.get('locked_text', 'The door is locked.')}
                spec['events'].append(ev)
        for t in spec.get('tiles', []):   # explicit tile placements {tile: name|id, at: [x,y], layer}
            tdef = pal['tiles'].get(t['tile']) if isinstance(t['tile'], str) else {'tile': t['tile'], 'layer': t.get('layer', 1)}
            layers[t.get('layer', tdef['layer']), t['at'][1], t['at'][0]] = tdef['tile']
        spec['_layers'] = layers
        spec['_tevents'] = []
    if 'tileset' in spec:
        ts = spec['tileset']
        spec['_tileset'] = TILESET_NAMES.get(ts, ts) if isinstance(ts, str) else ts
    H, W = spec['_layers'].shape[1:]
    spec['_size'] = (W, H)
    for e in spec['events']:
        if e['type'] == 'door' and 'link' in e:
            if e['link'] in ctx.doors: ctx.warn(mid, 'duplicate door link %s' % e['link'])
            ctx.doors[e['link']] = (mid, e['at'][0], e['at'][1])
        if e['type'] == 'exit':
            arr = e.get('arrive', [e['at'][0], e['at'][1] - 1, 'up'])
            ctx.exits[e['link']] = (mid, arr[0], arr[1], arr[2] if len(arr) > 2 else 'up')
        if e['type'] == 'warp' and 'link' in e:
            arr = e.get('arrive', [e['at'][0], e['at'][1] - 1, 'up'])
            ctx.exits.setdefault(e['link'], (mid, arr[0], arr[1], arr[2] if len(arr) > 2 else 'up'))


# ----------------------------------------------------------------------------- pass 2: events
def pages_from(e, ctx, mid):
    t = e['type']
    gfx = lambda: G.graphic(e.get('sprite', ''), FACING.get(e.get('dir', 'down'), 2), e.get('pattern', 0))
    cond = page_cond(e.get('cond'))
    if t == 'door':
        tgt = resolve_target(e, ctx, mid, door=True)
        char, pat, d = e.get('gfx', ['doors1', 0, 2])
        pg = G.door_pages(char, pat, d, tgt)
        return pg
    if t in ('exit', 'warp'):
        tgt = resolve_target(e, ctx, mid, door=False)
        se = e.get('se', 'Door exit') if t == 'exit' else e.get('se', None)
        return G.warp_pages(tgt, se=se, fade=e.get('fade', False))
    if t == 'npc':
        cmds = e.get('commands') or [{'text': e.get('text', '...')}]
        return [G.page(cond=cond, gfx=gfx(), trigger=G.TRIGGERS[e.get('trigger', 'action')],
                       move_type=G.MOVES[e.get('move', 'fixed')], freq=e.get('freq', 3), through=e.get('through', False),
                       step_anime=e.get('step_anime', False), dir_fix=e.get('dir_fix', False),
                       cmds=G.compile_cmds(cmds))]
    if t == 'sign':
        return [G.page(cond=cond, cmds=G.compile_cmds(e.get('commands') or [{'text': e.get('text', '')}]))]
    if t == 'item':
        return G.item_pages(e['item'], e.get('hidden', False))
    if t == 'trainer':
        tt, tn = e['trainer'][0], e['trainer'][1]
        ver = e['trainer'][2] if len(e['trainer']) > 2 else 0
        return G.trainer_pages(e.get('sprite', 'trainer_' + tt), tt, tn, ver, e.get('intro', '...'),
                               after=e.get('after', '...'), direction=FACING.get(e.get('dir', 'down'), 2),
                               rules=e.get('rules'), cond=cond)
    if t == 'mart':
        items = e['items']
        script = 'pbPokemonMart([\n' + ''.join('  :%s,\n' % i for i in items[:-1]) + '  :%s\n])' % items[-1]
        cmds = [{'text': e.get('greeting', 'Welcome! How may I serve you?')}] if e.get('greeting') else []
        return [G.page(gfx=gfx(), cmds=G.compile_cmds(cmds + [{'script': script}]))]
    if t == 'berry':   # same as the base project's berry plants (Map005)
        b = e['berry']
        return [G.page(gfx=G.graphic('berrytree_' + b, 8), walk_anime=False, step_anime=True, dir_fix=True,
                       cmds=G.compile_cmds([{'script': 'pbPickBerry(:%s, %d)' % (b, e.get('count', 2))}])),
                G.page(cond=G.condition(self_sw='A'), walk_anime=False, step_anime=True,
                       cmds=G.compile_cmds([{'script': 'pbBerryPlant'}]))]
    if t == 'pc':
        return [G.page(cmds=G.compile_cmds([{'script': 'pbPokeCenterPC'}]))]
    if t == 'event':
        out = []
        for p in e['pages']:
            g = p.get('graphic', {})
            out.append(G.page(cond=page_cond(p.get('cond')),
                              gfx=G.graphic(g.get('sprite', ''), FACING.get(g.get('dir', 'down'), 2), g.get('pattern', 0),
                                            tile_id=g.get('tile', 0)),
                              trigger=G.TRIGGERS[p.get('trigger', 'action')], move_type=G.MOVES[p.get('move', 'fixed')],
                              through=p.get('through', False), dir_fix=p.get('dir_fix', False),
                              step_anime=p.get('step_anime', False), on_top=p.get('on_top', False),
                              cmds=G.compile_cmds(p.get('commands', []))))
        return out
    raise ValueError('unknown event type %s' % t)


def page_cond(c):
    if not c:
        return None
    return G.condition(switch1=c.get('switch'), switch2=c.get('switch2'), var=c.get('var'), self_sw=c.get('self'))


def resolve_target(e, ctx, mid, door):
    if 'to' in e:
        to = dict(e['to'])
        to.setdefault('dir', 'up' if door else 'retain')
        return to
    link = e.get('link')
    if door:   # exterior door -> arrive 1 tile above the interior exit mat (or the exit's 'arrive' spot)
        if link in ctx.exits:
            m, x, y, d = ctx.exits[link]
            return {'map': m, 'x': x, 'y': y, 'dir': d}
    else:      # interior exit -> stand on the exterior door (door event animates the step out)
        if link in ctx.doors:
            m, x, y = ctx.doors[link]
            return {'map': m, 'x': x, 'y': y, 'dir': 'retain'}
    ctx.warn(mid, 'unresolved link %r at %s (warp points to itself)' % (link, e.get('at')))
    return {'map': mid, 'x': e['at'][0], 'y': e['at'][1], 'dir': 'retain'}


def build_map(spec, ctx):
    mid = spec['id']
    W, H = spec['_size']
    layers = spec['_layers']
    events = {}
    tev = spec['_tevents']
    nid = 1
    for ev in tev:
        events[ev.id] = ev
        nid = max(nid, ev.id + 1)
    occupied = {(ev.x, ev.y): ev.id for ev in tev}
    pal = ctx.palette(spec.get('palette', 'outside')) if 'map' in spec else None
    for e in spec['events']:
        x, y = e['at']
        if not (0 <= x < W and 0 <= y < H):
            ctx.warn(mid, 'event %s out of bounds %s' % (e.get('name', e['type']), e['at'])); continue
        if (x, y) in occupied:
            ctx.warn(mid, 'two events at %d,%d (%s)' % (x, y, e.get('name', e['type'])))
        if e['type'] == 'sign' and e.get('post', True) and pal and 'sign' in pal.get('tiles', {}):
            tdef = pal['tiles'][e.get('post_tile', 'sign')]
            layers[tdef['layer'], y, x] = tdef['tile']
        name = e.get('name') or default_name(e)
        events[nid] = G.event(nid, name, x, y, pages_from(e, ctx, mid))
        occupied[(x, y)] = nid
        nid += 1
    bgm = spec.get('bgm', '')
    m = G.rmap(spec['_tileset'], W, H, G.table3(layers), events, bgm=bgm, encounter_step=spec.get('encounter_step', 30))
    return m


def default_name(e):
    t = e['type']
    if t == 'trainer':
        return 'Trainer(%d)' % e.get('sight', 4)
    if t == 'item':
        return 'HiddenItem' if e.get('hidden') else 'Item'
    if t == 'berry':
        return 'BerryPlant'
    return {'exit': 'Exit', 'door': 'Door', 'warp': 'Warp', 'sign': 'Sign', 'pc': 'PC', 'mart': 'Mart'}.get(t, t.capitalize())


# ----------------------------------------------------------------------------- outputs
def metadata_block(spec):
    md = spec.get('metadata') or {}
    lines = ['#-------------------------------', '[%03d]   # %s' % (spec['id'], spec['name']),
             'Name = %s' % md.get('Name', spec.get('display_name', spec['name']))]
    for k, v in md.items():
        if k == 'Name':
            continue
        if isinstance(v, bool): v = 'true' if v else 'false'
        elif isinstance(v, (list, tuple)): v = ','.join(str(x) for x in v)
        lines.append('%s = %s' % (k, v))
    return '\n'.join(lines)


def connection_lines(spec, built):
    out = []
    for c in spec.get('connections', []):
        if c['to'] not in built:
            continue
        d = c['dir'][0].upper()
        opp = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}[d]
        out.append('# %s (%d) - %s (%d)' % (spec['name'], spec['id'], built[c['to']], c['to']))
        out.append('%d,%s,%d,%d,%s,%d' % (spec['id'], d, c.get('offset', 0), c['to'], opp, c.get('to_offset', 0)))
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    files = sorted(glob.glob(os.path.join(HERE, 'specs', '*.yaml')))
    ctx = Ctx()
    specs = []
    for f in files:
        for s in yaml.safe_load_all(open(f)):
            if s:
                s['_file'] = os.path.basename(f)
                specs.append(s)
    ids = [s['id'] for s in specs]
    if len(ids) != len(set(ids)):
        sys.exit('duplicate map ids in specs')
    for s in specs:
        prepare(s, ctx)
    built = {s['id']: s['name'] for s in specs}
    os.makedirs(os.path.join(OUT, 'Data'), exist_ok=True)
    os.makedirs(os.path.join(OUT, 'previews'), exist_ok=True)
    os.makedirs(os.path.join(OUT, 'PBS'), exist_ok=True)
    selected = [s for s in specs if not args or str(s['id']) in args or s['_file'] in args]
    mapinfos = []
    for s in specs:
        mapinfos.append(dict(id=s['id'], name=s['name'], parent=s.get('parent', 0)))
    for s in selected:
        m = build_map(s, ctx)
        path = os.path.join(OUT, 'Data', 'Map%03d.rxdata' % s['id'])
        M.dump_file(m, path)
        m2 = M.load_file(path)   # self-check: round trip through our reader
        assert m2.width == m.width and len(m2.events) == len(m.events)
        if '--no-preview' not in sys.argv:
            import render as R
            img = R.render(m2, grid='--grid' in sys.argv)
            img.convert('RGB').save(os.path.join(OUT, 'previews', '%03d_%s.png' % (s['id'], slug(s['name']))))
        print('built %3d %-34s %dx%d ts=%d events=%d' % (s['id'], s['name'], m.width, m.height, m.tileset_id, len(m.events)))
    # PBS
    with open(os.path.join(OUT, 'PBS', 'map_metadata_prismfall.txt'), 'w', encoding='utf-8') as f:
        f.write('# Generated by mapgen/build.py - do not edit by hand (edit mapgen/specs/*.yaml)\n')
        f.write('\n'.join(metadata_block(s) for s in specs) + '\n')
    with open(os.path.join(OUT, 'PBS', 'map_connections_prismfall.txt'), 'w', encoding='utf-8') as f:
        f.write('# Generated by mapgen/build.py - do not edit by hand\n#-------------------------------\n')
        for s in specs:
            for l in connection_lines(s, built):
                f.write(l + '\n')
    import shutil
    # MapInfos entries (merged into the user's own MapInfos.rxdata by merge_mapinfos.py / the in-game installer)
    with open(os.path.join(OUT, 'mapinfos_prismfall.txt'), 'w', encoding='utf-8') as f:
        f.write('# id<TAB>parent_id<TAB>name   (consumed by mapgen/merge_mapinfos.py and the Prismfall Map Installer plugin)\n')
        for mi in sorted(mapinfos, key=lambda d: d['id']):
            f.write('%d\t%d\t%s\n' % (mi['id'], mi['parent'], mi['name']))
    shutil.copyfile(os.path.join(OUT, 'mapinfos_prismfall.txt'), os.path.join(OUT, 'Data', 'mapinfos_prismfall.txt'))
    fmap = {}
    for s in specs:
        if s.get('field'):
            fmap[s['id']] = s['field']
    json.dump({'built': sorted(built), 'fields': fmap}, open(os.path.join(OUT, 'manifest.json'), 'w'), indent=1)
    for w in ctx.warnings:
        print('WARN', w)
    print('%d maps; %d warnings' % (len(selected), len(ctx.warnings)))


def slug(n):
    return ''.join(c if c.isalnum() else '_' for c in n).strip('_')[:40]


if __name__ == '__main__':
    main()
