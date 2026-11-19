"""Juno portraits, PASS 4: sprite busts. Head and shoulders cropped from her own Ever-Bloom front (80-px art),
32x32 crop x3 = 96x96. happy = Lass head (as on the front), neutral = Lady head, surprised/sad = few-pixel face
patches at sprite scale. python3 -I tools/kitbash/juno_portraits_p4.py"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, mat, juno_everbloom_p2 as e
from mat import H, BLACK
from PIL import Image
J, P = kb.WORK + '/juno', kb.WORK + '/passes'
BOX = (18, 0, 50, 32)
SK = (248, 208, 184, 255)
X = {'m': H('983840'), 'k': BLACK, 's': SK, 't': H('9ad8f0')}


def build(expr):
    im = e.build(False, ribbon=True, head='lady' if expr == 'neutral' else 'lass')
    if expr in ('surprised', 'sad'):
        p = im.load()
        for y in range(22, 26):
            for x in range(29, 35):
                c = p[x, y]
                if c[0] > 180 and c[1] < 110:        # the laugh's reds
                    p[x, y] = SK
        if expr == 'surprised':
            im = mat.patch(im, 31, 23, ['mm', 'mm'], X)
            im = mat.patch(im, 26, 17, ['kk'], X)
        else:
            im = mat.patch(im, 30, 24, ['.mm.', 'm..m'], X)
            im = mat.patch(im, 28, 21, ['t', 't'], X)
    return im.crop(BOX)


if __name__ == '__main__':
    items = []
    for ex in ['happy', 'surprised', 'sad', 'neutral']:
        b = build(ex); b.save(P + '/p4_%s_32.png' % ex); kb.up(b, 3).save(J + '/JUNO_%s_p4.png' % ex)
        items.append((ex, kb.on_bg(kb.up(b, 3), (236, 232, 222, 255))))
    kb.contact(items, 4, (98 * 3, 98 * 3), k=3, fs=11).save(kb.WORK + '/sheets/p4_busts_out.png')
