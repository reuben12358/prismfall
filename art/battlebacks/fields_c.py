"""Built / mystic fields: FACTORY, SCRAPYARD (same layout), GRAND_STAGE, NEON_GRID, HOLLOW_CATHEDRAL,
NEW_MOON, MINDSCAPE, INVERSE, PRISM_ARENA, BLEED (collage of the others, so build it last)."""
import os
from bblib import *
from paint import *
from props import *
from rubygen import S
from fields_a import vanilla, plat_pair, sky, REJ, REB, DES, EBDX, OWN, O


def steel_platform(canvas, center, rx, ry, plate=(120, 128, 140), side=(64, 68, 80), hazard=True, rust=0.0,
                   seed=0, thick=8):
    platform(canvas, center, rx, ry, plate, side, outline=(16, 18, 22), thick=thick, highlight=True)
    d = ImageDraw.Draw(canvas)
    cx, cy = center
    if hazard:
        for k in range(36):
            a0, a1 = k * 10, k * 10 + 10
            col = (230, 190, 40) if k % 2 == 0 else (30, 30, 34)
            d.arc([cx - rx + 2, cy - ry + 2, cx + rx - 2, cy + ry - 2], a0, a1, fill=C(col), width=3)
    for k in range(-2, 3):
        d.line([(cx + k * rx * 0.32, cy - ry * 0.75), (cx + k * rx * 0.32, cy + ry * 0.75)], fill=C(darker(plate, 0.75)))
    for k in range(16):
        a = k / 16 * 2 * math.pi
        x, y = cx + math.cos(a) * rx * 0.86, cy + math.sin(a) * ry * 0.78
        d.point((x, y), fill=C(lighter(plate, 0.5)))
        d.point((x + 1, y + 1), fill=C(darker(plate, 0.5)))
    if rust:
        rng = random.Random(seed)
        for _ in range(int(rx * ry * rust * 0.05)):
            a = rng.random() * 2 * math.pi; r = math.sqrt(rng.random())
            x, y = cx + math.cos(a) * rx * r, cy + math.sin(a) * ry * r
            d.point((x, y), fill=C(rng.choice([(130, 70, 36), (160, 90, 44), (96, 54, 30)])))


#---------------------------------------------------------------------------------------------
# FACTORY / SCRAPYARD
#---------------------------------------------------------------------------------------------
GEARS = [((236, 180), 92, 16, 1), ((356, 104), 52, 10, -1), ((708, 150), 110, 18, -1), ((826, 270), 60, 11, 1),
         ((560, 96), 40, 9, 1)]
CATWALK_Y = 236
BELT_Y = 292


def _foundry_base(wrecked):
    hd = vanilla("reborn", "Factory", base=False)
    if not wrecked:
        hd = gradient_map(hd, [(0, (10, 12, 22)), (0.3, (30, 36, 54)), (0.55, (58, 66, 88)), (0.8, (96, 104, 126)),
                               (1, (150, 158, 176))])
        hd = blend(hd, vgradient(HD, [(0, (255, 140, 40, 0)), (0.45, (255, 140, 40, 40)), (1, (255, 110, 30, 110))]),
                   "screen")
    else:
        hd = gradient_map(hd, [(0, (14, 10, 10)), (0.3, (44, 32, 28)), (0.55, (84, 60, 46)), (0.8, (124, 96, 74)),
                               (1, (170, 140, 110))])
    floor_top = 150 + 160
    fl = planks(HD, (70, 74, 86) if not wrecked else (82, 66, 54), (28, 30, 36) if not wrecked else (36, 26, 20),
                horizon_y=floor_top, vanish_x=520, n=10, seed=5)
    hd.alpha_composite(fl)
    return hd, floor_top


def _belt_strip(wrecked=False):
    w, h = 864, 34
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 6, w, 24], fill=C((40, 40, 46)), outline=C((14, 14, 16)))
    for x in range(0, w, 12):
        d.line([x, 7, x + 4, 23], fill=C((60, 60, 68)))
    rng = random.Random(2)
    x = 10
    while x < w - 50:
        if rng.random() < 0.55:
            bw = rng.randint(22, 40)
            if rng.random() < 0.5:   # glowing ingot
                d.rectangle([x, 0, x + bw, 7], fill=C((255, 160, 60)), outline=C((90, 40, 10)))
                d.line([x + 2, 1, x + bw - 2, 1], fill=C((255, 230, 150)))
            else:                     # crate
                d.rectangle([x, -6, x + bw, 7], fill=C((150, 110, 70)), outline=C((50, 34, 20)))
                d.line([x, -6, x + bw, 7], fill=C((110, 80, 50)))
        x += rng.randint(50, 90)
    for x in range(0, w, 48):
        d.ellipse([x, 22, x + 10, 32], fill=C((90, 92, 100)), outline=C((14, 14, 16)))
    return im


