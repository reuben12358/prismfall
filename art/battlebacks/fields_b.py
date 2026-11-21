"""Nature / water / sky fields."""
from bblib import *
from paint import *
from props import *
from rubygen import S
from fields_a import vanilla, plat_pair, sky, REJ, REB, DES, EBDX, OWN, O


#---------------------------------------------------------------------------------------------
# SILKWOOD
#---------------------------------------------------------------------------------------------
def silk_wrap(canvas, center, rx, ry, seed=0, n=9, color=(250, 250, 240)):
    rng = random.Random(seed)
    d = ImageDraw.Draw(canvas)
    for i in range(n):
        a0 = rng.uniform(0, math.pi)
        x0 = center[0] + math.cos(a0) * rx
        x1 = center[0] - math.cos(a0 + rng.uniform(-0.4, 0.4)) * rx
        y0 = center[1] - ry * rng.uniform(0.2, 0.9)
        y1 = center[1] + ry * rng.uniform(0.3, 1.0)
        d.line([(x0, y0), ((x0 + x1) / 2, (y0 + y1) / 2 + ry * 0.3), (x1, y1)], fill=C(color, 140), width=1)
    d.arc([center[0] - rx - 2, center[1] - ry - 2, center[0] + rx + 2, center[1] + ry + 2], 0, 180,
          fill=C(color, 200), width=2)


