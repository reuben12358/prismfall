"""rv2dt_view.py - quick zoom contact for review: python3 -I rv2dt_view.py out.png scale img1 [img2 ...]
Each image is cropped to its own size, scaled by `scale` (nearest), laid out left to right on a grey/cream plate."""
import sys
from PIL import Image
out, s = sys.argv[1], int(sys.argv[2])
ims = [Image.open(f).convert('RGBA') for f in sys.argv[3:]]
W = sum(i.width * s + 8 for i in ims) + 8
H = max(i.height * s for i in ims) + 16
bg = Image.new('RGBA', (W, H), (150, 150, 160, 255))
x = 8
for i in ims:
    z = i.resize((i.width * s, i.height * s), Image.NEAREST)
    plate = Image.new('RGBA', z.size, (236, 230, 214, 255))
    plate.alpha_composite(z)
    bg.alpha_composite(plate, (x, 8)); x += z.width + 8
bg.save(out)
