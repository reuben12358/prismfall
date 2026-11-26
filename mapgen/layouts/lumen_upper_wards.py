#!/usr/bin/env python3
"""layouts/lumen_upper_wards.py - Batch 1A Brand-New Canonical Act 1 Lumen Upper Wards,
Meridian Spire Upper Floors & Skyport Customs (7 Brand-New Maps; ZERO edits to any existing map or shared file!).

Outdoor Wards on Tileset 60 ("PF Rejuv Lumen"):
  - 194 Lumen City - Council Ward          (48x40, Zenith Council Hall [24,8] LC_COUNCIL -> 197, S exit -> 180 [47,8] down)
  - 195 Lumen City - Spire District        (44x48, Meridian Spire [22,12] -> 185 [12,15] up, W exit -> 180 [84,14] left)
  - 196 Lumen City - Skyport Terrace       (40x36, Skyport Customs [20,6] LC_SKYPORT -> 959, S exit -> 180 [74,6] down)

Spire & Council Interiors on Tileset 60 ("PF Rejuv Lumen"):
  - 197 Zenith Council Hall - Council Chamber  (31x23, cvY + lmw tiered hemicycle rostrum, Exit [15,22] LC_COUNCIL -> 194)
  - 198 Meridian Spire - Executive Gallery     (31x19, cvZ obsidian-gold sky-gallery, [15,18] -> 185 [12,6] down, [28,2] -> 199)
  - 199 Meridian Spire - Dark Stone Core       (25x25, cvZ/cvQ/lmw abyssal containment core [12,12], [12,24] -> 198 [28,3] down)

Aviation Terminal Interior on Tileset 34 ("Prismfall Interior"):
  - 959 Skyport Customs                        (17x11, 0x80 brass customs desk, manifest board, luggage scale, Exit [8,10] LC_SKYPORT)

Usage:
    PRISMFALL_GFX=/home/antigravity/pf_engine_run/game/Graphics \\
      /usr/bin/python3 -I mapgen/layouts/lumen_upper_wards.py
"""
import os
import sys
import random
import numpy as np
import yaml

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAY_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, LAY_DIR)

import lumenkit as LK
from lumenkit import City, sz
from cavekit import Cave, FLOOR, TER, PIT, MASS
from rkit import P1, STAMPS
import rcompose as RC
import passguard as PG
from terrain import NB2AUTO
from interiorkit import TF

TID60 = 60
TID34 = 34
VOID34 = 5437
RAW_DIR = os.path.join(HERE, 'data', 'raw')
SPEC_DIR = os.path.join(HERE, 'specs')

# Safe Lumen townhouse packs (all verified TS60 stamps; ZERO tr_teal!)
PACK_NOBLE = ['lb_t8a', 'lb_t7a', 'lb_t8b', 'lb_t6a', 'lb_t9a', 'lb_t6b', 'lb_t5a', 'lb_t7b', 'lb_t5b', 'lb_t4b', 'lb_t10a']
PACK_CORP = ['lb_t9a', 'lb_t8b', 'lb_t6c', 'lb_t7a', 'lb_t8a', 'lb_t6b', 'lb_t5a', 'lb_t4b']


# ==============================================================================
# SHARED TS60 HELPERS (Outdoor Wards + Spire/Council Interiors)
# ==============================================================================
def fix_autotiles_single_layer(Lr):
    """Enforce exact single-layer 8-neighbor NB2AUTO across every layer z in (0, 1, 2)."""
    Z, H, W = Lr.shape
    for z in range(Z):
        layer = Lr[z]
        auto_mask = (layer >= 48) & (layer < 384)
        if not auto_mask.any():
            continue
        slots = np.unique(layer[auto_mask] // 48)
        for slot in slots:
            m = (layer >= slot * 48) & (layer < (slot + 1) * 48)
            pad = np.pad(m, 1, constant_values=True)
            for y, x in np.argwhere(m):
                b = 0
                for dx, dy, bit in ((0, -1, 1), (1, -1, 2), (1, 0, 4), (1, 1, 8),
                                    (0, 1, 16), (-1, 1, 32), (-1, 0, 64), (-1, -1, 128)):
                    if pad[y + 1 + dy, x + 1 + dx]:
                        b |= bit
                Lr[z, y, x] = int(slot * 48 + NB2AUTO[b])


def write_ts60(m, mid, head, comment):
    """Resolve virtual IDs -> TS60, enforce single-layer NB2AUTO + passguard, save .npy + .yaml."""
    Lr = RC.resolve(m.L, TID60).astype(np.int32)
    fix_autotiles_single_layer(Lr)
    PG.guard(Lr, TID60, [tuple(e['at']) for e in m.events if e and e.get('at')], f'map {mid}')
    os.makedirs(RAW_DIR, exist_ok=True)
    rel = f'data/raw/{mid:03d}.npy'
    np.save(os.path.join(HERE, rel), Lr)
    key = Lr[0].astype(np.int64) * 10**10 + Lr[1].astype(np.int64) * 10**5 + Lr[2]
    mir = (key == key[:, ::-1]).mean() * 100.0
    print(f'Built {mid} {head["name"]:38s} {m.W}x{m.H} ts=60 events={len(m.events):2d} mirror={mir:.1f}%')
    spec = dict(head)
    fn = spec.pop('_file', f'{mid:03d}.yaml')
    spec['raw'] = rel
    spec['tileset'] = TID60
    body = yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=150, allow_unicode=True)
    body += yaml.safe_dump({'events': m.events}, sort_keys=False, default_flow_style=None, width=150, allow_unicode=True)
    with open(os.path.join(SPEC_DIR, fn), 'w', encoding='utf-8') as f:
        f.write(comment + body)
    return Lr


def room60(W, H, p, seed):
    m = Cave(W, H, p, seed, pool='Cave Pool', tid=TID60)
    m.STAIRS = LK.STAIRS_LM or LK.K.STAIRS_STONE
    return m


def put_if(m, name, x, y, on='.'):
    st = STAMPS[name]
    w, h = st['w'], st['h']
    if m.free(x, y, w, h, on=on) and not any((xx, yy) in m.keep_clear
                                              for xx in range(x, x + w) for yy in range(y, y + h)):
        m.put(name, x, y) if hasattr(m, 'put') and isinstance(m, Cave) else m.stamp(name, x, y)
        return True
    return False


def place_arch(m, name, x, y, mark_base=True):
    """Stamp an architectural piece onto m.over (allows pri>0 tops over cliff faces)."""
    st = STAMPS[name]
    h, w = st['h'], st['w']
    for dy in range(h):
        for dx in range(w):
            xx, yy = x + dx, y + dy
            if not m.inb(xx, yy):
                continue
            for z in (1, 2):
                t = st['layers'][z][dy][dx]
                if t:
                    m.over.append((z, xx, yy, t))
                    if mark_base and z == 1:
                        m.taken[yy, xx] = True


def abyss_piece(m, name, x, y):
    """Place a towering reactor/skyline piece inside non-walkable void/abyss/PIT bays."""
    st = STAMPS[name]
    for dy in range(st['h']):
        for dx in range(st['w']):
            xx, yy = x + dx, y + dy
            if not m.inb(xx, yy):
                continue
            for z in (1, 2):
                t = st['layers'][z][dy][dx]
                if t:
                    m.over.append((z, xx, yy, t))


def hang(m, name, x, y):
    L = STAMPS[name]['layers']
    for dy in range(len(L[0])):
        for dx in range(len(L[0][0])):
            t = next((L[z][dy][dx] for z in (2, 1, 0) if L[z][dy][dx]), 0)
            if t and m.inb(x + dx, y + dy) and m.cliff[y + dy, x + dx]:
                m.over.append((2, x + dx, y + dy, t))


def on_faces(m, name, cells):
    for x, y in cells:
        if m.inb(x, y) and m.cliff[y, x]:
            m.over.append((2, x, y, P1(name)))


def lamps_out(m, pts, name='lm_arclamp'):
    for x, y in pts:
        if m.free(x, y - 2, 1, 3, on='pqlrd.'):
            m.stamp(name, x, y - 2)


def pack_terrace(m, x0, x1, y_door, ymin, names, seed=0, fixed=(), fill=True, plaques=None):
    """Pack Lumen townhouses shoulder-to-shoulder along row y_door, roofing gaps cleanly."""
    rng = random.Random(m.seed * 19 + seed)
    out = []
    for nm, x, lk in fixed:
        w, h = sz(nm)
        d = m.put(nm, x, y_door - h + 1, link=lk[0] if lk else None, dname=lk[1] if lk else None)
        out.append((nm, x, y_door - h + 1, d))
    x = x0
    while x <= x1:
        if m.taken[y_door, x]:
            x += 1
            continue
        room = 0
        while x + room <= x1 and not m.taken[y_door, x + room]:
            room += 1
        cand = [n for n in names if sz(n)[0] <= room and sz(n)[1] <= y_door - ymin + 1]
        if not cand:
            x += room
            continue
        cand.sort(key=lambda n: -sz(n)[0] * 10 - rng.random() * 25)
        nm = cand[0] if rng.random() < 0.55 else rng.choice(cand)
        w, h = sz(nm)
        if not m.free(x, y_door - h + 1, w, h, on='pqlrd.'):
            x += 1
            continue
        d = m.put(nm, x, y_door - h + 1)
        out.append((nm, x, y_door - h + 1, d))
        x += w
    if fill:
        before = m.cls == 'f'
        m.fill(x0, ymin, x1, y_door)
        if seed % 2 == 0:
            m.slate = getattr(m, 'slate', set()) | {(int(cx), int(cy)) for cy, cx in np.argwhere((m.cls == 'f') & ~before)}
    if plaques:
        k = 0
        for nm, bx, by, d in out:
            if d is not None:
                continue
            st = STAMPS[nm]
            if 'door' not in st:
                continue
            dx, dy = st['door']
            m.events.append({
                'type': 'sign',
                'name': f'House plaque {seed}_{k}',
                'at': [bx + dx, by + dy],
                'post': False,
                'text': plaques[(k + seed) % len(plaques)],
            })
            k += 1
    return out


def scatter_wear_out(m, n_per_100=8, on='pq', seed=0, kinds=(1, 4)):
    """Subtle golden leaves & blossom petals on marble plazas (ZERO dark drain/oil stains!)."""
    rng = random.Random(m.seed * 13 + seed)
    for y in range(m.H):
        for x in range(m.W):
            if (m.cls[y, x] in on and not m.taken[y, x] and not m.cliff[y, x]
                    and (x, y) not in m.keep_clear and rng.random() * 100 < n_per_100):
                m.over.append((2, x, y, P1('lm_wear%d' % rng.choice(kinds))))


def paint_sunburst(m, sx, sy):
    """Reveal the 5x5 golden Meridian Sunburst on outdoor City maps by clearing City.ON_TOP L1 plaster over L0."""
    sun_L = STAMPS['lm_sun']['layers'][0]
    for dy in range(5):
        for dx in range(5):
            xx, yy = sx + dx, sy + dy
            if m.inb(xx, yy) and not m.cliff[yy, xx]:
                m.L[0, yy, xx] = sun_L[dy][dx]
                m.L[1, yy, xx] = 0


def dress_roofs_out(m, seed=1):
    """Break up uniform roof fills with skylights & vents (boosts L3 & destroys symmetry!)."""
    rng = random.Random(m.seed * 29 + seed)
    for y in range(m.H):
        for x in range(m.W):
            if m.cls[y, x] == 'f' and m.L[1, y, x] == 0 and rng.random() < 0.08:
                m.L[1, y, x] = P1('lm_grate_off')


def add_water_glints(m, seed=1):
    """Subtle shimmering glints on open Still water cells (never alters L0 autotile!)."""
    rng = random.Random(m.seed * 31 + seed)
    for y in range(m.H):
        for x in range(m.W):
            if m.cls[y, x] == 'w' and m.L[1, y, x] == 0 and m.L[2, y, x] == 0 and rng.random() < 0.14:
                m.L[2, y, x] = P1('hb_glint%d' % rng.randrange(4))


def floor_carpet_cave(m, x0, y0, x1, y1):
    for yy in range(y0, y1 + 1):
        for xx in range(x0, x1 + 1):
            if m.inb(xx, yy) and m.cls[yy, xx] == '.':
                part = ('n' if yy == y0 else 's' if yy == y1 else '') + ('w' if xx == x0 else 'e' if xx == x1 else '')
                m.L[0, yy, xx] = P1('lm_carpet_' + (part or 'c'))


