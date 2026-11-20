"""Round 5: no mirrored scenery above the rooms.

The margins bblib.extend_vanilla adds around a vanilla panel are mirror images of it. Above the panel (and beside
its upper half) they come into view whenever EBDX's camera leaves the default framing: upside-down crags, trees and
flowers when the send-out camera pulls back, "butterfly" rocks and crystals at the panel's sides in the opening
close-up on the foe. Here those regions are painted instead (margins.py: patch synthesis from the panel's own pixels
at its own art-pixel size, steered by a material layout that continues the panel's shapes), per panel:

  PLANS[<md5 of the panel>] = Plan(...)

so every room built on that panel (stage variants, the other field sharing a caldera...) gets the same painted
margins. Only the top margin and the side margins' upper rows are repainted; the floor below the panel and
everything a builder draws afterwards (platforms, props, layers) are unchanged.
"""
import math, random
import numpy as np
from PIL import Image
import margins as M
import bblib
from bblib import HD, depth_soften

PLANS = {}
BUILDERS = {}


class Plan:
    """labels(panel) -> material labels (art px; -1 = never sample); layout(x, y, lab) -> wanted labels in the
    margins (panel art coords); sides = (left rows, right rows) repainted below the panel's top edge."""

    def __init__(self, labels, layout, nlab, sides=(0, 0), block=16, seed=1, top=True, feather=6, post=None,
                 relight=0):
        self.labels, self.layout, self.nlab = labels, layout, nlab
        self.sides, self.block, self.seed, self.top, self.feather = sides, block, seed, top, feather
        self.post, self.relight = post, relight

    def room(self, bg, origin):
        """The filled art-pixel room (margins painted where the plan says, the old extension elsewhere)."""
        old = M._orig_extend(bg, origin=origin, blur_out=False)
        R = M.Room(bg, origin)
        lab = self.labels(R.panel)
        R.set_labels_panel(np.where(lab < 0, -1, lab))
        R.paint(lambda x, y: self.layout(x, y, lab))
        rl, rr = (min(r, R.bh) for r in self.sides)
        a = M.hd_to_art(R, old)
        keep = np.ones((R.H, R.W), bool)
        if self.top:
            keep[:R.T, :] = False
        keep[R.T:R.T + rl, :R.L] = False
        keep[R.T:R.T + rr, R.L + R.bw:] = False
        keep &= ~R.P
        R.A[keep] = a[keep]; R.K |= keep; R.P |= keep
        ex = M.Exemplar(R.panel, lab, self.nlab, self.block)
        order = []
        if rl:
            order.append(("left", (R.T, R.T + rl, 0, R.L)))
        if rr:
            order.append(("right", (R.T, R.T + rr, R.L + R.bw, R.W)))
        if self.top:
            order.append("top")
        R.fill(ex, order=order, seed=self.seed)
        if self.relight:
            # smooth (non pixel-art) panels: keep the patches' detail but take the large-scale shading from the old
            # extension (blurred far past any recognisable shape), so patch seams don't show as light/dark blocks
            from scipy.ndimage import gaussian_filter
            fixed = ~R.P
            lo = lambda A: np.stack([gaussian_filter(A[..., c], self.relight) for c in range(3)], -1)
            R.A[fixed] = np.clip(R.A + lo(a) - lo(R.A), 0, 255)[fixed]
        if self.post:
            self.post(R, lab)
        return R, old

    def region(self, R):
        """HD mask (float 0..1) of what this plan repaints, feathered where it meets the kept side margins."""
        s = R.s
        m = np.zeros((HD[1], HD[0]), np.float32)
        ox, oy, bw = R.ox, R.oy, R.bg.width
        if self.top:
            m[:oy, :] = 1
        rl, rr = (min(r, R.bh) * s for r in self.sides)
        f = self.feather
        for (x0, x1, rows) in ((0, ox, rl), (ox + bw, HD[0], rr)):
            if rows <= 0:
                continue
            y1 = oy + rows
            m[oy:y1, x0:x1] = 1
            for i in range(f):                                    # fade into the kept margin below
                if y1 - f + i < HD[1]:
                    m[y1 - f + i, x0:x1] = min(m[y1 - f + i, x0], 1 - (i + 1) / (f + 1))
        return m

    def __call__(self, bg, origin, blur_out=True, darken=0.22, old=None):
        R, old_raw = self.room(bg, origin)
        new = R.hd()
        m = self.region(R)[..., None]
        out = bblib.arr(old_raw) * (1 - m) + bblib.arr(new) * m
        out = bblib.img(out)
        return depth_soften(out, darken=darken) if blur_out else out


