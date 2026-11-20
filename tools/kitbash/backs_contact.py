"""backs_contact.py - contact sheet of trainer back sprites (first frame of each strip) from Reborn, Rejuvenation,
Desolation, the HGSS partner pack and the base project. python3 -I tools/kitbash/backs_contact.py OUT.png"""
import sys, os, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb
from PIL import Image

SRC = []
for g, tag in (('reborn', 'RB'), ('rejuvenation', 'RJ'), ('desolation', 'DS')):
    SRC += [(tag, f) for f in sorted(glob.glob('/home/claude/ref/games/%s/Graphics/Characters/trback*.png' % g))]
SRC += [('HG', f) for f in sorted(glob.glob('/home/claude/ref/art/sprites_gen4_partner_backs/extracted/*/*.png'))]
SRC += [('EB', f) for f in sorted(glob.glob('/home/claude/ref/ebdx/Graphics/Trainers/*back*.png'))]


def frames(path):
    im = kb.load(path)
    w, h = im.size
    n = 5 if w >= 4 * h else 1
    fw = w // n
    out = []
    for i in range(n):
        fr = im.crop((i * fw, 0, (i + 1) * fw, h))
        nat, f = kb.native(fr)
        if f == 1:
            # strips laid out at odd offsets: test the doubled-run heuristic
            pass
        out.append((nat, f))
    return out, n


def main(out):
    items = []
    for tag, f in SRC:
        try:
            frs, n = frames(f)
        except Exception as e:
            continue
        nat, fac = frs[0]
        bb = kb.bbox(nat)
        if not bb:
            continue
        lab = '%s %s x%d n%d' % (tag, os.path.basename(f)[:-4].replace('trback', 'tb').replace('POKEMONTRAINER_', ''), fac, n)
        items.append((lab, nat.crop(bb)))
    mw = max(i.size[0] for _, i in items); mh = max(i.size[1] for _, i in items)
    sh = kb.contact(items, 16, (min(mw, 130) + 6, min(mh, 130) + 4), k=1, fs=9, label_h=12)
    sh.save(out); print(out, sh.size, len(items))


if __name__ == '__main__':
    main(sys.argv[1])
