#!/usr/bin/env python3
"""Mine multi-tile stamps from the Tectonic reference maps (safe parser) -> data/stamps_t.json (tileset 30).
Definitions: textract.yaml  {name: {map, rect: [x,y,w,h], door: [dx,dy]?, keep0: false}}.
Layer 0 is dropped (terrain belongs to the painter) unless keep0; common terrain/foliage ids listed under
`drop` in the yaml are removed from layers 1-2 so stamps carry only the object.  --sheet out.png renders them."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import yaml, numpy as np
import rmarshal as M, render as R, probe as P
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
TD = '/home/claude/ref/art/tectonic/Data'


def main():
    spec = yaml.safe_load(open(os.path.join(HERE, 'textract.yaml')))
    drop = set(P.parse_ids([str(x) for x in spec.get('drop', [])]))
    out = {}; cache = {}
    for name, s in spec['stamps'].items():
        m = cache.setdefault(s['map'], M.load_file('%s/Map%03d.rxdata' % (TD, s['map'])))
        if 'seed' in s:   # 4-connected component of kept object tiles around the seed cell
            D = m.data.data
            d2 = drop - set(s.get('keep', []))
            obj = lambda xx, yy: any(int(D[z, yy, xx]) >= 384 and int(D[z, yy, xx]) not in d2 for z in (1, 2))
            seen = set(); st_ = [tuple(s['seed'])]
            while st_:
                cx, cy = st_.pop()
                if (cx, cy) in seen or not (0 <= cx < m.width and 0 <= cy < m.height) or not obj(cx, cy): continue
                seen.add((cx, cy)); st_ += [(cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)]
            if not seen:
                print('EMPTY seed', name); continue
            xs = [c[0] for c in seen]; ys = [c[1] for c in seen]
            x, y, w, h = min(xs), min(ys), max(xs) - min(xs) + 1, max(ys) - min(ys) + 1
            lay = m.data.data[:, y:y + h, x:x + w].astype(int).copy()
            for yy in range(h):
                for xx in range(w):
                    if (x + xx, y + yy) not in seen: lay[:, yy, xx] = 0
        else:
            x, y, w, h = s['rect']
            lay = m.data.data[:, y:y + h, x:x + w].astype(int).copy()
        if not s.get('keep0'):
            lay[0][:] = 0
        d2 = drop - set(s.get('keep', []))
        for z in (1, 2):
            lay[z][np.isin(lay[z], list(d2))] = 0
            lay[z][(lay[z] > 0) & (lay[z] < 384)] = 0
        occ = np.argwhere(lay.max(axis=0) > 0)
        if len(occ) == 0:
            print('EMPTY', name); continue
        (y0, x0), (y1, x1) = occ.min(axis=0), occ.max(axis=0)
        lay = lay[:, y0:y1 + 1, x0:x1 + 1]
        st = dict(tileset=30, w=int(x1 - x0 + 1), h=int(y1 - y0 + 1), layers=lay.tolist(), src=[s['map'], x + int(x0), y + int(y0)])
        if 'door' in s:
            st['door'] = [s['door'][0] - int(x0), s['door'][1] - int(y0)]; st['door_gfx'] = ['', 0, 2]
        out[name] = st
    json.dump(out, open(os.path.join(HERE, 'data', 'stamps_t.json'), 'w'))
    print('stamps:', {k: (v['w'], v['h']) for k, v in out.items()})
    if '--sheet' in sys.argv:
        tc = R.TileCache(R.tilesets()[30]); ims = []
        for name, st in out.items():
            im = Image.new('RGBA', (st['w'] * 32, st['h'] * 32), (150, 200, 120, 255))
            for z in range(3):
                for yy in range(st['h']):
                    for xx in range(st['w']):
                        t = st['layers'][z][yy][xx]
                        if t > 0 and tc.tile(t) is not None: im.alpha_composite(tc.tile(t), (xx * 32, yy * 32))
            if 'door' in st:
                ImageDraw.Draw(im).rectangle([st['door'][0] * 32, st['door'][1] * 32, st['door'][0] * 32 + 31, st['door'][1] * 32 + 31], outline=(255, 0, 0, 255), width=2)
            ims.append((name, im.resize((im.width // 2, im.height // 2))))
        rows = []; row = []; wsum = 0
        for n, i in ims:
            if wsum + i.width > 1300: rows.append(row); row = []; wsum = 0
            row.append((n, i)); wsum += i.width + 8
        rows.append(row)
        Hh = sum(max(i.height for _, i in r) + 16 for r in rows)
        sh = Image.new('RGB', (1310, Hh), (30, 30, 40)); d = ImageDraw.Draw(sh); y = 0
        for r in rows:
            x = 0
            for n, i in r:
                sh.paste(i, (x, y + 12)); d.text((x, y), n, fill=(255, 255, 0)); x += i.width + 8
            y += max(i.height for _, i in r) + 16
        sh.save(sys.argv[sys.argv.index('--sheet') + 1]); print(sh.size)


if __name__ == '__main__':
    main()
