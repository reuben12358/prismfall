"""tileview.py OUT.png TILESET.png [strip_h] - tall tileset -> side-by-side strips at 1x (y labels)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb
from PIL import Image, ImageDraw
src = kb.load(sys.argv[2]); sh = int(sys.argv[3]) if len(sys.argv) > 3 else 800
y0 = int(sys.argv[4]) if len(sys.argv) > 4 else 0
y1 = int(sys.argv[5]) if len(sys.argv) > 5 else src.size[1]
w = src.size[0]; n = (y1 - y0 + sh - 1) // sh
out = Image.new('RGBA', (n * (w + 30), sh), (150, 160, 170, 255)); d = ImageDraw.Draw(out); f = kb.font(9)
for i in range(n):
    part = src.crop((0, y0 + i * sh, w, min(y1, y0 + (i + 1) * sh)))
    out.alpha_composite(part, (i * (w + 30) + 28, 0))
    for yy in range(0, sh, 100):
        d.text((i * (w + 30), yy), str(y0 + i * sh + yy), fill=(0, 0, 0, 255), font=f)
out.save(sys.argv[1]); print(out.size)
