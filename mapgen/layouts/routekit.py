"""routekit: the road-leg generator for the massive routes (map builder 9, ROUTES.yaml legs).  A route is written as a
recipe: the road's waypoints (a Catmull-Rom lane from exit to exit), the open land that follows it, clearings and
encounter fields, terraces crossed by stairways, water (sea and beach, river, ponds), a side path to a dead end that
pays, a secret pocket behind a Cut tree, a landmark, then events.  Everything not opened is the staggered tree lattice
(forest borders come from what the place is: woods, or the sea and its cliffs).

    r = Route(527, 140, 64, 'coast', seed=527)
    r.road([(139, 30), (100, 26), ...]); r.exit('E', 28, 4); r.sea('S', 14); ...; r.finish(head)

Themes: meadow / forest (tileset 53, Sea(Grass) water), coast / dunes / marsh (51, Ocean, sand beach, Akuwa sea cliffs),
snow (52, rimewood.snowmap)."""
import os, sys, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
np = np
import rkit as K
from rkit import C, STAMPS
from terrain import vnoise
vnoise = vnoise
import rimewood as RW

trainer, npc, sign, item = RW.trainer, RW.npc, RW.sign, RW.item
DIRS = {'N': (0, -1), 'S': (0, 1), 'W': (-1, 0), 'E': (1, 0)}


def hidden(at, it, name='HiddenItem'):
    return {'type': 'item', 'at': list(at), 'item': it, 'hidden': True, 'name': name}


def talk(name, at, sprite, lines, d='down', move='fixed', again=None):
    return RW.npc(at, name, sprite, lines, d, move, again)


