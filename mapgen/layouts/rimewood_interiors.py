#!/usr/bin/env python3
"""Frostwick interiors 571-576 (maps.json), Sheridan timber rooms on tileset 34 (interiorkit).  Doors FW_* on 570.
Run: python3 -I layouts/rimewood.py int  (or this file), then build.py 571-576."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from interiorkit import Room, write, combine, HERE
import story_early as SE


def H(i, name, **kw):
    h = {'id': i, 'name': name, 'parent': 570, 'bgm': '', 'biome': 'interior', 'tone': [6, 2, -6, 0],
         'metadata': {'ShowArea': False}}
    h.update(kw); return h


def talk(at, name, sprite, lines, d='down', again=None):
    pages = [{'graphic': {'sprite': sprite, 'dir': d}, 'trigger': 'action', 'commands': list(lines) + ([{'selfswitch': ['A', True]}] if again else [])}]
    if again: pages.append({'cond': {'self': 'A'}, 'graphic': {'sprite': sprite, 'dir': d}, 'trigger': 'action', 'commands': list(again)})
    return {'type': 'event', 'name': name, 'at': list(at), 'pages': pages}


def main():
    S = []
    # 571 Pokemon Center
    r = Room(13, 8)
    for fx in (2, 10): r.window(fx)
    r.tf('heal', 3, -1); r.tf('counter4', 5, 1); r.tf('tv', 10, -1); r.sf('plantrack', 0, -1); r.sf('plantrack', 12, -1)
    r.rug(4, 3, 5, 3); r.tf('table_tea', 5, 4); r.tf('bench_v', 0, 3); r.tf('bench_v', 12, 3); r.tf('fern_big', 11, 6)
    s = r.spec(H(571, 'Frostwick Pokémon Center', bgm='Poke Center', metadata={'ShowArea': False, 'HealingSpot': [570, 13, 26]}),
               [talk(r.at(2, 5), 'Local', 'NPC 08', ["Two kingdoms, one nurse. She's the only person in town nobody argues with."])], 'FW_PC')
    s['take_events'] = [{'template': 'pokecenter', 'name': 'Nurse', 'at': r.at(6, 0), 'prepend': SE.NO_MON},
                        {'template': 'pokecenter', 'name': 'Healing balls', 'at': r.at(4, 0)},
                        {'template': 'pokecenter', 'name': 'PC', 'at': r.at(10, 0)}]
    S.append(s)
    # 572 The Exchange: mart + barter-woman
    r = Room(15, 7)
    r.window(7); r.tf('counter4', 0, 1); r.tf('shelf_goods', 6, -1); r.tf('shelf_goods', 8, -1); r.tf('shelf_green', 11, 3)
    r.tf('crates3', 11, -1); r.tf('barrel_y', 14, 4); r.tf('barrel_b', 13, 5); r.tf('display', 5, 4); r.sf('fern', 0, 5)
    s = r.spec(H(572, 'The Exchange', bgm='Poke Mart'),
               [talk(r.at(9, 2), 'Barter-woman', 'NPC 25', ["Coin? Pfah. Bring me honey and I'll find you fresh water. Bring silk and I'll find you oil.",
                                                           "Three Honey for one Fresh Water. Elowen silk for Isenmar furs. That's the rate since before the Accord."],
                     again=["Rates haven't changed. Neither have I."])], 'FW_EXCH')
    s['take_events'] = [{'template': 'mart', 'name': 'Mart', 'at': r.at(1, 0)}]
    S.append(s)
    # 573 The Two Hearths: two hearths, a long table
    r = Room(21, 9)
    for fx in (5, 15): r.window(fx)
    r.tf('kitchen', 1, -1); r.tf('kitchen', 16, -1); r.rug(6, 3, 9, 3); r.tf('table_w', 7, 3); r.tf('table_w', 12, 3)
    r.tf('bookcase', 10, -1); r.sf('plantrack', 0, 4); r.tf('barrel_b', 20, 5); r.tf('barrel_y', 19, 6); r.tf('crate', 18, 6)
    s = r.spec(H(573, 'The Two Hearths'),
               [talk(r.at(3, 2), 'Brannagh (inn)', 'NPC 25', ["West hearth's mine. Applewood. Proper fire.", "Rooms are a bed and a quilt each. The quilts are both kingdoms' work. Nobody notices."]),
                talk(r.at(17, 2), 'Halvard (inn)', 'NPC 28', ["East hearth. Whale oil. Burns hotter than her apple twigs.", "Don't tell her I said they smell nice."]),
                talk(r.at(9, 6), 'Guest', 'NPC 16', ["I sat in the middle of the table to be polite. Now both of them are mad at me."])], 'FW_INN')
    S.append(s)
    # 574 Rime-silk Loft (inside a giant tree)
    r = Room(11, 8)
    r.window(5); r.sf('shelf', 0, -1); r.tf('workbench', 7, -1); r.rug(3, 3, 5, 3); r.tf('crate_i', 9, 5); r.sf('fern', 10, 5)
    s = r.spec(H(574, 'Rime-silk Loft'),
               [talk(r.at(3, 2), 'Weaver', 'NPC 14', ["Briarwick silk drifts west on the wind and freezes in the Rimewood. We spin it again here.",
                                                      "Rime-silk never thaws. Never. We've tried. The kettle tried hardest."]),
                {'type': 'item', 'at': r.at(8, 5), 'item': 'SILKSCARF'}], 'FW_LOFT')
    S.append(s)
    # 575 Border House: three clerks, three seals
    r = Room(15, 7)
    r.window(4); r.window(10); r.tf('desk', 2, 2); r.tf('desk', 6, 2); r.tf('desk', 10, 2); r.tf('bookshelf_s', 0, -1); r.tf('bookshelf_s', 14, -1)
    s = r.spec(H(575, 'Border House'),
               [talk(r.at(3, 1), 'Elowen clerk', 'NPC 14', ["*THUMP* Briar seal. Welcome to Elowen. Or welcome back. We're not fussy."]),
                talk(r.at(11, 1), 'Isenmar clerk', 'NPC 11', ["*THUMP* Whale seal. Welcome to Isenmar. Wipe your boots."]),
                talk(r.at(7, 1), 'Meridian clerk', 'NPC 16', ["*THUMP* Sunburst. Over both of theirs. Standard procedure now.",
                                                              "Whose procedure? The procedure's. Next."])], 'FW_BORDER')
    S.append(s)
    # 576 Halvard's Smokehouse
    r = Room(9, 6)
    r.tf('crates3', 0, -1); r.tf('barrel_b', 8, -1); r.tf('barrel_y', 7, -1); r.tf('food_table', 3, 2)
    s = r.spec(H(576, "Halvard's Smokehouse"),
               [talk(r.at(2, 2), "Halvard's daughter", 'NPC 07', ["Smoked eel? Take one. Dad says the Elowen lot pretend not to like it.",
                                                                   "Brannagh had three last week."], again=["Shh. About Brannagh."])], 'FW_SMOKE')
    S.append(s)
    write('571_frostwick_interiors.yaml', S, '# Frostwick interiors 571-576. WRITTEN BY layouts/rimewood_interiors.py - edit that script.\n')
    print('frostwick interiors written')


if __name__ == '__main__':
    main()
