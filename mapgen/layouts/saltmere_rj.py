#!/usr/bin/env python3
"""Saltmere (140 / 146 / 147): the free port as a real harbour city.  Map builder 8, 2026-11-19 (replaces builder 7's
village-style version, kept as layouts/old_saltmere_rj_v1.py.txt).  Tileset 55 "PF Rejuv City" (cobbled streets,
flagged squares, the city kit from tdraw.py: kitbashed townhouses, shops, warehouses, civic fronts, quays, gates).

  140 The Upper Town (88x72): walled city on the bluff.  North Gate (to the Grey Saltings, closed until S108), East Gate
      (from Marram Down: the player's first view of the port), West Gate (the Frostflat Causeway).  Lantern Row, Gate
      Street, Chandlers' Way, Players' Lane; the market square with the fountain, the Lantern Theatre (Pageant Hall),
      the Lantern House, the Poke Center and Mart; ranks of townhouses wall to wall with alleys behind; the promenade
      on the sea wall above the white salt lake (salt pans, brine, heaps), a stair down to the pans, and two causeways
      over the lake: east to the Harbour (146), west to the Old Town (147).
  146 The Harbour (88x72): stone quays round a basin, the customs house (Harbour Office), warehouse row, cranes, fish
      market, ships at the moles, the Legion barge berth, the breakwater with the striped light.
  147 The Old Town (88x72): the Playhouse terrace and its square of playbills and lanterns, the Little Lantern, the
      costumiers' street, stepped lanes between terraces, the sea wall.

Story events: the old yaml events (layouts/old_14x_*_city.yaml) are re-seated by name; the Saltmere townsfolk, signs
and hidden items come from story/20_SCRIPT_CH0-2.md through scriptpour; the East Gate arrival and the North Gate warden
are written here.  Run: python3 -I layouts/saltmere_rj.py && python3 -I build.py --strict"""
import os, sys, math, random, re, copy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, yaml
import rkit as K
from rkit import C, STAMPS
from terrain import vnoise
import story_early as SE
HERE = K.HERE
OLD = {}
for fn in ('old_140_saltmere_city.yaml', 'old_146_saltmere_harbour_city.yaml', 'old_147_saltmere_oldtown_city.yaml'):
    for d in yaml.safe_load_all(open(os.path.join(HERE, 'layouts', fn))):
        if d: OLD[d['id']] = d

HOUSES = [n for n in STAMPS if n.startswith('th_')]
SHOPS = [n for n in STAMPS if n.startswith('sp_')]
WARES = [n for n in STAMPS if n.startswith('wh_')]
SZ = lambda n: (STAMPS[n]['w'], STAMPS[n]['h'])


def head(mid, fn, **kw):
    h = {k: v for k, v in OLD[mid].items() if k not in ('map', 'heights', 'stamps', 'tiles', 'tileblocks', 'events', 'palette', 'raw', 'tileset')}
    h.update(kw); h['rubric'] = True; h['yards_ok'] = True; h['_file'] = fn
    return h


def old_events(mid):
    ev = {}
    for e in OLD[mid].get('events', []):
        if e.get('type') == 'warp': continue
        key = e.get('name') or re.sub(r'[^A-Z ]', '', (e.get('text') or '').split('\n')[0].upper()).strip()
        e = dict(e); e.setdefault('name', key); ev[key] = e
    return ev


# ------------------------------------------------------------------ city kit helpers
def can_place(m, n, x, y):
    w, h = SZ(n)
    if x < 0 or y < 0 or x + w > m.W or y + h > m.H: return False
    if m.taken[y:y + h, x:x + w].any() or m.cliff[y:y + h, x:x + w].any(): return False
    if hasattr(m, 'bfoot') and m.bfoot[y:y + h, x:x + w].any(): return False
    sub = m.ht[y:y + h, x:x + w]
    return sub.min() == sub.max()


