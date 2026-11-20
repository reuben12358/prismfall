#!/usr/bin/env python3
"""Briarwick (120) on the PF Rejuv sheet (tileset 50 "PF Rejuv Village"), 72x64.  MAPGEN 2h.
A Sheridan-style forest village: old-growth lattice forest on every side, a stream down the west with the Thistledown Lea road
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
PALE = 3402                                # Goldenleaf pale deck plank (gl part: composite id = source id)


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
            m.tile(PALE, x, y, 1); m.cls[y, x] = 'D'               # Goldenleaf's pale porch planks: lighter than Sheridan's
    if all(m.inb(x, y0 - 1) and m.cls[y0 - 1, x] in '.t' and not m.taken[y0 - 1, x] for x in range(x0, x0 + w)):
        m.fence(x0, x0 + w - 1, y0 - 1)                              # a back rail
    for x in range(x0, x0 + w):
        if stairs is not None and x in (stairs, stairs + 1): continue
        m.tile(DECK['legL' if x == x0 else 'legR' if x == x0 + w - 1 else 'leg'], x, y0 + h, 1); m.cls[y0 + h, x] = 'B'
    if stairs is not None:
        for i, x in enumerate((stairs, stairs + 1)):
            m.tile(m.STAIRS[0 if i == 0 else 2], x, y0 + h, 2); m.cls[y0 + h, x] = 'd'


def walkway(m, x0, x1, y):
    """2-wide plank walkway (rows y, y+1) between x0..x1, open at both ends, stilts below where not water"""
    for x in range(x0, x1 + 1):
        m.tile(PALE, x, y, 1); m.tile(PALE, x, y + 1, 1); m.cls[y, x] = m.cls[y + 1, x] = 'D'
        m.taken[y, x] = m.taken[y + 1, x] = True


def build(preview=None):
    m = K.RMap(W, H, 50, 120, water='Sea(Grass)', kit='sh')
    m.keep_under = 'd'
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
    # ---------------------------------------------------------------- lanes: curved dirt lanes into the round green
    m.stairs(35, 14, w=3, kit_rows=4)
    m.stairs(21, 12, w=2, kit_rows=4)                                           # the ridge lip is row 12 at x 21-22
    m.plan_cliffs()
    LN = dict(c='d', only='.tT')
    m.blob(40.5, 33.0, 8.4, 5.0, 'd', seed=51, rough=0.3, only='.tT')            # the green: an oval of trodden earth
    m.rect(0, 30, 16, 2, 'd', only='.T')                                         # Thistledown Lea road (rows 30-31) from the west edge
    m.lane([(15, 31), (21, 31.4), (27, 32.4), (32.5, 33)], w=2.6, seed=52, wobble=0.2, **LN)
    m.rect(35, 18, 3, 1, 'd', only='.tT')
    m.lane([(36.5, 18.5), (37.2, 21.5), (39.2, 24.6), (40, 28.4)], w=2.8, seed=53, wobble=0.2, **LN)   # down from the Loomhouse
    m.rect(21, 16, 2, 1, 'd', only='.tT')
    m.lane([(22, 16.5), (23.4, 19.2), (29, 20.4), (35.6, 19.6)], w=2.1, seed=54, wobble=0.2, **LN)     # the shrine path
    m.lane([(48.4, 32.6), (54, 31.3), (60, 31)], w=2.9, seed=55, wobble=0.2, **LN)                      # east lane to the pylon
    m.rect(59, 30, 13, 3, 'd', only='.tT')
    m.rect(34, 57, 4, 7, 'd', only='.tT')                                        # from Gossamer Wood
    m.lane([(35.6, 57.5), (34.4, 52), (34.8, 46.5), (36.6, 41.5), (38.4, 38)], w=2.9, seed=56, wobble=0.25, **LN)
    m.lane([(46, 36.6), (48.4, 41), (52, 46), (58, 47.4), (64.4, 47.2)], w=2.4, seed=57, wobble=0.25, **LN)   # round the chapel
    m.lane([(36.5, 56.6), (44, 57), (53, 56.6), (62.5, 56.8)], w=2.2, seed=58, wobble=0.2, **LN)        # the lantern decks
    m.lane([(34.6, 46.2), (30, 45.2), (25, 45.4), (19.6, 44.6), (17.8, 40), (17.6, 35), (18.4, 32)], w=2.3, seed=59, wobble=0.25, **LN)  # dyers' loop
    m.lane([(34.5, 57.4), (30, 57.2), (26.5, 56.6)], w=2.0, seed=60, wobble=0.15, **LN)
    m.rect(22, 10, 2, 3, 'd', only='.')                                          # shrine path above the stairs
    m.smooth('d', into='.', passes=2, only='.tT')
    # map builder 9 (SWAP 1A): the North Gate lane up the ridge to Spinners' Rise; the old Thistledown Lea road ends at the
    # stream (the Lea now joins the Gossamer's west eaves, not Briarwick)
    m.lane([(42.5, 12.5), (46, 9.5), (51, 6), (53.5, 2), (53.5, 0)], w=3.2, seed=63, wobble=0.15, **LN)
    m.rect(52, 0, 4, 3, 'd', only='.tT')
    m.rect(0, 29, 4, 4, 'T', only='.d')
    m.blob(40.8, 32.0, 3.6, 2.0, '.', seed=61, rough=0.2, only='d')              # the island under the Gathering Tree
    # ---------------------------------------------------------------- buildings
    E = []
    P = lambda n, at, **kw: E.append(SE.place(120, n, at, **kw))
    d = {}
    d['gym'] = m.stamp('pf_g_elder', 30, 1, 'BW_GYM', 'Gym door')
    d['guild'] = m.stamp('pf_g_tree6', 13, 19, 'BW_GUILD', 'Guildhall door')
    d['pc'] = m.stamp('sh_inn', 45, 16, 'BW_PC', 'Poke Center door')             # a timber hall, not Sheridan's blue Help Center
    d['house1'] = m.stamp('pf_g_tree4', 58, 17, 'BW_HOUSE1', 'Treetop House door')
    d['mart'] = m.stamp('sh_cot', 26, 37, 'BW_MART', 'Mart door')
    d['chapel'] = m.stamp('sh_big', 55, 34, 'BW_CHAPEL', 'Chapel door')
    d['house2'] = m.stamp('pf_g_tree4', 40, 44, 'BW_HOUSE2', "Cutter's House door")
    m.stamp('pf_g_tree2', 39, 27)                                                # the Gathering Tree on the green
    hd = []
    for nm, x, y in (('pf_g_tree4p', 20, 36), ('pf_g_tree2', 47, 8), ('pf_g_tree2', 66, 14),
                     ('pf_g_tree2', 46, 50), ('sh_small', 65, 22), ('sh_small', 50, 35), ('sh_ell', 23, 49), ('pf_g_tree2', 8, 54),
                     ('pf_g_tree2', 67, 40)):
        if m.free(x, y, STAMPS[nm]['w'], STAMPS[nm]['h'], on='.dT'):
            m.stamp(nm, x, y)
            if 'door' in STAMPS[nm]: dd = STAMPS[nm]['door']; hd.append((x + dd[0], y + dd[1]))
        else: print('  (no room for %s at %d,%d)' % (nm, x, y))
    for dx, dy in list(d.values()) + hd: m.doorpath((dx, dy), depth=8)
    for y in range(58, 63):                                  # a clearing round the weavers' row house: no canopy over its eaves
        for x in range(20, 34):
            if m.cls[y, x] == 'T': m.cls[y, x] = '.' if y < 62 else 'T'
    for x, y in ((38, 31), (39, 33), (43, 31), (42, 33), (44, 32), (37, 32)):     # flowers round the Gathering Tree
        if m.cls[y, x] == '.' and not m.taken[y, x]: m.tile(m.decor['flowers'][(x * 3 + y) % 6], x, y, 1)
    put = lambda nm, x, y, on='.d': (m.stamp(nm, x, y) if m.free(x, y, STAMPS[nm]['w'], STAMPS[nm]['h'], on=on) and not m.cliff[y:y + STAMPS[nm]['h'], x:x + STAMPS[nm]['w']].any() else print('  (no room for %s at %d,%d)' % (nm, x, y)))
    put('pf_pcsign', 49, 27)
    deck(m, 22, 23, 7, 4, stairs=24)                         # the weavers' deck beside the Guildhall tree
    deck(m, 51, 52, 5, 3, stairs=52)                         # lantern decks, south-east
    deck(m, 59, 52, 5, 3, stairs=61)
    walkway(m, 56, 58, 52)
    walkway(m, sx(30) - 2, sx(31) + 4, 30)                   # the Thistledown Lea road over the stream
    # ---------------------------------------------------------------- events
    P('To Gossamer Wood', (35, 63)); P('To Gossamer Wood b', (36, 63))
    E.append({'type': 'sign', 'name': 'North Gate sign', 'at': list(m.snap(51, 4, '.d', r=3)), 'post': False,
              'text': "NORTH GATE - Spinners' Rise, Frostwick Pass and the Hoar Road north."})
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
    S('Town sign', 38, 58); S('Finch', 57, 33); S('Rope-bridge Boy', 28, 32); S('Grandmother knitting', 45, 36)
    town = [('Dyer', 16, 37), ('Apprentice', 21, 32), ('Silk Merchant', 35, 35), ('Meridian Linesman', 53, 31), ('Tired Mother', 32, 46),
            ('Old Man on bridge', 9, 31), ('Girl in ogre mask', 44, 31), ('Boy in dog mask', 45, 32), ('Egg-seller', 47, 34),
            ('Tax-barge Deserter', 33, 55), ('Accord Chaplain', 60, 47), ('Youngster', 50, 29), ('Woman with basket', 48, 41),
            ("Cutter's Wife", 44, 52), ('Bun-seller', 40, 40)]
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
                     ('pf_logbench', 59, 53), ('sh_campfire', 38, 36), ('sh_crates', 47, 29), ('pf_p_silk', 54, 52), ('pf_p_silk', 60, 52),
                     ('pf_logbench', 38, 33), ('pf_logbench', 42, 33), ('hb_tables', 33, 30), ('hb_dyeline', 14, 34), ('hb_rugline', 31, 35),
                     ('hb_boxes', 34, 37), ('hb_cask', 44, 29), ('hb_washline', 62, 26), ('hb_barrel', 53, 26), ('hb_tables', 44, 37),
                     ('pf_logbench', 20, 47), ('hb_keg', 31, 43), ('hb_barrel2', 57, 46), ('hb_rugline2', 20, 28), ('pf_logbench', 47, 44),
                     ('hb_boxes2', 37, 51), ('hb_cask', 31, 54), ('pf_p_awning', 33, 29), ('pf_p_awning', 44, 36), ('hb_fish', 36, 29), ('hb_barrel', 47, 36)):
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
    for cx, cy, n in ((24, 30, 1), (31, 41, 1), (43, 26, 1), (60, 44, 1), (52, 42, 2), (40, 54, 2), (44, 60, 2), (27, 17, 1),
                      (57, 13, 2), (64, 18, 1), (14, 43, 1), (66, 46, 1), (52, 59, 2), (20, 58, 2), (22, 28, 1), (30, 26, 2),
                      (33, 23, 1), (43, 21, 1), (56, 27, 1), (24, 42, 1), (52, 37, 1), (30, 49, 1), (42, 41, 1), (66, 36, 1)):
        m.trees(cx, cy, n, TREES, r=3, seed=cx + cy * 5)
    for x, y in ((34, 22), (42, 27), (32, 38), (49, 35), (37, 48), (58, 29), (26, 31), (19, 30), (33, 29), (50, 45), (22, 46),
                 (16, 40), (45, 55), (57, 55), (61, 46), (32, 55), (25, 19)):
        if m.free(x, y - 1, 1, 2, on='.'): m.stamp('pf_lantern', x, y - 1)
    m.beds(prefixes=('sh_',))
    print('  yard trees', m.autotrees(26, TREES, seed=7, gap=0, box=(12, 14, 68, 60)))
    m.greenfill(2)
    # ---------------------------------------------------------------- paint
    m.paint()
    garlands(m, ((33, 48, 28, 0), (33, 48, 38, 1), (44, 50, 27, 2), (17, 28, 30, 3), (50, 54, 33, 1), (33, 38, 56, 2), (32, 37, 45, 3)))
    m.scatter(9, seed=21, on='.T')
    m.seal_edges([('N', 52, 4)], keep=[tuple(e['at']) for e in m.events if e.get('type') == 'warp'] + [(x, H - 1) for x in range(33, 39)])
    if preview: m.preview(preview, 0.5)
    head = {'id': 120, 'biome': 'forest', 'name': 'Briarwick', 'parent': 0, 'bgm': 'Lappet Town', 'rubric': True, 'yards_ok': True,
            'metadata': {'Outdoor': True, 'ShowArea': True, 'MapPosition': [0, 12, 22], 'BattleBack': 'forest'},
            'tone': [-10, -22, 2, 4], 'fog': {'name': 'prismfall_spores', 'opacity': 46, 'blend': 1, 'zoom': 100, 'sx': 1, 'sy': -1},
            'connections': [{'dir': 'N', 'offset': 52, 'to': 566, 'to_offset': 38}], '_file': '120_briarwick.yaml'}
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
