#!/usr/bin/env python3
"""Builds the Rejuvenation-style trainer VS screen UI art (Prismfall EBDX Bridge 010_Bridge_VersusIntro.rb).

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


if __name__ == '__main__':
    main()
