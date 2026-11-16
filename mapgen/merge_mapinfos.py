#!/usr/bin/env python3
"""merge_mapinfos.py - install generated Prismfall maps into a user's RPG Maker XP / Essentials project.

    python3 -I merge_mapinfos.py <ProjectDir> [--maps-out DIR] [--dry-run] [--no-copy]

Steps (close RPG Maker XP first - it rewrites MapInfos.rxdata when it saves):
  1. backs up <ProjectDir>/Data/MapInfos.rxdata -> MapInfos.rxdata.prismfall-bak (once; never overwritten)
  2. copies maps_out/Data/MapNNN.rxdata into <ProjectDir>/Data (refuses to overwrite a map whose MapInfos name
     is not ours unless --force), plus maps_out/PBS/*_prismfall.txt into <ProjectDir>/PBS
  3. reads the project's OWN MapInfos.rxdata (safe pure-Python parser), adds one RPG::MapInfo per line of
     maps_out/mapinfos_prismfall.txt (id, parent, name), keeping every existing entry untouched.
     ID collisions with a differently-named existing map are reported and skipped.
  4. writes MapInfos.rxdata back (existing strings keep their original encoding style).
No prebuilt MapInfos is shipped: the merge always starts from the user's file.
An in-game alternative (uses the game's own Marshal) is the 'Prismfall Map Installer' debug plugin in maps_out/Plugins."""
import sys, os, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rmarshal as M
import rpg as G

HERE = os.path.dirname(os.path.abspath(__file__))


def read_entries(path):
    out = []
    for line in open(path, encoding='utf-8'):
        if not line.strip() or line.startswith('#'):
            continue
        i, p, name = line.rstrip('\n').split('\t', 2)
        out.append((int(i), int(p), name))
    return out


def merge(infos, entries, log=print):
    """infos: dict id -> RObject(RPG::MapInfo) (modified in place). Returns (added, skipped)."""
    max_order = max([v.order for v in infos.values()] + [0])
    ours = {i for i, _, _ in entries}
    by_id = {i: (p, n) for i, p, n in entries}
    added, skipped = [], []
    # parents before children: DFS order over our own tree
    children = {}
    for i, p, n in entries:
        children.setdefault(p if p in ours else 0, []).append(i)
    order = []
    def walk(pid):
        for c in sorted(children.get(pid, [])):
            order.append(c); walk(c)
    walk(0)
    for i in order:
        p, n = by_id[i]
        if i in infos:
            if infos[i].name == n:
                skipped.append(i)   # already installed
            else:
                log('COLLISION: map id %d is already "%s" in this project; skipped "%s"' % (i, infos[i].name, n))
                skipped.append(i)
            continue
        if p and p not in infos and p not in ours:
            log('note: parent %d of map %d not found; attaching to root' % (p, i)); p = 0
        max_order += 1
        infos[i] = G.mapinfo(n, parent_id=p, order=max_order)
        added.append(i)
    return added, skipped


def main():
    a = sys.argv[1:]
    if not a or a[0].startswith('-'):
        sys.exit(__doc__)
    proj = a[0]
    mo = a[a.index('--maps-out') + 1] if '--maps-out' in a else os.path.join(os.path.dirname(HERE), 'maps_out')
    dry = '--dry-run' in a
    mi_path = os.path.join(proj, 'Data', 'MapInfos.rxdata')
    if not os.path.exists(mi_path):
        sys.exit('not an RMXP project (no Data/MapInfos.rxdata): %s' % proj)
    infos = M.load_file(mi_path)
    entries = read_entries(os.path.join(mo, 'mapinfos_prismfall.txt'))
    names = {i: n for i, _, n in entries}
    collide = {i for i in names if i in infos and infos[i].name != names[i]}
    if not dry and '--no-copy' not in a:
        n = 0
        for i in names:
            src = os.path.join(mo, 'Data', 'Map%03d.rxdata' % i)
            if not os.path.exists(src):
                continue
            if i in collide and '--force' not in a:
                continue
            shutil.copyfile(src, os.path.join(proj, 'Data', 'Map%03d.rxdata' % i)); n += 1
        os.makedirs(os.path.join(proj, 'PBS'), exist_ok=True)
        for f in os.listdir(os.path.join(mo, 'PBS')):
            shutil.copyfile(os.path.join(mo, 'PBS', f), os.path.join(proj, 'PBS', f))
        print('copied %d map files + PBS files' % n)
    added, skipped = merge(infos, entries)
    print('MapInfos: %d added, %d already present/skipped, %d collisions' % (len(added), len(skipped), len(collide)))
    if dry:
        print('dry run: nothing written'); return
    bak = mi_path + '.prismfall-bak'
    if not os.path.exists(bak):
        shutil.copyfile(mi_path, bak); print('backup:', bak)
    M.dump_file(infos, mi_path)
    chk = M.load_file(mi_path)
    assert all(i in chk for i in added)
    print('wrote', mi_path, '- now open the project in RPG Maker XP, then start the game in Debug mode and compile.')


if __name__ == '__main__':
    main()
