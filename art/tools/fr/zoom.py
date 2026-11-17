"""zoom.py OUT S IMG [IMG...] - native-res view with a pixel grid and
coordinate ticks every 4 px, for planning pixel edits."""
import sys
from PIL import Image, ImageDraw
import numpy as np
def native(p):
    im = Image.open(p).convert('RGBA')
    a = np.array(im)
    if im.width % 2 == 0 and im.height % 2 == 0 and (a[0::2, 0::2] == a[1::2, 1::2]).all() and (a[0::2, 0::2] == a[0::2, 1::2]).all():
        im = im.resize((im.width // 2, im.height // 2), Image.NEAREST)
    return im
def zoom(im, S, crop=None, grid=True):
    if crop: im = im.crop(crop)
    ox, oy = (crop[0], crop[1]) if crop else (0, 0)
    W, H = im.width * S + 24, im.height * S + 24
    out = Image.new('RGBA', (W, H), (150, 165, 175, 255))
    big = im.resize((im.width * S, im.height * S), Image.NEAREST)
    out.alpha_composite(big, (24, 24))
    d = ImageDraw.Draw(out)
    if grid:
        for x in range(im.width + 1):
            d.line([(24 + x * S, 24), (24 + x * S, H)], fill=(0, 0, 0, 40 if (x + ox) % 4 else 110))
        for y in range(im.height + 1):
            d.line([(24, 24 + y * S), (W, 24 + y * S)], fill=(0, 0, 0, 40 if (y + oy) % 4 else 110))
        for x in range(0, im.width, 4):
            d.text((24 + x * S + 1, 2), str(x + ox), fill=(0, 0, 0, 255))
        for y in range(0, im.height, 4):
            d.text((1, 24 + y * S + 1), str(y + oy), fill=(0, 0, 0, 255))
    return out
if __name__ == '__main__':
    out, S = sys.argv[1], int(sys.argv[2])
    crop = None
    args = sys.argv[3:]
    if args[0].startswith('crop='):
        crop = tuple(int(v) for v in args[0][5:].split(',')); args = args[1:]
    ims = [zoom(native(p), S, crop) for p in args]
    W = sum(i.width for i in ims) + 6 * len(ims); H = max(i.height for i in ims)
    sh = Image.new('RGBA', (W, H), (90, 90, 100, 255)); x = 0
    for i in ims: sh.alpha_composite(i, (x, 0)); x += i.width + 6
    sh.save(out)
