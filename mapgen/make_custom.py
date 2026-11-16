#!/usr/bin/env python3
"""make_custom.py - generate mapgen/custom/prismfall_custom2.png (+ .json passages/priorities), the second custom block of
tileset 33. Everything is assembled from Tectonic / Sheridan tiles or drawn on the 16-px grid and doubled (ART_DIRECTION 6).
Layout (8 tiles wide; ids = compose offset 'custom2' + row*8 + col), see LAYOUT below. Re-run compose_tileset.py after."""
import os, json, random
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
Image.MAX_IMAGE_PIXELS = None
T = Image.open('/home/claude/ref/art/tectonic/Graphics/Tilesets/Outside.png').convert('RGBA')
S = Image.open('/home/claude/ref/art/wll/Changed Files/Graphics/Tilesets/Sheridan_2.png').convert('RGBA')
ROWS = 20
sheet = Image.new('RGBA', (256, ROWS * 32), (0, 0, 0, 0))
pas = [15] * (ROWS * 8); pri = [0] * (ROWS * 8)


def tt(src, t):
    x, y = (t - 384) % 8 * 32, (t - 384) // 8 * 32
    return src.crop((x, y, x + 32, y + 32))


def setp(c0, r0, w, h, p, q):
    for r in range(r0, r0 + h):
        for c in range(c0, c0 + w): pas[r * 8 + c] = p; pri[r * 8 + c] = q


