#!/usr/bin/env python3
"""Saltmere (140 / 146 / 147) on the PF Rejuv sheet (tileset 51 "PF Rejuv Coast").  Map builder 7, 2026-11-19.
Elowen's free port and, after SPINE Rev 14, the second town (Gym 1, Dorian Pell's Playhouse).  Replaces the tileset-33
city-kit version (layouts/saltmere_city.py; its specs are kept as layouts/old_14x_*_city.yaml, the events' source).

  140 The Promenade (upper town, 88x72): the north gate valley between two terraces, the Promenade market round the
      Pageant Hall, the Poke Center and Mart on the square, the overlook above the harbour, the harbour stairs.
  146 The Harbour (88x72): the quay under the bluff, warehouses and the Harbour Office, fish market, salt pans, timber
      piers, a merchant ship, the stone breakwater with the striped light.
  147 Old Town (88x72): the Playhouse rise (the Pell Playhouse, `pf_playhouse`, drawn in rdraw.py) above the players'
      square, costumiers' lanes, old houses on the terraces, the sea wall.

Kept exactly: map sizes, 140's N (x 43-48) and W (y 32-34) connection openings, the touch warps 140 (56-61, 71) <->
146 (42-47, 3) and 140 (87, 42-45) <-> 147 (0, 36-39), every door link (SM_PC, SM_MART, SM_PAGEANT, SM_HOUSE1,
SM_HARBOUR, SM_GYM).  Door CELLS moved (printed at the end; 141's HealingSpot follows the PC door).
Run: python3 -I layouts/saltmere_rj.py && python3 -I build.py --strict"""
import os, sys, math, random, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, yaml
import rkit as K
from rkit import C, STAMPS
from terrain import vnoise
import ferrow_rj as F
HERE = K.HERE
OLD = {}
for fn in ('old_140_saltmere_city.yaml', 'old_146_saltmere_harbour_city.yaml', 'old_147_saltmere_oldtown_city.yaml'):
    for d in yaml.safe_load_all(open(os.path.join(HERE, 'layouts', fn))):
        if d: OLD[d['id']] = d
HOUSES_GL = ['gl_cot', 'gl_flat1', 'gl_flat2', 'gl_shed', 'gl_emblem']
HOUSES_SH = ['sh_cot', 'sh_shop', 'sh_cot', 'gl_flat2']
INFILL = ['sh_cot', 'sh_shop', 'gl_cot', 'gl_flat1', 'gl_flat2', 'gl_shed', 'gl_emblem', 'sh_cot']
TREES = ['tr_oak', 'tr_oak2', 'tr_pink', 'tr_teal', 'tr_oak']


def head(mid, fn, **kw):
    h = {k: v for k, v in OLD[mid].items() if k not in ('map', 'heights', 'stamps', 'tiles', 'tileblocks', 'events', 'palette', 'raw', 'tileset')}
    h.update(kw); h['rubric'] = True; h['yards_ok'] = True; h['_file'] = fn
    return h


def old_events(mid):
    """(warps verbatim, other events keyed by name or by the first words of a sign)"""
    warps, ev = [], {}
    for e in OLD[mid].get('events', []):
        if e.get('type') == 'warp': warps.append(e); continue
        key = e.get('name') or re.sub(r'[^A-Z ]', '', (e.get('text') or '').split('\n')[0].upper()).strip()
        e = dict(e); e.setdefault('name', key); ev[key] = e
    return warps, ev


def seat(m, ev, key, x, y, on='.gds', r=6):
    key = next(k for k in ev if k.startswith(key)); e = ev.pop(key); e['at'] = list(m.snap(x, y, on, r=r)); m.taken[e['at'][1], e['at'][0]] = True
    if e.get('type') == 'sign':
        e['post'] = False; m.tile(C('sh', 4847 - 4448), e['at'][0], e['at'][1], 1)
    return e


def bld(m, nm, x, y, link=None, dname=None):
    try:
        return m.stamp(nm, x, y, link, dname)
    except SystemExit as ex:
        print('  (skip %s at %d,%d: %s)' % (nm, x, y, ex)); return None


def house_row(m, names, x0, x1, y_door, seed, gap=1):
    """houses whose doors stand on row y_door, packed from x0 to x1 (doors 1 row above the lane below them)"""
    rng = random.Random(seed); x = x0; out = []
    while x < x1:
        nm = rng.choice(names); st = STAMPS[nm]; ox, oy = st['door']
        if x + st['w'] > x1 + 1: break
        if m.free(x, y_door - oy, st['w'], st['h'], on='.tTdg') and not m.cliff[y_door - oy:y_door + 1, x:x + st['w']].any():
            d = bld(m, nm, x, y_door - oy)
            if d is not None or nm in STAMPS:
                if m.bfoot[y_door - oy:y_door + 1, x:x + st['w']].any() and (m.cls[y_door, x + ox] == 'B'):
                    out.append((x + ox, y_door)); x += st['w'] + gap + rng.choice((0, 0, 1)); continue
        x += 1
    for dx, dy in out: m.doorpath((dx, dy), depth=5)
    return out


