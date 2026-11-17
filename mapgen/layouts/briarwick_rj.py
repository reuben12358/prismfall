#!/usr/bin/env python3
"""Briarwick (120) on the PF Rejuv sheet (tileset 50 "PF Rejuv Village"), 72x64.  MAPGEN 2h.
A Sheridan-style forest village: old-growth lattice forest on every side, a stream down the west with the Route 3 road
crossing it on a raised plank walkway (rows 30-31), the north ridge (h=1) under Sheridan cliffs with the elder tree
Loomhouse on its knoll and the Loyal Three shrine at its west end, giant hollow trees (Prismfall's own art, re-graded
to Sheridan greens) as the Guildhall, Treetop House and Cutter's House, Sheridan timber houses for the Help Center,
the Mart and the chapel, the weavers' deck, lantern decks to the south-east, silk garlands over the green.
Story events come from layouts/story_early.py; this script seats them.
Run: python3 -I layouts/briarwick_rj.py && python3 -I build.py 120"""
import os, sys, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import rkit as K
from rkit import C, STAMPS
from terrain import vnoise
import story_early as SE
W, H = 72, 64
DECK = {k: C('sh', v) for k, v in dict(TL=488, T=489, TR=490, L=496, C=497, R=498, BL=504, B=505, BR=506,
                                        legL=523, leg=524, legR=525).items()}
TREES = ['tr_oak', 'tr_oak2', 'tr_pine', 'tr_pine2', 'tr_oak2']
GARL = None


def sx(y):
    return 8 + int(round(2.2 * math.sin(y / 7.0) + 1.6 * (vnoise(0, y, 6, 6.0) - 0.5)))


def ridge(x):
    """last row of the north ridge (h=1)"""
    if 28 <= x <= 44: return 14
    if 18 <= x <= 27: return 12 + (1 if x > 22 else 0)
    return 10 + int(round(1.5 * math.sin(x / 5.0) + 1.5 * (vnoise(x, 0, 3, 6.0) - 0.5)))


def deck(m, x0, y0, w, h, stairs=None):
    """Sheridan raised timber deck: 9-slice top, stilts below, plank stairs down the front at stairs=x"""
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            k = ('T' if y == y0 else 'B' if y == y0 + h - 1 else '') + ('L' if x == x0 else 'R' if x == x0 + w - 1 else '')
            k = {'': 'C', 'T': 'T', 'B': 'B', 'L': 'L', 'R': 'R'}.get(k, k)
            m.tile(DECK[k], x, y, 1); m.cls[y, x] = 'D'
    for x in range(x0, x0 + w):
        if stairs is not None and x in (stairs, stairs + 1): continue
        m.tile(DECK['legL' if x == x0 else 'legR' if x == x0 + w - 1 else 'leg'], x, y0 + h, 1); m.cls[y0 + h, x] = 'B'
    if stairs is not None:
        for i, x in enumerate((stairs, stairs + 1)):
            m.tile(K.RMap.STAIRS[0 if i == 0 else 2], x, y0 + h, 2); m.cls[y0 + h, x] = 'd'


def walkway(m, x0, x1, y):
    """2-wide plank walkway (rows y, y+1) between x0..x1, open at both ends, stilts below where not water"""
    for x in range(x0, x1 + 1):
        m.tile(DECK['T'], x, y, 1); m.tile(DECK['B'], x, y + 1, 1); m.cls[y, x] = m.cls[y + 1, x] = 'D'
        m.taken[y, x] = m.taken[y + 1, x] = True


