#!/usr/bin/env python3
"""Ferrow's Landing (100): a weathered ferry village at the edge of the realm, 68x60, palette `village`.
Three levels: the Tidewatch hill (lab, NW), the village bluff, the beach with the ferry pier; a lighthouse headland east.
Existing story events come from layouts/ferrow_events.yaml and are re-seated by name.
Run: python3 -I layouts/ferrow.py && python3 -I build.py 100"""
import os, sys, math, yaml
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from villagekit import Village, STAMPS, WS, GARDEN, HERE, vnoise
W, H = 68, 60
SRC = yaml.safe_load(open(os.path.join(HERE, 'layouts', 'ferrow_events.yaml')))[100]
ANCHORS = {}


def ev(key, at, item=None):
    for e in SRC['events']:
        if e.get('name') == key or str(e.get('text', '')).startswith(key) or (item and e.get('item') == item):
            return dict(e)
    raise KeyError(key)


def build():
    c = Village(W, H, 100)
    def shore(x): return 47 + int(round(1.5 * math.sin(x / 7.0) + 1.5 * (vnoise(x, 0, 3, 5.0) - 0.5)))
    def bluff(x): return 40 + int(round(1.2 * math.sin(x / 9.0 + 1) + 1.4 * (vnoise(x, 0, 4, 6.0) - 0.5)))
    c.hills([(15, 11, 17, 9, 2, 1)], base=1)
    for y in range(H):
        for x in range(W):
            head = ((x - 57) / 9.0) ** 2 + ((y - 38) / 15.0) ** 2 <= 1.0 + 0.3 * (vnoise(x, y, 5, 4.0) - 0.5)
            if y >= bluff(x) and not head: c.ht[y][x] = 0
            if y >= shore(x) and not head: c.ht[y][x] = -1
            if head and c.ht[y][x] < 1: c.ht[y][x] = 1
            if y < 22 and 7 <= x <= 24: c.ht[y][x] = 2
    c.notch(14, 18, 22, 2); c.notch(32, 36, 40, 1); c.notch(10, 12, 40, 1)
    for y in range(H):
        for x in range(W):
            if c.ht[y][x] < 0: c.g[y][x] = '~'
            elif c.ht[y][x] == 0: c.g[y][x] = 's'
    # ---- paths: the Route 1 lane, the green, the pier road
    c.path([(34.5, 0), (34.5, 10), (32, 20), (33, 28)], 3, 'd', 1, only='.')
    c.blob(32, 30, 8, 4.5, 'd', 2, only='.', rough=0.9); c.blob(32, 30, 3.5, 2, 'c', 3, only='d')
    c.path([(34, 33), (34.5, 39)], 3, 'd', 4, only='.')
    c.rect(11, 17, 11, 5, 'c', '.'); c.path([(16.5, 26), (22, 28), (27, 29)], 2, 'd', 5, only='.')
    c.path([(8, 30), (16, 31), (26, 31)], 2, 'd', 6, only='.'); c.path([(11.5, 31), (11.5, 39)], 2, 'd', 7, only='.')
    c.path([(38, 30), (46, 29), (52, 27)], 2, 'd', 8, only='.'); c.path([(46, 29), (47, 36), (52, 38)], 2, 'o', 9, only='.')
    c.path([(40, 22), (48, 20), (56, 21)], 2, 'd', 10, only='.'); c.path([(36, 20), (40, 22)], 2, 'd', 11, only='.')
    c.path([(6, 36), (16, 37), (30, 37)], 2, 'o', 12, only='.')
    # ---- pier and berth
    py = shore(34) - 1
    c.rect(33, py, 3, 58 - py, '=', '~s'); c.rect(12, shore(12) - 2, 2, 9, '=', '~s'); c.rect(22, shore(22) - 2, 2, 6, '=', '~s')
    c.stairs(15, 22); c.stairs(33, 40); c.stairs(10, 40)
    c.cliffs(face=2, keep='~=')
    for y in range(H):
        for x in range(W):
            if c.g[y][x] == 'C' and c.ht[y][x] < 0: c.g[y][x] = '~'; c.taken[y][x] = False
    # ---- named buildings
    d = {}
    d['lab'] = c.stamp('h_dome', 12, 8, 'FL_LAB', 'Lab door', force=True)
    d['pc'] = c.stamp('t_pokecenter', 22, 23, 'FL_PC', 'Poke Center door', force=True)
    d['mart'] = c.stamp('t_mart', 40, 24, 'FL_MART', 'Mart door', force=True)
    d['inn'] = c.stamp('w_ell_a', 2, 19, 'FL_INN', 'Inn door', force=True)
    d['customs'] = c.stamp('w_longhouse_s', 17, 30, 'FL_CUSTOMS', 'Customs door', force=True)
    d['dock'] = c.stamp('w_house_m', 40, 31, 'FL_DOCK', 'Dockmaster door', force=True)
    c.stamp('t_lighthouse', 55, 16, force=True)
    d['light'] = c.stamp('w_house', 48, 31, 'FL_LIGHT', 'Lighthouse door', force=True)
    c.stamp('t_stall', 37, 13, force=True)                      # Hales' bramble stall on the lane
    c.stamp('t_ship', 36, 50, force=True)                       # the Dovetail at her berth
    for k, dd in d.items():
        for dy in (1, 2):
            if c.g[dd[1] + dy][dd[0]] in '.,': c.g[dd[1] + dy][dd[0]] = 'd'
    # ---- events (existing, re-seated) and reserved anchors
    px = 34
    E = [dict(ev("FERROW'S", 0), at=c.snap(32, 4, 'd')), dict(ev('Accord plaque', 0), at=c.snap(30, 29, 'cd')),
         dict(ev('Customs scan', 0), at=[33, py]), dict(ev('Customs scan 2', 0), at=[34, py]), dict(ev('Customs scan 3', 0), at=[35, py]),
         dict(ev('Calla Wren', 0), at=[32, py - 1]), dict(ev('Captain Edda', 0), at=[35, 56]), dict(ev('Fisherman', 0), at=[33, 51]),
         dict(ev('Coll Hale', 0), at=[38, 19]), dict(ev('Wenna Hale', 0), at=[40, 19]),
         dict(ev('Skipping children', 0), at=c.snap(28, 31, 'd')), dict(ev('Kestrel K1', 0), at=[16, 27]),
         dict(ev('~none~', 0, item='POTION'), at=[5, 34]), dict(ev('~none~', 0, item='POKEBALL'), at=c.snap(53, 39, 'o'))]
    import scriptpour as SP
    npcs, signs, items = SP.parse(SP.section(r'^### Flavor townsfolk \(each', r'^### Sidequest A — "Captain Edda'))
    crier = [n for n in SP.parse(SP.section(r'^### Named residents', r'^### Flavor townsfolk \(each'))[0] if n['name'] == 'Crier']
    E = [e for e in E if e.get('name') != 'Skipping children']          # superseded by the script's rope-skipping girls
    E[0]['text'] = signs[0]['text']
    for e in E: c.taken[e['at'][1]][e['at'][0]] = True
    A = [(28, 31), (36, 30), (33, 22), (45, 29), (20, 31), (34, 37), (12, 33), (48, 21), (36, 12), (26, 43), (40, 43), (16, 44),
         (33, 48), (10, 44), (30, 26), (50, 38)]
    E += c.people(crier + npcs, A, 'dcos=')
    E += c.signs(signs[1:], [(30, 27), (36, 24), (41, 16), (22, 44)], '.s')
    for it, (ax, ay) in zip(items, [(39, 11), (34, 57)]):
        E.append({'type': 'item', 'item': it['item'], 'hidden': True, 'at': c.snap(ax, ay, '.=', r=6)})
    for x in (38, 39, 40): c.g[19][x] = ','; c.g[20][x] = 'd'
    # ---- houses along the lanes, then yards
    c.frontage(WS, (2, 14, 52, 39), 'do', 1); c.backfill([n for n in WS if 'cot' in n or 'house' in n], (26, 2, 52, 39), 0.5, 2)
    # ---- dressing: harbour clutter, gardens, lanterns, laundry
    c.dress(['hs_jonquil_26', 'hs_jonquil_29', 'hs_jonquil_31', 'hs_jonquil_33'], 8, 's', 1, (2, 41, 52, 47), pad=1)
    c.dress(['p_net', 'p_net', 'p_crates', 't_barrel', 't_barrel2', 'hs_jonquil_36', 'hs_jonquil_35', 'tp_stall_13', 't_crate_pair', 'p_stump', 'hs_jonquil_19', 'p_laundry'], 26, 's', 2, (2, 40, 52, 47))
    c.dress(['p_laundry', 'tp_stall_08', 'p_laundry'], 7, '.', 4, near='#')
    c.dress(GARDEN + ['tp_stall_01', 'p_crates', 't_barrel', 'tp_stall_16'], 44, '.', 5, near='#', pad=0)
    c.dress(['p_lantern'], 16, '.', 6, near='dco')
    c.dress(['p_cherry', 'p_rocks', 'p_bush_w', 'p_pinkbush'], 14, '.', 7)
    c.dress(['p_sign'], 3, '.', 8, near='d', pad=0); c.dress(['t_bench'], 4, 'c', 9, pad=0)
    c.fence_run([(26, 2), (26, 9)]); c.fence_run([(43, 2), (43, 12)]); c.fence_run([(44, 12), (50, 12)])
    c.fence_run([(3, 33), (9, 33)]); c.fence_run([(44, 33), (44, 38)])
    c.borders(p=0.7); c.meadow(0.76, 1)
    c.greenfill(0.36, 1, beds=0.04)
    c.sea_rocks(26, avoid=[(26, 44, 52, 59)])
    c.events = E
    head = dict(SRC['head']); head.update({'palette': 'village', 'rubric': True, 'yards_ok': True, 'tone': [6, 2, -10, 0],
                'connections': [{'dir': 'N', 'offset': 28, 'to': 520, 'to_offset': 10}]})
    head['metadata'] = dict(head['metadata'], Weather=['Rain', 0])
    del head['metadata']['Weather']
    c.write('100_ferrows_landing.yaml', head, "# Ferrow's Landing (100). WRITTEN BY layouts/ferrow.py - edit that script.\n")
    print('doors', d, 'pier top', py)
    return d


if __name__ == '__main__':
    build()
