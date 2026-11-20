#!/usr/bin/env python3
"""The Glass Dunes (map 926) stage and the desert war's effect sheets, for :WAR_CLIMAX (SPINE Rev 18).

  python3 -I tools/build_desert.py        (also run by tools/build_war_assets.py)

Until map 926 is built, the stage is a picture composed from the reference games' own tiles (read-only, decoded with
mapgen/rmarshal.py, nothing executed):
  * dunes: Reborn's Twilight Desert (Map841) dune layer, recoloured bone-white;
  * the Northern Sea along the top: Rejuvenation's Zor Coast autotiles (tileset 154), greyed;
  * Skaldfast: Rejuvenation's Castle Weiss outer wall (Map631), rime-tinted, at the foot of a Kristiline ice cliff;
  * the Ashkaar Siege Camp: Rejuvenation Badlands tents and palisade on an earthwork;
  * a sandstone mesa (Rejuvenation's Zorrialyn Desert, Map373) for Meridian's observers;
  * skulls, rocks and dead trees from both desert tilesets.
The flood-sea, the glass and the bone-carters are separate sheets so the scene can animate them.
"""
import os, sys, json, math, random
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_war_assets as B                      # save(), src(), up2(), tint_cloth(), CREDITS
import rmarshal, render, terrain, rdraw

REF = B.REF
W, H = 64, 24                                      # stage size in tiles (32 px), same as the old ice stage
STAGE = "pfw_glass_dunes"


def s(v):
    return v.decode("utf-8", "replace") if isinstance(v, (bytes, bytearray)) else str(v)


def tileset(game, tid):
    t = rmarshal.load_file(os.path.join(REF, game, "Data/Tilesets.rxdata"))[tid]
    return {"tileset_name": s(t.tileset_name), "autotile_names": [s(a) for a in t.autotile_names],
            "priorities": [int(v) for v in t.priorities.data.flatten()]}


def draw(game, ts, d):
    """Render a (3, h, w) tile array with a game's tileset; empty cells come out transparent."""
    class M: pass
    class T: pass
    m = M(); m.width, m.height = d.shape[2], d.shape[1]
    m.data = T(); m.data.data = d; m.events = {}
    render.GFX = os.path.join(REF, game, "Graphics"); render.OUT_GFX = "/nonexistent"
    a = np.array(render.render(m, events=False, ts=ts).convert("RGBA"))
    black = (a[:, :, 0] == 0) & (a[:, :, 1] == 0) & (a[:, :, 2] == 0)
    a[black, 3] = 0
    return Image.fromarray(a)


def ramp_map(img, ramp, mask=None, anchor=None):
    """Re-ramp the opaque pixels by the luminance of their colours (keeps the pixel art's banding). With anchor=k
    the commonest colour becomes ramp[k], darker colours spread over ramp[:k] and lighter ones over ramp[k+1:]."""
    a = np.array(img.convert("RGBA"))
    op = a[:, :, 3] > 0
    if mask is not None: op &= mask
    px = a[op][:, :3]
    if len(px) == 0: return img
    cols, inv, cnt = np.unique(px.reshape(-1, 3), axis=0, return_inverse=True, return_counts=True)
    lum = cols[:, 0] * 0.3 + cols[:, 1] * 0.59 + cols[:, 2] * 0.11
    lo, hi = lum.min(), lum.max()
    if anchor is None:
        idx = np.minimum(((lum - lo) / max(hi - lo, 1e-3) * len(ramp)).astype(int), len(ramp) - 1)
    else:
        mode = lum[np.argmax(cnt)]
        idx = np.full(len(lum), anchor)
        dk = lum < mode - 0.5
        lt = lum > mode + 0.5
        idx[dk] = np.minimum((((lum[dk] - lo) / max(mode - lo, 1e-3)) * anchor).astype(int), anchor - 1)
        idx[lt] = anchor + 1 + np.minimum((((lum[lt] - mode) / max(hi - mode, 1e-3)) * (len(ramp) - anchor - 1)).astype(int),
                                          len(ramp) - anchor - 2)
    lut = np.array(ramp, dtype=np.uint8)[idx]
    a[op, :3] = lut[inv.reshape(-1)]
    return Image.fromarray(a)


