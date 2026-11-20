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


def snow_ground(v):
    """snow ground variants (1x1, ground layer) matching Kristiline's snow (232,232,240): wind ripples, sparkle, a
    shadow dip, footprint-free"""
    base = (232, 232, 240)
    im = Image.new('RGBA', (16, 16), base + (255,)); r = random.Random(860 + v)
    if v == 0:
        for k in range(3):
            y = 3 + k * 5 + r.randrange(2)
            for x in range(16): P(im, x, y + int(math.sin(x * 0.6 + k) * 0.8), (220, 224, 236, 255))
    elif v == 1:
        for _ in range(9): P(im, r.randrange(16), r.randrange(16), (250, 252, 255, 255))
        for _ in range(4): P(im, r.randrange(16), r.randrange(16), (200, 224, 232, 255))
    elif v == 2:
        for y in range(16):
            for x in range(16):
                if ((x - 8) / 7.0) ** 2 + ((y - 9) / 5.0) ** 2 < 1: P(im, x, y, (224, 226, 238, 255))
        for x in range(4, 12): P(im, x, 4, (244, 246, 252, 255))
    else:
        for _ in range(6):
            x, y = r.randrange(14), r.randrange(15)
            P(im, x, y, (214, 220, 234, 255)); P(im, x + 1, y, (244, 246, 252, 255))
    return im


def fleece_cross():
    """the Fleece Cross (2x3): an old stone market cross on a stepped plinth, hung with yarn ribbons in every colour"""
    im, d = canvas(2, 3); r = random.Random(29)
    d.rectangle([4, 38, 27, 46], fill=STONE[1], outline=OUT); d.rectangle([7, 33, 24, 38], fill=STONE[2], outline=OUT)
    d.line([5, 39, 26, 39], fill=STONE[3]); d.line([8, 34, 23, 34], fill=STONE[3])
    d.rectangle([13, 6, 18, 33], fill=STONE[2], outline=OUT); d.line([14, 7, 14, 32], fill=STONE[3])
    d.rectangle([7, 10, 24, 15], fill=STONE[2], outline=OUT); d.line([8, 11, 23, 11], fill=STONE[3])
    cols = [(196, 52, 64), (52, 84, 186), (228, 196, 60), (240, 240, 236), (120, 180, 90), (200, 120, 200)]
    for k in range(9):
        x = 6 + k * 2 + r.randrange(2); y0 = 14 + r.randrange(3); L = 6 + r.randrange(12)
        c = r.choice(cols)
        for y in range(y0, y0 + L): P(im, x + (1 if (y - y0) % 5 == 4 else 0), y, c + (255,))
    for k in range(4): P(im, 15 + k - 2, 20 + k * 3, (240, 240, 236, 255))
    d.ellipse([3, 45, 28, 47], fill=(0, 0, 0, 60))
    return im, ['OO', 'OO', 'WW']


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
    for v in range(4): out['sn_g%d' % v] = (snow_ground(v), ['G'], None)
    im, c = fleece_cross(); out['pf_fleececross'] = (im, c, None)
    for nm, col in (('r', (196, 52, 64)), ('b', (52, 84, 186)), ('y', (228, 196, 60))):
        out['df_slab_' + nm] = (slab(col), ['F'], None)
    im, c = sluice(); out['df_sluice'] = (im, c, None)
    for v in range(2): im, c = waterwheel(v); out['eb_wheel%d' % v] = (im, c, None)
    im, c = lattice_intake(); out['eb_intake'] = (im, c, None)
    out.update(crystals())
    for v in range(2): out['bl_veil%d' % v] = (bleed_veil(v), ['V'], None)
    for v in range(3): out['bl_gust%d' % v] = (frozen_gust(v), ['V'], None)
    im, c = tipped_wagon(); out['pf_wagon'] = (im, c, None)
    # the war theatre (map builder 10)
    out['wr_tent_r'] = (tent(RED), ['OOO', 'WWW', 'WDW'][:0] or ['OOO', 'WWW', 'WWW'], None)
    out['wr_tent_b'] = (tent(BLUE), ['OOO', 'WWW', 'WWW'], None)
    out['wr_tent_w'] = (tent(CANVAS_W), ['OOO', 'WWW', 'WWW'], None)
    out['wr_tent_bone'] = (tent(BONE, stripe=(150, 140, 120, 255)), ['OOO', 'WWW', 'WWW'], None)
    im, c = war_tent(); out['wr_wartent'] = (im, c, (2, 3))
    im, c = trebuchet(); out['wr_trebuchet'] = (im, c, None)
    im, c = dragon_picket(); out['wr_picket'] = (im, c, None)
    im, c = sled_fort(); out['wr_sledfort'] = (im, c, None)
    im, c = sled_fort(False); out['wr_sledfort2'] = (im, c, None)
    for nm, cols, em in (('wr_ban_ash', RED, 'dragon'), ('wr_ban_ise', BLUE, 'whale'), ('wr_ban_bone', BONE, 'bone')):
        im, c = banner(cols, em); out[nm] = (im, c, None)
    im, c = caravan_well(); out['wr_well'] = (im, c, None)
    im, c = bone_cart(); out['wr_bonecart'] = (im, c, None)
    im, c = tally_wall(); out['wr_tally'] = (im, c, None)
    im, c = tripod(); out['wr_tripod'] = (im, c, None)
    im, c = dial_box(); out['wr_dial'] = (im, c, None)
    im, c = telegraph(); out['wr_telegraph'] = (im, c, None)
    for v in range(2): out['wr_trench%d' % v] = (trench(v), ['V'], None)
    for v in range(3): out['wr_ember%d' % v] = (embers(v), ['V'], None)
    for v in range(3): out['wr_frost%d' % v] = (frost_crust(v), ['V'], None)
    for v in range(3): out['wr_steam%d' % v] = (steam(v), ['V'], None)
    for v in range(3): out['wr_ripple%d' % v] = (ripple(v), ['V'], None)
    for v in range(2): out['wr_bones%d' % v] = (bones(v), ['V'], None)
    for v in range(2): out['wr_rut%d' % v] = (rut(v), ['V'], None)
    return out



