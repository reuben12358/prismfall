"""Quick test of the other route: heavy edit of a Rejuvenation trainer (trainer002, girl in dungarees, 90x90 native) into Juno.
Body: Rejuvenation's hand-drawn pixels, recoloured by role to Juno's palette (dungarees -> leaf green, leggings -> tall
brown boots, sneakers -> boot leather, white shirt -> cream). Head: my v4 Juno head (hair cloud, face, kerchief) placed on
her neck, then her ball hand put back on top. Read-only input; writes one PNG.
python3 -I rejuv_edit_test.py REJUV_TRAINER002.png JUNO.spr OUT.png"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from px4 import Sprite, hex2rgba
from contact import native
from PIL import Image
import numpy as np

J = {  # Juno palette (same as juno.spr)
    'K': '#1c1424', 'R': '#4a1a22', 'r': '#8a3428', 'h': '#c0552e', 'H': '#e8904c', 'o': '#b8601a', 'y': '#f39c1e',
    'Y': '#ffd04a', 's': '#eca282', 'S': '#ffdcc0', 'v': '#8e7e88', 'w': '#d4c4ac', 'W': '#f8f0d8', 'E': '#1f4636',
    'e': '#3a7838', 'g': '#5ea83a', 'G': '#9ad050', 'T': '#e8bc78', 'd': '#42221e', 'b': '#74402a', 'B': '#a86a3e',
    'p': '#8c2238', 'P': '#e43c3c', 'x': '#b8bccc', 'X': '#ffffff'}
# source colour -> Juno role (from the dump of trainer002's palette)
MAP = {
    '#000000': 'K', '#33030e': 'K', '#0f1821': 'd', '#111340': 'E', '#740022': 'E', '#20234e': 'E', '#23303d': 'd',
    '#6d2252': 'R', '#b9083c': 'e', '#363c88': 'e', '#3b454e': 'b', '#901f53': 'r', '#913066': 'r', '#3f4cad': 'e',
    '#98356b': 'r', '#bd3131': 'P', '#8a5146': 'r', '#4f6ac6': 'g', '#506bd0': 'g', '#ba4b82': 'o', '#7379b3': 'v',
    '#bd7b63': 'r', '#d7639d': 'y', '#6c89f4': 'G', '#988ec4': 'w', '#da9155': 'o', '#f581bb': 'Y', '#d8a888': 's',
    '#abbccd': 'b', '#c9cceb': 'w', '#ffd5bd': 'S', '#ffd6bd': 'S', '#ededf9': 'W', '#edf0f2': 'B', '#f8f8f8': 'X',
    '#ffffff': 'W'}


def main():
    src, d = native(Image.open(sys.argv[1]))
    a = np.array(src.convert('RGBA'))
    out = np.zeros_like(a)
    H, W = a.shape[:2]
    for y in range(H):
        for x in range(W):
            if a[y, x, 3] == 0:
                continue
            hx = '#%02x%02x%02x' % tuple(a[y, x, :3])
            out[y, x] = hex2rgba(J[MAP.get(hx, 'K')])
    body = out.copy()
    # remove her long hair below the head (it would show around my hair cloud): hair-coloured pixels below y=40 -> clear
    # (in this sprite the hair colours are the pink ramp, mapped to y/o/r/R/Y above)
    # paste my head: my rows 0..27, neck (39.5, 26) -> her neck (~45, 38)
    sp = Sprite.load(sys.argv[2])
    me = np.array(sp.image())
    dx, dy = 45 - 40, 38 - 26
    for y in range(0, 28):
        for x in range(16, 64):
            if x < 29 and y >= 17:
                continue   # skip my own ball hand
            if me[y, x, 3] and 0 <= y + dy < H and 0 <= x + dx < W:
                out[y + dy, x + dx] = me[y, x]
    # her hair strands that hung over the shoulders/back: anything in the old hair ramp outside my head -> clear
    hair_src = {'#6d2252', '#ba4b82', '#d7639d', '#f581bb', '#913066', '#98356b', '#901f53'}
    for y in range(H):
        for x in range(W):
            hx = '#%02x%02x%02x' % tuple(a[y, x, :3])
            inside_me = (0 <= y - dy < 28 and 16 <= x - dx < 64 and me[y - dy, x - dx, 3] > 0 and not (x - dx < 29 and y - dy >= 17))
            if hx in hair_src and not inside_me and y < 62 and not (52 <= y <= 57 and 40 <= x <= 52):
                out[y, x] = 0
    # put her ball hand back on top (x26..36, y34..47)
    for y in range(34, 48):
        for x in range(24, 37):
            if body[y, x, 3]:
                out[y, x] = body[y, x]
    im = Image.fromarray(out)
    im.save(sys.argv[3])


if __name__ == '__main__':
    main()
