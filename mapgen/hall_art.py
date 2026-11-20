"""hall_art.py - the hand-drawn pieces of tileset 54 "PF Rejuv Halls" (compose_halls.py), for the Gym 1/2 art pass.

Everything is drawn on the 16-px grid and doubled with nearest neighbour, so the pixel density matches the Rejuvenation
tiles it sits beside (MAPGEN 2h).  Colour ramps are taken from the neighbouring Rejuvenation tiles (Nightbox Theater's
gold and velvet, Sensei's House timber).  Each function returns a PIL RGBA image whose size is a multiple of 32.

  backdrop()          the Playhouse's painted drop: Saltmere harbour at dusk (15 x 4 tiles)
  gold_column(part)   proscenium pilaster: 'cap', 'shaft', 'base' (1 tile each)
  proscenium_beam()   the gilded beam over the stage opening (1 tile, repeats)
  footlight()         stage front with a brass footlight hood (1 tile, repeats); glow(): warm wash for the apron
  pit_floor(), pit_rail(), music_stand()
  loom_face(), lower_floor(row), warp_overlay(kind), light(kind), post(part), window(part), beam(), heddle_frame(...)"""
import random
from PIL import Image, ImageDraw

GOLD = [(64, 38, 14), (112, 74, 24), (168, 120, 38), (214, 170, 64), (244, 214, 128), (255, 246, 206)]
RED = [(46, 8, 14), (86, 16, 24), (128, 28, 36), (172, 48, 52), (210, 86, 80)]
WOOD = [(34, 20, 14), (56, 34, 22), (84, 54, 34), (116, 78, 48), (150, 106, 66), (186, 140, 90)]
SILK = [(236, 230, 214), (200, 192, 176), (150, 142, 134)]


def up(im):
    """16-px art -> 32-px tile density."""
    return im.resize((im.width * 2, im.height * 2), Image.NEAREST)


