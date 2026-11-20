#!/usr/bin/env python3
"""Ebbmouth (160) and Ebbmouth - Mill Quay (167), map builder 10 (job 5: the last stock FRLG town re-skinned).
PF Rejuv tileset 52 "PF Rejuv Snow" with the Rimewood kit (layouts/rimewood.py): Isenmar's southern port where the River
Ebb meets the sea, in a late-winter thaw - sleet, slush lanes, whalebone longhouses under snow, the river open and black.

  160 Ebbmouth (60x54): the Ebb comes down from the Mill Quay (N edge) between the towpath and the east bank, through the
      Tidelock (the gym's lock gates, a footway on top), under the Market Bridge, past the Guild Mill's wheel and the brass
      Meridian intake that squats at its mouth, into the harbour basin (quays, cranes, the fish market, boats) and out
      past the breakwater light to the sea; beyond, the sea is still frozen in pressure ridges.  West bank: the upper
      town on its terrace (Reyes house, the net-mender), the market with smoked-eel stalls and the Ebb Guild's hall, the
      Anglers' Guild, the Center and the Exchange; the coast road south to Gullcry Cliffs (561).
  167 Ebbmouth - Mill Quay (40x30): the tidal mills: three wheels on the quay under the union halls, the Mill Quay
      steps down to the black water, strikers' braziers, sacks and carts; reached up the towpath from 160.
Links: EB_PC, EB_MART, EB_ANGLER, EB_REYES, EB_HOUSE, EB_GYM, EB_NETLOFT (unchanged; interiors in 161/168/170).
Run: python3 -I layouts/ebbmouth.py && python3 -I build.py 160 167"""
import os, sys, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import rkit as K
from rkit import STAMPS
from terrain import vnoise
import rimewood as RW
from rimewood import snowmap, apron, doorstep, smooth, npc, sign, item, seat, signboard, head, over_tiles, bridges, ice, dress_ice, \
    road_tracks, drifts, reed_beds, lagoon

PREV = '--preview' in sys.argv
CONN160 = [{'dir': 'S', 'offset': 22, 'to': 561, 'to_offset': 12}, {'dir': 'N', 'offset': 0, 'to': 167, 'to_offset': 0}]
CONN167 = [{'dir': 'S', 'offset': 0, 'to': 160, 'to_offset': 0}]
TOW = (28, 31)                     # the towpath columns: the crossing between 160 and 167


def river_x(y, base=34.5, amp=1.4, per=7.0):
    return base + amp * math.sin(y / per)


def wheel(m, name, x, y):
    """a mill-wheel standing in the race (after paint: its tiles go on layer 3 over the water)"""
    over_tiles(m, name, x, y, z=2)


def obj(at, name, lines):
    return {'type': 'event', 'name': name, 'at': list(at), 'pages': [{'trigger': 'action', 'commands': list(lines)}]}


