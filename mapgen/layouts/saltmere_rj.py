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
    if np.isin(m.cls[y:y + h, x:x + w], list('wWsS')).any(): return False
    sub = m.ht[y:y + h, x:x + w]
    return sub.min() == sub.max()


def put(m, n, x, y, link=None, dname=None):
    """a building: its cells keep cobble underneath (no grass verge round the block)"""
    w, h = SZ(n)
    sub = m.cls[y:y + h, x:x + w]; sub[np.isin(sub, ['T', '.'])] = 'c'
    d = m.stamp(n, x, y, link, dname)
    if d: m.under[d[1], d[0]] = 'c'
    return (x + STAMPS[n]['door'][0], y + STAMPS[n]['door'][1]) if 'door' in STAMPS[n] else None


def rank(m, x0, x1, yb, pool, seed, maxh, minh=6, alley_every=0, last=None, setback=0.0):
    """buildings shoulder to shoulder from x0 to x1 (inclusive), bottom rows on yb (the street is yb+1).  Heights near
    maxh keep the backs tight; leftover space above a lower roof is back court.  alley_every: a 2-wide alley north
    through the rank about that often.  setback: chance a house stands one row back behind a stoop."""
    rng = random.Random(seed); x = x0; placed = []; since = 0; used = set()
    while x <= x1:
        room = x1 - x + 1
        if room < 3: break
        if alley_every and since >= alley_every and room > 8:
            m.court[yb - maxh + 1:yb + 1, x:x + 2] = True; m.alleys.append((x, yb - maxh + 1, 2, maxh)); x += 2; since = 0; continue
        sb = 1 if setback and rng.random() < setback else 0
        c = [n for n in pool if minh <= SZ(n)[1] <= maxh - sb and SZ(n)[0] <= room and n != last and can_place(m, n, x, yb - sb - SZ(n)[1] + 1)]
        if not c and sb:
            sb = 0; c = [n for n in pool if minh <= SZ(n)[1] <= maxh and SZ(n)[0] <= room and n != last and can_place(m, n, x, yb - SZ(n)[1] + 1)]
        if not c: x += 1; continue
        fits = [n for n in c if room - SZ(n)[0] == 0 or room - SZ(n)[0] >= 3]
        c = fits or c
        c.sort(key=lambda n: (abs(maxh - sb - SZ(n)[1]) + (2 if n in used else 0) + rng.random() * 2.2))
        n = c[0]; w, h = SZ(n)
        put(m, n, x, yb - sb - h + 1); placed.append((n, x, yb - sb - h + 1)); used.add(n); last = n
        x += w; since += w
    return placed


def block(m, x0, x1, ytop, yb, pool, seed, alley_every=14, setback=0.15):
    """fill a block whose south edge is street row yb+1: ranks from the bottom up with 2-row back alleys between them;
    every cell not built on becomes a cobbled back court (props, laundry, a well)"""
    m.rect(x0, ytop, x1 - x0 + 1, yb - ytop + 1, 'c', only='T.')
    m.court[ytop:yb + 1, x0:x1 + 1] |= (m.cls[ytop:yb + 1, x0:x1 + 1] == 'c')
    depth = yb - ytop + 1; k = 0
    while depth >= 6:
        if depth <= 11: hmax = depth
        elif depth < 14: hmax = depth - 8 if depth - 8 >= 6 else depth
        else: hmax = min(10, depth - 8)
        rank(m, x0, x1, yb, pool, seed + k, hmax, minh=max(6, min(hmax, 6)), alley_every=alley_every, setback=setback if k == 0 else 0)
        yb -= hmax
        if depth - hmax >= 8:
            m.alleys.append((x0, yb - 1, x1 - x0 + 1, 2)); yb -= 2
        depth = yb - ytop + 1; k += 1


def gardens(m, seed, trees=('tr_oak', 'tr_oak2', 'tr_teal', 'tr_pink', 'tr_oak')):
    """leftover block interiors (behind lower roofs, under terrace walls, block corners) become walled gardens:
    grass with fruit trees and shrubs, the alleys and doorsteps stay cobbled"""
    keep = np.zeros_like(m.court)
    for x, y, w, h in m.alleys: keep[y:y + h, x:x + w] = True
    for e in m.events:
        if e.get('type') == 'door': x, y = e['at']; keep[y:y + 3, max(0, x - 1):x + 2] = True
    street = np.isin(m.cls, ['c', 'f']) & ~m.court
    pad = np.pad(street, 1); near = sum(np.roll(np.roll(pad, dy, 0), dx, 1)[1:-1, 1:-1] for dy in (-1, 0, 1) for dx in (-1, 0, 1)) > 0
    g = m.court & (m.cls == 'c') & ~m.taken & ~m.cliff & ~keep & ~near
    from collections import deque
    seen = np.zeros_like(g)
    for y0, x0 in np.argwhere(g):
        if seen[y0, x0]: continue
        comp = []; q = deque([(y0, x0)]); seen[y0, x0] = True
        while q:
            y, x = q.popleft(); comp.append((y, x))
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                Y, X = y + dy, x + dx
                if 0 <= Y < m.H and 0 <= X < m.W and g[Y, X] and not seen[Y, X]: seen[Y, X] = True; q.append((Y, X))
        if len(comp) >= 8:
            for y, x in comp: m.cls[y, x] = '.'
    m.autotrees(400, list(trees), on='.', seed=seed, gap=1)
    return int(g.sum())


def parapets(m, kind='rw', rows=None, skip=()):
    """a balustrade (kind 'rw', stone) or an iron railing ('qy') along every south lip of a terrace or sea wall, with
    pier posts at the run ends; stairs, causeways and `skip` cells stay open.  rows: only lips on these rows."""
    st = set()
    for sx, sy, sw, sn in m.stairs_at:
        for xx in range(sx - 0, sx + sw): st.add((xx, sy))
    lip = np.zeros((m.H, m.W), bool)
    for y in range(m.H - 1):
        if rows and y not in rows: continue
        for x in range(m.W):
            if m.ht[y + 1, x] < m.ht[y, x] and (x, y) not in st and (x, y) not in skip and not m.taken[y, x] \
                    and m.ht[y, max(0, x - 1)] == m.ht[y, x] and m.ht[y, min(m.W - 1, x + 1)] == m.ht[y, x]:
                lip[y, x] = True
    for y, x in np.argwhere(lip):
        e = 'w' if not lip[y, max(0, x - 1)] or x == 0 else 'e' if x == m.W - 1 or not lip[y, x + 1] else 'm'
        overs(m, '%s_rail_%s' % (kind, e), x, y, z=2); m.taken[y, x] = True


