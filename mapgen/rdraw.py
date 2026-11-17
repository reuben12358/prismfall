#!/usr/bin/env python3
"""rdraw.py - hand-drawn pieces for the PF Rejuv `pf` part (MAPGEN 2h fix round): Frostwick's Isenmar whalebone
longhouses, the Two Hearths inn, the briar-wrapped whale-rib gate, rope walkways between the giant trees, hearth smoke,
market stalls, drying racks, sleds, the frozen waterfall and small snow props.

Everything is drawn on the 16-px logical grid and doubled with nearest-neighbour (ART_DIRECTION 1 and 6), with the
Kristiline / Sheridan ramps (snow 248/222/188/150, timber 52/84/110/140, outlines never black, light from the top left).
rcustom.py pastes the pieces after its own tiles (ids of earlier pieces never move) and writes stamps `wb_*` / `fw_*`.

A piece = (name, image (logical px, w*16 x h*16), code rows).  Code per tile:
  R  layer 3, passable, priority 1   (roof top / overhead, walk behind)
  r  layer 3, solid,    priority 1   (roof body)
  W  layer 2, solid                  (wall, trunk, counter, prop base)
  D  layer 2, passable               (door cell: the door event sits here)
  F  layer 2, passable, priority 0   (flat decal)
  O  layer 3, passable, priority 2   (high overhead: smoke, ropes, walkways, banners' tops)
  .  empty
    python3 -I rdraw.py out.png     # contact sheet of every piece (research)"""
import math, random, sys
from PIL import Image, ImageDraw

OUT = (58, 44, 52, 255)
BONE = [(112, 98, 86, 255), (178, 164, 142, 255), (220, 210, 190, 255), (246, 240, 226, 255)]
SNOW = [(150, 164, 200, 255), (188, 202, 228, 255), (222, 230, 242, 255), (248, 248, 252, 255)]
SOD = [(58, 46, 38, 255), (88, 72, 52, 255), (116, 98, 66, 255), (92, 116, 78, 255)]
WOOD = [(52, 36, 30, 255), (84, 58, 44, 255), (110, 80, 58, 255), (140, 104, 72, 255)]
STONE = [(66, 70, 86, 255), (100, 106, 124, 255), (138, 144, 162, 255), (176, 182, 198, 255)]
GLOW = [(196, 120, 60, 255), (255, 200, 104, 255), (255, 236, 168, 255)]
ICE = [(120, 168, 214, 255), (164, 214, 240, 255), (204, 238, 250, 255), (240, 252, 255, 255)]
TEAL = [(34, 70, 104, 255), (58, 122, 184, 255), (96, 168, 212, 255)]           # Isenmar cloth #3A7AB8
SLATE = [(56, 62, 78, 255), (90, 100, 120, 255), (126, 138, 158, 255)]
GREEN = [(28, 80, 46, 255), (47, 138, 74, 255), (92, 178, 108, 255)]            # Elowen cloth #2F8A4A
ROSE = [(140, 54, 84, 255), (214, 110, 140, 255), (244, 170, 190, 255)]
GOLD = [(150, 104, 40, 255), (232, 190, 90, 255), (252, 228, 150, 255)]
FISH = [(70, 84, 100, 255), (150, 170, 186, 255), (214, 226, 236, 255)]
CLEAR = (0, 0, 0, 0)


def canvas(w, h):
    im = Image.new('RGBA', (w * 16, h * 16), CLEAR)
    return im, ImageDraw.Draw(im)


def P(im, x, y, c):
    if 0 <= x < im.width and 0 <= y < im.height: im.putpixel((int(x), int(y)), c)


def disc(im, cx, cy, r, c):
    for y in range(int(cy - r - 1), int(cy + r + 2)):
        for x in range(int(cx - r - 1), int(cx + r + 2)):
            if (x + 0.5 - cx) ** 2 + (y + 0.5 - cy) ** 2 <= r * r: P(im, x, y, c)


def bez(p0, p1, p2, n=60):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
             (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in (i / n for i in range(n + 1))]


def bone(im, pts, r=1.6, taper=True):
    """a whale rib along a curve: dark outline, bone body, a light edge toward the top left"""
    n = len(pts)
    rr = [r * (1.0 - 0.45 * (i / (n - 1)) if taper else 1.0) for i in range(n)]
    for (x, y), q in zip(pts, rr): disc(im, x, y, q + 1.0, BONE[0])
    for (x, y), q in zip(pts, rr): disc(im, x, y, q, BONE[2])
    for (x, y), q in zip(pts, rr): disc(im, x + 0.6, y + 0.6, max(0.5, q - 0.6), BONE[1])
    for (x, y), q in zip(pts, rr): disc(im, x - 0.5, y - 0.5, max(0.4, q - 1.0), BONE[3])


