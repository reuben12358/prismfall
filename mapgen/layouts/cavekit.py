"""layouts/cavekit.py - caves on tileset 57 "PF Rejuv Cave" (map builder 13), on top of rkit.RMap.

A cave is rock MASS everywhere (class 'x', height MASS) with rooms and galleries carved out of it:
  floor 'p'-levels: PIT 0 (a chasm: black, solid), FLOOR 1, TERRACE 2 (and 3); MASS 6
  classes: '.' floor   'x' mass   'p' pit   'w' cave water (the map's pool autotile)   'W' deep water   'b' sand bar
           'c' crawlway (mass art on a passable tile: a hidden passage)
rkit.cliffs() draws every height change with the palette's wall kit (cvS / cvL / cvE): mass walls, terrace faces and
chasm walls all hang their faces on the lower side.  The mass darkens with distance from the cave (darkness edges);
the floor at the foot of a wall gets a shadow.  Tracks (rails on the floor, trestles over a chasm, points plates)
are laid after the cliffs and cut through them.  Ledges are one-way (jump south)."""
import os, sys, math
import numpy as np
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
import rkit as K
from rkit import RMap, P1, STAMPS
from terrain import vnoise

PIT, FLOOR, TER, TER2, MASS = 0, 1, 2, 3, 6
TID = 57
DIRS = {'U': (0, -1), 'D': (0, 1), 'L': (-1, 0), 'R': (1, 0)}


