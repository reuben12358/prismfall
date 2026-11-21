"""craftkit: the crafting layer for the massive roads (map builder 10), on top of routekit / rkit.

Rejuvenation's routes read as made places because of six habits this kit gives a layout:
  1. terrain levels: plateaus and stacked terraces with ragged-but-clean outlines (`plateau`, `shelf`), one-way grass or
     chalk ledges as shortcuts (`ledge`);
  2. water with a shore: streams with stepping stones, reeds and rocks (`stream`, `stones`), ponds and pools (`pond`),
     waterfalls off a terrace (`waterfall`), and on the coast wet sand, a tide line, rocks in the shallows, kelp and rock
     pools (`shore`);
  3. tall grass in organic patches of many sizes, never a noise field cut into blocks (`grass_patch`, `grass_fields`);
  4. mixed woods: the tree lattice in species zones (`woods`), a fringe of single trees of several kinds in front of
     it, undergrowth at the foot (`undergrowth`);
  5. flowers in meadows that thin out from a heart, not sprinkled evenly (`meadow`), ground that is never one flat
     green (`earth`), rocks, logs and stumps in groups (`props`);
  6. places with a purpose: camps, ruins, shrines, folds, built from props by the layout.
Everything works on a routekit.Route `r` (r.m is the rkit.RMap)."""
import os, sys, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import rkit as K
from rkit import STAMPS
from terrain import vnoise, NB2AUTO
import rcompose as RC

P1 = K.P1
_NB = ((0, -1, 1), (1, -1, 2), (1, 0, 4), (1, 1, 8), (0, 1, 16), (-1, 1, 32), (-1, 0, 64), (-1, -1, 128))


def nbits(mask, x, y, edge=True):
    H, W = mask.shape; b = 0
    for dx, dy, bit in _NB:
        X, Y = x + dx, y + dy
        if (0 <= X < W and 0 <= Y < H and mask[Y, X]) or (edge and not (0 <= X < W and 0 <= Y < H)): b |= bit
    return b


# ---------------------------------------------------------------------------------------------- forest species
def lat(name):
    """a 3x4 tree stamp as a lattice species (top two rows on layer 3, the trunk rows on layer 2)"""
    L = STAMPS[name]['layers']
    return ([list(L[2][0]), list(L[2][1])], [list(L[1][2]), list(L[1][3])], 1)


SPECIES = {'sh0': K.RMap.TREES_SH[0], 'sh1': K.RMap.TREES_SH[1]}
for _k, _n in (('teal', 'nt_teal_a'), ('teal2', 'nt_teal_b'), ('lime', 'nt_lime'), ('olive', 'nt_olive'), ('blossom', 'nt_blossom'),
               ('pink', 'nt_tree_pink'), ('red', 'nt_tree_red'), ('blue', 'nt_tree_blue'), ('purp', 'nt_tree_purp'),
               ('oak', 'tr_oak'), ('oak2', 'tr_oak2')):
    if _n in STAMPS: SPECIES[_k] = lat(_n)
_SILK = K._ST.get('_silk', {})
if _SILK:                                    # Gossamer Wood's silk-wrapped Sheridan trees (rcustom SILK_TREES)
    def _silk_lat(tr):
        top, bot, w = tr
        sw = lambda t: _SILK.get('silk_sh:%d' % (t - K.RC.offset('sh') + 384), t) if t else 0
        return ([[sw(t) for t in row] for row in top], [[sw(t) for t in row] for row in bot], 1)
    SPECIES['silk0'] = _silk_lat(K.RMap.TREES_SH[0]); SPECIES['silk1'] = _silk_lat(K.RMap.TREES_SH[1])
_SN2 = K._ST.get('_snow2', {})
if _SN2:                                     # snowified Akuwa oaks (rcustom SNOW_MORE): teal and blue under snow
    def _snow_lat(name):
        top, bot, w = lat(name)
        sw = lambda t: _SN2.get('snow_ak:%d' % (t - K.RC.offset('ak') + 384), t) if t else 0
        return ([[sw(t) for t in row] for row in top], [[sw(t) for t in row] for row in bot], 1)
    SPECIES['snowteal'] = _snow_lat('nt_teal_a'); SPECIES['snowteal2'] = _snow_lat('nt_teal_b'); SPECIES['snowblue'] = _snow_lat('nt_tree_blue')
if getattr(K.RMap, 'TREES_SNOW', None):
    SPECIES['snow0'], SPECIES['snow1'] = K.RMap.TREES_SNOW[0], K.RMap.TREES_SNOW[1]

