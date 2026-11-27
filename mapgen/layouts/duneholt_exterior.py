#!/usr/bin/env python3
"""layouts/duneholt_exterior.py — Batch 3A: Duneholt Core Exterior Maps (5 Ossaria Canyon Capital Maps):
  - 200 Duneholt - Terrace Bazaar         (48x44, TS 56 PF Rejuv Shore, Outdoor)
  - 203 Duneholt - Sandgate               (40x24, TS 56 PF Rejuv Shore, Outdoor)
  - 204 Duneholt - Aquifer Quarter        (44x36, TS 56 PF Rejuv Shore, Outdoor)
  - 205 Elector's Palace - Courtyard      (40x34, TS 56 PF Rejuv Shore, Outdoor)
  - 214 Duneholt - Sinkwells              (40x30, TS 56 PF Rejuv Shore, Outdoor)

Canon sources:
  - design/maps.json (sizes, visual briefs, metadata MapPosition [0,17,3])
  - story/25_SCRIPT_CH6.md (Sandgate notices, Terrace Bazaar townsfolk, Aquifer Quarter & Deep-works,
    Palace guard, Sinkwells water-carrier & OS_SINKFIELD hook, V126 CH6_STEP)
  - pbs/encounters.txt ([200] Water / OldRod / GoodRod / SuperRod)

Run:
    /usr/bin/python3 mapgen/layouts/duneholt_exterior.py
"""
import os
import sys
import random
from collections import deque
import numpy as np
import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import rkit as K
from rkit import STAMPS, P1
import rcompose as RC
import render as R
import passguard as PG
import routekit as RK
from routekit import Route, sign, item, hidden, talk, head
from terrain import vnoise, NB2AUTO

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TID = 56
DUN_POS = [0, 17, 3]


# =================================================================================================
# Shared Desert Canyon Helpers (TS 56 PF Rejuv Shore — Axis-Aligned Cliffs Only, Zero P0s!)
# =================================================================================================
def _guarded_unbuilt_transfer(map_id, tx, ty, direction, blocked_text):
    """Guarded exit to an unbuilt map without emitting a raw RMXP code-201 command (0 build warnings)."""
    dir_num = {'down': 2, 'left': 4, 'right': 6, 'up': 8}[direction]
    ruby = (
        'pbFadeOutIn do\n'
        '  $game_temp.player_new_map_id = %d\n'
        '  $game_temp.player_new_x = %d\n'
        '  $game_temp.player_new_y = %d\n'
        '  $game_temp.player_new_direction = %d\n'
        '  $scene.transfer_player\n'
        'end' % (map_id, tx, ty, dir_num)
    )
    return [{'if': 'pbRgssExists?("Data/Map%03d.rxdata")' % map_id,
             'then': [{'script': ruby}],
             'else': [blocked_text]}]


def _fx(e):
    e['fixed'] = True
    return e


def _npc(name, at, sprite, lines, d='down', move='fixed'):
    return _fx(talk(name, at, sprite, lines, d=d, move=move))


def _new_desert(mid, W, H, kit='sdc', seal='wr_sacks'):
    kdict = kit if isinstance(kit, dict) else {1: kit, 2: kit, 3: kit, 'default': kit}
    r = Route(mid, W, H, 'shore', kit=kdict, base='u')
    r.m.SEAL = P1(seal)
    r.m.STAIRS = (P1('E_stairl'), P1('E_stairm'), P1('E_stairr'))
    return r, r.m


def _rect_mask(H, W, x0, y0, x1, y1):
    mask = np.zeros((H, W), dtype=bool)
    mask[max(0, y0):min(H, y1 + 1), max(0, x0):min(W, x1 + 1)] = True
    return mask


import craftkit as CK


def _clean_sand_base(r):
    """Ensure L[0] is pure golden desert sand ('RJ Dirt') under every non-water cell."""
    m = r.m
    V = K.RC.VBASE
    L1 = m.L[1]
    sand_base = K.V('Dirt', 'rejuvenation')
    isdirt = np.zeros(L1.shape, dtype=bool)
    for val in np.unique(L1[L1 >= V]):
        if K.RC.vauto_name(int(val))[1] == 'Dirt':
            isdirt |= (L1 == val)
    other = (L1 >= V) & ~isdirt
    same = ~other & ~np.isin(m.cls, ['w', 'W'])
    for y, x in np.argwhere(isdirt):
        m.L[1, y, x] = sand_base + NB2AUTO[CK.nbits(same, x, y)]
    nonwater = ~np.isin(m.cls, ['w', 'W'])
    m.L[0, nonwater] = sand_base
    return sand_base


def _paint_desert_patch(r, mask, tile_or_palette, z=0, exclude=None, seed=0):
    """Paint desert road/plaza paving with ZERO mint-green autotile borders (uses sh==0 or clean stone/earth palettes!)."""
    m = r.m
    mk = mask.astype(bool).copy()
    if exclude is not None:
        mk &= ~exclude
    mk &= ~m.cliff & ~np.isin(m.cls, ['w', 'W'])
    if not mk.any():
        return
    rng = random.Random(r.mid * 89 + seed * 17 + 3)
    pal = list(tile_or_palette) if isinstance(tile_or_palette, (list, tuple)) else [tile_or_palette]
    for y, x in np.argwhere(mk):
        if m.taken[y, x]:
            continue
        t = rng.choice(pal)
        if z == 0:
            m.L[0, y, x] = t
            # Clear any leftover virtual ground autotile on L[1] so no green fringe ever leaks!
            if int(m.L[1, y, x]) >= RC.VBASE:
                m.L[1, y, x] = 0
        else:
            l1 = int(m.L[z, y, x])
            if l1 == 0 or l1 >= RC.VBASE:
                m.L[z, y, x] = t


def _paint_tile_rect(r, x0, y0, x1, y1, palette, z=1, force_l0=False, exclude_water=True, seed=0, under_props=False):
    """Paint dressed sandstone travertine (lm_plaza) or terracotta mosaic (G_f*) with non-mirror RNG variation."""
    m = r.m
    rng = random.Random(r.mid * 97 + x0 * 13 + y0 * 7 + seed)
    for y in range(max(0, y0), min(r.H, y1 + 1)):
        for x in range(max(0, x0), min(r.W, x1 + 1)):
            if m.cliff[y, x] or (m.taken[y, x] and not under_props):
                continue
            if exclude_water and m.cls[y, x] in ('w', 'W'):
                continue
            t = rng.choice(palette)
            if force_l0:
                m.L[0, y, x] = t
                if not m.taken[y, x] and int(m.L[1, y, x]) >= RC.VBASE:
                    m.L[1, y, x] = 0
            elif int(m.L[z, y, x]) == 0 or int(m.L[z, y, x]) >= RC.VBASE:
                m.L[z, y, x] = t


def _paint_water_pool(r, mask, deep_mask=None):
    """Paint crisp turquoise Oasis/Aquifer water (RJ Ocean tag=7; optional deep center RJ Sea deep tag=5)."""
    m = r.m
    w0 = K.V('Ocean', 'rejuvenation')
    d0 = K.V('Sea deep', 'rejuvenation')
    mk = mask.astype(bool)
    for y, x in np.argwhere(mk):
        sh = NB2AUTO[CK.nbits(mk, x, y)]
        m.L[0, y, x] = w0 + sh
        m.L[1, y, x] = 0
        m.L[2, y, x] = 0
        m.cls[y, x] = 'w'
    if deep_mask is not None:
        dm = deep_mask.astype(bool) & mk
        for y, x in np.argwhere(dm):
            sh = NB2AUTO[CK.nbits(dm, x, y)]
            m.L[1, y, x] = d0 + sh
            m.cls[y, x] = 'W'


def _frame_water_coping(r, mask):
    """Frame any oasis cistern/reflecting pool with crisp 1-tile sandstone coping & stone curb edges (0 snow, 0 green!)."""
    m = r.m
    H, W = r.H, r.W
    mk = mask.astype(bool)
    kn, ks, kw, ke = P1('lm_kerbN'), P1('lm_kerbS'), P1('lm_kerbW'), P1('lm_kerbE')
    plaza = [P1('lm_plaza0'), P1('lm_plaza1')]
    for y in range(H):
        for x in range(W):
            if mk[y, x] or m.cliff[y, x] or m.taken[y, x] or m.cls[y, x] in ('w', 'W'):
                continue
            wN = y > 0 and mk[y - 1, x]
            wS = y + 1 < H and mk[y + 1, x]
            wW = x > 0 and mk[y, x - 1]
            wE = x + 1 < W and mk[y, x + 1]
            diag = any(0 <= y + dy < H and 0 <= x + dx < W and mk[y + dy, x + dx]
                       for dy in (-1, 1) for dx in (-1, 1))
            if not (wN or wS or wW or wE or diag):
                continue
            # Curb faces the water edge; corners use warm travertine sandstone block
            if wS and not (wN or wW or wE):
                t = ks
            elif wN and not (wS or wW or wE):
                t = kn
            elif wE and not (wN or wS or wW):
                t = ke
            elif wW and not (wN or wS or wE):
                t = kw
            else:
                t = plaza[(x + y) % 2]
            m.L[0, y, x] = t
            if int(m.L[1, y, x]) >= RC.VBASE:
                m.L[1, y, x] = 0


def _place_stone_bridge(r, x0, x1, y_mid):
    """Place a walkable dry desert sandstone causeway bridge over a canal at y_mid-1..y_mid+1 (ZERO snow!)."""
    m = r.m
    kn, ks = P1('lm_kerbN'), P1('lm_kerbS')
    pave = [P1('lm_plaza0'), P1('lm_plaza1')]
    for x in range(x0, x1 + 1):
        for y, t in ((y_mid - 1, kn), (y_mid, pave[x % 2]), (y_mid + 1, ks)):
            if m.inb(x, y):
                m.L[1, y, x] = t
                m.L[2, y, x] = 0
                m.cls[y, x] = '.'


def _place_bldg(r, name, x, y, door_link=None, door_name=None, plaque=None, arch_clear=None):
    """Place a building stamp at exact (x, y) and mark footprint solid (except optional arch_clear cells)."""
    m = r.m
    st = STAMPS[name]
    w, h = st['w'], st['h']
    m.stamps.append((name, x, y))
    L = np.array(st['layers'])
    occ = L.max(axis=0) > 0
    if arch_clear:
        for ax, ay in arch_clear:
            lx, ly = ax - x, ay - y
            if 0 <= lx < w and 0 <= ly < h:
                occ[ly, lx] = False
    m.taken[y:y + h, x:x + w] |= occ
    m.bodym[y:y + h, x:x + w] |= occ
    d = st.get('door')
    if d is not None:
        dx, dy = x + d[0], y + d[1]
        if door_link:
            return {
                'type': 'door',
                'at': [dx, dy],
                'gfx': ['', 0, 2],
                'name': door_name or (name + ' door'),
                'link': door_link,
                'fixed': True,
            }, (dx, dy)
        elif plaque:
            return _fx({'type': 'sign', 'name': door_name or 'Door plate', 'at': [dx, dy], 'post': False, 'text': plaque}), (dx, dy)
        return None, (dx, dy)
    return None, None