# ==============================================================================
# MAP 194: LUMEN CITY - COUNCIL WARD (48x40, Outside TS60)
# ==============================================================================
def build_194():
    """194: Lumen City - Council Ward (48x40, Outside TS60).
    Grand marble aristocratic northwest ward housing Zenith Council Hall ([24,8] LC_COUNCIL -> 197).
    South return stairway [22..26, 39] -> 180 [47, 8] down.
    """
    W, H = 48, 40
    m = City(W, H, 194, base='p')
    m.ht[:] = 2
    m.roof_kind = 'V'

    # ---- 1. Plateau Elevation & West Nadir Cliff Overlook ----
    # Clean open west twilight plateau drop over Nadir (x=0..3, ht=0, cls='x' — ZERO floating concrete pads or stray roof strips!)
    m.cls[:, 0:4] = 'x'
    m.ht[:, 0:4] = 0
    # Upper Zenith Council Crown Terrace (x=4..47, y=0..14, ht=3 with lmw marble balustrade!)
    m.ht[0:15, 4:48] = 3
    m.rect(14, 9, 21, 6, 'q')            # Council Hall marble forecourt
    # Monumental grand marble stair descending from Council Terrace (y=14..16, x=22..26)
    m.stairs(22, 14, w=5, n=3, c='q')

    # Middle Founders' Orrery & Prism Fountain Plaza (x=14..34, y=18..31)
    m.rect(14, 17, 21, 16, 'q')
    # South Aristocratic Promenade & Grand Entry Terrace (y=33..39)
    m.rect(19, 33, 11, 7, 'q')

    # ---- 2. Zenith Council Hall & Founding Houses ----
    COUNCIL_PLAQUES = [
        'A brass crest: HOUSE SALLOW — FOUNDING HOUSE OF ZENITH. "Wind and Ledger."',
        'A brass crest: HOUSE STRADE — FOUNDING HOUSE OF ZENITH. "Tolerance in Steel."',
        'A brass crest: HOUSE HALCYON — FOUNDING HOUSE OF ZENITH. "First Light of the Plateau."',
        'A brass crest: HOUSE CALDER — FOUNDING HOUSE OF ZENITH. "Current and Wire."',
        'A brass crest: HOUSE VANCE — FOUNDING HOUSE OF ZENITH. "By Charter of AF 118."',
        'Locked. Inside, velvet curtains are drawn for the Tenth Year Council session.',
    ]
    # Zenith Council Hall (lb_council: 12x6, door=[6,5]) at (18, 3) -> door EXACTLY at [24, 8] LC_COUNCIL!
    m.put('lb_council', 18, 3, link='LC_COUNCIL', dname='Zenith Council Hall')
    # Roof fill behind Council Hall crown (y=0..2, x=18..29) so zero bare walkable strip behind dome!
    m.fill(18, 0, 29, 2)

    # Upper Terrace flanking aristocratic townhouses (y_door=8)
    pack_terrace(m, 5, 17, 8, 0, PACK_NOBLE, seed=1, plaques=COUNCIL_PLAQUES)
    pack_terrace(m, 30, 47, 8, 0, PACK_NOBLE, seed=2, plaques=COUNCIL_PLAQUES)

    # Middle Tier Founding House Townhouses (West & East wings along y_door=23 and East terrace y_door=31)
    pack_terrace(m, 5, 13, 23, 17, ['lb_t8a', 'lb_t5a', 'lb_t4b'], seed=3, plaques=COUNCIL_PLAQUES)
    pack_terrace(m, 35, 47, 23, 17, ['lb_t7a', 'lb_t6b', 'lb_t5b'], seed=4, plaques=COUNCIL_PLAQUES)
    pack_terrace(m, 36, 47, 32, 26, ['lb_t6a', 'lb_t5a', 'lb_t6c'], seed=5, plaques=COUNCIL_PLAQUES)

    # ---- 3. Manicured Terraced Gardens & Reflecting Pools (NO bare grass deserts!) ----
    # Twin Upper Forecourt Reflecting Parterres (x=7..12 & x=36..41, y=11..13)
    for gx in (7, 36):
        m.rect(gx, 11, 6, 3, '.')
        m.rect(gx + 1, 12, 4, 1, 'w')
    # Four Middle Plaza Ornamental Gardens flanking the Fountain & Founders' Orrery
    m.rect(15, 18, 5, 4, '.'); m.rect(16, 19, 3, 2, 'w')   # NW reflecting pool parterre
    m.rect(29, 18, 5, 4, '.'); m.rect(30, 19, 3, 2, 'w')   # NE reflecting pool parterre
    m.rect(5, 27, 8, 6, '.')                               # SW Founding House Conservatory Grove
    m.rect(6, 34, 11, 5, '.')                              # South-West Aristocratic Terrace Garden
    m.rect(31, 34, 15, 5, '.')                             # South-East Aristocratic Rose & Grove Garden

    # ---- 4. Centerpieces: Prism Fountain, Founders' Orrery, Ceremonial Carpet & Brass Inlays ----
    # Ceremonial crimson-and-brass carpet descending from Council Hall door (24,8) down to stair head (24,13)
    for y in range(9, 14):
        for i, x in enumerate((23, 24, 25)):
            m.over.append((1, x, y, P1('lm_carpet_' + ('w' if i == 0 else 'e' if i == 2 else 'c'))))
    # Prism Fountain (6x5) at (21, 19) -> x=21..26, y=19..23
    m.put('lm_fountain', 21, 19)
    # Unique Founders' Orrery Monument (lm_statue 2x3) at (23, 25) -> x=23..24, y=25..27
    m.put('lm_statue', 23, 25)
    # Golden Meridian Sunburst (5x5) inlaid at the South Promenade arrival court (22, 30) -> x=22..26, y=30..34
    m.put('lm_sun', 22, 30, force=True)

    # Brass light-conduit promenade inlays framing Council Plaza cleanly (never on grass/taken)
    inlay_pts = set()
    for x in range(15, 34):
        inlay_pts.add((x, 24))
        inlay_pts.add((x, 29))
    for y in range(18, 35):
        inlay_pts.add((20, y))
        inlay_pts.add((28, y))
    for x in range(14, 35):
        inlay_pts.add((x, 10))
    m.inlay([pt for pt in sorted(inlay_pts) if m.cls[pt[1], pt[0]] in 'pq' and not m.taken[pt[1], pt[0]]])

    # ---- 5. South Return Stairway & West Stone-Parapet Cliff Balustrade (matching lumen.py:591!) ----
    # South grand gateway steps (x=22..26, y=38..39) framed by bollards & horizontal railings
    for y in (38, 39):
        for i, x in enumerate(range(22, 27)):
            m.over.append((1, x, y, P1('lm_stair_' + ('l' if i == 0 else 'r' if i == 4 else 'm'))))
    for x in range(19, 30):
        if x not in range(22, 27):
            m.prop('lm_bollard' if x in (19, 21, 27, 29) else 'lm_railing_m', x, 39)
    # West Cliff Overlook vertical stone parapet (nr_wall_v) + brass bollards strictly on walkable rim rows (NEVER rooftops/cliffs!)
    for y in list(range(9, 15)) + list(range(24, 40)):
        if not m.taken[y, 4] and not m.cliff[y, 4]:
            m.prop('lm_bollard' if y in (9, 14, 24, 29, 34, 39) else 'nr_wall_v', 4, y)

    # ---- 6. Mounted Signpost & Overlook Telescope Props (Guaranteed visible directly under sign events!) ----
    place_arch(m, 'pf_signpost', 28, 35)   # Base at [28, 36] -> Council Ward Notice!
    place_arch(m, 'lm_viewer', 5, 24)      # Base at [5, 25] -> West Plateau Overlook!

    # ---- 7. Events (100% Static Lore + Clean Return Warps; Zero Invented Switches/Vars) ----
    # South Exit warps [22..26, 39] -> Map 180 [47, 8] down (verified walkable right below Council guard!)
    for wx in range(22, 27):
        m.events.append({
            'type': 'warp',
            'name': f'To Concourse ({wx})',
            'at': [wx, 39],
            'to': {'map': 180, 'x': 47, 'y': 8, 'dir': 'down'},
        })
    m.events += [
        {
            'type': 'npc',
            'name': 'Council Guard W',
            'at': [21, 10],
            'sprite': 'trainer_MERIDIAN_DIRECTORATE',
            'dir': 'down',
            'text': 'Directorate Guard: Zenith Council Hall. Sessions of the Six Founding Houses are held under Chair Voss.',
        },
        {
            'type': 'npc',
            'name': 'Council Guard E',
            'at': [27, 10],
            'sprite': 'trainer_MERIDIAN_DIRECTORATE',
            'dir': 'down',
            'text': 'Directorate Guard: Keep to the marble walkways. The marble balustrades were polished this morning for the Tenth Year.',
        },
        {
            'type': 'npc',
            'name': 'Council Clerk',
            'at': [20, 26],
            'sprite': 'NPC 14',
            'dir': 'right',
            'text': 'Council Clerk: Six Founding Houses, six votes — and Meridian Concord holds the Chair\'s tie-breaker. That is how Mandate politics work.',
        },
        {
            'type': 'npc',
            'name': 'House Sallow Steward',
            'at': [12, 25],
            'sprite': 'NPC 21',
            'dir': 'down',
            'text': 'Steward: Councillor Sallow\'s airships built half this ward before Voss ever strung a wire. Remember that when you hear his speeches.',
        },
        {
            'type': 'npc',
            'name': 'Aristocrat Gentleman',
            'at': [15, 31],
            'sprite': 'trainer_GENTLEMAN',
            'dir': 'right',
            'text': 'Gentleman: Up here on the plateau crown the air is crisp and the lamps never dim. One barely hears the trams below.',
        },
        {
            'type': 'npc',
            'name': 'Aristocrat Lady',
            'at': [33, 30],
            'sprite': 'trainer_LADY',
            'dir': 'left',
            'text': 'Lady: The Founders\' Orrery turns once every ten years to the minute — or so the brochure insists.',
        },
        {
            'type': 'sign',
            'name': "Founders' Orrery",
            'at': [24, 27],
            'post': False,
            'text': 'THE FOUNDERS\' ORRERY — CAST IN BRONZE, AF 118. Six rings for the Founding Houses of Zenith, turning slowly above the plateau.',
        },
        {
            'type': 'sign',
            'name': 'Council Ward Notice',
            'at': [28, 36],
            'post': False,
            'text': 'COUNCIL WARD — CROWN OF LUMEN CITY. North: Zenith Council Hall. South Steps: The Concourse.',
        },
        {
            'type': 'sign',
            'name': 'West Plateau Overlook',
            'at': [5, 25],
            'post': False,
            'text': 'Far below the marble rail, Nadir\'s orange lamps smoulder through evening haze.',
        },
        {
            'type': 'item',
            'name': 'Item',
            'at': [43, 35],
            'item': 'FULLHEAL',
        },
    ]

    # Protect all event spots, door thresholds & main thoroughfares
    for e in m.events:
        ex, ey = e['at']
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                m.keep_clear.add((ex + dx, ey + dy))
    m.keep_clear |= ({(x, y) for x in range(22, 27) for y in range(8, 40)}
                     | {(x, y) for x in range(14, 35) for y in (10, 17, 24, 29, 35)}
                     | {(x, y) for x in range(5, 47) for y in (9, 24, 33)})

    # ---- 8. Lush Botanical Planting, Street Furniture, Banners & Asymmetric Accents (ZERO tr_teal!) ----
    # Ceremonial Council Banner Lamps & Classical Arc Lamps
    for x, y in ((21, 11), (27, 11), (20, 18), (28, 18), (20, 35), (28, 35)):
        m.try_put('lm_bannerlamp_w', x, y, on='pq')
    lamps_out(m, [(15, 11), (33, 11), (14, 26), (34, 26), (17, 36), (31, 36), (10, 26), (39, 25)])
    # Scenic viewers, benches, planters, clock & news kiosk (ZERO duplicate statues; unique central Founders' Orrery!)
    for nm, x, y in (
        ('lm_viewer', 5, 12), ('lm_viewer', 5, 31),
        ('lm_clock', 32, 11), ('lm_kiosk', 14, 34), ('lm_news', 34, 12),
        ('lm_bench', 17, 22), ('lm_bench', 30, 22), ('lm_bench', 18, 28), ('lm_bench', 29, 28),
        ('lm_bench', 20, 37), ('lm_bench', 28, 37), ('lm_bench', 38, 13), ('lm_bench', 31, 26),
        ('lm_planter3', 15, 14), ('lm_planter3', 31, 14), ('lm_planter', 19, 13), ('lm_planter', 28, 13),
        ('lm_planter', 16, 12), ('lm_topiary', 31, 24),
        ('lm_topiary', 22, 9), ('lm_topiary', 26, 9), ('lm_topiary', 19, 20), ('lm_topiary', 28, 20),
        ('lm_topiary', 21, 25), ('lm_topiary', 26, 25),
        ('lm_holo', 35, 25), ('lm_stall_b', 15, 12),
    ):
        m.try_put(nm, x, y, on='pq')

    # Rich Botanical Garden Groves in SW & South Terrace Gardens (ZERO tr_teal; max 10x10 bare grass < 15%!)
    for nm, x, y in (
        ('tr_pink', 6, 27), ('tr_oak', 10, 28), ('nt_azalea0', 8, 27), ('nt_azalea1', 6, 31), ('nt_shrub0', 10, 31),
        ('tr_oak2', 7, 35), ('tr_pink', 11, 35), ('nt_teal_a', 14, 35),
        ('nt_azalea2', 6, 34), ('nt_azalea0', 9, 36), ('nt_shrub1', 12, 37), ('lm_topiary', 15, 37),
        ('tr_oak', 32, 35), ('tr_pink', 36, 35), ('nt_teal_a', 40, 35), ('tr_pine', 44, 34),
        ('nt_azalea1', 34, 37), ('nt_azalea2', 38, 36), ('nt_shrub0', 41, 37), ('nt_azalea0', 44, 37),
        ('lm_topiary', 7, 11), ('lm_topiary', 12, 11), ('lm_topiary', 36, 11), ('lm_topiary', 41, 11),
        ('nt_azalea0', 15, 18), ('nt_azalea1', 29, 18), ('nt_shrub0', 18, 20), ('nt_shrub1', 32, 20),
    ):
        m.try_put(nm, x, y, on='.')

    scatter_wear_out(m, n_per_100=7, on='pq', seed=194)
    m.paint()
    m.scatter(n_per_100=24, seed=194, on='.')
    dress_roofs_out(m, seed=194)
    add_water_glints(m, seed=194)

    # Refined post-paint limestone plaza borders (ZERO dark-brown lm_low0 potholes!)
    pave0, pave2 = P1('lm_pave0'), P1('lm_pave2')
    for x in range(14, 35):
        for y in (17, 32):
            if m.cls[y, x] == 'q' and not m.cliff[y, x] and m.L[1, y, x] in (P1('lm_plaza0'), P1('lm_plaza1')):
                m.L[0, y, x] = pave0; m.L[1, y, x] = pave0
    for y in range(18, 32):
        for x in (14, 34):
            if m.cls[y, x] == 'q' and not m.cliff[y, x] and m.L[1, y, x] in (P1('lm_plaza0'), P1('lm_plaza1')):
                m.L[0, y, x] = pave2; m.L[1, y, x] = pave2
    paint_sunburst(m, 22, 30)

    head = {
        'id': 194,
        'name': 'Lumen City - Council Ward',
        'parent': 180,
        'bgm': 'Cedolan City',
        'field': 'NEON_GRID',
        'rubric': True,
        'tone': [6, 4, 2, 0],
        'metadata': {
            'Outdoor': True,
            'ShowArea': True,
            'MapPosition': [0, 16, 16],
            'Name': 'Council Ward',
        },
        '_file': '194_lumen_council_ward.yaml',
    }
    return write_ts60(m, 194, head, '# GENERATED by mapgen/layouts/lumen_upper_wards.py (Batch 1A Act 1 Craft): 194 Council Ward.\n')