# ------------------------------------------------------------------ Ebbmouth (map builder 10, job 5)
def waterwheel(phase):
    """an undershot mill-wheel (3x3) standing in the race against its mill wall: a double timber rim, eight spokes round
    an iron hub, twelve paddles; phase 1 is turned half a paddle (two frames read as a wheel that turns)"""
    im, d = canvas(3, 3); cx, cy, R = 24, 22, 19
    a0 = math.pi / 12 * phase
    for k in range(12):                                                   # paddles, radial boards past the rim
        a = a0 + k * math.pi / 6
        x0, y0 = cx + (R - 3) * math.cos(a), cy + (R - 3) * math.sin(a)
        x1, y1 = cx + (R + 4) * math.cos(a), cy + (R + 4) * math.sin(a)
        d.line([x0, y0, x1, y1], fill=WOOD[0], width=4); d.line([x0, y0, x1, y1], fill=WOOD[2], width=2)
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=WOOD[0], width=5)
    d.ellipse([cx - R + 1, cy - R + 1, cx + R - 1, cy + R - 1], outline=WOOD[2], width=3)
    d.ellipse([cx - R + 2, cy - R + 2, cx + R - 2, cy + R - 2], outline=WOOD[3], width=1)
    for k in range(8):                                                    # spokes
        a = a0 + k * math.pi / 4
        d.line([cx, cy, cx + (R - 4) * math.cos(a), cy + (R - 4) * math.sin(a)], fill=WOOD[0], width=3)
        d.line([cx, cy, cx + (R - 4) * math.cos(a), cy + (R - 4) * math.sin(a)], fill=WOOD[2], width=1)
    disc(im, cx, cy, 4, (60, 62, 72, 255)); disc(im, cx - 1, cy - 1, 2, (140, 144, 156, 255))
    for x in range(2, 46):                                                # the race's white water churned at the foot
        if (x + phase * 3) % 5 < 3: P(im, x, 44, (236, 246, 252, 220)); P(im, x + 1, 45, (184, 216, 248, 170))
        if (x * 7 + phase) % 9 < 2: P(im, x, 46, (236, 246, 252, 150))
    return im, ['OOO', 'XXX', 'XXX']


