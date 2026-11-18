"""wardian2.py - Wardian case (travelling glass greenhouse) for Juno V1, near-frontal 3/4 view.

Hand-built (straight runs only): brass frame members, walnut base, flat glass tints, glints.
Donor-cut (behind the glass): Exeggutor's fronds + Oddish's leaves (Reborn battlers, 96-px art =
same pixel size as 80-px fronts), the Bounsweet icon (Reborn icon, 32-px art, same pixel size).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, mat
from mat import H, BLACK, CLEAR
from PIL import Image, ImageDraw

R = '/home/claude/ref/games/reborn/Graphics/'

BR_D, BR_M, BR_L, BR_H = H('7a4e1c'), H('b4842e'), H('e2c060'), H('fff2b4')
WOOD = [H('2a1810'), H('4e2c1c'), H('74442a'), H('9a6440')]
GLASS = {'side': (H('bfeae2'), H('94d0cc')), 'roof': (H('dcf6ee'), H('bfeae2')), 'front': (H('8ccac6'), H('5fa2a8'))}
TINT_A = {'side': 0.35, 'roof': 0.4, 'front': 0.22}
GLINT = H('ffffff')


def battler(name):
    n, f = kb.native(kb.load(R + 'Battlers/%s.png' % name).crop((0, 0, 192, 192)))
    return n


def icon(name):
    im = kb.load(R + 'Icons/%s.png' % name)
    n, f = kb.native(im.crop((0, 0, im.size[1], im.size[1])))
    return n.crop(kb.bbox(n))


def greens_only(im):
    out = im.copy(); p = out.load()
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            r, g, b, a = p[x, y]
            if a and not (g > r + 8 and g > b) and (r + g + b) >= 120:
                p[x, y] = CLEAR
    return out


def pmask(size, poly):
    m = Image.new('L', size, 0)
    ImageDraw.Draw(m).polygon(poly, fill=255, outline=255)
    return m


def run(F, x0, y0, x1, y1, col):
    dx, dy = abs(x1 - x0), -abs(y1 - y0)
    sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
    err = dx + dy
    while True:
        F[(x0, y0)] = col
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy; x0 += sx
        if e2 <= dx:
            err += dx; y0 += sy


def build(size=(80, 80), fx0=16, fx1=42, eave=21, base=43, dep=(-4, -2), contents=True, ncol=22):
    W, Hh = size
    cx = (fx0 + fx1) // 2
    peak = eave - (cx - fx0)          # 1:1 gable
    dx, dy = dep
    front = [(fx0, eave), (cx, peak), (fx1, eave), (fx1, base), (fx0, base)]
    side = [(fx0 + dx, eave + dy), (fx0, eave), (fx0, base), (fx0 + dx, base + dy)]
    roof = [(fx0 + dx, eave + dy), (cx + dx, peak + dy), (cx, peak), (fx0, eave)]
    masks = {'side': pmask(size, side), 'roof': pmask(size, roof), 'front': pmask(size, front)}
    inside = Image.new('RGBA', size, CLEAR)
    if contents:
        eg = greens_only(battler('exeggutor')); b = kb.bbox(eg)
        fan = eg.crop((b[0] + 12, b[1] + 2, b[0] + 42, b[1] + 21))
        inside.alpha_composite(fan, (fx0 - 3, eave - 6))
        od = battler('oddish'); ob = kb.bbox(od)
        leaf = od.crop((ob[0], ob[1], ob[2], ob[1] + 17))
        inside.alpha_composite(leaf, (cx - 4, eave + 2))
        bsw = icon('bounsweet')
        inside.alpha_composite(bsw, (fx0 + 3, base - bsw.size[1] + 1))
    out = Image.new('RGBA', size, CLEAR); op = out.load(); ip = inside.load()
    for face in ('side', 'roof', 'front'):
        mm = masks[face].load(); top, bot = GLASS[face]
        for y in range(Hh):
            for x in range(W):
                if not mm[x, y]:
                    continue
                c = ip[x, y]
                tone = top if y < (eave + base) // 2 + (2 if face == 'front' else 0) else bot
                if face == 'roof':
                    tone = top
                a = TINT_A[face]
                if face == 'front' and y > (eave + base) // 2:
                    a = 0.12
                op[x, y] = mat.blend(c, tone, a) if c[3] else tone
    # keep the glass+contents to a small palette (no blend noise)
    out = mat.reduce_colours(out, ncol)
    op = out.load()
    # glints: 45-degree streaks on the front panes and the lit side
    for (gx, gy, n) in [(fx0 + 6, eave + 2, 5), (fx0 + 8, eave + 2, 2), (cx + 7, eave + 2, 5), (cx + 9, eave + 2, 2),
                        (cx + 6, eave + 13, 3), (fx0 - 1, eave + 3, 3), (fx0 - 1, eave + 13, 2), (cx - 2, peak + 4, 3)]:
        for i in range(n):
            x, y = gx - i, gy + i
            if 0 <= x < W and 0 <= y < Hh and op[x, y][3]:
                op[x, y] = GLINT
    F = {}
    mid = (eave + base) // 2
    run(F, fx0 + dx, base + dy, fx0 + dx, eave + dy, BR_L)            # side back post
    run(F, fx0 + dx, mid + dy, fx0, mid, BR_L)                        # side rail
    run(F, fx0 + dx, eave + dy, cx + dx, peak + dy, BR_H)             # roof back edge (lit)
    run(F, cx + dx, peak + dy, cx, peak, BR_H)                        # ridge
    run(F, fx0, eave, cx, peak, BR_L)                                 # front gable left
    run(F, cx, peak, fx1, eave, BR_M)                                 # front gable right
    run(F, fx0, eave, fx0, base, BR_L)                                # front-left post
    run(F, fx0 + 1, eave, fx0 + 1, base, BR_D)
    run(F, fx1, eave, fx1, base, BR_D)                                # front-right post
    run(F, fx1 - 1, eave, fx1 - 1, base, BR_M)
    run(F, fx0, eave, fx1, eave, BR_L)                                # eave
    run(F, fx0, eave + 1, fx1, eave + 1, BR_D)
    run(F, fx0, mid, fx1, mid, BR_L)                                  # mid rail
    run(F, fx0, mid + 1, fx1, mid + 1, BR_D)
    run(F, cx, peak, cx, base, BR_L)                                  # centre mullion
    run(F, cx + 1, peak + 1, cx + 1, base, BR_D)
    run(F, fx0 + dx, eave + dy, fx0, eave, BR_H)                      # side top
    for (x, y), c in F.items():
        if 0 <= x < W and 0 <= y < Hh:
            op[x, y] = c
    # walnut base: front block + side block
    for x in range(fx0 + dx, fx0):
        y = base + dy + int(round((x - (fx0 + dx)) * (-dy) / (-dx))) + 1
        if 0 <= y < Hh:
            op[x, y] = BR_L
            op[x, y + 1] = WOOD[2]
    for x in range(fx0, fx1 + 1):
        off = 0 if x >= fx0 else int(round((fx0 - x) * dy / -dx))
        for k in range(5):
            y = base + 1 + k - (0 if x >= fx0 else -(-off))
            y = base + 1 + k + (0 if x >= fx0 else -off)
            if x >= fx0:
                col = [BR_L, WOOD[3], WOOD[2], WOOD[2], WOOD[1]][k]
            else:
                col = [BR_H, WOOD[3], WOOD[3], WOOD[3], WOOD[2]][k]
            if 0 <= y < Hh:
                op[x, y] = col
    # brass carry-ring on the ridge
    for (x, y, c) in [(cx, peak - 1, BR_M), (cx - 1, peak - 2, BR_L), (cx - 2, peak - 3, BR_H), (cx - 2, peak - 4, BR_L),
                      (cx - 1, peak - 5, BR_H), (cx, peak - 5, BR_L), (cx + 1, peak - 4, BR_M), (cx + 1, peak - 3, BR_D),
                      (cx, peak - 2, BR_D)]:
        op[x, y] = c
    # paper plant label tied to the mid rail (her tiny handwriting)
    lab = ['ww', 'wk', 'gg']
    LB = {'w': H('fffaf0'), 'k': H('8a8070'), 'g': H('c8bfae')}
    for j, row in enumerate(lab):
        for i, ch in enumerate(row):
            op[fx0 + 9 + i, mid + 2 + j] = LB[ch]
    # the cracked pane (upper right): a jagged hairline
    for (x, y) in [(fx1 - 3, eave + 3), (fx1 - 4, eave + 4), (fx1 - 4, eave + 5), (fx1 - 5, eave + 6), (fx1 - 3, eave + 5),
                   (fx1 - 2, eave + 6)]:
        op[x, y] = GLINT
    case = mat.outline_outer(out, BLACK)
    return case, inside


if __name__ == '__main__':
    case, inside = build()
    kb.grid(case, 8).save(kb.WORK + '/sheets/v1_case2.png')
