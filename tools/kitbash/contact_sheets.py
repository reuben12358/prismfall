"""contact_sheets.py - render donor contact sheets at native 1x (hi-res donors at 0.5x,
flagged with *), labelled with set:id so candidates can be picked and tagged.

python3 -I tools/kitbash/contact_sheets.py [set ...]
"""
import sys, os, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb
from PIL import Image

PER = 98
COLS = 14
CELL = (96, 100)


def short(d):
    b = os.path.basename(d['file'])[:-4]
    m = re.match(r'[Tt]rainer(.*)', b)
    return (m.group(1) if m else b)[:14]


def main():
    idx = json.load(open(kb.WORK + '/donor_index.json'))
    sets = sys.argv[1:] or ['rejuv', 'reborn', 'deso', 'showdown', 'wll', 'ebdx']
    for s in sets:
        sub = [d for d in idx if d['set'] == s]
        for p in range(0, len(sub), PER):
            items = []
            for d in sub[p:p + PER]:
                im = kb.load(d['file'])
                nat, f = kb.native(im)
                lab = short(d)
                if nat.size[0] > 130:  # hi-res donor: show half size, flag it
                    nat = nat.resize((nat.size[0] // 2, nat.size[1] // 2), Image.NEAREST)
                    lab += '*'
                bb = kb.bbox(nat)
                nat = nat.crop(bb)
                items.append((lab, nat))
            sh = kb.contact(items, COLS, CELL, fs=9)
            out = kb.WORK + '/sheets/idx_%s_%d.png' % (s, p // PER)
            sh.save(out)
            print(out, sh.size)


if __name__ == '__main__':
    main()
