#!/usr/bin/env python3
"""rcustom.py - the `pf` part of the PF Rejuv sheet: Prismfall's own pieces (giant trees, Briarwick's elder tree, silk
garlands and lanterns, the quay oil lamps, the moored Dovetail, material variants) ported from tileset 33 so they can
sit in Rejuvenation-family maps (MAPGEN 2h).  Greens of the tree art are re-graded onto Sheridan_2's foliage ramp so
the canopies match the forest around them (ART_DIRECTION 6: remap each source colour once, grid untouched).

    python3 -I rcustom.py && python3 -I rcompose.py
Writes data/rj_custom.png (256 x 32*CUSTOM_ROWS), data/rj_custom.json (passage/priority/tag per index, the 33->pf id
map) and data/stamps_rjc.json (stamps `pf_<name>` in PF Rejuv ids)."""
import os, sys, json, colorsys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image
import render as R, rcompose as RC
HERE = os.path.dirname(os.path.abspath(__file__))
OFF33 = json.load(open(os.path.join(HERE, 'data', 'compose_offsets.json')))
C2, C3 = OFF33['custom2']['offset'], OFF33['custom3']['offset']
SV = json.load(open(os.path.join(HERE, 'data', 'stamps_v.json')))
SM = json.load(open(os.path.join(HERE, 'data', 'stamps_m.json')))
TREES = ['g_elder', 'g_tree6', 'g_tree4', 'g_tree4p', 'g_tree2']
PROPS = ['p_lantern', 'p_silk', 'p_silk1', 'p_strand_w', 'p_strand_p', 'p_web', 'p_web1', 'p_loom', 'p_vat_b', 'p_vat_r',
         'p_vat_y', 'p_laundry', 'p_net', 'p_awning']
MATS = ['stairs_log@33', 'stairs_plank@33', 'signpost@33', 'lantern@33', 'logbench@33', 'barricade@33', 'glow@33']
SINGLES = {'lamp_off': C2 + 166, 'lamp_on': C2 + 167, 'garl_plain': C3 + 184, 'garl_pennant': C3 + 185,
           'garl_lantern': C3 + 186, 'garl_tufts': C3 + 187}


def sheridan_ramp():
    """Sheridan_2's tree greens, dark -> light (from the 3x4 forest tree, rows 26-29)."""
    im = Image.open(os.path.join(RC.RR.GAMES['rejuvenation'], 'Graphics', 'Tilesets', 'Sheridan_2.png')).convert('RGB')
    cols = {}
    for y in range(26 * 32, 30 * 32):
        for x in range(0, 96):
            r, g, b = im.getpixel((x, y))
            h, s, v = colorsys.rgb_to_hsv(r / 255., g / 255., b / 255.)
            if 0.22 < h < 0.48 and s > 0.25: cols[(r, g, b)] = v
    return sorted(cols, key=lambda c: cols[c])


def main():
    ts33 = R.tilesets()[33]; tc = R.TileCache(ts33)
    want = {}
    for n in TREES + PROPS:
        want[n] = SV[n]
    for n in MATS:
        want[n.replace('@33', '')] = SM[n]
    ship = json.load(open(os.path.join(HERE, 'data', 'ship_moored.json')))
    ids = set()
    for st in want.values():
        ids |= {t for t in np.array(st['layers']).reshape(-1).tolist() if t >= 384}
    ids |= set(SINGLES.values())
    off_ship = OFF33['ship_moored']['offset']
    ids |= {off_ship + i for _, _, _, i in ship}
    ids = sorted(ids)
    if len(ids) > RC.CUSTOM_ROWS * 8: raise SystemExit('custom part too small: %d tiles' % len(ids))
    tree_ids = {t for n in TREES for t in np.array(want[n]['layers']).reshape(-1).tolist() if t >= 384}
    ramp = sheridan_ramp()
    sheet = Image.new('RGBA', (256, RC.CUSTOM_ROWS * 32), (0, 0, 0, 0))
    idmap = {}; props = {}
    cache = {}
    for i, t in enumerate(ids):
        im = tc.tile(t)
        if im is None: continue
        im = im.copy()
        if t in tree_ids:                     # foliage greens -> Sheridan ramp by brightness; bark and windows untouched
            px = im.load()
            for yy in range(32):
                for xx in range(32):
                    r, g, b, a = px[xx, yy]
                    if not a: continue
                    k = (r, g, b)
                    if k not in cache:
                        h, s, v = colorsys.rgb_to_hsv(r / 255., g / 255., b / 255.)
                        cache[k] = ramp[min(len(ramp) - 1, int(v * len(ramp)))] if (0.18 < h < 0.45 and s > 0.2) else k
                    px[xx, yy] = cache[k] + (a,)
        sheet.paste(im, ((i % 8) * 32, (i // 8) * 32))
        idmap[t] = i
        props[i] = (ts33['passages'][t], ts33['priorities'][t], ts33['terrain_tags'][t])
    sheet.save(os.path.join(HERE, 'data', 'rj_custom.png'))
    json.dump({'props': {str(k): v for k, v in props.items()}, 'map33': {str(k): v for k, v in idmap.items()},
               'singles': {k: idmap[v] for k, v in SINGLES.items()}}, open(os.path.join(HERE, 'data', 'rj_custom.json'), 'w'))
    # stamps in PF Rejuv ids (the pf part's offset is fixed: it is the last part)
    base = json.load(open(os.path.join(HERE, 'data', 'rj_compose.json')))['parts']['pf']['offset']
    out = {}
    for n, st in want.items():
        L = np.array(st['layers'])
        L2 = np.where(L >= 384, np.vectorize(lambda t: base + idmap.get(int(t), 0) if t >= 384 else 0)(L), 0)
        d = dict(w=st['w'], h=st['h'], layers=L2.tolist(), src=['pf33', n])
        if n in ('g_elder',): d['door'] = [6, 11]
        if n == 'g_tree6': d['door'] = [4, 7]
        if n == 'g_tree4': d['door'] = [2, 6]
        out['pf_' + n] = d
    out['_ship_moored'] = {'tiles': [[x, y, z, base + idmap[off_ship + i]] for x, y, z, i in ship]}
    out['_singles'] = {k: base + idmap[v] for k, v in SINGLES.items()}
    json.dump(out, open(os.path.join(HERE, 'data', 'stamps_rjc.json'), 'w'))
    print('custom tiles', len(ids), 'stamps', len(out))


if __name__ == '__main__':
    main()
