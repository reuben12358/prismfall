#!/usr/bin/env python3
"""The Dovetail (109 deck, 110 cabin). The deck is plank tiles laid as a hull outline on open sea with a wooden rail,
freight, barrels and lanterns; events come from layouts/old_109.yaml re-seated. Run with early_interiors (cabin)."""
import os, sys, yaml
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from villagekit import Village, HERE
import early_interiors as EI
from interiorkit import write
OLD = {s['id']: s for s in yaml.safe_load_all(open(os.path.join(HERE, 'layouts', 'old_109.yaml'))) if s}


def old(name, at, **kw):
    e = dict(next(e for e in OLD[109]['events'] if e.get('name') == name)); e['at'] = list(at); e.update(kw); return e


def build():
    W, H = 34, 22
    c = Village(W, H, 109, base='~')
    def deck(x, y):
        if not 5 <= y <= 15: return False
        half = 5.5 if x < 22 else 5.5 * max(0.0, 1 - ((x - 22) / 8.0) ** 1.6)
        return 3 <= x <= 30 and abs(y - 10) <= half
    for y in range(H):
        for x in range(W):
            if deck(x, y):
                rim = not all(deck(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                c.g[y][x] = 'w' if rim else 'D'
                if rim: c.tile(3831, x, y, 0); c.taken[y][x] = True
    E = [old('Prologue intro', (1, 1)), old('Captain Edda', (10, 7)), old('Deckhand', (6, 13)), old('Horizon', (27, 10), post=False),
         old('Aurelian Voss', (22, 8)), old('Cabin hatch', (15, 10), arrive=[15, 11, 'down'])]
    for e in E: c.taken[e['at'][1]][e['at'][0]] = True
    for x in (14, 15, 16): c.taken[10][x] = c.taken[11][x] = True
    for nm, x, y in (('p_crates', 4, 6), ('p_crates', 17, 6), ('hs_jonquil_36', 8, 6), ('hs_jonquil_37', 9, 6), ('t_barrel', 20, 13),
                     ('t_barrel2', 21, 13), ('tp_stall_13', 11, 13), ('p_lantern', 12, 6), ('p_lantern', 23, 11), ('tp_stall_01', 4, 14),
                     ('hs_jonquil_35', 18, 13), ('p_net', 24, 8), ('t_crate_pair', 5, 9)):
        c.stamp(nm, x, y, force=True)
    c.events = E
    head = {k: v for k, v in OLD[109].items() if k not in ('events', 'map', 'stamps', 'tiles', 'palette')}
    head.update({'palette': 'village', 'tone': [14, -4, -24, 10]})
    c.write('109_dovetail.yaml', head, '# The Dovetail - Deck (109). WRITTEN BY layouts/dovetail.py.\n', mirror_max=1.0)
    cab = EI.build()
    txt = open(os.path.join(HERE, 'specs', '109_dovetail.yaml')).read()
    open(os.path.join(HERE, 'specs', '109_dovetail.yaml'), 'w').write(txt + '---\n' + yaml.safe_dump(cab, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))


if __name__ == '__main__':
    build()