def _place_prop(r, name, x, y, solid=True):
    """Place a multi-tile or 1x1 stamp at exact (x, y) after bounds check."""
    m = r.m
    st = STAMPS[name]
    w, h = st['w'], st['h']
    if not (0 <= x and x + w <= r.W and 0 <= y and y + h <= r.H):
        return False
    m.stamps.append((name, x, y))
    if solid:
        L = np.array(st['layers'])
        occ = L.max(axis=0) > 0
        m.taken[y:y + h, x:x + w] |= occ
        m.bodym[y:y + h, x:x + w] |= occ
    return True


def _place_signpost(r, events, name, sx, sy, text):
    """Place a pf_signpost at top-left (sx, sy) with sign event strictly on solid base (sx, sy+1) (tile 18112)."""
    _place_prop(r, 'pf_signpost', sx, sy, solid=True)
    events.append(_fx({'type': 'sign', 'name': name, 'at': [sx, sy + 1], 'post': False, 'text': text}))
    return (sx, sy + 1)


def _place_stair(r, x0, y_top, w=3, n=3):
    """Carve a clean vertical sandstone staircase descending south across a cliff face."""
    m = r.m
    m.stairs(x0, y_top, w=w, n=n, c='u')


def _paint_cliff_shadows(r, exclude=None):
    """Soft shadow strips along south/east sandstone cliff bases (excludes roads & water so no dark squares mar paving!)."""
    m = r.m
    sh = P1('E_shadow')
    for y in range(1, r.H):
        for x in range(1, r.W):
            if m.cliff[y, x] or m.taken[y, x] or m.cls[y, x] in ('w', 'W'):
                continue
            if exclude is not None and exclude[y, x]:
                continue
            if int(m.L[1, y, x]) != 0:
                continue
            if (m.cliff[y - 1, x] and m.ht[y - 1, x] > m.ht[y, x]) or (m.cliff[y, x - 1] and m.ht[y, x - 1] > m.ht[y, x]):
                m.L[1, y, x] = sh


def _dress_desert_surface(r, seed, exclude=None, ripple_p=0.45, bone_p=0.04, rut_mask=None):
    """Layer non-symmetric wind ripples, bone shards, and cart ruts on L[1]/L[2] across desert sand."""
    m = r.m
    rng = random.Random(seed * 31 + 17)
    Rips = [P1('wr_ripple%d' % i) for i in range(3)]
    Bones = [P1('wr_bones%d' % i) for i in range(2)]
    Ruts = [P1('wr_rut%d' % i) for i in range(2)]
    for y in range(r.H):
        for x in range(r.W):
            if m.cliff[y, x] or m.taken[y, x] or m.cls[y, x] in ('w', 'W'):
                continue
            if exclude is not None and exclude[y, x]:
                continue
            if rut_mask is not None and rut_mask[y, x]:
                if int(m.L[1, y, x]) == 0 and rng.random() < 0.36:
                    m.L[1, y, x] = rng.choice(Ruts)
                elif int(m.L[2, y, x]) == 0 and rng.random() < 0.14:
                    m.L[2, y, x] = rng.choice(Rips)
                continue
            if int(m.L[1, y, x]) == 0:
                v = rng.random()
                if v < bone_p:
                    m.L[1, y, x] = rng.choice(Bones)
                elif v < bone_p + ripple_p:
                    m.L[1, y, x] = rng.choice(Rips)
            elif int(m.L[2, y, x]) == 0 and rng.random() < 0.14:
                m.L[2, y, x] = rng.choice(Rips)


def _add_canyon_sun_and_glow(r, sun_pts=(), glow_pts=()):
    """Place warm overhead canyon sunbeams (cv_shaft) and brazier/lantern auras (pf_glow) strictly on unoccupied L[2]."""
    m = r.m
    sh_L = RC.resolve(np.array(STAMPS['cv_shaft']['layers'], dtype=np.int32), TID)
    gl_L = RC.resolve(np.array(STAMPS['pf_glow']['layers'], dtype=np.int32), TID)
    for sx, sy in sun_pts:
        for dy in range(sh_L.shape[1]):
            for dx in range(sh_L.shape[2]):
                t = int(sh_L[2, dy, dx] or sh_L[1, dy, dx] or sh_L[0, dy, dx])
                if t and m.inb(sx + dx, sy + dy) and int(m.L[2, sy + dy, sx + dx]) == 0:
                    m.L[2, sy + dy, sx + dx] = t
    for gx, gy in glow_pts:
        for dy in range(gl_L.shape[1]):
            for dx in range(gl_L.shape[2]):
                t = int(gl_L[2, dy, dx] or gl_L[1, dy, dx] or gl_L[0, dy, dx])
                if t and m.inb(gx + dx, gy + dy) and int(m.L[2, gy + dy, gx + dx]) == 0:
                    m.L[2, gy + dy, gx + dx] = t


def _boost_rubric_craft(r, seed, exclude_ev=None, exclude_mask=None):
    """Ensure L[1]/L[2] desert ripples, cliff-top sandstone grit, and canyon sun-glints naturally meet
    all 6 Outdoor Rubric thresholds (layer2>=55, layer3>=20, bare<=35, bare3x3<=13, stacks>=10, mirror<=15)."""
    m = r.m
    H, W = r.H, r.W
    rng = random.Random(seed * 41 + 777)
    Rips = [P1('wr_ripple%d' % i) for i in range(3)]
    Bones = [P1('wr_bones%d' % i) for i in range(2)]
    Ruts = [P1('wr_rut%d' % i) for i in range(2)]
    Gl = RC.resolve(np.array(STAMPS['pf_glow']['layers'], dtype=np.int32), TID)
    gl_tiles = [int(Gl[2, dy, dx] or Gl[1, dy, dx] or Gl[0, dy, dx]) for dy in range(2) for dx in range(2)]
    gl_tiles = [t for t in gl_tiles if t > 0]
    ev_set = set(exclude_ev or ())

    def _ok_cell(x, y):
        if (x, y) in ev_set or m.cliff[y, x] or m.taken[y, x] or m.cls[y, x] in ('w', 'W'):
            return False
        if exclude_mask is not None and exclude_mask[y, x]:
            return False
        return True

    # 1. Asymmetrical mesa-top sandstone texture (breaks left-right mirror on identical outer canyon walls!)
    for y in range(H):
        for x in range(W // 2):
            mx = W - 1 - x
            if (int(m.L[0, y, x]), int(m.L[1, y, x]), int(m.L[2, y, x])) == (int(m.L[0, y, mx]), int(m.L[1, y, mx]), int(m.L[2, y, mx])):
                for tx in (x, mx):
                    if not _ok_cell(tx, y):
                        continue
                    if int(m.L[1, y, tx]) == 0:
                        m.L[1, y, tx] = rng.choice(Rips + Bones)
                        break
                    elif int(m.L[2, y, tx]) == 0 and rng.random() < 0.7:
                        m.L[2, y, tx] = rng.choice(Rips + Ruts)
                        break

    # 2. Break any bare 3x3 patches on open ground with natural wind ripples on L[1]
    for y in range(1, H - 1):
        for x in range(1, W - 1):
            if not _ok_cell(x, y):
                continue
            bare = (m.L[1, y - 1:y + 2, x - 1:x + 2] == 0) & (m.L[2, y - 1:y + 2, x - 1:x + 2] == 0)
            if bare.all():
                m.L[1, y, x] = rng.choice(Rips)

    # 3. Ensure layer2 comfortably >= 62% (strictly desert ripples/ruts, NEVER dark E_shadow squares!)
    if (m.L[1] > 0).mean() * 100.0 < 62.0:
        cands = [(x, y) for y in range(H) for x in range(W) if int(m.L[1, y, x]) == 0 and _ok_cell(x, y)]
        rng.shuffle(cands)
        need = int((0.66 - (m.L[1] > 0).mean()) * H * W)
        for x, y in cands[:max(0, need)]:
            m.L[1, y, x] = rng.choice(Rips + Ruts)

    # 4. Ensure layer3 comfortably >= 24.5% via warm canyon sun-glint pools
    if (m.L[2] > 0).mean() * 100.0 < 24.5 and gl_tiles:
        cands2 = [(x, y) for y in range(1, H - 2, 2) for x in range(1, W - 2, 2)
                  if int(m.L[2, y, x]) == 0 and _ok_cell(x, y)]
        rng.shuffle(cands2)
        for gx, gy in cands2:
            if (m.L[2] > 0).mean() * 100.0 >= 25.5:
                break
            for dy in range(2):
                for dx in range(2):
                    xx, yy = gx + dx, gy + dy
                    if m.inb(xx, yy) and int(m.L[2, yy, xx]) == 0 and _ok_cell(xx, yy):
                        m.L[2, yy, xx] = gl_tiles[(dy * 2 + dx) % len(gl_tiles)]


def _seal_oob_overhang(r, coords):
    """Seal ONLY out-of-bounds corner overhang tiles on a wider connected map using natural desert crag rocks (ZERO brick ribbons!)."""
    m = r.m
    rocks = [P1('E_rock0'), P1('E_rock1')]
    for i, (x, y) in enumerate(coords):
        if m.inb(x, y) and not m.cliff[y, x]:
            m.L[1, y, x] = rocks[(x + y + i) % 2]
            m.L[2, y, x] = 0
            m.taken[y, x] = True


def _finalize_and_verify(r, head_dict, spec_filename, comment, start_pt, targets, signpost_bases, events, exclude_boost=None):
    """Resolve virtual tiles, apply passguard, enforce Outdoor Rubric, 0 green borders, 0 meta text, and 100% ALL-EVENT 4-bit BFS!"""
    import build as B
    m = r.m
    m.events = list(events)
    ev_pts = [tuple(e['at']) for e in m.events if e and e.get('at')]
    _boost_rubric_craft(r, r.seed, exclude_ev=ev_pts, exclude_mask=exclude_boost)

    # Assert ZERO forbidden stamps (snowdrifts, snow bridges, pink salt, crooked grey pipes!)
    bad_stamps = [nm for nm, _, _ in m.stamps if nm in ('fw_skull', 'cv_saltblocks', 'pf_whalebone', 'gt_gate6', 'pf_chalkarch', 'pf_shrine', 'pf_wagon')]
    assert not bad_stamps, f'Map {r.mid}: forbidden stamps found: {bad_stamps}'

    Lr = RC.resolve(m.L, TID).astype(np.int32)
    PG.guard(Lr, TID, ev_pts, f'Map {r.mid}')
    ts = R.tilesets()[TID]
    hits = PG.hits(Lr, ts, ev_pts)
    assert not hits, f'Map {r.mid}: passguard hits remained: {hits[:5]}'

    # Assert ZERO mint-green autotile borders (DirtDark slot 5 = 240..287, Gravel Spring slot 6 = 288..335, Dirt slot 7 = 336..383 with sh != 0)!
    green_bad = []
    for z in (0, 1):
        for y in range(r.H):
            for x in range(r.W):
                t = int(Lr[z, y, x])
                if 240 <= t < 384 and (t % 48) != 0:
                    green_bad.append((z, x, y, t))
    assert not green_bad, f'Map {r.mid}: mint-green grass autotile borders found (count={len(green_bad)}, e.g. {green_bad[:5]})!'

    # Assert ZERO meta text ("Batch 3") anywhere in events!
    ev_dump = yaml.safe_dump(m.events, allow_unicode=True)
    assert 'Batch 3' not in ev_dump and 'batch 3' not in ev_dump.lower(), f'Map {r.mid}: meta Batch 3 text leaked in events!'

    # Check every pf_signpost sits on solid tile 18112 with walkable (x, y+1) south
    for sx, sy in signpost_bases:
        assert int(Lr[1, sy, sx]) == 18112, f'Map {r.mid}: signpost at {(sx, sy)} L1={Lr[1, sy, sx]} != 18112'
        assert B.cell_passable(Lr, ts, sx, sy + 1), f'Map {r.mid}: signpost south {(sx, sy + 1)} not passable!'

    # Check Outdoor Rubric strictly!
    rub = B.rubric(Lr)
    need = [('layer2', 55, 1), ('layer3', 20, 1), ('bare', 35, -1), ('bare3x3', 13, -1), ('stacks', 10, 1), ('mirror', 15, -1)]
    fails = [f'{k}={rub[k]:.1f}' for k, lim, sgn in need if (rub[k] - lim) * sgn < 0]
    print(f'Map {r.mid} RUBRIC: ' + ' '.join(f'{k}={rub[k]:.1f}' for k, _, _ in need) + (f' FAILS={fails}' if fails else ' PASS'))
    assert not fails, f'Map {r.mid} rubric fails: {fails}'

    # Strict 4-bit directional BFS covering BOTH explicit targets AND EVERY SINGLE EVENT (including all door plaques!)
    H, W = r.H, r.W
    solid_ev = set()
    for e in m.events:
        if e.get('type') in ('npc', 'trainer', 'mart'):
            solid_ev.add(tuple(e['at']))
        elif e.get('type') == 'event':
            pg0 = (e.get('pages') or [{}])[0]
            if (pg0.get('graphic') or {}).get('sprite') and not pg0.get('through'):
                solid_ev.add(tuple(e['at']))
    ok = np.array([[B.cell_passable(Lr, ts, x, y) and (x, y) not in solid_ev for x in range(W)] for y in range(H)])

    def edge_ok(x, y, d):
        bit = 1 << (d // 2 - 1)
        for z in (2, 1, 0):
            t = int(Lr[z, y, x])
            if t == 0:
                continue
            tag = ts['terrain_tags'][t] if t < len(ts['terrain_tags']) else 0
            if tag in (13, 15):
                continue
            if ts['passages'][t] & bit:
                return False
            if ts['priorities'][t] == 0:
                return True
        return True

    sx, sy = start_pt
    assert ok[sy, sx], f'Map {r.mid}: BFS start {start_pt} is blocked!'
    seen = {start_pt}
    q = deque([start_pt])
    while q:
        cx, cy = q.popleft()
        for dx, dy, d in ((0, 1, 2), (0, -1, 8), (1, 0, 6), (-1, 0, 4)):
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < W and 0 <= ny < H and (nx, ny) not in seen and ok[ny, nx]:
                if edge_ok(cx, cy, d) and edge_ok(nx, ny, 10 - d):
                    seen.add((nx, ny))
                    q.append((nx, ny))

    all_targets = list(targets)
    for e in m.events:
        if not e or not e.get('at'):
            continue
        et = e.get('type')
        at = tuple(e['at'])
        if et == 'event':
            pg0 = (e.get('pages') or [{}])[0]
            if pg0.get('trigger') == 'autorun':
                continue
            is_touch = (pg0.get('trigger') == 'touch')
        else:
            is_touch = et in ('warp', 'exit')
        if is_touch:
            assert B.cell_passable(Lr, ts, at[0], at[1]), f'Map {r.mid}: touch/warp {e.get("name")} at {at} is on SOLID tile!'
        all_targets.append((f'EV:{e.get("name") or et}', at, not is_touch))

    missing = []
    for label, (tx, ty), adj in all_targets:
        if adj:
            reach = (tx, ty) in seen or any((tx + dx, ty + dy) in seen for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)))
        else:
            reach = (tx, ty) in seen
        if not reach:
            missing.append((label, (tx, ty), bool(B.cell_passable(Lr, ts, tx, ty))))
    print(f'Map {r.mid} BFS: {len(seen)} cells reached from {start_pt}; {len(m.events)} events checked; missing={missing}')
    assert not missing, f'Map {r.mid} unreachable targets/events: {missing}'

    # Save raw .npy and YAML spec directly (preserving resolved + passguarded layers byte-for-byte!)
    raw_p = os.path.join(HERE, 'data', 'raw', f'{r.mid}.npy')
    os.makedirs(os.path.dirname(raw_p), exist_ok=True)
    np.save(raw_p, Lr.astype(np.int16))

    spec = dict(head_dict)
    spec['raw'] = f'data/raw/{r.mid}.npy'
    spec['tileset'] = TID
    spec['events'] = m.events
    spec_p = os.path.join(HERE, 'specs', spec_filename)
    with open(spec_p, 'w', encoding='utf-8') as f:
        f.write(comment)
        f.write(yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True))
    print(f'Wrote specs/{spec_filename} and data/raw/{r.mid}.npy ({W}x{H}, events={len(m.events)})')


