#!/usr/bin/env python3
"""Real-engine playtest media: key shots + a short GIF into docs/playtest/.

The engine frames (Graphics.screenshot PNGs from the dev-only ZZ Playtest Bot) are never retouched: a caption
strip is added BELOW each frame, and the GIF joins trimmed segments with black "time skip" cards.

  python3 -I make_playtest_media.py RUN_OUT_DIR DOCS_DIR --shot FILE:"caption" ... --gif START-END[,START-END] [--step 2]
FILE is a name in RUN_OUT_DIR/shots/ or RUN_OUT_DIR/frames/; START-END are indices of frames/fNNNNNN.png.
"""
import argparse
import os
import re

from PIL import Image, ImageDraw, ImageFont

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
CAPTION = ("REAL ENGINE CAPTURE - mkxp-z 2.4.2 (Linux, Xvfb + Mesa llvmpipe) - Essentials v21.1 + EBDX Renovation "
           "+ Prismfall Dev Kit as packaged - scripted playtest bot (real input), AI battles - audio off")


def font(name, size):
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    except OSError:
        return ImageFont.load_default()


F_SMALL = font("DejaVuSans.ttf", 10)
F_TITLE = font("DejaVuSans-Bold.ttf", 12)


def wrap(text, fnt, width, draw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) > width and cur:
            lines.append(cur)
            cur = w
        else:
            cur = t
    if cur:
        lines.append(cur)
    return lines


def captioned(frame, title, small=True):
    w, h = frame.size
    tmp = ImageDraw.Draw(frame)
    title_lines = wrap(title, F_TITLE, w - 12, tmp)
    cap_lines = wrap(CAPTION, F_SMALL, w - 12, tmp) if small else []
    bar = 8 + 16 * len(title_lines) + 13 * len(cap_lines) + 2
    out = Image.new("RGB", (w, h + bar), (16, 18, 24))
    out.paste(frame, (0, 0))
    d = ImageDraw.Draw(out)
    y = h + 5
    for line in title_lines:
        d.text((6, y), line, font=F_TITLE, fill=(255, 200, 90))
        y += 16
    for line in cap_lines:
        d.text((6, y), line, font=F_SMALL, fill=(150, 158, 175))
        y += 13
    return out


def find(run, name):
    for sub in ("shots", "frames"):
        p = os.path.join(run, sub, name)
        if os.path.exists(p):
            return p
    raise SystemExit("not found: " + name)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run")
    ap.add_argument("docs")
    ap.add_argument("--shot", action="append", default=[], help='FILE:caption')
    ap.add_argument("--gif", default=None, help="START-END[,START-END...] frame index ranges")
    ap.add_argument("--labels", default=None, help="one label per --gif range, separated by |")
    ap.add_argument("--step", type=int, default=2)
    ap.add_argument("--ms", type=int, default=200, help="ms per GIF frame (frames are every 6th engine frame)")
    ap.add_argument("--colors", type=int, default=128)
    ap.add_argument("--name", default="first_minutes")
    ap.add_argument("--first", type=int, default=1, help="number of the first key shot")
    a = ap.parse_args()
    os.makedirs(a.docs, exist_ok=True)
    for n, spec in enumerate(a.shot, a.first):
        name, cap = spec.split(":", 1)
        slug = re.sub(r"[^a-z0-9_]", "", cap.split(":")[0].lower().replace(" ", "_"))[:40]
        out = os.path.join(a.docs, "%02d_%s.png" % (n, slug))
        captioned(Image.open(find(a.run, name)).convert("RGB"), cap).save(out)
        print("wrote", out)
    if not a.gif:
        return
    ranges = [tuple(int(x) for x in r.split("-")) for r in a.gif.split(",")]
    labels = a.labels.split("|") if a.labels else [""] * len(ranges)
    frames, durations = [], []
    for n, (st, en) in enumerate(ranges):
        if n > 0:   # a visible time-skip card between segments (never mistaken for footage)
            card = Image.new("RGB", frames[-1].size, (0, 0, 0))
            d = ImageDraw.Draw(card)
            d.text((12, 170), "... time skip ...", font=F_TITLE, fill=(200, 200, 200))
            d.text((12, 192), labels[n], font=F_TITLE, fill=(255, 200, 90))
            frames.append(card)
            durations.append(1100)
        for i in range(st, en + 1, a.step):
            p = os.path.join(a.run, "frames", "f%06d.png" % i)
            if os.path.exists(p):
                frames.append(captioned(Image.open(p).convert("RGB"), labels[n], small=False))
                durations.append(a.ms)
    sample = frames[::max(1, len(frames) // 24)]
    w, h = sample[0].size
    montage = Image.new("RGB", (w, h * len(sample)))
    for i, f in enumerate(sample):
        montage.paste(f.resize((w, h)), (0, i * h))
    palimg = montage.quantize(colors=a.colors, method=Image.Quantize.MEDIANCUT)
    pal = [f.resize((w, h)).quantize(palette=palimg, dither=Image.Dither.NONE) for f in frames]
    gif = os.path.join(a.docs, a.name + ".gif")
    pal[0].save(gif, save_all=True, append_images=pal[1:], duration=durations, loop=0, optimize=True)
    print("wrote %s: %d frames, %.1f MB" % (gif, len(pal), os.path.getsize(gif) / 1e6))


if __name__ == "__main__":
    main()
