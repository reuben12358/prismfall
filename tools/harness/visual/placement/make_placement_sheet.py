#!/usr/bin/env python3
"""Before/after sheet and battle-start GIF from the placement probe (003_PlacementProbe.rb).

  python3 -I make_placement_sheet.py sheet <before_dir> <after_dir> <out.png> [case ...]
  python3 -I make_placement_sheet.py gif <intro_dir> <frames_subdir> <out_base> [frame_ms=66] [last_frame]

Marks drawn on the real-engine frames (never retouched otherwise):
  cyan ellipse  the base painted in the room (mapped through that frame's room camera)
  red +         where EBDX stands the battler (BATTLERPOS anchor)
  yellow bar    the sprite's lowest opaque row in that frame (its feet)
"""
import csv, os, sys
from PIL import Image, ImageDraw

S = 2.25
FOE, PLAYER = (234, 152), (116, 252)                     # room px (PBS/EBDX/metrics.txt BATTLERPOS)
DEFAULT_BASES = [(526.5, 342.0, 116, 25), (261.0, 567.0, 232, 50)]   # HD centre, rx, ry (bblib FOE / PLAYER)
# painted bases that are not the default ones: (dir tag, case prefix) -> [foe, player] (None = no base)
BASES = {("before", "meadow"): [(492.0, 325.0, 118, 26), None],
         ("after", "meadow"): [(526.0, 343.0, 116, 26), (260.0, 568.0, 232, 54)]}
CYAN, RED, YELLOW = (60, 230, 255), (255, 40, 40), (255, 230, 40)


def load(d):
    rows = {}
    p = os.path.join(d, "probe.tsv")
    for r in csv.DictReader(open(p), delimiter="\t"):
        f = {k: (v if k in ("case", "view", "species") else float(v)) for k, v in r.items()}
        rows[(r["case"], r["view"], int(float(r["idx"])))] = f
    return rows


def cam(f):
    def to_screen(hx, hy):
        return (f["bg_x"] - (f["bg_ox"] - hx / S) * f["bg_zx"], f["bg_y"] - (f["bg_oy"] - hy / S) * f["bg_zy"])
    return to_screen


def bases_for(tag, case):
    for (t, pre), b in BASES.items():
        if t == tag and case.startswith(pre + "__"):
            return b
    return DEFAULT_BASES


def mark(im, rows, case, view, tag, ox=0, oy=0, sc=1.0):
    d = ImageDraw.Draw(im)
    f0 = rows.get((case, view, 1)) or rows.get((case, view, 0))
    if not f0:
        return
    ts = cam(f0)
    for b in bases_for(tag, case):
        if not b:
            continue
        cx, cy = ts(b[0], b[1])
        rx, ry = b[2] / S * f0["bg_zx"], b[3] / S * f0["bg_zy"]
        d.ellipse([(cx - rx - ox) * sc, (cy - ry - oy) * sc, (cx + rx - ox) * sc, (cy + ry - oy) * sc], outline=CYAN)
    for i in (0, 1):
        f = rows.get((case, view, i))
        if not f:
            continue
        ax, ay = (f["anchor_x"] - ox) * sc, (f["anchor_y"] - oy) * sc
        d.line([ax - 5, ay, ax + 5, ay], fill=RED, width=1)
        d.line([ax, ay - 5, ax, ay + 5], fill=RED, width=1)
        fy = f["spr_y"] + (f["feet_row"] + 1 - f["oy"]) * f["zoom_y"]
        fl = f["spr_x"] + (f["feet_l"] - f["ox"]) * f["zoom_x"]
        fr = f["spr_x"] + (f["feet_r"] + 1 - f["ox"]) * f["zoom_x"]
        d.line([(fl - ox) * sc, (fy - oy) * sc, (fr - ox) * sc, (fy - oy) * sc], fill=YELLOW, width=1)


