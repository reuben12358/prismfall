"""wildkit (builder 3): layout helpers for routes, forests and Bleed zones on tileset 40 "Prismfall Wilds".
A Wild is a citykit City (glyph grid + height grid) plus three explicit tile layers for trees, props and scatter, a
walkability model (so solid props never seal a path) and helpers for streams, bridges, ledges, landmarks and mood.
write() emits a spec for build.py (palette `wilds`).  Conventions: north is up; cliffs show south faces."""
import os, sys, json, math, random
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import yaml
from citykit import City, STAMPS
from terrain import vnoise

OFF = json.load(open(os.path.join(HERE, 'data', 'compose_wilds_offsets.json')))
B = OFF['bleed']['offset'] - 384            # Bleed copy of a Tectonic tile = id + B
R2 = OFF['route2']['offset'] - 384          # Rejuvenation Route 2 tile = id + R2
GL = OFF['goldenleaf']['offset'] - 384
CU = OFF['custom']['names']
PF = OFF.get('pfforest', {}).get('stamps', {})
_REG = None


def reg():
    global _REG
    if _REG is None:
        _REG = next(t for t in json.load(open(os.path.join(os.path.dirname(HERE), 'maps_out', 'tilesets_prismfall.json'))) if t['id'] == 40)
    return _REG


def solid(t): return t >= 384 and reg()['passages'][t] & 15 == 15
def prio(t): return reg()['priorities'][t] if t < len(reg()['priorities']) else 0


