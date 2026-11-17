"""wardian.py - builds the Wardian-case (travelling glass greenhouse) prop for Juno V1.

Frame = brass members built from straight pixel runs (the only hand-built part).
Contents = cut from professional donors: Exeggutor's fronds and Oddish's leaves
(Reborn battlers, 96-px art at the same pixel size as 80-px fronts), the Bounsweet
icon (Reborn icon, 32-px art) and a terracotta pot from the Apothecary tileset (x2).
Everything behind glass gets a glass tint; panes get diagonal glints (light from upper left).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kb, mat
from mat import H, BLACK, CLEAR
from PIL import Image, ImageDraw

R = '/home/claude/ref/games/reborn/Graphics/'
APO = '/home/claude/ref/art/morgebby/Graphics/Tilesets/Apothecary.png'

BRASS = [H('3c2410'), H('7a5020'), H('b88a38'), H('e8c870'), H('fff0b8')]   # outline-dark .. highlight
WOOD = [H('2a1810'), H('4e2c1c'), H('74442a'), H('9a6440')]
GLASS_BG = [H('9cc4c4'), H('b4d8d4'), H('cfe8e2')]
GLINT = H('f4fcf8')
TINT = (206, 236, 230)


def battler(name):
    im = kb.load(R + 'Battlers/%s.png' % name).crop((0, 0, 192, 192))
    n, f = kb.native(im)
    return n


def icon(name):
    im = kb.load(R + 'Icons/%s.png' % name)
    im = im.crop((0, 0, im.size[1], im.size[1]))
    n, f = kb.native(im)
    return n


def greens_only(im):
    """keep foliage + its dark outline (drop the Exeggutor heads/trunk colours)."""
    out = im.copy(); p = out.load()
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            r, g, b, a = p[x, y]
            if not a:
                continue
            green = g > r + 8 and g > b
            dark = (r + g + b) < 120
            if not (green or dark):
                p[x, y] = CLEAR
    return out


def line(px, x0, y0, x1, y1, col):
    """bresenham into dict px[(x,y)] = col"""
    dx, dy = abs(x1 - x0), -abs(y1 - y0)
    sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
    err = dx + dy
    while True:
        px[(x0, y0)] = col
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy; x0 += sx
        if e2 <= dx:
            err += dx; y0 += sy


def build(size=(80, 80), L=5, Rr=45, eave=18, peak=8, base_top=43, base_bot=48, mid=30, cols=(15, 25, 35),
          cracked=True, vent=True):
    W, Hh = size
    cx = (L + Rr) // 2
    # --- 1. contents (behind glass) -------------------------------------------
    inside = Image.new('RGBA', size, CLEAR)
    eg = greens_only(battler('exeggutor'))
    bb = kb.bbox(eg)
    fr = eg.crop((bb[0] + 8, bb[1], bb[0] + 58, bb[1] + 26))   # 50 x 26 frond fan
    inside.alpha_composite(fr, (L - 4, eave - 9))
    od = battler('oddish'); ob = kb.bbox(od)
    leaf = od.crop((ob[0], ob[1], ob[2], ob[1] + 20))
    leaf = mat.keep(leaf, mat.region(leaf.size, rect=(0, 0, leaf.size[0], 15)))
    inside.alpha_composite(leaf, (Rr - 30, mid - 6))
    # glass-tint + fill the empty panes
    glass = Image.new('RGBA', size, CLEAR)
    gp = glass.load(); ip = inside.load()

    def in_case(x, y):
        if L < x < Rr and eave < y < base_top:
            return True
        if y <= eave and y > peak:
            half = (y - peak) * 2
            return cx - half < x < cx + half
        return False

    for y in range(Hh):
        for x in range(W):
            if not in_case(x, y):
                continue
            c = ip[x, y]
            if c[3]:
                # behind glass: lift toward the tint and drop contrast a little
                gp[x, y] = mat.blend(c, TINT, 0.38)
            else:
                # empty glass: lighter toward upper-left of each pane
                u = ((x - L) % 10) + ((y - eave) % 12)
                gp[x, y] = GLASS_BG[2] if u < 6 else (GLASS_BG[1] if u < 14 else GLASS_BG[0])
    # --- 2. glints (diagonal, upper-left light) ---------------------------------
    for (gx, gy, n) in [(L + 4, eave + 7, 4), (L + 6, eave + 7, 2), (cols[1] + 6, eave + 6, 4),
                        (cols[2] + 5, mid + 8, 3), (L + 5, mid + 9, 3), (cx - 2, peak + 7, 3)]:
        for i in range(n):
            if in_case(gx - i, gy + i):
                gp[gx - i, gy + i] = GLINT
    # --- 3. frame ---------------------------------------------------------------
    fr_px = {}
    O, D, M, Lt, Hl = BRASS
    # outer verticals
    for y in range(eave, base_top + 1):
        fr_px[(L, y)] = Lt; fr_px[(L - 1, y)] = BLACK
        fr_px[(Rr, y)] = M; fr_px[(Rr + 1, y)] = BLACK
    # mullions (2 px: lit left, shade right)
    for x in cols:
        for y in range(eave, base_top):
            fr_px[(x, y)] = Lt; fr_px[(x + 1, y)] = D
    # eave rail and mid rail (2 px: lit top, shade bottom)
    for x in range(L, Rr + 1):
        fr_px[(x, eave)] = Lt; fr_px[(x, eave + 1)] = D
        fr_px[(x, mid)] = Lt; fr_px[(x, mid + 1)] = D
    # gable: 2:1 runs from eave corners to the peak, outlined above
    for i in range(0, (cx - L) + 1):
        y = eave - i // 2
        xl, xr = L + i, Rr - i
        fr_px[(xl, y)] = Hl if i % 2 == 0 else Lt
        fr_px[(xl, y - 1)] = BLACK
        fr_px[(xr, y)] = M
        fr_px[(xr, y - 1)] = BLACK
        fr_px[(xl, y + 1)] = fr_px.get((xl, y + 1), D) if (xl, y + 1) in fr_px else D
        fr_px[(xr, y + 1)] = D
    # gable centre post + a roof vent
    for y in range(peak + 1, eave):
        fr_px[(cx, y)] = Lt; fr_px[(cx + 1, y)] = D
    # finial knob
    for (x, y, c) in [(cx, peak - 2, Lt), (cx + 1, peak - 2, M), (cx, peak - 3, Hl), (cx + 1, peak - 3, Lt),
                      (cx - 1, peak - 2, BLACK), (cx + 2, peak - 2, BLACK), (cx, peak - 4, BLACK), (cx + 1, peak - 4, BLACK),
                      (cx - 1, peak - 3, BLACK), (cx + 2, peak - 3, BLACK), (cx, peak - 1, M), (cx + 1, peak - 1, D)]:
        fr_px[(x, y)] = c
    # --- 4. base tray (walnut, brass corners) -----------------------------------
    for y in range(base_top, base_bot + 1):
        for x in range(L - 1, Rr + 2):
            if y == base_bot or x in (L - 1, Rr + 1):
                fr_px[(x, y)] = BLACK
            elif y == base_top:
                fr_px[(x, y)] = Lt if x < Rr - 2 else M
            elif y == base_top + 1:
                fr_px[(x, y)] = WOOD[3]
            elif y == base_bot - 1:
                fr_px[(x, y)] = WOOD[1]
            else:
                fr_px[(x, y)] = WOOD[2]
    for (x0) in (L, Rr - 2):
        for dx in range(3):
            for y in range(base_top + 1, base_bot):
                fr_px[(x0 + dx, y)] = [Lt, M, D][dx] if y < base_bot - 1 else D
    # crack in the upper-right gable pane
    if cracked:
        for (x, y) in [(cx + 8, eave - 3), (cx + 7, eave - 2), (cx + 7, eave - 1), (cx + 9, eave - 2), (cx + 10, eave - 2)]:
            fr_px[(x, y)] = GLINT
    case = glass.copy(); cp = case.load()
    for (x, y), c in fr_px.items():
        if 0 <= x < W and 0 <= y < Hh:
            cp[x, y] = c
    # bounsweet peeking from behind the finial / vent (on top of everything)
    bsw = icon('bounsweet'); bbx = kb.bbox(bsw); bsw = bsw.crop(bbx)
    top = Image.new('RGBA', size, CLEAR)
    if vent:
        cut = bsw.crop((0, 0, bsw.size[0], 13))   # leaves + upper fruit
        top.alpha_composite(cut, (cx - 13, peak - 9))
    return case, top, inside


if __name__ == '__main__':
    case, top, inside = build()
    out = case.copy(); out.alpha_composite(top)
    kb.grid(out, 8).save(kb.WORK + '/sheets/v1_case.png')
