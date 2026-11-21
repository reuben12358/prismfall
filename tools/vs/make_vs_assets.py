#!/usr/bin/env python3
"""Builds the trainer VS screen UI art (B2W2 Elite Four style; the Rejuvenation band set below is kept for reference) (Prismfall EBDX Bridge 010_Bridge_VersusIntro.rb).

    python3 -I tools/vs/make_vs_assets.py            -> graphics/EBDX/VS/{vs_logo,panel_<theme>,band_edge}.png

All drawn on a native pixel grid and doubled (2x2 blocks), like the B2W2-style cast art.
  panel_<theme>.png  512x136, tiles horizontally: dark top/bottom, bright horizontal glow, speed streaks
  vs_logo.png        chunky italic VS, crimson with dark outline, top highlight and a slash
  band_edge.png      512x8 metal trim drawn above and below the band
Character busts are NOT made here: they come from Graphics/EBDX/VS/<ID>.png (Gemini) or fall back to the
96x96 dialogue portrait (Graphics/Portraits/<ID>.png)."""
import os, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, 'graphics', 'EBDX', 'VS')
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans-BoldOblique.ttf'

# theme: (deep, mid, bright, streak) - deep at the band edges, bright in the centre glow
THEMES = {
    'green':  ((6, 44, 18),   (22, 132, 48),  (92, 226, 96),  (196, 255, 170)),
    'blue':   ((6, 18, 56),   (22, 70, 160),  (70, 150, 232), (190, 230, 255)),
    'rose':   ((58, 10, 34),  (168, 46, 98),  (240, 118, 160), (255, 214, 228)),
    'violet': ((28, 8, 58),   (96, 44, 168),  (168, 112, 236), (230, 206, 255)),
    'gold':   ((58, 34, 4),   (176, 116, 18), (246, 200, 70),  (255, 244, 190)),
    'red':    ((56, 6, 8),    (170, 30, 34),  (238, 90, 70),   (255, 206, 180)),
    'teal':   ((4, 40, 44),   (18, 120, 120), (80, 214, 200),  (200, 255, 244)),
    'grey':   ((22, 24, 30),  (78, 84, 98),   (150, 158, 174), (230, 234, 240)),
}
NW, NH = 256, 68          # native panel size (doubled -> 512x136)


