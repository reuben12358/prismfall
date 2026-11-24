#!/usr/bin/env python3
"""layouts/lumen.py - Lumen City, Zenith's capital district (map builder 15): 180 the Concourse, 181 the Lowlight and
608 the Lowlight (Shattered), on tileset 60 "PF Rejuv Lumen" with the Lumen kit (ldraw.py, layouts/lumenkit.py).

  180 The Concourse (96x72): the north rank of brass-and-verdigris townhouses on North Avenue, the Council Ward's
      grand stair (closed for the anniversary) and the Skyport steps (ticketed); the Circuit Gym in its own square on
      the west side; the Prism Plaza (the Prism fountain, the Meridian sunburst in brass, the Founders' Lamp, arc lamps,
      holo pylons, kiosks, an airship sliding overhead); Meridian Spire's black-cored tower on the east, its gold
      forecourt; the tram boulevard; Market Street (the Pokémon Center, the Lumen Arcade, Glide Cycles) and South
      Walk (the West Gate, the Fossil Lab, the apartments); the gardens on the plateau's lip over Nadir's lights; and
      the Lowlight stairs down the east terrace (edge to 181).
  181 The Lowlight (60x44): the streets at the Spire's foot - soot-brick tenements, washing strung between them, the
      noodle cart, the hopscotch, the Nadir lift, the Spire's service door in the cliff, Rook's crew square; the twelve
      residents at fixed spots (story/24_SCRIPT_CH5.md).
  608 The Lowlight (Shattered): the same streets after the Shatter - the twelve in glass at the same spots, Bleed glass
      underfoot, the Veil at the district's edge, the lamps dead.

    python3 -I layouts/lumen.py [180|181|608]"""
import os, sys, random
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lumenkit as LK
from lumenkit import City, sz
from rkit import P1, STAMPS
import story_ch5 as ST
from story_early import page, ev, sign
HERE = LK.HERE

LINK_OF = {'lb_pc': ('LC_PC', 'Pokémon Center'), 'lb_arcade': ('LC_DEPT', 'Lumen Arcade'), 'lb_gym': ('LC_GYM', 'Circuit Gym'),
           'lb_cycle': ('LC_BIKE', 'Glide Cycles'), 'lb_lab': ('LC_FOSSIL', 'Fossil Lab'), 'lb_apt': ('LC_APT', 'Apartment'),
           'lb_spire': ('LC_TOWER', 'Meridian Spire'), 'lb_gate': ('GATE_LUMEN', 'West Gate')}
PLAQUES = ["A brass plate: PRIVATE RESIDENCE. A smaller plate under it: NO HAWKERS. A smaller one under that: NO, REALLY.",
           "Locked. Through the glass, a hallway lit like noon.", "A brass plate: OFFICES OF THE SALLOW LINE. Closed for the anniversary.",
           "Locked. A note in the door: GONE TO THE GALA (STANDING OUTSIDE IT).", "A brass plate: LATTICE ENGINEERS' GUILD, LUMEN CHAPTER.",
           "Locked. Somebody inside is practising the trumpet. Badly. With feeling.", "A brass plate: CHANDLER & SONS, LAMP-MAKERS SINCE BEFORE.",
           "Locked. The doorbell plays four notes of the anniversary song."]


def door_events(m, placed, plaques=True):
    """unlinked fronts get a flavour plate on their door cell"""
    k = 0
    for nm, x, y, d in placed:
        if d is not None: continue
        st = STAMPS[nm]
        if 'door' not in st: continue
        dx, dy = st['door']
        if plaques:
            m.events.append({'type': 'sign', 'name': 'Door plate %d' % k, 'at': [x + dx, y + dy], 'post': False,
                             'text': PLAQUES[(k + m.seed) % len(PLAQUES)]})
        k += 1


USED_LINKS = set()


def stamp_link(m, nm, x, y):
    lk = LINK_OF.get(nm)
    if lk and (m.seed, lk[0]) in USED_LINKS: lk = None
    if lk: USED_LINKS.add((m.seed, lk[0]))
    d = m.put(nm, x, y, link=lk[0] if lk else None, dname=lk[1] if lk else None)
    return (nm, x, y, d)


