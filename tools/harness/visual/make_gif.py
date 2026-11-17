#!/usr/bin/env python3
"""Assembles REAL engine frames (Graphics.screenshot BMPs from the dev-only
ZZ Demo Autorun plugin) into an animated GIF plus captioned key-frame PNGs.

The battle frames are never redrawn or retouched. A caption strip is added
BELOW each frame saying what the footage is.

  python3 -I make_gif.py FRAMES_DIR OUT_PREFIX --title "..." [--start N] [--end N] [--step 2]
                         [--key IDX:"caption"] ...
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


def captioned(frame, title, note=None):
    w, h = frame.size
    tmp = ImageDraw.Draw(frame)
    cap_lines = wrap(CAPTION, F_SMALL, w - 12, tmp)
    note_lines = wrap(note, F_TITLE, w - 12, tmp) if note else []
    bar = 8 + 16 + 13 * len(cap_lines) + 16 * len(note_lines) + 4
    out = Image.new("RGB", (w, h + bar), (16, 18, 24))
    out.paste(frame, (0, 0))
    d = ImageDraw.Draw(out)
    y = h + 5
    d.text((6, y), title, font=F_TITLE, fill=(255, 200, 90))
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
    ap.add_argument("--start", type=int, default=0)
    ap.add_argument("--end", type=int, default=None)
    ap.add_argument("--step", type=int, default=2)
    ap.add_argument("--ms", type=int, default=100, help="ms per GIF frame (step 2 at 100 ms = real time)")
    ap.add_argument("--key", action="append", default=[], help='IDX:caption')
    a = ap.parse_args()

    files = sorted(glob.glob(os.path.join(a.frames, "f*.bmp")))
    end = a.end if a.end is not None else len(files)
    picked = files[a.start:end:a.step]
    frames = [captioned(Image.open(f).convert("RGB"), a.title) for f in picked]
    pal = [f.quantize(colors=255, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE) for f in frames]
    gif = a.out_prefix + ".gif"
    pal[0].save(gif, save_all=True, append_images=pal[1:], duration=a.ms, loop=0, optimize=True, disposal=1)
    print("wrote %s: %d frames (engine frames %d..%d step %d), %.1f MB"
          % (gif, len(pal), a.start, end - 1, a.step, os.path.getsize(gif) / 1e6))
    for k in a.key:
        idx, note = k.split(":", 1)
        idx = int(idx)
        png = "%s_key_f%05d.png" % (a.out_prefix, idx)
        captioned(Image.open(files[idx]).convert("RGB"), a.title + "  (engine frame %d)" % idx, note).save(png)
        print("wrote", png)


if __name__ == "__main__":
    main()
