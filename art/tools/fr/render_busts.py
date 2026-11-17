import sys
import numpy as np
from PIL import Image, ImageDraw
import busts
from exprs import apply, EXPRS
from models import MODELS
BACK = dict(neutral=(226, 226, 232), happy=(255, 236, 170), smug=(214, 196, 236), angry=(244, 150, 130), crying=(160, 200, 240),
            shocked=(250, 250, 250), deadpan=(170, 176, 186), panic=(150, 150, 200), sad=(150, 170, 200), blush=(255, 205, 215))
BASES = {'pca': busts.base_pca, 'pcb': busts.base_pcb, 'larch': busts.base_larch}


def build(cid, expr):
    m = MODELS[cid]
    return apply(BASES[m['base']](), m, expr)


def disc(a, expr, S=2):
    im = Image.fromarray(a.astype(np.uint8))
    bg = Image.new('RGBA', im.size, BACK[expr] + (255,)); bg.alpha_composite(im)
    big = bg.resize((96 * S, 96 * S), Image.NEAREST)
    m = Image.new('L', big.size, 0); ImageDraw.Draw(m).ellipse((0, 0, big.width - 1, big.height - 1), fill=255)
    o = Image.new('RGBA', big.size, (60, 64, 76, 255)); o.paste(big, (0, 0), m)
    return o


if __name__ == '__main__':
    out = sys.argv[1]; ids = sys.argv[2].split(','); ex = sys.argv[3].split(',') if len(sys.argv) > 3 else EXPRS
    S = 2
    sh = Image.new('RGBA', (len(ex) * (96 * S + 4), len(ids) * (96 * S + 4)), (60, 64, 76, 255))
    for j, cid in enumerate(ids):
        for i, e in enumerate(ex):
            sh.alpha_composite(disc(build(cid, e), e, S), (i * (96 * S + 4), j * (96 * S + 4)))
    sh.save(out)