def rank(m, names, x0, x1, y_door, seed=0, gap=0):
    """buildings shoulder to shoulder whose doors sit on row y_door; returns [(name, x, y, door)]"""
    out = []; x = x0; i = 0
    while i < len(names):
        nm = names[i]; w, h = sz(nm)
        if x + w - 1 > x1: break
        y = y_door - h + 1
        out.append(stamp_link(m, nm, x, y)); x += w + gap; i += 1
    return out


def lamps(m, pts, name='lm_arclamp'):
    for x, y in pts:
        if m.free(x, y - 2, 1, 3, on='pqlrd.'):
            m.stamp(name, x, y - 2)


def scatter_wear(m, n_per_100=6, on='pq', seed=0, kinds=(0, 1, 2, 3, 4)):
    rng = random.Random(m.seed * 11 + seed)
    for y in range(m.H):
        for x in range(m.W):
            if m.cls[y, x] in on and not m.taken[y, x] and (x, y) not in m.keep_clear and rng.random() * 100 < n_per_100:
                m.over.append((2, x, y, P1('lm_wear%d' % rng.choice(kinds))))


def seat(m, mid, name, at, **kw):
    e = ST.place(mid, name, at, **kw); m.events.append(e); m.keep_clear.add(tuple(at)); return e


PACK_LUMEN = ['lb_t5a', 'lb_t8a', 'lb_t7a', 'lb_t4b', 'lb_t9a', 'lb_t8b', 'lb_t6a', 'lb_t6b', 'lb_t5b', 'lb_t7b', 'lb_t6c', 'lb_t4a', 'lb_t10a']
PACK_LOW = ['lb_l5a', 'lb_l6b', 'lb_l4a', 'lb_l5b', 'lb_l3a', 'lb_l6a']


def pack(m, x0, x1, y_door, ymin, names, seed=0, fixed=(), fill=True):
    """a block: buildings shoulder to shoulder with their doors on row y_door, between columns x0..x1, none taller than
    the block (rows ymin..y_door); `fixed` = [(name, x)] placed first; the rest of the block is roofed over"""
    rng = random.Random(m.seed * 13 + seed)
    out = []
    for nm, x in fixed:
        w, h = sz(nm); out.append(stamp_link(m, nm, x, y_door - h + 1))
    x = x0
    while x <= x1:
        if m.taken[y_door, x]: x += 1; continue
        room = 0
        while x + room <= x1 and not m.taken[y_door, x + room]: room += 1
        cand = [n for n in names if sz(n)[0] <= room and sz(n)[1] <= y_door - ymin + 1 and n not in LINK_OF]
        if not cand: x += room; continue
        cand.sort(key=lambda n: -sz(n)[0] * 10 - rng.random() * 25)
        nm = cand[0] if rng.random() < 0.5 else rng.choice(cand)
        w, h = sz(nm)
        if not m.free(x, y_door - h + 1, w, h, on='pqlrd.'): x += 1; continue
        out.append(stamp_link(m, nm, x, y_door - h + 1)); x += w
    if fill:
        before = m.cls == 'f'
        m.fill(x0, ymin, x1, y_door)
        if getattr(m, 'roof_kind', 'V') != 'T' and seed % 2 == 0:
            m.slate = getattr(m, 'slate', set()) | {(int(x), int(y)) for y, x in np.argwhere((m.cls == 'f') & ~before)}
    return out


