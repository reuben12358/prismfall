#!/usr/bin/env python3
"""cdraw.py - the Prismfall cave kit (map builder 13): tileset 57 "PF Rejuv Cave" shares the PF Rejuv sheet, and these
pieces are appended by rcustom AFTER every earlier block (so no earlier id moves) and doubled 2x like every rdraw /
tdraw / ndraw / gdraw piece.  16-px logical grid, light from the top left, outlines never black.

Three rock palettes, each a complete kit (prefix cvS_ / cvL_ / cvE_):
  S  salt   Brinecut Mine: chalk-white rock salt with rose halite veins, a dusty grey-brown mine floor
  L  slate  Gullcry Caves: wet blue-grey slate, barnacles and weed at the foot, dark shingle and sand bars
  E  earth  warm brown cave rock (the kit for later caves)
per palette:
  walls      <p>_N{w,m,e}  <p>_W  <p>_E  <p>_{lip,face,base}{w,m,e}  <p>_face{m1,m2} (alts)  <p>_in{W,E}{0,1}
             (rkit KITS 'cvS' / 'cvL' / 'cvE': mass walls and terraces share them; the lip shows the ground above)
  ground     <p>_f0-3 floor (layer 1 ground, walkable), <p>_fd0-2 floor detail decals (walkable)
  mass       <p>_m{0-3}{a,b}: the rock above the walls, darkening with distance from the cave (darkness edges);
             solid ground.  <p>_mP: the mass art on a PASSABLE tile (a crawlway that looks like rock: hidden passages)
  ledges     <p>l_{w,m,e} (one-way, jump south)   stairs <p>_st{l,m,r} (rock-cut steps)   <p>_shadow (wall-foot shade)
  rocks      <p>_rock0-1 (1x1 solid), <p>_stal (1x2 stalagmite), <p>_rubble0-1 (decal)
shared: cv_hole (ladder down), cv_ladder (ladder up: hole in the face + foot), crystals cv_xsalt / cv_xblue / cv_xsea
(1x1 and 1x2), fungus cv_fung0-1 (glow caps, decal) and cv_shelf (wall fungus), mine props (cv_rail_*, cv_cart,
cv_cart_salt, cv_lever_l / _r, cv_frame (3x2 pit-prop frame), cv_post, cv_lamp_on / _off (1x2), cv_walllamp,
cv_tools, cv_saltblocks, cv_pump (2x2), cv_buffer), sea-cave props (cv_barn (barnacled rock), cv_kelp0-1, cv_wrack,
cv_nest, cv_guano, cv_drift (2x1), cv_shaft (2x3 light shaft, overhead), cv_tide_wet / cv_tide_dry (the tide-mark
rock), cv_flood (a flooded sand bar: solid shallow water for tide events), cv_bar (sand bar)), cv_chalkx (a miner's
chalk mark).

    python3 -I cdraw.py out.png      # contact sheet"""
import math, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
from rdraw import P, WOOD, CLEAR, canvas, disc

# ------------------------------------------------------------------ palettes (dark -> light)
PAL = {
    'S': dict(rock=[(70, 62, 82), (112, 104, 120), (150, 144, 156), (184, 178, 186), (212, 208, 210), (238, 236, 232)],
              vein=[(168, 132, 140), (204, 172, 176), (230, 208, 208)],
              floor=[(98, 86, 82), (122, 110, 102), (142, 130, 120), (164, 154, 142), (196, 190, 180)],
              mass=[(62, 56, 70), (46, 40, 54), (30, 26, 38), (16, 13, 22)],
              foot=(56, 48, 54)),
    'L': dict(rock=[(28, 34, 50), (48, 58, 78), (72, 86, 108), (100, 116, 138), (134, 150, 170), (186, 202, 216)],
              vein=[(60, 76, 60), (92, 108, 74), (206, 200, 178)],          # weed dark / weed / barnacle cream
              floor=[(58, 60, 64), (78, 80, 82), (98, 98, 98), (122, 120, 114), (152, 148, 136)],
              mass=[(40, 46, 62), (28, 32, 46), (18, 20, 32), (9, 10, 18)],
              foot=(26, 30, 40)),
    'E': dict(rock=[(58, 38, 34), (90, 62, 48), (122, 88, 64), (154, 118, 84), (186, 152, 108), (220, 192, 146)],
              vein=[(98, 120, 132), (140, 168, 182), (206, 226, 232)],
              floor=[(84, 64, 50), (108, 84, 64), (128, 102, 78), (150, 124, 94), (180, 156, 120)],
              mass=[(60, 42, 38), (44, 30, 28), (28, 19, 20), (14, 10, 12)],
              foot=(48, 32, 28)),
}
PAL['T'] = dict(rock=[(44, 30, 30), (72, 48, 40), (98, 68, 50), (126, 90, 62), (156, 116, 80), (194, 154, 108)],
                vein=[(34, 70, 104), (58, 122, 184), (96, 168, 212)],          # Isenmar union cloth
                floor=[(66, 70, 84), (92, 98, 114), (116, 122, 138), (140, 146, 160), (172, 178, 190)],
                mass=[(34, 30, 36), (24, 21, 26), (15, 13, 17), (8, 7, 10)],
                foot=(36, 26, 26))
GLOW = [(150, 84, 34, 255), (236, 150, 60, 255), (255, 214, 120, 255), (255, 246, 206, 255)]
XSALT = [(150, 92, 108), (204, 140, 150), (236, 192, 194), (252, 236, 232)]
XBLUE = [(34, 58, 122), (62, 112, 190), (120, 180, 234), (214, 242, 255)]
XSEA = [(26, 82, 76), (46, 140, 122), (110, 206, 178), (220, 255, 240)]
FUNG = [(30, 70, 84), (44, 128, 140), (96, 214, 200), (210, 255, 244)]
FUNGA = [(110, 54, 30), (190, 104, 44), (246, 176, 86), (255, 236, 184)]
IRON = [(40, 40, 48, 255), (74, 74, 86, 255), (118, 118, 132, 255), (170, 170, 184, 255)]
SEA = [(18, 52, 66), (30, 82, 98), (48, 116, 128), (92, 168, 172), (196, 236, 232)]
SAND = [(110, 94, 72), (146, 128, 98), (176, 160, 124), (204, 190, 152), (228, 218, 186)]


def A(c, a=255):
    return tuple(c[:3]) + (a,)


def nz(x, y, s):
    h = (x * 374761393 + y * 668265263 + s * 2147483647) & 0xffffffff
    h = ((h ^ (h >> 13)) * 1274126177) & 0xffffffff
    return (h & 0xffff) / 65536.0


def smooth(x, y, s, sc):
    """value noise, periodic in x and y with period 16 (so every tile built from it is seamless with itself)"""
    def g(ix, iy): return nz(ix % max(1, int(16 / sc)), iy % max(1, int(16 / sc)), s)
    fx, fy = x / sc, y / sc; ix, iy = int(math.floor(fx)), int(math.floor(fy)); tx, ty = fx - ix, fy - iy
    tx, ty = tx * tx * (3 - 2 * tx), ty * ty * (3 - 2 * ty)
    a = g(ix, iy) * (1 - tx) + g(ix + 1, iy) * tx; b = g(ix, iy + 1) * (1 - tx) + g(ix + 1, iy + 1) * tx
    return a * (1 - ty) + b * ty


# ------------------------------------------------------------------ the rock face: columnar lumps lit from the top left
def cells(seed, period, w, h, sx=5.0, sy=7.0):
    r = random.Random(seed); pts = []
    y = -sy
    row = 0
    while y < h + sy:
        x = (row % 2) * sx * 0.5
        while x < period:
            pts.append((x + r.uniform(-1.4, 1.4), y + r.uniform(-1.8, 1.8), r.random()))
            x += sx
        y += sy; row += 1
    return pts


