import sys, os
from PIL import Image, ImageDraw
src = sys.argv[1]; out = sys.argv[2]; S = int(sys.argv[3]); per = int(sys.argv[4]); files = sys.argv[5:]
ims = []
for f in files:
    im = Image.open(os.path.join(src, f)).convert('RGBA')
    ims.append((f, im))
cw = max(i.width for _, i in ims) // 2 * S + 4; ch = max(i.height for _, i in ims) // 2 * S + 14
rows = (len(ims) + per - 1) // per
sh = Image.new('RGBA', (per * cw, rows * ch), (120, 140, 150, 255)); d = ImageDraw.Draw(sh)
for k, (f, im) in enumerate(ims):
    im = im.resize((im.width // 2 * S, im.height // 2 * S), Image.NEAREST)
    x, y = (k % per) * cw, (k // per) * ch
    sh.alpha_composite(im, (x, y + 12)); d.text((x + 2, y), f[:-4][:22], fill=(10, 10, 20, 255))
sh.save(out)
