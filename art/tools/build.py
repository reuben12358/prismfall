"""build.py - regenerate every Prismfall character file.

    python3 build.py              # everything
    python3 build.py LARCH JUNO   # only these ids

Writes art/out/Graphics/{Trainers,Characters,Portraits}/.  Files listed in
art/tools/locked.txt (hand-edited) are never overwritten.
"""
import os
import sys
from PIL import Image
import cast
from portrait import Bust
from trainer import Fig
from overworld import OW

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'out', 'Graphics'))
LOCKED = set()
_lp = os.path.join(os.path.dirname(__file__), 'locked.txt')
if os.path.exists(_lp):
    LOCKED = {l.strip() for l in open(_lp) if l.strip() and not l.startswith('#')}


def save(img, rel, scale=2):
    path = os.path.join(ROOT, rel)
    if rel in LOCKED:
        return None
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.resize((img.width * scale, img.height * scale), Image.NEAREST).save(path)
    return path


def build(cid):
    e = cast.CAST[cid]
    out = []
    names = e.get('tt') or [cid]
    if 'T' in e:
        im = Fig(e['T']).build()
        for tt in names:
            out.append(save(im, f'Trainers/{tt}.png'))
    if 'O' in e:
        sh = OW(e['O']).sheet()
        for tt in names:
            out.append(save(sh, f'Characters/trainer_{tt}.png'))
        out.append(save(sh, f'Characters/{cid}.png'))     # plain NPC charset name for events
    if 'P' in e:
        for x in e['exprs']:
            im = Bust(e['P']).build(x)
            out.append(save(im, f'Portraits/{cid}_{x}.png'))
            if x == 'neutral':
                out.append(save(im, f'Portraits/{cid}.png'))
    return [o for o in out if o]


if __name__ == '__main__':
    ids = sys.argv[1:] or list(cast.CAST)
    n = 0
    for cid in ids:
        n += len(build(cid))
    print(f'wrote {n} files for {len(ids)} characters -> {ROOT}')
