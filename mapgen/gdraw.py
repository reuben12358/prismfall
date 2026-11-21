#!/usr/bin/env python3
"""gdraw.py - the Glass Dunes kit (map builder 11), appended at the very end of ndraw.pieces() (so no earlier id
moves) and doubled 2x by rcustom like every rdraw / tdraw / ndraw piece.  16-px logical grid, light from the top left,
outlines never black.  Palettes follow the Glass Dunes and Flooded Dunes battle backdrops
(docs/battle_captures/backdrops/): black-green glass with teal sheen and ember cracks; pale wind-sand; red-brown
sandstone strata; turquoise flood water with foam.

  ground     gd_g0-3 (glass floor, layer 1 ground), gd_gc0-1 (ember-cracked glass), gd_floor_00..47 (the glass sheet's
             edge in the 48 autotile shapes, fused pale rim toward sand; layer 2 walk surface)
  cliffs     gdc_* glassed dune cliff kit and sdc_* sand / sandstone dune cliff kit (rkit KITS 'gdc' / 'sdc'):
             N rim w/m/e, W, E, rows lip / face / base w/m/e - no grass rim anywhere
  water      gd_flood_00..47 (flood channels: turquoise water in a dark wet-sand bed, foam at the edge; solid),
             gd_pool3 / gd_pool2 (steaming pools in glass basins)
  set pieces gd_wave (the frozen wave curl, 6x5), gd_shard0-1 (glass spires 1x2), gd_shard2 (1x1), gd_rope0-2 (ropy
             fused-glass flow texture, decal), gd_crack0-1 (ember cracks, decal), gd_spill0-1 (sand drift on glass)
  war        wr_treb_broken (3x3), wr_tower_wreck (4x2), wr_pal_h / wr_pal_hb / wr_pal_v (palisade), wr_stakes,
             wr_sandbags, wr_ban_ash_t / wr_ban_ise_t (torn banners), wr_supply (supply wagon 2x2), wr_sacks,
             wr_firering, wr_rack (weapon rack 1x2), wr_glasssled (a sled-fort fused into the glass 3x2)

    python3 -I gdraw.py out.png      # contact sheet"""
import math, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
from rdraw import P, OUT, WOOD, CLEAR, canvas, disc

GLASS = [(6, 20, 18, 255), (14, 44, 38, 255), (22, 62, 52, 255), (44, 116, 100, 255), (84, 172, 154, 255),
         (156, 230, 212, 255), (228, 255, 248, 255)]     # map builder 12: black-green body, teal-white sheen (the backdrop's glass)
FACE = [(4, 12, 14, 255), (10, 28, 28, 255), (18, 44, 42, 255), (44, 104, 96, 255), (120, 206, 188, 255)]   # obsidian faces in shade
EMBER = [(110, 36, 22, 255), (204, 88, 38, 255), (255, 164, 78, 255), (255, 228, 160, 255)]
SANDW = [(146, 124, 92, 255), (184, 162, 122, 255), (212, 194, 152, 255), (234, 222, 186, 255), (250, 244, 222, 255)]
STRATA = [(84, 46, 42, 255), (120, 68, 54, 255), (156, 98, 72, 255), (192, 136, 100, 255), (220, 180, 140, 255)]
FLOOD = [(18, 62, 72, 255), (30, 102, 110, 255), (48, 144, 146, 255), (88, 192, 182, 255), (168, 234, 222, 255),
         (240, 252, 246, 255)]
ICEW = [(56, 98, 150, 255), (98, 150, 206, 255), (150, 204, 236, 255), (204, 238, 250, 255), (246, 254, 255, 255)]
RED = [(92, 24, 28, 255), (150, 40, 40, 255), (196, 72, 56, 255), (232, 120, 84, 255)]
BLUE = [(30, 48, 92, 255), (52, 86, 150, 255), (96, 134, 196, 255), (176, 204, 236, 255)]
CANVAS = [(120, 108, 92, 255), (168, 156, 132, 255), (206, 198, 176, 255), (236, 230, 214, 255)]


def a(c, alpha):
    return c[:3] + (alpha,)


def mix(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3)) + (255,)


def nz(x, y, s):
    """cheap deterministic value noise in [0, 1)"""
    h = (x * 374761393 + y * 668265263 + s * 2147483647) & 0xffffffff
    h = ((h ^ (h >> 13)) * 1274126177) & 0xffffffff
    return (h & 0xffff) / 65536.0


# ------------------------------------------------------------------ glass ground
STREAKS = {0: [(3, 2, 12, 5), (11, 9, 5, 3)], 1: [(7, 0, 10, 4)], 2: [(12, 4, 12, 5), (4, 11, 4, 3)], 3: [(5, 1, 7, 3)],
           4: [(9, 3, 9, 4)], 5: [(2, 8, 8, 4)]}          # per variant: (row, x0, length, brightest ramp index)


def glass_px(x, y, seed, cracks=False):
    """one pixel of the glass floor (map builder 12): smooth black-green, a few designed specular streaks per variant
    (white-teal core fading to teal at the ends, a soft halo above), so neighbouring tiles scatter the glare instead of
    printing a grid; a faint sky lift near the top; rare glints"""
    gx, gy = x / 8.0, y / 8.0; ix, iy = int(gx), int(gy); fx, fy = gx - ix, gy - iy      # smooth mottles, period 16
    q = lambda i, j: nz((i % 2) + seed * 3, j % 2, seed)
    m = (q(ix, iy) * (1 - fx) + q(ix + 1, iy) * fx) * (1 - fy) + (q(ix, iy + 1) * (1 - fx) + q(ix + 1, iy + 1) * fx) * fy
    c = mix(GLASS[1], GLASS[2], 0.25 + 0.5 * m)
    if y < 4: c = mix(c, GLASS[3], 0.18 * (4 - y) / 4.0)
    for row, x0, ln, top in STREAKS.get(seed, []):
        u = x - x0
        if 0 <= u < ln:
            t = 1 - abs(u - (ln - 1) / 2.0) / (ln / 2.0)          # 1 in the middle, 0 at the ends
            if y == row: c = GLASS[min(6, 3 + int(round(t * (top - 3 + 0.49))))] if t > 0.15 else GLASS[3]
            elif y == row - 1 and t > 0.4: c = mix(c, GLASS[3], 0.5)
            elif y == row + 1 and t > 0.6: c = mix(c, GLASS[0], 0.4)
    if nz(x, y, seed + 7) > 0.997: c = GLASS[6]
    return c


