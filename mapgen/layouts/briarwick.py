#!/usr/bin/env python3
"""Briarwick (120): the weavers' village among giant trees and silk, 72x64, palette `village`.
Giant tree-houses (custom boles and crowns), rope bridges between crowns, a dye works on the stream, looms, silk awnings,
lanterns with light pools; the Loomhouse (Gym 1) is the largest tree, on a knoll. Old-growth forest is the border (forest biome).
Run: python3 -I layouts/briarwick.py && python3 -I build.py 120"""
import os, sys, math, yaml
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from villagekit import Village, STAMPS, GARDEN, HERE, C2, vnoise
W, H = 72, 64
SRC = yaml.safe_load(open(os.path.join(HERE, 'layouts', 'briarwick_events.yaml')))[120]


def ev(key):
    for e in SRC['events']:
        if e.get('name') == key or str(e.get('text', '')).startswith(key): return dict(e)
    raise KeyError(key)


def rope(c, x0, x1, y):
    for x in range(min(x0, x1), max(x0, x1) + 1): c.tile(C2 + 115, x, y, 2)


def build():
    c = Village(W, H, 120)
    c.hills([(36, 13, 13, 7, 1, 2)], base=0)
    def sx(y): return 11 + int(round(2.2 * math.sin(y / 7.0) + 2.0 * (vnoise(0, y, 6, 6.0) - 0.5)))
    for y in range(H):
        for x in range(W):
            if 28 <= x <= 44 and y < 18 and y > 5: c.ht[y][x] = 1
            if 0 <= x - sx(y) <= 2 or ((x - 17) / 5.0) ** 2 + ((y - 46) / 3.5) ** 2 < 1.0 + 0.4 * (vnoise(x, y, 7, 3.0) - 0.5):
                c.ht[y][x] = -1; c.g[y][x] = '~'
    c.notch(34, 38, 19, 1)
    # ---- old-growth border (forest biome), ragged inner edge
    for y in range(H):
        for x in range(W):
            edge = min(x, W - 1 - x, y, H - 1 - y)
            if edge < 5 + 3.5 * vnoise(x, y, 11, 6.0) and c.g[y][x] == '.': c.g[y][x] = 'T'
    # ---- paths
    c.rect(0, 30, 8, 2, 'd', '.T'); c.path([(7, 30.5), (20, 31), (30, 32)], 2, 'd', 1, only='.T~')
    c.blob(36, 33, 8, 4.5, 'd', 2, only='.', rough=0.9); c.blob(36, 33, 3, 1.8, 'c', 3, only='d')
    c.path([(36.5, 21), (36.5, 29)], 3, 'd', 4, only='.'); c.rect(32, 16, 9, 3, 'c', '.')
    c.path([(36, 37), (35.5, 50), (35.5, 63)], 2, 'd', 5, only='.T')
    c.path([(43, 33), (54, 32), (64, 34)], 2, 'd', 6, only='.T'); c.path([(54, 32), (55, 22), (50, 16)], 2, 'o', 7, only='.')
    c.path([(22, 31), (22, 22), (26, 17)], 2, 'o', 8, only='.'); c.path([(22, 32), (24, 42), (30, 48), (35, 50)], 2, 'o', 9, only='.')
    c.path([(36, 50), (48, 49), (56, 44), (54, 33)], 2, 'o', 10, only='.'); c.path([(14, 31), (15, 38), (20, 41)], 2, 'o', 11, only='.')
    for y in (30, 31):
        for x in range(8, 18):
            if c.g[y][x] == '~': c.g[y][x] = 'c'; c.ht[y][x] = 0            # stone ford on the Route 3 road
    c.stairs(35, 19)
    c.cliffs(face=2, keep='~')
    for y in range(H):
        for x in range(W):
            if c.g[y][x] == 'C' and c.ht[y][x] < 0: c.g[y][x] = '~'; c.taken[y][x] = False
    # ---- the giant trees
    d = {}
    d['gym'] = c.stamp('g_tree6', 32, 8, 'BW_GYM', 'Gym door', force=True)
    c.stamp('g_tree4p', 26, 9, force=True); c.stamp('g_tree4p', 40, 9, force=True)
    d['guild'] = c.stamp('g_tree6', 15, 19, 'BW_GUILD', 'Guildhall door', force=True)
    d['house1'] = c.stamp('g_tree4', 52, 23, 'BW_HOUSE1', 'Treetop House door', force=True)
    d['house2'] = c.stamp('g_tree4', 44, 40, 'BW_HOUSE2', "Cutter's House door", force=True)
    d['pc'] = c.stamp('t_pokecenter', 26, 24, 'BW_PC', 'Poke Center door', force=True)
    d['mart'] = c.stamp('t_mart', 45, 26, 'BW_MART', 'Mart door', force=True)
    for nm, x, y in (('g_tree4', 24, 37), ('g_tree4', 58, 36), ('g_tree4', 25, 50), ('g_tree6', 46, 51), ('g_tree4', 60, 14),
                     ('g_tree4p', 3, 22), ('g_tree4p', 62, 46), ('g_tree2', 46, 14), ('g_tree2', 20, 12), ('g_tree2', 40, 44),
                     ('g_tree2', 30, 40), ('g_tree2', 58, 26), ('g_tree2', 22, 56), ('g_tree2', 66, 28), ('g_tree2', 5, 38),
                     ('g_tree2', 52, 6), ('g_tree2', 14, 8), ('g_tree2', 64, 56), ('g_tree2', 4, 12), ('g_tree2', 38, 56)):
        c.stamp(nm, x, y, force=True)
    for k, dd in d.items():
        for dy in (1, 2):
            if c.g[dd[1] + dy][dd[0]] in '.,': c.g[dd[1] + dy][dd[0]] = 'd' if k not in ('gym',) else 'c'
    # rope bridges between crowns (overhead), silk awnings over doors
    rope(c, 32, 31, 11); rope(c, 40, 39, 11); rope(c, 23, 25, 21); rope(c, 46, 51, 25); rope(c, 50, 57, 38); rope(c, 34, 39, 46)
    rope(c, 54, 57, 53); rope(c, 21, 23, 39)
    for k in ('gym', 'guild', 'house1', 'house2'):
        c.stamp('p_awning', d[k][0] - 1, d[k][1] - 2, force=True)
    # ---- events re-seated
    gx, gy = d['gym']
    E = [dict(ev('To Gossamer Wood'), at=[35, 63], arrive=[35, 62, 'up']), dict(ev('Gym sign'), at=[gx + 2, gy + 2]),
         dict(ev('BRIARWICK') if any(str(e.get('text', '')).startswith('BRIARWICK') for e in SRC['events']) else SRC['events'][2], at=c.snap(20, 32, 'd')),
         dict(ev('Loyal Three shrine'), at=[38, 31]), dict(ev('Festival poster'), at=[33, 30]), dict(ev('Masked child'), at=c.snap(34, 35, 'd')),
         dict(ev('Pallbearer Thistle'), at=[63, 33]), dict(ev('Lattice pylon'), at=[65, 32]), dict(ev('Old woman at the shrine'), at=[39, 32]),
         dict(ev('Gym guide'), at=[34, 17]), dict(ev('Meridian liaison'), at=c.snap(50, 33, 'd')), dict(ev('Dyer'), at=[17, 36])]
    E.append({'type': 'warp', 'name': 'To Gossamer Wood b', 'at': [36, 63], 'to': None})
    E[-1] = dict(E[0], at=[36, 63], name='To Gossamer Wood b'); E[-1].pop('link', None); E[-1].pop('arrive', None)
    E[-1]['to'] = {'map': 524, 'x': 24, 'y': 1, 'dir': 'down'}
    import scriptpour as SP
    npcs, signs, items = SP.parse(SP.section(r'^### Flavor townsfolk$', r'^### EV "Old woman at the shrine'))
    named = [n for n in SP.parse(SP.section(r'^## Map 120 — Briarwick', r'^### Flavor townsfolk$'))[0] if n['name'] in ('Finch',)]
    E = [e for e in E if e.get('name') not in ('Dyer', 'Masked child')]     # superseded by the script's Dyer / masked children
    sg = {s['name']: s['text'] for s in signs}
    E[2]['text'] = sg['Town Sign']; E[1]['text'] = sg['Loomhouse Sign']
    for e in E:
        if e.get('name') == 'Festival poster': e['text'] = sg['Festival Poster']
        if e.get('name') == 'Lattice pylon': e['text'] = sg['Pylon']
    for e in E: c.taken[e['at'][1]][e['at'][0]] = True
    A = [(22, 30), (17, 36), (20, 28), (40, 46), (30, 33), (48, 32), (60, 33), (36, 26), (44, 47), (34, 35), (36, 44), (28, 46),
         (39, 30), (34, 20), (56, 40), (50, 44), (24, 22)]
    E += c.people(named + npcs, A, 'dco')
    E += c.signs([s for s in signs if s['name'] in ('Survey Flags', 'Silk Racks')], [(61, 30), (22, 26)], '.')
    for it, (ax, ay) in zip(items, [(36, 47), (15, 40)]):
        E.append({'type': 'item', 'item': it['item'], 'hidden': True, 'at': c.snap(ax, ay, '.', r=6)})
    # ---- dye works on the stream, looms by the guild, silk everywhere
    c.dress(['p_vat_b', 'p_vat_r', 'p_vat_y'], 9, '.', 1, (13, 32, 22, 42), pad=0)
    c.dress(['tp_stall_05', 'tp_stall_06', 'tp_stall_20', 'tp_stall_21', 'p_laundry', 'tp_stall_08'], 8, '.', 2, (12, 18, 30, 44))
    c.dress(['p_loom', 'p_loom', 'tp_garden_09'], 6, '.', 3, (13, 26, 34, 34), pad=0)
    c.dress(['p_silk', 'p_silk1', 'p_strand_w', 'p_strand_p', 'p_silk1'], 30, '.', 4, pad=0)
    c.dress(['p_web', 'p_web1'], 14, '.T', 5, pad=0)
    c.dress(['p_lantern'], 30, '.', 6, near='dco')
    c.dress(GARDEN + ['p_crates', 'tp_stall_13', 't_barrel', 'tp_stall_01'], 30, '.', 7, pad=0)
    c.dress(['p_cherry', 'p_pinkbush', 'p_pinkbush2', 'p_rocks'], 12, '.', 8)
    c.dress(['t_bench'], 3, 'c', 9, pad=0); c.dress(['p_banner3', 'p_banner'], 6, '.', 10, near='d', pad=0)
    c.meadow(0.74, 1)
    c.greenfill(0.42, 1, beds=0.05)
    c.sea_rocks(4)
    c.events = E
    head = dict(SRC['head']); head.update({'palette': 'village', 'rubric': True, 'yards_ok': True, 'tone': [-8, 8, -18, 0],
                'connections': [{'dir': 'W', 'offset': 29, 'to': 540, 'to_offset': 10}]})
    c.write('120_briarwick.yaml', head, '# Briarwick (120). WRITTEN BY layouts/briarwick.py - edit that script.\n', mirror_max=0.6)
    print('doors', d)
    return d


if __name__ == '__main__':
    build()