# zone palettes: {species: weight}; a map lists the palettes its woods drift through
ELOWEN = [{'sh0': 5, 'sh1': 4}, {'sh1': 4, 'teal': 3, 'teal2': 2}, {'sh0': 3, 'olive': 2, 'lime': 2}, {'sh0': 4, 'sh1': 3, 'blossom': 1}]
COAST = [{'sh0': 5, 'teal': 3}, {'teal': 4, 'teal2': 3, 'sh1': 2}, {'sh1': 4, 'olive': 2}]
GOSSAMER = [{'sh1': 4, 'teal2': 2, 'silk1': 2}, {'sh0': 3, 'teal': 3, 'silk0': 3}, {'teal': 3, 'teal2': 3, 'sh1': 2}, {'silk0': 3, 'silk1': 3, 'sh0': 2},
            {'olive': 3, 'sh0': 3, 'lime': 1}]


def woods(r, palettes, scale=13.0, accents=None, seed=None):
    """replace the map's lattice painter: the staggered tree lattice, each tree's species drawn from the palette of the
    noise zone it stands in (species drift in patches like Rejuvenation's woods); `accents` = {species: p} sprinkles a
    rare colour (a red maple, a blossom) anywhere"""
    m = r.m; s = (r.seed if seed is None else seed) + 1313
    rng = random.Random(s)
    def paint_forest(trees=None, mask=None, vstep=2):
        msk = (m.cls == 'T') if mask is None else mask
        tw, nt, nb = 3, 2, 2
        phase = rng.randrange(tw)
        for ty in range(-nt, m.H, vstep):
            phase = (phase + rng.choice((1, 2))) % tw
            for tx in range(phase - tw, m.W, tw):
                foot = [(tx + dx, ty + nt + dy) for dx in range(tw) for dy in range(nb)]
                if not all(msk[y, x] for x, y in foot if m.inb(x, y)): continue
                if not any(m.inb(x, y) for x, y in foot): continue
                z = vnoise(tx, ty, s, scale)
                pal = palettes[min(len(palettes) - 1, int(z * len(palettes) * 0.999))]
                if accents and rng.random() < sum(accents.values()):
                    sp = rng.choices(list(accents), list(accents.values()))[0]
                else:
                    sp = rng.choices(list(pal), list(pal.values()))[0]
                top, bot, _ = SPECIES[sp]
                for dy in range(nt):
                    for dx in range(tw):
                        x, y = tx + dx, ty + dy
                        if m.inb(x, y) and top[dy][dx] and m.L[2, y, x] == 0: m.L[2, y, x] = top[dy][dx]
                for dy in range(nb):
                    for dx in range(tw):
                        x, y = tx + dx, ty + nt + dy
                        if m.inb(x, y) and bot[dy][dx]: m.L[1, y, x] = bot[dy][dx]; m.taken[y, x] = True
        m.lattice = [SPECIES[k] for k in SPECIES]                 # put_stamps: trunks of every species count as lattice
    m.forest = paint_forest


FRINGE = {'meadow': ['nt_round_sh', 'nt_pine_sh', 'tr_oak', 'nt_dark_sh', 'nt_dpine_sh', 'nt_teal_a', 'nt_lime', 'tr_pine'],
          'coast': ['nt_pine_a', 'nt_pine_b', 'nt_teal_a', 'nt_teal_b', 'nt_round_sh', 'nt_dpine_sh', 'tr_pine2'],
          'wood': ['nt_dark_sh', 'nt_dpine_sh', 'nt_teal_b', 'nt_olive', 'tr_oak2', 'nt_pine_b', 'nt_conifer'],
          'orchard': ['tr_oak', 'tr_oak2', 'nt_blossom', 'tr_pink', 'nt_lime']}


