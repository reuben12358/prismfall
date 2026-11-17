#!/usr/bin/env python3
"""Assembles a SLOW-PACED real-engine capture (DEMO_SLOW=1) into
  <out>.mp4  - the whole battle at real time (30 fps, 2x nearest-neighbour), H.264
  <out>.gif  - the key stretch at real time, under a size budget
  <out>_key_*.png - full-colour key frames found by message text
each starting with a title card saying what to watch for.

Frames are never redrawn: a caption strip is added below each one. In the GIF, frames
are dropped only while a message is fully shown and the screen is near-static (the
remaining frame keeps the summed duration, so every hold time is preserved). Typing
frames are all kept; move animations run at 15 fps in the GIF and 30 fps in the MP4.

  python3 -I make_slow.py SPEC.json
SPEC: {"frames": dir, "out": prefix, "title": str, "watch": [str], "gif_from": regex,
       "gif_to": regex, "gif_after": seconds, "keys": [[regex, "caption", "first|last|flash"]]}
"""
import json
import os
import re
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

FPS = 30
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
CAPTION = ("REAL ENGINE CAPTURE - mkxp-z 2.4.2 + Essentials v21.1 + Elite Battle: DX + Prismfall plugins - "
           "AI vs AI - paced in-engine for reading (slow text, 2.5-3.5 s message holds, 1 s before each turn) - audio off")


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_SMALL, F_BOLD = font("DejaVuSans.ttf", 10), font("DejaVuSans-Bold.ttf", 12)
F_CARD_T, F_CARD, F_CARD_S = font("DejaVuSans-Bold.ttf", 21), font("DejaVuSans.ttf", 14), font("DejaVuSans.ttf", 11)


def wrap(text, fnt, width):
    d = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    out, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) > width and cur:
            out.append(cur)
            cur = w
        else:
            cur = t
    return out + ([cur] if cur else [])


class Captioner:
    def __init__(self, title, width=512):
        self.title_lines = wrap(title, F_BOLD, width - 12)
        self.cap_lines = wrap(CAPTION, F_SMALL, width - 12)
        h = 6 + 16 * len(self.title_lines) + 13 * len(self.cap_lines) + 4
        self.bar_h = h + (h % 2)

    def __call__(self, frame, note=None):
        w, h = frame.size
        note_lines = wrap(note, F_BOLD, w - 12) if note else []
        bar = self.bar_h + 16 * len(note_lines)
        out = Image.new("RGB", (w, h + bar), (16, 18, 24))
        out.paste(frame, (0, 0))
        d = ImageDraw.Draw(out)
        y = h + 4
        for line in self.title_lines:
            d.text((6, y), line, font=F_BOLD, fill=(255, 200, 90))
            y += 16
        for line in note_lines:
            d.text((6, y), line, font=F_BOLD, fill=(130, 215, 255))
            y += 16
        for line in self.cap_lines:
            d.text((6, y), line, font=F_SMALL, fill=(150, 158, 175))
            y += 13
        return out


def title_card(size, title, watch):
    w, h = size
    img = Image.new("RGB", size, (14, 16, 22))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w, 26], fill=(74, 52, 12))
    d.text((12, 6), "REAL ENGINE CAPTURE  -  title card (not game footage)", font=F_BOLD, fill=(255, 200, 90))
    y = 44
    for line in wrap(title, F_CARD_T, w - 24):
        d.text((12, y), line, font=F_CARD_T, fill=(235, 238, 245))
        y += 27
    y += 10
    d.text((12, y), "What to watch for:", font=F_BOLD, fill=(140, 226, 150))
    y += 22
    for item in watch:
        lines = wrap(item, F_CARD, w - 44)
        for i, line in enumerate(lines):
            d.text((14 if i == 0 else 30, y), ("- " if i == 0 else "") + line, font=F_CARD, fill=(215, 220, 230))
            y += 19
        y += 4
    y = h - 46
    for line in wrap("mkxp-z 2.4.2 built from source (Linux, Xvfb, Mesa llvmpipe), Essentials v21.1 + Elite Battle: DX "
                     "+ Prismfall plugins. AI plays both sides. Real-time playback; text paced in-engine for reading.",
                     F_CARD_S, w - 24):
        d.text((12, y), line, font=F_CARD_S, fill=(150, 158, 175))
        y += 14
    return img


