"""sheet14.py - art/previews/14_juno_portraits.png: sprite-bust portraits vs composite A vs reference faces."""
import sys, os, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, sheet09 as s
from PIL import Image, ImageDraw
P = kb.WORK + '/passes'
sh = Image.new('RGBA', (1500, 760), s.BG); d = ImageDraw.Draw(sh); f13, f10 = kb.font(13), kb.font(10)
d.text((16, 10), 'JUNO portraits, pass 4. Rows: sprite busts (her own front, 32-px crop x3) | composite A (pass 3, 48-px x2) | references (Rejuvenation Faces/1, Desolation Faces/13, 16, 09a). Each: 96x96 file at 1x, 2x, and in the bubble.', font=f10, fill=s.TXT)
rows = [('sprite bust', [kb.up(Image.open(P + '/p4_%s_32.png' % e).convert('RGBA'), 3) for e in ['happy', 'surprised', 'sad', 'neutral']]),
        ('composite A', [kb.up(Image.open(P + '/p3_A_%s_48.png' % e).convert('RGBA'), 2) for e in ['happy', 'surprised', 'sad', 'neutral']]),
        ('reference', [kb.load(f) for f in [sorted(glob.glob('/home/claude/ref/games/rejuvenation/Graphics/Faces/1*.png'))[0]] + ['/home/claude/ref/games/desolation/Graphics/Faces/%s.png' % n for n in ('13', '16', '09a')]])]
for r, (lab, ims) in enumerate(rows):
    y = 40 + r * 236; d.rectangle((16, y, 1484, y + 226), fill=s.PANEL); d.text((24, y + 4), lab, font=f13, fill=s.ACC)
    for i, im in enumerate(ims):
        x = 24 + i * 364
        sh.alpha_composite(s.stage(im, 1, s.STAGE, 100, 100), (x, y + 26)); sh.alpha_composite(s.stage(im, 2, s.STAGE, 196, 196), (x + 104, y + 26)) if False else None
        sh.alpha_composite(kb.up(kb.on_bg(im, s.STAGE), 2).resize((192, 192), Image.NEAREST), (x + 104, y + 26)); sh.alpha_composite(s.bubble(im.convert('RGBA'), r=28) if False else s.bubble(im.convert('RGBA')), (x - 6, y + 104) if False else (x + 300 - 60, y + 100))
sh.save(kb.GAME + '/art/previews/14_juno_portraits.png'); print(sh.size)
