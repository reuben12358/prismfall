#!/usr/bin/env python3
"""compose_wilds.py (builder 3) - tileset 40 "Prismfall Wilds" for the early routes, the Gossamer Wood, the Glassed
Orchard and Cocoonfall Hollow, and tileset 41 "Prismfall Loomhouse" for Gym 1 and the two small interiors.

Tileset 40 = Tectonic's Outside sheet with ids unchanged (so the `tectonic` painters, learned tables and stamps keep
working), then Rejuvenation `Route 2_new` and `Goldenleaf Forrest` (passages and priorities from the WLL Tilesets.rxdata,
safe parser; terrain tags zeroed), then a BLEED recolour of the whole Tectonic part (glassed, wrong-coloured land: same
passages, priorities and tags), then a small custom strip drawn here on the 16-px grid (silk, cocoons, light shafts).
Autotile slots: Waterfall2, Tall Grass, Bleed water (custom), Tall Grass Flowers 1, Tall Grass Flowers 2, water2,
Bleed grass (custom) - slots 1, 2, 4, 5, 6 match tilesets 30/33.
Offsets and custom tile names -> data/compose_wilds_offsets.json.   Run: python3 -I compose_wilds.py"""
import os, sys, json, colorsys, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import rmarshal as M
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(os.path.dirname(HERE), 'maps_out')
REG = os.path.join(OUT, 'tilesets_prismfall.json')
WLL = '/home/claude/ref/art/wll/Changed Files'
TAUTO = '/home/claude/ref/art/tectonic/Graphics/Autotiles'
CUSTOM = '/home/claude/ref/art/custom'
Image.MAX_IMAGE_PIXELS = None


def ramp(stops, t):
    t = max(0.0, min(1.0, t)) * (len(stops) - 1); i = min(int(t), len(stops) - 2); f = t - i
    return tuple(int(round(stops[i][k] + (stops[i + 1][k] - stops[i][k]) * f)) for k in range(3))


GLASS = [(22, 20, 54), (52, 46, 118), (96, 92, 190), (150, 160, 232), (214, 226, 250)]       # foliage -> blue-violet glass
ROSE = [(40, 14, 44), (104, 36, 92), (176, 80, 140), (232, 160, 196), (255, 226, 236)]         # wood, earth -> rose quartz
ASH = [(60, 54, 78), (120, 112, 140), (176, 170, 192), (214, 210, 226), (240, 238, 246)]       # ground grass -> ashen lilac
GALL = [(30, 8, 40), (92, 20, 96), (170, 44, 150), (236, 110, 200), (255, 200, 240)]           # water -> gall pink


def bleed_colour(rgb, ground=False):
    r, g, b = rgb
    h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
    lum = (0.30 * r + 0.59 * g + 0.11 * b) / 255.0
    if s < 0.12:
        return (int(r * 0.92), int(g * 0.90), min(255, int(b * 1.04)))
    if 0.17 <= h <= 0.47:
        return ramp(ASH if ground else GLASS, lum * (1.0 if ground else 1.15))
    if h < 0.17 or h > 0.93:
        return ramp(ROSE, lum * 1.05)
    if 0.47 < h < 0.72:
        return ramp(GALL, lum * 1.05)
    return rgb