def pavements(m):
    """a flagged pavement along the foot of every rank of buildings on a cobbled street (the Kugearen habit: a
    sidewalk strip between the house fronts and the carriageway)"""
    for n, x, y in m.stamps:
        if not n.startswith(('th_', 'sp_', 'wh_', 'cv_')): continue
        w, h = SZ(n); yy = y + h
        if yy >= m.H: continue
        for xx in range(x, x + w):
            if m.cls[yy, xx] == 'c' and not m.court[yy, xx] and not m.cliff[yy, xx]: m.cls[yy, xx] = 'f'


def street_trees(m, pts, kinds=('tr_oak2', 'tr_oak', 'tr_teal')):
    """plane trees standing in the paving (trunk on the flags)"""
    rng = random.Random(len(pts))
    for x, y in pts:
        k = rng.choice(kinds); st = STAMPS[k]; ok = False
        for d in range(4):
            for dy in range(-d, d + 1):
                for dx in range(-d, d + 1):
                    tx, ty = x + dx - st['w'] // 2, y + dy - st['h'] + 1
                    if not ok and max(abs(dx), abs(dy)) == d and m.can_tree(k, tx, ty, on='fc') \
                            and not m.taken[y + dy:y + dy + 2, max(0, tx - 1):tx + st['w'] + 1].any():
                        m.stamp(k, tx, ty, mark='B'); ok = True
        if not ok: print('  (no room for a street tree at %d,%d)' % (x, y))


def glints(m, seed, p=0.10):
    rng = random.Random(seed); G = [K.P1('hb_glint%d' % i) for i in range(4)]
    for y, x in np.argwhere(np.isin(m.cls, ['w', 'W'])):
        if m.L[1, y, x] == 0 and m.L[2, y, x] == 0 and rng.random() < p * (0.4 + vnoise(x, y, seed, 6.0)):
            m.L[2, y, x] = rng.choice(G)


def courts(m, seed, p=0.07):
    """back courts and alleys (m.court): laundry lines, barrels, crates, casks, a well-tub"""
    rng = random.Random(seed)
    props = ['hb_washline', 'hb_barrels', 'hb_crates4', 'hb_boxes', 'hb_cask', 'hb_keg', 'hb_barrel', 'hb_rugline', 'hb_tubs', 'hb_barrel2', 'hb_boxes2', 'hb_rugline2']
    cells = [tuple(c) for c in np.argwhere(m.court & np.isin(m.cls, ['c', '.']) & ~m.taken)]
    rng.shuffle(cells)
    for y, x in cells:
        if rng.random() > p * 3: continue
        n = rng.choice(props); w, h = SZ(n)
        if m.free(x, y, w, h, on='c.') and not m.cliff[y:y + h, x:x + w].any() and m.court[y:y + h, x:x + w].all() \
                and not m.taken[max(0, y - 1):y + h + 1, max(0, x - 1):x + w + 1].any():
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


def overs(m, n, x, y, z=None):
    """lay a stamp's tiles as over-tiles (decals and overhead strings that need no footprint)"""
    L = np.array(STAMPS[n]['layers'])
    for zz in range(3):
        for dy in range(L.shape[1]):
            for dx in range(L.shape[2]):
                t = int(L[zz, dy, dx])
                if t: m.over.append((zz if z is None else z, x + dx, y + dy, t))


def string_lights(m, x0, x1, y):
    for x in range(x0, x1 + 1): overs(m, 'pf_lstring%d' % (x % 3), x, y, z=2)


def seat(m, e, x, y, on='cf.', r=6):
    e = dict(e); e['at'] = list(m.snap(x, y, on, r=r)); m.taken[e['at'][1], e['at'][0]] = True
    if e.get('type') == 'sign' and e.get('post', True):
        e['post'] = False; m.tile(C('sh', 4847 - 4448), e['at'][0], e['at'][1], 1)
    return e


def door_props(m, rng, items=('hb_barrel', 'hb_cask', 'hb_keg', 'hb_boxes', 'hb_barrel2'), p=0.5):
    """a barrel or crate beside shop doors (never in front of a door)"""
    for e in m.events:
        if e.get('type') != 'door' and not e.get('name', '').endswith(' door'): continue
    for nm, x, y in list(m.stamps):
        if not nm.startswith(('sp_', 'wh_')) or 'door' not in STAMPS[nm]: continue
        dx, dy = STAMPS[nm]['door']; X, Y = x + dx, y + dy
        for side in (-2, 2, -1, 1):
            n = rng.choice(items); w, h = SZ(n)
            yy = Y + 1 - h + 1 if h > 1 else Y + 1
            xx = X + side
            if rng.random() < p and m.free(xx, Y + 1, w, 1, on='cf') and abs(xx - X) >= 1:
                if h == 1: m.stamp(n, xx, Y + 1); break


NPC_LINES = ["Mind your purse. Not because of thieves. Because of the caramel.", "Three plays tonight and I've tickets to two. Choices!",
             "My grandmother booed a Queen's barge in AF 92. She still has the voice for it.", "Salt's up a copper a sack. Blame the weather. Everyone does.",
             "The Lantern's doing the Loyal Three again. I could recite it. I have. At dinner.", "Don't stand under the gulls by the fish stalls.",
             "Dorian waved at me once. From a balcony. I think it was at me.", "The free port's free. The rent isn't.",
             "My cousin's in the Hound chorus. He says 'GRR' professionally.", "You can tell an outlander by the way they look up at the roofs.",
             "If you get lost, walk downhill. Everything in Saltmere ends at the water.", "They paint the playbills fresh every morning. The rain washes them by noon.",
             "Lamplighter's late. He's always late. The lamps forgive him.", "That's real salt on the steps, not frost. Mind your footing.",
             "Meridian wants to put glowing glass in the lamps. The Warden said the lamps have tenure.", "Fresh mackerel! Ordinary mackerel! Very ordinary!",
             "I came for a week. That was eleven years ago.", "The gate shuts at the Pageant. Tradition. Nobody remembers why. Probably a play."]


def crowd(m, cells, n, seed, on='cf', sprites=None, moving=0.6):
    """townsfolk filling a street or square: random walkers and loiterers with a line each"""
    rng = random.Random(seed); out = []
    sprites = sprites or ['NPC %02d' % i for i in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23)]
    cells = list(cells); rng.shuffle(cells)
    for x, y in cells:
        if len(out) >= n: break
        if not (m.inb(x, y) and m.cls[y, x] in on and not m.taken[max(0, y - 1):y + 2, max(0, x - 1):x + 2].any() and not m.cliff[y, x]): continue
        e = {'type': 'npc', 'name': 'Townsfolk %d' % (len(out) + 1), 'sprite': rng.choice(sprites), 'dir': rng.choice(['down', 'left', 'right', 'up']),
             'move': 'random' if rng.random() < moving else 'fixed', 'text': rng.choice(NPC_LINES), 'at': [x, y]}
        m.taken[y, x] = True; out.append(e)
    m.events += out
    return out


