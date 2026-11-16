"""Terrain painter: ASCII class grid -> 3-layer RMXP tile data, using a palette (palettes/*.yaml)."""
import random
import numpy as np

# Essentials TileDrawingHelper::NEIGHBORS_TO_AUTOTILE_INDEX (bits: N=1 NE=2 E=4 SE=8 S=16 SW=32 W=64 NW=128)
NB2AUTO = [
    46, 44, 46, 44, 43, 41, 43, 40, 46, 44, 46, 44, 43, 41, 43, 40,
    42, 32, 42, 32, 35, 19, 35, 18, 42, 32, 42, 32, 34, 17, 34, 16,
    46, 44, 46, 44, 43, 41, 43, 40, 46, 44, 46, 44, 43, 41, 43, 40,
    42, 32, 42, 32, 35, 19, 35, 18, 42, 32, 42, 32, 34, 17, 34, 16,
    45, 39, 45, 39, 33, 31, 33, 29, 45, 39, 45, 39, 33, 31, 33, 29,
    37, 27, 37, 27, 23, 15, 23, 13, 37, 27, 37, 27, 22, 11, 22, 9,
    45, 39, 45, 39, 33, 31, 33, 29, 45, 39, 45, 39, 33, 31, 33, 29,
    36, 26, 36, 26, 21, 7, 21, 5, 36, 26, 36, 26, 20, 3, 20, 1,
    46, 44, 46, 44, 43, 41, 43, 40, 46, 44, 46, 44, 43, 41, 43, 40,
    42, 32, 42, 32, 35, 19, 35, 18, 42, 32, 42, 32, 34, 17, 34, 16,
    46, 44, 46, 44, 43, 41, 43, 40, 46, 44, 46, 44, 43, 41, 43, 40,
    42, 32, 42, 32, 35, 19, 35, 18, 42, 32, 42, 32, 34, 17, 34, 16,
    45, 38, 45, 38, 33, 30, 33, 28, 45, 38, 45, 38, 33, 30, 33, 28,
    37, 25, 37, 25, 23, 14, 23, 12, 37, 25, 37, 25, 22, 10, 22, 8,
    45, 38, 45, 38, 33, 30, 33, 28, 45, 38, 45, 38, 33, 30, 33, 28,
    36, 24, 36, 24, 21, 6, 21, 4, 36, 24, 36, 24, 20, 2, 20, 0]
NB = [(0, -1, 1), (1, -1, 2), (1, 0, 4), (1, 1, 8), (0, 1, 16), (-1, 1, 32), (-1, 0, 64), (-1, -1, 128)]


def nbits(mask, x, y):
    """8-neighbour membership bits; outside the map counts as a member (RMXP/Essentials behaviour)."""
    H, W = mask.shape
    b = 0
    for dx, dy, bit in NB:
        xx, yy = x + dx, y + dy
        if not (0 <= xx < W and 0 <= yy < H) or mask[yy, xx]:
            b |= bit
    return b


def autotile_shape(mask, x, y):
    return NB2AUTO[nbits(mask, x, y)]


def autotile_layer(layer_arr, z, autotile_base):
    """Recompute shapes for every cell of layer z that holds autotile `autotile_base` (an id multiple of 48)."""
    kind = layer_arr[z] // 48
    mask = (kind == autotile_base // 48) & (layer_arr[z] < 384) & (layer_arr[z] > 0)
    for y, x in np.argwhere(mask):
        layer_arr[z, y, x] = autotile_base + autotile_shape(mask, x, y)


def blob_tile(r, b):
    n, e, s, w = b & 1, b & 4, b & 16, b & 64
    ne, se, sw, nw = b & 2, b & 8, b & 32, b & 128
    if not n and not w: return r['NW']
    if not n and not e: return r['NE']
    if not s and not w: return r['SW']
    if not s and not e: return r['SE']
    if not n: return r['N']
    if not s: return r['S']
    if not w: return r['W']
    if not e: return r['E']
    if not nw: return r.get('inner_nw', r['center'])
    if not ne: return r.get('inner_ne', r['center'])
    if not sw: return r.get('inner_sw', r['center'])
    if not se: return r.get('inner_se', r['center'])
    return r['center']


import json as _json, os as _os
_LEARNED = {}


def learned_table(name):
    """data/learned/t_<name>.json -> {bits: (tile, {layer: tile})} (majority votes)."""
    if name not in _LEARNED:
        d = _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'data', 'learned', 't_%s.json' % name)))
        tab = {}
        for b, c in d['table'].items():
            oth = {int(z): int(max(o, key=o.get)) for z, o in d['other'].get(b, {}).items()}
            tab[int(b)] = (int(max(c, key=c.get)), oth, sum(c.values()))
        _LEARNED[name] = tab
    return _LEARNED[name]


