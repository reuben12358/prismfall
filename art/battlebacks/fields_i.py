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
from PIL import Image, ImageDraw
import margins as M
import bblib
from bblib import HD, depth_soften

PLANS = {}
BUILDERS = {}


class Plan:
    """labels(panel) -> material labels (art px; -1 = never sample); layout(x, y, lab) -> wanted labels in the
    margins (panel art coords); sides = (left rows, right rows) repainted below the panel's top edge."""

    def __init__(self, labels, layout, nlab, sides=(0, 0), block=16, seed=1, top=True, feather=6, post=None,
                 relight=0, lam=2500.0, pre=None):
        self.labels, self.layout, self.nlab = labels, layout, nlab
        self.sides, self.block, self.seed, self.top, self.feather = sides, block, seed, top, feather
        self.post, self.relight, self.lam, self.pre = post, relight, lam, pre

    def room(self, bg, origin, old=None):
        """The filled art-pixel room (margins painted where the plan says, the old extension elsewhere)."""
        old = old() if old else M._orig_extend(bg, origin=origin, blur_out=False)
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
        if self.pre:
            self.pre(R, lab)                                  # fixed structures, known + protected before quilting
        ex = M.Exemplar(R.panel, lab, self.nlab, self.block)
        order = []
        if rl:
            order.append(("left", (R.T, R.T + rl, 0, R.L)))
        if rr:
            order.append(("right", (R.T, R.T + rr, R.L + R.bw, R.W)))
        if self.top:
            order.append("top")
        R.fill(ex, order=order, seed=self.seed, lam=self.lam)
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
        R, old_raw = self.room(bg, origin, old)
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
        old_raw = old() if old else M._orig_extend(bg, origin=origin, blur_out=False)
        a = bblib.arr(old_raw)
        top = int(origin[1]) - 2
        src = bblib.arr(_sky_top(bg, origin, self.zenith_mul, self.glow, old_raw))
        a[:top] = src[:top]
        out = bblib.img(a)
        return depth_soften(out, darken=darken) if blur_out else out

    def region(self, R):
        m = np.zeros((HD[1], HD[0]), np.float32)
        m[:R.oy - 2, :] = 1
        return m


def _sky_top(bg, origin, zenith_mul, glow, hd=None):
    """skies.extend_with_sky without its final softening (same maths)."""
    import math as _m
    hd = hd if hd is not None else M._orig_extend(bg, origin=origin, blur_out=False)
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
# Built structures: above the panel the structure's own band repeats upright (a second arcade tier over the
# colosseum's, the garden's trellis wall going higher, the neon towers rising), each repeat a little darker.
#---------------------------------------------------------------------------------------------
class TilePlan(Plan):
    """Above the panel, HD row y (< origin y) takes panel row r0 + ((y - oy) mod period): the band
    [r0, r0 + period) of panel rows repeated upward, never flipped. `fade`: brightness kept per repeat."""

    def __init__(self, r0, period, fade=0.9):
        Plan.__init__(self, None, None, 1)
        self.r0, self.period, self.fade = r0, period, fade

    def __call__(self, bg, origin, blur_out=True, darken=0.22, old=None):
        old_raw = old() if old else M._orig_extend(bg, origin=origin, blur_out=False)
        a = bblib.arr(old_raw)
        oy = int(origin[1])
        P = self.period
        for y in range(oy):
            d = oy - y                                     # rows above the panel's top edge
            k = (d - 1) // P + 1                           # which repeat
            src = self.r0 + ((-d) % P)
            a[y] = a[oy + src] * np.array([self.fade ** k] * 3 + [1.0], np.float32)
        out = bblib.img(a)
        return depth_soften(out, darken=darken) if blur_out else out

    def region(self, R):
        m = np.zeros((HD[1], HD[0]), np.float32)
        m[:R.oy, :] = 1
        return m


