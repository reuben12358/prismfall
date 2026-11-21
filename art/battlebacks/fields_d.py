"""Stage variants (Revision 10 field redesign) + WILDFIRE, and reworks of ASHEN_WASTE and INVERSE.
Variants reuse the stage-1 composition (captured from the base builder) so transitions read as the same place."""
import fields_a, fields_b, fields_c
from bblib import *
from paint import *
from props import *
from rubygen import S
from fields_a import vanilla, plat_pair, REJ, REB, DES, EBDX, OWN, O


def capture(builder, module):
    """Run a base builder without writing its room; return (hd, result)."""
    box = {}
    orig = module.save_room

    def fake(name, hd, out=OUT):
        box["hd"] = hd.convert("RGBA")
        return hd
    module.save_room = fake
    try:
        res = builder()
    finally:
        module.save_room = orig
    return box["hd"], res


def with_stages(base_builder, stages):
    def run():
        res = base_builder()
        res["profile"][S("stages")] = {}
        for n, fn in stages.items():
            sres = fn()
            res["profile"][S("stages")][n] = sres["profile"]
            res["origins"] = res["origins"] + [["stage %d" % n, sres["note"]]]
        return res
    return run


def keep(layers, *tags):
    return [l for l in layers if any(("_" + t) in l[S("bitmap")] for t in tags)]


#---------------------------------------------------------------------------------------------
# GRAND_STAGE 2 (Encore) / 3 (Standing Ovation)
#---------------------------------------------------------------------------------------------
def grand_stage_level(level):
    def run():
        hd, res = capture(fields_c.grand_stage, fields_c)
        F = "grand_stage%d" % level
        rng = random.Random(level)
        for _ in range(12 if level == 2 else 36):
            x = rng.uniform(170, 860); y = rng.uniform(380, 680)
            if abs(x - PLAYER[0]) < 250 and abs(y - PLAYER[1]) < 70:
                continue
            r = rose(rng.randint(10, 16)).rotate(rng.uniform(0, 360), expand=True, resample=Image.NEAREST)
            hd.alpha_composite(r, (int(x), int(y)))
        if level == 2:
            hd = grade(hd, mul=(1.1, 1.04, 0.98))
        else:
            hd = grade(hd, mul=(1.18, 1.1, 0.96))
            hd = blend(hd, vgradient(HD, [(0, (255, 210, 120, 90)), (1, (255, 180, 90, 40))]), "softlight")
        save_room("field_grand_stage_%d" % level, hd)
        layers = list(res["profile"][S("layers")])
        cols = [(255, 200, 220), (200, 220, 255)] if level == 2 else [(255, 220, 150), (255, 200, 230), (200, 230, 255)]
        for i, col in enumerate(cols):
            x = 250 + i * 260
            layers.append(layer(F, "sweep%d" % i, cone(HD, (x, 150), 16, 520, col, alpha=80, angle=90 + (i - 1) * 18),
                                anchor=(x, 150), z=2, blend=1, anim=S("sway"), amp=14, period=150 + i * 40,
                                phase=i * 2, opacity=200))
        if level == 3:
            layers.append(layer(F, "gold", soft_glow((520, 330), 420, (255, 210, 120), alpha=110, squash=0.5), z=1,
                                blend=1, anim=S("pulse"), min=50, max=120, period=70))
        n = 34 if level == 2 else 48
        fx = [P(type=":fall", count=n, shape=":rect", w=3, h=2, colors=PRISM, speed=[0.6, 1.3], sway=12,
                zoom=[0.6, 1.0], opacity=[200, 255], spin=8, layers=[":back", ":mid", ":front"])]
        if level == 3:
            fx.append(P(type=":fall", count=14, shape=":dot", size=3, colors=[[220, 30, 50], [255, 120, 140]],
                        speed=[0.5, 1.0], sway=14, zoom=[0.6, 1.0], opacity=[220, 255], spin=6,
                        layers=[":mid", ":front"]))
            fx.append(P(type=":twinkle", count=14, shape=":spark", size=5, colors=GOLD, speed=[3, 6],
                        zoom=[0.5, 0.9], opacity=[170, 255], layers=[":back", ":mid"], blend=1))
        note = ("Encore: roses on the boards, warmer house lights, sweeping coloured spots, heavier confetti"
                if level == 2 else
                "Standing Ovation: stage strewn with roses, golden flood light, three sweeping spots, "
                "confetti, rose petals and gold sparkle")
        return {"profile": {S("layers"): layers, S("fx"): fx}, "note": note}
    return run


