"""Write a solid-black silhouette of each input (native, cropped) next to the colour version: OUTDIR/<name>_cs.png
python3 -I sil.py OUTDIR FILE[%scale]..."""
import sys, os
from PIL import Image
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pack import native
out = sys.argv[1]
for spec in sys.argv[2:]:
    sc = 1.0
    if '%' in spec:
        spec, s = spec.rsplit('%', 1); sc = float(s)
    im = native(Image.open(spec).convert('RGBA'))
    a = np.array(im); ys, xs = np.where(a[..., 3] > 8)
    im = im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    if sc != 1:
        im = im.resize((int(im.width * sc), int(im.height * sc)), Image.NEAREST)
    a = np.array(im); s = a.copy(); s[..., :3] = 16; s[..., 3] = np.where(a[..., 3] > 8, 255, 0)
    S = Image.new('RGBA', (im.width * 2 + 6, im.height), (0, 0, 0, 0))
    S.alpha_composite(im, (0, 0)); S.alpha_composite(Image.fromarray(s), (im.width + 6, 0))
    n = os.path.splitext(os.path.basename(spec))[0]
    S.save(os.path.join(out, n + '_cs.png'))
