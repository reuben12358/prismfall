#!/usr/bin/env python3
"""Assembles REAL engine frames (Graphics.screenshot BMPs from the dev-only
ZZ Demo Autorun plugin) into an animated GIF plus captioned key-frame PNGs.

The battle frames are never redrawn or retouched. A caption strip is added
BELOW each frame saying what the footage is.

  python3 -I make_gif.py FRAMES_DIR OUT_PREFIX --title "..." [--ranges 40-560,1330-1480] [--step 2]
                         [--colors 128] [--key IDX:"caption"] ...
Segments of a --ranges list are joined with a short black "time skip" card.
"""
import argparse
import glob
import os

from PIL import Image, ImageDraw, ImageFont

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
CAPTION = ("REAL ENGINE CAPTURE - mkxp-z 2.4.2 (built from source, Linux, Xvfb + Mesa llvmpipe) - "
           "Essentials v21.1 + Elite Battle: DX + Prismfall plugins - AI vs AI - audio off")


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


def captioned(frame, title, note=None, caption=None):
    w, h = frame.size
    tmp = ImageDraw.Draw(frame)
    cap_lines = wrap(caption or CAPTION, F_SMALL, w - 12, tmp)
    title_lines = wrap(title, F_TITLE, w - 12, tmp)
    note_lines = wrap(note, F_TITLE, w - 12, tmp) if note else []
    bar = 8 + 16 * len(title_lines) + 13 * len(cap_lines) + 16 * len(note_lines) + 4
    out = Image.new("RGB", (w, h + bar), (16, 18, 24))
    out.paste(frame, (0, 0))
    d = ImageDraw.Draw(out)
    y = h + 5
    for line in title_lines:
        d.text((6, y), line, font=F_TITLE, fill=(255, 200, 90))
        y += 16
    for line in note_lines:
        d.text((6, y), line, font=F_TITLE, fill=(130, 215, 255))
        y += 16
    for line in cap_lines:
        d.text((6, y), line, font=F_SMALL, fill=(150, 158, 175))
        y += 13
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("frames")
    ap.add_argument("out_prefix")
    ap.add_argument("--title", required=True)
    ap.add_argument("--ranges", default=None, help="comma list of START-END engine frame ranges")
    ap.add_argument("--step", type=int, default=2)
    ap.add_argument("--colors", type=int, default=128)
    ap.add_argument("--ms", type=int, default=100, help="ms per GIF frame (step 2 at 100 ms = real time)")
    ap.add_argument("--key", action="append", default=[], help='IDX:caption')
    ap.add_argument("--caption", default=None, help="replaces the engine caption line (e.g. scripted moves, not AI vs AI)")
    a = ap.parse_args()

    files = sorted(glob.glob(os.path.join(a.frames, "f*.bmp")))
    ranges = [(0, len(files))]
    if a.ranges:
        ranges = [tuple(int(x) for x in r.split("-")) for r in a.ranges.split(",")]
    frames, durations = [], []
    for n, (st, en) in enumerate(ranges):
        if n > 0:   # a visible time-skip card between segments (never mistaken for footage)
            card = Image.new("RGB", frames[-1].size, (0, 0, 0))
            d = ImageDraw.Draw(card)
            d.text((12, 180), "... time skip: engine frames %d-%d omitted ..." % (ranges[n - 1][1], st),
                   font=F_TITLE, fill=(200, 200, 200))
            frames.append(card)
            durations.append(900)
        for f in files[st:min(en, len(files)):a.step]:
            frames.append(captioned(Image.open(f).convert("RGB"), a.title, caption=a.caption))
            durations.append(a.ms)
    # One shared palette (built from a sample of the frames) keeps colours stable between frames,
    # so the GIF encoder only stores the changed region of each frame.
    sample = frames[::max(1, len(frames) // 24)]
    w, h = sample[0].size
    montage = Image.new("RGB", (w, h * len(sample)))
    for i, f in enumerate(sample):
        montage.paste(f, (0, i * h))
    palimg = montage.quantize(colors=a.colors, method=Image.Quantize.MEDIANCUT)
    pal = [f.quantize(palette=palimg, dither=Image.Dither.NONE) for f in frames]
    gif = a.out_prefix + ".gif"
    pal[0].save(gif, save_all=True, append_images=pal[1:], duration=durations, loop=0, optimize=True)
    print("wrote %s: %d frames (engine ranges %s, step %d, %d colours), %.1f MB"
          % (gif, len(pal), ranges, a.step, a.colors, os.path.getsize(gif) / 1e6))
    for k in a.key:
        idx, note = k.split(":", 1)
        idx = int(idx)
        png = "%s_key_f%05d.png" % (a.out_prefix, idx)
        captioned(Image.open(files[idx]).convert("RGB"), a.title + "  (engine frame %d)" % idx, note, a.caption).save(png)
        print("wrote", png)


if __name__ == "__main__":
    main()
