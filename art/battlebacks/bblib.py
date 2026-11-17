"""Prismfall battle backdrop compositor (EBDX rooms).

Geometry (measured in the real engine, see README.md):
  EBDX room bitmap 384x308 is drawn at ROOM_SCALE 2.25.  At the default camera the screen
  (512x384) shows room x 70.44..298, y 66.44..237.  We author every backdrop as an HD canvas
  of 864x693 (= room * 2.25) which the Bridge draws as a flat EBDX layer at zoom 1/2.25, so at
  the default camera the art is shown exactly 1:1 (crisp pixel art, like the source games).
  The 384x308 room image is the HD canvas downscaled (used for EBDX's void colours, tree tinting
  and as a fallback).
"""
import os, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageEnhance

S = 2.25
ROOM = (384, 308)
HD = (864, 693)
VIEW = (158.5, 149.5)            # HD coords of the screen's top-left at the default camera
VIEW_W, VIEW_H = 512, 384
FOE = (526.5, 342.0)             # HD ground point of the foe (room 234,152)
PLAYER = (261.0, 567.0)          # HD ground point of the player (room 116,252)
FOE_D = [(576.0, 369.0), (445.5, 342.0)]     # doubles (room 256,164 / 198,152)
PLAYER_D = [(207.0, 540.0), (432.0, 589.5)]  # doubles (room 92,240 / 192,262)
# Vanilla Essentials/Reborn/Rejuvenation layout (512x384 screen): foe base centre (384,176).
# Placing a vanilla bg at this HD origin puts its foe point exactly on the EBDX foe point.
VANILLA_ORIGIN = (142, 166)

GAMES = "/home/claude/ref/games"
EBDX_REF = "/home/claude/ref/ebdx_renovation/Graphics/EBDX/Battlebacks"


def game_img(game, name):
    p = os.path.join(GAMES, game, "Graphics", "Battlebacks", name + ("" if name.endswith(".png") else ".png"))
    return Image.open(p).convert("RGBA")


def has_game_img(game, name):
    return os.path.exists(os.path.join(GAMES, game, "Graphics", "Battlebacks", name + ".png"))


def ebdx_img(sub, name):
    return Image.open(os.path.join(EBDX_REF, sub, name + ".png")).convert("RGBA")


def arr(im):
    return np.asarray(im.convert("RGBA")).astype(np.float32)


def img(a):
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGBA")


#---------------------------------------------------------------------------------------------
# Extending a vanilla 512x288 backdrop to the full HD canvas
#---------------------------------------------------------------------------------------------
def extend_vanilla(bg, origin=VANILLA_ORIGIN, floor_band=110, floor_scale=2, blur_out=True,
                   side_mode="reflect", top_mode="reflect", darken=0.22):
    """Return an HD canvas with `bg` pasted 1:1 at `origin` and every margin filled.
    Sides/top: mirrored continuation.  Floor: the bg's lowest `floor_band` rows, scaled up by
    `floor_scale` (nearer ground = bigger texture) and blended under the seam.  Areas outside the
    default view are progressively softened and darkened (depth of field)."""
    W, H = HD
    ox, oy = origin
    bw, bh = bg.size
    src = arr(bg)
    canvas = np.zeros((H, W, 4), np.float32)
    # 1) horizontal extension of the bg rows
    row = np.zeros((bh, W, 4), np.float32)
    for x in range(W):
        sx = x - ox
        if 0 <= sx < bw:
            row[:, x] = src[:, sx]
        else:
            if side_mode == "reflect":
                # mirror without repeating the edge column; bounce if far
                period = 2 * bw
                m = sx % period
                if m >= bw:
                    m = period - 1 - m
                row[:, x] = src[:, m]
            else:  # edge
                row[:, x] = src[:, min(max(sx, 0), bw - 1)]
    # 2) vertical: top
    for y in range(H):
        sy = y - oy
        if 0 <= sy < bh:
            canvas[y] = row[sy]
        elif sy < 0:
            if top_mode == "reflect":
                m = (-sy - 1) % (2 * bh)
                if m >= bh:
                    m = 2 * bh - 1 - m
                canvas[y] = row[m]
            else:
                canvas[y] = row[0]
    # 3) floor: scaled band below the bg
    band = row[bh - floor_band:bh]
    bimg = img(band)
    big = bimg.resize((W * floor_scale, floor_band * floor_scale), Image.NEAREST)
    cx = int(FOE[0] * floor_scale - FOE[0]) // 1  # keep the band centred on the arena axis
    cx = (W * floor_scale - W) // 2
    big = arr(big)[:, cx:cx + W]
    start = oy + bh - 18                      # overlap seam
    need = H - start
    reps = int(math.ceil(need / big.shape[0])) + 1
    stack = np.concatenate([big] * reps, axis=0)[:need]
    seam = 18
    for i in range(need):
        y = start + i
        if i < seam and y < oy + bh:
            t = i / seam
            canvas[y] = canvas[y] * (1 - t) + stack[i] * t
        else:
            canvas[y] = stack[i]
    out = img(canvas)
    if blur_out:
        out = depth_soften(out, darken=darken)
    return out


