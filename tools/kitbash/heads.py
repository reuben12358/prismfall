"""heads.py - crop the top H rows of each donor's figure (its head) at native density, x K, for head-swap picking.
python3 -I tools/kitbash/heads.py OUT.png K H COLS spec [spec ...]   (spec as in show.py; append '!' to flip)"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, show
from PIL import Image


def main(out, k, hh, cols, specs):
    items = []
    for sp in specs:
        flip = sp.endswith('!')
        n, f = show.get_native(sp.rstrip('!'))
        bb = kb.bbox(n)
        c = n.crop((bb[0], bb[1], bb[2], min(bb[3], bb[1] + hh)))
        if flip:
            c = c.transpose(Image.FLIP_LEFT_RIGHT)
        items.append((sp.replace('sd:', ''), c))
    mw = max(i.size[0] for _, i in items)
    sh = kb.contact(items, cols, (min(mw, 60) * k + 8, hh * k + 6), k=k, fs=11, label_h=14)
    sh.save(out); print(out, sh.size)


if __name__ == '__main__':
    a = sys.argv
    main(a[1], int(a[2]), int(a[3]), int(a[4]), a[5:])
