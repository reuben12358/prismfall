#!/usr/bin/env python3
"""Mine building stamps from the Rejuvenation (wll) reference maps into data/stamps_w.json, with tile ids remapped
onto the composite tileset 33 (compose_tileset.py). Objects only (layout is never copied): only tiles from the
building/prop rows of the source sheet are kept. Definitions: wextract.yaml. --sheet out.png renders them."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import yaml, numpy as np
import rmarshal as M, render as R
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
WD = '/home/claude/ref/art/wll/Changed Files/Data'


def main():
    spec = yaml.safe_load(open(os.path.join(HERE, 'wextract.yaml')))
    offs = json.load(open(os.path.join(HERE, 'data', 'compose_offsets.json')))
    out = {}; cache = {}
    for name, s in spec['stamps'].items():
        grp = spec['groups'][s.get('group', 'sheridan')]
        off = offs[grp['sheet']]['offset'] - 384
        rows = [tuple(r) for r in grp['rows']]; dropt = set(grp.get('drop', []))
        m = cache.setdefault(s['map'], M.load_file('%s/Map%03d.rxdata' % (WD, s['map'])))
        x, y, w, h = s['rect']
        lay = m.data.data[:, y:y + h, x:x + w].astype(int).copy()
        r = (lay - 384) // 8
        keep = np.zeros(lay.shape, bool)
        for a, b in rows: keep |= (lay >= 384) & (r >= a) & (r <= b)
        keep &= ~np.isin(lay, list(dropt))
        k0 = np.zeros(lay[0].shape, bool)
        for a, b in grp.get('rows0', []): k0 |= (lay[0] >= 384) & (r[0] >= a) & (r[0] <= b)
        keep[0] &= k0
        lay = np.where(keep, lay + off, 0)
        for c in s.get('clear', []):          # [x, y, w, h] relative cells to blank (stray neighbours)
            lay[:, c[1]:c[1] + c[3], c[0]:c[0] + c[2]] = 0
        occ = np.argwhere(lay.max(axis=0) > 0)
        (y0, x0), (y1, x1) = occ.min(axis=0), occ.max(axis=0)
        lay = lay[:, y0:y1 + 1, x0:x1 + 1]
        st = dict(tileset=33, w=int(x1 - x0 + 1), h=int(y1 - y0 + 1), layers=lay.tolist(), src=['wll', s['map'], x, y])
        doors = [(int(xx), int(yy)) for z in (1, 2) for yy, xx in np.argwhere(np.isin(lay[z] - off, grp.get('door_tiles', [])))]
        if doors:
            doors.sort(key=lambda d: (-d[1], d[0])); st['door'] = list(doors[0]); st['doors'] = [list(d) for d in doors]
            st['door_gfx'] = ['', 0, 2]
        out[name] = st
        for suf, key in (('_s', 'sheridan_slate'), ('_m', 'sheridan_moss')):      # recoloured variants
            if grp['sheet'] == 'sheridan' and key in offs:
                dlt = offs[key]['offset'] - offs['sheridan']['offset']
                v = dict(st); v['layers'] = np.where(lay > 0, lay + dlt, 0).tolist(); out[name + suf] = v
    for st in out.values():          # roofs belong on layer 3 (rubric 5): lift the upper rows where layer 3 is empty
        L = np.array(st['layers']); k = int(np.ceil(st['h'] * 0.6))
        m = (L[2, :k] == 0) & (L[1, :k] > 0)
        L[2, :k][m] = L[1, :k][m]; L[1, :k][m] = L[0, :k][m]; L[0, :k][m] = 0
        st['layers'] = L.tolist()
    json.dump(out, open(os.path.join(HERE, 'data', 'stamps_w.json'), 'w'))
    print({k: (v['w'], v['h'], v.get('door')) for k, v in out.items()})
    if '--sheet' in sys.argv:
        tc = R.TileCache(R.tilesets()[33]); x = 0
        sh = Image.new('RGB', (sum(v['w'] * 16 + 8 for v in out.values()), max(v['h'] for v in out.values()) * 16 + 14), (150, 200, 120))
        d = ImageDraw.Draw(sh)
        for name, st in out.items():
            im = Image.new('RGBA', (st['w'] * 32, st['h'] * 32), (150, 200, 120, 255))
            for z in range(3):
                for yy in range(st['h']):
                    for xx in range(st['w']):
                        t = st['layers'][z][yy][xx]
                        if t > 0 and tc.tile(t) is not None: im.alpha_composite(tc.tile(t), (xx * 32, yy * 32))
            for dd in st.get('doors', []):
                ImageDraw.Draw(im).rectangle([dd[0] * 32, dd[1] * 32, dd[0] * 32 + 31, dd[1] * 32 + 31], outline=(255, 0, 0, 255), width=3)
            sh.paste(im.resize((st['w'] * 16, st['h'] * 16)).convert('RGB'), (x, 12)); d.text((x, 0), name[:st['w'] * 3], fill=(0, 0, 0)); x += st['w'] * 16 + 8
        sh.save(sys.argv[sys.argv.index('--sheet') + 1]); print(sh.size)


if __name__ == '__main__':
    main()