# ==============================================================================
# MAP 195: LUMEN CITY - SPIRE DISTRICT (44x48, Outside TS60)
# ==============================================================================
def build_195():
    """195: Lumen City - Spire District (44x48, Outside TS60).
    Dramatic high-altitude ceremonial corporate plaza encircling Meridian Spire's base.
    Meridian Spire door [22, 12] -> 185 [12, 15] up (explicit to: avoids duplicate LC_TOWER link!).
    West return avenue [0, 33..37] -> 180 [84, 14] left.
    """
    W, H = 44, 48
    m = City(W, H, 195, base='p')
    m.ht[:] = 2
    m.roof_kind = 'V'

    # ---- 1. East Plateau Cliff Overlook (x=39..43) & Upper Spire Sanctuary (y=0..18, ht=3) ----
    # Clean open twilight sky drop along East rim (ZERO floating concrete pads or stray roof strips!)
    m.cls[:, 39:44] = 'x'
    m.ht[:, 39:44] = 0

    # Upper Meridian Spire Sanctuary Terrace (ht=3 with lmw marble balustrade!)
    m.ht[0:18, 0:39] = 3
    m.rect(10, 12, 25, 6, 'q')
    # Monumental grand Spire stair (x=20..24, y=17..19)
    m.stairs(20, 17, w=5, n=3, c='q')

    # Central Ceremonial Sunburst Plaza (x=9..35, y=20..36)
    m.rect(9, 20, 27, 17, 'q')
    # West Return Corporate Boulevard connecting cleanly to x=0, y=33..37 -> 180 [84, 14] left!
    m.rect(0, 32, 10, 7, 'q')

    # ---- 2. Meridian Spire Base & Corporate Annex Facades ----
    SPIRE_PLAQUES = [
        'A brushed-brass plate: MERIDIAN DIRECTORATE — GRID OPERATIONS.',
        'A brass plate: MERIDIAN CONCORD — LEGAL & CHARTER ARCHIVE.',
        'Locked. Security glass reflects the golden Spire overhead.',
        'A brass plate: LATTICE TRANSMISSION BUREAU — AUTHORIZED STAFF ONLY.',
    ]
    # Meridian Spire (lb_spire: 16x13, door=[8, 12]) at (14, 0) -> door at [22, 12]!
    # Note: do NOT pass link='LC_TOWER' (180 already owns LC_TOWER); add explicit door event below!
    m.put('lb_spire', 14, 0)
    # Frame the soaring upper Spire shaft cleanly with open starry night sky (cls='x', ht=3 -> solid & ZERO green shingle burial!)
    m.cls[0:7, 14:19] = 'x'; m.taken[0:7, 14:19] = True
    m.cls[0:7, 25:30] = 'x'; m.taken[0:7, 25:30] = True
    m.events.append({
        'type': 'door',
        'at': [22, 12],
        'gfx': ['', 0, 2],
        'name': 'Meridian Spire',
        'to': {'map': 185, 'x': 12, 'y': 15, 'dir': 'up'},
    })

    # Flanking Corporate Directorate Annexes on Upper Terrace (y_door=11)
    pack_terrace(m, 0, 13, 11, 0, PACK_CORP, seed=1, plaques=SPIRE_PLAQUES)
    pack_terrace(m, 30, 37, 11, 0, ['lb_t8a', 'lb_t7b', 'lb_t6b'], seed=2, plaques=SPIRE_PLAQUES)
    # West Corporate Colonnade Block north of the return boulevard (x=0..8, y=20..28)
    pack_terrace(m, 0, 8, 28, 20, ['lb_t8b', 'lb_t5a', 'lb_t4b'], seed=3, plaques=SPIRE_PLAQUES)

    # ---- 3. Ornamental Reflecting Gardens & Southern Cliff-Edge Park ----
    # Four Symmetrical-yet-Varied Spire Reflecting Parterres
    m.rect(11, 22, 6, 4, '.'); m.rect(12, 23, 4, 2, 'w')   # NW Reflecting Pool Garden
    m.rect(28, 22, 6, 4, '.'); m.rect(29, 23, 4, 2, 'w')   # NE Reflecting Pool Garden
    m.rect(11, 31, 6, 4, '.')                              # SW Azalea & Ornamental Tree Parterre
    m.rect(28, 31, 6, 4, '.')                              # SE Azalea & Ornamental Tree Parterre
    # South Skyline Promenade Gardens (y=41..47, leaving clear path to XSPEED at [4, 44]!)
    m.rect(8, 41, 13, 6, '.'); m.rect(12, 43, 5, 2, 'w')
    m.rect(24, 41, 13, 6, '.')
    m.rect(0, 40, 7, 3, '.')                               # NW corner garden above XSPEED alcove

    # ---- 4. Centerpiece Golden Sunburst, Gala Carpet & Sweeping Brass-Cyan Inlays ----
    # Royal Crimson Gala Carpet running from Spire door (22,12) down to stair head (22,16)
    for y in range(13, 17):
        for i, x in enumerate((21, 22, 23)):
            m.over.append((1, x, y, P1('lm_carpet_' + ('w' if i == 0 else 'e' if i == 2 else 'c'))))
    # 5x5 Monumental Golden Meridian Sunburst centered at (20, 26) -> x=20..24, y=26..30
    m.put('lm_sun', 20, 26, force=True)

    # Sweeping brass-and-cyan inlaid boulevards radiating through the Spire District
    inlays = set()
    for x in range(1, 37):
        inlays.add((x, 35))
    for x in range(10, 36):
        inlays.add((x, 21))
        inlays.add((x, 28))
    for y in range(21, 41):
        inlays.add((18, y))
        inlays.add((26, y))
    for y in range(31, 40):
        inlays.add((22, y))
    m.inlay([pt for pt in sorted(inlays) if m.cls[pt[1], pt[0]] in 'pq' and not m.taken[pt[1], pt[0]]])

    # ---- 5. Directorate Security Checkpoints & Vertical East Stone Parapet (matching lumen.py:591!) ----
    # East plateau stone parapet (nr_wall_v) + brass bollards strictly on walkable rim rows (NEVER rooftops/cliffs!)
    for y in list(range(12, 18)) + list(range(20, 48)):
        if not m.taken[y, 38] and not m.cliff[y, 38]:
            m.prop('lm_bollard' if y in (12, 17, 20, 26, 32, 38, 44, 47) else 'nr_wall_v', 38, y)
    # Directorate security checkpoint rails at y=37 (x=13..17 & x=27..31 — leaves wide central & side avenues!)
    for rx0 in (13, 27):
        for i, x in enumerate(range(rx0, rx0 + 5)):
            t = 'lm_bollard' if i in (0, 4) else ('lm_railing_w' if i == 1 else 'lm_railing_e' if i == 3 else 'lm_railing_m')
            m.prop(t, x, 37)

    # ---- 6. Mounted Foundation Signpost & East Overlook Telescope (Guaranteed directly under sign events!) ----
    place_arch(m, 'pf_signpost', 18, 13)   # Base at [18, 14] -> Spire Foundation Plaque!
    place_arch(m, 'lm_viewer', 37, 29)     # Base at [37, 30] -> East Cliff Overlook!

    # ---- 7. Events (Zero duplicate links, Zero invented switches/vars, 100% reachable!) ----
    # West Return Warps [0, 33..37] -> Map 180 [84, 14] left (verified walkable on Spire Forecourt!)
    for wy in range(33, 38):
        m.events.append({
            'type': 'warp',
            'name': f'To Concourse ({wy})',
            'at': [0, wy],
            'to': {'map': 180, 'x': 84, 'y': 14, 'dir': 'left'},
        })
    m.events += [
        {
            'type': 'npc',
            'name': 'Meridian Guard W',
            'at': [20, 14],
            'sprite': 'trainer_MERIDIAN_DIRECTORATE',
            'dir': 'down',
            'text': 'Meridian Guard: Gala invitations are checked inside the Spire Lobby. Keep the forecourt lane clear for envoys.',
        },
        {
            'type': 'npc',
            'name': 'Meridian Guard E',
            'at': [24, 14],
            'sprite': 'trainer_MERIDIAN_DIRECTORATE',
            'dir': 'down',
            'text': 'Meridian Guard: The Spire was raised on the foundations of the old Aurelian sun-tower. Still stands straight after three hundred years.',
        },
        {
            'type': 'npc',
            'name': 'Spire Architect',
            'at': [14, 28],
            'sprite': 'trainer_ENGINEER',
            'dir': 'right',
            'text': 'Architect: Feel that hum through your heels? Every brass inlay in this plaza carries live Lattice current from the Spire core.',
        },
        {
            'type': 'npc',
            'name': 'Directorate Inspector',
            'at': [26, 33],
            'sprite': 'trainer_SCIENTIST',
            'dir': 'left',
            'text': 'Inspector: Security sweep complete. The executive galleries above the lobby are sealed to all non-Directorate personnel.',
        },
        {
            'type': 'npc',
            'name': 'Gala Correspondent',
            'at': [16, 39],
            'sprite': 'NPC 17',
            'dir': 'up',
            'text': 'Reporter: Sovereign Valen Corrigan is arriving for the Tenth Year Gala! Every camera in Lumen is pointed up this avenue.',
        },
        {
            'type': 'sign',
            'name': 'Spire Foundation Plaque',
            'at': [18, 14],
            'post': False,
            'text': 'MERIDIAN SPIRE — CROWN OF ZENITH. Raised on the foundations of the Aurelian sun-tower; Meridian Concord headquarters since AF 241. "Light is Work."',
        },
        {
            'type': 'sign',
            'name': 'East Cliff Overlook',
            'at': [37, 30],
            'post': False,
            'text': 'Beyond the stone parapet the plateau drops sheer into night-haze. Far below, Nadir\'s furnaces glow like embers.',
        },
        {
            'type': 'item',
            'name': 'Item',
            'at': [4, 44],
            'item': 'XSPEED',
        },
    ]

    for e in m.events:
        ex, ey = e['at']
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                m.keep_clear.add((ex + dx, ey + dy))
    m.keep_clear |= ({(x, y) for x in range(20, 25) for y in range(12, 41)}
                     | {(x, y) for x in range(0, 38) for y in (35, 36)}
                     | {(x, y) for x in range(1, 7) for y in range(43, 47)})

    # ---- 8. Soaring Marble Colonnades, Holo-Ad Pylons, Gardens & Street Furniture (ZERO tr_teal!) ----
    # Soaring marble colonnade pillars flanking the Ceremonial Plaza
    for py in (22, 26, 30, 34):
        place_arch(m, 'lm_pillar', 9, py)
        place_arch(m, 'lm_pillar', 35, py)
    # Honor-guard banner lamps & holo-ad pylons
    for x, y in ((19, 13), (25, 13), (19, 21), (25, 21), (19, 32), (25, 32)):
        m.try_put('lm_bannerlamp_w', x, y, on='pq')
    for x, y in ((10, 14), (34, 14), (17, 25), (27, 25), (5, 31)):
        m.try_put('lm_holo', x, y, on='pq')
    lamps_out(m, [(12, 16), (32, 16), (6, 31), (10, 38), (34, 38), (20, 41), (24, 41)])
    for nm, x, y in (
        ('lm_viewer', 37, 15), ('lm_viewer', 37, 42),
        ('lm_kiosk', 14, 38), ('lm_shelter', 3, 30), ('lm_clock', 30, 14), ('lm_news', 31, 38),
        ('lm_statue', 13, 13), ('lm_statue', 29, 13),
        ('lm_bench', 19, 23), ('lm_bench', 24, 23), ('lm_bench', 11, 38), ('lm_bench', 33, 39),
        ('lm_bench', 21, 43), ('lm_planter3', 15, 16), ('lm_planter3', 27, 16), ('lm_planter', 35, 15),
        ('lm_topiary', 17, 22), ('lm_topiary', 27, 22), ('lm_topiary', 17, 32), ('lm_topiary', 27, 32),
        ('lm_stall_c', 7, 38),
    ):
        m.try_put(nm, x, y, on='pq')

    # Lush Ornamental Gardens (compact lm_tree + azaleas/topiaries sized cleanly for 6x4 parterres; ZERO tr_teal!)
    for nm, x, y in (
        ('nt_azalea0', 11, 22), ('nt_azalea1', 15, 24), ('nt_azalea2', 28, 22), ('nt_shrub0', 32, 24),
        ('lm_tree', 12, 31), ('nt_azalea1', 14, 32), ('lm_topiary', 11, 33), ('nt_shrub1', 15, 33),
        ('lm_tree', 30, 31), ('nt_azalea2', 28, 32), ('lm_topiary', 33, 33), ('nt_shrub0', 29, 33),
        ('tr_oak', 9, 41), ('tr_pink', 17, 42), ('nt_azalea0', 9, 45), ('nt_azalea1', 14, 45), ('nt_shrub0', 18, 45),
        ('nt_teal_a', 25, 41), ('tr_oak2', 29, 42), ('tr_pine', 34, 41),
        ('nt_azalea2', 24, 45), ('nt_azalea0', 28, 45), ('nt_shrub1', 32, 45), ('nt_azalea1', 35, 44),
        ('tr_pink', 1, 39), ('nt_azalea0', 4, 40), ('nt_shrub0', 1, 41),
    ):
        m.try_put(nm, x, y, on='.')

    scatter_wear_out(m, n_per_100=7, on='pq', seed=195)
    m.paint()
    m.scatter(n_per_100=24, seed=195, on='.')
    dress_roofs_out(m, seed=195)
    add_water_glints(m, seed=195)

    # Refined limestone plaza border accents (ZERO dark-brown lm_low0 potholes!)
    pave0 = P1('lm_pave0')
    for x in range(10, 36):
        for y in (20, 36):
            if m.cls[y, x] == 'q' and not m.cliff[y, x] and m.L[1, y, x] in (P1('lm_plaza0'), P1('lm_plaza1')):
                m.L[0, y, x] = pave0; m.L[1, y, x] = pave0
    paint_sunburst(m, 20, 26)

    head = {
        'id': 195,
        'name': 'Lumen City - Spire District',
        'parent': 180,
        'bgm': 'Cedolan City',
        'field': 'NEON_GRID',
        'rubric': True,
        'tone': [4, 2, 0, 0],
        'metadata': {
            'Outdoor': True,
            'ShowArea': True,
            'MapPosition': [0, 16, 16],
            'Name': 'Spire District',
        },
        '_file': '195_lumen_spire_district.yaml',
    }
    return write_ts60(m, 195, head, '# GENERATED by mapgen/layouts/lumen_upper_wards.py (Batch 1A Act 1 Craft): 195 Spire District.\n')