def view_mask(margin=8, feather=120):
    """0 inside the default camera view (plus margin), rising to 1 `feather` px outside it."""
    W, H = HD
    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    x0, y0 = VIEW[0] - margin, VIEW[1] - margin
    x1, y1 = VIEW[0] + VIEW_W + margin, VIEW[1] + VIEW_H + margin
    dx = np.maximum(np.maximum(x0 - xs, xs - x1), 0)
    dy = np.maximum(np.maximum(y0 - ys, ys - y1), 0)
    d = np.sqrt(dx * dx + dy * dy)
    return np.clip(d / feather, 0, 1)


def depth_soften(im, radius=2.2, darken=0.22, margin=8, feather=140):
    m = view_mask(margin, feather)[..., None]
    a = arr(im)
    b = arr(im.filter(ImageFilter.GaussianBlur(radius)))
    out = a * (1 - m) + b * m
    out[..., :3] *= (1 - darken * m)
    return img(out)


#---------------------------------------------------------------------------------------------
# Platforms
#---------------------------------------------------------------------------------------------
def ellipse_crop(base, alpha_thresh=8):
    """Crop a vanilla base image to its visible bounding box."""
    bb = base.getchannel("A").point(lambda v: 255 if v > alpha_thresh else 0).getbbox()
    return base.crop(bb) if bb else base


def place_foe_base(canvas, base, at=FOE, dy=0):
    b = ellipse_crop(base)
    x = int(round(at[0] - b.width / 2))
    y = int(round(at[1] - b.height / 2 + dy))
    canvas.alpha_composite(b, (x, y))


def place_player_base(canvas, base, at=PLAYER, dy=0):
    """Vanilla player bases are only the top of the ellipse (screen-bottom cut); mirror it into a
    full platform so zoom-outs look right."""
    b = ellipse_crop(base)
    full = Image.new("RGBA", (b.width, b.height * 2), (0, 0, 0, 0))
    full.alpha_composite(b, (0, 0))
    full.alpha_composite(b.transpose(Image.FLIP_TOP_BOTTOM), (0, b.height))
    x = int(round(at[0] - full.width / 2))
    y = int(round(at[1] - full.height / 2 + dy))
    canvas.alpha_composite(full, (x, y))


#---------------------------------------------------------------------------------------------
# Colour grading
#---------------------------------------------------------------------------------------------
def grade(im, mul=(1, 1, 1), add=(0, 0, 0), sat=1.0, contrast=1.0, gamma=1.0):
    a = arr(im)
    rgb = a[..., :3]
    if sat != 1.0:
        l = (rgb * np.array([0.299, 0.587, 0.114])).sum(-1, keepdims=True)
        rgb = l + (rgb - l) * sat
    if contrast != 1.0:
        rgb = (rgb - 128) * contrast + 128
    rgb = rgb * np.array(mul, np.float32) + np.array(add, np.float32)
    if gamma != 1.0:
        rgb = 255 * np.power(np.clip(rgb, 0, 255) / 255.0, gamma)
    a[..., :3] = rgb
    return img(a)


def hue_shift(im, deg):
    hsv = im.convert("RGB").convert("HSV")
    h, s, v = hsv.split()
    h = h.point(lambda x: (x + int(deg * 255 / 360)) % 256)
    out = Image.merge("HSV", (h, s, v)).convert("RGBA")
    out.putalpha(im.getchannel("A"))
    return out


def gradient_map(im, stops):
    """Map luminance to a colour ramp: stops = [(0.0,(r,g,b)), ..., (1.0,(r,g,b))]."""
    a = arr(im)
    l = (a[..., :3] * np.array([0.299, 0.587, 0.114])).sum(-1) / 255.0
    out = np.zeros_like(a[..., :3])
    xs = [s[0] for s in stops]
    for c in range(3):
        out[..., c] = np.interp(l, xs, [s[1][c] for s in stops])
    a[..., :3] = out
    return img(a)


