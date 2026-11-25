#!/usr/bin/env python3
"""layouts/war_craft.py — Rejuvenation V14 Map Craft Wave 9: Ch19 War & Desert Frontline Suite.

Revamps ALL 7 War Frontline Maps while preserving 100% of HEAD event, warp, trainer, puzzle-gate,
and map-connection parity:
  920 The Rimed Sands       (60x36, ts 56) — Wind-sculpted frost dunes, fortified Isenmar trenches,
                                             north watch-scarp, meltwater ice pools & sled-yard
  924 Ashkaar Siege Camp    (56x40, ts 56) — Layered obsidian-glass earthworks, siege trebuchets,
                                             regimental tent compounds, dragon pickets & field forge
  925 The Steamline         (64x32, ts 56) — Dramatic thermal rift valley where frost meets magma,
                                             obsidian canyon shoulders, geyser vents & timber bridges
  926 The Glass Dunes       (60x48, ts 56) — Climax WAR-1 vitrified-glass amphitheater, frozen wave,
                                             braided turquoise flood channels & glass causeway
  928 Command Pavilion      (24x18, ts 59) — Void-sculpted imperial crimson-gold war pavilion with
                                             mahogany map table, flaming oath-braziers & iron cage
  929 The Observers' Mesa   (36x28, ts 56) — Multi-tiered organic sandstone mesa, scenic north rim,
                                             signal cairns, survey tripods & cliff overlook
  930 The Bone-Carters' Camp(44x32, ts 56) — Wind-sheltered sandstone hollow, ancient shell pavement,
                                             whalebone & skull relics, scorched dragon landing stone

Run:
    PRISMFALL_GFX=/home/antigravity/pf_engine_run/game/Graphics /usr/bin/python3 -I mapgen/layouts/war_craft.py
"""
import os
import sys
import math
import random
import numpy as np
import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import rkit as K
from rkit import STAMPS, P1
import routekit as RK
from routekit import Route, trainer, npc, sign, item, hidden, talk, head
import craftkit as CK
from routes_early import obj
import rimewood as RW
from terrain import vnoise, NB2AUTO
from cavekit import Cave, FLOOR, TER, MASS

def make_front():
    return {
        'type': 'event',
        'name': 'War front',
        'at': [0, 0],
        'fixed': True,
        'pages': [{'trigger': 'parallel', 'commands': [
            {'script': "c = (pf_choice(:war_climax) rescue nil)\n"
                       "$game_switches[605] = (c == :back_ashkaar)\n"
                       "$game_switches[606] = (c == :back_isenmar)\n"
                       "$game_switches[607] = (c == :stand_between)"},
            {'wait': 60},
        ]}],
    }

SPRITE = {
    'ISENMAR_SOLDIER_M': 'trainer_POKEMONRANGER_M',
    'ISENMAR_SOLDIER_F': 'trainer_POKEMONRANGER_F',
    'ISENMAR_OFFICER': 'trainer_COOLTRAINER_M',
    'ASHKAAR_SOLDIER_M': 'trainer_BLACKBELT',
    'ASHKAAR_SOLDIER_F': 'trainer_CRUSHGIRL',
    'ASHKAAR_OFFICER': 'trainer_TAMER',
    'LEADER_SIGRUN': 'trainer_ELITEFOUR_Lance',
    'LEADER_MARISOL': 'trainer_LEADER_Misty',
    'DOMINAR': 'trainer_LEADER_Giovanni',
}

PARTNER_END = {'script': 'pbDeregisterPartner rescue ($PokemonGlobal.partner = nil)'}


def gauntlet(at, cls, name, ver, sw, intro, after, d='down', sight=4):
    return {
        'type': 'trainer', 'at': list(at), 'sight': sight, 'dir': d,
        'sprite': SPRITE.get(cls, 'trainer_' + cls),
        'trainer': [cls, name, ver], 'intro': intro, 'after': after,
        'cond': {'switch': sw}, 'fixed': True,
    }


def soldier(at, name, sprite, lines, d='down', move='fixed', cond=None):
    e = talk(name, at, sprite, lines, d=d, move=move)
    e['fixed'] = True
    if cond:
        e['pages'][0]['cond'] = cond
    return e


def fx(e):
    """Pin an event strictly to its exact HEAD coordinate so seat_events never drifts it."""
    e['fixed'] = True
    return e


# ================================================================================================
# SHARED TERRAIN & CRAFT ENGINE (Fixes L[0]/L[1] halos, adds 48-shape ground, shadows, glow, smoke)
# ================================================================================================
def desert(W, H, mid, base='u', kit='sdc', seal='wr_sandbags', stairs=None):
    kdict = kit if isinstance(kit, dict) else {1: kit, 2: kit, 3: kit, 'default': kit}
    r = Route(mid, W, H, 'shore', kit=kdict, base=base)
    r.m.SEAL = P1(seal)
    if stairs:
        r.m.STAIRS = tuple(P1(s) for s in stairs)
    return r, r.m


def blob(W, H, cx, cy, rx, ry, seed, rough=0.45):
    yy, xx = np.mgrid[0:H, 0:W]
    q = ((xx - cx) / max(0.5, float(rx))) ** 2 + ((yy - cy) / max(0.5, float(ry))) ** 2
    n = np.array([[vnoise(x, y, seed, 4.0) for x in range(W)] for y in range(H)])
    return q <= 1.0 + rough * (n - 0.5) * 2


def band(W, H, pts, w, seed, wob=0.45):
    out = np.zeros((H, W), bool)
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = int(max(abs(x1 - x0), abs(y1 - y0)) * 3) + 1
        for i in range(n + 1):
            t = i / n
            x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            ww = w * (1 + wob * (vnoise(int(x * 2), int(y * 2), seed, 3.0) - 0.5) * 2)
            for yy in range(int(y - ww - 1), int(y + ww + 2)):
                for xx in range(int(x - ww - 1), int(x + ww + 2)):
                    if 0 <= xx < W and 0 <= yy < H and (xx - x) ** 2 + (yy - y) ** 2 <= ww * ww:
                        out[yy, xx] = True
    return out


def smooth_mask(mask, passes=2):
    m = mask.copy()
    for _ in range(passes):
        pad = np.pad(m, 1, mode='edge')
        n8 = sum(np.roll(np.roll(pad, dy, 0), dx, 1)[1:-1, 1:-1].astype(int)
                 for dy in (-1, 0, 1) for dx in (-1, 0, 1)) - m.astype(int)
        m = (m & (n8 >= 3)) | (~m & (n8 >= 6))
    return m


def trail(r, pts, w=3.0, only='su.tT'):
    m = r.m
    before = r.road_mask.copy()
    r.road(pts, w=w, c='d', open_=None, only=only)
    m.cls[r.road_mask & ~before & (m.cls == 'd')] = 'u'


def ridge(r, x0, x1, y0, y1, seed, h=1, rough=0.38):
    CK.plateau(r, (x0 + x1) / 2.0, (y0 + y1) / 2.0, max(1.5, (x1 - x0) / 2.0), max(1.5, (y1 - y0) / 2.0),
               h, rough=rough, seed=seed)


def dunes(r, n, seed, box=None, w=(4, 9), face='sand', exclude=None):
    """Organic wind-sculpted lee dune crests (one-way jump ledges), avoiding roads, cliffs, events, and water."""
    m = r.m
    rng = random.Random(seed)
    x0, y0, x1, y1 = box or (2, 2, r.W - 2, r.H - 2)
    for _ in range(n * 3):
        if len(getattr(r, 'ledges', [])) >= n + 100:
            break
        x = int(rng.uniform(x0, x1))
        y = int(rng.uniform(y0, y1))
        L = int(rng.uniform(*w))
        xe = min(r.W - 2, x + L)
        if xe - x < 3:
            continue
        ok = True
        for xx in range(x, xe + 1):
            for yy in (y - 1, y, y + 1):
                if not m.inb(xx, yy):
                    ok = False; break
                if m.cls[yy, xx] not in 'su' or r.road_mask[yy, xx] or m.ht[yy, xx] != m.ht[y, x] or m.taken[yy, xx]:
                    ok = False; break
                if exclude is not None and exclude[yy, xx]:
                    ok = False; break
            if not ok:
                break
        if ok:
            CK.ledge(r, x, xe, y, face=face)
            n -= 1
            if n <= 0:
                break


def clean_sand_base(r):
    """Eliminate grass rims AND the L[0] gs_crust/sn_g square-halo bug behind boulders/ledges!
    Sets L[0] uniformly to the pure Dirt sand center tile under all non-water cells and returns sand_base."""
    m = r.m
    V = K.RC.VBASE
    L1 = m.L[1]
    isdirt = np.zeros(L1.shape, bool)
    base = None
    for val in np.unique(L1[L1 >= V]):
        if K.RC.vauto_name(int(val))[1] == 'Dirt':
            isdirt |= (L1 == val)
            if base is None:
                base = int(val) - (int(val) - V) % 48
    if base is None:
        base = K.V('Dirt')
    other = (L1 >= V) & ~isdirt
    same = ~other & ~np.isin(m.cls, ['w', 'W'])
    for y, x in np.argwhere(isdirt):
        m.L[1, y, x] = base + NB2AUTO[CK.nbits(same, x, y)]
    # CRITICAL FIX: replace green grass / random crust on L[0] cleanly with pure sand base everywhere non-water
    nonwater = ~np.isin(m.cls, ['w', 'W'])
    m.L[0, nonwater] = base
    return base


def _is_sand_l1(m, y, x, sand_base):
    v = int(m.L[1, y, x])
    if v == 0:
        return True
    if v >= K.RC.VBASE and (v - sand_base) in range(48):
        return True
    return False


def paint_patch(r, mask, prefix, sand_base, exclude=None, smooth=2):
    """Paint an organic 48-shape wavy ground transition (S_floorpatch / L_floorpatch / E_floorpatch / cs_wet).
    - Interior cells (sh==0): L[0] gets opaque patch center (props stand cleanly on frost/ash/earth with zero halo!),
      and plain sand on L[1] is cleared so L[2] stays 100% open for ripples, decals, shadows & glow.
    - Wavy border cells (sh!=0): open sand on L[1] gets PATCH[sh] over sand_base on L[0] for seamless curved edges!"""
    m = r.m
    pm = mask.astype(bool) & ~m.cliff & ~np.isin(m.cls, ['w', 'W'])
    if exclude is not None:
        pm &= ~exclude
    if smooth:
        pm = smooth_mask(pm, passes=smooth) & ~m.cliff & ~np.isin(m.cls, ['w', 'W'])
        if exclude is not None:
            pm &= ~exclude
    if not pm.any():
        return pm
    P48 = [P1('%s_%02d' % (prefix, i)) for i in range(48)]
    shape = pm | m.cliff
    for y, x in np.argwhere(pm):
        sh = NB2AUTO[CK.nbits(shape, x, y)]
        is_s1 = _is_sand_l1(m, y, x, sand_base)
        if sh == 0:
            m.L[0, y, x] = P48[0]
            if is_s1:
                m.L[1, y, x] = 0
        elif is_s1:
            m.L[0, y, x] = sand_base
            m.L[1, y, x] = P48[sh]
    return pm


def _is_floorpatch_tile(v):
    if not v:
        return False
    if not hasattr(_is_floorpatch_tile, '_set'):
        s = set()
        for pref in ('E_floorpatch', 'S_floorpatch', 'L_floorpatch', 'cs_wet'):
            for i in range(48):
                nm = '%s_%02d' % (pref, i)
                if nm in STAMPS:
                    s.add(P1(nm))
        _is_floorpatch_tile._set = s
    return int(v) in _is_floorpatch_tile._set


def paint_glass(r, mask, sand_base, cracks=0.06, rope=0.09, spill=0.04, seed=0):
    """Fused black-green vitrified glass over sand with wavy 48-shape rims (zero prop halos or event sand-holes)."""
    m = r.m
    rng = random.Random(r.seed * 7 + seed)
    mask = smooth_mask(mask & ~m.cliff, passes=1) & ~m.cliff
    GG = [P1('gd_g%d' % v) for v in range(4)]
    GC = [P1('gd_gc0'), P1('gd_gc1')]
    FL = [P1('gd_floor_%02d' % i) for i in range(48)]
    RP = [P1('gd_rope%d' % v) for v in range(3)]
    SP = [P1('gd_spill%d' % v) for v in range(2)]
    shape = mask | m.cliff
    for y, x in np.argwhere(mask):
        sh = NB2AUTO[CK.nbits(shape, x, y)]
        l1 = int(m.L[1, y, x])
        is_ground_l1 = _is_sand_l1(m, y, x, sand_base) or _is_floorpatch_tile(l1)
        if sh == 0:
            m.L[0, y, x] = rng.choice(GC) if rng.random() < cracks else GG[(x * 3 + y * 5 + int(vnoise(x, y, seed, 2.0) * 4)) % 4]
            if is_ground_l1:
                m.L[1, y, x] = 0
            if not m.L[2, y, x] and not m.taken[y, x] and not m.L[1, y, x]:
                k = rng.random()
                if k < rope * vnoise(x, y, seed + 3, 5.0) * 2:
                    m.L[2, y, x] = rng.choice(RP)
                elif k > 1 - spill:
                    m.L[2, y, x] = rng.choice(SP)
        elif not m.L[2, y, x] and is_ground_l1:
            m.L[1, y, x] = FL[sh]
    return mask


