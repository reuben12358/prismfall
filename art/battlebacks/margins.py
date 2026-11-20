"""Round 5: room margins painted from the room's own pixels instead of mirrored.

bblib.extend_vanilla fills everything around a 512x288 vanilla panel by reflecting it (sides and top) and by
scaling its lowest rows 2x (floor). Whenever EBDX's camera leaves the default framing (the opening close-up on
the foe, the send-out pull-back, the idle camera drifts) those margins come into view: upside-down crags and
trees, symmetric "butterfly" rocks at the panel's sides, a second copy of the panel's foreground at double
pixel size below it.

Here a margin is synthesised instead, at the panel's own art-pixel size and from the panel's own pixels
(patch-based texture synthesis, "texture by numbers"): every panel pixel gets a material label (rock, water,
canopy, sky...), the margin gets a hand-designed label layout that continues the panel's shapes, and the
margin is quilted from panel patches whose labels match that layout. Patches are copied, never flipped, so no
scenery is ever upside down or mirrored, and only small patches are used, so no recognisable object is
duplicated. Seams between patches follow a minimum-error cut. The panel itself is never changed; the margin is
then softened and dimmed exactly like before (bblib.depth_soften).

Used through `install(module_or_fn, plans)`: a plan is keyed by the md5 of the panel's pixels, so every room
that extends that panel (stage variants, night rooms) gets the same painted margins.
"""
import hashlib, math, random
import numpy as np
from PIL import Image
from scipy.signal import fftconvolve
import bblib
from bblib import HD, arr, img, depth_soften

_orig_extend = bblib.extend_vanilla


def src_key(bg):
    return hashlib.md5(bg.tobytes()).hexdigest()[:10]


