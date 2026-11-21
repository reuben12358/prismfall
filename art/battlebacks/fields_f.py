"""Round 3: painted sources (aveontrainer, carchagui, princess-phoenix, Rejuvenation painted rooms) replace the
blurred-gradient / procedural bases of DESERT, MOUNTAIN, SNOWY_MOUNTAIN, WASTELAND, CAVE, NEW_MOON, INVERSE,
PRISM_ARENA and FLOWER_GARDEN 1-2; sheet-based geysers for Cinderglass; smooth lava for Dragon's Den."""
import fields_a, fields_b, fields_c, fields_d, fields_e
from bblib import *
from paint import *
from props import *
from rubygen import S
from fields_a import REJ, REB, DES, EBDX, OWN, O
from fields_d import capture, with_stages

MORG = "/home/claude/ref/art/morgebby/Graphics/Tilesets/Tilesets/"
AVEON = "aveontrainer (DeviantArt battle backgrounds; credit)"
CARCH = "carchagui (DeviantArt backgrounds; credit)"
PPHX = "princess-phoenix (DeviantArt 'Some battle backgrounds'; credit)"


def art(name):
    return Image.open(MORG + name).convert("RGBA")


def room_from(bg, origin=O, **kw):
    return extend_vanilla(bg, origin=origin, **kw)


def sheet_layer(F, tag, sheet, x, y, frames, frame_time, z=2, zoom=1.0, phase=0, **kw):
    name = "pf_%s_%s" % (F, tag)
    save_element(name, sheet)
    fw, fh = sheet.width // frames, sheet.height
    return P(bitmap=name, hd=True, x=round(x / 2.25, 2), y=round(y / 2.25, 2), ox=fw // 2, oy=fh, z=z,
             frames=frames, frame_time=frame_time, zoom=zoom, phase_frames=phase, **kw)


#---------------------------------------------------------------------------------------------
def desert_base():
    """aveontrainer's dunes, extended; above the horizon the sky simply continues (skies.extend_with_sky), so no
    upside-down mesa hangs over the room when EBDX's camera pulls back. Shared by FLOODED_DUNES / GLASS_DUNES."""
    import skies
    return skies.extend_with_sky(art("battlebgdesert_by_aveontrainer_ddp4tzl.png"), origin=O)


def desert():
    F = "desert"
    hd = desert_base()
    fields_a.plat_pair(hd, (236, 196, 120), (176, 126, 70), speckle=([(214, 168, 100), (250, 226, 160)], 160))
    fields_a.save_room("field_desert", hd)
    layers = [layer(F, "sun", soft_glow((212, 176), 150, (255, 252, 220), alpha=190), z=1, blend=1, anim=S("pulse"),
                    min=100, max=190, period=200),
              layer(F, "devil", cone(HD, (640, 330), 16, 150, (240, 214, 160), alpha=120, angle=-90), z=2,
                    anim=[S("drift"), S("pulse")], amp=40, min=30, max=120, period=260)]
    extras = {"img001": strip(F, "haze", fog_strip(864, 90, (255, 240, 200), seed=17, scale=10, density=0.5, alpha=60),
                              230, speed=1, direction=1, z=3),
              "img002": strip(F, "haze2", fog_strip(864, 110, (240, 200, 140), seed=19, scale=20, density=0.5,
                                                    alpha=60), 420, speed=2, direction=1, z=24)}
    return {"profile": {S("art_extras"): extras, S("layers"): layers},
            "origins": [[AVEON, "battlebgdesert (painted dunes, mesas and cacti; extended)"],
                        [OWN, "sandstone platforms, sun glare, dust devil, heat haze"]]}


