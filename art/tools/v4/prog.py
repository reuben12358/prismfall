"""Progression sheet: every round's sprite side by side at 1x and 3x, labelled.
python3 -I prog.py OUT.png label=path.spr ..."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from px4 import Sprite, BG
from PIL import Image, ImageDraw

out = sys.argv[1]
items = []
for a in sys.argv[2:]:
    lab, p = a.split('=', 1)
    items.append((lab, Sprite.load(p).image()))
z = 3
cw = 80 * z + 8
S = Image.new('RGBA', (cw * len(items) + 8, 14 + 84 + 16 + 80 * z + 8), (60, 64, 72, 255))
d = ImageDraw.Draw(S)
d.rectangle([0, 12, S.width, 12 + 84], fill=BG)
d.rectangle([0, 12 + 84 + 14, S.width, S.height], fill=BG)
for i, (lab, im) in enumerate(items):
    x = 4 + i * cw
    d.text((x, 1), lab, fill=(255, 255, 255, 255))
    S.alpha_composite(im, (x + 80, 14))
    S.alpha_composite(im.resize((80 * z, 80 * z), Image.NEAREST), (x, 12 + 84 + 14))
S.save(out)