class Cave(RMap):
    def __init__(self, W, H, p, seed, pool, tid=TID, game='pf'):
        super().__init__(W, H, tid, seed, water=pool, kit={'default': 'cv' + p})
        self.p = p
        self.auto = {'w': (pool, game), 'W': ('Sea deep', 'rejuvenation')}
        self.STAIRS = tuple(P1('%s_stair%s' % (p, e)) for e in 'lmr')
        self.grass_var = False
        self.cls[:] = 'x'; self.ht[:] = MASS
        self.track = {}                     # (x, y) -> set of 'U','D','L','R' links
        self.junctions = set()
        self.ledge_rows = []
        self.keep_clear = set()

    # ------------------------------------------------------------ plan
    def room(self, cx, cy, rx, ry, h=FLOOR, c='.', rough=0.45, seed=0):
        for y in range(int(cy - ry - 3), int(cy + ry + 4)):
            for x in range(int(cx - rx - 3), int(cx + rx + 4)):
                if not self.inb(x, y): continue
                q = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
                if q <= 1.0 + rough * (vnoise(x, y, self.seed + 31 + seed, 3.0) - 0.5) * 2:
                    self.cls[y, x] = c; self.ht[y, x] = h

    def box(self, x0, y0, x1, y1, h=FLOOR, c='.'):
        for y in range(max(0, y0), min(self.H, y1 + 1)):
            for x in range(max(0, x0), min(self.W, x1 + 1)):
                self.cls[y, x] = c; self.ht[y, x] = h

    def gallery(self, pts, w=3.0, h=FLOOR, c='.', wobble=0.5, seed=0):
        """a winding passage (Catmull-Rom through pts) carved to height h"""
        before = self.cls.copy()
        self.lane(pts, c='@', w=w, seed=self.seed + 61 + seed, only=None, wobble=wobble)
        m = self.cls == '@'
        self.cls[m] = c; self.ht[m] = h

    def mass_at(self, cells):
        for x, y in cells:
            self.cls[y, x] = 'x'; self.ht[y, x] = MASS

    def crawl(self, cells, h=FLOOR):
        """a crawlway: passable, but drawn as the rock around it"""
        for x, y in cells:
            self.cls[y, x] = 'c'; self.ht[y, x] = MASS

    def tidy(self, passes=2):
        """no 1-cell mass spurs or floor notches (they draw as broken wall pieces)"""
        for _ in range(passes):
            m = self.cls == 'x'; pad = np.pad(m, 1, constant_values=True)
            n4 = pad[:-2, 1:-1].astype(int) + pad[2:, 1:-1] + pad[1:-1, :-2] + pad[1:-1, 2:]
            lone = m & (n4 <= 1)
            for y, x in np.argwhere(lone):
                nb = [(self.cls[y + dy, x + dx], self.ht[y + dy, x + dx]) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                      if self.inb(x + dx, y + dy) and self.cls[y + dy, x + dx] != 'x']
                if nb: self.cls[y, x], self.ht[y, x] = nb[0]
            # a floor cell with mass on both sides N and S (or W and E) and 1 wide: leave it (galleries may be narrow)

    def rails(self, pts):
        """an orthogonal track through waypoints"""
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            dx = (x1 > x0) - (x1 < x0); dy = (y1 > y0) - (y1 < y0)
            assert dx == 0 or dy == 0, 'track segments must be straight'
            x, y = x0, y0
            while (x, y) != (x1, y1):
                d = 'R' if dx > 0 else 'L' if dx < 0 else 'D' if dy > 0 else 'U'
                self.track.setdefault((x, y), set()).add(d)
                x, y = x + dx, y + dy
                self.track.setdefault((x, y), set()).add({'R': 'L', 'L': 'R', 'D': 'U', 'U': 'D'}[d])

    @staticmethod
    def path(pts):
        """the move string along a track's waypoints (U/D/L/R per step)"""
        out = ''
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            n = abs(x1 - x0) + abs(y1 - y0)
            out += ('R' if x1 > x0 else 'L' if x1 < x0 else 'D' if y1 > y0 else 'U') * n
        return out

    def ledge(self, x0, x1, y):
        self.ledge_rows.append((x0, x1, y))
        for x in range(x0, x1 + 1):
            self.taken[y, x] = True
            for yy in (y - 1, y + 1):
                if self.inb(x, yy): self.taken[yy, x] = True

    def put(self, name, x, y):
        """a multi-tile piece (stamp) at its top-left; its cells are taken"""
        L = STAMPS[name]['layers']; h, w = len(L[0]), len(L[0][0])
        self.stamps.append((name, x, y))
        self.taken[y:y + h, x:x + w] = True; self.bodym[y:y + h, x:x + w] = True

    # ------------------------------------------------------------ paint
    def mass_dist(self):
        m = np.isin(self.cls, ['x', 'c']) | (self.cls == 'p')
        m = np.isin(self.cls, ['x', 'c'])
        d = np.where(m, 99, 0)
        for _ in range(4):
            pad = np.pad(d, 1, constant_values=99)
            nb = np.minimum.reduce([pad[1 + dy:1 + dy + self.H, 1 + dx:1 + dx + self.W]
                                    for dy in (-1, 0, 1) for dx in (-1, 0, 1)])
            d = np.where(m, np.minimum(d, nb + 1), 0)
        return d

    def paint_ground(self):
        L = self.L; p = self.p
        d = self.mass_dist()
        for y in range(self.H):
            for x in range(self.W):
                c = self.cls[y, x]
                if c == 'x':
                    t = min(3, max(0, d[y, x] - 1))
                    L[0, y, x] = P1('%s_m%d%s' % (p, t, 'a' if vnoise(x, y, self.seed + 5, 2.0) > 0.5 else 'b'))
                elif c == 'c':
                    L[0, y, x] = P1('%s_mP' % p)
                elif c == 'p':
                    L[0, y, x] = P1('cv_pit%d' % (1 if vnoise(x, y, self.seed + 6, 1.5) > 0.8 else 0))
                elif c == 'b':
                    L[0, y, x] = P1('cv_bar')
                else:
                    n = vnoise(x, y, self.seed + 7, 3.0); r = (x * 7 + y * 13 + self.seed) % 11
                    v = 0 if n < 0.35 else 1 if n < 0.62 else 2 if r < 4 else 3
                    L[0, y, x] = P1('%s_f%d' % (p, v))

    def patches(self, thresh=0.64, scale=5.0):
        """soft-edged floor patches (salt crust / wet shingle / dust) in the 48 shapes over the floor"""
        from terrain import NB2AUTO
        if '%s_floorpatch_00' % self.p not in STAMPS: return
        ok = (self.cls == '.')
        pm = np.zeros((self.H, self.W), bool)
        for y in range(self.H):
            for x in range(self.W):
                if ok[y, x]: pm[y, x] = vnoise(x, y, self.seed + 300, scale) > thresh
        for _ in range(2):
            pad = np.pad(pm, 1); n8 = sum(np.roll(np.roll(pad, dy, 0), dx, 1)[1:-1, 1:-1] for dy in (-1, 0, 1) for dx in (-1, 0, 1)) - pm
            pm = (pm & (n8 >= 3)) | (~pm & ok & (n8 >= 6))
        pm &= ok
        pad = np.pad(pm, 1, constant_values=False)
        for y, x in np.argwhere(pm):
            b = 0
            for dx, dy, bit in ((0, -1, 1), (1, -1, 2), (1, 0, 4), (1, 1, 8), (0, 1, 16), (-1, 1, 32), (-1, 0, 64), (-1, -1, 128)):
                if pad[y + 1 + dy, x + 1 + dx]: b |= bit
            self.L[1, y, x] = P1('%s_floorpatch_%02d' % (self.p, NB2AUTO[b]))

    def cut_tracks(self):
        L = self.L
        shape = {frozenset('LR'): 'h', frozenset('UD'): 'v', frozenset('UR'): 'ne', frozenset('UL'): 'nw',
                 frozenset('DR'): 'se', frozenset('DL'): 'sw', frozenset('L'): 'h', frozenset('R'): 'h',
                 frozenset('U'): 'v', frozenset('D'): 'v'}
        for (x, y), ds in self.track.items():
            over_pit = self.cls[y, x] == 'p' or self.ht[y, x] == PIT
            for z in (1, 2): L[z, y, x] = 0
            if hasattr(self, 'pieces'): self.pieces.pop((x, y), None)
            if self.cls[y, x] == 'x':                       # a track through a wall: open floor under it
                self.cls[y, x] = '.'; L[0, y, x] = P1('%s_f0' % self.p)
            if len(ds) >= 3 or (x, y) in self.junctions:
                L[1, y, x] = P1('cv_points_tres' if over_pit else 'cv_points')
            else:
                k = shape[frozenset(ds)]
                L[1, y, x] = P1(('cv_tres_' if over_pit else 'cv_rail_') + k)
            self.taken[y, x] = True

    def paint_ledges(self):
        pre = '%sl_' % self.p
        for x0, x1, y in self.ledge_rows:
            for x in range(x0, x1 + 1):
                self.L[1, y, x] = P1(pre + ('w' if x == x0 else 'e' if x == x1 else 'm'))

    def shadows(self):
        """a shadow on the floor under each wall foot, and the base tile's foot already fades"""
        for (x, y), (kind, k, h) in getattr(self, 'pieces', {}).items():
            if kind == 'row' and k == 2 and self.inb(x, y + 1):
                if self.cls[y + 1, x] in '.b' and not self.L[1, y + 1, x] and not self.L[2, y + 1, x] and (x, y + 1) not in self.track:
                    self.L[2, y + 1, x] = P1('%s_shadow' % self.p)

    def floor_cells(self, free=True, on='.'):
        ok = np.isin(self.cls, list(on)) & ~self.cliff
        if free: ok &= ~self.taken
        return [(int(x), int(y)) for y, x in np.argwhere(ok)]

    def wall_foot(self, x, y):
        """a floor cell right under a wall base (good for props against the rock)"""
        return self.inb(x, y - 1) and self.cliff[y - 1, x] and self.ht[y - 1, x] == self.ht[y, x] and not self.cliff[y, x]

    def open_crawl(self):
        """crawlway cells keep the rock's look but lose their wall pieces: the tile under them is passable"""
        for y, x in np.argwhere(self.cls == 'c'):
            self.L[1, y, x] = 0; self.L[2, y, x] = 0
            if hasattr(self, 'pieces'): self.pieces.pop((x, y), None)

    def paint(self):
        self.paint_ground(); self.autotiles(); self.patches(*getattr(self, 'patch_args', ())); self.cliffs(); self.open_crawl()
        self.cut_tracks(); self.paint_stairs()
        self.paint_ledges(); self.put_stamps(); self.shadows()
        return self.L

    def dress(self, n=8, groups=None, seed=0, avoid=()):
        """decals on free floor: detail, rubble, fungus (groups: list of (piece names, weight))"""
        rng = self.rng; groups = groups or [(['%s_fd0' % self.p, '%s_fd1' % self.p, '%s_fd2' % self.p], 6),
                                            (['%s_rubble0' % self.p, '%s_rubble1' % self.p], 3)]
        names = [g for g, w in groups for _ in range(w)]
        evs = {tuple(e['at']) for e in self.events}
        for x, y in self.floor_cells(free=True):
            if (x, y) in evs or (x, y) in avoid or (x, y) in self.keep_clear: continue
            if self.L[1, y, x] or self.L[2, y, x]: continue
            if vnoise(x, y, self.seed + 90 + seed, 4.0) > 0.55 and rng.random() * 100 < n * 2:
                self.L[2, y, x] = P1(rng.choice(rng.choice(names) if isinstance(names[0], list) else names))

    def solid_props(self, names, n, near_wall=True, seed=0, box=None, avoid=()):
        """solid 1x1 props (crystals, rocks, nests...) at the foot of walls, never boxing in an event or a path"""
        evs = {tuple(e['at']) for e in self.events}
        cand = []
        for x, y in self.floor_cells(free=True):
            if box and not (box[0] <= x <= box[2] and box[1] <= y <= box[3]): continue
            if (x, y) in self.keep_clear or (x, y) in avoid: continue
            if near_wall and not self.wall_foot(x, y) and not any(self.cls[y + dy, x + dx] == 'x' for dx, dy in ((1, 0), (-1, 0)) if self.inb(x + dx, y + dy)): continue
            if any(abs(ex - x) + abs(ey - y) <= 1 for ex, ey in evs): continue
            cand.append((x, y))
        self.rng.shuffle(cand); out = []
        for x, y in cand:
            if len(out) >= n: break
            if any(abs(ox - x) + abs(oy - y) <= 1 for ox, oy in out): continue
            name = self.rng.choice(names)
            self.over.append((1, x, y, P1(name))); self.taken[y, x] = True; out.append((x, y))
        return out