def mountain():
    F = "mountain"
    hd = room_from(art("battlebgwaterfall_by_aveontrainer_ddpcj8m.png"))
    eb = game_img("reborn", "enemybaseMountain")
    place_foe_base(hd, eb); place_player_base_scaled(hd, eb)
    fields_a.save_room("field_mountain", hd)
    fall = Image.new("RGBA", (864, 60), (0, 0, 0, 0)); d = ImageDraw.Draw(fall)
    rng = random.Random(3)
    for _ in range(260):
        x, y = rng.uniform(0, 864), rng.uniform(0, 60)
        d.line([(x, y), (x + rng.uniform(4, 14), y + rng.uniform(-1, 1))], fill=(255, 255, 255, 170))
    hawk = Image.new("RGBA", (22, 10), (0, 0, 0, 0)); g = ImageDraw.Draw(hawk)
    g.line([(0, 2), (6, 0), (11, 5), (16, 0), (22, 2)], fill=(50, 40, 36, 255), width=2)
    layers = [layer(F, "hawk", onto(hawk, 520, 176), anchor=(531, 181), z=1, anim=[S("drift"), S("bob")], amp=60,
                    period=420),
              layer(F, "spray", soft_glow((400, 216), 190, (255, 255, 255), alpha=120, squash=0.35), z=1, blend=1,
                    anim=S("pulse"), min=40, max=120, period=70)]
    extras = {"img001": strip(F, "foam", fall, 196, speed=2, direction=1, z=1, opacity=150),
              "img002": strip(F, "mist", fog_strip(864, 70, (240, 250, 255), seed=4, scale=16, density=0.5, alpha=110),
                              180, speed=1, direction=1, z=2)}
    fx = [P(type=":streak", count=8, shape=":rect", w=22, h=1, colors=[[255, 255, 255]], angle=178, speed=[4, 7],
            zoom=[0.6, 1.0], opacity=[50, 110], layers=[":back", ":front"]),
          P(type=":rise", count=10, shape=":dot", size=2, colors=[[255, 255, 255], [210, 235, 255]],
            area=[90, 80, 300, 110], speed=[0.3, 0.7], sway=6, zoom=[0.5, 0.9], opacity=[150, 230], layers=[":back"])]
    return {"profile": {S("art_extras"): extras, S("layers"): layers, S("fx"): fx},
            "origins": [[AVEON, "battlebgwaterfall (painted highland tarn, crags and falls; extended)"],
                        [REB, "enemybaseMountain"],
                        [OWN, "moving foam on the falls, spray glow, mist, circling hawk, wind"]]}


def _cave_panel(i):
    sh = art("cave_background_by_carchagui_dd9gvd4.png")
    y0 = (0, 195, 390, 585)[i]
    return sh.crop((0, y0, 322, y0 + 194)).resize((644, 388), Image.NEAREST)


def snowy():
    F = "snowy_mountain"
    hd = room_from(_cave_panel(2), origin=(92, 148))
    hd = grade(hd, mul=(0.96, 1.0, 1.06), contrast=1.05)
    fields_a.plat_pair(hd, (236, 242, 252), (160, 178, 210), outline=(70, 90, 130))
    fields_a.save_room("field_snowy_mountain", hd)
    cols = [(220, 40, 40), (250, 210, 60), (60, 160, 80), (250, 250, 250), (50, 90, 200)]
    layers = [layer(F, "flags", onto(fields_a.prayer_flags(400, 36, cols), 300, 156), anchor=(500, 158), z=2,
                    anim=S("sway"), amp=1.2, period=90),
              layer(F, "glint", soft_glow((330, 430), 220, (220, 240, 255), alpha=90, squash=0.3), z=1, blend=1,
                    anim=S("pulse"), min=20, max=90, period=110)]
    extras = {"img001": strip(F, "spindrift", fog_strip(864, 120, (255, 255, 255), seed=5, scale=12, density=0.5,
                                                        alpha=110), 250, speed=3, direction=-1, z=3),
              "img002": strip(F, "blizzard", fog_strip(864, 200, (240, 246, 255), seed=6, scale=20, density=0.45,
                                                       alpha=70), 380, speed=4, direction=-1, z=26)}
    fx = [P(type=":fall", count=44, bitmap="snow", speed=[0.8, 1.8], sway=16, zoom=[0.2, 0.5], opacity=[200, 255],
            layers=[":back", ":mid", ":front"]),
          P(type=":streak", count=10, shape=":rect", w=18, h=1, colors=[[255, 255, 255]], angle=172, speed=[6, 9],
            zoom=[0.6, 1.0], opacity=[60, 130], layers=[":back", ":front"])]
    return {"profile": {S("art_extras"): extras, S("layers"): layers, S("fx"): fx},
            "origins": [[CARCH, "cave_background, snow panel at 2x (snowbound summit hollow)"],
                        [OWN, "snow platforms, prayer flags, spindrift, blizzard, ice glint"]]}


