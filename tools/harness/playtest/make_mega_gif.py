#!/usr/bin/env python3
"""Slow GIF of a real-engine Mega Evolution (run_mega.sh gif).

Reads RUN_OUT/bot.log for the bot's "MG: frames MegaEvolution... at rec frame N" marks and joins the recorded frames
(RUN_OUT/frames/fNNNNNN.png, every 2nd engine frame) from a little before the first Mega Evolution animation to a little
after its "has Mega Evolved" message, at 2.4x slow motion. Frames are never redrawn: a caption strip is added below.
Also copies the key shots (Fight menu, Mega button on, animation, after) next to the GIF.

  python3 -I make_mega_gif.py RUN_OUT_DIR OUT_DIR [--before 16] [--after 40] [--ms 80]
"""
import argparse
import os
import re
import shutil

from PIL import Image, ImageDraw, ImageFont

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
CAPTION = ("REAL ENGINE CAPTURE - mkxp-z 2.4.2 (Linux, Xvfb) - Essentials v21.1 + EBDX Renovation + Prismfall kit - "
           "the player's own Fight menu (bot input: Action = Mega button, Use = Flamethrower) - 2.4x slow motion - audio off")


def caption_strip(width, text, sub):
    try:
        f1, f2 = ImageFont.truetype(FONT, 11), ImageFont.truetype(FONT, 9)
    except OSError:
        f1 = f2 = ImageFont.load_default()
    img = Image.new("RGB", (width, 34), (16, 16, 24))
    d = ImageDraw.Draw(img)
    d.text((6, 3), text, font=f1, fill=(240, 230, 200))
    d.text((6, 19), sub[:150], font=f2, fill=(150, 150, 170))
    return img


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_out")
    ap.add_argument("out_dir")
    ap.add_argument("--before", type=int, default=16)
    ap.add_argument("--after", type=int, default=40)
    ap.add_argument("--ms", type=int, default=80)
    a = ap.parse_args()
    log = open(os.path.join(a.run_out, "bot.log"), encoding="utf-8", errors="replace").read()
    marks = [(m.group(1), m.group(2), m.group(3), int(m.group(4))) for m in
             re.finditer(r"MG: frames (MegaEvolution2?) (start|end)(?: for (.*?))? at rec frame (\d+)", log)]
    if not marks:
        raise SystemExit("no Mega Evolution marks in bot.log")
    first_start = next(f for n, k, _w, f in marks if n == "MegaEvolution" and k == "start")
    who = next((w for n, k, w, f in marks if n == "MegaEvolution" and k == "start"), "?")
    end2 = next((f for n, k, _w, f in marks if n == "MegaEvolution2" and k == "end" and f >= first_start), first_start + 120)
    lo, hi = max(0, first_start - a.before), end2 + a.after
    frames_dir = os.path.join(a.run_out, "frames")
    files = [os.path.join(frames_dir, "f%06d.png" % i) for i in range(lo, hi + 1)]
    files = [f for f in files if os.path.exists(f)]
    if not files:
        raise SystemExit("no frames in %s for %d-%d" % (frames_dir, lo, hi))
    os.makedirs(a.out_dir, exist_ok=True)
    imgs = []
    for f in files:
        im = Image.open(f).convert("RGB")
        strip = caption_strip(im.width, "Mega Evolution in Elite Battle DX: %s, Volcanic field (Prismfall)" % who, CAPTION)
        canvas = Image.new("RGB", (im.width, im.height + strip.height))
        canvas.paste(im, (0, 0))
        canvas.paste(strip, (0, im.height))
        imgs.append(canvas)
    # One shared palette from a strip of frames across the whole clip (the backdrop, the shatter stone, the Mega form).
    sample = imgs[::max(1, len(imgs) // 16)]
    strip = Image.new("RGB", (sample[0].width, sample[0].height * len(sample)))
    for i, im in enumerate(sample):
        strip.paste(im, (0, i * im.height))
    pal = strip.quantize(colors=255, method=Image.MEDIANCUT)
    q = [im.quantize(palette=pal, dither=Image.NONE) for im in imgs]
    durations = [a.ms] * len(q)
    durations[-1] = 1500
    out = os.path.join(a.out_dir, "mega_evolution_ebdx.gif")
    q[0].save(out, save_all=True, append_images=q[1:], duration=durations, loop=0, optimize=True, disposal=1)
    shots = os.path.join(a.run_out, "shots")
    kept = []
    if os.path.isdir(shots):
        for s in sorted(os.listdir(shots)):
            if re.search(r"mg_0[12]_|mg_anim_MegaEvolution_|mg_after_MegaEvolution2_", s):
                shutil.copy(os.path.join(shots, s), os.path.join(a.out_dir, s))
                kept.append(s)
    print("%s: %d frames (%d-%d), %.1f s at %d ms, %d KB; shots %s" %
          (out, len(q), lo, hi, sum(durations) / 1000.0, a.ms, os.path.getsize(out) // 1024, kept))


if __name__ == "__main__":
    main()
