"""One-off helper: lay the kerchief band's three rows along its arc (I then hand-fix the ends and the knot).
python3 -I kerchief.py SPR"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from px4 import Sprite

sp = Sprite.load(sys.argv[1])
L = sp.layers['main']
for x in range(29, 51):
    t = (x - 40) / 12.0
    yt = int(round(9 + 4.2 * t * t))
    L[yt - 1][x] = 'r' if L[yt - 1][x] in 'hH' else L[yt - 1][x]   # thin dark line where hair meets the band's top
    L[yt][x] = 'Y' if x <= 43 else 'y'
    L[yt + 1][x] = 'y'
    L[yt + 2][x] = 'o'
    L[yt + 3][x] = 'R'                                              # cast shadow of the band on the hair/bangs
sp.save(sys.argv[1])
