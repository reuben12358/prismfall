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
def longhouse(W, H=6, door=None, windows=(), shields=(), chimneys=(), seed=3, banners=(), porch=False, pc=False, skull=False, patch=()):
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
    if porch and door is not None:                         # a plank porch roof on two posts over the door, snow on top
        cx = door * 16 + 8
        d.rectangle([cx - 15, wall_top - 1, cx + 14, wall_top + 3], fill=WOOD[2], outline=OUT)
        for x in range(cx - 13, cx + 14, 4): d.line([x, wall_top, x, wall_top + 2], fill=WOOD[3])
        snow_cap(im, cx - 15, cx + 14, wall_top - 4, 3, seed + 9); icicles(im, cx - 13, cx + 12, wall_top + 4, seed + 4, 4)
        for x in (cx - 14, cx + 12): d.rectangle([x, wall_top + 4, x + 1, h - 1], fill=WOOD[1], outline=OUT)
    if pc and door is not None:                            # the Center's sign: a Poke Ball roundel over the arch, red cloth
        cx = door * 16 + 8; cy = wall_top - 17
        disc(im, cx, cy, 6.4, OUT); disc(im, cx, cy, 5.5, (236, 236, 240, 255))
        for y in range(int(cy - 6), int(cy)):
            for x in range(int(cx - 6), int(cx + 7)):
                if (x + 0.5 - cx) ** 2 + (y + 0.5 - cy) ** 2 <= 5.5 ** 2: P(im, x, y, (216, 60, 56, 255))
        d.line([cx - 5, cy, cx + 5, cy], fill=OUT); disc(im, cx, cy, 1.8, OUT); disc(im, cx, cy, 0.9, (248, 248, 252, 255))
    if skull and door is not None:                         # a whale vertebra hung over the door
        cx = door * 16 + 8; cy = wall_top - 15
        d.ellipse([cx - 5, cy - 3, cx + 4, cy + 3], fill=BONE[2], outline=BONE[0]); d.ellipse([cx - 2, cy - 1, cx + 1, cy + 1], fill=BONE[0])
        d.line([cx - 8, cy - 2, cx - 5, cy], fill=BONE[2]); d.line([cx + 4, cy, cx + 7, cy - 2], fill=BONE[2])
    for px, pw in patch:                                   # bare turf where the snow has slid off
        for x in range(px, px + pw):
            for y in range(eave - 14 - (x * 7 % 3), eave - 5):
                if x in tops and y > tops[x] + 4: P(im, x, y, SOD[3] if (x + y) % 4 == 0 else SOD[1] if (x * 3 + y) % 5 else SOD[2])
        snow_cap(im, px, px + pw - 1, eave - 17, 2, px)
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
ROPE = (196, 172, 120, 255); ROPED = (128, 104, 70, 255)


def walkway_h():
    """1x1 rope walkway, east-west, high overhead: snow-dusted planks, a dark underside and a cast shadow below
    (it reads as up in the air), hand-ropes above with hangers"""
    im, d = canvas(1, 1)
    for x in range(16): P(im, x, 14, (90, 100, 130, 110)); P(im, x, 15, (90, 100, 130, 70))      # shadow far below
    d.rectangle([0, 6, 15, 10], fill=WOOD[2])
    for x in range(0, 16, 3): d.line([x, 6, x, 10], fill=WOOD[0]); P(im, x + 1, 7, WOOD[3])
    d.line([0, 11, 15, 11], fill=WOOD[0]); d.line([0, 12, 15, 12], fill=OUT)
    for x in range(16): P(im, x, 6, SNOW[3] if x % 4 else SNOW[2])
    for x in range(16):                                  # hand-rope sagging between posts, hangers down to the planks
        yy = 2 + (1 if 3 <= x <= 12 else 0)
        P(im, x, yy, ROPE); P(im, x, yy + 1, ROPED)
    for x in (0, 15): d.line([x, 1, x, 6], fill=WOOD[1])
    for x in (5, 10): d.line([x, 4, x, 6], fill=ROPED)
    return im


def walkway_v():
    im, d = canvas(1, 1)
    d.rectangle([4, 0, 11, 15], fill=WOOD[2])
    for y in range(0, 16, 3): d.line([4, y, 11, y], fill=WOOD[0]); P(im, 5, y + 1, WOOD[3])
    d.line([3, 0, 3, 15], fill=OUT); d.line([12, 0, 12, 15], fill=OUT); d.line([13, 0, 13, 15], fill=(90, 100, 130, 110))
    for y in range(16):
        P(im, 4, y, SNOW[3] if y % 4 else SNOW[2]); P(im, 1, y, ROPE); P(im, 14, y, ROPE)
    return im


def walkway_end(side):
    """where a walkway is lashed to a giant's bole: the last planks, a rope knot, a hanging lantern"""
    im, d = canvas(1, 1)
    x0 = 0 if side == 'w' else 6
    for x in range(x0, x0 + 10): P(im, x, 14, (90, 100, 130, 110)); P(im, x, 15, (90, 100, 130, 70))
    d.rectangle([x0, 6, x0 + 9, 10], fill=WOOD[2])
    for x in range(x0, x0 + 10, 3): d.line([x, 6, x, 10], fill=WOOD[0])
    d.line([x0, 11, x0 + 9, 11], fill=WOOD[0]); d.line([x0, 12, x0 + 9, 12], fill=OUT)
    for x in range(x0, x0 + 10): P(im, x, 6, SNOW[3]); P(im, x, 2, ROPE); P(im, x, 3, ROPED)
    kx = 11 if side == 'w' else 4
    disc(im, kx, 5, 2.6, ROPED); disc(im, kx, 5, 1.5, ROPE)
    d.line([kx, 8, kx, 9], fill=OUT); d.rectangle([kx - 1, 10, kx + 1, 13], fill=GLOW[1], outline=OUT); P(im, kx, 11, GLOW[2])
    return im