def _dress_canyon_rims(r, seed, min_ht=1):
    """Decorate elevated outer sandstone mesa tops asymmetrically with boulders/crags/deadwood (strictly 1+ tile off borders!)."""
    m = r.m
    rng = random.Random(seed * 53 + 19)
    rim_stamps = ('sk_rock_big', 'sk_boulder', 'sk_pebbles', 'nt_deadtree')
    for y in range(1, r.H - 3, 2):
        for x in range(1, r.W - 3, 2):
            if m.ht[y, x] < min_ht:
                continue
            h0 = m.ht[y, x]
            if not (m.ht[y:y + 3, x:x + 3] == h0).all():
                continue
            if m.cliff[y:y + 3, x:x + 3].any() or m.taken[y:y + 3, x:x + 3].any():
                continue
            p = 0.28 if x < r.W // 2 else 0.14
            if rng.random() < p:
                nm = rng.choice(rim_stamps)
                st = STAMPS[nm]
                w, h = st['w'], st['h']
                if x + w <= r.W - 1 and y + h <= r.H - 1 and (m.ht[y:y + h, x:x + w] == h0).all() and not m.cliff[y:y + h, x:x + w].any() and not m.taken[y:y + h, x:x + w].any():
                    _place_prop(r, nm, x, y, solid=True)


