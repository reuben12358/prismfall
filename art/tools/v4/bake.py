"""Bake a block-in .spr into the hand-edit canvas: one 'main' layer + a first selective outline
(material's darkest tone on lit sides, near-black on the right/bottom shadow side). After this, edit the .spr by hand.
python3 -I bake.py IN.spr OUT.spr"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from px4 import Sprite, outline

DARK = {'h': 'R', 'H': 'R', 'r': 'R', 'R': 'R', 'y': 'r', 'Y': 'r', 'o': 'r', 'S': 'r', 's': 'r',
        'W': 'v', 'w': 'v', 'v': 'v', 'g': 'E', 'G': 'E', 'e': 'E', 'E': 'E', 'T': 'b', 'b': 'd', 'B': 'd', 'd': 'd',
        'P': 'K', 'p': 'K', 'X': 'K', 'x': 'K', 'K': 'K'}


def main():
    sp = Sprite.load(sys.argv[1])
    g = sp.compose()

    def col(x, y, nb):
        # nb: list of (dx, dy, char) of opaque neighbours; shadow side = neighbour lies left of or above us
        shadow = any(dx == -1 or dy == -1 for dx, dy, _ in nb)
        mats = [ch for _, _, ch in nb]
        if shadow:
            return 'K'
        return DARK.get(mats[0], 'K')
    outline(g, col)
    sp.layers.clear()
    sp.layers['main'] = g
    sp.save(sys.argv[2])


if __name__ == '__main__':
    main()
