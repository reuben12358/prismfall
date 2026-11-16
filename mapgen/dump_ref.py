#!/usr/bin/env python3
"""Summarize reference Tilesets.rxdata / MapInfos.rxdata / maps (read-only, safe parser).
usage: python3 -I dump_ref.py <ProjectDir> [out_dir]
Writes tilesets.json, mapinfos.json, maps_summary.json into out_dir (default mapgen/ref_dump)."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rmarshal as M
from collections import Counter


def main():
    proj = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ref_dump')
    os.makedirs(out, exist_ok=True)
    ts = M.load_file(os.path.join(proj, 'Data', 'Tilesets.rxdata'))
    tsj = []
    for t in ts:
        if t is None:
            continue
        n = t.passages.xsize
        tsj.append(dict(id=t.id, name=t.name, tileset_name=t.tileset_name,
                        autotile_names=list(t.autotile_names), panorama=t.panorama_name, fog=t.fog_name,
                        battleback=t.battleback_name, n_tiles=n,
                        passages=[int(x) for x in t.passages.data.reshape(-1)],
                        priorities=[int(x) for x in t.priorities.data.reshape(-1)],
                        terrain_tags=[int(x) for x in t.terrain_tags.data.reshape(-1)]))
    json.dump(tsj, open(os.path.join(out, 'tilesets.json'), 'w'))
    for t in tsj:
        print('tileset %3d %-28s img=%-28s n=%d auto=%s' % (t['id'], t['name'], t['tileset_name'], t['n_tiles'],
              [a for a in t['autotile_names'] if a]))
    mi = M.load_file(os.path.join(proj, 'Data', 'MapInfos.rxdata'))
    mij = {}
    for k, v in sorted(mi.items()):
        mij[k] = dict(name=v.name, parent_id=v.parent_id, order=v.order, expanded=v.expanded, scroll_x=v.scroll_x,
                      scroll_y=v.scroll_y)
    json.dump(mij, open(os.path.join(out, 'mapinfos.json'), 'w'), indent=0)
    print('mapinfos:', len(mij), 'ivar order:', list(next(iter(mi.values())).ivars.keys()))
    maps = {}
    for k in sorted(mi):
        p = os.path.join(proj, 'Data', 'Map%03d.rxdata' % k)
        if not os.path.exists(p):
            continue
        m = M.load_file(p)
        maps[k] = dict(name=mi[k].name, tileset_id=m.tileset_id, w=m.width, h=m.height, n_events=len(m.events),
                       bgm=m.bgm.name, autoplay_bgm=m.autoplay_bgm, ivars=list(m.ivars.keys()))
    json.dump(maps, open(os.path.join(out, 'maps_summary.json'), 'w'), indent=0)
    for k, v in maps.items():
        print('map %3d %-26s ts=%2d %3dx%-3d ev=%3d bgm=%s' % (k, v['name'], v['tileset_id'], v['w'], v['h'],
              v['n_events'], v['bgm']))


if __name__ == '__main__':
    main()