# ====================================================================================================== 160
def build_160():
    W, H = 60, 54
    m = snowmap(W, H, 160)
    rng = random.Random(160)
    # ---- the river, the harbour basin, the sea and its frozen reach
    for y in range(0, 40):
        c = river_x(y)
        for x in range(int(c - 2.6), int(c + 3.4)): m.cls[y, x] = 'w'
    m.blob(44, 41.5, 14.5, 5.0, 'w', seed=161, rough=0.35)                       # the harbour basin
    for y in range(44, H):                                                       # the sea, south-east of the coast road
        for x in range(W):
            coast = 27 + 3 * vnoise(0, y, 162, 5.0) - (y - 44) * 0.15
            if x >= coast: m.cls[y, x] = 'W'
    for y in range(36, 44):
        for x in range(26, W):
            if m.cls[y, x] == 'w' and y >= 42: m.cls[y, x] = 'W'
    for y in range(46, H):                                                       # the frozen reach beyond the breakwater
        for x in range(46, W):
            if m.cls[y, x] == 'W' and x >= 49 + 3 * vnoise(0, y, 163, 4.0) - (y - 46) * 0.4: m.cls[y, x] = 'o'
    lagoon(m, 0.62, seed=164)
    # ---- the upper town terrace (h1) in the north-west; woods and fjord rock round the edges
    for y in range(H):
        for x in range(W):
            if x <= 25 + 1.5 * vnoise(0, y, 165, 4.0) and y <= 12 + 1.2 * vnoise(x, 0, 166, 5.0): m.ht[y, x] = 1
    for y in range(H):
        for x in range(W):
            if m.cls[y, x] != '.': continue
            west = x <= 1 + 1.5 * vnoise(0, y, 167, 4.0) and 13 < y < 44
            north = y <= 1 + 1.2 * vnoise(x, 0, 168, 4.0) and not (TOW[0] <= x <= TOW[1])
            ne = x >= 50 + 3 * vnoise(0, y, 169, 5.0) and y <= 14 - 3 * vnoise(x, 0, 170, 5.0)
            east = x >= W - 2 - 1.5 * vnoise(0, y, 171, 4.0) and y < 36
            sw = x <= 4 + 6 * vnoise(0, y, 172, 6.0) and y >= 44
            if west or north or ne or east or sw: m.cls[y, x] = 'T'
    # ---- stairs and lanes (packed snow, trodden to slush)
    m.stairs(19, 12, w=3, kit_rows=4)                                            # the Net Steps, upper town to the market
    m.plan_cliffs()
    m.rect(TOW[0], 0, 4, 18, 'd', only='.T')                                     # the towpath up to the Mill Quay
    m.lane([(29.5, 17), (27, 22), (22, 26)], 'd', 2.6, seed=71, wobble=0.4)
    m.lane([(4, 9), (12, 10.2), (20, 10.6), (24, 9.6)], 'd', 2.2, seed=72, wobble=0.4)           # the upper town walk
    m.lane([(20.5, 16), (20, 21), (19, 26)], 'd', 2.4, seed=73, wobble=0.4)
    m.blob(15, 27.5, 9.5, 4.0, 'd', seed=74, rough=0.35, only='.T')              # the market square
    m.lane([(6, 24), (12, 26.5)], 'd', 2.2, seed=75, wobble=0.3)
    m.lane([(23, 29), (29, 29.5), (33, 29.5)], 'd', 3.0, seed=76, wobble=0.0, only='.T')        # to the Market Bridge
    m.lane([(38, 29.5), (44, 30), (50, 32), (55, 35)], 'd', 2.8, seed=77, wobble=0.4)          # east bank: to the quays
    m.lane([(42, 18.5), (45, 22), (44, 29)], 'd', 2.4, seed=78, wobble=0.4)
    m.lane([(15, 31), (16, 36), (21, 40), (21.5, 46), (21.5, 54)], 'd', 3.4, seed=79, wobble=0.3)  # the coast road south
    m.lane([(6, 36), (12, 37.5), (17, 37)], 'd', 2.2, seed=80, wobble=0.3)
    m.lane([(24, 37.5), (29, 38.5)], 'd', 2.4, seed=81, wobble=0.2)
    m.rect(20, 50, 4, 4, 'd', only='.T')                                         # the crossing to Gullcry Cliffs (x 20-23)
    smooth(m, 'd', into='.', passes=1)
    # the quays round the basin (packed snow on stone), and the breakwater out to the light
    for y in range(32, 40):
        for x in range(38, W):
            if m.cls[y, x] in '.T' and any(m.inb(x + dx, y + dy) and m.cls[y + dy, x + dx] == 'w' for dx in (-1, 0, 1) for dy in (-1, 0, 1, 2)):
                m.cls[y, x] = 'd'
    for i, (x, y) in enumerate([(57, 38), (56, 40), (55, 42), (53, 44), (51, 45), (49, 46)]):
        for dx in (0, 1, 2):
            for dy in (0, 1):
                if m.inb(x + dx, y + dy): m.cls[y + dy, x + dx] = 'd'
    for x in range(55, W):
        for y in range(36, 39): m.cls[y, x] = 'd'
    # ---- buildings: whalebone longhouses under snow
    d = {}
    d['reyes'] = m.stamp('wb_short', 3, 3, 'EB_REYES', 'Reyes House door')
    d['house'] = m.stamp('wb_hut', 12, 4, 'EB_HOUSE', "Net-mender's House door")
    m.stamp('kf_aframe', 18, 2, None, 'x')
    d['pc'] = m.stamp('wb_pc', 3, 15, 'EB_PC', 'Poke Center door')
    d['mart'] = m.stamp('wb_long', 9, 18, 'EB_MART', 'Mart door') if False else m.stamp('wb_long2', 12, 16, 'EB_MART', 'Mart door')
    d['angler'] = m.stamp('wb_long3', 2, 30, 'EB_ANGLER', "Anglers' Guild door")
    m.stamp('wb_inn', 22, 20, None, 'x')                                          # the Ebb Guild's hall (no interior)
    d['gym'] = m.stamp('wb_inn', 40, 8, 'EB_GYM', 'Tidelock Gym door')
    d['loft'] = m.stamp('wb_long3', 45, 21, 'EB_NETLOFT', 'Net Loft door')
    m.stamp('wb_smoke', 4, 38, None, 'x')                                         # the eel smokery
    m.stamp('wb_long', 38, 24, None, 'x') if False else None
    m.stamp('wb_short', 39, 1, None, 'x')                                         # the Upper Mill house (east bank)
    m.stamp('kf_aframe', 25, 33, None, 'x')                                       # the Guild Mill house (west bank)
    m.events = [e for e in m.events if e.get('name') != 'x']
    for k, (dx, dy) in d.items(): doorstep(m, (dx, dy)); apron(m, (dx, dy))
    # ---- yards, market, quays
    for nm, x, y in (('fw_stall_i', 10, 25), ('fw_stall_e', 14, 25), ('fw_stall_i', 18, 26), ('fw_stall_e', 9, 29), ('fw_rack', 12, 31),
                     ('fw_rack', 15, 31), ('pf_logbench', 17, 30), ('fw_brazier', 21, 27), ('fw_brazier', 8, 27), ('fw_wood', 22, 31),
                     ('sh_crates', 31, 20), ('fw_sled', 24, 27), ('hb_crane', 47, 31), ('hb_crane', 54, 33), ('hb_crates4', 50, 34),
                     ('hb_barrels', 41, 33), ('hb_fishstall', 39, 34) if False else ('hb_tubs', 44, 34), ('hb_rope', 57, 35),
                     ('fw_rack', 6, 44), ('fw_rack', 9, 44), ('fw_wood', 13, 43), ('fw_skull', 16, 44), ('fw_boat_over', 10, 47),
                     ('sh_crates', 26, 11), ('fw_rack', 9, 9) if False else ('fw_wood', 8, 10), ('fw_sled', 16, 9),
                     ('fw_brazier', 34, 23) if False else ('fw_brazier', 31, 26), ('hb_barrel', 43, 18), ('hb_cask', 50, 18),
                     ('pf_lantern', 23, 15), ('pf_lantern', 12, 23), ('pf_lantern', 27, 29), ('pf_lantern', 40, 28), ('pf_lantern', 52, 29),
                     ('pf_lantern', 18, 36), ('pf_lantern', 23, 45), ('pf_lantern', 10, 12), ('pf_lantern', 31, 8), ('pf_lantern', 46, 19)):
        m.near(nm, x, y, on='.d', r=3)
    m.stamp('pf_wlamp', 49, 45) if m.free(49, 45, 1, 3, on='d') else m.near('pf_wlamp', 50, 44, on='d', r=2)   # the breakwater light
    for cx, cy, n in ((6, 12, 2), (24, 5, 1), (2, 26, 1), (14, 40, 2), (8, 50, 3), (31, 14, 1), (56, 20, 2), (52, 26, 1), (36, 47, 0)):
        if n: m.trees(cx, cy, n, ['pine2', 'kf_tree', 'pine2'], r=2, on='.', seed=cx * 7 + cy)
    # ---- events
    E = [sign((22, 17), 'Gym sign', "TIDELOCK GYM\nWarden: Marisol Reyes - The Ebb runs both ways."),
         sign((24, 46), 'Town sign', "EBBMOUTH\nWhere the Ebb meets the sea. Southern port of Isenmar."),
         sign((27, 40), 'Lattice sign', "MERIDIAN TIDAL LATTICE - UNIT 2\nPowering Isenmar's future. Keep off the intake."),
         sign((30, 2), 'Towpath sign', "THE TOWPATH - up the Ebb to the Mill Quay. Mind the ropes: the river pulls both ways."),
         sign((9, 22), 'PC sign', "POKEMON CENTER"),
         obj((33, 3), 'Upper mill', ["The Upper Mill's wheel turns, stops dead, and turns again. The miller's boy counts under his breath: 'nine... ten... go on, go on...'"]),
         obj((29, 35), 'Guild mill', ["The Guild Mill. Its race runs past Meridian's brass intake. When the river stutters the wheel freezes mid-turn and the whole quay holds its breath."]),
         obj((52, 37), 'Harbour mast', ["A whaler's mast at the quay, its yard hung with nets. Gulls have opinions about it."]),
         npc((10, 33), 'Ice-fisher', 'trainer_FISHERMAN', ["♪ Sleep, old whale, under the ice... When the whale wakes, the sea remembers it's a sea. ♪"], d='up'),
         npc((19, 23), 'Guild striker', 'NPC 03', ["Ebb Guild: Thane Eirik taxes our catch, Meridian lays us off. And the river stops dead for minutes now!"], move='random'),
         npc((49, 36), 'Dockworker', 'trainer_SAILOR', ["Watch the mill-wheels. When the Ebb stutters they freeze mid-turn and we all hold our breath."], d='left'),
         npc((23, 23), 'Guild organiser', 'NPC 27', ["Guild organiser: Strike vote's at the bell. Marisol says she's 'neutral'. Marisol has never been neutral about anything in her life."]),
         npc((13, 29), 'Eel-smoker', 'NPC 20', ["Smoked eel! Smoked char! Smoked anything you hold still long enough!", "The Warden buys two every night after a gym fight. Win or lose. Mostly win."]),
         npc((43, 20), 'Lock-keeper', 'NPC 25', ["Lock-keeper: The Tidelock lifts boats up the Ebb when the tide's in and lets them down when it's out.",
                                                 "Lately the river doesn't know which it is. Neither do the gates."], d='down'),
         npc((36, 36), 'Meridian surveyor', 'NPC 12', ["Meridian surveyor: The stutters are within tolerance. Everything is within tolerance. Please stop asking."], d='left'),
         npc((17, 41), 'Child with a toy boat', 'NPC 07', ["I race my boat down the race! When the river stops, it stops too. Then it's a draw."], move='random'),
         npc((56, 34), 'Old whaler', 'NPC 28', ["Forty winters on the ice. You don't hear the sea under it. You FEEL it. Lately it's been turning over in its sleep."], d='down'),
         {'type': 'npc', 'name': 'Gull', 'at': [45, 37], 'sprite': 'Followers/WINGULL', 'dir': 'left', 'move': 'random', 'text': '(Kyaa! It eyes your bag.)'},
         item((58, 44), 'NETBALL', True), item((3, 47), 'FRESHWATER')]
    E = seat(m, E, on='.d')
    for e in E:
        if e['type'] == 'sign': signboard(m, e)
    teo_page = OLD160_TEO
    E.append(dict(teo_page, at=list(seat(m, [{'at': [30, 33], 'type': 'x'}], on='.d')[0]['at'])))
    m.greenfill(3)
    m.events = [e for e in m.events if e['type'] == 'door'] + E
    m.paint()
    bridges(m, ((28, 30),), cls='w')                                             # the Market Bridge
    bridges(m, ((16, 17),), cls='w')                                             # the lock gates' footway (the Tidelock)
    for x in range(m.W):                                                         # sluice paddles at the lock ends
        for y in (15, 18):
            if m.cls[y, x] == 'w' and m.cls[y - 1 if y == 15 else y + 1, x] == 'w' and (x % 2 == 0):
                over_tiles(m, 'df_sluice', x, y - 1 if y == 15 else y, z=2)
    wheel(m, 'eb_wheel0', int(river_x(4)) - 1, 2)                                # the Upper Mill's wheel
    wheel(m, 'eb_wheel1', int(river_x(33)) - 2, 32)                              # the Guild Mill's wheel
    over_tiles(m, 'eb_intake', 26, 37)                                           # Meridian's brass intake at the river mouth
    for nm, x, y in (('hb_boat1', 40, 39), ('hb_boat3', 46, 41), ('fw_boat', 33, 41), ('hb_boat2', 52, 39), ('fw_boat', 37, 44)):
        L = np.array(STAMPS[nm]['layers'])
        if all(m.inb(x + i, y + j) and m.cls[y + j, x + i] in 'wW' and m.L[2, y + j, x + i] == 0 for i in range(L.shape[2]) for j in range(L.shape[1])):
            for j in range(L.shape[1]):
                for i in range(L.shape[2]):
                    t = int(L[:, j, i].max())
                    if t: m.L[2, y + j, x + i] = t
    ice(m)
    dress_ice(m, 0.28, seed=160)
    reed_beds(m, 10, seed=160)
    for nm, x, y in (('fw_smoke_w', 6, 36), ('fw_smoke_w', 24, 18), ('fw_smoke_w', 6, 1), ('fw_smoke_w', 43, 4), ('fw_smoke_w', 50, 19)):
        over_tiles(m, nm, x, y)
    m.scatter(5, seed=160)
    road_tracks(m, 0.08, seed=160)
    drifts(m, 0.06, seed=160)
    m.seal_against(CONN160, spans=[('S', 20, 4), ('N', TOW[0], 4)], keep=[tuple(e['at']) for e in m.events if e.get('type') == 'warp'])
    if PREV: m.preview('/tmp/craft/e160.png', 0.5)
    m.write(160, head(160, 'Ebbmouth', biome='village', bgm='Lerucean Town',
                      metadata={'Outdoor': True, 'ShowArea': True, 'MapPosition': [0, 8, 20], 'BattleBack': 'field', 'Weather': ['Rain', 30]},
                      tone=[-6, -4, 6, 18], fog={'name': 'prismfall_seamist', 'opacity': 40, 'blend': 0, 'zoom': 100, 'sx': 1, 'sy': 0},
                      connections=CONN160, _file='160_ebbmouth.yaml'),
            '# Ebbmouth (160). WRITTEN BY layouts/ebbmouth.py (map builder 10, PF Rejuv Snow) - edit that script.\n'
            '# The old stock-palette version is layouts/old_160_ebbmouth.yaml.\n')
    print('ebbmouth doors', d)


