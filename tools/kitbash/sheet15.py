"""sheet15.py - art/previews/15_juno_portraits.png: pass-5 portraits vs composite A vs reference dialogue faces.
python3 -I tools/kitbash/sheet15.py"""
import sys, os, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, sheet09 as s
import juno_portraits_p5 as j5
from PIL import Image, ImageDraw

P = kb.WORK + '/passes'
EXPR = ['happy', 'surprised', 'sad', 'neutral', 'wink']
RJ = '/home/claude/ref/games/rejuvenation/Graphics/Transitions/'


def cell(sh, d, im96, x, y, lab, f10):
    sh.alpha_composite(s.stage(im96, 1, s.STAGE, 100, 100), (x, y))
    sh.alpha_composite(kb.up(kb.on_bg(im96, s.STAGE), 2), (x + 104, y))
    sh.alpha_composite(s.bubble(im96.convert('RGBA')), (x + 240, y + 74))
    d.text((x, y + 104), lab, font=f10, fill=s.DIM)


def main():
    W, H = 1880, 1090
    sh = Image.new('RGBA', (W, H), s.BG); d = ImageDraw.Draw(sh); f13, f10 = kb.font(13), kb.font(10)
    d.text((16, 10), 'JUNO portraits, pass 5: composite A rebuilt on a Rejuvenation VS-bust face (48-px art, 96x96 file). '
                     'Each: 1x, 2x, round bubble. Middle: pass-3 composite A (before). Bottom: the reference dialogue faces.',
           font=f10, fill=s.TXT)
    rows = [('pass 5 (new): happy / surprised / sad / neutral / wink', [(e, kb.up(j5.assemble(e), 2)) for e in EXPR]),
            ('before: composite A, pass 3', [(e, kb.up(Image.open(P + '/p3_A_%s_48.png' % e).convert('RGBA'), 2))
                                             for e in ['happy', 'surprised', 'sad', 'neutral']]),
            ('reference: Rejuvenation Faces/1, Desolation Faces/13, 16, 09a',
             [(n, kb.load(f)) for n, f in [('RJ 1', sorted(glob.glob('/home/claude/ref/games/rejuvenation/Graphics/Faces/1*.png'))[0])] +
              [('DS %s' % n, '/home/claude/ref/games/desolation/Graphics/Faces/%s.png' % n) for n in ('13', '16', '09a')]])]
    y = 34
    for lab, ims in rows:
        d.rectangle((16, y, W - 16, y + 238), fill=s.PANEL); d.text((24, y + 4), lab, font=f13, fill=s.ACC)
        for i, (n, im) in enumerate(ims):
            cell(sh, d, im, 24 + i * 368, y + 24, n, f10)
        y += 248
    # donors strip
    d.rectangle((16, y, W - 16, y + 300), fill=s.PANEL)
    d.text((24, y + 4), 'donors (Rejuvenation VS busts, 1:1 crops of the parts used)', font=f13, fill=s.ACC)
    don = [('vsTrainer150: face, eyes, fringe, collar', 'vsTrainer150', (72, 6, 168, 102)),
           ('vsTrainer143: big bloom (repainted)', 'vsTrainer143', (80, 0, 176, 96)),
           ('vsPlayer6_2: curl volume (left)', 'vsPlayer6_2', (70, 20, 166, 116)),
           ('vsTrainer159: open-beam mouth shape', 'vsTrainer159', (90, 20, 186, 116)),
           ('vsTrainer171: blossom + leaf colours', 'vsTrainer171', (130, 0, 226, 96))]
    for i, (lab, n, box) in enumerate(don):
        im = kb.load(RJ + n + '.png').crop(box)
        x = 24 + i * 300
        sh.alpha_composite(kb.up(kb.on_bg(im, s.STAGE), 2), (x, y + 26))
        d.text((x, y + 222 + 4), lab, font=f10, fill=s.DIM)
    d.text((24, y + 250), 'Hand pixels: the five mouths, the wink arc, sad lids/brows/tears, freckles, blush, wreath blossoms '
                          '(three shapes, bloom palette) and leaves.', font=f10, fill=s.TXT)
    sh.save(kb.GAME + '/art/previews/15_juno_portraits.png'); print(sh.size)


if __name__ == '__main__':
    main()