def lerp(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def panel(theme):
    deep, mid, bright, streak = THEMES[theme]
    im = Image.new('RGB', (NW, NH))
    px = im.load()
    c = (NH - 1) / 2.0
    # banded vertical gradient (posterised to 7 steps, pixel-art style)
    for y in range(NH):
        d = abs(y - c) / c                     # 0 centre .. 1 edge
        t = round((1 - d) ** 1.6 * 6) / 6.0
        col = lerp(deep, mid, min(1, t * 1.6)) if t < 0.62 else lerp(mid, bright, (t - 0.62) / 0.38)
        for x in range(NW):
            px[x, y] = col
    rng = random.Random(theme)
    d = ImageDraw.Draw(im)
    # speed streaks, wrapped so the strip tiles horizontally
    for _ in range(46):
        y = int(rng.triangular(3, NH - 4, c))
        ln = rng.randint(10, 70)
        x0 = rng.randint(0, NW - 1)
        near = 1 - abs(y - c) / c
        col = lerp(mid, streak, 0.35 + 0.65 * near * rng.random())
        for x in range(x0, x0 + ln):
            px[x % NW, y] = col
        if rng.random() < 0.3:                 # a brighter head on some streaks
            for x in range(x0 + ln - 6, x0 + ln):
                px[x % NW, y] = streak
    return im.resize((NW * 2, NH * 2), Image.NEAREST)


def vs_logo():
    # render big, threshold to a native grid (no anti-aliasing), then outline/highlight/shadow
    big = Image.new('L', (720, 520), 0)
    ImageDraw.Draw(big).text((10, -60), 'VS', font=ImageFont.truetype(FONT, 520), fill=255)
    bb = big.getbbox(); big = big.crop(bb)
    nw = 60; nh = int(round(big.height * nw / big.width * 1.3))      # a little taller than the font
    m = big.resize((nw, nh), Image.LANCZOS).point(lambda v: 255 if v > 90 else 0)
    m = m.filter(ImageFilter.MaxFilter(3))                             # heavier strokes, Rejuv-chunky
    W, H = nw + 8, nh + 8
    fill_d, fill_m, fill_l, hi, out, shadow = (128, 10, 44), (198, 22, 66), (236, 58, 98), (255, 150, 172), (40, 4, 18), (14, 2, 8)
    canvas = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    cp = canvas.load(); mp = m.load()
    inside = lambda x, y: 0 <= x < nw and 0 <= y < nh and mp[x, y] > 0
    ox, oy = 3, 2
    # drop shadow (down-right 2), outline (8-neighbour), fill with banded shading
    for y in range(nh):
        for x in range(nw):
            if inside(x, y):
                for dx, dy in ((2, 2), (3, 2), (2, 3)):
                    cp[ox + x + dx, oy + y + dy] = shadow + (255,)
    for y in range(-1, nh + 1):
        for x in range(-1, nw + 1):
            if inside(x, y): continue
            if any(inside(x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)):
                cp[ox + x, oy + y] = out + (255,)
    for y in range(nh):
        for x in range(nw):
            if not inside(x, y): continue
            t = y / max(1, nh - 1)
            col = fill_l if t < 0.3 else (fill_m if t < 0.72 else fill_d)
            if not inside(x, y - 1) or not inside(x, y - 2): col = hi       # top-edge highlight
            cp[ox + x, oy + y] = col + (255,)
    # a white slash through the gap between V and S
    d = ImageDraw.Draw(canvas)
    sx = ox + int(nw * 0.47)
    for i in range(H):
        x = sx + 7 - int(i * 0.45)
        for k in range(2):
            if 0 <= x + k < W and canvas.getpixel((x + k, i))[3] > 0:
                cp[x + k, i] = (255, 240, 244, 255)
    return canvas.resize((W * 2, H * 2), Image.NEAREST)


def band_edge():
    w, h = 256, 4
    im = Image.new('RGBA', (w, h))
    rows = [(150, 156, 168), (98, 104, 118), (58, 62, 74), (20, 22, 28)]
    for y, col in enumerate(rows):
        for x in range(w):
            im.putpixel((x, y), col + (255,))
    for x in range(0, w, 32):                 # rivets
        im.putpixel((x + 6, 1), (200, 206, 216, 255))
    return im.resize((w * 2, h * 2), Image.NEAREST)


def main():
    os.makedirs(OUT, exist_ok=True)
    for t in THEMES:
        panel(t).save(os.path.join(OUT, f'panel_{t}.png'))
    vs_logo().save(os.path.join(OUT, 'vs_logo.png'))
    band_edge().save(os.path.join(OUT, 'band_edge.png'))
    print('wrote', OUT, sorted(os.listdir(OUT)))



# ---------------------------------------------------------------- B2W2 Elite Four-style VS (creator's reference video 2026-11-21)
import math


def bolt(seed):
    """512x88 lightning: a chain of diamonds (two interleaved zigzags), glow + orange + yellow-white core"""
    W, H = 256, 44
    rng = random.Random(seed)
    up, dn = [], []
    x = -6
    while x < W + 12:
        step = rng.randint(16, 28)
        c = H // 2 + rng.randint(-4, 4)
        a = rng.randint(7, 16)
        up += [(x, c), (x + step // 2, c - a)]
        dn += [(x, c), (x + step // 2, c + a)]
        x += step
    up.append((x, H // 2)); dn.append((x, H // 2))
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for pts in (up, dn):
        d.line(pts, fill=(200, 60, 6, 120), width=11)
    for pts in (up, dn):
        d.line(pts, fill=(246, 120, 18, 255), width=6)
    for pts in (up, dn):
        d.line(pts, fill=(255, 200, 64, 255), width=3)
    for pts in (up, dn):
        d.line(pts, fill=(255, 252, 228, 255), width=1)
    # hard alpha (pixel art): glow pixels stay semi only where wanted
    return im.resize((W * 2, H * 2), Image.NEAREST)


def tunnel(theme):
    """640x640 radial warp streaks for the VS background (rotated in-engine)"""
    deep, mid, bright, streak = THEMES[theme]
    N = 320
    im = Image.new('RGB', (N, N), tuple(int(v * 0.5) for v in deep))
    d = ImageDraw.Draw(im)
    rng = random.Random('tunnel' + theme)
    cx = cy = N / 2
    R = N * 0.75
    for i in range(90):
        a = rng.uniform(0, 2 * math.pi)
        wdt = rng.uniform(0.015, 0.06)
        r0 = rng.uniform(18, 70)
        t = rng.random()
        col = lerp(mid, streak, t * 0.7) if rng.random() < 0.4 else lerp(deep, mid, t)
        if rng.random() < 0.1: col = (236, 230, 250)
        pts = [(cx + r0 * math.cos(a), cy + r0 * math.sin(a)),
               (cx + R * math.cos(a - wdt), cy + R * math.sin(a - wdt)),
               (cx + R * math.cos(a + wdt), cy + R * math.sin(a + wdt))]
        d.polygon(pts, fill=col)
    # dark core
    for r in range(40, 0, -2):
        k = r / 40
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=lerp((4, 2, 8), tuple(int(v * 0.5) for v in deep), k))
    return im.resize((N * 2, N * 2), Image.NEAREST)


def band(theme, bright_left):
    """512x136 band background: black to the theme colour across, light sweeps"""
    deep, mid, bright, streak = THEMES[theme]
    W, H = 256, 68
    im = Image.new('RGB', (W, H))
    px = im.load()
    for x in range(W):
        u = x / (W - 1)
        if bright_left: u = 1 - u
        u = round(u ** 1.3 * 20) / 20.0                       # posterised, B2W2 cel steps
        col = lerp((6, 4, 10), deep, min(1, u * 2)) if u < 0.5 else lerp(deep, bright if u > 0.85 else mid, (u - 0.5) * 2)
        for y in range(H):
            px[x, y] = col
    d = ImageDraw.Draw(im)
    rng = random.Random('band' + theme + str(bright_left))
    for _ in range(4):                                     # diagonal light sweeps
        x0 = rng.randint(W // 3, W)
        w = rng.randint(2, 6)
        sx = x0 if not bright_left else W - x0
        col = lerp(deep, mid, rng.uniform(0.5, 0.9))
        pts = [(sx, 0), (sx + w, 0), (sx + w - 30, H), (sx - 30, H)]
        if bright_left: pts = [(W - p[0], p[1]) for p in pts]
        d.polygon(pts, fill=col)
    return im.resize((W * 2, H * 2), Image.NEAREST)


def emblem():
    """faint Poke Ball outline drawn across both bands behind the VS (300x300)"""
    N = 150
    im = Image.new('RGBA', (N, N), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    col = (160, 34, 26, 150)
    d.ellipse((2, 2, N - 3, N - 3), outline=col, width=4)
    d.rectangle((2, N // 2 - 2, N // 2 - 22, N // 2 + 2), fill=col)
    d.rectangle((N // 2 + 22, N // 2 - 2, N - 3, N // 2 + 2), fill=col)
    d.ellipse((N // 2 - 20, N // 2 - 20, N // 2 + 20, N // 2 + 20), outline=col, width=4)
    d.ellipse((N // 2 - 9, N // 2 - 9, N // 2 + 9, N // 2 + 9), outline=col, width=3)
    return im.resize((N * 2, N * 2), Image.NEAREST)


def spark():
    im = Image.new('RGBA', (5, 5), (0, 0, 0, 0))
    for (x, y), c in {(2, 2): (255, 240, 200, 255), (1, 2): (255, 120, 40, 255), (3, 2): (255, 120, 40, 255),
                      (2, 1): (255, 120, 40, 255), (2, 3): (255, 120, 40, 255), (1, 1): (220, 40, 20, 160),
                      (3, 3): (220, 40, 20, 160), (1, 3): (220, 40, 20, 160), (3, 1): (220, 40, 20, 160)}.items():
        im.putpixel((x, y), c)
    return im.resize((10, 10), Image.NEAREST)


def main_b2w2():
    os.makedirs(OUT, exist_ok=True)
    for i in range(3):
        bolt(i).save(os.path.join(OUT, f'bolt{i}.png'))
    for t in THEMES:
        tunnel(t).save(os.path.join(OUT, f'tunnel_{t}.png'))
        band(t, False).save(os.path.join(OUT, f'bandfoe_{t}.png'))
        band(t, True).save(os.path.join(OUT, f'bandplayer_{t}.png'))
    emblem().save(os.path.join(OUT, 'emblem.png'))
    spark().save(os.path.join(OUT, 'spark.png'))
    print('b2w2 set written')


if __name__ == '__main__':
    main_b2w2()