#---------------------------------------------------------------------------------------------
# helpers for label rules (panel art pixels, float rgb 0..255)
#---------------------------------------------------------------------------------------------
def hsv(p):
    a = np.asarray(p, np.float32) / 255.0
    mx, mn = a.max(-1), a.min(-1)
    s = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    return a[..., 0], a[..., 1], a[..., 2], s, mx


def rows(lab):
    return np.arange(lab.shape[0])[:, None] + np.zeros(lab.shape, int)


def cols(lab):
    return np.arange(lab.shape[1])[None, :] + np.zeros(lab.shape, int)


wob = M.wobble


#---------------------------------------------------------------------------------------------
# MOUNTAIN: aveontrainer's highland tarn. Above the panel the falls keep falling and the two crags rise into a
# gorge (the crags' water-side edges lean outward a little); beside the panel the crags, the tarn and its grassy
# shore continue. 0 rock, 1 grass, 2 bank, 3 falling water, 4 tarn, 5 foam line (never above the panel)
#---------------------------------------------------------------------------------------------
def mountain_labels(p):
    r, g, b, s, v = hsv(p)
    lab = np.full(p.shape[:2], -1, np.int16)
    rock = (s < 0.31) & (v < 0.6) & (r >= b)
    bank = (r > g) & (s >= 0.31)
    grass = (g > r) & (g > b) & ~rock
    water = (b >= r) & ~grass
    y = rows(lab)
    lab[rock] = 0; lab[grass] = 1; lab[bank] = 2
    lab[water & (y < 42)] = 3; lab[water & (y >= 42)] = 4
    from scipy.ndimage import binary_dilation
    foam = water & (y < 50) & (s < 0.2) & (v > 0.9)
    lab[binary_dilation(foam, iterations=2) & water & (y >= 16) & (y < 50)] = 5
    lab[(lab == 0) & (y > 100)] = -1                      # the boulder on the shore: never copied
    return lab


def mountain_layout(x, y, lab):
    L = np.full(x.shape, 1, np.int16)
    top = y < 0
    le = 28 + 0.35 * y + wob(y, 3.0, 11)
    re = 197 - 0.3 * y + wob(y, 3.5, 12)
    L[top] = 3
    L[top & ((x < le) | (x > re))] = 0
    lm = (x < 0) & (y >= 0)
    L[lm & (y < 81 + 0.1 * (-x) + wob(x, 2, 13))] = 0
    L[lm & (y >= 81 + 0.1 * (-x) + wob(x, 2, 13))] = 4
    rm = (x > 255) & (y >= 0)
    L[rm & (y < 48 + 0.1 * (x - 255) + wob(x, 2, 15))] = 0
    L[rm & (y >= 48 + 0.1 * (x - 255) + wob(x, 2, 15))] = 4
    return L


PLANS["bd24b7ac4c"] = Plan(mountain_labels, mountain_layout, 6, sides=(100, 62), block=16, seed=3)


