"""Round 4 (sky fix): clouds that live in the sky.

MEADOW: the old cloud strip was a single flat band of white puffs drawn over the whole room (z above the room
bitmap), so it crossed the oak canopy and the windmill with a ruler-straight underside, and the room's top margin
was a mirror image of the panel (upside-down trunks, rocks and grass: the dark band seen whenever EBDX's camera
pulls back). Now:
  * the panel is extended upward with sky bands and the oak's crown painted in the panel's own canopy palette
    (no mirrored scenery anywhere above the horizon);
  * the room is split into room / clouds / sky-less front cut-out (see skies.py), so clouds only show in the sky;
  * pf_meadow_clouds is a wide strip of separated, soft-shaded cumulus that drifts slowly and follows the camera
    by a fraction (:parallax), smaller and fainter toward the horizon;
  * the night room gets its own moonlit clouds and cut-out (<name>_night, picked by the Bridge).
"""
import math, random
import numpy as np
from PIL import Image, ImageDraw
import fields_e
from bblib import *
from paint import *
from props import *
from rubygen import S
from skies import *
from fields_a import OWN

MAGI = fields_e.MAGI
MAGI_PNG = fields_e.MAGI_PNG

# Magiscarf day panel colours (the night panel is a 1:1 palette swap of it)
SKY_DAY = [(153, 217, 234), (175, 239, 207), (213, 243, 199), (234, 238, 176)]
SKY_EXT_DAY = [(141, 209, 233), (130, 201, 231)]            # deeper blues painted above the panel
SKY_EXT_NIGHT = [(100, 113, 230), (92, 104, 221)]
LEAF = {"dark": (31, 104, 42), "mid": (58, 131, 46), "light": (70, 155, 55), "speck": (122, 194, 69),
        "bark": (114, 100, 56), "bark_dark": (96, 79, 43)}
STARS = [(149, 158, 241), (193, 254, 229), (230, 253, 218)]
EXT = 75                                                    # art rows added above the 144-row panel
ORIGIN = (110, 150)                                         # HD position of the panel's top-left (as before)

NIGHT_CLOUD = [(178, 184, 246), (156, 164, 240), (138, 146, 232), (122, 130, 222), (110, 118, 214)]


def _panels():
    sheet = Image.open(MAGI_PNG).convert("RGBA")
    return sheet.crop((0, 160, 256, 304)), sheet.crop((272, 160, 528, 304))


def _palette_map(day, night):
    a, b = np.asarray(day.convert("RGB")), np.asarray(night.convert("RGB"))
    m = {}
    for p, q in zip(a.reshape(-1, 3), b.reshape(-1, 3)):
        m.setdefault(tuple(int(v) for v in p), tuple(int(v) for v in q))
    return m


