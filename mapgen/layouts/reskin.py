#!/usr/bin/env python3
"""reskin.py - re-skin a `wilds`-palette map onto the PF Rejuv sheet (MAPGEN 2h, step 4).  Keeps the map's size,
plan (glyph grid), heights, events, links and head; repaints everything with rkit (Sheridan ground, DirtDark lanes,
Sheridan 3-row cliffs from the height grid, log stairs, the Sheridan tree lattice, Sea(Grass) water, plank bridges).
The old spec's decoration lists (tileset 40 ids) are dropped and rebuilt by rkit's scatter / beds / yard trees.

    python3 -I layouts/reskin.py 520 521 524 525        then build.py with the same ids
Old specs are kept as layouts/old_<id>_wilds.yaml (the source of truth for the plan)."""
import os, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, yaml
import rkit as K
from rkit import C, STAMPS
HERE = K.HERE
SPECS = {520: '520_route1.yaml', 521: '521_route2.yaml', 524: '524_gossamer_wood.yaml', 525: '525_deepwood_cocoonfall.yaml'}
GLYPH = {'.': '.', ',': '.', 'g': 't', 'd': 'd', 'T': 'T', '~': 'w', '=': 'D', '#': '.', 'C': '.', 'S': 'd', 'a': '.', 'o': 'd'}
HOUSES = {'t_house_orange': 'gl_cot', 'h_long_g': 'gl_flat2'}
K.KITS['sh3'] = dict(K.KITS['sh'], rows=[K.KITS['sh']['rows'][0], K.KITS['sh']['rows'][1], K.KITS['sh']['rows'][3]])


def load(mid):
    fn = SPECS[mid]
    old = os.path.join(HERE, 'layouts', 'old_%d_wilds.yaml' % mid)
    if not os.path.exists(old): shutil.copyfile(os.path.join(HERE, 'specs', fn), old)
    docs = [d for d in yaml.safe_load_all(open(old)) if d]
    return docs, fn