def glass_ground(v, cracks=False):
    im = Image.new('RGBA', (16, 16), CLEAR); r = random.Random(1100 + v + (50 if cracks else 0))
    for y in range(16):
        for x in range(16): P(im, x, y, glass_px(x, y, v))
    if cracks:                                                     # a glowing crack: ember core, dark lips
        x, y = r.randrange(0, 4), r.randrange(3, 13)
        for _ in range(18):
            P(im, x, y - 1, GLASS[0]); P(im, x, y + 1, GLASS[0]); P(im, x, y, EMBER[1 + (x % 3 == 0)])
            x += 1; y += r.choice((-1, 0, 0, 1))
            if x > 15: break
        P(im, r.randrange(4, 12), r.randrange(2, 14), EMBER[3])
    return im


def edge_shapes(name, fill, rim, inner_rim, shadow, seed0, tex=None, R=6.0, amp=2.4):
    """an overlay in the 48 RMXP autotile shapes: `fill` inside; toward the missing neighbours a wavy, periodic edge
    (16-px period, so straight runs join up), rounded outer corners and small notches at inner corners"""
    import terrain
    rep = {}
    for b in range(256): rep.setdefault(terrain.NB2AUTO[b], b)
    out = {}
    wave = lambda u, ph: 1.6 + amp * (0.5 + 0.5 * math.sin(2 * math.pi * u / 16.0 + ph)) + 0.8 * (0.5 + 0.5 * math.sin(2 * math.pi * u / 8.0 + ph * 2))
    for sh in range(48):
        b = rep.get(sh, 255)
        n, ne, e, se, s, sw, w, nw = [(b >> i) & 1 for i in range(8)]
        im = Image.new('RGBA', (16, 16), CLEAR)
        for y in range(16):
            for x in range(16):
                d = 99.0; south = False
                cand = []
                if not n: cand.append((y - wave(x, 0.3), False))
                if not s: cand.append((15 - y - wave(x, 2.1), True))
                if not w: cand.append((x - wave(y, 1.2), False))
                if not e: cand.append((15 - x - wave(y, 4.0), False))
                for miss, cx, cy, sv in ((not n and not w, 0, 0, False), (not n and not e, 15, 0, False),
                                         (not s and not w, 0, 15, True), (not s and not e, 15, 15, True)):
                    if miss:
                        dx, dy = abs(x - cx), abs(y - cy)
                        if dx < R and dy < R: cand.append((R - math.hypot(R - dx, R - dy) - 1.0, sv))
                for ok, cx, cy in ((n and w and not nw, 0, 0), (n and e and not ne, 15, 0), (s and w and not sw, 0, 15), (s and e and not se, 15, 15)):
                    if ok: cand.append((math.hypot(x - cx, y - cy) - 3.2, cy == 15))
                for dd, sv in cand:
                    if dd < d: d, south = dd, sv
                if d < 0: continue
                if d < 1.0: c = shadow if south else rim
                elif d < 2.0: c = inner_rim
                else: c = tex(x, y, sh) if tex else fill
                P(im, x, y, c)
        out['%s_%02d' % (name, sh)] = im
    return out


