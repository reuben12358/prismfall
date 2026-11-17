"""preview.py - side-by-side with references at 1x and 2x on the same backgrounds.
python3 -I tools/kitbash/preview.py OUT.png sprite.png [sprite2.png ...] -- refspec ...
sprites are native 80px; refs are show.py specs."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, show
from PIL import Image, ImageDraw

BGS = [(152, 160, 172, 255), (96, 136, 96, 255), (236, 232, 220, 255)]


def row(ims, k, bg, pad=6):
    w = sum(i.size[0] * k + pad for i in ims) + pad
    h = max(i.size[1] for i in ims) * k + 2 * pad
    out = Image.new('RGBA', (w, h), bg)
    x = pad
    for im in ims:
        z = kb.up(im, k)
        out.alpha_composite(z, (x, h - pad - z.size[1]))
        x += z.size[0] + pad
    return out


def main():
    args = sys.argv[2:]
    if '--' in args:
        i = args.index('--'); sp, rp = args[:i], args[i + 1:]
    else:
        sp, rp = args, []
    ims = [Image.open(p).convert('RGBA') for p in sp]
    for r in rp:
        n, f = show.get_native(r)
        ims.append(n)
    rows = []
    for bg in BGS[:2]:
        rows.append(row(ims, 1, bg))
    rows.append(row(ims, 2, BGS[0]))
    rows.append(row(ims, 3, BGS[2]))
    W = max(r.size[0] for r in rows); Hh = sum(r.size[1] for r in rows)
    out = Image.new('RGBA', (W, Hh), (40, 42, 50, 255)); y = 0
    for r in rows:
        out.alpha_composite(r, (0, y)); y += r.size[1]
    out.save(sys.argv[1]); print(sys.argv[1], out.size)


if __name__ == '__main__':
    main()
