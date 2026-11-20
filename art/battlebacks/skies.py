"""Sky layering for outdoor field rooms: drifting cumulus BEHIND the scenery.

EBDX draws a room as flat layers stacked by z. A cloud strip laid over the room bitmap (the old way) sits in front
of every tree, mast and mesa painted into that bitmap. Here a room with sky is split into
  room (z 0)          the full painting, sky included (EBDX also samples it for void colours)
  clouds (z 0)        a wide, tileable, slowly scrolling cumulus strip, drawn after the room
  front cut-out (z 1) the same painting with every sky pixel made transparent
so the clouds only ever show through the sky gaps. The strip carries :parallax, which the Bridge
(003_Bridge_EBDX.rb) uses to let it follow the camera by a fraction: under EBDX's intro sweep and idle camera
moves the sky slides less than the ground.

Clouds are painted at the source art's pixel size (2 HD px per art pixel) with a small banded palette: soft
cumulus with lit domes, a shaded, lumpy underside, separated puffs, translucent rims, smaller and fainter
toward the horizon.
"""
import math, random
import numpy as np
from PIL import Image, ImageFilter
from bblib import *
from paint import INV, PREVIEW, save_element
from rubygen import S

# Day cumulus over a pale-blue pixel-art sky: highlight .. underside
DAY_CLOUD = [(255, 255, 255), (243, 250, 252), (225, 241, 248), (204, 229, 242), (184, 219, 238)]


def _puffs(rng, w, h):
    """Circles (cx, cy, r, layer) for one cumulus of about w x h art pixels, back to front.
    A domed top of a few unequal puffs (tallest off-centre), then a lumpy underside of small ones."""
    out = []
    base = h * 0.80                      # mean underside line
    n_top = 3 if w < 34 else rng.randint(4, 5)
    peak = rng.uniform(0.38, 0.62)       # where the cloud towers highest
    ts = sorted([(k + rng.uniform(0.25, 0.75)) / n_top for k in range(n_top)])
    for t in ts:
        dome = max(0.0, 1 - abs(t - peak) / 0.62) ** 1.2
        r = h * (0.24 + 0.30 * dome) * rng.uniform(0.85, 1.12)
        cx = w * (0.06 + 0.88 * t)
        cy = base - h * (0.12 + 0.42 * dome) - r * 0.25
        out.append((cx, cy, r, 0))
    out.sort(key=lambda c: c[2])         # small shoulders behind, big towers in front
    # underside: small puffs at jittered heights -> irregular, lumpy bottom edge
    n_bot = max(2, int(w / 7))
    for i in range(n_bot):
        t = (i + rng.uniform(0.25, 0.75)) / n_bot
        edge = math.sin(math.pi * t)
        r = h * rng.uniform(0.20, 0.30) * (0.7 + 0.4 * edge)
        cx = w * (0.06 + 0.88 * t)
        cy = base - r * 0.62 + rng.uniform(-0.8, 1.4) * (0.4 + edge)
        out.append((cx, cy, r, 1))
    # normalise so nothing is clipped: top of the highest puff at y = 0
    top = min(cy - r for _, cy, r, _ in out)
    left = min(cx - r for cx, _, r, _ in out)
    return [(cx - left, cy - top, r, l) for cx, cy, r, l in out]