def lattice_intake():
    """Meridian Tidal Lattice Unit 2 (3x2): a brass intake housing on the bank, a glass dial, ribbed pipes into the water,
    a sunburst plate bolted on"""
    im, d = canvas(3, 2)
    BR = [(92, 66, 30, 255), (150, 112, 44, 255), (206, 164, 72, 255), (244, 214, 128, 255)]
    d.rectangle([3, 4, 44, 26], fill=BR[1], outline=OUT)
    d.rectangle([4, 5, 43, 8], fill=BR[2]); d.line([4, 5, 43, 5], fill=BR[3])
    for x in range(8, 42, 6): d.line([x, 9, x, 25], fill=BR[0])
    disc(im, 24, 16, 6, (60, 70, 86, 255)); disc(im, 24, 16, 5, (150, 214, 236, 255)); d.line([24, 16, 27, 12], fill=(200, 60, 60, 255))
    for x in (8, 38): d.rectangle([x, 26, x + 3, 31], fill=BR[1], outline=OUT); d.line([x + 1, 26, x + 1, 31], fill=BR[3])
    d.polygon([(10, 12), (14, 10), (14, 14)], fill=BR[3])
    d.ellipse([2, 28, 45, 31], fill=(0, 0, 0, 60))
    return im, ['OOO', 'WWW']


# ------------------------------------------------------------------ job 6 imports and the Rehearsal (568)
CRYSTAL_COLS = ['blue', 'purple', 'pink', 'red', 'orange', 'yellow', 'green', 'teal']


def crystals():
    """J-Treecko252's Crystal Tiles (x2 art, art/imports/crystals_jtreecko252.png), halved to the 16-px grid: per colour
    a rounded crystal (1x2), a tall pillar (1x2, its top overhead) and a spiky cluster (1x1); clear and grey variants"""
    src = Image.open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'art', 'imports', 'crystals_jtreecko252.png')).convert('RGBA')
    half = lambda cx, cy, h=1: src.crop((cx * 32, cy * 32, cx * 32 + 32, cy * 32 + 32 * h)).resize((16, 16 * h), Image.NEAREST)
    out = {}
    for i, c in enumerate(CRYSTAL_COLS):
        out['cr_%s_e' % c] = (half(i, 0, 2), ['O', 'W'], None)      # rounded crystal (1x2, mostly the lower tile)
        out['cr_%s_t' % c] = (half(i, 2, 2), ['O', 'W'], None)      # tall pillar (1x2)
        out['cr_%s_c' % c] = (half(i, 4), ['W'], None)              # spiky cluster (1x1)
    out['cr_clear_t'] = (half(0, 5, 2), ['O', 'W'], None)
    out['cr_clear_e'] = (half(1, 5, 2), ['O', 'W'], None)
    out['cr_clear_c'] = (half(2, 5), ['W'], None)
    out['cr_grey_c'] = (half(2, 6), ['W'], None)
    out['cr_grey_t'] = (half(3, 5, 2), ['O', 'W'], None)
    out['cr_grey_e'] = (half(4, 5, 2), ['O', 'W'], None)
    return out


