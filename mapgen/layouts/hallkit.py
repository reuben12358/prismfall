"""layouts/hallkit.py - paints puzzle interiors on tileset 54 "PF Rejuv Halls" (compose_halls.py) from a glyph grid.

Two looks, both Rejuvenation's own tiles (only tiles are taken; the layouts are ours):
  'loom'   timber hall (Multi-Interiors: Sensei's House): plank floor, cream panel walls in a dark timber frame
  'stage'  theatre (Multi-Gym Interior: Goldenleaf Theatre): purple-framed black wall mass, pale panel walls
Cell classes (the caller maps its glyphs onto them): void, wall (a wall FACE: 2+ rows above a floor), floor, floor2,
pit, stair.  Wall-mass edges are drawn automatically in the void cells that touch the room, so every room needs a
one-cell void margin.  Writes data/raw/NNN.npy (final tile ids) and returns the `raw:` spec keys."""
import os, json, random
import numpy as np

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_H = json.load(open(os.path.join(HERE, 'data', 'halls.json')))
TID = 54


def MI(i): return _H['mi'][str(i)]
def MG(i): return _H['mg'][str(i)]
def PF(i): return _H['pf'][str(i)]
def CU(n): return _H['cu'][n]


STYLES = {
    'loom': dict(void=MI(404),
                 # void cell whose room lies: S, N, E, W; diagonal only SE, SW, NE, NW; two sides S+E, S+W, N+E, N+W
                 edge={'S': MI(1252), 'N': MI(1268), 'E': MI(1259), 'W': MI(1261), 'SE': MI(1251), 'SW': MI(1253), 'NE': MI(1267),
                       'NW': MI(1269), 'S+E': MI(1274), 'S+W': MI(1273), 'N+E': MI(1266), 'N+W': MI(1265)},
                 wall_hi=[MI(1249)], wall_lo=[MI(1257)], post_hi=MI(1250), post_lo=MI(1258), post_every=5,
                 end_l=(MI(1281), MI(1289)), end_r=(MI(1282), MI(1290)),
                 floor=[MI(1241), MI(1242), MI(1243)], floor_sh=[MI(1233), MI(1234), MI(1235)], floor2=[MI(1049)], floor2_sh=[MI(1049)],
                 stair=MI(962), pit=CU('warp'), pit_top=CU('warp_top'), pit_bot=CU('warp_bot')),
    'lobby': dict(void=MG(4508),
                  edge={'S': MG(4516), 'N': MG(4500), 'E': MG(4509), 'W': MG(4507), 'SE': MG(4502), 'SW': MG(4503), 'NE': MG(4510),
                        'NW': MG(4511), 'S+E': MG(4517), 'S+W': MG(4515), 'N+E': MG(4501), 'N+W': MG(4499)},
                  wall_hi=[MG(4630)], wall_lo=[MG(4638)], post_hi=MG(1704), post_lo=MG(1704), post_every=0,
                  end_l=None, end_r=None, door=((MG(4577), MG(4578), MG(4579)), (MG(4585), MG(4586), MG(4587))),
                  floor=[MG(4603)], floor_sh=[MG(4595)], floor2=[MG(4603)], floor2_sh=[MG(4595)],
                  frame=dict(l=MG(4602), r=MG(4604), b=MG(4611), bl=MG(4610), br=MG(4612), tl=MG(4594), tr=MG(4596)),
                  stair=MG(3151), pit=MG(4508), pit_top=MG(4508), pit_bot=MG(4508)),
    'stage': dict(void=MG(4508),
                  edge={'S': MG(4516), 'N': MG(4500), 'E': MG(4509), 'W': MG(4507), 'SE': MG(4502), 'SW': MG(4503), 'NE': MG(4510),
                        'NW': MG(4511), 'S+E': MG(4517), 'S+W': MG(4515), 'N+E': MG(4501), 'N+W': MG(4499)},
                  wall_hi=[MG(4524)], wall_lo=[MG(4532)], post_hi=MG(4520), post_lo=MG(4528), post_every=6,
                  end_l=None, end_r=None,
                  floor=[MI(1241), MI(1242), MI(1243)], floor_sh=[MI(1233), MI(1234), MI(1235)], floor2=[MG(4702)], floor2_sh=[MG(4694)],
                  stair=MG(3151), pit=MG(4508), pit_top=MG(4508), pit_bot=MG(4508),
                  door=((MG(4521), MG(4522), MG(4523)), (MG(4529), MG(4530), MG(4531))),
                  lip=MG(4489), seat=(MG(4691), MG(4692)), seat_back=MG(4683)),
}
# multi-tile objects: name -> (rows of ids, layer of each row)
OBJ = {
    'loom': ([[PF(17876), PF(17877)], [PF(17884), PF(17885)]], [1, 1]),
    'web': ([[PF(17746), PF(17747), PF(17748)], [PF(17749), PF(17750), PF(17751)]], [2, 2]),
    'web1': ([[PF(17744), PF(17745)]], [2]),
    'laundry': ([[PF(17869), PF(17870), PF(17871)]], [1]),
    'awning': ([[PF(17890), PF(17891), PF(17892)]], [2]),
    'vat_b': ([[PF(17872)]], [1]), 'vat_r': ([[PF(17873)]], [1]), 'vat_y': ([[PF(17889)]], [1]),
    'silk': ([[PF(17752)], [PF(17753)]], [1, 1]), 'silk1': ([[PF(17758)]], [1]),
    'lantern': ([[PF(18113)], [PF(18114)], [PF(18115)]], [2, 2, 1]),
    'plant': ([[MI(584)], [MI(592)]], [2, 1]),
    'shelf': ([[MI(1230), MI(1231)], [MI(1238), MI(1239)], [MI(1246), MI(1247)], [MI(1254), MI(1255)]], [2, 1, 1, 1]),
    'door_mi': ([[MI(1016), MI(1277), MI(1018)], [MI(1024), MI(1285), MI(1026)]], [1, 1]),
    'mat_mi': ([[MI(2696), MI(2697), MI(2698)]], [1]),
    'mat_mg': ([[MG(1731), MG(1732), MG(1733)]], [1]),
    'urn': ([[MG(1710)], [MG(1718)]], [2, 1]),
    'rope_h': ([[MG(1802), MG(1803), MG(1804)]], [2]),
    'poster_rain': ([[MG(4704), MG(4705), MG(4706)], [MG(4712), MG(4713), MG(4714)], [MG(4720), MG(4721), MG(4722)]], [1, 1, 1]),
    'poster_lady': ([[MG(4634), MG(4635), MG(4636)], [MG(4642), MG(4643), MG(4644)], [MG(4650), MG(4651), MG(4652)]], [1, 1, 1]),
    'poster_green': ([[MG(5184), MG(5185), MG(5186)], [MG(5192), MG(5193), MG(5194)], [MG(5200), MG(5201), MG(5202)]], [1, 1, 1]),
    'rug_mg': ([[MG(4645)] + [MG(4646)] * 4 + [MG(4647)], [MG(4653)] + [MG(4654)] * 4 + [MG(4655)], [MG(4661)] + [MG(4662)] * 4 + [MG(4663)]], [1, 1, 1]),
    'couch_l': ([[MG(4656)], [MG(4664)], [MG(4672)]], [2, 2, 2]),
    'couch_r': ([[MG(4657)], [MG(4665)], [MG(4673)]], [2, 2, 2]),
    'pillar': ([[MG(1704)]], [0]),
    'drape_top': ([[MG(4681)]], [1]), 'drape': ([[MG(4689)]], [1]), 'drape_bot': ([[MG(4697)]], [1]),
    'door_mg': ([[MG(4521), MG(4522), MG(4523)], [MG(4529), MG(4530), MG(4531)]], [1, 1]),
}


