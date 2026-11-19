#!/usr/bin/env python3
"""Early-game interiors on tileset 34 (interiorkit): Ferrow's Landing 101-108, the Dovetail cabin 110, Briarwick 121-125
(with the chapel beside the Treetop House and the Warden's loft above the Guildhall), and the routes builder's 523 Hale
Farmhouse / 526 Woodward's Hut re-tiled from their stock templates (their events from layouts/b3_interiors_523_526.yaml).
Every room has a filled centre (rug, table, work) and says who lives there. Story events: layouts/story_early.py.
Run: python3 -I layouts/dovetail.py (it calls this), then build.py."""
import os, sys, yaml
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from interiorkit import Room, write, combine, HERE
import story_early as SE
OLD = {}
for f in ('old_101', 'old_121', 'old_109'):
    for s in yaml.safe_load_all(open(os.path.join(HERE, 'layouts', f + '.yaml'))):
        if s: OLD[s['id']] = s
B3 = {s['id']: s for s in yaml.safe_load_all(open(os.path.join(HERE, 'layouts', 'b3_interiors_523_526.yaml'))) if s}
KEEP = ('id', 'name', 'display_name', 'parent', 'bgm', 'metadata', 'field')
FLOOR_TILE = 501         # glasshouse floor for Tidewatch's Wayfarer Sanctuary (Tectonic Inside, green diamond tile)


def head(i, src=None, **kw):
    s = (src or OLD)[i]; h = {k: s[k] for k in KEEP if k in s}; h.update(kw); h.setdefault('tone', [10, 4, -12, 0]); h.setdefault('biome', 'interior'); return h


def old(i, name, at, **kw):
    for e in OLD[i]['events']:
        if e.get('name') == name:
            e = dict(e); e['at'] = list(at); e.update(kw); return e
    raise KeyError((i, name))


def P(mid, name, at, **kw): return SE.place(mid, name, at, **kw)


def done(mid):
    m = SE.unplaced(mid)
    if m: raise SystemExit('early_interiors: map %d script events not placed: %s' % (mid, m))


def pc(i, link, spot, nurse_line, extra, flip=False):
    r = Room(13, 8); F = (lambda x, w=1: 13 - x - w) if flip else (lambda x, w=1: x)
    for fx in (2, 10): r.window(fx)
    r.tf('heal', F(3, 2), -1); r.tf('counter4', F(5, 4), 1); r.tf('tv', F(10, 2), -1)
    r.sf('plantrack', F(0), -1); r.sf('plantrack', F(12), -1)
    r.rug(F(4, 5), 3, 5, 3); r.tf('table_tea', F(5, 2), 4)
    r.tf('bench_v', F(0), 3); r.tf('bench_v', F(12), 3); r.tf('bookshelf_s', F(9), -1)
    r.tf('fern_big', F(11), 6); r.tf('plant_s', F(1), 6); r.tf('painting1', F(7, 2), -2); r.tf('stool', F(10), 4); r.tf('stool', F(11), 4)
    s = r.spec(head(i, metadata=dict(OLD[i]['metadata'], HealingSpot=spot)), [e(r, F) for e in extra], link)
    s['take_events'] = [{'template': 'pokecenter', 'name': 'Nurse', 'at': r.at(F(6), 0),
                         'replace_text': {'\\rHello, and welcome to the Pokémon Center.': '\\r' + nurse_line}, 'prepend': SE.NO_MON},
                        {'template': 'pokecenter', 'name': 'Healing balls', 'at': r.at(F(4), 0)},
                        {'template': 'pokecenter', 'name': 'PC', 'at': r.at(F(10), 0)}]
    return s


def mart(i, link, extra, prepend, flip=False):
    r = Room(11, 7); F = (lambda x, w=1: 11 - x - w) if flip else (lambda x, w=1: x)
    r.window(F(5)); r.tf('counter4', F(0, 4), 1); r.tf('shelf_goods', F(6, 2), -1); r.tf('shelf_goods', F(8, 2), -1)
    r.tf('shelf_green', F(5, 2), 3); r.tf('shelf_green', F(8, 2), 3); r.tf('display', F(1, 2), 4); r.tf('crate_i', F(9, 2), 5)
    r.tf('barrel_y', F(10), -1); r.sf('fern', F(0), 5); r.tf('shelf_bottles', F(3, 2), -1); r.tf('bucket', F(4), 3); r.tf('barrel_b', F(7), 5)
    s = r.spec(head(i), [e(r, F) for e in extra], link)
    s['take_events'] = [{'template': 'mart', 'name': 'Mart', 'at': r.at(F(1), 0), 'prepend': prepend}]
    return s


