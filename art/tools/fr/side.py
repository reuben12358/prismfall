"""side.py OUT A.png [B.png ...] - candidates beside stock sprites at 1x and 4x."""
import sys
from PIL import Image
from fs import load, REF_T
def strip(paths, S):
    ims = [Image.fromarray(load(p)) for p in paths]
    W = sum(i.width * S + 6 for i in ims); H = max(i.height for i in ims) * S
    sh = Image.new('RGBA', (W, H), (120, 140, 150, 255)); x = 0
    for i in ims:
        sh.alpha_composite(i.resize((i.width * S, i.height * S), Image.NEAREST), (x, H - i.height * S)); x += i.width * S + 6
    return sh
out = sys.argv[1]; refs = [REF_T + 'RIVAL1.png', REF_T + 'LEADER_Misty.png', REF_T + 'LASS.png']
paths = refs + sys.argv[2:]
a, b = strip(paths, 1), strip(paths, 4)
sh = Image.new('RGBA', (max(a.width, b.width), a.height + b.height + 8), (90, 100, 110, 255))
sh.alpha_composite(a, (0, 0)); sh.alpha_composite(b, (0, a.height + 8)); sh.save(out)
