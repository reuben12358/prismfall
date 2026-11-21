"""Battle bases that sit where EBDX actually stands the battlers (bblib.FOE / bblib.PLAYER).

EBDX anchors the foe at room (234,152) and the player at (116,252) (HD 526.5,342 / 261,567) in every room; the
Bridge (007_Bridge_Placement.rb) puts every sprite's feet on those points. Most rooms paint their platforms there
(platform() / place_foe_base() are centred on FOE and PLAYER). A room that takes its base from a painted panel
instead has it wherever the panel's artist put it:

MEADOW  Magiscarf's panel is pasted at (110,150) so its worn grass ellipse ends up 34 px left of and 18 px above
        the foe point (Tauros stood on the grass beside it), and the panel has no ground for the player at all.
        meadow_bases() moves the worn patch onto the foe point (its own pixels and outline, shifted by whole art
        pixels; the ground it leaves is refilled from the same rows just left of it, so the hills' tufted edge
        and the grass bands run on; its mirror image in the right margin goes too) and lays the same patch, drawn
        1.5x as big (bblib.PLAYER_SCALE), under the player.

Everything here runs on the HD canvas right after the panel is extended (to_hd) and never above the panel's
horizon, so the painted margins above the panels are untouched.
"""
import numpy as np
from bblib import FOE, PLAYER, PLAYER_SCALE, arr, img

# measured on the day panel at ORIGIN (110,150): core of the worn patch x 388..595, y 302..347
MEADOW_CORE = (168, 203, 116)        # the worn patch
MEADOW_RIM = (122, 194, 69)          # its lighter rim (also the hills' lit band above it, y < 298)
MEADOW_BOX = (352, 290, 704, 360)    # where the patch (and its mirror beyond x 622) can be
MEADOW_SHIFT = (34, 18)              # its centre (492,325) onto FOE (526.5,342), in whole art pixels (2 HD px)
MEADOW_FILL = (240, 134)             # ground it leaves: the same rows, tiled from x 240..373 (left of the patch,
                                     # right of the rock and pebbles: the hills' tufted edge and plain grass)
MEADOW_FILL_DY = 56                  # its mirror's spot (blurred margin): the same columns this far down
MEADOW_PANEL_RIGHT = 622             # x of the panel's right edge (the margin beyond it is a mirror)


BARE = []                            # the last meadow_bases() call's worn cores (HD mask)


def keep_bare(room, before):
    """Undo what was painted on the worn cores since `before` (the meadow scatters wildflowers everywhere)."""
    a, b = arr(room), arr(before)
    a[BARE[0]] = b[BARE[0]]
    return img(a)


def _up(a):
    """Nearest-neighbour PLAYER_SCALE enlargement of a mask or an RGBA block."""
    h, w = a.shape[:2]
    ys = (np.arange(int(round(h * PLAYER_SCALE))) / PLAYER_SCALE).astype(int).clip(0, h - 1)
    xs = (np.arange(int(round(w * PLAYER_SCALE))) / PLAYER_SCALE).astype(int).clip(0, w - 1)
    return a[ys][:, xs]


def _material(a, box):
    """Worn-patch pixels: the core colour plus rim pixels next to it, below the hills' lit band."""
    x0, y0, x1, y1 = box
    rgb = a[..., :3].astype(np.int32)
    core = np.all(rgb == MEADOW_CORE, -1)
    rim = np.all(rgb == MEADOW_RIM, -1)
    near = core.copy()
    for _ in range(6):                                  # 12 px sideways, 6 px up/down (2 px steps)
        n = near.copy()
        n[:, 2:] |= near[:, :-2]; n[:, :-2] |= near[:, 2:]
        near = n
    v = near.copy()
    for _ in range(3):
        n = v.copy(); n[2:] |= v[:-2]; n[:-2] |= v[2:]; v = n
    m = core | (rim & v)
    keep = np.zeros_like(m); keep[y0:y1, x0:x1] = True
    keep[:298] = False
    return m & keep


def meadow_bases(*rooms):
    """Same edit on the day and the night room (identical geometry, the night panel is a palette swap).
    Each room: the HD canvas straight out of fields_h.to_hd, day first (the masks are read from it).
    Returns the edited canvases."""
    a0 = arr(rooms[0])
    mat = _material(a0, MEADOW_BOX)
    old = mat.copy(); old[:, MEADOW_PANEL_RIGHT:] = False          # the panel's own patch
    # its mirror in the right margin (x' = 2 * 622 - 1 - x; softened there, so mirrored, not colour-matched)
    mir = np.zeros_like(old)
    w = old.shape[1]
    xs_m = np.arange(MEADOW_PANEL_RIGHT, w)
    src = 2 * MEADOW_PANEL_RIGHT - 1 - xs_m
    okm = src >= 0
    mir[:, xs_m[okm]] = old[:, src[okm]]
    for _ in range(2):                                             # + the blur's spread
        n = mir.copy(); n[:, 2:] |= mir[:, :-2]; n[:, :-2] |= mir[:, 2:]; n[2:] |= mir[:-2]; n[:-2] |= mir[2:]
        mir = n
    mir[:, :MEADOW_PANEL_RIGHT] = False
    sx, sy = MEADOW_SHIFT
    new = np.zeros_like(old); new[sy:, sx:] = old[:-sy, :-sx]
    clear = old & ~new
    mir &= ~new
    # player patch: the same patch PLAYER_SCALE times bigger (bblib: 1.5x = 3 px art pixels), centred on PLAYER
    ys, xs = np.nonzero(old)
    bx0, by0 = xs.min() // 2 * 2, ys.min() // 2 * 2
    bx1, by1 = xs.max() // 2 * 2 + 2, ys.max() // 2 * 2 + 2
    pmask = _up(old[by0:by1, bx0:bx1])
    ph, pw = pmask.shape
    px0 = int(round(PLAYER[0] - pw / 2.0))
    py0 = int(round(PLAYER[1] - ph / 2.0))
    # the worn cores (no wildflowers on them: keep_bare)
    core = np.all(a0[..., :3].astype(np.int32) == MEADOW_CORE, -1) & old
    BARE.clear()
    BARE.append(np.zeros_like(old)); BARE[0][sy:, sx:] = core[:-sy, :-sx]
    pc = np.zeros_like(old)
    pc[py0:py0 + ph, px0:px0 + pw] = _up(core[by0:by1, bx0:bx1])
    BARE[0] |= pc
    out = []
    for room in rooms:
        a = arr(room)
        b = a.copy()
        yy, xx = np.nonzero(clear)
        b[yy, xx] = a[yy, MEADOW_FILL[0] + (xx - MEADOW_FILL[0]) % MEADOW_FILL[1]]   # 1. clear the old spot
        yy, xx = np.nonzero(mir)
        b[yy, xx] = a[yy + MEADOW_FILL_DY, xx]                          #    and its mirror beside the panel
        yy, xx = np.nonzero(new)
        b[yy, xx] = a[yy - sy, xx - sx]                                 # 2. the patch, on the foe point
        big = _up(a[by0:by1, bx0:bx1])                                  # 3. the player's patch, bigger
        reg = b[py0:py0 + ph, px0:px0 + pw]
        reg[pmask] = big[pmask]
        out.append(img(b))
    return out
