"""show.py - quick zoomed look at donors.
python3 -I tools/kitbash/show.py OUT.png K COLS spec [spec ...]
spec = set:id  (rejuv:012, reborn:129, deso:009, sd:backpackerf, file:/abs/path.png)
Each donor is shown at native density x K (hi-res donors are flagged, not scaled).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb
from PIL import Image

PATHS = {
    'rejuv': '/home/claude/ref/games/rejuvenation/Graphics/Characters/trainer%s.png',
    'reborn': '/home/claude/ref/games/reborn/Graphics/Characters/trainer%s.png',
    'deso': '/home/claude/ref/games/desolation/Graphics/Characters/trainer%s.png',
    'sd': '/home/claude/ref/art/sprites_showdown/trainers/%s.png',
    'wll': '/home/claude/ref/art/wll/Changed Files/Graphics/Characters/trainer%s.png',
    'rjface': '/home/claude/ref/games/rejuvenation/Graphics/Faces/%s.png',
    'dsface': '/home/claude/ref/games/desolation/Graphics/Faces/%s.png',
}


def resolve(spec):
    s, i = spec.split(':', 1)
    if s == 'file':
        return i
    return PATHS[s] % i


def get_native(spec):
    im = kb.load(resolve(spec))
    nat, f = kb.native(im)
    return nat, f


def main():
    out, k, cols = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    items = []
    mw = mh = 0
    for spec in sys.argv[4:]:
        nat, f = get_native(spec)
        bb = kb.bbox(nat)
        nat = nat.crop(bb)
        lab = '%s x%d %dx%d' % (spec, f, nat.size[0], nat.size[1])
        items.append((lab, nat))
        mw, mh = max(mw, nat.size[0]), max(mh, nat.size[1])
    sh = kb.contact(items, cols, (mw * k + 8, mh * k + 6), k=k, fs=10, label_h=14)
    sh.save(out)
    print(out, sh.size)


if __name__ == '__main__':
    main()
