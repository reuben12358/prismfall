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


def tilesets():
    global _TS
    if _TS is None:
        _TS = {t['id']: t for t in json.load(open(os.path.join(HERE, 'data', 'tilesets.json')))}
    return _TS


class TileCache:
    def __init__(self, ts):
        self.ts = ts
        p = os.path.join(GFX, 'Tilesets', ts['tileset_name'] + '.png')
        self.sheet = Image.open(p).convert('RGBA') if ts['tileset_name'] and os.path.exists(p) else None
        self.autos = []
        for n in ts['autotile_names']:
            p = os.path.join(GFX, 'Autotiles', n + '.png') if n else None
            self.autos.append(Image.open(p).convert('RGBA') if p and os.path.exists(p) else None)
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
            pg = ev.pages[0]
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
