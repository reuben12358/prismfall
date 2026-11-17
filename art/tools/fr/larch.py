from fs import *
K = '#000000'
HAIR = ['#4a4856', '#77768a', '#a6a6b6', '#d4d4de']
OIL = ['#6e5226', '#a8822c', '#d4ac44', '#f0d47a']


def build():
    a = T('SCIENTIST')
    H, W = a.shape[:2]
    keep_glasses = rect(a, 0, 0, 63, 16)
    flask = rect(a, 45, 8, 63, 35)
    ball = rect(a, 8, 14, 22, 24)
    coat = ~keep_glasses & ~flask & ~ball
    a = ramp_map(a, ['#808890', '#b0b8c0', '#d0d8d0', '#f8f8f8'], OIL, coat)
    # hair (top of head) and trousers share the blue ramp
    hair = rect(a, 20, 0, 42, 19)
    a = remap(a, {'#384060': HAIR[0], '#586088': HAIR[1], '#8088a8': HAIR[2]}, hair)
    legs = rect(a, 0, 34, 63, 63)
    a = remap(a, {'#384060': '#2c3a38', '#586088': '#46584f', '#8088a8': '#687c70'}, legs)
    # vest/shirt strip and tie
    body = rect(a, 22, 18, 44, 40)
    a = remap(a, {'#384060': '#2e3c4a', '#a878a8': '#4c6c7a', '#e0a8d8': '#7c9ca6'}, body)
    # flask: kelp tea
    a = remap(a, {'#a878a8': '#3e7a3a', '#e0a8d8': '#86c062', '#8088a8': '#c8d4c8'}, flask)
    # bubbles above the flask -> clear; steam wisps drawn below
    a = clear(a, rect(a, 46, 8, 56, 16) & colmask(a, ['#c8d4c8', '#586088', '#384060']))
    L = {'k': K, 'd': HAIR[0], 'm': HAIR[1], 'l': HAIR[2], 'h': HAIR[3], 'r': '#a8453a', 'R': '#d8705a', 's': '#e2ece2', 'S': '#b8c8b8'}
    # braid flying out behind her (she is mid-stride)
    a = patch(a, 39, 8, [
        "k.........",
        "mkk.......",
        "lhmk......",
        "mldmkk....",
        "dkhlmdk...",
        ".kdmhlmk..",
        "..kkdkhlk.",
        "....kdmhmk",
        ".....kkdRk",
        ".......krk",
        "........k.",
    ], L)
    # long sidelock down the near cheek
    a = patch(a, 25, 15, ["km", "km", "kd", "k."], L)
    # steam off the kelp tea
    a = patch(a, 49, 12, ["..s", ".S.", "s..", ".s.", "..S"], L)
    return a


if __name__ == '__main__':
    a = build()
    to_img(a).save('/home/claude/fangame/art/previews/fr/larch_r3.png')
    import subprocess
    subprocess.run(['python3', 'zoom.py', '../../previews/fr/_z_larch_r3.png', '8', '../../previews/fr/larch_r3.png'])
