"""lint.py - house-style checks for a native sprite: alpha, orphans, colour count, outline colours.
python3 -I tools/kitbash/lint.py sprite.png [...]"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb
from PIL import Image
for f in sys.argv[1:]:
    im = Image.open(f).convert('RGBA'); p = im.load(); w, h = im.size
    semi = sum(1 for y in range(h) for x in range(w) if 0 < p[x, y][3] < 255)
    orph = []
    for y in range(h):
        for x in range(w):
            if p[x, y][3] == 0: continue
            n = sum(1 for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)) if 0 <= x+dx < w and 0 <= y+dy < h and p[x+dx, y+dy][3])
            if n == 0: orph.append((x, y))
    cols = kb.colours(im); bb = kb.bbox(im)
    print('%s size=%s bbox=%s colours=%d semi=%d orphans=%s' % (os.path.basename(f), im.size, bb, len(cols), semi, orph[:12]))