def put(m, n, x, y, link=None, dname=None):
    m.stamp(n, x, y, link, dname)
    w, h = SZ(n)
    sub = m.cls[y:y + h, x:x + w]; sub[sub == 'T'] = 'B'
    return (x + STAMPS[n]['door'][0], y + STAMPS[n]['door'][1]) if 'door' in STAMPS[n] else None


def rank(m, x0, x1, yb, pool, seed, maxh, minh=6, alley_every=0, last=None, back='c'):
    """buildings shoulder to shoulder from x0 to x1 (inclusive), every bottom row on yb (the street is yb+1).  Picks
    heights near maxh so the backs stay tight; leftover space above a lower roof becomes a back court (class `back`).
    alley_every: leave a 2-wide alley north through the rank about that often.  Returns placed (name, x, y)."""
    rng = random.Random(seed); x = x0; placed = []; since = 0; used = set()
    while x <= x1:
        room = x1 - x + 1
        if room < 3:
            m.rect(x, yb - 2, room, 3, back, only='.tT'); break
        if alley_every and since >= alley_every and room > 8:
            m.rect(x, yb - maxh + 1, 2, maxh, 'c', only='.tTB'); x += 2; since = 0; continue
        c = [n for n in pool if minh <= SZ(n)[1] <= maxh and SZ(n)[0] <= room and n != last and can_place(m, n, x, yb - SZ(n)[1] + 1)]
        if not c: x += 1; continue
        fits = [n for n in c if room - SZ(n)[0] == 0 or room - SZ(n)[0] >= 3]
        c = fits or c
        c.sort(key=lambda n: (abs(maxh - SZ(n)[1]) + (2 if n in used else 0) + rng.random() * 2.2))
        n = c[0]; w, h = SZ(n)
        put(m, n, x, yb - h + 1); placed.append((n, x, yb - h + 1)); used.add(n); last = n
        if h < maxh: m.rect(x, yb - maxh + 1, w, maxh - h, back, only='.tT')
        x += w; since += w
    return placed


def block(m, x0, x1, ytop, yb, pool, seed, alley_every=14):
    """fill a block whose south edge is street row yb+1: ranks from the bottom up with 2-row alleys between them"""
    depth = yb - ytop + 1; k = 0
    while depth >= 6:
        if depth <= 11: hmax = depth
        elif depth < 14: hmax = depth - 8 if depth - 8 >= 6 else depth          # leave room for an alley and a 6-row rank
        else: hmax = min(10, depth - 8)
        rank(m, x0, x1, yb, pool, seed + k, hmax, minh=max(6, min(hmax, 6)), alley_every=alley_every)
        yb -= hmax
        if depth - hmax >= 8:
            m.rect(x0, yb - 1, x1 - x0 + 1, 2, 'c', only='.tTB')               # the back alley
            yb -= 2
        depth = yb - ytop + 1; k += 1
    if depth > 0: m.rect(x0, ytop, x1 - x0 + 1, depth, 'c', only='.tT')


def courts(m, seed):
    """back courts (cobbled class c with no building): laundry lines, barrels, crates, a tree or a well"""
    rng = random.Random(seed)
    props = ['hb_washline', 'hb_barrels', 'hb_crates4', 'hb_boxes', 'hb_cask', 'hb_keg', 'hb_barrel', 'hb_rugline', 'sh_crates', 'hb_tubs']
    for y in range(m.H):
        for x in range(m.W):
            if m.cls[y, x] == 'c' and not m.taken[y, x] and rng.random() < 0.05:
                n = rng.choice(props); w, h = SZ(n)
                if m.free(x, y, w, h, on='c') and not m.cliff[y:y + h, x:x + w].any():
                    m.stamp(n, x, y)


def lamps(m, pts, on='cf'):
    for x, y in pts:
        if m.free(x, y - 1, 1, 2, on=on) and not m.cliff[y - 1:y + 1, x].any(): m.stamp('gl_lamp', x, y - 1)