def blend(base, top, mode="normal", opacity=1.0, mask=None):
    """Blend RGBA `top` over `base` (same size)."""
    A = arr(base)
    B = arr(top)
    ta = B[..., 3:4] / 255.0 * opacity
    if mask is not None:
        ta = ta * (np.asarray(mask, np.float32)[..., None] / 255.0 if not isinstance(mask, np.ndarray) else mask[..., None])
    a, b = A[..., :3] / 255.0, B[..., :3] / 255.0
    if mode == "normal":
        r = b
    elif mode == "multiply":
        r = a * b
    elif mode == "screen":
        r = 1 - (1 - a) * (1 - b)
    elif mode == "add":
        r = np.clip(a + b, 0, 1)
    elif mode == "overlay":
        r = np.where(a < 0.5, 2 * a * b, 1 - 2 * (1 - a) * (1 - b))
    elif mode == "softlight":
        r = (1 - 2 * b) * a * a + 2 * b * a
    elif mode == "color":
        # keep base luminance, take top hue/sat
        lb = (a * np.array([0.299, 0.587, 0.114])).sum(-1, keepdims=True)
        lt = (b * np.array([0.299, 0.587, 0.114])).sum(-1, keepdims=True)
        r = np.clip(b + (lb - lt), 0, 1)
    else:
        raise ValueError(mode)
    out = A.copy()
    out[..., :3] = (a * (1 - ta) + r * ta) * 255
    out[..., 3] = np.maximum(A[..., 3], B[..., 3] * ta[..., 0])
    return img(out)


def vgradient(size, stops):
    """Vertical gradient image: stops = [(t, (r,g,b,a)), ...] with t in 0..1 of height."""
    w, h = size
    t = np.linspace(0, 1, h)
    out = np.zeros((h, w, 4), np.float32)
    xs = [s[0] for s in stops]
    for c in range(4):
        col = np.interp(t, xs, [s[1][c] for s in stops])
        out[..., c] = col[:, None]
    return img(out)


def radial(size, center, radius, color, power=1.6, squash=1.0):
    """Soft radial glow (RGBA), alpha 1 at centre falling to 0 at radius."""
    w, h = size
    ys, xs = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.sqrt(((xs - center[0])) ** 2 + ((ys - center[1]) / squash) ** 2) / radius
    al = np.clip(1 - d, 0, 1) ** power
    out = np.zeros((h, w, 4), np.float32)
    out[..., 0], out[..., 1], out[..., 2] = color[0], color[1], color[2]
    out[..., 3] = al * (color[3] if len(color) > 3 else 255)
    return img(out)


def noise(size, scale=8, seed=0, octaves=3):
    """Smooth value noise 0..1 (numpy array h x w)."""
    rng = np.random.RandomState(seed)
    w, h = size
    total = np.zeros((h, w), np.float32)
    amp, norm = 1.0, 0.0
    for o in range(octaves):
        s = max(1, int(scale * (2 ** o)))
        gw, gh = w // s + 2, h // s + 2
        g = rng.rand(gh, gw).astype(np.float32)
        gi = Image.fromarray((g * 255).astype(np.uint8)).resize((gw * s, gh * s), Image.BICUBIC)
        total += np.asarray(gi, np.float32)[:h, :w] / 255.0 * amp
        norm += amp
        amp *= 0.5
    return total / norm


def posterize_alpha(im, levels=4):
    """Quantise alpha to a few steps for a pixel-art look on glows/fog."""
    a = arr(im)
    al = a[..., 3] / 255.0
    a[..., 3] = np.round(al * levels) / levels * 255
    return img(a)


def quantize_rgb(im, step=8):
    a = arr(im)
    a[..., :3] = np.round(a[..., :3] / step) * step
    return img(a)


#---------------------------------------------------------------------------------------------
# Output
#---------------------------------------------------------------------------------------------
OUT = "/home/claude/fangame/graphics/EBDX/Battlebacks"


def save_room(name, hd, out=OUT):
    """Write battlebg/<name>_hd.png (864x693) and battlebg/<name>.png (384x308)."""
    assert hd.size == HD, hd.size
    os.makedirs(os.path.join(out, "battlebg"), exist_ok=True)
    hd = hd.convert("RGBA")
    a = arr(hd)
    a[..., 3] = 255                     # rooms must be opaque (EBDX samples corner pixels)
    hd = img(a)
    hd.convert("RGB").save(os.path.join(out, "battlebg", name + "_hd.png"), optimize=True)
    lo = hd.resize(ROOM, Image.LANCZOS)
    lo.convert("RGB").save(os.path.join(out, "battlebg", name + ".png"), optimize=True)
    return hd


def save_element(name, im, out=OUT):
    os.makedirs(os.path.join(out, "elements"), exist_ok=True)
    p = os.path.join(out, "elements", name + ".png")
    im.save(p, optimize=True)
    return p


def preview(hd, path, show_view=True, pokemon=True):
    """Debug preview: the default camera crop (what the player sees), plus markers."""
    v = hd.crop((int(VIEW[0]), int(VIEW[1]), int(VIEW[0]) + VIEW_W, int(VIEW[1]) + VIEW_H))
    v.convert("RGB").save(path)
    return v


def place_player_base_scaled(canvas, foe_base, scale=2, at=PLAYER, dy=0):
    """Player platform = the foe platform drawn nearer (scaled up, nearest neighbour)."""
    b = ellipse_crop(foe_base)
    b = b.resize((b.width * scale, b.height * scale), Image.NEAREST)
    canvas.alpha_composite(b, (int(round(at[0] - b.width / 2)), int(round(at[1] - b.height / 2 + dy))))
