#!/usr/bin/env python3
"""import_tileset.py - register a NEW tileset (graphic + autotiles + passages/priorities/terrain tags) for the
map generator and for the user's project.

    python3 -I import_tileset.py mapgen/tilesets/<name>.yaml [--palette-skeleton]

Descriptor (YAML):
    id: 30                          # RMXP tileset ID (pick one the user's project doesn't use; base project uses 1-25)
    name: Prismfall Coast           # Database name
    tileset_name: Prismfall Coast   # file name in Graphics/Tilesets (no .png)
    graphic: /abs/path/Coast.png    # 256 px wide, height a multiple of 32
    autotiles:                      # up to 7 slots; `file` is copied, omit it to reuse a graphic the project already has
      - {name: Sea}
      - {name: Coast foam, file: /abs/path/Coast foam.png}
    battleback: ''
    defaults: {passage: 0, priority: 0, terrain: 0}
    passages:     {"384": 15, "392-399": 15}    # tile id or inclusive range -> value (15 = blocked all ways)
    priorities:   {"640-647": 1}
    terrain_tags: {"390": 2}
    autotile_props: {1: {passage: 15, priority: 0, terrain: 7}}   # per slot 1-7: applies to all 48 ids

Writes:
  maps_out/Graphics/Tilesets/<tileset_name>.png and maps_out/Graphics/Autotiles/*.png (copies)
  maps_out/tilesets_prismfall.json  (same format as mapgen/data/tilesets.json; read by render.py / build.py QA)
  palettes/<slug>.yaml skeleton with --palette-skeleton (only if it doesn't exist)
The user's Data/Tilesets.rxdata is updated separately by merge_tilesets.py (backup, collision check)."""
import sys, os, json, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import yaml
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), 'maps_out')
REG = os.path.join(OUT, 'tilesets_prismfall.json')


def expand(spec):
    out = {}
    for k, v in (spec or {}).items():
        k = str(k)
        if '-' in k:
            a, b = k.split('-')
            for i in range(int(a), int(b) + 1):
                out[i] = int(v)
        else:
            out[int(k)] = int(v)
    return out


TAG_REMAP = {17: 0, 18: 16, 19: 10, 21: 10, 22: 10, 23: 10, 25: 7, 33: 7, 35: 7, 36: 7, 37: 7, 38: 7, 26: 0, 28: 6}


def entry_from_rxdata(d):
    """from_rxdata: {file: .../Tilesets.rxdata, id: 24, graphics: <dir with Tilesets/ and Autotiles/>, remap_tags: true}
    Reads passages/priorities/terrain tags with the safe parser; terrain tags > 16 are remapped to v21.1 ids."""
    import rmarshal as M
    f = d['from_rxdata']
    t = M.load_file(f['file'])[int(f['id'])]
    tags = [int(x) for x in t.terrain_tags.data.reshape(-1)]
    if f.get('remap_tags', True):
        tags = [x if x <= 16 else TAG_REMAP.get(x, 0) for x in tags]
    g = f['graphics']
    d['graphic'] = os.path.join(g, 'Tilesets', t.tileset_name + '.png')
    d.setdefault('tileset_name', d.get('name', t.name))
    d['autotiles'] = [{'name': n, 'file': os.path.join(g, 'Autotiles', n + '.png')} if n else {'name': ''}
                      for n in t.autotile_names]
    return dict(id=int(d['id']), name=d['name'], tileset_name=d['tileset_name'], autotile_names=list(t.autotile_names),
                panorama='', fog='', battleback='', n_tiles=t.passages.xsize,
                passages=[int(x) for x in t.passages.data.reshape(-1)],
                priorities=[int(x) for x in t.priorities.data.reshape(-1)], terrain_tags=tags)


def build_entry(d):
    if 'from_rxdata' in d:
        return entry_from_rxdata(d)
    im = Image.open(d['graphic'])
    if im.width != 256 or im.height % 32:
        sys.exit('tileset graphic must be 256 px wide and a multiple of 32 tall (got %dx%d)' % im.size)
    n = 384 + (im.height // 32) * 8
    dflt = d.get('defaults', {})
    pas = [int(dflt.get('passage', 0))] * n
    pri = [int(dflt.get('priority', 0))] * n
    ter = [int(dflt.get('terrain', 0))] * n
    pas[0] = pri[0] = ter[0] = 0
    autos = [a.get('name', '') for a in (d.get('autotiles') or [])][:7]
    autos += [''] * (7 - len(autos))
    for slot, props in (d.get('autotile_props') or {}).items():
        for i in range(int(slot) * 48, int(slot) * 48 + 48):
            pas[i] = int(props.get('passage', pas[i])); pri[i] = int(props.get('priority', pri[i]))
            ter[i] = int(props.get('terrain', ter[i]))
    for table, key in ((pas, 'passages'), (pri, 'priorities'), (ter, 'terrain_tags')):
        for i, v in expand(d.get(key)).items():
            if 0 <= i < n:
                table[i] = v
    return dict(id=int(d['id']), name=d['name'], tileset_name=d['tileset_name'], autotile_names=autos,
                panorama='', fog='', battleback=d.get('battleback', ''), n_tiles=n,
                passages=pas, priorities=pri, terrain_tags=ter)


def main():
    a = sys.argv[1:]
    d = yaml.safe_load(open(a[0]))
    entry = build_entry(d)
    base_ids = {t['id'] for t in json.load(open(os.path.join(HERE, 'data', 'tilesets.json')))}
    if entry['id'] in base_ids and not d.get('replace'):
        sys.exit('tileset id %d is a base-project tileset; pick another id (or set replace: true)' % entry['id'])
    os.makedirs(os.path.join(OUT, 'Graphics', 'Tilesets'), exist_ok=True)
    os.makedirs(os.path.join(OUT, 'Graphics', 'Autotiles'), exist_ok=True)
    shutil.copyfile(d['graphic'], os.path.join(OUT, 'Graphics', 'Tilesets', d['tileset_name'] + '.png'))
    for at in d.get('autotiles') or []:
        if at.get('file'):
            shutil.copyfile(at['file'], os.path.join(OUT, 'Graphics', 'Autotiles', at['name'] + '.png'))
    reg = json.load(open(REG)) if os.path.exists(REG) else []
    reg = [t for t in reg if t['id'] != entry['id']] + [entry]
    json.dump(sorted(reg, key=lambda t: t['id']), open(REG, 'w'))
    print('registered tileset %d "%s" (%d tiles) -> %s' % (entry['id'], entry['name'], entry['n_tiles'] - 384, REG))
    if '--palette-skeleton' in a:
        slug = ''.join(c if c.isalnum() else '_' for c in d['name'].lower())
        p = os.path.join(HERE, 'palettes', slug + '.yaml')
        if not os.path.exists(p):
            first = next((i for i in range(384, entry['n_tiles']) if entry['passages'][i] & 15 == 0), 384)
            open(p, 'w').write('# Palette skeleton for imported tileset %d "%s". Fill in classes/glyphs (see outside.yaml).\n'
                               'tileset: %d\nground: {base: %d}\nclasses:\n  floor: {kind: ground}\ntiles: {}\n'
                               'glyphs:\n  \'.\': floor\n' % (entry['id'], d['name'], entry['id'], first))
            print('wrote palette skeleton', p)


if __name__ == '__main__':
    main()
