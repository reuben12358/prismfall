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
        order = ['tile', 'blob', 'autotile', 'pier', 'hline', 'tree2x2', 'wall']
        for kind in order:
            for n, c in classes.items():
                if c['kind'] != kind:
                    continue
                own = self.mask([n] + [a for a, t in alias.items() if t == n])
                if not own.any():
                    continue
                getattr(self, 'k_' + kind)(n, c, own, self.mask(members(n)))
        return L

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
        under = self.p['classes'][c['under']]
        z = c.get('layer', 1)
        for y, x in np.argwhere(own):
            if under['kind'] == 'autotile':
                sm = self.mask([c['under'], n] + under.get('same', []))
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