#---------------------------------------------------------------------------------------------
# NEON_GRID 2: Blackout
#---------------------------------------------------------------------------------------------
def neon_blackout():
    hd, res = capture(fields_c.neon_grid, fields_c)
    F = "neon_grid_blackout"
    cyan = mask_from(hd, lambda r, g, b: (g > 180) & (b > 200) & (r < 140))
    hd = grade(hd, mul=(0.3, 0.32, 0.42), sat=0.5)
    a = arr(hd)
    a[cyan > 0] = [30, 46, 60, 255]          # dead circuitry
    hd = img(a)
    d = ImageDraw.Draw(hd)
    reds = []
    for (x, y) in ((205, 190), (300, 230), (640, 170), (760, 210), (470, 250)):
        d.rectangle([x - 3, y - 2, x + 3, y + 2], fill=C((255, 50, 40)), outline=C((60, 0, 0)))
        reds.append((x, y))
    save_room("field_neon_grid_blackout", hd)
    rm = np.zeros((693, 864), np.float32)
    for (x, y) in reds:
        rm[y - 2:y + 3, x - 3:x + 4] = 1
    sparks = blank(); sd = ImageDraw.Draw(sparks)
    rng = random.Random(4)
    pts = []
    for _ in range(6):
        x, y = rng.uniform(220, 760), rng.uniform(300, 640)
        for k in range(6):
            a0 = rng.uniform(0, 2 * math.pi); L = rng.uniform(6, 16)
            sd.line([(x, y), (x + math.cos(a0) * L, y + math.sin(a0) * L * 0.5)], fill=(200, 240, 255, 255))
        pts.append((x, y))
    layers = [layer(F, "alarm", glow_from_mask(rm, (255, 40, 30), radius=8, gain=2.0, core=1.0), z=1, blend=1,
                    anim=S("pulse"), min=20, max=220, period=60),
              layer(F, "sparks", sparks, z=2, blend=1, anim=S("flicker"), opacity=0, min=255, chance=0.06,
                    dropout=3),
              layer(F, "flicker", glow_from_mask(cyan * (noise(HD, 20, 5, 1) > 0.6), (80, 240, 255), radius=4,
                                                 gain=1.0, core=0.6), z=1, blend=1, anim=S("flicker"), opacity=0,
                    min=160, chance=0.02, dropout=5)]
    fx = [P(type=":streak", count=8, shape=":rect", w=10, h=1, colors=[[200, 240, 255], [255, 255, 200]],
            area=[60, 130, 330, 300], angle=8, speed=[8, 12], zoom=[0.6, 1.0], opacity=[180, 255],
            layers=[":back", ":mid"], blend=1),
          P(type=":twinkle", count=14, shape=":spark", size=5, colors=[[200, 240, 255], [255, 255, 255]],
            area=[40, 130, 340, 300], speed=[8, 14], zoom=[0.4, 0.8], opacity=[200, 255], layers=[":back", ":mid"],
            blend=1),
          P(type=":flash", color=[120, 200, 255], alpha=80, interval=[120, 260], decay=20, double=True)]
    return {"profile": {S("art_extras"): {}, S("layers"): layers, S("fx"): fx},
            "note": "Blackout: same rooftop with the grid dead - dark city, red emergency lamps, live sparks "
                    "crackling over the floor, a few circuits buzzing back"}


#---------------------------------------------------------------------------------------------
# DESERT 2: Superbloom
#---------------------------------------------------------------------------------------------
def desert_bloom():
    hd, res = capture(fields_a.desert, fields_a)
    F = "desert_bloom"
    hz = 150 + 96
    a = arr(hd)
    ys = np.arange(693)[:, None, None]
    wet = (ys > hz + 10) * 1.0
    a[..., :3] = a[..., :3] * (1 - 0.18 * wet) + np.array([20, 40, 10]) * 0.18 * wet
    hd = img(a)
    hd = blend(hd, vgradient(HD, [(0, (120, 190, 255, 120)), (0.3, (200, 230, 255, 0)), (1, (0, 0, 0, 0))]),
               "softlight")
    cols = [(255, 120, 170), (255, 220, 70), (190, 120, 240), (255, 255, 255), (255, 150, 60)]
    flowers_scatter(hd, (0, hz + 6, 864, 693), 2600, cols, seed=3, size=(1, 3.5))
    grass = blank(); gd = ImageDraw.Draw(grass)
    rng = random.Random(5)
    for _ in range(500):
        x, y = rng.uniform(0, 864), rng.uniform(hz + 10, 693)
        h = 2 + (y - hz) / 60.0
        gd.line([(x, y), (x + rng.uniform(-2, 2), y - h)], fill=C((90, 160, 70)))
    hd.alpha_composite(grass)
    # faint post-rain rainbow
    rb = blank(); rd = ImageDraw.Draw(rb)
    for i, col in enumerate([(255, 80, 80), (255, 170, 60), (255, 240, 90), (120, 220, 90), (90, 160, 255),
                             (160, 110, 230)]):
        r0 = 330 - i * 7
        rd.arc([560 - r0, 330 - r0, 560 + r0, 330 + r0], 200, 340, fill=C(col, 70), width=7)
    hd = blend(hd, rb, "screen")
    plat_pair(hd, (222, 178, 112), (160, 112, 64), speckle=([(255, 120, 170), (255, 220, 70), (90, 160, 70)], 160))
    save_room("field_desert_bloom", hd)
    layers = keep(res["profile"][S("layers")], "sun")
    fx = [P(type=":drift", count=16, shape=":dot", size=3, colors=[[255, 150, 200], [255, 230, 120], [210, 160, 255]],
            dir=1, speed=[0.6, 1.2], sway=14, zoom=[0.6, 1.0], opacity=[200, 255], spin=6,
            layers=[":back", ":mid", ":front"]),
          P(type=":rise", count=10, shape=":dot", size=2, colors=GOLD, speed=[0.2, 0.5], sway=8, zoom=[0.5, 0.8],
            opacity=[120, 200], layers=[":back", ":mid"], blend=1),
          P(type=":drift", count=4, shape=":spark", size=5, colors=[[255, 255, 255], [255, 200, 240]],
            speed=[0.4, 0.8], sway=20, zoom=[0.6, 0.9], opacity=[200, 255], layers=[":mid", ":front"])]
    return {"profile": {S("layers"): layers, S("fx"): fx, S("art_extras"): {}},
            "note": "Superbloom: same dunes after rain - flower carpet, green shoots, damp sand, faint rainbow, "
                    "drifting petals and pollen"}


