"""Fire / earth / cave / mountain fields."""
from bblib import *
from paint import *
from props import *
from rubygen import S

REJ = "Pokémon Rejuvenation (Rejuvenation Team)"
REB = "Pokémon Reborn (Reborn Team)"
DES = "Pokémon Desolation (Desolation Team)"
EBDX = "Elite Battle: DX stock elements (Luka S.J.)"
OWN = "Prismfall (procedural, art/battlebacks/*.py)"
O = (142, 150)   # vanilla bg origin: its top row = top of the default view, foe point aligned


def vanilla(game, name, base=None, player_base="scaled", origin=O, mirror=False, **kw):
    bg = game_img(game, "battlebg" + name)
    if mirror:
        bg = bg.transpose(Image.FLIP_LEFT_RIGHT)
    hd = extend_vanilla(bg, origin=origin, **kw)
    bname = base or name
    if base is not False and has_game_img(game, "enemybase" + bname):
        eb = game_img(game, "enemybase" + bname)
        place_foe_base(hd, eb)
        if player_base == "scaled":
            place_player_base_scaled(hd, eb)
    return hd


def plat_pair(hd, top, side, **kw):
    platform(hd, FOE, 118, 26, top, side, **kw)
    platform(hd, PLAYER, *pb(118, 26), top, side, thick=12, **kw)


#---------------------------------------------------------------------------------------------
# VOLCANIC / ASHEN_WASTE: one layout so the quench reads as the same place
#---------------------------------------------------------------------------------------------
def _caldera_base():
    return vanilla("rejuvenation", "Volcano")


PILLARS = [(386, 1), (640, -1)]


def _obsidian_pillars(hd, rim=(255, 120, 40, 255)):
    for x, side in PILLARS:
        pillar(hd, x, 92, 316, 26, (34, 26, 38, 255), (74, 56, 82, 255), (18, 12, 22, 255),
               (8, 4, 10, 255), rim=rim, rim_side=side)
    return [(x, 104) for x, _ in PILLARS]


def volcanic():
    F = "volcanic"
    hd = _caldera_base()
    pivots = _obsidian_pillars(hd)
    lava = mask_from(hd, lambda r, g, b: (r > 200) & (g > 70) & (b < 120))
    save_room("field_volcanic", hd)
    glow = glow_from_mask(lava, (255, 130, 40), radius=8, gain=1.4)
    layers = [
        layer(F, "lavaglow", glow, z=1, blend=1, opacity=150, anim=S("pulse"), min=60, max=170, period=110),
        layer(F, "caldera", soft_glow((470, 660), 380, (255, 90, 20), alpha=120, squash=0.35), z=1, blend=1,
              anim=S("pulse"), min=40, max=110, period=170),
    ]
    for i, (x, y) in enumerate(pivots):
        b = banner(26, 104, (150, 24, 20, 255), (230, 170, 60, 255), (240, 190, 70, 255))
        layers.append(layer(F, "banner%d" % i, onto(b, x - b.width / 2, y), anchor=(x, y + 4), z=2,
                            anim=S("sway"), amp=2.2, period=150 + i * 37))
    haze = fog_strip(864, 160, (255, 120, 50), seed=7, scale=30, density=0.6, alpha=70)
    extras = {
        "img001": ebdx_stock("decor006", scrolling=True, speed=2, direction=-1, oy=0, z=3, flat=True, opacity=155),
        "img002": ebdx_stock("decor009", scrolling=True, speed=1, direction=1, oy=0, z=3, flat=True, opacity=96),
        "img003": strip(F, "haze", haze, 250, speed=0.5, direction=1, z=4),
        "img005": ebdx_stock("base001", scrolling=True, speed=0.5, direction=-1, oy=0, y=122, z=1, flat=True,
                             opacity=110),
        "bubbles": "bubbleRed",
    }
    return {"profile": {S("art_extras"): extras, S("layers"): layers},
            "origins": [[REJ, "battlebgVolcano, enemybaseVolcano (extended to the EBDX room, platforms re-placed)"],
                        [EBDX, "decor006, decor009, base001, bubbleRed (the MAGMA environment's layers)"],
                        [OWN, "obsidian pillars, dragon-lord banners, lava and caldera glow, heat haze"]]}