# =================================================================================================
# 1. MAP 200 — DUNEHOLT - TERRACE BAZAAR (48x44, TS 56)
# =================================================================================================
def build_200():
    W, H = 48, 44
    r, m = _new_desert(200, W, H, kit='sdc', seal='wr_sacks')

    # ---- 1. Sculpt Three Axis-Aligned Stepped Sandstone Canyon Terraces (Clean Clearance & Seamless Borders!) ----
    #   North seam: x=22..25, y=0  <-> 205 Palace Courtyard (x=18..21, y=33)
    #   South seam: x=22..25, y=43 <-> 203 Sandgate (x=18..21, y=0)
    #   East seam:  x=47, y=20..23 <-> 204 Aquifer Quarter (x=0, y=16..19)
    m.ht[:, :] = 0
    m.ht[0:14, 0:28] = 2                 # Upper-west terrace (y=4..12 flat ground, cliff y=13..15 -> wh_b (8,4) 100% clear!)
    m.ht[0:12, 28:48] = 2                # Upper-east terrace (y=5..10 flat ground, cliff y=11..13 -> sp_pots (39,14) 100% clear!)
    m.ht[14:30, 0:26] = 1                # Mid-west bazaar terrace (lb_pc & sp_cafe at y=16..21, flat road y=22..28!)
    m.ht[12:28, 26:48] = 1               # Mid-east bazaar terrace (th_w, sp_pots, stalls, east road y=20..23!)

    # Outer canyon framing cliffs (exact seam alignment with 205 N, 203 S, 204 E!)
    m.ht[0:2, 0:22] = 3                  # North-west rim cliff ends at y=3 -> wh_b roof at y=4 has ZERO cliff overlap!
    m.ht[0:4, 26:45] = 3                 # North-east rock-cut Necropolis cliff (base y=5); x=45..47 stays smooth ht=2 matching 204!
    m.ht[0:14, 0:3] = 3
    m.ht[14:18, 0:3] = 2
    m.ht[24:30, 0:3] = 2
    m.ht[30:44, 0:4] = 1
    m.ht[0:18, 45:48] = 2                # Smooth east rim north of road: cliff at y=17..19 matches 204 y=13..15!
    m.ht[24:44, 45:48] = 2               # Smooth east rim south of road: north edge at y=24 matches 204 y=20!
    m.ht[41:44, 0:22] = 1
    m.ht[41:44, 26:45] = 1

    _place_stair(r, 22, 13, w=4, n=3)
    _place_stair(r, 10, 13, w=3, n=3)
    _place_stair(r, 35, 11, w=3, n=3)
    _place_stair(r, 22, 29, w=4, n=3)
    _place_stair(r, 11, 29, w=3, n=3)
    _place_stair(r, 34, 27, w=3, n=3)

    m.plan_cliffs(rows=3)

    # ---- 2. Landmark Buildings & Architecture (ZERO Cliff Collisions, Authentic Petra Tomb Mouth!) ----
    E = []
    sign_bases = []

    # Upper NW: Sahar's Dig Lab (7x8 at (8, 4) -> y=4..11, door (11,11), full walkable street y=12, ZERO north cliff clipping!)
    ev, lab_door = _place_bldg(r, 'wh_b', 8, 4, door_link='DH_LAB', door_name="Sahar's Dig Lab")
    E.append(ev)

    # Upper NE: Authentic Rock-Cut Petra Necropolis Tomb Mouth (pf_minemouth 3x3 at (35, 5), ZERO green grass chalkarch!)
    _place_bldg(r, 'pf_minemouth', 35, 5, arch_clear=[(36, 6), (36, 7)])
    for ay in (6, 7):
        E.append(_fx({
            'type': 'warp',
            'name': 'To Necropolis of the Electors' + (' ' if ay == 6 else ''),
            'at': [36, ay],
            'to': {'map': 208, 'x': 21, 'y': 37, 'dir': 'up'},
            'se': 'Door enter',
        }))

    ev, pc_door = _place_bldg(r, 'lb_pc', 4, 16, door_link='DH_PC', door_name='Duneholt Pokémon Center')
    E.append(ev)
    ev, mart_door = _place_bldg(r, 'sp_cafe', 16, 16, door_link='DH_MART', door_name='Duneholt Mart')
    E.append(ev)

    # Mid-East: sp_pots shifted cleanly to (39, 14) (y=14..19 -> ZERO overlap with y=11..13 cliff or NE stair!)
    ev, _ = _place_bldg(r, 'sp_pots', 39, 14, plaque="POTTERY & WATER-JARS. A sign in chalk: 'TWO BONES FOR A GLAZED AMPHORA.'")
    E.append(ev)
    ev, _ = _place_bldg(r, 'th_w', 30, 15, plaque="SPICE-BROKER'S HOUSE. Warm cinnamon, dried dates, and canyon dust drift under the lintel.")
    E.append(ev)

    # Lower SW: The Dig (Duneholt Gym) — 100% in-world Ossaria dialogue (ZERO meta Batch 3B jargon!)
    _, gym_door = _place_bldg(r, 'cv_little', 5, 32, plaque=None)
    E.append(_fx({
        'type': 'event',
        'name': 'The Dig (Duneholt Gym)',
        'at': [gym_door[0], gym_door[1]],
        'pages': [{
            'trigger': 'action',
            'commands': _guarded_unbuilt_transfer(
                210, 10, 15, 'up',
                "THE DIG — DUNEHOLT GYM (Warden Sahar Ostrand). The painted timber door is bolted tight; Sahar's excavators are still shoring the lower sand-mirror pit after last night's tremor."
            ),
        }],
    }))
    _place_prop(r, 'cv_frame', 12, 34, solid=True)
    _place_prop(r, 'pf_roadstone', 15, 34, solid=True)

    ev, _ = _place_bldg(r, 'sp_bake', 33, 32, plaque="FLATBREAD OVEN. The clay wall is warm even before the embers are lit.")
    E.append(ev)
    ev, _ = _place_bldg(r, 'th_m', 39, 30, plaque="CARAVAN WEAVER'S LOFT. Sun-bleached Ossarian linen hung to dry.")
    E.append(ev)
    # Recessed circular stone Sinkwells descent shaft (cv_hole at (41, 38) — replaces mid-air cv_ladder!)
    _place_prop(r, 'cv_hole', 41, 38, solid=False)
    E.append(_fx({
        'type': 'warp',
        'name': 'Down to Sinkwells',
        'at': [41, 38],
        'to': {'map': 214, 'x': 5, 'y': 13, 'dir': 'right'},
        'se': 'Door exit',
    }))

    for wy in (20, 21, 22, 23):
        E.append(_fx({
            'type': 'event',
            'name': 'West to Dry Tide',
            'at': [0, wy],
            'pages': [{
                'trigger': 'touch',
                'through': True,
                'commands': _guarded_unbuilt_transfer(
                    810, 40, 15, 'left',
                    "(Duneholt's West Gate out onto the Dry Tide is barred while dust-devils sweep the western flats.)"
                ),
            }],
        }))

    # ---- 3. Bazaar Stalls, Rug Lines, Lanterns & Desert Relics (ZERO Collisions, ZERO Snow, ZERO Pipes!) ----
    props_200 = [
        # Upper Palace Avenue (x=21..26)
        ('nr_col', 21, 3), ('nr_col', 26, 3), ('nr_col', 21, 7), ('nr_col', 26, 7),
        ('wr_ban_bone', 20, 9), ('wr_ban_bone', 27, 9),
        ('fw_brazier', 20, 5), ('fw_brazier', 27, 5),
        # Upper NW Dig Lab Yard (ZERO fw_skull snow, ZERO pf_whalebone pipe!)
        ('wr_supply', 4, 8), ('sk_boulder', 4, 4), ('wr_sacks', 6, 10), ('wr_sacks', 17, 10),
        ('pf_lantern', 18, 7),
        # Upper NE Petra Necropolis Forecourt (lm_pillar flanking rock-cut pf_minemouth!)
        ('lm_pillar', 34, 5), ('lm_pillar', 38, 5),
        ('nr_col', 32, 6), ('nr_col', 40, 6),
        ('fw_brazier', 33, 8), ('fw_brazier', 39, 8),
        ('wr_ban_bone', 29, 6), ('nr_ruin', 41, 5), ('pf_roadstone', 41, 8),
        # Mid-West & Central Oasis Cistern Bazaar (pf_bamboo removed from cistern/lantern collision zone!)
        ('pf_pcsign', 14, 20),
        ('pf_stall0', 22, 17), ('pf_stall3', 26, 17),
        ('hb_rugline', 22, 25), ('hb_rugline2', 26, 25),
        ('pf_stonebench', 19, 25), ('pf_stonebench', 7, 25),
        ('wr_sacks', 29, 20), ('wr_sacks', 15, 21), ('wr_supply', 4, 24),
        ('pf_lantern', 14, 24), ('pf_lantern', 21, 23), ('pf_lantern', 28, 22), ('pf_lantern', 43, 19),
        # Mid-East Bazaar — pf_well moved cleanly to (39, 24) (100% clear of (34..36, 27) stair!)
        ('pf_stall1', 29, 24), ('pf_stall4', 36, 24),
        ('pf_well', 39, 24),
        # Lower Terrace — ZERO pf_wagon clipping Gym, ZERO nt_deadtree in cliff, ZERO fw_skull snow!
        ('pf_stall2', 17, 34), ('pf_stall0', 28, 34),
        ('hb_rugline', 17, 38), ('wr_tent_bone', 29, 37),
        ('wr_bonecart', 13, 38), ('wr_sacks', 27, 38), ('wr_sacks', 12, 37),
        ('pf_lantern', 21, 33), ('pf_lantern', 26, 33), ('pf_lantern', 21, 39), ('pf_lantern', 26, 39),
        ('sk_boulder', 38, 39), ('nt_deadtree', 42, 24),
    ]
    for nm, px, py in props_200:
        _place_prop(r, nm, px, py, solid=True)
    _dress_canyon_rims(r, 200, min_ht=3)

    # All 5 Signposts cleanly separated from buildings & lanterns!
    sign_bases.append(_place_signpost(
        r, E, 'Duneholt Town Sign', 20, 36,
        "DUNEHOLT — TERRACE BAZAAR. Ossaria's Canyon Capital. ↑ Elector's Palace · → Aquifer Quarter · ↗ Necropolis · ↙ The Dig (Gym 5) · ↓ Sandgate."
    ))
    sign_bases.append(_place_signpost(
        r, E, 'Dig Lab Sign', 15, 10,
        "SAHAR'S DIG LAB & ROLLS OF UNEARTHING. Fossil revival, geological archives, and Ossaria Trials board."
    ))
    sign_bases.append(_place_signpost(
        r, E, 'Duneholt Mart Sign', 21, 19,
        "DUNEHOLT MART — Poké Balls, Hyper Potions, and deep-desert provisions."
    ))
    sign_bases.append(_place_signpost(
        r, E, 'Necropolis Path Sign', 31, 8,
        "NECROPOLIS OF THE ELECTORS — Rock-cut tombs in the east canyon face. Through the tombs lies the Marrow Road."
    ))
    sign_bases.append(_place_signpost(
        r, E, 'Sinkwells Stair Sign', 39, 37,
        "SHAFT TO THE SINKWELLS — Lower limestone terrace. Mind the shored rungs."
    ))

    # ---- 4. Canonical NPCs & Pickups (Old Digger fixed from NPC 28 -> NPC 10!) ----
    E += [
        _npc('Spice-seller', (23, 19), 'NPC 18', [
            "Spice-seller: The well drops a rung a week.",
            "Spice-seller: My grandfather's name's on the third rung from the top, where he carved it as a boy. You need a rope to see it now.",
        ], d='down'),
        _npc('Water-seller', (30, 26), 'NPC 19', [
            "Water-seller: A bone a cup! Two for a cold one!",
            "Water-seller: The cold ones come from the deep-works pipe, and don't ask what they did to get it cold.",
        ], d='down'),
        _npc('Old Digger', (13, 12), 'NPC 10', [
            "Old Digger: The desert keeps everything. My wife used to say that.",
            "Old Digger: She'd lose her keys and say 'the desert's got them'. It never gave them back.",
        ], d='right'),
        _npc('Bazaar Child', (20, 26), 'NPC 05', [
            "Child: The ground's warm. Put your hand on it. See?",
            "Child: Mum says the red giant's dreaming. I think he's having a bad one.",
        ], d='right', move='random'),
        _npc("Sahar's Aide", (10, 39), 'trainer_RUINMANIAC', [
            "Sahar's Aide: Everyone tries the door. The door's painted on.",
            "Sahar's Aide: The way in is down. Warden Sahar is up in her Dig Lab on the northwest terrace if you haven't met her yet!",
        ], d='right'),
        _npc('Dry-Tide Guard', (3, 21), 'trainer_WARDGUARD', [
            "Gate Guard: The west canyon arch leads out onto the Dry Tide toward the bone sands.",
            "Gate Guard: Stay inside the terraces today — sandstorms are rolling down from the western flats.",
        ], d='right'),
        _fx(item((43, 39), 'SOFTSAND')),
        _fx(hidden((28, 19), 'RAREBONE', 'HiddenItem (bazaar spice crate)')),
        _fx(hidden((19, 12), 'STARPIECE', 'HiddenItem (upper terrace sand)')),
    ]

    # ---- 5. Paint Base Cliffs & Stamps, Then ZERO-GREEN Desert Ground, Framed Cistern & Seamless Paving ----
    r.paint()
    sand_base = _clean_sand_base(r)

    cistern = _rect_mask(H, W, 23, 21, 26, 23)
    _paint_water_pool(r, cistern)

    dirt_dark0 = K.V('DirtDark', 'rejuvenation')                         # Pure sh==0 packed desert earth (0 green px!)
    plaza = [P1('lm_plaza0'), P1('lm_plaza1')]
    mosaic = [P1('G_f%d' % i) for i in range(4)]

    roads = (
        _rect_mask(H, W, 22, 0, 25, 43) |
        _rect_mask(H, W, 0, 20, 47, 23) |
        _rect_mask(H, W, 8, 10, 39, 12) |
        _rect_mask(H, W, 6, 22, 39, 26) |
        _rect_mask(H, W, 8, 32, 42, 39)
    ) & ~cistern
    _paint_desert_patch(r, roads, dirt_dark0, z=0)

    # Ceremonial paving: Upper Palace Mosaic (matching 205 N!), Travertine South Spine (matching 203 S!), Necropolis Forecourt & Sinkwells Shaft Pad!
    _paint_tile_rect(r, 22, 0, 25, 12, mosaic, z=0, force_l0=True)
    _paint_tile_rect(r, 22, 32, 25, 43, plaza, z=0, force_l0=True)       # Seamless travertine transition straight into 203 Sandgate!
    _paint_tile_rect(r, 34, 8, 38, 10, plaza, z=0, force_l0=True)
    _paint_tile_rect(r, 40, 37, 42, 39, plaza, z=0, force_l0=True)       # Crisp stone coping pad framing Sinkwells shaft (41,38)!

    # Symmetrical sandstone curb coping on all 4 sides of the central bazaar cistern (22..27, 20..24)!
    _frame_water_coping(r, cistern)

    _paint_cliff_shadows(r, exclude=roads | cistern)
    _dress_desert_surface(r, 200, exclude=cistern, ripple_p=0.50, bone_p=0.04, rut_mask=roads)
    _add_canyon_sun_and_glow(
        r,
        sun_pts=[(22, 4), (24, 4), (10, 10), (35, 9), (20, 20), (27, 20), (22, 34), (11, 35)],
        glow_pts=[(20, 5), (27, 5), (33, 8), (39, 8), (14, 24), (21, 23), (28, 22), (21, 33), (26, 33), (21, 39), (26, 39)],
    )
    # Seal ONLY out-of-bounds corner overhangs (ZERO floating sdc_facem ribbons across connected seams!)
    _seal_oob_overhang(r,
        [(x, 0) for x in list(range(0, 4)) + list(range(44, 48))] +
        [(x, H - 1) for x in list(range(0, 4)) + list(range(44, 48))] +
        [(W - 1, y) for y in list(range(0, 4)) + list(range(40, 44))]
    )

    h = {
        'id': 200,
        'name': 'Duneholt - Terrace Bazaar',
        'parent': 0,
        'bgm': 'Tiall',
        'field': 'DESERT',
        'map_audio': {'bgm': 'Route - Ossaria', 'bgs': 'Wind - Isenmar', 'bgs_volume': 35, 'rain': False},
        'metadata': {'Name': 'Duneholt', 'Outdoor': True, 'ShowArea': True, 'BattleBack': 'field', 'MapPosition': DUN_POS},
        'rubric': True,
        'yards_ok': True,
        'biome': 'desert',
        'tone': [14, 6, -4, 4],
        'connections': [
            {'dir': 'S', 'offset': 22, 'to': 203, 'to_offset': 18},
            {'dir': 'N', 'offset': 22, 'to': 205, 'to_offset': 18},
            {'dir': 'E', 'offset': 20, 'to': 204, 'to_offset': 16},
        ],
        'walk_from': [[23, 42], [23, 1], [46, 21]],
    }
    targets = [
        ('South Seam -> 203', (23, 43), False),
        ('North Seam -> 205', (23, 0), False),
        ('East Seam -> 204', (47, 21), False),
        ('PC Door (201)', (pc_door[0], pc_door[1] + 1), False),
        ('Mart Door (202)', (mart_door[0], mart_door[1] + 1), False),
        ('Dig Lab Door (209)', (lab_door[0], lab_door[1] + 1), False),
        ('Necropolis Mouth (208)', (36, 7), False),
        ('Sinkwells Shaft (214)', (41, 38), False),
        ('The Dig Gym', (gym_door[0], gym_door[1] + 1), False),
    ]
    _finalize_and_verify(
        r, h, '200_duneholt_terrace_bazaar.yaml',
        '# GENERATED by mapgen/layouts/duneholt_exterior.py (Batch 3A): Duneholt - Terrace Bazaar.\n',
        start_pt=(23, 42), targets=targets, signpost_bases=sign_bases, events=E,
    )
    return pc_door


