#!/usr/bin/env python3
"""Find building stamps in reference Outside maps by flood-filling the non-ground tiles above each door event.
usage: python3 -I find_buildings.py <tileset_id> <out_sheet.png> <out_candidates.json>"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rmarshal as M
import render as R
import learn as L
from PIL import Image, ImageDraw
import numpy as np


def component(d, sx, sy, W, H, ground, maxw=14, maxh=12):
    """4-connected cells whose layer1/2 (or non-ground layer0) is non-zero."""
    def solid(x, y):
        return int(d[1, y, x]) or int(d[2, y, x]) or (int(d[0, y, x]) not in ground)
    seen = set(); st = [(sx, sy)]
    while st:
        x, y = st.pop()
        if (x, y) in seen or not (0 <= x < W and 0 <= y < H) or not solid(x, y):
            continue
        if abs(x - sx) > maxw or abs(y - sy) > maxh:
            continue
        seen.add((x, y)); st += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    return seen


def main():
    tsid = int(sys.argv[1])
    ground = set(range(384, 424)) | set(range(536, 576)) | set(range(480, 536))
    cands = []
    seen_keys = set()
    for mid, m in L.maps_for(tsid):
        d = m.data.data; W, H = m.width, m.height
        for ev in m.events.values():
            g = ev.pages[0].graphic
            isdoor = 'door' in ev.name.lower() or g.character_name.lower().startswith('door')
            if not isdoor and not any(c.code == 201 for p in ev.pages for c in p.list):
                continue
            comp = component(d, ev.x, ev.y - 1, W, H, ground) | component(d, ev.x, ev.y, W, H, ground)
            if len(comp) < 6:
                continue
            xs = [c[0] for c in comp]; ys = [c[1] for c in comp]
            x0, y0, x1, y1 = min(xs), min(ys), max(xs), max(ys)
            key = d[:, y0:y1 + 1, x0:x1 + 1].tobytes()
            if key in seen_keys or (x1 - x0 + 1) > 16 or (y1 - y0 + 1) > 12 or y1 - y0 < 2:
                continue
            seen_keys.add(key)
            cands.append(dict(map=mid, event=ev.name, door=[ev.x - x0, ev.y - y0], rect=[x0, y0, x1 - x0 + 1, y1 - y0 + 1],
                              door_gfx=[g.character_name, g.pattern, g.direction], isdoor=isdoor))
    # contact sheet
    tiles = []
    for i, c in enumerate(cands):
        m = M.load_file(os.path.join(L.REF, 'Data', 'Map%03d.rxdata' % c['map']))
        im = R.render(m, events=False)
        x, y, w, h = c['rect']
        crop = im.crop((x * 32, y * 32, (x + w) * 32, (y + h) * 32))
        crop = crop.resize((crop.width // 2, crop.height // 2))
        dr = ImageDraw.Draw(crop)
        dr.rectangle([c['door'][0] * 16, c['door'][1] * 16, c['door'][0] * 16 + 15, c['door'][1] * 16 + 15], outline=(255, 0, 0, 255))
        tiles.append((i, crop))
    cols = 6; cw = max(t.width for _, t in tiles) + 6; ch = max(t.height for _, t in tiles) + 14
    sheet = Image.new('RGBA', (cols * cw, ((len(tiles) + cols - 1) // cols) * ch), (30, 30, 40, 255))
    dr = ImageDraw.Draw(sheet)
    for k, (i, t) in enumerate(tiles):
        x, y = (k % cols) * cw, (k // cols) * ch
        sheet.paste(t, (x + 3, y + 12))
        dr.text((x + 3, y), '#%d m%d %dx%d' % (i, cands[i]['map'], cands[i]['rect'][2], cands[i]['rect'][3]), fill=(255, 255, 0, 255))
    sheet.convert('RGB').save(sys.argv[2])
    json.dump(cands, open(sys.argv[3], 'w'), indent=0)
    print(len(cands), 'candidates', sheet.size)


if __name__ == '__main__':
    main()