def bleed_veil(v):
    """the Bleed Veil's shimmer (a walk-through decal on the top layer): thin iridescent threads, pink to teal"""
    im = Image.new('RGBA', (16, 16), CLEAR); r = random.Random(880 + v)
    cols = [(255, 140, 200), (190, 150, 255), (130, 220, 240), (255, 230, 250)]
    for k in range(4):
        x = (k * 4 + v * 2 + r.randrange(2)) % 16
        for y in range(16):
            xx = x + (1 if (y + k + v) % 6 < 2 else 0)
            P(im, xx, y, cols[(y // 4 + k) % 4] + (70 + 40 * ((y + k) % 3),))
    return im


def frozen_gust(v):
    """salt spray stopped mid-gust: a curl of white droplets hanging in the air (decal, walk-through)"""
    im = Image.new('RGBA', (16, 16), CLEAR); r = random.Random(900 + v)
    cx, cy = 3 + r.randrange(4), 4 + r.randrange(6)
    for k in range(10):
        a = k * 0.55; rr = 1.5 + k * 0.6
        x, y = cx + rr * math.cos(a) + k * 0.6, cy + rr * math.sin(a) * 0.6
        P(im, int(x), int(y), (250, 252, 255, 230)); P(im, int(x) + 1, int(y), (220, 230, 245, 140))
    for _ in range(5): P(im, r.randrange(16), r.randrange(16), (255, 255, 255, 200))
    return im


def tipped_wagon():
    """the Rehearsal's wagon, tipped on its side in the wheel-rut (3x2): the bed on edge, one wheel in the air, spilled
    salt sacks"""
    im, d = canvas(3, 2)
    d.polygon([(4, 6), (40, 2), (44, 22), (8, 27)], fill=WOOD[2], outline=OUT)
    for k in range(5): d.line([6 + k * 8, 5 - k, 9 + k * 8, 25 - k], fill=WOOD[1])
    d.line([5, 15, 42, 11], fill=WOOD[3])
    d.ellipse([30, 0, 44, 14], outline=WOOD[0], width=2); d.line([37, 1, 37, 13], fill=WOOD[1]); d.line([31, 7, 43, 7], fill=WOOD[1])
    disc(im, 37, 7, 1, (70, 70, 80, 255))
    for x, y in ((10, 26), (18, 27), (26, 25)):
        d.ellipse([x - 4, y - 3, x + 4, y + 3], fill=(214, 200, 168, 255), outline=(150, 130, 100, 255))
    d.ellipse([4, 27, 46, 31], fill=(0, 0, 0, 60))
    return im, ['OOO', 'WWW']


# ------------------------------------------------------------------ the war theatre (920-930), map builder 10
RED = [(92, 24, 28, 255), (150, 40, 40, 255), (196, 72, 56, 255), (232, 120, 84, 255)]
BLUE = [(30, 48, 92, 255), (52, 86, 150, 255), (96, 134, 196, 255), (176, 204, 236, 255)]
BONE = [(150, 140, 120, 255), (196, 188, 166, 255), (226, 220, 202, 255), (248, 246, 236, 255)]
CANVAS_W = [(140, 132, 118, 255), (186, 178, 160, 255), (222, 216, 198, 255), (244, 240, 228, 255)]


def tent(cols, w=3, h=3, door=True, stripe=None):
    """a ridge tent seen from the south: roof in two pitches, a flap door, guy ropes and pegs"""
    im, d = canvas(w, h); W, Hh = w * 16, h * 16
    top, eave = 6, Hh - 14
    d.polygon([(2, eave), (W // 2, top), (W - 3, eave)], fill=cols[1], outline=OUT)
    d.polygon([(W // 2, top), (W - 3, eave), (W // 2 + 2, eave)], fill=cols[0])
    d.line([2, eave, W // 2, top], fill=cols[3]); d.line([W // 2, top, W // 2, eave], fill=cols[2])
    d.rectangle([4, eave, W - 5, Hh - 3], fill=cols[2], outline=OUT)
    if stripe: d.rectangle([4, eave + 2, W - 5, eave + 3], fill=stripe)
    if door:
        d.polygon([(W // 2 - 5, Hh - 3), (W // 2, eave - 4), (W // 2 + 5, Hh - 3)], fill=(40, 30, 30, 255))
        d.line([W // 2 - 5, Hh - 3, W // 2, eave - 4], fill=cols[3])
    for x0, x1 in ((2, 0), (W - 3, W - 1)): d.line([x0, eave + 1, x1, Hh - 1], fill=(120, 100, 80, 255))
    d.line([W // 2, top, W // 2, top - 5], fill=WOOD[0]); P(im, W // 2, top - 6, cols[3])
    d.ellipse([2, Hh - 4, W - 3, Hh - 1], fill=(0, 0, 0, 50))
    return im


def war_tent():
    """the Dominar's war-tent (5x4): red lacquer and gold, a great flap door (the door to 928), dragon standards"""
    im = tent(RED, 5, 4, stripe=(214, 170, 60, 255))
    d = ImageDraw.Draw(im)
    for x in (6, 72):
        d.line([x, 4, x, 60], fill=WOOD[0], width=2); d.polygon([(x, 4), (x + 8, 7), (x, 11)], fill=(214, 170, 60, 255))
    return im, ['OOOOO', 'OOOOO', 'WWWWW', 'WWDWW']


def trebuchet():
    """a legion trebuchet (3x3): A-frame, throwing arm cocked back, sling, counterweight crate"""
    im, d = canvas(3, 3)
    d.polygon([(8, 44), (24, 14), (40, 44)], outline=WOOD[0]); d.line([9, 44, 24, 15], fill=WOOD[1], width=3); d.line([39, 44, 24, 15], fill=WOOD[1], width=3)
    d.line([4, 44, 44, 44], fill=WOOD[0], width=3); d.line([14, 34, 34, 34], fill=WOOD[1], width=2)
    d.line([24, 16, 6, 4], fill=WOOD[2], width=3); d.line([24, 16, 34, 24], fill=WOOD[2], width=3)
    d.rectangle([30, 22, 40, 32], fill=(90, 80, 74, 255), outline=OUT)
    d.line([6, 4, 4, 14], fill=(160, 150, 130, 255)); d.ellipse([1, 13, 7, 18], fill=(110, 100, 90, 255))
    disc(im, 24, 16, 2, (70, 70, 80, 255))
    d.ellipse([3, 43, 45, 47], fill=(0, 0, 0, 60))
    return im, ['OOO', 'OOO', 'WWW']


def dragon_picket():
    """a dragon picket (1x2): an iron post with a heavy chain lying in scorched sand"""
    im, d = canvas(1, 2)
    d.rectangle([6, 4, 9, 28], fill=(60, 60, 70, 255), outline=OUT); d.line([7, 5, 7, 27], fill=(120, 120, 134, 255))
    d.ellipse([4, 1, 11, 6], fill=(214, 170, 60, 255), outline=OUT)
    for k in range(5): d.ellipse([9 + k, 22 + (k % 2), 12 + k, 25 + (k % 2)], outline=(90, 90, 100, 255))
    d.ellipse([1, 27, 15, 31], fill=(40, 30, 28, 110))
    return im, ['O', 'W']


def sled_fort(burnt=True):
    """a sled-fort dragged overland (3x2): a timber stockade on runners, scorched black where dragonfire caught it"""
    im, d = canvas(3, 2)
    for i, x in enumerate(range(3, 45, 5)):
        top = 4 + (i % 2) * 2
        c = (40, 34, 32, 255) if burnt and i % 3 != 1 else WOOD[2]
        d.rectangle([x, top, x + 4, 24], fill=c, outline=OUT); d.polygon([(x, top), (x + 2, top - 3), (x + 4, top)], fill=c)
    d.line([1, 27, 46, 27], fill=WOOD[0], width=2); d.arc([0, 22, 6, 30], 90, 270, fill=WOOD[0])
    if burnt:
        for k in range(6): P(im, 8 + k * 6, 3 + k % 3, (255, 140, 60, 200))
    d.ellipse([2, 28, 46, 31], fill=(0, 0, 0, 60))
    return im, ['OOO', 'WWW']


def banner(cols, emblem):
    """a war banner on a pole (1x3): Ashkaar's red dragon, Isenmar's blue whale, the bone-carters' white"""
    im, d = canvas(1, 3)
    d.line([3, 2, 3, 46], fill=WOOD[0], width=2)
    d.rectangle([4, 4, 14, 22], fill=cols[1], outline=OUT); d.polygon([(4, 22), (9, 27), (14, 22)], fill=cols[1], outline=OUT)
    d.line([5, 5, 13, 5], fill=cols[3])
    if emblem == 'dragon': d.polygon([(6, 16), (9, 8), (12, 16), (9, 13)], fill=(214, 170, 60, 255))
    elif emblem == 'whale': d.ellipse([6, 10, 13, 15], fill=cols[3]); d.polygon([(6, 12), (5, 9), (7, 11)], fill=cols[3])
    else: d.ellipse([7, 9, 11, 13], fill=BONE[0]); d.line([9, 13, 9, 19], fill=BONE[0]); d.line([7, 16, 11, 16], fill=BONE[0])
    d.ellipse([0, 44, 8, 47], fill=(0, 0, 0, 60))
    return im, ['O', 'O', 'W']


def caravan_well():
    """a caravan well (2x2): a ring of sandstone, a timber sweep, a bucket; the bone-carters' ribbon on the post"""
    im, d = canvas(2, 2)
    d.ellipse([3, 12, 28, 29], fill=(176, 146, 104, 255), outline=OUT); d.ellipse([7, 15, 24, 25], fill=(40, 52, 70, 255))
    d.line([6, 14, 25, 14], fill=(214, 186, 140, 255))
    d.line([27, 28, 27, 4], fill=WOOD[1], width=2); d.line([10, 2, 30, 8], fill=WOOD[2], width=2)
    d.rectangle([9, 2, 12, 7], fill=WOOD[0]); P(im, 28, 9, BONE[3]); P(im, 29, 10, BONE[3])
    d.ellipse([2, 28, 30, 31], fill=(0, 0, 0, 60))
    return im, ['OO', 'WW']


def bone_cart():
    """a burial cart (2x2): a two-wheeled handcart under white cloth, a bone-white pennant"""
    im, d = canvas(2, 2)
    d.rectangle([3, 10, 26, 21], fill=WOOD[2], outline=OUT); d.polygon([(4, 10), (14, 3), (25, 10)], fill=BONE[2], outline=OUT)
    d.line([5, 9, 24, 9], fill=BONE[3])
    for cx in (8, 21): d.ellipse([cx - 5, 17, cx + 5, 28], outline=WOOD[0], width=2); disc(im, cx, 22, 1, WOOD[0])
    d.line([27, 18, 31, 22], fill=WOOD[1], width=2); d.line([4, 2, 4, 12], fill=WOOD[0]); d.polygon([(5, 2), (10, 4), (5, 6)], fill=BONE[3])
    d.ellipse([2, 28, 30, 31], fill=(0, 0, 0, 60))
    return im, ['OO', 'WW']


def tally_wall():
    """the tally-wall of names (3x2): whitewashed mud brick, names in charcoal, bone tokens hung on nails"""
    im, d = canvas(3, 2); r = random.Random(71)
    d.rectangle([2, 6, 45, 28], fill=BONE[2], outline=OUT); d.line([3, 7, 44, 7], fill=BONE[3])
    for y in range(10, 26, 3):
        x = 5
        while x < 42:
            L = r.randrange(3, 7); d.line([x, y, x + L, y], fill=(70, 66, 62, 255)); x += L + 2
    for x in range(6, 44, 7): P(im, x, 8, BONE[0]); P(im, x, 9, BONE[1])
    d.ellipse([2, 28, 46, 31], fill=(0, 0, 0, 60))
    return im, ['OOO', 'WWW']


def tripod():
    """a Meridian brass survey tripod (1x2) with a lens head"""
    im, d = canvas(1, 2)
    for x1 in (2, 8, 14): d.line([8, 8, x1, 30], fill=(150, 112, 44, 255))
    d.rectangle([5, 3, 11, 9], fill=(206, 164, 72, 255), outline=OUT); disc(im, 8, 6, 1, (150, 214, 236, 255))
    d.ellipse([1, 28, 15, 31], fill=(0, 0, 0, 50))
    return im, ['O', 'W']


def dial_box():
    im, d = canvas(1, 1)
    d.rectangle([2, 4, 13, 14], fill=(150, 112, 44, 255), outline=OUT); disc(im, 7, 9, 3, (230, 232, 220, 255)); d.line([7, 9, 9, 7], fill=(200, 60, 60, 255))
    return im, ['W']


def telegraph():
    """a field-telegraph pole (1x3): crossbar, glass insulators, a wire sagging off east"""
    im, d = canvas(1, 3)
    d.line([7, 4, 7, 46], fill=WOOD[1], width=2); d.line([1, 7, 14, 7], fill=WOOD[0], width=2)
    for x in (2, 12): P(im, x, 5, (150, 214, 236, 255)); P(im, x, 6, (150, 214, 236, 255))
    d.line([12, 6, 16, 9], fill=(40, 40, 40, 255))
    d.ellipse([3, 44, 11, 47], fill=(0, 0, 0, 60))
    return im, ['O', 'O', 'W']


def trench(v):
    """frozen trench-line (decal on the top layer: the trench's white rim of frozen sand and its shadowed cut)"""
    im = Image.new('RGBA', (16, 16), CLEAR); r = random.Random(950 + v)
    for x in range(16):
        P(im, x, 4, (240, 246, 252, 230)); P(im, x, 5, (210, 224, 240, 220))
        for y in range(6, 12): P(im, x, y, (70, 84, 104, 150 + (y - 6) * 8))
        P(im, x, 12, (220, 232, 244, 200))
    for _ in range(6): P(im, r.randrange(16), r.randrange(3, 13), (255, 255, 255, 230))
    return im


def embers(v):
    """scorch and embers on the sand (decal): black glass streaks, a few live coals"""
    im = Image.new('RGBA', (16, 16), CLEAR); r = random.Random(960 + v)
    for _ in range(3):
        x, y, L = r.randrange(0, 10), r.randrange(2, 14), r.randrange(4, 9)
        for k in range(L): P(im, x + k, y + (k // 4), (40, 30, 32, 150)); P(im, x + k, y + 1 + (k // 4), (70, 50, 46, 90))
    for _ in range(3): P(im, r.randrange(16), r.randrange(16), (255, 140, 60, 230))
    return im


def frost_crust(v):
    """rime on sand (decal): white frost feathers"""
    im = Image.new('RGBA', (16, 16), CLEAR); r = random.Random(970 + v)
    for _ in range(4):
        x, y = r.randrange(16), r.randrange(16)
        for k in range(r.randrange(3, 6)):
            P(im, x + k, y - k // 2, (244, 250, 255, 210)); P(im, x + k, y + k // 2, (214, 232, 248, 170))
    return im


def steam(v):
    """the Steamline's wall of steam (decal, walk-through): drifting white columns with an iridescent Bleed edge"""
    im = Image.new('RGBA', (16, 16), CLEAR); r = random.Random(980 + v)
    for _ in range(26):
        x, y = r.randrange(16), r.randrange(16)
        P(im, x, y, (250, 252, 255, 90 + r.randrange(70)))
    for y in range(16):
        x = int(8 + 4 * math.sin((y + v * 5) / 3.0)); P(im, x, y, (255, 200, 236, 110)); P(im, x + 1, y, (190, 240, 250, 90))
    return im


def ripple(v):
    """wind ripples on dune sand (decal): long soft crests with a shadow under each"""
    im = Image.new('RGBA', (16, 16), CLEAR)
    for k, y0 in enumerate((3, 8, 13)):
        for x in range(16):
            y = y0 + int(1.2 * math.sin((x + v * 5 + k * 3) / 2.6))
            P(im, x, y, (236, 220, 176, 150)); P(im, x, y + 1, (176, 150, 104, 110))
    return im


def bones(v):
    """old bones half-buried in the sand (decal): a rib arc or a skull"""
    im = Image.new('RGBA', (16, 16), CLEAR); d = ImageDraw.Draw(im)
    if v == 0:
        for k in range(4): d.arc([2 + k * 3, 4, 8 + k * 3, 14], 200, 340, fill=BONE[2])
        d.line([2, 12, 14, 12], fill=BONE[1])
    else:
        d.ellipse([4, 4, 12, 11], fill=BONE[2], outline=BONE[0]); P(im, 6, 7, (60, 50, 40, 255)); P(im, 10, 7, (60, 50, 40, 255))
        d.line([5, 12, 11, 12], fill=BONE[1])
    return im


def rut(v):
    """cart ruts and boot-scuffs along a desert road (decal)"""
    im = Image.new('RGBA', (16, 16), CLEAR); r = random.Random(990 + v)
    for y0 in (4, 11):
        for x in range(16):
            y = y0 + (1 if (x + v * 3) % 9 < 2 else 0)
            P(im, x, y, (128, 98, 66, 210)); P(im, x, y + 1, (236, 216, 170, 150))
    for _ in range(3): P(im, r.randrange(16), r.randrange(6, 10), (140, 110, 80, 120))
    return im

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