# ==============================================================================
# MAP 196: LUMEN CITY - SKYPORT TERRACE (40x36, Outside TS60)
# ==============================================================================
def build_196():
    """196: Lumen City - Skyport Terrace (40x36, Outside TS60).
    Sunlit elevated airship promenade north of 180 Concourse.
    Skyport Customs door [20, 6] LC_SKYPORT -> 959.
    South return steps [18..22, 35] -> 180 [74, 6] down.
    """
    W, H = 40, 36
    m = City(W, H, 196, base='p')
    m.ht[:] = 2
    m.roof_kind = 'V'

    # ---- 1. Elevated Sky-Void Overlook & Twin Jutting Airship Mooring Piers ----
    # Open sky/cloud-abyss along the north rim & side plateau lips (cls='x', ht=0)
    m.cls[0:10, :] = 'x'; m.ht[0:10, :] = 0
    m.cls[:, 0:2] = 'x'; m.ht[:, 0:2] = 0
    m.cls[:, 38:40] = 'x'; m.ht[:, 38:40] = 0

    # Central Skyport Customs Promontory FLUSH with lb_gate (8x5 at x=16..23, y=2..6 -> ZERO grey wrapper rim!)
    m.cls[2:15, 16:24] = 'q'; m.ht[2:15, 16:24] = 2
    # West Airship Boarding Pier jutting north over the sky-drop (x=4..10, y=5..14, ht=2)
    m.cls[5:15, 4:11] = 'q'; m.ht[5:15, 4:11] = 2
    # East Airship Boarding Pier jutting north over the sky-drop (x=29..35, y=5..14, ht=2)
    m.cls[5:15, 29:36] = 'q'; m.ht[5:15, 29:36] = 2

    # Central Sunlit Departure Concourse (x=11..28, y=15..29)
    m.rect(11, 15, 18, 15, 'q')
    # South Grand Arrival Apron (x=15..25, y=30..35)
    m.rect(15, 30, 11, 6, 'q')

    # ---- 2. Skyport Customs Terminal ([20, 6] LC_SKYPORT -> 959!) & Pier-Seated Airship Mooring Masts ----
    # lb_gate (8x5, door=[4,4], marble + clock + blue aviation flag!) at (16, 2) -> door EXACTLY at [20, 6]!
    m.put('lb_gate', 16, 2, link='LC_SKYPORT', dname='Skyport Customs')

    # Moored Airships hovering cleanly beside West & East Boarding Piers + Mooring Masts seated squarely ON pier corners!
    abyss_piece(m, 'lm_airship', 4, 0)     # West Berth W1: Sallow Line's Dauntless (x=4..9, y=0..2)
    abyss_piece(m, 'lm_airship', 30, 0)    # East Berth E1: Meridian Courier (x=30..35, y=0..2)
    for mx in (4, 10, 29, 35):             # Seated firmly on marble pier corners (y=5) instead of floating in void!
        place_arch(m, 'lm_mast', mx, 1)

    # ---- 3. Manicured Sunlit Sky-Terrace Gardens & SE Static Tunnels Stone Headhouse ----
    m.rect(3, 17, 7, 7, '.'); m.rect(5, 19, 3, 3, 'w')     # West Wind-Swept Reflection Garden
    m.rect(30, 17, 7, 7, '.'); m.rect(32, 19, 3, 3, 'w')   # East Wind-Swept Reflection Garden
    m.rect(3, 27, 11, 7, '.')                              # SW Departure Grove Park
    m.rect(26, 27, 7, 7, '.')                              # SE Perimeter Grove Park (cleanly west of Static Tunnels headhouse!)

    # Solid raised stone-and-slate Static Tunnels Maintenance Headhouse at (33..36, 27..30) with paved approach (33..36, 31..33)!
    m.ht[27:29, 33:37] = 3
    m.fill(33, 27, 36, 28)
    m.rect(33, 31, 4, 3, 'p')

    # ---- 4. Navigation Sunburst Compass, Boarding Carpet & Brass Taxiway Inlays ----
    # Crimson boarding carpet from Skyport Customs door (20,6) down to concourse (20,14)
    for y in range(7, 15):
        for i, x in enumerate((19, 20, 21)):
            m.over.append((1, x, y, P1('lm_carpet_' + ('w' if i == 0 else 'e' if i == 2 else 'c'))))
    # 5x5 Golden Meridian Compass Sunburst at concourse heart (18, 19) -> x=18..22, y=19..23
    m.put('lm_sun', 18, 19, force=True)

    # Sweeping brass navigation inlays linking West Pier, Customs Terminal, East Pier & South Steps
    inlays = set()
    for x in range(7, 33):
        inlays.add((x, 15))
    for y in range(7, 16):
        inlays.add((7, y))
        inlays.add((32, y))
    for x in range(13, 28):
        inlays.add((x, 26))
    for y in range(16, 33):
        inlays.add((15, y))
        inlays.add((25, y))
    m.inlay([pt for pt in sorted(inlays) if m.cls[pt[1], pt[0]] in 'pq' and not m.taken[pt[1], pt[0]]])

    # ---- 5. Scenic Sky-Parapets, Boarding Gangway Bollards & South Return Steps ----
    # Boarding pier north railings (y=5, clear of seated pier-corner masts at x=4,10,29,35!)
    for rx in (5, 6, 8, 9, 30, 31, 33, 34):
        m.prop('lm_bollard' if rx in (6, 8, 31, 33) else 'lm_railing_m', rx, 5)
    # West & East vertical stone parapets (nr_wall_v) + brass bollards along x=2 and x=37 (y=10..35; ZERO horizontal ladders!)
    for y in range(10, 36):
        for rx in (2, 37):
            if not m.taken[y, rx] and not m.cliff[y, rx]:
                m.prop('lm_bollard' if y in (10, 15, 20, 25, 30, 35) else 'nr_wall_v', rx, y)
    # South grand return stairs (x=18..22, y=34..35) -> 180 [74, 6] down!
    for y in (34, 35):
        for i, x in enumerate(range(18, 23)):
            m.over.append((1, x, y, P1('lm_stair_' + ('l' if i == 0 else 'r' if i == 4 else 'm'))))
    for x in range(15, 26):
        if x not in range(18, 23):
            m.prop('lm_bollard' if x in (15, 17, 23, 25) else 'lm_railing_m', x, 35)
    # Recessed armored steel Static Tunnels hatch mounted flush into the raised stone headhouse face at (35, 29..30)!
    place_arch(m, 'lm_sdoor', 35, 29)
    for x in (34, 36):
        m.prop('lm_bollard', x, 31)

    # ---- 6. Mounted Schedule Board & Skyport Overlook Telescope (Guaranteed directly under sign events!) ----
    place_arch(m, 'lm_news', 23, 7)      # Base at [23, 8] -> Departure Schedule!
    place_arch(m, 'lm_viewer', 3, 12)    # Base at [3, 13] -> Skyport Overlook!

    # ---- 7. Events (100% Static Diegetic Lore + Clean Links/Warps; Zero Invented Switches/Vars) ----
    for wx in range(18, 23):
        m.events.append({
            'type': 'warp',
            'name': f'To Concourse ({wx})',
            'at': [wx, 35],
            'to': {'map': 180, 'x': 74, 'y': 6, 'dir': 'down'},
        })
    m.events += [
        {
            'type': 'npc',
            'name': 'Airship Captain',
            'at': [7, 10],
            'sprite': 'trainer_SAILOR',
            'dir': 'down',
            'text': 'Captain: The Sallow Line\'s Dauntless made Lumen twenty minutes ahead of the gale. Finest timber hull above the clouds.',
        },
        {
            'type': 'npc',
            'name': 'Dock Quartermaster',
            'at': [32, 10],
            'sprite': 'trainer_ENGINEER',
            'dir': 'down',
            'text': 'Quartermaster: Meridian Courier\'s loaded with Tenth Year lamp glass and champagne crates. Mind the mooring lines!',
        },
        {
            'type': 'npc',
            'name': 'Skyport Attendant',
            'at': [18, 8],
            'sprite': 'NPC 20',
            'dir': 'down',
            'text': 'Attendant: Skyport Customs is straight ahead. Ticketed passengers for Skyreach and Crownhaven check in at the brass desk.',
        },
        {
            'type': 'npc',
            'name': 'Cloud-Watcher',
            'at': [13, 21],
            'sprite': 'NPC 19',
            'dir': 'up',
            'text': 'Traveller: When the wind turns off the Stormfront you can smell ozone all the way across this terrace.',
        },
        {
            'type': 'sign',
            'name': 'Departure Schedule',
            'at': [23, 8],
            'post': False,
            'text': 'LUMEN SKYPORT TERRACE — BERTH W1: SALLOW LINE "DAUNTLESS" (MOORED). BERTH E1: MERIDIAN COURIER. SKYREACH SHUTTLE: DIPLOMATIC CHARTER STANDBY.',
        },
        {
            'type': 'sign',
            'name': 'Static Tunnels Gate',
            'at': [35, 30],
            'post': False,
            'text': 'STATIC TUNNELS — SUB-TERRACE RAIL SPUR. Sealed for Tenth Year Gala security. Flash illumination required inside.',
        },
        {
            'type': 'sign',
            'name': 'Skyport Overlook',
            'at': [3, 13],
            'post': False,
            'text': 'Cloud-banks drift level with the stone parapet. Far north, the silver airship lanes vanish toward Crownhaven.',
        },
        {
            'type': 'item',
            'name': 'Item',
            'at': [4, 29],
            'item': 'HYPERPOTION',
        },
    ]

    for e in m.events:
        ex, ey = e['at']
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                m.keep_clear.add((ex + dx, ey + dy))
    m.keep_clear |= ({(x, y) for x in range(18, 23) for y in range(6, 36)}
                     | {(x, y) for x in range(6, 34) for y in (14, 15, 16)}
                     | {(7, y) for y in range(6, 16)} | {(32, y) for y in range(6, 16)}
                     | {(35, 31), (35, 32)})

    # ---- 8. Luggage Cargo, Beacon Posts, Boarding Shelters & Lush Rooftop Gardens (ZERO floating bulbs/awnings, ZERO tr_teal!) ----
    for x, y in ((16, 9), (23, 10), (16, 29), (24, 29), (11, 16), (28, 16), (11, 28), (28, 28),
                 (5, 11), (9, 11), (30, 11), (34, 11), (17, 17), (23, 17), (17, 25), (23, 25),
                 (15, 30), (25, 30)):
        m.try_put('lm_bannerlamp_w', x, y, on='pq')
    lamps_out(m, [(5, 13), (10, 13), (30, 13), (35, 13), (12, 18), (28, 18), (12, 27), (28, 27),
                  (16, 14), (24, 14), (15, 33), (25, 33), (4, 16), (35, 16)])
    for nm, x, y in (
        ('hb_barrels', 5, 8), ('hb_barrels', 9, 8), ('hb_barrels', 30, 8), ('hb_barrels', 34, 8),
        ('lm_shelter', 12, 11), ('lm_shelter', 26, 11),
        ('lm_kiosk', 24, 17), ('lm_kiosk', 12, 17), ('lm_clock', 14, 11), ('lm_holo', 26, 22), ('lm_news', 14, 24),
        ('lm_bench', 12, 21), ('lm_bench', 26, 21), ('lm_bench', 16, 32), ('lm_bench', 23, 32),
        ('lm_viewer', 36, 12), ('lm_viewer', 3, 25), ('lm_viewer', 36, 25),
        ('lm_planter3', 13, 17), ('lm_planter3', 24, 27), ('lm_planter', 16, 7), ('lm_planter', 22, 11),
        ('lm_topiary', 16, 19), ('lm_topiary', 24, 19), ('lm_topiary', 16, 24), ('lm_topiary', 24, 24),
        ('lm_topiary', 11, 20), ('lm_topiary', 28, 20),
        ('lm_stall_a', 11, 24), ('lm_stall_b', 25, 24),
        ('lm_tree', 14, 31), ('lm_tree', 25, 31),
        ('lm_tree', 15, 12), ('lm_tree', 24, 12),
    ):
        m.try_put(nm, x, y, on='pq')

    # Rich Wind-Swept Botanical Rooftop Gardens (ALL trees cleanly fitted in both SW & SE parks; ZERO tr_teal!)
    for nm, x, y in (
        ('tr_pink', 3, 17), ('tr_oak', 7, 17), ('lm_tree', 3, 21), ('lm_tree', 8, 21), ('nt_azalea1', 6, 22),
        ('tr_oak', 34, 17), ('tr_pink', 30, 17), ('lm_tree', 34, 21), ('lm_tree', 30, 21), ('nt_azalea0', 32, 22),
        ('tr_oak2', 7, 27), ('tr_pink', 10, 28), ('lm_tree', 12, 31), ('tr_pine', 4, 30),
        ('nt_azalea1', 4, 32), ('nt_azalea2', 8, 32), ('nt_shrub0', 11, 32), ('lm_topiary', 3, 32),
        ('tr_pine', 26, 27), ('tr_oak', 29, 27), ('lm_tree', 26, 31), ('lm_tree', 31, 31),
        ('nt_azalea0', 28, 31), ('nt_azalea1', 30, 32), ('nt_shrub1', 27, 32),
        ('lm_tree', 3, 24), ('lm_tree', 35, 24),
    ):
        m.try_put(nm, x, y, on='.pq')

    scatter_wear_out(m, n_per_100=26, on='pq', seed=196)
    # Contiguous (step=1) festoon light strands anchored pixel-for-pixel between arclamp heads (5,11)-(10,11) & (30,11)-(35,11)!
    for x in (6, 7, 8, 9, 31, 32, 33, 34):
        if m.inb(x, 11) and not m.taken[11, x]:
            m.over.append((2, x, 11, P1('lm_bulbs%d' % (x % 3))))
    m.paint()
    m.scatter(n_per_100=24, seed=196, on='.')
    dress_roofs_out(m, seed=196)
    add_water_glints(m, seed=196)

    # Crisp limestone departure pad trim (ZERO dark sewer grates jammed into boarding railings!)
    pave0 = P1('lm_pave0')
    for x in range(11, 29):
        for y in (15, 29):
            if m.cls[y, x] == 'q' and not m.cliff[y, x] and m.L[1, y, x] in (P1('lm_plaza0'), P1('lm_plaza1')):
                m.L[0, y, x] = pave0; m.L[1, y, x] = pave0
    paint_sunburst(m, 18, 19)

    head = {
        'id': 196,
        'name': 'Lumen City - Skyport Terrace',
        'parent': 180,
        'bgm': 'Ingido Plateau',
        'field': 'STORMFRONT',
        'rubric': True,
        'tone': [8, 6, 4, 0],
        'metadata': {
            'Outdoor': True,
            'ShowArea': True,
            'MapPosition': [0, 16, 16],
            'Name': 'Skyport Terrace',
        },
        '_file': '196_lumen_skyport_terrace.yaml',
    }
    return write_ts60(m, 196, head, '# GENERATED by mapgen/layouts/lumen_upper_wards.py (Batch 1A Act 1 Craft): 196 Skyport Terrace.\n')


