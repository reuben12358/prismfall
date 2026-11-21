#!/usr/bin/env python3
"""ldraw.py - the Lumen kit (map builder 15): Zenith's capital in brass, white stone, glass and light.  Tileset 60
"PF Rejuv Lumen" shares the PF Rejuv sheet; these pieces are appended by rcustom AFTER the manor kit (mdraw), so no
earlier id moves, and doubled 2x like every other drawn piece.  16-px logical grid, light from the top left, outlines
never black (rdraw conventions).

Lumen City (story/04_ACT_I Ch5, maps.json 180-199): "Ten Years of Light" - a city over an undercity.  Zenith above:
white marble and cream stone, brass trim and verdigris copper mansards, tall arched windows lit warm, glass curtain
bays in cyan, arc lamps, light conduits inlaid in the paving, the Prism fountain, the Meridian sunburst.  Nadir below
(the Lowlight): soot brick tenements, iron fire escapes, laundry, grilles and lift cages, Hollow Ring graffiti.

Pieces (names in pieces()):
  ground   lm_pave0-3 (marble slabs), lm_road0-1 (basalt setts), lm_track_h / _v / _x (tram rails), lm_kerbN/S/W/E,
           lm_inlay_h / _v / _x / _ne / _nw / _se / _sw (brass light conduits), lm_grate (Nadir grille, walkable),
           lm_sun (5x5 sunburst mosaic), lm_low0-3 (Lowlight setts), lm_plaza0-1 (plaza flags), lm_stair_l/m/r
  walls    plateau kit `lmw` (marble balustrade / ashlar face / foot; rkit KITS lmw), lm_void0-3 (the drop over Nadir)
  build    lb_* (bldg(): Lumen towers, mansards, flat roofs with tanks and skylights, glass bays, Lowlight tenements),
           civic: lb_pc, lb_arcade, lb_gym, lb_spire, lb_gate, lb_lab, lb_cycle, lb_council
  street   lm_arclamp, lm_arclamp_off, lm_bannerlamp, lm_holo, lm_bench, lm_bollard, lm_planter, lm_topiary, lm_kiosk,
           lm_news, lm_clock, lm_statue, lm_fountain (the Prism fountain 6x5), lm_tram (5x2), lm_shelter, lm_mast,
           lm_airship, lm_pylon (Lattice pylon), lm_lift (lift cage to Nadir), lm_vent, lm_steam, lm_bulbs, lm_banner,
           lm_poster0-2, lm_crate, lm_drone (tile), Lowlight props, the Fixed (crystal people) lm_fixed0-3, Bleed decals
  rooms    wall kits Z (Circuit Gym: black glass, neon trim), Y (civic: cream marble, brass rail), Q (vault: steel);
           floors Z_f / Y_f / Q_f; gym devices lm_node{I,L,T}{0-3}, lm_strip_h/_v (+ _on), lm_gen, lm_lamp(_on),
           lm_alarm(_on), lm_pdoor(_open), lm_socket(_drone), lm_splice(_on), lm_cradle, lm_cable, studio props

    python3 -I ldraw.py out.png      # contact sheet"""
import math, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
from rdraw import P, CLEAR, disc
from cdraw import A, nz, smooth

# ------------------------------------------------------------------ palettes (dark -> light)
MARBLE = [(112, 108, 114), (160, 154, 152), (198, 192, 184), (224, 220, 210), (242, 240, 232)]
CREAM = [(150, 132, 106), (196, 180, 148), (224, 212, 182), (240, 232, 208), (250, 246, 232)]
BRASS = [(86, 58, 26), (140, 98, 38), (194, 148, 60), (230, 194, 100), (252, 234, 166)]
VERD = [(30, 66, 66), (46, 100, 94), (70, 138, 122), (108, 178, 154), (164, 214, 192)]
SLATEB = [(36, 40, 58), (56, 64, 88), (80, 90, 118), (112, 124, 152), (152, 164, 188)]
GLS = [(24, 44, 64), (38, 78, 106), (62, 124, 156), (120, 188, 210), (210, 244, 248)]
LITW = [(150, 92, 44), (232, 168, 76), (255, 220, 140), (255, 248, 214)]
IRN = [(28, 30, 40), (48, 52, 66), (76, 82, 98), (114, 122, 140), (160, 168, 184)]
SOOT = [(46, 36, 36), (72, 52, 48), (98, 70, 60), (126, 92, 76), (156, 122, 100)]
BRICKR = [(78, 34, 32), (118, 52, 44), (150, 72, 56), (180, 100, 78), (206, 136, 108)]
BASALT = [(40, 42, 52), (56, 60, 72), (74, 78, 92), (98, 102, 116), (126, 130, 144)]
LEAFL = [(30, 70, 46), (44, 102, 58), (70, 140, 74), (112, 178, 96), (164, 210, 130)]
WOODL = [(56, 36, 28), (88, 58, 40), (120, 84, 56), (154, 114, 76), (190, 150, 104)]
CYAN = [(0, 90, 120), (0, 170, 210), (90, 230, 255), (210, 252, 255)]
MAGENTA = [(110, 20, 80), (200, 50, 150), (255, 110, 200), (255, 210, 240)]
AMBER = [(160, 80, 20), (240, 150, 40), (255, 210, 110), (255, 244, 210)]
RED = [(96, 26, 34), (150, 40, 46), (200, 64, 60), (232, 112, 96)]
BLUEC = [(28, 44, 92), (42, 68, 136), (70, 104, 180), (120, 150, 214)]
WINE = [(70, 22, 40), (110, 34, 56), (150, 52, 72), (190, 86, 100)]
TEALC = [(20, 70, 76), (32, 108, 112), (56, 148, 146), (110, 196, 186)]
CRYST = [(92, 70, 150), (150, 120, 214), (200, 184, 246), (238, 232, 255), (255, 255, 255)]
OUTL = (44, 38, 48)
VOIDC = [(10, 10, 20), (16, 16, 30), (24, 24, 42), (34, 32, 54)]


def R(im, x0, y0, x1, y1, c):
    c = A(c) if len(c) == 3 else c
    for y in range(int(y0), int(y1) + 1):
        for x in range(int(x0), int(x1) + 1): P(im, x, y, c)


def H(im, x0, x1, y, c):
    R(im, x0, y, x1, y, c)


def Vl(im, x, y0, y1, c):
    R(im, x, y0, x, y1, c)


def bev(im, x0, y0, x1, y1, ramp, k=2):
    R(im, x0, y0, x1, y1, ramp[k])
    H(im, x0, x1, y0, ramp[min(len(ramp) - 1, k + 1)]); Vl(im, x0, y0, y1, ramp[min(len(ramp) - 1, k + 1)])
    H(im, x0, x1, y1, ramp[max(0, k - 1)]); Vl(im, x1, y0, y1, ramp[max(0, k - 1)])


def new(w=1, h=1):
    return Image.new('RGBA', (16 * w, 16 * h), CLEAR)


def blend(im, x, y, c, a):
    if not (0 <= x < im.width and 0 <= y < im.height): return
    r0, g0, b0, a0 = im.getpixel((int(x), int(y)))
    if not a0:
        P(im, x, y, (c[0], c[1], c[2], int(255 * a))); return
    P(im, x, y, (int(r0 + (c[0] - r0) * a), int(g0 + (c[1] - g0) * a), int(b0 + (c[2] - b0) * a), a0))


def shade_box(im, x0, y0, x1, y1, f):
    for y in range(max(0, y0), min(im.height, y1 + 1)):
        for x in range(max(0, x0), min(im.width, x1 + 1)):
            r, g, b, a = im.getpixel((x, y))
            if a: im.putpixel((x, y), (max(0, min(255, int(r * f))), max(0, min(255, int(g * f))), max(0, min(255, int(b * f))), a))


def glow(im, cx, cy, r, c, a=0.5):
    for y in range(int(cy - r), int(cy + r) + 1):
        for x in range(int(cx - r), int(cx + r) + 1):
            d = math.hypot(x - cx, y - cy)
            if d <= r: blend(im, x, y, c, a * (1 - d / r) ** 1.5)


# ================================================================== ground
def pave(v, ramp=MARBLE, seed=0):
    """big marble slabs, two staggered courses per tile (8 px), seams on fixed lines so every variant tiles"""
    im = new()
    for y in range(16):
        for x in range(16):
            n = smooth(x, y, 11 + seed, 4.0) * 0.6 + nz(x, y, 70 + v + seed) * 0.4
            c = ramp[3] if n > 0.42 else ramp[2]
            if n > 0.78: c = ramp[4]
            P(im, x, y, A(c))
    for y in (7, 15):
        H(im, 0, 15, y, A(ramp[1]))
        H(im, 0, 15, y - 7 if y == 7 else 8, A(ramp[4]))
    for x, y0, y1 in ((0, 0, 6), (8, 8, 14)):
        Vl(im, x, y0, y1, A(ramp[1])); Vl(im, (x + 1) % 16, y0, y1, A(ramp[4]))
    r = random.Random(v * 13 + seed)
    for _ in range(2 + v):                          # veins and wear
        x, y = r.randrange(16), r.randrange(16)
        for k in range(r.randrange(2, 5)):
            if 0 <= x < 16 and 0 <= y < 16 and y not in (7, 15): P(im, x, y, A(ramp[1] if v % 2 else ramp[2]))
            x += r.choice((-1, 0, 1)); y += 1
    if v == 3:                                       # a brass survey stud
        P(im, 11, 3, A(BRASS[3])); P(im, 12, 3, A(BRASS[2])); P(im, 11, 4, A(BRASS[1]))
    return im


