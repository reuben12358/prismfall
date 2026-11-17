"""rkit: the Rejuvenation-family map kit (MAPGEN 2h).  A layout script builds an RMap (class grid + height grid +
stamps + events), then `paint()` turns it into three layers of PF Rejuv tiles and `write()` emits a spec for build.py
(`raw:` layers file + `tileset:` id + events).  Everything is drawn in composite/virtual ids (rcompose.py) and resolved
to the map's tileset at write time.

Classes (one char per cell):  .  grass   t tall grass (encounters)   d dirt lane (DirtDark)   g gravel street
  w  water (map's `water` autotile)   W deep water   s sand shore   T forest (tree lattice)   B building / object
  D  timber deck or pier   x void.  Heights: `ht` (0, 1, 2...) drawn with a cliff kit (`kit=`)."""
import os, sys, json, math, random
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
import numpy as np, yaml
from terrain import NB2AUTO, vnoise
import rcompose as RC
import render as R

_ST = {}
for fn in ('stamps_rj.json', 'stamps_rjc.json'):
    p = os.path.join(HERE, 'data', fn)
    if os.path.exists(p): _ST.update(json.load(open(p)))
STAMPS = {k: v for k, v in _ST.items() if not k.startswith('_')}
SNOWT = _ST.get('_snow', {})


def SN(key, sid):
    """composite id of a snowified copy of a source tile (rcustom.SNOW)"""
    return SNOWT['%s:%d' % (key, sid)]
SHIP = _ST.get('_ship_moored', {}).get('tiles', [])
SINGLE = _ST.get('_singles', {})


def C(part, src):
    """composite id of source sheet tile `src` (a source tile id >= 384) of part `part`."""
    return RC.offset(part) + src - 384


def V(name, game='rejuvenation'):
    return RC.vauto(game, name, 0)


# ---------------------------------------------------------------- palettes of single tiles (composite ids)
SH_GRASS = [[C('sh', 647), C('sh', 646)], [C('sh', 655), C('sh', 654)]]
SH_TALL = C('sh', 390)
DECOR_SH = {'flowers': [5630, 5638, 5639, 5642, 5646, 5650, 5651, 5658, 4939, 4940, 4941, 4836, 4845],
            'green': [4837, 4838, 4843, 4844, 4851, 4852, 4853, 4854, 4859, 4860, 4861, 4862],
            'rare': [4835, 4855, 5654]}
# cliff kits (composite ids).  rows: lip / face... / base, each (W end, middle, E end); sides; north rim; inner corners
KITS = {
    'sh': dict(N=(C('sh', 1624), C('sh', 1625), C('sh', 1627)), W=C('sh', 1632), E=C('sh', 1634),
               rows=[(C('sh', 1640), C('sh', 1641), C('sh', 1642)), (C('sh', 1648), C('sh', 1649), C('sh', 1650)),
                     (C('sh', 1648), C('sh', 1649), C('sh', 1650)), (C('sh', 1656), C('sh', 1657), C('sh', 1658))],
               inW=(C('sh', 1636), C('sh', 1644)), inE=(C('sh', 1635), C('sh', 1643)), l0=True),
    'ak': dict(N=(C('ak', 440), C('ak', 441), C('ak', 442)), W=C('ak', 448), E=C('ak', 450),
               rows=[(C('ak', 456), C('ak', 457), C('ak', 458)), (C('ak', 464), C('ak', 465), C('ak', 466)),
                     (C('ak', 472), C('ak', 473), C('ak', 474))], inW=None, inE=None, l0=False),
}


KITS['shs'] = dict(N=(SN('cliff_sh', 1624), SN('cliff_sh', 1625), SN('cliff_sh', 1627)), W=SN('cliff_sh', 1632), E=SN('cliff_sh', 1634),
                   rows=[tuple(SN('cliff_sh', b + i) for i in range(3)) for b in (1640, 1648, 1648, 1656)],
                   inW=(SN('cliff_sh', 1636), SN('cliff_sh', 1644)), inE=(SN('cliff_sh', 1635), SN('cliff_sh', 1643)), l0=True) if SNOWT else None