def load_rows(frames_dir):
    rows = []
    with open(os.path.join(frames_dir, "frames.tsv"), encoding="utf-8") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            parts += [""] * (5 - len(parts))
            rows.append({"i": int(parts[0]), "state": parts[2], "cls": parts[3], "text": parts[4]})
    return rows


def frame_path(frames_dir, i):
    return os.path.join(frames_dir, "f%05d.png" % i)


def find(rows, regex, which="last", start=0, nth=1):
    """First/last frame of the nth run of frames showing a message that matches regex."""
    rx = re.compile(regex)
    hits = [k for k in range(start, len(rows)) if rows[k]["state"] == "shown" and rx.search(rows[k]["text"])]
    runs = [k for n, k in enumerate(hits) if n == 0 or hits[n - 1] != k - 1]
    if len(runs) < nth:
        return None
    hits = [k for k in hits if k >= runs[nth - 1]]
    if which == "first":
        return hits[0]
    # last frame of the FIRST run of matching frames
    k = hits[0]
    while k + 1 < len(rows) and rows[k + 1]["state"] == "shown" and rx.search(rows[k + 1]["text"]):
        k += 1
    return k


def write_mp4(spec, rows, cap, card):
    out = spec["out"] + ".mp4"
    first = Image.open(frame_path(spec["frames"], 0)).convert("RGB")
    w, h = cap(first).size
    W, H = w * 2, h * 2
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "%dx%d" % (W, H),
           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
           "-pix_fmt", "yuv420p", "-movflags", "+faststart", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    card_img = card.resize((W, H), Image.NEAREST).tobytes()
    for _ in range(int(spec.get("card_seconds", 6) * FPS)):
        p.stdin.write(card_img)
    for r in rows:
        im = cap(Image.open(frame_path(spec["frames"], r["i"])).convert("RGB"))
        p.stdin.write(im.resize((W, H), Image.NEAREST).tobytes())
    p.stdin.close()
    p.wait()
    secs = len(rows) / FPS
    print("wrote %s: %d engine frames = %.1f s of battle (+%ds title card), %dx%d, %.1f MB"
          % (out, len(rows), secs, spec.get("card_seconds", 6), W, H, os.path.getsize(out) / 1e6))


def gif_frames(spec, rows, a, b):
    """Frame selection with duration accounting. Returns [(row_index, duration_ms)]."""
    sel = []
    prev_arr, last_kept_arr = None, None
    pending_ms = 0.0
    step_ms = 1000.0 / FPS
    for k in range(a, b + 1):
        r = rows[k]
        arr = np.asarray(Image.open(frame_path(spec["frames"], r["i"])).convert("L"), dtype=np.int16)
        keep = True
        if sel and r["state"] == "shown" and rows[sel[-1][0]]["text"] == r["text"] and last_kept_arr is not None:
            changed = float((np.abs(arr - last_kept_arr) > 24).mean())
            static = changed < 0.03                                   # only particles moving
            if static and sel[-1][1] + pending_ms < 500:
                keep = False                                          # merge into the kept frame
            elif not static and r["state"] == "shown" and (k - a) % 2 == 1:
                keep = False                                          # animation under a shown message: 15 fps
        elif r["state"] == "none" and (k - a) % 2 == 1:
            keep = False                                              # animation with no text: 15 fps
        if keep:
            sel.append([k, step_ms])
            last_kept_arr = arr
        else:
            sel[-1][1] += step_ms
        prev_arr = arr
    return sel


