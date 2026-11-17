#!/usr/bin/env python3
"""export_tilesets_rxdata.py - write maps_out/Data/Tilesets_prismfall.rxdata: a Marshal file holding ONLY the
Prismfall RPG::Tileset entries registered in maps_out/tilesets_prismfall.json (import_tileset.py).

    python3 -I export_tilesets_rxdata.py [--check]

The file is a Hash {id => RPG::Tileset}. The in-game installer (Plugins/Prismfall Maps/001_Installer.rb,
Debug > Files > Install Prismfall maps) merges it into the project's own Data/Tilesets.rxdata with the game's
Marshal, so Windows users need neither Python nor numpy. tools/package.sh runs this before packaging.
Entries are built with merge_tilesets.tileset_obj, so both install paths write the same RPG::Tileset.
--check only reports whether the file on disk matches the registry."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rmarshal as M
from merge_tilesets import tileset_obj

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), 'maps_out')
DEST = os.path.join(OUT, 'Data', 'Tilesets_prismfall.rxdata')


def build():
    reg = json.load(open(os.path.join(OUT, 'tilesets_prismfall.json'), encoding='utf-8'))
    ret = {}
    for e in sorted(reg, key=lambda e: e['id']):
        n = len(e['passages'])
        if not (len(e['priorities']) == len(e['terrain_tags']) == n):
            sys.exit('tileset %d: passages/priorities/terrain_tags lengths differ' % e['id'])
        if len(e['autotile_names']) != 7:
            sys.exit('tileset %d: needs 7 autotile names' % e['id'])
        if e['id'] in ret:
            sys.exit('tileset %d registered twice' % e['id'])
        ret[e['id']] = tileset_obj(e)
    return ret


def main():
    data = M.dumps(build())
    if '--check' in sys.argv[1:]:
        same = os.path.exists(DEST) and open(DEST, 'rb').read() == data
        print('%s is %s' % (DEST, 'up to date' if same else 'STALE or missing'))
        sys.exit(0 if same else 1)
    os.makedirs(os.path.dirname(DEST), exist_ok=True)
    with open(DEST, 'wb') as f:
        f.write(data)
    chk = M.load_file(DEST)
    print('wrote %s: tilesets %s (%d bytes)' % (DEST, sorted(chk), len(data)))


if __name__ == '__main__':
    main()