PLANS["27a24fdcb9"] = TilePlan(0, 124, fade=0.88)       # COLOSSEUM: an upper arcade on the cornice
PLANS["f3d5a10597"] = TilePlan(8, 32, fade=0.95)        # FLOWER_GARDEN 1-3: the trellis wall goes higher
PLANS["52dcc239c2"] = TilePlan(8, 32, fade=0.95)
PLANS["9bae59a29e"] = TilePlan(8, 32, fade=0.95)
PLANS["7b90eb1361"] = TilePlan(0, 64, fade=0.96)        # FLOWER_GARDEN 4-5: the flower towers grow on
PLANS["8246117502"] = TilePlan(0, 64, fade=0.96)
PLANS["8d75491748"] = TilePlan(0, 34, fade=0.92)        # NEON_GRID (+ blackout): towers rise, no upside-down slab


#---------------------------------------------------------------------------------------------
# RAINBOW: the bow is an arc; beyond the panel every pixel takes the panel's colour at the same distance from the
# arc's centre, so the bands carry on round the arc (no chevron where the panel's edges used to mirror it).
#---------------------------------------------------------------------------------------------
class ArcPlan(Plan):
    """The bow's yellow/green and green/blue boundaries are found on every row and fitted with concentric circles;
    every margin pixel then takes the panel's (median) colour at its distance from the common centre, so the bands
    carry on round the arc instead of folding into a chevron at the panel's edges."""

    def __init__(self):
        Plan.__init__(self, None, None, 1)

    def fit(self, a):
        r, g, b = a[..., 0], a[..., 1], a[..., 2]
        yel = (r > 150) & (g > 150) & (b < 130)
        grn = (g > 150) & (r < 120) & (b < 120)
        blu = (b > 150) & (r < 80)
        pts = []
        for y in range(a.shape[0]):
            for A, B, k in ((yel, grn, 0), (grn, blu, 1)):
                xa, xb = np.nonzero(A[y])[0], np.nonzero(B[y])[0]
                if len(xa) < 6 or len(xb) < 6:
                    continue
                # the band A ends where band B starts (A lies left of B on every row of this bow)
                after = xb[xb > xa.min()]
                if not len(after):
                    continue
                x1 = after.min()
                x0 = xa[xa < x1].max() if (xa < x1).any() else None
                if x0 is not None and x1 - x0 < 24:
                    pts.append(((x0 + x1) / 2.0, y, k))
        P = np.array(pts, np.float64)
        M_ = np.zeros((len(P), 4))
        M_[:, 0] = 2 * P[:, 0]; M_[:, 1] = 2 * P[:, 1]
        M_[P[:, 2] == 0, 2] = 1; M_[P[:, 2] == 1, 3] = 1
        sol = np.linalg.lstsq(M_, (P[:, :2] ** 2).sum(1), rcond=None)[0]
        return sol[0], sol[1]

    SKY = (236, 222, 242)          # pale festival sky beyond the bow's outer (red) band
    RIM = 12                       # the panel's own baked-in light rim (left, top, right): repainted too

    def __call__(self, bg, origin, blur_out=True, darken=0.22, old=None):
        old_raw = old() if old else M._orig_extend(bg, origin=origin, blur_out=False)
        a = np.asarray(bg.convert("RGB"), np.float32)
        cx, cy = self.fit(a)
        H, W = a.shape[:2]
        I = self.RIM
        ys, xs = np.mgrid[I:H, I:W - I]
        rad = np.sqrt((xs - cx) ** 2 + (ys - cy) ** 2)
        ang = np.arctan2(ys - cy, xs - cx)
        ri = np.round(rad).astype(int)
        lo, hi = ri.min(), ri.max()
        amin = np.full(hi - lo + 1, np.inf); amax = np.full(hi - lo + 1, -np.inf)
        np.minimum.at(amin, ri.ravel() - lo, ang.ravel()); np.maximum.at(amax, ri.ravel() - lo, ang.ravel())
        out = bblib.arr(old_raw)
        ox, oy = int(origin[0]), int(origin[1])
        Y, X = np.mgrid[0:HD[1], 0:HD[0]]
        X2, Y2 = (X // 2) * 2 - ox, (Y // 2) * 2 - oy              # panel coords, the art's 2x2 pixel steps
        r = np.sqrt((X2 - cx) ** 2 + (Y2 - cy) ** 2)
        t = np.arctan2(Y2 - cy, X2 - cx)
        k = np.clip(np.round(r).astype(int), lo, hi) - lo
        # follow the pixel's own arc back to where it leaves the panel (a little inside), take that colour
        rc = np.clip(r, lo + 1, hi - 1)
        pad = 3.0 / np.maximum(rc, 1)
        tc = np.clip(t, amin[k] + pad, amax[k] - pad)
        sx = np.clip(np.round(cx + rc * np.cos(tc)).astype(int), I, W - 1 - I)
        sy = np.clip(np.round(cy + rc * np.sin(tc)).astype(int), I, H - 1)
        col = a[sy, sx]
        beyond = np.clip((r - (hi - 4)) / 40.0, 0, 1)[..., None]     # past the outer band: into the sky
        col = col * (1 - beyond) + np.array(self.SKY, np.float32) * beyond
        col = np.round(col / 4) * 4
        mask = self.region_mask(origin, bg.size)
        out[..., :3] = out[..., :3] * (1 - mask[..., None]) + col * mask[..., None]
        out = bblib.img(out)
        return depth_soften(out, darken=darken) if blur_out else out

    def region_mask(self, origin, size):
        m = np.zeros((HD[1], HD[0]), np.float32)
        ox, oy = int(origin[0]), int(origin[1])
        W, H, I = size[0], size[1], self.RIM
        m[:oy, :] = 1
        m[oy:oy + H, :ox] = 1
        m[oy:oy + H, ox + W:] = 1
        # the rim inside the panel: full over its outer I-4 px, fading out over the last 4
        ramp = np.clip((I - np.arange(I + 1)) / 4.0, 0, 1)            # distance in from the edge -> weight
        for d in range(I + 1):
            w = ramp[d]
            m[oy:oy + H, ox + d] = np.maximum(m[oy:oy + H, ox + d], w)
            m[oy:oy + H, ox + W - 1 - d] = np.maximum(m[oy:oy + H, ox + W - 1 - d], w)
            m[oy + d, ox:ox + W] = np.maximum(m[oy + d, ox:ox + W], w)
        return m

    def region(self, R):
        return self.region_mask((R.ox, R.oy), R.bg.size)


PLANS["0289ba330e"] = ArcPlan()


#---------------------------------------------------------------------------------------------
# HOLLOW_CATHEDRAL: above the panel its stone wall goes on (no upside-down tree, window or banner)
#---------------------------------------------------------------------------------------------
# Panel art columns: lancet window 0..28 (framed inside the panel), banner 59..76, pillar 101..134, tree crown
# 143..250, a second pillar cut by the right edge (the centre pillar's columns shifted by 149).
CATH_WALL_X = ((29, 59), (77, 101), (135, 143))


def cathedral_labels(p):
    r, g, b, s, v = hsv(p)
    lab = np.full(p.shape[:2], -1, np.int16)
    y, x = rows(lab), cols(lab)
    for x0, x1 in CATH_WALL_X:
        lab[(y < 38) & (x >= x0) & (x < x1)] = 0
    xs = np.nonzero(g[0] * 255 > r[0] * 255 + 15)[0]
    xs = xs[(xs >= 143) & (xs < 251)]
    lab[(x >= xs.min() + 2) & (x <= xs.max() - 2) & (y < 24)] = 1     # the crown's top band, outlines included
    lab[(lab == 1) & (r > g)] = -1                                    # no branch or trunk pixels
    return lab


def cathedral_layout(x, y, lab):
    L = np.zeros(x.shape, np.int16)
    xs = np.nonzero(lab[0] == 1)[0]
    if len(xs):
        a, b = xs.min() - 2, min(xs.max() + 2, 247)
        xc, hw = (a + b) / 2.0, (b - a) / 2.0
        h = 22 * np.sqrt(np.clip(1 - ((x - xc) / hw) ** 2, 0, 1)) + wob(x, 2.0, 31) * (np.abs(x - xc) < hw)
        L[(y < 0) & (-y < h)] = 1
    return L


def cathedral_pre(R, lab):
    T, Lx, P = R.T, R.L, R.panel
    W = R.W

    def put(y, x, c):
        if 0 <= Lx + x < W and 0 <= T + y < R.H:
            R.A[T + y, Lx + x] = c; R.K[T + y, Lx + x] = True; R.P[T + y, Lx + x] = True

    # the window runs on up to the room's top: panes and divider bars, period 19 (rows 10..28), never flipped
    for y in range(-T, 0):
        src = 10 + ((y - 10) % 19)
        for x in range(0, 29):
            put(y, x, P[src, x])
    # its outer edge beyond the panel's left edge: the same frame shading as its right edge (outline, then shade)
    edge = [P[20, 24], P[20, 24], P[20, 24], P[20, 27], P[20, 27]]
    for y in range(-T, 35):
        for i, c in enumerate(edge):
            put(y, -1 - i, c if y < 33 else P[min(y, 143), 29])
    # both pillars carry on up (vertically uniform shafts); the right one also beyond the panel's right edge
    for y in range(-T, 0):
        for x in range(101, 135):
            put(y, x, P[0, x])
    for x in range(250, 250 + 36):
        sx = x - 149
        for y in (range(-T, 45) if x >= 256 else range(-T, 0)):
            put(y, x, P[max(y, 0), sx])
    # the banner hangs from a gilt rod a few rows above the panel's top edge
    for y in range(-6, 0):
        for x in range(59, 77):
            put(y, x, P[2, x])
    gold, dark, deep = P[20, 60], np.array((60, 57, 71), np.float32), np.array((160, 43, 80), np.float32)
    for x in range(56, 80):
        put(-8, x, gold); put(-7, x, deep if 58 < x < 77 else dark)
    for x in (55, 56, 79, 80):
        put(-9, x, gold); put(-8, x, gold); put(-7, x, dark)


PLANS["fbfe12b060"] = Plan(cathedral_labels, cathedral_layout, 2, sides=(46, 46), block=14, seed=21,
                           pre=cathedral_pre)


#---------------------------------------------------------------------------------------------
# PRISM_ARENA: princess-phoenix's arena (night panel at 2x, 512x384). Its builder lays a festival starfield over
# the panel's top 36 rows; above it the whole arena used to hang upside down (court floor at the top of the room),
# and the barrier wall at the panel's left edge folded back into a mirrored corner.
#  * left margin: the barrier is a wall in perspective whose top stays at panel row ~24 while its foot drops
#    ~0.24 px per px toward the viewer; each margin column is a wall column from 142 px to its right, scaled
#    about the top edge to the height the wall has there (floor rows keep the old extension: plain court floor);
#  * above the panel: night sky, painted after the builder's grade by prism_arena() below.
#---------------------------------------------------------------------------------------------
class PrismPlan(Plan):
    TOP, SLOPE, D = 12, 0.24, 71                       # art px (panel / 2)

    def __init__(self):
        Plan.__init__(self, None, None, 1)

    def floor_line(self, panel):
        r, g, b = panel[..., 0], panel[..., 1], panel[..., 2]
        fl = (r > 190) & (g > 120) & (b < 150) & (r - b > 60)
        out = np.zeros(panel.shape[1], np.float32)
        for x in range(panel.shape[1]):
            col = fl[:, x]
            out[x] = next((y for y in range(4, panel.shape[0] - 5) if col[y:y + 5].all()), panel.shape[0])
        return out

    def __call__(self, bg, origin, blur_out=True, darken=0.22, old=None):
        old_raw = old() if old else M._orig_extend(bg, origin=origin, blur_out=False)
        out = bblib.arr(old_raw)
        P = np.asarray(bg.convert("RGB"), np.float32)[::2, ::2]
        fl = self.floor_line(P)
        T, s, D = self.TOP, self.SLOPE, self.D
        ox, oy = int(origin[0]), int(origin[1])
        for X in range(-(ox // 2), 0):                  # margin art columns
            xs = X + D
            f_here = fl[0] + s * (-X)
            k = (fl[xs] - T) / (f_here - T)
            for Y in range(T, int(np.ceil(f_here)) + 1):
                sy = int(round(T + (Y - T) * k))
                c = P[min(sy, P.shape[0] - 1), xs]
                hx, hy = ox + 2 * X, oy + 2 * Y
                out[hy:hy + 2, hx:hx + 2, :3] = c
        img_ = bblib.img(out)
        return depth_soften(img_, darken=darken) if blur_out else img_

    def region_mask(self, origin, size):
        m = np.zeros((HD[1], HD[0]), np.float32)
        ox, oy = int(origin[0]), int(origin[1])
        m[:oy, :] = 1
        T, s, D = self.TOP, self.SLOPE, self.D
        # the wall rows of the left margin (to just past its foot)
        for hx in range(0, ox):
            X = (hx - ox) // 2
            f_here = 68 + s * (-X)
            m[oy:oy + int(2 * (f_here + 2)), hx] = 1
        return m

    def region(self, R):
        return self.region_mask((R.ox, R.oy), R.bg.size)


PLANS["58598da0c3"] = PrismPlan()


def prism_arena():
    """fields_f.prism_arena on the planned room, then the festival sky above the stands: Rejuvenation's New World
    starfield (the strip the builder lays over the panel's top) tiled upward, under the same violet wash deepening
    toward the zenith; the prism plates' strings run up out of sight."""
    import fields_c, fields_f
    from fields_d import capture
    hd, res = capture(fields_f.prism_arena, fields_c)
    stars = bblib.game_img("rejuvenation", "battlebgNewWorld").crop((0, 0, 512, 110))
    sky = Image.new("RGBA", (864, 150))
    for y0 in range(150 - 110, -110, -110):
        for x in range(0, 864, 512):
            sky.alpha_composite(stars, (x, y0))
    sky.alpha_composite(bblib.vgradient((864, 150), [(0, (6, 4, 26, 110)), (1, (20, 14, 60, 120))]))
    d = ImageDraw.Draw(sky)
    import fields_c as fc
    for i in range(18):                                  # the same plate positions as the builder
        a = i / 18 * 2 * math.pi + 0.1
        x = 520 + math.cos(a) * 320
        d.line([x, 0, x, 150], fill=(180, 160, 110, 255))
    top = Image.new("RGBA", HD); top.alpha_composite(sky, (0, 0))
    a = bblib.arr(hd); t = bblib.arr(top)
    a[:150] = t[:150]
    soft = bblib.arr(depth_soften(bblib.img(a)))
    a[:150] = soft[:150]
    hd = bblib.img(a)
    bblib.save_room("field_prism_arena", hd)
    res["origins"] = [o if o[0] != fields_c.OWN else [o[0], o[1] + ", night sky above the stands, the barrier "
                                                                  "continued in perspective"] for o in res["origins"]]
    return res


BUILDERS["PRISM_ARENA"] = prism_arena


#---------------------------------------------------------------------------------------------
# NEW_MOON (+ Abyss, Lamplight): Rejuvenation's Starlight rooftop. Above the panel the bokeh city simply goes on
# (quilted from the panel's city band, rows above the railing) instead of the railing and the tiled roof hanging
# upside down at the top of the room.
#---------------------------------------------------------------------------------------------
PLANS["d7e72cf70f"] = Plan(band_labels(0, 46), all_wall, 1, sides=(0, 0), block=18, seed=23)


#---------------------------------------------------------------------------------------------
def install():
    import sys
    M.PLANS.update(PLANS)
    mods = [m for m in list(sys.modules.values())
            if getattr(m, "__file__", None) and m.__file__.startswith(bblib.__file__.rsplit("/", 1)[0])]
    M.install_everywhere(mods)

