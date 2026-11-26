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


def load_flags():
    """Story IDs from design/FLAGS.md (| S101 | NAME | ...), gym puzzle IDs from mapgen/flags.yaml."""
    f = yaml.safe_load(open(os.path.join(HERE, 'flags.yaml')))
    md = os.path.join(ROOT, 'design', 'FLAGS.md')
    if os.path.exists(md):
        for line in open(md, encoding='utf-8'):
            m = re.match(r'\|\s*([SV])(\d+)\s*\|\s*([A-Z][A-Z0-9_]+)\s*\|', line)
            if m:
                kind = 'switches' if m.group(1) == 'S' else 'variables'
                f[kind][m.group(3)] = int(m.group(2))
    return f


import re
FLAGS = load_flags()


def flag(v, kind):
    """Switch/variable id: int, or a NAME from flags.yaml."""
    if isinstance(v, str):
        if v not in FLAGS[kind]:
            raise ValueError('unknown %s %r (add it to flags.yaml)' % (kind, v))
        return FLAGS[kind][v]
    return v


G.FLAGMAP = flag


class Ctx:
    def __init__(self):
        self.stamps = json.load(open(os.path.join(HERE, 'data', 'stamps.json')))
        for tp in sorted(glob.glob(os.path.join(HERE, 'data', 'stamps_*.json'))):   # every data/stamps_*.json (REQUESTS item 4)
            self.stamps.update(json.load(open(tp)))
        self.palettes = {}
        self.specs = {}
        self.doors = {}   # link -> (map, x, y)   exterior door tiles
        self.exits = {}   # link -> (map, x, y)   interior exit mats
        self.warnings = []
        self.warp_ends = {}  # link -> [(map, x, y, dir)] arrival spots of two-way warps

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
    elif 'raw' in spec:             # MAPGEN 2h: layers painted by a layout script (layouts/rkit.py), ids already final
        layers = np.load(os.path.join(HERE, spec['raw'])).astype(np.int32)
        for ed in spec.get('tile_edits', []):
            if len(ed) == 4: layers[ed[0], ed[2], ed[1]] = ed[3]
        spec['_layers'] = layers
        spec['_tevents'] = []
        spec['_tileset'] = spec['tileset']
    else:
        pal = ctx.palette(spec.get('palette', 'outside'))
        lines = [l for l in spec['map'].strip('\n').split('\n')]
        p = T.Painter(pal, lines, seed=spec.get('seed', mid), warn=lambda m: ctx.warn(mid, m))
        if 'heights' in spec:
            hl = spec['heights'].strip('\n').split('\n')
            p.heights = np.array([[int(ch) if ch.isdigit() else 0 for ch in l.strip().ljust(p.W, '0')[:p.W]] for l in hl])
        layers = p.paint()
        spec['_painter'] = p
        spec['_tileset'] = pal['tileset']
        stamp_events = []
        for s in spec.get('stamps', []):
            st = ctx.stamps[s['stamp']]
            x, y = s['at']
            sl = np.array(st['layers'], dtype=np.int32)
            h, w = sl.shape[1:]
            if x < 0 or y < 0 or x + w > layers.shape[2] or y + h > layers.shape[1]:
                ctx.warn(mid, 'stamp %s at %s out of bounds' % (s['stamp'], s['at'])); continue
            occ = sl.max(axis=0) > 0
            for z in (1, 2):   # the object replaces whatever the painters scattered there
                layers[z, y:y + h, x:x + w][occ] = 0
            for z in range(3):
                reg = layers[z, y:y + h, x:x + w]
                m = sl[z] > 0
                reg[m] = sl[z][m]
            # clear tree canopy etc. on layer 2 where the stamp has layer-1 tiles but no layer-2 tile
            l2 = layers[2, y:y + h, x:x + w]; l2[(sl[1] > 0) & (sl[2] == 0)] = 0
            if 'door' in st or 'door' in s:
                dx, dy = s.get('door', st.get('door'))
                gfx = st.get('door_gfx', ['doors1', 0, 2])
                ev = {'type': 'door', 'at': [x + dx, y + dy], 'gfx': gfx, 'name': s.get('name', s['stamp'] + ' door')}
                if 'link' in s: ev['link'] = s['link']
                if 'to' in s: ev['to'] = s['to']
                if s.get('locked'):
                    ev = {'type': 'sign', 'at': [x + dx, y + dy], 'post': False, 'name': ev['name'],
                          'text': s.get('locked_text', 'The door is locked.')}
                stamp_events.append(ev)
        if pal.get('water_under_stamps'):   # objects placed on water (ships, piers) keep water beneath them
            wid = pal['water_under_stamps']
            wm = p.mask(['sea', 'pier']) & ~((layers[1] >= wid) & (layers[1] < wid + 48))
            layers[0][wm] = wid
        spec['events'] = stamp_events + spec['events']   # doors first: their autorun page runs before story autoruns
        for t in spec.get('tileblocks', []):   # {tile: top-left id, size: [w,h], at: [x,y], layer: 1}
            w, h = t['size']
            for dy in range(h):
                for dx in range(w):
                    tid = t['tile'] + dy * 8 + dx
                    if tid not in t.get('skip', []):
                        layers[t.get('layer', 1), t['at'][1] + dy, t['at'][0] + dx] = tid
        for t in spec.get('tiles', []):   # explicit tile placements {tile: name|id, at: [x,y], layer}
            tdef = pal['tiles'].get(t['tile']) if isinstance(t['tile'], str) else {'tile': t['tile'], 'layer': t.get('layer', 1)}
            layers[t.get('layer', tdef['layer']), t['at'][1], t['at'][0]] = tdef['tile']
        spec['_layers'] = layers
        spec['_tevents'] = []
        for i, tk in enumerate(spec.get('take_events', [])):   # reuse a base-template event (nurse, PC, clerk) at a new spot
            te = next((e for e in map(rjson.from_j, load_template(tk['template'])['events']) if e.name == tk['name']), None)
            if te is None:
                ctx.warn(mid, 'take_events: no %r in template %s' % (tk['name'], tk['template'])); continue
            te.ivars['x'], te.ivars['y'] = tk['at']
            for pg in te.ivars['pages'][:1] if (tk.get('prepend') or tk.get('replace_text')) else []:
                L = pg.ivars['list']
                for c in L:
                    pr = c.ivars['parameters']
                    if c.ivars['code'] in (101, 401) and pr and pr[0] in (tk.get('replace_text') or {}):
                        pr[0] = tk['replace_text'][pr[0]]
                if tk.get('prepend'):
                    pre = G.compile_cmds(tk['prepend'])
                    i0 = next((i for i, c in enumerate(L) if c.ivars['code'] not in (108, 408, 355)), 0)
                    L[i0:i0] = pre
            spec['_tevents'].append(te)
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
        if e['type'] == 'warp' and 'link' in e and 'arrive' in e and 'to' not in e:
            a = e['arrive']
            ctx.warp_ends.setdefault(e['link'], []).append((mid, a[0], a[1], a[2] if len(a) > 2 else 'retain'))
        if e['type'] == 'warp' and 'link' in e and 'arrive' in e:
            ctx.doors.setdefault(e['link'], (mid, e['arrive'][0], e['arrive'][1]))
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
        if e.get('locked'):     # {until: SWITCH, text: ...}: a locked page first, the door opens once SWITCH is on
            lk = e['locked']; sw = flag(lk['until'], 'switches')
            for p in pg:
                c = p.ivars['condition'].ivars
                if c['switch1_valid']: c['switch2_valid'], c['switch2_id'] = True, sw
                else: c['switch1_valid'], c['switch1_id'] = True, sw
            pg = [G.page(gfx=G.graphic(char, d, pat), cmds=G.compile_cmds(lk.get('commands') or [lk['text']]))] + pg
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
    if t == 'cut_tree':
        l = [G.ev_cmd(111, 0, [12, 'pbCut']), G.ev_cmd(355, 1, ['pbSmashEvent(get_self)']), G.ev_cmd(0, 1),
             G.ev_cmd(412, 0)]
        return [G.page(gfx=G.graphic('Object tree 1'), cmds=l)]
    if t == 'rock_smash':                                  # map builder 10: Essentials' "Rock" event (pbRockSmash)
        l = [G.ev_cmd(111, 0, [12, 'pbRockSmash']), G.ev_cmd(355, 1, ['pbSmashEvent(get_self)']), G.ev_cmd(0, 1),
             G.ev_cmd(412, 0)]
        return [G.page(gfx=G.graphic(e.get('sprite', 'Object rock')), cmds=l)]     # map builder 13: cave rocks (sprite:)
    if t == 'pc':
        return [G.page(cmds=G.compile_cmds([{'script': 'pbPokeCenterPC'}]))]
    if t == 'event':
        out = []
        for p in e['pages']:
            g = p.get('graphic', {})
            out.append(G.page(cond=page_cond(p.get('cond')),
                              gfx=G.graphic(g.get('sprite', ''), FACING.get(g.get('dir', 'down'), 2), g.get('pattern', 0),
                                            tile_id=g.get('tile', 0), opacity=g.get('opacity', 255)),
                              trigger=G.TRIGGERS[p.get('trigger', 'action')], move_type=G.MOVES[p.get('move', 'fixed')],
                              through=p.get('through', False), dir_fix=p.get('dir_fix', False),
                              step_anime=p.get('step_anime', False), on_top=p.get('on_top', False),
                              speed=p.get('speed', 3), freq=p.get('freq', 3),
                              # map builder 10: a page's own move route (move: custom), in rpg.route_cmds' DSL
                              route=G.move_route(G.route_cmds(p['route']), repeat=p.get('repeat', True), skippable=True) if p.get('route') else None,
                              cmds=G.compile_cmds(p.get('commands', []))))
        return out
    raise ValueError('unknown event type %s' % t)


