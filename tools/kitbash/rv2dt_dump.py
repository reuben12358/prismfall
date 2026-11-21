"""rv2dt_dump.py in.png x0 y0 x1 y1 legend(hex=char,...) - dump a region as ASCII with a fixed legend (for hand edits)"""
import sys
from PIL import Image
im = Image.open(sys.argv[1]).convert('RGBA'); p = im.load()
x0, y0, x1, y1 = (int(v) for v in sys.argv[2:6])
leg = dict(kv.split('=') for kv in sys.argv[6].split(','))
for y in range(y0, y1):
    s = ''
    for x in range(x0, x1):
        c = p[x, y]
        s += '.' if c[3] == 0 else leg.get('%02x%02x%02x' % c[:3], '?')
    print("'%s',  # %d" % (s, y))
