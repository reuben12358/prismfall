from fs import *
import sys
from pc_a import JACK, TEAL
HAIR = ['#3a2030', '#6a3450', '#8e4c68', '#b87892']
DX, DY = -3, 0


def build():
    b = T('POKEMONTRAINER_Leaf')
    l = T('LASS')
    # ---------------- body recolour
    torso = poly(b, [(23, 22), (38, 22), (38, 38), (23, 38)])
    b = remap(b, {'#182850': '#7c7c96', '#306888': JACK[0], '#5088b0': JACK[1], '#78b8d8': JACK[2]}, torso)
    skirt = rect(b, 20, 35, 39, 44)
    b = remap(b, {'#c04040': '#2c3044', '#f86058': '#4a5068', '#785850': '#1e2030'}, skirt & ~rect(b, 36, 33, 46, 45))
    socks = rect(b, 0, 48, 63, 63)
    b = remap(b, {'#306888': TEAL[0], '#5088b0': TEAL[1], '#78b8d8': TEAL[2], '#c04040': TEAL[0], '#182850': TEAL[0]}, socks)
    cuffs = rect(b, 12, 30, 22, 38) | rect(b, 38, 33, 50, 40)
    b = remap(b, {'#182850': TEAL[0], '#306888': TEAL[0], '#5088b0': TEAL[1], '#78b8d8': TEAL[2]}, cuffs)
    bag = rect(b, 35, 33, 46, 46)
    b = remap(b, {'#f8c058': '#b08458', '#c89070': '#8a6440'}, bag)
    hairm = poly(b, [(33, 14), (50, 14), (50, 33), (44, 37), (36, 37), (33, 30)]) & ~bag
    b = remap(b, {'#785850': HAIR[1], '#c89070': HAIR[2]}, hairm)
    # ---------------- head swap
    b = clear(b, rect(b, 20, 5, 37, 23) | rect(b, 37, 5, 41, 16))
    src = rect(l, 22, 5, 47, 23) & ~rect(l, 0, 18, 29, 30)
    src |= rect(l, 37, 23, 47, 28) & colmask(l, ['#584038', '#986038', '#d08848', '#000000'])
    ll = l.copy()
    hm = rect(l, 22, 5, 47, 28)
    ll = remap(ll, {'#584038': HAIR[0], '#986038': HAIR[1], '#d08848': HAIR[2]}, hm)
    ll = remap(ll, {'#40a8d0': TEAL[2], '#4068a0': TEAL[0]}, rect(l, 22, 10, 31, 18))
    b = copy(b, ll, src, DX, DY)
    b = pix(b, [(29, 19), (35, 19)], TEAL[0])
    b = pix(b, [(29, 10), (30, 10), (31, 9), (32, 9), (27, 12), (28, 11), (36, 11), (37, 12), (42, 21), (43, 22), (45, 26), (46, 27)], HAIR[3])
    # teal neckerchief matching PLAYER_A's scarf
    b = patch(b, 26, 23, ["..kkkkk..", ".kTtTtTk.", "..kttk..."], {'k': '#000000', 'T': TEAL[2], 't': TEAL[1]})
    return b


if __name__ == '__main__':
    tag = sys.argv[1] if len(sys.argv) > 1 else 'r1'
    to_img(build()).save(f'/home/claude/fangame/art/previews/fr/pcb_{tag}.png')
