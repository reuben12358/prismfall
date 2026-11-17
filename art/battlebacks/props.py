"""Procedural pixel-art props for Prismfall backdrops. Everything is drawn 1:1 at HD resolution
(1 px = 1 screen px at the default EBDX camera), aliased, with dark outlines, to sit with the
Rejuvenation/Reborn source art."""
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from bblib import *


def C(c, a=255):
    return (int(c[0]), int(c[1]), int(c[2]), a)


def mix(c1, c2, t):
    return tuple(int(round(c1[i] * (1 - t) + c2[i] * t)) for i in range(3))


def darker(c, f=0.7):
    return tuple(int(v * f) for v in c[:3])


def lighter(c, f=0.3):
    return tuple(int(v + (255 - v) * f) for v in c[:3])


#---------------------------------------------------------------------------------------------
# Platforms
#---------------------------------------------------------------------------------------------
def platform(canvas, center, rx, ry, top, side, outline=None, thick=7, seed=0, speckle=None,
             rim=None, highlight=True, texture=None):
    """Gen 5 style battle platform: an ellipse with a visible side band."""
    cx, cy = center
    d = ImageDraw.Draw(canvas)
    outline = outline or darker(side, 0.55)
    # side band (thickness)
    d.ellipse([cx - rx, cy - ry + thick, cx + rx, cy + ry + thick], fill=C(side), outline=C(outline))
    d.rectangle([cx - rx + 1, cy, cx + rx - 1, cy + thick], fill=C(side))
    d.line([cx - rx, cy, cx - rx, cy + thick], fill=C(outline))
    d.line([cx + rx, cy, cx + rx, cy + thick], fill=C(outline))
    # top face
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=C(top), outline=C(outline))
    if highlight:
        d.ellipse([cx - rx * 0.86, cy - ry * 0.8, cx + rx * 0.86, cy + ry * 0.66], fill=C(lighter(top, 0.08)))
        d.ellipse([cx - rx * 0.6, cy - ry * 0.55, cx + rx * 0.6, cy + ry * 0.35], fill=C(lighter(top, 0.14)))
    if rim:
        d.arc([cx - rx + 1, cy - ry + 1, cx + rx - 1, cy + ry - 1], 200, 340, fill=C(rim))
    if texture is not None:
        texture(canvas, center, rx, ry)
    if speckle:
        rng = random.Random(seed)
        cols, n = speckle
        for _ in range(n):
            a = rng.random() * 2 * math.pi
            r = math.sqrt(rng.random()) * 0.9
            x = cx + math.cos(a) * rx * r
            y = cy + math.sin(a) * ry * r
            d.point((x, y), fill=C(rng.choice(cols)))


def ring_stones(canvas, center, rx, ry, colors, n=22, size=(6, 10), seed=1, outline=(20, 16, 18)):
    """Ring of rocks/crystals/flowers around a platform's edge."""
    rng = random.Random(seed)
    d = ImageDraw.Draw(canvas)
    pts = []
    for i in range(n):
        a = (i / n) * 2 * math.pi + rng.uniform(-0.08, 0.08)
        pts.append((math.sin(a), a))
    pts.sort()  # back (top) first
    for _, a in pts:
        x = center[0] + math.cos(a) * rx
        y = center[1] + math.sin(a) * ry
        w = rng.randint(*size); h = int(w * 0.75)
        col = rng.choice(colors)
        d.ellipse([x - w / 2, y - h, x + w / 2, y + 2], fill=C(col), outline=C(outline))
        d.line([x - w / 4, y - h + 2, x, y - h + 2], fill=C(lighter(col, 0.35)))