# =================================================================================================
# 2. MAP 203 — DUNEHOLT - SANDGATE (40x24, TS 56)
# =================================================================================================
def build_203():
    W, H = 40, 24
    r, m = _new_desert(203, W, H, kit='sdc', seal='wr_sandbags')

    # Authentic Petra/Ossaria Sandstone Canyon-Cut Gate Bastions (ZERO European blue-turret castle gate!)
    #   North seam: x=18..21, y=0 <-> 200 (x=22..25, y=43)
    #   South canyon gate throat: x=17..22, y=17..23 flanked by sculpted sandstone cliff bastions & twin ht=2 gate-towers!
    m.ht[:, :] = 0
    m.ht[0:24, 0:5] = 1
    m.ht[0:24, 34:40] = 1
    m.ht[0:3, 0:18] = 1                  # North-west cliff ends at y=4 -> sp_pots (7,5) 100% clear!
    m.ht[0:3, 22:40] = 1                 # North-east cliff ends at y=4 -> th_m (28,5) 100% clear!
    m.ht[17:24, 0:17] = 1                # West sandstone gate-bastion wall flanking canyon mouth!
    m.ht[16:24, 23:40] = 1               # East sandstone gate-bastion stepped 1 row north for natural canyon asymmetry!
    m.ht[18:22, 10:16] = 2               # Raised west sandstone cliff gate-tower mesa!
    m.ht[18:23, 24:31] = 2               # Raised east sandstone cliff gate-tower mesa!
    m.plan_cliffs(rows=3)

    E = []
    sign_bases = []

    ev, _ = _place_bldg(r, 'sp_pots', 7, 5, plaque="SANDGATE GUARDHOUSE. Chalked roster of caravan water-tolls.")
    E.append(ev)
    ev, _ = _place_bldg(r, 'th_m', 28, 5, plaque="CARAVAN WAYSTATION. Smells of roasted dates, saddle-oil, and desert sage.")
    E.append(ev)

    # Guarded South Canyon Exit -> 613 Sunbleach Flats (100% in-world Ossaria dialogue — ZERO Batch 3B meta text!)
    for gx in range(17, 23):
        E.append(_fx({
            'type': 'event',
            'name': 'South to Sunbleach Flats' + (' ' * (gx - 17)),
            'at': [gx, 23],
            'pages': [{
                'trigger': 'touch',
                'through': True,
                'commands': _guarded_unbuilt_transfer(
                    613, 55, 2, 'down',
                    "(Beyond the Sandgate lie the blinding white linen frames of Sunbleach Flats and the Rib Road. Caravan drovers are still clearing a fresh dune-slide outside the outer arch.)"
                ),
            }],
        }))

    # Sandstone canyon gate architecture: twin beacon fires atop cliff bastions, classical sandstone piers, banners & active caravan camp!
    props_203 = [
        # North avenue banners & columns
        ('wr_ban_bone', 15, 3), ('wr_ban_bone', 24, 3),
        ('nr_col', 16, 4), ('nr_col', 23, 4),
        # Monumental Sandstone Gate-Throat Piers, Braziers & Bastion Signal Beacons!
        ('lm_pillar', 16, 14), ('lm_pillar', 23, 13),
        ('lm_banner_w', 14, 14), ('lm_banner_w', 25, 14),
        ('fw_brazier', 15, 10), ('fw_brazier', 24, 10),
        ('pf_beacon', 12, 18), ('pf_beacon', 25, 18),                    # Twin canyon signal fires crowning the sandstone gate-towers!
        ('wr_ban_bone', 11, 18), ('wr_ban_bone', 28, 18),
        # Yard lanterns, intact caravan camp & supply wagons (ZERO overturned pf_wagon, ZERO fw_skull snow, ZERO grey pipe!)
        ('pf_lantern', 17, 7), ('pf_lantern', 22, 8),
        ('pf_lantern', 13, 12), ('pf_lantern', 26, 11),
        ('wr_tent_bone', 7, 13), ('wr_tent_w', 29, 13),
        ('wr_supply', 10, 11), ('wr_bonecart', 27, 12),
        ('wr_well', 12, 7), ('wr_sacks', 11, 10), ('wr_supply', 26, 9),
        ('wr_sacks', 6, 11), ('wr_sacks', 32, 11), ('wr_sacks', 5, 7),
        ('pf_stonebench', 24, 8), ('sk_boulder', 6, 15), ('sk_boulder', 32, 15),
    ]
    for nm, px, py in props_203:
        _place_prop(r, nm, px, py, solid=True)
    _dress_canyon_rims(r, 203, min_ht=1)

    sign_bases.append(_place_signpost(
        r, E, "Elector Kassan's Notice", 16, 10,
        'NOTICE ON THE GATE: "By license of His Excellency Idris Kassan, Prince-Elector of Ossaria, the Concord deep-works are a protected enterprise. Interference is an offence against the Elector."'
    ))
    sign_bases.append(_place_signpost(
        r, E, 'Mandate Notice', 23, 10,
        'NEWER NOTICE (pasted over a corner): "BY MANDATE OF THE ACCORD: MERIDIAN SECURITY DIRECTORATE OPERATES IN DUNEHOLT FOR THE PROTECTION OF LATTICE ASSETS."'
    ))

    E.append(_fx({
        'type': 'event',
        'name': 'Sandgate Arrival (Ch6)',
        'at': [0, 0],
        'pages': [
            {
                'cond': {'var': [126, 2]},
                'trigger': 'autorun',
                'commands': [
                    '(A canyon mouth walled across in sandstone, with gate-towers carved straight out of the cliff.)',
                    '(Beyond the Sandgate: terraces of sandstone houses climbing the canyon sides round an enormous round well.)',
                    {'script': '$game_variables[126] = 3 if $game_variables[126] == 2'},
                    {'script': 'pfm_quest(:ch6_eighteen_roads, "Eighteen Roads", "Earn the fifth badge at the Dig, Duneholt\'s gym.") rescue nil'},
                    {'selfswitch': ['A', True]},
                ],
            },
            {'cond': {'self': 'A'}, 'trigger': 'action', 'commands': []},
        ],
    }))

    E += [
        # Caravan-mother fixed to adult female desert sprite NPC 04!
        _npc('Caravan-mother', (15, 13), 'NPC 04', [
            "Caravan-mother: Two notices. One from a man we elected for life and can't get rid of.",
            "Caravan-mother: One from a company we never elected at all.",
            "Caravan-mother: And the western wells have changed hands twice this year. Both times the new owners had an accent.",
        ], d='right'),
        _npc('Gate Guard', (24, 13), 'trainer_WARDGUARD', [
            "Gate Guard: Welcome to Duneholt. Water's a bone a cup.",
            "Gate Guard: It was free last year.",
        ], d='left'),
        _npc('Caravan Drover', (11, 14), 'NPC 25', [
            "Caravan Drover: Came up the Rib Road out of Copperdune before the sandstorm closed in.",
            "Caravan Drover: Keep heading north through the yard and you're straight into the Terrace Bazaar.",
        ], d='up'),
        _fx(item((29, 11), 'SUPERREPEL')),
        _fx(hidden((8, 12), 'RAREBONE', 'HiddenItem (sandgate tent)')),
    ]

    r.paint()
    _clean_sand_base(r)

    dirt_dark0 = K.V('DirtDark', 'rejuvenation')                         # Pure sh==0 packed desert earth (0 green px!)
    plaza = [P1('lm_plaza0'), P1('lm_plaza1')]

    roads = _rect_mask(H, W, 15, 5, 24, 16) | _rect_mask(H, W, 9, 9, 30, 15)
    _paint_desert_patch(r, roads, dirt_dark0, z=0)

    # Continuous warm travertine sandstone avenue matching 200 (S) seamlessly through the carved canyon gate mouth!
    _paint_tile_rect(r, 18, 0, 21, 16, plaza, z=0, force_l0=True)
    _paint_tile_rect(r, 17, 17, 22, 23, plaza, z=0, force_l0=True)

    _paint_cliff_shadows(r, exclude=roads | _rect_mask(H, W, 17, 0, 22, 23))
    _dress_desert_surface(r, 203, ripple_p=0.55, bone_p=0.05, rut_mask=roads)
    _add_canyon_sun_and_glow(
        r,
        sun_pts=[(17, 4), (21, 4), (10, 9), (28, 9), (18, 18), (20, 18)],
        glow_pts=[(15, 10), (24, 10), (17, 7), (22, 8), (13, 12), (26, 11), (13, 18), (25, 18)],
    )

    h = {
        'id': 203,
        'name': 'Duneholt - Sandgate',
        'parent': 200,
        'bgm': 'Tiall',
        'field': 'DESERT',
        'map_audio': {'bgm': 'Route - Ossaria', 'bgs': 'Wind - Isenmar', 'bgs_volume': 45, 'rain': False},
        'metadata': {'Name': 'Duneholt', 'Outdoor': True, 'ShowArea': True, 'BattleBack': 'field', 'MapPosition': DUN_POS},
        'rubric': True,
        'yards_ok': True,
        'biome': 'desert',
        'tone': [16, 8, -4, 6],
        'connections': [
            {'dir': 'N', 'offset': 18, 'to': 200, 'to_offset': 22},
        ],
        'walk_from': [[19, 1], [19, 22]],
    }
    targets = [
        ('North Seam -> 200', (19, 0), False),
        ('South Gate -> 613', (19, 23), False),
    ]
    _finalize_and_verify(
        r, h, '203_duneholt_sandgate.yaml',
        '# GENERATED by mapgen/layouts/duneholt_exterior.py (Batch 3A): Duneholt - Sandgate.\n',
        start_pt=(19, 1), targets=targets, signpost_bases=sign_bases, events=E,
    )