def page_cond(c):
    if not c:
        return None
    var = [flag(c['var'][0], 'variables'), c['var'][1]] if c.get('var') else None
    sw1 = flag(c['switch'], 'switches') if c.get('switch') is not None else None
    sw2 = flag(c['switch2'], 'switches') if c.get('switch2') is not None else None
    return G.condition(switch1=sw1, switch2=sw2, var=var, self_sw=c.get('self'))


def resolve_target(e, ctx, mid, door):
    if 'to' in e:
        to = dict(e['to'])
        to.setdefault('dir', 'up' if door else 'retain')
        return to
    link = e.get('link')
    if e.get('type') == 'warp' and link in ctx.warp_ends:
        other = [w for w in ctx.warp_ends[link] if w[0] != mid]
        if other:
            m, x, y, d = other[0]
            return {'map': m, 'x': x, 'y': y, 'dir': d}
    if door:   # exterior door -> arrive 1 tile above the interior exit mat (or the exit's 'arrive' spot)
        if link in ctx.exits:
            m, x, y, d = ctx.exits[link]
            return {'map': m, 'x': x, 'y': y, 'dir': d}
    else:      # interior exit -> stand on the exterior door (door event animates the step out)
        if link in ctx.doors and ctx.doors[link][0] != mid:
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
    G.EVMAP.clear()                     # event names -> ids, so commands can say who: "Name" / %EV[Name]%
    for ev in tev: G.EVMAP.setdefault(ev.name, ev.id)
    k = nid
    for e in spec['events']:
        x, y = e['at']
        if 0 <= x < W and 0 <= y < H:
            G.EVMAP.setdefault(e.get('name') or default_name(e), k); k += 1
    for e in spec['events']:
        x, y = e['at']
        if not (0 <= x < W and 0 <= y < H):
            ctx.warn(mid, 'event %s out of bounds %s' % (e.get('name', e['type']), e['at'])); continue
        if (x, y) in occupied:
            ctx.warn(mid, 'two events at %d,%d (%s)' % (x, y, e.get('name', e['type'])))
        if e['type'] == 'sign' and e.get('post', True) and pal and 'sign' in pal.get('tiles', {}):
            tdef = pal['tiles'][e.get('post_tile', 'sign')]
            layers[tdef['layer'], y, x] = tdef['tile']
            top = pal['tiles'].get('sign_top')
            if top and y > 0:
                layers[top['layer'], y - 1, x] = top['tile']
        name = e.get('name') or default_name(e)
        events[nid] = G.event(nid, name, x, y, pages_from(e, ctx, mid))
        occupied[(x, y)] = nid
        nid += 1
    bgm = spec.get('bgm', '')
    m = G.rmap(spec['_tileset'], W, H, G.table3(layers), events, bgm=bgm, encounter_step=spec.get('encounter_step', 30))
    check_reach(spec, ctx, m)
    ctx.material_bad = getattr(ctx, 'material_bad', 0) + material_check(spec, ctx, layers, spec['_tileset'])
    ctx.slab_bad = getattr(ctx, 'slab_bad', 0) + slab_check(spec, ctx, layers, spec['_tileset'])
    ctx.pass_bad = getattr(ctx, 'pass_bad', 0) + pass_check(spec, ctx, m)
    gate_check(spec, ctx, m)
    if spec.get('rubric'):
        walk_check(spec, ctx, m)
        r = rubric(layers)
        spec['_rubric'] = r
        need = [('layer2', 55, 1), ('layer3', 20, 1), ('bare', 35, -1), ('bare3x3', 13, -1), ('stacks', 10, 1), ('mirror', 15, -1)]
        print('RUBRIC %d %s: ' % (mid, spec['name']) + '  '.join(
            '%s %.1f%s' % (k, r[k], '' if (r[k] - lim) * sgn >= 0 else ' FAIL(%s%d)' % ('>=' if sgn > 0 else '<=', lim))
            for k, lim, sgn in need))
    return m