# ====================================================================================================== 167
def build_167():
    W, H = 40, 30
    m = snowmap(W, H, 167)
    for y in range(0, H):                                                        # the Ebb, lined up with 160's at the seam
        c = river_x(y + 54 * 0, base=34.5 - (H - 1 - y) * 0.12)
        for x in range(int(c - 2.6), int(c + 3.4)):
            if m.inb(x, y): m.cls[y, x] = 'w'
    m.blob(30, 8, 5.0, 3.0, 'w', seed=171, rough=0.35)                           # the mill pond above the head-race
    for y in range(H):
        for x in range(W):
            if m.cls[y, x] != '.': continue
            if y <= 2 + 1.5 * vnoise(x, 0, 172, 4.0) or x <= 1 + 1.2 * vnoise(0, y, 173, 4.0) or (x >= 38 and y < 26): m.cls[y, x] = 'T'
    for y in range(H):                                                           # the union halls stand on a raised bank (h1)
        for x in range(W):
            if x <= 18 + 1.0 * vnoise(0, y, 174, 4.0) and y <= 12: m.ht[y, x] = 1
    m.stairs(14, 12, w=3, kit_rows=4)
    m.plan_cliffs()
    m.rect(TOW[0], H - 10, 4, 10, 'd', only='.T')                                # the towpath from 160
    m.lane([(29.5, 21), (26, 18), (20, 17.5), (8, 18), (3, 20)], 'd', 3.0, seed=175, wobble=0.4)   # the Mill Quay
    m.lane([(15.5, 16), (15.5, 12)], 'd', 2.6, seed=176, wobble=0.1)
    m.lane([(4, 9), (10, 10), (18, 9.5)], 'd', 2.4, seed=177, wobble=0.3)
    m.lane([(10, 19), (9, 25), (12, 28)], 'd', 2.2, seed=178, wobble=0.3)
    m.lane([(27, 21), (27, 26)], 'd', 2.0, seed=179, wobble=0.1)
    smooth(m, 'd', into='.', passes=1)
    # the Mill Quay steps: a stair down the quay face to the water (the river note's place)
    for y in (22, 23):
        for x in (24, 25): m.cls[y, x] = 'd'
    E = []
    m.stamp('wb_long3', 3, 4, None, 'x'); m.stamp('wb_long', 14, 3, None, 'x')    # the union halls (no interiors)
    m.stamp('kf_aframe2', 20, 10, None, 'x') if False else m.stamp('kf_aframe', 22, 11, None, 'x')   # the tide mill
    m.stamp('wb_hut', 3, 22, None, 'x')
    m.events = [e for e in m.events if e.get('name') != 'x']
    for nm, x, y in (('fw_brazier', 12, 17), ('fw_brazier', 22, 19), ('sh_crates', 18, 20), ('hb_barrels', 6, 16), ('fw_sled', 8, 20),
                     ('hb_crates4', 20, 22), ('fw_wood', 4, 27), ('fw_rack', 15, 23), ('pf_lantern', 10, 15), ('pf_lantern', 26, 16),
                     ('pf_lantern', 30, 24), ('hb_cask', 25, 15), ('sh_campfire', 7, 13), ('pf_logbench', 9, 12)):
        m.near(nm, x, y, on='.d', r=3)
    for cx, cy, n in ((6, 26, 2), (19, 27, 1), (35, 27, 1)):
        m.trees(cx, cy, n, ['pine2', 'kf_tree'], r=2, on='.', seed=cx + cy)
    E += [obj((27, 17), 'Mill Quay wheel sign', ["THE MILL QUAY WHEEL. Cast 'EBB GUILD - AF 198'. Below the date somebody has scratched: 'AND STILL TURNING'."]),
          sign((30, 26), 'Quay sign', "THE MILL QUAY - Ebb Guild tidal mills. No Meridian vehicles past this sign. (By order of the Guild. And Bjorn.)"),
          npc((12, 18), 'Striker', 'NPC 03', ["Striker: No grain moves till the Thane drops the tax. No wheel turns till Meridian stops stopping it. Simple."], move='random'),
          npc((20, 18), 'Striker 2', 'NPC 21', ["Striker: My dad milled here. His dad milled here. Meridian says 'efficiency'. I say 'my dad'."]),
          npc((8, 10), 'Union steward', 'NPC 25', ["Union steward: Every hall on the quay votes. Even the Wooloo-shearers, and they're not even from here."]),
          npc((26, 23), 'Miller', 'NPC 28', ["Miller: Listen. Under the wheel. When the river stops, you can hear something down there. Like a note held too long."], d='right'),
          npc((5, 19), 'Carter', 'NPC 20', ["Carter: Grain to the harbour, salt back up. When the river stops, the carts are all Ebbmouth has."]),
          item((36, 28), 'SUPERPOTION'), item((2, 15), 'HEARTSCALE', True)]
    E = seat(m, E, on='.d')
    for e in E:
        if e['type'] == 'sign': signboard(m, e)
    m.greenfill(3)
    m.events = [e for e in m.events if e['type'] == 'door'] + E
    m.paint()
    for i, (x, y) in enumerate(((30, 12), (31, 18), (32, 24))):                   # three tide-mill wheels down the race
        cx = int(river_x(y, base=34.5 - (H - 1 - y) * 0.12)) - 3
        wheel(m, 'eb_wheel%d' % (i % 2), max(cx, 28), y)
    for y in (22, 23):                                                           # the steps down to the water
        for i, x in enumerate((24, 25)):
            m.L[2, y, x] = m.STAIRS[0 if i == 0 else 2]
    ice(m)
    dress_ice(m, 0.2, seed=167)
    for nm, x, y in (('fw_smoke_w', 6, 2), ('fw_smoke_w', 17, 1), ('fw_smoke_w', 24, 9)): over_tiles(m, nm, x, y)
    m.scatter(5, seed=167)
    road_tracks(m, 0.08, seed=167)
    drifts(m, 0.06, seed=167)
    m.seal_against(CONN167, spans=[('S', TOW[0], 4)])
    if PREV: m.preview('/tmp/craft/e167.png', 0.5)
    m.write(167, head(167, 'Ebbmouth - Mill Quay', biome='village', bgm='Lerucean Town', parent=160,
                      metadata={'Outdoor': True, 'ShowArea': True, 'MapPosition': [0, 3, 7], 'BattleBack': 'field', 'Weather': ['Rain', 30]},
                      tone=[-6, -4, 6, 18], fog={'name': 'prismfall_seamist', 'opacity': 40, 'blend': 0, 'zoom': 100, 'sx': 1, 'sy': 0},
                      connections=CONN167, _file='167_ebbmouth_mill_quay.yaml'),
            '# Ebbmouth - Mill Quay (167). WRITTEN BY layouts/ebbmouth.py (map builder 10, PF Rejuv Snow) - edit that script.\n')


def _old_teo():
    import yaml
    p = os.path.join(K.HERE, 'layouts', 'old_160_ebbmouth.yaml')
    if not os.path.exists(p):
        import shutil; shutil.copy(os.path.join(K.HERE, 'specs', '160_ebbmouth.yaml'), p)
    d = yaml.safe_load(open(p))
    return [e for e in d['events'] if e.get('name') == 'Teo'][0]


OLD160_TEO = _old_teo()

if __name__ == '__main__':
    a = [x for x in sys.argv[1:] if x.isdigit()] or ['160', '167']
    if '160' in a: build_160()
    if '167' in a: build_167()
