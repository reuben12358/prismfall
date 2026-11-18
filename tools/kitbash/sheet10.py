"""sheet10.py - pass-2 review sheet (art/previews/10_juno_kitbash_pass2.png) + pass-2 exports (*_p2). Pass-1 files untouched."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, sheet09 as s
from PIL import Image
s.OUTSHEET = kb.GAME + '/art/previews/10_juno_kitbash_pass2.png'
s.FINAL = [
    ('v1_p2.png', 'JUNO_v1_underglass_p2', '1  UNDER GLASS  pass 2', s.FINAL[0][3],
     s.FINAL[0][4] + [('sd:sonia', 'curled ponytail (flipped)')], 'hand-built: brass frame, glass tints, harness band, cast shadow'),
    ('v2_p2.png', 'JUNO_v2_everbloom_p2', '2  EVER-BLOOM  pass 2', s.FINAL[1][3], s.FINAL[1][4],
     'veil = two tail lengths, 50% see-through over hair; 3 blossoms'),
    ('v3_p2.png', 'JUNO_v3_rotbloom_p2', '3  ROT & BLOOM  pass 2', s.FINAL[2][3],
     [('sd:parasollady', 'body, pose, handle'), ('sd:lass', 'head, hair, laugh'), ('B:shiinotic', 'cap / parasol')], s.FINAL[2][5]),
]
s.CELL = 62
s.PNOTES = ['base: Desolation Faces/08a, brows from 08e, open grin (teeth + lip) from Faces/13;', 'repaint: auburn hair, green irises, knit collar + harness strap;', 'hand: ponytail tie, 6 freckles, carved crown corner']
_open = Image.open
def _o(p, *a, **k):
    return _open(p.replace('JUNO_portrait_native48', 'JUNO_portrait_p2_native48'), *a, **k)
Image.open = _o
_exp = s.export
def export():
    for src, name, *_ in s.FINAL:
        im = _open(os.path.join(s.P, src)).convert('RGBA')
        im.save(os.path.join(s.J, name + '_native80.png')); kb.up(im, 2).save(os.path.join(s.J, name + '.png'))
s.export = export
s.main()
