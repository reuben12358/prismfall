"""Juno bubble portrait (96x96 = 48-px art doubled), kitbashed from Desolation's face set 08.

Base face/hair : Desolation Faces/08a (smile), brows from 08e (raised, eager).
Repaint        : hair -> auburn ramp, irises -> green, hair flower -> a leafy sprig,
                 collar -> blackberry knit + the greenhouse's leather strap, freckles (hand, 6 px).
python3 -I tools/kitbash/juno_portrait.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, mat
from mat import H, CLEAR
from PIL import Image

D = '/home/claude/ref/games/desolation/Graphics/Faces/'
OUT = kb.WORK + '/juno'

HAIRMAP = {(111, 0, 42, 255): H('3c140e'), (123, 34, 66, 255): H('5e2216'), (148, 25, 82, 255): H('80301c'),
           (177, 35, 103, 255): H('a84426'), (219, 53, 135, 255): H('cc6232'), (255, 88, 175, 255): H('f09a5c'),
           (117, 70, 101, 255): H('7a4a3a'), (120, 76, 104, 255): H('7e4e3c'), (165, 111, 147, 255): H('b4806a'),
           (197, 152, 181, 255): H('dcb09a'), (197, 156, 184, 255): H('dcb29c')}
EYEMAP = {(111, 0, 42, 255): H('123828'), (148, 25, 82, 255): H('1e5a3c'), (177, 35, 103, 255): H('2e7a4a'),
          (219, 53, 135, 255): H('48a060'), (255, 88, 175, 255): H('8ed07a'), (123, 34, 66, 255): H('1e4a34')}
SPRIG = {(90, 0, 0, 255): H('1e3c22'), (145, 18, 28, 255): H('2e6a34'), (173, 26, 35, 255): H('4e9448'),
         (214, 40, 46, 255): H('8ccc6a')}
KNIT = {(36, 22, 42, 255): H('2a1636'), (53, 37, 55, 255): H('3e2250'), (64, 52, 70, 255): H('5a3470'),
        (79, 79, 91, 255): H('7a4e90')}


def face(name):
    return kb.native(kb.load(D + name + '.png'))[0]


def build():
    a = face('08a')
    e = face('08e')
    # eager brows from 08e (only the brow rows)
    brow = mat.region(a.size, rect=(12, 9, 44, 15))
    a = Image.composite(e, a, brow)
    eyes = mat.region(a.size, [[(15, 18), (24, 18), (24, 24), (15, 24)], [(34, 19), (40, 19), (40, 23), (34, 23)]])
    a = mat.recolour(a, EYEMAP, eyes)
    a = mat.recolour(a, HAIRMAP, mat.mask_not(eyes))
    a = mat.recolour(a, SPRIG, mat.region(a.size, rect=(36, 0, 48, 12)))
    a = mat.recolour(a, KNIT, mat.region(a.size, rect=(0, 38, 48, 48)))
    # freckles across nose and cheeks (skin shade colour)
    F = {'f': H('c88a74'), 'g': H('b87462')}
    for (x, y, c) in [(19, 27, 'f'), (21, 28, 'g'), (17, 29, 'f'), (27, 26, 'f'), (34, 27, 'g'), (36, 28, 'f')]:
        a = mat.patch(a, x, y, [c], F)
    # leather strap across the knit (the greenhouse harness) - straight 2px diagonal
    S = {'d': H('4e2c1c'), 'l': H('9a6440'), 'b': H('e2c060')}
    for i in range(10):
        a = mat.patch(a, 34 + i, 47 - i, ['dl'], S)
    a = mat.patch(a, 38, 42, ['b'], S)
    return a


if __name__ == '__main__':
    p = build()
    p.save(OUT + '/JUNO_portrait_native48.png')
    kb.up(p, 2).save(OUT + '/JUNO_happy.png')
    kb.grid(p, 10, every=4).save(kb.WORK + '/sheets/portrait_r1_grid.png')
