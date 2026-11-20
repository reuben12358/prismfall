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

    def __init__(self, labels, layout, nlab, sides=(0, 0), block=16, seed=1, top=True, feather=6):
        self.labels, self.layout, self.nlab = labels, layout, nlab
        self.sides, self.block, self.seed, self.top, self.feather = sides, block, seed, top, feather

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


#---------------------------------------------------------------------------------------------
def install():
    import sys
    M.PLANS.update(PLANS)
    mods = [m for m in list(sys.modules.values())
            if getattr(m, "__file__", None) and m.__file__.startswith(bblib.__file__.rsplit("/", 1)[0])]
    M.install_everywhere(mods)

