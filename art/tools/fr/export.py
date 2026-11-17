"""export.py - write the approved frankensprites to art/out/Graphics/."""
import os
import numpy as np
from PIL import Image
import sys as _sys, os as _os
_sys.path.insert(0, _os.path.join(_os.path.dirname(__file__), 'chars'))
import pc_a, pc_b, larch, ow_fr, batch2, ow3
import kestrel as k3, juno as j3, player_a as pa3
from render_busts import build
from exprs import EXPRS
OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'out', 'Graphics'))
LOCK = os.path.join(os.path.dirname(__file__), 'locked.txt')
LOCKED = {l.strip() for l in open(LOCK) if l.strip() and not l.startswith('#')} if os.path.exists(LOCK) else set()

CHARS = {
    'PLAYER_A': dict(front=pa3.build, ow=ow_fr.player_a),        # front v3; overworld still v2
    'PLAYER_B': dict(front=pc_b.build, ow=ow_fr.player_b),
    'LARCH': dict(front=larch.build, ow=ow_fr.larch),
}
# battle + overworld only (portraits on hold); several trainer types share one art file
SPRITES = {
    'KESTREL': dict(types=['RIVAL_KESTREL'], front=k3.build, ow=ow3.kestrel_ow),
    'JUNO': dict(types=['RIVAL_JUNO', 'LEADER_JUNO'], front=j3.build, ow=ow3.juno_ow),
}
BACKS = {'PLAYER_A_back': batch2.back_a, 'PLAYER_B_back': batch2.back_b}


def save(a, rel, scale):
    if rel in LOCKED:
        return 0
    p = os.path.join(OUT, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    im = Image.fromarray(a.astype(np.uint8))
    if scale != 1:
        im = im.resize((im.width * scale, im.height * scale), Image.NEAREST)
    im.save(p); return 1


if __name__ == '__main__':
    n = 0
    for cid, d in CHARS.items():
        n += save(d['front'](), f'Trainers/{cid}.png', 2)
        ow = d['ow']()
        n += save(ow, f'Characters/trainer_{cid}.png', 2)
        n += save(ow, f'Characters/{cid}.png', 2)
        for e in EXPRS:
            a = build(cid, e)
            n += save(a, f'Portraits/{cid}_{e}.png', 1)       # 96x96 native
            if e == 'neutral':
                n += save(a, f'Portraits/{cid}.png', 1)
    for cid, d in SPRITES.items():
        fr, ow = d['front'](), d['ow']()
        for tt in d['types']:
            n += save(fr, f'Trainers/{tt}.png', 2)
            n += save(ow, f'Characters/trainer_{tt}.png', 2)
        n += save(ow, f'Characters/{cid}.png', 2)
    for name, fn in BACKS.items():
        n += save(fn(), f'Trainers/{name}.png', 2)
    print('wrote', n, 'files to', OUT)