def face_px(pal, pts, period, x, y, H, seed, vein=True):
    """colour of a wall pixel: nearest cell (periodic in x), crevice where two cells meet, lit top-left inside"""
    best = (1e9, None); second = 1e9
    for px_, py_, k in pts:
        dx = (x - px_ + period / 2) % period - period / 2
        dy = (y - py_) * 0.72
        d = dx * dx + dy * dy
        if d < best[0]: second = best[0]; best = (d, (dx, dy, k))
        elif d < second: second = d
    rock = pal['rock']
    d1, (dx, dy, k) = best
    if math.sqrt(second) - math.sqrt(d1) < 0.9:
        return A(rock[0])
    lit = -(dx * 0.8 + dy * 1.1) / 4.2 + (k - 0.5) * 0.5
    v = 3 + lit
    v -= max(0.0, (y - H * 0.55) / H) * 2.2               # darker toward the foot (ambient occlusion)
    v += max(0.0, (H * 0.18 - y) / H) * 2.0                # rim light at the top
    v += (nz(x, y, seed) - 0.5) * 0.7
    i = int(round(max(1, min(5, v))))
    c = rock[i]
    if vein and pal is PAL['S'] and smooth(x * 1.0, y * 0.5, seed + 9, 5.0) > 0.74 and i >= 2:
        c = pal['vein'][min(2, i - 2)]                     # rose halite veins through the salt
    return A(c)


STYLE = {'S': 'strata', 'L': 'slate', 'E': 'lumps', 'T': 'boards'}


