"""Preview sheet: every expression for the given ids, disc-masked at 4x."""
import sys
from PIL import Image, ImageDraw
from portrait import Bust, EXPRESSIONS
import cast
BACK = dict(neutral=(226, 226, 232), happy=(255, 236, 170), smug=(214, 196, 236), angry=(244, 150, 130), crying=(160, 200, 240),
            shocked=(250, 250, 250), deadpan=(170, 176, 186), panic=(150, 150, 200), sad=(150, 170, 200), blush=(255, 205, 215))
def disc(im, expr, S=4):
    n = im.width
    bg = Image.new('RGBA', (n, n), BACK[expr] + (255,))
    bg.alpha_composite(im)
    big = bg.resize((n * S, n * S), Image.NEAREST)
    m = Image.new('L', big.size, 0); ImageDraw.Draw(m).ellipse((0, 0, big.width - 1, big.height - 1), fill=255)
    out = Image.new('RGBA', big.size, (60, 64, 76, 255)); out.paste(big, (0, 0), m)
    return out
def sheet(ids, path, S=4, exprs=None):
    rows = []
    for cid in ids:
        ex = exprs or cast.CAST[cid]['exprs']
        rows.append([disc(Bust(cast.CAST[cid]['P']).build(e), e, S) for e in ex])
    cw = 48 * S + 4
    W = max(len(r) for r in rows) * cw; H = len(rows) * cw
    sh = Image.new('RGBA', (W, H), (60, 64, 76, 255))
    for j, r in enumerate(rows):
        for i, im in enumerate(r):
            sh.alpha_composite(im, (i * cw, j * cw))
    sh.save(path)
if __name__ == '__main__':
    sheet(sys.argv[2].split(','), sys.argv[1], int(sys.argv[3]) if len(sys.argv) > 3 else 4, sys.argv[4].split(',') if len(sys.argv) > 4 else None)