def cave():
    F = "cave"
    hd = room_from(_cave_panel(1), origin=(92, 148))
    eb = game_img("rejuvenation", "enemybaseCave")
    place_foe_base(hd, eb); place_player_base_scaled(hd, eb)
    wood, wdark, wout = (122, 84, 52), (78, 52, 32), (30, 18, 10)
    d = ImageDraw.Draw(hd)
    for (xl, xr, top, bot, w) in ((176, 318, 196, 300, 10),):      # timbered mouth of the left tunnel
        for x in (xl, xr):
            shade_rect(d, x - w // 2, top, x + w // 2, bot, C(wood), C(lighter(wood, 0.25)), C(wdark), C(wout))
        shade_rect(d, xl - w, top - w, xr + w, top, C(wood), C(lighter(wood, 0.25)), C(wdark), C(wout))
    hd.alpha_composite(posterize_alpha(soft_glow((500, 380), 240, (255, 190, 110), alpha=70, squash=0.28), 5))
    fields_a.save_room("field_cave", hd)
    layers = []
    for i, (x, y, L) in enumerate(((247, 188, 22), (640, 150, 40))):
        im = blank(); ch = chain(L); lm = lamp()
        paste(im, ch, x - ch.width / 2, y); paste(im, lm, x - lm.width / 2, y + L - 2)
        layers.append(layer(F, "lantern%d" % i, im, anchor=(x, y), z=3, anim=S("sway"), amp=3, period=160 + i * 40))
        layers.append(layer(F, "lanternglow%d" % i, soft_glow((x, y + L + 14), 80, (255, 190, 100), alpha=150), z=3,
                            blend=1, anim=[S("pulse"), S("flicker")], min=90, max=150, period=50, chance=0.01,
                            dropout=3))
    extras = {"img001": ebdx_stock("decor006", scrolling=True, speed=2, direction=-1, oy=0, z=3, flat=True, opacity=110),
              "img003": ebdx_stock("fog", scrolling=True, speed=0.5, direction=1, oy=0, z=4, flat=True, opacity=150)}
    fx = [P(type=":drift", count=12, shape=":dot", size=2, colors=DUST, speed=[0.1, 0.3], sway=5, zoom=[0.5, 0.8],
            opacity=[70, 140], layers=[":back", ":mid"]),
          P(type=":fall", count=4, shape=":rect", w=1, h=3, colors=[[170, 200, 230]], area=[60, 60, 330, 240],
            speed=[2.0, 3.0], sway=0, zoom=[0.6, 0.9], opacity=[120, 200], layers=[":back", ":mid"])]
    return {"profile": {S("art_extras"): extras, S("layers"): layers, S("fx"): fx},
            "origins": [[CARCH, "cave_background, earth panel at 2x (twin tunnel mouths)"],
                        [REJ, "enemybaseCave"], [EBDX, "decor006, fog"],
                        [OWN, "timbered tunnel mouth, hanging lanterns and lantern light"]]}


def wasteland():
    F = "wasteland"
    bg = art("battlebgswamp2_by_aveontrainer_dd2qjzq.png")
    a = arr(bg)
    water = (a[..., 2] > a[..., 0] + 6) & (a[..., 1] > a[..., 2]) & (a[..., :3].sum(-1) < 330) & (np.arange(288)[:, None] > 110)
    bg = gradient_map(bg, [(0, (22, 16, 22)), (0.3, (66, 54, 52)), (0.55, (118, 104, 80)), (0.8, (176, 166, 104)),
                           (1, (240, 232, 160))])
    b = arr(bg); b[water] = b[water] * 0.55 + np.array([90, 150, 50, 255], np.float32) * 0.45
    hd = room_from(img(b))
    wm = np.zeros((693, 864), np.float32); wm[150:438, 142:654] = water
    fields_a.plat_pair(hd, (74, 66, 66), (40, 34, 38), outline=(16, 12, 14),
                       speckle=([(110, 100, 90), (50, 44, 46), (130, 160, 70)], 220))
    for (x, y, tip) in ((330, 322, False), (356, 326, True), (24, 652, True)):   # off the player platform
        paste(hd, fields_a.barrel(tipped=tip), x, y, "bottom")
    d = ImageDraw.Draw(hd)
    x, y = 716, 330
    d.rectangle([x - 14, y - 34, x + 14, y], fill=C((110, 64, 40)), outline=C((30, 16, 10)))
    d.ellipse([x - 14, y - 40, x + 14, y - 28], fill=C((60, 34, 22)), outline=C((30, 16, 10)))
    fields_a.save_room("field_wasteland", hd)
    layers = [layer(F, "pools", glow_from_mask(wm, (150, 255, 90), radius=8, gain=0.9, core=0.2), z=1, blend=1,
                    anim=S("pulse"), min=30, max=110, period=100),
              fields_e.flame_layer(F, x, y - 32, 1.2, 2, seed=5),
              layer(F, "fireglow", soft_glow((x, y - 30), 110, (255, 150, 50), alpha=170), z=2, blend=1,
                    anim=[S("pulse"), S("flicker")], min=90, max=170, period=30, chance=0.02, dropout=2)]
    extras = {"img001": strip(F, "smog", fog_strip(864, 140, (170, 160, 90), seed=44, scale=26, density=0.6, alpha=80),
                              190, speed=1, direction=1, z=3)}
    fx = [vent(330, 290, count=5, colors=SMOKE, rise=110, size=20, opacity=(50, 100)),
          P(type=":rise", count=12, shape=":glow", size=5, colors=[[150, 230, 80], [190, 255, 120]],
            area=[60, 110, 330, 200], speed=[0.3, 0.7], sway=6, zoom=[0.4, 0.8], opacity=[120, 200],
            layers=[":back", ":mid"], blend=1),
          P(type=":drift", count=10, shape=":dot", size=2, colors=ASH, speed=[0.6, 1.2], sway=4, zoom=[0.5, 0.8],
            opacity=[90, 150], layers=[":back", ":mid"])]
    return {"profile": {S("art_extras"): extras, S("layers"): layers, S("fx"): fx},
            "origins": [[AVEON, "battlebgswamp2 (painted dead-tree mire, gradient-mapped jaundiced; water turned toxic)"],
                        [OWN, "slag platforms, barrels, burning drum (flame sheet), toxic glow, smog"]]}


#---------------------------------------------------------------------------------------------
def new_moon():
    F = "new_moon"
    bg = game_img("rejuvenation", "battlebgGDCCentralSquareNight")
    hd = room_from(bg)
    hd = grade(hd, mul=(0.62, 0.56, 0.86), contrast=1.05)
    a = arr(hd)
    win = (arr(room_from(bg))[..., 0] > 200) & (arr(room_from(bg))[..., 1] > 150) & (np.arange(693)[:, None] < 300)
    moon_c, moon_r = (600, 214), 56
    sky = blank(); d = ImageDraw.Draw(sky)
    d.ellipse([moon_c[0] - moon_r - 3, moon_c[1] - moon_r - 3, moon_c[0] + moon_r + 3, moon_c[1] + moon_r + 3],
              fill=C((150, 110, 230)))
    d.ellipse([moon_c[0] - moon_r, moon_c[1] - moon_r, moon_c[0] + moon_r, moon_c[1] + moon_r], fill=C((8, 6, 14)))
    src = arr(room_from(bg))
    skym = (src[..., 2] > src[..., 0]) & (src[..., :3].sum(-1) < 330) & (np.arange(693)[:, None] < 270)   # behind the towers
    sa = arr(sky); sa[..., 3] *= skym
    hd.alpha_composite(img(sa))
    for c, rx, ry, t in ((FOE, 116, 25, 8), (PLAYER, *pb(116, 25), 12)):
        platform(hd, c, rx, ry, (40, 34, 56), (22, 18, 32), outline=(150, 110, 230), thick=t)
    fields_c.save_room("field_new_moon", hd)
    layers = [layer(F, "corona", soft_glow(moon_c, moon_r * 2.2, (160, 110, 255), alpha=150), z=1, blend=1,
                    anim=S("pulse"), min=50, max=150, period=200),
              layer(F, "windows", glow_from_mask(win.astype(np.float32), (255, 190, 140), radius=3, gain=1.2,
                                                 core=0.5), z=1, blend=1, anim=S("flicker"), opacity=150, min=50,
                    chance=0.01, dropout=10)]
    extras = {"vacuum": "dark004",
              "img001": strip(F, "shadow", fog_strip(864, 160, (40, 20, 70), seed=143, scale=28, density=0.6,
                                                     alpha=120), 290, speed=0.5, direction=-1, z=4)}
    fx = [P(type=":twinkle", count=20, bitmap="star", area=[0, 66, 384, 110], speed=[1, 3], zoom=[0.6, 1.2],
            opacity=[140, 255], layers=[":back"]),
          P(type=":rise", count=8, shape=":glow", size=5, colors=[[150, 110, 220], [90, 70, 160]], speed=[0.2, 0.4],
            sway=10, zoom=[0.5, 0.9], opacity=[90, 160], layers=[":back", ":mid", ":front"], blend=1)]
    return {"profile": {S("art_extras"): extras, S("layers"): layers, S("fx"): fx},
            "origins": [[REJ, "battlebgGDCCentralSquareNight (painted night plaza and skyline, darkened violet)"],
                        [EBDX, "dark004 (vacuum rings)"],
                        [OWN, "dark moon with violet corona, flickering windows, shadow mist, violet-rim platforms"]]}


def inverse():
    F = "inverse"
    bg = game_img("rejuvenation", "battlebgDarchlight")
    # colours inverted (hue turned 180 degrees) but the light kept: a dark violet world lit by a teal path
    neg = gradient_map(hue_shift(bg, 180), [(0, (30, 16, 62)), (0.15, (70, 40, 124)), (0.32, (124, 82, 196)),
                                             (0.5, (80, 196, 214)), (0.7, (206, 250, 240)), (1, (255, 255, 255))])
    hd = room_from(neg)
    over = neg.transpose(Image.FLIP_TOP_BOTTOM).crop((0, 150, 512, 288))      # the same world, hanging overhead
    ext = Image.new("RGBA", (864, 138))
    for x in range(-170, 864, 512):
        ext.alpha_composite(over if ((x + 170) // 512) % 2 == 0 else over.transpose(Image.FLIP_LEFT_RIGHT), (max(x, 0), 0)) if x >= 0 else ext.alpha_composite(over.crop((170, 0, 512, 138)), (0, 0))
    nn = noise((864, 1), 6, 311, 3)[0]
    e = arr(ext)
    for x in range(864):
        cut = int(70 + nn[x] * 50)
        e[cut:, x, 3] = 0
        e[max(cut - 3, 0):cut, x, :3] = [30, 10, 50]
    hd.alpha_composite(img(e), (0, 150))
    for c, rx, ry, t in ((FOE, 116, 25, 8), (PLAYER, *pb(116, 25), 12)):
        platform(hd, c, rx, ry, (26, 20, 40), (60, 40, 90), outline=(255, 255, 255), thick=t, highlight=False)
    fields_c.save_room("field_inverse", hd)
    layers = []
    for i, (cx, cy, w) in enumerate(((250, 250, 110), (716, 240, 130))):
        isl = Image.new("RGBA", (w + 8, w), (0, 0, 0, 0)); d = ImageDraw.Draw(isl)
        rng = random.Random(i); top = w * 0.28
        pts = [(4, top)] + [(4 + w * k / 6, top + w * 0.6 * math.sin(k / 6 * math.pi) * rng.uniform(0.7, 1.1))
                            for k in range(1, 6)] + [(w + 4, top)]
        d.polygon(pts, fill=C((40, 26, 70)), outline=C((255, 255, 255)))
        d.rectangle([4, top - 7, w + 4, top], fill=C((230, 120, 240)), outline=C((255, 255, 255)))
        layers.append(layer(F, "rock%d" % i, onto(isl, cx - w / 2, cy - top), z=1, anim=S("bob"), amp=6,
                            period=200 + i * 50, phase=i * 2))
    extras = {"img001": strip(F, "static", fog_strip(864, 120, (255, 255, 255), seed=161, scale=10, density=0.4,
                                                     alpha=50), 270, speed=2, direction=-1, z=3)}
    return {"profile": {S("art_extras"): extras, S("layers"): layers},
            "origins": [[REJ, "battlebgDarchlight (painted forest path, hue-inverted onto a violet/teal ramp; a flipped "
                              "copy hangs overhead)"],
                        [OWN, "negative platforms, floating rocks, static mist"]]}


def prism_arena():
    F = "prism_arena"
    sh = art("some_battle_backgrounds_by_princess_phoenix_ddfcwq4.png")
    bg = sh.crop((512, 192, 768, 384)).resize((512, 384), Image.NEAREST)        # arena, night panel
    hd = extend_vanilla(bg, origin=(142, 150))
    hd = grade(hd, mul=(0.5, 0.44, 0.78), contrast=1.1)
    W, H = HD
    d = ImageDraw.Draw(hd)
    # festival night sky above the stands, starfield from Rejuvenation's New World
    stars = game_img("rejuvenation", "battlebgNewWorld").crop((0, 0, 512, 110))
    src = arr(hd)
    skyrow = 150 + 36
    for x in range(0, 864, 512):
        hd.alpha_composite(stars.crop((0, 0, 512, 36)), (x, 150))
    hd.alpha_composite(vgradient((864, 36), [(0, (20, 14, 60, 120)), (1, (90, 50, 140, 160))]), (0, 150))
    cx, cy = FOE[0], 446
    for i in range(18):       # prismatic sigil laid over the painted court
        a0 = i * 20
        d.arc([cx - 330, cy - 96, cx + 330, cy + 96], a0 + 1, a0 + 19, fill=C(fields_c.PLATE_COLS[i]), width=7)
    for rx, ry in ((340, 100), (318, 90)):
        d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], outline=C((250, 220, 120)), width=2)
    plates = []
    for i in range(18):
        a = i / 18 * 2 * math.pi + 0.1
        plates.append((math.sin(a), 520 + math.cos(a) * 320, 204 + math.sin(a) * 30, i))
    for _, x, y, i in sorted(plates):
        pw, ph = 22, 30
        d.line([x, y - ph / 2, x, 150], fill=C((180, 160, 110)))
        d.rectangle([x - pw / 2, y - ph / 2, x + pw / 2, y + ph / 2], fill=C(fields_c.PLATE_COLS[i]), outline=C((40, 30, 20)))
        d.rectangle([x - pw / 2 + 3, y - ph / 2 + 3, x + pw / 2 - 3, y + ph / 2 - 3],
                    outline=C(lighter(fields_c.PLATE_COLS[i], 0.5)))
    for c, rx, ry, t in ((FOE, 116, 25, 8), (PLAYER, *pb(116, 25), 14)):
        platform(hd, c, rx, ry, (244, 240, 252), (184, 180, 204), outline=(120, 100, 60), thick=t, rim=(255, 220, 120))
    fields_c.save_room("field_prism_arena", hd)
    pm = np.zeros((693, 864), np.float32)
    for _, x, y, i in plates:
        pm[int(y) - 15:int(y) + 15, int(x) - 11:int(x) + 11] = 1
    ring = np.zeros((693, 864), np.float32)
    rm = Image.new("L", HD, 0); rd = ImageDraw.Draw(rm)
    rd.ellipse([cx - 334, cy - 98, cx + 334, cy + 98], outline=255, width=12)
    ring = np.asarray(rm, np.float32) / 255
    crowd = fields_a.crowd_sheet(864, 44, seed=9, color=(30, 22, 50), rim=(220, 180, 255))
    name = "pf_prism_arena_crowd"; save_element(name, crowd)
    layers = [P(bitmap=name, hd=True, x=0.0, y=round(196 / 2.25, 2), ox=0, oy=0, z=1, frames=2, frame_time=12,
                opacity=200),
              layer(F, "plates", glow_from_mask(pm, (255, 255, 255), radius=10, gain=1.0), z=1, blend=1,
                    anim=S("pulse"), min=60, max=170, period=120),
              layer(F, "sigil", glow_from_mask(ring, (255, 236, 210), radius=8, gain=1.2, core=0.3), z=1, blend=1,
                    anim=S("pulse"), min=40, max=160, period=150, phase=1.0)]
    for i, x in enumerate((230, 520, 810)):
        col = [(255, 200, 220), (220, 220, 255), (200, 255, 230)][i]
        layers.append(layer(F, "beam%d" % i, cone(HD, (x, 150), 12, 560, col, alpha=70, angle=90 + (i - 1) * 16),
                            anchor=(x, 150), z=2, blend=1, anim=S("sway"), amp=12, period=220 + i * 60, phase=i * 2,
                            opacity=170))
    extras = {"lightsA": True,
              "img001": strip(F, "prism", fog_strip(864, 100, (255, 230, 255), seed=171, scale=20, density=0.45,
                                                    alpha=60), 250, speed=1, direction=1, z=3)}
    fx = [P(type=":twinkle", count=18, shape=":spark", size=7, colors=PRISM, speed=[2, 5], zoom=[0.5, 1.0],
            opacity=[170, 255], layers=[":back", ":mid"], blend=1),
          P(type=":fall", count=22, shape=":rect", w=3, h=2, colors=PRISM, speed=[0.5, 1.0], sway=12,
            zoom=[0.6, 1.0], opacity=[200, 255], spin=8, layers=[":back", ":mid", ":front"]),
          P(type=":flash", color=[255, 255, 255], alpha=50, interval=[90, 200], decay=10)]
    return {"profile": {S("art_extras"): extras, S("layers"): layers, S("fx"): fx},
            "origins": [[PPHX, "arena panel (night) at 2x: painted stadium court and stands"],
                        [REJ, "battlebgNewWorld (starfield strip above the stands)"], [EBDX, "lightsA"],
                        [OWN, "the 18 Plates ring, prismatic sigil, cheering crowd sheet, sweeping spotlights, "
                              "confetti, camera flashes, marble platforms"]]}


#---------------------------------------------------------------------------------------------
# FLOWER_GARDEN 1-2 from the bright stage-3 art, flowers closed back into buds
#---------------------------------------------------------------------------------------------
def flower_garden():
    res = fields_b.flower_garden()
    src = game_img("reborn", "battlebgFlowerGarden2")
    a = arr(src)
    mx, mn = a[..., :3].max(-1), a[..., :3].min(-1)
    greenish = (a[..., 1] >= a[..., 0]) & (a[..., 1] >= a[..., 2])
    brownish = (a[..., 0] > a[..., 1]) & (a[..., 1] > a[..., 2]) & (mx - mn < 110) & (mx < 190)
    flower = (mx - mn > 60) & ~greenish & ~brownish & (np.arange(288)[:, None] < 150)
    keep = noise((512, 288), 14, 5, 2) > 0.62
    for st in (1, 2):
        b = a.copy()
        kill = flower if st == 1 else (flower & ~keep)
        lum = (b[..., :3] * np.array([0.299, 0.587, 0.114])).sum(-1) / 255.0
        bud = np.stack([70 + lum * 80, 130 + lum * 90, 60 + lum * 60, np.full_like(lum, 255)], -1)
        b[kill] = bud[kill]
        hd = extend_vanilla(img(b), origin=O)
        eb = game_img("reborn", "enemybaseFlowerGarden%d" % (st + 1))
        place_foe_base(hd, eb); place_player_base_scaled(hd, eb)
        hd = blend(hd, vgradient(HD, [(0, (255, 240, 170, 90)), (0.5, (255, 240, 170, 20)), (1, (0, 0, 0, 0))]),
                   "softlight")
        flowers_scatter(hd, (0, 300, 864, 693), 120 * st, [(255, 190, 210), (255, 240, 170), (255, 255, 255)],
                        seed=st, size=(1.5, 3))
        fields_b.save_room("field_flower_garden" + ("" if st == 1 else "_2"), hd)
    res["origins"][0] = [REB, "battlebgFlowerGarden2-4, enemybaseFlowerGarden1-4; stages 1-2 are the stage-3 garden "
                              "with its blooms closed back into green buds"]
    return res


#---------------------------------------------------------------------------------------------
# Cinderglass geysers as sheet cells; Dragon's Den with smooth lava
#---------------------------------------------------------------------------------------------
def cinderglass():
    res = fields_d.ashen_rework()
    F = "ashen_waste"
    L = [l for l in res["profile"][S("layers")] if "geyser" not in l[S("bitmap")]]
    sheet = plume_sheet()
    for i, (vx, vy) in enumerate(((330, 304), (612, 300), (230, 470), (720, 520))):
        L.append(sheet_layer(F, "plume", sheet, vx, vy, 8, 9 + i, z=3 if vy < 400 else 23,
                             zoom=0.8 if vy < 400 else 1.3, phase=i * 23, opacity=220))
        L.append(layer(F, "vent%d" % i, soft_glow((vx, vy), 26, (255, 150, 60), alpha=230, squash=0.4), z=2, blend=1,
                       anim=S("pulse"), min=90, max=230, period=72 + i * 8))
    res["profile"][S("layers")] = L
    res["origins"][-1][1] = res["origins"][-1][1].replace("steam geysers with bursts", "geyser plumes (8-cell sheets) over glowing vents")
    return res


def _smooth_dd():
    """Patch Dragon's Den: round off the 4x-pixel lava before it is painted."""
    orig_mask = fields_a.mask_from

    def smooth(im, fn):
        m = orig_mask(im, fn)
        if m.shape == (693, 864) and m.mean() < 0.2:
            mi = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3.2))
            m = (np.asarray(mi, np.float32) > 120).astype(np.float32)
        return m
    return smooth


def dragons_den_smooth():
    orig = fields_a.mask_from
    fields_a.mask_from = _smooth_dd()
    try:
        return with_stages(fields_a.dragons_den, {2: fields_d.dragons_wyrmfire})()
    finally:
        fields_a.mask_from = orig


# stage builders capture these module attributes, so swap the bases in place
fields_a.desert = desert
fields_a.cave = cave
fields_c.new_moon = new_moon

BUILDERS = {
    "DESERT": with_stages(desert, {2: fields_d.desert_bloom}),
    "MOUNTAIN": mountain,
    "SNOWY_MOUNTAIN": snowy,
    "CAVE": with_stages(cave, {2: fields_e.cave_cracked}),
    "WASTELAND": wasteland,
    "NEW_MOON": with_stages(new_moon, {2: fields_d.new_moon_abyss, 3: fields_d.new_moon_lamplight}),
    "INVERSE": inverse,
    "PRISM_ARENA": prism_arena,
    "FLOWER_GARDEN": flower_garden,
    "ASHEN_WASTE": cinderglass,
    "DRAGONS_DEN": dragons_den_smooth,
}
