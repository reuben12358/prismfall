#!/usr/bin/env python3
"""PIL map preview renderer (emulates Essentials' tile + autotile drawing).
usage: python3 -I render.py <MapNNN.rxdata> <out.png> [--grid] [--scale 0.5] [--crop x,y,w,h]"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rmarshal as M
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
GFX = os.environ.get('PRISMFALL_GFX', '/home/claude/ref/ebdx/Graphics')
_TS = None

AUTOTILE_PATTERNS = [
    [[27, 28, 33, 34], [5, 28, 33, 34], [27, 6, 33, 34], [5, 6, 33, 34],
     [27, 28, 33, 12], [5, 28, 33, 12], [27, 6, 33, 12], [5, 6, 33, 12]],
    [[27, 28, 11, 34], [5, 28, 11, 34], [27, 6, 11, 34], [5, 6, 11, 34],
     [27, 28, 11, 12], [5, 28, 11, 12], [27, 6, 11, 12], [5, 6, 11, 12]],
    [[25, 26, 31, 32], [25, 6, 31, 32], [25, 26, 31, 12], [25, 6, 31, 12],
     [15, 16, 21, 22], [15, 16, 21, 12], [15, 16, 11, 22], [15, 16, 11, 12]],
    [[29, 30, 35, 36], [29, 30, 11, 36], [5, 30, 35, 36], [5, 30, 11, 36],
     [39, 40, 45, 46], [5, 40, 45, 46], [39, 6, 45, 46], [5, 6, 45, 46]],
    [[25, 30, 31, 36], [15, 16, 45, 46], [13, 14, 19, 20], [13, 14, 19, 12],
     [17, 18, 23, 24], [17, 18, 11, 24], [41, 42, 47, 48], [5, 42, 47, 48]],
    [[37, 38, 43, 44], [37, 6, 43, 44], [13, 18, 19, 24], [13, 14, 43, 44],
     [37, 42, 43, 48], [17, 18, 47, 48], [13, 18, 43, 48], [1, 2, 7, 8]]]


OUT_GFX = os.path.join(os.path.dirname(HERE), 'maps_out', 'Graphics')


def tilesets():
    """Base-project tilesets (data/tilesets.json) + tilesets registered by import_tileset.py."""
    global _TS
    if _TS is None:
        _TS = {t['id']: t for t in json.load(open(os.path.join(HERE, 'data', 'tilesets.json')))}
        reg = os.path.join(os.path.dirname(HERE), 'maps_out', 'tilesets_prismfall.json')
        if os.path.exists(reg):
            _TS.update({t['id']: t for t in json.load(open(reg))})
    return _TS


def gfx(sub, name):
    """Imported graphics (maps_out/Graphics) win over the base project's."""
    for root in (OUT_GFX, GFX):
        p = os.path.join(root, sub, name + '.png')
        if os.path.exists(p):
            return p
    return None