def cell_passable(layers, ts, x, y):
    """Essentials' playerPassable? for a whole tile (no events, not surfing, not on a bridge)."""
    H, W = layers.shape[1:]
    if not (0 <= x < W and 0 <= y < H):
        return False
    for z in (2, 1, 0):
        t = int(layers[z, y, x])
        if t == 0:
            continue
        tag = ts['terrain_tags'][t] if t < len(ts['terrain_tags']) else 0
        if tag in (13, 15):        # Neutral ignores passability; bridges are ignored off-bridge
            continue
        if ts['passages'][t] & 0x0f == 0x0f:
            return False
        if ts['priorities'][t] == 0:
            return True
    return True


def check_reach(spec, ctx, m):
    """Every talk-to event needs a walkable neighbour; walk-on events need a walkable cell or neighbour."""
    import render as R
    ts = R.tilesets()[m.tileset_id]
    lay = m.data.data
    import re as _re
    airborne = _re.compile(spec['walk_airborne']) if spec.get('walk_airborne') else None
    for ev in m.events.values():
        if airborne is not None and airborne.search(ev.name or ''):
            continue   # reached mid-throw (see walk_check); the puzzle checker proves the landings
        n = [cell_passable(lay, ts, ev.x + dx, ev.y + dy) for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))]
        if not any(n) and not cell_passable(lay, ts, ev.x, ev.y):
            if any(p.trigger in (0, 1, 2) and any(c.code != 0 for c in p.list) for p in ev.pages):
                ctx.warn(spec['id'], 'event "%s" at %d,%d is walled in (no walkable neighbour)' % (ev.name, ev.x, ev.y))


def rubric(layers):
    """ART_DIRECTION.md section 3 numbers (same definitions as ref/art/tools/map_metrics.py)."""
    d = layers; H, W = d.shape[1:]; n = W * H
    key = d[0].astype(np.int64) * 10**8 + d[1].astype(np.int64) * 10**4 + d[2]
    bare = (d[1] == 0) & (d[2] == 0)
    bp = sum(1 for y in range(1, H - 1) for x in range(1, W - 1) if bare[y - 1:y + 2, x - 1:x + 2].all())
    return dict(layer2=(d[1] > 0).mean() * 100, layer3=(d[2] > 0).mean() * 100, bare=bare.mean() * 100,
                bare3x3=bp / n * 100, stacks=len(np.unique(key)) / n * 100, mirror=(key == key[:, ::-1]).mean() * 100)


_MAT = None


def material_check(spec, ctx, layers, tileset_id):
    """MAPGEN 2g: every tile's material (data/materials.yaml) against the map's `biome:`; returns the offender count."""
    global _MAT
    if _MAT is None:
        d = yaml.safe_load(open(os.path.join(HERE, 'data', 'materials.yaml')))
        _MAT = d; d['_tab'] = {}
    biome = spec.get('biome')
    if not biome: return 0
    forbid = set(_MAT['biomes'].get(biome, {}).get('forbid', []))
    if not forbid: return 0
    tab = _MAT['_tab'].get(tileset_id)
    if tab is None:
        tab = {}
        ranges = (_MAT['shared'] if tileset_id in (30, 33, 40) else []) + (_MAT.get('tilesets') or {}).get(tileset_id, [])
        for a, b, mat in ranges:
            for t in range(a, b + 1): tab[t] = mat
        _MAT['_tab'][tileset_id] = tab
    bad = {}
    Z, H, W = layers.shape
    for z in range(Z):
        for y in range(H):
            for x in range(W):
                mat = tab.get(int(layers[z, y, x]))
                if mat in forbid:
                    bad.setdefault(mat, []).append((x, y, int(layers[z, y, x])))
    for e in spec.get('events', []):                        # tile-graphic events (barriers, planks) count too
        for pg in e.get('pages', []) or []:
            t = (pg.get('graphic') or {}).get('tile')
            if isinstance(t, int) and tab.get(t) in forbid:
                bad.setdefault(tab[t], []).append((e['at'][0], e['at'][1], t))
    for mat, cells in bad.items():
        ctx.warn(spec['id'], 'MATERIAL %s in a %s map: %d tiles, e.g. tile %d at %d,%d' % (mat, biome, len(cells), cells[0][2], cells[0][0], cells[0][1]))
    return sum(len(v) for v in bad.values())


# map builder 8: the flat dark-brown plank slab (Sheridan_2 544-546 = PF Rejuv 4992-4994) that early layouts drew as
# cliff and quay "stairs".  Stairs are now real steps (tdraw st_stair_* / tb_stair_*, rdraw fw_stair_*); the slab must
# never come back on a PF Rejuv map.
OLD_SLAB = {4992, 4993, 4994}
PF_REJUV_TILESETS = (50, 51, 52, 53, 55, 56, 57, 58, 59)


def slab_check(spec, ctx, layers, tileset_id):
    if tileset_id not in PF_REJUV_TILESETS: return 0
    hit = np.argwhere(np.isin(layers, list(OLD_SLAB)))
    if len(hit):
        z, y, x = hit[0]
        ctx.warn(spec['id'], 'OLD SLAB STAIRS: %d tiles of the flat plank slab (4992-4994), e.g. at %d,%d: use real steps' % (len(hit), x, y))
    return len(hit)


def pass_check(spec, ctx, m):
    """map builder 11 (the passability audit): a passable priority-0 decoration above a solid tile makes that tile
    walkable in Essentials (playerPassable? stops at the first such tile, top layer first).  passguard.hits() lists the
    cells the player can really walk onto because of one; layout writers fix them with passguard.guard()."""
    import render as R
    import passguard as PG
    ts = R.tilesets()[m.tileset_id]
    hs = PG.hits(m.data.data, ts, [(e.x, e.y) for e in m.events.values()])
    if hs:
        x, y, z, t = hs[0]
        ctx.warn(spec['id'], 'PASS %d decorated solid cell(s) walkable, e.g. %s (tile %d, layer %d) at %d,%d: '
                 'passguard.guard() in the layout writer' % (len(hs), PG.tile_name(m.tileset_id, t) or 'sheet tile', t, z + 1, x, y))
    return len(hs)