# ---------------------------------------------------------------------------------------------------- objects
# name -> (first tile id, w, h, base rows on layer 1; rows above go to layer 2).  Tiles are row-major on the sheet.
OBJ = {
    # Tectonic trees (2x3) as explicit rows: see TREES below
    'smalltree': (1160, 2, 2, 1), 'bushtree': (1050, 2, 2, 1), 'bushtree_f': (1066, 2, 2, 1),
    'sapling': (1052, 1, 2, 1), 'sapling2': (1053, 1, 2, 1), 'sapling_f': (1068, 1, 2, 1), 'pine_s': (1062, 1, 2, 1), 'pine_s2': (1063, 1, 2, 1),
    'log_big': (1000, 2, 2, 2), 'log': (1017, 2, 1, 1), 'stump': (1016, 1, 1, 1), 'stump_tall': (1002, 1, 2, 1),
    'log_moss': (2085, 2, 1, 1), 'stump_moss': (2087, 1, 1, 1), 'log_moss2': (2102, 2, 1, 1),
    'log_grey': (1260, 2, 1, 1), 'stump_grey': (1262, 1, 1, 1),
    'fern_big': (1176, 2, 2, 1), 'rafflesia': (1178, 2, 2, 2), 'corpse': (1174, 2, 3, 1),
    'creep1': (1096, 2, 4, 1), 'fallen': (1116, 2, 2, 1),
    'dead1': (1232, 2, 4, 1), 'dead2': (1234, 2, 4, 1), 'dead3': (1236, 2, 3, 1), 'dead4': (1238, 2, 3, 1),
    'gstump_dark': (1085, 3, 4, 2), 'gstump': (1128, 3, 4, 2), 'roots': (1118, 2, 2, 1),
    'thicket': (1200, 4, 3, 3), 'hedge_v': (1204, 1, 3, 3),
    'rock_b1': (1456, 2, 1, 1), 'rock_b2': (1458, 2, 1, 1), 'rock_big': (1480, 2, 2, 1), 'rock_tall': (1485, 1, 2, 1),
    'boulder': (1512, 3, 3, 2), 'boulder2': (1515, 3, 3, 2), 'boulder_dark': (1518, 2, 2, 1),
    'pillar_moss': (1576, 1, 2, 1), 'pillar_moss2': (1577, 1, 2, 1), 'crag': (1578, 3, 4, 2), 'crag_bare': (1581, 3, 4, 2),
    'pit_ladder': (1273, 2, 2, 1),
    'hay': (3456, 2, 2, 1), 'haystack': (3461, 3, 2, 1), 'hay_loose': (3472, 2, 2, 2), 'haycart': (3476, 2, 2, 1),
    'beehive': (3488, 2, 2, 1), 'beehive2': (3490, 2, 2, 1), 'kennel': (3504, 1, 2, 1), 'scarecrow': (3505, 1, 2, 1),
    'crop': (3506, 1, 2, 1), 'pumpkin': (3515, 1, 1, 1), 'sack': (3507, 1, 1, 1),
    'tomb': (3592, 2, 2, 1), 'tablet': (3594, 2, 2, 1), 'plaque': (3598, 2, 2, 1),
    'web_s': (3623, 1, 1, 0),
    'signboard': (3259, 2, 2, 1),
    'cry_blue': (8088, 2, 2, 1), 'cry_teal': (8104, 2, 2, 1), 'cry_violet': (8120, 2, 2, 1),
    'cry_blue_s': (8090, 1, 2, 1), 'cry_teal_s': (8106, 1, 2, 1), 'cry_violet_s': (8122, 1, 2, 1),
    'cry_blue_m': (8093, 2, 2, 1), 'cry_teal_m': (8109, 2, 2, 1), 'cry_violet_m': (8125, 2, 2, 1),
    # Rejuvenation Route 2 (3x4 broadleaf trees, 5x5 great tree, pines, crystal sprays)
    'r_tree_l': (R2 + 401, 3, 4, 1), 'r_tree_d': (R2 + 404, 3, 4, 1), 'r_tree_l2': (R2 + 432, 3, 4, 1), 'r_tree_d2': (R2 + 600, 3, 4, 1),
    'r_tree_l3': (R2 + 635, 3, 4, 1), 'r_tree_l4': (R2 + 640, 3, 4, 1), 'r_tree_l5': (R2 + 672, 3, 4, 1), 'r_tree_l6': (R2 + 675, 3, 4, 1),
    'r_pine_d': (R2 + 603, 2, 3, 1), 'r_pine_l': (R2 + 605, 2, 3, 1), 'r_cherry': (R2 + 704, 5, 5, 1),
    'r_cry_big': (R2 + 2040, 2, 2, 1), 'r_cry_spray': (R2 + 2057, 2, 2, 1), 'r_cry_s': (R2 + 2064, 1, 1, 1), 'r_cry_s2': (R2 + 2042, 1, 2, 1),
    # custom strip
    'cocoon': (CU['cocoon'], 1, 2, 1), 'cocoon_big': (CU['cocoon_big'], 2, 3, 2), 'cocoon_low': (CU['cocoon_low'], 1, 1, 1),
    'curtain': (CU['curtain'], 1, 2, 1), 'shaft': (CU['shaft'], 2, 4, 0), 'shade': (CU['shade'], 2, 2, 4),
    'survey_flag': (CU['survey_flag'], 1, 2, 1), 'web_big': (CU.get('web_big', CU['web_nw']), 3, 3, 0), 'veil': (CU['veil'], 1, 1, 0), 'barrier': (3293, 2, 1, 1),
    'silk_tree': (CU['silk_tree'], 2, 3, 1), 'crystal_tree': (CU['crystal_tree'], 2, 3, 1),
}
for _k, (_t, _w, _h, _kind) in PF.items():
    if not _k.startswith('rustic'): OBJ['pf_' + _k] = (_t, _w, _h, 1)
OBJ['well'] = OBJ.get('pf_haunted_06', OBJ['pit_ladder'])
# Tectonic stamps (stamps_t.json) usable as objects: 'st:<name>'
def _stamp_cells(name):
    st = STAMPS[name]; out = []
    for z in range(3):
        for yy, row in enumerate(st['layers'][z]):
            for xx, t in enumerate(row):
                if t: out.append((xx, yy, z, t))
    return out
# Tectonic 2x3 trees: (top, mid, bot) left ids; right = +1
TREES = {'t_round': (401, 409, 417), 't_dark': (405, 413, 421), 't_leafy': (605, 613, 621), 't_olive': (688, 696, 704),
         't_yellow': (768, 736, 744), 't_bright': (732, 740, 748), 't_palm': (880, 888, 896)}
FLOWERS = [1024, 1025, 1026, 1027, 1032, 1033, 1034, 1035, 1040, 1041, 1042, 1043, 1044]
TUFTS = [1164, 1172, 1164, 1180, 1189, 947, 939, 955, 950, 958]
MUSH = [1142, 1143, 1150, 1148, 1158, 1263]


