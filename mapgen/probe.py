#!/usr/bin/env python3
"""Research helpers (safe parser).
  probe.py region <MapNNN.rxdata> x y w h          -> print 3-layer tile ids + terrain tags/passages
  probe.py sheet <tileset_id> <out.png> <ids...|a-b>  -> labelled contact sheet of tile ids
  probe.py rows <tileset_id> <out.png> <row0> <nrows> -> labelled tileset rows (8 per row)
  probe.py freq <tileset_id> [layer]                 -> most frequent tile ids across reference maps"""
import sys, os, json
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rmarshal as M
import render as R
from PIL import Image, ImageDraw

REF = os.environ.get('PRISMFALL_REF', '/home/claude/ref/ebdx')


def region(path, x0, y0, w, h):
    m = M.load_file(path)
    ts = R.tilesets()[m.tileset_id]
    for z in range(3):
        print('layer', z)
        for y in range(y0, y0 + h):
            print('%3d: ' % y + ' '.join('%5d' % m.data[x, y, z] for x in range(x0, x0 + w)))
    print('terrain/pass/prio of top non-zero tile')
    for y in range(y0, y0 + h):
        row = []
        for x in range(x0, x0 + w):
            tops = [m.data[x, y, z] for z in range(3) if m.data[x, y, z]]
            t = tops[-1] if tops else 0
            row.append('%d/%02x/%d' % (ts['terrain_tags'][t], ts['passages'][t], ts['priorities'][t]))
        print('%3d: ' % y + ' '.join('%8s' % r for r in row))


def parse_ids(args):
    ids = []
    for a in args:
        if '-' in a:
            s, e = a.split('-'); ids += list(range(int(s), int(e) + 1))
        else:
            ids.append(int(a))
    return ids


def sheet(tsid, out, ids, cols=8, scale=1):
    ts = R.tilesets()[tsid]
    tc = R.TileCache(ts)
    rows = (len(ids) + cols - 1) // cols
    cw, ch = 32 * scale + 8, 32 * scale + 14
    img = Image.new('RGBA', (cols * cw, rows * ch), (40, 40, 60, 255))
    d = ImageDraw.Draw(img)
    for i, t in enumerate(ids):
        x, y = (i % cols) * cw + 4, (i // cols) * ch + 12
        im = tc.tile(t)
        if im is not None:
            if scale != 1:
                im = im.resize((32 * scale, 32 * scale), Image.NEAREST)
            bg = Image.new('RGBA', im.size, (255, 0, 255, 255)); bg.alpha_composite(im)
            img.alpha_composite(bg, (x, y))
        tag = ts['terrain_tags'][t] if t < len(ts['terrain_tags']) else 0
        lab = '%d' % t + ('t%d' % tag if tag else '') + ('p%d' % ts['priorities'][t] if t < len(ts['priorities']) and ts['priorities'][t] else '')
        d.text((x - 3, y - 12), lab, fill=(255, 255, 0, 255))
    img.convert('RGB').save(out)
    print('wrote', out, img.size)


def freq(tsid, layer=None):
    mi = json.load(open(os.path.join(R.HERE, 'data', 'maps_summary.json')))
    c = Counter()
    for k, v in mi.items():
        if v['tileset_id'] != tsid:
            continue
        m = M.load_file(os.path.join(REF, 'Data', 'Map%03d.rxdata' % int(k)))
        zs = [layer] if layer is not None else [0, 1, 2]
        for z in zs:
            c.update(int(t) for t in m.data.data[z].reshape(-1))
    return c


def main():
    a = sys.argv[1:]
    if a[0] == 'region':
        region(a[1], *map(int, a[2:6]))
    elif a[0] == 'sheet':
        sheet(int(a[1]), a[2], parse_ids(a[3:]))
    elif a[0] == 'rows':
        r0, n = int(a[3]), int(a[4])
        sheet(int(a[1]), a[2], list(range(384 + r0 * 8, 384 + (r0 + n) * 8)))
    elif a[0] == 'freq':
        c = freq(int(a[1]), int(a[2]) if len(a) > 2 else None)
        print(' '.join('%d:%d' % kv for kv in c.most_common(int(a[3]) if len(a) > 3 else 80)))


if __name__ == '__main__':
    main()