#---------------------------------------------------------------------------------------------
# MINDSCAPE 2: Nightmare
#---------------------------------------------------------------------------------------------
def mindscape_nightmare():
    hd, res = capture(fields_c.mindscape, fields_c)
    F = "mindscape_nightmare"
    hd = gradient_map(hd, [(0, (4, 0, 6)), (0.3, (40, 6, 22)), (0.55, (100, 18, 44)), (0.8, (170, 50, 70)),
                           (1, (240, 150, 150))])
    # shadow hands reaching up from the floor
    d = ImageDraw.Draw(hd)
    rng = random.Random(6)
    for k in range(9):
        x = rng.uniform(160, 820); y = rng.uniform(330, 690)
        if abs(x - FOE[0]) < 140 and abs(y - FOE[1]) < 50:
            continue
        h = rng.uniform(40, 90) * (0.5 + (y - 300) / 400)
        if abs(x - PLAYER[0]) < 250 and y > PLAYER[1] - 50 and y - h < PLAYER[1] + 60:
            x = PLAYER[0] + (262 if x > PLAYER[0] else -250)          # not over the player's platform
        w = h * 0.35
        d.polygon([(x - w / 2, y), (x - w / 2 + 2, y - h * 0.6), (x + w / 2 - 2, y - h * 0.6), (x + w / 2, y)],
                  fill=C((6, 0, 6)))
        for f in range(4):
            fx_ = x - w / 2 + 2 + f * (w - 4) / 3
            d.line([(fx_, y - h * 0.6), (fx_ + rng.uniform(-4, 4), y - h)], fill=C((6, 0, 6)), width=max(2, int(w / 6)))
    save_room("field_mindscape_nightmare", hd)
    layers = []
    es = eye_sheet(10)
    name = "pf_mindscape_nightmare_eye"
    save_element(name, es)
    for i, (x, y, z) in enumerate(((250, 210, 1), (700, 190, 1), (430, 170, 1), (800, 330, 1), (210, 330, 1))):
        layers.append(P(bitmap=name, hd=True, x=round(x / 2.25, 2), y=round(y / 2.25, 2), z=z, frames=4,
                        frame_time=24 + i * 7, zoom=1.0 + (i % 2) * 0.6))
    layers.append(layer(F, "door", soft_glow((640, 266), 70, (255, 40, 40), alpha=220), z=1, blend=1,
                        anim=S("pulse"), min=60, max=220, period=50))
    fx = [P(type=":rise", count=16, shape=":glow", size=5, colors=[[60, 0, 20], [120, 10, 40], [20, 0, 10]],
            speed=[0.2, 0.5], sway=12, zoom=[0.5, 1.0], opacity=[140, 220], layers=[":back", ":mid", ":front"]),
          P(type=":flash", color=[160, 0, 30], alpha=60, interval=[160, 300], decay=10)]
    extras = {"vacuum": "dark006",
              "img001": strip(F, "dread", fog_strip(864, 160, (60, 0, 20), seed=181, scale=22, density=0.55,
                                                    alpha=120), 240, speed=0.5, direction=-1, z=3)}
    return {"profile": {S("layers"): layers, S("fx"): fx, S("art_extras"): extras},
            "note": "Nightmare: same dream curdled crimson-black - blinking eyes in the void, shadow hands, "
                    "blood-red door, dread mist"}


