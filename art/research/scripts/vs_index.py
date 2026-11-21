"""Index sheet of VS busts (native 128x64) for donor scouting. python3 -I vs_index.py <game> <out>"""
import sys, glob, os
sys.path.insert(0, '/home/claude/fangame/tools/kitbash')
import kb
from PIL import Image, ImageDraw
game, out = sys.argv[1], sys.argv[2]
fs = sorted(glob.glob(f'/home/claude/ref/games/{game}/Graphics/Transitions/vsTrainer*.png'))
cols = 10; cw, ch = 132, 78
S = Image.new('RGBA', (cols*cw, ((len(fs)+cols-1)//cols)*ch), (150, 150, 165, 255)); d = ImageDraw.Draw(S)
for i, f in enumerate(fs):
    im = kb.native(kb.load(f))[0]
    if im.size != (128, 64): im = im.resize((128, 64))
    x, y = (i % cols)*cw, (i//cols)*ch
    S.alpha_composite(im, (x, y)); d.text((x+2, y+64), os.path.basename(f)[9:-4], fill=(0, 0, 0, 255))
S.save(out); print(len(fs), S.size)