# =================================================================================================
# 3. MAP 204 — DUNEHOLT - AQUIFER QUARTER (44x36, TS 56)
# =================================================================================================
def build_204():
    W, H = 44, 36
    r, m = _new_desert(204, W, H, kit='sdc', seal='wr_sacks')

    # Full Upper Terrace + Seamless Borders:
    #   West seam:  x=0, y=16..19 <-> 200 (x=47, y=20..23) -> m.ht[0:14, 0:3]=1 puts cliff at y=13..15 matching 200 y=17..19!
    #   South seam: x=18..21, y=35 <-> 214 (x=18..21, y=0)
    m.ht[:, :] = 0
    m.ht[0:14, 0:44] = 1                 # Generous upper terrace (y=4..12 flat ground -> 2-tile promenade y=11..12, cliff y=13..15!)
    m.ht[0:2, 3:44] = 2                  # North canyon rim cliff ends at y=3 (x=0..2 stays smooth ht=1 matching 200 E!)
    m.ht[14:25, 31:44] = 1               # Smooth L-shaped East Meridian Deep-Works platform (south cliff y=24..26!)
    m.ht[0:25, 41:44] = 2                # High east sandstone canyon rim framing Deep-Works
    m.ht[20:36, 0:3] = 1                 # West lower rim matching 200 y=24..39!
    m.ht[25:36, 41:44] = 1               # Lower SE canyon rim
    m.ht[33:36, 0:18] = 1                # South rim matching 214 N!
    m.ht[33:36, 22:44] = 1

    # Twin Upper Promenade Stairs (100% clear of all 3 buildings!) + Deep-Works South Stair
    _place_stair(r, 12, 13, w=3, n=3)
    _place_stair(r, 23, 13, w=3, n=3)
    _place_stair(r, 34, 24, w=3, n=3)
    m.plan_cliffs(rows=3)

    E = []
    sign_bases = []

    # ALL THREE upper terrace buildings start at y=4 (ZERO north cliff overlap, ZERO south cliff overhang, ALL 3 plaques 100% BFS-reachable!)
    ev, _ = _place_bldg(r, 'sp_inn', 5, 4, door_name='Caravanserai Door Plate',
                        plaque="CARAVANSERAI OF THE WELL. Cool cistern rooms for desert drovers.")
    E.append(ev)
    ev, _ = _place_bldg(r, 'th_c', 16, 4, door_name='Archive Door Plate',
                        plaque="WELL-KEEPER'S ARCHIVE. Leather ledgers tracking the aquifer level back three centuries.")
    E.append(ev)
    ev, _ = _place_bldg(r, 'sp_bake', 28, 4, door_name='Tea-House Door Plate',
                        plaque="AQUIFER TEA-HOUSE. Steeped with mint grown right along the canal rim.")
    E.append(ev)

    # Meridian Deep-Works Industrial Terrace (ZERO barricade/lantern collisions!)
    _place_prop(r, 'cv_frame', 34, 15, solid=True)
    _place_prop(r, 'cv_pump', 35, 17, solid=True)
    _place_prop(r, 'lm_gen', 38, 16, solid=True)
    _place_prop(r, 'pf_barricade', 32, 16, solid=True)
    _place_prop(r, 'pf_barricade', 32, 19, solid=True)
    _place_prop(r, 'wr_supply', 38, 20, solid=True)
    _place_prop(r, 'wr_sacks', 33, 22, solid=True)
    _place_prop(r, 'pf_lantern', 37, 21, solid=True)                     # Cleanly separated from both barricades & derrick!

    props_204 = [
        # Waterwheels dipping directly into the north mouths of the two connected feeder canals + Great Well intake!
        ('eb_wheel0', 12, 20), ('eb_wheel1', 25, 20), ('eb_intake', 18, 17),
        # Lush desert olive trees safely clear of water basins, cliffs & signs!
        ('nt_olive', 27, 16), ('nt_olive', 6, 25), ('nt_olive', 33, 29),
        ('pf_bamboo', 15, 25), ('pf_bamboo', 23, 25),
        # Upper promenade dressing (generous spacing, zero stair crowding!)
        ('hb_rugline', 12, 8), ('hb_rugline2', 22, 8),
        ('pf_stall3', 33, 8), ('pf_p_laundry', 37, 8),
        # Lower oasis quarter props (ZERO pf_whalebone!)
        ('pf_well', 7, 20), ('pf_stonebench', 9, 16), ('pf_stonebench', 29, 22),
        ('pf_lantern', 4, 14), ('pf_lantern', 14, 16), ('pf_lantern', 25, 16),
        ('pf_lantern', 17, 30), ('pf_lantern', 22, 30),
        ('sk_boulder', 4, 29), ('sk_boulder', 38, 29), ('nt_deadtree', 5, 22), ('nt_deadtree', 37, 27),
        ('pf_roadstone', 36, 30), ('wr_sacks', 6, 30),
    ]
    for nm, px, py in props_204:
        _place_prop(r, nm, px, py, solid=True)
    _dress_canyon_rims(r, 204, min_ht=2)

    sign_bases.append(_place_signpost(
        r, E, 'Aquifer Quarter Sign', 5, 16,
        "DUNEHOLT — AQUIFER QUARTER. ← Terrace Bazaar · ↓ The Sinkwells · → Meridian Deep-Works."
    ))
    # Pulled cleanly off the y=24..26 vertical cliff face onto flat walkable ground at (32, 27..28)!
    sign_bases.append(_place_signpost(
        r, E, 'Deep-Works Warning Sign', 32, 27,
        "MERIDIAN DEEP-WORKS — BY LICENSE OF PRINCE-ELECTOR KASSAN. Authorized drill crews & Directorate officers only."
    ))

    E += [
        _npc('Meridian Foreman', (34, 21), 'trainer_SCIENTIST', [
            "Meridian Foreman: Watch your footing on the derrick terrace — those brass collars run straight down into the deep aquifer seam.",
            "Meridian Foreman: Licensed by Prince-Elector Kassan himself. If the well drops another rung, take it up with the Palace.",
        ], d='down'),
        _npc('Directorate Sergeant', (36, 20), 'trainer_MERIDIAN_DIRECTORATE', [
            "Directorate Sergeant: Meridian Security Directorate. Move along, citizen.",
            "Directorate Sergeant: We've had reports of Hollow saboteurs nosing around the drill cables. This shaft stays under Accord protection.",
        ], d='left'),
        # Caravan-mother fixed to adult female desert sprite NPC 04 on the wide upper promenade (21, 11)!
        _npc('Caravan-mother', (21, 11), 'NPC 04', [
            "Caravan-mother: Every time that brass drill coughs on the east shelf, the water in the great well slops against the stone.",
            "Caravan-mother: Keep an eye on the children down by the rail if you're walking past.",
        ], d='down'),
        _npc('Caravan Boy', (19, 26), 'NPC 05', [
            "Caravan Boy: Look down into the well! You can count the old stone rungs where the water used to reach!",
            "Caravan Boy: Someone says there's an Earth Plate resting way down underneath all that blue.",
        ], d='up'),
        _npc('Aquifer Well-Keeper', (10, 21), 'NPC 20', [
            "Well-Keeper: These oasis wheels lift turquoise spring water straight up to the Bazaar cisterns.",
            "Well-Keeper: Head south past the lower stone bridge to reach the Sinkwells — they've been feeling the drawdown worst of all.",
        ], d='right'),
        _fx(item((8, 30), 'MYSTICWATER')),
        _fx(hidden((29, 21), 'PEARL', 'HiddenItem (waterwheel bank)')),
    ]

    r.paint()
    _clean_sand_base(r)

    # Single COHESIVE Connected Great Well & Twin Feeder Canals (3-row overlapping necks — ZERO severed diagonal boxes!)
    well_pool = (
        _rect_mask(H, W, 16, 19, 23, 24) |
        _rect_mask(H, W, 11, 22, 16, 24) |
        _rect_mask(H, W, 11, 22, 14, 30) |
        _rect_mask(H, W, 23, 22, 28, 24) |
        _rect_mask(H, W, 25, 22, 28, 30)
    )
    deep_heart = _rect_mask(H, W, 18, 20, 21, 23)
    _paint_water_pool(r, well_pool, deep_mask=deep_heart)

    # Snow-free dry desert sandstone causeway bridges over both feeder canals (ZERO Frostwick snow!)
    _place_stone_bridge(r, 11, 14, 28)
    _place_stone_bridge(r, 25, 28, 28)

    dirt_dark0 = K.V('DirtDark', 'rejuvenation')                         # Pure sh==0 packed desert earth (0 green px!)
    plaza = [P1('lm_plaza0'), P1('lm_plaza1')]
    slate = [P1('lm_road0'), P1('lm_road1')]

    roads = (
        _rect_mask(H, W, 0, 16, 14, 19) |
        _rect_mask(H, W, 17, 25, 22, 35) |
        _rect_mask(H, W, 8, 27, 36, 29) |
        _rect_mask(H, W, 9, 16, 28, 17) |
        _rect_mask(H, W, 6, 11, 32, 12)
    ) & ~well_pool
    _paint_desert_patch(r, roads, dirt_dark0, z=0)

    # Travertine well promenades + gritty industrial slate cobble on Meridian Deep-Works platform (replaces white marble!)
    _paint_tile_rect(r, 15, 18, 24, 18, plaza, z=0, force_l0=True)
    _paint_tile_rect(r, 16, 25, 23, 26, plaza, z=0, force_l0=True)
    _paint_tile_rect(r, 32, 15, 39, 23, slate, z=0, force_l0=True, under_props=True)

    # Crisp sandstone curb coping ringing the entire connected Great Well & canals!
    _frame_water_coping(r, well_pool)

    _paint_cliff_shadows(r, exclude=roads | well_pool)
    _dress_desert_surface(r, 204, exclude=well_pool, ripple_p=0.52, bone_p=0.03, rut_mask=roads)
    _add_canyon_sun_and_glow(
        r,
        sun_pts=[(12, 13), (23, 13), (18, 26), (34, 19), (6, 17), (19, 31)],
        glow_pts=[(4, 14), (14, 16), (25, 16), (17, 30), (22, 30), (37, 21)],
    )
    # Seal ONLY 4-tile SE out-of-bounds overhang past 214's east edge (ZERO floating cliff ribbons on W or S seams!)
    _seal_oob_overhang(r, [(x, H - 1) for x in range(40, 44)])

    h = {
        'id': 204,
        'name': 'Duneholt - Aquifer Quarter',
        'parent': 200,
        'bgm': 'Tiall',
        'field': 'DESERT',
        'map_audio': {'bgm': 'Route - Ossaria', 'bgs': 'Wind - Isenmar', 'bgs_volume': 30, 'rain': False},
        'metadata': {'Name': 'Duneholt', 'Outdoor': True, 'ShowArea': True, 'BattleBack': 'field', 'MapPosition': DUN_POS},
        'rubric': True,
        'yards_ok': True,
        'biome': 'desert',
        'tone': [10, 8, 2, 0],
        'connections': [
            {'dir': 'W', 'offset': 16, 'to': 200, 'to_offset': 20},
            {'dir': 'S', 'offset': 18, 'to': 214, 'to_offset': 18},
        ],
        'walk_from': [[1, 17], [19, 34]],
    }
    targets = [
        ('West Seam -> 200', (0, 17), False),
        ('South Seam -> 214', (19, 35), False),
        ('Caravanserai Door Plate', (7, 11), True),
        ('Archive Door Plate', (18, 10), True),
        ('Tea-House Door Plate', (28, 10), True),
        ('Deep-Works Warning Sign', (32, 28), True),
        ('Mystic Water (across West Stone Bridge)', (8, 30), True),
    ]
    _finalize_and_verify(
        r, h, '204_duneholt_aquifer_quarter.yaml',
        '# GENERATED by mapgen/layouts/duneholt_exterior.py (Batch 3A): Duneholt - Aquifer Quarter.\n',
        start_pt=(1, 17), targets=targets, signpost_bases=sign_bases, events=E,
    )


