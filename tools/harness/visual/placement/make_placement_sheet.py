#!/usr/bin/env python3
"""Before/after sheet and battle-start GIF from the placement probe (003_PlacementProbe.rb).

  python3 -I make_placement_sheet.py sheet <before_dir> <after_dir> <out.png> [case ...]
  python3 -I make_placement_sheet.py ally <before_dir> <after_dir> <out.png> [--tag v1|before] [--title T] [--legend L] case ...
  python3 -I make_placement_sheet.py doubles <before_dir> <after_dir> <out.png> case ...
  python3 -I make_placement_sheet.py gif <intro_dir> <frames_subdir> <out_base> [frame_ms=66] [last_frame]

Marks drawn on the real-engine frames (never retouched otherwise):
  cyan ellipse  the base painted in the room (mapped through that frame's room camera)
  red +         where EBDX stands the battler (BATTLERPOS anchor)
  yellow bar    the sprite's lowest opaque row in that frame (its feet)
"""
import csv, os, sys
from PIL import Image, ImageDraw

S = 2.25
FOE, PLAYER = (234, 152), (116, 244)                     # room px: EBDX BATTLERPOS, player raised by the Bridge
ROOM_RAISE = {"frozen_lake": 8}                          # extra player raise (bblib.ROOM_PLAYER), room px
# painted bases, HD centre, rx, ry, per capture state:
#   "before" = the original rooms: player base 2x the foe base at EBDX's point (116,252)
#   "v1"     = player base 1.5x, point raised 8 room px          "after" = v2: 1.3x (MEADOW 1.2x, FROZEN_LAKE 1.15x
#              and 8 room px higher still)
TAG_BASES = {"before": [(526.5, 342.0, 116, 25), (261.0, 567.0, 232, 50)],
             "v1": [(526.5, 342.0, 116, 25), (261.0, 549.0, 174, 37.5)],
             "after": [(526.5, 342.0, 116, 25), (261.0, 549.0, 151, 32.5)]}
