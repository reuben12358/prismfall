from fs import *
import sys
K = '#000000'
HAIR = ['#2c2836', '#4e4a5c', '#78728a', '#a8a2ba']
JACK = ['#9a9ab2', '#cbcbda', '#efeff5']
TEAL = ['#1e6a68', '#2f948c', '#5cc4b4']
DX, DY = -3, 0


def build():
    b = T('POKEMONTRAINER_Brendan')
    r = T('RIVAL1')
    # --- body recolour (before the head goes on)
    top = rect(b, 0, 0, 63, 41)
    low = rect(b, 0, 42, 63, 63)
    b = remap(b, {'#182850': JACK[0], '#485880': JACK[1], '#607898': JACK[2]}, top)
    ball = rect(b, 43, 25, 55, 35)
    b = remap(b, {'#182850': '#232436', '#485880': '#3e4258', '#607898': '#5e6680'}, low)
    b = remap(b, {'#c04040': TEAL[0], '#f86058': TEAL[2]}, ~ball)
    glove = rect(b, 15, 37, 24, 45)
    b = remap(b, {'#b89858': '#3a3648', '#f8c058': '#5a566c'}, glove)
    b = remap(b, {'#b89858': '#7a5a3e', '#f8c058': '#b08458'}, ~glove)
    # --- head swap
    head = rect(b, 16, 0, 44, 24)
    b = clear(b, head)
    src = rect(r, 16, 0, 46, 25) & ~rect(r, 0, 22, 27, 30) & ~(rect(r, 35, 22, 46, 30) & colmask(r, ['#304050', '#687880', '#000000']))
    hairm = rect(r, 16, 0, 46, 21) & colmask(r, ['#c07808', '#d8a048'])
    hairedge = rect(r, 16, 0, 46, 18) & colmask(r, ['#684848'])
    rr = r.copy()
    rr = remap(rr, {'#c07808': HAIR[1], '#d8a048': HAIR[2]}, hairm)
    rr = remap(rr, {'#684848': HAIR[0]}, hairedge)
    rr = remap(rr, {'#c0c8b0': '#3f9a9e'}, rect(r, 16, 15, 46, 22))
    b = copy(b, rr, src, DX, DY)
    # simplify Brendan's chest pattern: collar becomes the teal scarf, the
    # chest stripes become plain jacket, wrist bands stay teal
    collar = rect(b, 24, 25, 39, 28)
    b = remap(b, {'#7a5a3e': TEAL[0], '#b08458': TEAL[1], JACK[2]: TEAL[2], JACK[1]: TEAL[1], JACK[0]: TEAL[0]}, collar)
    chest = rect(b, 25, 29, 39, 40)
    b = remap(b, {TEAL[0]: JACK[0], TEAL[2]: JACK[1], TEAL[1]: JACK[1]}, chest)
    # hair highlights (RIVAL1 hair has only two tones)
    b = pix(b, [(26, 10), (27, 10), (28, 11), (30, 9), (31, 9), (32, 10), (24, 13), (25, 13), (34, 11), (29, 13), (30, 13)], HAIR[3])
    return b


if __name__ == '__main__':
    tag = sys.argv[1] if len(sys.argv) > 1 else 'r1'
    a = build()
    to_img(a).save(f'/home/claude/fangame/art/previews/fr/pca_{tag}.png')