def salt_lake(m, box, seed):
    """white salt flats (class S) inside box (only over water)"""
    x0, y0, x1, y1 = box
    m.rect(x0, y0, x1 - x0 + 1, y1 - y0 + 1, 'S', only='w')


def paint_salt(m, seed):
    rng = random.Random(seed)
    salt = [K.P1('salt%d' % i) for i in range(4)]
    for y, x in np.argwhere(m.cls == 'S'):
        m.L[0, y, x] = salt[0] if rng.random() < 0.55 else rng.choice(salt); m.L[1, y, x] = 0


def brine_pans(m, x0, y0, x1, y1, seed, pw=(3, 6), ph=(2, 3)):
    """salt pans of uneven size on the flats (rows of brine with clay bunds, staggered like real salterns), leaving
    raking paths between them"""
    rng = random.Random(seed); y = y0
    while y < y1:
        h = rng.randint(*ph); x = x0 + rng.randint(0, 2)
        while x < x1:
            w = rng.randint(*pw)
            if x + w <= x1 and y + h <= y1 and (m.cls[y:y + h, x:x + w] == 'S').all() and not m.taken[y:y + h, x:x + w].any():
                for yy in range(y, y + h):
                    for xx in range(x, x + w):
                        v = ('n' if yy == y else 's' if yy == y + h - 1 else '') + ('w' if xx == x else 'e' if xx == x + w - 1 else '')
                        v = v or 'c'
                        m.tile(K.P1('brine_' + v), xx, yy, 1); m.cls[yy, xx] = 'B'
            x += w + rng.choice((1, 1, 2))
        y += h + 1


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
        if all(m.inb(x + i, y + j) and m.cls[y + j, x + i] in 'wW' and m.L[2, y + j, x + i] == 0 for i in range(ww) for j in range(hh)):
            for j in range(hh):
                for i in range(ww):
                    t = int(L[:, j, i].max())
                    if t: m.L[2, y + j, x + i] = t
        else: print('  (no water for %s at %d,%d)' % (n, x, y))


def ship(m, dx, dy):
    """the moored two-master (ship_art 'moored', the Dovetail's sister hull) at offset dx, dy: hull solid on layer 2,
    rigging overhead on layer 3; the hull cells become class B"""
    for x, y, z, t in K.SHIP:
        x += dx; y += dy
        if m.inb(x, y):
            m.L[1 if z == 0 else 2, y, x] = t
            if z == 0: m.taken[y, x] = True


def ship_cells(dx, dy):
    return [(x + dx, y + dy) for x, y, z, t in K.SHIP if z == 0]


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
def new_map(mid, kit):
    W, H = 88, 72
    m = K.RMap(W, H, 55, mid, water='Ocean', kit=kit); m.keep_under = 'cfS'
    m.court = np.zeros((H, W), bool); m.alleys = []
    return m


def keep_door_clear(m, d, rows=2):
    if d:
        x, y = d
        for k in range(1, rows + 1):
            if m.inb(x, y + k): m.taken[y + k, x] = True


def finish(m, seed, lamp_pts=(), on_crowd=None):
    courts(m, seed)


