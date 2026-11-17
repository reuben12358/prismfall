"""Pack reference images into labelled contact pages for study (inputs are read-only data).
python3 -I pack.py OUTPREFIX MAXW MAXH SCALE [--native] [--bg r,g,b] FILE...
Each image is cropped to its opaque bbox; --native halves images stored at 2x. Pages are OUTPREFIX_00.png ..."""
import sys, os
from PIL import Image, ImageDraw
import numpy as np


def native(im):
    a = np.array(im)
    h, w = a.shape[:2]
    if h % 2 == 0 and w % 2 == 0:
        b = a[0::2, 0::2]
        if (b == a[1::2, 1::2]).all() and (b == a[0::2, 1::2]).all() and (b == a[1::2, 0::2]).all():
            return Image.fromarray(b)
    return im


def load(f, nat):
    im = Image.open(f)
    im = im.convert('RGBA')
    if nat:
        im = native(im)
    a = np.array(im)
    ys, xs = np.where(a[..., 3] > 8)
    if len(xs) == 0:
        return None
    return im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))


def main():
    args = sys.argv[1:]
    pre, maxw, maxh, scale = args[0], int(args[1]), int(args[2]), float(args[3])
    nat = '--native' in args
    bg = (128, 140, 148)
    files = []
    i = 4
    while i < len(args):
        if args[i] == '--native':
            i += 1; continue
        if args[i] == '--bg':
            bg = tuple(int(v) for v in args[i + 1].split(',')); i += 2; continue
        files.append(args[i]); i += 1
    tiles = []
    for f in files:
        try:
            im = load(f, nat)
        except Exception:
            continue
        if im is None:
            continue
        if scale != 1:
            im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.NEAREST)
        tiles.append((os.path.splitext(os.path.basename(f))[0], im))
    page, x, y, rowh = 0, 4, 4, 0
    placed = []
    pages = []
    for name, im in tiles:
        w, h = max(im.width, 6 * len(name[:14])) + 6, im.height + 14
        if x + w > maxw:
            x, y, rowh = 4, y + rowh, 0
        if y + h > maxh and placed:
            pages.append(placed); placed = []; x, y, rowh = 4, 4, 0
        placed.append((x, y, name, im))
        x += w; rowh = max(rowh, h)
    if placed:
        pages.append(placed)
    for p, pl in enumerate(pages):
        H = max(yy + im.height + 14 for xx, yy, n, im in pl) + 4
        S = Image.new('RGBA', (maxw, H), bg + (255,))
        d = ImageDraw.Draw(S)
        for xx, yy, n, im in pl:
            d.text((xx, yy), n[:14], fill=(255, 255, 255, 255))
            S.alpha_composite(im, (xx, yy + 12))
        S.save('%s_%02d.png' % (pre, p))
        print('%s_%02d.png' % (pre, p), len(pl), S.size)


if __name__ == '__main__':
    main()
