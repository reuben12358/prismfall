# usage: python3 -I normalize.py <dir> [maxpx]
# converts *.raw/*.orig (any PIL-readable) to <name>.png, downscaled to maxpx on the long side
# (pixel art: if the image is small, it is kept at native size), then deletes the raw file.
import sys, os
from PIL import Image
d = sys.argv[1]; mx = int(sys.argv[2]) if len(sys.argv) > 2 else 1200
for f in sorted(os.listdir(d)):
    if not (f.endswith('.raw') or f.endswith('.orig') or f.endswith('.dl')):
        continue
    src = os.path.join(d, f); name = f.rsplit('.', 1)[0]
    try:
        im = Image.open(src); im.load()
    except Exception as e:
        print('BAD', f, e); os.remove(src); continue
    if getattr(im, 'is_animated', False):
        im.seek(0)
    im = im.convert('RGBA')
    w, h = im.size
    if max(w, h) > mx:
        s = mx / max(w, h)
        im = im.resize((round(w*s), round(h*s)), Image.LANCZOS)
    out = os.path.join(d, name + '.png')
    im.save(out, optimize=True)
    os.remove(src)
    print(name, (w, h), '->', im.size)