def tiles(im):
    """Cut a 32-multiple image into {(col, row): tile}."""
    return {(x // 32, y // 32): im.crop((x, y, x + 32, y + 32)) for y in range(0, im.height, 32) for x in range(0, im.width, 32)}


def blank(w=16, h=16, fill=(0, 0, 0, 0)):
    return Image.new('RGBA', (w, h), fill)


# ---------------------------------------------------------------------------------------------- the painted backdrop
def backdrop(w=15, h=4, seed=7):
    """Saltmere harbour at dusk, painted on a cloth drop: banded sky, clouds, the sun on the sea, the old town on the left
    headland and the lighthouse on the right.  w x h tiles."""
    W, H = w * 16, h * 16
    im = blank(W, H, (0, 0, 0, 255)); d = ImageDraw.Draw(im); r = random.Random(seed)
    horizon = int(H * 0.70)
    bands = [(40, 34, 84), (64, 44, 108), (104, 56, 126), (152, 70, 128), (206, 96, 116), (238, 140, 104), (250, 186, 120)]
    edges = [int(horizon * k / len(bands)) for k in range(len(bands) + 1)]
    for i, c in enumerate(bands):
        d.rectangle([0, edges[i], W, edges[i + 1]], fill=c)
        if i:                                                       # a dithered seam between bands (painted, not airbrushed)
            for x in range(0, W, 2):
                im.putpixel((x + (edges[i] % 2), edges[i]), bands[i - 1] + (255,))
    sx = int(W * 0.68)
    for rr, c in ((11, (252, 210, 120)), (9, (255, 232, 160)), (6, (255, 248, 214))):
        d.ellipse([sx - rr, horizon - rr, sx + rr, horizon + rr], fill=c)
    for cx, cy, cw in ((int(W * 0.18), int(H * 0.22), 34), (int(W * 0.47), int(H * 0.14), 26), (int(W * 0.84), int(H * 0.30), 30),
                       (int(W * 0.34), int(H * 0.42), 22)):
        for k in range(5):                                          # a cloud: overlapping puffs, lit from below by the sun
            ox = cx - cw // 2 + k * cw // 5 + r.randint(-1, 1); oy = cy + r.randint(-2, 1); rad = r.randint(4, 6)
            d.ellipse([ox - rad, oy - rad + 1, ox + rad, oy + rad], fill=(150, 72, 120))
        for k in range(5):
            ox = cx - cw // 2 + k * cw // 5 + 1; oy = cy - 1; rad = 4
            d.ellipse([ox - rad, oy - rad, ox + rad, oy + rad - 2], fill=(226, 136, 136))
        d.line([(cx - cw // 2, cy + 3), (cx + cw // 2, cy + 3)], fill=(250, 190, 150))
    d.rectangle([0, horizon, W, H], fill=(46, 44, 96))                # the sea
    for y in range(horizon + 2, H - 4, 2):
        for _ in range(W // 14):
            x = r.randrange(0, W - 6); n = r.randint(2, 6)
            d.line([(x, y), (x + n, y)], fill=(76, 70, 132) if r.random() < 0.7 else (118, 92, 150))
    for y in range(horizon + 1, H - 3, 2):                           # the sun's road on the water
        n = max(2, 9 - (y - horizon) // 2) + r.randint(-1, 1)
        d.line([(sx - n, y), (sx + n, y)], fill=(250, 200, 130) if y % 4 else (255, 236, 176))
    hl = [(0, horizon - 9), (12, horizon - 11), (30, horizon - 10), (52, horizon - 7), (74, horizon - 4), (92, horizon + 1)]
    d.polygon(hl + [(92, horizon + 2), (0, horizon + 2)], fill=(58, 36, 78))     # the old-town headland, west
    for x0, ww, hh, roof in ((4, 6, 7, 'p'), (11, 5, 5, 'f'), (17, 7, 9, 's'), (26, 5, 6, 'p'), (32, 6, 5, 'f'), (40, 5, 8, 'p'),
                             (47, 6, 4, 'f'), (55, 4, 6, 'p'), (62, 5, 3, 'f')):
        top = horizon - 9 - hh + (x0 // 14)
        d.rectangle([x0, top, x0 + ww, horizon - 4], fill=(44, 26, 62))
        if roof == 'p': d.polygon([(x0 - 1, top), (x0 + ww // 2, top - 4), (x0 + ww + 1, top)], fill=(44, 26, 62))
        if roof == 's': d.polygon([(x0 + 2, top), (x0 + ww // 2, top - 10), (x0 + ww - 2, top)], fill=(44, 26, 62))
        for wy in range(top + 2, horizon - 5, 3):                     # lit windows
            if r.random() < 0.55: im.putpixel((x0 + 1 + r.randrange(max(1, ww - 1)), wy), (255, 214, 120, 255))
    d.polygon([(196, horizon + 2), (204, horizon - 5), (226, horizon - 7), (240, horizon - 3), (240, horizon + 2)], fill=(58, 36, 78))
    lx = 214                                                          # the lighthouse on the east breakwater
    for i, y in enumerate(range(horizon - 26, horizon - 6, 4)):
        d.rectangle([lx - 2 + (1 if i < 2 else 0), y, lx + 2 - (1 if i < 2 else 0), y + 3], fill=(236, 226, 220) if i % 2 == 0 else (188, 62, 64))
    d.rectangle([lx - 3, horizon - 30, lx + 3, horizon - 27], fill=(70, 50, 70))
    d.rectangle([lx - 1, horizon - 30, lx + 1, horizon - 28], fill=(255, 240, 170))
    d.polygon([(lx + 2, horizon - 29), (lx + 26, horizon - 36), (lx + 26, horizon - 23)], fill=(255, 226, 150, 255))
    for k in range(3):                                                # a two-master under sail on the horizon
        bx = 132 + k
    d.polygon([(118, horizon - 1), (134, horizon - 1), (131, horizon + 2), (121, horizon + 2)], fill=(44, 26, 62))
    d.line([(124, horizon - 1), (124, horizon - 14)], fill=(44, 26, 62)); d.line([(129, horizon - 1), (129, horizon - 11)], fill=(44, 26, 62))
    d.polygon([(124, horizon - 13), (124, horizon - 3), (119, horizon - 4)], fill=(232, 200, 190))
    d.polygon([(129, horizon - 10), (129, horizon - 3), (133, horizon - 4)], fill=(232, 200, 190))
    for x in range(0, W, 40):                                         # canvas seams and the batten at the foot of the drop
        for y in range(0, H - 3):
            if y % 5: continue
            p = im.getpixel((x, y)); im.putpixel((x, y), tuple(max(0, c - 18) for c in p[:3]) + (255,))
    d.rectangle([0, H - 3, W, H - 2], fill=WOOD[2]); d.line([(0, H - 1), (W, H - 1)], fill=WOOD[0]); d.line([(0, H - 3), (W, H - 3)], fill=WOOD[4])
    return up(im)


# ---------------------------------------------------------------------------------------------- proscenium and stage
def gold_column(part):
    """A gilded pilaster on the proscenium, over a dark wall (transparent around it)."""
    im = blank(); d = ImageDraw.Draw(im)
    if part == 'shaft':
        d.rectangle([3, 0, 12, 15], fill=GOLD[2])
        for x, c in ((3, GOLD[0]), (4, GOLD[1]), (6, GOLD[4]), (7, GOLD[3]), (9, GOLD[1]), (10, GOLD[3]), (11, GOLD[2]), (12, GOLD[0])):
            d.line([(x, 0), (x, 15)], fill=c)
        for y in (4, 11):
            d.point((7, y), fill=GOLD[5])
    elif part == 'cap':
        d.rectangle([3, 8, 12, 15], fill=GOLD[2])
        for x, c in ((3, GOLD[0]), (4, GOLD[1]), (6, GOLD[4]), (7, GOLD[3]), (9, GOLD[1]), (10, GOLD[3]), (12, GOLD[0])):
            d.line([(x, 8), (x, 15)], fill=c)
        d.rectangle([1, 3, 14, 7], fill=GOLD[3], outline=GOLD[0])          # the capital with its two scrolls
        d.line([(2, 4), (13, 4)], fill=GOLD[5])
        d.ellipse([0, 4, 4, 8], fill=GOLD[2], outline=GOLD[0]); d.ellipse([11, 4, 15, 8], fill=GOLD[2], outline=GOLD[0])
        d.point((2, 6), fill=GOLD[5]); d.point((13, 6), fill=GOLD[5])
        d.rectangle([2, 0, 13, 2], fill=GOLD[1], outline=GOLD[0]); d.line([(3, 1), (12, 1)], fill=GOLD[4])
    elif part == 'base':
        d.rectangle([3, 0, 12, 8], fill=GOLD[2])
        for x, c in ((3, GOLD[0]), (4, GOLD[1]), (6, GOLD[4]), (7, GOLD[3]), (9, GOLD[1]), (10, GOLD[3]), (12, GOLD[0])):
            d.line([(x, 0), (x, 8)], fill=c)
        d.rectangle([1, 9, 14, 11], fill=GOLD[3], outline=GOLD[0]); d.line([(2, 10), (13, 10)], fill=GOLD[5])
        d.rectangle([0, 12, 15, 15], fill=GOLD[1], outline=GOLD[0]); d.line([(1, 13), (14, 13)], fill=GOLD[3])
    return up(im)


def proscenium_beam(part='mid'):
    """The gilded beam across the top of the stage opening, with a row of carved rosettes."""
    im = blank(); d = ImageDraw.Draw(im)
    d.rectangle([0, 3, 15, 12], fill=GOLD[2])
    d.line([(0, 3), (15, 3)], fill=GOLD[0]); d.line([(0, 4), (15, 4)], fill=GOLD[4]); d.line([(0, 11), (15, 11)], fill=GOLD[1]); d.line([(0, 12), (15, 12)], fill=GOLD[0])
    d.ellipse([5, 5, 10, 10], fill=GOLD[3], outline=GOLD[1]); d.point((7, 7), fill=GOLD[5]); d.point((8, 7), fill=GOLD[0])
    for x in (1, 13): d.line([(x, 6), (x + 1, 9)], fill=GOLD[1])
    if part == 'l': d.rectangle([0, 3, 1, 12], fill=GOLD[0])
    if part == 'r': d.rectangle([14, 3, 15, 12], fill=GOLD[0])
    d.line([(0, 13), (15, 13)], fill=(20, 10, 16, 120)); d.line([(0, 14), (15, 14)], fill=(20, 10, 16, 60))
    return up(im)


def mask_crest():
    """Comedy-and-tragedy crest for the centre of the proscenium beam (3 tiles wide: gilded scrolls either side)."""
    im = blank(48, 16); d = ImageDraw.Draw(im)
    for x0, dx in ((2, 1), (45, -1)):                                 # acanthus scrolls running out along the beam
        for k in range(4):
            x = x0 + dx * k * 3; d.ellipse([min(x, x + dx * 4), 5 - k % 2, max(x, x + dx * 4), 10 - k % 2], fill=GOLD[3], outline=GOLD[0])
    d.ellipse([14, 0, 34, 15], fill=GOLD[2], outline=GOLD[0]); d.ellipse([16, 1, 32, 14], fill=GOLD[3])
    for cx, smile in ((20, True), (28, False)):
        d.ellipse([cx - 4, 3, cx + 4, 12], fill=(246, 238, 224), outline=GOLD[0])
        d.point((cx - 2, 6), fill=(30, 20, 30)); d.point((cx + 2, 6), fill=(30, 20, 30))
        if smile: d.arc([cx - 3, 6, cx + 3, 11], 20, 160, fill=(150, 30, 40))
        else: d.arc([cx - 3, 9, cx + 3, 13], 200, 340, fill=(40, 40, 110))
    return up(im)


def footlight():
    """The stage front (dark polished panel) with a brass footlight hood throwing light up onto the apron."""
    im = blank(16, 16, WOOD[1] + (255,)); d = ImageDraw.Draw(im)
    d.line([(0, 0), (15, 0)], fill=WOOD[4]); d.line([(0, 1), (15, 1)], fill=WOOD[3])
    d.rectangle([0, 6, 15, 13], fill=WOOD[2]); d.rectangle([1, 7, 14, 12], outline=WOOD[1]); d.line([(2, 8), (13, 8)], fill=WOOD[3])
    d.line([(0, 14), (15, 14)], fill=WOOD[0]); d.line([(0, 15), (15, 15)], fill=(20, 12, 10))
    d.rectangle([4, 1, 11, 4], fill=GOLD[2], outline=GOLD[0]); d.line([(5, 2), (10, 2)], fill=GOLD[4])
    d.rectangle([6, 0, 9, 0], fill=(255, 244, 190))
    return up(im)


def glow():
    """Warm wash thrown by the footlights onto the bottom of the apron (overlay, alpha)."""
    im = blank()
    for y in range(16):
        a = int(max(0, (y - 4)) * 7)
        for x in range(16):
            im.putpixel((x, y), (255, 214, 140, min(90, a)))
    for x in (7, 8):
        for y in range(10, 16): im.putpixel((x, y), (255, 236, 180, 110))
    return up(im)


def pit_floor(src, shade=0.48):
    """The orchestra pit's floor: the stage boards a storey down, in shadow."""
    im = src.copy().convert('RGBA'); px = im.load()
    for y in range(im.height):
        k = shade * (0.85 + 0.15 * y / im.height)
        for x in range(im.width):
            r, g, b, a = px[x, y]; px[x, y] = (int(r * k * 0.9), int(g * k * 0.9), int(b * k * 1.05 + 6), a)
    return im


def pit_rail(part='mid'):
    """Brass rail along the edge of the orchestra pit, a velvet skirt below it."""
    im = blank(); d = ImageDraw.Draw(im)
    d.rectangle([0, 7, 15, 12], fill=RED[2]); d.line([(0, 12), (15, 12)], fill=RED[0])
    for x in range(1, 16, 4): d.line([(x, 8), (x, 11)], fill=RED[1])
    d.line([(0, 13), (15, 13)], fill=(10, 4, 8, 120))
    d.line([(0, 5), (15, 5)], fill=GOLD[4]); d.line([(0, 6), (15, 6)], fill=GOLD[1])
    xs = {'mid': (7,), 'l': (1, 7), 'r': (7, 14)}[part]
    for x in xs:
        d.rectangle([x, 3, x + 1, 12], fill=GOLD[2]); d.point((x, 3), fill=GOLD[5]); d.line([(x + 1, 4), (x + 1, 12)], fill=GOLD[1])
    return up(im)


def music_stand():
    im = blank(); d = ImageDraw.Draw(im)
    d.line([(7, 6), (7, 14)], fill=(30, 26, 30)); d.line([(5, 14), (10, 14)], fill=(30, 26, 30))
    d.rectangle([3, 2, 12, 7], fill=(40, 34, 40)); d.rectangle([4, 2, 11, 6], fill=(236, 230, 214))
    for y in (3, 5): d.line([(5, y), (10, y)], fill=(120, 110, 110))
    return up(im)


# ---------------------------------------------------------------------------------------------- the Weaving Hall
def loom_face(part='mid', color=None):
    """The front of a walkway, seen across a loom bed: timber joists dropping to the floor below, the breast beam the warp
    is tied to along its top.  `color`: a heddle's colour cord tied round the beam (which heddles lift this bed)."""
    im = blank(16, 16, WOOD[1] + (255,)); d = ImageDraw.Draw(im)
    d.line([(0, 0), (15, 0)], fill=WOOD[5]); d.rectangle([0, 1, 15, 4], fill=WOOD[3]); d.line([(0, 4), (15, 4)], fill=WOOD[2])
    for x in range(1, 16, 4): d.point((x, 2), fill=WOOD[4])
    for x in (0, 8):
        d.rectangle([x + 2, 5, x + 5, 15], fill=WOOD[2]); d.line([(x + 2, 5), (x + 2, 15)], fill=WOOD[3]); d.line([(x + 5, 5), (x + 5, 15)], fill=WOOD[0])
    for y in range(6, 16):                                          # the shadow deepens toward the floor below
        for x in range(16):
            r, g, b, a = im.getpixel((x, y)); k = 1 - (y - 6) * 0.045
            im.putpixel((x, y), (int(r * k), int(g * k), int(b * k), a))
    for x in (1, 5, 9, 13):                                          # warp threads tied over the beam
        d.line([(x, 3), (x, 15)], fill=SILK[0])
    for x in (3, 11):
        d.line([(x, 4), (x, 15)], fill=SILK[2])
    if part == 'l': d.rectangle([0, 0, 1, 15], fill=WOOD[0])
    if part == 'r': d.rectangle([14, 0, 15, 15], fill=WOOD[0])
    if color:
        d.rectangle([5, 1, 10, 4], fill=color); d.line([(5, 1), (10, 1)], fill=tuple(min(255, c + 50) for c in color))
        d.line([(7, 4), (7, 9)], fill=color); d.line([(8, 4), (8, 8)], fill=tuple(int(c * 0.6) for c in color))
    return up(im)


def lower_floor(src, depth):
    """The storey below a loom bed, seen through the warp: the hall's boards, darker the nearer they lie under the
    walkway above (depth 0 = just under the lip, 1+ = further out)."""
    im = src.copy().convert('RGBA'); px = im.load()
    for y in range(im.height):
        k = 0.42 + 0.07 * min(depth, 3) + 0.05 * (y / im.height)
        for x in range(im.width):
            r, g, b, a = px[x, y]; px[x, y] = (int(r * k * 0.92), int(g * k * 0.95), int(b * k * 1.1 + 8), a)
    return im


def warp_overlay(kind='mid'):
    """The warp: taut silk threads stretched across a loom bed (overlay; the floor below shows between them).
    kind 'bot' adds the back beam the threads are tied to at the far side."""
    im = blank(); d = ImageDraw.Draw(im)
    for x in (1, 5, 9, 13):                                          # the warp: one thread in four, so the floor below shows
        d.line([(x, 0), (x, 15)], fill=SILK[0] + (215,))
        d.line([(x + 1, 0), (x + 1, 15)], fill=(40, 30, 40, 70))     # each thread's shadow on the boards below
    for x in (3, 11):
        d.line([(x, 0), (x, 15)], fill=SILK[1] + (120,))
    if kind == 'bot':
        d.rectangle([0, 11, 15, 14], fill=WOOD[3]); d.line([(0, 11), (15, 11)], fill=WOOD[5]); d.line([(0, 14), (15, 14)], fill=WOOD[1])
        d.line([(0, 15), (15, 15)], fill=(0, 0, 0, 90))
        for x in (1, 5, 9, 13): im.putpixel((x, 12), SILK[0] + (255,))
    return up(im)


def light(kind):
    """Window light lying across the floor (overlay).  kind: 'full', 'l' (band's left edge: lit right of a diagonal),
    'r' (band's right edge)."""
    im = blank()
    for y in range(16):
        for x in range(16):
            on = kind == 'full' or (kind == 'l' and x >= 15 - y) or (kind == 'r' and x < 15 - y)
            if on: im.putpixel((x, y), (255, 236, 186, 46))
    return up(im)


def post(part):
    """A square timber post rising from the floor below to the hall's roof (stands in a loom bed, beside the warp)."""
    im = blank(); d = ImageDraw.Draw(im)
    d.rectangle([4, 0, 11, 15], fill=WOOD[3]); d.line([(4, 0), (4, 15)], fill=WOOD[4]); d.line([(5, 0), (5, 15)], fill=WOOD[5])
    d.line([(10, 0), (10, 15)], fill=WOOD[2]); d.line([(11, 0), (11, 15)], fill=WOOD[1])
    if part == 'base':
        d.rectangle([3, 12, 12, 15], fill=WOOD[2], outline=WOOD[0])
    if part == 'band':
        d.rectangle([3, 6, 12, 9], fill=(110, 110, 118), outline=(50, 50, 58)); d.line([(4, 7), (11, 7)], fill=(170, 170, 178))
    return up(im)


def window(part, w=2):
    """A tall arched window in the timber wall: 'top' (arch), 'mid', 'sill'.  w tiles wide; returns a (16w x 16) strip."""
    W = 16 * w
    im = blank(W, 16); d = ImageDraw.Draw(im)
    glass = [(150, 190, 214), (178, 210, 226), (214, 232, 238)]
    if part == 'top':
        d.ellipse([1, 2, W - 2, 30], fill=WOOD[1]); d.ellipse([3, 4, W - 4, 30], fill=glass[1])
        d.ellipse([5, 6, W - 6, 30], fill=glass[2])
        d.line([(W // 2, 4), (W // 2, 15)], fill=WOOD[1])
        d.arc([3, 4, W - 4, 30], 180, 360, fill=WOOD[2])
    else:
        d.rectangle([1, 0, W - 2, 15], fill=WOOD[1]); d.rectangle([3, 0, W - 4, 15], fill=glass[1])
        for x in range(4, W - 4, 3): d.line([(x, 0), (x + 3, 15)], fill=glass[2]) if x % 2 else None
        d.line([(W // 2, 0), (W // 2, 15)], fill=WOOD[1]); d.line([(3, 7), (W - 4, 7)], fill=WOOD[1])
        if part == 'sill':
            d.rectangle([0, 12, W - 1, 15], fill=WOOD[4], outline=WOOD[1]); d.line([(1, 13), (W - 2, 13)], fill=WOOD[5])
    return up(im)


def heddle_frame(color, part):
    """A heddle frame: two uprights and the shafts of heddle wires, the shaft painted in its colour, a shape tag on the
    header so colour is never the only cue.  part 'top' (header) / 'bot' (the treadle lever at its foot)."""
    im = blank(); d = ImageDraw.Draw(im); dk = tuple(int(c * 0.55) for c in color); hl = tuple(min(255, int(c * 1.2) + 30) for c in color)
    if part == 'top':
        d.rectangle([1, 4, 14, 7], fill=color, outline=dk); d.line([(2, 5), (13, 5)], fill=hl)
        d.line([(2, 8), (2, 15)], fill=WOOD[2]); d.line([(13, 8), (13, 15)], fill=WOOD[2])
        for x in range(4, 12, 2): d.line([(x, 8), (x, 15)], fill=(200, 196, 186))
        d.line([(3, 12), (12, 12)], fill=dk)
    else:
        d.line([(2, 0), (2, 9)], fill=WOOD[2]); d.line([(13, 0), (13, 9)], fill=WOOD[2])
        for x in range(4, 12, 2): d.line([(x, 0), (x, 6)], fill=(200, 196, 186))
        d.rectangle([1, 6, 14, 9], fill=color, outline=dk); d.line([(2, 7), (13, 7)], fill=hl)
        d.rectangle([0, 10, 15, 13], fill=WOOD[3], outline=WOOD[1]); d.ellipse([5, 12, 10, 15], fill=(0, 0, 0, 80))
    return up(im)


def silk_bolt(color):
    """A bolt of finished silk lying on the floor below (seen dim, through the warp)."""
    im = blank(); d = ImageDraw.Draw(im); dk = tuple(int(c * 0.6) for c in color)
    d.rectangle([2, 6, 13, 11], fill=color, outline=dk); d.line([(3, 7), (12, 7)], fill=tuple(min(255, c + 40) for c in color))
    d.ellipse([11, 6, 15, 11], fill=dk); d.ellipse([12, 7, 14, 10], fill=color)
    return up(im)


def yarn_basket(colors):
    im = blank(); d = ImageDraw.Draw(im)
    d.ellipse([2, 4, 13, 9], fill=WOOD[2]); d.rectangle([2, 7, 13, 13], fill=WOOD[3], outline=WOOD[1])
    for y in (9, 11): d.line([(3, y), (12, y)], fill=WOOD[2])
    for i, c in enumerate(colors[:3]):
        d.ellipse([3 + i * 3, 3, 8 + i * 3, 8], fill=c, outline=tuple(int(k * 0.6) for k in c))
    return up(im)


def dim(im, k=0.55, blue=8):
    """A prop as seen a storey down in the loom bed's shadow."""
    im = im.copy().convert('RGBA'); px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a: px[x, y] = (int(r * k), int(g * k), min(255, int(b * k) + blue), a)
    return im


FONT = {'E': ['111', '100', '110', '100', '111'], 'D': ['110', '101', '101', '101', '110'], 'K': ['101', '110', '100', '110', '101'],
        '.': ['0', '0', '0', '0', '1'], ' ': ['0', '0', '0', '0', '0']}


def old_poster():
    """The Playhouse lobby's oldest poster: a red-and-gold bill pasted over with a plain cream notice years ago; where
    the paste has lifted, the old title shows through: "...ED K..."  (3 x 3 tiles, in a gilt frame)."""
    im = blank(48, 48); d = ImageDraw.Draw(im)
    d.rectangle([1, 1, 46, 46], fill=GOLD[1], outline=GOLD[0]); d.rectangle([2, 2, 45, 45], outline=GOLD[4])
    d.rectangle([4, 4, 43, 43], fill=RED[2]); d.rectangle([5, 5, 42, 42], outline=GOLD[3])
    d.polygon([(4, 4), (43, 4), (43, 22), (36, 25), (30, 21), (24, 26), (17, 22), (10, 26), (4, 23)], fill=(226, 214, 186))
    d.polygon([(4, 34), (12, 31), (20, 35), (30, 32), (43, 35), (43, 43), (4, 43)], fill=(214, 202, 174))
    for y in (9, 13, 17): d.line([(9, y), (38, y)], fill=(170, 156, 130))
    for y in (37, 40): d.line([(9, y), (34, y)], fill=(160, 146, 120))
    x = 9
    for ch in '...ED K...':                                          # the old gilt title showing through the gap
        g = FONT[ch]
        for yy, row in enumerate(g):
            for xx, b in enumerate(row):
                if b == '1': im.putpixel((x + xx, 26 + yy), GOLD[4] + (255,))
        x += len(g[0]) + 1
    d.line([(4, 23), (10, 26), (17, 22), (24, 26), (30, 21), (36, 25), (43, 22)], fill=(150, 136, 110))
    return up(im)
