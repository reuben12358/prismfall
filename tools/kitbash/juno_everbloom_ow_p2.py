"""Juno Ever-Bloom overworld charset, PASS 2: project convention 128x192 (16x24-px frames doubled).
Donor: base project's trainer_LADY charset (Gen-4-style Lady). Hair -> auburn, dress -> ivory, wreath ring and a
shaped, fluttering veil hand-placed per direction and frame. python3 -I tools/kitbash/juno_everbloom_ow_p2.py"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, mat
from mat import H, CLEAR
from PIL import Image

SRC = '/home/claude/ref/ebdx_renovation/Graphics/Characters/trainer_LADY.png'
MAP = {(56, 56, 24, 255): H('5a2018'), (120, 112, 64, 255): H('b04a2a'), (200, 176, 104, 255): H('e8824a'),
       (80, 16, 0, 255): H('a07888'), (144, 64, 40, 255): H('e8d4d6'), (224, 112, 80, 255): H('fffaf6')}
PINK, LITE, ROSE = H('f090a8'), H('ffe0e6'), H('c05070')
VEIL, VSH, VED = H('ffe8ee'), H('f4c0cc'), H('d88098')
FW, FH = 16, 24


def veil_px(d, f):
    """list of (x, y, kind) in frame coords; kind: 0 body, 1 shade/fold, 2 edge."""
    out = []
    fl = 1 if f in (1, 3) else 0
    if d == 3:                       # up: falls down the whole back
        for y in range(7, 22):
            half = 3 + (y - 7) // 4 + (fl if y > 16 else 0)
            for x in range(8 - half, 8 + half):
                k = 2 if x in (8 - half, 8 + half - 1) or y == 21 else (1 if x == 7 + (y // 6) % 2 else 0)
                out.append((x, y, k))
    elif d in (1, 2):                # left / right: trails behind the head
        for y in range(8, 22):
            a = 11 + (y - 8) // 5
            b = 13 + (y - 8) // 3 + (fl if y > 14 else 0)
            for x in range(a, min(b, 15) + 1):
                k = 2 if x == min(b, 15) or y == 21 else (1 if x == a + 1 and y % 3 == 0 else 0)
                out.append((x if d == 1 else 15 - x, y, k))
    else:                            # down: shows either side behind the dress
        for y in range(15, 22):
            w = 1 + (y - 15) // 3 + (fl if y > 18 else 0)
            for i in range(w):
                out.append((3 - i, y, 2 if i == w - 1 else 0)); out.append((12 + i, y, 2 if i == w - 1 else 0))
    return out


def frame_edit(fr, d, f):
    p = fr.load()
    top = next(y for y in range(FH) if any(p[x, y][3] for x in range(FW)))
    dy = top - 3 if d != 0 else top - 3
    hair = {H('5a2018'), H('b04a2a'), H('e8824a')}
    for (x, y, k) in veil_px(d, f):
        y += dy
        if not (0 <= x < FW and 0 <= y < FH):
            continue
        c = p[x, y]
        col = [VEIL, VSH, VED][k]
        if c[3] == 0:
            p[x, y] = col
        elif d == 3 or (d in (1, 2) and c in hair and y > top + 6):
            if c != (0, 0, 0, 255):
                p[x, y] = mat.blend(c, col, 0.6) if c in hair else col
    # wreath: a ring of blossoms round the crown
    ring = [(3, 3), (4, 2), (5, 1), (6, 0), (7, 0), (8, 0), (9, 0), (10, 1), (11, 2), (12, 3)]
    for i, (x, oy) in enumerate(ring):
        y = top + oy
        if p[x, y][3]:
            p[x, y] = ROSE if i % 3 == 1 else PINK
            if p[x, y + 1][3]:
                p[x, y + 1] = LITE if i % 2 == 0 else PINK
    return fr


def build():
    n, f = kb.native(kb.load(SRC))
    n = mat.recolour(n, MAP)
    out = Image.new('RGBA', n.size, CLEAR)
    for r in range(4):
        for c in range(4):
            fr = n.crop((c * FW, r * FH, (c + 1) * FW, (r + 1) * FH))
            out.paste(frame_edit(fr, r, c), (c * FW, r * FH))
    return out


if __name__ == '__main__':
    o = build()
    o.save(kb.WORK + '/passes/eb_ow_p2_native.png')
    kb.up(o, 2).save(kb.WORK + '/juno/JUNO_everbloom_charset_p2.png')
    kb.up(kb.on_bg(o, (120, 160, 110, 255)), 8).save(kb.WORK + '/sheets/eb_ow_p2_8x.png')
