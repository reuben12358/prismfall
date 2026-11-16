#!/usr/bin/env python3
"""Early-game town interiors on tileset 34 (interiorkit): Ferrow's Landing 101-108, the Dovetail cabin 110, Briarwick
121-125. Story events are taken by name from the previous specs (layouts/old_*.yaml, the committed versions) and re-seated.
Maps 523 and 526 in the old 121 file belong to the routes builder and are carried over untouched.
Run: python3 -I layouts/early_interiors.py && python3 -I build.py 101 102 103 104 105 106 107 108 110 121 122 123 124 125"""
import os, sys, yaml
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from interiorkit import Room, write, HERE
OLD = {}
for f in ('old_101', 'old_121', 'old_109'):
    for s in yaml.safe_load_all(open(os.path.join(HERE, 'layouts', f + '.yaml'))):
        if s: OLD[s['id']] = s
import scriptpour as SP
FN = {n['name']: n for n in SP.parse(SP.section(r'^## Map 101 — Pok', r'^## Map 103'), per_speaker=True)[0]}
FS = SP.parse(SP.section(r'^## Map 101 — Pok', r'^## Map 103'))[1]
BN = {n['name']: n for n in SP.parse(SP.section(r'^## Maps 121–125', r'^## Map 120 — \*\*EV "Pallbearer'), per_speaker=True)[0]}
BS = {s['name']: s for s in SP.parse(SP.section(r'^## Maps 121–125', r'^## Map 120 — \*\*EV "Pallbearer'))[1]}


def say(e, n):
    """Give an existing simple NPC the script's lines (keeps its sprite and place)."""
    e = dict(e); e.pop('text', None); e['commands'] = list(n['first']); return e


KEEP = ('id', 'name', 'display_name', 'parent', 'bgm', 'metadata', 'field')


def head(i, **kw):
    h = {k: OLD[i][k] for k in KEEP if k in OLD[i]}; h.update(kw); h.setdefault('tone', [10, 4, -12, 0]); return h


def old(i, name, at, **kw):
    for e in OLD[i]['events']:
        if e.get('name') == name:
            e = dict(e); e['at'] = list(at); e.update(kw); return e
    raise KeyError((i, name))


def pc(i, link, spot, npc, flip=False):
    r = Room(13, 7); F = (lambda x, w=1: 13 - x - w) if flip else (lambda x, w=1: x)
    for fx in (2, 10): r.window(fx)
    r.tf('heal', F(3, 2), -1); r.tf('counter4', F(5, 4), 1); r.tf('tv', F(10, 2), -1)
    r.sf('plantrack', F(0), -1); r.sf('plantrack', F(12), -1); r.sf('sofa', F(0, 5), 4); r.sf('yellowrug', F(9, 2), 3)
    r.sf('fern', F(12), 4); r.tf('shrub', F(8), 5); r.sf('table_sm', F(10, 2), 5)
    s = r.spec(head(i, metadata=dict(OLD[i]['metadata'], HealingSpot=spot)), [say(old(i, npc, r.at(F(10), 4)), (FN['Trainer at PC'] if i == 101 else BN['Trainer']))] + ([SP.sign_event(BS['Gale Post Desk'], r.at(F(10), 5), post=False)] if i == 121 else []), link)
    s['take_events'] = [{'template': 'pokecenter', 'name': 'Nurse', 'at': r.at(F(6), 0)},
                        {'template': 'pokecenter', 'name': 'Healing balls', 'at': r.at(F(4), 0)},
                        {'template': 'pokecenter', 'name': 'PC', 'at': r.at(F(10), 0)}]
    s['anchors'] = [r.at(2, 3), r.at(6, 4), r.at(11, 2)]
    return s


def mart(i, link, events, flip=False):
    r = Room(11, 7); F = (lambda x, w=1: 11 - x - w) if flip else (lambda x, w=1: x)
    r.window(F(5)); r.tf('counter4', F(0, 4), 1); r.tf('shelf_goods', F(6, 2), -1); r.tf('shelf_goods', F(8, 2), -1)
    r.tf('shelf_green', F(5, 2), 3); r.tf('shelf_green', F(8, 2), 3); r.tf('display', F(1, 2), 4); r.tf('crate_i', F(9, 2), 5)
    r.tf('barrel_y', F(10), -1); r.sf('fern', F(0), 5)
    s = r.spec(head(i), [dict(e, at=r.at(F(e['at'][0]), e['at'][1])) for e in events], link)
    s['take_events'] = [{'template': 'mart', 'name': 'Mart', 'at': r.at(F(1), 0)}]
    return s


