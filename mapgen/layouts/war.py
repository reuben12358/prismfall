#!/usr/bin/env python3
"""The war theatre in Ossaria's western dunes (WORLD.md 9, story/14_WAR_AND_BLESSING.md Part B), map builder 10.

SUPERSEDED (2026-11-26): the specs 920-930 are written by layouts/war_craft.py (Map Craft Wave 9), which also carries
the Ch19 "lines" events of story/38_SCRIPT_CH19.md (Trenchers / Hirdmen / Ember-Riders, partners v19 on 920 / 924 /
925; 926 is the beam clash only). This file still has the Rev 18 events (Soldier / Captain, the 926 partner double):
don't run it over the crafted maps.
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
import rimewood as RW
from terrain import vnoise

PREV = '--preview' in sys.argv
ONE = lambda n: int(np.array(STAMPS[n]['layers']).max())
FRONT = {'type': 'event', 'name': 'War front', 'at': [0, 0], 'fixed': True, 'pages': [{'trigger': 'parallel', 'commands': [
    {'script': "c = (pf_choice(:war_climax) rescue nil)\n$game_switches[605] = (c == :back_ashkaar)\n"
               "$game_switches[606] = (c == :back_isenmar)\n$game_switches[607] = (c == :stand_between)"}, {'wait': 60}]}]}


def desert(W, H, mid, base='u', kit='sdc'):
    """map builder 11: plateaus use the dune cliff kits of gdraw.py (sdc sandstone, gdc glassed), never the green rim"""
    r = Route(mid, W, H, 'shore', kit={1: kit, 2: kit, 3: kit, 'default': kit}, base=base)
    r.m.SEAL = K.P1({920: 'wr_sandbags', 924: 'wr_stakes', 929: 'wr_sacks', 930: 'wr_sacks'}.get(mid, 'gd_shard2'))   # no green bush on a desert edge
    return r, r.m


def dunes(r, n, seed, box=None, w=(5, 10), face='sand'):
    """dune crests: one-way sand ledges (their lee faces south, you slide down them) east-west across the sand"""
    m = r.m; rng = random.Random(seed)
    x0, y0, x1, y1 = box or (2, 2, r.W - 2, r.H - 2)
    for i in range(n):
        x = int(rng.uniform(x0, x1)); y = int(rng.uniform(y0, y1)); L = int(rng.uniform(*w))
        if all(m.cls[y, xx] in 'su' and not r.road_mask[y, xx] for xx in range(x, min(r.W - 1, x + L))):
            CK.ledge(r, x, min(r.W - 2, x + L), y, face=face)


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


# ---------------------------------------------------------------------------------------------- the glass kit (map builder 11)
from terrain import NB2AUTO


def blob(W, H, cx, cy, rx, ry, seed, rough=0.45):
    """a ragged ellipse (bool mask)"""
    yy, xx = np.mgrid[0:H, 0:W]
    q = ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2
    n = np.array([[vnoise(x, y, seed, 4.0) for x in range(W)] for y in range(H)])
    return q <= 1.0 + rough * (n - 0.5) * 2


def band(W, H, pts, w, seed, wob=0.45):
    """a winding band along a polyline whose width breathes with noise (flows, channels, scars)"""
    out = np.zeros((H, W), bool)
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = int(max(abs(x1 - x0), abs(y1 - y0)) * 3) + 1
        for i in range(n + 1):
            t = i / n; x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            ww = w * (1 + wob * (vnoise(int(x * 2), int(y * 2), seed, 3.0) - 0.5) * 2)
            for yy in range(int(y - ww - 1), int(y + ww + 2)):
                for xx in range(int(x - ww - 1), int(x + ww + 2)):
                    if 0 <= xx < W and 0 <= yy < H and (xx - x) ** 2 + (yy - y) ** 2 <= ww * ww: out[yy, xx] = True
    return out


def paint_glass(r, mask, cracks=0.05, rope=0.10, spill=0.04, seed=0):
    """after paint: fused glass over the sand.  Inner cells get the glass floor on layer 1 (props may stand on it);
    edge cells the glass sheet's edge overlay (48 shapes) on the top layer where nothing else is"""
    m = r.m; rng = random.Random(r.seed * 7 + seed)
    mask = mask & ~m.cliff
    GG = [K.P1('gd_g%d' % v) for v in range(4)]; GC = [K.P1('gd_gc0'), K.P1('gd_gc1')]
    FL = [K.P1('gd_floor_%02d' % i) for i in range(48)]
    RP = [K.P1('gd_rope%d' % v) for v in range(3)]; CR = [K.P1('gd_crack%d' % v) for v in range(2)]
    SP = [K.P1('gd_spill%d' % v) for v in range(2)]
    shape = mask | m.cliff                                                # no fused rim against a cliff or a ridge side
    for y, x in np.argwhere(mask):
        sh = NB2AUTO[CK.nbits(shape, x, y)]
        ground1 = m.L[1, y, x] == 0 or m.L[1, y, x] >= K.RC.VBASE           # empty, or a ground autotile (virtual id)
        if sh == 0:
            m.L[0, y, x] = rng.choice(GC) if rng.random() < cracks else GG[(x * 3 + y * 5 + int(vnoise(x, y, seed, 2.0) * 4)) % 4]
            if ground1: m.L[1, y, x] = 0
            if not m.L[2, y, x] and not m.taken[y, x] and not m.L[1, y, x]:
                k = rng.random()
                if k < rope * vnoise(x, y, seed + 3, 5.0) * 2: m.L[2, y, x] = rng.choice(RP)
                elif k > 1 - spill: m.L[2, y, x] = rng.choice(SP)
        elif not m.L[2, y, x] and ground1 and not m.taken[y, x]:
            m.L[2, y, x] = FL[sh]
    return mask


def plan_flood(r, mask):
    """plan time: flood channels are solid water (the gdraw flood tiles); keep props and events off them"""
    m = r.m
    for y, x in np.argwhere(mask):
        if r.road_mask[y, x]: continue
        m.taken[y, x] = True
    return mask & ~r.road_mask


def paint_flood(r, mask, steam=0.25, seed=0):
    """after paint: turquoise flood water in its dark wet bed (48 shapes) on layer 2, steam rising off the banks"""
    m = r.m; rng = random.Random(r.seed * 11 + seed)
    FW = [K.P1('gd_flood_%02d' % i) for i in range(48)]; ST = [K.P1('wr_steam%d' % v) for v in range(3)]
    for y, x in np.argwhere(mask):
        m.L[1, y, x] = FW[NB2AUTO[CK.nbits(mask, x, y)]]; m.L[2, y, x] = 0
    for y, x in np.argwhere(mask):
        for dx, dy in ((0, -1), (1, 0), (-1, 0)):
            X, Y = x + dx, y + dy
            if m.inb(X, Y) and not mask[Y, X] and not m.L[2, Y, X] and not m.L[1, Y, X] and not m.taken[Y, X] and rng.random() < steam * 0.3:
                m.L[2, Y, X] = rng.choice(ST)