def fringe(r, kinds, n, box=None, on='.', seed=0, near_forest=2, zone_scale=9.0):
    """single trees in front of the woods (and in copses on open land): kinds drift by zone, so a clump is mostly one
    species with a stranger or two, like a real hedge bank.  near_forest: only within that many cells of class T (0 = anywhere)"""
    m = r.m; rng = random.Random(r.seed * 7 + seed); placed = 0
    x0, y0, x1, y1 = box or (0, 0, m.W, m.H)
    T = m.cls == 'T'
    if near_forest:
        pad = np.pad(T, near_forest); nearT = np.zeros_like(T)
        for dy in range(-near_forest, near_forest + 1):
            for dx in range(-near_forest, near_forest + 1):
                nearT |= pad[near_forest + dy:near_forest + dy + m.H, near_forest + dx:near_forest + dx + m.W]
    cells = [(x, y) for y in range(y0, y1) for x in range(x0, x1)]
    rng.shuffle(cells)
    ev = np.zeros((m.H, m.W), bool)
    for e in r.events:
        ex, ey = e['at']; ev[max(0, ey - 2):ey + 3, max(0, ex - 2):ex + 3] = True
    for x, y in cells:
        if placed >= n: break
        if near_forest and not nearT[y, x]: continue
        z = vnoise(x, y, r.seed + 77 + seed, zone_scale)
        k = kinds[int(z * len(kinds) * 0.999)] if rng.random() < 0.75 else rng.choice(kinds)
        st = STAMPS[k]; w, h = st['w'], st['h']
        ty = y - h + 1; tx = x - w // 2
        if ty < 0 or not m.can_tree(k, tx, ty, on): continue
        if ev[ty:y + 1, tx:tx + w].any() or r.road_mask[max(0, ty):y + 2, max(0, tx - 1):tx + w + 1].any(): continue
        if m.bodym[max(0, y - 1):y + 2, max(0, tx - 1):tx + w + 1].any(): continue
        if hasattr(m, 'bfoot') and m.bfoot[ty:ty + h, tx:tx + w].any(): continue        # the building guard would refuse it
        m.stamp(k, tx, ty, mark='B'); placed += 1
    return placed


def undergrowth(r, n, kinds=('nt_fern0', 'nt_fern1', 'nt_bush0', 'nt_bush1', 'nt_shrub0', 'ak_fern', 'nt_fern0'), on='.', seed=0, box=None):
    """ferns, bushes and shrubs at the foot of woods, cliffs and trees (cells just south or beside class T / B / cliff)"""
    m = r.m; rng = random.Random(r.seed * 11 + seed); placed = 0
    foot = np.zeros((m.H, m.W), bool)
    hard = (m.cls == 'T') | (m.cls == 'B') | m.cliff
    foot[1:, :] |= hard[:-1, :]; foot[:, 1:] |= hard[:, :-1]; foot[:, :-1] |= hard[:, 1:]
    x0, y0, x1, y1 = box or (0, 0, m.W, m.H)
    cells = [(x, y) for y in range(y0, y1) for x in range(x0, x1) if foot[y, x] and m.cls[y, x] in on]
    rng.shuffle(cells)
    ev = set()
    for e in r.events:
        ex, ey = e['at']
        for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)): ev.add((ex + dx, ey + dy))
    for x, y in cells:
        if placed >= n: break
        k = rng.choice(kinds); st = STAMPS[k]
        if (x, y) in ev or r.road_mask[y, x]: continue
        if m.free(x, y, st['w'], st['h'], on=on): m.stamp(k, x, y, mark='B'); placed += 1
    return placed


# ---------------------------------------------------------------------------------------------- terrain
def smooth_ht(m, h, passes=2, box=None):
    """majority-smooth the plateau mask of height >= h (no one-cell spurs or notches: the cliff kit reads cleanly)"""
    x0, y0, x1, y1 = box or (0, 0, m.W, m.H)
    for _ in range(passes):
        cur = m.ht >= h; pad = np.pad(cur, 1, mode='edge')
        n = sum(np.roll(np.roll(pad, dy, 0), dx, 1)[1:-1, 1:-1] for dy in (-1, 0, 1) for dx in (-1, 0, 1)) - cur
        grow = ~cur & (n >= 6); shrink = cur & (n <= 2)
        sub = np.zeros_like(cur); sub[y0:y1, x0:x1] = True
        m.ht[grow & sub] = h
        m.ht[shrink & sub] = h - 1
    # a plateau must be at least 3 cells deep north-south above each face (lip + walkable row + room for the north rim)
    for x in range(x0, x1):
        y = y0
        while y < y1:
            if m.ht[y, x] >= h:
                y2 = y
                while y2 < y1 and m.ht[y2, x] >= h: y2 += 1
                if y2 - y < 3 and y > 0: m.ht[y:y2, x] = h - 1
                y = y2
            else:
                y += 1


def plateau(r, cx, cy, rx, ry, h, rough=0.45, seed=0, smooth=2):
    """raise a ragged plateau (blob) to height h (cells already higher stay), then smooth its outline"""
    m = r.m; s = r.seed + 4100 + seed
    for y in range(int(cy - ry - 3), int(cy + ry + 4)):
        for x in range(int(cx - rx - 3), int(cx + rx + 4)):
            if not m.inb(x, y): continue
            q = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
            if q <= 1.0 + rough * (vnoise(x, y, s, 4.0) - 0.5) * 2:
                m.ht[y, x] = max(m.ht[y, x], h)
    if smooth: smooth_ht(m, h, smooth, box=(max(0, int(cx - rx - 4)), max(0, int(cy - ry - 4)), min(m.W, int(cx + rx + 5)), min(m.H, int(cy + ry + 5))))


