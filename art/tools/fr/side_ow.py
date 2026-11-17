import sys
from PIL import Image
from fs import load, REF_C
def strip(paths, S):
    ims = [Image.fromarray(load(p)) for p in paths]
    W = sum(i.width * S + 8 for i in ims); H = max(i.height for i in ims) * S
    sh = Image.new('RGBA', (W, H), (120, 140, 150, 255)); x = 0
    for i in ims:
        sh.alpha_composite(i.resize((i.width * S, i.height * S), Image.NEAREST), (x, 0)); x += i.width * S + 8
    return sh
refs = [REF_C + 'trainer_RIVAL1.png', REF_C + 'trainer_LASS.png']
paths = refs + sys.argv[2:]
a, b = strip(paths, 1), strip(paths, 3)
sh = Image.new('RGBA', (max(a.width, b.width), a.height + b.height + 8), (90, 100, 110, 255))
sh.alpha_composite(a, (0, 0)); sh.alpha_composite(b, (0, a.height + 8)); sh.save(sys.argv[1])