def gate_check(spec, ctx, m):
    """map builder 10 (playtest round 3 item 15): a story gate must really be shut.  spec `gates`: [{name, from: [[x, y],
    ...], sealed_edge: N/S/E/W and/or sealed: [[x, y], ...], ice_solid: true (ice counts as wall)}].  Flood-fills from each `from` cell over walkable tiles with
    every event that blocks on its FIRST page (a charset or a tile graphic, not Through) standing solid - the state before
    any switch is set - and warns if a sealed cell, or any walkable cell on the sealed edge, is reached."""
    gates = spec.get('gates')
    if not gates: return
    import render as R
    ts = R.tilesets()[m.tileset_id]; lay = m.data.data; H, W = m.height, m.width
    solid = set()
    for e in m.events.values():
        p0 = e.pages[0]
        if (p0.graphic.character_name or p0.graphic.tile_id) and not p0.through: solid.add((e.x, e.y))
    ok = np.array([[cell_passable(lay, ts, x, y) and (x, y) not in solid for x in range(W)] for y in range(H)])
    ice = None
    for g in gates:
        okg = ok
        if g.get('ice_solid'):                      # map builder 12: a place reached only by sliding must be shut on foot
            if ice is None:
                tt = ts['terrain_tags']
                ice = np.array([[any(int(lay[z, y, x]) and tt[int(lay[z, y, x])] == 12 for z in (0, 1, 2)) for x in range(W)] for y in range(H)])
            okg = ok & ~ice
        seen = np.zeros_like(ok); st = [tuple(p) for p in g['from'] if okg[p[1], p[0]]]
        if not st: ctx.warn(spec['id'], 'GATE "%s": no walkable start cell' % g['name']); continue

        def edge_ok(x, y, d):                       # directional passage bits as Essentials reads them (one-way ledges)
            bit = 1 << (d // 2 - 1)
            for z in (2, 1, 0):
                t = int(lay[z, y, x])
                if t == 0: continue
                if ts['passages'][t] & bit: return False
                if ts['priorities'][t] == 0: return True
            return True
        while st:
            x, y = st.pop()
            if seen[y, x]: continue
            seen[y, x] = True
            for dx, dy, d in ((0, 1, 2), (0, -1, 8), (1, 0, 6), (-1, 0, 4)):
                X, Y = x + dx, y + dy
                if 0 <= X < W and 0 <= Y < H and okg[Y, X] and not seen[Y, X] and edge_ok(x, y, d) and edge_ok(X, Y, 10 - d): st.append((X, Y))
        cells = [tuple(c) for c in g.get('sealed', [])]
        e = g.get('sealed_edge')
        if e: cells += [(0, y) for y in range(H)] if e == 'W' else [(W - 1, y) for y in range(H)] if e == 'E' else \
                       [(x, 0) for x in range(W)] if e == 'N' else [(x, H - 1) for x in range(W)]
        leak = [c for c in cells if seen[c[1], c[0]]]
        if leak:
            ctx.warn(spec['id'], 'GATE "%s" LEAKS: %d cell(s) reachable with the gate shut, e.g. %d,%d' % (g['name'], len(leak), leak[0][0], leak[0][1]))
            ctx.gate_bad = getattr(ctx, 'gate_bad', 0) + 1
        else:
            print('GATE ok   %d %s: shut (%d cells reachable from %s, none on the sealed side)' % (spec['id'], g['name'], int(seen.sum()), g['from']))


def walk_check(spec, ctx, m):
    """Flood-fill walkable tiles from the first warp/door: warn about cut-off events and stranded areas."""
    import render as R
    ts = R.tilesets()[m.tileset_id]; lay = m.data.data; H, W = m.height, m.width
    solid = {(e.x, e.y) for e in m.events.values() if e.pages[0].graphic.character_name and not e.pages[0].through}
    ok = np.array([[cell_passable(lay, ts, x, y) and (x, y) not in solid for x in range(W)] for y in range(H)])
    starts = [(e.x, e.y) for e in m.events.values() if any(c.code == 201 for p in e.pages for c in p.list)]
    if not starts:
        return
    seen = np.zeros_like(ok); st = []
    # walk_from: extra seeds (map edges joined by connections, halves joined through another map such as a cave)
    for sx, sy in starts[:1] + [tuple(p) for p in spec.get('walk_from', [])]:
        for dx, dy in ((0, 0), (0, 1), (0, -1), (1, 0), (-1, 0)):
            if 0 <= sx + dx < W and 0 <= sy + dy < H and ok[sy + dy, sx + dx]:
                st.append((sx + dx, sy + dy))
    while st:
        x, y = st.pop()
        if seen[y, x]: continue
        seen[y, x] = True
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            if 0 <= x + dx < W and 0 <= y + dy < H and ok[y + dy, x + dx] and not seen[y + dy, x + dx]:
                st.append((x + dx, y + dy))
    import re as _re
    airborne = _re.compile(spec['walk_airborne']) if spec.get('walk_airborne') else None
    for e in m.events.values():
        if not any(c.code != 0 for p in e.pages for c in p.list):
            continue
        # autorun / parallel: nobody walks to them.  Only pages that run something count: an empty rest page (the usual
        # `cond: {self: A}` after a one-shot parallel setter) is inert whatever its trigger.
        if all(p.trigger in (3, 4) for p in e.pages if any(c.code != 0 for c in p.list)):
            continue
        # walk_airborne: a name regex for events the player reaches in mid-air (the Canopy's web trampolines: one web
        # throws you onto the next).  Their landings are proved by the puzzle checker, not by this flood fill.
        if airborne is not None and airborne.search(e.name or ''):
            continue
        if not any(0 <= e.x + dx < W and 0 <= e.y + dy < H and seen[e.y + dy, e.x + dx]
                   for dx, dy in ((0, 0), (0, 1), (0, -1), (1, 0), (-1, 0))):
            ctx.warn(spec['id'], 'event "%s" at %d,%d cannot be reached on foot from the first door/warp' % (e.name, e.x, e.y))
    ign = spec.get('walk_ignore', ['wall', 'tower', 'keep'])   # parapet walks are scenery unless stairs reach them
    if spec.get('_painter') is not None:
        ok = ok & ~spec['_painter'].mask([c for c in ign if c in set(spec['_painter'].cls.reshape(-1))])
    # speckle: unreachable pockets of <= 4 tiles (passable rock / icicle tops, ravine-rim autotile corners) are scenery
    # gaps, not stranded areas.  Events inside them are still flagged above.
    lost = ok & ~seen; done = np.zeros_like(lost)
    for y0 in range(H):
        for x0 in range(W):
            if not lost[y0, x0] or done[y0, x0]: continue
            comp = []; st2 = [(x0, y0)]; done[y0, x0] = True
            while st2:
                x, y = st2.pop(); comp.append((x, y))
                for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                    if 0 <= x + dx < W and 0 <= y + dy < H and lost[y + dy, x + dx] and not done[y + dy, x + dx]:
                        done[y + dy, x + dx] = True; st2.append((x + dx, y + dy))
            if len(comp) <= spec.get('walk_speckle', 4):
                for x, y in comp: ok[y, x] = False
    stranded = int((ok & ~seen).sum())
    if stranded > ok.sum() * 0.05 and '--walkmap' in sys.argv:
        for y in range(H):
            print(''.join('#' if not ok[y, x] else ('.' if seen[y, x] else '!') for x in range(W)))
    if stranded > ok.sum() * 0.05 and not spec.get('yards_ok'):   # yards_ok: enclosed back gardens are intended
        ctx.warn(spec['id'], '%d walkable tiles (%.0f%%) are cut off from the first door/warp' % (stranded, 100.0 * stranded / max(1, ok.sum())))


def default_name(e):
    t = e['type']
    if t == 'trainer':
        return 'Trainer(%d)' % e.get('sight', 4)
    if t == 'item':
        return 'HiddenItem' if e.get('hidden') else 'Item'
    if t == 'berry':
        return 'BerryPlant'
    if t == 'cut_tree':
        return 'CutTree'
    if t == 'rock_smash':
        return 'Rock'
    return {'exit': 'Exit', 'door': 'Door', 'warp': 'Warp', 'sign': 'Sign', 'pc': 'PC', 'mart': 'Mart'}.get(t, t.capitalize())


# ----------------------------------------------------------------------------- outputs
_TOWN_POS = None


def town_map_position(mid):
    """MapPosition from mapgen/data/town_map_positions.json (cartographer, tools/worldmap/gen_docs.py), else None"""
    global _TOWN_POS
    if _TOWN_POS is None:
        p = os.path.join(HERE, 'data', 'town_map_positions.json')
        _TOWN_POS = json.load(open(p))['positions'] if os.path.exists(p) else {}
    return _TOWN_POS.get(str(mid))


def metadata_block(spec):
    md = dict(spec.get('metadata') or {})
    if town_map_position(spec['id']):
        md['MapPosition'] = town_map_position(spec['id'])   # the Velmora town map owns positions (region 0)
    lines = ['#-------------------------------', '[%03d]   # %s' % (spec['id'], spec['name']),
             'Name = %s' % md.get('Name', spec.get('display_name', spec['name']))]
    for k, v in md.items():
        if k == 'Name':
            continue
        if isinstance(v, bool): v = 'true' if v else 'false'
        elif isinstance(v, (list, tuple)): v = ','.join(str(x) for x in v)
        lines.append('%s = %s' % (k, v))
    return '\n'.join(lines)


_SEEN_CONN = set()


def connection_lines(spec, built):
    out = []
    for c in spec.get('connections', []):
        if c['to'] not in built:
            continue
        d = c['dir'][0].upper()
        opp = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}[d]
        key = tuple(sorted([(spec['id'], d), (c['to'], opp)]))
        if key in _SEEN_CONN:
            continue
        _SEEN_CONN.add(key)
        out.append('# %s (%d) - %s (%d)' % (spec['name'], spec['id'], built[c['to']], c['to']))
        out.append('%d,%s,%d,%d,%s,%d' % (spec['id'], d, c.get('offset', 0), c['to'], opp, c.get('to_offset', 0)))
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    # spec generators (gen_*.py) write some specs (test arena, gym puzzles): run them first
    import importlib
    for g in sorted(glob.glob(os.path.join(HERE, 'gen_*.py'))):
        if not os.path.basename(g)[:-3].isidentifier(): continue      # staging copies such as gen_gym1.new.py are not generators
        importlib.import_module(os.path.basename(g)[:-3]).main()
    files = sorted(glob.glob(os.path.join(HERE, 'specs', '*.yaml')))
    ctx = Ctx()
    specs = []
    for f in files:
        for s in yaml.safe_load_all(open(f)):
            if s:
                s['_file'] = os.path.basename(f)
                specs.append(s)
    import puzzles                              # puzzle events laid over maps whose layout another script owns (D1 chime rows)
    for mod in puzzles.modules():
        for mid, evs in getattr(mod, 'EVENTS', {}).items():
            for s in specs:
                if s['id'] == mid: s.setdefault('events', []); s['events'] = list(s['events']) + copy.deepcopy(evs)
    import trial_overlay                        # map builder 9: Trial events (design/TRIAL_EVENTS.yaml) over other scripts' maps
    import render as _R
    trial_overlay.apply(specs, cell_passable, _R.tilesets())
    ids = [s['id'] for s in specs]
    if len(ids) != len(set(ids)):
        sys.exit('duplicate map ids in specs')
    for s in specs:
        prepare(s, ctx)
    built = {s['id']: s['name'] for s in specs}
    os.makedirs(os.path.join(OUT, 'Data'), exist_ok=True)
    os.makedirs(os.path.join(OUT, 'previews'), exist_ok=True)
    os.makedirs(os.path.join(OUT, 'previews', 'mood'), exist_ok=True)
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
            if '--mood' in sys.argv and (s.get('tone') or s.get('fog')):   # second preview with tone + fog applied
                R.mood(img, s.get('tone'), s.get('fog')).convert('RGB').save(
                    os.path.join(OUT, 'previews', 'mood', '%03d_%s.png' % (s['id'], slug(s['name']))))
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
        f.write('# id<TAB>parent_id<TAB>name   (consumed by mapgen/merge_mapinfos.py and the Prismfall Maps plugin)\n')
        for mi in sorted(mapinfos, key=lambda d: d['id']):
            f.write('%d\t%d\t%s\n' % (mi['id'], mi['parent'], mi['name']))
    shutil.copyfile(os.path.join(OUT, 'mapinfos_prismfall.txt'), os.path.join(OUT, 'Data', 'mapinfos_prismfall.txt'))
    # map -> default field.  design/FIELD_DEFAULTS.yaml (field-effects workstream, every map of the world) is the source of
    # truth; a spec's own `field:` only fills in for a map the yaml does not list.  :NONE entries are written too (they
    # mark a map as deliberately field-free, so no environment fallback applies).  `wild:` -> MAP_WILD_FIELDS.
    fmap = {}; wmap = {}; names = dict(built)
    for s in specs:
        if s.get('field'):
            fmap[s['id']] = s['field']
    fd = os.path.join(os.path.dirname(HERE), 'design', 'FIELD_DEFAULTS.yaml')
    if os.path.exists(fd):
        for mid, e in (yaml.safe_load(open(fd)).get('maps') or {}).items():
            mid = int(mid); names.setdefault(mid, e.get('name', '?'))
            if e.get('field'):
                if mid in fmap and (fmap[mid][0] if isinstance(fmap[mid], list) else fmap[mid]) != e['field']:
                    print('FIELD %d: spec says %s, FIELD_DEFAULTS.yaml says %s (yaml wins)' % (mid, fmap[mid], e['field']))
                fmap[mid] = [e['field'], int(e['stage'])] if e.get('stage', 1) != 1 else e['field']
            if e.get('wild'): wmap[mid] = e['wild']
    fval = lambda v: ('[:%s, %d]' % (v[0], v[1])) if isinstance(v, list) else (':%s' % v)
    rb = ['# GENERATED by mapgen/build.py from design/FIELD_DEFAULTS.yaml (+ spec `field:` entries) - do not edit.',
          '# Map -> default field (FieldEffects::MAP_FIELDS) and wild-battle field (MAP_WILD_FIELDS).',
          'if defined?(FieldEffects) && FieldEffects.const_defined?(:MAP_FIELDS)']
    for mid in sorted(fmap):
        rb.append('  FieldEffects::MAP_FIELDS[%d] = %s   # %s' % (mid, fval(fmap[mid]), names.get(mid, '?')))
    rb.append('end')
    rb.append('if defined?(FieldEffects) && FieldEffects.const_defined?(:MAP_WILD_FIELDS)')
    for mid in sorted(wmap):
        rb.append('  FieldEffects::MAP_WILD_FIELDS[%d] = %s   # %s' % (mid, fval(wmap[mid]), names.get(mid, '?')))
    rb.append('end')
    pdir = os.path.join(OUT, 'Plugins', 'Prismfall Maps')
    os.makedirs(pdir, exist_ok=True)
    open(os.path.join(pdir, '002_MapFields.rb'), 'w', encoding='utf-8').write('\n'.join(rb) + '\n')
    # per-map atmosphere (ART_DIRECTION rubric 10): base screen tone, applied on entering the map
    rb = ['# GENERATED by mapgen/build.py from the specs\' `tone:` entries - do not edit.',
          'module PrismfallMaps', '  MAP_TONES = {']
    for s in specs:
        if s.get('tone'):
            rb.append('    %d => [%s],   # %s' % (s['id'], ', '.join(str(int(v)) for v in s['tone']), s['name']))
    rb += ['  }', '',
           '  # per-map fog picture (spec key `fog: {name, opacity, blend, zoom, sx, sy, hue}`; files in Graphics/Fogs/)',
           '  MAP_FOGS = {']
    for s in specs:
        f = s.get('fog')
        if f:
            rb.append('    %d => ["%s", %d, %d, %d, %d, %d, %d],   # %s' % (s['id'], f['name'], f.get('hue', 0), f.get('opacity', 60),
                      f.get('blend', 0), f.get('zoom', 100), f.get('sx', 2), f.get('sy', 0), s['name']))
    rb += ['  }', '',
           '  def self.apply_map_fog',
           '    return if !$game_map',
           '    f = MAP_FOGS[$game_map.map_id]',
           '    return if !f',
           '    $game_map.fog_name, $game_map.fog_hue, $game_map.fog_opacity, $game_map.fog_blend_type, $game_map.fog_zoom, $game_map.fog_sx, $game_map.fog_sy = *f',
           '  end', '',
           '  def self.apply_map_tone', '    return if !$game_map || !$game_screen',
           '    t = MAP_TONES[$game_map.map_id]', '    tone = (t) ? Tone.new(*t) : Tone.new(0, 0, 0, 0)',
           '    return if @last_tone_map == $game_map.map_id', '    @last_tone_map = $game_map.map_id',
           '    $game_screen.start_tone_change(tone, 0) if t || @tone_was_set', '    @tone_was_set = !t.nil?', '  end', 'end', '',
           'EventHandlers.add(:on_enter_map, :prismfall_map_tone,', '  proc { |_old_map_id| PrismfallMaps.apply_map_tone; PrismfallMaps.apply_map_fog }', ')']
    pdir0 = os.path.join(OUT, 'Plugins', 'Prismfall Maps')
    open(os.path.join(pdir0, '005_MapAtmosphere.rb'), 'w', encoding='utf-8').write('\n'.join(rb) + '\n')
    # map BGM / BGS: design/MAP_AUDIO.yaml (+ a spec's own `map_audio:` block) -> 013_MapAudio.rb, applied at run time and
    # only with installed files, so the spec `bgm:` baked into the map stays the fallback (see map_audio.py)
    import map_audio
    map_audio.write(specs)
    # hand-written runtime helpers used by the story events (pfm_* flags, story items, quest log, title cards)
    for rbf in sorted(glob.glob(os.path.join(HERE, 'ruby', '*.rb'))):
        shutil.copyfile(rbf, os.path.join(pdir0, os.path.basename(rbf)))
    # puzzle rooms: the runtime registry (reset / solved state / hints) comes from the same data the solver proves
    import puzzles
    open(os.path.join(pdir0, '007_PuzzleRooms.rb'), 'w', encoding='utf-8').write(puzzles.ruby_registry())
    ctx.puzzle_bad = puzzles.run_all()[0] + puzzles.run_built()[0]
    bosses = yaml.safe_load(open(os.path.join(HERE, 'bosses.yaml'))) or {}
    rb = ['# GENERATED by mapgen/build.py from mapgen/bosses.yaml - do not edit. Story bosses used by the generated maps.',
          'if defined?(Prismfall::Bosses)']
    for bid, b in bosses.items():
        body = '\n'.join('    ' + l for l in b['ruby'].rstrip().split('\n'))
        rb.append('  # map %s' % b.get('map', '?'))
        rb.append('  Prismfall::Bosses.register(:%s, {\n%s\n  })' % (bid, body))
    rb.append('end')
    open(os.path.join(pdir, '003_StoryBosses.rb'), 'w', encoding='utf-8').write('\n'.join(rb) + '\n')
    json.dump({'built': sorted(built), 'fields': fmap, 'wild_fields': wmap}, open(os.path.join(OUT, 'manifest.json'), 'w'), indent=1)
    # every Transfer Player must point at a built map (ours) or a base-project map (< 100)
    for s in selected:
        m = M.load_file(os.path.join(OUT, 'Data', 'Map%03d.rxdata' % s['id']))
        for ev in m.events.values():
            for pg in ev.pages:
                for c in pg.list:
                    if c.code == 201 and c.parameters[0] == 0:
                        tm = c.parameters[1]
                        if tm not in built and tm >= 100:
                            ctx.warn(s['id'], 'event "%s" transfers to map %d, which is not built yet' % (ev.name, tm))
                        elif tm in built and tm != s['id']:
                            tw, th = next(x['_size'] for x in specs if x['id'] == tm)
                            if not (0 <= c.parameters[2] < tw and 0 <= c.parameters[3] < th):
                                ctx.warn(s['id'], 'event "%s" transfers outside map %d' % (ev.name, tm))
    ctx.arrival_bad = check_arrivals(selected, specs, ctx)
    ctx.seam_bad = check_seams(specs, ctx)
    ctx.spot_bad = check_spots(specs, ctx)
    # trainers referenced by events -> list for the trainer-data owner
    need = set()
    for s in selected:
        m = M.load_file(os.path.join(OUT, 'Data', 'Map%03d.rxdata' % s['id']))
        for ev in m.events.values():
            for pg in ev.pages:
                for c in pg.list:
                    txt = str(c.parameters[-1]) if c.code in (111, 355, 655) else ''
                    for key in ('TrainerBattle.start(', 'Prismfall.rival_battle(', 'Prismfall.gym_battle('):
                        if key in txt:
                            arg = txt.split(key)[1].rsplit(')', 1)[0]
                            need.add((s['id'], arg if key == 'TrainerBattle.start(' else key + arg + ')'))
    with open(os.path.join(OUT, 'trainers_needed.txt'), 'w') as f:
        f.write('# map_id<TAB>TrainerBattle.start arguments used by generated events (must exist in PBS trainers)\n')
        for mid, a in sorted(need):
            f.write('%d\t%s\n' % (mid, a))
    for w in ctx.warnings:
        print('WARN', w)
    print('%d maps; %d warnings' % (len(selected), len(ctx.warnings)))
    if '--strict' in sys.argv and getattr(ctx, 'material_bad', 0):
        sys.exit('--strict: %d tiles of a material their map\'s biome forbids (see MATERIAL warnings)' % ctx.material_bad)
    if '--strict' in sys.argv and getattr(ctx, 'puzzle_bad', 0):
        sys.exit('--strict: %d puzzle proof(s) failed (see PUZZLE FAIL lines; mapgen/puzzles/)' % ctx.puzzle_bad)
    if '--strict' in sys.argv and getattr(ctx, 'arrival_bad', 0):
        sys.exit('--strict: %d blocked arrival / door tiles (see ARRIVAL warnings)' % ctx.arrival_bad)
    if '--strict' in sys.argv and getattr(ctx, 'seam_bad', 0):
        sys.exit('--strict: %d edge tiles that lead onto blocked ground across a map connection (see SEAM warnings)' % ctx.seam_bad)
    if '--strict' in sys.argv and getattr(ctx, 'slab_bad', 0):
        sys.exit('--strict: %d old slab-stair tiles (see OLD SLAB STAIRS warnings)' % ctx.slab_bad)
    if '--strict' in sys.argv and getattr(ctx, 'pass_bad', 0):
        sys.exit('--strict: %d decorated solid cell(s) the player can walk onto (see PASS warnings; mapgen/passguard.py)' % ctx.pass_bad)
    if '--strict' in sys.argv and getattr(ctx, 'gate_bad', 0):
        sys.exit('--strict: %d story gate(s) leak (see GATE warnings)' % ctx.gate_bad)
    if '--strict' in sys.argv and getattr(ctx, 'spot_bad', 0):
        sys.exit('--strict: %d HealingSpot / fly spot problem(s) (see SPOT warnings)' % ctx.spot_bad)


