#!/usr/bin/env python3
"""Labelled real-engine transition captures: half-speed GIFs and an aligned keyframe strip.

Frame dumps come from run_backdrop_stills.sh (BD_TRANSITIONS / BD_MOVES dump every 2nd engine frame, 33 ms).

  gif:  python3 -I make_ab_gif.py gif <dumps> <out.gif> --t0 N --from A --to B --title "..." --tag BEFORE
                                      [--phases "0:impact;0.2:front;..."] [--ms 66]
  keys: python3 -I make_ab_gif.py keys <out.png> --times "-0.1,0.1,0.3" --row "LABEL|<dumps>|t0" [--row ...]

--t0 is the dump index where the field change starts (t = 0); every frame is captioned with its time from t0
and, with --phases, the phase it is in. Frames are never retouched: the caption is a bar below the frame.
"""
import sys, os
from PIL import Image, ImageDraw, ImageFont

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
ENGINE = ("REAL ENGINE CAPTURE - mkxp-z 2.4.2 (Linux, Xvfb + Mesa llvmpipe) - Essentials v21.1 + Elite Battle: DX "
          "+ Prismfall plugins - every 2nd engine frame")
DUMP_S = 2 / 60.0


def font(name, size):
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    except OSError:
        return ImageFont.load_default()


F_S, F_B, F_TAG = font("DejaVuSans.ttf", 10), font("DejaVuSans-Bold.ttf", 12), font("DejaVuSans-Bold.ttf", 15)


def arg(args, k, default=None):
    return args[args.index(k) + 1] if k in args else default


def frames(d):
    return [os.path.join(d, f) for f in sorted(os.listdir(d)) if f.endswith((".bmp", ".png"))]


def phase_of(phases, t):
    cur = ""
    for start, name in phases:
        if t >= start:
            cur = name
    return cur


def wrap(text, fnt, width):
    d = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) > width and cur:
            lines.append(cur)
            cur = w
        else:
            cur = t
    if cur:
        lines.append(cur)
    return lines


def caption(im, tag, title, t, phase, speed, bar=None):
    """Frame + caption bar below it (tag, title, time and phase, engine line); returns (image, bar height)."""
    w, h = im.size
    tl = wrap(title, F_B, w - 100)
    pl = wrap("t = %+.2f s%s" % (t, ("  |  " + phase) if phase else ""), F_B, w - 12)
    el = wrap(ENGINE + " - " + speed, F_S, w - 12)
    need = 6 + max(22, 16 * len(tl)) + 4 + 16 * len(pl) + 2 + 12 * len(el) + 4
    bar = max(bar or 0, need)
    out = Image.new("RGB", (w, h + bar), (16, 18, 24))
    out.paste(im, (0, 0))
    d = ImageDraw.Draw(out)
    col = (255, 120, 110) if tag.upper().startswith("BEFORE") else (120, 240, 170)
    d.rectangle([0, h, 86, h + 24], fill=(40, 30, 34) if col[0] > 200 else (24, 44, 34))
    d.text((6, h + 4), tag, font=F_TAG, fill=col)
    for i, line in enumerate(tl):
        d.text((94, h + 5 + 16 * i), line, font=F_B, fill=(255, 210, 110))
    y = h + 6 + max(22, 16 * len(tl)) + 4
    for line in pl:
        d.text((6, y), line, font=F_B, fill=(235, 235, 235)); y += 16
    y += 2
    for line in el:
        d.text((6, y), line, font=F_S, fill=(150, 156, 170)); y += 12
    return out, need


def make_gif(args):
    src, out = args[1], args[2]
    t0, a, b = int(arg(args, "--t0")), int(arg(args, "--from")), int(arg(args, "--to"))
    title, tag = arg(args, "--title", ""), arg(args, "--tag", "")
    ms = int(arg(args, "--ms", 66))
    phases = []
    for p in (arg(args, "--phases", "") or "").split(";"):
        if ":" in p:
            s, n = p.split(":", 1)
            phases.append((float(s), n))
    fs = frames(src)[a:b + 1]
    speed = "half speed" if ms == 66 else "%d ms per frame" % ms
    bar = 0
    for i in range(len(fs)):                       # one bar height for every frame (the longest caption)
        t = (a + i - t0) * DUMP_S
        bar = max(bar, caption(Image.new("RGB", (512, 4)), tag, title, t, phase_of(phases, t), speed)[1])
    caps = []
    for i, f in enumerate(fs):
        t = (a + i - t0) * DUMP_S
        caps.append(caption(Image.open(f).convert("RGB"), tag, title, t, phase_of(phases, t), speed, bar)[0])
    q = [c.quantize(192, dither=Image.NONE) for c in caps]
    q[0].save(out, save_all=True, append_images=q[1:], duration=ms, loop=0, optimize=False)
    print(out, len(q), "frames", os.path.getsize(out) // 1024, "KB")


def make_keys(args):
    out = args[1]
    times = [float(x) for x in arg(args, "--times").split(",")]
    rows = [args[i + 1].split("|") for i, k in enumerate(args) if k == "--row"]
    title = arg(args, "--title", "")
    tw, th = 256, 192
    head, lab = 30, 150
    sheet = Image.new("RGB", (lab + tw * len(times), head + 16 + len(rows) * (th + 6) + 16), (16, 18, 24))
    d = ImageDraw.Draw(sheet)
    d.text((6, 6), title, font=F_B, fill=(255, 210, 110))
    for j, t in enumerate(times):
        d.text((lab + j * tw + 4, head), "t = %+.2f s" % t, font=F_B, fill=(235, 235, 235))
    for r, (label, src, t0) in enumerate(rows):
        fs = frames(src)
        y = head + 16 + r * (th + 6)
        lines = label.split("\\n")
        col = (255, 120, 110) if lines[0].upper().startswith("BEFORE") else (120, 240, 170)
        for li, line in enumerate(lines):
            d.text((6, y + 6 + li * 16), line, font=F_B if li == 0 else F_S, fill=col if li == 0 else (200, 204, 214))
        for j, t in enumerate(times):
            i = int(round(int(t0) + t / DUMP_S))
            i = max(0, min(i, len(fs) - 1))
            sheet.paste(Image.open(fs[i]).convert("RGB").resize((tw, th), Image.LANCZOS), (lab + j * tw, y))
    d.text((6, sheet.height - 14), ENGINE, font=F_S, fill=(150, 156, 170))
    sheet.save(out)
    print(out, sheet.size)


if __name__ == "__main__":
    {"gif": make_gif, "keys": make_keys}[sys.argv[1]](sys.argv[1:])
