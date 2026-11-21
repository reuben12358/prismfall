"""zoom.py out k cols file[:x0,y0,x1,y1] ... -> grid of nearest-neighbour zooms with an 8-px grid (study only)."""
import sys
sys.path.insert(0, '/home/claude/fangame/tools/kitbash')
import kb
from PIL import Image, ImageDraw
out, k, cols = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
ims = []
for a in sys.argv[4:]:
    f, _, box = a.partition(':')
    im = kb.load(f)
    if not f.startswith('/home/claude/fangame/art/out') and 'Portraits' not in f:
        im = kb.native(im)[0]
    if box: im = im.crop(tuple(int(v) for v in box.split(',')))
    ims.append(im)
cw = max(i.width for i in ims)*k + 8; ch = max(i.height for i in ims)*k + 8
rows = (len(ims)+cols-1)//cols
S = Image.new('RGBA', (cols*cw, rows*ch), (150, 150, 165, 255)); d = ImageDraw.Draw(S)
for n, im in enumerate(ims):
    x, y = (n % cols)*cw, (n//cols)*ch
    S.alpha_composite(im.resize((im.width*k, im.height*k), Image.NEAREST), (x, y))
    for g in range(0, im.width+1, 8): d.line([(x+g*k, y), (x+g*k, y+im.height*k)], fill=(255, 0, 0, 60))
    for g in range(0, im.height+1, 8): d.line([(x, y+g*k), (x+im.width*k, y+g*k)], fill=(255, 0, 0, 60))
S.save(out); print(S.size)
