import sys
from PIL import Image
for p in sys.argv[1:]:
    im=Image.open(p); print(p.split('/')[-1], im.size, im.mode, len(im.convert('RGBA').getcolors(100000) or []))