#---------------------------------------------------------------------------------------------
# Machinery
#---------------------------------------------------------------------------------------------
def gear(r, teeth=12, tooth=None, hole=None, spokes=5, base=(120, 125, 135), outline=(25, 25, 30),
         light=None, dark=None, broken=False, seed=0):
    """Pixel gear, centred in a square RGBA image; rotate in-engine about its centre."""
    tooth = tooth or max(4, r // 6)
    hole = hole if hole is not None else max(4, r // 5)
    light = light or lighter(base, 0.35)
    dark = dark or darker(base, 0.6)
    R = r + tooth
    size = 2 * R + 4
    c = size / 2
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    poly = []
    n = teeth * 4
    for i in range(n):
        a = i / n * 2 * math.pi
        k = i % 4
        rr = R if k in (1, 2) else r
        poly.append((c + math.cos(a) * rr, c + math.sin(a) * rr))
    d.polygon(poly, fill=C(outline))
    inner = []
    for (x, y) in poly:
        dx, dy = x - c, y - c
        L = math.hypot(dx, dy)
        inner.append((c + dx * (L - 1.5) / L, c + dy * (L - 1.5) / L))
    d.polygon(inner, fill=C(base))
    # bevel: light upper-left arc band, dark lower-right
    a = np.asarray(im).astype(np.float32)
    ys, xs = np.mgrid[0:size, 0:size].astype(np.float32)
    dx, dy = xs - c, ys - c
    dist = np.sqrt(dx * dx + dy * dy) + 1e-3
    ldot = (-dx - dy) / (dist * 1.414)
    body = a[..., 3] > 0
    band = (dist > r * 0.78) & body & (np.abs(a[..., 0] - base[0]) < 2)
    a[band & (ldot > 0.35)] = C(light)
    a[band & (ldot < -0.35)] = C(dark)
    # web ring and spokes cut-outs
    ring_in = r * 0.72
    hub = max(hole + 4, r * 0.28)
    cut = (dist < ring_in - 2) & (dist > hub + 2)
    if spokes > 0:
        ang = np.arctan2(dy, dx)
        sw = 0.22 if r > 30 else 0.3
        on_spoke = np.zeros_like(cut)
        for i in range(spokes):
            t = i / spokes * 2 * math.pi + 0.3
            diff = np.abs(((ang - t + math.pi) % (2 * math.pi)) - math.pi)
            on_spoke |= diff * dist < r * sw * 0.5
        cut = cut & ~on_spoke
    rim_out = cut & ~((dist < ring_in - 3) & (dist > hub + 3))
    a[cut] = 0
    a[rim_out] = C(outline)
    # spoke shading
    sp = body & (dist < ring_in - 2) & (dist > hub + 2) & ~cut
    a[sp & (ldot > 0.2)] = C(light)
    # hub + hole
    hubm = dist <= hub
    a[hubm] = C(base)
    a[hubm & (dist > hub - 1.5)] = C(outline)
    a[hubm & (dist < hub - 1.5) & (ldot > 0.4)] = C(light)
    a[dist <= hole] = C(outline)
    a[dist <= hole - 1.5] = 0
    if broken:
        rng = random.Random(seed)
        # a missing wedge of teeth and a crack
        t0 = rng.uniform(0, 2 * math.pi)
        ang = np.arctan2(dy, dx)
        diff = np.abs(((ang - t0 + math.pi) % (2 * math.pi)) - math.pi)
        a[(diff < 0.45) & (dist > r * 0.86)] = 0
        crack = (np.abs(((ang - t0 - 0.9 + math.pi) % (2 * math.pi)) - math.pi) * dist < 1.2) & (dist > hub)
        a[crack & body] = C(outline)
    return img(a)


def chain(length, link=(6, 9), color=(90, 92, 100), outline=(20, 20, 24)):
    w, h = link
    im = Image.new("RGBA", (w + 2, length), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    y, i = 0, 0
    while y < length - 2:
        if i % 2 == 0:
            d.ellipse([0, y, w, y + h], outline=C(outline), width=3)
            d.ellipse([1, y + 1, w - 1, y + h - 1], outline=C(color), width=1)
        else:
            d.rectangle([w // 2 - 1, y - 1, w // 2 + 1, y + h + 1], fill=C(outline))
            d.line([w // 2, y, w // 2, y + h], fill=C(color))
        y += h - 3
        i += 1
    return im


def hook(color=(110, 110, 118), outline=(20, 20, 24)):
    im = Image.new("RGBA", (22, 26), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([8, 0, 13, 8], fill=C(color), outline=C(outline))
    d.arc([2, 6, 20, 24], 330, 220, fill=C(outline), width=5)
    d.arc([3, 7, 19, 23], 330, 220, fill=C(color), width=2)
    return im


def girder(length, h=14, color=(70, 76, 88), outline=(18, 18, 22), vertical=False):
    """Lattice girder (truss)."""
    w = length
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w - 1, 2], fill=C(color), outline=C(outline))
    d.rectangle([0, h - 3, w - 1, h - 1], fill=C(color), outline=C(outline))
    step = h
    for x in range(0, w, step):
        d.line([x, 2, x + step // 2, h - 3], fill=C(outline), width=3)
        d.line([x + step // 2, h - 3, x + step, 2], fill=C(outline), width=3)
        d.line([x, 2, x + step // 2, h - 3], fill=C(color), width=1)
        d.line([x + step // 2, h - 3, x + step, 2], fill=C(color), width=1)
    return im.rotate(90, expand=True) if vertical else im


def pipe(canvas, pts, w, color, outline=(15, 15, 18), light=None):
    d = ImageDraw.Draw(canvas)
    light = light or lighter(color, 0.3)
    d.line(pts, fill=C(outline), width=w + 2, joint="curve")
    d.line(pts, fill=C(color), width=w, joint="curve")
    # highlight
    hp = [(x, y - w // 3) for x, y in pts]
    d.line(hp, fill=C(light), width=max(1, w // 4))
    for (x, y) in pts[1:-1]:
        d.ellipse([x - w / 2 - 2, y - w / 2 - 2, x + w / 2 + 2, y + w / 2 + 2], fill=C(darker(color, 0.8)), outline=C(outline))


#---------------------------------------------------------------------------------------------
# Nature
#---------------------------------------------------------------------------------------------
def web(size, spokes=14, rings=11, color=(255, 255, 250), alpha=150, seed=0, dew=True):
    """Orb web centred in a square RGBA image; returns (image, dew points)."""
    rng = random.Random(seed)
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = size / 2
    R = size / 2 - 2
    angs = sorted(i / spokes * 2 * math.pi + rng.uniform(-0.12, 0.12) for i in range(spokes))
    lens = [R * rng.uniform(0.82, 1.0) for _ in angs]
    col = C(color, alpha)
    for a, L in zip(angs, lens):
        d.line([c, c, c + math.cos(a) * L, c + math.sin(a) * L], fill=col)
    drops = []
    for k in range(1, rings + 1):
        f = k / (rings + 0.6)
        pts = []
        for a, L in zip(angs + [angs[0]], lens + [lens[0]]):
            rr = L * f
            pts.append((c + math.cos(a) * rr, c + math.sin(a) * rr))
        # sag between spokes
        for i in range(len(pts) - 1):
            (x0, y0), (x1, y1) = pts[i], pts[i + 1]
            mx, my = (x0 + x1) / 2, (y0 + y1) / 2
            vx, vy = mx - c, my - c
            L = math.hypot(vx, vy) + 1e-3
            mx -= vx / L * 2.5 * f
            my -= vy / L * 2.5 * f
            d.line([x0, y0, mx, my, x1, y1], fill=C(color, int(alpha * (0.75 + 0.25 * f))))
            if dew and rng.random() < 0.18:
                drops.append((mx, my))
    # hub
    d.ellipse([c - 3, c - 3, c + 3, c + 3], outline=C(color, alpha))
    for (x, y) in drops:
        d.point((x, y), fill=(255, 255, 255, 255))
        d.point((x + 1, y), fill=(220, 240, 255, 230))
    return im, drops


def strand(length, sag=0, color=(250, 250, 245), alpha=170, width=1):
    im = Image.new("RGBA", (max(6, int(abs(sag)) * 2 + 6), length), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx = im.width // 2
    pts = [(cx + sag * math.sin(t / length * math.pi), t) for t in range(0, length, 3)]
    d.line(pts, fill=C(color, alpha), width=width)
    # silk clump at the end
    d.ellipse([cx - 2, length - 6, cx + 2, length - 1], fill=C(color, alpha))
    return im


def crystal(h, w, base, outline=(25, 20, 40), lean=0.0, seed=0):
    """One hexagonal crystal prism pointing up (pivot at bottom centre)."""
    rng = random.Random(seed)
    W = int(w * 2 + abs(lean) * h + 8)
    H = int(h + 8)
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    bx = W / 2 - lean * h / 2
    by = H - 2
    tx = bx + lean * h
    ty = by - h
    shaft = h * 0.72
    sx = bx + lean * shaft
    sy = by - shaft
    hw = w / 2
    L = [(bx - hw, by), (sx - hw, sy), (tx, ty), (sx, sy + 3), (bx, by + 1)]
    R = [(bx, by + 1), (sx, sy + 3), (tx, ty), (sx + hw, sy), (bx + hw, by)]
    d.polygon(L, fill=C(lighter(base, 0.25)), outline=C(outline))
    d.polygon(R, fill=C(darker(base, 0.7)), outline=C(outline))
    # facet highlight
    d.line([(bx - hw * 0.45, by - 3), (sx - hw * 0.45, sy + 2)], fill=C(lighter(base, 0.6)))
    d.point((tx, ty + 3), fill=(255, 255, 255, 255))
    return im, (int(round(bx)), int(round(by)))


def crystal_cluster(canvas, foot, scale, palette, seed=0, n=5, outline=(25, 20, 40)):
    rng = random.Random(seed)
    items = []
    for i in range(n):
        h = int(scale * rng.uniform(0.45, 1.0))
        w = max(6, int(h * rng.uniform(0.22, 0.32)))
        lean = rng.uniform(-0.45, 0.45) * (0.4 if i == 0 else 1)
        dx = int(rng.uniform(-0.5, 0.5) * scale * 0.7) if i else 0
        items.append((h, w, lean, dx, rng.choice(palette)))
    items.sort(key=lambda t: -t[0])
    for h, w, lean, dx, col in items:
        cr, (px, py) = crystal(h, w, col, outline, lean, seed + h)
        canvas.alpha_composite(cr, (int(foot[0] + dx - px), int(foot[1] - py)))


def mountains(size, base_y, height, color, seed=0, rough=0.5, snow=None, outline=None, peaks=5):
    """Ridge silhouette band (RGBA) with optional snow caps."""
    w, h = size
    rng = np.random.RandomState(seed)
    xs = np.arange(w)
    prof = np.zeros(w, np.float32)
    for k in range(1, 6):
        ph = rng.uniform(0, 2 * np.pi)
        prof += np.sin(xs / w * 2 * np.pi * (peaks * k / 2.0) + ph) / (k ** (1.6 - rough))
    prof = (prof - prof.min()) / (prof.max() - prof.min() + 1e-6)
    tops = (base_y - prof * height).astype(int)
    im = Image.new("RGBA", size, (0, 0, 0, 0))
    a = np.zeros((h, w, 4), np.float32)
    for x in range(w):
        t = max(tops[x], 0)
        a[t:base_y + 1, x] = C(color)
        if outline is not None:
            a[t, x] = C(outline)
        if snow is not None:
            depth = int(6 + 10 * (1 - (tops[x] - tops.min()) / (height + 1)))
            if tops[x] < base_y - height * 0.45:
                a[t + 1:t + 1 + depth, x] = C(snow)
    # simple light/shadow by slope
    for x in range(1, w):
        if tops[x] > tops[x - 1] and snow is None:
            a[tops[x]:tops[x] + 4, x, :3] = np.array(lighter(color, 0.12))
    return img(a)


def pine(h, color=(30, 60, 50), outline=(10, 22, 18), snow=None, seed=0):
    rng = random.Random(seed)
    w = int(h * 0.42)
    im = Image.new("RGBA", (w + 4, h + 4), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx = (w + 4) / 2
    d.rectangle([cx - 2, h - h * 0.12, cx + 2, h + 2], fill=C((60, 40, 30)), outline=C(outline))
    tiers = 5
    for i in range(tiers):
        t0 = i / tiers
        y_top = 2 + h * 0.85 * t0
        y_bot = 2 + h * 0.85 * (t0 + 1.0 / tiers) + h * 0.08
        hw = (w / 2) * (0.35 + 0.65 * (i + 1) / tiers)
        poly = [(cx, y_top), (cx + hw, y_bot), (cx - hw, y_bot)]
        d.polygon(poly, fill=C(color), outline=C(outline))
        d.line([(cx, y_top + 2), (cx - hw + 3, y_bot - 1)], fill=C(lighter(color, 0.15)))
        if snow:
            d.line([(cx - hw + 2, y_bot - 1), (cx + hw - 2, y_bot - 1)], fill=C(snow), width=2)
            d.line([(cx, y_top + 1), (cx - hw * 0.5, (y_top + y_bot) / 2)], fill=C(snow))
    return im


def dead_tree(h, color=(40, 34, 30), outline=(12, 10, 10), seed=0):
    rng = random.Random(seed)
    im = Image.new("RGBA", (h, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)

    def branch(x, y, ang, L, w):
        if L < 5:
            return
        w = max(w, 1)
        x2 = x + math.cos(ang) * L
        y2 = y + math.sin(ang) * L
        d.line([x, y, x2, y2], fill=C(outline), width=w + 2)
        d.line([x, y, x2, y2], fill=C(color), width=w)
        for s in (-1, 1):
            if rng.random() < 0.8:
                branch(x2, y2, ang + s * rng.uniform(0.3, 0.7), L * rng.uniform(0.6, 0.78), w - 1)

    branch(h / 2, h - 2, -math.pi / 2, h * 0.38, max(3, h // 14))
    return im


def reeds(w, h, color=(70, 80, 50), outline=(20, 22, 14), n=14, seed=0, heads=(90, 60, 40)):
    rng = random.Random(seed)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i in range(n):
        x = rng.uniform(2, w - 2)
        top = rng.uniform(0, h * 0.5)
        bend = rng.uniform(-10, 10)
        pts = [(x + bend * (1 - t / 10.0) ** 2, top + (h - top) * t / 10.0) for t in range(11)]
        d.line(pts, fill=C(outline), width=3)
        d.line(pts, fill=C(color), width=1)
        if heads and rng.random() < 0.6:
            hx, hy = pts[0]
            d.ellipse([hx - 2, hy, hx + 2, hy + 10], fill=C(heads), outline=C(outline))
    return im


def skyline(size, base_y, color, seed=0, min_h=30, max_h=140, min_w=18, max_w=60, windows=None, win_p=0.25,
            outline=None):
    rng = random.Random(seed)
    w, h = size
    im = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x = -rng.randint(0, 20)
    wins = []
    while x < w:
        bw = rng.randint(min_w, max_w)
        bh = rng.randint(min_h, max_h)
        top = base_y - bh
        d.rectangle([x, top, x + bw, base_y], fill=C(color), outline=C(outline) if outline else None)
        if rng.random() < 0.35:
            d.rectangle([x + bw // 3, top - rng.randint(6, 18), x + bw // 3 + 3, top], fill=C(color))
        if windows:
            for wy in range(top + 6, base_y - 6, 9):
                for wx in range(x + 4, x + bw - 4, 7):
                    if rng.random() < win_p:
                        d.rectangle([wx, wy, wx + 2, wy + 3], fill=C(rng.choice(windows)))
                        wins.append((wx, wy))
        x += bw + rng.randint(-4, 6)
    return im, wins


def cloud_band(width, height, color, shade, seed=0, density=0.5, scale=20, levels=5, alpha=255):
    """Puffy pixel cloud band (tileable)."""
    from paint import tile_noise
    n = tile_noise(width, height, scale, seed, 3)
    t = np.linspace(0, 1, height)[:, None]
    n = n * (0.6 + 0.6 * np.sin(np.clip(t, 0, 1) * np.pi))
    v = np.clip((n - (1 - density)) / density, 0, 1)
    out = np.zeros((height, width, 4), np.float32)
    q = np.round(v * levels) / levels
    for c in range(3):
        out[..., c] = shade[c] + (color[c] - shade[c]) * np.clip(q * 1.3, 0, 1)
    out[..., 3] = (q > 0) * alpha
    return img(out)


#---------------------------------------------------------------------------------------------
# Architecture / interiors
#---------------------------------------------------------------------------------------------
def curtain(w, h, color=(150, 20, 34), dark=None, light=None, folds=7, hem=(220, 170, 60), seed=0, gather=0.0):
    """Velvet drape with vertical folds (RGBA)."""
    dark = dark or darker(color, 0.45)
    light = light or lighter(color, 0.25)
    xs = np.arange(w)[None, :].astype(np.float32)
    ys = np.arange(h)[:, None].astype(np.float32)
    # gather: folds narrow toward the bottom (tied back)
    f = folds * (1 + gather * (ys / h))
    ph = np.sin(xs / w * np.pi * 2 * f / 2 + np.sin(ys / 40.0) * 0.4)
    q = np.round((ph * 0.5 + 0.5) * 4) / 4
    out = np.zeros((h, w, 4), np.float32)
    for c in range(3):
        out[..., c] = np.where(q < 0.5, dark[c] + (color[c] - dark[c]) * q * 2,
                               color[c] + (light[c] - color[c]) * (q - 0.5) * 2)
    out[..., 3] = 255
    im = img(out)
    d = ImageDraw.Draw(im)
    if hem:
        d.rectangle([0, h - 6, w, h - 1], fill=C(hem))
        for x in range(0, w, 4):
            d.line([x, h - 6, x, h - 1], fill=C(darker(hem, 0.7)))
    return im


def valance(w, h, color=(150, 20, 34), swags=5, fringe=(230, 180, 70)):
    im = Image.new("RGBA", (w, h + 10), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    dark = darker(color, 0.5)
    sw = w / swags
    d.rectangle([0, 0, w, h * 0.45], fill=C(color))
    for i in range(swags):
        x0 = i * sw
        for k in range(5):
            t = k / 5.0
            col = mix(dark, lighter(color, 0.2), t)
            d.chord([x0 - 2 + k * 2, -h * 0.4 + k, x0 + sw + 2 - k * 2, h - k * 2], 0, 180, fill=C(col))
        d.arc([x0, -h * 0.4, x0 + sw, h], 0, 180, fill=C(fringe), width=3)
        for j in range(9):
            a = math.pi * (j + 0.5) / 9
            fx = x0 + sw / 2 + math.cos(a) * sw / 2
            fy = h * 0.3 + math.sin(a) * h * 0.7
            d.line([fx, fy, fx, fy + 6], fill=C(fringe))
    d.rectangle([0, 0, w, 6], fill=C(fringe))
    return im


def rose_window(r, glass, lead=(20, 14, 26), frame=(70, 60, 80), seed=0):
    rng = random.Random(seed)
    size = 2 * r + 8
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = size / 2
    d.ellipse([c - r - 3, c - r - 3, c + r + 3, c + r + 3], fill=C(frame), outline=C(lead))
    d.ellipse([c - r, c - r, c + r, c + r], fill=C(lead))
    petals = 12
    for ring, (r0, r1) in enumerate([(r * 0.62, r * 0.96), (r * 0.3, r * 0.6)]):
        for i in range(petals if ring == 0 else 8):
            n = petals if ring == 0 else 8
            a0 = i / n * 360
            a1 = (i + 1) / n * 360
            col = glass[(i + ring) % len(glass)]
            d.pieslice([c - r1, c - r1, c + r1, c + r1], a0 + 2, a1 - 2, fill=C(col))
            d.pieslice([c - r0, c - r0, c + r0, c + r0], a0, a1, fill=C(lead))
    d.ellipse([c - r * 0.26, c - r * 0.26, c + r * 0.26, c + r * 0.26], fill=C(glass[0]), outline=C(lead))
    # light grain
    for _ in range(r * 2):
        a = rng.random() * 2 * math.pi; rr = rng.random() * r * 0.95
        x, y = c + math.cos(a) * rr, c + math.sin(a) * rr
        px = im.getpixel((int(x), int(y)))
        if px[3] and px[:3] != lead:
            d.point((x, y), fill=C(lighter(px, 0.4)))
    return im


def gothic_arch(w, h, color, outline=(15, 10, 20), inner=None, light=None):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    light = light or lighter(color, 0.2)
    # outer pointed arch
    pts = []
    for i in range(41):
        t = i / 40
        a = math.pi * t
        x = w / 2 - math.cos(a) * w / 2
        y = h * 0.35 * (1 - math.sin(a)) ** 0.8
        pts.append((x, y))
    poly = [(0, h)] + [(x, y + h * 0.0) for x, y in pts] + [(w, h)]
    d.polygon(poly, fill=C(color), outline=C(outline))
    if inner:
        m = 6
        pts2 = [(m + (x - m) * (w - 2 * m) / w if False else x * (w - 2 * m) / w + m, y + m * 1.5) for x, y in pts]
        d.polygon([(m, h)] + pts2 + [(w - m, h)], fill=C(inner), outline=C(outline))
    return im


def planks(size, color=(120, 80, 50), seam=(60, 38, 24), horizon_y=0, vanish_x=None, n=18, seed=0):
    """Perspective floorboards converging to a vanishing point above `horizon_y`."""
    w, h = size
    vx = vanish_x if vanish_x is not None else w / 2
    rng = np.random.RandomState(seed)
    ys, xs = np.mgrid[0:h, 0:w].astype(np.float32)
    depth = np.clip((ys - horizon_y) / (h - horizon_y), 1e-3, 1)
    u = (xs - vx) / depth / (w / n)
    board = np.floor(u)
    frac = u - board
    tone = rng.uniform(0.85, 1.12, 512)
    t = tone[(board.astype(int) % 512)]
    out = np.zeros((h, w, 4), np.float32)
    for c in range(3):
        out[..., c] = color[c] * t
    edge = (frac < 0.06 / np.maximum(depth, 0.2))
    for c in range(3):
        out[..., c] = np.where(edge, seam[c], out[..., c])
    # cross seams
    v = 1.0 / depth
    cross = (np.abs(((v * 3 + board * 0.37) % 1.0)) < 0.04)
    for c in range(3):
        out[..., c] = np.where(cross & (ys > horizon_y), seam[c], out[..., c])
    out[..., 3] = np.where(ys >= horizon_y, 255, 0)
    return img(out)


def lamp(color=(255, 210, 120), body=(60, 56, 50), outline=(15, 14, 12), cage=True):
    im = Image.new("RGBA", (24, 30), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([10, 0, 13, 6], fill=C(body), outline=C(outline))
    d.polygon([(3, 14), (20, 14), (16, 6), (7, 6)], fill=C(body), outline=C(outline))
    d.ellipse([7, 12, 16, 22], fill=C(color), outline=C(outline))
    d.point((10, 15), fill=(255, 255, 255, 255))
    if cage:
        d.line([8, 14, 9, 22], fill=C(outline)); d.line([15, 14, 14, 22], fill=C(outline))
    return im


def cone(size, apex, spread, length, color, alpha=90, levels=6, angle=90):
    """Soft light cone (RGBA) from apex pointing at `angle` degrees (90 = down)."""
    w, h = size
    ys, xs = np.mgrid[0:h, 0:w].astype(np.float32)
    dx, dy = xs - apex[0], ys - apex[1]
    a = math.radians(angle)
    along = dx * math.cos(a) + dy * math.sin(a)
    across = -dx * math.sin(a) + dy * math.cos(a)
    halfw = np.maximum(along, 0) * math.tan(math.radians(spread / 2)) + 1
    v = np.clip(1 - np.abs(across) / halfw, 0, 1) * np.clip(1 - along / length, 0, 1) * (along > 0)
    v = np.round(v ** 0.8 * levels) / levels
    out = np.zeros((h, w, 4), np.float32)
    out[..., 0], out[..., 1], out[..., 2] = color
    out[..., 3] = v * alpha
    return img(out)


def side_walls(size, inner_x=(170, 700), top_y=0, bottom_y=693, color=(20, 10, 26), rim=(255, 130, 60),
               seed=0, jag=26, rim_w=2, ceiling=60):
    """Dark rock masses closing in from both sides and the ceiling (a cave mouth frame)."""
    w, h = size
    rng = np.random.RandomState(seed)
    ys = np.arange(h)
    n1 = noise((1, h), 5, seed, 3)[:, 0] if False else noise((h, 1), 4, seed, 3)[:, 0]
    n2 = noise((h, 1), 4, seed + 1, 3)[:, 0]
    t = ys / float(h)
    # walls bulge in toward the middle height
    lx = inner_x[0] * (0.35 + 0.65 * np.sin(np.clip(t, 0, 1) * np.pi) ** 0.6) + (n1 - 0.5) * jag * 2
    rx = w - (w - inner_x[1]) * (0.35 + 0.65 * np.sin(np.clip(t, 0, 1) * np.pi) ** 0.6) + (n2 - 0.5) * jag * 2
    xs = np.arange(w)
    nc = noise((w, 1), 5, seed + 2, 3)[:, 0] if False else noise((1, w), 5, seed + 2, 3)[0]
    ceil = ceiling * (1 - np.sin(np.clip(xs / w, 0, 1) * np.pi) ** 0.5 * 0.6) + (nc - 0.5) * jag * 2
    a = np.zeros((h, w, 4), np.float32)
    X, Y = np.meshgrid(xs, ys)
    m = (X < lx[:, None]) | (X > rx[:, None]) | (Y < ceil[None, :])
    a[m] = [color[0], color[1], color[2], 255]
    # rim light on the inner edges
    mi = Image.fromarray((m * 255).astype(np.uint8))
    er = np.asarray(mi.filter(ImageFilter.MinFilter(rim_w * 2 + 1)), np.float32) > 0
    edge = m & ~er
    a[edge] = [rim[0], rim[1], rim[2], 255]
    er2 = np.asarray(mi.filter(ImageFilter.MinFilter(rim_w * 4 + 3)), np.float32) > 0
    e2 = er & ~er2
    mid = [int(color[0] * 0.5 + rim[0] * 0.5), int(color[1] * 0.5 + rim[1] * 0.5), int(color[2] * 0.5 + rim[2] * 0.5)]
    a[e2] = [mid[0], mid[1], mid[2], 255]
    return img(a)


def ground_plane(size, horizon, near, far, seed=0, cracks=None, crack_n=24, vanish_x=512, grain=4):
    """Rocky perspective floor from `horizon` down: far colour -> near colour, with optional cracks."""
    w, h = size
    ys = np.arange(h)[:, None].astype(np.float32)
    t = np.clip((ys - horizon) / (h - horizon), 0, 1)
    n = noise(size, grain, seed, 3)
    a = np.zeros((h, w, 4), np.float32)
    for c in range(3):
        a[..., c] = far[c] + (near[c] - far[c]) * t + (n - 0.5) * 40 * (0.3 + t)
    a[..., 3] = np.where(ys >= horizon, 255, 0) * np.ones((1, w))
    im = quantize_rgb(img(a), 10)
    crack_img = None
    if cracks:
        crack_img = Image.new("RGBA", size, (0, 0, 0, 0))
        d = ImageDraw.Draw(crack_img)
        rng = random.Random(seed)
        for i in range(crack_n):
            ang = rng.uniform(0.15, math.pi - 0.15)
            x, y = vanish_x + math.cos(ang) * 30, horizon + 4
            L = rng.uniform(80, 400)
            pts = [(x, y)]
            for k in range(8):
                x += math.cos(ang) * L / 8 + rng.uniform(-8, 8)
                y += abs(math.sin(ang)) * L / 8 * (0.4 + k / 8.0)
                pts.append((x, y))
            d.line(pts, fill=C(cracks), width=1)
    return im, crack_img
