"""layouts/lumenkit.py - Lumen City on tileset 60 "PF Rejuv Lumen" (map builder 15), on top of rkit.RMap / cavekit.Cave.

City(RMap) classes (one char per cell):
  p  marble paving (lm_pave0-3)            q  cream plaza flags (lm_plaza0-1)       r  basalt roadway (lm_road0-1)
  k  tram track along a road (lm_track_h / _v; set with track())                    l  Lowlight setts (lm_low0-3)
  .  garden grass (Sheridan)                w  garden water (Still water)            x  the drop over Nadir (lm_void)
  B  building / object (stamps)             d  gravel walk (Gravel Spring)
Heights (`ht`) are drawn with the plateau kit `lmw` (marble balustrade, ashlar face, foot); stairs are lm_stair.
Kerbs are added where pavement meets road; inlays (brass light conduits) run along lines you lay with inlay().
Interiors use Cave with the wall kits cvZ (Circuit Gym), cvY (civic marble) and cvQ (vault steel) - registered here."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rkit as K
from rkit import P1, STAMPS
from terrain import vnoise
HERE = K.HERE
TID = 60

# ------------------------------------------------------------------ kit registration (rkit KITS)
for _p in 'ZYQ':
    if _p + '_lipm' in STAMPS:
        K.KITS['cv' + _p] = dict(N=tuple(P1('%s_N%s' % (_p, e)) for e in 'wme'), W=P1(_p + '_W'), E=P1(_p + '_E'),
                                 rows=[tuple(P1('%s_%s%s' % (_p, row, e)) for e in 'wme') for row in ('lip', 'face', 'base')],
                                 inW=(P1(_p + '_inW0'), P1(_p + '_inW1')), inE=(P1(_p + '_inE0'), P1(_p + '_inE1')), l0=False,
                                 alt={P1(_p + '_facem'): (P1(_p + '_facem1'), 0.35), P1(_p + '_lipm'): (P1(_p + '_lipm1'), 0.35),
                                      P1(_p + '_basem'): (P1(_p + '_facem2'), 0.0)})
if 'lmw_lipm' in STAMPS:
    K.KITS['lmw'] = dict(N=tuple(P1('lmw_N%s' % e) for e in 'wme'), W=P1('lmw_W'), E=P1('lmw_E'),
                         rows=[tuple(P1('lmw_%s%s' % (row, e)) for e in 'wme') for row in ('lip', 'face', 'base')],
                         inW=None, inE=None, l0=False,
                         alt={P1('lmw_facem'): (P1('lmw_facem1'), 0.12), P1('lmw_lipm'): (P1('lmw_lipm1'), 0.10)} if 'lmw_facem1' in STAMPS else {})
STAIRS_LM = tuple(P1('lm_stair_' + e) for e in 'lmr') if 'lm_stair_l' in STAMPS else None


def sz(name):
    st = STAMPS[name]; return st['w'], st['h']


class City(K.RMap):
    GROUND = {'p': ['lm_pave%d' % i for i in range(8)], 'q': ['lm_plaza0', 'lm_plaza1'],
              'r': ['lm_road0', 'lm_road1'], 'l': ['lm_low0', 'lm_low1', 'lm_low2', 'lm_low3'],
              'x': ['lm_deep%d' % i for i in range(6)], 'n': ['lm_nadir0', 'lm_nadir1', 'lm_nadir2']}
    ON_TOP = 'pqrlk'                 # paved classes go on layer 2 over the same slab on layer 1 (street surfaces, as Saltmere's cobbles)

    def __init__(self, W, H, seed, base='p'):
        super().__init__(W, H, TID, seed, water='Still water', kit='lmw')
        self.cls[:] = base
        self.auto = {'w': ('Still water', 'rejuvenation'), 'd': ('Gravel Spring', 'pf'), 'W': ('Sea deep', 'rejuvenation')}
        self.STAIRS = STAIRS_LM or self.STAIRS
        self.grass_var = True
        self.tracks = {}                    # (x, y) -> 'h' / 'v' / 'x'
        self.inlays = {}                    # (x, y) -> inlay kind
        self.keep_clear = set()
        self.SEAL = P1('lm_bollard')

    # ------------------------------------------------------------ plan helpers
    def track(self, pts, kind='h'):
        for p in pts:
            self.tracks[p] = 'x' if p in self.tracks and self.tracks[p] != kind else kind

    def inlay(self, pts):
        """a brass light conduit through the paving along a polyline of cells (orthogonal steps)"""
        pts = list(pts); s = set(pts)
        for x, y in pts:
            n = (x, y - 1) in s; so = (x, y + 1) in s; w = (x - 1, y) in s; e = (x + 1, y) in s
            k = {(1, 1, 0, 0): 'v', (0, 0, 1, 1): 'h', (1, 0, 0, 1): 'ne', (1, 0, 1, 0): 'nw', (0, 1, 0, 1): 'se',
                 (0, 1, 1, 0): 'sw'}.get((n, so, w, e))
            if k is None: k = 'x' if (n + so + w + e) >= 3 else ('v' if (n or so) else 'h')
            self.inlays[(x, y)] = k

    def can(self, name, x, y, on='pqlr.d'):
        w, h = sz(name)
        return self.free(x, y, w, h, on=on)

    def put(self, name, x, y, link=None, dname=None, on=None, force=False):
        w, h = sz(name)
        if not force and not self.free(x, y, w, h, on=on or 'pqlr.dkx'):
            raise SystemExit('lumen: no room for %s at %d,%d' % (name, x, y))
        return self.stamp(name, x, y, link=link, dname=dname)

    def try_put(self, name, x, y, on='pqlr.d'):
        w, h = sz(name)
        if self.free(x, y, w, h, on=on) and not any((xx, yy) in self.keep_clear for xx in range(x - 1, x + w + 1) for yy in range(y, y + h + 1)):
            self.stamp(name, x, y); return True
        return False

    def row_of(self, names, x0, x1, y_base, link_for=None, gap=0, seed=0):
        """a terrace of buildings shoulder to shoulder whose doors open onto row y_base (the street below their fronts);
        names cycle; returns [(name, x, y, door)]"""
        import random
        rng = random.Random(self.seed * 3 + seed)
        x = x0; out = []; i = 0
        while True:
            nm = names[i % len(names)] if not callable(names) else names(rng)
            w, h = sz(nm)
            if x + w - 1 > x1: break
            y = y_base - h
            if y < 0 or not self.free(x, y, w, h, on='pqlr.dx'):
                x += 1; continue
            link = link_for(nm, i) if link_for else None
            d = self.stamp(nm, x, y, link=link[0] if link else None, dname=link[1] if link else None)
            out.append((nm, x, y, d)); x += w + gap; i += 1
        return out

    def prop(self, name, x, y, z=None):
        """a single-cell piece through `over` (its own layer from its code)"""
        L = STAMPS[name]['layers']
        for zz in range(3):
            if L[zz][0][0]:
                self.over.append((z if z is not None else zz, x, y, L[zz][0][0]))
        self.taken[y, x] = True

    # ------------------------------------------------------------ paint
    def paint_ground(self):
        L = self.L
        super().paint_ground()
        h = lambda x, y, k: ((x * 73856093) ^ (y * 19349663) ^ (self.seed * 83492791 + k)) & 0xffffffff
        for y in range(self.H):
            for x in range(self.W):
                c = self.cls[y, x]
                if c == 'B': c = self.under[y, x] or 'p'
                if c == 'k': c = 'r'
                if c == 'f': c = getattr(self, 'fill_ground', 'p')
                g = self.GROUND.get(c)
                if not g: continue
                t = P1(g[h(x, y, 7) % len(g)])
                L[0, y, x] = t
                if c in self.ON_TOP: L[1, y, x] = t
        def put(x, y, t):
            L[0, y, x] = t
            if self.cls[y, x] in self.ON_TOP or self.cls[y, x] == 'B': L[1, y, x] = t
        for y in range(self.H):
            for x in range(self.W):
                if self.cls[y, x] not in 'pq': continue
                for side, (dx, dy) in (('N', (0, -1)), ('S', (0, 1)), ('W', (-1, 0)), ('E', (1, 0))):
                    xx, yy = x + dx, y + dy
                    if self.inb(xx, yy) and self.cls[yy, xx] in 'rk':
                        put(x, y, P1('lm_kerb' + side)); break
        for (x, y), k in self.tracks.items(): put(x, y, P1('lm_track_' + k))
        for (x, y), k in self.inlays.items():
            if self.cls[y, x] in 'pqB': put(x, y, P1('lm_inlay_' + k))
        kind = getattr(self, 'roof_kind', 'V')
        for y, x in np.argwhere(self.cls == 'f'):
            v = 0 if h(x, y, 3) % 9 > 1 else (1 + h(x, y, 5) % 2)
            k2 = 'S' if (x, y) in getattr(self, 'slate', ()) else kind
            v = 0 if h(x, y, 3) % 6 > 1 else (1 + h(x, y, 5) % 2)
            L[2, y, x] = P1('lm_roof%s%d' % (k2, v))

    def fill(self, x0, y0, x1, y1):
        """roof fill over every free cell of a block (the roofs behind the frontage)"""
        for y in range(max(0, y0), min(self.H, y1 + 1)):
            for x in range(max(0, x0), min(self.W, x1 + 1)):
                if not self.taken[y, x] and self.cls[y, x] not in 'xn': self.cls[y, x] = 'f'; self.taken[y, x] = True

    def paint(self):
        super().paint()
        return self.L


def head(mid, name, fn, parent=0, **kw):
    h = {'id': mid, 'name': name, 'parent': parent, '_file': fn}
    h.update(kw)
    return h


def write(m, mid, head_, comment):
    m.write(mid, head_, comment='# GENERATED by mapgen/layouts/%s (map builder 15).  Edit the layout script, not this file.\n%s'
            % (comment, ''))
