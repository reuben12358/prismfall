"""Procedural pixel-art painters and EBDX layer-spec helpers for Prismfall backdrops."""
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from bblib import *
from rubygen import S

INV = 1.0 / 2.25   # exact: drawn at 1:1 on screen at the default camera


def blank(size=HD):
    return Image.new("RGBA", size, (0, 0, 0, 0))


#---------------------------------------------------------------------------------------------
# Layer specs (Bridge :layers and EBDX art_extras images)
#---------------------------------------------------------------------------------------------
def layer(field, tag, im, anchor=None, z=1, crop=True, **kw):
    """Save an HD-resolution element and return a Bridge :layers spec.
    `anchor` = pivot in HD canvas coords (default: top-left of the cropped image)."""
    name = "pf_%s_%s" % (field, tag)
    x0, y0 = 0, 0
    if crop:
        bb = im.getchannel("A").getbbox()
        if bb:
            pad = 2
            bb = (max(bb[0] - pad, 0), max(bb[1] - pad, 0), min(bb[2] + pad, im.width), min(bb[3] + pad, im.height))
            im = im.crop(bb)
            x0, y0 = bb[0], bb[1]
    save_element(name, im)
    if anchor is None:
        anchor = (x0, y0)
    spec = {S("bitmap"): name, S("hd"): True,
            S("x"): round(anchor[0] / 2.25, 2), S("y"): round(anchor[1] / 2.25, 2),
            S("ox"): int(round(anchor[0] - x0)), S("oy"): int(round(anchor[1] - y0)), S("z"): z}
    for k, v in kw.items():
        spec[S(k)] = v
    return spec


def strip(field, tag, im, y_hd, speed=0.5, direction=1, z=3, opacity=255, vertical=False):
    """Save a horizontally tileable HD strip and return an EBDX scrolling img entry."""
    name = "pf_%s_%s" % (field, tag)
    save_element(name, im)
    d = {S("bitmap"): name, S("scrolling"): True, S("speed"): speed, S("direction"): direction,
         S("flat"): True, S("ox"): 0, S("oy"): 0, S("x"): 0, S("y"): round(y_hd / 2.25, 2),
         S("zoom_x"): INV, S("zoom_y"): INV, S("z"): z}
    if opacity != 255:
        d[S("opacity")] = opacity
    if vertical:
        d[S("vertical")] = True
    return d


def ebdx_stock(bitmap, **kw):
    d = {S("bitmap"): bitmap}
    for k, v in kw.items():
        d[S(k)] = v
    return d


#---------------------------------------------------------------------------------------------
# Masks and glows
#---------------------------------------------------------------------------------------------
def mask_from(im, fn):
    a = arr(im)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    return fn(r, g, b).astype(np.float32)


def glow_from_mask(mask, color, radius=6, gain=1.6, core=0.6, size=HD):
    """Additive-friendly glow: blurred mask (halo) + the mask itself (core)."""
    m = Image.fromarray((np.clip(mask, 0, 1) * 255).astype(np.uint8))
    halo = np.asarray(m.filter(ImageFilter.GaussianBlur(radius)), np.float32) / 255.0
    al = np.clip(halo * gain + np.clip(mask, 0, 1) * core, 0, 1)
    out = np.zeros((mask.shape[0], mask.shape[1], 4), np.float32)
    out[..., 0], out[..., 1], out[..., 2] = color[0], color[1], color[2]
    out[..., 3] = al * 255
    return posterize_alpha(img(out), 10)


def soft_glow(center, radius, color, alpha=255, squash=1.0, power=1.8, size=HD):
    return posterize_alpha(radial(size, center, radius, (color[0], color[1], color[2], alpha), power, squash), 12)