def cumulus(rng, w, h, palette=DAY_CLOUD, rim_alpha=150, under_alpha=215):
    """One cloud (RGBA, art pixels). Banded shading: per-puff light from the upper left, darkening toward the base."""
    pad = 2
    puffs = _puffs(rng, w, h)
    W = int(math.ceil(max(cx + r for cx, _, r, _ in puffs))) + 2 * pad
    H = int(math.ceil(max(cy + r for _, cy, r, _ in puffs))) + 2 * pad
    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    val = np.full((H, W), -1.0, np.float32)
    for cx, cy, r, layer in puffs:
        cx += pad; cy += pad
        dx = (xs + 0.5 - cx) / r
        dy = (ys + 0.5 - cy) / r
        d2 = dx * dx + dy * dy
        m = d2 < 1.0
        nz = np.sqrt(np.clip(1 - d2, 0, 1))
        lit = 0.45 * nz - 0.62 * dy - 0.30 * dx            # light from above, a little from the left
        v = 0.5 + 0.5 * lit
        v -= 0.10 * layer                                   # underside puffs sit in shadow
        val = np.where(m, v, val)
    inside = val > -0.5
    top = float(pad)
    span = max(1.0, H - 2 * pad - top * 0)
    g = np.clip((ys - top) / span, 0, 1)
    val = val - 0.42 * g ** 1.6                             # base of the cloud is in its own shade
    # bands: 0 highlight .. 4 underside
    edges = [0.80, 0.62, 0.44, 0.24]
    band = np.full((H, W), 4, np.int32)
    for i, e in reversed(list(enumerate(edges))):
        band = np.where(val >= e, i, band)
    out = np.zeros((H, W, 4), np.float32)
    pal = np.array(palette, np.float32)
    out[..., :3] = pal[band]
    alpha = np.where(inside, 255.0, 0.0)
    alpha = np.where(inside & (band == 4), under_alpha, alpha)
    # translucent rim: inside pixels touching the outside
    o = ~inside
    nb = np.zeros_like(inside)
    nb[1:, :] |= o[:-1, :]; nb[:-1, :] |= o[1:, :]; nb[:, 1:] |= o[:, :-1]; nb[:, :-1] |= o[:, 1:]
    alpha = np.where(inside & nb, np.minimum(alpha, rim_alpha), alpha)
    out[..., 3] = alpha
    return img(out)


def cloud_strip(width, height, rows, seed=0, palette=DAY_CLOUD, fade=None, wrap=True, flat=None, jitter=2):
    """Tileable strip of separated cumulus (art pixels). `rows`: list of (y_base, count, (wmin, wmax), opacity)
    - each row's clouds have their underside near y_base (art px); farther rows are smaller and fainter.
    `fade`: (y0, y1) art rows over which everything fades out toward the horizon."""
    rng = random.Random(seed)
    acc = np.zeros((height, width, 4), np.float32)
    for y_base, count, (wmin, wmax), opacity in rows:
        slots = [(k + rng.uniform(0.15, 0.85)) * width / count for k in range(count)]
        for x0 in slots:
            w = rng.uniform(wmin, wmax)
            h = w * (rng.uniform(0.34, 0.46) if flat is None else rng.uniform(flat * 0.8, flat * 1.15))
            c = cumulus(rng, w, h, palette)
            ca = arr(c)
            ca[..., 3] *= opacity
            cy = int(round(y_base - c.height + 3 + rng.uniform(-jitter, jitter)))
            cx = int(round(x0 - c.width / 2))
            for dx in ((-width, 0, width) if wrap else (0,)):
                _over(acc, ca, cx + dx, cy)
    if fade:
        y0, y1 = fade
        t = np.clip((np.arange(height, dtype=np.float32) - y0) / max(1, y1 - y0), 0, 1)
        acc[..., 3] *= (1 - t)[:, None]
    # keep the pixel-art look: a few alpha steps only
    acc[..., 3] = np.round(acc[..., 3] / 255 * 8) / 8 * 255
    return img(acc)


def _over(acc, src, x, y):
    """Alpha-composite float RGBA `src` onto float RGBA `acc` at (x, y), clipped."""
    H, W = acc.shape[:2]
    h, w = src.shape[:2]
    x0, y0 = max(x, 0), max(y, 0)
    x1, y1 = min(x + w, W), min(y + h, H)
    if x0 >= x1 or y0 >= y1:
        return
    s = src[y0 - y:y1 - y, x0 - x:x1 - x]
    d = acc[y0:y1, x0:x1]
    sa = s[..., 3:4] / 255.0
    da = d[..., 3:4] / 255.0
    oa = sa + da * (1 - sa)
    rgb = (s[..., :3] * sa + d[..., :3] * da * (1 - sa)) / np.maximum(oa, 1e-6)
    d[..., :3] = rgb
    d[..., 3:4] = oa * 255


def soften_top(im_hd, y_room0, top_view=VIEW[1], darken=0.22, radius=2.2, margin=8, feather=140):
    """Match bblib.depth_soften along y for a horizontally scrolling layer whose row 0 sits at HD y `y_room0`:
    rows above the default view get the same blur and dimming as the room behind them."""
    a = arr(im_hd)
    b = arr(im_hd.filter(ImageFilter.GaussianBlur(radius)))
    ys = np.arange(a.shape[0], dtype=np.float32) + y_room0
    m = np.clip(((top_view - margin) - ys) / feather, 0, 1)[:, None, None]
    out = a * (1 - m) + b * m
    out[..., :3] *= (1 - darken * m)
    return img(out)


