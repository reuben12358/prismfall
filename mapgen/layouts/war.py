#!/usr/bin/env python3
"""The war theatre in Ossaria's western dunes (WORLD.md 9, story/14_WAR_AND_BLESSING.md Part B), map builder 10.
PF Rejuv Shore (tileset 56) with the dune cliff kit (akd), the nature kit and the war kit (ndraw `wr_*`).

Graph (edges; the theatre's own story gates are events):
    920 The Rimed Sands --E/W-- 925 The Steamline --E/W-- 924 Ashkaar Siege Camp
       |S (NW of 926)              |S (the crest)               |S (NE of 926)
       +------------------------ 926 The Glass Dunes ------------+
                                   | S: warp up the goat-path to 929 The Observers' Mesa
                                   E: 930 The Bone-Carters' Camp (E edge: 810 the Dry Tide, not built)
    924's war-tent door -> 928 the Command Pavilion.  920's W edge (921 Skaldfast) is not built: a siege barricade.
Ch19 (the Battle of the Glass Dunes): the PC comes in from 930 onto the Glass Dunes' south flats.  The crest, where the
partner double and the legend wait, is reached only from the Steamline (925 S); 925 from either army's lines.  The gauntlet
runs through the side you did not back (REQUESTS, trainer designer round 3): back Ashkaar -> 920's Isenmar trench-lines,
back Isenmar -> 924's earthworks, stand between -> the Steamline (one soldier per side).  WAR_SIDE_ASH / _ISE / _MID
(S605-607) mirror pf_choice(:war_climax) (each map's "War front" event sets them).

    python3 -I layouts/war.py [920 924 925 926 928 929 930] [--preview]   then   python3 -I build.py <ids>"""
import os, sys, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import rkit as K
from rkit import STAMPS
import routekit as RK
from routekit import Route, trainer, npc, sign, item, hidden, talk, head
import craftkit as CK
from routes_early import obj, P
from terrain import vnoise

PREV = '--preview' in sys.argv
ONE = lambda n: int(np.array(STAMPS[n]['layers']).max())
FRONT = {'type': 'event', 'name': 'War front', 'at': [0, 0], 'fixed': True, 'pages': [{'trigger': 'parallel', 'commands': [
    {'script': "c = (pf_choice(:war_climax) rescue nil)\n$game_switches[605] = (c == :back_ashkaar)\n"
               "$game_switches[606] = (c == :back_isenmar)\n$game_switches[607] = (c == :stand_between)"}, {'wait': 60}]}]}


def desert(W, H, mid, base='u'):
    r = Route(mid, W, H, 'shore', kit={1: 'akd', 2: 'akd', 3: 'akd', 'default': 'akd'}, base=base)
    return r, r.m


def dunes(r, n, seed, box=None, w=(5, 10)):
    """dune crests: one-way sand ledges (their lee faces south, you slide down them) east-west across the sand"""
    m = r.m; rng = random.Random(seed)
    x0, y0, x1, y1 = box or (2, 2, r.W - 2, r.H - 2)
    for i in range(n):
        x = int(rng.uniform(x0, x1)); y = int(rng.uniform(y0, y1)); L = int(rng.uniform(*w))
        if all(m.cls[y, xx] in 'su' and not r.road_mask[y, xx] for xx in range(x, min(r.W - 1, x + L))):
            CK.ledge(r, x, min(r.W - 2, x + L), y, face='dune')


