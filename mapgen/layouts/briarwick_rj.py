#!/usr/bin/env python3
"""Briarwick (120) on the PF Rejuv sheet (tileset 50 "PF Rejuv Village"), 72x64.  MAPGEN 2h.
A Sheridan-style forest village: old-growth lattice forest on every side, a stream down the west with the Thistledown Lea road
crossing it on a raised plank walkway (rows 30-31), the north ridge (h=1) under Sheridan cliffs with the elder tree
Loomhouse on its knoll and the Loyal Three shrine at its west end, giant hollow trees (Prismfall's own art, re-graded
to Sheridan greens) as the Guildhall, Treetop House and Cutter's House, Sheridan timber houses for the Help Center,
the Mart and the chapel, the weavers' deck, lantern decks to the south-east, silk garlands over the green.
Story events come from layouts/story_early.py; this script seats them.
Run: python3 -I layouts/briarwick_rj.py && python3 -I build.py 120"""
import os, sys, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import rkit as K
from rkit import C, STAMPS
from terrain import vnoise
import story_early as SE
W, H = 72, 64
DECK = {k: C('sh', v) for k, v in dict(TL=488, T=489, TR=490, L=496, C=497, R=498, BL=504, B=505, BR=506,
                                        legL=523, leg=524, legR=525).items()}
TREES = ['tr_oak', 'tr_oak2', 'tr_pine', 'tr_pine2', 'tr_oak2']
GARL = None
PALE = 3402                                # Goldenleaf pale deck plank (gl part: composite id = source id)


def sx(y):
    # Organic woodland stream: gentle east meander past the weavers' dye vats (y=35..44) into the south dye pool
    dye_bend = 2.6 * math.exp(-((y - 39.5) / 6.5) ** 2)
    return 8 + int(round(dye_bend + 2.0 * math.sin(y / 6.8) + 1.5 * (vnoise(0, y, 6, 6.0) - 0.5)))


def ridge(x):
    """last row of the north ridge (h=1)"""
    if 28 <= x <= 50: return 14                    # map builder 9: the knoll runs on to the North Gate lane
    if 18 <= x <= 27: return 12 + (1 if x > 22 else 0)
    return 10 + int(round(1.5 * math.sin(x / 5.0) + 1.5 * (vnoise(x, 0, 3, 6.0) - 0.5)))


def deck(m, x0, y0, w, h, stairs=None, open_e=(), open_w=()):
    """Sheridan raised cedar timber deck: warm 9-slice top (Layer 0 after paint so props never punch grass holes),
    stilts below, plank stairs down the front at stairs=x (with open top entry), and open bridge joins."""
    if not hasattr(m, '_deck_tiles'): m._deck_tiles = []
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            top = (y == y0)
            bot = (y == y0 + h - 1) and not (stairs is not None and x in (stairs, stairs + 1))
            lft = (x == x0) and (y not in open_w)
            rgt = (x == x0 + w - 1) and (y not in open_e)
            k = ('T' if top else 'B' if bot else '') + ('L' if lft else 'R' if rgt else '')
            k = k or 'C'
            tid = DECK[k]
            m.tile(tid, x, y, 1); m.cls[y, x] = 'D'
            m._deck_tiles.append((x, y, tid))
    if all(m.inb(x, y0 - 1) and m.cls[y0 - 1, x] in '.t' and not m.taken[y0 - 1, x] for x in range(x0, x0 + w)):
        m.fence(x0, x0 + w - 1, y0 - 1)                              # a back rail
    for x in range(x0, x0 + w):
        if stairs is not None and x in (stairs, stairs + 1): continue
        m.tile(DECK['legL' if x == x0 else 'legR' if x == x0 + w - 1 else 'leg'], x, y0 + h, 1); m.cls[y0 + h, x] = 'B'
    if stairs is not None:
        for i, x in enumerate((stairs, stairs + 1)):
            m.tile(m.STAIRS[0 if i == 0 else 2], x, y0 + h, 2); m.cls[y0 + h, x] = 'd'


def walkway(m, x0, x1, y):
    """2-wide warm cedar plank walkway (rows y, y+1) between x0..x1, open left/right with N/S guard rails"""
    if not hasattr(m, '_deck_tiles'): m._deck_tiles = []
    for x in range(x0, x1 + 1):
        m.tile(DECK['T'], x, y, 1); m.tile(DECK['B'], x, y + 1, 1); m.cls[y, x] = m.cls[y + 1, x] = 'D'
        m._deck_tiles.append((x, y, DECK['T'])); m._deck_tiles.append((x, y + 1, DECK['B']))
        m.taken[y, x] = m.taken[y + 1, x] = True


