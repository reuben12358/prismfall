"""War-climax fields (Ch19): FLOODED_DUNES and GLASS_DUNES. Both are the DESERT room (aveontrainer's painted dunes)
in a new state - the same horizon, dunes, mesa, cacti and platform spots - so DESERT -> FLOODED_DUNES -> GLASS_DUNES
reads as one place: the sea arriving, then the white fire glassing it."""
import scipy.ndimage as ndi
import fields_a, fields_f
from bblib import *
from paint import *
from props import *
from rubygen import S
from fields_a import REJ, REB, DES, EBDX, OWN, O
from fields_f import AVEON, art, sheet_layer

SEA_HORIZON = 232      # HD y where the far sea meets the low sky (in the valley gap)


def _bare():
    return extend_vanilla(art("battlebgdesert_by_aveontrainer_ddp4tzl.png"), origin=O)


def _masks(hd):
    a = arr(hd)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    sky = (b > r + 15) | ((r > 215) & (g > 215) & (b > 200))
    cactus = ndi.binary_opening((g > r + 10) & (g > b), iterations=2)
    rock = (g / np.maximum(r, 1) < 0.62) & ~cactus & ~sky
    sand = ~sky & ~cactus & ~rock
    H, W = sand.shape
    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    n = noise((W, H), 9, 801, 2)
    shore = 284 + (n - 0.5) * 14                                        # where the far dunes meet the flooded valley
    hump = np.where(xs < 150, 392, 392 - (xs - 150) * 0.52) + (n - 0.5) * 18   # the left dune slope stays a crest

    def bar(cx, cy, rx, ry):
        return (((xs - cx) / rx) ** 2 + ((ys - cy) / ry) ** 2 + (n - 0.5) * 0.35) < 1.0
    sandbars = bar(526, 334, 150, 34) | bar(261, 580, 300, 78) | bar(820, 560, 120, 50)
    water = (ys > shore) & ~(ys < hump) & ~sandbars & ~rock & ~cactus & ~sky
    water = ndi.binary_opening(water, iterations=2)
    return dict(sky=sky, cactus=cactus, rock=rock, sand=sand & ~water, water=water, ys=ys, xs=xs)


def _shore_band(water, width):
    """Pixels of land within `width` px of the water (the wet line / glass rim)."""
    grown = ndi.binary_dilation(water, iterations=width)
    return grown & ~water


def _depth(water):
    """0 at the shore, 1 in the deepest water (pixel-art stepped)."""
    d = ndi.distance_transform_edt(water)
    d = np.clip(d / 40.0, 0, 1)
    return np.round(d * 4) / 4


def _lum(a):
    return (a[..., :3] * np.array([0.299, 0.587, 0.114])).sum(-1) / 255.0


def _ramp(lum, stops):
    out = np.zeros(lum.shape + (3,), np.float32)
    xs = [s[0] for s in stops]
    for c in range(3):
        out[..., c] = np.interp(lum, xs, [s[1][c] for s in stops])
    return out


def _sky(m, top, bottom, sea=None):
    H = 693
    ys = m["ys"]
    t = np.clip((ys - 0) / 300.0, 0, 1)[..., None]
    col = np.array(top, np.float32) * (1 - t) + np.array(bottom, np.float32) * t
    if sea is not None:
        seam = (ys > SEA_HORIZON)[..., None]
        col = np.where(seam, np.array(sea, np.float32), col)
    return col