def mountain():
    """fields_f.mountain on the painted room, plus a cut-out of the crags over the foam strip: its streaks used to
    run across both crags (it spans the whole width); now they only show on the water."""
    import fields_a, fields_f
    from fields_d import capture
    from skies import front_spec
    from rubygen import S
    hd, res = capture(fields_f.mountain, fields_a)
    bblib.save_room("field_mountain", hd)
    r, g, b, s, v = hsv(np.asarray(hd.convert("RGB")))
    rock = (s < 0.36) & (v < 0.66) & (r >= b - 0.01) & ~((g > r) & (g > b))
    band = np.zeros(rock.shape, bool)
    band[176:280] = True                                  # the foam strip (y 196..256) with room to spare
    a = bblib.arr(hd)
    a[..., 3] = np.where(rock & band, 255, 0)
    extras = res["profile"][S("art_extras")]
    extras["img002"][S("z")] = 3                          # mist stays in front of the crags
    extras["img003"] = front_spec("pf_mountain_crags", bblib.img(a), z=2)
    for l in res["profile"][S("layers")]:
        if l[S("bitmap")] == "pf_mountain_hawk":
            l[S("z")] = 3
    res["origins"] = [o if o[0] != fields_a.OWN else [o[0], o[1] + ", gorge above the falls, crag cut-out over the foam"]
                      for o in res["origins"]]
    return res


BUILDERS["MOUNTAIN"] = mountain


#---------------------------------------------------------------------------------------------
# Rock-walled rooms: above the panel the wall (ceiling) simply goes on, quilted from a band of clean wall near the
# panel's top (no cave mouths, crystals or outlines copied); the same wall continues beside the panel's upper rows.
#---------------------------------------------------------------------------------------------
def wall_labels(r0, r1, vmin=0.0, vmax=1.0, x0=0, x1=None, extra=None):
    def fn(p):
        r, g, b, s, v = hsv(p)
        lab = np.full(p.shape[:2], -1, np.int16)
        y, x = rows(lab), cols(lab)
        ok = (y >= r0) & (y < r1) & (v >= vmin) & (v <= vmax) & (x >= x0) & (x < (x1 or p.shape[1]))
        if extra is not None:
            ok &= extra(p)
        lab[ok] = 0
        return lab
    return fn


def all_wall(x, y, lab):
    return np.zeros(x.shape, np.int16)


# CAVE and its cracked stage: carchagui's cave panel (2x). The very top rows are a darker ceiling band; the wall
# exemplar is the band of plain wall between it and the two cave mouths.
PLANS["5a681c5c1e"] = Plan(wall_labels(4, 24, vmin=0.36), all_wall, 1, sides=(100, 100), block=14, seed=5)
# SNOWY_MOUNTAIN: the same panel in its snow-cave colours
PLANS["a0dc52e2d4"] = Plan(wall_labels(4, 24, vmin=0.36), all_wall, 1, sides=(100, 100), block=14, seed=6)