def build_140(prev=None):
    W, H = 88, 72
    m = new_map(140, {1: 'qy', 2: 'rw'})
    m.cls[:, :] = 'T'
    LAKE = 59
    m.ht[:, :] = 1
    m.ht[:12, :] = 2                                                                 # the High Town terrace (lip on row 11)
    m.ht[LAKE:, :] = 0; m.cls[LAKE:, :] = 'w'
    for cx in (9, 56):                                                               # causeways over the salt lake
        m.ht[LAKE:, cx:cx + 6] = 1; m.cls[LAKE:, cx:cx + 6] = 'f'
    salt_lake(m, (17, LAKE + 2, 52, H - 1), 140)
    salt_lake(m, (65, LAKE + 4, 87, H - 1), 141)
    # ---- stairs first (they cut the wall lines): Gate Street, Chandlers' Way, Players' Lane, the pan stair
    m.stairs(43, 11, w=6, kit_rows=3, c='c')
    m.stairs(19, 11, w=3, kit_rows=3, c='c')
    m.stairs(68, 11, w=3, kit_rows=3, c='c')
    m.stairs(31, LAKE - 1, w=3, kit_rows=3, c='c')
    m.stairs(74, LAKE - 1, w=3, kit_rows=3, c='c')
    m.plan_cliffs()
    S = lambda x, y, w, h, c='c': m.rect(x, y, w, h, c, only='T.')
    S(43, 0, 6, 26)                                                                  # Gate Street from the North Gate
    S(0, 8, 88, 4)                                                                   # Lantern Row (High Town)
    S(0, 31, 22, 4)                                                                  # West Street to the West Gate
    S(64, 44, 24, 4)                                                                 # East Street from the East Gate
    S(19, 12, 3, 38)                                                                 # Chandlers' Way
    S(68, 12, 3, 32)                                                                 # Players' Lane
    m.rect(22, 25, 42, 17, 'f', only='T.c')                                          # the market square
    m.rect(40, 42, 10, 8, 'f', only='T.c')                                           # the Fountain Walk to the promenade
    m.rect(0, 50, 88, LAKE - 50, 'f', only='T.c')                                    # the promenade on the sea wall
    m.rect(64, 48, 24, 2, 'c', only='T.')
    m.blob(37, 53.6, 4.6, 2.0, '.', seed=7, rough=0.25, only='f')                   # the promenade green (J1)
    m.blob(13, 53.5, 2.6, 1.6, '.', seed=8, rough=0.3, only='f')                    # little greens with planes
    m.blob(63, 53.5, 2.8, 1.6, '.', seed=9, rough=0.3, only='f')
    # ---- gates and civic fronts
    put(m, 'gt_gate6', 40, 0)
    for x, y in ((85, 38), (85, 48)): put(m, 'gt_tower', x, y)                      # the East Gate towers
    for x, y in ((0, 25), (0, 35)): put(m, 'gt_tower', x, y)                        # the West Gate towers
    d = {}
    d['pageant'] = put(m, 'cv_lantern', 28, 16, 'SM_PAGEANT', 'Pageant Hall door')
    d['lantern'] = put(m, 'th_af', 24, 17, 'SM_LANTERN', 'Lantern House door')     # map 148 (Trials, Sister Hollin)
    d['pc'] = put(m, 'cv_pc', 51, 18, 'SM_PC', 'Poke Center door')
    d['mart'] = put(m, 'cv_mart', 59, 19, 'SM_MART', 'Mart door')
    d['house1'] = put(m, 'sp_salt', 23, 44, 'SM_HOUSE1', 'House door')              # Sella the Saltwife, on the promenade
    put(m, 'gt_tower', 40, 18)                                                       # the old bell tower beside the Lantern
    for k in d.values(): keep_door_clear(m, k)
    # ---- blocks of townhouses wall to wall, alleys and back courts behind
    pool = HOUSES + SHOPS
    block(m, 0, 39, 0, 7, HOUSES, 11, alley_every=16)                                # High Town, west of the gate
    block(m, 52, 87, 0, 7, HOUSES + ['sp_books', 'sp_cost'], 12, alley_every=16)
    block(m, 0, 18, 14, 30, pool, 13)                                                # above West Street
    block(m, 22, 42, 14, 24, HOUSES, 14)
    block(m, 49, 67, 14, 24, SHOPS, 15)
    block(m, 71, 87, 14, 43, pool, 17, alley_every=10)
    block(m, 0, 18, 35, 49, pool, 19)                                                # above the promenade, west
    block(m, 22, 39, 42, 49, SHOPS + HOUSES, 20)
    block(m, 50, 63, 42, 49, SHOPS, 21)
    block(m, 64, 67, 25, 43, HOUSES, 22)
    m.cls[m.cls == 'T'] = 'c'
    pavements(m)
    m.blob(43.5, 32, 6.5, 4.6, 'c', seed=21, rough=0.0, only='f'); m.blob(43.5, 32, 4.4, 3.2, 'f', seed=22, rough=0.0, only='c')
    # ---- events
    E = []
    E += [{'type': 'warp', 'at': [cx + i, H - 1], 'to': {'map': 146 if cx == 56 else 147, 'x': (42 if cx == 56 else 40) + i, 'y': 1, 'dir': 'retain'}}
          for cx in (9, 56) for i in range(6)]
    ev = old_events(140); tf = townsfolk()
    E.append(seat(m, {'type': 'sign', 'name': 'Town sign', 'text': TOWN_SIGN}, 80, 43))
    E.append(seat(m, {'type': 'sign', 'name': 'North Gate sign', 'text': 'NORTH GATE - The Grey Saltings, the Dyers\' Ford and the weaving country.'}, 42, 9))
    E.append(seat(m, {'type': 'sign', 'name': 'West Gate sign', 'text': 'WEST GATE - The Frostflat Causeway. (Chained at the Border Stones by order of Isenmar customs.)'}, 4, 30))
    E.append(seat(m, {'type': 'sign', 'name': 'Harbour causeway sign', 'text': 'THE HARBOUR CAUSEWAY - Quays, the Harbour Office and the breakwater.'}, 55, 56))
    E.append(seat(m, {'type': 'sign', 'name': 'Old Town causeway sign', 'text': "THE PLAYERS' CAUSEWAY - The Old Town, the Pell Playhouse and the Little Lantern."}, 15, 56))
    E.append(seat(m, {'type': 'sign', 'name': 'Pageant poster', 'text': '"THE PAGEANT OF THE PRISMFALL - a Gift of Love from the Original One. Festival Year: Opening Night! With the companion piece THE LOYAL THREE. By leave of the Accord."'}, 38, 26))
    E.append(seat(m, {'type': 'sign', 'name': 'Festival poster', 'text': "The same poster as the Landing's. The painted Crown's stone has the same tiny dark fleck. Nobody here has bothered to circle it."}, 50, 26))
    E.append(seat(m, {'type': 'sign', 'name': 'Promenade lamps', 'text': 'Oil lamps on iron posts. Each has a number, and a playbill pasted to it.'}, 66, 52))
    E.append(seat(m, {'type': 'sign', 'name': 'Bell tower', 'text': 'THE SALT BELL. Rung for the tax-barge, for fire, and for curtain-up. Mostly for curtain-up.'}, 42, 25))
    E.append(seat(m, ev['Juno J1'], 37, 53, '.f'))
    E.append(seat(m, ev['Royal notice'], 47, 41, 'f'))
    E.append(seat(m, ev['Kestrel'], 36, 27, 'f'))
    E.append(seat(m, ev['Eevee breeder'], 58, 38, 'f'))
    E.append(seat(m, gate_warden(45), 46, 9, 'c'))
    E.append(seat(m, arrival_event(), 85, 46, 'c'))
    for n, x, y in (('Caramel Seller', 30, 38), ('Busker', 54, 33), ('Lamplighter', 72, 53), ('Child with an Ogre puppet', 36, 34),
                    ('Retired Actor on a bench', 28, 55), ('Hound Number Two', 49, 52), ('Grey Pilgrim', 60, 55), ('Accord Inspector', 37, 29),
                    ('Meridian Clerk', 55, 27), ('Fishwife', 66, 46)):
        E.append(seat(m, tf[n], x, y))
    E.append(seat(m, SE.hidden('HiddenItem lemonade', 'LEMONADE', 'Someone was saving it for the interval.'), 31, 39, 'f'))
    E.append(seat(m, {'type': 'npc', 'name': 'Woman from the ferry', 'sprite': 'NPC 13', 'dir': 'down', 'text':
                      "Woman from the ferry: You! From the Dovetail! I'm home! I'm not grey anymore. Look at me. I'm BEIGE.\nWoman from the ferry: Blank tint. Saltmere. The gate said so. My sister cried."}, 76, 46))
    E.append(seat(m, {'type': 'npc', 'name': 'Salt raker', 'sprite': 'NPC 19', 'dir': 'up', 'move': 'random', 'text':
                      'Salt raker: Rake it white, stack it high, sell it to people who think it tastes of something.'}, 40, 66, 'S'))
    m.events += E
    for e in E: m.taken[e['at'][1], e['at'][0]] = True
    for x, y in K.incoming(140): m.taken[y, x] = True
    # ---- the square: the fountain on its flagged dais, stalls in two arcs, benches, columns, lamps
    props(m, (('pf_fountain', 41, 30), ('pf_hounds', 43, 37)), on='f', r=0)
    props(m, (('pf_planter0', 40, 42), ('pf_planter1', 48, 42), ('pf_planter2', 40, 46), ('pf_planter3', 48, 46), ('pf_well', 30, 26),
              ('pf_planter1', 23, 25), ('pf_planter2', 61, 25), ('pf_planter0', 27, 49), ('pf_planter3', 59, 49)), on='fc', r=1)
    props(m, (('pf_stall0', 25, 36), ('pf_stall1', 29, 37), ('pf_stall4', 25, 29), ('pf_stall2', 33, 38), ('pf_stall3', 25, 32),
              ('pf_stall2', 55, 36), ('pf_stall0', 59, 33), ('pf_stall1', 59, 29), ('pf_stall4', 51, 38), ('pf_stall3', 59, 37),
              ('pf_morris', 39, 28), ('pf_morris', 47, 28), ('pf_morris', 39, 37), ('pf_morris', 47, 37),
              ('pf_logbench', 40, 36), ('pf_logbench', 44, 36), ('pf_logbench', 36, 32), ('pf_logbench', 48, 32),
              ('hb_crates4', 29, 34), ('hb_barrels', 32, 34), ('hb_tables', 52, 29), ('gl_tables', 33, 28), ('hb_boxes', 55, 31),
              ('hb_cask', 62, 40), ('hb_barrel', 23, 40), ('hb_washline', 23, 26)), on='f')
    # ---- the promenade: stalls, benches, columns, the fish market by the harbour causeway
    props(m, (('pf_stall1', 4, 51), ('pf_stall3', 68, 51), ('pf_logbench', 26, 56), ('pf_logbench', 46, 56), ('pf_logbench', 66, 56),
              ('pf_logbench', 80, 56), ('pf_logbench', 6, 56), ('pf_morris', 18, 51), ('pf_morris', 52, 51), ('pf_morris', 82, 51),
              ('hb_fishstall', 76, 50), ('hb_tubs', 71, 50), ('pf_stall0', 30, 51), ('hb_rope', 3, 56), ('hb_barrels', 54, 51),
              ('pf_stall2', 44, 51), ('hb_crates4', 58, 51)), on='f')
    props(m, (('pf_morris', 66, 45), ('hb_cask', 75, 45), ('hb_barrels', 64, 48), ('pf_morris', 10, 33), ('hb_boxes', 16, 31)), on='c')
    for x, y in ((12, 53), (64, 53)): m.trees(x, y, 1, ['tr_oak2', 'tr_teal'], r=1, on='.')
    lamps(m, [(x, 51) for x in range(5, 86, 8)] + [(x, 57) for x in range(9, 86, 12)] + [(42, 26), (49, 26), (23, 26), (62, 26), (23, 41), (62, 41),
              (40, 43), (49, 43), (46, 12), (42, 22), (49, 22), (18, 30), (72, 43), (10, 30), (80, 43), (67, 30), (8, 12), (30, 12), (58, 12), (80, 12)])
    string_lights(m, 23, 42, 25); string_lights(m, 49, 62, 25)                       # lantern strings along the civic fronts
    string_lights(m, 20, 23, 30); string_lights(m, 71, 84, 43); string_lights(m, 0, 18, 49)
    for x in (29, 35, 54, 60): overs(m, 'hb_banner', x, 22) if False else None
    parapets(m, 'rw', rows=(11,)); parapets(m, 'qy', rows=(LAKE - 1,))
    street_trees(m, [(8, 57), (20, 57), (32, 57), (50, 57), (70, 57), (84, 57), (25, 29), (61, 30), (24, 40), (61, 40), (2, 33), (82, 46)])
    gardens(m, 140); courts(m, 140)
    # ---- the salt lake: uneven pans with raking paths, heaps, tubs; boats on the open water
    brine_pans(m, 18, LAKE + 3, 52, H - 1, 140)
    brine_pans(m, 66, LAKE + 5, 87, H - 1, 141, pw=(3, 5))
    props(m, (('hb_salt0', 21, 69), ('hb_salt1', 34, 69), ('hb_salt2', 46, 68), ('hb_salt0', 75, 69), ('hb_salt1', 82, 66),
              ('hb_barrel', 40, 69), ('hb_tubs', 26, 69), ('hb_salt2', 28, 62), ('hb_salt0', 69, 65)), on='S', r=3)
    # ---- crowd: the square and the promenade are full on Pageant week
    sq = [(x, y) for y in range(26, 41) for x in range(23, 63)]
    pr = [(x, y) for y in range(51, 57) for x in range(2, 86)]
    crowd(m, sq, 12, 1401); crowd(m, pr, 10, 1402); crowd(m, [(x, y) for y in range(8, 11) for x in range(0, 88)], 4, 1403, on='c')
    m.paint()
    paint_salt(m, 140); dry_footings(m); glints(m, 140)
    boats(m, (('hb_boat1', 2, 61), ('hb_boat3', 2, 66), ('hb_boat2', 62, 61), ('hb_boat4', 79, 60), ('hb_boat1', 5, 69)))
    m.scatter(5, seed=140, on='.')
    m.seal_edges([('N', 43, 6), ('W', 31, 4), ('E', 44, 4)], keep=[tuple(e['at']) for e in m.events if e.get('type') == 'warp'] + [(x, H - 1) for x in range(W)])
    conn = [{'dir': 'N', 'offset': 43, 'to': 541, 'to_offset': 12}, {'dir': 'W', 'offset': 31, 'to': 560, 'to_offset': 12},
            {'dir': 'E', 'offset': 44, 'to': 528, 'to_offset': 38}]
    h = head(140, '140_saltmere.yaml', biome='harbour', tone=[8, 4, -12, 0], connections=conn,
             fog={'name': 'prismfall_seamist', 'opacity': 30, 'blend': 0, 'zoom': 100, 'sx': 2, 'sy': 0})
    m.write(140, h, "# Saltmere - The Upper Town (140). WRITTEN BY layouts/saltmere_rj.py (PF Rejuv City, tileset 55) - edit that script.\n")
    if prev: m.preview(prev, 0.5)
    return d


