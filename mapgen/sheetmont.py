#!/usr/bin/env python3
"""sheetmont.py sheet.png out.png rows_per_col scale [r0 r1] : row-numbered montage of a tileset sheet (research)."""
import sys
from PIL import Image, ImageDraw
Image.MAX_IMAGE_PIXELS = None
path, out, rows_per, scale = sys.argv[1], sys.argv[2], int(sys.argv[3]), float(sys.argv[4])
im = Image.open(path).convert('RGBA'); r0 = int(sys.argv[5]) if len(sys.argv) > 5 else 0
r1 = int(sys.argv[6]) if len(sys.argv) > 6 else im.height // 32
cols = -(-(r1 - r0) // rows_per); cw = int(256 * scale) + 34
o = Image.new('RGB', (cols * cw, int(rows_per * 32 * scale)), (70, 70, 70)); d = ImageDraw.Draw(o)
for c in range(cols):
    a = r0 + c * rows_per; b = min(r1, a + rows_per)
    cr = im.crop((0, a * 32, 256, b * 32)); bg = Image.new('RGBA', cr.size, (70, 70, 70, 255)); bg.alpha_composite(cr)
    o.paste(bg.resize((int(256 * scale), int(cr.height * scale)), Image.NEAREST).convert('RGB'), (c * cw + 30, 0))
    for r in range(a, b, 5 if scale < 0.7 else 2): d.text((c * cw + 2, int((r - a) * 32 * scale)), str(r), fill=(255, 255, 0))
o.save(out); print(o.size)
