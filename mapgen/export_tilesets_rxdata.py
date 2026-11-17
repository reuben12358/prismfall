#!/usr/bin/env python3
"""export_tilesets_rxdata.py - write maps_out/Data/Tilesets_prismfall.rxdata: a Marshal file holding ONLY the
Prismfall RPG::Tileset entries registered in maps_out/tilesets_prismfall.json (import_tileset.py).

    python3 -I export_tilesets_rxdata.py [--check]

The file is a Hash {id => RPG::Tileset}. The in-game installer (Plugins/Prismfall Maps/001_Installer.rb,
Debug > Files > Install Prismfall maps) merges it into the project's own Data/Tilesets.rxdata with the game's
Marshal, so Windows users need neither Python nor numpy. tools/package.sh runs this before packaging.
Entries are built with merge_tilesets.tileset_obj, so both install paths write the same RPG::Tileset.
--check only reports whether the file on disk matches the registry.
Also warns (kit sanity, read-only) when a map on one of these tilesets uses a tile ID the tileset doesn't have
(maps and tileset built at different times), or when the New Game start tile (004_NewGameStart.rb) is boxed in."""
import sys, os, json, re, glob
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


def _leaves(m, ts, x, y):
    """Can the player step off (x, y)? Essentials' playerPassable? on both tiles, events ignored."""
    def ok(tx, ty, d):
        bit = (1 << (d // 2 - 1)) & 0x0f
        for z in (2, 1, 0):
            t = m.data[tx, ty, z]
            if t == 0:
                continue
            p = ts.passages[t]
            if p & bit or (p & 0x0f) == 0x0f:
                return False
            if ts.priorities[t] == 0:
                return True
        return True
    for d, (dx, dy) in {2: (0, 1), 4: (-1, 0), 6: (1, 0), 8: (0, -1)}.items():
        nx, ny = x + dx, y + dy
        if 0 <= nx < m.width and 0 <= ny < m.height and ok(x, y, d) and ok(nx, ny, 10 - d):
            return True
    return False


def check_maps(tilesets):
    warns = []
    for p in sorted(glob.glob(os.path.join(OUT, 'Data', 'Map*.rxdata'))):
        m = M.load_file(p)
        ts = tilesets.get(m.tileset_id)
        if ts is not None and int(m.data.data.max()) >= ts.passages.xsize:
            warns.append('%s uses tile %d but tileset %d has %d ids (rebuild maps and tileset together)'
                         % (os.path.basename(p), int(m.data.data.max()), m.tileset_id, ts.passages.xsize))
    rb = os.path.join(OUT, 'Plugins', 'Prismfall Maps', '004_NewGameStart.rb')
    st = re.search(r'PRISMFALL_START\s*=\s*\[(\d+),\s*(\d+),\s*(\d+)\]', open(rb, encoding='utf-8').read()) \
        if os.path.exists(rb) else None
    mp = st and os.path.join(OUT, 'Data', 'Map%03d.rxdata' % int(st.group(1)))
    if mp and os.path.exists(mp):
        m = M.load_file(mp)
        x, y = int(st.group(2)), int(st.group(3))
        if m.tileset_id in tilesets and not _leaves(m, tilesets[m.tileset_id], x, y):
            warns.append('New Game start (%s, %d, %d) is boxed in: move PRISMFALL_START' % (st.group(1), x, y))
    for w in warns:
        print('WARN', w)
    return warns


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
    check_maps(chk)


if __name__ == '__main__':
    main()