# rooms whose bases differ: (state, case prefix) -> [foe, player] (None = no base)
BASES = {("before", "meadow"): [(492.0, 325.0, 118, 26), None],
         ("v1", "meadow"): [(526.0, 343.0, 116, 26), (261.0, 548.0, 175, 39)],
         ("after", "meadow"): [(526.0, 343.0, 116, 26), (260.0, 549.0, 146, 33)],
         ("before", "frozen_lake"): [(526.5, 342.0, 126, 31), (261.0, 567.0, 252, 62)],
         ("v1", "frozen_lake"): [(526.5, 342.0, 126, 31), (261.0, 549.0, 189, 46.5)],
         ("after", "frozen_lake"): [(526.5, 342.0, 126, 31), (261.0, 531.0, 145, 35.5)]}
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
    return TAG_BASES[tag]


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
    d.text((6, 36), "BEFORE: EBDX's species metrics, MEADOW's patch off the anchor, player base 2x the foe's. AFTER: Bridge "
                    "grounding (foe feet 16 px in front of the centre, floaters 20 px up), bases moved, player base 1.3x.",
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


def ally(bdir, adir, out, cases, before_tag="v1", title=None, legend=None):
    """Ally before/after: per room, the send-out pull-back and the battle camera (whole frames, 1/2), before
    (state `before_tag`) and after."""
    B, A = load(bdir), load(adir)
    sw, sh = 256, 192
    lab, head = 16, 60
    W = 4 * (sw + 4)
    img = Image.new("RGB", (W, head + len(cases) * (sh + lab + 6)), (14, 14, 18))
    d = ImageDraw.Draw(img)
    d.text((6, 4), title or "Ally placement - real engine (mkxp-z + EBDX + Prismfall Bridge). Send-out pull-back and "
                            "battle camera (1/2), BEFORE / AFTER.", fill=(235, 235, 235))
    for k, line in enumerate((legend or "").split("\n")):
        d.text((6, 20 + 13 * k), line, fill=(200, 200, 200))
    y = head
    for c in cases:
        foe, pl = c.split("__")[1:]
        d.text((6, y + 2), "%s   player %s / foe %s" % (c.split("__")[0].upper(), pl.upper(), foe.upper()),
               fill=(255, 220, 120))
        x = 0
        for view in ("sendout", "main"):
            for tag, rows, dd in ((before_tag, B, bdir), ("after", A, adir)):
                p = os.path.join(dd, "%s_%s_clean.png" % (c, view))
                if os.path.exists(p):
                    im = Image.open(p).convert("RGB")
                    im = im.resize((sw, sh), Image.LANCZOS)
                    mark(im, rows, c, view, tag, sc=0.5)
                    img.paste(im, (x, y + lab))
                d.rectangle([x, y + lab, x + 150, y + lab + 13], fill=(14, 14, 18))
                d.text((x + 4, y + lab + 1), ("BEFORE" if tag != "after" else "AFTER") +
                       (" - pull-back" if view == "sendout" else " - battle camera"),
                       fill=(255, 255, 255) if tag != "after" else (140, 255, 160))
                x += sw + 4
        y += sh + lab + 6
    img.save(out, optimize=True)
    print(out, img.size, len(cases), "rooms")


def mark_all(im, rows, case, view, sc=0.5):
    """Every battler of a frame: red + = where EBDX stands it, yellow = its feet."""
    d = ImageDraw.Draw(im)
    for (c, v, i), f in rows.items():
        if c != case or v != view:
            continue
        ax, ay = f["anchor_x"] * sc, f["anchor_y"] * sc
        d.line([ax - 4, ay, ax + 4, ay], fill=RED); d.line([ax, ay - 4, ax, ay + 4], fill=RED)
        fy = f["spr_y"] + (f["feet_row"] + 1 - f["oy"]) * f["zoom_y"]
        fl = f["spr_x"] + (f["feet_l"] - f["ox"]) * f["zoom_x"]
        fr = f["spr_x"] + (f["feet_r"] + 1 - f["ox"]) * f["zoom_x"]
        d.line([fl * sc, fy * sc, fr * sc, fy * sc], fill=YELLOW)


def doubles(bdir, adir, out, cases):
    """Double battles before/after: per room, the battle camera and the send-out pull-back (1/2), BEFORE / AFTER."""
    B, A = load(bdir), load(adir)
    sw, sh, lab, head = 256, 192, 16, 60
    img = Image.new("RGB", (4 * (sw + 4), head + len(cases) * (sh + lab + 6)), (14, 14, 18))
    d = ImageDraw.Draw(img)
    d.text((6, 4), "Double battles - real engine (mkxp-z + Essentials v21.1 + EBDX + Prismfall Bridge). Battle camera and "
                   "send-out pull-back, 1/2 size, BEFORE / AFTER.", fill=(235, 235, 235))
    d.text((6, 20), "BEFORE: the singles bases, EBDX's double points (near foe on the base's front rim, right-hand ally "
                    "off its base).", fill=(200, 200, 200))
    d.text((6, 33), "AFTER: each side's own base widened for two (art/battlebacks/doubles.py), battlers stood on it "
                    "(007_Bridge_Placement.rb DOUBLE_FOE / DOUBLE_ALLY).   red + = where each battler stands   "
                    "yellow = its feet", fill=(200, 200, 200))
    y = head
    for c in cases:
        room, foe, pl = c.split("__")
        d.text((6, y + 2), "%s   foes %s   allies %s" % (room.upper(), foe.upper().replace("+", " + "),
                                                         pl.upper().replace("+", " + ")), fill=(255, 220, 120))
        x = 0
        for view in ("main", "sendout"):
            for tag, rows, dd in (("before", B, bdir), ("after", A, adir)):
                p = os.path.join(dd, "%s_%s_clean.png" % (c, view))
                if os.path.exists(p):
                    im = Image.open(p).convert("RGB").resize((sw, sh), Image.LANCZOS)
                    mark_all(im, rows, c, view)
                    img.paste(im, (x, y + lab))
                d.rectangle([x, y + lab, x + 150, y + lab + 13], fill=(14, 14, 18))
                d.text((x + 4, y + lab + 1), tag.upper() + (" - battle camera" if view == "main" else " - pull-back"),
                       fill=(255, 255, 255) if tag == "before" else (140, 255, 160))
                x += sw + 4
        y += sh + lab + 6
    img.save(out, optimize=True)
    print(out, img.size, len(cases), "rooms")


def gif(idir, sub, out, ms=66, last=None):
    src = os.path.join(idir, sub)
    files = sorted(f for f in os.listdir(src) if f.endswith((".bmp", ".png")))
    if last is not None:
        files = files[:last + 1]
    log = {}
    p = os.path.join(idir, "intro_%s.tsv" % sub[3:] if sub.startswith("pp_") else "intro.tsv")
    if not os.path.exists(p):
        p = os.path.join(idir, "intro.tsv")
    if os.path.exists(p):
        for r in csv.DictReader(open(p), delimiter="\t"):
            log[int(float(r["shot"]))] = {k: float(v) for k, v in r.items()}
    frames = [Image.open(os.path.join(src, f)).convert("RGB") for f in files]
    case = sub[3:] if sub.startswith("pp_") else sub
    room, foe, pl_sp = (case.split("__") + ["", ""])[:3]
    title = "%s battle start - foe %s, ally %s - real engine (mkxp-z + EBDX + Prismfall Bridge), every 2nd frame, " \
            "half speed" % (room.upper(), foe.upper(), pl_sp.upper())
    # GIF: the real frames, untouched, with a caption bar under them
    cap = 16
    q = []
    for k, fr in enumerate(frames):
        c = Image.new("RGB", (fr.width, fr.height + cap), (14, 14, 18))
        c.paste(fr, (0, 0))
        dc = ImageDraw.Draw(c)
        dc.text((4, fr.height + 2), "%s battle start - real engine, half speed" % room.upper(), fill=(220, 220, 220))
        dc.text((fr.width - 44, fr.height + 2), "%4.1fs" % (k * 2 / 60.0), fill=(255, 220, 120))
        q.append(c.quantize(160, dither=Image.NONE))
    q[0].save(out + ".gif", save_all=True, append_images=q[1:], duration=ms, loop=0, optimize=False)
    # key frames with the marks: painted bases through each frame's camera, the anchors
    n = 8
    head, lab = 34, 14
    strip = Image.new("RGB", (512 * 4, head + (384 + lab) * 2), (14, 14, 18))
    ds = ImageDraw.Draw(strip)
    ds.text((6, 4), title, fill=(235, 235, 235))
    ds.text((6, 19), "Key frames. cyan = bases painted in the room (through that frame's camera)   red + = where EBDX "
                     "stands each battler (the ally's feet land just in front of it)", fill=(200, 200, 200))
    picks = [int(k * (len(frames) - 1) / (n - 1)) for k in range(n)]
    for k, i in enumerate(picks):
        im = frames[i].copy()
        f = log.get(i)
        if f:
            d = ImageDraw.Draw(im)
            pl = (PLAYER[0], PLAYER[1] - ROOM_RAISE.get(room, 0))
            for (bx, by, rx, ry), (ex, ey) in zip(bases_for("after", case), (FOE, pl)):
                cx = f["bg_x"] - (f["bg_ox"] - bx / S) * f["bg_zx"]; cy = f["bg_y"] - (f["bg_oy"] - by / S) * f["bg_zy"]
                ex_ = f["bg_x"] - (f["bg_ox"] - ex) * f["bg_zx"]; ey_ = f["bg_y"] - (f["bg_oy"] - ey) * f["bg_zy"]
                rxs, rys = rx / S * f["bg_zx"], ry / S * f["bg_zy"]
                d.ellipse([cx - rxs, cy - rys, cx + rxs, cy + rys], outline=CYAN)
                d.line([ex_ - 5, ey_, ex_ + 5, ey_], fill=RED); d.line([ex_, ey_ - 5, ex_, ey_ + 5], fill=RED)
        x, y = (k % 4) * 512, head + (k // 4) * (384 + lab)
        ds.text((x + 4, y), "%d. t = %.1f s" % (k + 1, i * 2 / 60.0), fill=(255, 220, 120))
        strip.paste(im, (x, y + lab))
    strip.save(out + "_keys.png", optimize=True)
    print(out + ".gif", len(frames), "frames", os.path.getsize(out + ".gif") // 1024, "KB")


if __name__ == "__main__":
    if sys.argv[1] == "sheet":
        sheet(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5:])
    elif sys.argv[1] == "doubles":        # doubles <before> <after> <out> case...
        doubles(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5:])
    elif sys.argv[1] == "ally":           # ally <before> <after> <out> [--tag v1|before] [--title T] [--legend L] case...
        a = sys.argv[5:]
        kw = {}
        for opt, key in (("--tag", "before_tag"), ("--title", "title"), ("--legend", "legend")):
            if opt in a:
                k = a.index(opt); kw[key] = a[k + 1]; del a[k:k + 2]
        ally(sys.argv[2], sys.argv[3], sys.argv[4], a, **kw)
    else:
        gif(sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5]) if len(sys.argv) > 5 else 66,
            int(sys.argv[6]) if len(sys.argv) > 6 else None)