def check_spots(specs, ctx):
    """map builder 10 (REQUESTS cartographer item 7): every HealingSpot (map metadata: where blacking out and Fly put the
    player) and every fly point of pbs/town_map.txt must land on a passable tile that no solid event covers, and from
    that tile the player must be able to walk to a way out (a transfer event or an open edge of a connected side).
    Returns the number of problems; each is a SPOT warning."""
    import render as R
    by_id = {s['id']: s for s in specs}
    spots = []
    for s in specs:
        hs = (s.get('metadata') or {}).get('HealingSpot')
        if hs: spots.append(('HealingSpot of %d %s' % (s['id'], s.get('name', '')), s['id'], tuple(int(v) for v in hs)))
    tm = os.path.join(os.path.dirname(HERE), 'pbs', 'town_map.txt')
    if os.path.exists(tm):
        for line in open(tm, encoding='utf-8'):
            if not line.startswith('Point'): continue
            f = [v.strip() for v in line.split('=', 1)[1].split(',')]
            if len(f) >= 7 and f[4] and f[5] and f[6]:
                spots.append(('fly spot "%s"' % f[2], None, (int(f[4]), int(f[5]), int(f[6]))))
    cache = {}
    bad = 0
    for what, owner, (mid, x, y) in spots:
        if mid not in by_id: continue
        p = os.path.join(OUT, 'Data', 'Map%03d.rxdata' % mid)
        if not os.path.exists(p): continue
        if mid not in cache:
            m = M.load_file(p); ts = R.tilesets()[m.tileset_id]; lay = m.data.data
            solid = {(e.x, e.y) for e in m.events.values() if (e.pages[0].graphic.character_name or e.pages[0].graphic.tile_id) and not e.pages[0].through}
            ok = np.array([[cell_passable(lay, ts, xx, yy) and (xx, yy) not in solid for xx in range(m.width)] for yy in range(m.height)])
            exits = {(e.x, e.y) for e in m.events.values() if any(c.code == 201 for pg in e.pages for c in pg.list)}
            sides = {c['dir'][0].upper() for c in by_id[mid].get('connections', []) or []}
            for c in (s for s in specs if any(cc.get('to') == mid for cc in s.get('connections', []) or [])):
                for cc in c.get('connections', []):
                    if cc.get('to') == mid: sides.add({'N': 'S', 'S': 'N', 'W': 'E', 'E': 'W'}[cc['dir'][0].upper()])
            cache[mid] = (m, ok, exits, sides)
        m, ok, exits, sides = cache[mid]
        tag = owner if owner is not None else mid
        if not (0 <= x < m.width and 0 <= y < m.height) or not ok[y, x]:
            ctx.warn(tag, 'SPOT: %s lands on map %d (%d,%d), a blocked or covered tile' % (what, mid, x, y)); bad += 1; continue
        seen = np.zeros_like(ok); st = [(x, y)]; out = False
        while st and not out:
            cx, cy = st.pop()
            if seen[cy, cx]: continue
            seen[cy, cx] = True
            if ((cx == 0 and 'W' in sides) or (cx == m.width - 1 and 'E' in sides) or (cy == 0 and 'N' in sides)
                    or (cy == m.height - 1 and 'S' in sides)):
                out = True; break
            for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                nx, ny = cx + dx, cy + dy
                if (nx, ny) in exits: out = True; break
                if 0 <= nx < m.width and 0 <= ny < m.height and ok[ny, nx] and not seen[ny, nx]: st.append((nx, ny))
        if not out:
            ctx.warn(tag, 'SPOT: %s on map %d (%d,%d) is boxed in: no door, warp or open edge can be walked to' % (what, mid, x, y)); bad += 1
    return bad