# ==============================================================================
# MAP 197: ZENITH COUNCIL HALL - COUNCIL CHAMBER (31x23, TS60 cvY + lmw)
# ==============================================================================
def build_197():
    """197: Zenith Council Hall - Council Chamber (31x23, TS60).
    Monumental semicircular / tiered Zenith Council assembly hall (ZERO floor chandeliers!).
    Exit [15, 22] LC_COUNCIL -> 194 [24, 8] (step out [24, 9] down).
    """
    W, H = 31, 23
    m = room60(W, H, 'Y', 197)
    m.kit = {TER: 'lmw', FLOOR: 'cvY', 'default': 'cvY'}

    # ---- 1. Sculpted Domed Hemicycle Chamber Silhouette (NO flat rectangle!) ----
    m.box(2, 5, 28, 18, FLOOR, '.')
    m.box(5, 19, 25, 19, FLOOR, '.')
    m.box(8, 20, 22, 20, FLOOR, '.')
    m.box(11, 21, 19, 21, FLOOR, '.')
    m.box(14, 22, 16, 22, FLOOR, '.')
    # Sculpt curved/stepped hemicycle outer shoulders into cvY wall mass
    m.mass_at([
        (2, 5), (3, 5), (27, 5), (28, 5),
        (2, 17), (2, 18), (3, 18), (4, 18),
        (28, 17), (28, 18), (27, 18), (26, 18),
    ])

    # ---- 2. Elevated North Presiding Rostrum Dais (TER -> lmw marble balustrade!) ----
    m.box(9, 3, 21, 7, TER, '.')
    # Monumental 5-wide ceremonial staircase descending from Presiding Rostrum (x=13..17, y=7..9)
    # Leaving (13, 6) & (17, 6) wide open around the 3-wide Chair's podium (14..16, 6) so 100% of the dais is walkable!
    m.stairs(13, 7, w=5, n=3, c='.')
    m.plan_cliffs(rows=3)

    # ---- 3. Events (Zero invented switches/vars; 100% reachable!) ----
    m.events += [
        {
            'type': 'exit',
            'at': [15, 22],
            'link': 'LC_COUNCIL',
            'arrive': [15, 21, 'up'],
        },
        {
            'type': 'npc',
            'name': 'Council Clerk',
            'at': [13, 18],
            'sprite': 'NPC 22',
            'dir': 'down',
            'text': 'Council Clerk: Welcome to the Zenith Council Chamber. Here the Six Founding Houses sit in assembly and name Zenith\'s Festival champions.',
        },
        {
            'type': 'npc',
            'name': 'House Sallow Aide',
            'at': [8, 14],
            'sprite': 'NPC 14',
            'dir': 'right',
            'text': 'Aide: Councillor Sallow argues every session for Nadir representation. Every session, the Meridian bloc tables the motion.',
        },
        {
            'type': 'npc',
            'name': 'Council Archivist',
            'at': [22, 14],
            'sprite': 'NPC 20',
            'dir': 'left',
            'text': 'Archivist: Six oak benches for the Six Founding Houses, raised under the Charter of AF 118. The seventh seat was left unbuilt on purpose.',
        },
        {
            'type': 'sign',
            'name': 'Presiding Rostrum',
            'at': [15, 6],
            'post': False,
            'text': 'CHAIR OF THE ZENITH COUNCIL — AURELIAN VOSS. An inlaid brass gavel rests beside neat stacks of Tenth Year Mandate decrees.',
        },
        {
            'type': 'sign',
            'name': 'Founding Charter Plaque',
            'at': [11, 12],
            'post': False,
            'text': 'CHARTER OF ZENITH, AF 118: "Light is Work; Order is Light." Signed by Houses Halcyon, Sallow, Strade, Calder, Vance, and Voss.',
        },
        {
            'type': 'sign',
            'name': 'Festival Delegation Plaque',
            'at': [19, 12],
            'post': False,
            'text': 'PRISM FESTIVAL OF AF 300 — Zenith\'s delegation shall depart from this chamber under the Seal of the Council.',
        },
    ]

    m.keep_clear |= ({(x, y) for x in (14, 15, 16) for y in range(6, 23)}
                     | {(x, y) for x in range(9, 22) for y in (10, 11, 17, 18)}
                     | {(8, 13), (8, 14), (8, 15), (9, 14), (22, 13), (22, 14), (22, 15), (21, 14),
                        (13, 18), (13, 19), (12, 18), (15, 5), (15, 6), (14, 6), (16, 6),
                        (11, 13), (10, 12), (12, 12), (19, 13), (18, 12), (20, 12)})

    # ---- 4. Grand North Apse Architecture: Six Founding House Banners, Arched Windows & Sconces ----
    for wx in (11, 15, 19):
        hang(m, 'lm_window', wx, 3)
    for bx, bn in ((10, 'lm_banner'), (13, 'lm_banner_w'), (17, 'lm_banner_w'), (20, 'lm_banner'),
                   (6, 'lm_banner'), (24, 'lm_banner_w')):
        hang(m, bn, bx, 3 if 10 <= bx <= 20 else 5)
    on_faces(m, 'mn_sconce', [(12, 4), (14, 4), (16, 4), (18, 4), (5, 6), (8, 6), (22, 6), (25, 6)])

    # ---- 5. High Presiding Rostrum (Voss's Chair + Brass-Oak Debating Podium) ----
    for x, part in ((14, 'l'), (15, 'm'), (16, 'r')):
        m.over.append((1, x, 6, P1('lm_counter_' + part)))
        m.taken[6, x] = True
    m.over.append((2, 14, 6, P1('mn_dt_cand')))
    m.over.append((2, 16, 6, P1('mn_orchid')))
    m.over.append((1, 15, 5, P1('mn_chairR_down')))
    m.taken[5, 15] = True
    # Asymmetric rostrum clerk & archival wings
    place_arch(m, 'mn_sideboard2', 11, 5)
    m.over.append((2, 12, 5, P1('mn_dt_plate')))
    place_arch(m, 'mn_console', 18, 5)
    place_arch(m, 'lm_pillar', 9, 3)
    place_arch(m, 'lm_pillar', 21, 3)

    # ---- 6. Semicircular Founding House Debating Benches (Varied Mahogany Desks + Velvet Seats) ----
    # West Debating Tier (x=6..7, y=11..15) w/ globe & candelabra
    for bx, by in ((6, 11), (6, 14)):
        place_arch(m, 'mn_sideboard2', bx, by)
    m.over.append((2, 6, 11, P1('mn_globe')))
    m.over.append((2, 7, 14, P1('mn_dt_plate')))
    for cx, cy, ch in ((6, 12, 'mn_chairR_up'), (7, 12, 'mn_chairR_up'), (6, 15, 'mn_chairR_up'), (7, 15, 'mn_chairR_up')):
        m.over.append((1, cx, cy, P1(ch)))
        m.taken[cy, cx] = True

    # East Debating Tier (x=23..24, y=11..15) w/ archival tea & candelabra
    for bx, by in ((23, 11), (23, 14)):
        place_arch(m, 'mn_sideboard2', bx, by)
    m.over.append((2, 24, 11, P1('mn_dt_cand')))
    m.over.append((2, 23, 14, P1('mn_tea')))
    for cx, cy, ch in ((23, 12, 'mn_chairR_up'), (24, 12, 'mn_chairR_up'), (23, 15, 'mn_chairR_up'), (24, 15, 'mn_chairR_up')):
        m.over.append((1, cx, cy, P1(ch)))
        m.taken[cy, cx] = True

    # South Hemicycle Arc Benches (facing north toward Chair's rostrum; ZERO pillar collision!)
    for sx in (9, 10, 11):
        m.over.append((1, sx, 16, P1('lm_counter_' + ('l' if sx == 9 else 'r' if sx == 11 else 'm'))))
        m.taken[16, sx] = True
    m.over.append((1, 10, 17, P1('mn_chairR_up'))); m.taken[17, 10] = True
    for sx in (19, 20, 21):
        m.over.append((1, sx, 16, P1('lm_counter_' + ('l' if sx == 19 else 'r' if sx == 21 else 'm'))))
        m.taken[16, sx] = True
    m.over.append((1, 20, 17, P1('mn_chairR_up'))); m.taken[17, 20] = True

    # ---- 7. West & East Spectator Gallery Balconies, Asymmetric Furnishings & Clean South Colonnade ----
    # Ceremonial forged brass bollard posts dividing outer spectator boxes (x=4 & x=26 — ZERO vertical lm_railing_m ladders!)
    for ry in (10, 12, 14, 15):
        m.over.append((1, 4, ry, P1('lm_bollard'))); m.taken[ry, 4] = True
        m.over.append((1, 26, ry, P1('lm_bollard'))); m.taken[ry, 26] = True
    for sy in (11, 14):
        m.over.append((1, 2, sy, P1('mn_chairR_right'))); m.taken[sy, 2] = True
        m.over.append((1, 28, sy, P1('mn_chairR_left'))); m.taken[sy, 28] = True

    # Fluted marble colonnade cleanly clear of chairs (10,17)/(20,17) and Clerk [13,18]!
    for px, py in ((5, 7), (25, 7), (8, 17), (22, 17)):
        place_arch(m, 'lm_pillar', px, py)
    # Deliberately asymmetric West (Library/Clock/Sofa) vs East (Archive/Palm/Bench) furnishings to keep mirror < 25%!
    place_arch(m, 'mn_books2', 6, 7)
    place_arch(m, 'lm_clock', 8, 7)
    place_arch(m, 'mn_sideboard2', 23, 7)
    m.over.append((2, 23, 7, P1('mn_orchid')))
    place_arch(m, 'lm_arclamp', 22, 7)
    # Marble Charter & Delegation Statues directly mounting [11, 12] & [19, 12] plaque sign events!
    place_arch(m, 'mn_statue', 11, 11)
    place_arch(m, 'mn_statue', 19, 11)
    place_arch(m, 'mn_candelabra', 12, 14)
    place_arch(m, 'mn_palm', 18, 13)
    for nm, x, y in (
        ('mn_sofa', 5, 19), ('lm_bench', 23, 19),
        ('mn_table_s', 6, 17), ('mn_bust', 24, 16),
        ('lm_plant', 12, 20), ('lm_plant', 18, 20),
        ('lm_bannerlamp_w', 12, 19), ('lm_bannerlamp_w', 18, 19),
        ('lm_planter', 11, 21), ('lm_planter', 18, 21),
    ):
        put_if(m, nm, x, y)

    # ZERO floor-level lm_chand / mn_chandelier decals and ZERO smeared pf_glow / cv_shaft blobs!
    m.paint()

    # ---- 8. Post-Paint Stately Parliament Marble Floor, Golden Sunburst & Warm Crimson Carpets ----
    paves = [P1('lm_pave%d' % i) for i in range(4)]
    plazas = [P1('lm_plaza0'), P1('lm_plaza1')]
    for y in range(H):
        for x in range(W):
            if m.cls[y, x] == '.':
                perim = (x <= 5 or x >= 25 or y >= 19)
                if perim:
                    m.L[0, y, x] = paves[(x * 7 + y * 13) % 4]
                else:
                    # Subtle organic marble slab grain (breaks exact L-R mirror palindrome while staying stately!)
                    m.L[0, y, x] = plazas[(x + y + (1 if x > 15 and (x * 3 + y) % 3 == 0 else 0)) & 1]

    # Glowing brass-and-cyan floor inlay framing the Sunburst well cleanly at y=10..15 (NEVER hitting y=16..17 chairs/benches!)
    for x in range(11, 20):
        if x not in (14, 15, 16) and m.cls[10, x] == '.':
            m.L[0, 10, x] = P1('lm_inlay_h')
        if x not in (13, 14, 15, 16, 17) and m.cls[15, x] == '.':
            m.L[0, 15, x] = P1('lm_inlay_h')
    for y in range(11, 15):
        for x in (10, 20):
            if m.cls[y, x] == '.':
                m.L[0, y, x] = P1('lm_inlay_v')
    for ix, iy, k in ((10, 10, 'se'), (20, 10, 'sw'), (10, 15, 'ne'), (20, 15, 'nw')):
        if m.cls[iy, ix] == '.':
            m.L[0, iy, ix] = P1('lm_inlay_' + k)

    # 5x5 Golden Meridian Sunburst Medallion centered in the Debating Floor (13..17, 11..15)
    sun_L = STAMPS['lm_sun']['layers'][0]
    for dy in range(5):
        for dx in range(5):
            if m.cls[11 + dy, 13 + dx] == '.' and m.L[1, 11 + dy, 13 + dx] == 0:
                m.L[0, 11 + dy, 13 + dx] = sun_L[dy][dx]

    # Royal crimson carpets: Entrance Runner, Elevated Presiding Rostrum & Spectator Boxes
    floor_carpet_cave(m, 14, 16, 16, 22)
    floor_carpet_cave(m, 11, 5, 19, 6)
    floor_carpet_cave(m, 2, 10, 3, 15)
    floor_carpet_cave(m, 27, 10, 28, 15)

    head = {
        'id': 197,
        'name': 'Zenith Council Hall - Council Chamber',
        'parent': 194,
        'bgm': 'Cedolan City',
        'field': 'NONE',
        'tone': [6, 2, -4, 6],
        'metadata': {
            'MapPosition': [0, 16, 16],
            'SnapEdges': True,
        },
        '_file': '197_zenith_council_chamber.yaml',
    }
    return write_ts60(m, 197, head, '# GENERATED by mapgen/layouts/lumen_upper_wards.py (Batch 1A Act 1 Craft): 197 Council Chamber.\n')