def learned_lookup(tab, bits):
    """Exact neighbourhood, else the closest learned one (orthogonal mismatches cost 4x diagonal ones)."""
    if bits in tab:
        return tab[bits]
    best = None
    for k, v in tab.items():
        x = k ^ bits
        cost = 4 * bin(x & 0x55).count('1') + bin(x & 0xAA).count('1') - min(v[2], 50) / 1000.0
        if best is None or cost < best[0]:
            best = (cost, v)
    return best[1]


def vnoise(x, y, seed, scale=5.0):
    """Cheap deterministic value noise in 0..1 (bilinear over a hashed lattice)."""
    def h(i, j):
        n = (i * 374761393 + j * 668265263 + seed * 1442695041) & 0xffffffff
        n = (n ^ (n >> 13)) * 1274126177 & 0xffffffff
        return ((n ^ (n >> 16)) & 0xffff) / 65535.0
    fx, fy = x / scale, y / scale
    i, j = int(fx), int(fy); u, v = fx - i, fy - j
    return (h(i, j) * (1 - u) + h(i + 1, j) * u) * (1 - v) + (h(i, j + 1) * (1 - u) + h(i + 1, j + 1) * u) * v


class Painter:
    def __init__(self, palette, grid_lines, seed=0, warn=print):
        self.p = palette
        self.warn = warn
        self.H = len(grid_lines)
        self.W = max(len(l) for l in grid_lines)
        self.rng = random.Random(seed)
        glyphs = palette['glyphs']
        self.cls = np.empty((self.H, self.W), dtype=object)
        for y, line in enumerate(grid_lines):
            line = line.ljust(self.W, '.')
            for x, ch in enumerate(line):
                c = glyphs.get(ch)
                if c is None:
                    warn('unknown glyph %r at %d,%d -> grass' % (ch, x, y)); c = 'grass'
                self.cls[y, x] = c
        self.layers = np.zeros((3, self.H, self.W), dtype=np.int32)
        self.heights = None

    def mask(self, names):
        names = [names] if isinstance(names, str) else names
        m = np.zeros((self.H, self.W), dtype=bool)
        for n in names:
            m |= (self.cls == n)
        return m

    def paint(self):
        P = self.p
        g = P['ground']
        variants = list(g.get('variants', {}).items())
        L = self.layers
        for y in range(self.H):
            for x in range(self.W):
                t = g['base']; r = self.rng.random() * 100
                for vid, wgt in variants:
                    if r < wgt: t = vid; break
                    r -= wgt
                L[0, y, x] = t
        classes = P['classes']
        # aliases ("ground_as") paint like another class
        alias = {n: c['as'] for n, c in classes.items() if c['kind'] == 'ground_as'}
        def members(n):
            c = classes[n]
            return [n] + [a for a, t in alias.items() if t == n] + c.get('same', [])
        order = ['blob', 'learned', 'autotile', 'sea', 'pier', 'tpier', 'hline', 'tree2x2', 'wall', 'cliffband',
                 'cliffline', 'tile', 'forest']
        for kind in order:
            for n, c in classes.items():
                if c['kind'] != kind:
                    continue
                own = self.mask([n] + [a for a, t in alias.items() if t == n])
                if not own.any():
                    continue
                getattr(self, 'k_' + kind)(n, c, own, self.mask(members(n)))
        if P.get('ground_table'):
            self.ground_pass(P['ground_table'], P.get('ground_ids'))
        if P.get('scatter'):
            self.scatter_pass(P['scatter'])
        return L

    # ------------------------------------------------------------------ example-based kinds (Tectonic palette)
    def k_learned(self, n, c, own, same):
        tab = learned_table(c['table']); z = c.get('layer', 0)
        for y, x in np.argwhere(own):
            t, oth, _ = learned_lookup(tab, nbits(same, x, y))
            self.layers[z, y, x] = t

    def k_sea(self, n, c, own, same):
        """Water autotile on layer 1. Its shore shapes are see-through, so boundary water cells keep a ground tile
        on layer 0: the neighbouring paving if there is one, else bare rock; open water has no layer-0 tile."""
        H, W = own.shape; L = self.layers
        land0 = L[0].copy()
        own = own | self.mask(c.get('also', []))
        same = same | own
        for y, x in np.argwhere(own):
            L[1, y, x] = c['id'] + autotile_shape(same, x, y)
            near = [(x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)
                    if 0 <= x + dx < W and 0 <= y + dy < H and not same[y + dy, x + dx]]
            if not near:
                L[0, y, x] = 0
            else:
                pav = [int(land0[yy, xx]) for xx, yy in near if self.cls[yy, xx] in c.get('quay', [])]
                L[0, y, x] = pav[0] if pav else c['rock']

    def k_tpier(self, n, c, own, same):
        for y, x in np.argwhere(own):
            b = nbits(own, x, y)
            self.layers[c.get('layer', 2), y, x] = c['left'] if not b & 64 else (c['right'] if not b & 4 else c['mid'])

    def k_cliffline(self, n, c, own, same):
        """Cliff rim lines (Gen 4 style): each 'C' cell is a rim piece chosen from its 4 connections; vertical
        pieces face away from the higher side (self.heights). Thick bands stack rim rows over a rock fill."""
        H, W = own.shape; L = self.layers
        tab = learned_table(c['table'])
        ht = self.heights
        at = lambda x, y: (not (0 <= x < W and 0 <= y < H)) or own[y, x]

        def side_height(x, y, dx):
            xx = x + dx
            while 0 <= xx < W and own[y, xx]:
                xx += dx
            return ht[y, xx] if (0 <= xx < W and ht is not None) else -1
        for y, x in np.argwhere(own):
            b = nbits(own, x, y)
            n_, e_, s_, w_ = at(x, y - 1), at(x + 1, y), at(x, y + 1), at(x - 1, y)
            t, oth, _ = learned_lookup(tab, b)
            if (n_ or s_) and not e_ and not w_:        # vertical run / end: pick the side by height
                t = c['west'] if side_height(x, y, 1) >= side_height(x, y, -1) else c['east']
            L[1, y, x] = t
            if oth.get(0) == c['rock'] or (n_ and e_ and s_ and w_):
                L[0, y, x] = c['rock']

    def k_forest(self, n, c, own, same):
        """Mixed forest: 2-wide, 3-tall trees (canopy on layer 2) in staggered rows 2 apart, species picked in
        noise patches, undergrowth in the gaps."""
        H, W = own.shape; L = self.layers
        sp = c['species']; seed = self.rng.randint(0, 9999)
        free = own.copy()
        for row, y in enumerate(range(-1, H, 2)):       # y = canopy row; trunk rows are y+1, y+2
            off = (row % 2)
            for x in range(off - 2, W, 2):
                x += int(vnoise(x, y, seed + 7, 3.0) * 1.99) if c.get('jitter', True) else 0
                cells = [(x, y + 1), (x + 1, y + 1), (x, y + 2), (x + 1, y + 2)]
                if not all(0 <= cx < W and 0 <= cy < H and free[cy, cx] for cx, cy in cells):
                    continue
                k = sp[int(vnoise(x, y, seed, c.get('patch', 6.0)) * len(sp) * 0.999)]
                if self.rng.random() < c.get('mix', 0.25):
                    k = self.rng.choice(sp)
                L[1, y + 1, x], L[1, y + 1, x + 1] = k['mid']
                L[1, y + 2, x], L[1, y + 2, x + 1] = k['bot']
                if y >= 0:
                    L[2, y, x], L[2, y, x + 1] = k['top']
                for cx, cy in cells:
                    free[cy, cx] = False
        under = c.get('under', [])
        for y, x in np.argwhere(free):
            if L[1, y, x] == 0 and under and self.rng.random() < c.get('under_p', 0.7):
                L[1, y, x] = self.rng.choice(under)

    def ground_pass(self, table, ids):
        """Re-tile layer-0 ground with the learned grass set: rims where grass meets rock, paving or water."""
        tab = learned_table(table); L = self.layers
        ids = set(ids)
        mem = np.isin(L[0], list(ids))
        for y, x in np.argwhere(mem):
            L[0, y, x] = learned_lookup(tab, nbits(mem, x, y))[0]

    def scatter_pass(self, sc):
        """Fill bare ground with detail: noise-patch decorations (flowers, tall grass) and sparse singles."""
        L = self.layers; H, W = L.shape[1:]
        seed = self.rng.randint(0, 9999)
        ok_cls = set(sc.get('on', ['grass']))
        for y in range(H):
            for x in range(W):
                if self.cls[y, x] not in ok_cls or L[1, y, x] or L[2, y, x]:
                    continue
                placed = False
                for i, pt in enumerate(sc.get('patches', [])):
                    if vnoise(x, y, seed + 31 * i, pt.get('scale', 4.0)) > pt['threshold'] and self.rng.random() < pt.get('fill', 0.8):
                        L[1, y, x] = self.rng.choice(pt['tiles']); placed = True; break
                if not placed and self.rng.random() < sc.get('density', 0.3):
                    tiles = sc['singles']
                    tot = sum(w for _, w in tiles); r = self.rng.random() * tot
                    for t, w in tiles:
                        if r < w:
                            L[1, y, x] = t; break
                        r -= w

    def k_tile(self, n, c, own, same):
        self.layers[c.get('layer', 0)][own] = c['tile']

    def k_blob(self, n, c, own, same):
        z = c.get('layer', 0)
        for y, x in np.argwhere(own):
            self.layers[z, y, x] = blob_tile(c, nbits(same, x, y))
            if c.get('min_width', 2) >= 2:
                b = nbits(same, x, y)
                if (not b & 1 and not b & 16) or (not b & 4 and not b & 64):
                    self.warn('%s is 1 tile thin at %d,%d (looks broken; make it >=2 wide)' % (n, x, y))

    def k_autotile(self, n, c, own, same):
        z = c.get('layer', 0)
        for y, x in np.argwhere(own):
            self.layers[z, y, x] = c['id'] + autotile_shape(same, x, y)

    def k_pier(self, n, c, own, same):
        if c.get('include'):
            own = own | self.mask(c['include'])
        under = self.p['classes'][c['under']]
        z = c.get('layer', 1)
        for y, x in np.argwhere(own):
            if under['kind'] == 'autotile':
                sm = self.mask([c['under'], n] + under.get('same', []) + c.get('include', []))
                self.layers[0, y, x] = under['id'] + autotile_shape(sm, x, y)
            b = nbits(own, x, y)
            col = 0 if not b & 64 else (2 if not b & 4 else 1)
            row = c['top'] if not b & 1 else c['body']
            self.layers[z, y, x] = row[col]

    def k_hline(self, n, c, own, same):
        z = c.get('layer', 1)
        H, W = own.shape
        at = lambda x, y: 0 <= x < W and 0 <= y < H and own[y, x]
        for y, x in np.argwhere(own):
            l, r, u, d = at(x - 1, y), at(x + 1, y), at(x, y - 1), at(x, y + 1)
            if (u or d) and not (l or r) and 'vmid' in c:
                t = c['vtop'] if not u else (c['vbottom'] if not d else c['vmid'])
            elif r and d and not u and not l and 'corner_tl' in c:
                t = c['corner_tl']
            elif l and r: t = c['mid']
            elif r: t = c['left']
            elif l: t = c['right']
            else: t = c['single']
            self.layers[z, y, x] = t

    def k_wall(self, n, c, own, same):
        """Interior walls: faces above floor, side edges, black elsewhere. Floor directly under a wall gets 'shadow'."""
        H, W = own.shape
        walk = ~self.mask([n] + c.get('not_floor', []))
        L = self.layers
        isw = lambda x, y: (not (0 <= x < W and 0 <= y < H)) or own[y, x]
        isf = lambda x, y: 0 <= x < W and 0 <= y < H and walk[y, x]
        for y, x in np.argwhere(own):
            if isf(x, y + 1): t = c['face_low']
            elif isw(x, y + 1) and isf(x, y + 2): t = c['face_high']
            elif isf(x + 1, y) or isf(x + 1, y + 1): t = c['side_l']
            elif isf(x - 1, y) or isf(x - 1, y + 1): t = c['side_r']
            else: t = c['solid']
            L[0, y, x] = t
        sh = c.get('shadow')
        if sh:
            for y, x in np.argwhere(walk):
                if y > 0 and own[y - 1, x] and self.cls[y, x] == c.get('shadow_on', 'floor'):
                    L[0, y, x] = sh

    def k_cliffband(self, n, c, own, same):
        """Cliff faces: every 'C' cell is a face tile (left/mid/right by row neighbours); the first non-cliff cell
        below a face column gets the base overlay on layer 1 (the bottom lip, drawn over the lower ground)."""
        H, W = own.shape
        stairs = self.mask(['stairs'])
        at = lambda x, y: 0 <= x < W and 0 <= y < H and (own[y, x] or stairs[y, x])
        for y, x in np.argwhere(own):
            l, r = at(x - 1, y), at(x + 1, y)
            self.layers[0, y, x] = c['mid'] if (l and r) else (c['left'] if r else (c['right'] if l else c['mid']))
            if y + 1 < H and not own[y + 1, x] and not stairs[y + 1, x]:
                lb, rb = at(x - 1, y), at(x + 1, y)
                self.layers[1, y + 1, x] = c['base_mid'] if (lb and rb) else (c['base_left'] if rb else (c['base_right'] if lb else c['base_mid']))

    def k_tree2x2(self, n, c, own, same):
        H, W = own.shape
        # snap to 2x2 blocks aligned on even coordinates (a block is forest if >= 2 of its cells are)
        snapped = np.zeros_like(own)
        for by in range(0, H, 2):
            for bx in range(0, W, 2):
                blk = own[by:by + 2, bx:bx + 2]
                if blk.sum() >= 2 or (blk.sum() >= 1 and blk.size < 4):
                    snapped[by:by + 2, bx:bx + 2] = True
        changed = int((snapped != own).sum())
        if changed:
            self.warn('%s: snapped %d cells to the 2x2 tree grid' % (n, changed))
        self.cls[own & ~snapped] = 'grass'
        self.cls[snapped] = n
        at = lambda x, y: (not (0 <= x < W and 0 <= y < H)) or snapped[y, x]
        L = self.layers
        for y, x in np.argwhere(snapped):
            px, py = x % 2, y % 2
            N, S, E, Wt = at(x, y - 1), at(x, y + 1), at(x + 1, y), at(x - 1, y)
            if py == 0:
                opened = (not N) or (px == 0 and not Wt) or (px == 1 and not E)
                t = c['Uopen'][px] if opened else c['U'][px]
            else:
                if not S: t = c['Dbottom'][px]
                elif (px == 0 and not Wt) or (px == 1 and not E): t = c['Dside'][px]
                else: t = c['D'][px]
            L[0, y, x] = t
            L[1, y, x] = 0
            if py == 0 and not N and y > 0:   # canopy overhangs the cell above
                L[c.get('canopy_layer', 2), y - 1, x] = c['canopy'][px]