def mix(img, rgb, amount, mask=None):
    a = np.array(img.convert("RGBA")).astype(np.float32)
    m = a[:, :, 3] > 0 if mask is None else mask
    for i in range(3):
        a[m, i] = a[m, i] * (1 - amount) + rgb[i] * amount
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


BONE = [(112, 94, 82), (150, 132, 112), (186, 170, 146), (212, 198, 174), (234, 226, 208), (250, 246, 236)]
SEA_GREY = [(52, 62, 78), (74, 88, 106), (102, 118, 136), (140, 156, 170), (196, 206, 214), (236, 240, 244)]
GLASS = [(96, 150, 176), (150, 206, 222), (196, 236, 244), (232, 250, 252), (255, 255, 255)]
HOT = [(150, 50, 30), (232, 110, 40), (255, 190, 90), (255, 240, 190), (255, 255, 255)]
WATER = [(40, 56, 80), (62, 84, 110), (92, 116, 140), (140, 164, 184)]


# --------------------------------------------------------------------------- pieces
def dunes():
    """Reborn Map841's dune field, dune tiles only (no ledges, palms or cacti), recoloured bone-white."""
    ts = tileset("reborn", 12)
    m = rmarshal.load_file(os.path.join(REF, "reborn/Data/Map841.rxdata"))
    d = np.array(m.data.data[:, 34:34 + H, 20:20 + W], dtype=np.int64)
    rows = set(range(79, 83)) | set(range(84, 88)) | set(range(94, 98))
    for z in (1, 2):
        t = d[z]
        r, c = (t - 384) // 8, (t - 384) % 8
        keep = (t >= 384) & np.isin(r, list(rows)) & (c < 6)
        t[~keep] = 0
    d[2][:] = 0
    d[0][:] = 144                                   # the Desert Dark autotile: plain sand under the dunes
    terrain.autotile_layer(d, 0, 144)
    return ramp_map(draw("reborn", ts, d), BONE, anchor=3)


def sea_depths():
    """Depth in tiles of the sea at each column (smooth: neighbours differ by at most one)."""
    dep = {}
    for x in range(13, 49):
        edge = min(x - 13, 48 - x)
        dep[x] = max(1, int(round(1.3 + min(edge, 6) * 0.3 + 1.2 * terrain.vnoise(x, 0, 926, 4.0))))
    for _ in range(3):
        for x in range(14, 48):
            dep[x] = max(min(dep[x], dep[x - 1] + 1, dep[x + 1] + 1), 1)
            if dep[x - 1] == dep[x + 1] and dep[x] != dep[x - 1]: dep[x] = dep[x - 1]
    return dep


def sea_mask():
    m = np.zeros((H, W), dtype=bool)
    for x, dpt in sea_depths().items():
        m[:dpt, x] = True
    return m


def shore(img):
    """Wet sand and a foam line along the Northern Sea's edge."""
    d = ImageDraw.Draw(img)
    for x, dpt in sea_depths().items():
        y = dpt * 32
        for k in range(32):
            px = x * 32 + k
            d.line([px, y, px, y + 5 + int(2 * math.sin(px * 0.21))], fill=BONE[2] + (255,))
            d.point([px, y + int(1.5 * math.sin(px * 0.33))], fill=(248, 250, 252, 255))
            if k % 3: d.point([px, y + 2 + int(1.5 * math.sin(px * 0.17 + 1))], fill=(214, 222, 230, 255))
    return img


