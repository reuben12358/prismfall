import sys
from PIL import Image
out=sys.argv[1]; scale=int(sys.argv[2]); ps=sys.argv[3:]
ims=[Image.open(p).convert('RGBA') for p in ps]
W=sum(i.width for i in ims)+8*len(ims); H=max(i.height for i in ims)
sh=Image.new('RGBA',(W,H),(120,140,150,255)); x=0
for i in ims:
    sh.alpha_composite(i,(x,0)); x+=i.width+8
sh=sh.resize((W*scale,H*scale),Image.NEAREST); sh.save(out)
# check doubled
import numpy as np
for p,i in zip(ps,ims):
    a=np.array(i); d=(a[0::2,0::2]==a[1::2,1::2]).all() and (a[0::2,0::2]==a[0::2,1::2]).all()
    print(p.split('/')[-1], i.size, 'pixel-doubled' if d else 'native')