class Hall:
    def __init__(self, rows, style, classes, seed=0):
        self.rows = [list(r) for r in rows]; self.H, self.W = len(rows), len(rows[0])
        assert all(len(r) == self.W for r in rows), 'ragged grid'
        self.st = STYLES[style]; self.cls = classes; self.r = random.Random(seed)
        self.L = np.zeros((3, self.H, self.W), dtype=np.int32)
        self.paint()

    def c(self, x, y):
        if not (0 <= x < self.W and 0 <= y < self.H): return 'void'
        return self.cls.get(self.rows[y][x], 'floor')

    def paint(self):
        st, L = self.st, self.L
        for y in range(self.H):
            for x in range(self.W):
                k = self.c(x, y); up = self.c(x, y - 1); dn = self.c(x, y + 1)
                if k == 'void':
                    L[0, y, x] = st['void']
                    room = lambda dx, dy: self.c(x + dx, y + dy) != 'void'
                    n, s, e, w = room(0, -1), room(0, 1), room(1, 0), room(-1, 0)
                    key = None
                    if s and e: key = 'S+E'
                    elif s and w: key = 'S+W'
                    elif n and e: key = 'N+E'
                    elif n and w: key = 'N+W'
                    elif s: key = 'S'
                    elif n: key = 'N'
                    elif e: key = 'E'
                    elif w: key = 'W'
                    elif room(1, 1): key = 'SE'
                    elif room(-1, 1): key = 'SW'
                    elif room(1, -1): key = 'NE'
                    elif room(-1, -1): key = 'NW'
                    if key: L[0, y, x] = st['edge'][key]
                elif k == 'wall':
                    lo = dn != 'wall'
                    post = st['post_every'] and x % st['post_every'] == 2
                    t = (st['post_lo'] if lo else st['post_hi']) if post else self.r.choice(st['wall_lo'] if lo else st['wall_hi'])
                    if st['end_l'] and self.c(x - 1, y) == 'void': t = st['end_l'][1 if lo else 0]
                    if st['end_r'] and self.c(x + 1, y) == 'void': t = st['end_r'][1 if lo else 0]
                    L[0, y, x] = t
                elif k == 'door':                       # a 3-wide double door set into the bottom two rows of a wall
                    lo = dn != 'wall' and dn != 'door'
                    col = sum(1 for dx in (1, 2) if self.c(x - dx, y) == 'door')
                    L[0, y, x] = st['door'][1 if lo else 0][col]
                elif k == 'lip':                        # the stage front: a lit edge over the dark under-stage
                    L[0, y, x] = st['void']; L[1, y, x] = st['lip']
                elif k == 'seat':
                    L[0, y, x] = st['floor2'][0]; L[1, y, x] = st['seat'][y % 2]; L[2, y, x] = st['seat_back']
                    if up != 'seat': L[2, y - 1, x] = st['seat_back']
                elif k in ('floor', 'floor2'):
                    sh = up in ('wall', 'door', 'lip')
                    L[0, y, x] = self.r.choice(st[k + '_sh'] if sh else st[k])
                    fr = st.get('frame')
                    if fr:
                        lv, rv, bv = self.c(x - 1, y) == 'void', self.c(x + 1, y) == 'void', self.c(x, y + 1) == 'void'
                        if sh and lv: L[0, y, x] = fr['tl']
                        elif sh and rv: L[0, y, x] = fr['tr']
                        elif bv and lv: L[0, y, x] = fr['bl']
                        elif bv and rv: L[0, y, x] = fr['br']
                        elif lv: L[0, y, x] = fr['l']
                        elif rv: L[0, y, x] = fr['r']
                        elif bv and not sh: L[0, y, x] = fr['b']
                elif k == 'stair':
                    L[0, y, x] = st['floor'][0]; L[1, y, x] = st['stair']
                elif k == 'pit':
                    L[0, y, x] = st['pit_top'] if up != 'pit' else (st['pit_bot'] if dn != 'pit' else st['pit'])

    def put(self, t, x, y, z=1):
        if 0 <= x < self.W and 0 <= y < self.H: self.L[z, y, x] = t

    def obj(self, name, x, y):
        rows, zs = OBJ[name]
        for dy, (r, z) in enumerate(zip(rows, zs)):
            for dx, t in enumerate(r): self.put(t, x + dx, y + dy, z)

    def write(self, mid):
        os.makedirs(os.path.join(HERE, 'data', 'raw'), exist_ok=True)
        rel = 'data/raw/%03d.npy' % mid
        np.save(os.path.join(HERE, rel), self.L)
        return {'raw': rel, 'tileset': TID}


def tile_event(name, x, y, pages):
    """Multi-page tile event. pages: [(cond dict or None, tile id or None, extra page keys)]."""
    out = []
    for cond, tile, *extra in pages:
        pg = {}
        if cond: pg['cond'] = cond
        if tile: pg['graphic'] = {'tile': tile}
        if extra: pg.update(extra[0])
        out.append(pg)
    return {'type': 'event', 'name': name, 'at': [x, y], 'pages': out}


def exact(var, k, tile, top, hidden=None):
    """Pages that show `tile` exactly while var == k (RMXP only tests >=): values 0..top."""
    pages = [(None, tile if k == 0 else hidden)]
    if k > 0: pages.append(({'var': [var, k]}, tile))
    if k < top: pages.append(({'var': [var, k + 1]}, hidden))
    return pages


def apprentice(name, sprite, x, y, room, greeting=None, direction='down'):
    call = 'pfp_apprentice(:%s, "%s"%s)' % (room, name, (', "%s"' % greeting.replace('"', '\\"')) if greeting else '')
    return {'type': 'npc', 'name': 'Apprentice ' + name, 'at': [x, y], 'sprite': sprite, 'dir': direction, 'commands': [{'script': call}]}
