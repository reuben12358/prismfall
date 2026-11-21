#!/usr/bin/env python3
"""Double-battle bases: every room's own bases, widened for two battlers per side.

  python3 -I art/battlebacks/doubles.py [room ...]     # all rooms in graphics/EBDX/Battlebacks/battlebg

A room paints one base per side, sized for one battler (the foe base 232x50 HD, the player base bblib.PLAYER_SCALE
times that). Two battlers side by side overhang it, and EBDX's double points (foe room 198,152 / 256,164, player
92,240 / 192,262) stand some of them off it. Widening the bases in the room itself would make the singles bases huge
again, so each room gets two overlays, `elements/dbl_<room>_foe.png` and `elements/dbl_<room>_ally.png` (full HD
canvas, transparent outside the base), which `plugins/Prismfall EBDX Bridge/007_Bridge_Placement.rb` lays over the
room when that side has two battlers, standing them on it (DOUBLE_FOE / DOUBLE_ALLY there = the numbers below).

How a base is widened (its own rim, texture and colours, pixel for pixel):
  1. the base's exact pixels: the rooms are rebuilt with that side's ground point moved off the canvas (the same
     builders; bblib.FOE / bblib.PLAYER patched), and the base is what differs from the shipped room around the
     point (the connected part inside a window, so props that only avoid the point stay out);
  2. its left half moves left, its right half moves right, and the gap is filled with its own centre slab
     (SLAB px, where the rim runs flat) repeated: an ellipse becomes a stadium, rings become racetracks, ring stones
     and silk repeat along the straight. The widened base covers the singles base entirely.
"""
import os, subprocess, sys, tempfile, shutil, types
import numpy as np
from PIL import Image
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bblib

S = bblib.S
SLAB = 16
# side -> (left shift, right shift) in HD px (even: 2 px art pixels stay aligned)
SPREAD = {"foe": (66, 66), "ally": (36, 114)}
# where the Bridge stands the two battlers of a side (room px; 007_Bridge_Placement.rb DOUBLE_FOE / DOUBLE_ALLY):
#   foe:  centre 234 (bblib.FOE), 29 px either side; the right one (battler 1) a touch nearer, as in EBDX
#   ally: centre 261 + (114 - 36) / 2 = 300 HD = 133.3 room, 42 px either side, on the singles base's line (y 244)
DOUBLE_FOE = {1: (263, 153), 3: (205, 151)}
DOUBLE_ALLY = {0: (91, 243), 2: (175, 246)}
WINDOW = {"foe": (150, 44, 6), "ally": (200, 70, 10)}      # rx, ry, dy of the search ellipse (HD px)


def ground_point(side, room):
    if side == "foe":
        return bblib.FOE
    for fid in bblib.ROOM_PLAYER:
        if room.startswith("field_" + fid.lower()):
            return bblib.player_at(fid)
    return bblib.PLAYER


#---------------------------------------------------------------------------------------------
# Bare rooms (run in a subprocess: the builders import bblib's points at import time)
#---------------------------------------------------------------------------------------------
def build_bare(side, tmp):
    far = (-4000.0, -4000.0)
    name = "FOE" if side == "foe" else "PLAYER"
    old = getattr(bblib, name)
    setattr(bblib, name, far)
    bblib.OUT = tmp
    for fn in (bblib.save_room, bblib.save_element):
        fn.__defaults__ = (tmp,)
    targets = [bblib.place_foe_base] if side == "foe" else [bblib.place_player_base, bblib.place_player_base_scaled]
    for fn in targets:
        fn.__defaults__ = tuple(far if (isinstance(v, tuple) and v == old) else v for v in fn.__defaults__)
    import bases
    if side == "foe":
        bases.MEADOW_SHIFT = (2000, 2000)            # MEADOW: the worn patch is cleared and not laid on the foe point
    else:
        bases.player_at = lambda fid=None: (680.0, 640.0)   # MEADOW's player patch: on the canvas, far off
    sys.modules["transitions"] = types.SimpleNamespace(build=lambda: None)
    import build_backdrops as bb
    bb.write_ruby = lambda *a, **k: None
    bb.write_credits = lambda *a, **k: None
    bb.write_preview = lambda *a, **k: None
    bb.ORIGINS = os.path.join(tmp, "origins.json")
    bb.main([])