# ------------------------------------------------------------------ cliff kits
def cliff_kit(prefix, glass):
    """N rim (w,m,e), W, E and three rows (lip, face, base) x (w,m,e).  The face is glass (vertical sheen, drips,
    ember seams) or sandstone (red-brown strata like the Flooded Dunes backdrop); the cap is pale wind-sand."""
    out = {}

    def face_px(x, y, seed):
        if glass:
            s = nz(x, 0, seed)
            v = (2 if y < 20 else 1) + (1 if s > 0.7 else 0)
            if y > 34: v = max(0, v - 1)
            if (x + seed) % 7 == 0 and nz(x, y, seed + 2) > 0.4: v = 3
            if (x + seed) % 11 == 4 and nz(x, y // 6, seed + 5) > 0.35: return FACE[4] if y % 9 else GLASS[6]   # vertical sheen
            if nz(x, y, seed + 9) > 0.997: return EMBER[2]
            return FACE[min(v, 3)]
        band = (y + int(2 * math.sin((x + seed) / 3.0))) // 3
        c = STRATA[1 + (band % 3)]
        if nz(x // 2, y, seed + band) > 0.86: c = STRATA[0]
        elif nz(x, y // 2, seed + 4) > 0.9: c = STRATA[4]
        return c

    def tile(kind, end):
        im = Image.new('RGBA', (16, 16), CLEAR); seed = {'w': 1, 'm': 2, 'e': 3}[end] + (0 if glass else 20)
        x0 = 3 if end == 'w' else 0; x1 = 12 if end == 'e' else 15
        for y in range(16):
            for x in range(16):
                inside = x0 <= x <= x1
                if end == 'w' and x < 3 + max(0, 3 - y // 3) and kind != 'face': inside = False
                if not inside and kind in ('lip', 'base'):
                    continue
                if kind == 'lip':
                    if y < 4: c = SANDW[3] if y == 3 else None            # the cap is the plateau's own ground
                    elif y == 4: c = GLASS[4] if glass else SANDW[4]
                    elif y == 5: c = FACE[3] if glass else STRATA[4]
                    elif y == 6: c = FACE[1] if glass else STRATA[3]
                    else: c = face_px(x, y, seed)
                    if c: P(im, x, y, c)
                elif kind == 'face':
                    if not inside: continue
                    P(im, x, y, face_px(x, y + 16, seed))
                else:                                                     # base: the foot and a spill of shards / sand
                    if y < 9: P(im, x, y, face_px(x, y + 32, seed))
                    elif y == 9: P(im, x, y, FACE[0] if glass else STRATA[0])
                    elif y == 10: P(im, x, y, a(FACE[0] if glass else STRATA[0], 150))
                    elif y < 13 and nz(x, y, seed) > 0.55: P(im, x, y, a(SANDW[1], 200))
        if kind in ('face', 'lip', 'base') and end in 'we':           # rounded, shaded ends
            for y in range(16):
                xe = x0 if end == 'w' else x1
                if im.getpixel((xe, y))[3]: P(im, xe, y, GLASS[0] if glass else STRATA[0])
        if glass and kind == 'face':                                   # a drip of fused glass running down the face
            r = random.Random(seed + 40); x = r.randrange(4, 12)
            for y in range(0, 12): P(im, x, y, FACE[3] if y % 4 else FACE[4])
        return im

    for end in 'wme':
        out['%s_lip%s' % (prefix, end)] = (tile('lip', end), ['W'], None)
        out['%s_face%s' % (prefix, end)] = (tile('face', end), ['W'], None)
        out['%s_base%s' % (prefix, end)] = (tile('base', end), ['W'], None)
    # north rim: a wind-crest along the plateau's north edge (the ground drops away north)
    for end in 'wme':
        im = Image.new('RGBA', (16, 16), CLEAR)
        for x in range(16):
            if end == 'w' and x < 4 or end == 'e' and x > 11: continue
            yy = 1 + int(1.2 * math.sin(x / 2.5 + (3 if end == 'e' else 0)))
            P(im, x, yy, a(GLASS[0] if glass else STRATA[1], 200)); P(im, x, yy + 1, SANDW[4] if not glass else GLASS[4])
            P(im, x, yy + 2, a(SANDW[3] if not glass else GLASS[3], 200))
        out['%s_N%s' % (prefix, end)] = (im, ['W' if end != 'm' else 'N'], None)
    for side in 'WE':
        im = Image.new('RGBA', (16, 16), CLEAR)
        for y in range(16):
            xs = (0, 1, 2, 3, 4) if side == 'W' else (15, 14, 13, 12, 11)
            cols = ([FACE[0], FACE[1], FACE[2], a(FACE[2], 150)] if glass else
                    [STRATA[0], STRATA[1], STRATA[3], a(SANDW[1], 150)])
            for k, xx in enumerate(xs[:4]):
                if k == 3 and nz(xx, y // 2, 3) > 0.5: continue
                P(im, xx, y, cols[k])
        out['%s_%s' % (prefix, side)] = (im, ['W'], None)
    return out


# ------------------------------------------------------------------ water: flood channels and steaming pools
def flood_tex(x, y, sh):
    t = (x * 0.8 + y * 1.7 + sh) % 9
    c = FLOOD[1] if t < 4 else FLOOD[2]
    if nz(x, y, sh + 17) > 0.93: c = FLOOD[4]
    if (y + x // 5) % 6 == 0 and nz(x // 3, y, sh) > 0.5: c = FLOOD[3]
    return c


def steam_pool(w, h, seed):
    im, d = canvas(w, h); W, H = w * 16, h * 16; r = random.Random(seed)
    d.ellipse([1, 3, W - 2, H - 2], fill=GLASS[1], outline=GLASS[0])
    d.ellipse([3, 4, W - 4, H - 5], fill=GLASS[3])
    d.ellipse([5, 6, W - 6, H - 6], fill=FLOOD[2])
    d.ellipse([7, 8, W - 9, H - 9], fill=FLOOD[3])
    for _ in range(w * h * 3):
        x, y = r.randrange(7, W - 8), r.randrange(8, H - 8)
        if im.getpixel((x, y))[:3] in (FLOOD[2][:3], FLOOD[3][:3]): P(im, x, y, FLOOD[5]); P(im, x + 1, y, FLOOD[4])
    d.arc([3, 4, W - 4, H - 5], 190, 330, fill=GLASS[5])
    for _ in range(w * 5):                                         # steam drifting off the water
        x, y = r.randrange(4, W - 4), r.randrange(0, H // 2)
        for k in range(4): P(im, x + (k % 2), y - k, (250, 252, 255, 120 - k * 20))
    return im


# ------------------------------------------------------------------ set pieces
def wave_curl():
    """the frozen wave (6x5): Kyogre's flood rose over the dunes and Isenmar's ice caught it mid-break, curling east"""
    im, d = canvas(6, 5); r = random.Random(77)
    outer = [(2, 78), (8, 60), (18, 42), (32, 26), (48, 14), (62, 8), (76, 8), (88, 14), (94, 24), (92, 34), (86, 39),
             (82, 32), (76, 28), (66, 30), (58, 38), (56, 50), (60, 62), (70, 70), (84, 74), (95, 79)]
    d.polygon(outer, fill=ICEW[1], outline=ICEW[0])
    for k in range(5):                                             # the back face lightens toward the crest
        off = k * 7
        d.line([(8 + off * 0.5, 64 - off), (24 + off * 0.6, 40 - off * 0.8), (44 + off * 0.3, 22 - off * 0.4)], fill=ICEW[2] if k % 2 else ICEW[1])
    barrel = [(82, 32), (76, 28), (66, 30), (58, 38), (56, 50), (60, 62), (70, 70), (80, 68), (75, 56), (74, 44), (80, 37)]
    d.polygon(barrel, fill=ICEW[0])
    for k in range(4): d.arc([60 + k * 2, 32 + k * 2, 84 - k, 72 - k], 110, 250, fill=(70, 120, 176, 255))
    d.line([(32, 26), (48, 14), (62, 8), (76, 8), (88, 14), (94, 24)], fill=ICEW[4], width=3)       # the frozen foam crest
    d.line([(30, 28), (46, 17), (62, 11), (76, 11), (86, 16)], fill=ICEW[3], width=1)
    for k in range(12):                                            # spray caught mid-air
        x = 40 + k * 4.5; y = 22 - 14 * math.sin(min(1.0, k / 7.0) * 1.3)
        d.polygon([(x, y), (x + 1.5, y - 5 - (k % 3) * 2), (x + 3, y)], fill=ICEW[4], outline=ICEW[2])
    for _ in range(20): P(im, r.randrange(44, 96), r.randrange(0, 14), ICEW[4])
    d.polygon([(86, 39), (92, 34), (93, 46), (88, 50)], fill=ICEW[3], outline=ICEW[1])       # the lip's falling tongue
    for k in range(5): P(im, 89 + (k % 2), 52 + k * 3, ICEW[3])
    for cx in (64, 78, 90):                                        # foam frozen at the foot
        d.ellipse([cx - 8, 72, cx + 6, 79], fill=ICEW[4], outline=ICEW[2])
    d.ellipse([0, 74, 95, 80], fill=(20, 40, 60, 60))
    return im, ['OOOOOO', 'OOOOOO', 'OOOOOO', 'WWWWWW', 'WWWWWW']


def shard(v):
    """a glass shard standing out of the floor (1x2; map builder 12): a faceted crystal blade, pale light face, dark
    facet, white edge and tip glint, a dark reflection at its foot - crystal, not a tree"""
    im, d = canvas(1, 2); r = random.Random(1200 + v)
    tip = (7 + r.randrange(3), 2 + r.randrange(4))
    lean = (-1, 2)[v]
    L = [(3, 30), (4 + lean, 14), tip, (tip[0], 30)]
    R = [(tip[0], 30), tip, (12 + lean, 12 + r.randrange(4)), (13, 30)]
    d.polygon(L, fill=(200, 246, 236, 255)); d.polygon(R, fill=(80, 168, 154, 255))
    d.line([tip, R[2], R[3]], fill=(30, 86, 80, 255)); d.line([L[0], L[1], tip], fill=(120, 200, 186, 255))
    d.line([tip, (tip[0], 29)], fill=(232, 255, 248, 255))
    d.line([(5 + lean, 16), (tip[0] - 1, tip[1] + 3)], fill=(240, 255, 250, 255))
    for k in range(2):
        y = 20 + k * 5; d.line([(5, y), (tip[0] - 1, y - 2)], fill=(196, 244, 230, 255))
    small = [(11, 30), (12 + lean, 21), (15, 30)]
    d.polygon(small, fill=(150, 222, 208, 255)); d.line([small[1], small[2]], fill=(30, 86, 80, 255)); P(im, 12 + lean, 22, (255, 255, 255, 255))
    P(im, tip[0], tip[1], (255, 255, 255, 255))
    d.ellipse([1, 29, 15, 32], fill=(0, 0, 0, 80))
    return im, ['O', 'W']


def shard_small():
    """a cluster of crystal points (1x1, solid; map builder 12): clear prisms with a bright lit face, a teal shade face,
    an outline only on the shaded side and the base, white tips and a sparkle - reads as crystal, not as a pine"""
    im, d = canvas(1, 1)
    for x0, h, w in ((0, 9, 5), (4, 14, 6), (10, 10, 5)):
        tip = (x0 + w // 2, 15 - h)
        d.polygon([(x0, 15), tip, (tip[0], 15)], fill=(206, 248, 238, 255))
        d.polygon([(tip[0], 15), tip, (x0 + w, 15)], fill=(92, 178, 164, 255))
        d.line([tip, (x0 + w, 15)], fill=(36, 96, 88, 255))
        d.line([(tip[0], tip[1] + 1), (tip[0], 14)], fill=(255, 255, 255, 255))
        P(im, tip[0], tip[1], (255, 255, 255, 255))
    d.line([(0, 15), (15, 15)], fill=(36, 96, 88, 200))
    P(im, 3, 3, (255, 255, 255, 220)); P(im, 2, 3, (220, 255, 248, 140)); P(im, 4, 3, (220, 255, 248, 140)); P(im, 3, 2, (220, 255, 248, 140))
    return im, ['W']


def rope(v):
    """fused-glass flow ridge (decal on glass; map builder 12): a long, nearly flat ridge with a hard specular top edge
    and a dark under-lip, so the floor reads as poured and polished, not as water"""
    im = Image.new('RGBA', (16, 16), CLEAR); r = random.Random(1300 + v)
    y0 = 4 + 4 * v
    for x in range(16):
        y = y0 + int(round(1.2 * math.sin((x + v * 5) / 5.0)))
        P(im, x, y, a(GLASS[5], 210)); P(im, x, y - 1, a(GLASS[3], 140)); P(im, x, y + 1, a(GLASS[0], 190))
        if x % 6 == 2: P(im, x, y, a(GLASS[6], 240))
    return im


def crack(v):
    im = Image.new('RGBA', (16, 16), CLEAR); r = random.Random(1350 + v)
    x, y = 0, r.randrange(4, 12)
    while x < 16:
        P(im, x, y, EMBER[1 + (r.random() < 0.3)]); P(im, x, y + 1, a(EMBER[0], 170)); P(im, x, y - 1, a(GLASS[0], 200))
        if r.random() < 0.2: P(im, x, y - 2, a(EMBER[2], 140))
        x += 1; y = max(2, min(13, y + r.choice((-1, 0, 0, 1))))
    return im


def spill(v):
    """wind-sand drifting over the glass (decal): soft pale streaks"""
    im = Image.new('RGBA', (16, 16), CLEAR); r = random.Random(1400 + v)
    for k in range(3):
        y0 = 2 + k * 5 + r.randrange(2); x0 = r.randrange(0, 6); L = r.randrange(6, 11)
        for i in range(L):
            P(im, x0 + i, y0 + (i > L // 2), a(SANDW[3], 210)); P(im, x0 + i, y0 + 1 + (i > L // 2), a(SANDW[1], 150))
    return im


# ------------------------------------------------------------------ war set pieces
def treb_broken():
    """a legion trebuchet broken on the glass (3x3): frame collapsed sideways, arm snapped, glass run down one side"""
    im, d = canvas(3, 3)
    d.line([4, 44, 30, 22], fill=WOOD[1], width=3); d.line([12, 44, 40, 30], fill=WOOD[1], width=3)
    d.line([2, 44, 46, 44], fill=WOOD[0], width=3); d.line([30, 22, 40, 30], fill=WOOD[0], width=2)
    d.line([30, 22, 14, 6], fill=WOOD[2], width=3); d.line([14, 6, 10, 2], fill=WOOD[3], width=2)       # snapped arm
    d.line([22, 40, 8, 30], fill=WOOD[2], width=3)                                                    # the other half
    d.rectangle([34, 34, 44, 43], fill=(86, 76, 70, 255), outline=OUT)
    for k in range(5): disc(im, 38 + k * 2 - 4, 44 - (k % 2) * 2, 1.4, (120, 112, 104, 255))
    for y in range(20, 46):                                                                           # glazed: the fire side
        if (y * 3) % 7 < 3: P(im, 41 + (y % 3), y, GLASS[4]); P(im, 42 + (y % 3), y, GLASS[2])
    for k in range(4): P(im, 30 + k * 2, 26 + k, EMBER[2])
    d.ellipse([2, 42, 46, 47], fill=(0, 0, 0, 70))
    return im, ['OOO', 'WWW', 'WWW']


def tower_wreck():
    """a siege tower toppled on its side (4x2): timber frame, hide panels burnt through, a wheel in the air"""
    im, d = canvas(4, 2)
    d.rectangle([2, 6, 60, 26], fill=WOOD[1], outline=OUT)
    for x in range(8, 60, 10): d.line([x, 6, x, 26], fill=WOOD[0], width=2)
    d.line([2, 16, 60, 16], fill=WOOD[0])
    for x0 in (10, 30): d.rectangle([x0 + 1, 8, x0 + 8, 14], fill=(110, 86, 64, 255)); d.rectangle([x0 + 3, 9, x0 + 6, 13], fill=(40, 30, 28, 255))
    d.ellipse([44, 0, 56, 12], outline=WOOD[0], width=2); disc(im, 50, 6, 1.5, WOOD[0])
    for k in range(10): P(im, 6 + k * 5, 24 - (k % 3), EMBER[1 + k % 2])
    d.ellipse([0, 26, 62, 31], fill=(0, 0, 0, 70))
    return im, ['WWWW', 'WWWW']


def palisade(kind):
    """a palisade of sharpened stakes: 'h' (a run east-west, seen from the south), 'hb' burnt, 'v' (a run north-south)"""
    im = Image.new('RGBA', (16, 16), CLEAR); d = ImageDraw.Draw(im); r = random.Random(1500 + len(kind))
    if kind in ('h', 'hb'):
        for i, x in enumerate(range(0, 16, 4)):
            top = 1 + (i % 2) * 2
            c = (44, 36, 34, 255) if kind == 'hb' and i % 2 == 0 else WOOD[2]
            d.rectangle([x, top + 2, x + 3, 13], fill=c, outline=WOOD[0]); d.polygon([(x, top + 2), (x + 1, top), (x + 3, top + 2)], fill=c)
            P(im, x + 1, top + 3, WOOD[3] if c == WOOD[2] else EMBER[2 if r.random() < 0.4 else 1])
        d.line([0, 9, 15, 9], fill=WOOD[0]); d.line([0, 14, 15, 14], fill=(0, 0, 0, 90))
    else:
        for y in range(0, 16, 4):
            d.ellipse([4, y, 11, y + 4], fill=WOOD[2], outline=WOOD[0]); disc(im, 7.5, y + 2, 1, WOOD[3])
        d.line([12, 0, 12, 15], fill=(0, 0, 0, 80))
    return im


def stakes():
    im = Image.new('RGBA', (16, 16), CLEAR); d = ImageDraw.Draw(im)
    for x0 in (1, 8):
        d.line([x0, 14, x0 + 6, 3], fill=WOOD[1], width=2); d.line([x0 + 6, 14, x0, 3], fill=WOOD[2], width=2)
        P(im, x0 + 6, 2, WOOD[3]); P(im, x0, 2, WOOD[3])
    d.line([0, 9, 15, 9], fill=WOOD[0], width=2); d.ellipse([0, 13, 15, 15], fill=(0, 0, 0, 60))
    return im


def sandbags():
    im = Image.new('RGBA', (16, 16), CLEAR); d = ImageDraw.Draw(im)
    for row, y in enumerate((9, 4)):
        for x in range(-4 + row * 4, 16, 8):
            d.rounded_rectangle([x, y, x + 8, y + 5], 2, fill=CANVAS[1], outline=CANVAS[0]); d.line([x + 2, y + 1, x + 6, y + 1], fill=CANVAS[2])
    d.line([0, 15, 15, 15], fill=(0, 0, 0, 70))
    return im


def torn_banner(cols, emblem):
    im, d = canvas(1, 3); r = random.Random(1600 + len(emblem))
    d.line([3, 2, 4, 46], fill=WOOD[0], width=2); d.line([2, 30, 5, 46], fill=GLASS[3])
    pts = [(4, 4), (14, 4), (14, 10), (11, 13), (13, 17), (9, 20), (10, 24), (6, 21), (4, 24)]
    d.polygon(pts, fill=cols[1], outline=OUT); d.line([5, 5, 13, 5], fill=cols[3])
    if emblem == 'dragon': d.polygon([(6, 15), (9, 7), (12, 15), (9, 12)], fill=(214, 170, 60, 255))
    else: d.ellipse([6, 9, 12, 13], fill=cols[3])
    for k in range(5): P(im, r.randrange(5, 13), r.randrange(6, 20), (40, 30, 30, 255))
    d.ellipse([0, 44, 8, 47], fill=(0, 0, 0, 60))
    return im, ['O', 'O', 'W']


def supply_wagon():
    im, d = canvas(2, 2)
    d.rectangle([2, 12, 29, 22], fill=WOOD[2], outline=OUT)
    d.chord([2, 1, 29, 22], 180, 360, fill=CANVAS[2], outline=CANVAS[0]); d.line([8, 4, 8, 12], fill=CANVAS[1]); d.line([23, 4, 23, 12], fill=CANVAS[1])
    for cx in (8, 23): d.ellipse([cx - 5, 18, cx + 5, 29], outline=WOOD[0], width=2); disc(im, cx, 23, 1, WOOD[0])
    d.rectangle([12, 14, 19, 20], fill=(150, 120, 80, 255), outline=WOOD[0])
    d.ellipse([1, 28, 31, 31], fill=(0, 0, 0, 60))
    return im, ['OO', 'WW']


def sacks():
    im = Image.new('RGBA', (16, 16), CLEAR); d = ImageDraw.Draw(im)
    for x0, y0 in ((1, 6), (8, 6), (4, 1)):
        d.rounded_rectangle([x0, y0, x0 + 7, y0 + 8], 3, fill=CANVAS[1], outline=CANVAS[0]); d.line([x0 + 2, y0 + 1, x0 + 5, y0 + 1], fill=CANVAS[3])
    d.line([1, 15, 15, 15], fill=(0, 0, 0, 70))
    return im


def fire_ring():
    im = Image.new('RGBA', (16, 16), CLEAR); d = ImageDraw.Draw(im)
    d.ellipse([2, 4, 13, 14], fill=(54, 46, 44, 255))
    for k in range(10):
        t = k / 10 * 2 * math.pi; x, y = 7.5 + 6 * math.cos(t), 9 + 5 * math.sin(t)
        disc(im, x, y, 1.6, (120, 112, 104, 255)); P(im, int(x), int(y) - 1, (168, 160, 150, 255))
    for x, y in ((6, 9), (8, 8), (9, 10)): P(im, x, y, EMBER[1])
    d.line([4, 8, 11, 11], fill=WOOD[0], width=2)
    return im


def weapon_rack():
    im, d = canvas(1, 2)
    d.line([2, 6, 2, 30], fill=WOOD[0], width=2); d.line([13, 6, 13, 30], fill=WOOD[0], width=2); d.line([1, 10, 14, 10], fill=WOOD[1], width=2)
    for x in (4, 7, 10):
        d.line([x, 2, x, 28], fill=(150, 150, 160, 255)); P(im, x, 1, (210, 210, 220, 255)); P(im, x, 2, (190, 190, 200, 255))
    d.ellipse([0, 28, 15, 31], fill=(0, 0, 0, 60))
    return im, ['O', 'W']


def glass_sled():
    """a sled-fort caught in the glass (3x2): the stockade half sunk in fused black-green glass, a runner sticking out"""
    im, d = canvas(3, 2)
    for i, x in enumerate(range(3, 45, 5)):
        top = 6 + (i % 2) * 2
        d.rectangle([x, top, x + 4, 22], fill=(44, 36, 34, 255) if i % 3 else WOOD[1], outline=OUT); d.polygon([(x, top), (x + 2, top - 3), (x + 4, top)], fill=(44, 36, 34, 255))
    d.polygon([(0, 31), (2, 18), (12, 16), (24, 19), (36, 15), (46, 18), (47, 31)], fill=GLASS[2], outline=GLASS[0])
    d.line([3, 19, 12, 17, 24, 20, 36, 16, 45, 19], fill=GLASS[5])
    d.line([36, 26, 47, 22], fill=WOOD[0], width=2)
    for k in range(5): P(im, 6 + k * 8, 24 + k % 2, GLASS[6])
    return im, ['OOO', 'WWW']


def ford(vertical):
    """a fused-glass causeway across a flood channel (walkable deck over the water): 'v' runs north-south"""
    im = Image.new('RGBA', (16, 16), CLEAR)
    for y in range(16):
        for x in range(16):
            u, v = (x, y) if vertical else (y, x)                      # u across the causeway, v along it
            if 3 <= u <= 12:
                c = glass_px(x, y, 9)
                if u in (3, 12): c = GLASS[0]
                elif u in (4, 11): c = GLASS[4] if u == 4 else GLASS[1]
                P(im, x, y, c)
            else:
                c = flood_tex(x, y, 5)
                if u in (2, 13): c = FLOOD[5]
                P(im, x, y, c)
    return im



# ------------------------------------------------------------------ map builder 12 (appended at the end of pieces())
SNOWTOP = [(150, 170, 196, 255), (196, 212, 232, 255), (222, 232, 246, 255), (238, 244, 252, 255), (252, 254, 255, 255)]
SNOWFACE = [(92, 108, 138, 255), (128, 146, 176, 255), (170, 186, 210, 255), (206, 218, 236, 255)]
BONE = [(104, 92, 76, 255), (168, 154, 128, 255), (214, 204, 180, 255), (240, 234, 216, 255)]


def sheen(v):
    """a specular streak on black glass (decal): v 0-1 a long diagonal glare band, v 2-3 a short bright glint with a
    four-point sparkle; white core, teal falloff, fading at the ends"""
    im = Image.new('RGBA', (16, 16), CLEAR)
    if v < 2:
        off = (-3, 4)[v]
        for x in range(16):
            yc = 15 - x * 0.75 + off
            fade = min(1.0, min(x + 1, 16 - x) / 5.0)
            for dy in range(-2, 3):
                y = int(round(yc + dy))
                if not (0 <= y < 16): continue
                if dy == 0: c, al = (244, 255, 250), 190
                elif abs(dy) == 1: c, al = GLASS[5][:3], 120
                else: c, al = GLASS[4][:3], 55
                P(im, x, y, c + (int(al * fade),))
    else:
        y0 = (6, 10)[v - 2]; x0 = (3, 6)[v - 2]
        for i in range(9):
            al = int(200 * (1 - abs(i - 4) / 5.0))
            P(im, x0 + i, y0, (240, 255, 250, al)); P(im, x0 + i, y0 + 1, GLASS[4][:3] + (al // 3,))
        cx = x0 + 4
        for k in (1, 2):
            P(im, cx, y0 - k, (255, 255, 255, 200 - 70 * k)); P(im, cx, y0 + k, (255, 255, 255, 200 - 70 * k))
        P(im, cx, y0, (255, 255, 255, 255))
    return im


def sky(v):
    """the sky reflected in the glass (decal): a soft pale wash with a brighter cloud streak, mostly transparent so the
    black-green shows through at the edges"""
    im = Image.new('RGBA', (16, 16), CLEAR)
    base = ((70, 170, 168), (110, 170, 200))[v]; cloud = ((200, 246, 240), (220, 236, 252))[v]
    for y in range(16):
        for x in range(16):
            d = math.hypot((x - 7.5) / 8.0, (y - 7.5) / 5.5)
            if d >= 1.0: continue
            al = int(120 * (1 - d) ** 0.6)
            c = base
            if abs((y - 6) - (x - 8) * 0.25) < 1.2 and 2 < x < 14: c, al = cloud, al + 50
            P(im, x, y, c + (min(255, al),))
    return im


def spire():
    """a crystal spire cluster (2x3): faceted prisms of clear glass, light face to the left, dark facet right, sharp
    tips, a white edge and a sparkle; reads as crystal, not a tree"""
    im, d = canvas(2, 3)
    prisms = [(6, 47, 13, 9, 5), (14, 47, 20, 2, 6), (21, 47, 27, 14, 5), (10, 47, 15, 22, 4), (24, 47, 30, 28, 3)]
    for x0, yb, x1, ytip, w in prisms:
        mid = (x0 + x1) // 2
        left = [(x0, yb), (x0 + 1, ytip + 8), (mid, ytip), (mid, yb)]
        right = [(mid, yb), (mid, ytip), (x1 - 1, ytip + 8), (x1, yb)]
        d.polygon(left, fill=(150, 224, 206, 255)); d.polygon(right, fill=(46, 104, 92, 255))
        d.line([(mid, ytip), (mid, yb)], fill=(232, 252, 246, 255))
        d.line([(x0, yb), (x0 + 1, ytip + 8), (mid, ytip), (x1 - 1, ytip + 8), (x1, yb)], fill=(16, 44, 40, 255))
        d.line([(x0 + 2, ytip + 10), (mid - 1, ytip + 3)], fill=(246, 255, 252, 255))
        for k in range(3):
            y = ytip + 14 + k * 7
            if y < yb - 2: d.line([(x0 + 2, y), (mid - 1, y - 2)], fill=(196, 240, 228, 255))
    for (x, y) in ((11, 11), (17, 4)):
        P(im, x, y, (255, 255, 255, 255)); P(im, x - 1, y, (220, 255, 245, 180)); P(im, x + 1, y, (220, 255, 245, 180))
        P(im, x, y - 1, (220, 255, 245, 180)); P(im, x, y + 1, (220, 255, 245, 180))
    d.ellipse([3, 44, 31, 48], fill=(0, 0, 0, 70))
    return im, ['OO', 'OO', 'WW']


def whalebone():
    """a whalebone waymarker (1x2): one great rib set upright and curving seaward, rope-bound, a cairn at the foot"""
    im, d = canvas(1, 2)
    for t in range(26):
        y = 28 - t; x = 5 + int(5 * math.sin(t / 26.0 * 1.9))
        wdt = 3 if t < 18 else 2
        for k in range(wdt):
            P(im, x + k, y, BONE[2] if k == 0 else BONE[1])
        P(im, x - 1, y, BONE[0]); P(im, x + wdt, y, BONE[0])
        if t % 5 == 2: P(im, x, y, BONE[3])
    for yy in (16, 18): d.line([(6, yy), (10, yy - 1)], fill=(122, 86, 52, 255))
    d.ellipse([2, 26, 13, 31], fill=(132, 140, 156, 255), outline=(84, 90, 104, 255))
    P(im, 5, 27, (190, 200, 214, 255)); P(im, 9, 28, (190, 200, 214, 255))
    return im, ['O', 'W']


def ice_px(x, y, sh):
    """frozen flood water (map builder 12): pale blue sea-ice in broad diagonal bands, white wind streaks, a few dark
    hairline cracks; 16-periodic so runs join"""
    band = ((x + y) // 3) % 6
    c = ICEW[3] if band < 2 else ICEW[2]
    if (x * 2 + y * 5) % 16 == 0: c = ICEW[4]
    if (y % 8 == 5 and 3 <= (x + 2 * (y // 8)) % 16 <= 9): c = ICEW[4]
    if (x - 2 * y) % 16 == 7 and (y % 16) in (2, 3, 4, 11, 12): c = ICEW[1]
    return c

def pieces():
    import ndraw
    out = {}
    GLASS_FACE = [FACE[1], FACE[2], FACE[3], FACE[4]]
    for e in 'wme':
        out['gdl_' + e] = (ndraw.ledge(e, face=GLASS_FACE, top=[GLASS[0], GLASS[3], GLASS[2], GLASS[4], GLASS[6]]), ['L'], None)   # 12: a glass lip
        out['sdl_' + e] = (ndraw.ledge(e, face=[STRATA[1], STRATA[2], STRATA[3], STRATA[4]], top=SANDW), ['L'], None)
    out['gd_ford_v'] = (ford(True), ['D'], None)
    out['gd_ford_h'] = (ford(False), ['D'], None)
    for v in range(4): out['gd_g%d' % v] = (glass_ground(v), ['G'], None)
    for v in range(2): out['gd_gc%d' % v] = (glass_ground(v + 4, cracks=True), ['G'], None)
    tex = lambda x, y, sh: glass_px(x, y, 0)
    for n, im in edge_shapes('gd_floor', GLASS[1], SANDW[4], GLASS[5], GLASS[0], 31, tex).items(): out[n] = (im, ['V'], None)
    for n, im in edge_shapes('gd_flood', FLOOD[1], FLOOD[5], FLOOD[3], (60, 52, 40, 255), 37, flood_tex).items(): out[n] = (im, ['W'], None)
    out.update(cliff_kit('gdc', True))
    out.update(cliff_kit('sdc', False))
    out['gd_pool3'] = (steam_pool(3, 2, 61), ['WWW', 'WWW'], None)
    out['gd_pool2'] = (steam_pool(2, 2, 62), ['WW', 'WW'], None)
    im, c = wave_curl(); out['gd_wave'] = (im, c, None)
    for v in range(2): im, c = shard(v); out['gd_shard%d' % v] = (im, c, None)
    im, c = shard_small(); out['gd_shard2'] = (im, c, None)
    for v in range(3): out['gd_rope%d' % v] = (rope(v), ['V'], None)
    for v in range(2): out['gd_crack%d' % v] = (crack(v), ['V'], None)
    for v in range(2): out['gd_spill%d' % v] = (spill(v), ['V'], None)
    im, c = treb_broken(); out['wr_treb_broken'] = (im, c, None)
    im, c = tower_wreck(); out['wr_tower_wreck'] = (im, c, None)
    for k in ('h', 'hb', 'v'): out['wr_pal_' + k] = (palisade(k), ['W'], None)
    out['wr_stakes'] = (stakes(), ['W'], None)
    out['wr_sandbags'] = (sandbags(), ['W'], None)
    im, c = torn_banner(RED, 'dragon'); out['wr_ban_ash_t'] = (im, c, None)
    im, c = torn_banner(BLUE, 'whale'); out['wr_ban_ise_t'] = (im, c, None)
    im, c = supply_wagon(); out['wr_supply'] = (im, c, None)
    out['wr_sacks'] = (sacks(), ['W'], None)
    out['wr_firering'] = (fire_ring(), ['W'], None)
    im, c = weapon_rack(); out['wr_rack'] = (im, c, None)
    im, c = glass_sled(); out['wr_glasssled'] = (im, c, None)
    # map builder 12: snow ledges (Rimewood), glass sheen and sky decals, the crystal spire, whalebone waymarkers
    for e in 'wme': out['lgs_' + e] = (ndraw.ledge(e, face=SNOWFACE, top=SNOWTOP), ['L'], None)
    for v in range(4): out['gd_sheen%d' % v] = (sheen(v), ['V'], None)
    for v in range(2): out['gd_sky%d' % v] = (sky(v), ['V'], None)
    im, c = spire(); out['gd_spire'] = (im, c, None)
    im, c = whalebone(); out['pf_whalebone'] = (im, c, None)
    tex_ice = lambda x, y, sh: ice_px(x, y, sh)
    for n, im in edge_shapes('gd_ice', ICEW[2], ICEW[4], ICEW[3], ICEW[0], 41, tex_ice, amp=1.8).items(): out[n] = (im, ['I'], None)
    return out


if __name__ == '__main__':
    ps = pieces()
    keep = lambda n: not (n.startswith(('gd_floor_', 'gd_flood_')) and not n.endswith(('_00', '_15', '_33', '_46', '_01', '_20')))
    ims = [(n, im.resize((im.width * 2, im.height * 2), Image.NEAREST)) for n, (im, c, dr) in ps.items() if keep(n)]
    Wd = 1400; x = y = 0; rowh = 0; pos = []
    for n, im in ims:
        if x + im.width > Wd: x = 0; y += rowh + 14; rowh = 0
        pos.append((n, im, x, y)); x += im.width + 10; rowh = max(rowh, im.height)
    sheet = Image.new('RGBA', (Wd, y + rowh + 14), SANDW[2])
    dr = ImageDraw.Draw(sheet)
    for n, im, x, y in pos:
        sheet.alpha_composite(im, (x, y + 12)); dr.text((x, y), n, fill=(120, 0, 60, 255))
    sheet.save(sys.argv[1] if len(sys.argv) > 1 else '/tmp/gdraw.png'); print(sheet.size)