def _crown(canvas, seed=411):
    """Paint the oak's crown above the panel (canvas = extended panel, panel row 0 at y = EXT).
    Leaf clumps in the panel's palette, painted bottom to top so each clump's shaded underside falls on the
    clumps behind it (the panel's canopy reads the same way); the lowest clumps are plain light leaves so the
    crown runs into the panel's canopy top without a seam."""
    rng = random.Random(seed)
    d = ImageDraw.Draw(canvas)
    y0 = EXT
    # the branch that leaves the top of the panel at x~97, continued into the crown
    for k in range(18):
        x = 98 - k * 0.3
        d.line([(x - 1, y0 - k), (x + 1, y0 - k)], fill=C(LEAF["bark"]))
        d.point((x - 1.5, y0 - k), fill=C(LEAF["bark_dark"]))
    lobes = [(46, y0 - 6, 18, 12), (68, y0 - 22, 28, 22), (100, y0 - 34, 36, 32), (136, y0 - 22, 30, 22),
             (157, y0 - 6, 12, 10), (78, y0 - 56, 30, 24), (122, y0 - 58, 30, 24), (102, y0 - 84, 36, 28)]

    def inside(x, y):
        return any(((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1 for cx, cy, rx, ry in lobes)
    clumps = []
    for gy in range(-6, y0 + 6, 9):
        for gx in range(18, 184, 11):
            x, y = gx + rng.uniform(-5, 5) + (gy % 18) * 0.3, gy + rng.uniform(-4, 4)
            r = rng.choice((rng.uniform(5.0, 8.0), rng.uniform(7.0, 10.0), rng.uniform(9.0, 13.0)))
            if y + r > y0 + 4 or not inside(x, y):
                continue
            if y > y0 - 26 and not (29 + (y0 - y) * 0.15 < x < 164 + (y0 - y) * 0.12):
                continue                      # flanks start at the panel canopy's own edges
            if y + r > y0 - 3 and (x - r < 29 or x + r > 165):
                continue                      # nothing may overhang the panel's sky at the seam
            clumps.append((x, y, r))
    # seam: a row of small light clumps right on the panel's cut canopy top, so its straight edge never shows
    sx = 31.0
    while sx < 164:
        r = rng.uniform(3.5, 5.5)
        clumps.append((min(sx, 164 - r * 0.6), y0 - rng.uniform(1.0, 2.5), r))
        sx += rng.uniform(4.5, 7.0)
    clumps.sort(key=lambda c: -c[1])        # bottom first: upper clumps overlap the ones below
    L, M, D = C(LEAF["light"]), C(LEAF["mid"]), C(LEAF["dark"])
    for x, y, r in clumps:
        low = y > y0 - 9
        if not low:
            if rng.random() < 0.45:
                d.ellipse([x - r + 1, y - r + 3, x + r + 1, y + r + 3], fill=D)
            d.ellipse([x - r, y - r + 1.5, x + r, y + r + 1.5], fill=M)
        d.ellipse([x - r, y - r, x + r, y + r - 1], fill=L)
        # lumpy outline: a smaller lobe on one shoulder
        sx = x + rng.choice((-1, 1)) * r * rng.uniform(0.45, 0.7)
        sr = r * rng.uniform(0.45, 0.6)
        d.ellipse([sx - sr, y - r * 0.55 - sr, sx + sr, y - r * 0.55 + sr], fill=L)
        # a mid-green fold on the clump's lower right, and leaf-tip jaggies on its upper rim
        if not low and r > 7:
            d.pieslice([x - r * 0.7, y - r * 0.2, x + r * 0.9, y + r * 0.9], 10, 80, fill=M)
        for _ in range(3):
            ang = rng.uniform(math.pi * 1.05, math.pi * 1.95)
            d.point((x + math.cos(ang) * (r + 0.5), y + math.sin(ang) * (r + 0.5)), fill=L)
        for _ in range(rng.randint(0, 2)):
            d.point((x + rng.uniform(-r, r) * 0.5, y - r * rng.uniform(0.2, 0.6)), fill=C(LEAF["speck"]))
    return clumps


def extended_panels():
    """(day, night) extended panels (256 x 144+EXT art px): sky bands + crown above the original panel."""
    day, night = _panels()
    pmap = _palette_map(day, night)
    W, H = day.width, day.height + EXT
    ext = Image.new("RGBA", (W, H), C(SKY_DAY[0]))
    d = ImageDraw.Draw(ext)
    # zenith bands (stepped, with a 2-row checker at each step, as the panel's own bands are flat)
    for y in range(EXT):
        band = 0 if y >= EXT - 22 else (1 if y >= EXT - 46 else 2)
        col = SKY_DAY[0] if band == 0 else SKY_EXT_DAY[band - 1]
        d.line([(0, y), (W, y)], fill=C(col))
    for yb, col in ((EXT - 22, SKY_DAY[0]), (EXT - 46, SKY_EXT_DAY[0])):
        for y in (yb - 1, yb - 2):
            for x in range((y % 2), W, 2):
                d.point((x, y), fill=C(col))
    ext.alpha_composite(day, (0, EXT))
    _crown(ext)
    # repair: the crown is only allowed to change canopy pixels inside the panel (never its sky)
    a = np.asarray(ext).copy()
    p = np.asarray(day)
    band = a[EXT:EXT + 6]
    src = p[:6]
    sky0 = np.zeros(src.shape[:2], bool)
    for c in SKY_DAY:
        sky0 |= np.all(src[..., :3] == c, -1)
    band[sky0] = src[sky0]
    a[EXT:EXT + 6] = band
    a[EXT + 6:] = p[6:]
    ext = Image.fromarray(a, "RGBA")
    # night: palette swap of the same pixels (+ the night-only zenith blues and some stars)
    extra = {tuple(SKY_EXT_DAY[i]): tuple(SKY_EXT_NIGHT[i]) for i in range(2)}
    pmap.update(extra)
    na = np.asarray(ext.convert("RGB")).copy()
    flat = na.reshape(-1, 3)
    keys = {}
    for i, px in enumerate(map(tuple, flat)):
        q = keys.get(px)
        if q is None:
            q = pmap.get(px, px)
            keys[px] = q
        flat[i] = q
    na = flat.reshape(na.shape)
    na[EXT:] = np.asarray(night.convert("RGB"))[:]            # the panel itself: exactly the night panel
    nimg = Image.fromarray(na, "RGB").convert("RGBA")
    rng = random.Random(77)
    nd = ImageDraw.Draw(nimg)
    sky_n = {pmap[c] for c in SKY_DAY} | set(SKY_EXT_NIGHT)
    for _ in range(46):
        x, y = rng.randrange(W), rng.randrange(EXT - 2)
        if tuple(nimg.getpixel((x, y))[:3]) in sky_n:
            nd.point((x, y), fill=C(STARS[rng.randrange(3)]))
    return ext, nimg


def sky_mask_art(ext_day):
    a = np.asarray(ext_day.convert("RGB"))
    m = np.zeros(a.shape[:2], bool)
    for c in SKY_DAY + SKY_EXT_DAY:
        m |= np.all(a == c, -1)
    return m


def to_hd(ext_art, blur=True):
    """Extended panel -> HD canvas: 2x pixels at ORIGIN (top row lands on HD y 0), sides mirrored and floor
    continued exactly as bblib.extend_vanilla does for every vanilla room."""
    bg = ext_art.resize((ext_art.width * 2, ext_art.height * 2), Image.NEAREST)
    oy = ORIGIN[1] - 2 * EXT
    assert oy == 0, oy
    return extend_vanilla(bg, origin=(ORIGIN[0], oy), blur_out=blur)


def mask_hd(mask_art):
    m = Image.fromarray((mask_art * 255).astype(np.uint8)).convert("RGBA")
    hd = to_hd(m, blur=False)
    a = np.asarray(hd, np.float32)[..., 0] / 255.0
    a[2 * (EXT + 144) - 40:, :] = 0                           # floor continuation never holds sky
    return (a > 0.5).astype(np.float32)


def _night_like(F, tag, im, mul=None):
    """Save pf_<F>_<tag>_night cropped exactly like paint.layer crops the day version (same pivot)."""
    bb = im.getchannel("A").getbbox()
    if bb:
        pad = 2
        im = im.crop((max(bb[0] - pad, 0), max(bb[1] - pad, 0), min(bb[2] + pad, im.width), min(bb[3] + pad, im.height)))
    if mul:
        im = grade(im, mul=mul)
    save_element("pf_%s_%s_night" % (F, tag), im)


def meadow_clouds(palette, seed, opacity=1.0):
    """1152 x 232 HD strip (576 x 116 art px). Big clouds high (in view when EBDX's camera pulls back), small and
    faint ones low over the hills (in the default view's sky gap); nothing below the aqua band."""
    rows = [(26, 3, (56, 78), 1.0 * opacity), (50, 4, (40, 58), 1.0 * opacity), (74, 4, (30, 44), 1.0 * opacity),
            (95, 5, (20, 32), 0.95 * opacity), (106, 6, (11, 19), 0.75 * opacity)]
    art = cloud_strip(576, 116, rows, seed=seed, palette=palette, fade=(100, 113))
    hd = art.resize((1152, 232), Image.NEAREST)
    return soften_top(hd, 0)


def meadow():
    F = "meadow"
    ext_day, ext_night = extended_panels()
    msk = mask_hd(sky_mask_art(ext_day))
    hd = to_hd(ext_day)
    hd = blend(hd, vgradient(HD, [(0, (255, 240, 180, 80)), (0.5, (255, 250, 200, 0)), (1, (20, 60, 20, 40))]),
               "softlight")
    wm = fields_e.windmill(64)
    paste(hd, wm, 612, 268, "bottom")
    flowers_scatter(hd, (110, 300, 864, 693), 700, [(255, 255, 255), (255, 224, 80), (214, 150, 250), (255, 150, 180)],
                    seed=404, size=(1.5, 3.5))
    wa = np.zeros(HD[::-1], np.float32)
    wx, wy = int(round(612 - wm.width / 2)), 268 - wm.height
    wa[wy:wy + wm.height, wx:wx + wm.width] = np.asarray(wm, np.float32)[..., 3] / 255.0
    msk = msk * (wa < 0.5)
    save_room("field_meadow", hd)
    hn = to_hd(ext_night)
    paste(hn, grade(wm, mul=(0.5, 0.5, 0.8)), 612, 268, "bottom")
    save_room("field_meadow_night", hn)
    front = front_spec("pf_meadow_front", cutout(hd, msk), z=1)
    save_element("pf_meadow_front_night", cutout(hn, msk))
    clouds = sky_strip_spec("pf_meadow_clouds", meadow_clouds(DAY_CLOUD, seed=4061), -144, 0, speed=0.17,
                            direction=1, z=0, parallax=(0.35, 0.18))
    save_element("pf_meadow_clouds_night", meadow_clouds(NIGHT_CLOUD, seed=4061, opacity=0.8))
    # everything else as in round 2 (fields_e.meadow): sails, light shafts, grass clumps, breeze, pollen
    layers = [layer(F, "sails", onto(fields_e.sails(26), 612 - 28, 268 - 58 - 28), anchor=(612, 268 - 58), z=1,
                    anim=S("rotate"), speed=0.8)]
    for i, (x, ang) in enumerate(((300, 62), (430, 68), (560, 74))):
        layers.append(layer(F, "shaft%d" % i, cone(HD, (x - 200, 60), 10, 640, (255, 248, 200), alpha=60, angle=ang),
                            z=2, blend=1, anim=S("pulse"), min=20, max=80, period=190 + i * 60, phase=i * 1.9))
    gcol = ((62, 150, 62), (96, 184, 76), (150, 210, 100))
    for i, (x, y, w, h, z) in enumerate(((200, 336, 60, 50, 2), (700, 340, 64, 52, 2), (90, 566, 150, 150, 24),
                                         (190, 610, 110, 120, 24), (820, 606, 150, 160, 24), (690, 656, 110, 110, 24),
                                         (430, 680, 120, 90, 24))):
        t = grass_tuft(w, h, colors=gcol, seed=i)
        layers.append(layer(F, "grass%d" % i, onto(t, x - w / 2, y - h), anchor=(x, y), z=z, anim=S("sway"),
                            amp=3 + (z > 10) * 2, period=110 + i * 9, phase=i * 0.4))
    extras = {"img001": clouds,
              "img002": strip(F, "breeze", fog_strip(864, 90, (255, 255, 230), seed=405, scale=14, density=0.4,
                                                     alpha=50), 300, speed=2, direction=1, z=3),
              "img003": front}
    # night versions of the day-lit layers (the Bridge picks <bitmap>_night with the *_night room)
    save_element("pf_meadow_breeze_night", fog_strip(864, 90, (180, 190, 255), seed=405, scale=14, density=0.4,
                                                      alpha=40))
    _night_like(F, "sails", onto(fields_e.sails(26), 612 - 28, 268 - 58 - 28), mul=(0.5, 0.5, 0.8))
    for i, (x, ang) in enumerate(((300, 62), (430, 68), (560, 74))):
        _night_like(F, "shaft%d" % i, cone(HD, (x - 200, 60), 10, 640, (170, 182, 255), alpha=34, angle=ang))
    for i, (x, y, w, h, z) in enumerate(((200, 336, 60, 50, 2), (700, 340, 64, 52, 2), (90, 566, 150, 150, 24),
                                         (190, 610, 110, 120, 24), (820, 606, 150, 160, 24), (690, 656, 110, 110, 24),
                                         (430, 680, 120, 90, 24))):
        t = grass_tuft(w, h, colors=gcol, seed=i)
        _night_like(F, "grass%d" % i, onto(t, x - w / 2, y - h), mul=(0.68, 0.64, 0.78))
    fx = [P(type=":drift", count=18, shape=":dot", size=2, colors=[[255, 255, 220], [255, 240, 160]], dir=1,
            speed=[0.6, 1.4], sway=14, zoom=[0.5, 0.9], opacity=[170, 240], layers=[":back", ":mid", ":front"], blend=1),
          P(type=":drift", count=8, shape=":dot", size=3, colors=[[255, 200, 220], [255, 240, 140], [210, 170, 255]],
            dir=1, speed=[0.6, 1.2], sway=16, zoom=[0.6, 1.0], opacity=[200, 255], spin=6, layers=[":mid", ":front"]),
          P(type=":drift", count=3, shape=":spark", size=5, colors=[[255, 240, 120], [255, 255, 255]],
            speed=[0.3, 0.6], sway=20, zoom=[0.6, 0.9], opacity=[200, 255], layers=[":mid"])]
    return {"profile": {S("art_extras"): extras, S("layers"): layers, S("fx"): fx},
            "origins": [[MAGI, "day-with-trees panel at 2x (room), night panel (field_meadow_night)"],
                        [OWN, "zenith sky and the oak's crown above the panel, sky-less front cut-out, drifting "
                              "cumulus (day and night), windmill with turning sails, light shafts, wildflowers, "
                              "swaying tall-grass clumps, breeze, pollen"]]}


BUILDERS = {"MEADOW": meadow}


#---------------------------------------------------------------------------------------------
# STORMFRONT: the scud strip was a band of flat slate blobs drawn over the mast, yard and rigging.
# Now: same airship-deck room, a sky-less front cut-out (deck, rail, mast, yard, shrouds) and ragged storm scud
# that races behind the rigging.
#---------------------------------------------------------------------------------------------
STORM_SCUD = [(152, 160, 180), (130, 138, 160), (110, 118, 142), (92, 100, 124), (78, 86, 110)]


def stormfront():
    import fields_b
    from fields_d import capture
    hd, res = capture(fields_b.stormfront, fields_b)
    save_room("field_stormfront", hd)
    # sky = everything above the rail's top bar, except the mast, its yard and the three shrouds (same geometry as
    # fields_b.stormfront draws them)
    deck_y = 150 + 190
    mx = 250
    m = Image.new("L", HD, 0)
    d = ImageDraw.Draw(m)
    d.rectangle([0, 0, 864, deck_y - 39], fill=255)
    d.rectangle([mx - 8, 0, mx + 8, deck_y], fill=0)
    d.rectangle([mx - 61, 79, mx + 61, 89], fill=0)
    for tx in (60, 420, 520):
        d.line([(mx, 30), (tx, deck_y - 36)], fill=0, width=4)
    msk = np.asarray(m, np.float32) / 255.0
    front = front_spec("pf_stormfront_front", cutout(hd, msk, soft=False), z=1)
    rows = [(80, 3, (170, 240), 0.78), (165, 3, (120, 180), 0.74), (235, 4, (80, 120), 0.68), (280, 5, (46, 76), 0.58)]
    scud = cloud_strip(1152, 300, rows, seed=815, palette=STORM_SCUD, fade=(272, 298), flat=0.27, jitter=16)
    extras = res["profile"][S("art_extras")]
    extras["img001"] = sky_strip_spec("pf_stormfront_scud", soften_top(scud, 0), -144, 0, speed=1, direction=-1, z=0,
                                      parallax=(0.3, 0.15))
    extras["img003"] = front
    res["origins"] = [o if o[0] != OWN else [OWN, o[1].replace("scud clouds", "storm scud racing behind the rigging, "
                                                                "sky-less front cut-out")] for o in res["origins"]]
    return res


BUILDERS["STORMFRONT"] = stormfront
