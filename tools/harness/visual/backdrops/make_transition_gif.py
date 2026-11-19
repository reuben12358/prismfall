#!/usr/bin/env python3
"""Half-speed GIF + key-frame strip from a transition recording (every 2nd engine frame, BMP).
   python3 -I make_transition_gif.py <frames_dir> <out_base> [frame_ms=66]"""
import sys, os
from PIL import Image
src, out = sys.argv[1], sys.argv[2]
ms = int(sys.argv[3]) if len(sys.argv) > 3 else 66        # captured at 33 ms -> played at half speed
files = sorted(f for f in os.listdir(src) if f.endswith((".bmp", ".png")))
frames = [Image.open(os.path.join(src, f)).convert("RGB") for f in files]
pal = frames[len(frames) // 2].quantize(160)
q = [f.quantize(palette=frames[i].quantize(160), dither=Image.NONE) if False else f.quantize(160, dither=Image.NONE) for i, f in enumerate(frames)]
q[0].save(out + ".gif", save_all=True, append_images=q[1:], duration=ms, loop=0, optimize=False)
n = 8
strip = Image.new("RGB", (512 * 4, 384 * 2))
for k in range(n):
    f = frames[int(k * (len(frames) - 1) / (n - 1))]
    strip.paste(f, ((k % 4) * 512, (k // 4) * 384))
strip.save(out + "_keys.png")
print(out + ".gif", len(frames), "frames", os.path.getsize(out + ".gif") // 1024, "KB")