class TileCache:
    def __init__(self, ts):
        self.ts = ts
        p = gfx('Tilesets', ts['tileset_name']) if ts['tileset_name'] else None
        self.sheet = Image.open(p).convert('RGBA') if p else None
        self.autos = []
        for n in ts['autotile_names']:
            p = gfx('Autotiles', n) if n else None
            self.autos.append(Image.open(p).convert('RGBA') if p else None)
        self.cache = {}

    def tile(self, tid):
        if tid in self.cache:
            return self.cache[tid]
        im = None
        if tid >= 384:
            if self.sheet is not None:
                i = tid - 384
                x, y = (i % 8) * 32, (i // 8) * 32
                if y + 32 <= self.sheet.height:
                    im = self.sheet.crop((x, y, x + 32, y + 32))
        elif tid >= 48:
            a = self.autos[tid // 48 - 1] if tid // 48 - 1 < len(self.autos) else None
            if a is not None:
                if a.height == 32:
                    im = a.crop((0, 0, 32, 32))
                else:
                    pat = AUTOTILE_PATTERNS[(tid % 48) >> 3][(tid % 48) & 7]
                    im = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
                    for i, q in enumerate(pat):
                        q -= 1
                        sx, sy = (q % 6) * 16, (q // 6) * 16
                        im.paste(a.crop((sx, sy, sx + 16, sy + 16)), ((i % 2) * 16, (i // 2) * 16))
        self.cache[tid] = im
        return im


_CHARS = {}


def charframe(name, hue, direction, pattern):
    key = (name, direction, pattern)
    if key in _CHARS:
        return _CHARS[key]
    p = os.path.join(GFX, 'Characters', name + '.png')
    im = None
    if os.path.exists(p):
        sh = Image.open(p).convert('RGBA')
        fw, fh = sh.width // 4, sh.height // 4
        row = max(0, min(3, direction // 2 - 1))
        im = sh.crop((pattern * fw, row * fh, pattern * fw + fw, row * fh + fh))
    _CHARS[key] = im
    return im


def initial_page(ev):
    """Page active at game start: last page whose conditions hold with all switches OFF and variables 0."""
    for pg in reversed(ev.pages):
        c = pg.condition
        if c.switch1_valid or c.switch2_valid or c.self_switch_valid:
            continue
        if c.variable_valid and c.variable_value > 0:
            continue
        return pg
    return None


def render(m, events=True, grid=False, ts=None):
    ts = ts or tilesets()[m.tileset_id]
    tc = TileCache(ts)
    W, H = m.width, m.height
    data = m.data.data  # (z, y, x)
    pri = ts['priorities']
    img = Image.new('RGBA', (W * 32, H * 32), (0, 0, 0, 255))
    high = []
    for z in range(3):
        for y in range(H):
            for x in range(W):
                tid = int(data[z, y, x])
                if tid <= 0:
                    continue
                t = tc.tile(tid)
                if t is None:
                    continue
                if tid < len(pri) and pri[tid] > 0:
                    high.append((x, y, z, t))
                img.alpha_composite(t, (x * 32, y * 32))
    if events:
        d = ImageDraw.Draw(img)
        for ev in sorted(m.events.values(), key=lambda e: e.y):
            pg = initial_page(ev)
            if pg is None:
                continue
            g = pg.graphic
            drawn = False
            if g.tile_id and g.tile_id >= 384:
                t = tc.tile(g.tile_id)
                if t is not None:
                    img.alpha_composite(t, (ev.x * 32, ev.y * 32)); drawn = True
            elif g.character_name:
                f = charframe(g.character_name, g.character_hue, g.direction, g.pattern)
                if f is not None:
                    px = ev.x * 32 + 16 - f.width // 2
                    py = ev.y * 32 + 32 - f.height
                    img.alpha_composite(f, (max(0, px), max(0, py))); drawn = True
            if not drawn:
                d.rectangle([ev.x * 32 + 3, ev.y * 32 + 3, ev.x * 32 + 28, ev.y * 32 + 28], outline=(255, 0, 255, 255), width=2)
        for x, y, z, t in high:  # priority tiles over characters
            img.alpha_composite(t, (x * 32, y * 32))
    if grid:
        d = ImageDraw.Draw(img)
        for x in range(0, W):
            c = (255, 255, 0, 110) if x % 5 == 0 else (255, 255, 255, 35)
            d.line([(x * 32, 0), (x * 32, H * 32)], fill=c)
        for y in range(0, H):
            c = (255, 255, 0, 110) if y % 5 == 0 else (255, 255, 255, 35)
            d.line([(0, y * 32), (W * 32, y * 32)], fill=c)
        for x in range(0, W, 5):
            for y in range(0, H, 5):
                d.text((x * 32 + 2, y * 32 + 1), '%d,%d' % (x, y), fill=(255, 255, 0, 255))
    return img


def mood(img, tone=None, fog=None):
    """Approximate the in-game look: RMXP screen tone (r, g, b added, gray desaturates) and a fog picture tiled over
    the map at its opacity / blend (0 normal, 1 add, 2 subtract). Fog files: maps_out/Graphics/Fogs, then GFX/Fogs."""
    import numpy as np
    a = np.asarray(img.convert('RGB')).astype(np.float32)
    if fog:
        fp = next((p for p in (os.path.join(OUT_GFX, 'Fogs', fog['name'] + '.png'), os.path.join(GFX, 'Fogs', fog['name'] + '.png'))
                   if os.path.exists(p)), None)
        if fp:
            f = Image.open(fp).convert('RGBA'); z = fog.get('zoom', 100) / 100.0
            if z != 1: f = f.resize((max(1, int(f.width * z)), max(1, int(f.height * z))))
            tile = Image.new('RGBA', img.size)
            for y in range(0, img.height, f.height):
                for x in range(0, img.width, f.width):
                    tile.paste(f, (x, y))
            t = np.asarray(tile).astype(np.float32); al = t[..., 3:4] / 255.0 * fog.get('opacity', 60) / 255.0
            b = fog.get('blend', 0)
            if b == 1: a = a + t[..., :3] * al
            elif b == 2: a = a - t[..., :3] * al
            else: a = a * (1 - al) + t[..., :3] * al
    if tone:
        r, g, b_, gray = (list(tone) + [0, 0, 0, 0])[:4]
        if gray:
            l = a.mean(axis=2, keepdims=True); a = a + (l - a) * (gray / 255.0)
        a = a + np.array([r, g, b_], dtype=np.float32)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def main():
    a = sys.argv[1:]
    m = M.load_file(a[0])
    img = render(m, grid='--grid' in a)
    if '--crop' in a:
        x, y, w, h = map(int, a[a.index('--crop') + 1].split(','))
        img = img.crop((x * 32, y * 32, (x + w) * 32, (y + h) * 32))
    if '--scale' in a:
        s = float(a[a.index('--scale') + 1])
        img = img.resize((int(img.width * s), int(img.height * s)), Image.LANCZOS)
    img.convert('RGB').save(a[1])
    print('wrote', a[1], img.size)


if __name__ == '__main__':
    main()
