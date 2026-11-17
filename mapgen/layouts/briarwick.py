#!/usr/bin/env python3
"""Briarwick (120): the weavers' village among giant trees and silk, 72x64, palette `village`, at lantern-lit dusk.
No crossroads: the Gossamer lane winds up from the south around the boles to an off-centre green; the Route 3 road
crosses the stream on a raised plank walkway and joins the lane below the green; the pylon lane leaves the green's east
side; stairs climb the knoll to the Loomhouse, the one enormous elder tree. Height: the knoll, two raised timber decks
(the weavers' deck beside the Guildhall tree, the lantern decks in the south-east joined by a walkway) reached by
plank stairs at the boles. Silk garlands and hanging lanterns are strung overhead on layer 3. Old-growth forest borders.
Every story event comes from layouts/story_early.py. Run: python3 -I layouts/briarwick.py && python3 -I build.py 120"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from villagekit import Village, STAMPS, GARDEN, HERE, C2, C3, DECK, vnoise
import story_early as SE
W, H = 72, 64
GARL = [C3 + 23 * 8 + i for i in range(4)]          # plain, pennants, lantern, tufts


def rope(c, x0, x1, y):
    for x in range(min(x0, x1), max(x0, x1) + 1): c.tile(C2 + 115, x, y, 2)


def deck(c, x0, y0, w, h, stairs=(), open_sides=''):
    """Raised timber deck: 9-slice planks with blocking edges, solid stilts below, plank stairs down from `stairs` columns.
    open_sides: 'W'/'E' leave that edge open (where a walkway joins)."""
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            top, bot, lef, rig = y == y0, y == y0 + h - 1, x == x0 and 'W' not in open_sides, x == x0 + w - 1 and 'E' not in open_sides
            k = ('T' if top else 'B' if bot else '') + ('L' if lef else 'R' if rig else '')
            if bot and x in stairs: k = 'L' if lef else 'R' if rig else 'C'
            c.tile(DECK.get(k or 'C', DECK['C']), x, y, 1); c.g[y][x] = ','; c.taken[y][x] = True
    for x in range(x0, x0 + w):
        y = y0 + h
        t = DECK['stair'] if x in stairs else DECK['legL' if x == x0 else 'legR' if x == x0 + w - 1 else 'leg']
        c.tile(t, x, y, 1); c.g[y][x] = ',' if x in stairs else '#'; c.taken[y][x] = True


def walkway(c, x0, x1, y):
    """A 2-wide raised plank walkway (rows y, y+1) between x0..x1, open at both ends; stilts below."""
    for x in range(x0, x1 + 1):
        c.tile(DECK['T'], x, y, 1); c.tile(DECK['B'], x, y + 1, 1); c.taken[y][x] = c.taken[y + 1][x] = True
        if c.g[y][x] != '~': c.g[y][x] = ','
        if c.g[y + 1][x] != '~': c.g[y + 1][x] = ','
        if c.g[y + 2][x] != '~': c.tile(DECK['leg'], x, y + 2, 1); c.g[y + 2][x] = '#'; c.taken[y + 2][x] = True


def garland(c, x0, x1, y, seed=0):
    for i, x in enumerate(range(x0, x1 + 1)):
        if c.inb(x, y): c.tile(GARL[(i + seed) % 4 if (i + seed) % 5 else 2], x, y, 2)


def build():
    c = Village(W, H, 120)
    c.hills([(37, 10, 11, 7, 1, 2)], base=0)
    def sx(y): return 9 + int(round(2.6 * math.sin(y / 6.5) + 1.8 * (vnoise(0, y, 6, 6.0) - 0.5)))
    for y in range(H):
        for x in range(W):
            if y < 3: c.ht[y][x] = max(c.ht[y][x], 0)
            if 0 <= x - sx(y) <= 2 or ((x - 16) / 5.0) ** 2 + ((y - 47) / 3.5) ** 2 < 1.0 + 0.4 * (vnoise(x, y, 7, 3.0) - 0.5):
                c.ht[y][x] = -1; c.g[y][x] = '~'
    c.notch(35, 37, 17, 1)
    # ---- old-growth border (forest biome), ragged inner edge
    for y in range(H):
        for x in range(W):
            edge = min(x, W - 1 - x, y, H - 1 - y)
            if edge < 4 + 3.5 * vnoise(x, y, 11, 6.0) and c.g[y][x] == '.': c.g[y][x] = 'T'
    # ---- lanes: the Gossamer lane bends around the boles, the green sits off-centre, no straight cross
    c.rect(34, 60, 4, 4, 'd', '.T')
    c.lane([(35.5, 63), (35, 58), (31, 53), (30, 47), (33, 42), (38, 38)], 'd', 1, only='.T')
    c.blob(41, 36, 6, 3.6, 'd', 2, only='.', rough=1.0); c.blob(41, 36, 2.6, 1.6, 'k', 3, only='d')
    c.lane([(0, 30.5), (6, 30.5)], 'd', 4, only='.T')
    c.lane([(15, 31), (21, 33), (26, 37), (30, 41)], 'd', 5, only='.T')
    c.lane([(44, 34), (50, 32), (57, 33), (63, 31), (69, 31)], 'd', 6, only='.T')
    c.lane([(39, 33), (37, 27), (36.5, 21)], 'd', 7, only='.')
    c.lane([(21, 33), (20, 28), (19.5, 26)], 'd', 8, only='.')
    c.lane([(31, 50), (36, 51), (40, 50)], 'd', 9, only='.T')
    c.lane([(37, 39), (44, 30), (45.5, 27)], 'd', 10, only='.', r=0.8)
    c.lane([(50, 41), (57, 44), (59, 47)], 'd', 11, only='.', r=0.8)
    c.lane([(33, 13), (27, 14), (23, 14)], 'd', 12, only='.')
    c.rect(32, 15, 9, 2, 'k', '.')
    c.stairs(35, 17)
    c.cliffs(face=2, keep='~')
    for y in range(H):
        for x in range(W):
            if c.g[y][x] == 'C' and c.ht[y][x] < 0: c.g[y][x] = '~'; c.taken[y][x] = False
    # ---- raised decks and the walkway over the stream (the Route 3 road crosses on it)
    walkway(c, sx(30) - 3, sx(31) + 5, 30)
    deck(c, 24, 26, 7, 5, stairs=(26, 27))                         # the weavers' deck, beside the Guildhall tree
    deck(c, 50, 51, 7, 4, stairs=(52, 53), open_sides='E')       # the lantern decks, south-east
    walkway(c, 57, 59, 52)
    deck(c, 60, 51, 6, 4, stairs=(), open_sides='W')
    # ---- the giant trees: one enormous elder (the Loomhouse), boles of every size
    d = {}
    d['gym'] = c.stamp('g_elder', 30, 4, 'BW_GYM', 'Gym door', force=True)
    d['guild'] = c.stamp('g_tree6', 15, 19, 'BW_GUILD', 'Guildhall door', force=True)
    d['house1'] = c.stamp('g_tree4', 52, 21, 'BW_HOUSE1', 'Treetop House door', force=True)
    d['house2'] = c.stamp('g_tree4', 38, 43, 'BW_HOUSE2', "Cutter's House door", force=True)
    d['pc'] = c.stamp('w_house_r', 42, 21, 'BW_PC', 'Poke Center door', force=True)
    d['mart'] = c.stamp('w_house_s', 23, 37, 'BW_MART', 'Mart door', force=True)
    d['chapel'] = c.stamp('w_house_m', 55, 37, 'BW_CHAPEL', 'Chapel door', force=True)
    for nm, x, y in (('g_tree4p', 24, 6), ('g_tree4p', 43, 6), ('g_tree6', 59, 9), ('g_tree4', 4, 21), ('g_tree6', 50, 44),
                     ('g_tree4p', 61, 44), ('g_tree2', 26, 47), ('g_tree2', 44, 47), ('g_tree2', 20, 52), ('g_tree4p', 41, 54),
                     ('g_tree2', 47, 14), ('g_tree2', 20, 9), ('g_tree2', 64, 24), ('g_tree2', 15, 38), ('g_tree2', 57, 28),
                     ('g_tree2', 29, 22), ('g_tree4p', 8, 41), ('g_tree2', 63, 37), ('g_tree2', 33, 30)):
        c.stamp(nm, x, y, force=True)
    for k, dd in d.items():
        for dy in (1, 2):
            if c.g[dd[1] + dy][dd[0]] in '.,T': c.g[dd[1] + dy][dd[0]] = 'd' if k != 'gym' else 'k'
    for x, y in ((d['pc'][0] + 1, d['pc'][1] - 1), (d['mart'][0] + 1, d['mart'][1] - 1)):
        c.tile(STAMPS['hs_jonquil_28']['layers'][1][0][0] or STAMPS['hs_jonquil_28']['layers'][2][0][0], x, y, 2)
    c.stamp('p_banner', d['pc'][0] + 2, d['pc'][1] - 1, force=True); c.stamp('p_banner', d['mart'][0] + 2, d['mart'][1] - 1, force=True)
    c.stamp('p_banner3', d['chapel'][0] + 2, d['chapel'][1] - 2, force=True)
    # rope bridges between crowns overhead, silk awnings over tree doors
    rope(c, 41, 42, 10); rope(c, 28, 29, 10); rope(c, 23, 26, 22); rope(c, 58, 61, 46); rope(c, 47, 50, 46)
    for k in ('guild', 'house1', 'house2'):
        c.stamp('p_awning', d[k][0] - 1, d[k][1] - 2, force=True)
    # ---- events (all from the script)
    E = []
    P = lambda n, at, **kw: E.append(SE.place(120, n, at, **kw))
    P('To Gossamer Wood', (35, 63)); P('To Gossamer Wood b', (36, 63))
    P('Arrival', (34, 62)); P('Juno (arrival)', (36, 61)); P('Stage manager', (37, 62))
    gx, gy = d['gym']
    for dy in range(3):                                            # the Loyal Three shrine: a carved stone idol
        for dx in range(2):
            c.tile(8288 + dy * 8 + dx, 23 + dx, 12 + dy, 1 if dy else 2); c.taken[12 + dy][23 + dx] = True; c.g[12 + dy][23 + dx] = '#'
    P('Loomhouse sign', (gx + 2, gy + 1)); P('Old woman at the shrine', (24, 15)); P('Loyal Three shrine', (23, 14)); P('Dusk petal', (25, 14))
    P('Lattice pylon', (68, 30)); P('Survey flags', (66, 33))
    for i, (x, y) in enumerate(((63, 30), (63, 31), (63, 32))): P('Pylon watch %d' % (i + 1), (x, y))
    P('Pallbearer Thistle', (66, 31)); P('Bereaved 1', (65, 29)); P('Bereaved 2', (66, 32))
    P('Tamsin (square)', (43, 35)); P('Festival poster', (40, 34)); P('Charcoal child', (40, 35))
    P('Weaver at loom', (28, 28)); P('Silk racks', (25, 27)); P('HiddenItem rope bridge', (24, 23))
    P('HiddenItem dye vats', (13, 36))
    for e in E: c.taken[e['at'][1]][e['at'][0]] = True
    S = lambda n, ax, ay, on='dk', r=8: P(n, c.snap(ax, ay, on, r=r))
    S('Town sign', 34, 58); S('Finch', 58, 34); S('Rope-bridge Boy', 24, 34); S('Grandmother knitting', 45, 39)
    town = [('Dyer', 16, 35), ('Apprentice', 21, 30), ('Silk Merchant', 38, 39), ('Meridian Linesman', 60, 32), ('Tired Mother', 31, 48),
            ('Old Man on bridge', 6, 31), ('Girl in ogre mask', 35, 37), ('Boy in dog mask', 36, 38), ('Egg-seller', 43, 38),
            ('Tax-barge Deserter', 33, 54), ('Accord Chaplain', 56, 43), ('Youngster', 46, 31), ('Woman with basket', 47, 40),
            ("Cutter's Wife", 38, 51)]
    for n, x, y in town: S(n, x, y)
    missing = SE.unplaced(120)
    if missing: raise SystemExit('briarwick: script events not placed: %s' % missing)
    # ---- dye works on the stream, looms on the deck, silk and lanterns everywhere
    c.dress(['p_vat_b', 'p_vat_r', 'p_vat_y'], 9, '.', 1, (12, 33, 22, 44), pad=0)
    c.dress(['tp_stall_05', 'tp_stall_06', 'tp_stall_20', 'tp_stall_21', 'p_laundry', 'tp_stall_08'], 8, '.', 2, (12, 18, 34, 50))
    for x, y in ((29, 27), (25, 29)): c.stamp('p_loom', x, y, force=True)
    for x, y in ((52, 51), (61, 52), (64, 51)): c.stamp('p_lantern', x - 1, y, force=True)
    for nm, x, y in (('tp_stall_13', 54, 52), ('t_barrel', 50, 52), ('tp_barrel_06', 62, 53), ('p_silk', 65, 51), ('t_bench', 56, 53),
                     ('tp_stall_05', 26, 26), ('tp_barrel_06', 30, 29), ('tp_garden_09', 41, 35)):
        c.stamp(nm, x, y, force=True)        # life on the decks; the well on the green
    c.dress(['p_silk', 'p_silk1', 'p_strand_w', 'p_strand_p', 'p_silk1'], 26, '.', 4, pad=0)
    c.dress(['p_web', 'p_web1'], 14, '.T', 5, pad=0)
    c.dress(['p_lantern'], 34, '.', 6, near='dk')
    c.dress(GARDEN + ['p_crates', 'tp_stall_13', 't_barrel', 'tp_stall_01', 'fo_rustic_20', 'fo_rustic_22'], 30, '.', 7, pad=0)
    c.dress(['p_cherry', 'p_pinkbush', 'p_pinkbush2', 'fo_fairy_05'], 10, '.', 8)
    c.dress(['t_bench'], 3, 'k', 9, pad=0); c.dress(['p_banner3', 'p_banner'], 5, '.', 10, near='d', pad=0)
    # silk strung overhead across the lanes (layer 3), lanterns hanging in it
    for x0, x1, y, sd in ((31, 47, 33, 0), (27, 35, 44, 1), (40, 49, 26, 2), (17, 23, 29, 3), (52, 62, 35, 1), (29, 39, 57, 2),
                          (49, 57, 40, 3), (31, 41, 19, 0)):
        garland(c, x0, x1, y, sd)
    c.meadow(0.74, 1)
    c.greenfill(0.47, 1, beds=0.06)
    c.sea_rocks(4)
    c.events = E
    head = {'id': 120, 'name': 'Briarwick', 'parent': 0, 'bgm': 'Lappet Town', 'palette': 'village', 'rubric': True, 'yards_ok': True,
            'metadata': {'Outdoor': True, 'ShowArea': True, 'MapPosition': [0, 12, 22], 'BattleBack': 'forest'},
            'tone': [-18, -30, 4, 12], 'fog': {'name': 'prismfall_spores', 'opacity': 46, 'blend': 1, 'zoom': 100, 'sx': 1, 'sy': -1},
            'connections': [{'dir': 'W', 'offset': 29, 'to': 540, 'to_offset': 10}]}
    import yaml
    src = yaml.safe_load(open(os.path.join(HERE, 'layouts', 'briarwick_events.yaml')))[120]['head']
    for k in ('bgm', 'metadata', 'field', 'display_name'):
        if k in src: head[k] = src[k]
    c.write('120_briarwick.yaml', head, '# Briarwick (120). WRITTEN BY layouts/briarwick.py - edit that script.\n', mirror_max=0.6)
    print('doors', d)
    return d


if __name__ == '__main__':
    build()
