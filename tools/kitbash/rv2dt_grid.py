"""rv2dt_grid.py - zoom with a pixel grid and row/col ticks for critique: python3 -I rv2dt_grid.py in.png out.png [scale] [bg]"""
import sys
from PIL import Image, ImageDraw
src = Image.open(sys.argv[1]).convert('RGBA')
s = int(sys.argv[3]) if len(sys.argv) > 3 else 10
bgc = sys.argv[4] if len(sys.argv) > 4 else 'e8e2d4'
bg = tuple(int(bgc[i:i + 2], 16) for i in (0, 2, 4)) + (255,)
W, H = src.width * s + 30, src.height * s + 30
out = Image.new('RGBA', (W, H), (60, 60, 70, 255))
pl = Image.new('RGBA', src.size, bg); pl.alpha_composite(src)
out.paste(pl.resize((src.width * s, src.height * s), Image.NEAREST), (30, 30))
d = ImageDraw.Draw(out)
for x in range(src.width + 1):
    c = (0, 0, 0, 90) if x % 5 else (255, 0, 0, 160)
    d.line([(30 + x * s, 30), (30 + x * s, H)], fill=c)
    if x % 5 == 0 and x < src.width: d.text((30 + x * s + 1, 4 + (x % 10) * 1), str(x), fill=(255, 255, 255, 255))
for y in range(src.height + 1):
    c = (0, 0, 0, 90) if y % 5 else (255, 0, 0, 160)
    d.line([(30, 30 + y * s), (W, 30 + y * s)], fill=c)
    if y % 5 == 0 and y < src.height: d.text((2, 30 + y * s + 1), str(y), fill=(255, 255, 255, 255))
out.save(sys.argv[2])