def blockfill(m, names, box, seed, limit=14):
    """pack houses into a block of open land (rows top to bottom, shoulder to shoulder), each with a trodden path
    from its door down to the nearest lane: towns read as built-up streets, not woods with a few houses"""
    rng = random.Random(seed); x0, y0, x1, y1 = box; n = 0
    for y in range(y0, y1):
        x = x0
        while x < x1 and n < limit:
            order = list(names); rng.shuffle(order); placed = False
            for nm in order:
                st = STAMPS[nm]; w, h = st['w'], st['h']
                if x + w > x1 or y + h + 1 > y1 or not m.free(x, y, w, h + 1, on='.tT'): continue
                if m.cliff[y:y + h + 1, x:x + w].any() or m.ht[y:y + h, x:x + w].min() != m.ht[y:y + h, x:x + w].max(): continue
                if hasattr(m, 'bfoot') and m.bfoot[y:y + h + 1, max(0, x - 1):x + w + 1].any(): continue
                sub = m.cls[y:y + h, x:x + w]; sub[sub == 'T'] = '.'
                bld(m, nm, x, y); dd = st['door']; m.doorpath((x + dd[0], y + dd[1]), depth=12, stop='dgsD')
                n += 1; x += w + 1 + rng.choice((0, 1)); placed = True; break
            if not placed: x += 1
    return n


def props(m, items, on='.g'):
    for nm, x, y in items: F.put(m, nm, x, y, on=on, r=2)


def lamps(m, pts):
    for x, y in pts:
        if m.free(x, y - 1, 1, 2, on='.gs') and not m.cliff[y - 1:y + 1, x].any(): m.stamp('gl_lamp', x, y - 1)


def ship_at(m, x0, y0):
    """the moored ship art (rcustom `_ship_moored`), moved so its bounding box starts at (x0, y0)"""
    xs = [t[0] for t in K.SHIP]; ys = [t[1] for t in K.SHIP]
    F.ship(m, x0 - min(xs), y0 - min(ys))


def finish(m, mid, h, comment, scatter=9):
    m.beds(); m.greenfill(3)
    m.paint()
    m.scatter(scatter, seed=mid, on='.T')
    m.write(mid, h, comment)


