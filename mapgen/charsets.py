#!/usr/bin/env python3
"""charsets.py - small event charsets the map layouts need (map builder 12), written to graphics/Characters/.

  pf_rime_curtain.png   a curtain of frozen silk (Rimewood Path 578): hanging rime-glazed strands with a cold sheen.
                        Rows follow Essentials' pbSmashEvent (down, left, right, up = whole, cracked, shattering, shards),
                        so the Rock Smash animation plays through them.

    python3 -I mapgen/charsets.py"""
import os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
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


# ------------------------------------------------------------------ map builder 13: cave event charsets (cdraw palettes)
def _frame_from16(im16, dy=0):
    """a 16x16 logical piece doubled into the bottom of a 32x48 frame"""
    fr = Image.new('RGBA', (FW, FH), (0, 0, 0, 0))
    big = im16.resize((32, 32), Image.NEAREST)
    fr.alpha_composite(big, (0, FH - 32 - dy))
    return fr


def cave_rock(p):
    """Rock Smash rock (rows follow pbSmashEvent: whole, cracked, shattering, rubble)"""
    import cdraw
    pal = cdraw.PAL[p]['rock']
    sheet = Image.new('RGBA', (FW * 4, FH * 4), (0, 0, 0, 0))
    for row in range(4):
        base = cdraw.rock1(p, 0)
        if row >= 1:                                         # a crack runs down the face
            for i in range(9):
                x = 6 + (i % 3 == 1) - (i % 4 == 3); y = 5 + i
                if base.getpixel((x, y))[3]: base.putpixel((x, y), pal[0] + (255,))
                if row >= 2 and base.getpixel((x + 3, y))[3] and i % 2: base.putpixel((x + 3, y), pal[0] + (255,))
        if row == 2:                                         # flying chips
            for (x, y) in ((2, 4), (13, 3), (1, 9), (14, 8)): base.putpixel((x, y), pal[3] + (255,))
        if row == 3:
            base = cdraw.rubble(p, 1)
        for col in range(4):
            sheet.paste(_frame_from16(base), (col * FW, row * FH))
    os.makedirs(OUT, exist_ok=True)
    pth = os.path.join(OUT, 'pf_cave_rock_%s.png' % p); sheet.save(pth); print('wrote', pth)


def cave_boulder(p):
    """Strength boulder: a big rounded block of the cave's rock, the same in every frame"""
    import cdraw
    pal = cdraw.PAL[p]['rock']
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    for y in range(16):
        for x in range(16):
            dx, dy = (x + 0.5 - 8) / 7.2, (y + 0.5 - 8.5) / 6.6
            d = dx * dx + dy * dy
            if d > 1: continue
            if d > 0.8: c = pal[0]
            else:
                l = -(dx + dy * 1.1) * 1.4 + 2.8 + (cdraw.nz(x, y, 11) - 0.5) * 0.5
                c = pal[int(max(1, min(5, round(l))))]
            im.putpixel((x, y), c[:3] + (255,))
    for x in range(4, 9): im.putpixel((x, 6 + (x % 2)), pal[1][:3] + (255,))      # a seam
    sheet = Image.new('RGBA', (FW * 4, FH * 4), (0, 0, 0, 0))
    for row in range(4):
        for col in range(4): sheet.paste(_frame_from16(im), (col * FW, row * FH))
    pth = os.path.join(OUT, 'pf_cave_boulder_%s.png' % p); sheet.save(pth); print('wrote', pth)


def minecart():
    """the Brinecut minecart: rows down / left / right / up, wheels turning across the four frames"""
    import cdraw
    sheet = Image.new('RGBA', (FW * 4, FH * 4), (0, 0, 0, 0))
    for row in range(4):
        for col in range(4):
            im = cdraw.cart(False)
            if row in (1, 2):                                   # side view: longer body, wheel spokes turn
                im = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
                for y in range(5, 12):
                    for x in range(1, 15):
                        c = cdraw.IRON[2] if y == 5 else cdraw.IRON[1] if y < 11 else cdraw.IRON[0]
                        if x in (1, 14): c = cdraw.IRON[0]
                        im.putpixel((x, y), c)
                for wx in (4, 11):
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1): im.putpixel((wx + dx, 13 + dy), cdraw.IRON[0])
                    sx, sy = [(1, 0), (0, 1), (-1, 0), (0, -1)][col]
                    im.putpixel((wx + sx, 13 + sy), cdraw.IRON[3])
            elif col % 2:
                for x in (4, 11): im.putpixel((x, 14), cdraw.IRON[3])
            sheet.paste(_frame_from16(im, dy=2), (col * FW, row * FH))
    pth = os.path.join(OUT, 'pf_minecart.png'); sheet.save(pth); print('wrote', pth)


def armchair():
    """pf_armchair.png: Thistledown's creeping armchair (D5).  Rows down / left / right / up (it turns to face where it
    shuffles); the four frames are a little hop with a ghostly shimmer, for the step it takes when your back is turned"""
    import mdraw
    sheet = Image.new('RGBA', (FW * 4, FW * 4), (0, 0, 0, 0))
    for row, f in enumerate(('down', 'left', 'right', 'up')):
        base = mdraw.armchair(mdraw.VELG, f).resize((32, 32), Image.NEAREST)
        for k in range(4):
            fr = Image.new('RGBA', (FW, FW), (0, 0, 0, 0))
            hop = (0, 2, 0, 1)[k]
            glow = Image.new('RGBA', (FW, FW), (0, 0, 0, 0))
            for y in range(FW):
                for x in range(FW):
                    if (x - 15.5) ** 2 / 200 + (y - 26) ** 2 / 30 < 1: glow.putpixel((x, y), (150, 110, 210, 40 + 20 * (k % 2)))
            fr.alpha_composite(glow)
            fr.alpha_composite(base, (0, -hop))
            if f != 'up':                                    # two pin-prick eyes in the button-back
                for ex in (12, 19):
                    fr.putpixel((ex if f == 'down' else ex + (-3 if f == 'left' else 3), 7 - hop), (220, 200, 255, 230))
            sheet.alpha_composite(fr, (k * FW, row * FW))
    sheet.save(os.path.join(OUT, 'pf_armchair.png'))


if __name__ == '__main__':
    rime_curtain()
    for _p in 'SLE':
        cave_rock(_p); cave_boulder(_p)
    minecart()
    armchair()
