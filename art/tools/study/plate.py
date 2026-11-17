"""Annotated study plate: each cell = image (native, scaled) + a wrapped caption.
python3 -I plate.py OUT.png TITLE SCALE CELLW  file1::caption1  file2::caption2 ...
A file may be suffixed with @x0,y0,x1,y1 to crop (in native pixels) and %S to override the scale for that cell."""
import sys, os, textwrap
from PIL import Image, ImageDraw
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pack import native


def load(spec, scale):
    crop = None
    if '%' in spec:
        spec, s = spec.rsplit('%', 1); scale = float(s)
    if '@' in spec:
        spec, c = spec.rsplit('@', 1); crop = tuple(int(v) for v in c.split(','))
    im = native(Image.open(spec).convert('RGBA'))
    if crop:
        im = im.crop(crop)
    a = np.array(im)
    ys, xs = np.where(a[..., 3] > 8)
    if len(xs) and not crop:
        im = im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    if scale != 1:
        im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.NEAREST)
    return im


def main():
    out, title, scale, cellw = sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4])
    cells = []
    for arg in sys.argv[5:]:
        f, cap = arg.split('::', 1)
        cells.append((load(f, scale), cap))
    maxw = 1800
    cols = max(1, maxw // cellw)
    rows = [cells[i:i + cols] for i in range(0, len(cells), cols)]
    chars = max(10, cellw // 6 - 1)
    heights = []
    for r in rows:
        ih = max(im.height for im, _ in r)
        th = max(len(textwrap.wrap(c, chars)) for _, c in r) * 11 + 6
        heights.append((ih, th))
    H = 22 + sum(ih + th + 14 for ih, th in heights)
    W = min(maxw, cols * cellw) + 8
    S = Image.new('RGBA', (W, H), (120, 132, 140, 255))
    d = ImageDraw.Draw(S)
    d.rectangle([0, 0, W, 18], fill=(30, 32, 40, 255))
    d.text((6, 4), title, fill=(255, 255, 255, 255))
    y = 24
    for r, (ih, th) in zip(rows, heights):
        x = 4
        for im, cap in r:
            S.alpha_composite(im, (x + (cellw - 8 - im.width) // 2 if im.width < cellw - 8 else x, y + ih - im.height))
            ty = y + ih + 4
            d.rectangle([x, ty - 1, x + cellw - 8, ty + th - 4], fill=(36, 38, 46, 255))
            for i, line in enumerate(textwrap.wrap(cap, chars)):
                d.text((x + 3, ty + 1 + i * 11), line, fill=(235, 235, 235, 255))
            x += cellw
        y += ih + th + 14
    S.save(out)
    print(out, S.size)


if __name__ == '__main__':
    main()