def _crucible(tipped=False, hot=True):
    im = Image.new("RGBA", (90, 80), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    body = [(12, 18), (78, 18), (68, 70), (22, 70)]
    d.polygon(body, fill=C((70, 70, 80)), outline=C((16, 16, 20)))
    d.line([(16, 24), (26, 66)], fill=C((110, 110, 122)), width=2)
    d.rectangle([6, 12, 84, 20], fill=C((90, 90, 100)), outline=C((16, 16, 20)))
    if hot:
        d.rectangle([10, 13, 80, 17], fill=C((255, 170, 60)))
    d.ellipse([0, 36, 10, 46], fill=C((60, 60, 70)), outline=C((16, 16, 20)))
    d.ellipse([80, 36, 90, 46], fill=C((60, 60, 70)), outline=C((16, 16, 20)))
    return im.rotate(-28 if not tipped else 100, expand=True, resample=Image.NEAREST)


def factory_scene(wrecked):
    F = "scrapyard" if wrecked else "factory"
    hd, floor_top = _foundry_base(wrecked)
    d = ImageDraw.Draw(hd)
    layers = []
    steel = (78, 86, 104) if not wrecked else (92, 70, 54)
    gear_col = (110, 118, 138) if not wrecked else (120, 84, 58)
    # gears (factory: rotating layers; scrapyard: dead, broken, painted into the wall)
    for i, (c, r, teeth, sgn) in enumerate(GEARS):
        g = gear(r, teeth, base=gear_col, outline=(14, 14, 18) if not wrecked else (24, 14, 10),
                 broken=wrecked and i % 2 == 0, seed=i)
        if wrecked:
            gr = g.rotate(i * 17, resample=Image.NEAREST)
            hd.alpha_composite(gr, (int(c[0] - g.width / 2), int(c[1] - g.height / 2)))
        else:
            layers.append(layer(F, "gear%d" % i, onto(g, c[0] - g.width / 2, c[1] - g.height / 2), anchor=c, z=1,
                                anim=S("rotate"), speed=sgn * 18.0 / r))
    # catwalk across the back
    cw = blank()
    cd = ImageDraw.Draw(cw)
    gl = girder(864, 16, steel)
    if not wrecked:
        cw.alpha_composite(gl, (0, CATWALK_Y))
        for x in range(0, 864, 30):
            cd.line([x, CATWALK_Y - 30, x, CATWALK_Y], fill=C((30, 32, 40)), width=3)
            cd.line([x, CATWALK_Y - 30, x, CATWALK_Y], fill=C(steel), width=1)
        cd.rectangle([0, CATWALK_Y - 32, 864, CATWALK_Y - 28], fill=C(steel), outline=C((14, 14, 18)))
        for x in (120, 470, 800):
            cw.alpha_composite(girder(floor_top - CATWALK_Y, 14, steel, vertical=True), (x, CATWALK_Y + 14))
    else:
        # collapsed: the walkway snapped in the middle, one half hanging to the floor
        cw.alpha_composite(gl.crop((0, 0, 330, 16)), (0, CATWALK_Y))
        broken = gl.crop((0, 0, 300, 16)).rotate(-24, expand=True, resample=Image.NEAREST)
        cw.alpha_composite(broken, (320, CATWALK_Y - 4))
        cw.alpha_composite(gl.crop((0, 0, 260, 16)), (620, CATWALK_Y))
        for x in range(0, 330, 30):
            cd.line([x, CATWALK_Y - 30, x, CATWALK_Y], fill=C(steel), width=2)
        cd.rectangle([0, CATWALK_Y - 32, 330, CATWALK_Y - 28], fill=C(steel), outline=C((24, 14, 10)))
        cw.alpha_composite(girder(floor_top - CATWALK_Y, 14, steel, vertical=True), (120, CATWALK_Y + 14))
        cw.alpha_composite(girder(floor_top - CATWALK_Y - 30, 14, steel, vertical=True).rotate(8, expand=True),
                           (800, CATWALK_Y + 40))
    hd.alpha_composite(cw)
    # conveyor
    if not wrecked:
        d.rectangle([0, BELT_Y + 24, 864, BELT_Y + 40], fill=C((30, 30, 36)), outline=C((10, 10, 12)))
        # molten channel along the back of the floor
        d.rectangle([0, floor_top - 2, 864, floor_top + 6], fill=C((255, 140, 40)), outline=C((60, 20, 6)))
        d.line([0, floor_top, 864, floor_top], fill=C((255, 230, 140)))
    else:
        belt = _belt_strip(True)
        hd.alpha_composite(belt.crop((0, 0, 340, 34)), (0, BELT_Y))
        hd.alpha_composite(belt.crop((600, 0, 864, 34)), (690, BELT_Y))
    # crucible + mould
    if not wrecked:
        d.rectangle([600, floor_top - 26, 690, floor_top + 4], fill=C((50, 52, 60)), outline=C((14, 14, 18)))
        d.rectangle([606, floor_top - 22, 684, floor_top - 14], fill=C((255, 150, 50)))
    else:
        cr = _crucible(tipped=True, hot=False)
        hd.alpha_composite(cr, (690, floor_top - 50))
        d.rectangle([700, floor_top - 20, 790, floor_top + 10], fill=C((50, 40, 34)), outline=C((24, 14, 10)))
        # scrap heaps
        rng = random.Random(4)
        for (hx, hy, hw) in ((300, floor_top + 30, 150), (780, floor_top + 70, 170), (90, 610, 220),
                             (840, 640, 200)):
            for _ in range(int(hw / 4)):
                sx = hx + rng.uniform(-hw / 2, hw / 2); sy = hy - rng.uniform(0, hw * 0.35) * (1 - abs(sx - hx) / (hw / 2))
                sw, sh = rng.randint(8, 24), rng.randint(4, 12)
                col = rng.choice([(110, 70, 44), (80, 60, 50), (130, 100, 70), (60, 50, 46), (150, 90, 50)])
                d.rectangle([sx, sy, sx + sw, sy + sh], fill=C(col), outline=C((24, 16, 12)))
        g = gear(60, 12, base=gear_col, outline=(24, 14, 10), broken=True, seed=9)
        g = g.resize((g.width, g.height // 3), Image.NEAREST)
        hd.alpha_composite(g, (430 - g.width // 2, floor_top + 40))
    steel_platform(hd, FOE, 116, 25, rust=0.0 if not wrecked else 0.8, hazard=not wrecked,
                   plate=(120, 128, 140) if not wrecked else (110, 90, 72), side=(64, 68, 80) if not wrecked else (60, 46, 36))
    steel_platform(hd, PLAYER, 232, 50, rust=0.0 if not wrecked else 0.8, hazard=not wrecked, thick=14,
                   plate=(120, 128, 140) if not wrecked else (110, 90, 72), side=(64, 68, 80) if not wrecked else (60, 46, 36))
    if wrecked:
        hd = grade(hd, mul=(0.92, 0.84, 0.8), sat=0.85)
    save_room("field_" + F, hd)
    # --- animated layers
    extras = {}
    fx = []
    if not wrecked:
        extras["img001"] = strip(F, "belt", _belt_strip(), BELT_Y, speed=2, direction=-1, z=2)
        cru = _crucible()
        cx0, cy0 = 590, 150
        layers.append(layer(F, "crucible", onto(cru, cx0, cy0), anchor=(cx0 + cru.width / 2, cy0), z=2,
                            anim=S("sway"), amp=0.6, period=200))
        ch = chain(cy0 + 6)
        layers.append(layer(F, "cruchain", onto(ch, cx0 + cru.width / 2 - 3, 0), z=2))
        pour = Image.new("RGBA", (16, 96), (0, 0, 0, 0)); pd = ImageDraw.Draw(pour)
        rng = random.Random(5)
        for y in range(0, 96, 2):
            w0 = 4 + rng.choice([0, 1, 1, 2])
            pd.line([(8 - w0, y), (8 + w0, y)], fill=C((255, 170, 60)))
            pd.line([(8 - 1, y), (8 + 1, y)], fill=C((255, 240, 170)))
        px = cx0 + 12
        extras["img010"] = {S("bitmap"): "pf_factory_pour2", S("scrolling"): True, S("vertical"): True, S("speed"): 3,
                            S("direction"): -1, S("ox"): 8, S("oy"): 0, S("x"): round(px / 2.25, 2),
                            S("y"): round((cy0 + 50) / 2.25, 2), S("zoom"): INV, S("z"): 2}
        pour_len = (floor_top - 22) - (cy0 + 50)
        save_element("pf_factory_pour2", pour.crop((0, 0, 16, pour_len)))
        extras["img010"][S("bitmap")] = "pf_factory_pour2"
        layers.append(layer(F, "pourglow", soft_glow((px, floor_top - 20), 120, (255, 140, 40), alpha=200, squash=0.5),
                            z=2, blend=1, anim=S("pulse"), min=110, max=220, period=30))
        layers.append(layer(F, "furnace", soft_glow((480, 693), 520, (255, 120, 30), alpha=120, squash=0.4), z=1,
                            blend=1, anim=S("pulse"), min=60, max=130, period=140))
        ch_m = np.zeros((693, 864), np.float32); ch_m[floor_top - 2:floor_top + 6, :] = 1
        layers.append(layer(F, "channel", glow_from_mask(ch_m, (255, 140, 40), radius=10, gain=1.4), z=1, blend=1,
                            anim=S("pulse"), min=90, max=190, period=80))
        for i, x in enumerate((190, 320, 720)):
            im = blank(); c2 = chain(30 + i * 14); hk = hook()
            paste(im, c2, x - c2.width / 2, CATWALK_Y + 16); paste(im, hk, x - hk.width / 2, CATWALK_Y + 14 + c2.height)
            layers.append(layer(F, "hook%d" % i, im, anchor=(x, CATWALK_Y + 16), z=3, anim=S("sway"), amp=3,
                                period=150 + i * 30))
        fx = [P(type=":fall", count=14, shape=":dot", size=2, colors=[[255, 150, 50], [255, 210, 90], [255, 240, 170]],
                area=[262, 90, 290, 140], speed=[2.0, 3.5], sway=10, zoom=[0.5, 0.8], opacity=[200, 255],
                layers=[":back", ":mid"], blend=1),
              P(type=":rise", count=10, shape=":glow", size=4, colors=[[255, 150, 50], [255, 200, 80]],
                area=[0, 140, 384, 308], speed=[0.5, 1.2], sway=8, zoom=[0.3, 0.6], opacity=[150, 230],
                layers=[":back", ":mid", ":front"], blend=1),
              vent(150, floor_top + 10, count=6, rise=100, size=20),
              vent(820, floor_top + 30, count=6, rise=100, size=20)]
        extras["img002"] = strip(F, "heat", fog_strip(864, 120, (255, 160, 80), seed=111, scale=24, density=0.5,
                                                      alpha=60), 250, speed=0.5, direction=1, z=4)
    else:
        piece = _belt_strip().crop((340, 0, 410, 34)).rotate(-82, expand=True, resample=Image.NEAREST)
        layers.append(layer(F, "dangle", onto(piece, 326, BELT_Y + 4), anchor=(340, BELT_Y + 6), z=2,
                            anim=S("sway"), amp=4, period=210))
        im = blank(); hk = hook((110, 80, 60)); c2 = chain(150, color=(110, 84, 62))
        paste(im, c2, 250 - c2.width / 2, 120); paste(im, hk, 250 - hk.width / 2, 120 + c2.height - 2)
        layers.append(layer(F, "chain", im, anchor=(250, 120), z=2, anim=S("sway"), amp=2, period=260))
        lm = lamp((255, 60, 40), body=(70, 50, 40))
        layers.append(layer(F, "alarm", onto(lm, 410, CATWALK_Y + 18), z=3))
        layers.append(layer(F, "alarmglow", soft_glow((422, CATWALK_Y + 36), 260, (255, 40, 30), alpha=120,
                                                     squash=0.8), z=3, blend=1, anim=[S("pulse"), S("flicker")],
                            min=10, max=130, period=50, chance=0.03, dropout=8))
        spark = blank(); sd = ImageDraw.Draw(spark)
        for k in range(10):
            a = k / 10 * 2 * math.pi
            sd.line([(340, 300), (340 + math.cos(a) * 14, 300 + math.sin(a) * 10)], fill=(255, 240, 160, 255))
        layers.append(layer(F, "spark", spark, z=3, blend=1, anim=S("flicker"), opacity=0, min=255, chance=0.05,
                            dropout=3))
        fx = [vent(300, floor_top + 20, count=7, colors=SMOKE, rise=140, size=24, opacity=(60, 120)),
              vent(700, floor_top - 10, count=7, colors=SMOKE, rise=140, size=24, opacity=(60, 120)),
              vent(90, 560, count=5, colors=SMOKE, rise=120, size=26, opacity=(50, 100), layers=(":front",)),
              P(type=":fall", count=5, shape=":dot", size=2, colors=EMBER, area=[146, 130, 156, 150],
                speed=[2.0, 3.5], sway=3, zoom=[0.5, 0.8], opacity=[200, 255], layers=[":back"], blend=1),
              P(type=":drift", count=10, shape=":dot", size=2, colors=ASH, speed=[0.2, 0.5], sway=6,
                zoom=[0.5, 0.8], opacity=[80, 140], layers=[":back", ":mid"])]
        extras["img002"] = strip(F, "smoke", fog_strip(864, 200, (90, 80, 76), seed=112, scale=30, density=0.6,
                                                       alpha=110), 180, speed=0.5, direction=-1, z=4)
    prof = {S("art_extras"): extras, S("layers"): layers, S("fx"): fx}
    src = [[REB, "battlebgFactory (gradient-mapped %s, extended)" % ("steel-blue with forge light" if not wrecked
                                                                      else "rust")]]
    if not wrecked:
        src.append([OWN, "rotating gears, catwalk and girders, conveyor with ingots (scrolling), crucible pouring "
                         "molten steel, hooks, hazard-striped steel platforms, furnace glow, heat haze"])
    else:
        src.append([OWN, "same layout wrecked: dead broken gears, collapsed catwalk, snapped conveyor, tipped "
                         "crucible, scrap heaps, rusted platforms, red alarm lamp, severed-cable sparks, smoke"])
    return {"profile": prof, "origins": src}


def factory():
    return factory_scene(False)


def scrapyard():
    return factory_scene(True)


#---------------------------------------------------------------------------------------------
# GRAND_STAGE
#---------------------------------------------------------------------------------------------
def opera_box(w, h, seed=0):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    gold, red, out = (214, 170, 70), (120, 18, 30), (50, 30, 10)
    d.rectangle([0, 0, w - 1, h - 1], fill=C((40, 8, 14)), outline=C(out))
    d.rectangle([4, 4, w - 5, h * 0.62], fill=C(red))
    d.chord([4, -h * 0.3, w - 5, h * 0.5], 0, 180, fill=C((150, 30, 40)), outline=C(gold))
    rng = random.Random(seed)
    for k in range(rng.randint(1, 3)):
        x = rng.uniform(10, w - 18)
        d.ellipse([x, h * 0.32, x + 8, h * 0.32 + 8], fill=C((24, 14, 16)))
        d.rectangle([x - 2, h * 0.32 + 7, x + 10, h * 0.62], fill=C((24, 14, 16)))
    d.rectangle([0, h * 0.62, w - 1, h - 1], fill=C(gold), outline=C(out))
    for x in range(4, w - 4, 6):
        d.line([x, h * 0.66, x, h - 4], fill=C((160, 120, 40)))
    d.line([2, h * 0.64, w - 3, h * 0.64], fill=C((255, 230, 140)))
    return im


def grand_stage():
    F = "grand_stage"
    hd = Image.new("RGBA", HD, (34, 8, 14, 255))
    hd = blend(hd, vgradient(HD, [(0, (70, 14, 24, 255)), (0.4, (40, 8, 14, 255)), (1, (20, 6, 10, 255))]))
    stage_y = 318
    # painted backdrop flat: the Saltmere seascape (Rejuvenation's beach art) on canvas, upstage
    flat = game_img("rejuvenation", "battlebgBeach").resize((420, 236), Image.LANCZOS).crop((0, 0, 420, 150))
    flat = grade(flat, sat=0.85, contrast=0.92, mul=(1.02, 0.98, 0.9))
    fx0, fy0 = 316, stage_y - 150
    hd.alpha_composite(flat, (fx0, fy0))
    d = ImageDraw.Draw(hd)
    d.rectangle([fx0 - 5, fy0 - 5, fx0 + 424, stage_y], outline=C((190, 150, 60)), width=4)
    # wing flats either side of the backdrop
    for x0 in (210, 742):
        d.rectangle([x0 - 50, 150, x0 + 50, stage_y], fill=C((60, 20, 30)), outline=C((24, 6, 10)))
        for k in range(4):
            d.line([x0 - 50 + k * 30, 150, x0 - 50 + k * 30, stage_y], fill=C((80, 30, 40)))
    fl = planks(HD, (140, 92, 54), (70, 42, 24), horizon_y=stage_y, vanish_x=500, n=26, seed=2)
    hd.alpha_composite(fl)
    d.rectangle([0, stage_y - 2, 864, stage_y + 3], fill=C((60, 34, 20)))
    # gilt boxes on the far sides (seen as the camera pulls back) + a gallery rail above the stage
    for (x, y) in ((10, 160), (10, 250), (760, 160), (760, 250)):
        hd.alpha_composite(opera_box(100, 70, seed=x + y), (x, y))
    # velvet curtains + valance framing the proscenium
    cl = curtain(110, 560, gather=0.6, seed=1)
    hd.alpha_composite(cl, (120, 150))
    hd.alpha_composite(cl.transpose(Image.FLIP_LEFT_RIGHT), (640, 150))
    hd.alpha_composite(valance(864, 54, swags=7), (0, 140))
    # footlights row at the stage lip (downstage, nearest the camera)
    for x in range(40, 864, 54):
        d.chord([x - 10, 640, x + 10, 656], 180, 360, fill=C((255, 230, 150)), outline=C((80, 50, 20)))
    platform(hd, FOE, 116, 25, (170, 40, 50), (100, 20, 30), outline=(40, 8, 12), rim=(255, 210, 110))
    platform(hd, PLAYER, 232, 50, (170, 40, 50), (100, 20, 30), outline=(40, 8, 12), thick=12, rim=(255, 210, 110))
    save_room("field_grand_stage", hd)
    lamps = np.zeros((693, 864), np.float32)
    for x in range(40, 864, 54):
        lamps[644:650, x - 6:x + 6] = 1
    layers = [layer(F, "spot", cone(HD, (526, 150), 30, 230, (255, 245, 210), alpha=120), z=2, blend=1,
                    anim=S("pulse"), min=80, max=130, period=160),
              layer(F, "pool", soft_glow(FOE, 150, (255, 240, 200), alpha=120, squash=0.3), z=1, blend=1,
                    anim=S("pulse"), min=70, max=120, period=160),
              layer(F, "footlights", glow_from_mask(lamps, (255, 220, 140), radius=8, gain=2.0), z=24, blend=1,
                    anim=S("pulse"), min=120, max=200, period=90),
              layer(F, "flatglow", soft_glow((526, 240), 260, (255, 200, 150), alpha=70, squash=0.5), z=1, blend=1,
                    anim=S("pulse"), min=30, max=70, period=220)]
    extras = {"lightsA": True, "spinLights": True}
    return {"profile": {S("art_extras"): extras, S("layers"): layers},
            "origins": [[REJ, "battlebgBeach (scaled, as the painted seascape backdrop flat)"],
                        [EBDX, "lightsA, spinLights"],
                        [OWN, "opera house: velvet curtains and valance, wing flats, gilt boxes, stage boards, "
                              "footlights, spotlight, velvet platforms"]]}


#---------------------------------------------------------------------------------------------
# NEON_GRID
#---------------------------------------------------------------------------------------------
def billboard(w, h, seed=0, base=(255, 60, 200)):
    rng = random.Random(seed)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w - 1, h - 1], fill=C(darker(base, 0.25), 220), outline=C(base))
    d.rectangle([2, 2, w - 3, h - 3], outline=C(lighter(base, 0.4)))
    for k in range(3):
        y = 6 + k * (h - 10) / 3
        d.rectangle([6, y, 6 + rng.uniform(0.3, 0.85) * (w - 12), y + 3], fill=C(lighter(base, 0.5)))
    d.ellipse([w - 18, h / 2 - 6, w - 6, h / 2 + 6], outline=C((255, 255, 255)))
    return im


def neon_grid():
    F = "neon_grid"
    bg = game_img("rejuvenation", "battlebgZeight")
    # night sky instead of the sunset
    a = arr(bg)
    skym = (a[..., 0] > 180) & (a[..., 1] > 120) & (a[..., 2] < 120)
    a[skym] = [18, 20, 48, 255]
    bg = img(a)
    hd = extend_vanilla(bg, origin=O, side_mode="edge")
    ha = arr(hd)
    skym = ((np.abs(ha[..., 0] - 18) < 6) & (np.abs(ha[..., 1] - 20) < 6) & (np.abs(ha[..., 2] - 48) < 6))
    hd = blend(hd, vgradient(HD, [(0, (8, 6, 30, 255)), (0.25, (30, 16, 72, 255)), (0.42, (90, 30, 120, 255)),
                                  (1, (90, 30, 120, 255))]), "normal", mask=skym.astype(np.float32))
    # perspective circuit grid on the rooftop floor
    roof = 150 + 132
    grid = blank()
    gd = ImageDraw.Draw(grid)
    vx = 500
    for k in range(-24, 25):
        gd.line([(vx + k * 12, roof), (vx + k * 120, 693 + 200)], fill=(60, 230, 255, 150))
    y = roof + 6; step = 6
    while y < 693:
        gd.line([(0, y), (864, y)], fill=(60, 230, 255, 120))
        step *= 1.35; y += step
    hd.alpha_composite(grid)
    skyl, wins = skyline((864, 693), roof - 2, (20, 18, 44), seed=4, min_h=40, max_h=150,
                         windows=[(80, 240, 255), (255, 80, 220), (255, 240, 120)], win_p=0.18)
    sk = arr(skyl)
    sk[..., 3] *= (arr(hd)[..., 2] < 60) & (arr(hd)[..., 0] < 40)
    hd.alpha_composite(img(sk))
    for (c, rx, ry, thick) in ((FOE, 118, 26, 8), (PLAYER, 236, 52, 14)):
        platform(hd, c, rx, ry, (24, 30, 50), (14, 16, 30), outline=(80, 240, 255), thick=thick)
        d = ImageDraw.Draw(hd)
        d.ellipse([c[0] - rx * 0.8, c[1] - ry * 0.8, c[0] + rx * 0.8, c[1] + ry * 0.8], outline=C((80, 240, 255)))
        d.ellipse([c[0] - rx * 0.35, c[1] - ry * 0.35, c[0] + rx * 0.35, c[1] + ry * 0.35], outline=C((255, 80, 220)))
        d.line([(c[0] - rx * 0.8, c[1]), (c[0] + rx * 0.8, c[1])], fill=C((80, 240, 255)))
    save_room("field_neon_grid", hd)
    cyan = mask_from(hd, lambda r, g, b: (g > 180) & (b > 200) & (r < 140))
    layers = [layer(F, "circuits", glow_from_mask(cyan, (80, 240, 255), radius=5, gain=1.2, core=0.5), z=1, blend=1,
                    anim=[S("pulse"), S("flicker")], min=60, max=180, period=70, chance=0.008, dropout=4)]
    for i, (x, y, w, h, col) in enumerate(((210, 90, 90, 50, (255, 60, 200)), (640, 60, 110, 56, (80, 220, 255)),
                                           (520, 180, 70, 36, (255, 220, 80)))):
        bb = billboard(w, h, seed=i, base=col)
        layers.append(layer(F, "board%d" % i, onto(bb, x, y), z=1, anim=[S("bob"), S("flicker")], amp=2,
                            period=120 + i * 30, chance=0.01, dropout=5, min=60))
    ship = Image.new("RGBA", (120, 40), (0, 0, 0, 0)); sd = ImageDraw.Draw(ship)
    sd.ellipse([0, 4, 110, 28], fill=C((30, 30, 50)), outline=C((80, 80, 120)))
    sd.rectangle([40, 26, 72, 36], fill=C((24, 24, 40)), outline=C((80, 80, 120)))
    for x in range(46, 70, 6):
        sd.point((x, 31), fill=C((255, 240, 160)))
    sd.point((106, 16), fill=C((255, 60, 60)))
    layers.append(layer(F, "airship", onto(ship, 330, 20), z=1, anim=[S("drift"), S("bob")], amp=40, period=600))
    extras = {"spinLights": True,
              "img001": strip(F, "scan", fog_strip(864, 50, (80, 240, 255), seed=121, scale=8, density=0.4,
                                                   alpha=60), roof - 20, speed=4, direction=1, z=2)}
    return {"profile": {S("art_extras"): extras, S("layers"): layers},
            "origins": [[REJ, "battlebgZeight (sky repainted to night, extended)"],
                        [EBDX, "spinLights"],
                        [OWN, "Lumen skyline, perspective circuit grid, neon ring platforms, holo-billboards, airship, "
                              "circuit glow"]]}


#---------------------------------------------------------------------------------------------
# HOLLOW_CATHEDRAL
#---------------------------------------------------------------------------------------------
def candle(h=14):
    im = Image.new("RGBA", (6, h + 6), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([1, 6, 4, h + 5], fill=C((230, 220, 200)), outline=C((60, 50, 40)))
    d.ellipse([1, 0, 4, 6], fill=C((255, 220, 120)))
    return im


def hollow_cathedral():
    F = "hollow_cathedral"
    bg = game_img("rejuvenation", "battlebgBlacksteepleIndoor")
    hd = extend_vanilla(bg, origin=O)
    hd = gradient_map(hd, [(0, (8, 6, 16)), (0.25, (26, 20, 44)), (0.5, (56, 46, 82)), (0.75, (100, 90, 130)),
                           (1, (170, 160, 200))])
    d = ImageDraw.Draw(hd)
    # nave arches + pillars at the back
    for x in (230, 390, 662, 822):
        hd.alpha_composite(gothic_arch(130, 200, (30, 24, 46), inner=(12, 10, 22)), (x - 65, 110))
    for x in (150, 310, 450, 602, 742):
        pillar(hd, x, 100, 304, 22, (54, 46, 76), (90, 80, 120), (28, 22, 42), (10, 8, 18))
    rw = rose_window(70, [(90, 26, 50), (34, 40, 96), (100, 80, 36), (30, 70, 56), (70, 32, 90)])
    rw = grade(rw, sat=0.75, mul=(0.85, 0.85, 0.95))
    a = arr(rw)
    rng = random.Random(3)
    for _ in range(9):   # broken panes
        x, y = rng.randint(20, rw.width - 20), rng.randint(20, rw.height - 20)
        a[y - 6:y + 6, x - 5:x + 5] = [10, 8, 18, 255]
    rw = img(a)
    hd.alpha_composite(rw, (526 - rw.width // 2, 156))
    # altar behind the foe
    d.rectangle([450, 286, 600, 322], fill=C((60, 50, 70)), outline=C((14, 10, 20)))
    d.rectangle([440, 280, 610, 288], fill=C((90, 80, 110)), outline=C((14, 10, 20)))
    for x in range(456, 600, 18):
        hd.alpha_composite(candle(12 + (x % 3) * 4), (x, 262 - (x % 3) * 4))
    # broken pews along the aisle (left, in front of the altar steps)
    for row, y in enumerate((380, 450, 540)):
        w = 150 + row * 50
        xs = 160 - row * 40
        d.rectangle([xs, y - 18 - row * 4, xs + w, y], fill=C((52, 34, 38)), outline=C((14, 8, 10)))
        d.rectangle([xs - 4, y, xs + w + 4, y + 8 + row * 3], fill=C((40, 26, 30)), outline=C((14, 8, 10)))
        d.line([xs + 2, y - 16 - row * 4, xs + w - 2, y - 16 - row * 4], fill=C((86, 60, 66)))
    platform(hd, FOE, 116, 25, (70, 62, 90), (40, 34, 56), outline=(12, 10, 20))
    platform(hd, PLAYER, 232, 50, (70, 62, 90), (40, 34, 56), outline=(12, 10, 20), thick=12)
    save_room("field_hollow_cathedral", hd)
    glass = mask_from(rw, lambda r, g, b: (r + g + b > 120) & ~((r < 20) & (g < 20)))
    gl = blank(); gl.alpha_composite(glow_from_mask(glass, (200, 160, 255), radius=10, gain=1.2, size=rw.size),
                                     (526 - rw.width // 2, 156))
    cm = np.zeros((693, 864), np.float32)
    for x in range(456, 600, 18):
        cm[262 - (x % 3) * 4: 266 - (x % 3) * 4, x + 1:x + 5] = 1
    layers = [layer(F, "rose", gl, z=1, blend=1, anim=S("pulse"), min=60, max=160, period=180),
              layer(F, "candles", glow_from_mask(cm, (255, 200, 110), radius=7, gain=2.2), z=1, blend=1,
                    anim=[S("pulse"), S("flicker")], min=120, max=210, period=25, chance=0.03, dropout=2)]
    for i, (x, ang) in enumerate(((420, 100), (640, 80))):
        layers.append(layer(F, "moon%d" % i, cone(HD, (x, 150), 18, 420, (190, 200, 255), alpha=70, angle=ang), z=2,
                            blend=1, anim=S("pulse"), min=30, max=80, period=240 + i * 60, phase=i * 2))
    extras = {"img001": strip(F, "mist", fog_strip(864, 160, (120, 110, 170), seed=131, scale=28, density=0.55,
                                                   alpha=90), 300, speed=0.5, direction=1, z=4)}
    return {"profile": {S("art_extras"): extras, S("layers"): layers},
            "origins": [[REJ, "battlebgBlacksteepleIndoor (gradient-mapped night violet, extended)"],
                        [OWN, "gothic nave arches and pillars, broken rose window, candle-lit altar, pews, "
                              "moonlight shafts, floor mist"]]}


#---------------------------------------------------------------------------------------------
# NEW_MOON
#---------------------------------------------------------------------------------------------
def new_moon():
    F = "new_moon"
    bg = game_img("rejuvenation", "battlebgStarlight1")
    hd = extend_vanilla(bg, origin=O, blur_out=False)
    hd = grade(hd, mul=(0.7, 0.62, 0.9))
    moon_c, moon_r = (600, 214), 62
    d = ImageDraw.Draw(hd)
    d.ellipse([moon_c[0] - moon_r - 3, moon_c[1] - moon_r - 3, moon_c[0] + moon_r + 3, moon_c[1] + moon_r + 3],
              fill=C((150, 110, 230)))
    d.ellipse([moon_c[0] - moon_r, moon_c[1] - moon_r, moon_c[0] + moon_r, moon_c[1] + moon_r], fill=C((8, 6, 14)))
    d.ellipse([moon_c[0] - moon_r + 6, moon_c[1] - moon_r + 2, moon_c[0] + moon_r + 2, moon_c[1] + moon_r - 4],
              fill=C((14, 10, 22)))
    roof = 150 + 170
    sk, wins = skyline((864, 693), roof, (16, 12, 26), seed=8, min_h=30, max_h=104, min_w=24, max_w=70,
                       windows=[(255, 200, 120), (170, 120, 255)], win_p=0.08, outline=(70, 50, 120))
    hd.alpha_composite(sk)
    hd.alpha_composite(mountains((864, 693), roof + 20, 40, (10, 8, 18), seed=141, rough=1.0, peaks=12,
                                 outline=(90, 60, 150)))
    hd.alpha_composite(Image.new("RGBA", (864, 693 - roof - 20), (10, 8, 18, 255)), (0, roof + 20))
    fl, _ = ground_plane(HD, roof + 20, (36, 30, 50), (16, 12, 26), seed=142, grain=6)
    hd.alpha_composite(fl)
    platform(hd, FOE, 116, 25, (40, 34, 56), (22, 18, 32), outline=(150, 110, 230))
    platform(hd, PLAYER, 232, 50, (40, 34, 56), (22, 18, 32), outline=(150, 110, 230), thick=12)
    save_room("field_new_moon", hd)
    wm = np.zeros((693, 864), np.float32)
    for (x, y) in wins:
        wm[y:y + 3, x:x + 2] = 1
    layers = [layer(F, "corona", soft_glow(moon_c, moon_r * 2.2, (160, 110, 255), alpha=150), z=1, blend=1,
                    anim=S("pulse"), min=50, max=150, period=200),
              layer(F, "windows", glow_from_mask(wm, (255, 190, 140), radius=3, gain=1.5, core=1.0), z=1, blend=1,
                    anim=S("flicker"), opacity=200, min=60, chance=0.01, dropout=10)]
    extras = {"vacuum": "dark004",
              "img001": strip(F, "shadow", fog_strip(864, 160, (40, 20, 70), seed=143, scale=28, density=0.6,
                                                     alpha=130), roof - 40, speed=0.5, direction=-1, z=4)}
    return {"profile": {S("art_extras"): extras, S("layers"): layers},
            "origins": [[REJ, "battlebgStarlight1 (starfield, darkened)"],
                        [EBDX, "dark004 (vacuum rings)"],
                        [OWN, "dark moon with violet corona, Underveil rooftops and windows, violet rim light"]]}


#---------------------------------------------------------------------------------------------
# MINDSCAPE
#---------------------------------------------------------------------------------------------
def bookshelf(w, h, seed=0):
    rng = random.Random(seed)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w - 1, h - 1], fill=C((90, 60, 110)), outline=C((30, 16, 40)))
    for y in range(6, h - 10, 22):
        x = 5
        while x < w - 8:
            bw = rng.randint(4, 8)
            bh = rng.randint(12, 18)
            d.rectangle([x, y + 18 - bh, x + bw, y + 18], fill=C(rng.choice([(220, 120, 180), (140, 120, 240),
                                                                              (240, 200, 120), (120, 200, 220),
                                                                              (250, 240, 250)])),
                        outline=C((40, 20, 50)))
            x += bw + 1
        d.rectangle([2, y + 18, w - 3, y + 21], fill=C((60, 36, 80)))
    return im


def stairs(n=8, step=(22, 10), color=(230, 210, 250), outline=(90, 60, 130)):
    w, h = n * step[0] + 4, n * step[1] + 30
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i in range(n):
        x = i * step[0]; y = h - 30 - (i + 1) * step[1]
        d.rectangle([x, y, x + step[0], y + step[1]], fill=C(color), outline=C(outline))
        d.rectangle([x, y + step[1], x + step[0], y + step[1] + 16], fill=C(darker(color, 0.75)), outline=C(outline))
    return im


def door(w=40, h=70, frame=(240, 220, 255), glow=(255, 240, 200), outline=(90, 60, 130)):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w - 1, h - 1], fill=C(frame), outline=C(outline))
    d.rectangle([5, 5, w - 6, h - 1], fill=C(glow), outline=C(outline))
    return im


def mindscape():
    F = "mindscape"
    hd = vanilla("reborn", "Psychic", base="Psychic")
    hd = gradient_map(hd, [(0, (40, 26, 90)), (0.35, (120, 90, 190)), (0.65, (220, 170, 235)), (1, (255, 236, 250))])
    floor_top = 320
    hd.alpha_composite(checker_plane(HD, floor_top, (236, 220, 250), (196, 170, 236), n=12, line=(250, 244, 255)))
    # reflection of the dream in the glassy floor
    refl = hd.crop((0, floor_top - 200, 864, floor_top)).transpose(Image.FLIP_TOP_BOTTOM)
    hd = blend(hd, onto(refl, 0, floor_top), "softlight", 0.6)
    pr = penrose(150)
    paste(hd, pr, 300, 300, "bottom")
    st = stairs()
    paste(hd, st, 760, 300, "bottom")
    paste(hd, st.transpose(Image.FLIP_TOP_BOTTOM), 210, 156, "topleft")
    paste(hd, st.rotate(90, expand=True), 690, 150, "topleft")
    dr = door()
    paste(hd, dr, 640, 300, "bottom")
    for c, rx, ry, t in ((FOE, 116, 25, 6), (PLAYER, 232, 50, 10)):
        platform(hd, c, rx, ry, (250, 236, 255), (200, 170, 230), outline=(140, 90, 190), thick=t)
        d = ImageDraw.Draw(hd)
        for k, f in enumerate((0.85, 0.6, 0.35)):
            d.ellipse([c[0] - rx * f, c[1] - ry * f, c[0] + rx * f, c[1] + ry * f], outline=C((255, 120, 220)))
    save_room("field_mindscape", hd)
    layers = [layer(F, "door", soft_glow((640, 266), 60, (255, 240, 200), alpha=200), z=1, blend=1,
                    anim=S("pulse"), min=80, max=200, period=120),
              layer(F, "penrose", soft_glow((300, 230), 120, (255, 160, 240), alpha=120), z=1, blend=1,
                    anim=S("pulse"), min=30, max=120, period=170, phase=1.0)]
    for i, (x, y, w, h, ang) in enumerate(((200, 230, 60, 110, -10), (700, 330, 54, 90, 14), (430, 160, 90, 56, 4))):
        bs = bookshelf(w, h, seed=i).rotate(ang, expand=True, resample=Image.NEAREST)
        layers.append(layer(F, "shelf%d" % i, onto(bs, x, y), z=1 if y < 300 else 22, anim=S("bob"), amp=4,
                            period=160 + i * 40, phase=i))
    rng = random.Random(9)
    for i in range(8):
        bk = Image.new("RGBA", (18, 12), (0, 0, 0, 0)); bd = ImageDraw.Draw(bk)
        col = rng.choice([(220, 120, 180), (140, 120, 240), (240, 200, 120), (250, 240, 250)])
        bd.polygon([(0, 2), (9, 4), (18, 2), (18, 10), (9, 12), (0, 10)], fill=C(col), outline=C((60, 30, 80)))
        bd.line([(9, 4), (9, 12)], fill=C((60, 30, 80)))
        x, y = rng.uniform(180, 740), rng.uniform(170, 300)
        layers.append(layer(F, "book%d" % i, onto(bk, x, y), anchor=(x + 9, y + 6), z=2 if y < 260 else 26,
                            anim=[S("bob"), S("sway")], amp=5, period=100 + i * 13, phase=i))
    extras = {"vacuum": "dark006",
              "img001": strip(F, "thought", fog_strip(864, 140, (255, 220, 255), seed=151, scale=22, density=0.5,
                                                      alpha=90), 240, speed=0.5, direction=1, z=3)}
    return {"profile": {S("art_extras"): extras, S("layers"): layers},
            "origins": [[REB, "battlebgPsychic (pastel gradient map)"],
                        [EBDX, "dark006 (vacuum rings)"],
                        [OWN, "Penrose triangle, impossible stairs, glowing door, floating library shelves and books, "
                              "mirror-glass checker floor, rune-ring platforms, thought mist"]]}


#---------------------------------------------------------------------------------------------
# INVERSE
#---------------------------------------------------------------------------------------------
def island_from(src, box, w, seed=0):
    """A floating island: a crop of other art, colour-inverted and flipped, with a rocky underside."""
    rng = random.Random(seed)
    cr = src.crop(box).resize((w, int(w * (box[3] - box[1]) / (box[2] - box[0]))), Image.NEAREST)
    a = arr(cr)
    a[..., :3] = 255 - a[..., :3]
    cr = img(a).transpose(Image.FLIP_TOP_BOTTOM)
    h = cr.height
    im = Image.new("RGBA", (w, h + 60), (0, 0, 0, 0))
    mask = Image.new("L", (w, h), 0); md = ImageDraw.Draw(mask)
    md.ellipse([0, 0, w, h * 1.6], fill=255)
    im.paste(cr, (0, 60), mask)
    d = ImageDraw.Draw(im)
    pts = [(0, 60 + h * 0.2)]
    for i in range(1, 8):
        pts.append((w * i / 8, 60 + h * 0.2 - rng.uniform(20, 60) * math.sin(i / 8 * math.pi)))
    pts.append((w, 60 + h * 0.2))
    d.polygon(pts, fill=C((200, 210, 220)), outline=C((255, 255, 255)))
    return im


def inverse():
    F = "inverse"
    hd = vanilla("reborn", "Inverse")
    src = game_img("rejuvenation", "battlebgForest")
    layers = []
    for i, (box, w, x, y) in enumerate((((0, 120, 200, 220), 170, 190, 170), ((300, 140, 512, 260), 190, 600, 150),
                                       ((100, 200, 300, 288), 110, 410, 196))):
        isl = island_from(src, box, w, seed=i)
        layers.append(layer(F, "island%d" % i, onto(isl, x, y), z=1, anim=S("bob"), amp=6, period=200 + i * 50,
                            phase=i * 2))
    save_room("field_inverse", hd)
    extras = {"img001": strip(F, "static", fog_strip(864, 120, (255, 255, 255), seed=161, scale=10, density=0.4,
                                                     alpha=50), 260, speed=2, direction=-1, z=3)}
    return {"profile": {S("art_extras"): extras, S("layers"): layers},
            "origins": [[REB, "battlebgInverse, enemybaseInverse"],
                        [REJ, "battlebgForest (inverted crops as upside-down floating islands)"],
                        [OWN, "floating island undersides, static mist"]]}


#---------------------------------------------------------------------------------------------
# PRISM_ARENA
#---------------------------------------------------------------------------------------------
PLATE_COLS = [(255, 80, 80), (255, 150, 60), (255, 220, 80), (160, 230, 70), (60, 200, 110), (60, 210, 200),
              (70, 170, 255), (110, 110, 255), (170, 100, 250), (230, 90, 220), (255, 110, 170), (200, 200, 200),
              (140, 110, 80), (120, 80, 170), (90, 90, 110), (250, 250, 230), (60, 60, 60), (180, 140, 250)]


def prism_arena():
    F = "prism_arena"
    hd = vanilla("reborn", "Champion", base=False)
    hd = gradient_map(hd, [(0, (8, 8, 26)), (0.4, (30, 24, 70)), (0.7, (90, 60, 130)), (1, (250, 200, 160))])
    W, H = HD
    d = ImageDraw.Draw(hd)
    rng = random.Random(4)
    # stands: three tiers sweeping around the arena, packed with glow-stick crowd lights
    for k, (top, col) in enumerate(((168, (26, 22, 50)), (214, (36, 30, 64)), (258, (46, 38, 78)))):
        d.chord([-240, top, W + 240, top + 560 - k * 70], 180, 360, fill=C(col), outline=C((230, 190, 90)))
        for _ in range(1100):
            x = rng.uniform(0, W); y = rng.uniform(top + 6, top + 44)
            d.point((x, y), fill=C(rng.choice(PLATE_COLS[:11] + [(255, 255, 255)] * 4)))
    floor_top = 306
    fl = checker_plane(HD, floor_top, (40, 34, 72), (30, 26, 58), n=10, line=(70, 60, 110))
    hd.alpha_composite(fl)
    # floor sigil: glowing gold rings and 18 coloured segments
    cx, cy = FOE[0], 440
    for i in range(18):
        a0 = i * 20
        d.arc([cx - 360, cy - 110, cx + 360, cy + 110], a0 + 1, a0 + 19, fill=C(PLATE_COLS[i]), width=8)
        a = math.radians(a0)
        d.line([(cx + math.cos(a) * 140, cy + math.sin(a) * 42), (cx + math.cos(a) * 350, cy + math.sin(a) * 106)],
               fill=C((230, 190, 90)))
    for rx, ry in ((372, 114), (346, 102), (140, 42), (100, 30)):
        d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], outline=C((250, 220, 120)), width=2)
    # the 18 Plates hung in a ring over the arena
    plates = []
    for i in range(18):
        a = i / 18 * 2 * math.pi + 0.1
        x = 520 + math.cos(a) * 330
        y = 196 + math.sin(a) * 34
        plates.append((math.sin(a), x, y, i))
    for _, x, y, i in sorted(plates):
        pw, ph = 22, 30
        d.line([x, y - ph / 2, x, 140], fill=C((180, 160, 110)))
        d.rectangle([x - pw / 2, y - ph / 2, x + pw / 2, y + ph / 2], fill=C(PLATE_COLS[i]), outline=C((40, 30, 20)))
        d.rectangle([x - pw / 2 + 3, y - ph / 2 + 3, x + pw / 2 - 3, y + ph / 2 - 3], outline=C(lighter(PLATE_COLS[i], 0.5)))
    for c, rx, ry, t in ((FOE, 116, 25, 8), (PLAYER, 232, 50, 14)):
        platform(hd, c, rx, ry, (240, 236, 250), (180, 176, 200), outline=(120, 100, 60), thick=t, rim=(255, 220, 120))
    save_room("field_prism_arena", hd)
    pm = np.zeros((693, 864), np.float32)
    for _, x, y, i in plates:
        pm[int(y) - 15:int(y) + 15, int(x) - 11:int(x) + 11] = 1
    sm = mask_from(hd, lambda r, g, b: (np.maximum(np.maximum(r, g), b) > 150) & (np.arange(693)[:, None] > floor_top + 20))
    layers = [layer(F, "plates", glow_from_mask(pm, (255, 255, 255), radius=10, gain=1.0), z=1, blend=1,
                    anim=S("pulse"), min=60, max=170, period=120),
              layer(F, "sigil", glow_from_mask(sm, (255, 230, 200), radius=6, gain=1.0, core=0.4), z=1, blend=1,
                    anim=S("pulse"), min=40, max=150, period=150, phase=1.0)]
    for i, x in enumerate((240, 800)):
        layers.append(layer(F, "beam%d" % i, cone(HD, (x, 693), 10, 700, (220, 220, 255), alpha=60,
                                                  angle=-80 if i == 0 else -100), z=1, blend=1,
                            anim=S("sway"), amp=6, period=300 + i * 70, opacity=150))
    extras = {"lightsA": True,
              "img001": strip(F, "prism", fog_strip(864, 100, (255, 230, 255), seed=171, scale=20, density=0.45,
                                                    alpha=60), 250, speed=1, direction=1, z=3)}
    return {"profile": {S("art_extras"): extras, S("layers"): layers},
            "origins": [[REB, "battlebgChampion (gradient-mapped night, as the arena sky glow)"],
                        [EBDX, "lightsA"],
                        [OWN, "Crownhaven stands with crowd lights, the 18 Plates ring, prismatic floor sigil, "
                              "searchlights, marble platforms"]]}


#---------------------------------------------------------------------------------------------
# BLEED: shards of the other fields bleeding through torn reality
#---------------------------------------------------------------------------------------------
def bleed():
    F = "bleed"
    base = game_img("rejuvenation", "battlebgDimensional")
    hd = extend_vanilla(base, origin=O)
    hd = grade(hd, mul=(1.0, 0.7, 0.8), contrast=1.1)
    rng = random.Random(13)
    others = ["field_volcanic", "field_silkwood", "field_neon_grid", "field_frozen_lake", "field_crystal_cavern",
              "field_fairy_tale", "field_water_surface", "field_desert", "field_factory", "field_hollow_cathedral",
              "field_grand_stage", "field_beach"]
    shards = []
    for i, n in enumerate(others):
        p = os.path.join(OUT, "battlebg", n + "_hd.png")
        if not os.path.exists(p):
            continue
        src = Image.open(p).convert("RGBA")
        spots = [(240, 220), (420, 190), (640, 200), (230, 420), (720, 380), (380, 500), (560, 520), (160, 560),
                 (780, 560), (470, 250), (300, 320), (680, 470)]
        cx, cy = spots[i % len(spots)]
        cx += rng.uniform(-30, 30); cy += rng.uniform(-30, 30)
        r = rng.uniform(80, 130)
        pts = [(cx + math.cos(a) * r * rng.uniform(0.5, 1.2), cy + math.sin(a) * r * rng.uniform(0.5, 1.2))
               for a in sorted(rng.uniform(0, 2 * math.pi) for _ in range(rng.randint(3, 5)))]
        mask = Image.new("L", HD, 0); ImageDraw.Draw(mask).polygon(pts, fill=255)
        piece = Image.new("RGBA", HD, (0, 0, 0, 0)); piece.paste(src, (0, 0), mask)
        # chromatic split: red ghost left, cyan ghost right
        r_ = arr(piece); rch = r_.copy(); rch[..., 1:3] = 0; cch = r_.copy(); cch[..., 0] = 0
        hd.alpha_composite(img(rch).transform(HD, Image.AFFINE, (1, 0, 4, 0, 1, 0)), (0, 0))
        hd = blend(hd, img(cch).transform(HD, Image.AFFINE, (1, 0, -4, 0, 1, 0)), "screen", 0.8)
        hd.alpha_composite(piece)
        ImageDraw.Draw(hd).polygon(pts, outline=C((255, 255, 255)))
        shards.append(pts)
    platform(hd, FOE, 116, 25, (40, 10, 20), (20, 4, 10), outline=(255, 40, 70))
    platform(hd, PLAYER, 232, 50, (40, 10, 20), (20, 4, 10), outline=(255, 40, 70), thick=12)
    save_room("field_bleed", hd)
    # glitch slices that flicker in and out
    layers = []
    for i in range(4):
        y = rng.randint(60, 600); h = rng.randint(4, 14)
        sl = hd.crop((0, y, 864, y + h))
        a = arr(sl); a[..., 0] = np.minimum(255, a[..., 0] * 1.4); sl = img(a)
        im = blank(); im.alpha_composite(sl, (rng.randint(-30, 30), y))
        layers.append(layer(F, "slice%d" % i, im, z=2 if i < 2 else 26, anim=S("flicker"), opacity=0, min=230,
                            chance=0.04, dropout=6))
    edge = np.zeros((693, 864), np.float32)
    em = Image.new("L", HD, 0); ed = ImageDraw.Draw(em)
    for pts in shards:
        ed.polygon(pts, outline=255)
    edge = np.asarray(em, np.float32) / 255
    layers.append(layer(F, "tears", glow_from_mask(edge, (255, 60, 90), radius=4, gain=1.5, core=1.0), z=1, blend=1,
                        anim=S("pulse"), min=60, max=200, period=40))
    return {"profile": {S("layers"): layers},
            "origins": [[REJ, "battlebgDimensional (red-graded)"],
                        [OWN, "torn-reality collage: shards of Prismfall's own field rooms with chromatic split, "
                              "glitch slices, glowing tears"]]}


BUILDERS = {"FACTORY": factory, "SCRAPYARD": scrapyard, "GRAND_STAGE": grand_stage, "NEON_GRID": neon_grid,
            "HOLLOW_CATHEDRAL": hollow_cathedral, "NEW_MOON": new_moon, "MINDSCAPE": mindscape, "INVERSE": inverse,
            "PRISM_ARENA": prism_arena, "ZZ_BLEED": bleed}