def check_arrivals(selected, specs, ctx):
    """Playtest blockers (2026-11-17): every Transfer Player of a built map must land on a passable tile that no solid
    event or decor covers; a door tile (interior exits land on it) and the tile below it (the door event walks the player
    out) must be passable.  Returns the number of problems; each is an ARRIVAL warning."""
    import render as R
    built = {s['id'] for s in specs}
    cache = {}

    def load(mid):
        if mid not in cache:
            p = os.path.join(OUT, 'Data', 'Map%03d.rxdata' % mid)
            cache[mid] = M.load_file(p) if os.path.exists(p) else None
        return cache[mid]

    def solid_event(m, x, y, skip=None):
        for ev in m.events.values():
            if ev.x == x and ev.y == y and ev is not skip:
                pg = ev.pages[0]; g = pg.graphic
                if (g.character_name or g.tile_id) and not pg.through: return ev.name
        return None

    def is_door(ev):
        return any(c.code == 201 for p in ev.pages for c in p.list) and any(
            c.code == 209 for p in ev.pages for c in p.list)

    bad = 0
    sel = {s['id'] for s in selected}
    for s in specs:                                         # every built map's transfers, reported when either end is selected
        m = load(s['id'])
        if m is None: continue
        for ev in m.events.values():
            for pg in ev.pages:
                for c in pg.list:
                    if c.code != 201 or c.parameters[0] != 0: continue
                    tm, tx, ty = c.parameters[1], c.parameters[2], c.parameters[3]
                    if tm not in built or (s['id'] not in sel and tm not in sel): continue
                    dm = load(tm)
                    if dm is None: continue
                    ts = R.tilesets()[dm.tileset_id]
                    lay = dm.data.data
                    door_here = next((e for e in dm.events.values() if e.x == tx and e.y == ty and is_door(e)), None)
                    if not cell_passable(lay, ts, tx, ty):
                        ctx.warn(s['id'], 'ARRIVAL: "%s" lands on map %d (%d,%d), a blocked tile' % (ev.name, tm, tx, ty)); bad += 1
                    who = solid_event(dm, tx, ty, door_here)
                    if who:
                        ctx.warn(s['id'], 'ARRIVAL: "%s" lands on map %d (%d,%d) under event "%s"' % (ev.name, tm, tx, ty, who)); bad += 1
                    if door_here is not None and not (cell_passable(lay, ts, tx, ty + 1) and not solid_event(dm, tx, ty + 1)):
                        ctx.warn(s['id'], 'ARRIVAL: "%s" lands on door "%s" (map %d), but the step out (%d,%d) is blocked'
                                 % (ev.name, door_here.name, tm, tx, ty + 1)); bad += 1
                    break
    return bad


