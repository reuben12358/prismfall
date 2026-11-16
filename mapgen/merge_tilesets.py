#!/usr/bin/env python3
"""merge_tilesets.py - add the imported Prismfall tilesets (maps_out/tilesets_prismfall.json, written by
import_tileset.py) to a user's RPG Maker XP project.

    python3 -I merge_tilesets.py <ProjectDir> [--dry-run] [--force]

Close RPG Maker XP first. Backs up Data/Tilesets.rxdata once (Tilesets.rxdata.prismfall-bak), copies
maps_out/Graphics/{Tilesets,Autotiles}/* into the project, then writes one RPG::Tileset per registered entry at
its ID. If the array is shorter, blank tilesets pad it, as RMXP's Database needs every slot to exist. An ID
already in use by a differently-named tileset is reported and skipped unless --force."""
import sys, os, json, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import rmarshal as M
from rmarshal import RObject, Sym, Table

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), 'maps_out')


def table1(values):
    a = np.array(values, dtype=np.int16).reshape((1, 1, len(values)))
    return Table(len(values), 1, 1, 1, a)


def tileset_obj(e):
    return RObject(Sym('RPG::Tileset'), dict(
        terrain_tags=table1(e['terrain_tags']), panorama_hue=0, fog_sy=0, name=e['name'], fog_opacity=64,
        priorities=table1(e['priorities']), panorama_name='', fog_sx=0, fog_hue=0, passages=table1(e['passages']),
        autotile_names=list(e['autotile_names']), fog_zoom=100, fog_name='', battleback_name=e.get('battleback', ''),
        tileset_name=e['tileset_name'], id=e['id'], fog_blend_type=0))


def blank(i):
    return tileset_obj(dict(id=i, name='', tileset_name='', autotile_names=[''] * 7, passages=[0] * 384,
                            priorities=[5] + [0] * 383, terrain_tags=[0] * 384))


def main():
    a = sys.argv[1:]
    if not a or a[0].startswith('-'):
        sys.exit(__doc__)
    proj = a[0]
    path = os.path.join(proj, 'Data', 'Tilesets.rxdata')
    reg = json.load(open(os.path.join(OUT, 'tilesets_prismfall.json')))
    ts = M.load_file(path)
    added = []
    for e in reg:
        i = e['id']
        while len(ts) <= i:
            ts.append(blank(len(ts)))
        cur = ts[i]
        if cur is not None and cur.name not in ('', e['name']) and '--force' not in a:
            print('COLLISION: tileset %d is "%s" in this project; skipped "%s"' % (i, cur.name, e['name']))
            continue
        ts[i] = tileset_obj(e)
        added.append(i)
    print('tilesets to write: %s' % added)
    if '--dry-run' in a:
        return
    for sub in ('Tilesets', 'Autotiles'):
        src = os.path.join(OUT, 'Graphics', sub)
        if os.path.isdir(src):
            os.makedirs(os.path.join(proj, 'Graphics', sub), exist_ok=True)
            for f in os.listdir(src):
                shutil.copyfile(os.path.join(src, f), os.path.join(proj, 'Graphics', sub, f))
    bak = path + '.prismfall-bak'
    if not os.path.exists(bak):
        shutil.copyfile(path, bak)
    M.dump_file(ts, path)
    chk = M.load_file(path)
    assert all(chk[i].name == next(e['name'] for e in reg if e['id'] == i) for i in added)
    print('wrote', path)


if __name__ == '__main__':
    main()