def obj_cells(name, bleed=False):
    """-> [(dx, dy, layer, tile)] with blank tiles dropped."""
    out = []; sh = B if bleed else 0
    if isinstance(name, int): return [(0, 0, 1, name + sh)]
    if name.startswith('st:'): return [(dx, dy, z, t + (sh if t < 8616 else 0)) for dx, dy, z, t in _stamp_cells(name[3:])]
    if name in TREES:
        top, mid, bot = TREES[name]
        for dx in (0, 1):
            out += [(dx, 0, 2, top + dx + sh), (dx, 1, 1, mid + dx + sh), (dx, 2, 1, bot + dx + sh)]
        return out
    t0, w, h, base = OBJ[name]
    for dy in range(h):
        for dx in range(w):
            t = t0 + dy * 8 + dx
            if not _nonblank(t): continue
            out.append((dx, dy, 1 if dy >= h - base else 2, t + (sh if t < 8616 else 0)))
    return out


_BLANK = None


def _nonblank(t):
    global _BLANK
    if _BLANK is None:
        from PIL import Image
        Image.MAX_IMAGE_PIXELS = None
        im = Image.open(os.path.join(os.path.dirname(HERE), 'maps_out', 'Graphics', 'Tilesets', 'Prismfall Wilds.png'))
        a = im.getchannel('A').resize((8, im.height // 32), Image.BOX)       # mean alpha per tile
        _BLANK = a.load(); _nonblank.h = im.height // 32
    i = t - 384
    return 0 <= i // 8 < _nonblank.h and _BLANK[i % 8, i // 8] > 2


WALK = set('.,dDoaAvgG=+S')


class Wild(City):
    def __init__(self, W, H, seed, base='.'):
        City.__init__(self, W, H, seed, base)
        self.o = [[[0] * W for _ in range(H)] for _ in range(3)]     # explicit tiles per layer
        self.sol = [[False] * W for _ in range(H)]                    # cells blocked by explicit props
        self.must = []                                                # cells that have to stay connected on foot
        self.ledges = []
        self.strand_ok = 2                                            # walkable cells a single prop may cut off
        self.log = []

    # ------------------------------------------------------------------ walkability model
    def walkable(self, x, y):
        return self.inb(x, y) and self.g[y][x] in WALK and not self.sol[y][x]

    def flood(self, start):
        seen = set(); st = [tuple(start)]
        while st:
            x, y = st.pop()
            if (x, y) in seen or not self.walkable(x, y): continue
            seen.add((x, y))
            st += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        return seen

    def connected(self):
        if len(self.must) < 2: return True
        seen = self.flood(self.must[0])
        return all(tuple(m) in seen for m in self.must[1:])

    def need(self, *cells):
        for c in cells: self.must.append(tuple(c))

    # ------------------------------------------------------------------ explicit tiles
    def put(self, t, x, y, z, force=False):
        if not self.inb(x, y): return False
        if self.o[z][y][x] and not force: return False
        self.o[z][y][x] = t
        return True

    def can(self, name, x, y, on='.', bleed=False, pad=0):
        cells = obj_cells(name, bleed)
        if not cells: return False
        h0 = None
        for dx, dy, z, t in cells:
            xx, yy = x + dx, y + dy
            if not self.inb(xx, yy) or self.o[z][yy][xx]: return False
            if z == 1:
                if self.g[yy][xx] not in on or self.taken[yy][xx]: return False
                if h0 is None: h0 = self.ht[yy][xx]
                if self.ht[yy][xx] != h0: return False
            elif self.g[yy][xx] in 'CB' and prio(t) == 0: return False
            elif solid(t) and (self.taken[yy][xx] or self.g[yy][xx] not in on + 'T'): return False
        if pad:
            for dx, dy, z, t in cells:
                if z != 1: continue
                for ax in range(-pad, pad + 1):
                    xx = x + dx + ax
                    if self.inb(xx, y + dy) and self.sol[y + dy][xx]: return False
        return True

    def obj(self, name, x, y, on='.', bleed=False, force=False, check=True, pad=0):
        """Place an object with its top-left at (x, y). Solid base cells are checked against the must-connect set."""
        if not force and not self.can(name, x, y, on, bleed, pad): return False
        cells = obj_cells(name, bleed)
        blocked = [(x + dx, y + dy) for dx, dy, z, t in cells if solid(t) and self.inb(x + dx, y + dy)]
        strict = check and not force and self.must and getattr(self, '_sealed', False)
        before = len(self.flood(self.must[0])) if strict else 0
        old = [(c, self.sol[c[1]][c[0]]) for c in blocked]
        for cx, cy in blocked: self.sol[cy][cx] = True
        if check and not force and self.must:
            bad = any(tuple(m) in blocked for m in self.must)
            if not bad:
                seen = self.flood(self.must[0])
                lost = sum(1 for (cx, cy), v in old if not v and self.g[cy][cx] in WALK)
                bad = any(tuple(m) not in seen for m in self.must[1:]) or (strict and len(seen) < before - lost - self.strand_ok)
            if bad:
                for (cx, cy), v in old: self.sol[cy][cx] = v
                return False
        for dx, dy, z, t in cells:
            if self.inb(x + dx, y + dy):
                self.o[z][y + dy][x + dx] = t
                if z == 1: self.taken[y + dy][x + dx] = True
        return True

    def land(self, name, x, y, on='.', bleed=False, r=3):
        """Landmark: place at (x, y) or the nearest spot within r that fits; says so when it cannot. -> (x, y) or None"""
        cand = sorted(((dx * dx + dy * dy, dx, dy) for dx in range(-r, r + 1) for dy in range(-r, r + 1)))
        for _, dx, dy in cand:
            if self.obj(name, x + dx, y + dy, on, bleed): return (x + dx, y + dy)
        print('  landmark %s could not be placed near %d,%d' % (name, x, y)); return None

    def overhang(self, p=0.5, seed=0, bleed=False):
        """Canopy hanging over the trail: walkable cells beside forest get a tree-top tile overhead (walk-under)."""
        import random as _r
        r = _r.Random(self.seed * 11 + seed); sh = B if bleed else 0
        tops = [(401, 402), (405, 406), (605, 606), (688, 689)]
        for y in range(1, self.H - 1):
            for x in range(1, self.W - 1):
                if self.o[2][y][x] or not self.walkable(x, y): continue
                if self.g[y][x - 1] in 'TU' and r.random() < p:
                    self.o[2][y][x] = r.choice(tops)[1] + sh
                elif self.g[y][x + 1] in 'TU' and r.random() < p:
                    self.o[2][y][x] = r.choice(tops)[0] + sh
                elif self.g[y - 1][x] in 'TU' and r.random() < p * 0.5:
                    self.o[2][y][x] = r.choice(tops)[r.randint(0, 1)] + sh

    def keep_clear(self, cells, r=2):
        """Reserve ground around gates and warps so no tree or prop crowds them."""
        for cx, cy in cells:
            for y in range(cy - r, cy + r + 1):
                for x in range(cx - r, cx + r + 1):
                    if self.inb(x, y) and self.g[y][x] in WALK: self.taken[y][x] = True

    def seal(self):
        """Call once the terrain is final: from here on no prop may strand walkable ground."""
        self._sealed = True

    def base_of(self, name):
        t = OBJ.get(name); return (t[1], t[2]) if t else (2, 3)

    # ------------------------------------------------------------------ terrain helpers
    def stream(self, pts, width=2, seed=3, c='~'):
        """Meandering water course through the listed points; sets height -1 so cliffs treat it as low ground."""
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            n = int(max(abs(x1 - x0), abs(y1 - y0)) * 2) + 1
            for i in range(n + 1):
                t = i / n; x = x0 + (x1 - x0) * t; y = y0 + (y1 - y0) * t
                x += 1.2 * math.sin(y / 3.1 + seed) ; y += 0.8 * math.sin(x / 3.7 + seed * 2)
                w = width + (1 if vnoise(x, y, seed, 5.0) > 0.62 else 0)
                for yy in range(int(round(y - w / 2.0)), int(round(y - w / 2.0)) + w):
                    for xx in range(int(round(x - w / 2.0)), int(round(x - w / 2.0)) + w):
                        if self.inb(xx, yy): self.g[yy][xx] = c

    def stairs(self, x, yrim, n=1, kind='t_stairs'):
        City.stairs(self, x, yrim, n, kind)
        h = STAMPS[kind]['h']
        for yy in range(yrim, yrim + h):
            for xx in range(x, x + 3 * n):
                if self.inb(xx, yy): self.g[yy][xx] = 'S'; self.taken[yy][xx] = True

    def pond(self, cx, cy, rx, ry, seed=1, c='~', only='.'):
        self.blob(cx, cy, rx, ry, c, seed, only=only, rough=0.6)

    def bridge(self, x0, y0, w, h, c='='):
        """Timber deck over water cells in the rect (plank runs east-west; ends on land)."""
        for y in range(y0, y0 + h):
            for x in range(x0, x0 + w):
                if self.inb(x, y) and self.g[y][x] in '~w': self.g[y][x] = c

    def ledge(self, x0, x1, y):
        """One-way hop south along row y (grass ledge 1365-1367 on layer 2)."""
        xs = [x for x in range(x0, x1 + 1) if self.inb(x, y) and self.g[y][x] in '.,' and not self.taken[y][x] and not self.o[1][y][x]]
        runs = []; cur = []
        for x in xs:
            if cur and x != cur[-1] + 1: runs.append(cur); cur = []
            cur.append(x)
        if cur: runs.append(cur)
        for run in runs:
            if len(run) < 3: continue
            for i, x in enumerate(run):
                self.o[2][y][x] = 1365 if i == 0 else (1367 if i == len(run) - 1 else 1366)
                self.o[1][y][x] = self.o[1][y][x] or 0
                self.taken[y][x] = True; self.sol[y][x] = True      # modelled as a wall: ledges are only shortcuts
            self.ledges.append((run[0], run[-1], y))

    def grassfill(self, blobs, c='g', only='.'):
        for i, (cx, cy, rx, ry) in enumerate(blobs):
            self.blob(cx, cy, rx, ry, c, 50 + i, only=only, rough=0.8)

    def fence_ring(self, x0, y0, w, h, gaps=()):
        """Wooden rail fence (2048 set) around a rect, as explicit layer-1 tiles; gaps = cells left open."""
        T = {'nw': 2048, 'n': 2049, 'ne': 2050, 'w': 2056, 'e': 2058, 'sw': 2064, 's': 2065, 'se': 2066}
        for y in range(y0, y0 + h):
            for x in range(x0, x0 + w):
                edge = ('n' if y == y0 else 's' if y == y0 + h - 1 else '') + ('w' if x == x0 else 'e' if x == x0 + w - 1 else '')
                if not edge or (x, y) in gaps or not self.inb(x, y) or self.g[y][x] not in '.,' or self.taken[y][x]: continue
                self.o[1][y][x] = T[edge]; self.taken[y][x] = True; self.sol[y][x] = True

    # ------------------------------------------------------------------ vegetation and scatter
    def trees(self, names, n, box=None, on='.', seed=0, bleed=False, pad=0, near=None, far=None):
        """Scatter n trees/props from `names` over free cells (noise-clumped). near/far: glyph sets to hug or avoid."""
        r = random.Random(self.seed * 31 + seed); k = 0
        x0, y0, x1, y1 = box or (0, 0, self.W - 1, self.H - 1)
        for _ in range(n * 60):
            if k >= n: break
            nm = r.choice(names)
            x = r.randint(x0, x1); y = r.randint(y0 - 3, y1)
            if vnoise(x, y, self.seed + seed, 6.0) < 0.35: continue
            if near and not self._near(x, y + 2, near, 3): continue
            if far and self._near(x, y + 2, far, 1): continue
            if self.obj(nm, x, y, on, bleed, pad=pad): k += 1
        return k

    def _near(self, x, y, glyphs, r):
        for yy in range(y - r, y + r + 1):
            for xx in range(x - r, x + r + 1):
                if self.inb(xx, yy) and self.g[yy][xx] in glyphs: return True
        return False

    def scatter(self, patches, singles, density=0.2, on='.', seed=0, bleed=False, box=None):
        """Ground detail on free cells: patches = [(tiles, threshold, scale, fill)], singles = [(tile, weight)].
        Only passable decals belong here; they go on layer 1."""
        r = random.Random(self.seed * 17 + seed); sh = B if bleed else 0
        x0, y0, x1, y1 = box or (0, 0, self.W - 1, self.H - 1)
        drop = sorted({t for tl, _, _, _ in patches for t in tl if solid(t + sh)} | {t for t, _ in singles if solid(t + sh)})
        if drop: print('  scatter: dropped solid tiles', drop)
        patches = [([t for t in tl if not solid(t + sh)] or [1164], a, b_, c_) for tl, a, b_, c_ in patches]
        singles = [(t, w) for t, w in singles if not solid(t + sh)]
        tot = float(sum(w for _, w in singles)) or 1.0
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if self.g[y][x] not in on or self.taken[y][x] or self.o[1][y][x]: continue
                done = False
                for i, (tiles, thr, scale, fill) in enumerate(patches):
                    if vnoise(x, y, self.seed + seed + 31 * i, scale) > thr and r.random() < fill:
                        self.o[1][y][x] = r.choice(tiles) + sh; done = True; break
                if not done and r.random() < density:
                    q = r.random() * tot
                    for t, w in singles:
                        if q < w:
                            self.o[1][y][x] = t + sh; break
                        q -= w

    def edge_decor(self, tiles, p, on='.', by='TdC~', seed=0, bleed=False, layer=1):
        """Put decals on free cells that touch one of the `by` glyphs (mushrooms at tree feet, reeds at water...)."""
        r = random.Random(self.seed * 5 + seed); sh = B if bleed else 0
        if any(solid(t + sh) for t in tiles): print('  edge_decor: dropped solid tiles', [t for t in tiles if solid(t + sh)])
        tiles = [t for t in tiles if not solid(t + sh)] or [1164]
        for y in range(self.H):
            for x in range(self.W):
                if self.g[y][x] not in on or self.taken[y][x] or self.o[layer][y][x]: continue
                if any(self.inb(x + dx, y + dy) and self.g[y + dy][x + dx] in by for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))) and r.random() < p:
                    self.o[layer][y][x] = r.choice(tiles) + sh

    def hedge(self, x0, y0, w, h=2):
        """Clipped hedge bank (Tectonic 1200 set), solid, w x h cells (h >= 2)."""
        for y in range(y0, y0 + h):
            for x in range(x0, x0 + w):
                if not self.inb(x, y) or self.g[y][x] not in '.,' or self.taken[y][x] or self.o[1][y][x]: return False
        old = [row[:] for row in self.sol]
        for y in range(y0, y0 + h):
            for x in range(x0, x0 + w): self.sol[y][x] = True
        if not self.connected():
            self.sol = old; return False
        for y in range(y0, y0 + h):
            for x in range(x0, x0 + w):
                r = 1200 if y == y0 else (1216 if y == y0 + h - 1 else 1208)
                cidx = 0 if x == x0 else (3 if x == x0 + w - 1 else 1 + (x - x0) % 2)
                self.o[1][y][x] = r + cidx; self.taken[y][x] = True
        return True

    def path_decor(self, tiles, p=0.06, on='d', seed=0, bleed=False):
        """Pebbles and tufts on lane cells (layer 2 decals; passable)."""
        r = random.Random(self.seed * 7 + seed); sh = B if bleed else 0
        for y in range(self.H):
            for x in range(self.W):
                if self.g[y][x] in on and not self.o[2][y][x] and not self.taken[y][x] and r.random() < p:
                    self.o[2][y][x] = r.choice(tiles) + sh

    def water_decor(self, p=0.08, seed=0, c='~', where=None):
        """Lily pads and reeds on open water next to the bank (layer 2 over the water autotile)."""
        r = random.Random(self.seed * 3 + seed)
        for y in range(1, self.H - 1):
            for x in range(1, self.W - 1):
                if self.g[y][x] != c or self.o[2][y][x] or (where and not where(x, y)): continue
                nb = [self.g[y + dy][x + dx] for dx in (-1, 0, 1) for dy in (-1, 0, 1)]
                if all(v == c for v in nb) and r.random() < p:
                    self.o[2][y][x] = r.choice([1675, 1676, 1683, 1684, 1675, 1685])

    def overlay(self, name, x, y, bleed=False):
        """Overhead decal (webs, shafts): all cells on layer 2, never blocks; skips occupied cells."""
        for dx, dy, z, t in obj_cells(name, bleed):
            if self.inb(x + dx, y + dy) and not self.o[2][y + dy][x + dx]: self.o[2][y + dy][x + dx] = t

    # ------------------------------------------------------------------ events
    def fog_event(self, name, opacity=60, blend=0, zoom=200, sx=1, sy=0, hue=0):
        """Parallel event that sets the map fog once (RMXP command 204, subtype 1). build.py has no fog key yet."""
        return {'type': 'event', 'name': 'Atmosphere', 'at': [0, 0],
                'pages': [{'trigger': 'parallel', 'commands': [{'comment': 'fog: %s (see REQUESTS.md item 3)' % name},
                                                               {'raw': [204, [1, name, hue, opacity, blend, zoom, sx, sy]]},
                                                               {'selfswitch': ['A', True]}]},
                          {'cond': {'self': 'A'}}]}

    def spot(self, x, y, on='.,dDoaAv', r=6, keep=True):
        """Nearest free walkable cell to (x, y) on the given glyphs; reserved for an event."""
        best = None
        for yy in range(max(1, y - r), min(self.H - 1, y + r + 1)):
            for xx in range(max(1, x - r), min(self.W - 1, x + r + 1)):
                if self.g[yy][xx] in on and not self.taken[yy][xx] and not self.sol[yy][xx] and not self.o[1][yy][xx]:
                    d = (xx - x) ** 2 + (yy - y) ** 2
                    if best is None or d < best[0]: best = (d, xx, yy)
        if best is None: raise SystemExit('spot: nothing free near %d,%d' % (x, y))
        self.taken[best[2]][best[1]] = True
        if keep: self.must.append((best[1], best[2]))
        return [best[1], best[2]]

    def dump(self, seen=()):
        for y in range(self.H):
            print('%2d ' % y + ''.join(('*' if self.sol[y][x] and self.g[y][x] in WALK else self.g[y][x]) if (x, y) in seen or self.g[y][x] not in WALK
                                       else '!' for x in range(self.W)) + '  ' + ''.join(str(max(0, h)) for h in self.ht[y]))

    # ------------------------------------------------------------------ output
    def write(self, fname, head, comment='', mirror_max=0.40, extra_specs=()):
        if not self.connected():
            seen = self.flood(self.must[0])
            self.dump(seen)
            raise SystemExit('%s: must-connect cells cut off: %s' % (fname, [m for m in self.must if tuple(m) not in seen]))
        for z in range(3):
            for y in range(self.H):
                for x in range(self.W):
                    if self.o[z][y][x]: self.tiles.append({'tile': self.o[z][y][x], 'at': [x, y], 'layer': z})
        m = self.mirror()
        print('%s: plan mirror match %.1f%%' % (fname, m * 100))
        rows = [''.join(r) for r in self.g]
        hr = [''.join(str(min(9, max(h, 0))) for h in r) for r in self.ht]
        head = dict(head); head.setdefault('palette', 'wilds'); head.setdefault('rubric', True)
        body = yaml.safe_dump(head, sort_keys=False, default_flow_style=None, width=150, allow_unicode=True)
        body += 'map: |\n' + '\n'.join('  ' + r for r in rows) + '\nheights: |\n' + '\n'.join('  ' + r for r in hr) + '\n'
        tl = 'tiles:\n' + ''.join('- {tile: %d, at: [%d, %d], layer: %d}\n' % (t['tile'], t['at'][0], t['at'][1], t.get('layer', 1)) for t in self.tiles) if self.tiles else 'tiles: []\n'
        body += yaml.safe_dump({'stamps': self.stamps, 'tileblocks': self.blocks}, sort_keys=False, default_flow_style=None, width=150, allow_unicode=True)
        body += tl
        body += yaml.safe_dump({'events': self.events}, sort_keys=False, default_flow_style=None, width=150, allow_unicode=True)
        return comment + body


def save(fname, *bodies):
    open(os.path.join(HERE, 'specs', fname), 'w').write('---\n'.join(bodies))
    print('wrote specs/' + fname)


# ---------------------------------------------------------------------------------------------------- dialogue helpers
def say(name, expr, text):
    """Portrait line for the Cutscenes plugin message tag (design/CUTSCENES.md)."""
    return '\\pf[%s,%s]%s: %s' % (name.upper(), expr, name.capitalize(), text)


def trainer(at, ttype, name, sprite, d, sight, intro, after, **kw):
    e = {'type': 'trainer', 'at': list(at), 'sight': sight, 'dir': d, 'sprite': sprite, 'trainer': [ttype, name], 'intro': intro, 'after': after}
    e.update(kw); return e


def once(map_id, key, cmds):
    """Run cmds a single time across several events (a touch strip): keyed on a spare self-switch slot of event 0."""
    k = "$game_self_switches[[%d, 0, '%s']]" % (map_id, key)
    return [{'if': k, 'then': [], 'else': list(cmds) + [{'script': k + ' = true'}]}]
