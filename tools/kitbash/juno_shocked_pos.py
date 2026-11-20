"""Juno SHOCKED, placement-only fix of the 16f face (16h). The user rejected the 16g redraws: keep 16f's eye style and mouth
design exactly; fix only where they sit.
  - Left eye on screen: replaced by the exact mirror image of the right eye on screen (her left), about the face centre
    x = 25 (her normal eyes span x14..20 and x30..36), same rows y25..33. The face outline and hair at x13/x14 are kept.
  - Mouth: 16f's mouth pixels, unchanged, moved 1 px left and 1 px down to x23..30, y35..41: top row at y35 like the happy
    and surprised mouths, centred at x26.5 like the surprised mouth. The pixels it leaves come back from the base face
    (skin, and the nose pixel at 29,34 that 16f's top line had covered).
python3 -I tools/kitbash/juno_shocked_pos.py -> passes/p3z_shocked_48.png, juno/JUNO_shocked_p3z.png,
                                              art/previews/16h_juno_shocked_pos.png"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, sheet09 as s
from mat import H
from PIL import Image, ImageDraw

P, J = kb.WORK + '/passes', kb.WORK + '/juno'
SKIN, BLACK = H('f8d0b8'), H('000000')
HAIR = {H('c8582e'), H('963a24'), H('6a2219'), H('d86888')}
MOUTH_COLS = {H('983840'), H('702838'), H('e06880')}           # the base face's own (surprised) mouth colours
AXIS2 = 50                                                    # mirror x -> 50 - x
EYE_ROWS = range(25, 34)
RIGHT_EYE_X = range(30, 38)
# 16f mouth, exactly as juno_extras.shocked() drew it at (24, 34)
MOUTH_ROWS = ['..kkkk..', '.kWWWWk.', 'kddddddk', 'kddddddk', 'kddppddk', '.kppppk.', '..kkkk..']
OLD_MOUTH, NEW_MOUTH = (24, 34), (23, 35)


def protected(p, x, y):
    """face outline and hair: hair colours, and black pixels touching hair."""
    if p[x, y] in HAIR:
        return True
    if p[x, y] == BLACK:
        return any(p[x + dx, y + dy] in HAIR for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
    return False


def fix():
    im = Image.open(P + '/p3x_shocked_48.png').convert('RGBA')
    base = Image.open(P + '/p3x_surprised_48.png').convert('RGBA'); pb = base.load()
    src = im.copy(); ps = src.load()
    p = im.load()
    # --- eyes: clear the old left eye, then paint the mirror of the right one (outline/hair kept)
    for y in EYE_ROWS:
        for x in range(13, 22):
            if not protected(ps, x, y):
                p[x, y] = SKIN
        for x in RIGHT_EYE_X:
            tx = AXIS2 - x
            if not protected(ps, tx, y):
                p[tx, y] = ps[x, y]
    # --- mouth: lift 16f's mouth, restore what the base face had under it, put it down 1 left / 1 down
    mouth = {}
    for j, row in enumerate(MOUTH_ROWS):
        for i, ch in enumerate(row):
            if ch != '.':
                x, y = OLD_MOUTH[0] + i, OLD_MOUTH[1] + j
                mouth[(i, j)] = ps[x, y]
                b = pb[x, y]
                p[x, y] = SKIN if b in MOUTH_COLS else b
    for (i, j), c in mouth.items():
        p[NEW_MOUTH[0] + i, NEW_MOUTH[1] + j] = c
    return im


def main():
    before = Image.open(P + '/p3x_shocked_48.png').convert('RGBA')
    im = fix()
    # report what changed
    pa, pb = before.load(), im.load()
    ch = [(x, y) for y in range(48) for x in range(48) if pa[x, y] != pb[x, y]]
    xs = [c[0] for c in ch]; ys = [c[1] for c in ch]
    print('changed', len(ch), 'bbox', (min(xs), min(ys), max(xs), max(ys)))
    outside = [(x, y) for x, y in ch if not ((13 <= x <= 21 and 25 <= y <= 33) or (23 <= x <= 31 and 34 <= y <= 41))]
    print('outside eye/mouth boxes:', outside)
    im.save(P + '/p3z_shocked_48.png')
    kb.up(im, 2).save(J + '/JUNO_shocked_p3z.png')
    cols = [('16f shocked (before)', before), ('fixed placement (after)', im)]
    W, Hh = 16 + 2 * 420, 330
    sh = Image.new('RGBA', (W, Hh), s.BG); d = ImageDraw.Draw(sh); f13, f10 = kb.font(13), kb.font(10)
    d.text((16, 8), 'JUNO SHOCKED, placement only (16h). Left eye = mirror of the right eye at her normal left-eye spot; '
                    'mouth unchanged, moved 1 left / 1 down to her normal mouth spot.', font=f10, fill=s.TXT)
    for i, (lab, x_im) in enumerate(cols):
        x = 16 + i * 420
        d.rectangle((x, 30, x + 410, Hh - 10), fill=s.PANEL)
        d.text((x + 8, 34), lab, font=f13, fill=s.ACC if i else s.DIM)
        im96 = kb.up(x_im, 2)
        sh.alpha_composite(s.stage(im96, 1, s.STAGE, 100, 100), (x + 8, 56))
        sh.alpha_composite(kb.up(kb.on_bg(im96, s.STAGE), 2), (x + 112, 56))
        sh.alpha_composite(s.bubble(im96), (x + 2, 170))
        d.text((x + 8, 296), '1x (96 file), 2x, bubble', font=f10, fill=s.DIM)
    sh.save(kb.GAME + '/art/previews/16h_juno_shocked_pos.png'); print(sh.size)


if __name__ == '__main__':
    main()