def palisade(kind):
    """the town palisade: sharpened log stakes lashed with rope, snow on the points.  'v' runs north-south (seen
    edge-on: a column of stakes), 'h' east-west (a row of stakes, lower half solid)"""
    im, d = canvas(1, 1)
    if kind == 'h':
        for i, x in enumerate(range(0, 16, 4)):
            top = 2 + (i % 2)
            d.rectangle([x, top + 2, x + 3, 15], fill=WOOD[2]); d.line([x, top + 2, x, 15], fill=WOOD[0])
            d.line([x + 1, top + 3, x + 1, 14], fill=WOOD[3])
            d.polygon([(x, top + 2), (x + 1.5, top - 1), (x + 3, top + 2)], fill=WOOD[1]); P(im, x + 1, top, SNOW[3])
        d.line([0, 9, 15, 9], fill=ROPE); d.line([0, 10, 15, 10], fill=ROPED)
    else:
        d.rectangle([5, 0, 10, 15], fill=WOOD[2]); d.line([5, 0, 5, 15], fill=WOOD[0]); d.line([10, 0, 10, 15], fill=WOOD[0])
        d.line([6, 0, 6, 15], fill=WOOD[3])
        for y in range(0, 16, 4): d.line([5, y, 10, y], fill=WOOD[1]); P(im, 7, y + 1, SNOW[3]); P(im, 8, y + 1, SNOW[2])
        for y in (5, 13): d.line([4, y, 11, y], fill=ROPE)
    return im


def smoke(kind):
    """a hearth plume, 1x2 high overhead: applewood (thin, warm grey) or whale oil (heavier, blue-grey)"""
    im, d = canvas(1, 2)
    rng = random.Random(1 if kind == 'apple' else 2)
    base = (176, 166, 160) if kind == 'apple' else (104, 110, 132)
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


def fishing_hole(tripod=False):
    """an ice-fishing hole: dark water in a ring of broken white ice (1x1, over ice); with a little line tripod"""
    im, d = canvas(1, 1)
    d.ellipse([3, 6, 12, 13], fill=ICE[3]); d.ellipse([4, 7, 11, 12], fill=(52, 84, 128, 255)); d.ellipse([5, 8, 9, 10], fill=(70, 110, 156, 255))
    P(im, 3, 9, ICE[1]); P(im, 12, 10, ICE[1]); P(im, 7, 13, ICE[2])
    if tripod:
        d.line([4, 13, 8, 3], fill=WOOD[2]); d.line([12, 13, 8, 3], fill=WOOD[2]); d.line([8, 3, 8, 9], fill=SNOW[1])
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
    d.polygon([(3, 15), (5, 9), (7, 12), (8, 6), (10, 11), (12, 8), (12, 15)], fill=(214, 92, 40, 255))
    d.polygon([(5, 15), (7, 10), (8, 13), (10, 9), (11, 15)], fill=GLOW[1]); d.line([7, 14, 9, 12], fill=GLOW[2])
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


BARK = [(56, 58, 76, 255), (88, 94, 118, 255), (122, 130, 156, 255), (164, 174, 198, 255)]


BROWN = [(64, 46, 40, 255), (104, 78, 62, 255), (138, 108, 84, 255), (172, 142, 112, 255)]


