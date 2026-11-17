#!/usr/bin/env python3
"""ship_art.py - the Dovetail as a real timber ship for map 109 (MAPGEN 2g).
Painted on the 16-px logical grid (doubled): curved hull with planking, a wale and the waterline foam, a raised bulwark
rail with a cap, lengthwise deck planks with butt joints, a pointed bow with stem post and bowsprit, a stern transom,
two masts with crow's nests, yards across the beam with the sails furled on them, shrouds and stays in tarred rope, and
a pennant. Layer `base` (hull, deck, rail, mast feet) and layer `over` (yards, sails, rigging, crow's nests; drawn above
the player). slice() turns both into unique 32x32 tiles plus a placement list for layouts/dovetail.py."""
import math
from PIL import Image, ImageDraw

W, H = 34, 22                     # map 109
CY = 10.5                         # hull centre line (tile units, centre of row 10)
MASTS = [(11, 9), (22, 9)]       # mast feet (tile cells); keep clear of story events
GANG = (9, 15)


def half(xf):
    """Half-beam in tiles at x (continuous): straight waist, rounded stern, long tapering bow."""
    if xf < 7.0: return max(0.0, 5.5 * (1 - ((7.0 - xf) / 5.0) ** 2))
    if xf > 22.0: return max(0.0, 5.5 * (1 - ((xf - 22.0) / 8.6) ** 1.6))
    return 5.5


def deck(x, y):
    """Tile-level deck mask (same footprint the story events were seated on)."""
    if not 5 <= y <= 15: return False
    return 3 <= x <= 30 and abs(y - 10) <= half(x + 0.5) + 0.01


S = 16
DECK = [(150, 112, 72), (178, 138, 92), (204, 166, 116), (222, 190, 140)]
HULL = [(48, 30, 22), (78, 48, 30), (106, 68, 42), (138, 92, 58)]
ROPE = (52, 40, 30)


