"""citykit: layout helpers shared by the city layout scripts (Saltmere, Verdance, ...).
A City is a glyph grid + height grid + stamp/prop lists; write() emits a spec (palette `city`) for build.py.
Conventions: north is up; cliffs and walls show south faces; all houses face south onto a street."""
import os, sys, json, math, random
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
import yaml
from terrain import vnoise

STAMPS = {}
for fn in ('stamps_t.json', 'stamps_w.json', 'stamps_v.json'):
    p = os.path.join(HERE, 'data', fn)
    if os.path.exists(p):
        STAMPS.update(json.load(open(p)))
# door cell (dx, dy) inside each stamp that has one (bottom row unless noted)
DOORS = {'t_hall': (7, 15), 't_theatre': (3, 5), 't_house_red': (2, 4), 't_pokecenter': (2, 4), 't_mart': (1, 3),
         't_lodge': (1, 5), 'w_longhouse': (2, 6), 'w_ell_a': (7, 7), 'w_manor_a': (2, 8), 'w_manor_b': (2, 8),
         'w_ell_b': (2, 5), 'w_house': (2, 5), 'h_dome': (4, 8), 'h_manor': (5, 5), 't_shop_purple': (2, 5)}
POOL_TECT = ['h_green', 'h_gable_o', 'h_green2', 'h_chim_o', 'h_red', 'h_black', 'h_olive2', 't_house_red2',
             't_house_blue', 't_house_orange', 'h_big_o', 'h_teal', 'h_blue', 't_townhouse', 't_house_blue2']
POOL_TIMBER = ['w_longhouse', 'w_cot', 'w_ell_a', 'w_manor_a', 'w_manor_b', 'w_ell_b', 'w_house', 'w_house', 'w_cot']
POOL_SHOPS = ['t_stall', 't_shop_purple', 't_townhouse', 'h_teal', 'h_black']
POOL_DOCK = ['t_warehouse', 't_lodge', 'h_long_g', 't_house_blue', 'h_black', 't_warehouse']
UMBRELLAS = [3552, 3554, 3556, 3558, 3568, 3570, 3572]