def fallen_log(part):
    """the fallen giant over the Rimewood ravine, lying north-south: brown furrowed bark with snow along its upper
    (west) flank and moss on the lee side; 2 tiles wide.  'n' is the torn-up root plate with roots splayed and earth
    in them, 'm' a trunk segment (repeats), 's' the shattered crown end with snapped limbs.  Walkable: it is the bridge."""
    im, d = canvas(2, 1)
    def trunk(y0, y1):
        for y in range(y0, y1 + 1):
            for x in range(4, 28):
                f = (x - 4) / 23.0
                c = BROWN[3] if f < 0.2 else BROWN[2] if f < 0.6 else BROWN[1]
                if (x * 5 + (y // 2) * 3) % 7 == 0: c = BROWN[0]                       # bark furrows run along the trunk
                if (x + y // 3) % 9 == 4 and f > 0.5: c = (86, 110, 78, 255)            # moss
                P(im, x, y, c)
            P(im, 3, y, OUT); P(im, 28, y, OUT); P(im, 29, y, (90, 100, 130, 150)); P(im, 30, y, (90, 100, 130, 80))
            for x in range(5, 12):                                                      # snow lying along the west flank
                if (x * 3 + y * 5) % 11 < 7 - (x - 5): P(im, x, y, SNOW[3] if x < 9 else SNOW[2])
    if part == 'm':
        trunk(0, 15)
        d.ellipse([15, 5, 20, 10], fill=BROWN[0]); d.ellipse([16, 6, 19, 9], fill=(40, 30, 28, 255))   # a knot hole
        d.line([28, 3, 31, 1], fill=OUT); d.line([28, 4, 31, 2], fill=BROWN[1])                            # a branch stub
    elif part == 'n':
        trunk(9, 15)
        for (x0, y0, x1, y1, cx) in ((6, 10, 0, 2, 2), (11, 9, 7, 0, 8), (16, 9, 16, 1, 15), (21, 9, 25, 0, 24), (26, 10, 31, 3, 30)):
            pts = bez((x0, y0), (cx, (y0 + y1) / 2.0), (x1, y1), 14)
            for (x, y) in pts: disc(im, x, y, 1.6, OUT)
            for (x, y) in pts: disc(im, x, y, 0.9, BROWN[2])
        d.ellipse([7, 6, 25, 12], fill=(92, 70, 52, 255), outline=OUT)                                    # the earth-caked root plate
        for x, y in ((10, 8), (14, 10), (19, 8), (22, 10), (16, 7)): P(im, x, y, (132, 104, 76, 255))
        snow_cap(im, 9, 23, 4, 2, 44)
    else:
        trunk(0, 7)
        d.polygon([(3, 7), (7, 12), (10, 8), (13, 14), (17, 9), (21, 13), (24, 8), (28, 7)], fill=(196, 160, 118, 255), outline=OUT)
        for (x0, y0, x1, y1) in ((6, 9, 1, 15), (26, 9, 31, 14), (15, 11, 15, 15)):                        # snapped limbs
            d.line([x0, y0, x1, y1], fill=OUT, width=3); d.line([x0, y0, x1, y1], fill=BROWN[2])
        P(im, 2, 14, SNOW[3]); P(im, 30, 13, SNOW[3])
    return im


def snow_stairs(part):
    """timber stairs cut into a snowy bank (1x1, repeats down the flight): split-log treads with snow lying on each,
    a dark riser shadow, and a post-and-rope rail on the outer pieces.  part: l / m / r"""
    im, d = canvas(1, 1)
    for k in range(4):
        y = k * 4
        d.rectangle([0, y, 15, y + 1], fill=SNOW[3]); d.line([0, y + 1, 15, y + 1], fill=SNOW[2])
        d.line([0, y + 2, 15, y + 2], fill=WOOD[3]); d.line([0, y + 3, 15, y + 3], fill=WOOD[0])
        for x in range(2 + k % 2 * 3, 16, 6): P(im, x, y + 2, WOOD[2]); P(im, x + 1, y, SNOW[1])
    if part in 'lr':
        x = 0 if part == 'l' else 13
        d.rectangle([x, 0, x + 2, 15], fill=WOOD[1], outline=OUT); d.line([x + 1, 0, x + 1, 15], fill=WOOD[3])
        for y in (2, 10): P(im, x + 1, y, ROPE); d.line([x, y + 1, x + 2, y + 1], fill=ROPED)
        P(im, x + 1, 0, SNOW[3]); P(im, x + 1, 8, SNOW[3])
    return im


SOFT = [(170, 204, 230, 255), (196, 222, 240, 255), (216, 234, 246, 255), (236, 244, 250, 255)]


def soft_ice(v):
    """lagoon / brook ice in the snow palette: pale blue-white with faint wind streaks and a few snow patches (4
    variants, each tiles on itself), replacing Kristiline's saturated cyan stripes on our maps.  Terrain tag 12."""
    im, d = canvas(1, 1)
    rng = random.Random(90 + v)
    d.rectangle([0, 0, 15, 15], fill=SOFT[2])
    for k in range(3 + v % 2):
        y = rng.randrange(1, 15); x0 = rng.randrange(1, 9); L = rng.randrange(3, 7)
        for x in range(x0, x0 + L): P(im, x, y - (x - x0) // 3, SOFT[3])
    if v >= 2:
        cx, cy = rng.randrange(4, 12), rng.randrange(4, 12)
        for _ in range(9): P(im, cx + rng.randrange(-3, 4), cy + rng.randrange(-2, 3), SOFT[1] if v == 2 else SNOW[3])
    if v == 1: d.line([3, 11, 8, 9], fill=SOFT[0]); d.line([8, 9, 12, 10], fill=SOFT[0])
    return im


def boat(up):
    """a clinker-built fishing boat, 3x2: hauled out on the ice (upright, with oars and a net) or turned over for the
    winter with snow on the keel"""
    im, d = canvas(3, 2)
    if up:
        d.polygon([(2, 12), (10, 8), (38, 8), (46, 12), (40, 24), (8, 24)], fill=WOOD[1], outline=OUT)
        d.polygon([(6, 12), (11, 10), (37, 10), (42, 12), (38, 20), (10, 20)], fill=WOOD[3])
        for x in (16, 24, 32): d.line([x, 10, x, 20], fill=WOOD[1])
        for y in (22,): d.line([9, y, 39, y], fill=WOOD[2])
        d.line([12, 14, 36, 17], fill=BONE[2]); d.line([12, 15, 36, 18], fill=BONE[0])           # an oar
        d.rectangle([26, 11, 34, 14], fill=(120, 132, 126, 255)); P(im, 28, 12, (170, 180, 172, 255))  # a net
        snow_cap(im, 4, 44, 24, 2, 61)
    else:
        d.polygon([(2, 24), (8, 12), (24, 8), (40, 12), (46, 24)], fill=WOOD[2], outline=OUT)
        for y in (14, 18, 22): d.arc([4, y - 8, 44, y + 6], 200, 340, fill=WOOD[0])
        d.line([8, 12, 40, 12], fill=WOOD[3]); d.line([24, 8, 24, 24], fill=WOOD[1])
        snow_cap(im, 10, 38, 8, 3, 62); snow_cap(im, 2, 46, 23, 3, 63)
    return im, ['OOO', 'WWW']


def peg():
    """a Meridian survey peg: a short stake with a brass sunburst tag and a red ribbon (1x1, solid)"""
    im, d = canvas(1, 1)
    d.rectangle([7, 4, 8, 15], fill=WOOD[2]); d.line([7, 4, 7, 15], fill=WOOD[0])
    disc(im, 8, 4, 2.2, GOLD[0]); disc(im, 8, 4, 1.4, GOLD[1]); P(im, 7, 3, GOLD[2])
    d.line([9, 7, 12, 9], fill=(196, 60, 60, 255)); d.line([9, 8, 11, 10], fill=(150, 40, 46, 255))
    snow_cap(im, 4, 11, 13, 2, 3)
    return im


def reeds(seed):
    """frosted bulrushes, 1x2: tall stems and seed heads rimed white (top on layer 3, passable)"""
    im, d = canvas(1, 2)
    rng = random.Random(seed)
    for i in range(5):
        x = 2 + i * 3 + rng.randrange(0, 2); top = 4 + rng.randrange(0, 8)
        lean = rng.choice((-1, 0, 1))
        d.line([x, 31, x + lean, top + 4], fill=(150, 128, 92, 255))
        d.line([x + 1, 31, x + 1 + lean, top + 6], fill=(184, 160, 116, 255))
        if i % 2 == 0:
            d.rectangle([x + lean - 1, top, x + lean + 1, top + 5], fill=(120, 86, 60, 255), outline=OUT)
            P(im, x + lean, top, SNOW[3]); P(im, x + lean - 1, top + 1, SNOW[3])
    snow_cap(im, 0, 15, 28, 3, seed)
    return im


def crack(seed):
    """a pressure crack in sea ice with a ridge of broken plates (1x1 decal on ice)"""
    im, d = canvas(1, 1)
    rng = random.Random(seed)
    x, y = rng.randrange(0, 4), rng.randrange(4, 12)
    for _ in range(9):
        nx, ny = x + rng.randrange(1, 4), y + rng.randrange(-2, 3)
        d.line([x, y, nx, ny], fill=ICE[0]); d.line([x, y + 1, nx, ny + 1], fill=ICE[3])
        x, y = nx, max(1, min(14, ny))
        if x >= 15: break
    if seed % 2: P(im, 6, 6, ICE[3]); P(im, 7, 6, ICE[3]); P(im, 6, 7, ICE[1])
    return im


def floe(seed):
    """a loose ice floe on open water, rimmed in snow (1x1)"""
    im, d = canvas(1, 1)
    rng = random.Random(seed)
    pts = [(8 + (5 + rng.random() * 2) * math.cos(a), 8 + (3.5 + rng.random() * 1.5) * math.sin(a)) for a in [k * math.pi / 4 for k in range(8)]]
    d.polygon(pts, fill=ICE[2], outline=ICE[0]); d.line([4, 6, 10, 5], fill=SNOW[3]); P(im, 11, 9, ICE[3])
    return im


def face_icicles(seed):
    """icicles and a rime streak hanging down a snowy cliff face (1x1 overlay, layer 3)"""
    im, d = canvas(1, 1)
    rng = random.Random(seed)
    for x in range(1, 15, 2):
        if rng.random() < 0.55:
            L = rng.randrange(3, 13)
            for k in range(L): P(im, x, k, ICE[3] if k < 2 else ICE[2] if k < L - 2 else ICE[1])
            if L > 6: P(im, x + 1, 0, ICE[3])
    return im


def tracks(kind):
    """sled-runner tracks or bootprints pressed into packed snow (1x1 decal; very light, paths stay readable)"""
    im, d = canvas(1, 1)
    c = (184, 190, 220, 255)
    if kind == 0:
        for x in (4, 10):
            for y in range(16): P(im, x + (1 if y > 9 else 0), y, c)
    else:
        for i, y in enumerate(range(1, 16, 5)):
            x = 4 if i % 2 else 9
            d.rectangle([x, y, x + 2, y + 3], fill=c)
    return im


IRON = [(40, 44, 56, 255), (74, 82, 98, 255), (112, 122, 140, 255), (160, 170, 186, 255)]


def anchor_monument():
    """Ferrow's harbour monument, 3x4: the Dovetail line's first anchor, tarred iron gone green at the flukes, set upright
    on a stepped sandstone plinth with the bronze Accord plaque; rope coiled round the shank, gull droppings and all."""
    im, d = canvas(3, 4)
    SAND = [(120, 100, 76, 255), (176, 152, 112, 255), (212, 190, 146, 255), (236, 220, 180, 255)]
    for (x0, x1, y0, y1) in ((2, 45, 50, 63), (7, 40, 40, 51)):                  # two plinth steps
        d.rectangle([x0, y0, x1, y1], fill=SAND[1], outline=OUT)
        d.line([x0 + 1, y0 + 1, x1 - 1, y0 + 1], fill=SAND[3]); d.line([x0 + 1, y0 + 2, x1 - 1, y0 + 2], fill=SAND[2])
        for x in range(x0 + 6, x1, 9): d.line([x, y0 + 3, x, y1 - 1], fill=SAND[0])
    d.rectangle([17, 54, 30, 60], fill=GOLD[0], outline=OUT); d.line([19, 56, 28, 56], fill=GOLD[2]); d.line([19, 58, 26, 58], fill=GOLD[1])
    d.rectangle([22, 8, 25, 41], fill=IRON[1], outline=IRON[0]); d.line([23, 9, 23, 40], fill=IRON[3])      # shank
    d.ellipse([19, 1, 28, 9], outline=IRON[0], width=2); d.ellipse([21, 3, 26, 7], outline=IRON[2])           # ring
    d.rectangle([12, 11, 35, 13], fill=IRON[1], outline=IRON[0]); d.line([13, 12, 34, 12], fill=IRON[3])     # stock
    d.arc([6, 16, 41, 42], 0, 180, fill=IRON[0], width=4); d.arc([7, 17, 40, 41], 10, 170, fill=IRON[2], width=1)   # arms
    for fx, s_ in ((6, 1), (41, -1)):                                                                       # flukes, verdigris
        d.polygon([(fx, 30), (fx - 4 * s_, 22), (fx + 5 * s_, 25)], fill=(74, 130, 120, 255), outline=IRON[0])
    for y in range(18, 34, 3): d.line([21, y, 26, y + 2], fill=(196, 172, 120, 255)); d.line([21, y + 1, 26, y + 3], fill=(128, 104, 70, 255))
    P(im, 14, 10, SNOW[3]); P(im, 15, 10, SNOW[3]); P(im, 31, 10, SNOW[2])
    return im, ['OOO', 'OOO', 'WWW', 'WWW']


def snow_bridge(part):
    """Frostwick's brook bridges (1x1 tiles, the bridge runs east-west): split planks laid across the stringers with
    snow trodden into the gaps and lying along the edges, a post-and-beam rail with a snow cap on the north (n) and
    south (s) tiles, the dark underside showing over the ice below the south rail.  part: n / m / s (+ digit variant)"""
    im, d = canvas(1, 1)
    v = int(part[1]) if len(part) > 1 else 0; part = part[0]
    rng = random.Random(700 + v * 13 + ord(part))
    d.rectangle([0, 0, 15, 15], fill=WOOD[2])
    for x in range(0, 16, 4):                                  # planks, 4 px wide, each a touch different
        c = WOOD[3] if (x // 4 + v) % 3 == 0 else WOOD[2]
        d.rectangle([x, 0, x + 2, 15], fill=c); d.line([x + 3, 0, x + 3, 15], fill=WOOD[0])
        d.line([x, 0, x, 15], fill=WOOD[3] if c == WOOD[2] else (164, 126, 90, 255))
    for _ in range(5 + 2 * v):                                 # snow trodden into the boards
        x, y = rng.randrange(16), rng.randrange(2, 14)
        P(im, x, y, SNOW[3]); P(im, x + 1, y, SNOW[2])
        if rng.random() < 0.4: P(im, x, y + 1, SNOW[2])
    for _ in range(3): P(im, rng.randrange(16), rng.randrange(16), WOOD[1])
    if part == 'n':
        d.rectangle([0, 0, 15, 2], fill=CLEAR)
        d.rectangle([0, 6, 15, 7], fill=WOOD[0])               # rail shadow on the deck
        for x in range(16): P(im, x, 8, SNOW[2] if (x + v) % 5 else SNOW[3])   # snow blown against the rail foot
        for x in range(0, 16, 3): P(im, x + v % 2, 9, SNOW[3])
        d.rectangle([0, 3, 15, 5], fill=WOOD[1]); d.line([0, 3, 15, 3], fill=OUT); d.line([0, 4, 15, 4], fill=WOOD[3])
        for px in (3, 11):                                     # posts
            d.rectangle([px, 1, px + 2, 7], fill=WOOD[1], outline=OUT); d.line([px + 1, 2, px + 1, 6], fill=WOOD[3])
            P(im, px, 0, SNOW[2]); P(im, px + 1, 0, SNOW[3]); P(im, px + 2, 0, SNOW[3]); P(im, px + 1, 1, SNOW[3])
        for x in range(16):                                    # snow cap on the beam
            if x not in (3, 4, 5, 11, 12, 13):
                P(im, x, 2, SNOW[3]); P(im, x, 3, SNOW[3] if (x * 7 + v) % 4 else SNOW[2])
    if part == 's':
        for x in range(16): P(im, x, 5, SNOW[2] if (x + v) % 4 else SNOW[3])
        for x in range(1, 16, 3): P(im, x, 4, SNOW[3])
        d.rectangle([0, 9, 15, 11], fill=WOOD[1]); d.line([0, 9, 15, 9], fill=OUT); d.line([0, 10, 15, 10], fill=WOOD[3])
        d.rectangle([0, 12, 15, 13], fill=WOOD[0]); d.rectangle([0, 14, 15, 15], fill=CLEAR)
        for x in range(0, 16, 2): P(im, x, 14, (96, 120, 160, 150))    # shadow on the ice
        for px in (3, 11):
            d.rectangle([px, 6, px + 2, 13], fill=WOOD[1], outline=OUT); d.line([px + 1, 7, px + 1, 12], fill=WOOD[3])
            P(im, px, 5, SNOW[3]); P(im, px + 1, 5, SNOW[3]); P(im, px + 2, 5, SNOW[2]); P(im, px + 1, 6, SNOW[3])
        for x in range(16):
            if x not in (3, 4, 5, 11, 12, 13):
                P(im, x, 8, SNOW[3]); P(im, x, 9, SNOW[3] if (x * 5 + v) % 4 else SNOW[2])
    return im



def pc_sign():
    """a village Poke Center sign, 1x2: a carved board hung from a timber post, a red-and-white ball painted on it"""
    im, d = canvas(1, 2)
    d.rectangle([2, 6, 4, 30], fill=WOOD[1], outline=OUT); d.line([3, 7, 3, 29], fill=WOOD[3])
    d.rectangle([2, 4, 14, 6], fill=WOOD[1], outline=OUT); d.line([3, 5, 13, 5], fill=WOOD[3])
    d.line([8, 7, 8, 8], fill=ROPED); d.line([12, 7, 12, 8], fill=ROPED)
    d.rectangle([5, 9, 15, 20], fill=(226, 212, 180, 255), outline=OUT)
    d.ellipse([6, 10, 14, 19], fill=(244, 244, 248, 255), outline=OUT)
    d.pieslice([6, 10, 14, 19], 180, 360, fill=(216, 60, 56, 255), outline=OUT)
    d.line([7, 14, 13, 14], fill=OUT); d.rectangle([9, 13, 11, 15], fill=(244, 244, 248, 255), outline=OUT)
    P(im, 8, 12, (244, 130, 120, 255))
    d.line([1, 31, 5, 31], fill=(60, 90, 60, 160))
    return im, ['O', 'W']



RED = [(84, 26, 34, 255), (128, 40, 44, 255), (170, 62, 58, 255), (208, 98, 80, 255), (232, 140, 112, 255)]
PLASTER = [(150, 130, 108, 255), (196, 180, 152, 255), (226, 214, 186, 255), (244, 236, 214, 255)]


def playhouse():
    """The Pell Playhouse, Saltmere (14x12): a timber-framed playhouse on a stone arcade.  Crimson tile roof with a
    gilded ridge, a front gable holding a round window with the comedy and tragedy masks, a pennant on the apex;
    plastered upper storey with red-curtained windows and two crimson banners; stone ground floor with an arcade of
    posters, a gilt marquee board over the double doors.  Light from the top left; outlines never black."""
    W, H = 14, 12
    im, d = canvas(W, H); w, h = W * 16, H * 16
    # ---- main roof (rows 0-5): a broad hipped roof, eaves at y 92
    ey, ry = 92, 22
    d.polygon([(4, ey), (22, ry), (w - 23, ry), (w - 5, ey)], fill=RED[1], outline=OUT)
    for y in range(ry + 4, ey - 1, 5):                               # tile courses, staggered
        t = (y - ry) / float(ey - ry); x0 = int(22 - 18 * t) + 2; x1 = int(w - 23 + 18 * t) - 2
        d.line([x0, y, x1, y], fill=RED[0])
        for x in range(x0 + ((y // 5) % 2) * 3, x1, 6): P(im, x, y - 1, RED[2]); P(im, x + 1, y - 2, RED[3])
    d.line([23, ry + 1, 40, ry + 1], fill=RED[4]); d.line([6, ey - 2, 21, ry + 2], fill=RED[3])     # lit hip edge
    d.line([22, ry, w - 23, ry], fill=GOLD[1]); d.line([22, ry - 1, w - 23, ry - 1], fill=GOLD[0])   # gilded ridge
    for x in range(26, w - 24, 8): d.polygon([(x, ry - 1), (x + 2, ry - 5), (x + 4, ry - 1)], fill=GOLD[1], outline=GOLD[0])
    d.rectangle([4, ey, w - 5, ey + 3], fill=WOOD[1], outline=OUT); d.line([5, ey + 1, w - 6, ey + 1], fill=WOOD[3])   # eaves board
    # ---- front gable (centre): a tall triangle over the entrance with the masks window
    cx = w // 2; gy0, gy1 = 6, ey + 2
    d.polygon([(cx - 40, gy1), (cx, gy0), (cx + 40, gy1)], fill=RED[2], outline=OUT)
    for y in range(gy0 + 8, gy1, 5):
        half = int(40 * (y - gy0) / float(gy1 - gy0)) - 2
        d.line([cx - half, y, cx + half, y], fill=RED[1])
        for x in range(cx - half + ((y // 5) % 2) * 3, cx + half, 6): P(im, x, y - 1, RED[3])
    d.line([cx - 1, gy0 + 1, cx - 39, gy1 - 1], fill=RED[4])
    d.polygon([(cx - 30, gy1), (cx, gy0 + 20), (cx + 30, gy1)], fill=PLASTER[2], outline=OUT)      # plaster tympanum
    d.line([cx - 29, gy1 - 1, cx, gy0 + 21], fill=PLASTER[3])
    d.ellipse([cx - 13, 52, cx + 13, 78], fill=GOLD[0], outline=OUT); d.ellipse([cx - 11, 54, cx + 11, 76], fill=(44, 60, 92, 255))
    for a in range(0, 360, 45):                                     # rose window tracery
        import math as _m
        d.line([cx, 65, cx + int(11 * _m.cos(_m.radians(a))), 65 + int(11 * _m.sin(_m.radians(a)))], fill=GOLD[1])
    d.ellipse([cx - 9, 59, cx - 1, 69], fill=PLASTER[3], outline=OUT)     # comedy (left)
    P(im, cx - 7, 62, OUT); P(im, cx - 4, 62, OUT); d.arc([cx - 8, 62, cx - 2, 67], 20, 160, fill=OUT)
    d.ellipse([cx + 1, 61, cx + 9, 71], fill=GOLD[2], outline=OUT)        # tragedy (right)
    P(im, cx + 3, 64, OUT); P(im, cx + 6, 64, OUT); d.arc([cx + 2, 67, cx + 8, 72], 200, 340, fill=OUT)
    d.line([cx, gy0, cx, gy0 - 6], fill=WOOD[0]); d.polygon([(cx + 1, gy0 - 6), (cx + 9, gy0 - 4), (cx + 1, gy0 - 2)], fill=RED[3], outline=RED[0])
    # ---- upper storey (y 96-139): plaster between timber posts, curtained windows, banners
    fy0, fy1 = 96, 140
    d.rectangle([6, fy0, w - 7, fy1], fill=PLASTER[2], outline=OUT)
    d.line([7, fy0 + 1, w - 8, fy0 + 1], fill=PLASTER[3])
    posts = [6, 34, 62, 96, 126, 160, 188, w - 9]
    for px in posts:
        d.rectangle([px, fy0, px + 3, fy1], fill=WOOD[1], outline=OUT); d.line([px + 1, fy0 + 1, px + 1, fy1 - 1], fill=WOOD[3])
    d.rectangle([6, fy0 + 20, w - 7, fy0 + 22], fill=WOOD[1]); d.line([6, fy0 + 20, w - 7, fy0 + 20], fill=WOOD[3])
    for a, b in zip(posts, posts[1:]):
        if b - a < 20: continue
        m_ = (a + b) // 2
        d.rectangle([m_ - 7, fy0 + 4, m_ + 7, fy0 + 18], fill=WOOD[0], outline=OUT)             # window
        d.rectangle([m_ - 6, fy0 + 5, m_ + 6, fy0 + 17], fill=(255, 214, 140, 255))
        d.polygon([(m_ - 6, fy0 + 5), (m_ - 1, fy0 + 5), (m_ - 6, fy0 + 17)], fill=RED[2])         # curtains
        d.polygon([(m_ + 6, fy0 + 5), (m_ + 1, fy0 + 5), (m_ + 6, fy0 + 17)], fill=RED[2])
        d.line([m_ - 6, fy0 + 5, m_ + 6, fy0 + 5], fill=RED[1])
        d.line([a + 4, fy0 + 23, b - 1, fy1 - 1], fill=WOOD[1]); d.line([b - 1, fy0 + 23, a + 4, fy1 - 1], fill=WOOD[1])   # braces
    d.rectangle([7, fy0 + 2, w - 8, fy0 + 3], fill=PLASTER[1])                            # shadow under the eaves
    for bx in (posts[2] - 3, posts[5] - 3):                          # two crimson banners on the posts, with the gold mask
        d.rectangle([bx, fy0 + 2, bx + 8, fy0 + 36], fill=RED[1], outline=OUT); d.line([bx + 1, fy0 + 3, bx + 1, fy0 + 35], fill=RED[3])
        d.polygon([(bx, fy0 + 36), (bx + 4, fy0 + 32), (bx + 8, fy0 + 36), (bx + 8, fy0 + 40), (bx + 4, fy0 + 37), (bx, fy0 + 40)], fill=RED[1], outline=OUT)
        d.ellipse([bx + 1, fy0 + 12, bx + 7, fy0 + 19], fill=GOLD[1], outline=GOLD[0]); P(im, bx + 3, fy0 + 15, OUT); P(im, bx + 5, fy0 + 15, OUT)
        d.rectangle([bx - 1, fy0, bx + 9, fy0 + 2], fill=GOLD[0])
    # ---- ground floor (y 140-191): stone arcade, posters, marquee, double doors, steps
    gy = 140
    d.rectangle([4, gy, w - 5, h - 1], fill=STONE[1], outline=OUT)
    for y in range(gy + 6, h - 1, 7):
        d.line([5, y, w - 6, y], fill=STONE[0])
        for x in range(5 + (y // 7 % 2) * 6, w - 6, 12): d.line([x, y - 6, x, y - 1], fill=STONE[0]); P(im, x + 1, y - 6, STONE[2])
    d.rectangle([4, gy, w - 5, gy + 3], fill=STONE[3], outline=OUT); d.line([5, gy + 4, w - 6, gy + 4], fill=STONE[0])
    for i, ax in enumerate(range(12, w - 20, 24)):                  # arcade bays
        if abs(ax + 8 - cx) < 20: continue
        d.rectangle([ax, gy + 12, ax + 16, h - 6], fill=STONE[0], outline=OUT)
        d.pieslice([ax, gy + 6, ax + 16, gy + 22], 180, 360, fill=STONE[0], outline=OUT)
        d.rectangle([ax + 3, gy + 15, ax + 13, gy + 33], fill=PLASTER[3], outline=OUT)            # playbill
        col = (RED, TEAL, GOLD, ROSE)[i % 4]
        d.rectangle([ax + 4, gy + 17, ax + 12, gy + 24], fill=col[1]); d.line([ax + 5, gy + 27, ax + 11, gy + 27], fill=OUT); d.line([ax + 5, gy + 30, ax + 10, gy + 30], fill=STONE[1])
    d.rectangle([cx - 18, gy + 4, cx + 17, gy + 13], fill=GOLD[1], outline=OUT)                # marquee board
    d.line([cx - 17, gy + 5, cx + 16, gy + 5], fill=GOLD[2])
    for x in range(cx - 14, cx + 14, 4): d.rectangle([x, gy + 8, x + 2, gy + 10], fill=RED[0])
    for x in range(cx - 18, cx + 18, 5): P(im, x, gy + 14, (255, 236, 168, 255))                  # bulbs
    d.rectangle([cx - 14, gy + 18, cx + 13, h - 3], fill=WOOD[0], outline=OUT)                  # double doors
    d.pieslice([cx - 14, gy + 12, cx + 13, gy + 26], 180, 360, fill=WOOD[0], outline=OUT)
    for dx in (-12, 1):
        d.rectangle([cx + dx, gy + 20, cx + dx + 10, h - 4], fill=RED[1], outline=OUT); d.line([cx + dx + 1, gy + 21, cx + dx + 1, h - 5], fill=RED[3])
        d.rectangle([cx + dx + 2, gy + 24, cx + dx + 8, gy + 34], outline=GOLD[1])
    P(im, cx - 3, gy + 38, GOLD[2]); P(im, cx + 2, gy + 38, GOLD[2])
    for x in (cx - 20, cx + 19):                                    # lanterns either side
        d.rectangle([x - 1, gy + 18, x + 1, gy + 26], fill=IRON[1], outline=IRON[0]); P(im, x, gy + 21, (255, 214, 120, 255))
    code = ['R' * W] + ['r' * W] * 6 + ['W' * W] * 4 + [''.join('D' if c == 7 else 'W' for c in range(W))]
    return im, code



def pieces():
    """every piece: name -> (image at logical scale, code rows, door tile or None)"""
    out = {}
    out['wb_long'] = (longhouse(9, 6, door=4, windows=(2, 6), shields=(1, 7), chimneys=((6, 'stone'),), seed=3, porch=True), code_house(9, 6, 4), (4, 5))
    out['wb_long2'] = (longhouse(8, 6, door=2, windows=(4, 6), shields=(0,), chimneys=((5, 'stone'),), seed=5, skull=True, patch=((78, 22),)), code_house(8, 6, 2), (2, 5))
    out['wb_long3'] = (longhouse(11, 6, door=7, windows=(1, 3, 5, 9), shields=(2, 4), chimneys=((2, 'stone'), (8, 'stone')), seed=17, porch=True, patch=((20, 18),)), code_house(11, 6, 7), (7, 5))
    out['wb_short'] = (longhouse(6, 6, door=3, windows=(1,), shields=(5,), chimneys=((1, 'stone'),), seed=7, skull=True), code_house(6, 6, 3), (3, 5))
    out['wb_hut'] = (longhouse(5, 5, door=2, windows=(), shields=(0, 4), chimneys=((3, 'stone'),), seed=19, patch=((52, 14),)), code_house(5, 5, 2), (2, 4))
    out['wb_inn'] = (longhouse(12, 6, door=6, windows=(2, 4, 8, 10), shields=(), chimneys=((3, 'stone'), (9, 'timber')), seed=11,
                              banners=((1, TEAL), (5, SLATE), (7, ROSE), (11, GREEN)), porch=True), code_house(12, 6, 6), (6, 5))
    out['wb_smoke'] = (longhouse(7, 6, door=3, windows=(5,), shields=(1,), chimneys=((2, 'stone'), (5, 'stone')), seed=13, patch=((60, 16),)), code_house(7, 6, 3), (3, 5))
    out['wb_pc'] = (longhouse(9, 6, door=4, windows=(1, 2, 6, 7), shields=(), chimneys=((7, 'timber'),), seed=23, porch=True, pc=True,
                              banners=((3, ((140, 40, 44, 255), (216, 60, 56, 255), (244, 130, 120, 255))), (5, ((140, 40, 44, 255), (216, 60, 56, 255), (244, 130, 120, 255))))), code_house(9, 6, 4), (4, 5))
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
    out['fw_hole_t'] = (fishing_hole(True), ['F'], None)
    out['fw_pal_h'] = (palisade('h'), ['W'], None)
    out['fw_peg'] = (peg(), ['W'], None)
    for k in 'lmr': out['fw_stair_' + k] = (snow_stairs(k), ['F'], None)
    for v in range(4): out['fw_ice%d' % v] = (soft_ice(v), ['I'], None)
    im, c = boat(True); out['fw_boat'] = (im, c, None)
    im, c = boat(False); out['fw_boat_over'] = (im, c, None)
    for i in range(2): out['fw_reeds%d' % i] = (reeds(i + 3), ['O', 'F'], None)
    for i in range(3): out['fw_crack%d' % i] = (crack(i + 1), ['F'], None)
    for i in range(2): out['fw_floe%d' % i] = (floe(i + 5), ['F'], None)
    for i in range(3): out['fw_icy%d' % i] = (face_icicles(i + 11), ['O'], None)
    for i in range(2): out['fw_tracks%d' % i] = (tracks(i), ['F'], None)
    im, c = anchor_monument(); out['pf_anchor'] = (im, c, None)
    out['fw_pal_v'] = (palisade('v'), ['W'], None)
    im, c = frozen_fall(4, 5); out['fw_fall'] = (im, c, None)
    for k in 'nms': out['fw_log_' + k] = (fallen_log(k), ['FF'], None)
    # ---- appended by map builder 7 (append below this line only: earlier ids must not move)
    for k, code in (('n', 'N'), ('m', 'F'), ('s', 'S')):
        for v in range(2): out['fw_bridge_%s%d' % (k, v)] = (snow_bridge('%s%d' % (k, v)), [code], None)
    return out


def pieces_late():
    """pieces added after rcustom's EXTRA33 block.  APPEND NEW PIECES HERE (at the end): ids before them never move."""
    out = {}
    im, c = pc_sign(); out['pf_pcsign'] = (im, c, None)
    import os, json                                   # imported sheets (rimport.py): keyed 16-px pieces at 1x
    d_ = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'imports')
    mp = os.path.join(d_, 'manifest.json')
    if os.path.exists(mp):
        for n, v in json.load(open(mp)).items():
            out[n] = (Image.open(os.path.join(d_, n + '.png')).convert('RGBA'), v['code'], tuple(v['door']) if v.get('door') else None)
    return out


CODE = {'R': (2, 0, 1), 'r': (2, 15, 1), 'W': (1, 15, 0), 'D': (1, 0, 0), 'F': (1, 0, 0), 'O': (2, 0, 2), 'I': (1, 0, 0, 12),
        'N': (1, 8, 0), 'S': (1, 1, 0),
        'Q': (1, 0, 0), 'G': (0, 0, 0)}   # layer, passage, priority (Q: walkable quay coping; G: ground tile)


def pieces_late2():
    """fourth block (after rcustom's Dovetail port).  APPEND NEW PIECES HERE: earlier ids never move."""
    out = {}
    im, c = playhouse(); out['pf_playhouse'] = (im, c, (7, 11))
    return out


def pieces_late3():
    """fifth block (map builder 8): Saltmere's city kit from tdraw.py (townhouses, quay kit, stone and timber stairs,
    cranes, salt, playbills, fountain, stalls, grass variation).  rcustom dedups identical tiles in this block."""
    import tdraw
    return tdraw.city_pieces()


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