def sheet(bdir, adir, out, cases):
    B, A = load(bdir), load(adir)
    if not cases:
        cases = []
        for (c, v, i) in A:
            if c not in cases and (c, "main", 1) in B:
                cases.append(c)
    MAIN = (180, 76, 540, 268)                 # foe side at the battle camera, 1:1
    mw, mh = MAIN[2] - MAIN[0], MAIN[3] - MAIN[1]
    sw, sh = 256, 192                          # send-out pull-back at 1/2
    lab = 16
    W = 2 * mw + 2 * sw + 12
    head = 58
    img = Image.new("RGB", (W, head + len(cases) * (mh + lab + 6)), (14, 14, 18))
    d = ImageDraw.Draw(img)
    d.text((6, 4), "Battler placement - real engine (mkxp-z + Essentials v21.1 + EBDX + Prismfall Bridge). "
                   "Columns: BEFORE / AFTER at the battle camera (foe side, 1:1), BEFORE / AFTER send-out pull-back "
                   "(1/2).", fill=(235, 235, 235))
    d.text((6, 20), "cyan = base painted in the room   red + = where EBDX stands the battler   yellow = sprite's "
                    "lowest opaque row (its feet) in that frame", fill=(235, 235, 235))
    d.text((6, 36), "BEFORE: EBDX's own species metrics (feet 2..26 px off the anchor), MEADOW's patch off the anchor, "
                    "no player patch. AFTER: Bridge grounding (foe feet 16 px in front of the base centre, player's on it, "
                    "floaters 20 px above that line), bases moved.",
           fill=(200, 200, 200))
    y = head
    for c in cases:
        foe, pl = c.split("__")[1:]
        d.text((6, y + 2), "%s   foe %s / player %s" % (c.split("__")[0].upper(), foe.upper(), pl.upper()),
               fill=(255, 220, 120))
        x = 0
        for tag, rows, dd in (("before", B, bdir), ("after", A, adir)):
            p = os.path.join(dd, c + "_main_clean.png")
            if os.path.exists(p):
                im = Image.open(p).convert("RGB")
                mark(im, rows, c, "main", tag)
                img.paste(im.crop(MAIN), (x, y + lab))
            d.text((x + 4, y + lab + 2), tag.upper(), fill=(255, 255, 255))
            x += mw + 4
        for tag, rows, dd in (("before", B, bdir), ("after", A, adir)):
            p = os.path.join(dd, c + "_sendout_clean.png")
            if os.path.exists(p):
                im = Image.open(p).convert("RGB").resize((sw, sh), Image.LANCZOS)
                mark(im, rows, c, "sendout", tag, sc=0.5)
                img.paste(im, (x, y + lab))
            d.text((x + 4, y + lab + 2), tag.upper() + " - send-out", fill=(255, 255, 255))
            x += sw + 4
        y += mh + lab + 6
    img.save(out, optimize=True)
    print(out, img.size, len(cases), "rooms")


def gif(idir, sub, out, ms=66, last=None):
    src = os.path.join(idir, sub)
    files = sorted(f for f in os.listdir(src) if f.endswith((".bmp", ".png")))
    if last is not None:
        files = files[:last + 1]
    log = {}
    p = os.path.join(idir, "intro.tsv")
    if os.path.exists(p):
        for r in csv.DictReader(open(p), delimiter="\t"):
            log[int(float(r["shot"]))] = {k: float(v) for k, v in r.items()}
    frames = [Image.open(os.path.join(src, f)).convert("RGB") for f in files]
    q = [f.quantize(160, dither=Image.NONE) for f in frames]
    q[0].save(out + ".gif", save_all=True, append_images=q[1:], duration=ms, loop=0, optimize=False)
    # key frames with the marks: painted bases through each frame's camera, the anchors
    n = 8
    strip = Image.new("RGB", (512 * 4, 384 * 2))
    picks = [int(k * (len(frames) - 1) / (n - 1)) for k in range(n)]
    for k, i in enumerate(picks):
        im = frames[i].copy()
        f = log.get(i)
        if f:
            d = ImageDraw.Draw(im)
            for (bx, by, rx, ry), (ex, ey) in zip(BASES[("after", "meadow")], (FOE, PLAYER)):
                cx = f["bg_x"] - (f["bg_ox"] - bx / S) * f["bg_zx"]; cy = f["bg_y"] - (f["bg_oy"] - by / S) * f["bg_zy"]
                ex_ = f["bg_x"] - (f["bg_ox"] - ex) * f["bg_zx"]; ey_ = f["bg_y"] - (f["bg_oy"] - ey) * f["bg_zy"]
                rxs, rys = rx / S * f["bg_zx"], ry / S * f["bg_zy"]
                d.ellipse([cx - rxs, cy - rys, cx + rxs, cy + rys], outline=CYAN)
                d.line([ex_ - 5, ey_, ex_ + 5, ey_], fill=RED); d.line([ex_, ey_ - 5, ex_, ey_ + 5], fill=RED)
        strip.paste(im, ((k % 4) * 512, (k // 4) * 384))
    strip.save(out + "_keys.png", optimize=True)
    print(out + ".gif", len(frames), "frames", os.path.getsize(out + ".gif") // 1024, "KB")


if __name__ == "__main__":
    if sys.argv[1] == "sheet":
        sheet(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5:])
    else:
        gif(sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5]) if len(sys.argv) > 5 else 66,
            int(sys.argv[6]) if len(sys.argv) > 6 else None)