# ============================================================================================ 180 the Concourse
def build_180():
    W, H = 96, 72
    m = City(W, H, 180, base='p')
    m.ht[:] = 2; m.roof_kind = 'V'
    # -------- the plateau: the south lip over Nadir, the east drop, the terrace down to the Lowlight
    m.cls[63:, :] = 'x'; m.ht[63:, :] = 0
    m.cls[66:68, :] = 'n'
    m.cls[48:63, 84:] = 'p'; m.ht[48:63, 84:] = 1
    m.cls[0:47, 93:] = 'x'; m.ht[0:47, 93:] = 0
    m.stairs(88, 47, w=3, n=4)
    # -------- streets and squares
    m.rect(28, 10, 37, 22, 'q')                              # the Prism Plaza
    m.rect(73, 13, 20, 19, 'q')                              # the Spire's forecourt
    m.rect(0, 33, 84, 4, 'r')                                # the tram boulevard
    m.track([(x, 34) for x in range(0, 84)])
    m.rect(0, 59, 84, 3, '.')                                # the lawns on the lip
    m.rect(44, 0, 8, 7, 'q'); m.rect(73, 0, 4, 13, 'q')       # the Council stair, the Skyport steps
    placed = []
    placed.append(stamp_link(m, 'lb_spire', 77, 0))
    # -------- the north rank on North Avenue (doors on row 6)
    placed += pack(m, 0, 43, 6, 0, PACK_LUMEN, seed=1, fixed=[('lb_apt', 30)])
    placed += pack(m, 52, 72, 6, 0, PACK_LUMEN, seed=2)
    # -------- the west quarter: two ranks, the gym, the Gym Square's side blocks
    placed += pack(m, 0, 27, 15, 10, PACK_LUMEN, seed=3)
    placed += pack(m, 0, 27, 22, 17, PACK_LUMEN, seed=4, fixed=[('lb_gym', 9)])
    placed += pack(m, 0, 8, 31, 26, PACK_LUMEN, seed=5)
    placed += pack(m, 20, 27, 31, 26, PACK_LUMEN, seed=6)
    # -------- the block between the plaza and the forecourt (a lane on rows 19-20)
    placed += pack(m, 66, 72, 18, 10, PACK_LUMEN, seed=7)
    placed += pack(m, 66, 72, 31, 21, PACK_LUMEN, seed=8)
    # -------- Row A on Market Street (doors on row 45), Row B on South Walk (doors on row 56)
    for lx in (16, 63):                                      # Lantern Lane and Arc Street run north-south through both rows
        m.rect(lx, 37, 3, 22, 'p')
        for y in range(38, 58): m.taken[y, lx:lx + 3] = True
    placed += pack(m, 0, 15, 45, 39, PACK_LUMEN, seed=9)
    placed += pack(m, 19, 62, 45, 39, PACK_LUMEN, seed=11, fixed=[('lb_pc', 20), ('lb_arcade', 34), ('lb_cycle', 50)])
    placed += pack(m, 66, 83, 45, 39, PACK_LUMEN, seed=12)
    placed += pack(m, 0, 15, 56, 49, PACK_LUMEN, seed=10, fixed=[('lb_gate', 1)])
    placed += pack(m, 19, 62, 56, 49, PACK_LUMEN, seed=13, fixed=[('lb_lab', 22), ('lb_apt', 45)])
    placed += pack(m, 66, 83, 56, 49, PACK_LUMEN, seed=14)
    for lx in (16, 63):
        for y in range(38, 58): m.taken[y, lx:lx + 3] = False
        lamps(m, [(lx, 41), (lx + 2, 52)])
    door_events(m, placed)
    # the Council stair (closed) and the Skyport steps (ticketed)
    for y in range(1, 6):
        for i, x in enumerate(range(45, 51)): m.over.append((1, x, y, P1('lm_stair_' + ('l' if i == 0 else 'r' if i == 5 else 'm'))))
    for x in range(44, 52): m.over.append((1, x, 6, P1('lm_bars_m' if x not in (47, 48) else 'lm_bars_l')))
    for x, y in ((44, 1), (51, 1), (44, 4), (51, 4)): m.prop('lm_bollard', x, y)
    for y in range(1, 4):
        for i, x in enumerate(range(73, 77)): m.over.append((1, x, y, P1('lm_stair_' + ('l' if i == 0 else 'r' if i == 3 else 'm'))))
    for x in range(73, 77): m.over.append((1, x, 4, P1('lm_bars_m')))
    m.keep_clear |= {(x, y) for x in range(44, 52) for y in range(0, 8)} | {(x, y) for x in range(73, 77) for y in range(0, 6)}
    # -------- the Prism Plaza
    m.put('lm_fountain', 43, 13)
    m.put('lm_sun', 44, 20, force=True)
    m.put('lm_statue', 45, 26)
    for bx, by in ((31, 13), (52, 13), (31, 25), (54, 25)):              # four lawns with flowers round the fountain
        m.rect(bx, by, 6, 3, '.')
        for x, y in ((bx - 1, by), (bx + 6, by)): m.try_put('lm_topiary', x, y - 1, on='q')
    m.inlay([(x, 22) for x in range(28, 44)] + [(x, 22) for x in range(49, 65)] + [(46, y) for y in range(29, 32)])
    m.keep_clear |= {(x, 22) for x in range(28, 65)} | {(46, y) for y in range(25, 32)} | {(x, 19) for x in range(40, 52)}
    lamps(m, [(41, 13), (50, 13), (41, 19), (50, 19), (38, 24), (53, 24), (30, 11), (63, 11), (30, 30), (63, 30), (43, 30), (49, 30), (38, 18), (53, 18)])
    for x, y in ((28, 13), (62, 13), (28, 25), (62, 25)): m.try_put('lm_tree', x, y, on='q')
    for x, y in ((35, 17), (57, 17)): m.try_put('lm_holo', x, y, on='q')
    for x, y in ((32, 17), (52, 17), (39, 28), (51, 28), (34, 21), (56, 21)): m.try_put('lm_bench', x, y, on='q')
    for x, y in ((36, 11), (55, 11), (33, 29), (58, 29)): m.try_put('lm_planter', x, y, on='q')
    m.try_put('lm_kiosk', 29, 27, on='q'); m.try_put('lm_news', 60, 27, on='q'); m.try_put('lm_clock', 61, 18, on='q')
    m.try_put('lm_topiary', 42, 26, on='q'); m.try_put('lm_topiary', 49, 26, on='q')
    for x, y in ((37, 21), (55, 21)): m.try_put('lm_bannerlamp', x, y, on='q')
    for i, (x, y) in enumerate(((29, 19), (59, 19), (34, 23), (58, 23))):
        m.try_put(['lm_stall_a', 'lm_stall_b', 'lm_stall_c', 'lm_stall_b'][i], x, y, on='q')
    m.try_put('lm_airship', 50, 10, on='q')
    for x in range(30, 64, 2):
        if m.free(x, 10, 1, 1, on='q'): m.over.append((2, x, 10, P1('lm_bulbs%d' % (x % 3))))
    # -------- the Spire's forecourt: the gala carpet, banner lamps, parterres, guards
    for y in range(13, 32):
        for i, x in enumerate((84, 85, 86)):
            m.over.append((1, x, y, P1('lm_carpet_%s' % ('w' if i == 0 else 'e' if i == 2 else 'c'))))
    m.keep_clear |= {(x, y) for x in (84, 85, 86) for y in range(13, 33)} | {(83, 13), (87, 13)}
    for y in (15, 19, 23, 27): m.try_put('lm_bannerlamp_w', 82, y, on='q'); m.try_put('lm_bannerlamp_w', 88, y, on='q')
    for bx in (75, 89):
        m.rect(bx, 16, 3, 12, '.')
        for y in (15, 28): m.try_put('lm_topiary', bx + 1, y - 1, on='q')
    m.try_put('lm_pylon', 79, 28, on='q'); m.try_put('lm_planter3', 89, 30, on='q'); m.try_put('lm_planter3', 74, 30, on='q')
    m.try_put('lm_statue', 79, 14, on='q'); m.try_put('lm_holo', 90, 13, on='q')
    for y in range(0, 47): m.prop('lm_railing_m', 92, y)
    # -------- the west quarter's Gym Square
    for x, y in ((10, 24), (16, 24)): m.try_put('lm_stall_c' if x == 10 else 'lm_stall_a', x, y, on='p')
    for x, y in ((10, 28), (17, 28)): m.try_put('lm_tree', x, y - 1, on='p')
    lamps(m, [(13, 25), (9, 30), (19, 30), (5, 9), (17, 9), (29, 9), (58, 9), (70, 9), (23, 9), (11, 9), (64, 9)])
    m.try_put('lm_bench', 13, 30, on='p'); m.try_put('lm_holo', 15, 27, on='p')
    # -------- the boulevard: the tram, shelters, lamps, the lift-grille
    m.put('lm_tram', 12, 34, force=True)
    m.try_put('lm_shelter', 31, 30, on='qp'); m.try_put('lm_shelter', 67, 31, on='qp')
    lamps(m, [(x, 32) for x in range(4, 84, 8)] + [(x, 38) for x in range(2, 84, 7)])
    for x in range(5, 83, 7):
        if m.free(x, 38, 2, 1, on='p'): m.try_put('lm_planter', x, 38, on='p')
    lamps(m, [(x, 46) for x in range(3, 83, 6)] + [(x, 57) for x in range(6, 83, 7)])
    rng = random.Random(7)
    for x in range(2, 82, 4):
        for y in (47, 58):
            if rng.random() < 0.5: m.try_put(rng.choice(['lm_bench', 'lm_planter', 'lm_topiary', 'lm_bollard', 'lm_news', 'lm_vent']), x, y, on='p')
    for x in range(1, 83, 4):
        if m.free(x, 46, 1, 1, on='p') and rng.random() < 0.6: m.over.append((2, x, 46, P1('lm_bulbs%d' % (x % 3))))
    # -------- the lawns on the lip
    for x in range(2, 82, 9): m.try_put('lm_tree', x, 59, on='.')
    for x in range(6, 82, 9): m.try_put('lm_bench', x, 60, on='.')
    for x in range(8, 82, 18): m.try_put('lm_viewer', x, 60, on='.')
    # -------- the east terrace down to the Lowlight
    for x, y in ((85, 39), (90, 39)): m.try_put('lm_tree', x, y, on='p')
    lamps(m, [(86, 45), (91, 45), (85, 55), (93, 50), (93, 60), (84, 61)])
    m.try_put('lm_steam0', 90, 53, on='p'); m.try_put('lm_vent', 90, 55, on='p'); m.try_put('lm_lift', 86, 59, on='p')
    m.try_put('lm_viewer', 92, 41, on='p')
    # -------- story events
    E = m.events
    seat(m, 180, 'Arrival', (6, 58))
    seat(m, 180, 'Pin-seller', (42, 19))
    seat(m, 180, 'Plaza banner', (37, 23))
    seat(m, 180, 'Gym sign', (14, 23))
    seat(m, 180, 'Gym attendant', (16, 23))
    seat(m, 180, 'Lift-grille', (75, 38))
    m.over.append((1, 74, 38, P1('lm_grate'))); m.over.append((1, 75, 38, P1('lm_grate')))
    seat(m, 180, 'Nadir Kid', (74, 38)); ST.EVENTS[180]['Grille scene']['_placed'] = True
    seat(m, 180, 'Zenith Officer', (77, 38))
    seat(m, 180, 'Office Worker', (33, 24))
    seat(m, 180, 'Old Man', (40, 28))
    seat(m, 180, 'Airship Spotter', (52, 15))
    seat(m, 180, 'Rotom Drone', (47, 30))
    seat(m, 180, 'Tourist from Briarwick', (39, 16))
    seat(m, 180, 'Meridian Lineman', (80, 24))
    seat(m, 180, 'Street Performer', (57, 22))
    ST.EVENTS[180]['Fizzbolt machine']['_placed'] = True          # the Trials overlay lays the machine (FIZZBOLT_MACHINE)
    seat(m, 180, 'P-3NNY kiosk', (60, 28))
    seat(m, 180, 'Council guard', (47, 7))
    seat(m, 180, 'Skyport guard', (74, 5))
    seat(m, 180, 'Spire guard', (83, 13))
    seat(m, 180, 'Lowlight stairs', (87, 46))
    seat(m, 180, 'Founders statue', (45, 29))
    E.append({'type': 'sign', 'name': 'Skyport sign', 'at': [76, 5], 'post': False, 'text': "SKYPORT TERRACE. TICKETED PASSENGERS. THE DAUNTLESS ARRIVES 18:00 FOR THE GALA."})
    E.append({'type': 'sign', 'name': 'Council sign', 'at': [49, 7], 'post': False, 'text': "COUNCIL WARD. THE FOUNDING HOUSES OF ZENITH. CLOSED TO THE PUBLIC FOR THE TENTH YEAR OF LIGHT."})
    E.append({'type': 'sign', 'name': 'Tram stop', 'at': [32, 32], 'post': False, 'text': "CONCOURSE STOP. TRAMS EVERY FOUR MINUTES. (A smaller sign: SUSPENDED FOR THE ANNIVERSARY PARADE.)"})
    E.append({'type': 'sign', 'name': 'Lip view', 'at': [9, 61], 'post': False, 'text': "Below the balustrade the cliff drops away into haze. Far down, Nadir's lamps glow orange, like a city at the bottom of a well."})
    E.append({'type': 'item', 'name': 'Item', 'at': [94, 61], 'item': 'XSPEED'})
    for e in E:
        x, y = e['at']
        m.keep_clear.add((x, y))
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)): m.keep_clear.add((x + dx, y + dy))
    scatter_wear(m, 10, on='pq', seed=1, kinds=(0, 1, 1, 2, 4, 4))
    m.paint()
    m.scatter(14, seed=4, on='.')
    m.seal_edges([('E', 52, 7)], filler=P1('lm_bollard'), sides='E')
    return m