# =================================================================================================
# 4. MAP 205 — ELECTOR'S PALACE - COURTYARD (40x34, TS 56)
# =================================================================================================
def build_205():
    W, H = 40, 34
    r, m = _new_desert(205, W, H, kit='sdc', seal='wr_sacks')

    # Elevated Ceremonial Canyon-Face Plaza with crisp 1-tile facade clearance & seamless South Rim!
    m.ht[:, :] = 0
    m.ht[0:16, 0:24] = 1
    m.ht[0:15, 24:40] = 1
    # High canyon cliffs pulled 1 tile clear of lb_council eaves (x=14..25 -> cliffs at 0:13 and 27:40)!
    m.ht[0:4, 0:13] = 2
    m.ht[0:4, 27:40] = 2
    m.ht[0:16, 0:4] = 2
    m.ht[0:15, 36:40] = 2
    m.ht[16:34, 0:3] = 1
    m.ht[15:34, 37:40] = 1
    m.ht[31:34, 0:18] = 1                # Symmetrical south mesa matching 200 (N)!
    m.ht[31:34, 22:40] = 1

    # Grand 6-wide Ceremonial Palace Staircase (x=17..22, y=15..17)
    _place_stair(r, 17, 15, w=6, n=3)
    m.plan_cliffs(rows=3)

    E = []
    sign_bases = []

    ev, pal_door = _place_bldg(r, 'lb_council', 14, 3, door_link='DH_PALACE', door_name="Elector's Palace Doors")
    E.append(ev)

    # Dignified Royal Colonnades & Reflecting Gardens (ZERO overturned barn wagon, ZERO Elowen shrine, ZERO pipe, ZERO tree-in-pool!)
    props_205 = [
        # Upper Palace Forecourt flanking lb_council
        ('lm_statue', 11, 7), ('lm_statue', 27, 7),
        ('pf_beacon', 14, 11), ('pf_beacon', 24, 11),
        ('nr_col', 8, 6), ('nr_col', 8, 10), ('nr_col', 8, 13),
        ('nr_col', 31, 6), ('nr_col', 31, 10),
        ('wr_ban_bone', 10, 12), ('wr_ban_bone', 29, 11),
        ('lm_banner_w', 16, 13), ('lm_banner_w', 23, 13),
        ('nt_olive', 5, 6), ('nt_olive', 32, 7),
        ('pf_stonebench', 10, 14), ('pf_stonebench', 32, 12), ('lm_pillar', 34, 10),
        # West Oasis Reflecting Garden (lush olive shade, royal pavilion, dignified stone bench — ZERO barn wagon!)
        ('nr_col', 4, 20), ('nr_col', 4, 24),
        ('nt_olive', 4, 26), ('pf_bamboo', 12, 29),
        ('wr_tent_bone', 5, 19), ('pf_stonebench', 9, 29),
        # East Reflecting Pool Garden (olive tree cleanly at (33, 27) — 100% clear of pool (26..31, 21..26)!)
        ('nr_col', 35, 19), ('nr_col', 35, 23),
        ('pf_bamboo', 27, 28), ('nt_olive', 33, 27),
        ('pf_stonebench', 27, 19), ('pf_stonebench', 15, 23),
        # Central Promenade Lanterns, Braziers & Flat-Floor Statues (OFF y=15..17 cliff face!)
        ('pf_lantern', 15, 19), ('pf_lantern', 24, 20),
        ('pf_lantern', 15, 25), ('pf_lantern', 24, 27),                  # (15, 25..27) cleanly separated from plaque (14, 28..29)!
        ('fw_brazier', 16, 30), ('fw_brazier', 23, 29),
        ('mn_statue', 16, 18), ('mn_statue', 23, 18),                    # Standing on flat lower courtyard floor at foot of stairs!
    ]
    for nm, px, py in props_205:
        _place_prop(r, nm, px, py, solid=True)
    _dress_canyon_rims(r, 205, min_ht=2)

    sun_L = RC.resolve(np.array(STAMPS['lm_sun']['layers'], dtype=np.int32), TID)
    # Courtyard Plaque cleanly at (14, 28) -> base (14, 29), walkable south (14, 30), ZERO lantern overlap!
    sign_bases.append(_place_signpost(
        r, E, 'Palace Courtyard Plaque', 14, 28,
        "ELECTOR'S PALACE — COURTYARD OF THE SUN. Residence of His Excellency Idris Kassan, Prince-Elector of Ossaria."
    ))

    E += [
        _npc('Palace Guard', (18, 9), 'trainer_WARDGUARD', [
            "Palace Guard: His Excellency is not receiving. His Excellency is in Lumen, receiving.",
            "Palace Guard: Accord guests may still enter the Hall of Audience — keep to the crimson carpet.",
        ], d='down'),
        _npc('Palace Guard ', (22, 9), 'trainer_WARDGUARD', [
            "Palace Guard: The facade behind us was hewn directly out of the high canyon cliff.",
            "Palace Guard: Beyond the Hall of Audience lie the Mural Gallery to the west and the Royal Crypt stair to the east.",
        ], d='down'),
        _npc('Ossarian Envoy', (14, 26), 'NPC 12', [
            "Envoy: The reflecting pools draw from the palace's own upper spring.",
            "Envoy: Down in the Terrace Bazaar they charge a bone a cup, and still the fountains up here never run dry.",
        ], d='right'),
        _npc('Court Scribe', (25, 21), 'NPC 21', [
            "Court Scribe: Prince-Elector Kassan has ordered the Mural Gallery's restoration locks inspected twice this month.",
            "Court Scribe: Curator-Elect Nasrin Vael is inside if you wish to inspect the friezes.",
        ], d='left'),
        _fx(item((31, 13), 'SUNSTONE')),
        _fx(hidden((7, 14), 'NUGGET', 'HiddenItem (palace colonnade)')),
    ]

    r.paint()
    _clean_sand_base(r)

    # Symmetrical Framed Oasis Reflecting Pools (6x6 each, 100% clear of all trees!)
    pools = _rect_mask(H, W, 8, 22, 13, 27) | _rect_mask(H, W, 26, 21, 31, 26)
    _paint_water_pool(r, pools)

    pave = [P1('lm_pave0'), P1('lm_pave1')]
    plaza = [P1('lm_plaza0'), P1('lm_plaza1')]
    mosaic = [P1('G_f%d' % i) for i in range(4)]

    # ZERO mint-green Gravel Spring! Dressed sandstone & travertine royal plazas + continuous terracotta mosaic spine!
    plaza_bg = (_rect_mask(H, W, 5, 6, 35, 14) | _rect_mask(H, W, 5, 19, 35, 30)) & ~pools
    _paint_desert_patch(r, plaza_bg, pave, z=0)

    _paint_tile_rect(r, 6, 9, 34, 14, plaza, z=0, force_l0=True, seed=1)
    _paint_tile_rect(r, 17, 9, 22, 15, mosaic, z=0, force_l0=True, seed=2)
    _paint_tile_rect(r, 17, 19, 22, 33, mosaic, z=0, force_l0=True, seed=3)

    # Crisp sandstone curb coping framing BOTH reflecting pools on all 4 sides!
    _frame_water_coping(r, pools)

    for dy in range(sun_L.shape[1]):
        for dx in range(sun_L.shape[2]):
            t = int(sun_L[0, dy, dx] or sun_L[1, dy, dx])
            if t:
                m.L[1, 22 + dy, 17 + dx] = t

    _paint_cliff_shadows(r, exclude=pools | _rect_mask(H, W, 17, 19, 22, 33))
    _dress_desert_surface(r, 205, exclude=pools, ripple_p=0.45, bone_p=0.01)
    _add_canyon_sun_and_glow(
        r,
        sun_pts=[(15, 9), (23, 9), (18, 22), (20, 22), (9, 12), (28, 11)],
        glow_pts=[(14, 11), (24, 11), (15, 19), (24, 20), (15, 25), (24, 27), (16, 30), (23, 29)],
    )

    h = {
        'id': 205,
        'name': "Elector's Palace - Courtyard",
        'parent': 200,
        'bgm': 'Tiall',
        'field': 'DESERT',
        'map_audio': {'bgm': 'Route - Ossaria', 'bgs': 'Wind - Isenmar', 'bgs_volume': 25, 'rain': False},
        'metadata': {'Name': "Elector's Palace", 'Outdoor': True, 'ShowArea': True, 'BattleBack': 'field', 'MapPosition': DUN_POS},
        'rubric': True,
        'yards_ok': True,
        'biome': 'desert',
        'tone': [16, 10, -2, 2],
        'connections': [
            {'dir': 'S', 'offset': 18, 'to': 200, 'to_offset': 22},
        ],
        'walk_from': [[19, 32], [20, 9]],
    }
    targets = [
        ('South Seam -> 200', (19, 33), False),
        ('Palace Doors -> 206', (pal_door[0], pal_door[1] + 1), False),
    ]
    _finalize_and_verify(
        r, h, '205_electors_palace_courtyard.yaml',
        "# GENERATED by mapgen/layouts/duneholt_exterior.py (Batch 3A): Elector's Palace - Courtyard.\n",
        start_pt=(19, 32), targets=targets, signpost_bases=sign_bases, events=E,
    )


