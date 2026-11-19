#!/usr/bin/env python3
"""The Dovetail (109 deck, 110 cabin). The deck is plank tiles laid as a hull outline on open sea with a wooden rail,
a wheelhouse aft, freight, barrels and lanterns. Every event comes from layouts/story_early.py (the FINAL script):
the intro, Edda at the rail, Voss and the Fellowship, six passengers, the gangway that opens on S101.
Run: python3 -I layouts/dovetail.py   (also writes the cabin and the other early interiors via early_interiors.py)"""
import os, sys, yaml
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from villagekit import HERE
import story_early as SE
import early_interiors as EI


def build():
    """109 on the PF Rejuv sheet (tileset 51 "Coast"): Rejuvenation's animated Ocean with deep swells round the ship,
    ship_art's deck (ported to the pf part by rcustom.py), freight and fittings from the PF Rejuv harbour props."""
    import numpy as np, json as _json
    import rkit as K
    import render as R
    from terrain import vnoise
    import ship_art as SA
    W, H = 34, 22
    m = K.RMap(W, H, 51, 109, water='Ocean')
    SA.use('dovetail'); deck = SA.deck
    dk = np.array([[bool(deck(x, y)) for x in range(W)] for y in range(H)])
    near = np.zeros((H, W), bool)
    for y, x in np.argwhere(dk): near[max(0, y - 3):y + 4, max(0, x - 3):x + 4] = True
    for y in range(H):
        for x in range(W):
            m.cls[y, x] = 'W' if (not near[y, x] and vnoise(x, y, 9, 5.0) > 0.5) else 'w'
    K.RMap.smooth(m, 'W', into='w', passes=2, only='w')
    m.cls[near & (m.cls == 'W')] = 'w'
    gang = (9, 15)                                   # the gangway gap in the starboard rail, aft
    E = []
    P = lambda n, at, **kw: E.append(SE.place(109, n, at, **kw))
    P('Prologue intro', (16, 13)); P('Rail sign', (12, 5)); P('Mug ring', (13, 5))
    for i, x in enumerate(range(10, 15)): P('Rail watch %d' % (i + 1), (x, 6))
    edda = (6, 9); P('Captain Edda', edda)
    for e in E:
        if e['name'].startswith('Rail watch'):
            txt = yaml.safe_dump(e['pages']).replace('moveto(EDDA_HOME)', 'moveto(%d, %d)' % edda)
            e['pages'] = yaml.safe_load(txt)
    P('Aurelian Voss', (21, 8)); P('Gangway', gang)
    P('Horizon', (30, 10)); P('HiddenItem coiled rope', (27, 12))
    P('Deckhand', (8, 12)); P('Old Man', (18, 6)); P('Woman with crate', (24, 13)); P('Boy', (16, 7))
    P("Boy's Mother", (17, 8)); P('Sailor', (26, 9)); P('Seasick Man', (4, 11))
    P('Cabin hatch', (15, 10), arrive=[15, 11, 'down'])
    missing = SE.unplaced(109)
    if missing: raise SystemExit('dovetail: script events not placed: %s' % missing)
    m.events = E
    # ---- paint: sea, then the ship (opaque deck tiles replace the ground layer so freight can stand on them)
    m.paint_ground(); m.autotiles()
    tc = R.TileCache(R.tilesets()[51]); opaque = {}
    def is_opaque(t):
        if t not in opaque:
            im = tc.tile(t); opaque[t] = im is not None and im.getchannel('A').getextrema()[0] == 255
        return opaque[t]
    interior = np.zeros((H, W), bool)
    for x, y, z, t in K._ST['_ship_dovetail']['tiles']:
        if not m.inb(x, y): continue
        if z == 0:
            if is_opaque(t): m.L[0, y, x] = t; m.L[1, y, x] = 0; interior[y, x] = True
            else: m.L[1, y, x] = t
        else: m.L[2, y, x] = t
    props = (('hb_wheelhouse', 4, 6), ('sh_crates', 18, 11), ('sh_crates', 21, 11), ('hb_barrel', 9, 6), ('hb_barrel2', 8, 6),
             ('hb_barrel', 20, 13), ('hb_barrel2', 21, 13), ('pf_p_lantern', 23, 6), ('pf_lantern', 10, 11), ('sh_crates', 13, 12),
             ('hb_fish', 18, 13), ('pf_p_net', 24, 8), ('sh_crates', 4, 11), ('hb_banner', 19, 8), ('hb_buoy2', 26, 7), ('hb_keg', 25, 11),
             ('hb_boxes', 11, 13), ('hb_cask', 27, 10), ('hb_boxes2', 22, 13), ('hb_crates4', 20, 6), ('hb_barrels', 6, 13),
             ('hb_tubs', 11, 9) if False else ('hb_keg', 12, 12), ('hb_boxes', 25, 6), ('hb_cask', 16, 5))
    ev = {tuple(e['at']) for e in E}
    start = (7, 6)                                   # PRISMFALL_START (004_NewGameStart.rb) must stay walkable
    for nm, x, y in props:
        st = K.STAMPS[nm]; L = np.array(st['layers'])
        cells = [(x + i, y + j) for j in range(st['h']) for i in range(st['w']) if L[:, j, i].any()]
        solid = [(x + i, y + j) for j in range(st['h']) for i in range(st['w']) if L[1, j, i]]
        bad = [c for c in solid if not m.inb(*c) or not interior[c[1], c[0]] or c in ev or c == start or m.taken[c[1], c[0]]]
        if any(not m.inb(*c) for c in cells) or len(bad) * 2 > len(solid) or any(c in ev or c == start for c in bad):
            print('  (dovetail: %s at %d,%d skipped)' % (nm, x, y)); continue
        for j in range(st['h']):
            for i in range(st['w']):
                if L[1, j, i] and interior[y + j, x + i] and not m.taken[y + j, x + i]: m.L[1, y + j, x + i] = int(L[1, j, i]); m.taken[y + j, x + i] = True
                if L[2, j, i]: m.L[2, y + j, x + i] = int(L[2, j, i])
    head = {'id': 109, 'biome': 'harbour', 'name': 'The Dovetail - Deck', 'parent': 0, 'bgm': 'Surfing', 'tone': [14, -4, -24, 10],
            'fog': {'name': 'prismfall_seamist', 'opacity': 55, 'blend': 0, 'zoom': 100, 'sx': 3, 'sy': 0},
            'metadata': {'Outdoor': True, 'ShowArea': True, 'MapPosition': [0, 14, 28], 'Weather': ['Rain', 0]}, '_file': '109_dovetail.yaml'}
    old = {s['id']: s for s in yaml.safe_load_all(open(os.path.join(HERE, 'layouts', 'old_109.yaml'))) if s}[109]
    for k in ('bgm', 'metadata', 'display_name'):
        if k in old: head[k] = old[k]
    m.write(109, head, '# The Dovetail - Deck (109). WRITTEN BY layouts/dovetail.py (PF Rejuv, tileset 51).\n')
    cab = EI.build()
    txt = open(os.path.join(HERE, 'specs', '109_dovetail.yaml')).read()
    open(os.path.join(HERE, 'specs', '109_dovetail.yaml'), 'w').write(txt + '---\n' + yaml.safe_dump(cab, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))


if __name__ == '__main__':
    build()
