"""villagekit: early-game town helpers on top of citykit (palette `village`, tileset 33).
Defines the prop stamps (data/stamps_v.json): giant tree-houses, laundry lines, net racks, silk lanterns, looms, dye vats,
crates, banners, flower bushes, cherry trees, silk bales and awnings; and Village, a City with garden/prop dressing passes."""
import os, sys, json, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import citykit
from citykit import City, STAMPS, HERE, vnoise
OFF = json.load(open(os.path.join(HERE, 'data', 'compose_offsets.json')))
C2 = OFF['custom2']['offset']; SH = OFF['sheridan']['offset']


def blk(t0, w, h):
    return [[t0 + r * 8 + c for c in range(w)] for r in range(h)]


def mk(rows, top=0, place=None):
    """rows: 2D ids (0 = empty). The first `top` rows go on layer 3 (walk-behind), the rest on layer 2."""
    h, w = len(rows), len(rows[0]); L = [[[0] * w for _ in range(h)] for _ in range(3)]
    for y in range(h):
        for x in range(w):
            L[2 if y < top else 1][y][x] = rows[y][x]
    return dict(tileset=33, w=w, h=h, layers=L)


def overlay(w, h, parts):
    """parts: [(layer, x, y, rows)]"""
    L = [[[0] * w for _ in range(h)] for _ in range(3)]
    for z, x0, y0, rows in parts:
        for y, row in enumerate(rows):
            for x, t in enumerate(row):
                if t: L[z][y0 + y][x0 + x] = t
    return dict(tileset=33, w=w, h=h, layers=L)


V = {
    'g_tree6': overlay(8, 8, [(1, 1, 3, blk(C2 + 40, 6, 5)), (2, 0, 0, blk(C2, 8, 5))]),            # door at (4, 7)
    'g_tree4': overlay(6, 7, [(1, 1, 3, blk(C2 + 80, 4, 4)), (2, 0, 0, blk(C2 + 160, 6, 4))]),      # door at (2, 6)
    'g_tree4p': overlay(6, 7, [(1, 1, 3, blk(C2 + 84, 4, 4)), (2, 0, 0, blk(C2 + 160, 6, 4))]),
    'g_tree2': overlay(4, 6, [(1, 1, 2, blk(C2 + 46, 2, 4)), (2, 0, 0, blk(C2 + 140, 4, 3))]),
    'p_laundry': mk([[C2 + 112, C2 + 113, C2 + 114]]),
    'p_net': mk(blk(C2 + 125, 2, 2), top=1),
    'p_loom': mk(blk(C2 + 123, 2, 2), top=1),
    'p_lantern': overlay(3, 3, [(2, 1, 0, [[C2 + 127]]), (1, 1, 1, [[C2 + 135]]), (1, 0, 1, [[C2 + 120, 0, C2 + 122]]),
                                (1, 0, 2, [[C2 + 128, C2 + 129, C2 + 130]])]),
    'p_vat_b': mk([[C2 + 118]]), 'p_vat_r': mk([[C2 + 119]]), 'p_vat_y': mk([[C2 + 136]]),
    'p_awning': overlay(3, 1, [(2, 0, 0, [[C2 + 137, C2 + 138, C2 + 139]])]),
    'p_crates': mk(blk(SH + 32, 3, 3), top=1),
    'p_banner': mk([[SH + 1], [SH + 9]], top=1),
    'p_banner3': mk([[SH + 52], [SH + 60], [SH + 68]], top=2),
    'p_sign': mk([[SH + 15]]), 'p_pot': mk([[SH + 14]]),
    'p_bush_w': mk(blk(SH + 19, 2, 2)), 'p_bush_g': mk(blk(SH + 21, 2, 2)), 'p_bush_r': mk([[SH + 23]]),
    'p_cherry': mk(blk(SH + 864, 3, 3), top=2),
    'p_pinkbush': mk(blk(SH + 776, 2, 2)), 'p_pinkbush2': mk(blk(SH + 792, 2, 2)),
    'p_silk': mk([[SH + 128], [SH + 136]]), 'p_silk1': mk([[SH + 822]]),
    'p_strand_w': mk([[SH + 809], [SH + 817]], top=1), 'p_strand_p': mk([[SH + 808], [SH + 816]], top=1),
    'p_web': overlay(3, 2, [(2, 0, 0, blk(3628, 3, 2))]), 'p_web1': overlay(2, 1, [(2, 0, 0, [[3622, 3623]])]),
    'p_rocks': mk(blk(SH + 859, 3, 3), top=1),
    'p_stump': mk([[SH + 3]]),
}
AT = os.path.join(os.path.dirname(HERE), 'art', 'tilesets')
for key, pre in (('town_props', 'tp_'), ('houses', 'hs_'), ('forest', 'fo_')):       # Art Director's curated stamps
    fp = os.path.join(AT, key + '_stamps.json')
    if not os.path.exists(fp) or 'pf_' + key not in OFF: continue
    base = OFF['pf_' + key]['offset'] - 384
    for st in json.load(open(fp)):
        x, y, w, h = st['tile_rect']
        rows = [[base + 384 + (y + r) * 8 + x + c for c in range(w)] for r in range(h)]
        V[pre + st['name']] = mk(rows, top=(h - 1 if st.get('kind') != 'house' else (1 if h >= 4 else 0)))