# ====================================================================================================== 140
def build_140(prev=None):
    W, H = 88, 72
    m = K.RMap(W, H, 51, 140, water='Ocean', kit={1: 'ak', 2: 'sh'}); m.keep_under = 'gds'
    def lip(x):                                         # the bluff above the harbour (h=1 above it)
        if x < 22: return 50 + int(round(6 * math.sin(x / 7.0)))
        return 61 + int(round(1.2 * math.sin(x / 5.0) + 1.2 * (vnoise(x, 0, 41, 5.0) - 0.5))) if not 50 <= x <= 67 else 61
    for x in range(W):
        for y in range(H):
            if y <= lip(x): m.ht[y, x] = 1
            elif x < 22 + int(round(4 * math.sin(y / 3.0) + 3 * (vnoise(0, y, 43, 4.0) - 0.5))) and y > lip(x) + 5: m.cls[y, x] = 'w'
            else: m.cls[y, x] = 's'
            nw = x <= 38 and y <= 15 + int(2 * math.sin(x / 6.0))     # the Lanterns terrace (NW) and the Gardens (NE)
            ne = x >= 54 and y <= 13 + int(2 * math.cos(x / 7.0))
            if nw or ne: m.ht[y, x] = 2
    m.cls[(m.cls == 'w') & (np.arange(H)[:, None] > 66)] = 'W'
    for y in range(H):
        for x in range(W):
            if m.ht[y, x] >= 1 and (x < 2 + 2 * vnoise(0, y, 3, 4.0) and not 30 <= y <= 36 or x > 85 - 2 * vnoise(0, y, 4, 4.0) and not 40 <= y <= 47
                                     or y < 2 + 2 * vnoise(x, 0, 5, 4.0) and not 41 <= x <= 50):
                m.cls[y, x] = 'T'
    m.stairs(56, 61, w=6, kit_rows=3)                                  # the harbour stairs (lip row 61)
    m.stairs(20, 15, w=3, kit_rows=4); m.stairs(64, 13, w=3, kit_rows=4)
    m.plan_cliffs()
    G = dict(c='g', only='.tTs')
    m.rect(43, 0, 6, 6, 'g', only='.tT')                                # the north gate road (541 x 12-17)
    m.lane([(45.5, 5), (45, 12), (44.2, 18), (44.5, 23)], w=5.0, seed=11, wobble=0.3, **G)
    m.rect(0, 32, 6, 3, 'g', only='.tT')                                # the causeway road (560 y 12-14)
    m.lane([(4, 33), (12, 33.4), (20, 34.6), (28, 36)], w=3.2, seed=12, wobble=0.3, **G)
    m.blob(44, 38, 15.5, 7.5, 'g', seed=13, rough=0.3, only='.tT')       # the Promenade
    m.lane([(58, 43), (66, 43.4), (76, 43.6), (87, 43.5)], w=4.2, seed=14, wobble=0.3, **G)   # to the Players' Gate
    m.rect(82, 42, 6, 4, 'g', only='.tT')
    m.lane([(50, 45), (54, 50), (58.5, 55), (58.5, 60)], w=5.0, seed=15, wobble=0.3, **G)      # down to the stairs
    m.rect(56, 57, 6, 4, 'g', only='.tTs')
    m.rect(56, 64, 6, 8, 'g', only='s')                                 # the landing to the harbour (warps x 56-61)
    m.lane([(21.5, 19), (24, 24), (28.5, 27.5), (32, 31)], c='d', w=2.4, seed=16, wobble=0.3, only='.tT')   # Lanterns stair lane
    m.lane([(3, 13), (10, 12.6), (20, 13), (30, 12.4), (36, 12.8)], c='d', w=2.2, seed=17, wobble=0.3, only='.tT')    # terrace walk
    m.rect(20, 13, 3, 2, 'd', only='.tT')
    m.lane([(65.5, 17), (63, 22), (58, 27), (56, 31)], c='d', w=2.4, seed=18, wobble=0.3, only='.tT')
    m.lane([(56, 9), (66, 10.4), (76, 10), (84, 10.6)], c='d', w=2.2, seed=19, wobble=0.3, only='.tT')
    m.rect(64, 11, 3, 2, 'd', only='.tT')
    m.lane([(30, 45), (24, 50), (18, 52), (10, 51)], c='d', w=2.3, seed=20, wobble=0.3, only='.tT')       # the cove lane
    m.lane([(66, 48), (74, 52.5), (82, 53), (84, 57)], c='d', w=2.3, seed=21, wobble=0.3, only='.tT')
    m.lane([(36, 47), (40, 53), (44, 57)], c='d', w=2.2, seed=22, wobble=0.3, only='.tT')
    for c in 'gd': m.smooth(c, into='.', passes=2, only='.tT')
    m.blob(40.5, 37.5, 4.2, 2.4, '.', seed=23, rough=0.2, only='g')    # the Promenade green (J1 stands beside it)
    d = {}
    d['pageant'] = bld(m, 'sh_big', 38, 18, 'SM_PAGEANT', 'Pageant Hall door')
    d['pc'] = bld(m, 'gl_pc', 18, 22, 'SM_PC', 'Poke Center door')
    d['mart'] = bld(m, 'gl_mart', 56, 26, 'SM_MART', 'Mart door')
    d['house1'] = bld(m, 'sh_ell', 23, 1, 'SM_HOUSE1', 'House door')
    for k in list(d):
        if d[k] is None: raise SystemExit('saltmere 140: no room for %s' % k)
    for v in d.values(): m.doorpath(v, depth=6)
    hd = []
    hd += house_row(m, HOUSES_GL, 3, 18, 11, 1)                         # the Lanterns terrace
    hd += house_row(m, HOUSES_GL, 27, 37, 11, 2)
    hd += house_row(m, HOUSES_SH + ['gl_emblem'], 55, 85, 8, 3)          # the Gardens
    hd += house_row(m, HOUSES_SH, 61, 84, 41, 4)                        # the Players' Road
    hd += house_row(m, HOUSES_SH, 64, 80, 51, 5)
    hd += house_row(m, HOUSES_GL + ['sh_cot'], 3, 17, 31, 6)            # the causeway end
    hd += house_row(m, HOUSES_SH, 26, 50, 51, 7)                        # above the overlook
    hd += house_row(m, HOUSES_GL, 3, 20, 48, 8)
    warps, ev = old_events(140)
    E = list(warps)
    E.append(seat(m, ev, 'SALTMERE', 49, 6))
    E.append(seat(m, ev, 'Juno J1', 37, 37, 'g'))
    E.append(seat(m, ev, 'Busker', 33, 40, 'g'))
    E.append(seat(m, ev, 'Caramel seller', 47, 41, 'g'))
    E.append(seat(m, ev, 'Royal notice', 50, 31, 'g'))
    E.append(seat(m, ev, 'Kestrel', 52, 32, 'g'))
    E.append(seat(m, ev, 'Eevee breeder', 46, 58, '.gd'))
    E.append(seat(m, ev, 'HARBOUR STAIRS', 55, 59, '.g'))
    E.append(seat(m, ev, 'PLAYERS GATE', 82, 46, '.g'))
    if ev: raise SystemExit('saltmere 140: events not seated %s' % list(ev))
    m.events += E
    for e in warps: m.taken[e['at'][1], e['at'][0]] = True
    for x, y in K.incoming(140): m.taken[y, x] = True
    # ---- the market: tables under awnings round the green, fish and rug lines, crates; the overlook rail
    props(m, (('hb_tables', 31, 33), ('hb_tables', 49, 34), ('hb_fishstall', 52, 38), ('hb_rugline', 33, 43), ('hb_dyeline', 41, 43),
              ('hb_tables', 46, 44), ('hb_boxes', 30, 37), ('hb_barrel', 55, 36), ('hb_cask', 36, 44), ('sh_crates', 56, 40),
              ('hb_keg', 29, 40), ('gl_tables', 54, 42), ('pf_logbench', 38, 40), ('pf_logbench', 42, 35), ('hb_banner', 37, 31),
              ('hb_banner', 49, 31), ('hb_boxes2', 25, 37), ('hb_crates4', 59, 33), ('hb_tables', 36, 33), ('hb_fishstall', 27, 41),
              ('hb_tables', 51, 41), ('hb_rugline2', 45, 32), ('hb_fish', 34, 38), ('hb_barrels', 58, 39), ('gl_tables', 31, 44)), on='g')
    for x, y in ((31, 32), (49, 33)):
        st = STAMPS['pf_p_awning']
        if all(not m.taken[y, x + i] for i in range(3)): m.over += [(2, x + i, y, max(st['layers'][z][0][i] for z in range(3))) for i in range(3)]
    m.fence(24, 49, 60); m.fence(64, 80, 60)
    props(m, (('hb_washline', 8, 44), ('hb_rugline2', 70, 47), ('hb_cask', 62, 36), ('hb_shed', 13, 26), ('hb_washline', 76, 13),
              ('pf_logbench', 30, 58), ('pf_logbench', 40, 58), ('pf_logbench', 70, 58), ('hb_barrel2', 66, 30), ('hb_keg', 28, 19)))
    props(m, (('hb_boat2', 4, 58), ('hb_boat4', 12, 62), ('hb_tubs', 30, 64), ('hb_fish', 40, 66), ('sh_crates', 47, 64), ('hb_barrels', 66, 66),
              ('pf_p_net', 72, 64), ('hb_crates4', 76, 67), ('ak_rock2', 82, 63)), on='s')
    lamps(m, ((42, 6), (50, 6), (42, 17), (49, 17), (30, 33), (58, 35), (40, 47), (52, 47), (60, 45), (70, 45), (80, 45), (55, 56),
              (62, 56), (12, 35), (22, 35), (20, 10), (66, 7), (55, 63), (62, 63), (26, 47), (70, 55)))
    m.trees(30, 3, 2, TREES, r=3, seed=1); m.trees(78, 3, 2, TREES, r=3, seed=2)
    print('  140 blocks', [blockfill(m, INFILL, b, 140 + i) for i, b in enumerate(((62, 14, 86, 39), (2, 36, 20, 47), (26, 18, 38, 32), (66, 46, 86, 60), (2, 18, 16, 30)))])
    print('  140 yard trees', m.autotrees(40, TREES, seed=140, gap=0, box=(0, 0, W, 60)))
    h = head(140, '140_saltmere.yaml', biome='village', tone=[8, 4, -12, 0],
             fog={'name': 'prismfall_seamist', 'opacity': 30, 'blend': 0, 'zoom': 100, 'sx': 2, 'sy': 0})
    finish(m, 140, h, "# Saltmere - The Promenade (140). WRITTEN BY layouts/saltmere_rj.py (PF Rejuv) - edit that script.\n")
    if prev: m.preview(prev, 0.5)
    return d