#---------------------------------------------------------------------------------------------
# FLOODED_DUNES
#---------------------------------------------------------------------------------------------
def flooded_dunes():
    F = "flooded_dunes"
    hd = _bare()
    m = _masks(hd)
    a = arr(hd)
    lum = _lum(a)
    out = a.copy()
    # low rain sky with the grey Northern Sea on the horizon
    skycol = _sky(m, (84, 98, 116), (176, 188, 196), sea=(96, 120, 124))
    cl = noise(HD, 30, 811, 3)
    skycol = skycol * (0.9 + 0.18 * np.round(cl * 4)[..., None] / 4)
    out[..., :3] = np.where(m["sky"][..., None], skycol, out[..., :3])
    # pale wet bone-white sand
    sand_rgb = _ramp(lum, [(0.2, (82, 76, 66)), (0.45, (150, 142, 124)), (0.62, (198, 192, 174)),
                           (0.78, (226, 222, 206)), (1.0, (244, 242, 232))])
    out[..., :3] = np.where(m["sand"][..., None], sand_rgb, out[..., :3])
    wet = _shore_band(m["water"], 7) & m["sand"]
    out[..., :3] = np.where(wet[..., None], out[..., :3] * 0.62 + np.array([20, 30, 34]) * 0.38, out[..., :3])
    # wet dark rock and cacti
    rock_rgb = _ramp(lum, [(0.1, (30, 22, 26)), (0.35, (78, 52, 50)), (0.6, (124, 88, 74)), (1.0, (170, 138, 116))])
    out[..., :3] = np.where(m["rock"][..., None], rock_rgb, out[..., :3])
    out[..., :3] = np.where(m["cactus"][..., None], out[..., :3] * np.array([0.7, 0.82, 0.86]), out[..., :3])
    # the flood-sea: shallow turquoise-grey at the shores, deep green-grey in the hollows, swell lines
    dep = _depth(m["water"])
    sea = np.array([126, 168, 160], np.float32) * (1 - dep[..., None]) + np.array([48, 86, 92], np.float32) * dep[..., None]
    swell = (np.sin(m["xs"] / 23.0 + np.sin(m["ys"] / 9.0) * 1.6 + m["ys"] * 0.9) > 0.86)
    sea = np.where(swell[..., None], sea + 26, sea)
    out[..., :3] = np.where(m["water"][..., None], sea, out[..., :3])
    hd = img(out)
    # foam lines at every waterline
    foam = _shore_band(~m["water"], 2) & m["water"]
    fa = arr(hd)
    fa[foam] = [236, 244, 244, 255]
    hd = img(fa)
    # sandbar platforms: wet sand with a foam ring
    for c, rx, ry, t in ((FOE, 116, 25, 8), (PLAYER, 232, 50, 14)):
        platform(hd, c, rx, ry, (214, 208, 190), (120, 112, 98), outline=(60, 56, 50), thick=t,
                 speckle=([(170, 164, 146), (236, 232, 220)], int(rx * 1.4)))
        ImageDraw.Draw(hd).arc([c[0] - rx - 4, c[1] - ry - 2, c[0] + rx + 4, c[1] + ry + t + 4], 0, 180,
                               fill=(240, 248, 248, 255), width=2)
    hd = blend(hd, vgradient(HD, [(0, (150, 180, 210, 70)), (0.5, (150, 190, 210, 30)), (1, (40, 70, 90, 60))]),
               "softlight")
    fields_a.save_room("field_flooded_dunes", hd)
    # --- animated layers
    W = m["water"]
    hi = np.zeros(W.shape, np.float32)
    rng = random.Random(5)
    ys_, xs_ = np.nonzero(W)
    hl = blank(); d = ImageDraw.Draw(hl)
    for k in rng.sample(range(len(xs_)), 900):
        x, y = xs_[k], ys_[k]
        L = 3 + (y - 280) / 40.0
        d.line([(x, y), (x + L, y)], fill=(230, 245, 245, 220))
    ha = arr(hl); ha[..., 3] *= ndi.binary_erosion(W, iterations=3)
    hl = img(ha)
    tide = np.zeros(W.shape, np.float32)
    tide[_shore_band(~W, 5) & W] = 1
    layers = [layer(F, "swellA", hl, z=1, anim=[S("drift"), S("pulse")], amp=5, min=60, max=200, period=210),
              layer(F, "swellB", hl.transpose(Image.FLIP_LEFT_RIGHT) if False else hl, z=1,
                    anim=[S("drift"), S("pulse")], amp=5, min=40, max=160, period=170, phase=2.4),
              layer(F, "tide", glow_from_mask(tide, (240, 250, 250), radius=1, gain=0.6, core=1.0), z=1,
                    anim=[S("bob"), S("pulse")], amp=2.5, min=90, max=230, period=180),
              layer(F, "sheen", soft_glow((470, 420), 420, (200, 230, 255), alpha=70, squash=0.4), z=1, blend=1,
                    anim=S("pulse"), min=20, max=70, period=240)]
    clouds = fog_strip(864, 130, (70, 82, 98), seed=812, scale=30, density=0.65, alpha=170, fade_top=False)
    extras = {"img001": strip(F, "rainclouds", clouds, 150, speed=1, direction=-1, z=1),
              "img002": strip(F, "spray", fog_strip(864, 70, (236, 246, 250), seed=813, scale=12, density=0.45,
                                                    alpha=110), SEA_HORIZON - 30, speed=2, direction=1, z=2)}
    fx = [P(type=":streak", count=40, shape=":rect", w=12, h=1, colors=[[210, 225, 240], [180, 200, 220]],
            angle=102, speed=[7, 10], zoom=[0.6, 1.0], opacity=[110, 190], layers=[":back", ":mid", ":front"]),
          P(type=":drift", count=14, shape=":dot", size=2, colors=[[255, 255, 255], [210, 235, 250]], dir=1,
            area=[0, 110, 384, 300], speed=[1.0, 2.0], sway=10, zoom=[0.5, 0.9], opacity=[150, 230],
            layers=[":back", ":mid", ":front"]),
          P(type=":twinkle", count=14, shape=":spark", size=5, colors=[[255, 255, 255], [210, 240, 255]],
            area=[0, 130, 384, 300], speed=[2, 5], zoom=[0.5, 0.9], opacity=[160, 255], layers=[":back", ":mid"],
            blend=1)]
    return {"profile": {S("art_extras"): extras, S("layers"): layers, S("fx"): fx},
            "origins": [[AVEON, "battlebgdesert (the DESERT room's painted dunes, mesa and cacti, recoloured wet "
                                "bone-white)"],
                        [OWN, "flood-sea filling the hollows (depth-stepped), foam lines, wet sand bands, rain sky "
                              "with the grey sea on the horizon, sandbar platforms, swell and tide-line layers, rain, "
                              "spray, glints"]]}