def setts(v, ramp=BASALT, seed=0, wet=False):
    """square-cut setts (the tram roadway / the Lowlight), 4x4 px, mortar lines"""
    im = new()
    for y in range(16):
        for x in range(16):
            bx, by = (x + (2 if (y // 4) % 2 else 0)) // 4, y // 4
            n = nz(bx, by, 40 + seed + v)
            c = ramp[2] if n < 0.55 else ramp[3] if n < 0.85 else ramp[1]
            lx, ly = (x + (2 if (y // 4) % 2 else 0)) % 4, y % 4
            if lx == 3 or ly == 3: c = ramp[0]
            elif lx == 0 and ly == 0: c = ramp[min(4, ramp.index(c) + 1)]
            P(im, x, y, A(c))
    if wet:
        r = random.Random(v + seed)
        cx, cy = r.randrange(4, 12), r.randrange(4, 12)
        for y in range(16):
            for x in range(16):
                d = ((x - cx) / 5.0) ** 2 + ((y - cy) / 3.0) ** 2
                if d < 1: blend(im, x, y, (40, 52, 70), 0.55);
                if 0.6 < d < 0.8 and x < cx: blend(im, x, y, (150, 120, 190), 0.35)
    return im


def track(kind):
    im = setts(0)
    def rail_h(y):
        H(im, 0, 15, y, A(IRN[1])); H(im, 0, 15, y + 1, A(IRN[4])); H(im, 0, 15, y + 2, A(IRN[2]))
    def rail_v(x):
        Vl(im, x, 0, 15, A(IRN[1])); Vl(im, x + 1, 0, 15, A(IRN[4])); Vl(im, x + 2, 0, 15, A(IRN[2]))
    if kind in ('h', 'x'):
        for x in range(0, 16, 4): R(im, x, 3, x + 1, 13, A(WOODL[1]) if kind == 'h' else A(BASALT[1]))
        rail_h(4); rail_h(10)
    if kind in ('v', 'x'):
        if kind == 'v':
            for y in range(0, 16, 4): R(im, 3, y, 13, y + 1, A(WOODL[1]))
        rail_v(4); rail_v(10)
    return im


def kerb(side):
    """the pavement's kerb: a granite edge and its shadow on the road side"""
    im = pave(1)
    if side == 'N':                                   # road to the north of this pavement tile
        H(im, 0, 15, 0, A(MARBLE[0])); H(im, 0, 15, 1, A(MARBLE[4])); H(im, 0, 15, 2, A(MARBLE[3])); H(im, 0, 15, 3, A(MARBLE[1]))
    if side == 'S':
        H(im, 0, 15, 12, A(MARBLE[4])); H(im, 0, 15, 13, A(MARBLE[2])); H(im, 0, 15, 14, A(MARBLE[1])); H(im, 0, 15, 15, A(BASALT[0]))
    if side == 'W':
        Vl(im, 0, 0, 15, A(MARBLE[0])); Vl(im, 1, 0, 15, A(MARBLE[4])); Vl(im, 2, 0, 15, A(MARBLE[3]))
    if side == 'E':
        Vl(im, 13, 0, 15, A(MARBLE[4])); Vl(im, 14, 0, 15, A(MARBLE[2])); Vl(im, 15, 0, 15, A(BASALT[0]))
    return im


def inlay(kind, base=None):
    """a brass light conduit set into the paving: brass edges, a glowing cyan core"""
    im = base.copy() if base is not None else pave(0)
    def seg(x0, y0, x1, y1):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1): P(im, x, y, A(BRASS[2]))
    def core(x0, y0, x1, y1):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1): P(im, x, y, A(CYAN[2]))
    h = kind in ('h', 'x', 'ne', 'nw', 'se', 'sw')
    arms = {'h': 'WE', 'v': 'NS', 'x': 'NSWE', 'ne': 'NE', 'nw': 'NW', 'se': 'SE', 'sw': 'SW'}[kind]
    for a in arms:
        if a == 'W': seg(0, 6, 9, 9)
        if a == 'E': seg(6, 6, 15, 9)
        if a == 'N': seg(6, 0, 9, 9)
        if a == 'S': seg(6, 6, 9, 15)
    for a in arms:
        if a == 'W': core(0, 7, 8, 8)
        if a == 'E': core(7, 7, 15, 8)
        if a == 'N': core(7, 0, 8, 8)
        if a == 'S': core(7, 7, 8, 15)
    for a in arms:                                    # the lit top edge / shaded lower edge of the brass
        if a in 'WE': H(im, 0 if a == 'W' else 6, 9 if a == 'W' else 15, 6, A(BRASS[3])); H(im, 0 if a == 'W' else 6, 9 if a == 'W' else 15, 9, A(BRASS[1]))
        if a in 'NS': Vl(im, 6, 0 if a == 'N' else 6, 9 if a == 'N' else 15, A(BRASS[3])); Vl(im, 9, 0 if a == 'N' else 6, 9 if a == 'N' else 15, A(BRASS[1]))
    for a in arms:
        if a == 'W': core(0, 7, 8, 8)
        if a == 'E': core(7, 7, 15, 8)
        if a == 'N': core(7, 0, 8, 8)
        if a == 'S': core(7, 7, 8, 15)
    P(im, 7, 7, A(CYAN[3])); P(im, 8, 8, A(CYAN[3]))
    return im


def grate(lit=True):
    im = new()
    R(im, 0, 0, 15, 15, A(IRN[0]))
    for y in range(1, 15):
        for x in range(1, 15):
            c = (255, 150, 60) if lit else (40, 30, 30)
            glowk = max(0.0, 1 - math.hypot(x - 7.5, y - 7.5) / 9.0)
            P(im, x, y, A(tuple(int(c[i] * glowk * 0.55 + IRN[0][i] * (1 - glowk * 0.55)) for i in range(3))))
    for x in range(0, 16, 3): Vl(im, x, 0, 15, A(IRN[2])); Vl(im, x + 1, 0, 15, A(IRN[3]) if x % 6 == 0 else A(IRN[2]))
    H(im, 0, 15, 0, A(IRN[3])); H(im, 0, 15, 15, A(IRN[1])); Vl(im, 15, 0, 15, A(IRN[1]))
    for x, y in ((1, 1), (14, 1), (1, 14), (14, 14)): P(im, x, y, A(BRASS[3]))
    return im


def sunburst():
    """the Meridian sunburst set into the plaza (5x5): cream and brass rays from a gilt disc"""
    im = new(5, 5); cx = cy = 40
    for y in range(80):
        for x in range(80):
            d = math.hypot(x + 0.5 - cx, y + 0.5 - cy); a = (math.atan2(y + 0.5 - cy, x + 0.5 - cx) + math.pi) / (2 * math.pi)
            ray = int(a * 24) % 2
            if d > 39.5:
                c = pave(nz(x // 16, y // 16, 3) > 0.5 and 1 or 2).getpixel((x % 16, y % 16))[:3]
            elif d > 37: c = BRASS[1] if d > 38.5 else BRASS[3]
            elif d > 12:
                c = (CREAM[3] if ray else MARBLE[2]) if d < 30 or ray else MARBLE[3]
                if abs((a * 24) % 1 - 0.0) < 0.06 or abs((a * 24) % 1 - 1.0) < 0.06: c = BRASS[2]
                if 29 < d < 31: c = BRASS[2]
            elif d > 10: c = BRASS[1]
            elif d > 6: c = BRASS[3] if (x + y) % 2 else BRASS[2]
            else: c = CYAN[2] if d > 2 else CYAN[3]
            P(im, x, y, A(c))
    return im


def stair(part, ramp=MARBLE):
    """white marble steps (walkable), brass nosings; part l / m / r"""
    im = new()
    for k in range(4):
        y = k * 4
        R(im, 0, y, 15, y + 3, A(ramp[3] if k % 2 == 0 else ramp[2]))
        H(im, 0, 15, y, A(ramp[4])); H(im, 0, 15, y + 1, A(BRASS[3]) if k == 0 else A(ramp[4])); H(im, 0, 15, y + 3, A(ramp[1]))
    if part == 'l': Vl(im, 0, 0, 15, A(ramp[1])); Vl(im, 1, 0, 15, A(ramp[4]))
    if part == 'r': Vl(im, 15, 0, 15, A(ramp[0])); Vl(im, 14, 0, 15, A(ramp[1]))
    return im


# ------------------------------------------------------------------ the plateau wall kit (lmw) and the drop over Nadir
def lmw_px(row, x, y):
    """lip: a marble balustrade on its coping; face: coursed ashlar with a brass band; base: plinth and foot shadow"""
    if row == 'lip':
        if y <= 1: return MARBLE[4] if y == 0 else MARBLE[3]
        if y <= 9:                                   # balusters
            bx = x % 4
            if y in (2, 3): return MARBLE[4] if y == 2 else MARBLE[2]
            if bx in (1, 2): return MARBLE[3] if bx == 1 else MARBLE[2]
            return VOIDC[2] if y > 4 else MARBLE[1]
        if y <= 11: return MARBLE[4] if y == 10 else MARBLE[2]
        return MARBLE[2] if (x // 8 + y) % 7 else MARBLE[1]
    if row == 'face':
        if y in (6, 7): return BRASS[3] if y == 6 else BRASS[1]
        cy = y % 5; off = 0 if (y // 5) % 2 else 5
        if cy == 4: return MARBLE[1]
        if (x + off) % 10 == 9: return MARBLE[1]
        return MARBLE[3] if cy == 0 else MARBLE[2]
    if row == 'base':
        if y < 4: return MARBLE[2] if (x + 3) % 10 else MARBLE[1]
        if y == 4: return MARBLE[4]
        if y < 12: return MARBLE[1] if y < 6 else MARBLE[2] if (x // 5) % 2 else MARBLE[1]
        return (60, 58, 66)
    return MARBLE[2]


def lmw_kit():
    out = {}
    for row in ('lip', 'face', 'base'):
        for end in 'wme':
            im = new()
            for y in range(16):
                for x in range(16): P(im, x, y, A(lmw_px(row, x, y)))
            if end == 'w': Vl(im, 0, 0, 15, A(MARBLE[4])); Vl(im, 1, 0, 15, A(MARBLE[3]))
            if end == 'e': Vl(im, 15, 0, 15, A(MARBLE[0])); Vl(im, 14, 0, 15, A(MARBLE[1]))
            out['lmw_%s%s' % (row, end)] = (im, ['W'] if row != 'lip' else ['W'], None)
    for end in 'wme':                                # the north rim (the wall's top seen from the high side)
        im = new()
        for y in range(16):
            for x in range(16): P(im, x, y, A(MARBLE[3] if y > 3 else MARBLE[4] if y < 2 else MARBLE[2]))
        H(im, 0, 15, 4, A(MARBLE[1]))
        out['lmw_N%s' % end] = (im, ['W'], None)
    for side in 'WE':
        im = new()
        for y in range(16):
            for x in range(16): P(im, x, y, A(MARBLE[2]))
        xs = (0, 1, 2) if side == 'W' else (15, 14, 13)
        for k, xx in enumerate(xs): Vl(im, xx, 0, 15, A([MARBLE[4], MARBLE[3], MARBLE[1]][k] if side == 'W' else [MARBLE[0], MARBLE[1], MARBLE[3]][k]))
        out['lmw_%s' % side] = (im, ['W'], None)
    return out


def void(v):
    """the drop off the plateau: Nadir's haze far below, its lamps like spilled embers"""
    im = new()
    for y in range(16):
        for x in range(16):
            n = smooth(x, y, 90 + v, 6.0)
            P(im, x, y, A(VOIDC[1] if n < 0.45 else VOIDC[2] if n < 0.8 else VOIDC[3]))
    r = random.Random(77 + v)
    for _ in range(2 + v):
        x, y = r.randrange(1, 15), r.randrange(1, 15)
        c = r.choice([(255, 170, 80), (240, 110, 70), (120, 220, 255), (200, 120, 255)])
        P(im, x, y, A(c)); blend(im, x + 1, y, c, 0.35); blend(im, x, y + 1, c, 0.25)
    return im


def railing(end='m'):
    """a brass railing along the plateau edge (solid; set on the top row of the void)"""
    im = new()
    for x in range(16):
        P(im, x, 3, A(BRASS[3])); P(im, x, 4, A(BRASS[2])); P(im, x, 5, A(BRASS[0]))
        P(im, x, 12, A(BRASS[2])); P(im, x, 13, A(BRASS[0]))
    for x in range(1, 16, 4):
        Vl(im, x, 5, 12, A(BRASS[2])); Vl(im, x + 1, 5, 12, A(BRASS[1]))
    if end in 'we':
        x = 0 if end == 'w' else 13
        R(im, x, 0, x + 2, 15, A(MARBLE[2])); Vl(im, x, 0, 15, A(MARBLE[4])); P(im, x + 1, 0, A(BRASS[3]))
    return im


# ================================================================== buildings
def ashlar(w, h, ramp, seed=1, course=5, block=(8, 13)):
    rng = random.Random(seed)
    im = Image.new('RGBA', (w, h), A(ramp[2])); d = ImageDraw.Draw(im)
    y = 0; k = 0
    while y < h:
        x = -rng.randrange(0, 7) if k % 2 else 0
        while x < w:
            bw = rng.randrange(*block)
            c = ramp[2] if rng.random() < 0.72 else ramp[3] if rng.random() < 0.55 else ramp[1]
            d.rectangle([x, y, x + bw - 1, y + course - 1], fill=A(c))
            d.line([x, y, x + bw - 2, y], fill=A(ramp[min(4, ramp.index(c) + 1)]))
            d.line([x + bw - 1, y, x + bw - 1, y + course - 1], fill=A(ramp[1] if c != ramp[1] else ramp[0]))
            x += bw
        d.line([0, y + course - 1, w, y + course - 1], fill=A(ramp[1]))
        y += course; k += 1
    return im


def plaster(w, h, ramp, seed=1):
    rng = random.Random(seed); im = Image.new('RGBA', (w, h), A(ramp[2]))
    for _ in range(w * h // 12):
        x, y = rng.randrange(w), rng.randrange(h); P(im, x, y, A(ramp[3] if rng.random() < 0.6 else ramp[1]))
    return im


def brickwall(w, h, ramp, seed=2, soot=0.0):
    rng = random.Random(seed); im = Image.new('RGBA', (w, h), A(ramp[2])); d = ImageDraw.Draw(im)
    for y in range(0, h, 3):
        off = 0 if (y // 3) % 2 else 3
        for x in range(-3 + off, w, 6):
            c = ramp[2] if rng.random() < 0.6 else ramp[3] if rng.random() < 0.5 else ramp[1]
            d.rectangle([x, y, x + 5, y + 1], fill=A(c)); d.line([x, y, x + 4, y], fill=A(ramp[min(4, ramp.index(c) + 1)]))
        d.line([0, y + 2, w, y + 2], fill=A(ramp[0]))
    if soot:                                           # soot streaks from the windows and a grimy foot
        for x in range(w):
            for y in range(h):
                s = soot * (smooth(x, y * 0.25, seed + 5, 5.0) * 0.6 + (y / max(1, h)) * 0.5)
                if s > 0.35: shade_box(im, x, y, x, y, 1 - min(0.35, (s - 0.35)))
    return im


def arch_window(im, x, y, w, h, lit, frame=BRASS, deep=GLS, rng=None, mull=True):
    """a tall window with a round top (frame, glass, a cross bar, a sill)"""
    g = LITW if lit else deep
    for yy in range(h):
        for xx in range(w):
            inside = True
            if yy < w // 2:
                cx = (w - 1) / 2.0; r = w / 2.0
                inside = (xx - cx) ** 2 + (yy - r + 0.3) ** 2 <= r * r
            if not inside: continue
            edge = xx in (0, w - 1) or yy == h - 1
            if yy < w // 2:
                cx = (w - 1) / 2.0; r = w / 2.0
                edge = edge or (xx - cx) ** 2 + (yy - r + 0.3) ** 2 > (r - 1.1) ** 2
            if edge: P(im, x + xx, y + yy, A(frame[1] if xx == w - 1 or yy == h - 1 else frame[3]))
            else:
                c = g[1] if yy > h * 0.55 else g[2]
                if xx == 1 and yy > 1: c = g[3] if not lit else g[2]
                if lit and yy < h * 0.4: c = g[3]
                P(im, x + xx, y + yy, A(c))
    if mull and w >= 5:
        Vl(im, x + w // 2, y + 2, y + h - 2, A(frame[2])); H(im, x + 1, x + w - 2, y + int(h * 0.55), A(frame[2]))
    H(im, x - 1, x + w, y + h, A(MARBLE[4])); H(im, x - 1, x + w, y + h + 1, A(MARBLE[1]))


def rect_window(im, x, y, w, h, lit, frame=BRASS, deep=GLS, shutters=None, boarded=False):
    g = LITW if lit else deep
    R(im, x, y, x + w - 1, y + h - 1, A(frame[1]))
    R(im, x + 1, y + 1, x + w - 2, y + h - 2, A(g[1]))
    R(im, x + 1, y + 1, x + w - 2, y + h // 2, A(g[2]))
    Vl(im, x + 1, y + 1, y + h - 2, A(g[3] if not lit else g[2]))
    Vl(im, x + w // 2, y + 1, y + h - 2, A(frame[2])); H(im, x + 1, x + w - 2, y + h // 2, A(frame[2]))
    if boarded:
        for k in range(3): H(im, x, x + w - 1, y + 2 + k * 3, A(WOODL[2 + (k % 2)]))
    if shutters:
        for sx in (x - 2, x + w):
            R(im, sx, y, sx + 1, y + h - 1, A(shutters[1])); Vl(im, sx, y, y + h - 1, A(shutters[2]))
    H(im, x - 1, x + w, y + h, A(MARBLE[3])); H(im, x - 1, x + w, y + h + 1, A((40, 36, 44)))


def scales(w, h, ramp, seed=0):
    """fish-scale roof shingles (copper / slate), 4-px rows"""
    im = Image.new('RGBA', (w, h), A(ramp[2]))
    for y in range(h):
        for x in range(w):
            row = y // 4; off = 2 if row % 2 else 0
            lx = (x + off) % 4; ly = y % 4
            c = ramp[2]
            if ly == 3 or (ly == 2 and lx in (0, 3)): c = ramp[1]
            elif ly == 0 and lx in (1, 2): c = ramp[3]
            if nz(x // 4, row, seed) > 0.86 and ly < 2: c = ramp[3] if c != ramp[1] else c
            P(im, x, y, A(c))
    return im


def dentils(im, x0, x1, y, ramp=MARBLE):
    H(im, x0, x1, y, A(ramp[4])); H(im, x0, x1, y + 1, A(ramp[3]))
    for x in range(x0, x1 + 1): P(im, x, y + 2, A(ramp[3] if x % 3 else ramp[1]))
    H(im, x0, x1, y + 3, A(ramp[1]))


def wall_lamp(im, x, y, lit=True):
    P(im, x, y + 3, A(BRASS[1])); P(im, x + 1, y + 3, A(BRASS[2]))
    R(im, x, y, x + 1, y + 2, A(AMBER[2] if lit else IRN[3])); P(im, x, y, A(AMBER[3] if lit else IRN[4]))
    H(im, x - 1, x + 2, y - 1, A(BRASS[2]))
    if lit: glow(im, x + 0.5, y + 1, 5, AMBER[2], 0.35)


def neon_blade(im, x, y, h, col, seed=0):
    """a vertical neon blade sign: dark panel, glowing bars"""
    R(im, x, y, x + 4, y + h, A(IRN[0])); Vl(im, x, y, y + h, A(BRASS[2])); Vl(im, x + 4, y, y + h, A(BRASS[1]))
    rng = random.Random(seed)
    yy = y + 2
    while yy < y + h - 2:
        k = rng.choice((2, 3))
        for t in range(k): H(im, x + 1, x + 3, yy + t, A(col[2] if t % 2 == 0 else col[3]))
        yy += k + 2
    for yy in range(y, y + h + 1): blend(im, x - 1, yy, col[2], 0.35); blend(im, x + 5, yy, col[2], 0.35)


def clock_face(im, cx, cy, r=5):
    disc(im, cx, cy, r + 1.2, A(BRASS[1])); disc(im, cx, cy, r + 0.6, A(BRASS[3])); disc(im, cx, cy, r - 0.2, A((246, 242, 228)))
    for k in range(12):
        a = k * math.pi / 6; P(im, int(round(cx + (r - 1.2) * math.cos(a))), int(round(cy + (r - 1.2) * math.sin(a))), A((90, 80, 70)))
    for t in range(int(r * 0.55) + 1): P(im, int(cx), int(cy - t), A((40, 34, 40)))
    for t in range(int(r * 0.8) + 1): P(im, int(cx + t * 0.7), int(cy + t * 0.3), A((40, 34, 40)))


def ball_plaque(im, cx, cy):
    disc(im, cx, cy, 6.6, A(OUTL)); disc(im, cx, cy, 5.8, A((244, 244, 248)))
    for y in range(int(cy - 6), int(cy)):
        for x in range(int(cx - 6), int(cx + 7)):
            if (x + 0.5 - cx) ** 2 + (y + 0.5 - cy) ** 2 <= 5.8 ** 2: P(im, x, y, A((216, 60, 56)))
    H(im, int(cx - 6), int(cx + 6), int(cy), A(OUTL)); disc(im, cx, cy + 0.4, 2.2, A(OUTL)); disc(im, cx, cy + 0.4, 1.3, A((244, 244, 248)))
    P(im, int(cx - 3), int(cy - 4), A((250, 150, 140)))


ROOFS = {'verd': VERD, 'slate': SLATEB, 'brass': BRASS, 'terra': [(92, 38, 30), (148, 62, 44), (196, 98, 70), (226, 140, 104), (246, 186, 150)],
         'wine': [(60, 20, 34)] + WINE, 'iron': IRN}
WALLS = {'marble': MARBLE, 'cream': CREAM, 'soot': SOOT, 'brick': BRICKR, 'slate': SLATEB}
AWNS = {'teal': (TEALC, (236, 228, 214)), 'wine': (WINE, (240, 220, 170)), 'navy': (BLUEC, (236, 228, 214)),
        'gold': (BRASS, (250, 244, 226)), 'red': (RED, (240, 232, 220)), 'soot': (SOOT, (170, 150, 120))}


def awning(im, x0, x1, y, kind, depth=5):
    ramp, light = AWNS[kind]
    for yy in range(depth):
        for x in range(x0, x1 + 1):
            c = ramp[2] if ((x - x0) // 3) % 2 == 0 else light
            if yy == 0: c = ramp[3] if c == ramp[2] else (255, 252, 240)
            P(im, x, y + yy, A(c))
    for x in range(x0, x1 + 1):                     # scalloped hem
        if (x - x0) % 3 != 1: P(im, x, y + depth, A(ramp[1] if ((x - x0) // 3) % 2 == 0 else ramp[0]))
    H(im, x0, x1, y + depth + 1, (20, 16, 24, 70))


GOODS = {'books': [(120, 40, 40), (40, 70, 110), (60, 100, 60), (200, 170, 90)], 'cloth': [(196, 60, 70), (60, 110, 170), (220, 190, 80)],
         'lamps': [(255, 220, 130), (255, 196, 90), (250, 240, 200)], 'soda': [(80, 200, 230), (255, 120, 80), (250, 240, 120)],
         'cakes': [(250, 210, 220), (240, 160, 180), (250, 240, 220)], 'gears': [(194, 148, 60), (140, 150, 160), (230, 194, 100)],
         'flowers': [(240, 90, 120), (250, 220, 110), (200, 140, 240)], 'junk': [(110, 90, 70), (140, 130, 110), (90, 100, 90)]}


def shopfront(im, x0, x1, gtop, h, goods, lit=True, frame=BRASS):
    R(im, x0, gtop + 7, x1, h - 3, A(frame[1]))
    R(im, x0 + 1, gtop + 8, x1 - 1, h - 4, A(LITW[1] if lit else GLS[1]))
    R(im, x0 + 1, gtop + 8, x1 - 1, gtop + 10, A(LITW[2] if lit else GLS[2]))
    for x in range(x0 + 4, x1, 5): Vl(im, x, gtop + 8, h - 4, A(frame[2]))
    rng = random.Random(x0 * 7 + gtop)
    for x in range(x0 + 1, x1):
        if rng.random() < 0.75: P(im, x, h - 5, A(rng.choice(GOODS[goods])))
        if rng.random() < 0.5: P(im, x, h - 6, A(rng.choice(GOODS[goods])))
    H(im, x0, x1, h - 3, A(MARBLE[4])); H(im, x0, x1, h - 2, A(MARBLE[1]))


def glass_door(im, dx, gtop, h, wide=False, frame=BRASS, lit=True, iron=False):
    x0, x1 = (dx + 2, dx + 13) if not wide else (dx - 4, dx + 19)
    if iron:
        R(im, x0, gtop + 5, x1, h - 1, A(IRN[1])); R(im, x0 + 1, gtop + 6, x1 - 1, h - 1, A(IRN[2]))
        for x in range(x0 + 2, x1, 3): Vl(im, x, gtop + 6, h - 2, A(IRN[0]))
        H(im, x0, x1, gtop + 5, A(IRN[3])); P(im, x1 - 2, gtop + 14, A(BRASS[3]))
        return
    R(im, x0, gtop + 2, x1, h - 1, A(frame[1]))
    cx = (x0 + x1) / 2.0; r = (x1 - x0) / 2.0
    for y in range(gtop - 2, gtop + 4):              # the fanlight
        for x in range(x0, x1 + 1):
            if (x + 0.5 - cx - 0.5) ** 2 / (r * r) + ((y - gtop - 3) / 5.5) ** 2 <= 1:
                P(im, x, y, A(frame[2]))
                if (x + 0.5 - cx - 0.5) ** 2 / ((r - 1.5) ** 2) + ((y - gtop - 3) / 4.2) ** 2 <= 1: P(im, x, y, A(LITW[3] if lit else GLS[3]))
    R(im, x0 + 1, gtop + 4, x1 - 1, h - 1, A(LITW[1] if lit else GLS[1]))
    R(im, x0 + 1, gtop + 4, x1 - 1, gtop + 7, A(LITW[2] if lit else GLS[2]))
    mx = (x0 + x1) // 2
    Vl(im, mx, gtop + 4, h - 1, A(frame[2])); Vl(im, mx + 1, gtop + 4, h - 1, A(frame[0]))
    P(im, mx - 2, gtop + 13, A(frame[4])); P(im, mx + 3, gtop + 13, A(frame[4]))
    H(im, x0 - 1, x1 + 1, h - 1, A(MARBLE[3]))


def bldg(W, floors, roof='verd', wall='marble', door=None, seed=1, shop=None, awn=None, neon=None, clock=False,
         dome=False, balcony=(), lit=0.4, wins='arch', pil=True, roof_rows=2, chim=0, glass=(), plaque=None,
         board=None, flag=None, fire=False, laundry=False, graffiti=False, pipes=False, lamps=True, wide_door=False,
         iron_door=False, dormers=True, ground=None, crest=True, soot=0.0, boarded=0.0, frame=BRASS, aerial=False):
    """A Lumen building W tiles wide.  floors: upper-storey heights in px (the ground storey is always 24 px).
    roof: verd / slate / brass / terra / wine mansard, 'flat' (parapet, tanks, skylights), 'vault' (glass barrel vault).
    glass: indices of upper floors drawn as a glass curtain bay.  Returns (image, code rows, door cell)."""
    rng = random.Random(seed * 31 + W)
    door = W // 2 if door is None else door
    wall_h = sum(floors) + 24
    Hh = roof_rows + -(-wall_h // 16)
    w, h = W * 16, Hh * 16
    im = Image.new('RGBA', (w, h), CLEAR)
    fy = h - wall_h
    wr = WALLS[wall]
    if wall in ('marble', 'cream') and wall == 'marble': fac = ashlar(w, wall_h, wr, seed)
    elif wall == 'cream': fac = plaster(w, wall_h, wr, seed)
    else: fac = brickwall(w, wall_h, wr, seed, soot=soot)
    im.alpha_composite(fac, (0, fy))
    gtop = h - 24
    # ground storey: rusticated plinth
    if ground != 'same':
        gr = MARBLE if wall in ('marble', 'cream') else SOOT if wall == 'soot' else IRN if wall == 'slate' else BRICKR
        g = ashlar(w, 24, gr if wall != 'cream' else MARBLE, seed + 9, course=6, block=(14, 22))
        im.alpha_composite(g, (0, gtop))
        H(im, 0, w - 1, gtop, A(gr[4])); H(im, 0, w - 1, gtop + 1, A(gr[3]))
    # glass curtain bays
    for k, fh in enumerate(floors):
        if k in glass:
            yy = fy + sum(floors[:k])
            R(im, 3, yy + 1, w - 4, yy + fh - 2, A(GLS[1]))
            for x in range(3, w - 3):
                for y2 in range(yy + 1, yy + fh - 1):
                    t = (x * 0.6 + (y2 - yy) * 1.3 + seed) % 23
                    if t < 2.2: P(im, x, y2, A(GLS[3]))
                    elif t < 6: P(im, x, y2, A(GLS[2]))
            for x in range(3, w - 3, 5): Vl(im, x, yy + 1, yy + fh - 2, A(frame[2])); Vl(im, x + 1, yy + 1, yy + fh - 2, A(frame[0]))
            if rng.random() < 0.6:
                for x in range(5, w - 5, 5):
                    if rng.random() < lit: R(im, x + 1, yy + fh - 6, x + 3, yy + fh - 3, A(LITW[2]))
    # pilasters
    if pil:
        cols = [0, w - 3]
        if W >= 7 and wall in ('marble', 'cream'): cols += [w // 2 - 1] if W % 2 else []
        for x in cols:
            R(im, x, fy, x + 2, gtop - 1, A(MARBLE[3])); Vl(im, x, fy, gtop - 1, A(MARBLE[4])); Vl(im, x + 2, fy, gtop - 1, A(MARBLE[1]))
            R(im, x - (1 if x else 0), fy + 3, x + 2 + (1 if x < w - 3 else 0), fy + 4, A(MARBLE[4]))
    # string courses
    for k in range(1, len(floors) + 1):
        yy = fy + sum(floors[:k]) - 1
        H(im, 0, w - 1, yy, A(frame[1] if wall in ('marble', 'cream') else wr[0])); H(im, 0, w - 1, yy + 1, A(frame[3] if wall in ('marble', 'cream') else wr[3]))
    # windows
    nwin = W
    for k, fh in enumerate(floors):
        if k in glass: continue
        yy = fy + sum(floors[:k])
        kind = wins if not isinstance(wins, (list, tuple)) else wins[k % len(wins)]
        for i in range(nwin):
            sx = i * 16 + 4
            if pil and (i == 0 or i == nwin - 1) and W >= 4: sx = i * 16 + (5 if i == 0 else 4)
            if fire and i == nwin - 2: pass
            wh = fh - 6
            if kind == 'arch' and wh >= 8:
                arch_window(im, sx, yy + 3, 7, wh, rng.random() < lit, frame=frame)
            elif kind == 'round':
                cx, cy = sx + 3, yy + fh // 2
                disc(im, cx + 0.5, cy, 3.6, A(frame[1])); disc(im, cx + 0.5, cy, 2.6, A(LITW[2] if rng.random() < lit else GLS[2]))
                P(im, cx - 1, cy - 1, A(GLS[3]))
            else:
                rect_window(im, sx, yy + 3, 7, max(6, wh), rng.random() < lit, frame=frame if wall in ('marble', 'cream') else (WOODL[1], WOODL[2], WOODL[3], WOODL[4], WOODL[4]),
                            shutters=(WOODL if wall == 'soot' and rng.random() < 0.4 else None), boarded=rng.random() < boarded)
        if k in balcony:
            by = yy + fh - 3
            R(im, 2, by, w - 3, by + 1, A(MARBLE[3])); H(im, 2, w - 3, by + 2, A(MARBLE[1]))
            for x in range(2, w - 2, 2): Vl(im, x, by - 4, by - 1, A(IRN[1]))
            H(im, 2, w - 3, by - 4, A(IRN[2]))
    # ground storey: door, shops, lamps
    dx = door * 16
    if shop:
        goods = shop
        lx0, lx1 = 3, dx - 3; rx0, rx1 = dx + 19, w - 4
        if wide_door: lx1 -= 5; rx0 += 5
        for a, b in ((lx0, lx1), (rx0, rx1)):
            if b - a >= 8:
                shopfront(im, a, b, gtop, h, goods, lit=True, frame=frame)
                if awn: awning(im, a - 1, b + 1, gtop + 1, awn)
    else:
        for gx in range(W):
            if abs(gx - door) <= (1 if wide_door else 0): continue
            if wall == 'soot': rect_window(im, gx * 16 + 4, gtop + 8, 7, 9, rng.random() < lit * 0.8, frame=(WOODL[1], WOODL[2], WOODL[3], WOODL[4], WOODL[4]), boarded=rng.random() < boarded)
            else: arch_window(im, gx * 16 + 4, gtop + 6, 7, 13, rng.random() < lit, frame=frame)
    glass_door(im, dx, gtop, h, wide=wide_door, frame=frame, lit=True, iron=iron_door)
    if lamps and not iron_door:
        wall_lamp(im, dx + (-6 if wide_door else 0), gtop + 6); wall_lamp(im, dx + (20 if wide_door else 14), gtop + 6)
    elif lamps:
        wall_lamp(im, dx + 14, gtop + 4, lit=rng.random() < 0.6)
    if plaque == 'ball': ball_plaque(im, dx + 8, gtop - 6)
    if board:
        bc, n = board; bx0, bx1 = max(3, dx - 6 * n), min(w - 4, dx + 15 + 6 * n)
        R(im, bx0, gtop - 4, bx1, gtop + 3, A(bc[1])); H(im, bx0, bx1, gtop - 4, A(bc[3])); H(im, bx0, bx1, gtop + 3, A(bc[0]))
        Vl(im, bx0, gtop - 4, gtop + 3, A(BRASS[3])); Vl(im, bx1, gtop - 4, gtop + 3, A(BRASS[1]))
        for i, x in enumerate(range(bx0 + 3, bx1 - 2, 3)):
            if i % 4 != 3: R(im, x, gtop - 2, x + 1, gtop + 1 - (i % 2), A(BRASS[4]))
    if neon:
        nx = w - 9 if door < W - 1 else 3
        neon_blade(im, nx, fy + 4, min(28, wall_h - 30), neon, seed)
    # Lowlight dressing
    if pipes:
        for px_ in ([w - 6] if W < 6 else [5, w - 6]):
            Vl(im, px_, fy, h - 2, A(IRN[2])); Vl(im, px_ + 1, fy, h - 2, A(IRN[1]))
            for y in range(fy + 4, h, 8): H(im, px_ - 1, px_ + 2, y, A(IRN[3]))
    if fire and len(floors) >= 2:                    # an iron fire escape: landings and a zigzag stair
        fx0, fx1 = w - 30, w - 5
        for k in range(len(floors)):
            yy = fy + sum(floors[:k + 1]) - 2
            R(im, fx0, yy, fx1, yy + 1, A(IRN[2])); H(im, fx0, fx1, yy + 2, A(IRN[0]))
            for x in range(fx0, fx1 + 1, 2): Vl(im, x, yy - 5, yy - 1, A(IRN[1]))
            H(im, fx0, fx1, yy - 5, A(IRN[3]))
            if k < len(floors) - 1:
                y2 = fy + sum(floors[:k + 2]) - 2; y1 = yy
                for t in range(10):
                    xx = (fx0 + 2 + t) if k % 2 == 0 else (fx1 - 2 - t)
                    yy2 = y1 + (y2 - y1) * t // 10
                    P(im, xx, yy2, A(IRN[3])); P(im, xx, yy2 + 1, A(IRN[1]))
    if laundry and len(floors) >= 1:
        k = 0; yy = fy + 3
        cols = [(230, 230, 220), (200, 80, 80), (90, 130, 200), (230, 200, 90), (150, 190, 140)]
        for x in range(4, w - 4): P(im, x, yy + int(1.5 * math.sin(math.pi * (x - 4) / max(1, w - 8))), A((70, 60, 60)))
        x = 6
        while x < w - 8:
            c = rng.choice(cols); ww = rng.randrange(3, 6)
            base = yy + int(1.5 * math.sin(math.pi * (x - 4) / max(1, w - 8))) + 1
            R(im, x, base, x + ww - 1, base + rng.randrange(4, 7), A(c)); Vl(im, x + ww - 1, base, base + 4, A(tuple(int(v * 0.8) for v in c)))
            x += ww + rng.randrange(2, 5)
    if graffiti:                                     # the Hollow Ring: a ring with one bar through it
        gx, gy = (4 if door > 1 else w - 16), gtop + 5
        cx, cy = gx + 6, gy + 7
        for a in range(0, 360, 8):
            r = 5.2
            P(im, int(cx + r * math.cos(math.radians(a))), int(cy + r * math.sin(math.radians(a))), A((214, 206, 230)))
            P(im, int(cx + (r - 1) * math.cos(math.radians(a))), int(cy + (r - 1) * math.sin(math.radians(a))), A((150, 120, 200)))
        Vl(im, cx, cy - 7, cy + 7, A((214, 206, 230))); Vl(im, cx + 1, cy - 6, cy + 6, A((150, 120, 200)))
    # cornice at the eave
    dentils(im, 0, w - 1, fy - 2, MARBLE if wall in ('marble', 'cream') else (SOOT if wall == 'soot' else BRICKR))
    if wall in ('marble', 'cream'): H(im, 0, w - 1, fy + 2, A(frame[2]))
    shade_box(im, 1, fy + 2, w - 2, fy + 4, 0.8)
    Vl(im, 0, fy - 2, h - 1, A(OUTL)); Vl(im, w - 1, fy - 2, h - 1, A(OUTL))
    # ---------------- roof
    ry0, ry1 = 2, fy - 2
    if roof == 'flat':
        R(im, 1, ry0, w - 2, ry1, A(IRN[2] if wall != 'soot' else SOOT[1]))
        for y in range(ry0 + 3, ry1, 6): H(im, 3, w - 4, y, A(IRN[1] if wall != 'soot' else SOOT[0]))
        for x in range(4, w - 4, 9): Vl(im, x, ry0 + 3, ry1 - 1, A(IRN[3] if wall != 'soot' else SOOT[2]))
        bev(im, 1, ry0, w - 2, ry0 + 2, MARBLE if wall in ('marble', 'cream') else SOOT, 3)
        Vl(im, 1, ry0, ry1, A(MARBLE[3] if wall in ('marble', 'cream') else SOOT[3])); Vl(im, w - 2, ry0, ry1, A(MARBLE[1] if wall in ('marble', 'cream') else SOOT[1]))
        props = ['tank', 'sky', 'vent', 'garden'] if wall != 'soot' else ['tank', 'vent', 'shack', 'vent']
        x = 4; k = 0
        while x < w - 12 and ry1 - ry0 >= 10:
            pr = props[(seed + k) % len(props)]
            if pr == 'tank':
                disc(im, x + 5, ry0 + 9, 4.6, A(WOODL[1])); disc(im, x + 5, ry0 + 8, 4.0, A(WOODL[3])); disc(im, x + 5, ry0 + 8, 2.4, A(WOODL[2]))
                H(im, x + 1, x + 9, ry0 + 9, A(IRN[1]))
            elif pr == 'sky':
                R(im, x, ry0 + 5, x + 10, ry1 - 3, A(frame[1])); R(im, x + 1, ry0 + 6, x + 9, ry1 - 4, A(GLS[2]))
                for xx in range(x + 1, x + 10, 3): Vl(im, xx, ry0 + 6, ry1 - 4, A(frame[2]))
                P(im, x + 2, ry0 + 7, A(GLS[4]))
            elif pr == 'vent':
                R(im, x + 2, ry0 + 5, x + 5, ry0 + 11, A(IRN[3])); H(im, x + 1, x + 6, ry0 + 5, A(IRN[4])); H(im, x + 2, x + 5, ry0 + 11, A(IRN[1]))
            elif pr == 'garden':
                R(im, x, ry0 + 6, x + 10, ry1 - 3, A(WOODL[1]))
                for xx in range(x + 1, x + 10):
                    for yy in range(ry0 + 6, ry1 - 3):
                        if nz(xx, yy, seed) < 0.75: P(im, xx, yy, A(LEAFL[1 + int(nz(xx, yy, seed + 1) * 3)]))
            elif pr == 'shack':
                R(im, x, ry0 + 4, x + 9, ry1 - 2, A(WOODL[2])); H(im, x, x + 9, ry0 + 4, A(IRN[3]))
                for xx in range(x, x + 10, 2): Vl(im, xx, ry0 + 5, ry1 - 2, A(WOODL[1]))
            x += 14; k += 1
        if aerial:
            Vl(im, w - 7, 0, ry0 + 8, A(IRN[2])); P(im, w - 7, 0, A((255, 80, 60)))
            H(im, w - 9, w - 5, 3, A(IRN[2]))
    elif roof == 'vault':
        for y in range(ry0, ry1 + 1):
            t = (y - ry0) / max(1, ry1 - ry0)
            for x in range(1, w - 1):
                c = GLS[3] if t < 0.25 else GLS[2] if t < 0.65 else GLS[1]
                P(im, x, y, A(c))
        for x in range(1, w - 1, 6): Vl(im, x, ry0, ry1, A(frame[2]))
        H(im, 1, w - 2, ry0, A(frame[3])); H(im, 1, w - 2, (ry0 + ry1) // 2, A(frame[1]))
        for x in range(3, w - 3, 12): P(im, x, ry0 + 2, A(GLS[4])); P(im, x + 1, ry0 + 3, A(GLS[4]))
        Vl(im, 1, ry0, ry1, A(frame[3])); Vl(im, w - 2, ry0, ry1, A(frame[1]))
    else:
        rr = ROOFS[roof]
        im.alpha_composite(scales(w - 2, ry1 - ry0, rr, seed).crop((0, 0, w - 2, ry1 - ry0)), (1, ry0))
        span = max(1, ry1 - ry0)
        for y in range(ry0, ry1):
            shade_box(im, 1, y, w - 2, y, 1.12 - 0.30 * (y - ry0) / span)
        for x in range(1, 6):                       # hipped ends
            shade_box(im, x, ry0, x, ry1 - 1, 1.08); shade_box(im, w - 1 - x, ry0, w - 1 - x, ry1 - 1, 0.84)
        R(im, 1, ry0 - 2, w - 2, ry0, A(BRASS[2] if crest else rr[3]))
        H(im, 1, w - 2, ry0 - 2, A(BRASS[3] if crest else rr[4])); H(im, 1, w - 2, ry0, A(BRASS[1] if crest else rr[1]))
        if crest:
            for x in range(4, w - 3, 4): P(im, x, ry0 - 3, A(BRASS[3])); P(im, x, ry0 - 4, A(BRASS[4]))
        Vl(im, 0, ry0 - 2, ry1, A(OUTL)); Vl(im, w - 1, ry0 - 2, ry1, A(OUTL))
        if dormers and span >= 12:
            n = max(1, W // 3)
            for k in range(n):
                cx = int((k + 0.5) * w / n); cy = ry0 + span // 2
                disc(im, cx, cy + 1, 4.4, A(rr[0])); disc(im, cx, cy, 4.0, A(MARBLE[3]))
                disc(im, cx, cy, 3.0, A(frame[1])); disc(im, cx, cy, 2.2, A(LITW[2] if rng.random() < lit else GLS[2]))
                P(im, cx - 1, cy - 1, A(GLS[4]))
        for c in range(chim):
            cx = 6 + int((c + 0.5) * (w - 12) / max(1, chim))
            R(im, cx, max(0, ry0 - 1), cx + 4, ry0 + 6, A(BRICKR[2])); H(im, cx - 1, cx + 5, max(0, ry0 - 1), A(BRICKR[4]))
            Vl(im, cx + 4, ry0, ry0 + 6, A(BRICKR[0]))
    if dome:
        cx = w // 2; rx = min(w // 2 - 4, 22); ry_ = min(ry1 - ry0, 18)
        base = ry1 - 1
        for y in range(base - ry_, base + 1):
            for x in range(cx - rx, cx + rx + 1):
                if ((x - cx) / rx) ** 2 + ((y - base) / ry_) ** 2 <= 1:
                    t = (x - cx + rx) / (2.0 * rx)
                    c = GLS[3] if t < 0.3 else GLS[2] if t < 0.7 else GLS[1]
                    if ((x - cx) / rx) ** 2 + ((y - base) / ry_) ** 2 > 0.86: c = frame[1]
                    P(im, x, y, A(c))
        for k in range(-2, 3):
            for y in range(base - ry_, base + 1):
                xx = cx + int(k * rx * 0.45 * math.sqrt(max(0, 1 - ((y - base) / ry_) ** 2)))
                P(im, xx, y, A(frame[2]))
        H(im, cx - rx, cx + rx, base, A(frame[2]))
        R(im, cx - 1, base - ry_ - 3, cx + 1, base - ry_, A(frame[3]))
    if clock:
        clock_face(im, w // 2, fy - 4 if roof == 'flat' else ry0 + (ry1 - ry0) // 2, 5)
    if flag:
        fx = w - 10
        Vl(im, fx, 0, 12, A(IRN[2])); R(im, fx + 1, 1, fx + 9, 6, A(flag[1])); H(im, fx + 1, fx + 9, 1, A(flag[2]))
        disc(im, fx + 5, 3.5, 1.6, A(BRASS[3]))
    code = []                                         # the whole roof is solid (Lumen packs its blocks: no walking behind)
    for ty in range(Hh):
        if ty * 16 < fy - 8: code.append('r' * W)
        else: code.append('W' * W)
    row = list(code[-1]); row[door] = 'D'; code[-1] = ''.join(row)
    return im, code, (door, Hh - 1)


# ================================================================== civic pieces
def spire():
    """Meridian Spire's base: a marble podium with a grand door, and the black-cored tower rising out of the map"""
    pim, pcode, _ = bldg(16, [18, 18], roof='flat', wall='marble', door=8, seed=41, wide_door=True, lit=0.7,
                         board=(IRN, 5), balcony=(1,), clock=False, glass=(1,))
    shaft_rows = 7
    W = 16; Hh = len(pcode) + shaft_rows
    im = new(W, Hh); im.alpha_composite(pim, (0, shaft_rows * 16))
    x0, x1 = 5 * 16, 11 * 16 - 1
    top_y = 0; bot_y = shaft_rows * 16 + 14
    for y in range(top_y, bot_y + 1):
        for x in range(x0, x1 + 1):
            t = (x - x0) / (x1 - x0)
            c = (30, 28, 40) if t < 0.15 else (44, 42, 58) if t < 0.5 else (22, 20, 30)
            if (x - x0) % 12 in (0, 1): c = BRASS[2] if (x - x0) % 12 == 0 else BRASS[0]
            if 0.47 < t < 0.53: c = (120, 60, 200) if (y // 3) % 2 else (70, 30, 140)        # the Dark Stone's seam of black light
            if y % 24 == 0: c = BRASS[3]
            if y % 24 in (8, 9, 16, 17) and (x - x0) % 12 in (4, 5, 7, 8) and not (0.4 < t < 0.6):
                c = LITW[2] if nz(x // 12, y // 8, 5) < 0.45 else GLS[2]
            P(im, x, y, A(c))
    for y in range(top_y, bot_y + 1):
        P(im, x0, y, A(BRASS[3])); P(im, x1, y, A(BRASS[0]))
        blend(im, x0 - 1, y, (120, 60, 200), 0.25); blend(im, x1 + 1, y, (120, 60, 200), 0.25)
    # the sunburst on the podium front
    cx, cy = 128, shaft_rows * 16 + 30
    for k in range(16):
        a = k * math.pi / 8
        for r in range(6, 13 if k % 2 == 0 else 10):
            P(im, int(cx + r * math.cos(a)), int(cy + r * math.sin(a) * 0.6), A(BRASS[3] if r % 2 else BRASS[2]))
    disc(im, cx, cy, 5.5, A(BRASS[1])); disc(im, cx, cy, 4.5, A(BRASS[3])); disc(im, cx, cy, 2.2, A((120, 60, 200)))
    code = ['.' * 5 + 'r' * 6 + '.' * 5 for _ in range(shaft_rows)]
    pcode = list(pcode); pcode[0] = 'r' * 16
    code = code + pcode
    return im, code, (8, Hh - 1)


def gym_front():
    """Rook Calder's Circuit Gym: a black-glass studio, the neon bolt, ON AIR, the broadcast mast"""
    im, code, door = bldg(10, [18, 18], roof='flat', wall='slate', seed=51, glass=(0, 1), neon=MAGENTA, lit=0.5,
                          wide_door=True, aerial=True, frame=IRN, pil=False)
    gtop = im.height - 24
    pts = [(80, gtop - 30), (72, gtop - 16), (79, gtop - 16), (70, gtop - 2), (88, gtop - 20), (81, gtop - 20), (88, gtop - 30)]
    d = ImageDraw.Draw(im)
    d.polygon(pts, fill=A(CYAN[2]), outline=A(CYAN[3]))
    for x, y in pts: glow(im, x, y, 6, CYAN[2], 0.3)
    R(im, 106, gtop - 26, 125, gtop - 19, A((60, 10, 14))); R(im, 107, gtop - 25, 124, gtop - 20, A((230, 40, 40)))
    for x in range(109, 123, 3): R(im, x, gtop - 24, x + 1, gtop - 21, A((255, 220, 210)))
    glow(im, 116, gtop - 22, 9, (255, 60, 60), 0.3)
    return im, code, door


# ================================================================== street furniture
def arclamp(lit=True, num=None, banner=None):
    im = new(1, 3)
    R(im, 6, 44, 9, 47, A(BRASS[1])); H(im, 5, 10, 44, A(BRASS[3])); H(im, 5, 10, 47, A(BRASS[0]))
    Vl(im, 7, 8, 43, A(IRN[3])); Vl(im, 8, 8, 43, A(IRN[1]))
    for y in (20, 32): H(im, 6, 9, y, A(BRASS[2]))
    if num is not None:
        R(im, 5, 34, 10, 38, A(BRASS[2])); H(im, 5, 10, 34, A(BRASS[3])); P(im, 7, 36, A(IRN[0])); P(im, 8, 36, A(IRN[0]))
    H(im, 3, 12, 8, A(BRASS[2])); P(im, 3, 9, A(BRASS[1])); P(im, 12, 9, A(BRASS[1]))
    disc(im, 7.5, 4.5, 3.6, A(BRASS[1]))
    disc(im, 7.5, 4.5, 2.9, A(CYAN[3] if lit else (200, 210, 220)))
    if lit:
        disc(im, 7.5, 4.5, 1.6, A((255, 255, 255)))
        glow(im, 7.5, 4.5, 8, (190, 240, 255), 0.45)
    H(im, 6, 9, 0, A(BRASS[3]))
    if banner:
        R(im, 9, 12, 13, 28, A(banner[1])); Vl(im, 9, 12, 28, A(banner[2])); H(im, 9, 13, 12, A(BRASS[3]))
        P(im, 11, 16, A(BRASS[4])); R(im, 10, 18, 12, 20, A(BRASS[3])); P(im, 11, 19, A(banner[1]))
        H(im, 10, 12, 23, A((240, 236, 220))); H(im, 10, 12, 25, A((240, 236, 220)))
        P(im, 9, 29, A(banner[1])); P(im, 11, 29, A(banner[1])); P(im, 13, 29, A(banner[1]))
    return im


def holo():
    im = new(1, 3)
    R(im, 5, 40, 10, 47, A(BRASS[1])); H(im, 5, 10, 40, A(BRASS[3]))
    R(im, 6, 18, 9, 39, A(IRN[2])); Vl(im, 6, 18, 39, A(IRN[3]))
    for y in range(2, 18):
        for x in range(2, 14):
            a = 0.45 + 0.25 * ((y % 3) == 0)
            blend(im, x, y, CYAN[2], a)
    for y in range(4, 16, 3): H(im, 4, 11, y, A(CYAN[3]))
    disc(im, 8, 10, 2.5, A(MAGENTA[2]))
    return im


def bench():
    im = new(2, 1)
    R(im, 1, 5, 30, 8, A(WOODL[3])); H(im, 1, 30, 5, A(WOODL[4])); H(im, 1, 30, 8, A(WOODL[1]))
    R(im, 1, 10, 30, 12, A(WOODL[2])); H(im, 1, 30, 10, A(WOODL[3]))
    for x in (2, 15, 28): R(im, x, 4, x + 1, 15, A(BRASS[1])); P(im, x, 4, A(BRASS[3]))
    H(im, 2, 29, 15, (20, 16, 24, 80))
    return im


def bollard():
    im = new()
    R(im, 5, 5, 10, 14, A(BRASS[2])); Vl(im, 5, 5, 14, A(BRASS[3])); Vl(im, 10, 5, 14, A(BRASS[0]))
    disc(im, 7.5, 5, 3, A(BRASS[3])); P(im, 6, 4, A(BRASS[4])); H(im, 5, 10, 10, A(BRASS[1])); H(im, 4, 11, 15, (20, 16, 24, 90))
    return im


def planter(w=2, flowers=True):
    im = new(w, 1)
    R(im, 1, 6, w * 16 - 2, 15, A(MARBLE[2])); H(im, 1, w * 16 - 2, 6, A(MARBLE[4])); H(im, 1, w * 16 - 2, 7, A(BRASS[2]))
    H(im, 1, w * 16 - 2, 15, A(MARBLE[0])); Vl(im, w * 16 - 2, 6, 15, A(MARBLE[1]))
    r = random.Random(w)
    for x in range(2, w * 16 - 2):
        for y in range(1, 7):
            if nz(x, y, 5) < 0.8 - y * 0.05: P(im, x, y, A(LEAFL[1 + int(nz(x, y, 6) * 3)]))
    if flowers:
        for _ in range(8 * w):
            x, y = r.randrange(3, w * 16 - 3), r.randrange(1, 6)
            P(im, x, y, A(r.choice([(240, 90, 120), (250, 220, 110), (200, 140, 240), (255, 255, 255)])))
    return im


def topiary():
    im = new(1, 2)
    R(im, 3, 24, 12, 31, A(BRASS[2])); H(im, 3, 12, 24, A(BRASS[3])); Vl(im, 12, 24, 31, A(BRASS[0]))
    Vl(im, 7, 18, 23, A(WOODL[1]))
    for y in range(2, 19):
        for x in range(1, 15):
            if (x - 7.5) ** 2 / 42.0 + (y - 10) ** 2 / 64.0 <= 1:
                n = nz(x, y, 9); c = LEAFL[3] if (x < 7 and y < 9) else LEAFL[2] if n < 0.6 else LEAFL[1]
                if (x - 7.5) ** 2 / 42.0 + (y - 10) ** 2 / 64.0 > 0.8: c = LEAFL[0] if x > 7 or y > 12 else LEAFL[2]
                P(im, x, y, A(c))
    return im


def street_tree():
    im = new(2, 3)
    for y in range(36, 48): R(im, 4, y, 27, y, A(IRN[1] if y in (36, 47) else IRN[2]))
    for x in range(6, 26, 3): Vl(im, x, 37, 46, A(IRN[0]))
    Vl(im, 15, 28, 40, A(WOODL[1])); Vl(im, 16, 28, 40, A(WOODL[2]))
    for y in range(0, 32):
        for x in range(0, 32):
            q = (x - 15.5) ** 2 / 210.0 + (y - 15) ** 2 / 200.0
            if q <= 1 + 0.25 * (nz(x // 2, y // 2, 4) - 0.5):
                n = smooth(x, y, 12, 4.0)
                c = LEAFL[3] if n > 0.62 and (x + y) < 34 else LEAFL[2] if n > 0.4 else LEAFL[1]
                if q > 0.85 and (x > 16 or y > 20): c = LEAFL[0]
                P(im, x, y, A(c))
    for _ in range(14):
        r = random.Random(_)
        x, y = 4 + (_ * 7) % 24, 4 + (_ * 11) % 22
        P(im, x, y, A((250, 236, 170)))
    return im


def kiosk():
    """the Fizzbolt soda kiosk: a striped awning, a cooler of bottles, crates"""
    im = new(3, 2)
    R(im, 2, 14, 45, 31, A(TEALC[1])); H(im, 2, 45, 14, A(TEALC[3]))
    R(im, 5, 18, 42, 26, A(GLS[1]))
    r = random.Random(4)
    for x in range(6, 42, 3):
        c = r.choice(GOODS['soda']); R(im, x, 20, x + 1, 25, A(c)); P(im, x, 20, A((240, 240, 240)))
    R(im, 2, 27, 45, 31, A(WOODL[2])); H(im, 2, 45, 27, A(WOODL[4]))
    for yy in range(0, 10):
        for x in range(0, 48):
            c = (240, 90, 60) if (x // 4) % 2 == 0 else (250, 240, 220)
            if yy == 0: c = (255, 140, 100) if c[0] == 240 else (255, 252, 240)
            P(im, x, yy + 2, A(c))
    for x in range(0, 48):
        if x % 4 != 1: P(im, x, 12, A((180, 60, 40) if (x // 4) % 2 == 0 else (200, 190, 170)))
    R(im, 14, 4, 33, 9, A((30, 160, 200))); H(im, 14, 33, 4, A((120, 230, 255)))
    for x in range(16, 32, 3): R(im, x, 6, x + 1, 7, A((255, 255, 255)))
    return im


def news():
    im = new(1, 2)
    R(im, 2, 10, 13, 30, A(TEALC[1])); H(im, 2, 13, 10, A(TEALC[3])); Vl(im, 13, 10, 30, A(TEALC[0]))
    R(im, 4, 13, 11, 20, A((236, 232, 220)))
    for y in range(14, 20, 2): H(im, 5, 10, y, A((120, 116, 110)))
    R(im, 4, 22, 11, 27, A((236, 232, 220))); H(im, 5, 10, 23, A((200, 60, 60)))
    H(im, 2, 13, 31, (20, 16, 24, 80))
    return im


def clockpost():
    im = new(1, 3)
    R(im, 5, 42, 10, 47, A(BRASS[1])); H(im, 5, 10, 42, A(BRASS[3]))
    Vl(im, 7, 14, 41, A(IRN[3])); Vl(im, 8, 14, 41, A(IRN[1]))
    clock_face(im, 7.5, 7.5, 6)
    return im


def statue():
    """the Founders' Lamp: a bronze figure lifting a lamp, on a marble plinth"""
    im = new(2, 3)
    R(im, 4, 30, 27, 47, A(MARBLE[2])); H(im, 4, 27, 30, A(MARBLE[4])); H(im, 4, 27, 31, A(MARBLE[3])); Vl(im, 27, 30, 47, A(MARBLE[1]))
    H(im, 2, 29, 44, A(MARBLE[3])); R(im, 2, 45, 29, 47, A(MARBLE[1]))
    R(im, 10, 36, 21, 40, A(BRASS[1])); H(im, 11, 20, 37, A(BRASS[3]))
    BZ = [(60, 46, 36), (96, 72, 50), (132, 100, 66), (176, 138, 88)]
    R(im, 12, 14, 19, 29, A(BZ[1])); Vl(im, 12, 14, 29, A(BZ[2])); Vl(im, 19, 14, 29, A(BZ[0]))
    R(im, 10, 22, 21, 29, A(BZ[1])); H(im, 10, 21, 29, A(BZ[0]))
    disc(im, 15.5, 11, 3.2, A(BZ[2])); P(im, 14, 10, A(BZ[3]))
    Vl(im, 20, 3, 15, A(BZ[2])); Vl(im, 21, 3, 15, A(BZ[0]))
    disc(im, 21, 3, 2.6, A(AMBER[2])); glow(im, 21, 3, 7, AMBER[2], 0.5)
    return im


def prism_fountain():
    """the Prism fountain (6x5): an octagonal marble basin, light water, a glass prism throwing colours"""
    im = new(6, 5)
    cx, cy = 48, 48; rx, ry = 44, 26
    for y in range(80):
        for x in range(96):
            q = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
            qi = ((x - cx) / (rx - 5)) ** 2 + ((y - cy) / (ry - 4)) ** 2
            if q <= 1:
                if qi <= 1:
                    n = smooth(x, y, 21, 5.0)
                    c = (90, 190, 220) if n < 0.5 else (130, 214, 236)
                    if (x + y * 2) % 17 == 0: c = (220, 250, 255)
                    P(im, x, y, A(c))
                else:
                    c = MARBLE[3] if y < cy - 4 else MARBLE[2]
                    if qi <= 1.18 and y > cy: c = MARBLE[1]
                    if qi > 1.25 and q > 0.9 and y > cy: c = MARBLE[1]
                    P(im, x, y, A(c))
    for y in range(cy + ry - 2, cy + ry + 6):
        for x in range(96):
            if ((x - cx) / rx) ** 2 <= 1 - 0.0 and y < 80:
                q = ((x - cx) / rx) ** 2 + ((y - cy - 4) / ry) ** 2
                if q <= 1 and ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 > 1: P(im, x, y, A(MARBLE[1] if y > cy + ry + 2 else MARBLE[2]))
    for k in range(-30, 31, 6):                      # rainbow light thrown across the water
        cols = [(255, 120, 120), (255, 210, 110), (140, 240, 140), (120, 200, 255), (200, 140, 255)]
        c = cols[(k // 6) % 5]
        for t in range(0, 22):
            blend(im, int(cx + k + t * 0.6 * (1 if k > 0 else -1)), int(cy + 4 + t * 0.45), c, 0.32)
    # the plinth and prism
    R(im, cx - 6, cy - 4, cx + 5, cy + 6, A(MARBLE[3])); H(im, cx - 6, cx + 5, cy - 4, A(MARBLE[4])); Vl(im, cx + 5, cy - 4, cy + 6, A(MARBLE[1]))
    pts = [(cx, 2), (cx - 7, cy - 4), (cx + 6, cy - 4)]
    d = ImageDraw.Draw(im)
    d.polygon(pts, fill=A((200, 236, 248)))
    d.polygon([(cx, 2), (cx - 7, cy - 4), (cx - 1, cy - 4)], fill=A((236, 250, 255)))
    d.line([(cx, 2), (cx - 1, cy - 4)], fill=A((255, 255, 255)))
    for t in range(4, cy - 6, 3):
        blend(im, cx + 2, t, (255, 160, 200), 0.35); blend(im, cx - 3, t + 1, (160, 220, 255), 0.4)
    glow(im, cx, 10, 12, (220, 246, 255), 0.4)
    for sx, sy in ((cx - 20, cy - 8), (cx + 18, cy - 6), (cx - 28, cy + 6), (cx + 26, cy + 8)):   # jets
        Vl(im, sx, sy - 7, sy, A((210, 244, 255))); P(im, sx - 1, sy - 6, A((240, 252, 255))); P(im, sx + 1, sy - 5, A((240, 252, 255)))
    return im


def tram():
    im = new(5, 2)
    R(im, 1, 6, 78, 27, A(CREAM[3])); R(im, 1, 18, 78, 27, A(TEALC[2])); H(im, 1, 78, 18, A(BRASS[3]))
    H(im, 1, 78, 6, A(CREAM[4])); R(im, 3, 2, 76, 6, A(TEALC[1])); H(im, 3, 76, 2, A(TEALC[3]))
    for x in range(6, 74, 9):
        R(im, x, 9, x + 6, 15, A(BRASS[1])); R(im, x + 1, 10, x + 5, 14, A(LITW[2])); P(im, x + 1, 10, A(LITW[3]))
    R(im, 0, 8, 2, 26, A(BRASS[2])); R(im, 77, 8, 79, 26, A(BRASS[1]))
    for x in (12, 64): disc(im, x, 28, 3.2, A(IRN[1])); disc(im, x, 28, 1.6, A(IRN[3]))
    Vl(im, 40, 0, 2, A(IRN[2])); H(im, 34, 46, 0, A(IRN[3]))
    R(im, 28, 21, 50, 25, A(TEALC[1]))
    for x in range(30, 49, 3): R(im, x, 22, x + 1, 24, A(BRASS[3]))
    H(im, 1, 78, 31, (20, 16, 24, 90))
    return im


def shelter():
    im = new(3, 2)
    for x in (2, 45): R(im, x, 4, x + 1, 31, A(BRASS[1])); Vl(im, x, 4, 31, A(BRASS[3]))
    R(im, 0, 0, 47, 7, A(GLS[2])); H(im, 0, 47, 0, A(BRASS[3])); H(im, 0, 47, 7, A(BRASS[1]))
    for x in range(0, 48, 8): Vl(im, x, 0, 7, A(BRASS[2]))
    for y in range(8, 22):
        for x in range(4, 45): blend(im, x, y, GLS[3], 0.28)
    R(im, 6, 22, 41, 25, A(WOODL[3])); H(im, 6, 41, 22, A(WOODL[4]))
    R(im, 18, 10, 30, 17, A(CREAM[4])); H(im, 19, 29, 12, A(TEALC[2])); H(im, 19, 26, 14, A(IRN[2]))
    return im


def mast():
    im = new(2, 5)
    for y in range(4, 76):
        w_ = 2 + int((y / 76.0) * 8)
        P(im, 16 - w_, y, A(IRN[2])); P(im, 15 + w_, y, A(IRN[1]))
        if y % 8 == 0:
            for x in range(16 - w_, 16 + w_): P(im, x, y, A(IRN[3]))
            for t in range(w_ * 2):
                P(im, 16 - w_ + t, y + int(t * 8 / max(1, w_ * 2)), A(IRN[2]))
    R(im, 12, 0, 19, 4, A(BRASS[2])); H(im, 12, 19, 0, A(BRASS[3])); disc(im, 15.5, 1, 1.5, A((255, 80, 60)))
    R(im, 4, 74, 27, 79, A(MARBLE[2])); H(im, 4, 27, 74, A(MARBLE[4]))
    for k in range(3):
        H(im, 19, 31, 8 + k * 2, A((200, 60, 60) if k % 2 == 0 else (240, 230, 220)))
    return im


def airship():
    im = new(6, 3)
    cx, cy = 50, 16
    for y in range(48):
        for x in range(96):
            q = ((x - cx) / 44.0) ** 2 + ((y - cy) / 13.0) ** 2
            if q <= 1:
                t = (y - cy + 13) / 26.0
                c = CREAM[4] if t < 0.3 else CREAM[3] if t < 0.6 else CREAM[1]
                if (x - 8) % 12 == 0 and q < 0.95: c = BRASS[2]
                if q > 0.9: c = CREAM[0] if y > cy else CREAM[2]
                P(im, x, y, A(c))
    d = ImageDraw.Draw(im)
    d.polygon([(4, 6), (12, 14), (4, 24)], fill=A(TEALC[2]), outline=A(TEALC[0]))
    R(im, 34, 30, 66, 37, A(WOODL[2])); H(im, 34, 66, 30, A(BRASS[3])); H(im, 34, 66, 37, A(WOODL[0]))
    for x in range(37, 64, 5): R(im, x, 32, x + 2, 34, A(LITW[2]))
    for x in (38, 62): Vl(im, x, 26, 30, A(IRN[2]))
    H(im, 40, 60, 20, A((200, 60, 60))); H(im, 40, 60, 21, A((240, 230, 220)))
    for y in range(40, 48):
        for x in range(30, 70): blend(im, x, y, (20, 20, 40), 0.12)
    return im


def pylon(lit=True):
    """a Meridian Extraction Lattice pylon: steel lattice, brass coils, a glow of drawn power"""
    im = new(2, 4)
    for y in range(6, 60):
        w_ = 3 + int((y / 60.0) * 9)
        P(im, 16 - w_, y, A(IRN[3])); P(im, 15 + w_, y, A(IRN[1]))
        if y % 6 == 0:
            for x in range(16 - w_, 16 + w_): P(im, x, y, A(IRN[2]))
            for t in range(w_ * 2): P(im, 16 - w_ + t, y + int(t * 6 / max(1, w_ * 2)), A(IRN[2]))
    for k, y in enumerate((10, 22, 34)):
        R(im, 11, y, 20, y + 5, A(BRASS[2])); H(im, 11, 20, y, A(BRASS[3]))
        for x in range(12, 20, 2): Vl(im, x, y + 1, y + 4, A(BRASS[1]))
    R(im, 4, 58, 27, 63, A(MARBLE[1])); H(im, 4, 27, 58, A(MARBLE[3]))
    disc(im, 15.5, 4, 3.4, A(BRASS[1])); disc(im, 15.5, 4, 2.4, A(CYAN[2] if lit else IRN[3]))
    if lit:
        glow(im, 15.5, 4, 10, CYAN[2], 0.45)
        for k in range(5): P(im, 13 + k, 12 + k * 6, A(CYAN[3]))
    R(im, 22, 50, 27, 56, A((230, 200, 60))); P(im, 24, 52, A(IRN[0])); P(im, 24, 54, A(IRN[0]))
    return im


def lift():
    """a lift cage down to Nadir: iron lattice, a brass car, the grimy glow from below"""
    im = new(2, 3)
    R(im, 1, 4, 30, 47, A(IRN[0]))
    for y in range(8, 47):
        for x in range(2, 30): blend(im, x, y, (255, 140, 60), 0.10 + 0.25 * (y / 47.0))
    R(im, 6, 18, 25, 44, A(BRASS[1])); R(im, 8, 20, 23, 34, A(LITW[1])); H(im, 6, 25, 18, A(BRASS[3]))
    for x in range(1, 31, 3): Vl(im, x, 4, 47, A(IRN[2]))
    for y in range(4, 48, 6): H(im, 1, 30, y, A(IRN[3]))
    R(im, 0, 0, 31, 5, A(IRN[2])); H(im, 0, 31, 0, A(IRN[4])); R(im, 10, 1, 21, 4, A((230, 200, 60)))
    for x in range(11, 21, 3): P(im, x, 2, A(IRN[0]))
    return im


def steam(v=0):
    im = new(1, 2)
    r = random.Random(v)
    for k in range(5):
        cx, cy = 8 + r.uniform(-3, 3), 26 - k * 5
        disc(im, cx, cy, 3 + k * 0.6, (236, 236, 244, 110 - k * 14))
    return im


def vent():
    im = new()
    R(im, 2, 6, 13, 14, A(IRN[2])); H(im, 2, 13, 6, A(IRN[4]))
    for y in range(8, 14, 2): H(im, 3, 12, y, A(IRN[0]))
    H(im, 1, 14, 15, (20, 16, 24, 90))
    return im


def bulbs(v=0):
    im = new()
    for x in range(16): P(im, x, 6 + int(1.5 * math.sin((x + v * 8) / 16.0 * math.pi)), A((70, 60, 60)))
    for k, x in enumerate((3, 11)):
        y = 7 + int(1.5 * math.sin((x + v * 8) / 16.0 * math.pi))
        c = [AMBER[2], CYAN[2], MAGENTA[2]][(k + v) % 3]
        disc(im, x, y + 1, 1.6, A(c)); glow(im, x, y + 1, 4, c, 0.35)
    return im


def poster(v):
    im = new()
    R(im, 2, 1, 13, 14, A((236, 230, 214))); H(im, 2, 13, 1, A((250, 248, 240))); Vl(im, 13, 1, 14, A((180, 170, 150)))
    if v == 0:                                       # "Light for Everyone - Ten Years"
        R(im, 3, 2, 12, 9, A(BLUEC[1])); disc(im, 7.5, 6, 2.5, A(BRASS[3]))
        for k in range(8):
            a = k * math.pi / 4; P(im, int(7.5 + 4 * math.cos(a)), int(6 + 3.5 * math.sin(a)), A(BRASS[2]))
        H(im, 4, 11, 11, A(BLUEC[2])); H(im, 5, 10, 13, A(BRASS[1]))
    elif v == 1:                                     # Rook's stream
        R(im, 3, 2, 12, 13, A((30, 20, 40))); disc(im, 7.5, 6, 2.5, A((230, 120, 60)))
        H(im, 4, 11, 10, A(CYAN[2])); H(im, 4, 9, 12, A(MAGENTA[2]))
    else:                                            # the gala
        R(im, 3, 2, 12, 13, A(WINE[1])); H(im, 4, 11, 4, A(BRASS[3])); Vl(im, 7, 6, 11, A((240, 236, 220))); Vl(im, 8, 6, 11, A((240, 236, 220)))
        H(im, 4, 11, 12, A(BRASS[2]))
    return im


def wallbanner(col):
    im = new(1, 2)
    H(im, 2, 13, 1, A(BRASS[3])); R(im, 3, 2, 12, 27, A(col[1])); Vl(im, 3, 2, 27, A(col[2])); Vl(im, 12, 2, 27, A(col[0]))
    for x in range(3, 13):
        if x % 3 != 1: P(im, x, 28, A(col[1]))
    disc(im, 7.5, 10, 3, A(BRASS[3])); disc(im, 7.5, 10, 1.6, A(col[1]))
    for k in range(8):
        a = k * math.pi / 4; P(im, int(7.5 + 4.5 * math.cos(a)), int(10 + 4.5 * math.sin(a)), A(BRASS[2]))
    H(im, 5, 10, 18, A((240, 236, 220))); H(im, 5, 10, 21, A((240, 236, 220))); H(im, 6, 9, 24, A(BRASS[2]))
    return im


def stall(cols, goods, seed=0):
    im = new(3, 2)
    R(im, 2, 16, 45, 28, A(WOODL[2])); H(im, 2, 45, 16, A(WOODL[4])); H(im, 2, 45, 28, A(WOODL[0]))
    r = random.Random(seed)
    for x in range(4, 44):
        if r.random() < 0.8: P(im, x, 17, A(r.choice(GOODS[goods])))
        if r.random() < 0.6: P(im, x, 18, A(r.choice(GOODS[goods])))
    for x in (3, 44): Vl(im, x, 6, 30, A(WOODL[1]))
    for yy in range(0, 9):
        for x in range(0, 48):
            c = cols[0] if (x // 6) % 2 == 0 else cols[1]
            P(im, x, yy + 2, A(c))
    H(im, 0, 47, 2, A(tuple(min(255, v + 30) for v in cols[0])))
    for x in range(48):
        if x % 6 not in (0, 5): P(im, x, 11, A(tuple(int(v * 0.7) for v in (cols[0] if (x // 6) % 2 == 0 else cols[1]))))
    H(im, 2, 45, 31, (20, 16, 24, 80))
    return im


def junk(v):
    im = new(); r = random.Random(v)
    if v == 0:                                       # crate stack
        bev(im, 2, 6, 13, 15, WOODL, 2); H(im, 3, 12, 10, A(WOODL[1])); bev(im, 4, 1, 11, 6, WOODL, 3)
    elif v == 1:                                     # brazier
        R(im, 4, 8, 11, 14, A(IRN[1])); H(im, 4, 11, 8, A(IRN[3]))
        for x in range(5, 11): P(im, x, 7, A(AMBER[r.randrange(1, 4)])); P(im, x, 6 - (x % 2), A(AMBER[2]))
        glow(im, 7.5, 6, 7, AMBER[1], 0.4)
    elif v == 2:                                     # pipe junction
        R(im, 0, 7, 15, 10, A(IRN[2])); H(im, 0, 15, 7, A(IRN[4])); R(im, 6, 4, 10, 14, A(BRASS[1])); H(im, 6, 10, 4, A(BRASS[3]))
        disc(im, 8, 8, 2, A((200, 50, 40)))
    else:                                            # barrels
        for bx in (2, 8):
            R(im, bx, 5, bx + 5, 14, A(WOODL[2])); H(im, bx, bx + 5, 7, A(IRN[2])); H(im, bx, bx + 5, 12, A(IRN[2])); Vl(im, bx, 5, 14, A(WOODL[3]))
    return im


def fixed(v):
    """the Fixed: a Lowlight neighbour caught in glass mid-motion (1x2)"""
    im = new(1, 2)
    d = ImageDraw.Draw(im)
    body = {0: [(5, 8), (10, 8), (11, 20), (12, 30), (3, 30), (4, 20)],                 # woman hanging laundry, arms up
            1: [(5, 9), (10, 9), (12, 20), (11, 30), (4, 30), (3, 20)],                 # a man mid-laugh, leaning back
            2: [(6, 12), (10, 12), (11, 22), (10, 30), (5, 30), (5, 22)],               # Dex mid-wave, soda crate on his hip
            3: [(4, 14), (11, 14), (12, 24), (11, 30), (4, 30), (3, 24)]}[v]
    d.polygon(body, fill=A(CRYST[1]), outline=A(CRYST[0]))
    hy = {0: 5, 1: 6, 2: 9, 3: 11}[v]
    disc(im, 7.5 + (1 if v == 1 else 0), hy, 2.8 if v != 2 else 2.4, A(CRYST[2]))
    if v == 0:
        d.line([(5, 10), (2, 2)], fill=A(CRYST[2])); d.line([(10, 10), (13, 2)], fill=A(CRYST[2]))
        H(im, 0, 15, 1, A(CRYST[3])); R(im, 3, 2, 12, 5, A(CRYST[3]))
    if v == 1:
        d.line([(10, 11), (14, 8)], fill=A(CRYST[2])); d.line([(5, 11), (2, 16)], fill=A(CRYST[2]))
    if v == 2:
        d.line([(10, 14), (14, 5)], fill=A(CRYST[2])); P(im, 14, 4, A(CRYST[4]))
        R(im, 1, 20, 5, 25, A(CRYST[3])); H(im, 1, 5, 20, A(CRYST[4]))
    for k in range(6):
        x, y = 4 + (k * 5) % 8, 10 + (k * 7) % 18
        P(im, x, y, A(CRYST[4])); P(im, x + 1, y + 1, A(CRYST[3]))
    for y in range(31):
        for x in range(16):
            if im.getpixel((x, y))[3] and (x + y) % 5 == 0: blend(im, x, y, (255, 255, 255), 0.35)
    H(im, 3, 12, 31, A((120, 100, 170)))
    return im


def bleed_decal(v):
    im = new(); r = random.Random(90 + v)
    for k in range(3 + v):
        x, y = r.randrange(2, 14), r.randrange(2, 14)
        for t in range(r.randrange(3, 7)):
            P(im, x, y, A(CRYST[2] if t % 2 else CRYST[3])); blend(im, x + 1, y, CRYST[1], 0.4)
            x += r.choice((-1, 1)); y += r.choice((-1, 0, 1))
    for k in range(2):
        x, y = r.randrange(3, 13), r.randrange(3, 13)
        P(im, x, y, A(CRYST[4])); P(im, x, y - 1, A(CRYST[3])); P(im, x - 1, y, A(CRYST[2]))
    return im


def drone():
    """Rook's Rotom camera drone (a tile for events): orange plasma body, a lens, two rotors"""
    im = new()
    disc(im, 8, 9, 4.2, A((200, 90, 40))); disc(im, 8, 9, 3.4, A((246, 140, 60))); P(im, 6, 7, A((255, 220, 160)))
    disc(im, 8.5, 9.5, 1.8, A((30, 40, 60))); P(im, 8, 9, A((140, 220, 255)))
    H(im, 1, 5, 4, A(IRN[3])); H(im, 11, 15, 4, A(IRN[3])); Vl(im, 3, 4, 6, A(IRN[2])); Vl(im, 13, 4, 6, A(IRN[2]))
    P(im, 5, 13, A((255, 200, 120))); P(im, 11, 13, A((255, 200, 120)))
    H(im, 5, 11, 15, (20, 16, 24, 60))
    return im


# ================================================================== interior wall kits (Cave machinery: rkit KITS cvZ / cvY / cvQ)
def wall_px(p, x, y):
    """one column of the 48-px wall (lip 0-15, face 16-31, base 32-47)"""
    if p == 'Z':                                     # the Circuit Gym: black glass, neon cyan at the cornice, magenta low
        if y <= 1: return IRN[3] if y == 0 else IRN[1]
        if y == 2: return CYAN[2]
        if y == 3: return CYAN[0]
        if y >= 44: return (14, 14, 22)
        if y >= 38: return IRN[3] if y == 38 else IRN[2] if y < 42 else IRN[1]
        if y == 33: return MAGENTA[2]
        if y == 34: return MAGENTA[0]
        if x % 8 == 0: return IRN[2]
        t = (x * 0.7 + y * 0.9) % 19
        if t < 1.2: return (64, 76, 100)
        return (22, 24, 34) if (x // 8) % 2 else (28, 30, 42)
    if p == 'Y':                                     # Lumen civic: cream marble panels, brass pilasters, walnut wainscot
        if y <= 3:
            if y == 0: return CREAM[4]
            if y == 1: return BRASS[3]
            return CREAM[3] if (x % 3 or y == 3) else CREAM[1]
        if y >= 46: return (40, 32, 30)
        if y >= 42: return MARBLE[3] if y == 42 else MARBLE[2]
        if y in (30, 31): return BRASS[3] if y == 30 else BRASS[1]
        if y >= 32:
            if x % 8 == 0: return WOODL[0]
            return WOODL[2] if y in (33, 40) else WOODL[1]
        if x % 16 in (0, 1, 2):
            return [MARBLE[4], MARBLE[3], MARBLE[1]][x % 16]
        if y in (6, 27) and 4 <= x % 16 <= 14: return CREAM[1]
        if x % 16 in (4, 14) and 6 <= y <= 27: return CREAM[1]
        return CREAM[3] if (smooth(x, y, 17, 4.0) > 0.45) else CREAM[2]
    if p == 'Q':                                     # the vault: riveted steel plates, a hazard band
        if y <= 1: return IRN[4] if y == 0 else IRN[2]
        if y >= 44: return (14, 14, 22)
        if y >= 37:
            return (230, 196, 40) if ((x + y) // 3) % 2 == 0 else (30, 30, 36)
        if y % 12 == 2 or x % 16 == 0: return IRN[1]
        if (y % 12 == 4 or y % 12 == 10) and x % 16 in (3, 12): return IRN[4]
        return IRN[3] if (x % 16) < 2 else IRN[2]
    raise KeyError(p)


def wall_kit(p):
    out = {}
    full = Image.new('RGBA', (16, 48), CLEAR); alt = Image.new('RGBA', (16, 48), CLEAR)
    for y in range(48):
        for x in range(16):
            full.putpixel((x, y), A(wall_px(p, x, y))); alt.putpixel((x, y), A(wall_px(p, x + 8, y)))
    for k, nm in enumerate(('lip', 'face', 'base')):
        for end in 'wme':
            im = full.crop((0, k * 16, 16, k * 16 + 16)).copy()
            if end == 'w':
                for y in range(16): P(im, 0, y, A(VOIDC[1])); P(im, 1, y, (0, 0, 0, 110))
            if end == 'e':
                for y in range(16): P(im, 15, y, A(VOIDC[1])); P(im, 14, y, (0, 0, 0, 90))
            out['%s_%s%s' % (p, nm, end)] = (im, ['W'], None)
        out['%s_%sm1' % (p, nm)] = (alt.crop((0, k * 16, 16, k * 16 + 16)), ['W'], None)
    out['%s_facem2' % p] = (full.crop((0, 32, 16, 48)), ['W'], None)
    out['%s_lipm2' % p] = (alt.crop((0, 0, 16, 16)), ['W'], None)
    cap = {'Z': [IRN[0], IRN[1], IRN[2], CYAN[1], CYAN[2]], 'Y': [WOODL[0], WOODL[1], CREAM[2], CREAM[3], CREAM[4]],
           'Q': [IRN[0], IRN[1], IRN[2], IRN[3], IRN[4]]}[p]
    for end in 'wme':
        im = Image.new('RGBA', (16, 16), A(VOIDC[1]))
        for x in range(16):
            if end == 'w' and x < 3 or end == 'e' and x > 12: continue
            P(im, x, 0, A(cap[4])); P(im, x, 1, A(cap[2])); P(im, x, 2, A(cap[1])); P(im, x, 3, A(VOIDC[0]))
        out['%s_N%s' % (p, end)] = (im, ['W'], None)
    for side in 'WE':
        im = Image.new('RGBA', (16, 16), A(VOIDC[1]))
        xs = (0, 1, 2, 3) if side == 'W' else (15, 14, 13, 12)
        cols = [cap[4], cap[2], cap[1], VOIDC[0]]
        for y in range(16):
            for k, xx in enumerate(xs): P(im, xx, y, A(cols[k]))
        out['%s_%s' % (p, side)] = (im, ['W'], None)
        for k in (0, 1): out['%s_in%s%d' % (p, side, k)] = (im.copy(), ['W'], None)
    for t in range(4):
        for v, s in enumerate('ab'):
            im = Image.new('RGBA', (16, 16), A(VOIDC[min(3, 3 - t)] if False else VOIDC[max(0, 2 - t // 2)]))
            for y in range(16):
                for x in range(16):
                    if nz(x, y, 31 + v + t + ord(p)) > 0.94: P(im, x, y, A(VOIDC[3]))
            out['%s_m%d%s' % (p, t, s)] = (im, ['M'], None)
    im = Image.new('RGBA', (16, 16), CLEAR)
    for y in range(5):
        for x in range(16): P(im, x, y, (8, 6, 14, 120 - y * 24))
    out['%s_shadow' % p] = (im, ['V'], None)
    out['%s_mP' % p] = (Image.new('RGBA', (16, 16), A(VOIDC[1])), ['G'], None)
    return out


def floor(p, v):
    im = new()
    if p == 'Z':                                     # dark studio tiles, cyan traces in some
        for y in range(16):
            for x in range(16):
                c = (34, 36, 50) if ((x // 8) + (y // 8)) % 2 else (40, 42, 58)
                if x % 8 == 0 or y % 8 == 0: c = (24, 26, 36)
                if x % 8 == 1 and y % 8 != 0: c = (50, 54, 72) if c != (24, 26, 36) else c
                P(im, x, y, A(c))
        if v == 3:
            r = random.Random(v)
            x, y = r.randrange(2, 6), 3
            for k in range(14):
                P(im, x, y, A((40, 110, 140))); x += 1
                if k == 6: 
                    for t in range(6): P(im, x, y + t, A((40, 110, 140)))
                    y += 6
            P(im, x, y, A(CYAN[2]))
        if v == 2:
            for x, y in ((3, 3), (12, 11)): P(im, x, y, A((60, 66, 86)))
    elif p == 'Y':                                   # polished marble checker, brass studs
        for y in range(16):
            for x in range(16):
                dark = ((x // 8) + (y // 8)) % 2
                c = (64, 112, 116) if dark else MARBLE[3]
                if dark and (x + y) % 11 == 0: c = (90, 140, 140)
                if not dark and smooth(x, y, 30 + v, 4.0) > 0.7: c = MARBLE[4]
                P(im, x, y, A(c))
        for x, y in ((0, 0), (8, 8), (0, 8), (8, 0)): P(im, x, y, A(BRASS[3]))
        if v == 3:
            H(im, 0, 15, 7, A(BRASS[2])); H(im, 0, 15, 8, A(BRASS[1]))
    elif p == 'Q':                                   # steel tread plate
        R(im, 0, 0, 15, 15, A(IRN[2]))
        for y in range(1, 16, 4):
            for x in range((y // 4) % 2 * 2, 16, 4):
                P(im, x, y, A(IRN[4])); P(im, x + 1, y + 1, A(IRN[1]))
        if v == 1: H(im, 0, 15, 15, A(IRN[1]))
        if v == 2: Vl(im, 15, 0, 15, A(IRN[1]))
    return im


def carpet(part, ramp=WINE, border=BRASS):
    im = new()
    R(im, 0, 0, 15, 15, A(ramp[1]))
    for y in range(16):
        for x in range(16):
            if (x + y) % 6 == 0 and part == 'c': P(im, x, y, A(ramp[2]))
    n = 'n' in part; s = 's' in part[-1:] and part != 'c'; w = part.endswith('w') or part == 'w'; e = part.endswith('e') or part == 'e'
    s = part in ('s', 'sw', 'se'); n = part in ('n', 'nw', 'ne')
    if n: H(im, 0, 15, 0, A(ramp[0])); H(im, 0, 15, 2, A(border[3])); H(im, 0, 15, 3, A(border[1]))
    if s: H(im, 0, 15, 15, A(ramp[0])); H(im, 0, 15, 13, A(border[3])); H(im, 0, 15, 12, A(border[1]))
    if w: Vl(im, 0, 0, 15, A(ramp[0])); Vl(im, 2, 0, 15, A(border[3])); Vl(im, 3, 0, 15, A(border[1]))
    if e: Vl(im, 15, 0, 15, A(ramp[0])); Vl(im, 13, 0, 15, A(border[3])); Vl(im, 12, 0, 15, A(border[1]))
    return im


# ================================================================== Gym 4 devices
PORTS = {'I': 1 | 4, 'L': 1 | 2, 'T': 1 | 2 | 4}


def rotm(m, k):
    for _ in range(k): m = ((m << 1) & 15) | (m >> 3)
    return m


def node(shape, rot):
    """a rotatable conduit node: a dark plate, a brass hub, conduit stubs to its ports (N1 E2 S4 W8)"""
    im = floor('Z', 0)
    bev(im, 1, 1, 14, 14, IRN, 2)
    m = rotm(PORTS[shape], rot)
    for bit, (x0, y0, x1, y1) in ((1, (6, 0, 9, 7)), (2, (8, 6, 15, 9)), (4, (6, 8, 9, 15)), (8, (0, 6, 7, 9))):
        if m & bit:
            R(im, x0, y0, x1, y1, A(BRASS[2]))
            if bit in (1, 4): Vl(im, 7, y0, y1, A(CYAN[1])); Vl(im, 8, y0, y1, A(CYAN[1])); Vl(im, x0, y0, y1, A(BRASS[3])); Vl(im, x1, y0, y1, A(BRASS[0]))
            else: H(im, x0, x1, 7, A(CYAN[1])); H(im, x0, x1, 8, A(CYAN[1])); H(im, x0, x1, y0, A(BRASS[3])); H(im, x0, x1, y1, A(BRASS[0]))
    disc(im, 7.5, 7.5, 3.6, A(BRASS[1])); disc(im, 7.5, 7.5, 2.8, A(BRASS[3])); disc(im, 7.5, 7.5, 1.6, A(CYAN[1]))
    P(im, 6, 6, A(BRASS[4]))
    for x, y in ((2, 2), (13, 2), (2, 13), (13, 13)): P(im, x, y, A(IRN[4]))
    return im


def strip(kind, on):
    im = floor('Z', 0)
    if kind == 'h':
        R(im, 0, 5, 15, 10, A(IRN[0])); H(im, 0, 15, 5, A(BRASS[1])); H(im, 0, 15, 10, A(BRASS[3]))
        R(im, 0, 7, 15, 8, A(CYAN[2] if on else (50, 60, 76)))
        if on:
            for x in range(16): blend(im, x, 6, CYAN[2], 0.5); blend(im, x, 9, CYAN[2], 0.5); blend(im, x, 4, CYAN[2], 0.2); blend(im, x, 11, CYAN[2], 0.2)
            for x in range(1, 16, 5): P(im, x, 7, A(CYAN[3]))
    else:
        R(im, 5, 0, 10, 15, A(IRN[0])); Vl(im, 5, 0, 15, A(BRASS[1])); Vl(im, 10, 0, 15, A(BRASS[3]))
        R(im, 7, 0, 8, 15, A(CYAN[2] if on else (50, 60, 76)))
        if on:
            for y in range(16): blend(im, 6, y, CYAN[2], 0.5); blend(im, 9, y, CYAN[2], 0.5); blend(im, 4, y, CYAN[2], 0.2); blend(im, 11, y, CYAN[2], 0.2)
            for y in range(1, 16, 5): P(im, 7, y, A(CYAN[3]))
    return im


def generator():
    im = new(2, 2)
    R(im, 2, 6, 29, 31, A(IRN[1])); bev(im, 2, 6, 29, 31, IRN, 1)
    for k, x in enumerate((6, 14, 22)):
        R(im, x, 2, x + 5, 20, A(BRASS[2])); H(im, x, x + 5, 2, A(BRASS[4]))
        for y in range(4, 20, 2): H(im, x, x + 5, y, A(BRASS[1]))
        disc(im, x + 2.5, 1, 2, A(CYAN[2])); glow(im, x + 2.5, 1, 5, CYAN[2], 0.4)
    R(im, 8, 23, 23, 29, A(IRN[0])); R(im, 10, 25, 13, 27, A((60, 220, 120))); R(im, 17, 25, 21, 27, A((230, 200, 60)))
    return im


def lamp(kind, on):
    im = floor('Z', 2)
    R(im, 4, 9, 11, 15, A(IRN[1])); H(im, 4, 11, 9, A(IRN[3]))
    if kind == 'door':
        disc(im, 7.5, 5.5, 4.2, A(BRASS[1])); disc(im, 7.5, 5.5, 3.3, A(CYAN[2] if on else (60, 70, 86)))
        if on: disc(im, 7.5, 5, 1.6, A(CYAN[3])); glow(im, 7.5, 5.5, 8, CYAN[2], 0.4)
    else:                                            # Rook's camera flash: the alarm
        R(im, 3, 2, 12, 8, A(IRN[0])); disc(im, 7.5, 5, 2.6, A((255, 255, 255) if on else (70, 70, 90)))
        R(im, 10, 1, 12, 2, A((230, 40, 40))); 
        if on: glow(im, 7.5, 5, 9, (255, 255, 255), 0.6)
    return im


def pdoor(open_):
    im = floor('Z', 0)
    if open_:
        R(im, 0, 0, 2, 15, A(IRN[2])); R(im, 13, 0, 15, 15, A(IRN[2])); H(im, 0, 15, 0, A(IRN[3]))
        Vl(im, 2, 0, 15, A(CYAN[1])); Vl(im, 13, 0, 15, A(CYAN[1]))
    else:
        R(im, 0, 0, 15, 15, A(IRN[2]))
        for y in range(2, 16, 3): H(im, 1, 14, y, A(IRN[3])); H(im, 1, 14, y + 1, A(IRN[1]))
        R(im, 6, 0, 9, 1, A((220, 40, 40))); glow(im, 7.5, 1, 5, (255, 60, 60), 0.4)
        Vl(im, 0, 0, 15, A(IRN[4])); Vl(im, 15, 0, 15, A(IRN[0]))
    return im


def latch_gate(open_):
    im = floor('Z', 0)
    R(im, 0, 0, 1, 15, A(BRASS[1])); R(im, 14, 0, 15, 15, A(BRASS[1]))
    if not open_:
        for x in range(3, 14, 3): Vl(im, x, 0, 15, A(BRASS[3])); Vl(im, x + 1, 0, 15, A(BRASS[0]))
        H(im, 0, 15, 4, A(BRASS[2])); H(im, 0, 15, 11, A(BRASS[2]))
        R(im, 6, 6, 9, 9, A(IRN[0])); disc(im, 7.5, 7.5, 1.4, A((230, 60, 60)))
    else:
        R(im, 6, 0, 9, 2, A(IRN[1])); P(im, 7, 1, A((60, 220, 120))); P(im, 8, 1, A((60, 220, 120)))
    return im


def socket(docked):
    im = floor('Z', 0)
    bev(im, 2, 6, 13, 15, IRN, 1); disc(im, 7.5, 9, 4.6, A(BRASS[1])); disc(im, 7.5, 9, 3.6, A(IRN[0]))
    if docked:
        d = drone(); im.alpha_composite(d.crop((0, 0, 16, 14)), (0, -2))
        glow(im, 7.5, 9, 8, CYAN[2], 0.35)
    else:
        for a in range(0, 360, 45): P(im, int(7.5 + 3 * math.cos(math.radians(a))), int(9 + 3 * math.sin(math.radians(a))), A(CYAN[0]))
    return im


def splice(on):
    im = floor('Z', 0)
    bev(im, 3, 2, 12, 14, IRN, 2)
    R(im, 5, 4, 10, 8, A(IRN[0])); P(im, 6, 5, A((60, 220, 120) if on else (90, 40, 40))); P(im, 9, 5, A((230, 200, 60)))
    Vl(im, 7, 9 if on else 10, 13, A(BRASS[3])); disc(im, 7.5, 9 if on else 13, 1.5, A((220, 50, 50)))
    if on: glow(im, 7.5, 7, 7, CYAN[2], 0.35)
    return im


def cradle(state):
    """the Zap Plate's cradle: 'cold' (empty, dust), 'plate' (the Plate in it), 'cracked'"""
    im = new(1, 2)
    R(im, 3, 18, 12, 31, A(MARBLE[2])); H(im, 3, 12, 18, A(MARBLE[4])); Vl(im, 12, 18, 31, A(MARBLE[1]))
    R(im, 1, 12, 14, 18, A(BRASS[2])); H(im, 1, 14, 12, A(BRASS[3])); H(im, 1, 14, 18, A(BRASS[0]))
    R(im, 3, 13, 12, 16, A(IRN[0]))
    if state in ('plate', 'cracked'):
        R(im, 3, 6, 12, 15, A((230, 196, 60))); H(im, 3, 12, 6, A((255, 236, 140))); Vl(im, 12, 6, 15, A((170, 130, 30)))
        disc(im, 7.5, 10.5, 2.4, A((255, 250, 210)))
        for k in range(3): P(im, 5 + k * 2, 8 + (k % 2), A((255, 255, 255)))
        if state == 'cracked':
            for t in range(9): P(im, 4 + t, 6 + (t * 7) % 9, A((90, 50, 140))); P(im, 5 + t, 6 + (t * 7) % 9, A((200, 160, 255)))
            glow(im, 7.5, 10, 9, (180, 120, 255), 0.45)
        else:
            glow(im, 7.5, 10, 8, (255, 236, 120), 0.35)
    else:
        for k in range(6): P(im, 4 + k, 14, A((150, 140, 130)))
    return im


def cable(kind):
    im = new()
    if kind == 'h': R(im, 0, 6, 15, 10, A((24, 22, 28))); H(im, 0, 15, 6, A((70, 66, 80))); H(im, 0, 15, 11, (10, 8, 14, 90))
    else: R(im, 6, 0, 10, 15, A((24, 22, 28))); Vl(im, 6, 0, 15, A((70, 66, 80))); Vl(im, 11, 0, 15, (10, 8, 14, 90))
    for k in range(0, 16, 6):
        if kind == 'h': Vl(im, k, 6, 10, A(BRASS[1]))
        else: H(im, 6, 10, k, A(BRASS[1]))
    return im


def studio(kind):
    if kind == 'cam':
        im = new(1, 2)
        for dx in (-4, 0, 4): ImageDraw.Draw(im).line([(7.5, 14), (7.5 + dx, 30)], fill=A(IRN[2]))
        R(im, 2, 4, 13, 12, A(IRN[1])); bev(im, 2, 4, 13, 12, IRN, 1); disc(im, 4, 8, 2.6, A((40, 50, 70))); P(im, 3, 7, A((160, 220, 255)))
        P(im, 12, 5, A((230, 40, 40)))
        return im
    if kind == 'ring':
        im = new(1, 2)
        Vl(im, 7, 14, 30, A(IRN[2])); H(im, 4, 11, 30, A(IRN[2]))
        for a in range(0, 360, 10):
            P(im, int(7.5 + 5.5 * math.cos(math.radians(a))), int(7 + 5.5 * math.sin(math.radians(a))), A((255, 250, 240)))
        glow(im, 7.5, 7, 8, (255, 250, 230), 0.25)
        return im
    if kind == 'monitors':
        im = new(2, 2)
        for k, (x0, y0) in enumerate(((1, 2), (16, 2), (1, 15), (16, 15))):
            R(im, x0, y0, x0 + 14, y0 + 11, A(IRN[0])); R(im, x0 + 1, y0 + 1, x0 + 13, y0 + 9, A([(40, 120, 180), (180, 60, 140), (60, 160, 120), (200, 140, 40)][k]))
            for t in range(3): H(im, x0 + 2, x0 + 4 + t * 3, y0 + 2 + t * 2, A((240, 240, 255)))
        return im
    if kind == 'rack':
        im = new(1, 2)
        R(im, 2, 2, 13, 31, A(IRN[0])); bev(im, 2, 2, 13, 31, IRN, 1)
        for y in range(5, 30, 3):
            H(im, 4, 11, y, A(IRN[2])); P(im, 5, y, A((60, 220, 120) if (y // 3) % 2 else (230, 200, 60))); P(im, 7, y, A(CYAN[2]))
        return im
    if kind == 'speaker':
        im = new(1, 2)
        R(im, 2, 4, 13, 31, A(IRN[0])); bev(im, 2, 4, 13, 31, IRN, 1)
        disc(im, 7.5, 11, 3.8, A(IRN[2])); disc(im, 7.5, 11, 1.6, A(IRN[0])); disc(im, 7.5, 23, 5.2, A(IRN[2])); disc(im, 7.5, 23, 2.4, A(IRN[0]))
        return im
    if kind == 'couch':
        im = new(2, 1)
        R(im, 1, 2, 30, 15, A(MAGENTA[0])); R(im, 1, 2, 30, 6, A(MAGENTA[1])); H(im, 1, 30, 2, A(MAGENTA[2]))
        R(im, 1, 2, 4, 15, A(MAGENTA[1])); R(im, 27, 2, 30, 15, A(MAGENTA[0]))
        disc(im, 9, 9, 2.5, A(CYAN[1])); H(im, 2, 29, 15, (10, 8, 14, 100))
        return im
    if kind == 'onair':
        im = new()
        R(im, 1, 4, 14, 11, A((60, 10, 14))); R(im, 2, 5, 13, 10, A((230, 40, 40)))
        for x in range(3, 13, 3): R(im, x, 6, x + 1, 9, A((255, 220, 210)))
        glow(im, 7.5, 7.5, 8, (255, 60, 60), 0.3)
        return im
    if kind == 'neonbolt':
        im = new(2, 2)
        d = ImageDraw.Draw(im)
        pts = [(18, 1), (8, 16), (15, 16), (10, 31), (24, 12), (17, 12), (23, 1)]
        d.polygon(pts, fill=A(CYAN[2]), outline=A(CYAN[3]))
        for x, y in pts: glow(im, x, y, 6, CYAN[2], 0.3)
        return im
    if kind == 'desk':
        im = new(2, 1)
        R(im, 1, 3, 30, 15, A(IRN[1])); H(im, 1, 30, 3, A(IRN[3]))
        for x in range(3, 29, 2):
            Vl(im, x, 5, 9, A(IRN[0])); P(im, x, 6 + (x * 3) % 4, A(BRASS[3]))
        R(im, 20, 10, 28, 13, A(CYAN[1]))
        return im
    if kind == 'cables':
        im = new()
        for k, c in enumerate(((30, 30, 40), (200, 60, 60), (40, 40, 60))):
            for x in range(16): P(im, x, 5 + k * 3 + int(1.6 * math.sin((x + k * 5) / 3.0)), A(c))
        return im
    if kind == 'gearbox':
        im = new()
        bev(im, 2, 5, 13, 15, IRN, 2); H(im, 2, 13, 9, A((230, 196, 40))); R(im, 5, 2, 10, 5, A(IRN[1]))
        return im
    raise KeyError(kind)


def gala(kind):
    if kind == 'chand':
        im = new(2, 2)
        Vl(im, 15, 0, 6, A(BRASS[2]))
        for y in range(6, 26):
            for x in range(4, 28):
                q = ((x - 15.5) / 11.5) ** 2 + ((y - 14) / 9.0) ** 2
                if q <= 1:
                    if (x + y) % 3 == 0: P(im, x, y, A((230, 246, 255)))
                    elif (x * 2 + y) % 5 == 0: P(im, x, y, A(BRASS[3]))
        for k in range(7): disc(im, 6 + k * 3.3, 20 + (k % 2) * 2, 1.2, A((255, 244, 200)))
        glow(im, 15.5, 16, 14, (255, 240, 200), 0.3)
        return im
    if kind == 'bar':
        im = new(3, 1)
        R(im, 0, 3, 47, 15, A(WOODL[1])); R(im, 0, 3, 47, 6, A(MARBLE[3])); H(im, 0, 47, 3, A(MARBLE[4])); H(im, 0, 47, 7, A(BRASS[2]))
        for x in range(4, 44, 6):
            R(im, x, 0, x + 1, 3, A((210, 230, 220))); P(im, x, 0, A((250, 240, 180)))
        return im
    if kind == 'table':
        im = new()
        disc(im, 7.5, 8, 6.8, A((236, 234, 226))); disc(im, 7.5, 7, 6.2, A((250, 248, 242)))
        R(im, 2, 9, 13, 14, A((228, 226, 218)))
        for x in range(2, 14, 3): Vl(im, x, 10, 14, A((210, 206, 196)))
        disc(im, 7.5, 6, 1.4, A((210, 230, 220))); P(im, 7, 4, A((250, 230, 150))); P(im, 4, 6, A(BRASS[3])); P(im, 11, 6, A(BRASS[3]))
        H(im, 2, 13, 15, (10, 8, 14, 90))
        return im
    if kind == 'window':
        im = new(1, 2)
        R(im, 1, 0, 14, 31, A(BRASS[1]))
        for y in range(1, 30):
            for x in range(2, 14):
                t = y / 30.0
                P(im, x, y, A((int(40 + 140 * t), int(60 + 130 * t), int(130 + 90 * t))))
        R(im, 4, 10, 11, 13, A(CREAM[3])); H(im, 5, 10, 14, A(WOODL[2]))
        Vl(im, 7, 1, 30, A(BRASS[2])); H(im, 2, 13, 16, A(BRASS[2]))
        P(im, 3, 3, A((255, 255, 255))); P(im, 11, 6, A((255, 255, 255)))
        return im
    if kind == 'core':
        """the Dark Stone in its glass shaft (3x4): black stone, black light"""
        im = new(3, 4)
        R(im, 4, 0, 43, 55, A((24, 22, 34)))
        for y in range(0, 56):
            for x in range(4, 44):
                t = (x - 4) / 40.0
                c = (36, 34, 50) if t < 0.2 else (28, 26, 40) if t < 0.7 else (18, 16, 26)
                if (x - 4) % 10 == 0: c = BRASS[1]
                P(im, x, y, A(c))
        disc(im, 24, 28, 9, A((10, 8, 16))); disc(im, 24, 28, 7, A((30, 14, 50)))
        for k in range(10):
            a = k * 0.63; P(im, int(24 + 6 * math.cos(a)), int(28 + 6 * math.sin(a)), A((150, 90, 230)))
        glow(im, 24, 28, 18, (110, 50, 190), 0.35)
        R(im, 0, 54, 47, 63, A(MARBLE[2])); H(im, 0, 47, 54, A(MARBLE[4])); H(im, 0, 47, 56, A(BRASS[2]))
        Vl(im, 4, 0, 54, A(BRASS[3])); Vl(im, 43, 0, 54, A(BRASS[0]))
        return im
    if kind == 'vault':
        im = new(3, 3)
        R(im, 0, 0, 47, 47, A(IRN[2]))
        disc(im, 24, 22, 21, A(IRN[1])); disc(im, 24, 22, 19, A(IRN[3])); disc(im, 24, 22, 16, A(IRN[2]))
        for a in range(0, 360, 30):
            P(im, int(24 + 18 * math.cos(math.radians(a))), int(22 + 18 * math.sin(math.radians(a))), A(BRASS[3]))
        disc(im, 24, 22, 6, A(BRASS[2])); disc(im, 24, 22, 4, A(BRASS[1]))
        for a in (0, 120, 240):
            for r in range(4, 12): P(im, int(24 + r * math.cos(math.radians(a))), int(22 + r * math.sin(math.radians(a))), A(BRASS[3]))
        return im
    if kind == 'case':
        im = new(2, 2)
        R(im, 1, 18, 30, 31, A(WOODL[1])); H(im, 1, 30, 18, A(BRASS[3]))
        R(im, 2, 2, 29, 18, A(GLS[2]))
        for y in range(3, 18):
            for x in range(3, 29): blend(im, x, y, GLS[4], 0.15)
        R(im, 8, 8, 23, 15, A(MARBLE[3])); disc(im, 15.5, 8, 4, A(CYAN[2])); glow(im, 15.5, 8, 9, CYAN[2], 0.4)
        Vl(im, 2, 2, 18, A(BRASS[2])); Vl(im, 29, 2, 18, A(BRASS[1])); H(im, 2, 29, 2, A(BRASS[3]))
        return im
    if kind == 'pillar':
        im = new(1, 3)
        R(im, 3, 4, 12, 43, A(MARBLE[3])); Vl(im, 3, 4, 43, A(MARBLE[4])); Vl(im, 12, 4, 43, A(MARBLE[1]))
        for x in range(5, 11, 2): Vl(im, x, 6, 41, A(MARBLE[2]))
        R(im, 1, 0, 14, 4, A(BRASS[2])); H(im, 1, 14, 0, A(BRASS[3])); R(im, 1, 43, 14, 47, A(MARBLE[2])); H(im, 1, 14, 43, A(MARBLE[4]))
        return im
    if kind == 'plant':
        im = new(1, 2)
        R(im, 4, 22, 11, 31, A(BRASS[2])); H(im, 4, 11, 22, A(BRASS[3]))
        for k in range(9):
            a = -math.pi / 2 + (k - 4) * 0.33
            for t in range(4, 15):
                P(im, int(7.5 + t * math.cos(a) * 0.7), int(22 + t * math.sin(a)), A(LEAFL[2 if t < 10 else 3]))
        return im
    raise KeyError(kind)


def desk_counter(part):
    """a reception counter (gate / Spire lobby): cream marble front, brass top rail; part l / m / r"""
    im = new()
    R(im, 0, 3, 15, 15, A(CREAM[2])); H(im, 0, 15, 3, A(MARBLE[4])); H(im, 0, 15, 4, A(BRASS[3])); H(im, 0, 15, 5, A(BRASS[1]))
    for x in range(2, 16, 8): R(im, x, 7, x + 4, 13, A(CREAM[1])); R(im, x + 1, 8, x + 3, 12, A(CREAM[3]))
    if part == 'l': Vl(im, 0, 3, 15, A(CREAM[4]))
    if part == 'r': Vl(im, 15, 3, 15, A(CREAM[0]))
    return im


def gate_bars(part):
    """the West Gate's brass security barrier (1x1, solid)"""
    im = new()
    for x in range(1, 16, 4): R(im, x, 2, x + 1, 15, A(BRASS[2])); P(im, x, 2, A(BRASS[4]))
    H(im, 0, 15, 5, A(BRASS[3])); H(im, 0, 15, 11, A(BRASS[1]))
    disc(im, 8, 8, 2, A(CYAN[2]) if part == 'm' else A(BRASS[3]))
    return im


# ================================================================== pieces
CODES = {'Z': (2, 15, 2)}                            # solid, drawn over the player (tall props seen from behind)


def pieces():
    import rdraw, ndraw, cdraw
    rdraw.CODE.update(ndraw.CODES); rdraw.CODE.update(cdraw.CODES); rdraw.CODE.update(CODES)
    out = {}
    for v in range(4):
        out['lm_pave%d' % v] = (pave(v), ['G'], None)
        out['lm_low%d' % v] = (setts(v, SOOT, seed=7, wet=(v == 3)), ['G'], None)
    for v in range(2):
        out['lm_road%d' % v] = (setts(v), ['G'], None)
        out['lm_plaza%d' % v] = (pave(v + 1, CREAM, seed=5), ['G'], None)
    for k in ('h', 'v', 'x'): out['lm_track_%s' % k] = (track(k), ['G'], None)
    for s in 'NSWE': out['lm_kerb%s' % s] = (kerb(s), ['G'], None)
    for k in ('h', 'v', 'x', 'ne', 'nw', 'se', 'sw'): out['lm_inlay_%s' % k] = (inlay(k), ['G'], None)
    out['lm_grate'] = (grate(True), ['G'], None)
    out['lm_grate_off'] = (grate(False), ['G'], None)
    out['lm_sun'] = (sunburst(), ['GGGGG'] * 5, None)
    for e in 'lmr': out['lm_stair_%s' % e] = (stair(e), ['D'], None)
    out.update(lmw_kit())
    for v in range(4): out['lm_void%d' % v] = (void(v), ['M'], None)
    for e in 'wme': out['lm_railing_%s' % e] = (railing(e), ['X'], None)
    # ---- buildings
    B = {}
    B['lb_t6a'] = bldg(6, [16, 16], 'verd', 'marble', seed=3, shop='books', awn='teal')
    B['lb_t6b'] = bldg(6, [16, 16], 'slate', 'cream', seed=13, shop='cakes', awn='wine', balcony=(0,))
    B['lb_t5a'] = bldg(5, [16, 16, 16], 'verd', 'marble', seed=5, lit=0.5, chim=1)
    B['lb_t5b'] = bldg(5, [16, 16], 'brass', 'cream', seed=15, shop='lamps', awn='gold', crest=False)
    B['lb_t7a'] = bldg(7, [16, 16, 16], 'slate', 'cream', seed=8, clock=True, balcony=(1,), chim=2)
    B['lb_t7b'] = bldg(7, [18, 16], 'flat', 'marble', seed=17, glass=(0,), shop='gears', awn='navy', neon=CYAN)
    B['lb_t8a'] = bldg(8, [18, 16, 16], 'flat', 'marble', seed=4, glass=(1,), neon=CYAN, shop='soda', awn='wine', aerial=True)
    B['lb_t8b'] = bldg(8, [16, 16, 16], 'verd', 'marble', seed=18, shop='flowers', awn='teal', balcony=(0, 2), lit=0.5)
    B['lb_t4a'] = bldg(4, [16, 16], 'verd', 'cream', seed=21, wins='arch', lit=0.6)
    B['lb_t4b'] = bldg(4, [16, 16, 16], 'slate', 'marble', seed=22, wins=['arch', 'round', 'arch'])
    B['lb_t9a'] = bldg(9, [18, 18, 16], 'flat', 'marble', seed=23, glass=(0, 1), shop='cloth', awn='navy', aerial=True)
    B['lb_t6c'] = bldg(6, [18, 18], 'flat', 'cream', seed=24, glass=(1,), neon=MAGENTA, shop='soda', awn='red')
    B['lb_t10a'] = bldg(10, [16, 16], 'verd', 'marble', seed=25, wide_door=True, clock=True, balcony=(0,), chim=2, lit=0.55)
    # the Lowlight: tenements in soot brick
    B['lb_l5a'] = bldg(5, [14, 14], 'flat', 'soot', seed=31, fire=True, laundry=True, graffiti=True, pipes=True, soot=0.8, iron_door=True, wins='rect', lit=0.3, boarded=0.15)
    B['lb_l5b'] = bldg(5, [14, 14, 14], 'flat', 'brick', seed=32, fire=True, pipes=True, soot=0.6, iron_door=True, wins='rect', lit=0.35, laundry=True)
    B['lb_l4a'] = bldg(4, [14, 14], 'iron', 'soot', seed=33, laundry=True, soot=0.9, iron_door=True, wins='rect', lit=0.25, boarded=0.3, dormers=False, crest=False)
    B['lb_l6a'] = bldg(6, [14, 14], 'flat', 'brick', seed=34, graffiti=True, pipes=True, soot=0.7, iron_door=True, wins='rect', lit=0.3, shop='junk', awn='soot')
    B['lb_l6b'] = bldg(6, [14, 14, 14], 'flat', 'soot', seed=35, fire=True, laundry=True, soot=0.9, iron_door=True, wins='rect', lit=0.4, boarded=0.1)
    B['lb_l3a'] = bldg(3, [14, 14], 'iron', 'brick', seed=36, soot=0.7, iron_door=True, wins='rect', lit=0.3, dormers=False, crest=False, pil=False)
    # civic
    B['lb_pc'] = bldg(10, [18, 16], 'terra', 'marble', seed=6, dome=True, plaque='ball', wide_door=True, board=(RED, 3), lit=0.7)
    B['lb_arcade'] = bldg(12, [18], 'vault', 'marble', seed=7, wide_door=True, shop='gears', awn='gold', board=(BLUEC, 4), lit=0.7)
    B['lb_gym'] = gym_front()
    B['lb_spire'] = spire()
    B['lb_gate'] = bldg(8, [20], 'verd', 'marble', seed=44, wide_door=True, clock=True, board=(IRN, 3), flag=BLUEC, lit=0.6)
    B['lb_lab'] = bldg(7, [16, 16], 'flat', 'marble', seed=45, glass=(0, 1), board=(TEALC, 2), dome=True)
    B['lb_cycle'] = bldg(6, [16], 'brass', 'cream', seed=46, shop='gears', awn='teal', board=(TEALC, 2), crest=False)
    B['lb_council'] = bldg(12, [20, 18], 'verd', 'marble', seed=47, wide_door=True, clock=True, dome=True, balcony=(0,), lit=0.6, chim=2)
    B['lb_apt'] = bldg(5, [16, 16, 16], 'flat', 'cream', seed=48, balcony=(0, 1, 2), lit=0.5)
    for n, (im, code, door) in B.items(): out[n] = (im, code, door)
    # ---- street furniture
    out['lm_arclamp'] = (arclamp(True), ['R', 'R', 'W'], None)
    out['lm_arclamp_num'] = (arclamp(True, num=1), ['R', 'R', 'W'], None)
    out['lm_arclamp_off'] = (arclamp(False, num=1), ['R', 'R', 'W'], None)
    out['lm_bannerlamp'] = (arclamp(True, banner=BLUEC), ['R', 'R', 'W'], None)
    out['lm_bannerlamp_w'] = (arclamp(True, banner=WINE), ['R', 'R', 'W'], None)
    out['lm_holo'] = (holo(), ['R', 'R', 'W'], None)
    out['lm_bench'] = (bench(), ['WW'], None)
    out['lm_bollard'] = (bollard(), ['W'], None)
    out['lm_planter'] = (planter(2), ['WW'], None)
    out['lm_planter3'] = (planter(3), ['WWW'], None)
    out['lm_topiary'] = (topiary(), ['R', 'W'], None)
    out['lm_tree'] = (street_tree(), ['RR', 'RR', 'WW'], None)
    out['lm_kiosk'] = (kiosk(), ['RRR', 'WWW'], None)
    out['lm_news'] = (news(), ['R', 'W'], None)
    out['lm_clock'] = (clockpost(), ['R', 'R', 'W'], None)
    out['lm_statue'] = (statue(), ['RR', 'RR', 'WW'], None)
    out['lm_fountain'] = (prism_fountain(), ['RRRRRR', 'WWWWWW', 'WWWWWW', 'WWWWWW', 'WWWWWW'], None)
    out['lm_tram'] = (tram(), ['RRRRR', 'WWWWW'], None)
    out['lm_shelter'] = (shelter(), ['RRR', 'WWW'], None)
    out['lm_mast'] = (mast(), ['RR', 'RR', 'RR', 'RR', 'WW'], None)
    out['lm_airship'] = (airship(), ['OOOOOO'] * 3, None)
    out['lm_pylon'] = (pylon(True), ['RR', 'RR', 'RR', 'WW'], None)
    out['lm_pylon_off'] = (pylon(False), ['RR', 'RR', 'RR', 'WW'], None)
    out['lm_lift'] = (lift(), ['RR', 'WW', 'WW'], None)
    for v in range(2): out['lm_steam%d' % v] = (steam(v), ['O', 'O'], None)
    out['lm_vent'] = (vent(), ['W'], None)
    for v in range(3): out['lm_bulbs%d' % v] = (bulbs(v), ['O'], None)
    for v in range(3): out['lm_poster%d' % v] = (poster(v), ['X'], None)
    out['lm_banner'] = (wallbanner(BLUEC), ['X', 'X'], None)
    out['lm_banner_w'] = (wallbanner(WINE), ['X', 'X'], None)
    out['lm_stall_a'] = (stall([(150, 60, 50), (210, 190, 150)], 'junk', 1), ['RRR', 'WWW'], None)
    out['lm_stall_b'] = (stall([(60, 90, 120), (190, 180, 150)], 'cloth', 2), ['RRR', 'WWW'], None)
    out['lm_stall_c'] = (stall([(90, 110, 60), (200, 190, 140)], 'soda', 3), ['RRR', 'WWW'], None)
    for v in range(4): out['lm_junk%d' % v] = (junk(v), ['W'], None)
    for v in range(4): out['lm_fixed%d' % v] = (fixed(v), ['Z', 'W'], None)
    for v in range(3): out['lm_bleed%d' % v] = (bleed_decal(v), ['V'], None)
    out['lm_drone'] = (drone(), ['X'], None)
    # ---- rooms
    for p in 'ZYQ':
        out.update(wall_kit(p))
        for v in range(4): out['%s_f%d' % (p, v)] = (floor(p, v), ['G'], None)
    for part in ('nw', 'n', 'ne', 'w', 'c', 'e', 'sw', 's', 'se'):
        out['lm_carpet_%s' % part] = (carpet(part), ['D'], None)
    for s in 'ILT':
        for r in range(2 if s == 'I' else 4): out['lm_node%s%d' % (s, r)] = (node(s, r), ['W'], None)
    for k in 'hv':
        out['lm_strip_%s' % k] = (strip(k, False), ['D'], None)
        out['lm_strip_%s_on' % k] = (strip(k, True), ['D'], None)
    out['lm_gen'] = (generator(), ['RR', 'WW'], None)
    out['lm_lamp'] = (lamp('door', False), ['W'], None)
    out['lm_lamp_on'] = (lamp('door', True), ['W'], None)
    out['lm_alarm'] = (lamp('alarm', False), ['W'], None)
    out['lm_alarm_on'] = (lamp('alarm', True), ['W'], None)
    out['lm_pdoor'] = (pdoor(False), ['W'], None)
    out['lm_pdoor_open'] = (pdoor(True), ['D'], None)
    out['lm_latch'] = (latch_gate(False), ['W'], None)
    out['lm_latch_open'] = (latch_gate(True), ['D'], None)
    out['lm_socket'] = (socket(False), ['W'], None)
    out['lm_socket_drone'] = (socket(True), ['W'], None)
    out['lm_splice'] = (splice(False), ['W'], None)
    out['lm_splice_on'] = (splice(True), ['W'], None)
    for s in ('cold', 'plate', 'cracked'): out['lm_cradle_%s' % s] = (cradle(s), ['Z', 'W'], None)
    for k in 'hv': out['lm_cable_%s' % k] = (cable(k), ['V'], None)
    for k, code in (('cam', ['Z', 'W']), ('ring', ['Z', 'W']), ('monitors', ['XX', 'XX']), ('rack', ['Z', 'W']), ('speaker', ['Z', 'W']),
                    ('couch', ['WW']), ('onair', ['X']), ('neonbolt', ['XX', 'XX']), ('desk', ['WW']), ('cables', ['V']), ('gearbox', ['W'])):
        out['lm_%s' % k] = (studio(k), code, None)
    for k, code in (('chand', ['OO', 'OO']), ('bar', ['WWW']), ('table', ['W']), ('window', ['X', 'X']), ('core', ['ZZZ', 'ZZZ', 'WWW', 'WWW']),
                    ('vault', ['XXX', 'XXX', 'WWW']), ('case', ['ZZ', 'WW']), ('pillar', ['Z', 'Z', 'W']), ('plant', ['Z', 'W'])):
        out['lm_%s' % k] = (gala(k), code, None)
    for e in 'lmr':
        out['lm_counter_%s' % e] = (desk_counter(e), ['W'], None)
        out['lm_bars_%s' % e] = (gate_bars(e), ['W'], None)
    return pieces_b3(pieces_b2(out))


# ================================================================== map builder 15, batch 2: wear, Lowlight life, more of the Fixed
def wear(v):
    """pavement wear (top-layer decals over the slabs): oil stain, leaves, litter, a brass drain, petals, chalk"""
    im = new(); r = random.Random(300 + v)
    if v == 0:
        for y in range(16):
            for x in range(16):
                d = ((x - 8) / 6.0) ** 2 + ((y - 9) / 4.0) ** 2
                if d < 1: blend(im, x, y, (60, 58, 70), 0.30 * (1 - d))
        P(im, 6, 8, A((150, 120, 190))); P(im, 9, 10, A((120, 180, 190)))
    elif v == 1:
        for _ in range(5):
            x, y = r.randrange(2, 14), r.randrange(2, 14); c = r.choice([(196, 140, 60), (170, 96, 50), (214, 176, 80)])
            P(im, x, y, A(c)); P(im, x + 1, y, A(c)); P(im, x, y + 1, A(tuple(int(t * 0.8) for t in c)))
    elif v == 2:
        R(im, 5, 6, 9, 9, A((236, 232, 222))); H(im, 5, 9, 7, A((120, 116, 110))); P(im, 11, 11, A((200, 60, 60))); P(im, 12, 11, A((200, 60, 60)))
    elif v == 3:
        R(im, 4, 5, 11, 10, A(IRN[1])); H(im, 4, 11, 5, A(BRASS[3]))
        for x in range(5, 11, 2): Vl(im, x, 6, 9, A(IRN[0]))
    elif v == 4:
        for _ in range(7):
            x, y = r.randrange(1, 15), r.randrange(1, 15); P(im, x, y, A(r.choice([(250, 220, 230), (240, 170, 190), (255, 255, 255)])))
    elif v == 5:                                     # Nessa's hopscotch, chalked
        for k, (x, y) in enumerate(((5, 1), (5, 5), (2, 9), (8, 9), (5, 13))):
            for t in range(5): P(im, x + t, y, A((240, 236, 226))); P(im, x + t, y + 3, A((240, 236, 226)))
            for t in range(4): P(im, x, y + t, A((240, 236, 226))); P(im, x + 4, y + t, A((240, 236, 226)))
    return im


def noodle_cart():
    im = new(2, 2)
    R(im, 2, 14, 29, 27, A(WINE[1])); H(im, 2, 29, 14, A(WINE[3])); R(im, 4, 17, 27, 24, A(WINE[0]))
    for x in range(6, 26, 5): R(im, x, 19, x + 2, 22, A(LITW[2]))
    disc(im, 7, 29, 2.6, A(IRN[1])); disc(im, 24, 29, 2.6, A(IRN[1]))
    R(im, 0, 2, 31, 6, A(RED[2])); H(im, 0, 31, 2, A(RED[3]))
    for x in range(0, 32, 4): Vl(im, x, 7, 9, A(RED[1]))
    for x in (3, 28): Vl(im, x, 6, 14, A(WOODL[1]))
    disc(im, 22, 12, 3, A(IRN[2])); 
    for k in range(3): disc(im, 21 + k, 7 - k * 2, 1.6, (240, 240, 250, 120))
    disc(im, 10, 11, 2, A(AMBER[2])); glow(im, 10, 11, 5, AMBER[2], 0.4)
    return im


def cobbler():
    im = new(2, 1)
    R(im, 2, 6, 29, 13, A(WOODL[2])); H(im, 2, 29, 6, A(WOODL[4])); Vl(im, 2, 6, 15, A(WOODL[1])); Vl(im, 29, 6, 15, A(WOODL[1]))
    for x, c in ((5, (120, 60, 40)), (10, (60, 50, 70)), (15, (150, 110, 70)), (21, (40, 40, 40))):
        R(im, x, 3, x + 3, 6, A(c)); P(im, x, 3, A(tuple(min(255, t + 40) for t in c)))
    R(im, 24, 2, 27, 5, A(IRN[2]))
    return im


def ladder():
    im = new(1, 2)
    for x in (3, 12): Vl(im, x, 0, 31, A(WOODL[2])); Vl(im, x + 1, 0, 31, A(WOODL[1]))
    for y in range(2, 32, 5): H(im, 3, 13, y, A(WOODL[3]))
    return im


def washline():
    im = new(3, 1)
    cols = [(230, 230, 220), (200, 80, 80), (90, 130, 200), (230, 200, 90), (150, 190, 140), (220, 150, 180)]
    for x in range(48): P(im, x, 2 + int(2 * math.sin(math.pi * x / 47.0)), A((70, 60, 60)))
    r = random.Random(5); x = 3
    while x < 44:
        c = r.choice(cols); w = r.randrange(3, 7); y = 3 + int(2 * math.sin(math.pi * x / 47.0))
        R(im, x, y, x + w - 1, y + r.randrange(5, 10), A(c)); Vl(im, x + w - 1, y, y + 4, A(tuple(int(t * 0.8) for t in c)))
        x += w + r.randrange(1, 4)
    return im


def sdoor():
    """the Spire's service door in the cliff: iron, rivets, a Meridian plate"""
    im = new(1, 2)
    R(im, 1, 2, 14, 31, A(IRN[1])); bev(im, 1, 2, 14, 31, IRN, 2)
    for y in range(6, 30, 6): H(im, 2, 13, y, A(IRN[1]))
    R(im, 3, 9, 12, 13, A(BRASS[2])); H(im, 4, 11, 11, A(BRASS[0]))
    P(im, 12, 20, A(BRASS[3])); P(im, 12, 21, A(BRASS[1]))
    R(im, 6, 3, 9, 5, A((220, 40, 40)))
    return im


def junction(open_=False):
    im = new()
    bev(im, 2, 1, 13, 15, IRN, 2); R(im, 4, 3, 11, 9, A(IRN[0]))
    for x in range(5, 11, 2): Vl(im, x, 4, 8, A((230, 196, 40)))
    if open_:
        disc(im, 8, 6, 3, A((246, 140, 60))); glow(im, 8, 6, 8, (255, 160, 80), 0.5)
    H(im, 3, 12, 12, A((230, 196, 40))); P(im, 7, 13, A(IRN[0]))
    return im


def fixed_more(v):
    """more of the Fixed: 4 the cobbler at his bench, 5 the child on one leg, 6 the lamp-tender on his ladder,
    7 the old woman bending to the bird"""
    im = new(1, 2); d = ImageDraw.Draw(im)
    if v == 4:
        d.polygon([(4, 14), (11, 14), (12, 24), (13, 30), (2, 30), (3, 24)], fill=A(CRYST[1]), outline=A(CRYST[0])); disc(im, 8, 10, 2.8, A(CRYST[2]))
        d.line([(11, 18), (15, 22)], fill=A(CRYST[2]))
    elif v == 5:
        d.polygon([(6, 10), (10, 10), (10, 20), (8, 22), (6, 20)], fill=A(CRYST[1]), outline=A(CRYST[0])); disc(im, 8, 7, 2.4, A(CRYST[2]))
        d.line([(7, 22), (7, 30)], fill=A(CRYST[2])); d.line([(9, 21), (12, 25)], fill=A(CRYST[2]))
        d.line([(6, 12), (2, 9)], fill=A(CRYST[2])); d.line([(10, 12), (14, 9)], fill=A(CRYST[2]))
    elif v == 6:
        for x in (3, 12): Vl(im, x, 0, 31, A(CRYST[0]))
        for y in range(4, 32, 6): H(im, 3, 12, y, A(CRYST[2]))
        d.polygon([(5, 4), (10, 4), (11, 14), (4, 14)], fill=A(CRYST[1]), outline=A(CRYST[0])); disc(im, 7.5, 1.5, 2.4, A(CRYST[2]))
        d.line([(10, 6), (14, 1)], fill=A(CRYST[3]))
    else:
        d.polygon([(3, 12), (10, 10), (12, 20), (12, 30), (4, 30), (4, 20)], fill=A(CRYST[1]), outline=A(CRYST[0])); disc(im, 4, 10, 2.6, A(CRYST[2]))
        d.line([(4, 16), (2, 24)], fill=A(CRYST[2])); disc(im, 2, 27, 1.8, A(CRYST[3]))
    for k in range(5):
        x, y = 4 + (k * 5) % 8, 6 + (k * 7) % 22
        if im.getpixel((x, y))[3]: P(im, x, y, A(CRYST[4]))
    for y in range(32):
        for x in range(16):
            if im.getpixel((x, y))[3] and (x + y) % 5 == 0: blend(im, x, y, (255, 255, 255), 0.35)
    H(im, 3, 12, 31, A((120, 100, 170)))
    return im


def veil(v):
    """the Bleed Veil's shimmer (overhead, see-through)"""
    im = new()
    for y in range(16):
        for x in range(16):
            t = math.sin((x + v * 5) * 0.8 + y * 0.35) * 0.5 + 0.5
            if t > 0.55: P(im, x, y, (200, 170, 255, int(40 + 90 * (t - 0.55))))
    for k in range(3): P(im, (k * 5 + v * 3) % 16, (k * 7 + v) % 16, (255, 255, 255, 200))
    return im


def pieces_b2(out):
    for v in range(6): out['lm_wear%d' % v] = (wear(v), ['V'], None)
    out['lm_noodles'] = (noodle_cart(), ['RR', 'WW'], None)
    out['lm_cobbler'] = (cobbler(), ['WW'], None)
    out['lm_ladder'] = (ladder(), ['Z', 'W'], None)
    out['lm_washline'] = (washline(), ['OOO'], None)
    out['lm_sdoor'] = (sdoor(), ['X', 'W'], None)
    out['lm_junction'] = (junction(False), ['W'], None)
    out['lm_junction_on'] = (junction(True), ['W'], None)
    for v in range(4, 8): out['lm_fixed%d' % v] = (fixed_more(v), ['Z', 'W'], None)
    for v in range(3): out['lm_veil%d' % v] = (veil(v), ['O'], None)
    return out


# ================================================================== batch 3: roofscape fill, plateau-wall alternates, Nadir far below, a viewer
def roof_fill(kind, v):
    """the roofs of the blocks behind the fronts (solid fill between buildings): verdigris scales, slate, soot tar"""
    im = new()
    if kind == 'T':
        R(im, 0, 0, 15, 15, A(SOOT[1]))
        for y in range(0, 16, 4): H(im, 0, 15, y, A(SOOT[0]))
        for x in range(0, 16, 8): Vl(im, x + (4 if v % 2 else 0), 0, 15, A(SOOT[2]))
        r = random.Random(40 + v)
        if v == 1: R(im, 4, 4, 9, 9, A(IRN[2])); H(im, 4, 9, 4, A(IRN[4])); disc(im, 6.5, 6.5, 1.5, A(IRN[0]))
        if v == 2: R(im, 6, 2, 9, 12, A(BRICKR[2])); H(im, 5, 10, 2, A(BRICKR[4])); P(im, 7, 0, (200, 200, 210, 120))
    else:
        rr = VERD if kind == 'V' else SLATEB
        im.alpha_composite(scales(16, 16, rr, seed=v + (0 if kind == 'V' else 9)), (0, 0))
        if v == 1:
            R(im, 5, 4, 10, 11, A(MARBLE[3])); disc(im, 7.5, 7.5, 2.2, A(LITW[2] if kind == 'V' else GLS[2]))
        if v == 2:
            R(im, 6, 1, 10, 9, A(BRICKR[2])); H(im, 5, 11, 1, A(BRICKR[4])); Vl(im, 10, 1, 9, A(BRICKR[0]))
    return im


def lmw_alt(row):
    im = new()
    for y in range(16):
        for x in range(16): P(im, x, y, A(lmw_px(row, x, y)))
    if row == 'face':                                 # a carved sunburst medallion
        disc(im, 8, 9, 4.5, A(MARBLE[1])); disc(im, 8, 9, 3.6, A(MARBLE[4])); disc(im, 8, 9, 1.8, A(BRASS[3]))
        for k in range(8):
            a = k * math.pi / 4; P(im, int(8 + 3 * math.cos(a)), int(9 + 3 * math.sin(a)), A(BRASS[2]))
    else:                                            # a lamp on the balustrade
        Vl(im, 7, 0, 9, A(IRN[2])); Vl(im, 8, 0, 9, A(IRN[1])); disc(im, 7.5, 1.5, 2.2, A(AMBER[2])); glow(im, 7.5, 1.5, 6, AMBER[2], 0.4)
    return im


def void2(v):
    """the drop off the plateau, deeper: near-black haze, a few lamps far below"""
    im = new()
    for y in range(16):
        for x in range(16):
            n = smooth(x, y, 190 + v, 8.0)
            P(im, x, y, A(VOIDC[0] if n < 0.5 else VOIDC[1]))
    r = random.Random(170 + v)
    for _ in range(v % 3):
        x, y = r.randrange(1, 15), r.randrange(1, 15); c = r.choice([(240, 150, 70), (200, 110, 60), (110, 200, 240)])
        P(im, x, y, A(c)); blend(im, x + 1, y, c, 0.3)
    return im


def nadir_band(v):
    """Nadir far below: tenement silhouettes in haze, lit windows, a lift cable going down"""
    im = new()
    for y in range(16):
        for x in range(16): P(im, x, y, A(VOIDC[2] if y < 6 else VOIDC[1]))
    r = random.Random(60 + v)
    x = 0
    while x < 16:
        w = r.randrange(3, 7); top = r.randrange(5, 11)
        R(im, x, top, min(15, x + w - 1), 15, A((38, 32, 52)))
        H(im, x, min(15, x + w - 1), top, A((56, 48, 72)))
        for yy in range(top + 2, 15, 3):
            for xx in range(x + 1, min(15, x + w - 1), 2):
                if r.random() < 0.35: P(im, xx, yy, A(r.choice([(240, 160, 80), (250, 200, 110), (200, 110, 70)])))
        x += w
    for y in range(0, 6):
        for x in range(16): blend(im, x, y, (90, 60, 110), 0.18)
    if v == 2: Vl(im, 9, 0, 15, A((70, 70, 90)))
    return im


def viewer():
    """a coin-op brass viewer on the lip"""
    im = new(1, 2)
    R(im, 6, 18, 9, 30, A(BRASS[1])); Vl(im, 6, 18, 30, A(BRASS[3])); R(im, 4, 28, 11, 31, A(MARBLE[2])); H(im, 4, 11, 28, A(MARBLE[4]))
    R(im, 3, 9, 12, 17, A(BRASS[2])); H(im, 3, 12, 9, A(BRASS[3])); H(im, 3, 12, 17, A(BRASS[0]))
    disc(im, 4, 12, 1.8, A(GLS[2])); disc(im, 11, 12, 1.8, A(GLS[2])); P(im, 8, 15, A(IRN[0]))
    return im


def pieces_b3(out):
    for v in range(4, 8): out['lm_pave%d' % v] = (pave(v, seed=v * 3), ['G'], None)
    for k in 'VST':
        for v in range(3): out['lm_roof%s%d' % (k, v)] = (roof_fill(k, v), ['r'], None)
    out['lmw_facem1'] = (lmw_alt('face'), ['W'], None)
    out['lmw_lipm1'] = (lmw_alt('lip'), ['W'], None)
    for v in range(6): out['lm_deep%d' % v] = (void2(v), ['M'], None)
    for v in range(3): out['lm_nadir%d' % v] = (nadir_band(v), ['M'], None)
    out['lm_viewer'] = (viewer(), ['Z', 'W'], None)
    return out


if __name__ == '__main__':
    ps = pieces()
    ims = [(n, im.resize((im.width * 2, im.height * 2), Image.NEAREST)) for n, (im, c, dr) in ps.items()]
    Wd = 2000; x = y = 0; rowh = 0; pos = []
    for n, im in ims:
        if x + im.width > Wd: x = 0; y += rowh + 14; rowh = 0
        pos.append((n, im, x, y)); x += im.width + 8; rowh = max(rowh, im.height)
    sheet = Image.new('RGBA', (Wd, y + rowh + 14), (70, 80, 74, 255))
    dr = ImageDraw.Draw(sheet)
    for n, im, x, y in pos:
        sheet.alpha_composite(im, (x, y + 12)); dr.text((x, y), n[:12], fill=(255, 230, 120, 255))
    sheet.save(sys.argv[1] if len(sys.argv) > 1 else '/tmp/ldraw.png'); print(sheet.size, len(ps))