KITS['aks'] = dict(N=tuple(SN('cliff_ak', 440 + i) for i in range(3)), W=SN('cliff_ak', 448), E=SN('cliff_ak', 450),
                   rows=[tuple(SN('cliff_ak', b + i) for i in range(3)) for b in (456, 464, 472)], inW=None, inE=None, l0=False) if SNOWT else None
SNOW_GROUND = [[C('kf', 2475), C('kf', 2475)], [C('kf', 2475), C('kf', 2475)]]
SNOW_TALL = [C('kf', i) for i in (411, 412, 419, 420, 427, 428)]        # frosted ferns (terrain tag 2)
DECOR_SNOW = {'flowers': [9725, 9725, 10620], 'green': [10551, 10555, 10556, 10371, 9725],
              'rare': [10628, 10620]}


class RMap:
    def __init__(self, W, H, tileset, seed, water='Sea(Grass)', kit='sh', grass=SH_GRASS, decor=DECOR_SH):
        self.W, self.H, self.tid, self.seed = W, H, tileset, seed
        self.rng = random.Random(seed)
        self.cls = np.full((H, W), '.', dtype='<U1')
        self.ht = np.zeros((H, W), int)
        self.taken = np.zeros((H, W), bool)
        self.L = np.zeros((3, H, W), np.int64)
        self.over = []                      # (layer, x, y, tile) applied after painting
        self.stamps = []                    # (name, x, y)
        self.events = []; self.doors = {}; self.stairs_at = []
        self.water, self.kit, self.grass, self.decor = water, kit, grass, decor
        self.tall = SH_TALL
        self.auto = {'d': ('DirtDark', 'rejuvenation'), 'g': ('Gravel Spring', 'pf'), 'w': (water, 'rejuvenation'),
                     's': ('Sand shore_2', 'rejuvenation'), 'W': ('Sea deep', 'rejuvenation'), 'u': ('Dirt', 'rejuvenation')}
        self.cliff = np.zeros((H, W), bool)

    def inb(self, x, y): return 0 <= x < self.W and 0 <= y < self.H

    # ------------------------------------------------------------ plan
    def rect(self, x0, y0, w, h, c, only=None):
        for y in range(max(0, y0), min(self.H, y0 + h)):
            for x in range(max(0, x0), min(self.W, x0 + w)):
                if only is None or self.cls[y, x] in only: self.cls[y, x] = c

    def blob(self, cx, cy, rx, ry, c, seed=1, only=None, rough=0.5, ht=None):
        for y in range(int(cy - ry - 3), int(cy + ry + 4)):
            for x in range(int(cx - rx - 3), int(cx + rx + 4)):
                if not self.inb(x, y): continue
                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1.0 + rough * (vnoise(x, y, seed, 3.0) - 0.5):
                    if ht is not None: self.ht[y, x] = ht
                    elif only is None or self.cls[y, x] in only: self.cls[y, x] = c

    def lane(self, pts, c='d', w=2.0, seed=1, only='.tT', wobble=0.35):
        """Catmull-Rom lane through pts, width w (+ noise)."""
        P = [pts[0]] + list(pts) + [pts[-1]]
        for i in range(1, len(P) - 2):
            p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
            n = int(max(abs(p2[0] - p1[0]), abs(p2[1] - p1[1])) * 3) + 1
            for k in range(n + 1):
                t = k / n; t2, t3 = t * t, t * t * t
                x = 0.5 * (2 * p1[0] + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
                y = 0.5 * (2 * p1[1] + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
                r = w / 2.0 + wobble * (vnoise(x, y, seed, 4.0) - 0.5)
                for yy in range(int(y - r - 1), int(y + r + 2)):
                    for xx in range(int(x - r - 1), int(x + r + 2)):
                        if self.inb(xx, yy) and (xx + 0.5 - x - 0.5) ** 2 + (yy + 0.5 - y - 0.5) ** 2 <= r * r + 0.15:
                            if only is None or self.cls[yy, xx] in only: self.cls[yy, xx] = c

    def free(self, x, y, w, h, on='.t'):
        if x < 0 or y < 0 or x + w > self.W or y + h > self.H: return False
        return not self.taken[y:y + h, x:x + w].any() and all(ch in on for ch in self.cls[y:y + h, x:x + w].reshape(-1))

    def stamp(self, name, x, y, link=None, dname=None, door=None, mark='B', level=None):
        st = STAMPS[name]; w, h = st['w'], st['h']
        if x < 0 or y < 0 or x + w > self.W or y + h > self.H: raise SystemExit('stamp %s at %d,%d out of bounds' % (name, x, y))
        self.stamps.append((name, x, y))
        L = np.array(st['layers'])
        occ = L.max(axis=0) > 0
        if mark == 'B' and name[:3] in ('gl_', 'sh_', 'kf_', 'pf_', 'ak_') and name != 'kf_tree':
            if not hasattr(self, 'bfoot'): self.bfoot = np.zeros((self.H, self.W), bool)
            hit = self.bfoot[y:y + h, x:x + w] & occ
            if hit.any():
                yy, xx = np.argwhere(hit)[0]
                raise SystemExit('stamp %s at %d,%d overlaps another building at %d,%d' % (name, x, y, x + xx, y + yy))
            self.bfoot[y:y + h, x:x + w] |= occ
        self.taken[y:y + h, x:x + w] |= occ
        if mark:
            ts = self.ts()
            for dy in range(h):
                for dx in range(w):
                    if occ[dy, dx] and self.blocked_stack(L[:, dy, dx], ts): self.cls[y + dy, x + dx] = mark
        d = door or st.get('door')
        if d is not None and (link or dname):
            ev = {'type': 'door', 'at': [x + d[0], y + d[1]], 'gfx': ['', 0, 2], 'name': dname or (name + ' door')}
            if link: ev['link'] = link
            self.events.append(ev)
            self.cls[y + d[1], x + d[0]] = 'B'
            return (x + d[0], y + d[1])
        return None

    def front(self, name, dx, dy, link=None, dname=None, **kw):
        """place a stamp so that its door lands on (dx, dy)"""
        st = STAMPS[name]; ox, oy = st['door']
        return self.stamp(name, dx - ox, dy - oy, link, dname or (name + ' door'), **kw)

    def near(self, name, x, y, on='.', r=3):
        """place a prop stamp at the free spot nearest (x, y) (within r); returns True if placed"""
        st = STAMPS[name]
        for d in range(r + 1):
            for yy in range(y - d, y + d + 1):
                for xx in range(x - d, x + d + 1):
                    if max(abs(xx - x), abs(yy - y)) == d and self.free(xx, yy, st['w'], st['h'], on=on):
                        self.stamp(name, xx, yy); return True
        print('  (no room for %s near %d,%d)' % (name, x, y)); return False

    def beds(self, prefixes=('gl_', 'sh_'), p=0.8, seed=4):
        """flower beds along the foot of every building's front wall and along its sides (Sheridan / Goldenleaf habit)"""
        rng = random.Random(self.seed + seed)
        fl = self.decor['flowers']
        for name, x, y in self.stamps:
            if not name.startswith(prefixes) or 'door' not in STAMPS[name]: continue
            st = STAMPS[name]; occ = np.array(st['layers']).max(axis=0) > 0
            cols = [dx for dx in range(st['w']) if occ[:, dx].any()]
            for dx in cols:
                bottom = max(dy for dy in range(st['h']) if occ[dy, dx])
                X, Y = x + dx, y + bottom + 1
                if self.inb(X, Y) and self.cls[Y, X] == '.' and not self.taken[Y, X] and rng.random() < p:
                    self.tile(rng.choice(fl), X, Y, 1)

    def greenfill(self, dist=3, on='.', seed=9):
        """Goldenleaf habit: leftover lawn far from streets, doors and events becomes tree mass (class T, painted by the
        lattice), so towns read as streets cut through woodland, not houses on a lawn"""
        walk = np.isin(self.cls, list('dgsD')) | self.cliff
        for e in self.events:
            x, y = e['at']; walk[max(0, y - 1):y + 2, max(0, x - 1):x + 2] = True
        from collections import deque
        D = np.full((self.H, self.W), 99); q = deque()
        for y, x in np.argwhere(walk): D[y, x] = 0; q.append((y, x))
        while q:
            y, x = q.popleft()
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                Y, X = y + dy, x + dx
                if 0 <= Y < self.H and 0 <= X < self.W and D[Y, X] > D[y, x] + 1:
                    D[Y, X] = D[y, x] + 1; q.append((Y, X))
        n = 0
        for y in range(self.H):
            for x in range(self.W):
                if self.cls[y, x] in on and not self.taken[y, x] and D[y, x] >= dist + (vnoise(x, y, seed, 3.0) > 0.7):
                    self.cls[y, x] = 'T'; n += 1
        return n

    def street(self, pts, w=3, c='g', only=None):
        """orthogonal street through pts (each leg axis-aligned), w wide, centred on the points"""
        a = w // 2
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            xa, xb = sorted((x0, x1)); ya, yb = sorted((y0, y1))
            self.rect(xa - a, ya - a, xb - xa + w, yb - ya + w, c, only)

    def can_tree(self, name, x, y, on='.'):
        st = STAMPS[name]; w, h = st['w'], st['h']
        if x < 0 or x + w > self.W or y + h > self.H: return False
        foot = [(x + dx, y + h - 1 - dy) for dx in range(w) for dy in range(2)]        # trunk rows must be free
        return all(self.cls[yy, xx] in on and not self.taken[yy, xx] and not self.cliff[yy, xx] for xx, yy in foot if yy >= 0)

    def trees(self, cx, cy, n, kinds, r=4, on='.', seed=0):
        """a cluster of up to n yard trees around (cx, cy); canopies may overlap, trunks may not"""
        rng = random.Random(self.seed * 31 + seed + cx * 7 + cy); placed = 0
        for _ in range(n * 12):
            if placed >= n: break
            k = rng.choice(kinds); st = STAMPS[k]
            x = int(round(cx + rng.uniform(-r, r))) - st['w'] // 2; y = int(round(cy + rng.uniform(-r, r))) - st['h'] + 1
            if y >= 0 and self.can_tree(k, x, y, on):
                self.stamp(k, x, y, mark='B'); placed += 1
        return placed

    def fence(self, x0, x1, y, gaps=()):
        F = (C('sh', 4875 - 4448), C('sh', 4876 - 4448), C('sh', 4877 - 4448))
        for x in range(x0, x1 + 1):
            if any(a <= x <= b for a, b in gaps) or not self.inb(x, y): continue
            l = x == x0 or any(x == b + 1 for a, b in gaps); r = x == x1 or any(x == a - 1 for a, b in gaps)
            self.tile(F[0] if l and not r else F[2] if r and not l else F[1], x, y, 1); self.cls[y, x] = 'B'

    def ts(self):
        return R.tilesets()[self.tid]

    def blocked_stack(self, stack, ts):
        for t in reversed([int(v) for v in stack]):
            if t <= 0: continue
            if t >= RC.VBASE: continue
            if ts['passages'][t] & 15 == 15: return True
            if ts['priorities'][t] == 0: return False
        return False

    def tile(self, t, x, y, z=1):
        if self.inb(x, y): self.over.append((z, x, y, t)); self.taken[y, x] = True

    def snap(self, x, y, on='.dgDt', r=8):
        best = None
        for yy in range(y - r, y + r + 1):
            for xx in range(x - r, x + r + 1):
                if self.inb(xx, yy) and self.cls[yy, xx] in on and not self.taken[yy, xx] and not self.cliff[yy, xx]:
                    d = abs(xx - x) + abs(yy - y)
                    if best is None or d < best[0]: best = (d, xx, yy)
        if best is None: raise SystemExit('snap: nothing free near %d,%d' % (x, y))
        return (best[1], best[2])

    # ------------------------------------------------------------ paint
    def paint_ground(self):
        L = self.L
        g2 = getattr(self, 'grass2', None)
        for y in range(self.H):
            for x in range(self.W):
                L[0, y, x] = (g2 if g2 and vnoise(x, y, self.seed + 77, 4.0) > 0.52 else self.grass)[y % 2][x % 2]
        for y, x in np.argwhere(self.cls == 't'):
            L[0, y, x] = self.tall[(x * 7 + y * 3) % len(self.tall)] if isinstance(self.tall, list) else self.tall

    # class -> layer of its autotile: water on the ground layer; lanes, streets, beach sand and deep water on layer 2
    AUTO_Z = {'w': 0, 'd': 1, 'g': 1, 's': 1, 'W': 1, 'u': 1}
    JOIN = {'w': 'wW', 's': None, 'W': 'W'}          # None: everything except water joins (no shore edge toward land)

    def autotiles(self):
        """Each autotile class on its layer; neighbours of the same class (and the map edge) join."""
        water = np.isin(self.cls, ['w', 'W'])
        for c, (name, game) in self.auto.items():
            cells = self.cls == c
            if not cells.any(): continue
            j = self.JOIN.get(c, c)
            if j == 'all': j = None
            m = ~water if j is None else np.isin(self.cls, list(j))
            if j is None: m = m | cells
            base = RC.vauto(game, name, 0); z = self.AUTO_Z.get(c, 0)
            pad = np.pad(m, 1, constant_values=True)
            for y, x in np.argwhere(cells):
                b = 0
                for dx, dy, bit in ((0, -1, 1), (1, -1, 2), (1, 0, 4), (1, 1, 8), (0, 1, 16), (-1, 1, 32), (-1, 0, 64), (-1, -1, 128)):
                    if pad[y + 1 + dy, x + 1 + dx]: b |= bit
                self.L[z, y, x] = base + NB2AUTO[b]
        wg, wn = self.auto['w'][1], self.auto['w'][0]
        wbase = RC.vauto(wg, wn, 0)                           # water under the beach and deep band (edges show it)
        for y, x in np.argwhere(np.isin(self.cls, ['s', 'W'])):
            self.L[0, y, x] = wbase + 0
        if (self.cls == 's').any() or (self.cls == 'W').any():
            wm = np.isin(self.cls, ['w', 'W', 's'])
            pad = np.pad(wm, 1, constant_values=True)
            for y, x in np.argwhere(np.isin(self.cls, ['w', 'W', 's'])):
                b = 0
                for dx, dy, bit in ((0, -1, 1), (1, -1, 2), (1, 0, 4), (1, 1, 8), (0, 1, 16), (-1, 1, 32), (-1, 0, 64), (-1, -1, 128)):
                    if pad[y + 1 + dy, x + 1 + dx]: b |= bit
                self.L[0, y, x] = wbase + NB2AUTO[b]

    def cliffs(self):
        """Plateaus in `ht`.  The last high row of a plateau is the lip; the face rows hang below it on the LOW cells
        (kit rows 1..n).  High cells beside lower ground are 1-wide W/E sides; a high cell beside a lower plateau's
        lip or first face row is an inner corner; high cells under lower ground to the north get the north rim.
        Faces sit over grass (kit sh, also drawn on layer 1) or over water (kit ak)."""
        kitof = (lambda h: KITS[self.kit.get(h, self.kit.get('default', 'sh'))]) if isinstance(self.kit, dict) else (lambda h: KITS[self.kit])
        ht = self.ht; H, W = self.H, self.W
        piece = {}
        for y in range(H - 1):
            for x in range(W):
                h = ht[y, x]; nrows = len(kitof(h)['rows'])
                if ht[y + 1, x] < h:
                    piece[(x, y)] = ('row', 0, h)
                    for k in range(1, nrows):
                        if y + k >= H or ht[y + k, x] >= h: break
                        if (x, y + k) not in piece: piece[(x, y + k)] = ('row', k, h)
        for y in range(H):
            for x in range(W):
                if (x, y) in piece: continue
                h = ht[y, x]; K = kitof(h)
                wl = x > 0 and ht[y, x - 1] < h; el = x + 1 < W and ht[y, x + 1] < h
                wp = piece.get((x - 1, y)); ep = piece.get((x + 1, y))
                if wp and wp[0] == 'row' and wp[2] <= h and (wp[1] == 0 and wp[2] == h or wl) and wp[1] < 2 and K.get('inW'):
                    piece[(x, y)] = ('inW', wp[1], h)
                elif ep and ep[0] == 'row' and ep[2] <= h and (ep[1] == 0 and ep[2] == h or el) and ep[1] < 2 and K.get('inE'):
                    piece[(x, y)] = ('inE', ep[1], h)
                elif wl: piece[(x, y)] = ('W', 0, h)
                elif el: piece[(x, y)] = ('E', 0, h)
                elif y > 0 and ht[y - 1, x] < h: piece[(x, y)] = ('N', 0, h)
        for sx, sy, sw, sn in self.stairs_at:          # stairways cut the cliff: no pieces, the run ends beside them
            for yy in range(sy, sy + sn):
                for xx in range(sx, sx + sw): piece.pop((xx, yy), None)
        for (x, y), (kind, k, h) in piece.items():
            K = kitof(h)
            if kind == 'row':
                same = lambda xx: piece.get((xx, y), ('',))[0] == 'row' and piece[(xx, y)][1] == k
                wend, eend = not same(x - 1), not same(x + 1)
                t = K['rows'][k][0 if wend and not eend else 2 if eend and not wend else 1]
            elif kind == 'W': t = K['W']
            elif kind == 'E': t = K['E']
            elif kind == 'inW': t = K['inW'][k]
            elif kind == 'inE': t = K['inE'][k]
            else:
                wn = x > 0 and ht[y, x - 1] < h; en = x + 1 < W and ht[y, x + 1] < h
                t = K['N'][0 if wn else 2 if en else 1]
            if kind == 'row' and 0 < k < len(K['rows']) - 1 and K.get('vines') and self.rng.random() < K['vines'][1]:
                t = K['vines'][0] if t == K['rows'][k][1] else t
            z = 2 if self.L[1, y, x] and self.cls[y, x] in 'sdgW' else 1     # over a beach or lane: above it
            self.L[z, y, x] = t
            if K.get('l0') and self.cls[y, x] == '.' and kind == 'row' and t == K['rows'][k][1]: self.L[0, y, x] = t
            if kind != 'N': self.cliff[y, x] = True
            self.taken[y, x] = True
        self.pieces = piece

    STAIRS = (C('sh', 544), C('sh', 545), C('sh', 546))

    def stairs(self, x, ylip, w=3, n=None, kit_rows=4):
        """A wooden stairway w wide down a south face whose lip row is ylip (plan-time: cells become dirt lane)."""
        n = n or kit_rows
        self.stairs_at.append((x, ylip, w, n))
        for yy in range(ylip, ylip + n):
            for xx in range(x, x + w):
                self.cls[yy, xx] = 'd'

    def paint_stairs(self):
        for sx, sy, sw, sn in self.stairs_at:
            for yy in range(sy, sy + sn):
                for i, xx in enumerate(range(sx, sx + sw)):
                    self.L[2, yy, xx] = self.STAIRS[0 if i == 0 else 2 if i == sw - 1 else 1]
                    self.taken[yy, xx] = True; self.cliff[yy, xx] = False

    TREES_SH = [  # 3x4 forest trees: (top two rows on layer 3, bottom two rows on layer 2), weights
        ([[C('sh', 592), C('sh', 593), 0], [C('sh', 600), C('sh', 601), C('sh', 602)]],
         [[C('sh', 608), C('sh', 609), C('sh', 610)], [C('sh', 616), C('sh', 617), C('sh', 618)]], 5),
        ([[C('sh', 1504), C('sh', 1505), C('sh', 1506)], [C('sh', 1512), C('sh', 1513), C('sh', 1514)]],
         [[C('sh', 1520), C('sh', 1521), C('sh', 1522)], [C('sh', 1528), C('sh', 1529), C('sh', 1530)]], 4)]
    if SNOWT:
        TREES_SNOW = [([[SN('tree_sh', t) if t else 0 for t in row] for row in top], [[SN('tree_sh', t) for t in row] for row in bot], w)
                      for top, bot, w in (([[592, 593, 0], [600, 601, 602]], [[608, 609, 610], [616, 617, 618]], 5),
                                          ([[1504, 1505, 1506], [1512, 1513, 1514]], [[1520, 1521, 1522], [1528, 1529, 1530]], 4))]
    PINES = [([[C('rb4', 538), C('rb4', 539)], [C('rb4', 546), C('rb4', 547)]], [[C('rb4', 554), C('rb4', 555)]], 1)]
    lattice = None

    def forest(self, trees=None, mask=None, vstep=2):
        """Staggered lattice of trees on class T (Rejuvenation/Reborn habit): rows every `vstep`, period = tree width,
        each row shifted; the top rows go on layer 3, the trunk rows on layer 2."""
        trees = trees or self.lattice or self.TREES_SH
        m = (self.cls == 'T') if mask is None else mask
        wts = [t[2] for t in trees]
        tw = len(trees[0][1][0]); nt = len(trees[0][0]); nb = len(trees[0][1])
        phase = self.rng.randrange(tw)
        for ty in range(-nt, self.H, vstep):
            phase = (phase + self.rng.choice(range(1, tw)) if tw > 1 else 0) % tw
            for tx in range(phase - tw, self.W, tw):
                foot = [(tx + dx, ty + nt + dy) for dx in range(tw) for dy in range(nb)]
                if not all(m[y, x] for x, y in foot if self.inb(x, y)): continue
                if not any(self.inb(x, y) for x, y in foot): continue
                top, bot, _ = self.rng.choices(trees, wts)[0]
                for dy in range(nt):
                    for dx in range(tw):
                        x, y = tx + dx, ty + dy
                        if self.inb(x, y) and top[dy][dx] and self.L[2, y, x] == 0: self.L[2, y, x] = top[dy][dx]
                for dy in range(nb):
                    for dx in range(tw):
                        x, y = tx + dx, ty + nt + dy
                        if self.inb(x, y) and bot[dy][dx]: self.L[1, y, x] = bot[dy][dx]; self.taken[y, x] = True

    def put_stamps(self):
        lattice = {t for tr in (self.lattice or self.TREES_SH) for part in tr[:2] for row in part for t in row if t}
        for name, x, y in self.stamps:
            L = np.array(STAMPS[name]['layers']); h, w = L.shape[1:]
            for dy in range(h):
                for dx in range(w):
                    X, Y = x + dx, y + dy
                    t0, t1, t2 = (int(v) for v in L[:, dy, dx])
                    cur1 = int(self.L[1, Y, X])
                    if t0:
                        self.L[0, Y, X] = t0
                        if cur1 >= RC.VBASE: self.L[1, Y, X] = 0; cur1 = 0
                    if t1:
                        if cur1 >= RC.VBASE: self.L[0, Y, X] = cur1          # keep the lane / sand under the object
                        self.L[1, Y, X] = t1
                    elif t2 and cur1 in lattice:
                        self.L[1, Y, X] = 0                                   # a forest trunk under a roof goes
                    if t2: self.L[2, Y, X] = t2
        for z, x, y, t in self.over:
            if z == 1 and self.L[1, y, x] >= RC.VBASE: self.L[0, y, x] = self.L[1, y, x]
            self.L[z, y, x] = t

    def scatter(self, n_per_100=9, seed=3, on='.', groups=None, edge_boost=2.5):
        """Decor on free grass: green tufts and flowers, thicker along edges (walls, lanes, cliffs, trees) the way
        Rejuvenation's mappers dress the foot of things; flowers drift in noise patches; a few rare props."""
        groups = groups or self.decor
        open_ = (self.cls == '.') & ~self.taken & ~self.cliff & (self.L[1] == 0) & (self.L[2] == 0)
        pad = np.pad(open_, 1, constant_values=True)
        for y in range(self.H):
            for x in range(self.W):
                if not open_[y, x] or self.cls[y, x] not in on: continue
                edge = not pad[y:y + 3, x:x + 3].all()
                k = n_per_100 * (edge_boost if edge else 1.0)
                nz = vnoise(x, y, seed, 5.0)
                r = self.rng.random() * 100
                if nz > 0.58 and r < k * 2.4: self.L[1, y, x] = self.rng.choice(groups['flowers'])
                elif r < k: self.L[1, y, x] = self.rng.choice(groups['green'])
                elif r < k + 0.6: self.L[1, y, x] = self.rng.choice(groups['rare'])

    def paint(self):
        self.paint_ground(); self.autotiles(); self.cliffs(); self.paint_stairs(); self.forest(); self.put_stamps()
        return self.L

    # ------------------------------------------------------------ output
    def rubric(self):
        import build as B
        return B.rubric(RC.resolve(self.L, self.tid))

    def write(self, mid, head, comment=''):
        Lr = RC.resolve(self.L, self.tid).astype(np.int32)
        os.makedirs(os.path.join(HERE, 'data', 'raw'), exist_ok=True)
        rel = 'data/raw/%03d.npy' % mid
        np.save(os.path.join(HERE, rel), Lr)
        key = Lr[0].astype(np.int64) * 10 ** 10 + Lr[1].astype(np.int64) * 10 ** 5 + Lr[2]
        mir = (key == key[:, ::-1]).mean()
        print('map %d: mirror %.1f%%' % (mid, mir * 100))
        spec = dict(head); spec['raw'] = rel; spec['tileset'] = self.tid
        body = yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=150, allow_unicode=True)
        body += yaml.safe_dump({'events': self.events}, sort_keys=False, default_flow_style=None, width=150, allow_unicode=True)
        fn = head.get('_file') or '%03d.yaml' % mid
        spec.pop('_file', None)
        open(os.path.join(HERE, 'specs', fn), 'w').write(comment + body.replace("_file: %s\n" % fn, ''))
        return Lr

    def preview(self, path, scale=0.5, events=True):
        """Quick look without build.py: resolved layers + event markers (magenta = event, red = door)."""
        from PIL import Image, ImageDraw
        Lr = RC.resolve(self.L, self.tid)
        tc = R.TileCache(R.tilesets()[self.tid])
        im = Image.new('RGBA', (self.W * 32, self.H * 32), (0, 0, 0, 255))
        for z in range(3):
            for y in range(self.H):
                for x in range(self.W):
                    t = int(Lr[z, y, x])
                    if t:
                        ti = tc.tile(t)
                        if ti is not None: im.alpha_composite(ti, (x * 32, y * 32))
        if events:
            d = ImageDraw.Draw(im)
            for e in self.events:
                x, y = e['at']; c = (255, 0, 0, 255) if e.get('type') == 'door' else (255, 0, 255, 255)
                d.rectangle([x * 32 + 4, y * 32 + 4, x * 32 + 27, y * 32 + 27], outline=c, width=3)
        im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
        im.convert('RGB').save(path)
