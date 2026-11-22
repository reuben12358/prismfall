#!/usr/bin/env python3
"""Chapter "key events" reel from REAL engine frames.

Two steps, so the huge BMP dumps can be deleted between capture runs:

  python3 -I make_story_gif.py pick FRAMES_DIR KEEP_DIR --step 4 [--range 0-900]
      copies every STEP-th frame (as PNG) of FRAMES_DIR into KEEP_DIR.

  python3 -I make_story_gif.py reel OUT.gif --title "Chapter 11 - The Thaw" \
      --seg "KEEP_DIR_1|Caption for this part" --seg "KEEP_DIR_2|..." [--ms 90] [--colors 128]
      joins the parts with a title card before each, and a caption strip under every frame.

The frames themselves are never redrawn or retouched.
"""
import argparse
import glob
import os
import shutil

from PIL import Image, ImageDraw, ImageFont

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
STRIP = 40
NOTE = "REAL ENGINE CAPTURE - mkxp-z + Essentials v21.1 + EBDX + Prismfall plugins - AI plays both sides"


def font(name, size):
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    except OSError:
        return ImageFont.load_default()


def pick(args):
    os.makedirs(args.keep, exist_ok=True)
    files = sorted(glob.glob(os.path.join(args.frames, "*.bmp")) + glob.glob(os.path.join(args.frames, "*.png")))
    lo, hi = 0, len(files)
    if args.range:
        lo, hi = (int(x) for x in args.range.split("-"))
    n = 0
    for i, f in enumerate(files[lo:hi]):
        if i % args.step:
            continue
        Image.open(f).convert("RGB").save(os.path.join(args.keep, "k%05d.png" % n))
        n += 1
    print("kept %d of %d frames from %s" % (n, len(files), args.frames))


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def card(size, title, sub):
    w, h = size
    im = Image.new("RGB", (w, h + STRIP), (12, 14, 22))
    d = ImageDraw.Draw(im)
    ft, fs = font("DejaVuSans-Bold.ttf", 26), font("DejaVuSans.ttf", 16)
    y = h // 2 - 40
    for line in wrap(d, title, ft, w - 60):
        d.text(((w - d.textlength(line, font=ft)) / 2, y), line, font=ft, fill=(235, 225, 190))
        y += 34
    y += 10
    for line in wrap(d, sub, fs, w - 80):
        d.text(((w - d.textlength(line, font=fs)) / 2, y), line, font=fs, fill=(170, 180, 200))
        y += 22
    return im


def captioned(im, caption):
    w, h = im.size
    out = Image.new("RGB", (w, h + STRIP), (12, 14, 22))
    out.paste(im, (0, 0))
    d = ImageDraw.Draw(out)
    d.text((8, h + 4), caption, font=font("DejaVuSans-Bold.ttf", 13), fill=(235, 225, 190))
    d.text((8, h + 22), NOTE, font=font("DejaVuSans.ttf", 10), fill=(140, 150, 170))
    return out


def reel(args):
    frames, durs = [], []
    size = None
    segs = [s.split("|", 1) for s in args.seg]
    for i, (keep, cap) in enumerate(segs):
        files = sorted(glob.glob(os.path.join(keep, "*.png")))
        if not files:
            continue
        if size is None:
            size = Image.open(files[0]).size
            frames.append(card(size, args.title, "Key events, captured in the real engine"))
            durs.append(2200)
        frames.append(card(size, "%d. %s" % (i + 1, cap), ""))
        durs.append(1400)
        for f in files[::args.every]:
            frames.append(captioned(Image.open(f).convert("RGB"), cap))
            durs.append(args.ms * args.every)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    pal = [f.quantize(colors=args.colors, method=Image.Quantize.MEDIANCUT) for f in frames]
    pal[0].save(args.out, save_all=True, append_images=pal[1:], duration=durs, loop=0, optimize=True)
    print("wrote %s: %d frames, %.1f MB" % (args.out, len(frames), os.path.getsize(args.out) / 1e6))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("pick")
    p.add_argument("frames"); p.add_argument("keep")
    p.add_argument("--step", type=int, default=4); p.add_argument("--range")
    r = sub.add_parser("reel")
    r.add_argument("out"); r.add_argument("--title", required=True)
    r.add_argument("--seg", action="append", required=True)
    r.add_argument("--ms", type=int, default=90); r.add_argument("--every", type=int, default=1); r.add_argument("--colors", type=int, default=128)
    a = ap.parse_args()
    pick(a) if a.cmd == "pick" else reel(a)


if __name__ == "__main__":
    main()