def boards_px(pal, x, y, H, seed):
    """a timber wall: vertical boards between heavy posts, two horizontal rails, a tarred plinth at the foot"""
    rock = pal['rock']
    if x % 16 in (0, 1):                                    # the post
        return A(rock[1] if x % 16 == 0 else rock[3])
    if x % 16 == 15: return A(rock[0])
    if y in (9, 10, 30, 31):                                # rails
        return A(rock[4] if y in (9, 30) else rock[1])
    if y >= H - 10: return A(rock[1] if y % 3 else rock[0])  # tarred plinth
    board = (x - 2) // 3
    lvl = 2 + (board % 2) + (1 if nz(board, y // 7, seed) > 0.8 else 0)
    if (x - 2) % 3 == 2: lvl = 1                            # the board gaps
    if nz(x, y, seed + 3) > 0.96: lvl -= 1                  # knots
    if y < 3: lvl += 1
    return A(rock[max(1, min(5, lvl))])


def strata_px(pal, x, y, H, seed):
    """rock salt: horizontal bedding (grey, white, a faint rose bed now and then) broken by joints, lit from the left"""
    rock = pal['rock']
    yy = y + 0.55 * math.sin(2 * math.pi * x / 16.0 + seed * 0.7) + 0.35 * math.sin(2 * math.pi * x / 8.0 + seed)
    band = int(yy // 4)
    lvl = (2, 3, 4, 3, 2, 4)[int(nz(band, 0, seed) * 5.99)]
    vein = nz(band, 1, seed + 1) > 0.8
    f = yy % 4
    if f < 1: lvl += 1                                       # the lit top edge of each bed
    elif f >= 3.3 and nz(x, band, seed + 4) > 0.3: lvl -= 1
    blk = int((y + 3) // 7)
    j = int(nz(blk, 2, seed) * 16)
    if nz(blk, 3, seed) > 0.25:
        if x == j: return A(rock[1])
        if (x - j) % 16 == 1: lvl += 1
        if (j - x) % 16 == 1: lvl -= 1
    lvl -= int(max(0.0, (y - H * 0.62) / H) * 4.5)
    if y < 3: lvl += 1
    if nz(x, y, seed + 7) > 0.95: lvl += 1
    lvl = max(1, min(5, lvl))
    if vein and lvl >= 2: return A(pal['vein'][min(2, lvl - 2)])
    return A(rock[lvl])


def slate_px(pal, x, y, H, seed):
    """wet slate: thin laminations dipping a little, cleavage cracks, a wet sheen running down"""
    rock = pal['rock']
    yy = y + (x * 0.25) % 4 + 0.8 * math.sin(2 * math.pi * x / 16.0 + seed)
    lam = int(yy // 2)
    lvl = 2 + (lam % 2) + (1 if nz(lam, 4, seed) > 0.7 else 0)
    if (x + int(y * 0.5) + seed) % 9 == 0 and nz(x // 3, y // 4, seed) > 0.35: return A(rock[0])
    if (x + int(y * 0.5) + seed) % 9 == 1: lvl -= 1
    if (x * 5 + seed) % 13 == 0 and nz(x, y // 5, seed + 2) > 0.45: lvl = 5         # wet sheen
    lvl -= int(max(0.0, (y - H * 0.6) / H) * 4.5)
    if y < 3: lvl += 1
    lvl = max(1, min(5, lvl))
    if y > H - 9 and nz(x, y, seed + 3) > 0.8: return A(pal['vein'][2] if nz(x, y, 5) > 0.5 else pal['vein'][1])   # barnacles / weed at the foot
    return A(rock[lvl])


def wall_strip(pal, seed, rows, period=16, style='lumps'):
    """a period-wide strip of wall face, rows*16 tall"""
    H = rows * 16; pts = cells(seed, period, period, H)
    im = Image.new('RGBA', (period, H), CLEAR)
    for y in range(H):
        for x in range(period):
            if style == 'strata': c = strata_px(pal, x, y, H, seed)
            elif style == 'slate': c = slate_px(pal, x, y, H, seed)
            elif style == 'boards': c = boards_px(pal, x, y, H, seed)
            else: c = face_px(pal, pts, period, x, y, H, seed)
            im.putpixel((x, y), c)
    return im


def wall_kit(p):
    """N rim, W, E, three rows (lip / face / base) x (w, m, e), face alts, inner corners"""
    pal = PAL[p]; rock = pal['rock']; out = {}
    strips = [wall_strip(pal, 11 + 7 * v + ord(p), 3, style=STYLE[p]) for v in range(3)]

    def row_tile(strip, k, end):
        im = Image.new('RGBA', (16, 16), CLEAR)
        src = strip.crop((0, k * 16, 16, k * 16 + 16))
        for y in range(16):
            for x in range(16):
                c = src.getpixel((x, y)); yy = k * 16 + y
                # rounded ends: the w / e tiles curve in at the top (lip) and stand straight below
                if end == 'w':
                    edge = 3 if k else 3 + max(0, 3 - y // 2)
                    if x < edge: continue
                    if x == edge: c = A(rock[0]) if (y + x) % 5 else A(rock[1])
                    elif x == edge + 1: c = A(rock[4] if k == 0 and y < 9 else rock[2])
                if end == 'e':
                    edge = 12 if k else 12 - max(0, 3 - y // 2)
                    if x > edge: continue
                    if x == edge: c = A(rock[0])
                    elif x == edge - 1: c = A(rock[1])
                if k == 0:                                   # the lip: ground shows above, a lit rounded rim
                    top = 5 + (1 if nz(x, 0, 3) > 0.7 else 0) + (2 if end != 'm' and (x < 6 if end == 'w' else x > 9) else 0)
                    if y < top - 1: continue
                    if y == top - 1: c = A(rock[2], 220)
                    elif y == top: c = A(rock[5])
                    elif y == top + 1: c = A(rock[4])
                if k == 2:                                   # the base: foot line, a soft shadow and a few fallen chips
                    if y == 10: c = A(pal['foot'])
                    elif y == 11: c = A(pal['foot'], 150)
                    elif y == 12: c = A(pal['foot'], 70)
                    elif y > 12:
                        c = A(rock[2]) if nz(x, y, 5 + ord(p)) > 0.93 else None
                        if c is None: continue
                im.putpixel((x, y), c)
        return im

    for end in 'wme':
        for k, nm in enumerate(('lip', 'face', 'base')):
            out['%s_%s%s' % (p, nm, end)] = (row_tile(strips[0], k, end), ['W'], None)
    for v in (1, 2):
        out['%s_facem%d' % (p, v)] = (row_tile(strips[v], 1, 'm'), ['W'], None)
        out['%s_lipm%d' % (p, v)] = (row_tile(strips[v], 0, 'm'), ['W'], None)
    # north rim: the edge of the level above, seen from the room to its north - a lit crest and a dark drop line
    for end in 'wme':
        im = Image.new('RGBA', (16, 16), CLEAR)
        for x in range(16):
            if end == 'w' and x < 4 or end == 'e' and x > 11: continue
            yy = 1 + (1 if nz(x, 1, ord(p)) > 0.6 else 0)
            P(im, x, yy, A(rock[0], 230)); P(im, x, yy + 1, A(rock[5])); P(im, x, yy + 2, A(rock[3]))
            P(im, x, yy + 3, A(rock[2], 200))
            if nz(x, 9, ord(p)) > 0.75: P(im, x, yy + 4, A(rock[1], 160))
        out['%s_N%s' % (p, end)] = (im, ['W'], None)            # solid: in a cave the high side is usually rock
    for side in 'WE':
        im = Image.new('RGBA', (16, 16), CLEAR)
        for y in range(16):
            xs = (0, 1, 2, 3, 4) if side == 'W' else (15, 14, 13, 12, 11)
            cols = [A(rock[0]), A(rock[2] if side == 'W' else rock[1]), A(rock[4] if side == 'W' else rock[3]), A(rock[2], 150)]
            for k, xx in enumerate(xs[:4]):
                if k == 3 and nz(xx, y // 2, 3) > 0.5: continue
                P(im, xx, y, cols[k])
            if nz(y, 2, ord(p)) > 0.8: P(im, xs[1], y, A(rock[3]))
        out['%s_%s' % (p, side)] = (im, ['W'], None)
    # inner corners (a high cell beside a lower plateau's lip / first face row): the face turns the corner
    for side in 'WE':
        for k in (0, 1):
            src = row_tile(strips[0], k, 'm')
            im = Image.new('RGBA', (16, 16), CLEAR)
            for y in range(16):
                for x in range(16):
                    near = x if side == 'W' else 15 - x          # distance from the side the face comes from
                    if near < 9 - (y // 3 if k == 0 else 0):
                        c = src.getpixel((x, y))
                        if c[3]: im.putpixel((x, y), c)
                    elif near == 9 - (y // 3 if k == 0 else 0):
                        im.putpixel((x, y), A(rock[0]))
                    elif near == 10 - (y // 3 if k == 0 else 0):
                        im.putpixel((x, y), A(rock[3]))
            out['%s_in%s%d' % (p, side, k)] = (im, ['W'], None)
    return out


# ------------------------------------------------------------------ ground
def floor(p, v):
    pal = PAL[p]; fl = pal['floor']; im = Image.new('RGBA', (16, 16), CLEAR)
    for y in range(16):
        for x in range(16):
            n = smooth(x, y, 40 + ord(p), 4.0) * 0.7 + nz(x, y, 41 + v) * 0.3
            i = 1 if n < 0.36 else 2 if n < 0.62 else 3
            im.putpixel((x, y), A(fl[i]))
    r = random.Random(ord(p) * 10 + v)
    for _ in range((2, 3, 1, 4)[v]):                       # pebbles: lit top-left, shade under
        x, y = r.randrange(2, 13), r.randrange(2, 13)
        P(im, x, y, A(fl[4])); P(im, x + 1, y, A(fl[3])); P(im, x, y + 1, A(fl[3])); P(im, x + 1, y + 1, A(fl[0]))
        P(im, x + 2, y + 1, A(fl[1]))
    if v == 2:                                              # a hairline crack
        x, y = r.randrange(3, 8), r.randrange(4, 10)
        for i in range(7):
            P(im, x + i, y + (1 if i in (2, 3, 6) else 0), A(fl[0]))
    if v == 3 and p == 'S':                                 # salt sparkle
        for _ in range(4):
            P(im, r.randrange(1, 15), r.randrange(1, 15), A(PAL['S']['rock'][5]))
    return im


def floor_detail(p, v):
    pal = PAL[p]; fl = pal['floor']; im = Image.new('RGBA', (16, 16), CLEAR); r = random.Random(77 + v + ord(p))
    if v == 0:                                              # scattered gravel
        for _ in range(9):
            x, y = r.randrange(1, 15), r.randrange(1, 15)
            P(im, x, y, A(fl[4] if r.random() < 0.5 else fl[0]))
    elif v == 1:                                            # a worn rut / footpath scuff
        for x in range(16):
            y = 7 + int(1.3 * math.sin(x / 2.6 + ord(p)))
            P(im, x, y, A(fl[0], 170)); P(im, x, y + 1, A(fl[1], 140))
            if x % 3: P(im, x, y + 3, A(fl[0], 110))
    else:                                                   # crust: salt (S), weed-wrack (L), dry clay crazing (E)
        if p == 'S':
            for _ in range(5):
                cx, cy = r.randrange(3, 13), r.randrange(3, 13)
                for dx, dy in ((0, 0), (1, 0), (0, 1), (-1, 0), (0, -1)):
                    P(im, cx + dx, cy + dy, A(PAL['S']['rock'][5], 230))
                P(im, cx + 1, cy + 1, A(PAL['S']['vein'][1], 200))
        elif p == 'L':
            for _ in range(3):
                cx, cy = r.randrange(2, 12), r.randrange(3, 13)
                for i in range(5):
                    P(im, cx + i, cy + int(math.sin(i)), A(pal['vein'][0])); P(im, cx + i, cy - 1 + int(math.sin(i)), A(pal['vein'][1]))
        else:
            for _ in range(3):
                cx, cy = r.randrange(2, 12), r.randrange(2, 12)
                for i in range(6): P(im, cx + i, cy + (i % 3 == 0), A(fl[0]))
                for i in range(4): P(im, cx + 2, cy + i, A(fl[0]))
    return im


PATCH = {'S': 'crust', 'L': 'wet', 'E': 'dust'}


def floor_patches(p):
    """a soft-edged floor patch in the 48 autotile shapes (salt crust / wet shingle / trodden dust), layer 2 walk surface"""
    import gdraw
    fl = PAL[p]['floor']
    if p == 'S':
        body, rim, inner = (196, 190, 186), (214, 210, 206), (180, 172, 168)
        tex = lambda x, y, sh: A(PAL['S']['rock'][5] if nz(x, y, sh) > 0.9 else (200, 194, 190) if smooth(x, y, 51, 4.0) > 0.45 else (186, 178, 174))
    elif p == 'L':
        body, rim, inner = (64, 66, 70), (88, 90, 92), (70, 72, 76)
        tex = lambda x, y, sh: A((150, 156, 160) if nz(x, y, sh) > 0.9 else (60, 62, 68) if smooth(x, y, 52, 4.0) > 0.45 else (70, 72, 78))
    else:
        body, rim, inner = fl[1], fl[2], fl[1]
        tex = lambda x, y, sh: A(fl[0] if nz(x, y, sh) > 0.88 else fl[1])
    return gdraw.edge_shapes('%s_floorpatch' % p, A(body), A(rim), A(inner), A(fl[0], 120), 60 + ord(p), tex, R=5.0, amp=1.6)


def mass(p, tier, v):
    """the rock above the walls: lumpy rock-top lit faintly near the cave, fading into black further in"""
    pal = PAL[p]; m = pal['mass']; im = Image.new('RGBA', (16, 16), CLEAR)
    pts = cells(200 + v * 13 + ord(p), 16, 16, 16, sx=6.0, sy=6.0)
    for y in range(16):
        for x in range(16):
            best = (1e9, None); second = 1e9
            for px_, py_, k in pts:
                dx = (x - px_ + 8) % 16 - 8; dy = (y - py_ + 8) % 16 - 8
                d = dx * dx + dy * dy
                if d < best[0]: second = best[0]; best = (d, (dx, dy, k))
                elif d < second: second = d
            d1, (dx, dy, k) = best
            edge = math.sqrt(second) - math.sqrt(d1) < 0.8
            lit = -(dx + dy) / 6.0
            base = m[min(3, tier)]
            if tier >= 3:
                c = base if nz(x, y, v + 5) > 0.08 else m[2]
            elif edge:
                c = m[min(3, tier + 1)]
            else:
                hi = pal['rock'][1] if tier == 0 else m[max(0, tier - 1)]
                t = max(0.0, min(1.0, 0.5 + lit * 0.6 + (k - 0.5) * 0.3))
                c = tuple(int(base[i] + (hi[i] - base[i]) * t * (0.9 if tier == 0 else 0.6)) for i in range(3))
            im.putpixel((x, y), A(c))
    return im


def shadow(p):
    """the dark band at the foot of a wall, on the floor (darkness creeping out of the rock)"""
    im = Image.new('RGBA', (16, 16), CLEAR); f = PAL[p]['mass'][3]
    for y in range(16):
        a = int(max(0, 120 - y * 14))
        for x in range(16):
            if a and nz(x, y, 9) < 0.9: P(im, x, y, A(f, a))
    return im


def stairs(p, end):
    """rock-cut steps: four treads per tile, lit edges, cheek walls at the ends"""
    pal = PAL[p]; rock = pal['rock']; fl = pal['floor']; im = Image.new('RGBA', (16, 16), CLEAR)
    for y in range(16):
        k = y % 4
        for x in range(16):
            c = A(fl[4]) if k == 0 else A(fl[3]) if k == 1 else A(fl[2]) if k == 2 else A(rock[0])
            if nz(x, y // 4, 31) > 0.85 and k in (1, 2): c = A(fl[1])
            im.putpixel((x, y), c)
    for y in range(16):
        if end == 'l':
            for x, c in ((0, rock[0]), (1, rock[3]), (2, rock[2]), (3, rock[1])): P(im, x, y, A(c))
        if end == 'r':
            for x, c in ((15, rock[0]), (14, rock[1]), (13, rock[2]), (12, rock[1])): P(im, x, y, A(c))
    return im


def rock1(p, v):
    pal = PAL[p]; rock = pal['rock']; im = Image.new('RGBA', (16, 16), CLEAR)
    cx, cy, rx, ry = (8, 9, 6.2, 5.0) if v == 0 else (7.5, 10, 5.0, 4.2)
    for y in range(16):
        for x in range(16):
            dx, dy = (x + 0.5 - cx) / rx, (y + 0.5 - cy) / ry
            d = dx * dx + dy * dy
            if d > 1: continue
            if d > 0.78: c = rock[0]
            else:
                l = -(dx + dy * 1.2) * 1.3 + 2.6 + (nz(x, y, 3 + v) - 0.5) * 0.6
                c = rock[int(max(1, min(5, round(l))))]
            P(im, x, y, A(c))
    for x in range(int(cx - rx + 1), int(cx + rx)):
        P(im, x, int(cy + ry), A(pal['foot'], 120))
    if p == 'L':                                            # barnacles and weed
        for i in range(4): P(im, 5 + i * 2, 12 - (i % 2), A(pal['vein'][2]))
        for x in range(4, 12): P(im, x, 13, A(pal['vein'][0]))
    return im


def stalagmite(p):
    pal = PAL[p]; rock = pal['rock']; im = Image.new('RGBA', (16, 32), CLEAR)
    for y in range(4, 30):
        w = 1.2 + (y - 4) * 0.2
        for x in range(16):
            dx = x + 0.5 - 8
            if abs(dx) > w: continue
            if abs(dx) > w - 1: c = rock[0]
            else: c = rock[4] if dx < -w * 0.3 else rock[3] if dx < w * 0.2 else rock[2]
            if (y + int(dx)) % 6 == 0 and abs(dx) < w - 1: c = rock[2]
            P(im, x, y, A(c))
    for x in range(2, 14): P(im, x, 30, A(pal['foot'], 140))
    return im


def rubble(p, v):
    pal = PAL[p]; rock = pal['rock']; im = Image.new('RGBA', (16, 16), CLEAR); r = random.Random(900 + v + ord(p))
    for _ in range(5 + v * 2):
        x, y = r.randrange(2, 13), r.randrange(3, 13)
        P(im, x, y, A(rock[4])); P(im, x + 1, y, A(rock[2])); P(im, x, y + 1, A(rock[1])); P(im, x + 1, y + 1, A(rock[0]))
    return im


def crawl_mass(p):
    """a crawlway: the darkest mass tone, with a faint draught line only a careful eye reads"""
    im = mass(p, 1, 0)
    for x in range(3, 13):
        if nz(x, 0, 71) > 0.35: P(im, x, 8 + (x % 3 == 0), A(PAL[p]['mass'][3], 200))
    return im


# ------------------------------------------------------------------ shared pieces
def hole():
    """a shaft down: rock rim, black throat, ladder rails over the edge"""
    im = Image.new('RGBA', (16, 16), CLEAR)
    for y in range(16):
        for x in range(16):
            dx, dy = (x + 0.5 - 8) / 6.6, (y + 0.5 - 8.5) / 5.8
            d = dx * dx + dy * dy
            if d <= 1:
                P(im, x, y, (10, 8, 14, 255) if d < 0.62 else (36, 30, 34, 255) if dy < 0 else (64, 56, 58, 255))
    for x in (5, 10):
        for y in range(3, 13): P(im, x, y, WOOD[2] if y < 6 else WOOD[1])
    for y in (4, 7, 10):
        for x in range(6, 10): P(im, x, y, WOOD[3] if y == 4 else WOOD[1])
    return im


def ladder_up():
    """ladder up a wall: the top tile is a dark hole in the face, the foot stands on the floor"""
    im = Image.new('RGBA', (16, 32), CLEAR)
    for y in range(2, 14):
        for x in range(4, 12):
            if (x - 7.5) ** 2 / 16 + (y - 8) ** 2 / 36 <= 1: P(im, x, y, (12, 10, 16, 255))
    for x in (5, 10):
        for y in range(4, 30): P(im, x, y, WOOD[3] if x == 5 else WOOD[1])
    for y in range(6, 29, 4):
        for x in range(6, 10): P(im, x, y, WOOD[2]); P(im, x, y + 1, WOOD[0])
    for x in range(4, 12): P(im, x, 30, (0, 0, 0, 90))
    return im


def crystal(col, tall, seed):
    """a cluster of hexagonal crystals: lit face, shade face, white edge; tall = 1x2 spire cluster"""
    H = 32 if tall else 16
    im = Image.new('RGBA', (16, H), CLEAR); r = random.Random(seed)
    specs = [(8, H - 2, 3.2, H - 6 if tall else 11), (4, H - 1, 2.2, (H - 6) * 0.55 if tall else 7), (12, H - 1, 2.0, (H - 6) * 0.45 if tall else 6)]
    for cx, base, w, h in sorted(specs, key=lambda s: -s[3]):
        lean = r.uniform(-0.15, 0.15)
        for y in range(int(base - h), base):
            t = (base - y) / h
            ww = w * (1.0 if t < 0.75 else (1 - t) / 0.25)
            mid = cx + lean * (base - y)
            for x in range(int(mid - ww - 1), int(mid + ww + 2)):
                dx = x + 0.5 - mid
                if abs(dx) > ww: continue
                c = col[2] if dx < -ww * 0.15 else col[1]
                if abs(dx) > ww - 0.9: c = col[0]
                if -ww * 0.3 < dx < -ww * 0.05 and t > 0.2: c = col[3]
                P(im, x, y, A(c))
    for x in range(3, 14): P(im, x, H - 1, (0, 0, 0, 70))
    return im


def halite():
    """Brinecut's salt: cubic halite crystals stacked in a rose-white cluster"""
    im = Image.new('RGBA', (16, 16), CLEAR)
    for (x0, y0, s) in ((2, 7, 6), (8, 5, 6), (6, 10, 5), (10, 10, 4)):
        for y in range(y0, y0 + s):
            for x in range(x0, x0 + s):
                c = XSALT[3] if y == y0 else XSALT[2] if x < x0 + s // 2 else XSALT[1]
                if x == x0 + s - 1 or y == y0 + s - 1: c = XSALT[0]
                P(im, x, y, A(c))
        P(im, x0 + 1, y0 + 1, A(XSALT[3]))
    return im


def fungus(v):
    col = FUNG if v == 0 else FUNGA
    im = Image.new('RGBA', (16, 16), CLEAR); r = random.Random(500 + v)
    for cx, cy, rr in ((5, 10, 2.6), (10, 8, 3.2), (11, 13, 1.8), (3, 13, 1.6)):
        for y in range(int(cy), int(cy + 3)):
            P(im, int(cx), y, A(col[0])); P(im, int(cx) + 1, y, A(col[1]))
        for y in range(int(cy - rr), int(cy + 1)):
            for x in range(int(cx - rr), int(cx + rr + 2)):
                dx, dy = x + 0.5 - cx - 0.5, y + 0.5 - cy
                if dx * dx / (rr * rr) + dy * dy / (rr * rr * 0.5) > 1: continue
                c = col[2] if dx < 0.3 else col[1]
                if dy > -0.6: c = col[0]
                P(im, x, y, A(c))
        P(im, int(cx - rr * 0.4), int(cy - rr * 0.5), A(col[3]))
    return im


def shelf_fungus():
    im = Image.new('RGBA', (16, 16), CLEAR)
    for (cx, cy, w) in ((6, 6, 5), (10, 11, 4), (4, 12, 3)):
        for x in range(cx - w, cx + w + 1):
            hgt = int(2 + 1.5 * math.cos((x - cx) / w * 1.4))
            for y in range(cy - hgt, cy + 1):
                P(im, x, y, A(FUNG[2] if y == cy - hgt else FUNG[1] if y < cy else FUNG[0]))
    return im


RAIL_H = 'h'


def rail(kind):
    """rails on the floor: two iron rails on wooden sleepers (decal over the floor)"""
    im = Image.new('RGBA', (16, 16), CLEAR)
    def sleeper_h(x):
        for y in range(3, 13): P(im, x, y, WOOD[1]); P(im, x + 1, y, WOOD[2])
    def sleeper_v(y):
        for x in range(3, 13): P(im, x, y, WOOD[1]); P(im, x, y + 1, WOOD[2])
    if kind == 'h':
        for x in (1, 6, 11): sleeper_h(x)
        for x in range(16):
            for y, c in ((4, IRON[3]), (5, IRON[1]), (10, IRON[3]), (11, IRON[1])): P(im, x, y, c)
    elif kind == 'v':
        for y in (1, 6, 11): sleeper_v(y)
        for y in range(16):
            for x, c in ((4, IRON[3]), (5, IRON[1]), (10, IRON[3]), (11, IRON[1])): P(im, x, y, c)
    else:                                   # curves: ne / nw / se / sw join the two named sides
        cx = 16 if 'e' in kind else 0; cy = 0 if 'n' in kind else 16
        for y in range(16):
            for x in range(16):
                d = math.hypot(x + 0.5 - cx, y + 0.5 - cy)
                if 6.6 < d < 8.2 and nz(x, y, 1) < 2: P(im, x, y, WOOD[1])
        for y in range(16):
            for x in range(16):
                d = math.hypot(x + 0.5 - cx, y + 0.5 - cy)
                if 4.0 <= d < 5.0 or 10.0 <= d < 11.0: P(im, x, y, IRON[3])
                elif 5.0 <= d < 5.8 or 11.0 <= d < 11.8: P(im, x, y, IRON[1])
    return im


def trestle(kind):
    """rails on a timber trestle across a chasm: heavy stringers under the rails, posts dropping into the dark"""
    im = Image.new('RGBA', (16, 16), CLEAR)
    if kind in ('h', 'v'):
        for i in range(16):
            for d, c in ((2, WOOD[0]), (3, WOOD[2]), (12, WOOD[1]), (13, WOOD[0])):
                if kind == 'h': P(im, i, d, c)
                else: P(im, d, i, c)
        for k in (2, 9):                                  # posts fading down into the chasm
            for j in range(4):
                a = 200 - j * 50
                if kind == 'h': P(im, k, 14 + j // 2, A(WOOD[0], a)); P(im, k + 4, 14 + j // 2, A(WOOD[0], a))
        rl = rail(kind)
        im.alpha_composite(rl)
    else:
        rl = rail(kind)
        cx = 16 if 'e' in kind else 0; cy = 0 if 'n' in kind else 16
        for y in range(16):
            for x in range(16):
                d = math.hypot(x + 0.5 - cx, y + 0.5 - cy)
                if 2.6 <= d < 3.6 or 12.0 <= d < 13.0: P(im, x, y, WOOD[1])
        im.alpha_composite(rl)
    return im


def points():
    """a points plate where the line forks: an iron plate, the switch blade and its rod"""
    im = Image.new('RGBA', (16, 16), CLEAR)
    for y in range(2, 14):
        for x in range(2, 14):
            P(im, x, y, IRON[1] if (x + y) % 5 else IRON[0])
    for x in range(2, 14): P(im, x, 2, IRON[3]); P(im, x, 13, IRON[0])
    for y in range(2, 14): P(im, 2, y, IRON[2]); P(im, 13, y, IRON[0])
    for i in range(10):
        P(im, 4 + i, 4 + i // 2, IRON[3]); P(im, 4 + i, 11 - i // 2, IRON[2])
    disc(im, 8, 8, 1.5, (196, 60, 48, 255))
    return im


def pit(v):
    """the chasm floor seen from above: black, with a faint far-down glint of brine"""
    im = Image.new('RGBA', (16, 16), CLEAR)
    for y in range(16):
        for x in range(16):
            c = (8, 7, 12) if nz(x, y, 300 + v) > 0.04 else (30, 40, 48)
            P(im, x, y, A(c))
    return im


def rail_end(direction):
    """a buffer stop at the end of a line: timber block with iron straps"""
    im = rail('v' if direction in 'ns' else 'h')
    if direction == 'n':
        for y in range(1, 7):
            for x in range(2, 14): P(im, x, y, WOOD[2] if y < 3 else WOOD[1])
        for x in range(2, 14): P(im, x, 1, WOOD[3]); P(im, x, 6, WOOD[0])
        for x in (4, 11):
            for y in range(1, 7): P(im, x, y, IRON[2])
    return im


def cart(salt=False):
    im = Image.new('RGBA', (16, 16), CLEAR)
    for y in range(4, 13):
        for x in range(2, 14):
            c = IRON[2] if y == 4 else IRON[1] if x < 4 or x > 11 else IRON[0] if y > 10 else (96, 70, 52, 255)
            P(im, x, y, c)
    for x in range(2, 14): P(im, x, 4, IRON[3]); P(im, x, 12, IRON[0])
    for x in (3, 7, 12):
        for y in range(5, 12): P(im, x, y, IRON[2])
    for x in (4, 11):
        disc(im, x + 0.5, 13.5, 1.6, IRON[0]); P(im, x, 13, IRON[3])
    if salt:
        for y in range(1, 6):
            for x in range(3 + (5 - y) // 2, 13 - (5 - y) // 2):
                P(im, x, y, A(XSALT[3] if (x + y) % 3 else XSALT[2]))
    else:
        for x in range(4, 12): P(im, x, 5, (40, 30, 26, 255))
    return im


def lever(right):
    im = Image.new('RGBA', (16, 16), CLEAR)
    for y in range(9, 14):
        for x in range(4, 12): P(im, x, y, WOOD[1] if y > 9 else WOOD[3])
    for x in range(4, 12): P(im, x, 14, (0, 0, 0, 80))
    bx = 8
    for i in range(8):
        x = bx + (i // 2 if right else -i // 2); y = 9 - i
        P(im, x, y, IRON[2]); P(im, x + 1, y, IRON[1])
    hx = bx + (4 if right else -4)
    disc(im, hx + 0.5, 2.5, 1.8, (196, 60, 48, 255)); P(im, hx, 2, (240, 140, 120, 255))
    # the painted arrow on the box shows which way the points are set
    for i in range(3):
        P(im, (9 + i) if right else (6 - i), 11, (236, 214, 150, 255))
    return im


def pit_frame():
    """a pit-prop frame over a gallery mouth: two posts and a lintel (3x2; the lintel is overhead)"""
    im = Image.new('RGBA', (48, 32), CLEAR)
    for x in range(1, 47):
        for y in range(2, 8):
            P(im, x, y, WOOD[3] if y == 2 else WOOD[2] if y < 5 else WOOD[1])
        P(im, x, 8, (0, 0, 0, 90))
    for x0 in (2, 40):
        for y in range(2, 31):
            for x in range(x0, x0 + 6):
                P(im, x, y, WOOD[2] if x < x0 + 2 else WOOD[1] if x < x0 + 5 else WOOD[0])
        for y in range(4, 30, 7): P(im, x0 + 1, y, WOOD[3])
    for x in (6, 41): P(im, x, 9, IRON[1]); P(im, x, 10, IRON[2])
    return im


def post():
    im = Image.new('RGBA', (16, 32), CLEAR)
    for y in range(3, 30):
        for x in range(6, 11): P(im, x, y, WOOD[2] if x < 8 else WOOD[1] if x < 10 else WOOD[0])
    for x in range(3, 14):
        P(im, x, 3, WOOD[3]); P(im, x, 4, WOOD[2]); P(im, x, 5, WOOD[1])
    for x in range(5, 12): P(im, x, 30, (0, 0, 0, 80))
    return im


def lamp(on):
    """a miner's lamp on a post (1x2): glass lantern with a warm glow when lit"""
    im = Image.new('RGBA', (16, 32), CLEAR)
    if on:
        for y in range(0, 16):
            for x in range(16):
                d = math.hypot(x + 0.5 - 8, y + 0.5 - 9)
                if d < 7.5: P(im, x, y, A(GLOW[2], int(max(0, 90 - d * 12))))
    for y in range(14, 30):
        for x in range(7, 10): P(im, x, y, WOOD[2] if x == 7 else WOOD[1])
    for x in range(5, 12): P(im, x, 30, (0, 0, 0, 80))
    for y in range(5, 14):
        for x in range(5, 12):
            c = IRON[1] if x in (5, 11) or y in (5, 13) else ((GLOW[2] if (x < 8) else GLOW[1]) if on else (66, 70, 82, 255))
            P(im, x, y, c)
    if on: P(im, 7, 8, GLOW[3]); P(im, 7, 9, GLOW[3])
    for x in range(6, 11): P(im, x, 4, IRON[2])
    P(im, 8, 3, IRON[2])
    return im


def wall_lamp(on=True):
    im = Image.new('RGBA', (16, 16), CLEAR)
    if on:
        for y in range(16):
            for x in range(16):
                d = math.hypot(x + 0.5 - 8, y + 0.5 - 8)
                if d < 8: P(im, x, y, A(GLOW[2], int(max(0, 80 - d * 10))))
    for x in range(4, 12): P(im, x, 4, IRON[1])
    for y in range(5, 12):
        for x in range(5, 11):
            P(im, x, y, IRON[1] if x in (5, 10) or y in (5, 11) else (GLOW[2] if x < 8 else GLOW[1]) if on else (66, 70, 82, 255))
    return im


def tools():
    im = Image.new('RGBA', (16, 16), CLEAR)
    for y in range(2, 15):
        P(im, 4, y, WOOD[2]); P(im, 11, y, WOOD[1])
    for x in range(3, 13): P(im, x, 3, WOOD[3]); P(im, x, 4, WOOD[1])
    for i, x in enumerate((6, 9)):
        for y in range(5, 14): P(im, x, y, WOOD[3] if i == 0 else WOOD[2])
    for x in range(4, 9): P(im, x, 5, IRON[3]); P(im, x, 6, IRON[1])       # pick head
    for x in range(8, 11): P(im, x, 12, IRON[2]); P(im, x, 13, IRON[1])     # shovel blade
    for x in range(3, 14): P(im, x, 15, (0, 0, 0, 80))
    return im


def salt_blocks():
    im = Image.new('RGBA', (32, 16), CLEAR)
    for (x0, y0) in ((1, 7), (11, 7), (21, 7), (6, 1), (16, 1)):
        for y in range(y0, y0 + 7):
            for x in range(x0, x0 + 10):
                c = XSALT[3] if y == y0 else XSALT[2] if x < x0 + 6 else XSALT[1]
                if x == x0 + 9 or y == y0 + 6: c = XSALT[0]
                P(im, x, y, A(c))
    for x in range(1, 31): P(im, x, 14, (0, 0, 0, 80))
    return im


def pump():
    """the B1F brine pump: a wheel on an iron frame over a sump (2x2)"""
    im = Image.new('RGBA', (32, 32), CLEAR)
    for y in range(18, 30):
        for x in range(3, 29): P(im, x, y, IRON[1] if y > 19 else IRON[2])
    for x in range(3, 29): P(im, x, 30, (0, 0, 0, 90))
    cx, cy = 16, 13
    for a in range(0, 360, 3):
        for rr in (9, 10):
            P(im, cx + rr * math.cos(math.radians(a)), cy + rr * math.sin(math.radians(a)), WOOD[2] if rr == 9 else WOOD[1])
    for a in range(0, 360, 45):
        for rr in range(2, 9):
            P(im, cx + rr * math.cos(math.radians(a)), cy + rr * math.sin(math.radians(a)), WOOD[3])
    disc(im, cx, cy, 2.2, IRON[2]); P(im, cx - 1, cy - 1, IRON[3])
    return im


def barnacle_rock():
    im = rock1('L', 0)
    r = random.Random(4)
    for _ in range(10):
        x, y = r.randrange(4, 12), r.randrange(6, 13)
        if im.getpixel((x, y))[3]: P(im, x, y, A(PAL['L']['vein'][2])); P(im, x + 1, y + 1, A(PAL['L']['rock'][1]))
    return im


def kelp(v):
    im = Image.new('RGBA', (16, 16), CLEAR); r = random.Random(60 + v)
    for _ in range(3 + v):
        x0, y0 = r.randrange(1, 12), r.randrange(4, 14)
        for i in range(6):
            x = x0 + i; y = y0 - int(1.5 * math.sin(i / 1.6 + v))
            P(im, x, y, A((52, 84, 48) if i % 2 else (78, 112, 60))); P(im, x, y + 1, A((34, 52, 34), 200))
    return im


def wrack():
    im = Image.new('RGBA', (16, 16), CLEAR); r = random.Random(8)
    for x in range(16):
        y = 9 + int(2 * math.sin(x / 2.7))
        P(im, x, y, A((70, 60, 44))); P(im, x, y + 1, A((96, 84, 58), 200))
        if r.random() < 0.3: P(im, x, y - 1, A((206, 200, 178)))     # shell bits
    return im


def nest():
    im = Image.new('RGBA', (16, 16), CLEAR)
    for y in range(8, 15):
        for x in range(2, 14):
            if (x - 7.5) ** 2 / 36 + (y - 11) ** 2 / 9 <= 1:
                P(im, x, y, WOOD[2] if (x + y) % 3 else WOOD[3])
    for y in range(9, 12):
        for x in range(4, 12):
            if (x - 7.5) ** 2 / 12 + (y - 10) ** 2 / 2 <= 1: P(im, x, y, WOOD[0])
    for (x, y) in ((6, 9), (9, 9), (7, 10)):
        disc(im, x + 0.5, y + 0.5, 1.3, (220, 214, 196, 255)); P(im, x, y, (246, 244, 232, 255)); P(im, x + 1, y + 1, (120, 130, 110, 255))
    return im


def guano():
    im = Image.new('RGBA', (16, 16), CLEAR); r = random.Random(3)
    for _ in range(4):
        x = r.randrange(2, 14); y0 = r.randrange(0, 6)
        for y in range(y0, y0 + r.randrange(5, 11)):
            P(im, x + (y % 5 == 0), y, A((228, 226, 214), 220))
    return im


def driftwood():
    im = Image.new('RGBA', (32, 16), CLEAR)
    for x in range(2, 30):
        y = 8 + int(1.2 * math.sin(x / 5))
        for d in range(-2, 3):
            P(im, x, y + d, A((150, 140, 122)) if d < 0 else A((118, 106, 90)) if d < 2 else A((84, 74, 64)))
    for x in range(3, 30): P(im, x, 12, (0, 0, 0, 70))
    for (x, y) in ((8, 5), (20, 4)):
        for i in range(3): P(im, x + i, y + i, A((118, 106, 90)))
    return im


def light_shaft():
    """daylight through a blowhole: a soft pale-blue beam falling right-down (2x3, overhead, see-through)"""
    im = Image.new('RGBA', (32, 48), CLEAR)
    for y in range(48):
        x0 = 4 + y * 0.35; x1 = 16 + y * 0.35
        for x in range(32):
            if x0 <= x <= x1:
                edge = min(x - x0, x1 - x) / 3.0
                a = int(min(1.0, edge) * (70 - y * 0.6))
                if a > 0: P(im, x, y, (214, 236, 250, a))
    for y in range(40, 48):
        for x in range(12, 28):
            if (x - 20) ** 2 / 64 + (y - 45) ** 2 / 9 <= 1: P(im, x, y, (230, 246, 255, 60))
    return im


def tide_rock(wet):
    """the tide-mark rock: dry it shows a pale band, wet the sea has turned it dark and glossy"""
    im = rock1('L', 1)
    for y in range(16):
        for x in range(16):
            c = im.getpixel((x, y))
            if not c[3]: continue
            if wet and y > 7: P(im, x, y, A(SEA[1] if (x + y) % 4 else SEA[3]))
            if not wet and y == 9: P(im, x, y, A((214, 206, 176)))
    return im


def flood():
    """a sand bar under the tide: shallow sea, too strong to wade (solid)"""
    im = Image.new('RGBA', (16, 16), CLEAR)
    for y in range(16):
        for x in range(16):
            n = smooth(x, y, 91, 4.0)
            c = SEA[2] if n < 0.45 else SEA[3] if n < 0.8 else SEA[4]
            if (x + 2 * y) % 11 == 0 and n > 0.5: c = SEA[4]
            P(im, x, y, A(c))
    return im


def sand_bar():
    im = Image.new('RGBA', (16, 16), CLEAR)
    for y in range(16):
        for x in range(16):
            n = smooth(x, y, 92, 4.0) * 0.7 + nz(x, y, 93) * 0.3
            c = SAND[1] if n < 0.3 else SAND[2] if n < 0.68 else SAND[3]
            P(im, x, y, A(c))
    r = random.Random(5)
    for _ in range(4):
        x, y = r.randrange(1, 15), r.randrange(1, 15); P(im, x, y, A(SAND[4]))
    for x in range(16):                                  # ripple marks
        for y0 in (4, 10):
            if (x + y0) % 4 < 2: P(im, x, y0 + int(math.sin(x / 2.5)), A(SAND[0], 140))
    return im


def chalk_x():
    im = Image.new('RGBA', (16, 16), CLEAR)
    for i in range(7):
        P(im, 5 + i, 4 + i, (240, 236, 226, 230)); P(im, 11 - i, 4 + i, (240, 236, 226, 230))
    for x in range(5, 12): P(im, x, 13, (240, 236, 226, 200))
    return im


def pieces():
    import rdraw, ndraw
    rdraw.CODE.update(ndraw.CODES); rdraw.CODE.update(CODES)
    out = {}
    for p in 'SLE':
        out.update(wall_kit(p))
        for v in range(4): out['%s_f%d' % (p, v)] = (floor(p, v), ['G'], None)
        for v in range(3): out['%s_fd%d' % (p, v)] = (floor_detail(p, v), ['V'], None)
        for t in range(4):
            for v, s in enumerate('ab'):
                out['%s_m%d%s' % (p, t, s)] = (mass(p, t, v), ['M'], None)
        out['%s_mP' % p] = (crawl_mass(p), ['G'], None)
        for n, im in floor_patches(p).items(): out[n] = (im, ['D'], None)
        out['%s_shadow' % p] = (shadow(p), ['V'], None)
        rock = PAL[p]['rock']
        for e in 'wme':
            out['%sl_%s' % (p, e)] = (ndraw.ledge(e, face=[A(rock[1]), A(rock[2]), A(rock[3]), A(rock[4])],
                                                  top=[A(rock[0]), A(rock[2]), A(rock[3]), A(rock[4]), A(rock[5])]), ['L'], None)
        for e in 'lmr': out['%s_stair%s' % (p, e)] = (stairs(p, e), ['D'], None)
        for v in range(2): out['%s_rock%d' % (p, v)] = (rock1(p, v), ['W'], None)
        out['%s_stal' % p] = (stalagmite(p), ['R', 'W'], None)
        for v in range(2): out['%s_rubble%d' % (p, v)] = (rubble(p, v), ['V'], None)
    out['cv_hole'] = (hole(), ['D'], None)
    out['cv_ladder'] = (ladder_up(), ['X', 'D'], None)
    out['cv_xsalt'] = (halite(), ['W'], None)
    out['cv_xblue'] = (crystal(XBLUE, False, 3), ['W'], None)
    out['cv_xblue2'] = (crystal(XBLUE, True, 4), ['R', 'W'], None)
    out['cv_xsea'] = (crystal(XSEA, False, 5), ['W'], None)
    out['cv_xsea2'] = (crystal(XSEA, True, 6), ['R', 'W'], None)
    out['cv_xrose2'] = (crystal(XSALT, True, 7), ['R', 'W'], None)
    for v in range(2): out['cv_fung%d' % v] = (fungus(v), ['V'], None)
    out['cv_shelf'] = (shelf_fungus(), ['X'], None)
    for k in ('h', 'v', 'ne', 'nw', 'se', 'sw'): out['cv_rail_' + k] = (rail(k), ['D'], None)
    out['cv_rail_end'] = (rail_end('n'), ['W'], None)
    for k in ('h', 'v', 'ne', 'nw', 'se', 'sw'): out['cv_tres_' + k] = (trestle(k), ['W'], None)
    out['cv_points'] = (points(), ['D'], None)
    out['cv_points_tres'] = (points(), ['W'], None)
    for v in range(2): out['cv_pit%d' % v] = (pit(v), ['M'], None)
    out['cv_cart'] = (cart(False), ['W'], None)
    out['cv_cart_salt'] = (cart(True), ['W'], None)
    out['cv_lever_l'] = (lever(False), ['W'], None)
    out['cv_lever_r'] = (lever(True), ['W'], None)
    out['cv_frame'] = (pit_frame(), ['RRR', 'W.W'], None)
    out['cv_post'] = (post(), ['R', 'W'], None)
    out['cv_lamp_on'] = (lamp(True), ['R', 'W'], None)
    out['cv_lamp_off'] = (lamp(False), ['R', 'W'], None)
    out['cv_walllamp'] = (wall_lamp(True), ['X'], None)
    out['cv_walllamp_off'] = (wall_lamp(False), ['X'], None)
    out['cv_tools'] = (tools(), ['W'], None)
    out['cv_saltblocks'] = (salt_blocks(), ['WW'], None)
    out['cv_pump'] = (pump(), ['WW', 'WW'], None)
    out['cv_barn'] = (barnacle_rock(), ['W'], None)
    for v in range(2): out['cv_kelp%d' % v] = (kelp(v), ['V'], None)
    out['cv_wrack'] = (wrack(), ['V'], None)
    out['cv_nest'] = (nest(), ['W'], None)
    out['cv_guano'] = (guano(), ['X'], None)
    out['cv_drift'] = (driftwood(), ['WW'], None)
    out['cv_shaft'] = (light_shaft(), ['OO', 'OO', 'OO'], None)
    out['cv_tide_dry'] = (tide_rock(False), ['W'], None)
    out['cv_tide_wet'] = (tide_rock(True), ['W'], None)
    out['cv_flood'] = (flood(), ['W'], None)
    out['cv_bar'] = (sand_bar(), ['G'], None)
    out['cv_chalkx'] = (chalk_x(), ['X'], None)
    # map builder 13, Gym 3 (Tidelock): the timber lock hall kit, flagstones, mud, rafts, gates, wheels, the race
    out.update(wall_kit('T'))
    for v in range(4): out['T_f%d' % v] = (flags(v), ['G'], None)
    for t in range(4):
        for v, s_ in enumerate('ab'):
            out['T_m%d%s' % (t, s_)] = (mass('T', t, v), ['M'], None)
    out['T_shadow'] = (shadow('T'), ['V'], None)
    for v in range(4): out['cv_mud%d' % v] = (mud(v), ['G'], None)
    for k in 'tmb':
        out['cv_raft_' + k] = (raft(k, 'float'), ['D'], None)
        out['cv_raftS_' + k] = (raft(k, 'float'), ['W'], None)
        out['cv_raftG_' + k] = (raft(k, 'ground'), ['W'], None)
    out['cv_gate_shut'] = (lock_gate(True), ['W'], None)
    out['cv_gate_open'] = (lock_gate(False), ['W'], None)
    out['cv_sluice'] = (sluice_wheel(), ['W'], None)
    out['cv_sluice_hi'] = (sluice_wheel(True), ['W'], None)
    for v in range(2): out['cv_race%d' % v] = (race(v), ['X'], None)
    out['cv_chain'] = (chain(), ['X'], None)
    out['cv_window'] = (window(), ['X'], None)
    out['cv_ladder_q'] = (quay_ladder(), ['D'], None)
    out['cv_banner'] = (union_banner(), ['X', 'X'], None)
    return out


def flags(v):
    """grey-blue stone flags, the Ebbmouth quays' stone: courses of slabs, worn edges, a little water in the joints"""
    fl = PAL['T']['floor']; im = Image.new('RGBA', (16, 16), CLEAR)
    for y in range(16):
        for x in range(16):
            row = y // 8; off = 4 if row % 2 else 0
            jx = (x + off) % 8 == 0; jy = y % 8 == 0
            n = smooth(x, y, 70, 4.0) * 0.6 + nz((x + off) // 8, row, 71 + v) * 0.4
            c = fl[1] if n < 0.4 else fl[2] if n < 0.7 else fl[3]
            if jx or jy: c = fl[0]
            elif (x + off) % 8 == 1 or y % 8 == 1: c = fl[min(4, fl.index(c) + 1)]
            im.putpixel((x, y), A(c))
    r = random.Random(80 + v)
    for _ in range(v):
        P(im, r.randrange(2, 14), r.randrange(2, 14), A(fl[4]))
    return im


def mud(v):
    """the lock bed at low water: wet river mud, weed and puddles"""
    im = Image.new('RGBA', (16, 16), CLEAR); r = random.Random(120 + v)
    M_ = [(44, 40, 38), (62, 56, 50), (80, 72, 62), (100, 92, 80)]
    for y in range(16):
        for x in range(16):
            n = smooth(x, y, 121, 4.0) * 0.7 + nz(x, y, 122 + v) * 0.3
            im.putpixel((x, y), A(M_[0] if n < 0.25 else M_[1] if n < 0.55 else M_[2]))
    if v in (1, 3):                                          # a puddle catching the light
        cx, cy = r.randrange(4, 11), r.randrange(4, 11)
        for y in range(cy - 2, cy + 2):
            for x in range(cx - 3, cx + 3):
                if (x - cx) ** 2 / 9 + (y - cy + 0.5) ** 2 / 3 <= 1: P(im, x, y, A((58, 80, 96) if y > cy - 1 else (96, 124, 140)))
    if v in (2, 3):
        for _ in range(3):
            x0, y0 = r.randrange(1, 12), r.randrange(3, 14)
            for i in range(4): P(im, x0 + i, y0 - (i % 2), A((54, 76, 48)))
    return im


def raft(k, mode):
    """a log raft, three tiles long north-south (t / m / b): logs lashed with rope; grounded = sat in the mud"""
    im = Image.new('RGBA', (16, 16), CLEAR)
    for x in range(1, 15):
        lg = (x - 1) // 3
        for y in range(16):
            if k == 't' and y < 2 + (lg % 2): continue
            if k == 'b' and y > 13 - (lg % 2): continue
            c = WOOD[2] if (x - 1) % 3 == 0 else WOOD[3] if (x - 1) % 3 == 1 else WOOD[1]
            if y % 6 == 0 and k != 't': c = WOOD[0]
            P(im, x, y, c)
    for y in (5, 11):
        for x in range(1, 15): P(im, x, y, (196, 170, 120, 255))       # rope lashings
    if mode == 'ground':
        for x in range(1, 15):
            if k == 'b': P(im, x, 14, (44, 40, 38, 200)); P(im, x, 15, (44, 40, 38, 120))
    else:
        for x in (0, 15):
            for y in range(16):
                if (y + x) % 4 == 0: P(im, x, y, (196, 230, 240, 160))   # ripples along the logs
    return im


def lock_gate(shut):
    """a lock gate leaf: heavy timber with iron straps; open, the leaves stand folded against the walls"""
    im = Image.new('RGBA', (16, 16), CLEAR)
    if shut:
        for y in range(16):
            for x in range(5, 11):
                P(im, x, y, WOOD[2] if x < 7 else WOOD[1] if x < 10 else WOOD[0])
        for y in (2, 7, 12):
            for x in range(5, 11): P(im, x, y, IRON[2])
        for y in range(16): P(im, 4, y, (0, 0, 0, 70)); P(im, 11, y, (230, 240, 246, 120))
    else:
        for y in range(16):
            for x in (0, 1, 14, 15): P(im, x, y, WOOD[2] if x in (0, 14) else WOOD[0])
        for y in (2, 7, 12): P(im, 0, y, IRON[2]); P(im, 15, y, IRON[2])
    return im


def sluice_wheel(hi=False):
    """a sluice wheel on a post, union-stamped: red rim, iron spokes; hi = the wheel stands raised"""
    im = Image.new('RGBA', (16, 16), CLEAR)
    for y in range(9, 16):
        for x in range(6, 10): P(im, x, y, WOOD[2] if x < 8 else WOOD[1])
    cx, cy = 8, 7 if not hi else 6
    for a_ in range(0, 360, 8):
        for rr in (5.0, 5.8):
            P(im, cx + rr * math.cos(math.radians(a_)), cy + rr * math.sin(math.radians(a_)), (178, 52, 44, 255) if rr < 5.5 else (110, 30, 30, 255))
    for a_ in range(0, 360, 60):
        for rr in range(1, 5): P(im, cx + rr * math.cos(math.radians(a_)), cy + rr * math.sin(math.radians(a_)), IRON[2])
    disc(im, cx, cy, 1.4, IRON[3])
    return im


def race(v):
    """white water in a race: a current running north, foam streaks over the dark water"""
    im = Image.new('RGBA', (16, 16), CLEAR)
    for x in range(16):
        for y in range(16):
            yy = (y + v * 5 + int(2 * math.sin(x / 2.5))) % 8
            if yy in (0, 1) and nz(x, y // 2, 4 + v) > 0.25: P(im, x, y, (226, 242, 248, 200 if yy == 0 else 120))
    for x in (2, 7, 12):
        for y in range(4): P(im, x + (v % 2), (y * 4 + v * 2) % 16, (255, 255, 255, 220))
    return im


def chain():
    im = Image.new('RGBA', (16, 16), CLEAR)
    for y in range(0, 16, 3):
        P(im, 7, y, IRON[2]); P(im, 8, y, IRON[3]); P(im, 7, y + 1, IRON[1]); P(im, 9, y + 1, IRON[1]); P(im, 8, y + 2, IRON[0])
    return im


def window():
    """a high window in a timber wall: grey daylight through small panes"""
    im = Image.new('RGBA', (16, 16), CLEAR)
    for y in range(3, 13):
        for x in range(4, 12):
            c = (176, 200, 220, 255) if (x + y) % 5 else (220, 236, 246, 255)
            if x in (4, 11) or y in (3, 12) or x == 8 or y == 7: c = WOOD[1]
            P(im, x, y, c)
    for x in range(3, 13): P(im, x, 13, WOOD[3])
    return im


def quay_ladder():
    """iron rungs down a quay wall into the lock bed"""
    im = Image.new('RGBA', (16, 16), CLEAR)
    for y in range(16):
        P(im, 4, y, IRON[2]); P(im, 11, y, IRON[1])
    for y in range(1, 16, 4):
        for x in range(4, 12): P(im, x, y, IRON[3]); P(im, x, y + 1, IRON[0])
    return im


def union_banner():
    """the Ebbmouth dockers' union banner: Isenmar teal, a white anchor and a whale's fluke"""
    im = Image.new('RGBA', (16, 32), CLEAR); T = PAL['T']['vein']
    for x in range(2, 14): P(im, x, 1, WOOD[1]); P(im, x, 2, WOOD[2])
    for y in range(3, 28):
        for x in range(3, 13):
            if y > 24 and abs(x - 7.5) < (y - 24) * 1.5: continue
            P(im, x, y, T[1] if x > 4 else T[2])
            if x == 12: P(im, x, y, T[0])
    for y in range(8, 20): P(im, 8, y, (236, 240, 244, 255))
    for x in range(6, 11): P(im, x, 10, (236, 240, 244, 255))
    for x in range(5, 12): P(im, x, 19 - abs(x - 8) // 2, (236, 240, 244, 255))
    return im


CODES = {'M': (0, 15, 0)}                      # solid ground (the rock mass above the walls)


if __name__ == '__main__':
    ps = pieces()
    ims = [(n, im.resize((im.width * 2, im.height * 2), Image.NEAREST)) for n, (im, c, dr) in ps.items()]
    Wd = 1500; x = y = 0; rowh = 0; pos = []
    for n, im in ims:
        if x + im.width > Wd: x = 0; y += rowh + 14; rowh = 0
        pos.append((n, im, x, y)); x += im.width + 8; rowh = max(rowh, im.height)
    sheet = Image.new('RGBA', (Wd, y + rowh + 14), (60, 54, 64, 255))
    dr = ImageDraw.Draw(sheet)
    for n, im, x, y in pos:
        sheet.alpha_composite(im, (x, y + 12)); dr.text((x, y), n[:9], fill=(255, 230, 120, 255))
    sheet.save(sys.argv[1] if len(sys.argv) > 1 else '/tmp/cdraw.png'); print(sheet.size, len(ps))