def sea():
    """The Northern Sea along the horizon (Rejuvenation Zor Coast 'Sea' autotile), greyed."""
    ts = tileset("rejuvenation", 154)
    d = np.zeros((3, H, W), dtype=np.int64)
    d[0][sea_mask()] = 192                          # 'Sea'
    terrain.autotile_layer(d, 0, 192)
    return ramp_map(draw("rejuvenation", ts, d), SEA_GREY, anchor=2)


def glacier_and_wall():
    """Skaldfast: Castle Weiss's gate towers, rime-tinted, under a Kristiline ice cliff (the Mast Glacier's foot)."""
    out = Image.new("RGBA", (W * 32, H * 32), (0, 0, 0, 0))
    # the ice cliff: Kristiline (Frozen) snow + cliff faces, as the old ice stage built them
    ts = tileset("rejuvenation", 93)
    d = np.zeros((3, 6, 22), dtype=np.int64)
    d[0][:] = 2475                                  # snow
    rng = np.random.RandomState(3)
    for x in range(22):
        d[1, 3, x] = [761, 689, 690][rng.randint(0, 3)] if rng.rand() < 0.3 else 761
        d[1, 4, x] = 1485
    d[0, 4:, :] = 0
    cliff = draw("rejuvenation", ts, d)
    out.alpha_composite(cliff, (0, -40))
    ts2 = tileset("rejuvenation", 199)
    m = rmarshal.load_file(os.path.join(REF, "rejuvenation/Data/Map631.rxdata"))
    dd = np.array(m.data.data[:, 44:56, 0:26], dtype=np.int64)
    wall = draw("rejuvenation", ts2, dd).crop((280, 40, 768, 318))
    a = np.array(wall)
    green = (a[:, :, 1] > a[:, :, 0] + 12) & (a[:, :, 1] > a[:, :, 2] - 4)   # the castle garden behind the walk
    teal = (a[:, :, 2] > 150) & (a[:, :, 1] > 150) & (a[:, :, 0] < 120)       # moat water
    a[green | teal, 3] = 0
    wall = mix(Image.fromarray(a), (214, 232, 250), 0.22)
    d2 = ImageDraw.Draw(wall)
    rng2 = random.Random(5)
    for x in range(0, wall.width, 12):                                       # rime icicles along the parapets
        for y0 in (110, 150):
            if rng2.random() < 0.5 and a[min(y0 + 2, a.shape[0] - 1), min(x, a.shape[1] - 1), 3] > 0:
                L = rng2.randrange(3, 9)
                d2.line([x, y0, x, y0 + L], fill=(236, 248, 255, 255))
    out.alpha_composite(wall, (0, 320 - wall.height))
    return out, (0, 320 - wall.height, wall.width, 320)


def rimed_sands(base):
    """Isenmar's frozen sand west of x 15 tiles: tinted rime-white, frost glints, white trench-lines with dark slots."""
    a = np.array(base).astype(np.float32)
    yy, xx = np.mgrid[0:H * 32, 0:W * 32]
    edge = 470 + 46 * np.sin(yy / 41.0) + 28 * np.sin(yy / 13.0 + 1.3)
    k = np.clip((edge - xx) / 36.0, 0, 1)
    k = np.where((k > 0) & (k < 1), np.where(((xx + yy) % 2 == 0) & (k > 0.5), 1.0, np.where(k > 0.75, 1.0, 0.0)), k)
    k = k * (yy > 250)
    for i, c in enumerate((222, 236, 250)):
        a[:, :, i] = a[:, :, i] * (1 - 0.42 * k) + c * 0.42 * k
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(img)
    rng = random.Random(77)
    for _ in range(260):
        x, y = rng.randrange(0, 500), rng.randrange(330, 760)
        if x < 520 - (y - 330) * 0.05:
            d.point([x, y], fill=(255, 255, 255, 255))
    for ty, x1 in ((362, 470), (474, 440), (590, 400), (690, 360)):           # zig-zag trenches
        pts, x = [], 0
        y = ty
        while x < x1:
            pts.append((x, y)); x += rng.randrange(36, 64); y = ty + rng.choice((-10, 0, 10))
        pts.append((x1, y))
        d.line(pts, fill=(250, 252, 255, 255), width=9)                     # the rime spoil bank
        d.line([(p[0], p[1] + 2) for p in pts], fill=(46, 54, 78, 255), width=4)   # the dark slot
        d.line([(p[0], p[1] + 5) for p in pts], fill=(150, 168, 196, 255), width=1)
        for p in pts[1:-1]:
            d.rectangle([p[0] - 3, p[1] - 6, p[0] + 3, p[1] - 3], fill=(236, 240, 246, 255), outline=(120, 132, 156, 255))  # sandbag
    return img


