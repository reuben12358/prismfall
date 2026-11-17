"""Juno concept sheet: 4 concepts at 1x (two battle-ish backgrounds) and 4x, two references, the before (v4),
and the favourite's portrait. python3 -I sheet.py OUT.png"""
import sys, os, textwrap
from PIL import Image, ImageDraw
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'study'))
from pack import native  # noqa: E402

W = '/home/claude/fangame/art/work/concepts/'
CONCEPTS = [
    ('1  UNDER GLASS', W + 'c1.png', 'A girl who carries her whole world under glass: a walking greenhouse of rescued plants (and the seed-pod that becomes Tsareena), because she cannot bear to lose one more thing.'),
    ('2  ROT & BLOOM', W + 'c2.png', 'Verdance is the city where nothing ever rots; Juno is the girl who thinks rot is the most beautiful thing in the world. A gleeful little toadstool of a forager.'),
    ('3  SEED BOMBER', W + 'c3.png', 'Earnest chaos, literally: a guerrilla gardener who lobs seed bombs at every bare patch of ground, and at most of her problems. Backs every underdog, weeds included.'),
    ('4  EVER-BLOOM', W + 'c4.png', 'She was three when her aunt became a tree in permanent bloom. She has worn its never-wilting blossoms every day since: the flower girl of a wedding that never ended.'),
]
REFS = [
    ('ref: Bianca (BW, official)', '/home/claude/ref/charrefs/showdown/bianca.png', 'Canon friendly rival: personality in the pose (heel kick, ball hugged).'),
    ('ref: Angie (Rejuvenation)', '/home/claude/ref/games/rejuvenation/Graphics/Characters/trainer139.png', 'Fangame bar: mundane role (maid) + one supernatural shape (flame hair).'),
]
BEFORE = ('before: Juno v4', '/home/claude/fangame/art/out/v4/Trainers/JUNO_v4_native80.png')
BG1, BG2 = (148, 160, 166, 255), (88, 120, 96, 255)
INK, PAPER, DARK = (20, 20, 24, 255), (238, 236, 230, 255), (44, 46, 54, 255)


def load(p):
    im = native(Image.open(p).convert('RGBA'))
    a = np.array(im); ys, xs = np.where(a[..., 3] > 8)
    return im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))


def main(out):
    items = [(n, load(p), t) for n, p, t in CONCEPTS] + [(n, load(p), t) for n, p, t in REFS]
    z = 4
    colw = max(im.width for _, im, _ in items) * z + 24
    hmax = max(im.height for _, im, _ in items)
    Wd = colw * len(items) + 8
    # rows: title 26 | 1x strips 120 | 4x row hmax*4 + labels 120 | portrait row 330
    H = 26 + 130 + 22 + hmax * z + 130 + 360
    S = Image.new('RGBA', (Wd, H), DARK)
    d = ImageDraw.Draw(S)
    d.text((8, 7), 'JUNO HALE - four directions (quick, bold thumbnails, NOT polished). 80x80 native battle fronts drawn with px4. '
           'Pick a direction; nothing gets polished before that.', fill=PAPER)
    # ---- 1x strips on two backgrounds
    y = 30
    x = 8
    for bg in (BG1, BG2):
        sw = sum(im.width + 14 for _, im, _ in items) + 14 + 90
        d.rectangle([x, y, x + sw, y + hmax + 26], fill=bg)
        xx = x + 10
        for n, im, _ in items:
            S.alpha_composite(im, (xx, y + 18 + hmax - im.height))
            d.text((xx, y + 3), n.split('  ')[0] if n[0].isdigit() else n.split(':')[1].split('(')[0].strip()[:8], fill=INK)
            xx += im.width + 14
        bv = load(BEFORE[1])
        S.alpha_composite(bv, (xx + 20, y + 18 + hmax - bv.height))
        d.text((xx + 14, y + 3), 'v4 before', fill=INK)
        x += sw + 24
    d.text((x + 4, y + 10), '1x, as in battle. Squint: which', fill=PAPER)
    d.text((x + 4, y + 24), 'shapes survive?', fill=PAPER)
    # ---- 4x row
    y4 = y + hmax + 50
    d.rectangle([0, y4 - 4, Wd, y4 + hmax * z + 8], fill=BG1)
    xx = 8
    for i, (n, im, t) in enumerate(items):
        big = im.resize((im.width * z, im.height * z), Image.NEAREST)
        S.alpha_composite(big, (xx + (colw - big.width) // 2, y4 + hmax * z - big.height))
        ly = y4 + hmax * z + 14
        d.rectangle([xx, ly - 2, xx + colw - 12, ly + 112], fill=(30, 32, 40, 255) if i < 4 else (54, 56, 66, 255))
        d.text((xx + 6, ly + 2), n, fill=(255, 214, 120, 255) if i < 4 else PAPER)
        for j, line in enumerate(textwrap.wrap(t, max(20, (colw - 24) // 6))):
            d.text((xx + 6, ly + 18 + j * 12), line, fill=PAPER)
        xx += colw
    # ---- portrait row (favourite)
    py = y4 + hmax * z + 140
    d.text((8, py), 'Favourite: 1 UNDER GLASS - matching bubble portrait (96x96 native; shown 1x, 3x, and in a speech-bubble circle)', fill=(255, 214, 120, 255))
    por = Image.open(W + 'c1_portrait.png').convert('RGBA')
    d.rectangle([8, py + 18, 8 + 96 + 16, py + 18 + 96 + 16], fill=BG1)
    S.alpha_composite(por, (16, py + 26))
    p3 = por.resize((288, 288), Image.NEAREST)
    d.rectangle([136, py + 18, 136 + 288 + 16, py + 18 + 288 + 16], fill=BG1)
    S.alpha_composite(p3, (144, py + 26))
    # circle bubble preview (2x)
    p2 = por.resize((192, 192), Image.NEAREST)
    mask = Image.new('L', (192, 192), 0); ImageDraw.Draw(mask).ellipse([0, 0, 191, 191], fill=255)
    bub = Image.new('RGBA', (192, 192), (250, 250, 250, 255)); bub.alpha_composite(p2)
    cx, cy = 470, py + 40
    d.ellipse([cx - 6, cy - 6, cx + 198, cy + 198], fill=(20, 20, 24, 255))
    S.paste(bub, (cx, cy), mask)
    d.text((cx + 210, cy + 60), '[portrait: JUNO, happy]', fill=PAPER)
    d.text((cx + 210, cy + 76), '"Did you know larches drop every needle', fill=PAPER)
    d.text((cx + 210, cy + 90), ' each winter? They look dead! They are NOT!"', fill=PAPER)
    S.save(out)
    print(out, S.size)


if __name__ == '__main__':
    main(sys.argv[1])