def pixel_scale(bg):
    """Size of the panel's art pixel in panel pixels (pixel art drawn at 2x -> 2)."""
    a = np.asarray(bg.convert("RGB")).astype(np.int16)
    for s in (4, 3, 2):
        h, w = (a.shape[0] // s) * s, (a.shape[1] // s) * s
        b = a[:h, :w].reshape(h // s, s, w // s, s, 3)
        if (b == b[:, :1, :, :1]).all(axis=(1, 3, 4)).mean() > 0.995:
            return s
    return 1


#---------------------------------------------------------------------------------------------
# Image quilting (Efros & Freeman 2001) with a label term (texture by numbers)
#---------------------------------------------------------------------------------------------
def _corr(a, k):
    """Valid-mode cross-correlation of 2-D `a` with kernel `k`."""
    return fftconvolve(a, k[::-1, ::-1], mode="valid")


def _cut_vertical(err):
    """Min-error path top->bottom through err (h x w); returns per-row column index of the cut."""
    h, w = err.shape
    cost = err.copy()
    back = np.zeros((h, w), np.int32)
    for y in range(1, h):
        for x in range(w):
            lo, hi = max(0, x - 1), min(w, x + 2)
            j = lo + int(np.argmin(cost[y - 1, lo:hi]))
            back[y, x] = j
            cost[y, x] += cost[y - 1, j]
    path = np.zeros(h, np.int32)
    path[-1] = int(np.argmin(cost[-1]))
    for y in range(h - 1, 0, -1):
        path[y - 1] = back[y, path[y]]
    return path


class Exemplar:
    def __init__(self, pix, labels, nlab, block):
        self.pix = pix.astype(np.float32)                       # h x w x 3 (art pixels)
        self.lab = labels.astype(np.int16)                      # h x w, -1 = never sample
        self.nlab = nlab
        self.B = block
        self.sq = (self.pix ** 2).sum(-1)
        self.onehot = [(self.lab == c).astype(np.float32) for c in range(nlab)]
        bad = (self.lab < 0).astype(np.float32)
        k = np.ones((block, block), np.float32)
        self.invalid = _corr(bad, k) > 0.5
        self.usage = np.zeros(self.invalid.shape, np.float32)


def quilt_rect(A, K, P, Lt, ex, y0, y1, x0, x1, ov, rng, lam=2500.0, tol=0.12, reuse=60.0):
    """Fill A[y0:y1, x0:x1] in raster order (down, then right). A: H x W x 3 float canvas (art px),
    K: known mask (updated), P: protected mask (never written), Lt: target labels (-1 = don't care).
    Each block's window starts `ov` px above/left of its write area, so it overlaps what is already known."""
    B = ex.B
    st = B - ov
    H, W = K.shape
    for by in range(y0, y1, st):
        for bx in range(x0, x1, st):
            wy, wx = by - ov, bx - ov
            sy0, sx0 = max(wy, 0), max(wx, 0)
            sy1, sx1 = min(wy + B, H), min(wx + B, W)
            # window (clipped to the canvas) and its offset inside a full B x B block
            oy, ox = sy0 - wy, sx0 - wx
            h, w = sy1 - sy0, sx1 - sx0
            win = A[sy0:sy1, sx0:sx1]
            km = K[sy0:sy1, sx0:sx1].astype(np.float32)
            lt = Lt[sy0:sy1, sx0:sx1]
            kf = np.zeros((B, B), np.float32); kf[oy:oy + h, ox:ox + w] = km
            wf = np.zeros((B, B, 3), np.float32); wf[oy:oy + h, ox:ox + w] = win
            nk = kf.sum()
            cost = np.zeros(ex.invalid.shape, np.float32)
            if nk > 0:
                ssd = _corr(ex.sq, kf)
                for c in range(3):
                    ssd -= 2 * _corr(ex.pix[..., c], kf * wf[..., c])
                ssd += (kf[..., None] * wf ** 2).sum()
                cost += np.maximum(ssd, 0) / (3 * nk)
            ltf = np.full((B, B), -1, np.int16); ltf[oy:oy + h, ox:ox + w] = lt
            nl = (ltf >= 0).sum()
            if nl > 0:
                match = np.zeros_like(cost)
                for c in range(ex.nlab):
                    m = (ltf == c).astype(np.float32)
                    if m.any():
                        match += _corr(ex.onehot[c], m)
                cost += lam * (1 - match / nl)
            cost += reuse * ex.usage
            cost[ex.invalid] = 1e12
            best = cost.min()
            cand = np.argwhere(cost <= best * (1 + tol) + 1.0)
            py, px = cand[rng.randrange(len(cand))]
            r = max(1, B // 2)
            ex.usage[max(py - r, 0):py + r, max(px - r, 0):px + r] += 1
            patch = ex.pix[py:py + B, px:px + B][oy:oy + h, ox:ox + w]
            # minimum-error boundary cut through the known overlap
            take = np.ones((h, w), bool)
            err = ((patch - win) ** 2).sum(-1) * km
            lo = max(ov - ox, 0)                                   # columns of left overlap inside window
            if lo > 0 and km[:, :lo].any():
                path = _cut_vertical(err[:, :lo] + 1e-3)
                for yy in range(h):
                    take[yy, :path[yy]] = False
            to = max(ov - oy, 0)
            if to > 0 and km[:to, :].any():
                path = _cut_vertical(err[:to, :].T + 1e-3)
                for xx in range(w):
                    take[:path[xx], xx] = False
            take |= ~K[sy0:sy1, sx0:sx1]                           # unknown pixels always come from the patch
            take &= ~P[sy0:sy1, sx0:sx1]
            # the write area itself is always filled
            ay0, ax0 = by - sy0, bx - sx0
            take[max(ay0, 0):, max(ax0, 0):] |= ~P[sy0:sy1, sx0:sx1][max(ay0, 0):, max(ax0, 0):]
            win[take] = patch[take]
            K[sy0:sy1, sx0:sx1] |= take
    return A


def _flip(arrs, axis):
    return [np.flip(a, axis=axis).copy() if a is not None else None for a in arrs]


def quilt_region(A, K, P, Lt, ex, y0, y1, x0, x1, ov, rng, direction="down", **kw):
    """quilt_rect in any of four growth directions (by flipping canvas AND exemplar, so the patches themselves are
    never mirrored in the result)."""
    H, W = K.shape
    if direction == "down":
        return quilt_rect(A, K, P, Lt, ex, y0, y1, x0, x1, ov, rng, **kw)
    axis = 0 if direction == "up" else 1
    A2, K2, P2, L2 = _flip([A, K, P, Lt], axis)
    ex2 = Exemplar(np.flip(ex.pix, axis), np.flip(ex.lab, axis), ex.nlab, ex.B)
    if axis == 0:
        ny0, ny1, nx0, nx1 = H - y1, H - y0, x0, x1
    else:
        ny0, ny1, nx0, nx1 = y0, y1, W - x1, W - x0
        # rows still go top->bottom; growth goes left->right in the flipped frame
    quilt_rect(A2, K2, P2, L2, ex2, ny0, ny1, nx0, nx1, ov, rng, **kw)
    A[...] = np.flip(A2, axis); K[...] = np.flip(K2, axis)
    return A


#---------------------------------------------------------------------------------------------
# A panel on the HD canvas, in art pixels
#---------------------------------------------------------------------------------------------
class Room:
    """Art-pixel canvas covering the whole HD room around a panel placed at HD `origin`."""

    def __init__(self, bg, origin, scale=None):
        self.bg = bg.convert("RGBA")
        self.s = s = scale or pixel_scale(bg)
        self.ox, self.oy = int(origin[0]), int(origin[1])
        self.bw, self.bh = bg.width // s, bg.height // s
        self.L = int(math.ceil(self.ox / s))
        self.T = int(math.ceil(self.oy / s))
        self.R = int(math.ceil((HD[0] - self.ox - bg.width) / s))
        self.Bm = int(math.ceil((HD[1] - self.oy - bg.height) / s))
        self.W = self.L + self.bw + max(self.R, 0)
        self.H = self.T + self.bh + max(self.Bm, 0)
        self.A = np.zeros((self.H, self.W, 3), np.float32)
        self.K = np.zeros((self.H, self.W), bool)
        self.panel = np.asarray(self.bg.convert("RGB"), np.float32)[::s, ::s][:self.bh, :self.bw]
        self.A[self.T:self.T + self.bh, self.L:self.L + self.bw] = self.panel
        self.K[self.T:self.T + self.bh, self.L:self.L + self.bw] = True
        self.P = self.K.copy()
        self.Lt = np.full((self.H, self.W), -1, np.int16)
        ys, xs = np.mgrid[0:self.H, 0:self.W]
        self.ys, self.xs = ys - self.T, xs - self.L          # panel art coordinates of every canvas pixel

    # panel-coordinate helpers -------------------------------------------------------------
    def region(self, name):
        """Canvas slices (y0, y1, x0, x1) of the four margins."""
        T, L, bh, bw = self.T, self.L, self.bh, self.bw
        return {"left": (T, T + bh, 0, L), "right": (T, T + bh, L + bw, self.W),
                "top": (0, T, 0, self.W), "bottom": (T + bh, self.H, 0, self.W)}[name]

    def set_labels_panel(self, lab):
        self.Lt[self.T:self.T + self.bh, self.L:self.L + self.bw] = lab

    def paint(self, layout_fn):
        """layout_fn(xs, ys) -> labels for every canvas pixel (panel art coords; only margins are used)."""
        lab = layout_fn(self.xs.astype(np.float32), self.ys.astype(np.float32)).astype(np.int16)
        m = ~self.P
        self.Lt[m] = lab[m]

    def fill(self, ex, order=("left", "right", "top", "bottom"), ov=None, seed=0, **kw):
        rng = random.Random(seed)
        ov = ov or max(2, ex.B // 3)
        for name in order:
            if isinstance(name, tuple):
                name, rect = name[0], name[1]
            else:
                rect = None
            y0, y1, x0, x1 = rect or self.region(name)
            if y1 <= y0 or x1 <= x0:
                continue
            d = {"left": "left", "right": "down", "top": "up", "bottom": "down"}[name]
            if d == "left":
                # grow leftwards: flip horizontally; inside the strip rows are processed top->bottom
                quilt_region(self.A, self.K, self.P, self.Lt, ex, y0, y1, x0, x1, ov, rng, direction="left", **kw)
            else:
                quilt_region(self.A, self.K, self.P, self.Lt, ex, y0, y1, x0, x1, ov, rng, direction=d, **kw)

    def hd(self):
        """Unsoftened HD canvas (RGBA) from the art canvas."""
        s = self.s
        a = np.clip(np.round(self.A), 0, 255).astype(np.uint8)
        big = np.repeat(np.repeat(a, s, 0), s, 1)
        cx, cy = self.L * s - self.ox, self.T * s - self.oy
        big = big[cy:cy + HD[1], cx:cx + HD[0]]
        out = np.full((HD[1], HD[0], 4), 255, np.uint8)
        out[:big.shape[0], :big.shape[1], :3] = big
        im = Image.fromarray(out, "RGBA")
        # the panel itself at its own resolution (not re-sampled), exactly where extend_vanilla puts it
        im.alpha_composite(self.bg, (self.ox, self.oy))
        return im


def hd_to_art(room, hd):
    """Sample an HD canvas (RGBA image) on the room's art grid (top-left HD pixel of every art pixel)."""
    s = room.s
    a = np.asarray(hd.convert("RGB"), np.float32)
    xs = np.clip(room.ox + s * (np.arange(room.W) - room.L), 0, HD[0] - 1)
    ys = np.clip(room.oy + s * (np.arange(room.H) - room.T), 0, HD[1] - 1)
    return a[ys][:, xs]


def seed_from(room, hd, regions):
    """Copy the given margins of an existing (unsoftened) HD canvas into the room and protect them."""
    a = hd_to_art(room, hd)
    for name in regions:
        y0, y1, x0, x1 = room.region(name)
        room.A[y0:y1, x0:x1] = a[y0:y1, x0:x1]
        room.K[y0:y1, x0:x1] = True
        room.P[y0:y1, x0:x1] = True


def old_floor(canvas, origin, bh, floor_band=110, floor_scale=2):
    """bblib.extend_vanilla's floor step (the panel's lowest rows scaled up and blended under the seam), applied to
    an unsoftened HD canvas whose rows origin[1]..origin[1]+bh hold the panel and its side margins."""
    W, H = HD
    oy = int(origin[1])
    c = arr(canvas)
    row = c[oy:oy + bh]
    band = row[bh - floor_band:bh]
    big = arr(img(band).resize((W * floor_scale, floor_band * floor_scale), Image.NEAREST))
    cx = (W * floor_scale - W) // 2
    big = big[:, cx:cx + W]
    start = oy + bh - 18
    need = H - start
    reps = int(math.ceil(need / big.shape[0])) + 1
    stack = np.concatenate([big] * reps, axis=0)[:need]
    for i in range(need):
        y = start + i
        if i < 18 and y < oy + bh:
            t = i / 18.0
            c[y] = c[y] * (1 - t) + stack[i] * t
        else:
            c[y] = stack[i]
    return img(c)


def compose(room, floor="paint", blur_out=True, darken=0.22):
    """The finished HD room: painted margins, the panel 1:1, and either the painted floor or the old scaled one."""
    out = room.hd()
    if floor == "old":
        out = old_floor(out, (room.ox, room.oy), room.bg.height)
    if blur_out:
        out = depth_soften(out, darken=darken)
    return out


#---------------------------------------------------------------------------------------------
# Installing plans: extend_vanilla is swapped while a field's builder runs
#---------------------------------------------------------------------------------------------
PLANS = {}          # src_key -> fn(bg, origin, **kw) -> unsoftened-or-softened HD canvas (as extend_vanilla)
_cache = {}


def extend_vanilla(bg, origin=bblib.VANILLA_ORIGIN, floor_band=110, floor_scale=2, blur_out=True,
                   side_mode="reflect", top_mode="reflect", darken=0.22):
    k = src_key(bg)
    plan = PLANS.get(k)
    if plan is None:
        return _orig_extend(bg, origin=origin, floor_band=floor_band, floor_scale=floor_scale, blur_out=blur_out,
                            side_mode=side_mode, top_mode=top_mode, darken=darken)
    ck = (k, tuple(origin), blur_out, darken, side_mode, top_mode, floor_band, floor_scale)
    if ck not in _cache:
        # `old`: the builder's own (mirrored) extension, unsoftened, with every argument it asked for (side_mode...):
        # plans keep it everywhere they don't repaint
        _cache[ck] = plan(bg, origin, blur_out=blur_out, darken=darken,
                          old=lambda: _orig_extend(bg, origin=origin, floor_band=floor_band, floor_scale=floor_scale,
                                                   side_mode=side_mode, top_mode=top_mode, blur_out=False))
    return _cache[ck].copy()


def install_everywhere(modules):
    """Point every module's extend_vanilla at the planned version."""
    for m in modules:
        if getattr(m, "extend_vanilla", None) is _orig_extend:
            m.extend_vanilla = extend_vanilla


#---------------------------------------------------------------------------------------------
# Labels and layouts
#---------------------------------------------------------------------------------------------
def kmeans_labels(panel, k=4, blur=2.0, seed=0, iters=25):
    """Material labels for a panel (art pixels): k-means on a blurred copy, so a material's own shading levels stay
    in one label."""
    from PIL import ImageFilter
    im = Image.fromarray(np.clip(panel, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(blur))
    x = np.asarray(im, np.float32).reshape(-1, 3)
    rng = np.random.RandomState(seed)
    c = x[rng.choice(len(x), k, replace=False)]
    for _ in range(iters):
        d = ((x[:, None, :] - c[None]) ** 2).sum(-1)
        l = d.argmin(1)
        for j in range(k):
            if (l == j).any():
                c[j] = x[l == j].mean(0)
    return l.reshape(panel.shape[:2]).astype(np.int16)


def wobble(t, amp, seed, freqs=(0.07, 0.16, 0.37)):
    r = random.Random(seed)
    out = np.zeros_like(t, dtype=np.float32)
    for i, f in enumerate(freqs):
        out += amp / (1 + i) * np.sin(t * f + r.uniform(0, 6.283))
    return out


def extrude_layout(lab, amp=3.0, seed=0, lean=(0.0, 0.0)):
    """Layout continuing the panel's edge labels outward: above the panel every column keeps the label of the
    panel's top row (boundaries wander by `amp` art px), beside it every row keeps the label of the edge column.
    `lean`: horizontal drift per row above the panel (left, right half) so walls can splay."""
    bh, bw = lab.shape

    def fn(x, y):
        out = np.zeros(x.shape, np.int16)
        # above: column label of the top row
        xs = x + wobble(y, amp, seed) + np.where(x < bw / 2, lean[0], lean[1]) * np.minimum(y, 0)
        xi = np.clip(np.round(xs), 0, bw - 1).astype(int)
        top = lab[0][xi]
        # sides: row label of the edge column
        ys = y + wobble(x, amp, seed + 1)
        yi = np.clip(np.round(ys), 0, bh - 1).astype(int)
        left = lab[:, 0][yi]; right = lab[:, bw - 1][yi]
        out = np.where(y < 0, top, np.where(x < 0, left, np.where(x >= bw, right, lab[np.clip(y, 0, bh - 1).astype(int), np.clip(x, 0, bw - 1).astype(int)])))
        return out
    return fn
