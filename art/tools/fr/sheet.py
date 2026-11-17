"""Style-check sheet: frankensprites beside stock at 1x and 4x."""
import numpy as np
from PIL import Image, ImageDraw
from fs import load, REF_T, REF_C
import pc_a, pc_b, larch, ow_fr
from render_busts import build, disc
from exprs import EXPRS
P = '/home/claude/fangame/art/previews/fr/'
BG = (120, 140, 150, 255)


def label(im, text):
    d = ImageDraw.Draw(im); d.rectangle([0, 0, len(text) * 6 + 6, 12], fill=(30, 30, 40, 255)); d.text((3, 1), text, fill=(240, 240, 240, 255))


def strip(arrs, S, gap=8, bottom=True):
    ims = [Image.fromarray(a.astype(np.uint8)) for a in arrs]
    W = sum(i.width * S + gap for i in ims); H = max(i.height for i in ims) * S
    sh = Image.new('RGBA', (W, H), BG); x = 0
    for i in ims:
        sh.alpha_composite(i.resize((i.width * S, i.height * S), Image.NEAREST), (x, H - i.height * S if bottom else 0)); x += i.width * S + gap
    return sh


def main(out):
    ours = [pc_a.build(), pc_b.build(), larch.build()]
    stock = [load(REF_T + n + '.png') for n in ('RIVAL1', 'LEADER_Misty', 'LASS')]
    ow_ours = [ow_fr.player_a(), ow_fr.player_b(), ow_fr.larch()]
    ow_stock = [load(REF_C + n + '.png') for n in ('trainer_RIVAL1', 'trainer_LASS')]
    parts = []
    a = strip(stock + ours, 1, 12); label(a, 'BATTLE 1x: stock RIVAL1, Misty, Lass | ours PLAYER_A, PLAYER_B, LARCH'); parts.append(a)
    b = strip(stock + ours, 4, 8); label(b, 'BATTLE 4x'); parts.append(b)
    c = strip(ow_stock + ow_ours, 1, 12, False); label(c, 'OVERWORLD 1x: stock x2 | ours'); parts.append(c)
    d = strip(ow_stock + ow_ours, 3, 10, False); label(d, 'OVERWORLD 3x'); parts.append(d)
    for cid, ex in (('PLAYER_A', EXPRS), ('PLAYER_B', EXPRS), ('LARCH', EXPRS)):
        row = Image.new('RGBA', (len(ex) * 196 + 10 * 100, 196), (60, 64, 76, 255))
        for i, e in enumerate(ex):
            row.alpha_composite(disc(build(cid, e), e, 2), (i * 196, 0))
        for i, e in enumerate(ex):
            row.alpha_composite(disc(build(cid, e), e, 1), (len(ex) * 196 + i * 100, 50))
        label(row, f'PORTRAITS {cid} (2x, then 1x)'); parts.append(row)
    W = max(p.width for p in parts); H = sum(p.height + 10 for p in parts)
    sh = Image.new('RGBA', (W, H), (90, 100, 110, 255)); y = 0
    for p in parts:
        sh.alpha_composite(p, (0, y)); y += p.height + 10
    sh.save(out)
    return sh.size


def main03(out):
    import batch2
    stock = [load(REF_T + n + '.png') for n in ('RIVAL1', 'ELITEFOUR_Lance', 'POKEMONTRAINER_May')]
    ours = [batch2.kestrel(), batch2.juno(), pc_a.build(), pc_b.build(), larch.build()]
    parts = []
    a = strip(stock + ours, 1, 12); label(a, 'BATTLE 1x: stock RIVAL1, Lance, May | ours KESTREL, JUNO (+ PLAYER_A, PLAYER_B, LARCH for poses)'); parts.append(a)
    b = strip(stock + ours, 4, 8); label(b, 'BATTLE 4x'); parts.append(b)
    ow_stock = [load(REF_C + n + '.png') for n in ('trainer_RIVAL1', 'trainer_ELITEFOUR_Lance', 'trainer_POKEMONTRAINER_May')]
    ow_ours = [batch2.kestrel_ow(), batch2.juno_ow()]
    c = strip(ow_stock + ow_ours, 1, 12, False); label(c, 'OVERWORLD 1x: stock x3 | ours KESTREL, JUNO'); parts.append(c)
    d = strip(ow_stock + ow_ours, 3, 10, False); label(d, 'OVERWORLD 3x'); parts.append(d)
    backs = [batch2.back_a(), batch2.back_b(), load(REF_T + 'POKEMONTRAINER_Brendan_back.png'), load(REF_T + 'POKEMONTRAINER_May_back.png')]
    for arr, name in zip(backs, ('PLAYER_A_back (ours)', 'PLAYER_B_back (ours)', 'stock Brendan_back', 'stock May_back')):
        e = strip([arr], 2, 0); label(e, name + ', 5-frame throw strip, 2x'); parts.append(e)
    W = max(p.width for p in parts); H = sum(p.height + 10 for p in parts)
    sh = Image.new('RGBA', (W, H), (90, 100, 110, 255)); y = 0
    for p in parts:
        sh.alpha_composite(p, (0, y)); y += p.height + 10
    sh.save(out)
    return sh.size


if __name__ == '__main__':
    import sys
    print(main03(sys.argv[1]) if '03' in sys.argv[1] else main(sys.argv[1]))
