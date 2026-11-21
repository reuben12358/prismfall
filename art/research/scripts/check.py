"""check.py out img48 [img48 ...]: each portrait at 2x (in-game 96x96) on a dark and a light plate, plus 4x, beside Juno pass 3."""
import sys
from PIL import Image
out = sys.argv[1]; fs = sys.argv[2:] + ['/home/claude/fangame/art/out/Graphics/Portraits/JUNO.png']
ims = []
for f in fs:
    im = Image.open(f).convert('RGBA')
    if im.size == (96, 96): im = im.resize((48, 48), Image.NEAREST)
    ims.append(im)
S = Image.new('RGBA', (len(ims) * 420, 300), (40, 40, 48, 255))
for i, im in enumerate(ims):
    x = i * 420
    for j, bg in enumerate([(52, 56, 74, 255), (232, 226, 212, 255)]):
        b = Image.new('RGBA', (100, 100), bg); b.alpha_composite(im.resize((96, 96), Image.NEAREST), (2, 2))
        S.alpha_composite(b, (x + 10, 10 + j * 110))
    b = Image.new('RGBA', (192, 192), (52, 56, 74, 255)); b.alpha_composite(im.resize((192, 192), Image.NEAREST))
    S.alpha_composite(b, (x + 120, 10))
    S.alpha_composite(im, (x + 10, 240))
S.save(out)
