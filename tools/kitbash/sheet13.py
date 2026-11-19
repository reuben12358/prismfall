"""sheet13.py - art/previews/13_juno_portraits.png. python3 -I tools/kitbash/sheet13.py"""
import sys, os, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, sheet09 as s
from PIL import Image, ImageDraw
P, J = kb.WORK + '/passes', kb.WORK + '/juno'
V = '/home/claude/ref/art/sprites_gen5_vs_tech/extracted/Gen 5 VS Sprites/vsTrainer_'
W, H = 1960, 1150
sh = Image.new('RGBA', (W, H), s.BG); d = ImageDraw.Draw(sh); f16, f13, f10 = kb.font(17), kb.font(13), kb.font(10)
d.text((16, 10), 'JUNO portraits, pass 3: composite faces, no single donor. Top: three candidates (1x / 3x / bubble) + donors. Middle: the pick in four expressions. Right: comparisons, front, engine.', font=f13, fill=s.TXT)
def bust(n, box): return kb.native(kb.load(V + n + '.png'))[0].crop(box)
C = [('A  PICK', 'p3_cand_A_48.png', [('POKEMONTRAINER_Rosa', (40, 2, 88, 50), 'face, fringe, crown'), ('POKEMONTRAINER_Hilda', (8, 0, 56, 48), 'wavy hair mass')], 'hand: smile, brows, freckles, tears; wreath = Comfey bloom + stamps'),
     ('B  (rough)', 'p3_cand_B_48.png', [('POKEMONTRAINER_Hilda', (32, 0, 80, 48), 'face, crown'), ('ELITEFOUR_Caitlin', (30, 6, 78, 54), 'wavy hair')], 'crown still reads as a cap: rejected'),
     ('C  (rough)', 'p3_cand_C_48.png', [('LEADER_Skyla', (38, 4, 86, 52), 'face, own open smile'), ('ELITEFOUR_Caitlin', (30, 6, 78, 54), 'hair'), ('POKEMONTRAINER_Hilda', (8, 0, 56, 48), 'hair mass')], 'liveliest, but holes at the neck and still reads as Skyla: rejected')]
for i, (t, f, dons, note) in enumerate(C):
    x = 16 + i * 440; d.rectangle((x, 40, x + 428, 400), fill=s.PANEL); d.text((x + 8, 46), t, font=f16, fill=s.ACC)
    p96 = kb.up(Image.open(P + '/' + f).convert('RGBA'), 2)
    sh.alpha_composite(s.stage(p96, 1, s.STAGE, 100, 100), (x + 8, 72)); sh.alpha_composite(s.stage(p96, 2, s.STAGE, 196, 196), (x + 114, 72)); sh.alpha_composite(s.bubble(p96), (x + 300, 72))
    dx = x + 8
    for n, box, part in dons:
        sh.alpha_composite(s.stage(bust(n, box), 2, s.STAGE, 100, 100), (dx, 276)); d.text((dx, 378), part, font=f10, fill=s.TXT); dx += 106
    s.wrap(d, note, (x + 300, 200), 124, f10, s.DIM)
d.rectangle((16, 412, 1324, 1134), fill=s.PANEL); d.text((24, 418), 'pick A: happy / surprised / sad / neutral  (4x, 1x, bubble)', font=f16, fill=s.ACC)
for i, e in enumerate(['happy', 'surprised', 'sad', 'neutral']):
    p96 = kb.up(Image.open(P + '/p3_A_%s_48.png' % e).convert('RGBA'), 2); x = 28 + i * 324
    sh.alpha_composite(s.stage(p96, 3, s.STAGE, 292, 292), (x, 446)); sh.alpha_composite(s.stage(p96, 1, s.STAGE, 100, 100), (x, 744)); sh.alpha_composite(s.bubble(p96), (x + 110, 740)); d.text((x, 850), e, font=f13, fill=s.TXT)
d.text((28, 880), 'comparison portraits (3x): Bianca (official B2W2 bust crop), Rejuvenation Faces, Desolation Faces', font=f13, fill=s.ACC)
cmp = [bust('POKEMONTRAINER_Bianca', (36, 4, 84, 52)), kb.native(kb.load(sorted(glob.glob('/home/claude/ref/games/rejuvenation/Graphics/Faces/1*.png'))[0]))[0], kb.native(kb.load('/home/claude/ref/games/desolation/Graphics/Faces/13.png'))[0], Image.open(P + '/p3_A_happy_48.png').convert('RGBA')]
for i, c in enumerate(cmp):
    sh.alpha_composite(s.stage(kb.up(c, 2), 2, s.STAGE, 200, 200), (28 + i * 212, 904))
d.rectangle((1336, 40, 1944, 1134), fill=s.PANEL); d.text((1346, 46), 'front, pass 3: ribbon train, deeper pink + rose outline (4x, 1x)', font=f13, fill=s.ACC)
fr = Image.open(P + '/eb_P3.png').convert('RGBA'); fr.save(J + '/JUNO_everbloom_p3_native80.png'); kb.up(fr, 2).save(J + '/JUNO_everbloom_p3.png')
sh.alpha_composite(s.stage(fr, 4, s.STAGE, 344, 324), (1346, 70)); sh.alpha_composite(s.stage(fr, 1, s.BATTLE, 240, 324), (1696, 70))
d.text((1346, 404), 'engine (mkxp-z): pick A in a dialogue bubble; charset loads as the walker, map tiles did not render', font=f10, fill=s.TXT)
for i, f in enumerate(['f00078.bmp', 'f00097.bmp']):
    pth = '/home/claude/run_juno/captures_keep/junoow/' + f
    if os.path.exists(pth):
        e = Image.open(pth).convert('RGBA'); e.save(kb.GAME + '/art/previews/13_engine_%d.png' % i); sh.alpha_composite(e.crop((0, 100, 512, 384)), (1346 + 44, 424 + i * 296))
sh.save(kb.GAME + '/art/previews/13_juno_portraits.png'); print(sh.size)