# ==============================================================================
# MAP 198: MERIDIAN SPIRE - EXECUTIVE GALLERY (31x19, TS60 cvZ Obsidian-Gold)
# ==============================================================================
def build_198():
    """198: Meridian Spire - Executive Gallery (31x19, TS60).
    Sleek obsidian-marble & gold-trim executive sky-gallery above 185 Spire Lobby.
      - South Executive Lift [15, 18] -> 185 [12, 6] down
      - NE Fortified Core Security Lift [28, 2] -> 199 [12, 23] up (arrival from 199: [28, 3] down)
    """
    W, H = 31, 19
    m = room60(W, H, 'Z', 198)
    m.kit = {FLOOR: 'cvZ', 'default': 'cvZ'}

    # ---- 1. Sculpted Obsidian-Gold Executive Sky-Gallery Silhouette ----
    # Start floor at y=1 so cvZ north wall occupies y=0..2 (windows on y=1..2, walkable floor starts y=3!)
    m.box(2, 1, 29, 15, FLOOR, '.')
    m.box(5, 16, 26, 16, FLOOR, '.')
    m.box(9, 17, 22, 17, FLOOR, '.')
    m.box(14, 18, 16, 18, FLOOR, '.')
    # Sculpt chamfered executive gallery corners into dark obsidian wall mass
    m.mass_at([(2, 15), (3, 15), (28, 15), (29, 15), (2, 14), (29, 14)])
    m.plan_cliffs(rows=3)

    # ---- 2. Events (Clean Warps to 185 & 199; Zero Invented Switches/Vars) ----
    m.events += [
        {
            'type': 'warp',
            'name': 'Executive Lift to Lobby',
            'at': [15, 18],
            'to': {'map': 185, 'x': 12, 'y': 6, 'dir': 'down'},
            'se': 'Door exit',
        },
        {
            'type': 'warp',
            'name': 'Core Security Lift',
            'at': [28, 2],
            'to': {'map': 199, 'x': 12, 'y': 23, 'dir': 'up'},
            'se': 'Door exit',
        },
        {
            'type': 'sign',
            'name': 'Aurelian Artifact Case',
            'at': [6, 7],
            'post': False,
            'text': 'EXHIBIT 01 — SITE AURELIA, AF 289. A shard of resonant dark crystal sealed in cyan stasis glass, dredged from beneath the Sump. The glass feels oddly cold.',
        },
        {
            'type': 'sign',
            'name': 'Gilded King Mural',
            'at': [9, 2],
            'post': False,
            'text': 'A restored Aurelian mural of the Gilded King beneath an eighteen-pillared sun-tower. Its silhouette matches Meridian Spire.',
        },
        {
            'type': 'sign',
            'name': 'Lattice Telemetry Console',
            'at': [22, 6],
            'post': False,
            'text': 'LUMEN GRID TELEMETRY — ALL EIGHTEEN CALIBRATION CHANNELS STANDBY. SUB-VAULT CORE RESONANCE: NOMINAL. CLEARANCE: CHAIR VOSS.',
        },
        {
            'type': 'npc',
            'name': 'Executive Curator',
            'at': [11, 10],
            'sprite': 'NPC 24',
            'dir': 'left',
            'text': 'Curator: Chair Voss funded three expeditions beneath the Sump to assemble this wing. He calls it "knowing what we stand on."',
        },
        {
            'type': 'npc',
            'name': 'Spire Security Officer',
            'at': [26, 5],
            'sprite': 'trainer_MERIDIAN_DIRECTORATE',
            'dir': 'left',
            'text': 'Directorate Officer: That fortified lift goes straight down to the Dark Stone Core. Only Chair Voss and Chief Engineer Strade carry keys.',
        },
    ]

    m.keep_clear |= ({(x, y) for x in (14, 15, 16) for y in range(4, 19)}
                     | {(28, 2), (28, 3), (28, 4), (28, 5), (27, 4), (26, 4), (26, 5), (25, 5),
                        (6, 8), (5, 7), (7, 7), (9, 3), (22, 7), (21, 7), (11, 10), (11, 11), (10, 10), (12, 10)})

    # ---- 3. Panoramic Glass Curtain North Wall (y=1..2; ZERO clipped windows!) ----
    for wx in (4, 6, 12, 14, 16, 18, 21, 24):
        hang(m, 'lm_window', wx, 1)
    on_faces(m, 'mn_portK', [(8, 2)])
    on_faces(m, 'mn_portQ', [(9, 2)])
    on_faces(m, 'mn_portL', [(10, 2)])
    on_faces(m, 'mn_portF', [(20, 2)])
    hang(m, 'lm_monitors', 22, 1)
    on_faces(m, 'lm_alarm_on', [(26, 2)])
    on_faces(m, 'mn_sconce', [(3, 2), (7, 2), (11, 2), (19, 2), (25, 2)])

    # ---- 4. West Aurelian Artifact Gallery (Curated Museum Variety — ZERO cloned cyan orbs!) ----
    m.put('lm_case', 5, 6)          # Primary Site Aurelia stasis display case (sign right at [6, 7]!)
    place_arch(m, 'lm_cradle_cold', 9, 6)  # Empty calibration cradle exhibit cleanly on marble (off carpet!)
    place_arch(m, 'mn_statue', 5, 10)      # Aurelian marble figure
    place_arch(m, 'mn_bust', 9, 10)        # Classical founder bust
    place_arch(m, 'mn_plinth', 3, 9)       # Spotlighted reliquary plinth cleanly inside west crimson runner
    put_if(m, 'mn_sofa', 6, 14)
    put_if(m, 'lm_bench', 9, 14)

    # ---- 5. Central Executive Atrium & Flanking Fluted Colonnades (100% clear of floor inlays!) ----
    for px, py in ((11, 4), (19, 4), (11, 13), (19, 13)):
        place_arch(m, 'lm_pillar', px, py)
    for bx, by in ((11, 16), (19, 16)):
        put_if(m, 'lm_bannerlamp_w', bx, by)
    put_if(m, 'lm_plant', 12, 16)
    put_if(m, 'lm_plant', 18, 16)
    place_arch(m, 'lm_arclamp', 13, 4)
    place_arch(m, 'lm_arclamp', 17, 4)

    # ---- 6. East Voss Executive Wing, Real Telemetry Console & Illuminated Core Security Lift ----
    # Authentic executive telemetry console (mn_console 2x1 at 21..22, 6 -> sign right at [22, 6]!) + junction node
    place_arch(m, 'mn_console', 21, 6)
    m.over.append((1, 23, 6, P1('lm_junction_on'))); m.taken[6, 23] = True
    m.over.append((1, 22, 5, P1('mn_chairR_down'))); m.taken[5, 22] = True
    place_arch(m, 'mn_books2', 20, 10)
    place_arch(m, 'mn_table_s', 22, 10)
    m.over.append((2, 22, 10, P1('mn_globe')))   # Brass zenith globe exhibit (no duplicate cyan orb!)
    place_arch(m, 'lm_clock', 25, 11)
    put_if(m, 'lm_rack', 24, 9)
    # Replace outdoor pink street billboard with sleek dark server cabinet + parlor palm!
    place_arch(m, 'lm_rack', 27, 10)
    put_if(m, 'lm_plant', 28, 13)
    put_if(m, 'mn_sofa', 21, 14)
    put_if(m, 'lm_planter', 25, 14)

    # Forged brass security divider along y=8 separating restricted NE Core Lift vestibule (x=24..25 open!)
    for x, t in ((26, 'lm_bollard'), (27, 'lm_railing_w'), (28, 'lm_railing_m'), (29, 'lm_bollard')):
        m.over.append((1, x, 8, P1(t))); m.taken[8, x] = True
    # Armored fluted pilasters starting cleanly at y=1 (y=1..3 -> ZERO y=0 wall slicing!) framing Core Security Lift [28, 2]
    place_arch(m, 'lm_pillar', 27, 1)
    place_arch(m, 'lm_pillar', 29, 1)

    m.paint()

    # ---- 7. Post-Paint Obsidian-Marble & Gold-Trim Executive Floor Craft ----
    paves = [P1('lm_pave%d' % i) for i in range(4)]
    pave2 = P1('lm_pave2')
    plazas = [P1('lm_plaza0'), P1('lm_plaza1')]
    for y in range(H):
        for x in range(W):
            if m.cls[y, x] == '.':
                is_obs = (x <= 4 or x >= 26 or y <= 4 or y >= 15)
                is_trim = (not is_obs) and (x in (5, 25) or y in (5, 14))
                if is_obs:
                    m.L[0, y, x] = P1('Z_f%d' % ((x * 3 + y) % 3))
                elif 12 <= x <= 18:
                    m.L[0, y, x] = plazas[(x + y) & 1]
                elif is_trim:
                    m.L[0, y, x] = pave2
                else:
                    m.L[0, y, x] = paves[(x * 3 + y * 5) % 4]

    # Illuminated High-Security Core Lift threshold at [28, 2] + steel LED lintel header at (28, 1) + continuous cyan power feed!
    m.L[0, 2, 28] = P1('lm_plaza0')                          # Bright lit metallic elevator cabin floor (ZERO black hole!)
    m.L[1, 2, 28] = P1('lm_pdoor_open')                      # Open cyan-framed sliding security lift portal (walkable!)
    m.L[2, 2, 28] = 0
    m.L[2, 1, 28] = STAMPS['lm_sdoor']['layers'][2][0][0]    # Brushed-steel security header w/ red LED & gold lock plate!
    m.L[0, 3, 28] = P1('lm_grate')                           # Arrival grate pad from 199!
    for cy in (4, 5, 6):                                     # Continuous glowing cyan conduit down into east wing!
        m.L[0, cy, 28] = P1('lm_strip_v_on')
    m.L[0, 7, 28] = P1('lm_grate')                           # Clean floor junction plate above security rail
    for cx in range(24, 28):
        if m.cls[6, cx] == '.' and not m.taken[6, cx]:
            m.L[0, 6, cx] = P1('lm_strip_h_on')

    # Glowing brass-and-cyan marble floor inlays cleanly INSIDE atrium pillars (12..18, 7..13 -> ZERO pillar clipping!)
    for x in range(13, 18):
        if x not in (14, 15, 16) and m.cls[7, x] == '.':
            m.L[0, 7, x] = P1('lm_inlay_h')
        if x not in (14, 15, 16) and m.cls[13, x] == '.':
            m.L[0, 13, x] = P1('lm_inlay_h')
    for y in range(8, 13):
        for x in (12, 18):
            if m.cls[y, x] == '.':
                m.L[0, y, x] = P1('lm_inlay_v')
    for ix, iy, k in ((12, 7, 'se'), (18, 7, 'sw'), (12, 13, 'ne'), (18, 13, 'nw')):
        if m.cls[iy, ix] == '.':
            m.L[0, iy, ix] = P1('lm_inlay_' + k)

    # 5x5 Golden Meridian Sunburst gleaming at Executive Atrium center (13..17, 8..12)
    sun_L = STAMPS['lm_sun']['layers'][0]
    for dy in range(5):
        for dx in range(5):
            if m.cls[8 + dy, 13 + dx] == '.' and m.L[1, 8 + dy, 13 + dx] == 0:
                m.L[0, 8 + dy, 13 + dx] = sun_L[dy][dx]

    # Royal crimson carpets: Entrance Runner, North Skyline Promenade & West Aurelian Artifact Exhibition Strip
    floor_carpet_cave(m, 14, 13, 16, 18)
    floor_carpet_cave(m, 14, 4, 16, 7)
    floor_carpet_cave(m, 3, 6, 4, 12)

    head = {
        'id': 198,
        'name': 'Meridian Spire - Executive Gallery',
        'parent': 185,
        'bgm': 'Cedolan City',
        'field': 'NEON_GRID',
        'tone': [2, 0, -6, 10],
        'metadata': {
            'MapPosition': [0, 16, 16],
            'SnapEdges': True,
        },
        '_file': '198_meridian_executive_gallery.yaml',
    }
    return write_ts60(m, 198, head, '# GENERATED by mapgen/layouts/lumen_upper_wards.py (Batch 1A Act 1 Craft): 198 Executive Gallery.\n')


