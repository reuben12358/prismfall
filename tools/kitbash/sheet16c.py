"""sheet16c.py - art/previews/16c_juno_hair.png: per expression, pass 3 | middle ground | new step | hair fix (1x, 2x, bubble).
python3 -I tools/kitbash/sheet16c.py"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, sheet09 as s
from sheet16h import cell
from PIL import Image, ImageDraw

P = kb.WORK + '/passes'
EXPR = ['happy', 'surprised', 'sad', 'neutral']
COLS = [('pass 3', 'p3_A'), ('middle ground (16b)', 'p3m'), ('new step (installed)', 'p3q'), ('hair fix (16)', 'p3h')]

W, H = 1536, 34 + 4 * 252 + 10
sh = Image.new('RGBA', (W, H), s.BG); d = ImageDraw.Draw(sh); f13, f10 = kb.font(13), kb.font(10)
d.text((16, 10), 'JUNO hair, a step from the middle ground back toward pass 3: more of pass 3\'s lock divisions (dark brown, tapered), its outline with only the worst stair-steps removed, its two-tone blocks with a hint of the lock gradient; wreath band and crisp highlight arc kept. Each: 1x, 2x, bubble.', font=f10, fill=s.TXT)
for r, e in enumerate(EXPR):
    y = 34 + r * 252
    d.rectangle((16, y, W - 16, y + 244), fill=s.PANEL)
    for c, (lab, pre) in enumerate(COLS):
        x = 24 + c * 376
        d.text((x, y + 4), '%s - %s' % (e, lab), font=f13 if c == 2 else f10, fill=s.ACC if c == 2 else s.DIM)
        im = kb.up(Image.open('%s/%s_%s_48.png' % (P, pre, e)).convert('RGBA'), 2)
        cell(sh, im, x, y + 24)
sh.save(kb.GAME + '/art/previews/16c_juno_hair.png'); print(sh.size)
