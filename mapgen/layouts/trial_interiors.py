#!/usr/bin/env python3
"""Small interiors requested by the Trials workstream (mapgen/REQUESTS.md, design/TRIAL_EVENTS.yaml), map builder 9:
  148 Saltmere Lantern House  - a quiet grey room beside the Lantern Theatre: benches, a lantern rope, Sister Hollin
  126 Briarwick Lantern House - the hollow-tree room under the Loyal Three shrine: a lantern-loom, Mother Aldreth
  168 The Net Loft (Ebbmouth) - nets, the carved Tally Mast, a long feast table, Bersi Gullsong
Every keeper is one call, pf_trial_talk(:KEY) (plugins/Prismfall Trials): dialogue lives in the plugin.
Run: python3 -I layouts/trial_interiors.py && python3 -I build.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from interiorkit import Room, write, combine

TALK = lambda key: [{'script': 'pf_trial_talk(:%s)' % key}]


def keeper(name, key, at, sprite, d='down'):
    return {'type': 'event', 'name': name, 'at': list(at), 'pages': [
        {'graphic': {'sprite': sprite, 'dir': d}, 'trigger': 'action', 'commands': TALK(key)}]}


def obj(name, at, text=None, cmds=None):
    return {'type': 'event', 'name': name, 'at': list(at), 'pages': [{'trigger': 'action', 'commands': cmds or [text]}]}


def head(mid, name, parent, bgm, link_town, **kw):
    h = {'id': mid, 'name': name, 'parent': parent, 'bgm': bgm, 'metadata': {}, 'tone': [6, 2, -6, 8], 'biome': 'interior'}
    h.update(kw); return h


def build():
    specs = []
    # ---------------------------------------------------------------- 148 Saltmere Lantern House
    r = Room(11, 7, door_x=4)
    for fx in (1, 8): r.window(fx)
    r.rug(3, 1, 5, 4)
    for fy in (2, 4):
        for fx in (0, 1, 9, 10): r.tf('stool', fx, fy)
    r.tf('bench_v', 0, 0); r.tf('bench_v', 10, 0)
    r.tf('bust', 5, -1); r.tf('flowerpot', 3, 0); r.tf('flowerpot', 7, 0); r.tf('shelf_low', 8, -1); r.tf('books_open', 2, -1)
    r.tf('plant', 10, 4); r.tf('bookshelf_s', 0, 5)
    ev = [keeper('Sister Hollin', 'HOLLIN', r.at(6, 2), 'NPC 28', 'down'),
          obj('Lantern rope', r.at(5, 0), cmds=[{'script': 'pf_trial_board(:ELOWEN)'}]),
          obj('Slate', r.at(4, 2), 'A slate on a stand. Someone has written, very neatly: "PLEASE BE QUIET." Underneath, in a child\'s hand: "why"')]
    specs.append(r.spec(head(148, 'Saltmere Lantern House', 140, 'Lerucean Town', 'SM_LANTERN', metadata={'MapPosition': [0, 10, 25]}), ev, 'SM_LANTERN'))
    # ---------------------------------------------------------------- 126 Briarwick Lantern House (hollow tree)
    r = Room(9, 7, door_x=3)
    r.window(4)
    r.rug(2, 2, 5, 3); r.tf('stool', 1, 3); r.tf('stool', 7, 3); r.tf('flowerpot', 0, 0); r.tf('flowerpot', 8, 0)
    r.tf('shelf_wood', 6, -1); r.tf('plant', 0, 4); r.tf('bucket', 8, 5); r.tf('easel1', 1, 0)
    ev = [keeper('Mother Aldreth', 'ALDRETH', r.at(4, 1), 'NPC 27', 'down'),
          obj('Lantern-loom', r.at(3, 1), 'A loom strung with paper lantern-cords instead of thread. Each knot is a name.'),
          obj('Lantern board', r.at(7, 1), cmds=[{'script': 'pf_trial_board(:ELOWEN)'}])]
    specs.append(r.spec(head(126, 'Briarwick Lantern House', 120, 'Lerucean Town', 'BW_LANTERN'), ev, 'BW_LANTERN'))
    # ---------------------------------------------------------------- 168 The Net Loft (Ebbmouth)
    r = Room(15, 8, door_x=6)
    for fx in (2, 7, 12): r.window(fx)
    r.rug(3, 3, 9, 3); r.tf('dining', 4, 3)
    r.tf('crates3', 0, 0); r.tf('barrel_b', 13, 0); r.tf('barrel_y', 14, 0); r.tf('lifering', 9, -2); r.tf('rodbucket', 14, 5)
    r.tf('bench_v', 1, 4); r.tf('bench_v', 13, 3); r.tf('pallet', 12, 6); r.tf('bucket', 0, 6); r.tf('shelf_bottles', 4, -1)
    ev = [keeper('Bersi Gullsong', 'BERSI', r.at(7, 1), 'NPC 21', 'down'),
          obj('Tally Mast', r.at(6, 0), 'THE TALLY MAST. Every notch a debt, every debt a name, every name sung once a year.'),
          obj('Tally board', r.at(10, 1), cmds=[{'script': 'pf_trial_board(:ISENMAR)'}])]
    specs.append(r.spec(head(168, 'The Net Loft', 160, 'Lerucean Town', 'EB_NETLOFT', metadata={}), ev, 'EB_NETLOFT'))
    # ---------------------------------------------------------------- 542 The Brinewife's Rest (re-tiled from the stock house2 template)
    r = Room(11, 7, door_x=4)
    for fx in (2, 8): r.window(fx)
    r.sf('bed_o', 0, 0); r.sf('bed_o', 8, 0); r.rug(3, 2, 5, 3); r.tf('table_dark', 4, 3); r.tf('stool', 3, 4); r.tf('stool', 7, 4)
    r.tf('kitchen', 4, -1); r.tf('barrel_y', 0, 5); r.tf('bucket', 10, 5); r.tf('shelf_bottles', 9, -1) if False else None
    ev = [{'type': 'event', 'name': 'Rest house keeper', 'at': r.at(6, 2), 'pages': [{'graphic': {'sprite': 'NPC 28', 'dir': 'down'}, 'trigger': 'action', 'commands': [
        "Brinewife: Marsh got you? It gets everyone. Sit. Rest. There's broth, and it's mostly salt, and it's good.", {'heal': True}, {'me': 'Pkmn healing'},
        'Your Pokémon were fully restored.']}]}]
    specs.append(r.spec(head(542, "The Brinewife's Rest", 541, 'Route 2', 'R4_REST', metadata={}), ev, 'R4_REST'))
    write('148_trial_interiors.yaml', specs,
          "# Trial interiors 148 / 126 / 168. WRITTEN BY layouts/trial_interiors.py - edit that script.\n")


if __name__ == '__main__':
    build()
