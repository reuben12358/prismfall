"""interiorkit: timber rooms on tileset 34 (palette `interior`). Walls and floor are Rejuvenation's SheridanInside set;
furniture is mined at run time from the Sheridan interior maps (objects only) or listed from Tectonic's Inside sheet.
A Room emits a spec with explicit tiles; events are given by the caller."""
import os, sys, json
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
import yaml
import rmarshal as M
OFF = json.load(open(os.path.join(HERE, 'data', 'compose_offsets.json')))
SI = OFF['in_sheridan']['offset'] - 384
WD = '/home/claude/ref/art/wll/Changed Files/Data'
_maps = {}
VOID = 5437
# Sheridan furniture: name -> (map, x, y, w, h)
SF = {'bed_w': (27, 9, 4, 3, 2), 'plantrack': (27, 3, 3, 1, 3), 'fern': (27, 3, 5, 1, 2), 'yellowrug': (27, 3, 7, 2, 2),
      'shelf': (36, 5, 0, 2, 4), 'bed_o': (36, 31, 2, 3, 3), 'chest': (36, 35, 2, 3, 2), 'sofa': (36, 8, 9, 5, 2),
      'table_long': (36, 8, 12, 5, 2), 'table_sm': (36, 7, 17, 2, 1), 'bed_s': (40, 9, 38, 2, 3), 'study': (40, 36, 7, 5, 8),
      'stairs': (40, 59, 21, 3, 4), 'counter': (40, 58, 27, 5, 4), 'dining': (40, 11, 69, 9, 7), 'pantry': (40, 51, 26, 4, 7),
      'deskflowers': (40, 11, 42, 5, 2), 'tallcab': (40, 33, 57, 1, 5), 'radio': (40, 65, 27, 2, 3), 'plants3': (36, 3, 15, 3, 3),
      'shelves2': (40, 8, 7, 15, 3)}
# Tectonic Inside furniture (ids are the sheet's own): rows; `top` rows go on layer 3
TF = {'heal': ([[2706, 2707], [2714, 2715], [2722, 2723]], 1), 'counter4': ([[2716, 2717, 2718, 2719]], 0),
      'shelf_green': ([[2720, 2721], [2728, 2729]], 1), 'shelf_goods': ([[2748, 2749], [2756, 2757], [2764, 2765]], 2),
      'display': ([[2772, 2773], [2780, 2781]], 1), 'display2': ([[2774, 2775], [2782, 2783]], 1), 'tv': ([[2704, 2705], [2712, 2713]], 1),
      'kitchen': ([[2448, 2449, 2450, 2451], [2456, 2457, 2458, 2459]], 1), 'table_w': ([[2485, 2486], [2493, 2494], [2501, 2502]], 1),
      'dresser': ([[2488, 2489, 2490], [2496, 2497, 2498]], 1), 'desk': ([[2512, 2513], [2520, 2521]], 1),
      'cabinet': ([[2515, 2516], [2523, 2524]], 1), 'plant': ([[2539], [2547], [2555]], 2),
      'food_table': ([[2557, 2558], [2565, 2566], [2573, 2574]], 1), 'wardrobe': ([[4080, 4081], [4088, 4089]], 1),
      'workbench': ([[4082, 4083, 4084], [4090, 4091, 4092]], 1), 'shrub': ([[4085], [4093]], 1), 'drawer': ([[4096, 4097], [4104, 4105]], 1),
      'bigbed': ([[4098, 4099, 4100], [4106, 4107, 4108], [4114, 4115, 4116], [4122, 4123, 4124]], 1),
      'lifering': ([[4118, 4119], [4126, 4127]], 0), 'crates3': ([[4136, 4137, 4138], [4144, 4145, 4146], [4152, 4153, 4154]], 1),
      'bunk_o': ([[4140, 4141], [4148, 4149], [4156, 4157]], 1), 'bunk_b': ([[4142, 4143], [4150, 4151], [4158, 4159]], 1),
      'crate': ([[4168, 4169], [4176, 4177]], 1), 'crate_i': ([[4170, 4171], [4178, 4179]], 1), 'crate_i2': ([[4172, 4173], [4180, 4181]], 1),
      'labtank': ([[4784, 4785], [4792, 4793], [4800, 4801], [4808, 4809]], 2), 'console': ([[4779, 4780, 4781], [4787, 4788, 4789]], 1),
      'pallet': ([[4824, 4825], [4832, 4833]], 0), 'barrel_y': ([[4822], [4830]], 1), 'barrel_b': ([[4823], [4831]], 1),
      'sofa_g': ([[3571, 3572, 3573, 3574], [3579, 3580, 3581, 3582]], 1), 'web': ([[2790, 2791], [2798, 2799]], 0),
      'bed_blue': ([[3568, 3569, 3570], [3576, 3577, 3578], [3584, 3585, 3586], [3592, 3593, 3594]], 1)}


