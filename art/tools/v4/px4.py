"""px4: a small pixel-drawing toolkit for hand-made sprites.

Sprite file format (.spr, plain text):
    # comment
    [palette]
    a #000000  outline-dark          (char, hex, optional name; '.' is always transparent)
    [layer back]
    00|................................................................................
    01|......
    ...
Each layer holds H rows of exactly W chars, every row prefixed with its 2-digit row number and '|' so a single row can
be found and replaced by hand. Layers compose in file order; '.' is transparent.

CLI:
    python3 -I px4.py render SPR OUT.png [--refs A.png,B.png] [--label TEXT] [--head x0,y0,x1,y1]
    python3 -I px4.py lint SPR
    python3 -I px4.py grid SPR x0 y0 x1 y1 [layer]
    python3 -I px4.py png SPR OUT.png [--x2]
"""
import sys, os, re, colorsys
from collections import OrderedDict
from PIL import Image, ImageDraw
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from contact import native  # noqa: E402

W = H = 80
BG = (148, 160, 166, 255)       # neutral mid grey-teal, like a battle background average
BG2 = (88, 120, 96, 255)        # grassy darker backdrop, to catch halos


# ---------------------------------------------------------------- file io
def hex2rgba(h):
    h = h.lstrip('#')
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)


class Sprite:
    def __init__(self, w=W, h=H):
        self.w, self.h = w, h
        self.pal = OrderedDict()   # char -> (hex, name)
        self.layers = OrderedDict()  # name -> list of lists of chars

    # -- io
    @classmethod
    def load(cls, path):
        s = cls()
        sec, cur = None, None
        for raw in open(path):
            line = raw.rstrip('\n')
            if not line.strip() or line.lstrip().startswith('#') and not re.match(r'^\s*\S\s+#[0-9a-fA-F]{6}', line):
                continue
            m = re.match(r'^\[(\w+)(?:\s+(\S+))?\]', line)
            if m:
                sec = m.group(1)
                if sec == 'layer':
                    cur = m.group(2)
                    s.layers[cur] = [['.'] * s.w for _ in range(s.h)]
                elif sec == 'size':
                    pass
                continue
            if sec == 'palette':
                parts = line.split()
                s.pal[parts[0]] = (parts[1], ' '.join(parts[2:]))
            elif sec == 'layer':
                m = re.match(r'^(\d+)\|(.*)$', line)
                if not m:
                    raise ValueError('bad row: %r' % line)
                y, row = int(m.group(1)), m.group(2)
                if len(row) != s.w:
                    raise ValueError('row %d of layer %s has %d chars' % (y, cur, len(row)))
                s.layers[cur][y] = list(row)
        return s

    def save(self, path):
        out = ['[palette]']
        for c, (hx, name) in self.pal.items():
            out.append('%s %s  %s' % (c, hx, name))
        for name, g in self.layers.items():
            out.append('')
            out.append('[layer %s]' % name)
            for y in range(self.h):
                out.append('%02d|%s' % (y, ''.join(g[y])))
        open(path, 'w').write('\n'.join(out) + '\n')

    # -- compose
    def compose(self, only=None):
        g = [['.'] * self.w for _ in range(self.h)]
        for name, L in self.layers.items():
            if only and name not in only:
                continue
            for y in range(self.h):
                for x in range(self.w):
                    if L[y][x] != '.':
                        g[y][x] = L[y][x]
        return g

    def image(self, grid=None):
        grid = grid or self.compose()
        a = np.zeros((self.h, self.w, 4), np.uint8)
        for y in range(self.h):
            for x in range(self.w):
                c = grid[y][x]
                if c != '.':
                    if c not in self.pal:
                        raise KeyError('char %r at %d,%d not in palette' % (c, x, y))
                    a[y, x] = hex2rgba(self.pal[c][0])
        return Image.fromarray(a)


