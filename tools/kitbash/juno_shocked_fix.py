"""Juno SHOCKED, fix pass (16g). Base: the installed surprised face (p3x_surprised_48, tan band already removed).
User on 16f: the shocked face's left eye "looks so weird" (wall-eyed: a white blob with a pin-prick vs a smaller pale oval),
and the big pink mouth with teeth "looks so unnatural".
  - Eyes: one stamp, mirrored about the face centre (x = 25), so both are the same shape and size: her normal B2W2 eye
    (thick black top lash, soft r line inside, brown n line outside, tan lower lid) with the opening widened by 1 px all
    round, and a small green iris (dark rim, light green, black pupil, one white glint) centred in the white.
  - Mouth A: a small rounded "O" gasp. Mouth B: a soft trapezoid (her happy mouth's outline, smaller, no teeth).
    Both: 1-px 983840 line like the surprised mouth, dark 702838 inside, a hint of e06880 tongue.
  - Only pixels inside the two eye boxes and the mouth box change (checked in main()).
python3 -I tools/kitbash/juno_shocked_fix.py   -> passes/p3y_shocked_{A,B}_48.png, juno/JUNO_shocked_p3y{A,B}.png,
                                                 art/previews/16g_juno_shocked.png"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, mat, sheet09 as s
from mat import H
from PIL import Image, ImageDraw

P, J = kb.WORK + '/passes', kb.WORK + '/juno'
SKIN = H('f8d0b8')
XP = {'k': H('000000'), 's': SKIN, 'w': H('e8e8f8'), 'W': H('f8f8f8'), 'g': H('48a060'), 'G': H('8ed07a'),
      'D': H('1e5a3c'), 'n': H('b08058'), 'r': H('804848'), 't': H('d8a078'),
      'm': H('983840'), 'd': H('702838'), 'p': H('e06880')}

# right eye (viewer's right), columns x29..37, rows y24..33. '.' keeps the face pixel.
# Opening x30..36 (7 wide, was 5) and y26..32 (7 tall, was 6); iris 3x4 centred; inner lid line r above, t below.
EYE_R = ['...kkkk..',
         '.kkkkkkkn',
         'rkwwwwwkn',
         'rwwwwwwwn',
         'rwwgggwwn',
         'twwgkgwwn',
         'twwgkGwwn',
         'twwwGwwwt',
         '.twwwwwn.',
         '..ttttt..']
IRIS = ['ggg', 'gkg', 'gkG', 'wGw']      # rounded 3x4 iris, 1x2 pupil, light lower rim (no dark corners: they read as an x)
EYE_X, EYE_Y = 29, 24


def mirror_rows(rows):
    """mirror the outline but keep the iris (and its glint) reading the same way, so the light comes from one side."""
    out = []
    for r in rows:
        m = r[::-1]
        out.append(m)
    return out


def eyes(im):
    # clear both old eyes inside their boxes (the face outline at x13 and x38 is outside the boxes)
    p = im.load()
    for y in range(EYE_Y, EYE_Y + len(EYE_R)):
        for x in list(range(14, 22)) + list(range(29, 38)):
            if y == EYE_Y and p[x, y] not in (H('000000'), H('804848')):
                continue            # row 24 is the fringe's edge: only re-ink, never paint skin over hair
            p[x, y] = SKIN if y > EYE_Y else p[x, y]
    im = mat.patch(im, EYE_X, EYE_Y, EYE_R, XP)
    left = mirror_rows(EYE_R)
    # iris of the left eye: same orientation as the right one (glint upper-left), placed in the mirrored opening
    iris = IRIS
    lx = 50 - (EYE_X + len(EYE_R[0]) - 1)          # mirrored stamp origin (x13)
    # the left stamp's outer column (x13) runs along the face outline: keep the outline's black pixels, paint the brown
    # n line only where hair shows through
    p = im.load()
    left = [('.' if p[lx, EYE_Y + j] == XP['k'] else r[0]) + r[1:] for j, r in enumerate(left)]
    im = mat.patch(im, lx, EYE_Y, left, XP)
    im = mat.patch(im, lx + 3, EYE_Y + 4, iris, XP)
    return im


MOUTH_BOX = (22, 34, 31, 40)          # inclusive
MOUTH = {
    'A': (24, 35, ['.mmmm.',
                   'mddddm',
                   'mddddm',
                   'mdppdm',
                   '.mmmm.']),
    'B': (23, 35, ['.mmmmm.',
                   'mdddddm',
                   'mdddddm',
                   '.mdppm.',
                   '..mmm..']),
}


def mouth(im, key):
    p = im.load()
    x0, y0, x1, y1 = MOUTH_BOX
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if p[x, y] in (XP['m'], XP['d'], XP['p']):
                p[x, y] = SKIN
    mx, my, rows = MOUTH[key]
    return mat.patch(im, mx, my, rows, XP)


def build(key):
    im = Image.open(P + '/p3x_surprised_48.png').convert('RGBA')
    return mouth(eyes(im), key)


def changed_outside(a, b):
    pa, pb = a.load(), b.load(); bad = []
    for y in range(48):
        for x in range(48):
            if pa[x, y] != pb[x, y]:
                in_eye = EYE_Y <= y <= EYE_Y + 9 and (13 <= x <= 21 or 29 <= x <= 37)
                in_mouth = MOUTH_BOX[0] <= x <= MOUTH_BOX[2] and MOUTH_BOX[1] <= y <= MOUTH_BOX[3]
                if not (in_eye or in_mouth):
                    bad.append((x, y))
    return bad


def main():
    base = Image.open(P + '/p3x_surprised_48.png').convert('RGBA')
    before = Image.open(P + '/p3x_shocked_48.png').convert('RGBA')
    outs = {}
    for k in MOUTH:
        im = build(k)
        bad = changed_outside(base, im)
        print(k, 'pixels changed outside eye/mouth boxes:', bad)
        im.save(P + '/p3y_shocked_%s_48.png' % k)
        kb.up(im, 2).save(J + '/JUNO_shocked_p3y%s.png' % k)
        outs[k] = im
    cols = [('surprised (installed base)', base), ('shocked, 16f (rejected)', before),
            ('shocked A: fixed eyes + "O" gasp', outs['A']), ('shocked B: fixed eyes + soft trapezoid', outs['B'])]
    W, Hh = 24 + 4 * 420, 330
    sh = Image.new('RGBA', (W, Hh), s.BG); d = ImageDraw.Draw(sh); f13, f10 = kb.font(13), kb.font(10)
    d.text((16, 8), 'JUNO SHOCKED fix (16g). Eyes: one stamp mirrored about the face centre, her normal eye widened 1 px all round, '
                    'small green irises. Mouths: a smaller gasp in her own line weight, no teeth. Only eye and mouth boxes change.',
           font=f10, fill=s.TXT)
    for i, (lab, im) in enumerate(cols):
        x = 16 + i * 420
        d.rectangle((x, 30, x + 410, Hh - 10), fill=s.PANEL)
        d.text((x + 8, 34), lab, font=f13, fill=s.ACC if i >= 2 else s.DIM)
        im96 = kb.up(im, 2)
        sh.alpha_composite(s.stage(im96, 1, s.STAGE, 100, 100), (x + 8, 56))
        sh.alpha_composite(kb.up(kb.on_bg(im96, s.STAGE), 2), (x + 112, 56))
        sh.alpha_composite(s.bubble(im96), (x + 2, 170))
        d.text((x + 8, 296), '1x (96 file), 2x, bubble', font=f10, fill=s.DIM)
    sh.save(kb.GAME + '/art/previews/16g_juno_shocked.png'); print(sh.size)


if __name__ == '__main__':
    main()
