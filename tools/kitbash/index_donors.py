"""index_donors.py - build the donor index (density, size, colours, outline) and
contact sheets for every trainer front we have.

python3 -I tools/kitbash/index_donors.py
Writes art/work/kitbash/donor_index.json and art/work/kitbash/sheets/idx_<set>_<n>.png
"""
import sys, os, glob, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb
from PIL import Image

SETS = {
    'rejuv': '/home/claude/ref/games/rejuvenation/Graphics/Characters/trainer*.png',
    'reborn': '/home/claude/ref/games/reborn/Graphics/Characters/trainer*.png',
    'deso': '/home/claude/ref/games/desolation/Graphics/Characters/trainer*.png',
    'wll': '/home/claude/ref/art/wll/**/[Tt]rainer*.png',
    'showdown': '/home/claude/ref/art/sprites_showdown/trainers/*.png',
    'kyledove_xy': '/home/claude/ref/art/sprites_kyledove_xy/sprites/*.png',
    'kyledove_oras': '/home/claude/ref/art/sprites_kyledove_oras/sprites/*.png',
    'kyledove_swsh': '/home/claude/ref/art/sprites_kyledove_swsh/sprites/*.png',
    'muffyang': '/home/claude/ref/art/sprites_muffyang/extracted/**/*.png',
    'ebdx': '/home/claude/ref/ebdx_renovation/Graphics/Trainers/*.png',
}


def main():
    idx = []
    for s, pat in SETS.items():
        files = sorted(glob.glob(pat, recursive=True))
        for f in files:
            if s == 'showdown' and any(t in os.path.basename(f) for t in ('-gen1', '-gen2', '-gen3')):
                continue   # off-style (smaller density)
            try:
                im = kb.load(f)
            except Exception as e:
                continue
            w, h = im.size
            if w > 400 or h > 400:  # strips / sheets
                continue
            nat, fac = kb.native(im)
            bb = kb.bbox(nat)
            if not bb:
                continue
            cols = kb.colours(nat)
            oc = kb.outline_colours(nat)
            top = oc[0][0] if oc else None
            dark_edge = sum(n for c, n in oc if kb.lum(c) < 60) / max(1, sum(n for c, n in oc))
            idx.append(dict(set=s, file=f, size=[w, h], factor=fac, native=list(nat.size),
                            bbox=list(bb), fig_h=bb[3] - bb[1], fig_w=bb[2] - bb[0],
                            ncol=len(cols), outline_top=list(top) if top else None,
                            dark_edge=round(dark_edge, 2),
                            dratio=round(kb.doubled_ratio(im), 2) if fac == 1 else 1.0))
    json.dump(idx, open(kb.WORK + '/donor_index.json', 'w'), indent=0)
    # summary
    from collections import Counter
    for s in SETS:
        sub = [d for d in idx if d['set'] == s]
        print(s, len(sub), Counter((tuple(d['size']), d['factor']) for d in sub).most_common(6))
        hs = sorted(d['fig_h'] for d in sub)
        if hs:
            print('   fig_h native: min %d med %d max %d' % (hs[0], hs[len(hs) // 2], hs[-1]))


if __name__ == '__main__':
    main()
