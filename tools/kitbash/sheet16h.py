"""sheet16h.py - art/previews/16_juno_hair_fix.png: pass-3 portraits before/after the hair fix, 1x, 2x, bubble.
python3 -I tools/kitbash/sheet16h.py"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, sheet09 as s
from PIL import Image, ImageDraw

P = kb.WORK + '/passes'
EXPR = ['happy', 'surprised', 'sad', 'neutral']


def cell(sh, im96, x, y):
    sh.alpha_composite(s.stage(im96, 1, s.STAGE, 100, 100), (x, y))
    sh.alpha_composite(kb.up(kb.on_bg(im96, s.STAGE), 2), (x + 104, y))
    sh.alpha_composite(s.bubble(im96.convert('RGBA')), (x + 240, y + 74))


def main():
    W, H = 1520, 560
    sh = Image.new('RGBA', (W, H), s.BG); d = ImageDraw.Draw(sh); f13, f10 = kb.font(13), kb.font(10)
    d.text((16, 10), 'JUNO pass-3 portraits, HAIR FIX only (face, eyes, mouths, freckles, wreath, bloom, veil unchanged). '
                     'Top: before (installed). Bottom: after. Each: 1x, 2x, bubble.', font=f10, fill=s.TXT)
    for r, (lab, pre) in enumerate([('before: pass 3 as installed', 'p3_A'), ('after: hair redrawn as flowing locks', 'p3h')]):
        y = 34 + r * 262
        d.rectangle((16, y, W - 16, y + 252), fill=s.PANEL); d.text((24, y + 4), lab, font=f13, fill=s.ACC)
        for i, e in enumerate(EXPR):
            im = kb.up(Image.open('%s/%s_%s_48.png' % (P, pre, e)).convert('RGBA'), 2)
            cell(sh, im, 24 + i * 372, y + 26)
            d.text((24 + i * 372, y + 230), e, font=f10, fill=s.DIM)
    sh.save(kb.GAME + '/art/previews/16_juno_hair_fix.png'); print(sh.size)


if __name__ == '__main__':
    main()