# ==============================================================================
# MAP 199: MERIDIAN SPIRE - DARK STONE CORE (25x25, TS60 cvZ / cvQ / lmw)
# ==============================================================================
def build_199():
    """199: Meridian Spire - Dark Stone Core (25x25, TS60).
    Ominous subterranean vaulted containment chamber beneath Meridian Spire:
      - Glowing cyan-violet conduit tracks radiating into a central recessed obsidian cradle [12, 12]
      - Industrial steel catwalks, forged brass hazard rails, telemetry consoles & abyssal reactor chasm
      - South Security Lift [12, 24] -> 198 [28, 3] down (arrival from 198: [12, 23] up)
    """
    W, H = 25, 25
    m = room60(W, H, 'Z', 199)
    # Cohesive dark industrial containment bunker (cvQ dark steel island + cvZ obsidian walls — ZERO bright outdoor white marble!)
    m.kit = {TER: 'cvQ', FLOOR: 'cvQ', 'default': 'cvZ'}

    # ---- 1. Crisp Octagonal Subterranean Abyssal Containment Vault (ZERO outer 1-tile chasm slivers!) ----
    m.box(4, 4, 20, 20, PIT, 'p')
    m.box(5, 2, 19, 3, PIT, 'p')
    m.mass_at(
        [(x, y) for y in range(0, 2) for x in range(0, 25)] +
        [(x, y) for y in range(2, 4) for x in list(range(0, 5)) + list(range(20, 25))] +
        [(x, y) for y in range(4, 21) for x in (0, 1, 2, 3, 21, 22, 23, 24)] +
        [(x, y) for y in range(21, 25) for x in list(range(0, 4)) + list(range(21, 25))] +
        [(x, 23) for x in list(range(0, 8)) + list(range(17, 25))] +
        [(x, 24) for x in list(range(0, 11)) + list(range(14, 25))]
    )

    # ---- 2. Central Elevated Dark-Steel Core Cradle Island (TER -> cvQ, x=9..15, y=9..15) ----
    m.box(9, 9, 15, 15, TER, '.')

    # ---- 3. Suspended Industrial Steel Catwalk Ring + Central Reactor Bridge ----
    # South Lift Vestibule & Containment Staging Bay (x=7..17, y=20..23 + lift notch x=11..13, y=24)
    m.box(7, 20, 17, 23, FLOOR, '.')
    m.box(11, 24, 13, 24, FLOOR, '.')
    m.mass_at([(7, 23), (17, 23)])

    # South-to-Core Conduit Catwalk Bridge (x=11..13, y=16..19) + stairs climbing onto Core Cradle Island!
    m.box(11, 16, 13, 19, FLOOR, '.')
    m.stairs(11, 15, w=3, n=3, c='.')

    # Crisp Octagonal Service Catwalk Ring (West x=4..6, East x=18..20, North y=4..7, South y=21..22)
    m.box(4, 4, 6, 22, FLOOR, '.')
    m.box(18, 4, 20, 22, FLOOR, '.')
    m.box(4, 21, 20, 22, FLOOR, '.')
    m.box(4, 4, 20, 7, FLOOR, '.')
    m.mass_at([(4, 22), (20, 22)])
    m.plan_cliffs(rows=3)

    # ---- 4. Events (ALL 3 consoles mounted directly on real visible mn_console & lm_rack props; Zero invented switches!) ----
    m.events += [
        {
            'type': 'warp',
            'name': 'Core Security Lift (Up)',
            'at': [12, 24],
            'to': {'map': 198, 'x': 28, 'y': 3, 'dir': 'down'},
            'se': 'Door exit',
        },
        {
            'type': 'event',
            'name': 'Dark Stone Core',
            'at': [12, 12],
            'pages': [
                {
                    'graphic': {'sprite': '', 'dir': 'down'},
                    'trigger': 'action',
                    'move': 'fixed',
                    'commands': [
                        'THE DARK STONE. Suspended in a cracked gold-and-obsidian containment cradle bound with braided conduits. It does not shine — the vault\'s lamps bend inward around it.',
                        'For one quiet heartbeat the steel decking hums beneath your boots, as if something vast inside the stone drew breath.',
                    ],
                }
            ],
        },
        {
            'type': 'sign',
            'name': 'North Containment Console',
            'at': [12, 5],
            'post': False,
            'text': 'RESONANCE LOG — SITE AURELIA SPECIMEN 00. LATTICE EXTRACTION: ACTIVE. CAUTION: THERMAL MICRO-FRACTURES IN CONTAINMENT RING.',
        },
        {
            'type': 'sign',
            'name': 'West Conduit Console',
            'at': [4, 12],
            'post': False,
            'text': 'CONDUIT ARRAY WEST: ROUTING TO LUMEN CONCOURSE & CIRCUIT GYM. DO NOT SEVER UNDER LIVE LOAD.',
        },
        {
            'type': 'sign',
            'name': 'East Conduit Console',
            'at': [20, 12],
            'post': False,
            'text': 'CONDUIT ARRAY EAST: ROUTING TELEMETRY TO COGSWORTH FOUNDRY TEST-BED. AUTHORIZATION: VOSS / STRADE.',
        },
        {
            'type': 'npc',
            'name': 'Core Technician',
            'at': [9, 21],
            'sprite': 'trainer_SCIENTIST',
            'dir': 'up',
            'text': 'Technician: Don\'t lean over the chasm rail. Whenever a storm rolls across the plateau, the Dark Stone answers it.',
        },
    ]

    m.keep_clear |= ({(x, y) for x in (11, 12, 13) for y in range(11, 25)}
                     | {(10, 12), (14, 12), (12, 10), (12, 11), (12, 13), (12, 14)}
                     | {(x, 6) for x in range(5, 20)} | {(x, 7) for x in range(5, 20)}
                     | {(5, y) for y in range(6, 22)} | {(19, y) for y in range(6, 22)}
                     | {(x, 21) for x in range(5, 20)} | {(x, 22) for x in range(8, 17)})

    # ---- 5. North Containment Bulkhead Hardware (Monitors, Alarms, Vents) ----
    hang(m, 'lm_monitors', 9, 2)
    hang(m, 'lm_monitors', 14, 2)
    hang(m, 'lm_banner', 12, 2)
    on_faces(m, 'lm_alarm_on', [(8, 3), (16, 3)])
    on_faces(m, 'lm_vent', [(5, 3), (19, 3)])

    # ---- 6. Central Cracked Dark Stone Cradle, Mounted Consoles, Dual Generators & Asymmetric Machinery ----
    # Dramatic glowing cracked Dark Stone resonance cradle squarely at [12, 11..12] (ZERO clipping abyss props!)
    place_arch(m, 'lm_cradle_cracked', 12, 11)
    # Four glowing cyan containment corner lamps on Core Island (ZERO cliff-clipping pillars!)
    for lx, ly in ((10, 10), (14, 10), (10, 14), (14, 14)):
        m.over.append((1, lx, ly, P1('lm_lamp_on')))
        m.taken[ly, lx] = True

    # Mounted Console Props DIRECTLY under all 3 sign events (guaranteed visible!)
    place_arch(m, 'mn_console', 11, 5)    # North Containment Console directly at [12, 5]!
    place_arch(m, 'lm_rack', 4, 11)       # West Conduit Console server rack directly at [4, 12]!
    place_arch(m, 'lm_rack', 20, 11)      # East Conduit Console server rack directly at [20, 12]!

    # Dual Triple-Coil Containment Generators firmly seated on the North Deck (x=6..7 & 17..18, y=4..5)!
    place_arch(m, 'lm_gen', 6, 4)
    place_arch(m, 'lm_gen', 17, 4)

    # Deliberately asymmetric West vs East maintenance/telemetry hardware (breaks mirror symmetry below 25%!)
    place_arch(m, 'lm_gearbox', 4, 9)
    m.over.append((1, 4, 14, P1('lm_junction_on'))); m.taken[14, 4] = True
    place_arch(m, 'lm_gearbox', 4, 17)
    place_arch(m, 'lm_rack', 20, 8)
    place_arch(m, 'lm_rack', 20, 15)
    m.over.append((1, 20, 18, P1('lm_junction'))); m.taken[18, 20] = True
    m.over.append((1, 14, 5, P1('lm_junction_on'))); m.taken[5, 14] = True
    m.over.append((1, 9, 5, P1('lm_gearbox'))); m.taken[5, 9] = True
    for nm, x, y in (
        ('lm_rack', 8, 22), ('lm_gearbox', 16, 22), ('lm_junction_on', 15, 22),
        ('lm_bollard', 10, 23), ('lm_bollard', 14, 23),
        ('lm_lamp_on', 10, 20), ('lm_lamp_on', 14, 20),
    ):
        put_if(m, nm, x, y)

    # Forged brass chasm hazard rails cleanly grounded along South Vestibule & Core Island north lip!
    for x, t in ((7, 'lm_bollard'), (8, 'lm_railing_w'), (9, 'lm_railing_e'), (10, 'lm_bollard'),
                 (14, 'lm_bollard'), (15, 'lm_railing_w'), (16, 'lm_railing_e'), (17, 'lm_bollard')):
        m.over.append((1, x, 20, P1(t))); m.taken[20, x] = True
    for x, t in ((10, 'lm_bollard'), (11, 'lm_railing_w'), (12, 'lm_railing_m'), (13, 'lm_railing_e'), (14, 'lm_bollard')):
        m.over.append((1, x, 9, P1(t))); m.taken[9, x] = True

    # ZERO unattached cv_shaft / pf_glow smears and ZERO floating abyss props!
    m.paint()

    # ---- 7. Post-Paint Abyssal Chasm, Obsidian Core Decking & Glowing Cyan-Violet Conduit Tracks ----
    deeps = [P1('lm_deep%d' % i) for i in range(6)]
    for y in range(H):
        for x in range(W):
            if m.cls[y, x] == 'p':
                m.L[0, y, x] = deeps[(x * 7 + y * 13) % len(deeps)]
            elif m.cls[y, x] == '.':
                m.L[0, y, x] = P1('Z_f%d' % ((x * 5 + y * 3) % 3))

    # Central glowing cyan-violet conduit spine straight from Lift [12, 24] -> Stairs -> Dark Stone Core [12, 12]!
    for y in range(13, 25):
        if m.cls[y, 12] == '.':
            m.L[0, y, 12] = P1('lm_strip_v_on')
        for sx in (11, 13):
            if m.cls[y, sx] == '.' and y >= 16:
                m.L[0, y, sx] = P1('lm_grate')
    # Glowing conduit tracks radiating E/W and N out of the Dark Stone Core [12, 12]
    for x in (10, 11, 13, 14):
        m.L[0, 12, x] = P1('lm_strip_h_on')
    m.L[0, 11, 12] = P1('lm_strip_v_on')
    m.L[0, 10, 12] = P1('lm_strip_v_on')
    # Perimeter service catwalk glowing cyan-violet conduit ring + asymmetric industrial grate bays!
    for y in range(7, 21):
        if m.cls[y, 5] == '.':
            m.L[0, y, 5] = P1('lm_strip_v_on')
        if m.cls[y, 19] == '.':
            m.L[0, y, 19] = P1('lm_strip_v_on')
    for x in range(6, 19):
        if m.cls[6, x] == '.':
            m.L[0, 6, x] = P1('lm_strip_h_on')
    for x in range(6, 19):
        if x not in (11, 12, 13) and m.cls[21, x] == '.':
            m.L[0, 21, x] = P1('lm_strip_h_on')
    # Subtle asymmetric catwalk service grates
    for gx, gy in ((6, 11), (6, 12), (6, 13), (18, 9), (18, 10), (10, 7), (14, 7)):
        if m.cls[gy, gx] == '.':
            m.L[0, gy, gx] = P1('lm_grate')

    # Dark industrial steel grating surrounding Dark Stone Core [12, 12] (ZERO clashing white-sidewalk squares!)
    for cx, cy in ((11, 11), (13, 11), (11, 13), (13, 13), (12, 12)):
        m.L[0, cy, cx] = P1('lm_grate')

    head = {
        'id': 199,
        'name': 'Meridian Spire - Dark Stone Core',
        'parent': 185,
        'bgm': 'Cave',
        'field': 'FACTORY',
        'tone': [-18, -20, 10, 34],
        'fog': {'name': 'prismfall_cave', 'opacity': 28, 'blend': 1, 'zoom': 100, 'sx': 1, 'sy': 0},
        'metadata': {
            'MapPosition': [0, 16, 16],
            'SnapEdges': True,
        },
        '_file': '199_meridian_dark_stone_core.yaml',
    }
    return write_ts60(m, 199, head, '# GENERATED by mapgen/layouts/lumen_upper_wards.py (Batch 1A Act 1 Craft): 199 Dark Stone Core.\n')