def props(m, items, on='cf', r=2):
    for n, x, y in items:
        w, h = SZ(n); ok = False
        for d in range(r + 1):
            for yy in range(y - d, y + d + 1):
                for xx in range(x - d, x + d + 1):
                    if not ok and max(abs(xx - x), abs(yy - y)) == d and m.free(xx, yy, w, h, on=on) and not m.cliff[yy:yy + h, xx:xx + w].any():
                        m.stamp(n, xx, yy); ok = True
        if not ok: print('  (no room for %s near %d,%d)' % (n, x, y))


def overs(m, n, x, y):
    """lay a stamp's tiles as over-tiles (decals and overhead strings that need no footprint)"""
    L = np.array(STAMPS[n]['layers'])
    for z in range(3):
        for dy in range(L.shape[1]):
            for dx in range(L.shape[2]):
                t = int(L[z, dy, dx])
                if t: m.over.append((z, x + dx, y + dy, t))


def seat(m, e, x, y, on='cf.', r=6):
    e = dict(e); e['at'] = list(m.snap(x, y, on, r=r)); m.taken[e['at'][1], e['at'][0]] = True
    if e.get('type') == 'sign' and e.get('post', True):
        e['post'] = False; m.tile(C('sh', 4847 - 4448), e['at'][0], e['at'][1], 1)
    return e


def salt_lake(m, box, seed):
    """white salt flats (class S) with brine pans and heaps inside box"""
    x0, y0, x1, y1 = box; rng = random.Random(seed)
    m.rect(x0, y0, x1 - x0 + 1, y1 - y0 + 1, 'S', only='w')
    return rng


def paint_salt(m, seed):
    rng = random.Random(seed)
    salt = [K.P1('salt%d' % i) for i in range(4)]
    for y, x in np.argwhere(m.cls == 'S'):
        m.L[0, y, x] = salt[0] if rng.random() < 0.55 else rng.choice(salt); m.L[1, y, x] = 0
    for kind in ('f2',):                                         # quay faces standing on salt get the dry footing
        pass


def brine_pans(m, x0, y0, nx, ny, pw=4, ph=2, gap=1):
    """rectangular salt pans on the flats: brine with clay bunds"""
    for j in range(ny):
        for i in range(nx):
            px, py = x0 + i * (pw + gap), y0 + j * (ph + gap)
            if not (m.cls[py:py + ph, px:px + pw] == 'S').all() or m.taken[py:py + ph, px:px + pw].any(): continue
            for yy in range(py, py + ph):
                for xx in range(px, px + pw):
                    v = ('n' if yy == py else 's' if yy == py + ph - 1 else '') + ('w' if xx == px else 'e' if xx == px + pw - 1 else '')
                    v = {'': 'c', 'nw': 'nw', 'ne': 'ne', 'sw': 'sw', 'se': 'se', 'n': 'n', 's': 's', 'w': 'w', 'e': 'e'}.get(v, v)
                    if ph == 1: v = 'ns' if pw == 1 else ('w' if xx == px else 'e' if xx == px + pw - 1 else 'ns')
                    m.tile(K.P1('brine_' + v), xx, yy, 1); m.cls[yy, xx] = 'B'


def dry_footings(m):
    """quay faces (f2 = wet base) standing on salt flats or paving get the dry footing course instead"""
    wet = {K.P1('qy_f2w0'): K.P1('rw_f2w0'), K.P1('qy_f2m0'): K.P1('rw_f2m0'), K.P1('qy_f2e0'): K.P1('rw_f2e0'),
           K.P1('qy_f2m1'): K.P1('rw_f2m0')}
    eff = getattr(m, 'eff', m.cls)
    for z in (1, 2):
        for y, x in np.argwhere(np.isin(m.L[z], list(wet))):
            if m.cls[y, x] in 'Scf' or eff[y, x] in 'Scf': m.L[z, y, x] = wet[int(m.L[z, y, x])]


def boats(m, items):
    for n, x, y in items:
        L = np.array(STAMPS[n]['layers']); hh, ww = L.shape[1:]
        if all(m.cls[y + j, x + i] == 'w' and m.L[2, y + j, x + i] == 0 for i in range(ww) for j in range(hh)):
            for j in range(hh):
                for i in range(ww):
                    t = int(L[:, j, i].max())
                    if t: m.L[2, y + j, x + i] = t


