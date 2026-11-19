"""sheet11.py - art/previews/11_juno_everbloom.png + final Ever-Bloom exports. python3 -I tools/kitbash/sheet11.py"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, show, sheet09 as s
from PIL import Image, ImageDraw
P, J = kb.WORK + '/passes', kb.WORK + '/juno'
ENG = '/home/claude/run_juno/captures_keep/juno/f00032.bmp'
pick = Image.open(P + '/eb_A.png').convert('RGBA')
pick.save(J + '/JUNO_everbloom_native80.png'); kb.up(pick, 2).save(J + '/JUNO_everbloom.png')
W, H = 1960, 1180
sh = Image.new('RGBA', (W, H), s.BG); d = ImageDraw.Draw(sh)
f16, f13, f11, f10 = kb.font(17), kb.font(13), kb.font(11), kb.font(10)
d.text((16, 10), 'JUNO HALE - EVER-BLOOM, finished pass. 80-px art, file 160x160, shown by EBDX at scale 1 (see engine capture).', font=f13, fill=s.TXT)
# pick, big
d.rectangle((16, 40, 376, 600), fill=s.PANEL)
d.text((26, 46), 'PICK: A   (4x)', font=f16, fill=s.ACC)
sh.alpha_composite(s.stage(pick, 4, s.STAGE, 344, 324), (24, 70))
sh.alpha_composite(s.stage(pick, 2, s.STAGE, 168, 172), (24, 400)); sh.alpha_composite(s.stage(pick, 1, s.BATTLE, 168, 172), (200, 400))
s.wrap(d, "A cheerful girl in the blossoms of a wedding that never ended: laughing face, the Bride Tree's wreath, a veil that will not wilt.", (26, 580 - 2), 340, f11, s.TXT)
# variants
d.rectangle((390, 40, 1130, 600), fill=s.PANEL)
d.text((400, 46), 'variations (3x)', font=f16, fill=s.ACC)
for i, (k, note) in enumerate([('A', 'A  PICK: Lass head (laugh), cloth veil from Diantha cape + floor train'),
                               ('B', 'B: Lady head (calm smile), same veil'), ('C', 'C: Lass head, veil from two tail lengths (pass-2 style)')]):
    im = Image.open(P + '/eb_%s.png' % k).convert('RGBA')
    x = 398 + i * 244
    sh.alpha_composite(s.stage(im, 3, s.STAGE, 240, 250), (x, 72))
    sh.alpha_composite(s.stage(im, 1, s.BATTLE, 240, 96), (x, 326))
    s.wrap(d, note, (x + 2, 428), 232, f10, s.ACC if k == 'A' else s.TXT)
# donors
dx = 400
d.text((400, 476), 'donors used (A)', font=f11, fill=s.ACC)
for spec, part in [('sd:lady', 'body, gown, back hair'), ('sd:lass', 'head, laugh, hair'), ('sd:diantha', 'cape -> veil'), ('sd:miku-flying', 'tail -> train'), ('B:comfey', 'blooms')]:
    dn = s.donor_img(spec)
    sh.alpha_composite(s.stage(dn, 1, s.STAGE, 84, 86), (dx, 492)); d.text((dx, 580), part, font=f10, fill=s.TXT); dx += 90
# refs
d.rectangle((1144, 40, 1944, 600), fill=s.PANEL); d.text((1154, 46), 'references (2x, 1x)', font=f13, fill=s.ACC)
rx = 1152
for spec, lab in s.REFS:
    n, f = show.get_native(spec)
    sh.alpha_composite(s.stage(n, 2, s.STAGE, 196, 196), (rx, 72)); sh.alpha_composite(s.stage(n, 1, s.BATTLE, 196, 100), (rx, 272))
    d.text((rx + 2, 376), lab, font=f10, fill=s.DIM); rx += 204
sh.alpha_composite(s.stage(pick, 2, s.STAGE, 180, 196), (rx, 72)); sh.alpha_composite(s.stage(pick, 1, s.BATTLE, 180, 100), (rx, 272)); d.text((rx + 2, 376), 'Juno A', font=f10, fill=s.ACC)
# portraits
d.rectangle((16, 612, 1130, 1164), fill=s.PANEL); d.text((26, 618), 'bubble portraits (96x96 files; 1x, 3x)  -  Desolation Faces/08 set + Faces/13 grin', font=f13, fill=s.ACC)
for i, e in enumerate(['happy', 'surprised', 'sad', 'neutral']):
    p96 = kb.up(Image.open(P + '/eb_portrait_%s_48.png' % e).convert('RGBA'), 2)
    x = 26 + i * 276
    sh.alpha_composite(s.stage(p96, 2, s.STAGE, 200, 200), (x, 644)); sh.alpha_composite(s.stage(p96, 1, s.STAGE, 100, 100), (x, 852))
    sh.alpha_composite(s.bubble(p96), (x + 110, 846)); d.text((x, 958), e, font=f11, fill=s.TXT)
# charset
ow = Image.open(P + '/eb_ow_native.png').convert('RGBA')
d.rectangle((1144, 612, 1944, 1164), fill=s.PANEL); d.text((1154, 618), 'overworld charset (4x4, 3x)  +  real EBDX battle intro (mkxp-z)', font=f13, fill=s.ACC)
sh.alpha_composite(s.stage(ow, 3, s.BATTLE, 372, 392), (1152, 644))
if os.path.exists(ENG):
    e = Image.open(ENG).convert('RGBA'); e.save(kb.GAME + '/art/previews/11_juno_everbloom_engine.png')
    sh.alpha_composite(e.resize((384, 288), Image.NEAREST) if False else e.crop((128, 0, 512, 384)), (1536, 644))
sh.save(kb.GAME + '/art/previews/11_juno_everbloom.png'); print(sh.size)
