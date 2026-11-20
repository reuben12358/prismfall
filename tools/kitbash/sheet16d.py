"""sheet16d.py - art/previews/16d_juno_hair.png: per expression, pass 3 | step (16c) | combined (1x, 2x, bubble).
python3 -I tools/kitbash/sheet16d.py"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, sheet09 as s
from sheet16h import cell
from PIL import Image, ImageDraw

P = kb.WORK + '/passes'
EXPR = ['happy', 'surprised', 'sad', 'neutral']
COLS = [('pass 3', 'p3_A'), ('step (16c)', 'p3q'), ('combined (installed)', 'p3c')]

W, H = 1160, 34 + 4 * 252 + 10
sh = Image.new('RGBA', (W, H), s.BG); d = ImageDraw.Draw(sh); f13, f10 = kb.font(13), kb.font(10)
d.text((16, 10), 'JUNO hair, combined: pass 3 exactly below the eye line (side locks, long hair), the 16c step above it (dome, fringe, wreath band, highlight); seam rows matched. Each: 1x, 2x, bubble.', font=f10, fill=s.TXT)
for r, e in enumerate(EXPR):
    y = 34 + r * 252
    d.rectangle((16, y, W - 16, y + 244), fill=s.PANEL)
    for c, (lab, pre) in enumerate(COLS):
        x = 24 + c * 376
        d.text((x, y + 4), '%s - %s' % (e, lab), font=f13 if c == 2 else f10, fill=s.ACC if c == 2 else s.DIM)
        im = kb.up(Image.open('%s/%s_%s_48.png' % (P, pre, e)).convert('RGBA'), 2)
        cell(sh, im, x, y + 24)
sh.save(kb.GAME + '/art/previews/16d_juno_hair.png'); print(sh.size)