def build(preview=None):
    m = K.RMap(W, H, 50, 120, water='Sea(Grass)', kit='sh')
    # ---------------------------------------------------------------- terrain
    for x in range(W):
        for y in range(H):
            if y <= ridge(x): m.ht[y, x] = 1
    for y in range(H):
        s = sx(y)
        for x in range(s, s + 3): m.cls[y, x] = 'w'
    m.blob(16, 49, 5.5, 3.2, 'w', seed=7, rough=0.5)
    m.blob(13, 46, 2.5, 2.0, 'w', seed=8, rough=0.4)
    for y in range(H):
        for x in range(W):
            if m.cls[y, x] == 'w': m.ht[y, x] = 0
    # old-growth border, ragged inner edge; the ridge is forest except the knoll and the shrine
    for y in range(H):
        for x in range(W):
            if m.cls[y, x] != '.': continue
            edge = min(x, W - 1 - x, y, H - 1 - y)
            deep = edge < 4 + 4 * vnoise(x, y, 11, 6.0)
            knoll = ((x - 36) / 9.0) ** 2 + ((y - 11) / 5.5) ** 2 < 1.0 + 0.5 * (vnoise(x, y, 4, 3.0) - 0.5)
            shrine = ((x - 22) / 5.5) ** 2 + ((y - 9) / 4.5) ** 2 < 1.0 + 0.5 * (vnoise(x, y, 5, 3.0) - 0.5)
            ridge_forest = m.ht[y, x] == 1 and not knoll and not shrine
            if deep or ridge_forest: m.cls[y, x] = 'T'
    # ---------------------------------------------------------------- lanes (Sheridan dirt, orthogonal with soft bends)
    m.street([(35, 63), (35, 52), (40, 52), (40, 38)], 3, 'd', only='.T')       # from Gossamer Wood up to the green
    m.rect(34, 29, 15, 9, 'd', '.')                                              # the green (Tamsin's square)
    m.street([(0, 31), (34, 31)], 2, 'd', only='.T')                             # Route 3 road (rows 30-31) from the west edge
    m.street([(48, 31), (71, 31)], 3, 'd', only='.T')                            # east lane to the pylon
    m.street([(36, 19), (36, 29)], 3, 'd', only='.')                             # stairs down from the Loomhouse
    m.street([(22, 14), (22, 19), (36, 19)], 2, 'd', only='.T')                  # shrine stairs path
    m.street([(17, 27), (17, 30)], 2, 'd', only='.')
    m.street([(45, 25), (45, 29)], 2, 'd', only='.')
    m.street([(56, 25), (56, 30)], 2, 'd', only='.')
    m.street([(27, 41), (27, 37), (34, 37)], 2, 'd', only='.')
    m.street([(63, 43), (63, 46), (51, 46)], 2, 'd', only='.')
    m.street([(42, 51), (42, 52)], 2, 'd', only='.')
    m.street([(48, 37), (55, 46), (55, 49)], 2, 'd', only='.')
    m.stairs(35, 14, w=3, kit_rows=4)
    m.stairs(21, 13, w=2, kit_rows=4)
    # ---------------------------------------------------------------- buildings
    E = []
    P = lambda n, at, **kw: E.append(SE.place(120, n, at, **kw))
    d = {}
    d['gym'] = m.stamp('pf_g_elder', 30, 1, 'BW_GYM', 'Gym door')
    d['guild'] = m.stamp('pf_g_tree6', 13, 19, 'BW_GUILD', 'Guildhall door')
    d['pc'] = m.stamp('sh_help', 42, 18, 'BW_PC', 'Poke Center door')
    d['house1'] = m.stamp('pf_g_tree4', 53, 18, 'BW_HOUSE1', 'Treetop House door')
    d['mart'] = m.stamp('sh_cot', 24, 34, 'BW_MART', 'Mart door')
    d['chapel'] = m.stamp('sh_big', 55, 34, 'BW_CHAPEL', 'Chapel door')
    d['house2'] = m.stamp('pf_g_tree4', 40, 44, 'BW_HOUSE2', "Cutter's House door")
    for nm, x, y in (('pf_g_tree4p', 22, 44), ('pf_g_tree2', 47, 9), ('pf_g_tree2', 61, 20), ('pf_g_tree4p', 61, 39),
                     ('pf_g_tree2', 29, 48), ('pf_g_tree2', 48, 45), ('sh_small', 64, 24), ('sh_small', 49, 36)):
        if m.free(x, y, STAMPS[nm]['w'], STAMPS[nm]['h'], on='.dT'): m.stamp(nm, x, y)
        else: print('  (no room for %s at %d,%d)' % (nm, x, y))
    for k, (dx, dy) in d.items():
        for yy in (dy + 1, dy + 2):
            if m.inb(dx, yy) and m.cls[yy, dx] in '.tT' and m.ht[yy, dx] == m.ht[dy, dx]: m.cls[yy, dx] = 'd'
    deck(m, 22, 23, 7, 4, stairs=24)                         # the weavers' deck beside the Guildhall tree
    deck(m, 51, 52, 5, 3, stairs=52)                         # lantern decks, south-east
    deck(m, 59, 52, 5, 3, stairs=61)
    walkway(m, 56, 58, 52)
    walkway(m, sx(30) - 2, sx(31) + 4, 30)                   # the Route 3 road over the stream
    # ---------------------------------------------------------------- events
    P('To Gossamer Wood', (35, 63)); P('To Gossamer Wood b', (36, 63))
    P('Arrival', (34, 62)); P('Juno (arrival)', (36, 61)); P('Stage manager', (37, 62))
    gx, gy = d['gym']
    P('Loomhouse sign', (gx + 2, gy + 1))
    P('Loyal Three shrine', (21, 8)); P('Old woman at the shrine', (22, 9)); P('Dusk petal', (23, 8))
    P('Lattice pylon', (69, 30)); P('Survey flags', (67, 33))
    for i, y in enumerate((30, 31, 32)): P('Pylon watch %d' % (i + 1), (63, y))
    P('Pallbearer Thistle', (66, 31)); P('Bereaved 1', (65, 30)); P('Bereaved 2', (66, 32))
    P('Tamsin (square)', (41, 34)); P('Festival poster', (38, 30)); P('Charcoal child', (38, 35))
    P('Weaver at loom', (26, 25)); P('Silk racks', (23, 24)); P('HiddenItem rope bridge', (28, 21))
    P('HiddenItem dye vats', (14, 38))
    for e in E: m.taken[e['at'][1], e['at'][0]] = True
    def S(n, ax, ay, on='.d', r=8):
        e = SE.place(120, n, m.snap(ax, ay, on, r=r)); E.append(e); m.taken[e['at'][1], e['at'][0]] = True
    S('Town sign', 37, 57); S('Finch', 60, 35); S('Rope-bridge Boy', 30, 31); S('Grandmother knitting', 46, 36)
    town = [('Dyer', 16, 36), ('Apprentice', 21, 31), ('Silk Merchant', 36, 36), ('Meridian Linesman', 52, 31), ('Tired Mother', 33, 48),
            ('Old Man on bridge', 9, 31), ('Girl in ogre mask', 43, 32), ('Boy in dog mask', 44, 33), ('Egg-seller', 47, 33),
            ('Tax-barge Deserter', 33, 55), ('Accord Chaplain', 59, 42), ('Youngster', 50, 29), ('Woman with basket', 46, 40),
            ("Cutter's Wife", 44, 52)]
    for n, x, y in town: S(n, x, y)
    for e in E:
        if e.get('type') == 'sign':
            e['post'] = False; x, y = e['at']
            if e['name'] in ('Town sign', 'Loomhouse sign'): m.tile(4833, x, y - 1, 2); m.tile(4841, x, y, 1)
            elif e['name'] != 'Silk racks': m.tile(4847, x, y, 1)
    missing = SE.unplaced(120)
    if missing: raise SystemExit('briarwick: script events not placed: %s' % missing)
    m.events += E
    # ---------------------------------------------------------------- dressing
    for nm, x, y in (('pf_p_loom', 23, 24), ('pf_p_loom', 27, 24), ('pf_p_laundry', 23, 23), ('pf_p_vat_b', 13, 36),
                     ('pf_p_vat_r', 15, 37), ('pf_p_vat_y', 13, 39), ('sh_crates', 51, 52), ('sh_crates', 62, 52),
                     ('pf_logbench', 59, 53), ('sh_campfire', 42, 36), ('sh_crates', 49, 36), ('pf_p_silk', 54, 52), ('pf_p_silk', 60, 52)):
        st = STAMPS[nm]
        if m.free(x, y, st['w'], st['h'], on='.dD') or all(m.cls[y + j, x + i] == 'D' for i in range(st['w']) for j in range(st['h'])):
            m.over += [(z, x + i, y + j, t) for z in (1, 2) for j in range(st['h']) for i in range(st['w']) for t in [st['layers'][z][j][i]] if t]
            m.taken[y:y + st['h'], x:x + st['w']] = True
        else: m.near(nm, x, y, on='.d', r=2)
    for y in range(0, 3):                                     # above the elder's crown: wild grass, not lawn
        for x in range(26, 47):
            if m.cls[y, x] == '.' and not m.taken[y, x]: m.cls[y, x] = 't'
    rng = random.Random(3)                                    # wild grass along the forest edge and the stream banks
    for y in range(H):
        for x in range(W):
            if m.cls[y, x] == '.' and not m.taken[y, x] and m.ht[y, x] == 0:
                near_edge = any(m.inb(x + dx, y + dy) and m.cls[y + dy, x + dx] in 'Tw' for dx in (-2, -1, 0, 1, 2) for dy in (-2, -1, 0, 1, 2))
                if near_edge and vnoise(x, y, 17, 4.0) > 0.6: m.cls[y, x] = 't'
    for cx, cy, n in ((20, 35, 2), (30, 42, 2), (48, 26, 1), (60, 46, 2), (52, 40, 2), (30, 54, 2), (44, 58, 2), (27, 17, 1),
                      (50, 15, 2), (62, 15, 2), (14, 43, 1), (66, 46, 1), (52, 58, 2), (24, 58, 2), (18, 28, 1)):
        m.trees(cx, cy, n, TREES, r=3, seed=cx + cy * 5)
    for x, y in ((33, 21), (39, 27), (33, 39), (48, 34), (38, 48), (59, 32), (27, 32), (18, 30)):
        if m.free(x, y - 1, 1, 2, on='.'): m.stamp('pf_lantern', x, y - 1)
    m.beds(prefixes=('sh_',))
    # ---------------------------------------------------------------- paint
    m.paint()
    garlands(m, ((33, 47, 29, 0), (35, 41, 47, 1), (41, 48, 25, 2), (18, 28, 29, 3), (50, 62, 36, 1), (33, 40, 57, 2)))
    m.scatter(7, seed=21)
    if preview: m.preview(preview, 0.5)
    head = {'id': 120, 'biome': 'forest', 'name': 'Briarwick', 'parent': 0, 'bgm': 'Lappet Town', 'rubric': True, 'yards_ok': True,
            'metadata': {'Outdoor': True, 'ShowArea': True, 'MapPosition': [0, 12, 22], 'BattleBack': 'forest'},
            'tone': [-10, -22, 2, 4], 'fog': {'name': 'prismfall_spores', 'opacity': 46, 'blend': 1, 'zoom': 100, 'sx': 1, 'sy': -1},
            'connections': [{'dir': 'W', 'offset': 29, 'to': 540, 'to_offset': 10}], '_file': '120_briarwick.yaml'}
    import yaml
    src = yaml.safe_load(open(os.path.join(K.HERE, 'layouts', 'briarwick_events.yaml')))[120]['head']
    for k in ('bgm', 'metadata', 'field', 'display_name'):
        if k in src: head[k] = src[k]
    m.write(120, head, '# Briarwick (120). WRITTEN BY layouts/briarwick_rj.py (PF Rejuv) - edit that script.\n')
    print('doors', d)
    return m


def garlands(m, runs):
    """silk garlands strung overhead (layer 3) across lanes; a lantern every fifth span"""
    g = [K.SINGLE['garl_plain'], K.SINGLE['garl_pennant'], K.SINGLE['garl_lantern'], K.SINGLE['garl_tufts']]
    for x0, x1, y, sd in runs:
        for i, x in enumerate(range(x0, x1 + 1)):
            if m.inb(x, y) and m.L[2, y, x] == 0: m.L[2, y, x] = g[(i + sd) % 4 if (i + sd) % 5 else 2]


if __name__ == '__main__':
    build(sys.argv[1] if len(sys.argv) > 1 else None)