# ====================================================================================================== 146
def build_146(prev=None):
    """The Harbour: the causeway lands on the quay town; Harbour Square and the customs house; warehouse row on Quay
    Street with cranes; the basin between the West Mole and the East Mole with two ships moored; the fish market;
    the Legion barge berth; the breakwater with the striped light at its end"""
    W, H = 88, 72
    m = new_map(146, {1: 'qy', 2: 'rw'})
    m.cls[:, :] = 'w'; m.ht[:, :] = 0
    TOWN0, QUAY = 6, 36                                                              # town plateau rows 6..36 (lip 36)
    m.ht[TOWN0:QUAY + 1, :] = 1; m.cls[TOWN0:QUAY + 1, :] = 'T'
    m.ht[:TOWN0, 42:48] = 1; m.cls[:TOWN0, 42:48] = 'f'                            # the causeway from the Upper Town
    m.ht[QUAY + 1:59, 0:10] = 1; m.cls[QUAY + 1:59, 0:10] = 'f'                     # the West Mole
    m.ht[QUAY + 1:63, 78:88] = 1; m.cls[QUAY + 1:63, 78:88] = 'f'                   # the East Mole
    m.ht[60:63, 24:88] = 1; m.cls[60:63, 24:88] = 'f'                               # the breakwater
    m.ht[55:63, 20:27] = 1; m.cls[55:63, 20:27] = 'f'                               # the light's footing at its west end
    m.cls[63:, :] = 'W'; m.cls[64:, :] = 'W'
    m.blob(80, 68, 6, 3, 'w', seed=3, only='W'); m.blob(12, 66, 8, 4, 'w', seed=4, only='W')
    m.rect(0, 0, 37, 4, 'S', only='w'); m.blob(10, 4, 6, 1.4, 'S', seed=8, only='w')                # the salt lake's last flats
    # ---- stairs: down to the boat steps on both moles, onto the breakwater's landing
    m.stairs(30, QUAY, w=3, kit_rows=3, c='c')
    m.plan_cliffs()
    S = lambda x, y, w, h, c='c': m.rect(x, y, w, h, c, only='T.')
    S(42, TOWN0, 6, 16)                                                              # Customs Street (the causeway's end)
    S(0, TOWN0, 88, 3)                                                               # the Rope Walk along the lake wall
    S(18, 9, 2, 24); S(70, 9, 2, 24)                                                 # Net Lane, Tar Lane
    m.rect(30, 22, 31, 11, 'f', only='T.c')                                         # Harbour Square
    m.rect(0, 33, 88, 4, 'f', only='T.c')                                           # Quay Street (the apron)
    # ---- civic: the customs house (Harbour Office) on the square; the fish market hall
    d = {}
    d['office'] = put(m, 'cv_customs', 50, 14, 'SM_HARBOUR', 'Harbour Office door')
    keep_door_clear(m, d['office'])
    put(m, 'gt_tower', 30, 16)                                                       # the harbour bell tower
    # ---- warehouse row on Quay Street, shops and lodgings behind
    block(m, 0, 17, 9, 32, WARES + SHOPS, 31, alley_every=0, setback=0)
    block(m, 20, 41, 9, 21, HOUSES + SHOPS, 32, alley_every=12)
    block(m, 20, 29, 22, 32, WARES, 33, alley_every=0, setback=0)
    block(m, 48, 49, 9, 21, HOUSES, 34)
    block(m, 60, 69, 9, 21, SHOPS + HOUSES, 35)
    block(m, 61, 69, 22, 32, WARES, 36, alley_every=0, setback=0)
    block(m, 72, 87, 9, 32, WARES + ['sp_tav', 'sp_inn', 'sp_fish', 'sp_chand'], 37, alley_every=0, setback=0)
    m.cls[m.cls == 'T'] = 'c'
    pavements(m)
    # ---- events
    E = [{'type': 'warp', 'at': [42 + i, 0], 'to': {'map': 140, 'x': 56 + i, 'y': 70, 'dir': 'retain'}} for i in range(6)]
    ev = old_events(146); tf = townsfolk()
    E.append(seat(m, {'type': 'sign', 'name': 'Harbour Office sign', 'text': 'SALTMERE HARBOUR OFFICE\nAll ferries suspended by order of the Accord. Dues payable within. Biscuits are not a bribe.'}, d['office'][0] + 2, d['office'][1] + 1, 'f'))
    E.append(seat(m, {'type': 'sign', 'name': 'Breakwater sign', 'text': ev.get('THE BREAKWATER', {}).get('text') or "THE BREAKWATER. By tradition, the Queen's barge is booed from here. Please boo responsibly."}, 30, 61, 'f'))
    E.append(seat(m, {'type': 'sign', 'name': 'Quay sign', 'text': 'QUAY STREET - The West Mole, the fish market and the boat steps. East: the Legion berth and the breakwater.'}, 44, 32, 'f'))
    E.append(seat(m, ev['Stevedore'], 26, 34, 'f'))
    E.append(seat(m, ev['Old angler'], 8, 57, 'f'))
    E.append(seat(m, ev['Salt raker'], 36, 8, 'c'))
    for n, x, y in (('Fisherman', 4, 45), ('Old Sailor', 84, 40), ('Stagehand on a smoke break', 38, 27)):
        if n in tf: E.append(seat(m, tf[n], x, y))
    E.append(seat(m, SE.hidden('HiddenItem stardust', 'STARDUST', 'It blew in on the salt.'), 23, 61, 'f'))
    E.append(seat(m, {'type': 'npc', 'name': 'Legion recruiter', 'sprite': 'NPC 21', 'dir': 'left', 'text':
                      "Legion recruiter: The Ashkaar Legion pays in coin and glory! ...Mostly coin. The glory's on back order."}, 80, 47, 'f'))
    m.events += E
    for e in E: m.taken[e['at'][1], e['at'][0]] = True
    for x, y in K.incoming(146): m.taken[y, x] = True
    brine_pans(m, 1, 0, 36, 4, 146, pw=(3, 5), ph=(2, 2))
    props(m, (('hb_salt1', 30, 1), ('hb_salt0', 14, 2)), on='S', r=2)
    # ---- the square and the quay: cranes, freight, the fish market, nets, bollards; the berth and the breakwater
    props(m, (('hb_crane', 22, 31), ('hb_crane', 34, 31), ('hb_crane', 58, 31), ('hb_crane', 66, 31)), on='f', r=2)
    props(m, (('pf_fountain', 43, 25), ('pf_stall0', 32, 25), ('pf_stall2', 32, 29), ('hb_fishstall', 52, 23), ('pf_stall3', 56, 28),
              ('hb_tubs', 36, 29), ('pf_logbench', 40, 31), ('pf_logbench', 48, 31), ('pf_morris', 40, 23), ('pf_well', 58, 24),
              ('hb_fish', 49, 27), ('hb_tables', 36, 23)), on='f')
    props(m, (('hb_crates4', 3, 33), ('hb_boxes', 9, 34), ('hb_barrels', 16, 33), ('hb_boxes2', 21, 34), ('hb_cask', 28, 33),
              ('hb_crates4', 60, 33), ('hb_barrels', 64, 34), ('hb_boxes', 68, 33), ('hb_keg', 77, 34), ('hb_crates4', 81, 33),
              ('hb_rugline', 6, 40), ('hb_washline', 3, 50), ('hb_boxes2', 6, 54), ('hb_tubs', 2, 42),
              ('sh_campfire', 81, 49), ('hb_rope', 84, 51), ('hb_banner', 86, 44), ('hb_banner', 79, 44), ('hb_barrels', 85, 55),
              ('hb_crates4', 40, 61), ('hb_rope', 50, 61), ('hb_crates4', 66, 61), ('pf_logbench', 58, 61)), on='f')
    for x in (2, 12, 20, 27, 37, 44, 52, 60, 68, 76, 86):
        if not (30 <= x <= 32): overs(m, 'hb_bollard%d' % (x % 2), x, QUAY, z=2); m.taken[QUAY, x] = True
    for y in (40, 46, 52): overs(m, 'hb_bollard0', 9, y, z=2); overs(m, 'hb_bollard1', 78, y + 2, z=2)
    props(m, (('hb_fishstall', 2, 44), ('hb_tubs', 6, 47), ('hb_fish', 2, 49), ('hb_crates4', 4, 52), ('hb_barrel', 7, 55)), on='f')
    lamps(m, [(x, 33) for x in range(6, 86, 10)] + [(x, 60) for x in range(30, 86, 9)] + [(8, 40), (8, 50), (79, 40), (79, 56), (42, 12), (47, 12),
              (31, 22), (60, 22), (10, 8), (30, 8), (60, 8), (80, 8)])
    string_lights(m, 30, 41, 22); string_lights(m, 72, 87, 32)
    gardens(m, 146); courts(m, 146)
    sq = [(x, y) for y in range(22, 33) for x in range(30, 61)]; qy = [(x, y) for y in range(33, 36) for x in range(0, 88)]
    crowd(m, sq, 8, 1461); crowd(m, qy, 8, 1462); crowd(m, [(x, y) for y in range(37, 62) for x in range(78, 88)], 3, 1463)
    parapets(m, 'qy', rows=(5,))
    m.paint(); dry_footings(m)
    ship(m, 21, -11); ship(m, -6, -11)                                               # two ships alongside Quay Street
    boats(m, (('hb_boat1', 40, 47), ('hb_boat2', 46, 52), ('hb_boat3', 36, 55), ('hb_boat4', 14, 62), ('hb_boat1', 62, 64),
              ('hb_boat2', 70, 56), ('hb_boat3', 10, 4), ('hb_boat4', 60, 2)))
    boats(m, (('ak_rock2', 50, 67), ('ak_boulder', 4, 65), ('ak_rock2', 33, 66), ('ak_rock2', 72, 4) if False else ('ak_rock2', 12, 0),
              ('ak_rock2', 84, 66), ('ak_rock2', 64, 1)))
    m.stamps.append(('lighthouse', 21, 46))
    for dy in range(9, 16): m.taken[46 + dy, 21:26] = True
    L = np.array(STAMPS['lighthouse']['layers'])
    for z in range(3):
        for dy in range(L.shape[1]):
            for dx in range(L.shape[2]):
                t = int(L[z, dy, dx])
                if t: m.L[2 if 46 + dy < 56 else max(1, z), 46 + dy, 21 + dx] = t
    paint_salt(m, 146); glints(m, 146, p=0.3)
    h = head(146, '146_saltmere_harbour.yaml', biome='harbour', tone=[6, 4, -8, 0], connections=[],
             fog={'name': 'prismfall_seamist', 'opacity': 36, 'blend': 0, 'zoom': 100, 'sx': 2, 'sy': 0})
    m.write(146, h, "# Saltmere - The Harbour (146). WRITTEN BY layouts/saltmere_rj.py (PF Rejuv City, tileset 55) - edit that script.\n")
    if prev: m.preview(prev, 0.5)
    return d