#---------------------------------------------------------------------------------------------
# GLASS_DUNES
#---------------------------------------------------------------------------------------------
def glass_wave(w=150, h=110):
    """A breaking wave set into green glass mid-curl (pivot bottom-left)."""
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    out, deep, mid, hi = (6, 18, 14), (14, 52, 38), (34, 104, 74), (170, 240, 200)
    body = [(0, h - 1), (w * 0.12, h * 0.72), (w * 0.3, h * 0.42), (w * 0.52, h * 0.16), (w * 0.72, h * 0.04),
            (w * 0.9, h * 0.08), (w * 0.98, h * 0.22), (w * 0.9, h * 0.32), (w * 0.8, h * 0.24), (w * 0.7, h * 0.3),
            (w * 0.66, h * 0.5), (w * 0.72, h * 0.8), (w * 0.86, h - 1)]
    d.polygon(body, fill=C(mid), outline=C(out))
    hollow = [(w * 0.64, h * 0.52), (w * 0.7, h * 0.32), (w * 0.8, h * 0.27), (w * 0.86, h * 0.34), (w * 0.8, h * 0.6),
              (w * 0.76, h * 0.86), (w * 0.68, h * 0.8)]
    d.polygon(hollow, fill=C(deep), outline=C(out))
    for k in range(5):     # refraction streaks along the face
        t = 0.2 + k * 0.13
        d.line([(w * t * 0.9, h * (0.95 - t * 0.8)), (w * (t * 0.9 + 0.18), h * (0.98 - t * 0.6))],
               fill=C(lighter(mid, 0.35)), width=2)
    d.line([(w * 0.3, h * 0.42), (w * 0.52, h * 0.16), (w * 0.72, h * 0.04), (w * 0.9, h * 0.08), (w * 0.98, h * 0.22)],
           fill=C(hi), width=2)
    d.line([(w * 0.12, h * 0.72), (w * 0.3, h * 0.42)], fill=C(lighter(mid, 0.5)), width=1)
    for (x, y) in ((w * 0.92, h * 0.2), (w * 0.85, h * 0.32), (w * 0.95, h * 0.27)):    # frozen spray droplets
        d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=C(hi), outline=C(out))
    return im


