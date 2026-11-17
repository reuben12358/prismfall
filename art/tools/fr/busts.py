"""Frankenportraits: HGSS VS busts, Scale2x'd to 96-px-native, recoloured,
cropped to the 96x96 bubble, then hand-patched per expression."""
import numpy as np
from PIL import Image
from fs import *
W = '/home/claude/fangame/art/work/'
TEAL = ['#1e6a68', '#2f948c', '#5cc4b4']


def up(name):
    return np.array(Image.open(W + f'up_{name}.png').convert('RGBA'))


def crop(a, x0, y0, n=96):
    out = np.zeros((n, n, 4), np.uint8)
    h, w = a.shape[:2]
    sub = a[max(0, y0):min(h, y0 + n), max(0, x0):min(w, x0 + n)]
    out[max(0, -y0):max(0, -y0) + sub.shape[0], max(0, -x0):max(0, -x0) + sub.shape[1]] = sub
    return out


def flood(a, seed, cols):
    from collections import deque
    ok = colmask(a, cols)
    m = np.zeros(ok.shape, bool)
    q = deque([seed[::-1]])
    while q:
        y, x = q.popleft()
        if 0 <= y < ok.shape[0] and 0 <= x < ok.shape[1] and ok[y, x] and not m[y, x]:
            m[y, x] = True
            q.extend(((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)))
    return m


def base_pca():
    a = up('blue')
    eyes = rect(a, 104, 45, 120, 61) | rect(a, 130, 44, 148, 60)
    a = remap(a, {'#684820': '#1e6a68', '#a07040': '#2f948c'}, eyes & ~rect(a, 104, 45, 120, 47) & ~rect(a, 130, 44, 148, 46))
    hair = rect(a, 80, 0, 191, 110) & ~eyes
    a = remap(a, {'#684820': '#363244', '#a87840': '#5a566c', '#d89050': '#8a84a2'}, hair)
    a = remap(a, {'#383840': '#9a9ab2', '#505058': '#cbcbda'}, rect(a, 0, 86, 191, 127))
    a = remap(a, {'#7888a0': TEAL[0], '#c8c8d8': TEAL[1], '#f0f0f8': TEAL[2]}, rect(a, 0, 86, 191, 127))
    return crop(a, 84, 4)


def base_pcb():
    a = up('misty')
    head = rect(a, 0, 0, 119, 110)
    face = flood(a, (70, 60), ['#f8d8c0', '#d8a888']) | flood(a, (50, 62), ['#f8d8c0', '#d8a888'])
    for _ in range(2):   # grow onto the face's own shadow pixels
        g = face.copy(); g[1:] |= face[:-1]; g[:-1] |= face[1:]; g[:, 1:] |= face[:, :-1]; g[:, :-1] |= face[:, 1:]
        face = g
    a = remap(a, {'#784828': '#5a2a44', '#d89840': '#b87892'}, head)
    a = remap(a, {'#a07040': '#8e4c68'}, head & ~face)
    a = remap(a, {'#a07040': '#c48474'}, face)        # rosier cheek shadow under plum hair
    a = remap(a, {'#286028': '#1e6a68', '#589050': '#3fa69e'})
    a = remap(a, {'#b0d0f0': '#efeff5', '#80a0c8': '#cbcbda', '#385078': '#7c7c96', '#4070a8': TEAL[0], '#38a0d8': TEAL[1]})
    return crop(a, 22, 2)


def base_larch():
    a = up('erika')
    head = rect(a, 0, 0, 191, 80)
    a = remap(a, {'#383848': '#6a6878', '#585860': '#9898a8', '#b0b0d0': '#d8d8e2', '#803838': '#6a6878', '#b85858': '#9898a8', '#d07070': '#c0c0cc'}, head)
    body = rect(a, 0, 78, 191, 127)
    a = remap(a, {'#e8c038': '#d4ac44', '#c89050': '#a8822c', '#803838': '#3c4c56', '#b85858': '#5b6e78', '#d07070': '#7c9098'}, body)
    eyes = rect(a, 74, 36, 92, 56) | rect(a, 102, 36, 114, 56)
    a = remap(a, {'#604830': '#2c4048', '#a07040': '#56707a'}, eyes & ~rect(a, 74, 36, 114, 40))
    return crop(a, 44, 6)


if __name__ == '__main__':
    import sys
    tag = sys.argv[1] if len(sys.argv) > 1 else 'r1'
    for n, fn in (('pca', base_pca), ('pcb', base_pcb), ('larch', base_larch)):
        Image.fromarray(fn()).save(W + f'bust_{n}_{tag}.png')