#---------------------------------------------------------------------------------------------
def base_mask(room, bare, c, win):
    a = np.asarray(room.convert("RGB")).astype(int)
    b = np.asarray(bare.convert("RGB")).astype(int)
    m = np.any(a != b, -1)
    H, W = m.shape
    ys, xs = np.mgrid[0:H, 0:W]
    m &= (((xs - c[0]) / win[0]) ** 2 + ((ys - c[1] - win[2]) / win[1]) ** 2) <= 1
    lab, n = ndimage.label(ndimage.binary_dilation(m, iterations=3))
    if n == 0:
        return m
    k = lab[int(c[1]), int(c[0])]
    if k == 0:
        k = int(np.argmax(ndimage.sum(m, lab, range(1, n + 1)))) + 1
    return m & (lab == k)


def widen(a, m, sl, sr):
    H, W = m.shape
    ys, xs = np.nonzero(m)
    cx = (xs.min() + xs.max() + 1) // 2 // 2 * 2
    out = np.zeros((H, W, 4), np.uint8)
    left = m.copy(); left[:, cx:] = False
    right = m.copy(); right[:, :cx] = False
    y, x = np.nonzero(left); ok = x - sl >= 0
    out[y[ok], x[ok] - sl] = a[y[ok], x[ok]]
    y, x = np.nonzero(right); ok = x + sr < W
    out[y[ok], x[ok] + sr] = a[y[ok], x[ok]]
    s0 = cx - SLAB // 2
    for gx in range(cx - sl, cx + sr):
        sx = s0 + (gx - (cx - sl)) % SLAB
        col = m[:, sx]
        out[col, gx] = a[col, sx]
    out[..., 3] = np.where(out[..., 3] > 0, 255, 0)
    return Image.fromarray(out, "RGBA")


def main(argv):
    if argv[:1] == ["--bare"]:
        build_bare(argv[1], argv[2])
        return
    rooms_dir = os.path.join(bblib.OUT, "battlebg")
    elem_dir = os.path.join(bblib.OUT, "elements")
    tmps = {}
    try:
        for side in ("foe", "ally"):
            tmps[side] = tempfile.mkdtemp(prefix="pf_dbl_%s_" % side)
            subprocess.run([sys.executable, "-I", os.path.abspath(__file__), "--bare",
                            "foe" if side == "foe" else "player", tmps[side]], check=True, stdout=subprocess.DEVNULL)
        names = sorted(f[:-7] for f in os.listdir(os.path.join(tmps["foe"], "battlebg")) if f.endswith("_hd.png"))
        if argv:
            names = [n for n in names if n in argv]
        for n in names:
            room = Image.open(os.path.join(rooms_dir, n + "_hd.png")).convert("RGBA")
            a = np.asarray(room)
            for side in ("foe", "ally"):
                bare = Image.open(os.path.join(tmps[side], "battlebg", n + "_hd.png"))
                m = base_mask(room, bare, ground_point(side, n), WINDOW[side])
                if m.sum() < 400:
                    print("no %s base found: %s" % (side, n))
                    continue
                widen(a, m, *SPREAD[side]).save(os.path.join(elem_dir, "dbl_%s_%s.png" % (n, side)), optimize=True)
            print("wrote elements/dbl_%s_{foe,ally}.png" % n)
    finally:
        for t in tmps.values():
            shutil.rmtree(t, ignore_errors=True)


if __name__ == "__main__":
    main(sys.argv[1:])
