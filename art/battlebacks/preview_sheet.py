"""Offline preview: default-camera crop of each HD room (with its static layers composited)."""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bblib import *
from PIL import ImageDraw

D = OUT


def compose(name):
    hd = Image.open(os.path.join(D, "battlebg", name + "_hd.png")).convert("RGBA")
    return hd


def main(out, names, cols=4, scale=0.5, full=False):
    tiles = []
    for n in names:
        hd = compose(n)
        if full:
            im = hd
        else:
            im = hd.crop((int(VIEW[0]), int(VIEW[1]), int(VIEW[0]) + 512, int(VIEW[1]) + 384))
        im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS if scale < 1 else Image.NEAREST)
        tiles.append((n, im))
    cw = max(t.width for _, t in tiles); ch = max(t.height for _, t in tiles) + 14
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cw, rows * ch), (24, 24, 24))
    d = ImageDraw.Draw(sheet)
    for i, (n, t) in enumerate(tiles):
        x, y = (i % cols) * cw, (i // cols) * ch
        sheet.paste(t.convert("RGB"), (x, y + 14)); d.text((x + 3, y + 1), n, fill=(255, 255, 0))
    sheet.save(out)
    print(out, sheet.size)


if __name__ == "__main__":
    out = sys.argv[1]
    names = sys.argv[2:] or sorted(f[:-7] for f in os.listdir(os.path.join(D, "battlebg")) if f.endswith("_hd.png"))
    main(out, names)