def ashen_waste():
    F = "ashen_waste"
    hd = _caldera_base()
    lava = mask_from(hd, lambda r, g, b: (r > 200) & (g > 70) & (b < 120))
    pivots = _obsidian_pillars(hd, rim=(170, 160, 150, 255))
    # cooled caldera: violet-charcoal shadows, slate stone, pale ash highlights
    hd = gradient_map(hd, [(0.0, (16, 13, 20)), (0.22, (44, 40, 50)), (0.45, (82, 78, 86)),
                           (0.7, (138, 132, 132)), (1.0, (222, 214, 204))])
    a = arr(hd)
    lm = lava[..., None]
    # lava turned to ropy basalt crust: dark fill, lighter rims
    edge = np.asarray(Image.fromarray((lava * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3)), np.float32) / 255
    rimm = np.clip(edge - lava, 0, 1)[..., None]
    a = a * (1 - lm) + np.array([40, 36, 42, 255], np.float32) * lm
    a = a * (1 - rimm) + np.array([74, 68, 74, 255], np.float32) * rimm
    hd = img(a)
    hd = blend(hd, vgradient(HD, [(0, (150, 170, 200, 0)), (0.4, (150, 170, 200, 50)), (1, (40, 40, 60, 70))]),
               "softlight")
    save_room("field_ashen_waste", hd)
    # the last warmth: thin cracks inside the old lava flows
    inner = np.asarray(Image.fromarray((lava * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(5)), np.float32) / 255
    cr = inner * (np.abs(noise(HD, 6, 21, 2) - 0.5) < 0.035)
    ember = glow_from_mask(cr, (255, 110, 40), radius=3, gain=1.0, core=1.0)
    layers = [layer(F, "embers", ember, z=1, blend=1, opacity=150, anim=S("pulse"), min=40, max=170, period=150)]
    for i, (x, y) in enumerate(pivots):
        b = banner(26, 104, (64, 56, 58, 255), (130, 120, 110, 255), (120, 110, 100, 255))
        layers.append(layer(F, "banner%d" % i, onto(b, x - b.width / 2, y), anchor=(x, y + 4), z=2,
                            anim=S("sway"), amp=1.4, period=170 + i * 29))
    haze = fog_strip(864, 220, (205, 205, 210), seed=9, scale=34, density=0.62, alpha=85)
    extras = {
        "img001": ebdx_stock("decor006", scrolling=True, speed=2, direction=-1, oy=0, z=3, flat=True, opacity=110),
        "img003": strip(F, "steam", haze, 200, speed=0.5, direction=1, z=4),
    }
    fx = [P(type=":fall", count=30, shape=":dot", size=3, colors=ASH, speed=[0.3, 0.8], sway=16,
            zoom=[0.4, 0.8], opacity=[140, 220], layers=[":back", ":mid", ":front"])]
    for (vx, vy) in [(330, 300), (604, 296), (250, 455), (700, 520)]:
        fx.append(vent(vx, vy, count=6, rise=80, size=18))
    return {"profile": {S("art_extras"): extras, S("layers"): layers, S("fx"): fx},
            "origins": [[REJ, "battlebgVolcano, enemybaseVolcano (cooled: gradient-mapped, lava crusted over)"],
                        [EBDX, "decor006"],
                        [OWN, "quench recolour, ember cracks, steam vents, soot-stained banners"]]}


#---------------------------------------------------------------------------------------------
# DRAGONS_DEN: Wyrmrest lair, violet-black cavern, hoard and bones
#---------------------------------------------------------------------------------------------
def dragon_skull(scale=1.0, bone=(214, 200, 170), outline=(30, 20, 26), shade=(150, 132, 110)):
    w, h = int(150 * scale), int(90 * scale)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    s = scale
    head = [(10 * s, 52 * s), (40 * s, 30 * s), (80 * s, 24 * s), (112 * s, 32 * s), (140 * s, 50 * s),
            (138 * s, 60 * s), (100 * s, 62 * s), (60 * s, 70 * s), (20 * s, 66 * s)]
    d.polygon(head, fill=C(bone), outline=C(outline))
    d.polygon([(20 * s, 66 * s), (60 * s, 70 * s), (100 * s, 64 * s), (90 * s, 80 * s), (40 * s, 84 * s),
               (14 * s, 74 * s)], fill=C(shade), outline=C(outline))
    for i in range(7):
        x = (28 + i * 11) * s
        d.polygon([(x, 64 * s), (x + 4 * s, 64 * s), (x + 2 * s, 72 * s)], fill=C((240, 232, 210)), outline=C(outline))
    d.ellipse([84 * s, 36 * s, 104 * s, 50 * s], fill=C((20, 10, 24)), outline=C(outline))
    d.ellipse([30 * s, 46 * s, 38 * s, 52 * s], fill=C((30, 16, 30)))
    for k in (0, 1):
        pts = [(96 * s, 30 * s), (120 * s, 8 * s - k * 6 * s), (146 * s, 2 * s + k * 4 * s), (128 * s, 18 * s),
               (110 * s, 34 * s)]
        d.polygon(pts, fill=C(shade if k else bone), outline=C(outline))
    d.line([(44 * s, 38 * s), (78 * s, 30 * s)], fill=C(lighter(bone, 0.4)))
    return im


def hoard(w, h, seed=0, gold=(226, 176, 56), dark=(130, 80, 24), light=(255, 238, 150), outline=(54, 30, 8),
          extras=True):
    """Mound of coins: stepped outline, coin rows lit from the upper left, a few jewels and a blade."""
    rng = random.Random(seed)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    pts = []
    for i in range(0, w + 1, 4):
        u = (i - w / 2) / (w / 2)
        y = h - (h - 4) * max(0.0, 1 - abs(u) ** 1.7) ** 0.8 + rng.uniform(-1.5, 1.5)
        pts.append((i, min(h - 1, y)))
    d.polygon([(0, h - 1)] + pts + [(w, h - 1)], fill=C(dark), outline=C(outline))
    for yy in range(4, h, 3):
        for xx in range(2, w - 2, 4):
            u = (xx - w / 2) / (w / 2)
            top = h - (h - 4) * max(0.0, 1 - abs(u) ** 1.7) ** 0.8
            if yy < top + 2 or rng.random() < 0.15:
                continue
            lit = (1 - (yy - top) / max(h - top, 1)) * 0.6 + (0.4 if u < 0 else 0.1)
            col = light if lit > 0.75 else gold if lit > 0.35 else (186, 128, 36)
            ox = (yy // 3) % 2 * 2
            d.ellipse([xx + ox - 2, yy - 1, xx + ox + 2, yy + 1], fill=C(col))
            if rng.random() < 0.3:
                d.point((xx + ox - 1, yy - 1), fill=C(lighter(col, 0.5)))
    if extras:
        for _ in range(max(1, w // 60)):
            x = rng.uniform(0.25, 0.75) * w; y = h * rng.uniform(0.45, 0.75)
            c = rng.choice([(210, 40, 70), (60, 170, 230), (90, 210, 120), (190, 90, 230)])
            d.polygon([(x, y - 4), (x + 4, y), (x, y + 4), (x - 4, y)], fill=C(c), outline=C((40, 20, 20)))
            d.point((x - 1, y - 2), fill=(255, 255, 255, 255))
        if w > 120:
            bx = w * rng.uniform(0.35, 0.6)
            d.line([(bx, h * 0.15), (bx + 10, h * 0.62)], fill=C((30, 30, 40)), width=5)
            d.line([(bx, h * 0.15), (bx + 10, h * 0.62)], fill=C((200, 210, 230)), width=3)
            d.line([(bx - 7, h * 0.58), (bx + 18, h * 0.54)], fill=C((180, 130, 40)), width=4)
    for _ in range(w // 10):
        x = rng.uniform(0, w); y = h - rng.uniform(1, 4)
        d.ellipse([x - 2, y - 1, x + 2, y + 1], fill=C(rng.choice([gold, light])))
    return im


def dragons_den():
    F = "dragons_den"
    # deep inside the caldera tunnel: the painted cave zoomed 2x on its tunnel mouth, recoloured violet
    # a hoard chamber: 2x view of the caldera's great wall and lava fall (no tunnel mouth in frame)
    src = game_img("rejuvenation", "battlebgVolcano")
    src = src.crop((0, 40, 256, 184)).resize((512, 288), Image.NEAREST)
    src = src.convert("RGB").filter(ImageFilter.ModeFilter(5)).convert("RGBA")   # round off the 2x stair-steps
    hd = extend_vanilla(src, origin=O)
    lava = mask_from(hd, lambda r, g, b: (r > 200) & (g > 70) & (b < 120))
    hd = gradient_map(hd, [(0.0, (14, 6, 22)), (0.08, (34, 16, 50)), (0.18, (66, 32, 88)), (0.3, (104, 54, 126)),
                           (0.45, (150, 84, 160)), (0.7, (255, 150, 70)), (1.0, (255, 230, 150))])
    a = arr(hd)
    lm = lava[..., None]
    a = a * (1 - lm) + np.array([255, 120, 50, 255], np.float32) * lm
    hd = img(a)
    for x, flip in ((356, False), (698, True)):
        pillar(hd, x, 176, 318, 22, (52, 30, 60), (96, 62, 104), (26, 14, 32), (10, 4, 12),
               rim=(255, 140, 70), rim_side=-1 if flip else 1)
        sk = dragon_skull(0.46, bone=(110, 76, 120), shade=(70, 44, 80), outline=(14, 6, 18))
        if flip:
            sk = sk.transpose(Image.FLIP_LEFT_RIGHT)
        paste(hd, sk, x, 180, "bottom")
    paste(hd, hoard(220, 74, seed=2), 680, 340, "bottom")
    paste(hd, hoard(160, 56, seed=5), 372, 334, "bottom")
    paste(hd, hoard(320, 110, seed=8), 110, 620, "bottom")
    paste(hd, hoard(240, 80, seed=11), 790, 640, "bottom")
    paste(hd, dragon_skull(0.8), 236, 360, "bottom")
    rib = Image.new("RGBA", (130, 64), (0, 0, 0, 0)); rd = ImageDraw.Draw(rib)
    for i in range(5):
        rd.arc([i * 18, 4, i * 18 + 50, 120], 200, 300, fill=C((30, 20, 26)), width=6)
        rd.arc([i * 18, 4, i * 18 + 50, 120], 200, 300, fill=C((214, 200, 170)), width=3)
    paste(hd, rib, 820, 470, "bottom")
    platform(hd, FOE, 116, 25, (70, 40, 66), (40, 22, 40), outline=(14, 6, 16))
    ring_stones(hd, FOE, 116, 25, [(232, 182, 60), (255, 230, 130), (190, 130, 40)], n=26, size=(5, 8), seed=4)
    platform(hd, PLAYER, *pb(116, 25), (70, 40, 66), (40, 22, 40), outline=(14, 6, 16), thick=12)
    ring_stones(hd, PLAYER, *pb(116, 25), [(232, 182, 60), (255, 230, 130), (190, 130, 40)], n=30, size=(7, 12), seed=9)
    save_room("field_dragons_den", hd)
    gold = mask_from(hd, lambda r, g, b: (r > 225) & (g > 170) & (b < 120))
    layers = [
        layer(F, "magma", glow_from_mask(lava, (255, 110, 50), radius=9, gain=1.3), z=1, blend=1,
              opacity=140, anim=S("pulse"), min=50, max=170, period=130),
        layer(F, "violet", soft_glow((520, 230), 330, (170, 60, 255), alpha=120, squash=0.5), z=1, blend=1,
              anim=S("pulse"), min=30, max=120, period=190, phase=1.5),
        layer(F, "goldglint", glow_from_mask(gold, (255, 220, 120), radius=3, gain=0.8, core=0.4), z=1, blend=1,
              opacity=120, anim=S("pulse"), min=40, max=150, period=70),
    ]
    haze = fog_strip(864, 180, (150, 60, 170), seed=13, scale=32, density=0.6, alpha=80)
    extras = {"img001": ebdx_stock("decor009", scrolling=True, speed=1, direction=1, oy=0, z=3, flat=True,
                                   opacity=90),
              "img003": strip(F, "haze", haze, 230, speed=0.5, direction=-1, z=4)}
    return {"profile": {S("art_extras"): extras, S("layers"): layers},
            "origins": [[REJ, "battlebgVolcano (2x crop of the great wall and lava fall, gradient-mapped violet, lava kept as magma)"],
                        [EBDX, "decor009"],
                        [OWN, "wyrm statues, dragon skull and ribs, gold hoard, coin-ringed platforms, glows"]]}


#---------------------------------------------------------------------------------------------
# DESERT: Duneholt dunes, mesas, half-buried ruins
#---------------------------------------------------------------------------------------------
def desert():
    F = "desert"
    hd = vanilla("reborn", "Desert", base=False)
    hz = 150 + 96            # horizon (HD y)
    far = mountains((864, 693), hz + 4, 70, (214, 150, 96), seed=3, rough=0.2, peaks=3)
    a = arr(far); ys = np.arange(693)[:, None]
    # mesas: flatten the tops
    hd = blend(hd, far, "normal", 0.55)
    mid = mountains((864, 693), hz + 14, 54, (176, 104, 62), seed=8, rough=0.1, peaks=2,
                    outline=(120, 66, 40))
    ma = arr(mid)
    tops = np.argmax(ma[..., 3] > 0, axis=0)
    flat = np.minimum.accumulate(np.maximum(tops, np.percentile(tops, 25)))
    hd.alpha_composite(posterize_alpha(mid, 2))
    # ruins: broken sandstone columns sinking into the dunes
    sand = (232, 196, 128); sdark = (168, 120, 70)
    for x, top, bot, w in ((300, 252, 330, 20), (334, 286, 330, 18), (700, 232, 318, 24), (742, 270, 320, 18),
                           (110, 400, 520, 30)):
        pillar(hd, x, top, bot, w, (214, 168, 104), (240, 212, 150), (150, 106, 62), (90, 58, 30),
               cap=(top < 260))
        d = ImageDraw.Draw(hd)
        d.chord([x - w * 2, bot - 14, x + w * 2, bot + 18], 180, 360, fill=C(sand))
        d.arc([x - w * 2, bot - 14, x + w * 2, bot + 18], 200, 340, fill=C(lighter(sand, 0.3)))
    d = ImageDraw.Draw(hd)
    d.line([(334, 282), (300, 252)], fill=C((90, 58, 30)), width=1)
    plat_pair(hd, (222, 178, 112), (160, 112, 64), speckle=([(200, 150, 90), (240, 210, 150)], 160))
    # broken arch on the far dune
    shade_rect(d, 262, 196, 380, 214, C((214, 168, 104)), C((240, 212, 150)), C((150, 106, 62)), C((90, 58, 30)))
    d.polygon([(380, 196), (396, 204), (380, 214)], fill=C((150, 106, 62)), outline=C((90, 58, 30)))
    hd = blend(hd, vgradient(HD, [(0, (255, 250, 220, 120)), (0.35, (255, 240, 200, 0)), (1, (0, 0, 0, 0))]), "screen")
    save_room("field_desert", hd)
    sun = soft_glow((720, 120), 260, (255, 250, 210), alpha=170, squash=1.0)
    haze = fog_strip(864, 90, (255, 240, 200), seed=17, scale=10, density=0.5, alpha=60)
    layers = [layer(F, "sun", sun, z=1, blend=1, anim=S("pulse"), min=90, max=170, period=200)]
    extras = {"img001": strip(F, "haze", haze, 205, speed=1, direction=1, z=3),
              "img002": strip(F, "haze2", fog_strip(864, 110, (240, 200, 140), seed=19, scale=20, density=0.5,
                                                    alpha=70), 400, speed=2, direction=1, z=24)}
    return {"profile": {S("art_extras"): extras, S("layers"): layers},
            "origins": [[REB, "battlebgDesert (extended)"],
                        [OWN, "mesas, half-buried sandstone ruins, sandstone slab platforms, sun glare, heat haze"]]}


#---------------------------------------------------------------------------------------------
# CAVE: Velmoran mine-cave, timber supports, lantern-lit path
#---------------------------------------------------------------------------------------------
def cave():
    F = "cave"
    src = game_img("rejuvenation", "battlebgCave")
    bg = src.crop((200, 30, 456, 174)).resize((512, 288), Image.NEAREST)   # 2x: deep in the tunnel mouth
    hd = extend_vanilla(bg, origin=O)
    eb = game_img("rejuvenation", "enemybaseCave")
    place_foe_base(hd, eb); place_player_base_scaled(hd, eb)
    hd = grade(hd, mul=(0.92, 0.9, 0.95), sat=0.9)
    wood, wdark, wout = (122, 84, 52), (78, 52, 32), (30, 18, 10)
    d = ImageDraw.Draw(hd)
    # timber supports: two posts + crossbeam, near and far
    for (xl, xr, top, bot, w) in ((250, 470, 170, 318, 12), (60, 830, 40, 600, 22)):
        for x in (xl, xr):
            shade_rect(d, x - w // 2, top, x + w // 2, bot, C(wood), C(lighter(wood, 0.25)), C(wdark), C(wout))
        shade_rect(d, xl - w, top - w, xr + w, top, C(wood), C(lighter(wood, 0.25)), C(wdark), C(wout))
        d.line([(xl + w, top + 2), (xl + w * 3, top - w + 2)], fill=C(wout))
    # stalactites
    rng = random.Random(4)
    for _ in range(26):
        x = rng.uniform(150, 720); L = rng.uniform(14, 46); wd = rng.uniform(5, 12)
        y0 = rng.uniform(150, 175) if rng.random() < 0.6 else rng.uniform(0, 60)
        d.polygon([(x - wd, y0), (x + wd, y0), (x, y0 + L)], fill=C((70, 56, 50)), outline=C((26, 18, 16)))
        d.line([(x - wd + 2, y0 + 1), (x - 1, y0 + L - 4)], fill=C((110, 92, 80)))
    # lantern-lit path: warm pools on the floor
    pool = soft_glow((520, 360), 220, (255, 190, 110), alpha=90, squash=0.28)
    hd.alpha_composite(posterize_alpha(pool, 5))
    save_room("field_cave", hd)
    layers = []
    for i, (x, y, len_) in enumerate(((360, 156, 20), (140, 26, 40))):
        lm = lamp()
        ch = chain(len_)
        im = blank(); paste(im, ch, x - ch.width / 2, y); paste(im, lm, x - lm.width / 2, y + len_ - 2)
        layers.append(layer(F, "lantern%d" % i, im, anchor=(x, y), z=3 if i == 0 else 30, anim=S("sway"),
                            amp=3, period=160 + i * 40))
        layers.append(layer(F, "lanternglow%d" % i, soft_glow((x, y + len_ + 14), 70 + i * 40, (255, 190, 100),
                                                               alpha=150), z=3 if i == 0 else 30, blend=1,
                            anim=[S("pulse"), S("flicker")], min=90, max=150, period=50, chance=0.01, dropout=3))
    extras = {
        "img001": ebdx_stock("decor006", scrolling=True, speed=2, direction=-1, oy=0, z=3, flat=True, opacity=120),
        "img002": ebdx_stock("decor009", scrolling=True, speed=1, direction=1, oy=0, z=3, flat=True, opacity=80),
        "img003": ebdx_stock("fog", scrolling=True, speed=0.5, direction=1, oy=0, z=4, flat=True, opacity=160),
    }
    fx = [P(type=":drift", count=12, shape=":dot", size=2, colors=DUST, speed=[0.1, 0.3], sway=5, zoom=[0.5, 0.8],
            opacity=[70, 140], layers=[":back", ":mid"]),
          P(type=":fall", count=4, shape=":rect", w=1, h=3, colors=[[170, 200, 230]], area=[60, 60, 330, 240],
            speed=[2.0, 3.0], sway=0, zoom=[0.6, 0.9], opacity=[120, 200], layers=[":back", ":mid"])]
    return {"profile": {S("art_extras"): extras, S("layers"): layers, S("fx"): fx},
            "origins": [[REJ, "battlebgCave (2x crop of the tunnel mouth), enemybaseCave"],
                        [EBDX, "decor006, decor009, fog (the CAVE environment's layers)"],
                        [OWN, "timber mine supports, stalactites, hanging lanterns, lantern light"]]}


#---------------------------------------------------------------------------------------------
# CRYSTAL_CAVERN / DARK_CRYSTAL: one layout (the crystals die in the transition)
#---------------------------------------------------------------------------------------------
CLUSTERS = [((236, 330), 150, 1), ((700, 318), 120, 2), ((420, 300), 70, 3), ((96, 560), 230, 4),
            ((790, 600), 190, 5)]


def _clusters(hd, palette, outline, glowcol, F, dim=False):
    glows = blank()
    for foot, sc, seed in CLUSTERS:
        crystal_cluster(hd, foot, sc, palette, seed=seed, n=6, outline=outline)
        glows.alpha_composite(soft_glow((foot[0], foot[1] - sc * 0.5), sc * 0.9, glowcol, alpha=150))
    return glows


def crystal_cavern():
    F = "crystal_cavern"
    hd = vanilla("rejuvenation", "CrystalCavern", mirror=True)
    hd = grade(hd, mul=(0.95, 0.98, 1.06), sat=1.05)
    pal = [(140, 230, 255), (190, 150, 255), (255, 170, 230), (150, 255, 220)]
    glows = _clusters(hd, pal, (30, 26, 60), (150, 220, 255), F)
    save_room("field_crystal_cavern", hd)
    shine = mask_from(hd, lambda r, g, b: (np.maximum(np.maximum(r, g), b) > 200) &
                      ((np.maximum(np.maximum(r, g), b) - np.minimum(np.minimum(r, g), b)) > 70))
    layers = [
        layer(F, "glow", glows, z=1, blend=1, anim=S("pulse"), min=40, max=140, period=140),
        layer(F, "shine", glow_from_mask(shine, (200, 240, 255), radius=4, gain=1.0, core=0.5), z=1, blend=1,
              anim=S("pulse"), min=30, max=130, period=90, phase=2.0),
    ]
    for i, (x, col) in enumerate(((300, (150, 220, 255)), (520, (230, 160, 255)), (680, (160, 255, 220)))):
        layers.append(layer(F, "shaft%d" % i, cone(HD, (x + 60, 0), 14, 420, col, alpha=70, angle=100), z=2,
                            blend=1, anim=S("pulse"), min=20, max=90, period=180 + i * 50, phase=i * 2.0))
    fx = [P(type=":twinkle", count=22, shape=":spark", size=7, colors=[[200, 255, 255], [255, 255, 255],
                                                                       [230, 190, 255]],
            speed=[3, 7], zoom=[0.5, 1.0], opacity=[170, 255], layers=[":back", ":mid"], blend=1),
          P(type=":drift", count=10, shape=":dot", size=2, colors=[[200, 255, 255], [240, 200, 255]],
            speed=[0.2, 0.4], sway=6, zoom=[0.5, 0.8], opacity=[90, 160], layers=[":mid", ":front"], blend=1)]
    return {"profile": {S("layers"): layers, S("fx"): fx},
            "origins": [[REJ, "battlebgCrystalCavern (mirrored), enemybaseCrystalCavern"],
                        [OWN, "giant prismatic crystal clusters, crystal glow, prismatic light shafts"]]}


def dark_crystal():
    F = "dark_crystal"
    hd = vanilla("rejuvenation", "DarkCrystalCavern", mirror=True)
    pal = [(54, 34, 84), (80, 50, 120), (36, 24, 60), (110, 70, 160)]
    glows = _clusters(hd, pal, (10, 6, 18), (140, 60, 255), F)
    hd = grade(hd, mul=(0.9, 0.86, 1.0))
    save_room("field_dark_crystal", hd)
    layers = [layer(F, "glow", glows, z=1, blend=1, anim=S("pulse"), min=10, max=80, period=200)]
    extras = {"vacuum": "dark006",
              "img003": strip(F, "murk", fog_strip(864, 200, (60, 30, 90), seed=23, scale=30, density=0.6,
                                                   alpha=110), 230, speed=0.5, direction=-1, z=4)}
    return {"profile": {S("art_extras"): extras, S("layers"): layers},
            "origins": [[REJ, "battlebgDarkCrystalCavern (mirrored), enemybaseDarkCrystalCavern"],
                        [EBDX, "dark006 (vacuum rings)"],
                        [OWN, "obsidian crystal clusters (same placement as Crystal Cavern), dying glow, murk"]]}


#---------------------------------------------------------------------------------------------
# COLOSSEUM: Ironreach pit ring in an old mine shaft
#---------------------------------------------------------------------------------------------
def crowd_sheet(w, h, seed=0, color=(30, 22, 26), rim=(200, 140, 80), frames=2):
    rng = random.Random(seed)
    sheet = Image.new("RGBA", (w * frames, h), (0, 0, 0, 0))
    people = []
    x = 2
    while x < w - 4:
        people.append((x, rng.randint(10, 16), rng.random() < 0.45, rng.randint(0, 6)))
        x += rng.randint(9, 14)
    for f in range(frames):
        d = ImageDraw.Draw(sheet)
        ox = f * w
        for (px, hw, cheer, dy) in people:
            up = (f + dy) % 2 == 0 and cheer
            top = h - 26 - dy - (3 if up else 0)
            d.ellipse([ox + px, top, ox + px + 9, top + 9], fill=C(color))
            d.rectangle([ox + px - 2, top + 8, ox + px + 11, h], fill=C(color))
            d.line([ox + px + 1, top + 1, ox + px + 1, top + 5], fill=C(rim))
            if cheer:
                ay = top - 8 if up else top + 4
                d.line([ox + px - 1, top + 10, ox + px - 4, ay], fill=C(color), width=3)
                d.line([ox + px + 10, top + 10, ox + px + 13, ay], fill=C(color), width=3)
    return sheet


def colosseum():
    F = "colosseum"
    hd = vanilla("rejuvenation", "Colosseum")
    # sand over the pit floor
    W, H = HD
    sandn = noise(HD, 3, 31, 2)
    a = arr(hd)
    ys = np.arange(H)[:, None]
    floor = (ys > 150 + 150) & np.ones((1, W), bool)
    sand = np.stack([200 + sandn * 30, 160 + sandn * 26, 104 + sandn * 18, np.full_like(sandn, 255)], -1)
    t = np.clip((ys - 300) / 40.0, 0, 1)[..., None] * 0.55
    a = np.where(floor[..., None], a * (1 - t) + sand * t, a)
    hd = img(a)
    eb = game_img("rejuvenation", "enemybaseColosseum")
    place_foe_base(hd, eb); place_player_base_scaled(hd, eb)
    # crowd on scaffolding in the arches + chain-link fence
    cs = crowd_sheet(864, 60, seed=3)
    d = ImageDraw.Draw(hd)
    for y in (232, 268):
        d.rectangle([0, y, 864, y + 4], fill=C((70, 58, 46)), outline=C((24, 18, 14)))
    for x in range(10, 864, 64):
        d.rectangle([x, 200, x + 4, 300], fill=C((70, 58, 46)), outline=C((24, 18, 14)))
    fence = blank()
    fd = ImageDraw.Draw(fence)
    for x in range(-200, 1000, 10):
        fd.line([(x, 190), (x + 110, 300)], fill=(150, 150, 160, 110))
        fd.line([(x + 110, 190), (x, 300)], fill=(150, 150, 160, 110))
    fd.rectangle([0, 186, 864, 190], fill=(110, 110, 120, 255))
    fd.rectangle([0, 298, 864, 302], fill=(90, 90, 100, 255))
    for x in range(0, 864, 96):
        fd.rectangle([x, 186, x + 4, 302], fill=(100, 100, 110, 255))
    save_room("field_colosseum", hd)
    name = "pf_colosseum_crowd"
    save_element(name, cs)
    layers = [P(bitmap=name, hd=True, x=0.0, y=round(212 / 2.25, 2), ox=0, oy=0, z=1, frames=2, frame_time=14)]
    layers.append(layer(F, "fence", fence, z=2))
    for i, x in enumerate((300, 560, 760, 120)):
        im = blank(); ch = chain(70 if i < 2 else 40); lm = lamp((255, 230, 160))
        paste(im, ch, x - ch.width / 2, 0); paste(im, lm, x - lm.width / 2, ch.height - 2)
        layers.append(layer(F, "lamp%d" % i, im, anchor=(x, 0), z=3 if i < 2 else 30, anim=S("sway"), amp=2.5,
                            period=170 + i * 31))
        layers.append(layer(F, "cone%d" % i, cone(HD, (x, ch.height + 16), 40, 330, (255, 220, 150), alpha=60),
                            z=3 if i < 2 else 30, blend=1, anim=S("pulse"), min=60, max=110, period=90 + i * 17))
    fx = [P(type=":drift", count=16, shape=":dot", size=2, colors=DUST, speed=[0.2, 0.5], sway=6, zoom=[0.5, 0.9],
            opacity=[80, 150], layers=[":back", ":mid", ":front"]),
          P(type=":flash", color=[255, 240, 200], alpha=40, interval=[200, 400], decay=8)]
    return {"profile": {S("layers"): layers, S("fx"): fx},
            "origins": [[REJ, "battlebgColosseum, enemybaseColosseum (sanded floor)"],
                        [OWN, "cheering crowd (2-frame sheet), scaffolding, chain-link fence, hanging work lamps"]]}


#---------------------------------------------------------------------------------------------
# MOUNTAIN / SNOWY_MOUNTAIN / FROZEN_LAKE
#---------------------------------------------------------------------------------------------
def sky(top, bottom, horizon_y, below=None):
    g = vgradient(HD, [(0, C(top)), (horizon_y / 693.0, C(bottom)), (1, C(below or bottom))])
    return g


def mountain():
    F = "mountain"
    hd = vanilla("reborn", "Mountain", base="Mountain")
    hz = 150 + 100
    sk = sky((120, 170, 220), (220, 232, 236), hz)
    hd = blend(hd, sk, "normal", mask=np.clip((hz + 10 - np.arange(693)) / 40.0, 0, 1)[:, None] * np.ones((1, 864)))
    far = mountains((864, 693), hz + 6, 120, (150, 168, 196), seed=11, rough=0.6, peaks=4,
                    snow=(236, 244, 250))
    hd.alpha_composite(far)
    mid = mountains((864, 693), hz + 40, 90, (92, 110, 104), seed=12, rough=0.7, peaks=6, outline=(54, 66, 62))
    hd.alpha_composite(mid)
    eb = game_img("reborn", "enemybaseMountain")
    place_foe_base(hd, eb); place_player_base_scaled(hd, eb)
    clouds = cloud_band(864, 90, (255, 255, 255), (200, 214, 230), seed=3, density=0.42, scale=18)
    layers = []
    rng = random.Random(7)
    pines = blank()
    for i in range(14):
        x = rng.uniform(0, 864); y = hz + 30 + rng.uniform(0, 30)
        if 380 < x < 680 and y > hz + 20:
            continue
        p = pine(int(rng.uniform(40, 70)), (46, 70, 60), (16, 26, 22), seed=i)
        paste(pines, p, x, y, "bottom")
    hd.alpha_composite(pines)
    save_room("field_mountain", hd)
    for i, (x, h) in enumerate(((176, 150), (770, 170))):
        p = pine(h, (40, 64, 54), (14, 24, 20), seed=40 + i)
        layers.append(layer(F, "pine%d" % i, onto(p, x - p.width / 2, 470 - p.height + 8), anchor=(x, 470),
                            z=22, anim=S("sway"), amp=1.5, period=130 + i * 40, angle=-4))
    extras = {"img001": strip(F, "clouds", clouds, 70, speed=0.5, direction=1, z=1),
              "img002": strip(F, "mist", fog_strip(864, 70, (240, 246, 250), seed=4, scale=16, density=0.5,
                                                   alpha=100), 270, speed=1, direction=1, z=2)}
    fx = [P(type=":streak", count=8, shape=":rect", w=22, h=1, colors=[[255, 255, 255]], angle=178,
            speed=[4, 7], zoom=[0.6, 1.0], opacity=[50, 110], layers=[":back", ":front"]),
          P(type=":drift", count=8, shape=":dot", size=2, colors=[[120, 160, 90], [170, 190, 110]], dir=-1,
            speed=[1.0, 2.0], sway=10, zoom=[0.6, 1.0], opacity=[140, 220], spin=8, layers=[":mid", ":front"])]
    return {"profile": {S("art_extras"): extras, S("layers"): layers, S("fx"): fx},
            "origins": [[REB, "battlebgMountain, enemybaseMountain"],
                        [OWN, "sky, layered snow-capped ridges, pines, clouds, valley mist"]]}


def prayer_flags(w, sag, colors, seed=0):
    im = Image.new("RGBA", (w, sag + 22), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    pts = [(x, 2 + sag * math.sin(x / w * math.pi)) for x in range(0, w + 1, 4)]
    d.line(pts, fill=(60, 50, 40, 255))
    for i, x in enumerate(range(8, w - 8, 16)):
        y = 2 + sag * math.sin(x / w * math.pi)
        col = colors[i % len(colors)]
        d.rectangle([x - 5, y, x + 5, y + 12], fill=C(col), outline=C(darker(col, 0.5)))
    return im


def snowy_mountain():
    F = "snowy_mountain"
    hd = vanilla("reborn", "SnowyMountain", base="SnowyMountain")
    hz = 150 + 80
    far = mountains((864, 693), hz + 10, 130, (176, 196, 222), seed=21, rough=0.7, peaks=3, snow=(250, 252, 255))
    hd.alpha_composite(far)
    near = mountains((864, 693), hz + 70, 120, (206, 220, 240), seed=22, rough=0.8, peaks=5,
                     outline=(120, 140, 180))
    hd.alpha_composite(near)
    d = ImageDraw.Draw(hd)
    rng0 = random.Random(23)
    for _ in range(14):
        x = rng0.uniform(0, 864); y = rng0.uniform(hz - 10, hz + 60)
        if not (arr(near)[int(min(y, 692)), int(min(x, 863)), 3] > 0):
            continue
        w0 = rng0.uniform(10, 28)
        d.polygon([(x - w0, y + 8), (x - w0 * 0.3, y - 6), (x + w0 * 0.5, y - 2), (x + w0, y + 8)],
                  fill=C((70, 80, 100)), outline=C((40, 46, 62)))
        d.line([(x - w0 * 0.3, y - 5), (x + w0 * 0.5, y - 1)], fill=C((240, 246, 255)), width=2)
    rng = random.Random(3)
    for i in range(10):
        x = rng.uniform(0, 864)
        if 360 < x < 700:
            continue
        paste(hd, pine(int(rng.uniform(46, 80)), (40, 66, 70), (14, 24, 28), snow=(250, 252, 255), seed=i),
              x, hz + 90 + rng.uniform(0, 30), "bottom")
    if not has_game_img("reborn", "enemybaseSnowyMountain"):
        plat_pair(hd, (236, 242, 250), (170, 186, 210))
    hd = grade(hd, mul=(0.9, 0.95, 1.04), contrast=1.08)
    save_room("field_snowy_mountain", hd)
    flags = prayer_flags(420, 40, [(220, 40, 40), (250, 210, 60), (60, 160, 80), (250, 250, 250), (50, 90, 200)])
    layers = [layer(F, "flags", onto(flags, 420, 168), anchor=(630, 170), z=2, anim=S("sway"), amp=1.2,
                    period=90),
              layer(F, "flags2", onto(prayer_flags(360, 50, [(50, 90, 200), (250, 250, 250), (220, 40, 40),
                                                              (60, 160, 80), (250, 210, 60)]), 40, 120),
                    anchor=(220, 120), z=30, anim=S("sway"), amp=1.6, period=110)]
    extras = {"img001": strip(F, "spindrift", fog_strip(864, 120, (255, 255, 255), seed=5, scale=12,
                                                        density=0.5, alpha=120), 230, speed=3, direction=-1, z=3),
              "img002": strip(F, "blizzard", fog_strip(864, 200, (240, 246, 255), seed=6, scale=20, density=0.45,
                                                       alpha=70), 360, speed=4, direction=-1, z=26)}
    fx = [P(type=":fall", count=44, bitmap="snow", speed=[0.8, 1.8], sway=16, zoom=[0.2, 0.5],
            opacity=[200, 255], layers=[":back", ":mid", ":front"]),
          P(type=":streak", count=10, shape=":rect", w=18, h=1, colors=[[255, 255, 255]], angle=172,
            speed=[6, 9], zoom=[0.6, 1.0], opacity=[60, 130], layers=[":back", ":front"])]
    return {"profile": {S("art_extras"): extras, S("layers"): layers, S("fx"): fx},
            "origins": [[REB, "battlebgSnowyMountain" + (", enemybaseSnowyMountain" if has_game_img(
                "reborn", "enemybaseSnowyMountain") else "")],
                        [OWN, "summit ridges and cornices, snowy pines, prayer flags, spindrift, blizzard"]]}


def frozen_lake(night=False):
    F = "frozen_lake"
    hd = vanilla("rejuvenation", "Frozen", base="Frozen", player_base=None)   # placed below, raised (ROOM_PLAYER)
    hz = 150 + 128
    xs = np.arange(864)
    nn = noise((1, 864), 3, 31, 3)[0]
    rise = np.clip((np.abs(xs - 470) - 150) / 160.0, 0, 1) ** 0.7
    tops = hz + 2 - rise * 190 - nn * 18 * (rise > 0) - 6
    a = np.zeros((693, 864, 4), np.float32)
    ys = np.arange(693)[:, None]
    m = (ys >= tops[None, :]) & (ys <= hz + 4)
    a[m] = [92, 108, 140, 255]
    # snow on ledges + light faces
    ledge = m & ~np.vstack([m[:1] * 0, m[:-1]]).astype(bool)
    shade = noise((864, 693), 6, 32, 2)
    a[m & (shade > 0.58)] = [128, 146, 176, 255]
    a[m & (shade > 0.7)] = [228, 238, 250, 255]
    edge = np.zeros_like(m); edge[1:] = m[1:] & ~m[:-1]
    for k in range(3):
        e = np.roll(edge, k, axis=0)
        a[e & m] = [244, 248, 255, 255]
    hd.alpha_composite(img(a))
    rng = random.Random(9)
    for i in range(26):
        x = rng.uniform(0, 864)
        paste(hd, pine(int(rng.uniform(22, 40)), (36, 60, 70), (14, 22, 30), snow=(240, 248, 255), seed=i),
              x, hz + 6 + rng.uniform(-2, 4), "bottom")
    # ice cracks on the lake
    d = ImageDraw.Draw(hd)
    for i in range(14):
        x, y = rng.uniform(160, 760), rng.uniform(hz + 30, 680)
        for k in range(4):
            nx, ny = x + rng.uniform(-60, 60), y + rng.uniform(-12, 12)
            d.line([(x, y), (nx, ny)], fill=C((240, 252, 255)), width=2)
            d.line([(x, y + 2), (nx, ny + 2)], fill=C((40, 120, 170)), width=1)
            x, y = nx, ny
    eb = game_img("rejuvenation", "enemybaseFrozen")
    place_foe_base(hd, eb)
    place_player_base_scaled(hd, eb, scale=player_scale("FROZEN_LAKE"), at=player_at("FROZEN_LAKE"))
    if night:
        hd = grade(hd, mul=(0.45, 0.55, 0.75), add=(0, 6, 22))
        aur = blank()
        n = tile_noise(864, 200, 40, 77)
        ys = np.linspace(0, 1, 200)[:, None]
        band = np.exp(-((ys - 0.45 - 0.2 * np.sin(np.arange(864)[None, :] / 90.0)) ** 2) / 0.02)
        al = np.clip(band * (0.4 + n), 0, 1)
        aa = np.zeros((200, 864, 4), np.float32)
        aa[..., 0] = 80 + 120 * n; aa[..., 1] = 255; aa[..., 2] = 170 + 60 * (1 - n); aa[..., 3] = al * 140
        aur.alpha_composite(posterize_alpha(img(aa), 6), (0, 20))
        hd = blend(hd, aur, "screen")
        save_room("field_frozen_lake_night", hd)
        return
    save_room("field_frozen_lake", hd)
    layers = []
    fx = [P(type=":fall", count=30, bitmap="snow", speed=[0.6, 1.4], sway=12, zoom=[0.2, 0.45],
            opacity=[200, 255], layers=[":back", ":mid", ":front"]),
          P(type=":twinkle", count=12, shape=":spark", size=5, colors=[[220, 245, 255]], area=[0, 130, 384, 300],
            speed=[3, 6], zoom=[0.5, 0.9], opacity=[160, 255], layers=[":back", ":mid"], blend=1)]
    extras = {"img001": strip(F, "mist", fog_strip(864, 60, (240, 250, 255), seed=8, scale=14, density=0.5,
                                                   alpha=110), hz - 20, speed=0.5, direction=1, z=1)}
    return {"profile": {S("art_extras"): extras, S("fx"): fx},
            "origins": [[REJ, "battlebgFrozen, enemybaseFrozen"],
                        [OWN, "fjord cliffs, far-shore pines, ice cracks, lake mist; night variant with aurora"]]}


def frozen_lake_all():
    r = frozen_lake(False)
    frozen_lake(True)
    return r


#---------------------------------------------------------------------------------------------
# WASTELAND: Bleed-scarred dump under a jaundiced sky
#---------------------------------------------------------------------------------------------
def barrel(color=(120, 70, 40), outline=(26, 14, 8), tipped=False, k=1.6):
    W, H = int(30 * k), int(40 * k)
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([3, 4 * k, W - 4, H - 3], fill=C(color), outline=C(outline))
    d.ellipse([3, 0, W - 4, 8 * k], fill=C(lighter(color, 0.2)), outline=C(outline))
    d.ellipse([8, 2 * k, W - 9, 6 * k], fill=C(darker(color, 0.5)))
    for y in (12 * k, 26 * k):
        d.line([3, y, W - 4, y], fill=C(darker(color, 0.6)), width=3)
    d.line([7, 6 * k, 7, H - 4], fill=C(lighter(color, 0.3)), width=2)
    d.rectangle([W * 0.55, H * 0.45, W * 0.8, H * 0.62], fill=C((150, 220, 70)), outline=C(outline))
    return im.rotate(80, expand=True) if tipped else im


def wasteland():
    F = "wasteland"
    hd = vanilla("reborn", "Wasteland", base="Wasteland")
    hz = 150 + 92
    a = arr(hd)
    ys = np.arange(693)[:, None, None]
    skyw = np.clip((hz + 20 - ys) / 60.0, 0, 1)
    jaund = gradient_map(hd, [(0, (60, 54, 30)), (0.5, (170, 160, 80)), (1, (236, 226, 150))])
    ground = gradient_map(hd, [(0, (30, 24, 30)), (0.4, (78, 64, 66)), (0.75, (130, 112, 98)), (1, (190, 170, 140))])
    hd = img(arr(jaund) * skyw + arr(ground) * (1 - skyw))
    heaps = mountains((864, 693), hz + 30, 70, (52, 44, 48), seed=41, rough=0.9, peaks=7, outline=(28, 22, 26))
    hd.alpha_composite(heaps)
    rng = random.Random(5)
    for i, (x, y, h) in enumerate(((230, hz + 40, 110), (700, hz + 36, 130), (90, 470, 200), (820, 520, 180))):
        paste(hd, dead_tree(h, (46, 40, 38), (16, 12, 12), seed=i), x, y, "bottom")
    for (x, y, tip) in ((330, 318, False), (352, 322, True), (690, 312, False), (150, 600, True), (740, 640, False)):
        paste(hd, barrel(tipped=tip), x, y, "bottom")
    d = ImageDraw.Draw(hd)
    pools = blank()
    pd = ImageDraw.Draw(pools)
    for (x, y, rx, ry) in ((410, 330, 50, 9), (300, 520, 90, 18), (720, 460, 70, 14)):
        d.ellipse([x - rx, y - ry, x + rx, y + ry], fill=C((90, 170, 60)), outline=C((30, 50, 20)))
        d.ellipse([x - rx * 0.6, y - ry * 0.6, x + rx * 0.3, y + ry * 0.2], fill=C((150, 220, 90)))
        pd.ellipse([x - rx - 20, y - ry - 12, x + rx + 20, y + ry + 12], fill=(140, 255, 90, 255))
    plat_pair(hd, (74, 66, 66), (40, 34, 38), outline=(16, 12, 14),
              speckle=([(110, 100, 90), (50, 44, 46), (130, 160, 70)], 220))
    save_room("field_wasteland", hd)
    pg = pools.filter(ImageFilter.GaussianBlur(10))
    layers = [layer(F, "pools", posterize_alpha(pg, 6), z=1, blend=1, opacity=110, anim=S("pulse"), min=40,
                    max=120, period=100)]
    extras = {"img001": strip(F, "smog", fog_strip(864, 140, (170, 160, 90), seed=44, scale=26, density=0.6,
                                                   alpha=90), 200, speed=1, direction=1, z=3)}
    fx = [vent(330, 300, count=6, colors=SMOKE, rise=110, size=20, opacity=(60, 110)),
          vent(700, 296, count=6, colors=SMOKE, rise=110, size=20, opacity=(60, 110)),
          P(type=":rise", count=12, shape=":glow", size=5, colors=[[150, 230, 80], [190, 255, 120]],
            area=[100, 140, 340, 300], speed=[0.3, 0.7], sway=6, zoom=[0.4, 0.8], opacity=[120, 200],
            layers=[":back", ":mid"], blend=1),
          P(type=":drift", count=10, shape=":dot", size=2, colors=ASH, speed=[0.6, 1.2], sway=4, zoom=[0.5, 0.8],
            opacity=[90, 150], layers=[":back", ":mid"])]
    return {"profile": {S("art_extras"): extras, S("layers"): layers, S("fx"): fx},
            "origins": [[REB, "battlebgWasteland (sky re-graded), enemybaseWasteland"],
                        [OWN, "slag heaps, dead trees, rusted barrels, glowing toxic pools, smog"]]}


BUILDERS = {"VOLCANIC": volcanic, "ASHEN_WASTE": ashen_waste, "DRAGONS_DEN": dragons_den, "DESERT": desert,
            "CAVE": cave, "CRYSTAL_CAVERN": crystal_cavern, "DARK_CRYSTAL": dark_crystal, "COLOSSEUM": colosseum,
            "MOUNTAIN": mountain, "SNOWY_MOUNTAIN": snowy_mountain, "FROZEN_LAKE": frozen_lake_all,
            "WASTELAND": wasteland}