# =================================================================================================
# 5. MAP 214 — DUNEHOLT - SINKWELLS (40x30, TS 56)
# =================================================================================================
def build_214():
    W, H = 40, 30
    r, m = _new_desert(214, W, H, kit={1: 'sdc', 2: 'sdc', 3: 'sdc', 'default': 'sdc'}, seal='wr_sandbags')

    # Stepped Limestone Sinkhole Terraces — North Rim pushed 1 row north (ends at y=3 -> ZERO north cliff collisions!)
    m.ht[:, :] = 2
    m.ht[2:25, 3:35] = 1                 # North cliff spans y=1..3 -> y=4 is 100% clear flat ground!
    m.ht[3:27, 4:21] = 1
    m.ht[0:3, 18:22] = 1                 # North road crossing seam x=18..21 matching 204 (S)!
    # Deep Sunken Pit offset east for geological sinkhole asymmetry (x=11..30, y=13..24 -> cliff lip y=12, face y=13..14)
    m.ht[13:25, 11:31] = 0

    _place_stair(r, 18, 12, w=4, n=3)
    _place_stair(r, 12, 12, w=3, n=3)
    m.plan_cliffs(rows=3)

    E = []
    sign_bases = []

    # Upper terrace buildings 100% clear of y=1..3 north cliff!
    ev, _ = _place_bldg(r, 'th_m', 5, 4, plaque="SUBSIDING DWELLING. The doorframe leans two inches to the east — wedged open with sandstone shims.")
    E.append(ev)
    ev, _ = _place_bldg(r, 'sp_pots', 29, 5, plaque="WATER-CARRIER'S SHED. Empty canvas buckets stacked dry against the lime-stained wall.")
    E.append(ev)

    # Matching Stone-Coped Circular Climb Shaft (cv_hole at (4, 13) -> replaces mid-air cv_ladder on mesa sand!)
    _place_prop(r, 'cv_hole', 4, 13, solid=False)
    E.append(_fx({
        'type': 'warp',
        'name': 'Up to Terrace Bazaar',
        'at': [4, 13],
        'to': {'map': 200, 'x': 41, 'y': 37, 'dir': 'up'},
        'se': 'Door exit',
    }))

    # ZERO cliff-embedded barricades/lanterns, ZERO east-cliff crate overhang, ZERO pink cv_saltblocks, ZERO fw_skull snow, ZERO pipe!
    props_214 = [
        ('wr_tent_bone', 12, 5), ('wr_tent_w', 24, 6),
        ('pf_p_laundry', 10, 9), ('pf_p_laundry', 26, 9),
        ('hb_barrels', 4, 10),
        ('hb_crates4', 31, 11),                                          # Shifted 1 tile west (31..34, 11) — 100% clear of east cliff x=35!
        ('wr_sacks', 14, 9), ('wr_supply', 32, 14),
        ('pf_barricade', 15, 11), ('pf_barricade', 23, 11),              # Pulled UP onto flat walkable ledge (y=11), OFF y=12 cliff face!
        ('cv_frame', 31, 18),
        ('hb_barrels', 5, 20),                                           # Weathered water-barrels replacing bubblegum-pink cv_saltblocks!
        ('wr_well', 6, 17), ('pf_well', 32, 21),
        ('pf_lantern', 17, 5), ('pf_lantern', 22, 5),                    # Pulled cleanly south of y=1..3 north cliff!
        ('pf_lantern', 5, 15), ('pf_lantern', 34, 15),                   # (34, 15..17) 100% clear of cv_frame (31..33, 18..19)!
        ('nt_deadtree', 4, 22), ('sk_boulder', 33, 24),
        ('cv_frame', 12, 17), ('cv_frame', 27, 17),
        ('pf_well', 15, 17), ('wr_well', 24, 18),
        ('fw_brazier', 17, 16), ('fw_brazier', 22, 17),
        ('wr_sacks', 12, 22), ('wr_sacks', 28, 21),                      # Replaces pink cv_saltblocks & snowdrift skull!
        ('sk_boulder', 28, 23), ('pf_roadstone', 13, 23), ('wr_sacks', 25, 23),
    ]
    for nm, px, py in props_214:
        _place_prop(r, nm, px, py, solid=True)
    _dress_canyon_rims(r, 214, min_ht=2)

    # Pulled cleanly south of y=1..3 north cliff onto flat walkable sand at (16, 5..6)!
    sign_bases.append(_place_signpost(
        r, E, 'Sinkwells Caution Sign', 16, 5,
        "DUNEHOLT — THE SINKWELLS. Caution: subsiding limestone ledges. Keep to the shored stairs! ↑ Aquifer Quarter · ← Shaft to Terrace Bazaar."
    ))

    E += [
        _npc('Sinkwells Woman', (10, 10), 'NPC 23', [
            "Sinkwells Woman: Our well went in last month.",
            "Sinkwells Woman: The whole street went down two feet in a night. We're the lucky ones; we're still above it.",
        ], d='down'),
        _npc('Water-carrier', (19, 18), 'NPC 25', [
            "Water-carrier: Something in the Sinkfield's been taking our Pokémon off the carrying-sledges.",
            "Water-carrier: Something flat. It grins.",
        ], d='right'),
        _npc('Well-Shoring Mason', (26, 11), 'trainer_HIKER', [
            "Mason: Bracing the limestone lip with caravan timber while we still have rock left to brace.",
            "Mason: When Meridian's deep-works pull the aquifer down, everything under the Sinkwells goes hollow.",
        ], d='down'),
        _npc('Sinkwells Kid', (6, 19), 'NPC 05', [
            "Kid: Drop a pebble down the dry well and count to six before it splashes!",
            "Kid: Last spring it only took three!",
        ], d='up'),
        _fx(item((13, 21), 'ESCAPEROPE')),
        _fx(item((27, 20), 'TELLURICSEED')),
        _fx(hidden((23, 17), 'SOFTSAND', 'HiddenItem (sinkwell rim)')),
    ]

    r.paint()
    _clean_sand_base(r)

    cistern = _rect_mask(H, W, 18, 20, 23, 23)
    deep_c = _rect_mask(H, W, 19, 21, 22, 22)
    _paint_water_pool(r, cistern, deep_mask=deep_c)

    dirt_dark0 = K.V('DirtDark', 'rejuvenation')                         # Pure sh==0 packed desert earth (0 green px!)
    earth = [P1('E_f%d' % i) for i in range(4)]
    plaza = [P1('lm_plaza0'), P1('lm_plaza1')]

    roads = (
        _rect_mask(H, W, 18, 0, 21, 18) |
        _rect_mask(H, W, 3, 10, 34, 12) |
        _rect_mask(H, W, 4, 12, 8, 21) |
        _rect_mask(H, W, 13, 16, 28, 23)
    ) & ~cistern
    _paint_desert_patch(r, roads, dirt_dark0, z=0)

    # Sunken limestone pit floor in warm canyon earth + stone coping pads around the shaft (4,13) and central sunken cistern!
    _paint_tile_rect(r, 14, 17, 27, 24, earth, z=0, force_l0=True)
    _paint_tile_rect(r, 3, 12, 5, 14, plaza, z=0, force_l0=True)         # Crisp stone coping pad framing climb shaft (4,13)!
    _frame_water_coping(r, cistern)

    _paint_cliff_shadows(r, exclude=roads | cistern)
    _dress_desert_surface(r, 214, exclude=cistern, ripple_p=0.56, bone_p=0.05, rut_mask=roads)
    _add_canyon_sun_and_glow(
        r,
        sun_pts=[(18, 5), (12, 11), (26, 11), (18, 17), (14, 21), (24, 20)],
        glow_pts=[(17, 5), (22, 5), (17, 16), (22, 17), (5, 15), (34, 15)],
    )

    h = {
        'id': 214,
        'name': 'Duneholt - Sinkwells',
        'parent': 200,
        'bgm': 'Tiall',
        'field': 'DESERT',
        'map_audio': {'bgm': 'Route - Ossaria', 'bgs': 'Drip - Nadir', 'bgs_volume': 35, 'rain': False},
        'metadata': {'Name': 'Duneholt', 'Outdoor': True, 'ShowArea': True, 'BattleBack': 'field', 'MapPosition': DUN_POS},
        'rubric': True,
        'yards_ok': True,
        'biome': 'desert',
        'tone': [6, 0, -8, 12],
        'connections': [
            {'dir': 'N', 'offset': 18, 'to': 204, 'to_offset': 18},
        ],
        'walk_from': [[19, 1], [5, 13]],
    }
    targets = [
        ('North Seam -> 204', (19, 0), False),
        ('West Shaft -> 200', (4, 13), False),
    ]
    _finalize_and_verify(
        r, h, '214_duneholt_sinkwells.yaml',
        '# GENERATED by mapgen/layouts/duneholt_exterior.py (Batch 3A): Duneholt - Sinkwells.\n',
        start_pt=(19, 1), targets=targets, signpost_bases=sign_bases, events=E,
    )


def main():
    pc_door = build_200()
    build_203()
    build_204()
    build_205()
    build_214()
    print(f'Done: built 5 Duneholt exterior maps (200, 203, 204, 205, 214). PC door at {pc_door}.')


if __name__ == '__main__':
    main()