# ====================================================================================================== 147
def build_147(prev=None):
    """The Old Town on its hill above the sea: the Players' Causeway lands at the Players' Gate on Mask Row (h3);
    stepped lanes down to Curtain Lane (h2), where the Pell Playhouse stands on its terrace above a grand stair with the
    Little Lantern and the costumiers beside it; the Theatre Square below (h1) with playbill columns, stalls, lanterns
    and the crowd; the seafront street on the sea wall."""
    W, H = 88, 72
    m = new_map(147, {1: 'qy', 2: 'rw', 3: 'rw'})
    m.cls[:, :] = 'T'
    m.ht[:, :] = 1
    m.ht[:19, :] = 3; m.ht[19:39, :] = 2
    m.ht[:7, :] = 0; m.cls[:7, :] = 'w'
    m.ht[:7, 39:47] = 3; m.cls[:7, 39:47] = 'f'                                    # the Players' Causeway (copings at 39 / 46)
    m.ht[61:, :] = 0; m.cls[61:, :] = 'w'; m.cls[66:, :] = 'W'
    m.blob(20, 69, 10, 3, 'w', seed=5, only='W'); m.blob(70, 70, 9, 3, 'w', seed=6, only='W')
    # ---- stairs: Gate Steps, Mask Steps, the grand stair, Curtain Steps, the boat steps
    m.stairs(41, 18, w=4, kit_rows=3, c='c'); m.stairs(9, 18, w=3, kit_rows=3, c='c'); m.stairs(77, 18, w=3, kit_rows=3, c='c')
    m.stairs(38, 38, w=12, kit_rows=3, c='f')
    m.stairs(10, 38, w=3, kit_rows=3, c='c'); m.stairs(76, 38, w=3, kit_rows=3, c='c')
    m.stairs(56, 60, w=3, kit_rows=3, c='c')
    m.plan_cliffs()
    S = lambda x, y, w, h, c='c': m.rect(x, y, w, h, c, only='T.')
    S(40, 7, 6, 12)                                                                  # under the Players' Gate
    S(0, 15, 88, 4)                                                                  # Mask Row (h3)
    S(0, 36, 88, 3)                                                                  # Curtain Lane (h2)
    S(9, 21, 3, 15); S(77, 21, 3, 15)                                                # the Mask Steps lanes
    m.rect(34, 34, 20, 4, 'f', only='T.c')                                          # the Playhouse forecourt
    m.rect(18, 41, 52, 10, 'f', only='T.c')                                         # the Theatre Square (h1)
    S(10, 41, 3, 17); S(76, 41, 3, 17)
    m.rect(0, 57, 88, 4, 'f', only='T.c')                                           # the seafront on the sea wall
    # ---- the gate, the Playhouse, the Little Lantern
    put(m, 'gt_gate6', 37, 7)
    d = {}
    d['gym'] = put(m, 'pf_playhouse2', 36, 21, 'SM_GYM', 'Playhouse door')
    keep_door_clear(m, d['gym'])
    d['little'] = put(m, 'cv_little', 57, 29)
    keep_door_clear(m, d['little'])
    put(m, 'sp_cost', 25, 28); put(m, 'sp_masks', 29, 29)                             # the costumiers beside the Playhouse
    # ---- blocks
    block(m, 0, 36, 7, 14, HOUSES, 41, alley_every=12)
    block(m, 49, 87, 7, 14, HOUSES + ['sp_books'], 42, alley_every=12)
    block(m, 0, 8, 19, 35, HOUSES + SHOPS, 43, alley_every=0)
    block(m, 12, 33, 19, 35, HOUSES + ['sp_cost', 'sp_masks', 'sp_cafe', 'sp_tav'], 44, alley_every=10)
    block(m, 54, 76, 19, 35, HOUSES + ['sp_cafe', 'sp_books'], 45, alley_every=10)
    block(m, 80, 87, 19, 35, HOUSES, 46, alley_every=0)
    block(m, 0, 9, 41, 56, HOUSES + SHOPS, 47, alley_every=0)
    block(m, 13, 17, 41, 56, HOUSES, 48, alley_every=0)
    block(m, 18, 69, 51, 56, SHOPS + ['th_s', 'th_t', 'th_u', 'th_v', 'th_w', 'th_y', 'th_m', 'th_q', 'th_d'], 49, alley_every=14)
    block(m, 70, 75, 41, 56, HOUSES, 50, alley_every=0)
    block(m, 79, 87, 41, 56, HOUSES + SHOPS, 51, alley_every=0)
    m.cls[m.cls == 'T'] = 'c'
    pavements(m)
    m.blob(43.5, 45.5, 8.5, 3.6, 'c', seed=23, rough=0.0, only='f'); m.blob(43.5, 45.5, 6.0, 2.2, 'f', seed=24, rough=0.0, only='c')
    # ---- events
    E = [{'type': 'warp', 'at': [40 + i, 0], 'to': {'map': 140, 'x': 9 + i, 'y': 70, 'dir': 'retain'}} for i in range(6)]
    ev = old_events(147); tf = townsfolk()
    E.append(seat(m, {'type': 'sign', 'name': 'Playhouse sign', 'text': 'THE PELL PLAYHOUSE - SALTMERE GYM. WARDEN: DORIAN PELL.\n"Every pageant is a lie. The trick is choosing which lie to tell."'}, d['gym'][0] - 3, d['gym'][1] + 1, 'f'))
    E.append(seat(m, {'type': 'sign', 'name': 'Little Lantern sign', 'text': 'THE LITTLE LANTERN - "THE PAGEANT OF THE PAGEANT." Held over. Held over again. Held over by D. Pell, who has bought every Thursday.'}, d['little'][0] + 2, d['little'][1] + 1, 'c'))
    E.append({'type': 'sign', 'name': 'Little Lantern door', 'at': list(d['little']), 'post': False, 'text': 'SOLD OUT. (A hand-lettered card adds: "and the matinee. and tomorrow.")'})
    E.append(seat(m, {'type': 'sign', 'name': "Players' Gate sign", 'text': "THE PLAYERS' GATE - North: the Players' Causeway to the Upper Town and the market."}, 39, 16, 'c'))
    E.append(seat(m, {'type': 'sign', 'name': 'Playbill wall', 'text': 'Playbills, ten deep: "THE LOYAL THREE", "THE DROWNED DUKE", "...ED K..." (pasted over, twice), "THE PAGEANT OF THE PAGEANT".'}, 22, 42, 'f'))
    E.append(seat(m, ev['Costumier'], 27, 37, 'c'))
    E.append(seat(m, ev['Street player'], 44, 46, 'f'))
    for n, x, y in (('Rival Theatre Barker', 60, 37),):
        if n in tf: E.append(seat(m, tf[n], x, y))
    E.append(seat(m, {'type': 'npc', 'name': 'Street Juggler', 'sprite': 'NPC 06', 'dir': 'down', 'move': 'fixed', 'text':
                      'Street Juggler: I juggle for coins. In Saltmere the coins are the only thing that falls the way you expect.'}, 30, 45, 'f'))
    E.append(seat(m, {'type': 'npc', 'name': 'Costumed Usher', 'sprite': 'NPC 18', 'dir': 'down', 'move': 'fixed', 'text':
                      "Costumed Usher: Programmes! A copper! Dorian's face on every page, free of charge!"}, 49, 35, 'f'))
    E.append(seat(m, {'type': 'event', 'name': 'Lillipup (Hound Number Three)', 'pages': [
        {'cond': {}, 'commands': []},
        {'cond': {'self': None}, 'commands': []}]}, 62, 37, 'c') if False else None)
    E = [e for e in E if e]
    m.events += E
    for e in E: m.taken[e['at'][1], e['at'][0]] = True
    for x, y in K.incoming(147): m.taken[y, x] = True
    # ---- playbills on the walls, columns, lantern strings, stalls, benches, the crowd
    props(m, (('pf_morris', 22, 44), ('pf_morris', 65, 44), ('pf_morris', 33, 48), ('pf_morris', 55, 48), ('pf_morris', 35, 35), ('pf_morris', 52, 35),
              ('pf_stall4', 24, 47), ('pf_stall1', 60, 47), ('pf_stall3', 40, 49), ('pf_stall0', 46, 49),
              ('pf_logbench', 28, 42), ('pf_logbench', 58, 42), ('pf_hounds', 42, 42) if False else ('pf_planter0', 36, 41),
              ('pf_planter3', 51, 41), ('hb_tables', 20, 49), ('gl_tables', 66, 48), ('hb_barrels', 68, 42), ('pf_well', 19, 42)), on='f')
    props(m, (('hb_barrel', 24, 37), ('hb_cask', 64, 36), ('hb_crates4', 70, 37), ('pf_morris', 15, 37), ('pf_morris', 74, 16), ('pf_morris', 14, 16),
              ('hb_rugline', 3, 37), ('hb_washline', 82, 36)), on='c')
    props(m, (('pf_logbench', 6, 59), ('pf_logbench', 30, 59), ('pf_logbench', 64, 59), ('hb_rope', 52, 59), ('hb_crates4', 70, 58),
              ('pf_stall2', 18, 57), ('hb_fishstall', 78, 57), ('pf_morris', 44, 58)), on='f')
    for x in (20, 26, 31, 57, 62, 67): overs(m, 'pf_bill%d' % (x % 4), x, 50, z=2)
    lamps(m, [(x, 57) for x in range(4, 86, 9)] + [(x, 36) for x in range(4, 86, 12)] + [(x, 15) for x in range(6, 86, 13)] +
          [(34, 34), (53, 34), (18, 41), (69, 41), (18, 50), (69, 50)])
    string_lights(m, 34, 53, 34); string_lights(m, 18, 69, 41); string_lights(m, 0, 87, 36) if False else None
    string_lights(m, 18, 69, 50); string_lights(m, 12, 33, 36); string_lights(m, 54, 76, 36)
    parapets(m, 'rw', rows=(18, 38)); parapets(m, 'qy', rows=(60,))
    street_trees(m, [(16, 60), (36, 60), (50, 60), (70, 60), (20, 49), (67, 49)])
    gardens(m, 147); courts(m, 147)
    crowd(m, [(x, y) for y in range(42, 50) for x in range(18, 70)], 16, 1471, moving=0.5)
    crowd(m, [(x, y) for y in range(34, 39) for x in range(0, 88)], 6, 1472)
    crowd(m, [(x, y) for y in range(57, 60) for x in range(0, 88)], 5, 1473); crowd(m, [(x, y) for y in range(15, 18) for x in range(0, 88)], 4, 1474, on='c')
    m.paint()
    boats(m, (('ak_rock2', 30, 66), ('ak_boulder', 2, 66), ('ak_rock2', 80, 1), ('hb_boat1', 8, 63), ('hb_boat2', 24, 64), ('hb_boat3', 62, 63), ('hb_boat4', 80, 64), ('hb_boat1', 10, 2), ('hb_boat2', 70, 3)))
    m.scatter(5, seed=147, on='.'); glints(m, 147, p=0.3)
    h = head(147, '147_saltmere_oldtown.yaml', biome='harbour', tone=[12, 4, -18, 0], connections=[],
             fog={'name': 'prismfall_seamist', 'opacity': 24, 'blend': 0, 'zoom': 100, 'sx': 2, 'sy': 0})
    m.write(147, h, "# Saltmere - The Old Town (147). WRITTEN BY layouts/saltmere_rj.py (PF Rejuv City, tileset 55) - edit that script.\n")
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
