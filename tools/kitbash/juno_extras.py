"""Juno extras on the installed portrait style (p3k = pass 3 + hair work + closed crown):
  - the faint tan band across the eye line removed (the old visor shadow, d8a078 between the eyes)
  - WINK: happy face with her left eye (viewer's right) shut in a thick B2W2-style arc
  - SHOCKED: surprised face pushed: pin-prick pupils in white eyes, a big open mouth with teeth and tongue
Only face pixels inside the eye/mouth boxes change. Not installed (for the user to choose).
python3 -I tools/kitbash/juno_extras.py ; sheet: art/previews/16f_juno_extras.png"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, mat, sheet09 as s
from mat import H, CLEAR, BLACK
from PIL import Image, ImageDraw

P, J = kb.WORK + '/passes', kb.WORK + '/juno'
SKIN, TAN = H('f8d0b8'), H('d8a078')
GREENS = (H('48a060'), H('8ed07a'), H('1e5a3c'))
XP = {'k': BLACK, 's': SKIN, 'm': H('983840'), 'd': H('702838'), 'p': H('e06880'), 'w': H('f8f8f8'), 'g': H('1e5a3c'),
      'G': H('48a060'), 'b': H('e49d8c')}


def no_band(im):
    p = im.load()
    for y in range(28, 31):
        for x in range(20, 32):
            if p[x, y] == TAN:
                p[x, y] = SKIN
    return im


def wink(im):
    p = im.load()
    for y in range(24, 34):
        for x in range(30, 38):
            if p[x, y] != BLACK or y >= 25:
                p[x, y] = SKIN
    # restore the face outline just right of the eye if it was there in the source
    return mat.patch(im, 30, 26, ['..kkkk..',
                                  '.kkkkkk.',
                                  'kk....kk',
                                  'k......k',
                                  '........',
                                  '.b.b.b..'], XP)


def shocked(im):
    p = im.load()
    for (x0, x1, cx, y1) in ((16, 21, 18, 31), (31, 38, 33, 33)):
        for y in range(26, y1):
            for x in range(x0, x1):
                if p[x, y] in GREENS or (p[x, y] == BLACK and x0 < x < x1 - 1):
                    p[x, y] = H('e8e8f8')
        im = mat.patch(im, cx, 27, ['kg', 'gk'], XP)       # pin-prick pupils
        p = im.load()
    for y in range(34, 41):
        for x in range(24, 32):
            if p[x, y] in (H('983840'), H('702838'), H('e06880'), BLACK, H('c0506e')):
                p[x, y] = SKIN
    return mat.patch(im, 24, 34, ['..kkkk..',
                                  '.kwwwwk.',
                                  'kddddddk',
                                  'kddddddk',
                                  'kddppddk',
                                  '.kppppk.',
                                  '..kkkk..'], XP)


def main():
    outs = {}
    for e in ['happy', 'surprised', 'sad', 'neutral']:
        im = no_band(Image.open(P + '/p3k_%s_48.png' % e).convert('RGBA'))
        outs[e] = im
    outs['wink'] = wink(outs['happy'].copy())
    outs['shocked'] = shocked(outs['surprised'].copy())
    for e, im in outs.items():
        im.save(P + '/p3x_%s_48.png' % e)
        kb.up(im, 2).save(J + '/JUNO_%s_p3x.png' % e)
    # sheet: installed (top) vs extras (bottom)
    cols = ['happy', 'surprised', 'sad', 'neutral', 'wink', 'shocked']
    W, Hh = 24 + 6 * 310, 560
    sh = Image.new('RGBA', (W, Hh), s.BG); d = ImageDraw.Draw(sh); f13, f10 = kb.font(13), kb.font(10)
    d.text((16, 10), 'JUNO extras on the installed style: tan band across the eye line removed (all), new WINK and a proper SHOCKED. '
                     'Top: installed now. Bottom: proposed (not installed). Each: 1x, 2x, bubble.', font=f10, fill=s.TXT)
    for r, (lab, src) in enumerate([('installed now', 'p3k'), ('proposed', 'p3x')]):
        y = 34 + r * 262
        d.rectangle((16, y, W - 16, y + 252), fill=s.PANEL); d.text((24, y + 4), lab, font=f13, fill=s.ACC if r else s.DIM)
        for i, e in enumerate(cols):
            f = '%s/%s_%s_48.png' % (P, src, e)
            if not os.path.exists(f):
                continue
            im96 = kb.up(Image.open(f).convert('RGBA'), 2)
            x = 24 + i * 310
            sh.alpha_composite(s.stage(im96, 1, s.STAGE, 100, 100), (x, y + 26))
            sh.alpha_composite(kb.up(kb.on_bg(im96, s.STAGE), 2), (x + 104, y + 26))
            sh.alpha_composite(s.bubble(im96), (x - 4, y + 128))
            d.text((x, y + 236), e, font=f10, fill=s.DIM)
    sh.save(kb.GAME + '/art/previews/16f_juno_extras.png'); print(sh.size)


if __name__ == '__main__':
    main()