def townsfolk():
    """the script's Saltmere townsfolk (scriptpour), keyed by name"""
    fl, _, _ = SE.parsed(r'^### Flavor townsfolk \(Saltmere', r'^\*\[after S108')
    return {n['name']: SE.npc_from(n, move='random' if n['name'] in ('Busker', 'Child with an Ogre puppet', 'Hound Number Two') else 'fixed') for n in fl}


TOWN_SIGN = "SALTMERE - The Free Port.\nAnswers to the Accord and to No Crown. (Booing Tuesdays.)"


def arrival_event():
    """first entry by the East Gate (script: Map 140 Arrival).  The tax-barge business is told, not animated."""
    P = SE.P
    cmds = [{'se': 'Horse'}, '(Lamplit promenades along a white salt lake, striped awnings, salt-caramel smoke. A long green barge flying Elowen\'s briar crown rows across the lake toward the harbour mouth.)',
            {'se': 'Applause'}, 'The Breakwater: BOOOOOOOOOOOO.', '(The green barge turns, slowly, and rows away.)',
            P('JUNO', 'deadpan', "That's the Queen's tax-barge. They do that every week. It's tradition. The barge comes, everyone boos, the barge goes."),
            P('JUNO', 'neutral', 'Mum says it\'s the only time in history a tax has been defeated by noise.'),
            P('JUNO', 'happy', "I'm taking the tarts to the Lantern Theatre! Find me on the green after. Don't go into the gym without me! I need to be AUDIENCE!"),
            {'script': 'pfm_set(:sm_arrived)'}, {'selfswitch': ['A', True]}]
    return {'type': 'event', 'name': 'Arrival (East Gate)', 'pages': [
        {'trigger': 'autorun', 'cond': {}, 'commands': [{'if': '!pfm?(:sm_arrived) && $game_player.x >= 80', 'then': cmds, 'else': [{'selfswitch': ['A', True]}]}]},
        {'cond': {'self': 'A'}, 'commands': []}]}


def gate_warden(x):
    return {'type': 'event', 'name': 'Gate Warden', 'pages': [
        {'graphic': {'sprite': 'trainer_GENTLEMAN', 'dir': 'down'}, 'commands': [
            'Gate Warden: The North Gate is shut while the Pageant runs. Accord orders: nobody leaves with a full purse or an empty seat.',
            'Gate Warden: Come back when the curtain\'s down. The Saltings road isn\'t going anywhere. It never does.']},
        {'cond': {'switch': 'CH3_PAGEANT_DONE'}, 'graphic': {'sprite': 'trainer_GENTLEMAN', 'dir': 'left'}, 'commands': [
            'Gate Warden: The gate\'s open. After last night... mind the Grey Saltings. And mind who you talk to.']}]}