def cocoon(h=34):
    im = Image.new("RGBA", (16, h + 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.line([8, 0, 8, 20], fill=(250, 250, 240, 170))
    d.ellipse([2, 18, 14, 18 + h], fill=C((236, 232, 214)), outline=C((90, 84, 70)))
    for y in range(22, 18 + h, 5):
        d.line([3, y, 13, y + 2], fill=C((196, 190, 168)))
    d.line([5, 22, 5, 14 + h], fill=C((255, 255, 250)))
    return im


def silkwood():
    F = "silkwood"
    hd = vanilla("rejuvenation", "Forest", base=False)
    hd = grade(hd, mul=(1.0, 1.02, 0.9), sat=1.05)
    stump_platform(hd, FOE, 116, 25)
    stump_platform(hd, PLAYER, 232, 50, thick=24)
    hd = blend(hd, vgradient(HD, [(0, (255, 220, 120, 70)), (0.45, (200, 230, 120, 0)), (1, (20, 40, 20, 60))]),
               "softlight")
    silk_wrap(hd, FOE, 120, 26, seed=1)
    silk_wrap(hd, PLAYER, 240, 52, seed=2, n=14)
    webs = blank()
    dew = []
    for (cx, cy, sz, seed) in ((250, 200, 180, 1), (700, 190, 200, 2), (470, 160, 90, 3), (120, 470, 240, 4),
                               (820, 500, 220, 5)):
        w, drops = web(sz, spokes=14 if sz > 150 else 10, rings=12 if sz > 150 else 7, seed=seed, alpha=135)
        webs.alpha_composite(w, (int(cx - sz / 2), int(cy - sz / 2)))
        dew += [(cx - sz / 2 + x, cy - sz / 2 + y) for x, y in drops]
    # silk curtains between trunks (diagonal sheets)
    d = ImageDraw.Draw(webs)
    rng = random.Random(7)
    for k in range(40):
        x0 = rng.uniform(170, 320); x1 = x0 + rng.uniform(80, 200)
        y0 = rng.uniform(150, 200)
        d.line([(x0, y0), ((x0 + x1) / 2, y0 + rng.uniform(20, 50)), (x1, y0 + rng.uniform(-10, 10))],
               fill=(255, 255, 248, 70))
    for k in range(40):
        x0 = rng.uniform(560, 680); x1 = x0 + rng.uniform(60, 160)
        y0 = rng.uniform(150, 210)
        d.line([(x0, y0), ((x0 + x1) / 2, y0 + rng.uniform(20, 50)), (x1, y0 + rng.uniform(-10, 10))],
               fill=(255, 255, 248, 70))
    hd.alpha_composite(webs)
    save_room("field_silkwood", hd)
    dm = np.zeros((693, 864), np.float32)
    for (x, y) in dew:
        if 0 <= int(y) < 693 and 0 <= int(x) < 864:
            dm[int(y), int(x)] = 1
    layers = [layer(F, "dew", glow_from_mask(dm, (255, 255, 230), radius=2, gain=2.0, core=1.0), z=1, blend=1,
                    anim=S("pulse"), min=40, max=220, period=60)]
    for i, (x, y, L) in enumerate(((330, 150, 120), (410, 150, 70), (620, 150, 140), (690, 150, 60), (230, 150, 90))):
        st = strand(L, sag=0)
        im = blank(); paste(im, st, x - st.width / 2, y)
        layers.append(layer(F, "strand%d" % i, im, anchor=(x, y), z=2, anim=S("sway"), amp=4, period=140 + i * 23))
    for i, (x, y) in enumerate(((290, 150), (650, 150))):
        cc = cocoon()
        layers.append(layer(F, "cocoon%d" % i, onto(cc, x - cc.width / 2, y), anchor=(x, y), z=2, anim=S("sway"),
                            amp=3, period=180 + i * 41))
    layers.append(layer(F, "canopy", soft_glow((520, 160), 300, (255, 230, 140), alpha=90, squash=0.6), z=2, blend=1,
                        anim=S("pulse"), min=30, max=90, period=200))
    extras = {"lightsC": True,
              "img001": ebdx_stock("forestShade", z=1, flat=True, oy=0, y=94, sheet=True, frames=2, speed=16,
                                   opacity=120)}
    fx = [P(type=":drift", count=12, shape=":rect", w=7, h=1, colors=[[255, 255, 245]], speed=[0.3, 0.7], sway=8,
            zoom=[0.6, 1.0], opacity=[90, 170], layers=[":back", ":mid", ":front"]),
          P(type=":rise", count=12, shape=":dot", size=3, colors=[[200, 255, 160], [240, 255, 200], [170, 230, 120]],
            speed=[0.3, 0.7], sway=10, zoom=[0.4, 0.8], opacity=[120, 200], layers=[":back", ":mid"], blend=1),
          P(type=":twinkle", count=8, shape=":spark", size=5, colors=[[255, 255, 230]], area=[60, 50, 330, 230],
            speed=[3, 6], zoom=[0.4, 0.8], opacity=[150, 255], layers=[":back"], blend=1)]
    return {"profile": {S("art_extras"): extras, S("layers"): layers, S("fx"): fx},
            "origins": [[REJ, "battlebgForest (graded green-gold)"],
                        [EBDX, "forestShade, lightsC"],
                        [OWN, "orb webs with dew, silk curtains, silk-wrapped stump platforms, hanging strands and cocoons"]]}


#---------------------------------------------------------------------------------------------
# FLOWER_GARDEN (5 stages, identical composition)
#---------------------------------------------------------------------------------------------
def big_bloom(r=70, petals=(255, 120, 190), center=(255, 220, 90), outline=(90, 30, 60)):
    size = 2 * r + 10
    im = Image.new("RGBA", (size, size + 120), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = size / 2
    d.line([(c, c), (c + 6, size + 118)], fill=C((40, 90, 40)), width=9)
    d.line([(c, c), (c + 6, size + 118)], fill=C((80, 150, 70)), width=5)
    for i in range(10):
        a = i / 10 * 2 * math.pi
        px, py = c + math.cos(a) * r * 0.55, c + math.sin(a) * r * 0.55
        d.ellipse([px - r * 0.48, py - r * 0.3, px + r * 0.48, py + r * 0.3], fill=C(petals), outline=C(outline))
    for i in range(10):
        a = (i + 0.5) / 10 * 2 * math.pi
        px, py = c + math.cos(a) * r * 0.4, c + math.sin(a) * r * 0.4
        d.ellipse([px - r * 0.3, py - r * 0.2, px + r * 0.3, py + r * 0.2], fill=C(lighter(petals, 0.3)),
                  outline=C(outline))
    d.ellipse([c - r * 0.28, c - r * 0.28, c + r * 0.28, c + r * 0.28], fill=C(center), outline=C(outline))
    rng = random.Random(1)
    for _ in range(20):
        a = rng.random() * 2 * math.pi; rr = rng.random() * r * 0.22
        d.point((c + math.cos(a) * rr, c + math.sin(a) * rr), fill=C(darker(center, 0.7)))
    return im


def flower_garden():
    F = "flower_garden"
    out = None
    stages = {}
    for st in range(1, 6):
        hd = vanilla("reborn", "FlowerGarden%d" % (st - 1))
        if st <= 2:
            # a promising garden, not a gloomy one: sunlit soil and fresh green, beds full of buds
            hd = grade(hd, mul=(1.3, 1.32, 1.12) if st == 1 else (1.12, 1.3, 1.1), gamma=0.72 if st == 1 else 0.8)
            hd = blend(hd, vgradient(HD, [(0, (255, 240, 170, 110)), (0.5, (255, 240, 170, 30)), (1, (0, 0, 0, 0))]),
                       "softlight")
            flowers_scatter(hd, (0, 300, 864, 693), 140 if st == 1 else 260,
                            [(150, 210, 110), (190, 230, 130), (255, 190, 210), (255, 240, 170)], seed=st, size=(2, 4))
            ring_stones(hd, FOE, 120, 26, [(140, 200, 100), (255, 180, 200), (190, 230, 130)], n=14, size=(4, 6),
                        seed=st, outline=(50, 80, 40))
        if st >= 3:
            cols = [(255, 150, 200), (255, 240, 120), (190, 150, 255), (255, 255, 255), (255, 120, 120)]
            n = {3: 18, 4: 26, 5: 34}[st]
            ring_stones(hd, FOE, 120, 26, cols, n=n, size=(5, 8), seed=st, outline=(60, 40, 50))
            ring_stones(hd, PLAYER, 240, 52, cols, n=n + 10, size=(8, 13), seed=st + 10, outline=(60, 40, 50))
        if st == 5:
            bloom = big_bloom(78)
            paste(hd, bloom, 610, 330, "bottom")
        name = "field_flower_garden" + ("" if st == 1 else "_%d" % st)
        save_room(name, hd)
        layers = []
        if st >= 2:
            sun = cone(HD, (720, 0), 30, 560, (255, 250, 200), alpha=40 + st * 10, angle=112)
            layers.append(layer("%s%d" % (F, st), "sun", sun, z=2, blend=1, anim=S("pulse"), min=30 + st * 6,
                                max=60 + st * 12, period=200))
        if st == 5:
            layers.append(layer("%s%d" % (F, st), "glow", soft_glow((610, 200), 160, (255, 200, 230), alpha=140),
                                z=1, blend=1, anim=S("pulse"), min=40, max=140, period=120))
        stages[st] = layers
    prof = {S("layers"): stages[1], S("stages"): {st: {S("layers"): stages[st]} for st in range(2, 6)}}
    return {"profile": prof,
            "origins": [[REB, "battlebgFlowerGarden0-4, enemybaseFlowerGarden0-4 (one per stage)"],
                        [OWN, "sunlit bud-filled beds (stages 1-2), flower rings round the platforms, giant bloom (stage 5), sunbeams"]]}


#---------------------------------------------------------------------------------------------
# FAIRY_TALE
#---------------------------------------------------------------------------------------------
def castle(w=150, h=120, color=(120, 90, 150), roof=(70, 50, 120), outline=(40, 26, 60), win=(255, 220, 140)):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    wins = []
    towers = [(0.12, 0.55, 0.11), (0.32, 0.3, 0.12), (0.5, 0.12, 0.14), (0.68, 0.34, 0.12), (0.88, 0.5, 0.11)]
    d.rectangle([w * 0.15, h * 0.6, w * 0.85, h], fill=C(color), outline=C(outline))
    for x in range(int(w * 0.15), int(w * 0.85), 8):
        d.rectangle([x, h * 0.6 - 5, x + 4, h * 0.6], fill=C(color), outline=C(outline))
    for (cx, top, tw) in towers:
        x0, x1 = w * (cx - tw / 2), w * (cx + tw / 2)
        d.rectangle([x0, h * (top + 0.12), x1, h], fill=C(color), outline=C(outline))
        d.polygon([(x0 - 3, h * (top + 0.12)), (x1 + 3, h * (top + 0.12)), ((x0 + x1) / 2, h * top - 6)],
                  fill=C(roof), outline=C(outline))
        d.line([((x0 + x1) / 2, h * top - 6), ((x0 + x1) / 2, h * top - 14)], fill=C(outline))
        d.polygon([((x0 + x1) / 2, h * top - 14), ((x0 + x1) / 2 + 7, h * top - 11), ((x0 + x1) / 2, h * top - 9)],
                  fill=C((255, 120, 160)))
        wy = h * (top + 0.25)
        d.rectangle([(x0 + x1) / 2 - 2, wy, (x0 + x1) / 2 + 2, wy + 6], fill=C(win))
        wins.append(((x0 + x1) / 2, wy + 3))
    d.chord([w * 0.44, h * 0.78, w * 0.56, h * 1.1], 180, 360, fill=C(outline))
    return im, wins


def mushroom(h, cap=(220, 50, 60), spots=(255, 240, 230), stem=(240, 228, 200), outline=(60, 20, 30)):
    w = int(h * 1.1)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([w * 0.38, h * 0.4, w * 0.62, h - 1], fill=C(stem), outline=C(outline))
    d.line([w * 0.42, h * 0.45, w * 0.42, h - 3], fill=C(lighter(stem, 0.5)))
    d.chord([1, 0, w - 2, h * 0.9], 180, 360, fill=C(cap), outline=C(outline))
    d.line([2, h * 0.45, w - 3, h * 0.45], fill=C(outline))
    rng = random.Random(h)
    for _ in range(5):
        x = rng.uniform(0.2, 0.8) * w; y = rng.uniform(0.1, 0.35) * h
        r = h * 0.06
        d.ellipse([x - r, y - r * 0.7, x + r, y + r * 0.7], fill=C(spots))
    d.arc([4, 3, w - 5, h * 0.85], 200, 250, fill=C(lighter(cap, 0.4)), width=2)
    return im


def fairy_tale():
    F = "fairy_tale"
    hd = vanilla("rejuvenation", "Meadow")
    cs, wins = castle(170, 128)
    paste(hd, cs, 470, 236, "bottom")
    hd = grade(hd, mul=(1.04, 0.96, 1.04))
    hd = blend(hd, vgradient(HD, [(0, (255, 170, 120, 90)), (0.5, (255, 160, 200, 30)), (1, (90, 40, 110, 70))]),
               "softlight")
    for (x, y, h, cap) in ((300, 330, 54, (220, 60, 80)), (330, 336, 34, (240, 120, 60)), (735, 330, 64, (190, 80, 200)),
                           (90, 600, 120, (220, 60, 80)), (800, 640, 100, (240, 120, 60))):
        paste(hd, mushroom(h, cap=cap), x, y, "bottom")
    ring_stones(hd, FOE, 118, 26, [(230, 70, 90), (250, 240, 230), (200, 90, 210)], n=16, size=(6, 9), seed=3,
                outline=(70, 30, 50))
    save_room("field_fairy_tale", hd)
    wm = np.zeros((693, 864), np.float32)
    for (wx, wy) in wins:
        wm[int(236 - 128 + wy), int(470 - 85 + wx)] = 1
    layers = [layer(F, "windows", glow_from_mask(wm, (255, 220, 140), radius=4, gain=3.0, core=1.0), z=1, blend=1,
                    anim=S("pulse"), min=80, max=220, period=90)]
    for i, (x, y) in enumerate(((260, 250), (690, 230), (420, 210), (180, 420), (760, 420))):
        g = soft_glow((x, y), 18, (255, 230, 160), alpha=220)
        layers.append(layer(F, "wisp%d" % i, g, z=2 if y < 400 else 26, blend=1, anim=[S("pulse"), S("bob")], amp=6,
                            min=80, max=220, period=100 + i * 17, phase=i))
    fx = [P(type=":rise", count=16, shape=":spark", size=5, colors=[[255, 180, 230], [255, 240, 160], [255, 255, 255]],
            speed=[0.3, 0.7], sway=12, zoom=[0.5, 1.0], opacity=[170, 255], layers=[":back", ":mid", ":front"], blend=1),
          P(type=":fall", count=10, shape=":dot", size=3, colors=[[255, 170, 210], [255, 220, 235]], speed=[0.4, 0.8],
            sway=16, zoom=[0.6, 1.0], opacity=[200, 255], spin=6, layers=[":back", ":mid", ":front"])]
    return {"profile": {S("layers"): layers, S("fx"): fx},
            "origins": [[REJ, "battlebgMeadow, enemybaseMeadow (twilight grade)"],
                        [OWN, "storybook castle, giant mushrooms, fairy ring, lantern wisps"]]}


#---------------------------------------------------------------------------------------------
# WATER_SURFACE / UNDERWATER / BEACH
#---------------------------------------------------------------------------------------------
def piling(h, w=10, wood=(96, 72, 54), outline=(30, 20, 14), wet=(60, 70, 70)):
    im = Image.new("RGBA", (w + 4, h + 6), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([2, 2, w + 1, h], fill=C(wood), outline=C(outline))
    d.rectangle([2, h * 0.6, w + 1, h], fill=C(wet), outline=C(outline))
    d.line([4, 4, 4, h - 2], fill=C(lighter(wood, 0.3)))
    d.ellipse([0, h - 3, w + 3, h + 4], outline=C((220, 240, 250), 200))
    return im


def harbour(w=320, h=90, color=(70, 94, 112), outline=(40, 56, 70), win=(255, 220, 150)):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    rng = random.Random(4)
    x = 0
    while x < w - 60:
        bw = rng.randint(16, 30); bh = rng.randint(18, 40)
        d.rectangle([x, h - bh, x + bw, h], fill=C(color))
        d.polygon([(x - 2, h - bh), (x + bw + 2, h - bh), (x + bw / 2, h - bh - 10)], fill=C(darker(color, 0.85)))
        if rng.random() < 0.6:
            d.rectangle([x + bw / 2 - 1, h - bh + 6, x + bw / 2 + 1, h - bh + 9], fill=C(win))
        x += bw + rng.randint(0, 4)
    lx = w - 40
    d.polygon([(lx, h), (lx + 16, h), (lx + 12, h - 70), (lx + 4, h - 70)], fill=C((210, 214, 220)), outline=C(outline))
    for y in range(h - 60, h, 14):
        d.rectangle([lx + 3, y, lx + 13, y + 5], fill=C((200, 60, 60)))
    d.rectangle([lx + 2, h - 80, lx + 14, h - 70], fill=C((255, 240, 170)), outline=C(outline))
    d.polygon([(lx, h - 80), (lx + 16, h - 80), (lx + 8, h - 88)], fill=C(outline))
    return im, (lx + 8, h - 75)


def water_surface():
    F = "water_surface"
    hd = vanilla("reborn", "WaterSurface")
    hz = 150 + 86
    hb, beacon = harbour()
    paste(hd, posterize_alpha(hb, 2), 560, hz + 2, "bottom")
    rng = random.Random(6)
    for (x, y, h) in ((240, 330, 60), (262, 336, 46), (760, 320, 70), (690, 300, 40), (80, 520, 150), (14, 600, 120),
                      (840, 560, 130)):   # none inside the player's pool (bases.py)
        paste(hd, piling(h, 10 if h < 100 else 16), x, y, "bottom")
    hd = grade(hd, mul=(0.92, 1.0, 1.02))
    save_room("field_water_surface", hd)
    bx, by = 560 - 160 + beacon[0], hz + 2 - 90 + beacon[1]
    buoy = Image.new("RGBA", (26, 40), (0, 0, 0, 0)); d = ImageDraw.Draw(buoy)
    d.polygon([(5, 22), (21, 22), (17, 6), (9, 6)], fill=C((210, 60, 50)), outline=C((60, 16, 12)))
    d.rectangle([8, 12, 18, 16], fill=C((240, 240, 240)))
    d.ellipse([1, 20, 25, 32], fill=C((180, 40, 36)), outline=C((60, 16, 12)))
    d.line([13, 0, 13, 6], fill=C((40, 40, 40)), width=2)
    layers = [layer(F, "beacon", soft_glow((bx, by), 30, (255, 240, 170), alpha=255), z=1, blend=1,
                    anim=S("pulse"), min=0, max=255, period=80),
              layer(F, "buoy", onto(buoy, 330, 300), anchor=(343, 330), z=2, anim=[S("bob"), S("sway")], amp=2,
                    period=90),
              layer(F, "buoy2", onto(buoy, 800, 420), anchor=(813, 450), z=22, anim=[S("bob"), S("sway")], amp=3,
                    period=110)]
    glints = blank()
    gd = ImageDraw.Draw(glints)
    for _ in range(260):
        x, y = rng.uniform(0, 864), rng.uniform(hz + 6, 693)
        L = rng.uniform(3, 10) * (0.5 + (y - hz) / 300.0)
        gd.line([(x, y), (x + L, y)], fill=(230, 250, 255, 200))
    extras = {"img001": strip(F, "glints", glints.crop((0, hz, 864, 693)), hz, speed=0.5, direction=1, z=1,
                              opacity=150),
              "img002": strip(F, "spray", fog_strip(864, 80, (240, 250, 255), seed=61, scale=14, density=0.45,
                                                    alpha=110), hz - 30, speed=1, direction=-1, z=2)}
    fx = [P(type=":twinkle", count=14, shape=":spark", size=5, colors=[[255, 255, 255]], area=[0, 110, 384, 300],
            speed=[2, 5], zoom=[0.5, 0.9], opacity=[160, 255], layers=[":back", ":mid"], blend=1),
          P(type=":drift", count=6, shape=":rect", w=5, h=2, colors=[[250, 250, 250]], area=[0, 20, 384, 100],
            dir=-1, speed=[0.6, 1.0], sway=8, zoom=[0.6, 1.0], opacity=[180, 240], layers=[":back"])]
    return {"profile": {S("art_extras"): extras, S("layers"): layers, S("fx"): fx},
            "origins": [[REB, "battlebgWaterSurface, enemybaseWaterSurface"],
                        [OWN, "Ebbmouth harbour and lighthouse silhouette, drowned pilings, buoys, glint strip, spray"]]}


def kelp(h, color=(40, 120, 80), outline=(10, 40, 30), seed=0):
    rng = random.Random(seed)
    im = Image.new("RGBA", (40, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    pts = [(20 + 6 * math.sin(y / 18.0 + seed), y) for y in range(h, 0, -4)]
    d.line(pts, fill=C(outline), width=5)
    d.line(pts, fill=C(color), width=3)
    for i, (x, y) in enumerate(pts[2::3]):
        s = 1 if i % 2 else -1
        d.polygon([(x, y), (x + s * 14, y - 6), (x + s * 16, y - 2), (x, y + 5)], fill=C(lighter(color, 0.15)),
                  outline=C(outline))
    return im


def underwater():
    F = "underwater"
    hd = vanilla("reborn", "Underwater")
    d = ImageDraw.Draw(hd)
    for (x, top, w, broken) in ((300, 210, 26, True), (700, 190, 30, False), (760, 260, 24, True)):
        pillar(hd, x, top, 322, w, (110, 130, 140), (150, 170, 180), (70, 86, 96), (30, 40, 50), cap=not broken)
    sea = Image.new("RGBA", HD, (0, 0, 0, 0))
    rng = random.Random(3)
    for i in range(18):
        x = rng.uniform(0, 864)
        if 380 < x < 680:
            continue
        paste(hd, kelp(int(rng.uniform(80, 170)), seed=i), x, 330, "bottom")
    hd = grade(hd, mul=(0.9, 1.0, 1.05))
    save_room("field_underwater", hd)
    layers = []
    for i, (x, h) in enumerate(((120, 260), (200, 200), (790, 280), (840, 220))):
        k = kelp(h, (50, 140, 90), seed=20 + i)
        layers.append(layer(F, "kelp%d" % i, onto(k, x - 20, 693 - h), anchor=(x, 693), z=24, anim=S("sway"),
                            amp=3, period=120 + i * 21))
    for i, x in enumerate((250, 480, 700)):
        layers.append(layer(F, "ray%d" % i, cone(HD, (x + 80, -20), 12, 520, (180, 230, 255), alpha=70, angle=100),
                            z=2, blend=1, anim=S("pulse"), min=20, max=80, period=150 + i * 40, phase=i * 1.7))
    extras = {"bubbles": True, "lightsC": True,
              "img001": ebdx_stock("forestShade", z=1, flat=True, oy=0, y=94, sheet=True, frames=2, speed=16,
                                   opacity=90)}
    return {"profile": {S("art_extras"): extras, S("layers"): layers},
            "origins": [[REB, "battlebgUnderwater, enemybaseUnderwater"],
                        [EBDX, "bubbles, lightsC, forestShade (caustics)"],
                        [OWN, "sunken ruin columns, kelp forest (swaying), god rays"]]}


def pier(w=200, h=60, wood=(110, 80, 56), outline=(36, 24, 16)):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([0, h * 0.4, w, h * 0.5], fill=C(wood), outline=C(outline))
    for x in range(4, w, 18):
        d.rectangle([x, h * 0.5, x + 4, h], fill=C(darker(wood, 0.8)), outline=C(outline))
    # ferry
    d.polygon([(w * 0.55, h * 0.4), (w * 0.95, h * 0.4), (w * 0.9, h * 0.25), (w * 0.6, h * 0.25)], fill=C((240, 240, 236)),
              outline=C(outline))
    d.rectangle([w * 0.65, h * 0.08, w * 0.82, h * 0.25], fill=C((230, 230, 226)), outline=C(outline))
    d.rectangle([w * 0.72, 0, w * 0.76, h * 0.08], fill=C((200, 60, 50)), outline=C(outline))
    for x in range(int(w * 0.67), int(w * 0.8), 6):
        d.rectangle([x, h * 0.13, x + 3, h * 0.18], fill=C((120, 170, 210)))
    return im


def beach():
    F = "beach"
    bg = game_img("rejuvenation", "battlebgBeach")
    hd = extend_vanilla(bg, origin=O)
    paste(hd, pier(), 300, 150 + 100, "bottom")
    sand_top, sand_side = (238, 212, 168), (200, 166, 120)
    plat_pair(hd, sand_top, sand_side, speckle=([(220, 190, 140), (250, 236, 200), (255, 180, 170)], 140))
    d = ImageDraw.Draw(hd)
    for (x, y, rw) in ((200, 330, 40), (760, 340, 56), (40, 670, 90), (820, 600, 70)):   # off the player base
        d.ellipse([x - rw, y - rw * 0.35, x + rw, y + rw * 0.25], fill=C((120, 120, 128)), outline=C((50, 50, 60)))
        d.ellipse([x - rw * 0.7, y - rw * 0.3, x + rw * 0.3, y], fill=C((160, 160, 170)))
        d.ellipse([x + rw * 0.4, y, x + rw * 1.4, y + rw * 0.22], fill=C((90, 180, 210)), outline=C((60, 120, 150)))
    save_room("field_beach", hd)
    glints = blank(); gd = ImageDraw.Draw(glints)
    rng = random.Random(8)
    for _ in range(140):
        x, y = rng.uniform(0, 864), rng.uniform(0, 70)
        gd.line([(x, y), (x + rng.uniform(3, 8), y)], fill=(255, 255, 255, 220))
    gull = Image.new("RGBA", (16, 8), (0, 0, 0, 0)); g = ImageDraw.Draw(gull)
    g.line([(0, 2), (4, 0), (8, 4), (12, 0), (16, 2)], fill=(250, 250, 250, 255), width=2)
    layers = [layer(F, "gull%d" % i, onto(gull, x, y), anchor=(x + 8, y + 4), z=1, anim=[S("drift"), S("bob")],
                    amp=30, period=300 + i * 70, phase=i) for i, (x, y) in enumerate(((300, 170), (620, 190), (700, 160)))]
    extras = {"img001": strip(F, "glints", glints, 150 + 70, speed=0.5, direction=1, z=1, opacity=170),
              "img002": strip(F, "foam", fog_strip(864, 40, (255, 255, 255), seed=71, scale=8, density=0.5, alpha=150),
                              150 + 112, speed=1, direction=-1, z=1)}
    fx = [P(type=":twinkle", count=12, shape=":spark", size=5, colors=[[255, 255, 255]], area=[0, 95, 384, 125],
            speed=[2, 5], zoom=[0.5, 0.8], opacity=[150, 255], layers=[":back"], blend=1)]
    return {"profile": {S("art_extras"): extras, S("layers"): layers, S("fx"): fx},
            "origins": [[REJ, "battlebgBeach"],
                        [OWN, "ferry pier, sand platforms, tide-pool rocks, sea glints and foam, gulls"]]}


#---------------------------------------------------------------------------------------------
# STORMFRONT / RAINBOW
#---------------------------------------------------------------------------------------------
def stormfront():
    F = "stormfront"
    bg = game_img("desolation", "battlebgClouds")
    bg = gradient_map(bg, [(0, (14, 18, 30)), (0.35, (40, 50, 70)), (0.6, (82, 94, 116)), (0.85, (150, 160, 180)),
                           (1, (220, 226, 236))])
    hd = extend_vanilla(bg, origin=O)
    deck_y = 150 + 190
    deck = planks(HD, (96, 72, 54), (40, 28, 20), horizon_y=deck_y, vanish_x=520, n=22, seed=3)
    hd.alpha_composite(deck)
    d = ImageDraw.Draw(hd)
    d.rectangle([0, deck_y - 4, 864, deck_y + 2], fill=C((60, 44, 34)), outline=C((20, 14, 10)))
    for x in range(0, 864, 40):
        d.rectangle([x, deck_y - 34, x + 5, deck_y], fill=C((80, 60, 46)), outline=C((20, 14, 10)))
    d.rectangle([0, deck_y - 38, 864, deck_y - 33], fill=C((90, 68, 50)), outline=C((20, 14, 10)))
    # mast and rigging
    mx = 250
    d.rectangle([mx - 7, 0, mx + 7, deck_y], fill=C((84, 62, 46)), outline=C((24, 16, 10)))
    d.line([mx - 4, 0, mx - 4, deck_y], fill=C((120, 92, 68)))
    for tx in (60, 420, 520):
        d.line([(mx, 30), (tx, deck_y - 36)], fill=C((30, 24, 20)), width=2)
    d.rectangle([mx - 60, 80, mx + 60, 88], fill=C((84, 62, 46)), outline=C((24, 16, 10)))
    plat = (120, 126, 136)
    plat_pair(hd, plat, (70, 74, 84), outline=(24, 26, 30))
    for (cx, cy, rx, ry) in ((FOE[0], FOE[1], 118, 26), (PLAYER[0], PLAYER[1], 236, 52)):
        for k in range(8):
            a = k / 8 * 2 * math.pi
            d.ellipse([cx + math.cos(a) * rx * 0.8 - 2, cy + math.sin(a) * ry * 0.8 - 1,
                       cx + math.cos(a) * rx * 0.8 + 2, cy + math.sin(a) * ry * 0.8 + 1], fill=C((40, 42, 50)))
    save_room("field_stormfront", hd)
    pen = Image.new("RGBA", (70, 22), (0, 0, 0, 0)); pd = ImageDraw.Draw(pen)
    pd.polygon([(0, 0), (70, 6), (52, 11), (70, 16), (0, 22)], fill=C((200, 40, 50)), outline=C((60, 10, 14)))
    pd.line([(0, 11), (40, 11)], fill=C((240, 200, 80)), width=2)
    layers = [layer(F, "pennant", onto(pen, mx + 7, 6), anchor=(mx + 7, 17), z=2, anim=S("sway"), amp=8, period=40),
              layer(F, "lightning", soft_glow((600, 120), 300, (200, 210, 255), alpha=150, squash=0.6), z=1, blend=1,
                    anim=S("flicker"), opacity=0, min=150, chance=0.012, dropout=4)]
    scud = cloud_band(864, 120, (70, 80, 100), (40, 46, 60), seed=81, density=0.45, scale=22, alpha=200)
    extras = {"img001": strip(F, "scud", scud, 40, speed=3, direction=-1, z=1),
              "img002": strip(F, "mist", fog_strip(864, 140, (150, 160, 180), seed=82, scale=24, density=0.5,
                                                   alpha=90), 280, speed=4, direction=-1, z=26)}
    return {"profile": {S("art_extras"): extras, S("layers"): layers},
            "origins": [[DES, "battlebgClouds (gradient-mapped to storm)"],
                        [OWN, "airship deck, rail, mast and rigging, pennant, scud clouds, lightning glow"]]}


def make_cloud_strip():
    im = cloud_floor(864, 120, 40, seed=95, rmin=14, rmax=30, rows=2)
    a = arr(im)
    a[100:, :, 3] = 0
    return img(a)


def rainbow():
    F = "rainbow"
    hd = vanilla("reborn", "Rainbow")
    hd = grade(hd, sat=1.1, contrast=1.05)
    hd.alpha_composite(cloud_floor(864, 693, 150 + 140, seed=91, rmin=16, rmax=40, rows=6))
    eb = game_img("reborn", "enemybaseRainbow")
    place_foe_base(hd, eb); place_player_base_scaled(hd, eb)
    save_room("field_rainbow", hd)
    layers = [layer(F, "shimmer", soft_glow((470, 120), 420, (255, 255, 255), alpha=90, squash=0.5), z=1, blend=1,
                    anim=S("pulse"), min=20, max=90, period=160)]
    extras = {"img001": strip(F, "mist", fog_strip(864, 120, (255, 220, 250), seed=93, scale=20, density=0.5,
                                                   alpha=100), 260, speed=0.5, direction=1, z=2),
              "img002": strip(F, "clouds", make_cloud_strip(), 600, speed=1, direction=-1, z=26)}
    return {"profile": {S("art_extras"): extras, S("layers"): layers},
            "origins": [[REB, "battlebgRainbow, enemybaseRainbow"],
                        [OWN, "cloud-bank floor, prismatic mist, drifting foreground clouds"]]}


#---------------------------------------------------------------------------------------------
# CORROSIVE_MIRE
#---------------------------------------------------------------------------------------------
def corrosive_mire():
    F = "corrosive_mire"
    hd = vanilla("reborn", "Corrosive")
    hd = gradient_map(hd, [(0, (18, 12, 24)), (0.35, (60, 36, 70)), (0.6, (104, 64, 110)), (0.85, (150, 120, 140)),
                           (1, (200, 190, 170))])
    # undercity wall with drain pipes
    d = ImageDraw.Draw(hd)
    wall_b = 150 + 120
    for x in range(0, 864, 48):
        d.rectangle([x, 0, x + 47, wall_b], outline=C((30, 20, 34)))
    rust = (130, 74, 44)
    pipes = [(330, 150, 26), (620, 120, 34), (720, 200, 22)]
    for (x, y, w) in pipes:
        pipe(hd, [(x, 0), (x, y), (x + 30, y + 30), (x + 30, wall_b - 40)], w, rust, light=(190, 120, 70))
        d.ellipse([x + 30 - w / 2 - 4, wall_b - 46, x + 30 + w / 2 + 4, wall_b - 34], fill=C((40, 26, 20)),
                  outline=C((20, 12, 10)))
    sludge = (120, 200, 70)
    for (x, y, rx, ry) in ((360, 300, 60, 10), (660, 290, 90, 14), (200, 520, 120, 22), (760, 560, 110, 20)):
        d.ellipse([x - rx, y - ry, x + rx, y + ry], fill=C((80, 150, 50)), outline=C((30, 50, 20)))
        d.ellipse([x - rx * 0.7, y - ry * 0.7, x + rx * 0.2, y], fill=C(sludge))
        d.ellipse([x + rx * 0.1, y - ry * 0.3, x + rx * 0.5, y + ry * 0.2], fill=C((170, 110, 210)))
    for (x, y, w, h) in ((150, 330, 120, 90), (720, 320, 110, 80), (40, 640, 160, 140), (820, 660, 150, 150)):
        paste(hd, reeds(w, h, (70, 66, 50), (24, 20, 16), n=12, seed=x, heads=(80, 60, 50)), x, y, "bottom")
    plat_pair(hd, (70, 54, 66), (40, 30, 40), outline=(14, 10, 16),
              speckle=([(120, 200, 70), (90, 70, 90), (170, 110, 210)], 200),
              rim=(140, 230, 90))
    save_room("field_corrosive_mire", hd)
    sm = mask_from(hd, lambda r, g, b: (g > 140) & (r < 180) & (b < 120))
    layers = [layer(F, "sludgeglow", glow_from_mask(sm, (150, 255, 90), radius=10, gain=1.2), z=1, blend=1,
                    anim=S("pulse"), min=40, max=140, period=110)]
    im = blank(); ch = chain(60); lm = lamp((170, 255, 120))
    paste(im, ch, 470 - ch.width / 2, 0); paste(im, lm, 470 - lm.width / 2, 58)
    layers.append(layer(F, "lamp", im, anchor=(470, 0), z=3, anim=S("sway"), amp=3, period=170))
    layers.append(layer(F, "lampcone", cone(HD, (470, 80), 50, 300, (160, 255, 120), alpha=70), z=3, blend=1,
                        anim=[S("pulse"), S("flicker")], min=40, max=100, period=60, chance=0.02, dropout=5))
    goo = Image.new("RGBA", (14, 120), (0, 0, 0, 0)); gd = ImageDraw.Draw(goo)
    rng = random.Random(3)
    for y in range(0, 120, 2):
        w0 = 4 + 2 * math.sin(y / 9.0)
        gd.line([(7 - w0, y), (7 + w0, y)], fill=C((130, 210, 80), 230))
        if rng.random() < 0.2:
            gd.point((7 - w0 + 1, y), fill=C((210, 255, 170)))
    extras = {"bubbles": "bubbleDark"}
    for i, (x, y, w) in enumerate(pipes):
        gx = x + 30
        extras["img%03d" % (10 + i)] = {S("bitmap"): "pf_corrosive_mire_goo", S("scrolling"): True,
                                        S("vertical"): True, S("speed"): 2, S("direction"): -1,
                                        S("ox"): 7, S("oy"): 0, S("x"): round(gx / 2.25, 2),
                                        S("y"): round((wall_b - 34) / 2.25, 2), S("zoom"): INV, S("z"): 2}
    save_element("pf_corrosive_mire_goo", goo)
    extras["img020"] = strip(F, "fumes", fog_strip(864, 160, (130, 220, 100), seed=101, scale=26, density=0.55,
                                                   alpha=80), 230, speed=1, direction=1, z=4)
    fx = [P(type=":rise", count=18, shape=":glow", size=5, colors=[[190, 90, 230], [140, 220, 90], [220, 120, 255]],
            area=[0, 120, 384, 308], speed=[0.3, 0.8], sway=6, zoom=[0.4, 0.9], opacity=[140, 220],
            layers=[":back", ":mid", ":front"], blend=1),
          P(type=":fall", count=6, shape=":rect", w=2, h=3, colors=[[150, 230, 90]], area=[140, 0, 340, 120],
            speed=[1.5, 2.5], sway=0, zoom=[0.6, 1.0], opacity=[180, 240], layers=[":back"])]
    return {"profile": {S("art_extras"): extras, S("layers"): layers, S("fx"): fx},
            "origins": [[REB, "battlebgCorrosive (gradient-mapped)"],
                        [EBDX, "bubbleDark"],
                        [OWN, "undercity wall, rusted drain pipes with falling sludge, sludge pools, dead reeds, "
                              "sickly hanging lamp, fumes, sludge-rimmed platforms"]]}


BUILDERS = {"SILKWOOD": silkwood, "FLOWER_GARDEN": flower_garden, "FAIRY_TALE": fairy_tale,
            "WATER_SURFACE": water_surface, "UNDERWATER": underwater, "BEACH": beach, "STORMFRONT": stormfront,
            "RAINBOW": rainbow, "CORROSIVE_MIRE": corrosive_mire}
