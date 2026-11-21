# usage: python3 -I contact.py <out.png> <cell_px> <cols> <img>... ; contact sheet with filename labels
import sys, os
from PIL import Image, ImageDraw
out, cell, cols = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
files = sys.argv[4:]
rows = (len(files)+cols-1)//cols
S = Image.new('RGB', (cols*(cell+6)+6, rows*(cell+22)+6), (40,40,46))
d = ImageDraw.Draw(S)
for i, f in enumerate(files):
    im = Image.open(f).convert('RGBA')
    w, h = im.size; s = min(cell/w, cell/h)
    rs = Image.NEAREST if max(w,h) <= 300 else Image.LANCZOS
    im = im.resize((max(1,round(w*s)), max(1,round(h*s))), rs)
    bg = Image.new('RGBA', (cell, cell), (150,150,160,255)); bg.alpha_composite(im, ((cell-im.width)//2, (cell-im.height)//2))
    x = 6 + (i%cols)*(cell+6); y = 6 + (i//cols)*(cell+22)
    S.paste(bg.convert('RGB'), (x, y))
    d.text((x, y+cell+3), os.path.basename(f)[:int(cell/6)], fill=(230,230,230))
S.save(out)
