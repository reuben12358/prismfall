"""Round 2: painted Meadow (Magiscarf), glowing Embers, midgrounds + an animated element for the plain outdoor
fields, and stage-2 art for CAVE (cracked ceiling) and COLOSSEUM (frenzy)."""
import fields_a, fields_b, fields_c, fields_d
from bblib import *
from paint import *
from props import *
from rubygen import S
from fields_a import REJ, REB, DES, EBDX, OWN, O
from fields_d import capture, with_stages

MAGI = "Magiscarf, 'Fields Backgrounds' (DeviantArt ddejpun; non-commercial, credit)"
MAGI_PNG = "/home/claude/ref/art/morgebby/Graphics/Tilesets/Tilesets/ddejpun-94829cc1-fc31-4811-be2e-9431eaf7b76a.png"


def enhance(module, name, fn, src_note):
    """Wrap a base builder: compose as before, then paint a midground and add layers/fx on top."""
    orig = getattr(module, name)

    def run():
        hd, res = capture(orig, module)
        room, layers, fx = fn(hd)
        module.save_room(room[0], room[1])
        res["profile"].setdefault(S("layers"), [])
        res["profile"][S("layers")] = list(res["profile"][S("layers")]) + layers
        if fx:
            res["profile"][S("fx")] = list(res["profile"].get(S("fx"), [])) + fx
        res["origins"] = res["origins"] + [[OWN, src_note]]
        return res
    setattr(module, name, run)
    return run


def flame_layer(F, x, y, zoom=1.0, z=2, seed=1):
    name = "pf_%s_flame" % F
    save_element(name, flame_sheet(seed=seed))
    return P(bitmap=name, hd=True, x=round(x / 2.25, 2), y=round(y / 2.25, 2), ox=13, oy=44, z=z, frames=4,
             frame_time=5, zoom=zoom)