def write_gif(spec, rows, cap, card):
    if spec.get("gif_watch"):
        card = title_card(card.size, spec["title"] + " - key stretch",
                          spec["gif_watch"] + ["The MP4 next to this GIF has the whole battle at the same pace."])
    a = find(rows, spec["gif_from"], "first", nth=spec.get("gif_from_nth", 1))
    b = find(rows, spec["gif_to"], "last", start=a or 0)
    if a is None or b is None:
        raise SystemExit("gif markers not found: %r %r" % (spec["gif_from"], spec["gif_to"]))
    a = max(0, a - int(spec.get("gif_before", 1.0) * FPS))
    b = min(len(rows) - 1, b + int(spec.get("gif_after", 1.5) * FPS))
    sel = gif_frames(spec, rows, a, b)
    imgs = [card] + [cap(Image.open(frame_path(spec["frames"], rows[k]["i"])).convert("RGB")) for k, _ in sel]
    durs = [spec.get("card_seconds", 6) * 1000.0] + [d for _, d in sel]
    # GIF delays are in 10 ms units: round with error carry so total time stays exact
    out_d, carry = [], 0.0
    for d in durs:
        t = d + carry
        q = max(20, int(round(t / 10.0)) * 10)
        carry = t - q
        out_d.append(q)
    sample = imgs[1::max(1, len(imgs) // 24)]
    w, h = imgs[1].size
    mont = Image.new("RGB", (w, h * len(sample)))
    for n, im in enumerate(sample):
        mont.paste(im, (0, n * h))
    mont.paste(card.resize((w, h)), (0, 0))
    pal = mont.quantize(colors=spec.get("colors", 128), method=Image.Quantize.MEDIANCUT)
    q = [im.quantize(palette=pal, dither=Image.Dither.NONE) for im in imgs]
    out = spec["out"] + ".gif"
    q[0].save(out, save_all=True, append_images=q[1:], duration=out_d, loop=0, optimize=True)
    total = sum(out_d) / 1000.0
    print("wrote %s: %d GIF frames covering engine frames %d-%d (%.1f s of battle + card), %.1f MB"
          % (out, len(q), rows[a]["i"], rows[b]["i"], total - spec.get("card_seconds", 6), os.path.getsize(out) / 1e6))


def write_keys(spec, rows, cap):
    for regex, note, which in spec.get("keys", []):
        if which == "flash":
            # brightest-changing frame shortly before the message starts (the Bridge's transition flash)
            k = find(rows, regex, "first")
            if k is None:
                print("key not found:", regex)
                continue
            best, bestv = k, -1
            for j in range(max(0, k - 4 * FPS), k):
                v = float(np.asarray(Image.open(frame_path(spec["frames"], rows[j]["i"])).convert("L")).mean())
                if v > bestv:
                    best, bestv = j, v
            k = best
        else:
            k = find(rows, regex, which)
            if k is None:
                print("key not found:", regex)
                continue
        i = rows[k]["i"]
        im = cap(Image.open(frame_path(spec["frames"], i)).convert("RGB"), note)
        path = "%s_key_f%05d.png" % (spec["out"], i)
        im.save(path)
        print("wrote", path)


def main():
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    rows = load_rows(spec["frames"])
    rows = [r for r in rows if os.path.exists(frame_path(spec["frames"], r["i"]))]
    cap = Captioner(spec["title"])
    w, h = cap(Image.open(frame_path(spec["frames"], 0)).convert("RGB")).size
    card = title_card((w, h), spec["title"], spec["watch"])
    os.makedirs(os.path.dirname(spec["out"]) or ".", exist_ok=True)
    card.save(spec["out"] + "_title_card.png")
    if "only" not in spec or "keys" in spec["only"]:
        write_keys(spec, rows, cap)
    if "only" not in spec or "gif" in spec["only"]:
        write_gif(spec, rows, cap, card)
    if "only" not in spec or "mp4" in spec["only"]:
        write_mp4(spec, rows, cap, card)


if __name__ == "__main__":
    main()