def build(preview=None):
    m = K.RMap(W, H, 50, 120, water='Sea(Grass)', kit='sh')
    m.keep_under = 'd'
    # ---------------------------------------------------------------- terrain
    for x in range(W):
        for y in range(H):
            if y <= ridge(x): m.ht[y, x] = 1
    for y in range(H):
        s = sx(y)
        for x in range(s, s + 3): m.cls[y, x] = 'w'
    m.blob(16, 49, 5.8, 3.4, 'w', seed=7, rough=0.5)
    m.blob(13, 45, 2.8, 2.2, 'w', seed=8, rough=0.4)
    for y in range(H):
        for x in range(W):
            if m.cls[y, x] == 'w': m.ht[y, x] = 0
    # old-growth border, ragged inner edge; lush curved forest skirt along the south edge framing Gossamer Wood gate
    for y in range(H):
        for x in range(W):
            if m.cls[y, x] != '.': continue
            edge = min(x, W - 1 - x, y, H - 1 - y)
            s_skirt = (H - 1 - y) < 5 + int(round(2.4 * vnoise(x, 9, 13, 5.5))) and not (32 <= x <= 39)
            deep = edge < 4 + 4 * vnoise(x, y, 11, 6.0) or s_skirt
            knoll = ((x - 36) / 9.0) ** 2 + ((y - 11) / 5.5) ** 2 < 1.0 + 0.5 * (vnoise(x, y, 4, 3.0) - 0.5)
            shrine = ((x - 22) / 5.5) ** 2 + ((y - 9) / 4.5) ** 2 < 1.0 + 0.5 * (vnoise(x, y, 5, 3.0) - 0.5)
            ridge_forest = m.ht[y, x] == 1 and not knoll and not shrine
            if deep or ridge_forest: m.cls[y, x] = 'T'
    # ---------------------------------------------------------------- lanes: curved dirt lanes into the round green
    m.stairs(35, 14, w=3, kit_rows=4)
    m.stairs(21, 12, w=2, kit_rows=4)                                           # the ridge lip is row 12 at x 21-22
    m.plan_cliffs()
    LN = dict(c='d', only='.tT')
    m.blob(40.5, 33.0, 8.4, 5.0, 'd', seed=51, rough=0.3, only='.tT')            # the green: an oval of trodden earth
    m.rect(0, 30, 16, 2, 'd', only='.T')                                         # Thistledown Lea road (rows 30-31) from the west edge
    m.lane([(15, 31), (21, 31.4), (27, 32.4), (32.5, 33)], w=2.6, seed=52, wobble=0.2, **LN)
    m.rect(35, 18, 3, 1, 'd', only='.tT')
    m.lane([(36.5, 18.5), (37.2, 21.5), (39.2, 24.6), (40, 28.4)], w=2.8, seed=53, wobble=0.2, **LN)   # down from the Loomhouse
    m.rect(21, 16, 2, 1, 'd', only='.tT')
    m.lane([(22, 16.5), (23.4, 19.2), (29, 20.4), (35.6, 19.6)], w=2.1, seed=54, wobble=0.2, **LN)     # the shrine path
    m.lane([(48.4, 32.6), (54, 31.3), (60, 31)], w=2.9, seed=55, wobble=0.2, **LN)                      # east lane to the pylon
    m.rect(59, 30, 13, 3, 'd', only='.tT')
    m.rect(34, 57, 4, 7, 'd', only='.tT')                                        # from Gossamer Wood
    m.lane([(35.6, 57.5), (34.4, 52), (34.8, 46.5), (36.6, 41.5), (38.4, 38)], w=2.9, seed=56, wobble=0.25, **LN)
    m.lane([(46, 36.6), (48.4, 41), (52, 46), (58, 47.4), (64.4, 47.2)], w=2.4, seed=57, wobble=0.25, **LN)   # round the chapel
    m.lane([(36.5, 56.6), (44, 57), (53, 56.6), (62.5, 56.8)], w=2.2, seed=58, wobble=0.2, **LN)        # the lantern decks
    m.lane([(34.6, 46.2), (30, 45.2), (25, 45.4), (19.6, 44.6), (17.8, 40), (17.6, 35), (18.4, 32)], w=2.3, seed=59, wobble=0.25, **LN)  # dyers' loop
    m.lane([(34.5, 57.4), (30, 57.2), (26.5, 56.6)], w=2.0, seed=60, wobble=0.15, **LN)
    m.rect(22, 10, 2, 3, 'd', only='.')                                          # shrine path above the stairs
    m.smooth('d', into='.', passes=2, only='.tT')
    # map builder 9 (SWAP 1A): the North Gate lane up the ridge to Spinners' Rise; the old Thistledown Lea road ends at the
    # stream (the Lea now joins the Gossamer's west eaves, not Briarwick)
    m.lane([(42.5, 12.5), (46, 9.5), (51, 6), (53.5, 2), (53.5, 0)], w=3.2, seed=63, wobble=0.15, **LN)
    m.rect(52, 0, 4, 3, 'd', only='.tT')
    m.rect(0, 29, 4, 4, 'T', only='.d')
    m.blob(40.8, 32.0, 3.6, 2.0, '.', seed=61, rough=0.2, only='d')              # the island under the Gathering Tree
    # ---------------------------------------------------------------- buildings (steep-shingle Goldenleaf & living giant trees; exact door coords preserved!)
    E = []
    P = lambda n, at, **kw: E.append(SE.place(120, n, at, **kw))
    d = {}
    d['gym'] = m.stamp('pf_g_elder', 30, 1, 'BW_GYM', 'Gym door')                # door (36, 12)
    d['guild'] = m.stamp('pf_g_tree6', 13, 19, 'BW_GUILD', 'Guildhall door')     # door (17, 26)
    d['pc'] = m.stamp('gl_ell', 45, 19, 'BW_PC', 'Poke Center door')             # warm steep-roof lodge w/ tea patio, door (47, 25) exact!
    d['house1'] = m.stamp('pf_g_tree4', 58, 17, 'BW_HOUSE1', 'Treetop House door')  # door (60, 23)
    d['mart'] = m.stamp('gl_flat2', 25, 39, 'BW_MART', 'Mart door')              # steep-shingle timber mart, door (29, 43) exact!
    d['chapel'] = m.stamp('sh_big', 55, 34, 'BW_CHAPEL', 'Chapel door')          # door (63, 42) + Locked door (58, 42) exact!
    d['house2'] = m.stamp('pf_g_tree4', 40, 44, 'BW_HOUSE2', "Cutter's House door")  # door (42, 50)
    m.stamp('pf_g_tree2', 39, 27)                                                # the Gathering Tree on the green
    hd = []
    # Clear organic meadow pocket right around the SW cottage gl_cot (24, 49) while keeping the lush south forest rim!
    for y in range(49, 59):
        for x in range(23, 32):
            if m.cls[y, x] == 'T': m.cls[y, x] = '.'
    for nm, x, y in (('pf_g_tree4p', 20, 36), ('pf_g_tree2', 57, 7), ('pf_g_tree2', 66, 14),
                     ('pf_g_tree2', 46, 50), ('gl_shed', 65, 22), ('gl_shed', 50, 36), ('gl_cot', 24, 49), ('pf_g_tree2', 8, 54),
                     ('pf_g_tree2', 67, 40)):
        if m.free(x, y, STAMPS[nm]['w'], STAMPS[nm]['h'], on='.dT') and not (nm.startswith('pf_g') and (m.cls[y:y + STAMPS[nm]['h'], x:x + STAMPS[nm]['w']] == 'd').any()):
            m.stamp(nm, x, y)
            if 'door' in STAMPS[nm]: dd = STAMPS[nm]['door']; hd.append((x + dd[0], y + dd[1]))
        else: print('  (no room for %s at %d,%d)' % (nm, x, y))
    # map builder 9: the Briarwick Lantern House (126, Trials) is a hollow tree under the Loyal Three shrine
    for lx, ly in ((24, 2), (23, 1), (25, 1), (12, 3), (14, 2), (10, 4), (16, 3)):
        sub = m.ht[ly:ly + 9, lx:lx + 6]; dx_, dy_ = lx + 2, ly + 6
        if m.free(lx, ly, STAMPS['pf_g_tree4']['w'], STAMPS['pf_g_tree4']['h'], on='.dT') and not m.cliff[ly:ly + 9, lx:lx + 6].any() \
                and sub.min() == sub.max() and m.cls[dy_ + 1, dx_] in '.d' and m.cls[dy_ + 2, dx_] in '.d' and not m.taken[dy_ + 1:dy_ + 3, dx_].any():
            d['lantern'] = m.stamp('pf_g_tree4', lx, ly, 'BW_LANTERN', 'Lantern House door', blend=True); break
    else: print('  (no room for the Lantern House tree)')
    for dx, dy in list(d.values()) + hd: m.doorpath((dx, dy), depth=8)
    for x, y in ((38, 31), (39, 33), (43, 31), (42, 33), (44, 32), (37, 32), (45, 27), (44, 27)):  # lush blossoms round the Gathering Tree & PC Lodge
        if m.cls[y, x] == '.' and not m.taken[y, x]: m.tile(m.decor['flowers'][(x * 3 + y) % 6], x, y, 1)
    put = lambda nm, x, y, on='.d': (m.stamp(nm, x, y) if m.free(x, y, STAMPS[nm]['w'], STAMPS[nm]['h'], on=on) and not m.cliff[y:y + STAMPS[nm]['h'], x:x + STAMPS[nm]['w']].any() else print('  (no room for %s at %d,%d)' % (nm, x, y)))
    put('pf_pcsign', 44, 25)
    deck(m, 22, 23, 7, 4, stairs=24)                         # the weavers' cedar deck beside the Guildhall tree
    deck(m, 51, 52, 5, 3, stairs=52, open_e=(52, 53))        # lantern cedar decks, south-east (open onto bridge)
    deck(m, 59, 52, 5, 3, stairs=61, open_w=(52, 53))
    walkway(m, 56, 58, 52)
    walkway(m, sx(30) - 2, sx(31) + 4, 30)                   # cedar plank bridge over the stream
    # ---------------------------------------------------------------- events
    P('To Gossamer Wood', (35, 63)); P('To Gossamer Wood b', (36, 63))
    E.append({'type': 'sign', 'name': 'North Gate sign', 'at': list(m.snap(51, 4, '.d', r=3)), 'post': False,
              'text': "NORTH GATE - Spinners' Rise, Frostwick Pass and the Hoar Road north."})
    P('Arrival', (34, 62)); P('Juno (arrival)', (36, 61)); P('Stage manager', (37, 62))
    gx, gy = d['gym']
    P('Loomhouse sign', (gx + 4, gy))                       # map builder 9: off the 1-row knoll walk to the North Gate lane
    P('Loyal Three shrine', (21, 8)); P('Old woman at the shrine', (22, 9)); P('Dusk petal', (23, 8))
    P('Lattice pylon', (69, 30)); P('Survey flags', (67, 33))
    for i, y in enumerate((30, 31, 32)): P('Pylon watch %d' % (i + 1), (63, y))
    P('Pallbearer Thistle', (66, 31)); P('Bereaved 1', (65, 30)); P('Bereaved 2', (66, 32))
    P('Tamsin (square)', (41, 34)); P('Festival poster', (38, 30)); P('Charcoal child', (38, 35))
    P('Weaver at loom', (26, 25)); P('Silk racks', (23, 24)); P('HiddenItem rope bridge', (28, 21))
    P('HiddenItem dye vats', (14, 38))
    for e in E: m.taken[e['at'][1], e['at'][0]] = True
    def S(n, ax, ay, on='.d', r=8):
        e = SE.place(120, n, m.snap(ax, ay, on, r=r)); E.append(e); m.taken[e['at'][1], e['at'][0]] = True
    S('Town sign', 38, 58); S('Finch', 57, 33); S('Rope-bridge Boy', 28, 32); S('Grandmother knitting', 45, 36)
    town = [('Dyer', 16, 37), ('Apprentice', 21, 32), ('Silk Merchant', 35, 35), ('Meridian Linesman', 53, 31), ('Tired Mother', 32, 46),
            ('Old Man on bridge', 9, 31), ('Girl in ogre mask', 44, 31), ('Boy in dog mask', 45, 32), ('Egg-seller', 47, 34),
            ('Tax-barge Deserter', 33, 55), ('Accord Chaplain', 60, 47), ('Youngster', 50, 29), ('Woman with basket', 48, 41),
            ("Cutter's Wife", 44, 52), ('Bun-seller', 40, 40)]
    for n, x, y in town: S(n, x, y)
    for e in E:
        if e.get('type') == 'sign':
            e['post'] = False; x, y = e['at']
            if e['name'] in ('Town sign', 'Loomhouse sign'): m.tile(4833, x, y - 1, 2); m.tile(4841, x, y, 1)
            elif e['name'] != 'Silk racks': m.tile(4847, x, y, 1)
    missing = SE.unplaced(120)
    if missing: raise SystemExit('briarwick: script events not placed: %s' % missing)
    m.events += E
    # Keep Poke Center doorstep & Briarwick Fly/HealingSpot (47, 26) strictly clear of snapped props!
    m.taken[26, 47] = True
    # ---------------------------------------------------------------- dressing
    for nm, x, y in (('pf_p_loom', 23, 24), ('pf_p_loom', 27, 24), ('pf_p_laundry', 23, 23), ('pf_p_vat_b', 14, 36),
                     ('pf_p_vat_r', 15, 37), ('pf_p_vat_y', 14, 39), ('sh_crates', 51, 52), ('sh_crates', 62, 52),
                     ('pf_logbench', 59, 53), ('sh_campfire', 38, 36), ('sh_crates', 47, 29), ('pf_p_silk', 54, 52), ('pf_p_silk', 60, 52),
                     ('pf_logbench', 38, 33), ('pf_logbench', 42, 33), ('hb_tables', 33, 30), ('hb_dyeline', 15, 34), ('hb_rugline', 31, 35),
                     ('hb_boxes', 34, 37), ('hb_cask', 44, 29), ('hb_washline', 62, 26), ('hb_barrel', 53, 26), ('hb_tables', 44, 37),
                     ('pf_logbench', 20, 47), ('hb_keg', 31, 43), ('hb_barrel2', 57, 46), ('hb_rugline2', 20, 28), ('pf_logbench', 47, 44),
                     ('hb_boxes2', 37, 51), ('hb_cask', 31, 54), ('pf_p_awning', 33, 29), ('pf_p_awning', 44, 36), ('hb_fish', 36, 29), ('hb_barrel', 47, 36),
                     # Cozy Pass-2 village craft: flower planters, stone benches, well, & dye-mill barrels
                     ('pf_planter0', 42, 26), ('pf_planter1', 26, 44), ('pf_planter2', 60, 43), ('pf_planter3', 31, 44),
                     ('pf_stonebench', 32, 21), ('pf_stonebench', 40, 21), ('pf_well', 44, 42)):
        st = STAMPS[nm]
        if m.free(x, y, st['w'], st['h'], on='.dD') or all(m.cls[y + j, x + i] == 'D' for i in range(st['w']) for j in range(st['h'])):
            m.over += [(z, x + i, y + j, t) for z in (1, 2) for j in range(st['h']) for i in range(st['w']) for t in [st['layers'][z][j][i]] if t]
            m.taken[y:y + st['h'], x:x + st['w']] = True
        else: m.near(nm, x, y, on='.d', r=2)
    # Shoreline reeds, azaleas, ferns & stream stones along the curved dye-mill brook
    for nm, x, y in (('nt_reed0', 11, 33), ('nt_reed1', 12, 35), ('nt_reed0', 13, 41), ('nt_reed1', 18, 47),
                     ('nt_reed0', 12, 52), ('nt_azalea0', 33, 19), ('nt_azalea1', 42, 19), ('nt_azalea2', 32, 59),
                     ('nt_azalea0', 39, 59), ('nt_azalea1', 55, 29), ('nt_azalea2', 20, 49)):
        st = STAMPS[nm]
        if m.free(x, y, st['w'], st['h'], on='.t') and not m.cliff[y:y + st['h'], x:x + st['w']].any():
            m.stamp(nm, x, y)
    for y in range(0, 3):                                     # above the elder's crown: wild grass, not lawn
        for x in range(26, 47):
            if m.cls[y, x] == '.' and not m.taken[y, x]: m.cls[y, x] = 't'
    rng = random.Random(3)                                    # wild grass along the forest edge and the stream banks
    for y in range(H):
        for x in range(W):
            if m.cls[y, x] == '.' and not m.taken[y, x] and m.ht[y, x] == 0:
                near_edge = any(m.inb(x + dx, y + dy) and m.cls[y + dy, x + dx] in 'Tw' for dx in (-2, -1, 0, 1, 2) for dy in (-2, -1, 0, 1, 2))
                if near_edge and vnoise(x, y, 17, 4.0) > 0.6: m.cls[y, x] = 't'
    for cx, cy, n in ((24, 30, 1), (31, 41, 1), (43, 26, 1), (60, 44, 1), (52, 42, 2), (40, 54, 2), (44, 60, 2), (27, 17, 1),
                      (57, 13, 2), (64, 18, 1), (14, 43, 1), (66, 46, 1), (52, 59, 2), (20, 58, 2), (22, 28, 1), (30, 26, 2),
                      (33, 23, 1), (43, 21, 1), (56, 27, 1), (24, 42, 1), (52, 37, 1), (30, 49, 1), (42, 41, 1), (66, 36, 1)):
        m.trees(cx, cy, n, TREES, r=3, seed=cx + cy * 5)
    for x, y in ((34, 22), (42, 27), (32, 38), (49, 35), (37, 48), (58, 29), (26, 31), (19, 30), (33, 29), (50, 45), (22, 46),
                 (16, 40), (45, 55), (57, 55), (61, 46), (32, 55), (25, 19), (33, 60), (38, 60)):
        if m.free(x, y - 1, 1, 2, on='.'): m.stamp('pf_lantern', x, y - 1)
    m.beds(prefixes=('sh_', 'gl_'))
    print('  yard trees', m.autotrees(26, TREES, seed=7, gap=0, box=(12, 14, 68, 60)))
    m.greenfill(2)
    # ---------------------------------------------------------------- paint
    m.paint()
    # Seat opaque Sheridan cedar deck planks on Layer 0 so deck props (looms, crates, silk racks, benches) sit on cedar, never grass!
    for dx_, dy_, tid_ in getattr(m, '_deck_tiles', ()):
        m.L[0, dy_, dx_] = tid_
        if m.L[1, dy_, dx_] == tid_:
            m.L[1, dy_, dx_] = 0
    # Clean stray top-right pole tile (3255) from gl_cot at (24, 49) -> (30, 49)
    if m.L[2, 49, 30] == 3255:
        m.L[2, 49, 30] = 0
    # Warm stepping stones along Loomhouse stair plaza, Gathering Tree green, and South Gossamer approach
    st0 = STAMPS['pf_stepstone0']['layers'][1][0][0]
    st1 = STAMPS['pf_stepstone1']['layers'][1][0][0]
    for sx_, sy_ in ((36, 19), (37, 22), (39, 25), (35, 32), (45, 32), (36, 59), (35, 61), (47, 26), (29, 44)):
        if m.inb(sx_, sy_) and m.cls[sy_, sx_] == 'd' and m.L[1, sy_, sx_] == 0 and m.L[2, sy_, sx_] == 0:
            m.L[1, sy_, sx_] = st0 if (sx_ + sy_) % 2 == 0 else st1
    garlands(m, ((33, 48, 28, 0), (33, 48, 38, 1), (44, 50, 27, 2), (17, 28, 30, 3), (50, 54, 33, 1), (33, 38, 56, 2), (32, 37, 45, 3), (34, 38, 60, 0)))
    m.scatter(9, seed=21, on='.T')
    m.seal_against([{'dir': 'N', 'offset': 52, 'to': 566, 'to_offset': 38}], spans=[('N', 52, 4)], keep=[tuple(e['at']) for e in m.events if e.get('type') == 'warp'])
    if preview: m.preview(preview, 0.5)
    head = {'id': 120, 'biome': 'forest', 'name': 'Briarwick', 'parent': 0, 'bgm': 'Lappet Town', 'rubric': True, 'yards_ok': True,
            'metadata': {'Outdoor': True, 'ShowArea': True, 'MapPosition': [0, 12, 22], 'BattleBack': 'forest'},
            'tone': [-10, -22, 2, 4], 'fog': {'name': 'prismfall_spores', 'opacity': 46, 'blend': 1, 'zoom': 100, 'sx': 1, 'sy': -1},
            'connections': [{'dir': 'N', 'offset': 52, 'to': 566, 'to_offset': 38}], '_file': '120_briarwick.yaml'}
    import yaml
    src = yaml.safe_load(open(os.path.join(K.HERE, 'layouts', 'briarwick_events.yaml')))[120]['head']
    for k in ('bgm', 'metadata', 'field', 'display_name'):
        if k in src: head[k] = src[k]
    m.write(120, head, '# Briarwick (120). WRITTEN BY layouts/briarwick_rj.py (PF Rejuv) - edit that script.\n')
    print('doors', d)
    return m


def garlands(m, runs):
    """silk garlands strung overhead (layer 3) across lanes; a lantern every fifth span"""
    g = [K.SINGLE['garl_plain'], K.SINGLE['garl_pennant'], K.SINGLE['garl_lantern'], K.SINGLE['garl_tufts']]
    for x0, x1, y, sd in runs:
        for i, x in enumerate(range(x0, x1 + 1)):
            if m.inb(x, y) and m.L[2, y, x] == 0: m.L[2, y, x] = g[(i + sd) % 4 if (i + sd) % 5 else 2]


if __name__ == '__main__':
    build(sys.argv[1] if len(sys.argv) > 1 else None)
