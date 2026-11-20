"""sheet16b.py - art/previews/16b_juno_hair_middle.png: per expression, pass 3 | hair fix | middle ground (1x, 2x, bubble).
python3 -I tools/kitbash/sheet16b.py"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, sheet09 as s
from sheet16h import cell
from PIL import Image, ImageDraw

P = kb.WORK + '/passes'
EXPR = ['happy', 'surprised', 'sad', 'neutral']
COLS = [('pass 3 (before)', 'p3_A'), ('hair fix (16)', 'p3h'), ('middle ground (installed)', 'p3m')]

W, H = 1160, 34 + 4 * 252 + 10
sh = Image.new('RGBA', (W, H), s.BG); d = ImageDraw.Draw(sh); f13, f10 = kb.font(13), kb.font(10)
d.text((16, 10), 'JUNO hair, middle ground: the fix\'s flowing-lock shading and smooth silhouette + pass 3\'s lock divisions and wreath band '
                 'as dark-brown tapered contours + one crisp highlight band. Each: 1x, 2x, bubble.', font=f10, fill=s.TXT)
for r, e in enumerate(EXPR):
    y = 34 + r * 252
    d.rectangle((16, y, W - 16, y + 244), fill=s.PANEL)
    for c, (lab, pre) in enumerate(COLS):
        x = 24 + c * 376
        d.text((x, y + 4), '%s - %s' % (e, lab), font=f13 if c == 2 else f10, fill=s.ACC if c == 2 else s.DIM)
        im = kb.up(Image.open('%s/%s_%s_48.png' % (P, pre, e)).convert('RGBA'), 2)
        cell(sh, im, x, y + 24)
sh.save(kb.GAME + '/art/previews/16b_juno_hair_middle.png'); print(sh.size)