def crown(w, h, seed, c0, r0):
    rng = random.Random(seed); cv = Image.new('RGBA', (w * 32, h * 32), (0, 0, 0, 0))
    balls = []
    for sp in ((401, 402, 409, 410), (405, 406, 413, 414)):
        b = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        for i, t in enumerate(sp): b.alpha_composite(tt(T, t), (i % 2 * 32, i // 2 * 32))
        balls.append(b.crop((0, 0, 64, 52)))
    pts = []
    for _ in range(w * h * 4):
        x = rng.randrange(0, w * 32 - 64, 2); y = rng.randrange(0, h * 32 - 52, 2)
        cx, cy = (x + 32) / (w * 16.0) - 1, (y + 26) / (h * 16.0) - 1
        if cx * cx + cy * cy < 0.62: pts.append((y, x))
    for y, x in sorted(pts):
        cv.alpha_composite(balls[0] if rng.random() < 0.72 else balls[1], (x, y))
    sheet.alpha_composite(cv, (c0 * 32, r0 * 32)); setp(c0, r0, w, h, 0, 5)


def bole(w, h, c0, r0, door=None, window=None):
    for r in range(h):
        base = 1152 if r == h - 1 else 1144
        for c in range(w):
            t = tt(T, base + (0 if c == 0 else (2 if c == w - 1 else 1)))
            if 0 < c < w - 1 and c % 2 == 0: t = t.transpose(Image.FLIP_LEFT_RIGHT)
            sheet.alpha_composite(t, ((c0 + c) * 32, (r0 + r) * 32))
    if door is not None:
        sheet.alpha_composite(tt(S, 1429), ((c0 + door) * 32, (r0 + h - 2) * 32))
        sheet.alpha_composite(tt(S, 1437), ((c0 + door) * 32, (r0 + h - 1) * 32))
        pas[(r0 + h - 1) * 8 + c0 + door] = 0
    if window is not None:
        sheet.alpha_composite(tt(S, 522), ((c0 + window) * 32, (r0 + h - 3) * 32))
    for r in range(h - 2):                      # upper bole rows are walk-behind
        for c in range(w): pri[(r0 + r) * 8 + c0 + c] = 0


def draw16(w, h, fn, c0, r0, p=15, q=0):
    im = Image.new('RGBA', (w * 16, h * 16), (0, 0, 0, 0)); fn(ImageDraw.Draw(im), im)
    sheet.alpha_composite(im.resize((w * 32, h * 32), Image.NEAREST), (c0 * 32, r0 * 32)); setp(c0, r0, w, h, p, q)


OUTL = (52, 36, 30, 255); WOOD = (122, 84, 52, 255); WOODL = (158, 114, 72, 255); ROPE = (196, 172, 120, 255)


def laundry(d, im):
    for x in (1, 45): d.rectangle([x, 2, x + 1, 15], fill=WOOD, outline=OUTL)
    d.line([3, 4, 44, 5], fill=ROPE)
    for x, col in ((6, (232, 232, 226)), (14, (206, 92, 84)), (22, (92, 142, 196)), (30, (236, 206, 110)), (37, (226, 226, 232))):
        d.rectangle([x, 5, x + 5, 12], fill=col + (255,), outline=OUTL)
        d.line([x + 1, 7, x + 1, 11], fill=tuple(min(255, c + 22) for c in col) + (255,))


def bridge(d, im):
    d.rectangle([0, 2, 15, 13], fill=WOOD)
    for x in range(0, 16, 4): d.line([x, 3, x, 12], fill=OUTL); d.line([x + 1, 3, x + 1, 12], fill=WOODL)
    d.line([0, 1, 15, 1], fill=ROPE); d.line([0, 14, 15, 14], fill=ROPE); d.line([0, 2, 15, 2], fill=OUTL); d.line([0, 13, 15, 13], fill=OUTL)


def vat(col):
    def f(d, im):
        d.ellipse([1, 3, 14, 14], fill=WOOD, outline=OUTL); d.ellipse([3, 4, 12, 11], fill=col + (255,), outline=OUTL)
        d.line([5, 6, 8, 6], fill=tuple(min(255, c + 50) for c in col) + (255,)); d.line([1, 9, 14, 9], fill=OUTL)
    return f


def pool(d, im):
    for i, a in enumerate((26, 44, 62)):
        d.ellipse([2 + i * 5, 2 + i * 3, 45 - i * 5, 29 - i * 3], fill=(255, 226, 140, a))


def loom(d, im):
    d.rectangle([2, 2, 4, 30], fill=WOOD, outline=OUTL); d.rectangle([27, 2, 29, 30], fill=WOOD, outline=OUTL)
    d.rectangle([2, 4, 29, 6], fill=WOODL, outline=OUTL); d.rectangle([2, 22, 29, 25], fill=WOODL, outline=OUTL)
    for x in range(6, 27, 2): d.line([x, 7, x, 21], fill=(236, 236, 240, 255))
    d.rectangle([6, 15, 26, 21], fill=(150, 196, 170, 255)); d.line([6, 17, 26, 17], fill=(206, 110, 130, 255)); d.line([6, 19, 26, 19], fill=(236, 206, 110, 255))


def netrack(d, im):
    for x in (2, 28): d.rectangle([x, 6, x + 1, 30], fill=WOOD, outline=OUTL)
    d.rectangle([1, 6, 30, 7], fill=WOODL, outline=OUTL)
    for i in range(-20, 30, 4):
        d.line([i, 8, i + 18, 26], fill=(150, 160, 150, 255)); d.line([i + 18, 8, i, 26], fill=(118, 130, 124, 255))
    d.rectangle([0, 27, 31, 31], fill=(0, 0, 0, 0)); d.rectangle([0, 0, 0, 31], fill=(0, 0, 0, 0)); d.rectangle([31, 0, 31, 31], fill=(0, 0, 0, 0))
    for x in (2, 28): d.rectangle([x, 6, x + 1, 30], fill=WOOD, outline=OUTL)


def lantern(d, im):
    d.rectangle([7, 12, 8, 31], fill=WOOD, outline=OUTL); d.line([8, 5, 12, 5], fill=OUTL); d.line([8, 6, 8, 11], fill=OUTL)
    d.ellipse([3, 1, 13, 11], fill=(255, 236, 170, 70)); d.ellipse([10, 6, 14, 12], fill=(255, 226, 120, 255), outline=OUTL)
    d.point([11, 8], fill=(255, 255, 230, 255))


def awning(d, im):       # spider-silk awning: pale scalloped cloth, walk-behind
    d.rectangle([0, 2, 47, 9], fill=(232, 236, 240, 235), outline=(150, 160, 176, 255))
    for x in range(0, 48, 8):
        d.pieslice([x, 5, x + 8, 14], 0, 180, fill=(214, 220, 230, 235), outline=(150, 160, 176, 255))
    for x in range(2, 48, 6): d.line([x, 3, x + 3, 8], fill=(255, 255, 255, 255))


crown(8, 5, 11, 0, 0)
bole(6, 5, 0, 5, door=3, window=1); bole(2, 4, 6, 5)
bole(4, 4, 0, 10, door=1, window=3); bole(4, 4, 4, 10)
draw16(3, 1, laundry, 0, 14); draw16(1, 1, bridge, 3, 14, 0, 5)
draw16(1, 1, vat((70, 110, 190)), 6, 14); draw16(1, 1, vat((190, 70, 90)), 7, 14); draw16(1, 1, vat((220, 190, 80)), 0, 17)
draw16(3, 2, pool, 0, 15, 0, 0); draw16(2, 2, loom, 3, 15); draw16(2, 2, netrack, 5, 15); draw16(1, 2, lantern, 7, 15)
pri[15 * 8 + 7] = 5; pas[15 * 8 + 7] = 0; pri[15 * 8 + 3] = pri[15 * 8 + 4] = 5; pas[15 * 8 + 3] = pas[15 * 8 + 4] = 0
pri[15 * 8 + 5] = pri[15 * 8 + 6] = 5; pas[15 * 8 + 5] = pas[15 * 8 + 6] = 0
draw16(3, 1, awning, 1, 17, 0, 5)
crown(4, 3, 23, 4, 17)
os.makedirs(os.path.join(HERE, 'custom'), exist_ok=True)
sheet.save(os.path.join(HERE, 'custom', 'prismfall_custom2.png'))
json.dump({'passages': pas, 'priorities': pri}, open(os.path.join(HERE, 'custom', 'prismfall_custom2.json'), 'w'))
bg = Image.new('RGBA', sheet.size, (120, 170, 110, 255)); bg.alpha_composite(sheet); bg.convert('RGB').save('/tmp/w/custom2.png')
print('custom2', sheet.size)
