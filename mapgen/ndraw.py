#!/usr/bin/env python3
"""ndraw.py - the nature kit for the crafted roads (map builder 10), appended to the PF Rejuv `pf` part through
rdraw.pieces_late4 (rcustom dedups identical tiles).  Drawn on the 16-px logical grid like rdraw / tdraw (light from
the top left, outlines never black, Sheridan / Akuwa ramps) and doubled 2x by rcustom.

Pieces:
  ledges        lg_w/m/e (grass) and lgc_w/m/e (chalk): one-way jump-down ledges (terrain tag 1, entered from above only)
  coast         cs_wet_00..47 (wet-sand overlay in the 48 RMXP autotile shapes), cs_wrack0-3 (tide line), cs_shell0-1,
                cs_wrock0-2 (rocks in the shallows, dark ring and foam), cs_kelp0-1, cs_pool_a/b (rock pools),
                pf_seaarch, pf_seastack (chalk in the sea), pf_lacearch (the Lace Arches, walk-through N-S)
  landmarks     pf_wlamp (the Wrecker's Lamp), pf_sigpole, pf_beacon, pf_stonebench, pf_roadstone, pf_shrine,
                nr_wall_w/m/e/v (drystone walls), nr_col, nr_colfall, nr_ruin, pf_hayrick, pf_sledge
  silk          gw_drape0/1, gw_cocoons, gw_rack, gw_spool, gw_bridge_n/m/s (the Weft Bridge)
  mechanics     fw_gust0-2 (wind-gap streaks), df_slab_r/b/y (sluice stones), df_sluice, mr_chute0-1 (the sledge run)

    python3 -I ndraw.py out.png      # contact sheet"""
import math, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import rdraw as D
from rdraw import P, OUT, WOOD, STONE, GLOW, CLEAR, canvas, disc

GRASS = [(40, 104, 80, 255), (64, 176, 136, 255), (112, 200, 160, 255), (136, 216, 184, 255), (160, 224, 192, 255)]
TALL = [(56, 88, 16, 255), (56, 144, 48, 255), (24, 160, 104, 255)]
EARTH = [(70, 50, 44, 255), (96, 70, 56, 255), (124, 94, 70, 255), (150, 118, 88, 255)]
CHALK = [(110, 108, 118, 255), (160, 158, 162, 255), (198, 196, 192, 255), (226, 224, 216, 255), (246, 244, 236, 255)]
SAND = [(150, 140, 100), (178, 168, 124), (200, 192, 146), (216, 211, 162), (232, 228, 186)]
WATER = [(48, 96, 176, 255), (72, 120, 216, 255), (72, 144, 216, 255), (184, 216, 248, 255), (236, 246, 252, 255)]
SILK = [(150, 156, 178, 255), (196, 202, 220, 255), (226, 230, 242, 255), (248, 250, 255, 255)]
SANDF = [(122, 92, 60, 255), (160, 128, 86, 255), (196, 168, 116, 255), (222, 202, 150, 255)]
ROCK = [(72, 38, 40, 255), (92, 66, 68, 255), (124, 94, 92, 255), (150, 128, 120, 255), (176, 160, 150, 255)]
MOSS = [(52, 104, 60, 255), (86, 150, 86, 255), (130, 190, 110, 255)]

# extra code letters (layer, passage, priority[, terrain tag]); merged into rdraw.CODE by pieces()
CODES = {'L': (1, 1, 0, 1),        # ledge: layer 2, entered from above only, terrain tag 1 (Essentials jumps 2 tiles)
         'V': (2, 0, 0),           # flat decal on the top layer, priority 0 (walkable ground under it)
         'X': (2, 15, 0),          # solid object on the top layer (rocks in water: the water autotile stays below)
         'B': (1, 8, 0),           # bridge rail row, north side: deck, no crossing the top edge
         'C': (1, 1, 0),           # bridge rail row, south side
         'K': (1, 0, 0)}           # bridge deck


def rng_for(*k):
    return random.Random(hash(k) & 0xffffffff)


def shade(c, f):
    return tuple(max(0, min(255, int(v * f))) for v in c[:3]) + (c[3] if len(c) > 3 else 255,)