def shelf(r, poly, h):
    """raise a polygon (list of (x, y)) to height h: hand-shaped terraces where the plan needs an exact edge"""
    from PIL import Image, ImageDraw
    m = r.m; im = Image.new('L', (m.W, m.H), 0); ImageDraw.Draw(im).polygon(poly, fill=1)
    a = np.array(im, bool); m.ht[a] = np.maximum(m.ht[a], h)


def stair(r, x, y_lip, w=3, h=None):
    """a stairway down a south face at lip row y_lip: straighten the lip there (routekit.flatten) and cut the steps"""
    m = r.m; h = h if h is not None else int(m.ht[y_lip, x + w // 2])
    n = len(K.KITS[m.kit.get(h, m.kit.get('default')) if isinstance(m.kit, dict) else m.kit]['rows'])
    r.flatten(x, x + w - 1, y_lip, h); r.crossing(x, y_lip, w=w, rows=n)
    for yy in (y_lip - 2, y_lip - 1, y_lip + n, y_lip + n + 1):          # the landings stay clear (no tree or rock)
        for xx in range(x, x + w):
            if m.inb(xx, yy):
                r.road_mask[yy, xx] = True
                if m.cls[yy, xx] in 'tT': m.cls[yy, xx] = '.'


def ledge(r, x0, x1, y, chalk=False, face=None):
    """a one-way ledge across x0..x1 at row y (jump down southward).  Cells stay grass class; the tiles go on layer 2.
    face: 'chalk', 'dune' or None (earth)"""
    m = r.m; face = face or ('chalk' if chalk else None)
    pre = {'chalk': 'lgc_', 'dune': 'lgd_', 'glass': 'gdl_', 'sand': 'sdl_'}.get(face, 'lg_')   # map builder 11: no-turf dune lips
    for x in range(x0, x1 + 1):
        if not m.inb(x, y): continue
        t = P1(pre + ('w' if x == x0 else 'e' if x == x1 else 'm'))
        if m.cls[y, x] == 't': m.cls[y, x] = '.'
        m.over.append((1, x, y, t)); m.taken[y, x] = True
        for yy in (y - 1, y + 1):                                  # the take-off and landing rows stay clear
            if m.inb(x, yy) and m.cls[yy, x] == 't': m.cls[yy, x] = '.'
            if m.inb(x, yy): m.taken[yy, x] = True
    r.ledges = getattr(r, 'ledges', []) + [(x0, x1, y)]


def stream(r, pts, w=2.4, c='w', seed=0, only='T.t'):
    """a narrow winding stream (a lane of water class)"""
    r.m.lane(pts, c=c, w=w, seed=r.seed + 900 + seed, only=only, wobble=0.6)


def stones(r, cells):
    """stepping stones: the cells stay water, a stone decal makes them walkable"""
    r.stepping = getattr(r, 'stepping', []) + list(cells)
    for x, y in cells: r.m.taken[y, x] = True


def pond(r, cx, cy, rx, ry, c='w', rough=0.5, seed=0):
    r.m.blob(cx, cy, rx, ry, c, seed=r.seed + 700 + seed, rough=rough, only=None)


def waterfall(r, x0, x1, y_lip):
    """mark a waterfall where a stream drops off a south face (columns x0..x1, lip row y_lip): painted after the cliffs"""
    r.falls = getattr(r, 'falls', []) + [(x0, x1, y_lip)]


def paint_falls(r):
    m = r.m
    for x0, x1, yl in getattr(r, 'falls', []):
        h = m.ht[yl, x0]; y = yl
        cells = []
        while y < m.H and (y == yl or m.ht[y, x0] < h) and m.cls[y, x0] != 'w':
            cells += [(x, y) for x in range(x0, x1 + 1)]; y += 1
        cells = [c for c in cells if c[1] <= yl + 3]
        mask = np.zeros((m.H, m.W), bool)
        for x, y in cells: mask[y, x] = True
        base = RC.vauto('rejuvenation', 'Waterfall', 0)
        for x, y in cells:
            for z in (1, 2): m.L[z, y, x] = 0
            m.L[0, y, x] = base + NB2AUTO[nbits(mask, x, y)]
            m.L[1, y, x] = 0
        bot = RC.vauto('rejuvenation', 'Waterfall bottom', 0)
        by = max(c[1] for c in cells) + 1 if cells else yl + 1
        bm = np.zeros((m.H, m.W), bool)
        for x in range(x0, x1 + 1):
            if m.inb(x, by): bm[by, x] = True
        for x in range(x0, x1 + 1):
            if m.inb(x, by) and m.cls[by, x] in 'wW': m.L[1, by, x] = bot + NB2AUTO[nbits(bm, x, by)]


# ---------------------------------------------------------------------------------------------- tall grass, flowers
def grass_patch(r, cx, cy, size, seed=0, keep_road=1, on='.u'):
    """one organic patch of tall grass: 2-4 overlapping lobes with a rough edge, smoothed (no square corners)"""
    m = r.m; rng = random.Random(r.seed * 5 + seed + cx * 31 + cy)
    lobes = [(cx, cy, size, size * rng.uniform(0.55, 0.9))]
    for _ in range(rng.randrange(1, 4)):
        a = rng.uniform(0, 6.28); d = size * rng.uniform(0.4, 0.9)
        lobes.append((cx + math.cos(a) * d, cy + math.sin(a) * d * 0.7, size * rng.uniform(0.45, 0.8), size * rng.uniform(0.35, 0.7)))
    road = np.isin(m.cls, list('dgsDw')) | r.road_mask
    mask = np.zeros((m.H, m.W), bool)
    R_ = int(size * 2.2) + 3
    for y in range(int(cy - R_), int(cy + R_) + 1):
        for x in range(int(cx - R_), int(cx + R_) + 1):
            if not m.inb(x, y) or m.cls[y, x] not in on or m.taken[y, x] or m.cliff[y, x]: continue
            q = min(((x - lx) / max(1, rx)) ** 2 + ((y - ly) / max(1, ry)) ** 2 for lx, ly, rx, ry in lobes)
            if q <= 1.0 + 0.5 * (vnoise(x, y, r.seed + seed + 61, 2.5) - 0.5):
                if keep_road and road[max(0, y - keep_road):y + keep_road + 1, max(0, x - keep_road):x + keep_road + 1].any(): continue
                mask[y, x] = True
    pad = np.pad(mask, 1)
    n = sum(np.roll(np.roll(pad, dy, 0), dx, 1)[1:-1, 1:-1] for dy in (-1, 0, 1) for dx in (-1, 0, 1)) - mask
    mask &= n >= 2
    # a ragged rim: single tufts stray off the edge, bites out of it (never a ruled line of tiles)
    edge = mask & (n <= 6)
    for y, x in np.argwhere(edge):
        if rng.random() < 0.18: mask[y, x] = False
    for y, x in np.argwhere(edge):
        if rng.random() < 0.22:
            dx, dy = rng.choice(((1, 0), (-1, 0), (0, 1), (0, -1)))
            X, Y = x + dx, y + dy
            if m.inb(X, Y) and not mask[Y, X] and m.cls[Y, X] in on and not m.taken[Y, X] and not m.cliff[Y, X] and not road[Y, X]: mask[Y, X] = True
    m.cls[mask] = 't'
    return int(mask.sum())


def smooth_sea(m, passes=3):
    """majority-smooth the deep-water band (its edge is a soft wobble, never blocks of columns)"""
    for _ in range(passes):
        cur = m.cls == 'W'; sea = np.isin(m.cls, ['w', 'W'])
        pad = np.pad(cur, 1, mode='edge')
        n = sum(np.roll(np.roll(pad, dy, 0), dx, 1)[1:-1, 1:-1] for dy in (-1, 0, 1) for dx in (-1, 0, 1)) - cur
        m.cls[cur & (n <= 3)] = 'w'
        m.cls[~cur & sea & (n >= 5)] = 'W'


def grass_fields(r, spots):
    """spots: [(cx, cy, size)] -> organic patches"""
    return sum(grass_patch(r, cx, cy, s, seed=i) for i, (cx, cy, s) in enumerate(spots))


def meadow(r, cx, cy, rx, ry, tiles=None, p=0.75, seed=0, on='.'):
    """a flower meadow that thins out from its heart: dense at the centre, a scatter at the rim, 1-3 kinds of flower in
    drifts (not every kind everywhere)"""
    m = r.m; rng = random.Random(r.seed * 3 + seed + cx * 7 + cy)
    fl = K.DECOR_SH['flowers']
    tiles = tiles or rng.sample(fl, 2)
    for y in range(int(cy - ry - 1), int(cy + ry + 2)):
        for x in range(int(cx - rx - 1), int(cx + rx + 2)):
            if not m.inb(x, y) or m.cls[y, x] not in on or m.taken[y, x] or m.cliff[y, x]: continue
            if m.L[1, y, x] or m.L[2, y, x]: continue
            q = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
            q += 0.35 * (vnoise(x, y, r.seed + seed + 5, 3.0) - 0.5)
            if q > 1.0: continue
            dens = p * (1.0 - q) ** 0.7
            if rng.random() < dens:
                k = int(vnoise(x, y, r.seed + seed + 9, 2.0) * len(tiles) * 0.999)
                m.L[1, y, x] = tiles[k]


def earth(r, spots, c='u', on='.'):
    """worn earth / sandy patches on open ground (the Dirt autotile blends them in): [(cx, cy, rx, ry)]"""
    for i, (cx, cy, rx, ry) in enumerate(spots):
        r.m.blob(cx, cy, rx, ry, c, seed=r.seed + 3300 + i, rough=0.8, only=on)


def props(r, kinds, n, box=None, on='.', seed=0, clump=0):
    """rocks, logs, stumps in groups: n placements; clump > 0 keeps each within clump cells of a few centres"""
    m = r.m; rng = random.Random(r.seed * 13 + seed); placed = 0
    x0, y0, x1, y1 = box or (0, 0, m.W, m.H)
    centres = [(rng.randrange(x0, x1), rng.randrange(y0, y1)) for _ in range(max(1, n // 3))] if clump else None
    ev = set()
    for e in r.events:
        ex, ey = e['at']
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1, 2): ev.add((ex + dx, ey + dy))
    for _ in range(n * 25):
        if placed >= n: break
        k = rng.choice(kinds); st = STAMPS[k]
        if clump:
            cx, cy = rng.choice(centres); x, y = cx + rng.randrange(-clump, clump + 1), cy + rng.randrange(-clump, clump + 1)
        else:
            x, y = rng.randrange(x0, x1), rng.randrange(y0, y1)
        if any((x + dx, y + dy) in ev for dx in range(st['w']) for dy in range(st['h'])): continue
        if r.road_mask[max(0, y - 1):y + st['h'] + 1, max(0, x - 1):x + st['w'] + 1].any(): continue
        if m.free(x, y, st['w'], st['h'], on=on) and not m.cliff[y:y + st['h'], x:x + st['w']].any():
            m.stamp(k, x, y, mark='B'); placed += 1
    return placed


def scatter_quiet(r, n=4, seed=None):
    """the kit's decor pass without the evenly sprinkled flowers (meadows do flowers): greens and rare props only"""
    m = r.m
    from rkit import TUFTS, CLOVER                   # walkable decor only: tufts and clover, never the solid bushes, which
    import render as R                              # can wall a talker or a whole field off (540, 568)
    ts = R.tilesets()[m.tid]
    walk = lambda ids: [t for t in ids if ts['passages'][t] & 0x0f != 0x0f]
    groups = {'flowers': TUFTS + CLOVER, 'green': walk(m.decor['green']) + TUFTS + CLOVER, 'rare': walk(m.decor['rare']) or TUFTS}
    m.scatter(n, seed=r.mid if seed is None else seed, groups=groups)


# ---------------------------------------------------------------------------------------------- the shore
def shore(r, wet=1, wet_noise=0.55, wrack=0.5, shallows=0.035, kelp=0.02, chalk_rocks=True, seed=0):
    """coast detail after painting: a band of wet sand along the waterline (soft, ragged inland edge), a tide line of
    wrack and shells at its top, rocks in the shallows with dark rings and foam, kelp on the water"""
    m = r.m; rng = random.Random(r.seed * 17 + seed)
    water = np.isin(m.cls, ['w', 'W'])
    sand = m.cls == 's'
    from collections import deque
    D = np.full((m.H, m.W), 99); q = deque()
    for y, x in np.argwhere(water): D[y, x] = 0; q.append((y, x))
    while q:
        y, x = q.popleft()
        if D[y, x] >= 4: continue
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            Y, X = y + dy, x + dx
            if 0 <= Y < m.H and 0 <= X < m.W and D[Y, X] > D[y, x] + 1: D[Y, X] = D[y, x] + 1; q.append((Y, X))
    wetm = sand & ((D <= wet) | ((D == wet + 1) & (np.array([[vnoise(x, y, r.seed + 51, 3.0) for x in range(m.W)] for y in range(m.H)]) > wet_noise)))
    wetm &= ~m.taken | (m.L[2] == 0)
    full = wetm | water
    WET = [P1('cs_wet_%02d' % i) for i in range(48)]
    for y, x in np.argwhere(wetm):
        if m.L[2, y, x]: continue
        m.L[2, y, x] = WET[NB2AUTO[nbits(full, x, y)]]
    # the tide line: just above the wet band
    WR = [P1('cs_wrack%d' % i) for i in range(4)] + [P1('cs_shell0'), P1('cs_shell1')]
    for y, x in np.argwhere(sand & ~wetm & (D <= wet + 2)):
        if m.L[2, y, x] or m.taken[y, x] or m.L[1, y, x] and m.L[1, y, x] < RC.VBASE: continue
        if rng.random() < wrack * (0.35 + vnoise(x, y, r.seed + 52, 4.0)):
            m.L[2, y, x] = rng.choice(WR)
    # rocks and kelp in the shallows (one or two cells off the beach)
    RK_ = [P1('cs_wrock%d' % i) for i in range(3)] if chalk_rocks else [P1('cs_wrockb0'), P1('cs_wrockb1')]
    KE = [P1('cs_kelp0'), P1('cs_kelp1')]
    for y, x in np.argwhere(water):
        if m.L[2, y, x] or (x, y) in getattr(r, 'deck', []): continue
        d_land = min([abs(dy) + abs(dx) for dy in range(-3, 4) for dx in range(-3, 4)
                      if 0 <= y + dy < m.H and 0 <= x + dx < m.W and not water[y + dy, x + dx]] or [9])
        if 2 <= d_land <= 4 and rng.random() < shallows: m.L[2, y, x] = rng.choice(RK_)
        elif 1 <= d_land <= 6 and rng.random() < kelp: m.L[2, y, x] = rng.choice(KE)


def rock_pools(r, spots):
    """rock pools on the sand / rock shelf: [(x, y, 'a'|'b'|'c')]"""
    for x, y, k in spots:
        n = 'cs_pool_' + k; st = STAMPS[n]
        if r.m.free(x, y, st['w'], st['h'], on='s.d'): r.m.stamp(n, x, y, mark='B')


def water_stamp(r, n, x, y):
    """a stamp standing in water (sea stacks, arches, boats): only where every cell is water and free"""
    m = r.m; L = np.array(STAMPS[n]['layers']); hh, ww = L.shape[1:]
    if all(m.inb(x + i, y + j) and m.cls[y + j, x + i] in 'wW' and not m.L[2, y + j, x + i] for i in range(ww) for j in range(hh)):
        for j in range(hh):
            for i in range(ww):
                for z in (1, 2):
                    if L[z, j, i]: m.L[2, y + j, x + i] = int(L[z, j, i])
        return True
    return False


def paint_extras(r):
    """after r.paint(): stepping stones and waterfalls"""
    m = r.m
    ST = [P1('pf_stepstone0'), P1('pf_stepstone1')]
    for x, y in getattr(r, 'stepping', []):
        m.L[1, y, x] = ST[(x + y) % 2]
    paint_falls(r)


# ---------------------------------------------------------------------------------------------- salt works
def pans_varied(r, x0, y0, x1, y1, kinds=('brine', 'brp', 'brg', 'brx'), pw=(2, 6), ph=(2, 3), on='S', seed=0, gap=(1, 2)):
    """salt pans of many sizes and brine colours on class `on` cells (a clay bund drawn round each); returns the pans
    as (x, y, w, h) so a layout can lay boardwalks, rakes and heaps between them"""
    m = r.m; rng = random.Random(r.seed * 19 + seed); out = []
    y = y0
    while y < y1:
        h = rng.randint(*ph); x = x0 + rng.randint(0, 2)
        while x < x1:
            w = rng.randint(*pw)
            if x + w <= x1 and y + h <= y1 and (m.cls[y:y + h, x:x + w] == on).all() and not m.taken[y:y + h, x:x + w].any():
                k = rng.choice(kinds)
                for yy in range(y, y + h):
                    for xx in range(x, x + w):
                        v = ('n' if yy == y else 's' if yy == y + h - 1 else '') + ('w' if xx == x else 'e' if xx == x + w - 1 else '')
                        m.tile(P1('%s_%s' % (k, v or 'c')), xx, yy, 1); m.cls[yy, xx] = 'B'
                out.append((x, y, w, h))
            x += w + rng.randint(*gap)
        y += h + rng.randint(*gap)
    return out


def crust_ground(r, cells, seed=0):
    """grey salt crust on the given cells' ground layer"""
    m = r.m; rng = random.Random(r.seed + 23 + seed); G = [P1('gs_crust%d' % i) for i in range(4)]
    for x, y in cells:
        m.L[0, y, x] = G[0] if rng.random() < 0.5 else rng.choice(G)


def boardwalks(r, cells):
    """light timber boardwalks over water / mud: each cell picks the plank direction from its neighbours"""
    m = r.m; S = set(cells)
    for x, y in cells:
        horiz = ((x - 1, y) in S or (x + 1, y) in S) and not ((x, y - 1) in S and (x, y + 1) in S)
        m.L[1, y, x] = P1('bw_h' if horiz else 'bw_v')


def clear_around(r, radius=1):
    """after seating: keep the ring round every event free of trees, rocks and bushes placed later (nothing boxes a
    talker or a trainer in); the cells keep their class"""
    m = r.m
    for e in r.events:
        x, y = e['at']
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                X, Y = x + dx, y + dy
                if m.inb(X, Y) and m.cls[Y, X] in '.tdgsuS' and not m.cliff[Y, X]: m.taken[Y, X] = True


def drapes_along(r, every=5, seed=0, kinds=('gw_drape0', 'gw_drape1', 'gw_cocoons', 'pf_p_web')):
    """silk hung where the woods meet a trail: a drape, a web or cocoons every few cells along the wood's edge (overhead,
    so the player walks under them)"""
    m = r.m; rng = random.Random(r.seed * 23 + seed); n = 0
    walk = np.isin(m.cls, list('dgt.')) & ~m.taken
    for y in range(1, m.H - 3):
        for x in range(0, m.W - 2):
            if m.cls[y, x] != 'T' or not walk[y + 1, x] or rng.random() > 1.0 / every: continue
            k = rng.choice(kinds); st = STAMPS[k]
            if x + st['w'] > m.W or y + st['h'] > m.H: continue
            if k == 'pf_p_web':
                if not m.free(x, y + 1, st['w'], st['h'], on='.'): continue
                m.stamp(k, x, y + 1, mark=None); n += 1; continue
            L = np.array(st['layers'])
            for dy in range(st['h']):
                for dx in range(st['w']):
                    t = int(L[:, dy, dx].max())
                    if t: m.over.append((2, x + dx, y + dy, t))
            n += 1
    return n


def seat(r, name, x, y, radius=8, on='.tT', avoid='d', **kw):
    """seat a building at the nearest legal spot to (x, y): free of stamps/crowns, every cell in `on`, no road cell
    under it, and its door front walkable; forest under the footprint and in a ring round it is cleared to grass.
    Returns (x, y) or None"""
    m = r.m; st = STAMPS[name]; w, h = st['w'], st['h']; door = st.get('door')
    best = None
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            X, Y = x + dx, y + dy
            if not m.free(X, Y, w, h, on=on): continue
            sub = m.cls[Y:Y + h, X:X + w]
            if any(ch in avoid for ch in sub.reshape(-1)): continue
            if door:
                fx, fy = X + door[0], Y + door[1] + 1
                if not m.inb(fx, fy) or m.cls[fy, fx] not in '.tTdgu' or m.taken[fy, fx]: continue
            d = dx * dx + dy * dy
            if best is None or d < best[0]: best = (d, X, Y)
    if best is None: return None
    _, X, Y = best
    for yy in range(max(0, Y - 1), min(m.H, Y + h + 2)):
        for xx in range(max(0, X - 1), min(m.W, X + w + 1)):
            if m.cls[yy, xx] == 'T' and not m.taken[yy, xx]: m.cls[yy, xx] = '.'
    m.stamp(name, X, Y, **kw)
    return X, Y


SNOWWOOD = [{'snow0': 5, 'snow1': 4}, {'snow1': 3, 'snowteal': 3, 'snowteal2': 2}, {'snow0': 3, 'snowblue': 2, 'snowteal': 2},
            {'snowteal2': 3, 'snow1': 3, 'snowblue': 1}]


def snow_ground_var(r, thr=0.5, seed=0):
    """snow ground that is never one flat sheet: wind ripples, sparkle and shadow dips drift in noise patches"""
    m = r.m; G = [P1('sn_g%d' % i) for i in range(4)]
    base = set(t for row in K.SNOW_GROUND for t in row)
    for y in range(m.H):
        for x in range(m.W):
            if m.L[0, y, x] in base and vnoise(x, y, r.seed + 4440 + seed, 5.0) > thr:
                m.L[0, y, x] = G[int(vnoise(x, y, r.seed + 4441 + seed, 2.5) * 3.999)]
