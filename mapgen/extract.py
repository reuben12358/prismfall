#!/usr/bin/env python3
"""Extract stamps + interior templates from the reference project's maps (safe parser) into mapgen/data.
usage: python3 -I extract.py [--sheet out.png]"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import yaml
import numpy as np
import rmarshal as M
import rjson
import render as R
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.environ.get('PRISMFALL_REF', '/home/claude/ref/ebdx')
GROUND = {1: set(range(384, 424)) | set(range(536, 576)) | set(range(480, 536))}


def load_map(mid):
    return M.load_file(os.path.join(REF, 'Data', 'Map%03d.rxdata' % mid))


def main():
    spec = yaml.safe_load(open(os.path.join(HERE, 'extract.yaml')))
    stamps = {}
    for name, s in (spec.get('stamps') or {}).items():
        m = load_map(s['map'])
        x, y, w, h = s['rect']
        lay = m.data.data[:, y:y + h, x:x + w].astype(int).copy()
        ground = GROUND.get(m.tileset_id, set())
        if not s.get('keep_ground'):
            lay[0][np.isin(lay[0], list(ground))] = 0
            lay[0][lay[0] < 384] = 0          # autotiles (water etc.) belong to the terrain, not the stamp
            for v in s.get('drop0', []):
                lay[0][lay[0] == v] = 0
            if s.get('drop0_all'):
                lay[0][:] = 0
            for v in s.get('drop1', []):
                lay[1][lay[1] == v] = 0
        st = dict(tileset=m.tileset_id, w=w, h=h, layers=lay.tolist(), src=[s['map']] + s['rect'])
        if 'door' in s:
            dx, dy = s['door']
            st['door'] = [dx, dy]
            ev = next((e for e in m.events.values() if e.x == x + dx and e.y == y + dy), None)
            if ev is not None:
                g = ev.pages[0].graphic
                st['door_gfx'] = [g.character_name, g.pattern, g.direction]
            else:
                print('WARN no door event for', name)
        stamps[name] = st
    json.dump(stamps, open(os.path.join(HERE, 'data', 'stamps.json'), 'w'))
    os.makedirs(os.path.join(HERE, 'data', 'templates'), exist_ok=True)
    for name, t in (spec.get('templates') or {}).items():
        m = load_map(t['map'])
        r = t.get('rect', 'auto')
        if r == 'auto':
            void = int(m.data.data[0, m.height - 1, m.width - 1])
            occ = (m.data.data[0] != void) | (m.data.data[1] > 0) | (m.data.data[2] > 0)
            for e in m.events.values():
                occ[e.y, e.x] = True
            nz = np.argwhere(occ)
            (y0, x0), (y1, x1) = nz.min(axis=0), nz.max(axis=0)
            r = [int(x0), int(y0), int(x1 - x0 + 1), int(y1 - y0 + 1)]
        x, y, w, h = r
        lay = m.data.data[:, y:y + h, x:x + w].astype(int)
        evs = []
        for e in sorted(m.events.values(), key=lambda e: e.id):
            if x <= e.x < x + w and y <= e.y < y + h and e.name not in t.get('drop_events', []):
                e.ivars['x'] = e.x - x; e.ivars['y'] = e.y - y
                evs.append(rjson.to_j(e))
        out = dict(tileset=m.tileset_id, w=w, h=h, layers=lay.tolist(), events=evs, src=[t['map']] + [x, y, w, h],
                   bgm=m.bgm.name)
        json.dump(out, open(os.path.join(HERE, 'data', 'templates', name + '.json'), 'w'))
    print('stamps:', len(stamps), 'templates:', len(spec.get('templates') or {}))
    if '--sheet' in sys.argv:
        sheet(stamps, sys.argv[sys.argv.index('--sheet') + 1])


def sheet(stamps, out):
    ims = []
    for name, st in stamps.items():
        ts = R.tilesets()[st['tileset']]
        tc = R.TileCache(ts)
        im = Image.new('RGBA', (st['w'] * 32, st['h'] * 32), (90, 160, 90, 255))
        for z in range(3):
            for yy in range(st['h']):
                for xx in range(st['w']):
                    t = st['layers'][z][yy][xx]
                    if t > 0 and tc.tile(t) is not None:
                        im.alpha_composite(tc.tile(t), (xx * 32, yy * 32))
        if 'door' in st:
            ImageDraw.Draw(im).rectangle([st['door'][0] * 32, st['door'][1] * 32, st['door'][0] * 32 + 31, st['door'][1] * 32 + 31], outline=(255, 0, 0, 255), width=2)
        ims.append((name, im))
    W = sum(i.width + 8 for _, i in ims); H = max(i.height for _, i in ims) + 14
    sh = Image.new('RGBA', (W, H), (30, 30, 40, 255)); d = ImageDraw.Draw(sh); x = 0
    for n, i in ims:
        sh.paste(i, (x, 14)); d.text((x, 1), n, fill=(255, 255, 0, 255)); x += i.width + 8
    sh.convert('RGB').save(out); print('sheet', out, sh.size)


if __name__ == '__main__':
    main()