def build():
    S = []
    S.append(pc(101, 'FL_PC', [100, 24, 28], 'Local'))
    S.append(mart(102, 'FL_MART', [old(102, 'Shopper', (7, 5))]))
    # 103 Tidewatch Station: Larch's lab. Tide instruments, books, the starter table.
    r = Room(17, 10)
    for fx in (5, 11): r.window(fx)
    r.sf('shelf', 0, -2); r.sf('shelf', 2, -2); r.tf('console', 7, -1); r.tf('labtank', 13, -1); r.tf('labtank', 15, -1)
    r.sf('table_long', 6, 3); r.tf('desk', 0, 5); r.tf('cabinet', 0, 8); r.sf('deskflowers', 11, 6); r.sf('plantrack', 16, 3)
    r.tf('crate_i', 3, 8); r.tf('plant', 5, -2); r.sf('yellowrug', 13, 4); r.tf('barrel_b', 16, 8)
    S.append(r.spec(head(103), [old(103, 'Professor Larch', r.at(8, 1)), old(103, 'Juno', r.at(4, 3)),
                                old(103, 'Starter table', r.at(8, 4)), old(103, 'Starter ball L', r.at(7, 4)),
                                old(103, 'Starter ball R', r.at(9, 4)), old(103, 'Rowan Ashby', r.at(3, 6)),
                                old(103, 'Imprint scanner', r.at(8, 0), post=False)], 'FL_LAB'))
    # 104 Tidewater Inn: counter, kitchen, a long table, three guest beds
    r = Room(15, 9)
    for fx in (3, 8): r.window(fx)
    r.tf('counter4', 0, 2); r.tf('kitchen', 10, -1); r.sf('table_long', 5, 4); r.sf('bed_o', 12, 3); r.sf('bed_o', 12, 6)
    r.tf('bunk_b', 0, 5); r.tf('food_table', 6, 0); r.sf('fern', 14, 1); r.sf('plantrack', 5, -1); r.tf('barrel_y', 9, 7); r.sf('chest', 2, 7)
    S.append(r.spec(head(104), [say(old(104, 'Innkeeper', r.at(1, 1)), FN['Innkeeper']), SP.npc_event(FN['Inn Guest'], r.at(7, 6)),
                                SP.npc_event(FN['Inn Guest 2'], r.at(10, 2))], 'FL_INN'))
    # 105 Lighthouse 1F: the keeper's room; stairs up
    r = Room(9, 7); r.window(2)
    r.tf('bunk_o', 0, 0); r.tf('kitchen', 3, -1); r.sf('stairs', 6, -2); r.tf('lifering', 0, 4); r.tf('crate', 7, 5); r.sf('table_sm', 3, 3)
    e = [old(105, None, r.at(7, 1), arrive=r.at(7, 2) + ['down']) if False else None]
    up = next(x for x in OLD[105]['events'] if x['type'] == 'warp'); upe = dict(up, at=r.at(8, 1), arrive=r.at(7, 2) + ['down'])
    s105 = r.spec(head(105), [upe, old(105, 'Keeper', r.at(3, 4))], 'FL_LIGHT'); a105 = r.at(7, 2)
    # 106 Lamp room
    r = Room(7, 6); r.tf('crates3', 0, 0); r.tf('barrel_b', 6, 0); r.tf('tv', 3, -1); r.tf('pallet', 5, 4)
    dn = next(x for x in OLD[106]['events'] if x['type'] == 'warp')
    upe['to'] = {'map': 106, 'x': r.at(1, 3)[0], 'y': r.at(1, 3)[1], 'dir': 'down'}
    s106 = r.spec(head(106), [dict(dn, at=r.at(1, 4), to={'map': 105, 'x': a105[0], 'y': a105[1], 'dir': 'down'}),
                              old(106, 'Hesper Vane', r.at(3, 2))], None)
    s106['tiles'] = [t for t in s106['tiles'] if t['tile'] not in (5512, 5513, 5514)]
    S += [s105, s106]
    # 107 Dockmaster: ledgers, a life ring, crates of unclaimed freight
    r = Room(11, 7); r.window(6)
    r.tf('desk', 1, 0); r.sf('shelf', 3, -2); r.tf('lifering', 8, -2); r.tf('bigbed', 8, 0); r.tf('crates3', 0, 4); r.tf('barrel_y', 3, 5)
    r.tf('drawer', 5, 0); r.sf('fern', 10, 5)
    S.append(r.spec(head(107), [say(old(107, 'Dockmaster', r.at(2, 2)), FN['Dockmaster']), SP.sign_event(FS[0], r.at(3, 1), post=False)], 'FL_DOCK'))
    # 108 Quarantine Customs Hall
    r = Room(19, 10)
    for fx in (4, 14): r.window(fx)
    r.tf('counter4', 2, 3); r.tf('counter4', 11, 3); r.tf('labtank', 8, -1); r.tf('console', 15, -1); r.tf('crates3', 0, 0)
    r.tf('pallet', 0, 7); r.tf('crate_i', 2, 8); r.tf('crate_i2', 16, 7); r.tf('sofa_g', 6, 7); r.tf('barrel_y', 18, 0); r.tf('barrel_b', 17, 0)
    r.sf('plantrack', 18, 4)
    S.append(r.spec(head(108), [old(108, 'Customs officer', r.at(3, 2)), old(108, 'Meridian tech', r.at(12, 2))], 'FL_CUSTOMS'))
    write('101_ferrows_landing_interiors.yaml', S, "# Ferrow's Landing interiors (101-108). WRITTEN BY layouts/early_interiors.py.\n")
    # 110 Dovetail cabin
    r = Room(9, 6); r.tf('bunk_o', 0, 0); r.tf('bunk_b', 2, 0); r.tf('desk', 5, 0); r.tf('crate_i', 7, 4); r.tf('barrel_y', 8, 0); r.tf('lifering', 4, -2)
    c110 = r.spec(head(110), [old(110, 'Up to deck', list(r.exit), arrive=[r.exit[0], r.exit[1] - 1, 'up']),
                              old(110, "Ines's letter", r.at(5, 1), post=False), old(110, 'Bunk', r.at(0, 2), post=False)], None)
    B = [pc(121, 'BW_PC', [120, 28, 29], 'Trainer', flip=True), mart(122, 'BW_MART', OLD[122].get('events', []) + [SP.npc_event(BN['Customer'], (7, 5))], flip=True)]
    # 123 Weavers' Guildhall: bolts of silk, pattern shelves, the long cutting tables
    r = Room(15, 9)
    for fx in (4, 10): r.window(fx)
    r.sf('shelf', 0, -2); r.sf('shelf', 13, -2); r.sf('table_long', 2, 3); r.sf('table_long', 8, 3); r.sf('chest', 0, 7); r.sf('chest', 12, 7)
    r.sf('yellowrug', 6, 6); r.sf('plantrack', 7, -1); r.tf('crate_i2', 4, 7); r.tf('wardrobe', 2, -1)
    B.append(r.spec(head(123), [old(123, 'Guild master', r.at(5, 2)), old(123, 'Apprentice', r.at(9, 5))], 'BW_GUILD'))
    r = Room(9, 7); r.window(4)
    r.sf('bed_o', 0, 0); r.sf('shelf', 6, -2); r.sf('table_sm', 3, 3); r.sf('plantrack', 8, 1); r.sf('yellowrug', 4, 5); r.tf('dresser', 3, -1)
    B.append(r.spec(head(124), [say(old(124, 'Grandmother', r.at(5, 3)), BN['Retired Weaver']), SP.sign_event(BS['Bookshelf'], r.at(6, 1), post=False)], 'BW_HOUSE1'))
    r = Room(9, 7); r.window(2)
    r.tf('workbench', 0, 0); r.tf('crates3', 6, 0); r.tf('pallet', 0, 5); r.tf('bunk_b', 4, 0); r.tf('drawer', 7, 5)
    B.append(r.spec(head(125), [old(125, 'Cutter', r.at(5, 3))], 'BW_HOUSE2'))
    raw = open(os.path.join(HERE, 'layouts', 'old_121.yaml')).read().split('\n---\n')
    others = [d for d in raw if any(('\nid: %d\n' % i) in ('\n' + d) for i in (526, 523))]
    write('121_briarwick_interiors.yaml', B, '# Briarwick interiors (121-125). WRITTEN BY layouts/early_interiors.py. 526 / 523 below are carried over.\n')
    open(os.path.join(HERE, 'specs', '121_briarwick_interiors.yaml'), 'a').write('---\n' + '\n---\n'.join(others) + '\n')
    return c110


if __name__ == '__main__':
    build()