def reskin(d, preview=None):
    mid = d['id']
    rows = d['map'].strip('\n').split('\n'); H, W = len(rows), max(len(r) for r in rows)
    m = K.RMap(W, H, 53, mid, water='Sea(Grass)', kit='sh3')
    m.auto = {'d': ('DirtDark', 'rejuvenation'), 'w': ('Sea(Grass)', 'rejuvenation')}
    hl = d['heights'].strip('\n').split('\n')
    for y in range(H):
        for x in range(W):
            ch = rows[y][x] if x < len(rows[y]) else '.'
            m.cls[y, x] = GLYPH.get(ch, '.')
            hc = hl[y][x] if y < len(hl) and x < len(hl[y]) else '0'
            m.ht[y, x] = int(hc) if hc.isdigit() else 0
    # stairs: each old log-stair stamp (3 wide, lip at its top row) becomes a rkit stairway
    for s in d.get('stamps', []):
        x, y = s['at']
        if s['stamp'].startswith('stairs'):
            m.stairs(x, y, w=3, kit_rows=3)
        elif s['stamp'] in HOUSES:                               # same door cell as before, so links and arrivals hold
            nm = HOUSES[s['stamp']]
            if 'door' in s and s.get('link'):
                m.front(nm, x + s['door'][0], y + s['door'][1], s['link'], s.get('name'))
            else:
                st = STAMPS[nm]; m.stamp(nm, x - (st['w'] - 4), y + 5 - st['h'] if st['h'] > 5 else y)
    for e in d.get('events', []):                             # events keep their cells: keep them walkable and free
        x, y = e['at']
        if m.inb(x, y): m.taken[y, x] = True
    for x, y in K.incoming(mid):                              # and so do the cells other maps' warps land on
        if m.inb(x, y): m.taken[y, x] = True; m.cls[y, x] = 'd' if m.cls[y, x] in 'T' else m.cls[y, x]
    # bridges / piers over water: plank deck tiles
    deck = np.argwhere(m.cls == 'D')
    for y, x in deck: m.over.append((1, x, y, C('sh', 497))); m.cls[y, x] = 'w'
    m.events = [e for e in m.events if e['type'] == 'door'] + list(d.get('events', []))
    for e in m.events:
        if e.get('type') == 'sign': e['post'] = False; m.tile(4847, e['at'][0], e['at'][1], 1)
    keep = np.zeros((H, W), bool)                              # events keep a free ring (trees may not wall them in)
    for x, y in [e['at'] for e in m.events] + K.incoming(mid):
        keep[max(0, y - 2):y + 3, max(0, x - 2):x + 3] = True
    m.taken |= keep
    import random
    rng = random.Random(mid)
    DENSE = mid in (520,)                                      # coastal heath: gorse, copses and sea rocks, not lawn
    for _ in range(W * H // (45 if DENSE else 90)):            # yard trees and copses in the open
        m.trees(rng.randrange(W), rng.randrange(H), rng.choice((1, 2, 3)), ['tr_oak', 'tr_oak2', 'tr_pine', 'tr_pine2'], r=3,
                seed=rng.randrange(999))
    if d.get('field') == 'SILKWOOD':                           # the Gossamer identity: webs and silk strands at the woods' edge
        for _ in range(W * H // 70):
            nm = rng.choice(['pf_p_web', 'pf_p_web1', 'pf_p_silk', 'pf_p_strand_w', 'pf_p_strand_p'])
            x, y = rng.randrange(W), rng.randrange(H); st = STAMPS[nm]
            if m.free(x, y, st['w'], st['h'], on='.'): m.stamp(nm, x, y, mark=None)
    m.greenfill(4, on='.')
    m.taken &= ~keep
    for x, y in [e['at'] for e in m.events] + K.incoming(mid):
        if m.inb(x, y): m.taken[y, x] = True
    m.paint()
    for y, x in deck: m.L[1, y, x] = C('sh', 497)
    m.scatter(30 if DENSE else 8, seed=mid)
    if DENSE: sea_rocks(m, mid)
    if preview: m.preview(preview, 0.5)
    h = {k: v for k, v in d.items() if k not in ('map', 'heights', 'stamps', 'tiles', 'tileblocks', 'events', 'palette')}
    h['_file'] = SPECS[mid] if len(load(mid)[0]) == 1 else '%d_reskin.yaml' % mid
    return m, h


def sea_rocks(m, seed):
    """Akuwa's offshore rocks (2x2) and single stones on the sea: the water stays open, the surface is not blank"""
    import random
    rng = random.Random(seed)
    small = [[[C('ak', 1644), C('ak', 1645)], [C('ak', 1652), C('ak', 1653)]], [[C('ak', 1646), C('ak', 1647)], [C('ak', 1654), C('ak', 1655)]]]
    water = m.cls == 'w'
    for _ in range(int(water.sum()) // 9):
        x, y = rng.randrange(m.W - 1), rng.randrange(m.H - 1)
        if water[y:y + 2, x:x + 2].all() and (m.L[2, y:y + 2, x:x + 2] == 0).all() and (m.L[1, y:y + 2, x:x + 2] == 0).all():
            r = rng.choice(small)
            for j in range(2):
                for i in range(2): m.L[2, y + j, x + i] = r[j][i]


def main():
    a = [int(x) for x in sys.argv[1:] if x.isdigit()]
    for mid in a:
        docs, fn = load(mid)
        out_docs = []
        for d in docs:
            if d['id'] != mid and d.get('palette') == 'wilds' and d['id'] in a:
                continue
            if d.get('palette') != 'wilds' or d['id'] not in a:
                out_docs.append(d); continue
            m, h = reskin(d, '/tmp/rj/rs%d.png' % d['id'] if '--preview' in sys.argv else None)
            h['_file'] = '%d_%s.yaml' % (d['id'], 'reskin')
            m.write(d['id'], h, '# %s (%d). RE-SKINNED BY layouts/reskin.py from layouts/old_%d_wilds.yaml - edit that plan.\n'
                    % (d['name'], d['id'], mid))
        rest = [x for x in out_docs if x['id'] != mid]
        dst = os.path.join(HERE, 'specs', fn)
        if rest:
            open(dst, 'w').write('# Remaining maps of the old %s (not re-skinned).\n' % fn + '\n---\n'.join(
                yaml.safe_dump(x, sort_keys=False, default_flow_style=None, width=150, allow_unicode=True) for x in rest))
        elif os.path.exists(dst):
            os.remove(dst)
        print('reskinned', mid)


if __name__ == '__main__':
    main()
