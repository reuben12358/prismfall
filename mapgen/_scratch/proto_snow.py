import sys, os
sys.path.insert(0, '/home/claude/fangame/mapgen/layouts'); sys.path.insert(0, '/home/claude/fangame/mapgen')
import rkit as K, rimewood as RW, numpy as np
m = RW.snowmap(30, 20, 999)
m.auto['d'] = ('Packed Snow', 'pf'); m.auto['p'] = ('Frozen Pond', 'pf'); m.auto['e'] = ('KristilineDirt', 'rejuvenation')
m.AUTO_Z = dict(m.AUTO_Z, p=0, e=1); m.JOIN = dict(m.JOIN, p='p')
m.lane([(-1, 4), (8, 4), (14, 8), (14, 19)], 'd', 2.6, seed=3, only='.', wobble=0.4)
m.blob(20, 10, 7, 4.5, 'p', seed=5, rough=0.8, only='.')
m.rect(12, 9, 4, 2, 'e', only='d')
m.paint()
m.preview('/home/claude/fangame/mapgen/_scratch/proto_snow.png', 1.0, events=False)