# ------------------------------------------------------------------ ledges
def ledge(end, face=None, top=None):
    """one tile of a south-facing ledge (Gen 4 habit): a turf lip over a tall, shaded drop face (earth or chalk) that
    fills the lower half of the tile, a dark foot and a shadow; above the lip the tile is clear so the ground shows.
    end: 'w', 'm', 'e' (the ends round off into the ground)"""
    face = face or EARTH; top = top or GRASS
    im = Image.new('RGBA', (16, 16), CLEAR); r = random.Random({'w': 1, 'm': 2, 'e': 3}[end] + (7 if face is CHALK else 0))
    dark = tuple(max(0, c - 40) for c in face[0][:3]) + (255,)
    for x in range(16):
        inset = 0
        if end == 'w': inset = max(0, 4 - x)
        if end == 'e': inset = max(0, x - 11)
        if inset >= 4: continue
        y0 = 4 + inset + (1 if (x * 7) % 5 == 0 else 0)                 # the lip, slightly uneven
        yb = 14 - inset // 2
        P(im, x, y0 - 1, top[0]); P(im, x, y0, top[4]); P(im, x, y0 + 1, top[2])
        P(im, x, y0 + 2, top[0])                                         # under the lip
        for y in range(y0 + 3, yb):
            k = (y - y0 - 3) / max(1, yb - y0 - 3)
            c = face[3] if k < 0.15 else face[2] if k < 0.55 else face[1]
            if (x + 3 * y) % 9 == 0: c = face[0]
            P(im, x, y, c)
        if r.random() < 0.55: P(im, x, y0 + 3, top[1])                   # turf hanging over the face
        if r.random() < 0.25: P(im, x, y0 + 4, top[0])
        P(im, x, yb, dark); P(im, x, yb + 1, (0, 0, 0, 80))
    if end == 'w':
        for y in range(8, 15): P(im, 3 - (y - 8) // 3, y, dark)
    if end == 'e':
        for y in range(8, 15): P(im, 12 + (y - 8) // 3, y, dark)
    return im


# ------------------------------------------------------------------ coast
def wet_shapes():
    """the wet-sand overlay in the 48 RMXP autotile shapes: a translucent damp tint, ragged at the edges toward dry
    sand (the shape's missing neighbours), a few darker specks and tiny shell glints.  Placed on z=2 over the sand."""
    import terrain
    rep = {}
    for b in range(256):
        rep.setdefault(terrain.NB2AUTO[b], b)
    out = {}
    for sh in range(48):
        b = rep.get(sh, 255)
        n, ne, e, se, s, sw, w, nw = [(b >> i) & 1 for i in range(8)]
        im = Image.new('RGBA', (16, 16), CLEAR); r = random.Random(500 + sh)
        for y in range(16):
            for x in range(16):
                d = 9.0
                if not n: d = min(d, y)
                if not s: d = min(d, 15 - y)
                if not w: d = min(d, x)
                if not e: d = min(d, 15 - x)
                if n and w and not nw: d = min(d, max(x, y))
                if n and e and not ne: d = min(d, max(15 - x, y))
                if s and w and not sw: d = min(d, max(x, 15 - y))
                if s and e and not se: d = min(d, max(15 - x, 15 - y))
                lim = 2.2 + 1.6 * math.sin(x * 1.7 + y * 0.9 + sh) * 0.5 + r.random() * 1.2
                if d < lim - 1.0: continue
                a = 110 if d >= lim else 60
                c = SAND[0] if r.random() < 0.06 else SAND[1]
                P(im, x, y, c + (a,))
        for _ in range(2):
            x, y = r.randrange(2, 14), r.randrange(2, 14)
            if im.getpixel((x, y))[3]: P(im, x, y, (236, 232, 214, 180))
        out['cs_wet_%02d' % sh] = im
    return out


def wrack(v):
    """the tide line: dark kelp strands, a twig of driftwood, a shell (1x1 decal on sand)"""
    im = Image.new('RGBA', (16, 16), CLEAR); r = random.Random(610 + v)
    for _ in range(2 + v % 2):
        x, y = r.randrange(1, 10), r.randrange(4, 13); L = r.randrange(4, 8)
        for k in range(L):
            yy = y + int(round(math.sin(k * 0.9 + v) * 1.2))
            P(im, x + k, yy, (60, 70, 40, 255)); P(im, x + k, yy + 1, (40, 48, 30, 140))
            if k % 3 == 1: P(im, x + k, yy - 1, (96, 104, 54, 255))
    if v in (1, 3):
        x, y = r.randrange(3, 10), r.randrange(3, 12)
        for k in range(5): P(im, x + k, y + k // 3, (140, 110, 80, 255)); P(im, x + k, y + k // 3 + 1, (90, 70, 56, 255))
    if v in (0, 2):
        x, y = r.randrange(4, 12), r.randrange(4, 12)
        P(im, x, y, (250, 236, 230, 255)); P(im, x + 1, y, (240, 200, 196, 255)); P(im, x, y + 1, (214, 170, 170, 255)); P(im, x + 1, y + 1, (190, 150, 150, 255))
    return im


def shell(v):
    im = Image.new('RGBA', (16, 16), CLEAR); r = random.Random(630 + v)
    for _ in range(3):
        x, y = r.randrange(2, 13), r.randrange(2, 13)
        c = [(250, 240, 232, 255), (236, 190, 190, 255), (200, 214, 236, 255)][r.randrange(3)]
        P(im, x, y, c); P(im, x + 1, y, shade(c, 0.85)); P(im, x, y + 1, shade(c, 0.75))
    for _ in range(4):
        P(im, r.randrange(1, 15), r.randrange(1, 15), (150, 140, 120, 255))
    return im


def wrock(v, chalk=True):
    """a rock in the shallows: a darker ring of deeper water, a lace of foam round the foot, the rock lit from the NW"""
    im = Image.new('RGBA', (16, 16), CLEAR); r = random.Random(650 + v)
    pal = CHALK if chalk else ROCK
    disc(im, 8, 9.5, 7.2, (40, 84, 170, 110))
    for a in range(0, 360, 20):
        if r.random() < 0.7:
            x = 8 + 6.3 * math.cos(math.radians(a)); y = 9.8 + 4.6 * math.sin(math.radians(a))
            P(im, x, y, WATER[4][:3] + (220,))
    rx, ry = 4.6 + v * 0.6, 3.8 + (v % 2) * 0.6
    for y in range(16):
        for x in range(16):
            dx, dy = (x + 0.5 - 8) / rx, (y + 0.5 - 8) / ry
            if dx * dx + dy * dy <= 1.0:
                lit = -dx * 0.6 - dy * 0.8
                c = pal[3] if lit > 0.45 else pal[2] if lit > -0.15 else pal[1]
                P(im, x, y, c)
            elif dx * dx + dy * dy <= 1.25:
                P(im, x, y, pal[0])
    if v == 2: P(im, 6, 6, (230, 90, 110, 255)); P(im, 7, 6, (200, 70, 90, 255))     # a starfish
    return im


def kelp(v):
    im = Image.new('RGBA', (16, 16), CLEAR); r = random.Random(670 + v)
    for _ in range(4):
        x, y = r.randrange(3, 13), r.randrange(3, 13)
        for k in range(5):
            P(im, x + int(math.sin(k + v) * 1.5), y + k - 2, (70, 100, 50, 220))
        P(im, x, y - 2, (120, 150, 70, 230))
    return im


def rock_pool(w, h, seed):
    """a rock pool on the shore: a ragged ring of chalk rock round still, clear water with weed, an anemone"""
    im = Image.new('RGBA', (w * 16, h * 16), CLEAR); r = random.Random(seed)
    W_, H_ = w * 16, h * 16; cx, cy = W_ / 2, H_ / 2 + 1
    ax, ay = W_ / 2 - 1.5, H_ / 2 - 1.5
    for y in range(H_):
        for x in range(W_):
            dx, dy = (x + 0.5 - cx) / ax, (y + 0.5 - cy) / ay
            q = dx * dx + dy * dy + 0.08 * math.sin(x * 0.9) * math.cos(y * 1.3)
            if q <= 0.42:
                deep = q < 0.18
                P(im, x, y, (64, 128, 196, 255) if deep else (96, 160, 214, 255))
            elif q <= 1.0:
                lit = -dx * 0.55 - dy * 0.8
                c = CHALK[3] if lit > 0.35 else CHALK[2] if lit > -0.2 else CHALK[1]
                if r.random() < 0.08: c = (140, 160, 110, 255)
                P(im, x, y, c)
            elif q <= 1.18:
                P(im, x, y, CHALK[0])
    for _ in range(w * h):
        x, y = int(cx + r.uniform(-ax * 0.5, ax * 0.5)), int(cy + r.uniform(-ay * 0.4, ay * 0.4))
        P(im, x, y, (90, 140, 70, 255)); P(im, x, y - 1, (120, 170, 80, 255))
    x, y = int(cx + ax * 0.25), int(cy - ay * 0.1)
    P(im, x, y, (230, 80, 120, 255)); P(im, x + 1, y, (250, 140, 170, 255)); P(im, x, y + 1, (190, 60, 100, 255))
    for x in range(int(cx - ax * 0.6), int(cx + ax * 0.6)): P(im, x, int(cy - ay * 0.55), (220, 236, 250, 120))
    return im


def chalk_blob(im, cx, cy, rx, ry, r, lace=0):
    """a chalk mass, strata lines and lace holes"""
    for y in range(int(cy - ry - 1), int(cy + ry + 2)):
        for x in range(int(cx - rx - 1), int(cx + rx + 2)):
            dx, dy = (x + 0.5 - cx) / rx, (y + 0.5 - cy) / ry
            q = dx * dx + dy * dy + 0.06 * math.sin(y * 1.4 + x * 0.3)
            if q <= 1.0:
                lit = -dx * 0.7 - dy * 0.3
                c = CHALK[4] if lit > 0.5 else CHALK[3] if lit > 0 else CHALK[2] if lit > -0.5 else CHALK[1]
                if (y + int(x * 0.2)) % 6 == 0: c = shade(c, 0.86)
                P(im, x, y, c)
            elif q <= 1.2:
                P(im, x, y, CHALK[0])
    for _ in range(lace):
        x, y = r.uniform(cx - rx * 0.6, cx + rx * 0.6), r.uniform(cy - ry * 0.5, cy + ry * 0.5)
        rr = r.choice((1.2, 1.6, 2.0))
        disc(im, x, y, rr + 0.7, CHALK[0]); disc(im, x, y, rr, (72, 120, 160, 255)); P(im, x - 0.5, y - 0.5, (110, 160, 200, 255))


def turf_cap(im, x0, x1, y, r, pinks=True):
    for x in range(x0, x1 + 1):
        h = 3 + (1 if r.random() < 0.4 else 0)
        for k in range(h): P(im, x, y + k, GRASS[1] if k else GRASS[3])
        P(im, x, y + h, GRASS[0])
        if pinks and r.random() < 0.18: P(im, x, y + 1, (240, 150, 180, 255))


def sea_arch():
    """a chalk sea arch standing in the water (6x5): two legs, a laced span, foam at the feet; water shows through"""
    im, d = canvas(6, 5); r = random.Random(81)
    for (cx, w) in ((15, 13), (81, 13)):
        for y in range(26, 76):
            rx = w + (2 if y > 64 else 0) - (y < 34) * 2
            for x in range(int(cx - rx), int(cx + rx) + 1):
                dx = (x - cx) / rx; lit = -dx
                c = CHALK[3] if lit > 0.3 else CHALK[2] if lit > -0.4 else CHALK[1]
                if (y + x // 5) % 7 == 0: c = shade(c, 0.86)
                P(im, x, y, c)
            P(im, cx - rx - 1, y, CHALK[0]); P(im, cx + rx + 1, y, CHALK[0])
        for x in range(int(cx - w - 3), int(cx + w + 4)):
            if r.random() < 0.8: P(im, x, 76 + r.randrange(2), WATER[4][:3] + (230,))
    chalk_blob(im, 48, 22, 46, 16, r, lace=7)
    for x in range(30, 66):                                     # the opening's underside
        y = 30 + int(8 * math.sin(math.pi * (x - 30) / 36))
        for yy in range(y, 40): P(im, x, yy, CLEAR)
        P(im, x, y - 1, CHALK[0]); P(im, x, y - 2, CHALK[1])
    turf_cap(im, 6, 90, 6, r)
    code = ['OOOOOO', 'OOOOOO', 'XO..OX', 'XX..XX', 'XX..XX']
    return im, code


def sea_stack(seed=91):
    """a chalk stack in the sea (3x4) with a Wingull rookery on its turf cap (nests, whitewash)"""
    im, d = canvas(3, 4); r = random.Random(seed)
    for y in range(10, 62):
        rx = 18 - (y < 16) * 3 + (y > 50) * 2
        for x in range(int(24 - rx), int(24 + rx) + 1):
            dx = (x - 24) / rx; lit = -dx
            c = CHALK[3] if lit > 0.3 else CHALK[2] if lit > -0.4 else CHALK[1]
            if (y + x // 4) % 6 == 0: c = shade(c, 0.88)
            if r.random() < 0.05 and y > 20: c = CHALK[4]
            P(im, x, y, c)
        P(im, 24 - rx - 1, y, CHALK[0]); P(im, 24 + rx + 1, y, CHALK[0])
    for x in range(4, 45):
        if r.random() < 0.75: P(im, x, 62 + r.randrange(2), WATER[4][:3] + (230,))
    turf_cap(im, 8, 40, 7, r, pinks=False)
    for _ in range(4):                                          # nests and whitewash
        x, y = r.randrange(12, 36), r.randrange(8, 12)
        P(im, x, y, (130, 100, 70, 255)); P(im, x + 1, y, (150, 120, 80, 255)); P(im, x, y - 1, (250, 250, 250, 255))
        for k in range(r.randrange(4, 12)): P(im, x + r.randrange(-1, 2), y + 3 + k, (250, 250, 246, 200))
    return im, ['OOO', 'XXX', 'XXX', 'XXX']


def lace_arch():
    """the Lace Arches (7x5): a sea-worn chalk arch on the cliff top; the path runs north-south through the opening"""
    im, d = canvas(7, 5); r = random.Random(77)
    for (cx, w) in ((16, 14), (96, 14)):
        for y in range(24, 79):
            rx = w + (1 if y > 70 else 0) - (y < 30) * 2
            for x in range(int(cx - rx), int(cx + rx) + 1):
                dx = (x - cx) / rx; lit = -dx
                c = CHALK[3] if lit > 0.35 else CHALK[2] if lit > -0.35 else CHALK[1]
                if (y + x // 6) % 7 == 0: c = shade(c, 0.86)
                P(im, x, y, c)
            P(im, cx - rx - 1, y, CHALK[0]); P(im, cx + rx + 1, y, CHALK[0])
        for x in range(int(cx - w), int(cx + w)): P(im, x, 79, (0, 0, 0, 70))
    chalk_blob(im, 56, 20, 54, 17, r, lace=11)
    for x in range(32, 81):
        y = 34 + int(10 * math.sin(math.pi * (x - 32) / 48))
        for yy in range(y, 80): P(im, x, yy, CLEAR)
        P(im, x, y - 1, CHALK[0]); P(im, x, y - 2, CHALK[1])
    turf_cap(im, 4, 108, 3, r)
    for x in (10, 22, 90, 102):                                 # sea-pink tufts at the feet
        for k in range(3): P(im, x + k, 77, (240, 150, 180, 255)); P(im, x + k, 78, MOSS[1])
    return im, ['rrOOOrr', 'rrOOOrr', 'WWOOOWW', 'WW...WW', 'WW...WW']


# ------------------------------------------------------------------ landmarks and props
def wreckers_lamp():
    im, d = canvas(1, 3); r = random.Random(5)
    d.rectangle([7, 10, 8, 46], fill=WOOD[1]); d.line([7, 10, 7, 46], fill=WOOD[3])
    d.line([3, 9, 12, 9], fill=WOOD[0])
    d.rectangle([4, 2, 11, 9], fill=(56, 50, 48, 255)); d.rectangle([5, 3, 10, 8], fill=GLOW[1]); d.rectangle([6, 4, 9, 7], fill=GLOW[2])
    d.polygon([(3, 2), (8, -1), (12, 2)], fill=(70, 60, 56, 255))
    for k in range(6): P(im, 2 - k // 2, 5 + k, GLOW[0][:3] + (90,)); P(im, 13 + k // 2, 5 + k, GLOW[0][:3] + (90,))
    d.ellipse([3, 44, 12, 47], fill=(0, 0, 0, 70))
    return im, ['O', 'O', 'W']


def signal_pole():
    im, d = canvas(1, 3)
    d.rectangle([7, 4, 8, 46], fill=WOOD[1]); d.line([7, 4, 7, 46], fill=WOOD[3])
    d.line([2, 8, 13, 8], fill=WOOD[1]); d.line([2, 8, 2, 12], fill=(90, 90, 96, 255))
    d.rectangle([1, 12, 3, 16], fill=(80, 76, 72, 255)); P(im, 2, 14, GLOW[1])
    d.polygon([(8, 3), (15, 5), (8, 7)], fill=(190, 60, 60, 255))
    d.ellipse([3, 44, 12, 47], fill=(0, 0, 0, 70))
    return im, ['O', 'O', 'W']


def beacon():
    """the Saltmere Beacon (2x3): a dry-stone plinth with a timber cradle and a brazier fire on top"""
    im, d = canvas(2, 3); r = random.Random(9)
    for y in range(22, 46):
        for x in range(4, 28):
            c = STONE[2] if (x // 4 + (y // 3) % 2) % 2 else STONE[1]
            if (y % 3) == 0: c = STONE[0]
            P(im, x, y, c)
    d.rectangle([3, 21, 28, 46], outline=OUT)
    d.line([4, 22, 27, 22], fill=STONE[3])
    for x0 in (7, 22): d.line([x0, 8, x0 + (3 if x0 == 7 else -3), 21], fill=WOOD[1])
    d.rectangle([6, 8, 25, 12], fill=(60, 56, 56, 255), outline=OUT)
    for k in range(18):
        x = 7 + k; h = 4 + int(4 * abs(math.sin(k * 0.8)))
        for y in range(8 - h, 8): P(im, x, y, GLOW[2] if y > 8 - h // 2 else GLOW[1])
        P(im, x, 8 - h - 1, (230, 110, 50, 255))
    d.ellipse([2, 44, 29, 47], fill=(0, 0, 0, 70))
    return im, ['OO', 'WW', 'WW']


def stone_bench():
    im, d = canvas(2, 1)
    d.rectangle([2, 5, 29, 10], fill=CHALK[3], outline=OUT); d.line([3, 6, 28, 6], fill=CHALK[4])
    for x0 in (4, 24): d.rectangle([x0, 10, x0 + 3, 14], fill=CHALK[1], outline=OUT)
    for x in range(6, 26, 3): P(im, x, 8, CHALK[1]); P(im, x + 1, 8, CHALK[1])       # carved lace pattern
    d.line([2, 15, 29, 15], fill=(0, 0, 0, 60))
    return im, ['WW']


def roadstone():
    im, d = canvas(1, 2)
    d.polygon([(4, 4), (11, 4), (12, 28), (3, 28)], fill=STONE[2], outline=OUT)
    d.pieslice([4, 0, 11, 8], 180, 360, fill=STONE[2], outline=OUT)
    d.line([5, 5, 5, 27], fill=STONE[3])
    for k, y in enumerate((10, 15, 20)): d.line([6, y, 9, y], fill=STONE[0])
    for x in range(3, 13): P(im, x, 27, MOSS[1] if x % 2 else MOSS[0])
    d.ellipse([2, 27, 13, 30], fill=(0, 0, 0, 60))
    return im, ['O', 'W']


def shrine():
    """a wayside shrine (2x3): a stone niche under a little shingle roof, a lantern and tied ribbons"""
    im, d = canvas(2, 3)
    d.rectangle([5, 14, 26, 44], fill=STONE[2], outline=OUT); d.line([6, 15, 6, 43], fill=STONE[3])
    d.rectangle([10, 20, 21, 32], fill=(46, 40, 52, 255), outline=OUT)
    d.rectangle([14, 25, 17, 31], fill=GLOW[1]); P(im, 15, 26, GLOW[2])
    d.polygon([(1, 15), (16, 3), (30, 15)], fill=(110, 70, 60, 255), outline=OUT)
    for y in range(6, 15, 3): d.line([16 - (y - 3) * 15 // 12, y, 16 + (y - 3) * 14 // 12, y], fill=(90, 56, 50, 255))
    for x, c in ((8, (220, 60, 70, 255)), (24, (60, 90, 200, 255)), (12, (230, 200, 80, 255))):
        d.line([x, 16, x + 1, 24], fill=c)
    d.ellipse([3, 42, 28, 47], fill=(0, 0, 0, 70))
    return im, ['OO', 'WW', 'WW']


def drywall(kind):
    """drystone wall: stacked grey stones with moss on the coping (1x1; 'v' runs north-south)"""
    im = Image.new('RGBA', (16, 16), CLEAR); r = random.Random({'w': 1, 'm': 2, 'e': 3, 'v': 4}[kind])
    if kind == 'v':
        x0, x1, y0, y1 = 4, 11, 0, 15
    else:
        x0, x1, y0, y1 = (2 if kind == 'w' else 0), (13 if kind == 'e' else 15), 3, 13
    y = y0
    while y <= y1:
        x = x0 - r.randrange(2)
        while x <= x1:
            w = r.randrange(3, 6)
            c = r.choice(STONE[1:4])
            for xx in range(max(x0, x), min(x1, x + w - 1) + 1):
                for yy in range(y, min(y1, y + 2) + 1): P(im, xx, yy, c)
                P(im, xx, min(y1, y + 2), STONE[0])
            P(im, x + w - 1, y, STONE[0]) if x + w - 1 <= x1 else None
            x += w
        y += 3
    if kind != 'v':
        for x in range(x0, x1 + 1):
            P(im, x, y0, MOSS[1] if r.random() < 0.6 else STONE[3])
        for x in range(x0, x1 + 1): P(im, x, y1 + 1, (0, 0, 0, 60))
    return im


def column(fallen=False):
    if not fallen:
        im, d = canvas(1, 2)
        d.rectangle([4, 6, 11, 28], fill=CHALK[2], outline=OUT); d.line([5, 7, 5, 27], fill=CHALK[4])
        for x in (7, 9): d.line([x, 7, x, 27], fill=CHALK[1])
        d.polygon([(3, 6), (6, 2), (8, 4), (10, 1), (12, 6)], fill=CHALK[3], outline=OUT)
        d.rectangle([2, 27, 13, 30], fill=CHALK[1], outline=OUT)
        for x in range(3, 13, 2): P(im, x, 26, MOSS[1])
        return im, ['O', 'W']
    im, d = canvas(3, 1)
    d.rectangle([3, 3, 40, 11], fill=CHALK[2], outline=OUT); d.line([4, 4, 39, 4], fill=CHALK[4])
    for y in (6, 8): d.line([4, y, 39, y], fill=CHALK[1])
    d.ellipse([38, 2, 46, 12], fill=CHALK[3], outline=OUT); d.ellipse([40, 4, 44, 10], fill=CHALK[1])
    for x in range(4, 40, 3): P(im, x, 11, MOSS[1])
    d.line([3, 13, 44, 13], fill=(0, 0, 0, 60))
    return im, ['WWW']


def ruin():
    """a broken wall with an arch stub and fallen blocks (3x2): the old toll keep, chapel or mill"""
    im, d = canvas(3, 2); r = random.Random(33)
    top = [10, 6, 4, 8, 14, 18, 12, 9, 16, 20, 22, 24]
    for x in range(2, 46):
        t = top[min(11, x // 4)] + r.randrange(2)
        for y in range(t, 26):
            c = STONE[2] if ((x // 4) + (y // 3)) % 2 else STONE[1]
            if y % 3 == 0: c = STONE[0]
            P(im, x, y, c)
        P(im, x, t, MOSS[1] if r.random() < 0.6 else STONE[3]); P(im, x, t - 1, OUT)
    for x in range(14, 26):                                        # the arch stub
        y = 26 - int(9 * math.sin(math.pi * (x - 14) / 12))
        for yy in range(y, 27): P(im, x, yy, (40, 36, 44, 255))
    for (x, y) in ((34, 27), (40, 25), (8, 27)):
        d.rectangle([x, y, x + 4, y + 3], fill=STONE[2], outline=OUT)
    for x in range(2, 46): P(im, x, 26, (0, 0, 0, 50))
    for _ in range(10): P(im, r.randrange(2, 46), r.randrange(10, 25), MOSS[0])
    return im, ['OOO', 'WWW']


def hayrick():
    im, d = canvas(2, 2); r = random.Random(4)
    d.ellipse([2, 6, 29, 30], fill=(196, 168, 90, 255), outline=OUT)
    d.pieslice([4, 0, 27, 20], 180, 360, fill=(214, 186, 104, 255), outline=OUT)
    for _ in range(40):
        x, y = r.randrange(5, 27), r.randrange(4, 28)
        if im.getpixel((x, y))[3]: P(im, x, y, r.choice([(170, 140, 70, 255), (230, 204, 130, 255)]))
    d.line([4, 18, 27, 18], fill=(120, 96, 50, 255))
    d.ellipse([3, 28, 28, 31], fill=(0, 0, 0, 60))
    return im, ['OO', 'WW']


def sledge():
    im, d = canvas(2, 1)
    d.rectangle([4, 4, 27, 9], fill=WOOD[2], outline=OUT); d.line([5, 5, 26, 5], fill=WOOD[3])
    d.line([2, 11, 28, 11], fill=WOOD[0]); d.arc([0, 6, 6, 12], 90, 270, fill=WOOD[0])
    for x in (8, 22): d.line([x, 9, x, 11], fill=WOOD[1])
    d.line([3, 13, 28, 13], fill=(0, 0, 0, 60))
    return im, ['WW']


def chute(v):
    """the sledge run: a polished groove down the dune (walkable decal; the slide is an event)"""
    im = Image.new('RGBA', (16, 16), CLEAR)
    for y in range(16):
        for x in (4, 5, 10, 11):
            P(im, x + (v and y % 4 == 0), y, (170, 150, 100, 170))
        for x in range(6, 10): P(im, x, y, (236, 226, 180, 110))
    return im


# ------------------------------------------------------------------ silk (Gossamer Wood)
def drape(v):
    """silk hung from the canopy (2x3, overhead): translucent sheets with folds, frayed at the hem"""
    im, d = canvas(2, 3); r = random.Random(700 + v)
    for k in range(3 + v):
        x0 = 3 + k * (24 // (3 + v)); w = 6 + r.randrange(4); hem = 30 + r.randrange(16)
        for y in range(0, hem):
            sway = int(1.5 * math.sin(y * 0.12 + k))
            for x in range(x0 + sway, x0 + sway + w):
                c = SILK[3] if x == x0 + sway + 1 else SILK[2] if (x - x0) % 3 else SILK[1]
                P(im, x, y, c[:3] + (150 + (40 if y < 6 else 0),))
            if y == hem - 1:
                for x in range(x0 + sway, x0 + sway + w, 2): P(im, x, y + 1 + r.randrange(2), SILK[3][:3] + (140,))
    return im, ['OO', 'OO', 'OO']


def cocoons():
    im, d = canvas(1, 2); r = random.Random(3)
    d.line([8, 0, 8, 6], fill=SILK[2])
    for (x, y, h) in ((5, 6, 9), (9, 9, 11), (6, 18, 8)):
        d.ellipse([x - 3, y, x + 3, y + h], fill=SILK[2], outline=SILK[0])
        d.line([x - 1, y + 2, x - 1, y + h - 2], fill=SILK[3])
        for k in range(2, h, 3): d.line([x - 2, y + k, x + 2, y + k + 1], fill=SILK[1])
    return im, ['O', 'O']


def silk_rack():
    """a silk-drying rack (3x2): two posts, a crossbar, skeins of raw silk"""
    im, d = canvas(3, 2); r = random.Random(12)
    for x in (4, 42): d.rectangle([x, 4, x + 2, 30], fill=WOOD[1], outline=OUT)
    d.rectangle([3, 3, 45, 5], fill=WOOD[2], outline=OUT)
    for k in range(7):
        x = 9 + k * 5; h = 12 + r.randrange(8)
        c = SILK[2] if k % 3 else (232, 214, 170, 255)
        d.rectangle([x, 6, x + 3, 6 + h], fill=c, outline=SILK[0])
        d.line([x + 1, 7, x + 1, 5 + h], fill=SILK[3])
    d.line([3, 31, 46, 31], fill=(0, 0, 0, 60))
    return im, ['OOO', 'WWW']


def spool():
    im, d = canvas(2, 2)
    d.ellipse([3, 2, 28, 10], fill=WOOD[2], outline=OUT)
    d.rectangle([6, 6, 25, 24], fill=SILK[2], outline=SILK[0])
    for y in range(8, 24, 2): d.line([7, y, 24, y], fill=SILK[1 + (y // 2) % 2])
    d.ellipse([3, 20, 28, 28], fill=WOOD[1], outline=OUT); d.ellipse([4, 3, 27, 9], fill=WOOD[3])
    d.ellipse([2, 27, 29, 31], fill=(0, 0, 0, 60))
    return im, ['OO', 'WW']


def weft_bridge(row):
    """the Weft Bridge: a span of spun silk as thick as a road.  Three rows: north cable, deck, south cable"""
    im = Image.new('RGBA', (16, 16), CLEAR); r = random.Random({'n': 1, 'm': 2, 's': 3}[row])
    for y in range(16):
        for x in range(16):
            c = SILK[2] if (x + y * 2) % 6 else SILK[1]
            if (x - y) % 7 == 0: c = SILK[3]
            P(im, x, y, c)
    if row == 'n':
        for x in range(16): P(im, x, 0, SILK[0]); P(im, x, 1, SILK[3]); P(im, x, 2, SILK[1]); P(im, x, 3, SILK[0])
    if row == 's':
        for x in range(16): P(im, x, 12, SILK[0]); P(im, x, 13, SILK[3]); P(im, x, 14, SILK[1]); P(im, x, 15, (0, 0, 0, 90))
    return im


# ------------------------------------------------------------------ mechanics
def gust(v):
    im = Image.new('RGBA', (16, 16), CLEAR); r = random.Random(720 + v)
    for _ in range(3):
        x, y, L = r.randrange(0, 8), r.randrange(2, 14), r.randrange(5, 10)
        for k in range(L):
            P(im, x + k, y + (1 if k > L - 3 else 0), (250, 252, 255, 120 + 10 * k))
        P(im, x + L, y + 1, (250, 252, 255, 230))
    return im


def slab(col):
    im = Image.new('RGBA', (16, 16), CLEAR); d = ImageDraw.Draw(im)
    d.rectangle([2, 3, 13, 13], fill=col + (255,), outline=OUT)
    d.line([3, 4, 12, 4], fill=tuple(min(255, c + 60) for c in col) + (255,))
    d.line([2, 14, 13, 14], fill=(0, 0, 0, 70))
    return im


def sluice():
    im, d = canvas(1, 2)
    for x in (2, 12): d.rectangle([x, 2, x + 2, 30], fill=WOOD[1], outline=OUT)
    d.rectangle([4, 10, 12, 24], fill=WOOD[2], outline=OUT)
    for y in range(12, 24, 3): d.line([5, y, 11, y], fill=WOOD[3])
    d.ellipse([4, 0, 12, 6], fill=(90, 86, 84, 255), outline=OUT)
    return im, ['O', 'W']


def shoal(v):
    """the drowned cart road at low water: wet sand and ruts with a sheen of water (1x1, opaque; shown by an event at
    night over the channel, where its passage makes the cell walkable)"""
    im = Image.new('RGBA', (16, 16), SAND[1] + (255,)); r = random.Random(740 + v)
    for _ in range(26): P(im, r.randrange(16), r.randrange(16), SAND[0] + (255,))
    for _ in range(14): P(im, r.randrange(16), r.randrange(16), SAND[2] + (255,))
    for x in range(16):                                            # cart ruts
        P(im, x, 4 + (x // 6) % 2, (120, 108, 80, 255)); P(im, x, 11 + (x // 7) % 2, (120, 108, 80, 255))
    for _ in range(3):
        x, y = r.randrange(0, 11), r.randrange(1, 15)
        for k in range(r.randrange(3, 6)): P(im, x + k, y, (150, 190, 214, 200))
    return im


def mine_mouth():
    """a timbered mine mouth in a chalk face (3x3): the opening (middle column) is walkable, the warp stands in it"""
    im, d = canvas(3, 3)
    d.rectangle([6, 14, 41, 47], fill=(26, 22, 30, 255))
    for x0 in (4, 38): d.rectangle([x0, 12, x0 + 5, 47], fill=WOOD[2], outline=OUT); d.line([x0 + 1, 13, x0 + 1, 46], fill=WOOD[3])
    d.rectangle([2, 8, 45, 14], fill=WOOD[1], outline=OUT); d.line([3, 9, 44, 9], fill=WOOD[3])
    for x in range(10, 38, 6): d.line([x, 14, x + 3, 22], fill=(60, 50, 44, 255))
    for k in range(8): P(im, 18 + k * 2, 44 + (k % 2), (110, 104, 96, 255))      # rails
    for x in range(2, 46): P(im, x, 6 + (x % 3 == 0), CHALK[1])
    return im, ['OOO', 'WDW', 'WDW']


BRINES = {'brp': ((214, 150, 164), (236, 186, 196)),       # halophile pink: the oldest pans
          'brg': ((140, 172, 158), (172, 200, 186)),       # grey-green: fresh brine off the marsh
          'brx': ((198, 208, 218), (236, 240, 246))}       # crystallising: the salt is nearly ready to rake


def brine_col(v, key):
    """a salt pan of standing brine in one of the BRINES colours (1x1, its clay bund on the sides named in v)"""
    base, hi = BRINES[key]
    im = Image.new('RGBA', (16, 16), base + (255,)); d = ImageDraw.Draw(im); r = random.Random(400 + len(v) + ord(key[2]))
    for _ in range(8): P(im, r.randrange(16), r.randrange(16), hi + (255,))
    for _ in range(5 if key != 'brx' else 14): P(im, r.randrange(16), r.randrange(16), (246, 248, 250, 255))
    C1, C2 = (176, 150, 116, 255), (138, 112, 86, 255)
    if 'n' in v: d.rectangle([0, 0, 15, 2], fill=C1); d.line([0, 2, 15, 2], fill=C2)
    if 's' in v: d.rectangle([0, 13, 15, 15], fill=C1); d.line([0, 13, 15, 13], fill=(232, 236, 240, 255))
    if 'w' in v: d.rectangle([0, 0, 2, 15], fill=C1); d.line([2, 0, 2, 15], fill=C2)
    if 'e' in v: d.rectangle([13, 0, 15, 15], fill=C1); d.line([13, 0, 13, 15], fill=(232, 236, 240, 255))
    return im


def crust(v):
    """the grey salt crust of the Saltings (1x1 ground): grey-cream, crazed, glinting crystals, a little mud"""
    im = Image.new('RGBA', (16, 16), (204, 202, 194, 255)); r = random.Random(760 + v)
    for _ in range(4):
        x, y = r.randrange(16), r.randrange(16); L = r.randrange(3, 7); dx = r.choice((1, -1))
        for k in range(L): P(im, (x + k * dx) % 16, (y + k // 2) % 16, (168, 166, 160, 255))
    for _ in range(12): P(im, r.randrange(16), r.randrange(16), (232, 234, 236, 255))
    for _ in range(6): P(im, r.randrange(16), r.randrange(16), (186, 182, 172, 255))
    if v == 3:
        for _ in range(6): P(im, r.randrange(16), r.randrange(16), (150, 136, 112, 255))
    return im


def boardwalk(vertical):
    """a light timber boardwalk on posts (1x1, walkable): planks across the way of travel, a shadow on the water"""
    im = Image.new('RGBA', (16, 16), CLEAR); d = ImageDraw.Draw(im)
    W2 = [(126, 96, 66, 255), (166, 128, 88, 255), (196, 160, 112, 255)]
    if vertical:
        d.rectangle([2, 0, 13, 15], fill=W2[1])
        for y in range(0, 16, 4): d.line([2, y, 13, y], fill=W2[0]); d.line([2, y + 1, 13, y + 1], fill=W2[2])
        d.line([2, 0, 2, 15], fill=W2[0]); d.line([13, 0, 13, 15], fill=W2[0]); d.line([14, 0, 14, 15], fill=(0, 0, 0, 70))
    else:
        d.rectangle([0, 2, 15, 12], fill=W2[1])
        for x in range(0, 16, 4): d.line([x, 2, x, 12], fill=W2[0]); d.line([x + 1, 2, x + 1, 12], fill=W2[2])
        d.line([0, 2, 15, 2], fill=W2[2]); d.line([0, 12, 15, 12], fill=W2[0]); d.line([0, 13, 15, 13], fill=(0, 0, 0, 80))
    return im


def dye_cloth(col, v):
    """a drying line across the road (1x1, overhead: you walk under it): a sagging rope and a length of dyed cloth"""
    im = Image.new('RGBA', (16, 16), CLEAR); d = ImageDraw.Draw(im); r = random.Random(800 + v + sum(col))
    for x in range(16): P(im, x, 2 + (1 if 4 < x < 11 else 0), (90, 76, 60, 255))
    x0 = 2 + r.randrange(2); x1 = x0 + 10 + r.randrange(2); hem = 11 + r.randrange(4)
    lo = tuple(int(c * 0.72) for c in col); hi = tuple(min(255, int(c * 1.18) + 16) for c in col)
    for x in range(x0, x1):
        for y in range(3 + (1 if 4 < x < 11 else 0), hem + (x % 3 == 0)):
            P(im, x, y, (hi if x == x0 + 1 else lo if (x - x0) % 4 == 3 else col) + (235,))
    for x in (x0, x1 - 1): P(im, x, 3, (240, 236, 226, 255))                 # pegs
    return im


def dye_post():
    im = Image.new('RGBA', (16, 16), CLEAR); d = ImageDraw.Draw(im)
    d.rectangle([6, 0, 9, 14], fill=WOOD[1], outline=OUT); d.line([7, 1, 7, 13], fill=WOOD[3])
    d.line([0, 3, 15, 3], fill=(90, 76, 60, 255)); d.ellipse([4, 13, 11, 15], fill=(0, 0, 0, 70))
    return im


def stone_bridge(part):
    """an old stone bridge running north-south (1x1): 'm' the cobbled deck, 'w' / 'e' the parapets (solid)"""
    im = Image.new('RGBA', (16, 16), CLEAR); d = ImageDraw.Draw(im); r = random.Random({'m': 1, 'w': 2, 'e': 3}[part])
    if part == 'm':
        for y in range(0, 16, 4):
            off = 0 if (y // 4) % 2 else 2
            for x in range(-off, 16, 5):
                d.rectangle([x, y, x + 4, y + 3], fill=STONE[2] if r.random() < 0.7 else STONE[3], outline=STONE[1])
        return im
    x0 = 3 if part == 'w' else 2
    d.rectangle([x0, 0, x0 + 10, 15], fill=STONE[2], outline=OUT)
    for y in range(0, 16, 4): d.line([x0 + 1, y, x0 + 9, y], fill=STONE[1])
    d.line([x0 + 1, 0, x0 + 1, 15], fill=STONE[3])
    for _ in range(4): P(im, x0 + 2 + r.randrange(8), r.randrange(16), MOSS[1])
    if part == 'w': d.line([x0 + 11, 0, x0 + 11, 15], fill=(0, 0, 0, 70))
    return im


def bamboo():
    """a bamboo clump (2x3): pale green culms with nodes, leaf sprays at the top (overhead)"""
    im, d = canvas(2, 3); r = random.Random(17)
    for k in range(7):
        x = 3 + k * 4 + r.randrange(-1, 2); top = 2 + r.randrange(10)
        for y in range(top, 46):
            P(im, x, y, (110, 170, 80, 255)); P(im, x + 1, y, (150, 206, 110, 255)); P(im, x + 2, y, (70, 120, 60, 255))
            if (y - top) % 9 == 0: P(im, x, y, (60, 100, 50, 255)); P(im, x + 1, y, (60, 100, 50, 255)); P(im, x + 2, y, (60, 100, 50, 255))
        for _ in range(5):
            lx, ly = x + r.randrange(-4, 6), top + r.randrange(0, 14)
            for t in range(4): P(im, lx + t, ly + t // 2, (90, 160, 70, 255))
    d.ellipse([2, 43, 29, 47], fill=(0, 0, 0, 70))
    return im, ['OO', 'OO', 'WW']


def bellpost():
    """the Hale Bell (1x3): a ship's bell hung from a gallows post above the cliff, a cloth tied round its clapper"""
    im, d = canvas(1, 3)
    d.rectangle([6, 4, 9, 46], fill=WOOD[1], outline=OUT); d.line([7, 5, 7, 45], fill=WOOD[3])
    d.rectangle([1, 4, 14, 7], fill=WOOD[2], outline=OUT)
    d.line([3, 8, 3, 11], fill=(80, 76, 72, 255))
    d.polygon([(0, 20), (1, 12), (5, 11), (6, 12), (7, 20)], fill=(196, 152, 64, 255), outline=(110, 80, 40, 255))
    d.line([1, 13, 1, 19], fill=(240, 210, 120, 255))
    d.rectangle([2, 20, 5, 23], fill=(232, 228, 216, 255))                # the cloth on the clapper
    d.ellipse([3, 44, 12, 47], fill=(0, 0, 0, 70))
    return im, ['O', 'O', 'W']


def pieces():
    """name -> (image, code rows, door): appended by rcustom (rdraw.pieces_late4)"""
    D.CODE.update(CODES)
    out = {}
    for e in 'wme':
        out['lg_' + e] = (ledge(e), ['L'], None)
        out['lgc_' + e] = (ledge(e, face=CHALK), ['L'], None)
        out['lgd_' + e] = (ledge(e, face=SANDF), ['L'], None)
    for n, im in wet_shapes().items(): out[n] = (im, ['V'], None)
    for v in range(4): out['cs_wrack%d' % v] = (wrack(v), ['V'], None)
    for v in range(2): out['cs_shell%d' % v] = (shell(v), ['V'], None)
    for v in range(3): out['cs_wrock%d' % v] = (wrock(v), ['X'], None)
    for v in range(2): out['cs_wrockb%d' % v] = (wrock(v + 1, chalk=False), ['X'], None)
    for v in range(2): out['cs_kelp%d' % v] = (kelp(v), ['O'], None)
    out['cs_pool_a'] = (rock_pool(3, 2, 41), ['XXX', 'XXX'], None)
    out['cs_pool_b'] = (rock_pool(2, 2, 42), ['XX', 'XX'], None)
    out['cs_pool_c'] = (rock_pool(4, 3, 43), ['XXXX', 'XXXX', 'XXXX'], None)
    im, c = sea_arch(); out['pf_seaarch'] = (im, c, None)
    im, c = sea_stack(); out['pf_seastack'] = (im, c, None)
    im, c = sea_stack(95); out['pf_seastack2'] = (im, c, None)
    im, c = lace_arch(); out['pf_lacearch'] = (im, c, None)
    im, c = wreckers_lamp(); out['pf_wlamp'] = (im, c, None)
    im, c = signal_pole(); out['pf_sigpole'] = (im, c, None)
    im, c = beacon(); out['pf_beacon'] = (im, c, None)
    im, c = stone_bench(); out['pf_stonebench'] = (im, c, None)
    im, c = roadstone(); out['pf_roadstone'] = (im, c, None)
    im, c = shrine(); out['pf_shrine'] = (im, c, None)
    for k in 'wmev': out['nr_wall_' + k] = (drywall(k), ['W'], None)
    im, c = column(); out['nr_col'] = (im, c, None)
    im, c = column(True); out['nr_colfall'] = (im, c, None)
    im, c = ruin(); out['nr_ruin'] = (im, c, None)
    im, c = hayrick(); out['pf_hayrick'] = (im, c, None)
    im, c = sledge(); out['pf_sledge'] = (im, c, None)
    for v in range(2): out['mr_chute%d' % v] = (chute(v), ['V'], None)
    for v in range(2):
        im, c = drape(v); out['gw_drape%d' % v] = (im, c, None)
    im, c = cocoons(); out['gw_cocoons'] = (im, c, None)
    im, c = silk_rack(); out['gw_rack'] = (im, c, None)
    im, c = spool(); out['gw_spool'] = (im, c, None)
    out['gw_bridge_n'] = (weft_bridge('n'), ['B'], None)
    out['gw_bridge_m'] = (weft_bridge('m'), ['K'], None)
    out['gw_bridge_s'] = (weft_bridge('s'), ['C'], None)
    for v in range(3): out['fw_gust%d' % v] = (gust(v), ['O'], None)
    for v in range(2): out['cs_shoal%d' % v] = (shoal(v), ['F'], None)
    im, c = mine_mouth(); out['pf_minemouth'] = (im, c, None)
    for key in BRINES:
        for v in ('', 'n', 's', 'w', 'e', 'nw', 'ne', 'sw', 'se', 'ns', 'we'):
            out['%s_%s' % (key, v or 'c')] = (brine_col(v, key), ['W'], None)
    for v in range(4): out['gs_crust%d' % v] = (crust(v), ['G'], None)
    out['bw_h'] = (boardwalk(False), ['D'], None); out['bw_v'] = (boardwalk(True), ['D'], None)
    for nm, col in (('r', (196, 52, 64)), ('b', (52, 84, 186)), ('y', (228, 196, 60))):
        for v in range(2): out['dl_cloth_%s%d' % (nm, v)] = (dye_cloth(col, v), ['O'], None)
    out['dl_post'] = (dye_post(), ['W'], None)
    out['sb_m'] = (stone_bridge('m'), ['D'], None); out['sb_w'] = (stone_bridge('w'), ['W'], None); out['sb_e'] = (stone_bridge('e'), ['W'], None)
    im, c = bamboo(); out['pf_bamboo'] = (im, c, None)
    im, c = bellpost(); out['pf_bellpost'] = (im, c, None)
    for nm, col in (('r', (196, 52, 64)), ('b', (52, 84, 186)), ('y', (228, 196, 60))):
        out['df_slab_' + nm] = (slab(col), ['F'], None)
    im, c = sluice(); out['df_sluice'] = (im, c, None)
    return out


if __name__ == '__main__':
    ps = pieces()
    ims = [(n, im.resize((im.width * 2, im.height * 2), Image.NEAREST)) for n, (im, c, dr) in ps.items() if not n.startswith('cs_wet_') or n.endswith(('_00', '_15', '_33', '_46'))]
    Wd = 1400; x = y = 0; rowh = 0; pos = []
    for n, im in ims:
        if x + im.width > Wd: x = 0; y += rowh + 14; rowh = 0
        pos.append((n, im, x, y)); x += im.width + 10; rowh = max(rowh, im.height)
    sheet = Image.new('RGBA', (Wd, y + rowh + 14), (112, 200, 160, 255))
    dr = ImageDraw.Draw(sheet)
    for n, im, x, y in pos:
        if n.startswith(('cs_w', 'cs_k', 'pf_sea')):
            bg = Image.new('RGBA', im.size, (72, 120, 216, 255)); bg.alpha_composite(im); im = bg
        elif n.startswith(('cs_', 'mr_')):
            bg = Image.new('RGBA', im.size, (216, 211, 162, 255)); bg.alpha_composite(im); im = bg
        sheet.alpha_composite(im, (x, y + 12)); dr.text((x, y), n, fill=(120, 0, 60, 255))
    sheet.save(sys.argv[1] if len(sys.argv) > 1 else '/tmp/ndraw.png'); print(sheet.size)