# ==============================================================================
# MAP 959: SKYPORT CUSTOMS (17x11, Harbour/Interior TS34)
# ==============================================================================
def build_959():
    """959: Skyport Customs (17x11, TS34 Prismfall Interior).
    Crisp aviation customs terminal connected via Exit [8, 10] LC_SKYPORT -> 196 [20, 6] (step out [20, 7] down).
    Features brass 0x80 inspection desk, stamped manifest board, luggage scale & trolley, route map,
    departure gate stanchions & waiting benches!
    """
    from act1_upper_interiors import (
        CREAM_STONE, MODERN_TILE, SEAMLESS_PARQUET, BLUE_CARPET, RED_CARPET,
        SCOREBOARD_WALL, SEA_CHART, SOFA_MODERN,
        _put_grid, _put_9slice, _put_tf, _put_lamp, _put_plant, _seam_ts34,
    )

    W, H = 17, 11
    L = np.zeros((3, H, W), dtype=np.int32)

    # ---- 1. Void-Sculpted Aviation Customs Terminal Silhouette (Clean aligned north wall across y=1..2!) ----
    floor = np.zeros((H, W), dtype=bool)
    floor[3:9, 1:6] = True        # West Luggage Scale & Parcel Inspection Bay (x=1..5, y=3..8)
    floor[8, 1] = False           # SW architectural chamfer
    floor[3:10, 6:11] = True      # Central Vaulted Customs Desk Concourse (x=6..10, y=3..9)
    floor[10, 7:10] = True        # Recessed Departure Gate Exit Vestibule (x=7..9, y=10; Exit @ [8, 10]!)
    floor[3:9, 11:16] = True      # East Passenger Waiting Lounge (x=11..15, y=3..8)
    floor[8, 15] = False          # SE architectural chamfer

    _seam_ts34(L, floor, wall_style='urban', floor_style='slate', wall_rows=2)

    # ---- 2. Crisp Multi-Zone Aviation Terminal Flooring ----
    # West Freight & Luggage Bay: sleek steel-blue aviation tile
    _put_9slice(L, MODERN_TILE, 1, 3, 5, 8, z=0, mask=floor)
    # Central Customs Concourse: bright cream terminal stone + royal-blue departure carpet runner!
    _put_9slice(L, CREAM_STONE, 6, 3, 10, 9, z=0, mask=floor)
    _put_9slice(L, BLUE_CARPET, 7, 5, 9, 9, z=1, mask=floor)
    # Recessed exit threshold mat centered on Exit [8, 10]
    L[0, 10, 7] = 5936; L[0, 10, 8] = 5937; L[0, 10, 9] = 5938
    L[1, 10, 7] = 5512; L[1, 10, 8] = 5513; L[1, 10, 9] = 5514
    # East Passenger Waiting Lounge: pure seamless 1068 honey parquet (ZERO dotted tracks!) + warm crimson rug!
    _put_9slice(L, SEAMLESS_PARQUET, 11, 3, 15, 8, z=0, mask=floor)
    _put_9slice(L, RED_CARPET, 12, 4, 14, 7, z=1, mask=floor)

    # ---- 3. North Wall Dressings (ALL cleanly aligned on y=1..2!): Manifest Board, Flight Board & Public Route Map ----
    # Stamped Manifest Board (complete 3x2 bulletin board 5795..5805 on West wall x=2..4, y=1..2)
    _put_grid(L, [[5795, 5796, 5797], [5803, 5804, 5805]], 2, 1, z_rows=(1, 1))
    # Backlit Skyport Flight Board centered cleanly behind Purser on Central north wall (x=7..9, y=1..2)
    _put_grid(L, SCOREBOARD_WALL, 7, 1, z_rows=(1, 1))
    # Public Airship Route Map mounted on the East Waiting Lounge wall (x=13..14, y=1..2 -> readable publicly at [13, 2]!)
    _put_grid(L, SEA_CHART, 13, 1, z_rows=(1, 1))

    # ---- 4. Enclosed Brass-and-Mahogany Customs Booth (0x80 Counter!) Wrapping Airship Purser @ [8, 3] ----
    # Single-row flush mahogany side arms (3491/3495 at y=3 w/ vase tops 3483/3487 on y=2 wall — ZERO double-stacked pots!)
    L[2, 2, 6] = 3483; L[1, 3, 6] = 3491         # Left floral mahogany arm flush to north wall (0x8f)
    L[2, 2, 10] = 3487; L[1, 3, 10] = 3495       # Right floral mahogany arm flush to north wall (0x8f)
    L[1, 3, 7] = 4523; L[1, 3, 9] = 4523         # Flanking mahogany customs filing cabinets (ZERO walk-behind leak & 0 cut-off tiles!)
    L[1, 4, 6] = 3499; L[1, 4, 7] = 3500; L[1, 4, 8] = 3501; L[1, 4, 9] = 3502; L[1, 4, 10] = 3503  # Front 0x80 desk!
    L[2, 4, 7] = 3428   # Open stamped customs manifest ledger atop counter W!
    L[2, 4, 9] = 3436   # Clean blue customs ink & stamp pad atop counter E (ZERO red office stapler!)

    # ---- 5. West Luggage Scale, Brass Trolley & Parcel Stacks (x=1..5, y=3..8) ----
    _put_grid(L, [[7486, 7487], [7494, 7495]], 1, 3, z_rows=(2, 1))
    _put_tf(L, 'console', 2, 7)
    L[1, 6, 1] = 7501
    L[1, 3, 5] = 7501
    L[1, 8, 5] = 5580

    # ---- 6. Departure Gate Stanchions & Spacious East Passenger Waiting Lounge ----
    _put_plant(L, 6, 7)
    _put_plant(L, 10, 7)
    # Single uncrowded Modern Terminal Sofa cleanly inside crimson rug (x=12..14, y=4..5) + travel suitcase (14, 7)!
    _put_grid(L, SOFA_MODERN, 12, 4, z_rows=(2, 1))
    L[1, 7, 14] = 7501
    _put_lamp(L, 15, 4)

    # ---- 7. Events (100% Diegetic Lore; Zero Invented Switches/Vars; 100% Reachable!) ----
    events = [
        {
            'type': 'exit',
            'at': [8, 10],
            'link': 'LC_SKYPORT',
            'arrive': [8, 9, 'up'],
        },
        {
            'type': 'npc',
            'name': 'Airship Purser',
            'at': [8, 3],
            'sprite': 'NPC 12',
            'dir': 'down',
            'text': 'Airship Purser: Welcome to Lumen Skyport Customs! The Skyreach shuttle is chartered for diplomatic service until the Council lifts the Tenth Year Gala charter — please keep your boarding stub ready.',
        },
        {
            'type': 'npc',
            'name': 'Customs Inspector',
            'at': [4, 5],
            'sprite': 'trainer_MERIDIAN_DIRECTORATE',
            'dir': 'down',
            'text': 'Customs Inspector: All trunks over forty pounds go across the brass scale. And no loose Magnemite near the compass desk, please.',
        },
        {
            'type': 'npc',
            'name': 'Waiting Passenger',
            'at': [12, 6],
            'sprite': 'trainer_GENTLEMAN',
            'dir': 'right',
            'text': 'Passenger: My cabin on the Dauntless was bumped for a Meridian envoy. Ten years of light and still a two-hour boarding queue.',
        },
        {
            'type': 'sign',
            'name': 'Stamped Manifest Board',
            'at': [3, 2],
            'post': False,
            'text': 'SKYPORT MANIFEST — BERTH W1: SALLOW LINE "DAUNTLESS" (CLEARED). BERTH E1: MERIDIAN COURIER (CARGO INSPECTION). SKYREACH SHUTTLE: DIPLOMATIC STANDBY.',
        },
        {
            'type': 'sign',
            'name': 'Airship Route Map',
            'at': [13, 2],
            'post': False,
            'text': 'ZENITH SKYWAYS: LUMEN SKYPORT — SKYREACH CITADEL — CROWNHAVEN. High-altitude crosswind advisories posted every hour.',
        },
    ]

    ev_cells = [tuple(e['at']) for e in events] + [(8, 9), (8, 5), (13, 3)]
    PG.guard(L, TID34, ev_cells, 'map 959')
    os.makedirs(RAW_DIR, exist_ok=True)
    raw_rel = 'data/raw/959.npy'
    np.save(os.path.join(HERE, raw_rel), L.astype(np.int32))

    spec = {
        'id': 959,
        'name': 'Skyport Customs',
        'parent': 196,
        'bgm': 'Poke Mart',
        'field': 'NONE',
        'tone': [-2, 0, 6, 2],
        'biome': 'interior',
        'metadata': {
            'MapPosition': [0, 19, 14],
        },
        'raw': raw_rel,
        'tileset': TID34,
        'events': events,
    }
    hdr = '# GENERATED by mapgen/layouts/lumen_upper_wards.py (Batch 1A Act 1 Craft): 959 Skyport Customs.\n'
    with open(os.path.join(SPEC_DIR, '959_skyport_customs.yaml'), 'w', encoding='utf-8') as f:
        f.write(hdr + yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=150, allow_unicode=True))
    print(f'Built 959 Skyport Customs                  {W}x{H} ts=34 events={len(events):2d}')
    return L


def main():
    build_194()
    build_195()
    build_196()
    build_197()
    build_198()
    build_199()
    build_959()


if __name__ == '__main__':
    main()