def sand_dress(r, ripple=0.42, seed=0, on='su', bones=0.01):
    """after paint: wind ripples drift across open sand in noise bands, a few old bones; ruts along the roads"""
    m = r.m; rng = random.Random(r.seed * 3 + seed)
    R = [K.P1('wr_ripple%d' % v) for v in range(3)]; Bn = [K.P1('wr_bones%d' % v) for v in range(2)]
    RU = [K.P1('wr_rut%d' % v) for v in range(2)]
    for y, x in np.argwhere(r.road_mask):
        if m.cls[y, x] in on and not m.L[2, y, x] and not m.taken[y, x] and rng.random() < 0.7: m.L[2, y, x] = RU[(x + y) % 2]
    for y, x in np.argwhere(np.isin(m.cls, list(on))):
        if m.L[2, y, x] or m.cliff[y, x] or r.road_mask[y, x] or m.taken[y, x]: continue
        n = vnoise(x, y, r.seed * 11 + seed, 4.0)
        if n > 1 - ripple - 0.15 and rng.random() < 0.85: m.L[2, y, x] = R[(x // 3 + y) % 3]
        elif rng.random() < bones: m.L[2, y, x] = rng.choice(Bn)


def frozen_ground(r, cells, thr=0.42, seed=0):
    """sand frozen hard by Isenmar's host: the snow-ground variants (ndraw sn_g*) on layer 1 in noise patches"""
    m = r.m; G = [K.P1('sn_g%d' % v) for v in range(4)]
    for x, y in cells:
        if m.inb(x, y) and m.cls[y, x] in 'su' and not m.cliff[y, x] and vnoise(x, y, r.seed + seed, 5.0) > thr:
            m.L[0, y, x] = G[(x * 7 + y * 3) % 4]


def ground_var(r, names, thr=0.45, seed=0, cells=None, scale=4.0):
    """variety under the sand: layer-1 ground variants (salt crust, frost) in noise patches"""
    m = r.m; G = [K.P1(n) for n in names]
    src = cells if cells is not None else [tuple(c[::-1]) for c in np.argwhere(np.isin(m.cls, ['s', 'u']))]
    for x, y in src:
        if m.inb(x, y) and m.cls[y, x] in 'su' and not m.cliff[y, x] and vnoise(x, y, r.seed + 77 + seed, scale) > thr:
            m.L[0, y, x] = G[(x * 5 + y * 3 + int(vnoise(x, y, seed, 1.3) * 7)) % len(G)]


def decal(r, names, p, on='su', seed=0, cells=None):
    m = r.m; rng = random.Random(r.seed * 5 + seed); T = [K.P1(n) for n in names]
    src = cells if cells is not None else [tuple(c[::-1]) for c in np.argwhere(np.isin(m.cls, list(on)))]
    for x, y in src:                                 # never over a prop: a priority-0 decal on top makes it walkable
        if m.inb(x, y) and not m.L[2, y, x] and not m.cliff[y, x] and not m.taken[y, x] and m.cls[y, x] != 'B' and rng.random() < p:
            m.L[2, y, x] = rng.choice(T)


# stand-in charsets from the base project until the sprite artist draws the war classes (maps_out/trainers_needed.txt)
SPRITE = {'ISENMAR_SOLDIER_M': 'trainer_POKEMONRANGER_M', 'ISENMAR_SOLDIER_F': 'trainer_POKEMONRANGER_F', 'ISENMAR_OFFICER': 'trainer_COOLTRAINER_M',
          'ASHKAAR_SOLDIER_M': 'trainer_BLACKBELT', 'ASHKAAR_SOLDIER_F': 'trainer_CRUSHGIRL', 'ASHKAAR_OFFICER': 'trainer_TAMER',
          'LEADER_SIGRUN': 'trainer_ELITEFOUR_Lance', 'LEADER_MARISOL': 'trainer_LEADER_Misty', 'DOMINAR': 'trainer_LEADER_Giovanni'}


def gauntlet(at, cls, name, ver, sw, intro, after, d='down', sight=4):
    """a war trainer who stands only in the gauntlet of the side you did not back (switch sw)"""
    return {'type': 'trainer', 'at': list(at), 'sight': sight, 'dir': d, 'sprite': SPRITE.get(cls, 'trainer_' + cls),
            'trainer': [cls, name, ver], 'intro': intro, 'after': after, 'cond': {'switch': sw}, 'fixed': True}


def soldier(at, name, sprite, lines, d='down', move='fixed', cond=None):
    e = talk(name, at, sprite, lines, d=d, move=move)
    if cond: e['pages'][0]['cond'] = cond
    return e


# ====================================================================================================== 920 The Rimed Sands
def build_920():
    """The Rimed Sands (60x36, DESERT): Isenmar's front in the western dunes.  The road from Skaldfast (W, barricaded:
    921 is not built) runs east through three frozen trench-lines, each a revetment of drystone and burnt sled-forts with
    one sally port, to the Steamline (E); the dunes south of the road are rime-crusted, and a sled-yard of dragged forts
    and blue tents stands behind the first line.  South (NW): down to the Glass Dunes.  Back Ashkaar: an Isenmar soldier
    holds each sally port (the gauntlet)."""
    W, H = 60, 36
    r, m = desert(W, H, 920)
    dunes(r, 9, 920, box=(2, 20, 56, 33))
    dunes(r, 5, 921, box=(2, 3, 56, 9))
    road = [(0, 14.5), (12, 15), (24, 14), (36, 15.5), (48, 14.5), (59, 15)]
    r.road(road, w=3.0, c='u', open_=None, only='su.tT')
    r.road([(10, 16), (8, 24), (8, 35)], w=3.0, c='u', open_=None, only='su.tT')           # south to the Glass Dunes
    r.lane([(30, 16), (31, 22)], w=2.0, c='u', open_=None, only='su.')
    r.exit('W', 13, 4); r.exit('E', 13, 4)
    r.finish_plan(border=1)
    # the three trench-lines: a revetment column x = 18, 32, 46 from the north rim to the south dunes, one sally port each
    ports = {18: 14, 32: 15, 46: 14}
    rev = []
    for x, py in ports.items():
        for y in range(1, H - 1):
            if abs(y - py) <= 1 or m.ht[y, x] != 0 or m.cliff[y, x] or m.cls[y, x] not in 'su': continue
            if (y - py) % 7 == 3 and abs(y - py) > 3: continue                               # (never a gap: blocked by a fort)
            rev.append((x, y))
    E = [FRONT, {'type': 'warp', 'name': 'To the Glass Dunes', 'at': [8, 35], 'link': 'WAR_RIMED_DUNES', 'arrive': [8, 34, 'up'], 'fixed': True},
         sign((3, 12), 'Road sign', "THE RIMED SANDS. W: Skaldfast (under siege: the road is barricaded). E: the Steamline. S: the Glass Dunes."),
         obj('Siege barricade', (1, 17), ['Sledges on their sides, lashed with whale-gut, piled with frozen sand. Skaldfast is two miles west, and burning.']),
         obj('Sled-yard', (12, 6), ['Sled-forts dragged over the Mast Glacier, two hundred miles, on bone runners. Most are burnt black on the eastern side.']),
         soldier((15, 13), 'Isenmar picket', 'NPC 11', ["Isenmar picket: The sand was hot when we got here. We fixed that.",
                                                         "Picket: Our Glaceon froze it a yard deep. You can feel the cold through your boots. That's the line."], d='right'),
         soldier((28, 17), 'Skald', 'NPC 28', ["Skald: I'm here to remember it. Somebody has to, and it may as well be someone who rhymes."]),
         soldier((44, 12), 'Ice-rider', 'NPC 25', ["Ice-rider: My Mamoswine walked over the glacier. It will walk back. I promised it."]),
         obj('Frozen trench', (20, 20), ['A trench cut in sand and frozen hard, its walls glazed white. Someone has carved a tally of days into the ice. It is a long tally.']),
         gauntlet((19, 14), 'ISENMAR_SOLDIER_M', 'Soldier', 0, 'WAR_SIDE_ASH', 'You came with the dragons. You leave without them.',
                  'The line holds behind me. You will see.', d='left'),
         gauntlet((33, 15), 'ISENMAR_SOLDIER_F', 'Soldier', 0, 'WAR_SIDE_ASH', "The Thane said the sand would never be cold. Ask the sand.",
                  'Go, then. Tell them the Rimed Sands were held.', d='left'),
         gauntlet((47, 14), 'ISENMAR_OFFICER', 'Captain', 0, 'WAR_SIDE_ASH', 'Third line. Nobody has passed the third line.',
                  'Somebody has passed the third line. Mark it in the tally.', d='left'),
         item((52, 4), 'ICEBERRY') if False else item((52, 4), 'NEVERMELTICE'), hidden((26, 30), 'STARDUST', 'HiddenItem (rimed dune)'),
         item((5, 28), 'FULLRESTORE')]
    for e in E: e.setdefault('fixed', e['type'] in ('trainer',))
    r.add(*E)
    r.seat_events(on='su')
    for x, y in rev:
        if not m.taken[y, x] and m.cls[y, x] in 'su': m.stamp('nr_wall_v', x, y, mark='B')
    for x, py in ports.items():                                                           # forts either side of each port
        for (fx, fy) in ((x - 1, py - 5), (x - 1, py + 3)):
            r.near('wr_sledfort', fx, fy, on='su', r=2)
    for nm, x, y in (('wr_tent_b', 6, 8), ('wr_tent_b', 10, 3), ('wr_tent_w', 14, 8), ('wr_sledfort2', 6, 3), ('wr_sledfort', 23, 6),
                     ('wr_ban_ise', 17, 10), ('wr_ban_ise', 31, 11), ('wr_ban_ise', 45, 10), ('wr_tent_b', 24, 9), ('wr_sledfort2', 38, 7),
                     ('wr_tent_w', 50, 7), ('fw_sled', 9, 11), ('fw_wood', 12, 11), ('fw_brazier', 21, 12), ('fw_brazier', 35, 12),
                     ('fw_rack', 4, 6), ('pf_signpost', 3, 18) if False else ('fw_sled', 26, 19)):
        r.near(nm, x, y, on='su', r=3)
    CK.props(r, ['dk_rock_big', 'dk_boulder', 'dk_pebbles', 'nt_deadtree'], 22, box=(0, 18, W, H), on='su', clump=2, seed=5)
    CK.props(r, ['dk_boulder', 'dk_pebbles'], 10, box=(0, 0, W, 12), on='su', clump=2, seed=6)
    r.dress(trees=('nt_deadtree',), n_trees=0, copses=0, scatter=0)
    r.paint()
    sand_dress(r, 0.52, seed=920, bones=0.03)
    # rime: the frozen side (west of the third line) is white with frost; trenches cut along each revetment's west face
    frozen_ground(r, [(x, y) for y in range(H) for x in range(0, 47 + int(3 * vnoise(0, y, 9201, 4.0)))], thr=0.30)
    ground_var(r, ['gs_crust0', 'gs_crust1', 'gs_crust2', 'gs_crust3'], 0.40, seed=1, cells=[(x, y) for y in range(H) for x in range(44, W)])
    decal(r, ['wr_frost0', 'wr_frost1', 'wr_frost2'], 0.30, on='su', seed=1,
          cells=[(x, y) for y in range(H) for x in range(0, 47) if m.cls[y, x] in 'su'])
    decal(r, ['wr_trench0', 'wr_trench1'], 1.0, seed=2, cells=[(x - 1, y) for x, y in rev] + [(x - 2, y) for x, y in rev if y % 2])
    decal(r, ['wr_ember0', 'wr_ember1'], 0.06, on='su', seed=3)
    decal(r, ['wr_bones0', 'wr_bones1', 'wr_rut0', 'wr_ember2'], 0.05, on='su', seed=4)
    CK.scatter_quiet(r, 14)
    h = head(920, 'The Rimed Sands', field='DESERT', bgm='Route 9', biome='desert', weather=['Snow', 10],
             connections=[{'dir': 'E', 'offset': 13, 'to': 925, 'to_offset': 13}],
             tone=[10, 6, 14, 10], fog={'name': 'prismfall_seamist', 'opacity': 24, 'blend': 0, 'zoom': 200, 'sx': 1, 'sy': 0})
    h['metadata']['MapPosition'] = [0, 12, 14]
    r.write(h, '920_rimed_sands.yaml', '# The Rimed Sands (920). WRITTEN BY layouts/war.py (map builder 10) - edit that script.\n',
            '/tmp/craft/920.png' if PREV else None)


BUILD = {920: build_920}


# ====================================================================================================== 925 The Steamline
def build_925():
    """The Steamline (64x32, BLEED): no-man's-land where the two Imprints meet.  The west half is Isenmar's (sand frozen
    white, rime, a dead ice-sled), the east half Ashkaar's (scorched black, embers, a burnt-out picket line); down the
    middle the permanent steam wall stands over a belt of sand fused to glass, crystal growths in every Imprint's colour
    with three quiet lanes through.  W: the Rimed Sands, E: the Siege Camp, S (the middle): down onto the crest of the
    Glass Dunes.  Stand between: one soldier of each army waits in the glass (the gauntlet)."""
    W, H = 64, 32
    r, m = desert(W, H, 925)
    dunes(r, 5, 925, box=(2, 3, 26, 28)); dunes(r, 5, 926, box=(38, 3, 62, 28))
    r.road([(0, 14.5), (14, 15), (24, 13.5), (31, 15), (40, 16.5), (52, 15), (63, 14.5)], w=3.0, c='u', open_=None, only='su.tT')
    r.road([(31, 16), (31, 24), (31.5, 31)], w=3.0, c='u', open_=None, only='su.tT')
    r.exit('W', 13, 4); r.exit('E', 13, 4); r.exit('S', 30, 4)
    r.finish_plan(border=1)
    E = [FRONT,
         sign((10, 12), 'Field marker', "ISENMAR LINES -> W.  The rest is anybody's."),
         sign((54, 12), 'Field marker ', "ASHKAAR LINES -> E.  (Somebody has scratched under it: \"and the glass is nobody's.\")"),
         obj('The steam wall', (29, 8), ['Where ice meets fire the air is a wall: steam that never thins, and inside it the Bleed ringing like a struck glass.',
                                          'Soldiers who walk in come out with frost on one side of their face and burns on the other. You walk in. It goes quiet.']),
         obj('Glassed sand', (35, 22), ['Sand fused to glass a foot deep, clouded, with things in it: a boot, a spearhead, a whole Sandile, curled up.']),
         obj('Convoy marker', (20, 17), ['A cairn of sled runners with a white rag tied on: the convoys from Duneholt stop here and wait for someone who can walk them through.']),
         soldier((18, 13), 'Isenmar sentry', 'NPC 11', ["Isenmar sentry: Past this point the ground can't decide what it is. Neither can you, after a while."], d='right'),
         soldier((45, 17), 'Ashkaar sentry', 'NPC 21', ["Ashkaar sentry: The Dominar says the glass is ours by right of fire. The glass hasn't said."], d='left'),
         gauntlet((27, 14), 'ISENMAR_SOLDIER_M', 'Soldier', 1, 'WAR_SIDE_MID', "Between the lines? Then you're nobody's. Nobody's is fair game.",
                  "...You really are nobody's. All right.", d='right'),
         gauntlet((36, 16), 'ASHKAAR_SOLDIER_M', 'Soldier', 1, 'WAR_SIDE_MID', 'You walked out of the steam like it was a door. Show me the rest.',
                  "The steam lets you through. So will I.", d='left'),
         hidden((33, 4), 'STARDUST', 'HiddenItem (the glass)'), item((60, 28), 'FIRESTONE'), item((3, 28), 'ICESTONE')]
    r.add(*E)
    r.seat_events(on='su')
    rng = random.Random(925)
    CRY = ['cr_clear_c', 'cr_teal_c', 'cr_clear_e', 'cr_grey_c', 'cr_purple_c', 'cr_pink_c', 'cr_clear_t', 'cr_teal_e', 'cr_red_c', 'cr_blue_c']
    lanes = (5, 15, 24)                                                         # three quiet lanes through the glass belt (rows)
    for y in range(1, H - 1):
        for x in range(27, 37):
            if r.road_mask[y, x] or any(abs(y - ly) <= 1 for ly in lanes) or m.taken[y, x] or m.cls[y, x] not in 'su': continue
            if vnoise(x, y, 9251, 2.5) > 0.42 and rng.random() < 0.55:
                n = rng.choice(CRY)
                if m.free(x, y, 1, STAMPS[n]['h'], on='su'): m.stamp(n, x, y, mark='B')
    for nm, x, y in (('fw_sled', 8, 20), ('wr_sledfort2', 4, 5), ('wr_ban_ise', 12, 9), ('fw_rack', 6, 25), ('ak_rock2', 15, 26),
                     ('wr_picket', 50, 9), ('wr_picket', 53, 9), ('wr_picket', 56, 9), ('wr_ban_ash', 51, 20), ('wr_sledfort', 57, 24),
                     ('nr_colfall', 46, 26), ('pf_wagon', 42, 6)):
        r.near(nm, x, y, on='su', r=3)
    CK.props(r, ['dk_rock_big', 'dk_boulder', 'dk_pebbles', 'nt_deadtree'], 14, box=(0, 0, W, H), on='su', clump=2, seed=5)
    r.dress(trees=('nt_deadtree',), n_trees=0, copses=0, scatter=0)
    r.paint()
    sand_dress(r, 0.35, seed=925)
    frozen_ground(r, [(x, y) for y in range(H) for x in range(0, 27 + int(3 * vnoise(0, y, 9252, 4.0)))], thr=0.25)
    decal(r, ['wr_frost0', 'wr_frost1', 'wr_frost2'], 0.35, seed=1, cells=[(x, y) for y in range(H) for x in range(0, 28)])
    decal(r, ['wr_ember0', 'wr_ember1', 'wr_ember2'], 0.40, seed=2, cells=[(x, y) for y in range(H) for x in range(37, W)])
    for y in range(H):                                                           # the steam wall over the glass belt
        for x in range(25, 39):
            if m.inb(x, y) and not m.L[2, y, x] and not m.taken[y, x] and m.cls[y, x] != 'B' and vnoise(x, y, 9253, 3.0) > 0.3 - 0.25 * (1 - abs(x - 31.5) / 7.0):
                m.L[2, y, x] = K.P1('wr_steam%d' % ((x + 2 * y) % 3))
    for y, x in np.argwhere(np.isin(m.cls, ['s', 'u'])):                         # obsidian scorch: ember side ground darkened
        if x >= 40 and vnoise(x, y, 9254, 4.0) > 0.62 and not m.L[2, y, x] and not m.taken[y, x]: m.L[2, y, x] = K.P1('wr_ember%d' % ((x + y) % 3))
    CK.scatter_quiet(r, 8)
    h = head(925, 'The Steamline', field='BLEED', bgm='Route 9', biome='bleed',
             connections=[{'dir': 'W', 'offset': 13, 'to': 920, 'to_offset': 13}, {'dir': 'E', 'offset': 13, 'to': 924, 'to_offset': 18},
                          {'dir': 'S', 'offset': 2, 'to': 926, 'to_offset': 0}],
             tone=[6, -4, 10, 30], fog={'name': 'prismfall_seamist', 'opacity': 60, 'blend': 0, 'zoom': 150, 'sx': 2, 'sy': 0})
    h['metadata']['MapPosition'] = [0, 13, 14]
    r.write(h, '925_steamline.yaml', '# The Steamline (925, :BLEED). WRITTEN BY layouts/war.py (map builder 10) - edit that script.\n',
            '/tmp/craft/925.png' if PREV else None)


BUILD[925] = build_925


# ====================================================================================================== 924 Ashkaar Siege Camp
def build_924():
    """Ashkaar Siege Camp (56x40, ASHEN_WASTE): the legions on the eastern dunes behind two earthworks facing the
    Steamline (W), each with one gate.  Inside: lines of red legion tents, the dragon pickets (chained riders' mounts),
    trebuchets on the inner earthwork, the forge and the mess fire, and the Dominar's war-tent (the door to 928).  E: the
    war road back to Glasswake (not built: a guarded barricade).  S: down to the Glass Dunes.  Back Isenmar: Ashkaar
    soldiers hold the two gates and the war-tent's approach (the gauntlet)."""
    W, H = 56, 40
    r, m = desert(W, H, 924)
    dunes(r, 4, 924, box=(2, 2, 54, 6)); dunes(r, 4, 9241, box=(24, 33, 54, 37))
    r.road([(0, 19.5), (12, 19.5), (24, 20), (36, 19), (48, 20), (55, 19.5)], w=3.0, c='u', open_=None, only='su.tT')
    r.road([(20, 21), (14, 30), (8, 39)], w=3.0, c='u', open_=None, only='su.tT')
    for y0 in (10, 28):
        r.lane([(24, y0), (50, y0)], w=2.0, c='u', open_=None, only='su.')
    r.lane([(36, 20), (36, 14)], w=3.0, c='u', open_=None, only='su.')
    for cx, cy, rx, ry in ((30, 17, 4, 1.6), (44, 18, 5, 1.8), (27, 34, 4, 1.5)):          # drill yards: trodden gravel
        m.blob(cx, cy, rx, ry, 'g', seed=cx + cy, rough=0.4, only='su')
    r.exit('W', 18, 4); r.exit('E', 18, 4)
    r.finish_plan(border=1)
    gates = {10: 19, 20: 20}
    works = []
    for x, gy in gates.items():
        for y in range(1, H - 1):
            if abs(y - gy) <= 1 or m.cls[y, x] not in 'su': continue
            if x == 20 and 28 <= y <= 33: continue                                   # (the south road leaves through a cut)
            works.append((x, y))
    d = m.stamp('wr_wartent', 34, 9, 'WAR_TENT', "War-tent door")
    E = [FRONT, {'type': 'warp', 'name': 'To the Glass Dunes', 'at': [8, 39], 'link': 'WAR_CAMP_DUNES', 'arrive': [8, 38, 'up'], 'fixed': True},
         sign((4, 17), 'Camp sign', "ASHKAAR SIEGE CAMP - by the Dominar's leave and the Elector's Lease. Lies are a capital crime in this camp."),
         obj('Earthwork', (9, 14), ['A rampart of sand and black glass, packed hard and baked: the legion engineers fire it with Torkoal until it rings.']),
         obj('Forge', (44, 25), ['A field forge, roaring. Spearheads for the legion, shoes for the Rapidash, and a dragon\'s neck-plate the size of a door.']),
         obj('Mess fire', (28, 25), ['The mess fire. Somebody is stirring a pot of red lentils as big as a bath and singing a marching song badly.']),
         soldier((26, 16), 'Legionary', 'NPC 21', ["Legionary: The steam's a wall. The wall's a Bleed. The Bleed's Isenmar's fault. That's the briefing."], d='down'),
         soldier((40, 22), 'Dragon handler', 'NPC 20', ["Dragon handler: Don't look them in the eye. Don't look them in the tail either. Just walk."], d='left'),
         soldier((47, 31), 'Quartermaster', 'NPC 25', ["Quartermaster: Fire we have. Water we buy. From Ossaria. At Ossarian prices."], d='up'),
         soldier((15, 26), 'Scout', 'NPC 22', ["Scout: The bone-carters walk straight across. Nobody shoots a bone-carter. Not twice."], d='right'),
         talk('Dragonite', (46, 12), 'Followers/DRAGONITE', ['(It is chained to the picket. It looks at the chain, then at you, then sighs.)'], move='random'),
         talk('Charizard', (50, 14), 'Followers/CHARIZARD', ['(A war-mount, scarred. It warms the sand where it lies.)']),
         obj('Barricade (war road)', (53, 22), ['The war road east to Glasswake, barricaded and guarded. Supplies come in; nobody goes out.']),
         gauntlet((11, 19), 'ASHKAAR_SOLDIER_M', 'Soldier', 0, 'WAR_SIDE_ISE', 'Isenmar sends children now? Then I fight children.',
                  "...Not children. Go on, then. The next gate won't be so polite.", d='left'),
         gauntlet((21, 20), 'ASHKAAR_SOLDIER_F', 'Soldier', 0, 'WAR_SIDE_ISE', 'Second gate. The fire behind it is real.',
                  'The fire behind it is real. So is that.', d='left'),
         gauntlet((35, 16), 'ASHKAAR_OFFICER', 'Captain', 0, 'WAR_SIDE_ISE', "You want the Dominar's tent? Through me. That is how it works here.",
                  "That is how it works here. Pass.", d='down'),
         item((52, 36), 'CHARCOAL'), hidden((30, 4), 'STARDUST', 'HiddenItem (dune)'), item((3, 36), 'HYPERPOTION')]
    r.events += [e for e in m.events if e.get('link') == 'WAR_TENT']; m.events = []
    r.add(*E)
    r.seat_events(on='su')
    for x, y in works:
        if not m.taken[y, x] and m.cls[y, x] in 'su': m.stamp('nr_wall_v', x, y, mark='B')
    for x, gy in gates.items():
        r.near('wr_ban_ash', x - 1, gy - 3, on='su', r=1); r.near('wr_ban_ash', x - 1, gy + 2, on='su', r=1)
    tents = [(x, y) for y in (5, 12, 23, 30) for x in range(24, 52, 5)]
    for i, (x, y) in enumerate(tents):
        if abs(x - 36) < 5 and y < 16: continue
        r.near('wr_tent_r' if i % 4 else 'wr_tent_w', x, y, on='su', r=1)
    for nm, x, y in (('wr_trebuchet', 13, 6), ('wr_trebuchet', 13, 30), ('wr_trebuchet', 22, 8), ('wr_picket', 45, 13), ('wr_picket', 49, 15),
                     ('wr_picket', 52, 11), ('sh_campfire', 28, 26), ('fw_brazier', 33, 18), ('fw_brazier', 39, 18), ('hb_crates4', 46, 27),
                     ('hb_barrels', 49, 27), ('sh_crates', 42, 33), ('wr_ban_ash', 31, 11), ('wr_ban_ash', 41, 11), ('hb_tubs', 30, 33)):
        r.near(nm, x, y, on='su', r=3)
    CK.props(r, ['dk_rock_big', 'dk_boulder', 'dk_pebbles'], 10, box=(0, 0, 10, H), on='su', clump=2, seed=5)
    r.dress(trees=('nt_deadtree',), n_trees=0, copses=0, scatter=0)
    r.paint()
    sand_dress(r, 0.40, seed=924)
    decal(r, ['wr_ember0', 'wr_ember1', 'wr_ember2'], 0.30, on='sug', seed=2)
    decal(r, ['wr_trench0', 'wr_trench1'], 1.0, seed=3, cells=[(x - 1, y) for x, y in works])
    decal(r, ['wr_bones0', 'wr_bones1', 'wr_rut0', 'wr_rut1'], 0.06, on='sug', seed=4)
    CK.scatter_quiet(r, 16)
    h = head(924, 'Ashkaar Siege Camp', field='ASHEN_WASTE', bgm='Route 9', biome='desert',
             connections=[{'dir': 'W', 'offset': 18, 'to': 925, 'to_offset': 13}],
             tone=[18, 4, -10, 10])
    h['metadata']['MapPosition'] = [0, 14, 14]
    r.write(h, '924_siege_camp.yaml', '# Ashkaar Siege Camp (924). WRITTEN BY layouts/war.py (map builder 10) - edit that script.\n',
            '/tmp/craft/924.png' if PREV else None)


BUILD[924] = build_924


# ====================================================================================================== 926 The Glass Dunes
PARTNER_END = {'script': 'pbDeregisterPartner rescue ($PokemonGlobal.partner = nil)'}


def partner_page(sw, who, ver, foes, lines, win):
    return {'cond': {'switch': sw}, 'graphic': {'sprite': SPRITE['LEADER_%s' % who.upper()], 'dir': 'down'}, 'trigger': 'action',
            'commands': list(lines) + [
                {'script': 'pbRegisterPartner(:LEADER_%s, "%s", %d)' % (who.upper(), who, ver)}, {'script': 'setBattleRule("double")'},
                {'if': 'TrainerBattle.start(%s)' % foes, 'then': [PARTNER_END] + list(win) + [{'script': 'pfm_set(:war_partner_done)'}, {'selfswitch': ['A', True]}],
                 'else': [PARTNER_END]}]}


def build_926():
    """The Glass Dunes (60x48, DESERT; the battlefield of the climax, WAR-1).  Bone-white dunes across the old caravan
    road; the wells both armies want; wrecked sleds and burnt pickets from a winter of skirmishes.  The crest (north
    middle) is reached only from the Steamline (N, x 28-31) and drops one way to the south flats by the dune ledges; west
    and east, glass ridges and wrecks close it.  NW: up to the Rimed Sands (920); NE: up to the Siege Camp (924); E: the
    bone-carters' camp (930); S: the goat-path to the Observers' Mesa (929, after the battle).  On the crest in Ch19: the
    crest singles, the partner double (Sigrun, or Marisol if you back Isenmar) and the legend (Reshiram, or Kyogre if you
    back Ashkaar), then WAR-1."""
    W, H = 60, 48
    r, m = desert(W, H, 926)
    # the crest: a high dune plateau (h1) in the north middle, lee ledges along its south face
    CREST = {x: 14 for x in range(18, 43)}                                     # (one straight lee: a stepped one leaks at every step)
    r.road([(29.5, 0), (30, 6), (30, 12)], w=3.0, c='u', open_=None, only='su.tT')            # from the Steamline onto the crest
    r.road([(7, 1), (9, 12), (14, 22), (24, 28), (36, 30), (48, 31), (59, 31.5)], w=3.0, c='u', open_=None, only='su.tT')   # the caravan road
    r.road([(51, 1), (50, 12), (46, 24), (44, 30)], w=3.0, c='u', open_=None, only='su.tT')
    r.lane([(30, 31), (30, 40), (30, 46)], w=2.0, c='u', open_=None, only='su.')
    r.exit('N', 28, 4); r.exit('E', 30, 4)
    # dry flood channels (wadis) cut by the Primal rain of the Thaw, gravel beds snaking down to the south
    CK.stream(r, [(2, 20), (8, 27), (12, 35), (10, 42), (14, 47)], w=2.2, c='g', seed=1, only='su')
    CK.stream(r, [(57, 22), (52, 28), (54, 36), (49, 42), (51, 47)], w=2.0, c='g', seed=2, only='su')
    CK.stream(r, [(22, 33), (26, 38), (24, 44), (27, 47)], w=1.8, c='g', seed=3, only='su')
    dunes(r, 8, 926, box=(2, 34, 56, 45)); dunes(r, 4, 9262, box=(2, 18, 14, 28)); dunes(r, 4, 9263, box=(46, 16, 57, 26))
    r.finish_plan(border=1)
    for x, y in CREST.items():                                                  # (keep the lee row and the sides free of dunes)
        for yy in range(y, y + 2): r.road_mask[yy, x] = r.road_mask[yy, x]
    E = [FRONT,
         {'type': 'warp', 'name': 'To the Rimed Sands', 'at': [7, 1], 'link': 'WAR_RIMED_DUNES', 'arrive': [7, 2, 'down'], 'fixed': True},
         {'type': 'warp', 'name': 'To the Siege Camp', 'at': [51, 1], 'link': 'WAR_CAMP_DUNES', 'arrive': [51, 2, 'down'], 'fixed': True},
         sign((27, 1), 'Field marker', 'THE CREST. Below it, the caravan road and the wells. Above it, everything else.'),
         obj('Caravan well', (36, 33), ['A caravan well between the lines. A white ribbon on the sweep: the bone-carters\' sign. No blood at a well. Both armies keep that.']),
         obj('Caravan well ', (18, 26), ['The second well, its bucket gone, its rope cut. Someone has left a full waterskin on the rim for whoever comes next.']),
         obj("Bone-carters' banner", (40, 9), ['The bone-carters\' white banner on the crest\'s east shoulder. Under it, a tally-stick for every soldier carried off the sand. Both armies\' names.']),
         obj('Wrecked sled', (10, 18), ['An Isenmar sled-fort, overturned, its runners in the air, burnt to the iron on the eastern side.']),
         talk('Bone-carter', (40, 37), 'NPC 27', ["Bone-carter: We carry them out. Whose they were doesn't matter. Whose they are now does: Ossaria's. Tomb-law."], d='left'),
         gauntlet((27, 8), 'ASHKAAR_SOLDIER_F', 'Soldier', 1, 'WAR_SIDE_ASH', "The crest is held. By me, for now.", 'For now.', d='down'),
         gauntlet((33, 8), 'ISENMAR_SOLDIER_F', 'Soldier', 1, 'WAR_SIDE_ASH', "One more between you and the crest.", 'Go. Look at what we did.', d='down'),
         gauntlet((27, 9), 'ASHKAAR_SOLDIER_F', 'Soldier', 1, 'WAR_SIDE_ISE', "The crest is held. By me, for now.", 'For now.', d='down'),
         gauntlet((33, 9), 'ISENMAR_SOLDIER_F', 'Soldier', 1, 'WAR_SIDE_ISE', "One more between you and the crest.", 'Go. Look at what we did.', d='down'),
         gauntlet((27, 10), 'ASHKAAR_SOLDIER_F', 'Soldier', 1, 'WAR_SIDE_MID', "The crest is held. By me, for now.", 'For now.', d='down'),
         gauntlet((33, 10), 'ISENMAR_SOLDIER_F', 'Soldier', 1, 'WAR_SIDE_MID', "One more between you and the crest.", 'Go. Look at what we did.', d='down'),
         {'type': 'event', 'name': 'Partner', 'at': [30, 4], 'fixed': True, 'pages': [
             {'commands': []},
             partner_page('WAR_SIDE_MID', 'Sigrun', 19, ':ISENMAR_OFFICER, "Captain", 1, :ASHKAAR_OFFICER, "Captain", 1',
                          ['Sigrun: Between them? Then we hold the middle. Both captains are coming. Back to back.'], ['Sigrun: Still standing. Both of us. Look up.']),
             partner_page('WAR_SIDE_ASH', 'Sigrun', 19, ':ISENMAR_OFFICER, "Captain", 1, :ISENMAR_SOLDIER_M, "Soldier", 2',
                          ["Sigrun: With us, then. The Isenmar line breaks here or nowhere."], ['Sigrun: It broke. Now the sky.']),
             partner_page('WAR_SIDE_ISE', 'Marisol', 19, ':ASHKAAR_OFFICER, "Captain", 1, :ASHKAAR_SOLDIER_M, "Soldier", 2',
                          ["Marisol: Kid. You came. Course you came. Stand on my left; the sea's on my right."], ["Marisol: Ha! The Ebb runs both ways, and today it ran ours."]),
             {'cond': {'self': 'A'}, 'commands': ['(The ground under the crest is humming. Something enormous is coming.)']}]},
         {'type': 'event', 'name': 'The legend', 'at': [30, 2], 'fixed': True, 'pages': [
             {'commands': []},
             {'cond': {'switch': 'WAR_SIDE_ASH'}, 'trigger': 'action', 'commands': [{'call': 'legend'}] if False else []},
         ]},
         item((56, 44), 'FULLRESTORE'), hidden((4, 40), 'STARDUST', 'HiddenItem (dunes)'), hidden((38, 4), 'BIGNUGGET', 'HiddenItem (the crest)')]
    legend = [{'if': '!pfm?(:war_partner_done)', 'then': ['(The ground is shaking. Over the sea the clouds are turning the wrong way. Not yet.)'],
               'else': [{'if': 'pfm?(:war_battle_done)', 'then': ['(The glass hums underfoot, quietly. It is over.)'], 'else': [
                   {'script': "legend = (pf_choice(:war_legend) rescue nil)\nif legend != :neither\n  Prismfall::Bosses.wild_battle($game_switches[605] ? :KYOGRE_GLASS_DUNES : :RESHIRAM_GLASS_DUNES)\nend"},
                   {'if': "((pf_choice(:war_legend) rescue nil) == :neither) || ((Prismfall::Bosses.last_result || {})[:result] == :turned_back)",
                    'then': [{'script': 'Prismfall::Cutscene.play(:WAR_CLIMAX) rescue nil'}, {'script': 'pfm_set(:war_battle_done)'}],
                    'else': ['(It wheels away over the flood and comes round again. The crest shakes.)']}]}]}]
    E[[i for i, e in enumerate(E) if e.get('name') == 'The legend'][0]]['pages'] = [
        {'commands': []}] + [{'cond': {'switch': sw}, 'trigger': 'action', 'commands': legend} for sw in ('WAR_SIDE_MID', 'WAR_SIDE_ASH', 'WAR_SIDE_ISE')]
    E.append({'type': 'event', 'name': 'Goat-path', 'at': [30, 46], 'fixed': True, 'pages': [{'trigger': 'action', 'commands': [
        {'if': 'pfm?(:war_battle_done)', 'then': ['A goat-path up the sandstone to the mesa, where Meridian\'s white tents stand.', {'se': 'Door exit'},
                                                    {'transfer': {'map': 929, 'x': 17, 'y': 26, 'dir': 'up'}}],
         'else': ['A goat-path up the sandstone mesa. Meridian guards in white at the top, with brass glasses on everything. "Observers only."']}]}]})
    rng0 = random.Random(9260)
    for x0, x1, yend in ((15, 18, CREST[18] + 1), (43, 46, CREST[42] + 1)):            # glass ridges close the crest's sides
        for y in range(1, yend):                                                       # (laid before anything else is seated)
            for x in range(x0, x1):
                if m.cls[y, x] in 'sug' and not r.road_mask[y, x]:
                    m.stamp(rng0.choice(['cr_clear_c', 'cr_teal_c', 'cr_grey_c', 'cr_clear_c', 'cr_blue_c']), x, y, mark='B')
    r.add(*E)
    r.seat_events(on='su')
    # the crest's lee: one-way dune ledges along its south face (crest -> flats), glass ridges and wrecks closing its sides
    for x, y in CREST.items():                                                  # the crest's lee: one way down to the flats
        m.over.append((1, x, y, K.P1('lgd_' + ('w' if x == 18 else 'e' if x == 42 else 'm')))); m.taken[y, x] = True
        if m.cls[y, x] not in 'su': m.cls[y, x] = 'u'
    rng = random.Random(926)
    for nm, x, y in (('wr_sledfort', 8, 16), ('wr_sledfort2', 21, 22), ('wr_well', 35, 31), ('wr_well', 17, 24), ('wr_ban_bone', 44, 9),
                     ('wr_bonecart', 41, 34), ('wr_bonecart', 25, 36), ('wr_picket', 47, 20), ('wr_picket', 49, 22), ('wr_ban_ash', 52, 14),
                     ('wr_ban_ise', 6, 22), ('pf_wagon', 12, 30), ('nr_colfall', 54, 40), ('fw_sled', 4, 30), ('wr_tally', 48, 38)):
        r.near(nm, x, y, on='su', r=3)
    CK.props(r, ['dk_rock_big', 'dk_boulder', 'dk_pebbles', 'nt_deadtree'], 22, box=(0, 18, W, H), on='su', clump=2, seed=5)
    CK.props(r, ['cr_clear_c', 'cr_grey_c', 'cr_clear_e', 'cr_teal_c'], 16, box=(14, 18, 46, H), on='su', clump=2, seed=6)   # glass from the skirmishes
    CK.props(r, ['dk_pebbles', 'nt_rocks_s0'], 14, box=(0, 18, W, H), on='g', clump=2, seed=7)
    r.dress(trees=('nt_deadtree',), n_trees=0, copses=0, scatter=0)
    r.paint()
    sand_dress(r, 0.45, seed=926, bones=0.03)
    frozen_ground(r, [(x, y) for y in range(H) for x in range(0, 14)], thr=0.55)
    decal(r, ['wr_frost0', 'wr_frost1'], 0.18, seed=1, cells=[(x, y) for y in range(H) for x in range(0, 16)])
    decal(r, ['wr_ember0', 'wr_ember1', 'wr_ember2'], 0.18, seed=2, cells=[(x, y) for y in range(H) for x in range(44, W)])
    CK.scatter_quiet(r, 10)
    h = head(926, 'The Glass Dunes', field='DESERT', bgm='Route 9', biome='desert',
             connections=[{'dir': 'N', 'offset': 0, 'to': 925, 'to_offset': 2}, {'dir': 'E', 'offset': 30, 'to': 930, 'to_offset': 15}],
             tone=[14, 8, 0, 10])
    h['metadata']['MapPosition'] = [0, 13, 15]
    h['gates'] = [{'name': 'The crest (only from the Steamline)', 'from': [[56, 31], [7, 3], [51, 3]], 'sealed': [[30, 4], [30, 6]]}]
    r.write(h, '926_glass_dunes.yaml', '# The Glass Dunes (926). WRITTEN BY layouts/war.py (map builder 10) - edit that script.\n',
            '/tmp/craft/926.png' if PREV else None)


BUILD[926] = build_926


# ====================================================================================================== 928 the Command Pavilion
def build_928():
    """Ashkaar Siege Camp - Command Pavilion (24x18 interior of 924's war-tent; tileset 54 'stage', red and gold): red
    lacquer screens down both sides, the map table of the western dunes, the oath-brazier (lies are a capital crime
    here), the Light Stone's empty stand on the dais, and the prisoner's cage in the back alcove.  Anchors for the story
    owner: 'Dominar Hrothgar' (the petition, :ch19_dominar) and 'Anja (cage)' (:war_prisoner, Ch15-16)."""
    import hallkit as HK
    from hallkit import MI, MG, NM, CU
    W, H = 24, 18
    rows = ['#' * W]
    for y in range(1, H - 1):
        if y in (1, 2): rows.append('#' + 'W' * (W - 2) + '#')
        elif y == H - 2: rows.append('#' * 10 + '....' + '#' * 10)
        else: rows.append('#' + '.' * (W - 2) + '#')
    rows.append('#' * W)
    h = HK.Hall(rows, 'stage', {'#': 'void', 'W': 'wall', '.': 'floor'}, seed=928)
    for y in range(3, H - 1):
        for x in range(1, W - 1):
            if rows[y][x] == '.': h.put(NM(685), x, y, 0)                                       # red damask underfoot
    for x in range(1, W - 1): h.put(NM(393), x, 1, 0)                                          # lacquer and gold up top
    for y in range(3, 13):                                                                     # the lacquer screens
        for x in (2, W - 3): h.put(MG(4681) if y == 3 else MG(4697) if y == 12 else MG(4689), x, y, 1)
    h.block([[CU('crest_0'), CU('crest_1'), CU('crest_2')]], 10, 1, 2)
    h.put(CU('dais'), 11, 4, 1); h.put(CU('dais'), 12, 4, 1); h.put(CU('rostrum'), 12, 3, 1)      # the Light Stone's empty stand
    h.obj('rug_mg', 9, 8)                                                                       # the map table on its rug
    h.obj('urn', 6, 5); h.obj('urn', 17, 5)                                                     # the oath-brazier and its twin
    for x in range(4, 9): h.put(MG(1704), x, 4, 1)                                              # the cage's iron posts (back left)
    h.obj('couch_l', 18, 9); h.obj('plant', 20, 13); h.obj('plant', 3, 13)
    spec = {'id': 928, 'name': 'Ashkaar Siege Camp - Command Pavilion', 'parent': 924, 'biome': 'interior', 'bgm': 'Route 9',
            'tone': [16, 0, -10, 0], 'metadata': {'MapPosition': [0, 14, 14]}}
    spec.update(h.write(928))
    spec['events'] = [
        {'type': 'exit', 'at': [11, 16], 'link': 'WAR_TENT'}, {'type': 'exit', 'at': [12, 16], 'link': 'WAR_TENT'},
        {'type': 'event', 'name': 'Dominar Hrothgar', 'at': [12, 6], 'pages': [{'graphic': {'sprite': SPRITE['DOMINAR'], 'dir': 'down'}, 'trigger': 'action',
            'commands': ['Dominar Hrothgar: Speak plainly. The brazier is lit. In this tent a lie is a death sentence, and I have signed eleven.']}]},
        {'type': 'event', 'name': 'Anja (cage)', 'at': [6, 3], 'pages': [{'commands': []},
            {'cond': {'switch': 'WAR_SIDE_ASH'}, 'commands': []}]},
        {'type': 'sign', 'name': 'Map table', 'at': [11, 9], 'post': False,
         'text': "The western dunes in sand on a lacquer table: Skaldfast a white stone, the Siege Camp a red one, the Steamline a line of salt. Someone has drawn the bone-carters' banner in the margin. Small."},
        {'type': 'sign', 'name': 'Oath-brazier', 'at': [6, 7], 'post': False,
         'text': 'The oath-brazier. Its flame is white at the heart. In Ashkaar, what is said over it is true, or the speaker is not long for the world.'},
        {'type': 'sign', 'name': 'Empty stand', 'at': [12, 5], 'post': False,
         'text': "A stand of black glass, empty. Something round and heavy sat here. The dust says: recently."},
        {'type': 'sign', 'name': 'Cage', 'at': [9, 4], 'post': False, 'text': 'An iron cage, the kind they keep hawks in, made larger.'}]
    import yaml
    out = os.path.join(K.HERE, 'specs', '928_command_pavilion.yaml')
    open(out, 'w').write('# Ashkaar Siege Camp - Command Pavilion (928). WRITTEN BY layouts/war.py (map builder 10) - edit that script.\n'
                         + yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))


BUILD[928] = build_928


# ====================================================================================================== 929 The Observers' Mesa
def build_929():
    """The Observers' Mesa (36x28, DESERT): a flat-topped sandstone mesa behind the lines, reached by one goat-path from
    the Glass Dunes' south edge (926).  Meridian's white tents, brass tripods and dial-boxes, a field telegraph strung
    off east; from the north rim the whole battlefield below.  Dr. Quent packs up here after WAR-1."""
    W, H = 36, 28
    r, m = desert(W, H, 929)
    for y in range(H):                                                           # the mesa top (h1); its rim drops all round
        for x in range(W):
            if 2 <= x <= W - 3 and 2 <= y <= H - 4 - (3 if 15 <= x <= 19 else 0) and vnoise(x, y, 9291, 4.0) > 0.12 * (min(x - 2, W - 3 - x, y - 2, H - 4 - y) < 1):
                m.ht[y, x] = 1
    CK.smooth_ht(m, 1, 2)
    CK.stair(r, 16, max(y for y in range(H) if m.ht[y, 17] == 1), w=3, h=1)
    r.lane([(17, 27), (17, 20), (17, 12), (12, 8)], w=2.0, c='u', open_=None, only='su')
    r.lane([(17, 14), (26, 10)], w=2.0, c='u', open_=None, only='su')
    r.finish_plan(border=0)
    for y in range(H):                                                           # beyond the rim: sky-drop (the dunes far below)
        for x in range(W):
            if m.ht[y, x] == 0 and not r.road_mask[y, x] and not (15 <= x <= 19 and y >= H - 6) and m.cls[y, x] in 'su': m.cls[y, x] = 'W' if False else m.cls[y, x]
    E = [{'type': 'event', 'name': 'Goat-path', 'at': [17, 27], 'fixed': True, 'pages': [{'trigger': 'touch', 'through': True, 'commands': [
            {'se': 'Door exit'}, {'transfer': {'map': 926, 'x': 30, 'y': 45, 'dir': 'down'}}]}]},
         talk('Dr. Quent', (14, 9), 'trainer_SCIENTIST', ["Dr. Quent: Don't touch the dials. They are still reading. Everything down there is still reading.",
                                                          "Dr. Quent: A battle? To you. To the Engine it was a calibration. A very good one. Pack the lenses, Tobin."], d='down'),
         talk('Observer Tobin', (21, 12), 'NPC 12', ["Observer Tobin: Two Imprints at full draw and a Bleed dome at the meeting point. I've never seen the needle do that.",
                                                     "Observer Tobin: Dr. Quent says we were never here. I've written that down too."], d='left'),
         talk('Telegraphist', (27, 9), 'NPC 18', ["Telegraphist: Tap tap tap. Meridian Spire wants it in words of one syllable. 'IT WORKED.' That's three."], d='down'),
         {'type': 'sign', 'name': 'The rim', 'at': [17, 3], 'post': False,
          'text': "From the north rim the whole battlefield is spread out below: the white trench-lines, the red camp, the Steamline's steam, and the glass where the beams met, still smoking."},
         {'type': 'sign', 'name': 'Dial-box', 'at': [9, 13], 'post': False, 'text': "A brass dial-box. Its needle is pinned hard right, past a mark labelled 'THEORETICAL'."},
         item((30, 20), 'RARECANDY'), hidden((5, 20), 'STARDUST', 'HiddenItem (mesa)')]
    r.add(*E)
    r.seat_events(on='su')
    for nm, x, y in (('wr_tent_w', 8, 5), ('wr_tent_w', 22, 4), ('wr_tent_w', 26, 15), ('wr_tripod', 12, 4), ('wr_tripod', 16, 4), ('wr_tripod', 20, 3),
                     ('wr_dial', 10, 12), ('wr_dial', 23, 12), ('wr_telegraph', 30, 8), ('wr_telegraph', 30, 16), ('hb_crates4', 6, 15),
                     ('hb_boxes', 9, 17), ('sh_crates', 24, 19), ('hb_barrel', 13, 18), ('wr_ban_bone', 4, 10) if False else ('dk_boulder', 4, 10)):
        r.near(nm, x, y, on='su', r=3)
    CK.props(r, ['dk_rock_big', 'dk_boulder', 'dk_pebbles', 'nt_deadtree'], 10, box=(0, 0, W, H), on='su', clump=2, seed=5)
    r.dress(trees=('nt_deadtree',), n_trees=0, copses=0, scatter=0)
    r.paint()
    sand_dress(r, 0.50, seed=929, bones=0.02)
    ground_var(r, ['gs_crust0', 'gs_crust1', 'gs_crust2', 'gs_crust3'], 0.45, seed=1)
    decal(r, ['wr_rut0', 'wr_rut1', 'wr_bones0'], 0.05, seed=4)
    CK.scatter_quiet(r, 12)
    h = head(929, "The Observers' Mesa", field='DESERT', bgm='Route 9', biome='desert', tone=[16, 8, 0, 10])
    h['metadata']['MapPosition'] = [0, 13, 16]
    r.write(h, '929_observers_mesa.yaml', "# The Observers' Mesa (929). WRITTEN BY layouts/war.py (map builder 10) - edit that script.\n",
            '/tmp/craft/929.png' if PREV else None)


BUILD[929] = build_929


# ====================================================================================================== 930 The Bone-Carters' Camp
def build_930():
    """The Bone-Carters' Camp (44x32, DESERT): Ossaria's burial guild at the Dry Tide's west end, under the white bone-banner
    on its pole.  Burial carts in a line, the tally-wall of names (both armies'), the embalmers' tent, the elder's
    awning; old shell pavements of the dried sea under the sand.  W: the Glass Dunes (926).  E: the Dry Tide (810, not built:
    the road runs to a cairn).  Sigrun sets the PC down here in Ch19 (the landing stone by the banner)."""
    W, H = 44, 32
    r, m = desert(W, H, 930)
    dunes(r, 6, 930, box=(2, 2, 42, 10)); dunes(r, 5, 931, box=(2, 24, 42, 30))
    r.road([(0, 16.5), (10, 16), (22, 15.5), (32, 17), (43, 16.5)], w=3.0, c='u', open_=None, only='su.tT')
    m.blob(22, 18, 9, 5, 'g', seed=9301, rough=0.4, only='su')                     # the shell pavement of the old sea floor
    r.exit('W', 15, 4); r.exit('E', 15, 4)
    r.finish_plan(border=1)
    E = [FRONT,
         sign((40, 13), 'Road sign', "THE BONE-CARTERS' CAMP. E: the Dry Tide to Duneholt. W: the front. (Bone-carters walk where they like.)"),
         talk('Elder Ossa', (24, 11), 'NPC 28', ["Elder Ossa: We carry out the dead the armies leave. Ours by tomb-law, whoever they were.",
                                                "Elder Ossa: The carts can't reach the glass. If you walk where we can't, bring them home. One tally-stick each. We'll do the rest."]),
         talk('Embalmer', (33, 22), 'NPC 20', ["Embalmer: Salt, resin and a song. The song matters most. Nobody believes that until they hear it."], d='left'),
         talk('Carter', (12, 21), 'NPC 25', ["Carter: Isenmar boy, Ashkaar girl, same cart this morning. The sand doesn't sort them. Neither do we."], d='right'),
         talk('Carter ', (16, 12), 'NPC 03', ["Carter: White banner, white cloth, white bones. Both armies hold fire when they see white. Mostly."]),
         {'type': 'sign', 'name': 'Tally-wall', 'at': [28, 9], 'post': False,
          'text': 'The tally-wall: names in charcoal, rows on rows, Isenmar and Ashkaar mixed together in the order they were carried in. The newest row is still wet.'},
         {'type': 'sign', 'name': 'Landing stone', 'at': [21, 21], 'post': False,
          'text': "A flat stone scorched in a ring, where Sigrun's dragon sets down. Somebody has left a waterskin on it, for whoever comes next."},
         item((40, 28), 'FULLRESTORE'), hidden((6, 5), 'STARDUST', 'HiddenItem (dune)')]
    r.add(*E)
    r.seat_events(on='sug')
    for nm, x, y in (('wr_ban_bone', 22, 6), ('wr_ban_bone', 4, 13), ('wr_tally', 27, 7), ('wr_tent_bone', 31, 18), ('wr_tent_bone', 8, 22),
                     ('wr_tent_w', 36, 5), ('wr_bonecart', 12, 18), ('wr_bonecart', 15, 18), ('wr_bonecart', 18, 18), ('wr_well', 30, 24),
                     ('pf_wagon', 37, 24), ('hb_crates4', 35, 10), ('hb_tubs', 25, 24), ('fw_rack', 6, 9), ('fw_brazier', 21, 13), ('wr_bonecart', 40, 20)):
        r.near(nm, x, y, on='sug', r=3)
    CK.props(r, ['dk_rock_big', 'dk_boulder', 'dk_pebbles', 'nt_deadtree'], 14, box=(0, 0, W, H), on='su', clump=2, seed=5)
    r.dress(trees=('nt_deadtree',), n_trees=0, copses=0, scatter=0)
    r.paint()
    sand_dress(r, 0.48, seed=930, bones=0.04)
    ground_var(r, ['gs_crust0', 'gs_crust1', 'gs_crust2', 'gs_crust3'], 0.45, seed=1)
    decal(r, ['wr_bones0', 'wr_bones1', 'wr_rut0'], 0.05, on='sug', seed=4)
    CK.scatter_quiet(r, 12)
    h = head(930, "The Bone-Carters' Camp", field='DESERT', bgm='Route 9', biome='desert', tone=[14, 8, 0, 6],
             connections=[{'dir': 'W', 'offset': 15, 'to': 926, 'to_offset': 30}])
    h['metadata']['MapPosition'] = [0, 14, 3]
    r.write(h, '930_bone_carters_camp.yaml', "# The Bone-Carters' Camp (930). WRITTEN BY layouts/war.py (map builder 10) - edit that script.\n",
            '/tmp/craft/930.png' if PREV else None)


BUILD[930] = build_930

if __name__ == '__main__':
    ids = [int(a) for a in sys.argv[1:] if a.isdigit()] or sorted(BUILD)
    for i in ids:
        BUILD[i](); print('built', i)