# ====================================================================================================== 146
def build_146(prev=None):
    W, H = 88, 72
    m = K.RMap(W, H, 51, 146, water='Ocean', kit={1: 'ak', 2: 'sh'}); m.keep_under = 'gds'
    def shore(x):                                         # the quay edge; water south of it
        return 41 + int(round(1.5 * math.sin(x / 8.0))) if x < 70 else 43
    for x in range(W):
        for y in range(H):
            if y <= 0: m.ht[y, x] = 1                       # the foot of the bluff (140 above)
            m.cls[y, x] = '.' if y < shore(x) - 5 else 'g' if y < shore(x) else 'w'
    # the breakwater: a stone arm from the east shore sweeping west along the bottom, the light at its tip
    for x in range(30, 88):
        yb = 58 + int(round(1.5 * math.sin((x - 30) / 14.0)))
        for y in range(yb, yb + 4): m.cls[y, x] = 'g'
    for y in range(42, 62): m.rect(82, y, 6, 1, 'g')
    for y in range(58, 72):                                              # open sea beyond the breakwater: swell patches, not a band
        for x in range(W):
            if (x < 30 or y > 62) and m.cls[y, x] in 'w.g' and not (x >= 30 and m.cls[y, x] == 'g'):
                m.cls[y, x] = 'W' if vnoise(x, y, 61, 5.0) > 0.42 or y > 68 else 'w'
    m.stairs(42, 0, w=6, kit_rows=3)
    m.plan_cliffs()
    m.lane([(44.5, 6), (44, 12), (42, 18), (36, 24), (24, 26), (10, 25)], w=3.4, seed=31, wobble=0.3, c='g', only='.')
    m.lane([(44, 12), (54, 15), (66, 16), (80, 20), (84, 30)], w=3.4, seed=32, wobble=0.3, c='g', only='.')
    m.rect(42, 3, 6, 6, 'g', only='.')

    # the salt pans (NW): shallow brine squares between raked walkways
    m.rect(2, 4, 30, 17, 'd')
    for py in (6, 11, 16):
        for px in (4, 11, 18, 25):
            m.rect(px, py, 5, 3, 'w')
    # piers into the basin
    piers = [(16, shore(17) - 1, 52), (40, shore(41) - 1, 55), (62, shore(63) - 1, 52)]
    for x, y0, y1 in piers:
        for y in range(y0, y1):
            for i in range(3): m.cls[y, x + i] = 'D'
    d = {}
    d['office'] = bld(m, 'gl_hall', 47, 15, 'SM_HARBOUR', 'Harbour Office door')
    if d['office'] is None: raise SystemExit('saltmere 146: no room for the office')
    m.doorpath(d['office'], depth=5, stop='dgsD')
    for nm, x, y in (('gl_emblem', 59, 7), ('gl_flat2', 68, 7), ('gl_shed', 77, 9), ('sh_shop', 3, 22) if False else ('gl_flat1', 34, 3),
                     ('gl_shed', 62, 21), ('gl_flat2', 70, 21), ('gl_cot', 26, 14) if False else ('gl_ell', 29, 13), ('gl_shed', 79, 22),
                     ('gl_flat1', 6, 22), ('gl_shed', 14, 22)):
        dd = bld(m, nm, x, y)
        if dd: m.doorpath(dd, depth=4, stop='dgsD')
    warps, ev = old_events(146)
    E = list(warps)
    E.append(seat(m, ev, 'SALTMERE HARBOUR OFFICE', d['office'][0] + 2, d['office'][1] + 1, '.gd'))
    E.append(seat(m, ev, 'Stevedore', 30, 37, 'g'))
    E.append(seat(m, ev, 'Salt raker', 9, 10, 'd'))
    E.append(seat(m, ev, 'Old angler', 41, 54, 'w' if False else 'D'))
    E.append(seat(m, ev, 'THE BREAKWATER', 70, 59, 'g'))
    if ev: raise SystemExit('saltmere 146: events not seated %s' % list(ev))
    m.events += E
    for e in warps: m.taken[e['at'][1], e['at'][0]] = True
    for x, y in K.incoming(146): m.taken[y, x] = True
    for x, y in ((7, 35), (12, 34), (72, 35)):                           # awnings over the quay stalls
        if all(not m.taken[y, x + i] for i in range(3)): m.over += [(2, x + i, y, max(STAMPS['pf_p_awning']['layers'][z][0][i] for z in range(3))) for i in range(3)]
    m.stamp('lighthouse', 30, 45)                                        # the striped light at the breakwater's tip
    for x in range(6, 82, 5):                                            # bollards along the quay edge
        y = shore(x) - 1
        if m.cls[y, x] == 'g' and not m.taken[y - 1:y + 1, x].any() and not any(px <= x <= px + 2 for px, _, _ in piers): m.stamp('hb_post1' if x % 2 else 'hb_post2', x, y - 1)
    props(m, (('hb_fishstall', 20, 27), ('hb_tables', 26, 24), ('hb_fish', 34, 31), ('hb_tubs', 9, 30), ('sh_crates', 46, 30),
              ('hb_crates4', 50, 31), ('hb_barrels', 56, 30), ('hb_boxes', 58, 31), ('pf_p_net', 66, 30), ('hb_cask', 70, 31),
              ('hb_boxes2', 74, 30), ('hb_barrel', 77, 31), ('sh_crates', 37, 26), ('hb_keg', 31, 26), ('hb_washline', 22, 3),
              ('hb_rugline', 56, 3), ('hb_shed', 74, 14), ('hb_boxes', 52, 23), ('pf_p_net', 2, 29), ('hb_barrel2', 41, 22),
              ('hb_crates4', 66, 12), ('hb_cask', 84, 40), ('hb_barrels', 84, 50), ('hb_boxes', 52, 63), ('hb_keg', 60, 64)), on='gs')
    props(m, (('hb_fishstall', 8, 37), ('hb_tables', 13, 36), ('hb_fish', 21, 38), ('hb_tubs', 26, 36), ('sh_crates', 30, 36),
              ('hb_crates4', 34, 38), ('hb_barrels', 37, 36), ('pf_p_net', 45, 37), ('hb_boxes', 49, 38), ('sh_crates', 53, 36),
              ('hb_crates4', 57, 38), ('hb_cask', 66, 37), ('hb_boxes2', 70, 38), ('hb_fishstall', 73, 36), ('hb_barrel', 79, 37),
              ('pf_p_net', 84, 44), ('hb_boxes', 84, 52), ('hb_keg', 44, 59), ('sh_crates', 60, 58), ('hb_barrels', 74, 58)), on='g')
    lamps(m, ((40, 8), (49, 8), (20, 31), (30, 31), (40, 31), (50, 31), (60, 31), (70, 31), (80, 31), (36, 63), (48, 64), (60, 64),
              (72, 63), (84, 45), (84, 58), (12, 27), (60, 17), (4, 37), (18, 37), (42, 37), (64, 38), (76, 38), (40, 58), (56, 58), (68, 58), (78, 58), (10, 38), (26, 38), (34, 37), (50, 37), (58, 37), (70, 37), (84, 41), (84, 50), (46, 58), (62, 59), (74, 59)))
    print('  146 blocks', [blockfill(m, INFILL, b, 146 + i) for i, b in enumerate(((34, 2, 42, 14), (56, 2, 86, 14), (2, 20, 36, 35), (60, 18, 86, 35), (40, 28, 60, 35)))])
    print('  146 yard trees', m.autotrees(60, TREES, seed=146, gap=0, box=(0, 0, W, 34)))
    h = head(146, '146_saltmere_harbour.yaml', biome='harbour')
    m.beds(); m.greenfill(3)
    m.paint()
    for x0, y0, y1 in piers:                                             # pier planks over the water
        for y in range(y0, y1):
            for i in range(3): m.L[1, y, x0 + i] = C('ak', 1524 + i)
    ship_at(m, 46, 44)
    import reskin as RS; RS.sea_rocks(m, 146) if False else None
    rng_ = random.Random(146)
    rocks = [[[C('ak', 1644), C('ak', 1645)], [C('ak', 1652), C('ak', 1653)]], [[C('ak', 1646), C('ak', 1647)], [C('ak', 1654), C('ak', 1655)]]]
    for _ in range(22):                                                  # rocks off the breakwater, outside the basin
        x, y = rng_.randrange(0, 86), rng_.randrange(62, 70)
        if (m.cls[y:y + 2, x:x + 2] == 'W').all() and (m.L[2, y:y + 2, x:x + 2] == 0).all():
            r = rng_.choice(rocks)
            for j in range(2):
                for i in range(2): m.L[2, y + j, x + i] = r[j][i]
    for nm, x, y in (('hb_boat1', 20, 44), ('hb_boat3', 24, 49), ('hb_boat2', 11, 45), ('hb_boat4', 4, 47), ('hb_boat1', 48, 43), ('hb_boat2', 28, 44), ('hb_boat4', 36, 47), ('hb_boat1', 66, 45),
                     ('hb_boat3', 72, 49), ('hb_boat2', 66, 52), ('hb_boat4', 8, 52), ('hb_boat1', 76, 44), ('hb_boat3', 30, 52)):
        L = np.array(STAMPS[nm]['layers']); hh, ww = L.shape[1:]
        if all(m.cls[y + j, x + i] == 'w' and m.L[2, y + j, x + i] == 0 for i in range(ww) for j in range(hh)):
            for j in range(hh):
                for i in range(ww):
                    t = int(L[:, j, i].max())
                    if t: m.L[2, y + j, x + i] = t
    m.scatter(8, seed=146, on='.T')
    m.write(146, h, "# Saltmere - The Harbour (146). WRITTEN BY layouts/saltmere_rj.py (PF Rejuv) - edit that script.\n")
    if prev: m.preview(prev, 0.5)
    return d