# ====================================================================================================== 140
def build_140(prev=None):
    W, H = 88, 72
    m = K.RMap(W, H, 55, 140, water='Ocean', kit={1: 'qy', 2: 'qy'}); m.keep_under = 'cfS'
    m.cls[:, :] = 'T'
    LAKE = 58
    m.ht[:LAKE, :] = 1
    m.cls[LAKE:, :] = 'w'
    # causeways over the salt lake (stay at the city's height): west to the Old Town, east to the Harbour
    for cx in (9, 56):
        m.ht[LAKE:, cx:cx + 6] = 1; m.cls[LAKE:, cx:cx + 6] = 'f'
    salt_lake(m, (17, LAKE + 2, 52, H - 1), 140)
    salt_lake(m, (66, LAKE + 6, 87, H - 1), 141)
    m.stairs(30, LAKE - 1, w=3, kit_rows=3, c='c')                                     # down the sea wall onto the pans
    m.plan_cliffs()
    # ---- streets and squares (all at h=1)
    S = lambda x, y, w, h, c='c': m.rect(x, y, w, h, c, only='T.')
    S(43, 0, 6, 26)                                                                  # Gate Street from the North Gate
    S(0, 10, 88, 3)                                                                  # Lantern Row
    S(0, 31, 27, 4)                                                                  # West Street to the West Gate
    S(62, 44, 26, 4)                                                                 # East Street from the East Gate
    S(19, 13, 3, 37)                                                                 # Chandlers' Way
    S(68, 13, 3, 31)                                                                 # Players' Lane
    m.rect(26, 25, 36, 17, 'f', only='T.c')                                          # the market square
    m.rect(40, 42, 10, 8, 'f', only='T.c')                                           # the Fountain Steps down to the promenade
    m.rect(0, 50, 88, LAKE - 50, 'f', only='T.c')                                    # the promenade on the sea wall
    m.rect(62, 44, 26, 6, 'c', only='T.')                                            # the East Gate esplanade
    m.blob(39, 53.5, 4.2, 2.2, '.', seed=7, rough=0.2, only='f')                     # the promenade green (J1)
    # ---- gates and civic fronts
    put(m, 'gt_gate6', 40, 0)
    for x, y in ((84, 38), (84, 48)): put(m, 'gt_tower', x, y)                      # the East Gate towers
    for x, y in ((0, 25), (0, 35)): put(m, 'gt_tower', x, y)                        # the West Gate towers
    d = {}
    d['pageant'] = put(m, 'cv_lantern', 29, 24 - 9 + 1, 'SM_PAGEANT', 'Pageant Hall door')
    d['pc'] = put(m, 'cv_pc', 52, 24 - 7 + 1, 'SM_PC', 'Poke Center door')
    d['mart'] = put(m, 'cv_mart', 60, 24 - 6 + 1, 'SM_MART', 'Mart door')
    d['house1'] = put(m, 'sp_salt', 22, 49 - 6 + 1, 'SM_HOUSE1', 'House door')      # Sella the Saltwife, on the promenade
    lh = put(m, 'th_af', 25, 24 - 8 + 1)                                              # the Lantern House (map 148, Trials): door kept clear
    # ---- blocks of townhouses (bottom rows on the street below), alleys behind
    pool = HOUSES + SHOPS
    block(m, 0, 39, 0, 9, HOUSES, 11)                                                # north of Lantern Row, west of the gate
    block(m, 52, 87, 0, 9, HOUSES, 12)
    block(m, 0, 18, 13, 30, pool, 13)                                                # above West Street
    block(m, 22, 24, 13, 24, HOUSES, 14)
    block(m, 49, 51, 13, 24, HOUSES, 15)
    block(m, 66, 67, 13, 43, HOUSES, 16)
    block(m, 71, 83, 13, 43, pool, 17)
    block(m, 84, 87, 13, 37, HOUSES, 18)
    block(m, 0, 18, 37, 49, pool, 19)                                                # above the promenade, west
    block(m, 22, 39, 42, 49, SHOPS + HOUSES, 20)
    block(m, 50, 61, 42, 49, SHOPS + HOUSES, 21)
    block(m, 62, 67, 26, 43, pool, 22)
    m.rect(25, 13, 4, 12, 'c', only='T.')                                            # what is left becomes cobbled courts
    m.cls[m.cls == 'T'] = 'c'
    # ---- events
    E = []
    E += [{'type': 'warp', 'at': [cx + i, H - 1], 'to': {'map': 146 if cx == 56 else 147, 'x': (42 if cx == 56 else 40) + i, 'y': 1, 'dir': 'retain'}}
          for cx in (9, 56) for i in range(6)]
    ev = old_events(140); tf = townsfolk()
    E.append(seat(m, {'type': 'sign', 'name': 'Town sign', 'text': TOWN_SIGN}, 82, 43))
    E.append(seat(m, {'type': 'sign', 'name': 'North Gate sign', 'text': 'NORTH GATE - The Grey Saltings, the Dyers\' Ford and the weaving country.'}, 42, 9))
    E.append(seat(m, {'type': 'sign', 'name': 'West Gate sign', 'text': 'WEST GATE - The Frostflat Causeway. (Chained at the Border Stones by order of Isenmar customs.)'}, 4, 30))
    E.append(seat(m, {'type': 'sign', 'name': 'Harbour causeway sign', 'text': 'THE HARBOUR CAUSEWAY - Quays, the Harbour Office and the breakwater.'}, 55, 56))
    E.append(seat(m, {'type': 'sign', 'name': 'Old Town causeway sign', 'text': "THE PLAYERS' CAUSEWAY - The Old Town, the Pell Playhouse and the Little Lantern."}, 15, 56))
    E.append(seat(m, {'type': 'sign', 'name': 'Pageant poster', 'text': '"THE PAGEANT OF THE PRISMFALL - a Gift of Love from the Original One. Festival Year: Opening Night! With the companion piece THE LOYAL THREE. By leave of the Accord."'}, 41, 26))
    E.append(seat(m, {'type': 'sign', 'name': 'Festival poster', 'text': "The same poster as the Landing's. The painted Crown's stone has the same tiny dark fleck. Nobody here has bothered to circle it."}, 50, 26))
    E.append(seat(m, {'type': 'sign', 'name': 'Promenade lamps', 'text': 'Oil lamps on iron posts. Each has a number, and a playbill pasted to it.'}, 64, 52))
    E.append(seat(m, ev['Juno J1'], 39, 53, '.f'))
    E.append(seat(m, ev['Royal notice'], 47, 41, 'f'))
    E.append(seat(m, ev['Kestrel'], 44, 27, 'f'))
    E.append(seat(m, ev['Eevee breeder'], 58, 38, 'f'))
    E.append(seat(m, gate_warden(45), 45, 9, 'c'))
    E.append(seat(m, arrival_event(), 85, 46, 'c'))
    for n, x, y in (('Caramel Seller', 33, 38), ('Busker', 54, 33), ('Lamplighter', 72, 53), ('Child with an Ogre puppet', 36, 34),
                    ('Retired Actor on a bench', 28, 52), ('Hound Number Two', 49, 52), ('Grey Pilgrim', 60, 54), ('Accord Inspector', 37, 27),
                    ('Meridian Clerk', 55, 27), ('Fishwife', 66, 46)):
        E.append(seat(m, tf[n], x, y))
    E.append(seat(m, SE.hidden('HiddenItem lemonade', 'LEMONADE', 'Someone was saving it for the interval.'), 34, 39, 'f'))
    E.append(seat(m, {'type': 'npc', 'name': 'Woman from the ferry', 'sprite': 'NPC 13', 'dir': 'down', 'text':
                      "Woman from the ferry: You! From the Dovetail! I'm home! I'm not grey anymore. Look at me. I'm BEIGE.\nWoman from the ferry: Blank tint. Saltmere. The gate said so. My sister cried."}, 76, 46))
    m.events += E
    for e in E: m.taken[e['at'][1], e['at'][0]] = True
    for x, y in K.incoming(140): m.taken[y, x] = True
    if lh: m.taken[lh[1], lh[0]] = True; m.taken[min(H - 1, lh[1] + 1), lh[0]] = True
    # ---- the square and the promenade: fountain, stalls, benches, lamps, playbill columns, planters
    props(m, (('pf_fountain', 42, 30),), on='f', r=0)
    props(m, (('pf_stall0', 29, 36), ('pf_stall1', 35, 36), ('pf_stall2', 52, 36), ('pf_stall3', 57, 34), ('pf_stall4', 29, 30),
              ('pf_stall2', 56, 29), ('pf_morris', 39, 28), ('pf_morris', 50, 28), ('pf_logbench', 41, 36), ('pf_logbench', 46, 36),
              ('hb_crates4', 31, 33), ('hb_barrels', 59, 38), ('hb_tables', 33, 27), ('gl_tables', 47, 39)), on='f')
    props(m, (('pf_stall1', 6, 51), ('pf_stall3', 66, 51), ('pf_logbench', 26, 55), ('pf_logbench', 46, 55), ('pf_logbench', 62, 55),
              ('pf_logbench', 74, 55), ('pf_morris', 18, 51), ('pf_morris', 52, 51), ('hb_fishstall', 78, 51), ('hb_tubs', 70, 50),
              ('pf_stall0', 82, 51), ('hb_rope', 3, 55)), on='f')
    props(m, (('pf_morris', 66, 45), ('hb_cask', 75, 44), ('hb_barrels', 64, 48)), on='c')
    lamps(m, [(x, 51) for x in range(5, 86, 8)] + [(42, 26), (49, 26), (27, 26), (60, 26), (27, 40), (60, 40), (40, 44), (49, 44),
                                                    (46, 13), (42, 22), (49, 22), (20, 30), (72, 43), (10, 30), (80, 43), (66, 30)])
    for x in range(44, 48): overs(m, 'pf_lstring%d' % (x % 3), x, 12)                 # lantern strings over Lantern Row
    for x in range(20, 27): overs(m, 'pf_lstring%d' % (x % 3), x, 30)
    for x in range(71, 84): overs(m, 'pf_lstring%d' % (x % 3), x, 43)
    courts(m, 140)
    # ---- the salt lake: pans, heaps, rakes; boats on the open water
    brine_pans(m, 18, LAKE + 3, 7, 3, pw=4, ph=2)
    brine_pans(m, 67, LAKE + 8, 4, 2, pw=4, ph=2)
    props(m, (('hb_salt0', 21, 69), ('hb_salt1', 34, 69), ('hb_salt2', 46, 69), ('hb_salt0', 75, 68), ('hb_salt1', 82, 66),
              ('hb_barrel', 40, 69), ('hb_tubs', 26, 69)), on='S', r=2)
    print('  140 courts / props done')
    m.beds(prefixes=('th_', 'sp_')) if False else None
    m.paint()
    paint_salt(m, 140); dry_footings(m)
    boats(m, (('hb_boat1', 3, 61), ('hb_boat3', 64, 60), ('hb_boat2', 70, 61), ('hb_boat4', 3, 66), ('hb_boat1', 78, 61)))
    m.scatter(6, seed=140, on='.')
    conn = [{'dir': 'N', 'offset': 43, 'to': 541, 'to_offset': 12}, {'dir': 'W', 'offset': 31, 'to': 560, 'to_offset': 12},
            {'dir': 'E', 'offset': 44, 'to': 528, 'to_offset': 38}]
    h = head(140, '140_saltmere.yaml', biome='harbour', tone=[8, 4, -12, 0], connections=conn,
             fog={'name': 'prismfall_seamist', 'opacity': 30, 'blend': 0, 'zoom': 100, 'sx': 2, 'sy': 0})
    m.write(140, h, "# Saltmere - The Upper Town (140). WRITTEN BY layouts/saltmere_rj.py (PF Rejuv City, tileset 55) - edit that script.\n")
    if prev: m.preview(prev, 0.5)
    return d


def main():
    a = sys.argv[1:]
    which = [x for x in a if x.isdigit()] or ['140', '146', '147']
    out = {}
    if '140' in which: out[140] = build_140('/tmp/b8/s140.png' if '--preview' in a else None)
    if '146' in which and 'build_146' in globals(): out[146] = build_146('/tmp/b8/s146.png' if '--preview' in a else None)
    if '147' in which and 'build_147' in globals(): out[147] = build_147('/tmp/b8/s147.png' if '--preview' in a else None)
    if 140 in out:                                                       # 141's HealingSpot follows the PC door
        x, y = out[140]['pc']; p = os.path.join(HERE, 'specs', '141_saltmere_interiors.yaml')
        s = open(p).read(); s = re.sub(r'HealingSpot: \[140, \d+, \d+\]', 'HealingSpot: [140, %d, %d]' % (x, y + 1), s); open(p, 'w').write(s)
    print('doors', out)


if __name__ == '__main__':
    main()