def sky_strip_spec(name, im_hd, x_hd, y_hd, speed, direction=1, z=0, parallax=(0.35, 0.18), opacity=255):
    """Save a scrolling sky strip and return its EBDX img entry (with the Bridge's :parallax)."""
    save_element(name, im_hd)
    PREVIEW.append((im_hd, (x_hd, y_hd), 0, opacity, 1))
    d = {S("bitmap"): name, S("scrolling"): True, S("speed"): speed, S("direction"): direction,
         S("flat"): True, S("ox"): 0, S("oy"): 0, S("x"): round(x_hd / 2.25, 2), S("y"): round(y_hd / 2.25, 2),
         S("zoom_x"): INV, S("zoom_y"): INV, S("z"): z, S("parallax"): list(parallax)}
    if opacity != 255:
        d[S("opacity")] = opacity
    return d


def front_spec(name, im_hd, z=1):
    """The room's sky-less cut-out, drawn exactly over the room (flat, 1:1 at the default camera)."""
    save_element(name, im_hd)
    PREVIEW.append((im_hd, (0, 0), 0, 255, 1))
    return {S("bitmap"): name, S("flat"): True, S("x"): 0, S("y"): 0, S("ox"): 0, S("oy"): 0,
            S("zoom_x"): INV, S("zoom_y"): INV, S("z"): z}


def cutout(room_hd, sky_mask_hd, soft=True):
    """Room RGBA with sky pixels transparent. `sky_mask_hd`: float array 0..1 (1 = sky), HD size.
    Outside the default view the mask edge is softened exactly like the room (depth_soften)."""
    m = np.clip(np.asarray(sky_mask_hd, np.float32), 0, 1)
    if soft:
        mi = Image.fromarray((m * 255).astype(np.uint8))
        mb = np.asarray(mi.filter(ImageFilter.GaussianBlur(2.2)), np.float32) / 255.0
        vm = view_mask(8, 140)
        m = m * (1 - vm) + mb * vm
    a = arr(room_hd)
    a[..., 3] = np.round((1 - m) * 255)
    return img(a)


def extend_with_sky(bg, origin=VANILLA_ORIGIN, keep=2, glow=18, zenith_mul=(0.86, 0.9, 0.97), darken=0.22, **kw):
    """bblib.extend_vanilla for a source whose top rows are open sky, without its mirrored top margin (which hangs
    the source's scenery upside down above the horizon whenever EBDX's camera pulls back). Above the source the
    sky is the source's plain sky colour (its commonest top-row colour) deepening toward the zenith; whatever is
    brighter than that along the top edge (a sun glare) carries on as a soft glow that fades out within `glow` rows."""
    hd = extend_vanilla(bg, origin=origin, blur_out=False, **kw)
    a = arr(hd)
    oy = int(origin[1])
    top = oy - keep
    if top <= 0:
        return depth_soften(img(a), darken=darken)
    row0 = np.asarray(bg.convert("RGB"))[0].reshape(-1, 3)
    vals, counts = np.unique(row0, axis=0, return_counts=True)
    plain = np.array(list(vals[counts.argmax()]) + [255], np.float32)
    zen = plain.copy()
    zen[:3] *= np.array(zenith_mul, np.float32)
    excess = np.clip(a[top] - plain[None, :], 0, None)
    excess[:, 3] = 0
    k = 41
    pad = np.concatenate([np.repeat(excess[:1], k, 0), excess, np.repeat(excess[-1:], k, 0)], 0)
    ker = np.ones(k, np.float32) / k
    excess = np.stack([np.convolve(pad[:, c], ker, mode="same") for c in range(4)], -1)[k:-k]
    for y in range(top):
        d = top - y
        t = d / float(top)
        sky = plain * (1 - t) + zen * t
        a[y] = sky[None, :] + excess * math.exp(-d / float(glow))
    a[:top, :, 3] = 255
    a[:top, :, :3] = np.round(np.clip(a[:top, :, :3], 0, 255) / 4) * 4   # pixel-art steps, not a perfect ramp
    return depth_soften(img(a), darken=darken)
