#!/usr/bin/env python3
"""charsets.py - small event charsets the map layouts need (map builder 12), written to graphics/Characters/.

  pf_rime_curtain.png   a curtain of frozen silk (Rimewood Path 578): hanging rime-glazed strands with a cold sheen.
                        Rows follow Essentials' pbSmashEvent (down, left, right, up = whole, cracked, shattering, shards),
                        so the Rock Smash animation plays through them.

    python3 -I mapgen/charsets.py"""
import os, random
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), 'graphics', 'Characters')
FW, FH = 32, 48

ICE = [(70, 96, 128), (112, 146, 180), (160, 196, 222), (206, 228, 242), (244, 250, 255)]
SILK = [(150, 160, 178), (196, 204, 220), (232, 236, 246)]


def curtain_frame(stage, seed=3):
    """stage 0 whole, 1 cracked, 2 shattering, 3 shards on the ground"""
    rng = random.Random(seed)
    im = Image.new('RGBA', (FW, FH), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    top = 6
    if stage < 3:
        # the branch the curtain hangs from
        d.rectangle([2, top - 3, FW - 3, top - 1], fill=(92, 84, 96, 255))
        d.line([2, top - 3, FW - 3, top - 3], fill=(150, 160, 178, 255))
        for x in range(3, FW - 3, 2):                    # rime on the branch
            if rng.random() < 0.7: d.point((x, top - 4), fill=ICE[4] + (255,))
        # strands: each hangs to its own length, glazed (ice core, silk edge), thicker drips at the ends
        for i, x in enumerate(range(3, FW - 3)):
            ln = 34 + int(6 * ((i * 7) % 5) / 4.0) + rng.randint(-2, 2)
            if stage == 2: ln = int(ln * (0.35 + 0.4 * rng.random()))
            for y in range(top, top + ln):
                t = (y - top) / float(ln)
                c = ICE[2] if (x % 3) else SILK[1]
                if (x + y // 5) % 7 == 0: c = ICE[4]
                if t > 0.85: c = ICE[3]
                if x % 4 == 0: c = ICE[1] if t < 0.85 else ICE[2]
                a = 235 if x % 4 else 200
                im.putpixel((x, y), c + (a,))
            im.putpixel((x, top + ln - 1), ICE[4] + (255,))
        # cold sheen: a diagonal light streak and a dark fold
        for k in range(22):
            x, y = 8 + k // 2, top + 4 + k
            if 0 <= x < FW and y < FH and im.getpixel((x, y))[3]: im.putpixel((x, y), ICE[4] + (255,))
        for y in range(top + 2, top + 30):
            x = 22
            if im.getpixel((x, y))[3]: im.putpixel((x, y), ICE[0] + (230,))
        if stage >= 1:                                  # cracks
            pts = [(16, top + 4), (13, top + 12), (18, top + 19), (14, top + 27), (19, top + 33)]
            d.line(pts, fill=(40, 60, 90, 255), width=1)
            d.line([(18, top + 19), (24, top + 23)], fill=(40, 60, 90, 255))
            d.line([(13, top + 12), (7, top + 15)], fill=(40, 60, 90, 255))
    # shards and rime at the foot
    n = (3, 4, 9, 14)[stage]
    for _ in range(n):
        x = rng.randint(3, FW - 6); y = rng.randint(FH - 8, FH - 3)
        w = rng.randint(2, 4)
        d.polygon([(x, y), (x + w, y - rng.randint(1, 3)), (x + w + 1, y)], fill=ICE[rng.randint(2, 4)] + (255,))
    if stage == 3:
        d.line([(4, FH - 3), (FW - 5, FH - 3)], fill=ICE[3] + (200,))
    return im


def rime_curtain():
    sheet = Image.new('RGBA', (FW * 4, FH * 4), (0, 0, 0, 0))
    for row in range(4):
        for col in range(4):
            sheet.paste(curtain_frame(row, seed=3 + col * 0), (col * FW, row * FH))
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, 'pf_rime_curtain.png'); sheet.save(p); print('wrote', p)


if __name__ == '__main__':
    rime_curtain()