def snow_cap(im, x0, x1, y, depth=3, seed=1):
    """a soft snow lip along y from x0..x1: white top, blue shadow under its wavy edge"""
    rng = random.Random(seed)
    for x in range(x0, x1 + 1):
        d = depth + (1 if rng.random() < 0.35 else 0) - (1 if rng.random() < 0.2 else 0)
        for k in range(d):
            P(im, x, y + k, SNOW[3] if k < d - 2 else SNOW[2])
        P(im, x, y + d, SNOW[1]); P(im, x, y - 1, SNOW[2] if rng.random() < 0.6 else CLEAR)


def icicles(im, x0, x1, y, seed=2, step=3):
    rng = random.Random(seed)
    for x in range(x0, x1 + 1, step):
        L = rng.choice((1, 2, 2, 3, 4))
        for k in range(L):
            P(im, x, y + k, ICE[2] if k < L - 1 else ICE[1])
        P(im, x + 1, y, ICE[3])


# --------------------------------------------------------------------------------------------- the longhouse kit
def longhouse(W, H=6, door=None, windows=(), shields=(), chimneys=(), seed=3, banners=()):
    """An Isenmar longhouse, W tiles wide, H tall: a long sway-backed turf roof under deep snow with whale-rib crosses
    at both gable ends, a stave wall on a stone footing, a whale-rib arch round the door, warm windows, round shields."""
    im, d = canvas(W, H)
    w, h = W * 16, H * 16
    rng = random.Random(seed)
    wall_top = h - 30; foot = h - 7
    # --- wall: vertical staves, shadow under the eave, stone footing
    for x in range(3, w - 3):
        for y in range(wall_top, foot):
            c = WOOD[2] if x % 5 else WOOD[0]
            if x % 5 == 1: c = WOOD[3]
            if y < wall_top + 5: c = WOOD[1] if x % 5 else WOOD[0]
            P(im, x, y, c)
    for x in range(2, w - 2):
        for y in range(foot, h):
            k = (x // 5 + (y - foot) // 3) % 3
            c = STONE[1 + (k == 0)] if y < h - 1 else STONE[0]
            if (x + (3 if (y - foot) // 3 % 2 else 0)) % 5 == 0 or (y - foot) % 3 == 2: c = STONE[0]
            P(im, x, y, c)
    for y in range(wall_top, h): P(im, 2, y, OUT); P(im, w - 3, y, OUT)
    # --- roof: a long mound, ridge sagging a little in the middle, rounded hips at both ends
    eave = wall_top + 3
    def ridge(x):
        t = (x - 6) / max(1, (w - 12))
        return 9 + 3 * math.sin(math.pi * t)
    tops = {}
    for x in range(1, w - 1):
        e = min(x - 1, w - 2 - x)
        top = ridge(x) + (max(0, 10 - e) ** 2) / 7.0
        tops[x] = int(top)
        for y in range(int(top), eave):
            fy = (y - top) / max(1, eave - top)
            c = SNOW[3] if fy < 0.3 else SNOW[2] if fy < 0.78 else SNOW[1]
            P(im, x, y, c)
        P(im, x, int(top) - 1, OUT if e > 1 else CLEAR)
    # snow lying in soft courses over the sod (lumps with a shadow under each and a lit top-left edge)
    for k, yy in enumerate(range(int(ridge(w // 2)) + 7, eave - 7, 6)):
        off = 4 if k % 2 else 0
        for x0 in range(2 + off, w - 2, 8):
            for i in range(8):
                x = x0 + i
                if x not in tops or yy < tops[x] + 3: continue
                dy = int(round(2.2 * math.sin(math.pi * i / 8.0)))
                P(im, x, yy + dy, SNOW[1] if k < 3 else SNOW[0])
                if i in (1, 2): P(im, x, yy + dy - 3, SNOW[3])
            if k >= 2 and rng.random() < 0.35:                      # turf peeking through the thinner snow low down
                tx = x0 + rng.randrange(1, 6)
                if tx in tops: P(im, tx, yy + 2, SOD[3]); P(im, tx + 1, yy + 2, SOD[1]); P(im, tx, yy + 3, SOD[1])
    for x in range(2, w - 2):                                        # ridge highlight
        if x in tops and min(x - 1, w - 2 - x) > 4: P(im, x, tops[x], SNOW[3]); P(im, x, tops[x] + 1, SNOW[3])
    # hips: outline down to the eave
    for side in (0, 1):
        for y in range(int(ridge(6)), eave):
            e = 10 - math.sqrt(max(0, (y - ridge(6)) * 7)) if y - ridge(6) < 15 else 0
            x = int(1 + max(0, e)) if side == 0 else int(w - 2 - max(0, e))
            P(im, x, y, OUT); P(im, x + (1 if side == 0 else -1), y, SNOW[1] if side else SNOW[2])
    # turf showing under the snow at the eave, grass tufts, then icicles over the wall
    for x in range(2, w - 2):
        for y in range(eave - 3, eave + 2):
            P(im, x, y, SOD[1] if y < eave else SOD[0])
        if rng.random() < 0.25: P(im, x, eave - 4, SOD[3]); P(im, x, eave - 3, SOD[3])
        if x % 3 == 0: P(im, x, eave - 3, SOD[2])
    snow_cap(im, 2, w - 3, eave - 6, 3, seed)
    icicles(im, 4, w - 5, eave + 2, seed + 1, 3)
    for x in range(1, w - 1): P(im, x, eave + 2 if False else eave + 1, OUT if x in (1, w - 2) else im.getpixel((x, eave + 1)))
    # windows with warm light, shutters
    for wx in windows:
        x0 = wx * 16 + 3; y0 = wall_top + 7
        d.rectangle([x0 - 1, y0 - 1, x0 + 10, y0 + 8], fill=WOOD[0])
        d.rectangle([x0, y0, x0 + 9, y0 + 7], fill=GLOW[1])
        d.rectangle([x0, y0, x0 + 3, y0 + 2], fill=GLOW[2])
        d.line([x0 + 4, y0, x0 + 4, y0 + 7], fill=WOOD[1]); d.line([x0, y0 + 4, x0 + 9, y0 + 4], fill=WOOD[1])
        d.rectangle([x0 - 4, y0 - 1, x0 - 2, y0 + 8], fill=TEAL[0]); d.rectangle([x0 + 12, y0 - 1, x0 + 14, y0 + 8], fill=TEAL[0])
        d.line([x0 - 3, y0, x0 - 3, y0 + 7], fill=TEAL[1]); d.line([x0 + 13, y0, x0 + 13, y0 + 7], fill=TEAL[1])
        snow_cap(im, x0 - 1, x0 + 10, y0 + 9, 1, seed + wx)
    for sx in shields:
        cx = sx * 16 + 8; cy = wall_top + 11
        disc(im, cx, cy, 5.2, OUT); disc(im, cx, cy, 4.4, TEAL[1])
        for y in range(int(cy - 4), int(cy + 5)):
            for x in range(int(cx), int(cx + 5)):
                if (x + 0.5 - cx) ** 2 + (y + 0.5 - cy) ** 2 <= 4.4 ** 2: P(im, x, y, SLATE[2])
        disc(im, cx, cy, 1.4, BONE[2]); P(im, cx - 2, cy - 3, TEAL[2])
    # door inside a whale-rib arch
    if door is not None:
        x0 = door * 16 + 3; y0 = wall_top + 4
        d.rectangle([x0 - 1, y0 - 1, x0 + 10, h - 1], fill=OUT)
        d.rectangle([x0, y0, x0 + 9, h - 1], fill=WOOD[1])
        for x in range(x0 + 1, x0 + 10, 3): d.line([x, y0 + 1, x, h - 1], fill=WOOD[2])
        d.line([x0, y0 + 7, x0 + 9, y0 + 7], fill=STONE[0]); d.line([x0, h - 8, x0 + 9, h - 8], fill=STONE[0])
        P(im, x0 + 7, y0 + 12, GOLD[1])
        cx = door * 16 + 8
        bone(im, bez((cx - 9, h - 1), (cx - 10, wall_top - 10), (cx + 1, wall_top - 13)), 1.8)
        bone(im, bez((cx + 9, h - 1), (cx + 10, wall_top - 10), (cx - 1, wall_top - 13)), 1.8)
    # whale-rib crosses at the gable ends
    for gx, s in ((8, 1), (w - 9, -1)):
        gy = int(ridge(6)) + 6
        bone(im, bez((gx - 3 * s, gy + 3), (gx - 1 * s, gy - 7), (gx + 7 * s, gy - 13)), 1.9)
        bone(im, bez((gx + 6 * s, gy + 3), (gx + 3 * s, gy - 7), (gx - 5 * s, gy - 12)), 1.9)
    # smoke holes / chimneys
    for cx, kind in chimneys:
        x = cx * 16 + 8; y = int(ridge(x)) + 2
        if kind == 'stone':
            d.rectangle([x - 4, y - 7, x + 3, y + 5], fill=STONE[1], outline=OUT)
            d.line([x - 3, y - 6, x - 3, y + 4], fill=STONE[3]); d.line([x - 4, y - 2, x + 3, y - 2], fill=STONE[0])
            snow_cap(im, x - 4, x + 3, y - 8, 2, x)
        else:
            d.rectangle([x - 3, y - 5, x + 2, y + 5], fill=WOOD[2], outline=OUT)
            d.line([x - 2, y - 4, x - 2, y + 4], fill=WOOD[3]); snow_cap(im, x - 4, x + 3, y - 6, 2, x)
    for bx, cols in banners:
        x = bx * 16 + 7; y0 = wall_top - 2
        d.line([x, y0, x, y0 + 18], fill=WOOD[0]); d.line([x + 1, y0, x + 1, y0 + 18], fill=WOOD[1])
        d.polygon([(x + 2, y0 + 1), (x + 9, y0 + 1), (x + 9, y0 + 14), (x + 5, y0 + 11), (x + 2, y0 + 14)], fill=cols[1], outline=OUT)
        d.line([x + 3, y0 + 2, x + 3, y0 + 11], fill=cols[2]); d.line([x + 6, y0 + 4, x + 8, y0 + 6], fill=cols[0])
    return im


def code_house(W, H, door, roof_rows=None):
    rr = roof_rows if roof_rows is not None else H - 2
    rows = []
    for r in range(H):
        if r == 0: rows.append('R' * W)
        elif r < rr: rows.append('r' * W)
        else: rows.append(''.join('D' if (r == H - 1 and door is not None and c == door) else 'W' for c in range(W)))
    return rows


# --------------------------------------------------------------------------------------------- the rib gate
def rib_gate():
    """the east gate: two pairs of whale ribs arching over the road, wrapped in Elowen briar with roses; an Elowen and an
    Isenmar pennant hang from the apex.  5 x 5 tiles: legs solid on the bottom row, the arch overhead."""
    im, d = canvas(5, 5)
    rng = random.Random(9)
    outer = [bez((6, 79), (2, 6), (40, 4)), bez((73, 79), (78, 6), (40, 4))]
    inner = [bez((11, 79), (9, 16), (40, 13)), bez((68, 79), (71, 16), (40, 13))]
    for c in inner: bone(im, c, 1.4, taper=False)
    for c in outer: bone(im, c, 2.2, taper=False)
    for c in outer + inner:                         # briar spirals with thorns and roses
        for i, (x, y) in enumerate(c[::2]):
            if i % 3 == 0:
                P(im, x + 1.5, y, SOD[0]); P(im, x - 1.5, y + 1, GREEN[0]); P(im, x, y - 1.5, GREEN[1])
            if rng.random() < 0.13:
                disc(im, x + rng.choice((-2, 2)), y, 1.3, ROSE[1]); P(im, x, y - 1, ROSE[2])
            elif rng.random() < 0.2:
                P(im, x + 2, y + 1, GREEN[2]); P(im, x + 3, y + 1, GREEN[1])
    for px, cols in ((35, GREEN), (44, TEAL)):      # pennants from the apex
        d.line([px, 8, px, 10], fill=OUT)
        d.polygon([(px - 3, 10), (px + 3, 10), (px + 3, 24), (px, 21), (px - 3, 24)], fill=cols[1], outline=OUT)
        d.line([px - 2, 11, px - 2, 20], fill=cols[2])
    d.rectangle([38, 9, 41, 12], fill=GOLD[1], outline=OUT)        # the Meridian sunburst bolted on (newer than the rest)
    for k in range(8):
        a = k * math.pi / 4; P(im, 39.5 + 4 * math.cos(a), 10.5 + 4 * math.sin(a), GOLD[2])
    for x in (4, 71):                               # snow on the feet
        snow_cap(im, x - 2, x + 6, 76, 2, x)
    return im, ['OOOOO', 'OOOOO', 'OO.OO', 'OO.OO', 'WO.OW']


# --------------------------------------------------------------------------------------------- walkways, smoke, props
def walkway_h():
    """1x1 rope walkway, east-west: snow-dusted planks between two hand-ropes (high overhead)"""
    im, d = canvas(1, 1)
    d.rectangle([0, 5, 15, 11], fill=WOOD[2])
    for x in range(0, 16, 4): d.line([x, 5, x, 11], fill=WOOD[0]); d.line([x + 1, 6, x + 1, 10], fill=WOOD[3])
    d.line([0, 4, 15, 4], fill=OUT); d.line([0, 12, 15, 12], fill=OUT)
    for x in range(16): P(im, x, 5, SNOW[3] if x % 5 else SNOW[2]); P(im, x, 6, SNOW[2] if x % 3 == 0 else im.getpixel((x, 6)))
    for x in range(16):
        P(im, x, 2 + (1 if 4 <= x <= 11 else 0), (196, 172, 120, 255)); P(im, x, 14 + (1 if 4 <= x <= 11 else 0), (196, 172, 120, 255))
    return im


def walkway_v():
    im, d = canvas(1, 1)
    d.rectangle([4, 0, 11, 15], fill=WOOD[2])
    for y in range(0, 16, 4): d.line([4, y, 11, y], fill=WOOD[0]); d.line([5, y + 1, 10, y + 1], fill=WOOD[3])
    d.line([3, 0, 3, 15], fill=OUT); d.line([12, 0, 12, 15], fill=OUT)
    for y in range(16):
        P(im, 4, y, SNOW[3] if y % 4 else SNOW[2]); P(im, 1, y, (196, 172, 120, 255)); P(im, 14, y, (196, 172, 120, 255))
    return im


def walkway_end(side):
    """the rope lashing where a walkway meets a giant's bole: knot and a hanging lantern"""
    im, d = canvas(1, 1)
    x0 = 0 if side == 'w' else 8
    d.rectangle([x0, 5, x0 + 7, 11], fill=WOOD[2])
    for x in range(x0, x0 + 8, 4): d.line([x, 5, x, 11], fill=WOOD[0])
    d.line([x0, 4, x0 + 7, 4], fill=OUT); d.line([x0, 12, x0 + 7, 12], fill=OUT)
    for x in range(x0, x0 + 8): P(im, x, 5, SNOW[3])
    kx = 7 if side == 'w' else 8
    disc(im, kx, 8, 2.4, (150, 120, 80, 255)); disc(im, kx, 8, 1.3, (196, 172, 120, 255))
    d.line([kx, 11, kx, 13], fill=OUT); d.rectangle([kx - 1, 13, kx + 1, 15], fill=GLOW[1], outline=OUT)
    return im


def smoke(kind):
    """a hearth plume, 1x2 high overhead: applewood (thin, warm grey) or whale oil (heavier, blue-grey)"""
    im, d = canvas(1, 2)
    rng = random.Random(1 if kind == 'apple' else 2)
    base = (180, 172, 168) if kind == 'apple' else (120, 126, 146)
    hi = (236, 232, 228) if kind == 'apple' else (188, 194, 208)
    for i, y in enumerate(range(30, -1, -3)):
        x = 8 + 3.5 * math.sin(y / 5.0 + (0 if kind == 'apple' else 1.3))
        r = 1.6 + (30 - y) / 11.0 * (1.0 if kind == 'apple' else 1.3)
        a = int(235 - (30 - y) * 5.0)
        if a <= 20: continue
        disc(im, x, y, r, base + (a,)); disc(im, x - 0.8, y - 0.8, max(0.6, r - 1.2), hi + (min(255, a + 20),))
    return im


def stall(kind):
    """a market stall, 3x3: striped canopy on posts, goods on the counter.  elowen: rose and green, honey jars, silk
    bolts; isenmar: teal and slate, hanging fish, furs, a barrel of eels"""
    im, d = canvas(3, 3)
    A, B = (ROSE, GREEN) if kind == 'elowen' else (TEAL, SLATE)
    for x in (2, 44):                                   # posts
        d.rectangle([x, 8, x + 2, 47], fill=WOOD[2], outline=OUT)
    d.rectangle([1, 30, 46, 46], fill=WOOD[2], outline=OUT)          # counter
    for x in range(3, 46, 6): d.line([x, 37, x, 45], fill=WOOD[1])
    d.line([2, 31, 45, 31], fill=WOOD[3]); d.line([2, 36, 45, 36], fill=WOOD[0])
    for i, x in enumerate(range(0, 48, 6)):             # canopy stripes and scalloped valance
        c = A if i % 2 == 0 else B
        d.polygon([(x, 4), (x + 6, 4), (x + 6, 13), (x, 13)], fill=c[1])
        d.line([x, 5, x + 5, 5], fill=c[2])
        d.pieslice([x, 9, x + 6, 17], 0, 180, fill=c[1], outline=OUT)
    d.line([0, 3, 47, 3], fill=OUT); snow_cap(im, 0, 47, 1, 2, 7 if kind == 'elowen' else 8)
    if kind == 'elowen':
        for x in (6, 12, 18):                           # honey jars
            d.rectangle([x, 24, x + 4, 30], fill=GOLD[1], outline=OUT); d.line([x + 1, 25, x + 1, 28], fill=GOLD[2])
            d.rectangle([x, 22, x + 4, 23], fill=ROSE[1], outline=OUT)
        for x, c in ((26, ROSE), (33, GREEN), (39, (210, 214, 230, 255))):   # silk bolts
            col = c if isinstance(c[0], int) else c[1]
            cc = (col, c[2] if not isinstance(c[0], int) else SNOW[3]) if not isinstance(c[0], int) else (col, SNOW[3])
            d.ellipse([x, 24, x + 6, 30], fill=cc[0], outline=OUT); P(im, x + 2, 26, cc[1])
        for x in range(8, 40, 7): d.line([x, 18, x + 3, 21], fill=(232, 236, 244, 255))   # silk strands drying
    else:
        for x in (8, 15, 22, 29, 36):                   # fish hung from the valance
            d.polygon([(x, 17), (x + 3, 17), (x + 4, 25), (x + 1, 28), (x - 1, 25)], fill=FISH[1], outline=OUT)
            P(im, x + 1, 19, FISH[2]); P(im, x + 2, 26, FISH[0])
        d.rectangle([4, 26, 22, 30], fill=(140, 116, 92, 255), outline=OUT)          # furs
        for x in range(5, 22, 3): P(im, x, 27, (184, 160, 130, 255))
        d.rectangle([26, 24, 34, 30], fill=WOOD[2], outline=OUT); d.line([26, 26, 34, 26], fill=STONE[1])  # eel barrel
        for x in (28, 31): d.line([x, 22, x + 1, 24], fill=(60, 66, 58, 255))
        d.ellipse([37, 25, 44, 30], fill=SNOW[2], outline=OUT); P(im, 39, 26, SNOW[3])   # a block of ice
    return im, ['RRR', 'WWW', 'WWW']


def rack():
    """an eel and fish drying rack, 2x2: two A-frames and a pole hung with fish and eels"""
    im, d = canvas(2, 2)
    for x in (3, 28):
        d.line([x - 2, 31, x + 1, 6], fill=OUT, width=2); d.line([x + 3, 31, x, 6], fill=OUT, width=2)
        d.line([x - 1, 30, x + 1, 8], fill=WOOD[2]); d.line([x + 2, 30, x, 8], fill=WOOD[2])
    d.line([1, 7, 30, 7], fill=OUT, width=2); d.line([1, 7, 30, 7], fill=WOOD[3])
    for i, x in enumerate(range(6, 27, 3)):
        if i % 2:
            d.line([x, 9, x, 21], fill=(52, 60, 56, 255), width=2); P(im, x, 10, (96, 110, 100, 255))
        else:
            d.polygon([(x - 1, 9), (x + 1, 9), (x + 2, 16), (x, 19), (x - 2, 16)], fill=FISH[1], outline=OUT); P(im, x, 11, FISH[2])
    snow_cap(im, 1, 30, 4, 2, 5)
    return im, ['OO', 'WW']


def sled():
    im, d = canvas(2, 1)
    d.rectangle([3, 4, 27, 10], fill=WOOD[2], outline=OUT)
    for x in range(5, 27, 4): d.line([x, 5, x, 9], fill=WOOD[3])
    d.line([2, 13, 28, 13], fill=OUT, width=2); d.arc([24, 4, 31, 14], 270, 90, fill=OUT, width=2)
    for x in (6, 22): d.line([x, 10, x, 12], fill=OUT)
    d.rectangle([7, 1, 18, 5], fill=(140, 116, 92, 255), outline=OUT); P(im, 9, 2, (184, 160, 130, 255))
    return im, ['WW']


def skull():
    """a whale skull half-buried in the snow (2x1): the town's oldest bench"""
    im, d = canvas(2, 1)
    d.ellipse([2, 3, 29, 14], fill=BONE[2], outline=BONE[0])
    d.ellipse([4, 4, 20, 9], fill=BONE[3]); d.ellipse([20, 6, 25, 10], fill=BONE[0])
    for x in range(6, 26, 4): P(im, x, 12, BONE[1])
    snow_cap(im, 0, 31, 12, 3, 4)
    return im, ['WW']


def woodpile():
    im, d = canvas(2, 1)
    for row, y in enumerate((9, 5)):
        for i, x in enumerate(range(2 + row * 3, 28 - row * 3, 6)):
            disc(im, x + 3, y + 3, 3.2, OUT); disc(im, x + 3, y + 3, 2.4, (176, 132, 86, 255)); P(im, x + 3, y + 3, (120, 84, 56, 255))
    snow_cap(im, 4, 26, 1, 2, 3)
    return im, ['WW']


def drift(seed):
    """a snowdrift with a few dry stalks (1x1 decal on the ground layer)"""
    im, d = canvas(1, 1)
    rng = random.Random(seed)
    cx, cy = 8, 10
    for y in range(4, 16):
        for x in range(16):
            dx, dy = (x - cx) / 7.0, (y - cy) / 4.0
            if dx * dx + dy * dy < 1.0 + 0.15 * rng.random():
                P(im, x, y, SNOW[3] if dy < -0.2 else SNOW[2] if dy < 0.5 else SNOW[1])
    for _ in range(3 if seed % 2 else 0):
        x = rng.randrange(3, 13); d.line([x, 3, x + rng.choice((-1, 1)), 9], fill=(150, 120, 92, 255))
    return im


def fishing_hole():
    """an ice-fishing hole with a little tripod and line (1x1, over ice)"""
    im, d = canvas(1, 1)
    d.ellipse([3, 8, 12, 14], fill=(40, 62, 98, 255), outline=ICE[3]); d.ellipse([5, 9, 10, 12], fill=(30, 46, 76, 255))
    d.line([3, 14, 7, 2], fill=WOOD[1]); d.line([11, 14, 7, 2], fill=WOOD[1]); d.line([7, 2, 7, 11], fill=(220, 220, 220, 255))
    return im


def banner(cols):
    im, d = canvas(1, 2)
    d.line([3, 2, 3, 31], fill=OUT, width=2); d.line([3, 3, 3, 30], fill=WOOD[2])
    d.polygon([(5, 4), (13, 4), (13, 19), (9, 16), (5, 19)], fill=cols[1], outline=OUT)
    d.line([6, 5, 6, 15], fill=cols[2]); d.line([8, 8, 11, 8], fill=cols[0])
    disc(im, 3, 2, 1.3, GOLD[1])
    return im, ['O', 'W']


def brazier():
    im, d = canvas(1, 2)
    d.line([4, 31, 7, 18], fill=OUT, width=2); d.line([11, 31, 8, 18], fill=OUT, width=2)
    d.rectangle([2, 15, 13, 19], fill=STONE[1], outline=OUT); d.line([3, 16, 12, 16], fill=STONE[3])
    for i, (x, y, r, c) in enumerate(((7.5, 11, 3.4, GLOW[0]), (7.5, 10, 2.4, GLOW[1]), (7, 9, 1.2, GLOW[2]))): disc(im, x, y, r, c)
    disc(im, 7.5, 8, 4.5, (255, 200, 110, 40))
    return im, ['O', 'W']


def frozen_fall(W=4, H=5):
    """the frozen Hoar Fall: a cascade stopped mid-pour - ice columns with blue cores and white crests, an icicle lip
    under a snow cap at the top, a heaped ice-and-snow foot at the bottom.  Solid (it covers a cliff face)."""
    im, d = canvas(W, H)
    w, h = W * 16, H * 16
    rng = random.Random(21)
    cols = []
    x = 1
    while x < w - 1:
        cw = rng.choice((3, 4, 5)); cols.append((x, min(w - 2, x + cw))); x += cw
    for i, (a, b) in enumerate(cols):
        top = 5 + rng.randrange(0, 4); bot = h - 9 - rng.randrange(0, 5)
        for xx in range(a, b + 1):
            edge = xx in (a, b)
            for yy in range(top, bot):
                f = (xx - a) / max(1, b - a)
                c = ICE[3] if f < 0.25 else ICE[2] if f < 0.6 else ICE[1]
                if edge: c = ICE[0]
                if (yy + i * 5) % 11 == 0 and not edge: c = ICE[3]
                P(im, xx, yy, c)
            if not edge:
                for k in range(rng.randrange(1, 5)): P(im, xx, bot + k, ICE[1] if k else ICE[2])
    for xx in range(w):                     # blue shadow behind the columns (the cliff under the ice)
        for yy in range(4, h - 6):
            if im.getpixel((xx, yy))[3] == 0: P(im, xx, yy, (96, 132, 176, 255))
    snow_cap(im, 0, w - 1, 1, 4, 31); icicles(im, 1, w - 2, 6, 33, 2)
    for xx in range(w):                     # the foot: heaped ice and snow
        hgt = 7 + int(3 * math.sin(xx / 5.0) + rng.random() * 2)
        for k in range(hgt):
            yy = h - 1 - k
            P(im, xx, yy, SNOW[3] if k > hgt - 3 else ICE[2] if (xx + k) % 7 else SNOW[2])
        P(im, xx, h - 1, SNOW[1])
    return im, ['O' * W] + ['W' * W] * (H - 1)


def hearth_stone():
    """the truce stone: a standing stone carved twice (knotwork and runes), 1x2"""
    im, d = canvas(1, 2)
    d.polygon([(3, 30), (2, 10), (5, 3), (10, 2), (13, 8), (13, 30)], fill=STONE[2], outline=OUT)
    d.line([4, 9, 4, 28], fill=STONE[3]); d.line([11, 9, 11, 28], fill=STONE[1])
    for y in range(9, 26, 4): P(im, 6, y, GREEN[1]); P(im, 7, y + 1, GREEN[1]); P(im, 9, y + 2, TEAL[1]); P(im, 10, y, TEAL[1])
    snow_cap(im, 4, 11, 1, 2, 8); snow_cap(im, 0, 15, 29, 2, 9)
    return im, ['O', 'W']


def pieces():
    """every piece: name -> (image at logical scale, code rows, door tile or None)"""
    out = {}
    out['wb_long'] = (longhouse(9, 6, door=4, windows=(2, 6), shields=(1, 7), chimneys=((5, 'stone'),), seed=3), code_house(9, 6, 4), (4, 5))
    out['wb_long2'] = (longhouse(8, 6, door=3, windows=(1, 5), shields=(6,), chimneys=((5, 'stone'),), seed=5), code_house(8, 6, 3), (3, 5))
    out['wb_short'] = (longhouse(6, 6, door=2, windows=(4,), shields=(), chimneys=((3, 'stone'),), seed=7), code_house(6, 6, 2), (2, 5))
    out['wb_inn'] = (longhouse(12, 6, door=6, windows=(2, 4, 8, 10), shields=(), chimneys=((3, 'stone'), (9, 'timber')), seed=11,
                              banners=((1, TEAL), (5, SLATE), (7, ROSE), (11, GREEN))), code_house(12, 6, 6), (6, 5))
    out['wb_smoke'] = (longhouse(7, 6, door=3, windows=(5,), shields=(1,), chimneys=((2, 'stone'), (5, 'stone')), seed=13), code_house(7, 6, 3), (3, 5))
    g, c = rib_gate(); out['wb_gate'] = (g, c, None)
    out['fw_walk_h'] = (walkway_h(), ['O'], None)
    out['fw_walk_v'] = (walkway_v(), ['O'], None)
    out['fw_walk_w'] = (walkway_end('w'), ['O'], None)
    out['fw_walk_e'] = (walkway_end('e'), ['O'], None)
    out['fw_smoke_a'] = (smoke('apple'), ['O', 'O'], None)
    out['fw_smoke_w'] = (smoke('whale'), ['O', 'O'], None)
    for k in ('elowen', 'isenmar'):
        im, c = stall(k); out['fw_stall_' + k[0]] = (im, c, None)
    for n, fn in (('fw_rack', rack), ('fw_sled', sled), ('fw_skull', skull), ('fw_wood', woodpile), ('fw_brazier', brazier),
                  ('fw_stone', hearth_stone)):
        im, c = fn(); out[n] = (im, c, None)
    im, c = banner(GREEN); out['fw_ban_e'] = (im, c, None)
    im, c = banner(TEAL); out['fw_ban_i'] = (im, c, None)
    for i in range(3): out['fw_drift%d' % i] = (drift(i + 1), ['F'], None)
    out['fw_hole'] = (fishing_hole(), ['F'], None)
    im, c = frozen_fall(4, 5); out['fw_fall'] = (im, c, None)
    return out


CODE = {'R': (2, 0, 1), 'r': (2, 15, 1), 'W': (1, 15, 0), 'D': (1, 0, 0), 'F': (1, 0, 0), 'O': (2, 0, 2)}   # layer, passage, priority


if __name__ == '__main__':
    ps = pieces()
    ims = [(n, im.resize((im.width * 2, im.height * 2), Image.NEAREST)) for n, (im, c, dr) in ps.items()]
    Wd = 1400; x = y = 0; rowh = 0; pos = []
    for n, im in ims:
        if x + im.width > Wd: x = 0; y += rowh + 14; rowh = 0
        pos.append((n, im, x, y)); x += im.width + 10; rowh = max(rowh, im.height)
    sheet = Image.new('RGBA', (Wd, y + rowh + 14), (232, 232, 240, 255))
    dr = ImageDraw.Draw(sheet)
    for n, im, x, y in pos:
        sheet.alpha_composite(im, (x, y + 12)); dr.text((x, y), n, fill=(200, 0, 120, 255))
    sheet.save(sys.argv[1] if len(sys.argv) > 1 else '/tmp/rdraw.png'); print(sheet.size)