if 'hs_jonquil_08' in V:      # Ferrow's lighthouse: the octagonal tower of jonquil_08 without its loose base pieces
    L = V['hs_jonquil_08']['layers']; rows = [[L[1][y][x] or L[2][y][x] for x in range(5)] for y in range(9)]
    V['lh_ferrow'] = mk(rows, top=6)
json.dump(V, open(os.path.join(HERE, 'data', 'stamps_v.json'), 'w'))
STAMPS.update(V)
citykit.DOORS.update({'g_tree6': (4, 7), 'g_tree4': (2, 6)})
WS = [n + s for n in ('w_longhouse', 'w_cot', 'w_ell_a', 'w_manor_a', 'w_manor_b', 'w_ell_b', 'w_house') for s in ('', '_s', '_m')]
GARDEN = ['p_bush_w', 'p_bush_g', 'p_bush_r', 'p_pot', 'p_pinkbush', 'p_bush_r', 'p_pot', 'p_stump']


class Village(City):
    def door_path(self, door, to, c='d', width=2, seed=1, only='.,'):
        self.path([(door[0], door[1] + 1), (door[0], door[1] + 2), to], width, c, seed, only=only)

    def dress(self, names, n, on='.', seed=0, box=None, pad=1, near=None):
        """Scatter prop stamps on free cells of glyph set `on`; `near` = glyph set that must touch the prop (e.g. '#' walls)."""
        r = random.Random(self.seed * 41 + seed); k = 0; x0, y0, x1, y1 = box or (1, 1, self.W - 2, self.H - 2)
        for _ in range(n * 60):
            if k >= n: break
            nm = r.choice(names); st = STAMPS[nm]; w, h = st['w'], st['h']
            x = r.randint(x0, max(x0, x1 - w + 1)); y = r.randint(y0, max(y0, y1 - h + 1))
            if not self.free(x - pad, y - (1 if pad else 0), w + 2 * pad, h + (2 if pad else 0), on, level=True): continue
            if near and not any(self.inb(xx, yy) and self.g[yy][xx] in near for xx in range(x - 2, x + w + 2) for yy in range(y - 2, y + h + 2)): continue
            self.stamp(nm, x, y, force=True)
            for yy in range(y, y + h):
                for xx in range(x, x + w):
                    self.taken[yy][xx] = True
                    if self.g[yy][xx] == '#': self.g[yy][xx] = ','
            k += 1
        return k

    def stamp(self, name, x, y, link=None, dname=None, force=False, on=None, door=None, pad=0):
        d = City.stamp(self, name, x, y, link, dname, force, on, door, pad)
        if name.startswith('p_') or name.startswith('t_lamp'):
            st = STAMPS[name]
            for yy in range(y, y + st['h']):
                for xx in range(x, x + st['w']):
                    if self.inb(xx, yy) and self.g[yy][xx] == '#': self.g[yy][xx] = ','
        return d

    def borders(self, on='.', p=0.5, seed=0, glyph='H'):
        """Flower borders: free grass cells beside house walls (left, right, behind) become flower-bed autotile."""
        r = random.Random(self.seed * 43 + seed)
        for y in range(1, self.H - 1):
            for x in range(1, self.W - 1):
                if self.g[y][x] in on and not self.taken[y][x] and r.random() < p and vnoise(x, y, seed + 3, 3.0) > 0.35:
                    if self.g[y][x - 1] == '#' or self.g[y][x + 1] == '#' or self.g[y + 1][x] == '#':
                        self.g[y][x] = glyph; self.taken[y][x] = True

    def meadow(self, thr=0.62, seed=0, glyph='t', on='.'):
        for y in range(self.H):
            for x in range(self.W):
                if self.g[y][x] in on and not self.taken[y][x] and vnoise(x, y, self.seed + 77 + seed, 3.5) > thr:
                    self.g[y][x] = glyph

    def fence_run(self, pts, glyph='w', on='.'):
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            n = max(abs(x1 - x0), abs(y1 - y0))
            for i in range(n + 1):
                x = x0 + (x1 - x0) * i // max(1, n); y = y0 + (y1 - y0) * i // max(1, n)
                if self.inb(x, y) and self.g[y][x] in on and not self.taken[y][x]: self.g[y][x] = glyph; self.taken[y][x] = True

    def people(self, npcs, anchors, street='dco', sx=0):
        """Seat parsed script NPCs (scriptpour) on free street cells near the anchors, round-robin; returns events."""
        import scriptpour as SP
        out = []
        for i, n in enumerate(npcs):
            ax, ay = anchors[(i + sx) % len(anchors)]
            out.append(SP.npc_event(n, self.snap(ax, ay, street, r=10), move='random' if i % 3 == 0 else 'fixed'))
        return out

    def signs(self, signs, anchors, on='.'):
        import scriptpour as SP
        out = []
        for s, (ax, ay) in zip(signs, anchors):
            x, y = self.snap(ax, ay, on, r=8)
            if y > 0: self.taken[y - 1][x] = True
            out.append(SP.sign_event(s, (x, y)))
        return out