def _map(i):
    if i not in _maps: _maps[i] = M.load_file('%s/Map%03d.rxdata' % (WD, i)).data.data
    return _maps[i]


class Room:
    def __init__(self, w, h, door_x=None, pad=2):
        """w x h = floor size. The map adds `pad` void cells around, 3 wall rows on top and the door notch below."""
        self.w, self.h, self.pad = w, h, pad
        self.W = max(20, w + 2 * pad + 2); self.H = max(15, h + pad + 3 + 2 + pad)   # RMXP's minimum map is 20x15
        self.x0 = pad + 1; self.y0 = pad + 3                      # first floor cell
        self.t = []; self.events = []; self.occ = set()
        self.door_x = self.x0 + (w // 2 - 1 if door_x is None else door_x)
        x0, y0, x1, y1 = self.x0, self.y0, self.x0 + w - 1, self.y0 + h - 1
        P = self.put0
        for x in range(x0, x1 + 1):
            P(x, y0 - 3, 5534); P(x, y0 - 2, 5547); P(x, y0 - 1, 5555)
            for y in range(y0, y1 + 1):
                P(x, y, (5352 if x == x0 else 5353 + (x - x0 - 1) % 3) if y == y0 else (5360 if x == x0 else 5361 + (x - x0 - 1) % 3))
            P(x, y1 + 1, 5550)
        for y in range(y0 - 2, y1 + 1): P(x0 - 1, y, 5541); P(x1 + 1, y, 5543)
        P(x0 - 1, y0 - 3, 5533); P(x1 + 1, y0 - 3, 5535); P(x0 - 1, y1 + 1, 5549); P(x1 + 1, y1 + 1, 5551)
        P(x0, y0 - 2, 5563); P(x0, y0 - 1, 5571); P(x1, y0 - 2, 5564); P(x1, y0 - 1, 5572)
        dx = self.door_x                                              # door notch, 3 wide
        for i in range(3): P(dx + i, y1 + 1, 5361 + i % 3); P(dx + i, y1 + 2, 5550); self.t.append((1, dx + i, y1 + 1, 5512 + i))
        P(dx - 1, y1 + 1, 5554); P(dx + 3, y1 + 1, 5553); P(dx - 1, y1 + 2, 5549); P(dx + 3, y1 + 2, 5551)
        self.exit = (dx + 1, y1 + 1)

    def put0(self, x, y, t):
        self.t = [q for q in self.t if not (q[0] == 0 and q[1] == x and q[2] == y)]; self.t.append((0, x, y, t))

    def window(self, fx):
        x = self.x0 + fx; self.put0(x, self.y0 - 2, 5544); self.put0(x, self.y0 - 1, 5552)

    def sf(self, name, fx, fy):
        """Sheridan furniture at floor coords (fx, fy) = top-left (may start on the wall rows with fy < 0)."""
        m, sx, sy, w, h = SF[name]; D = _map(m)
        for z in (1, 2):
            for dy in range(h):
                for dx in range(w):
                    t = int(D[z, sy + dy, sx + dx])
                    if t >= 384: self.t.append((z, self.x0 + fx + dx, self.y0 + fy + dy, t + SI)); self.occ.add((fx + dx, fy + dy))

    def tf(self, name, fx, fy):
        rows, top = TF[name]
        for dy, row in enumerate(rows):
            for dx, t in enumerate(row):
                self.t.append((2 if dy < top else 1, self.x0 + fx + dx, self.y0 + fy + dy, t)); self.occ.add((fx + dx, fy + dy))

    def tile(self, t, fx, fy, z=1):
        self.t.append((z, self.x0 + fx, self.y0 + fy, t)); self.occ.add((fx, fy))

    def at(self, fx, fy): return [self.x0 + fx, self.y0 + fy]

    def spec(self, head, events, exit_link=None):
        ev = []
        if exit_link: ev.append({'type': 'exit', 'at': list(self.exit), 'link': exit_link})
        s = dict(head); s['palette'] = 'interior'
        s['map'] = '\n'.join('.' * self.W for _ in range(self.H)) + '\n'
        s['tiles'] = [{'tile': t, 'at': [x, y], 'layer': z} for z, x, y, t in self.t]
        s['events'] = ev + events
        return s


def write(fname, specs, comment=''):
    out = comment + '\n---\n'.join(yaml.safe_dump(s, sort_keys=False, default_flow_style=None, width=160, allow_unicode=True) for s in specs)
    open(os.path.join(HERE, 'specs', fname), 'w').write(out)