HEAD180 = dict(id=180, name='Lumen City - The Concourse', parent=0, bgm='Cedolan City', rubric=True,
               metadata={'Outdoor': True, 'ShowArea': True, 'MapPosition': [0, 16, 16], 'Name': 'Lumen City'},
               connections=[{'dir': 'E', 'offset': 52, 'to': 181, 'to_offset': 4}],
               tone=[6, 4, 0, 0])


# ============================================================================================ 181 / 608 the Lowlight
RES_AT = {'Dex': (4, 7), 'Marta Vell': (13, 12), 'Old Jory': (15, 24), 'Nessa': (40, 25), 'Hob Carrow': (36, 13),
          'Linesman Aldo Fisk': (48, 7), 'Sukie': (7, 31), 'Ilo': (20, 37), 'Mattie': (21, 37), 'Gran Osk': (45, 31),
          'Benno': (24, 16), 'Mr Imrie': (11, 25)}


def build_lowlight(shattered=False):
    W, H = 60, 44
    m = City(W, H, 181 if not shattered else 608, base='l')
    m.ht[:] = 1; m.roof_kind = 'T'
    # the Spire's foot (north wall), the drop to Nadir (south and east)
    m.cls[0:3, :] = 'x'; m.ht[0:3, :] = 2
    m.cls[0:3, 0:8] = 'p'; m.ht[0:3, 0:8] = 1
    m.cls[41:, :] = 'x'; m.ht[41:, :] = 0
    m.cls[:, 57:] = 'x'; m.ht[:, 57:] = 0
    m.rect(0, 3, 8, 8, 'p')                                  # the landing at the foot of the Concourse steps
    # streets: Shadow Row (11-13), Market Row (24-26), the Edge Walk (37-39); Lift Lane (6-8), Pidove Steps (44-46)
    # blocks (doors on their bottom row) are packed with tenements and roofed over behind
    E = m.events
    reserve = {(47, y) for y in range(5, 11)} | {(48, y) for y in range(5, 11)} | {(49, y) for y in range(5, 11)}
    for x, y in reserve: m.taken[y, x] = True
    m.rect(22, 14, 14, 10, 'q')                              # Rook's crew square (an old cracked plaza)
    for x, y in ((9, 29), (10, 29), (9, 30), (10, 30), (9, 31), (10, 31)): m.taken[y, x] = True       # the lift cage
    placed = []
    placed += pack(m, 8, 46, 10, 5, PACK_LOW, seed=1)
    placed += pack(m, 50, 56, 10, 5, PACK_LOW, seed=2)
    placed += pack(m, 9, 21, 23, 14, PACK_LOW, seed=3)
    placed += pack(m, 36, 43, 23, 14, PACK_LOW, seed=4)
    placed += pack(m, 47, 56, 23, 14, PACK_LOW, seed=5)
    placed += pack(m, 11, 25, 36, 27, PACK_LOW, seed=6)
    placed += pack(m, 28, 43, 36, 27, PACK_LOW, seed=7)
    placed += pack(m, 47, 56, 36, 27, PACK_LOW, seed=8)
    placed += pack(m, 0, 5, 23, 14, PACK_LOW, seed=9)
    placed += pack(m, 0, 5, 36, 27, PACK_LOW, seed=10)
    for x, y in reserve: m.taken[y, x] = False
    for x, y in ((9, 29), (10, 29), (9, 30), (10, 30), (9, 31), (10, 31)): m.taken[y, x] = False
    m.put('lm_lift', 9, 29, force=True); m.over.append((1, 8, 31, P1('lm_grate')))
    door_events(m, placed, plaques=not shattered)
    # life of the street (both states); the living street only before the Shatter
    m.try_put('lm_noodles', 22, 14, on='q'); m.try_put('lm_cobbler', 13, 24, on='l')
    m.try_put('lm_ladder', 37, 12, on='l')
    m.over.append((2, 40, 24, P1('lm_wear5')))
    for x, y in ((12, 11), (28, 11), (17, 24), (32, 24), (49, 24), (16, 37), (34, 37)):
        if m.free(x, y, 3, 1, on='lq'): m.stamp('lm_washline', x, y)
    lamps(m, [(16, 13), (41, 13), (55, 12), (12, 26), (52, 26), (25, 39), (42, 39), (54, 39), (3, 12), (3, 39)], name='lm_arclamp_off')
    if not shattered:
        m.try_put('lm_stall_a', 28, 21, on='q'); m.try_put('lm_stall_c', 32, 14, on='q'); m.try_put('lm_stall_b', 49, 37, on='l')
        for x, y in ((24, 18), (33, 18)): m.try_put('lm_ring', x, y, on='q')
        m.try_put('lm_cam', 30, 19, on='q')
        m.over.append((2, 27, 19, P1('lm_cables'))); m.over.append((2, 28, 19, P1('lm_cables')))
    else:
        m.try_put('lm_junk0', 28, 21, on='q'); m.try_put('lm_junk3', 32, 15, on='q'); m.try_put('lm_junk0', 49, 37, on='l')
        for x, y in ((24, 18), (33, 18)): m.try_put('lm_ring', x, y, on='q')
    for x, y in ((54, 27), (53, 13), (5, 25)): m.try_put('lm_junk3', x, y, on='l')
    m.try_put('lm_steam0', 20, 25, on='l'); m.try_put('lm_vent', 26, 38, on='l')
    m.try_put('lm_junk1', 14, 38, on='l'); m.try_put('lm_junk2', 45, 38, on='l'); m.try_put('lm_junk1', 30, 12, on='l')
    m.try_put('lm_bench', 9, 24, on='l'); m.try_put('lm_viewer', 33, 39, on='l')
    if not shattered:
        for nm, at in RES_AT.items(): seat(m, 181, nm, at)
        seat(m, 181, 'Spark the Pichu', (3, 7))
        seat(m, 181, 'Rook', (28, 17)); seat(m, 181, 'Director', (25, 17)); seat(m, 181, 'Boom operator', (31, 18))
        for i, at in enumerate(((17, 13), (43, 12), (12, 38), (50, 5))):
            seat(m, 181, 'Junction box %d' % (i + 1), at)
        seat(m, 181, 'Blackout ends', (2, 4))
        seat(m, 181, 'Service door', (48, 4)); seat(m, 181, 'Lowlight lift', (8, 30))
        E.append({'type': 'item', 'name': 'HiddenItem', 'at': [55, 38], 'item': 'CELLBATTERY', 'hidden': True})
    else:
        for nm, at in RES_AT.items():
            g = next((gp for n, s_, d, l, gp in ST.RES if n == nm), 2)
            m.stamp('lm_fixed%d' % g, at[0], at[1] - 1)
            seat(m, 608, 'Glass ' + nm, at)
        seat(m, 608, 'Aftermath', (2, 4)); seat(m, 608, 'Rook (off camera)', (3, 9)); seat(m, 608, 'Valen at the Veil', (1, 6))
        seat(m, 608, 'Voss with the crate', (6, 9)); seat(m, 608, 'Testimony', (5, 5)); seat(m, 608, 'Spark the Pichu', (5, 7))
        seat(m, 608, 'Lowlight screen', (6, 3))
        # Back into the Plate Vault for Larch's 3 a.m. scene (Wave 0 softlock 2: every way in locked from CH5_STEP 9).
        E.append(dict(ev('Service door', page(["The vault's service door hangs open. Violet light behind it, and the smell of struck metal.",
                                               "(Directorate tape across it. Not now.)"]),
                         page(["(3 a.m. A note was waiting at the Center's desk, in a hand you know: \"Vault. Now. Bring your Flash. — I.L.\")",
                               {'se': 'Door exit'}, {'transfer': {'map': 952, 'x': 18, 'y': 16, 'dir': 'up'}}],
                              cond={'var': ['CH5_STEP', 11]}, trigger='action'),
                         page(["The vault's service door. Directorate seals on it now."], cond={'var': ['CH5_STEP', 12]})), at=[48, 4]))
        rng = random.Random(608)
        for y in range(3, 41):
            for x in range(0, 57):
                if m.cls[y, x] in 'lpq' and not m.taken[y, x] and rng.random() < 0.12 and (x, y) not in m.keep_clear:
                    m.over.append((2, x, y, P1('lm_bleed%d' % rng.randrange(3))))
        for y in range(3, 11): m.over.append((2, 0, y, P1('lm_veil%d' % (y % 3))))
        for y in range(4, 11):                                # back through the Veil to the Concourse's terrace
            E.append({'type': 'warp', 'name': 'The Veil %d' % y, 'at': [0, y], 'to': {'map': 180, 'x': 94, 'y': y + 48, 'dir': 'left'}})
    for e in E:
        x, y = e['at']
        m.keep_clear.add((x, y))
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)): m.keep_clear.add((x + dx, y + dy))
    scatter_wear(m, 6, on='lq', seed=2, kinds=(0, 1, 2))
    m.paint()
    sd = STAMPS['lm_sdoor']['layers']
    m.L[2, 3, 48] = next(sd[z][0][0] for z in range(3) if sd[z][0][0]); m.L[2, 4, 48] = next(sd[z][1][0] for z in range(3) if sd[z][1][0])
    m.seal_edges([('W', 4, 7)], filler=P1('lm_bollard'), sides='W')
    return m