# ---------------------------------------------------------------------------------------------- map builder 12: glass that reads as glass
def glass_dress(r, glass, sheen=0.07, sky=0.035, seed=0):
    """after paint_glass: the polish.  Specular streaks and glints (gd_sheen*) in drifting bands, the sky reflected in
    the open glass (gd_sky*), on inner glass cells nothing stands on"""
    m = r.m; rng = random.Random(r.seed * 13 + seed)
    SH = [K.P1('gd_sheen%d' % v) for v in range(4)]; SK = [K.P1('gd_sky%d' % v) for v in range(2)]
    for y, x in np.argwhere(glass):
        if m.L[2, y, x] or m.taken[y, x] or m.cliff[y, x] or m.L[1, y, x]: continue
        if not all(glass[yy, xx] for yy in range(max(0, y - 1), min(r.H, y + 2)) for xx in range(max(0, x - 1), min(r.W, x + 2))): continue
        band_ = vnoise(x + y, 0, r.seed + 31 + seed, 5.0)                    # glare runs in diagonal bands
        q = rng.random()
        if q < sheen * (0.4 + 1.4 * band_): m.L[2, y, x] = SH[(x + y) % 2] if rng.random() < 0.7 else SH[2 + (x % 2)]
        elif q < sheen * 1.8 + sky * vnoise(x, y, r.seed + 37 + seed, 7.0) * 2: m.L[2, y, x] = SK[(x // 5 + y // 4) % 2]


def glass_ledges(r, glass):
    """the dune slides turn to glass lips where they cross glass (same one-way passage, gdl_* instead of sdl_*)"""
    m = r.m
    for x0, x1, y in getattr(r, 'ledges', []):
        for x in range(x0, x1 + 1):
            if not m.inb(x, y): continue
            near = any(glass[yy, x] for yy in (y - 1, y, y + 1) if 0 <= yy < r.H)
            if near: m.L[1, y, x] = K.P1('gdl_' + ('w' if x == x0 else 'e' if x == x1 else 'm'))


def plan_ice(r, mask):
    """plan time: a frozen flood pool (ice, terrain tag 12: you slide).  Nothing is seated on it"""
    m = r.m
    mask = mask & ~r.road_mask & (m.ht == 0)
    for y, x in np.argwhere(mask): m.taken[y, x] = True
    return mask


def paint_ice(r, mask, stoppers=(), seed=0):
    """after paint: the frozen flood (gd_ice_* in the 48 shapes, tag 12) on layer 2; stoppers are glass shards frozen
    into it (solid, top layer); rime round the shore"""
    m = r.m; rng = random.Random(r.seed * 17 + seed)
    IC = [K.P1('gd_ice_%02d' % i) for i in range(48)]; FR = [K.P1('wr_frost%d' % v) for v in range(3)]
    for y, x in np.argwhere(mask):
        m.L[1, y, x] = IC[NB2AUTO[CK.nbits(mask, x, y)]]; m.L[2, y, x] = 0
    for x, y in stoppers: m.L[2, y, x] = K.P1('gd_shard2')
    for y, x in np.argwhere(mask):
        for dx, dy in ((0, -1), (1, 0), (-1, 0), (0, 1)):
            X, Y = x + dx, y + dy
            if m.inb(X, Y) and not mask[Y, X] and not m.L[2, Y, X] and not m.L[1, Y, X] and not m.taken[Y, X] and not m.cliff[Y, X] \
                    and rng.random() < 0.5:
                m.L[2, Y, X] = rng.choice(FR)


def ice_puzzle(r, mask, goal, seed=7, tries=3000):
    """stoppers on a frozen pool so that `goal` (a land cell on the far shore, walled off on foot) takes >= 3 slides
    from the near shore and the way back exists.  Returns the stopper cells (rimewood.slide_solve's rules)"""
    m = r.m; rng = random.Random(seed)
    cells = {(int(x), int(y)) for y, x in np.argwhere(mask)}
    land = set()
    for (x, y) in cells:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + dx, y + dy)
            if n not in cells and m.inb(*n) and m.cls[n[1], n[0]] in 'su' and not m.cliff[n[1], n[0]] and (not m.taken[n[1], n[0]] or n == goal): land.add(n)
    start = land - {goal}
    inner = sorted(cells)
    best = None
    for _ in range(tries):
        rocks = set(rng.sample(inner, min(len(inner) // 6, rng.randint(4, 9))))
        ice = cells - rocks
        k, _p = RW.slide_solve(ice, land, start, {goal})
        if k is None or k < 3: continue
        back, _q = RW.slide_solve(ice, land, {goal}, start)
        if back is None: continue
        sc = k * 10 - len(rocks)
        if best is None or sc > best[0]: best = (sc, rocks, k)
        if k >= 5: break
    if best is None: print('  (ice_puzzle: no layout)'); return set()
    print('  ice puzzle: %d stoppers, %d slides' % (len(best[1]), best[2]))
    return best[1]


def trail(r, pts, w=3.0, only='su.tT'):
    """a road over open sand: planned as a lane (so road_mask, ruts and the flood causeways know it) but painted as the
    sand itself - every Rejuvenation road autotile has a grass rim, which has no business in a desert"""
    m = r.m
    before = r.road_mask.copy()
    r.road(pts, w=w, c='d', open_=None, only=only)
    m.cls[r.road_mask & ~before & (m.cls == 'd')] = 'u'


def sand_seams(r):
    """after paint: the sand (Dirt) autotile is cut by every change of height, and its edge shapes carry a grass rim.
    Re-shape it so only water, flood and other autotiles count as a different region: plateaus, ledges and props sit
    on one unbroken sand sheet (map builder 11: the green rims on the war maps)"""
    m = r.m; V = K.RC.VBASE
    L1 = m.L[1]
    isdirt = np.zeros(L1.shape, bool)
    for val in np.unique(L1[L1 >= V]):
        if K.RC.vauto_name(int(val))[1] == 'Dirt': isdirt |= (L1 == val)
    other = (L1 >= V) & ~isdirt                                              # water, sea, other autotiles: real edges
    same = ~other & ~np.isin(m.cls, ['w', 'W'])
    base = None
    for y, x in np.argwhere(isdirt):
        base = int(L1[y, x]) - (int(L1[y, x]) - V) % 48
        m.L[1, y, x] = base + NB2AUTO[CK.nbits(same, x, y)]
    if base is not None:                                                     # the shore theme lays grass on layer 1 under
        L0 = m.L[0]                                                          # everything: under see-through kit pieces,
        grassy = (L0 > 0) & (L0 < V) & ~np.isin(m.cls, ['w', 'W'])            # props and decals it showed as green rims
        CR = [K.P1('gs_crust%d' % v) for v in range(4)]                       # (salt crust where the wind scoured it)
        for y, x in np.argwhere(grassy):
            n = vnoise(x, y, r.seed + 4242, 3.0)
            m.L[0, y, x] = CR[(x * 3 + y) % 4] if n > 0.55 and isdirt[y, x] else base     # (crust only under opaque sand)


def ridge(r, x0, x1, y0, y1, seed, h=1):
    """a glassed (or sandstone) dune ridge: a ragged plateau east-west, smoothed so the cliff kit reads cleanly"""
    CK.plateau(r, (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2, (y1 - y0) / 2, h, rough=0.35, seed=seed)


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
    # map builder 12: the north rim is a rime-glazed sandstone scarp (x 20-58) with Isenmar's watch line along its top,
    # reached by one stair between the second and third trench-lines; under it the sea that came over the dunes froze
    # in two pools you slide on (the Watch-post's Never-Melt Ice lies past the east one), with ice spires and frozen
    # wrecks; the sled-yard keeps the north-west
    for x in range(20, 59):
        top = 4 + int(round(2.2 * (vnoise(x, 0, 9202, 6.0) - 0.5) * 2))
        m.ht[:max(1, top) + 1, x] = 1
    CK.smooth_ht(m, 1, 2, box=(18, 0, 60, 10))
    dunes(r, 9, 920, box=(2, 20, 56, 33))
    dunes(r, 3, 921, box=(2, 3, 18, 9))
    road = [(0, 14.5), (12, 15), (24, 14), (36, 15.5), (48, 14.5), (59, 15)]
    trail(r, road, w=3.0)
    trail(r, [(10, 16), (8, 24), (8, 35)], w=3.0)           # south to the Glass Dunes
    trail(r, [(30, 16), (31, 22)], w=2.0, only='su.')
    r.exit('W', 13, 4); r.exit('E', 13, 4)
    pools = (blob(W, H, 25.5, 8.5, 4.5, 2.2, 92021, 0.3) | blob(W, H, 51.5, 9.0, 4.8, 2.3, 92022, 0.3)) & (m.ht == 0)
    for y in range(H):                                                     # (never across a trench-line)
        for x in (18, 32, 46): pools[y, x - 1:x + 2] = False
    ISLET = [(51, 9), (52, 9)]                                              # the Never-Melt Ice on an islet in the east pool
    for x, y in ISLET: pools[y, x] = False
    ice = plan_ice(r, pools)
    for x, y in ISLET: m.taken[y, x] = True
    GOAL920 = ISLET[1]
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
         hidden((26, 30), 'STARDUST', 'HiddenItem (rimed dune)'),
         obj('Frozen sea', (25, 11), ['The sea came over the dunes this far. The Glaceon lines froze it where it stood: a pool of green ice with the sand still in it.']),
         soldier((44, 2), 'Watch-post sergeant', 'NPC 28', ["Watch-post sergeant: Up here you can see Skaldfast burning and the Steamline smoking. Pick which to look at.",
                                                            "Sergeant: The ice on the flats? Slide it. The children of Skaldfast could, before."], d='down'),
         obj('Signal horn', (40, 2), ['A great horn of whale-bone on a frame. Blown once for the dragons, twice for the sea. Nobody has blown it twice yet.']),
         item((5, 28), 'FULLRESTORE')]
    for e in E: e.setdefault('fixed', e['type'] in ('trainer',))
    E.append(dict(item(ISLET[0], 'NEVERMELTICE'), fixed=True))
    r.add(*E)
    r.seat_events(on='su')
    yl = max(y for y in range(H) if m.ht[y, 39] == 1)
    CK.stair(r, 38, yl, w=3, h=1)
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
    CK.props(r, ['sk_rock_big', 'sk_boulder', 'sk_pebbles', 'nt_deadtree'], 22, box=(0, 18, W, H), on='su', clump=2, seed=5)
    CK.props(r, ['sk_boulder', 'sk_pebbles'], 10, box=(0, 0, W, 12), on='su', clump=2, seed=6)
    for nm, x, y in (('wr_supply', 5, 16), ('wr_supply', 27, 13), ('wr_sacks', 8, 13), ('wr_sacks', 30, 12), ('wr_rack', 16, 9),
                     ('wr_rack', 34, 9), ('wr_firering', 11, 7), ('wr_firering', 40, 6), ('wr_ban_ise_t', 47, 18), ('wr_glasssled', 52, 22),
                     ('wr_stakes', 20, 10), ('wr_stakes', 20, 19), ('wr_stakes', 34, 9), ('wr_stakes', 34, 21), ('wr_stakes', 48, 9), ('wr_stakes', 48, 19),
                     ('wr_sandbags', 17, 12), ('wr_sandbags', 31, 13), ('wr_sandbags', 45, 12), ('gd_shard2', 55, 25), ('gd_shard0', 57, 20)):
        r.near(nm, x, y, on='su', r=2)
    for nm, x, y in (('wr_sledfort2', 22, 1), ('wr_ban_ise', 27, 1), ('fw_brazier', 30, 2), ('wr_tent_b', 33, 0), ('wr_ban_ise', 47, 1),
                     ('wr_sledfort', 49, 2), ('fw_rack', 53, 1), ('wr_tent_w', 55, 0), ('fw_brazier', 36, 2), ('wr_sacks', 42, 3),
                     ('cr_clear_t', 21, 9), ('cr_blue_c', 30, 8), ('cr_clear_c', 29, 10), ('cr_blue_t', 48, 10), ('cr_clear_e', 56, 8),
                     ('fw_boat', 23, 11), ('fw_sled', 53, 12), ('gd_shard2', 45, 7), ('cr_blue_e', 34, 9)):
        r.near(nm, x, y, on='su', r=2)
    r.dress(trees=('nt_deadtree',), n_trees=0, copses=0, scatter=0)
    m.cls[m.cls == 'd'] = 'u'
    r.paint()
    sand_seams(r)
    stop = ice_puzzle(r, ice & (np.arange(W)[None, :] > 46), GOAL920, seed=9203) if GOAL920 else set()
    paint_ice(r, ice, stop, seed=920)
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
    h['walk_from'] = [list(GOAL920)]                                          # the islet: over the ice only
    h['gates'] = [{'name': 'The ice islet (sliding only)', 'from': [[1, 14], [58, 14], [8, 34]], 'sealed': [list(GOAL920)], 'ice_solid': True}]
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
    trail(r, [(0, 14.5), (14, 15), (24, 13.5), (31, 15), (40, 16.5), (52, 15), (63, 14.5)], w=3.0)
    trail(r, [(31, 16), (31, 24), (31.5, 31)], w=3.0)
    r.exit('W', 13, 4); r.exit('E', 13, 4); r.exit('S', 30, 4)
    # map builder 12: the west half is where Kyogre's sea reached the Isenmar lines and froze: two frozen flood pools
    # (you slide on them), ice-locked wrecks, a rime-glazed sandstone knoll with a lookout; the far spit of the south
    # pool (the Icestone) is reached only over the ice
    ridge(r, 3, 12, 3, 9, seed=11)                                              # the knoll (NW)
    CK.smooth_ht(m, 1, 2, box=(0, 0, 16, 12))
    nw = blob(W, H, 17.5, 6.0, 6.5, 3.2, 92511, 0.35) & (m.ht == 0)
    sw = blob(W, H, 12.0, 24.5, 9.5, 3.6, 92512, 0.3) & (m.ht == 0)
    SPIT = [(2, 23), (2, 24), (2, 25), (3, 24), (3, 25)]
    for x, y in SPIT: sw[y, x] = False
    for y in range(20, 30):                                                      # the spit is walled on foot: shards and ice spires
        for x in range(0, 5):
            if (x, y) not in SPIT and not sw[y, x] and not r.road_mask[y, x]: m.cls[y, x] = 'B'
    ice = plan_ice(r, nw | sw)
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
         hidden((33, 4), 'STARDUST', 'HiddenItem (the glass)'), item((60, 28), 'FIRESTONE'), dict(item((2, 24), 'ICESTONE'), fixed=True),
         obj('Frozen flood', (14, 20), ['The sea came this far. Then the Glaceon lines came out of their trenches and the sea stopped, mid-wave, and stayed.',
                                        'The ice is clear as a window. There are fish in it, and a boot, and the Isenmar standard, still upright.']),
         obj('Ice-locked whaleboat', (22, 9), ['A whaleboat from Skaldfast, frozen into the flood up to its gunwales. Its oars are still out.']),
         soldier((8, 11), 'Isenmar lookout', 'NPC 11', ["Isenmar lookout: From up here you see it all: the sea frozen on our side, the glass on theirs, and the steam where they meet."], d='down'),
         {'type': 'berry', 'at': [5, 13], 'berry': 'ASPEARBERRY'}]
    for e in E:
        if e.get('type') == 'item' and e.get('item') == 'ICESTONE': m.taken[24, 2] = True
    r.add(*E)
    r.seat_events(on='su')
    stop = ice_puzzle(r, sw & ice, (3, 24), seed=9251)
    yk = max(y for y in range(H) if m.ht[y, 7] == 1)
    CK.stair(r, 6, yk, w=3, h=1)
    rng = random.Random(925)
    CRY = ['cr_clear_c', 'cr_teal_c', 'cr_clear_e', 'cr_grey_c', 'cr_purple_c', 'cr_pink_c', 'cr_clear_t', 'cr_teal_e', 'cr_red_c', 'cr_blue_c']
    lanes = (5, 15, 24)                                                         # three quiet lanes through the glass belt (rows)
    for y in range(1, H - 1):
        for x in range(27, 37):
            if r.road_mask[y, x] or any(abs(y - ly) <= 1 for ly in lanes) or m.taken[y, x] or m.cls[y, x] not in 'su': continue
            if vnoise(x, y, 9251, 2.5) > 0.42 and rng.random() < 0.55:
                n = rng.choice(CRY)
                if m.free(x, y, 1, STAMPS[n]['h'], on='su'): m.stamp(n, x, y, mark='B')
    for nm, x, y in (('wr_sledfort2', 4, 3), ('wr_ban_ise', 10, 4), ('fw_brazier', 7, 6), ('wr_tent_b', 18, 25) if False else ('fw_rack', 21, 18),
                     ('fw_boat', 21, 8), ('cr_clear_t', 11, 10), ('cr_blue_c', 24, 5), ('cr_clear_c', 13, 3), ('cr_blue_e', 25, 7),
                     ('cr_clear_t', 22, 22), ('cr_blue_c', 21, 27), ('cr_clear_e', 4, 21), ('cr_blue_t', 1, 27), ('fw_sled', 16, 19),
                     ('wr_sledfort', 23, 28), ('wr_ban_ise_t', 18, 28), ('fw_wood', 14, 18), ('wr_sacks', 20, 17),
                     ('fw_sled', 8, 17), ('wr_ban_ise', 12, 9), ('fw_rack', 6, 28), ('ak_rock2', 15, 29),
                     ('wr_picket', 50, 9), ('wr_picket', 53, 9), ('wr_picket', 56, 9), ('wr_ban_ash', 51, 20), ('wr_sledfort', 57, 24),
                     ('nr_colfall', 46, 26), ('pf_wagon', 42, 6)):
        r.near(nm, x, y, on='su', r=3)
    CK.props(r, ['sk_rock_big', 'sk_boulder', 'sk_pebbles', 'nt_deadtree'], 14, box=(0, 0, W, H), on='su', clump=2, seed=5)
    for nm, x, y in (('wr_ban_ise_t', 22, 10), ('wr_ban_ash_t', 41, 10), ('wr_treb_broken', 44, 24), ('wr_glasssled', 20, 23),
                     ('gd_pool2', 25, 20), ('gd_pool3', 36, 5), ('wr_stakes', 24, 16), ('wr_stakes', 39, 13), ('wr_sandbags', 16, 16),
                     ('wr_pal_hb', 48, 12), ('wr_pal_hb', 49, 12), ('wr_pal_h', 50, 12), ('wr_supply', 56, 18), ('wr_sacks', 9, 16)):
        r.near(nm, x, y, on='su', r=2)
    CK.props(r, ['gd_shard0', 'gd_shard1', 'gd_shard2'], 18, box=(24, 0, 40, H), on='su', clump=2, seed=12)
    r.dress(trees=('nt_deadtree',), n_trees=0, copses=0, scatter=0)
    m.cls[m.cls == 'd'] = 'u'
    r.paint()
    sand_seams(r)
    glass = paint_glass(r, band(W, H, [(31, 0), (30, 9), (32, 19), (31, 31)], 3.6, 92501) | blob(W, H, 47, 6, 5, 3, 92513, 0.45)
                        | blob(W, H, 52, 24, 5, 3, 92514, 0.45), cracks=0.08, rope=0.10, seed=925)
    glass_dress(r, glass, seed=925); glass_ledges(r, glass)
    paint_ice(r, ice, stop, seed=925)
    for y, x in np.argwhere(m.cls == 'B'):                                       # the spit's wall: shards and spires frozen in rime
        if x < 6 and m.L[1, y, x] == 0 and m.L[2, y, x] == 0: m.L[1, y, x] = K.P1('gd_shard2')
    sand_dress(r, 0.35, seed=925)
    frozen_ground(r, [(x, y) for y in range(H) for x in range(0, 27 + int(3 * vnoise(0, y, 9252, 4.0))) if not ice[y, x]], thr=0.25)
    decal(r, ['wr_frost0', 'wr_frost1', 'wr_frost2'], 0.35, seed=1, cells=[(x, y) for y in range(H) for x in range(0, 28) if not ice[y, x]])
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
    h['walk_from'] = [[3, 25]]                                                     # the spit: over the ice only
    h['gates'] = [{'name': 'The Icestone spit (over the frozen flood only)', 'from': [[1, 14], [62, 14], [31, 30]], 'sealed': [[3, 24]], 'ice_solid': True}]
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
    trail(r, [(0, 19.5), (12, 19.5), (24, 20), (36, 19), (48, 20), (55, 19.5)], w=3.0)
    trail(r, [(20, 21), (14, 30), (8, 39)], w=3.0)
    for y0 in (10, 28):
        trail(r, [(24, y0), (50, y0)], w=2.0, only='su.')
    trail(r, [(36, 20), (36, 14)], w=3.0, only='su.')
    for cx, cy, rx, ry in ((30, 17, 4, 1.6), (44, 18, 5, 1.8), (27, 34, 4, 1.5)):          # drill yards: trodden gravel
        pass                                                                          # (drill yards: trodden decals after paint)
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
    CK.props(r, ['sk_rock_big', 'sk_boulder', 'sk_pebbles'], 10, box=(0, 0, 10, H), on='su', clump=2, seed=5)
    for x in range(24, 54):                                              # the camp's palisade, north and south, burnt in places
        for y in (2, 37):
            if not m.taken[y, x] and m.cls[y, x] in 'su' and not r.road_mask[y, x] and x % 9: m.stamp('wr_pal_hb' if (x + y) % 4 == 0 else 'wr_pal_h', x, y, mark='B')
    for nm, x, y in (('wr_supply', 50, 24), ('wr_supply', 38, 33), ('wr_sacks', 48, 29), ('wr_sacks', 32, 31), ('wr_rack', 27, 21),
                     ('wr_rack', 43, 16), ('wr_firering', 31, 28), ('wr_ban_ash_t', 9, 9), ('wr_ban_ash_t', 9, 29), ('wr_stakes', 8, 16),
                     ('wr_stakes', 8, 23), ('wr_stakes', 18, 15), ('wr_stakes', 18, 25), ('gd_shard2', 4, 8), ('gd_shard0', 5, 31)):
        r.near(nm, x, y, on='su', r=2)
    r.dress(trees=('nt_deadtree',), n_trees=0, copses=0, scatter=0)
    m.cls[m.cls == 'd'] = 'u'
    r.paint()
    sand_seams(r)
    g924 = paint_glass(r, blob(W, H, 48, 13, 5, 3, 92401) | blob(W, H, 4, 20, 4, 7, 92402) | blob(W, H, 44, 26, 3, 2, 92403),
                       cracks=0.12, rope=0.1, seed=924)                   # sand fired to glass round the dragon lines and forge
    glass_dress(r, g924, seed=924); glass_ledges(r, g924)
    sand_dress(r, 0.40, seed=924)
    decal(r, ['wr_ember0', 'wr_ember1', 'wr_ember2'], 0.30, on='sug', seed=2)
    for cx, cy, rx, ry in ((30, 17, 4, 1.6), (44, 18, 5, 1.8), (27, 34, 4, 1.5)):        # drill yards: trodden sand
        decal(r, ['wr_rut0', 'wr_rut1'], 0.7, seed=cx, cells=[(x, y) for y in range(H) for x in range(W) if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 < 1])
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
    """The Glass Dunes (60x48, DESERT; the battlefield of the climax, WAR-1), rebuilt by map builder 11 to the Glass
    Dunes / Flooded Dunes backdrops: a war-scarred desert turned to black-green glass.

    The crest (north middle) is the beam scar: fused glass between two glassed ridges (W x 13-17, E x 43-47), reached
    only from the Steamline (N, x 28-31) and left one way, down the glass lee ledge (y 14).  The flood came in from the
    west: turquoise channels braid across the Isenmar flats, crossed only where the caravan road runs over a fused-glass
    causeway (the choke point), steaming where they met the fire; the frozen wave stands where Isenmar's ice caught it.
    The east is glassed: fused-glass flows pour off the crest toward the bone-carters' road, glassed dune ridges with
    stairs up to lookouts, Ashkaar's burnt palisade and camp.  No-man's-land between: broken siege engines, the wells,
    stake lines with one gap (the south lane), wrecked sleds sunk in glass, supply carts along the road.
    NW warp: the Rimed Sands (920); NE warp: the Siege Camp (924); E: the bone-carters' camp (930); S: the goat-path
    to the Observers' Mesa (929, after the battle).  Ch19 events on the crest: the crest singles, the partner double
    and the legend, then WAR-1 (unchanged from map builder 10)."""
    W, H = 60, 48
    r, m = desert(W, H, 926, kit='gdc')
    # ---- plan: roads first (ridges and water keep off them)
    trail(r, [(29.5, 0), (30, 6), (30, 12)], w=3.0)                       # Steamline -> crest
    trail(r, [(7, 1), (9, 12), (14, 22), (24, 28), (36, 30), (48, 31), (59, 31.5)], w=3.0)
    trail(r, [(51, 1), (50, 12), (47, 22), (44, 30)], w=3.0)
    trail(r, [(30, 31), (30, 40), (30, 46)], w=2.0, only='su.')
    trail(r, [(16, 40.5), (10, 41), (4, 41.5)], w=2.0)                    # sally port -> the blue camp
    r.exit('N', 28, 4); r.exit('E', 30, 4)
    # the crest's glassed side ridges (exact: they seal the crest) and the glassed dune ridges of the flats
    def crest_sides():                                                  # ragged outer flanks, an exact sealed core
        for x0, x1, out in ((13, 17, -1), (43, 47, 1)):
            for y in range(0, 13):
                for x in range(x0, x1 + 1): m.ht[y, x] = 1
                bump = int(2.6 * vnoise(x0, y, 9267, 3.0))
                for k in range(1, bump + 1):
                    xx = (x0 - k) if out < 0 else (x1 + k)
                    if 0 <= xx < W and not r.road_mask[y, xx]: m.ht[y, xx] = 1
    crest_sides()
    ridge(r, 16, 25, 33, 38, seed=1)                                   # the west lookout ridge (stair from the lane)
    ridge(r, 34, 43, 36, 41, seed=2)
    ridge(r, 51, 58, 16, 22, seed=3)                                   # the east lookout ridge (stair from the lane)
    ridge(r, 49, 57, 38, 43, seed=4)
    for x0, x1, y0, y1 in ((16, 25, 31, 40), (34, 43, 34, 43), (51, 58, 14, 24), (49, 57, 36, 45)):  # never over a road
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if r.road_mask[max(0, y - 1):y + 4, max(0, x - 1):x + 2].any(): m.ht[y, x] = 0
    for x0, x1, y0, y1 in ((16, 25, 31, 40), (34, 43, 34, 43), (51, 58, 14, 24), (49, 57, 36, 45)):
        CK.smooth_ht(m, 1, 2, box=(x0 - 1, y0 - 1, x1 + 2, y1 + 2))
    CK.smooth_ht(m, 1, 2, box=(8, 0, 20, 14)); CK.smooth_ht(m, 1, 2, box=(41, 0, 53, 14))
    for x0, x1 in ((13, 17), (43, 47)):                               # (smoothing never opens the crest's sealed core)
        for y in range(0, 13):
            for x in range(x0, x1 + 1): m.ht[y, x] = 1
        for x in range(x0, x1 + 1): m.ht[13:, x] = np.minimum(m.ht[13:, x], m.ht[13:, x])
    for sx, ex, ey in ((20, 29, None), (53, 48, None)):                # a stair up each lookout ridge, a spur from the road
        col = [y for y in range(14, H) if m.ht[y, sx + 1] == 1]
        if not col: continue
        lip = max(col); CK.stair(r, sx, lip, w=3)
        foot = lip + 4
        trail(r, [(ex, foot + 0.5), (sx + 1, foot + 0.5)], w=2.0, only='su.')
    # the flood: braided channels across the western flats (Kyogre's sea, dragged in over the dunes)
    flood = band(W, H, [(0, 13), (3, 15), (5, 20), (10, 24), (16, 26), (19, 30)], 1.25, 9261) | \
            band(W, H, [(0, 26), (5, 28), (8, 33), (7, 38), (11, 43), (13, 47)], 1.35, 9262) | \
            band(W, H, [(5, 28), (2, 34), (0, 37)], 1.0, 9263)
    flood &= (m.ht == 0)
    flood = plan_flood(r, flood)
    dunes(r, 7, 9268, box=(19, 21, 47, 31), w=(4, 8)); dunes(r, 5, 9269, box=(44, 32, 58, 37), w=(4, 7))   # one-way dune slides
    dunes(r, 4, 9270, box=(14, 41, 28, 46), w=(4, 7))
    r.finish_plan(border=1)
    E = [FRONT,
         {'type': 'warp', 'name': 'To the Rimed Sands', 'at': [7, 1], 'link': 'WAR_RIMED_DUNES', 'arrive': [7, 2, 'down'], 'fixed': True},
         {'type': 'warp', 'name': 'To the Siege Camp', 'at': [51, 1], 'link': 'WAR_CAMP_DUNES', 'arrive': [51, 2, 'down'], 'fixed': True},
         sign((27, 1), 'Field marker', 'THE CREST. Below it, the caravan road and the wells. Above it, everything else.'),
         obj('Caravan well', (36, 33), ['A caravan well between the lines. A white ribbon on the sweep: the bone-carters\' sign. No blood at a well. Both armies keep that.']),
         obj('Caravan well ', (18, 26), ['The second well, its bucket gone, its rope cut. Someone has left a full waterskin on the rim for whoever comes next.']),
         obj("Bone-carters' banner", (40, 9), ['The bone-carters\' white banner on the crest\'s east shoulder. Under it, a tally-stick for every soldier carried off the sand. Both armies\' names.']),
         obj('Wrecked sled', (10, 18), ['An Isenmar sled-fort, overturned, its runners in the air, burnt to the iron on the eastern side.']),
         obj('The frozen wave', (5, 9), ['A wave, taller than a house, standing on dry sand. It broke over the dunes at noon and the ice caught it before it landed.',
                                         'Inside the curl the light is green. Something small and silver is frozen in it, mid-leap. A Feebas, maybe.']),
         obj('The causeway', (13, 22), ['Where the caravan road crosses the flood the sand has run to glass a yard thick: the only dry way over the water for a mile.']),
         obj('Steaming pool', (24, 21), ['Flood water in a basin of glass, still too hot to touch. It hisses where the edge is thinnest.']),
         obj('Broken trebuchet', (38, 18), ['An Ashkaar trebuchet, its arm snapped clean. The far side of it has run like candle wax and set hard as green glass.']),
         talk('Bone-carter', (40, 37) if False else (31, 35), 'NPC 27', ["Bone-carter: We carry them out. Whose they were doesn't matter. Whose they are now does: Ossaria's. Tomb-law."], d='left'),
         talk('Ashkaar straggler', (54, 27), 'NPC 21', ["Ashkaar straggler: The palisade burnt from the inside. Our own fire. Reshiram doesn't take sides; it takes everything."], d='left'),
         talk('Isenmar straggler', (6, 40), 'NPC 11', ["Isenmar straggler: The sea came over the dunes like it had somewhere to be. We built the trench to keep fire out. Not water."], d='right'),
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
         {'type': 'event', 'name': 'The legend', 'at': [30, 2], 'fixed': True, 'pages': [{'commands': []}]},
         item((56, 44) if False else (23, 34), 'FULLRESTORE'), hidden((2, 43), 'STARDUST', 'HiddenItem (dunes)'),
         hidden((38, 4), 'BIGNUGGET', 'HiddenItem (the crest)'), item((55, 17), 'HYPERPOTION'),
         hidden((7, 14), 'NEVERMELTICE', 'HiddenItem (behind the wave)'), item((58, 46), 'MAXREVIVE')]
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
    # the frozen wave and the big set pieces go down before the events are seated
    m.stamp('gd_wave', 1, 6, mark='B')                                  # north-west, beside the Rimed Sands road
    r.add(*E)
    r.seat_events(on='su')
    # the crest's lee: one way down the glass to the flats
    for x in range(18, 43):
        m.over.append((1, x, 14, K.P1('gdl_' + ('w' if x == 18 else 'e' if x == 42 else 'm')))); m.taken[14, x] = True
        if m.cls[14, x] not in 'su': m.cls[14, x] = 'u'
    for nm, x, y in (('wr_treb_broken', 37, 16), ('wr_treb_broken', 22, 16), ('wr_tower_wreck', 39, 25), ('wr_glasssled', 15, 30),
                     ('wr_glasssled', 26, 43), ('wr_sledfort', 8, 16), ('gd_pool3', 23, 19), ('gd_pool2', 34, 20), ('gd_pool2', 10, 28),
                     ('gd_pool3', 2, 22), ('wr_well', 35, 31), ('wr_well', 17, 24), ('wr_ban_bone', 41, 8), ('wr_ban_ise_t', 19, 16),
                     ('wr_ban_ash_t', 41, 16), ('wr_ban_ise', 11, 30), ('wr_ban_ise', 11, 38), ('wr_ban_ash', 49, 26), ('wr_ban_ash', 56, 36),
                     ('wr_bonecart', 32, 33), ('wr_bonecart', 27, 37), ('wr_supply', 40, 33), ('wr_supply', 52, 28), ('wr_supply', 18, 23),
                     ('pf_wagon', 45, 34), ('wr_tally', 48, 38), ('wr_picket', 55, 30), ('nr_colfall', 54, 46), ('fw_sled', 4, 30),
                     # the north-west: Isenmar's forward post where the wave caught them; the north-east: Ashkaar's dragon lines
                     ('wr_sledfort2', 1, 12), ('fw_brazier', 5, 14), ('wr_ban_ise_t', 11, 9), ('cr_clear_t', 8, 6), ('cr_blue_c', 0, 4),
                     ('wr_treb_broken', 53, 4), ('wr_picket', 50, 9), ('wr_picket', 56, 10), ('wr_picket', 58, 7), ('wr_ban_ash_t', 49, 4),
                     ('wr_sandbags', 54, 13), ('wr_sacks', 57, 13), ('wr_rack', 52, 11)):
        r.near(nm, x, y, on='su', r=3)
    # Isenmar's trench line on the flats (sandbags, two sally ports) and the blue camp in the south-west
    for y in range(29, 46):
        if y in (33, 34, 40, 41): continue
        if not m.taken[y, 13] and m.cls[y, 13] in 'su' and not r.road_mask[y, 13]: m.stamp('wr_sandbags', 13, y, mark='B')
    for nm, x, y in (('wr_tent_b', 2, 38), ('wr_tent_b', 6, 43), ('wr_tent_w', 9, 38), ('wr_firering', 6, 41), ('wr_rack', 10, 43),
                     ('wr_sacks', 3, 45), ('wr_sacks', 11, 46), ('fw_brazier', 8, 36)):
        r.near(nm, x, y, on='su', r=2)
    # Ashkaar's burnt palisade south of the east ridge (a gate where the lookout lane runs) and the red camp
    for x in range(48, 59):
        if 51 <= x <= 53: continue
        if not m.taken[26, x] and m.cls[26, x] in 'su' and not r.road_mask[26, x]: m.stamp('wr_pal_hb' if x % 3 else 'wr_pal_h', x, 26, mark='B')
    for nm, x, y in (('wr_tent_r', 50, 41) if False else ('wr_tent_r', 49, 44), ('wr_tent_r', 54, 45) if False else ('wr_tent_r', 52, 44),
                     ('wr_firering', 56, 44), ('wr_rack', 58, 42), ('wr_sacks', 47, 46), ('wr_picket', 57, 38)):
        r.near(nm, x, y, on='su', r=2)
    # stake lines across no-man's-land: one gap, where the south lane runs
    for y, xs in ((35, range(19, 29)), (35, range(32, 34)), (40, range(32, 34))):
        for x in xs:
            if not m.taken[y, x] and m.cls[y, x] in 'su' and not r.road_mask[y, x] and m.ht[y, x] == 0: m.stamp('wr_stakes', x, y, mark='B')
    CK.props(r, ['gd_spire', 'gd_shard0', 'gd_shard1', 'gd_shard2', 'cr_clear_c'], 26, box=(18, 0, 43, 14), on='su', clump=2, seed=6)   # the beam scar
    CK.props(r, ['gd_spire', 'gd_shard0', 'gd_shard1', 'gd_shard2', 'cr_teal_c', 'cr_clear_t'], 34, box=(18, 14, W, H), on='su', clump=2, seed=7)
    CK.props(r, ['gd_shard2', 'cr_teal_c', 'cr_clear_c', 'sk_pebbles'], 14, box=(0, 14, 30, H), on='su', clump=2, seed=8)
    CK.props(r, ['gd_shard0', 'gd_shard1', 'gd_shard2'], 10, box=(13, 0, 18, 12), on='su', seed=9)
    CK.props(r, ['gd_shard0', 'gd_shard1', 'gd_shard2'], 10, box=(43, 0, 48, 12), on='su', seed=10)
    CK.props(r, ['sk_rock_big', 'sk_boulder', 'sk_pebbles'], 8, box=(0, 0, W, H), on='su', clump=2, seed=5)
    CK.props(r, ['wr_firering', 'wr_sacks', 'wr_rack', 'wr_stakes', 'fw_sled', 'wr_sandbags'], 12, box=(18, 20, 48, 34), on='su', clump=3, seed=11)
    r.dress(trees=('nt_deadtree',), n_trees=0, copses=0, scatter=0)
    m.cls[m.cls == 'd'] = 'u'                                          # (stair landings: sand, not the grass-rimmed dirt)
    r.paint()
    sand_seams(r)
    # ---- glass: the crest's beam scar, the flows off its lee, the glassed ridges and the east
    glass = blob(W, H, 30, 7, 12, 7.5, 92601, 0.35) | (m.ht == 1)
    glass |= band(W, H, [(23, 15), (25, 20), (22, 25), (20, 29)], 2.0, 92602)
    glass |= band(W, H, [(31, 15), (31, 21), (33, 26), (36, 29)], 1.9, 92603)
    glass |= band(W, H, [(37, 15), (41, 20), (46, 25), (52, 29), (58, 31)], 2.4, 92604)
    glass |= blob(W, H, 52, 21, 7, 5, 92605, 0.4) | blob(W, H, 45, 40, 6, 4, 92606, 0.45) | blob(W, H, 37, 22, 4, 3, 92607)
    glass |= blob(W, H, 55, 7, 5, 4, 92608, 0.45)                       # the dragon lines, scorched to glass
    # map builder 12: the beam's splash reaches the south flats and the no-man's-land (the open sand was most of the map)
    glass |= blob(W, H, 24, 41, 7, 3.5, 92609, 0.45) | blob(W, H, 39, 44, 7, 3, 92610, 0.45) | blob(W, H, 21, 33, 4, 2.5, 92611, 0.5)
    glass |= band(W, H, [(30, 15), (29, 24), (30, 31), (30, 40)], 1.6, 92612) | blob(W, H, 13, 3, 4, 2.5, 92613, 0.4)
    glass |= blob(W, H, 47, 13, 3, 2, 92614, 0.4) | blob(W, H, 4, 25, 3, 2.5, 92615, 0.5)
    glass &= ~flood
    paint_flood(r, flood, steam=0.5)
    glass = paint_glass(r, glass, cracks=0.07, rope=0.10, spill=0.05, seed=926)
    glass_dress(r, glass, sheen=0.08, sky=0.04, seed=926); glass_ledges(r, glass)
    rest = [(x, y) for y in range(H) for x in range(W) if not glass[y, x] and not flood[y, x]]
    restset = set(rest)
    sand_dress(r, 0.40, seed=926, bones=0.03) if False else None
    RIP = [K.P1('wr_ripple%d' % v) for v in range(3)]; RU = [K.P1('wr_rut%d' % v) for v in range(2)]
    rng = random.Random(9264)
    for x, y in rest:                                                   # wind ripples on the sand that is still sand
        if m.L[2, y, x] or m.cliff[y, x] or m.taken[y, x] or m.cls[y, x] not in 'su': continue
        if r.road_mask[y, x]:
            if rng.random() < 0.85: m.L[2, y, x] = RU[(x + y) % 2]
        elif vnoise(x, y, 9265, 4.0) > 0.55 and rng.random() < 0.8: m.L[2, y, x] = RIP[(x // 3 + y) % 3]
    frozen_ground(r, [c for c in rest if c[0] < 16 + int(3 * vnoise(0, c[1], 9266, 4.0))], thr=0.40)
    frozen_ground(r, [c for c in rest if (c[0] - 4) ** 2 / 64.0 + (c[1] - 9) ** 2 / 49.0 < 1], thr=-1)     # rime round the wave
    decal(r, ['wr_frost0', 'wr_frost1', 'wr_frost2'], 0.55, seed=6, cells=[c for c in rest if (c[0] - 4) ** 2 / 81.0 + (c[1] - 9) ** 2 / 64.0 < 1])
    decal(r, ['wr_frost0', 'wr_frost1', 'wr_frost2'], 0.20, seed=1, cells=[c for c in rest if c[0] < 18])
    decal(r, ['wr_trench0', 'wr_trench1'], 1.0, seed=3, cells=[(12, y) for y in range(29, 46) if (12, y) in restset])
    decal(r, ['wr_ember0', 'wr_ember1', 'wr_ember2'], 0.22, seed=2, cells=[c for c in rest if c[0] > 42])
    decal(r, ['wr_bones0', 'wr_bones1'], 0.025, seed=4, cells=rest)
    decal(r, ['wr_steam0', 'wr_steam1', 'wr_steam2'], 0.35, seed=5,
          cells=[(x + dx, y + dy) for (nm, x, y) in m.stamps if nm.startswith('gd_pool') for dx in range(-1, 4) for dy in (-1, 0, 2)])
    CK.scatter_quiet(r, 6)
    h = head(926, 'The Glass Dunes', field='DESERT', bgm='Route 9', biome='desert',
             connections=[{'dir': 'N', 'offset': 0, 'to': 925, 'to_offset': 2}, {'dir': 'E', 'offset': 30, 'to': 930, 'to_offset': 15}],
             tone=[6, 10, 4, 14], fog={'name': 'prismfall_seamist', 'opacity': 30, 'blend': 0, 'zoom': 200, 'sx': 1, 'sy': 0})
    h['metadata']['MapPosition'] = [0, 13, 15]
    h['gates'] = [{'name': 'The crest (only from the Steamline)', 'from': [[56, 31], [7, 3], [51, 3]], 'sealed': [[30, 4], [30, 6]]}]
    r.write(h, '926_glass_dunes.yaml', '# The Glass Dunes (926). WRITTEN BY layouts/war.py (map builders 10 and 11) - edit that script.\n',
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
    # map builder 11: the pavilion furnished - pillars down the nave, war drapes, the archive of campaign maps, lanterns
    for x in (5, 18):
        for y in (7, 11): h.obj('pillar', x, y)
    for x in (4, 19): h.obj('drape', x, 3)
    h.obj('shelf', 14, 2); h.obj('shelf', 16, 2)                                                 # campaign maps in their cases
    for x, y in ((3, 6), (20, 6), (8, 13), (15, 13)): h.obj('lantern', x, y)
    h.obj('rug_mg', 9, 12); h.obj('urn', 21, 11); h.obj('couch_r', 18, 12) if False else None
    h.obj('awning', 10, 3) if False else None
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
    trail(r, [(17, 27), (17, 20), (17, 12), (12, 8)], w=2.0, only='su')
    trail(r, [(17, 14), (26, 10)], w=2.0, only='su')
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
                     ('hb_boxes', 9, 17), ('sh_crates', 24, 19), ('hb_barrel', 13, 18), ('wr_ban_bone', 4, 10) if False else ('sk_boulder', 4, 10)):
        r.near(nm, x, y, on='su', r=3)
    CK.props(r, ['sk_rock_big', 'sk_boulder', 'sk_pebbles', 'nt_deadtree'], 10, box=(0, 0, W, H), on='su', clump=2, seed=5)
    for nm, x, y in (('wr_supply', 25, 19), ('wr_sacks', 7, 17), ('wr_firering', 19, 16)):
        r.near(nm, x, y, on='su', r=2)
    r.dress(trees=('nt_deadtree',), n_trees=0, copses=0, scatter=0)
    m.cls[m.cls == 'd'] = 'u'
    r.paint()
    sand_seams(r)
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
    trail(r, [(0, 16.5), (10, 16), (22, 15.5), (32, 17), (43, 16.5)], w=3.0)
    pass                                                                          # (the shell pavement: crust ground after paint)
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
    CK.props(r, ['sk_rock_big', 'sk_boulder', 'sk_pebbles', 'nt_deadtree'], 14, box=(0, 0, W, H), on='su', clump=2, seed=5)
    for nm, x, y in (('wr_supply', 38, 13), ('wr_sacks', 34, 13), ('wr_firering', 26, 15), ('wr_sacks', 9, 20), ('wr_rack', 29, 21)):
        r.near(nm, x, y, on='su', r=2)
    r.dress(trees=('nt_deadtree',), n_trees=0, copses=0, scatter=0)
    m.cls[m.cls == 'd'] = 'u'
    r.paint()
    sand_seams(r)
    sand_dress(r, 0.48, seed=930, bones=0.04)
    ground_var(r, ['gs_crust0', 'gs_crust1', 'gs_crust2', 'gs_crust3'], 0.45, seed=1)
    ground_var(r, ['gs_crust0', 'gs_crust1', 'gs_crust2', 'gs_crust3'], -1, seed=2, cells=[(x, y) for y in range(H) for x in range(W) if ((x - 22) / 9.0) ** 2 + ((y - 18) / 5.0) ** 2 < 1])
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