class City:
    def __init__(self, W, H, seed, base='.'):
        self.W, self.H = W, H
        self.rng = random.Random(seed); self.seed = seed
        self.g = [[base] * W for _ in range(H)]
        self.ht = [[0] * W for _ in range(H)]
        self.taken = [[False] * W for _ in range(H)]
        self.stamps = []; self.tiles = []; self.blocks = []; self.events = []
        self.stairs_x = []          # (x0, x1, yrim) spans kept free of cliff tiles

    def inb(self, x, y): return 0 <= x < self.W and 0 <= y < self.H

    # ---------------------------------------------------------------- terrain
    def rect(self, x0, y0, w, h, c, only=None):
        for y in range(y0, y0 + h):
            for x in range(x0, x0 + w):
                if self.inb(x, y) and (only is None or self.g[y][x] in only):
                    self.g[y][x] = c

    def blob(self, cx, cy, rx, ry, c, seed=1, only='.', level=None, rough=0.5):
        for y in range(int(cy - ry - 2), int(cy + ry + 3)):
            for x in range(int(cx - rx - 2), int(cx + rx + 3)):
                if not self.inb(x, y) or self.g[y][x] not in only or self.taken[y][x]: continue
                if level is not None and self.ht[y][x] != level: continue
                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1.0 + rough * (vnoise(x, y, seed, 3.0) - 0.5):
                    self.g[y][x] = c

    def path(self, pts, width, c, seed=1, only=None):
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            n = int(max(abs(x1 - x0), abs(y1 - y0)) * 2) + 1
            for i in range(n + 1):
                t = i / n; x = x0 + (x1 - x0) * t; y = y0 + (y1 - y0) * t
                w = width + (1 if vnoise(x, y, seed, 4.0) > 0.6 else 0)
                self.rect(int(round(x - w / 2.0)), int(round(y - w / 2.0)), w, w, c, only)

    def set_heights(self, fn):
        self.ht = [[fn(x, y) for x in range(self.W)] for y in range(self.H)]

    def cliffs(self, face=2, keep=''):
        """Rim line wherever a higher level meets a lower one; south-facing edges get `face` extra rows.
        Cells whose glyph is in `keep` (walls, water) and stair spans are left alone."""
        W, H, ht = self.W, self.H, self.ht
        cl = [[False] * W for _ in range(H)]
        for y in range(H):
            for x in range(W):
                h = ht[y][x]
                if h < 1: continue
                low = any(self.inb(x + dx, y + dy) and max(ht[y + dy][x + dx], 0) < h for dx in (-1, 0, 1) for dy in (-1, 0, 1))
                if not low: continue
                cl[y][x] = True
                if y + 1 < H and max(ht[y + 1][x], 0) < h:
                    for k in range(1, face + 1):
                        if y + k < H and ht[y + k][x] >= 0: cl[y + k][x] = True
        for y in range(H):
            for x in range(W):
                if cl[y][x] and self.g[y][x] not in keep and not any(a <= x <= b and r <= y <= r + face + 1 for a, b, r in self.stairs_x):
                    self.g[y][x] = 'C'; self.taken[y][x] = True

    def stairs(self, x, yrim, n=1, kind='t_stairs'):
        """n side-by-side 3-wide stone stairways through a south-facing cliff whose rim row is yrim."""
        self.stairs_x.append((x, x + 3 * n - 1, yrim))
        for i in range(n):
            self.stamp(kind, x + 3 * i, yrim, force=True)

    # ---------------------------------------------------------------- castle kit
    def wall_h(self, x0, x1, y, face=2, gaps=(), top='W', fc='F', thick=2):
        """East-west curtain wall: parapet rows y..y+thick-1, face rows below. gaps = [(xa, xb)] left open (gates)."""
        for x in range(x0, x1 + 1):
            if any(a <= x <= b for a, b in gaps): continue
            for yy in range(y, y + thick + face):
                if self.inb(x, yy):
                    self.g[yy][x] = top if yy < y + thick else fc; self.taken[yy][x] = True

    def wall_v(self, x, y0, y1, face=2, gaps=(), top='W', fc='F', thick=2):
        """North-south wall: a parapet strip `thick` wide; its south end shows a face."""
        for y in range(y0, y1 + 1):
            if any(a <= y <= b for a, b in gaps): continue
            for xx in range(x, x + thick):
                if self.inb(xx, y): self.g[y][xx] = top; self.taken[y][xx] = True
        for yy in range(y1 + 1, y1 + 1 + face):          # face under the southern end
            for xx in range(x, x + thick):
                if self.inb(xx, yy) and self.g[yy][xx] not in 'WKQ':
                    self.g[yy][xx] = fc; self.taken[yy][xx] = True

    def tower(self, x, y, w=4, h=3, face=4, top='K', fc='G'):
        for yy in range(y, y + h + face):
            for xx in range(x, x + w):
                if self.inb(xx, yy):
                    self.g[yy][xx] = top if yy < y + h else fc; self.taken[yy][xx] = True

    def gate_arch(self, x, ybase):
        """Open archway (3 wide, 2 tall) set into a wall face; ybase = the face's bottom row. Walk in at (x+1, ybase)."""
        for dy, row in ((-1, (3979, 3980, 3981)), (0, (3987, 3988, 3989))):
            for dx, t in enumerate(row):
                self.tiles.append({'tile': t, 'at': [x + dx, ybase + dy], 'layer': 1})

    def gate_door(self, x, ybase):
        for dy, row in ((-1, (3963, 3964, 3965)), (0, (3971, 3972, 3973))):
            for dx, t in enumerate(row):
                self.tiles.append({'tile': t, 'at': [x + dx, ybase + dy], 'layer': 1})

    # ---------------------------------------------------------------- objects
    def free(self, x, y, w, h, on=None, level=True):
        if x < 0 or y < 0 or x + w > self.W or y + h > self.H: return False
        h0 = self.ht[y + h - 1][x]
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                if self.taken[yy][xx] or (on is not None and self.g[yy][xx] not in on): return False
                if level and self.ht[yy][xx] != h0: return False
        return True

    def stamp(self, name, x, y, link=None, dname=None, force=False, on=None, door=None, pad=0):
        st = STAMPS[name]; w, h = st['w'], st['h']
        if not force and not self.free(x - pad, y, w + 2 * pad, h, on): return None
        d = {'stamp': name, 'at': [x, y]}
        dd = door or DOORS.get(name) or DOORS.get(name[:-2] if name[-2:] in ('_s', '_m') else name)
        if link:
            d.update({'link': link, 'name': dname or name, 'door': list(dd)})
        self.stamps.append(d)
        occ = [[any(st['layers'][z][yy][xx] for z in range(3)) for xx in range(w)] for yy in range(h)]
        for yy in range(h):
            for xx in range(w):
                if self.inb(x + xx, y + yy) and (occ[yy][xx] or h > 3):
                    self.taken[y + yy][x + xx] = True
                    if self.g[y + yy][x + xx] in '.T': self.g[y + yy][x + xx] = '#'
        if h >= 4:                                  # keep the doorstep row free of trees and scatter
            for xx in range(x, x + w):
                if self.inb(xx, y + h) and self.g[y + h][xx] == '.': self.g[y + h][xx] = ','
        return (x + dd[0], y + dd[1]) if dd else (x + w // 2, y + h - 1)

    def house_row(self, x0, x1, yb, pool, gaps=(0, 0, 1, 1, 2), on='.#cpbk,', jitter=0):
        """Houses side by side with their bottom rows on yb (doors face the street below). Returns door cells."""
        x = x0; out = []; last = None
        while x <= x1:
            cand = [n for n in pool if n != last and x + STAMPS[n]['w'] - 1 <= x1]
            self.rng.shuffle(cand); done = False
            for n in cand:
                st = STAMPS[n]; j = self.rng.randint(0, jitter) if jitter else 0
                d = self.stamp(n, x, yb - j - st['h'] + 1, on=on)
                if d:
                    out.append((n, d)); x += st['w'] + (0 if x1 - (x + st['w']) < 10 else self.rng.choice(gaps)); last = n; done = True; break
            if not done: x += 1
        return out

    def quarter(self, x0, y0, x1, y1, pool, pad='c', pitch=7, gaps=(0, 0, 0, 1), beds=True, seed=0, first=None):
        """A built-up block: kerbed paving pad, packed house rows facing south (an alley between rows), then
        flower beds, shrubs and clutter in whatever is left. `first` = [(stamp, x, link, name)] placed on the front row."""
        r = random.Random(self.seed * 31 + x0 * 7 + y0 + seed)
        if pad: self.rect(x0, y0, x1 - x0 + 1, y1 - y0 + 1, pad, '.k')
        on = (pad or '.') + '#.k'
        doors = {}
        yb = y1 - 1
        for nm, x, link, dn in (first or []):
            doors[link or nm] = self.stamp(nm, x, yb - STAMPS[nm]['h'] + 1, link, dn, on=on)
        while yb - 4 >= y0:
            self.house_row(x0 + 1, x1 - 1, yb, pool, gaps=gaps, on=on)
            yb -= pitch + r.choice((0, 0, 1))
        if beds:
            for _ in range(max(1, (x1 - x0) * (y1 - y0) // 28)):
                w, h = r.choice(((2, 2), (3, 2), (2, 3), (4, 2))); x = r.randint(x0 + 1, max(x0 + 1, x1 - w)); y = r.randint(y0 + 1, max(y0 + 1, y1 - h))
                if self.free(x - 1, y - 1, w + 2, h + 2, (pad or '.'), level=False):
                    for yy in range(y, y + h):
                        for xx in range(x, x + w): self.g[yy][xx] = 'h'; self.taken[yy][xx] = True
        self.scatter_props(x0 + 1, y0 + 1, x1 - 1, y1 - 1, ['t_barrel', 't_barrel2', 't_board', 't_barrel', 't_bench'],
                           max(1, (x1 - x0) * (y1 - y0) // 50), (pad or '.'), seed + x0)
        for _ in range((x1 - x0) * (y1 - y0) // 30):
            x, y = r.randint(x0 + 1, x1 - 1), r.randint(y0 + 1, y1 - 1)
            if self.free(x, y, 1, 1, on, level=False) and self.g[y][x] == pad:
                self.tile(914, x, y, 1); self.taken[y][x] = True
        return doors

    def trees(self, x0, y0, w, h=2, only='.k'):
        """Tree pit / tree row: forest cells on an even row (the forest painter plants on even trunk rows)."""
        y0 -= y0 % 2
        for y in range(y0, y0 + h):
            for x in range(x0, x0 + w):
                if self.inb(x, y) and self.g[y][x] in only and not self.taken[y][x]: self.g[y][x] = 'T'

    def pits(self, n, on='k', seed=0, w=3):
        """Street trees: n grass planters (w x 2) with a tree, only where a 2-wide passage stays on every side."""
        r = random.Random(self.seed * 5 + seed); k = 0
        for _ in range(n * 60):
            if k >= n: break
            x = r.randint(3, self.W - w - 4); y = r.randint(2, self.H // 2 - 3) * 2
            if not self.free(x - 2, y - 2, w + 4, 6, on, level=True): continue
            for yy in (y, y + 1):
                for xx in range(x, x + w): self.g[yy][xx] = 'T'; self.taken[yy][xx] = True
            for xx in range(x - 1, x + w + 1):
                for yy in (y - 1, y + 2): self.taken[yy][xx] = True
            k += 1
        return k

    def groves(self, n, seed=0, rmin=1.6, rmax=3.5):
        """Tree clumps on whatever open grass is left (never on doorsteps, which are ','), plus undergrowth."""
        r = random.Random(self.seed * 3 + seed)
        for i in range(n):
            x, y = r.randint(2, self.W - 3), r.randint(2, self.H - 3)
            if self.g[y][x] == '.' and not self.taken[y][x]:
                self.blob(x, y, r.uniform(rmin, rmax), r.uniform(rmin, rmax) * 0.8, 'T', seed + i, only='.')

    # ---------------------------------------------------------------- organic plans (fix round)
    def hills(self, blobs, base=1):
        """Height map from irregular noise-edged blobs [(cx, cy, rx, ry, level, seed)]: elevation as masses, not bands."""
        def h(x, y):
            v = base
            for cx, cy, rx, ry, lv, sd in blobs:
                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1.0 + 0.55 * (vnoise(x, y, sd, 5.0) - 0.5) + 0.25 * (vnoise(x, y, sd + 1, 2.5) - 0.5):
                    v = max(v, lv) if lv >= 0 else lv
            return v
        self.set_heights(h)

    def notch(self, x0, x1, y, level, depth=40):
        """Cut a straight south-facing step into a hill so a stairway fits: columns x0..x1 drop below row y."""
        for x in range(x0 - 1, x1 + 2):
            for yy in range(y + 1, min(self.H, y + depth)):
                if self.ht[yy][x] >= level: self.ht[yy][x] = level - 1
            for yy in range(max(0, y - 3), y + 1):
                if self.ht[yy][x] < level: self.ht[yy][x] = level

    def is_street(self, x, y, street='kbcog='):
        return self.inb(x, y) and self.g[y][x] in street

    def front_place(self, name, near, link=None, dname=None, street='kbco', r=14):
        """Put a named building on the street frontage nearest to `near` (its door row sits just above street cells)."""
        st = STAMPS[name]; w, h = st['w'], st['h']; dd = DOORS.get(name, (w // 2, h - 1))
        cand = []
        for y in range(max(h, near[1] - r), min(self.H - 1, near[1] + r)):
            for x in range(max(0, near[0] - r), min(self.W - w, near[0] + r)):
                if self.is_street(x + dd[0], y + 1, street) and not self.is_street(x + dd[0], y, street):
                    cand.append(((x + dd[0] - near[0]) ** 2 + (y - near[1]) ** 2, x, y))
        for _, x, y in sorted(cand):
            if self.free(x, y - h + 1, w, h, on='.,#T'):
                return self.stamp(name, x, y - h + 1, link, dname)
        raise SystemExit('front_place: no frontage for %s near %s' % (name, near))

    def frontage(self, pool, box=None, street='kbco', seed=0, skip=0.0):
        """Pack houses wall to wall along every street: each sits with its bottom row directly above street cells."""
        r = random.Random(self.seed * 11 + seed); x0, y0, x1, y1 = box or (0, 0, self.W - 1, self.H - 1); n = 0
        for y in range(y1 - 1, y0, -1):
            x = x0
            while x <= x1:
                if not (self.is_street(x, y + 1, street) and not self.is_street(x, y, street)) or self.taken[y][x] or r.random() < skip:
                    x += 1; continue
                cand = list(pool); r.shuffle(cand); ok = False
                for nm in cand:
                    st = STAMPS[nm]; w, h = st['w'], st['h']
                    if x + w - 1 > x1 or y - h + 1 < y0: continue
                    if sum(self.is_street(xx, y + 1, street) for xx in range(x, x + w)) * 2 < w: continue
                    if self.free(x, y - h + 1, w, h, on='.,#T') and self.stamp(nm, x, y - h + 1):
                        x += w; n += 1; ok = True; break
                if not ok: x += 1
        return n

    def backfill(self, pool, box=None, p=0.6, seed=0):
        """Second rank: houses behind the frontage wherever a footprint is still free (alleys of roofs, Prizca-style)."""
        r = random.Random(self.seed * 17 + seed); x0, y0, x1, y1 = box or (0, 0, self.W - 1, self.H - 1); n = 0
        for y in range(y1, y0, -1):
            x = x0
            while x <= x1:
                nm = r.choice(pool); st = STAMPS[nm]; w, h = st['w'], st['h']
                if r.random() < p and x + w - 1 <= x1 and y - h + 1 >= y0 and self.free(x, y - h + 1, w, h, on='.#T') \
                        and self.stamp(nm, x, y - h + 1):
                    x += w + r.choice((0, 0, 1)); n += 1
                else: x += 1
        return n

    def greenfill(self, thr=0.38, seed=0, beds=0.10, box=None):
        """Whatever land is left becomes garden: tree masses where the noise is high, flower beds and lawn elsewhere."""
        r = random.Random(self.seed * 19 + seed); x0, y0, x1, y1 = box or (0, 0, self.W - 1, self.H - 1)
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if self.g[y][x] != '.' or self.taken[y][x]: continue
                if vnoise(x, y, self.seed + seed, 4.0) > thr: self.g[y][x] = 'T'
                elif r.random() < beds: self.g[y][x] = 'h'

    def edge_props(self, names, n, street='kbc', seed=0):
        """Street furniture hugging the building line (lamps, barrels, boards, benches); the carriageway stays clear."""
        r = random.Random(self.seed * 23 + seed); k = 0
        for _ in range(n * 80):
            if k >= n: break
            nm = r.choice(names); st = STAMPS[nm]; w, h = st['w'], st['h']
            x, y = r.randint(1, self.W - w - 2), r.randint(h, self.H - 3)
            if not all(self.is_street(xx, y, street) and not self.taken[y][xx] for xx in range(x, x + w)): continue
            if self.is_street(x, y - 1, street) and self.is_street(x - 1, y, street) and self.is_street(x + w, y, street): continue
            if not all(self.is_street(xx, y + dy, street) and not self.taken[y + dy][xx] for xx in range(x - 1, x + w + 1) for dy in (1, 2)): continue
            if any(self.taken[yy][xx] and (self.g[yy][xx] in street) for xx in range(x - 2, x + w + 2) for yy in range(y - 1, y + 2) if self.inb(xx, yy)): continue
            if self.free(x, y - h + 1, w, h, level=False) and self.stamp(nm, x, y - h + 1): k += 1
        return k

    def snap(self, x, y, street='kbco', r=8):
        """Nearest free street cell to (x, y); the cell is reserved (events stand there, props keep off)."""
        best = None
        for yy in range(max(1, y - r), min(self.H - 1, y + r + 1)):
            for xx in range(max(1, x - r), min(self.W - 1, x + r + 1)):
                if self.g[yy][xx] in street and not self.taken[yy][xx]:
                    d = (xx - x) ** 2 + (yy - y) ** 2
                    if best is None or d < best[0]: best = (d, xx, yy)
        if best is None: raise SystemExit('snap: no street near %d,%d' % (x, y))
        self.taken[best[2]][best[1]] = True
        return [best[1], best[2]]

    def mirror(self):
        """Share of land cells equal to their mirror image (open water is exempt, as in the rubric)."""
        n = t = 0
        for y in range(self.H):
            for x in range(self.W):
                a, b = self.g[y][x], self.g[y][self.W - 1 - x]
                if a == '~' and b == '~': continue
                t += 1; n += a == b
        return n / float(max(1, t))

    def prop(self, name, x, y, on=None):
        return self.stamp(name, x, y, on=on)

    def tile(self, t, x, y, layer=1):
        if self.inb(x, y): self.tiles.append({'tile': t, 'at': [x, y], 'layer': layer})

    def block(self, t, x, y, w, h, layer=1, on=None):
        if not self.free(x, y, w, h, on, level=False): return False
        self.blocks.append({'tile': t, 'size': [w, h], 'at': [x, y], 'layer': layer})
        for yy in range(y, y + h):
            for xx in range(x, x + w): self.taken[yy][xx] = True
        return True

    def lamps(self, cells):
        for x, y in cells:                      # (x, y) = lamp foot
            self.stamp('t_lamp', x, y - 2)

    def scatter_props(self, x0, y0, x1, y1, names, n, on, seed=0):
        r = random.Random(self.seed * 77 + seed); k = 0
        for _ in range(n * 30):
            if k >= n: break
            nm = r.choice(names); st = STAMPS[nm]
            x = r.randint(x0, max(x0, x1 - st['w'] + 1)); y = r.randint(y0, max(y0, y1 - st['h'] + 1))
            if self.free(x - 1, y, st['w'] + 2, st['h'] + 1, on) and self.stamp(nm, x, y, on=on): k += 1
        return k

    def inlay(self, x0, y0, x1, y1, on, tiles, p, seed=3):
        """Swap a share of plain paving cells for drain / inlay variants (layer 0)."""
        r = random.Random(self.seed * 13 + seed)
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if self.inb(x, y) and self.g[y][x] == on and not self.taken[y][x] and r.random() < p:
                    nb = [self.g[yy][xx] for xx, yy in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)) if self.inb(xx, yy)]
                    if all(c == on for c in nb): self.tiles.append({'tile': r.choice(tiles), 'at': [x, y], 'layer': 0})

    def sea_rocks(self, n, avoid=(), seed=9):
        r = random.Random(self.seed + seed); got = []
        for _ in range(n * 40):
            if len(got) >= n: break
            x, y = r.randrange(1, self.W - 2), r.randrange(1, self.H - 2)
            if any(self.g[yy][xx] != '~' or self.taken[yy][xx] for xx in range(x - 1, x + 3) for yy in range(y - 1, y + 3)): continue
            if any(abs(x - a) < 3 and abs(y - b) < 3 for a, b in got): continue
            if any(a <= x <= c and b <= y <= d for a, b, c, d in avoid): continue
            if r.random() < 0.3:
                for dx, dy, t in ((0, 0, 1552), (1, 0, 1553), (0, 1, 1560), (1, 1, 1561)): self.tile(t, x + dx, y + dy, 2)
            else:
                a = r.choice([(1554, 1562), (1555, 1563)]); self.tile(a[0], x, y, 2); self.tile(a[1], x, y + 1, 2)
            got.append((x, y))

    # ---------------------------------------------------------------- events
    def warp_line(self, cells, to_map, to_cells, d='retain'):
        for (x, y), (tx, ty) in zip(cells, to_cells):
            self.events.append({'type': 'warp', 'at': [x, y], 'to': {'map': to_map, 'x': tx, 'y': ty, 'dir': d}})

    def write(self, fname, head, comment='', mirror_max=0.40):
        m = self.mirror()                      # symmetry guard: the glyph plan may not mirror itself left-right
        print('%s: plan mirror match %.1f%% (limit %.0f%%)' % (fname, m * 100, mirror_max * 100))
        if m > mirror_max:
            raise SystemExit('%s: layout is too symmetric (%.1f%% of cells equal their mirror image)' % (fname, m * 100))
        rows = [''.join(r) for r in self.g]
        hr = [''.join(str(min(9, max(h, 0))) for h in r) for r in self.ht]
        spec = dict(head)
        body = yaml.safe_dump(spec, sort_keys=False, default_flow_style=None, width=150, allow_unicode=True)
        body += 'map: |\n' + '\n'.join('  ' + r for r in rows) + '\nheights: |\n' + '\n'.join('  ' + r for r in hr) + '\n'
        body += yaml.safe_dump({'stamps': self.stamps, 'tiles': self.tiles, 'tileblocks': self.blocks, 'events': self.events},
                               sort_keys=False, default_flow_style=None, width=150, allow_unicode=True)
        open(os.path.join(HERE, 'specs', fname), 'w').write(comment + body)
