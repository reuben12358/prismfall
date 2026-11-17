#!/usr/bin/env python3
"""The Dovetail (109 deck, 110 cabin). The deck is plank tiles laid as a hull outline on open sea with a wooden rail,
a wheelhouse aft, freight, barrels and lanterns. Every event comes from layouts/story_early.py (the FINAL script):
the intro, Edda at the rail, Voss and the Fellowship, six passengers, the gangway that opens on S101.
Run: python3 -I layouts/dovetail.py   (also writes the cabin and the other early interiors via early_interiors.py)"""
import os, sys, yaml
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from villagekit import Village, HERE
import story_early as SE
import early_interiors as EI


def build():
    W, H = 34, 22
    c = Village(W, H, 109, base='~')
    def deck(x, y):
        if not 5 <= y <= 15: return False
        half = 5.5 if x < 22 else 5.5 * max(0.0, 1 - ((x - 22) / 8.0) ** 1.6)
        if x < 7: half = 5.5 * (1 - ((7 - x) / 5.0) ** 2)
        return 3 <= x <= 30 and abs(y - 10) <= half
    for y in range(H):
        for x in range(W):
            if deck(x, y):
                rim = not all(deck(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                c.g[y][x] = 'w' if rim else 'D'
                if rim: c.tile(3831, x, y, 0); c.taken[y][x] = True
    gang = (9, 15)                                   # the gangway gap in the starboard rail, aft
    c.g[gang[1]][gang[0]] = 'D'
    E = []
    P = lambda n, at, **kw: E.append(SE.place(109, n, at, **kw))
    P('Prologue intro', (16, 13)); P('Rail sign', (12, 5)); P('Mug ring', (13, 5))
    for i, x in enumerate(range(10, 15)): P('Rail watch %d' % (i + 1), (x, 6))
    edda = (6, 9); P('Captain Edda', edda)
    for p in SE.EVENTS[109]['Rail watch 1']['pages']: pass
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
    for e in E: c.taken[e['at'][1]][e['at'][0]] = True
    for x in (14, 15, 16): c.taken[10][x] = c.taken[11][x] = True
    for x in range(10, 15): c.taken[6][x] = True
    for nm, x, y in (('hs_jonquil_12', 4, 6), ('p_crates', 18, 11), ('p_crates', 21, 11), ('hs_jonquil_36', 9, 6), ('hs_jonquil_37', 8, 6),
                     ('t_barrel', 20, 13), ('t_barrel2', 21, 13), ('tp_stall_13', 11, 12), ('p_lantern', 23, 6), ('p_lantern', 7, 12),
                     ('tp_stall_01', 12, 14), ('hs_jonquil_35', 18, 13), ('p_net', 24, 8), ('t_crate_pair', 5, 13), ('p_banner3', 19, 8),
                     ('hs_jonquil_07', 28, 9), ('tp_barrel_06', 25, 11)):
        c.stamp(nm, x, y, force=True)
    c.events = E
    head = {'id': 109, 'name': 'The Dovetail - Deck', 'parent': 0, 'bgm': 'Surfing', 'palette': 'village', 'tone': [14, -4, -24, 10],
            'fog': {'name': 'prismfall_seamist', 'opacity': 55, 'blend': 0, 'zoom': 100, 'sx': 3, 'sy': 0},
            'metadata': {'Outdoor': True, 'ShowArea': True, 'MapPosition': [0, 14, 28], 'Weather': ['Rain', 0]}}
    old = {s['id']: s for s in yaml.safe_load_all(open(os.path.join(HERE, 'layouts', 'old_109.yaml'))) if s}[109]
    for k in ('bgm', 'metadata', 'display_name'):
        if k in old: head[k] = old[k]
    c.write('109_dovetail.yaml', head, '# The Dovetail - Deck (109). WRITTEN BY layouts/dovetail.py.\n', mirror_max=1.0)
    cab = EI.build()
    txt = open(os.path.join(HERE, 'specs', '109_dovetail.yaml')).read()
    open(os.path.join(HERE, 'specs', '109_dovetail.yaml'), 'w').write(txt + '---\n' + yaml.safe_dump(cab, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))


if __name__ == '__main__':
    build()
