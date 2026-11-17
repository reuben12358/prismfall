"""Contact sheet of reference sprites (read-only inputs). Usage:
python3 -I contact.py OUT.png SCALE COLS FILE...
Each file is shown at native resolution (halved if stored doubled) * SCALE, labelled with its basename."""
import sys, os
from PIL import Image, ImageDraw
import numpy as np


def native(im):
    im = im.convert('RGBA')
    a = np.array(im)
    h, w = a.shape[:2]
    if h % 2 == 0 and w % 2 == 0:
        if (a[0::2, 0::2] == a[1::2, 1::2]).all() and (a[0::2, 0::2] == a[0::2, 1::2]).all() and (a[0::2, 0::2] == a[1::2, 0::2]).all():
            return Image.fromarray(a[0::2, 0::2]), 2
    return im, 1


def main():
    out, scale, cols = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    files = sys.argv[4:]
    tiles = []
    for f in files:
        try:
            im, d = native(Image.open(f))
        except Exception as e:
            continue
        im = im.resize((im.width * scale, im.height * scale), Image.NEAREST)
        tiles.append((os.path.basename(f) + ('' if d == 1 else ' x2'), im))
    cw = max(t[1].width for t in tiles) + 4
    ch = max(t[1].height for t in tiles) + 14
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new('RGBA', (cw * cols, ch * rows), (120, 136, 144, 255))
    d = ImageDraw.Draw(sheet)
    for i, (name, im) in enumerate(tiles):
        x, y = (i % cols) * cw, (i // cols) * ch
        sheet.alpha_composite(im, (x + 2, y + 12))
        d.text((x + 2, y), name[:22], fill=(255, 255, 255, 255))
    sheet.save(out)


if __name__ == '__main__':
    main()
