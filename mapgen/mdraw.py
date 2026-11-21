#!/usr/bin/env python3
"""mdraw.py - the Prismfall manor kit (map builder 14): tileset 59 "PF Rejuv Manor" shares the PF Rejuv sheet; these
pieces are appended by rcustom AFTER the cave kit (cdraw), so no earlier id moves, and doubled 2x like every rdraw /
tdraw / ndraw / gdraw / cdraw piece.  16-px logical grid, light from the top left, outlines never black.

Thistledown Manor (546/547): a sagging Elowen manor where a dead theatre family still rehearses.
Wall kits (rkit KITS 'cv' + letter; the Cave machinery draws them: lip / face / base rows, N rim, W / E sides, inner
corners, the void above):
  F  the foyer and stair hall: sage damask over oak panelling, cream cornice
  H  the portrait gallery: crimson damask over walnut, gilt picture rail
  N  the dining room: teal stripe over dark walnut
  P  the parlour: dusty-rose floral paper over cream-painted panels
  G  the conservatory: night glass in white-painted iron glazing bars on a stone plinth
  A  the attic: bare boards under the rafters
  B  the landing's gallery front (TER): oak handrail and turned balusters over a panelled front
floors <p>_f0-3 (F checker marble, H parquet, N dark boards, P light parquet, G encaustic tiles, A dusty boards);
rugs (9-slice, walkable): mn_rugR (crimson Persian), mn_rugB (blue runner), mn_rugG (green);
furniture and dressing: mn_* (see pieces()).

    python3 -I mdraw.py out.png      # contact sheet"""
import math, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
from rdraw import P, CLEAR, disc
from cdraw import A, nz, smooth

# ------------------------------------------------------------------ palettes (dark -> light)
OAK = [(58, 40, 30), (88, 62, 42), (120, 88, 58), (152, 116, 76), (186, 148, 100), (216, 182, 132)]
WAL = [(40, 24, 22), (62, 38, 30), (88, 56, 40), (116, 76, 52), (148, 102, 68), (184, 136, 92)]
PAINT = [(120, 112, 98), (156, 148, 130), (190, 182, 162), (214, 206, 186), (232, 226, 208), (246, 242, 228)]
GOLD = [(96, 66, 28), (146, 106, 40), (196, 152, 64), (232, 198, 104), (252, 236, 170)]
CREAM = [(150, 136, 116), (184, 170, 148), (214, 202, 180), (236, 228, 210), (250, 246, 234)]
VOID = [(34, 27, 38), (25, 19, 29), (16, 12, 20), (9, 7, 12)]
IRONW = [(120, 126, 130), (176, 182, 184), (214, 220, 220), (240, 244, 244)]
STONE = [(96, 92, 90), (128, 124, 118), (160, 156, 148), (192, 188, 178), (222, 218, 206)]
VELR = [(70, 16, 26), (104, 26, 36), (140, 40, 48), (176, 62, 66), (206, 104, 100)]
VELG = [(26, 52, 40), (38, 76, 56), (54, 104, 74), (78, 136, 96), (120, 170, 128)]
VELB = [(26, 36, 70), (38, 54, 100), (56, 78, 134), (84, 110, 166), (132, 156, 200)]
SHEET = [(124, 122, 132), (156, 154, 164), (186, 184, 192), (214, 212, 218), (236, 234, 238)]
LEAF = [(30, 62, 40), (44, 92, 52), (66, 124, 66), (100, 158, 82), (150, 192, 110)]
DEAD = [(70, 56, 36), (104, 84, 52), (138, 112, 66), (170, 142, 88)]
FLAME = [(200, 92, 30), (246, 164, 60), (255, 222, 130), (255, 250, 220)]
MOON = (190, 214, 248)
GHOST = [(120, 86, 170), (160, 120, 214), (200, 170, 240), (236, 222, 255)]

PAPER = {
    'F': dict(paper=[(66, 86, 72), (82, 104, 86), (98, 122, 100)], motif=(122, 146, 116), acc=(146, 166, 134), wood=OAK, style='damask'),
    'H': dict(paper=[(78, 24, 32), (100, 34, 42), (120, 46, 52)], motif=(146, 64, 64), acc=GOLD[2], wood=WAL, style='damask'),
    'N': dict(paper=[(30, 56, 66), (42, 76, 84), (56, 94, 100)], motif=(74, 116, 118), acc=GOLD[2], wood=WAL, style='stripe'),
    'P': dict(paper=[(134, 92, 100), (156, 112, 118), (174, 134, 136)], motif=(222, 200, 186), acc=(106, 138, 96), wood=PAINT, style='floral'),
    'A': dict(paper=[(86, 70, 58), (108, 88, 70), (128, 106, 84)], motif=(148, 124, 98), acc=(64, 50, 42), wood=OAK, style='attic'),
    'G': dict(paper=[(26, 40, 70), (36, 54, 90), (50, 72, 112)], motif=(210, 226, 240), acc=IRONW[2], wood=STONE, style='glass'),
}


def R(im, x0, y0, x1, y1, c):
    for y in range(int(y0), int(y1) + 1):
        for x in range(int(x0), int(x1) + 1): P(im, x, y, A(c) if len(c) == 3 else c)


def bev(im, x0, y0, x1, y1, ramp, k=2):
    """a bevelled box: body ramp[k], lit top/left ramp[k+1], shaded bottom/right ramp[k-1]"""
    R(im, x0, y0, x1, y1, ramp[k])
    for x in range(x0, x1 + 1): P(im, x, y0, A(ramp[min(len(ramp) - 1, k + 1)])); P(im, x, y1, A(ramp[max(0, k - 1)]))
    for y in range(y0, y1 + 1): P(im, x0, y, A(ramp[min(len(ramp) - 1, k + 1)])); P(im, x1, y, A(ramp[max(0, k - 1)]))


def new(w=1, h=1):
    return Image.new('RGBA', (16 * w, 16 * h), CLEAR)


def shadow_under(im, x0, x1, y, a=90):
    for x in range(x0, x1 + 1): P(im, x, y, (10, 6, 14, a))


# ------------------------------------------------------------------ the wall: cornice / paper / dado / wainscot / skirting
FLEUR = ["...#...", "..###..", ".#.#.#.", "##.#.##", ".#####.", "...#...", "..###..", ".#...#.", "...#..."]