def tile_crop(game, name, col, row, w, h):
    im = Image.open(B.src(game, "Tilesets", name)).convert("RGBA")
    return im.crop((col * 32, row * 32, (col + w) * 32, (row + h) * 32))


BAD = "Badlands - Desert.png"


def siege_camp(img):
    """The Ashkaar Siege Camp (east): an earthwork with a stake palisade, red-and-white tents behind it."""
    d = ImageDraw.Draw(img)
    x0, x1, y = 1250, 1760, 330                     # the earthwork's foot
    rng = random.Random(15)
    for x in range(x0, x1, 4):                      # earthwork berm: lit crest, shaded face (bone ramp)
        h = 22 + int(3 * math.sin(x * 0.05))
        d.line([x, y - h, x, y], fill=BONE[2] + (255,)); d.line([x + 1, y - h, x + 1, y], fill=BONE[2] + (255,))
        d.line([x, y - h + 6, x, y], fill=BONE[1] + (255,)); d.line([x + 2, y - h + 10, x + 3, y], fill=BONE[0] + (255,))
        d.line([x, y - h, x + 3, y - h], fill=BONE[4] + (255,))
    tent = tile_crop("rejuvenation", BAD, 0, 509, 5, 5)
    brown = tile_crop("rejuvenation", BAD, 4, 506, 3, 3)
    for (tx, ty, im) in ((1310, 250, tent), (1440, 214, brown), (1540, 246, tent), (1650, 216, brown), (1716, 254, tent)):
        img.alpha_composite(im, (tx - im.width // 2, ty - im.height + 20))
    stakes = tile_crop("rejuvenation", BAD, 0, 12, 3, 2)
    for x in range(x0, x1, stakes.width - 2):
        if 1478 <= x <= 1530: continue              # the gate
        img.alpha_composite(stakes, (x, y - 22 - stakes.height + 14))
    return img


def mesa(img):
    """A sandstone mesa (Rejuvenation Map373's plateau and ledges), far right, where Meridian watches from."""
    ts = tileset("rejuvenation", 150)
    m = rmarshal.load_file(os.path.join(REF, "rejuvenation/Data/Map373.rxdata"))
    d = np.array(m.data.data[:, 15:24, 34:44], dtype=np.int64)
    sand = (d[0] == 2515) | ((d[0] > 0) & (d[0] < 384))
    d[0][sand] = 0
    piece = draw("rejuvenation", ts, d)
    a = np.array(piece).astype(np.float32)                                    # desaturate the orange 35%
    g = a[:, :, :3].mean(axis=2, keepdims=True)
    a[:, :, :3] = a[:, :, :3] * 0.65 + g * 0.35
    piece = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    img.alpha_composite(piece, (W * 32 - piece.width + 8, -14))
    return img, (W * 32 - piece.width + 8, -14, piece.width, piece.height)


def props(img, keep_out):
    """Skulls, bones, rocks and a dead tree from the two desert tilesets, scattered clear of the action."""
    pieces = [tile_crop("rejuvenation", BAD, 3, 5, 1, 1), tile_crop("rejuvenation", BAD, 4, 5, 1, 1),
              tile_crop("rejuvenation", BAD, 0, 10, 2, 2), tile_crop("rejuvenation", BAD, 0, 2, 3, 2),
              tile_crop("reborn", "Desert.png", 7, 76, 1, 1), tile_crop("rejuvenation", BAD, 0, 0, 2, 2)]
    weights = [5, 3, 4, 2, 4, 1]
    rng = random.Random(9)
    placed = 0
    tries = 0
    while placed < 26 and tries < 2000:
        tries += 1
        x, y = rng.randrange(20, W * 32 - 60), rng.randrange(120, H * 32 - 40)
        if any(kx0 <= x <= kx1 and ky0 <= y <= ky1 for kx0, ky0, kx1, ky1 in keep_out): continue
        p = rng.choices(pieces, weights)[0]
        p = mix(p, BONE[2], 0.4)
        img.alpha_composite(p, (x, y))
        placed += 1
    return img


# --------------------------------------------------------------------------- the stage
def stage():
    base = dunes()
    base = rimed_sands(base)
    base.alpha_composite(sea())
    base = shore(base)
    wall, wall_box = glacier_and_wall()
    base.alpha_composite(wall)
    base = siege_camp(base)
    base, mesa_box = mesa(base)
    keep_out = [(0, 0, 520, 330), (430, 60, 1150, 600), (1240, 150, 1880, 360), (mesa_box[0] - 20, 0, 2048, 240),
                (0, 360, 520, 460), (1260, 380, 1760, 460), (700, 540, 940, 600)]
    base = props(base, keep_out)
    B.save(base, "Pictures", STAGE,
           "Reborn: Map841 (Twilight Desert) dune layer + Tileset 'Desert'; Rejuvenation: Map631 (Castle Weiss) wall, "
           "Tileset 'Kristiline Town (Frozen)', Map373 (Zorrialyn Desert) mesa, Tileset 'Badlands - Desert' tents, "
           "palisade, skulls, rocks, Zor Coast sea autotile",
           "composed 64x24-tile Glass Dunes: bone-white dunes, grey Northern Sea, Skaldfast (rime-tinted), the Rimed "
           "Sands' trench-lines, the Siege Camp; temporary stage for :WAR_CLIMAX until map 926 exists")
    json.dump({"tiles": [W, H], "skaldfast": wall_box, "mesa": mesa_box, "flood_box": FLOOD_BOX},
              open(os.path.join(B.OUT, "Pictures", STAGE + ".json"), "w"))


# --------------------------------------------------------------------------- the flood-sea
FX0, FY0, FW, FH = 12, 0, 24, 18                    # flood sheet region in tiles: x 384..1152, y 0..576
FLOOD_BOX = [FX0 * 32, FY0 * 32, FW * 32, FH * 32]


def flood_masks():
    """Six stages of Kyogre's flood pouring south from the sea into the hollows round Kyogre (700, 418): a union of
    lobes roughened with value noise; each frame admits the cells whose (noisy) arrival time has come."""
    lobes = [(21.0, 4.5, 8.0, 5.0), (21.5, 12.0, 7.0, 4.4), (16.0, 9.0, 4.0, 3.4), (26.0, 9.5, 2.6, 2.6), (27.5, 3.0, 5, 3)]
    out = []
    seam = sea_mask()[:FH, FX0:FX0 + FW]
    for f in range(6):
        e = (f + 1) / 6.0
        m = seam.copy()
        for y in range(FH):
            for x in range(FW):
                wx, wy = FX0 + x, FY0 + y
                n = (terrain.vnoise(wx, wy, 41, 1.7) - 0.5) + 0.6 * (terrain.vnoise(wx, wy, 43, 0.9) - 0.5)
                inside = min(((wx - cx) / rx) ** 2 + ((wy - cy) / ry) ** 2 for cx, cy, rx, ry in lobes) < 1.0 + 1.5 * n
                arrive = wy / 15.5 + 0.34 * (terrain.vnoise(wx, wy, 57, 1.8) - 0.5) + 0.05 * abs(wx - 22) / 6.0
                if inside and arrive <= e: m[y, x] = True
        for _ in range(2):                              # no pinholes or lone cells
            p = np.pad(m, 1)
            nb = p[:-2, 1:-1].astype(int) + p[2:, 1:-1] + p[1:-1, :-2] + p[1:-1, 2:]
            m = (m & (nb >= 2)) | (~m & (nb >= 3))
            m |= seam
        m[3:, 0] = False; m[3:, -1] = False
        out.append(m)
    return out


def flood():
    """Kyogre's flood-sea: 6 frames (3x2) of the Zor Coast 'Sea' autotile over transparent ground, greyed to the
    Northern Sea, with a foam front where it is still advancing. Anchor: bottom centre of the cell = (768, 576)."""
    ts = tileset("rejuvenation", 154)
    masks = flood_masks()
    cw, ch = FW * 32, FH * 32
    sheet = Image.new("RGBA", (cw * 3, ch * 2), (0, 0, 0, 0))
    for f, m in enumerate(masks):
        d = np.zeros((3, FH, FW), dtype=np.int64)
        d[0][m] = 192
        terrain.autotile_layer(d, 0, 192)
        im = ramp_map(draw("rejuvenation", ts, d), SEA_GREY, anchor=2)
        dr = ImageDraw.Draw(im)
        rng = random.Random(f)
        nxt = masks[min(f + 1, 5)]
        for y, x in np.argwhere(m):                      # foam: lips on the edge facing dry sand
            if y + 1 < FH and not m[y + 1, x]:
                by = (y + 1) * 32 - 6
                for k in range(0, 32, 2):
                    yy = by + int(2 * math.sin((x * 32 + k) * 0.35 + f))
                    dr.point([x * 32 + k, yy], fill=(250, 252, 255, 255))
                    if rng.random() < 0.6: dr.point([x * 32 + k + 1, yy + 1], fill=(206, 216, 226, 255))
                if f < 5 and nxt[y + 1, x]:                                       # still advancing: a thicker surf line
                    dr.line([x * 32, by - 3, x * 32 + 31, by - 3], fill=(236, 242, 248, 255), width=2)
        sheet.alpha_composite(im, ((f % 3) * cw, (f // 3) * ch))
    B.save(sheet, "Animations", "pfw_fx_flood", "Rejuvenation: Tileset 154 (Zor Coast) 'Sea' autotile",
           "6 frames (3x2 cells of 768x576): the flood-sea rolling south over the dunes, greyed, own foam")


# --------------------------------------------------------------------------- glass
def glass_ring():
    """Wet sand turning to steam-glass in a ring round the clash point: 4 growing frames, white-hot to cool glass.
    Logical 224x112 doubled to 448x224 (cells 4x1); squashed for the 3/4 view. Replaces the ice fracture."""
    W2, H2 = 224, 112
    sheet = Image.new("RGBA", (W2 * 2 * 4, H2 * 2), (0, 0, 0, 0))
    rng = random.Random(18)
    spokes = [(k * 2 * math.pi / 13 + rng.uniform(-0.2, 0.2), rng.uniform(0.75, 1.0)) for k in range(13)]
    for f in range(4):
        reach = (0.3, 0.55, 0.8, 1.0)[f]
        heat = (1.0, 0.7, 0.35, 0.0)[f]
        im = Image.new("RGBA", (W2, H2), (0, 0, 0, 0))
        a = np.zeros((H2, W2, 4), dtype=np.uint8)
        yy, xx = np.mgrid[0:H2, 0:W2]
        nx, ny = (xx - W2 / 2) / (W2 / 2 - 4), (yy - H2 / 2) / (H2 / 2 - 4)
        ang = np.arctan2(ny, nx)
        wob = 1 + 0.08 * np.sin(ang * 5 + f) + 0.05 * np.sin(ang * 11)
        r = np.sqrt(nx ** 2 + ny ** 2) / wob
        inside = r < reach
        band = np.clip((r / max(reach, 1e-3)), 0, 1)
        # cool glass: pale, diagonal gloss streaks; the edge still hot while it spreads
        gl = np.select([band > 0.92, band > 0.8, ((xx + yy * 2) // 6) % 7 == 0, band > 0.45], [4, 3, 3, 2], default=1)
        for k, c in enumerate(GLASS):
            m = inside & (gl == k)
            a[m, :3] = c; a[m, 3] = 215
        if heat > 0:
            hot = inside & (band > 1 - 0.35 * heat - 0.1)
            a[hot, :3] = HOT[2] if f < 2 else HOT[1]; a[hot, 3] = 235
            core = inside & (band < 0.35 * heat)
            a[core, :3] = HOT[4]; a[core, 3] = 240
        rim = inside & (band > 0.96)
        a[rim, :3] = (255, 255, 255); a[rim, 3] = 255
        im = Image.fromarray(a)
        d = ImageDraw.Draw(im)
        for th, L in spokes:                             # crazing: dark hairlines with a lit lower lip
            if f == 0: break
            px, py = W2 / 2, H2 / 2
            for step in range(int(10 * reach * L)):
                nxp = px + math.cos(th) * 5 + rng.uniform(-1.5, 1.5)
                nyp = py + math.sin(th) * 2.4 + rng.uniform(-1, 1)
                d.line([px, py + 1, nxp, nyp + 1], fill=(255, 255, 255, 230))
                d.line([px, py, nxp, nyp], fill=(70, 120, 150, 230))
                px, py = nxp, nyp
        sheet.alpha_composite(B.up2(im), (f * W2 * 2, 0))
    B.save(sheet, "Animations", "pfw_fx_glass_ring", "own art (tools/build_desert.py)",
           "4x1 cells of 448x224: sand glassing outward round the clash, hot to cool")


def glass_patch():
    """Blue Flare's trail on wet sand: 4 frames of one patch (32x16 logical -> 64x32): hot, white, cooling, glass."""
    sheet = Image.new("RGBA", (64 * 4, 32), (0, 0, 0, 0))
    for f in range(4):
        im = Image.new("RGBA", (32, 16), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        if f == 0:
            d.ellipse([2, 4, 29, 12], fill=HOT[1] + (230,)); d.ellipse([7, 6, 24, 10], fill=HOT[3] + (255,))
        elif f == 1:
            d.ellipse([1, 3, 30, 13], fill=HOT[2] + (240,)); d.ellipse([5, 5, 26, 11], fill=(255, 255, 255, 255))
        elif f == 2:
            d.ellipse([1, 3, 30, 13], fill=HOT[1] + (230,)); d.ellipse([3, 4, 28, 12], fill=GLASS[2] + (230,))
            d.line([8, 6, 20, 6], fill=(255, 255, 255, 255))
        else:
            d.ellipse([1, 3, 30, 13], fill=GLASS[1] + (220,)); d.ellipse([3, 4, 28, 11], fill=GLASS[2] + (220,))
            d.line([7, 6, 19, 5], fill=(255, 255, 255, 255)); d.line([21, 9, 25, 9], fill=GLASS[3] + (255,))
            d.arc([1, 3, 30, 13], 20, 160, fill=GLASS[0] + (220,))
        sheet.alpha_composite(B.up2(im), (f * 64, 0))
    B.save(sheet, "Animations", "pfw_fx_glass_patch", "own art (tools/build_desert.py)",
           "4x1 cells of 64x32: one patch of the glass trail under Blue Flare (hot -> glass)")


def glass_wave():
    """A breaking wave of the flood setting into glass mid-curl: frames 0-2 water curling, 3-5 water -> glass.
    Logical 64x48 doubled to 128x96; anchor bottom centre."""
    sheet = Image.new("RGBA", (128 * 6, 96), (0, 0, 0, 0))

    def wave(t, pal, foam):
        im = Image.new("RGBA", (64, 48), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        lift = int(6 * t)
        body = [(2, 47), (6, 34), (14, 24 - lift), (26, 14 - lift), (38, 10 - lift), (48, 12 - lift), (55, 18 - lift),
                (52, 22 - lift), (45, 19 - lift), (40, 22 - lift), (40, 30), (46, 40), (60, 47)]
        d.polygon(body, fill=pal[1] + (255,), outline=pal[0] + (255,))
        d.polygon([(10, 47), (14, 32), (22, 24 - lift), (30, 20 - lift), (34, 26), (34, 40), (40, 47)], fill=pal[2] + (255,))
        d.line([(16, 30 - lift // 2), (24, 22 - lift), (34, 16 - lift)], fill=pal[3] + (255,))
        d.arc([38, 16 - lift, 54, 32 - lift], 180, 330, fill=pal[0] + (255,))           # the curl's hollow
        for x, y in ((28, 13), (34, 11), (40, 10), (46, 11), (51, 14), (54, 17)):           # the lip
            d.point([x, y - lift], fill=foam + (255,)); d.point([x + 1, y - lift + 1], fill=foam + (255,))
        if t > 0.5:
            for x, y in ((50, 20), (53, 24), (56, 27)):
                d.point([x, y - lift + 4], fill=foam + (255,))
        return im
    wpal = [WATER[0], WATER[1], WATER[2], (190, 206, 220)]
    gpal = [GLASS[0], GLASS[1], GLASS[2], (255, 255, 255)]
    for f in range(6):
        if f < 3:
            im = wave(f / 2.0, wpal, (250, 252, 255))
        else:
            k = (f - 2) / 3.0
            pal = [tuple(int(w * (1 - k) + g * k) for w, g in zip(wp, gp)) for wp, gp in zip(wpal, gpal)]
            im = wave(1.0, pal, (255, 255, 255))
            if f == 5:
                d = ImageDraw.Draw(im)
                d.line([20, 26, 26, 18], fill=(255, 255, 255, 255)); d.line([30, 34, 33, 24], fill=(255, 255, 255, 255))
        sheet.alpha_composite(B.up2(im), (f * 128, 0))
    B.save(sheet, "Animations", "pfw_fx_glass_wave", "own art (tools/build_desert.py)",
           "6x1 cells of 128x96: a flood wave curling (0-2), then setting into glass (3-5)")


# --------------------------------------------------------------------------- people and props
def people():
    grunt = Image.open(B.src("rejuvenation", "Characters", "Grunt_1.png")).convert("RGBA")
    B.save(B.outline_dark(B.tint_cloth(grunt, (236, 228, 206), 0.85)), "Characters", "pfw_bone_carter",
           "Rejuvenation: Graphics/Characters/Grunt_1.png", "recoloured bone-white (Ossaria's bone-carters)")
    im, _ = rdraw.banner([(150, 140, 120, 255), (240, 236, 222, 255), (255, 255, 250, 255)])
    B.save(B.up2(B.up2(im)), "Characters", "pfw_banner_carters", "Prismfall mapgen/rdraw.py banner()",
           "own art, 4x scale (64x128): the bone-carters' white banner")
    sled, _ = rdraw.sled()
    B.save(B.up2(sled), "Characters", "pfw_sled", "Prismfall mapgen/rdraw.py sled()", "own art, 2x scale (64x32): an Isenmar ice-sledge")
    B.copy("rejuvenation", "Characters", "pkmn_gyarados.png", "pfw_gyarados",
           "4x4 overworld follower sprite (Marisol's Gyarados, no-legend variant)")


def build():
    stage()
    flood()
    glass_ring()
    glass_patch()
    glass_wave()
    people()


if __name__ == "__main__":
    build()
    for f, o, n in B.CREDITS:
        print("| `%s` | %s | %s |" % (f, o, n))