def paint():
    base = Image.new('RGBA', (W * S, H * S)); over = Image.new('RGBA', (W * S, H * S))
    b = base.load(); d = ImageDraw.Draw(base); o = ImageDraw.Draw(over)
    top = lambda xf: (CY - half(xf) - 0.5) * S
    bot = lambda xf: (CY + half(xf) + 0.5) * S
    for px in range(W * S):
        xf = px / float(S)
        h = half(xf)
        if h <= 0.05 and not (2.6 <= xf <= 31.6): continue
        t, bt = top(xf), bot(xf)
        if h <= 0.05: t, bt = CY * S - 3, CY * S + 3
        # hull: visible flank under the deck edge (south), a dark lip on the north
        for py in range(int(t) - 3, int(bt) + 22):
            if py < 0 or py >= H * S: continue
            if py < t:                                      # north lip
                b[px, py] = HULL[0] + (255,)
            elif py >= bt:                                  # south flank: planks, wale, waterline
                k = py - int(bt)
                if k < 2: c = HULL[3]
                elif k < 5: c = HULL[2] if (px // 6 + k) % 7 else HULL[1]
                elif k < 7: c = (176, 128, 72)              # the wale
                elif k < 15: c = HULL[1] if (k % 3) else HULL[0]
                elif k < 17: c = (28, 22, 20)               # waterline
                else:
                    c = (232, 244, 250) if (px * 7 + k * 3) % 5 == 0 else None
                    if c is None: continue
                    b[px, py] = c + (200,); continue
                b[px, py] = c + (255,)
            else:                                           # deck planks run fore and aft
                row = int((py - t) // 4)
                joint = ((px + row * 23) % 48) == 0
                c = DECK[2] if (py - t) % 4 else DECK[0]
                if joint: c = DECK[0]
                if row % 5 == 2 and (py - t) % 4 == 1: c = DECK[3]
                b[px, py] = c + (255,)
    # bulwark: a raised rail just inside the hull edge (cap light, inner shadow)
    for px in range(W * S):
        xf = px / float(S); h = half(xf)
        if h <= 0.05: continue
        t, bt = int(top(xf)), int(bot(xf))
        for py, c in ((t, HULL[3]), (t + 1, (232, 200, 150)), (t + 2, (232, 200, 150)), (t + 3, HULL[1]), (t + 4, DECK[0]),
                      (bt - 1, HULL[2]), (bt - 2, (232, 200, 150)), (bt - 3, (232, 200, 150)), (bt - 4, HULL[1])):
            if 0 <= py < H * S: b[px, py] = c + (255,)
        if px % 16 == 8:                                     # stanchions along the rail
            for py in (t + 1, t + 2, bt - 2, bt - 3): b[px, py] = HULL[1] + (255,)
    gx = GANG[0] * S                                         # the gangway gap aft on the starboard side
    for px in range(gx + 2, gx + 14):
        bt = int(bot(px / float(S)))
        for py in range(bt - 4, bt): b[px, py] = DECK[1] + (255,)
    # bow: stem post and bowsprit; stern: transom with a gilt band
    d.line([(int(30.6 * S), int(CY * S)), (int(33.8 * S), int(CY * S) - 6)], fill=HULL[1] + (255,), width=3)
    d.line([(int(30.6 * S), int(CY * S) - 1), (int(33.8 * S), int(CY * S) - 7)], fill=HULL[3] + (255,), width=1)
    for py in range(int(top(2.8)), int(bot(2.8))):
        for px in range(int(2.0 * S), int(2.8 * S)):
            if b[px, py][3]: b[px, py] = ((196, 160, 60) if py % 9 == 4 else HULL[1]) + (255,)
    # hatches (grated), the capstan
    for (hx, hy, hw, hh) in ((16.2, 9.2, 1.6, 1.6), (19.5, 12.2, 1.4, 1.0)):
        x0, y0 = int(hx * S), int(hy * S)
        d.rectangle((x0, y0, x0 + int(hw * S), y0 + int(hh * S)), fill=HULL[1] + (255,))
        for gx2 in range(x0 + 2, x0 + int(hw * S) - 1, 3):
            for gy2 in range(y0 + 2, y0 + int(hh * S) - 1, 3): base.putpixel((gx2, gy2), (40, 28, 20, 255))
    # masts: round feet on deck; yards across the beam with furled sails, crow's nests, rigging overhead
    for i, (mx, my) in enumerate(MASTS):
        cx, cy = mx * S + 8, my * S + 8
        d.ellipse((cx - 6, cy - 5, cx + 6, cy + 7), fill=(40, 30, 24, 120))
        d.ellipse((cx - 5, cy - 6, cx + 5, cy + 4), fill=HULL[2] + (255,)); d.ellipse((cx - 3, cy - 5, cx + 1, cy - 1), fill=HULL[3] + (255,))
        span = half(mx + 0.5) + 1.4
        y0, y1 = int((CY - span) * S), int((CY + span) * S)
        yx = cx + (0 if i else 2)
        o.rectangle((yx - 2, y0, yx + 2, y1), fill=HULL[1] + (255,))                      # the yard
        o.rectangle((yx - 6, y0 + 6, yx + 4, y1 - 6), fill=(226, 214, 186, 255))           # furled sail
        o.rectangle((yx - 6, y0 + 6, yx - 5, y1 - 6), fill=(186, 170, 140, 255))
        for ty in range(y0 + 10, y1 - 8, 9): o.rectangle((yx - 6, ty, yx + 4, ty + 1), fill=ROPE + (255,))   # gaskets
        o.ellipse((cx - 9, cy - 22, cx + 9, cy - 6), fill=HULL[1] + (255,)); o.ellipse((cx - 7, cy - 20, cx + 7, cy - 8), fill=HULL[3] + (255,))
        o.ellipse((cx - 3, cy - 17, cx + 3, cy - 11), fill=HULL[0] + (255,))                 # crow's nest, mast through it
        for sx in (-2.2, 2.2):                                                              # shrouds to both rails
            for side in (-1, 1):
                ex = int((mx + sx) * S); ey = int((CY + side * (half(mx + sx) + 0.2)) * S)
                o.line([(cx, cy - 14), (ex, ey)], fill=ROPE + (220,), width=1)
        if i == 0:                                                                           # pennant
            o.polygon([(cx + 2, cy - 24), (cx + 16, cy - 21), (cx + 2, cy - 18)], fill=(46, 76, 150, 255))
            o.line([(cx + 2, cy - 24), (cx + 16, cy - 21)], fill=(200, 60, 60, 255))
    fx, fy = MASTS[1][0] * S + 8, MASTS[1][1] * S + 8                                       # forestay to the bowsprit
    o.line([(fx, fy - 14), (int(33.6 * S), int(CY * S) - 6)], fill=ROPE + (220,), width=1)
    mx0, my0 = MASTS[0][0] * S + 8, MASTS[0][1] * S + 8
    o.line([(mx0, my0 - 14), (fx, fy - 14)], fill=ROPE + (200,), width=1)                  # the stay between the masts
    big = lambda im: im.resize((im.width * 2, im.height * 2), Image.NEAREST)
    return big(base), big(over)


def slice_tiles():
    """-> (tiles [RGBA 32x32], passages, priorities, placements [(x, y, layer, index)])"""
    base, over = paint(); tiles = []; pas = []; pri = []; seen = {}; place = []
    def add(im, p, q):
        k = (im.tobytes(), p, q)
        if k not in seen:
            seen[k] = len(tiles); tiles.append(im); pas.append(p); pri.append(q)
        return seen[k]
    for y in range(H):
        for x in range(W):
            bb = base.crop((x * 32, y * 32, x * 32 + 32, y * 32 + 32)); oo = over.crop((x * 32, y * 32, x * 32 + 32, y * 32 + 32))
            hb, ho = bb.getbbox() is not None, oo.getbbox() is not None
            on_deck = deck(x, y)
            if on_deck:
                rim = not all(deck(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))) and (x, y) != GANG \
                    and not (y == 10 and 26 <= x <= 29)          # the bow walk up to the stem (the Horizon scene)
                solid = rim or (x, y) in MASTS
                if hb: place.append((x, y, 0, add(bb, 15 if solid else 0, 0)))
                if ho: place.append((x, y, 2, add(oo, 0, 3)))
            elif hb or ho:                                   # hull and rigging over the sea: one composite, solid, under
                cm = bb.copy(); cm.alpha_composite(oo)
                place.append((x, y, 2, add(cm, 15, 0)))
    return tiles, pas, pri, place


def strip():
    tiles, pas, pri, place = slice_tiles()
    n = (len(tiles) + 7) // 8 * 8
    im = Image.new('RGBA', (256, n // 8 * 32))
    for i, t in enumerate(tiles): im.paste(t, (i % 8 * 32, i // 8 * 32))
    return im, pas + [0] * (n - len(tiles)), pri + [0] * (n - len(tiles)), place