def glass_dress(r, glass, sheen=0.08, sky=0.04, seed=0):
    m = r.m
    rng = random.Random(r.seed * 13 + seed)
    SH = [P1('gd_sheen%d' % v) for v in range(4)]
    SK = [P1('gd_sky%d' % v) for v in range(2)]
    for y, x in np.argwhere(glass):
        if m.L[2, y, x] or m.taken[y, x] or m.cliff[y, x] or m.L[1, y, x]:
            continue
        if not all(glass[yy, xx] for yy in range(max(0, y - 1), min(r.H, y + 2))
                   for xx in range(max(0, x - 1), min(r.W, x + 2))):
            continue
        band_ = vnoise(x + y, 0, r.seed + 31 + seed, 5.0)
        q = rng.random()
        if q < sheen * (0.4 + 1.4 * band_):
            m.L[2, y, x] = SH[(x + y) % 2] if rng.random() < 0.7 else SH[2 + (x % 2)]
        elif q < sheen * 1.8 + sky * vnoise(x, y, r.seed + 37 + seed, 7.0) * 2:
            m.L[2, y, x] = SK[(x // 5 + y // 4) % 2]


def glass_ledges(r, glass):
    m = r.m
    for x0, x1, y in getattr(r, 'ledges', []):
        for x in range(x0, x1 + 1):
            if not m.inb(x, y):
                continue
            near = any(glass[yy, x] for yy in (y - 1, y, y + 1) if 0 <= yy < r.H)
            if near:
                m.L[1, y, x] = P1('gdl_' + ('w' if x == x0 else 'e' if x == x1 else 'm'))


def plan_flood(r, mask):
    m = r.m
    mask = mask & ~r.road_mask & (m.ht == 0)
    for y, x in np.argwhere(mask):
        m.taken[y, x] = True
    return mask


def paint_flood(r, mask, sand_base, steam=0.35, seed=0):
    m = r.m
    rng = random.Random(r.seed * 11 + seed)
    # Damp wet-sand bank (1 tile around flood channels!)
    pad = np.pad(mask, 1, constant_values=False)
    wet = np.zeros_like(mask)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            wet |= pad[1 + dy:1 + dy + r.H, 1 + dx:1 + dx + r.W]
    wet &= ~mask & ~m.cliff & (m.ht == 0)
    paint_patch(r, wet, 'cs_wet', sand_base, exclude=mask, smooth=0)
    FW = [P1('gd_flood_%02d' % i) for i in range(48)]
    ST = [P1('wr_steam%d' % v) for v in range(3)]
    for y, x in np.argwhere(mask):
        m.L[0, y, x] = sand_base
        m.L[1, y, x] = FW[NB2AUTO[CK.nbits(mask, x, y)]]
        m.L[2, y, x] = 0
    for y, x in np.argwhere(mask):
        for dx, dy in ((0, -1), (1, 0), (-1, 0)):
            X, Y = x + dx, y + dy
            if m.inb(X, Y) and not mask[Y, X] and not m.L[2, Y, X] and not m.taken[Y, X] and not m.cliff[Y, X] and rng.random() < steam * 0.32:
                m.L[2, Y, X] = rng.choice(ST)


def plan_ice(r, mask):
    m = r.m
    mask = mask & ~r.road_mask & (m.ht == 0)
    for y, x in np.argwhere(mask):
        m.taken[y, x] = True
    return mask


def paint_ice(r, mask, sand_base, stoppers=(), seed=0):
    m = r.m
    rng = random.Random(r.seed * 17 + seed)
    # Damp icy shore halo around pool
    pad = np.pad(mask, 1, constant_values=False)
    rim = np.zeros_like(mask)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            rim |= pad[1 + dy:1 + dy + r.H, 1 + dx:1 + dx + r.W]
    rim &= ~mask & ~m.cliff & (m.ht == 0)
    paint_patch(r, rim, 'cs_wet', sand_base, exclude=mask, smooth=0)
    IC = [P1('gd_ice_%02d' % i) for i in range(48)]
    FR = [P1('wr_frost%d' % v) for v in range(3)]
    for y, x in np.argwhere(mask):
        m.L[0, y, x] = sand_base
        m.L[1, y, x] = IC[NB2AUTO[CK.nbits(mask, x, y)]]
        m.L[2, y, x] = 0
    for x, y in stoppers:
        m.L[2, y, x] = P1('gd_shard2')
    for y, x in np.argwhere(mask):
        for dx, dy in ((0, -1), (1, 0), (-1, 0), (0, 1)):
            X, Y = x + dx, y + dy
            if m.inb(X, Y) and not mask[Y, X] and not m.L[2, Y, X] and not m.taken[Y, X] and not m.cliff[Y, X] and rng.random() < 0.48:
                m.L[2, Y, X] = rng.choice(FR)


def ice_puzzle(r, mask, goal, seed=7, tries=4000):
    m = r.m
    rng = random.Random(seed)
    cells = {(int(x), int(y)) for y, x in np.argwhere(mask)}
    land = set()
    for (x, y) in cells:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + dx, y + dy)
            if n not in cells and m.inb(*n) and m.cls[n[1], n[0]] in 'su' and not m.cliff[n[1], n[0]] and (not m.taken[n[1], n[0]] or n == goal):
                land.add(n)
    start = land - {goal}
    inner = sorted(cells)
    best = None
    for _ in range(tries):
        rocks = set(rng.sample(inner, min(max(3, len(inner) // 6), rng.randint(4, 9))))
        ice = cells - rocks
        k, _p = RW.slide_solve(ice, land, start, {goal})
        if k is None or k < 3:
            continue
        back, _q = RW.slide_solve(ice, land, {goal}, start)
        if back is None:
            continue
        sc = k * 10 - len(rocks)
        if best is None or sc > best[0]:
            best = (sc, rocks, k)
        if k >= 5:
            break
    if best is None:
        raise RuntimeError('ice_puzzle: failed to find solvable layout for goal %r' % (goal,))
    print('  ice puzzle: %d stoppers, %d slides' % (len(best[1]), best[2]))
    return best[1]


def sand_dress(r, ripple=0.40, seed=0, exclude=None, bones=0.015):
    """Wind ripples across open sand (not glass/water/ice), wheel ruts along roads."""
    m = r.m
    rng = random.Random(r.seed * 3 + seed)
    R = [P1('wr_ripple%d' % v) for v in range(3)]
    Bn = [P1('wr_bones%d' % v) for v in range(2)]
    RU = [P1('wr_rut%d' % v) for v in range(2)]
    for y, x in np.argwhere(r.road_mask):
        if exclude is not None and exclude[y, x]:
            continue
        if m.cls[y, x] in 'su' and not m.L[2, y, x] and not m.taken[y, x] and not m.cliff[y, x] and rng.random() < 0.72:
            m.L[2, y, x] = RU[(x + y) % 2]
    for y, x in np.argwhere(np.isin(m.cls, ['s', 'u'])):
        if exclude is not None and exclude[y, x]:
            continue
        if m.L[2, y, x] or m.cliff[y, x] or r.road_mask[y, x] or m.taken[y, x]:
            continue
        n = vnoise(x, y, r.seed * 11 + seed, 4.0)
        if n > 1 - ripple - 0.14 and rng.random() < 0.82:
            m.L[2, y, x] = R[(x // 3 + y) % 3]
        elif rng.random() < bones:
            m.L[2, y, x] = rng.choice(Bn)


def decal(r, names, p, seed=0, cells=None, exclude=None):
    m = r.m
    rng = random.Random(r.seed * 5 + seed)
    T = [P1(n) for n in names]
    src = cells if cells is not None else [tuple(c[::-1]) for c in np.argwhere(np.isin(m.cls, ['s', 'u']))]
    for x, y in src:
        if not m.inb(x, y):
            continue
        if exclude is not None and exclude[y, x]:
            continue
        if not m.L[2, y, x] and not m.cliff[y, x] and not m.taken[y, x] and m.cls[y, x] in 'su' and rng.random() < p:
            m.L[2, y, x] = rng.choice(T)


def paint_cliff_shadows(r, shadow_name='E_shadow', exclude=None):
    """Soft ambient-occlusion cliff-foot shadow on open walkable cells immediately south of cliff bases."""
    m = r.m
    sh_id = P1(shadow_name)
    for y in range(r.H - 1):
        for x in range(r.W):
            if m.cliff[y, x] and not m.cliff[y + 1, x]:
                if exclude is not None and exclude[y + 1, x]:
                    continue
                if m.cls[y + 1, x] in 'su' and not m.taken[y + 1, x] and m.L[2, y + 1, x] == 0:
                    m.L[2, y + 1, x] = sh_id


def place_glow(m, cx, cy):
    """Warm 2x2 pri=5 firelight bloom centered over a brazier/beacon/campfire (never overwrites existing L2)."""
    L = STAMPS['pf_glow']['layers'][2]
    for dy in range(2):
        for dx in range(2):
            x, y = cx + dx, cy + dy
            if m.inb(x, y) and m.L[2, y, x] == 0 and L[dy][dx]:
                m.L[2, y, x] = int(L[dy][dx])


def place_smoke(m, x, y, kind='fw_smoke_w'):
    """Curling 1x2 pri=2 smoke plume (never overwrites existing L2)."""
    L = STAMPS[kind]['layers'][2]
    for dy in range(2):
        yy = y + dy
        if m.inb(x, yy) and m.L[2, yy, x] == 0 and L[dy][0]:
            m.L[2, yy, x] = int(L[dy][0])


def place_shaft(m, x, y):
    """Atmospheric 2x3 pri=2 overhead light shaft (never overwrites existing L2)."""
    L = STAMPS['cv_shaft']['layers'][2]
    for dy in range(3):
        for dx in range(2):
            xx, yy = x + dx, y + dy
            if m.inb(xx, yy) and m.L[2, yy, xx] == 0 and L[dy][dx]:
                m.L[2, yy, xx] = int(L[dy][dx])


def add_fire_lighting(m, smoke_for=('pf_beacon', 'sh_campfire')):
    """Automatically add warm radial pf_glow + rising smoke above all placed braziers, beacons & campfires."""
    for nm, sx, sy in list(m.stamps):
        if nm == 'fw_brazier':
            place_glow(m, sx - 1, sy)
            place_glow(m, sx, sy)
        elif nm == 'pf_beacon':
            place_glow(m, sx, sy)
            place_smoke(m, sx, sy - 2, 'fw_smoke_a')
        elif nm == 'sh_campfire':
            place_glow(m, sx + 1, sy)
            place_smoke(m, sx + 2, sy - 2, 'fw_smoke_w')
        elif nm == 'wr_firering':
            place_glow(m, sx, sy - 1)
            place_smoke(m, sx, sy - 2, 'fw_smoke_w')


def frame_border_crags(r, sides='NSWE', kinds=('sk_rock_big', 'sk_boulder', 'ak_rock2'), seed=101):
    """Organic boulder/crag framing along non-exit edges so map borders look geological, not 1-tile SEAL fences."""
    m = r.m
    rng = random.Random(r.seed + seed)
    exits = r.exits
    ev_pad = np.zeros((r.H, r.W), bool)
    for e in r.events:
        ex, ey = e['at']
        ev_pad[max(0, ey - 2):ey + 3, max(0, ex - 2):ex + 3] = True
    for side, off, w in exits:
        for k in range(-2, w + 2):
            if side in 'NS':
                xx = off + k
                if 0 <= xx < r.W:
                    y0 = 0 if side == 'N' else r.H - 4
                    ev_pad[y0:y0 + 4, xx] = True
            else:
                yy = off + k
                if 0 <= yy < r.H:
                    x0 = 0 if side == 'W' else r.W - 4
                    ev_pad[yy, x0:x0 + 4] = True

    def try_place(nm, x, y):
        st = STAMPS[nm]
        w, h = st['w'], st['h']
        if x < 0 or y < 0 or x + w > r.W or y + h > r.H:
            return False
        if ev_pad[y:y + h, x:x + w].any() or r.road_mask[y:y + h, x:x + w].any():
            return False
        if m.cliff[y:y + h, x:x + w].any() or m.taken[y:y + h, x:x + w].any():
            return False
        if not np.all(np.isin(m.cls[y:y + h, x:x + w], ['s', 'u'])):
            return False
        m.stamp(nm, x, y, mark='B')
        return True

    if 'N' in sides:
        for x in range(0, r.W - 1, 2):
            nm = rng.choice(kinds)
            try_place(nm, x, 0)
    if 'S' in sides:
        for x in range(0, r.W - 1, 2):
            nm = rng.choice(kinds)
            st = STAMPS[nm]
            try_place(nm, x, r.H - st['h'])
    if 'W' in sides:
        for y in range(0, r.H - 1, 2):
            nm = rng.choice(kinds)
            try_place(nm, 0, y)
    if 'E' in sides:
        for y in range(0, r.H - 1, 2):
            nm = rng.choice(kinds)
            st = STAMPS[nm]
            try_place(nm, r.W - st['w'], y)


def seal_non_exit_edge(r, side, palette=('wr_sandbags', 'wr_pal_v', 'wr_stakes'), keep_pts=()):
    """Ensure every non-exit border tile on `side` is organically blocked with varied natural tiles (zero uniform fence)."""
    m = r.m
    rng = random.Random(r.seed * 29 + ord(side))
    keep = set(keep_pts)
    exits = r.exits

    def is_open(i):
        return any(s == side and o <= i < o + w for s, o, w in exits)

    coords = ([(x, 0, x) for x in range(r.W)] if side == 'N' else
              [(x, r.H - 1, x) for x in range(r.W)] if side == 'S' else
              [(0, y, y) for y in range(r.H)] if side == 'W' else
              [(r.W - 1, y, y) for y in range(r.H)])
    for x, y, i in coords:
        if is_open(i) or (x, y) in keep or m.taken[y, x] or m.cliff[y, x] or m.cls[y, x] not in 'su':
            continue
        nm = palette[(i + rng.randrange(len(palette))) % len(palette)]
        m.stamp(nm, x, y, mark='B')


# ================================================================================================
# 1. MAP 920 — THE RIMED SANDS (60x36, ts 56, DESERT / Snow)
# ================================================================================================
def build_920():
    W, H = 60, 36
    r, m = desert(W, H, 920, kit='sdc', seal='wr_sandbags',
                  stairs=('fw_stair_l', 'fw_stair_m', 'fw_stair_r'))

    # 1. Sculpted North Watch-Scarp (organic undulating rim x=19..58, y=0..6)
    for x in range(19, 59):
        top = 4 + int(round(1.9 * (vnoise(x, 0, 9202, 5.5) - 0.5) * 2))
        if 37 <= x <= 42:
            top = 4   # clean flat landing for the watch-post stair & Signal horn (40,2)
        m.ht[:max(2, top) + 1, x] = 1
    CK.smooth_ht(m, 1, 2, box=(18, 0, 60, 9))
    # Guarantee Watch-post sergeant (44,2) and Signal horn (40,2) sit comfortably on ht=1
    m.ht[0:5, 38:46] = 1

    # Sculpted SW & S-Central dune bluff ridges framing the southern frost-dunes & item coves
    ridge(r, 11, 17, 29, 34, seed=92011, h=1, rough=0.35)
    ridge(r, 50, 58, 28, 34, seed=92012, h=1, rough=0.35)

    # 2. Primary military roads (packed earth supply corridor W->E + south Glass Dunes approach)
    road = [(0, 14.5), (12, 15), (24, 14), (36, 15.5), (48, 14.5), (59, 15)]
    trail(r, road, w=3.2)
    trail(r, [(10, 16), (8, 24), (8, 35)], w=3.0)
    trail(r, [(28, 16), (26, 23), (26, 28)], w=2.0, only='su.')
    trail(r, [(12, 14), (11, 8)], w=2.2, only='su.')
    r.exit('W', 13, 4)
    r.exit('E', 13, 4)

    # Keep south/north ridges well clear of roads and events
    for rx0, rx1, ry0, ry1 in ((10, 18, 27, 36), (48, 59, 26, 36)):
        for y in range(ry0, min(H, ry1)):
            for x in range(rx0, min(W, rx1)):
                if r.road_mask[max(0, y - 1):y + 4, max(0, x - 1):x + 2].any():
                    m.ht[y, x] = 0
        CK.smooth_ht(m, 1, 2, box=(rx0, ry0, min(W, rx1 + 1), min(H, ry1)))

    # 3. Two organic frozen sea-meltwater pools beneath the north scarp
    pools = (blob(W, H, 25.5, 9.0, 4.6, 2.4, 92021, 0.34) |
             blob(W, H, 51.5, 9.2, 4.9, 2.5, 92022, 0.34)) & (m.ht == 0)
    for y in range(H):
        for x in (18, 32, 46):
            pools[y, x - 1:x + 2] = False
        # Keep cliff face below north scarp clear of ice
        for x in range(18, 59):
            if m.ht[max(0, y - 3):y + 1, x].any():
                pools[y, x] = False
    # Ensure east pool nicely wraps ISLET = [(51, 9), (52, 9)] so gate stays strictly sealed on foot!
    for y in range(7, 12):
        for x in range(48, 56):
            if (x - 51.5) ** 2 / 14.0 + (y - 9.0) ** 2 / 5.5 <= 1.0 and m.ht[y, x] == 0:
                pools[y, x] = True
    ISLET = [(51, 9), (52, 9)]
    for x, y in ISLET:
        pools[y, x] = False
    ice = plan_ice(r, pools)
    for x, y in ISLET:
        m.taken[y, x] = True
    GOAL920 = ISLET[1]

    # Organic sand lee dune ledges (avoiding trenches, roads, pools, events)
    ev_excl = ice.copy()
    for tx in (18, 32, 46):
        ev_excl[:, max(0, tx - 2):min(W, tx + 3)] = True
    dunes(r, 7, 920, box=(2, 20, 56, 32), w=(4, 8), exclude=ev_excl)
    dunes(r, 2, 921, box=(2, 2, 16, 8), w=(4, 7), exclude=ev_excl)

    r.finish_plan(border=1)

    # 4. ALL 18 HEAD Events pinned to exact HEAD IDs & coordinates!
    E = [
        make_front(),
        {'type': 'warp', 'name': 'To the Glass Dunes', 'at': [8, 35], 'link': 'WAR_RIMED_DUNES', 'arrive': [8, 34, 'up'], 'fixed': True},
        gauntlet((19, 14), 'ISENMAR_SOLDIER_M', 'Soldier', 0, 'WAR_SIDE_ASH',
                 'You came with the dragons. You leave without them.', 'The line holds behind me. You will see.', d='left'),
        gauntlet((33, 15), 'ISENMAR_SOLDIER_F', 'Soldier', 0, 'WAR_SIDE_ASH',
                 "The Thane said the sand would never be cold. Ask the sand.", 'Go, then. Tell them the Rimed Sands were held.', d='left'),
        gauntlet((47, 14), 'ISENMAR_OFFICER', 'Captain', 0, 'WAR_SIDE_ASH',
                 'Third line. Nobody has passed the third line.', 'Somebody has passed the third line. Mark it in the tally.', d='left'),
        fx(item(ISLET[0], 'NEVERMELTICE')),
        fx(sign((3, 12), 'Road sign', "THE RIMED SANDS. W: Skaldfast (under siege: the road is barricaded). E: the Steamline. S: the Glass Dunes.")),
        fx(obj('Siege barricade', (1, 17), ['Sledges on their sides, lashed with whale-gut, piled with frozen sand. Skaldfast is two miles west, and burning.'])),
        fx(obj('Sled-yard', (12, 6), ['Sled-forts dragged over the Mast Glacier, two hundred miles, on bone runners. Most are burnt black on the eastern side.'])),
        soldier((15, 13), 'Isenmar picket', 'NPC 11', [
            "Isenmar picket: The sand was hot when we got here. We fixed that.",
            "Picket: Our Glaceon froze it a yard deep. You can feel the cold through your boots. That's the line."], d='right'),
        soldier((28, 17), 'Skald', 'NPC 28', ["Skald: I'm here to remember it. Somebody has to, and it may as well be someone who rhymes."]),
        soldier((44, 12), 'Ice-rider', 'NPC 25', ["Ice-rider: My Mamoswine walked over the glacier. It will walk back. I promised it."]),
        fx(obj('Frozen trench', (20, 19), ['A trench cut in sand and frozen hard, its walls glazed white. Someone has carved a tally of days into the ice. It is a long tally.'])),
        fx(hidden((26, 30), 'STARDUST', 'HiddenItem (rimed dune)')),
        fx(obj('Frozen sea', (25, 11), ['The sea came over the dunes this far. The Glaceon lines froze it where it stood: a pool of green ice with the sand still in it.'])),
        soldier((44, 2), 'Watch-post sergeant', 'NPC 28', [
            "Watch-post sergeant: Up here you can see Skaldfast burning and the Steamline smoking. Pick which to look at.",
            "Sergeant: The ice on the flats? Slide it. The children of Skaldfast could, before."], d='down'),
        fx(obj('Signal horn', (40, 2), ['A great horn of whale-bone on a frame. Blown once for the dragons, twice for the sea. Nobody has blown it twice yet.'])),
        fx(item((5, 28), 'FULLRESTORE')),
    ]
    r.add(*E)
    r.seat_events(on='su')

    # Watch-post stair up the north sandstone scarp
    yl = max(y for y in range(10) if m.ht[y, 39] == 1)
    CK.stair(r, 38, yl, w=3, h=1)

    # 5. Fortified Isenmar Trench-Lines (x=18, 32, 46): layered sandbags, frosted palisades, sled-fort bastions & stakes!
    #    ZERO ugly blue dotted nr_wall_v stripes!
    ports = {18: 14, 32: 15, 46: 14}
    rev_cells = []
    for x, py in ports.items():
        # Heavy sled-fort bastions immediately flanking each sally port
        for fy in (py - 4, py + 3):
            if m.inb(x - 1, fy) and m.free(x - 1, fy, 3, 2, on='su'):
                m.stamp('wr_sledfort' if (x + fy) % 2 == 0 else 'wr_sledfort2', x - 1, fy, mark='B')
        # Parapet revetment line (alternating sandbags + frosted timber palisades)
        for y in range(1, H - 1):
            if abs(y - py) <= 1 or m.ht[y, x] != 0 or m.cliff[y, x] or m.cls[y, x] not in 'su':
                continue
            if m.taken[y, x]:
                rev_cells.append((x, y))
                continue
            # Leave clean visual breathing notches backed by stakes, never unguarded gaps
            piece = 'wr_sandbags' if (y % 3 != 0) else 'fw_pal_v'
            m.stamp(piece, x, y, mark='B')
            rev_cells.append((x, y))
            # Forward glacis cheveaux-de-frise stakes on east face
            if (y % 4 == 1) and m.inb(x + 2, y) and not m.taken[y, x + 2] and not m.cliff[y, x + 2] and not r.road_mask[y, x + 2] and m.cls[y, x + 2] in 'su' and m.ht[y, x + 2] == 0:
                m.stamp('wr_stakes', x + 2, y, mark='B')

    # 6. Storytelling Camp Clusters, Sled-Yard, Watch-Post & Ice Pool Framing
    hero_props = [
        # Skaldfast western siege barricade cluster (dramatic heavy defense!)
        ('pf_barricade', 0, 17), ('wr_sledfort', 1, 18), ('wr_sandbags', 0, 12), ('wr_supply', 5, 16),
        ('fw_brazier', 3, 17), ('wr_ban_ise', 2, 11),
        # NW Sled-Yard (Isenmar dragged glacier forts, blue/white tents, firewood & hearth)
        ('wr_sledfort2', 5, 2), ('wr_tent_b', 9, 2), ('wr_tent_w', 14, 3),
        ('wr_tent_b', 5, 7), ('wr_tent_w', 13, 8), ('wr_firering', 10, 7),
        ('fw_rack', 3, 5), ('fw_sled', 8, 10), ('fw_wood', 11, 10), ('wr_sacks', 8, 12),
        ('pf_whalebone', 15, 2), ('fw_brazier', 15, 10),
        # Sally Port 1, 2, 3 Command Vignettes (banners + glowing watch-braziers + supply crates)
        ('wr_ban_ise', 17, 10), ('fw_brazier', 20, 12), ('wr_rack', 16, 8),
        ('wr_ban_ise', 31, 11), ('fw_brazier', 34, 12), ('wr_supply', 26, 13), ('wr_sacks', 29, 12), ('wr_tent_b', 22, 11),
        ('wr_ban_ise', 45, 10), ('fw_brazier', 48, 12), ('wr_ban_ise_t', 48, 17), ('wr_glasssled', 52, 22),
        # North Watch-Scarp Lookout Post (Sergeant + Whalebone Signal Horn + Banners + Braziers!)
        ('wr_sledfort2', 21, 1), ('wr_ban_ise', 26, 1), ('fw_brazier', 29, 1), ('wr_tent_b', 31, 0),
        ('fw_brazier', 36, 1), ('pf_whalebone', 41, 1), ('wr_ban_ise', 46, 1),
        ('wr_sledfort', 49, 1), ('fw_rack', 53, 1), ('wr_tent_w', 55, 0), ('wr_sacks', 43, 3),
        # Frozen Meltwater Pools Framing (crystalline ice spires, reeds, ice-locked whaleboat & sleds!)
        ('cr_blue_t', 20, 8), ('cr_clear_t', 21, 10), ('cr_blue_c', 29, 7), ('cr_clear_c', 30, 10),
        ('fw_boat', 22, 10), ('fw_reeds0', 21, 7), ('fw_reeds1', 28, 10),
        ('cr_blue_t', 47, 9), ('cr_clear_t', 56, 8), ('cr_blue_e', 55, 10), ('fw_sled', 53, 12),
        ('fw_reeds0', 48, 11), ('fw_reeds1', 55, 7), ('wr_tent_w', 49, 4), ('wr_sledfort', 36, 6),
        # South Rimed Dunes Storytelling (sleds, boulders, frost crags, camp lanterns, glass shards east)
        ('fw_sled', 24, 19), ('fw_brazier', 22, 18), ('pf_lantern', 10, 22), ('pf_lantern', 10, 31),
        ('pf_barricade', 4, 24), ('sk_rock_big', 2, 29), ('ak_rock2', 35, 28), ('wr_firering', 38, 22),
        ('wr_tent_b', 36, 19), ('wr_rack', 40, 20), ('gd_shard0', 55, 19), ('gd_shard1', 56, 24), ('gd_shard2', 53, 25),
    ]
    for nm, x, y in hero_props:
        r.near(nm, x, y, on='su', r=2)

    CK.props(r, ['sk_rock_big', 'sk_boulder', 'sk_pebbles', 'nt_deadtree'], 18, box=(1, 18, W - 1, H - 1), on='su', clump=2, seed=5)
    CK.props(r, ['sk_boulder', 'sk_pebbles'], 8, box=(1, 1, 20, 12), on='su', clump=2, seed=6)

    # Organic boulder/palisade border framing on E edge (leaving E y=13..16 strictly open!)
    frame_border_crags(r, sides='NSE', kinds=('sk_rock_big', 'sk_boulder'), seed=9201)
    seal_non_exit_edge(r, 'E', palette=('wr_sandbags', 'fw_pal_v', 'wr_stakes'))

    r.dress(trees=('nt_deadtree',), n_trees=0, copses=0, scatter=0)
    m.cls[m.cls == 'd'] = 'u'
    r.paint()

    # 7. Clean Sand Base + Multi-Layer 48-Shape Frost Blanket, Packed Roads & Frozen Pools!
    sand_base = clean_sand_base(r)
    stop = ice_puzzle(r, ice & (np.arange(W)[None, :] > 46), GOAL920, seed=9203)

    # Sweeping Isenmar frost blanket across the west 3/4 of the map (S_floorpatch 48-shape wavy edges!)
    frost_mask = np.zeros((H, W), bool)
    for y in range(H):
        east_edge = 45.5 + 3.2 * (vnoise(0, y, 9201, 4.5) - 0.5) * 2
        for x in range(W):
            if x < east_edge and vnoise(x, y, 9204, 6.0) > 0.34:
                frost_mask[y, x] = True
            # Guaranteed frost pools around the sled-yard, north watch-scarp & frozen sea basins
            if x < 17 and y < 12:
                frost_mask[y, x] = True
    frost_mask &= ~ice & ~r.road_mask
    paint_patch(r, frost_mask, 'S_floorpatch', sand_base, exclude=ice, smooth=2)

    # Packed-earth military supply road & trench bottoms (E_floorpatch 48-shape!)
    trench_mask = np.zeros((H, W), bool)
    for x, y in rev_cells:
        for dx in (-2, -1):
            if m.inb(x + dx, y) and not m.cliff[y, x + dx] and not ice[y, x + dx]:
                trench_mask[y, x + dx] = True
    road_earth = (r.road_mask | trench_mask) & ~ice
    paint_patch(r, road_earth, 'E_floorpatch', sand_base, exclude=ice, smooth=1)

    # Frozen meltwater pools with damp shore rims & ice-puzzle stoppers
    paint_ice(r, ice, sand_base, stop, seed=920)

    # Soft cliff-foot shadows beneath north watch-scarp & south dune ridges
    paint_cliff_shadows(r, 'E_shadow', exclude=ice)

    # Wind ripples, wheel ruts, frost crystals, snowdrifts, trench cuts & embers
    sand_dress(r, 0.44, seed=920, exclude=ice, bones=0.025)
    decal(r, ['wr_frost0', 'wr_frost1', 'wr_frost2'], 0.28, seed=1,
          cells=[(x, y) for y in range(H) for x in range(0, 48) if not ice[y, x]], exclude=ice)
    decal(r, ['fw_drift0', 'fw_drift1', 'fw_drift2'], 0.10, seed=11,
          cells=[(x, y) for y in range(H) for x in range(0, 45) if frost_mask[y, x]], exclude=ice)
    decal(r, ['wr_trench0', 'wr_trench1'], 0.85, seed=2,
          cells=[(x - 1, y) for x, y in rev_cells] + [(x - 2, y) for x, y in rev_cells if y % 2], exclude=ice)
    decal(r, ['wr_ember0', 'wr_ember1'], 0.08, seed=3,
          cells=[(x, y) for y in range(H) for x in range(44, W)], exclude=ice)

    # Warm firelight glow + atmospheric light shaft on Watch-Post & Frozen Sea
    add_fire_lighting(m)
    place_shaft(m, 39, 1)
    place_shaft(m, 24, 7)

    CK.scatter_quiet(r, 12)
    h = head(920, 'The Rimed Sands', field='DESERT', bgm='Route 9', biome='desert', weather=['Snow', 10],
             connections=[{'dir': 'E', 'offset': 13, 'to': 925, 'to_offset': 13}],
             tone=[10, 6, 14, 10], fog={'name': 'prismfall_seamist', 'opacity': 24, 'blend': 0, 'zoom': 200, 'sx': 1, 'sy': 0})
    h['metadata']['MapPosition'] = [0, 12, 14]
    h['walk_from'] = [list(GOAL920)]
    h['gates'] = [{'name': 'The ice islet (sliding only)', 'from': [[1, 14], [58, 14], [8, 34]], 'sealed': [list(GOAL920)], 'ice_solid': True}]
    r.write(h, '920_rimed_sands.yaml', '# The Rimed Sands (920). WRITTEN BY layouts/war_craft.py (Wave 9) - edit that script.\n')


# ================================================================================================
# 2. MAP 924 — ASHKAAR SIEGE CAMP (56x40, ts 56, ASHEN_WASTE)
# ================================================================================================
def build_924():
    W, H = 56, 40
    # Use vitrified obsidian-glass cliff kit ('gdc') for Ashkaar's fired earthworks & volcanic perimeter ridges!
    r, m = desert(W, H, 924, kit='gdc', seal='wr_pal_v',
                  stairs=('L_stairl', 'L_stairm', 'L_stairr'))

    # 1. Tactical camp avenues FIRST (so earthwork bastions & dunes never block them)
    trail(r, [(0, 19.5), (12, 19.5), (24, 20), (36, 19), (48, 20), (55, 19.5)], w=3.2)
    trail(r, [(20, 21), (14, 30), (8, 39)], w=3.0)
    trail(r, [(24, 10), (44, 10)], w=2.2, only='su.')
    trail(r, [(24, 28), (50, 28)], w=2.2, only='su.')
    trail(r, [(36, 20), (36, 13)], w=3.2, only='su.')
    r.exit('W', 18, 4)
    r.exit('E', 18, 4)

    # 2. Layered Obsidian-Glass Earthwork Bastions & Volcanic Perimeter Ridges (replaces flat blue stripes!)
    # Outer & inner fortified bastion mounds (raised ht=1 gdc obsidian earthworks flanking the two siege gates!)
    ridge(r, 1, 7, 1, 6, seed=92401, h=1, rough=0.35)      # NW volcanic bastion overlooking west approach
    ridge(r, 48, 54, 1, 6, seed=92402, h=1, rough=0.35)    # NE dragon-roost basalt crag
    ridge(r, 15, 22, 1, 5, seed=92403, h=1, rough=0.35)    # North central redoubt ridge
    ridge(r, 38, 46, 1, 5, seed=92404, h=1, rough=0.35)    # North war-tent backdrop ridge
    ridge(r, 14, 23, 35, 39, seed=92405, h=1, rough=0.35)  # South earthwork bluff
    # Keep roads, events, and war-tent footprint completely clear of cliffs
    for y in range(H):
        for x in range(W):
            if r.road_mask[max(0, y - 1):y + 4, max(0, x - 1):x + 2].any():
                m.ht[y, x] = 0
            if 32 <= x <= 41 and 6 <= y <= 16:
                m.ht[y, x] = 0
            if 27 <= x <= 33 and 3 <= y <= 7:
                m.ht[y, x] = 0
            if 44 <= x <= 53 and 10 <= y <= 16:
                m.ht[y, x] = 0
    CK.smooth_ht(m, 1, 2)

    # Organic wind-carved dune ledges on open edges
    ev_excl = np.zeros((H, W), bool)
    for tx in (10, 20):
        ev_excl[:, max(0, tx - 2):min(W, tx + 3)] = True
    dunes(r, 3, 924, box=(24, 3, 52, 7), w=(4, 7), exclude=ev_excl)
    dunes(r, 3, 9241, box=(26, 33, 52, 37), w=(4, 7), exclude=ev_excl)

    r.finish_plan(border=1)

    # 3. Stamp Dominar's War-Tent FIRST (door WAR_TENT lands at exact HEAD [36, 13]!)
    m.stamp('wr_wartent', 34, 9, 'WAR_TENT', 'War-tent door')

    # 4. ALL 20 HEAD Events pinned at exact HEAD IDs (1..20) & coordinates!
    tent_doors = []
    for e in m.events:
        if e.get('link') == 'WAR_TENT':
            e['at'] = [36, 13]
            tent_doors.append(fx(e))
    m.events = []
    E = [
        {'type': 'warp', 'name': 'To the Glass Dunes', 'at': [8, 39], 'link': 'WAR_CAMP_DUNES', 'arrive': [8, 38, 'up'], 'fixed': True},
        gauntlet((11, 19), 'ASHKAAR_SOLDIER_M', 'Soldier', 0, 'WAR_SIDE_ISE',
                 'Isenmar sends children now? Then I fight children.', "...Not children. Go on, then. The next gate won't be so polite.", d='left'),
        gauntlet((21, 20), 'ASHKAAR_SOLDIER_F', 'Soldier', 0, 'WAR_SIDE_ISE',
                 'Second gate. The fire behind it is real.', 'The fire behind it is real. So is that.', d='left'),
        gauntlet((35, 16), 'ASHKAAR_OFFICER', 'Captain', 0, 'WAR_SIDE_ISE',
                 "You want the Dominar's tent? Through me. That is how it works here.", "That is how it works here. Pass.", d='down'),
    ] + tent_doors + [
        make_front(),
        fx(sign((4, 17), 'Camp sign', "ASHKAAR SIEGE CAMP - by the Dominar's leave and the Elector's Lease. Lies are a capital crime in this camp.")),
        fx(obj('Earthwork', (9, 14), ['A rampart of sand and black glass, packed hard and baked: the legion engineers fire it with Torkoal until it rings.'])),
        fx(obj('Forge', (44, 25), ['A field forge, roaring. Spearheads for the legion, shoes for the Rapidash, and a dragon\'s neck-plate the size of a door.'])),
        fx(obj('Mess fire', (28, 25), ['The mess fire. Somebody is stirring a pot of red lentils as big as a bath and singing a marching song badly.'])),
        soldier((26, 16), 'Legionary', 'NPC 21', ["Legionary: The steam's a wall. The wall's a Bleed. The Bleed's Isenmar's fault. That's the briefing."], d='down'),
        soldier((40, 22), 'Dragon handler', 'NPC 20', ["Dragon handler: Don't look them in the eye. Don't look them in the tail either. Just walk."], d='left'),
        soldier((47, 31), 'Quartermaster', 'NPC 25', ["Quartermaster: Fire we have. Water we buy. From Ossaria. At Ossarian prices."], d='up'),
        soldier((15, 26), 'Scout', 'NPC 22', ["Scout: The bone-carters walk straight across. Nobody shoots a bone-carter. Not twice."], d='right'),
        fx(talk('Dragonite', (46, 12), 'Followers/DRAGONITE', ['(It is chained to the picket. It looks at the chain, then at you, then sighs.)'], move='random')),
        fx(talk('Charizard', (50, 14), 'Followers/CHARIZARD', ['(A war-mount, scarred. It warms the sand where it lies.)'])),
        fx(obj('Barricade (war road)', (53, 22), ['The war road east to Glasswake, barricaded and guarded. Supplies come in; nobody goes out.'])),
        fx(item((52, 36), 'CHARCOAL')),
        fx(hidden((30, 5), 'STARDUST', 'HiddenItem (dune)')),
        fx(item((3, 36), 'HYPERPOTION')),
    ]
    r.add(*E)
    r.seat_events(on='su')

    # 5. Two Fortified Volcanic Earthwork Ramparts (x=10 & x=20): charred siege palisades + sandbags + stakes + banners + fire beacons!
    gates = {10: 19, 20: 20}
    works = []
    for x, gy in gates.items():
        # Gatehouse banners & flaming braziers flanking each sally gate
        r.near('wr_ban_ash', x - 1, gy - 3, on='su', r=1)
        r.near('wr_ban_ash', x - 1, gy + 2, on='su', r=1)
        r.near('fw_brazier', x + 1, gy - 3, on='su', r=2)
        r.near('fw_brazier', x + 1, gy + 2, on='su', r=2)
        for y in range(2, H - 2):
            if abs(y - gy) <= 1 or m.cls[y, x] not in 'su' or m.cliff[y, x] or m.ht[y, x] > 0:
                continue
            if x == 20 and 27 <= y <= 33:
                continue  # south Glass Dunes road cut
            if m.taken[y, x]:
                continue
            piece = 'wr_pal_v' if (y % 3 != 0) else 'wr_sandbags'
            m.stamp(piece, x, y, mark='B')
            works.append((x, y))
            # Forward charred stakes on the west assault face
            if y % 4 == 2 and m.inb(x - 2, y) and not m.taken[y, x - 2] and not m.cliff[y, x - 2] and not r.road_mask[y, x - 2] and m.cls[y, x - 2] in 'su' and m.ht[y, x - 2] == 0:
                m.stamp('wr_stakes', x - 2, y, mark='B')

    # 6. Command Plaza, Artillery Batteries, Regimental Tent Compounds, Dragon Pickets & Field Forge
    camp_props = [
        # Dominar's War-Tent Command Plaza (grand ceremonial framing around wr_wartent!)
        ('wr_ban_ash', 32, 10), ('wr_ban_ash', 40, 10),
        ('fw_brazier', 32, 15), ('fw_brazier', 40, 15),
        ('fw_brazier', 33, 17), ('fw_brazier', 39, 17),
        ('wr_rack', 32, 13), ('wr_rack', 40, 13),
        # Siege Trebuchet Artillery Batteries + boulder ammo piles!
        ('wr_trebuchet', 13, 6), ('sk_boulder', 16, 8), ('wr_sacks', 16, 7),
        ('wr_trebuchet', 13, 29), ('sk_boulder', 16, 31), ('wr_sandbags', 12, 32),
        ('wr_trebuchet', 22, 6), ('wr_rack', 25, 8),
        # Regimental Tent Compounds (asymmetric, organic clusters instead of sterile uniform grid!)
        ('wr_tent_r', 25, 11), ('wr_tent_w', 29, 11), ('wr_tent_r', 24, 5),
        ('wr_tent_r', 46, 6), ('wr_tent_w', 42, 6),
        ('wr_tent_w', 24, 22), ('wr_tent_r', 31, 22), ('wr_tent_r', 37, 22),
        ('wr_tent_r', 24, 30), ('wr_tent_w', 33, 30), ('wr_tent_r', 39, 31),
        ('wr_tent_r', 49, 23), ('wr_tent_r', 49, 31),
        # Dragon Pickets (East-North vitrified crater with chains & volcanic crags)
        ('wr_picket', 45, 13), ('wr_picket', 49, 15), ('wr_picket', 52, 11),
        ('gd_spire', 52, 8), ('gd_shard0', 44, 14), ('gd_shard1', 53, 15),
        # Field Forge (roaring twin war-braziers, anvil crates, barrels, weapon racks & glass hearth!)
        ('fw_brazier', 43, 23), ('fw_brazier', 46, 24), ('hb_crates4', 44, 27),
        ('hb_barrels', 48, 26), ('wr_rack', 42, 26), ('wr_supply', 50, 21),
        # Legion Mess Fire Courtyard (cozy campfire + log benches + tubs + supply wagon)
        ('sh_campfire', 27, 25), ('pf_logbench', 28, 23), ('hb_tubs', 29, 32),
        ('wr_firering', 35, 29), ('wr_sacks', 31, 29), ('wr_supply', 38, 34), ('sh_crates', 43, 33),
        ('wr_sacks', 48, 29), ('wr_rack', 27, 21), ('wr_rack', 42, 17),
        # East Glasswake Barricade & West Outlying Crags
        ('pf_barricade', 53, 20), ('pf_barricade', 52, 17), ('wr_stakes', 53, 23),
        ('wr_ban_ash_t', 8, 9), ('wr_ban_ash_t', 8, 29),
        ('gd_spire', 3, 9), ('gd_shard0', 5, 31), ('gd_shard2', 4, 24),
        ('ak_rock2', 3, 28), ('sk_rock_big', 4, 11),
    ]
    for nm, x, y in camp_props:
        r.near(nm, x, y, on='su', r=2)

    # Charred north & south camp palisade walls
    for x in range(23, 54):
        for y in (2, 37):
            if not m.taken[y, x] and m.cls[y, x] in 'su' and not m.cliff[y, x] and m.ht[y, x] == 0 and not r.road_mask[y, x] and x % 8 != 0:
                m.stamp('wr_pal_hb' if (x + y) % 3 == 0 else 'wr_pal_h', x, y, mark='B')

    CK.props(r, ['sk_rock_big', 'sk_boulder', 'sk_pebbles'], 9, box=(1, 1, 9, H - 1), on='su', clump=2, seed=5)
    frame_border_crags(r, sides='NSW', kinds=('sk_rock_big', 'sk_boulder', 'ak_rock2'), seed=9249)
    seal_non_exit_edge(r, 'W', palette=('wr_pal_v', 'wr_stakes', 'wr_sandbags'))

    r.dress(trees=('nt_deadtree',), n_trees=0, copses=0, scatter=0)
    m.cls[m.cls == 'd'] = 'u'
    r.paint()

    # 7. Clean Sand Base + Multi-Layer Volcanic Scorch (L_floorpatch), Packed Roads (E_floorpatch) & Vitrified Glass!
    sand_base = clean_sand_base(r)

    # Scorched volcanic drill yards & command plaza (L_floorpatch 48-shape dark charcoal basalt!)
    scorch = (
        blob(W, H, 36, 15, 7.5, 4.5, 92421, 0.35) |   # War-tent Command Plaza
        blob(W, H, 29, 26, 6.5, 4.0, 92422, 0.38) |   # Mess fire & inner drill yard
        blob(W, H, 45, 25, 5.5, 4.0, 92423, 0.35) |   # Field Forge yard
        blob(W, H, 15, 19, 4.5, 8.0, 92424, 0.40) |   # Between the two fired earthworks
        blob(W, H, 48, 33, 5.0, 3.5, 92425, 0.38)     # SE quartermaster yard
    )
    paint_patch(r, scorch, 'L_floorpatch', sand_base, smooth=2)

    # Packed-earth war-roads & earthwork trenches
    trench_m = np.zeros((H, W), bool)
    for x, y in works:
        if m.inb(x - 1, y) and not m.cliff[y, x - 1]:
            trench_m[y, x - 1] = True
    paint_patch(r, (r.road_mask | trench_m) & ~scorch, 'E_floorpatch', sand_base, smooth=1)

    # Vitrified black-green obsidian glass fired by dragons, Torkoal engineers & forge
    g924 = paint_glass(
        r,
        blob(W, H, 48, 13, 5.5, 3.2, 92401, 0.38) |
        blob(W, H, 4, 20, 4.2, 7.5, 92402, 0.42) |
        blob(W, H, 44, 25, 3.5, 2.5, 92403, 0.35) |
        (m.ht == 1),
        sand_base, cracks=0.14, rope=0.10, seed=924,
    )
    glass_dress(r, g924, sheen=0.09, sky=0.03, seed=924)
    glass_ledges(r, g924)

    paint_cliff_shadows(r, 'L_shadow', exclude=g924)
    sand_dress(r, 0.38, seed=924, exclude=g924, bones=0.015)

    # Glowing volcanic embers, ember cracks & earthwork trench decals
    decal(r, ['wr_ember0', 'wr_ember1', 'wr_ember2'], 0.30, seed=2, exclude=g924)
    decal(r, ['gd_crack0', 'gd_crack1'], 0.08, seed=7, cells=[(x, y) for y, x in np.argwhere(scorch)])
    decal(r, ['wr_trench0', 'wr_trench1'], 0.90, seed=3, cells=[(x - 1, y) for x, y in works], exclude=g924)
    decal(r, ['wr_bones0', 'wr_bones1', 'wr_rut0', 'wr_rut1'], 0.05, seed=4, exclude=g924)

    add_fire_lighting(m)
    place_shaft(m, 35, 11)   # Dramatic warm light over the Dominar's War-Tent entrance!

    CK.scatter_quiet(r, 12)
    h = head(924, 'Ashkaar Siege Camp', field='ASHEN_WASTE', bgm='Route 9', biome='desert',
             connections=[{'dir': 'W', 'offset': 18, 'to': 925, 'to_offset': 13}],
             tone=[18, 4, -10, 10])
    h['metadata']['MapPosition'] = [0, 14, 14]
    r.write(h, '924_siege_camp.yaml', '# Ashkaar Siege Camp (924). WRITTEN BY layouts/war_craft.py (Wave 9) - edit that script.\n')


# ================================================================================================
# 3. MAP 925 — THE STEAMLINE (64x32, ts 56, BLEED / Heavy Seamist)
# ================================================================================================
def build_925():
    W, H = 64, 32
    # Dual-elevation rift valley: level 1 = obsidian-glass volcanic rift walls ('gdc'), sandstone knoll NW!
    r, m = desert(W, H, 925, kit={1: 'gdc', 2: 'sdc', 'default': 'gdc'}, seal='wr_sandbags',
                  stairs=('E_stairl', 'E_stairm', 'E_stairr'))

    # 1. Main caravan road W->E + south crest descent S
    trail(r, [(0, 14.5), (14, 15), (24, 14), (31, 15), (40, 16), (52, 15), (63, 14.5)], w=3.2)
    trail(r, [(31, 16), (31, 24), (31.5, 31)], w=3.2)
    r.exit('W', 13, 4)
    r.exit('E', 13, 4)
    r.exit('S', 30, 4)

    # 2. Dramatic Rift Valley Topography:
    #    - NW Isenmar frosted lookout knoll (ht=1, climbed by stair at x=6..8)
    #    - NE & SE volcanic obsidian-glass canyon shoulders framing Ashkaar's scorched rift approach
    #    - North & South obsidian canyon walls pinching the Steamline gorge!
    ridge(r, 3, 12, 2, 9, seed=11, h=1, rough=0.35)      # NW Isenmar lookout knoll
    ridge(r, 42, 54, 0, 5, seed=9251, h=1, rough=0.38)   # NE volcanic rim shoulder
    ridge(r, 54, 63, 1, 7, seed=9252, h=1, rough=0.36)   # Far-NE basalt bluff
    ridge(r, 44, 54, 26, 31, seed=9253, h=1, rough=0.36) # SE obsidian canyon rim
    ridge(r, 18, 26, 26, 31, seed=9254, h=1, rough=0.35) # SW-central frosted bluff framing south exit

    # Keep roads, exits, events & frozen pool footprints strictly clear of cliffs
    for y in range(H):
        for x in range(W):
            if r.road_mask[max(0, y - 1):y + 4, max(0, x - 1):x + 2].any():
                m.ht[y, x] = 0
            if 58 <= x <= 62 and 26 <= y <= 30:  # FIRESTONE (60, 28)
                m.ht[y, x] = 0
            if 28 <= x <= 35 and 0 <= y <= 31:   # center rift stays navigable
                m.ht[y, x] = 0
            if 2 <= x <= 11 and 10 <= y <= 16:   # lookout (8,13), berry (5,13), Field marker (10,13)
                m.ht[y, x] = 0
    CK.smooth_ht(m, 1, 2)
    # Guarantee NW lookout knoll top stays intact for stair + sledfort
    m.ht[3:8, 5:11] = 1
    CK.smooth_ht(m, 1, 2, box=(2, 1, 14, 11))

    # 3. West Frozen Flood Basins (NW & SW sliding ice pools; SW spit strictly sealed on foot -> ICESTONE!)
    nw = blob(W, H, 17.5, 6.2, 6.2, 3.1, 92511, 0.35) & (m.ht == 0)
    sw = blob(W, H, 12.2, 24.5, 9.2, 3.6, 92512, 0.30) & (m.ht == 0)
    # Keep ice off cliffs below NW knoll & SW-central bluff
    for y in range(H):
        for x in range(W):
            if m.ht[max(0, y - 3):y + 1, x].any():
                nw[y, x] = False
                sw[y, x] = False
    SPIT = [(2, 23), (2, 24), (2, 25), (3, 24), (3, 25)]
    for x, y in SPIT:
        sw[y, x] = False
    # Guarantee a solid contiguous ice apron east & north/south of SPIT so SPIT is 100% strictly sealed on foot!
    for y in range(21, 29):
        for x in range(4, 16):
            if m.ht[y, x] == 0 and not r.road_mask[y, x]:
                if (x - 11.5) ** 2 / 64.0 + (y - 24.5) ** 2 / 14.0 <= 1.0:
                    sw[y, x] = True
    # Plug the NW corner of the SW pool so (4,22), (4,23), (5,22) are sliding ice (zero foot bypass around SPIT!)
    for ix, iy in ((4, 22), (4, 23), (5, 22), (5, 23), (4, 26), (4, 27)):
        if m.ht[iy, ix] == 0 and not r.road_mask[iy, ix]:
            sw[iy, ix] = True
    for x, y in SPIT:
        sw[y, x] = False
    # Wall the spit off on foot using geological rock/ice barrier cells (covering x=0..5 around SPIT cleanly!)
    spit_wall = []
    for y in range(19, 31):
        for x in range(0, 6):
            if (x, y) not in SPIT and not sw[y, x] and not r.road_mask[y, x] and m.ht[y, x] == 0:
                m.cls[y, x] = 'B'
                spit_wall.append((x, y))
    # Guarantee (3, 23) and (3, 26) directly above/below SPIT (3,24..25) are sealed if dry
    for wx, wy in ((3, 22), (3, 23), (3, 26), (3, 27)):
        if not sw[wy, wx]:
            m.cls[wy, wx] = 'B'
            spit_wall.append((wx, wy))

    ice = plan_ice(r, nw | sw)
    for x, y in SPIT:
        m.taken[y, x] = True

    # Organic sand/glass dune ledges on east and far-west flats
    ev_excl = ice.copy()
    ev_excl[:, 26:38] = True
    dunes(r, 3, 925, box=(3, 16, 24, 21), w=(4, 7), exclude=ev_excl)
    dunes(r, 4, 926, box=(40, 6, 61, 25), w=(4, 8), exclude=ev_excl)

    r.finish_plan(border=1)

    # 4. ALL 17 HEAD Events pinned to exact HEAD IDs (1..17) & coordinates!
    E = [
        gauntlet((27, 14), 'ISENMAR_SOLDIER_M', 'Soldier', 1, 'WAR_SIDE_MID',
                 "Between the lines? Then you're nobody's. Nobody's is fair game.", "...You really are nobody's. All right.", d='right'),
        gauntlet((36, 16), 'ASHKAAR_SOLDIER_M', 'Soldier', 1, 'WAR_SIDE_MID',
                 'You walked out of the steam like it was a door. Show me the rest.', "The steam lets you through. So will I.", d='left'),
        fx(item((2, 24), 'ICESTONE')),
        make_front(),
        fx(sign((10, 13), 'Field marker', "ISENMAR LINES -> W.  The rest is anybody's.")),
        fx(sign((54, 12), 'Field marker ', "ASHKAAR LINES -> E.  (Somebody has scratched under it: \"and the glass is nobody's.\")")),
        fx(obj('The steam wall', (29, 8), [
            'Where ice meets fire the air is a wall: steam that never thins, and inside it the Bleed ringing like a struck glass.',
            'Soldiers who walk in come out with frost on one side of their face and burns on the other. You walk in. It goes quiet.'])),
        fx(obj('Glassed sand', (35, 22), ['Sand fused to glass a foot deep, clouded, with things in it: a boot, a spearhead, a whole Sandile, curled up.'])),
        fx(obj('Convoy marker', (20, 17), ['A cairn of sled runners with a white rag tied on: the convoys from Duneholt stop here and wait for someone who can walk them through.'])),
        soldier((18, 13), 'Isenmar sentry', 'NPC 11', ["Isenmar sentry: Past this point the ground can't decide what it is. Neither can you, after a while."], d='right'),
        soldier((45, 17), 'Ashkaar sentry', 'NPC 21', ["Ashkaar sentry: The Dominar says the glass is ours by right of fire. The glass hasn't said."], d='left'),
        fx(hidden((33, 3), 'STARDUST', 'HiddenItem (the glass)')),
        fx(item((60, 28), 'FIRESTONE')),
        fx(obj('Frozen flood', (14, 20), [
            'The sea came this far. Then the Glaceon lines came out of their trenches and the sea stopped, mid-wave, and stayed.',
            'The ice is clear as a window. There are fish in it, and a boot, and the Isenmar standard, still upright.'])),
        fx(obj('Ice-locked whaleboat', (21, 9), ['A whaleboat from Skaldfast, frozen into the flood up to its gunwales. Its oars are still out.'])),
        soldier((8, 13), 'Isenmar lookout', 'NPC 11', [
            "Isenmar lookout: From up here you see it all: the sea frozen on our side, the glass on theirs, and the steam where they meet."], d='down'),
        fx({'type': 'berry', 'at': [5, 13], 'berry': 'ASPEARBERRY'}),
    ]
    r.add(*E)
    r.seat_events(on='su')

    # Solve SW frozen-flood sliding puzzle onto SPIT (3, 24)
    stop = ice_puzzle(r, sw & ice, (3, 24), seed=9251)

    # Stair up NW Isenmar lookout knoll
    yk = max(y for y in range(11) if m.ht[y, 7] == 1)
    CK.stair(r, 6, yk, w=3, h=1)

    # 5. Cohesive Thermal Crystal Spires & Obsidian Shards along the Central Rift (NO garish rainbow candy spam!)
    #    Use frost-blue/clear on the west flank of the rift, teal/obsidian glass spires in the core, amber/red embers on east!
    rng = random.Random(925)
    lanes = (5, 15, 24)
    for y in range(2, H - 2):
        for x in range(27, 37):
            if r.road_mask[y, x] or any(abs(y - ly) <= 1 for ly in lanes) or m.taken[y, x] or m.cls[y, x] not in 'su' or m.ht[y, x] > 0:
                continue
            if vnoise(x, y, 9251, 2.8) > 0.48 and rng.random() < 0.45:
                if x < 30:
                    nm = rng.choice(['cr_clear_c', 'cr_blue_c', 'cr_clear_t', 'gd_shard0'])
                elif x > 33:
                    nm = rng.choice(['gd_spire', 'gd_shard1', 'cr_orange_c', 'cr_red_c', 'gd_shard0'])
                else:
                    nm = rng.choice(['gd_spire', 'cr_teal_c', 'cr_teal_t', 'cr_clear_e', 'gd_shard0'])
                st = STAMPS[nm]
                if m.free(x, y, st['w'], st['h'], on='su') and not m.cliff[y:y + st['h'], x:x + st['w']].any():
                    m.stamp(nm, x, y, mark='B')

    # 6. Storytelling Landmarks: Frozen Wrecks, Steaming Thermal Geysers, Burnt Ashkaar Pickets!
    props_925 = [
        # NW Isenmar Lookout Knoll & Frozen Sea
        ('wr_sledfort2', 4, 3), ('wr_ban_ise', 10, 3), ('fw_brazier', 7, 5),
        ('fw_boat', 20, 8), ('fw_sled', 15, 18), ('fw_sled', 8, 17), ('fw_wood', 13, 17),
        ('fw_rack', 21, 18), ('wr_sacks', 19, 17), ('wr_sandbags', 16, 16), ('wr_stakes', 24, 16),
        ('cr_clear_t', 11, 9), ('cr_blue_t', 24, 5), ('cr_clear_c', 13, 3), ('cr_blue_e', 25, 7),
        ('fw_reeds0', 12, 8), ('fw_reeds1', 22, 6), ('cr_clear_t', 22, 22), ('cr_blue_c', 21, 26),
        ('wr_glasssled', 20, 22), ('wr_ban_ise', 12, 9), ('wr_ban_ise_t', 22, 10),
        # Central Thermal Steam Geyser Pools (hissing pools + curling steam plumes!)
        ('gd_pool3', 35, 5), ('gd_pool2', 25, 19), ('gd_pool3', 36, 25),
        ('gd_spire', 27, 2), ('gd_spire', 35, 1), ('gd_spire', 26, 26), ('gd_spire', 36, 19),
        # East Ashkaar Scorched Picket Line & Shattered Siege Gear
        ('wr_ban_ash_t', 40, 10), ('wr_stakes', 39, 13), ('wr_picket', 49, 9), ('wr_picket', 52, 9), ('wr_picket', 55, 9),
        ('wr_pal_hb', 48, 12), ('wr_pal_hb', 49, 12), ('wr_pal_h', 50, 12),
        ('wr_treb_broken', 43, 21), ('nr_colfall', 45, 25), ('pf_wagon', 41, 6),
        ('wr_ban_ash', 51, 19), ('wr_sledfort', 57, 23), ('wr_supply', 56, 17),
        ('fw_brazier', 47, 17), ('fw_brazier', 57, 12), ('wr_firering', 53, 20),
        ('ak_boulder', 40, 25), ('sk_rock_big', 14, 29), ('wr_sacks', 8, 16),
    ]
    for nm, x, y in props_925:
        r.near(nm, x, y, on='su', r=2)

    CK.props(r, ['sk_rock_big', 'sk_boulder', 'sk_pebbles'], 12, box=(2, 2, W - 2, H - 2), on='su', clump=2, seed=5)

    # Organic geological perimeter framing (ZERO cyan gd_shard2 border picket fence!)
    frame_border_crags(r, sides='NSWE', kinds=('sk_rock_big', 'sk_boulder', 'ak_rock2'), seed=9257)
    seal_non_exit_edge(r, 'W', palette=('wr_sandbags', 'fw_pal_v', 'wr_stakes'))
    seal_non_exit_edge(r, 'E', palette=('wr_pal_v', 'wr_stakes', 'wr_sandbags'))
    seal_non_exit_edge(r, 'S', palette=('wr_sandbags', 'wr_stakes', 'wr_pal_h'))

    r.dress(trees=('nt_deadtree',), n_trees=0, copses=0, scatter=0)
    m.cls[m.cls == 'd'] = 'u'
    r.paint()

    # 7. Clean Sand Base + Frost West vs Volcanic Ash East vs Vitrified Obsidian Rift Center!
    sand_base = clean_sand_base(r)

    # West frosted tundra-sand (S_floorpatch)
    frost_w = np.zeros((H, W), bool)
    for y in range(H):
        cut = 25.5 + 2.5 * (vnoise(0, y, 9252, 4.0) - 0.5) * 2
        for x in range(W):
            if x < cut and vnoise(x, y, 9255, 5.5) > 0.30:
                frost_w[y, x] = True
    frost_w &= ~ice & ~r.road_mask
    paint_patch(r, frost_w, 'S_floorpatch', sand_base, exclude=ice, smooth=2)

    # East volcanic scorched ash flats (L_floorpatch)
    ash_e = np.zeros((H, W), bool)
    for y in range(H):
        cut = 38.0 + 2.8 * (vnoise(10, y, 9256, 4.5) - 0.5) * 2
        for x in range(W):
            if x > cut and vnoise(x, y, 9257, 5.5) > 0.36:
                ash_e[y, x] = True
    ash_e &= ~r.road_mask
    paint_patch(r, ash_e, 'L_floorpatch', sand_base, smooth=2)

    # Packed-earth caravan road approaching the rift from both sides
    paint_patch(r, r.road_mask & ~ice, 'E_floorpatch', sand_base, exclude=ice, smooth=1)

    # Central serpentine vitrified obsidian-glass thermal rift + scorched glass pockets east
    glass_mask = (
        band(W, H, [(31, 0), (30, 8), (32, 16), (31, 24), (31, 31)], 3.8, 92501, wob=0.50) |
        blob(W, H, 47, 6, 5.0, 3.0, 92513, 0.45) |
        blob(W, H, 52, 23, 5.2, 3.2, 92514, 0.45) |
        (m.ht == 1) & (np.arange(W)[None, :] > 16)
    ) & ~ice
    glass = paint_glass(r, glass_mask, sand_base, cracks=0.10, rope=0.11, seed=925)
    glass_dress(r, glass, sheen=0.09, sky=0.04, seed=925)
    glass_ledges(r, glass)

    # Weathered timber bridge causeway spanning the hissing thermal rift along the main E-W caravan road (y=14..15, x=28..34)!
    for bx in range(28, 35):
        for by, bname in ((14, 'fw_bridge_n0'), (15, 'fw_bridge_m0'), (16, 'fw_bridge_s0')):
            if not m.taken[by, bx] and not m.cliff[by, bx] and m.cls[by, bx] in 'su':
                m.L[1, by, bx] = P1(bname)
                m.L[2, by, bx] = 0

    # Frozen pools + geological frost/rock barrier sealing the SW ICESTONE spit cleanly!
    paint_ice(r, ice, sand_base, stop, seed=925)
    for x, y in spit_wall:
        if m.L[1, y, x] == 0 or _is_sand_l1(m, y, x, sand_base) or _is_floorpatch_tile(m.L[1, y, x]):
            m.L[1, y, x] = P1('cr_blue_c' if (x + y) % 3 == 0 else 'wr_sandbags' if (x + y) % 3 == 1 else 'cr_clear_c')
            m.L[2, y, x] = 0

    paint_cliff_shadows(r, 'L_shadow', exclude=ice | glass)
    sand_dress(r, 0.34, seed=925, exclude=ice | glass)

    # Frost drifts west, volcanic embers & glowing cracks east, rising steam curtain along center rift
    decal(r, ['wr_frost0', 'wr_frost1', 'wr_frost2'], 0.32, seed=1,
          cells=[(x, y) for y in range(H) for x in range(0, 27) if not ice[y, x]], exclude=ice | glass)
    decal(r, ['fw_drift0', 'fw_drift1', 'fw_drift2'], 0.12, seed=12,
          cells=[(x, y) for y in range(H) for x in range(0, 26) if frost_w[y, x]], exclude=ice)
    decal(r, ['wr_ember0', 'wr_ember1', 'wr_ember2'], 0.36, seed=2,
          cells=[(x, y) for y in range(H) for x in range(37, W)], exclude=ice | glass)
    decal(r, ['gd_crack0', 'gd_crack1'], 0.10, seed=14,
          cells=[(x, y) for y, x in np.argwhere(ash_e)], exclude=ice)

    # Permanent Steam Wall along the thermal clash zone + curling steam plumes over geyser basins
    for y in range(H):
        for x in range(25, 39):
            if m.inb(x, y) and not m.L[2, y, x] and not m.taken[y, x] and not m.cliff[y, x] and m.cls[y, x] in 'su':
                if vnoise(x, y, 9253, 3.0) > 0.32 - 0.25 * (1 - abs(x - 31.5) / 7.0):
                    m.L[2, y, x] = P1('wr_steam%d' % ((x + 2 * y) % 3))
    for nm, sx, sy in list(m.stamps):
        if nm.startswith('gd_pool'):
            place_smoke(m, sx + 1, sy - 1, 'fw_smoke_w')

    add_fire_lighting(m)
    place_shaft(m, 30, 12)   # Atmospheric shaft piercing the steamline bridge!

    CK.scatter_quiet(r, 8)
    h = head(925, 'The Steamline', field='BLEED', bgm='Route 9', biome='bleed',
             connections=[{'dir': 'W', 'offset': 13, 'to': 920, 'to_offset': 13},
                          {'dir': 'E', 'offset': 13, 'to': 924, 'to_offset': 18},
                          {'dir': 'S', 'offset': 2, 'to': 926, 'to_offset': 0}],
             tone=[6, -4, 10, 30], fog={'name': 'prismfall_seamist', 'opacity': 60, 'blend': 0, 'zoom': 150, 'sx': 2, 'sy': 0})
    h['metadata']['MapPosition'] = [0, 13, 14]
    h['walk_from'] = [[3, 25]]
    h['gates'] = [{'name': 'The Icestone spit (over the frozen flood only)', 'from': [[1, 14], [62, 14], [31, 30]], 'sealed': [[3, 24]], 'ice_solid': True}]
    r.write(h, '925_steamline.yaml', '# The Steamline (925, :BLEED). WRITTEN BY layouts/war_craft.py (Wave 9) - edit that script.\n')


# ================================================================================================
# 4. MAP 926 — THE GLASS DUNES (60x48, ts 56, DESERT — Ch19 WAR-1 Climax Battleground!)
# ================================================================================================
def partner_page(sw, who, ver, foes, lines, win):
    return {
        'cond': {'switch': sw},
        'graphic': {'sprite': SPRITE['LEADER_%s' % who.upper()], 'dir': 'down'},
        'trigger': 'action',
        'commands': list(lines) + [
            {'script': 'pbRegisterPartner(:LEADER_%s, "%s", %d)' % (who.upper(), who, ver)},
            {'script': 'setBattleRule("double")'},
            {'if': 'TrainerBattle.start(%s)' % foes,
             'then': [PARTNER_END] + list(win) + [{'script': 'pfm_set(:war_partner_done)'}, {'selfswitch': ['A', True]}],
             'else': [PARTNER_END]},
        ],
    }


def build_926():
    W, H = 60, 48
    r, m = desert(W, H, 926, kit='gdc', seal='wr_sandbags',
                  stairs=('L_stairl', 'L_stairm', 'L_stairr'))

    # 1. Primary tactical roads (caravan road, crest entrance, camp approaches, goat-path south)
    trail(r, [(29.5, 0), (30, 6), (30, 12)], w=3.2)                                  # Steamline -> Crest arena
    trail(r, [(7, 1), (9, 12), (14, 22), (24, 28), (36, 30), (48, 31), (59, 31.5)], w=3.2)
    trail(r, [(51, 1), (50, 12), (47, 22), (44, 30)], w=3.0)
    trail(r, [(30, 31), (30, 40), (30, 46)], w=2.4, only='su.')
    trail(r, [(16, 40.5), (10, 40.5), (4, 41.5)], w=3.2)                               # wide sally port -> Isenmar blue camp (clear around straggler @ 6,40!)
    trail(r, [(44, 34), (47, 41), (47, 46), (57, 46)], w=2.0, only='su.')              # clean SE Ashkaar camp path to MAXREVIVE (58,46)!
    r.exit('N', 28, 4)
    r.exit('E', 30, 4)

    # 2. Sculpted Obsidian-Glass Crater Walls (Sealing the Climax Crest Amphitheater Organically!)
    #    Ragged curving outer slopes while keeping the exact sealed core (x=13..17 & x=43..47, y=0..12) 100% solid!
    for x0, x1, out in ((13, 17, -1), (43, 47, 1)):
        for y in range(0, 13):
            for x in range(x0, x1 + 1):
                m.ht[y, x] = 1
            # Curved amphitheater shoulders wider near y=2..8, tapering organically near y=11..12
            arch = int(round(2.5 * math.sin(math.pi * y / 13.0) + 1.8 * vnoise(x0, y, 9267, 3.0)))
            for k in range(1, arch + 1):
                xx = (x0 - k) if out < 0 else (x1 + k)
                if 0 <= xx < W and not r.road_mask[y, xx]:
                    m.ht[y, xx] = 1

    # Four sculpted obsidian-glass battlefield lookout ridges
    ridge(r, 16, 25, 33, 38, seed=1, h=1, rough=0.40)    # West lookout ridge (stair from central lane)
    ridge(r, 34, 43, 36, 41, seed=2, h=1, rough=0.40)    # South-central glass ridge
    ridge(r, 51, 58, 16, 22, seed=3, h=1, rough=0.40)    # East lookout ridge (stair from east lane)
    ridge(r, 49, 57, 38, 43, seed=4, h=1, rough=0.40)    # SE glass bluff

    # Keep roads and key item/event pockets cleanly carved out of cliffs
    for x0, x1, y0, y1 in ((15, 26, 31, 40), (33, 44, 34, 43), (50, 59, 14, 24), (48, 58, 36, 45)):
        for y in range(y0, min(H, y1 + 1)):
            for x in range(x0, min(W, x1 + 1)):
                if r.road_mask[max(0, y - 1):y + 4, max(0, x - 1):x + 2].any():
                    m.ht[y, x] = 0
        CK.smooth_ht(m, 1, 2, box=(max(0, x0 - 1), max(0, y0 - 1), min(W, x1 + 2), min(H, y1 + 2)))
    CK.smooth_ht(m, 1, 2, box=(8, 0, 20, 14))
    CK.smooth_ht(m, 1, 2, box=(41, 0, 53, 14))
    # Guarantee Crest side walls stay 100% sealed (strict GATE invariant!)
    for x0, x1 in ((13, 17), (43, 47)):
        m.ht[0:13, x0:x1 + 1] = 1
    # Guarantee FULLRESTORE (22, 35) & HYPERPOTION (55, 18) sit cleanly on top of their lookout ridges (ht=1)!
    m.ht[33:37, 19:24] = 1
    m.ht[17:21, 53:57] = 1

    # Stairs up the West (y=31..40) & East (y=15..24) battlefield lookout ridges (explicit y-bounds so East Ridge never hits SE bluff!)
    for sx, ex, y0, y1 in ((20, 29, 31, 41), (53, 48, 15, 25)):
        col = [y for y in range(y0, y1) if m.ht[y, sx + 1] == 1]
        if not col:
            continue
        lip = max(col)
        CK.stair(r, sx, lip, w=3)
        foot = lip + 4
        trail(r, [(ex, foot + 0.5), (sx + 1, foot + 0.5)], w=2.0, only='su.')

    # 3. Braided Turquoise Flood Channels across the western Isenmar flats (Kyogre's sea dragged inland!)
    flood = (
        band(W, H, [(0, 13), (3, 15), (5, 20), (10, 24), (16, 26), (19, 30)], 1.35, 9261) |
        band(W, H, [(0, 26), (5, 28), (8, 33), (7, 38), (11, 43), (13, 47)], 1.40, 9262) |
        band(W, H, [(5, 28), (2, 34), (0, 37)], 1.05, 9263)
    )
    flood = plan_flood(r, flood)

    # Organic wind-carved dune lee ledges (avoiding roads, flood & events)
    dunes(r, 6, 9268, box=(19, 21, 47, 30), w=(4, 8), exclude=flood)
    dunes(r, 4, 9269, box=(44, 33, 57, 37), w=(4, 7), exclude=flood)
    dunes(r, 3, 9270, box=(15, 41, 28, 46), w=(4, 7), exclude=flood)

    r.finish_plan(border=1)

    # 4. ALL 30 HEAD Events pinned at exact HEAD IDs (1..30) & coordinates!
    legend = [{'if': '!pfm?(:war_partner_done)', 'then': ['(The ground is shaking. Over the sea the clouds are turning the wrong way. Not yet.)'],
               'else': [{'if': 'pfm?(:war_battle_done)', 'then': ['(The glass hums underfoot, quietly. It is over.)'], 'else': [
                   {'script': "legend = (pf_choice(:war_legend) rescue nil)\n"
                              "if legend != :neither\n"
                              "  Prismfall::Bosses.wild_battle($game_switches[605] ? :KYOGRE_GLASS_DUNES : :RESHIRAM_GLASS_DUNES)\n"
                              "end"},
                   {'if': "((pf_choice(:war_legend) rescue nil) == :neither) || ((Prismfall::Bosses.last_result || {})[:result] == :turned_back)",
                    'then': [{'script': 'Prismfall::Cutscene.play(:WAR_CLIMAX) rescue nil'}, {'script': 'pfm_set(:war_battle_done)'}],
                    'else': ['(It wheels away over the flood and comes round again. The crest shakes.)']}]}]}]
    legend_pages = [{'commands': []}] + [{'cond': {'switch': sw}, 'trigger': 'action', 'commands': legend}
                                         for sw in ('WAR_SIDE_MID', 'WAR_SIDE_ASH', 'WAR_SIDE_ISE')]
    E = [
        {'type': 'warp', 'name': 'To the Rimed Sands', 'at': [7, 1], 'link': 'WAR_RIMED_DUNES', 'arrive': [7, 2, 'down'], 'fixed': True},
        {'type': 'warp', 'name': 'To the Siege Camp', 'at': [51, 1], 'link': 'WAR_CAMP_DUNES', 'arrive': [51, 2, 'down'], 'fixed': True},
        gauntlet((27, 8), 'ASHKAAR_SOLDIER_F', 'Soldier', 1, 'WAR_SIDE_ASH', "The crest is held. By me, for now.", 'For now.', d='down'),
        gauntlet((33, 8), 'ISENMAR_SOLDIER_F', 'Soldier', 1, 'WAR_SIDE_ASH', "One more between you and the crest.", 'Go. Look at what we did.', d='down'),
        gauntlet((27, 9), 'ASHKAAR_SOLDIER_F', 'Soldier', 1, 'WAR_SIDE_ISE', "The crest is held. By me, for now.", 'For now.', d='down'),
        gauntlet((33, 9), 'ISENMAR_SOLDIER_F', 'Soldier', 1, 'WAR_SIDE_ISE', "One more between you and the crest.", 'Go. Look at what we did.', d='down'),
        gauntlet((27, 10), 'ASHKAAR_SOLDIER_F', 'Soldier', 1, 'WAR_SIDE_MID', "The crest is held. By me, for now.", 'For now.', d='down'),
        gauntlet((33, 10), 'ISENMAR_SOLDIER_F', 'Soldier', 1, 'WAR_SIDE_MID', "One more between you and the crest.", 'Go. Look at what we did.', d='down'),
        {'type': 'event', 'name': 'Partner', 'at': [30, 4], 'fixed': True, 'pages': [
            {'commands': []},
            partner_page('WAR_SIDE_MID', 'Sigrun', 19, ':ISENMAR_OFFICER, "Captain", 1, :ASHKAAR_OFFICER, "Captain", 1',
                         ['Sigrun: Between them? Then we hold the middle. Both captains are coming. Back to back.'],
                         ['Sigrun: Still standing. Both of us. Look up.']),
            partner_page('WAR_SIDE_ASH', 'Sigrun', 19, ':ISENMAR_OFFICER, "Captain", 1, :ISENMAR_SOLDIER_M, "Soldier", 2',
                         ["Sigrun: With us, then. The Isenmar line breaks here or nowhere."],
                         ['Sigrun: It broke. Now the sky.']),
            partner_page('WAR_SIDE_ISE', 'Marisol', 19, ':ASHKAAR_OFFICER, "Captain", 1, :ASHKAAR_SOLDIER_M, "Soldier", 2',
                         ["Marisol: Kid. You came. Course you came. Stand on my left; the sea's on my right."],
                         ["Marisol: Ha! The Ebb runs both ways, and today it ran ours."]),
            {'cond': {'self': 'A'}, 'commands': ['(The ground under the crest is humming. Something enormous is coming.)']},
        ]},
        {'type': 'event', 'name': 'The legend', 'at': [30, 2], 'fixed': True, 'pages': legend_pages},
        {'type': 'event', 'name': 'Goat-path', 'at': [30, 46], 'fixed': True,
         'pages': [{'trigger': 'action', 'commands': [
             {'if': 'pfm?(:war_battle_done)',
              'then': ["A goat-path up the sandstone to the mesa, where Meridian's white tents stand.",
                       {'se': 'Door exit'},
                       {'transfer': {'map': 929, 'x': 17, 'y': 26, 'dir': 'up'}}],
              'else': ['A goat-path up the sandstone mesa. Meridian guards in white at the top, with brass glasses on everything. "Observers only."']}]}]},
        make_front(),
        fx(sign((27, 1), 'Field marker', 'THE CREST. Below it, the caravan road and the wells. Above it, everything else.')),
        fx(obj('Caravan well', (36, 33), ["A caravan well between the lines. A white ribbon on the sweep: the bone-carters' sign. No blood at a well. Both armies keep that."])),
        fx(obj('Caravan well ', (18, 26), ['The second well, its bucket gone, its rope cut. Someone has left a full waterskin on the rim for whoever comes next.'])),
        fx(obj("Bone-carters' banner", (40, 9), ["The bone-carters' white banner on the crest's east shoulder. Under it, a tally-stick for every soldier carried off the sand. Both armies' names."])),
        fx(obj('Wrecked sled', (10, 18), ['An Isenmar sled-fort, overturned, its runners in the air, burnt to the iron on the eastern side.'])),
        fx(obj('The frozen wave', (7, 9), [
            'A wave, taller than a house, standing on dry sand. It broke over the dunes at noon and the ice caught it before it landed.',
            'Inside the curl the light is green. Something small and silver is frozen in it, mid-leap. A Feebas, maybe.'])),
        fx(obj('The causeway', (13, 22), ['Where the caravan road crosses the flood the sand has run to glass a yard thick: the only dry way over the water for a mile.'])),
        fx(obj('Steaming pool', (24, 21), ['Flood water in a basin of glass, still too hot to touch. It hisses where the edge is thinnest.'])),
        fx(obj('Broken trebuchet', (38, 18), ['An Ashkaar trebuchet, its arm snapped clean. The far side of it has run like candle wax and set hard as green glass.'])),
        fx(talk('Bone-carter', (31, 35), 'NPC 27', ["Bone-carter: We carry them out. Whose they were doesn't matter. Whose they are now does: Ossaria's. Tomb-law."], d='left')),
        fx(talk('Ashkaar straggler', (54, 27), 'NPC 21', ["Ashkaar straggler: The palisade burnt from the inside. Our own fire. Reshiram doesn't take sides; it takes everything."], d='left')),
        fx(talk('Isenmar straggler', (6, 40), 'NPC 11', ["Isenmar straggler: The sea came over the dunes like it had somewhere to be. We built the trench to keep fire out. Not water."], d='right')),
        fx(item((22, 35), 'FULLRESTORE')),
        fx(hidden((2, 43), 'STARDUST', 'HiddenItem (dunes)')),
        fx(hidden((38, 4), 'BIGNUGGET', 'HiddenItem (the crest)')),
        fx(item((55, 18), 'HYPERPOTION')),
        fx(hidden((7, 14), 'NEVERMELTICE', 'HiddenItem (behind the wave)')),
        fx(item((58, 46), 'MAXREVIVE')),
    ]

    # Iconic Hero Setpiece: The Frozen Wave (NW, 6x5)
    m.stamp('gd_wave', 1, 6, mark='B')
    r.add(*E)
    r.seat_events(on='su')

    # Crest South Lee: strict one-way glass jump ledge across x=18..42, y=14 (seals Crest from below!)
    for x in range(18, 43):
        m.over.append((1, x, 14, P1('gdl_' + ('w' if x == 18 else 'e' if x == 42 else 'm'))))
        m.taken[14, x] = True
        if m.cls[14, x] not in 'su':
            m.cls[14, x] = 'u'

    # 5. Climax Arena Cathedral Spires, Siege Wrecks, Flooded Frontline & Camp Clusters
    hero_926 = [
        # Iconic Central Climax Arena Framing (glass obelisks + shattered opposing banners framing Partner/Legend!)
        ('gd_spire', 22, 2), ('gd_spire', 36, 2), ('gd_spire', 20, 9), ('gd_spire', 38, 9),
        ('wr_ban_ise_t', 24, 5), ('wr_ban_ash_t', 35, 5), ('wr_ban_bone', 41, 8),
        ('gd_shard0', 25, 2), ('gd_shard1', 34, 2),
        # No-Man's-Land Siege Wrecks, Steaming Basins & Truce Wells
        ('wr_treb_broken', 37, 16), ('wr_treb_broken', 22, 16), ('wr_tower_wreck', 39, 24),
        ('wr_glasssled', 15, 30), ('wr_glasssled', 25, 43), ('wr_sledfort', 8, 16),
        ('gd_pool3', 23, 19), ('gd_pool2', 34, 20), ('gd_pool2', 10, 28), ('gd_pool3', 2, 22),
        ('wr_well', 35, 31), ('wr_well', 17, 24),
        ('wr_ban_ise_t', 19, 16), ('wr_ban_ash_t', 41, 16),
        ('wr_ban_ise', 11, 30), ('wr_ban_ise', 11, 38), ('wr_ban_ash', 49, 25), ('wr_ban_ash', 56, 36),
        ('wr_bonecart', 32, 33), ('wr_bonecart', 27, 37), ('wr_supply', 40, 33), ('wr_supply', 52, 28), ('wr_supply', 18, 23),
        ('pf_wagon', 45, 34), ('wr_tally', 47, 38), ('wr_picket', 55, 30), ('nr_colfall', 53, 45), ('fw_sled', 4, 30),
        ('fw_skull', 33, 37), ('pf_whalebone', 42, 43),
        # NW Frozen Wave Forward Post
        ('wr_sledfort2', 1, 12), ('fw_brazier', 5, 14), ('wr_ban_ise_t', 11, 9),
        ('cr_clear_t', 8, 6), ('cr_blue_t', 1, 3), ('cr_clear_e', 8, 11), ('fw_boat', 1, 17),
        # NE Ashkaar Dragon Lines & Scorched Siege Post
        ('wr_treb_broken', 53, 4), ('wr_picket', 50, 9), ('wr_picket', 56, 10), ('wr_picket', 58, 7),
        ('wr_ban_ash_t', 49, 4), ('fw_brazier', 53, 10), ('wr_sandbags', 54, 13), ('wr_sacks', 57, 13), ('wr_rack', 52, 11),
        # SW Isenmar Blue Camp (keep wide 2-tile lane around Isenmar straggler @ 6,40 so (2,43) stays 100% open!)
        ('wr_tent_b', 2, 37), ('wr_tent_b', 6, 44), ('wr_tent_w', 9, 37),
        ('wr_firering', 4, 44), ('wr_rack', 10, 44), ('wr_sacks', 2, 45), ('wr_sacks', 11, 46), ('fw_brazier', 8, 36),
        # SE Ashkaar Red Camp & Goat-Path Overlook Gateposts
        ('wr_tent_r', 49, 34), ('wr_tent_r', 54, 34), ('wr_firering', 56, 43),
        ('wr_rack', 57, 41), ('wr_sacks', 45, 45), ('wr_picket', 57, 38), ('fw_brazier', 51, 37),
        ('nr_col', 28, 45), ('nr_col', 32, 45), ('pf_roadstone', 28, 43), ('fw_brazier', 32, 42),
    ]
    for nm, x, y in hero_926:
        r.near(nm, x, y, on='su', r=2)

    # Isenmar SW sandbag trench line (with 2 sally ports)
    for y in range(29, 46):
        if y in (33, 34, 40, 41):
            continue
        if not m.taken[y, 13] and m.cls[y, 13] in 'su' and not r.road_mask[y, 13] and not m.cliff[y, 13]:
            m.stamp('wr_sandbags' if y % 3 else 'fw_pal_v', 13, y, mark='B')

    # Ashkaar charred palisade south of east ridge
    for x in range(48, 59):
        if 51 <= x <= 53:
            continue
        if not m.taken[26, x] and m.cls[26, x] in 'su' and not r.road_mask[26, x] and not m.cliff[26, x]:
            m.stamp('wr_pal_hb' if x % 3 else 'wr_pal_h', x, 26, mark='B')

    # No-man's-land stakes framing the south approach
    for y, xs in ((35, range(19, 29)), (35, range(32, 34)), (40, range(32, 34))):
        for x in xs:
            if not m.taken[y, x] and m.cls[y, x] in 'su' and not r.road_mask[y, x] and m.ht[y, x] == 0 and not m.cliff[y, x]:
                m.stamp('wr_stakes', x, y, mark='B')

    # Clustered glass spires, shards & battlefield debris (organic groupings, ZERO sparse scatter!)
    CK.props(r, ['gd_spire', 'gd_shard0', 'gd_shard1', 'gd_shard2'], 18, box=(18, 1, 43, 13), on='su', clump=2, seed=6)
    CK.props(r, ['gd_spire', 'gd_shard0', 'gd_shard1', 'cr_teal_c'], 26, box=(18, 15, W - 2, H - 2), on='su', clump=2, seed=7)
    CK.props(r, ['cr_teal_c', 'cr_clear_c', 'sk_boulder'], 12, box=(2, 15, 28, H - 2), on='su', clump=2, seed=8)
    CK.props(r, ['gd_shard0', 'gd_shard1'], 8, box=(13, 1, 18, 12), on='su', seed=9)
    CK.props(r, ['gd_shard0', 'gd_shard1'], 8, box=(43, 1, 48, 12), on='su', seed=10)
    CK.props(r, ['sk_rock_big', 'sk_boulder', 'ak_rock2'], 10, box=(1, 1, W - 1, H - 1), on='su', clump=2, seed=5)
    CK.props(r, ['wr_firering', 'wr_sacks', 'wr_rack', 'wr_stakes', 'wr_sandbags'], 10, box=(18, 20, 48, 34), on='su', clump=2, seed=11)

    # Organic boulder/glass perimeter framing (ZERO neon-cyan gd_shard2 border fence!)
    frame_border_crags(r, sides='NSE', kinds=('sk_rock_big', 'sk_boulder', 'ak_rock2'), seed=9269)
    seal_non_exit_edge(r, 'N', palette=('wr_sandbags', 'wr_pal_h', 'wr_stakes'), keep_pts=((7, 1), (51, 1)))
    seal_non_exit_edge(r, 'E', palette=('wr_pal_v', 'wr_sandbags', 'wr_stakes'))

    r.dress(trees=('nt_deadtree',), n_trees=0, copses=0, scatter=0)
    m.cls[m.cls == 'd'] = 'u'
    r.paint()

    # 6. Clean Sand Base + Multi-Biome War Ground (Frost NW, Ash SE, Packed Caravan Road, Flood + Glass Causeway, Vitrified Glass!)
    sand_base = clean_sand_base(r)

    # Frost halo around the Frozen Wave & Isenmar western flats (S_floorpatch)
    frost_926 = (
        blob(W, H, 5.5, 9.5, 8.5, 6.8, 92631, 0.38) |
        blob(W, H, 7.0, 41.0, 7.0, 5.5, 92632, 0.40)
    ) & ~flood & (m.ht == 0)
    paint_patch(r, frost_926, 'S_floorpatch', sand_base, exclude=flood, smooth=2)

    # Ashkaar scorched eastern flats (L_floorpatch)
    ash_926 = (
        blob(W, H, 53.0, 8.0, 6.5, 5.5, 92633, 0.40) |
        blob(W, H, 53.0, 29.0, 5.5, 4.5, 92634, 0.38) |
        blob(W, H, 52.0, 44.0, 6.0, 4.0, 92635, 0.38)
    ) & ~flood & (m.ht == 0)
    paint_patch(r, ash_926, 'L_floorpatch', sand_base, exclude=flood, smooth=2)

    # Packed-earth caravan road & Goat-path approach (E_floorpatch)
    paint_patch(r, r.road_mask & ~flood, 'E_floorpatch', sand_base, exclude=flood, smooth=1)

    # Braided turquoise flood channels + wet shore rims + steaming mist
    paint_flood(r, flood, sand_base, steam=0.45, seed=926)

    # Vitrified Obsidian-Glass Clash Crater, Lava-Glass Flows, Glass Causeway Crossing (13,22) & Ridges
    glass = (
        blob(W, H, 30, 6.8, 12.2, 7.5, 92601, 0.35) | (m.ht == 1) |
        band(W, H, [(23, 15), (25, 20), (22, 25), (20, 29)], 2.1, 92602) |
        band(W, H, [(31, 15), (31, 21), (33, 26), (36, 29)], 2.0, 92603) |
        band(W, H, [(37, 15), (41, 20), (46, 25), (52, 29), (58, 31)], 2.4, 92604) |
        blob(W, H, 52, 21, 7, 5, 92605, 0.40) | blob(W, H, 45, 40, 6, 4, 92606, 0.45) |
        blob(W, H, 37, 22, 4, 3, 92607) | blob(W, H, 55, 7, 5, 4, 92608, 0.45) |
        blob(W, H, 24, 41, 7, 3.5, 92609, 0.45) | blob(W, H, 39, 44, 7, 3, 92610, 0.45) |
        blob(W, H, 21, 33, 4, 2.5, 92611, 0.50) |
        band(W, H, [(30, 15), (29, 24), (30, 31), (30, 40)], 1.6, 92612) |
        blob(W, H, 13, 3, 4, 2.5, 92613, 0.40) | blob(W, H, 47, 13, 3, 2, 92614, 0.40) |
        blob(W, H, 4, 25, 3, 2.5, 92615, 0.50) |
        blob(W, H, 13.5, 22.0, 3.0, 2.2, 92616, 0.25)   # Smooth vitrified-glass causeway crossing the flood!
    ) & ~flood
    glass = paint_glass(r, glass, sand_base, cracks=0.08, rope=0.10, spill=0.05, seed=926)
    glass_dress(r, glass, sheen=0.09, sky=0.045, seed=926)
    glass_ledges(r, glass)

    paint_cliff_shadows(r, 'L_shadow', exclude=flood | glass)
    sand_dress(r, 0.40, seed=926, exclude=flood | glass, bones=0.025)

    # Ambient frost, ember cracks, trenches & steam plumes around hot glass pools
    decal(r, ['wr_frost0', 'wr_frost1', 'wr_frost2'], 0.45, seed=6,
          cells=[(x, y) for y, x in np.argwhere(frost_926)], exclude=flood | glass)
    decal(r, ['fw_drift0', 'fw_drift1', 'fw_drift2'], 0.14, seed=15,
          cells=[(x, y) for y, x in np.argwhere(frost_926)], exclude=flood | glass)
    decal(r, ['wr_trench0', 'wr_trench1'], 0.90, seed=3,
          cells=[(12, y) for y in range(29, 46)], exclude=flood | glass)
    decal(r, ['wr_ember0', 'wr_ember1', 'wr_ember2'], 0.28, seed=2,
          cells=[(x, y) for y in range(H) for x in range(42, W)], exclude=flood | glass)
    decal(r, ['gd_crack0', 'gd_crack1'], 0.09, seed=16,
          cells=[(x, y) for y in range(2, 13) for x in range(20, 40)], exclude=flood)
    decal(r, ['wr_steam0', 'wr_steam1', 'wr_steam2'], 0.38, seed=5,
          cells=[(x + dx, y + dy) for (nm, x, y) in m.stamps if nm.startswith('gd_pool')
                 for dx in range(-1, 4) for dy in (-1, 0, 2)], exclude=flood)
    for nm, sx, sy in list(m.stamps):
        if nm.startswith('gd_pool'):
            place_smoke(m, sx + 1, sy - 1, 'fw_smoke_w')

    # Dramatic WAR-1 Climax Atmosphere: light shafts over Clash Arena, Frozen Wave & Causeway + firelight bloom!
    add_fire_lighting(m)
    place_shaft(m, 29, 2)    # Iconic sky-beam illuminating Partner & Legend on the Crest!
    place_shaft(m, 4, 6)     # Dramatic light shaft catching the Frozen Wave!
    place_shaft(m, 29, 43)   # Light over the Goat-path south overlook!

    CK.scatter_quiet(r, 6)
    h = head(926, 'The Glass Dunes', field='DESERT', bgm='Route 9', biome='desert',
             connections=[{'dir': 'N', 'offset': 0, 'to': 925, 'to_offset': 2},
                          {'dir': 'E', 'offset': 30, 'to': 930, 'to_offset': 15}],
             tone=[6, 10, 4, 14], fog={'name': 'prismfall_seamist', 'opacity': 30, 'blend': 0, 'zoom': 200, 'sx': 1, 'sy': 0})
    h['metadata']['MapPosition'] = [0, 13, 15]
    h['gates'] = [{'name': 'The crest (only from the Steamline)', 'from': [[56, 31], [7, 3], [51, 3]], 'sealed': [[30, 4], [30, 6]]}]
    r.write(h, '926_glass_dunes.yaml', '# The Glass Dunes (926). WRITTEN BY layouts/war_craft.py (Wave 9) - edit that script.\n')


# ================================================================================================
# 5. MAP 928 — COMMAND PAVILION (24x18, ts 59 PF Rejuv Manor — Void-Sculpted Imperial War Pavilion!)
# ================================================================================================
def build_928():
    W, H = 24, 18
    # Build on Tileset 59 (PF Rejuv Manor): rich crimson-damask imperial walls ('cvH'), dark carved
    # walnut/mahogany floors ('H_f*'), dark mahogany glass-top lacquer war-map table ('mn_case_*'),
    # real flaming Oath-Braziers ('fw_brazier' + 'pf_glow'), iron hawk-cage ('lm_bars_*'), and void-sculpted silhouette!
    m = Cave(W, H, 'H', seed=928, pool='Cave Pool', tid=59)
    m.kit = {'default': 'cvH', TER: 'cvB'}
    m.STAIRS = tuple(P1('mn_stair_' + k) for k in 'lmr')

    # 1. Void-Sculpted Imperial War-Pavilion Silhouette (ZERO boxy rectangle!)
    #    Starting north floor at y=1 with plan_cliffs(rows=2) makes y=0 void ceiling, y=1..2 crimson-damask
    #    north wall face, and y=3..13 clean walkable floor (so Anja @ [6,3] stands cleanly on cage floor!).
    m.box(3, 1, 20, 13, FLOOR)
    m.box(9, 14, 14, 15, FLOOR)
    m.box(10, 16, 13, 16, FLOOR)

    # Sculpt dramatic chamfered pavilion walls & recessed structural alcoves (cleanly avoiding all events!)
    m.mass_at([
        # SW & SE grand stepped pavilion corners (creates unmistakable T / cruciform imperial tent silhouette!)
        (3, 13), (4, 13), (5, 13), (6, 13),
        (17, 13), (18, 13), (19, 13), (20, 13),
        (3, 12), (4, 12), (19, 12), (20, 12),
        # Mid-nave architectural wall pilasters framing the central war table bay
        (3, 8), (3, 9), (20, 8), (20, 9),
        # Narrow threshold pillars framing the south double exit mat [11, 16] & [12, 16]
        (9, 15), (14, 15),
    ])

    m.tidy()
    m.plan_cliffs(rows=2)

    # 2. Paint base crimson-damask pavilion walls & dark walnut plank flooring
    m.paint()

    # Replace cage alcove floor (x=4..8, y=3..4) with cold dark prison slate (L_f0..3) for stark material contrast!
    for y in (3, 4):
        for x in range(4, 9):
            if m.cls[y, x] == '.' and not m.cliff[y, x]:
                m.L[0, y, x] = P1('L_f%d' % ((x + y) % 4))

    # Give the north Command Dais floor (x=10..14, y=3..5) rich warm parquet (P_f0..3)
    for y in range(3, 6):
        for x in range(10, 15):
            if m.cls[y, x] == '.' and not m.cliff[y, x]:
                m.L[0, y, x] = P1('P_f%d' % ((x * 3 + y) % 4))

    # 3. Ornate Crimson-and-Gold Imperial Carpets & Runners (on Layer 1, pas=0, walkable!)
    def lay_rug(prefix, x0, y0, x1, y1):
        for y in range(y0, y1 + 1):
            r_k = 'n' if y == y0 else ('s' if y == y1 else '')
            for x in range(x0, x1 + 1):
                c_k = 'w' if x == x0 else ('e' if x == x1 else '')
                part = (r_k + c_k) or ('c2' if (prefix == 'mn_rugR' and (x + y) % 2 == 0) else 'c')
                if m.cls[y, x] == '.' and not m.cliff[y, x]:
                    m.L[1, y, x] = P1('%s_%s' % (prefix, part))

    # Grand ceremonial imperial runner marching straight from entry doors [11..12, 16] up to Command Dais [10..14, 3..6]!
    lay_rug('lm_carpet', 10, 11, 13, 16)
    lay_rug('lm_carpet', 10, 3, 14, 6)
    # Ornate Persian crimson-gold war-council carpet cradling the central War-Map Table (x=8..14, y=7..10)!
    lay_rug('mn_rugR', 8, 7, 14, 10)
    # Subtle side runners beneath the Oath-Brazier (x=5..7, y=6..8) and Twin Brazier (x=16..18, y=6..8)
    lay_rug('mn_rugR', 5, 6, 7, 8)
    lay_rug('mn_rugR', 16, 6, 18, 8)

    rugs = {P1('mn_rugR_' + p) for p in ('nw', 'n', 'ne', 'w', 'c', 'c2', 'e', 'sw', 's', 'se')} | \
           {P1('lm_carpet_' + p) for p in ('nw', 'n', 'ne', 'w', 'c', 'e', 'sw', 's', 'se')}

    def put_prop(name, x0, y0):
        st = STAMPS[name]
        L = st['layers']
        for dy in range(st['h']):
            for dx in range(st['w']):
                x, y = x0 + dx, y0 + dy
                if not m.inb(x, y):
                    continue
                for z in (1, 2):
                    t = int(L[z][dy][dx])
                    if not t:
                        continue
                    if z == 1 and int(m.L[1, y, x]) in rugs and int(m.L[2, y, x]) == 0:
                        m.L[2, y, x] = t
                    else:
                        m.L[z, y, x] = t

    def put_tile(name, x, y, prefer_z=1):
        t = P1(name)
        if prefer_z == 1 and int(m.L[1, y, x]) in rugs and int(m.L[2, y, x]) == 0:
            m.L[2, y, x] = t
        else:
            m.L[prefer_z, y, x] = t

    # 4. HERO CENTERPIECE: Dark Mahogany & Glass Lacquer Tactical War-Map Table (x=9..13, y=8..9) — `Map table` [11, 9]!
    #    Dark lacquer wood & glass sand-map cases (NO blinding white wedding tablecloth!) crowned by brass candelabrum!
    for ty in (8, 9):
        for tx, nm in ((9, 'mn_case_l'), (10, 'mn_case_m'), (11, 'mn_case_m'), (12, 'mn_case_m'), (13, 'mn_case_r')):
            m.L[1, ty, tx] = P1(nm)
    # Brass war-council candelabrum & tactical map markers gleaming on Layer 2 atop the mahogany map table!
    m.L[2, 8, 11] = P1('mn_dt_cand')
    # War-council crimson chairs flanking the east and west ends of the map table!
    put_tile('mn_chairR_right', 8, 8, 1)
    put_tile('mn_chairR_right', 8, 9, 1)
    put_tile('mn_chairR_left', 14, 8, 1)
    put_tile('mn_chairR_left', 14, 9, 1)

    # 5. REAL FLAMING OATH-BRAZIER right at [6, 7] (`Oath-brazier`) & Twin Brazier at [17, 7]!
    put_prop('fw_brazier', 6, 6)    # flame at (6,6) pri=2, iron bowl solid at (6,7) right on event [6,7]!
    put_prop('fw_brazier', 17, 6)   # symmetric twin war-brazier at (17,7)!
    # South entry ceremonial braziers flanking the war-tent threshold!
    put_prop('fw_brazier', 9, 13)
    put_prop('fw_brazier', 14, 13)

    # 6. COMMAND DAIS & EMPTY STAND (`Empty stand` at [12, 5], `Dominar Hrothgar` standing right in front at [12, 6]!)
    #    Black-glass Light Stone Cradle (lm_cradle_cold: top at (12,4), pedestal at (12,5)!)
    put_prop('lm_cradle_cold', 12, 4)
    # Flanking royal Ashkaar dragon banners, armored war-guards & golden wall banners framing the Dais!
    put_prop('wr_ban_ash', 10, 0)
    put_prop('wr_ban_ash', 14, 0)
    put_prop('mn_armour', 10, 3)
    put_prop('mn_armour', 14, 3)
    put_prop('lm_banner_w', 11, 0)
    put_prop('lm_banner_w', 13, 0)

    # 7. NW IRON PRISONER CAGE (`Anja (cage)` on prison-slate floor [6, 3], `Cage` sign [9, 4])!
    #    Bolted iron bars across x=4..8, y=4 & left cage stanchion at (4, 3); (9, 3..5) stays cleanly walkable
    #    (matching HEAD cage layout!) so Anja @ (6, 3) stands visibly inside the bars AND is 100% reachable in BFS!
    put_tile('lm_bollard', 4, 3, 1)
    put_tile('lm_bars_l', 4, 4, 1)
    put_tile('lm_bars_m', 5, 4, 1)
    put_tile('lm_bars_m', 6, 4, 1)
    put_tile('lm_bars_m', 7, 4, 1)
    put_tile('lm_bars_r', 8, 4, 1)

    # 8. FLANKING WAR-ARCHIVE, WEAPON RACKS, ARMOUR, CHESTS & CANDELABRAS (Richly dressed perimeter, zero clutter!)
    # NE Campaign Archive Wing (x=15..20, y=3..5): map bookcases, cartographer globe & candelabra
    put_prop('mn_books2', 16, 2)
    put_prop('mn_books2', 18, 2)
    put_tile('mn_globe', 15, 3, 1)
    put_prop('mn_candelabra', 20, 3)
    # East Wing (x=18..20, y=6..12): Ashkaar banner, console, weapon rack, military trunk & candelabra
    put_prop('wr_ban_ash', 19, 5)
    put_prop('mn_console', 18, 10)
    put_tile('mn_trunk', 18, 11, 1)
    put_prop('wr_rack', 17, 11)
    put_prop('mn_candelabra', 16, 12)
    # West Wing (x=4..6, y=7..12): weapon racks, supply chest, war banner & candelabra
    put_prop('wr_ban_ash', 4, 5)
    put_prop('wr_rack', 4, 9)
    put_prop('wr_rack', 4, 10)
    put_tile('mn_trunk', 5, 11, 1)
    put_prop('mn_candelabra', 7, 12)
    # South Threshold Royal Honour Guard Armor flanking entry corridor
    put_prop('mn_armour', 10, 14)
    put_prop('mn_armour', 13, 14)

    # 9. Wall Sconces, Hanging Grand Chandelier, Warm Firelight Blooms & Dramatic Overhead Sky-Shaft!
    for sx in (5, 8, 15, 19):
        if m.L[2, 1, sx] == 0:
            m.L[2, 1, sx] = P1('mn_sconce')
    # Grand gilded chandelier hanging overhead above the War-Map Table (pri=2!)
    put_prop('mn_chandelier', 10, 6)
    # Warm radial pf_glow over Oath-Brazier, Twin Brazier, Entry Braziers, War Table & Command Dais!
    for gx, gy in ((5, 6), (16, 6), (8, 13), (13, 13), (10, 7), (11, 4)):
        place_glow(m, gx, gy)
    # Overhead atmospheric light shaft spotlighting Dominar Hrothgar & the Empty Stand!
    place_shaft(m, 11, 3)

    # Subtle cliff-foot/wall shadow along north floor edge where free (strictly walkable cells!)
    h_shad = P1('H_shadow')
    for y in range(2, H - 1):
        for x in range(1, W - 1):
            if m.cls[y, x] == '.' and not m.cliff[y, x] and m.cliff[y - 1, x] and m.L[1, y, x] == 0 and m.L[2, y, x] == 0:
                m.L[2, y, x] = h_shad

    # 10. ALL 8 HEAD Events at exact HEAD coordinates (100% verbatim!)
    events_928 = [
        {'type': 'exit', 'at': [11, 16], 'link': 'WAR_TENT'},
        {'type': 'exit', 'at': [12, 16], 'link': 'WAR_TENT'},
        {'type': 'event', 'name': 'Dominar Hrothgar', 'at': [12, 6], 'pages': [{
            'graphic': {'sprite': SPRITE['DOMINAR'], 'dir': 'down'}, 'trigger': 'action',
            'commands': ['Dominar Hrothgar: Speak plainly. The brazier is lit. In this tent a lie is a death sentence, and I have signed eleven.'],
        }]},
        {'type': 'event', 'name': 'Anja (cage)', 'at': [6, 3], 'pages': [
            {'commands': []},
            {'cond': {'switch': 'WAR_SIDE_ASH'}, 'commands': []},
        ]},
        {'type': 'sign', 'name': 'Map table', 'at': [11, 9], 'post': False,
         'text': "The western dunes in sand on a lacquer table: Skaldfast a white stone, the Siege Camp a red one, the Steamline a line of salt. Someone has drawn the bone-carters' banner in the margin. Small."},
        {'type': 'sign', 'name': 'Oath-brazier', 'at': [6, 7], 'post': False,
         'text': 'The oath-brazier. Its flame is white at the heart. In Ashkaar, what is said over it is true, or the speaker is not long for the world.'},
        {'type': 'sign', 'name': 'Empty stand', 'at': [12, 5], 'post': False,
         'text': "A stand of black glass, empty. Something round and heavy sat here. The dust says: recently."},
        {'type': 'sign', 'name': 'Cage', 'at': [9, 4], 'post': False,
         'text': 'An iron cage, the kind they keep hawks in, made larger.'},
    ]

    spec = {
        'id': 928,
        'name': 'Ashkaar Siege Camp - Command Pavilion',
        'parent': 924,
        'biome': 'interior',
        'bgm': 'Route 9',
        'tone': [16, 2, -10, 0],
        'metadata': {'MapPosition': [0, 14, 14]},
        'events': events_928,
    }
    m.events = events_928
    # Write raw/928.npy via RMap.write (resolves virtual IDs, runs passguard.guard, emits YAML!)
    spec['_file'] = '928_command_pavilion.yaml'
    m.write(928, spec, '# Ashkaar Siege Camp - Command Pavilion (928). WRITTEN BY layouts/war_craft.py (Wave 9) - edit that script.\n')


# ================================================================================================
# 6. MAP 929 — THE OBSERVERS' MESA (36x28, ts 56, DESERT — Multi-Tiered Scenic Cliff Overlook!)
# ================================================================================================
def build_929():
    W, H = 36, 28
    r, m = desert(W, H, 929, kit='sdc', seal='wr_sacks',
                  stairs=('E_stairl', 'E_stairm', 'E_stairr'))

    # 1. Truly Asymmetric Multi-Tier Sandstone Mesa (crushes L-R mirror symmetry WELL under 15%!)
    #    - West side: high sheltered bluff (y=2..23) jutting west in SW around (5,20) STARDUST
    #    - East side: stepped-down headland (y=4..21) jutting east around Telegraphist (27,9) & Rare Candy (30,20)
    for y in range(2, H - 3):
        if y < 12:
            w_edge = 5 + int(round(1.6 * math.sin(y / 3.0) + 1.2 * (vnoise(0, y, 9292, 4.0) - 0.5) * 2))
            e_edge = W - 2 - int(round(1.2 * math.sin(y / 3.5) + 1.1 * (vnoise(10, y, 9293, 4.0) - 0.5) * 2))
        else:
            w_edge = 2 + int(round(1.3 * math.cos(y / 3.8) + 1.2 * (vnoise(0, y, 9292, 4.0) - 0.5) * 2))
            e_edge = W - 4 - int(round(1.8 * math.sin(y / 3.4) + 1.3 * (vnoise(10, y, 9293, 4.0) - 0.5) * 2))
        w_edge = max(2, min(8, w_edge))
        e_edge = max(W - 8, min(W - 2, e_edge))
        for x in range(w_edge, e_edge + 1):
            if 15 <= x <= 19 and y >= 21:
                continue
            # Asymmetric north cliff terrace: West half reaches y=2 (cradling The Rim 17,3), East half steps back to y=4!
            if x >= 21 and y < 4:
                continue
            # Asymmetric south cliff step: West half reaches y=23, East half steps up to y=21!
            if x >= 20 and y > 21:
                continue
            m.ht[y, x] = 1
    # Guarantee all mesa events sit comfortably inside the ht=1 plateau!
    for ex, ey in ((14, 9), (21, 12), (27, 9), (17, 3), (9, 13), (30, 20), (5, 20)):
        m.ht[max(2, ey - 2):min(23, ey + 2), max(3, ex - 2):min(W - 3, ex + 3)] = 1
    CK.smooth_ht(m, 1, 2)
    # Re-ensure smooth clean south goat-path notch at x=15..19
    m.ht[21:, 15:20] = 0
    m.ht[18:21, 15:20] = 1

    # Single dramatic asymmetric NW upper-rim sandstone crag (ht=2) (ZERO mirrored twin towers!)
    ridge(r, 3, 10, 2, 7, seed=92911, h=2, rough=0.38)
    CK.smooth_ht(m, 2, 2)
    m.ht[(m.ht == 2) & (np.arange(W)[None, :] > 10)] = 1

    # Broad carved sandstone steps climbing from the Goat-path onto the Mesa
    ylip = max(y for y in range(H) if m.ht[y, 17] == 1)
    CK.stair(r, 16, ylip, w=3, h=1)

    # Organic Asymmetric Survey Trails (sweeping S-curve west past Dial-box -> Quent -> Rim, separate diagonal to Telegraphist & Rare Candy!)
    trail(r, [(17, 27), (17, 21), (14, 17), (12, 13), (15, 9), (17, 4)], w=2.2, only='su')
    trail(r, [(12, 13), (9, 14), (6, 19)], w=1.9, only='su')
    trail(r, [(15, 16), (22, 14), (27, 10)], w=2.0, only='su')
    trail(r, [(22, 14), (26, 18), (30, 20)], w=1.8, only='su')

    r.finish_plan(border=0)

    # 2. ALL 8 HEAD Events pinned at exact HEAD coordinates!
    E = [
        {'type': 'event', 'name': 'Goat-path', 'at': [17, 27], 'fixed': True, 'pages': [{'trigger': 'touch', 'through': True, 'commands': [
            {'se': 'Door exit'}, {'transfer': {'map': 926, 'x': 30, 'y': 45, 'dir': 'down'}}]}]},
        fx(talk('Dr. Quent', (14, 9), 'trainer_SCIENTIST', [
            "Dr. Quent: Don't touch the dials. They are still reading. Everything down there is still reading.",
            "Dr. Quent: A battle? To you. To the Engine it was a calibration. A very good one. Pack the lenses, Tobin."], d='down')),
        fx(talk('Observer Tobin', (21, 12), 'NPC 12', [
            "Observer Tobin: Two Imprints at full draw and a Bleed dome at the meeting point. I've never seen the needle do that.",
            "Observer Tobin: Dr. Quent says we were never here. I've written that down too."], d='left')),
        fx(talk('Telegraphist', (27, 9), 'NPC 18', [
            "Telegraphist: Tap tap tap. Meridian Spire wants it in words of one syllable. 'IT WORKED.' That's three."], d='down')),
        fx({'type': 'sign', 'name': 'The rim', 'at': [17, 3], 'post': False,
            'text': "From the north rim the whole battlefield is spread out below: the white trench-lines, the red camp, the Steamline's steam, and the glass where the beams met, still smoking."}),
        fx({'type': 'sign', 'name': 'Dial-box', 'at': [9, 13], 'post': False,
            'text': "A brass dial-box. Its needle is pinned hard right, past a mark labelled 'THEORETICAL'."}),
        fx(item((30, 20), 'RARECANDY')),
        fx(hidden((5, 20), 'STARDUST', 'HiddenItem (mesa)')),
    ]
    r.add(*E)
    r.seat_events(on='su')

    # 3. Asymmetric Meridian Expedition Camp, North Overlook Tripods, Telegraph Ridge & Supply Yard!
    props_929 = [
        # North Scenic Rim Overlook: survey tripods, signal poles & warm overlook brazier (NO blocky pf_beacon!)
        ('wr_tripod', 13, 3), ('wr_tripod', 19, 3), ('wr_tripod', 24, 5), ('wr_tripod', 29, 6),
        ('pf_sigpole', 11, 3), ('pf_sigpole', 26, 5), ('fw_brazier', 19, 6),
        # Asymmetric Meridian White Expedition Tents (clustered NW-below-crag, NE telegraph ridge, SE quartermaster!)
        ('wr_tent_w', 7, 10), ('wr_tent_w', 23, 6), ('wr_tent_w', 27, 14),
        ('wr_dial', 10, 12), ('wr_dial', 23, 12),
        ('wr_telegraph', 31, 8), ('wr_telegraph', 32, 12), ('wr_telegraph', 31, 17),
        # Asymmetric Camp Hearth & West Packing Depot
        ('wr_firering', 18, 15), ('pf_logbench', 19, 17), ('fw_brazier', 11, 17),
        ('hb_crates4', 5, 14), ('hb_boxes', 7, 17), ('wr_sacks', 4, 17), ('hb_barrel', 10, 19),
        ('sh_crates', 24, 18), ('wr_supply', 26, 18), ('pf_lantern', 14, 19), ('pf_lantern', 21, 18),
        # Asymmetric Gorge Framing & Valley Crags (distinct left vs right valley silhouettes!)
        ('sk_rock_big', 12, 24), ('ak_rock2', 22, 24), ('pf_roadstone', 15, 25),
        ('ak_rock2', 0, 12), ('sk_rock_big', 33, 15), ('gd_spire', 1, 0), ('gd_spire', 29, 1),
        ('nr_col', 12, 7), ('nr_colfall', 25, 21), ('sk_boulder', 28, 25), ('sk_boulder', 5, 25),
        ('gd_shard0', 24, 1), ('gd_shard1', 33, 2), ('cr_blue_c', 7, 0), ('sk_rock_big', 25, 25),
    ]
    for nm, x, y in props_929:
        r.near(nm, x, y, on='su', r=2)

    CK.props(r, ['sk_rock_big', 'sk_boulder', 'sk_pebbles', 'nt_deadtree'], 13, box=(1, 2, W - 1, H - 1), on='su', clump=2, seed=5)

    r.dress(trees=('nt_deadtree',), n_trees=0, copses=0, scatter=0)
    m.cls[m.cls == 'd'] = 'u'
    r.paint()

    # 4. Clean Sand Base + Asymmetric Multi-Layer Mesa Ground (Wind-Scoured Rim, Packed Trails, Deep Valley Rim!)
    sand_base = clean_sand_base(r)

    valley_below = (m.ht == 0) & ~r.road_mask & ~(
        (np.arange(W)[None, :] >= 15) & (np.arange(W)[None, :] <= 19) & (np.arange(H)[:, None] >= 22)
    )
    # Asymmetric battlefield valley below: Isenmar frost-scarred valley to the NW/W, Ashkaar basalt-glass valley to the NE/E!
    val_ash = valley_below & (np.arange(W)[None, :] >= 14)
    val_frost = valley_below & (np.arange(W)[None, :] < 14)
    paint_patch(r, val_ash, 'L_floorpatch', sand_base, smooth=1)
    paint_patch(r, val_frost, 'S_floorpatch', sand_base, smooth=1)

    # Asymmetric wind-scoured pale sandstone flagstones along NE rim & west instrument pad (S_floorpatch)
    rim_stone = (
        blob(W, H, 21.0, 6.5, 10.0, 3.0, 92941, 0.38) |
        blob(W, H, 8.5, 15.0, 4.5, 3.5, 92942, 0.38) |
        blob(W, H, 28.0, 13.5, 4.2, 3.8, 92943, 0.38)
    ) & (m.ht >= 1) & ~r.road_mask
    paint_patch(r, rim_stone, 'S_floorpatch', sand_base, smooth=2)

    # Packed-earth expedition trails & asymmetric campfire yard (E_floorpatch)
    trail_pad = (r.road_mask | blob(W, H, 18.5, 15.5, 3.2, 2.5, 92944, 0.38)) & (m.ht >= 1) | (r.road_mask & (np.arange(H)[:, None] >= 21))
    paint_patch(r, trail_pad, 'E_floorpatch', sand_base, smooth=1)

    paint_cliff_shadows(r, 'E_shadow')
    sand_dress(r, 0.42, seed=929, exclude=valley_below, bones=0.02)
    decal(r, ['wr_ember0', 'wr_ember1'], 0.22, seed=21, cells=[(x, y) for y, x in np.argwhere(val_ash)])
    decal(r, ['wr_frost0', 'wr_frost1'], 0.22, seed=22, cells=[(x, y) for y, x in np.argwhere(val_frost)])
    decal(r, ['wr_rut0', 'wr_rut1', 'wr_bones0'], 0.06, seed=4, exclude=valley_below)

    # Distant battlefield smoke wisps rising from below the north cliff edge!
    for sx in (5, 14, 21, 30):
        place_smoke(m, sx, 0, 'fw_smoke_w')

    add_fire_lighting(m)
    place_shaft(m, 16, 3)   # Dramatic warm light over The Rim scenic overlook!

    CK.scatter_quiet(r, 10)
    h = head(929, "The Observers' Mesa", field='DESERT', bgm='Route 9', biome='desert', tone=[16, 8, 0, 10])
    h['metadata']['MapPosition'] = [0, 13, 16]
    r.write(h, '929_observers_mesa.yaml', "# The Observers' Mesa (929). WRITTEN BY layouts/war_craft.py (Wave 9) - edit that script.\n")


# ================================================================================================
# 7. MAP 930 — THE BONE-CARTERS' CAMP (44x32, ts 56, DESERT — Eerie Desert Scavenger/Burial Bivouac!)
# ================================================================================================
def build_930():
    W, H = 44, 32
    r, m = desert(W, H, 930, kit='sdc', seal='wr_sacks',
                  stairs=('E_stairl', 'E_stairm', 'E_stairr'))

    # 1. Main caravan road W (Glass Dunes) -> E (Dry Tide cairn) + camp loops
    trail(r, [(0, 16.5), (10, 16), (22, 15.5), (32, 17), (43, 16.5)], w=3.2)
    trail(r, [(21, 16), (22, 21)], w=2.2, only='su.')
    trail(r, [(22, 15), (25, 11)], w=2.2, only='su.')
    r.exit('W', 15, 4)
    r.exit('E', 15, 4)

    # 2. Wind-Carved Sandstone Canyon Hollow Framing the Camp (DESTROY the flat empty desert rectangle!)
    #    Four asymmetric sandstone perimeter ridges sheltering the camp alcoves while keeping all events open!
    ridge(r, 0, 11, 0, 5, seed=93001, h=1, rough=0.38)      # NW sandstone shelf (shelters HiddenItem STARDUST (6,5) below!)
    ridge(r, 32, 43, 0, 5, seed=93002, h=1, rough=0.38)     # NE desert bluff
    ridge(r, 0, 10, 26, 31, seed=93003, h=1, rough=0.38)    # SW dune crag
    ridge(r, 31, 39, 27, 31, seed=93004, h=1, rough=0.38)   # SE canyon ridge (shelters FULLRESTORE (40,28) alcove!)

    # Keep roads, exits, and all event positions cleanly off cliffs
    for y in range(H):
        for x in range(W):
            if r.road_mask[max(0, y - 1):y + 4, max(0, x - 1):x + 2].any():
                m.ht[y, x] = 0
            if 4 <= x <= 9 and 4 <= y <= 8:       # HiddenItem (6, 5)
                m.ht[y, x] = 0
            if 38 <= x <= 42 and 26 <= y <= 30:   # FULLRESTORE (40, 28)
                m.ht[y, x] = 0
            if 34 <= x <= 39 and 4 <= y <= 9:     # NE tent alcove
                m.ht[y, x] = 0
    CK.smooth_ht(m, 1, 2)

    # Organic wind-carved dune lee ledges framing the northern & southern slopes
    dunes(r, 4, 930, box=(12, 3, 32, 8), w=(4, 7))
    dunes(r, 4, 931, box=(12, 25, 31, 29), w=(4, 7))

    r.finish_plan(border=1)

    # 3. ALL 10 HEAD Events pinned at exact HEAD IDs (1..10) & coordinates!
    E = [
        make_front(),
        fx(sign((40, 13), 'Road sign', "THE BONE-CARTERS' CAMP. E: the Dry Tide to Duneholt. W: the front. (Bone-carters walk where they like.)")),
        fx(talk('Elder Ossa', (24, 11), 'NPC 28', [
            "Elder Ossa: We carry out the dead the armies leave. Ours by tomb-law, whoever they were.",
            "Elder Ossa: The carts can't reach the glass. If you walk where we can't, bring them home. One tally-stick each. We'll do the rest."])),
        fx(talk('Embalmer', (33, 22), 'NPC 20', ["Embalmer: Salt, resin and a song. The song matters most. Nobody believes that until they hear it."], d='left')),
        fx(talk('Carter', (12, 21), 'NPC 25', ["Carter: Isenmar boy, Ashkaar girl, same cart this morning. The sand doesn't sort them. Neither do we."], d='right')),
        fx(talk('Carter ', (16, 12), 'NPC 03', ["Carter: White banner, white cloth, white bones. Both armies hold fire when they see white. Mostly."])),
        fx({'type': 'sign', 'name': 'Tally-wall', 'at': [28, 9], 'post': False,
            'text': 'The tally-wall: names in charcoal, rows on rows, Isenmar and Ashkaar mixed together in the order they were carried in. The newest row is still wet.'}),
        fx({'type': 'sign', 'name': 'Landing stone', 'at': [21, 21], 'post': False,
            'text': "A flat stone scorched in a ring, where Sigrun's dragon sets down. Somebody has left a waterskin on it, for whoever comes next."}),
        fx(item((40, 28), 'FULLRESTORE')),
        fx(hidden((6, 5), 'STARDUST', 'HiddenItem (dune)')),
    ]
    r.add(*E)
    r.seat_events(on='su')

    # 4. Eerie Bleached Bone & Timber Storytelling Clusters, Memorial Hearth & Embalmers' Sanctuary!
    props_930 = [
        # Central Memorial Sanctuary: White Bone-Banner, Tally-Wall, Whalebone Arch & Vigil Hearth!
        ('wr_ban_bone', 22, 6), ('wr_tally', 27, 6),
        ('pf_whalebone', 20, 7), ('pf_whalebone', 30, 7), ('fw_skull', 24, 7),
        ('fw_brazier', 21, 12), ('wr_firering', 26, 13), ('pf_stonebench', 23, 13),
        ('nr_ruin', 17, 6), ('nr_col', 31, 9), ('pf_lantern', 19, 13), ('pf_lantern', 29, 13),
        # West Gateposts & Burial-Cart Convoy Yard
        ('wr_ban_bone', 4, 12), ('pf_whalebone', 3, 19), ('fw_skull', 7, 13),
        ('wr_bonecart', 11, 18), ('wr_bonecart', 14, 18), ('wr_bonecart', 17, 18),
        ('wr_tent_bone', 7, 22), ('fw_rack', 6, 9), ('wr_sacks', 10, 21), ('pf_logbench', 10, 24),
        ('fw_brazier', 15, 22),
        # East Embalmers' Sanctuary ("Salt, resin and a song" — salt mounds, embalming tubs, curing well!)
        ('wr_tent_bone', 31, 18), ('wr_well', 30, 24), ('hb_tubs', 25, 23),
        ('hb_salt0', 34, 24), ('hb_salt1', 36, 21), ('wr_rack', 29, 20),
        ('wr_tent_w', 35, 6), ('hb_crates4', 34, 10), ('wr_supply', 37, 12), ('wr_sacks', 34, 12),
        ('pf_wagon', 37, 24), ('wr_bonecart', 40, 19),
        # East Dry-Tide Road Cairn & Desert Relics
        ('sk_rock_big', 41, 12), ('pf_roadstone', 41, 18), ('wr_ban_bone', 42, 13),
        ('pf_whalebone', 14, 26), ('fw_skull', 36, 28), ('nr_colfall', 17, 27),
    ]
    for nm, x, y in props_930:
        r.near(nm, x, y, on='su', r=2)

    CK.props(r, ['sk_rock_big', 'sk_boulder', 'sk_pebbles', 'nt_deadtree'], 13, box=(1, 2, W - 1, H - 2), on='su', clump=2, seed=5)

    # Organic boulder/crag perimeter framing on W edge (ZERO repetitive sack-wall!)
    frame_border_crags(r, sides='NSWE', kinds=('sk_rock_big', 'sk_boulder', 'ak_rock2'), seed=9308)
    seal_non_exit_edge(r, 'W', palette=('wr_sandbags', 'wr_sacks', 'wr_stakes'))

    r.dress(trees=('nt_deadtree',), n_trees=0, copses=0, scatter=0)
    m.cls[m.cls == 'd'] = 'u'
    r.paint()

    # 5. Clean Sand Base + Ancient Dried-Sea Shell Pavement (S_floorpatch), Dragon Landing Ring (L_floorpatch) & Caravan Road!
    sand_base = clean_sand_base(r)

    # Sweeping ancient dried-sea pale shell-crust pavement across the heart of the burial camp (S_floorpatch!)
    shell_pave = (
        blob(W, H, 23.0, 16.5, 11.5, 7.2, 93041, 0.36) |
        blob(W, H, 33.0, 21.5, 6.0, 4.2, 93042, 0.38)
    ) & (m.ht == 0)
    paint_patch(r, shell_pave, 'S_floorpatch', sand_base, smooth=2)

    # Packed-earth burial-cart caravan road (E_floorpatch)
    paint_patch(r, r.road_mask, 'E_floorpatch', sand_base, smooth=1)

    # LITERAL VISUAL STORYTELLING: Scorched dark-basalt ring right around Sigrun's Dragon Landing Stone (21, 21)!
    landing_scorch = blob(W, H, 21.0, 21.0, 3.1, 2.4, 93045, 0.25) & (m.ht == 0)
    paint_patch(r, landing_scorch, 'L_floorpatch', sand_base, smooth=1)

    paint_cliff_shadows(r, 'E_shadow')
    sand_dress(r, 0.44, seed=930, exclude=landing_scorch, bones=0.04)
    decal(r, ['wr_ember0', 'wr_ember1'], 0.35, seed=9, cells=[(x, y) for y, x in np.argwhere(landing_scorch)])
    decal(r, ['wr_bones0', 'wr_bones1', 'wr_rut0'], 0.06, seed=4)

    add_fire_lighting(m)
    place_shaft(m, 23, 8)   # Quiet atmospheric light beam over Elder Ossa & the Tally-Wall!

    CK.scatter_quiet(r, 10)
    h = head(930, "The Bone-Carters' Camp", field='DESERT', bgm='Route 9', biome='desert', tone=[14, 8, 0, 6],
             connections=[{'dir': 'W', 'offset': 15, 'to': 926, 'to_offset': 30}])
    h['metadata']['MapPosition'] = [0, 14, 3]
    r.write(h, '930_bone_carters_camp.yaml', "# The Bone-Carters' Camp (930). WRITTEN BY layouts/war_craft.py (Wave 9) - edit that script.\n")


BUILD = {
    920: build_920,
    924: build_924,
    925: build_925,
    926: build_926,
    928: build_928,
    929: build_929,
    930: build_930,
}


if __name__ == '__main__':
    ids = [int(a) for a in sys.argv[1:] if a.isdigit()] or sorted(BUILD)
    for mid in ids:
        BUILD[mid]()
        print('built', mid)