def build():
    S = []
    # ------------------------------------------------------------------ 101 Ferrow PC, 102 Mart
    S.append(pc(101, 'FL_PC', [100, 24, 15], SE.NURSE_FL, [lambda r, F: P(101, 'Trainer at PC', r.at(F(10), 5))]))
    S.append(mart(102, 'FL_MART', [lambda r, F: P(102, 'Shopper', r.at(F(7), 5))], SE.MART_FL))
    done(101); done(102)
    # ------------------------------------------------------------------ 103 Tidewatch Station + the Wayfarer Sanctuary annex
    r = Room(22, 10)
    for fx in (3, 9, 14, 19): r.window(fx)
    r.floor(13, 0, 9, 10, FLOOR_TILE)                    # the glasshouse annex: tiled floor, plants, pens
    r.sf('shelf', 0, -2); r.tf('bookcase', 2, -2); r.tf('map_wall', 5, -2); r.tf('console', 8, -1); r.tf('kitchen', 10, -1)
    r.sf('table_long', 4, 2); r.tf('desk', 0, 5); r.tf('cabinet', 0, 8); r.tf('crate_i', 3, 8); r.tf('barrel_b', 8, 8)   # off the door column (x 11 = map 14: playtest)
    r.rug(4, 5, 5, 3); r.tf('table_dark', 5, 5); r.tf('stool', 7, 6); r.tf('books_open', 4, 6); r.tf('clock', 11, 1)
    r.sf('stairs', 9, 5)                                    # Larch's hayloft (Kestrel sleeps up there)
    for fx, fy in ((13, 0), (21, 0), (13, 8), (21, 8), (16, 8), (19, 3)): r.tf('fern_big' if (fx + fy) % 2 else 'plant', fx, fy - 1 if fy == 0 else fy - 1)
    r.tf('labtank', 15, -1); r.tf('shrub', 18, -1); r.sf('plants3', 13, 3); r.tf('shrub', 21, 4); r.tf('flowerpot', 20, 6)
    r.tf('table_tea', 16, 4); r.tf('bucket', 14, 7); r.tf('pen', 18, 6)    # a starter pen
    E = [P(103, 'Professor Larch', r.at(6, 1), ), P(103, 'Juno', r.at(5, 4)), P(103, 'Kestrel (loft)', r.at(10, 3)),
         P(103, 'Starter table', r.at(17, 5)), P(103, 'Rowan Ashby', r.at(14, 5)), P(103, 'Juno (station)', r.at(16, 6)),
         P(103, 'Station bookshelf', r.at(1, 0)), P(103, 'Imprint scanner', r.at(9, 0)), P(103, 'Kettle', r.at(11, 0))]
    E[0]['pages'][0]['graphic']['dir'] = 'up'
    S.append(r.spec(head(103), E, 'FL_LAB')); done(103)
    # ------------------------------------------------------------------ 104 Tidewater Inn: full of people who came home
    r = Room(15, 9)
    for fx in (3, 8, 12): r.window(fx)
    r.tf('counter4', 0, 2); r.tf('kitchen', 10, -1); r.sf('bed_o', 12, 3); r.sf('bed_o', 12, 6); r.tf('bunk_b', 0, 5)
    r.tf('food_table', 6, -1); r.sf('fern', 14, 0); r.sf('plantrack', 5, -1); r.tf('barrel_y', 9, 7); r.sf('chest', 2, 7)
    r.rug(4, 3, 7, 4); r.tf('dining', 6, 3); r.tf('clock', 4, -2); r.tf('painting3', 1, -2); r.tf('crate_i', 10, 7)
    r.tf('stool', 4, 4); r.tf('stool', 9, 5); r.tf('shelf_bottles', 2, -1)
    S.append(r.spec(head(104), [P(104, 'Innkeeper', r.at(1, 1)), P(104, 'Inn Guest', r.at(5, 6)), P(104, 'Inn Guest 2', r.at(10, 2))], 'FL_INN'))
    done(104)
    # ------------------------------------------------------------------ 105 / 106 the lighthouse (Hesper and Kestrel)
    r = Room(9, 7); r.window(2)
    r.tf('bunk_o', 0, 0); r.tf('kitchen', 3, -1); r.sf('stairs', 6, -2); r.tf('lifering', 0, 4); r.tf('crate', 7, 5); r.tf('table_dark', 3, 3)
    r.rug(2, 3, 4, 3); r.tf('rodbucket', 8, 2); r.tf('stool', 5, 4); r.tf('bucket', 0, 6)
    up = next(x for x in OLD[105]['events'] if x['type'] == 'warp'); upe = dict(up, at=r.at(8, 1), arrive=r.at(7, 2) + ['down'])
    s105 = r.spec(head(105), [upe, P(105, 'Rope coils', r.at(7, 5)), P(105, 'Cot', r.at(0, 1)), P(105, 'Cracked mirror', r.at(2, 0)),
                              P(105, 'Trunk', r.at(5, 5))], 'FL_LIGHT'); a105 = r.at(7, 2); done(105)
    r = Room(7, 6); r.tf('crates3', 0, 0); r.tf('barrel_b', 6, 0); r.tf('labtank', 3, -1); r.tf('pallet', 5, 4); r.tf('lifering', 1, -2)
    dn = next(x for x in OLD[106]['events'] if x['type'] == 'warp')
    upe['to'] = {'map': 106, 'x': r.at(1, 3)[0], 'y': r.at(1, 3)[1], 'dir': 'down'}
    s106 = r.spec(head(106), [dict(dn, at=r.at(1, 4), to={'map': 105, 'x': a105[0], 'y': a105[1], 'dir': 'down'}),
                              P(106, 'Hesper Vane', r.at(3, 2))], None)
    s106['tiles'] = [t for t in s106['tiles'] if t['tile'] not in (5512, 5513, 5514)]
    S += [s105, s106]; done(106)
    # ------------------------------------------------------------------ 107 the Dockmaster: ledgers and unclaimed freight
    r = Room(11, 7); r.window(6)
    r.tf('desk', 1, 0); r.sf('shelf', 3, -2); r.tf('lifering', 8, -2); r.tf('bigbed', 8, 0); r.tf('crates3', 0, 4); r.tf('barrel_y', 3, 5)
    r.tf('drawer', 5, 0); r.sf('fern', 10, 5); r.tf('map_wall', 5, -2); r.rug(4, 3, 4, 3); r.tf('table_dark', 5, 3); r.tf('rodbucket', 7, 5)
    S.append(r.spec(head(107), [P(107, 'Dockmaster', r.at(2, 2)), P(107, "Dockmaster's ledger", r.at(4, 0))], 'FL_DOCK')); done(107)
    # ------------------------------------------------------------------ 108 Quarantine Customs Hall
    r = Room(19, 10)
    for fx in (4, 14): r.window(fx)
    r.tf('counter4', 2, 3); r.tf('counter4', 11, 3); r.tf('labtank', 8, -1); r.tf('console', 15, -1); r.tf('crates3', 0, 0)
    r.tf('pallet', 0, 7); r.tf('crate_i', 2, 8); r.tf('crate_i2', 16, 7); r.tf('sofa_g', 6, 7); r.tf('barrel_y', 18, 0); r.tf('barrel_b', 17, 0)
    r.sf('plantrack', 18, 4); r.rug(7, 4, 5, 2); r.tf('map_wall', 5, -2); r.tf('clock', 12, -2); r.tf('bench_v', 18, 6); r.tf('stool', 4, 5)
    S.append(r.spec(head(108), [old(108, 'Customs officer', r.at(3, 2)), old(108, 'Meridian tech', r.at(12, 2))], 'FL_CUSTOMS'))
    write('101_ferrows_landing_interiors.yaml', S, "# Ferrow's Landing interiors (101-108). WRITTEN BY layouts/early_interiors.py.\n")
    # ------------------------------------------------------------------ 110 the Dovetail's cabin
    r = Room(9, 6); r.tf('bunk_o', 0, 0); r.tf('bunk_b', 2, 0); r.tf('kitchen', 5, -1); r.tf('crate_i', 7, 4); r.tf('lifering', 4, -2)
    r.window(8); r.tf('bookshelf_s', 4, -1); r.rug(2, 3, 4, 2); r.tf('table_dark', 3, 3); r.tf('barrel_y', 0, 4); r.tf('crates3', 6, 3) if False else None
    c110 = r.spec(head(110), [P(110, 'Up to deck', list(r.exit), arrive=[r.exit[0], r.exit[1] - 1, 'up']), P(110, 'Bunk', r.at(0, 2)),
                              P(110, 'Porthole', r.at(8, 0)), P(110, 'Cook', r.at(6, 2)), P(110, 'Bookshelf', r.at(4, 0)),
                              P(110, 'Locked trunk', r.at(7, 3)), P(110, "Mum's letter", r.at(1, 2))], None)
    c110['tiles'] = [t for t in c110['tiles'] if not (t['tile'] in (5512, 5513, 5514))]
    done(110)
    # ------------------------------------------------------------------ Briarwick
    B = [pc(121, 'BW_PC', [120, 47, 26], SE.NURSE_BW, [lambda r, F: P(121, 'Trainer', r.at(F(10), 5)),
                                                         lambda r, F: P(121, 'Gale Post desk', r.at(F(9), 1))], flip=True),
         mart(122, 'BW_MART', [lambda r, F: P(122, 'Customer', r.at(F(7), 5))], SE.MART_BW, flip=True)]
    done(121); done(122)
    # 123 Weavers' Guildhall (hall) + the Warden's loft (stairs between them)
    h = Room(15, 9)
    for fx in (4, 10): h.window(fx)
    h.sf('shelf', 0, -2); h.sf('table_long', 2, 3); h.sf('table_long', 8, 3); h.sf('chest', 0, 7); h.tf('wardrobe', 2, -1)
    h.rug(5, 6, 5, 2); h.sf('plantrack', 7, -1); h.tf('crate_i2', 4, 7); h.sf('stairs', 12, -2); h.tf('easel1', 10, -1)
    h.tf('shelf_wood', 6, -1); h.tf('stool', 4, 2); h.tf('stool', 10, 2); h.tf('bucket', 9, 7)
    l = Room(11, 7); l.window(5)
    l.rug(3, 2, 5, 3); l.tf('desk_dark', 4, 2); l.tf('bookcase', 0, -2); l.tf('bookshelf_s', 2, -1); l.tf('clock', 9, -2)
    l.tf('crates3', 8, 4); l.tf('stool', 6, 3); l.tf('flowerpot', 10, 1); l.sf('stairs', 0, 3)
    stair_h, stair_l = h.at(13, 1), l.at(1, 4)
    ev = [(0, P(123, 'Hett', h.at(5, 2))), (0, P(123, 'Apprentice (guild)', h.at(9, 5))), (0, P(123, 'Moth tally board', h.at(1, 0))),
          (0, P(123, 'Silk bolts', h.at(0, 6))), (0, P(123, 'Loft manager', h.at(14, 7))),
          (1, P(123, 'Guild ledger', l.at(4, 1))), (1, P(123, 'Tamsin (loft)', l.at(6, 1))), (1, P(123, 'Juno (loft)', l.at(2, 5)))]
    sp = combine([(h, 'BW_GUILD'), (l, None)], head(123), ev)
    xo = sp['_offsets']
    sp['events'] += [{'type': 'warp', 'name': 'Loft stairs up', 'at': [stair_h[0] + xo[0], stair_h[1]],
                      'to': {'map': 123, 'x': stair_l[0] + xo[1] + 2, 'y': stair_l[1], 'dir': 'right'}, 'se': 'Door exit'},
                     {'type': 'warp', 'name': 'Loft stairs down', 'at': [stair_l[0] + xo[1], stair_l[1]],
                      'to': {'map': 123, 'x': stair_h[0] + xo[0] - 1, 'y': stair_h[1] + 1, 'dir': 'down'}, 'se': 'Door exit'}]
    B.append(sp); done(123)
    # 124 Treetop House (the retired weaver) + the chapel (own door on 120)
    h = Room(9, 7); h.window(4)
    h.sf('bed_o', 0, 0); h.sf('shelf', 6, -2); h.sf('plantrack', 8, 1); h.tf('dresser', 3, -1); h.rug(2, 3, 5, 3); h.tf('table_tea', 3, 3)
    h.sf('loom', 7, 4) if False else h.tf('stool', 6, 4)
    h.tf('easel1', 0, 4); h.tf('flowerpot', 8, 5); h.tf('bucket', 1, 5)
    ch = Room(13, 9)
    for fx in (2, 6, 10): ch.window(fx)
    for fy in (3, 5, 7):                                  # rows of chapel chairs either side of the aisle
        for fx in (1, 2, 3, 9, 10, 11): ch.tf('stool', fx, fy)
    ch.rug(5, 1, 3, 8); ch.tf('bust', 6, -1); ch.tf('flowerpot', 4, 0); ch.tf('flowerpot', 8, 0); ch.tf('painting2', 0, -2); ch.tf('painting4', 11, -2)
    ch.tf('plant', 0, 0); ch.tf('plant', 12, 0)
    ev = [(0, P(124, 'Retired Weaver', h.at(5, 3))), (0, P(124, 'Bookshelf', h.at(6, 0))), (0, P(124, 'Loom', h.at(0, 3))),
          (1, P(124, 'Chapel mural', ch.at(6, 0))), (1, P(124, 'Child in pew', ch.at(5, 4))), (1, P(124, 'Chapel window', ch.at(10, 0)))]
    B.append(combine([(h, 'BW_HOUSE1'), (ch, 'BW_CHAPEL')], head(124), ev)); done(124)
    # 125 Cutter's House: axes, logs, a workbench
    r = Room(9, 7); r.window(2)
    r.tf('workbench', 0, 0); r.tf('crates3', 6, 0); r.tf('pallet', 0, 5); r.tf('bunk_b', 4, 0); r.tf('drawer', 7, 5)
    r.rug(2, 3, 4, 2); r.tf('table_dark', 3, 3); r.tf('stool', 5, 4); r.tf('bucket', 8, 3); r.tf('shelf_wood', 2, -1)
    B.append(r.spec(head(125), [P(125, 'Cutter', r.at(5, 3)), P(125, 'Axe rack', r.at(3, 0))], 'BW_HOUSE2')); done(125)
    # ------------------------------------------------------------------ 523 Hale Farmhouse / 526 Woodward's Hut (builder 3's events)
    r = Room(15, 8)
    for fx in (3, 9): r.window(fx)
    r.tf('kitchen', 0, -1); r.tf('shelf_bottles', 4, -1); r.rug(4, 2, 6, 4); r.tf('dining', 5, 2); r.tf('clock', 11, -2)
    r.sf('bed_o', 12, 0); r.tf('bookcase', 10, -2); r.sf('plants3', 12, 5); r.tf('barrel_y', 0, 6); r.tf('crate_i', 1, 6)
    r.tf('sideboard', 0, 2); r.tf('stool', 9, 3); r.tf('painting1', 6, -2); r.tf('bucket', 11, 6)
    b = B3[523]; at = {'Kitchen table': (6, 1), 'Wenna': (4, 3), 'Farmer Hale': (10, 5), 'Bookshelf': (10, 0), "Juno's seed packets": (8, 0), 'Bed': (13, 2)}
    h523 = {k: b[k] for k in KEEP if k in b}; h523['tone'] = [10, 4, -12, 0]
    s523 = r.spec(h523, [dict(e, at=r.at(*at[e['name']])) for e in b['events']], b['exit_link'])
    r = Room(9, 7); r.window(2)
    r.tf('workbench', 0, 0); r.tf('crates3', 6, 0); r.tf('bunk_o', 4, 0); r.rug(2, 3, 4, 2); r.tf('table_dark', 3, 3)
    r.tf('rodbucket', 8, 3); r.tf('bucket', 0, 5); r.tf('stool', 5, 4); r.tf('pallet', 7, 5)
    b = B3[526]; at = {'Woodward': (5, 3), 'Bookshelf': (2, 0)}
    h526 = {k: b[k] for k in KEEP if k in b}; h526['tone'] = [10, 4, -12, 0]
    s526 = r.spec(h526, [dict(e, at=r.at(*at[e['name']])) for e in b['events']], b['exit_link'])
    write('121_briarwick_interiors.yaml', B + [s523, s526],
          "# Briarwick interiors (121-125) + 523 / 526 (events from layouts/b3_interiors_523_526.yaml). WRITTEN BY layouts/early_interiors.py.\n")
    return c110


if __name__ == '__main__':
    build()
