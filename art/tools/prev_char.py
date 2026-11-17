"""One presentation sheet per group: battle sprite, overworld sheet and the
portrait row, at 4x, with two stock sprites for scale."""
import sys
from PIL import Image, ImageDraw
import cast
from portrait import Bust
from trainer import Fig
from overworld import OW
from prev_portraits import disc

REF_T = '/home/claude/ref/ebdx_renovation/Graphics/Trainers/'
REF_C = '/home/claude/ref/ebdx_renovation/Graphics/Characters/'
BG = (120, 140, 150, 255)


def row(cid, S=4, exprs=None):
    e = cast.CAST[cid]
    t = Fig(e['T']).build().resize((64 * S, 64 * S), Image.NEAREST)
    o = OW(e['O']).sheet().resize((64 * S // 2 * 2, 96 * S // 2 * 2), Image.NEAREST)
    o = o.resize((64 * S, 96 * S), Image.NEAREST)
    ps = [disc(Bust(e['P']).build(x), x, S // 2 + 1) for x in (exprs or e['exprs'])]
    pw = ps[0].width
    per = 5
    prow = (len(ps) + per - 1) // per
    W = t.width + o.width + 20 + per * (pw + 4)
    H = max(t.height, o.height, prow * (pw + 4))
    im = Image.new('RGBA', (W, H), BG)
    im.alpha_composite(t, (0, H - t.height))
    im.alpha_composite(o, (t.width + 10, 0))
    for i, p in enumerate(ps):
        im.alpha_composite(p, (t.width + o.width + 20 + (i % per) * (pw + 4), (i // per) * (pw + 4)))
    return im


def refs(S=4):
    a = Image.open(REF_T + 'RIVAL1.png').convert('RGBA').resize((64 * S, 64 * S), Image.NEAREST)
    b = Image.open(REF_T + 'LEADER_Misty.png').convert('RGBA').resize((64 * S, 64 * S), Image.NEAREST)
    c = Image.open(REF_C + 'trainer_RIVAL1.png').convert('RGBA').resize((64 * S, 96 * S), Image.NEAREST)
    im = Image.new('RGBA', (a.width * 2 + c.width + 20, c.height), BG)
    im.alpha_composite(a, (0, c.height - a.height)); im.alpha_composite(b, (a.width, c.height - b.height)); im.alpha_composite(c, (a.width * 2 + 20, 0))
    d = ImageDraw.Draw(im); d.text((6, 6), 'STOCK REFERENCE (Gen 4/5 fronts + charset)', fill=(20, 20, 30, 255))
    return im


def sheet(ids, path, S=4):
    rows = [refs(S)] + [row(c, S) for c in ids]
    W = max(r.width for r in rows); H = sum(r.height + 12 for r in rows)
    sh = Image.new('RGBA', (W, H), (90, 100, 110, 255))
    y = 0
    for r in rows:
        sh.alpha_composite(r, (0, y)); y += r.height + 12
    sh.save(path)


if __name__ == '__main__':
    sheet(sys.argv[2].split(','), sys.argv[1], int(sys.argv[3]) if len(sys.argv) > 3 else 4)