def gem_tips(is_gem, max_h=6):
    """Post step: crystals cut by the panel's top edge get their tips drawn above it (the panel's own crystal colours,
    tapering one art pixel per side per row, darkest colour on the edges) instead of a flat cut."""
    def post(R, lab):
        top = R.panel[0]
        g = is_gem(R.panel[:3])
        runs, x = [], 0
        while x < R.bw:
            if g[0, x]:
                a = x
                while x < R.bw and g[0, x]:
                    x += 1
                runs.append((a, x - 1))
            x += 1
        for a, b in runs:
            seg = R.panel[0:3, a:b + 1][g[0:3, a:b + 1]]
            if not len(seg):
                continue
            lum = seg.sum(-1)
            dark, light = seg[lum.argmin()], seg[lum.argmax()]
            h = min(max_h, (b - a) // 2 + 1)
            for i in range(1, h + 1):
                l, r = a + i // 2 + (i > 1), b - i // 2 - (i > 1)
                if l > r:
                    break
                y = R.T - i
                for xx in range(l, r + 1):
                    c = top[xx]
                    if xx in (l, r):
                        c = dark
                    elif xx == l + 1 and i < h:
                        c = light
                    R.A[y, R.L + xx] = c
    return post


def gem_mask(p):
    r, g, b, s, v = hsv(p)
    return (s > 0.45) & (v > 0.45)


def cave_labels(r1, vmin, smax=0.45, extra_bad=None):
    def fn(p):
        r, g, b, s, v = hsv(p)
        lab = np.full(p.shape[:2], -1, np.int16)
        y = rows(lab)
        ok = (y < r1) & (v >= vmin) & (s <= smax)
        if extra_bad is not None:
            ok &= ~extra_bad(p)
        # keep a margin around excluded things so no patch carries half a crystal
        from scipy.ndimage import binary_dilation
        ok &= ~binary_dilation(~ok & (y < r1), iterations=2)
        lab[ok] = 0
        return lab
    return fn


# CRYSTAL_CAVERN / DARK_CRYSTAL: Rejuvenation's crystal tunnel. Above it the streaked wall goes on (crystals and the
# tunnel's dark mouth are never copied); crystals cut by the top edge get their tips.
def tunnel_labels(vwall, vdark, bad=None):
    """0 wall, 1 the tunnel's dark mouth (upper left), -1 crystals / floor."""
    base = cave_labels(70, vwall, extra_bad=bad)

    def fn(p):
        lab = base(p)
        r, g, b, s, v = hsv(p)
        y, x = rows(lab), cols(lab)
        lab[(v < vdark) & (y < 90) & (x < 130)] = 1
        return lab
    return fn


def tunnel_layout(x, y, lab):
    """Wall everywhere, except that the tunnel mouth cut by the panel's left edge closes in a rounded end 9 art px
    into the margin."""
    L = np.zeros(x.shape, np.int16)
    run = np.where(lab[:, 0] == 1)[0]
    if len(run):
        a, b = run.min(), run.max()
        yc, ry = (a + b) / 2.0, (b - a) / 2.0 + 1
        inside = (x < 0) & (((x - 0) / 9.0) ** 2 + ((y - yc) / ry) ** 2 < 1)
        L[inside] = 1
    # the dark arch cut by the panel's top edge closes in a low curve just above it
    cs = np.where(lab[0] == 1)[0]
    if len(cs):
        a, b = cs.min() - 6, cs.max()
        xc, hw = (a + b) / 2.0, (b - a) / 2.0 + 1
        h = 7 * np.sqrt(np.clip(1 - ((x - xc) / hw) ** 2, 0, 1))
        L[(y < 0) & (-y < h)] = 1
    return L


PLANS["a84f34677a"] = Plan(tunnel_labels(0.25, 0.25), tunnel_layout, 2, sides=(110, 110), block=12, seed=7,
                           post=gem_tips(gem_mask))
PLANS["4bb0600cef"] = Plan(tunnel_labels(0.12, 0.12, bad=lambda p: hsv(p)[4] > 0.62), tunnel_layout, 2,
                           sides=(110, 110), block=12, seed=8, post=gem_tips(lambda p: hsv(p)[4] > 0.62))
# DRAGONS_DEN (both stages): the smoothed den wall (1:1 pixels); its lava vein is never copied
PLANS["ea51db409b"] = Plan(cave_labels(200, 0.0, smax=0.75), all_wall, 1, sides=(250, 250), block=40, seed=9,
                           relight=14)
# VOLCANIC / ASHEN_WASTE: the caldera tunnel; lava is never copied, so the stream down the panel's right edge gets a
# rock bank instead of a mirrored twin
PLANS["f6bc3067b7"] = Plan(cave_labels(70, 0.0, smax=0.78), all_wall, 1, sides=(110, 110), block=16, seed=10)


#---------------------------------------------------------------------------------------------
# Forest rooms whose canopy runs along the panel's whole top edge: above it the canopy simply goes on (quilted from
# the canopy band), beside it the canopy band continues; trunks below keep their (upright) side extension.
#---------------------------------------------------------------------------------------------
def band_labels(r0, r1, bad=None):
    def fn(p):
        lab = np.full(p.shape[:2], -1, np.int16)
        y = rows(lab)
        ok = (y >= r0) & (y < r1)
        if bad is not None:
            ok &= ~bad(p)
        lab[ok] = 0
        return lab
    return fn


PLANS["ea05019cda"] = Plan(band_labels(0, 22), all_wall, 1, sides=(30, 30), block=16, seed=11)   # FAIRY_TALE
PLANS["cad33552c5"] = Plan(band_labels(0, 20), all_wall, 1, sides=(26, 26), block=16, seed=12)   # SILKWOOD
PLANS["c9861069ac"] = Plan(band_labels(0, 24), all_wall, 1, sides=(34, 34), block=16, seed=13)   # WILDFIRE (+embers)
PLANS["725fac2b17"] = Plan(band_labels(0, 22), all_wall, 1, sides=(30, 30), block=16, seed=14)   # WASTELAND


#---------------------------------------------------------------------------------------------
# Open skies: above the horizon the sky (and its clouds) goes on, quilted from the panel's upper sky only
#---------------------------------------------------------------------------------------------
def beach_bad(p):
    r, g, b, s, v = hsv(p)
    x = cols(p[..., 0])
    return (x > 170) & (x < 330)                         # the sun and its rays: never copied


PLANS["453a1ba8d8"] = Plan(band_labels(0, 36, bad=beach_bad), all_wall, 1, sides=(36, 36), block=14, seed=15)  # BEACH
PLANS["e94eae6c5d"] = Plan(band_labels(0, 60), all_wall, 1, sides=(0, 0), block=20, seed=16)        # STORMFRONT


class GradPlan(Plan):
    """Smooth (gradient) skies and water: above the panel its top row simply deepens toward the zenith
    (skies.extend_with_sky), with no bubbles, clouds or horizon copied."""

    def __init__(self, zenith_mul=(0.86, 0.9, 0.97), glow=18):
        Plan.__init__(self, None, None, 1)
        self.zenith_mul, self.glow = zenith_mul, glow

    def __call__(self, bg, origin, blur_out=True, darken=0.22, old=None):
        old_raw = M._orig_extend(bg, origin=origin, blur_out=False)
        a = bblib.arr(old_raw)
        top = int(origin[1]) - 2
        src = bblib.arr(_sky_top(bg, origin, self.zenith_mul, self.glow))
        a[:top] = src[:top]
        out = bblib.img(a)
        return depth_soften(out, darken=darken) if blur_out else out

    def region(self, R):
        m = np.zeros((HD[1], HD[0]), np.float32)
        m[:R.oy - 2, :] = 1
        return m


def _sky_top(bg, origin, zenith_mul, glow):
    """skies.extend_with_sky without its final softening (same maths)."""
    import math as _m
    hd = M._orig_extend(bg, origin=origin, blur_out=False)
    a = bblib.arr(hd)
    oy = int(origin[1]); top = oy - 2
    row0 = np.asarray(bg.convert("RGB"))[0].reshape(-1, 3)
    vals, counts = np.unique(row0, axis=0, return_counts=True)
    plain = np.array(list(vals[counts.argmax()]) + [255], np.float32)
    zen = plain.copy(); zen[:3] *= np.array(zenith_mul, np.float32)
    excess = np.clip(a[top] - plain[None, :], 0, None); excess[:, 3] = 0
    k = 41
    pad = np.concatenate([np.repeat(excess[:1], k, 0), excess, np.repeat(excess[-1:], k, 0)], 0)
    ker = np.ones(k, np.float32) / k
    excess = np.stack([np.convolve(pad[:, c], ker, mode="same") for c in range(4)], -1)[k:-k]
    for y in range(top):
        d = top - y; t = d / float(top)
        a[y] = (plain * (1 - t) + zen * t)[None, :] + excess * _m.exp(-d / float(glow))
    a[:top, :, 3] = 255
    a[:top, :, :3] = np.round(np.clip(a[:top, :, :3], 0, 255) / 4) * 4
    return bblib.img(a)


PLANS["9cf6fafc5a"] = GradPlan(zenith_mul=(0.8, 0.84, 0.88), glow=10)    # UNDERWATER: deeper water above
PLANS["f184641a67"] = GradPlan(zenith_mul=(0.9, 0.92, 0.96), glow=30)    # FROZEN_LAKE: overcast sky
PLANS["b673189225"] = GradPlan(zenith_mul=(0.82, 0.88, 0.96), glow=24)   # WATER_SURFACE


#---------------------------------------------------------------------------------------------
def install():
    import sys
    M.PLANS.update(PLANS)
    mods = [m for m in list(sys.modules.values())
            if getattr(m, "__file__", None) and m.__file__.startswith(bblib.__file__.rsplit("/", 1)[0])]
    M.install_everywhere(mods)

