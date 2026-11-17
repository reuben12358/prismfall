#!/usr/bin/env python3
"""material_art.py - per-biome variants of the pieces that kept looking out of place (MAPGEN 2g).
Built from Tectonic Outside tiles (same ids in tilesets 30, 33 and 40) plus a few hand-drawn pixels on the 16-px grid
(everything doubled with nearest-neighbour), so they match the pack:
  stairs (3x4, passable, on layer 3 over a cliff cut):
    stairs_log    earth-cut steps with log risers        forest, route
    stairs_stone  worn stone steps (castle-kit stairs, weathered to the cliff's grey-brown)   village, ruins
    stairs_plank  plank stairs between log posts          harbour, decks
  props:
    signpost (1x2)  wooden signpost         lantern (1x3)  lantern on a timber post, warm glass
    logbench (2x1)  split-log bench         barricade (2x1)  timber saw-horse barrier (painted top rail)
strip(sheet) -> (image 256 px wide, names {name: index of top-left tile}, passages, priorities); composers append it."""
from PIL import Image, ImageDraw

T = 32


def tile(sheet, tid):
    i = tid - 384
    return sheet.crop((i % 8 * T, i // 8 * T, i % 8 * T + T, i // 8 * T + T)).convert('RGBA')


def tint(im, mul, add=(0, 0, 0)):
    im = im.copy(); px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a: px[x, y] = (min(255, int(r * mul[0]) + add[0]), min(255, int(g * mul[1]) + add[1]), min(255, int(b * mul[2]) + add[2]), a)
    return im


def stairs_log(sheet):
    im = Image.new('RGBA', (96, 128))
    rock = tile(sheet, 2609); dirt = tile(sheet, 2572)
    for y in range(4):
        for x in range(3): im.paste(rock, (x * T, y * T))
    log = Image.new('RGBA', (64, 32)); log.paste(tile(sheet, 1017), (0, 0)); log.paste(tile(sheet, 1018), (32, 0))
    band = log.crop((0, 10, 64, 26))                                   # the log body, 16 px tall
    longlog = Image.new('RGBA', (84, 16)); longlog.paste(band.crop((0, 0, 42, 16)), (0, 0)); longlog.paste(band.crop((22, 0, 64, 16)), (42, 0))
    for i in range(4):
        y0 = i * T
        for x in range(6, 90, 2):                                      # tread: packed earth
            im.paste(dirt.crop((x % 32, 4, x % 32 + 2, 22)), (x, y0))
        im.alpha_composite(longlog, (6, y0 + 14))                     # riser: a log pegged across
        d = ImageDraw.Draw(im)
        d.rectangle((6, y0 + 28, 89, y0 + 29), fill=(60, 42, 30, 120))   # shadow under the log
    d = ImageDraw.Draw(im)
    for y in range(0, 128, 2):                                         # earth banks either side
        d.rectangle((4, y, 5, y + 1), fill=(96, 72, 52, 255)); d.rectangle((90, y, 91, y + 1), fill=(96, 72, 52, 255))
    return im


def stairs_stone(sheet):
    rows = [[3925, 3926, 3927], [3933, 3934, 3935], [3933, 3934, 3935], [3941, 3942, 3943]]
    im = Image.new('RGBA', (96, 128))
    for y, row in enumerate(rows):
        for x, t in enumerate(row): im.paste(tile(sheet, t), (x * T, y * T))
    im = tint(im, (0.80, 0.77, 0.72))
    d = ImageDraw.Draw(im)
    for (x, y) in ((20, 22), (60, 54), (34, 86), (72, 110), (12, 70)):  # moss in the joints
        d.rectangle((x, y, x + 3, y + 1), fill=(96, 128, 72, 255)); d.rectangle((x + 2, y - 2, x + 3, y - 1), fill=(120, 150, 86, 255))
    return im


def stairs_plank(sheet):
    im = Image.new('RGBA', (96, 128)); board = tile(sheet, 3814)
    d = ImageDraw.Draw(im)
    for i in range(4):
        y0 = i * T
        for x in range(8, 88, 32): im.paste(board.crop((0, 0, min(32, 88 - x), 22)), (x, y0))
        d.rectangle((8, y0 + 22, 87, y0 + 31), fill=(74, 52, 36, 255)); d.rectangle((8, y0 + 22, 87, y0 + 23), fill=(110, 80, 54, 255))
    for x0 in (0, 88):                                                 # log posts with a highlight
        d.rectangle((x0, 0, x0 + 7, 127), fill=(92, 64, 42, 255)); d.rectangle((x0 + 2, 0, x0 + 3, 127), fill=(140, 102, 66, 255))
        for y in range(6, 128, 32): d.rectangle((x0, y, x0 + 7, y + 1), fill=(62, 42, 28, 255))
    return im


def dbl(im): return im.resize((im.width * 2, im.height * 2), Image.NEAREST)
WOOD = [(58, 38, 26, 255), (96, 64, 40, 255), (138, 96, 60, 255), (178, 134, 88, 255)]


def signpost():
    c = Image.new('RGBA', (16, 32)); d = ImageDraw.Draw(c)
    d.ellipse((4, 28, 12, 31), fill=(30, 40, 30, 90))
    d.rectangle((7, 10, 8, 29), fill=WOOD[1]); d.line([(7, 10), (7, 29)], fill=WOOD[2])
    d.rectangle((1, 3, 14, 11), fill=WOOD[2]); d.rectangle((1, 3, 14, 3), fill=WOOD[3]); d.rectangle((1, 11, 14, 11), fill=WOOD[0])
    d.line([(1, 3), (1, 11)], fill=WOOD[0]); d.line([(14, 3), (14, 11)], fill=WOOD[0])
    for y in (5, 7, 9): d.line([(3, y), (12 - (y % 3), y)], fill=(70, 48, 32, 255))
    return dbl(c)


def lantern():
    c = Image.new('RGBA', (16, 48)); d = ImageDraw.Draw(c)
    d.ellipse((3, 44, 13, 47), fill=(30, 40, 30, 90))
    d.rectangle((5, 6, 6, 45), fill=WOOD[1]); d.line([(5, 6), (5, 45)], fill=WOOD[2])
    d.rectangle((5, 6, 12, 7), fill=WOOD[1])                                    # arm
    d.line([(11, 8), (11, 9)], fill=(60, 50, 40, 255))
    d.rectangle((9, 10, 13, 17), fill=(70, 52, 36, 255))                        # lantern frame
    d.rectangle((10, 11, 12, 16), fill=(255, 214, 110, 255)); d.point((11, 12), fill=(255, 250, 220, 255))
    d.rectangle((9, 9, 13, 9), fill=(48, 36, 26, 255))
    for (x, y, a) in ((8, 12, 90), (14, 12, 90), (11, 19, 80), (7, 15, 50), (15, 15, 50)):
        d.point((x, y), fill=(255, 220, 140, a))
    d.rectangle((3, 42, 8, 45), fill=(120, 116, 110, 255)); d.line([(3, 42), (8, 42)], fill=(160, 156, 148, 255))   # footing stone
    return dbl(c)


def logbench():
    c = Image.new('RGBA', (32, 16)); d = ImageDraw.Draw(c)
    d.ellipse((2, 12, 30, 15), fill=(30, 40, 30, 80))
    for x in (4, 25): d.rectangle((x, 9, x + 3, 13), fill=WOOD[1]); d.line([(x, 9), (x + 3, 9)], fill=WOOD[3])
    d.rectangle((2, 5, 29, 9), fill=WOOD[2]); d.line([(2, 5), (29, 5)], fill=WOOD[3]); d.line([(2, 9), (29, 9)], fill=WOOD[0])
    for x in range(5, 28, 6): d.point((x, 7), fill=WOOD[1])
    d.rectangle((1, 5, 2, 9), fill=(196, 160, 112, 255)); d.rectangle((29, 5, 30, 9), fill=(196, 160, 112, 255))   # cut ends
    return dbl(c)


def barricade():
    c = Image.new('RGBA', (32, 16)); d = ImageDraw.Draw(c)
    d.ellipse((2, 12, 30, 15), fill=(30, 40, 30, 80))
    for x0 in (3, 22):
        d.line([(x0, 13), (x0 + 6, 4)], fill=WOOD[1], width=2); d.line([(x0 + 6, 13), (x0, 4)], fill=WOOD[1], width=2)
    d.rectangle((1, 3, 30, 6), fill=(232, 228, 214, 255)); d.line([(1, 3), (30, 3)], fill=(255, 255, 255, 255))
    for x in range(4, 30, 8): d.rectangle((x, 3, x + 3, 6), fill=(46, 76, 140, 255))   # the Accord's blue bands
    d.line([(1, 6), (30, 6)], fill=WOOD[0])
    return dbl(c)


PIECES = [  # name, builder, (w, h), passages rows, priorities rows
    ('stairs_log', stairs_log, (3, 4), 0, 0), ('stairs_stone', stairs_stone, (3, 4), 0, 0), ('stairs_plank', stairs_plank, (3, 4), 0, 0),
    ('signpost', lambda s: signpost(), (1, 2), [[0], [15]], [[1], [0]]),
    ('lantern', lambda s: lantern(), (1, 3), [[0], [0], [15]], [[2], [1], [0]]),
    ('logbench', lambda s: logbench(), (2, 1), 15, 0), ('barricade', lambda s: barricade(), (2, 1), 15, 0)]


def strip(sheet):
    """-> (RGBA image 256 wide, {name: tile index}, passages list, priorities list); index 0 = first tile of the strip."""
    tiles = []; names = {}
    def pad():
        while len(tiles) % 8: tiles.append(None)
    for name, fn, (w, h), pas, pri in PIECES:
        im = fn(sheet)
        if len(tiles) % 8 + w > 8: pad()
        base = len(tiles); names[name] = base
        need = (h - 1) * 8 + w
        while len(tiles) < base + need: tiles.append(None)
        for j in range(h):
            for i in range(w):
                p = pas[j][i] if isinstance(pas, list) else pas; q = pri[j][i] if isinstance(pri, list) else pri
                tiles[base + j * 8 + i] = (im.crop((i * T, j * T, i * T + T, j * T + T)), p, q)
    pad()
    out = Image.new('RGBA', (256, len(tiles) // 8 * T))
    for k, t in enumerate(tiles):
        if t: out.paste(t[0], (k % 8 * T, k // 8 * T))
    return out, names, [t[1] if t else 0 for t in tiles], [t[2] if t else 0 for t in tiles]


def stamps(offset, names):
    """Stamp dicts (stamps_m.json format) for a tileset whose material strip starts at tile id `offset`."""
    out = {}
    for name, fn, (w, h), pas, pri in PIECES:
        b = offset + names[name]
        lay = [[[0] * w for _ in range(h)] for _ in range(3)]
        for j in range(h):
            for i in range(w):
                z = 2 if name.startswith('stairs') else (1 if (isinstance(pri, list) and pri[j][i] == 0) or pri == 0 else 2)
                lay[z][j][i] = b + j * 8 + i
        out[name] = {'w': w, 'h': h, 'layers': lay}
    return out