# ---------------------------------------------------------------- drawing primitives on a char grid
class Canvas:
    def __init__(self, w=W, h=H, grid=None):
        self.w, self.h = w, h
        self.g = grid if grid is not None else [['.'] * w for _ in range(h)]

    def px(self, x, y, c):
        x, y = int(round(x)), int(round(y))
        if 0 <= x < self.w and 0 <= y < self.h:
            self.g[y][x] = c

    def get(self, x, y):
        if 0 <= x < self.w and 0 <= y < self.h:
            return self.g[y][x]
        return '.'

    def line(self, x0, y0, x1, y1, c, width=1):
        x0, y0, x1, y1 = map(lambda v: int(round(v)), (x0, y0, x1, y1))
        dx, dy = abs(x1 - x0), -abs(y1 - y0)
        sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
        err = dx + dy
        while True:
            if width == 1:
                self.px(x0, y0, c)
            else:
                self.disc(x0, y0, width / 2.0, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy; x0 += sx
            if e2 <= dx:
                err += dx; y0 += sy

    def disc(self, cx, cy, r, c):
        for y in range(int(cy - r - 1), int(cy + r + 2)):
            for x in range(int(cx - r - 1), int(cx + r + 2)):
                if (x - cx) ** 2 + (y - cy) ** 2 <= r * r + 0.25:
                    self.px(x, y, c)

    def ellipse(self, cx, cy, rx, ry, c):
        for y in range(int(cy - ry - 1), int(cy + ry + 2)):
            for x in range(int(cx - rx - 1), int(cx + rx + 2)):
                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1.0:
                    self.px(x, y, c)

    def poly(self, pts, c):
        """Scanline fill of a polygon given in pixel-centre coordinates."""
        ys = [p[1] for p in pts]
        for y in range(int(min(ys)), int(max(ys)) + 1):
            xs = []
            n = len(pts)
            for i in range(n):
                (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % n]
                if y0 == y1:
                    continue
                if (y0 <= y < y1) or (y1 <= y < y0):
                    xs.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
            xs.sort()
            for i in range(0, len(xs) - 1, 2):
                for x in range(int(round(xs[i])), int(round(xs[i + 1])) + 1):
                    self.px(x, y, c)

    def limb(self, pts, widths, c):
        """A tapered limb: polyline with a width at each point, filled as a chain of quads + end discs."""
        for i in range(len(pts) - 1):
            (x0, y0), (x1, y1) = pts[i], pts[i + 1]
            w0, w1 = widths[i] / 2.0, widths[i + 1] / 2.0
            dx, dy = x1 - x0, y1 - y0
            L = max(1e-6, (dx * dx + dy * dy) ** 0.5)
            nx, ny = -dy / L, dx / L
            self.poly([(x0 + nx * w0, y0 + ny * w0), (x1 + nx * w1, y1 + ny * w1),
                       (x1 - nx * w1, y1 - ny * w1), (x0 - nx * w0, y0 - ny * w0)], c)
        for (x, y), w in zip(pts, widths):
            self.disc(x, y, w / 2.0 - 0.3, c)

    def replace_in(self, region_mask_fn, old, new):
        for y in range(self.h):
            for x in range(self.w):
                if self.g[y][x] == old and region_mask_fn(x, y):
                    self.g[y][x] = new


def outline(grid, colour_for, inner=False):
    """Add a 1-px outline around opaque pixels of `grid` (in place, returns grid).
    colour_for(x, y, neighbour_chars) -> char to place at transparent pixel (x,y) touching opaque ones (4-neighbourhood)."""
    h, w = len(grid), len(grid[0])
    add = []
    for y in range(h):
        for x in range(w):
            if grid[y][x] != '.':
                continue
            nb = []
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                xx, yy = x + dx, y + dy
                if 0 <= xx < w and 0 <= yy < h and grid[yy][xx] != '.':
                    nb.append((dx, dy, grid[yy][xx]))
            if nb:
                add.append((x, y, colour_for(x, y, nb)))
    for x, y, c in add:
        if c:
            grid[y][x] = c
    return grid


# ---------------------------------------------------------------- analysis
def lint(sp, allow_orphans=''):
    g = sp.compose()
    used = {}
    for y in range(sp.h):
        for x in range(sp.w):
            c = g[y][x]
            if c != '.':
                used[c] = used.get(c, 0) + 1
    orphans = []
    for y in range(sp.h):
        for x in range(sp.w):
            c = g[y][x]
            if c == '.' or c in allow_orphans:
                continue
            same = 0
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if (dx or dy) and 0 <= x + dx < sp.w and 0 <= y + dy < sp.h and g[y + dy][x + dx] == c:
                        same += 1
            if same == 0:
                orphans.append((x, y, c))
    # outline gaps: opaque pixel touching transparent that is not a dark colour
    lum = {c: (0.299 * hex2rgba(h)[0] + 0.587 * hex2rgba(h)[1] + 0.114 * hex2rgba(h)[2]) for c, (h, n) in sp.pal.items()}
    edge_light = []
    for y in range(sp.h):
        for x in range(sp.w):
            c = g[y][x]
            if c == '.':
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                xx, yy = x + dx, y + dy
                if not (0 <= xx < sp.w and 0 <= yy < sp.h) or g[yy][xx] == '.':
                    if lum[c] > 110:
                        edge_light.append((x, y, c))
                    break
    return used, orphans, edge_light


def print_lint(sp, allow=''):
    used, orphans, edge = lint(sp, allow)
    print('colours used: %d' % len(used))
    for c, (hx, name) in sp.pal.items():
        if c in used:
            print('  %s %s %-22s %4d' % (c, hx, name, used[c]))
    unused = [c for c in sp.pal if c not in used]
    if unused:
        print('  unused palette entries:', ''.join(unused))
    rare = [c for c in used if used[c] < 3]
    if rare:
        print('  colours used < 3 times:', ''.join(rare))
    print('orphans (%d):' % len(orphans), ' '.join('%s@%d,%d' % (c, x, y) for x, y, c in orphans))
    print('light pixels on the silhouette edge (%d):' % len(edge), ' '.join('%s@%d,%d' % (c, x, y) for x, y, c in edge[:60]))


def print_grid(sp, x0, y0, x1, y1, layer=None):
    g = sp.layers[layer] if layer else sp.compose()
    print('    ' + ''.join(str((x // 10) % 10) for x in range(x0, x1)))
    print('    ' + ''.join(str(x % 10) for x in range(x0, x1)))
    for y in range(y0, y1):
        print('%02d| %s' % (y, ''.join(g[y][x0:x1])))


# ---------------------------------------------------------------- rendering
def load_ref(path):
    im, d = native(Image.open(path))
    a = np.array(im)
    ys, xs = np.where(a[..., 3] > 0)
    return im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))


def crop_content(im):
    a = np.array(im)
    ys, xs = np.where(a[..., 3] > 0)
    return im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))


def sheet(sprite_im, refs, out, label='', head=None, extra=None):
    """1x row on two backgrounds, 4x row (sprite + refs, bottom-aligned), optional 8x head crop."""
    items = [('Juno v4', crop_content(sprite_im))] + [(os.path.basename(r).split('.')[0], load_ref(r)) for r in refs]
    if extra:
        items = [('Juno v4', crop_content(sprite_im))] + [(n, crop_content(e)) for n, e in extra] + items[1:]
    z = 4
    pad = 10
    hmax = max(im.height for _, im in items)
    w4 = sum(im.width * z + pad * 2 for _, im in items)
    w1 = sum(im.width + pad for _, im in items) * 2 + 40
    head_im = None
    if head:
        hx0, hy0, hx1, hy1 = head
        head_im = sprite_im.crop(head).resize(((hx1 - hx0) * 8, (hy1 - hy0) * 8), Image.NEAREST)
    W_ = max(w4, w1) + (head_im.width + 20 if head_im else 0)
    H_ = 16 + hmax + 12 + 16 + hmax * z + 20
    S = Image.new('RGBA', (W_, H_), (60, 64, 72, 255))
    d = ImageDraw.Draw(S)
    d.text((4, 2), (label + '  |  ' if label else '') + '1x on two backgrounds, then 4x (sprite first, references after)', fill=(255, 255, 255, 255))
    # 1x strip
    x = 4
    for bg in (BG, BG2):
        strip_w = sum(im.width + pad for _, im in items) + pad
        d.rectangle([x, 16, x + strip_w, 16 + hmax + 8], fill=bg)
        xx = x + pad
        for _, im in items:
            S.alpha_composite(im, (xx, 16 + 4 + hmax - im.height))
            xx += im.width + pad
        x += strip_w + 20
    # 4x strip
    y4 = 16 + hmax + 12 + 16
    d.rectangle([0, y4 - 14, w4 + 4, y4 + hmax * z + 8], fill=BG)
    xx = 4
    for name, im in items:
        big = im.resize((im.width * z, im.height * z), Image.NEAREST)
        S.alpha_composite(big, (xx + pad, y4 + hmax * z - big.height))
        d.text((xx + pad, y4 - 12), name, fill=(20, 20, 20, 255))
        xx += big.width + pad * 2
    if head_im:
        hx = max(w4, w1) + 10
        d.rectangle([hx - 4, 14, hx + head_im.width + 4, 18 + head_im.height + 4], fill=BG)
        S.alpha_composite(head_im, (hx, 18))
        d.text((hx, 2), '8x head', fill=(255, 255, 255, 255))
    S.save(out)
    return S


def main():
    cmd = sys.argv[1]
    if cmd == 'render':
        spr, out = sys.argv[2], sys.argv[3]
        refs, label, head = [], '', None
        args = sys.argv[4:]
        i = 0
        while i < len(args):
            if args[i] == '--refs':
                refs = args[i + 1].split(','); i += 2
            elif args[i] == '--label':
                label = args[i + 1]; i += 2
            elif args[i] == '--head':
                head = tuple(int(v) for v in args[i + 1].split(',')); i += 2
            else:
                i += 1
        sp = Sprite.load(spr)
        sheet(sp.image(), refs, out, label, head)
    elif cmd == 'lint':
        sp = Sprite.load(sys.argv[2])
        print_lint(sp, sys.argv[3] if len(sys.argv) > 3 else '')
    elif cmd == 'grid':
        sp = Sprite.load(sys.argv[2])
        x0, y0, x1, y1 = map(int, sys.argv[3:7])
        print_grid(sp, x0, y0, x1, y1, sys.argv[7] if len(sys.argv) > 7 else None)
    elif cmd == 'png':
        sp = Sprite.load(sys.argv[2])
        im = sp.image()
        if '--x2' in sys.argv:
            im = im.resize((im.width * 2, im.height * 2), Image.NEAREST)
        im.save(sys.argv[3])


if __name__ == '__main__':
    main()


# ---------------------------------------------------------------- hand patches
def apply_patch(sp, patch_path, layer='main'):
    """Patch file: blocks starting with '@ X Y' then rows of chars. '~' keeps the pixel, '.' clears it."""
    L = sp.layers[layer]
    x0 = y0 = None
    row = 0
    for raw in open(patch_path):
        line = raw.rstrip('\n')
        if not line.strip() or line.startswith('#'):
            continue
        if line.startswith('@'):
            _, x0, y0 = line.split()
            x0, y0, row = int(x0), int(y0), 0
            continue
        m = re.match(r'^\s*(\d+)\s*:(.*)$', line)
        if m:   # segment form  "Y: X chars | X chars"
            y = int(m.group(1))
            for seg in m.group(2).split('|'):
                seg = seg.strip()
                if not seg:
                    continue
                xs, chars = seg.split(None, 1)
                for i, ch in enumerate(chars.strip()):
                    if ch != '~' and 0 <= int(xs) + i < sp.w:
                        L[y][int(xs) + i] = ch
            continue
        s = line.strip()
        for i, ch in enumerate(s):
            if ch == '~':
                continue
            x, y = x0 + i, y0 + row
            if 0 <= x < sp.w and 0 <= y < sp.h:
                L[y][x] = ch
        row += 1


if __name__ == '__main__' and len(sys.argv) > 1 and sys.argv[1] == 'patch':
    sp = Sprite.load(sys.argv[2])
    for p in sys.argv[3:]:
        apply_patch(sp, p)
    sp.save(sys.argv[2])
