"""sheet12.py - art/previews/12_juno_everbloom_p2.png + pass-2 Ever-Bloom exports. python3 -I tools/kitbash/sheet12.py"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, show, sheet09 as s
from PIL import Image, ImageDraw
P, J = kb.WORK + '/passes', kb.WORK + '/juno'
K = '/home/claude/run_juno/captures_keep/'
pick = Image.open(P + '/eb_P2.png').convert('RGBA')
pick.save(J + '/JUNO_everbloom_p2_native80.png'); kb.up(pick, 2).save(J + '/JUNO_everbloom_p2.png')
W, H = 1960, 1240
sh = Image.new('RGBA', (W, H), s.BG); d = ImageDraw.Draw(sh)
f16, f13, f10 = kb.font(17), kb.font(13), kb.font(10)
d.text((16, 10), 'JUNO HALE - EVER-BLOOM pass 2: front (cloth train, deeper veil), new portrait donor, 128x192 charset, engine frames.', font=f13, fill=s.TXT)
d.rectangle((16, 40, 1130, 600), fill=s.PANEL); d.text((26, 46), 'front, pass 2 (4x / 2x / 1x)  |  arm-graft try (rejected)  |  pass 1', font=f16, fill=s.ACC)
sh.alpha_composite(s.stage(pick, 4, s.STAGE, 344, 324), (24, 72))
sh.alpha_composite(s.stage(pick, 2, s.STAGE, 168, 172), (24, 404)); sh.alpha_composite(s.stage(pick, 1, s.BATTLE, 168, 172), (200, 404))
for i, (f, lab) in enumerate([('eb_P2arm.png', 'tried: Parasol Lady arm + drifting blossoms. Join is muddy: rejected'), ('eb_A.png', 'pass 1 (ribbon train, paler veil)')]):
    im = Image.open(P + '/' + f).convert('RGBA'); x = 390 + i * 370
    sh.alpha_composite(s.stage(im, 4, s.STAGE, 344, 324), (x, 72)); sh.alpha_composite(s.stage(im, 1, s.BATTLE, 344, 100), (x, 404)); d.text((x, 510), lab, font=f10, fill=s.TXT)
d.rectangle((1144, 40, 1944, 600), fill=s.PANEL); d.text((1154, 46), 'references (2x, 1x)', font=f13, fill=s.ACC)
rx = 1152
for spec, lab in s.REFS:
    n, f = show.get_native(spec)
    sh.alpha_composite(s.stage(n, 2, s.STAGE, 196, 196), (rx, 72)); sh.alpha_composite(s.stage(n, 1, s.BATTLE, 196, 100), (rx, 272)); d.text((rx + 2, 376), lab, font=f10, fill=s.DIM); rx += 204
sh.alpha_composite(s.stage(pick, 2, s.STAGE, 180, 196), (rx, 72)); sh.alpha_composite(s.stage(pick, 1, s.BATTLE, 180, 100), (rx, 272))
d.rectangle((16, 612, 1130, 1224), fill=s.PANEL); d.text((26, 618), 'bubble portraits, pass 2 (B2W2 Burgh VS bust, 48-px crop) - 4x, 1x, bubble', font=f13, fill=s.ACC)
for i, e in enumerate(['happy', 'surprised', 'sad', 'neutral']):
    p96 = kb.up(Image.open(P + '/eb_portrait_p2_%s_48.png' % e).convert('RGBA'), 2); x = 26 + i * 276
    sh.alpha_composite(s.stage(p96, 2, s.STAGE, 200, 200), (x, 644)); sh.alpha_composite(s.stage(p96, 1, s.STAGE, 100, 100), (x, 852))
    sh.alpha_composite(s.bubble(p96), (x + 110, 846)); d.text((x, 958), e, font=f13, fill=s.TXT)
ow = Image.open(P + '/eb_ow_p2_native.png').convert('RGBA')
d.text((26, 986), 'overworld charset, pass 2 (16x24 frames, file 128x192; 3x)', font=f13, fill=s.ACC)
sh.alpha_composite(s.stage(ow, 2, s.BATTLE, 140, 200), (26, 1008)); sh.alpha_composite(s.stage(ow.crop((0, 0, 64, 48)), 4, s.BATTLE, 270, 200), (176, 1008)); sh.alpha_composite(s.stage(ow.crop((0, 48, 64, 96)), 4, s.BATTLE, 270, 200), (456, 1008))
d.rectangle((1144, 612, 1944, 1224), fill=s.PANEL); d.text((1154, 618), 'real engine frames (mkxp-z + EBDX): battle intro, portrait bubbles in dialogue', font=f13, fill=s.ACC)
for i, (f, crop) in enumerate([('juno/f00024.bmp', None), ('junoow/f00079.bmp', None), ('junoow/f00109.bmp', None), ('junoow/f00124.bmp', None)]):
    if os.path.exists(K + f):
        e = Image.open(K + f).convert('RGBA'); e.save(kb.GAME + '/art/previews/12_engine_%d.png' % i)
        sh.alpha_composite(e.resize((384, 288), Image.NEAREST), (1152 + (i % 2) * 392, 644 + (i // 2) * 292))
sh.save(kb.GAME + '/art/previews/12_juno_everbloom_p2.png'); print(sh.size)
