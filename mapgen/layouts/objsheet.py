#!/usr/bin/env python3
"""objsheet.py [out.png] [filter] - contact sheet of every wildkit object (name, footprint; red = solid cell)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wildkit as w
from PIL import Image, ImageDraw
Image.MAX_IMAGE_PIXELS = None
sheet = Image.open(os.path.join(os.path.dirname(w.HERE), 'maps_out', 'Graphics', 'Tilesets', 'Prismfall Wilds.png')).convert('RGBA')
def tile(t): i = t - 384; return sheet.crop((i % 8 * 32, i // 8 * 32, i % 8 * 32 + 32, i // 8 * 32 + 32))
names = [n for n in list(w.TREES) + list(w.OBJ) if len(sys.argv) < 3 or sys.argv[2] in n]
cw, ch = 5 * 32 + 12, 6 * 32 + 16; cols = 9
out = Image.new('RGBA', (cols * cw, ((len(names) + cols - 1) // cols) * ch), (120, 190, 110, 255)); d = ImageDraw.Draw(out)
for i, n in enumerate(names):
    ox, oy = (i % cols) * cw + 4, (i // cols) * ch + 14
    d.text((ox, oy - 13), n[:24], fill=(0, 0, 0))
    for dx, dy, z, t in w.obj_cells(n):
        if dx > 4 or dy > 5: continue
        tl = tile(t); out.alpha_composite(tl, (ox + dx * 32, oy + dy * 32))
        if w.solid(t): d.rectangle((ox + dx * 32 + 13, oy + dy * 32 + 13, ox + dx * 32 + 18, oy + dy * 32 + 18), fill=(255, 0, 0))
        if z == 2: d.rectangle((ox + dx * 32, oy + dy * 32, ox + dx * 32 + 4, oy + dy * 32 + 4), fill=(0, 0, 255))
out.convert('RGB').save(sys.argv[1] if len(sys.argv) > 1 else '/tmp/b3/objs.png'); print(out.size, len(names))