def recolour(im, ground_rows=()):
    im = im.copy(); px = im.load(); cache = {}
    for y in range(im.height):
        gr = any(a <= y // 32 < b for a, b in ground_rows)
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a == 0: continue
            k = (r, g, b, gr)
            if k not in cache: cache[k] = bleed_colour((r, g, b), gr)
            px[x, y] = cache[k] + (a,)
    return im


# ------------------------------------------------------------------ custom strip (16-px logical grid, doubled)
class Strip:
    def __init__(self):
        self.tiles = []; self.names = {}

    def add(self, name, im, passage=0, priority=0, tag=0):
        """im: w*32 x h*32 RGBA; registers tiles row-major, name -> index of the top-left tile (rows padded to 8)."""
        w, h = im.width // 32, im.height // 32
        if len(self.tiles) % 8 + w > 8: self.pad()
        base = len(self.tiles); self.names[name] = base
        need = (h - 1) * 8 + w
        while len(self.tiles) < base + need + (8 - (base + need) % 8) % 8: self.tiles.append(None)
        for j in range(h):
            for i in range(w):
                p = passage[j][i] if isinstance(passage, list) else passage
                q = priority[j][i] if isinstance(priority, list) else priority
                self.tiles[base + j * 8 + i] = (im.crop((i * 32, j * 32, i * 32 + 32, j * 32 + 32)), p, q, tag)
        return base

    def pad(self):
        while len(self.tiles) % 8: self.tiles.append(None)

    def image(self):
        self.pad()
        im = Image.new('RGBA', (256, len(self.tiles) // 8 * 32), (0, 0, 0, 0))
        for i, t in enumerate(self.tiles):
            if t: im.paste(t[0], (i % 8 * 32, i // 8 * 32))
        return im


def canvas(w, h): return Image.new('RGBA', (w * 16, h * 16), (0, 0, 0, 0))
def dbl(im): return im.resize((im.width * 2, im.height * 2), Image.NEAREST)
SILK = [(250, 250, 255, 255), (222, 226, 240, 255), (184, 190, 214, 255), (140, 146, 178, 255)]


def strand(pts, w=1, a=235, col=SILK[0]):
    im = canvas(1, 1) if max(max(p) for p in pts) < 16 else canvas(2, 2)
    d = ImageDraw.Draw(im); d.line(pts, fill=col[:3] + (a,), width=w)
    return im


def draw_custom():
    S = Strip(); rnd = random.Random(40)
    # --- silk strands (passable overlays, drawn above the player) ---
    for name, pts in (('strand_h', [(0, 7), (4, 8), (11, 8), (15, 7)]), ('strand_v', [(8, 0), (7, 5), (8, 11), (8, 15)]),
                      ('strand_d1', [(0, 0), (6, 5), (10, 11), (15, 15)]), ('strand_d2', [(15, 0), (10, 5), (5, 10), (0, 15)])):
        im = canvas(1, 1); d = ImageDraw.Draw(im)
        d.line(pts, fill=SILK[2], width=1)
        d.line([(x, y - 1) for x, y in pts] if name == 'strand_h' else [(x - 1, y) for x, y in pts], fill=SILK[0], width=1)
        for i in range(3):
            x, y = pts[1 + i % 2]; d.point((x + rnd.randint(-2, 2), y + rnd.randint(-2, 2)), fill=SILK[1])
        S.add(name, dbl(im), 0, 3)
    # --- web fans for corners (1x1 each): NW, NE, SW, SE ---
    for name, (ox, oy) in (('web_nw', (0, 0)), ('web_ne', (15, 0)), ('web_sw', (0, 15)), ('web_se', (15, 15))):
        im = canvas(1, 1); d = ImageDraw.Draw(im)
        sx = 1 if ox == 0 else -1; sy = 1 if oy == 0 else -1
        for k, (ex, ey) in enumerate(((15, 2), (13, 8), (8, 13), (2, 15))):
            d.line([(ox, oy), (ox + sx * ex, oy + sy * ey)], fill=SILK[0] if k % 2 == 0 else SILK[1])
        for r in (5, 9, 13):
            pts = [(ox + sx * int(r * c), oy + sy * int(r * s)) for c, s in ((1.0, 0.12), (0.86, 0.5), (0.5, 0.86), (0.12, 1.0))]
            d.line(pts, fill=SILK[1])
        S.add(name, dbl(im), 0, 3)
    S.pad()
    # --- silk floor mat: 3x3 blob (NW N NE / W C E / SW S SE), passable ground overlay ---
    mat = canvas(3, 3); px = mat.load()
    for y in range(48):
        for x in range(48):
            dx = min(x, 47 - x); dy = min(y, 47 - y); edge = min(dx, dy)
            rag = (x * 7 + y * 13) % 5
            if edge < 2 + (rag < 2) - (dx < 3 and dy < 3) * -2: continue
            if dx < 4 and dy < 4 and dx + dy < 5: continue
            c = SILK[1] if (x + y * 3) % 7 else SILK[0]
            if (x * 3 + y) % 11 == 0 or edge < 4: c = SILK[2]
            if (x - y) % 9 == 0: c = SILK[0]
            px[x, y] = c[:3] + (225,)
    S.add('silkmat', dbl(mat), 0, 0)
    # --- cocoon (1x2) and great cocoon (2x3); bottoms block ---
    def cocoon(w, h, hang=True):
        im = canvas(w, h); d = ImageDraw.Draw(im); W, H = w * 16, h * 16
        if hang: d.line([(W // 2, 0), (W // 2, 5)], fill=SILK[1]); d.line([(W // 2 - 1, 0), (W // 2 - 1, 3)], fill=SILK[0])
        box = (2, 4, W - 3, H - 2)
        d.ellipse(box, fill=SILK[1], outline=(96, 100, 136, 255))
        d.ellipse((box[0] + 2, box[1] + 1, box[2] - 3, box[3] - 5), fill=SILK[0])
        for k in range(box[1] + 4, box[3] - 2, 3):
            xs = int(((W - 6) / 2.0) * (1 - ((k - (box[1] + box[3]) / 2.0) / ((box[3] - box[1]) / 2.0)) ** 2) ** 0.5)
            d.line([(W // 2 - xs + 1, k + 1), (W // 2, k - 1), (W // 2 + xs - 2, k + 1)], fill=SILK[2])
        d.arc((box[0] + 1, box[1] + 1, box[2] - 1, box[3] - 1), 20, 110, fill=SILK[3])
        d.ellipse((2, H - 4, W - 3, H - 1), fill=(40, 60, 50, 90))
        return dbl(im)
    S.add('cocoon', cocoon(1, 2), [[0], [15]], [[2], [0]])
    S.add('cocoon_big', cocoon(2, 3), [[0, 0], [15, 15], [15, 15]], [[2, 2], [1, 1], [0, 0]])
    S.add('cocoon_low', cocoon(1, 1, False), 15, 0)
    # --- silk curtain: 1x2 hanging sheet that blocks (the forest's silk walls), plus a 1x1 web knot ---
    cur = canvas(1, 2); d = ImageDraw.Draw(cur)
    for x in range(16):
        top = 1 + (x * 5) % 3; bot = 29 + (x * 7) % 3
        col = SILK[(x // 2 + (x % 5 == 0)) % 3]
        d.line([(x, top), (x, bot)], fill=col[:3] + (238,))
    for y in (6, 13, 21, 27):
        d.line([(0, y), (5, y + 1), (10, y - 1), (15, y)], fill=SILK[3][:3] + (255,))
    S.add('curtain', dbl(cur), [[15], [15]], [[1], [0]])
    S.pad()
    # --- light shaft 2x4: translucent, passable, above everything ---
    sh = canvas(2, 4); px = sh.load()
    for y in range(64):
        for x in range(32):
            c = x + y * 0.42 - 18
            if 0 <= c < 12:
                a = int(58 * (1 - abs(c - 6) / 6.5) * (1 - y / 80.0)) + (10 if (x + y) % 2 == 0 else 0)
                px[x, y] = (255, 246, 200, max(0, a))
    S.add('shaft', dbl(sh), 0, 5)
    # --- leaf shade 2x2: translucent dark dapple on the ground under giant trees ---
    sd = canvas(2, 2); px = sd.load()
    for y in range(32):
        for x in range(32):
            r = ((x - 15.5) / 15.0) ** 2 + ((y - 15.5) / 13.0) ** 2
            if r < 1.0 and (x * 5 + y * 3) % 4 != 0: px[x, y] = (16, 40, 34, int(80 * (1 - r) + 16))
    S.add('shade', dbl(sd), 0, 0)
    # --- Art Director prototypes: silk-wrapped tree and crystal tree (2x3; trunk rows block) ---
    for name, fn in (('silk_tree', 'silk_tree_2x3.png'), ('crystal_tree', 'crystal_tree_2x3.png')):
        im = Image.open(os.path.join(CUSTOM, fn)).convert('RGBA')
        S.add(name, im, [[0, 0], [15, 15], [15, 15]], [[2, 2], [1, 1], [0, 0]])
    S.pad()
    return S


def wll_part(wt, tid, fname):
    im = Image.open(os.path.join(WLL, 'Graphics', 'Tilesets', fname + '.png')).convert('RGBA')
    im = im.crop((0, 0, 256, im.height // 32 * 32)); n = im.height // 32 * 8
    t = wt[tid]
    p = [int(x) for x in t.passages.data.reshape(-1)][384:384 + n]; q = [int(x) for x in t.priorities.data.reshape(-1)][384:384 + n]
    return im, p + [0] * (n - len(p)), q + [0] * (n - len(q))


def auto_recolour(src, dst):
    im = Image.open(src).convert('RGBA')
    recolour(im).save(dst)


def main():
    reg = json.load(open(REG))
    base = next(t for t in reg if t['id'] == 30)
    tect = Image.open(os.path.join(OUT, 'Graphics', 'Tilesets', base['tileset_name'] + '.png')).convert('RGBA')
    n0 = 384 + tect.height // 32 * 8
    pas, pri, tag = (list(v[:n0]) + [0] * (n0 - len(v)) for v in (base['passages'], base['priorities'], base['terrain_tags']))
    ims = [tect]; offs = {}
    wt = M.load_file(os.path.join(WLL, 'Data', 'Tilesets.rxdata'))
    for key, tid, fname in (('route2', 39, 'Route 2_new'), ('goldenleaf', 15, 'Goldenleaf Forrest')):
        im, p, q = wll_part(wt, tid, fname)
        offs[key] = {'offset': len(pas), 'tiles': len(p)}
        pas += p; pri += q; tag += [0] * len(p); ims.append(im)
    # Bleed recolour of the Tectonic part; ground rows (grass, dry grass, dirt-in-grass) go ashen instead of glassy
    ground_rows = [((a - 384) // 8, (b - 384) // 8) for a, b in ((2080, 2128), (2184, 2304), (2504, 2560), (936, 968))]
    bl = recolour(tect, ground_rows)
    offs['bleed'] = {'offset': len(pas), 'tiles': n0 - 384}
    pas += pas[384:n0]; pri += pri[384:n0]; tag += tag[384:n0]; ims.append(bl)
    S = draw_custom(); cu = S.image()
    offs['custom'] = {'offset': len(pas), 'tiles': len(S.tiles), 'names': {k: len(pas) + v for k, v in S.names.items()}}
    for t in S.tiles:
        pas.append(t[1] if t else 0); pri.append(t[2] if t else 0); tag.append(t[3] if t else 0)
    ims.append(cu)
    sheet = Image.new('RGBA', (256, sum(i.height for i in ims)), (0, 0, 0, 0)); y = 0
    for i in ims:
        sheet.paste(i, (0, y)); y += i.height
    sheet.save(os.path.join(OUT, 'Graphics', 'Tilesets', 'Prismfall Wilds.png'))
    adir = os.path.join(OUT, 'Graphics', 'Autotiles')
    auto_recolour(os.path.join(TAUTO, 'water2.png'), os.path.join(adir, 'Bleed water.png'))
    auto_recolour(os.path.join(TAUTO, 'Tall Grass.png'), os.path.join(adir, 'Bleed grass.png'))
    names = list(base['autotile_names']); names[2] = 'Bleed water'; names[6] = 'Bleed grass'
    for i in range(48):                                   # slot 3 = water (blocked, Water tag); slot 7 = tall grass
        pas[144 + i], pri[144 + i], tag[144 + i] = pas[288 + i], pri[288 + i], tag[288 + i]
        pas[336 + i], pri[336 + i], tag[336 + i] = pas[96 + i], pri[96 + i], tag[96 + i]
    e = dict(base); e.update(id=40, name='Prismfall Wilds', tileset_name='Prismfall Wilds', n_tiles=len(pas), passages=pas,
                             priorities=pri, terrain_tags=tag, autotile_names=names)
    reg = json.load(open(REG))
    reg = [t for t in reg if t['id'] != 40] + [e]
    json.dump(sorted(reg, key=lambda t: t['id']), open(REG, 'w'))
    json.dump(offs, open(os.path.join(HERE, 'data', 'compose_wilds_offsets.json'), 'w'), indent=1)
    print('tileset 40: %d tiles, sheet %dx%d' % (len(pas) - 384, sheet.width, sheet.height))
    print({k: v['offset'] for k, v in offs.items()}); print(offs['custom']['names'])


if __name__ == '__main__':
    main()