def check_seams(specs, ctx):
    """map builder 9 (REQUESTS item 11): every connection edge, tile by tile.  A walkable tile on one map's joined edge
    must meet a walkable tile across the seam (and that tile must reach the neighbour's first door/warp or another
    edge), or walking off the edge strands the player.  Returns the number of SEAM problems."""
    import render as R
    by_id = {s['id']: s for s in specs}
    cache = {}

    def load(mid):
        if mid not in cache:
            p = os.path.join(OUT, 'Data', 'Map%03d.rxdata' % mid)
            if not os.path.exists(p): cache[mid] = None
            else:
                m = M.load_file(p); ts = R.tilesets()[m.tileset_id]; lay = m.data.data
                solid = {(e.x, e.y) for e in m.events.values() if (e.pages[0].graphic.character_name or e.pages[0].graphic.tile_id) and not e.pages[0].through}
                ok = np.array([[cell_passable(lay, ts, x, y) and (x, y) not in solid for x in range(m.width)] for y in range(m.height)])
                cache[mid] = (m, ok)
        return cache[mid]
    OPP = {'N': 'S', 'S': 'N', 'W': 'E', 'E': 'W'}
    bad = 0; done = set()
    for s in specs:
        for c in s.get('connections', []) or []:
            a, b_ = s['id'], c['to']
            key = tuple(sorted((a, b_)))
            if key in done or b_ not in by_id: continue
            done.add(key)
            A, B = load(a), load(b_)
            if not A or not B: continue
            (ma, oka), (mb, okb) = A, B
            d = c['dir'][0].upper(); oa, ob = c.get('offset', 0), c.get('to_offset', 0)
            if d in 'NS':
                ya = 0 if d == 'N' else ma.height - 1; yb = mb.height - 1 if d == 'N' else 0
                pairs = [((x, ya), (x - oa + ob, yb)) for x in range(ma.width)]
            else:
                xa = 0 if d == 'W' else ma.width - 1; xb = mb.width - 1 if d == 'W' else 0
                pairs = [((xa, y), (xb, y - oa + ob)) for y in range(ma.height)]
            opened = 0; ab = []; ba = []
            for (x1, y1), (x2, y2) in pairs:
                inb = 0 <= x2 < mb.width and 0 <= y2 < mb.height
                pa = oka[y1, x1]; pb = okb[y2, x2] if inb else False
                if pa and pb: opened += 1
                elif pa and not pb: ab.append((x1, y1, x2, y2))
                elif pb and not pa and inb: ba.append((x2, y2, x1, y1))
            if ab:
                x1, y1, x2, y2 = ab[0]
                ctx.warn(a, 'SEAM: %d tile(s) of %d\'s %s edge lead onto blocked ground of map %d, e.g. (%d,%d) -> (%d,%d)' % (len(ab), a, d, b_, x1, y1, x2, y2)); bad += len(ab)
            if ba:
                x1, y1, x2, y2 = ba[0]
                ctx.warn(b_, 'SEAM: %d tile(s) of %d\'s %s edge lead onto blocked ground of map %d, e.g. (%d,%d) -> (%d,%d)' % (len(ba), b_, OPP[d], a, x1, y1, x2, y2)); bad += len(ba)
            if not opened:
                ctx.warn(a, 'SEAM: connection %d %s <-> %d has no walkable crossing at all' % (a, d, b_)); bad += 1
    return bad


def slug(n):
    return ''.join(c if (c.isascii() and c.isalnum()) else '_' for c in n).strip('_')[:40]


if __name__ == '__main__':
    main()
