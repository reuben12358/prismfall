"""sheet09.py - the review sheet art/previews/09_juno_kitbash.png + final exports.
python3 -I tools/kitbash/sheet09.py
"""
import sys, os, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, show
from PIL import Image, ImageDraw

J = kb.WORK + '/juno'
P = kb.WORK + '/passes'
OUTSHEET = kb.GAME + '/art/previews/09_juno_kitbash.png'
R = '/home/claude/ref/games/reborn/Graphics/'

FINAL = [
    ('v1_final.png', 'JUNO_v1_underglass', '1  UNDER GLASS',
     'She carries every rescued plant on her back in a brass Wardian case, because she cannot bear to lose one more thing.',
     [('sd:backpackerf', 'body, pose, head'), ('B:exeggutor', 'fronds'), ('B:oddish', 'leaves'), ('I:bounsweet', 'Bounsweet')],
     'hand-built: brass frame, glass tints, glints, label, crack'),
    ('v2_final.png', 'JUNO_v2_everbloom', '2  EVER-BLOOM',
     "The flower girl of a wedding that never ended: she still wears the Bride Tree's blossoms, and they still won't wilt.",
     [('sd:lady', 'body, pose, head, hair'), ('sd:miku-flying', 'veil (tail, flipped)'), ('B:comfey', 'big blooms')],
     'hand-built: 5-px blossoms, buds, leaves, ribbon tails'),
    ('v3_final.png', 'JUNO_v3_rotbloom', '3  ROT & BLOOM',
     'In the city where nothing rots, the girl who thinks rot is beautiful: a forager under a Shiinotic-cap parasol.',
     [('sd:parasollady', 'body, pose, head, handle'), ('B:shiinotic', 'cap / parasol')],
     'hand-built: 6 cap spots, gill patch'),
]
REFS = [('sd:bianca', 'Bianca (official BW)'), ('rejuv:139', 'Angie (Rejuvenation)'), ('reborn:093', 'Julia (Reborn)')]

BG = (40, 42, 50, 255)
PANEL = (58, 61, 72, 255)
STAGE = (152, 160, 172, 255)
BATTLE = (112, 150, 104, 255)
TXT = (232, 232, 236, 255)
DIM = (170, 174, 186, 255)
ACC = (240, 200, 120, 255)


def donor_img(spec):
    if spec.startswith('B:'):
        n, f = kb.native(kb.load(R + 'Battlers/%s.png' % spec[2:]).crop((0, 0, 192, 192)))
    elif spec.startswith('I:'):
        im = kb.load(R + 'Icons/%s.png' % spec[2:])
        n, f = kb.native(im.crop((0, 0, im.size[1], im.size[1])))
    else:
        n, f = show.get_native(spec)
    return n.crop(kb.bbox(n))