def paper_px(p, x, y):
    """the paper field, y in 0..21 (periodic in x with period 16)"""
    d = PAPER[p]; pp = d['paper']; st = d['style']
    if st == 'damask':
        c = pp[1] if (x + y) % 2 else pp[1]
        if nz(x, y, 7 + ord(p)) > 0.86: c = pp[0]
        for ox, oy in ((5, 1), (-3, 12)):
            fx, fy = (x - ox) % 16, y - oy
            if 0 <= fx < 7 and 0 <= fy < 9 and FLEUR[fy][fx] == '#':
                c = d['motif'] if fy < 5 else pp[2]
        if p == 'H' and (x % 16, y) in ((8, 11), (0, 0), (0, 21)): c = d['acc']
        return c
    if st == 'stripe':
        k = x % 8
        if k in (0, 1): c = pp[0]
        elif k == 4: c = d['acc'] if y % 3 else pp[2]
        else: c = pp[1] if k != 2 else pp[2]
        if nz(x, y, 9) > 0.92: c = pp[0]
        return c
    if st == 'floral':
        c = pp[1]
        if nz(x, y, 11) > 0.9: c = pp[2]
        for ox, oy in ((4, 3), (12, 9), (4, 15)):
            dx, dy = (x - ox) % 16, y - oy
            if dx > 8: dx -= 16
            if (dx, dy) in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)): c = d['motif'] if (dx, dy) != (0, 0) else (232, 160, 150)
            if (dx, dy) in ((1, 2), (-1, 2), (2, 1)): c = d['acc']
        return c
    if st == 'attic':
        b = x // 4
        c = pp[1] if b % 2 else pp[2]
        if x % 4 == 3: c = pp[0]
        if nz(b, y // 6, 13) > 0.8: c = pp[0] if c == pp[1] else pp[1]
        if nz(x, y, 14) > 0.94: c = d['motif']
        return c
    if st == 'glass':
        # night through old glass: panes between white glazing bars, a few stars, the garden's black shapes low down
        if x % 8 in (0,) or y in (0, 10, 21): return IRONW[2] if x % 8 == 0 and y % 2 == 0 else IRONW[1]
        c = pp[1] if y < 10 else pp[0]
        if y > 15 and smooth(x * 1.0, 0, 21, 6.0) * 6 + 15 < y: c = (18, 28, 34)
        if nz(x, y, 15) > 0.965: c = d['motif']
        if (x % 8 + y) % 9 == 0 and y < 10: c = pp[2]                 # a glint of moonlight on the pane
        return c
    return pp[1]


def wall_px(p, x, y):
    """the whole 48-px wall: y 0-1 ceiling shadow, 2-5 cornice, 6-27 paper, 28-30 dado, 31-43 panels, 44-47 skirting"""
    d = PAPER[p]; w = d['wood']; st = d['style']
    if y == 0: return VOID[1]
    if y == 1: return VOID[0] if st != 'attic' else w[0]
    if st == 'attic':                                      # rafters and a purlin, rough boards to the floor
        if y in (2, 3, 4): return w[3] if y == 2 else w[2] if y == 3 else w[0]
        if x % 16 in (6, 7, 8, 9) and y < 26:              # a rafter foot
            return w[3] if x % 16 == 6 else w[2] if x % 16 < 9 else w[0]
        if y >= 44: return w[1] if y < 46 else VOID[0]
        return paper_px(p, x, (y - 6) % 22)
    if st == 'glass':
        if y in (2, 3): return IRONW[3] if y == 2 else IRONW[1]
        if 4 <= y <= 27: return paper_px(p, x, (y - 4) * 22 // 24)
        if y in (28, 29): return IRONW[3] if y == 28 else IRONW[1]
        if y < 44:                                         # the stone plinth: ashlar courses
            c = STONE[2] if (y // 5 + (x + (4 if (y // 5) % 2 else 0)) // 8) % 2 else STONE[3]
            if y % 5 == 0 or (x + (4 if (y // 5) % 2 else 0)) % 8 == 0: c = STONE[1]
            return c
        return STONE[2] if y == 44 else STONE[1] if y < 47 else VOID[0]
    if y in (2, 3, 4, 5):                                  # cornice with dentils
        if y == 2: return CREAM[4]
        if y == 3: return CREAM[3]
        if y == 4: return CREAM[1] if x % 3 == 0 else CREAM[2]
        return CREAM[0]
    if y == 6: return VOID[0] if st != 'floral' else d['paper'][0]
    if 7 <= y <= 27:
        if p == 'H' and y == 8: return GOLD[2]             # the gilt picture rail
        if p == 'H' and y == 9: return GOLD[0]
        return paper_px(p, x, y - 6)
    if y == 28: return w[5]
    if y == 29: return w[3]
    if y == 30: return w[1]
    if y >= 44:
        return w[4] if y == 44 else w[2] if y == 45 else w[1] if y == 46 else VOID[0]
    # wainscot: a raised panel per tile
    xx = x % 16; yy = y - 31                               # 0..12
    if xx in (0, 15) or yy in (0, 12): return w[2]
    if xx == 1 or yy == 1: return w[3]
    if xx == 14 or yy == 11: return w[1]
    if xx == 2 or yy == 2: return w[4]
    if xx == 13 or yy == 10: return w[1]
    c = w[3]
    if nz(xx, yy // 3, 17 + ord(p)) > 0.75: c = w[2]
    return c


def wall_kit(p):
    out = {}
    full = Image.new('RGBA', (16, 48), CLEAR)
    for y in range(48):
        for x in range(16): full.putpixel((x, y), A(wall_px(p, x, y)))
    alt = Image.new('RGBA', (16, 48), CLEAR)
    for y in range(48):
        for x in range(16): alt.putpixel((x, y), A(wall_px(p, x + 8, y)))
    for k, nm in enumerate(('lip', 'face', 'base')):
        for end in 'wme':
            src = full.crop((0, k * 16, 16, k * 16 + 16))
            im = src.copy()
            if end == 'w':                                 # the corner / jamb: shadow falls into the room's corner
                for y in range(16):
                    P(im, 0, y, A(VOID[1])); P(im, 1, y, A(PAPER[p]['wood'][1] if k == 2 or (k == 1 and y >= 12) else VOID[0], 200))
            if end == 'e':
                for y in range(16):
                    P(im, 15, y, A(VOID[1])); P(im, 14, y, (0, 0, 0, 90))
            out['%s_%s%s' % (p, nm, end)] = (im, ['W'], None)
        out['%s_%sm1' % (p, nm)] = (alt.crop((0, k * 16, 16, k * 16 + 16)), ['W'], None)
    out['%s_facem2' % p] = (full.crop((0, 32, 16, 48)), ['W'], None)
    out['%s_lipm2' % p] = (alt.crop((0, 0, 16, 16)), ['W'], None)
    cap = PAPER[p]['wood'] if p not in 'G' else IRONW
    # north rim: the top of the room's south wall, seen from above (a moulded cap)
    for end in 'wme':
        im = Image.new('RGBA', (16, 16), A(VOID[1]))
        for x in range(16):
            if end == 'w' and x < 3 or end == 'e' and x > 12: continue
            P(im, x, 0, A(cap[4] if p != 'G' else cap[3])); P(im, x, 1, A(cap[2])); P(im, x, 2, A(cap[1])); P(im, x, 3, A(VOID[0]))
        out['%s_N%s' % (p, end)] = (im, ['W'], None)
    for side in 'WE':                                      # side walls: the wall's top edge on the room side
        im = Image.new('RGBA', (16, 16), A(VOID[1]))
        xs = (0, 1, 2, 3) if side == 'W' else (15, 14, 13, 12)
        cols = [cap[4] if p != 'G' else cap[3], cap[2], cap[1], VOID[0]]
        for y in range(16):
            for k, xx in enumerate(xs): P(im, xx, y, A(cols[k] if side == 'W' else cols[k] if k else cap[1]))
        out['%s_%s' % (p, side)] = (im, ['W'], None)
        for k in (0, 1):
            out['%s_in%s%d' % (p, side, k)] = (im.copy(), ['W'], None)
    for t in range(4):
        for v, s in enumerate('ab'):
            im = Image.new('RGBA', (16, 16), A(VOID[min(3, t)]))
            for y in range(16):
                for x in range(16):
                    if nz(x, y, 31 + v + t) > 0.93: P(im, x, y, A(VOID[max(0, t - 1)]))
            out['%s_m%d%s' % (p, t, s)] = (im, ['M'], None)
    im = Image.new('RGBA', (16, 16), CLEAR)
    for y in range(5):
        for x in range(16): P(im, x, y, (10, 6, 14, 110 - y * 22))
    out['%s_shadow' % p] = (im, ['V'], None)
    out['%s_mP' % p] = (Image.new('RGBA', (16, 16), A(VOID[1])), ['G'], None)
    return out


# ------------------------------------------------------------------ floors
def floor(p, v):
    im = new(); r = random.Random(ord(p) * 10 + v)
    if p == 'F':                                           # checker marble, 8-px squares, veined
        for y in range(16):
            for x in range(16):
                dark = ((x // 8) + (y // 8)) % 2 == 0
                if dark:
                    c = (46, 46, 56) if nz(x, y, 40 + v) > 0.3 else (58, 58, 70)
                    if abs(smooth(x * 1.0, y * 1.0, 41 + v, 4.0) - 0.5) < 0.05: c = (92, 92, 104)
                else:
                    c = (220, 212, 194) if nz(x, y, 42 + v) > 0.25 else (232, 226, 212)
                    if abs(smooth(x * 1.0, y * 1.0, 43 + v, 4.0) - 0.5) < 0.04: c = (184, 176, 162)
                if x % 8 == 7 or y % 8 == 7: c = tuple(max(0, k - 18) for k in c)
                if x % 8 == 0 or y % 8 == 0: c = tuple(min(255, k + 10) for k in c)
                im.putpixel((x, y), A(c))
        if v == 3:
            for i in range(5): P(im, 2 + i, 9 + (i % 2), (30, 30, 36, 255))      # a hairline crack
        return im
    if p in 'HP':                                          # basket-weave parquet, 8-px squares of four slats
        W_ = OAK if p == 'P' else WAL
        for y in range(16):
            for x in range(16):
                horiz = ((x // 8) + (y // 8)) % 2 == 0
                k = (y % 8) // 2 if horiz else (x % 8) // 2
                c = W_[3 + (k % 2)] if p == 'P' else W_[3 + (k % 2)]
                edge = (y % 8) % 2 == 1 if horiz else (x % 8) % 2 == 1
                if edge: c = W_[2]
                if x % 8 == 7 or y % 8 == 7: c = W_[1]
                if nz(x, y, 50 + v) > 0.9: c = W_[2]
                im.putpixel((x, y), A(c))
        if v >= 2:
            for _ in range(v): P(im, r.randrange(1, 15), r.randrange(1, 15), A(W_[5]))
        return im
    if p in 'NA':                                          # boards: dark polished walnut / pale dusty attic deal
        W_ = WAL if p == 'N' else [(84, 74, 66), (108, 96, 84), (132, 118, 102), (152, 138, 120), (172, 160, 142), (194, 184, 166)]
        for y in range(16):
            for x in range(16):
                b = y // 4; off = (b * 5 + v * 3) % 16
                c = W_[3] if b % 2 else W_[2]
                if (x + off) % 16 == 0: c = W_[1]
                if y % 4 == 3: c = W_[1]
                if y % 4 == 0: c = W_[4] if p == 'N' else W_[3]
                if nz(x // 3, y, 60 + v) > 0.82: c = W_[2] if c != W_[1] else c
                im.putpixel((x, y), A(c))
        if p == 'A':
            for _ in range(6): P(im, r.randrange(16), r.randrange(16), A(W_[5]))
        if v == 3:
            P(im, 4, 6, A(W_[0])); P(im, 11, 10, A(W_[0]))          # nail heads
        return im
    if p == 'G':                                           # encaustic tiles: terracotta and buff, black diamond keys
        T_ = [(122, 58, 42), (156, 76, 54), (182, 98, 70), (206, 124, 92)]
        B_ = [(178, 162, 128), (206, 190, 154), (226, 214, 182)]
        for y in range(16):
            for x in range(16):
                xx, yy = x % 8, y % 8
                terra = ((x // 8) + (y // 8)) % 2 == 0
                c = (T_[2] if nz(x, y, 70 + v) > 0.2 else T_[1]) if terra else (B_[1] if nz(x, y, 71 + v) > 0.2 else B_[0])
                if abs(xx - 3.5) + abs(yy - 3.5) < 1.6 and not terra: c = (46, 40, 44)
                if xx == 7 or yy == 7: c = (88, 70, 60)
                if xx == 0 or yy == 0: c = T_[3] if terra else B_[2]
                im.putpixel((x, y), A(c))
        if v >= 2:                                         # earth and moss in the joints
            for _ in range(4): P(im, r.randrange(16), r.choice((7, 15)), A(LEAF[1]))
        return im
    return im


# ------------------------------------------------------------------ rugs (9-slice, walkable)
RUGS = {'R': dict(field=[(96, 22, 30), (122, 32, 38), (150, 48, 50)], border=[(42, 30, 52), (196, 152, 64), (232, 208, 150)], motif=(214, 170, 90)),
        'B': dict(field=[(30, 44, 86), (42, 60, 110), (60, 82, 136)], border=[(80, 24, 34), (196, 152, 64), (226, 214, 190)], motif=(210, 196, 150)),
        'G': dict(field=[(34, 66, 52), (46, 86, 66), (66, 110, 84)], border=[(70, 40, 30), (190, 146, 62), (220, 208, 170)], motif=(196, 176, 110))}


def rug(k, part):
    """part in nw n ne w c e sw s se c2; the field has a small lozenge lattice, the border three bands, fringe N/S"""
    d = RUGS[k]; f = d['field']; b = d['border']; im = new()
    top = part[0] == 'n'; bot = part[0] == 's'; lef = part.endswith('w'); rig = part.endswith('e')
    for y in range(16):
        for x in range(16):
            # distance into the rug from each open edge
            dt = y - 2 if top else 99; db = 13 - y if bot else 99; dl = x - 1 if lef else 99; dr = 14 - x if rig else 99
            dd = min(dt, db, dl, dr)
            if dd < 0:
                if (top and y < 2) or (bot and y > 13):           # fringe
                    if x % 2 == 0 and not (lef and x < 1) and not (rig and x > 14): P(im, x, y, A(b[2], 220))
                continue
            if dd == 0: c = b[0]
            elif dd == 1: c = b[1]
            elif dd == 2: c = b[0] if (x + y) % 2 else b[2]
            elif dd == 3: c = b[1]
            elif dd == 4: c = b[0]
            else:
                c = f[1]
                if (abs((x % 8) - 4) + abs((y % 8) - 4)) == 3: c = d['motif']
                elif (abs((x % 8) - 4) + abs((y % 8) - 4)) < 2: c = f[2]
                if nz(x, y, 80) > 0.94: c = f[0]
                if part == 'c2':                                   # the medallion (a 4x4 diamond)
                    if abs(x - 7.5) + abs(y - 7.5) < 7: c = f[2] if (abs(x - 7.5) + abs(y - 7.5)) % 3 > 1 else d['motif']
                    if abs(x - 7.5) + abs(y - 7.5) < 3: c = b[0]
            im.putpixel((x, y), A(c))
    return im


# ------------------------------------------------------------------ furniture and dressing
def armchair(ramp=VELG, facing='down', sheet=False):
    """a wing armchair (1x1): carved walnut feet, buttoned velvet, wings; facing down (front) / up (back) / left / right"""
    im = new()
    if sheet:
        return dust_sheet(1, 1, 'chair')
    w = WAL
    if facing in ('down', 'up'):
        # back
        R(im, 3, 1, 12, 7, ramp[1]); R(im, 4, 1, 11, 6, ramp[2])
        for x in range(4, 12): P(im, x, 1, A(ramp[3]))
        if facing == 'down':
            for bx, by in ((6, 3), (9, 3), (7, 5), (8, 5)): P(im, bx, by, A(ramp[0]))
        # arms (wings)
        R(im, 1, 4, 3, 12, ramp[1]); R(im, 12, 4, 14, 12, ramp[0]); R(im, 1, 4, 2, 11, ramp[2]); P(im, 2, 4, A(ramp[3]))
        R(im, 13, 4, 13, 11, ramp[1])
        if facing == 'down':
            R(im, 4, 8, 11, 11, ramp[2]); R(im, 4, 8, 11, 8, ramp[3])          # the seat cushion
            R(im, 4, 12, 11, 12, ramp[1])
        else:
            R(im, 3, 7, 12, 12, ramp[1]); R(im, 4, 7, 11, 7, ramp[0])
        R(im, 1, 13, 14, 13, w[2])                                             # apron
        for fx in (2, 13): R(im, fx, 14, fx, 15, w[1]); P(im, fx, 14, A(w[3]))
        shadow_under(im, 3, 12, 15, 70)
    else:
        L = facing == 'left'
        xs = range(16) if L else range(15, -1, -1)
        def X(i): return i if L else 15 - i
        R(im, min(X(9), X(13)), 1, max(X(9), X(13)), 12, ramp[1])            # back seen side-on
        R(im, min(X(10), X(12)), 2, max(X(10), X(12)), 11, ramp[2])
        R(im, min(X(2), X(9)), 7, max(X(2), X(9)), 11, ramp[2])              # seat
        R(im, min(X(2), X(9)), 7, max(X(2), X(9)), 7, ramp[3])
        R(im, min(X(3), X(9)), 5, max(X(3), X(9)), 6, ramp[1])               # the arm
        P(im, X(3), 5, A(ramp[3]))
        R(im, min(X(2), X(13)), 12, max(X(2), X(13)), 13, w[2])
        for fx in (X(3), X(12)): R(im, fx, 14, fx, 15, w[1])
        shadow_under(im, 3, 12, 15, 70)
    return im


def dust_sheet(w, h, kind='chair'):
    """white dust sheets thrown over furniture: soft lit folds, a hem with a little drape at the floor"""
    im = new(w, h); W_, H_ = 16 * w, 16 * h
    if kind == 'chair':
        shape = lambda x, y: (2 <= x <= 13 and 2 <= y <= 14) and not (y < 6 and (x < 4 or x > 11) and y < 4)
    elif kind == 'tall':
        shape = lambda x, y: abs(x - 7.5) < 4.0 + y / 10.0 and 1 <= y <= 30
    elif kind == 'piano':
        shape = lambda x, y: ((x - 20) ** 2 / 400.0 + (y - 14) ** 2 / 160.0 < 1.0 or (2 <= x <= 22 and 3 <= y <= 24)) and y <= 28 and x <= 45
    else:                                                  # table / sofa
        shape = lambda x, y: 1 <= x <= W_ - 2 and 2 <= y <= H_ - 2
    for y in range(H_):
        for x in range(W_):
            if not shape(x, y): continue
            # folds: soft diagonal ridges, lit from the top left
            f = math.sin((x * 0.55 + y * 0.35) + 0.6 * math.sin(y * 0.4)) * 0.5 + 0.5
            k = 2 + (1 if f > 0.6 else 0) - (1 if f < 0.25 else 0)
            if not shape(x - 1, y) or not shape(x, y - 1): k = 4
            if not shape(x + 1, y) or not shape(x, y + 1): k = 1
            if nz(x, y, 90) > 0.95: k = max(0, k - 1)
            im.putpixel((x, y), A(SHEET[k]))
    for x in range(W_):                                    # the hem's shadow on the floor
        ys = [y for y in range(H_) if shape(x, y)]
        if ys and ys[-1] + 1 < H_: P(im, x, ys[-1] + 1, (10, 6, 14, 90))
    return im


def portrait(kind, crooked=False):
    """a gilt-framed portrait (1x1, hung on the wall face): K the Old King, Q Dame Rosamund, L young Laertes,
    F the Fool, X the painted-over face"""
    im = new()
    R(im, 2, 1, 13, 14, GOLD[1]); R(im, 3, 2, 12, 13, GOLD[2])
    for x in range(2, 14): P(im, x, 1, A(GOLD[3]))
    for y in range(1, 15): P(im, 2, y, A(GOLD[3]))
    R(im, 4, 3, 11, 12, (40, 30, 36))                      # dark varnished ground
    bg = {'K': (54, 40, 64), 'Q': (40, 56, 50), 'L': (58, 52, 40), 'F': (62, 44, 36), 'X': (48, 42, 46)}[kind]
    R(im, 4, 3, 11, 12, bg)
    skin = [(150, 104, 84), (196, 148, 118), (226, 186, 152)]
    # shoulders
    coat = {'K': VELR, 'Q': VELG, 'L': VELB, 'F': [(70, 50, 20), (150, 110, 30), (210, 170, 60), (230, 200, 100), (250, 230, 150)], 'X': SHEET}[kind]
    R(im, 4, 10, 11, 12, coat[1]); R(im, 5, 10, 10, 10, coat[2])
    # head
    for y in range(5, 10):
        for x in range(6, 10):
            if (x - 7.5) ** 2 / 4.2 + (y - 7.2) ** 2 / 6.5 <= 1: P(im, x, y, A(skin[1] if x < 9 else skin[0]))
    P(im, 6, 6, A(skin[2]))
    if kind != 'X':
        P(im, 7, 7, A((40, 26, 24))); P(im, 9, 7, A((40, 26, 24)))
    if kind == 'K':
        for x in range(6, 10): P(im, x, 4, A(GOLD[3]))
        for x in (6, 8, 9): P(im, x, 3, A(GOLD[3]))
        R(im, 6, 9, 9, 10, (200, 200, 206)); P(im, 7, 10, A((220, 220, 226)))      # white beard
    elif kind == 'Q':
        R(im, 5, 4, 10, 5, (170, 70, 40)); P(im, 5, 6, A((170, 70, 40))); P(im, 10, 6, A((150, 60, 36)))   # red hair
        R(im, 4, 9, 11, 9, (236, 232, 224)); P(im, 4, 10, A((236, 232, 224))); P(im, 11, 10, A((220, 214, 206)))  # the ruff
    elif kind == 'L':
        R(im, 6, 4, 9, 5, (50, 34, 28)); P(im, 6, 6, A((50, 34, 28)))
        R(im, 7, 10, 8, 12, (236, 232, 224))
    elif kind == 'F':
        P(im, 5, 4, A(VELR[3])); P(im, 6, 5, A(VELR[3])); P(im, 10, 4, A((70, 130, 70))); P(im, 9, 5, A((70, 130, 70)))
        P(im, 4, 3, A(GOLD[4])); P(im, 11, 3, A(GOLD[4]))
        P(im, 8, 9, A((200, 60, 60)))                       # a painted grin
    else:
        R(im, 6, 5, 9, 9, (116, 108, 112))                  # painted over
        for y in range(5, 10): P(im, 6 + (y % 3), y, A((96, 90, 94)))
    P(im, 12, 3, A(GOLD[4]))
    for x in range(3, 13): P(im, x, 15, (10, 6, 14, 80))
    if crooked:
        im = im.rotate(-9, resample=Image.NEAREST, center=(8, 2))
    return im


def company_portrait():
    """the big 2x2 portrait of the whole company, AF 211: eight small figures, one face painted over"""
    im = new(2, 2)
    R(im, 1, 1, 30, 29, GOLD[1]); R(im, 2, 2, 29, 28, GOLD[2]); R(im, 4, 4, 27, 26, (46, 38, 48))
    for x in range(1, 31): P(im, x, 1, A(GOLD[3]))
    for y in range(1, 30): P(im, 1, y, A(GOLD[3]))
    R(im, 4, 4, 27, 12, (58, 48, 66)); R(im, 4, 21, 27, 26, (70, 52, 40))       # backdrop, stage boards
    cols = [VELR, VELG, VELB, VELR, VELG, VELB, VELR, VELB]
    for i in range(8):
        x = 5 + i * 3; y = 13 if i % 2 else 11
        R(im, x, y + 3, x + 1, y + 9, cols[i][2]); P(im, x, y + 3, A(cols[i][3]))
        R(im, x, y, x + 1, y + 2, (210, 166, 132) if i != 5 else (120, 112, 116))
        if i == 3:
            for xx in range(x, x + 2): P(im, xx, y - 1, A(GOLD[3]))
    for x in range(2, 30): P(im, x, 30, (10, 6, 14, 80))
    return im


def window(curtained=True):
    """a tall arched sash window (1x2, on the lip and face rows): moonlight through small panes, a deep sill"""
    im = new(1, 2)
    R(im, 3, 2, 12, 28, OAK[1])
    for y in range(3, 28):
        for x in range(4, 12):
            if y < 6 and (x - 7.5) ** 2 + (y - 6) ** 2 * 3 > 16: continue
            c = (122, 150, 196) if (x + y) % 6 else (170, 196, 232)
            if y < 14: c = (92, 120, 170) if (x + y) % 5 else (150, 180, 226)
            if x in (7, 8) or y in (11, 19): c = OAK[3]
            P(im, x, y, A(c))
    disc(im, 6, 8, 1.2, A(MOON))
    R(im, 2, 28, 13, 29, CREAM[3]); R(im, 2, 30, 13, 30, CREAM[0])
    if curtained:
        for side in (0, 1):
            for y in range(1, 31):
                for i in range(3):
                    x = (2 + i if side == 0 else 13 - i)
                    if y > 26 and i == 2: continue
                    c = VELR[2 + (1 if i == 0 else 0) - (1 if (y + i) % 4 == 0 else 0)]
                    P(im, x, y, A(c))
        R(im, 1, 0, 14, 1, GOLD[1]); P(im, 1, 0, A(GOLD[3])); P(im, 14, 0, A(GOLD[3]))
    return im


def sconce(lit=True):
    """a brass wall sconce, one candle (on the face row)"""
    im = new()
    R(im, 7, 7, 8, 11, GOLD[1]); R(im, 5, 11, 10, 11, GOLD[2]); P(im, 5, 11, A(GOLD[3]))
    R(im, 7, 4, 8, 6, CREAM[4]); P(im, 8, 5, A(CREAM[2]))
    if lit:
        P(im, 7, 2, A(FLAME[1])); P(im, 7, 3, A(FLAME[2])); P(im, 8, 3, A(FLAME[0])); P(im, 7, 1, A(FLAME[3], 200))
        for a_ in range(0, 360, 30):
            P(im, 7.5 + 4 * math.cos(math.radians(a_)), 3 + 3 * math.sin(math.radians(a_)), (255, 220, 140, 50))
    return im


def candelabra():
    """a standing candelabrum (1x2): three candles on a brass stem, lit"""
    im = new(1, 2)
    R(im, 7, 10, 8, 28, GOLD[1]); P(im, 7, 10, A(GOLD[3]))
    R(im, 4, 9, 11, 9, GOLD[2]); R(im, 4, 7, 4, 9, GOLD[2]); R(im, 11, 7, 11, 9, GOLD[1])
    R(im, 5, 28, 10, 29, GOLD[1]); R(im, 4, 30, 11, 30, GOLD[0])
    for cx in (4, 7, 11):
        R(im, cx, 4, cx, 7, CREAM[4]) if cx != 7 else R(im, 7, 3, 8, 9, CREAM[4])
        P(im, cx, 2 if cx != 7 else 1, A(FLAME[2])); P(im, cx, 1 if cx != 7 else 0, A(FLAME[3], 200))
    for y in range(-2, 8):
        for x in range(0, 16):
            if (x - 7.5) ** 2 + (y - 2) ** 2 * 2 < 40 and im.getpixel((x, max(0, y)))[3] == 0 and y >= 0:
                P(im, x, y, (255, 214, 140, 26))
    shadow_under(im, 4, 11, 31, 80)
    return im


def chandelier():
    """a crystal chandelier (3x2, overhead): a brass hoop of candles and drops of glass"""
    im = new(3, 2)
    R(im, 23, 0, 24, 6, GOLD[1])
    for a_ in range(0, 360, 4):
        for rr in (13.0, 13.6):
            P(im, 24 + rr * math.cos(math.radians(a_)), 15 + rr * 0.45 * math.sin(math.radians(a_)), A(GOLD[2] if math.sin(math.radians(a_)) < 0 else GOLD[1]))
    for i, a_ in enumerate(range(0, 360, 30)):
        x = 24 + 13.3 * math.cos(math.radians(a_)); y = 15 + 6 * math.sin(math.radians(a_))
        R(im, x, y - 4, x, y - 1, CREAM[4]); P(im, x, y - 5, A(FLAME[2])); P(im, x, y - 6, A(FLAME[3], 200))
        P(im, x, y + 2, A((200, 226, 250))); P(im, x, y + 3, A((150, 180, 220)))
    for y in range(6, 22):
        if y % 3 == 0: P(im, 24, y, A((210, 232, 250)))
    disc(im, 24, 18, 2.2, A(GOLD[2])); P(im, 23, 17, A(GOLD[4]))
    return im


def fireplace(lit=False):
    """a marble chimneypiece (3x2): mantel with a clock and candlesticks on the wall base row, the firebox below"""
    im = new(3, 2)
    M = [(150, 146, 150), (186, 182, 186), (214, 210, 212), (236, 234, 234)]
    R(im, 1, 8, 46, 11, M[2]); R(im, 1, 8, 46, 8, M[3]); R(im, 1, 11, 46, 11, M[0])       # the mantel shelf
    R(im, 20, 1, 27, 7, WAL[2]); disc(im, 23.5, 4, 2.6, A(CREAM[4])); P(im, 23, 3, A(WAL[0])); P(im, 24, 4, A(WAL[0]))  # clock
    for cx in (6, 41):
        R(im, cx, 3, cx + 1, 7, GOLD[2]); P(im, cx, 1, A(FLAME[2] if lit else CREAM[4])); P(im, cx, 2, A(CREAM[4]))
    R(im, 3, 12, 44, 30, M[1])                                                            # the surround
    R(im, 3, 12, 3, 30, M[3]); R(im, 44, 12, 44, 30, M[0])
    R(im, 10, 15, 37, 30, (26, 20, 24))                                                   # the firebox
    for y in range(15, 20):
        for x in range(10, 38):
            if (x - 23.5) ** 2 / 196 + (y - 20) ** 2 / 25 > 1: P(im, x, y, A(M[1]))
    R(im, 13, 25, 34, 27, (60, 56, 60)); R(im, 13, 25, 34, 25, (100, 96, 100))            # the grate
    if lit:
        for x in range(14, 34):
            h = 3 + int(3 * nz(x, 0, 5));
            for y in range(25 - h, 25): P(im, x, y, A(FLAME[min(3, (25 - y) // 2)]))
    else:
        for x in range(14, 34): P(im, x, 24, A((90, 84, 80) if x % 3 else (140, 134, 128)))  # cold ash
        P(im, 20, 23, A((160, 70, 40))); P(im, 27, 23, A((120, 50, 34)))                 # two embers' ghosts
    R(im, 0, 30, 47, 31, (120, 116, 118))
    return im


def bookcase(w=1):
    """a glazed bookcase (w x 2): top on the wall base row, books in five colours, a dust-greyed cornice"""
    im = new(w, 2); W_ = 16 * w
    R(im, 1, 1, W_ - 2, 31, WAL[1]); R(im, 1, 1, W_ - 2, 2, WAL[3]); R(im, 1, 1, 1, 31, WAL[3])
    bk = [VELR[2], VELG[2], VELB[2], (150, 110, 50), (110, 60, 80), CREAM[1]]
    r = random.Random(W_)
    for shelf in (4, 11, 18, 25):
        x = 3
        while x < W_ - 3:
            c = r.choice(bk); h = r.randint(4, 6); wd = r.choice((1, 1, 2))
            R(im, x, shelf + 6 - h, x + wd - 1, shelf + 5, c); P(im, x, shelf + 6 - h, A(tuple(min(255, k + 40) for k in c)))
            x += wd + (1 if r.random() < 0.2 else 0)
        R(im, 2, shelf + 6, W_ - 3, shelf + 6, WAL[3])
    for x in range(2, W_ - 2):
        if nz(x, 0, 7) > 0.5: P(im, x, 0, A(SHEET[2], 200))         # dust on the cornice
    shadow_under(im, 1, W_ - 2, 31, 60)
    return im


def grandfather_clock():
    im = new(1, 2)
    R(im, 3, 1, 12, 30, WAL[2]); R(im, 3, 1, 12, 2, WAL[4]); R(im, 3, 1, 3, 30, WAL[4]); R(im, 12, 1, 12, 30, WAL[0])
    disc(im, 7.5, 7, 3.4, A(CREAM[4])); P(im, 7, 5, A(WAL[0])); P(im, 7, 6, A(WAL[0])); P(im, 8, 7, A(WAL[0])); P(im, 9, 8, A(WAL[0]))
    R(im, 5, 13, 10, 26, WAL[1]); R(im, 6, 14, 9, 25, (36, 26, 30))
    R(im, 7, 15, 8, 22, GOLD[1]); disc(im, 7.5, 23, 1.6, A(GOLD[3]))            # the pendulum
    R(im, 2, 29, 13, 31, WAL[1])
    return im


def armour():
    """a suit of armour on a stand (1x2), halberd at its side"""
    im = new(1, 2)
    S = [(70, 76, 88), (110, 118, 132), (156, 164, 178), (206, 212, 222)]
    R(im, 6, 2, 9, 7, S[2]); R(im, 6, 2, 9, 2, S[3]); R(im, 6, 5, 9, 5, (20, 20, 24))          # helm, visor slit
    R(im, 4, 8, 11, 17, S[1]); R(im, 5, 8, 10, 9, S[3]); R(im, 5, 10, 7, 16, S[2])            # cuirass
    R(im, 3, 9, 3, 18, S[1]); R(im, 12, 9, 12, 18, S[0])
    R(im, 5, 18, 7, 27, S[1]); R(im, 8, 18, 10, 27, S[0]); P(im, 5, 18, A(S[3]))
    R(im, 4, 28, 11, 30, WAL[2])
    R(im, 14, 0, 14, 29, WAL[3]); R(im, 13, 1, 15, 3, S[3]); P(im, 15, 4, A(S[2]))
    return im


def bust():
    """a marble bust on a fluted plinth (1x2)"""
    im = new(1, 2)
    M = [(140, 136, 140), (180, 176, 178), (214, 210, 210), (240, 238, 236)]
    for y in range(2, 9):
        for x in range(5, 11):
            if (x - 7.5) ** 2 / 7 + (y - 5) ** 2 / 9 <= 1: P(im, x, y, A(M[2] if x < 9 else M[1]))
    P(im, 6, 4, A(M[3])); R(im, 4, 9, 11, 12, M[1]); R(im, 4, 9, 10, 9, M[3])
    R(im, 5, 13, 10, 28, M[2]); R(im, 5, 13, 5, 28, M[3]); R(im, 10, 13, 10, 28, M[0])
    for x in (7, 8): R(im, x, 14, x, 27, M[1])
    R(im, 4, 13, 11, 13, M[3]); R(im, 3, 28, 12, 30, M[1]); R(im, 3, 28, 12, 28, M[3])
    return im


def curio_case(part):
    """a long glazed curio case (pieces l / m / r, 1 row): props from old productions under dusty glass"""
    im = new()
    x0 = 1 if part == 'l' else 0; x1 = 14 if part == 'r' else 15
    R(im, x0, 3, x1, 13, WAL[2]); R(im, x0, 3, x1, 4, WAL[4])
    R(im, x0 + (1 if part == 'l' else 0), 5, x1 - (1 if part == 'r' else 0), 11, (70, 90, 110))
    for y in range(5, 12):
        for x in range(x0, x1 + 1):
            if (x + y) % 7 == 0: P(im, x, y, (190, 214, 236, 200))
    things = {'l': [(4, 8, GOLD[3]), (5, 8, GOLD[3]), (6, 7, GOLD[2])], 'm': [(5, 8, (200, 200, 206)), (6, 9, (200, 200, 206)), (10, 7, VELR[3]), (11, 8, VELR[2])],
              'r': [(7, 8, (60, 60, 70)), (8, 7, (160, 160, 170)), (9, 8, (60, 60, 70))]}[part]
    for x, y, c in things: P(im, x, y, A(c))
    R(im, x0, 12, x1, 13, WAL[1])
    if part == 'l': R(im, 1, 13, 2, 15, WAL[1])
    if part == 'r': R(im, 13, 13, 14, 15, WAL[1])
    shadow_under(im, x0, x1, 15, 60)
    return im


def plinth():
    """a stubby plinth with an urn (1x1): the ends of the gallery's alcoves"""
    im = new()
    M = [(140, 136, 140), (180, 176, 178), (214, 210, 210), (240, 238, 236)]
    R(im, 3, 7, 12, 14, M[1]); R(im, 3, 7, 12, 7, M[3]); R(im, 3, 7, 3, 14, M[2]); R(im, 12, 7, 12, 14, M[0])
    for y in range(1, 7):
        for x in range(4, 12):
            if (x - 7.5) ** 2 / 10 + (y - 4) ** 2 / 6 <= 1: P(im, x, y, A(VELB[2] if x < 9 else VELB[1]))
    P(im, 6, 2, A(VELB[4])); R(im, 6, 0, 9, 0, VELB[1])
    shadow_under(im, 3, 12, 15)
    return im


def table9(part, cloth=True):
    """the dining table, 9-slice with a white damask cloth hanging over its edges"""
    im = new(); top = part[0] == 'n'; bot = part[0] == 's'; lef = part.endswith('w'); rig = part.endswith('e')
    C_ = [(170, 168, 160), (204, 200, 190), (226, 222, 212), (242, 240, 232)]
    for y in range(16):
        for x in range(16):
            if top and y < 2: continue
            if lef and x < 1: continue
            if rig and x > 14: continue
            c = C_[2]
            if (x // 4 + y // 4) % 2 == 0 and nz(x, y, 4) > 0.5: c = C_[3]
            if bot and y > 10: c = C_[1] if y < 14 else C_[0]
            if lef and x < 3: c = C_[1]
            if rig and x > 12: c = C_[0]
            if top and y == 2: c = C_[3]
            if bot and y == 15: c = (70, 50, 40)
            im.putpixel((x, y), A(c))
    if nz(ord(part[0]), ord(part[-1]), 3) > 0.6:
        for i in range(4): P(im, 4 + i, 6 + (i % 2), A(SHEET[0], 160))       # old wine stain
    return im


def place_setting():
    im = new(); disc(im, 7.5, 7.5, 3.6, A(CREAM[4])); disc(im, 7.5, 7.5, 2.2, A(CREAM[2]))
    R(im, 2, 5, 2, 10, IRONW[2]); R(im, 13, 5, 13, 10, IRONW[2])
    disc(im, 11, 3, 1.3, A((170, 200, 220, 200)))
    return im


def table_candelabra():
    im = new(); R(im, 7, 6, 8, 13, GOLD[2]); R(im, 4, 6, 11, 6, GOLD[2]); R(im, 5, 13, 10, 14, GOLD[1])
    for cx in (4, 7, 11):
        R(im, cx, 2, cx, 5, CREAM[4]); P(im, cx, 1, A(FLAME[2])); P(im, cx, 0, A(FLAME[3], 180))
    for x in range(3, 13): P(im, x, 7, A(SHEET[1], 120))                   # cobweb between the arms
    return im


def dining_chair(facing):
    im = new(); w = WAL; v = VELR
    if facing == 'down':                                   # seen from the front: seat and the top of the back
        R(im, 3, 2, 12, 7, w[2]); R(im, 4, 3, 11, 6, v[2]); R(im, 3, 2, 12, 2, w[4])
        R(im, 3, 8, 12, 11, v[2]); R(im, 3, 8, 12, 8, v[3]); R(im, 3, 12, 12, 12, w[1])
        for fx in (3, 12): R(im, fx, 13, fx, 15, w[1])
    elif facing == 'up':                                   # seen from behind
        R(im, 3, 4, 12, 13, w[2]); R(im, 4, 5, 11, 12, w[3]); R(im, 3, 4, 12, 4, w[4])
        for x in (5, 7, 9): R(im, x, 6, x, 12, w[1])
        for fx in (3, 12): R(im, fx, 14, fx, 15, w[1])
    else:
        L = facing == 'left'; X = (lambda i: i) if L else (lambda i: 15 - i)
        R(im, min(X(3), X(11)), 8, max(X(3), X(11)), 10, v[2]); R(im, min(X(3), X(11)), 8, max(X(3), X(11)), 8, v[3])
        R(im, min(X(10), X(12)), 1, max(X(10), X(12)), 10, w[2])
        for fx in (X(3), X(11)): R(im, fx, 11, fx, 15, w[1])
    shadow_under(im, 3, 12, 15, 60)
    return im


def sideboard(part):
    """a walnut sideboard (l / r, 2 wide) with a silver tureen and a candlestick on top"""
    im = new()
    R(im, 0 if part == 'r' else 1, 4, 15 if part == 'l' else 14, 14, WAL[2])
    R(im, 0 if part == 'r' else 1, 4, 15 if part == 'l' else 14, 5, WAL[4])
    R(im, 3 if part == 'l' else 1, 7, 12 if part == 'l' else 12, 12, WAL[1])
    P(im, 7, 9, A(GOLD[3]))
    if part == 'l':
        disc(im, 8, 2, 2.6, A(IRONW[2])); P(im, 7, 1, A(IRONW[3])); R(im, 7, 0, 8, 0, IRONW[1])
    else:
        R(im, 7, 0, 8, 3, GOLD[2]); P(im, 7, 0, A(CREAM[4]))
    shadow_under(im, 1, 14, 15, 70)
    return im


def china_cabinet():
    """a tall china cabinet (2x2): glazed doors over blue-and-white plates"""
    im = new(2, 2)
    R(im, 1, 1, 30, 31, WAL[1]); R(im, 1, 1, 30, 2, WAL[3])
    for y0 in (4, 13):
        R(im, 3, y0, 28, y0 + 7, (60, 70, 86))
        for cx in (7, 15, 23):
            disc(im, cx, y0 + 4, 2.7, A((222, 228, 236))); disc(im, cx, y0 + 4, 1.4, A((70, 100, 170)))
    R(im, 15, 3, 16, 21, WAL[2])
    R(im, 3, 23, 28, 29, WAL[2]); P(im, 9, 26, A(GOLD[3])); P(im, 22, 26, A(GOLD[3]))
    return im


def trapdoor(open_=False):
    """an old cellar trapdoor in the dining-room boards: an iron ring, strap hinges.  Open: the lid stands up, black below"""
    im = new()
    W_ = WAL
    if not open_:
        R(im, 1, 1, 14, 14, W_[3])
        for y in (4, 8, 12): R(im, 1, y, 14, y, W_[1])
        R(im, 1, 1, 14, 1, W_[0]); R(im, 1, 14, 14, 14, W_[0]); R(im, 1, 1, 1, 14, W_[0]); R(im, 14, 1, 14, 14, W_[0])
        for y in (3, 11): R(im, 2, y, 6, y, IRONW[0])
        for a_ in range(0, 360, 30): P(im, 10 + 2 * math.cos(math.radians(a_)), 8 + 2 * math.sin(math.radians(a_)), A(IRONW[1]))
    else:
        R(im, 1, 6, 14, 15, (8, 6, 10)); R(im, 2, 7, 13, 8, (24, 18, 22))
        R(im, 1, 0, 14, 5, W_[3]); R(im, 1, 0, 14, 0, W_[4])
        for y in (2,): R(im, 2, y, 13, y, W_[1])
        R(im, 3, 9, 6, 12, VELG[1])                        # a velvet arm, down there in the dark
    return im


def hatch():
    """the attic hatch in the ceiling of the back-stair nook: a square of boards and a pull cord (on the face)"""
    im = new()
    R(im, 2, 1, 13, 6, OAK[2]); R(im, 2, 1, 13, 1, OAK[4]); R(im, 2, 6, 13, 6, OAK[0])
    R(im, 7, 7, 7, 13, (210, 190, 150)); disc(im, 7, 14, 1.3, A(VELR[3]))
    return im


def ladder():
    """the attic ladder, unfolded (walkable)"""
    im = new()
    R(im, 3, 0, 4, 15, OAK[3]); R(im, 11, 0, 12, 15, OAK[2])
    for y in range(1, 16, 4): R(im, 3, y, 12, y, OAK[4]); R(im, 3, y + 1, 12, y + 1, OAK[1])
    return im


def stair(part):
    """the grand staircase: oak treads with a crimson runner held by brass rods; the outer columns carry the banister"""
    im = new()
    for y in range(16):
        step = y % 4
        for x in range(16):
            c = OAK[4] if step == 0 else OAK[3] if step == 1 else OAK[2] if step == 2 else OAK[0]
            if part == 'm' or (part == 'l' and x >= 8) or (part == 'r' and x <= 7):
                if (part == 'm') or (part == 'l' and x >= 10) or (part == 'r' and x <= 5):
                    c = VELR[3] if step == 0 else VELR[2] if step < 3 else VELR[0]
                    if step == 1 and x % 5 == 0: c = GOLD[3]
            if part == 'l' and x < 4: c = WAL[2] if x != 3 else WAL[4]
            if part == 'r' and x > 11: c = WAL[2] if x != 12 else WAL[0]
            im.putpixel((x, y), A(c))
    if part in 'lr':
        bx = 1 if part == 'l' else 14
        for y in range(0, 16, 3): R(im, bx, y, bx, y + 1, CREAM[3])
    return im


def newel():
    """the newel post at the stair foot: a turned oak post with a brass finial (1x1, solid)"""
    im = new()
    R(im, 5, 4, 10, 15, OAK[2]); R(im, 5, 4, 5, 15, OAK[4]); R(im, 10, 4, 10, 15, OAK[0])
    R(im, 4, 3, 11, 4, OAK[3]); disc(im, 7.5, 1.5, 1.8, A(GOLD[3]))
    shadow_under(im, 5, 10, 15)
    return im


def sofa(ramp=VELR, facing='down'):
    """a chesterfield settee (2x1)"""
    im = new(2, 1)
    if facing == 'down':
        R(im, 2, 1, 29, 7, ramp[1]); R(im, 3, 1, 28, 6, ramp[2]); R(im, 3, 1, 28, 1, ramp[3])
        for bx in range(5, 28, 4): P(im, bx, 4, A(ramp[0]))
        R(im, 1, 4, 3, 12, ramp[2]); R(im, 28, 4, 30, 12, ramp[0])
        R(im, 4, 8, 27, 11, ramp[2]); R(im, 4, 8, 27, 8, ramp[3]); R(im, 15, 8, 16, 11, ramp[1])
    else:
        R(im, 1, 3, 30, 12, ramp[1]); R(im, 2, 3, 29, 4, ramp[2]); R(im, 1, 3, 30, 3, ramp[3])
    R(im, 1, 13, 30, 13, WAL[2])
    for fx in (2, 29): R(im, fx, 14, fx, 15, WAL[1])
    shadow_under(im, 3, 28, 15, 70)
    return im


def tea_table(cups=True):
    im = new()
    disc(im, 7.5, 6.5, 6, A(WAL[3])); disc(im, 7.5, 6.5, 5, A(WAL[4]))
    R(im, 7, 11, 8, 14, WAL[1]); R(im, 4, 15, 11, 15, WAL[0])
    if cups:
        disc(im, 5, 5, 1.6, A(CREAM[4])); P(im, 5, 5, A((140, 90, 60)))
        disc(im, 10, 7, 1.6, A((214, 190, 230))); P(im, 10, 7, A((120, 80, 60))); P(im, 12, 7, A((214, 190, 230)))   # a chipped teacup
        R(im, 7, 3, 9, 4, IRONW[2]); P(im, 10, 3, A(IRONW[1]))                       # the teapot
    return im


def piano():
    """a grand piano (3x2), lid up, black lacquer with a moonlit sheen"""
    im = new(3, 2); B_ = [(16, 14, 20), (30, 26, 36), (48, 44, 58), (90, 88, 110)]
    for y in range(2, 28):
        for x in range(2, 46):
            if (x - 18) ** 2 / 300.0 + (y - 15) ** 2 / 170.0 < 1.0 or (2 <= x <= 20 and 3 <= y <= 26): P(im, x, y, A(B_[1]))
    for x in range(4, 40): P(im, x, 4, A(B_[3])) if x % 2 == 0 else None
    R(im, 2, 3, 6, 26, B_[2]); R(im, 3, 5, 5, 24, (236, 232, 224))
    for y in range(6, 24, 2): R(im, 3, y, 4, y, (20, 18, 22))
    for y in range(8, 22): P(im, 30 - (y - 8), y, A(B_[3]))                         # the propped lid's edge
    for x in (8, 36): R(im, x, 26, x + 1, 30, B_[0])
    shadow_under(im, 6, 38, 31, 80)
    return im


def harp():
    im = new(1, 2)
    for y in range(1, 30):
        P(im, 4 + y // 10, y, A(GOLD[2]));
    for x in range(4, 13): P(im, x, 1 + (x - 4) // 3, A(GOLD[3]))
    R(im, 11, 4, 12, 28, GOLD[1])
    for x in range(6, 11): R(im, x, 3 + (x - 4) // 3, x, 26, (226, 222, 210, 180))
    R(im, 3, 28, 13, 30, WAL[2])
    return im


def gramophone():
    im = new()
    R(im, 3, 10, 12, 14, WAL[2]); R(im, 3, 10, 12, 10, WAL[4]); disc(im, 7.5, 11, 3, A((20, 18, 22)))
    for i in range(7):
        r_ = 1 + i * 0.75
        for a_ in range(200, 340, 8):
            P(im, 9 + i * 0.6 + r_ * math.cos(math.radians(a_)), 5 - i * 0.4 + r_ * math.sin(math.radians(a_)), A(GOLD[2 if i < 5 else 3]))
    R(im, 8, 6, 8, 10, GOLD[1])
    return im


def globe():
    im = new()
    disc(im, 7.5, 6, 5, A((60, 100, 140))); P(im, 5, 4, A(DEAD[2])); R(im, 6, 5, 8, 7, DEAD[2]); P(im, 10, 7, A(DEAD[2]))
    for a_ in range(200, 360, 6): P(im, 7.5 + 6 * math.cos(math.radians(a_)), 6 + 6 * math.sin(math.radians(a_)), A(GOLD[2]))
    R(im, 7, 11, 8, 13, WAL[2]); R(im, 4, 14, 11, 14, WAL[1])
    return im


def palm(big=False):
    """a potted palm (1x2) / a conservatory palm in a tub (2x3)"""
    w, h = (2, 3) if big else (1, 2)
    im = new(w, h); W_, H_ = 16 * w, 16 * h
    cx = W_ / 2 - 0.5
    pot_top = H_ - (12 if big else 9)
    R(im, cx - (6 if big else 4), pot_top, cx + (6 if big else 4), H_ - 2, (150, 84, 58) if not big else WAL[2])
    R(im, cx - (6 if big else 4), pot_top, cx + (6 if big else 4), pot_top + 1, (196, 120, 84) if not big else WAL[4])
    R(im, cx - (7 if big else 5), pot_top - 1, cx + (7 if big else 5), pot_top - 1, (120, 64, 44) if not big else WAL[1])
    rr = random.Random(w * 7 + h)
    n = 9 if big else 6
    for i in range(n):
        ang = math.radians(-160 + i * (140 / (n - 1)) + rr.uniform(-6, 6))
        L = (13 if big else 8) + rr.uniform(-2, 2)
        for t in range(int(L * 3)):
            tt = t / (L * 3.0)
            x = cx + math.cos(ang) * L * tt; y = pot_top - 2 + math.sin(ang) * L * tt * 1.2 + (tt ** 2) * L * 0.6
            P(im, x, y, A(LEAF[2]))
            for s in (-1, 1):
                fl = 3 * math.sin(tt * math.pi) * (1.4 if big else 1)
                P(im, x + s * fl * 0.6, y + fl * 0.5, A(LEAF[1] if s > 0 else LEAF[3]))
    R(im, cx, pot_top - 3, cx + 1, pot_top - 1, LEAF[0])
    shadow_under(im, int(cx - 5), int(cx + 6), H_ - 1)
    return im


def fern():
    im = new()
    R(im, 4, 10, 11, 14, (150, 84, 58)); R(im, 4, 10, 11, 10, (196, 120, 84))
    for i, a_ in enumerate(range(-170, -5, 22)):
        for t in range(7):
            x = 7.5 + math.cos(math.radians(a_)) * t; y = 9 + math.sin(math.radians(a_)) * t * 0.8 + t * t * 0.06
            P(im, x, y, A(LEAF[2 + (i % 2)]))
    shadow_under(im, 4, 11, 15)
    return im


def dead_plant():
    im = new()
    R(im, 4, 10, 11, 14, STONE[2]); R(im, 4, 10, 11, 10, STONE[4])
    for a_ in (-120, -90, -60, -30, -150):
        for t in range(8):
            P(im, 7.5 + math.cos(math.radians(a_)) * t * 0.7, 9 + math.sin(math.radians(a_)) * t + t * t * 0.08, A(DEAD[1 + (t % 2)]))
    P(im, 3, 9, A(DEAD[2])); P(im, 12, 11, A(DEAD[3]))
    return im


def orchid():
    im = new()
    R(im, 5, 11, 10, 14, (214, 210, 204)); R(im, 5, 11, 10, 11, (240, 238, 234))
    R(im, 7, 3, 7, 10, LEAF[1])
    for fx, fy in ((5, 3), (9, 4), (6, 6)):
        P(im, fx, fy, A((236, 180, 226))); P(im, fx + 1, fy, A((214, 140, 200))); P(im, fx, fy + 1, A((200, 120, 190)))
    R(im, 4, 9, 6, 10, LEAF[2]); R(im, 9, 9, 11, 10, LEAF[1])
    return im


def trough(part, earth=False):
    """a raised planting bed (l / r): stone sides, overgrown, or freshly turned (Scene 3's graveyard)"""
    im = new()
    x0 = 1 if part == 'l' else 0; x1 = 14 if part == 'r' else 15
    R(im, x0, 5, x1, 14, STONE[2]); R(im, x0, 5, x1, 5, STONE[4]); R(im, x0, 13, x1, 14, STONE[1])
    for y in range(6, 12):
        for x in range(x0 + 1, x1):
            c = (70, 50, 36) if nz(x, y, 3) > 0.4 else (90, 66, 46)
            if not earth and nz(x, y, 6) > 0.55: c = LEAF[1] if nz(x, y, 8) > 0.5 else DEAD[1]
            P(im, x, y, A(c))
    if earth and part == 'l':
        R(im, 9, 0, 9, 9, WAL[3]); R(im, 7, 3, 11, 3, WAL[3])            # a wooden cross, a prop
    if not earth:
        for x in range(x0 + 1, x1, 3): P(im, x, 4, A(LEAF[2])); P(im, x + 1, 3, A(LEAF[3]))
    shadow_under(im, x0, x1, 15)
    return im


def fountain():
    """a dry conservatory fountain (2x2): a stone basin, a fluted column, a Lotad-shaped spout"""
    im = new(2, 2)
    for y in range(10, 30):
        for x in range(1, 31):
            q = (x - 15.5) ** 2 / 225 + (y - 21) ** 2 / 64
            if q <= 1: P(im, x, y, A(STONE[3] if q > 0.75 else (70, 76, 60) if q > 0.0 else STONE[2]))
    for y in range(14, 28):
        for x in range(4, 28):
            if (x - 15.5) ** 2 / 144 + (y - 21) ** 2 / 36 <= 1: P(im, x, y, A((60, 64, 50) if nz(x, y, 9) > 0.3 else DEAD[1]))
    R(im, 13, 4, 18, 18, STONE[2]); R(im, 13, 4, 13, 18, STONE[4]); R(im, 18, 4, 18, 18, STONE[0])
    disc(im, 15.5, 3.5, 4, A((92, 150, 96))); disc(im, 15.5, 3, 2.4, A((130, 190, 120)))
    P(im, 14, 2, A((40, 40, 40))); P(im, 17, 2, A((40, 40, 40)))
    return im


def iron_bench():
    im = new(2, 1)
    for x in range(2, 30):
        if x % 3 == 0: R(im, x, 2, x, 8, IRONW[1])
    R(im, 2, 2, 29, 2, IRONW[3]); R(im, 2, 8, 29, 9, IRONW[2]); R(im, 2, 10, 29, 10, IRONW[0])
    for fx in (3, 28): R(im, fx, 11, fx, 15, IRONW[1])
    shadow_under(im, 3, 28, 15)
    return im


def ivy(v):
    im = new(); r = random.Random(90 + v)
    x = r.randrange(4, 12)
    for y in range(16):
        x += r.choice((-1, 0, 0, 1)); x = max(1, min(14, x))
        P(im, x, y, A(LEAF[0]))
        if y % 3 == v % 3:
            P(im, x - 1, y, A(LEAF[2])); P(im, x - 2, y + 1, A(LEAF[1])); P(im, x + 1, y + 1, A(LEAF[3]))
    return im


def broken_pane():
    im = new()
    for i in range(6): P(im, 6 + i, 3 + i * 2 // 3, A(IRONW[3])); P(im, 8 - i // 2, 5 + i, A(IRONW[2]))
    R(im, 5, 6, 8, 9, (6, 8, 14))
    return im


def decal(kind, v=0):
    im = new(); r = random.Random(hash(kind) % 1000 + v)
    if kind == 'dust':
        for _ in range(26):
            x, y = r.randrange(1, 15), r.randrange(1, 15); P(im, x, y, (200, 196, 206, 70))
        for _ in range(3): x, y = r.randrange(2, 13), r.randrange(2, 13); R(im, x, y, x + 1, y, (190, 186, 196, 120))
    elif kind == 'web':
        cx, cy = (0, 0) if v == 0 else (15, 0)
        for a_ in range(0, 91, 18):
            aa = math.radians(a_ if v == 0 else 180 - a_)
            for t in range(13): P(im, cx + math.cos(aa) * t, cy + math.sin(aa) * t, (226, 226, 236, 170))
        for rr in (4, 8, 12):
            for a_ in range(0, 91, 3):
                aa = math.radians(a_ if v == 0 else 180 - a_)
                P(im, cx + math.cos(aa) * rr, cy + math.sin(aa) * rr * (1 + 0.05 * math.sin(a_)), (226, 226, 236, 120))
    elif kind == 'webhang':
        for x in range(2, 14):
            y = 1 + int(5 * math.sin((x - 2) / 11.0 * math.pi)); P(im, x, y, (226, 226, 236, 150))
        for x in (4, 8, 11): R(im, x, 0, x, 3 + x % 3, (226, 226, 236, 110))
    elif kind == 'moon':
        for y in range(16):
            for x in range(16):
                if 3 + y * 0.3 < x < 12 + y * 0.3 and (y + v) % 7 != 3: P(im, x, y, MOON + (38,))
    elif kind == 'leaves':
        for _ in range(4 + v):
            x, y = r.randrange(2, 13), r.randrange(2, 13); c = r.choice(DEAD)
            P(im, x, y, A(c)); P(im, x + 1, y, A(c)); P(im, x, y + 1, A(DEAD[0]))
    elif kind == 'shards':
        for _ in range(5):
            x, y = r.randrange(2, 13), r.randrange(2, 13); P(im, x, y, (220, 236, 250, 220)); P(im, x + 1, y + 1, (160, 190, 220, 200))
    elif kind == 'soil':
        for y in range(4, 13):
            for x in range(3, 13):
                if (x - 7.5) ** 2 / 25 + (y - 8.5) ** 2 / 16 <= 1: P(im, x, y, A((84, 62, 44) if nz(x, y, 2) > 0.4 else (66, 48, 34)))
    elif kind == 'feet':                                   # a child's small footprints in the dust
        for i in range(3):
            P(im, 5 + (i % 2) * 4, 13 - i * 5, (60, 56, 70, 140)); P(im, 5 + (i % 2) * 4, 12 - i * 5, (60, 56, 70, 110))
    elif kind == 'wax':
        disc(im, 8, 9, 2, A(CREAM[3])); P(im, 10, 11, A(CREAM[2])); P(im, 6, 11, A(CREAM[2]))
    elif kind == 'petals':
        for _ in range(6):
            x, y = r.randrange(2, 14), r.randrange(2, 14); P(im, x, y, A((236, 236, 240))); P(im, x + 1, y, A((210, 206, 216)))
    elif kind == 'mat':
        R(im, 1, 3, 14, 12, (120, 90, 54)); R(im, 2, 4, 13, 11, (150, 116, 70))
        for x in range(3, 13, 2): R(im, x, 5, x, 10, (132, 100, 60))
    return im


def coat_stand():
    im = new(1, 2)
    R(im, 7, 3, 8, 29, WAL[2]); R(im, 4, 29, 11, 30, WAL[1])
    for hx, hy in ((4, 4), (11, 4), (5, 7), (10, 7)): P(im, hx, hy, A(WAL[3])); P(im, hx + (1 if hx < 8 else -1), hy + 1, A(WAL[2]))
    R(im, 3, 6, 6, 16, (60, 52, 70)); R(im, 3, 6, 6, 6, (90, 80, 100))                  # an opera cloak
    R(im, 8, 1, 12, 3, (30, 26, 30)); R(im, 9, 0, 11, 0, (30, 26, 30))                  # a top hat
    return im


def umbrella_stand():
    im = new()
    R(im, 4, 7, 11, 14, (160, 168, 182)); R(im, 4, 7, 11, 7, (210, 216, 226)); R(im, 5, 9, 10, 9, (70, 100, 170))
    R(im, 6, 1, 6, 7, (40, 36, 44)); R(im, 9, 2, 9, 7, (110, 30, 40)); P(im, 5, 1, A((40, 36, 44)))
    shadow_under(im, 4, 11, 15)
    return im


def console_table(part):
    im = new()
    R(im, 0 if part == 'r' else 1, 6, 15 if part == 'l' else 14, 8, WAL[3]); R(im, 0 if part == 'r' else 1, 6, 15 if part == 'l' else 14, 6, WAL[5])
    R(im, 0 if part == 'r' else 1, 9, 15 if part == 'l' else 14, 9, WAL[1])
    fx = 2 if part == 'l' else 13; R(im, fx, 10, fx, 15, WAL[1])
    if part == 'l':
        R(im, 5, 2, 12, 5, (236, 232, 220)); R(im, 8, 2, 9, 5, (196, 190, 176)); R(im, 6, 3, 7, 3, (60, 50, 60))   # the guest book
    else:
        for y in range(0, 6):
            for x in range(4, 11):
                if (x - 7) ** 2 / 9 + (y - 3) ** 2 / 9 <= 1: P(im, x, y, A((210, 214, 226)))
        P(im, 6, 0, A(VELR[3])); P(im, 8, 1, A((236, 236, 240))); P(im, 7, 0, A(DEAD[2]))   # a vase of dead roses
    return im


def statue():
    """a tragic muse on a plinth (1x2): the manor's theatrical bent"""
    im = new(1, 2)
    M = [(140, 136, 140), (180, 176, 178), (214, 210, 210), (240, 238, 236)]
    disc(im, 7.5, 3.5, 2.4, A(M[2])); P(im, 6, 2, A(M[3]))
    R(im, 5, 6, 10, 19, M[2]); R(im, 5, 6, 6, 19, M[3]); R(im, 9, 6, 10, 19, M[1])
    R(im, 10, 6, 12, 8, M[2]); disc(im, 12.5, 5, 1.6, A(M[1])); P(im, 12, 5, A((60, 60, 66)))   # holding up a mask
    R(im, 4, 20, 11, 28, M[1]); R(im, 4, 20, 11, 20, M[3]); R(im, 3, 28, 12, 30, M[1])
    return im


def trunk(open_=False):
    im = new()
    R(im, 1, 4, 14, 14, (100, 60, 40)); R(im, 1, 4, 14, 6, (130, 84, 54)); R(im, 1, 4, 14, 4, (156, 108, 70))
    for x in (4, 11): R(im, x, 4, x, 14, GOLD[1])
    R(im, 7, 7, 8, 8, GOLD[3])
    if open_:
        R(im, 1, 0, 14, 3, (130, 84, 54)); R(im, 2, 5, 13, 6, VELR[2]); R(im, 4, 5, 8, 5, (236, 232, 224))
    shadow_under(im, 1, 14, 15)
    return im


def hatboxes():
    im = new()
    for (cx, cy, rr, c) in ((7.5, 11, 5.6, (170, 120, 150)), (7.5, 6, 4.4, (120, 150, 170)), (7.5, 2.2, 3.0, (200, 180, 120))):
        for y in range(16):
            for x in range(16):
                if (x - cx) ** 2 / rr ** 2 + (y - cy) ** 2 / (rr * 0.6) ** 2 <= 1: P(im, x, y, A(c))
        for x in range(int(cx - rr), int(cx + rr) + 1): P(im, x, int(cy - rr * 0.55), A(tuple(min(255, k + 40) for k in c)))
    return im


def dummy():
    """a dressmaker's dummy wearing a ruff (1x2)"""
    im = new(1, 2)
    R(im, 7, 1, 8, 2, WAL[2])
    for y in range(3, 18):
        hw = 3 + (1 if 5 < y < 10 else 0) + (1 if y > 13 else 0)
        R(im, 8 - hw, y, 7 + hw, y, (180, 160, 136))
        P(im, 8 - hw, y, A((206, 188, 162)))
    R(im, 3, 3, 12, 4, (236, 232, 224)); R(im, 4, 2, 11, 2, (220, 214, 206))
    R(im, 7, 18, 8, 28, WAL[1]); R(im, 4, 28, 11, 29, WAL[1])
    return im


def rocking_horse():
    im = new()
    for x in range(1, 15): P(im, x, 13 + int(2 * math.cos((x - 7.5) / 5)), A(WAL[3]))
    R(im, 4, 6, 11, 10, (226, 220, 210)); R(im, 10, 2, 13, 7, (226, 220, 210)); P(im, 12, 3, A((30, 26, 30)))
    R(im, 9, 2, 10, 6, VELR[2]); P(im, 3, 7, A(VELR[2])); P(im, 2, 8, A(VELR[2]))
    for lx in (5, 10): R(im, lx, 11, lx, 13, (226, 220, 210))
    R(im, 6, 5, 9, 6, VELR[3])
    return im


def mirror():
    """a cheval mirror, cracked (1x2)"""
    im = new(1, 2)
    R(im, 3, 2, 12, 24, GOLD[1]); R(im, 4, 3, 11, 23, (120, 140, 160))
    for y in range(3, 24):
        for x in range(4, 12):
            if (x * 2 + y) % 11 == 0: P(im, x, y, A((200, 220, 236)))
    for i in range(9): P(im, 6 + i // 2, 8 + i, A((230, 240, 250)))
    R(im, 7, 24, 8, 29, WAL[2]); R(im, 3, 29, 12, 30, WAL[1])
    return im


def costume_rail():
    """a rail of old costumes (2x2): a gown, a doublet, a ruff, a crown on top"""
    im = new(2, 2)
    R(im, 2, 3, 29, 3, IRONW[1]); R(im, 2, 3, 2, 30, IRONW[1]); R(im, 29, 3, 29, 30, IRONW[0])
    for i, (c, w) in enumerate(((VELR, 6), (VELB, 5), (VELG, 6), ([(110, 90, 40), (150, 120, 50), (190, 160, 70), (220, 190, 100), (240, 220, 150)], 5))):
        x0 = 4 + i * 6
        for y in range(4, 24 if i % 2 == 0 else 18):
            hw = w // 2 + (y - 4) // 7
            R(im, x0 + 2 - hw // 2, y, x0 + 2 + hw // 2, y, c[2 if (y + i) % 5 else 3])
    for x in range(8, 13): P(im, x, 2, A(GOLD[3]))
    for x in (8, 10, 12): P(im, x, 1, A(GOLD[3]))
    R(im, 1, 30, 30, 31, IRONW[0])
    return im


def flats():
    """painted scenery flats leaning on the wall (2x2): a castle battlement (Scene 1's backdrop)"""
    im = new(2, 2)
    R(im, 2, 2, 29, 29, (96, 110, 140)); R(im, 2, 2, 29, 2, OAK[3]); R(im, 2, 29, 29, 29, OAK[1])
    R(im, 2, 2, 2, 29, OAK[3]); R(im, 29, 2, 29, 29, OAK[1])
    R(im, 4, 14, 27, 27, (140, 136, 130))
    for x in range(4, 28, 5): R(im, x, 11, x + 2, 13, (140, 136, 130))
    for y in range(16, 27, 3): R(im, 4, y, 27, y, (110, 106, 100))
    disc(im, 22, 7, 2.5, A((230, 226, 200)))
    return im


def oculus():
    """a round gable window (2x2 on the attic's end wall), moonlight"""
    im = new(2, 2)
    for y in range(32):
        for x in range(32):
            q = (x - 15.5) ** 2 + (y - 15.5) ** 2
            if q <= 13 ** 2:
                c = OAK[1] if q > 11 ** 2 else ((92, 120, 170) if (x + y) % 5 else (150, 180, 226))
                if q <= 11 ** 2 and (abs(x - 15.5) < 1 or abs(y - 15.5) < 1): c = OAK[2]
                P(im, x, y, A(c))
    disc(im, 11, 10, 1.6, A(MOON))
    return im


def rafter():
    """a tie-beam across the attic (overhead, 1 row)"""
    im = new()
    R(im, 0, 4, 15, 9, OAK[2]); R(im, 0, 4, 15, 4, OAK[4]); R(im, 0, 9, 15, 9, OAK[0])
    for x in (3, 11): P(im, x, 6, A(OAK[0]))
    return im


def footlight():
    """the attic stage's footlights: tin hoods along the stage lip (decal on the lip)"""
    im = new()
    for cx in (4, 11):
        R(im, cx - 2, 9, cx + 2, 12, IRONW[0]); R(im, cx - 2, 9, cx + 2, 9, IRONW[2]); P(im, cx, 8, A(FLAME[2]))
    return im


def door():
    """a panelled oak door with a brass lock, shut (the dining room's, locked until the portraits are set)"""
    im = new()
    R(im, 1, 0, 14, 15, OAK[1]); R(im, 2, 1, 13, 15, OAK[3]); R(im, 2, 1, 13, 1, OAK[4])
    for x0 in (3, 9):
        for y0 in (3, 9):
            R(im, x0, y0, x0 + 3, y0 + 4, OAK[2]); R(im, x0, y0, x0 + 3, y0, OAK[4]); R(im, x0, y0 + 4, x0 + 3, y0 + 4, OAK[1])
    R(im, 7, 1, 8, 15, OAK[1]); disc(im, 11, 8, 1.2, A(GOLD[3])); P(im, 11, 9, A(GOLD[0]))
    return im


def gallery_kit():
    """the landing's gallery front (kit 'B'): oak handrail over turned balusters (lip), a panelled front (face), skirting"""
    out = {}
    for end in 'wme':
        lip = new(); face = new(); base = new()
        for y in range(16):
            for x in range(16):
                # the lip: the landing's boards behind, the handrail and balusters in front
                c = OAK[3] if y < 5 else None
                if y in (5, 6): c = WAL[4] if y == 5 else WAL[2]
                if y >= 7 and x % 4 in (1, 2): c = CREAM[3] if x % 4 == 1 else CREAM[1]
                if y >= 7 and x % 4 in (0, 3): c = (40, 32, 40)
                if y == 15: c = WAL[1]
                lip.putpixel((x, y), A(c) if c else CLEAR)
                c = WAL[2]
                if y in (0, 15) or x in (0, 15): c = WAL[1]
                elif y == 1 or x == 1: c = WAL[4]
                elif y == 14 or x == 14: c = WAL[0]
                face.putpixel((x, y), A(c))
                c = WAL[2] if y < 11 else WAL[1] if y < 15 else VOID[0]
                if y == 0: c = WAL[4]
                base.putpixel((x, y), A(c))
        if end != 'm':
            ex = 0 if end == 'w' else 15
            for im in (lip, face, base):
                for y in range(16): P(im, ex, y, A(WAL[0])); P(im, ex + (1 if end == 'w' else -1), y, A(WAL[4] if end == 'w' else WAL[1]))
            R(lip, min(ex, 15 - ex if False else ex), 0, ex, 15, WAL[1])
            # the newel at the gallery's end
            nx0 = 1 if end == 'w' else 10
            R(lip, nx0, 0, nx0 + 4, 15, OAK[2]); R(lip, nx0, 0, nx0 + 4, 1, OAK[4]); disc(lip, nx0 + 2, 1, 1.5, A(GOLD[3]))
        out['B_lip%s' % end] = (lip, ['W'], None)
        out['B_face%s' % end] = (face, ['W'], None)
        out['B_base%s' % end] = (base, ['W'], None)
    out['B_facem1'] = (out['B_facem'][0], ['W'], None); out['B_lipm1'] = (out['B_lipm'][0], ['W'], None)
    out['B_facem2'] = (out['B_facem'][0], ['W'], None); out['B_lipm2'] = (out['B_lipm'][0], ['W'], None)
    for e in 'wme': out['B_N%s' % e] = wall_kit('F')['F_N%s' % e]
    for s in ('W', 'E', 'inW0', 'inW1', 'inE0', 'inE1'):
        out['B_%s' % s] = wall_kit('F')['F_%s' % ('W' if s.startswith(('W', 'inW')) else 'E')]
    return out


# ------------------------------------------------------------------ the table
def pieces():
    import rdraw, ndraw, cdraw
    rdraw.CODE.update(ndraw.CODES); rdraw.CODE.update(cdraw.CODES)
    out = {}
    for p in 'FHNPGA':
        out.update(wall_kit(p))
        for v in range(4): out['%s_f%d' % (p, v)] = (floor(p, v), ['G'], None)
    out.update(gallery_kit())
    for k in RUGS:
        for part in ('nw', 'n', 'ne', 'w', 'c', 'e', 'sw', 's', 'se', 'c2'):
            out['mn_rug%s_%s' % (k, part)] = (rug(k, part), ['D'], None)
    for f in ('down', 'up', 'left', 'right'):
        out['mn_chair_%s' % f] = (armchair(VELG, f), ['W'], None)
        out['mn_chairR_%s' % f] = (armchair(VELR, f), ['W'], None)
    out['mn_sheet_chair'] = (dust_sheet(1, 1, 'chair'), ['W'], None)
    out['mn_sheet_tall'] = (dust_sheet(1, 2, 'tall'), ['R', 'W'], None)
    out['mn_sheet_sofa'] = (dust_sheet(2, 1, 'sofa'), ['WW'], None)
    out['mn_sheet_table'] = (dust_sheet(2, 2, 'table'), ['WW', 'WW'], None)
    out['mn_sheet_piano'] = (dust_sheet(3, 2, 'piano'), ['WWW', 'WWW'], None)
    for k in 'KQLFX':
        out['mn_port%s' % k] = (portrait(k), ['X'], None)
        out['mn_port%s_c' % k] = (portrait(k, crooked=True), ['X'], None)
    out['mn_company'] = (company_portrait(), ['XX', 'XX'], None)
    out['mn_window'] = (window(True), ['X', 'X'], None)
    out['mn_window_bare'] = (window(False), ['X', 'X'], None)
    out['mn_sconce'] = (sconce(True), ['X'], None)
    out['mn_sconce_off'] = (sconce(False), ['X'], None)
    out['mn_candelabra'] = (candelabra(), ['R', 'W'], None)
    out['mn_chandelier'] = (chandelier(), ['OOO', 'OOO'], None)
    out['mn_fire'] = (fireplace(False), ['XXX', 'WWW'], None)
    out['mn_fire_lit'] = (fireplace(True), ['XXX', 'WWW'], None)
    out['mn_books'] = (bookcase(1), ['X', 'W'], None)
    out['mn_books2'] = (bookcase(2), ['XX', 'WW'], None)
    out['mn_clock'] = (grandfather_clock(), ['X', 'W'], None)
    out['mn_armour'] = (armour(), ['R', 'W'], None)
    out['mn_bust'] = (bust(), ['R', 'W'], None)
    for part in 'lmr': out['mn_case_%s' % part] = (curio_case(part), ['W'], None)
    out['mn_plinth'] = (plinth(), ['W'], None)
    for part in ('nw', 'n', 'ne', 'w', 'c', 'e', 'sw', 's', 'se'):
        out['mn_dt_%s' % part] = (table9(part), ['W'], None)
    out['mn_dt_plate'] = (place_setting(), ['X'], None)
    out['mn_dt_cand'] = (table_candelabra(), ['X'], None)
    for f in ('down', 'up', 'left', 'right'): out['mn_dch_%s' % f] = (dining_chair(f), ['W'], None)
    out['mn_sideboard'] = (Image.merge('RGBA', sideboard('l').split()), ['W'], None)
    sb = new(2, 1); sb.alpha_composite(sideboard('l'), (0, 0)); sb.alpha_composite(sideboard('r'), (16, 0))
    out['mn_sideboard2'] = (sb, ['WW'], None)
    out['mn_china'] = (china_cabinet(), ['XX', 'WW'], None)
    out['mn_trap'] = (trapdoor(False), ['D'], None)
    out['mn_trap_open'] = (trapdoor(True), ['W'], None)
    out['mn_hatch'] = (hatch(), ['X'], None)
    out['mn_ladder'] = (ladder(), ['D'], None)
    for part in 'lmr': out['mn_stair_%s' % part] = (stair(part), ['D'], None)
    out['mn_newel'] = (newel(), ['W'], None)
    out['mn_sofa'] = (sofa(VELR, 'down'), ['WW'], None)
    out['mn_sofa_up'] = (sofa(VELR, 'up'), ['WW'], None)
    out['mn_sofaG'] = (sofa(VELG, 'down'), ['WW'], None)
    out['mn_tea'] = (tea_table(True), ['W'], None)
    out['mn_table_s'] = (tea_table(False), ['W'], None)
    out['mn_piano'] = (piano(), ['WWW', 'WWW'], None)
    out['mn_harp'] = (harp(), ['R', 'W'], None)
    out['mn_gramophone'] = (gramophone(), ['W'], None)
    out['mn_globe'] = (globe(), ['W'], None)
    out['mn_palm'] = (palm(False), ['R', 'W'], None)
    out['mn_palm_big'] = (palm(True), ['RR', 'RR', 'WW'], None)
    out['mn_fern'] = (fern(), ['W'], None)
    out['mn_deadplant'] = (dead_plant(), ['W'], None)
    out['mn_orchid'] = (orchid(), ['W'], None)
    for part in 'lr':
        out['mn_trough_%s' % part] = (trough(part), ['W'], None)
        out['mn_grave_%s' % part] = (trough(part, earth=True), ['W'], None)
    out['mn_fountain'] = (fountain(), ['WW', 'WW'], None)
    out['mn_bench'] = (iron_bench(), ['WW'], None)
    for v in range(2): out['mn_ivy%d' % v] = (ivy(v), ['X'], None)
    out['mn_pane_broken'] = (broken_pane(), ['X'], None)
    for v in range(3): out['mn_dust%d' % v] = (decal('dust', v), ['V'], None)
    out['mn_web_l'] = (decal('web', 0), ['X'], None)
    out['mn_web_r'] = (decal('web', 1), ['X'], None)
    out['mn_webhang'] = (decal('webhang'), ['X'], None)
    for v in range(2): out['mn_moon%d' % v] = (decal('moon', v), ['V'], None)
    for v in range(3): out['mn_leaves%d' % v] = (decal('leaves', v), ['V'], None)
    out['mn_shards'] = (decal('shards'), ['V'], None)
    out['mn_soil'] = (decal('soil'), ['V'], None)
    out['mn_feet'] = (decal('feet'), ['V'], None)
    out['mn_wax'] = (decal('wax'), ['V'], None)
    out['mn_petals'] = (decal('petals'), ['V'], None)
    mat = new(2, 1); mat.alpha_composite(decal('mat'), (0, 0)); mat.alpha_composite(decal('mat').transpose(Image.FLIP_LEFT_RIGHT), (16, 0))
    out['mn_mat'] = (mat, ['DD'], None)
    out['mn_coat'] = (coat_stand(), ['R', 'W'], None)
    out['mn_umbrella'] = (umbrella_stand(), ['W'], None)
    ct = new(2, 1); ct.alpha_composite(console_table('l'), (0, 0)); ct.alpha_composite(console_table('r'), (16, 0))
    out['mn_console'] = (ct, ['WW'], None)
    out['mn_statue'] = (statue(), ['R', 'W'], None)
    out['mn_trunk'] = (trunk(False), ['W'], None)
    out['mn_trunk_open'] = (trunk(True), ['W'], None)
    out['mn_hatboxes'] = (hatboxes(), ['W'], None)
    out['mn_dummy'] = (dummy(), ['R', 'W'], None)
    out['mn_rocking'] = (rocking_horse(), ['W'], None)
    out['mn_mirror'] = (mirror(), ['R', 'W'], None)
    out['mn_rail'] = (costume_rail(), ['RR', 'WW'], None)
    out['mn_flats'] = (flats(), ['XX', 'WW'], None)
    out['mn_oculus'] = (oculus(), ['XX', 'XX'], None)
    out['mn_rafter'] = (rafter(), ['O'], None)
    out['mn_footlight'] = (footlight(), ['X'], None)
    out['mn_door'] = (door(), ['W'], None)
    return out


if __name__ == '__main__':
    ps = pieces()
    ims = [(n, im.resize((im.width * 2, im.height * 2), Image.NEAREST)) for n, (im, c, dr) in ps.items()]
    Wd = 1600; x = y = 0; rowh = 0; pos = []
    for n, im in ims:
        if x + im.width > Wd: x = 0; y += rowh + 14; rowh = 0
        pos.append((n, im, x, y)); x += im.width + 8; rowh = max(rowh, im.height)
    sheet = Image.new('RGBA', (Wd, y + rowh + 14), (60, 54, 64, 255))
    dr = ImageDraw.Draw(sheet)
    for n, im, x, y in pos:
        sheet.alpha_composite(im, (x, y + 12)); dr.text((x, y), n[:10], fill=(255, 230, 120, 255))
    sheet.save(sys.argv[1] if len(sys.argv) > 1 else '/tmp/mdraw.png'); print(sheet.size, len(ps))