def head_lowlight(shattered):
    if shattered:
        return dict(id=608, name='The Lowlight (Shattered)', parent=180, bgm='Underwater', rubric=True, field='BLEED',
                    metadata={'Outdoor': True, 'ShowArea': True, 'MapPosition': [0, 16, 16], 'Name': 'The Lowlight'},
                    tone=[-40, -50, 10, 60])
    return dict(id=181, name='Lumen City - The Lowlight', parent=180, bgm='Cedolan City', rubric=True,
                metadata={'Outdoor': True, 'ShowArea': True, 'MapPosition': [0, 16, 16], 'Name': 'The Lowlight'},
                connections=[{'dir': 'W', 'offset': 4, 'to': 180, 'to_offset': 52}],
                tone=[-24, -28, -8, 30])


def main(which):
    if 180 in which:
        m = build_180()
        m.write(180, dict(HEAD180, _file='180_lumen_concourse.yaml'),
                comment='# GENERATED by mapgen/layouts/lumen.py (map builder 15).  Edit the layout script, not this file.\n')
        print('180 unplaced:', ST.unplaced(180))
    for sh, mid in ((False, 181), (True, 608)):
        if mid in which:
            m = build_lowlight(sh)
            m.write(mid, dict(head_lowlight(sh), _file='%d_lumen_lowlight%s.yaml' % (mid, '' if not sh else '_shattered')),
                    comment='# GENERATED by mapgen/layouts/lumen.py (map builder 15).  Edit the layout script, not this file.\n')
            print(mid, 'unplaced:', ST.unplaced(mid))


if __name__ == '__main__':
    args = [int(a) for a in sys.argv[1:]] or [180, 181, 608]
    main(args)
