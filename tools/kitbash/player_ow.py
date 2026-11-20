"""Player overworld walk charsets, Essentials format: 4 rows (down, left, right, up) x 4 frames of 16x24 art, doubled to a
128x192 file (the convention of the base project's trainer_*.png and our JUNO/KESTREL sheets).
The base project's FRLG-style charsets share one animation template, so heads and bodies swap cell by cell:
  A: head rows 0-14 from trainer_COOLTRAINER_M (soft full hair -> ash; RIVAL1's spikes read as Blue), body rows 15-23 from trainer_POKEMONTRAINER_Red
     (vest -> chalk white, jeans -> slate, yellow pack -> teal canvas, + a red tag pixel on the pack in the back view).
  B: head rows 0-14 from trainer_BEAUTY (long hair -> ash; the Lass bob read as a helmet), body rows 15-23 from trainer_POKEMONTRAINER_Leaf (hair below
     the cut -> ash, tank -> white, skirt -> slate, satchel -> teal).
python3 -I tools/kitbash/player_ow.py -> art/work/kitbash/player/PLAYER_{A,B}_ow.png (+_native)"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, mat, player as pl
from mat import H, CLEAR, BLACK
from PIL import Image

P = pl.P
R = '/home/claude/ref/ebdx_renovation/Graphics/Characters/'
CUT = 15


def sheet(n):
    return kb.native(kb.load(R + n + '.png'))[0]


def splice(head, body, cut=CUT):
    out = body.copy()
    for r in range(4):
        for c in range(4):
            x0, y0 = c * 16, r * 24
            hb = head.crop((x0, y0, x0 + 16, y0 + cut))
            out.paste(Image.new('RGBA', (16, cut), CLEAR), (x0, y0))
            out.paste(hb, (x0, y0))
    return out


def rows_mask(size, y_from, y_to):
    m = Image.new('L', size, 0); p = m.load()
    for r in range(4):
        for y in range(r * 24 + y_from, r * 24 + y_to):
            for x in range(size[0]):
                p[x, y] = 255
    return m


DARK = H('3a3632')


def ow_a():
    head = mat.recolour(sheet('trainer_COOLTRAINER_M'), {H('a090f0'): P['a1'], H('6850b8'): P['a2'], H('403860'): P['a3']},
                        rows_mask((64, 96), 0, CUT))
    body = sheet('trainer_POKEMONTRAINER_Red')
    body = mat.recolour(body, {H('f86848'): P['w1'], H('c03838'): P['w2'], H('682828'): P['w4'],
                               H('383878'): P['s3'], H('70a0c0'): P['s1'],
                               H('f8d858'): P['t2'], H('b89838'): P['t3'], H('a87840'): P['t4']},
                        rows_mask(body.size, CUT, 24))
    out = splice(head, body)
    # RIVAL1's dark-green shirt pixels that sit in the head rows (collar) -> slate
    out = mat.recolour(out, {H('204010'): P['s4']})
    # the ferry tag: one red pixel + one paper pixel on the bag, back view (row 3), every frame
    p = out.load()
    for c in range(4):
        x0, y0 = c * 16, 3 * 24
        for y in range(y0 + 15, y0 + 22):
            for x in range(x0 + 3, x0 + 13):
                if p[x, y] in (P['t2'], P['t3']) and p[x + 1, y] in (P['t2'], P['t3']) and p[x, y - 1] in (P['t2'], P['t3'], BLACK):
                    p[x, y] = P['g1']; p[x, y + 1] = P['g2']
                    break
            else:
                continue
            break
    return out


def ow_b():
    head = mat.recolour(sheet('trainer_BEAUTY'), {H('f8e050'): P['a1'], H('d0b028'): P['a2'], H('806000'): P['a3'],
                                                   H('483030'): DARK}, rows_mask((64, 96), 0, CUT))
    body = sheet('trainer_POKEMONTRAINER_Leaf')
    low = rows_mask(body.size, CUT, 24)
    body = mat.recolour(body, {H('784040'): P['a3'], H('a87840'): P['a2'],
                               H('70a0c0'): P['w1'], H('4040d0'): P['w3'], H('e8e8f8'): P['w1'], H('b0b0d0'): P['w2'],
                               H('c03838'): P['s2'], H('f86848'): P['s1'], H('682828'): P['s3'],
                               H('f8d858'): P['t2'], H('b89838'): P['t3']}, low)
    out = splice(head, body)
    out = mat.recolour(out, {H('e87840'): P['t2'], H('a84038'): P['t3'], H('383878'): P['s3']})   # ribbon -> teal
    # her hair covers her back in the up row: the sea bag goes on top of it, over her left shoulder, with the tag
    for c in range(4):
        x0, y0 = c * 16, 3 * 24
        top = kb.bbox(out.crop((x0, y0, x0 + 16, y0 + 24)))[1]
        out = mat.patch(out, x0 + 9, y0 + top + 9, ['.kk.', 'kTtk', 'kgtk', 'kuTk', 'kuTk', 'kuuk', '.kk.'],
                        dict(pl.X, g=P['g1']))
    return out


def main():
    d = kb.WORK + '/player'
    os.makedirs(d, exist_ok=True)
    outs = {'A': ow_a(), 'B': ow_b()}
    for k, im in outs.items():
        im.save('%s/PLAYER_%s_ow_native.png' % (d, k))
        kb.up(im, 2).save('%s/PLAYER_%s_ow.png' % (d, k))
    ims = [('A', outs['A']), ('B', outs['B'])]
    sh = kb.contact(ims, 2, (64 * 4 + 8, 96 * 4 + 6), k=4, fs=11, label_h=14)
    sh.save('/tmp/ow_pl.png'); print(sh.size)


if __name__ == '__main__':
    main()