def glass_dunes():
    F = "glass_dunes"
    hd = _bare()
    m = _masks(hd)
    a = arr(hd)
    lum = _lum(a)
    out = a.copy()
    # white-fire haze: pale mint at the horizon, deep teal-grey above
    skycol = _sky(m, (40, 70, 70), (214, 238, 224))
    out[..., :3] = np.where(m["sky"][..., None], skycol, out[..., :3])
    # sand fused to black-green glass; contrast pushed so the dune shading reads as gloss
    glass = _ramp(lum ** 1.4, [(0.0, (2, 8, 6)), (0.18, (8, 26, 20)), (0.36, (16, 54, 40)), (0.56, (30, 94, 68)),
                               (0.74, (62, 150, 110)), (0.9, (150, 226, 190)), (1.0, (230, 255, 240))])
    land = m["sand"] | m["water"]
    out[..., :3] = np.where(land[..., None], glass, out[..., :3])
    # the flood, glassed: frozen swell ridges in the old water
    ridge = (np.sin(m["xs"] / 23.0 + np.sin(m["ys"] / 9.0) * 1.6 + m["ys"] * 0.9) > 0.86) & m["water"]
    out[..., :3] = np.where(ridge[..., None], np.array([90, 190, 150], np.float32), out[..., :3])
    rim = _shore_band(m["water"], 3) & m["sand"]
    out[..., :3] = np.where(rim[..., None], np.array([120, 210, 170], np.float32), out[..., :3])
    # scorched rock with a glass skin, cacti fused into green glass sculptures
    rock_rgb = _ramp(lum, [(0.1, (10, 10, 12)), (0.4, (40, 36, 40)), (0.7, (80, 76, 78)), (1.0, (140, 150, 146))])
    out[..., :3] = np.where(m["rock"][..., None], rock_rgb, out[..., :3])
    cac = _ramp(lum, [(0.0, (4, 20, 14)), (0.4, (20, 80, 56)), (0.7, (70, 170, 120)), (1.0, (200, 255, 220))])
    out[..., :3] = np.where(m["cactus"][..., None], cac, out[..., :3])
    # boiling pools in the deepest hollows
    deep = ndi.binary_erosion(m["water"], iterations=16)
    deep = ndi.binary_opening(deep, iterations=3)
    pool = np.array([96, 186, 168], np.float32)
    out[..., :3] = np.where(deep[..., None], pool, out[..., :3])
    pr = _shore_band(deep, 2) & ~deep
    out[..., :3] = np.where(pr[..., None], np.array([210, 250, 236], np.float32), out[..., :3])
    hd = img(out)
    # amber seams where the glass is still cooling
    sn = noise(HD, 26, 821, 3)
    seam = (np.abs(sn - 0.5) < 0.012) & land & ~deep & (m["ys"] > 260)
    seam = ndi.binary_dilation(seam, iterations=1)
    sa = arr(hd); sa[seam] = [255, 176, 70, 255]
    hd = img(sa)
    # the breaking wave set in glass, between the mesa and the foe
    wv = glass_wave()
    paste(hd, wv, 300, 342, "topleft") if False else hd.alpha_composite(wv, (296, 342 - wv.height))
    for c, rx, ry, t in ((FOE, 116, 25, 8), (PLAYER, 232, 50, 14)):
        platform(hd, c, rx, ry, (20, 62, 46), (8, 26, 20), outline=(150, 230, 190), thick=t, highlight=True)
        dd = ImageDraw.Draw(hd)
        dd.arc([c[0] - rx * 0.8, c[1] - ry * 0.8, c[0] + rx * 0.8, c[1] + ry * 0.8], 200, 330,
               fill=(200, 255, 230, 255), width=2)
        dd.line([(c[0] - rx * 0.3, c[1] + ry * 0.2), (c[0] + rx * 0.1, c[1] - ry * 0.1), (c[0] + rx * 0.45, c[1] + ry * 0.3)],
                fill=(255, 176, 70, 255), width=1)
    fields_a.save_room("field_glass_dunes", hd)
    # --- animated layers
    spec = mask_from(hd, lambda r, g, b: (g > 200) & (b > 160) & (r > 120))
    pools_lbl, npool = ndi.label(deep)
    centers = []
    for i in range(1, npool + 1):
        ys_, xs_ = np.nonzero(pools_lbl == i)
        if len(xs_) < 120:
            continue
        centers.append((int(xs_.mean()), int(ys_.min()) + 4, len(xs_)))
    centers = sorted(centers, key=lambda c: -c[2])[:4]
    layers = [layer(F, "seams", glow_from_mask(seam.astype(np.float32), (255, 150, 50), radius=5, gain=1.6, core=0.6),
                    z=1, blend=1, anim=S("pulse"), min=70, max=210, period=95),
              layer(F, "facets", glow_from_mask(spec, (220, 255, 235), radius=3, gain=1.2, core=0.5), z=1, blend=1,
                    anim=S("pulse"), min=40, max=170, period=130, phase=1.2),
              layer(F, "pools", glow_from_mask(deep.astype(np.float32), (160, 255, 220), radius=6, gain=0.8, core=0.15),
                    z=1, blend=1, anim=S("pulse"), min=40, max=130, period=60),
              layer(F, "sun", soft_glow((560, 170), 200, (255, 255, 250), alpha=180), z=1, blend=1, anim=S("pulse"),
                    min=110, max=190, period=210)]
    sheet = plume_sheet(color=(240, 250, 246), shade=(186, 214, 204))
    for i, (x, y, _) in enumerate(centers):
        layers.append(sheet_layer(F, "plume", sheet, x, y, 8, 10 + i * 2, z=3 if y < 420 else 23,
                                  zoom=0.9 if y < 420 else 1.3, phase=i * 31, opacity=210))
    # the prismatic Bleed shimmer where the two Imprints lock: a faint hue-cycling band (EBDX RainbowSprite)
    band = np.zeros((150, 864, 4), np.float32)
    xs = np.arange(864)[None, :]
    yy = np.arange(150)[:, None]
    env = np.exp(-((yy - 75) / 40.0) ** 2) * (0.5 + 0.5 * np.sin(xs / 37.0) * np.sin(xs / 91.0 + 1))
    huecol = _ramp((xs / 864.0 * 3) % 1 * np.ones((150, 1)), [(0, (255, 120, 160)), (0.33, (140, 255, 170)),
                                                               (0.66, (130, 170, 255)), (1, (255, 120, 160))])
    band[..., :3] = huecol
    band[..., 3] = np.clip(env, 0, 1) * 70
    save_element("pf_glass_dunes_prism", posterize_alpha(img(band), 6))
    extras = {"img001": {S("bitmap"): "pf_glass_dunes_prism", S("rainbow"): True, S("speed"): 2, S("flat"): True,
                         S("ox"): 0, S("oy"): 0, S("x"): 0, S("y"): round(200 / 2.25, 2), S("zoom_x"): INV,
                         S("zoom_y"): INV, S("z"): 2, S("opacity"): 200},
              "img002": strip(F, "steam", fog_strip(864, 170, (236, 246, 240), seed=822, scale=28, density=0.55,
                                                    alpha=90), 250, speed=0.5, direction=1, z=4)}
    fx = [P(type=":twinkle", count=22, shape=":spark", size=7, colors=[[255, 255, 255], [200, 255, 220]],
            area=[0, 110, 384, 308], speed=[4, 8], zoom=[0.4, 0.9], opacity=[170, 255], layers=[":back", ":mid"],
            blend=1),
          P(type=":rise", count=8, shape=":glow", size=4, colors=[[255, 170, 70], [255, 220, 140]],
            area=[0, 140, 384, 308], speed=[0.3, 0.7], sway=8, zoom=[0.3, 0.6], opacity=[140, 220],
            layers=[":back", ":mid"], blend=1)]
    for (x, y, _) in centers:
        fx.append(vent(x, y, count=5, rise=90, size=18, speed=(0.4, 0.8), opacity=(60, 120), layers=(":back", ":mid")))
    return {"profile": {S("art_extras"): extras, S("layers"): layers, S("fx"): fx},
            "origins": [[AVEON, "battlebgdesert (the DESERT room's dunes fused to black-green glass by gradient map)"],
                        [OWN, "glassed flood ridges, boiling pools, amber cooling seams, breaking wave set in glass, "
                              "glass cacti and platforms, steam plumes (8-cell sheets), facet glints, white-fire sun, "
                              "hue-cycling prismatic shimmer band (EBDX rainbow layer), steam strip"]]}


BUILDERS = {"FLOODED_DUNES": flooded_dunes, "GLASS_DUNES": glass_dunes}