#---------------------------------------------------------------------------------------------
# HOLLOW_CATHEDRAL 2: Consecrated
#---------------------------------------------------------------------------------------------
def cathedral_consecrated():
    hd, res = capture(fields_c.hollow_cathedral, fields_c)
    F = "hollow_cathedral_consecrated"
    hd = gradient_map(hd, [(0, (40, 30, 44)), (0.3, (110, 92, 100)), (0.6, (196, 176, 160)), (0.85, (240, 226, 200)),
                           (1, (255, 252, 236))])
    rw = rose_window(70, [(220, 40, 70), (50, 90, 220), (240, 200, 60), (50, 180, 110), (170, 70, 220)])
    hd.alpha_composite(rw, (526 - rw.width // 2, 156))
    save_room("field_hollow_cathedral_consecrated", hd)
    glass = mask_from(rw, lambda r, g, b: (r + g + b > 120) & ~((r < 30) & (g < 30)))
    gl = blank(); gl.alpha_composite(glow_from_mask(glass, (255, 240, 200), radius=14, gain=1.4, size=rw.size),
                                     (526 - rw.width // 2, 156))
    layers = [layer(F, "rose", gl, z=1, blend=1, anim=S("pulse"), min=120, max=220, period=140)]
    layers += keep(res["profile"][S("layers")], "candles")
    for i, (x, ang) in enumerate(((470, 100), (526, 90), (590, 80))):
        layers.append(layer(F, "holy%d" % i, cone(HD, (x, 190), 16, 480, (255, 236, 170), alpha=90, angle=ang),
                            z=2, blend=1, anim=S("pulse"), min=50, max=110, period=200 + i * 50, phase=i * 1.5))
    fx = [P(type=":rise", count=18, shape=":spark", size=5, colors=GOLD + [[255, 255, 255]], speed=[0.2, 0.5],
            sway=12, zoom=[0.5, 0.9], opacity=[170, 255], layers=[":back", ":mid", ":front"], blend=1),
          P(type=":drift", count=10, shape=":dot", size=2, colors=DUST, speed=[0.1, 0.3], sway=4, zoom=[0.5, 0.8],
            opacity=[90, 160], layers=[":back", ":mid"])]
    extras = {"lightsC": True}
    return {"profile": {S("layers"): layers, S("fx"): fx, S("art_extras"): extras},
            "note": "Consecrated: same nave washed in ivory and gold, rose window restored and blazing, holy "
                    "light shafts, rising light motes"}


#---------------------------------------------------------------------------------------------
# NEW_MOON 2: Abyss / 3: Lamplight
#---------------------------------------------------------------------------------------------
def new_moon_abyss():
    hd, res = capture(fields_c.new_moon, fields_c)
    F = "new_moon_abyss"
    a = arr(hd)
    lum = (a[..., :3] * np.array([0.299, 0.587, 0.114])).sum(-1)
    edges = np.asarray(Image.fromarray(np.clip(lum, 0, 255).astype(np.uint8)).filter(ImageFilter.FIND_EDGES),
                       np.float32)
    a[..., :3] = a[..., :3] * 0.08
    em = (edges > 40)[..., None] & (np.arange(693)[:, None, None] > 160)
    a[..., :3] = np.where(em, np.array([34, 22, 58]), a[..., :3])
    hd = img(a)
    platform(hd, FOE, 116, 25, (10, 8, 16), (6, 4, 10), outline=(70, 40, 120))
    platform(hd, PLAYER, *pb(116, 25), (10, 8, 16), (6, 4, 10), outline=(70, 40, 120), thick=12)
    save_room("field_new_moon_abyss", hd)
    layers = [layer(F, "rim", soft_glow(FOE, 160, (90, 50, 170), alpha=90, squash=0.3), z=1, blend=1,
                    anim=S("pulse"), min=20, max=90, period=180)]
    fx = [P(type=":rise", count=12, shape=":glow", size=5, colors=[[90, 60, 160], [50, 30, 100]], speed=[0.1, 0.3],
            sway=10, zoom=[0.5, 0.9], opacity=[60, 130], layers=[":back", ":mid", ":front"], blend=1)]
    extras = {"vacuum": "dark004",
              "img001": strip(F, "void", fog_strip(864, 220, (10, 4, 20), seed=191, scale=30, density=0.6,
                                                   alpha=170), 240, speed=0.5, direction=-1, z=4)}
    return {"profile": {S("layers"): layers, S("fx"): fx, S("art_extras"): extras},
            "note": "Abyss: same rooftops swallowed by darkness - stars and moon gone, only faint violet edges, "
                    "void mist"}


def new_moon_lamplight():
    hd, res = capture(fields_c.new_moon, fields_c)
    F = "new_moon_lamplight"
    roof = 150 + 170
    d = ImageDraw.Draw(hd)
    lamps = []
    for x in (180, 300, 420, 640, 760, 860):
        top = roof - 8
        d.rectangle([x - 2, top, x + 2, roof + 40], fill=C((30, 26, 30)), outline=C((10, 8, 10)))
        d.rectangle([x - 6, top - 12, x + 6, top], fill=C((255, 200, 110)), outline=C((40, 30, 20)))
        d.polygon([(x - 8, top - 12), (x + 8, top - 12), (x, top - 18)], fill=C((30, 26, 30)))
        lamps.append((x, top - 6))
    a = arr(hd)
    winm = (a[..., 0] > 200) & (a[..., 1] > 150) & (a[..., 2] < 160) & (np.arange(693)[:, None] < roof)
    hd = blend(hd, vgradient(HD, [(0, (0, 0, 0, 0)), (0.42, (255, 150, 60, 0)), (0.6, (255, 150, 70, 70)),
                                  (1, (255, 120, 40, 30))]), "softlight")
    save_room("field_new_moon_lamplight", hd)
    lm = np.zeros((693, 864), np.float32)
    for (x, y) in lamps:
        lm[y - 5:y + 5, max(x - 5, 0):x + 5] = 1
    layers = [layer(F, "lamps", glow_from_mask(lm, (255, 190, 100), radius=14, gain=2.0), z=1, blend=1,
                    anim=[S("pulse"), S("flicker")], min=150, max=220, period=40, chance=0.008, dropout=3),
              layer(F, "pools", soft_glow((520, 420), 380, (255, 170, 80), alpha=70, squash=0.3), z=1, blend=1,
                    anim=S("pulse"), min=40, max=80, period=120),
              layer(F, "windows", glow_from_mask(winm.astype(np.float32), (255, 200, 130), radius=3, gain=1.5,
                                                 core=1.0), z=1, blend=1, anim=S("pulse"), min=120, max=200,
                    period=90)]
    layers += keep(res["profile"][S("layers")], "corona")
    fx = [P(type=":rise", count=8, shape=":glow", size=4, colors=[[255, 190, 100], [255, 150, 60]],
            area=[60, 110, 330, 180], speed=[0.2, 0.4], sway=6, zoom=[0.4, 0.7], opacity=[120, 200],
            layers=[":back", ":mid"], blend=1),
          P(type=":twinkle", count=18, bitmap="star", area=[0, 70, 384, 130], speed=[1, 3], zoom=[0.6, 1.2],
            opacity=[140, 255], layers=[":back"])]
    return {"profile": {S("layers"): layers, S("fx"): fx, S("art_extras"): {}},
            "note": "Lamplight: same rooftops with Nadir's gaslamps lit - lamp posts, warm windows and light "
                    "pools, rising lamp sparks"}


#---------------------------------------------------------------------------------------------
# DRAGONS_DEN 2: Wyrmfire
#---------------------------------------------------------------------------------------------
def dragons_wyrmfire():
    hd, res = capture(fields_a.dragons_den, fields_a)
    F = "dragons_den_wyrmfire"
    lava = mask_from(hd, lambda r, g, b: (r > 230) & (g > 100) & (b < 110))
    grown = np.asarray(Image.fromarray((lava * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(9)), np.float32) / 255
    a = arr(hd)
    a = a * (1 - grown[..., None] * 0.85) + np.array([255, 150, 60, 255], np.float32) * grown[..., None] * 0.85
    hd = img(a)
    hd = gradient_map(hd, [(0, (16, 4, 6)), (0.18, (60, 14, 18)), (0.36, (120, 30, 26)), (0.55, (190, 70, 34)),
                           (0.75, (250, 140, 50)), (1, (255, 236, 160))])
    d = ImageDraw.Draw(hd)
    eyes = [(352 - 10, 168), (698 + 4, 168)]
    for (x, y) in eyes:
        d.rectangle([x - 2, y - 1, x + 2, y + 1], fill=C((255, 60, 30)))
    save_room("field_dragons_den_wyrmfire", hd)
    layers = [layer(F, "magma", glow_from_mask(grown, (255, 120, 40), radius=12, gain=1.4), z=1, blend=1,
                    anim=S("pulse"), min=110, max=230, period=60)]
    em = np.zeros((693, 864), np.float32)
    for (x, y) in eyes:
        em[y - 2:y + 3, x - 3:x + 4] = 1
    layers.append(layer(F, "eyes", glow_from_mask(em, (255, 60, 30), radius=6, gain=3.0, core=1.0), z=1, blend=1,
                        anim=S("pulse"), min=100, max=255, period=45))
    fs = flame_sheet(seed=3)
    name = "pf_dragons_den_wyrmfire_flame"
    save_element(name, fs)
    for i, (x, y, zoom, z) in enumerate(((300, 330, 1.0, 2), (420, 318, 0.8, 2), (720, 330, 1.1, 2), (180, 470, 1.6, 22),
                                         (820, 500, 1.8, 22), (620, 300, 0.7, 1))):
        layers.append(P(bitmap=name, hd=True, x=round(x / 2.25, 2), y=round(y / 2.25, 2), ox=13, oy=44, z=z,
                        frames=4, frame_time=4 + i % 3, zoom=zoom, blend=0))
    fx = [P(type=":rise", count=30, shape=":glow", size=5, colors=[[255, 140, 50], [200, 90, 255], [255, 210, 90]],
            speed=[1.0, 2.2], sway=10, zoom=[0.3, 0.7], opacity=[180, 255], layers=[":back", ":mid", ":front"],
            blend=1),
          P(type=":twinkle", count=10, shape=":spark", size=5, colors=GOLD, area=[0, 120, 384, 308], speed=[3, 6],
            zoom=[0.5, 0.9], opacity=[160, 255], layers=[":back", ":mid"], blend=1)]
    extras = dict(res["profile"][S("art_extras")])
    extras["bubbles"] = "bubbleRed"
    return {"profile": {S("layers"): layers, S("fx"): fx, S("art_extras"): extras},
            "note": "Wyrmfire: same lair awake - magma surging wider and brighter, statue eyes lit, wyrmfire "
                    "flames (4-frame sheets) along the floor, heavy embers"}


#---------------------------------------------------------------------------------------------
# WILDFIRE (new) / stage 2 Embers
#---------------------------------------------------------------------------------------------
def _wild_base():
    hd = vanilla("rejuvenation", "GoldForest")
    return hd


FLAMES = [(210, 250, 1.6, 1), (300, 214, 1.2, 1), (380, 236, 1.0, 1), (640, 230, 1.3, 1), (720, 250, 1.7, 1),
          (560, 214, 0.9, 1), (120, 480, 2.4, 22), (830, 520, 2.6, 22), (250, 330, 1.0, 2), (760, 330, 1.1, 2)]


def wildfire():
    F = "wildfire"
    hd = _wild_base()
    foliage = mask_from(hd, lambda r, g, b: (r > 180) & (g > 120) & (b < 110))
    hd = gradient_map(hd, [(0, (20, 8, 8)), (0.3, (80, 24, 14)), (0.55, (170, 60, 24)), (0.8, (240, 140, 50)),
                           (1, (255, 230, 150))])
    hd = blend(hd, vgradient(HD, [(0, (40, 20, 20, 160)), (0.35, (90, 30, 20, 60)), (0.6, (0, 0, 0, 0)),
                                  (1, (0, 0, 0, 0))]), "multiply")
    save_room("field_wildfire", hd)
    fs = flame_sheet(seed=1)
    name = "pf_wildfire_flame"
    save_element(name, fs)
    layers = [layer(F, "blaze", glow_from_mask(foliage, (255, 120, 30), radius=10, gain=1.2), z=1, blend=1,
                    anim=S("pulse"), min=80, max=190, period=50)]
    for i, (x, y, zoom, z) in enumerate(FLAMES):
        layers.append(P(bitmap=name, hd=True, x=round(x / 2.25, 2), y=round(y / 2.25, 2), ox=13, oy=44, z=z,
                        frames=4, frame_time=4 + i % 3, zoom=zoom))
    extras = {"img001": strip(F, "smoke", fog_strip(864, 200, (60, 40, 36), seed=201, scale=28, density=0.6,
                                                    alpha=150), 150, speed=1, direction=-1, z=3),
              "img002": strip(F, "heat", fog_strip(864, 120, (255, 130, 50), seed=202, scale=18, density=0.5,
                                                   alpha=60), 330, speed=1, direction=1, z=4)}
    fx = [P(type=":rise", count=34, shape=":glow", size=5, colors=EMBER, speed=[1.0, 2.4], sway=12,
            zoom=[0.3, 0.7], opacity=[180, 255], layers=[":back", ":mid", ":front"], blend=1),
          P(type=":fall", count=12, shape=":dot", size=3, colors=ASH, speed=[0.4, 0.9], sway=14, zoom=[0.4, 0.7],
            opacity=[110, 180], layers=[":back", ":mid"]),
          vent(260, 230, count=6, colors=SMOKE, rise=120, size=26, opacity=(70, 120)),
          vent(700, 230, count=6, colors=SMOKE, rise=120, size=26, opacity=(70, 120))]
    res = {"profile": {S("art_extras"): extras, S("layers"): layers, S("fx"): fx},
           "origins": [[REJ, "battlebgGoldForest, enemybaseGoldForest (gradient-mapped to fire)"],
                       [OWN, "burning-canopy glow, 4-frame flame sheets on trees and ground, smoke and heat strips"]]}
    # stage 2: embers
    hd2 = _wild_base()
    hd2 = gradient_map(hd2, [(0, (10, 8, 10)), (0.3, (34, 28, 30)), (0.55, (70, 62, 60)), (0.8, (120, 112, 106)),
                             (1, (180, 172, 160))])
    nb = noise(HD, 36, 211, 2)
    fine = noise(HD, 3, 212, 1)
    coals = (nb > 0.64) & (fine > 0.78) & (np.arange(693)[:, None] > 300)
    a2 = arr(hd2)
    a2[coals] = [90, 36, 24, 255]
    hd2 = img(a2)
    d = ImageDraw.Draw(hd2)
    rng = random.Random(7)
    for _ in range(70):   # pioneer sprouts
        x, y = rng.uniform(160, 860), rng.uniform(310, 690)
        h = 3 + (y - 300) / 60
        d.line([(x, y), (x, y - h)], fill=C((70, 150, 60)))
        d.point((x - 1, y - h), fill=C((120, 200, 90))); d.point((x + 1, y - h + 1), fill=C((120, 200, 90)))
    save_room("field_wildfire_embers", hd2)
    F2 = "wildfire_embers"
    layers2 = [layer(F2, "coals", glow_from_mask(coals.astype(np.float32), (255, 90, 30), radius=4, gain=1.0,
                                                 core=0.9), z=1, blend=1, anim=S("pulse"), min=40, max=170,
                     period=130)]
    extras2 = {"img001": strip(F2, "smoke", fog_strip(864, 200, (120, 120, 136), seed=212, scale=30, density=0.6,
                                                      alpha=100), 220, speed=0.5, direction=-1, z=3)}
    fx2 = [P(type=":fall", count=30, shape=":dot", size=3, colors=ASH, speed=[0.3, 0.7], sway=16, zoom=[0.4, 0.8],
             opacity=[130, 210], layers=[":back", ":mid", ":front"]),
           P(type=":rise", count=10, shape=":glow", size=4, colors=EMBER, speed=[0.4, 1.0], sway=8, zoom=[0.3, 0.6],
             opacity=[150, 230], layers=[":back", ":mid"], blend=1),
           vent(300, 300, count=5, colors=[[150, 160, 190], [120, 130, 160]], rise=120, size=24, opacity=(40, 90)),
           vent(700, 320, count=5, colors=[[150, 160, 190], [120, 130, 160]], rise=120, size=24, opacity=(40, 90))]
    res["profile"][S("stages")] = {2: {S("art_extras"): extras2, S("layers"): layers2, S("fx"): fx2}}
    res["origins"].append(["stage 2", "Embers: same forest charred - charcoal grade, glowing coal beds, ghostly "
                                      "smoke, pioneer sprouts, falling ash"])
    return res


#---------------------------------------------------------------------------------------------
# Reworks: ASHEN_WASTE (ash-covered floor, more contrast) and INVERSE (hanging negative world)
#---------------------------------------------------------------------------------------------
def ashen_rework():
    """ASHEN_WASTE is 'Cinderglass' since the Revision 10 redesign: the Volcanic caldera (same layout) quenched
    into black volcanic glass with hot seams, glints and steam geysers."""
    F = "ashen_waste"
    hd = fields_a._caldera_base()
    lava = mask_from(hd, lambda r, g, b: (r > 200) & (g > 70) & (b < 120))
    pivots = fields_a._obsidian_pillars(hd, rim=(190, 150, 255, 255))
    hd = gradient_map(hd, [(0.0, (6, 4, 14)), (0.2, (22, 14, 44)), (0.38, (48, 30, 88)), (0.55, (84, 60, 140)),
                           (0.75, (150, 130, 220)), (1.0, (236, 228, 255))])
    # glassy sheen: hard specular streaks across the floor
    ys = np.arange(693)[:, None]
    n = noise(HD, 60, 501, 1)
    streak = ((np.sin((np.arange(864)[None, :] * 0.5 + ys * 1.4) / 26.0 + n * 6) > 0.985) & (ys > 300))
    a = arr(hd)
    a[streak] = a[streak] * 0.72 + np.array([170, 150, 240, 255], np.float32) * 0.28
    lm = Image.fromarray((lava * 255).astype(np.uint8))
    inner = np.asarray(lm.filter(ImageFilter.MinFilter(5)), np.float32) / 255
    a[lava > 0] = [14, 8, 26, 255]                    # flows frozen to black glass
    a[inner > 0] = [255, 130, 40, 255]                # ...with hot seams still alive inside
    core = np.asarray(lm.filter(ImageFilter.MinFilter(9)), np.float32) / 255
    a[core > 0] = [255, 220, 130, 255]
    hd = img(a)
    # obsidian shards standing in the glass
    for foot, sc, seed in (((250, 330), 60, 1), ((716, 322), 70, 2), ((110, 590), 150, 3), ((800, 620), 130, 4)):
        crystal_cluster(hd, foot, sc, [(30, 20, 56), (60, 40, 110), (16, 10, 30), (110, 90, 180)], seed=seed, n=4,
                        outline=(4, 2, 10))
    fields_a.save_room("field_ashen_waste", hd)
    layers = [layer(F, "seams", glow_from_mask(inner, (255, 120, 40), radius=7, gain=1.5), z=1, blend=1,
                    anim=S("pulse"), min=70, max=200, period=100),
              layer(F, "sheen", soft_glow((500, 430), 380, (150, 110, 255), alpha=90, squash=0.35), z=1, blend=1,
                    anim=S("pulse"), min=30, max=90, period=180)]
    for i, (x, y) in enumerate(pivots):
        b = banner(26, 104, (60, 40, 100, 255), (190, 170, 240, 255), (220, 200, 255, 255))
        layers.append(layer(F, "banner%d" % i, onto(b, x - b.width / 2, y), anchor=(x, y + 4), z=2,
                            anim=S("sway"), amp=1.8, period=160 + i * 29))
    geysers = [(330, 304), (612, 300), (230, 470), (720, 520)]
    for i, (vx, vy) in enumerate(geysers):     # geyser bursts: a tall plume that flares up now and then
        pl = blank(); pl.alpha_composite(soft_glow((vx, vy - 90), 70, (236, 238, 248), alpha=200, squash=2.2,
                                                   power=1.2))
        layers.append(layer(F, "geyser%d" % i, pl, z=3 if vy < 400 else 23, anim=S("flicker"), opacity=0,
                            min=150, chance=0.006, dropout=22))
    extras = {"img001": ebdx_stock("decor006", scrolling=True, speed=2, direction=-1, oy=0, z=3, flat=True,
                                   opacity=120),
              "img003": strip(F, "steam", fog_strip(864, 160, (220, 220, 240), seed=9, scale=34, density=0.5,
                                                    alpha=70), 230, speed=0.5, direction=1, z=4)}
    fx = [P(type=":twinkle", count=22, shape=":spark", size=7, colors=[[255, 255, 255], [200, 180, 255],
                                                                       [255, 200, 150]],
            area=[0, 110, 384, 308], speed=[4, 8], zoom=[0.4, 0.9], opacity=[170, 255], layers=[":back", ":mid"],
            blend=1),
          P(type=":drift", count=10, shape=":dot", size=2, colors=[[200, 180, 255], [255, 255, 255]],
            speed=[0.3, 0.7], sway=6, zoom=[0.5, 0.8], opacity=[110, 190], layers=[":mid", ":front"], blend=1)]
    for (vx, vy) in geysers:
        fx.append(vent(vx, vy, count=6, rise=110, size=20, speed=(0.5, 1.0), opacity=(70, 130)))
    return {"profile": {S("art_extras"): extras, S("layers"): layers, S("fx"): fx},
            "origins": [[REJ, "battlebgVolcano, enemybaseVolcano (Volcanic's layout quenched to black glass: "
                              "gradient-mapped violet-black, flows glassed over with hot seams)"],
                        [EBDX, "decor006"],
                        [OWN, "Cinderglass: faint glass sheen, obsidian shards, seam glow, steam geysers with "
                              "bursts, glass glints, violet banners"]]}


def inverse_rework():
    hd, res = capture(fields_c.inverse, fields_c)
    F = "inverse"
    src = game_img("rejuvenation", "battlebgForest")
    neg = arr(src); neg[..., :3] = 255 - neg[..., :3]
    neg = img(neg).transpose(Image.FLIP_TOP_BOTTOM)          # the world, hanging upside down
    band = neg.crop((0, 0, 512, 150))
    ext = Image.new("RGBA", (864, 150))
    for x in range(0, 864, 512):
        ext.alpha_composite(band if (x // 512) % 2 == 0 else band.transpose(Image.FLIP_LEFT_RIGHT), (x, 0))
    nn = noise((864, 1), 6, 311, 3)[0]
    a = arr(ext)
    for x in range(864):
        cut = int(110 + nn[x] * 36)
        a[cut:, x, 3] = 0
        a[max(cut - 3, 0):cut, x, :3] = [255, 255, 255]
    hd.alpha_composite(img(a), (0, 150))
    fields_c.save_room("field_inverse", hd)
    layers = []
    for i, (cx, cy, w) in enumerate(((250, 236, 120), (700, 226, 140), (480, 186, 80))):
        isl = Image.new("RGBA", (w + 8, w), (0, 0, 0, 0))
        d = ImageDraw.Draw(isl)
        rng = random.Random(i)
        top = w * 0.28
        pts = [(4, top)] + [(4 + w * k / 6, top + w * 0.6 * math.sin(k / 6 * math.pi) * rng.uniform(0.7, 1.1))
                            for k in range(1, 6)] + [(w + 4, top)]
        d.polygon(pts, fill=C((200, 214, 230)), outline=C((255, 255, 255)))
        for k in range(1, 6):
            x0, y0 = pts[k]
            d.line([(x0, top + 3), (x0 - 4, y0 - 4)], fill=C((150, 166, 190)))
        d.rectangle([4, top - 7, w + 4, top], fill=C((210, 60, 220)), outline=C((255, 255, 255)))
        d.chord([10, top - 24, w - 2, top + 10], 180, 360, fill=C((160, 40, 190)))
        layers.append(layer(F, "rock%d" % i, onto(isl, cx - w / 2, cy - top), z=1, anim=S("bob"), amp=6,
                            period=200 + i * 50, phase=i * 2))
    res["profile"][S("layers")] = layers
    res["origins"] = [[REB, "battlebgInverse, enemybaseInverse"],
                      [REJ, "battlebgForest (colour-inverted and flipped: the world hanging overhead)"],
                      [OWN, "negative floating rock islands, static mist"]]
    return res


BUILDERS = {
    "GRAND_STAGE": with_stages(fields_c.grand_stage, {2: grand_stage_level(2), 3: grand_stage_level(3)}),
    "NEON_GRID": with_stages(fields_c.neon_grid, {2: neon_blackout}),
    "DESERT": with_stages(fields_a.desert, {2: desert_bloom}),
    "MINDSCAPE": with_stages(fields_c.mindscape, {2: mindscape_nightmare}),
    "HOLLOW_CATHEDRAL": with_stages(fields_c.hollow_cathedral, {2: cathedral_consecrated}),
    "NEW_MOON": with_stages(fields_c.new_moon, {2: new_moon_abyss, 3: new_moon_lamplight}),
    "DRAGONS_DEN": with_stages(fields_a.dragons_den, {2: dragons_wyrmfire}),
    "WILDFIRE": wildfire,
    "ASHEN_WASTE": ashen_rework,
    "INVERSE": inverse_rework,
}


#---------------------------------------------------------------------------------------------
# MEADOW (new): Elowen's open countryside
#---------------------------------------------------------------------------------------------
def meadow():
    F = "meadow"
    hd = vanilla("reborn", "Field", base=False)
    hz = 150 + 104
    far = mountains((864, 693), hz + 6, 46, (120, 170, 120), seed=401, rough=0.3, peaks=3)
    hd.alpha_composite(far)
    mid = mountains((864, 693), hz + 26, 34, (96, 160, 80), seed=402, rough=0.4, peaks=4, outline=(60, 120, 60))
    hd.alpha_composite(mid)
    d = ImageDraw.Draw(hd)
    # hedgerows along the slope + orchard rows
    rng = random.Random(403)
    for row, y in enumerate((hz + 22, hz + 40)):
        for x in range(-10, 874, 7):
            r = rng.uniform(4, 7)
            d.ellipse([x - r, y - r - row * 2, x + r, y + r * 0.6], fill=C((54, 110, 54)), outline=C((30, 70, 30)))
    for k, y in enumerate((hz + 16, hz + 30)):
        for x in range(30 + k * 20, 860, 46):
            if 400 < x < 660 and k == 1:
                continue
            paste(hd, orchard_tree(10 + k * 3, seed=x + k), x, y, "bottom")
    # river meadow: a bright ribbon of water winding across the middle distance
    pts = [(x, hz + 52 + 8 * math.sin(x / 70.0)) for x in range(0, 870, 6)]
    d.line(pts, fill=C((140, 200, 230)), width=7)
    d.line([(x, y - 2) for x, y in pts], fill=C((220, 245, 255)), width=1)
    flowers_scatter(hd, (0, hz + 60, 864, 693), 900, [(255, 255, 255), (255, 220, 70), (200, 140, 240), (255, 140, 170)],
                    seed=404, size=(1, 2.5))
    eb = game_img("reborn", "enemybaseFieldGrass")
    place_foe_base(hd, eb); place_player_base_scaled(hd, eb)
    save_room("field_meadow", hd)
    layers = []
    for i, (x, y, w, h, z) in enumerate(((190, 330, 60, 60, 2), (330, 336, 50, 44, 2), (720, 336, 64, 58, 2),
                                         (800, 330, 50, 50, 2), (90, 560, 140, 150, 24), (160, 600, 100, 120, 24),
                                         (820, 600, 150, 160, 24), (700, 650, 110, 120, 24))):
        t = grass_tuft(w, h, seed=i)
        layers.append(layer(F, "grass%d" % i, onto(t, x - w / 2, y - h), anchor=(x, y), z=z, anim=S("sway"),
                            amp=3 + (z > 10) * 2, period=110 + i * 9, phase=i * 0.4))
    extras = {"img001": strip(F, "clouds", make_cloud_band(), 150, speed=0.5, direction=1, z=1),
              "img002": strip(F, "breeze", fog_strip(864, 90, (255, 255, 230), seed=405, scale=14, density=0.4,
                                                     alpha=50), 300, speed=2, direction=1, z=3)}
    fx = [P(type=":drift", count=14, shape=":dot", size=2, colors=[[255, 255, 240], [250, 240, 200]], dir=1,
            speed=[0.8, 1.6], sway=12, zoom=[0.5, 0.9], opacity=[160, 230], layers=[":back", ":mid", ":front"]),
          P(type=":drift", count=8, shape=":dot", size=3, colors=[[255, 200, 220], [255, 240, 140], [210, 170, 255]],
            dir=1, speed=[0.6, 1.2], sway=16, zoom=[0.6, 1.0], opacity=[200, 255], spin=6, layers=[":mid", ":front"]),
          P(type=":drift", count=3, shape=":spark", size=5, colors=[[255, 240, 120], [255, 255, 255]],
            speed=[0.3, 0.6], sway=20, zoom=[0.6, 0.9], opacity=[200, 255], layers=[":mid"])]
    return {"profile": {S("art_extras"): extras, S("layers"): layers, S("fx"): fx},
            "origins": [[REB, "battlebgField, enemybaseFieldGrass"],
                        [OWN, "rolling hills, hedgerows, orchard rows, river ribbon, wildflowers, swaying tall-grass "
                              "clumps, clouds, breeze"]]}


def make_cloud_band():
    im = cloud_floor(864, 110, 30, color=(255, 255, 255), shade=(220, 232, 246), deep=(200, 216, 236), seed=406,
                     rmin=12, rmax=26, rows=2)
    a = arr(im)
    a[70:, :, 3] = 0
    return img(a)


BUILDERS["MEADOW"] = meadow