class Route:
    def __init__(self, mid, W, H, theme='meadow', seed=None, kit=None, base='T'):
        self.mid, self.W, self.H, self.theme = mid, W, H, theme
        seed = mid if seed is None else seed
        self.rng = random.Random(seed); self.seed = seed
        if theme == 'snow':
            m = RW.snowmap(W, H, mid, kit=kit or 'shs')
        elif theme in ('coast', 'dunes', 'marsh'):
            m = K.RMap(W, H, 51, mid, water='Ocean', kit=kit or {1: 'sh3', 2: 'sh3', 3: 'sh3', 'default': 'sh3'})
            m.auto = {'d': ('DirtDark', 'rejuvenation'), 'w': ('Ocean', 'rejuvenation'), 's': ('Sand shore_2', 'rejuvenation'),
                      'W': ('Sea deep', 'rejuvenation'), 'g': ('Gravel Spring', 'pf'), 'u': ('Dirt', 'rejuvenation')}
        else:
            m = K.RMap(W, H, 53, mid, water='Sea(Grass)', kit=kit or 'sh3')
            m.auto = {'d': ('DirtDark', 'rejuvenation'), 'w': ('Sea(Grass)', 'rejuvenation'), 'u': ('Dirt', 'rejuvenation'),
                      'g': ('Gravel(G)', 'rejuvenation')}
        if 'sh3' not in K.KITS:
            K.KITS['sh3'] = dict(K.KITS['sh'], rows=[K.KITS['sh']['rows'][0], K.KITS['sh']['rows'][1], K.KITS['sh']['rows'][3]])
        m.cls[:, :] = base
        self.m = m
        self.road_mask = np.zeros((H, W), bool)
        self.events = []; self.exits = []; self.keep = []
        self.deck = []

    # ------------------------------------------------------------------ plan
    def road(self, pts, w=3.0, c='d', open_=(2, 6), wobble=0.4, only='T.t'):
        """the road: a lane through pts, with open land along it (width varies with noise between open_[0] and open_[1])"""
        m = self.m
        before = m.cls == c
        m.lane(pts, c=c, w=w, seed=self.seed + len(self.exits) * 7 + int(pts[0][0]), only=only, wobble=wobble)
        self.road_mask |= (m.cls == c) & ~before
        if open_:
            self.open_along(m.cls == c, *open_)

    def open_along(self, mask, lo, hi, seed=None):
        m = self.m
        from collections import deque
        D = np.full((self.H, self.W), 99); q = deque()
        for y, x in np.argwhere(mask): D[y, x] = 0; q.append((y, x))
        while q:
            y, x = q.popleft()
            if D[y, x] >= hi: continue
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                Y, X = y + dy, x + dx
                if 0 <= Y < self.H and 0 <= X < self.W and D[Y, X] > D[y, x] + 1:
                    D[Y, X] = D[y, x] + 1; q.append((Y, X))
        s = self.seed + 101 if seed is None else seed
        for y in range(self.H):
            for x in range(self.W):
                if 0 < D[y, x] <= hi and m.cls[y, x] == 'T':
                    lim = lo + (hi - lo) * vnoise(x, y, s, 7.0)
                    if D[y, x] <= lim: m.cls[y, x] = '.'

    def forest_band(self, side, depth, wobble=3.0, scale=9.0, only='.t'):
        """woods along one edge (the inland side of a coast road, the far side of a meadow)"""
        m = self.m; s = self.seed + 505 + ord(side)
        for y in range(self.H):
            for x in range(self.W):
                t = {'S': self.H - 1 - y, 'N': y, 'W': x, 'E': self.W - 1 - x}[side]
                along = x if side in 'NS' else y
                if t < depth + wobble * (vnoise(along, 0, s, scale) - 0.5) * 2 and m.cls[y, x] in only: m.cls[y, x] = 'T'

    def copse(self, cx, cy, rx, ry, rough=0.6):
        self.m.blob(cx, cy, rx, ry, 'T', seed=self.seed + int(cx * 3 + cy * 11), rough=rough, only='.t')

    def clearing(self, cx, cy, rx, ry, c='.', rough=0.5, only='T'):
        self.m.blob(cx, cy, rx, ry, c, seed=self.seed + int(cx * 13 + cy), rough=rough, only=only)

    def lane(self, pts, w=2.0, c='d', open_=(1, 3)):
        """a side path (narrower), with a little open land"""
        self.road(pts, w=w, c=c, open_=open_, wobble=0.3)

    def grass(self, thr=0.58, scale=6.0, keep_road=2, box=None, seed=None):
        """encounter fields: noise patches of tall grass on open land, kept off the road edge"""
        m = self.m; s = self.seed + 202 if seed is None else seed
        x0, y0, x1, y1 = box or (0, 0, self.W, self.H)
        road = np.isin(m.cls, list('dgs')) | self.road_mask
        pad = np.pad(road, keep_road); near = np.zeros_like(road)
        for dy in range(-keep_road, keep_road + 1):
            for dx in range(-keep_road, keep_road + 1):
                near |= pad[keep_road + dy:keep_road + dy + self.H, keep_road + dx:keep_road + dx + self.W]
        for y in range(y0, y1):
            for x in range(x0, x1):
                if m.cls[y, x] in '.u' and not near[y, x] and vnoise(x, y, s, scale) > thr: m.cls[y, x] = 't'

    def water(self, cx, cy, rx, ry, c='w', rough=0.6):
        self.m.blob(cx, cy, rx, ry, c, seed=self.seed + int(cx + cy * 7), rough=rough, only=None)

    def sea(self, side, depth, wobble=4.0, beach=3, deep=6, cliff=0, scale=12.0):
        """the sea along one side: open water, a deep band at the edge, a sand beach (or a cliff edge when cliff=h: the
        land behind is raised to h so the Akuwa sea-cliff kit stands on the beach)"""
        m = self.m; s = self.seed + 303
        for y in range(self.H):
            for x in range(self.W):
                t = {'S': self.H - 1 - y, 'N': y, 'W': x, 'E': self.W - 1 - x}[side]
                along = x if side in 'NS' else y
                d = depth + wobble * (vnoise(along, 0, s, scale) - 0.5) * 2
                if t < d: m.cls[y, x] = 'W' if t < d - deep and deep else 'w'
                elif t < d + beach: m.cls[y, x] = 's' if m.cls[y, x] != 'd' or True else m.cls[y, x]
                elif cliff and t >= d + beach: m.ht[y, x] = max(m.ht[y, x], cliff)

    def terraces(self, bands, wobble=2.5, scale=10.0, x_range=None):
        """horizontal terraces climbing north: bands = [(y_lip, h)], every cell north of (y_lip + wobble noise) gets at
        least height h (lip on the last high row); the road crosses each with stairs (crossing())"""
        m = self.m
        for i, (yl, h) in enumerate(bands):
            for x in range(self.W):
                if x_range and not (x_range[0] <= x <= x_range[1]): continue
                yy = int(round(yl + wobble * (vnoise(x, i, self.seed + 404 + i, scale) - 0.5) * 2))
                m.ht[:yy + 1, x] = np.maximum(m.ht[:yy + 1, x], h)

    def flatten(self, x0, x1, y_lip, h):
        """straighten a terrace's lip between x0..x1 to y_lip (where a stairway crosses)"""
        m = self.m
        for x in range(x0 - 2, x1 + 3):
            if not (0 <= x < self.W): continue
            m.ht[max(0, y_lip - 3):y_lip + 1, x] = np.maximum(m.ht[max(0, y_lip - 3):y_lip + 1, x], h)
            m.ht[y_lip + 1:y_lip + 6, x] = np.minimum(m.ht[y_lip + 1:y_lip + 6, x], h - 1)

    def crossing(self, x, y_lip, w=3, rows=3):
        self.m.stairs(x, y_lip, w=w, kit_rows=rows, c='d')

    def exit(self, side, offset, width, depth=4):
        """open the map edge at offset..offset+width-1 and run the road stub into it"""
        m = self.m
        for k in range(width):
            for t in range(depth):
                if side in 'NS':
                    x = offset + k; y = t if side == 'N' else self.H - 1 - t
                else:
                    y = offset + k; x = t if side == 'W' else self.W - 1 - t
                if m.inb(x, y) and m.cls[y, x] in 'T.t': m.cls[y, x] = 'd'
        self.exits.append((side, offset, width))

    def plank_bridge(self, x0, y0, x1, y1):
        """a timber bridge or boardwalk over water (cells stay water class; planks painted after)"""
        for y in range(min(y0, y1), max(y0, y1) + 1):
            for x in range(min(x0, x1), max(x0, x1) + 1):
                self.deck.append((x, y))

    def pocket(self, cx, cy, rx, ry, gate=None, cut=True):
        """a secret pocket: a clearing walled by forest, entered through one gap that holds a Cut tree"""
        self.clearing(cx, cy, rx, ry, '.', rough=0.4)
        if gate:
            gx, gy = gate; m = self.m
            m.cls[gy, gx] = '.'
            if cut: self.events.append({'type': 'cut_tree', 'at': [gx, gy], 'name': 'CutTree'})

    # ------------------------------------------------------------------ dressing
    def stamp(self, name, x, y, **kw):
        return self.m.stamp(name, x, y, **kw)

    def near(self, name, x, y, on='.', r=4):
        return self.m.near(name, x, y, on=on, r=r)

    def add(self, *evs):
        self.events += [e for e in evs if e]

    def finish_plan(self, border=3):
        m = self.m
        if border:                                                    # a forest rim on every land edge (exits stay open)
            def opening(side, i):
                return any(s == side and o - 1 <= i < o + w + 1 for s, o, w in self.exits)
            for y in range(self.H):
                for x in range(self.W):
                    for side, t, i in (('N', y, x), ('S', self.H - 1 - y, x), ('W', x, y), ('E', self.W - 1 - x, y)):
                        if t < border and not opening(side, i) and m.cls[y, x] in '.t' and m.ht[y, x] == m.ht[min(self.H - 1, max(0, y)), x]:
                            m.cls[y, x] = 'T'
        m.plan_cliffs()
        for sx, sy, sw, sn in m.stairs_at:
            m.cls[sy:sy + sn, sx:sx + sw] = 'd'
        for y, x in np.argwhere(np.isin(m.cls, ['d', 's', 'w', 'W']) & (m.ht > 0) & False): pass

    def seat_events(self, on='.dts'):
        m = self.m
        for x, y in K.incoming(self.mid):
            if m.inb(x, y): m.taken[y, x] = True
        self.events = RW.seat(m, self.events, on=on + 'D')
        for e in self.events:
            if e.get('type') == 'sign': e['post'] = False; m.tile(C('sh', 4847 - 4448), e['at'][0], e['at'][1], 1)

    def dress(self, trees=('tr_oak', 'tr_oak2', 'tr_pine', 'tr_pine2', 'tr_teal'), n_trees=None, copses=None, scatter=9,
              rocks=0, greenfill=None):
        """yard trees and copses on the open land, (optionally) leftover lawn far from the road to forest, decor"""
        m = self.m
        keep = np.zeros((self.H, self.W), bool)
        for e in self.events:
            x, y = e['at']; keep[max(0, y - 2):y + 3, max(0, x - 2):x + 3] = True
        for x, y in K.incoming(self.mid): keep[max(0, y - 2):y + 3, max(0, x - 2):x + 3] = True
        for side, off, w in self.exits:
            for k in range(-1, w + 1):
                if side in 'NS':
                    x = off + k; y0 = 0 if side == 'N' else self.H - 4
                    if 0 <= x < self.W: keep[y0:y0 + 4, x] = True
                else:
                    y = off + k; x0 = 0 if side == 'W' else self.W - 4
                    if 0 <= y < self.H: keep[y, x0:x0 + 4] = True
        was = m.taken.copy(); m.taken |= keep
        n = n_trees if n_trees is not None else self.W * self.H // 120
        for _ in range(copses if copses is not None else self.W * self.H // 400):
            m.trees(self.rng.randrange(self.W), self.rng.randrange(self.H), self.rng.choice((2, 3, 4)), list(trees), r=3,
                    seed=self.rng.randrange(9999), on='.')
        m.autotrees(n, list(trees), on='.', seed=self.seed, gap=2)
        if greenfill: m.greenfill(greenfill, on='.')
        m.taken = was | (m.taken & ~keep)
        self._scatter = scatter

    def paint(self, glint=0.0):
        m = self.m
        m.events = list(self.events)
        m.paint()
        for x, y in self.deck:
            if m.inb(x, y): m.L[1, y, x] = C('sh', 497)
        m.scatter(self._scatter if hasattr(self, '_scatter') else 9, seed=self.mid)
        keep = [tuple(e['at']) for e in self.events if e.get('type') in ('warp',)]
        self.sealed = m.seal_edges(self.exits, keep=keep)
        if glint:
            G = [K.P1('hb_glint%d' % i) for i in range(4)]
            for y, x in np.argwhere(np.isin(m.cls, ['w', 'W'])):
                if m.L[1, y, x] == 0 and m.L[2, y, x] == 0 and (x, y) not in self.deck and self.rng.random() < glint * (0.4 + vnoise(x, y, self.seed, 6.0)):
                    m.L[2, y, x] = self.rng.choice(G)

    def write(self, head, fname, comment, preview=None):
        m = self.m
        connections = head.pop('connections', [])
        head['connections'] = connections
        head['_file'] = fname
        m.write(self.mid, head, comment)
        if preview: m.preview(preview, 0.5)


def head(mid, name, field=None, bgm='Route 1', weather=None, biome='route', **kw):
    md = {'Outdoor': True, 'ShowArea': True, 'BattleBack': 'field'}
    if weather: md['Weather'] = weather
    h = {'id': mid, 'name': name, 'parent': 0, 'bgm': bgm, 'metadata': md, 'rubric': True, 'yards_ok': True, 'biome': biome}
    if field: h['field'] = field
    h.update(kw)
    return h