def tile_noise(width, height, scale=24, seed=1, octaves=3):
    """Horizontally seamless value noise 0..1."""
    ov = max(8, width // 5)
    n = noise((width + ov, height), scale, seed, octaves)
    t = np.linspace(0, 1, ov)[None, :]
    n[:, :ov] = n[:, width:width + ov] * (1 - t) + n[:, :ov] * t
    return n[:, :width]


def fog_strip(width, height, color, seed=1, scale=24, density=0.55, alpha=150, fade_top=True, fade_bottom=True,
              levels=8):
    """Tileable soft fog/haze band (RGBA)."""
    n = tile_noise(width, height, scale, seed)
    v = np.clip((n - (1 - density)) / max(density, 1e-3), 0, 1)
    t = np.linspace(0, 1, height)[:, None]
    env = np.ones_like(t)
    if fade_top:
        env = env * np.clip(t / 0.35, 0, 1)
    if fade_bottom:
        env = env * np.clip((1 - t) / 0.35, 0, 1)
    v = v * env
    out = np.zeros((height, width, 4), np.float32)
    out[..., 0], out[..., 1], out[..., 2] = color
    out[..., 3] = v * alpha
    return posterize_alpha(img(out), levels)


#---------------------------------------------------------------------------------------------
# Shapes
#---------------------------------------------------------------------------------------------
def shade_rect(d, x0, y0, x1, y1, base, light, dark, outline=None, bands=3):
    d.rectangle([x0, y0, x1, y1], fill=base)
    w = x1 - x0
    d.rectangle([x0, y0, x0 + max(1, w // 6), y1], fill=light)
    d.rectangle([x1 - max(1, w // 5), y0, x1, y1], fill=dark)
    if outline:
        d.rectangle([x0, y0, x1, y1], outline=outline)


def pillar(canvas, x, top, bottom, w, stone, light, dark, outline, cap=True, rim=None, rim_side=1):
    d = ImageDraw.Draw(canvas)
    x0, x1 = x - w // 2, x + w // 2
    shade_rect(d, x0, top, x1, bottom, stone, light, dark, outline)
    # vertical facets
    for fx in range(x0 + w // 3, x1 - 2, max(4, w // 3)):
        d.line([fx, top + 4, fx, bottom - 4], fill=dark)
    if cap:
        shade_rect(d, x0 - 6, top - 10, x1 + 6, top, stone, light, dark, outline)
        shade_rect(d, x0 - 8, bottom - 8, x1 + 8, bottom + 4, stone, light, dark, outline)
    if rim:
        rx = x0 + 1 if rim_side < 0 else x1 - 2
        d.line([rx, top + 2, rx, bottom - 2], fill=rim)
        d.line([rx - rim_side, top + 2, rx - rim_side, bottom - 2], fill=tuple(int(c * 0.7) for c in rim))


def banner(w, h, cloth, trim, emblem, outline=(20, 8, 8, 255), tail=14, seed=3):
    """Hanging swallow-tail banner with a flame/dragon emblem, pivot at top centre."""
    im = Image.new("RGBA", (w + 8, h + 12), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x0, x1 = 4, 4 + w
    poly = [(x0, 6), (x1, 6), (x1, h), ((x0 + x1) // 2, h - tail), (x0, h)]
    d.polygon(poly, fill=cloth, outline=outline)
    dark = tuple(int(c * 0.72) for c in cloth[:3]) + (255,)
    # folds
    for fx in range(x0 + 4, x1 - 2, 7):
        d.line([fx, 8, fx, h - 6 - (tail if abs(fx - (x0 + x1) // 2) < 4 else 0)], fill=dark)
    # trim
    d.rectangle([x0, 6, x1, 10], fill=trim, outline=outline)
    d.line([x0 + 2, h - 2, (x0 + x1) // 2, h - tail - 2], fill=trim)
    d.line([x1 - 2, h - 2, (x0 + x1) // 2, h - tail - 2], fill=trim)
    # rod
    d.rectangle([0, 3, w + 7, 6], fill=(60, 50, 40, 255), outline=outline)
    # emblem: stylised flame / wyrm head
    cx, cy = (x0 + x1) // 2, 6 + (h - tail) // 2
    s = w // 4
    d.polygon([(cx, cy - s - 4), (cx + s, cy + s // 2), (cx, cy + s), (cx - s, cy + s // 2)], fill=emblem, outline=outline)
    d.polygon([(cx, cy - s // 2), (cx + s // 2, cy + s // 2), (cx - s // 2, cy + s // 2)], fill=cloth)
    return im


def P(**kw):
    """Particle/layer spec: keys become Symbols; string values starting with ':' become Symbols."""
    def conv(v):
        if isinstance(v, str) and v.startswith(":"):
            return S(v[1:])
        if isinstance(v, (list, tuple)):
            return [conv(x) for x in v]
        return v
    return {S(k): conv(v) for k, v in kw.items()}


EMBER = [[255, 150, 50], [255, 100, 30], [255, 210, 90]]
ASH = [[110, 110, 110], [150, 140, 130], [80, 80, 85]]
SNOW = [[255, 255, 255], [225, 240, 255]]
STEAM = [[235, 235, 238], [205, 210, 215]]
SMOKE = [[90, 86, 84], [70, 68, 70], [110, 104, 98]]
DUST = [[230, 220, 190], [255, 245, 220]]
GOLD = [[255, 230, 120], [255, 250, 200]]
PRISM = [[255, 90, 90], [255, 200, 80], [120, 255, 120], [90, 200, 255], [190, 120, 255]]


def hd2room(x, y):
    return round(x / 2.25, 1), round(y / 2.25, 1)


def vent(x_hd, y_hd, count=5, colors=None, rise=90, size=18, grow=1.6, opacity=(50, 95), speed=(0.25, 0.5),
         layers=(":back",), sway=6, blend=0):
    """Rising puffs (steam/smoke) from a point on the HD canvas."""
    x, y = hd2room(x_hd, y_hd)
    return P(type=":rise", count=count, shape=":puff", size=size, colors=colors or STEAM,
             area=[x - 5, y - rise, x + 5, y], speed=list(speed), sway=sway, zoom=[0.5, 0.8], grow=grow,
             opacity=list(opacity), layers=list(layers), blend=blend)


def v2h(vx, vy):
    """Default-view screen coords -> HD canvas coords."""
    return vx + 158.5, vy + 149.5


def paste(canvas, im, x, y, anchor="topleft"):
    if anchor == "bottom":
        x, y = x - im.width / 2, y - im.height
    elif anchor == "center":
        x, y = x - im.width / 2, y - im.height / 2
    canvas.alpha_composite(im, (int(round(x)), int(round(y))))


def onto(im, x, y, anchor="topleft", size=HD):
    c = blank(size)
    paste(c, im, x, y, anchor)
    return c


def silhouette_noise(size, top_fn, color, seed=0):
    """Fill below a profile y = top_fn(x) (list/array)."""
    w, h = size
    a = np.zeros((h, w, 4), np.float32)
    tops = np.asarray(top_fn, np.float32)
    ys = np.arange(h)[:, None]
    m = ys >= tops[None, :]
    a[m] = C4(color)
    return img(a)


def C4(c, a=255):
    return [c[0], c[1], c[2], a if len(c) < 4 else c[3]]