def stage(im, k, bg, w, h):
    s = Image.new('RGBA', (w, h), bg)
    z = kb.up(im, k)
    s.alpha_composite(z, ((w - z.size[0]) // 2, h - z.size[1] - 4))
    return s


def wrap(d, text, xy, width, font, fill):
    words = text.split(); line = ''; x, y = xy
    for w in words:
        t = (line + ' ' + w).strip()
        if d.textlength(t, font=font) > width:
            d.text((x, y), line, font=font, fill=fill); y += font.size + 3; line = w
        else:
            line = t
    if line:
        d.text((x, y), line, font=font, fill=fill); y += font.size + 3
    return y


def export():
    for src, name, *_ in FINAL:
        im = Image.open(os.path.join(P, src)).convert('RGBA')
        im.save(os.path.join(J, name + '_native80.png'))
        kb.up(im, 2).save(os.path.join(J, name + '.png'))
    p = Image.open(os.path.join(J, 'JUNO_portrait_native48.png')).convert('RGBA')
    kb.up(p, 2).save(os.path.join(J, 'JUNO_happy.png'))


def bubble(portrait96, r=58):
    size = 2 * r + 8
    out = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    m = Image.new('L', (size, size), 0); dm = ImageDraw.Draw(m)
    dm.ellipse((4, 4, size - 5, size - 5), fill=255)
    bgc = Image.new('RGBA', (size, size), (236, 232, 222, 255))
    bgc.alpha_composite(portrait96, ((size - 96) // 2, (size - 96) // 2 + 6))
    out.paste(bgc, (0, 0), m)
    d = ImageDraw.Draw(out)
    d.ellipse((4, 4, size - 5, size - 5), outline=(24, 24, 32, 255), width=4)
    return out


def main():
    export()
    W, H = 1960, 1060
    sh = Image.new('RGBA', (W, H), BG); d = ImageDraw.Draw(sh)
    f16, f13, f11, f10 = kb.font(17), kb.font(13), kb.font(11), kb.font(10)
    d.text((16, 10), 'JUNO HALE - kitbash pass (frankensprites from professional donors). 80-px art, stored 160x160 like Reborn/EBDX fronts. '
                     'Top: 4x. Below: 2x and 1x in battle. Right: references at the same density (2x, 1x).', font=f13, fill=TXT)
    colw = 360; x0 = 16; y0 = 40
    for i, (src, name, title, pitch, donors, hand) in enumerate(FINAL):
        x = x0 + i * (colw + 14)
        d.rectangle((x, y0, x + colw, y0 + 1000), fill=PANEL)
        im = Image.open(os.path.join(P, src)).convert('RGBA')
        d.text((x + 10, y0 + 6), title + '   (4x)', font=f16, fill=ACC)
        sh.alpha_composite(stage(im, 4, STAGE, colw - 16, 324), (x + 8, y0 + 28))
        sh.alpha_composite(stage(im, 2, STAGE, (colw - 24) // 2, 172), (x + 8, y0 + 352))
        sh.alpha_composite(stage(im, 1, BATTLE, (colw - 24) // 2, 172), (x + 16 + (colw - 24) // 2, y0 + 352))
        d.text((x + 12, y0 + 354), '2x', font=f10, fill=(30, 30, 40, 255))
        d.text((x + 20 + (colw - 24) // 2, y0 + 354), '1x (in battle)', font=f10, fill=(20, 30, 20, 255))
        yy = wrap(d, pitch, (x + 10, y0 + 534), colw - 20, f13, TXT)
        d.text((x + 10, yy + 6), 'donors used', font=f11, fill=ACC)
        dx = x + 10; dy = yy + 22
        for spec, part in donors:
            dn = donor_img(spec)
            k = 1
            cell = max(dn.size[0] + 8, 80)
            s = stage(dn, k, STAGE, cell, 92)
            sh.alpha_composite(s, (dx, dy))
            src = spec.replace('B:', 'Reborn battler:').replace('I:', 'Reborn icon:').replace('sd:', 'BW/showdown:')
            for j, t in enumerate(src.split(':')):
                d.text((dx, dy + 94 + 11 * j), t, font=f10, fill=DIM)
            wrap(d, part, (dx, dy + 118), cell, f10, TXT)
            dx += cell + 6
        d.text((x + 10, dy + 150), hand, font=f10, fill=DIM)
    # references column
    rx = x0 + 3 * (colw + 14)
    rw = W - rx - 16
    d.rectangle((rx, y0, rx + rw, y0 + 660), fill=PANEL)
    d.text((rx + 10, y0 + 8), 'references (same density)', font=f13, fill=ACC)
    ry = y0 + 30
    for spec, lab in REFS:
        n, f = show.get_native(spec)
        sh.alpha_composite(stage(n, 2, STAGE, 200, 196), (rx + 8, ry))
        sh.alpha_composite(stage(n, 1, BATTLE, 110, 196), (rx + 214, ry))
        d.text((rx + 10, ry + 2), lab, font=f10, fill=(30, 30, 40, 255))
        ry += 204
    # portrait block
    py = y0 + 670
    d.rectangle((rx, py, rx + rw, y0 + 1000), fill=PANEL)
    d.text((rx + 10, py + 8), 'bubble portrait (for 1, UNDER GLASS)', font=f13, fill=ACC)
    p48 = Image.open(os.path.join(J, 'JUNO_portrait_native48.png')).convert('RGBA')
    p96 = kb.up(p48, 2)
    sh.alpha_composite(stage(p96, 1, STAGE, 100, 100), (rx + 10, py + 32))
    d.text((rx + 10, py + 134), '1x (96x96 file)', font=f10, fill=DIM)
    sh.alpha_composite(stage(p96, 3, STAGE, 292, 292), (rx + 118, py + 32))
    d.text((rx + 120, py + 328), '3x', font=f10, fill=DIM)
    b = bubble(p96)
    sh.alpha_composite(b, (rx + 420, py + 40))
    wrap(d, '[portrait: JUNO, happy] "Did you know larches drop every needle each winter? They look dead. They are NOT!"',
         (rx + 420, py + 172), 360, f11, TXT)
    d.text((rx + 420, py + 230), 'base: Desolation Faces/08a, brows from 08e;', font=f10, fill=DIM)
    d.text((rx + 420, py + 242), 'repaint: auburn hair, green irises, leaf sprig,', font=f10, fill=DIM)
    d.text((rx + 420, py + 254), 'knit collar + harness strap; hand: 6 freckles', font=f10, fill=DIM)
    sh.save(OUTSHEET)
    print(OUTSHEET, sh.size)


if __name__ == '__main__':
    main()
