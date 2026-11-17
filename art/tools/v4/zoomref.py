"""Show reference sprites side by side at an integer zoom, cropped to their content, optional pixel grid.
python3 -I zoomref.py OUT.png ZOOM [grid] FILE[:x0,y0,x1,y1] ...   (crop box in native pixels)"""
import sys, os
from PIL import Image, ImageDraw
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from contact import native


def load(spec):
    crop = None
    if ':' in spec and ',' in spec.split(':')[-1]:
        spec, c = spec.rsplit(':', 1)
        crop = tuple(int(v) for v in c.split(','))
    im, d = native(Image.open(spec))
    a = np.array(im)
    if crop:
        im = im.crop(crop)
    else:
        ys, xs = np.where(a[..., 3] > 0)
        im = im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    return os.path.basename(spec), im


def main():
    out, z = sys.argv[1], int(sys.argv[2])
    args = sys.argv[3:]
    grid = False
    if args and args[0] == 'grid':
        grid, args = True, args[1:]
    tiles = [load(s) for s in args]
    W = sum(t[1].width * z + 8 for t in tiles)
    H = max(t[1].height * z for t in tiles) + 14
    sheet = Image.new('RGBA', (W, H), (126, 140, 150, 255))
    d = ImageDraw.Draw(sheet)
    x = 0
    for name, im in tiles:
        big = im.resize((im.width * z, im.height * z), Image.NEAREST)
        sheet.alpha_composite(big, (x, 14))
        if grid and z >= 6:
            for gx in range(im.width + 1):
                d.line([(x + gx * z, 14), (x + gx * z, 14 + im.height * z)], fill=(0, 0, 0, 40))
            for gy in range(im.height + 1):
                d.line([(x, 14 + gy * z), (x + im.width * z, 14 + gy * z)], fill=(0, 0, 0, 40))
        d.text((x, 1), name, fill=(255, 255, 255, 255))
        x += big.width + 8
    sheet.save(out)


if __name__ == '__main__':
    main()
