"""Juno Ever-Bloom overworld charset (4 dirs x 4 frames, 30x32-px frames, exported doubled 240x256 like the donor).
Donor: official BW overworld trchar048 (white-dress girl; Radical Raptr rip). Hair repainted auburn; wreath
(pink/white dots over the crown) and veil (sheer strip behind the head and down the back) hand-placed per frame.
python3 -I tools/kitbash/juno_everbloom_ow.py"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, mat
from mat import H, CLEAR
from PIL import Image

SRC = '/home/claude/ref/art/sprites_gen5_ow_radicalraptr/extracted/Gen 5 Characters/trchar048.png'
HAIRMAP = {(48, 32, 16, 255): H('4a1c16'), (80, 56, 40, 255): H('7a2c1c'), (120, 72, 48, 255): H('a8442a'),
           (120, 80, 48, 255): H('a8442a'), (160, 112, 56, 255): H('c8582e'), (192, 152, 88, 255): H('f0945a')}
W = {'p': H('ec8aa2'), 'w': H('fff0f0'), 'd': H('b0485e'), 'v': H('ffe4ea'), 's': H('f0b8c6'), 'e': H('c8788e')}
FW, FH = 30, 32


def frame_edit(fr, d):
    p = fr.load()
    top = next(y for y in range(FH) if any(p[x, y][3] for x in range(FW)))
    xs = [x for x in range(FW) if p[x, top + 3][3]]
    x0, x1 = min(xs), max(xs)
    # veil first (so the wreath sits on it)
    def sheer(x, y, edge=False):
        if 0 <= x < FW and 0 <= y < FH:
            if p[x, y][3] == 0:
                p[x, y] = W['e'] if edge else W['v']
            elif p[x, y] != (0, 0, 0, 255):
                p[x, y] = mat.blend(p[x, y], (255, 228, 234), 0.5)
    if d == 3:      # up: veil covers the back of the head and falls to the hem
        for y in range(top + 5, top + 24):
            half = 4 + (y - top - 5) // 4
            cx = (x0 + x1) // 2
            for x in range(cx - half, cx + half + 1):
                sheer(x, y, edge=(x in (cx - half, cx + half)))
    elif d in (1, 2):   # side: veil trails behind
        back = 1 if d == 1 else -1
        bx = (x1 if d == 1 else x0)
        for y in range(top + 6, top + 24):
            for k in range(0, 3 + (y - top) // 8):
                x = bx - back * 2 + back * k
                sheer(x, y, edge=(k == 2 + (y - top) // 8))
    else:           # down: a little veil shows either side below the hair
        for y in range(top + 17, top + 23):
            sheer(x0 + 1, y, True); sheer(x0 + 2, y); sheer(x1 - 1, y, True); sheer(x1 - 2, y)
    # wreath: alternating blossoms over the crown
    pat = 'pwpdpwp'
    cx = (x0 + x1) // 2
    for i, ch in enumerate(pat):
        x = cx - 3 + i
        y = top + 2 + (1 if i in (0, 6) else 0)
        if 0 <= x < FW:
            p[x, y] = W[ch]
            if ch in 'pw' and i % 2 == 0:
                p[x, y - 1] = W['p'] if p[x, y - 1][3] else p[x, y - 1]
    return fr


def build():
    n, f = kb.native(kb.load(SRC))
    n = mat.recolour(n, HAIRMAP)
    out = Image.new('RGBA', n.size, CLEAR)
    for r in range(4):
        for c in range(4):
            fr = n.crop((c * FW, r * FH, (c + 1) * FW, (r + 1) * FH))
            out.paste(frame_edit(fr, r), (c * FW, r * FH))
    return out


if __name__ == '__main__':
    o = build()
    o.save(kb.WORK + '/passes/eb_ow_native.png')
    kb.up(o, 2).save(kb.WORK + '/juno/JUNO_everbloom_charset.png')
    kb.up(kb.on_bg(o, (120, 160, 110, 255)), 5).save(kb.WORK + '/sheets/eb_ow_5x.png')