# ====================================================================================================== 147
def build_147(prev=None):
    W, H = 88, 72
    m = K.RMap(W, H, 51, 147, water='Ocean', kit={1: 'ak', 2: 'sh'}); m.keep_under = 'gds'
    def lip(x): return 62 + int(round(1.5 * math.sin(x / 6.0) + 1.5 * (vnoise(x, 0, 13, 5.0) - 0.5)))
    for x in range(W):
        for y in range(H):
            if y <= lip(x): m.ht[y, x] = 1
            elif y > lip(x) + 3: m.cls[y, x] = 'w'
            else: m.cls[y, x] = 's'
            rise = 26 <= x <= 62 and y <= 24 + int(round(1.0 * math.sin(x / 4.0))) if not 40 <= x <= 48 else 26 <= x <= 62 and y <= 24
            west = x <= 18 and y <= 20 + int(2 * math.sin(x / 5.0)); east = x >= 70 and y <= 22 + int(2 * math.cos(x / 5.0))
            if rise or west or east: m.ht[y, x] = 2
    m.cls[(m.cls == 'w') & (np.arange(H)[:, None] > 67)] = 'W'
    for y in range(H):
        for x in range(W):
            if m.ht[y, x] >= 1 and (y < 2 + 2 * vnoise(x, 0, 7, 4.0) or x > 85 - 2 * vnoise(0, y, 8, 4.0)) and m.cls[y, x] == '.':
                m.cls[y, x] = 'T'
    m.stairs(41, 24, w=7, kit_rows=4)                                  # the Playhouse steps
    m.stairs(8, 20, w=3, kit_rows=4); m.stairs(76, 22, w=3, kit_rows=4)
    m.plan_cliffs()
    G = dict(c='g', only='.tT')
    m.rect(0, 35, 6, 6, 'g', only='.tT')                                # from the Players' Gate (warps x 0, y 36-39)
    m.lane([(4, 37.5), (14, 38), (24, 39.5), (34, 40)], w=4.2, seed=41, wobble=0.3, **G)
    m.blob(44, 36, 13.5, 7.0, 'g', seed=42, rough=0.3, only='.tT')       # the players' square
    m.rect(41, 28, 7, 4, 'g', only='.tT')
    m.rect(28, 19, 33, 5, 'g', only='.tT')                              # the Playhouse forecourt (h=2)
    m.lane([(56, 38), (66, 37), (77, 34), (77.5, 28)], w=2.8, seed=43, wobble=0.3, **G)
    m.lane([(9.5, 26), (10, 31), (12, 36)], c='d', w=2.3, seed=44, wobble=0.3, only='.tT')
    m.lane([(3, 15), (10, 16), (17, 15.5)], c='d', w=2.2, seed=45, wobble=0.3, only='.tT')
    m.lane([(72, 18), (80, 19), (85, 18)], c='d', w=2.2, seed=46, wobble=0.3, only='.tT')
    m.lane([(22, 41), (20, 48), (24, 54), (34, 56), (48, 55), (60, 56), (72, 54), (80, 49), (78, 40)], c='d', w=2.5, seed=47, wobble=0.4, only='.tT')
    m.lane([(44, 43), (44.5, 50), (46, 55)], c='d', w=2.4, seed=48, wobble=0.3, only='.tT')
    for c in 'gd': m.smooth(c, into='.', passes=2, only='.tT')
    m.blob(44.5, 36.5, 2.6, 1.6, '.', seed=49, rough=0.1, only='g')    # a green island under the square's tree
    d = {}
    d['gym'] = bld(m, 'pf_playhouse', 37, 7, 'SM_GYM', 'Playhouse door')
    for nm, x, y in (('gl_flat2', 28, 12), ('sh_shop', 51, 5), ('gl_shed', 24, 14)): bld(m, nm, x, y)   # the rise's flanks
    if d['gym'] is None: raise SystemExit('saltmere 147: no room for the Playhouse')
    hd = []
    hd += house_row(m, HOUSES_SH, 2, 17, 13, 11)
    hd += house_row(m, HOUSES_SH + ['gl_emblem'], 69, 86, 16, 12)
    hd += house_row(m, HOUSES_SH, 18, 36, 34, 13)
    hd += house_row(m, HOUSES_SH + ['gl_cot'], 58, 76, 33, 14)
    hd += house_row(m, HOUSES_SH + HOUSES_GL, 4, 40, 52, 15)
    hd += house_row(m, HOUSES_SH, 50, 82, 52, 16)
    hd += house_row(m, HOUSES_GL, 2, 22, 31, 17)
    warps, ev = old_events(147)
    E = list(warps)
    E.append(seat(m, ev, 'Playhouse sign', d['gym'][0] + 3, d['gym'][1] + 1, 'g'))
    E.append(seat(m, ev, 'PLAYERS GATE', 4, 41, '.g'))
    E.append(seat(m, ev, 'Costumier', 26, 41, 'g'))
    E.append(seat(m, ev, 'Street player', 48, 38, 'g'))
    if ev: raise SystemExit('saltmere 147: events not seated %s' % list(ev))
    m.events += E
    for e in warps: m.taken[e['at'][1], e['at'][0]] = True
    for x, y in K.incoming(147): m.taken[y, x] = True
    m.stamp('pf_g_tree2', 43, 31)                                        # the square's old tree
    props(m, (('hb_banner', 36, 20), ('hb_banner', 52, 20), ('hb_tables', 31, 31), ('hb_tables', 53, 31), ('gl_tables', 35, 40),
              ('gl_tables', 52, 39), ('hb_rugline', 18, 41), ('hb_rugline2', 28, 43), ('hb_dyeline', 14, 42), ('hb_washline', 6, 27),
              ('pf_logbench', 39, 41), ('pf_logbench', 48, 41), ('hb_boxes', 57, 36), ('hb_cask', 33, 36), ('hb_keg', 56, 41),
              ('hb_banner', 30, 23), ('hb_banner', 58, 23), ('pf_logbench', 32, 22), ('pf_logbench', 55, 22), ('hb_washline', 66, 45),
              ('hb_barrel', 64, 39), ('sh_crates', 70, 38)), on='.g')
    for x, y in ((31, 30), (53, 30)):
        st = STAMPS['pf_p_awning']
        if all(not m.taken[y, x + i] for i in range(3)): m.over += [(2, x + i, y, max(st['layers'][z][0][i] for z in range(3))) for i in range(3)]
    m.fence(4, 38, 61); m.fence(50, 84, 61)
    props(m, (('hb_boat2', 10, 64), ('hb_boat4', 30, 64), ('pf_p_net', 56, 64), ('hb_barrels', 70, 64), ('ak_rock2', 82, 65)), on='s')
    lamps(m, ((34, 19), (54, 19), (40, 27), (49, 27), (30, 35), (58, 34), (12, 36), (22, 36), (40, 46), (50, 46), (20, 50), (64, 50),
              (76, 50), (10, 14), (78, 17), (68, 36), (6, 34)))
    print('  147 blocks', [blockfill(m, INFILL, b, 147 + i) for i, b in enumerate(((60, 23, 86, 34), (2, 22, 22, 35), (62, 40, 86, 50), (4, 42, 20, 51), (26, 42, 40, 51), (50, 42, 60, 51)))])
    print('  147 yard trees', m.autotrees(36, TREES, seed=147, gap=0, box=(0, 0, W, 60)))
    h = head(147, '147_saltmere_oldtown.yaml', biome='village')
    finish(m, 147, h, "# Saltmere - Old Town (147). WRITTEN BY layouts/saltmere_rj.py (PF Rejuv) - edit that script.\n")
    if prev: m.preview(prev, 0.5)
    return d


def main():
    a = sys.argv[1:]
    which = [x for x in a if x.isdigit()] or ['140', '146', '147']
    out = {}
    if '140' in which: out[140] = build_140('/tmp/mb7/s140.png' if '--preview' in a else None)
    if '146' in which: out[146] = build_146('/tmp/mb7/s146.png' if '--preview' in a else None)
    if '147' in which: out[147] = build_147('/tmp/mb7/s147.png' if '--preview' in a else None)
    if 140 in out:                                                       # 141's HealingSpot follows the PC door
        x, y = out[140]['pc']; p = os.path.join(HERE, 'specs', '141_saltmere_interiors.yaml')
        s = open(p).read(); s = re.sub(r'HealingSpot: \[140, \d+, \d+\]', 'HealingSpot: [140, %d, %d]' % (x, y + 1), s); open(p, 'w').write(s)
    print('doors', out)


if __name__ == '__main__':
    main()