#---------------------------------------------------------------------------------------------
# MEADOW: Magiscarf's painted field at 2x
#---------------------------------------------------------------------------------------------
def windmill(h=70):
    im = Image.new("RGBA", (40, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.polygon([(12, h), (28, h), (24, 14), (16, 14)], fill=C((226, 214, 190)), outline=C((90, 76, 60)))
    d.polygon([(13, 16), (27, 16), (20, 4)], fill=C((170, 80, 60)), outline=C((80, 36, 28)))
    d.rectangle([18, h - 12, 22, h - 1], fill=C((90, 60, 40)))
    d.rectangle([18, 30, 21, 35], fill=C((90, 120, 150)))
    return im


def sails(r=30):
    im = Image.new("RGBA", (r * 2 + 4, r * 2 + 4), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = r + 2
    for k in range(4):
        a = k * math.pi / 2 + 0.3
        ex, ey = c + math.cos(a) * r, c + math.sin(a) * r
        px, py = -math.sin(a) * 5, math.cos(a) * 5
        d.line([(c, c), (ex, ey)], fill=C((70, 50, 36)), width=2)
        d.polygon([(c + (ex - c) * 0.3, c + (ey - c) * 0.3), (ex, ey), (ex + px, ey + py),
                   (c + (ex - c) * 0.3 + px, c + (ey - c) * 0.3 + py)], fill=C((240, 232, 214)), outline=C((90, 76, 60)))
    d.ellipse([c - 2, c - 2, c + 2, c + 2], fill=C((60, 40, 30)))
    return im


def meadow():
    F = "meadow"
    sheet = Image.open(MAGI_PNG).convert("RGBA")
    bg = sheet.crop((0, 160, 256, 304)).resize((512, 288), Image.NEAREST)        # day, with trees
    hd = extend_vanilla(bg, origin=(110, 150))
    hd = blend(hd, vgradient(HD, [(0, (255, 240, 180, 80)), (0.5, (255, 250, 200, 0)), (1, (20, 60, 20, 40))]),
               "softlight")
    # distant landmark on the far ridge + wildflowers through the grass
    wm = windmill(64)
    paste(hd, wm, 742, 262, "bottom")
    flowers_scatter(hd, (110, 300, 864, 693), 700, [(255, 255, 255), (255, 224, 80), (214, 150, 250), (255, 150, 180)],
                    seed=404, size=(1.5, 3.5))
    save_room("field_meadow", hd)
    night = sheet.crop((272, 160, 528, 304)).resize((512, 288), Image.NEAREST)
    hn = extend_vanilla(night, origin=(110, 150))
    paste(hn, grade(wm, mul=(0.5, 0.5, 0.8)), 742, 262, "bottom")
    save_room("field_meadow_night", hn)
    layers = [layer(F, "sails", onto(sails(26), 742 - 28, 262 - 58 - 28), anchor=(742, 262 - 58), z=1,
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
    extras = {"img001": strip(F, "clouds", fields_d.make_cloud_band(), 138, speed=0.5, direction=1, z=1, opacity=230),
              "img002": strip(F, "breeze", fog_strip(864, 90, (255, 255, 230), seed=405, scale=14, density=0.4,
                                                     alpha=50), 300, speed=2, direction=1, z=3)}
    fx = [P(type=":drift", count=18, shape=":dot", size=2, colors=[[255, 255, 220], [255, 240, 160]], dir=1,
            speed=[0.6, 1.4], sway=14, zoom=[0.5, 0.9], opacity=[170, 240], layers=[":back", ":mid", ":front"], blend=1),
          P(type=":drift", count=8, shape=":dot", size=3, colors=[[255, 200, 220], [255, 240, 140], [210, 170, 255]],
            dir=1, speed=[0.6, 1.2], sway=16, zoom=[0.6, 1.0], opacity=[200, 255], spin=6, layers=[":mid", ":front"]),
          P(type=":drift", count=3, shape=":spark", size=5, colors=[[255, 240, 120], [255, 255, 255]],
            speed=[0.3, 0.6], sway=20, zoom=[0.6, 0.9], opacity=[200, 255], layers=[":mid"])]
    return {"profile": {S("art_extras"): extras, S("layers"): layers, S("fx"): fx},
            "origins": [[MAGI, "day-with-trees panel at 2x (room), night panel (field_meadow_night)"],
                        [OWN, "windmill with turning sails, light shafts, wildflowers, swaying tall-grass clumps, "
                              "clouds, breeze, pollen"]]}


#---------------------------------------------------------------------------------------------
# WILDFIRE stage 2: Embers that glow
#---------------------------------------------------------------------------------------------
def wildfire():
    res = fields_d.wildfire()
    F = "wildfire_embers"
    hd = fields_a.vanilla("rejuvenation", "GoldForest")
    hd = gradient_map(hd, [(0, (12, 6, 8)), (0.28, (44, 24, 22)), (0.5, (86, 52, 40)), (0.75, (150, 100, 70)),
                           (1, (240, 190, 130))])
    hd = blend(hd, vgradient(HD, [(0, (60, 20, 40, 120)), (0.45, (255, 110, 40, 30)), (1, (255, 120, 40, 120))]),
               "softlight")
    a = arr(hd)
    lum = (a[..., :3] * np.array([0.299, 0.587, 0.114])).sum(-1)
    ed = np.asarray(Image.fromarray(np.clip(lum, 0, 255).astype(np.uint8)).filter(ImageFilter.FIND_EDGES), np.float32)
    rim = (ed > 46) & (np.arange(693)[:, None] < 330) & (noise(HD, 30, 601, 2) > 0.42)   # ember-lit trunk edges
    a[rim] = [255, 140, 50, 255]
    hd = img(a)
    d = ImageDraw.Draw(hd)
    rng = random.Random(7)
    beds = [(300, 372, 70, 13), (720, 360, 60, 11), (190, 520, 110, 22), (640, 560, 130, 24), (840, 470, 70, 14),
            (440, 640, 120, 22)]
    bedm = np.zeros((693, 864), np.float32)
    for (x, y, rx, ry) in beds:      # banked coal beds
        d.ellipse([x - rx, y - ry, x + rx, y + ry], fill=C((40, 16, 12)), outline=C((20, 8, 6)))
        for _ in range(int(rx * ry / 9)):
            aa = rng.random() * 2 * math.pi; rr = math.sqrt(rng.random()) * 0.85
            cx, cy = x + math.cos(aa) * rx * rr, y + math.sin(aa) * ry * rr
            col = rng.choice([(255, 110, 30), (255, 170, 50), (200, 50, 20), (255, 230, 130)])
            d.rectangle([cx - 1, cy - 1, cx + 1, cy], fill=C(col))
            if 0 <= int(cy) < 693 and 0 <= int(cx) < 864:
                bedm[int(cy), int(cx)] = 1
    for _ in range(46):              # the first green shoots
        x, y = rng.uniform(170, 850), rng.uniform(330, 688)
        h = 5 + (y - 300) / 40
        d.line([(x, y), (x, y - h)], fill=C((60, 150, 60)), width=2)
        d.ellipse([x - 4, y - h - 2, x, y - h + 2], fill=C((130, 220, 100)), outline=C((40, 110, 40)))
        d.ellipse([x + 1, y - h - 3, x + 5, y - h + 1], fill=C((150, 235, 110)), outline=C((40, 110, 40)))
    save_room("field_wildfire_embers", hd)
    layers = [layer(F, "beds", glow_from_mask(bedm, (255, 110, 30), radius=9, gain=2.6, core=0.6), z=1, blend=1,
                    anim=S("pulse"), min=90, max=230, period=90),
              layer(F, "rims", glow_from_mask(rim.astype(np.float32), (255, 120, 40), radius=4, gain=1.4, core=0.5),
                    z=1, blend=1, anim=S("pulse"), min=50, max=190, period=140, phase=2.0),
              layer(F, "warmth", soft_glow((470, 600), 460, (255, 100, 30), alpha=110, squash=0.45), z=1, blend=1,
                    anim=S("pulse"), min=40, max=110, period=160)]
    extras = {"img001": strip(F, "smoke", fog_strip(864, 180, (150, 130, 140), seed=212, scale=30, density=0.5,
                                                    alpha=70), 190, speed=0.5, direction=-1, z=3)}
    fx = [P(type=":rise", count=30, shape=":glow", size=4, colors=EMBER, speed=[0.5, 1.4], sway=12, zoom=[0.3, 0.7],
            opacity=[170, 255], layers=[":back", ":mid", ":front"], blend=1),
          P(type=":twinkle", count=12, shape=":spark", size=5, colors=[[255, 200, 100], [255, 240, 180]],
            area=[40, 140, 350, 308], speed=[4, 8], zoom=[0.4, 0.8], opacity=[170, 255], layers=[":back", ":mid"],
            blend=1),
          P(type=":fall", count=8, shape=":dot", size=3, colors=ASH, speed=[0.3, 0.7], sway=16, zoom=[0.4, 0.7],
            opacity=[110, 170], layers=[":back", ":mid"]),
          vent(300, 360, count=4, colors=[[170, 150, 160], [140, 124, 136]], rise=120, size=22, opacity=(40, 80))]
    res["profile"][S("stages")] = {2: {S("art_extras"): extras, S("layers"): layers, S("fx"): fx}}
    res["origins"][-1] = ["stage 2", "Embers: warm charcoal grade, ember-lit trunk edges, banked coal beds, rising "
                                     "sparks, first green shoots"]
    return res


#---------------------------------------------------------------------------------------------
# Midgrounds with character + one animated element
#---------------------------------------------------------------------------------------------
def desert_mid(hd):
    d = ImageDraw.Draw(hd)
    st, li, dk, ol = (214, 168, 104), (244, 216, 156), (150, 106, 62), (90, 58, 30)
    # sunken temple gate on the far dune
    for i, (x0, x1, y0) in enumerate(((236, 420, 300), (250, 406, 286), (264, 392, 272))):
        shade_rect(d, x0, y0, x1, y0 + 14, C(st), C(li), C(dk), C(ol))
    shade_rect(d, 270, 196, 386, 272, C(st), C(li), C(dk), C(ol))
    d.rectangle([308, 222, 348, 272], fill=C((60, 36, 24)), outline=C(ol))
    d.chord([308, 204, 348, 240], 180, 360, fill=C((60, 36, 24)), outline=C(ol))
    for x in (280, 296, 360, 376):
        d.line([x, 200, x, 270], fill=C(dk))
    shade_rect(d, 262, 184, 394, 198, C(li), C(li), C(st), C(ol))
    d.polygon([(262, 184), (328, 160), (394, 184)], fill=C(st), outline=C(ol))
    d.chord([220, 296, 440, 332], 180, 360, fill=C((232, 196, 128)))
    aw = Image.new("RGBA", (70, 44), (0, 0, 0, 0)); ad = ImageDraw.Draw(aw)
    ad.polygon([(0, 0), (70, 4), (64, 30), (40, 22), (20, 38), (4, 26)], fill=C((170, 60, 50)), outline=C((80, 24, 20)))
    ad.line([(0, 8), (66, 12)], fill=C((230, 190, 90)), width=2)
    layers = [layer("desert", "awning", onto(aw, 318, 206), anchor=(320, 208), z=1, anim=S("sway"), amp=5, period=70),
              layer("desert", "devil", cone(HD, (700, 330), 16, 150, (240, 214, 160), alpha=120, angle=-90), z=2,
                    anim=[S("drift"), S("pulse")], amp=50, min=30, max=120, period=260)]
    return ("field_desert", hd), layers, []


def wasteland_mid(hd):
    d = ImageDraw.Draw(hd)
    col = (60, 52, 50)
    hd.alpha_composite(girder(190, 16, col, vertical=True), (250, 130))
    hd.alpha_composite(girder(170, 12, col).rotate(14, expand=True, resample=Image.NEAREST), (230, 108))
    d.line([(392, 124), (392, 220)], fill=C((30, 26, 26)), width=2)
    hd.alpha_composite(hook((90, 70, 50)), (381, 218))
    for (x, y) in ((690, 330), (760, 322)):       # drums; one burning
        d.rectangle([x - 14, y - 34, x + 14, y], fill=C((110, 64, 40)), outline=C((30, 16, 10)))
        d.ellipse([x - 14, y - 40, x + 14, y - 28], fill=C((60, 34, 22)), outline=C((30, 16, 10)))
        d.line([x - 14, y - 16, x + 14, y - 16], fill=C((70, 40, 26)), width=2)
    layers = [flame_layer("wasteland", 690, 298, 1.2, 2, seed=5),
              layer("wasteland", "fireglow", soft_glow((690, 300), 110, (255, 150, 50), alpha=170), z=2, blend=1,
                    anim=[S("pulse"), S("flicker")], min=90, max=170, period=30, chance=0.02, dropout=2),
              layer("wasteland", "hookswing", onto(chain(60, color=(90, 70, 50)), 300, 150), anchor=(303, 150), z=1,
                    anim=S("sway"), amp=5, period=180)]
    return ("field_wasteland", hd), layers, []


def snowy_mid(hd):
    d = ImageDraw.Draw(hd)
    crag = mountains((864, 693), 330, 110, (70, 82, 110), seed=701, rough=1.0, peaks=5, snow=(240, 246, 255),
                     outline=(40, 48, 70))
    a = arr(crag)
    a[..., 3] *= ((np.arange(864) < 330) | (np.arange(864) > 700))[None, :]
    hd.alpha_composite(img(a))
    # summit shrine: a stone stupa with a lit lamp
    x, y = 296, 334
    for i, (w, h) in enumerate(((60, 12), (44, 14), (30, 16))):
        yy = y - sum(hh for _, hh in ((60, 12), (44, 14), (30, 16))[:i + 1])
        shade_rect(d, x - w // 2, yy, x + w // 2, yy + h, C((110, 116, 134)), C((170, 176, 196)), C((70, 74, 92)),
                   C((36, 38, 52)))
        d.line([x - w // 2 + 1, yy, x + w // 2 - 1, yy], fill=C((246, 250, 255)), width=3)
    d.polygon([(x - 10, y - 42), (x + 10, y - 42), (x, y - 66)], fill=C((190, 150, 60)), outline=C((80, 60, 20)))
    d.rectangle([x - 4, y - 24, x + 4, y - 14], fill=C((255, 210, 110)), outline=C((60, 40, 20)))
    layers = [layer("snowy_mountain", "lamp", soft_glow((x, y - 19), 46, (255, 200, 110), alpha=220), z=2, blend=1,
                    anim=[S("pulse"), S("flicker")], min=110, max=220, period=40, chance=0.02, dropout=3)]
    return ("field_snowy_mountain", grade(hd, contrast=1.1, mul=(0.94, 0.97, 1.04))), layers, []


def frozen_mid(hd):
    d = ImageDraw.Draw(hd)
    x, y = 286, 322      # ice-fishing hut on the lake
    d.rectangle([x - 26, y - 30, x + 26, y], fill=C((150, 70, 54)), outline=C((60, 24, 18)))
    for xx in range(x - 22, x + 26, 8):
        d.line([xx, y - 29, xx, y - 1], fill=C((120, 52, 40)))
    d.polygon([(x - 32, y - 30), (x + 32, y - 30), (x + 22, y - 48), (x - 22, y - 48)], fill=C((240, 246, 255)),
              outline=C((120, 150, 190)))
    d.rectangle([x - 6, y - 20, x + 6, y - 8], fill=C((255, 214, 120)), outline=C((60, 24, 18)))
    d.rectangle([x + 12, y - 58, x + 17, y - 46], fill=C((70, 60, 60)), outline=C((30, 24, 24)))
    d.ellipse([x - 40, y - 2, x + 40, y + 8], outline=C((230, 250, 255)))
    ice = [(170, 235, 255), (220, 250, 255), (120, 200, 240)]
    for foot, sc, seed in (((720, 326), 70, 11), ((180, 470), 110, 12), ((830, 560), 150, 13)):
        crystal_cluster(hd, foot, sc, ice, seed=seed, n=4, outline=(60, 120, 170))
    layers = [layer("frozen_lake", "window", soft_glow((x, y - 14), 40, (255, 200, 110), alpha=220), z=2, blend=1,
                    anim=S("pulse"), min=120, max=220, period=70)]
    fx = [vent(x + 14, y - 58, count=5, rise=70, size=14, opacity=(60, 120))]
    return ("field_frozen_lake", hd), layers, fx


def mountain_mid(hd):
    d = ImageDraw.Draw(hd)
    x, y = 300, 318      # ridge watchtower
    shade_rect(d, x - 16, y - 80, x + 16, y, C((128, 122, 116)), C((176, 170, 160)), C((84, 80, 78)), C((40, 38, 38)))
    for k in range(-2, 3):
        d.rectangle([x + k * 8 - 3, y - 88, x + k * 8 + 3, y - 80], fill=C((128, 122, 116)), outline=C((40, 38, 38)))
    d.rectangle([x - 4, y - 60, x + 4, y - 46], fill=C((40, 34, 34)))
    d.rectangle([x - 5, y - 16, x + 5, y], fill=C((70, 48, 34)), outline=C((40, 38, 38)))
    d.line([x, y - 88, x, y - 120], fill=C((60, 50, 44)), width=2)
    pen = Image.new("RGBA", (44, 18), (0, 0, 0, 0)); pd = ImageDraw.Draw(pen)
    pd.polygon([(0, 0), (44, 4), (34, 9), (44, 14), (0, 18)], fill=C((60, 130, 90)), outline=C((20, 60, 40)))
    hawk = Image.new("RGBA", (22, 10), (0, 0, 0, 0)); g = ImageDraw.Draw(hawk)
    g.line([(0, 2), (6, 0), (11, 5), (16, 0), (22, 2)], fill=(50, 40, 36, 255), width=2)
    layers = [layer("mountain", "pennant", onto(pen, x + 1, y - 122), anchor=(x + 1, y - 113), z=1, anim=S("sway"),
                    amp=9, period=44),
              layer("mountain", "hawk", onto(hawk, 560, 190), anchor=(571, 195), z=1, anim=[S("drift"), S("bob")],
                    amp=60, period=420)]
    return ("field_mountain", hd), layers, []


def water_mid(hd):
    boat = Image.new("RGBA", (110, 96), (0, 0, 0, 0)); d = ImageDraw.Draw(boat)
    d.polygon([(6, 70), (104, 70), (90, 90), (20, 90)], fill=C((120, 70, 46)), outline=C((46, 24, 14)))
    d.line([(8, 74), (102, 74)], fill=C((220, 210, 190)), width=2)
    d.rectangle([52, 6, 55, 70], fill=C((70, 46, 30)))
    d.polygon([(57, 8), (57, 62), (98, 62)], fill=C((240, 232, 214)), outline=C((120, 110, 96)))
    d.polygon([(50, 16), (50, 62), (18, 62)], fill=C((200, 80, 60)), outline=C((90, 30, 24)))
    d.rectangle([30, 58, 46, 70], fill=C((230, 226, 214)), outline=C((60, 50, 40)))
    layers = [layer("water_surface", "boat", onto(boat, 250, 226), anchor=(305, 316), z=2, anim=[S("bob"), S("sway")],
                    amp=2.5, period=120),
              layer("water_surface", "beam", cone(HD, (688, 163), 12, 420, (255, 244, 190), alpha=90, angle=180),
                    anchor=(688, 163), z=1, blend=1, anim=S("sway"), amp=26, period=320, opacity=170)]
    return ("field_water_surface", hd), layers, []


desert = enhance(fields_a, "desert", desert_mid, "sunken temple gate, torn awning (sways), dust devil")
wasteland = enhance(fields_a, "wasteland", wasteland_mid, "derelict crane, burning drum (flame sheet), swinging chain")
snowy = enhance(fields_a, "snowy_mountain", snowy_mid, "dark crags, summit stupa with a flickering lamp")
mountain = enhance(fields_a, "mountain", mountain_mid, "ridge watchtower with a streaming pennant, circling hawk")
water = enhance(fields_b, "water_surface", water_mid, "fishing boat bobbing at anchor, sweeping lighthouse beam")


_frozen_orig = fields_a.frozen_lake


def frozen_all():
    hd, res = capture(lambda: _frozen_orig(False), fields_a)
    room, layers, fx = frozen_mid(hd)
    fields_a.save_room(*room)
    res["profile"][S("layers")] = layers
    res["profile"][S("fx")] = list(res["profile"][S("fx")]) + fx
    res["origins"] = res["origins"] + [[OWN, "ice-fishing hut with lit window and chimney smoke, ice blocks"]]
    _frozen_orig(True)
    return res


#---------------------------------------------------------------------------------------------
# CAVE 2 (cracked ceiling) / COLOSSEUM 2 (frenzy): bridge-side stage art (profile :backdrop)
#---------------------------------------------------------------------------------------------
def cave_cracked():
    hd, res = capture(fields_a.cave, fields_a)
    F = "cave_cracked"
    d = ImageDraw.Draw(hd)
    rng = random.Random(3)
    for (x, y) in ((380, 150), (560, 156), (250, 160), (680, 150)):      # cracks running down from the ceiling
        pts = [(x, y)]
        for k in range(9):
            x += rng.uniform(-22, 22); y += rng.uniform(8, 20)
            pts.append((x, y))
            if rng.random() < 0.4:
                d.line([(x, y), (x + rng.uniform(-30, 30), y + rng.uniform(4, 16))], fill=C((14, 8, 8)), width=2)
        d.line(pts, fill=C((14, 8, 8)), width=3)
        d.line([(px + 2, py) for px, py in pts], fill=C((190, 160, 130)), width=1)
    for _ in range(26):                                                   # fallen rubble
        x, y = rng.uniform(170, 850), rng.uniform(330, 680)
        if abs(x - FOE[0]) < 130 and abs(y - FOE[1]) < 40:
            continue
        w = rng.uniform(5, 16)
        d.polygon([(x - w, y), (x - w * 0.4, y - w * 0.8), (x + w * 0.6, y - w * 0.6), (x + w, y)],
                  fill=C((110, 90, 76)), outline=C((30, 20, 16)))
    save_room("field_cave_cracked", hd)
    layers = list(res["profile"][S("layers")])
    layers.append(layer(F, "daylight", cone(HD, (470, 150), 12, 420, (255, 244, 210), alpha=110, angle=96), z=2,
                        blend=1, anim=S("pulse"), min=60, max=120, period=130))
    fx = list(res["profile"][S("fx")]) + [
        P(type=":fall", count=10, shape=":dot", size=3, colors=[[120, 100, 84], [80, 64, 54]], area=[60, 60, 330, 250],
          speed=[2.5, 4.0], sway=0, zoom=[0.5, 1.0], opacity=[220, 255], layers=[":back", ":mid", ":front"]),
        vent(470, 340, count=4, colors=DUST, rise=60, size=18, opacity=(40, 80))]
    return {"profile": {S("backdrop"): "field_cave_cracked", S("layers"): layers, S("fx"): fx},
            "note": "Cracked ceiling (bridge-side key field_cave_cracked): fissures, rubble, a shaft of daylight, "
                    "falling stones and dust"}


def colosseum_frenzy():
    hd, res = capture(fields_a.colosseum, fields_a)
    F = "colosseum_frenzy"
    hd = grade(hd, mul=(1.16, 0.96, 0.84), contrast=1.08)
    hd = blend(hd, vgradient(HD, [(0, (255, 90, 40, 90)), (0.5, (255, 140, 60, 20)), (1, (120, 20, 10, 60))]),
               "softlight")
    d = ImageDraw.Draw(hd)
    rng = random.Random(8)
    for _ in range(60):          # thrown streamers and tickets on the sand
        x, y = rng.uniform(160, 860), rng.uniform(330, 690)
        col = rng.choice([(230, 60, 50), (250, 210, 80), (240, 240, 240)])
        d.line([(x, y), (x + rng.uniform(-8, 8), y + rng.uniform(-3, 3))], fill=C(col), width=2)
    save_room("field_colosseum_frenzy", hd)
    layers = []
    for l in res["profile"][S("layers")]:
        l = dict(l)
        if "crowd" in l[S("bitmap")]:
            l[S("frame_time")] = 5
        if "lamp" in l[S("bitmap")] or "cone" in l[S("bitmap")]:
            l[S("amp")] = 7 if "lamp" in l[S("bitmap")] else l.get(S("amp"), 0)
            l[S("period")] = 70
        layers.append(l)
    layers.append(layer(F, "roar", soft_glow((500, 240), 460, (255, 110, 50), alpha=120, squash=0.4), z=1, blend=1,
                        anim=S("pulse"), min=30, max=120, period=36))
    fx = [P(type=":fall", count=30, shape=":rect", w=3, h=2, colors=[[230, 60, 50], [250, 210, 80], [240, 240, 240]],
            speed=[0.8, 1.6], sway=12, zoom=[0.6, 1.0], opacity=[200, 255], spin=10, layers=[":back", ":mid", ":front"]),
          P(type=":drift", count=14, shape=":dot", size=2, colors=DUST, speed=[0.4, 0.9], sway=6, zoom=[0.5, 0.9],
            opacity=[100, 170], layers=[":back", ":mid", ":front"]),
          P(type=":flash", color=[255, 230, 180], alpha=70, interval=[60, 140], decay=12, double=True)]
    return {"profile": {S("backdrop"): "field_colosseum_frenzy", S("layers"): layers, S("fx"): fx},
            "note": "Frenzy (bridge-side key field_colosseum_frenzy): hot red light, crowd bouncing fast, swinging "
                    "lamps, streamers, camera flashes"}


BUILDERS = {
    "MEADOW": meadow,
    "WILDFIRE": wildfire,
    "DESERT": with_stages(desert, {2: fields_d.desert_bloom}),
    "WASTELAND": wasteland,
    "SNOWY_MOUNTAIN": snowy,
    "MOUNTAIN": mountain,
    "FROZEN_LAKE": frozen_all,
    "WATER_SURFACE": water,
    "CAVE": with_stages(fields_a.cave, {2: cave_cracked}),
    "COLOSSEUM": with_stages(fields_a.colosseum, {2: colosseum_frenzy}),
}
